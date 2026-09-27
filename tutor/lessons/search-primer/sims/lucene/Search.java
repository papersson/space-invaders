// Lucene side of the search primer's evidence: index TREC-COVID with Lucene's English analyzer and
// its default BM25 (k1 = 1.2, b = 0.75), then read posting lists, scores, explanations and timings.
//
//   javac -cp 'jars/*' Search.java
//   java -cp 'jars/*:.' Search index   CORPUS_TSV INDEX_DIR
//   java -cp 'jars/*:.' Search stats   INDEX_DIR word ...          (analysed with the English analyzer)
//   java -cp 'jars/*:.' Search run     INDEX_DIR TOPICS_TSV FIELD K OUT [tfidf]  (FIELD 1 = keyword query, 2 = question)
//   java -cp 'jars/*:.' Search explain INDEX_DIR "query" N [tfidf]
//   java -cp 'jars/*:.' Search analyze "text"
//   java -cp 'jars/*:.' Search mismatch INDEX_DIR "query"        (query analysed without stemming)
//   java -cp 'jars/*:.' Search timing  INDEX_DIR CORPUS_TSV "query" REPEATS
//   java -cp 'jars/*:.' Search boolean INDEX_DIR word word       (AND / OR match counts)
//   java -cp 'jars/*:.' Search term    INDEX_DIR Word ...           (exact term lookup, no analysis)
//   java -cp 'jars/*:.' Search doc     INDEX_DIR PAPER_ID word ...  (counts, positions, BM25 explanation)
import java.io.*;
import java.nio.file.*;
import java.util.*;
import org.apache.lucene.analysis.*;
import org.apache.lucene.analysis.en.EnglishAnalyzer;
import org.apache.lucene.analysis.standard.StandardAnalyzer;
import org.apache.lucene.analysis.tokenattributes.CharTermAttribute;
import org.apache.lucene.document.*;
import org.apache.lucene.index.*;
import org.apache.lucene.queryparser.classic.QueryParser;
import org.apache.lucene.search.*;
import org.apache.lucene.search.similarities.*;
import org.apache.lucene.store.FSDirectory;
import org.apache.lucene.util.BytesRef;

public class Search {
  static final String F = "body";

  /** Plain TF-IDF: score = sum over query terms of tf * ln(N / n). No saturation, no length normalisation. */
  static class RawTfIdf extends SimilarityBase {
    @Override protected double score(BasicStats stats, double freq, double docLen) {
      return freq * Math.log((double) stats.getNumberOfDocuments() / stats.getDocFreq());
    }
    @Override public String toString() { return "raw tf-idf"; }
  }

  static List<String> tokens(Analyzer a, String text) throws IOException {
    List<String> out = new ArrayList<>();
    try (TokenStream ts = a.tokenStream(F, text)) {
      CharTermAttribute t = ts.addAttribute(CharTermAttribute.class);
      ts.reset();
      while (ts.incrementToken()) out.add(t.toString());
      ts.end();
    }
    return out;
  }

  static IndexSearcher searcher(String dir) throws IOException {
    return new IndexSearcher(DirectoryReader.open(FSDirectory.open(Paths.get(dir))));
  }

  static Query parse(Analyzer a, String q) throws Exception {
    return new QueryParser(F, a).parse(QueryParser.escape(q));
  }

  public static void main(String[] args) throws Exception {
    Analyzer en = new EnglishAnalyzer();
    switch (args[0]) {
      case "index": {
        IndexWriterConfig cfg = new IndexWriterConfig(en).setOpenMode(IndexWriterConfig.OpenMode.CREATE)
            .setRAMBufferSizeMB(256);
        long t0 = System.nanoTime();
        try (IndexWriter w = new IndexWriter(FSDirectory.open(Paths.get(args[2])), cfg);
             BufferedReader r = Files.newBufferedReader(Paths.get(args[1]))) {
          String line;
          int n = 0;
          while ((line = r.readLine()) != null) {
            String[] p = line.split("\t", 2);
            Document d = new Document();
            d.add(new StringField("id", p[0], Field.Store.YES));
            d.add(new TextField(F, p.length > 1 ? p[1] : "", Field.Store.NO));
            w.addDocument(d);
            n++;
          }
          w.forceMerge(1);
          System.out.printf("indexed %d documents in %.1f s%n", n, (System.nanoTime() - t0) / 1e9);
        }
        break;
      }
      case "stats": {
        IndexSearcher s = searcher(args[1]);
        IndexReader r = s.getIndexReader();
        long docs = r.getDocCount(F), sum = r.getSumTotalTermFreq(F);
        LeafReader leaf = r.leaves().get(0).reader();
        Terms terms = leaf.terms(F);
        System.out.printf("N=%d sumTotalTermFreq=%d avgdl=%.3f uniqueTerms=%d leaves=%d%n", docs, sum,
            (double) sum / docs, terms.size(), r.leaves().size());
        StoredFields sf = s.storedFields();
        for (int i = 2; i < args.length; i++) {
          for (String t : tokens(en, args[i])) {
            TermsEnum te = terms.iterator();
            if (!te.seekExact(new BytesRef(t))) { System.out.printf("%s -> %s: not in index%n", args[i], t); continue; }
            System.out.printf("%s -> %s: df=%d ttf=%d first postings:", args[i], t, te.docFreq(), te.totalTermFreq());
            PostingsEnum pe = te.postings(null, PostingsEnum.POSITIONS);
            for (int k = 0; k < 5 && pe.nextDoc() != DocIdSetIterator.NO_MORE_DOCS; k++) {
              StringBuilder pos = new StringBuilder();
              for (int j = 0; j < pe.freq(); j++) pos.append(j == 0 ? "" : ",").append(pe.nextPosition());
              System.out.printf(" [doc %d id=%s tf=%d pos=%s]", pe.docID(), sf.document(pe.docID()).get("id"), pe.freq(), pos);
            }
            System.out.println();
          }
        }
        break;
      }
      case "run": {
        IndexSearcher s = searcher(args[1]);
        if (args.length > 6 && args[6].equals("tfidf")) s.setSimilarity(new RawTfIdf());
        String tag = args.length > 6 ? args[6] : "lucene-bm25";
        int field = Integer.parseInt(args[3]), k = Integer.parseInt(args[4]);
        StoredFields sf = s.storedFields();
        try (PrintWriter out = new PrintWriter(args[5])) {
          for (String line : Files.readAllLines(Paths.get(args[2]))) {
            String[] p = line.split("\t");
            TopDocs td = s.search(parse(en, p[field]), k);
            int rank = 1;
            for (ScoreDoc d : td.scoreDocs)
              out.printf(Locale.ROOT, "%s Q0 %s %d %.6f %s%n", p[0], sf.document(d.doc).get("id"), rank++, d.score, tag);
          }
        }
        break;
      }
      case "explain": {
        IndexSearcher s = searcher(args[1]);
        if (args.length > 4 && args[4].equals("tfidf")) s.setSimilarity(new RawTfIdf());
        Query q = parse(en, args[2]);
        System.out.println("query: " + q);
        TopDocs td = s.search(q, Integer.parseInt(args[3]));
        System.out.println("total hits: " + td.totalHits);
        StoredFields sf = s.storedFields();
        for (ScoreDoc d : td.scoreDocs) {
          System.out.printf("=== doc %d id=%s score=%.6f%n", d.doc, sf.document(d.doc).get("id"), d.score);
          System.out.println(s.explain(q, d.doc));
        }
        break;
      }
      case "analyze": {
        System.out.println("english:  " + tokens(en, args[1]));
        System.out.println("standard: " + tokens(new StandardAnalyzer(), args[1]));
        System.out.println("stopwords: " + EnglishAnalyzer.ENGLISH_STOP_WORDS_SET);
        break;
      }
      case "mismatch": {
        IndexSearcher s = searcher(args[1]);
        for (Analyzer a : new Analyzer[] {en, new StandardAnalyzer()}) {
          Query q = parse(a, args[2]);
          System.out.printf("%s -> %s : %s hits%n", a.getClass().getSimpleName(), q, s.count(q));
          for (String t : tokens(a, args[2])) {
            TermQuery tq = new TermQuery(new Term(F, t));
            System.out.printf("   term %s : %d docs%n", t, s.count(tq));
          }
        }
        break;
      }
      case "term": {   // look terms up exactly as given, with no analysis (like a term query on a text field)
        IndexSearcher s = searcher(args[1]);
        for (int i = 2; i < args.length; i++)
          System.out.printf("unanalysed term '%s': %d documents; analysed %s: %d documents%n", args[i],
              s.count(new TermQuery(new Term(F, args[i]))), tokens(en, args[i]), s.count(parse(en, args[i])));
        break;
      }
      case "doc": {   // one paper: its Lucene doc number, and per query word: count, positions; then the BM25 explanation
        IndexSearcher s = searcher(args[1]);
        TopDocs hit = s.search(new TermQuery(new Term("id", args[2])), 1);
        int doc = hit.scoreDocs[0].doc;
        LeafReader leaf = s.getIndexReader().leaves().get(0).reader();
        System.out.printf("paper %s = doc %d%n", args[2], doc);
        StringBuilder q = new StringBuilder();
        for (int i = 3; i < args.length; i++) {
          q.append(args[i]).append(' ');
          for (String t : tokens(en, args[i])) {
            PostingsEnum pe = leaf.postings(new Term(F, t), PostingsEnum.POSITIONS);
            if (pe == null || pe.advance(doc) != doc) { System.out.printf("  %s: 0%n", t); continue; }
            StringBuilder pos = new StringBuilder();
            for (int j = 0; j < pe.freq(); j++) pos.append(j == 0 ? "" : ",").append(pe.nextPosition());
            System.out.printf("  %s: tf=%d positions=%s%n", t, pe.freq(), pos);
          }
        }
        Query query = parse(en, q.toString().trim());
        System.out.println(s.explain(query, doc));
        break;
      }
      case "boolean": {
        IndexSearcher s = searcher(args[1]);
        String a = tokens(en, args[2]).get(0), b = tokens(en, args[3]).get(0);
        TermQuery qa = new TermQuery(new Term(F, a)), qb = new TermQuery(new Term(F, b));
        Query and = new BooleanQuery.Builder().add(qa, BooleanClause.Occur.MUST).add(qb, BooleanClause.Occur.MUST).build();
        Query or = new BooleanQuery.Builder().add(qa, BooleanClause.Occur.SHOULD).add(qb, BooleanClause.Occur.SHOULD).build();
        System.out.printf("%s: %d  %s: %d  AND: %d  OR: %d%n", a, s.count(qa), b, s.count(qb), s.count(and), s.count(or));
        break;
      }
      case "timing": {
        IndexSearcher s = searcher(args[1]);
        List<String> docs = new ArrayList<>();
        long bytes = 0;
        try (BufferedReader r = Files.newBufferedReader(Paths.get(args[2]))) {
          String line;
          while ((line = r.readLine()) != null) { String t = line.split("\t", 2)[1].toLowerCase(Locale.ROOT); docs.add(t); bytes += t.length(); }
        }
        List<String> words = tokens(new StandardAnalyzer(), args[3]);
        Query q = parse(en, args[3]);
        int reps = Integer.parseInt(args[4]);
        long[] scan = new long[reps], idx = new long[reps];
        int found = 0;
        for (int rep = 0; rep < reps; rep++) {
          long t0 = System.nanoTime();
          found = 0;
          for (String d : docs) {   // text lowercased in advance: the scan only tests for the words
            boolean any = false;
            for (String w : words) if (d.contains(w)) { any = true; break; }
            if (any) found++;
          }
          scan[rep] = System.nanoTime() - t0;
          t0 = System.nanoTime();
          TopDocs td = s.search(q, 10);
          idx[rep] = System.nanoTime() - t0;
        }
        Arrays.sort(scan); Arrays.sort(idx);
        System.out.printf("docs=%d chars=%d words=%s scan-found=%d%n", docs.size(), bytes, words, found);
        System.out.printf("scan (substring test on every document, text lowercased in advance): median %.1f ms, min %.1f ms%n", scan[reps / 2] / 1e6, scan[0] / 1e6);
        System.out.printf("index (BM25 top 10 via posting lists): median %.3f ms, min %.3f ms%n", idx[reps / 2] / 1e6, idx[0] / 1e6);
        break;
      }
      default:
        throw new IllegalArgumentException(args[0]);
    }
  }
}
