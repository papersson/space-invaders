"""A small LLM agent in one file: a model that only writes text, a program that runs its requests,
and a loop. Derived from lessons/llm-agents/sims/agent.py, with a plain-text request format and a
search tool.

    python3 agent.py WORKDIR OUT.json

The model is Claude, called through the `claude` command-line tool with its own tools turned off
(`--tools ""`), so each call is text in, text out, and each call is a fresh process that remembers
nothing. Everything else an agent does is in this file: it sends the whole context on every call,
spots a request in the reply, carries it out itself, and appends the result to the context. The
tools are plain Python functions confined to WORKDIR; run tests runs one fixed command.

The request format (one request per reply):
    search: TEXT              lines in the project's files that contain TEXT
    open file: NAME           the file's text, with line numbers
    edit file: NAME           replace some lines of the file with others: the lines between
    replace:                    "replace:" and "with:" (which must appear exactly once in the
    OLD LINES                   file) become the lines between "with:" and "end edit"
    with:
    NEW LINES
    end edit
    run tests                 runs python3 -m unittest and returns its output
A reply with no request in it is the model's answer, and the loop stops.
"""
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

TASK = ("Our program stops with this error:\n\n"
        "LookupError: no price for 'gadget'\n\n"
        "Please fix it, and check that the tests pass.")

SYSTEM = """You are a coding agent working on a small Python project. You cannot see or run anything yourself. To get something done, reply with exactly one request, in one of the forms below, and nothing else. A program carries out the request and sends you the result.

search: TEXT
    lists every line in the project's files that contains TEXT
open file: NAME
    shows the file, with line numbers
edit file: NAME
replace:
THE LINES TO REPLACE, COPIED EXACTLY FROM THE FILE
with:
THE NEW LINES
end edit
    replaces those lines (they must appear exactly once in the file)
run tests
    runs the project's tests and shows their output

When you have finished the task, reply with a short message for the user, with no request in it."""


# --- the tools: ordinary code, run by this program, never by the model ----------------------------
class Tools:
    def __init__(self, root):
        self.root, self.log = Path(root).resolve(), []

    def _path(self, name):
        p = (self.root / name).resolve()
        if self.root not in p.parents or not p.is_file():
            raise ValueError(f"there is no file called {name}")
        return p

    def files(self):
        return sorted(p for p in self.root.iterdir() if p.is_file() and p.suffix in (".py", ".csv", ".md", ".txt"))

    def search(self, text):
        hits = [f"{p.name}:{i}: {line.strip()}" for p in self.files()
                for i, line in enumerate(p.read_text().splitlines(), 1) if text in line]
        return "\n".join(hits) if hits else "no matches"

    def open_file(self, name):
        lines = self._path(name).read_text().splitlines()
        return "\n".join(f"{i:3d}  {line}" for i, line in enumerate(lines, 1))

    def edit_file(self, name, old, new):
        p = self._path(name)
        if old is None:
            return 'error: an edit needs "replace:", the old lines, "with:", the new lines, and "end edit"'
        if not old.strip():
            return "error: there are no lines to replace"
        text = p.read_text()
        n = text.count(old)
        if n != 1:
            return f"error: that text appears {n} times in {name}, not once"
        p.write_text(text.replace(old, new))
        return f"edited {name}"

    def run_tests(self):
        r = subprocess.run([sys.executable, "-m", "unittest"], cwd=self.root, capture_output=True,
                           text=True, timeout=30)
        return (r.stdout + r.stderr).replace(str(self.root) + "/", "")

    def run(self, request):
        kind, args = request
        try:
            return getattr(self, kind)(*args)
        except Exception as e:  # a failed tool is still a result the model should see
            return f"error: {e}"


# --- spotting a request in the model's text -------------------------------------------------------
def parse_request(reply):
    """(tool, args) for the first request in the reply, or None: no request means the model is done."""
    raw = reply.strip().splitlines()
    lines = [l.strip() for l in raw]
    for i, line in enumerate(lines):
        if m := re.fullmatch(r"search:\s*(.+)", line):
            return "search", (m.group(1),)
        if m := re.fullmatch(r"open file:\s*(\S+)", line):
            return "open_file", (m.group(1),)
        if m := re.fullmatch(r"edit file:\s*(\S+)", line):
            try:
                a = lines.index("replace:", i + 1)
                b = lines.index("with:", a + 1)
                c = lines.index("end edit", b + 1)
            except ValueError:  # malformed: the tool reports the error
                return "edit_file", (m.group(1), None, None)
            return "edit_file", (m.group(1), "\n".join(raw[a + 1:b]), "\n".join(raw[b + 1:c]))
        if line == "run tests":
            return "run_tests", ()
    return None


# --- the model: one call is one fresh process ------------------------------------------------------
def render(context):
    heads = {"task": "TASK", "model": "YOU WROTE", "result": "RESULT"}
    return "\n\n".join(f"{heads[role]}\n{text}" for role, text in context)


def call_model(tools, context):
    """Send the instructions and the whole context; return the model's reply."""
    prompt = render(context)
    r = subprocess.run(["claude", "-p", "--tools", "", "--system-prompt", SYSTEM,
                        "--output-format", "json", "--no-session-persistence", "--safe-mode",
                        "--disable-slash-commands", "--strict-mcp-config"],
                       input=prompt, capture_output=True, text=True, timeout=600, cwd=tools.root)
    out = json.loads(r.stdout)
    u = out["usage"]
    tools.log.append({"call": len(tools.log) + 1, "prompt_chars": len(prompt),
                      "context_tokens": u["input_tokens"] + u["cache_creation_input_tokens"]
                      + u["cache_read_input_tokens"], "output_tokens": u["output_tokens"]})
    return out["result"].strip()


# --- the loop --------------------------------------------------------------------------------------
def agent(task, tools, max_calls=20):
    context = [("task", task)]
    for _ in range(max_calls):
        reply = call_model(tools, context)
        context.append(("model", reply))
        request = parse_request(reply)
        if request is None:
            return context
        context.append(("result", tools.run(request)))
    return context


def main():
    workdir, out = sys.argv[1], sys.argv[2]
    tools = Tools(workdir)
    t0 = time.time()
    context = agent(TASK, tools)
    # Afterwards, and outside the agent: do the tests really pass, and does the program run?
    after = tools.run_tests()
    prog = subprocess.run([sys.executable, "invoice.py", "orders.csv"], cwd=tools.root, capture_output=True,
                          text=True, timeout=30)
    record = {"task": TASK, "system": SYSTEM, "context": context, "calls": tools.log,
              "seconds": round(time.time() - t0, 1), "test_after": after,
              "passed_after": after.rstrip().endswith("OK"),
              "program_after": (prog.stdout + prog.stderr).replace(str(tools.root) + "/", "")}
    Path(out).write_text(json.dumps(record, indent=1))
    for c in tools.log:
        print(f"call {c['call']:2d}: context {c['context_tokens']:6,d} tokens")
    for role, text in context:
        print(f"--- {role}\n{text[:700]}")
    print("TEST AFTER:", "PASS" if record["passed_after"] else "FAIL", after.strip().splitlines()[-1])
    print("PROGRAM AFTER:", record["program_after"].strip())


if __name__ == "__main__":
    main()
