Reviewed the full script and cross-checked every number against the evidence table and against standard IR terminology/formulas. My assessment below.

---

## BLOCKING

**§3 — "Look up Coronavirus exactly as typed, with its capital C, and the index has no such term: zero papers."**
This misattributes the cause of the miss to capitalization alone. The stored term is `coronaviru` (after lowercasing *and* Porter stemming), so a query for the exact string `coronavirus` — all lowercase, capitalization already "fixed" — would *also* return zero hits, since it still isn't stemmed. As worded, a viewer's natural takeaway is "the bug is the capital C, so lowercasing the query would fix it," which is false: you need the full analyzer chain (case-folding *and* stemming), not just case-folding. The on-screen direction actually shows the right supporting data (`Coronavirus → 0`, and separately `coronaviru → 35,095`), so the fix is purely narrational.
**Corrected wording:** "Look up Coronavirus exactly as typed — with its capital C, and without stemming it — and the index has no such term: zero papers. Even lowercased, `coronavirus` still isn't in the dictionary; the stored term is `coronaviru`."

---

## SHOULD FIX

**§4 — "A classic answer is TF-IDF... A paper's score is each word's count times its weight, added up."**
This presents an unnormalized `Σ tf × idf` as simply "TF-IDF," with no caveat, right before showing its length-normalization pathology (the 25×-average-length paper ranking #2). But plenty of "classic" TF-IDF variants (e.g. cosine-normalized vector-space scoring, or Lucene's own historical `ClassicSimilarity`, which divides by `sqrt(numTerms)`) already have *some* length normalization built in. The BM25 footnote gets a careful "as Lucene computes it..." caveat; TF-IDF gets none, so the comparison reads as more universally damning of "TF-IDF" than it is. This narrative arc (raw tf·idf → add saturation → add length norm) is the standard way BM25 is motivated, so it isn't wrong to use it — it just needs the same rigor already applied to BM25.
**Corrected wording:** add a small footnote parallel to BM25's: *"This is the simplest form — a raw sum, with no length normalization. Some classic TF-IDF variants (e.g. cosine-normalized vector space scoring) partially correct for length; BM25's saturation curve is the fix they don't have."*

**§6 — "Reciprocal rank fusion gives a paper one over sixty plus its rank, from each ranking, and adds them up."**
This states "sixty" as if it were fixed by the method, but 60 is a tunable constant (`k`), chosen empirically in Cormack, Clarke & Büttcher (2009) and used as a common default (e.g. Elasticsearch's `rank_constant`). As written it reads as canonical rather than a widely-used default.
**Corrected wording:** "Reciprocal rank fusion gives a paper one over a constant, usually sixty, plus its rank, from each ranking, and adds them up."

**§10 — no caveat that the specific NDCG gains (0.30 → 0.61 → 0.68 → 0.74) are this collection's numbers.**
Every earlier chapter carefully scopes numbers with "in this collection," but §10's summary table states the improvements as flat facts ("BM25 doubles TF-IDF's NDCG..."). For an audience being taught that offline numbers are collection-specific (a point the video itself makes about judgments in §7-8), it's worth one line noting the *ordering* of methods generalizes but the *magnitudes* are specific to TREC-COVID.
**Corrected wording:** append to the paragraph: "These exact numbers are for this collection; the ordering — BM25 over raw TF-IDF, hybrid over either alone, reranking on top — is typical, but the gaps vary by collection and query type."

---

## NITs

**§2/§3 — dictionary initially labeled "coronavirus," later corrected to "coronaviru."** Handled deliberately (chapter 3 explicitly relabels it), but a viewer who pauses on chapter 2's screen will see an inaccurate dictionary entry. Consider showing the stemmed form from the start with a "(stemmed)" tag, revealed as "why" in chapter 3, rather than showing the wrong string first.

**§2 — "origin" posting list purity.** The evidence itself notes the term "origin" also collects `originated` and `original` via stemming — meaning some of the 5,482 postings are not really about "origin" (e.g. "original data"). Worth one clause acknowledging over-stemming as the flip side of the "coronaviru" under-stemming example already given.

**§7 — "judges: medical students and National Library of Medicine indexers."** This specific composition claim isn't backed by a citation in the evidence table (which only cites Voorhees et al. generally for "judges with medical expertise"). Recommend double-checking the exact wording against the TREC-COVID overview paper before shipping.

**Rounding inconsistencies:**
- §1/§2: narration says "about two milliseconds," on-screen shows "1.8 ms," but the measured median is 1.85 ms (which rounds to 1.9, not 1.8). Trivial, but pick one rounding convention.
- §6: narration says "about thirty-five papers a second," on-screen shows "≈ 36 papers / s," both from the same 35.7 papers/s figure. Harmless but worth aligning.

**§2 — "That's how the index answers in two milliseconds."** Attributes the full 1.8 ms solely to reading ~40k postings, eliding scoring/ranking cost (BM25 computation, top-k heap). Fine as a simplification for the target audience, but a one-clause acknowledgment ("plus scoring them") would be more precise.

---

Everything else checked out: all arithmetic (idf values, BM25 worked example, DCG/NDCG computation, RRF worked example, the results table, the billion-paper extrapolation) is correct to the precision shown; terminology (posting list, bi-encoder/cross-encoder, HNSW, pooling, qrels, P@k/R@k, MRR, NDCG) is standard and consistently used; the BM25 formula and its Lucene-specific footnote are accurate and well-caveated; the vocabulary-mismatch and exact-match (D614G) failure-mode examples are well-chosen and correctly quantified; and the offline/online evaluation framing (Joachims 2005, Turpin & Hersh 2001) is accurately cited.

VERDICT: REVISE
