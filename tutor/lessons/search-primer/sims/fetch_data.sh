#!/bin/sh
# Fetch everything the evidence needs (nothing here is committed): the BEIR release of TREC-COVID,
# NIST's round 5 topics, and the Lucene jars. Models are fetched by sentence-transformers on first
# use: sentence-transformers/all-MiniLM-L6-v2 and cross-encoder/ms-marco-MiniLM-L-6-v2.
#   sh sims/fetch_data.sh DATA_DIR LUCENE_DIR
set -e
D=$1; J=$2
mkdir -p "$D" "$J/jars"
hf=https://huggingface.co/datasets
curl -sSL -o "$D/covid_corpus.parquet" $hf/BeIR/trec-covid/resolve/main/corpus/corpus-00000-of-00001.parquet
curl -sSL -o "$D/covid_queries.parquet" $hf/BeIR/trec-covid/resolve/main/queries/queries-00000-of-00001.parquet
curl -sSL -o "$D/covid_qrels.tsv" $hf/BeIR/trec-covid-qrels/resolve/main/test.tsv
curl -sSL -o "$D/topics-rnd5.xml" https://ir.nist.gov/trec-covid/data/topics-rnd5.xml
for a in lucene-core lucene-analysis-common lucene-queryparser lucene-queries; do
  curl -sSL -o "$J/jars/$a-10.5.1.jar" https://repo1.maven.org/maven2/org/apache/lucene/$a/10.5.1/$a-10.5.1.jar
done
(cd "$D" && sha256sum covid_corpus.parquet covid_queries.parquet covid_qrels.tsv topics-rnd5.xml)
