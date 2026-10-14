"""What a challenge is, and the proof that each one is sound.

A challenge is a function for the student to write. It ships with the page as
a signature to fill in, the tests it will be marked against and two hints. It
does not ship with its solution until the student has used up their attempts.

validate() is what makes a bank of fifty of these trustworthy, and runs on
every build:

* the reference solution has to pass every test, and obey the challenge's rules
* the starter code has to FAIL, or the obstacle is already open
* every listed mistake has to fail, by a test or by a rule. A test suite that a
  plausible wrong answer slips through is not a test, and the student would be
  told they were right when they were not
* every expected value is computed by running the solution, never typed in, so
  the tests cannot disagree with the solution that defines them
"""
import ast
import copy
import json
from dataclasses import dataclass, field

from . import harness


@dataclass
class Level:
    n: int
    name: str
    concept: str
    stage: str                    # GCSE or A Level, for the progression label
    blurb: str
    palette: str                  # which colours the canvas uses
    obstacles: list               # three kinds, one per challenge
    revise: list                  # (label, url) pairs on this site


@dataclass
class Challenge:
    id: str
    level: int
    title: str
    story: str
    task: str
    fn: str
    starter: str
    solution: str
    tests: list                   # argument tuples; the first two double as examples
    wrong: list                   # source strings of plausible mistakes
    hints: list
    rules: list = field(default_factory=list)


# ------------------------------------------------------------------ rules

def loop(why="This one is about loops: use a for or a while inside the function."):
    return {"kind": "loop", "why": why}


def recursive(why="This level is about recursion: the function has to call itself."):
    return {"kind": "recursive", "why": why}


def forbid(names, why):
    return {"kind": "forbid", "names": list(names), "why": why}


def calls(name, why=None):
    return {"kind": "calls", "name": name,
            "why": why or "Use the %s() function that is already in the starter code." % name}


# --------------------------------------------------------------- expected

def call_text(fn, args):
    return "%s(%s)" % (fn, ", ".join(repr(a) for a in args))


def solve(ch):
    """Run the reference solution on every test, returning the expected values."""
    ns = {}
    exec(compile(ch.solution, "solution of " + ch.id, "exec"), ns)
    f = ns[ch.fn]
    return [f(*copy.deepcopy(args)) for args in ch.tests]


def test_records(ch):
    """The tests as they travel to the browser: every value as Python source."""
    out = []
    for args, expected in zip(ch.tests, solve(ch)):
        out.append({"c": call_text(ch.fn, args), "a": repr(tuple(args)), "e": repr(expected)})
    return out


# ------------------------------------------------------------------ proof

class BankError(Exception):
    pass


_H = None


def _check(ch, src, tests):
    global _H
    if _H is None:
        _H = harness.load()
    raw = _H["__game_check"](src, ch.fn, json.dumps(tests), json.dumps(ch.rules))
    return json.loads(raw)


def _passes(res):
    return res["phase"] == "tests" and all(r["ok"] for r in res["results"]) and not res["rule"]


def validate(ch):
    problems = []
    if len(ch.tests) < 4:
        problems.append("fewer than four tests")
    if len(ch.hints) < 2:
        problems.append("fewer than two hints")
    if not ch.wrong:
        problems.append("no listed mistakes, so the tests are unproven")
    try:
        tests = test_records(ch)
    except Exception as e:
        return ["the solution raised %s: %s" % (type(e).__name__, e)]
    for t in tests:
        if json.loads(json.dumps(t)) != t:
            problems.append("test record does not survive JSON")
    res = _check(ch, ch.solution, tests)
    if not _passes(res):
        why = res.get("message") or res.get("rule") or [r for r in res.get("results", []) if not r["ok"]][:1]
        problems.append("the reference solution does not pass its own tests: %s" % (why,))
    res = _check(ch, ch.starter, tests)
    if _passes(res):
        problems.append("the starter code already passes, so the obstacle opens by itself")
    for i, src in enumerate(ch.wrong):
        res = _check(ch, src, tests)
        if _passes(res):
            problems.append("listed mistake %d passes every test, so the tests cannot tell it from a right answer" % (i + 1))
    return problems


# --------------------------------------------------------------- fallback

def _perturb(expected):
    """Plausible wrong answers of the same shape, to pad a multiple choice."""
    out = []
    if isinstance(expected, bool):
        out.append(not expected)
    elif isinstance(expected, int):
        out += [expected + 1, expected - 1, expected * 2, 0]
    elif isinstance(expected, float):
        out += [round(expected + 1, 2), round(expected * 2, 2), round(expected - 1, 2)]
    elif isinstance(expected, str):
        out += [expected[::-1], expected.upper() if expected != expected.upper() else expected.lower(), expected[:-1], expected + expected[-1:]]
    elif isinstance(expected, list):
        out += [expected[::-1], expected[:-1], expected + expected[-1:], sorted(expected, key=repr)]
    elif isinstance(expected, dict):
        out += [{}, dict(list(expected.items())[:-1])]
    else:
        out += [None]
    return out


def fallback(ch, slot=0):
    """A predict-the-output question for when Python cannot be loaded.

    The distractors are what the listed mistakes really return, so a wrong
    option is a mistake a student could actually have made. Those runs go
    through the same guarded marker as everything else: some of the mistakes
    are infinite loops.
    """
    tests = test_records(ch)
    runs = [_check(ch, src, tests) for src in ch.wrong]
    best = None
    for i, t in enumerate(tests):
        wrongs = []
        for res in runs:
            if res["phase"] != "tests":
                continue
            r = res["results"][i]
            if not r["ok"] and not r["err"] and r["got"] != t["e"] and r["got"] not in wrongs:
                wrongs.append(r["got"])
        if best is None or len(wrongs) > len(best[1]):
            best = (i, wrongs)
        if len(wrongs) >= 3:
            break
    i, wrongs = best
    expected = ast.literal_eval(tests[i]["e"])
    options = [tests[i]["e"]]
    for w in wrongs + [repr(p) for p in _perturb(expected)]:
        if w not in options:
            options.append(w)
        if len(options) == 4:
            break
    while len(options) < 4:
        options.append("None" if "None" not in options else "'?'")
    # The right answer goes in the slot it is given (the caller spreads these
    # evenly over A to D), and the wrong ones fill the rest in a fixed order, so
    # a rebuild never moves anything.
    slot %= 4
    rest = options[1:]
    shuffled = rest[:slot] + [options[0]] + rest[slot:]
    return {"call": tests[i]["c"], "options": shuffled, "answer": slot}
