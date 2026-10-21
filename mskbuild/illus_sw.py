"""Illustrations for software, graphics, machine learning and the data stack."""
import math

from .illus import Canvas, PAL, INK, ARROW, figure, illustration, _n
from . import illus_props as P


def pills_row(cv, x, y, labels, color="paper", size=12, pad=9, h=24, gap=6):
    """Pills laid end to end from x. Returns markup."""
    out = ""
    for lab in labels:
        w = len(lab) * size * .58 + pad * 2
        out += P.pill(cv, x, y, lab, color, size, pad, h, 700, anchor="start")
        x += w + gap
    return out


def icon_tile(cv, x, y, w, h, inner=""):
    """A small white app tile."""
    return cv.rect(x, y + 3, w, h, 11, "#10303A", op=.16) + cv.rect(x, y, w, h, 11, "#FFFFFF") + inner


def shield(cv, cx, cy, s=1.0):
    body = cv.path("M0 -14 L12 -9 L12 2 C12 10 6 15 0 18 C-6 15 -12 10 -12 2 L-12 -9 Z", fill=cv.g("green"), stroke=PAL["green"][2], sw=1.5)
    body += cv.path("M-5 2 L-1 6 L6 -4", stroke="#fff", sw=3)
    return cv.group(body, cx, cy, s)


def zipper(cv, cx, cy, s=1.0):
    body = cv.rect(-14, -13, 28, 26, 5, cv.g("sun")) + cv.rect(-2, -13, 4, 26, 0, PAL["sun"][2])
    for k in range(4):
        body += cv.rect(-5 if k % 2 == 0 else 1, -11 + k * 6, 4, 3, 1, "#fff")
    return cv.group(body, cx, cy, s)


def backup_icon(cv, cx, cy, s=1.0):
    body = cv.rect(-14, 2, 28, 12, 4, cv.g("sky")) + cv.circle(8, 8, 1.8, "#fff")
    body += P.arrow(cv, [(0, -14), (0, 0)], PAL["sky"][2], 4, 8)
    return cv.group(body, cx, cy, s)


# ------------------------------------------------------------------ layers

@illustration("abstraction-layers")
def _layers():
    cv = Canvas(800, 500).backdrop()
    # applications on top
    cv.add(P.lift(cv, 24, 40, 524, 92, "coral", 18, 8))
    cv.add(cv.text(58, 76, "Applications", 20, 800, anchor="start", fill=P._on("coral")),
           cv.text(58, 100, "browser · word processor · game", 13, 600, anchor="start", fill=P._on("coral")))
    for i in range(3):
        cv.add(icon_tile(cv, 302 + i * 76, 54, 62, 60))
    cv.add(P.browser_screen(cv, 308, 64, 50, 40, " ", True))
    cv.add(P.doc(cv, 392, 58, .62, lines=4, head="coral"))
    cv.add(P.pixel_cat(cv, 458, 60, 50))
    # operating system and utilities, side by side
    cv.add(P.lift(cv, 24, 176, 348, 92, "teal", 18, 8), P.lift(cv, 388, 176, 160, 92, "plum", 18, 8))
    cv.add(cv.text(58, 210, "Operating system", 20, 800, anchor="start", fill=P._on("teal")))
    cv.add(pills_row(cv, 44, 244, ["memory", "files", "processes", "drivers"]))
    cv.add(P.gear(cv, 340, 218, 22, "slate"))
    cv.add(cv.text(410, 210, "Utilities", 20, 800, anchor="start", fill=P._on("plum")))
    for i, fn in enumerate((shield, zipper, backup_icon)):
        x = 408 + i * 44
        cv.add(icon_tile(cv, x, 222, 40, 38), fn(cv, x + 20, 241, .85))
    # hardware at the bottom
    cv.add(P.lift(cv, 24, 312, 524, 92, "dark", 18, 8))
    cv.add(cv.text(58, 348, "Hardware", 20, 800, anchor="start", fill="#FFFFFF"),
           cv.text(58, 372, "the parts you could drop on your foot", 13, 600, anchor="start", fill="#E6EEF2"))
    cv.add(cv.rect(332, 324, 204, 68, 14, "#EEF3F6"))
    cv.add(P.cpu_chip(cv, 346, 342, 34, "", 1, "dark", 6), P.ram_stick(cv, 398, 346, 220, 67, .33, 3), P.ssd(cv, 482, 346, 230, .21, label=False))
    cv.add(cv.text(347, 384, "CPU", 10.5, 800, fill="#2E4855", anchor="start", mono=True), cv.text(398, 384, "RAM", 10.5, 800, fill="#2E4855", anchor="start", mono=True),
           cv.text(488, 384, "disk", 10.5, 800, fill="#2E4855", anchor="start", mono=True))
    # each layer asks the one below
    for x in (120, 270):
        cv.add(P.arrow(cv, [(x, 142), (x, 172)], PAL["teal"][2], 5, 12), P.arrow(cv, [(x, 278), (x, 308)], PAL["teal"][2], 5, 12))
    cv.add(P.pill(cv, 168, 157, "asks", "paper", 12.5, 10, 22, 800), P.pill(cv, 168, 293, "asks", "paper", 12.5, 10, 22, 800))
    cv.add(P.pill(cv, 286, 446, "each layer only talks to the one below it", "sun", 14, 14, 30, 750))
    # one worked example
    cv.add(P.card(cv, 566, 34, 220, 448, 20, "Saving a file", "coral"))
    tiles = [(64, "coral", "Word processor", "Save as essay.docx"), (158, "teal", "Operating system", "finds space, tracks the file"), (252, "sky", "Device driver", "speaks this disk's language")]
    for y, col, t, sub in tiles:
        cv.add(P.lift(cv, 580, y, 192, 56, col, 14, 6, hl=False))
        cv.add(cv.text(676, y + 24, t, 15, 800, fill=P._on(col)), cv.text(676, y + 43, sub, 12, 600, fill=P._on(col)))
    cv.add(P.arrow(cv, [(676, 128), (676, 152)], PAL["teal"][2], 4, 10), P.arrow(cv, [(676, 222), (676, 246)], PAL["teal"][2], 4, 10))
    cv.add(P.arrow(cv, [(664, 322), (630, 350)], PAL["teal"][2], 4, 10), P.arrow(cv, [(688, 322), (722, 350)], PAL["teal"][2], 4, 10))
    cv.add(P.hdd(cv, 588, 356, 80), P.ssd(cv, 686, 362, 230, .38, label=False))
    cv.add(cv.text(628, 440, "hard disk", 12.5, 700, cls="il-ink2"), cv.text(730, 440, "SSD", 12.5, 700, cls="il-ink2"))
    cv.add(cv.text(676, 466, "the app never knows which", 13, 750, cls="il-ink"))
    cv.add(P.badge(cv, 30, 316, 1), P.badge(cv, 30, 180, 2), P.badge(cv, 394, 180, 3), P.badge(cv, 30, 44, 4), P.badge(cv, 584, 36, 5))
    return figure(
        "abstraction-layers", cv, "Hardware, operating system, utilities, applications",
        "The layers of a computer system, from the metal upwards. At the bottom is the hardware: the processor, the memory, the disks, the "
        "screen. On top of it sits the operating system, which manages all of that on everyone's behalf, handling memory allocation, the file "
        "system, processes and scheduling, device drivers and user accounts. Beside it sits utility software, the housekeeping programs that "
        "keep the system in order: backup, defragmentation, compression and antivirus. On top sit the applications, the browser, the word "
        "processor, the game, which is what the person actually wanted to use. The rule that makes this worth drawing is that each layer "
        "talks only to the layer below it, shown by the arrows pointing down. A worked example on the right follows one save: the word "
        "processor asks the operating system, the operating system asks the device driver, and the driver talks to whichever disk is fitted, "
        "a hard disk or an SSD. The application never addresses the disk directly and never needs to know which kind it is. That is exactly "
        "why the same program can run on two machines with completely different hardware inside them.",
        ["The hardware at the bottom: the parts you could drop on your foot.",
         "The operating system sits on it and manages all of it for you.",
         "Utility software does the housekeeping jobs around the system.",
         "Your applications sit on top and never touch the hardware directly.",
         "That is why a program written once runs on very different machines."],
        "An application that wants a file asks the operating system. It has no idea whether the file is on a hard disk or an SSD, and it does not need to.")


# ------------------------------------------------------------ graphics layers

SHEET_W, SHEET_H = 300, 190


def star(cx, cy, r, n=5, inner=.45):
    pts = []
    for i in range(n * 2):
        a = -math.pi / 2 + math.pi * i / n
        rr = r if i % 2 == 0 else r * inner
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    return pts


def glass(cv, col):
    """A see-through sheet: you can see what is behind a layer wherever it is empty."""
    return (cv.rect(0, 0, SHEET_W, SHEET_H, 10, "#FFFFFF", op=.88)
            + cv.rect(0, 0, SHEET_W, SHEET_H, 10, "none", stroke=col, sw=3.5, dash="10 7"))


def layer_art(cv, which):
    """What is painted on each layer, in a 300 x 190 sheet."""
    if which == "bg":
        out = cv.rect(0, 0, SHEET_W, SHEET_H, 10, cv.lin("gl-bg", [(0, "#F6ECFC"), (1, "#C6AEE6")], 0, 0, 1, 1))
        for (x, y, r) in ((40, 150, 28), (256, 44, 36), (214, 164, 18), (92, 38, 14), (150, 112, 10), (30, 60, 9)):
            out += cv.circle(x, y, r, "#fff", op=.3)
        return out
    if which == "photo":
        return glass(cv, "#2F82C0") + P.photo(cv, 44, 34, 212, 128, 8)
    if which == "logo":
        out = glass(cv, "#C78A00")
        out += cv.circle(236, 54, 34, "#10303A", op=.2) + cv.circle(236, 50, 34, cv.g("coral", "deep"))
        out += cv.poly(star(236, 51, 22), "#FFFFFF")
        return out
    out = glass(cv, "#C84B43")
    out += cv.text(150, 150, "FRESH", 62, 800, fill="#1F3A44")
    out += cv.text(150, 174, "bakery · est. 2025", 14, 700, fill="#1F3A44")
    return out


def sheet(cv, which, ex, fy, col):
    """One layer, tipped back so you can see it is a flat sheet. (ex, fy) is its top left corner."""
    body = cv.rect(0, 14, SHEET_W, SHEET_H, 10, "#10303A", op=.22) + layer_art(cv, which)
    return '<g transform="matrix(1 0 -.6 .5 %s %s)">%s</g>' % (_n(ex), _n(fy), body)


def eye(cv, cx, cy):
    out = cv.path("M%s %s Q%s %s %s %s Q%s %s %s %s Z" % (_n(cx - 11), _n(cy), _n(cx), _n(cy - 11), _n(cx + 11), _n(cy), _n(cx), _n(cy + 11), _n(cx - 11), _n(cy)), fill="#FFFFFF", stroke="#4A6470", sw=1.8)
    return out + cv.circle(cx, cy, 4.6, "#2A3E49") + cv.circle(cx + 1.4, cy - 1.4, 1.4, "#fff")


@illustration("graphics-layers")
def _gfx():
    cv = Canvas(800, 500).backdrop()
    ex = 148
    order = [("bg", 330, "#8061A9"), ("photo", 232, "#2F82C0"), ("logo", 134, "#C78A00"), ("text", 36, "#C84B43")]
    for x in (ex + SHEET_W, ex - SHEET_H * .6):
        cv.add(cv.line(x, 40, x, 424, ARROW, 1.5, op=.28, dash="4 7"))
    for i, (w, fy, col) in enumerate(order):
        cv.add(cv.shadow(ex + 110, fy + 108, 150, 7, .1))
        cv.add(sheet(cv, w, ex, fy, col))
    for i, (w, fy, col) in enumerate(order):
        cv.add(P.badge(cv, 28, fy + 84, i + 1))
    # the layers panel, top layer first, as in any image editor
    cv.add(P.card(cv, 508, 34, 278, 270, 20, "Layers panel", "plum"))
    rows = [("Text", "real text, still editable", "text", "#C84B43"), ("Logo", "vector, scales cleanly", "logo", "#E0A800"),
            ("Photograph", "its own layer", "photo", "#2F82C0"), ("Background", "colour or texture", "bg", "#8061A9")]
    for i, (name, hint, w, col) in enumerate(rows):
        y = 70 + i * 56
        cv.add(cv.rect(520, y, 254, 48, 10, "#FFFFFF"), cv.rect(520, y, 7, 48, 3, col))
        cv.add(eye(cv, 546, y + 24))
        cv.add('<g transform="translate(572 %s) scale(.17)">%s</g>' % (_n(y + 8), layer_art(cv, w).replace('stroke-dasharray="10 7"', 'stroke-dasharray="14 8"')))
        cv.add(cv.text(634, y + 22, name, 15, 800, anchor="start", fill=INK), cv.text(634, y + 39, hint, 11.5, 600, anchor="start", fill="#4A6470"))
    # flatten: everything merges, and cannot be separated again
    cv.add(P.arrow(cv, [(647, 312), (647, 350)], PAL["teal"][2], 6, 15))
    cv.add(P.pill(cv, 720, 331, "Flatten", "sun", 14, 14, 28, 800))
    cv.add('<g transform="translate(520 360) scale(.5)">%s</g>' % "".join(layer_art(cv, w) for w, _, _ in order))
    cv.add(cv.rect(517, 357, 156, 101, 8, "none", stroke="#FFFFFF", sw=3))
    for i, t in enumerate(("one flat image:", "nothing can be", "pulled apart")):
        cv.add(cv.text(690, 392 + i * 19, t, 13, 700, anchor="start", cls="il-ink"))
    cv.add(P.badge(cv, 522, 330, 5))
    return figure(
        "graphics-layers", cv, "Working in layers",
        "Why graphics software works in layers. Each part of the design sits on its own layer, stacked above the others and drawn here pulled "
        "apart so they can be told apart: the background colour or texture at the bottom, then the photograph, then the logo, then the "
        "text on top. Nothing is painted into anything else, so any one layer can be moved, recoloured, hidden or deleted without disturbing "
        "the rest. The logo stays a vector, so it scales to any size cleanly, and the text stays real text, so the wording and the typeface can "
        "still be changed. The layers panel on the right lists them in the same order, top layer first. Flattening merges every layer into a "
        "single image, which is what an exported JPEG or PNG is, and at that point none of it can be separated again. That is why the working "
        "practice is always to keep the layered master file and export a flat copy for use.",
        ["The background sits at the bottom of the stack.",
         "The photograph goes on a layer of its own, above it.",
         "The logo goes above that, so it is never painted into the photo.",
         "The text sits on top, and can be restyled without touching anything else.",
         "Flatten it and they merge into one image, and that is no longer editable."],
        "A flattened file is a finished file. The master stays layered, because the client always wants one change.")


# ----------------------------------------------------------- neural network

@illustration("neural-network")
def _nn():
    cv = Canvas(800, 500).backdrop()
    xs = [196, 358, 520, 664]
    layers = [(4, [130, 210, 290, 370], "sky", 22), (5, [126, 188, 250, 312, 374], "teal", 22),
              (4, [136, 212, 288, 364], "plum", 22), (1, [250], "coral", 30)]
    # the connections first, so the nodes sit on top: thick and teal for a strong weight, coral for a negative one
    for k in range(3):
        a, b = layers[k], layers[k + 1]
        for i, ya in enumerate(a[1]):
            for j, yb in enumerate(b[1]):
                w = ((i * 5 + j * 3 + k * 7) % 7) / 6.0
                neg = (i + 2 * j + k) % 4 == 0
                cv.add(cv.line(xs[k] + a[3], ya, xs[k + 1] - b[3], yb, "#F0675B" if neg else "#25B3BB", .8 + w * 3.4, op=.18 + w * .5))
    for k, (n, ys, col, r) in enumerate(layers):
        for y in ys:
            cv.add(P.lift(cv, xs[k] - r, y - r, r * 2, r * 2, col, r, 5, hl=False))
            cv.add(cv.ellipse(xs[k] - r * .25, y - r * .45, r * .45, r * .2, "#fff", op=.3))
    # what goes in
    feats = [("amount", "£950"), ("hour", "03:12"), ("country", "overseas"), ("history", "new account")]
    for (n, v), y in zip(feats, layers[0][1]):
        cv.add(cv.text(28, y - 2, n, 14.5, 800, anchor="start", cls="il-ink"), cv.text(28, y + 16, v, 13, 650, anchor="start", cls="il-ink2", mono=True))
        cv.add(cv.line(122, y, xs[0] - 24, y, ARROW, 2, op=.45))
    # what comes out
    cv.add(P.arrow(cv, [(xs[3] + 34, 250), (xs[3] + 62, 250)], PAL["coral"][2], 5, 12))
    cv.add(P.tile(cv, 724, 214, 66, 72, "red", "0.93", None, 14, 6, 18, 12, "#FFFFFF"), cv.text(757, 276, "fraud?", 12.5, 800, fill="#FFFFFF"))
    # the layers' names and jobs
    titles = [("Input", "sky"), ("Hidden 1", "teal"), ("Hidden 2", "plum"), ("Output", "coral")]
    notes = [("one node per", "feature"), ("each node mixes", "every input"), ("mixes the mixes", ""), ("one number out", "")]
    for k, ((t, c), (n1, n2)) in enumerate(zip(titles, notes)):
        cv.add(P.pill(cv, xs[k] + (-24 if k == 0 else 0), 64, t, c, 14.5, 14, 30, 800))
        cv.add(cv.text(xs[k] + (-24 if k == 0 else 0), 416, n1, 12.5, 650, cls="il-ink2"))
        if n2:
            cv.add(cv.text(xs[k] + (-24 if k == 0 else 0), 432, n2, 12.5, 650, cls="il-ink2"))
    # training: the loop that sets every weight
    cv.add(P.band(cv, 24, 446, 752, 44, 22))
    cv.add(cv.text(44, 474, "Training:", 15, 800, anchor="start", cls="il-ink"))
    x = 134
    for i, (t, c) in enumerate((("predict", "sky"), ("measure the error", "sun"), ("nudge every weight", "teal"), ("repeat", "mint"))):
        w = len(t) * 14 * .58 + 28
        cv.add(P.pill(cv, x, 468, t, c, 14, 14, 28, 800, anchor="start"))
        x += w
        if i < 3:
            cv.add(P.arrow(cv, [(x + 5, 468), (x + 26, 468)], ARROW, 3, 8, op=.7))
            x += 32
    for k, (t, c) in enumerate(titles):
        cx = xs[k] + (-24 if k == 0 else 0)
        cv.add(P.badge(cv, cx - (len(t) * 14.5 * .58 + 28) / 2 - 20, 64, k + 1))
    cv.add(P.badge(cv, 770, 448, 5))
    return figure(
        "neural-network", cv, "A neural network, layer by layer",
        "A small neural network drawn layer by layer from left to right. The input layer has four nodes, one per feature of the record being "
        "judged: the amount, the hour, the country and the customer's history. A first hidden layer of five nodes follows, and each of those "
        "nodes combines every input using its own set of weights. A second hidden layer of four nodes combines what the first layer produced, "
        "which is why these are called combinations of combinations. At the end a single output node produces one number, here 0.93, the "
        "probability that the transaction is fraudulent. Every line between nodes is a weight: a thicker line is a stronger weight, a teal line "
        "pushes the next node up and a coral one pushes it down. Training is the repeated process of predicting, measuring the error against the "
        "known labels and nudging all of those weights to reduce it, over and over. The network is a sequence of transformations, each one working "
        "on the output of the last, rather than a single step.",
        ["The input layer: one node per feature of the record.",
         "A hidden layer: each node combines every input, with its own weights.",
         "A second hidden layer: it combines what the first layer produced.",
         "The output layer: one number, here the probability of fraud.",
         "Training adjusts every weight, over and over, to reduce the error."],
        "Deep learning is this, with far more layers. The depth in the name is literally the number of hidden layers.")


# ---------------------------------------------------------------- data stack

@illustration("data-stack")
def _stack():
    cv = Canvas(800, 500).backdrop()
    X, W = 24, 752
    slabs = [  # top to bottom
        ("Dashboard", "one chart, one decision", 30, 64, "plum"),
        ("Warehouse", "modelled, ready to query", 114, 76, "mint"),
        ("Transformation", "where most of the work is", 210, 96, "sun"),
        ("Lake", "raw, whatever shape it came in", 326, 76, "teal"),
        ("Sources", "every system that makes data", 422, 64, "sky"),
    ]
    for t, sub, y, h, col in slabs:
        cv.add(P.lift(cv, X, y, W, h, col, 18, 8))
        cv.add(cv.text(58, y + h / 2 - 2, t, 19, 800, anchor="start", fill=P._on(col)), cv.text(58, y + h / 2 + 19, sub, 12.5, 600, anchor="start", fill=P._on(col)))
    # everything flows upwards
    for y in (102, 198, 314, 410):
        for x in (150, 640):
            cv.add(cv.poly([(x - 11, y + 4), (x + 11, y + 4), (x, y - 8)], PAL["teal"][2]))
    PX = 292
    # dashboard
    cv.add(cv.rect(PX, 38, 444, 48, 10, "#FFFFFF"))
    pts = [(PX + 16, 76), (PX + 52, 62), (PX + 88, 68), (PX + 124, 52), (PX + 160, 56), (PX + 196, 44)]
    cv.add(cv.path("M" + " L".join("%s %s" % p for p in pts), stroke="#2F82C0", sw=3.5))
    cv.add(cv.circle(pts[-1][0], pts[-1][1], 4.5, "#2F82C0"))
    cv.add(cv.text(PX + 232, 70, "£12.4k", 21, 800, anchor="start", fill=INK, mono=True))
    cv.add(P.pill(cv, PX + 322, 62, "reorder stock", "sun", 14, 14, 30, 800, anchor="start"))
    # warehouse: a tidy table
    cv.add(cv.rect(PX, 122, 444, 60, 10, "#FFFFFF"))
    for j, (c, x) in enumerate((("customer", 0), ("amount", 160), ("date", 270))):
        cv.add(cv.text(PX + 14 + x, 140, c, 11.5, 800, anchor="start", fill="#4A6470"))
    for r, row in enumerate((("Aisha Khan", "12.50", "2025-03-12"), ("Tom Reilly", "8.00", "2025-03-12"))):
        for (v, x) in zip(row, (0, 160, 270)):
            cv.add(cv.text(PX + 14 + x, 158 + r * 17, v, 12.5, 700, anchor="start", fill=INK, mono=True))
    cv.add(cv.line(PX + 8, 146, PX + 436, 146, "#DCE6EC", 1.5))
    # transformation: messy in, tidy out, four jobs
    cv.add(cv.rect(PX, 218, 444, 80, 10, "#FFFFFF"))
    cv.add(cv.text(PX + 14, 244, "a. khan ", 13, 700, anchor="start", fill="#8A4B3E", mono=True), cv.text(PX + 14, 266, "12.5", 13, 700, anchor="start", fill="#8A4B3E", mono=True))
    cv.add(P.gear(cv, PX + 150, 254, 20, "sun"), P.arrow(cv, [(PX + 92, 254), (PX + 122, 254)], INK, 3, 8), P.arrow(cv, [(PX + 178, 254), (PX + 206, 254)], INK, 3, 8))
    cv.add(cv.text(PX + 214, 244, "Aisha Khan", 13, 800, anchor="start", fill="#1F7A4F", mono=True), cv.text(PX + 214, 266, "12.50", 13, 800, anchor="start", fill="#1F7A4F", mono=True))
    x = PX + 322
    cv.add(cv.text(x, 236, "clean · type", 12.5, 750, anchor="start", fill=INK), cv.text(x, 255, "join · de-duplicate", 12.5, 750, anchor="start", fill=INK))
    cv.add(cv.text(x, 282, "the slow part", 12, 650, anchor="start", fill="#C84B43"))
    # lake: raw files in whatever shape
    cv.add(cv.rect(PX, 334, 444, 60, 10, "#FFFFFF"))
    raw = ['{"cust": "a. khan ", "amt": "12.5"}', '{"cust": "A KHAN", "amt": 12.50, "x": null}', "order,A. Khan,£12.5,,12/03"]
    for i, t in enumerate(raw):
        cv.add(cv.text(PX + 14, 352 + i * 16, t, 11.5, 650, anchor="start", fill="#4A6470", mono=True))
    # sources: five kinds
    srcs = [("orders", "doc"), ("sensors", "wifi"), ("APIs", "api"), ("forms", "form"), ("logs", "log")]
    for i, (t, ic) in enumerate(srcs):
        x = PX + i * 90
        cv.add(cv.rect(x, 432, 84, 44, 10, "#FFFFFF"))
        cx, cy = x + 17, 454
        if ic == "doc":
            cv.add(cv.rect(cx - 8, cy - 11, 16, 22, 3, "#DCE6EC"), cv.rect(cx - 5, cy - 6, 10, 2.5, 1, "#8AA0AC"), cv.rect(cx - 5, cy - 1, 10, 2.5, 1, "#8AA0AC"), cv.rect(cx - 5, cy + 4, 6, 2.5, 1, "#8AA0AC"))
        elif ic == "wifi":
            cv.add(P.wifi(cv, cx, cy + 8, 15, "#2F82C0", 2.6))
        elif ic == "api":
            cv.add(cv.text(cx, cy + 6, "{ }", 17, 800, fill="#1F6FA8", mono=True))
        elif ic == "form":
            for k in range(3):
                cv.add(cv.rect(cx - 9, cy - 11 + k * 8, 5, 5, 1.5, "#41B56D"), cv.rect(cx - 2, cy - 10 + k * 8, 11, 3, 1.5, "#8AA0AC"))
        else:
            for k in range(4):
                cv.add(cv.rect(cx - 10, cy - 11 + k * 6, 20 - (k % 2) * 7, 3, 1.5, "#8AA0AC"))
        cv.add(cv.text(x + 33, 459, t, 12, 750, anchor="start", fill=INK))
    cv.add(P.badge(cv, 30, 426, 1), P.badge(cv, 30, 330, 2), P.badge(cv, 30, 214, 3), P.badge(cv, 30, 118, 4), P.badge(cv, 30, 34, 5))
    return figure(
        "data-stack", cv, "The data stack, layer by layer",
        "The modern data stack drawn as five layers standing on each other, with the data flowing upwards. At the bottom are the sources: "
        "orders, sensors, APIs, forms and logs, every system that generates data. Above that the data lake holds it raw, in whatever structure "
        "it arrived in, with a structure applied only when it is read. Above that the transformation layer cleans, types, joins and "
        "deduplicates it, turning a messy name and a text amount into a clean name and a proper number, and this is where most of the actual "
        "work happens. Above that the warehouse holds the modelled data as tidy tables, stored by column and ready to be queried. Only at the "
        "top does a dashboard sit, carrying one chart and one decision. The stacking is the point: the dashboard that a manager reads is "
        "standing on four layers of work, and a figure nobody trusts is worth less than no figure at all.",
        ["At the bottom, the sources: every system that generates data.",
         "The lake holds it raw, in whatever shape it arrived.",
         "Transformation cleans, types, joins and deduplicates it.",
         "The warehouse holds modelled data, ready to be queried.",
         "And only then can a dashboard be trusted by the people reading it."],
        "The dashboard is the thin layer on top. Almost all the effort is in the layers below it.")
