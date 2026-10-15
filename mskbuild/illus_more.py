"""Illustrations that fill the thinnest topics: tracing, casting, compression, the life of a device,
quick sort and stability, computational methods, loops, string and list methods, and flat selection."""
import math

from .illus import Canvas, PAL, INK, ARROW, figure, illustration, _n
from . import illus_props as P
from . import illus_glyphs as G
from .illus_algo import num_tile
from .illus_machine import mini_window


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


def sp(t):
    """Spaces that stay spaces in a drawing: SVG collapses runs of them unless they are non-breaking."""
    return t.replace(" ", "\u00a0")


def chip(cv, x, y, w, h, text, fill="#FFFFFF", tc=INK, size=14, stroke="#9FB3BE", mono=True, weight=800, r=None):
    return cv.rect(x, y, w, h, r if r is not None else min(9, h / 2.4), fill, stroke=stroke, sw=1.5) + cv.text(x + w / 2, y + h / 2 + size * .36, text, size, weight, fill=tc, mono=mono)


# ------------------------------------------------------------------ tracing a program

@illustration("trace-table-walk")
def _trace():
    cv = Canvas(800, 500).backdrop()
    cv.add(G.code(cv, 14, 30, 360, ["total = 0", "for i in range(1, 4):", "    total = total + i", "print(total)"], title="total.py", size=14, hl=(2,), numbers=True), P.badge(cv, 34, 28, 1))
    cv.add(P.card(cv, 14, 196, 360, 286, 20, "How to trace", "teal"), P.badge(cv, 36, 222, 2))
    for i, (a_, b_) in enumerate((("Take one line at a time", "and do exactly what it says"), ("One column per variable", "and one for the output"), ("Write a new row each time", "a value changes, never overwrite"), ("Check the last row", "it is the answer the program gives"))):
        y = 262 + i * 52
        cv.add(cv.text(44, y, a_, 14.5, 800, anchor="start", cls="il-ink"), cv.text(44, y + 20, b_, 12.5, 650, anchor="start", cls="il-ink2"))
    # the table
    cv.add(P.card(cv, 390, 30, 396, 452, 20, "The trace table", "coral"), P.badge(cv, 412, 56, 3))
    heads = ["line", "i", "total", "output"]
    widths = [66, 76, 96, 126]
    rows = [(1, "", "0", ""), (2, "1", "0", ""), (3, "1", "1", ""), (2, "2", "1", ""), (3, "2", "3", ""), (2, "3", "3", ""), (3, "3", "6", ""), (4, "3", "6", "6")]
    tx, ty, rh = 410, 82, 40
    cx = tx
    for h_, w_ in zip(heads, widths):
        cv.add(cv.rect(cx, ty, w_, rh, 0, cv.g("teal"), stroke="#FFFFFF", sw=1), cv.text(cx + w_ / 2, ty + 26, h_, 14, 800, fill=INK, mono=True))
        cx += w_
    for r, row in enumerate(rows):
        cx = tx
        last = r == len(rows) - 1
        for k, (v, w_) in enumerate(zip(row, widths)):
            bg = "#E1F5EA" if last else "#FFFFFF"
            cv.add(cv.rect(cx, ty + (r + 1) * rh, w_, rh, 0, bg, stroke="#D5DEE4", sw=1), cv.text(cx + w_ / 2, ty + (r + 1) * rh + 26, str(v), 15, 750 if k else 650, fill=INK, mono=True))
            cx += w_
    cv.add(P.badge(cv, tx + 366, ty + 8 * rh + 20, 4))
    cv.add(cv.text(588, 464, "6 is printed: 1 + 2 + 3", 14.5, 800, cls="il-ink"))
    return figure(
        "trace-table-walk", cv, "A trace table for a loop that adds 1, 2 and 3",
        "A short program sets total to 0, then loops for i from 1 to 3 adding i to total, then prints total. Beside it is its trace table, with one "
        "column for the line number, one for i, one for total and one for the output. Line 1 sets total to 0. Line 2 sets i to 1, line 3 makes total 1. "
        "Line 2 sets i to 2, line 3 makes total 3. Line 2 sets i to 3, line 3 makes total 6. Line 4 prints 6, so the output column of the last row holds 6. "
        "The method: take one line at a time, give each variable its own column and the output one too, write a new row each time a value changes, "
        "and read the answer from the last row.",
        ["Run the program by hand, one line at a time. Line 3 is the one that repeats.", "Follow four rules: one line at a time, one column per variable, a new row for each change, and check the last row.",
         "Each time the loop runs, i goes up by one and total grows: 0, 1, 3, 6.", "The output is written when print runs. Here it is 6."],
        "A trace table shows exactly what the program does, one step at a time. It is how you find a logic error.")


# ------------------------------------------------------------------ casting

TYPE_COL = {"string": "sky", "integer": "mint", "float": "coral"}


@illustration("casting")
def _casting():
    cv = Canvas(800, 500).backdrop()
    spec = [('int("42")', "42", "string", "42", "integer", "text to a whole number"), ("int(3.7)", "3.7", "float", "3", "integer", "cuts off the decimal part: it does not round"),
            ("str(5)", "5", "integer", '"5"', "string", "a number to text, so it can be joined to words"), ('float("3.14")', '"3.14"', "string", "3.14", "float", "text to a decimal number")]
    for n, (call, a_, ta, b_, tb, note_) in enumerate(spec):
        x, y = (14, 406)[n % 2], (28, 172)[n // 2]
        cv.add(P.card(cv, x, y, 380, 134, 20), P.pill(cv, x + 190, y, call, "paper", 15.5, 18, 30, 800))
        cv.add(P.lift(cv, x + 24, y + 34, 110, 44, TYPE_COL[ta], 10, 4, hl=False), cv.text(x + 79, y + 62, a_, 20, 800, fill=INK, mono=True), cv.text(x + 79, y + 96, ta, 12.5, 750, cls="il-ink2", mono=True))
        cv.add(P.arrow(cv, [(x + 142, y + 56), (x + 236, y + 56)], ARROW, 4, 12), cv.text(x + 189, y + 46, call.split("(")[0] + "()", 13, 800, cls="il-ink", mono=True))
        cv.add(P.lift(cv, x + 246, y + 34, 110, 44, TYPE_COL[tb], 10, 4, hl=False), cv.text(x + 301, y + 62, b_, 20, 800, fill=INK, mono=True), cv.text(x + 301, y + 96, tb, 12.5, 750, cls="il-ink2", mono=True))
        cv.add(cv.text(x + 190, y + 120, note_, 12.5, 700, cls="il-ink"))
    cv.add(P.badge(cv, 36, 50, 1), P.badge(cv, 428, 50, 2), P.badge(cv, 36, 194, 3), P.badge(cv, 428, 194, 4))
    cv.add(P.card(cv, 14, 330, 380, 152, 18, "input() always gives text", "sun"), P.badge(cv, 36, 356, 5))
    cv.add(G.code(cv, 30, 368, 348, ['age = int(input("Age? "))', "print(age + 1)"], title=None, size=12.5, numbers=False))
    cv.add(cv.text(204, 462, "convert it before doing sums with it", 12.5, 700, cls="il-ink"))
    cv.add(P.card(cv, 406, 330, 380, 152, 18, "Some conversions fail", "coral"), P.badge(cv, 428, 356, 6))
    cv.add(G.terminal(cv, 422, 366, 348, ['>>> int("hello")', ("ValueError: invalid literal", "#FF9A91")], "Output", 12))
    cv.add(cv.text(596, 468, "so check the input before converting it", 12.5, 700, cls="il-ink"))
    return figure(
        "casting", cv, "Casting between types: int, float and str, and when it fails",
        "Casting converts a value from one data type to another. int of the text 42 gives the whole number 42. int of 3.7 gives 3, because it cuts "
        "off the decimal part and does not round. str of the number 5 gives the text 5, so it can be joined to words. float of the text 3.14 gives "
        "the decimal number 3.14. The input function always gives back text, so a number typed by a user must be converted, as in age equals int "
        "of input. Some conversions fail: int of the text hello raises a ValueError, so input should be checked before it is converted.",
        ["int() turns text into a whole number.", "int() on a float cuts off the decimals. It does not round.", "str() turns a number into text.", "float() turns text into a decimal number.",
         "input() always returns text, so convert it before doing sums.", "A conversion that does not make sense raises an error, so validate first."],
        "Casting does not change the original. It makes a new value of the type you asked for.")


# ------------------------------------------------------------------ lossy and lossless compression

def squares(cv, x, y, w, h, kind):
    """A small picture, either sharp or with its detail thrown away."""
    out = P.photo(cv, x, y, w, h, 6)
    if kind == "lossy":
        n = 8
        cw, ch_ = w / n, h / n
        for i in range(n):
            for j in range(n):
                if (i + j) % 3 == 0:
                    out += cv.rect(x + i * cw, y + j * ch_, cw, ch_, 0, "#FFFFFF", op=.28)
                elif (i * 2 + j) % 5 == 0:
                    out += cv.rect(x + i * cw, y + j * ch_, cw, ch_, 0, "#6684AA", op=.18)
    return out


@illustration("lossy-lossless")
def _lossy():
    cv = Canvas(800, 500).backdrop()
    for k, (x, title, col, how, size_, same) in enumerate(((14, "Lossless", "teal", "ZIP, PNG, FLAC", "3.2 MB", True), (406, "Lossy", "coral", "JPEG, MP3, MP4", "0.5 MB", False))):
        cv.add(P.card(cv, x, 30, 380, 296, 20, title, col), P.badge(cv, x + 22, 56, k + 1))
        cv.add(squares(cv, x + 24, 86, 90, 70, "orig"), cv.text(x + 69, 182, "original", 13, 700, cls="il-ink"), cv.text(x + 69, 200, "5.0 MB", 14, 800, cls="il-ink", mono=True))
        cv.add(P.arrow(cv, [(x + 126, 120), (x + 156, 120)], ARROW, 3.5, 10))
        cv.add(P.lift(cv, x + 164, 88, 52, 62, "paper", 8, 3, hl=False), cv.rect(x + 184, 90, 12, 40, 3, PAL[col][1]), cv.text(x + 190, 182, "compressed", 13, 700, cls="il-ink"), cv.text(x + 190, 200, size_, 14, 800, cls="il-ink", mono=True))
        cv.add(P.arrow(cv, [(x + 228, 120), (x + 258, 120)], ARROW, 3.5, 10))
        cv.add(squares(cv, x + 266, 86, 90, 70, "orig" if same else "lossy"), cv.text(x + 311, 182, "restored", 13, 700, cls="il-ink"))
        cv.add(P.tick(cv, x + 268, 214, 11) if same else P.cross(cv, x + 252, 214, 11), cv.text(x + 286 if same else x + 270, 219, "identical" if same else "not identical", 13.5, 800, anchor="start", cls="il-ink"))
        cv.add(cv.text(x + 190, 250, how, 13.5, 800, cls="il-ink", mono=True))
        for j, ln in enumerate(wrap("nothing is lost: every bit comes back" if same else "detail is thrown away for good", 36)):
            cv.add(cv.text(x + 190, 276 + j * 18, ln, 13.5, 700, cls="il-ink2"))
    cv.add(P.card(cv, 14, 346, 772, 136, 18, "Which to use?", "sun"), P.badge(cv, 36, 372, 3))
    for i, (head, items, col) in enumerate((("Lossless", "text, programs, spreadsheets, medical scans: anything that must be exact", "teal"), ("Lossy", "photos, music, video: small losses go unnoticed and the files shrink a lot", "coral"))):
        x = 36 + i * 380
        cv.add(P.pill(cv, x, 400, head, col, 14, 14, 26, 800, anchor="start"))
        for j, ln in enumerate(wrap(items, 40)):
            cv.add(cv.text(x, 436 + j * 18, ln, 13.5, 650, anchor="start", cls="il-ink"))
    return figure(
        "lossy-lossless", cv, "Lossless against lossy compression: a picture before and after, and when to use each",
        "Two ways to compress a file. With lossless compression a 5 megabyte picture is compressed to 3.2 megabytes using something like ZIP, PNG "
        "or FLAC, and when it is restored it is identical to the original, because nothing is lost. With lossy compression the same picture is "
        "compressed to 0.5 megabytes using something like JPEG, MP3 or MP4, and when it is restored it is not identical, because detail has "
        "been thrown away for good. Lossless suits text, programs, spreadsheets and medical scans, anything that must be exact. Lossy suits "
        "photos, music and video, where small losses go unnoticed and the files shrink a lot.",
        ["Lossless: the file gets smaller, and decompressing gives back exactly the original.", "Lossy: the file gets much smaller, but detail is thrown away for good, so it cannot be restored exactly.",
         "Choose lossless when the data must be exact, and lossy when small losses do not matter."],
        "Lossy files can never be restored to the original. That is the trade for a much smaller file.")


# ------------------------------------------------------------------ the life of a device

def pickaxe_rock(cv, cx, cy):
    out = cv.poly([(cx - 22, cy + 16), (cx - 12, cy - 12), (cx + 6, cy - 20), (cx + 24, cy - 4), (cx + 20, cy + 16)], cv.g("slate", "deep"), stroke="#6B7F8C", sw=1.4)
    return out + cv.poly([(cx - 6, cy - 2), (cx + 4, cy - 12), (cx + 12, cy - 2), (cx + 4, cy + 6)], cv.g("sky"), stroke="#2F82C0", sw=1.2)


def factory(cv, cx, cy):
    out = cv.rect(cx - 26, cy - 6, 52, 26, 3, cv.g("slate", "deep")) + cv.rect(cx - 20, cy - 24, 10, 20, 2, cv.g("coral", "deep")) + cv.rect(cx - 4, cy - 18, 10, 14, 2, cv.g("coral", "deep"))
    for k in range(3):
        out += cv.rect(cx - 18 + k * 14, cy + 2, 8, 8, 1, "#DDF3FA")
    return out + cv.circle(cx - 14, cy - 30, 5, "#B9C6CE", op=.7) + cv.circle(cx - 8, cy - 38, 4, "#B9C6CE", op=.5)


def bin_(cv, cx, cy):
    out = cv.poly([(cx - 18, cy - 12), (cx + 18, cy - 12), (cx + 14, cy + 22), (cx - 14, cy + 22)], cv.g("slate", "deep"), stroke="#6B7F8C", sw=1.4)
    out += cv.rect(cx - 22, cy - 20, 44, 8, 3, cv.g("metal", "deep"))
    for k in (-8, 0, 8):
        out += cv.line(cx + k, cy - 6, cx + k * .8, cy + 16, "#8799A7", 1.6)
    return out


@illustration("tech-lifecycle")
def _life():
    cv = Canvas(800, 500).backdrop()
    nodes = [("Mining", "rare metals, damage to land", pickaxe_rock, "sun"), ("Making", "energy, water and chemicals", factory, "coral"),
             ("Using", "electricity for charging and data centres", None, "sky"), ("Throwing away", "e-waste: toxic metals in landfill", bin_, "slate"), ("Recycling", "recover metals, repair and reuse", None, "mint")]
    xs = [92 + i * 154 for i in range(5)]
    for i, ((name, sub, icon, col), x) in enumerate(zip(nodes, xs)):
        cv.add(cv.circle(x, 123, 46, "#10303A", op=.14), cv.circle(x, 120, 46, "var(--il-card)", stroke=PAL[col][2], sw=3.4))
        if icon is not None:
            cv.add(icon(cv, x, 122))
        elif name == "Using":
            cv.add(P.bulb(cv, x - 18, 90, .8, True))
        else:
            cv.add(G.arrow_ring(cv, x, 120, 20, -60, 240, "#2F9F77", 5, 11))
        cv.add(P.badge(cv, x - 38, 82, i + 1, "deep", 12))
        cv.add(cv.text(x, 196, name, 16, 800, cls="il-ink"))
        for j, ln in enumerate(wrap(sub, 20)):
            cv.add(cv.text(x, 216 + j * 15, ln, 12.5, 650, cls="il-ink2"))
        if i < 4:
            cv.add(P.arrow(cv, [(x + 52, 120), (xs[i + 1] - 52, 120)], "#25B3BB", 5, 13))
    # the loop back: recovered materials go into new devices
    cv.add(cv.path("M%s 276 L%s 304 Q%s 318 %s 318 L%s 318 Q%s 318 %s 304 L%s 288" % (xs[4], xs[4], xs[4], xs[4] - 14, xs[1] + 14, xs[1], xs[1], xs[1]), stroke="#2F9F77", sw=5))
    cv.add(cv.poly([(xs[1], 276), (xs[1] - 9, 291), (xs[1] + 9, 291)], "#2F9F77"))
    cv.add(cv.text((xs[1] + xs[4]) / 2, 306, "recovered metals go into new devices", 13.5, 800, cls="il-ink"))
    # what to do about it
    cv.add(P.card(cv, 14, 346, 772, 136, 18, "Reduce, reuse, recycle", "mint"), P.badge(cv, 36, 372, 6))
    for i, (head, body, col) in enumerate((("Reduce", "buy only what you need, and keep it longer", "mint"), ("Reuse", "repair it, resell it or give it away", "sky"), ("Recycle", "recover the materials at the end", "sun"))):
        x = 34 + i * 250
        cv.add(P.lift(cv, x, 392, 234, 74, col, 12, 5, hl=False), cv.text(x + 117, 418, head, 17, 800, fill=INK))
        for j, ln in enumerate(wrap(body, 30)):
            cv.add(cv.text(x + 117, 440 + j * 16, ln, 12.5, 700, fill=INK))
    return figure(
        "tech-lifecycle", cv, "The life of a device, from mining to recycling, and its environmental impact at each stage",
        "The life of a device in five stages, left to right. One, mining the rare metals it needs, which damages land. Two, making it, which "
        "uses energy, water and chemicals. Three, using it, which uses electricity for charging and for the data centres behind online services. "
        "Four, throwing it away, which creates e-waste, with toxic metals that end up in landfill. Five, recycling, which recovers metals and lets "
        "devices be repaired and reused, and the recovered metals go back into making new devices. Below, the three ways to reduce the impact: "
        "reduce, by buying only what you need and keeping it longer; reuse, by repairing, reselling or giving it away; and recycle, by recovering "
        "the materials at the end.",
        ["Mining rare metals damages land.", "Making a device uses energy, water and chemicals.", "Using it needs electricity, including at the data centres.",
         "Throwing it away creates e-waste, with toxic metals in landfill.", "Recycling recovers materials, which go back into making new devices.",
         "Reduce, reuse and recycle, in that order of importance."],
        "The biggest saving is to use a device for longer. Recycling is the last resort, not the first.")


# ------------------------------------------------------------------ quick sort

@illustration("quick-sort-cards")
def _quick():
    cv = Canvas(800, 500).backdrop()
    steps = [("Pick a pivot", "the first item"), ("Partition", "smaller left, larger right"), ("Repeat on each part", "recursively"), ("Join them up", "nothing to merge")]
    def tiles(y, groups):
        x = 262
        out = ""
        for gi, grp in enumerate(groups):
            for v, col in grp:
                out += num_tile(cv, x, y, v, 52, 46, col, 21)
                x += 58
            x += 22
        return out
    for i, (head, sub) in enumerate(steps):
        y = 52 + i * 102
        if i % 2 == 0:
            cv.add(cv.rect(14, y - 18, 772, 90, 14, "var(--il-band)"))
        cv.add(P.badge(cv, 40, y + 22, i + 1), cv.text(66, y + 18, head, 16, 800, anchor="start", cls="il-ink"), cv.text(66, y + 38, sub, 13, 650, anchor="start", cls="il-ink2"))
    cv.add(tiles(52, [[(6, "coral"), (3, "slate"), (9, "slate"), (1, "slate"), (8, "slate"), (4, "slate")]]))
    cv.add(cv.text(288, 40, "pivot", 13, 800, cls="il-ink"))
    cv.add(tiles(154, [[(3, "sky"), (1, "sky"), (4, "sky")], [(6, "coral")], [(9, "mint"), (8, "mint")]]))
    cv.add(cv.text(321, 144, "smaller", 12.5, 750, cls="il-ink2"), cv.text(582, 144, "larger", 12.5, 750, cls="il-ink2"), cv.text(466, 144, "pivot", 12.5, 750, cls="il-ink2"))
    cv.add(tiles(256, [[(1, "sky"), (3, "coral"), (4, "mint")], [(6, "coral")], [(8, "sky"), (9, "coral")]]))
    cv.add(cv.text(321, 246, "3 is the pivot", 12.5, 750, cls="il-ink2"), cv.text(582, 246, "9 is the pivot", 12.5, 750, cls="il-ink2"))
    cv.add(tiles(358, [[(1, "green"), (3, "green"), (4, "green"), (6, "green"), (8, "green"), (9, "green")]]))
    cv.add(P.pill(cv, 400, 470, "Average n log n. Worst case n squared, if the pivot is always the smallest or largest.", "paper", 13.5, 16, 28, 750))
    return figure(
        "quick-sort-cards", cv, "Quick sort on 6 3 9 1 8 4: pick a pivot, partition, repeat on each part, join",
        "Quick sort on the list 6, 3, 9, 1, 8, 4. Step one, pick a pivot, here the first item, 6. Step two, partition: everything smaller than the "
        "pivot goes on its left, 3, 1 and 4, and everything larger goes on its right, 9 and 8. The pivot, 6, is now in its final place. Step three, "
        "do the same to each part. In the left part 3 is the pivot, with 1 smaller and 4 larger. In the right part 9 is the pivot, with 8 smaller "
        "and nothing larger. Step four, join the parts: 1, 3, 4, 6, 8, 9. There is nothing to merge, because the partitioning did the work. On average "
        "it takes n log n steps, but the worst case is n squared, when the pivot is always the smallest or the largest item.",
        ["Choose a pivot. Here it is the first item.", "Partition: smaller items to its left, larger to its right. The pivot is now in its final position.",
         "Sort each part the same way, recursively. A part of one item is already sorted.", "Join the parts in order. There is no merge step."],
        "Merge sort does the easy split and the hard merge. Quick sort does the hard split, the partition, and the merge is nothing at all.")


# ------------------------------------------------------------------ stability

@illustration("sort-stability")
def _stable():
    cv = Canvas(800, 500).backdrop()
    people = [("Ana", 70, "coral"), ("Ben", 90, "slate"), ("Cat", 70, "sky"), ("Dev", 80, "slate")]

    def rec(x, y, name, score, col):
        tc = INK
        return P.lift(cv, x, y, 118, 54, col, 10, 4, hl=False) + cv.text(x + 59, y + 24, name, 15, 800, fill=tc) + cv.text(x + 59, y + 44, "score %d" % score, 12.5, 700, fill=tc, mono=True)

    cv.add(P.card(cv, 14, 30, 772, 110, 18, "Before: in the order they were entered", "sun"), P.badge(cv, 36, 56, 1))
    for i, (n_, s_, c_) in enumerate(people):
        cv.add(rec(120 + i * 150, 68, n_, s_, c_))
    for k, (x, title, col, order, same) in enumerate(((14, "Stable sort", "mint", [(0, 0), (2, 1), (3, 2), (1, 3)], True), (406, "Unstable sort", "coral", [(2, 0), (0, 1), (3, 2), (1, 3)], False))):
        cv.add(P.card(cv, x, 170, 380, 220, 18, title, col, tx=.5), P.badge(cv, x + 22, 196, k + 2))
        for pos, (src, _) in enumerate(order):
            n_, s_, c_ = people[src]
            rx, ry = x + 12 + pos * 90, 232
            cv.add(P.lift(cv, rx, ry, 80, 58, c_, 8, 4, hl=False), cv.text(rx + 40, ry + 24, n_, 14, 800, fill=INK), cv.text(rx + 40, ry + 44, str(s_), 13, 700, fill=INK, mono=True))
        cv.add(cv.text(x + 190, 326, "Ana is still before Cat" if same else "Cat is now before Ana", 14, 800, cls="il-ink"), cv.text(x + 190, 346, "equal scores keep their order" if same else "equal scores swapped places", 12.5, 650, cls="il-ink2"))
        cv.add(P.tick(cv, x + 190, 372, 11) if same else P.cross(cv, x + 190, 372, 11))
    cv.add(P.card(cv, 14, 410, 772, 72, 16))
    cv.add(cv.text(34, 440, "Why it matters:", 15, 800, anchor="start", cls="il-ink"), cv.text(160, 440, "sort a list by name, then by score. A stable sort keeps the names in order", 14, 650, anchor="start", cls="il-ink"))
    cv.add(cv.text(160, 462, "within each score. An unstable one scrambles them.", 14, 650, anchor="start", cls="il-ink"))
    return figure(
        "sort-stability", cv, "A stable sort keeps equal items in their original order, an unstable sort may not",
        "Four people are entered in the order Ana with a score of 70, Ben with 90, Cat with 70 and Dev with 80, and then sorted by score. A stable "
        "sort puts them in the order Ana 70, Cat 70, Dev 80, Ben 90, so Ana, who was before Cat, is still before Cat. An unstable sort may give "
        "Cat 70, Ana 70, Dev 80, Ben 90, where the two equal scores have swapped. Stability matters when a list is sorted twice, for example by name "
        "and then by score: a stable sort keeps the names in order within each score.",
        ["The starting order. Ana and Cat have the same score.", "A stable sort keeps Ana before Cat, as they were.", "An unstable sort may swap them."],
        "Merge sort and insertion sort are stable. Quick sort in its usual form is not.")


# ------------------------------------------------------------------ computational methods

@illustration("computational-methods")
def _methods():
    cv = Canvas(800, 500).backdrop()
    spec = [("Divide and conquer", "coral", "split, solve the parts, combine"), ("Backtracking", "sky", "undo the last choice and try another"), ("Heuristics", "sun", "a good answer, found fast"),
            ("Data mining", "mint", "find patterns in a huge dataset"), ("Performance modelling", "plum", "predict behaviour without building it"), ("Visualisation", "teal", "see patterns a table hides")]
    for n, (title, col, cap) in enumerate(spec):
        x, y = (14, 277, 540)[n % 3], (30, 262)[n // 3]
        cv.add(P.card(cv, x, y, 246, 200, 18, title, col), P.badge(cv, x + 16, y + 24, n + 1))
        cx = x + 123
        cv.add(cv.text(cx, y + 186, cap, 12.5, 700, cls="il-ink"))
        if n == 0:
            cv.add(P.lift(cv, cx - 70, y + 44, 140, 26, "slate", 7, 3, hl=False), cv.text(cx, y + 62, "8 items", 12.5, 800, fill=INK))
            for k in range(2):
                bx = cx - 100 + k * 100
                cv.add(P.lift(cv, bx, y + 88, 96, 24, "sky", 7, 3, hl=False), cv.text(bx + 48, y + 105, "4", 12.5, 800, fill=INK, mono=True), cv.line(cx, y + 72, bx + 48, y + 88, "#8AA0AC", 1.8))
            for k in range(4):
                bx = cx - 108 + k * 54
                cv.add(P.lift(cv, bx, y + 130, 46, 22, "mint", 6, 3, hl=False), cv.text(bx + 23, y + 146, "2", 12, 800, fill=INK, mono=True), cv.line(cx - 50 + (k // 2) * 100, y + 112, bx + 23, y + 130, "#8AA0AC", 1.6))
        elif n == 1:
            c_ = 30
            ox, oy = x + 52, y + 46
            walls = [(0, 0, 0, 4), (0, 0, 5, 0), (1, 0, 1, 2), (1, 1, 3, 1), (3, 1, 3, 3), (2, 2, 2, 4), (2, 3, 5, 3), (4, 1, 4, 3), (5, 0, 5, 2)]
            for (x0_, y0_, x1_, y1_) in walls:
                cv.add(cv.line(ox + x0_ * c_, oy + y0_ * c_, ox + x1_ * c_, oy + y1_ * c_, "#6684AA", 3.4))
            mid = lambda i, j: (ox + (i + .5) * c_, oy + (j + .5) * c_)
            cv.add(cv.path("M%s %s L%s %s L%s %s" % (*mid(0, 0), *mid(0, 2), *mid(1, 2)), stroke="#BA352D", sw=3.4), P.cross(cv, *mid(1, 2), 7))
            cv.add(cv.path("M%s %s L%s %s L%s %s L%s %s L%s %s" % (*mid(0, 2), *mid(0, 1), *mid(2, 1), *mid(2, 0), *mid(4, 0)), stroke="#248049", sw=3.6))
            cv.add(cv.circle(*mid(0, 0), 6, "#FFFFFF", stroke=INK, sw=2.4), P.tick(cv, *mid(4, 0), 8))
        elif n == 2:
            a_, b_ = (x + 34, y + 140), (x + 212, y + 70)
            for (c1, c2, o) in (((x + 80, y + 60), (x + 150, y + 170), .25), ((x + 60, y + 170), (x + 190, y + 150), .25), ((x + 100, y + 100), (x + 120, y + 60), .25)):
                cv.add(cv.path("M%s %s Q%s %s %s %s" % (a_[0], a_[1], c1[0] + 30, c1[1] + 20, b_[0], b_[1]), stroke="#8AA0AC", sw=2.2, dash="4 5", op=.7))
            cv.add(cv.path("M%s %s Q%s %s %s %s" % (a_[0], a_[1], x + 120, y + 96, b_[0], b_[1]), stroke="#248049", sw=5))
            cv.add(cv.circle(a_[0], a_[1], 9, "#FFFFFF", stroke=INK, sw=2.6), cv.circle(b_[0], b_[1], 9, "#FFFFFF", stroke=INK, sw=2.6))
            cv.add(P.pill(cv, cx, y + 50, "good enough", "paper", 12, 8, 22, 750))
        elif n == 3:
            for k in range(4):
                bx = x + 14 + k * 58
                cv.add(cv.rect(bx, y + 46, 50, 66, 7, "#FFFFFF", stroke="#9FB3BE", sw=1.4))
                items = [("B", "sun"), ("M", "sky"), ("T", "coral")] if k != 2 else [("M", "sky"), ("E", "mint"), ("T", "coral")]
                if k == 3:
                    items = [("B", "sun"), ("E", "mint"), ("T", "coral")]
                for j, (lt, c2) in enumerate(items):
                    cv.add(cv.rect(bx + 8, y + 52 + j * 18, 34, 15, 4, cv.g(c2)), cv.text(bx + 25, y + 64 + j * 18, lt, 10.5, 800, fill=INK))
            cv.add(cv.text(cx, y + 134, "B = bread   T = butter   M = milk   E = eggs", 11.5, 650, cls="il-ink2"))
            cv.add(P.pill(cv, cx, y + 158, "bread and butter go together", "paper", 12, 8, 22, 750))
        elif n == 4:
            ox, oy, w_, h_ = x + 26, y + 150, 196, 100
            cv.add(cv.line(ox, oy, ox, oy - h_, ARROW, 2), cv.line(ox, oy, ox + w_, oy, ARROW, 2))
            cv.add(cv.text(ox + w_, oy + 16, "users", 11.5, 650, anchor="end", cls="il-ink2"), cv.text(ox + 4, oy - h_ - 6, "response time", 11.5, 650, anchor="start", cls="il-ink2"))
            pts = [(ox + t * w_ / 20.0, oy - (6 + (t / 20.0) ** 4 * 88)) for t in range(0, 21)]
            cv.add(cv.path("M" + " L".join("%s %s" % (_n(px), _n(py)) for px, py in pts), stroke="#8061A9", sw=3.6))
            cv.add(cv.line(ox + w_ * .86, oy, ox + w_ * .86, oy - h_ + 8, "#BA352D", 2, dash="4 4"), cv.text(ox + w_ * .86 - 4, oy - h_ + 10, "limit", 11.5, 800, anchor="end", cls="il-bad"))
        else:
            ox, oy = x + 16, y + 48
            for r in range(4):
                for c in range(3):
                    cv.add(cv.rect(ox + c * 34, oy + r * 20, 32, 18, 3, "#FFFFFF", stroke="#D5DEE4", sw=1), cv.text(ox + c * 34 + 16, oy + r * 20 + 13, str((5, 6, 5, 6, 7, 5, 6, 5, 7, 6, 55, 6)[r * 3 + c]), 10.5, 650, fill=INK, mono=True))
            cv.add(P.arrow(cv, [(ox + 106, oy + 40), (ox + 126, oy + 40)], ARROW, 3, 9))
            bx = ox + 130
            for k, v in enumerate((20, 24, 20, 26, 22, 78)):
                cv.add(cv.rect(bx + k * 13, oy + 82 - v, 10, v, 2, cv.g("coral") if v > 60 else cv.g("teal")))
            cv.add(cv.line(bx - 2, oy + 82, bx + 78, oy + 82, ARROW, 1.6))
            cv.add(cv.text(bx + 58, oy - 6, "the spike", 11.5, 800, anchor="middle", cls="il-bad"))
    return figure(
        "computational-methods", cv, "Six computational methods: divide and conquer, backtracking, heuristics, data mining, performance modelling and visualisation",
        "Six methods that an A Level problem solver uses. Divide and conquer splits a problem of 8 items into two of 4, then four of 2, solves the "
        "small parts and combines them. Backtracking goes down a path in a maze, finds it is a dead end, undoes the last choice and tries another way "
        "that reaches the exit. A heuristic is a rule of thumb that finds a good enough route quickly instead of checking every route. Data "
        "mining searches a huge dataset for patterns, such as bread and butter being bought together in many baskets. Performance modelling "
        "predicts, from a mathematical model, how response time rises with the number of users and where the limit is, without building the "
        "system. Visualisation turns a table of numbers into a chart, where a spike that was hidden in the table jumps out.",
        ["Divide and conquer: split, solve the small parts, combine.", "Backtracking: when a path fails, go back to the last choice and try another.",
         "Heuristics: a rule of thumb that gives a good answer quickly.", "Data mining: find patterns in a huge dataset.", "Performance modelling: predict behaviour from a model.",
         "Visualisation: charts show patterns a table of numbers hides."],
        "Each method answers a different problem. In an exam, name the method and say why it suits the scenario.")


# ------------------------------------------------------------------ loops

@illustration("while-loops")
def _while():
    cv = Canvas(800, 500).backdrop()
    cv.add(P.card(cv, 14, 30, 380, 262, 20, "for: you know how many times", "teal"), P.badge(cv, 36, 56, 1))
    cv.add(G.code(cv, 30, 72, 348, ["for i in range(5):", "    print('lap', i)"], title=None, size=13, numbers=False))
    for k in range(5):
        x = 34 + k * 68
        cv.add(P.lift(cv, x, 168, 56, 44, ("sky", "mint")[k % 2], 9, 4, hl=False), cv.text(x + 28, 196, str(k), 20, 800, fill=INK, mono=True))
        if k < 4:
            cv.add(P.arrow(cv, [(x + 58, 190), (x + 66, 190)], ARROW, 2.5, 6))
    cv.add(cv.text(204, 244, "i takes 0, 1, 2, 3, 4 and then the loop ends by itself", 13, 700, cls="il-ink"), cv.text(204, 266, "five laps, counted for you", 12.5, 650, cls="il-ink2"))
    cv.add(P.card(cv, 406, 30, 380, 262, 20, "while: repeat until something changes", "coral"), P.badge(cv, 428, 56, 2))
    cv.add(G.code(cv, 422, 72, 348, ["guess = ''", "while guess != 'cat':", "    guess = input('Guess? ')", "print('Correct!')"], title=None, size=12.5, numbers=False, hl=(1,)))
    for i, (g_, res) in enumerate((("dog", True), ("bird", True), ("cat", False))):
        y = 190 + i * 30
        cv.add(chip(cv, 426, y, 84, 24, g_, "#FFFFFF", INK, 13))
        cv.add(cv.text(522, y + 17, "!=", 12.5, 800, anchor="start", cls="il-ink2", mono=True))
        cv.add(P.pill(cv, 566, y + 12, "True" if res else "False", "coral" if res else "mint", 12.5, 8, 22, 800))
        cv.add(P.arrow(cv, [(604, y + 12), (630, y + 12)], ARROW, 2.5, 7), cv.text(640, y + 17, "ask again" if res else "carry on", 13, 800, anchor="start", cls="il-ink"))
    cv.add(cv.text(596, 284, "checked every time round, before the body runs", 12.5, 650, cls="il-ink2"))
    cv.add(P.card(cv, 14, 312, 772, 170, 20, "The classic bug: an infinite loop", "red"), P.badge(cv, 36, 338, 3))
    cv.add(G.code(cv, 30, 352, 330, ["n = 5", "while n > 0:", "    print(n)", "    # forgot: n = n - 1"], title=None, size=12.5, numbers=False, hl=(3,)))
    cv.add(G.arrow_ring(cv, 440, 424, 34, -60, 240, "#BA352D", 6, 14), cv.text(440, 430, "5", 22, 800, cls="il-bad", mono=True))
    cv.add(cv.text(500, 392, "n never changes, so n > 0 is always true", 14.5, 800, anchor="start", cls="il-ink"), cv.text(500, 416, "and the loop never stops: 5, 5, 5, 5 ...", 13.5, 650, anchor="start", cls="il-ink2"))
    cv.add(P.tick(cv, 512, 448, 10), cv.text(532, 446, "make sure something inside the loop", 13, 750, anchor="start", cls="il-ink"), cv.text(532, 464, "changes the condition", 13, 750, anchor="start", cls="il-ink"))
    return figure(
        "while-loops", cv, "A for loop that counts, a while loop that waits for a condition, and an infinite loop",
        "Two kinds of loop. A for loop is used when you know how many times: for i in range 5 runs five times with i taking 0, 1, 2, 3 and 4, and "
        "then ends by itself. A while loop repeats until something changes: while guess is not cat, ask again, and when the guess is cat it carries on. "
        "The number of laps is not known in advance. The classic bug is the infinite loop. With n equal to 5 and while n greater than 0 printing n, "
        "if the line that reduces n is forgotten then n never changes, n greater than 0 is always true and the loop never stops. Make sure "
        "something inside the loop changes the condition.",
        ["for repeats a counted number of times and stops by itself.", "while checks a condition each time and repeats until it is false.",
         "If nothing inside the loop changes the condition, the loop never stops."],
        "Use for when you know the count, and while when you are waiting for something to happen.")


# ------------------------------------------------------------------ string methods

@illustration("string-methods")
def _strmeth():
    cv = Canvas(800, 500).backdrop()
    cv.add(P.band(cv, 14, 24, 512, 44, 14))
    cv.add(cv.text(30, 52, sp('text = "  Hello World  "'), 15, 800, anchor="start", cls="il-ink", mono=True))
    rows = [('text.upper()', '"  HELLO WORLD  "', "sky"), ('text.strip()', '"Hello World"', "mint"), ('text.replace("l", "L")', '"  HeLLo WorLd  "', "coral"), ('text.strip().split(" ")', '["Hello", "World"]', "sun"),
            ('"-".join(["a", "b", "c"])', '"a-b-c"', "plum"), ('text.find("World")', "8", "teal")]
    for i, (call, res, col) in enumerate(rows):
        y = 80 + i * 58
        cv.add(P.badge(cv, 32, y + 22, i + 1, "deep", 12))
        cv.add(chip(cv, 56, y + 4, 232, 36, call, "#1C2831", "#FFFFFF", 13.5, "#1C2831"))
        cv.add(P.arrow(cv, [(296, y + 22), (322, y + 22)], ARROW, 3.5, 10))
        w = min(196, max(80, len(res) * 8.4 + 24))
        cv.add(P.lift(cv, 330, y + 4, w, 36, col, 9, 4, hl=False), cv.text(330 + w / 2, y + 28, sp(res), 13.5, 800, fill="#FFFFFF" if col in ("plum",) else INK, mono=True))
    cv.add(P.card(cv, 546, 24, 240, 384, 18, "Strings are fixed", "red"), P.badge(cv, 568, 50, 7))
    cv.add(cv.rect(566, 78, 200, 38, 8, "#FFFFFF", stroke="#9FB3BE", sw=1.4), cv.text(666, 102, "text", 13, 800, fill=INK, mono=True), cv.text(666, 142, "stays the same", 13, 700, cls="il-ink2"))
    cv.add(P.padlock(cv, 641, 156, .7, "sun"))
    cv.add(cv.text(666, 238, "text.upper() makes", 13.5, 750, cls="il-ink"), cv.text(666, 256, "a brand new string", 13.5, 750, cls="il-ink"))
    cv.add(cv.rect(566, 270, 200, 38, 8, "#C9EAFB", stroke="#2F82C0", sw=1.4), cv.text(666, 294, "new string", 13, 800, fill=INK, mono=True))
    cv.add(cv.text(666, 340, "keep it by assigning:", 12.5, 700, cls="il-ink2"), cv.text(666, 362, "name = name.upper()", 13, 800, cls="il-ink", mono=True))
    cv.add(P.card(cv, 14, 432, 772, 52, 14))
    cv.add(cv.text(400, 463, "split and join are opposites: split breaks text into a list, join builds text from a list.", 14, 750, cls="il-ink"))
    return figure(
        "string-methods", cv, "Six string methods applied to the text with spaces round Hello World, and why the original never changes",
        "Six string methods applied to text equal to two spaces, Hello World, two spaces. upper gives all capitals. strip removes the spaces at "
        "the ends, giving Hello World. replace of l with capital L swaps every match, giving HeLLo WorLd with its spaces. strip then split on a space breaks the "
        "text into the list Hello, World. join of the list a, b, c with a hyphen builds the text a-b-c. find of World gives 8, the position where it starts. "
        "On the right a reminder that strings do not change: text dot upper makes a brand new string and leaves text as it was, so to keep the "
        "result you assign it, name equals name dot upper. Split and join are opposites.",
        ["upper() makes every letter a capital.", "strip() removes spaces from both ends.", "replace() swaps every match for something else.", "split() breaks a string into a list.",
         "join() builds a string from a list.", "find() gives the position of the first match, or -1 if there is none.", "A method returns a new string. The original is never changed unless you assign the result."],
        "Methods return new strings. To keep the result, assign it to a variable.")


# ------------------------------------------------------------------ list methods

@illustration("list-methods")
def _listmeth():
    cv = Canvas(800, 500).backdrop()
    cv.add(P.band(cv, 14, 24, 772, 44, 14))
    cv.add(cv.text(30, 52, "scores = [45, 78, 12, 90, 33]", 15, 800, anchor="start", cls="il-ink", mono=True), cv.text(770, 52, "each row starts from this list", 12.5, 650, anchor="end", cls="il-ink2"))

    def cells(x, y, vals, hot=None, kinds=None):
        out = ""
        for i, v in enumerate(vals):
            col = (kinds or {}).get(i, "slate")
            out += P.lift(cv, x + i * 44, y, 40, 34, col, 7, 3, hl=False) + cv.text(x + i * 44 + 20, y + 23, str(v), 14.5, 800, fill=INK, mono=True)
        return out
    base = [45, 78, 12, 90, 33]
    rows = [("scores.append(60)", base[:] + [60], {5: "mint"}, "added to the end"), ("scores.insert(1, 99)", [45, 99, 78, 12, 90, 33], {1: "mint"}, "inserted at index 1, the rest move along"),
            ("scores.remove(12)", [45, 78, 90, 33], {}, "the first 12 is removed, the rest close up"), ("scores.pop()", [45, 78, 12, 90], {}, "the last item is removed and returned: 33"), ("scores.sort()", [12, 33, 45, 78, 90], {0: "sky", 1: "sky", 2: "sky", 3: "sky", 4: "sky"}, "sorted in place, smallest first")]
    for i, (call, after, kinds, note_) in enumerate(rows):
        y = 84 + i * 80
        cv.add(P.badge(cv, 32, y + 22, i + 1, "deep", 12))
        cv.add(chip(cv, 54, y + 2, 190, 34, call, "#1C2831", "#FFFFFF", 13.5, "#1C2831"))
        gone = {"remove": {2: "coral"}, "pop": {4: "coral"}}.get(call.split(".")[1].split("(")[0], {})
        cv.add(cells(256, y, base, None, gone))
        cv.add(P.arrow(cv, [(484, y + 17), (512, y + 17)], ARROW, 3.5, 10))
        cv.add(cells(522, y, after, None, kinds))
        cv.add(cv.text(54, y + 60, note_, 12.5, 700, anchor="start", cls="il-ink2"))
    return figure(
        "list-methods", cv, "Five list methods, each shown on the list 45, 78, 12, 90, 33 before and after",
        "Five list methods, each starting from the list 45, 78, 12, 90, 33. append of 60 adds 60 on the end. insert of 1 comma 99 puts 99 at index 1 and "
        "the rest move along. remove of 12 takes out the first 12 and the rest close up, leaving 45, 78, 90, 33. pop takes off the last item, 33, "
        "and returns it, leaving 45, 78, 12, 90. sort puts the list in place in order, smallest first: 12, 33, 45, 78, 90.",
        ["append() adds to the end.", "insert() puts an item at a position, and the rest move along.", "remove() takes out the first item with that value.",
         "pop() removes the last item and gives it back.", "sort() orders the list in place."],
        "These methods change the list itself. They do not make a copy.")


# ------------------------------------------------------------------ flat selection

@illustration("selection-flatten")
def _flatten():
    cv = Canvas(800, 500).backdrop()
    cv.add(P.card(cv, 14, 30, 386, 340, 20, "Nested: hard to follow", "coral"), P.badge(cv, 36, 56, 1))
    nested = ["if mark >= 0:", "    if mark <= 100:", "        if mark >= 70:", '            grade = "A"', "        else:", '            grade = "B"', "    else:", '        grade = "invalid"', "else:", '    grade = "invalid"']
    cv.add(G.code(cv, 30, 74, 354, nested, title=None, size=12, numbers=False, bars={0: "#BA352D", 1: "#BA352D", 2: "#BA352D", 3: "#BA352D"}))
    cv.add(cv.text(207, 344, "three levels deep, and invalid appears twice", 12.5, 700, cls="il-ink"))
    cv.add(P.card(cv, 414, 30, 372, 340, 20, "Flat: check the bad cases first", "mint"), P.badge(cv, 436, 56, 2))
    flat = ["if mark < 0 or mark > 100:", '    grade = "invalid"', "elif mark >= 70:", '    grade = "A"', "else:", '    grade = "B"']
    cv.add(G.code(cv, 430, 74, 340, flat, title=None, size=12.5, numbers=False, bars={0: "#248049", 1: "#248049", 2: "#248049", 3: "#248049", 4: "#248049", 5: "#248049"}))
    cv.add(cv.text(600, 232, "one level, and every case is in the open", 12.5, 700, cls="il-ink"))
    for i, (a_, b_) in enumerate((("Guard first", "deal with the invalid values straight away"), ("elif chain", "only one branch ever runs"))):
        y = 262 + i * 50
        cv.add(P.tick(cv, 446, y + 4, 9), cv.text(466, y + 2, a_, 13.5, 800, anchor="start", cls="il-ink"), cv.text(466, y + 20, b_, 12.5, 650, anchor="start", cls="il-ink2"))
    cv.add(P.card(cv, 14, 390, 772, 92, 18, "The same answer, in a shape you can read", "sky"), P.badge(cv, 36, 416, 3))
    for i, (t, col) in enumerate((("mark = 85", "slate"), ("mark = 55", "slate"), ("mark = 120", "slate"))):
        x = 44 + i * 250
        cv.add(chip(cv, x, 438, 110, 32, t, "#FFFFFF", INK, 13.5), P.arrow(cv, [(x + 116, 454), (x + 138, 454)], ARROW, 3, 8), chip(cv, x + 146, 438, 90, 32, ("A", "B", "invalid")[i], ("#C9F3E0", "#C9EAFB", "#FDE7E4")[i], INK, 14))
    return figure(
        "selection-flatten", cv, "The same grading code written as nested ifs and as a flat if, elif, else chain",
        "The same grading code written two ways. Nested ifs go three levels deep, checking mark is at least 0, then at most 100, then at least 70, "
        "and the word invalid appears twice, so the code is hard to follow. The flat version checks the bad cases first, if mark is below 0 or "
        "above 100 then the grade is invalid, then elif mark is at least 70 the grade is A, else the grade is B. It is one level deep, every case "
        "is in the open and only one branch ever runs. Both give the same answers: a mark of 85 is A, 55 is B and 120 is invalid.",
        ["Nested ifs push the code to the right and repeat cases.", "A flat chain checks the invalid values first and then the normal cases. Only one branch runs.",
         "Both give the same answers, but the flat one is easier to read and to test."],
        "Flatten selection: guard against bad values first, then use elif for the normal cases.")
