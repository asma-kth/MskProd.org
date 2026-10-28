"""The parts every illustration is built from: devices, chips, people, badges.

Every function returns SVG markup and draws at a canonical size, placed by its
top left corner unless the docstring says otherwise, and scaled by `s`. They take
the Canvas first because gradients are registered on it, one set per figure.
"""
import math

from .illus import PAL, INK, _n


def _lum(hex_):
    h = hex_.lstrip("#")
    r, g, b = (int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    f = lambda v: v / 12.92 if v <= .03928 else ((v + .055) / 1.055) ** 2.4
    return .2126 * f(r) + .7152 * f(g) + .0722 * f(b)


def _on(color):
    """Ink or white, whichever reads better on a palette colour.

    Text sits in the upper half of a soft gradient, where the colour is lighter
    than at its base, so that is the colour to judge against: judged at the
    base alone, white text on a mid purple passes and then fails on the lit top.
    """
    lo, base, hi = PAL[color]
    mid = tuple(int(int(lo[i:i + 2], 16) * .55 + int(base[i:i + 2], 16) * .45) for i in (1, 3, 5))
    l = _lum("#%02x%02x%02x" % mid)
    white = 1.05 / (l + .05)
    ink = (l + .05) / (_lum(INK) + .05)
    return "#FFFFFF" if white >= ink else INK


# ------------------------------------------------------------------ blocks

def lift(cv, x, y, w, h, color, r=14, depth=6, hl=True):
    """A rounded block that looks raised off the page: a dark lip, a lit face, a sheen."""
    lo, base, hi = PAL[color]
    out = cv.rect(x, y + depth, w, h, r, hi)
    out += cv.rect(x, y, w, h, r, cv.g(color))
    if hl:
        out += cv.rect(x + 5, y + 4, w - 10, max(6, h * .32), max(3, r - 5), "#fff", op=.22)
    return out


def tile(cv, x, y, w, h, color, label=None, sub=None, r=14, depth=6, size=18, subsize=14, tc=None):
    """A lifted block with a label in it."""
    out = lift(cv, x, y, w, h, color, r, depth)
    tc = tc or _on(color)
    if label is not None and sub is not None:
        out += cv.text(x + w / 2, y + h / 2 - 2, label, size, 700, fill=tc)
        out += cv.text(x + w / 2, y + h / 2 + subsize + 1, sub, subsize, 500, fill=tc)
    elif label is not None:
        out += cv.text(x + w / 2, y + h / 2 + size * .36, label, size, 700, fill=tc)
    return out


def pill(cv, x, y, label, color="paper", size=15, pad=12, h=28, weight=650, tc=None, anchor="middle"):
    """A small label on a rounded chip. (x, y) is its centre."""
    w = len(label) * size * .58 + pad * 2
    lo, base, hi = PAL[color]
    x0 = x - w / 2 if anchor == "middle" else x
    out = cv.rect(x0, y - h / 2 + 2, w, h, h / 2, hi, op=.5 if color == "paper" else 1)
    out += cv.rect(x0, y - h / 2, w, h, h / 2, cv.g(color))
    out += cv.text(x0 + w / 2, y + size * .35, label, size, weight, fill=tc or _on(color))
    return out


def badge(cv, x, y, n, color="deep", r=15):
    """A numbered marker that ties the picture to the list underneath it."""
    out = cv.circle(x, y + 2, r + 3, "#10303A", op=.18)
    out += cv.circle(x, y, r + 3, "#FFFFFF")
    out += cv.circle(x, y, r, cv.g(color, "deep"))
    out += cv.text(x, y + 6, str(n), 17, 800, fill="#FFFFFF")
    return out


def arrow(cv, pts, color="#25B3BB", w=6, head=15, dash=None, op=None):
    """A polyline with a round-ended shaft and a filled head on the last point."""
    d = "M" + " L".join("%s %s" % (_n(x), _n(y)) for x, y in pts)
    (x0, y0), (x1, y1) = pts[-2], pts[-1]
    ang = math.atan2(y1 - y0, x1 - x0)
    # pull the shaft back so it does not poke through the head
    bx, by = x1 - math.cos(ang) * head * .7, y1 - math.sin(ang) * head * .7
    d = "M" + " L".join("%s %s" % (_n(x), _n(y)) for x, y in pts[:-1]) + " L%s %s" % (_n(bx), _n(by))
    out = cv.path(d, stroke=color, sw=w, dash=dash, op=op)
    hw = head * .62
    px, py = -math.sin(ang), math.cos(ang)
    tip = (x1, y1)
    l = (x1 - math.cos(ang) * head + px * hw, y1 - math.sin(ang) * head + py * hw)
    r = (x1 - math.cos(ang) * head - px * hw, y1 - math.sin(ang) * head - py * hw)
    out += cv.path("M%s %s L%s %s L%s %s Z" % (_n(tip[0]), _n(tip[1]), _n(l[0]), _n(l[1]), _n(r[0]), _n(r[1])),
                   fill=color, stroke=color, sw=2, op=op)
    return out


def curve_arrow(cv, p0, c1, c2, p1, color="#25B3BB", w=6, head=15, op=None, dash=None):
    """A cubic curve with an arrowhead that follows the curve's last direction."""
    ang = math.atan2(p1[1] - c2[1], p1[0] - c2[0])
    bx, by = p1[0] - math.cos(ang) * head * .7, p1[1] - math.sin(ang) * head * .7
    d = "M%s %s C%s %s %s %s %s %s" % (_n(p0[0]), _n(p0[1]), _n(c1[0]), _n(c1[1]), _n(c2[0]), _n(c2[1]), _n(bx), _n(by))
    out = cv.path(d, stroke=color, sw=w, op=op, dash=dash)
    hw = head * .62
    px, py = -math.sin(ang), math.cos(ang)
    l = (p1[0] - math.cos(ang) * head + px * hw, p1[1] - math.sin(ang) * head + py * hw)
    r = (p1[0] - math.cos(ang) * head - px * hw, p1[1] - math.sin(ang) * head - py * hw)
    out += cv.path("M%s %s L%s %s L%s %s Z" % (_n(p1[0]), _n(p1[1]), _n(l[0]), _n(l[1]), _n(r[0]), _n(r[1])),
                   fill=color, stroke=color, sw=2, op=op)
    return out


def cable(cv, d, color="slate", w=8):
    """A cable: a dark sleeve with a lighter core line along it."""
    lo, base, hi = PAL[color]
    return cv.path(d, stroke=hi, sw=w + 3) + cv.path(d, stroke=base, sw=w) + cv.path(d, stroke=lo, sw=max(2, w * .28), op=.8)


# ----------------------------------------------------------------- devices

def laptop(cv, x, y, s=1.0, screen=""):
    """A laptop seen from the front. Canonical size 220 x 150."""
    body = cv.shadow(110, 146, 112, 8)
    body += cv.rect(22, 0, 176, 120, 12, cv.g("dark", "deep"))
    body += cv.rect(22, 0, 176, 120, 12, "none", stroke="#0E171C", sw=1.2, op=.5)
    body += cv.rect(31, 9, 158, 102, 5, "#EAF6F8")
    body += screen
    body += cv.circle(110, 4.6, 1.8, "#0E171C")
    body += cv.rect(18, 118, 184, 8, 3, "#27343D")
    body += cv.path("M0 126 L220 126 Q220 139 205 139 L15 139 Q0 139 0 126 Z", fill=cv.g("metal"))
    body += cv.rect(88, 126, 44, 6, 3, PAL["metal"][2], op=.55)
    body += cv.path("M3 128 L217 128", stroke="#fff", sw=1.4, op=.6)
    return cv.group(body, x, y, s)


def monitor(cv, x, y, s=1.0, screen="", w=200, h=130):
    """A desktop monitor on its stand. Canonical size 200 x 170."""
    body = cv.shadow(w / 2, 168, 70, 6)
    body += cv.rect(w / 2 - 14, h - 6, 28, 30, 4, cv.g("metal", "side"))
    body += cv.rect(w / 2 - 54, h + 18, 108, 12, 6, cv.g("metal", "deep"))
    body += cv.rect(0, 0, w, h, 11, cv.g("dark", "deep"))
    body += cv.rect(8, 8, w - 16, h - 16, 5, "#EAF6F8")
    body += screen
    body += cv.circle(w / 2, h - 4, 1.8, "#9FB2BD")
    return cv.group(body, x, y, s)


def phone(cv, x, y, s=1.0, screen="", w=64, h=120):
    body = cv.shadow(w / 2, h + 4, w * .6, 5)
    body += cv.rect(0, 0, w, h, 11, cv.g("dark", "deep"))
    body += cv.rect(5, 8, w - 10, h - 16, 5, "#EAF6F8")
    body += screen
    body += cv.rect(w / 2 - 9, 3, 18, 3, 1.5, "#0E171C")
    return cv.group(body, x, y, s)


def server_rack(cv, x, y, units=4, s=1.0, color="dark", leds=("#5BE08A", "#FFC84A")):
    """A rack of servers. Canonical width 130, height 28 + 46 per unit."""
    h = 28 + 46 * units
    body = cv.shadow(65, h + 6, 74, 7)
    body += cv.rect(0, 0, 130, h, 10, cv.g(color, "deep"))
    body += cv.rect(6, 6, 118, h - 12, 6, "#0F1A20", op=.55)
    for i in range(units):
        yy = 14 + i * 46
        body += cv.rect(12, yy, 106, 38, 6, cv.g("dark"))
        body += cv.rect(12, yy, 106, 38, 6, "none", stroke="#0E171C", sw=1, op=.5)
        for k in range(5):
            body += cv.rect(20 + k * 13, yy + 9, 8, 20, 2, "#0F1A20", op=.7)
        body += cv.circle(98, yy + 13, 3.4, leds[i % len(leds)])
        body += cv.circle(108, yy + 13, 3.4, "#5C6F7B")
        body += cv.rect(94, yy + 25, 18, 3, 1.5, "#6F8794")
    body += cv.rect(12, 4, 106, 2, 1, "#fff", op=.18)
    return cv.group(body, x, y, s)


def tower(cv, x, y, s=1.0, color="metal"):
    """A desktop tower. Canonical 70 x 140."""
    body = cv.shadow(35, 142, 44, 6)
    body += cv.rect(0, 0, 70, 140, 9, cv.g(color))
    body += cv.rect(0, 0, 70, 140, 9, "none", stroke=PAL[color][2], sw=1.2, op=.5)
    body += cv.rect(10, 12, 50, 8, 3, "#33444E")
    body += cv.rect(10, 28, 50, 8, 3, "#33444E")
    body += cv.circle(35, 112, 9, cv.g("slate", "deep"))
    body += cv.circle(35, 112, 4, "#5BE08A")
    return cv.group(body, x, y, s)


def router(cv, x, y, s=1.0, color="coral"):
    """A wifi router. Canonical 150 x 90."""
    body = cv.shadow(75, 86, 70, 6)
    body += cv.rect(24, 6, 6, 40, 3, "#2A3E49") + cv.circle(27, 6, 5, "#2A3E49")
    body += cv.rect(120, 6, 6, 40, 3, "#2A3E49") + cv.circle(123, 6, 5, "#2A3E49")
    body += lift(cv, 0, 38, 150, 42, color, 12, 6)
    for i, c in enumerate(("#5BE08A", "#5BE08A", "#FFD24A", "#FFFFFF")):
        body += cv.circle(24 + i * 16, 60, 4, c)
    body += cv.rect(96, 54, 40, 12, 6, "#0F1A20", op=.35)
    return cv.group(body, x, y, s)


def net_switch(cv, x, y, s=1.0, ports=8, color="sky", w=180):
    """A network switch: a flat box with a row of ports. Canonical 180 x 54."""
    body = cv.shadow(w / 2, 62, w * .45, 6)
    body += lift(cv, 0, 0, w, 44, color, 10, 6)
    pw = (w - 36) / ports
    for i in range(ports):
        px = 18 + i * pw
        body += cv.rect(px, 14, pw - 5, 16, 3, "#16313F")
        body += cv.rect(px + 2, 25, pw - 9, 3, 1.5, "#5BE08A" if i % 3 != 1 else "#FFC84A")
    return cv.group(body, x, y, s)


def cloud(cv, x, y, w=180, color="paper", s=1.0, tint="#CFEAF6"):
    """A puffy cloud. (x, y) is the top left of a w x 0.6w box."""
    h = w * .6
    d = ("M%s %s C%s %s %s %s %s %s C%s %s %s %s %s %s C%s %s %s %s %s %s C%s %s %s %s %s %s Z"
         % (_n(w * .18), _n(h * .98),
            _n(-w * .02), _n(h * .98), _n(-w * .02), _n(h * .62), _n(w * .14), _n(h * .56),
            _n(w * .1), _n(h * .2), _n(w * .38), _n(h * .12), _n(w * .46), _n(h * .3),
            _n(w * .56), _n(-h * .06), _n(w * .86), _n(h * .06), _n(w * .84), _n(h * .46),
            _n(w * 1.04), _n(h * .5), _n(w * 1.02), _n(h * .98), _n(w * .82), _n(h * .98)))
    body = cv.path(d, fill=cv.lin("cloud", [(0, "#FFFFFF"), (1, tint)]))
    body += cv.path("M%s %s L%s %s" % (_n(w * .2), _n(h * .98), _n(w * .82), _n(h * .98)), stroke="#fff", sw=2, op=0)
    return cv.group(body, x, y, s)


def cpu_chip(cv, x, y, size=120, label="CPU", s=1.0, color="dark", pins=10):
    """A processor seen from above, with its pins. (x, y) is the top left."""
    body = cv.shadow(size / 2, size + 8, size * .56, 6)
    pad = size * .1
    pw = (size - pad * 2) / pins
    for i in range(pins):
        px = pad + i * pw + pw * .2
        for (ax, ay, aw, ah) in ((px, -7, pw * .6, 10), (px, size - 3, pw * .6, 10),
                                 (-7, px, 10, pw * .6), (size - 3, px, 10, pw * .6)):
            body += cv.rect(ax, ay, aw, ah, 1.5, cv.g("gold"))
    body += cv.rect(0, 0, size, size, size * .09, cv.g(color, "deep"))
    inset = size * .14
    body += cv.rect(inset, inset, size - inset * 2, size - inset * 2, size * .05, cv.g("metal"))
    body += cv.rect(inset + 3, inset + 3, size - inset * 2 - 6, (size - inset * 2) * .4, size * .04, "#fff", op=.35)
    body += cv.poly([(size * .08, size * .08), (size * .08 + 11, size * .08), (size * .08, size * .08 + 11)], "#FFCC4A")
    body += cv.text(size / 2, size / 2 + size * .07, label, size * .24, 800, fill="#44606E")
    return cv.group(body, x, y, s)


def ram_stick(cv, x, y, w=230, h=62, s=1.0, chips=6, label=None):
    """A memory module: green board, black chips, gold contacts along the bottom."""
    body = cv.shadow(w / 2, h + 12, w * .45, 5)
    body += cv.rect(0, 0, w, h, 5, cv.g("pcb"))
    body += cv.rect(0, 0, w, h, 5, "none", stroke=PAL["pcb"][2], sw=1.2, op=.6)
    cw = (w - 40) / chips
    for i in range(chips):
        body += cv.rect(20 + i * cw, 10, cw - 8, h - 30, 3, "#1A242B")
        body += cv.rect(22 + i * cw, 12, cw - 12, 5, 2, "#fff", op=.18)
    for i in range(int((w - 14) / 7)):
        body += cv.rect(7 + i * 7, h - 9, 4.2, 9, 1, cv.g("gold"))
    body += cv.rect(w * .55, h - 10, 6, 10, 0, PAL["pcb"][1])
    body += cv.circle(7, h / 2 - 4, 3, "#E9F7EF", op=.8)
    if label:
        body += cv.text(w - 36, 22, label, 11, 700, fill="#DFF6EA", mono=True)
    return cv.group(body, x, y, s)


def hdd(cv, x, y, w=230, s=1.0):
    """A hard disk drive with its lid off: platter, spindle and the read-write arm."""
    h = w * .76
    body = cv.shadow(w / 2, h + 10, w * .5, 7)
    body += cv.rect(0, 0, w, h, 14, cv.g("metal"))
    body += cv.rect(0, 0, w, h, 14, "none", stroke=PAL["metal"][2], sw=2, op=.6)
    for (px, py) in ((12, 12), (w - 12, 12), (12, h - 12), (w - 12, h - 12)):
        body += cv.circle(px, py, 4, PAL["metal"][2], op=.7)
    cx, cy, r = w * .42, h * .5, h * .4
    body += cv.circle(cx, cy, r + 5, "#10303A", op=.2)
    body += cv.circle(cx, cy, r, cv.rad("platter", [(0, "#F4F8FA"), (.55, "#C8D4DB"), (.8, "#E7EEF2"), (1, "#9FB1BD")], .4, .35, .75))
    for k in (.8, .6, .45):
        body += cv.circle(cx, cy, r * k, "none", stroke="#fff", sw=1.4, op=.55)
    body += cv.path("M%s %s A%s %s 0 0 1 %s %s" % (_n(cx - r * .7), _n(cy - r * .5), _n(r), _n(r), _n(cx + r * .2), _n(cy - r * .95)),
                    stroke="#fff", sw=5, op=.55)
    body += cv.circle(cx, cy, r * .2, cv.g("metal", "deep"))
    body += cv.circle(cx, cy, r * .07, "#6E8390")
    ax, ay = w * .87, h * .84
    body += cv.circle(ax, ay, 9, cv.g("dark"))
    body += cv.path("M%s %s L%s %s L%s %s" % (_n(ax), _n(ay), _n(cx + r * .3), _n(cy + r * .5), _n(cx + r * .08), _n(cy + r * .3)),
                    stroke=PAL["dark"][1], sw=8, cap="round")
    body += cv.circle(cx + r * .06, cy + r * .28, 5, "#1A242B")
    return cv.group(body, x, y, s)


def ssd(cv, x, y, w=230, s=1.0, label=True):
    """A solid state drive: a circuit board of memory chips, with no moving parts."""
    h = w * .52
    body = cv.shadow(w / 2, h + 10, w * .46, 6)
    body += cv.rect(0, 0, w, h, 8, cv.g("pcb"))
    body += cv.rect(0, 0, w, h, 8, "none", stroke=PAL["pcb"][2], sw=1.4, op=.6)
    for i in range(6):
        body += cv.rect(4 + i * 7, h - 11, 4.5, 11, 1, cv.g("gold"))
    cw = (w - 70) / 3
    for i in range(3):
        for j in range(2):
            cx0, cy0 = 54 + i * cw, 12 + j * (h - 26) / 2
            body += cv.rect(cx0, cy0, cw - 10, (h - 40) / 2, 4, "#1A242B")
            body += cv.rect(cx0 + 3, cy0 + 3, cw - 16, 5, 2, "#fff", op=.16)
    body += cv.rect(w - 36, h * .38, 24, 24, 3, "#232E35")
    if label:
        body += cv.text(w - 24, h * .38 + 16, "CTRL", 8, 800, fill="#C9D8E0", mono=True)
    for k in range(4):
        body += cv.path("M%s %s l12 0 l5 5 l30 0" % (_n(30), _n(14 + k * 9)), stroke="#fff", sw=1, op=.35)
    return cv.group(body, x, y, s)


def disc(cv, cx, cy, r=70, s=1.0):
    """An optical disc, its rainbow sheen and the hole in the middle. Centred."""
    body = cv.shadow(0, r + 8, r * .9, 6)
    body += cv.circle(0, 0, r + 2, "#10303A", op=.16)
    body += cv.circle(0, 0, r, cv.rad("disc", [(0, "#FFFFFF"), (.5, "#E4ECF1"), (1, "#B8C7D1")], .4, .3, .8))
    sheen = cv.lin("sheen", [(0, "#FF9CC8", .0), (.25, "#9CD8FF", .55), (.5, "#B5FFC8", .55), (.75, "#FFE49C", .55), (1, "#FF9CC8", 0)], 0, 0, 1, 1)
    body += cv.circle(0, 0, r * .96, sheen)
    body += cv.circle(0, 0, r * .72, "none", stroke="#fff", sw=1.2, op=.7)
    body += cv.circle(0, 0, r * .45, cv.g("metal"))
    body += cv.circle(0, 0, r * .17, "#F3F7F9")
    body += cv.circle(0, 0, r * .17, "none", stroke=PAL["metal"][2], sw=1.5)
    body += cv.path("M%s %s A%s %s 0 0 1 %s %s" % (_n(-r * .8), _n(-r * .3), _n(r * .86), _n(r * .86), _n(-r * .2), _n(-r * .82)),
                    stroke="#fff", sw=4, op=.7)
    return cv.group(body, cx, cy, s)


def chip_small(cv, x, y, w=60, color="dark", label="", s=1.0):
    """A little IC with legs on its sides. Canonical w x w*0.7."""
    h = w * .7
    body = ""
    n = 4
    for i in range(n):
        yy = 6 + i * (h - 12) / (n - 1) - 2
        body += cv.rect(-5, yy, 8, 4, 1, cv.g("gold")) + cv.rect(w - 3, yy, 8, 4, 1, cv.g("gold"))
    body += cv.rect(0, 0, w, h, 5, cv.g(color, "deep"))
    body += cv.rect(3, 3, w - 6, h * .3, 3, "#fff", op=.18)
    if label:
        body += cv.text(w / 2, h / 2 + 5, label, 13, 800, fill="#FFFFFF", mono=True)
    return cv.group(body, x, y, s)


# ------------------------------------------------------------------ people

SKINS = {"light": "#F6CDA8", "tan": "#E0A879", "brown": "#B97B52", "deep": "#8A5638", "pale": "#FADFC8"}
HAIRS = {"black": "#2B2B36", "brown": "#6B4026", "blond": "#E7B866", "ginger": "#C8602E", "grey": "#B9BEC6", "navy": "#2E3F6E"}


def person(cv, x, y, s=1.0, skin="light", hair="black", shirt="coral", style="short", glasses=False,
           mood="smile", hood=False):
    """A friendly head-and-shoulders character. Canonical 120 wide by 150 tall."""
    sk = SKINS.get(skin, skin)
    hr = HAIRS.get(hair, hair)
    lo, base, hi = PAL[shirt]
    body = cv.shadow(60, 150, 56, 5, .2)
    # shoulders
    body += cv.path("M8 150 C8 114 32 98 60 98 C88 98 112 114 112 150 Z", fill=cv.g(shirt))
    body += cv.path("M8 150 C8 114 32 98 60 98 C88 98 112 114 112 150", stroke=hi, sw=2, op=.35)
    if hood:
        body += cv.path("M22 118 C30 96 90 96 98 118 C90 108 30 108 22 118 Z", fill=hi, op=.6)
    else:
        body += cv.path("M44 100 Q60 118 76 100", stroke=hi, sw=5, op=.5)
    # neck
    body += cv.rect(50, 80, 20, 26, 7, "#000", op=.12)
    body += cv.rect(50, 78, 20, 26, 7, sk)
    # hair behind the head
    if style == "long":
        body += cv.path("M24 60 C16 120 30 132 40 128 L80 128 C90 132 104 120 96 60 Z", fill=hr)
    if hood:
        body += cv.ellipse(60, 54, 40, 42, hi)
    # ears and head
    body += cv.circle(27, 58, 7, sk) + cv.circle(93, 58, 7, sk)
    body += cv.ellipse(60, 56, 32, 36, sk)
    body += cv.ellipse(60, 56, 32, 36, cv.lin("skinshade", [(0, "#fff", .2), (.5, "#fff", 0), (1, "#7A3B1E", .14)]))
    # hair on top
    if style == "short":
        body += cv.path("M27 52 C22 20 98 16 93 52 C86 38 72 32 60 32 C46 32 34 38 27 52 Z", fill=hr)
    elif style == "long":
        body += cv.path("M27 56 C22 18 98 14 93 56 C90 42 74 34 60 34 C44 34 30 42 27 56 Z", fill=hr)
    elif style == "bun":
        body += cv.circle(60, 16, 13, hr)
        body += cv.path("M27 52 C22 22 98 18 93 52 C86 38 72 32 60 32 C46 32 34 38 27 52 Z", fill=hr)
    elif style == "curly":
        for cx, cy in ((34, 34), (48, 26), (62, 24), (76, 26), (88, 36), (28, 50), (94, 50)):
            body += cv.circle(cx, cy, 13, hr)
    elif style == "cap":
        body += cv.path("M26 50 C24 18 96 16 94 50 Z", fill=cv.g("sky", "deep"))
        body += cv.rect(54, 44, 52, 7, 3.5, PAL["sky"][2])
    elif style == "bald":
        pass
    if hood:
        body += cv.path("M28 52 C30 26 90 26 92 52 C84 44 36 44 28 52 Z", fill=PAL[shirt][2], op=.9)
    # face
    ey = 60
    body += cv.ellipse(48, ey, 3.4, 4.4, "#26262F") + cv.ellipse(72, ey, 3.4, 4.4, "#26262F")
    body += cv.circle(49.2, ey - 1.6, 1.2, "#fff") + cv.circle(73.2, ey - 1.6, 1.2, "#fff")
    body += cv.path("M42 51 Q48 47 54 50", stroke=hr, sw=2.4, op=.9) + cv.path("M66 50 Q72 47 78 51", stroke=hr, sw=2.4, op=.9)
    body += cv.circle(40, 70, 5, "#F27A72", op=.28) + cv.circle(80, 70, 5, "#F27A72", op=.28)
    if mood == "smile":
        body += cv.path("M50 74 Q60 84 70 74", stroke="#8A3E3E", sw=3)
    elif mood == "open":
        body += cv.path("M50 73 Q60 90 70 73 Z", fill="#7A2E34") + cv.path("M54 80 Q60 86 66 80", fill="#F27A72", stroke="#F27A72", sw=1)
    elif mood == "worry":
        body += cv.path("M51 80 Q60 72 69 80", stroke="#8A3E3E", sw=3)
    else:
        body += cv.path("M52 77 L68 77", stroke="#8A3E3E", sw=3)
    if glasses:
        body += cv.circle(48, ey, 11, "none", stroke="#26262F", sw=2.6) + cv.circle(72, ey, 11, "none", stroke="#26262F", sw=2.6)
        body += cv.path("M59 58 Q60 56 61 58", stroke="#26262F", sw=2.4)
    return cv.group(body, x, y, s)


# ----------------------------------------------------------- small glyphs

def gear(cv, cx, cy, r=28, color="slate", teeth=8):
    """A cog, centred."""
    lo, base, hi = PAL[color]
    pts = []
    for i in range(teeth * 2):
        a = math.pi * i / teeth
        rr = r if i % 2 == 0 else r * .78
        a0, a1 = a - math.pi / teeth * .5, a + math.pi / teeth * .5
        pts += [(cx + math.cos(a0) * rr, cy + math.sin(a0) * rr), (cx + math.cos(a1) * rr, cy + math.sin(a1) * rr)]
    out = cv.poly(pts, cv.g(color), stroke=hi, sw=1.4)
    out += cv.circle(cx, cy, r * .36, "var(--il-hole)")
    return out


def padlock(cv, x, y, s=1.0, color="sun", open_=False):
    """A padlock. Canonical 56 x 70."""
    body = cv.shadow(28, 72, 28, 4, .2)
    sh = "M14 32 L14 20 C14 6 42 6 42 20 L42 32" if not open_ else "M14 32 L14 20 C14 6 42 6 42 18 L42 22"
    body += cv.path(sh, stroke=PAL["metal"][2], sw=8) + cv.path(sh, stroke=PAL["metal"][0], sw=4)
    body += lift(cv, 0, 30, 56, 38, color, 9, 5)
    body += cv.circle(28, 47, 5, PAL[color][2]) + cv.rect(26, 49, 4, 10, 2, PAL[color][2])
    return cv.group(body, x, y, s)


def key(cv, x, y, s=1.0, color="sun"):
    """A key lying horizontally. Canonical 80 x 30."""
    lo, base, hi = PAL[color]
    body = cv.circle(15, 15, 14, cv.g(color)) + cv.circle(15, 15, 5.5, "var(--il-hole)")
    body += cv.rect(26, 11, 52, 8, 3, cv.g(color)) + cv.rect(60, 18, 7, 10, 2, base) + cv.rect(70, 18, 7, 7, 2, base)
    body += cv.path("M8 8 Q15 3 22 8", stroke="#fff", sw=2.4, op=.6)
    return cv.group(body, x, y, s)


def folder(cv, x, y, s=1.0, color="sun", w=84, h=62):
    body = cv.shadow(w / 2, h + 5, w * .5, 4, .2)
    body += cv.path("M0 8 Q0 0 8 0 L30 0 L38 9 L%s 9 Q%s 9 %s 17 L%s %s Q%s %s %s %s L8 %s Q0 %s 0 %s Z"
                    % (_n(w - 8), _n(w), _n(w), _n(w), _n(h - 8), _n(w), _n(h), _n(w - 8), _n(h), _n(h), _n(h), _n(h - 8)),
                    fill=PAL[color][2])
    body += cv.rect(0, 14, w, h - 14, 8, cv.g(color))
    body += cv.rect(5, 18, w - 10, 12, 5, "#fff", op=.25)
    return cv.group(body, x, y, s)


def doc(cv, x, y, s=1.0, w=62, h=80, lines=4, color="paper", head=None):
    """A sheet of paper with a folded corner and a few lines of text."""
    body = cv.shadow(w / 2, h + 6, w * .55, 4, .18)
    body += cv.path("M4 0 L%s 0 L%s 16 L%s %s Q%s %s %s %s L4 %s Q0 %s 0 %s L0 4 Q0 0 4 0 Z"
                    % (_n(w - 16), _n(w), _n(w), _n(h - 5), _n(w), _n(h), _n(w - 5), _n(h), _n(h), _n(h), _n(h - 5)),
                    fill=cv.g(color), stroke=PAL["paper"][2], sw=1.4)
    body += cv.path("M%s 0 L%s 16 L%s 16 Z" % (_n(w - 16), _n(w), _n(w - 16)), fill=PAL["paper"][2], op=.8)
    if head:
        body += cv.rect(9, 12, w * .5, 9, 3, PAL[head][1])
    for i in range(lines):
        body += cv.rect(9, 28 + i * 11, (w - 18) * (1 if i % 3 else .7), 4.5, 2, "#C5D1D9")
    return cv.group(body, x, y, s)


def magnifier(cv, x, y, s=1.0, r=20):
    """A magnifying glass, lens up and to the left. (x, y) is the lens centre."""
    body = cv.path("M%s %s L%s %s" % (_n(r * .72), _n(r * .72), _n(r * 1.8), _n(r * 1.8)), stroke=PAL["dark"][1], sw=r * .34)
    body += cv.circle(0, 0, r, "#DDF3FA", op=.55)
    body += cv.circle(0, 0, r, "none", stroke=cv.g("metal", "deep"), sw=r * .22)
    body += cv.path("M%s %s A%s %s 0 0 1 %s %s" % (_n(-r * .55), _n(-r * .1), _n(r * .6), _n(r * .6), _n(-r * .05), _n(-r * .58)),
                    stroke="#fff", sw=3, op=.9)
    return cv.group(body, x, y, s)


def bulb(cv, x, y, s=1.0, on=True):
    """A light bulb. Canonical 50 x 70."""
    body = ""
    if on:
        body += cv.circle(25, 24, 40, cv.rad("glow", [(0, "#FFE680", .75), (1, "#FFE680", 0)]))
    body += cv.path("M25 0 C6 0 -2 16 5 30 C10 40 16 44 16 54 L34 54 C34 44 40 40 45 30 C52 16 44 0 25 0 Z",
                    fill=cv.lin("bulbon" if on else "bulboff", [(0, "#FFF5B8"), (1, "#FFC93C")] if on else [(0, "#F3F6F8"), (1, "#C4CFD7")]))
    body += cv.path("M16 54 L34 54 L34 58 L16 58 Z", fill=PAL["metal"][1])
    body += cv.rect(16, 58, 18, 5, 2, PAL["metal"][2]) + cv.rect(19, 63, 12, 5, 2.5, PAL["dark"][1])
    body += cv.path("M16 20 Q20 10 28 8", stroke="#fff", sw=3.5, op=.8)
    if on:
        for a in range(-60, 61, 30):
            ra = math.radians(a - 90)
            body += cv.line(25 + math.cos(ra) * 34, 24 + math.sin(ra) * 34, 25 + math.cos(ra) * 44, 24 + math.sin(ra) * 44, "#FFC93C", 3)
    return cv.group(body, x, y, s)


def toggle(cv, x, y, on=True, w=56, h=30, color="green"):
    """A switch, on or off. Top left."""
    body = cv.rect(0, 0, w, h, h / 2, cv.g(color, "deep") if on else "#B5C2CB")
    body += cv.rect(0, 0, w, h, h / 2, "none", stroke="#10303A", sw=1, op=.15)
    kx = w - h / 2 if on else h / 2
    body += cv.circle(kx, h / 2 + 1.5, h / 2 - 3, "#10303A", op=.2)
    body += cv.circle(kx, h / 2, h / 2 - 3, "#FFFFFF")
    return cv.group(body, x, y)


def wifi(cv, cx, cy, r=26, color="#25B3BB", w=5):
    """Wireless arcs fanning upwards from a point."""
    out = cv.circle(cx, cy, w * .7, color)
    for k in (.45, .75, 1.0):
        rr = r * k
        out += cv.path("M%s %s A%s %s 0 0 1 %s %s" % (_n(cx - rr * .72), _n(cy - rr * .72), _n(rr), _n(rr), _n(cx + rr * .72), _n(cy - rr * .72)),
                       stroke=color, sw=w)
    return out


def envelope(cv, x, y, s=1.0, w=70, h=48, color="paper", flap="sky", n=None):
    """A sealed envelope, optionally numbered. Top left."""
    body = cv.shadow(w / 2, h + 5, w * .5, 4, .2)
    body += cv.rect(0, 0, w, h, 6, cv.g(color)) + cv.rect(0, 0, w, h, 6, "none", stroke=PAL["paper"][2], sw=1.4)
    body += cv.path("M2 4 L%s %s L%s 4" % (_n(w / 2), _n(h * .6), _n(w - 2)), fill="none", stroke=PAL[flap][2], sw=2.4)
    body += cv.path("M2 4 L%s %s L%s 4 Z" % (_n(w / 2), _n(h * .6), _n(w - 2)), fill=cv.g(flap), op=.9)
    if n is not None:
        body += cv.circle(w / 2, h * .56, 9, "#fff") + cv.text(w / 2, h * .56 + 5, str(n), 13, 800, fill=INK)
    return cv.group(body, x, y, s)


def pixel_cat(cv, x, y, size=80):
    """Pixel, the site's robot cat, dropped in as a nested graphic. Top left."""
    from . import cat
    svg = cat.flat(label="Pixel")
    svg = svg.replace('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100" class="cat" role="img" aria-label="Pixel"',
                      '<svg x="%s" y="%s" width="%s" height="%s" viewBox="0 0 100 100" aria-hidden="true" '
                      'style="width:%spx;height:%spx;max-width:none"' % (_n(x), _n(y), size, size, size, size))
    return svg


# ---------------------------------------------------------- panels and marks

def band(cv, x, y, w, h, r=16):
    """A soft strip that groups a row of things."""
    return cv.rect(x, y, w, h, r, "var(--il-band)")


def card(cv, x, y, w, h, r=20, title=None, color="teal", tx=.5):
    """A panel for one half of a comparison. An optional coloured heading chip sits on its top edge."""
    out = cv.rect(x, y + 3, w, h, r, "#10303A", op=.07)
    out += cv.rect(x, y, w, h, r, "var(--il-card)", stroke="var(--il-line)", sw=1.5)
    if title:
        out += pill(cv, x + w * tx, y, title, color, 17, 18, 32, 750)
    return out


def tick(cv, cx, cy, r=11):
    """A green circle with a tick."""
    out = cv.circle(cx, cy, r, cv.g("green", "deep"))
    out += cv.path("M%s %s L%s %s L%s %s" % (_n(cx - r * .45), _n(cy + r * .02), _n(cx - r * .1), _n(cy + r * .38), _n(cx + r * .5), _n(cy - r * .36)),
                   stroke="#fff", sw=max(2.2, r * .26))
    return out


def cross(cv, cx, cy, r=11):
    """A red circle with a cross."""
    out = cv.circle(cx, cy, r, cv.g("red", "deep"))
    k = r * .38
    out += cv.path("M%s %s L%s %s M%s %s L%s %s" % (_n(cx - k), _n(cy - k), _n(cx + k), _n(cy + k), _n(cx + k), _n(cy - k), _n(cx - k), _n(cy + k)),
                   stroke="#fff", sw=max(2.2, r * .26))
    return out


def photo(cv, x, y, w=80, h=60, r=6):
    """A picture: sky, sun and two hills, in a white frame. Top left."""
    out = cv.rect(x - 3, y - 3, w + 6, h + 6, r + 2, "#FFFFFF")
    out += cv.rect(x, y, w, h, r, cv.lin("photosky", [(0, "#8ED5F5"), (1, "#DDF3FB")]))
    out += cv.circle(x + w * .76, y + h * .28, h * .13, "#FFD75E")
    out += cv.path("M%s %s L%s %s Q%s %s %s %s L%s %s L%s %s Z" % (_n(x), _n(y + h), _n(x), _n(y + h * .72), _n(x + w * .2), _n(y + h * .44),
                                                                   _n(x + w * .42), _n(y + h * .66), _n(x + w * .52), _n(y + h), _n(x), _n(y + h)), fill="#5FC38C")
    out += cv.path("M%s %s Q%s %s %s %s L%s %s Z" % (_n(x + w * .36), _n(y + h), _n(x + w * .62), _n(y + h * .42), _n(x + w), _n(y + h * .7), _n(x + w), _n(y + h)),
                   fill="#37A777")
    return out


def browser_screen(cv, x, y, w, h, url="example.com", page=True):
    """The content of a screen: a browser window with an address bar and a simple page."""
    out = cv.rect(x, y, w, h, 4, "#FFFFFF")
    out += cv.rect(x, y, w, h * .17, 4, "#DCE8EE") + cv.rect(x, y + h * .1, w, h * .08, 0, "#DCE8EE")
    for i, c in enumerate(("#FF7B72", "#FFCB47", "#5BD58B")):
        out += cv.circle(x + 6 + i * 6.5, y + h * .085, 1.9, c)
    out += cv.rect(x + 28, y + h * .035, w - 36, h * .095, 3, "#FFFFFF")
    out += cv.text(x + 33, y + h * .108, url, max(5.5, h * .075), 600, fill="#4A6470", anchor="start")
    if page:
        out += cv.rect(x + 6, y + h * .24, w - 12, h * .2, 3, cv.g("teal"))
        out += cv.rect(x + 6, y + h * .5, (w - 18) / 2, h * .38, 3, "#CFE7F0") + cv.rect(x + 12 + (w - 18) / 2, y + h * .5, (w - 18) / 2, h * .38, 3, "#E6DDF3")
    return out


def book(cv, x, y, s=1.0, color="coral", label="DNS"):
    """A thick book, spine to the left, like a phone book. Canonical 110 x 130."""
    body = cv.shadow(55, 134, 58, 5, .22)
    body += cv.rect(0, 6, 110, 124, 8, PAL[color][2])
    body += cv.rect(8, 0, 102, 122, 8, "#FFFFFF")
    body += cv.rect(8, 0, 102, 122, 8, "none", stroke=PAL["paper"][2], sw=1.4)
    body += cv.rect(0, 0, 18, 124, 7, cv.g(color))
    body += cv.rect(30, 18, 66, 30, 6, cv.g(color))
    body += cv.text(63, 40, label, 20, 800, fill=_on(color))
    for i in range(4):
        body += cv.rect(30, 62 + i * 12, 66 if i % 2 == 0 else 48, 5, 2.5, "#C5D1D9")
    return cv.group(body, x, y, s)
