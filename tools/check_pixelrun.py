#!/usr/bin/env python3
"""Check the Pixel Run challenge bank.

    python3 tools/check_pixelrun.py            # prove the bank (build.py does this too)
    python3 tools/check_pixelrun.py --mutate   # also break each solution and see if its tests notice

The proof is what the build runs: every solution passes its tests and rules,
every starter fails, every listed mistake fails.

--mutate goes further. It makes small changes to each reference solution (a +
becomes a -, a < becomes <=, a line is deleted, a number moves by one) and runs
the tests on every changed copy. A copy that still passes is either equivalent to
the original, such as a tie broken the other way when equal values look alike, or
a gap in the tests. The survivors are listed so a person can tell which.
"""
import ast
import collections
import copy
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from content import pixelrun  # noqa: E402
from content.pixelrun import harness, model  # noqa: E402

SWAP_BIN = {ast.Add: ast.Sub, ast.Sub: ast.Add, ast.Mult: ast.Add, ast.FloorDiv: ast.Div,
            ast.Div: ast.FloorDiv, ast.Mod: ast.FloorDiv, ast.Pow: ast.Mult}
SWAP_CMP = {ast.Lt: ast.LtE, ast.LtE: ast.Lt, ast.Gt: ast.GtE, ast.GtE: ast.Gt,
            ast.Eq: ast.NotEq, ast.NotEq: ast.Eq, ast.In: ast.NotIn, ast.NotIn: ast.In}


def mutants(src):
    tree = ast.parse(src)
    sites = []
    for i, node in enumerate(ast.walk(tree)):
        if isinstance(node, ast.BinOp) and type(node.op) in SWAP_BIN:
            sites.append(("bin", i))
        elif isinstance(node, ast.AugAssign) and type(node.op) in SWAP_BIN:
            sites.append(("aug", i))
        elif isinstance(node, ast.Compare):
            sites += [("cmp", i, k) for k, op in enumerate(node.ops) if type(op) in SWAP_CMP]
        elif isinstance(node, ast.BoolOp):
            sites.append(("bool", i))
        elif isinstance(node, ast.Constant) and type(node.value) is int:
            sites += [("const+", i), ("const-", i)]
        elif isinstance(node, (ast.Assign, ast.AugAssign, ast.Expr, ast.Return, ast.If)):
            sites.append(("del", i))
    for site in sites:
        t = copy.deepcopy(tree)
        nodes = list(ast.walk(t))
        node, kind = nodes[site[1]], site[0]
        if kind in ("bin", "aug"):
            node.op = SWAP_BIN[type(node.op)]()
        elif kind == "cmp":
            node.ops[site[2]] = SWAP_CMP[type(node.ops[site[2]])]()
        elif kind == "bool":
            node.op = ast.Or() if isinstance(node.op, ast.And) else ast.And()
        elif kind == "const+":
            node.value += 1
        elif kind == "const-":
            node.value -= 1
        elif kind == "del":
            for p in nodes:
                for field in ("body", "orelse"):
                    lst = getattr(p, field, None)
                    if isinstance(lst, list) and node in lst:
                        lst[lst.index(node)] = ast.copy_location(ast.Pass(), node)
        ast.fix_missing_locations(t)
        yield "%s@%d" % (kind, site[1]), ast.unparse(t)


def mutation_run():
    # short deadlines: a mutant that loops forever only has to be noticed
    fast = harness.HARNESS.replace("time.time() + 2", "time.time() + 0.25").replace("time.time() + 3", "time.time() + 0.5")
    ns = {}
    exec(compile(fast, "fast harness", "exec"), ns)
    total = 0
    survivors = collections.defaultdict(list)
    for ch in pixelrun.BANK:
        tests, rules = json.dumps(model.test_records(ch)), json.dumps(ch.rules)
        base = ast.unparse(ast.parse(ch.solution))
        seen = set()
        for desc, src in mutants(ch.solution):
            if src == base or src in seen:
                continue
            seen.add(src)
            total += 1
            res = json.loads(ns["__game_check"](src, ch.fn, tests, rules))
            if res["phase"] == "tests" and all(r["ok"] for r in res["results"]) and not res["rule"]:
                before, after = base.splitlines(), src.splitlines()
                diff = [(a, b) for a, b in zip(before, after) if a != b] or [("(line removed)", "")]
                survivors[ch.id].append("%-10s %s" % (desc, "  ->  ".join(x.strip() for x in diff[0])))
    killed = total - sum(len(v) for v in survivors.values())
    print("%d changed copies, %d caught by the tests, %d survived" % (total, killed, total - killed))
    for cid, lines in survivors.items():
        print("  %s" % cid)
        for line in lines:
            print("      " + line)


def main():
    n = pixelrun.validate_all()
    print("%d challenges proven: solutions pass, starters fail, every listed mistake fails" % n)
    if "--mutate" in sys.argv:
        mutation_run()


if __name__ == "__main__":
    main()
