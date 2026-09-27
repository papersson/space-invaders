"""Every number the video shows about retrieval quality, from the runs, into data/*.json.

    python sims/make_evidence.py DATA_DIR WORK_DIR

Reads the TREC-COVID qrels (BEIR version), topics and corpus from DATA_DIR and the runs from WORK_DIR
(sims/lucene/Search.java, sims/dense_pipeline.py). The worked examples use the topics' short keyword
queries (what a person types, e.g. "coronavirus origin"); the results table over all fifty topics uses
each topic's question as the query, BEIR's standard setup for this collection, and also records the
keyword-query table. Writes to the lesson's data/ folder.
"""
import json
import math
import re
import sys
from pathlib import Path

import pandas as pd

from metrics import dcg, evaluate, load_qrels, load_run, mean, ndcg_at, precision_at, recall_at

DATA, WORK = Path(sys.argv[1]), Path(sys.argv[2])
OUT = Path(__file__).resolve().parent.parent / "data"
OUT.mkdir(exist_ok=True)
STAGES = [("TF-IDF", "tfidf"), ("BM25", "bm25"), ("dense", "dense"), ("hybrid", "hybrid"),
          ("hybrid + rerank", "hybrid_rerank"), ("BM25 + rerank", "bm25_rerank"), ("dense (HNSW)", "hnsw")]
KEYS = ["NDCG@10", "P@10", "R@100", "R@1000", "MRR", "MRR@10", "judged@10"]

qrels = load_qrels(DATA / "covid_qrels.tsv")
topics = {l.split("\t")[0]: l.rstrip("\n").split("\t")[1:] for l in open(DATA / "covid_topics.tsv")}
corpus = pd.read_parquet(DATA / "covid_corpus.parquet").set_index("_id")
title = lambda d: " ".join(str(corpus.at[d, "title"]).split())
text = lambda d: str(corpus.at[d, "title"]) + " " + str(corpus.at[d, "text"])


def runs_for(form):
    return {tag: load_run(WORK / f"run_{tag}_{form}.txt") for _, tag in STAGES
            if (WORK / f"run_{tag}_{form}.txt").exists()}


def table(form):
    runs = runs_for(form)
    per = {tag: evaluate(r, qrels) for tag, r in runs.items()}
    rows = [{"name": n, "tag": t, **{k: round(mean(per[t], k), 4) for k in KEYS}} for n, t in STAGES if t in per]
    wins = {q: per["dense"][q]["NDCG@10"] - per["bm25"][q]["NDCG@10"] for q in qrels}
    extra = {"dense_beats_bm25": sum(1 for v in wins.values() if v > 0),
             "bm25_beats_dense": sum(1 for v in wins.values() if v < 0),
             "rerank_beats_hybrid": sum(1 for q in qrels if per["hybrid_rerank"][q]["NDCG@10"] > per["hybrid"][q]["NDCG@10"]),
             "rerank_below_hybrid": sum(1 for q in qrels if per["hybrid_rerank"][q]["NDCG@10"] < per["hybrid"][q]["NDCG@10"]),
             "per_topic_ndcg10": {t: {q: round(v["NDCG@10"], 4) for q, v in p.items()} for t, p in per.items()}}
    return rows, extra, runs


rows_q, extra_q, runs_q = table("q")
rows_kw, extra_kw, runs_kw = table("kw")
relevant = [sum(1 for g in v.values() if g >= 1) for v in qrels.values()]
results = {"topics": len(qrels), "table_form": "question", "stages": rows_q, **extra_q,
           "mean_relevant_per_topic": sum(relevant) / len(relevant),
           "keyword_queries": {"stages": rows_kw, **{k: v for k, v in extra_kw.items() if k != "per_topic_ndcg10"}}}
(OUT / "results.json").write_text(json.dumps(results, indent=1))


def top10(runs, tag, q):
    return [{"rank": i + 1, "id": d, "title": title(d), "grade": qrels[q].get(d)} for i, d in enumerate(runs[tag][q][:10])]


# topic 1 ("coronavirus origin") under BM25: the opening's ten results, P/R by cutoff, the NDCG@10 worked example
bm = runs_kw["bm25"]["1"]
g1 = qrels["1"]
grades = [g1.get(d, 0) for d in bm[:10]]
disc = [math.log2(i + 1) for i in range(1, 11)]
ideal = sorted(g1.values(), reverse=True)[:10]
t1 = {"query": topics["1"][0], "question": topics["1"][1], "relevant": sum(1 for g in g1.values() if g >= 1),
      "grade2": sum(1 for g in g1.values() if g == 2), "grade1": sum(1 for g in g1.values() if g == 1),
      "judged": len(g1), "bm25_top10": top10(runs_kw, "bm25", "1"), "tfidf_top10": top10(runs_kw, "tfidf", "1"),
      "pr": [{"k": k, "P": round(precision_at(bm, g1, k), 4), "R": round(recall_at(bm, g1, k), 4),
              "found": sum(1 for d in bm[:k] if g1.get(d, 0) >= 1)} for k in range(1, 1001)],
      "ndcg": {"grades": grades, "log2": disc, "terms": [g / x for g, x in zip(grades, disc)], "dcg": dcg(grades),
               "ideal_grades": ideal, "idcg": dcg(ideal), "ndcg": ndcg_at(bm, g1, 10)}}
# reciprocal rank fusion, worked for the hybrid's top paper
bl = {d: i + 1 for i, d in enumerate(runs_kw["bm25"]["1"])}
dl = {d: i + 1 for i, d in enumerate(runs_kw["dense"]["1"])}
t1["rrf"] = [{"id": d, "title": title(d), "bm25_rank": bl.get(d), "dense_rank": dl.get(d),
              "rrf": sum(1 / (60 + r) for r in (bl.get(d), dl.get(d)) if r)} for d in runs_kw["hybrid"]["1"][:5]]
t1["hybrid_top10"] = top10(runs_kw, "hybrid", "1")
(OUT / "topic1.json").write_text(json.dumps(t1, indent=1))

# topic 16 ("how long does coronavirus survive on surfaces"): vocabulary mismatch, BM25 against dense
g16 = qrels["16"]
rel2 = [d for d, g in g16.items() if g == 2 and d in corpus.index]
words = {w: sum(1 for d in rel2 if re.search(r"\b" + w + r"\b", text(d), re.I))
         for w in ["survive", "survives", "survival", "persistence", "stability", "inanimate", "surfaces"]}
t16 = {"query": topics["16"][0], "question": topics["16"][1], "grade2": len(rel2), "word_counts": words,
       "bm25_top10": top10(runs_kw, "bm25", "16"), "dense_top10": top10(runs_kw, "dense", "16"),
       "ndcg10": {t: round(ndcg_at(runs_kw[t]["16"], g16, 10), 4) for t in ("bm25", "dense", "hybrid", "hybrid_rerank")},
       "p10": {t: precision_at(runs_kw[t]["16"], g16, 10) for t in ("bm25", "dense")}}
(OUT / "topic16.json").write_text(json.dumps(t16, indent=1))

for r in rows_q:
    print(f"{r['name']:16s}", {k: r[k] for k in ("NDCG@10", "P@10", "R@100", "MRR", "judged@10")})
print("topic 1: NDCG@10", round(t1["ndcg"]["ndcg"], 4), "DCG", round(t1["ndcg"]["dcg"], 3), "IDCG", round(t1["ndcg"]["idcg"], 3))
print("rrf", json.dumps(t1["rrf"][:3], indent=0))
print("topic 16", t16["ndcg10"], t16["p10"], t16["word_counts"])
