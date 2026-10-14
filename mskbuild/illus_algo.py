"""Illustrations for algorithms, computational thinking, searching, sorting and complexity."""
import math
import random

from .illus import Canvas, PAL, INK, figure, illustration, _n
from . import illus_props as P
from . import illus_glyphs as G


def num_tile(cv, x, y, v, w=52, h=48, color="sky", size=22, op=None):
    """A numbered card, the unit every searching and sorting picture is built from.

    op fades the card but not its number, so a card that is out of play is still readable.
    """
    face = P.lift(cv, x, y, w, h, color, 10, 5, hl=False)
    if op is not None:
        face = '<g opacity="%s">%s</g>' % (op, face)
    return face + cv.text(x + w / 2, y + h / 2 + size * .36, str(v), size, 800, fill=INK, mono=True)


# ------------------------------------------------- the four techniques

def mini_bars(cv, x, y, w, h, vals, hot, color="sky"):
    out = ""
    bw = w / len(vals)
    for i, v in enumerate(vals):
        bh = h * v / 100.0
        c = "coral" if i == hot else color
        out += cv.rect(x + i * bw + 2, y + h - bh, bw - 4, bh, 3, cv.g(c))
    return out + cv.line(x, y + h + 1, x + w, y + h + 1, "#8AA0AC", 1.6)


@illustration("ct-four")
def _ct_four():
    cv = Canvas(800, 500).backdrop()
    spec = [("Decomposition", "teal", 14, 34), ("Abstraction", "sky", 406, 34), ("Pattern recognition", "coral", 14, 262), ("Algorithms", "plum", 406, 262)]
    for t, col, x, y in spec:
        cv.add(P.card(cv, x, y, 380, 212, 20, t, col))
    # decomposition
    cv.add(P.lift(cv, 34, 106, 124, 66, "sun", 14, 6, hl=False), cv.text(96, 134, "Plan a", 15, 800, fill=INK), cv.text(96, 154, "journey", 15, 800, fill=INK))
    for i, t in enumerate(("find the roads", "choose a route", "estimate the time", "give directions")):
        yy = 74 + i * 36
        cv.add(cv.path("M158 139 C190 139 188 %d 214 %d" % (yy + 14, yy + 14), stroke=PAL["teal"][1], sw=2.6))
        cv.add(P.lift(cv, 214, yy, 156, 28, "teal", 8, 4, hl=False), cv.text(292, yy + 19, t, 13, 750, fill=P._on("teal")))
    cv.add(cv.text(204, 232, "break a big problem into small parts", 13, 700, cls="il-ink"))
    # abstraction: a messy town becomes a clean map
    rnd = random.Random(7)
    clip = cv._def("ctclip", '<clipPath id="{id}"><rect x="426" y="70" width="150" height="124" rx="10"/></clipPath>')
    town = cv.rect(426, 70, 150, 124, 10, "#E6EEF2")
    town += cv.path("M426 140 Q470 120 500 150 T576 130", stroke="#9CD3F0", sw=14)
    town += cv.path("M440 70 L470 194 M520 70 L540 194 M426 110 L576 100", stroke="#C3CFD8", sw=7)
    for _ in range(12):
        hx, hy = 432 + rnd.random() * 134, 76 + rnd.random() * 108
        town += cv.rect(hx, hy, 10, 8, 1, rnd.choice(("#C9A27A", "#E8B7A0", "#B8C5CF"))) + cv.poly([(hx - 1, hy), (hx + 5, hy - 5), (hx + 11, hy)], "#8E5B2B")
    for _ in range(10):
        town += cv.circle(432 + rnd.random() * 134, 76 + rnd.random() * 108, 5, "#62B58A")
    cv.add('<g clip-path="%s">%s</g>' % (clip, town))
    cv.add(cv.rect(426, 70, 150, 124, 10, "none", stroke="#B9C6CE", sw=2))
    cv.add(P.arrow(cv, [(582, 132), (608, 132)], PAL["sky"][2], 4, 11))
    cv.add(cv.rect(614, 70, 152, 124, 10, "#FFFFFF", stroke="#B9C6CE", sw=2))
    for pts, c in ((((630, 170), (660, 140), (700, 140), (750, 96)), "#F0584B"), (((632, 100), (672, 130), (700, 140), (746, 176)), "#25B3BB"), (((650, 184), (680, 160), (716, 110), (744, 82)), "#8B6BB8")):
        cv.add(cv.path("M" + " L".join("%d %d" % p for p in pts), stroke=c, sw=5))
    for (px, py) in ((660, 140), (700, 140), (680, 160), (716, 110), (672, 130)):
        cv.add(cv.circle(px, py, 6, "#FFFFFF", stroke="#1F3A44", sw=2.4))
    cv.add(cv.text(596, 232, "keep what matters, hide the rest", 13, 700, cls="il-ink"))
    # pattern recognition: the same rush hour every weekday
    for i, d in enumerate("MTWTF"):
        x = 36 + i * 68
        cv.add(mini_bars(cv, x, 316, 58, 66, [14, 34, 92, 40, 16], 2))
        cv.add(cv.text(x + 29, 402, d, 13, 800, cls="il-ink"))
    cv.add(cv.text(204, 456, "the same peak every weekday, so we can predict it", 13, 700, cls="il-ink"))
    # algorithms: clear steps
    for i, t in enumerate(("find where you are", "find where you want to go", "pick the shortest route", "give the next turn")):
        yy = 306 + i * 36
        cv.add(cv.circle(436, yy + 12, 13, cv.g("plum", "deep")), cv.text(436, yy + 18, str(i + 1), 15, 800, fill="#FFFFFF"))
        cv.add(P.lift(cv, 460, yy, 290, 26, "paper", 8, 3, hl=False), cv.text(476, yy + 19, t, 13.5, 750, anchor="start", fill=INK))
        if i < 3:
            cv.add(P.arrow(cv, [(436, yy + 26), (436, yy + 38)], PAL["plum"][2], 3, 7))
    cv.add(cv.text(596, 456, "clear steps anyone could follow", 13, 700, cls="il-ink"))
    cv.add(P.badge(cv, 30, 36, 1), P.badge(cv, 422, 36, 2), P.badge(cv, 30, 264, 3), P.badge(cv, 422, 264, 4))
    return figure(
        "ct-four", cv, "The four techniques of computational thinking, shown on a satnav",
        "The four techniques of computational thinking, one card each, all using a satnav as the example. Decomposition breaks a big problem into small "
        "parts: plan a journey splits into find the roads, choose a route, estimate the time and give directions. Abstraction keeps what matters and "
        "hides the rest: a busy picture of a town, with its houses, trees, river and roads, is simplified into a clean map of coloured lines and "
        "stations. Pattern recognition spots what repeats: five small charts for Monday to Friday all show the same rush hour peak, so it can be "
        "predicted. Algorithms are clear, step by step instructions anyone could follow: find where you are, find where you want to go, pick the "
        "shortest route and give the next turn.",
        ["Decomposition: break a big problem into small parts you can solve one at a time.",
         "Abstraction: keep what matters and hide the detail you do not need.",
         "Pattern recognition: spot what repeats, so one solution can be reused.",
         "Algorithms: put the solution in clear steps that a computer, or anyone, can follow."],
        "A real problem needs all four. Name the technique and say what it did to the problem.")


@illustration("abstraction-map")
def _abstraction_map():
    cv = Canvas(800, 500).backdrop()
    rnd = random.Random(11)
    cv.add(P.card(cv, 14, 34, 372, 262, 20, "The real town", "slate"))
    clip = cv._def("amclip", '<clipPath id="{id}"><rect x="30" y="68" width="340" height="212" rx="12"/></clipPath>')
    town = cv.rect(30, 68, 340, 212, 12, "#E6EEF2")
    town += cv.path("M30 190 Q120 150 200 200 T370 170", stroke="#9CD3F0", sw=24)
    town += cv.path("M80 68 L110 280 M220 68 L250 280 M30 120 L370 108 M30 240 L370 252", stroke="#C3CFD8", sw=11)
    for _ in range(30):
        hx, hy = 38 + rnd.random() * 320, 74 + rnd.random() * 196
        town += cv.rect(hx, hy, 15, 12, 1.5, rnd.choice(("#C9A27A", "#E8B7A0", "#B8C5CF", "#D8C58E"))) + cv.poly([(hx - 1, hy), (hx + 7.5, hy - 7), (hx + 16, hy)], "#8E5B2B")
    for _ in range(26):
        town += cv.circle(38 + rnd.random() * 320, 74 + rnd.random() * 196, 6.5, "#62B58A")
    for _ in range(8):
        cx_, cy_ = 38 + rnd.random() * 320, 74 + rnd.random() * 196
        town += cv.rect(cx_, cy_, 12, 6, 2, rnd.choice(("#F0584B", "#4FA3D9", "#FFC93C")))
    cv.add('<g clip-path="%s">%s</g>' % (clip, town))
    cv.add(cv.rect(30, 68, 340, 212, 12, "none", stroke="#B9C6CE", sw=2))
    cv.add(P.arrow(cv, [(392, 166), (424, 166)], PAL["sky"][2], 6, 15))
    cv.add(P.card(cv, 414, 34, 372, 262, 20, "The abstraction", "sky"))
    cv.add(cv.rect(430, 68, 340, 212, 12, "#FFFFFF", stroke="#B9C6CE", sw=2))
    lines = [(((452, 250), (520, 200), (590, 200), (700, 110)), "#F0584B"), (((452, 112), (540, 176), (590, 200), (700, 250)), "#25B3BB"), (((500, 262), (560, 224), (640, 150), (730, 88)), "#8B6BB8")]
    for pts, c in lines:
        cv.add(cv.path("M" + " L".join("%d %d" % p for p in pts), stroke=c, sw=8))
    names = {(520, 200): ("Park", -12, 26, "end"), (590, 200): ("Centre", 12, 24, "start"), (540, 176): ("Market", -6, -16, "end"),
             (640, 150): ("Station", 12, -10, "start"), (700, 110): ("Hill", 12, -10, "start"), (700, 250): ("Docks", 12, 24, "start")}
    for (px, py), (n, dx, dy, anc) in names.items():
        cv.add(cv.circle(px, py, 8, "#FFFFFF", stroke="#1F3A44", sw=3))
        tw_ = len(n) * 7.4 + 10
        lx = px + dx - tw_ + 5 if anc == "end" else (px + dx - 5 if anc == "start" else px + dx - tw_ / 2)
        cv.add(cv.rect(lx, py + dy - 14, tw_, 19, 6, "#FFFFFF", op=.92))
        cv.add(cv.text(px + dx, py + dy, n, 12.5, 750, anchor=anc, fill=INK))
    cv.add(P.badge(cv, 30, 36, 1), P.badge(cv, 430, 36, 2))
    # what stays, what goes
    cv.add(P.card(cv, 14, 318, 262, 162, 18, "What stays", "teal"))
    for i, t in enumerate(("the stations", "which connect to which", "the lines")):
        cv.add(P.tick(cv, 40, 366 + i * 34, 10), cv.text(60, 371 + i * 34, t, 14, 700, anchor="start", cls="il-ink"))
    cv.add(P.card(cv, 292, 318, 262, 162, 18, "What goes", "coral"))
    for i, t in enumerate(("houses and trees", "exact distances", "street names")):
        cv.add(P.cross(cv, 318, 366 + i * 34, 10), cv.text(338, 371 + i * 34, t, 14, 700, anchor="start", cls="il-ink"))
    cv.add(P.card(cv, 570, 318, 216, 162, 18, "In code", "plum"))
    for i, (a_, b_) in enumerate((("score", "hides memory"), ("print()", "hides its code"), ("a button", "hides the server"))):
        cv.add(cv.text(588, 362 + i * 34, a_, 14, 800, anchor="start", cls="il-ink", mono=True), cv.text(588, 378 + i * 34, b_, 12, 650, anchor="start", cls="il-ink2"))
    cv.add(P.badge(cv, 30, 320, 3), P.badge(cv, 308, 320, 4))
    return figure(
        "abstraction-map", cv, "Abstraction: a map that keeps only what matters",
        "Abstraction shown with a town and a map of it. On the left is the real town, packed with houses, trees, a river, roads and cars. On the right "
        "is its abstraction, a clean map of three coloured lines, with stations as white circles and interchanges where lines cross. What stays is "
        "the stations, which connect to which, and the lines. What goes is the houses and trees, the exact distances and the street names, because "
        "none of them help you plan a journey. The same idea runs through programming: a variable name hides the memory address behind it, a "
        "function such as print hides the code inside it, and a button hides the server it talks to.",
        ["The real thing is full of detail: most of it is no use for the job in hand.",
         "The abstraction is a simple model that keeps only what the job needs.",
         "What stays: the stations, what connects to what, and the lines.",
         "What goes: the detail that does not help, such as houses, exact distances and street names."],
        "Abstraction is deciding what to leave out. Say what was removed and why it was safe to remove it.")


@illustration("decomposition-tree")
def _decomposition():
    cv = Canvas(800, 500).backdrop()
    cv.add(P.lift(cv, 205, 44, 170, 44, "sun", 14, 6, hl=False), cv.text(290, 73, "A quiz app", 19, 800, fill=INK))
    kids = [("Questions", "sky", ["store them", "pick at random", "check the answer"]), ("Scoring", "mint", ["add points", "high scores"]),
            ("Timer", "coral", ["count down", "end the round"]), ("Screens", "lilac", ["menu", "question", "results"])]
    for i, (t, col, leaves) in enumerate(kids):
        cx = 82 + i * 130
        cv.add(cv.path("M290 90 L290 104 L%d 104 L%d 126" % (cx, cx), stroke="#8AA0AC", sw=2.6))
        cv.add(P.lift(cv, cx - 58, 126, 116, 38, col, 12, 5, hl=False), cv.text(cx, 151, t, 15, 800, fill=INK))
        for k, lf in enumerate(leaves):
            ly = 196 + k * 40
            cv.add(cv.line(cx, 164 if k == 0 else ly - 10, cx, ly, "#8AA0AC", 2.4))
            cv.add(P.lift(cv, cx - 56, ly, 112, 30, "paper", 8, 4, hl=False), cv.text(cx, ly + 20, lf, 12.5, 700, fill=INK))
    cv.add(cv.text(290, 340, "each small part can be solved on its own", 13.5, 750, cls="il-ink"))
    cv.add(P.badge(cv, 196, 44, 1), P.badge(cv, 28, 128, 2), P.badge(cv, 28, 198, 3))
    # why
    cv.add(P.card(cv, 560, 34, 216, 446, 20, "Why break it up?", "teal"))
    why = [("Build in parallel", "different people write", "different parts", "sky"), ("Test one part", "a fault is easy to", "find in a small part", "mint"), ("Reuse a part", "the timer can serve", "another game", "sun")]
    for i, (h_, a_, b_, col) in enumerate(why):
        y = 90 + i * 124
        cv.add(P.lift(cv, 580, y, 176, 108, col, 14, 6, hl=False))
        if i == 0:
            cv.add(P.person(cv, 596, y + 16, .3, "tan", "black", "coral", "bun"), P.person(cv, 640, y + 16, .3, "light", "brown", "teal", "short"), P.person(cv, 684, y + 16, .3, "deep", "black", "plum", "curly"))
        elif i == 1:
            cv.add(P.magnifier(cv, 640, y + 36, .9, 16))
        else:
            cv.add(G.arrow_ring(cv, 668, y + 38, 18, -60, 240, "#8E5B2B", 4, 9))
        cv.add(cv.text(668, y + 72, h_, 14, 800, fill=INK), cv.text(668, y + 88, a_, 11.5, 650, fill="#2E4855"), cv.text(668, y + 101, b_, 11.5, 650, fill="#2E4855"))
    cv.add(P.badge(cv, 576, 36, 4))
    return figure(
        "decomposition-tree", cv, "Decomposition: breaking a quiz app into parts",
        "Decomposition drawn as a tree. The whole problem, a quiz app, sits at the top. It splits into four parts: questions, scoring, the timer and "
        "the screens. Each of those splits again into smaller jobs. Questions becomes store them, pick at random and check the answer. Scoring "
        "becomes add points and high scores. The timer becomes count down and end the round. The screens become the menu, the question screen "
        "and the results. Each small part can be solved on its own. A panel on the right gives the three reasons to do this: different people can "
        "build different parts at the same time, a fault is easy to find in a small part, and a part such as the timer can be reused in another program.",
        ["Start with the whole problem at the top.",
         "Split it into a few main parts.",
         "Keep splitting until every part is small enough to solve.",
         "Why bother: parts can be built in parallel, tested separately and reused."],
        "Decomposition is top-down: big problem, main parts, small jobs. Say what each small part is for.")


# ---------------------------------------------------------------- flowcharts

def fc_shape(cv, kind, cx, cy, w, h, label, color="paper", size=13):
    tc = INK if color in ("paper", "sun", "sky", "mint", "slate") else P._on(color)
    if kind == "terminal":
        out = cv.rect(cx - w / 2, cy - h / 2 + 4, w, h, h / 2, PAL[color][2]) + cv.rect(cx - w / 2, cy - h / 2, w, h, h / 2, cv.g(color))
    elif kind == "process":
        out = cv.rect(cx - w / 2, cy - h / 2 + 4, w, h, 6, PAL[color][2]) + cv.rect(cx - w / 2, cy - h / 2, w, h, 6, cv.g(color))
    elif kind == "decision":
        pts = [(cx, cy - h / 2), (cx + w / 2, cy), (cx, cy + h / 2), (cx - w / 2, cy)]
        out = cv.poly([(px, py + 4) for px, py in pts], PAL[color][2]) + cv.poly(pts, cv.g(color))
    else:  # input / output
        sk = h * .32
        pts = [(cx - w / 2 + sk, cy - h / 2), (cx + w / 2, cy - h / 2), (cx + w / 2 - sk, cy + h / 2), (cx - w / 2, cy + h / 2)]
        out = cv.poly([(px, py + 4) for px, py in pts], PAL[color][2]) + cv.poly(pts, cv.g(color))
    return out + cv.text(cx, cy + size * .36, label, size, 800, fill=tc, mono=(kind in ("process", "io")))


@illustration("flowchart-symbols")
def _flowchart():
    cv = Canvas(800, 500).backdrop()
    cv.add(P.card(cv, 14, 34, 306, 446, 20, "The symbols", "teal"))
    legend = [("terminal", "Start / Stop", "where it begins and ends", "green", "Start"), ("io", "Input / Output", "data in, or shown out", "sky", "INPUT"),
              ("process", "Process", "a calculation or an action", "mint", "x = x + 1"), ("decision", "Decision", "a question with two exits", "sun", "x > 5 ?")]
    for i, (k, name, d, col, lab) in enumerate(legend):
        y = 104 + i * 92
        cv.add(fc_shape(cv, k, 92, y, 112 if k != "decision" else 100, 48 if k != "decision" else 62, lab, col, 12.5 if k != "decision" else 12))
        cv.add(cv.text(166, y - 6, name, 15, 800, anchor="start", cls="il-ink"), cv.text(166, y + 14, d, 12, 650, anchor="start", cls="il-ink2"))
    cv.add(P.arrow(cv, [(60, 440), (130, 440)], PAL["ink"][1], 4, 12), cv.text(166, 445, "flow line: the order", 12, 650, anchor="start", cls="il-ink2"))
    cv.add(P.badge(cv, 30, 36, 1))
    # an example
    cv.add(P.card(cv, 336, 34, 450, 446, 20, "Example: a ticket price", "plum"))
    cx = 520
    cv.add(fc_shape(cv, "terminal", cx, 84, 100, 34, "Start", "green"))
    cv.add(P.arrow(cv, [(cx, 104), (cx, 120)], PAL["ink"][1], 3, 9))
    cv.add(fc_shape(cv, "io", cx, 140, 156, 38, "INPUT age", "sky"))
    cv.add(P.arrow(cv, [(cx, 162), (cx, 182)], PAL["ink"][1], 3, 9))
    cv.add(fc_shape(cv, "decision", cx, 222, 150, 70, "age < 16 ?", "sun"))
    cv.add(cv.text(cx - 94, 218, "Yes", 12.5, 800, anchor="end", cls="il-ink"), cv.text(cx + 94, 218, "No", 12.5, 800, cls="il-ink"))
    cv.add(cv.path("M%d 222 L%d 222 L%d 262" % (cx - 75, cx - 118, cx - 118), stroke="#4A6470", sw=3))
    cv.add(cv.path("M%d 222 L%d 222 L%d 262" % (cx + 75, cx + 118, cx + 118), stroke="#4A6470", sw=3))
    cv.add(P.arrow(cv, [(cx - 118, 252), (cx - 118, 268)], PAL["ink"][1], 3, 9), P.arrow(cv, [(cx + 118, 252), (cx + 118, 268)], PAL["ink"][1], 3, 9))
    cv.add(fc_shape(cv, "process", cx - 118, 292, 114, 36, "price = 5", "mint"), fc_shape(cv, "process", cx + 118, 292, 114, 36, "price = 8", "mint"))
    cv.add(cv.path("M%d 312 L%d 346 L%d 346" % (cx - 118, cx - 118, cx), stroke="#4A6470", sw=3), cv.path("M%d 312 L%d 346 L%d 346" % (cx + 118, cx + 118, cx), stroke="#4A6470", sw=3))
    cv.add(P.arrow(cv, [(cx, 346), (cx, 372)], PAL["ink"][1], 3, 9))
    cv.add(fc_shape(cv, "io", cx, 392, 170, 38, "OUTPUT price", "sky"))
    cv.add(P.arrow(cv, [(cx, 414), (cx, 430)], PAL["ink"][1], 3, 9))
    cv.add(fc_shape(cv, "terminal", cx, 448, 100, 34, "Stop", "green"))
    cv.add(P.badge(cv, 352, 36, 2), P.badge(cv, cx + 70, 184, 3))
    cv.add(G.code(cv, 640, 90, 134, ["age = input()", "if age < 16:", "  price = 5", "else:", "  price = 8", "print(price)"], None, 11.5, numbers=False))
    cv.add(cv.text(707, 250, "the same thing", 12, 700, cls="il-ink2"), cv.text(707, 267, "as code", 12, 700, cls="il-ink2"))
    return figure(
        "flowchart-symbols", cv, "Flowchart symbols, and a worked example",
        "The standard flowchart symbols on the left. A terminal, a rounded shape, marks where the program starts and stops. A parallelogram is "
        "input or output, data coming in or being shown. A rectangle is a process, a calculation or an action. A diamond is a decision: a question "
        "with two exits, Yes and No. Arrows are flow lines that show the order. On the right is a worked example. The flowchart starts, inputs an "
        "age, then asks whether age is less than 16. If yes the price is set to 5, and if no it is set to 8. Both routes join up again, the price "
        "is output, and the chart stops. The same logic is written as code in a small box beside it.",
        ["Each shape has one meaning: terminals start and stop, parallelograms are input or output, rectangles are processes, diamonds are decisions.",
         "Flow lines show the order, and every chart starts and stops with a terminal.",
         "A decision has two exits, labelled Yes and No, and the two routes join up again."],
        "Use the right shape for the job, label every decision exit, and let every route reach the end.")


# ------------------------------------------------------- searching, sorting

def row(cv, x, y, vals, kinds, w=44, h=44, pitch=48, size=19):
    """A row of number tiles. kinds: one of 'n' normal, 'x' checked, 'f' found, 'h' highlighted, 'g' sorted, 'd' dimmed."""
    colors = {"n": "sky", "x": "slate", "f": "green", "h": "sun", "g": "mint", "d": "slate", "c": "coral"}
    out = ""
    for i, (v, k) in enumerate(zip(vals, kinds)):
        out += num_tile(cv, x + i * pitch, y, v, w, h, colors[k], size, .8 if k == "d" else None)
    return out


@illustration("search-compare")
def _search():
    cv = Canvas(800, 500).backdrop()
    vals = [3, 8, 11, 14, 17, 21, 26, 30, 33, 38, 42, 47, 51, 56, 60]
    x0 = 40
    cx = lambda i: x0 + i * 48 + 22
    cv.add(P.card(cv, 14, 34, 772, 160, 20, "Linear search: look at every item in turn", "coral"))
    cv.add(row(cv, x0, 96, vals, ["x"] * 9 + ["f"] + ["n"] * 5))
    for i in range(10):
        cv.add(cv.text(cx(i), 88, str(i + 1), 12.5, 800, cls="il-ink2", mono=True))
    cv.add(P.arrow(cv, [(cx(0), 158), (cx(9) - 8, 158)], PAL["coral"][2], 4, 12))
    cv.add(P.pill(cv, cx(4), 176, "not it, not it, not it ...", "paper", 13, 12, 24, 700), P.pill(cv, cx(11), 176, "found it on the 10th look", "green", 13.5, 12, 26, 800))
    cv.add(P.badge(cv, 30, 36, 1))
    cv.add(P.card(cv, 14, 208, 772, 232, 20, "Binary search: halve the sorted list every time", "teal"))
    blocks = [(250, ["n"] * 7 + ["h"] + ["n"] * 7, "check the middle: 30. 38 is bigger, so drop the left half", 7),
              (316, ["d"] * 8 + ["n", "n", "n", "h", "n", "n", "n"], "check the middle: 47. 38 is smaller, so drop the right half", 11),
              (382, ["d"] * 8 + ["n", "f", "n"] + ["d"] * 4, "check the middle: 38. Found it, on the 3rd look", 9)]
    for i, (yy, kinds, note, mid) in enumerate(blocks):
        cv.add(row(cv, x0, yy, vals, kinds, 44, 32, 48, 16))
        cv.add(P.pill(cv, cx(mid), yy + 46, note, "green" if i == 2 else "paper", 12.5, 12, 20, 750))
    cv.add(P.badge(cv, 30, 210, 2))
    # the point of it
    cv.add(P.lift(cv, 24, 450, 220, 34, "coral", 12, 5, hl=False), cv.text(134, 473, "linear: 10 looks", 16, 800, fill=P._on("coral")))
    cv.add(P.lift(cv, 262, 450, 220, 34, "teal", 12, 5, hl=False), cv.text(372, 473, "binary: 3 looks", 16, 800, fill=P._on("teal")))
    cv.add(P.pill(cv, 636, 468, "binary search needs a sorted list", "sun", 13, 12, 28, 800))
    cv.add(P.badge(cv, 30, 452, 3))
    return figure(
        "search-compare", cv, "Linear search and binary search, looking for 38",
        "Two ways of finding the number 38 in a sorted list of fifteen numbers. In a linear search the program looks at the items one at a time from "
        "the left, so it has to look at the first nine and reject each one before it finds 38 on the tenth look. In a binary search the program checks "
        "the middle item, which is 30. 38 is bigger, so the whole left half is thrown away. It then checks the middle of what is left, which is 47. "
        "38 is smaller, so the right half is thrown away, leaving three items. The middle of those is 38, found on the third look. Binary search takes "
        "3 looks where linear search took 10, and the gap grows as the list grows, but binary search only works if the list is sorted.",
        ["Linear search looks at every item in turn from the start, so it can be slow.",
         "Binary search checks the middle and throws half the list away each time.",
         "3 looks against 10. The longer the list, the bigger the gap, but binary search needs the list sorted."],
        "Linear works on any list. Binary is far faster, but only on a sorted one.")


@illustration("bubble-sort-cards")
def _bubble():
    cv = Canvas(800, 500).backdrop()
    cv.add(P.card(cv, 14, 34, 410, 446, 20, "One pass, step by step", "coral"))
    states = [[5, 2, 4, 1, 3], [2, 5, 4, 1, 3], [2, 4, 5, 1, 3], [2, 4, 1, 5, 3], [2, 4, 1, 3, 5]]
    cmp_ = [(0, "5 > 2: swap"), (1, "5 > 4: swap"), (2, "5 > 1: swap"), (3, "5 > 3: swap"), None]
    for r, st in enumerate(states):
        y = 70 + r * 80
        kinds = ["n"] * 5
        if cmp_[r]:
            i = cmp_[r][0]
            kinds[i] = kinds[i + 1] = "h"
        else:
            kinds[4] = "g"
        cv.add(row(cv, 30, y, st, kinds, 46, 46, 52, 21))
        if cmp_[r]:
            i = cmp_[r][0]
            cv.add(P.curve_arrow(cv, (30 + i * 52 + 23, y - 4), (30 + i * 52 + 34, y - 20), (30 + i * 52 + 62, y - 20), (30 + i * 52 + 75, y - 4), PAL["coral"][2], 3, 9))
            cv.add(cv.text(300, y + 28, cmp_[r][1], 12.5, 800, anchor="start", cls="il-ink", mono=True))
        else:
            cv.add(cv.text(300, y + 28, "5 is in place", 12.5, 800, anchor="start", cls="il-ok"))
    cv.add(P.badge(cv, 30, 36, 1), P.badge(cv, 404, 94, 2), P.badge(cv, 404, 334, 3))
    cv.add(P.card(cv, 440, 34, 346, 446, 20, "After every pass", "teal"))
    passes = [("start", [5, 2, 4, 1, 3], 0), ("pass 1", [2, 4, 1, 3, 5], 1), ("pass 2", [2, 1, 3, 4, 5], 2), ("pass 3", [1, 2, 3, 4, 5], 3), ("pass 4", [1, 2, 3, 4, 5], 5)]
    for r, (lab, st, done) in enumerate(passes):
        y = 84 + r * 62
        cv.add(cv.text(460, y + 28, lab, 13.5, 800, anchor="start", cls="il-ink"))
        kinds = ["n"] * (5 - done) + ["g"] * done if done < 5 else ["g"] * 5
        cv.add(row(cv, 540, y, st, kinds, 40, 38, 44, 17))
    cv.add(cv.text(613, 408, "pass 4 made no swaps,", 13, 800, cls="il-ink"), cv.text(613, 428, "so the list is sorted", 13, 800, cls="il-ink"))
    cv.add(P.pill(cv, 613, 456, "stop when a pass makes no swaps", "sun", 12.5, 12, 24, 800))
    cv.add(P.badge(cv, 456, 36, 4))
    return figure(
        "bubble-sort-cards", cv, "Bubble sort on 5, 2, 4, 1, 3",
        "Bubble sort drawn with numbered cards. On the left is the first pass, step by step. The two cards being compared are lit up. 5 is bigger than "
        "2, so they swap. 5 is bigger than 4, so they swap again. 5 is bigger than 1 and then 3, and swaps each time, so the 5 has bubbled all the "
        "way to the end, where it is in its final place and is shown in green. On the right is the list after every pass: after pass 1 the 5 is in place, "
        "after pass 2 the 4 and 5, and after pass 3 the whole list is in order. Pass 4 makes no swaps at all, which is how the algorithm knows it can stop.",
        ["Compare two neighbours, and if they are the wrong way round, swap them.",
         "Work along the list. A big value is carried all the way to the end.",
         "After a pass the last item is in its final place, so the next pass can be shorter.",
         "Repeat until a whole pass makes no swaps."],
        "Each pass puts one more item in place. A pass with no swaps means the list is sorted.")


@illustration("merge-sort-cards")
def _merge():
    cv = Canvas(800, 500).backdrop()
    levels = [[[6, 3, 8, 1, 7, 2, 5, 4]], [[6, 3, 8, 1], [7, 2, 5, 4]], [[6, 3], [8, 1], [7, 2], [5, 4]], [[6], [3], [8], [1], [7], [2], [5], [4]],
              [[3, 6], [1, 8], [2, 7], [4, 5]], [[1, 3, 6, 8], [2, 4, 5, 7]], [[1, 2, 3, 4, 5, 6, 7, 8]]]
    tw_, gap = 34, 5
    for r, groups in enumerate(levels):
        y = 44 + r * 62
        n = sum(len(g) for g in groups)
        total = n * (tw_ + gap) - gap + (len(groups) - 1) * 16
        x = 360 - total / 2 + 20
        for g in groups:
            kind = "n" if r < 4 else "g"
            if r == 6:
                kind = "f"
            cv.add(row(cv, x, y, g, [kind] * len(g), tw_, 32, tw_ + gap, 16))
            gw = len(g) * (tw_ + gap) - gap
            cv.add(cv.rect(x - 4, y - 4, gw + 8, 40, 10, "none", stroke="#8AA0AC", sw=1.8, dash="3 4", op=.9))
            x += gw + 16
    # the labels down the side
    cv.add(P.arrow(cv, [(60, 66), (60, 232)], PAL["coral"][2], 5, 13), P.arrow(cv, [(60, 450), (60, 290)], PAL["teal"][2], 5, 13))
    cv.add(P.pill(cv, 60, 150, "divide", "coral", 14, 12, 26, 800), P.pill(cv, 60, 372, "merge", "teal", 14, 12, 26, 800))
    cv.add(P.pill(cv, 716, 232, "1 item is sorted", "sun", 12.5, 10, 24, 800))
    cv.add(P.card(cv, 640, 322, 146, 150, 16))
    cv.add(cv.text(713, 348, "to merge:", 13, 800, cls="il-ink"))
    for i, t in enumerate(("compare the", "front of each", "group, take the", "smaller one")):
        cv.add(cv.text(713, 372 + i * 20, t, 12.5, 650, cls="il-ink2"))
    cv.add(P.badge(cv, 30, 66, 1), P.badge(cv, 626, 232, 2), P.badge(cv, 30, 450, 3))
    return figure(
        "merge-sort-cards", cv, "Merge sort on eight numbers: divide, then merge",
        "Merge sort drawn as a diamond of numbered cards, read from the top down and then back up. The list of eight numbers, 6 3 8 1 7 2 5 4, is "
        "divided in half again and again: first into two groups of four, then four groups of two, then eight single cards. A single card is already "
        "sorted. Then the groups are merged back together, working upwards. Each merge compares the front card of the two groups and takes the smaller "
        "one every time, so the pairs become 3 6, 1 8, 2 7 and 4 5, then the groups of four become 1 3 6 8 and 2 4 5 7, and finally the whole list is "
        "merged into 1 2 3 4 5 6 7 8.",
        ["Divide the list in half, again and again.",
         "Stop when every group is a single item. One item is already sorted.",
         "Merge groups back together, taking the smaller front item each time, until one sorted list is left."],
        "Merge sort divides until the pieces are trivial, then does all its real work while merging.")


@illustration("insertion-sort-cards")
def _insertion():
    cv = Canvas(800, 500).backdrop()
    cv.add(P.pill(cv, 400, 52, "like sorting playing cards in your hand", "paper", 14, 14, 28, 750))
    steps = [([4], 3, [5, 1, 2], "take 3: it is smaller than 4, so 4 shifts right"), ([3, 4], 5, [1, 2], "take 5: bigger than 4, so it stays where it is"),
             ([3, 4, 5], 1, [2], "take 1: shift 3, 4 and 5 right, then drop it in front"), ([1, 3, 4, 5], 2, [], "take 2: shift 3, 4 and 5 right, drop it after 1"),
             ([1, 2, 3, 4, 5], None, [], "no cards left: the list is sorted")]
    for r, (srt, cur, rest, note) in enumerate(steps):
        y = 94 + r * 78
        x = 40
        if srt:
            cv.add(row(cv, x, y, srt, ["g" if cur is not None else "f"] * len(srt), 50, 46, 56, 21))
        x += len(srt) * 56 + 14
        if cur is not None:
            cv.add(cv.rect(x - 9, y - 6, 3, 58, 1.5, "#8AA0AC"))
            cv.add(num_tile(cv, x, y - 8, cur, 50, 46, "sun", 21))
            cv.add(cv.shadow(x + 25, y + 52, 26, 3, .2))
            x += 64
        if rest:
            cv.add(row(cv, x, y, rest, ["x"] * len(rest), 50, 46, 56, 21))
        cv.add(cv.text(430, y + 29, note, 13.5, 700, anchor="start", cls="il-ink"))
    cv.add(P.badge(cv, 22, 94, 1), P.badge(cv, 418, 94, 2), P.badge(cv, 418, 250, 3), P.badge(cv, 418, 406, 4))
    return figure(
        "insertion-sort-cards", cv, "Insertion sort on 4, 3, 5, 1, 2",
        "Insertion sort drawn as sorting playing cards in your hand. The sorted cards, in green, sit on the left and the unsorted cards, in grey, on "
        "the right, with the card currently being placed lifted up in yellow. Start with just the 4 as the sorted part. Take 3: it is smaller than 4, "
        "so the 4 shifts right and the 3 goes in front. Take 5: it is bigger than 4, so it stays where it is. Take 1: it is smaller than 3, 4 and 5, so "
        "all three shift right and the 1 goes at the front. Take 2: the 3, 4 and 5 shift right and the 2 drops in after the 1. No cards are left, so "
        "the list is sorted.",
        ["The sorted part grows from the left, one card at a time.",
         "Take the next card and slide it back past every larger card.",
         "Larger cards shift one place right to make room.",
         "When no cards are left, the whole list is sorted."],
        "Insertion sort is quick on lists that are nearly sorted already, and simple to write.")


# ------------------------------------------------------- complexity, graphs

@illustration("big-o-growth")
def _bigo():
    cv = Canvas(800, 500).backdrop()
    cv.add(P.card(cv, 14, 34, 468, 446, 20, "How the work grows with the input", "teal"))
    X0, Y0, PW, PH = 72, 430, 376, 330
    cv.add(cv.line(X0, Y0, X0 + PW, Y0, "#4A6470", 2.5), cv.line(X0, Y0, X0, Y0 - PH, "#4A6470", 2.5))
    cv.add(cv.text(X0 + PW / 2, 462, "size of the input, n", 13, 700, cls="il-ink2"), cv.text(40, 270, "work", 13, 700, cls="il-ink2"))
    for g in range(1, 5):
        cv.add(cv.line(X0, Y0 - g * PH / 4, X0 + PW, Y0 - g * PH / 4, "var(--il-line)", 1.2))
    top = 40.0          # the chart stops at 40 units of work, so the steep curves leave through the top
    curves = [("O(1)", "green", lambda n: 1.0), ("O(log n)", "teal", lambda n: math.log2(n)), ("O(n)", "sky", lambda n: n),
              ("O(n log n)", "sun", lambda n: n * math.log2(n)), ("O(n²)", "coral", lambda n: n * n), ("O(2ⁿ)", "plum", lambda n: 2 ** n)]
    for name, col, f in curves:
        pts = []
        for i in range(0, 91):
            n = 1 + i * .1
            v = f(n)
            if v > top:
                pts.append((X0 + (n - 1) / 9.0 * PW, Y0 - PH))
                break
            pts.append((X0 + (n - 1) / 9.0 * PW, Y0 - v / top * PH))
        d = "M" + " L".join("%s %s" % (_n(a), _n(b)) for a, b in pts)
        cv.add(cv.path(d, stroke=PAL[col][2] if col in ("sun", "green") else PAL[col][1], sw=5))
    cv.add(P.badge(cv, 30, 36, 1))
    # in words
    cv.add(P.card(cv, 498, 34, 288, 446, 20, "What each one feels like", "coral"))
    words = [("O(1)", "green", "open the first page"), ("O(log n)", "teal", "halve a phone book, again and again"), ("O(n)", "sky", "read every page"),
             ("O(n log n)", "sun", "merge sort a pile of cards"), ("O(n²)", "coral", "compare every pair of people"), ("O(2ⁿ)", "plum", "try every combination")]
    for i, (n, col, d) in enumerate(words):
        y = 84 + i * 64
        cv.add(P.lift(cv, 514, y, 92, 34, col, 10, 4, hl=False), cv.text(560, y + 23, n, 14, 800, fill=P._on(col), mono=True))
        if len(d) < 22:
            cv.add(cv.text(616, y + 22, d, 12, 700, anchor="start", cls="il-ink"))
        else:
            cut = d.rfind(" ", 0, 21)
            cv.add(cv.text(616, y + 14, d[:cut], 12, 700, anchor="start", cls="il-ink"), cv.text(616, y + 30, d[cut + 1:], 12, 700, anchor="start", cls="il-ink"))
    cv.add(P.badge(cv, 514, 36, 2))
    cv.add(P.pill(cv, 642, 464, "it counts steps, not seconds", "paper", 12.5, 12, 24, 750))
    return figure(
        "big-o-growth", cv, "Big O: how the work grows as the input grows",
        "A chart of the six common growth rates, with the size of the input along the bottom and the amount of work up the side. O of 1 is a flat line: "
        "the work does not depend on the size of the input. O of log n rises very slowly. O of n is a straight line: double the input and you double the "
        "work. O of n log n is slightly steeper than that. O of n squared curves up sharply and O of 2 to the n shoots off the top of the chart almost at "
        "once. A panel on the right gives each one a feel: O of 1 is opening the first page, O of log n is halving a phone book again and again, O of n is "
        "reading every page, O of n log n is merge sorting a pile of cards, O of n squared is comparing every pair of people, and O of 2 to the n is "
        "trying every combination. Big O counts steps, not seconds, and describes how the work grows, not how long a particular run takes.",
        ["Each curve shows how the work grows as the input gets bigger.",
         "From flat, to slow, to straight, to steep, to explosive: O(1), O(log n), O(n), O(n log n), O(n²), O(2ⁿ).",
         ],
        "Big O compares algorithms by how they scale. It ignores the speed of any particular machine.")


@illustration("shortest-path")
def _shortest():
    cv = Canvas(800, 500).backdrop()
    cv.add(P.card(cv, 14, 34, 520, 446, 20, "Shortest path from A to F", "teal"))
    N = {"A": (70, 250), "B": (190, 130), "C": (190, 370), "D": (340, 250), "E": (430, 380), "F": (480, 130)}
    # Dijkstra's answer: A-C-B-D-E-F = 2 + 1 + 5 + 2 + 3 = 13
    E = [("A", "B", 4), ("A", "C", 2), ("B", "C", 1), ("B", "D", 5), ("C", "D", 8), ("C", "E", 10), ("D", "E", 2), ("D", "F", 6), ("E", "F", 3)]
    best = {("A", "C"), ("B", "C"), ("B", "D"), ("D", "E"), ("E", "F")}
    for a, b, w in E:
        (x1, y1), (x2, y2) = N[a], N[b]
        on = (a, b) in best or (b, a) in best
        cv.add(P.cable(cv, "M%d %d L%d %d" % (x1, y1, x2, y2), "coral" if on else "slate", 9 if on else 5))
    for a, b, w in E:
        (x1, y1), (x2, y2) = N[a], N[b]
        on = (a, b) in best or (b, a) in best
        cv.add(P.pill(cv, (x1 + x2) / 2, (y1 + y2) / 2, str(w), "coral" if on else "paper", 13, 8, 22, 800))
    dist = {"A": 0, "B": 3, "C": 2, "D": 8, "E": 10, "F": 13}
    for n, (x, y) in N.items():
        cv.add(cv.shadow(x, y + 30, 24, 4, .22) + cv.circle(x, y + 4, 26, PAL["navy" if n in "AF" else "sky"][2]) + cv.circle(x, y, 26, cv.g("navy" if n in "AF" else "sky")))
        cv.add(cv.text(x, y + 7, n, 20, 800, fill="#FFFFFF" if n in "AF" else INK))
    cv.add(P.pill(cv, 70, 296, "start", "paper", 12, 8, 20, 800), P.pill(cv, 480, 176, "finish", "paper", 12, 8, 20, 800))
    cv.add(P.pill(cv, 275, 464, "shortest: A, C, B, D, E, F = 2 + 1 + 5 + 2 + 3 = 13", "coral", 12.5, 12, 24, 800))
    cv.add(P.badge(cv, 30, 36, 1), P.badge(cv, 134, 336, 2))
    # the working
    cv.add(P.card(cv, 550, 34, 236, 446, 20, "The working", "plum"))
    cv.add(cv.rect(566, 76, 204, 26, 7, cv.g("plum")))
    for xx, t in ((578, "node"), (640, "distance"), (722, "via")):
        cv.add(cv.text(xx if t != "via" else 724, 94, t, 12.5, 800, anchor="start" if t != "via" else "middle", fill=P._on("plum")))
    order = [("A", "0", "-"), ("C", "2", "A"), ("B", "3", "C"), ("D", "8", "B"), ("E", "10", "D"), ("F", "13", "E")]
    for i, (n, d, v) in enumerate(order):
        y = 110 + i * 38
        cv.add(cv.rect(566, y, 204, 32, 7, "#FFFFFF" if n != "F" else "#FFE3DD", stroke="#DCE6EC", sw=1))
        cv.add(cv.text(582, y + 22, n, 15, 800, anchor="start", fill=INK, mono=True), cv.text(650, y + 22, d, 15, 800, fill=INK, mono=True), cv.text(724, y + 22, v, 15, 800, fill=INK, mono=True))
    cv.add(cv.text(668, 360, "visited in this order:", 12.5, 700, cls="il-ink2"))
    cv.add(cv.text(668, 382, "A, C, B, D, E, F", 15, 800, cls="il-ink", mono=True))
    cv.add(P.pill(cv, 668, 424, "always visit the unvisited", "sun", 12, 10, 22, 800), P.pill(cv, 668, 450, "node nearest to the start", "sun", 12, 10, 22, 800))
    cv.add(P.badge(cv, 566, 36, 3), P.badge(cv, 566, 424, 4))
    return figure(
        "shortest-path", cv, "Dijkstra's algorithm finding the shortest path from A to F",
        "A weighted graph of six nodes, A to F, with the weight of each edge written on it, and the shortest path from A to F picked out in coral. "
        "Dijkstra's algorithm starts at A with a distance of 0 and every other node at infinity. It repeatedly visits the unvisited node that is nearest "
        "to the start and updates its neighbours if the route through it is shorter. It visits A, then C at distance 2, then B at 3, then D at 8, then "
        "E at 10 and finally F at 13. The working table records each node's distance and the node it was reached via, and reading the via column back "
        "from F gives the path: F from E, E from D, D from B, B from C and C from A. So the shortest path is A, C, B, D, E, F with a total weight of "
        "2 plus 1 plus 5 plus 2 plus 3, which is 13. The direct looking route through the heavy edge from C to E would cost 15.",
        ["A weighted graph: each edge has a cost, such as a distance or a time.",
         "The shortest route is not always the one with the fewest edges: here it takes five edges to save two units.",
         "The working table holds each node's best distance so far and the node it came via.",
         "Always visit the unvisited node nearest the start, then update its neighbours. Read the route back through the via column."],
        "Dijkstra gives the cheapest route to every node. Show the table, not just the answer.")


@illustration("graph-traversal")
def _traversal():
    cv = Canvas(800, 500).backdrop()
    pos = {"A": (190, 92), "B": (80, 190), "C": (190, 190), "D": (300, 190), "E": (44, 288), "F": (116, 288), "G": (190, 288), "H": (264, 288), "I": (336, 288)}
    tree = [("A", "B"), ("A", "C"), ("A", "D"), ("B", "E"), ("B", "F"), ("C", "G"), ("D", "H"), ("D", "I")]
    bfs = ["A", "B", "C", "D", "E", "F", "G", "H", "I"]
    dfs = ["A", "B", "E", "F", "C", "G", "D", "H", "I"]
    for t, col, x0, order in (("Breadth first", "sky", 14, bfs), ("Depth first", "coral", 406, dfs)):
        cv.add(P.card(cv, x0, 34, 380, 446, 20, t, col))
        for a, b in tree:
            (x1, y1), (x2, y2) = pos[a], pos[b]
            cv.add(P.cable(cv, "M%d %d L%d %d" % (x1 + x0 + 4, y1 + 36, x2 + x0 + 4, y2 + 36), "slate", 5))
        for n, (x, y) in pos.items():
            k = order.index(n) + 1
            cv.add(cv.circle(x + x0 + 4, y + 36 + 4, 22, PAL[col][2]) + cv.circle(x + x0 + 4, y + 36, 22, cv.g(col)))
            cv.add(cv.text(x + x0 + 4, y + 43, n, 18, 800, fill=P._on(col)))
            cv.add(cv.circle(x + x0 + 22, y + 36 - 18, 10, "#FFFFFF", stroke=PAL[col][2], sw=1.8), cv.text(x + x0 + 22, y + 36 - 13.5, str(k), 12.5, 800, fill=INK))
    # the structure each one uses
    cv.add(cv.text(204, 388, "visits level by level", 13.5, 800, cls="il-ink"), cv.text(204, 408, "uses a queue: first in, first out", 12.5, 650, cls="il-ink2"))
    for i, v in enumerate(("A", "B", "C", "D")):
        cv.add(num_tile(cv, 56 + i * 54, 428, v, 46, 34, "sky", 16))
    cv.add(P.arrow(cv, [(280, 445), (330, 445)], PAL["sky"][2], 4, 11), cv.text(352, 449, "out", 12.5, 800, anchor="start", cls="il-ink2"))
    cv.add(cv.text(596, 388, "goes as deep as it can first", 13.5, 800, cls="il-ink"), cv.text(596, 408, "uses a stack: last in, first out", 12.5, 650, cls="il-ink2"))
    for i, v in enumerate(("A", "B", "E")):
        cv.add(num_tile(cv, 560, 452 - i * 20, v, 56, 18, "coral", 13))
    cv.add(P.badge(cv, 30, 36, 1), P.badge(cv, 422, 36, 2))
    return figure(
        "graph-traversal", cv, "Breadth first and depth first traversal of the same tree",
        "The same tree of nine nodes, A to I, traversed two ways, with each node numbered in the order it is visited. Breadth first visits level by "
        "level: A, then its children B, C and D, then their children E, F, G, H and I. It uses a queue, first in first out, so the nodes found earliest "
        "are explored earliest. Depth first goes as deep as it can before backing up: A, then B, then E, back to B and on to F, back up to A and down "
        "to C, then G, then D, then H and I. It uses a stack, last in first out, or recursion, which uses the call stack. Both visit every node "
        "exactly once, but in a different order.",
        ["Breadth first: visit everything one step away, then everything two steps away, and so on. It uses a queue.",
         "Depth first: follow one branch as far as it goes, then back up and try the next. It uses a stack, or recursion."],
        "Same graph, same nodes. Only the order differs, and the order comes from queue against stack.")
