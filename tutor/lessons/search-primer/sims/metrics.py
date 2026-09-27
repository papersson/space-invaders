"""Evaluation metrics, written out to match the definitions shown in the video, and checked against
trec_eval (through pytrec_eval) in sims/check_metrics.py.

Relevance grades come from the TREC-COVID judgments: 2 relevant, 1 partially relevant, 0 not relevant.
For precision, recall and reciprocal rank a document counts as relevant when its grade is 1 or more,
as trec_eval does. A document nobody judged counts as not relevant.
"""
import math


def load_qrels(path):
    q = {}
    for line in open(path):
        p = line.split()
        if p[0] == "query-id":
            continue
        q.setdefault(p[0], {})[p[1]] = max(int(p[2]), 0)
    return q


def load_run(path):
    r = {}
    for line in open(path):
        qid, _, doc, rank, score, _ = line.split()
        r.setdefault(qid, []).append((int(rank), doc, float(score)))
    return {q: [d for _, d, _ in sorted(v)] for q, v in r.items()}


def precision_at(ranked, grades, k):
    return sum(1 for d in ranked[:k] if grades.get(d, 0) >= 1) / k


def recall_at(ranked, grades, k):
    rel = sum(1 for g in grades.values() if g >= 1)
    return sum(1 for d in ranked[:k] if grades.get(d, 0) >= 1) / rel if rel else 0.0


def reciprocal_rank(ranked, grades):
    for i, d in enumerate(ranked, 1):
        if grades.get(d, 0) >= 1:
            return 1 / i
    return 0.0


def dcg(gains):
    """Gain = the judged grade; discount = log2(rank + 1)."""
    return sum(g / math.log2(i + 1) for i, g in enumerate(gains, 1))


def ndcg_at(ranked, grades, k):
    got = dcg([grades.get(d, 0) for d in ranked[:k]])
    ideal = dcg(sorted(grades.values(), reverse=True)[:k])
    return got / ideal if ideal else 0.0


def judged_at(ranked, grades, k):
    return sum(1 for d in ranked[:k] if d in grades) / k


def evaluate(run, qrels, depth=None):
    out = {}
    for q, grades in qrels.items():
        ranked = run.get(q, [])[:depth] if depth else run.get(q, [])
        out[q] = {"P@10": precision_at(ranked, grades, 10), "R@10": recall_at(ranked, grades, 10),
                  "R@100": recall_at(ranked, grades, 100), "R@1000": recall_at(ranked, grades, 1000),
                  "MRR": reciprocal_rank(ranked, grades), "MRR@10": reciprocal_rank(ranked[:10], grades),
                  "NDCG@10": ndcg_at(ranked, grades, 10), "judged@10": judged_at(ranked, grades, 10)}
    return out


def mean(per_query, key):
    return sum(v[key] for v in per_query.values()) / len(per_query)
