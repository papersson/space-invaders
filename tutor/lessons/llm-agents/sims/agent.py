"""A complete LLM agent in one file: a model, a few tools, and a loop.

    python3 agent.py VARIANT WORKDIR OUT.json

The model is Claude, called through the `claude` command-line tool with its own tools turned off
(`--tools ""`), so each call is plain text in, text out, and each call is a fresh process that
remembers nothing. The command-line tool adds about 1,150 tokens of its own to every call
(reminders such as the working directory and the date); the model runs from WORKDIR.
Everything an agent does beyond that is in this file: it pastes the whole context into every
call, reads the tool request out of the reply, runs it itself, and appends the result. The tools
are plain Python functions confined to WORKDIR; run_tests runs one fixed command.

AGENT_MODEL, when set, is passed to the command-line tool's --model option (used once, to rerun
no_tests with a more capable model; the default model made every other run).

Variants (same model, same task, same project):
  bare      one call, no tools described
  one_tool  tools described, but no loop: one call, run its tool, one more call, stop
  loop      the agent: repeat until the model replies without a tool call
  no_tests  the agent without run_tests
"""
import json
import os
import re
import subprocess
import sys
import time
from pathlib import Path

TASK = "The test in test_report.py fails. Fix report.py so that the test passes."

TOOL_DOCS = {
    "list_files": '{"tool": "list_files"}  lists the files in the project',
    "read_file": '{"tool": "read_file", "path": "report.py"}  returns the file\'s text',
    "write_file": '{"tool": "write_file", "path": "report.py", "content": "..."}  replaces the file\'s text',
    "run_tests": '{"tool": "run_tests"}  runs python3 -m unittest and returns its output',
}


def system_prompt(tool_names):
    if not tool_names:
        return "You are a helpful assistant for a software engineer."
    docs = "\n".join(TOOL_DOCS[t] for t in tool_names)
    return ("You are a coding agent working on a small Python project. You cannot see or run anything "
            "yourself; you can only ask for one tool at a time. To use a tool, reply with only its JSON "
            "object on one line, and nothing else. The tools:\n" + docs + "\n"
            "The tool's output will be sent back to you. When you have finished the task, reply in plain "
            "text with no JSON.")


# --- the tools: ordinary code, run by us, never by the model ------------------------------------
class Tools:
    def __init__(self, root, names):
        self.root, self.names, self.log = Path(root).resolve(), names, []

    def _path(self, path):
        p = (self.root / path).resolve()
        if self.root not in p.parents:
            raise ValueError("path outside the project")
        return p

    def list_files(self):
        return "\n".join(sorted(p.name for p in self.root.iterdir() if p.is_file()))

    def read_file(self, path):
        return self._path(path).read_text()

    def write_file(self, path, content):
        self._path(path).write_text(content)
        return f"wrote {len(content)} characters to {path}"

    def run_tests(self):
        r = subprocess.run([sys.executable, "-m", "unittest"], cwd=self.root, capture_output=True,
                           text=True, timeout=30)
        return (r.stdout + r.stderr).replace(str(self.root) + "/", "")

    def run(self, request):
        request = dict(request)
        name = request.pop("tool")
        if name not in self.names:
            return f"error: there is no tool called {name}"
        try:
            return getattr(self, name)(**request)
        except Exception as e:  # a failed tool is still a result the model should see
            return f"error: {type(e).__name__}: {e}"


# --- the model: one call is one fresh process ----------------------------------------------------
def render(context):
    heads = {"task": "TASK", "model": "YOU WROTE", "result": "TOOL RESULT"}
    return "\n\n".join(f"{heads[role]}\n{text}" for role, text in context)


def call_model(tools, context):
    """Send the system prompt and the whole context; return the model's reply."""
    prompt = render(context)
    model = ["--model", os.environ["AGENT_MODEL"]] if os.environ.get("AGENT_MODEL") else []
    r = subprocess.run(["claude", "-p", "--tools", "", "--system-prompt", system_prompt(tools.names),
                        "--output-format", "json", "--no-session-persistence", "--safe-mode",
                        "--disable-slash-commands", "--strict-mcp-config", *model],
                       input=prompt, capture_output=True, text=True, timeout=600, cwd=tools.root)
    out = json.loads(r.stdout)
    u = out["usage"]
    tools.log.append({"call": len(tools.log) + 1, "prompt_chars": len(prompt),
                      "context_tokens": u["input_tokens"] + u["cache_creation_input_tokens"]
                      + u["cache_read_input_tokens"],
                      "output_tokens": u["output_tokens"]})
    return out["result"].strip()


def parse_tool_call(reply):
    """The first JSON object in the reply that names a tool, or None: no tool call means done."""
    for m in re.finditer(r"\{.*\}", reply, re.S):
        try:
            obj = json.loads(m.group(0))
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict) and "tool" in obj:
            return obj
    return None


# --- three versions, each built from the last ----------------------------------------------------
def bare(task, tools):
    """One call. The model can only answer with text."""
    context = [("task", task)]
    context.append(("model", call_model(tools, context)))
    return context


def one_tool(task, tools):
    """One call; if it asks for a tool, run it and call once more. No loop."""
    context = [("task", task)]
    reply = call_model(tools, context)
    context.append(("model", reply))
    request = parse_tool_call(reply)
    if request is not None:
        context.append(("result", tools.run(request)))
        context.append(("model", call_model(tools, context)))
    return context


def agent(task, tools, max_calls=20):
    context = [("task", task)]
    for _ in range(max_calls):
        reply = call_model(tools, context)
        context.append(("model", reply))
        request = parse_tool_call(reply)
        if request is None:
            return context
        context.append(("result", tools.run(request)))
    return context


ALL = ["list_files", "read_file", "write_file", "run_tests"]
VARIANTS = {
    "bare": (bare, []),
    "one_tool": (one_tool, ALL),
    "loop": (agent, ALL),
    "no_tests": (agent, ["list_files", "read_file", "write_file"]),
}


def main():
    variant, workdir, out = sys.argv[1], sys.argv[2], sys.argv[3]
    run, names = VARIANTS[variant]
    tools = Tools(workdir, names)
    t0 = time.time()
    context = run(TASK, tools)
    # Afterwards, and outside the agent: does the test really pass?
    after = Tools(workdir, ["run_tests"]).run_tests()
    record = {"variant": variant, "task": TASK, "system": system_prompt(names),
              "context": context, "calls": tools.log, "seconds": round(time.time() - t0, 1),
              "test_after": after, "passed_after": after.rstrip().endswith("OK")}
    Path(out).write_text(json.dumps(record, indent=1))
    for c in tools.log:
        print(f"call {c['call']:2d}: context {c['context_tokens']:6,d} tokens")
    for role, text in context:
        print(f"--- {role}\n{text[:600]}")
    print("TEST AFTER:", "PASS" if record["passed_after"] else "FAIL", after.strip().splitlines()[-1])


if __name__ == "__main__":
    main()
