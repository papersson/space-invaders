"""Per-query costs of the neural stages on this machine (4 CPU cores, no GPU): encoding one query with the
bi-encoder, exact and HNSW vector search, and the cross-encoder reading the top 100 candidates.

    python sims/timing.py DATA_DIR WORK_DIR        -> data/timing_neural.json
"""
import json
import statistics as st
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from sentence_transformers import CrossEncoder, SentenceTransformer

DATA, WORK = Path(sys.argv[1]), Path(sys.argv[2])
torch.set_num_threads(4)
topics = [l.rstrip("\n").split("\t") for l in open(DATA / "covid_topics.tsv")]
E = np.concatenate([np.load(f) for f in sorted((WORK / "emb").glob("chunk_*.npy"))])
bi = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cpu")
ce = CrossEncoder("cross-encoder/ms-marco-MiniLM-L-6-v2", device="cpu")
corpus = pd.read_parquet(DATA / "covid_corpus.parquet").set_index("_id")
hyb = {}
for line in open(WORK / "run_hybrid_q.txt"):
    q, _, d, r, s, _ = line.split()
    if int(r) <= 100:
        hyb.setdefault(q, []).append(d)
enc, exact, rer = [], [], []
for _ in range(3):
    bi.encode(["warm up query"], show_progress_bar=False)
ce.predict([("warm up", "warm up text")] * 32, batch_size=32)
# encodes first, then searches: interleaving numpy's and torch's thread pools adds ~90 ms of thread start-up
vs = []
for t in topics[:20]:
    t0 = time.perf_counter(); vs.append(bi.encode([t[2]], normalize_embeddings=True, show_progress_bar=False)[0])
    enc.append(time.perf_counter() - t0)
for v in vs:
    t0 = time.perf_counter(); s = E @ v; top = np.argpartition(-s, 1000)[:1000]; exact.append(time.perf_counter() - t0)
for t in topics[:8]:
    pairs = [(t[2], str(corpus.at[d, "title"]) + " " + str(corpus.at[d, "text"])) for d in hyb[t[0]]]
    t0 = time.perf_counter(); ce.predict(pairs, batch_size=32); rer.append(time.perf_counter() - t0)
out = {"encode_one_query_ms_median": st.median(enc) * 1000, "exact_search_171332_ms_median": st.median(exact) * 1000,
       "rerank_100_s_median": st.median(rer), "rerank_papers_per_s": 100 / st.median(rer),
       "rerank_all_171332_hours": 171332 / (100 / st.median(rer)) / 3600}
(Path(__file__).resolve().parent.parent / "data" / "timing_neural.json").write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
