#!/usr/bin/env python3
"""Prove that every Python example in the course actually runs.

Every Python code block on the site gets a Run button, and the course promises
that "every example runs". That is easy to promise and easy to break: one
renamed variable in prose, one example that leans on the block above it (each
Run starts from a clean slate), and a student presses Run and sees a
NameError on a page that is teaching them to read error messages.

    python3 tools/check_python_examples.py            # new GCSE and A Level topics, CPython
    python3 tools/check_python_examples.py --all      # every topic in the course
    python3 tools/check_python_examples.py --pyodide  # also run in the real browser engine
    python3 tools/check_python_examples.py --show     # print what every block outputs

--pyodide runs each block in the same Pyodide build the site loads, under Node,
and compares its output with CPython's. It needs `npm install pyodide@<version>`
somewhere and PYODIDE_DIR pointing at node_modules/pyodide. It is the check that
matters most, because it is what a student actually sees.

Conventions the content follows, and this tool enforces:

  * Every block is self contained. Nothing may depend on an earlier block.
  * Examples are deterministic. Where a program has to call input(), its topic
    module lists the answers to type in an INPUTS dict, keyed by the block's
    position ("#3", "exam 2 model"), so the page stays free of test scaffolding.
    An EXPECT dict, keyed the same way, names the error a block must fail with,
    for the cases (an exam figure to debug) where a visible marker would give
    the answer away.
  * A block that is meant to fail starts with `# raises: ErrorName` and must
    fail with exactly that error.
  * A block whose output legitimately varies (random numbers, timings) starts
    with `# varies` and is only checked for not crashing.
  * A `pylocal` block is Python the browser cannot run (threads, sockets,
    asyncio). It gets no Run button, so it is only compiled here, to catch typos.
"""
import json
import os
import re
import subprocess
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

NEW_MODULES = ["content.python_gcse", "content.python_alevel", "content.python_advanced"]


def blocks_of(body, wanted="python"):
    """Yield every fenced block of one language in a section body."""
    lines = body.split("\n")
    i = 0
    while i < len(lines):
        m = re.match(r"^```(\w+)\s*$", lines[i])
        if m:
            lang, buf = m.group(1), []
            i += 1
            while i < len(lines) and not lines[i].startswith("```"):
                buf.append(lines[i])
                i += 1
            if lang == wanted:
                yield "\n".join(buf)
        i += 1


def collect(everything, wanted="python"):
    import importlib
    out = []
    if everything:
        course = importlib.import_module("content.python_course").COURSE
        topics = [t for u in course.units for t in u.topics]
    else:
        topics = []
        for name in NEW_MODULES:
            try:
                mod = importlib.import_module(name)
            except ImportError:
                continue
            topics += list(getattr(mod, "TOPICS", []))
    feeds, expects = {}, {}
    for name in ([] if everything else NEW_MODULES):
        try:
            mod = importlib.import_module(name)
        except ImportError:
            continue
        feeds.update(getattr(mod, "INPUTS", {}))
        expects.update(getattr(mod, "EXPECT", {}))
    for t in topics:
        n = 0
        for s in t.sections:
            for code in blocks_of(s.body, wanted):
                n += 1
                key = "#%d" % n
                out.append({"id": "%s %s (%s)" % (t.slug, key, s.title[:28]), "code": code,
                            "feed": feeds.get(t.slug, {}).get(key),
                            "raises": expects.get(t.slug, {}).get(key)})
        # Model answers are programs too, and a model answer that does not run
        # is worse than none. Exam figures are set code to trace or to fix, so
        # only the ones marked as Python (not pseudocode) are run.
        for k, q in enumerate(t.exam):
            for what, text in (("model", q.model), ("figure", q.figure)):
                key = "exam %d %s" % (k + 1, what)
                for code in blocks_of(text, wanted):
                    out.append({"id": "%s %s" % (t.slug, key), "code": code,
                                "feed": feeds.get(t.slug, {}).get(key),
                                "raises": expects.get(t.slug, {}).get(key)})
    return out


def expectation(code, declared=None):
    if declared:
        return declared, False
    for line in code.split("\n"):
        if not line.strip():
            continue
        m = re.match(r"#\s*raises:\s*(\w+)", line)
        varies = bool(re.match(r"#\s*varies", line))
        return (m.group(1) if m else None), varies
    return None, False


def with_feed(code, feed):
    """Put a scripted keyboard in front of the program, as the Run button does."""
    return ("_feed = iter(%r)\n"
            "def input(prompt=''):\n"
            "    try:\n"
            "        return next(_feed)\n"
            "    except StopIteration:\n"
            "        raise EOFError('EOF when reading a line')\n" % (list(feed or []),)) + code


def run_cpython(code, feed=None):
    code = with_feed(code, feed)
    with tempfile.TemporaryDirectory() as tmp:
        try:
            r = subprocess.run([sys.executable, "-I", "-c", code], cwd=tmp, capture_output=True,
                               text=True, timeout=15, stdin=subprocess.DEVNULL)
        except subprocess.TimeoutExpired:
            return {"ok": False, "out": "", "err": "TimeoutError: ran for more than 15 seconds"}
    err = r.stderr.strip().split("\n")[-1] if r.returncode else ""
    return {"ok": r.returncode == 0, "out": r.stdout, "err": err}


def run_pyodide(blocks):
    pyo = os.environ.get("PYODIDE_DIR")
    if not pyo or not os.path.isdir(pyo):
        sys.exit("--pyodide needs PYODIDE_DIR=<path to node_modules/pyodide>")
    runner = os.path.join(os.path.dirname(os.path.abspath(__file__)), "pyodide_blocks.mjs")
    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as fh:
        json.dump(blocks, fh)
        path = fh.name
    r = subprocess.run(["node", runner, os.path.join(pyo, "pyodide.mjs"), path],
                       capture_output=True, text=True, timeout=900, stdin=subprocess.DEVNULL)
    os.unlink(path)
    if r.returncode:
        sys.exit("pyodide runner failed:\n" + r.stderr[-1500:])
    return json.loads(r.stdout)


def main():
    use_pyodide = "--pyodide" in sys.argv
    blocks = collect("--all" in sys.argv)
    if not blocks:
        sys.exit("no Python blocks found")
    problems = []
    local = collect("--all" in sys.argv, "pylocal")
    for b in local:
        try:
            compile(b["code"], b["id"], "exec")
        except SyntaxError as e:
            problems.append("%s: does not compile (%s, line %s)" % (b["id"], e.msg, e.lineno))
    results = {}
    for b in blocks:
        raises, varies = expectation(b["code"], b.get("raises"))
        r = run_cpython(b["code"], b.get("feed"))
        results[b["id"]] = r
        if raises:
            if r["ok"]:
                problems.append("%s: expected %s but it ran cleanly" % (b["id"], raises))
            elif not r["err"].startswith(raises):
                problems.append("%s: expected %s, got %s" % (b["id"], raises, r["err"][:80]))
        elif not r["ok"]:
            problems.append("%s: %s" % (b["id"], r["err"][:120]))

    mismatches = 0
    if use_pyodide:
        py = {r["id"]: r for r in run_pyodide(blocks)}
        for b in blocks:
            raises, varies = expectation(b["code"], b.get("raises"))
            a, p = results[b["id"]], py[b["id"]]
            if raises:
                if p["ok"] or not p["err"].startswith(raises):
                    problems.append("%s [pyodide]: expected %s, got %r" % (b["id"], raises, p["err"][:80]))
            elif not p["ok"]:
                problems.append("%s [pyodide]: %s" % (b["id"], p["err"][:120]))
            elif not varies and a["ok"] and a["out"].strip() != p["out"].strip():
                mismatches += 1
                problems.append("%s: CPython and Pyodide disagree\n      cpython : %r\n      pyodide : %r"
                                % (b["id"], a["out"].strip()[:90], p["out"].strip()[:90]))

    if "--show" in sys.argv:
        for b in blocks:
            r = results[b["id"]]
            print("--- %s" % b["id"])
            print((r["out"] or r["err"]).rstrip())
    ran = len(blocks)
    expected_fail = sum(1 for b in blocks if expectation(b["code"], b.get("raises"))[0])
    print("%d Python blocks%s: %d ran cleanly, %d fail on purpose, %d on-your-computer blocks compile, %d problems"
          % (ran, " under CPython and Pyodide" if use_pyodide else " under CPython",
             ran - expected_fail, expected_fail, len(local), len(problems)))
    for p in problems[:40]:
        print("  -", p)
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
