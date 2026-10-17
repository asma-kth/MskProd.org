"""Mark a student's Python program against the checks of one exam question.

This one file runs in two places. In the browser, under Pyodide, it marks what a
student typed into a programming question. In the build, under CPython, it marks
every question's model solution, which must score full marks, and the starter
code and listed wrong answers, which must not. Because the same code does both,
a mark the build has proved is exactly the mark a student will be given.

A check is a Python expression worth one mark, evaluated with these names:

    run(inputs, files)   run the whole program, typing each input as one line;
                         returns everything it printed (raises if it crashed)
    ns(inputs, files)    the program's global names after it has run
    call(name, *args)    call one of the program's functions; returns its value
    printed(name, *args) call a function and return what it printed
    after(name, *args)   call a function, then return its arguments, to see what
                         it changed in place (a list it was meant to update)
    read(name, inputs, files)  run the program, then return a file it wrote
    test(code)           run a few lines of test code after the program, such as
                         making an object and calling its methods; returns the
                         value the test code puts in a variable called result
    has(text, *parts)    every part appears in the text (case and spacing ignored)
    nums(text)           the numbers in a piece of text, as floats
    lines(text)          the non-blank lines of a piece of text
    src                  the program's source, with comments removed
    uses(*patterns)      the source matches any of these regular expressions
    count(kind)          how many AST nodes of a kind, eg count("For")
    defines(name)        the program defines a function of that name
    params(name)         the parameter names of that function

An SQL question is marked the same way, but its student answer is one SQL
statement, run against a fresh copy of the question's database. Its checks see:

    rows()               the rows the student's query returns (raises if it fails)
    cols()               the column names of that result, in lower case
    q(sql)               the rows of any query, on the database before the statement
    qa(sql)              the rows of any query, after the student's statement has run
    fields(), tables()   the names in the SELECT and FROM clauses, in lower case
    where(), order()     the text of the WHERE and ORDER BY clauses
    same_where(tables, clause)   the student's WHERE picks exactly the rows the
                         model clause picks, so any equivalent condition passes
    same_order(tables, order, where="")   the student's ORDER BY gives the same order
    same_rows(sql, ordered=False)   the student's result equals the model query's
    src, uses(*patterns) the statement without comments; a case-blind regex search
"""
import ast
import contextlib
import io
import json
import os
import re
import shutil
import sys
import tempfile
import time
import tokenize

LIMIT = 2.0        # seconds for one run of the student's program


class Timeout(Exception):
    pass


def _guarded(fn, limit=LIMIT):
    deadline = time.time() + limit

    def guard(frame, event, arg):
        # Opcode events as well as line events: a loop written on one line,
        # such as while True: pass, never starts a new line.
        frame.f_trace_opcodes = True
        if time.time() > deadline:
            raise Timeout("it ran for more than %g seconds, so it probably has a loop that never ends" % limit)
        return guard
    old = sys.gettrace()
    sys.settrace(guard)
    try:
        return fn()
    finally:
        sys.settrace(old)


def _strip_comments(src):
    try:
        toks = [t for t in tokenize.generate_tokens(io.StringIO(src).readline) if t.type != tokenize.COMMENT]
        return tokenize.untokenize(toks)
    except (tokenize.TokenError, IndentationError, SyntaxError):
        return re.sub(r"#[^\n]*", "", src)


def norm(text):
    return " ".join(str(text).lower().split())


def has(text, *parts):
    t = norm(text)
    return all(norm(p) in t for p in parts)


def nums(text):
    return [float(x) for x in re.findall(r"-?\d+(?:\.\d+)?", str(text))]


def lines(text):
    return [ln.strip() for ln in str(text).splitlines() if ln.strip()]


class Program:
    """One student program, run as many times as the checks need."""

    def __init__(self, source, files=None):
        self.source = source
        self.files = dict(files or {})
        self._runs = {}
        self.tree = ast.parse(source)

    def _key(self, inputs, files):
        merged = dict(self.files)
        merged.update(files or {})
        return tuple(str(v) for v in inputs), tuple(sorted(merged.items())), merged

    def _exec(self, inputs=(), files=None):
        ins, fkey, merged = self._key(inputs, files)
        key = (ins, fkey)
        if key in self._runs:
            return self._runs[key]
        queue = list(ins)

        def _input(prompt=""):
            if not queue:
                raise EOFError("the program asked for more input than this test types in")
            return queue.pop(0)
        g = {"__name__": "__main__", "input": _input}
        here = os.getcwd()
        work = tempfile.mkdtemp()
        buf = io.StringIO()
        err = None
        try:
            os.chdir(work)
            for name, text in merged.items():
                with open(name, "w") as fh:
                    fh.write(text)
            code = compile(self.source, "answer.py", "exec")
            with contextlib.redirect_stdout(buf):
                try:
                    _guarded(lambda: exec(code, g))
                except SystemExit:
                    pass
            written = {}
            for name in os.listdir(work):
                path = os.path.join(work, name)
                if os.path.isfile(path):
                    with open(path) as fh:
                        written[name] = fh.read()
        except BaseException as e:      # a crash, a timeout, too little input
            err = e
            written = {}
        finally:
            os.chdir(here)
            shutil.rmtree(work, ignore_errors=True)
        self._runs[key] = (buf.getvalue(), g, err, written)
        return self._runs[key]

    def run(self, inputs=(), files=None):
        out, g, err, written = self._exec(inputs, files)
        if err is not None:
            raise err
        return out

    def ns(self, inputs=(), files=None):
        out, g, err, written = self._exec(inputs, files)
        if err is not None:
            raise err
        return g

    def read(self, name, inputs=(), files=None):
        out, g, err, written = self._exec(inputs, files)
        if err is not None:
            raise err
        return written[name]

    def call(self, name, *args):
        fn = self.ns()[name]
        with contextlib.redirect_stdout(io.StringIO()):
            return _guarded(lambda: fn(*args))

    def after(self, name, *args):
        """Call a function, then return its arguments, to see what it changed in place."""
        self.call(name, *args)
        return args

    def test(self, code):
        """Run test code in a copy of the program's namespace; return its result."""
        g = dict(self.ns())
        with contextlib.redirect_stdout(io.StringIO()):
            _guarded(lambda: exec(code, g))
        return g.get("result")

    def printed(self, name, *args):
        fn = self.ns()[name]
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            _guarded(lambda: fn(*args))
        return buf.getvalue()


def _env(p):
    src = _strip_comments(p.source)
    funcs = {n.name: n for n in ast.walk(p.tree) if isinstance(n, ast.FunctionDef)}
    return {
        "run": p.run, "ns": p.ns, "call": p.call, "printed": p.printed, "read": p.read, "after": p.after, "test": p.test,
        "has": has, "nums": nums, "lines": lines, "norm": norm,
        "src": src,
        "uses": lambda *pats: any(re.search(pt, src) for pt in pats),
        "count": lambda kind: sum(1 for n in ast.walk(p.tree) if type(n).__name__ == kind),
        "defines": lambda name: name in funcs,
        "params": lambda name: [a.arg for a in funcs[name].args.args] if name in funcs else [],
        "len": len, "sorted": sorted, "sum": sum, "abs": abs, "round": round, "any": any, "all": all,
        "int": int, "float": float, "str": str, "list": list, "set": set, "isinstance": isinstance,
    }


def _explain(e):
    if isinstance(e, Timeout):
        return str(e)
    if isinstance(e, EOFError):
        return "the program asked for more input than the test types in"
    if isinstance(e, KeyError):
        return "it does not define %s" % e
    return "%s: %s" % (type(e).__name__, e)


# ------------------------------------------------------------------ SQL

_SELECT = re.compile(r"^\s*select\s+(?P<select>.+?)\s+from\s+(?P<from>.+?)"
                     r"(?:\s+where\s+(?P<where>.+?))?(?:\s+order\s+by\s+(?P<order>.+?))?\s*$", re.I | re.S)


def _clean_sql(source):
    text = re.sub(r"/\*.*?\*/", " ", source, flags=re.S)
    text = re.sub(r"--[^\n]*", "", text)
    return text.strip().rstrip(";").strip()


def _connect(setup):
    import sqlite3
    con = sqlite3.connect(":memory:")
    con.executescript(setup)
    return con


def _key(rows):
    return sorted(repr(r) for r in rows)


class Query:
    """One student SQL statement, run against a fresh copy of the question's database."""

    def __init__(self, source, setup):
        self.setup = setup
        self.src = _clean_sql(source)
        self._done = None

    def _run(self):
        if self._done is None:
            con = _connect(self.setup)
            try:
                if not self.src:
                    raise ValueError("there is no SQL statement to run")
                cur = con.execute(self.src)
                rows = [tuple(r) for r in cur.fetchall()]
                cols = [d[0].lower() for d in cur.description] if cur.description else []
                self._done = (con, rows, cols, None)
            except Exception as e:
                self._done = (con, [], [], e)
        return self._done

    def ran(self):
        return self._run()[3] is None

    def rows(self):
        con, rows, cols, err = self._run()
        if err is not None:
            raise err
        return rows

    def cols(self):
        self.rows()
        return self._run()[2]

    def q(self, sql):
        return [tuple(r) for r in _connect(self.setup).execute(sql).fetchall()]

    def qa(self, sql):
        self.rows()
        return [tuple(r) for r in self._run()[0].execute(sql).fetchall()]

    def parts(self):
        m = _SELECT.match(self.src)
        return {k: ((m.group(k) or "").strip() if m else "") for k in ("select", "from", "where", "order")}

    def fields(self):
        sel = self.parts()["select"]
        return [re.sub(r"^\w+\.", "", f.strip().lower()) for f in sel.split(",")] if sel else []

    def tables(self):
        frm = re.sub(r"\bon\b.+?(?=\b(?:inner\s+|left\s+|right\s+|outer\s+)*join\b|$)", " ", self.parts()["from"], flags=re.I | re.S)
        pieces = re.split(r",|\b(?:inner\s+|left\s+|right\s+|outer\s+)*join\b", frm, flags=re.I)
        return [p.split()[0].lower() for p in pieces if p.split()]

    def same_where(self, tables, clause):
        mine = self.parts()["where"]
        if not mine:
            return False
        base = "SELECT * FROM %s WHERE " % tables
        return _key(self.q(base + mine)) == _key(self.q(base + clause))

    def same_order(self, tables, order, where=""):
        mine = self.parts()["order"]
        if not mine:
            return False
        base = "SELECT * FROM %s%s ORDER BY " % (tables, " WHERE " + where if where else "")
        return self.q(base + mine) == self.q(base + order)

    def same_rows(self, sql, ordered=False):
        mine, want = self.rows(), self.q(sql)
        return mine == want if ordered else _key(mine) == _key(want)


def _sql_env(qy):
    return {
        "rows": qy.rows, "cols": qy.cols, "q": qy.q, "qa": qy.qa, "ran": qy.ran,
        "fields": qy.fields, "tables": qy.tables,
        "where": lambda: qy.parts()["where"], "order": lambda: qy.parts()["order"],
        "same_where": qy.same_where, "same_order": qy.same_order, "same_rows": qy.same_rows,
        "src": qy.src, "uses": lambda *pats: any(re.search(pt, qy.src, re.I) for pt in pats),
        "has": has, "norm": norm, "len": len, "sorted": sorted, "set": set, "any": any, "all": all,
    }


def preview(source, setup):
    """What the Run button shows for an SQL answer: the result, as a table."""
    qy = Query(source, setup)
    try:
        rows, cols = qy.rows(), qy.cols()
    except Exception as e:
        return {"output": "", "error": "Your SQL could not run: %s" % e}
    if not cols:
        m = re.match(r"\s*(?:insert\s+into|update|delete\s+from)\s+(\w+)", qy.src, re.I)
        if not m:
            return {"output": "The statement ran.", "error": ""}
        cur = qy._run()[0].execute("SELECT * FROM %s" % m.group(1))
        cols, rows = [d[0] for d in cur.description], [tuple(r) for r in cur.fetchall()]
        head = "The statement ran. %s now holds:\n\n" % m.group(1)
    else:
        head = "%d row%s returned:\n\n" % (len(rows), "" if len(rows) == 1 else "s")
    cells = [[str(c) for c in cols]] + [["" if v is None else str(v) for v in r] for r in rows]
    width = [max(len(r[k]) for r in cells) for k in range(len(cols))]
    out = ["  ".join(v.ljust(width[k]) for k, v in enumerate(r)).rstrip() for r in cells]
    out.insert(1, "  ".join("-" * w for w in width))
    return {"output": head + "\n".join(out), "error": ""}


def preview_json(source, setup):
    return json.dumps(preview(source, setup))


def _explain_sql(e):
    if isinstance(e, ValueError):
        return str(e)
    return "your SQL could not run: %s" % e


def mark(source, checks, files=None, lang="python", setup=""):
    """Mark one program. Returns [[passed, message], ...], one per check."""
    if lang == "sql":
        env = _sql_env(Query(source, setup))
        explain = _explain_sql
    else:
        try:
            p = Program(source, files)
        except SyntaxError as e:
            why = "your code has a syntax error on line %s, so it cannot run: %s" % (e.lineno, e.msg)
            return [[False, why] for _ in checks]
        env = _env(p)
        explain = _explain
    # One namespace, not separate globals and locals: a comprehension in a
    # check runs in its own scope and can only see the globals.
    env["__builtins__"] = __builtins__
    out = []
    for expr in checks:
        try:
            ok = bool(eval(expr, env))
            out.append([ok, ""])
        except BaseException as e:      # a check fails if the program crashes on it
            out.append([False, explain(e)])
    return out


def mark_json(source, checks_json, files_json="{}", lang="python", setup=""):
    """The browser's entry point: JSON in, JSON out."""
    return json.dumps(mark(source, json.loads(checks_json), json.loads(files_json), lang, setup))
