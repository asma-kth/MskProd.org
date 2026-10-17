"""A last set of illustrations for the topics with the most words to the fewest pictures: file size
calculations, running unit tests, evaluating postfix with a stack, comparing sorts, A* against
Dijkstra, a flowchart beside its code, and laying out a tkinter window."""
import heapq
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


def chip(cv, x, y, w, h, text, fill="#FFFFFF", tc=INK, size=14, stroke="#9FB3BE", mono=True, weight=800, r=None):
    return cv.rect(x, y, w, h, r if r is not None else min(9, h / 2.4), fill, stroke=stroke, sw=1.5) + cv.text(x + w / 2, y + h / 2 + size * .36, text, size, weight, fill=tc, mono=mono)


# ------------------------------------------------------------------ file size calculations

@illustration("file-size-formulas")
def _filesize():
    cv = Canvas(800, 500).backdrop()
    spec = [("Image", "sky", [("width", "1,000"), ("× height", "800"), ("× colour depth", "24")], "19,200,000 bits", "2,400,000 bytes", "2.4 MB"),
            ("Sound", "plum", [("sample rate", "44,100"), ("× bit depth", "16"), ("× seconds", "10")], "7,056,000 bits", "882,000 bytes", "0.88 MB"),
            ("Text", "mint", [("characters", "2,000"), ("× bits each", "8"), None], "16,000 bits", "2,000 bytes", "2 KB")]
    for n, (title, col, rows, bits, byts, big) in enumerate(spec):
        x = (14, 277, 540)[n]
        cv.add(P.card(cv, x, 30, 246, 328, 18, title, col), P.badge(cv, x + 16, 54, n + 1))
        for i, row in enumerate(rows):
            if row is None:
                continue
            y = 76 + i * 40
            cv.add(cv.text(x + 18, y + 20, row[0], 13, 700, anchor="start", cls="il-ink"))
            cv.add(chip(cv, x + 140, y + 2, 92, 28, row[1], "#FFFFFF", INK, 14.5))
        cv.add(cv.line(x + 18, 202, x + 228, 202, "var(--il-line)", 1.6))
        cv.add(cv.text(x + 18, 232, "= " + bits, 15, 800, anchor="start", cls="il-ink", mono=True))
        cv.add(cv.text(x + 18, 262, "÷ 8 = " + byts, 13, 750, anchor="start", cls="il-ink", mono=True))
        cv.add(P.lift(cv, x + 18, 286, 210, 46, col, 12, 5, hl=False), cv.text(x + 123, 317, big, 22, 800, fill="#FFFFFF" if col == "plum" else INK, mono=True))
    cv.add(P.card(cv, 14, 378, 772, 106, 18, "From bits to bigger units", "sun"), P.badge(cv, 36, 404, 4))
    tiles = [("bits", "slate"), ("bytes", "sky"), ("KB", "mint"), ("MB", "coral"), ("GB", "plum")]
    labels = ["÷ 8", "÷ 1000", "÷ 1000", "÷ 1000"]
    x = 40
    for i, (t, col) in enumerate(tiles):
        cv.add(P.lift(cv, x, 418, 90, 38, col, 10, 4, hl=False), cv.text(x + 45, 443, t, 16, 800, fill="#FFFFFF" if col == "plum" else INK, mono=True))
        if i < 4:
            cv.add(P.arrow(cv, [(x + 96, 437), (x + 150, 437)], ARROW, 3.5, 10), cv.text(x + 123, 428, labels[i], 12.5, 800, cls="il-ink", mono=True))
        x += 150
    cv.add(cv.text(400, 474, "OCR, AQA and Key Stage 3 divide by 1000. Edexcel divides by 1024 and writes KiB, MiB and GiB.", 12.5, 650, cls="il-ink2"))
    return figure(
        "file-size-formulas", cv, "File size formulas for an image, a sound and a piece of text, each worked through to a size in bytes",
        "The file size of three kinds of data, each worked through from the formula to a size. For an image, multiply the width by the height by "
        "the colour depth: 1,000 times 800 times 24 is 19,200,000 bits, which divided by 8 is 2,400,000 bytes, or 2.4 megabytes. For a sound, "
        "multiply the sample rate by the bit depth by the number of seconds: 44,100 times 16 times 10 is 7,056,000 bits, which divided by 8 is "
        "882,000 bytes, or 0.88 megabytes. For text, multiply the number of characters by the bits per character: 2,000 times 8 is 16,000 bits, "
        "which divided by 8 is 2,000 bytes, or 2 kilobytes. To move up the units, divide bits by 8 for bytes, then by 1,000 for kilobytes, "
        "megabytes and gigabytes. OCR, AQA and Key Stage 3 use 1,000. Edexcel uses 1,024 and the names kibibyte, mebibyte and gibibyte.",
        ["Image: width × height × colour depth. Every pixel costs the colour depth in bits.", "Sound: sample rate × bit depth × seconds, and × 2 for stereo.",
         "Text: number of characters × bits per character. ASCII uses 8.", "Divide by 8 to turn bits into bytes, then by 1,000 for each step up."],
        "Every file size question is the same three steps: multiply, divide by 8, then change the unit. Show each step.")


# ------------------------------------------------------------------ unit tests

@illustration("unittest-run")
def _unittest():
    cv = Canvas(800, 500).backdrop()
    lines = ["import unittest", "from shapes import area", "", "class TestArea(unittest.TestCase):", "    def test_square(self):", "        self.assertEqual(area(4, 4), 16)",
             "    def test_zero(self):", "        self.assertEqual(area(0, 5), 0)", "    def test_negative(self):", "        self.assertEqual(area(-2, 3), 0)"]
    cv.add(G.code(cv, 14, 30, 430, lines, title="test_shapes.py", size=12.5, numbers=True, hl=(9,), bars={5: "#62CFA3", 7: "#62CFA3", 9: "#F77F72"}), P.badge(cv, 34, 28, 1))
    cv.add(G.terminal(cv, 462, 30, 324, [("..F", "#FFDA8A"), ("FAIL: test_negative", "#FF9A91"), ("AssertionError: -6 != 0", "#FF9A91"), ("Ran 3 tests in 0.001s", "#CFE8DC"), ("FAILED (failures=1)", "#FF9A91")], "python -m unittest", 12.5), P.badge(cv, 482, 28, 2))
    cv.add(P.arrow(cv, [(444, 130), (456, 130)], ARROW, 3, 8))
    cv.add(P.card(cv, 462, 218, 324, 118, 16, "Reading the result", "teal"), P.badge(cv, 482, 244, 3))
    for i, (sym, t, col) in enumerate(((".", "a test passed", "mint"), ("F", "a test failed: the answer was wrong", "coral"), ("E", "an error: the code crashed", "sun"))):
        y = 256 + i * 26
        cv.add(P.lift(cv, 480, y, 26, 22, col, 6, 3, hl=False), cv.text(493, y + 16, sym, 14, 800, fill=INK, mono=True), cv.text(516, y + 16, t, 13, 700, anchor="start", cls="il-ink"))
    cv.add(P.card(cv, 14, 356, 772, 126, 18, "Red, then fix, then green", "coral"), P.badge(cv, 36, 382, 4))
    steps = [("Run the tests", "see which fail", "sky"), ("Read the message", "actual -6, expected 0", "sun"), ("Fix the code", "area must not go negative", "coral"), ("Run them all again", "..., 3 passed", "mint")]
    for i, (a_, b_, col) in enumerate(steps):
        x = 36 + i * 190
        cv.add(P.lift(cv, x, 402, 172, 62, col, 12, 5, hl=False), cv.text(x + 86, 428, a_, 14, 800, fill=INK), cv.text(x + 86, 448, b_, 12, 650, fill=INK))
        if i < 3:
            cv.add(P.arrow(cv, [(x + 176, 433), (x + 186, 433)], ARROW, 3, 7))
    return figure(
        "unittest-run", cv, "A unittest file with three tests, the result of running it, and how to read it",
        "A test file using Python's unittest module. The class TestArea has three tests. test square checks that area of 4 and 4 equals 16, test "
        "zero checks that area of 0 and 5 equals 0, and test negative checks that area of minus 2 and 3 equals 0. Running the file prints a result: "
        "a dot for each test that passed and an F for each that failed, here dot, dot, F. The failure message names the test and shows the actual "
        "answer, minus 6, against the expected one, 0, then reports ran 3 tests, failed with one failure. A dot means a test passed, an F means a "
        "test failed because the answer was wrong, and an E means an error where the code crashed. The cycle is to run the tests, read the message, "
        "fix the code and run all the tests again.",
        ["Each test method checks one thing with assertEqual(actual, expected).", "The runner prints a dot for a pass and an F for a failure, then the message.",
         "Read the symbols: a dot passed, F is a wrong answer, E is a crash.", "Run, read, fix, run again. Re-run every test, so a fix cannot break something else."],
        "A failing test is useful information. It tells you exactly what the code got wrong.")


# ------------------------------------------------------------------ postfix

@illustration("postfix-stack")
def _postfix():
    cv = Canvas(800, 500).backdrop()
    cv.add(P.band(cv, 14, 24, 772, 66, 16), P.badge(cv, 36, 57, 1))
    cv.add(cv.text(64, 52, "infix", 12.5, 700, anchor="start", cls="il-ink2"), cv.text(64, 74, "(3 + 4) * 2", 21, 800, anchor="start", cls="il-ink", mono=True))
    cv.add(P.arrow(cv, [(266, 60), (356, 60)], ARROW, 4, 12), cv.text(311, 50, "shunting yard", 12, 750, cls="il-ink2"))
    cv.add(cv.text(380, 52, "postfix", 12.5, 700, anchor="start", cls="il-ink2"), cv.text(380, 74, "3 4 + 2 *", 21, 800, anchor="start", cls="il-ink", mono=True))
    cv.add(cv.text(560, 52, "no brackets needed:", 12.5, 700, anchor="start", cls="il-ink2"), cv.text(560, 72, "the order is the meaning", 13, 750, anchor="start", cls="il-ink"))
    steps = [("3", "push 3", [3], "sky"), ("4", "push 4", [3, 4], "sky"), ("+", "pop 4 and 3, push 3 + 4 = 7", [7], "coral"), ("2", "push 2", [7, 2], "sky"), ("*", "pop 2 and 7, push 7 × 2 = 14", [14], "coral")]
    cv.add(P.card(cv, 14, 106, 772, 376, 18, "Evaluate it with a stack, one token at a time", "teal"), P.badge(cv, 36, 132, 2))
    for i, (tok, what, stack, col) in enumerate(steps):
        x = 30 + i * 150
        cv.add(P.lift(cv, x + 38, 150, 64, 40, "sun" if tok in "+*" else "paper", 10, 4, hl=False), cv.text(x + 70, 178, tok, 22, 800, fill=INK, mono=True))
        cv.add(cv.text(x + 70, 144, "token %d" % (i + 1), 12, 700, cls="il-ink2"))
        # the stack: a tall open box with tiles piling up from the bottom
        bx, by, bw, bh = x + 30, 212, 80, 160
        cv.add(cv.path("M%s %s L%s %s L%s %s L%s %s" % (bx, by, bx, by + bh, bx + bw, by + bh, bx + bw, by), stroke="#8AA0AC", sw=4))
        for k, v in enumerate(stack):
            ty = by + bh - 6 - (k + 1) * 38
            cv.add(P.lift(cv, bx + 8, ty, bw - 16, 32, col, 8, 3, hl=False), cv.text(bx + bw / 2, ty + 22, str(v), 17, 800, fill=INK, mono=True))
        for j, ln in enumerate(wrap(what, 20)):
            cv.add(cv.text(x + 70, 402 + j * 16, ln, 12.5, 700, cls="il-ink"))
        if i < 4:
            cv.add(P.arrow(cv, [(x + 120, 290), (x + 148, 290)], ARROW, 3, 8))
    cv.add(P.pill(cv, 400, 456, "The answer is the one value left on the stack: 14.", "sun", 14.5, 16, 28, 800), P.badge(cv, 120, 456, 3))
    return figure(
        "postfix-stack", cv, "Evaluating the postfix expression 3 4 + 2 * with a stack, one token at a time",
        "The infix expression, 3 plus 4 in brackets, times 2, is converted by the shunting yard algorithm into the postfix expression 3 4 + 2 *, "
        "which needs no brackets because the order of the tokens is the meaning. It is evaluated with a stack, one token at a time. The token 3 is "
        "pushed, so the stack holds 3. The token 4 is pushed, so the stack holds 3 and 4. The token plus pops 4 and 3 and pushes their sum, 7. The "
        "token 2 is pushed, so the stack holds 7 and 2. The token times pops 2 and 7 and pushes 14. The answer is the one value left on the stack, 14.",
        ["Infix has the operator between the numbers and needs brackets. Postfix puts the operator after them.", "Numbers are pushed on the stack. An operator pops two values, applies itself and pushes the result.",
         "When the tokens run out, the single value left on the stack is the answer."],
        "Postfix is easy for a computer because it needs no brackets and no rules about precedence: just a stack.")


# ------------------------------------------------------------------ comparing the sorts

@illustration("sort-compare")
def _sortcmp():
    cv = Canvas(800, 500).backdrop()
    cv.add(P.card(cv, 14, 30, 772, 330, 18, "The four sorts side by side", "teal"), P.badge(cv, 36, 56, 1))
    cols = [("Best", 262), ("Average", 372), ("Worst", 482), ("Extra memory", 598), ("Stable", 706)]
    for t, cx in cols:
        cv.add(cv.text(cx, 90, t, 13.5, 800, cls="il-ink"))
    good, ok, bad = "mint", "sun", "coral"
    rows = [("Bubble", [("O(n)", good), ("O(n²)", bad), ("O(n²)", bad), ("O(1)", good), ("yes", good)]),
            ("Insertion", [("O(n)", good), ("O(n²)", bad), ("O(n²)", bad), ("O(1)", good), ("yes", good)]),
            ("Merge", [("O(n log n)", ok), ("O(n log n)", ok), ("O(n log n)", ok), ("O(n)", bad), ("yes", good)]),
            ("Quick", [("O(n log n)", ok), ("O(n log n)", ok), ("O(n²)", bad), ("O(log n)", good), ("no", bad)])]
    for i, (name, cells) in enumerate(rows):
        y = 104 + i * 60
        if i % 2 == 0:
            cv.add(cv.rect(26, y, 748, 54, 10, "var(--il-band)"))
        cv.add(cv.text(44, y + 33, name, 16, 800, anchor="start", cls="il-ink"))
        for (t, c), (_, cx) in zip(cells, cols):
            w = len(t) * 7.9 + 18
            cv.add(P.lift(cv, cx - w / 2, y + 10, w, 32, c, 9, 4, hl=False), cv.text(cx, y + 31, t, 13, 800, fill=INK, mono=True))
    for i, (c, t) in enumerate(((good, "good"), (ok, "fair"), (bad, "poor"))):
        cv.add(P.lift(cv, 44 + i * 96, 340, 22, 14, c, 4, 2, hl=False), cv.text(72 + i * 96, 352, t, 12.5, 700, anchor="start", cls="il-ink2"))
    cv.add(P.card(cv, 14, 380, 772, 102, 18, "Which one to choose", "sun"), P.badge(cv, 36, 406, 2))
    for i, (a_, b_, col) in enumerate((("Nearly sorted", "insertion sort: close to O(n)", "sky"), ("Guaranteed speed", "merge sort: always O(n log n)", "mint"), ("Fastest on average", "quick sort, in place", "coral"))):
        x = 34 + i * 250
        cv.add(P.lift(cv, x, 422, 236, 48, col, 10, 4, hl=False), cv.text(x + 118, 443, a_, 14, 800, fill=INK), cv.text(x + 118, 461, b_, 12, 650, fill=INK))
    return figure(
        "sort-compare", cv, "Bubble, insertion, merge and quick sort compared on speed, memory and stability",
        "A table compares four sorting algorithms. Bubble sort is O of n at best, if it stops when a pass makes no swaps, O of n squared on average and "
        "at worst, uses O of 1 extra memory and is stable. Insertion sort has the same times, O of n best, O of n squared average and worst, "
        "O of 1 memory, and is stable. Merge sort is O of n log n in every case, uses O of n extra memory, and is stable. Quick sort is O of "
        "n log n on average and at best, but O of n squared at worst, uses O of log n memory for its recursion, and is not stable. To choose: "
        "insertion sort for data that is nearly sorted, merge sort when guaranteed speed matters, and quick sort for the fastest on average, done in place.",
        ["Compare the sorts on best, average and worst case time, on extra memory, and on whether they are stable.", "Choose by the situation: nearly sorted, guaranteed speed, or fastest on average."],
        "Quote the case when you give a complexity. Quick sort is O(n log n) on average but O(n²) at worst.")


# ------------------------------------------------------------------ A* against Dijkstra

def search_grid(heuristic):
    """Run a search on a small grid with a wall, and return the cells it looked at and the path it found."""
    W, H = 12, 9
    walls = {(6, y) for y in range(2, 8)}
    start, goal = (1, 4), (10, 4)
    h = (lambda p: abs(p[0] - goal[0]) + abs(p[1] - goal[1])) if heuristic else (lambda p: 0)
    heap, cnt = [(h(start), 0, 0, start)], 0
    g, came, seen = {start: 0}, {}, []
    while heap:
        f, _, gc, cur = heapq.heappop(heap)
        if cur in seen:
            continue
        seen.append(cur)
        if cur == goal:
            break
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nb = (cur[0] + dx, cur[1] + dy)
            if not (0 <= nb[0] < W and 0 <= nb[1] < H) or nb in walls:
                continue
            ng = g[cur] + 1
            if ng < g.get(nb, 1 << 30):
                g[nb] = ng
                came[nb] = cur
                cnt += 1
                heapq.heappush(heap, (ng + h(nb), h(nb), cnt, nb))
    path, cur = [], goal
    while cur != start:
        path.append(cur)
        cur = came[cur]
    path.append(start)
    return seen, path[::-1], walls, start, goal, W, H


@illustration("a-star-heuristic")
def _astar():
    cv = Canvas(800, 500).backdrop()
    cs = 30
    for k, (x, title, col, use_h) in enumerate(((14, "Dijkstra: looks everywhere", "sky", False), (406, "A*: looks towards the goal", "mint", True))):
        seen, path, walls, start, goal, W, H = search_grid(use_h)
        cv.add(P.card(cv, x, 30, 380, 340, 18, title, col), P.badge(cv, x + 22, 56, k + 1))
        ox, oy = x + 10, 72
        for gx in range(W):
            for gy in range(H):
                p = (gx, gy)
                fill = "#FFFFFF"
                if p in walls:
                    fill = "#4A5A64"
                elif p in seen:
                    fill = "#C9EAFB" if not use_h else "#C9F3E0"
                cv.add(cv.rect(ox + gx * cs, oy + gy * cs, cs, cs, 0, fill, stroke="#D5DEE4", sw=.8))
        cv.add(cv.path("M" + " L".join("%s %s" % (_n(ox + (px + .5) * cs), _n(oy + (py + .5) * cs)) for px, py in path), stroke="#C84B43", sw=4))
        cv.add(cv.circle(ox + (start[0] + .5) * cs, oy + (start[1] + .5) * cs, 9, "#248049", stroke="#FFFFFF", sw=2.4), cv.text(ox + (start[0] + .5) * cs, oy + (start[1] + .5) * cs + 4.5, "S", 12, 800, fill="#FFFFFF"))
        cv.add(cv.circle(ox + (goal[0] + .5) * cs, oy + (goal[1] + .5) * cs, 9, "#BA352D", stroke="#FFFFFF", sw=2.4), cv.text(ox + (goal[0] + .5) * cs, oy + (goal[1] + .5) * cs + 4.5, "G", 12, 800, fill="#FFFFFF"))
        cv.add(cv.rect(x + 40, 338, 300, 26, 13, "#FFFFFF", op=.96), cv.text(x + 190, 356, "looked at %d cells, path of %d steps" % (len(seen), len(path) - 1), 13.5, 800, fill=INK))
    cv.add(P.card(cv, 14, 390, 772, 92, 18, "The only difference is a guess", "sun"), P.badge(cv, 36, 416, 3))
    cv.add(cv.text(40, 444, "Dijkstra picks the cell with the smallest distance from the start: g.", 14, 700, anchor="start", cls="il-ink"))
    cv.add(cv.text(40, 466, "A* picks the smallest g + h, where h is a guess of the distance left, so it favours cells that look closer to the goal.", 13.5, 700, anchor="start", cls="il-ink"))
    return figure(
        "a-star-heuristic", cv, "Dijkstra and A* finding a path round a wall, and how many cells each one looks at",
        "Two searches find a path from S on the left to G on the right round a wall. Dijkstra's algorithm picks the cell with the smallest "
        "distance from the start, so it spreads out in every direction and looks at a large area of the grid. A star picks the cell with the "
        "smallest distance travelled plus a heuristic guess of the distance left, so it favours cells that look closer to the goal and looks at "
        "far fewer cells. Both find a shortest path of the same length, drawn in red. The explored cells are shaded blue for Dijkstra and green for A star.",
        ["Dijkstra explores in every direction, cell by cell in order of distance from the start.", "A* adds a heuristic, a guess of the distance still to go, so it heads for the goal.",
         "The difference is one guess: g for Dijkstra, g plus h for A*. The heuristic must never overestimate."],
        "A* finds the same shortest path as Dijkstra, but looks at far fewer cells, as long as the heuristic never overestimates.")


# ------------------------------------------------------------------ a flowchart beside its code

@illustration("flowchart-to-code")
def _flow2code():
    cv = Canvas(800, 500).backdrop()
    cv.add(P.card(cv, 14, 30, 380, 452, 18, "The flowchart", "teal"), P.badge(cv, 36, 56, 1))

    def oval(cx, cy, t):
        return cv.rect(cx - 52, cy - 17, 104, 34, 17, cv.g("slate"), stroke=PAL["slate"][2], sw=2) + cv.text(cx, cy + 5, t, 14, 800, fill=INK)

    def para(cx, cy, t, col, w=176):
        pts = [(cx - w / 2 + 14, cy - 18), (cx + w / 2 + 14, cy - 18), (cx + w / 2 - 14, cy + 18), (cx - w / 2 - 14, cy + 18)]
        return cv.poly(pts, cv.g(col), stroke=PAL[col][2], sw=2) + cv.text(cx, cy + 5, t, 13, 800, fill=INK, mono=True)

    cv.add(oval(204, 82, "Start"))
    cv.add(P.arrow(cv, [(204, 99), (204, 128)], ARROW, 3, 9))
    cv.add(para(204, 148, 'input age', "sky"))
    cv.add(P.arrow(cv, [(204, 166), (204, 196)], ARROW, 3, 9))
    cv.add(cv.path("M204 198 L284 240 L204 282 L124 240 Z", fill=cv.g("sun"), stroke=PAL["sun"][2], sw=2.4), cv.text(204, 245, "age >= 18 ?", 13, 800, fill=INK, mono=True))
    cv.add(cv.text(300, 232, "yes", 13, 800, anchor="start", cls="il-ink"), cv.text(108, 232, "no", 13, 800, anchor="end", cls="il-ink"))
    cv.add(P.arrow(cv, [(284, 240), (320, 240), (320, 290)], ARROW, 3, 9), P.arrow(cv, [(124, 240), (88, 240), (88, 290)], ARROW, 3, 9))
    cv.add(para(326, 310, 'output "Adult"', "mint", 120), para(82, 310, 'output "Child"', "coral", 120))
    cv.add(cv.path("M326 328 L326 372 L204 372", stroke=ARROW, sw=3), cv.path("M82 328 L82 372 L204 372", stroke=ARROW, sw=3))
    cv.add(P.arrow(cv, [(204, 372), (204, 408)], ARROW, 3, 9), oval(204, 428, "End"))
    colors = {"input": "#66B8EC", "decision": "#FFCC4A", "adult": "#62CFA3", "child": "#F77F72"}
    cv.add(G.code(cv, 410, 30, 376, ['age = int(input("Age? "))', "if age >= 18:", '    print("Adult")', "else:", '    print("Child")'], title="age.py", size=13, numbers=False,
                  bars={0: colors["input"], 1: colors["decision"], 2: colors["adult"], 3: colors["decision"], 4: colors["child"]}), P.badge(cv, 430, 28, 2))
    cv.add(G.code(cv, 410, 196, 376, ['age = input("Age? ")', "if age >= 18 then", '    print("Adult")', "else", '    print("Child")', "endif"], title="the same, in pseudocode", size=13, numbers=False,
                  bars={0: colors["input"], 1: colors["decision"], 2: colors["adult"], 3: colors["decision"], 4: colors["child"], 5: colors["decision"]}), P.badge(cv, 430, 194, 3))
    cv.add(P.card(cv, 410, 394, 376, 88, 16))
    for i, (t, col) in enumerate((("input, output", "sky"), ("decision", "sun"), ("start, end", "slate"))):
        cv.add(P.pill(cv, 428 + i * 124, 416, t, col, 12.5, 10, 24, 750, anchor="start"))
    cv.add(cv.text(598, 462, "same colour = same step, in all three", 13, 750, cls="il-ink"))
    return figure(
        "flowchart-to-code", cv, "One algorithm as a flowchart, as Python and as pseudocode, with matching steps in matching colours",
        "The same algorithm written three ways. The flowchart starts, inputs an age, then reaches a decision diamond that asks whether age is "
        "greater than or equal to 18. If yes it outputs Adult, if no it outputs Child, and both paths join and reach the end. The Python code "
        "has the same steps: age equals int of input, if age is at least 18 print Adult, else print Child. The pseudocode is the same again, "
        "ending with endif. The input is coloured blue, the decision yellow, and the two outputs green and red in all three versions, so each "
        "step can be matched across them. Rounded ovals mean start and end, slanted boxes mean input and output, and a diamond means a decision.",
        ["The flowchart: ovals for start and end, slanted boxes for input and output, a diamond for a decision with a yes branch and a no branch.",
         "The Python version has the same steps, matched by colour.", "The pseudocode is the same algorithm again. Only the notation changes."],
        "A flowchart, pseudocode and a program are three ways to write one algorithm. Practise moving between them.")


# ------------------------------------------------------------------ laying out a tkinter window

@illustration("tk-grid")
def _tkgrid():
    cv = Canvas(800, 500).backdrop()
    cv.add(P.card(cv, 14, 30, 400, 310, 18, "grid(): rows and columns", "teal"), P.badge(cv, 36, 56, 1))
    gx, gy, cw, rh = 76, 112, 100, 62
    for c in range(3):
        cv.add(cv.text(gx + c * cw + cw / 2, gy - 8, "column %d" % c, 12.5, 750, cls="il-ink2"))
    for r in range(3):
        cv.add(cv.text(gx - 8, gy + r * rh + rh / 2 + 4, "row %d" % r, 12.5, 750, anchor="end", cls="il-ink2"))
    for r in range(3):
        for c in range(3):
            cv.add(cv.rect(gx + c * cw + 1, gy + r * rh + 1, cw - 2, rh - 2, 6, "var(--il-band)", stroke="#8AA0AC", sw=1.2, dash="4 4"))
    # widgets
    cv.add(cv.rect(gx + 8, gy + 14, cw - 16, 34, 6, "#DDF3FA", stroke="#2F82C0", sw=2), cv.text(gx + cw / 2, gy + 36, "Name:", 13.5, 750, fill=INK, mono=True))
    cv.add(cv.rect(gx + cw + 8, gy + 14, 2 * cw - 16, 34, 6, "#FFFFFF", stroke="#0F7C84", sw=2), cv.text(gx + cw + 18, gy + 36, "Aisha", 13.5, 750, anchor="start", fill=INK, mono=True))
    cv.add(cv.rect(gx + 8, gy + rh + 14, cw - 16, 34, 6, "#DDF3FA", stroke="#2F82C0", sw=2), cv.text(gx + cw / 2, gy + rh + 36, "Mark:", 13.5, 750, fill=INK, mono=True))
    cv.add(cv.rect(gx + cw + 8, gy + rh + 14, cw - 16, 34, 6, "#FFFFFF", stroke="#0F7C84", sw=2), cv.text(gx + cw + 18, gy + rh + 36, "72", 13.5, 750, anchor="start", fill=INK, mono=True))
    cv.add(cv.rect(gx + 2 * cw + 8, gy + rh + 14, cw - 16, 34, 8, "#FFE9A8", stroke="#B98A12", sw=2), cv.text(gx + 2.5 * cw, gy + rh + 36, "Add", 13.5, 800, fill=INK))
    cv.add(cv.rect(gx + 8, gy + 2 * rh + 8, 3 * cw - 16, rh - 16, 6, "#FFFFFF", stroke="#C84B43", sw=2), cv.text(gx + 18, gy + 2 * rh + 30, "Aisha   72", 13, 650, anchor="start", fill=INK, mono=True))
    cv.add(cv.text(214, 322, "columnspan lets a widget cross several columns", 12.5, 650, cls="il-ink2"))
    cv.add(G.code(cv, 430, 30, 356, ["name_label.grid(row=0, column=0)", "name_entry.grid(row=0, column=1,", "               columnspan=2)", "mark_label.grid(row=1, column=0)", "mark_entry.grid(row=1, column=1)", "add_button.grid(row=1, column=2)", "listbox.grid(row=2, column=0,", "             columnspan=3)"],
                  title="layout.py", size=11.5, numbers=False, bars={0: "#66B8EC", 1: "#25B3BB", 3: "#66B8EC", 4: "#25B3BB", 5: "#FFCC4A", 6: "#F77F72"}), P.badge(cv, 450, 28, 2))
    cv.add(P.card(cv, 14, 360, 772, 122, 18, "Three ways to place a widget", "sun"), P.badge(cv, 36, 386, 3))
    mini = [("pack()", "one after another, top to bottom", "sky"), ("grid()", "a table of rows and columns", "mint"), ("place()", "exact x and y, rarely used", "coral")]
    for i, (name, sub, col) in enumerate(mini):
        x = 34 + i * 250
        cv.add(P.lift(cv, x, 408, 236, 56, col, 12, 5, hl=False), cv.text(x + 118, 432, name, 16, 800, fill=INK, mono=True), cv.text(x + 118, 452, sub, 12.5, 650, fill=INK))
    return figure(
        "tk-grid", cv, "A tkinter window laid out with grid, the code that does it, and the three layout managers",
        "How grid lays out a tkinter window. The window is a table of three columns and three rows. A Label reading Name is in row 0, column 0. "
        "An Entry holding Aisha is in row 0, column 1 and uses columnspan 2 so that it crosses columns 1 and 2. A Label reading Mark is in row 1, "
        "column 0, an Entry holding 72 is in row 1, column 1, and a Button labelled Add is in row 1, column 2. A Listbox is in row 2, column 0 with "
        "columnspan 3 so that it crosses the whole width. The code beside it has one grid call for each widget, with the row and column. Below "
        "are the three layout managers: pack puts widgets one after another, grid places them in a table of rows and columns, and place puts them at an "
        "exact x and y position and is rarely used. Use one manager in each container.",
        ["Grid is a table. Every widget gets a row and a column, counted from 0.", "One grid() call per widget, and columnspan lets a widget cross several columns.",
         "pack, grid and place are the three layout managers. Use only one of them inside a container."],
        "Plan the window as a table on paper first, then every grid() call is just reading off a cell.")
