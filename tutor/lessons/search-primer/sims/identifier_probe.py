"""Exact identifiers: how many of the top ten from BM25 (Lucene) and from dense retrieval contain the identifier.

    python sims/identifier_probe.py DATA_DIR WORK_DIR LUCENE_RUN_FILE ID [ID ...]
LUCENE_RUN_FILE: a TREC run of the identifier queries made by sims/lucene/Search.java (topic ids 1..n in order).
Writes data/identifiers.json.
"""
import json
import re
import sys
from pathlib import Path

import numpy as np
import pandas as pd
from sentence_transformers import SentenceTransformer

DATA, WORK, LRUN, IDS = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3], sys.argv[4:]
ids = json.loads((WORK / "emb" / "ids.json").read_text())
E = np.concatenate([np.load(f) for f in sorted((WORK / "emb").glob("chunk_*.npy"))])
c = pd.read_parquet(DATA / "covid_corpus.parquet").set_index("_id")
text = lambda d: str(c.at[d, "title"]) + " " + str(c.at[d, "text"])
m = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", device="cpu")
bm = {}
for line in open(LRUN):
    q, _, d, r, s, _ = line.split()
    bm.setdefault(q, []).append(d)
out = []
for k, ident in enumerate(IDS, 1):
    pat = re.compile(r"(?<![A-Za-z0-9])" + re.escape(ident) + r"(?![A-Za-z0-9])", re.I)
    q = m.encode([ident], normalize_embeddings=True)[0]
    top = np.argsort(-(E @ q))[:10]
    dense = [ids[j] for j in top]
    b10 = bm.get(str(k), [])[:10]
    row = {"id": ident, "papers_containing": int(sum(1 for d in c.index if pat.search(text(d)))),
           "bm25_top10_containing": sum(1 for d in b10 if pat.search(text(d))),
           "dense_top10_containing": sum(1 for d in dense if pat.search(text(d))),
           "bm25_titles": [str(c.at[d, "title"])[:120] for d in b10],
           "dense_titles": [str(c.at[d, "title"])[:120] for d in dense]}
    out.append(row)
    print(ident, row["bm25_top10_containing"], row["dense_top10_containing"])
    for t in row["dense_titles"][:10]:
        print("    dense:", t)
(Path(__file__).resolve().parent.parent / "data" / "identifiers.json").write_text(json.dumps(out, indent=1))
