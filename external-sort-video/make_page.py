"""Build the review page (out/page/index.html) around out/web.mp4 and out/captions.vtt."""
import html
import json
import shutil
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "out"
PAGE = OUT / "page"

T = json.loads((HERE / "audio" / "timings.json").read_text())
RACE = json.loads((HERE / "data" / "race.json").read_text())
SORTCAP = json.loads((HERE / "captures" / "gnu_sort_tmp.json").read_text())
PYCAP = json.loads((HERE / "captures" / "python_memoryerror.json").read_text())


def mmss(t):
    return f"{int(t // 60)}:{int(t % 60):02d}"


def chapters():
    out = []
    for s in T["segments"]:
        d = s["end"] - s["start"]
        out.append(f'<button class="ch" style="flex-grow:{d:.2f}" data-t="{s["start"]:.2f}" '
                   f'data-end="{s["end"]:.2f}"><span class="ch-block"></span>'
                   f'<span class="ch-time">{mmss(s["start"])}</span>'
                   f'<span class="ch-name">{html.escape(s["title"])}</span></button>')
    return "\n".join(out)


def script():
    out = []
    for s in T["segments"]:
        lines = "\n".join(
            f'<button class="line" data-t="{l["start"]:.2f}" data-end="{l["end"] + 0.3:.2f}">'
            f'{html.escape(l["caption"])}</button>' for l in s["lines"])
        out.append(f'<section class="seg" data-t="{s["start"]:.2f}" data-end="{s["end"]:.2f}">'
                   f'<div class="seg-head"><span class="seg-time">{mmss(s["start"])}</span>'
                   f'<h3>{html.escape(s["title"])}</h3></div><div class="seg-lines">{lines}</div></section>')
    return "\n".join(out)


def sources():
    h, m = RACE["heapsort"]["trips"], RACE["mergesort"]["trips"]
    ch, cm = RACE["comparisons"]["heapsort"], RACE["comparisons"]["mergesort"]
    runs = sorted({f["bytes"] for s in SORTCAP["samples"] for f in s["tmp_files"]}, reverse=True)
    rows = [
        ("Opening: Python vs. sort",
         f"Real runs on this machine. GNU sort 9.4 on 1,000 MB of 10,000-byte records with "
         f"<code>-S 86000000b</code> (86 MB): {SORTCAP['n_temp_files_max']} temp files "
         f"({SORTCAP['n_temp_files_max'] - 1} of {runs[0] / 1e6:.2f} MB and one of {runs[-1] / 1e6:.2f} MB), "
         f"then one {SORTCAP['n_temp_files_max']}-way merge; done in {SORTCAP['duration_s']:.1f} s. "
         f"Python 3 under an 86 MB address-space cap: <code>MemoryError</code> after {PYCAP['duration_s']:.2f} s."),
        ("Heapsort vs. merge sort race",
         f"Simulation (<code>iosim.py</code>), LRU virtual memory: {RACE['n']:,} items, memory {RACE['M']:,} "
         f"items (1/12, the proportions of sort's file), blocks of {RACE['B']} items. Comparisons {ch:,} vs "
         f"{cm:,} ({ch / cm:.2f}×); I/Os {h:,} vs {m:,} ({h / m:.1f}×), {h / RACE['n']:.1f} per item for heapsort."),
        ("Time at typical speeds",
         f"Not measured: {ch / 1e6:.2f} M comparisons × ~100 ns (a memory access, generous for a comparison) "
         f"= {ch * 100e-9:.2f} s; {h:,} I/Os × ~100 µs (a typical SSD access) = {h * 100e-6:.0f} s."),
        ("18 → 5 → 2 passes",
         f"⌈log₂ {RACE['n']:,}⌉ = 18 merge sort passes; the first {RACE['pieces_below_memory']} make pieces "
         f"of at most 16,384 items, under memory's {RACE['M']:,}. Twelve runs plus four two-way passes = 5 "
         f"({RACE['pass_ios']['runs_then_two_way']:,} I/Os); twelve runs plus one 12-way merge = 2 "
         f"({RACE['pass_ios']['runs_then_multiway']:,} I/Os)."),
        ("The card toy",
         "48 cards, blocks of 4, memory of 4 blocks: 3 runs. The merge replays the event log of a real "
         "3-way merge: 24 I/Os to make the runs, 24 for the merge."),
        ("Scale-up numbers",
         "GNU sort merges at most 16 files at once by default (coreutils manual, <code>--batch-size</code>). "
         "16 GB ÷ 1 MB = 16,000 blocks (decimal units throughout), so about 16,000 runs per merge; "
         "100,000 runs → ⌈100,000 ÷ 15,999⌉ = 7 → 1."),
        ("PostgreSQL line",
         "PostgreSQL 16.13, a 1,000,000-row table (128 MB), default <code>work_mem</code> (4 MB), parallel "
         "query off, <code>EXPLAIN (ANALYZE, COSTS OFF)</code>: <code>Sort Method: external merge&nbsp; "
         "Disk: 107696kB</code>."),
        ("End card",
         "Ramakrishnan &amp; Gehrke, <i>Database Management Systems</i>, 3rd ed., ch. 13 (external sorting); "
         "Aggarwal &amp; Vitter, “The input/output complexity of sorting and related problems”, CACM 31(9), "
         "1988 (the lower bound); Mehlhorn &amp; Sanders, <i>The Basic Toolbox</i>, §5.7."),
    ]
    return "\n".join(f"<div class=\"src\"><dt>{a}</dt><dd>{b}</dd></div>" for a, b in rows)


CSS = """
:root{
  --bg:#0E1216;--surface:#151B22;--line:#252D36;--ink:#E6EBF0;--muted:#8C97A4;--faint:#5E6874;
  --amber:#F2A93B;--ice:#8FD3FF;
  color-scheme:dark;
}
body{background:var(--bg);color:var(--ink);font:16px/1.55 "IBM Plex Sans",system-ui,-apple-system,"Segoe UI",sans-serif;
  padding-inline:20px;padding-block:28px 64px}
.wrap{max-width:1120px;margin:0 auto;display:flex;flex-direction:column;gap:28px}
.eyebrow{font:500 12px/1 "IBM Plex Mono",ui-monospace,monospace;letter-spacing:.08em;text-transform:uppercase;color:var(--muted);
  display:flex;flex-wrap:wrap;gap:8px 18px}
.eyebrow .dot{color:var(--amber)}
h1{font-weight:600;font-size:clamp(34px,5vw,56px);line-height:1.05;margin:10px 0 8px;text-wrap:balance;letter-spacing:-.01em}
.lede{color:var(--muted);max-width:62ch;margin:0;font-size:17px}
.player{background:#000;border:1px solid var(--line);border-radius:10px;overflow:hidden;aspect-ratio:16/9;max-width:100%}
video{display:block;width:100%;height:100%}
.under{display:flex;gap:16px;align-items:center;flex-wrap:wrap;margin-top:-14px}
.cc{all:unset;cursor:pointer;font:500 13px "IBM Plex Mono",ui-monospace,monospace;color:var(--muted);
  border:1.5px solid var(--line);border-radius:6px;padding:5px 10px}
.cc[aria-pressed="true"]{color:var(--bg);background:var(--ice);border-color:var(--ice)}
.cc:focus-visible{outline:2px solid var(--ice);outline-offset:2px}
.chapters{display:flex;gap:6px;align-items:stretch}
.ch{all:unset;cursor:pointer;min-width:0;display:flex;flex-direction:column;gap:6px;flex-basis:0}
.ch-block{height:14px;border-radius:4px;border:1.5px solid var(--line);background:var(--surface);position:relative;overflow:hidden}
.ch-block::after{content:"";position:absolute;inset:0;width:var(--p,0%);background:var(--ice);opacity:.85}
.ch.on .ch-block{border-color:var(--ice)}
.ch-time{font:12px "IBM Plex Mono",ui-monospace,monospace;color:var(--faint);font-variant-numeric:tabular-nums}
.ch-name{font-size:13px;color:var(--muted);line-height:1.25;overflow:hidden;text-overflow:ellipsis}
.ch.on .ch-name{color:var(--ink)}
.ch:focus-visible .ch-block{outline:2px solid var(--ice);outline-offset:2px}
h2{font-weight:600;font-size:22px;margin:0 0 4px}
.note{color:var(--muted);margin:0;font-size:14px}
.grid{display:grid;grid-template-columns:minmax(0,1.6fr) minmax(0,1fr);gap:40px;align-items:start}
.seg{display:grid;grid-template-columns:150px minmax(0,1fr);gap:18px;padding-block:16px;border-top:1px solid var(--line)}
.seg-head{display:flex;flex-direction:column;gap:2px}
.seg-time{font:12px "IBM Plex Mono",ui-monospace,monospace;color:var(--faint);font-variant-numeric:tabular-nums}
.seg h3{margin:0;font-size:15px;font-weight:500;color:var(--muted)}
.seg.on h3{color:var(--ink)}
.seg-lines{display:flex;flex-direction:column;gap:2px}
.line{all:unset;cursor:pointer;padding:3px 8px;margin-inline:-8px;border-radius:6px;color:#C3CBD4;max-width:68ch}
.line:hover{background:var(--surface)}
.line.on{color:var(--ink);background:var(--surface);box-shadow:inset 2px 0 0 var(--ice)}
.line:focus-visible{outline:2px solid var(--ice)}
aside{display:flex;flex-direction:column;gap:22px;position:sticky;top:calc(env(safe-area-inset-top,0px) + 16px)}
dl{margin:0;display:flex;flex-direction:column;gap:14px}
.src dt{font-weight:500;font-size:14px}
.src dd{margin:2px 0 0;color:var(--muted);font-size:14px}
code{font:13px "IBM Plex Mono",ui-monospace,monospace;color:var(--ink);background:var(--surface);padding:1px 5px;border-radius:4px}
.made{color:var(--muted);font-size:14px;margin:0}
.made b{color:var(--ink);font-weight:500}
.legend{display:flex;gap:16px;flex-wrap:wrap;font-size:13px;color:var(--muted)}
.sw{display:inline-block;width:10px;height:10px;border-radius:2px;margin-right:6px;vertical-align:-1px}
@media (max-width:860px){
  .grid{grid-template-columns:1fr}
  aside{position:static}
  .seg{grid-template-columns:1fr;gap:6px}
  .ch-name{display:none}
}
@media (max-width:600px){.ch-time{display:none}.chapters{gap:4px}}
@media (prefers-reduced-motion:reduce){*{scroll-behavior:auto}}
"""

JS = """
const v=document.getElementById('v');
const chs=[...document.querySelectorAll('.ch')], segs=[...document.querySelectorAll('.seg')],
      lines=[...document.querySelectorAll('.line')];
function seek(t){v.currentTime=t;v.play().catch(()=>{});}
[...chs,...lines].forEach(b=>b.addEventListener('click',()=>seek(+b.dataset.t)));
function tick(){
  const t=v.currentTime;
  chs.forEach(c=>{const a=+c.dataset.t,b=+c.dataset.end;const on=t>=a&&t<b;c.classList.toggle('on',on);
    const p=t>=b?100:t<=a?0:(t-a)/(b-a)*100;c.style.setProperty('--p',p+'%');});
  segs.forEach(s=>s.classList.toggle('on',t>=+s.dataset.t&&t<+s.dataset.end));
  lines.forEach(l=>l.classList.toggle('on',t>=+l.dataset.t&&t<+l.dataset.end));
}
v.addEventListener('timeupdate',tick);v.addEventListener('seeked',tick);tick();
const track=v.addTextTrack('captions','English','en');
CUES.forEach(c=>track.addCue(new VTTCue(c[0],c[1],c[2])));
track.mode='hidden';
const cc=document.getElementById('cc');
cc.addEventListener('click',()=>{const on=track.mode!=='showing';track.mode=on?'showing':'hidden';
  cc.setAttribute('aria-pressed',on);cc.textContent='Captions: '+(on?'on':'off');});
"""


def main():
    PAGE.mkdir(parents=True, exist_ok=True)
    shutil.copy(OUT / "web.mp4", PAGE / "video.mp4")
    # poster: the multiway merge under way (segment 4: run three's item has gone to the output)
    s4 = next(s for s in T["segments"] if s["id"] == "s4")
    t = next(l["end"] for l in s4["lines"] if l["id"] == "s4_10") - 0.15
    import subprocess
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", str(OUT / "video.mp4"),
                    "-frames:v", "1", "-vf", "scale=1280:-2", "-q:v", "4", str(PAGE / "poster.jpg")], check=True)
    total = T["total"]
    cues = json.dumps([[round(l["start"], 2), round(l["end"] + 0.25, 2), l["caption"]]
                       for s in T["segments"] for l in s["lines"]])
    words = sum(len(l["caption"].split()) for s in T["segments"] for l in s["lines"])
    doc = f"""<title>Bigger Than Memory</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;500&family=IBM+Plex+Sans:wght@400;500;600&display=swap">
<style>{CSS}</style>
<div class="wrap">
  <header>
    <div class="eyebrow"><span>Explainer video</span><span class="dot">●</span><span>{mmss(total)}</span>
      <span class="dot">●</span><span>Undergrad CS</span><span class="dot">●</span><span>External memory algorithms</span></div>
    <h1>Bigger Than Memory</h1>
    <p class="lede">Sort a file twelve times bigger than the memory you allow, and Unix sort just finishes
      while twelve temporary files come and go. This explains what those files are: external merge sort, and why
      counting I/Os rather than comparisons is what makes it fast. Narrated, with captions under the player.</p>
  </header>
  <div class="player"><video id="v" controls preload="metadata" poster="poster.jpg" playsinline>
    <source src="video.mp4" type="video/mp4">
  </video></div>
  <div class="under"><button id="cc" class="cc" aria-pressed="false">Captions: off</button>
    <span class="note">Chapters below jump to each part.</span></div>
  <nav class="chapters" aria-label="Chapters">{chapters()}</nav>
  <div class="grid">
    <main>
      <h2>Script</h2>
      <p class="note">{words} words, voiced by Kokoro (af_heart, 0.92×). Click a line to jump there.</p>
      {script()}
    </main>
    <aside>
      <div>
        <h2>Where the numbers come from</h2>
        <p class="note">Everything on screen that looks like data is data.</p>
      </div>
      <dl>{sources()}</dl>
      <div class="legend"><span><i class="sw" style="background:var(--amber)"></i>amber: cost (block transfers)</span>
        <span><i class="sw" style="background:var(--ice)"></i>ice: the current selection</span></div>
      <p class="made"><b>How it was made.</b> The script came first and was locked before any animation:
        written from a canonical-sources survey, then revised over 15 rounds by three fresh-context reviewers
        (a domain expert, a student and an editor) until none had a blocking finding. Every number on screen
        traces to a row above.</p>
      <p class="made"><b>Made with</b> Manim Community 0.21, Kokoro TTS, ffmpeg, IBM Plex, and seaborn's
        "mako" colormap. Source: <code>external-sort-video/</code> on branch <code>claude/umap-video-plan-jp3tjk</code>.</p>
    </aside>
  </div>
</div>
<script>const CUES={cues};{JS}</script>
"""
    (PAGE / "index.html").write_text(doc)
    print(PAGE / "index.html")


if __name__ == "__main__":
    main()
