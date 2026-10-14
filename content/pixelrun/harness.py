"""The marker for the Python game, written once and run in two places.

HARNESS is a string of Python. The build runs it under CPython to prove that
every challenge's solution passes and every listed mistake fails, and the
browser runs the same string under Pyodide to mark a student's code. One
source means the build cannot approve a challenge that the page then marks
differently.

The student's code is only ever run inside their own browser tab, against
tests that arrive with the page. Nothing is sent anywhere.
"""

HARNESS = r'''
import ast, copy, json, sys, time

def __game_same(got, expected):
    # True is not 1, and a list is not a tuple, but 2 and 2.0 are the same answer,
    # and a Counter or a defaultdict is a perfectly good dict
    if isinstance(expected, bool) or isinstance(got, bool):
        return isinstance(got, type(expected)) and got == expected
    if isinstance(expected, (int, float)):
        return isinstance(got, (int, float)) and abs(got - expected) <= 1e-9 * max(1, abs(expected))
    return isinstance(got, type(expected)) and got == expected

class __GameCounted(list):
    """A list that counts how many of its items the student's code looks at."""
    def __init__(self, items):
        list.__init__(self, items)
        self.probes = 0
    def __getitem__(self, i):
        self.probes += 1
        return list.__getitem__(self, i)
    def __iter__(self):
        for x in list.__iter__(self):
            self.probes += 1
            yield x
    def __contains__(self, x):
        self.probes += len(self)
        return list.__contains__(self, x)

def __game_args(text):
    try:
        return ast.literal_eval(text)
    except (ValueError, SyntaxError):
        # a long list written as list(range(...)); this text is the game's own
        return eval(text, {"__builtins__": {}, "list": list, "range": range})

def __game_rules(tree, fn, rules):
    func = None
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef) and node.name == fn:
            func = node
            break
    if func is None:
        return ""
    for rule in rules:
        kind = rule["kind"]
        if kind == "recursive":
            if not any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == fn
                       for n in ast.walk(func)):
                return rule["why"]
        elif kind == "calls":
            if not any(isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == rule["name"]
                       for n in ast.walk(func)):
                return rule["why"]
        elif kind == "loop":
            if not any(isinstance(n, (ast.For, ast.While, ast.comprehension)) for n in ast.walk(func)):
                return rule["why"]
        elif kind == "forbid":
            names = set(rule["names"])
            for n in ast.walk(func):
                if isinstance(n, ast.Call):
                    f = n.func
                    if isinstance(f, ast.Name) and f.id in names:
                        return rule["why"]
                    if isinstance(f, ast.Attribute) and f.attr in names:
                        return rule["why"]
                if "**" in names and isinstance(n, ast.BinOp) and isinstance(n.op, ast.Pow):
                    return rule["why"]
                if "in" in names and isinstance(n, ast.Compare) \
                        and any(isinstance(o, (ast.In, ast.NotIn)) for o in n.ops):
                    return rule["why"]
                if "[::-1]" in names and isinstance(n, ast.Subscript):
                    sl = n.slice
                    if isinstance(sl, ast.Slice) and isinstance(sl.step, ast.UnaryOp) \
                            and isinstance(sl.step.op, ast.USub):
                        return rule["why"]
    return ""

def __game_check(src, fn, tests_json, rules_json):
    tests = json.loads(tests_json)
    rules = json.loads(rules_json)
    try:
        tree = ast.parse(src)
    except SyntaxError as e:
        return json.dumps({"phase": "syntax", "message": "SyntaxError: %s (line %s)" % (e.msg, e.lineno)})
    except Exception as e:
        return json.dumps({"phase": "syntax", "message": "%s: %s" % (type(e).__name__, e)})
    state = {"deadline": 0}
    def guard(frame, event, arg):
        if time.time() > state["deadline"]:
            raise TimeoutError("this took too long. Is there a loop that never ends?")
        return guard
    def no_input(prompt=""):
        raise EOFError("input() cannot be used here. The function gets its values as parameters.")
    g = {"__name__": "__main__", "input": no_input}
    state["deadline"] = time.time() + 3
    sys.settrace(guard)
    try:
        exec(compile(tree, "your code", "exec"), g)
    except BaseException as e:
        return json.dumps({"phase": "load", "message": "%s: %s" % (type(e).__name__, e)})
    finally:
        sys.settrace(None)
    f = g.get(fn)
    if not callable(f):
        return json.dumps({"phase": "missing",
                           "message": "Your code needs to define a function called %s." % fn})
    results = []
    probe_rule = None
    probe_fail = ""
    for rule in rules:
        if rule["kind"] == "probes":
            probe_rule = rule
    for t in tests:
        args = __game_args(t["a"])
        expected = ast.literal_eval(t["e"])
        state["deadline"] = time.time() + 2
        got, err = None, None
        call_args = list(copy.deepcopy(args))
        counted = None
        if probe_rule is not None and isinstance(call_args[probe_rule["arg"]], list):
            counted = __GameCounted(call_args[probe_rule["arg"]])
            call_args[probe_rule["arg"]] = counted
        sys.settrace(guard)
        try:
            got = f(*call_args)
        except BaseException as e:
            err = "%s: %s" % (type(e).__name__, e)
        finally:
            sys.settrace(None)
        if counted is not None and not probe_fail:
            limit = probe_rule["per_log2"] * (len(counted) + 1).bit_length() + probe_rule["plus"]
            if counted.probes > limit:
                probe_fail = probe_rule["why"]
        ok = err is None and __game_same(got, expected)
        shown = err if err is not None else repr(got)
        results.append({"call": t["c"], "expected": t["e"], "got": shown[:160], "ok": ok,
                        "err": err is not None})
        if err is not None and err.startswith("TimeoutError"):
            for rest in tests[len(results):]:
                results.append({"call": rest["c"], "expected": rest["e"],
                                "got": "not run, because an earlier test timed out", "ok": False, "err": True})
            break
    return json.dumps({"phase": "tests", "results": results,
                       "rule": __game_rules(tree, fn, rules) or probe_fail})
'''


def load():
    """Execute HARNESS and return its namespace, for the build to use."""
    ns = {}
    exec(compile(HARNESS, "game harness", "exec"), ns)
    return ns
