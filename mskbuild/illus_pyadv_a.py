"""Illustrations for the Advanced Python topics, set one: names and objects, copies, generators, pipelines,
decorators, context managers, special methods, exceptions, the standard library and version control."""
from .illus import Canvas, PAL, INK, ARROW, figure, illustration, _n
from . import illus_props as P
from . import illus_glyphs as G
from .illus_pyalevel_a import node


def tag(cv, x, y, text, color="sun", w=None):
    """A name tag: a small label with a pointed right edge, the way a name is attached to an object. (x, y) is its centre."""
    w = w or (len(text) * 11 + 26)
    x0, y0, h = x - w / 2, y - 15, 30
    d = "M%s %s L%s %s L%s %s L%s %s L%s %s Z" % (_n(x0 + 8), _n(y0), _n(x0 + w - 14), _n(y0), _n(x0 + w), _n(y), _n(x0 + w - 14), _n(y0 + h), _n(x0 + 8), _n(y0 + h))
    out = cv.path(d, fill=cv.g(color), stroke=PAL[color][2], sw=1.8)
    return out + cv.text(x - 4, y + 6, text, 16, 800, fill=INK, mono=True)


def list_box(cv, x, y, items, color="sky", cell=44, hot=False):
    """A list object: a row of cells. (x, y) is the top left."""
    n = len(items)
    out = cv.rect(x - 4, y - 4, n * cell + 8, 52, 12, "#FFFFFF", stroke="#C84B43" if hot else "#9FB3BE", sw=2.6 if hot else 1.6)
    for i, v in enumerate(items):
        out += cv.rect(x + i * cell + 2, y, cell - 4, 44, 8, cv.g(color)) + cv.text(x + i * cell + cell / 2, y + 29, str(v), 18, 800, fill=INK, mono=True)
    return out


# ------------------------------------------------------------------ names and objects

@illustration("names-objects")
def _names():
    cv = Canvas(800, 480).backdrop()
    cv.add(P.card(cv, 14, 24, 330, 432, 20, "the code", "teal"))
    cv.add(G.code(cv, 30, 80, 298, ["a = [1, 2, 3]", "b = a", "b.append(4)", "c = [1, 2, 3, 4]"], title=None, size=14, numbers=False, bars={0: "#66B8EC", 1: "#FFCC4A", 2: "#C84B43", 3: "#62CFA3"}, h=140))
    for i, (t, c) in enumerate((("a name is attached to an object", "#66B8EC"), ("b is another name for the same list", "#FFCC4A"), ("the one list changes: both names see it", "#C84B43"), ("c is a different list with equal contents", "#62CFA3"))):
        cv.add(cv.rect(34, 244 + i * 44, 10, 28, 4, c), cv.text(54, 264 + i * 44, t, 13.5, 700, anchor="start", cls="il-ink"))
    cv.add(P.badge(cv, 42, 64, 1))
    cv.add(P.card(cv, 360, 24, 426, 432, 20, "names and objects", "sun"))
    cv.add(tag(cv, 420, 120, "a", "sky", 70), tag(cv, 420, 188, "b", "sun", 70))
    cv.add(P.arrow(cv, [(458, 120), (528, 150)], ARROW, 3, 10), P.arrow(cv, [(458, 188), (528, 168)], ARROW, 3, 10))
    cv.add(list_box(cv, 534, 134, [1, 2, 3, 4], "sky", 44, True))
    cv.add(cv.text(622, 208, "one list object", 13, 700, cls="il-ink2"))
    cv.add(P.badge(cv, 392, 74, 2))
    cv.add(tag(cv, 420, 330, "c", "mint", 70))
    cv.add(P.arrow(cv, [(458, 330), (528, 330)], ARROW, 3, 10))
    cv.add(list_box(cv, 534, 308, [1, 2, 3, 4], "mint", 44))
    cv.add(cv.text(622, 382, "a second list object", 13, 700, cls="il-ink2"))
    cv.add(P.badge(cv, 392, 280, 3))
    cv.add(cv.text(384, 424, "a is b: True", 14, 800, anchor="start", cls="il-ok", mono=True), cv.text(512, 424, "a == c: True", 14, 800, anchor="start", cls="il-ok", mono=True), cv.text(646, 424, "a is c: False", 14, 800, anchor="start", cls="il-bad", mono=True))
    return figure(
        "names-objects", cv, "Names are labels attached to objects: two names for one list, and an equal list that is a different object",
        "Four lines of code. a equals a list of 1, 2, 3 makes a list object and attaches the name a to it. b equals a does not copy anything: it "
        "attaches a second name, b, to the same list. b dot append 4 changes that one list, so both a and b show 1, 2, 3, 4. c equals a new list "
        "1, 2, 3, 4 makes a different object with equal contents. So a is b is true, because they are the same object. a equals equals c is true, "
        "because the values are equal. a is c is false, because they are two different objects.",
        ["Assignment attaches a name to an object. Nothing is copied.", "A second name for the same list: a change made through either name is seen through both.",
         "Equal values are not the same object. == compares values, and is asks whether two names are attached to one object."],
        "A Python variable is closer to a label on an object than to a box that holds a value.")


# ------------------------------------------------------------------ alias, shallow copy, deep copy

@illustration("copy-depth")
def _copies():
    cv = Canvas(800, 540).backdrop()
    titles = (("alias", "b = a", "teal"), ("shallow copy", "b = a[:]", "sun"), ("deep copy", "b = copy.deepcopy(a)", "plum"))
    for k, (title, code, color) in enumerate(titles):
        x0 = 14 + k * 264
        cv.add(P.card(cv, x0, 24, 252, 486, 20, title, color))
        cv.add(cv.text(x0 + 138, 78, code, 13, 800, cls="il-ink", mono=True))
        cv.add(P.badge(cv, x0 + 28, 70, k + 1))

    def outer(x, y, rows_color, hot=False):
        """An outer list holding two row lists side by side."""
        out = cv.rect(x, y, 214, 72, 12, "#FFFFFF", stroke="#6F8794", sw=2.2)
        out += list_box(cv, x + 14, y + 12, [0, 0], rows_color, 34, hot)
        out += list_box(cv, x + 118, y + 12, [0, 0], rows_color, 34, hot)
        return out

    def hang(x, y, name, color):
        """A name tag above an outer list, with an arrow down into it."""
        return tag(cv, x + 107, y - 36, name, color, 64) + P.arrow(cv, [(x + 107, y - 18), (x + 107, y - 2)], ARROW, 2.6, 9)

    def verdict(cx, text, cls):
        return cv.text(cx, 488, text, 13, 800, cls=cls)

    def link_label(x, y, text, stroke):
        """A label that sits over the connecting lines, on a white pill so the lines stop behind it."""
        return cv.rect(x + 22, y - 12, 170, 24, 12, "#FFFFFF", stroke=stroke, sw=1.6) + cv.text(x + 107, y + 5, text, 12.5, 800, fill=INK)

    # alias: two names, one object
    x = 14 + 19
    cv.add(tag(cv, x + 62, 192, "a", "sky", 64), tag(cv, x + 152, 192, "b", "sun", 64))
    cv.add(P.arrow(cv, [(x + 62, 210), (x + 90, 242)], ARROW, 2.6, 9), P.arrow(cv, [(x + 152, 210), (x + 124, 242)], ARROW, 2.6, 9))
    cv.add(outer(x, 246, "sky"))
    cv.add(cv.text(14 + 126, 350, "one outer list", 13.5, 800, cls="il-ink"), cv.text(14 + 126, 372, "holding one pair of rows", 13, 700, cls="il-ink2"))
    cv.add(cv.text(14 + 126, 436, "nothing is copied:", 14, 800, cls="il-ink"), cv.text(14 + 126, 458, "everything is shared", 14, 800, cls="il-ink"))
    cv.add(verdict(14 + 126, "a[0][0] = 9 changes b too", "il-bad"))
    # shallow copy: two outer lists, the same rows
    x = 14 + 264 + 19
    cv.add(hang(x, 150, "a", "sky"), outer(x, 150, "sky", True))
    cv.add(hang(x, 336, "b", "sun"), outer(x, 336, "sky", True))
    for rx in (x + 14 + 38, x + 118 + 38):
        cv.add(cv.line(rx, 226, rx, 342, "#C84B43", 3, dash="6 5"))
    cv.add(link_label(x, 254, "same two row objects", "#C84B43"))
    cv.add(cv.text(14 + 264 + 126, 436, "a new outer list,", 14, 800, cls="il-ink"), cv.text(14 + 264 + 126, 458, "but shared rows", 14, 800, cls="il-ink"))
    cv.add(verdict(14 + 264 + 126, "a[0][0] = 9 changes b too", "il-bad"))
    # deep copy: two outer lists, separate rows
    x = 14 + 528 + 19
    cv.add(hang(x, 150, "a", "sky"), outer(x, 150, "sky"))
    cv.add(hang(x, 336, "b", "sun"), outer(x, 336, "mint"))
    cv.add(link_label(x, 254, "separate row objects", "#2E8B67"))
    cv.add(cv.text(14 + 528 + 126, 436, "everything is copied:", 14, 800, cls="il-ink"), cv.text(14 + 528 + 126, 458, "nothing is shared", 14, 800, cls="il-ink"))
    cv.add(verdict(14 + 528 + 126, "a[0][0] = 9 leaves b alone", "il-ok"))
    return figure(
        "copy-depth", cv, "An alias, a shallow copy and a deep copy of a list of lists",
        "Three ways of making b from a list that holds two row lists. Left, an alias, b equals a: a and b are two names for the very same outer "
        "list, so nothing is copied and everything is shared. Middle, a shallow copy, b equals a slice of everything: b is a new outer list, but its "
        "two slots refer to the same two row lists as a, shown by the red dashed lines, so changing a row through one name is seen through the "
        "other. Right, a deep copy: b is a new outer list holding new copies of the rows, so nothing is shared and the two never affect each other.",
        ["An alias is no copy at all: one object with two names.", "A shallow copy makes a new outer list, but the items inside it are the same objects.",
         "A deep copy copies the container and everything inside it, to any depth."],
        "Use the shallowest copy that is safe. A deep copy costs time and memory, and a shallow one shares anything mutable inside.")


# ------------------------------------------------------------------ a generator pauses

@illustration("generator-pause")
def _generator():
    cv = Canvas(800, 500).backdrop()
    cv.add(P.card(cv, 14, 24, 360, 452, 20, "a generator function", "teal"))
    lines = ["def count():", "    print('start')", "    yield 1", "    print('middle')", "    yield 2", "    print('end')"]
    colors = {1: "#66B8EC", 2: "#66B8EC", 3: "#62CFA3", 4: "#62CFA3", 5: "#C84B43"}
    cv.add(G.code(cv, 30, 80, 328, lines, title=None, size=14, numbers=False, bars=colors, h=186))
    cv.add(cv.text(194, 300, "calling count() runs nothing yet:", 13.5, 700, cls="il-ink"), cv.text(194, 320, "it just makes a generator object", 13.5, 700, cls="il-ink"))
    cv.add(G.code(cv, 30, 346, 328, ["g = count()"], title=None, size=14, numbers=False, h=52))
    cv.add(P.badge(cv, 42, 64, 1))
    rows = [("next(g)", "#66B8EC", "sky", "prints start", "returns 1", "runs to the first yield, then freezes"),
            ("next(g)", "#62CFA3", "mint", "prints middle", "returns 2", "carries on from where it froze"),
            ("next(g)", "#C84B43", "coral", "prints end", "StopIteration", "runs off the end: the loop stops")]
    cv.add(P.card(cv, 390, 24, 396, 452, 20, "each next() runs to the next yield", "sun"))
    for i, (call, col, c, prints, ret, note) in enumerate(rows):
        y = 84 + i * 128
        cv.add(cv.rect(404, y, 10, 104, 4, col))
        cv.add(P.lift(cv, 426, y, 120, 36, c, 10, 4, hl=False), cv.text(486, y + 24, call, 16, 800, fill=INK, mono=True))
        cv.add(P.arrow(cv, [(550, y + 18), (580, y + 18)], ARROW, 2.8, 9))
        cv.add(cv.text(588, y + 24, prints, 14, 800, anchor="start", cls="il-ink", mono=True))
        cv.add(cv.text(426, y + 62, "gives back:", 13, 650, anchor="start", cls="il-ink2"), P.pill(cv, 570, y + 57, ret, "paper", 14, 10, 26, 800, INK, "middle"))
        cv.add(cv.text(426, y + 94, note, 13, 650, anchor="start", cls="il-ink2"))
    cv.add(P.badge(cv, 414, 66, 2))
    return figure(
        "generator-pause", cv, "A generator pauses at each yield and carries on from the same place",
        "A generator function with six lines: print start, yield 1, print middle, yield 2, print end. Calling count does not run any of it: it only "
        "makes a generator object. The first call of next runs from the top to the first yield, so it prints start and gives back 1, and then the "
        "generator freezes with its variables kept. The second call of next carries on from that point, prints middle, and gives back 2. The third "
        "call carries on, prints end, runs off the end of the function, and raises StopIteration, which tells a loop to stop. The coloured bars "
        "match each stretch of code to the call that ran it.",
        ["Calling a generator function runs none of its body. It returns a generator object.",
         "Each next() runs the body up to the next yield, hands a value back, and freezes the generator with its state kept."],
        "Between calls the generator costs almost nothing: it holds only its place and its local variables, however long the sequence is.")


# ------------------------------------------------------------------ a pipeline of generators

@illustration("pipeline-stages")
def _pipeline():
    cv = Canvas(800, 390).backdrop()
    cv.add(P.card(cv, 14, 24, 772, 340, 20, "a lazy pipeline: one item at a time through every stage", "teal"))
    stages = [("log file", "paper", None), ("read_lines()", "sky", "yields a line"), ("parse()", "mint", "yields a record"), ("only('ERROR')", "sun", "keeps the errors"), ("for loop", "coral", "uses each one")]
    x, w, gap = 34, 128, 24
    centres = []
    for i, (name, color, sub) in enumerate(stages):
        cx = x + i * (w + gap)
        cv.add(P.lift(cv, cx, 150, w, 70, color, 12, 5, hl=False))
        cv.add(cv.text(cx + w / 2, 182, name, 15 if len(name) < 13 else 13.5, 800, fill=INK, mono=True))
        if sub:
            cv.add(cv.text(cx + w / 2, 204, sub, 12, 650, fill=INK))
        centres.append(cx + w / 2)
        if i:
            cv.add(P.arrow(cv, [(cx - gap + 4, 185), (cx - 4, 185)], ARROW, 3, 10))
    # one item on each arrow, travelling to the right
    for i, (label, fill) in enumerate((("a line", "#FFFFFF"), ("a record", "#FFFFFF"), ("an error", "#FFFFFF"), ("its message", "#C9F3E0"))):
        ax = x + (i + 1) * (w + gap) - gap / 2
        cv.add(cv.rect(ax - 52, 96, 104, 28, 9, fill, stroke="#9FB3BE", sw=1.4), cv.text(ax, 115, label, 13, 800, fill=INK, mono=True))
        cv.add(cv.line(ax, 124, ax, 176, "#9FB3BE", 1.6, dash="3 4"))
    cv.add(P.badge(cv, 42, 62, 1))
    cv.add(P.arrow(cv, [(centres[4] + 6, 240), (centres[1] - 4, 240)], ARROW, 2.4, 9, dash="6 5"))
    cv.add(cv.text(400, 266, "the loop asks for the next error, so each stage asks the stage before it", 14.5, 750, cls="il-ink"))
    cv.add(cv.text(400, 290, "a line is read only when it is needed, and nothing is held in a list", 14.5, 750, cls="il-ink"))
    cv.add(P.badge(cv, 42, 274, 2))
    cv.add(P.pill(cv, 400, 330, "memory used: one line, however big the file is", "mint", 15.5, 18, 32, 800))
    return figure(
        "pipeline-stages", cv, "A pipeline of generators: log file, read lines, parse, keep the errors, use them",
        "Five stages in a row: a log file, then read lines, parse, only ERROR, and the for loop that uses the results. Each stage is a generator "
        "that takes the items of the stage before it and yields its own. Items flow through one at a time: a line is read, turned into a record, "
        "tested, and if it is an error its message reaches the loop. A dashed arrow pointing backwards shows that the loop pulls: it asks for the "
        "next error, and each stage asks the one before it. Because a line is read only when it is needed, the memory used is one line however big "
        "the file is.",
        ["Each stage is a generator that takes the items of the stage before and yields its own.",
         "The loop pulls the data through: a line is read only when it is needed, so nothing is stored in a list."],
        "Each small stage can be tested and reused on its own, and the whole pipeline works the same on ten lines or ten billion.")


# ------------------------------------------------------------------ a decorator wraps a function

@illustration("decorator-wrap")
def _decorator():
    cv = Canvas(800, 470).backdrop()
    cv.add(P.card(cv, 14, 24, 380, 422, 20, "what you write", "teal"))
    cv.add(G.code(cv, 30, 78, 348, ["@count_calls", "def greet(name):", "    return 'Hello, ' + name"], title=None, size=14, numbers=False, hl=(0,), h=108))
    cv.add(cv.text(204, 226, "means exactly the same as", 14, 700, cls="il-ink2"))
    cv.add(G.code(cv, 30, 244, 348, ["def greet(name):", "    return 'Hello, ' + name", "", "greet = count_calls(greet)"], title=None, size=14, numbers=False, hl=(3,), h=132))
    cv.add(cv.text(204, 414, "the name greet now points at the wrapper", 14, 750, cls="il-ink"))
    cv.add(P.badge(cv, 42, 62, 1))
    cv.add(P.card(cv, 410, 24, 376, 422, 20, "what happens on a call", "sun"))
    # nested boxes
    cv.add(cv.rect(436, 88, 324, 250, 20, "#EEE2F8", stroke="#8061A9", sw=2.4))
    cv.add(cv.text(598, 118, "wrapper  (made by count_calls)", 15, 800, fill=INK, mono=False))
    cv.add(cv.rect(496, 176, 204, 100, 14, "#C9EAFB", stroke="#2F82C0", sw=2.4))
    cv.add(cv.text(598, 214, "greet(name)", 18, 800, fill=INK, mono=True), cv.text(598, 242, "the original function", 13, 700, fill=INK))
    cv.add(P.badge(cv, 436, 70, 2))
    cv.add(P.arrow(cv, [(414, 150), (452, 150)], "#C84B43", 3.4, 11))
    cv.add(cv.text(470, 154, "calls", 12.5, 800, anchor="start", fill=INK))
    cv.add(P.arrow(cv, [(598, 138), (598, 170)], ARROW, 3, 10))
    cv.add(cv.text(612, 160, "before: calls += 1", 12.5, 750, anchor="start", fill=INK, mono=True))
    cv.add(P.arrow(cv, [(598, 280), (598, 314)], ARROW, 3, 10))
    cv.add(cv.text(612, 300, "after: pass the", 12.5, 750, anchor="start", fill=INK), cv.text(612, 316, "result back", 12.5, 750, anchor="start", fill=INK))
    cv.add(cv.text(598, 366, "the caller never sees the wrapper:", 14, 750, cls="il-ink"))
    cv.add(cv.text(598, 388, "it calls greet() as usual", 14, 750, cls="il-ink"))
    cv.add(P.pill(cv, 598, 424, "functools.wraps keeps the name and docstring", "mint", 12.5, 10, 26, 800))
    return figure(
        "decorator-wrap", cv, "A decorator replaces a function with a wrapper that calls the original",
        "Left: the line at sign count calls above def greet means exactly the same as defining greet and then writing greet equals count calls of "
        "greet, so the name greet now points at a wrapper. Right: what happens when greet is called. The call goes first into the wrapper, which is "
        "made by count calls. Before it calls the original function it does its own work, here adding one to a count. It then calls the original "
        "greet, which does its job, and the wrapper passes the result back to the caller. The caller never sees the wrapper: it calls greet as "
        "usual. functools dot wraps copies the original name and docstring onto the wrapper.",
        ["The @ line is shorthand: greet = count_calls(greet). The name greet now refers to the wrapper.",
         "A call goes into the wrapper first. It adds its own behaviour, calls the original, and passes the result back."],
        "Because the wrapper is a closure it remembers the original function, which is how it can call it.")


# ------------------------------------------------------------------ the with statement

@illustration("with-block")
def _with():
    cv = Canvas(800, 480).backdrop()
    for k, (title, color, body, tail) in enumerate((("the block finishes normally", "mint", "body runs to the end", None), ("an error is raised in the block", "coral", "body stops: an error is raised", "the error carries on upwards"))):
        x0 = 14 + k * 396
        cv.add(P.card(cv, x0, 24, 376, 436, 20, title, color))
        cx = x0 + 188
        cv.add(P.lift(cv, cx - 120, 84, 240, 56, "sky", 12, 5, hl=False), cv.text(cx, 108, "with Section('A'):", 16, 800, fill=INK, mono=True), cv.text(cx, 128, "__enter__ runs: set up", 13, 650, fill=INK))
        cv.add(P.arrow(cv, [(cx, 146), (cx, 188)], ARROW, 3, 10))
        cv.add(P.lift(cv, cx - 120, 192, 240, 56, "paper" if k == 0 else "coral", 12, 5, hl=False), cv.text(cx, 216, "the block's code", 16, 800, fill=INK, mono=True), cv.text(cx, 236, body, 12.5, 650, fill=INK))
        if k == 1:
            cv.add(P.cross(cv, cx + 108, 192, 14))
        cv.add(P.arrow(cv, [(cx, 254), (cx, 296)], ARROW, 3, 10))
        cv.add(P.lift(cv, cx - 120, 300, 240, 56, "sun", 12, 5, hl=False), cv.text(cx, 324, "__exit__ ALWAYS runs", 16, 800, fill=INK, mono=True), cv.text(cx, 344, "clean up: close, release, commit", 12.5, 650, fill=INK))
        if tail:
            cv.add(P.arrow(cv, [(cx, 362), (cx, 396)], "#C84B43", 3.4, 11))
            cv.add(cv.text(cx, 420, tail, 14, 800, cls="il-bad"))
        else:
            cv.add(P.arrow(cv, [(cx, 362), (cx, 396)], ARROW, 3, 10))
            cv.add(cv.text(cx, 420, "the program carries on", 14, 800, cls="il-ok"))
        cv.add(P.badge(cv, x0 + 28, 64, k + 1))
    return figure(
        "with-block", cv, "The with statement: __enter__ at the start and __exit__ at the end, whatever happens in between",
        "Two columns. Left, the block finishes normally: with Section A runs the method __enter__ to set things up, the block's code runs to the "
        "end, and then __exit__ runs to clean up, for example closing a file, releasing a lock or committing a change, and the program carries on. "
        "Right, an error is raised in the block: the code in the block stops, but __exit__ still runs and does its clean up, and then the error "
        "carries on upwards to be handled elsewhere. __exit__ always runs, which is the whole point of using with.",
        ["A normal run: set up, the block, then clean up.",
         "If the block raises an error the clean up still happens, and then the error carries on upwards."],
        "Writing the clean up once, in the context manager, removes the risk of forgetting a close or a release on one of the paths.")


# ------------------------------------------------------------------ special methods

@illustration("dunder-map")
def _dunder():
    cv = Canvas(800, 520).backdrop()
    cv.add(P.card(cv, 14, 24, 770, 472, 20, "what you write, and the special method Python calls", "teal"))
    rows = [("a + b", "a.__add__(b)"), ("3 * a", "a.__rmul__(3)"), ("a == b", "a.__eq__(b)"), ("a < b", "a.__lt__(b)"),
            ("len(a)", "a.__len__()"), ("a[2]", "a.__getitem__(2)"), ("for x in a:", "a.__iter__()"), ("x in a", "a.__contains__(x)"),
            ("print(a)", "a.__str__()"), ("a(5)", "a.__call__(5)")]
    cv.add(cv.text(210, 80, "you write", 14, 800, cls="il-ink2"), cv.text(590, 80, "Python calls", 14, 800, cls="il-ink2"))
    for i, (src, call) in enumerate(rows):
        y = 92 + i * 38
        cv.add(P.lift(cv, 60, y, 300, 30, "sky", 10, 3, hl=False), cv.text(210, y + 21, src, 16, 800, fill=INK, mono=True))
        cv.add(P.arrow(cv, [(368, y + 15), (418, y + 15)], ARROW, 2.8, 9))
        cv.add(P.lift(cv, 426, y, 330, 30, "mint", 10, 3, hl=False), cv.text(591, y + 21, call, 16, 800, fill=INK, mono=True))
    cv.add(P.badge(cv, 42, 64, 1))
    cv.add(cv.text(400, 494, "define the methods in your class and your objects join in like the built-in types", 14, 750, cls="il-ink"))
    return figure(
        "dunder-map", cv, "Operators and built-in functions are calls to special methods",
        "Ten rows, each pairing something you write with the special method that Python calls. a plus b calls a dot __add__ of b. 3 times a calls "
        "a dot __rmul__ of 3. a equals equals b calls __eq__. a less than b calls __lt__. len of a calls __len__. a with an index in square "
        "brackets calls __getitem__. A for loop calls __iter__. x in a calls __contains__. print of a calls __str__. a called like a function with "
        "5 calls __call__. If your own class defines these methods, its objects behave like the built-in types.",
        ["Each operator, built-in function and loop is a call to a special method with double underscores at each end."],
        "That is why a class that defines __len__ and __getitem__ can be indexed, sliced, looped over and sorted without any more code.")


# ------------------------------------------------------------------ the whole try statement

@illustration("exception-flow")
def _exception():
    cv = Canvas(800, 560).backdrop()
    cv.add(P.card(cv, 14, 24, 772, 520, 20, "try, except, else and finally", "teal"))
    cx = 400
    cv.add(P.lift(cv, cx - 120, 80, 240, 46, "sky", 12, 5, hl=False), cv.text(cx, 110, "try: run the risky code", 16, 800, fill=INK, mono=True))
    cv.add(P.arrow(cv, [(cx, 132), (cx, 168)], ARROW, 3, 10))
    cv.add(cv.path("M%s 172 L%s 214 L%s 256 L%s 214 Z" % (cx, cx + 90, cx, cx - 90), fill=cv.g("sun"), stroke=PAL["sun"][2], sw=2.4))
    cv.add(cv.text(cx, 220, "error raised?", 16, 800, fill=INK))
    # yes branch
    cv.add(P.arrow(cv, [(cx - 90, 214), (170, 214), (170, 290)], "#C84B43", 3.4, 11))
    cv.add(cv.text(cx - 130, 204, "yes", 15, 800, cls="il-bad"))
    cv.add(P.lift(cv, 50, 296, 240, 66, "coral", 12, 5, hl=False), cv.text(170, 324, "except: handle it", 16, 800, fill=INK, mono=True), cv.text(170, 348, "the first matching one runs", 12.5, 650, fill=INK))
    # no branch
    cv.add(P.arrow(cv, [(cx + 90, 214), (630, 214), (630, 290)], "#2F9F77", 3.4, 11))
    cv.add(cv.text(cx + 130, 204, "no", 15, 800, cls="il-ok"))
    cv.add(P.lift(cv, 510, 296, 240, 66, "mint", 12, 5, hl=False), cv.text(630, 324, "else: success code", 16, 800, fill=INK, mono=True), cv.text(630, 348, "only if nothing went wrong", 12.5, 650, fill=INK))
    # both to finally
    cv.add(P.arrow(cv, [(170, 368), (170, 410), (cx - 20, 410), (cx - 20, 430)], ARROW, 3, 10))
    cv.add(P.arrow(cv, [(630, 368), (630, 410), (cx + 20, 410), (cx + 20, 430)], ARROW, 3, 10))
    cv.add(P.lift(cv, cx - 150, 436, 300, 56, "sun", 12, 5, hl=False), cv.text(cx, 462, "finally: ALWAYS runs", 17, 800, fill=INK, mono=True), cv.text(cx, 482, "clean up, even after a return or an uncaught error", 12.5, 650, fill=INK))
    cv.add(cv.text(400, 526, "then the program continues, or an uncaught error carries on upwards", 13.5, 700, cls="il-ink2"))
    cv.add(P.badge(cv, 42, 66, 1), P.badge(cv, 56, 290, 2), P.badge(cv, 516, 290, 3), P.badge(cv, 250, 442, 4))
    return figure(
        "exception-flow", cv, "The flow of a try statement: try, then except or else, then finally",
        "A flowchart. The try block runs the risky code. A decision asks whether an error was raised. If yes, the first matching except block runs "
        "to handle it. If no, the else block runs, which holds the code that should only run on success. Both paths then arrive at the finally "
        "block, which always runs, for clean up, even after a return or an error that was not caught. After that the program continues, or an "
        "error that was not caught carries on upwards.",
        ["try holds the code that might fail, kept as short as possible.", "except handles a named error. Put the specific handlers before the general ones.",
         "else runs only when the try block raised nothing, so success code goes there.", "finally always runs, so it is where clean up belongs."],
        "Reading a try statement is following this one flow chart.")


# ------------------------------------------------------------------ the standard library

@illustration("stdlib-toolbox")
def _toolbox():
    cv = Canvas(800, 500).backdrop()
    cv.add(P.card(cv, 14, 24, 772, 452, 20, "batteries included: some of what ships with Python", "sun"))
    tools = [("collections", "Counter, deque,", "defaultdict", "sky"), ("itertools", "lazy loops,", "combinations", "mint"), ("functools", "cache, partial,", "wraps", "lilac"),
             ("heapq / bisect", "smallest first,", "binary search", "coral"), ("re", "patterns in", "text", "sun"),
             ("json / csv", "data in text", "files", "teal"), ("datetime", "dates, times,", "differences", "sky"), ("pathlib", "files and", "folders", "mint"),
             ("sqlite3", "a database", "in one file", "coral"), ("statistics", "mean, median,", "spread", "lilac")]
    for i, (name, l1, l2, color) in enumerate(tools):
        col, row = i % 5, i // 5
        x, y = 34 + col * 148, 84 + row * 190
        cv.add(P.lift(cv, x, y, 136, 150, color, 14, 6, hl=True))
        tc = INK
        cv.add(cv.text(x + 68, y + 52, name, 15 if len(name) < 12 else 12.5, 800, fill=tc, mono=True))
        cv.add(cv.line(x + 22, y + 70, x + 114, y + 70, tc, 1.6, op=.5))
        cv.add(cv.text(x + 68, y + 104, l1, 13, 700, fill=tc), cv.text(x + 68, y + 124, l2, 13, 700, fill=tc))
    cv.add(P.badge(cv, 42, 62, 1))
    return figure(
        "stdlib-toolbox", cv, "Ten parts of the Python standard library and what each is for",
        "Ten tiles, each a module that comes with Python. collections gives Counter, deque and defaultdict. itertools gives lazy loops and "
        "combinations. functools gives cache, partial and wraps. heapq and bisect give smallest first and binary search. re finds patterns in "
        "text. json and csv read and write data files. datetime handles dates, times and differences. pathlib handles files and folders. sqlite3 "
        "is a database in one file. statistics gives the mean, the median and the spread.",
        ["Before writing a utility yourself, check the standard library: the tested, documented version is nearly always better."],
        "Knowing what is in the box is a skill in itself. It saves hours, and the next reader recognises the tools.")


# ------------------------------------------------------------------ version control

@illustration("git-branches")
def _git():
    cv = Canvas(800, 470).backdrop()
    cv.add(P.card(cv, 14, 24, 772, 276, 20, "commits and branches", "teal"))
    ys = {"main": 100, "feature": 210}
    cv.add(cv.line(70, ys["main"], 730, ys["main"], "#0F7C84", 6))
    commits = [(122, "main", "first version"), (256, "main", "add scoring"), (572, "main", "merge"), (668, "main", "release")]
    feat = [(352, "feature", "high scores"), (472, "feature", "tidy up")]
    cv.add(cv.path("M256 100 C296 100 306 210 352 210 L472 210 C532 210 542 100 572 100", stroke="#8061A9", sw=6))
    for x, b, msg in commits:
        cv.add(node(cv, x, ys[b], "", "sun", 16, 14, mono=False))
        cv.add(cv.text(x, ys[b] - 30, msg, 13, 750, cls="il-ink"))
    for x, b, msg in feat:
        cv.add(node(cv, x, ys[b], "", "lilac", 16, 14, mono=False))
        cv.add(cv.text(x, ys[b] + 38, msg, 13, 750, cls="il-ink"))
    cv.add(P.pill(cv, 752, 66, "main", "teal", 14, 10, 24, 800), P.pill(cv, 540, 252, "feature", "plum", 14, 10, 24, 800))
    cv.add(P.badge(cv, 42, 66, 1), P.badge(cv, 334, 162, 2), P.badge(cv, 602, 142, 3))
    cv.add(cv.text(400, 280, "each circle is a commit: a snapshot of every file, with a message and a unique id", 13.5, 700, cls="il-ink2"))
    cv.add(P.card(cv, 14, 322, 772, 138, 20, "the commands", "plum"))
    cmds = [("git switch -c feature", "start a branch"), ("git commit -m \"...\"", "save a snapshot"), ("git merge feature", "bring it back"), ("git push", "send it to the server")]
    for i, (c, d) in enumerate(cmds):
        x = 30 + i * 190
        cv.add(P.lift(cv, x, 366, 180, 34, "paper", 9, 3, hl=False), cv.text(x + 90, 388, c, 12, 800, fill=INK, mono=True), cv.text(x + 90, 424, d, 13, 700, cls="il-ink"))
    return figure(
        "git-branches", cv, "Commits on a main branch, a feature branch, and the merge that brings them together",
        "A line of commits on the main branch: first version, add scoring, then merge and release. After add scoring a second line leaves the main "
        "line, the feature branch, with two commits of its own, high scores and tidy up, so that new work does not disturb the working version. The "
        "feature branch then joins back into main at the commit called merge. Each circle is a commit, a snapshot of every file with a message and a "
        "unique id. Below are the four commands for this: git switch with the minus c option to start a branch, git commit to save a snapshot, git "
        "merge to bring the branch back, and git push to send it to the server.",
        ["Commits are snapshots in a chain. Every commit records the one before it.", "A branch is a separate line of work that leaves the main line.",
         "A merge brings the branch's changes back into the main line."],
        "A branch is just a movable label on a commit, which is why creating one in Git is instant.")


# ------------------------------------------------------------------ logging levels

@illustration("log-levels")
def _logging():
    cv = Canvas(800, 350).backdrop()
    cv.add(P.card(cv, 14, 24, 470, 300, 20, "five levels, and a threshold", "teal"))
    levels = [("CRITICAL", 50, "red", "cannot continue"), ("ERROR", 40, "coral", "something failed"), ("WARNING", 30, "sun", "unexpected, carries on"),
              ("INFO", 20, "sky", "normal events"), ("DEBUG", 10, "slate", "detail for developers")]
    ys = [84, 124, 164, 236, 276]
    for (name, num, color, use), y in zip(levels, ys):
        shown = num >= 30
        if shown:
            tc = P._on(color)
            cv.add(P.lift(cv, 34, y, 430, 34, color, 10, 4, hl=False))
        else:
            tc = INK
            cv.add(cv.rect(34, y, 430, 34, 10, "#FFFFFF", stroke="#9FB3BE", sw=1.8, dash="6 4"))
        cv.add(cv.text(50, y + 23, "%s  %d" % (name, num), 15, 800, anchor="start", fill=tc, mono=True), cv.text(452, y + 22, use if shown else "dropped", 12.5, 700, anchor="end", fill=tc))
    cv.add(cv.line(28, 218, 470, 218, "#C84B43", 3, dash="9 6"))
    cv.add(P.pill(cv, 249, 218, "logger level = WARNING", "paper", 13.5, 14, 26, 800))
    cv.add(P.badge(cv, 42, 64, 1))
    cv.add(P.card(cv, 500, 24, 286, 300, 20, "three parts", "sun"))
    parts = [("logger", "receives messages, checks level", "sky"), ("handler", "where: screen, file, network", "mint"), ("formatter", "how each line looks", "sun")]
    for i, (name, sub, color) in enumerate(parts):
        y = 84 + i * 80
        cv.add(P.lift(cv, 520, y, 246, 52, color, 12, 5, hl=False), cv.text(643, y + 23, name, 16, 800, fill=INK, mono=True), cv.text(643, y + 42, sub, 12.5, 650, fill=INK))
        if i < 2:
            cv.add(P.arrow(cv, [(643, y + 62), (643, y + 78)], ARROW, 2.8, 9))
    cv.add(P.badge(cv, 528, 66, 2))
    return figure(
        "log-levels", cv, "Five logging levels with a threshold, and the logger, handler and formatter that deal with each message",
        "Left, the five levels of the logging module from most to least serious: CRITICAL, 50, the program cannot continue. ERROR, 40, something "
        "failed. WARNING, 30, something unexpected but the program carries on. INFO, 20, normal events. DEBUG, 10, detail for developers. A red "
        "dashed line labelled logger level equals WARNING sits between WARNING and INFO: the three levels above it are shown, and INFO and DEBUG, "
        "drawn with dashed outlines, are dropped. Right, three parts: the logger receives messages and checks the level, the handler decides where "
        "they go, such as the screen, a file or the network, and the formatter decides how each line looks.",
        ["Every message has a level. The logger ignores anything below its threshold, so turning the level up or down needs no change to the code that logs.",
         "A logger receives the message, a handler sends it somewhere, and a formatter sets out how it looks."],
        "Unlike print, logging can be filtered by seriousness and sent to a file or a server, which is what makes it fit for a running program.")
