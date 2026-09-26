# Declarative Queries & Query Planning — Canonical Treatment

## 1. Canonical worked example

There are two standard examples, from two different traditions:

- **Academic/theoretical canonical example**: the multi-way **join-order problem**, as introduced in **Selinger et al., "Access Path Selection in a Relational Database Management System," SIGMOD 1979** (the System R paper). It uses a 3–4 relation join and shows cost formulas, access path choice (index vs. scan), and dynamic-programming join enumeration with "interesting orders." This is *the* paper every database course traces back to (CMU 15-445/645, Berkeley CS186, Stanford CS245 all cite it directly), and it's the most-cited paper in query optimization.
- **Practitioner/engineering canonical example**: a single-table `WHERE` clause query shown with `EXPLAIN` / `EXPLAIN ANALYZE`, comparing a **sequential scan vs. an index scan** as selectivity changes. This is the standard example in **Markus Winand's "Use the Index, Luke"** (also his book *SQL Performance Explained*, 2012) and in the PostgreSQL documentation's own optimizer chapter.

For a short, industry-audience lesson, the **EXPLAIN-based scan-vs-index example is more common and more teachable**; the join-order example is the deeper academic canon but is heavier machinery than a short video needs.

## 2. Standard progression

The order used almost universally (Ramakrishnan & Gehrke; Garcia-Molina/Ullman/Widom; Silberschatz et al.; CMU 15-445):

1. Declarative (SQL) vs. procedural — contrast with relational algebra as the "how."
2. **Pipeline**: parse → translate to logical plan (relational algebra) → **optimize** (rewrite + choose physical operators) → execute.
3. Simple case first: **one table, one predicate** — sequential scan vs. index scan, introduce *cost* and *selectivity*.
4. Extend to **joins**: nested-loop, sort-merge, hash join, then the join-*ordering* problem.
5. Statistics/cardinality estimation as the input the cost model depends on.
6. Show that the optimizer's choice can be *wrong* when statistics are stale or assumptions (independence, uniformity) fail — this is the standard bridge to "why the same query can be fast or slow."

Ramakrishnan & Gehrke, *Database Management Systems* (3rd ed.), Ch. 12–15, follows exactly this arc and is the most commonly assigned textbook sequence for it.

## 3. Models & terminology

| Term | Canonical definition | Source |
|---|---|---|
| **Relational algebra** | Procedural formalism (select σ, project π, join ⋈, etc.) that is the *target* of SQL translation | Codd, "A Relational Model of Data for Large Shared Data Banks," CACM 1970 |
| **Relational calculus** | Declarative formalism SQL is closer to in spirit | Codd 1970; relational completeness proven equivalent to algebra in Codd, "Relational Completeness of Data Sublanguages," 1972 |
| **Logical plan** | Algebra tree, no physical detail | Garcia-Molina/Ullman/Widom Ch. 16 |
| **Physical plan / access path** | Concrete operators + algorithms (e.g., "hash join," "index scan") | Selinger 1979 coined "access path selection" |
| **Cost-based optimizer (CBO)** vs. **rule-based optimizer (RBO)** | CBO estimates I/O + CPU cost from statistics; RBO uses fixed heuristics regardless of data. Oracle is the canonical source of this terminology (RBO deprecated after Oracle 10g) | Oracle docs; also in Silberschatz Ch. 16 |
| **Interesting orders** | Sort orders worth preserving mid-plan because a later operator (merge join, ORDER BY, GROUP BY) needs them | Selinger 1979 |
| **Selectivity / cardinality estimation** | Fraction of rows a predicate is expected to match; used to price plans | Silberschatz Ch. 16, Ramakrishnan & Gehrke Ch. 15 |
| **Statistics: histograms, MCV (most-common-values), NDV** | Per-column data distribution summaries the optimizer consults | PostgreSQL/MySQL/Oracle docs all use this vocabulary near-identically |

Terminology varies by vendor: Postgres calls it "the planner"; Oracle/SQL Server/MySQL call it "the optimizer." SQL Server distinguishes **estimated** vs. **actual** execution plans explicitly in tooling; Postgres expresses the same distinction as `EXPLAIN` vs. `EXPLAIN ANALYZE`.

## 4. Key results / guarantees, and their limits

- **Relational completeness** (Codd 1972): SQL/relational algebra can express any query expressible in relational calculus, and vice versa — the formal justification for "declarative = as powerful as procedural, within this model." **Stops holding** for recursive queries (transitive closure) — plain relational algebra is *not* Turing/fixpoint-complete, which is why `WITH RECURSIVE` had to be added as an extension (Garcia-Molina/Ullman/Widom Ch. 7 discusses this limitation explicitly).
- **Semantic equivalence guarantee**: the optimizer only promises the chosen plan returns the *same result set* as any other valid plan — it makes **no optimality guarantee** on performance. It picks the cheapest plan *it can estimate and search*, not the true cheapest plan.
- **Join-order optimization is NP-hard** in the number of relations (Ibaraki & Kameda, "On the Optimal Nesting Order for Computing N-relational Joins," ACM TODS 1984), which is why System R's dynamic programming (exact, but exponential) is replaced by heuristics/genetic search beyond a threshold in real systems (e.g., Postgres switches to its Genetic Query Optimizer, GEQO, above `geqo_threshold`, default 12 tables).
- **Cost-model assumptions**: independence of predicates/columns and uniform distribution within histogram buckets. These are known-false in practice for correlated columns — this is the standard, textbook-cited explanation for optimizer misestimation (Silberschatz Ch. 16; Ramakrishnan & Gehrke Ch. 15).

## 5. Standard concrete examples in canonical sources

- Selinger 1979: cost formulas for a join of `EMPLOYEE`/`DEPARTMENT`-style tables comparing index-nested-loop vs. sort-merge.
- PostgreSQL docs / Winand: `SELECT * FROM t WHERE col = ?` shown with `EXPLAIN ANALYZE`, demonstrating the scan flips from index to sequential as the predicate matches a larger fraction of rows (commonly quoted informally as "around a few percent of the table," though the exact crossover is cost-model- and hardware-dependent, not a fixed constant — this specific number is often overstated, see §9).
- CMU 15-445 (Andy Pavlo) lecture slides use a TPC-H-style schema (`orders`, `lineitem`, `customer`) for join-order and physical-operator examples — TPC-H is the de facto standard benchmark schema referenced across systems courses and papers.

## 6. Misconceptions and how the canonical treatment corrects them

- *"SQL executes in the order it's written (SELECT, FROM, WHERE...)"* — corrected by teaching the **logical processing order** (FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY) is separate from both textual order and actual execution order, which the optimizer freely rearranges (Ben-Gan's T-SQL books are the widely cited source for the "logical query processing order" teaching device, used alongside standard textbooks).
- *"Adding an index always speeds up a query"* — corrected via cost-based reasoning: for low selectivity/small tables, random I/O of an index scan can cost more than a sequential scan (Winand's central thesis).
- *"The optimizer finds the best plan"* — corrected by stating it's a **heuristic search over an estimated cost space**, bounded by statistics quality and search-space pruning (Silberschatz Ch. 16 states this directly).
- *"The same query always gets the same plan"* — corrected by **parameter sniffing**: a cached plan compiled for one parameter value/data skew is reused for very different value distributions (canonical, widely cited source: Erland Sommarskog, "Slow in the Application, Fast in SSMS" — the standard SQL Server community reference; Oracle's answer to the same phenomenon is *bind variable peeking* / *adaptive cursor sharing*, documented in Oracle's optimizer guides).

## 7. Essential / extra / cut, for a short lesson

- **Essential**: declarative-vs-procedural distinction; the parse→optimize→execute pipeline; the concept of a *plan space* with cost estimates; seq-scan-vs-index-scan as the minimal concrete illustration; statistics as the input that can go stale; `EXPLAIN` as the tool that makes this visible.
- **Common extra** (nice, but expendable in a short format): full dynamic-programming join enumeration; detailed cost formulas; sort-merge vs. hash join internals; histograms in depth.
- **Leave out**: GEQO/genetic optimizers, Volcano/Cascades framework internals, distributed/parallel query planning, materialized-view rewriting, recursive-query optimization — all real but second-course material.

## 8. Real systems and their mechanisms

| System | Mechanism | Canonical reference |
|---|---|---|
| PostgreSQL | Cost-based, dynamic programming ≤ `geqo_threshold` (default 12) then GEQO (genetic algorithm); statistics from `ANALYZE` | PostgreSQL docs, "Planner Statistics" & "How the Planner Uses Statistics" |
| MySQL/InnoDB | Cost-based optimizer (rewritten 5.7+ with pluggable cost model); histograms since 8.0 | MySQL Reference Manual, "The Cost Model" |
| Oracle | CBO (RBO deprecated); bind-variable peeking, adaptive cursor sharing for parameter sensitivity | Oracle Database Performance Tuning Guide |
| SQL Server | Cost-based, **Cascades**-style transformation-rule optimizer framework | Goetz Graefe, "The Cascades Framework for Query Optimization," IEEE Data Eng. Bulletin 1995 |
| SQLite | Simpler cost-based optimizer | SQLite docs, "Query Planning" / `EXPLAIN QUERY PLAN` |
| Apache Calcite (used by Flink, Hive, Druid, etc.) | Volcano/Cascades-style extensible planner (`VolcanoPlanner`) | Goetz Graefe, "Volcano — An Extensible and Parallel Query Evaluation System," IEEE TKDE 1994 |

Volcano/Cascades (Graefe) is the standard citation for *why* modern optimizer architectures look the way they do — rule-based logical rewrites plus cost-based physical-plan search, generalizing System R's original design.

## 9. Commonly overstated or subtly wrong claims

- **"SQL is purely declarative"** — overstated; SQL has procedural elements (cursors, stored procedures, guaranteed side-effect ordering in some constructs) and `ORDER BY`/window functions impose sequence semantics.
- **"The optimizer picks the fastest plan"** — wrong; it picks the **cheapest by its estimate**, which can be badly wrong under correlated data or stale stats.
- **"There's a fixed % selectivity threshold where index beats scan"** (e.g., "10%") — overstated as a rule; it's a cost-model output, not a constant, and depends on row/page size, hardware, and cache state (Winand explicitly warns against treating any fixed percentage as universal).
- **"Join order never matters, the optimizer handles it"** — true only under the exhaustive-search regime (small numbers of joins); for large joins, systems fall back to heuristics/GEQO, where join order written by the developer can genuinely change performance.
- **Uncertain / not fully verifiable**: I could not confirm a single universally-quoted numeric selectivity crossover point cited *by name* in a canonical textbook — treat any specific percentage as illustrative, not canon.

## 10. Best learning modality per part

- **Narrated animation** — the parse→optimize→execute pipeline, and the idea of a *search over a tree/space of candidate plans* with cost annotations. This is inherently about structure and flow, which animates well and is hard to convey in text (matches how CMU 15-445 and Berkeley CS186 lecture slides visualize it).
- **Doing / interactive** — running `EXPLAIN ANALYZE` on a real table while varying a `WHERE` predicate's selectivity or adding/dropping an index, and watching the plan flip. This is the single most-recommended hands-on exercise across practitioner sources (Winand's site is built around exactly this loop) because cost intuition doesn't stick from description alone.
- **Reading** — the formal definitions (relational algebra operators, Codd's completeness result) and the Selinger 1979 paper itself for anyone going deeper; these are precise, citation-heavy, and better absorbed as text/reference than as narration.
