# Bigger Than Memory

A 5-minute explainer on external merge sort and the I/O model, for undergrad CS.
`PLAN.md` is the plan it was built from; `out/web.mp4` is the finished video.

## Pipeline

| Step | Command | Writes |
|---|---|---|
| Narration (Kokoro, `af_heart`, 0.92×) | `python narration.py` | `audio/narration.{wav,mp3}`, `audio/timings.json` |
| Data behind the visuals | `python make_data.py` | `data/` (race traces, sawtooth strip, toy merge event log) |
| Real-world captures | see `captures/README.md` | `captures/` (GNU sort, Python, Postgres) |
| Animation and assembly | `python build.py` (`--only s5`, `--preview`) | `out/video.mp4`, `out/web.mp4`, `out/captions.vtt` |
| Review page | `python make_page.py` | `out/page/` |

Each scene in `scenes/` reads its segment's line timings from `audio/timings.json`, so changing
a line of narration and re-running `narration.py` and `build.py` keeps the cuts in sync.

Requirements: Python 3.11 with `manim` 0.21, `kokoro`, `torch`, `numpy`, `matplotlib`, `seaborn`,
`scipy`, `soundfile`; system `ffmpeg`, `espeak-ng`, Cairo/Pango and the IBM Plex fonts.

## What is real

- The heapsort vs. merge sort race and the scoreboard come from `iosim.py` (an LRU cache counting
  block transfers).
- The cold open replays real runs of GNU sort and Python, scaled down 100×. The Postgres
  output is a real `EXPLAIN ANALYZE`.
- The toy merge replays the event log of a real 3-way merge.
- The latency ladder uses typical published values, not measurements.
