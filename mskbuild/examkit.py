"""Short ways of writing exam questions, so a paper reads like the paper.

    tick("Which is volatile?", ["ROM", "*RAM", "Flash"])            tick one box: * marks the key
    tick("Which two ...?", ["*A", "B", "*C", "D"])                     tick two boxes, 1 mark each
    rows("Tick RAM or ROM.", ["RAM", "ROM"], [("Volatile", "RAM"), ...])   one tick per row
    ans("Convert 1011 to denary.", "11", numeric=True)                 one answer box
    table("Complete the truth table.", ["A", "B", "Q"], [["0", "0", "=0"], ...])
                                                                       cells starting = are boxes
    calc("Calculate ...", "5000", 3, [("method", ["phrases"])], unit="bytes")
                                                                       answer box plus working
    write("Explain ...", 4, [("mark point", ["phrases"]), ...], "model answer")
    prog("Write a program ...", starter, solution, [("mark point", "check expr"), ...])
    sql("Write an SQL query ...", db(("Pupil", ["Name TEXT", ...], rows)), solution, checks)

Every helper passes extra keyword arguments (label, lead, section, figure,
command, model) straight through to EQ.
"""
from .models import EQ, MP, Blank, Check, CodeTask


def _mp(points):
    return [p if isinstance(p, MP) else MP(p[0], list(p[1])) for p in points]


def tick(stem, options, model="", **kw):
    """Tick box question. Options starting with * are the correct ones."""
    correct = [i for i, o in enumerate(options) if o.startswith("*")]
    clean = [o[1:] if o.startswith("*") else o for o in options]
    return EQ(stem, len(correct), [], model, kind="choice", options=clean, correct=correct, **kw)


def rows(stem, cols, pairs, marks=None, model="", **kw):
    """One tick per row. pairs are (row text, the column it belongs in)."""
    correct = [cols.index(c) for _, c in pairs]
    return EQ(stem, marks or len(pairs), [], model, kind="matrix", rows=[r for r, _ in pairs],
              cols=list(cols), correct=correct, **kw)


def _blank(spec, numeric=False, unit="", width=8, label="", tol=0.0):
    accept = [spec] if isinstance(spec, str) else list(spec)
    return Blank(accept=accept, numeric=numeric, unit=unit, width=width, label=label, tol=tol)


def ans(stem, accept, numeric=False, unit="", model="", width=8, label_box="", tol=0.0, **kw):
    """One answer box, worth one mark. A calculation worth more is calc()."""
    b = _blank(accept, numeric, unit, width, label_box, tol)
    return EQ(stem, 1, [], model, kind="blanks", blanks=[b], **kw)


def boxes(stem, specs, model="", groups=None, numeric=False, **kw):
    """Several labelled answer boxes. specs are (label, accepted answers[, unit]) tuples."""
    blanks = []
    for sp in specs:
        label, accept = sp[0], sp[1]
        unit = sp[2] if len(sp) > 2 else ""
        blanks.append(_blank(accept, numeric, unit, 10, label))
    g = groups or []
    marks = len(g) if g else len(blanks)
    return EQ(stem, marks, [], model, kind="blanks", blanks=blanks, groups=g, **kw)


def table(stem, head, grid, model="", per_row=False, groups=None, numeric=False, width=6, **kw):
    """A table with answer boxes. A cell written "=answer" (or "=a|b" for
    alternatives) is a box. Each box is a mark, or each row with per_row."""
    blanks, out_rows, row_groups = [], [], []
    for r, row in enumerate(grid):
        cells, mine = [], []
        for cell in row:
            if isinstance(cell, str) and cell.startswith("="):
                blanks.append(_blank(cell[1:].split("|"), numeric, "", width))
                cells.append(len(blanks) - 1)
                mine.append(len(blanks) - 1)
            else:
                cells.append(cell)
        out_rows.append(cells)
        if mine:
            row_groups.append(mine)
    if groups is not None:
        g = groups
    elif per_row:
        g = [("Row %d" % (k + 1), nums) for k, nums in enumerate(row_groups)]
    else:
        g = []
    marks = len(g) if g else len(blanks)
    return EQ(stem, marks, [], model, kind="blanks", blanks=blanks, grid=out_rows, grid_head=list(head),
              groups=g, **kw)


def calc(stem, accept, marks, method, model="", unit="", numeric=True, tol=0.0, **kw):
    """A calculation: the right final answer earns every mark; otherwise the
    method points found in the working earn up to marks - 1."""
    b = _blank(accept, numeric, unit, 12, "Answer", tol)
    return EQ(stem, marks, _mp(method), model, kind="blanks", blanks=[b], groups=[("", [0])],
              working=True, **kw)


def write(stem, marks, points, model, **kw):
    """A written answer, marked against mark points."""
    return EQ(stem, marks, _mp(points), model, **kw)


def prog(stem, starter, solution, checks, model="", wrong=(), files=None, filename="answer.py", **kw):
    """A program to write or amend, marked by running it. checks are
    (mark scheme line, check expression) pairs, one mark each."""
    task = CodeTask(starter=starter, solution=solution, checks=[Check(t, e) for t, e in checks],
                    wrong=list(wrong), files=dict(files or {}), filename=filename)
    return EQ(stem, len(checks), [], model, kind="code", code=task, **kw)


def _sqlval(v):
    if v is None:
        return "NULL"
    if isinstance(v, bool):
        return "TRUE" if v else "FALSE"
    if isinstance(v, (int, float)):
        return repr(v)
    return "'%s'" % str(v).replace("'", "''")


def _cell(v, kind):
    if isinstance(v, bool):
        return "True" if v else "False"
    if kind == "REAL" and isinstance(v, (int, float)):
        return "%.2f" % v
    return str(v)


def db(*tables):
    """Tables for SQL questions, each (name, ["Column TYPE", ...], rows).

    Returns (setup script, figure). The script builds the database an answer
    runs against and the figure prints the same tables, so the two always
    agree. Text compares without regard to case, as an examiner would read it."""
    script, figs = [], []
    for name, columns, data in tables:
        kinds = [c.split()[1].upper() for c in columns]
        defs = [c + " COLLATE NOCASE" if k == "TEXT" else c for c, k in zip(columns, kinds)]
        script.append("CREATE TABLE %s (%s);" % (name, ", ".join(defs)))
        for r in data:
            script.append("INSERT INTO %s VALUES (%s);" % (name, ", ".join(_sqlval(v) for v in r)))
        heads = [c.split()[0] for c in columns]
        fig = ["**%s**" % name, "", "| " + " | ".join(heads) + " |", "|" + "---|" * len(heads)]
        fig += ["| " + " | ".join(_cell(v, k) for v, k in zip(r, kinds)) + " |" for r in data]
        figs.append("\n".join(fig))
    return "\n".join(script), "\n\n".join(figs)


def sql(stem, database, solution, checks, model="", wrong=(), starter="", filename="query.sql", **kw):
    """One SQL statement to write, marked by running it against the database
    db() made. checks are (mark scheme line, check expression) pairs."""
    setup, figure = database
    kw.setdefault("figure", figure)
    task = CodeTask(starter=starter, solution=solution, checks=[Check(t, e) for t, e in checks],
                    wrong=list(wrong), filename=filename, lang="sql", setup=setup)
    return EQ(stem, len(checks), [], model, kind="code", code=task, **kw)
