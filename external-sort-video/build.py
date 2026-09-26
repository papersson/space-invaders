"""Render every scene, join them, add the narration and write captions.

    python build.py                 # 1080p30, all scenes
    python build.py --only s5       # re-render one segment, then re-assemble
    python build.py --preview       # 480p15, faster

Outputs in out/: video.mp4 (master), web.mp4 (smaller, for the page), captions.vtt.
Scene lengths come from audio/timings.json, so the cuts land on the narration.
"""
import json
import subprocess
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

HERE = Path(__file__).parent
SCENES = [(f"s{i}", f"v2_s{i}.py", f"V2S{i}") for i in range(1, 7)]
OUT = HERE / "out"


def media_dir():
    import os
    return Path(os.environ.get("MEDIA_DIR", HERE / "media"))


def render(seg, preview):
    sid, file, cls = seg
    q = ["-ql"] if preview else ["--resolution", "1920,1080", "--frame_rate", "30"]
    cmd = ["manim", *q, "--disable_caching", "--media_dir", str(media_dir()), file, cls]
    r = subprocess.run(cmd, cwd=HERE / "scenes", capture_output=True, text=True)
    if r.returncode:
        raise RuntimeError(f"{cls} failed:\n{r.stdout[-3000:]}\n{r.stderr[-3000:]}")
    sub = "480p15" if preview else "1080p30"
    return media_dir() / "videos" / Path(file).stem / sub / f"{cls}.mp4"


def duration(path):
    out = subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0",
                          str(path)], capture_output=True, text=True).stdout
    return float(out)


def vtt_time(t):
    h, rem = divmod(t, 3600)
    m, s = divmod(rem, 60)
    return f"{int(h):02d}:{int(m):02d}:{s:06.3f}"


def captions(timings):
    lines = ["WEBVTT", ""]
    for seg in timings["segments"]:
        for ln in seg["lines"]:
            lines += [vtt_time(ln["start"]) + " --> " + vtt_time(ln["end"] + 0.25), ln["caption"], ""]
    (OUT / "captions.vtt").write_text("\n".join(lines))


def main():
    preview = "--preview" in sys.argv
    only = sys.argv[sys.argv.index("--only") + 1].split(",") if "--only" in sys.argv else None
    OUT.mkdir(exist_ok=True)
    timings = json.loads((HERE / "audio" / "timings.json").read_text())
    todo = [s for s in SCENES if only is None or s[0] in only]
    with ThreadPoolExecutor(max_workers=4) as ex:
        for seg, path in zip(todo, ex.map(lambda s: render(s, preview), todo)):
            print(f"{seg[0]}: {path.name} {duration(path):.2f}s")
    sub = "480p15" if preview else "1080p30"
    parts = [media_dir() / "videos" / Path(f).stem / sub / f"{c}.mp4" for _, f, c in SCENES]
    expected = {s["id"]: s["end"] - s["start"] for s in timings["segments"]}
    for (sid, _, _), p in zip(SCENES, parts):
        d = duration(p)
        flag = "" if abs(d - expected[sid]) < 0.1 else "  <-- length mismatch"
        print(f"  {sid} {d:7.2f}s (narration {expected[sid]:7.2f}s){flag}")
    lst = OUT / "parts.txt"
    lst.write_text("".join(f"file '{p}'\n" for p in parts))
    master = OUT / ("preview.mp4" if preview else "video.mp4")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst),
                    "-i", str(HERE / "audio" / "narration.wav"), "-map", "0:v", "-map", "1:a",
                    "-c:v", "libx264", "-crf", "18", "-preset", "medium", "-pix_fmt", "yuv420p",
                    "-c:a", "aac", "-b:a", "160k", "-movflags", "+faststart", str(master)], check=True)
    captions(timings)
    print(f"{master.name}: {duration(master):.2f}s, {master.stat().st_size / 1e6:.1f} MB "
          f"(narration {timings['total']:.2f}s)")
    if not preview:
        web = OUT / "web.mp4"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(master), "-c:v", "libx264",
                        "-crf", "27", "-preset", "slow", "-tune", "animation", "-pix_fmt", "yuv420p",
                        "-c:a", "aac", "-b:a", "96k", "-movflags", "+faststart", str(web)], check=True)
        print(f"web.mp4: {web.stat().st_size / 1e6:.1f} MB")


if __name__ == "__main__":
    main()
