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
    h, m, e = RACE["heapsort"]["trips"], RACE["mergesort"]["trips"], RACE["external_mergesort"]
    h64, m64 = RACE["b64"]["heapsort"], RACE["b64"]["mergesort"]
    temp = SORTCAP["n_temp_files_max"]
    run_mb = max(f["bytes"] for s in SORTCAP["samples"] for f in s["tmp_files"]) / 1e6
    rows = [
        ("Heapsort vs. merge sort race, scoreboard",
         f"Simulation (<code>iosim.py</code>): 262,144 keys, memory holds 1/16, blocks of 256, LRU cache. "
         f"Heapsort {h:,} trips, 2-way merge sort {m:,}, external merge sort {e:,}. "
         f"With blocks of 64: {h64:,} vs {m64:,} ({h64 / m64:.1f}×)."),
        ("Cold open: sort vs. Python",
         f"Real runs on this machine, scaled down 100×. GNU sort 9.4 on a 1 GB file with <code>-S 160M</code> "
         f"wrote {temp} temp files of {run_mb:.1f} MB, then did one {temp}-way merge. Python under a 600 MB "
         f"cap raised <code>MemoryError</code> at {PYCAP['peak_rss_kb_vmhwm'] / 1000:.0f} MB."),
        ("Postgres line",
         "PostgreSQL 16.13, 1,000,000 rows, default <code>work_mem</code> (4 MB), parallel query off: "
         "<code>Sort Method: external merge&nbsp; Disk: 107696kB</code>."),
        ("Sawtooth strip",
         "1,000,000 random keys, memory holds 160,000 (the 16 GB to 100 GB ratio): 7 real runs, "
         "one sampled key per pixel column."),
        ("Scale-up numbers",
         "16 GiB of memory ÷ 1 MiB blocks = 16,384 blocks, so 16,383 runs merge at once and two passes "
         "sort up to 16 GiB × 16,383 ≈ 256 TiB. 10 TB with 16 GB runs is 583 runs, which takes 10 two-way rounds."),
        ("Latency ladder",
         "Typical values, not measured here: memory ~100 ns, NVMe random read ~90 µs, hard disk seek ~10 ms, "
         "scaled so memory = 1 second."),
        ("Merge animation",
         "Replays the event log of a real 3-way merge of the 48-card toy (B = 4, M = 16): 24 trips for phase 1, "
         "24 for the merge, against 64 for 2-way merging."),
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
"""


def main():
    PAGE.mkdir(parents=True, exist_ok=True)
    shutil.copy(OUT / "web.mp4", PAGE / "video.mp4")
    shutil.copy(OUT / "captions.vtt", PAGE / "captions.vtt")
    # poster: the wide merge in full swing (segment 5, a few seconds after the heap appears)
    s5 = next(s for s in T["segments"] if s["id"] == "s5")
    t = s5["start"] + next(l["start"] for l in s5["lines"] if l["id"] == "s5_l11") - s5["start"]
    import subprocess
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{t:.2f}", "-i", str(OUT / "video.mp4"),
                    "-frames:v", "1", "-vf", "scale=1280:-2", "-q:v", "4", str(PAGE / "poster.jpg")], check=True)
    total = T["total"]
    words = sum(len(l["text"].split()) for s in T["segments"] for l in s["lines"])
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
    <p class="lede">How external merge sort sorts a file much larger than RAM, and the I/O model that explains
      why it takes only two passes. Narration and visuals; captions are in the player's CC menu.</p>
  </header>
  <div class="player"><video id="v" controls preload="metadata" poster="poster.jpg" playsinline>
    <source src="video.mp4" type="video/mp4">
    <track kind="captions" src="captions.vtt" srclang="en" label="English">
  </video></div>
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
      <p class="made"><b>Made with</b> Manim Community 0.21, Kokoro TTS, ffmpeg, IBM Plex, and seaborn's
        "mako" colormap. Source: <code>external-sort-video/</code> on branch <code>claude/umap-video-plan-jp3tjk</code>.</p>
    </aside>
  </div>
</div>
<script>{JS}</script>
"""
    (PAGE / "index.html").write_text(doc)
    print(PAGE / "index.html")


if __name__ == "__main__":
    main()
