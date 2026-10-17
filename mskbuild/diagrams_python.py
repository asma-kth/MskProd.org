"""Diagrams for the GCSE Python topics, and the algorithm diagrams the A Level shares.

Every figure here is a picture of something the page's code actually does, and
where a number appears in a picture it was produced by running the same
algorithm, not typed in, so a caption can never disagree with the program
beside it.

Stepped figures follow one rule: every stage ADDS to the picture and none
redraws what an earlier stage drew, so with JavaScript off, when every stage is
visible at once, the figure reads as the finished diagram and not as a pile of
overlapping states.

Registered into the shared registry: `!diagram py-<name>` works as everywhere.
"""
import math

from .diagrams import (diagram, TEAL, TEAL_SOFT, LILAC, LILAC_SOFT, WARN,
                       WARN_SOFT, FILL, LINE, MUTED)
from .svg import (figure, figure_steps, step, box, text, line, path, circle,
                  chip)

FILL2 = "var(--dg-fill-2)"
SOFT = "var(--dg-line-soft)"
INK = "var(--dg-text)"
PAPER = "var(--dg-paper)"


# ---------------------------------------------------------------- helpers

def rect(x, y, w, h, fill="none", stroke="none", sw=1.5, r=0, opacity=None,
         dash=None):
    """A bare rectangle, for the overlays that box() has no way to draw."""
    o = ' fill-opacity="%s"' % opacity if opacity is not None else ""
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    return ('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s"%s '
            'stroke="%s" stroke-width="%s"%s/>' % (x, y, w, h, r, fill, o, stroke, sw, d))


def cell(x, y, w, h, label, fill=FILL, stroke=LINE, size=12, weight=600,
         ink=INK, r=0, mono=True, sw=1.5):
    """A box with a centred value, the unit every array diagram is made of."""
    return (rect(x, y, w, h, fill=fill, stroke=stroke, sw=sw, r=r)
            + text(x + w / 2, y + h / 2 + size * 0.35, label, size, weight,
                   fill=ink, mono=mono))


def tri_up(x, y, size=9, fill=INK):
    """A small pointer triangle with its tip at (x, y)."""
    return ('<path d="M%s %s L%s %s L%s %s Z" fill="%s"/>'
            % (x, y, x - size * 0.7, y + size, x + size * 0.7, y + size, fill))


# ============================================ binary search, run for real

@diagram("py-binary-search")
def _binary_search():
    data = [3, 8, 12, 17, 21, 25, 30, 36, 41, 47, 52, 58, 63, 70, 76]
    target = 63
    x0, y0, cw, ch = 50, 92, 44, 36

    low, high, hist = 0, len(data) - 1, []
    while low <= high:
        mid = (low + high) // 2
        rec = {"low": low, "high": high, "mid": mid, "val": data[mid]}
        if data[mid] == target:
            rec["why"] = "found it"
            rec["kind"] = "found"
        elif data[mid] < target:
            rec["why"] = "%d < %d, so low = %d" % (data[mid], target, mid + 1)
            rec["kind"] = "right"
            low = mid + 1
        else:
            rec["why"] = "%d > %d, so high = %d" % (data[mid], target, mid - 1)
            rec["kind"] = "left"
            high = mid - 1
        hist.append(rec)
        if rec["kind"] == "found":
            break

    base = [text(380, 22, "Binary search for %d in a sorted list of %d items"
                 % (target, len(data)), 12, 650, fill=MUTED)]
    for i, v in enumerate(data):
        base.append(cell(x0 + i * cw, y0, cw, ch, str(v), r=0, size=12))
        base.append(text(x0 + i * cw + cw / 2, y0 + ch + 15, str(i), 9.5, 500,
                         fill=MUTED, mono=True))
    base.append(text(x0, y0 + ch + 32, "position", 9.5, 500, anchor="start", fill=MUTED))
    # The working table, drawn once; the rows appear stage by stage.
    ty = 186
    heads = [("#", 60), ("low", 110), ("high", 170), ("mid", 230), ("items[mid]", 320),
             ("decision", 420)]
    for label, hx in heads:
        base.append(text(hx, ty, label, 10.5, 700, anchor="start", fill=MUTED, mono=True))
    base.append(line(50, ty + 8, 710, ty + 8, stroke=SOFT, w=1))

    def rows_to(k):
        out = []
        for j in range(k):
            r = hist[j]
            y = ty + 28 + j * 26
            out.append(text(60, y, str(j + 1), 11, 700, anchor="start", fill=TEAL, mono=True))
            for val, hx in ((r["low"], 110), (r["high"], 170), (r["mid"], 230), (r["val"], 320)):
                out.append(text(hx, y, str(val), 11, 600, anchor="start", mono=True))
            out.append(text(420, y, r["why"], 11, 500, anchor="start", mono=True,
                            fill=TEAL if r["kind"] == "found" else INK))
        return "".join(out)

    def stage(k):
        out = []
        # Ruled out cells first, drawn opaque so that drawing them again in a
        # later stage changes nothing, then the markers on top.
        for j in range(k):
            r = hist[j]
            if r["kind"] == "right":
                span = (r["low"], r["mid"])
            elif r["kind"] == "left":
                span = (r["mid"], r["high"])
            else:
                span = None
            if span:
                for i in range(span[0], span[1] + 1):
                    out.append(cell(x0 + i * cw, y0, cw, ch, str(data[i]), fill=FILL2, stroke=SOFT,
                                    ink=MUTED, size=12, weight=500))
        for j in range(k):
            r = hist[j]
            cx = x0 + r["mid"] * cw + cw / 2
            hit = r["kind"] == "found"
            col = TEAL if hit else WARN
            out.append(rect(x0 + r["mid"] * cw, y0, cw, ch, stroke=col, sw=3 if hit else 2.2, r=2))
            out.append(chip(cx, y0 - 24, str(j + 1), fill=TEAL_SOFT if hit else WARN_SOFT,
                            stroke=col, text_fill=col, size=11))
            out.append(line(cx, y0 - 12, cx, y0 - 2, stroke=col, w=1.8, arrow=True))
        return "".join(out) + rows_to(k)

    L = ["Looking for %d. The list is sorted, so the middle item says which half to throw away." % target]
    for j, r in enumerate(hist):
        if r["kind"] == "found":
            L.append("Comparison %d: position %d holds %d. Found, after only %d comparisons."
                     % (j + 1, r["mid"], r["val"], j + 1))
        else:
            L.append("Comparison %d: the middle of positions %d to %d is %d, which is %d. %s."
                     % (j + 1, r["low"], r["high"], r["mid"], r["val"], r["why"]))
    steps = [step(1, text(x0, 58, "target = %d" % target, 12, 700, anchor="start", fill=TEAL, mono=True), L[0])]
    for k in range(1, len(hist) + 1):
        steps.append(step(k + 1, stage(k), L[k]))
    desc = ("A binary search for %d in a sorted list of fifteen numbers, from 3 up to 76. "
            "The first comparison is with position 7, which holds 36. 36 is less than 63, so "
            "positions 0 to 7 are ruled out and low becomes 8. The second comparison is with "
            "position 11, which holds 58. That is still less than 63, so positions 8 to 11 are "
            "ruled out and low becomes 12. The third is with position 13, which holds 70. That "
            "is more than 63, so positions 13 and 14 are ruled out and high becomes 12. The "
            "fourth is with position 12, which holds 63, so the search ends after four "
            "comparisons. A linear search of the same list would have needed thirteen." % target)
    return figure_steps("py-binary", 760, 330, "".join(base), steps,
                        "Binary search narrowing the list", desc,
                        "Every comparison halves what is left, so doubling the list adds only "
                        "one more comparison.", labels=L)


# ===================================================== merge sort, split and merge

@diagram("py-merge-sort")
def _merge_sort():
    items = [38, 27, 43, 3, 9, 82, 10]
    xs = [112 + i * 86 for i in range(7)]
    cw, ch = 40, 30
    rows_y = [52 + r * 54 for r in range(7)]

    def group(row, i0, i1, values, fill, stroke):
        x = xs[i0] - 6
        w = xs[i1] + cw - xs[i0] + 12
        o = [rect(x, rows_y[row] - 6, w, ch + 12, fill=fill, stroke=stroke, sw=1.4, r=8)]
        for k, v in enumerate(values):
            o.append(text(xs[i0 + k] + cw / 2, rows_y[row] + ch / 2 + 4.5, str(v), 12.5, 650,
                          mono=True))
        return "".join(o)

    # The divide half: (first position, last position) for each group, per row.
    split_rows = [[(0, 6)], [(0, 3), (4, 6)], [(0, 1), (2, 3), (4, 5), (6, 6)],
                  [(i, i) for i in range(7)]]

    def sorted_groups(spans):
        return [sorted(items[a:b + 1]) for a, b in spans]

    merge_rows = [[(0, 1), (2, 3), (4, 5), (6, 6)], [(0, 3), (4, 6)], [(0, 6)]]

    body = [text(380, 22, "Merge sort on seven items: divide, then merge", 12, 650, fill=MUTED)]
    for row, spans in enumerate(split_rows):
        for a, b in spans:
            body.append(group(row, a, b, items[a:b + 1], TEAL_SOFT if row < 3 else WARN_SOFT,
                              TEAL if row < 3 else WARN))
    for k, spans in enumerate(merge_rows):
        row = 4 + k
        for (a, b), vals in zip(spans, sorted_groups(spans)):
            body.append(group(row, a, b, vals, LILAC_SOFT, LILAC))

    # Margin labels and the arrows that say which way time runs.
    body.append(line(16, 50, 16, 206, stroke=TEAL, w=2, arrow=True, marker="ah-accent"))
    body.append(text(28, 118, "DIVIDE", 10.5, 750, anchor="start", fill=TEAL))
    body.append(text(28, 134, "into halves", 9.5, 500, anchor="start", fill=MUTED))
    body.append(text(28, 232, "single items", 9.5, 500, anchor="start", fill=MUTED))
    body.append(text(28, 244, "are sorted", 9.5, 500, anchor="start", fill=MUTED))
    body.append(line(16, 392, 16, 262, stroke=LILAC, w=2, arrow=True, marker="ah-alt"))
    body.append(text(28, 322, "MERGE", 10.5, 750, anchor="start", fill=LILAC))
    body.append(text(28, 338, "in order", 9.5, 500, anchor="start", fill=MUTED))
    body.append(text(380, 434, "Merging two sorted lists only ever looks at the front of each, "
                     "so it is quick. Splitting costs nothing.", 11, 600, fill=MUTED))
    desc = ("Merge sort on the list 38, 27, 43, 3, 9, 82, 10. The divide half splits the list "
            "into 38, 27, 43, 3 and 9, 82, 10, then into 38, 27 and 43, 3 and 9, 82 and 10, "
            "and finally into seven single items, which are each already sorted. The merge "
            "half joins neighbours back together in order: 27, 38 and 3, 43 and 9, 82 and 10, "
            "then 3, 27, 38, 43 and 9, 10, 82, and finally the whole list in order: 3, 9, 10, "
            "27, 38, 43, 82.")
    return figure("py-merge", 760, 452, "".join(body), "Merge sort: divide, then merge", desc,
                  "Splitting down to single items is free. All of the work is in the merging.")


# ================================================= GCSE: range and the exam loop

@diagram("py-range-numbers")
def _range_numbers():
    cases = [("for i = 1 to 5", "range(1, 6)", [1, 2, 3, 4, 5], 6),
             ("for i = 0 to 20 step 5", "range(0, 21, 5)", [0, 5, 10, 15, 20], 21),
             ("for i = 10 to 1 step -3", "range(10, 0, -3)", [10, 7, 4, 1], 0)]
    body = [text(380, 22, "The exam loop and the Python that matches it", 12, 650, fill=MUTED)]
    for r, (exam, py, vals, stop) in enumerate(cases):
        y = 50 + r * 82
        body.append(text(24, y + 14, exam, 11.5, 650, anchor="start", mono=True, fill=LILAC))
        body.append(text(24, y + 34, py, 11.5, 650, anchor="start", mono=True, fill=TEAL))
        for k, v in enumerate(vals):
            body.append(cell(300 + k * 54, y, 46, 36, str(v), fill=TEAL_SOFT, stroke=TEAL, r=6))
        sx = 300 + len(vals) * 54
        body.append(cell(sx, y, 46, 36, str(stop), fill=WARN_SOFT, stroke=WARN, r=6, ink=WARN))
        body.append(line(sx + 3, y + 4, sx + 43, y + 32, stroke=WARN, w=1.8))
        body.append(text(sx + 23, y + 56, "stop: never included", 9.5, 600, fill=WARN))
        body.append(text(300 + (len(vals) * 54 - 8) / 2, y + 56, "the loop runs for these", 9.5, 600, fill=TEAL))
    body.append(text(380, 300, "The stop value is always one past the last number you want, "
                     "in whichever direction the loop counts.", 11, 650, fill=MUTED))
    desc = ("Three exam loops beside their Python. For i equals 1 to 5 is range 1, 6: the loop "
            "runs for 1, 2, 3, 4 and 5, and the stop value 6 is not used. For i equals 0 to 20 "
            "step 5 is range 0, 21, 5: the loop runs for 0, 5, 10, 15 and 20, and 21 is not "
            "used. For i equals 10 to 1 step minus 3 is range 10, 0, minus 3: the loop runs "
            "for 10, 7, 4 and 1, and the stop value 0 is not used. The stop value is always "
            "one past the last wanted number in the direction of counting.")
    return figure("py-range", 760, 320, "".join(body), "Exam loops and range", desc,
                  "Write down the last value you want, then move one step past it.")


# ================================================= GCSE: arrays and grids

@diagram("py-array-grid")
def _array_grid():
    body = [text(190, 22, "One dimensional array", 12, 650, fill=MUTED),
            text(560, 22, "Two dimensional array", 12, 650, fill=MUTED)]
    # 1D
    vals = [12, 18, 0, 0, 7]
    for i, v in enumerate(vals):
        body.append(cell(40 + i * 56, 70, 52, 38, str(v), fill=TEAL_SOFT if i == 2 else FILL,
                         stroke=TEAL if i == 2 else LINE, r=4))
        body.append(text(66 + i * 56, 128, str(i), 11, 650, fill=MUTED, mono=True))
    body.append(text(40, 150, "position", 10, 500, anchor="start", fill=MUTED))
    body.append(text(180, 190, "scores[2]", 13, 700, fill=TEAL, mono=True))
    body.append(text(180, 210, "holds 0, the third box", 10.5, 500, fill=MUTED))
    body.append(text(180, 252, "Positions run from 0 to 4,", 10.5, 600, fill=MUTED))
    body.append(text(180, 268, "so scores[5] does not exist.", 10.5, 600, fill=WARN))
    # 2D
    gx, gy = 440, 80
    grid = [[0, 0, 0, 0], [0, 0, 9, 0], [0, 0, 0, 0]]
    for c in range(4):
        body.append(text(gx + 26 + c * 52, gy - 8, str(c), 11, 650, fill=MUTED, mono=True))
    body.append(text(gx - 6, gy - 22, "column", 10, 500, anchor="end", fill=MUTED))
    for r in range(3):
        body.append(text(gx - 12, gy + 28 + r * 44, str(r), 11, 650, anchor="end", fill=MUTED, mono=True))
        for c in range(4):
            hit = (r, c) == (1, 2)
            body.append(cell(gx + c * 52, gy + r * 44, 52, 44, str(grid[r][c]),
                             fill=LILAC_SOFT if hit else FILL, stroke=LILAC if hit else LINE))
    body.append(text(gx - 12, gy + 150, "row", 10, 500, anchor="end", fill=MUTED))
    body.append(text(gx + 104, gy + 176, "grid[1][2]", 13, 700, fill=LILAC, mono=True))
    body.append(text(gx + 104, gy + 196, "row 1, then column 2", 10.5, 500, fill=MUTED))
    body.append(text(gx + 104, gy + 232, "Rows first, then columns.", 10.5, 600, fill=MUTED))
    desc = ("Two arrays. A one dimensional array called scores holds 12, 18, 0, 0 and 7 in "
            "positions 0 to 4, and scores at position 2 holds 0. There is no position 5. A "
            "two dimensional array called grid has three rows and four columns, all zero "
            "except one nine, in row 1, column 2, which is written grid, one, two, with the "
            "row index first and the column index second.")
    return figure("py-arrays", 760, 330, "".join(body), "Arrays and grids", desc,
                  "A grid is a list of rows. The first index picks the row, the second the box in it.")


# ================================================= GCSE: scope

@diagram("py-scope")
def _scope():
    body = [rect(20, 40, 720, 296, fill=FILL2, stroke=LINE, sw=1.6, r=12),
            text(40, 64, "MAIN PROGRAM", 11, 750, anchor="start", fill=MUTED),
            text(40, 84, "global scope: every subprogram can read these", 10.5, 500, anchor="start", fill=MUTED),
            box(40, 104, 200, 54, None, fill=WARN_SOFT, stroke=WARN, r=8),
            text(140, 126, "VAT = 0.2", 12.5, 700, mono=True, fill=WARN),
            text(140, 146, "total_sales = 0", 12.5, 700, mono=True, fill=WARN)]
    # two functions
    body += [box(300, 100, 190, 200, None, fill=TEAL_SOFT, stroke=TEAL, r=10),
             text(395, 124, "price_with_vat(price)", 11.5, 700, mono=True, fill=TEAL),
             text(395, 146, "local scope", 10, 500, fill=MUTED),
             box(316, 158, 158, 58, None, fill=FILL, stroke=TEAL, r=6),
             text(395, 180, "price", 12, 650, mono=True),
             text(395, 200, "result", 12, 650, mono=True),
             text(395, 252, "created when called,", 10, 500, fill=MUTED),
             text(395, 268, "gone when it returns", 10, 500, fill=MUTED)]
    body += [box(530, 100, 190, 200, None, fill=LILAC_SOFT, stroke=LILAC, r=10),
             text(625, 124, "report()", 11.5, 700, mono=True, fill=LILAC),
             text(625, 146, "local scope", 10, 500, fill=MUTED),
             box(546, 158, 158, 58, None, fill=FILL, stroke=LILAC, r=6),
             text(625, 180, "line", 12, 650, mono=True),
             text(625, 200, "price", 12, 650, mono=True),
             text(625, 252, "a different price:", 10, 500, fill=MUTED),
             text(625, 268, "no clash", 10, 500, fill=MUTED)]
    # reads of a global
    body += [path("M300 132 C 270 132, 262 132, 242 132", stroke=TEAL, w=2, arrow=True, marker="ah-accent"),
             text(272, 122, "can read", 9.5, 650, fill=TEAL),
             path("M625 300 L625 322 L140 322 L140 162", stroke=LILAC, w=2, arrow=True, marker="ah-alt", dash="5 4"),
             text(382, 316, "report() reads total_sales", 9.5, 650, fill=LILAC)]
    # no sight between the two
    body += [line(492, 200, 528, 200, stroke=WARN, w=2, dash="4 4"),
             text(510, 190, "no", 10, 700, fill=WARN),
             text(510, 218, "view", 10, 700, fill=WARN)]
    desc = ("Variable scope. The main program holds the global variables VAT, 0.2, and "
            "total_sales, 0, which every subprogram can read. The function price_with_vat has "
            "its own local variables price and result, which exist only while it is running. "
            "The procedure report has its own local variables line and price. The two price "
            "variables are different variables and do not clash. Neither subprogram can see "
            "the other's locals.")
    return figure("py-scope", 760, 350, "".join(body), "Local and global variables", desc,
                  "A local variable is created when its subprogram is called and gone when it "
                  "returns. That is why two functions can both use the name price.")


# ================================================= GCSE: kinds of test data

@diagram("py-test-data")
def _test_data():
    x0, y0, w = 80, 130, 600
    lo, hi = -3, 14
    def X(v):
        return x0 + (v - lo) / (hi - lo) * w
    body = [text(380, 22, "A program that accepts whole numbers from 1 to 10", 12, 650, fill=MUTED)]
    # valid band
    body.append(rect(X(1), y0 - 30, X(10) - X(1), 60, fill=TEAL_SOFT, stroke=TEAL, sw=1.4, r=6))
    body.append(text((X(1) + X(10)) / 2, y0 - 38, "ACCEPTED", 10.5, 750, fill=TEAL))
    body.append(line(x0, y0, x0 + w, y0, stroke=LINE, w=1.8))
    for v in range(lo, hi + 1):
        body.append(line(X(v), y0 - 4, X(v), y0 + 4, stroke=LINE, w=1.2))
        body.append(text(X(v), y0 + 20, str(v), 9.5, 500, fill=MUTED, mono=True))
    def dot(v, label, kind, fill, stroke, ink, dy=-58):
        cx = X(v)
        return (circle(cx, y0, 7, fill=fill, stroke=stroke, w=2)
                + line(cx, y0 - 8, cx, y0 + dy + 8, stroke=stroke, w=1.2)
                + chip(cx, y0 + dy, label, fill=fill, stroke=stroke, text_fill=ink, size=10.5))
    body.append(dot(5, "5", "normal", TEAL_SOFT, TEAL, TEAL, -70))
    body.append(dot(7, "7", "normal", TEAL_SOFT, TEAL, TEAL, -70))
    body.append(dot(1, "1", "boundary", LILAC_SOFT, LILAC, LILAC, -62))
    body.append(dot(10, "10", "boundary", LILAC_SOFT, LILAC, LILAC, -62))
    body.append(dot(0, "0", "boundary", LILAC_SOFT, LILAC, LILAC, 52))
    body.append(dot(11, "11", "boundary", LILAC_SOFT, LILAC, LILAC, 52))
    body.append(dot(-2, "-2", "invalid", WARN_SOFT, WARN, WARN, 52))
    body.append(dot(13, "13", "invalid", WARN_SOFT, WARN, WARN, 52))
    # legend
    ly = 232
    items = [("Normal", "typical valid data: 5, 7", TEAL, TEAL_SOFT),
             ("Boundary", "the edge, and one step outside: 1, 10 and 0, 11", LILAC, LILAC_SOFT),
             ("Invalid", "the right type, not allowed: -2, 13, 250", WARN, WARN_SOFT),
             ("Erroneous", "the wrong type: \"ten\", 4.5, an empty entry", MUTED, FILL2)]
    for i, (name, desc_, ink, soft) in enumerate(items):
        yy = ly + (i % 2) * 28
        xx = 40 + (i // 2) * 360
        body.append(rect(xx, yy - 13, 14, 14, fill=soft, stroke=ink, sw=1.6, r=3))
        body.append(text(xx + 22, yy - 1, name, 11, 700, anchor="start", fill=ink))
        body.append(text(xx + 92, yy - 1, desc_, 10.5, 500, anchor="start", fill=INK))
    desc = ("A number line from minus 3 to 14 for a program that accepts whole numbers from 1 "
            "to 10. The accepted band runs from 1 to 10. Normal data, such as 5 and 7, lies "
            "inside it. Boundary data is 1 and 10, on the edge and accepted, and 0 and 11, "
            "one step outside and rejected. Invalid data, such as minus 2 and 13, is the right "
            "type but outside the range and is rejected. Erroneous data is the wrong type "
            "altogether, such as the word ten, 4.5 or an empty entry, and is rejected.")
    return figure("py-testdata", 760, 290, "".join(body), "Kinds of test data", desc,
                  "Test both sides of every edge. Most off by one errors hide on the boundary.")


# ================================================= GCSE: the anatomy of SELECT

@diagram("py-sql-anatomy")
def _sql_anatomy():
    rows = [(1, "Asha", 10, 56), (2, "Ben", 11, 71), (3, "Chloe", 10, 38),
            (4, "Dev", 11, 90), (5, "Esme", 10, 64), (6, "Alan", 11, 45)]
    heads = ["StudentID", "Name", "Year", "Mark"]
    colw = [86, 80, 56, 56]
    tx, ty, rh = 40, 112, 30
    cx = [tx + sum(colw[:i]) for i in range(4)]
    match = [r for r in rows if r[2] == 11 and r[3] >= 60]

    body = [text(380, 22, "SELECT Name, Mark FROM Student WHERE Year = 11 AND Mark >= 60",
                 12, 700, mono=True, fill=INK)]
    for c, h in enumerate(heads):
        body.append(cell(cx[c], ty, colw[c], rh, h, fill=FILL2, size=10.5, weight=700, ink=MUTED))
    for r, row in enumerate(rows):
        for c, v in enumerate(row):
            body.append(cell(cx[c], ty + rh * (r + 1), colw[c], rh, str(v), size=11.5))
    body.append(text(tx + sum(colw) / 2, ty - 14, "Student", 11, 700, fill=MUTED, mono=True))
    # the result table, drawn empty; its rows appear in the last stage
    rx = 470
    body.append(text(rx + 70, ty - 14, "result", 11, 700, fill=MUTED, mono=True))
    body.append(cell(rx, ty, 90, rh, "Name", fill=FILL2, size=10.5, weight=700, ink=MUTED))
    body.append(cell(rx + 90, ty, 60, rh, "Mark", fill=FILL2, size=10.5, weight=700, ink=MUTED))

    lx, ly = rx, 282
    s1 = (rect(tx - 4, ty - 4, sum(colw) + 8, rh * 7 + 8, stroke=LILAC, sw=2.6, r=6)
          + text(lx, ly, "FROM: look in this table", 11, 700, anchor="start", fill=LILAC))
    s2 = ""
    for r, row in enumerate(rows):
        if row in match:
            s2 += rect(tx - 2, ty + rh * (r + 1) + 1, sum(colw) + 4, rh - 2, stroke=WARN, sw=2.6, r=4)
    s2 += text(lx, ly + 22, "WHERE: keep only these rows", 11, 700, anchor="start", fill=WARN)
    s3 = ""
    for r, row in enumerate(rows):
        if row in match:
            for c in (1, 3):
                s3 += rect(cx[c] + 2, ty + rh * (r + 1) + 3, colw[c] - 4, rh - 6, stroke=TEAL, sw=2.4, r=4)
    s3 += rect(cx[1] + 2, ty + 3, colw[1] - 4, rh - 6, stroke=TEAL, sw=2.4, r=4)
    s3 += rect(cx[3] + 2, ty + 3, colw[3] - 4, rh - 6, stroke=TEAL, sw=2.4, r=4)
    s3 += text(lx, ly + 44, "SELECT: show only these columns", 11, 700, anchor="start", fill=TEAL)
    s3 += path("M%s %s L%s %s" % (tx + sum(colw) + 14, ty + 110, rx - 14, ty + 110),
               stroke=TEAL, w=2.2, arrow=True, marker="ah-accent")
    for k, row in enumerate(match):
        s3 += cell(rx, ty + rh * (k + 1), 90, rh, row[1], fill=TEAL_SOFT, stroke=TEAL, size=11.5)
        s3 += cell(rx + 90, ty + rh * (k + 1), 60, rh, str(row[3]), fill=TEAL_SOFT, stroke=TEAL, size=11.5)
    L = ["FROM names the table to search, so the whole Student table is the starting point.",
         "WHERE tests every row, and keeps only Year 11 students with a mark of 60 or more: Ben and Dev.",
         "SELECT picks the columns to show from the rows that are left. Only Name and Mark appear."]
    steps = [step(i + 1, b, L[i]) for i, b in enumerate([s1, s1 + s2, s1 + s2 + s3])]
    desc = ("How one SELECT query works on the Student table of six students. FROM Student "
            "starts with the whole table. WHERE Year equals 11 AND Mark is at least 60 keeps "
            "only the rows for Ben, who is in Year 11 and scored 71, and Dev, who is in Year "
            "11 and scored 90. Alan is in Year 11 but scored 45, and Esme scored 64 but is in "
            "Year 10, so neither is kept. SELECT Name, Mark then shows only those two "
            "columns, giving the result Ben 71 and Dev 90.")
    return figure_steps("py-sql", 760, 340, "".join(body), steps, "Reading a SELECT query", desc,
                        "Read a query in the order the computer does: FROM, then WHERE, then SELECT.",
                        labels=L)


# ================================================= GCSE: a trace table filling in

@diagram("py-trace-table")
def _trace_table():
    code = ["number = 4721", "total = 0", "while number > 0:", "    digit = number % 10",
            "    total = total + digit", "    number = number // 10", "print(total)"]
    number, total, rows = 4721, 0, []
    while number > 0:
        digit = number % 10
        total += digit
        number //= 10
        rows.append((digit, total, number))
    heads = ["pass", "digit", "total", "number"]
    colw = [54, 70, 70, 80]
    tx, ty, rh = 410, 70, 32
    cx = [tx + sum(colw[:i]) for i in range(4)]
    body = [text(380, 22, "A trace table fills in one pass at a time", 12, 650, fill=MUTED)]
    for i, line_ in enumerate(code):
        body.append(text(30, 66 + i * 28, line_, 12.5, 550, anchor="start", mono=True))
    body.append(text(tx + sum(colw) / 2, ty - 18, "TRACE TABLE", 10.5, 750, fill=TEAL))
    for c, h in enumerate(heads):
        body.append(cell(cx[c], ty, colw[c], rh, h, fill=FILL2, size=10.5, weight=700, ink=MUTED))
    start = (0, 0, 4721)
    body.append(cell(cx[0], ty + rh, colw[0], rh, "start", size=10.5))
    body.append(cell(cx[1], ty + rh, colw[1], rh, "", size=11.5))
    body.append(cell(cx[2], ty + rh, colw[2], rh, "0", size=11.5))
    body.append(cell(cx[3], ty + rh, colw[3], rh, "4721", size=11.5))
    for r, (digit, tot, num) in enumerate(rows):
        y = ty + rh * (r + 2)
        for c, v in enumerate((r + 1, digit, tot, num)):
            body.append(cell(cx[c], y, colw[c], rh, str(v), size=11.5))
    out_y = ty + rh * (len(rows) + 2)
    body.append(text(tx + 10, out_y + 24, "output:", 11, 650, anchor="start", fill=MUTED, mono=True))
    body.append(text(tx + 80, out_y + 24, str(total), 13, 750, anchor="start", fill=TEAL, mono=True))

    def hl_code(i):
        return rect(22, 66 + i * 28 - 18, 340, 25, stroke=TEAL, sw=2, r=5)
    def hl_row(r):
        y = ty + rh * (r + 1)
        return rect(tx - 3, y - 2, sum(colw) + 6, rh + 4, stroke=TEAL, sw=2.6, r=5)
    L = ["Before the loop, total is 0 and number is 4721.",
         "Pass 1: number % 10 is 1, the last digit. total becomes 1 and number loses its last digit.",
         "Pass 2: the digit is 2. total is now 3 and number is 47.",
         "Pass 3: the digit is 7. total is 10 and number is 4.",
         "Pass 4: the digit is 4. total is 14 and number is 0, so number > 0 is false.",
         "The loop ends, and print shows the total, 14."]
    steps = [step(1, hl_code(0) + hl_code(1) + hl_row(1), L[0])]
    for r in range(4):
        steps.append(step(r + 2, hl_code(3) + hl_code(4) + hl_code(5) + hl_row(r + 2), L[r + 1]))
    steps.append(step(6, hl_code(6) + rect(tx - 3, out_y + 4, sum(colw) + 6, 30, stroke=TEAL, sw=2.6, r=5), L[5]))
    desc = ("A trace table for a program that adds up the digits of 4721. Before the loop, "
            "total is 0 and number is 4721. Pass one takes the last digit, 1, so total becomes "
            "1 and number becomes 472. Pass two takes 2, total 3, number 47. Pass three takes "
            "7, total 10, number 4. Pass four takes 4, total 14, number 0, and the loop stops "
            "because number is no longer greater than 0. The program outputs 14.")
    return figure_steps("py-trace", 760, 330, "".join(body), steps, "Filling in a trace table", desc,
                        "One row for each pass, one column for each variable, and the value after the pass.",
                        labels=L)
