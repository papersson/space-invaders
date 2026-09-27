"""Dense retrieval, approximate nearest-neighbour search, hybrid fusion and reranking on TREC-COVID.

    python sims/dense_pipeline.py DATA_DIR WORK_DIR [kw|q]

Needs WORK_DIR/emb (sims/embed_corpus.py) and WORK_DIR/run_bm25_<kw|q>.txt (sims/lucene/Search.java).
Writes, in TREC run format (top 1000 per topic unless noted):
  run_dense_<f>.txt          exact cosine similarity against all 171,332 document vectors
  run_hnsw_<f>.txt           HNSW graph search (faiss IndexHNSWFlat, M = 32, efConstruction = 200)
  run_hybrid_<f>.txt         reciprocal rank fusion of BM25 and dense, k = 60 (Cormack et al. 2009)
  run_hybrid_rerank_<f>.txt  the hybrid top 100 re-scored by a cross-encoder, then the rest in hybrid order
  run_bm25_rerank_<f>.txt    the same, starting from BM25's top 100
and WORK_DIR/dense_stats_<f>.json (HNSW distance computations and recall, timings).
Models: sentence-transformers/all-MiniLM-L6-v2 (bi-encoder), cross-encoder/ms-marco-MiniLM-L-6-v2.
"""
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import torch

DATA, WORK = Path(sys.argv[1]), Path(sys.argv[2])
FORM = sys.argv[3] if len(sys.argv) > 3 else "kw"
DEPTH, RERANK, K_RRF = 1000, 100, 60
torch.set_num_threads(4)


def write_run(path, run, tag):
    with open(path, "w") as f:
        for q, docs in run.items():
            for i, (d, s) in enumerate(docs, 1):
                f.write(f"{q} Q0 {d} {i} {s:.6f} {tag}\n")


def read_run(path):
    r = {}
    for line in open(path):
        q, _, d, rank, s, _ = line.split()
        r.setdefault(q, []).append((d, float(s)))
    return r


def main():
    from sentence_transformers import CrossEncoder, SentenceTransformer

    ids = json.loads((WORK / "emb" / "ids.json").read_text())
    E = np.concatenate([np.load(f) for f in sorted((WORK / "emb").glob("chunk_*.npy"))])
    assert len(E) == len(ids), (len(E), len(ids))
    topics = [l.rstrip("\n").split("\t") for l in open(DATA / "covid_topics.tsv")]
    qtext = {t[0]: t[1] if FORM == "kw" else t[2] for t in topics}
    bi = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cpu")
    t0 = time.perf_counter()
    Q = bi.encode([qtext[q] for q in qtext], normalize_embeddings=True, batch_size=64)
    enc_ms = (time.perf_counter() - t0) / len(qtext) * 1000
    stats = {"docs": len(ids), "dim": int(E.shape[1]), "query_encode_ms": enc_ms}

    # exact search: cosine similarity = dot product of unit vectors, against every document
    t0 = time.perf_counter()
    S = Q @ E.T
    stats["exact_ms_per_query"] = (time.perf_counter() - t0) / len(qtext) * 1000
    dense = {}
    for qi, q in enumerate(qtext):
        top = np.argpartition(-S[qi], DEPTH)[:DEPTH]
        top = top[np.argsort(-S[qi][top])]
        dense[q] = [(ids[j], float(S[qi][j])) for j in top]
    write_run(WORK / f"run_dense_{FORM}.txt", dense, "dense-exact")

    # approximate search: HNSW graph
    import faiss
    faiss.omp_set_num_threads(4)
    t0 = time.perf_counter()
    index = faiss.IndexHNSWFlat(E.shape[1], 32, faiss.METRIC_INNER_PRODUCT)
    index.hnsw.efConstruction = 200
    index.add(E)
    stats["hnsw_build_s"] = time.perf_counter() - t0
    stats["hnsw"] = {}
    faiss.omp_set_num_threads(1)
    for ef in (16, 64, 128, 256):
        index.hnsw.efSearch = ef
        recalls, ndis, times = [], [], []
        for qi, q in enumerate(qtext):
            faiss.cvar.hnsw_stats.reset()
            t0 = time.perf_counter()
            D, I = index.search(Q[qi:qi + 1], 10)
            times.append(time.perf_counter() - t0)
            ndis.append(faiss.cvar.hnsw_stats.ndis)
            true10 = {d for d, _ in dense[q][:10]}
            recalls.append(len(true10 & {ids[j] for j in I[0]}) / 10)
        stats["hnsw"][ef] = {"recall@10_vs_exact": float(np.mean(recalls)), "min_recall": float(np.min(recalls)),
                             "distance_computations_mean": float(np.mean(ndis)),
                             "ms_per_query_median": float(np.median(times) * 1000)}
        print("efSearch", ef, stats["hnsw"][ef], flush=True)
    index.hnsw.efSearch = 256
    D, I = index.search(Q, DEPTH)
    write_run(WORK / f"run_hnsw_{FORM}.txt", {q: [(ids[j], float(d)) for j, d in zip(I[qi], D[qi]) if j >= 0]
                                              for qi, q in enumerate(qtext)}, "hnsw-ef256")

    # hybrid: reciprocal rank fusion of the BM25 and dense lists
    bm25 = read_run(WORK / f"run_bm25_{FORM}.txt")
    hybrid = {}
    for q in qtext:
        score = {}
        for lst in (bm25.get(q, []), dense[q]):
            for r, (d, _) in enumerate(lst, 1):
                score[d] = score.get(d, 0.0) + 1.0 / (K_RRF + r)
        hybrid[q] = sorted(score.items(), key=lambda x: -x[1])[:DEPTH]
    write_run(WORK / f"run_hybrid_{FORM}.txt", hybrid, "rrf60")

    # reranking: a cross-encoder reads the query and each candidate together
    ce = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2", device="cpu")
    corpus = pd.read_parquet(DATA / "covid_corpus.parquet").set_index("_id")
    text = lambda d: (str(corpus.at[d, "title"]) + " " + str(corpus.at[d, "text"])).strip()
    times = []
    for name, first in (("hybrid", hybrid), ("bm25", bm25)):
        out = {}
        for q in qtext:
            cand = [d for d, _ in first[q][:RERANK]]
            t0 = time.perf_counter()
            s = ce.predict([(qtext[q], text(d)) for d in cand], batch_size=32)
            times.append(time.perf_counter() - t0)
            top = sorted(zip(cand, map(float, s)), key=lambda x: -x[1])
            floor = min(x for _, x in top) - 1
            rest = [(d, floor - i * 1e-3) for i, (d, _) in enumerate(first[q][RERANK:])]
            out[q] = top + rest
        write_run(WORK / f"run_{name}_rerank_{FORM}.txt", out, f"{name}+ce")
        print("reranked", name, flush=True)
    stats["rerank_s_per_query_100_docs_median"] = float(np.median(times))
    stats["rerank_docs_per_s"] = RERANK / float(np.median(times))
    (WORK / f"dense_stats_{FORM}.json").write_text(json.dumps(stats, indent=1))
    print(json.dumps(stats, indent=1))


if __name__ == "__main__":
    main()
