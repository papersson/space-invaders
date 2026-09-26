# Declarative queries and the query planner: the canonical treatment

Scope. This covers two "models": (a) **declarative** (non-procedural, set-at-a-time) data access versus **imperative/navigational** (record-at-a-time) access, and (b) the **cost-based planner** model: SQL text → logical plan → a space of equivalent physical plans → cost estimates from statistics → run the cheapest *estimated* plan. Sources are cited inline, and a link list is at the end. Items marked **(uncertain)** are ones I could not verify against the primary text.

---

## 1. Canonical worked examples, and why

Each part of the lesson has its own standard example.

**A. Declarative vs imperative: a loop versus a `SELECT` over one collection.**
- Kleppmann, *Designing Data-Intensive Applications* (DDIA), 1st ed. 2017, ch. 2 "Data Models and Query Languages", section "Query Languages for Data". It contrasts a JavaScript `getSharks()` loop with `SELECT * FROM animals WHERE family = 'Sharks';` and with σ_family="Sharks"(animals). This is the version most cited in modern practitioner material. In the 2nd edition (Kleppmann & Riccomini) the chapter becomes ch. 3. Whether the sharks example survives unchanged is **(uncertain)**.
- The historical form of the same contrast is CODASYL/IMS navigation versus relational queries.
  - Codd 1970, *CACM* 13(6), §1.2 names three dependencies: "ordering dependence, indexing dependence, and access path dependence". His example stores parts and projects in five alternative hierarchies.
  - Bachman's 1973 Turing lecture, "The Programmer as Navigator".
  - Stonebraker & Hellerstein, "What Goes Around Comes Around" (2005), which uses a Supplier/Part/Supply schema.

**B. The textbook planner example: a 2–3-table join with one selective filter.** The same shape appears in every canonical source:
- **Selinger et al. 1979** (System R, SIGMOD), Fig. 1: `EMP, DEPT, JOB`, "employees who are clerks and work for departments in Denver".
- **Ramakrishnan & Gehrke** (R&G), *Database Management Systems* 3e, ch. 12 "Overview of Query Evaluation", "Motivating Example". It uses Sailors/Reserves with `R.bid=100 AND S.rating>5`, and is reused in ch. 15 and in Berkeley CS186.
- **Silberschatz, Korth & Sudarshan** 7e, ch. 16 §16.2: "names of all instructors in the Music department, along with the titles of the courses that they teach".
- Garcia-Molina, Ullman & Widom (GMUW), *Database Systems: The Complete Book* 2e, ch. 16 "The Query Compiler": StarsIn/MovieStar, "movies with stars born in 1960" (exact wording **(uncertain)**).
- Elmasri & Navathe 7e, ch. 18–19, COMPANY schema (the specific example is from memory, **(uncertain)**).

Why this example is the standard:
1. It is the smallest query that forces all three planner decisions: **scan method, join method, join order**. That is the framing of Momjian's talk, slide 6.
2. Read literally, as product → filter → project, the SQL gives a correct but catastrophic plan. That makes the value of optimization visible:
   - R&G's naive plan costs "500+500*1000 I/Os … By no means the worst plan!"
   - Silberschatz's ch. 16 slides: plan costs differ by "seconds vs. days".
3. It fits on one slide as an operator tree.
4. It is Selinger's own example.

**C. The practitioner example of "same query, fast or slow": one indexed table, swept across selectivities.**
- PostgreSQL docs §14.1 "Using EXPLAIN" (regression table `tenk1`): `unique1 < 7000` gives a Seq Scan, `< 100` a Bitmap scan, `= 42` an Index Scan.
- Bruce Momjian, "Explaining the Postgres Query Optimizer" (long-running talk): a skewed first-letter table, where a common value gets a seq scan and a rare value gets an index(-only) scan.
- Winand, *Use The Index, Luke* (also published as *SQL Performance Explained*), ch. 2 "Bind Parameters": `subsidiary_id` 20 returns 99 rows and gets an index, while 30 returns 1000 rows and gets a full scan.
- SQLite doc "Query Planning" (FruitsForSale table).

**Competing examples, and which is more common.**
- By query shape, (B) "join + selective predicate" dominates textbooks and university courses, and (C) the "selectivity sweep" dominates vendor docs and talks. In teaching specifically about the planner, (B) is the more common one.
- By schema, the **employee/department** family and the **suppliers/parts** family compete:
  - Employee/department: Selinger's EMP/DEPT, Oracle's classic SCOTT EMP/DEPT schema, Winand's EMPLOYEES, Elmasri & Navathe's COMPANY.
  - Suppliers/parts: Codd 1970's `supply (supplier part project quantity)`, C. J. Date's S/P/SP, and Stonebraker & Hellerstein.
  - In optimizer material, employee/department is the more common of the two. Several course books use their own schemas instead: Sailors (R&G), University (Silberschatz), Movies (GMUW).
  - This is my assessment from the sources, not a count.

---

## 2. Standard progression

**Textbooks and courses** all follow the same arc: model → language → storage/index → operators → optimizer.
1. Relational model and algebra, then SQL.
   - Silberschatz 7e ch. 2–3; R&G ch. 4–5.
   - CMU 15-445 (Pavlo, Fall 2024) lectures 01 "Relational Model & Algebra" and 02 "Modern SQL".
   - Berkeley CS186 starts with SQL I/II.
2. Storage and B+-tree indexes. Silberschatz ch. 13–14; CMU L03–L09; CS186 "Disks, Buffers, Files", "Cost Models and Index", "B+ Trees".
3. Query processing. Silberschatz ch. 15 is the model order:
   - §15.1 Overview: parse/translate → optimize → evaluate.
   - §15.2 Measures of Query Cost.
   - §15.3 Selection.
   - §15.4 Sorting.
   - §15.5 Join, in the order simple nested-loop → block nested-loop → indexed nested-loop → merge → hash.
   - §15.7 Evaluation of Expressions (materialization vs pipelining).
   - Also: R&G ch. 12–14; CMU L11 Sorting, L12 Joins, L13–14 Query Execution; CS186 "Sorting and Hashing", "Joins", "Iterators and Relational Algebra". The iterator ("pull") model comes from Graefe's *Volcano* (IEEE TKDE 1994).
4. Query optimization.
   - Silberschatz ch. 16: §16.2 Transformation of Relational Expressions (equivalence rules), §16.3 Estimating Statistics of Expression Results, §16.4 Choice of Evaluation Plans (dynamic programming, left-deep trees, interesting orders, heuristics).
   - Also: R&G ch. 15 "A Typical Relational Query Optimizer" (System R); GMUW ch. 16 (§16.2 "Algebraic Laws for Improving Query Plans", §16.6 "Choosing an Order for Joins"); CMU L15 "Query Planning & Optimization"; CS186 "QO: Plan Space" then "QO: Costs and Search".
5. Advanced topics: nested-subquery decorrelation, materialized views, adaptive/parametric optimization, parallel/distributed plans. Silberschatz §16.5–16.6 and ch. 22.

**Simpler version shown before the full one:**
- Single-table access-path choice comes before joins (Selinger §4 before §5; SQLite "Query Planning").
- A two-way join comes before n-way join ordering (Selinger §5).
- The logical plan (algebra tree) comes before the physical plan (CMU L15 notes §1).
- Heuristic rewrites ("perform selection early") come before cost-based search. Silberschatz slides place heuristics as a cheaper alternative; CMU L15 §3 comes before §4.
- Bottom-up left-deep DP (System R) comes before top-down transformation search (Volcano/Cascades). See Chaudhuri 1998 §3 → §6; CMU L15 §10 → §11.
- Estimates first assume uniformity and independence (Selinger Table 1). Then come histograms and sampling (CMU L15 §6–7), then multi-column/extended statistics (PostgreSQL §14.2.2).
- `EXPLAIN` comes before `EXPLAIN ANALYZE` (PostgreSQL §14.1).

**Practitioner and talk progressions:**
- **Kleppmann DDIA ch. 2:** imperative vs declarative (sharks), then CODASYL "access paths", then the relational query optimizer as an *automatic* access-path chooser ("only need to build a query optimizer once").
- **Momjian's talk**, in slide order:
  1. Which scan method? Distribution matters, and `ANALYZE` flips the plan.
  2. Which join method? A tight restriction gives a nested loop, a looser one a hash join, none a merge join.
  3. "Order of Joined Relations Is Insignificant".
  4. Statistics, then indexes.
  5. `LIMIT` switches join methods.
  6. "Same Join, Different Plans".
- **Winand**, in chapter order:
  1. "Anatomy of an Index" (tree traversal, leaf-node chain, table access).
  2. "The Where Clause" (equality, concatenated keys, "Slow Indexes, Part II", functions, bind parameters, ranges).
  3. Performance and scalability.
  4. Joins.
  5. Sorting and grouping.
  6. Execution plans.
- **PostgreSQL docs:**
  - ch. 14 "Performance Tips": §14.1 Using EXPLAIN → §14.2 Statistics Used by the Planner → §14.3 Controlling the Planner with Explicit JOIN Clauses.
  - Internals ch. 51 "Overview of PostgreSQL Internals": §51.1 "The Path of a Query" → §51.5 Planner/Optimizer.

---

## 3. Models and terminology

**Declarative (non-procedural).**
- You state the conditions the result must meet, not the steps to compute it.
  - Selinger 1979 abstract: in SQL "requests are stated non-procedurally, without reference to access paths".
  - Kleppmann: you specify "the pattern of the data you want … but not how to achieve that goal". The optimizer decides "which indexes and which join methods to use, and in which order".
  - CMU L15: "the query only tells the DBMS what to compute, but not how".
- **What it guarantees:** the answer is defined by the query's semantics alone, so every correct plan returns the same result.
- **What it does not guarantee:**
  - Speed.
  - Row order without `ORDER BY`. PostgreSQL §7.5: order "will depend on the scan and join plan types … but it must not be relied on".
  - Evaluation order of subexpressions. PostgreSQL §4.2.14: "not defined … not the same as the left-to-right 'short-circuiting' … found in some programming languages".

**Imperative / procedural / navigational / record-at-a-time.**
- The program fixes the traversal and the access paths: CODASYL `FIND … NEXT … WITHIN set`, IMS DL/I `GET NEXT`, or a host-language loop.
- Execution follows the program. Performance and correctness are the programmer's job, and programs break when the physical structure changes: Codd's "access path dependence".
- Stonebraker & Hellerstein 2005:
  - Lesson 4: "A record-at-a-time user interface forces the programmer to do manual query optimization, and this is often hard."
  - Lesson 7: "Set-a-time languages are good … since they offer much improved physical data independence."

**Data independence** (Codd 1970 abstract): "Future users of large data banks must be protected from having to know how the data is organized in the machine (the internal representation)." The physical/logical split is the ANSI/SPARC tradition.

**Relational algebra vs relational calculus.**
- Silberschatz 7e ch. 2 slides: "Procedural versus non-procedural, or declarative". The "pure" languages (algebra, tuple calculus, domain calculus) "are equivalent in computing power" (Codd 1972, "Relational Completeness of Data Base Sublanguages").
- Terminology differs by source. Older texts call the algebra "procedural"; some newer ones call it "functional" (Silberschatz 7e text, **(uncertain)**).
- SQL (SEQUEL: Chamberlin & Boyce 1974) is calculus-flavoured: SEQUEL was said to have power "equivalent to the first order predicate calculus" without bound variables or quantifiers.

**Plan vocabulary:**
- *Query plan*, *execution plan*, *access plan* (DB2) and *physical operator tree* are synonyms. Chaudhuri 1998 uses "physical operator tree and execution plan … interchangeably".
- *Logical plan* (algebra) vs *physical plan* (algorithms plus access paths): CMU L15.
- *Planner* (PostgreSQL), *optimizer* (most systems) and *query compiler* (GMUW ch. 16) name the same component.
- *Access path* (System R, Oracle) is what PostgreSQL calls a scan type: Seq Scan, Index Scan, Index Only Scan, Bitmap Heap/Index Scan.

**Estimates:**
- The fraction of rows a predicate keeps has three names: *selectivity factor F* (Selinger), *reduction factor* (R&G) and *selectivity* (PostgreSQL, CMU). *Cardinality* is the estimated row count (`rows=` in PostgreSQL EXPLAIN).
- Watch the wording. "Highly selective" means *few* rows pass, but "high selectivity" is used both ways in the wild.

**Sargable:**
- The term comes from System R's "search arguments (SARGS)", i.e. predicates the storage layer can apply.
- The practitioner form is Winand's *access vs filter predicates*. PostgreSQL shows these as `Index Cond` vs `Filter`, and SQL Server as `Seek Predicates` vs `Predicate` (**(uncertain)** on the exact SQL Server labels).

**Cost:**
- Cost is in **arbitrary units**. PostgreSQL §14.1 uses units of page fetches, with `seq_page_cost = 1.0`.
- System R: `COST = PAGE FETCHES + W * (RSI CALLS)`.

**Optimizer styles:**
- *Rule-based vs cost-based* (Oracle's RBO/CBO); *heuristic vs cost-based* (textbooks).
- *Bottom-up/generative* (System R, DB2, MySQL, PostgreSQL) vs *top-down/transformational* (Volcano/Cascades: SQL Server, Greenplum, CockroachDB). That grouping is from CMU L15 §9.

**Plan reuse has a different name in each system:**
- PostgreSQL: *custom vs generic plans* (`plan_cache_mode`).
- SQL Server: *parameter sniffing* / *parameter sensitivity*.
- Oracle: *bind peeking*, then *adaptive cursor sharing*.
- MongoDB: *plan cache query shape*.

**Planner control:**
- Oracle, MySQL and SQL Server have *hints*.
- Core PostgreSQL deliberately has none; its `enable_*` settings are described as "a crude method" (§19.7).
- SQLite offers `likelihood()`, unary `+`, `CROSS JOIN` (forces loop order) and `INDEXED BY`.

---

## 4. Key results and guarantees: assumptions, and where they stop holding

1. **Data independence** (Codd 1970).
   - Queries stay *correct* as indexes and storage change. Codd asks whether programs can "remain invariant as indices come and go".
   - It stops at performance: dropping an index can leave results unchanged but make the query orders of magnitude slower.
2. **Algebra ≡ calculus** (Codd 1972).
   - Declarative queries can be translated into algebra trees, and those trees are what the planner rewrites.
   - The assumption is set semantics without NULLs or aggregates. SQL uses bags (Silberschatz ch. 16 slides: "In SQL, inputs and outputs are multisets of tuples"), NULLs with three-valued logic, and aggregates, so each equivalence must be re-checked.
3. **Equivalence rules.**
   - Inner joins are commutative and associative, and selections and projections can be pushed down (Silberschatz §16.2; GMUW §16.2). This is what creates the search space.
   - Some rules fail for **outer joins**. Silberschatz's slides give σ_year=2017(instructor ⟕ teaches) ≢ σ_year=2017(instructor ⋈ teaches), and "Outerjoins are not associative".
   - Rules must also respect volatile functions, where evaluation order becomes observable.
4. **Selinger dynamic programming.**
   - Key observation (Selinger §5): once the first k relations are joined, the way to join the (k+1)-st "is independent of the order of joining the first k". So the best plan per *subset* can be kept, plus one per "interesting order" (ORDER BY/GROUP BY/join columns).
   - Heuristic: Cartesian products "as late in the join sequence as possible".
   - The result is optimal *within the search space and under the cost model*.
   - Size of the space (Silberschatz ch. 16 slides): (2(n−1))!/(n−1)! join orders, which is more than 176 billion at n=10.
   - DP cost: O(3ⁿ) for bushy trees, about 59,000 at n=10, and O(n·2ⁿ) for left-deep trees.
   - It stops at large n. The general problem is NP-hard (Ibaraki & Kameda, *TODS* 1984).
     - PostgreSQL switches to its Genetic Query Optimizer at `geqo_threshold` = 12 FROM items.
     - MySQL's docs warn that "queries with 12, 13, or more tables may easily require hours and even days to compile" with full search depth.
   - Faster exact DP: DPccp/DPhyp (Moerkotte & Neumann, VLDB 2006 / SIGMOD 2008).
5. **Relative, not absolute, accuracy.**
   - Selinger's conclusion: "although the costs predicted by the optimizer are often not accurate in absolute value, the true optimal path is selected in a large majority of cases."
   - This stops holding when estimation errors are large (points 6–8).
6. **Estimation assumptions: uniformity, independence, inclusion.**
   - Named in Leis et al. 2015 §2.3 and CMU L15 §5.
   - Selinger's Table 1 is explicit. Equality uses F = 1/ICARD, which "assumes an even distribution". AND uses F1·F2, where "this assumes that column values are independent". With no statistics the defaults are 1/10 (=), 1/3 (open range) and 1/4 (BETWEEN).
   - These fail on skew, on correlated columns (city/zip in the PostgreSQL §14.2.2 example; `model='accord' AND make='honda'` in Leis 2025) and on correlations that cross joins.
   - **Errors grow exponentially with the number of joins** (Ioannidis & Christodoulakis, SIGMOD 1991).
   - Leis et al. (PVLDB 2015, Join Order Benchmark on IMDB, 113 queries): "all estimators routinely produce large errors". Their 2025 retrospective adds that in PostgreSQL 9.4 "roughly 10% of the JOB queries failed to complete in any reasonable time frame due to cardinality estimation errors".
7. **Cardinality matters more than the cost model.**
   - Lohman (SIGMOD blog 2014): cardinality estimation is "the Achilles Heel". The cost model "may introduce errors of at most 30%", while cardinality errors reach "many orders of magnitude".
   - Leis 2015: the cost model "has much less influence on query performance than the cardinality estimates".
8. **Risk is asymmetric, and more access paths mean more chances to be wrong** (Leis 2015 §4).
   - Picking a non-indexed nested-loop join on an underestimated input is "extremely risky" for "a very small payoff". Disabling such joins removed timeouts and slowed down no query.
   - After foreign-key indexes were added, "40% of the queries [were] slower by a factor of 2" relative to plans made with true cardinalities: "the more indexes are available the harder the job of the query optimizer becomes".
9. **Plan choice is non-linear in the parameters** (Reddy & Haritsa, VLDB 2005, "plan diagrams"). Commercial optimizers:
   - make "extremely fine-grained plan choices";
   - have plan regions with "irregular boundaries";
   - show "non-monotonic cost behavior".
   This is the formal version of "change the constant and the plan flips".
10. **Statistics are samples.** PostgreSQL `ANALYZE` docs: statistics "will change slightly each time ANALYZE is run … In rare situations, this non-determinism will cause the planner's choices of query plans to change."
11. **Plan caching trades plan quality for planning cost.**
    - PostgreSQL `PREPARE`: "the first five executions are done with custom plans". After that a generic plan is used if its estimated cost is not much worse.
    - SQL Server (Parameter Sensitive Plan optimization, 2022, compatibility level 160) addresses the case where "a single cached plan for a parameterized query isn't optimal for all possible incoming parameter values … with non-uniform data distributions". It supports equality predicates only and uses low/medium/high cardinality buckets.
    - Winand ("Bind Parameters"): without values, the optimizer "just assumes an equal distribution".

---

## 5. Standard concrete examples as they appear in the sources

**Kleppmann, DDIA 1e ch. 2 (sharks):**
```js
function getSharks() {
  var sharks = [];
  for (var i = 0; i < animals.length; i++) {
    if (animals[i].family === "Sharks") sharks.push(animals[i]);
  }
  return sharks;
}
```
```sql
SELECT * FROM animals WHERE family = 'Sharks';
```
The book's points:
- The declarative version is more concise.
- The engine can change its algorithms (for example, add indexes) without changing queries.
- The declarative version promises no ordering.
- It "lend[s] itself to parallel execution".

**Selinger 1979, Fig. 1:**
```sql
SELECT NAME, TITLE, SAL, DNAME
FROM EMP, DEPT, JOB
WHERE TITLE='CLERK' AND LOC='DENVER'
  AND EMP.DNO=DEPT.DNO AND EMP.JOB=JOB.JOB
```
The paper then builds the search tree:
- Figs. 2–3: the best access path for each single relation, per interesting order (DNO, JOB).
- Figs. 4–6: extensions to pairs of relations and then all three, using nested loops or merging scans.

**R&G 3e ch. 12 "Motivating Example"** (Reserves: 1000 pages; Sailors: 500 pages):
```sql
SELECT S.sname FROM Reserves R, Sailors S
WHERE R.sid=S.sid AND R.bid=100 AND S.rating>5
```
The costs fall as the plan improves:

| Plan | Cost (page I/Os) |
|---|---|
| Naive simple nested loops | 500 + 500·1000 = 500,500 |
| Push selections, sort-merge join | 3,560 |
| Push selections, block nested-loop join | 2,770 |
| Also push projections | < 2,000 |
| Clustered index on `bid`, then index nested loops using the hash index on `Sailors.sid`, pipelined | 1,210 |

The same deck gives the "index is not always better" example: 10% of Reserves via an unclustered index costs "upto 10000 I/Os", versus a 1000-page scan.

**Silberschatz 7e §16.2 (pushing selections):**
Π_name,title(σ_dept_name='Music'(instructor ⋈ (teaches ⋈ Π_course_id,title(course)))) becomes
Π_name,title((σ_dept_name='Music'(instructor)) ⋈ (teaches ⋈ Π_course_id,title(course))).
The book's gloss: "Performing the selection as early as possible reduces the size of the relation to be joined."

**PostgreSQL §14.1 (selectivity sweep on `tenk1`, 10,000 rows, 345 pages):**
- A full scan costs 345·1.0 + 10000·0.01 = 445.
- `WHERE unique1 < 7000` → `Seq Scan … (cost=0.00..470.00 rows=7000)`.
- `WHERE unique1 < 100` → `Bitmap Heap Scan … (cost=5.06..224.98 rows=100)` over a `Bitmap Index Scan on tenk1_unique1`.
- `WHERE unique1 = 42` → `Index Scan using tenk1_unique1 … (cost=0.29..8.30 rows=1)`.
- Caveat in the same section: "Results on small tables cannot be assumed to apply to large tables."

**Momjian's talk (skew and `ANALYZE`):**
- The table holds the first letter of `pg_class.relname`, with 'p' = 83.4% of rows.
- Before `ANALYZE`, every letter gets the same bitmap plan with `rows=2`.
- After `ANALYZE`:
  - 'p' gets a Seq Scan;
  - 'd' gets a Bitmap Heap Scan;
  - 'i' gets an Index Only Scan.
- Later slides:
  - "LIMIT 100 Switches to Merge Join"; "LIMIT 1000 Switches Back to Hash Join".
  - "Same Join, Different Plans".

**Winand, *Use The Index, Luke*:**
```sql
-- index on last_name is not used: the function is a black box
SELECT first_name, last_name, phone_number FROM employees
 WHERE UPPER(last_name) = UPPER('winand');
CREATE INDEX emp_up_name ON employees (UPPER(last_name));  -- function-based index fix
```
- Concatenated index for `date_of_birth BETWEEN ? AND ? AND subsidiary_id = ?`: use `(subsidiary_id, date_of_birth)`. The rule is "Index for equality first—then for ranges".
- "Slow Indexes, Part II": with wrong statistics (40 estimated rows vs 1000 actual), the optimizer picks an index range scan plus table access (cost 680) over a full scan (cost 477).

**PostgreSQL §14.2.2 (correlated columns):**
```sql
CREATE STATISTICS stts (dependencies) ON city, zip FROM zipcodes;
ANALYZE zipcodes;   -- zip => city 1.00, city => zip 0.42
```
This exists because "the planner assumes conditions are independent".

**PostgreSQL §4.2.14 (no evaluation order):**
```sql
SELECT ... WHERE x > 0 AND y/x > 1.5;                              -- untrustworthy
SELECT ... WHERE CASE WHEN x > 0 THEN y/x > 1.5 ELSE false END;    -- safe, but "will defeat optimization attempts"
```

**PostgreSQL §7.8 (`WITH` inlining; from v12):** a CTE referenced once is folded into the parent query. `MATERIALIZED` / `NOT MATERIALIZED` override this. The docs' example is `WITH w AS (SELECT * FROM big_table)` joined to itself.

**Rails Guides, "N + 1 Queries Problem"** (the imperative loop smuggled back in through an ORM):
- `Book.limit(10).each { |b| b.author.last_name }` runs 11 queries.
- `Book.includes(:author).limit(10)` runs 2.

**SQL Server Parameter Sensitive Plan docs:** `SELECT … FROM dbo.Property WHERE AgentId = @AgentId`. Some agents have few listings and some have very many, so one cached plan cannot suit both.

---

## 6. Misconceptions practitioners bring, and the canonical correction

- **"The database runs my SQL in the order I wrote it"** (or in the FROM→WHERE→…→SELECT order).
  - That is *logical* semantics only.
  - Julia Evans, "SQL queries don't start with SELECT" (2019): "Database engines don't actually literally run queries in this order."
  - The textbook correction is the logical vs physical plan distinction (CMU L15; Silberschatz §15.1).
- **"WHERE conditions short-circuit left to right"** or **"rows come back in primary-key/insert order".** Both are undefined (PostgreSQL §4.2.14, §7.5; Kleppmann's point that SQL promises no order).
- **"An index always makes it faster; if it's slow, add an index."**
  - An index lookup is tree traversal + leaf chain + table access (Winand ch. 1). A wide range plus many table fetches is slower than a scan.
  - See R&G's 10% unclustered example and PostgreSQL's `unique1 < 7000` Seq Scan.
  - Codd notes that indexes also "slow down response to insertions and deletions".
- **"The optimizer picks the best plan."**
  - It picks the cheapest *estimated* plan in a restricted space.
  - R&G ch. 12 slides: "Ideally: Want to find best plan. Practically: Avoid worst plans!"
  - PostgreSQL §51.5: the plan "expected to run the fastest".
- **"EXPLAIN tells me what happened; cost is milliseconds."**
  - `EXPLAIN` shows estimates in arbitrary units. `EXPLAIN ANALYZE` executes the query.
  - Compare estimated vs actual rows (PostgreSQL §14.1).
- **"Same SQL means same plan means same speed."**
  - Plans depend on parameter values (skew), statistics freshness and sampling, data growth crossing a cost crossover, and cached generic/sniffed plans.
  - See the PostgreSQL ANALYZE/PREPARE docs, SQL Server PSP, Momjian, and Winand's bind parameters.
- **"A slow index has degenerated; rebuild it."** Winand's myth directory ("Indexes Can Degenerate") and "Slow Indexes, Part I". The real causes are the leaf-chain walk and the table accesses.
- **"Most selective column first in a composite index."** Also a Winand myth. The canonical rule is equality columns first, then ranges.
- **"Wrapping a column in a function or cast is harmless."** It makes the predicate non-sargable (Winand ch. 2 "Functions", "Obfuscated Conditions").
- **"Joins are slow, so denormalize or loop in code."**
  - Hash, merge and index nested-loop joins are efficient. The documented failures come from *misestimated* inputs (Leis 2015).
  - Looping in application code is exactly the record-at-a-time style the relational model replaced (Stonebraker & Hellerstein, Lesson 10: optimizers "can beat all but the best record-at-a-time … programmers"). The ORM N+1 problem is its modern form.

---

## 7. For a short lesson: essential, common extras, leave out

**Essential:**
1. **What vs how.** One SQL query has many physical plans with identical results. Use the sharks loop vs `SELECT`, plus Codd's data independence.
2. **The pipeline:** parse → rewrite → *plan* (enumerate alternatives, estimate cost, pick the cheapest) → execute (Silberschatz §15.1; PostgreSQL §51.1).
3. **The three decisions:** scan method, join method, join order, shown on one small join with a selective filter (Selinger/R&G/Silberschatz shape).
4. **Estimates drive choices.** Row-count estimates come from statistics under the uniformity and independence assumptions. Cost is an estimate, not a measurement.
5. **Why the same query is fast or slow:**
   - a selectivity crossover (the `tenk1` sweep);
   - skewed parameter values plus plan caching;
   - stale or missing statistics;
   - correlated predicates.
6. **How to look:** `EXPLAIN` vs `EXPLAIN ANALYZE`; compare estimated vs actual rows.

**Common extras:**
- Selinger DP, interesting orders, and the left-deep restriction; the join-order count explosion (176 billion vs 59,000).
- Histograms, MCVs, and extended statistics.
- The three join algorithms in detail.
- Non-sargable predicates and composite-index column order.
- Vendor plan caching (generic plans, parameter sniffing, PSP).
- Adaptive execution (Oracle 12c adaptive plans, Spark AQE).
- Leis et al.'s headline findings; the Codd/Bachman "Great Debate" history.

**Leave out:**
- Cost formulas and I/O arithmetic.
- Volcano/Cascades memo internals.
- DPccp/DPhyp, NP-hardness proofs, and GEQO internals.
- Relational calculus and Codd's theorem proof.
- Outer-join reordering theory.
- Learned optimizers; worst-case-optimal and Yannakakis joins.
- Distributed/parallel optimization; buffer management.

---

## 8. Systems canonically cited, with their mechanism

| System / language | Model | Specific mechanism (source) |
|---|---|---|
| CODASYL/IDMS, IMS DL/I | Navigational, record-at-a-time | Programmer walks sets or hierarchies with `FIND/GET NEXT`. Access paths are hard-coded in programs (Codd 1970 §1.2; Stonebraker & Hellerstein 2005). |
| System R / SQL (SEQUEL) | Declarative + cost-based | Bottom-up DP over relation subsets; left-deep trees; Cartesian products deferred; interesting orders. Cost = page fetches + W·RSI calls. Selectivity factors from catalog statistics refreshed by `UPDATE STATISTICS` (Selinger 1979). |
| Ingres / QUEL | Declarative | Query *decomposition*: one-variable detachment plus tuple substitution, a greedy and adaptive alternative (Wong & Youssefi, *TODS* 1976). |
| IBM Starburst → DB2 | Declarative, extensible | Rule-based *query rewrite* on the Query Graph Model, then bottom-up cost-based plan optimization (Chaudhuri 1998 §6.1). The LEO learning optimizer used runtime feedback. |
| Volcano/Cascades (Graefe 1994/1995) → **SQL Server**, Greenplum Orca, **CockroachDB**, Apache Calcite | Declarative, top-down | Transformation + implementation rules; top-down memoized DP ("memo"); goal-driven search with physical properties (Chaudhuri 1998 §6.2; CMU L15 §11; CockroachDB blog "How we built a cost-based SQL optimizer"). |
| **PostgreSQL** | System R-style | Near-exhaustive DP below `geqo_threshold` (12); genetic search above it. `pg_statistic` holds MCVs, histograms, `n_distinct` and `correlation`, with `CREATE STATISTICS` for correlated columns. Cost constants `seq_page_cost` 1.0 / `random_page_cost` 4.0 / `cpu_tuple_cost` 0.01. `join_collapse_limit`/`from_collapse_limit` 8. Custom vs generic plans. No hints in core (§14, §19.7, §51.5). |
| **MySQL** | Bottom-up, greedy/exhaustive | `optimizer_search_depth` and `optimizer_prune_level` bound the search. Optimizer hints; histograms (8.0); hash join and `EXPLAIN ANALYZE` (8.0.18). |
| **Oracle** | RBO → CBO | Rule-based optimizer obsolete/unsupported from 10g. Bind peeking, then adaptive cursor sharing (11g). Adaptive plans (12c): a statistics collector switches nested loops ↔ hash join at runtime. Hints. |
| **SQL Server** | Cascades-style | Plan cache plus parameter sniffing; Query Store; PSP optimization (2022) dispatches up to 3 query variants by cardinality bucket. |
| **SQLite** | Heuristic | "Next Generation Query Planner" (3.8.0): an N-nearest-neighbours search over join orders. Optional Query Planner Stability Guarantee. `likelihood()`, unary `+`, `CROSS JOIN` forces loop order. |
| **MongoDB** | Declarative-ish documents | Multi-planner "plan racing": the winner is the plan that "produces the most results during the trial period while performing the least amount of work". The winner is cached per query shape. A cost-based ranker was added in 8.3. |
| **Spark SQL** | Declarative DataFrame/SQL | Catalyst rule- and cost-based optimizer (Armbrust et al., SIGMOD 2015). Adaptive Query Execution re-plans with runtime statistics (default since 3.2.0). |
| CSS selectors, Datalog, Cypher/SPARQL | Declarative (non-SQL) | Kleppmann DDIA ch. 2 uses CSS as the everyday analogy for declarative querying, and covers Datalog/Cypher/SPARQL as declarative graph queries. |

---

## 9. Claims that are commonly overstated or subtly wrong

- **"SQL is declarative, so how you write it doesn't matter."**
  - Mostly true for simple rewrites, but not in general:
    - non-sargable expressions;
    - CTEs, which were an optimization fence in PostgreSQL before v12;
    - `LIMIT` changing join methods (Momjian);
    - more than 8 explicit JOINs in PostgreSQL, which keep the written order (`join_collapse_limit`);
    - SQLite `CROSS JOIN`;
    - MySQL `STRAIGHT_JOIN` and hints.
  - "Order of joined relations is insignificant" holds for *inner* joins below those limits. For outer joins, order is semantics.
- **"The optimizer finds the optimal plan."** It is optimal only *relative to its estimates and search space*. Even DP's optimality guarantee is conditional: "if the cost model and cardinality estimates were correct" (Leis 2025).
- **"Join ordering is NP-hard, so optimizers use heuristics."** True in general (Ibaraki & Kameda 1984). Real systems nonetheless run exact DP for typical queries (up to about 10–12 relations) and switch to heuristics only above thresholds. Silberschatz: "typical queries have small n, generally < 10."
- **"Better cost models fix bad plans."** Cardinality errors dominate (Lohman 2014; Leis 2015).
- **"Optimizers always underestimate."** That is true on JOB. The 2025 retrospective reports the *opposite* trend (overestimation) on the SQLStorm benchmark.
- **Specific numbers from Leis 2015.** Its conference-version enumeration results "were incorrect due to a data-handling issue; they were corrected in the journal version" (Leis et al., *VLDB J.* 2018, per the 2025 retrospective). Cite the journal version for enumeration numbers.
- **"ML/learned optimizers have solved it."** Leis 2025: "in real-world systems learned methods have not replaced classical methods yet". CMU L15: "no major DBMS currently deploys" an ML-based optimizer.
- **"Cost = time."** Cost is in arbitrary units, and the defaults encode assumptions. PostgreSQL's `random_page_cost` 4.0 is low *because* most random reads "are assumed to be in cache" (§19.7.2).
- **"SQL is relational algebra / set theory."** SQL uses multisets, NULLs with three-valued logic, and ordering. Some algebraic identities need care (Silberschatz ch. 16 slides; Date, *SQL and Relational Theory*).
- **"Prepared statements / bind parameters are always faster."** They save parsing and planning but can lock in a plan that is wrong for skewed values (Winand "Bind Parameters"; PostgreSQL generic plans; SQL Server sniffing).
- **"Data independence means performance independence."** It means correctness independence only (Codd 1970).
- **"Selinger's design is what every database uses."** Its ideas (cost-based search, DP, interesting orders) are pervasive (Chaudhuri 1998). But SQL Server, CockroachDB and Orca are Cascades-style, SQLite is heuristic, and MongoDB uses plan racing.
- **"Rule-based optimization is obsolete."** Oracle's *RBO* is. But rule-based *rewrites* (predicate pushdown, subquery decorrelation) are a standard phase before cost-based search (Starburst; CMU L15 §3).

---

## 10. Best medium for each part

**Narrated animation** suits processes that unfold over time or space, where narration can hold attention on one decision at a time:
- SQL text → logical tree → several candidate physical trees with cost labels → the chosen one → the executor pulling rows up the tree (Volcano iterators).
- An index lookup, following Winand's three steps (descend the B-tree, walk the leaf chain, fetch scattered heap pages). This shows *why* 10% via an index can lose to a scan.
- Nested-loop vs hash vs merge join side by side, with work counters.
- The selectivity crossover: a flat seq-scan cost line and a rising index-scan line cross, and the chosen plan flips at the crossing. This is a 1-D plan diagram (Reddy & Haritsa 2005).
- An underestimate at a leaf multiplying up a join tree, until a nested loop is chosen where a hash join was needed (Ioannidis & Christodoulakis 1991; Leis 2015).

**Doing (running code, interactive simulation, exercises)** suits what is a procedural skill. The habit of comparing estimated vs actual rows, and the surprise of "my index wasn't used", stick best when self-discovered.
- On a real PostgreSQL or SQLite instance, repeat the `tenk1` sweep or Momjian's skewed-table recipe. Change the constant; run `ANALYZE`; add or drop an index; wrap the column in `UPPER()`; execute a prepared statement 6+ times to see the switch to a generic plan; create correlated columns, then fix the estimate with `CREATE STATISTICS`.
- A slider-driven simulation of selectivity vs plan cost.
- A "be the optimizer" exercise: order a 3-table join from given row counts, then reveal the true counts.
- Rewrite an ORM N+1 loop as one join and count the queries.

**Reading** suits exact wording, history and reference material that is looked up rather than practised:
- History and motivation: Codd 1970, the Codd–Bachman "Great Debate", System R.
- Precise guarantees and caveats, which need exact wording: unspecified row order; undefined evaluation order; bag semantics; outer-join non-equivalences.
- Engine-specific terminology and settings: plan-cache behaviour, hints, cost constants.
- Research results (Selinger's formulas, Leis's numbers), for learners who want depth.

---

## Sources (links)

**Papers**
- Codd 1970, "A Relational Model of Data for Large Shared Data Banks", *CACM* 13(6) — https://www.engineering.upenn.edu/~zives/03f/cis550/codd.pdf
- Selinger et al. 1979, "Access Path Selection in a Relational DBMS", SIGMOD — https://people.eecs.berkeley.edu/~brewer/cs262/3-selinger79.pdf
- Chamberlin & Boyce 1974, "SEQUEL" — https://dl.acm.org/doi/10.1145/800296.811515
- Chaudhuri 1998, "An Overview of Query Optimization in Relational Systems", PODS — https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/pods98-tutorial.pdf
- Stonebraker & Hellerstein 2005, "What Goes Around Comes Around" — https://people.cs.umass.edu/~yanlei/courses/CS691LL-f06/papers/SH05.pdf
- Leis et al. 2015, "How Good Are Query Optimizers, Really?", PVLDB 9(3) — https://www.vldb.org/pvldb/vol9/p204-leis.pdf
- Leis et al. 2025, "Still Asking: How Good Are Query Optimizers, Really?", PVLDB 18(12) — http://www.vldb.org/pvldb/vol18/p5531-viktor.pdf (quotes Lohman 2014, https://wp.sigmod.org/?p=1075)
- Ioannidis & Christodoulakis 1991, SIGMOD — https://dl.acm.org/doi/10.1145/115790.115835
- Ibaraki & Kameda 1984, *TODS* 9(3) — https://dl.acm.org/doi/10.1145/1270.1498
- Moerkotte & Neumann 2006, VLDB (DPccp) — https://dblp.org/rec/conf/vldb/MoerkotteN06.html
- Reddy & Haritsa 2005, "Analyzing Plan Diagrams of Database Query Optimizers", VLDB — https://www.vldb.org/archives/website/2005/program/paper/fri/p1228-reddy.pdf
- Graefe 1994, Volcano (IEEE TKDE); Graefe 1995, Cascades (IEEE Data Eng. Bull. 18(3))

**Textbooks and courses**
- Silberschatz, Korth & Sudarshan, *Database System Concepts* 7e: TOC https://www.db-book.com/toc-dir/toc.pdf; ch. 16 slides https://www.db-book.com/slides-dir/PDF-dir/ch16.pdf
- Ramakrishnan & Gehrke 3e, ch. 12 slides — https://pages.cs.wisc.edu/~dbbook/openAccess/thirdEdition/slides/slides3ed-english/Ch12_Overview_Query_Evaluation.pdf
- Garcia-Molina, Ullman & Widom 2e, ch. 15–16; Elmasri & Navathe 7e, ch. 18–19
- CMU 15-445 Fall 2024, schedule https://15445.courses.cs.cmu.edu/fall2024/schedule.html; L15 notes https://15445.courses.cs.cmu.edu/fall2024/notes/15-optimization.pdf
- Berkeley CS186 — https://cs186berkeley.net/
- Kleppmann, *Designing Data-Intensive Applications* 1e (2017), ch. 2 (2e, with Riccomini: ch. 3)

**Official documentation**
- PostgreSQL:
  - Using EXPLAIN https://www.postgresql.org/docs/current/using-explain.html
  - Planner statistics https://www.postgresql.org/docs/current/planner-stats.html
  - Planner/Optimizer https://www.postgresql.org/docs/current/planner-optimizer.html
  - Query planning GUCs https://www.postgresql.org/docs/current/runtime-config-query.html
  - PREPARE https://www.postgresql.org/docs/current/sql-prepare.html
  - ANALYZE https://www.postgresql.org/docs/current/sql-analyze.html
  - Expression evaluation rules https://www.postgresql.org/docs/current/sql-expressions.html
  - ORDER BY https://www.postgresql.org/docs/current/queries-order.html
  - WITH queries https://www.postgresql.org/docs/current/queries-with.html
- MySQL: Controlling Query Plan Evaluation https://dev.mysql.com/doc/refman/8.4/en/controlling-query-plan-evaluation.html
- SQL Server: Parameter Sensitive Plan optimization https://learn.microsoft.com/en-us/sql/relational-databases/performance/parameter-sensitive-plan-optimization
- SQLite: Query Planning https://sqlite.org/queryplanner.html; Next Generation Query Planner https://www.sqlite.org/queryplanner-ng.html
- MongoDB: Query Plans https://www.mongodb.com/docs/manual/core/query-plans/
- Spark: Performance Tuning (AQE) https://spark.apache.org/docs/latest/sql-performance-tuning.html
- Oracle adaptive plans: https://blogs.oracle.com/optimizer/whats-new-in-12c-adaptive-joins; RBO obsolete in 10g: https://oracle-base.com/articles/10g/performance-tuning-enhancements-10g
- Rails Guides, N+1 queries — https://guides.rubyonrails.org/active_record_querying.html

**Engineering articles and talks**
- Winand, *Use The Index, Luke* — https://use-the-index-luke.com/sql/table-of-contents
- Momjian, "Explaining the Postgres Query Optimizer" — https://momjian.us/main/writings/pgsql/optimizer.pdf
- Julia Evans, "SQL queries don't start with SELECT" (2019) — https://jvns.ca/blog/2019/10/03/sql-queries-don-t-start-with-select/
- CockroachDB, "How we built a cost-based SQL optimizer" — https://www.cockroachlabs.com/blog/building-cost-based-sql-optimizer/
