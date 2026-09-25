"""Render the narration with Kokoro TTS, one line at a time.

Writes audio/narration.wav, audio/narration.mp3 and audio/timings.json. Every
line keeps its own start/end time, so the animation can cue off line ids and a
single line can be re-recorded without touching the rest.

    python narration.py            # render with Kokoro
    python narration.py --estimate # timings only, from word counts (no audio)
"""
import json
import subprocess
import sys
from pathlib import Path

VOICE = "af_heart"
SPEED = 0.92
RATE = 24_000
LEAD_IN = 0.8        # silence before the first line
LINE_GAP = 0.45      # between lines inside a segment
SEGMENT_GAP = 1.2    # between segments
TAIL = 2.5           # silence after the last line

# (segment id, title, [(line id, text, extra hold after the line in seconds)])
# Spelling is for the ear: "Rocks D B", "N log N", years in words.
SCRIPT = [
    ("s1", "Cold open", [
        ("l1", "Here's a hundred-gigabyte file, and a laptop with sixteen gigabytes of memory.", 0),
        ("l2", "Ask Python to sort it, and it runs out of memory.", 0.3),
        ("l3", "Ask the Unix sort command, and it just... finishes.", 0),
        ("l4", "While it works, files pile up in the temp folder, and then they vanish.", 0.4),
        ("l5", "Those files are the whole trick.", 0.3),
        ("l6", "This is how you compute on data that's bigger than your memory.", 2.6),
    ]),
    ("s2", "The memory wall", [
        ("l1", "Picture memory as your desk, and the disk as a warehouse across town.", 0),
        ("l2", "The desk is small, but anything on it is instant. The warehouse holds everything, but every trip is slow.", 0),
        ("l3", "How slow? If reaching into memory took one second, a read from a fast SSD would take about fifteen minutes.", 0),
        ("l4", "A seek on a spinning hard drive: more than a day.", 0.6),
        ("l5", "There's one saving grace. A trip costs about the same whether you bring back one item, or a whole crate.", 0),
        ("l6", "So what matters isn't how many operations you do. It's how many trips you make.", 0.4),
        ("l7", "On paper, heapsort and merge sort are both N log N.", 0),
        ("l8", "But heapsort hops all over the file, and makes about four trips for every item it sorts.", 0),
        ("l9", "Merge sort sweeps through in long, straight lines, and needs dozens of times fewer.", 0),
        ("l10", "And bigger crates only widen the gap.", 1.5),
    ]),
    ("s3", "The I/O model", [
        ("l1", "Computer scientists turned this into a model with three numbers.", 0),
        ("l2", "N: how many items you have.", 0),
        ("l3", "M: how many fit in memory.", 0),
        ("l4", "B: how many come in one crate, called a block.", 0.2),
        ("l5", "Then one bold simplification: computation is free. The only cost is the number of blocks moved between disk and memory.", 0),
        ("l6", "Reading the whole file once costs N over B. That's our yardstick, and it's called a scan.", 0.8),
    ]),
    ("s4", "Phase 1: runs", [
        ("l1", "The classic algorithm is external merge sort, and it works in two phases.", 0),
        ("l2", "Phase one: fill memory, sort it right there, which is free, and write it back to disk as a sorted chunk called a run.", 0),
        ("l3", "Repeat until you've been through the whole file.", 0.8),
        ("l4", "It still isn't sorted, but now it's made of sorted runs.", 0),
        ("l5", "Every block was read once and written once: two scans.", 2.2),
    ]),
    ("s5", "Phase 2: the wide merge", [
        ("l1", "Phase two: merge the runs.", 0),
        ("l2", "You already know how to merge two sorted lists: compare the fronts, take the smaller, repeat.", 0),
        ("l3", "Merge the runs in pairs, then pairs of pairs, until one is left, and every round reads and writes the whole file.", 0.6),
        ("l4", "But look at memory while that happens.", 0),
        ("l5", "To merge two runs, you only need the front block of each, plus one block for the output. The rest of the desk sits empty.", 0.5),
        ("l6", "So use it. Give every run its own one-block buffer, and merge them all at once.", 0),
        ("l7", "A small heap tracks which run has the smallest item at its front.", 0),
        ("l8", "Move that item to the output buffer.", 0),
        ("l9", "When the output block fills, write it out in one trip.", 0),
        ("l10", "When an input buffer runs dry, fetch that run's next block.", 0),
        ("l11", "Every block still makes exactly one trip in, and one trip out.", 3.0),
        ("l12", "How many runs fit at once? About one per block of memory: M over B.", 0),
        ("l13", "With sixteen gigabytes of memory and one-megabyte blocks, that's over sixteen thousand runs, merged in a single pass.", 1.2),
    ]),
    ("s6", "How many passes", [
        ("l1", "So the number of passes is still a logarithm, but its base is M over B instead of two, and that base is enormous.", 0),
        ("l2", "To sort ten terabytes on this laptop, two-way merging needs ten rounds over the data. The wide merge needs one.", 0),
        ("l3", "In fact, one pass to form runs plus one pass to merge can sort about a quarter of a petabyte.", 0.4),
        ("l4", "And it's optimal: in nineteen eighty-eight, Aggarwal and Vitter proved that no comparison sort can do asymptotically fewer transfers.", 0.3),
        ("l5", "In our simulation, that's the difference between almost a million trips, and about four thousand.", 1.5),
    ]),
    ("s7", "You've seen this", [
        ("l1", "Once you know this pattern, you see it everywhere.", 0),
        ("l2", "When a database has to sort more rows than its memory budget, Postgress reports external merge, and spills runs to disk.", 0),
        ("l3", "Big-data shuffles in MapReduce and Spark sort chunks, spill them, and merge.", 0),
        ("l4", "Storage engines like Rocks D B write sorted files, and keep merging them in the background.", 0),
        ("l5", "Searching gets the same treatment: a B-tree gives each node hundreds of children, so any of a billion keys is three or four trips away.", 0),
        ("l6", "And the desk and warehouse are relative: the same model describes cache versus RAM, and GPU memory versus the rest of the machine.", 0.5),
    ]),
    ("s8", "Recap", [
        ("l1", "So, when data outgrows memory: count trips, not operations.", 0),
        ("l2", "Stream through the data, instead of hopping around it.", 0),
        ("l3", "Build runs as big as memory, then merge as many as memory allows.", 0.3),
        ("l4", "That's external merge sort: a logarithm with a huge base, which is why sorting a file bigger than your RAM usually takes just two passes.", 0),
    ]),
]

# Spoken spellings -> how captions should read them.
CAPTION_FIXES = [("Postgress", "Postgres"), ("Rocks D B", "RocksDB"), ("nineteen eighty-eight", "1988"),
                 ("sixteen gigabytes", "16 GB"), ("one-megabyte", "1 MB"), ("sixteen thousand", "16,000"),
                 ("ten terabytes", "10 TB"), ("hundred-gigabyte", "100 GB"), ("just... finishes", "just… finishes")]


def caption(text):
    for spoken, shown in CAPTION_FIXES:
        text = text.replace(spoken, shown)
    return text


HERE = Path(__file__).parent
OUT = HERE / "audio"


def layout(durations):
    """Place every line on one timeline; segments start at their first line."""
    t, segments = LEAD_IN, []
    for si, (sid, title, lines) in enumerate(SCRIPT):
        if si:
            t += SEGMENT_GAP
        seg = {"id": sid, "title": title, "start": t, "lines": []}
        for li, (lid, text, hold) in enumerate(lines):
            if li:
                t += LINE_GAP
            d = durations[f"{sid}_{lid}"]
            seg["lines"].append({"id": f"{sid}_{lid}", "text": text, "caption": caption(text), "start": round(t, 3),
                                 "end": round(t + d, 3)})
            t += d + hold
        segments.append(seg)
    total = t + TAIL
    # A segment's video runs from its first line to the next segment's first line,
    # so the silence between segments belongs to the segment that just ended.
    segments[0]["start"] = 0.0
    for a, b in zip(segments, segments[1:]):
        b["start"] = round(b["lines"][0]["start"] - 0.35, 3)
        a["end"] = b["start"]
    segments[-1]["end"] = round(total, 3)
    return {"voice": VOICE, "speed": SPEED, "total": round(total, 3), "segments": segments}


def main():
    OUT.mkdir(exist_ok=True)
    lines = [(f"{sid}_{lid}", text) for sid, _, ls in SCRIPT for lid, text, _ in ls]
    if "--estimate" in sys.argv:
        timings = layout({k: len(t.split()) / 2.8 + 0.3 for k, t in lines})
        (OUT / "timings.json").write_text(json.dumps(timings, indent=1))
        print(f"estimated total {timings['total']:.1f}s")
        return

    import numpy as np
    import soundfile as sf
    from kokoro import KPipeline

    pipe = KPipeline(lang_code="a", repo_id="hexgrad/Kokoro-82M")
    clips, phonemes = {}, {}
    for key, text in lines:
        parts = list(pipe(text, voice=VOICE, speed=SPEED, split_pattern=None))
        audio = np.concatenate([p.audio.numpy() for p in parts])
        # trim Kokoro's own leading/trailing silence so gaps are ours to control
        nz = np.flatnonzero(np.abs(audio) > 0.01)
        clips[key] = audio[max(nz[0] - 240, 0): nz[-1] + 480]
        phonemes[key] = " ".join(p.phonemes for p in parts)
        print(f"{key}: {len(clips[key]) / RATE:5.2f}s  {phonemes[key][:70]}")

    timings = layout({k: len(a) / RATE for k, a in clips.items()})
    track = np.zeros(int(timings["total"] * RATE) + RATE, dtype=np.float32)
    for seg in timings["segments"]:
        for ln in seg["lines"]:
            i = int(round(ln["start"] * RATE))
            track[i: i + len(clips[ln["id"]])] = clips[ln["id"]]
    track = track[: int(timings["total"] * RATE)]
    sf.write(OUT / "narration.wav", track, RATE)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(OUT / "narration.wav"),
                    "-codec:a", "libmp3lame", "-b:a", "128k", str(OUT / "narration.mp3")], check=True)
    timings["phonemes"] = phonemes
    timings["peak"] = float(np.abs(track).max())
    (OUT / "timings.json").write_text(json.dumps(timings, indent=1))
    print(f"total {timings['total']:.1f}s, peak {timings['peak']:.2f}")


if __name__ == "__main__":
    main()
