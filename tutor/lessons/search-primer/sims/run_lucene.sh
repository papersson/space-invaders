#!/bin/sh
# Build the Lucene index and write every Lucene capture the video uses into captures/.
#   sh sims/run_lucene.sh DATA_DIR LUCENE_DIR WORK_DIR      (after sims/fetch_data.sh and sims/to_tsv.py)
set -e
D=$1; J=$2; W=$3
HERE=$(cd "$(dirname "$0")/.." && pwd)
C=$HERE/captures
cp "$HERE/sims/lucene/Search.java" "$J/" && (cd "$J" && javac -cp 'jars/*' Search.java)
run() { (cd "$J" && java -Xmx4g --enable-native-access=ALL-UNNAMED -cp 'jars/*:.' Search "$@" 2>&1 \
  | grep -v -E "JAVA_TOOL|VectorizationProvider|incubator|^$" || true); }
[ -d "$J/idx" ] || run index "$D/covid_corpus.tsv" "$J/idx"
run stats "$J/idx" coronavirus origin > "$C/lucene_stats.txt"
run boolean "$J/idx" coronavirus origin >> "$C/lucene_stats.txt"
run analyze "Zoonotic origins of human coronavirus 2019 (HCoV-19 / SARS-CoV-2): why is this work important?" > "$C/lucene_analyze.txt"
run analyze "how do people die from the coronavirus" >> "$C/lucene_analyze.txt"
run term "$J/idx" Coronavirus coronavirus Origin origin > "$C/lucene_term.txt"
run explain "$J/idx" "coronavirus origin" 10 > "$C/lucene_explain_topic1.txt"
for p in 75773gwg ne5r4d4b 2qto9vsb jkrj0lbm; do run doc "$J/idx" $p coronavirus origin > "$C/lucene_doc_$p.txt"; done
run run "$J/idx" "$D/covid_topics.tsv" 1 1000 "$W/run_bm25_kw.txt"
run run "$J/idx" "$D/covid_topics.tsv" 1 1000 "$W/run_tfidf_kw.txt" tfidf
run run "$J/idx" "$D/covid_topics.tsv" 2 1000 "$W/run_bm25_q.txt"
run run "$J/idx" "$D/covid_topics.tsv" 2 1000 "$W/run_tfidf_q.txt" tfidf
