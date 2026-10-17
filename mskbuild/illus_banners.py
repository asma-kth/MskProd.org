"""Banner pictures for the top of every topic page.

A banner is decoration, not teaching: it says what the topic is about at a glance and gives every page
the same friendly look. It is aria-hidden, it has no text in it, and on a phone it is cropped to its middle
so the main object stays in view. Teaching happens in the figures lower down the page.

Each motif is a small composition of the same parts the figures use. banner_for() picks a motif from the
course and the topic's slug, so a new topic gets a sensible picture without anyone choosing one.
"""
import math

from .illus import Canvas, PAL, INK, _n
from . import illus_props as P
from . import illus_glyphs as G

W, H = 800, 132
FLOOR = 112

MOTIFS = {}


def motif(*names):
    def wrap(fn):
        for n in names:
            MOTIFS[n] = fn
        return fn
    return wrap


def shelf(cv, x0=40, x1=760, y=FLOOR + 6):
    """The surface the objects stand on."""
    return cv.rect(x0, y, x1 - x0, 5, 2.5, "var(--il-line)")


def spark(cv, cx, cy, r=6, color="#FFCC4A", op=.9):
    return cv.poly([(cx, cy - r), (cx + r * .3, cy - r * .3), (cx + r, cy), (cx + r * .3, cy + r * .3), (cx, cy + r), (cx - r * .3, cy + r * .3), (cx - r, cy), (cx - r * .3, cy - r * .3)], color, op=op)


def plate(cv, cx, cy, r=34):
    """A pale disc behind a dark drawing, so that it still shows on the dark theme's panel."""
    return cv.circle(cx, cy, r, "#EEF3F6", op=.92)


def dots(cv, pts, color="#25B3BB", r=3.2, op=.6):
    return "".join(cv.circle(x, y, r, color, op=op) for x, y in pts)


# ------------------------------------------------------------------ the machine

@motif("cpu")
def _cpu(cv):
    cv.add(shelf(cv))
    cv.add(P.ram_stick(cv, 70, 56, 170, 46, 1, 4))
    cv.add(cv.path("M245 80 L310 80", stroke="#25B3BB", sw=3, dash="2 7"), cv.path("M490 62 L560 62", stroke="#25B3BB", sw=3, dash="2 7"))
    cv.add(P.cpu_chip(cv, 330, 20, 92, "CPU"))
    cv.add(P.chip_small(cv, 565, 52, 60, "dark", "ALU"), P.chip_small(cv, 650, 66, 52, "sky", "CU"))
    cv.add(G.stopwatch(cv, 518, 84, 20, -50), P.gear(cv, 740, 40, 20, "sun"))
    cv.add(spark(cv, 280, 28), spark(cv, 470, 24, 5))


@motif("memory")
def _memory(cv):
    cv.add(shelf(cv))
    cv.add(P.ram_stick(cv, 120, 22, 220, 54, 1, 6), P.ram_stick(cv, 120, 70, 220, 38, 1, 6))
    cv.add(G.stopwatch(cv, 420, 70, 28, -70))
    cv.add(P.cpu_chip(cv, 490, 30, 72, "CPU"))
    cv.add(P.chip_small(cv, 610, 50, 64, "dark", "ROM"), P.chip_small(cv, 695, 64, 44, "pcb", ""))
    cv.add(dots(cv, [(360, 44), (372, 56), (384, 44), (396, 56)]))


@motif("storage")
def _storage(cv):
    cv.add(shelf(cv))
    cv.add(P.hdd(cv, 100, 12, 132))
    cv.add(P.ssd(cv, 280, 30, 150, 1.0, False))
    cv.add(P.disc(cv, 520, 64, 40))
    cv.add(cv.rect(600, 62, 74, 46, 8, cv.g("coral", "deep")), cv.rect(574, 76, 30, 18, 3, cv.g("metal", "deep")), cv.circle(660, 78, 4, "var(--il-bg1)"))
    cv.add(P.cloud(cv, 690, 26, 80))


@motif("system")
def _system(cv):
    cv.add(shelf(cv))
    cv.add(P.laptop(cv, 110, 28, .48))
    cv.add(P.gear(cv, 290, 70, 26, "slate"), P.gear(cv, 328, 52, 16, "sun"))
    cv.add(P.folder(cv, 380, 52, .7, "sun"))
    cv.add(P.padlock(cv, 470, 40, .75, "sun"))
    cv.add(mini_term(cv, 550, 36))
    cv.add(P.pill(cv, 700, 70, "OS", "teal", 22, 22, 36, 800))


def mini_term(cv, x, y):
    return cv.rect(x, y, 110, 66, 9, "#1C2831") + cv.rect(x, y, 110, 14, 9, "#3C505B") + cv.rect(x, y + 8, 110, 6, 0, "#3C505B") + cv.text(x + 12, y + 38, ">_", 15, 800, anchor="start", fill="#8CE3EA", mono=True) + cv.rect(x + 12, y + 48, 56, 5, 2, "#B0C3CC", op=.6)


# ------------------------------------------------------------------ data

def bits_row(cv, x, y, s, cw=30, ch=34, gap=5):
    out, cx = "", x
    for c in s:
        col = "sky" if c == "1" else "slate"
        out += P.lift(cv, cx, y, cw, ch, col, 7, 4, hl=False) + cv.text(cx + cw / 2, y + ch / 2 + 6, c, 17, 800, fill=INK, mono=True)
        cx += cw + gap
    return out


@motif("binary")
def _binary(cv):
    cv.add(shelf(cv))
    cv.add(bits_row(cv, 90, 36, "10110100"))
    cv.add(P.arrow(cv, [(380, 54), (420, 54)], "#25B3BB", 4, 11))
    for i, (t, col) in enumerate((("B", "coral"), ("4", "sun"))):
        cv.add(P.lift(cv, 432 + i * 52, 30, 44, 50, col, 10, 5, hl=False), cv.text(454 + i * 52, 64, t, 24, 800, fill=INK, mono=True))
    cv.add(P.bulb(cv, 600, 28, .9, True), P.bulb(cv, 650, 28, .9, False), P.bulb(cv, 700, 28, .9, True))


@motif("datarep")
def _datarep(cv):
    cv.add(shelf(cv))
    cv.add(P.lift(cv, 90, 32, 52, 56, "sky", 10, 5, hl=False), cv.text(116, 70, "A", 30, 800, fill=INK, mono=True))
    cv.add(P.arrow(cv, [(152, 58), (184, 58)], "#25B3BB", 3.5, 10), cv.text(222, 66, "65", 24, 800, cls="il-ink", mono=True))
    # a tiny bitmap
    for r in range(5):
        for c in range(5):
            on = (r, c) in ((0, 2), (1, 1), (1, 2), (1, 3), (2, 0), (2, 1), (2, 2), (2, 3), (2, 4), (3, 1), (3, 3), (4, 0), (4, 4))
            cv.add(cv.rect(300 + c * 17, 22 + r * 17, 16, 16, 2, "#2A3E49" if on else "#FFFFFF", stroke="#C9D5DC", sw=.8))
    # a sound wave
    pts = [(450 + i * 6, 62 - math.sin(i / 3.4) * 26 * math.sin(i / 14.0 + .4)) for i in range(0, 46)]
    cv.add(cv.path("M" + " L".join("%s %s" % (_n(x), _n(y)) for x, y in pts), stroke="#8061A9", sw=3.4))
    for i in range(0, 46, 3):
        cv.add(cv.circle(pts[i][0], pts[i][1], 2.8, "#FFFFFF", stroke="#8061A9", sw=1.6))
    cv.add(P.photo(cv, 730, 34, 40, 30, 4))


@motif("analytics")
def _analytics(cv):
    cv.add(shelf(cv))
    for i, h_ in enumerate((34, 56, 44, 72, 60)):
        cv.add(cv.rect(110 + i * 34, FLOOR - h_, 26, h_, 5, cv.g(("teal", "sky", "coral", "sun", "mint")[i])))
    pts = [(330 + i * 38, 90 - (i * 8 + (i % 2) * 14)) for i in range(6)]
    cv.add(cv.path("M" + " L".join("%s %s" % p for p in pts), stroke="#C84B43", sw=4))
    for x, y in pts:
        cv.add(cv.circle(x, y, 5, "#FFFFFF", stroke="#C84B43", sw=2.6))
    cv.add(cv.circle(600, 66, 38, cv.g("sky")), cv.path("M600 66 L600 28 A38 38 0 0 1 636 78 Z", fill=cv.g("coral")), cv.path("M600 66 L636 78 A38 38 0 0 1 570 94 Z", fill=cv.g("sun")))
    cv.add(P.magnifier(cv, 690, 56, .9, 18))


@motif("database")
def _database(cv):
    cv.add(shelf(cv))
    cv.add(G.cylinder(cv, 140, 64, 80, 80, "sky", 3), G.cylinder(cv, 240, 76, 56, 56, "teal", 2))
    for r in range(4):
        for c in range(4):
            cv.add(cv.rect(330 + c * 40, 22 + r * 22, 38, 20, 3, cv.g("teal") if r == 0 else "#FFFFFF", stroke="#C9D5DC", sw=1))
    cv.add(P.magnifier(cv, 556, 52, 1.0, 20), P.key(cv, 596, 40, .9, "sun"))
    cv.add(cv.text(716, 74, "SQL", 24, 800, cls="il-ink", mono=True))


# ------------------------------------------------------------------ networks and the web

@motif("network")
def _network(cv):
    cv.add(shelf(cv))
    cv.add(P.cloud(cv, 330, 8, 130))
    cv.add(P.router(cv, 330, 58, .62))
    cv.add(P.laptop(cv, 100, 36, .46), P.phone(cv, 220, 38, .46, "", 64, 120), P.laptop(cv, 530, 36, .46))
    cv.add(P.phone(cv, 660, 38, .46, "", 64, 120))
    cv.add(P.wifi(cv, 400, 60, 22, "#25B3BB", 3.4))
    cv.add(cv.path("M280 90 L330 90 M470 90 L530 90", stroke="#25B3BB", sw=3, dash="2 7"))


@motif("protocols")
def _protocols(cv):
    cv.add(shelf(cv))
    for i in range(3):
        cv.add(P.envelope(cv, 100 + i * 100, 46, .8, 70, 48, "paper", ("sky", "coral", "mint")[i], i + 1))
        if i < 2:
            cv.add(P.arrow(cv, [(164 + i * 100, 66), (194 + i * 100, 66)], "#25B3BB", 3, 9))
    for i, c in enumerate(("sun", "coral", "sky", "mint")):
        cv.add(P.lift(cv, 450 + i * 14, 24 + i * 22, 150 - i * 6, 20, c, 6, 3, hl=False))
    cv.add(P.laptop(cv, 676, 36, .42))


@motif("web")
def _web(cv):
    cv.add(shelf(cv))
    cv.add(cv.rect(110, 18, 220, 90, 9, "#FFFFFF", stroke="#9FB3BE", sw=1.4), cv.rect(110, 18, 220, 20, 9, "#DCE8EE"), cv.rect(110, 30, 220, 8, 0, "#DCE8EE"))
    for i, c in enumerate(("#FF7B72", "#FFCB47", "#5BD58B")):
        cv.add(cv.circle(124 + i * 12, 28, 3.4, c))
    cv.add(cv.rect(126, 46, 188, 14, 4, cv.g("teal")), cv.rect(126, 68, 88, 32, 4, "#CFE7F0"), cv.rect(222, 68, 92, 32, 4, "#E6DDF3"))
    cv.add(cv.path("M290 70 L290 96 L297 90 L303 101 L308 99 L302 88 L311 88 Z", fill="#FFFFFF", stroke=INK, sw=1.6))
    cv.add(cv.text(396, 66, "</>", 34, 800, cls="il-ink", mono=True))
    cv.add(cv.circle(520, 62, 40, cv.rad("glb", [(0, "#8EE1E5"), (1, "#14707A")], .38, .3, .85)), cv.ellipse(520, 62, 16, 40, "none", stroke="#FFFFFF", sw=1.4, op=.55), cv.line(480, 62, 560, 62, "#FFFFFF", 1.4, op=.55))
    cv.add(P.envelope(cv, 606, 42, .8, 70, 48, "paper", "sky"), P.padlock(cv, 700, 36, .7, "sun"))


@motif("security")
def _security(cv):
    cv.add(shelf(cv))
    cv.add(P.padlock(cv, 110, 26, 1.0, "sun"))
    sh = "M360 20 L412 34 L412 70 Q412 98 360 112 Q308 98 308 70 L308 34 Z"
    cv.add(cv.path(sh, fill=cv.g("teal"), stroke=PAL["teal"][2], sw=3), cv.path("M338 66 L354 82 L384 48", stroke="#FFFFFF", sw=8))
    cv.add(plate(cv, 490, 68, 38), G.bug(cv, 490, 68, 1.3), P.cross(cv, 520, 36, 11))
    cv.add(P.key(cv, 570, 56, 1.0, "sun"), plate(cv, 710, 62, 36), G.fingerprint(cv, 710, 52, 1.0))


@motif("law")
def _law(cv):
    cv.add(shelf(cv))
    cv.add(scales_art(cv, 150, 62))
    cv.add(P.doc(cv, 270, 18, .9, 62, 80, 5, "paper", "sky"))
    cv.add(gavel_art(cv, 420, 56))
    cv.add(cv.circle(560, 62, 40, cv.rad("glb2", [(0, "#8EE1E5"), (1, "#14707A")], .38, .3, .85)), cv.ellipse(560, 62, 16, 40, "none", stroke="#FFFFFF", sw=1.4, op=.55), cv.line(520, 62, 600, 62, "#FFFFFF", 1.4, op=.55))
    cv.add(P.person(cv, 640, 8, .6, "tan", "black", "plum", "short"), P.person(cv, 700, 14, .5, "light", "brown", "sky", "bun"))


def scales_art(cv, cx, cy):
    out = cv.rect(cx - 18, cy + 40, 36, 7, 3, cv.g("dark", "deep")) + cv.line(cx, cy - 36, cx, cy + 42, "#5B6D79", 5) + cv.line(cx - 52, cy - 28, cx + 52, cy - 22, "#36464F", 4)
    for (bx, by) in ((cx - 52, cy - 28), (cx + 52, cy - 22)):
        out += cv.line(bx, by, bx - 18, by + 34, "#8799A7", 1.6) + cv.line(bx, by, bx + 18, by + 34, "#8799A7", 1.6)
        out += cv.path("M%s %s Q%s %s %s %s Z" % (bx - 20, by + 34, bx, by + 54, bx + 20, by + 34), fill=cv.g("coral"), stroke=PAL["coral"][2], sw=1.2)
    return out + cv.circle(cx, cy - 38, 5, cv.g("sun"))


def gavel_art(cv, cx, cy):
    out = cv.rect(cx - 36, cy + 34, 72, 10, 4, PAL["wood"][2]) + cv.rect(cx - 26, cy + 26, 52, 9, 4, cv.g("wood"))
    head = cv.rect(-24, -13, 48, 26, 6, cv.g("wood", "deep")) + cv.rect(-3, 12, 7, 56, 3, cv.g("wood")) + cv.rect(-24, -13, 7, 26, 3, PAL["wood"][2])
    return out + cv.group(head, cx - 6, cy - 22, 1, -32)


# ------------------------------------------------------------------ code and algorithms

@motif("code")
def _code(cv):
    cv.add(shelf(cv))
    cv.add(G.code(cv, 90, 12, 250, ["def greet(name):", "    return 'Hi ' + name"], title=None, size=12.5, numbers=False))
    cv.add(cv.rect(90, 12, 250, 64, 12, "none", stroke="#8AA0AC", sw=1.4, op=.7), cv.rect(372, 32, 170, 70, 9, "none", stroke="#8AA0AC", sw=1.4, op=.7))
    cv.add(cv.rect(372, 32, 170, 70, 9, "#0F1B22"), cv.text(388, 62, ">>> greet('Maya')", 12.5, 700, anchor="start", fill="#8CE3EA", mono=True), cv.text(388, 86, "Hi Maya", 12.5, 700, anchor="start", fill="#9AF0B5", mono=True))
    cv.add(P.gear(cv, 610, 64, 28, "slate"), P.gear(cv, 648, 44, 16, "sun"))
    cv.add(plate(cv, 716, 66, 34), G.bug(cv, 716, 66, 1.2), spark(cv, 570, 22), spark(cv, 690, 24, 5))


@motif("algorithm")
def _algorithm(cv):
    cv.add(shelf(cv))
    cv.add(cv.rect(90, 28, 74, 30, 15, cv.g("mint")), cv.text(127, 48, "start", 13, 800, fill=INK))
    cv.add(P.arrow(cv, [(164, 43), (196, 43)], "#25B3BB", 3, 9))
    cv.add(cv.path("M244 18 L292 43 L244 68 L196 43 Z", fill=cv.g("sun"), stroke=PAL["sun"][2], sw=2))
    cv.add(cv.text(244, 48, "?", 18, 800, fill=INK))
    cv.add(P.arrow(cv, [(292, 43), (326, 43)], "#25B3BB", 3, 9))
    cv.add(P.lift(cv, 332, 26, 72, 34, "sky", 8, 4, hl=False), P.lift(cv, 332, 78, 72, 30, "coral", 8, 4, hl=False), P.arrow(cv, [(244, 68), (244, 93), (328, 93)], "#25B3BB", 3, 9))
    for i, v in enumerate((36, 70, 24, 56, 88, 44)):
        cv.add(cv.rect(470 + i * 36, FLOOR - v, 28, v, 5, cv.g(("coral", "sky", "mint", "sun", "plum", "teal")[i])))


@motif("logic")
def _logic(cv):
    cv.add(shelf(cv))
    gate_and = "M120 30 L150 30 A26 26 0 0 1 150 82 L120 82 Z"
    cv.add(cv.path(gate_and, fill=cv.g("sky"), stroke=PAL["sky"][2], sw=3), cv.text(143, 62, "AND", 12.5, 800, fill=INK))
    gate_or = "M250 30 Q290 30 322 56 Q290 82 250 82 Q270 56 250 30 Z"
    cv.add(cv.path(gate_or, fill=cv.g("coral"), stroke=PAL["coral"][2], sw=3), cv.text(284, 61, "OR", 12.5, 800, fill=INK))
    cv.add(cv.path("M390 30 L390 82 L432 56 Z", fill=cv.g("mint"), stroke=PAL["mint"][2], sw=3), cv.circle(438, 56, 6, "#FFFFFF", stroke=PAL["mint"][2], sw=3), cv.text(402, 62, "NOT", 10.5, 800, fill=INK))
    for (x, y, on) in ((60, 38, True), (60, 66, False)):
        cv.add(P.toggle(cv, x, y, on, 40, 22), cv.line(x + 40, y + 11, x + 58, y + 11, "#8AA0AC", 2.4))
    for (x, y, on) in ((210, 38, True), (210, 66, True)):
        cv.add(P.toggle(cv, x - 30, y, on, 40, 22))
    cv.add(P.bulb(cv, 520, 22, 1.2, True), cv.text(640, 62, "1 0 1", 26, 800, cls="il-ink", mono=True))


@motif("data-structures")
def _structures(cv):
    cv.add(shelf(cv))
    for i, c in enumerate(("sky", "mint", "sun", "coral")):
        cv.add(P.lift(cv, 90, 88 - i * 24, 90, 20, c, 6, 3, hl=False))
    for i, c in enumerate(("sun", "mint", "sky", "coral")):
        cv.add(P.lift(cv, 220 + i * 44, 70, 38, 32, c, 7, 3, hl=False), cv.text(239 + i * 44, 92, str(i + 1), 17, 800, fill=INK, mono=True))
    cv.add(cv.line(520, 40, 480, 66, "#8AA0AC", 2.4), cv.line(520, 40, 560, 66, "#8AA0AC", 2.4), cv.line(480, 76, 456, 96, "#8AA0AC", 2.4), cv.line(480, 76, 504, 96, "#8AA0AC", 2.4))
    for (x, y, c) in ((520, 36, "coral"), (480, 72, "sky"), (560, 72, "mint"), (456, 98, "sun"), (504, 98, "sun")):
        cv.add(cv.circle(x, y, 14, cv.g(c, "deep"), stroke="#FFFFFF", sw=2))
    for i in range(3):
        cv.add(P.lift(cv, 620 + i * 52, 62, 40, 30, ("sky", "mint", "sun")[i], 7, 3, hl=False))
        if i < 2:
            cv.add(P.arrow(cv, [(662 + i * 52, 77), (670 + i * 52, 77)], "#25B3BB", 2.4, 6))


@motif("oop")
def _oop(cv):
    cv.add(shelf(cv))
    cv.add(cv.rect(120, 14, 150, 90, 9, "#FFFFFF", stroke="#8AA0AC", sw=1.8), cv.rect(121, 15, 148, 24, 8, cv.g("sun")), cv.text(195, 32, "Dog", 14, 800, fill=INK, mono=True))
    cv.add(cv.text(134, 58, "name", 12, 700, anchor="start", fill=INK, mono=True), cv.text(134, 76, "breed", 12, 700, anchor="start", fill=INK, mono=True), cv.text(134, 94, "bark()", 12, 700, anchor="start", fill=INK, mono=True))
    for i, (nm, c) in enumerate((("rex", "sky"), ("mia", "mint"))):
        y = 18 + i * 50
        cv.add(P.arrow(cv, [(272, 50 + i * 24), (346, y + 18)], "#25B3BB", 2.6, 8, dash="4 4"))
        cv.add(P.lift(cv, 352, y, 130, 38, c, 9, 4, hl=False), cv.text(417, y + 25, nm, 15, 800, fill=INK, mono=True))
    cv.add(P.gear(cv, 600, 60, 24, "slate"), spark(cv, 680, 30), spark(cv, 720, 90, 5), P.gear(cv, 650, 40, 14, "sun"))


@motif("complexity")
def _complexity(cv):
    cv.add(shelf(cv))
    ox, oy = 110, 108
    cv.add(cv.line(ox, oy, ox, 12, "#8AA0AC", 2.4), cv.line(ox, oy, ox + 330, oy, "#8AA0AC", 2.4))
    for fn, col in ((lambda t: 12 + t * 40, "#25B3BB"), (lambda t: 10 + t * t * 82, "#F77F72"), (lambda t: 8 + (2 ** (t * 4.2) - 1) / 16.0 * 86, "#8061A9")):
        pts = [(ox + t * 320, oy - min(fn(t), 92)) for t in [i / 24.0 for i in range(25)]]
        cv.add(cv.path("M" + " L".join("%s %s" % (_n(x), _n(y)) for x, y in pts), stroke=col, sw=3.6))
    cv.add(G.stopwatch(cv, 540, 62, 30, -60))
    for i, (t, col) in enumerate((("O(n)", "teal"), ("O(n^2)", "coral"), ("O(2^n)", "plum"))):
        cv.add(P.pill(cv, 700, 34 + i * 30, t, col, 14, 12, 24, 800, "#FFFFFF" if col == "plum" else None))


# ------------------------------------------------------------------ making things

@motif("graphics")
def _graphics(cv):
    cv.add(shelf(cv))
    cv.add(cv.circle(130, 66, 34, cv.g("coral")), cv.rect(170, 34, 68, 68, 10, cv.g("sky")), cv.poly([(290, 100), (326, 30), (362, 100)], cv.g("sun")))
    cv.add(cv.path("M410 96 C430 26 480 26 500 70 S560 100 580 40", stroke="#8061A9", sw=4))
    for (x, y) in ((410, 96), (500, 70), (580, 40)):
        cv.add(cv.rect(x - 7, y - 7, 14, 14, 2, "#FFFFFF", stroke=INK, sw=2.4))
    cv.add(cv.line(500, 70, 470, 30, "#0F7C84", 2), cv.circle(470, 30, 5, "#FFFFFF", stroke="#0F7C84", sw=2.4))
    cv.add(P.photo(cv, 640, 30, 90, 66, 6))
    cv.add(P.lift(cv, 700, 62, 60, 44, "plum", 8, 4, hl=False))


@motif("video")
def _video(cv):
    cv.add(shelf(cv))
    from .illus_imedia2 import clapper
    cv.add(clapper(cv, 90, 24))
    cv.add(cv.rect(230, 20, 230, 74, 5, "#1C2831"))
    for i in range(6):
        cv.add(cv.rect(238 + i * 36, 26, 22, 8, 2, "#FFFFFF", op=.7), cv.rect(238 + i * 36, 80, 22, 8, 2, "#FFFFFF", op=.7))
        cv.add(cv.rect(236 + i * 36, 40, 32, 36, 3, ("#66B8EC", "#F77F72", "#FFCC4A", "#62CFA3", "#8061A9", "#66B8EC")[i]))
    cv.add(cube_art(cv, 560, 60))
    cv.add(plate(cv, 692, 62, 44), P.pixel_cat(cv, 650, 22, 80))


def cube_art(cv, cx, cy):
    top = [(cx, cy - 32), (cx + 38, cy - 14), (cx, cy + 6), (cx - 38, cy - 14)]
    left = [(cx - 38, cy - 14), (cx, cy + 6), (cx, cy + 48), (cx - 38, cy + 28)]
    right = [(cx, cy + 6), (cx + 38, cy - 14), (cx + 38, cy + 28), (cx, cy + 48)]
    return cv.poly(left, "#66B8EC", stroke="#2F82C0", sw=1.4) + cv.poly(right, "#2F82C0", stroke="#1F5F9A", sw=1.4) + cv.poly(top, "#C9EAFB", stroke="#66B8EC", sw=1.4)


@motif("audio")
def _audio(cv):
    cv.add(shelf(cv))
    from .illus_imedia2 import microphone
    cv.add(microphone(cv, 130, 30))
    pts = [(220 + i * 5, 62 - math.sin(i / 2.6) * 30 * math.sin(i / 16.0 + .3)) for i in range(0, 62)]
    cv.add(cv.path("M" + " L".join("%s %s" % (_n(x), _n(y)) for x, y in pts), stroke="#8061A9", sw=3.6))
    cv.add(cv.rect(560, 34, 46, 62, 8, cv.g("dark", "deep")), cv.circle(583, 56, 12, "#5B6D79"), cv.circle(583, 56, 5, "#1C2831"), cv.circle(583, 82, 6, "#5B6D79"))
    cv.add(cv.path("M630 44 Q648 62 630 80 M644 36 Q672 62 644 88", stroke="#25B3BB", sw=3.4))
    cv.add(P.doc(cv, 700, 22, .8, 62, 80, 4, "paper", "mint"))


@motif("ui")
def _ui(cv):
    cv.add(shelf(cv))
    cv.add(P.phone(cv, 130, 8, .8, "", 64, 120))
    cv.add(cv.rect(146, 22, 48, 14, 4, cv.g("teal")), cv.rect(146, 42, 48, 16, 5, cv.g("sun")), cv.rect(146, 64, 48, 16, 5, "#FFFFFF", stroke="#9FB3BE", sw=1.2), cv.rect(146, 86, 48, 14, 7, cv.g("coral")))
    cv.add(cv.rect(260, 24, 150, 78, 9, "#FFFFFF", stroke="#9FB3BE", sw=1.4), cv.rect(260, 24, 150, 18, 9, cv.g("teal")), cv.rect(274, 52, 90, 16, 4, "#F1F5F8", stroke="#B9C6CE", sw=1.2), cv.rect(274, 76, 52, 18, 7, cv.g("sun")))
    cv.add(cv.path("M372 70 L372 96 L379 90 L385 101 L390 99 L384 88 L393 88 Z", fill="#FFFFFF", stroke=INK, sw=1.6))
    cv.add(P.toggle(cv, 470, 36, True, 52, 28), P.toggle(cv, 470, 76, False, 52, 28))
    for i, c in enumerate(("coral", "sky", "mint", "sun")):
        cv.add(cv.circle(600 + i * 40, 58, 16, cv.g(c)))
    cv.add(spark(cv, 740, 40, 8))


@motif("ai")
def _ai(cv):
    cv.add(shelf(cv))
    layers = [[(110, 40), (110, 76)], [(190, 22), (190, 58), (190, 94)], [(270, 40), (270, 76)]]
    for a, b in zip(layers, layers[1:]):
        for (x0, y0) in a:
            for (x1, y1) in b:
                cv.add(cv.line(x0, y0, x1, y1, "#8AA0AC", 1.6, op=.8))
    for layer, col in zip(layers, ("sky", "coral", "mint")):
        for (x, y) in layer:
            cv.add(cv.circle(x, y, 11, cv.g(col, "deep"), stroke="#FFFFFF", sw=2))
    cv.add(plate(cv, 398, 62, 48), P.pixel_cat(cv, 350, 16, 96))
    cv.add(cv.rect(490, 50, 18, 54, 4, cv.g("sky")), cv.rect(516, 34, 18, 70, 4, cv.g("teal")), cv.rect(542, 20, 18, 84, 4, cv.g("mint")))
    cv.add(spark(cv, 640, 40, 9), spark(cv, 676, 70, 6))
    cv.add(P.pill(cv, 720, 60, "AI", "plum", 22, 16, 34, 800))


@motif("testing")
def _testing(cv):
    cv.add(shelf(cv))
    cv.add(P.doc(cv, 110, 14, 1.0, 62, 80, 0, "paper"))
    for i in range(3):
        cv.add(P.tick(cv, 126, 40 + i * 20, 7), cv.rect(140, 37 + i * 20, 22, 5, 2.5, "#C5D1D9"))
    cv.add(P.magnifier(cv, 260, 56, 1.0, 22), plate(cv, 340, 68, 38), G.bug(cv, 340, 68, 1.3))
    cv.add(cv.path("M400 86 L430 86 L430 40 L470 40", stroke="#25B3BB", sw=3, dash="3 7"))
    for i, (t, col) in enumerate((("PASS", "mint"), ("PASS", "mint"), ("FAIL", "coral"))):
        cv.add(P.pill(cv, 600, 28 + i * 30, t, col, 14, 14, 24, 800))
    cv.add(G.flag(cv, 690, 40, 1.3, "coral"))


@motif("media")
def _media(cv):
    cv.add(shelf(cv))
    for i in range(3):
        cv.add(cv.rect(100 + i * 96, 22, 84, 62, 6, "#FFFFFF", stroke="#9FB3BE", sw=1.4), cv.rect(106 + i * 96, 28, 72, 36, 3, ("#C9EAFB", "#FFE9A8", "#C9F3E0")[i]), cv.rect(106 + i * 96, 70, 50, 5, 2, "#C5D1D9"))
    cv.add(cv.circle(142, 46, 9, "#F77F72"), cv.poly([(230, 62), (254, 36), (278, 62)], "#62CFA3"), cv.circle(368, 40, 8, "#FFCC4A"))
    cv.add(P.pill(cv, 520, 36, "client brief", "sun", 14, 14, 28, 800), P.pill(cv, 520, 72, "audience", "sky", 14, 14, 28, 800))
    cv.add(cv.path("M600 100 L690 30 L704 44 L614 114 L596 118 Z", fill=cv.g("sun"), stroke=PAL["sun"][2], sw=2), cv.poly([(596, 118), (600, 100), (614, 114)], "#4A5A64"))
    cv.add(P.doc(cv, 700, 24, .8, 62, 80, 4, "paper", "coral"))


@motif("nature")
def _nature(cv):
    cv.add(shelf(cv))
    from .illus_society import leaf, globe, scales
    cv.add(leaf(cv, 150, 66), globe(cv, 260, 66))
    cv.add(P.cloud(cv, 340, 18, 100), P.server_rack(cv, 500, 14, 1, .6))
    cv.add(spark(cv, 590, 30, 8))
    cv.add(P.bulb(cv, 640, 24, .9, True), G.sun(cv, 730, 44, 14))


@motif("people")
def _people(cv):
    cv.add(shelf(cv))
    for i, (sk, hr, sh, st) in enumerate((("tan", "black", "teal", "short"), ("light", "brown", "coral", "bun"), ("brown", "black", "sky", "curly"), ("pale", "blond", "plum", "long"), ("deep", "black", "sun", "short"))):
        cv.add(P.person(cv, 120 + i * 120, 8 + (i % 2) * 6, .62, sk, hr, sh, st))
    cv.add(spark(cv, 100, 24), spark(cv, 700, 20, 5))


# ------------------------------------------------------------------ A Level and advanced Python

def _state(cv, x, y, color, r=24, double=False):
    """A state of a finite state machine: a circle, ringed twice if it accepts."""
    out = cv.circle(x, y + 3, r, "#10303A", op=.16)
    if double:
        out += cv.circle(x, y, r + 6, "#FFFFFF", stroke=PAL[color][2], sw=2.4)
    return out + cv.circle(x, y, r, cv.g(color), stroke=PAL[color][2], sw=2)


@motif("automata")
def _automata(cv):
    cv.add(shelf(cv))
    cv.add(P.arrow(cv, [(92, 70), (158, 70)], "#25B3BB", 3, 10))
    for x, c, d in ((190, "sky", False), (330, "mint", False), (470, "sun", True)):
        cv.add(_state(cv, x, 70, c, 24, d))
    cv.add(P.arrow(cv, [(216, 70), (300, 70)], "#25B3BB", 3, 10), P.arrow(cv, [(356, 70), (436, 70)], "#25B3BB", 3, 10))
    cv.add(P.curve_arrow(cv, (176, 48), (160, 4), (222, 4), (204, 48), "#25B3BB", 3, 9))
    cv.add(P.pill(cv, 258, 52, "0", "paper", 13, 9, 22, 800), P.pill(cv, 396, 52, "1", "paper", 13, 9, 22, 800))
    for i, v in enumerate("1011"):
        cv.add(P.lift(cv, 580 + i * 42, 62, 36, 34, "sun" if v == "1" else "sky", 8, 3, hl=False), cv.text(598 + i * 42, 86, v, 18, 800, fill=INK, mono=True))
    cv.add(cv.poly([(598, 46), (610, 46), (604, 58)], PAL["plum"][1]))


@motif("compiler")
def _compiler(cv):
    cv.add(shelf(cv))
    for i, (t, c) in enumerate((("2", "sky"), ("+", "sun"), ("3", "sky"))):
        cv.add(P.lift(cv, 90 + i * 50, 70, 42, 34, c, 8, 3, hl=False), cv.text(111 + i * 50, 93, t, 18, 800, fill=INK, mono=True))
    cv.add(P.arrow(cv, [(250, 88), (306, 88)], "#25B3BB", 3, 9))
    cv.add(cv.line(400, 36, 366, 72, "#8AA0AC", 2.4), cv.line(400, 36, 434, 72, "#8AA0AC", 2.4))
    for x, y, t, c in ((400, 30, "+", "sun"), (366, 78, "2", "sky"), (434, 78, "3", "sky")):
        cv.add(cv.circle(x, y, 17, cv.g(c), stroke=PAL[c][2], sw=2), cv.text(x, y + 6, t, 16, 800, fill=INK, mono=True))
    cv.add(P.arrow(cv, [(470, 88), (524, 88)], "#25B3BB", 3, 9))
    for i, t in enumerate(("push 2", "push 3", "add")):
        cv.add(P.lift(cv, 540, 20 + i * 32, 110, 26, ("mint", "mint", "coral")[i], 7, 3, hl=False), cv.text(595, 38 + i * 32, t, 13, 800, fill=INK, mono=True))
    cv.add(spark(cv, 700, 40), spark(cv, 730, 78, 5))


@motif("turing")
def _turing(cv):
    cv.add(shelf(cv))
    for i, v in enumerate(("1", "0", "1", "1", "0", "", "")):
        x = 100 + i * 78
        cv.add(P.lift(cv, x, 74, 70, 38, "paper" if v == "" else ("sun" if v == "1" else "sky"), 8, 3, hl=False))
        if v:
            cv.add(cv.text(x + 35, 100, v, 22, 800, fill=INK, mono=True))
    cx = 100 + 2 * 78 + 35
    cv.add(cv.poly([(cx - 13, 56), (cx + 13, 56), (cx, 72)], PAL["plum"][1]))
    cv.add(P.lift(cv, cx - 36, 14, 72, 38, "lilac", 9, 4, hl=False), cv.text(cx, 40, "q1", 17, 800, fill=INK, mono=True))
    cv.add(P.gear(cv, 690, 56, 24, "sun"), P.gear(cv, 726, 90, 15, "sky", 6))


@motif("scheduler")
def _scheduler(cv):
    cv.add(shelf(cv))
    runs = (("P1", "sky", 70), ("P2", "mint", 44), ("P3", "sun", 90), ("P1", "sky", 50), ("P2", "mint", 70), ("P3", "sun", 56), ("P1", "sky", 40))
    x = 90
    for name, c, w in runs:
        cv.add(P.lift(cv, x, 52, w - 4, 40, c, 6, 3, hl=False), cv.text(x + (w - 4) / 2, 78, name, 14, 800, fill=INK, mono=True))
        x += w
    cv.add(cv.line(90, 106, x, 106, "#8AA0AC", 2.4))
    for tx in range(90, int(x) + 1, 50):
        cv.add(cv.line(tx, 100, tx, 112, "#8AA0AC", 2))
    cv.add(G.stopwatch(cv, 700, 62, 28, -50), spark(cv, 650, 24))


@motif("crypto")
def _crypto(cv):
    cv.add(shelf(cv))
    cv.add(P.lift(cv, 80, 54, 120, 42, "paper", 10, 4, hl=False), cv.text(140, 82, "hello", 20, 800, fill=INK, mono=True))
    cv.add(P.arrow(cv, [(206, 75), (262, 75)], "#25B3BB", 3, 10))
    cv.add(P.padlock(cv, 290, 28, 1.0, "sun"), P.key(cv, 360, 74, .9, "sun"))
    cv.add(P.arrow(cv, [(448, 75), (504, 75)], "#25B3BB", 3, 10))
    cv.add(P.lift(cv, 512, 54, 120, 42, "coral", 10, 4, hl=False), cv.text(572, 82, "q9#Zf", 19, 800, fill=INK, mono=True))
    cv.add(cv.circle(700, 66, 30, cv.g("mint"), stroke=PAL["mint"][2], sw=2.4), cv.text(700, 78, "#", 34, 800, fill=INK, mono=True))
    cv.add(spark(cv, 660, 24), spark(cv, 748, 100, 5))


@motif("pipeline")
def _pipeline(cv):
    cv.add(shelf(cv))
    for i, (name, c) in enumerate((("read", "sky"), ("parse", "mint"), ("filter", "sun"), ("use", "coral"))):
        x = 90 + i * 160
        cv.add(P.lift(cv, x, 62, 108, 44, c, 10, 4, hl=False), cv.text(x + 54, 90, name, 16, 800, fill=INK, mono=True))
        if i < 3:
            cv.add(P.arrow(cv, [(x + 114, 84), (x + 154, 84)], "#25B3BB", 3, 9))
            cv.add(cv.rect(x + 120, 48, 28, 20, 5, "#FFFFFF", stroke="#9FB3BE", sw=1.4), cv.line(x + 134, 68, x + 134, 80, "#9FB3BE", 1.6, dash="3 3"))
    cv.add(spark(cv, 40, 30), spark(cv, 760, 34, 5))


@motif("wrap")
def _wrap(cv):
    cv.add(shelf(cv))
    cv.add(cv.rect(270, 12, 260, 98, 18, "#EEE2F8", stroke="#8061A9", sw=2.4))
    cv.add(cv.rect(332, 40, 136, 52, 12, "#C9EAFB", stroke="#2F82C0", sw=2.4), cv.text(400, 74, "f()", 22, 800, fill=INK, mono=True))
    cv.add(cv.circle(300, 34, 15, cv.g("sun"), stroke=PAL["sun"][2], sw=2), cv.text(300, 41, "@", 19, 800, fill=INK, mono=True))
    cv.add(P.arrow(cv, [(150, 66), (258, 66)], "#25B3BB", 3, 10), P.arrow(cv, [(542, 66), (650, 66)], "#25B3BB", 3, 10))
    cv.add(spark(cv, 100, 36), spark(cv, 700, 34, 5))


@motif("toolbox")
def _toolbox(cv):
    cv.add(shelf(cv))
    cv.add(cv.path("M360 44 Q360 18 384 18 L416 18 Q440 18 440 44", stroke="#4A5A64", sw=7))
    cv.add(cv.rect(310, 44, 180, 68, 10, cv.g("coral", "deep")), cv.rect(310, 44, 180, 24, 10, cv.g("coral")), cv.rect(392, 58, 16, 16, 4, "#FFE9A8", stroke="#DFA000", sw=1.6))
    cv.add(P.gear(cv, 220, 82, 26, "sun"), P.magnifier(cv, 140, 54, .9, 18))
    cv.add(P.folder(cv, 560, 48, .75, "sky"), P.pill(cv, 680, 44, "json", "mint", 14, 12, 26, 800), P.pill(cv, 700, 84, "re", "sun", 14, 14, 26, 800))
    cv.add(spark(cv, 280, 26), spark(cv, 520, 28, 5))


@motif("git")
def _git(cv):
    cv.add(shelf(cv))
    cv.add(cv.line(90, 44, 710, 44, "#25B3BB", 6), cv.path("M250 44 C290 44 300 92 350 92 L470 92 C520 92 530 44 570 44", stroke="#8061A9", sw=6))
    for x, y, c in ((110, 44, "sun"), (250, 44, "sun"), (570, 44, "sun"), (690, 44, "sun"), (350, 92, "lilac"), (470, 92, "lilac")):
        cv.add(cv.circle(x, y, 13, cv.g(c), stroke=PAL[c][2], sw=2.4))
    cv.add(P.pill(cv, 740, 22, "main", "teal", 13, 10, 22, 800))


@motif("dice")
def _dice(cv):
    import random
    cv.add(shelf(cv))
    for x, y, rot, pips in ((150, 62, -10, ((-13, -13), (13, -13), (0, 0), (-13, 13), (13, 13))), (236, 70, 12, ((-13, -13), (0, 0), (13, 13)))):
        body = cv.rect(-26, -26, 52, 52, 10, "#FFFFFF", stroke="#9FB3BE", sw=2) + "".join(cv.circle(px, py, 5, INK) for px, py in pips)
        cv.add(cv.group(body, x, y, rot=rot))
    for i, h in enumerate((8, 16, 28, 42, 54, 42, 28, 16, 8)):
        cv.add(cv.rect(340 + i * 28, FLOOR - h, 22, h, 4, cv.g(("sky", "mint", "sun")[i % 3])))
    rng = random.Random(5)
    cv.add(cv.path("M650 112 L650 18 A94 94 0 0 1 744 112 Z", fill="#C9F3E0", stroke="#2F9F77", sw=2))
    for _ in range(46):
        x, y = rng.random() * 94, rng.random() * 94
        cv.add(cv.circle(650 + x, 112 - y, 3, "#2F9F77" if x * x + y * y <= 94 * 94 else "#C84B43"))


# ------------------------------------------------------------------ choosing a motif

# the first rule whose word appears in the slug wins; the order is deliberate
RULES = [
    # words that sit inside longer ones come first: "loops" holds "oop", "job-roles" holds "roles", "representing-algorithms" holds "representing"
    ("loops", "code"), ("job-roles", "people"), ("representing-algorithms", "algorithm"), ("decomposition", "algorithm"),
    ("heaps", "data-structures"), ("dynamic-programming", "algorithm"), ("finite-state", "automata"), ("grammars", "compiler"), ("turing", "turing"),
    ("little-man", "cpu"), ("scheduling", "scheduler"), ("encryption", "crypto"), ("iterators", "pipeline"), ("decorators", "wrap"),
    ("exceptions", "testing"), ("standard-library", "toolbox"), ("professional", "git"), ("simulation", "dice"),
    ("cpu", "cpu"), ("processor", "cpu"), ("architecture", "cpu"), ("embedded", "cpu"), ("systems-architecture", "cpu"),
    ("primary-storage", "memory"), ("memory", "memory"),
    ("secondary-storage", "storage"), ("units-of-data", "storage"), ("input-output", "storage"), ("data-storage", "storage"),
    ("binary", "binary"), ("number-bases", "binary"), ("hexadecimal", "binary"), ("data-types-and-boolean", "binary"),
    ("character", "datarep"), ("storing-", "datarep"), ("representing", "datarep"), ("data-representation", "datarep"), ("compression", "datarep"),
    ("protocols", "protocols"), ("network", "network"), ("computer-networks", "network"),
    ("cyber", "security"), ("digital-literacy", "security"), ("security", "security"), ("threat", "security"),
    ("legal", "law"), ("legislation", "law"), ("ethical", "law"), ("issues", "law"), ("privacy", "law"),
    ("environment", "nature"), ("society", "nature"), ("green", "nature"),
    ("boolean", "logic"), ("truth", "logic"),
    ("database", "database"), ("sql", "database"), ("relational", "database"),
    ("web", "web"), ("html", "web"),
    ("artificial", "ai"), ("machine-learning", "ai"),
    ("vector", "graphics"), ("graphics", "graphics"), ("visual-identity", "graphics"), ("creating-digital", "graphics"),
    ("3d", "video"), ("animation", "video"), ("video", "video"),
    ("audio", "audio"), ("sound", "audio"),
    ("app", "ui"), ("interface", "ui"), ("tkinter", "ui"), ("interactive", "ui"), ("pygame", "ui"),
    ("testing", "testing"), ("debugging", "testing"), ("tdd", "testing"), ("project", "testing"), ("robust", "testing"), ("validation", "testing"),
    ("software", "system"), ("operating", "system"), ("systems", "system"), ("applications-generation", "system"), ("languages", "system"), ("paradigms", "system"),
    ("oop", "oop"), ("classes", "oop"), ("inheritance", "oop"),
    ("big-o", "complexity"), ("complexity", "complexity"), ("dijkstra", "complexity"),
    ("stacks", "data-structures"), ("linked", "data-structures"), ("trees", "data-structures"), ("data-structures", "data-structures"),
    ("algorithm", "algorithm"), ("computational", "algorithm"), ("searching", "algorithm"), ("sorting", "algorithm"), ("recursion", "algorithm"), ("functional", "algorithm"),
    ("understanding-data", "analytics"), ("managing-data", "analytics"), ("data-across", "analytics"), ("roles", "analytics"), ("big-data", "analytics"), ("scope", "analytics"),
    ("spreadsheet", "analytics"),
    ("media", "media"), ("client", "media"), ("target-audience", "media"), ("research", "media"), ("style", "media"), ("pre-production", "media"), ("work-planning", "media"),
    ("file-formats", "media"), ("distribution", "media"), ("job-roles", "people"),
    ("programming", "code"), ("python", "code"), ("variables", "code"), ("input-and", "code"), ("selection", "code"), ("loops", "code"), ("string", "code"), ("lists", "code"),
    ("functions", "code"), ("subprograms", "code"), ("pseudocode", "code"), ("arrays", "code"), ("dictionaries", "code"), ("first-steps", "code"), ("scratch", "code"),
    ("using-computers", "system"), ("understanding-computers", "cpu"), ("hardware", "cpu"), ("data-types", "code"),
]

DEFAULT_BY_COURSE = {"ks3": "code", "ks4/computer-science": "cpu", "ks4/aqa-computer-science": "cpu", "ks4/edexcel-computer-science": "cpu",
                     "ks4/imedia": "media", "ks5": "code", "python": "code", "data-analytics": "analytics"}


def motif_for(course_slug, topic_slug):
    for word, name in RULES:
        if word in topic_slug:
            return name
    return DEFAULT_BY_COURSE.get(course_slug, "code")


# the picture on each course's own page, chosen so that the three GCSE boards do not look alike
COURSE_MOTIF = {"ks3": "people", "ks4/computer-science": "cpu", "ks4/aqa-computer-science": "network", "ks4/edexcel-computer-science": "logic",
                "ks4/imedia": "media", "ks5": "complexity", "python": "code", "data-analytics": "analytics"}


def course_banner(course_slug):
    """The banner under the heading of a course page."""
    return banner(course_slug, "", COURSE_MOTIF.get(course_slug, "code"))


def banner(course_slug, topic_slug, name=None):
    """The banner for one topic: a decorative inline SVG in its own wrapper."""
    name = name or motif_for(course_slug, topic_slug)
    cv = Canvas(W, H).backdrop("teal" if len(topic_slug) % 2 else "plum")
    MOTIFS[name](cv)
    return ('<div class="topic-banner" aria-hidden="true" data-motif="%s"><svg viewBox="0 0 %d %d" preserveAspectRatio="xMidYMid slice" '
            'focusable="false">%s</svg></div>' % (name, W, H, cv.svg_body()))
