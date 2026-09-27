"""Encode every TREC-COVID document (BEIR version) with a small bi-encoder, in chunks that survive a restart.

    python sims/embed_corpus.py DATA_DIR WORK_DIR

DATA_DIR holds covid_corpus.parquet (see sims/fetch_data.sh). Writes WORK_DIR/emb/chunk_NNN.npy
(float32, L2-normalised, 384 numbers per document) and WORK_DIR/emb/ids.json (the document order).
Model: sentence-transformers/all-MiniLM-L6-v2 (6 layers, 22.7M parameters, 384 dimensions,
max_seq_length 256). Text: title + " " + abstract, as in BEIR.
"""
import json
import sys
import time
from pathlib import Path

import numpy as np
import pandas as pd
import torch
from sentence_transformers import SentenceTransformer

DATA, WORK = Path(sys.argv[1]), Path(sys.argv[2])
MODEL = "sentence-transformers/all-MiniLM-L6-v2"
CHUNK = 4000

torch.set_num_threads(4)
out = WORK / "emb"
out.mkdir(parents=True, exist_ok=True)
c = pd.read_parquet(DATA / "covid_corpus.parquet")
ids = c["_id"].tolist()
(out / "ids.json").write_text(json.dumps(ids))
texts = (c["title"].fillna("") + " " + c["text"].fillna("")).str.strip().tolist()
m = SentenceTransformer(MODEL, device="cpu")
print(MODEL, m.max_seq_length, m.get_sentence_embedding_dimension(), flush=True)
t0 = time.time()
for k, a in enumerate(range(0, len(texts), CHUNK)):
    f = out / f"chunk_{k:03d}.npy"
    if f.exists():
        continue
    e = m.encode(texts[a:a + CHUNK], batch_size=64, normalize_embeddings=True, convert_to_numpy=True)
    np.save(f, e.astype(np.float32))
    print(f"chunk {k} ({a + len(e)}/{len(texts)}) {time.time() - t0:.0f}s", flush=True)
print("done", flush=True)
