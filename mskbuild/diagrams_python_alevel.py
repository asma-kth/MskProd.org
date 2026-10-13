"""Diagrams for the A Level Python topics: recursion, structures, graphs and data.

Same rules as diagrams_python.py: every number is produced by running the
algorithm being drawn, and each stage of a stepped figure draws the state at
that moment in a way that never conflicts with its neighbours, so the union of
all stages, which is what a reader without JavaScript sees, is the finished
picture.
"""
import math

from .diagrams import (diagram, TEAL, TEAL_SOFT, LILAC, LILAC_SOFT, WARN,
                       WARN_SOFT, FILL, LINE, MUTED)
from .diagrams_python import rect, cell, tri_up, FILL2, SOFT, INK, PAPER
from .svg import (figure, figure_steps, step, box, text, line, path, circle,
                  chip)


def badge(cx, cy, label, fill=TEAL, ink=PAPER, r=11, size=11):
    """A small filled disc with a number in it, for ordering things."""
    return (circle(cx, cy, r, fill=fill, stroke=fill, w=1)
            + text(cx, cy + size * 0.36, str(label), size, 700, fill=ink))


# ===================================================== recursion: the call stack

@diagram("py-call-stack")
def _call_stack():
    depth = 4
    fx, fw, fh, gap, bottom = 150, 270, 54, 6, 330
    frames = []          # bottom (outermost call) first
    for i in range(depth):
        n = depth - i
        frames.append({"n": n, "y": bottom - fh - i * (fh + gap)})
    returns = {1: "returns 1", 2: "returns 2 × 1 = 2", 3: "returns 3 × 2 = 6", 4: "returns 4 × 6 = 24"}

    base = [text(380, 22, "The call stack while factorial(4) runs", 12, 650, fill=MUTED),
            line(fx - 10, bottom + 4, fx + fw + 10, bottom + 4, stroke=LINE, w=3),
            text(fx + fw / 2, bottom + 22, "bottom of the stack", 9.5, 500, fill=MUTED),
            line(34, bottom - 6, 34, 78, stroke=TEAL, w=2, arrow=True, marker="ah-accent"),
            text(34, 62, "calls push", 10, 700, fill=TEAL),
            line(716, 84, 716, bottom - 6, stroke=LILAC, w=2, arrow=True, marker="ah-alt"),
            text(716, 62, "returns pop", 10, 700, fill=LILAC)]

    def frame(i, lit=None):
        f = frames[i]
        n, y = f["n"], f["y"]
        top = n == 1
        sub = ("n = 1, the base case: no further call" if top
               else "n = %d, waiting for factorial(%d)" % (n, n - 1))
        col = TEAL if lit == "push" else LILAC if lit == "pop" else LINE
        return (box(fx, y, fw, fh, None, fill=TEAL_SOFT if top else FILL, stroke=col if lit else (TEAL if top else LINE), r=8)
                + text(fx + fw / 2, y + 23, "factorial(%d)" % n, 13, 700, mono=True)
                + text(fx + fw / 2, y + 42, sub, 10, 500, fill=MUTED))

    def stage(k):
        """k = 1..4 pushes so far; k = 5..8 pops so far (k - 4)."""
        out = []
        if k <= depth:
            live = range(0, k)
        else:
            live = range(0, depth - (k - depth))
        lit_i = (k - 1) if k <= depth else (depth - (k - depth))
        for i in live:
            lit = None
            if k <= depth and i == k - 1:
                lit = "push"
            out.append(frame(i, lit))
        if k > depth:
            # the frame that was just popped is shown ghosted where it was
            i = depth - (k - depth)
            f = frames[i]
            out.append(rect(fx, f["y"], fw, fh, stroke=LILAC, sw=2, r=8, dash="5 4"))
        for i in range(min(k, depth)):
            out.append(badge(fx - 34, frames[i]["y"] + fh / 2, i + 1))
        popped = max(0, k - depth)
        for p in range(popped):
            i = depth - 1 - p
            f = frames[i]
            out.append(badge(fx + fw + 30, f["y"] + fh / 2, depth + p + 1, fill=LILAC))
            out.append(text(fx + fw + 48, f["y"] + fh / 2 + 4, returns[frames[i]["n"]], 11.5, 700,
                            anchor="start", mono=True, fill=LILAC))
        return "".join(out)

    L = ["factorial(4) is called, so a frame holding its own n is pushed onto the stack.",
         "It cannot answer until factorial(3) has, so factorial(3) is called and its frame goes on top.",
         "factorial(3) needs factorial(2), so a third frame is pushed.",
         "factorial(2) needs factorial(1). That is the base case, and the stack is four frames deep.",
         "The base case needs no more calls. It returns 1, and its frame is popped.",
         "factorial(2) can finish: 2 × 1 = 2. It returns and its frame is popped.",
         "factorial(3) can finish: 3 × 2 = 6. It returns and its frame is popped.",
         "factorial(4) finishes: 4 × 6 = 24. The last frame is popped and the stack is empty."]
    steps = [step(k, stage(k), L[k - 1]) for k in range(1, 9)]
    desc = ("The call stack while factorial of 4 runs. Calling factorial 4 pushes a frame holding "
            "n equals 4. That call needs factorial 3, so a second frame is pushed on top. "
            "Factorial 3 calls factorial 2, which adds a third frame, and factorial 2 calls "
            "factorial 1, the base case, which makes the stack four frames deep. The returns "
            "then happen in reverse: factorial 1 returns 1 and its frame is popped, factorial 2 "
            "returns 2 times 1 which is 2, factorial 3 returns 3 times 2 which is 6, and "
            "factorial 4 returns 4 times 6 which is 24. Each call has its own frame, with its "
            "own n, which is why the stack grows with the depth of the recursion.")
    return figure_steps("py-stack", 760, 372, "".join(base), steps, "The call stack during recursion",
                        desc, "Nothing is returned until the base case is reached, and the answer "
                        "is built on the way back down.", labels=L)


# ===================================================== functional: map, filter, reduce

@diagram("py-map-filter-reduce")
def _mfr():
    body = [text(380, 22, "Three higher order functions, each given a function to apply", 12, 650, fill=MUTED)]
    ox = 500

    def row(y, name, color, soft, inputs, fn, outputs, note, dropped=()):
        o = [text(20, y + 22, name, 14, 750, anchor="start", mono=True, fill=color)]
        for k, v in enumerate(inputs):
            gone = k in dropped
            o.append(cell(110 + k * 40, y, 36, 36, str(v), fill=FILL2 if gone else soft,
                          stroke=SOFT if gone else color, size=12, ink=MUTED if gone else INK, r=6))
            if gone:
                o.append(line(113 + k * 40, y + 4, 143 + k * 40, y + 32, stroke=WARN, w=1.6))
        o.append(path("M%s %s L%s %s" % (110 + len(inputs) * 40 + 8, y + 18, ox - 14, y + 18),
                      stroke=color, w=2, arrow=True,
                      marker="ah-alt" if color == LILAC else "ah-accent" if color == TEAL else "ah"))
        o.append(chip((110 + len(inputs) * 40 + 8 + ox - 14) / 2, y + 18, fn, fill=soft, stroke=color,
                      text_fill=color, size=11))
        for k, v in enumerate(outputs):
            o.append(cell(ox + k * 40, y, 36, 36, str(v), fill=soft, stroke=color, size=12, r=6))
        o.append(text(110, y + 62, note, 10.5, 600, anchor="start", fill=MUTED))
        return "".join(o)

    body.append(row(50, "map", TEAL, TEAL_SOFT, [1, 2, 3, 4], "n * n", [1, 4, 9, 16],
                    "applies the function to every item: the same length comes out"))
    body.append(row(150, "filter", LILAC, LILAC_SOFT, [1, 2, 3, 4, 5, 6], "n % 2 == 0", [2, 4, 6],
                    "keeps the items for which the function is True: the same or fewer come out",
                    dropped=(0, 2, 4)))
    # reduce, with its running total
    y = 250
    o = [text(20, y + 22, "reduce", 14, 750, anchor="start", mono=True, fill=WARN)]
    for k, v in enumerate([1, 2, 3, 4]):
        o.append(cell(110 + k * 40, y, 36, 36, str(v), fill=WARN_SOFT, stroke=WARN, size=12, r=6))
    o.append(path("M278 %s L%s %s" % (y + 18, ox - 14, y + 18), stroke=WARN, w=2, arrow=True))
    o.append(chip((278 + ox - 14) / 2, y + 18, "a + b", fill=WARN_SOFT, stroke=WARN, text_fill=WARN, size=11))
    o.append(cell(ox, y, 36, 36, "10", fill=WARN_SOFT, stroke=WARN, size=12, r=6))
    for k, txt in enumerate(["1 + 2 = 3", "3 + 3 = 6", "6 + 4 = 10"]):
        o.append(text(110 + k * 100, y + 62, txt, 10.5, 650, anchor="start", mono=True, fill=WARN))
    o.append(text(110, y + 84, "combines the items two at a time into one value", 10.5, 600, anchor="start", fill=MUTED))
    body.append("".join(o))
    desc = ("Three higher order functions. Map applies the function n times n to every item of "
            "1, 2, 3, 4 and gives 1, 4, 9, 16, a list of the same length. Filter applies the test "
            "n mod 2 equals 0 to 1 to 6 and keeps only 2, 4 and 6. Reduce combines 1, 2, 3, 4 "
            "with a plus b, two at a time: 1 plus 2 is 3, 3 plus 3 is 6, 6 plus 4 is 10, so it "
            "returns the single value 10.")
    return figure("py-mfr", 760, 350, "".join(body), "Map, filter and reduce", desc,
                  "Each takes a function as an argument. That is what makes them higher order.")


# ===================================================== OOP: a UML class diagram

@diagram("py-uml-class")
def _uml():
    def klass(x, y, w, name, attrs, methods, abstract=False, tone=TEAL, soft=TEAL_SOFT):
        h1 = 38 if abstract else 28
        h2 = 22 + 17 * len(attrs)
        h3 = 12 + 17 * len(methods)
        o = [rect(x, y, w, h1 + h2 + h3, fill=FILL, stroke=tone, sw=1.6, r=6),
             rect(x, y, w, h1, fill=soft, stroke=tone, sw=1.6, r=6),
             line(x, y + h1 + h2, x + w, y + h1 + h2, stroke=tone, w=1.4)]
        if abstract:
            o.append(text(x + w / 2, y + 14, "«abstract»", 9.5, 500, fill=MUTED))
            o.append(text(x + w / 2, y + 30, name, 12.5, 700, fill=tone))
        else:
            o.append(text(x + w / 2, y + 19, name, 12.5, 700, fill=tone))
        for i, a in enumerate(attrs):
            o.append(text(x + 10, y + h1 + 20 + i * 17, a, 10.5, 500, anchor="start", mono=True))
        for i, m in enumerate(methods):
            o.append(text(x + 10, y + h1 + h2 + 20 + i * 17, m, 10.5, 500, anchor="start", mono=True))
        return "".join(o), h1 + h2 + h3

    body = [text(380, 20, "Inheritance, drawn as a UML class diagram", 12, 650, fill=MUTED)]
    shape, hs = klass(270, 36, 220, "Shape", ["# name: str"], ["+ area(): float", "+ describe(): str"], abstract=True)
    body.append(shape)
    circle_, hc = klass(70, 206, 220, "Circle", ["- radius: float"], ["+ area(): float"], tone=LILAC, soft=LILAC_SOFT)
    rect_, hr = klass(470, 206, 220, "Rectangle", ["- width: float", "- height: float"], ["+ area(): float"],
                      tone=LILAC, soft=LILAC_SOFT)
    body.append(circle_)
    body.append(rect_)
    # one hollow triangle at the parent, and a line that forks to each child
    top = 36 + hs
    body.append(path("M380 %s L370 %s L390 %s Z" % (top, top + 16, top + 16), stroke=INK, w=1.6, fill=PAPER))
    body.append(line(380, top + 16, 380, 184, stroke=INK, w=1.6))
    body.append(line(180, 184, 580, 184, stroke=INK, w=1.6))
    body.append(line(180, 184, 180, 206, stroke=INK, w=1.6))
    body.append(line(580, 184, 580, 206, stroke=INK, w=1.6))
    body.append(text(396, 178, "is a", 10, 700, anchor="start", fill=MUTED))

    # the other three relationships
    y = 340
    body.append(line(24, y - 18, 736, y - 18, stroke=SOFT, w=1))
    def pair(x, a, b, kind, caption):
        o = [box(x, y, 70, 34, a, fill=FILL, stroke=LINE, r=4, label_size=12),
             box(x + 130, y, 70, 34, b, fill=FILL, stroke=LINE, r=4, label_size=12)]
        mid = y + 17
        if kind in ("comp", "agg"):
            d = "M%s %s L%s %s L%s %s L%s %s Z" % (x + 70, mid, x + 82, mid - 6, x + 94, mid, x + 82, mid + 6)
            o.append(path(d, stroke=INK, w=1.6, fill=INK if kind == "comp" else PAPER))
            o.append(line(x + 94, mid, x + 130, mid, stroke=INK, w=1.6))
        else:
            o.append(line(x + 70, mid, x + 130, mid, stroke=INK, w=1.6, arrow=True))
        o.append(text(x + 100, y + 56, caption[0], 10.5, 700, fill=TEAL))
        o.append(text(x + 100, y + 72, caption[1], 9.5, 500, fill=MUTED))
        return "".join(o)
    body.append(pair(30, "Car", "Engine", "comp", ("Composition", "the car owns its engine")))
    body.append(pair(280, "Team", "Player", "agg", ("Aggregation", "players exist without the team")))
    body.append(pair(530, "Teacher", "Student", "assoc", ("Association", "one uses the other")))
    desc = ("A UML class diagram. An abstract class Shape has a protected attribute name and the "
            "public methods area and describe. Two classes, Circle, with a private radius, and "
            "Rectangle, with a private width and height, each inherit from Shape, shown by a "
            "hollow triangle at Shape's end of the line, and each has its own area method. "
            "Below are the three other relationships. Composition, a filled diamond, joins Car to "
            "Engine because the car owns its engine. Aggregation, a hollow diamond, joins Team "
            "to Player because the players exist without the team. Association, a plain arrow, "
            "joins Teacher to Student because one uses the other.")
    return figure("py-uml", 760, 428, "".join(body), "A UML class diagram", desc,
                  "A plus is public, a minus is private and a hash is protected.")


# ===================================================== queues: the circular queue

@diagram("py-circular-queue")
def _circular_queue():
    cx0, cw, ch = 220, 62, 38
    rows = [("enqueue A, B, C, D", ["A", "B", "C", "D"], 0, 3, 4, "full: count = 4"),
            ("dequeue twice: A and B leave", ["", "", "C", "D"], 2, 3, 2, "count = 2"),
            ("enqueue E", ["E", "", "C", "D"], 2, 0, 3, "rear = (3 + 1) MOD 4 = 0: it wraps round"),
            ("enqueue F", ["E", "F", "C", "D"], 2, 1, 4, "full again: count = 4")]
    base = [text(380, 20, "A circular queue held in an array of four places", 12, 650, fill=MUTED)]
    ys = [52 + r * 108 for r in range(4)]
    for r, (label, vals, front, rear, count, note) in enumerate(rows):
        y = ys[r]
        base.append(text(14, y + 16, label, 10.5, 650, anchor="start"))
        base.append(text(14, y + 32, "step %d" % (r + 1), 9.5, 500, anchor="start", fill=MUTED))
        for i, v in enumerate(vals):
            base.append(cell(cx0 + i * cw, y, cw, ch, v, fill=TEAL_SOFT if v else FILL,
                             stroke=TEAL if v else LINE, size=14, r=4))
            base.append(text(cx0 + i * cw + cw / 2, y - 5, str(i), 9, 500, fill=MUTED, mono=True))
        # pointers sit under their cells, side by side when they share one
        fx = cx0 + front * cw + cw / 2 - (16 if front == rear else 0)
        rx = cx0 + rear * cw + cw / 2 + (16 if front == rear else 0)
        base.append(tri_up(fx, y + ch + 3, 8, fill=WARN))
        base.append(text(fx, y + ch + 25, "front", 9.5, 700, fill=WARN))
        base.append(tri_up(rx, y + ch + 3, 8, fill=LILAC))
        base.append(text(rx, y + ch + 25, "rear", 9.5, 700, fill=LILAC))
        base.append(text(cx0 + 4 * cw + 18, y + 14, note, 10.5, 600, anchor="start",
                         fill=LILAC if "wraps" in note else INK))
    # the wrap, drawn on step 3
    wy = ys[2]
    wrap = path("M%s %s C %s %s, %s %s, %s %s" % (cx0 + 3.5 * cw, wy - 16, cx0 + 3.2 * cw, wy - 44,
                                                   cx0 + 0.8 * cw, wy - 44, cx0 + 0.5 * cw, wy - 16),
                stroke=LILAC, w=2.2, arrow=True, marker="ah-alt")
    wrap += text(cx0 + 1.9 * cw, wy - 27, "wraps round", 10, 700, fill=LILAC)
    def hl(r):
        return rect(8, ys[r] - 18, 744, 82, stroke=TEAL, sw=2.4, r=8)
    L = ["Four items are added. The rear pointer has reached the last place and the queue is full.",
         "Two items leave from the front, so front moves up to position 2. Places 0 and 1 are free.",
         "Adding E: the next place after position 3 is (3 + 1) MOD 4, which is 0. The pointer wraps to the start.",
         "Adding F fills position 1. The queue spans the end of the array and the start of it."]
    steps = [step(1, hl(0), L[0]), step(2, hl(1), L[1]), step(3, hl(2) + wrap, L[2]), step(4, hl(3), L[3])]
    desc = ("A circular queue in an array of four places, shown in four stages. First A, B, C "
            "and D are added, so the front pointer is at position 0, the rear pointer at 3, and "
            "the queue is full. Then two items leave from the front, so front moves to position "
            "2 and places 0 and 1 are empty. Adding E puts it at position 0, because the rear "
            "moves to 3 plus 1 mod 4, which is 0: the pointer wraps round to the start of the "
            "array. Adding F fills position 1. Front is at 2 and rear at 1, so the queue holds "
            "C, D, E and F in that order, spanning the end of the array and the start.")
    return figure_steps("py-circq", 760, 470, "".join(base), steps, "A circular queue", desc,
                        "The remainder operator is what turns a row of boxes into a ring.", labels=L)


# ===================================================== linked lists: inserting a node

@diagram("py-linked-list")
def _linked_list():
    nw, pw, nh = 46, 30, 34

    def node(x, y, data, tone=TEAL, soft=TEAL_SOFT):
        return (cell(x, y, nw, nh, str(data), fill=soft, stroke=tone, size=13, r=4)
                + rect(x + nw, y, pw, nh, fill=FILL, stroke=tone, sw=1.5, r=4)
                + circle(x + nw + pw / 2, y + nh / 2, 3.4, fill=tone, stroke=tone, w=1))

    def link(x, y, nx, ny, tone=INK, w=1.7, arrow=True, dash=None):
        return path("M%s %s L%s %s" % (x + nw + pw / 2, y + nh / 2, nx, ny + nh / 2),
                    stroke=tone, w=w, arrow=arrow, dash=dash)

    def head_label(x, y):
        return (box(x, y, 56, nh, "head", fill=WARN_SOFT, stroke=WARN, r=4, label_size=12)
                + path("M%s %s L%s %s" % (x + 56, y + nh / 2, x + 76, y + nh / 2), stroke=WARN, w=1.7, arrow=True))

    def none(x, y):
        return (line(x + nw + pw / 2, y + nh / 2, x + nw + pw + 26, y + nh / 2, stroke=INK, w=1.7)
                + line(x + nw + pw + 26, y + nh / 2 - 8, x + nw + pw + 26, y + nh / 2 + 8, stroke=INK, w=1.7)
                + text(x + nw + pw + 54, y + nh / 2 + 4, "None", 10.5, 600, fill=MUTED, mono=True))

    base = [text(380, 20, "Inserting 30 between 20 and 40: two pointers change, nothing moves", 12, 650, fill=MUTED)]
    # row A: the list as it was
    ya = 50
    xa = [170, 310, 450]
    base.append(text(14, ya + 22, "before", 11, 700, anchor="start", fill=MUTED))
    HX = 70
    base.append(head_label(HX, ya))
    for x, v in zip(xa, [10, 20, 40]):
        base.append(node(x, ya, v))
    base.append(link(xa[0], ya, xa[1], ya))
    base.append(link(xa[1], ya, xa[2], ya))
    base.append(none(xa[2], ya))
    # row B: a new node, pointing at 40
    yb = 150
    base.append(text(14, yb + 22, "during", 11, 700, anchor="start", fill=MUTED))
    # row C: after
    yc = 290
    xc = [170, 290, 410, 530]
    base.append(text(14, yc + 22, "after", 11, 700, anchor="start", fill=MUTED))
    base.append(head_label(HX, yc))
    for x, v in zip(xc, [10, 20, 30, 40]):
        base.append(node(x, yc, v, LILAC if v == 30 else TEAL, LILAC_SOFT if v == 30 else TEAL_SOFT))
    base.append(link(xc[0], yc, xc[1], yc))
    base.append(link(xc[1], yc, xc[2], yc, tone=LILAC, w=2.4))
    base.append(link(xc[2], yc, xc[3], yc, tone=LILAC, w=2.4))
    base.append(none(xc[3], yc))
    # the stages
    s1 = ""
    for x, v in zip(xa, [10, 20, 40]):
        s1 += node(x, yb, v)
    s1 += link(xa[0], yb, xa[1], yb) + link(xa[1], yb, xa[2], yb) + none(xa[2], yb)
    s1 += head_label(HX, yb)
    newx, newy = 360, yb + 62
    s1 += node(newx, newy, 30, LILAC, LILAC_SOFT)
    s1 += path("M%s %s C %s %s, %s %s, %s %s" % (newx + nw + pw / 2, newy + nh / 2, newx + nw + pw + 40, newy + nh / 2,
                                                  xa[2] + nw / 2, yb + nh + 40, xa[2] + nw / 2, yb + nh + 2),
               stroke=LILAC, w=2.4, arrow=True, marker="ah-alt")
    s1 += text(newx - 8, newy + nh / 2 + 4, "new.next = 20.next", 10.5, 700, anchor="end", fill=LILAC, mono=True)
    cut_x = (xa[1] + nw + pw + xa[2]) / 2
    s2 = (line(cut_x - 7, yb + nh / 2 - 9, cut_x + 7, yb + nh / 2 + 9, stroke=WARN, w=2.6)
          + line(cut_x + 7, yb + nh / 2 - 9, cut_x - 7, yb + nh / 2 + 9, stroke=WARN, w=2.6)
          + text(cut_x, yb - 4, "old link replaced", 10, 700, fill=WARN)
          + text(xa[1] + nw + pw - 6, yb + nh + 22, "20.next = new", 10.5, 700, anchor="end", fill=TEAL, mono=True))
    s2 += path("M%s %s L%s %s" % (xa[1] + nw + pw / 2, yb + nh / 2, newx + nw / 2 - 6, newy - 2),
               stroke=TEAL, w=2.4, arrow=True, marker="ah-accent")
    L = ["Start with the list 10, 20, 40. The head pointer leads to the first node.",
         "Make the new node, 30, and point it at whatever 20 pointed at: the node 40.",
         "Now point 20 at the new node. The old link from 20 to 40 is replaced, and the list is 10, 20, 30, 40."]
    steps = [step(1, "", L[0]), step(2, s1, L[1]), step(3, s1 + s2, L[2])]
    desc = ("Inserting the value 30 into a linked list holding 10, 20 and 40, between 20 and 40. "
            "Before: the head pointer leads to the node 10, which points to 20, which points to "
            "40, whose pointer is None. Step one: a new node holding 30 is made, and its pointer "
            "is set to the node 40, which is what 20 currently points at. Step two: the pointer "
            "of 20 is changed to point at the new node. After: the list reads 10, 20, 30, 40. "
            "Only two pointers were changed and no node was moved. The order of the two steps "
            "matters: if 20 were changed first, the only pointer to 40 would be lost.")
    return figure_steps("py-llist", 760, 346, "".join(base), steps, "Inserting into a linked list",
                        desc, "Point the new node onward first, then point the old node at it. "
                        "The other way round loses the rest of the list.", labels=L)


# ===================================================== hash tables

@diagram("py-hash-table")
def _hash_table():
    names = ["Asha", "Ben", "Chloe", "Dev", "Esme"]
    size = 5
    index = {n: sum(ord(ch) for ch in n) % size for n in names}
    chains = {i: [n for n in names if index[n] == i] for i in range(size)}
    kx, ky = 24, 54
    slot_x, slot_y = 450, 54
    colors = {1: (WARN, WARN_SOFT), 2: (LILAC, LILAC_SOFT)}

    body = [text(380, 20, "A hash table of five slots, with chaining", 12, 650, fill=MUTED)]
    # hash function bar
    body.append(rect(220, 40, 96, 270, fill=FILL2, stroke=LINE, sw=1.6, r=10))
    body.append(text(268, 70, "hash", 12, 750, mono=True, fill=INK))
    body.append(text(268, 90, "add the", 10, 500, fill=MUTED))
    body.append(text(268, 104, "letter codes,", 10, 500, fill=MUTED))
    body.append(text(268, 118, "then MOD 5", 10, 500, fill=MUTED))
    for k, n in enumerate(names):
        y = ky + k * 52
        tone, soft = colors.get(index[n], (TEAL, TEAL_SOFT))
        body.append(box(kx, y, 90, 34, n, fill=soft, stroke=tone, r=6, label_size=12.5))
        body.append(path("M%s %s L%s %s" % (kx + 90, y + 17, 220, y + 17), stroke=tone, w=1.8, arrow=True))
        ty = slot_y + index[n] * 52
        body.append(path("M316 %s C 360 %s, 380 %s, %s %s" % (y + 17 if False else 150 + k * 22, 150 + k * 22, ty + 17,
                                                             slot_x - 4, ty + 17),
                         stroke=tone, w=1.8, arrow=True, marker="ah-alt" if tone == LILAC else "ah"))
        body.append(chip(352, 150 + k * 22 if False else 0, "", fill=PAPER, stroke=PAPER)) if False else None
    for i in range(size):
        y = slot_y + i * 52
        tone, soft = colors.get(i, (LINE, FILL))
        body.append(cell(slot_x, y, 50, 34, str(i), fill=FILL2, stroke=LINE, size=13, weight=700, r=4))
        for c, n in enumerate(chains[i]):
            nx = slot_x + 66 + c * 92
            body.append(path("M%s %s L%s %s" % (nx - 16 if c else slot_x + 50, y + 17, nx, y + 17), stroke=INK, w=1.6, arrow=True))
            body.append(box(nx, y, 76, 34, n, fill=soft if i in colors else TEAL_SOFT,
                            stroke=tone if i in colors else TEAL, r=6, label_size=12))
        if len(chains[i]) > 1:
            body.append(text(slot_x + 66 + len(chains[i]) * 92 - 6, y + 21, "collision", 10, 700,
                             anchor="start", fill=tone))
        if not chains[i]:
            body.append(text(slot_x + 66, y + 21, "empty", 10, 500, anchor="start", fill=MUTED))
    body.append(text(380, 330, "Asha and Chloe hash to the same slot, and so do Ben and Dev. Each "
                     "slot holds a list, so nothing is lost.", 10.5, 600, fill=MUTED))
    mapping = ", ".join("%s to slot %d" % (n, index[n]) for n in names)
    desc = ("A hash table with five slots, numbered 0 to 4, using chaining to handle collisions. "
            "The hash function adds the character codes of the letters in the key and takes the "
            "remainder when divided by 5. This sends %s. Slot 1 holds Asha and Chloe, and slot "
            "2 holds Ben and Dev, so those are collisions, and each slot keeps a list of the "
            "records that share it. Slots 0 and 3 are empty." % mapping)
    return figure("py-hash", 760, 350, "".join(body), "A hash table with chaining", desc,
                  "The same key always lands in the same slot, so a lookup repeats the calculation.")


# ===================================================== trees: a binary search tree

@diagram("py-bst")
def _bst():
    # Built by inserting the values in this order, so the shape is the real one.
    order = [50, 30, 70, 20, 40, 60, 80, 35]
    nodes = {}

    def insert(root, v):
        if root is None:
            return {"v": v, "l": None, "r": None}
        if v < root["v"]:
            root["l"] = insert(root["l"], v)
        else:
            root["r"] = insert(root["r"], v)
        return root
    root = None
    for v in order:
        root = insert(root, v)
    # lay out by in-order position, so the tree is never drawn crossing itself
    pos = {}
    counter = [0]

    def place(node, depth):
        if node is None:
            return
        place(node["l"], depth + 1)
        pos[node["v"]] = (0, depth)
        node["slot"] = counter[0]
        counter[0] += 1
        place(node["r"], depth + 1)
    place(root, 0)
    # x from the in-order slot, y from the depth
    def walk(node, depth, out):
        if node is None:
            return
        walk(node["l"], depth + 1, out)
        out[node["v"]] = (70 + node["slot"] * 80, 56 + depth * 70)
        walk(node["r"], depth + 1, out)
    xy = {}
    walk(root, 0, xy)

    body = [text(380, 20, "A binary search tree, built by inserting 50, 30, 70, 20, 40, 60, 80, 35", 12, 650, fill=MUTED)]
    edges = []

    def collect(node):
        if node is None:
            return
        for side in ("l", "r"):
            if node[side]:
                edges.append((node["v"], node[side]["v"]))
                collect(node[side])
    collect(root)
    path_ = [50, 30, 40, 35]
    on_path = {(path_[i], path_[i + 1]) for i in range(len(path_) - 1)}
    for a, b in edges:
        (x1, y1), (x2, y2) = xy[a], xy[b]
        hit = (a, b) in on_path
        body.append(line(x1, y1 + 19, x2, y2 - 19, stroke=TEAL if hit else LINE, w=3 if hit else 1.6))
    for v, (x, y) in xy.items():
        hit = v in path_
        body.append(circle(x, y, 20, fill=TEAL_SOFT if hit else FILL, stroke=TEAL if hit else LINE, w=2.4 if hit else 1.6))
        body.append(text(x, y + 4.5, str(v), 13, 700, mono=True, fill=TEAL if hit else INK))
    # decisions along the search path for 35
    notes = {(50, 30): "35 < 50: go left", (30, 40): "35 > 30: go right", (40, 35): "35 < 40: go left"}
    for (a, b), note in notes.items():
        (x1, y1), (x2, y2) = xy[a], xy[b]
        body.append(text((x1 + x2) / 2 + (-6 if x2 < x1 else 6), (y1 + y2) / 2 - 2, note, 9.5, 700,
                         anchor="end" if x2 < x1 else "start", fill=TEAL))
    body.append(text(740, 44, "left is smaller, right is larger", 10.5, 650, anchor="end", fill=MUTED))
    body.append(text(740, 62, "searching for 35 visits 4 of 8 nodes", 10.5, 650, anchor="end", fill=TEAL))
    # the three traversals, calculated
    def pre(n):
        return [] if n is None else [n["v"]] + pre(n["l"]) + pre(n["r"])
    def ino(n):
        return [] if n is None else ino(n["l"]) + [n["v"]] + ino(n["r"])
    def post(n):
        return [] if n is None else post(n["l"]) + post(n["r"]) + [n["v"]]
    for i, (name, seq, tone) in enumerate([("Pre-order", pre(root), INK), ("In-order", ino(root), TEAL),
                                           ("Post-order", post(root), INK)]):
        yy = 306 + i * 22
        body.append(text(30, yy, name, 10.5, 700, anchor="start", fill=tone))
        body.append(text(130, yy, "  ".join(str(v) for v in seq), 11, 600 if tone == INK else 750,
                         anchor="start", mono=True, fill=tone))
    body.append(text(350, 328, "sorted!", 11, 750, anchor="start", fill=TEAL))
    desc = ("A binary search tree made by inserting 50, 30, 70, 20, 40, 60, 80 and 35. 50 is the "
            "root. Its left child is 30 and its right child is 70. 30 has children 20 and 40, and "
            "70 has children 60 and 80. 35 is the left child of 40. Everything to the left of any "
            "node is smaller, and everything to the right is larger. A search for 35 goes from "
            "50 to the left to 30, right to 40 and left to 35, visiting four of the eight nodes. "
            "The pre-order traversal is %s. The in-order traversal is %s, which is sorted. The "
            "post-order traversal is %s." % (", ".join(map(str, pre(root))),
                                              ", ".join(map(str, ino(root))),
                                              ", ".join(map(str, post(root)))))
    return figure("py-bst", 760, 372, "".join(body), "A binary search tree", desc,
                  "In-order traversal reads a binary search tree in sorted order.")


# ===================================================== graphs: breadth first against depth first

GRAPH = {"A": ["B", "C"], "B": ["A", "D"], "C": ["A", "D", "E"],
         "D": ["B", "C", "F"], "E": ["C", "F"], "F": ["D", "E"]}
POS = {"A": (50, 56), "B": (170, 56), "C": (50, 136), "D": (170, 136), "F": (290, 136), "E": (170, 212)}


def _bfs_trace():
    visited, queue, rows, parent = ["A"], ["A"], [], {"A": None}
    while queue:
        v = queue.pop(0)
        for n in GRAPH[v]:
            if n not in visited:
                visited.append(n)
                queue.append(n)
                parent[n] = v
        rows.append((v, list(queue)))
    return rows, parent


def _dfs_trace():
    order, parent, rows = [], {}, []

    def go(v, path, par):
        order.append(v)
        parent[v] = par
        rows.append((v, path + [v]))
        for n in GRAPH[v]:
            if n not in order:
                go(n, path + [v], v)
    go("A", [], None)
    return rows, parent


@diagram("py-graph-traversal")
def _graph_traversal():
    bfs_rows, bfs_parent = _bfs_trace()
    dfs_rows, dfs_parent = _dfs_trace()
    panels = [("Breadth first", "a queue", 14, bfs_rows, bfs_parent, "queue", TEAL, TEAL_SOFT),
              ("Depth first", "a stack, or recursion", 394, dfs_rows, dfs_parent, "path", LILAC, LILAC_SOFT)]
    edges = [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"), ("C", "E"), ("D", "F"), ("E", "F")]
    base = []
    for title, uses, ox, rows, parent, col, tone, soft in panels:
        base.append(text(ox + 170, 20, "%s search" % title, 12.5, 750, fill=tone))
        base.append(text(ox + 170, 38, "uses " + uses, 10, 500, fill=MUTED))
        for a, b in edges:
            (x1, y1), (x2, y2) = POS[a], POS[b]
            base.append(line(ox + x1, 20 + y1 + 22, ox + x2, 20 + y2 + 22, stroke=LINE, w=1.6))
        for v, (x, y) in POS.items():
            base.append(circle(ox + x, 20 + y + 22, 17, fill=FILL, stroke=LINE, w=1.6))
            base.append(text(ox + x, 20 + y + 27, v, 13, 700, mono=True))
        # the working table, one row per visit
        ty = 300
        base.append(text(ox + 4, ty, "#", 10.5, 700, anchor="start", fill=MUTED, mono=True))
        base.append(text(ox + 30, ty, "visit", 10.5, 700, anchor="start", fill=MUTED, mono=True))
        base.append(text(ox + 80, ty, "queue after it" if col == "queue" else "path to it", 10.5, 700,
                         anchor="start", fill=MUTED, mono=True))
        base.append(line(ox, ty + 8, ox + 350, ty + 8, stroke=SOFT, w=1))
        for k, (v, c) in enumerate(rows):
            y = ty + 28 + k * 24
            base.append(text(ox + 4, y, str(k + 1), 11, 700, anchor="start", fill=tone, mono=True))
            base.append(text(ox + 30, y, v, 11.5, 700, anchor="start", mono=True))
            base.append(text(ox + 80, y, "[" + ", ".join(c) + "]", 11, 500, anchor="start", mono=True))

    def stage(k):
        out = []
        for title, uses, ox, rows, parent, col, tone, soft in panels:
            for i in range(k):
                v = rows[i][0]
                p_ = parent[v]
                if p_:
                    (x1, y1), (x2, y2) = POS[p_], POS[v]
                    out.append(line(ox + x1, 20 + y1 + 22, ox + x2, 20 + y2 + 22, stroke=tone, w=3.4))
            for i in range(k):
                v = rows[i][0]
                x, y = POS[v]
                out.append(circle(ox + x, 20 + y + 22, 17, fill=soft, stroke=tone, w=2.4))
                out.append(text(ox + x, 20 + y + 27, v, 13, 700, mono=True, fill=tone))
                out.append(badge(ox + x + 15, 20 + y + 22 - 15, i + 1, fill=tone, r=9, size=10))
            out.append(rect(ox - 4, 300 + 28 + (k - 1) * 24 - 16, 358, 22, stroke=tone, sw=2.2, r=5))
        return "".join(out)

    L = []
    for k in range(6):
        L.append("Visit %d: breadth first goes to %s, taken from the front of the queue. Depth first goes to %s, "
                 "following one path as deep as it can." % (k + 1, bfs_rows[k][0], dfs_rows[k][0]))
    steps = [step(k + 1, stage(k + 1), L[k]) for k in range(6)]
    desc = ("The same six vertex graph searched two ways from A. The edges are A to B, A to C, B to "
            "D, C to D, C to E, D to F and E to F. Breadth first search uses a queue and visits "
            "%s, finishing each ring of neighbours before the next. Depth first search uses a "
            "stack or recursion and visits %s, following one path as far as it will go before "
            "backing up." % (", ".join(r[0] for r in bfs_rows), ", ".join(r[0] for r in dfs_rows)))
    return figure_steps("py-graph", 760, 470, "".join(base), steps, "Breadth first and depth first search",
                        desc, "Same graph, same start. The only difference is the data structure that "
                        "decides what is next.", labels=L)


# ===================================================== Dijkstra's algorithm, one vertex at a time

WEIGHTS = {"A": {"B": 7, "C": 9, "F": 14}, "B": {"A": 7, "C": 10, "D": 15},
           "C": {"A": 9, "B": 10, "D": 11, "F": 2}, "D": {"B": 15, "C": 11, "E": 6},
           "E": {"D": 6, "F": 9}, "F": {"A": 14, "C": 2, "E": 9}}
DPOS = {"A": (50, 150), "B": (150, 56), "C": (186, 168), "D": (320, 96), "E": (320, 256), "F": (186, 266)}


def _dijkstra_trace():
    import heapq
    dist = {v: float("inf") for v in WEIGHTS}
    prev = {v: None for v in WEIGHTS}
    dist["A"] = 0
    heap, fixed, rows = [(0, "A")], [], []
    while heap:
        d, v = heapq.heappop(heap)
        if v in fixed:
            continue
        fixed.append(v)
        for n, w in WEIGHTS[v].items():
            if d + w < dist[n]:
                dist[n] = d + w
                prev[n] = v
                heapq.heappush(heap, (dist[n], n))
        rows.append((v, [dist[x] for x in "ABCDEF"]))
    return rows, dist, prev


@diagram("py-dijkstra")
def _dijkstra():
    rows, dist, prev = _dijkstra_trace()
    order = [v for v, _ in rows]
    tx, ty, rh = 428, 52, 28
    widths = [34, 40] + [38] * 6
    cx = [tx + sum(widths[:i]) for i in range(8)]
    base = [text(190, 22, "Weighted graph", 11.5, 700, fill=MUTED),
            text(tx + sum(widths) / 2, 22, "Working table", 11.5, 700, fill=MUTED)]
    seen = set()
    for a, nbrs in WEIGHTS.items():
        for b, w in nbrs.items():
            if (b, a) in seen:
                continue
            seen.add((a, b))
            (x1, y1), (x2, y2) = DPOS[a], DPOS[b]
            base.append(line(x1, y1, x2, y2, stroke=LINE, w=1.6))
            mx, my = (x1 + x2) / 2, (y1 + y2) / 2
            base.append(rect(mx - 11, my - 9, 22, 18, fill=PAPER, r=5))
            base.append(text(mx, my + 4, str(w), 10.5, 700, fill=WARN, mono=True))
    for v, (x, y) in DPOS.items():
        base.append(circle(x, y, 17, fill=FILL, stroke=LINE, w=1.6))
        base.append(text(x, y + 5, v, 13, 700, mono=True))
    heads = ["step", "fixed"] + list("ABCDEF")
    for c, h in enumerate(heads):
        base.append(cell(cx[c], ty, widths[c], rh, h, fill=FILL2, size=10.5, weight=700, ink=MUTED))
    prevrow = [0] + [float("inf")] * 5
    for r, (v, row) in enumerate(rows):
        y = ty + rh * (r + 1)
        base.append(cell(cx[0], y, widths[0], rh, str(r + 1), size=11, weight=700, ink=TEAL))
        base.append(cell(cx[1], y, widths[1], rh, v, size=12, weight=700))
        for c, d in enumerate(row):
            improved = d != prevrow[c] and d != float("inf")
            base.append(cell(cx[2 + c], y, widths[2 + c], rh, "∞" if d == float("inf") else str(d), size=11.5,
                             fill=WARN_SOFT if improved else FILL, stroke=WARN if improved else LINE,
                             ink=WARN if improved else INK, weight=700 if improved else 600))
        prevrow = row
    base.append(text(tx, ty + rh * 8 + 10, "orange: a shorter route was just found", 10, 600, anchor="start", fill=WARN))
    # how the shortest path is read back
    path_to = []
    v = "E"
    while v:
        path_to.append(v)
        v = prev[v]
    path_to.reverse()

    def stage(k):
        out = []
        for i in range(k):
            v = order[i]
            x, y = DPOS[v]
            out.append(circle(x, y, 17, fill=TEAL_SOFT, stroke=TEAL, w=2.6))
            out.append(text(x, y + 5, v, 13, 700, mono=True, fill=TEAL))
            out.append(badge(x + 17, y - 19, rows[i][1]["ABCDEF".index(v)], fill=TEAL, r=11, size=10.5))
        out.append(rect(tx - 3, ty + rh * k - 1, sum(widths) + 6, rh + 2, stroke=TEAL, sw=2.6, r=4))
        if k == len(rows):
            for a, b in zip(path_to, path_to[1:]):
                (x1, y1), (x2, y2) = DPOS[a], DPOS[b]
                out.append(line(x1, y1, x2, y2, stroke=TEAL, w=4.2))
            for a, b in zip(path_to, path_to[1:]):
                (x1, y1), (x2, y2) = DPOS[a], DPOS[b]
                mx, my = (x1 + x2) / 2, (y1 + y2) / 2
                out.append(rect(mx - 11, my - 9, 22, 18, fill=PAPER, stroke=TEAL, sw=1.4, r=5))
                out.append(text(mx, my + 4, str(WEIGHTS[a][b]), 10.5, 700, fill=TEAL, mono=True))
            for v in path_to:
                x, y = DPOS[v]
                out.append(circle(x, y, 17, fill=TEAL_SOFT, stroke=TEAL, w=2.6))
                out.append(text(x, y + 5, v, 13, 700, mono=True, fill=TEAL))
            out.append(text(tx, ty + rh * 8 + 30, "shortest path to E: " + " → ".join(path_to) +
                            "  (total %d)" % dist["E"], 11, 750, anchor="start", fill=TEAL))
        return "".join(out)

    L = []
    for k, (v, row) in enumerate(rows):
        d = row["ABCDEF".index(v)]
        if k == 0:
            L.append("Fix A at distance 0. Its neighbours get provisional distances: B 7, C 9, F 14.")
        else:
            L.append("Fix %s, the nearest vertex not yet fixed, at distance %d. Then see whether it gives its neighbours a shorter route." % (v, d))
    L[2] = L[2] + " Going through C makes D 20 (not 22) and F 11 (not 14)."
    steps = [step(k + 1, stage(k + 1), L[k]) for k in range(len(rows))]
    desc = ("Dijkstra's algorithm on a weighted graph of six vertices, A to F, with the edges A to "
            "B 7, A to C 9, A to F 14, B to C 10, B to D 15, C to D 11, C to F 2, D to E 6 and E "
            "to F 9. Starting at A, the vertices are fixed in the order %s. The working table "
            "gives the best known distance to each vertex after each step, and the final "
            "distances from A are %s. The shortest path from A to E goes %s with a total of %d." %
            (", ".join(order), ", ".join("%s %d" % (v, dist[v]) for v in "ABCDEF"),
             ", ".join(path_to), dist["E"]))
    return figure_steps("py-dijk", 760, 360, "".join(base), steps, "Dijkstra's algorithm", desc,
                        "Always fix the nearest vertex that is not yet fixed. Its distance can never "
                        "be improved after that.", labels=L)


# ===================================================== complexity: how the growth classes diverge

@diagram("py-growth-curves")
def _growth():
    x0, y0, w, h = 78, 300, 560, 250
    xmax, ymax = 12, 120
    curves = [("O(1)", lambda n: 1, MUTED), ("O(log n)", lambda n: math.log2(n) if n >= 1 else 0, TEAL),
              ("O(n)", lambda n: n, INK), ("O(n log n)", lambda n: n * math.log2(n) if n >= 1 else 0, LILAC),
              ("O(n²)", lambda n: n * n, WARN), ("O(2ⁿ)", lambda n: 2 ** n, "var(--dg-link)")]
    from .diagrams_data import axes
    body = [text(380, 20, "Steps taken, as the size of the input grows", 12, 650, fill=MUTED),
            axes(x0, y0, w, h, "input size n", "steps",
                 xticks=[(i / xmax, str(i)) for i in range(0, xmax + 1, 2)],
                 yticks=[(v / ymax, str(v)) for v in range(0, ymax + 1, 20)])]
    for name, fn, col in curves:
        pts = []
        for i in range(0, 241):
            n = xmax * i / 240.0
            v = fn(n)
            if v > ymax:
                # stop where the curve leaves the picture, interpolating onto the top edge
                if pts:
                    pn, pv = pts[-1][2], pts[-1][3]
                    t = (ymax - pv) / (v - pv) if v != pv else 0
                    en = pn + (n - pn) * t
                    pts.append((x0 + w * en / xmax, y0 - h * ymax / ymax, en, ymax))
                break
            pts.append((x0 + w * n / xmax, y0 - h * v / ymax, n, v))
        d = "M" + " L".join("%.1f %.1f" % (px, py) for px, py, _, _ in pts)
        body.append(path(d, stroke=col, w=2.6))
        lx, ly = pts[-1][0], pts[-1][1]
        top = ly <= y0 - h + 1
        dy = {"O(log n)": 3, "O(1)": 14}.get(name, 4)
        body.append(text(lx + (4 if top else 8), ly + (-4 if top else dy), name, 11, 700,
                         anchor="start" if not top else "middle", fill=col))
    body.append(text(x0 + w / 2, 362, "O(1) and O(log n) are almost flat. O(2ⁿ) leaves the picture at n = 7.", 10.5, 600, fill=MUTED))
    desc = ("A graph of the number of steps against the size of the input, n, from 0 to 12. "
            "Constant time stays flat at 1. Logarithmic time rises very slowly, to about 3.6. "
            "Linear time rises steadily to 12. n log n rises faster, to about 43. n squared "
            "rises steeply, reaching 100 at n equals 10 and leaving the top of the graph at "
            "about 11. Exponential time, 2 to the power n, leaves the top at about n equals 7, "
            "when it reaches 128, and keeps climbing far beyond the graph.")
    return figure("py-growth", 760, 378, "".join(body), "How algorithm costs grow", desc,
                  "Past n = 7, the exponential curve is already off the page. Past n = 40 it is "
                  "off the page of any computer.")


# ===================================================== binary: two's complement

@diagram("py-twos-complement")
def _twos():
    weights = [-128, 64, 32, 16, 8, 4, 2, 1]
    x0, cw = 130, 70
    base = [text(380, 20, "Eight bit two's complement: the leftmost column is negative", 12, 650, fill=MUTED)]
    for c, wgt in enumerate(weights):
        base.append(cell(x0 + c * cw, 36, cw, 30, str(wgt), fill=WARN_SOFT if c == 0 else FILL2,
                         stroke=WARN if c == 0 else LINE, size=12.5, weight=700, ink=WARN if c == 0 else MUTED, r=0))
    base.append(text(x0 - 12, 56, "column", 10.5, 600, anchor="end", fill=MUTED))
    examples = [(5, "00000101"), (-5, "11111011"), (-128, "10000000")]
    for r, (val, bits) in enumerate(examples):
        y = 78 + r * 48
        base.append(text(x0 - 12, y + 24, str(val), 15, 750, anchor="end", mono=True, fill=TEAL if val > 0 else LILAC))
        terms = []
        for c, b in enumerate(bits):
            on = b == "1"
            neg = c == 0
            base.append(cell(x0 + c * cw, y, cw, 38, b, fill=(WARN_SOFT if neg else TEAL_SOFT) if on else FILL,
                             stroke=(WARN if neg else TEAL) if on else LINE, size=15, weight=700,
                             ink=(WARN if neg else TEAL) if on else MUTED, r=0))
            if on:
                terms.append(str(weights[c]))
        total = sum(weights[c] for c, b in enumerate(bits) if b == "1")
        assert total == val

    # how to make 5 negative
    sy = 238
    base.append(line(24, sy - 16, 736, sy - 16, stroke=SOFT, w=1))
    base.append(text(380, sy + 4, "To make 5 into -5: invert every bit, then add 1", 11.5, 700, fill=MUTED))
    stages = [("5", "00000101", TEAL, TEAL_SOFT), ("invert", "11111010", WARN, WARN_SOFT),
              ("add 1", "11111011", LILAC, LILAC_SOFT)]
    for i, (lab, bits, tone, soft) in enumerate(stages):
        x = 40 + i * 240
        base.append(box(x, sy + 22, 190, 54, None, fill=soft, stroke=tone, r=10))
        base.append(text(x + 95, sy + 42, lab, 10.5, 700, fill=tone))
        base.append(text(x + 95, sy + 64, bits, 15, 750, mono=True, fill=tone))
        if i < 2:
            base.append(path("M%s %s L%s %s" % (x + 196, sy + 49, x + 230, sy + 49), stroke=INK, w=2, arrow=True))
    base.append(text(380, sy + 100, "-5 = -128 + 64 + 32 + 16 + 8 + 2 + 1", 11.5, 700, fill=LILAC, mono=True))
    desc = ("The column values of an eight bit two's complement number are minus 128, 64, 32, 16, "
            "8, 4, 2 and 1. The number 5 is 00000101, which is 4 plus 1. The number minus 5 is "
            "11111011, which is minus 128 plus 64 plus 32 plus 16 plus 8 plus 2 plus 1, which "
            "makes minus 5. The number minus 128 is 10000000, with only the negative column set. "
            "To turn 5 into minus 5, invert every bit of 00000101 to get 11111010, then add 1 to "
            "get 11111011.")
    return figure("py-twos", 760, 372, "".join(base), "Two's complement", desc,
                  "The leftmost bit is not a sign flag. It is a column worth minus 128.")


# ===================================================== databases: an entity relationship diagram

@diagram("py-er-diagram")
def _er():
    ew, y0 = 150, 56
    ents = [("Customer", 20, [("PK", "CustomerID"), ("", "Name"), ("", "City")]),
            ("CustomerOrder", 210, [("PK", "OrderID"), ("FK", "CustomerID"), ("", "OrderDate")]),
            ("OrderLine", 400, [("PK FK", "OrderID"), ("PK FK", "ProductID"), ("", "Quantity")]),
            ("Product", 590, [("PK", "ProductID"), ("", "Name"), ("", "Price")])]
    body = [text(380, 22, "Entity relationship diagram for the shop database", 12, 650, fill=MUTED)]
    for name, x, attrs in ents:
        body.append(rect(x, y0, ew, 30, fill=TEAL_SOFT, stroke=TEAL, sw=1.6, r=6))
        body.append(rect(x, y0 + 30, ew, 22 + 22 * len(attrs), fill=FILL, stroke=TEAL, sw=1.6, r=0))
        body.append(text(x + ew / 2, y0 + 20, name, 12, 750, fill=TEAL))
        for i, (key, a_) in enumerate(attrs):
            yy = y0 + 30 + 22 + i * 22
            body.append(text(x + 8, yy - 2, key, 9.5, 750, anchor="start", fill=WARN))
            body.append(text(x + 50, yy - 2, a_, 10.5, 600, anchor="start", mono=True))

    def crow(x_edge, y, direction):
        s_ = direction
        return (line(x_edge + s_ * 14, y, x_edge, y - 9, stroke=INK, w=1.6)
                + line(x_edge + s_ * 14, y, x_edge, y, stroke=INK, w=1.6)
                + line(x_edge + s_ * 14, y, x_edge, y + 9, stroke=INK, w=1.6))

    def one(x_edge, y, direction):
        s_ = direction
        return (line(x_edge + s_ * 8, y - 8, x_edge + s_ * 8, y + 8, stroke=INK, w=1.8)
                + line(x_edge + s_ * 14, y - 8, x_edge + s_ * 14, y + 8, stroke=INK, w=1.8))

    ly = y0 + 70
    body.append(line(20 + ew, ly, 210, ly, stroke=INK, w=1.6))
    body.append(one(20 + ew, ly, 1))
    body.append(crow(210, ly, -1))
    body.append(line(210 + ew, ly, 400, ly, stroke=INK, w=1.6))
    body.append(one(210 + ew, ly, 1))
    body.append(crow(400, ly, -1))
    body.append(line(590, ly, 400 + ew, ly, stroke=INK, w=1.6))
    body.append(one(590, ly, -1))
    body.append(crow(400 + ew, ly, 1))
    body.append(text(380, 218, "One customer places many orders. One order contains many order lines. "
                     "One product appears on many order lines.", 10.5, 600, fill=MUTED))
    body.append(text(380, 238, "OrderLine is the link table that resolves the many to many relationship between orders "
                     "and products.", 10.5, 600, fill=MUTED))
    ky = 270
    body.append(line(60, ky, 90, ky, stroke=INK, w=1.6))
    body.append(one(90, ky, -1))
    body.append(text(104, ky + 4, "exactly one", 10, 600, anchor="start", fill=MUTED))
    body.append(line(220, ky, 250, ky, stroke=INK, w=1.6))
    body.append(crow(250, ky, -1))
    body.append(text(268, ky + 4, "many", 10, 600, anchor="start", fill=MUTED))
    body.append(text(380, ky + 4, "PK primary key,  FK foreign key", 10, 650, anchor="start", fill=WARN))
    desc = ("An entity relationship diagram with four tables. Customer has the primary key "
            "CustomerID, a name and a city. CustomerOrder has the primary key OrderID, the "
            "foreign key CustomerID, and an order date. OrderLine has a primary key made of the "
            "two foreign keys OrderID and ProductID, and a quantity. Product has the primary key "
            "ProductID, a name and a price. One customer places many orders. One order contains "
            "many order lines. One product appears on many order lines. OrderLine is the link "
            "table that resolves the many to many relationship between orders and products.")
    return figure("py-er", 760, 292, "".join(body), "An entity relationship diagram", desc,
                  "The crow's foot goes on the many side, which is where the foreign key lives.")


# ===================================================== databases: normalisation, stage by stage

@diagram("py-normalisation")
def _normalisation():
    def table(x, y, w, name, attrs, tone=TEAL, soft=TEAL_SOFT):
        """attrs are (key marker, name); the markers are shown in front."""
        rows = []
        line_ = ""
        for key, a in attrs:
            rows.append(("%s " % key if key else "") + a)
        h = 30 + 20 * len(rows)
        out = [rect(x, y, w, 26, fill=soft, stroke=tone, sw=1.6, r=6),
               rect(x, y + 26, w, h - 26, fill=FILL, stroke=tone, sw=1.6),
               text(x + w / 2, y + 18, name, 11.5, 750, fill=tone)]
        for i, r in enumerate(rows):
            out.append(text(x + 8, y + 26 + 17 + i * 20, r, 10.5, 600, anchor="start", mono=True))
        return "".join(out), h

    PK, FK = "PK", "FK"
    s1_attrs = [(PK, "OrderID"), (PK, "ProductID"), ("", "OrderDate"), ("", "CustomerID"), ("", "CustomerName"),
                ("", "Address"), ("", "ProductName"), ("", "Price"), ("", "Quantity")]
    base = [text(380, 20, "Normalisation, one form at a time", 12, 650, fill=MUTED)]
    # stage 1: one wide table
    y1 = 40
    t1, h1 = table(20, y1, 720, "Orders (1NF)", [], WARN, WARN_SOFT)
    base.append(rect(20, y1, 720, 26, fill=WARN_SOFT, stroke=WARN, sw=1.6, r=6))
    base.append(rect(20, y1 + 26, 720, 40, fill=FILL, stroke=WARN, sw=1.6))
    base.append(text(380, y1 + 18, "Orders  (1NF: every cell holds one value, and there is a primary key)", 11.5, 750, fill=WARN))
    base.append(text(30, y1 + 50, "PK OrderID   PK ProductID   OrderDate   CustomerID   CustomerName   Address   "
                     "ProductName   Price   Quantity", 10.5, 600, anchor="start", mono=True))
    # arrow 1
    base.append(path("M380 %s L380 %s" % (y1 + 70, y1 + 100), stroke=INK, w=2, arrow=True))
    base.append(text(396, y1 + 90, "2NF: Price and ProductName depend only on ProductID;", 10.5, 650, anchor="start", fill=TEAL))
    base.append(text(396, y1 + 104, "OrderDate and the customer's details only on OrderID.", 10.5, 650, anchor="start", fill=TEAL))
    # stage 2: three tables
    y2 = y1 + 120
    a, ha = table(20, y2, 270, "Order", [(PK, "OrderID"), ("", "OrderDate"), ("", "CustomerID"), ("", "CustomerName"), ("", "Address")])
    b, hb = table(310, y2, 200, "Product", [(PK, "ProductID"), ("", "ProductName"), ("", "Price")])
    c, hc = table(530, y2, 210, "OrderLine", [("PK FK", "OrderID"), ("PK FK", "ProductID"), ("", "Quantity")])
    base += [a, b, c]
    base.append(path("M380 %s L380 %s" % (y2 + 146, y2 + 178), stroke=INK, w=2, arrow=True))
    base.append(text(396, y2 + 160, "3NF: CustomerName and Address depend on", 10.5, 650, anchor="start", fill=TEAL))
    base.append(text(396, y2 + 174, "CustomerID, which is not the key of Order.", 10.5, 650, anchor="start", fill=TEAL))
    # stage 3: four tables
    y3 = y2 + 196
    d, hd = table(20, y3, 160, "Customer", [(PK, "CustomerID"), ("", "CustomerName"), ("", "Address")], LILAC, LILAC_SOFT)
    e, he = table(200, y3, 160, "Order", [(PK, "OrderID"), ("", "OrderDate"), (FK, "CustomerID")], LILAC, LILAC_SOFT)
    f, hf = table(380, y3, 160, "Product", [(PK, "ProductID"), ("", "ProductName"), ("", "Price")], LILAC, LILAC_SOFT)
    g, hg = table(560, y3, 180, "OrderLine", [("PK FK", "OrderID"), ("PK FK", "ProductID"), ("", "Quantity")], LILAC, LILAC_SOFT)
    base += [d, e, f, g]
    base.append(text(380, y3 + hd + 24, "Every fact is now stored once: the key, the whole key, and nothing but the key.", 11, 650, fill=MUTED))
    def hl(y, h):
        return rect(10, y - 8, 740, h + 16, stroke=TEAL, sw=2.4, r=10)
    L = ["First normal form: one value in every cell, no repeating groups, and a primary key of OrderID with ProductID.",
         "Second normal form: facts that depend on only part of the key move to a table of their own, the product's and the order's.",
         "Third normal form: the customer's details depend on CustomerID, which is not the key of Order, so they move to a Customer table."]
    steps = [step(1, hl(y1, 66), L[0]), step(2, hl(y2, hb if hb > ha else ha), L[1]), step(3, hl(y3, hd), L[2])]
    desc = ("Normalising a shop's order data in three stages. In first normal form there is a "
            "single table, Orders, with the primary key OrderID and ProductID and the attributes "
            "OrderDate, CustomerID, CustomerName, Address, ProductName, Price and Quantity. For "
            "second normal form, the facts that depend on only part of the key are moved out: "
            "Product holds ProductID, ProductName and Price, Order holds OrderID, OrderDate and "
            "the customer's details, and OrderLine holds OrderID, ProductID and Quantity. For "
            "third normal form, the customer's name and address, which depend on CustomerID and "
            "not on the order, are moved into a Customer table, and Order keeps CustomerID as a "
            "foreign key. The result is four tables, Customer, Order, Product and OrderLine.")
    return figure_steps("py-norm", 760, y3 + hd + 40, "".join(base), steps, "Normalisation to third normal form",
                        desc, "Each stage removes one kind of repeated data.", labels=L)


# ===================================================== the project: how the program is organised

@diagram("py-nea-structure")
def _nea_structure():
    body = [text(380, 20, "Decomposing the flashcard program into modules", 12, 650, fill=MUTED)]
    top = box(270, 36, 220, 46, None, fill=TEAL_SOFT, stroke=TEAL, r=10)
    body.append(top)
    body.append(text(380, 56, "Flashcard program", 12.5, 750, fill=TEAL))
    body.append(text(380, 72, "the whole solution", 10, 500, fill=MUTED))
    mods = [("main.py", "starts the program,", "runs the menu loop", 40, TEAL, TEAL_SOFT),
            ("ui.py", "asks the user, checks", "input, shows results", 300, TEAL, TEAL_SOFT),
            ("deck.py", "the box rules and the", "database: add, due, record", 560, LILAC, LILAC_SOFT)]
    for name, l1, l2, x, tone, soft in mods:
        body.append(line(380, 82, x + 80, 118, stroke=LINE, w=1.6))
        body.append(box(x, 118, 160, 66, None, fill=soft, stroke=tone, r=10))
        body.append(text(x + 80, 140, name, 12.5, 750, mono=True, fill=tone))
        body.append(text(x + 80, 158, l1, 10, 500, fill=MUTED))
        body.append(text(x + 80, 172, l2, 10, 500, fill=MUTED))
    # dependencies
    body.append(path("M200 151 L300 151", stroke=INK, w=1.8, arrow=True))
    body.append(path("M460 151 L560 151", stroke=INK, w=1.8, arrow=True))
    body.append(text(250, 144, "calls", 9.5, 650, fill=MUTED))
    body.append(text(510, 144, "calls", 9.5, 650, fill=MUTED))
    # the database
    body.append(box(580, 238, 120, 40, None, fill=FILL, stroke=LINE, r=6))
    body.append(text(640, 255, "card table", 11.5, 700, mono=True))
    body.append(text(640, 270, "SQLite", 9.5, 500, fill=MUTED))
    body.append(path("M640 184 L640 238", stroke=INK, w=1.8, arrow=True))
    body.append(text(656, 214, "stores", 9.5, 650, anchor="start", fill=MUTED))
    # tests
    body.append(box(300, 238, 160, 40, None, fill=WARN_SOFT, stroke=WARN, r=8))
    body.append(text(380, 255, "tests.py", 12, 750, mono=True, fill=WARN))
    body.append(text(380, 270, "unittest, from the test plan", 9.5, 500, fill=MUTED))
    body.append(path("M460 258 L560 190", stroke=WARN, w=1.8, arrow=True, marker="ah"))
    body.append(text(486, 236, "tests", 9.5, 650, anchor="start", fill=WARN))
    body.append(text(380, 306, "Each part has one job and can be built, run and tested on its own.", 10.5, 650, fill=MUTED))
    desc = ("A structure diagram for the flashcard program. The whole program is split into three "
            "modules. main.py starts the program and runs the menu loop. ui.py asks the user, "
            "checks input and shows results. deck.py holds the rules of the boxes and the "
            "database, with add, due and record. main.py calls ui.py, and ui.py calls deck.py, "
            "which stores the data in a card table in SQLite. A fourth file, tests.py, uses "
            "unittest to test deck.py against the test plan.")
    return figure("py-nea", 760, 324, "".join(body), "Structure diagram for the project", desc,
                  "A decomposition shows the marker how the problem was broken down before any code was written.")
