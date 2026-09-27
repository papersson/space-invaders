"""Check sims/metrics.py against trec_eval (via pytrec_eval) on every run, and print the comparison.

    python sims/check_metrics.py QRELS RUN [RUN ...]
trec_eval measures: ndcg_cut_10 (gain = grade, discount log2(rank + 1)), P_10, recall_100, recall_1000,
recip_rank. Relevance level 1 (the default) makes grades 1 and 2 relevant.
"""
import sys

import pytrec_eval

from metrics import evaluate, load_qrels, load_run, mean

qrels = load_qrels(sys.argv[1])
pairs = {"NDCG@10": "ndcg_cut_10", "P@10": "P_10", "R@100": "recall_100", "R@1000": "recall_1000", "MRR": "recip_rank"}
ev = pytrec_eval.RelevanceEvaluator(qrels, set(pairs.values()))
worst = 0.0
for path in sys.argv[2:]:
    run_list = load_run(path)
    # trec_eval sorts by score and breaks ties by document id, so hand it scores that encode our rank order
    run = {q: {d: float(len(ds) - i) for i, d in enumerate(ds)} for q, ds in run_list.items()}
    te = ev.evaluate(run)
    ours = evaluate(run_list, qrels)
    for k, m in pairs.items():
        a = mean(ours, k)
        b = sum(te[q][m] for q in qrels) / len(qrels)
        worst = max(worst, abs(a - b))
        print(f"{path.split('/')[-1]:28s} {k:8s} ours {a:.4f}  trec_eval {b:.4f}")
print("largest difference", worst)
assert worst < 1e-6
