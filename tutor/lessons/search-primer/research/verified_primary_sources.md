# Primary sources checked in this session (2026-09-27)

Every fact below was read in the primary source (fetched in this session) or produced by running the real system. Quotes are verbatim.

## Engines

- **Lucene BM25, exact form (Lucene 10.5.1, run here).** `IndexSearcher.explain` on the TREC-COVID index prints: `idf, computed as log(1 + (N - n + 0.5) / (n + 0.5))` and `tf, computed as freq / (freq + k1 * (1 - b + b * dl / avgdl))` with `1.2 = k1, term saturation parameter`, `0.75 = b, length normalization parameter`, `dl, length of field (approximate)`. There is no (k1 + 1) factor in the numerator (a constant factor; it does not change the ranking). Capture: captures/lucene_explain_topic1.txt.
- **Lucene BM25Similarity Javadoc (10.3):** "BM25 with these default values: k1 = 1.2 b = 0.75"; idf "Implemented as log(1 + (docCount - docFreq + 0.5)/(docFreq + 0.5))". https://lucene.apache.org/core/10_3_0/core/org/apache/lucene/search/similarities/BM25Similarity.html
- **Lucene 6.0 CHANGES:** "LUCENE-6789: IndexSearcher's default Similarity is changed to BM25Similarity. Use ClassicSimilarity to get the old vector space DefaultSimilarity." https://lucene.apache.org/core/6_0_0/changes/Changes.html
- **Elasticsearch similarity docs:** "BM25 similarity (default)"; "k1 Controls non-linear term frequency normalization (saturation). The default value is 1.2"; "b Controls to what degree document length normalizes tf values. The default value is 0.75." https://www.elastic.co/docs/reference/elasticsearch/index-settings/similarity
- **Elasticsearch standard analyzer:** "stopwords ... Defaults to _none_." https://www.elastic.co/docs/reference/text-analysis/analysis-standard-analyzer
- **Elasticsearch term query:** "Avoid using the term query for text fields. By default, Elasticsearch changes the values of text fields as part of analysis. This can make finding exact matches for text field values difficult." ... "The term query does not analyze the search term ... may return poor or no results when searching text fields." https://www.elastic.co/docs/reference/query-languages/query-dsl/query-dsl-term-query
- **Elasticsearch RRF retriever:** "rank_constant ... Defaults to 60." https://www.elastic.co/docs/reference/elasticsearch/rest-apis/reciprocal-rank-fusion
- **Lucene EnglishAnalyzer (10.5.1, run here):** stop set `[but, be, with, such, then, for, no, will, not, are, and, their, if, this, on, into, a, or, there, in, that, they, was, is, it, an, the, as, at, these, by, to, of]` (33 words); chain StandardTokenizer, EnglishPossessiveFilter, LowerCaseFilter, StopFilter, PorterStemFilter. Capture: captures/lucene_analyze.txt.

## Textbook (Manning, Raghavan and Schütze, Introduction to Information Retrieval, 2008, online edition)

- §2.2.2: "The general trend in IR systems over time has been from standard use of quite large stop lists (200-300 terms) to very small stop lists (7-12 terms) to no stop list whatsoever. Web search engines generally do not use stop lists."
- §8.2: "the U.S. National Institute of Standards and Technology (NIST) has run a large IR test bed evaluation series since 1992."
- §8.3: precision and recall "clearly trade off against one another: you can always get a recall of 1 (but very low precision) by retrieving all documents for all queries! Recall is a non-decreasing function of the number of documents retrieved. On the other hand, in a good system, precision usually decreases as the number of documents retrieved is increased."
- §8.4, eq. 8.44: NDCG(Q, k) = (1/|Q|) Σ_j Z_kj Σ_{m=1..k} (2^{R(j,m)} − 1) / log2(1 + m) (exponential gain). NDCG "is designed for situations of non-binary notions of relevance".
- §8.5: "The most standard approach is pooling, where relevance is assessed over a subset of the collection that is formed from the top documents returned by a number of different IR systems".
- §11.4.3, eq. 11.32: BM25 RSV_d = Σ_t log(N/df_t) · (k1 + 1) tf_td / (k1((1 − b) + b × (L_d/L_ave)) + tf_td).

## Papers

- **TREC-COVID** (Voorhees et al., "TREC-COVID: Constructing a Pandemic Information Retrieval Test Collection", SIGIR Forum 54(1), 2020; arXiv:2005.04474): assessors "with clinical expertise": "ten Oregon Health and Science University medical students ... as well as additional relevance assessment help from professional indexers from the National Library of Medicine"; documents marked "'Relevant', 'Partially Relevant', or 'Not Relevant'"; "The computation of NDCG uses gain values of 1 for 'Partially Relevant' documents and 2 for 'Relevant' documents. Measures that use binary judgments are computed using both types of relevant documents as the relevant set."; judging is driven by pools of submitted runs ("Depth-7 pools created from only the first priority run from each team"); "TREC-COVID Round 1 received 143 runs from 56 teams."; "The final pandemic test collection ... will contain the cumulative judgments from all rounds".
- **BEIR** (Thakur et al., NeurIPS 2021 Datasets and Benchmarks; arXiv:2104.08663): TREC-COVID: 50 queries, 171,332 documents, 493.5 relevant documents per query on average, 3-level relevance; nDCG@10 BM25 0.656, BM25 + cross-encoder reranking 0.757; §6: "TREC-COVID used a pooling method to reduce the impact of the ... Hole@10" analysis: dense systems retrieve more unjudged documents (Hole@10 up to 31.8% for TAS-B vs 6.4% for BM25).
- **RRF** (Cormack, Clarke and Büttcher, SIGIR 2009): "RRFscore(d ∈ D) = Σ_{r∈R} 1/(k + r(d)), where k = 60 was fixed during a pilot investigation and not altered during subsequent validation."
- **Joachims, Granka, Pan, Hembrooke and Gay, "Accurately Interpreting Clickthrough Data as Implicit Feedback", SIGIR 2005:** "clicks are informative but biased"; "a 'trust bias' which leads to more clicks on links ranked highly by Google, even if those abstracts are less relevant"; "also under the swapped condition, there is still a strong bias to click on link one even if the second abstract is more relevant."
- **Turpin and Hersh, "Why batch and user evaluations do not give the same results", SIGIR 2001** (title and venue checked on Semantic Scholar; abstract not available).
- **Brutlag, "Speed Matters for Google Web Search", Google, 22 June 2009:** "Experiments demonstrate that increasing web search latency 100 to 400 ms reduces the daily number of searches per user by 0.2% to 0.6%."; "one group of users experienced the delay, while a second group served as the control."
- **HNSW:** Malkov and Yashunin, arXiv:1603.09320 (2016), IEEE TPAMI 2020.
- **Cross-encoder reranking:** Nogueira and Cho, "Passage Re-ranking with BERT", arXiv:1901.04085 (2019).
- **Dense passage retrieval (bi-encoder):** Karpukhin et al., EMNLP 2020, arXiv:2004.04906.
- **Retrieval-augmented generation:** Lewis et al., NeurIPS 2020, arXiv:2005.11401.

## Web

- **Google, "How Google Search organizes information"** (fetched 2026-09-27): "The Google Search index covers hundreds of billions of webpages and is well over 100,000,000 gigabytes in size."
- **Turpin and Hersh, SIGIR 2001, abstract** (OHSU repository, fetched 2026-09-27): "Previous results demonstrated that improved performance as measured by relevance-based metrics in batch studies did not correspond with the results of outcomes based on real user searching tasks. ... while the queries entered by real users into systems yielding better results in batch studies gave comparable gains in ranking of relevant documents for those users, they did not translate into better performance on specific tasks."
- **Manning et al. §1.3:** intersecting two sorted posting lists by walking them "simultaneously, in time linear in the total number of postings entries"; "Our indexing methods gain us just a constant, not a difference in time complexity compared to a linear scan, but in practice the constant is huge."
- **Nogueira and Cho (2019), §2:** "First, a large number (for example, a thousand) of possibly relevant documents to a given question are retrieved from a corpus by a standard mechanism, such as BM25. In the second stage, passage re-ranking, each of these documents is scored and re-ranked by a more computationally-intensive method."
- **BEIR, Appendix:** on TREC-COVID, "approx. 42k out of 171k" papers are titles without an abstract, and the cosine-similarity model "prefers retrieving these documents".
- **all-MiniLM-L6-v2 model card:** fine-tuned "on a 1B sentence pairs dataset" with "a contrastive learning objective".
