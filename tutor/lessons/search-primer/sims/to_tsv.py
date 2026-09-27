"""Write the BEIR TREC-COVID corpus and topics as plain TSV for the Lucene program (sims/lucene/Search.java).

    python sims/to_tsv.py DATA_DIR
Writes DATA_DIR/covid_corpus.tsv (id, title + " " + abstract) and DATA_DIR/covid_topics.tsv
(topic number, keyword query, question) from the official round 5 topics file.
"""
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import pandas as pd

D = Path(sys.argv[1])
c = pd.read_parquet(D / "covid_corpus.parquet")
clean = lambda s: " ".join(str(s).split())
with open(D / "covid_corpus.tsv", "w") as f:
    for i, t, x in zip(c["_id"], c["title"].fillna(""), c["text"].fillna("")):
        f.write(f"{i}\t{clean(t + ' ' + x)}\n")
with open(D / "covid_topics.tsv", "w") as f:
    for t in ET.parse(D / "topics-rnd5.xml").getroot():
        f.write(f"{t.get('number')}\t{clean(t.find('query').text)}\t{clean(t.find('question').text)}\n")
print(len(c), "documents")
