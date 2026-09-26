"""Turn a captured `claude -p --output-format stream-json --verbose` run into a per-call event log.

    python3 parse_stream.py captures/run.jsonl data/run.json

One record per model call (one API response, grouped by message id), in order:
  context   tokens the model read on that call: input + cache_creation + cache_read. This is the
            whole conversation so far, re-sent by the harness, plus the system prompt and tools.
  text      what the model wrote (thinking blocks are not recorded)
  tools     the tool calls it asked for: name and input
  results   what the harness sent back for each: content (trimmed), is_error, denied
The model identifier and the scratch path are scrubbed: the series never shows a model id.
"""
import json
import re
import sys
from pathlib import Path

MODEL_RE = re.compile(r"claude-(?:opus|sonnet|haiku|fable|instant)[a-z0-9.\-]*")


def scrub(s, root):
    s = s.replace(root + "/", "").replace(root, ".") if root else s
    return MODEL_RE.sub("<model>", s)


def parse(path):
    events = [json.loads(l) for l in Path(path).read_text().splitlines() if l.strip()]
    init = next(e for e in events if e.get("type") == "system" and e.get("subtype") == "init")
    root = init.get("cwd", "")
    calls, by_id, pending = [], {}, {}
    for e in events:
        if e.get("type") == "assistant" and not e.get("parent_tool_use_id"):
            m = e["message"]
            if m["id"] not in by_id:
                u = m["usage"]
                ctx = u["input_tokens"] + u.get("cache_creation_input_tokens", 0) + u.get("cache_read_input_tokens", 0)
                rec = {"call": len(calls) + 1, "context": ctx, "text": [], "tools": [], "results": []}
                by_id[m["id"]] = rec
                calls.append(rec)
            rec = by_id[m["id"]]
            for c in m["content"]:
                if c["type"] == "text" and c["text"].strip():
                    rec["text"].append(scrub(c["text"], root))
                elif c["type"] == "tool_use":
                    rec["tools"].append({"id": c["id"], "name": c["name"],
                                         "input": json.loads(scrub(json.dumps(c["input"]), root))})
                    pending[c["id"]] = rec
        elif e.get("type") == "user" and not e.get("parent_tool_use_id"):
            content = e["message"]["content"]
            if isinstance(content, str):
                continue
            for c in content:
                if c.get("type") != "tool_result":
                    continue
                body = c.get("content")
                if isinstance(body, list):
                    body = "\n".join(x.get("text", "") for x in body if isinstance(x, dict))
                rec = pending.get(c["tool_use_id"])
                if rec is not None:
                    rec["results"].append({"id": c["tool_use_id"], "is_error": bool(c.get("is_error")),
                                           "denied": "Permission for this tool use was denied" in (body or ""),
                                           "content": scrub(body or "", root)[:4000]})
    result = next((e for e in events if e.get("type") == "result"), {})
    summary = {"calls": len(calls), "tool_calls": sum(len(c["tools"]) for c in calls),
               "context_first": calls[0]["context"] if calls else None,
               "context_last": calls[-1]["context"] if calls else None,
               "tokens_read_total": sum(c["context"] for c in calls),
               "num_turns": result.get("num_turns"), "stop": result.get("subtype"),
               "final_text": scrub(result.get("result", "") or "", root)}
    return {"summary": summary, "calls": calls}


if __name__ == "__main__":
    out = parse(sys.argv[1])
    Path(sys.argv[2]).write_text(json.dumps(out, indent=1))
    s = out["summary"]
    print(json.dumps(s, indent=1)[:1500])
    for c in out["calls"]:
        tools = "; ".join(f"{t['name']}({json.dumps(t['input'])[:90]})" for t in c["tools"])
        errs = "".join(" ERR" if r["is_error"] else "" for r in c["results"])
        print(f"{c['call']:3d} ctx={c['context']:7,d}  {tools}{errs}  {' '.join(c['text'])[:100]!r}")
