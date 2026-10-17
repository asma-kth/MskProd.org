"""A Level illustrations, set one: translators, methodologies, paradigms, the Little Man Computer,
addressing modes, hashing, hash tables and the split between browser and server."""
import hashlib
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


def lines_at(cv, x, y, text, n, size=12.5, weight=650, cls="il-ink2", anchor="middle", gap=None):
    gap = gap or size * 1.32
    return "".join(cv.text(x, y + i * gap, ln, size, weight, anchor=anchor, cls=cls) for i, ln in enumerate(wrap(text, n)))


def token(cv, x, y, text, kind, h=26):
    col = {"id": "sky", "op": "slate", "num": "sun"}[kind]
    w = len(text) * 8.4 + 16
    return P.lift(cv, x, y, w, h, col, 7, 3, hl=False) + cv.text(x + w / 2, y + h / 2 + 4.8, text, 13, 800, fill=INK, mono=True), w


# ------------------------------------------------------------------ compilation

@illustration("compilation-stages")
def _compile():
    cv = Canvas(800, 500).backdrop()
    cv.add(P.pill(cv, 400, 18, "total = price + 2", "paper", 15, 18, 28, 800))
    names = [("Lexical analysis", "teal"), ("Syntax analysis", "sky"), ("Code generation", "sun"), ("Optimisation", "mint")]
    caps = ["tokens and a symbol table", "an abstract syntax tree", "machine or object code", "faster, smaller code"]
    for i, (name, col) in enumerate(names):
        x = 14 + i * 196
        cv.add(P.card(cv, x, 52, 186, 200, 18), P.pill(cv, x + 93, 52, name, col, 14.5, 12, 28, 750), P.badge(cv, x + 18, 78, i + 1, "deep", 13))
        cx = x + 93
        if i == 0:
            xs = x + 16
            row1, row2 = [("id", "total"), ("op", "="), ("id", "price")], [("op", "+"), ("num", "2")]
            for r, items in enumerate((row1, row2)):
                cx0 = xs + 4
                for kind, t in items:
                    mk, w = token(cv, cx0, 100 + r * 40, t, kind)
                    cv.add(mk)
                    cx0 += w + 6
            cv.add(cv.text(cx, 188, "symbol table:", 12, 700, cls="il-ink2"), cv.text(cx, 206, "total, price", 12.5, 750, cls="il-ink", mono=True))
        elif i == 1:
            nodes = {"=": (cx, 108), "total": (cx - 44, 150), "+": (cx + 36, 150), "price": (cx + 4, 192), "2": (cx + 68, 192)}
            for a_, b_ in (("=", "total"), ("=", "+"), ("+", "price"), ("+", "2")):
                cv.add(cv.line(nodes[a_][0], nodes[a_][1], nodes[b_][0], nodes[b_][1], "#8AA0AC", 2.4))
            for t, (nx, ny) in nodes.items():
                w = max(26, len(t) * 8 + 14)
                cv.add(cv.rect(nx - w / 2, ny - 13, w, 26, 13, "#FFFFFF", stroke="#2F82C0", sw=2), cv.text(nx, ny + 4.8, t, 12.5, 800, fill=INK, mono=True))
        elif i == 2:
            cv.add(G.code(cv, x + 18, 92, 150, ["LDA price", "ADD 2", "STA total"], title=None, size=12.5, numbers=False))
        else:
            cv.add(G.code(cv, x + 18, 90, 150, ["x = 2 * 3"], title=None, size=12.5, numbers=False))
            cv.add(P.arrow(cv, [(cx, 142), (cx, 162)], ARROW, 3.5, 10))
            cv.add(G.code(cv, x + 18, 168, 150, ["x = 6"], title=None, size=12.5, numbers=False))
        cv.add(cv.text(cx, 240, caps[i], 12.5, 700, cls="il-ink"))
        if i < 3:
            cv.add(P.arrow(cv, [(x + 187, 152), (x + 196, 152)], PAL["teal"][2], 3, 7))
    # linking and loading
    cv.add(P.card(cv, 14, 280, 282, 202, 18), P.pill(cv, 155, 280, "Static linking", "coral", 14.5, 12, 28, 750), P.badge(cv, 32, 306, 5, "deep", 13))
    cv.add(P.lift(cv, 34, 322, 242, 66, "slate", 12, 5, hl=False), cv.text(155, 338, "the executable", 12, 700, fill=INK))
    cv.add(P.lift(cv, 46, 346, 100, 32, "sky", 8, 3, hl=False), cv.text(96, 367, "your code", 12.5, 750, fill=INK), P.lift(cv, 154, 346, 110, 32, "sun", 8, 3, hl=False), cv.text(209, 367, "library copy", 12.5, 750, fill=INK))
    cv.add(lines_at(cv, 155, 420, "bigger file, but it runs on its own and later library changes cannot break it", 36, 12.5, 650))
    cv.add(P.card(cv, 308, 280, 282, 202, 18), P.pill(cv, 449, 280, "Dynamic linking", "coral", 14.5, 12, 28, 750), P.badge(cv, 326, 306, 6, "deep", 13))
    for k, t in enumerate(("program A", "program B")):
        cv.add(P.lift(cv, 326, 322 + k * 46, 92, 34, "sky", 8, 3, hl=False), cv.text(372, 344 + k * 46, t, 12.5, 750, fill=INK))
        cv.add(P.arrow(cv, [(422, 339 + k * 46), (462, 360)], ARROW, 3, 9))
    cv.add(P.lift(cv, 466, 332, 108, 56, "sun", 10, 4, hl=False), cv.text(520, 356, "shared", 12.5, 750, fill=INK), cv.text(520, 374, "library", 12.5, 750, fill=INK))
    cv.add(lines_at(cv, 449, 420, "smaller files and shared updates, but the library must be there at run time", 36, 12.5, 650))
    cv.add(P.card(cv, 602, 280, 184, 202, 18), P.pill(cv, 694, 280, "Loader", "mint", 14.5, 12, 28, 750), P.badge(cv, 620, 306, 7, "deep", 13))
    cv.add(P.lift(cv, 632, 322, 124, 32, "slate", 8, 3, hl=False), cv.text(694, 343, "executable", 12.5, 750, fill=INK))
    cv.add(P.arrow(cv, [(694, 362), (694, 384)], ARROW, 3.5, 10), P.ram_stick(cv, 624, 392, 140, 38, 1, 4))
    cv.add(cv.text(694, 458, "copies it into memory", 12.5, 650, cls="il-ink2"))
    return figure(
        "compilation-stages", cv, "The four stages of compilation for total = price + 2, then linking and loading",
        "How a compiler turns the line total equals price plus 2 into a program. Stage one, lexical analysis, reads the characters and groups them "
        "into tokens: the identifiers total and price, the operators equals and plus, and the number 2. Identifiers go into a symbol table. Stage "
        "two, syntax analysis, checks the tokens against the grammar and builds an abstract syntax tree with an equals at the top, total on "
        "one side and plus on the other, which has price and 2 beneath it. Stage three, code generation, produces machine or object code: "
        "load price, add 2, store total. Stage four, optimisation, improves the code, for example turning 2 times 3 into 6 before the program "
        "runs. Then the linker joins the object code to libraries. With static linking the library code is copied into the executable, "
        "giving a bigger file that runs on its own. With dynamic linking the programs only refer to a shared library, giving smaller files and "
        "shared updates, but the library must be present at run time. The loader copies the executable into memory.",
        ["Lexical analysis: group the characters into tokens and record the names in the symbol table.", "Syntax analysis: check the grammar and build the abstract syntax tree.",
         "Code generation: produce machine or object code.", "Optimisation: make the code faster or smaller.", "Static linking copies library code into the executable.",
         "Dynamic linking keeps a reference to a shared library, loaded when the program runs.", "The loader copies the executable into memory and prepares it to run."],
        "Lexical, syntax, code generation, optimisation. Say what each one produces: tokens, a tree, object code, better code.")


# ------------------------------------------------------------------ development methodologies

@illustration("methodologies")
def _methods():
    cv = Canvas(800, 500).backdrop()
    spec = [("Waterfall", "sky", ("Clear documents at every stage", "Inflexible: late changes cost a lot")), ("Agile", "mint", ("Working software early and often", "Needs the customer all the time")),
            ("Extreme programming", "coral", ("Pairs, tests first, small releases", "High quality but needs discipline")), ("Spiral", "plum", ("Risk analysed on every turn", "Expensive, needs risk expertise"))]
    for n, (title, col, (good, bad)) in enumerate(spec):
        x, y = (14, 406)[n % 2], (30, 258)[n // 2]
        cv.add(P.card(cv, x, y, 380, 214, 20, title, col), P.badge(cv, x + 22, y + 24, n + 1))
        if n == 0:
            for i, t in enumerate(("Analysis", "Design", "Implement", "Test", "Evaluate")):
                bx = x + 24 + i * 66
                cv.add(P.lift(cv, bx, y + 44 + i * 18, 64, 26, "sky", 6, 3, hl=False), cv.text(bx + 32, y + 62 + i * 18, t, 11, 750, fill=INK))
                if i < 4:
                    cv.add(P.arrow(cv, [(bx + 50, y + 70 + i * 18), (bx + 58, y + 62 + (i + 1) * 18)], ARROW, 2, 6))
        elif n == 1:
            for k in range(4):
                bx = x + 24 + k * 84
                cv.add(P.lift(cv, bx, y + 48, 70, 50, "mint", 10, 4, hl=False), cv.text(bx + 35, y + 70, "cycle", 11.5, 700, fill=INK), cv.text(bx + 35, y + 88, str(k + 1), 14, 800, fill=INK, mono=True))
                cv.add(P.pill(cv, bx + 35, y + 118, "working!", "paper", 11.5, 6, 20, 750))
                if k < 3:
                    cv.add(P.arrow(cv, [(bx + 72, y + 73), (bx + 84, y + 73)], ARROW, 2.5, 6))
            cv.add(cv.text(x + 190, y + 146, "short cycles, the customer reviews each one", 12.5, 650, cls="il-ink2"))
        elif n == 2:
            cv.add(P.laptop(cv, x + 20, y + 54, .5))
            cv.add(P.person(cv, x + 138, y + 52, .4, "tan", "brown", "sky", "short"), P.person(cv, x + 188, y + 52, .4, "light", "black", "coral", "bun"))
            cv.add(cv.text(x + 160, y + 140, "pair programming", 12.5, 700, cls="il-ink2"))
            for k, t in enumerate(("test first", "tiny releases", "refactor")):
                cv.add(P.pill(cv, x + 318, y + 56 + k * 30, t, "paper", 12, 10, 22, 700))
        else:
            cx, cy, r = x + 190, y + 104, 54
            for k, (t, c) in enumerate((("objectives", "sun"), ("risk", "coral"), ("build", "mint"), ("plan next", "sky"))):
                a0 = -90 + k * 90
                x0_, y0_, x1_, y1_ = cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0)), cx + r * math.cos(math.radians(a0 + 90)), cy + r * math.sin(math.radians(a0 + 90))
                cv.add(cv.path("M%s %s L%s %s A%s %s 0 0 1 %s %s Z" % (cx, cy, _n(x0_), _n(y0_), r, r, _n(x1_), _n(y1_)), fill=cv.g(c), stroke="#FFFFFF", sw=2.5))
            for (tx, ty, t) in ((cx + 24, cy - 24, "aims"), (cx + 28, cy + 30, "risk"), (cx - 26, cy + 30, "build"), (cx - 26, cy - 24, "plan")):
                cv.add(cv.text(tx, ty + 4, t, 11.5, 800, fill=INK))
        cv.add(P.tick(cv, x + 30, y + 168, 8), cv.text(x + 46, y + 173, good, 13, 700, anchor="start", cls="il-ink"))
        cv.add(P.cross(cv, x + 30, y + 194, 8), cv.text(x + 46, y + 199, bad, 13, 700, anchor="start", cls="il-ink"))
    return figure(
        "methodologies", cv, "Four development methodologies: waterfall, agile, extreme programming and spiral",
        "Four ways of running a software project, one card each with a strength and a weakness. Waterfall runs the stages in order, analysis, "
        "design, implementation, test and evaluate, each finished before the next begins, drawn as a staircase. It gives clear documents at every "
        "stage but is inflexible, because a late change costs a lot. Agile works in short cycles that each produce working software for the "
        "customer to review, which is early and often, but it needs the customer all the time. Extreme programming, a form of agile, uses pair "
        "programming, tests written first, tiny releases and refactoring. It gives high quality but needs discipline. The spiral model goes "
        "round four quadrants, objectives, risk analysis, build and plan the next turn, so risk is analysed on every turn. It suits large, "
        "high risk projects but is expensive and needs risk expertise.",
        ["Waterfall: each stage is finished before the next begins. Clear, but inflexible.", "Agile: short cycles with working software each time. Flexible, but needs the customer.",
         "Extreme programming: pair programming, tests first and tiny releases.", "Spiral: repeated turns with risk analysis each time. Good for large, risky projects."],
        "Justify your choice from the scenario: fixed, safety critical requirements suggest waterfall, changing requirements suggest agile.")
