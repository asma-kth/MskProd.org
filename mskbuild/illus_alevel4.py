"""A Level illustrations, set four: ACID, SQL, the programming project, levels of testing and
test driven development."""
import math

from .illus import Canvas, PAL, INK, ARROW, figure, illustration, _n
from . import illus_props as P
from . import illus_glyphs as G


def wrap(text, n):
    out, cur = [], ""
    for w in text.split():
        if len(cur) + len(w) + 1 > n and cur:
            out.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    out.append(cur)
    return out


# ------------------------------------------------------------------ ACID

def account(cv, x, y, name, amount, col="sky", w=92):
    return P.lift(cv, x, y, w, 56, col, 10, 4, hl=False) + cv.text(x + w / 2, y + 22, name, 13, 800, fill=INK) + cv.text(x + w / 2, y + 44, amount, 16, 800, fill=INK, mono=True)


@illustration("acid")
def _acid():
    cv = Canvas(800, 500).backdrop()
    spec = [("Atomicity", "coral", "all or nothing"), ("Consistency", "sky", "the rules always hold"), ("Isolation", "sun", "no peeking at half-finished work"), ("Durability", "mint", "once committed, it stays")]
    for n, (title, col, rule) in enumerate(spec):
        x, y = (14, 406)[n % 2], (30, 258)[n // 2]
        cv.add(P.card(cv, x, y, 380, 214, 20, title, col), P.badge(cv, x + 22, y + 24, n + 1))
        cv.add(cv.text(x + 190, y + 206, rule, 13.5, 750, cls="il-ink"))
        if n == 0:
            cv.add(account(cv, x + 26, y + 58, "Account A", "£100"), account(cv, x + 262, y + 58, "Account B", "£0"))
            cv.add(P.arrow(cv, [(x + 126, y + 86), (x + 256, y + 86)], ARROW, 4, 12), P.pill(cv, x + 190, y + 66, "move £50", "paper", 13, 10, 24, 750))
            cv.add(P.tick(cv, x + 52, y + 140, 11), cv.text(x + 72, y + 145, "both steps done: commit", 13, 700, anchor="start", cls="il-ink"))
            cv.add(P.cross(cv, x + 52, y + 170, 11), cv.text(x + 72, y + 175, "one step fails: undo both", 13, 700, anchor="start", cls="il-ink"))
        elif n == 1:
            for k, (lab, a_, b_) in enumerate((("before", "£100", "£100"), ("after", "£50", "£150"))):
                bx = x + 30 + k * 176
                cv.add(cv.text(bx + 70, y + 56, lab, 13, 800, cls="il-ink2"))
                cv.add(account(cv, bx, y + 66, "A", a_, "sky", 66), account(cv, bx + 74, y + 66, "B", b_, "sky", 66))
                cv.add(P.pill(cv, bx + 70, y + 148, "total £200", "sun", 13.5, 12, 26, 800))
            cv.add(P.arrow(cv, [(x + 176, y + 94), (x + 204, y + 94)], ARROW, 3.5, 10))
            cv.add(cv.text(x + 190, y + 182, "no account may go below £0", 12.5, 650, cls="il-ink2"))
        elif n == 2:
            for k, (nm, col2, off) in enumerate((("Transaction 1", "sky", 0), ("Transaction 2", "coral", 1))):
                yy = y + 60 + k * 56
                cv.add(cv.text(x + 22, yy + 22, nm, 12.5, 750, anchor="start", cls="il-ink"))
                bx = x + 120 + off * 110
                cv.add(P.lift(cv, bx, yy, 150 if k == 0 else 140, 34, col2, 8, 4, hl=False), cv.text(bx + (75 if k == 0 else 70), yy + 22, "works on balance" if k == 0 else "waits, then runs", 12.5, 750, fill=INK))
            cv.add(P.padlock(cv, x + 280, y + 90, .5, "sun"))
            cv.add(cv.line(x + 120 + 150, y + 54, x + 120 + 150, y + 176, "#8AA0AC", 1.8, dash="4 5"))
            cv.add(cv.text(x + 270, y + 50, "commit", 12, 700, cls="il-ink2"))
        else:
            cv.add(G.cylinder(cv, x + 110, y + 112, 80, 90, "sky", 3), P.tick(cv, x + 140, y + 66, 13))
            bolt = [(x + 270, y + 62), (x + 244, y + 118), (x + 262, y + 118), (x + 250, y + 168), (x + 296, y + 100), (x + 274, y + 100), (x + 290, y + 62)]
            cv.add(cv.poly(bolt, "#FFC93C", stroke="#B98A12", sw=1.6))
            cv.add(cv.text(x + 270, y + 180, "power cut", 12, 700, cls="il-ink2"), cv.text(x + 110, y + 180, "still there", 12, 700, cls="il-ink2"))
    return figure(
        "acid", cv, "The four ACID properties of a database transaction: atomicity, consistency, isolation and durability",
        "The four properties that make a database transaction reliable. Atomicity means all or nothing: moving 50 pounds from account A to account "
        "B either completes both steps, which is committed, or if one step fails both are undone. Consistency means the rules always hold: before "
        "the move A and B have 100 pounds each, after it they have 50 and 150, the total is still 200 pounds, and no account goes below zero. "
        "Isolation means transactions cannot see each other's half finished work: transaction 2 waits while transaction 1 has the balance locked, "
        "then runs after it commits. Durability means that once a transaction is committed it stays, even if the power is cut.",
        ["Atomicity: a transaction is all or nothing.", "Consistency: the database goes from one valid state to another, and the rules always hold.",
         "Isolation: concurrent transactions do not see each other's half finished work.", "Durability: committed data survives a crash."],
        "Learn the four words and give the bank transfer as the example for each.")


# ------------------------------------------------------------------ SQL

def table(cv, x, y, headers, rows, widths, rh=30, tint=None, struck=()):
    out = ""
    cx = x
    for h_, w_ in zip(headers, widths):
        out += cv.rect(cx, y, w_, rh, 0, cv.g("teal"), stroke="#FFFFFF", sw=1) + cv.text(cx + w_ / 2, y + rh / 2 + 4.8, h_, 13.5, 800, fill=INK)
        cx += w_
    for r, row in enumerate(rows):
        cx = x
        bg = (tint or {}).get(r, "#FFFFFF")
        for v, w_ in zip(row, widths):
            out += cv.rect(cx, y + (r + 1) * rh, w_, rh, 0, bg, stroke="#D5DEE4", sw=1) + cv.text(cx + w_ / 2, y + (r + 1) * rh + rh / 2 + 4.8, str(v), 13.5, 650, fill=INK, mono=isinstance(v, int))
            cx += w_
        if r in struck:
            out += P.cross(cv, x + sum(widths) + 17, y + (r + 1) * rh + rh / 2, 9)
    return out


@illustration("sql-anatomy")
def _sql():
    cv = Canvas(800, 500).backdrop()
    clauses = [("SELECT name, mark", "which columns", "#FF7B72", "coral"), ("FROM results", "which table", "#FFCB47", "sun"), ("WHERE mark > 60", "which rows", "#5BD58B", "mint"), ("ORDER BY mark DESC;", "in what order", "#66B8EC", "sky")]
    cv.add(G.code(cv, 14, 30, 360, [c[0] for c in clauses], title="query.sql", size=14, numbers=False, bars={i: c[2] for i, c in enumerate(clauses)}))
    for i, (_, what, _, col) in enumerate(clauses):
        y = 30 + 28 + 12 + 14 * 1.6 * i + 14 * 1.05 - 5
        cv.add(P.pill(cv, 396, y, what, col, 12.5, 10, 20, 750, anchor="start"))
        cv.add(cv.line(374, y, 392, y, "#8AA0AC", 1.6, dash="3 4"))
    cv.add(P.badge(cv, 574, 52, 1))
    names = [(1, "Aisha", 72), (2, "Ben", 55), (3, "Chloe", 91), (4, "Dev", 64), (5, "Eli", 48)]
    rows = [(i, n_, m) for i, n_, m in names]
    cv.add(P.card(cv, 14, 196, 372, 286, 20, "The table: results", "teal"), P.badge(cv, 36, 222, 2))
    cv.add(table(cv, 42, 252, ["id", "name", "mark"], rows, [60, 140, 100], 32, tint={1: "#FDE7E4", 4: "#FDE7E4"}, struck=(1, 4)))
    cv.add(cv.text(200, 468, "WHERE mark > 60 keeps 3 rows and drops 2", 13.5, 750, cls="il-ink"))
    cv.add(P.arrow(cv, [(392, 360), (428, 360)], PAL["teal"][2], 5, 13))
    cv.add(P.card(cv, 436, 196, 350, 286, 20, "The result", "coral"), P.badge(cv, 458, 222, 3))
    res = [("Chloe", 91), ("Aisha", 72), ("Dev", 64)]
    cv.add(table(cv, 476, 252, ["name", "mark"], res, [140, 100], 36, tint={0: "#E6F7EE"}))
    cv.add(cv.text(611, 420, "only the two chosen columns,", 13.5, 750, cls="il-ink"), cv.text(611, 440, "highest mark first", 13.5, 750, cls="il-ink"))
    return figure(
        "sql-anatomy", cv, "An SQL query labelled clause by clause, and what each clause does to the table",
        "An SQL query is read clause by clause. SELECT name, mark chooses which columns. FROM results says which table. WHERE mark greater than "
        "60 chooses which rows. ORDER BY mark DESC puts them in order, highest first. Applied to a table of five pupils, id, name and mark, "
        "WHERE drops Ben on 55 and Eli on 48 and keeps three rows. SELECT keeps only the name and mark columns. ORDER BY puts the result in "
        "order: Chloe 91, Aisha 72 and Dev 64.",
        ["Each clause has a job: SELECT picks columns, FROM names the table, WHERE picks rows, ORDER BY sorts.", "WHERE keeps the rows that meet the condition and drops the rest.",
         "The result has only the selected columns, in the order asked for."],
        "Read a query in the order FROM, WHERE, SELECT, ORDER BY: pick the table, filter the rows, choose the columns, then sort.")


# ------------------------------------------------------------------ the programming project

@illustration("nea-lifecycle")
def _nea():
    cv = Canvas(800, 500).backdrop()
    stages = [("Analysis", "coral", ("the problem and who it is for", "research into similar solutions", "requirements and success criteria", "limits and scope")),
              ("Design", "sun", ("break the problem into parts", "algorithms and data structures", "screens and usability", "a test plan with test data")),
              ("Development", "mint", ("build it in small steps", "annotated code as evidence", "test as you go", "record each change")),
              ("Testing", "sky", ("run the test plan", "normal, boundary and erroneous data", "tables and screenshots as evidence", "fix, then retest")),
              ("Evaluation", "plum", ("judge against each success criterion", "feedback from the users", "what works, and what does not", "improvements and maintenance"))]
    for i, (name, col, bullets) in enumerate(stages):
        x = 14 + i * 156
        lo, base, hi = PAL[col]
        pts = [(x, 34), (x + 134, 34), (x + 152, 64), (x + 134, 94), (x, 94), (x + 18, 64)] if i else [(x, 34), (x + 134, 34), (x + 152, 64), (x + 134, 94), (x, 94)]
        cv.add(cv.poly([(px, py + 4) for px, py in pts], hi), cv.poly(pts, cv.g(col)))
        cv.add(cv.text(x + 80, 70, name, 15, 800, fill="#FFFFFF" if col == "plum" else INK))
        cv.add(P.badge(cv, x + 14, 30, i + 1))
        cv.add(P.card(cv, x, 112, 148, 282, 16))
        yy = 140
        for b in bullets:
            lines = wrap(b, 17)
            cv.add(cv.circle(x + 14, yy - 4, 3.6, cv.g(col, "deep")))
            for j, ln in enumerate(lines):
                cv.add(cv.text(x + 26, yy + j * 16, ln, 12.5, 650, anchor="start", cls="il-ink"))
            yy += len(lines) * 16 + 18
    cv.add(P.curve_arrow(cv, (470, 400), (470, 436), (330, 436), (330, 402), PAL["sky"][2], 3.5, 11))
    cv.add(cv.text(400, 450, "iterate: test, then go back and improve", 13, 750, cls="il-ink"))
    cv.add(P.card(cv, 14, 462, 772, 30, 12))
    cv.add(cv.text(400, 482, "Keep your evidence as you go. The evidence is what earns the marks.", 13.5, 800, cls="il-ink"))
    return figure(
        "nea-lifecycle", cv, "The five stages of the programming project, with the evidence each one needs",
        "The programming project runs through five stages. Analysis: the problem and who it is for, research into similar solutions, requirements "
        "and success criteria, and the limits and scope. Design: breaking the problem into parts, algorithms and data structures, screens and "
        "usability, and a test plan with test data. Development: building in small steps, annotated code as evidence, testing as you go and "
        "recording each change. Testing: running the test plan with normal, boundary and erroneous data, keeping tables and screenshots as "
        "evidence, and fixing and retesting. Evaluation: judging the work against each success criterion, feedback from the users, what works "
        "and what does not, and improvements and maintenance. An arrow shows that testing leads back to development to iterate. Keep your evidence "
        "as you go, because the evidence is what earns the marks.",
        ["Analysis, design, development, testing and evaluation, in that order.", "Each stage has its own evidence.",
         "Testing leads back to development, so the project iterates.", "Collect the evidence as you work, not at the end."],
        "Success criteria written at the analysis stage are what you test and evaluate against at the end.")


# ------------------------------------------------------------------ levels of testing

@illustration("test-levels")
def _levels():
    cv = Canvas(800, 500).backdrop()
    layers = [("Acceptance", "coral", "the client or users decide if it does the job"), ("System", "sun", "the whole program, against the requirements"),
              ("Integration", "mint", "modules working together"), ("Unit", "sky", "one function or method on its own: many, fast tests")]
    base_w, top_w, top_y, lh = 400, 90, 40, 64
    for i, (name, col, desc) in enumerate(layers):
        wt = top_w + i * (base_w - top_w) / 4.0
        wb = top_w + (i + 1) * (base_w - top_w) / 4.0
        y = top_y + i * lh
        cx = 222
        pts = [(cx - wt / 2, y), (cx + wt / 2, y), (cx + wb / 2, y + lh - 4), (cx - wb / 2, y + lh - 4)]
        cv.add(cv.poly(pts, cv.g(col), stroke="#FFFFFF", sw=3), cv.text(cx, y + lh / 2 + 3, name, 14.5, 800, fill=INK))
        cv.add(cv.line(cx + wb / 2 + 6, y + lh / 2, 450, y + lh / 2, "#8AA0AC", 1.6, dash="3 4"))
        for j, ln in enumerate(wrap(desc, 30)):
            cv.add(cv.text(458, y + lh / 2 - (len(wrap(desc, 30)) - 1) * 9 + j * 18 + 5, ln, 14, 700, anchor="start", cls="il-ink"))
    cv.add(P.badge(cv, 46, 52, 1))
    cv.add(cv.text(222, 312, "fewer tests as you go up, but each covers more", 13, 650, cls="il-ink2"))
    # black box and white box
    cv.add(P.card(cv, 14, 342, 380, 142, 18, "Black box testing", "slate"), P.badge(cv, 36, 366, 2))
    cv.add(cv.rect(158, 380, 92, 70, 10, "#1C2831"), cv.text(204, 421, "?", 28, 800, fill="#FFFFFF"))
    cv.add(P.arrow(cv, [(86, 415), (150, 415)], ARROW, 3.5, 10), P.arrow(cv, [(258, 415), (322, 415)], ARROW, 3.5, 10))
    cv.add(cv.text(60, 408, "input", 12.5, 700, cls="il-ink2"), cv.text(354, 408, "output", 12.5, 700, cls="il-ink2"))
    cv.add(cv.text(204, 470, "test inputs and outputs, without seeing the code", 12.5, 650, cls="il-ink"))
    cv.add(P.card(cv, 406, 342, 380, 142, 18, "White box testing", "slate"), P.badge(cv, 428, 366, 3))
    cv.add(cv.rect(550, 380, 92, 70, 10, "#FFFFFF", stroke="#8AA0AC", sw=2))
    cv.add(cv.path("M566 395 L596 395 L596 414 L626 414", stroke="#1F5F9A", sw=3), cv.path("M566 395 L566 436 L626 436", stroke="#BA352D", sw=3), cv.circle(596, 414, 4, "#1F5F9A"))
    cv.add(P.arrow(cv, [(478, 415), (542, 415)], ARROW, 3.5, 10), P.arrow(cv, [(650, 415), (714, 415)], ARROW, 3.5, 10))
    cv.add(cv.text(596, 470, "test every path through the code", 12.5, 650, cls="il-ink"))
    return figure(
        "test-levels", cv, "The four levels of testing as a pyramid, and black box against white box testing",
        "Four levels of testing drawn as a pyramid. At the base are unit tests, one function or method on its own, which are many and fast. Above "
        "them are integration tests, which check modules working together, then system tests, which check the whole program against the "
        "requirements, and at the top acceptance tests, where the client or users decide whether it does the job. There are fewer tests as you go "
        "up but each covers more. Below, black box testing checks inputs and outputs without seeing the code, and white box testing checks every path "
        "through the code.",
        ["Four levels: unit, integration, system and acceptance. Unit tests are many and fast, acceptance tests are few and cover the most.",
         "Black box: test the inputs and outputs without seeing the code.", "White box: test every path through the code."],
        "Name the level, say what it tests and who runs it. Acceptance testing is done by the client or users.")


# ------------------------------------------------------------------ test driven development

@illustration("tdd-cycle")
def _tdd():
    cv = Canvas(800, 500).backdrop()
    nodes = [("RED", "#BA352D", (128, 126), ("a test that fails",)), ("GREEN", "#1E7344", (320, 126), ("just enough code", "to pass")), ("REFACTOR", "#1F5F9A", (224, 316), ("tidy up, and the", "tests stay green"))]
    cv.add(P.card(cv, 14, 30, 380, 452, 20, "Test driven development", "teal"))
    cv.add(P.arrow(cv, [(190, 126), (256, 126)], ARROW, 4.5, 13), P.curve_arrow(cv, (310, 182), (302, 214), (286, 238), (270, 256), ARROW, 4.5, 13), P.curve_arrow(cv, (178, 258), (162, 238), (144, 214), (136, 184), ARROW, 4.5, 13))
    for i, (name, col, (cx, cy), cap) in enumerate(nodes):
        cv.add(cv.circle(cx, cy + 4, 60, "#10303A", op=.2), cv.circle(cx, cy, 60, col, stroke="#FFFFFF", sw=3.5), cv.text(cx, cy - 6, name, 16, 800, fill="#FFFFFF", mono=True))
        for j, ln in enumerate(cap):
            cv.add(cv.text(cx, cy + 16 + j * 16, ln, 12, 700, fill="#FFFFFF"))
        cv.add(P.badge(cv, cx - 50, cy - 46, i + 1))
    cv.add(cv.text(204, 422, "write the test first, then the code,", 13, 650, cls="il-ink2"), cv.text(204, 442, "and repeat in tiny steps", 13, 650, cls="il-ink2"))
    # an example of each
    cv.add(G.code(cv, 414, 30, 372, ["assert add(2, 3) == 5"], title="test_add.py", size=12.5, numbers=False))
    cv.add(G.terminal(cv, 414, 112, 372, [("NameError: add is not defined", "#FF9A91"), ("1 failed", "#FF9A91")], "red", 12))
    cv.add(G.code(cv, 414, 204, 372, ["def add(a, b):", "    return a + b"], title="add.py", size=12.5, numbers=False))
    cv.add(G.terminal(cv, 414, 316, 372, [("1 passed", "#9AF0B5")], "green", 12))
    cv.add(P.pill(cv, 604, 466, "refactor, then run the tests again: still 1 passed", "paper", 12.5, 12, 26, 700))
    cv.add(P.badge(cv, 404, 46, 1), P.badge(cv, 404, 220, 2), P.badge(cv, 404, 466, 3))
    return figure(
        "tdd-cycle", cv, "The red, green, refactor cycle of test driven development, with an example",
        "Test driven development repeats a three step cycle. Red: write a test first and watch it fail, here assert add of 2 and 3 equals 5, which "
        "fails with a NameError because add does not exist yet. Green: write just enough code to make the test pass, here def add of a and b "
        "returning a plus b, and the test result is 1 passed. Refactor: tidy up the code while the tests stay green, then run the tests again to "
        "check that they still pass. Then repeat in tiny steps.",
        ["Red: write a test that fails.", "Green: write just enough code to make it pass.", "Refactor: improve the code, and run the tests again to be sure they still pass."],
        "The test comes first. It describes what the code must do before any of the code exists.")
