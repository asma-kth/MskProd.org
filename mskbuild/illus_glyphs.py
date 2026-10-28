"""Shared drawing parts for the programming and concept illustrations.

The device and people props live in illus_props. This module adds what the
code-led pictures keep needing: a syntax coloured code window, a console, a
speech bubble, and a handful of small objects (a labelled box, a machine, a
bug, a signpost, a stopwatch) that stand in for ideas.

Everything takes the Canvas first and returns SVG markup, like the props.
"""
import re

from .illus import PAL, INK, _n
from .svg import esc
from . import illus_props as P

# ------------------------------------------------------------------ code
#
# The window is dark, like the editors it imitates, so the
# colours below are fixed and chosen to clear 4.5 to 1 on the window body.

CODE_BG = ("#2A3A44", "#1C2831")
C_KW, C_BUILTIN, C_STR, C_NUM, C_COM, C_TXT, C_DIM = (
    "#D9BEFF", "#8CE3EA", "#9AF0B5", "#FFDA8A", "#B7CAD3", "#EEF4F6", "#B0C3CC")

KEYWORDS = set("""if elif else for while in def return import from class and or not try except finally with as pass
break continue lambda is raise global True False None then endif endwhile endfor next do until repeat function
endfunction procedure endprocedure switch case default endswitch const array to step elseif div mod
subroutine endsubroutine output userinput""".split())
BUILTINS = set("""print input len range int str float bool open list dict set tuple sum min max abs round sorted type
enumerate zip map filter isinstance super self random append""".split())

_TOK = re.compile(r'''(?P<com>\#.*$|//.*$)|(?P<str>[fFrR]?(?:"[^"]*"|'[^']*'))|(?P<num>\b\d+(?:\.\d+)?\b)'''
                  r'''|(?P<id>[A-Za-z_][A-Za-z_0-9]*)|(?P<ws>\s+)|(?P<op>.)''')


def tokens(line):
    """Split one line of Python or exam pseudocode into (text, colour) pieces."""
    out = []
    for m in _TOK.finditer(line):
        kind, tx = m.lastgroup, m.group()
        if kind == "com":
            col = C_COM
        elif kind == "str":
            col = C_STR
        elif kind == "num":
            col = C_NUM
        elif kind == "id":
            low = tx.lower()
            if tx in KEYWORDS or (tx.isupper() and len(tx) > 1 and low in KEYWORDS):
                col = C_KW
            elif tx in BUILTINS:
                col = C_BUILTIN
            else:
                col = C_TXT
        else:
            col = C_TXT
        out.append((tx, col))
    return out


def code_h(n, size=13, title=True):
    return (28 if title else 0) + 24 + size * 1.6 * n


def code_x(x, size=13, numbers=True):
    """Left edge of the code text, so callouts can be lined up with it."""
    return x + 14 + ((size * .6 * 2 + 8) if numbers else 0)


def code_y(y, i, size=13, title=True):
    """Baseline of line i."""
    return y + (28 if title else 0) + 12 + size * 1.6 * i + size * 1.05


def code(cv, x, y, w, lines, title="main.py", size=13, hl=(), numbers=True, bars=None, h=None, start=1):
    """A code editor window holding lines of Python or pseudocode.

    hl: indexes of lines to light up. bars: {index: colour} draws a coloured tab
    at the left of a line so it can be matched to something elsewhere.
    """
    lh = size * 1.6
    top = 28 if title is not None else 0
    h = h or (top + 24 + lh * len(lines))
    out = cv.rect(x, y + 4, w, h, 12, "#10303A", op=.18)
    out += cv.rect(x, y, w, h, 12, cv.lin("codebg", [(0, CODE_BG[0]), (1, CODE_BG[1])]))
    if title is not None:
        out += cv.rect(x, y, w, 28, 12, "#3C505B") + cv.rect(x, y + 14, w, 14, 0, "#3C505B")
        for i, c in enumerate(("#FF7B72", "#FFCB47", "#5BD58B")):
            out += cv.circle(x + 16 + i * 16, y + 14, 4.5, c)
        out += cv.text(x + w / 2, y + 18.5, title, 12, 600, fill="#D7E3E8", mono=True)
    cw = size * .6
    gx = x + 12
    tx = code_x(x, size, numbers)
    for i, line in enumerate(lines):
        ly = y + top + 12 + lh * i
        if i in hl:
            out += cv.rect(x + 5, ly - 1, w - 10, lh, 5, "#FFD479", op=.12) + cv.rect(x + 5, ly - 1, 3, lh, 1.5, "#FFD479")
        if bars and i in bars:
            out += cv.rect(x + 5, ly + 1, 4, lh - 4, 2, bars[i])
        base = ly + size * 1.05
        if numbers:
            out += ('<text x="%s" y="%s" font-size="%s" font-weight="500" class="il-m" fill="%s">%s</text>'
                    % (_n(gx), _n(base), _n(size - 1.5), C_DIM, start + i))
        spans = "".join('<tspan fill="%s">%s</tspan>' % (c, esc(t).replace(" ", " ")) for t, c in tokens(line))
        out += ('<text x="%s" y="%s" font-size="%s" font-weight="500" class="il-m">%s</text>'
                % (_n(tx), _n(base), _n(size), spans))
    return out


def terminal(cv, x, y, w, lines, title="Output", size=13):
    """A console. Each line is text, or (text, colour) for an error or a prompt."""
    lh = size * 1.55
    h = 28 + 22 + lh * len(lines)
    out = cv.rect(x, y + 4, w, h, 12, "#10303A", op=.18)
    out += cv.rect(x, y, w, h, 12, "#0F1B22")
    out += cv.rect(x, y, w, 28, 12, "#27363F") + cv.rect(x, y + 14, w, 14, 0, "#27363F")
    out += cv.text(x + 16, y + 18.5, title, 12, 600, fill="#C9D8DF", anchor="start", mono=True)
    for i, ln in enumerate(lines):
        t, col = ln if isinstance(ln, tuple) else (ln, "#CFE8DC")
        out += ('<text x="%s" y="%s" font-size="%s" font-weight="500" class="il-m" fill="%s">%s</text>'
                % (_n(x + 16), _n(y + 28 + 14 + lh * i + size * .75), _n(size), col, esc(t).replace(" ", " ")))
    return out


def term_h(n, size=13):
    return 28 + 22 + size * 1.55 * n


# --------------------------------------------------------------- bubbles

def bubble(cv, x, y, w, h, lines, tail=(0, 0), size=14, fill="#FFFFFF", tc=INK, weight=650, r=16):
    """A speech bubble. tail is the point it speaks from, as an offset from the
    bubble's centre; (0, 0) gives a plain rounded box."""
    out = cv.rect(x, y + 3, w, h, r, "#10303A", op=.12) + cv.rect(x, y, w, h, r, fill)
    if tail != (0, 0):
        cx, cy = x + w / 2, y + h / 2
        tx_, ty_ = cx + tail[0], cy + tail[1]
        bx = min(max(tx_, x + 20), x + w - 20)
        by = y + h - 1 if ty_ > cy else y + 1
        d = 1 if ty_ > cy else -1
        out += cv.poly([(bx - 9, by), (bx + 9, by), (tx_, ty_)], fill)
    ly = y + h / 2 - (len(lines) - 1) * size * .6 + size * .35
    for i, t in enumerate(lines):
        out += cv.text(x + w / 2, ly + i * size * 1.2, t, size, weight, fill=tc)
    return out


# ---------------------------------------------------------------- objects

def var_box(cv, x, y, w, h, name, value, typ=None, color="wood", tag="sun", vsize=26):
    """A cardboard box that holds a value, with its name on a label."""
    lo, base, hi = PAL[color]
    out = cv.shadow(x + w / 2, y + h + 10, w * .56, 5, .22)
    out += cv.rect(x, y + 6, w, h, 8, hi)
    out += cv.rect(x, y, w, h, 8, cv.g(color))
    out += cv.rect(x, y, w, 15, 8, "#FFFFFF", op=.22)
    out += cv.rect(x + w / 2 - 15, y, 30, 15, 3, hi, op=.55)          # the tape
    lab = max(54, len(name) * 9 + 22)
    out += cv.rect(x + w / 2 - lab / 2, y + 22, lab, 22, 6, "#FFFFFF") + cv.rect(x + w / 2 - lab / 2, y + 22, lab, 22, 6, "none", stroke=hi, sw=1.2)
    out += cv.text(x + w / 2, y + 38, name, 14, 800, fill=INK, mono=True)
    vy = y + h * .72
    out += cv.text(x + w / 2, vy, value, vsize, 800, fill=INK, mono=True)
    if typ:
        out += P.pill(cv, x + w / 2, y + h - 12, typ, tag, 11.5, 8, 18, 800)
    return out


def machine(cv, x, y, w, h, label, color="teal", sub=None):
    """A little factory machine: a hopper on top to put things in, a chute to take them out."""
    lo, base, hi = PAL[color]
    out = cv.shadow(x + w / 2, y + h + 12, w * .6, 6, .22)
    hopper = cv.poly([(x + w * .22, y - 26), (x + w * .78, y - 26), (x + w * .62, y + 4), (x + w * .38, y + 4)], cv.g("slate", "deep"))
    out += hopper + cv.rect(x + w * .22, y - 30, w * .56, 8, 4, PAL["metal"][1])
    out += P.lift(cv, x, y, w, h, color, 16, 8)
    out += cv.rect(x + w * .1, y + h - 30, w * .8, 12, 6, "#0F1A20", op=.28)
    out += P.gear(cv, x + 26, y + h - 22, 16, "slate") + P.gear(cv, x + w - 26, y + h - 22, 11, "metal")
    out += cv.rect(x + w - 8, y + h * .56, 30, 24, 4, cv.g("slate", "deep"))                  # the chute
    out += cv.poly([(x + w + 22, y + h * .56 + 24), (x + w + 22, y + h * .56 + 34), (x + w + 14, y + h * .56 + 24)], PAL["slate"][2])
    tc = P._on(color)
    out += cv.text(x + w / 2, y + 34, label, 20, 800, fill=tc, mono=True)
    if sub:
        out += cv.text(x + w / 2, y + 54, sub, 12.5, 650, fill=tc)
    return out


def bug(cv, cx, cy, s=1.0, color="red"):
    """A cartoon beetle, for an error."""
    body = ""
    for sx in (-1, 1):
        for k, ang in enumerate((-30, 5, 40)):
            body += cv.path("M%s %s l%s %s" % (_n(sx * 9), _n(-2 + k * 8), _n(sx * 12), _n(ang * .45)), stroke="#2A3E49", sw=2.6)
        body += cv.path("M%s -17 q%s -9 %s -13" % (_n(sx * 4), _n(sx * 3), _n(sx * 9)), stroke="#2A3E49", sw=2.2)
    body += cv.ellipse(0, 4, 13, 16, cv.g(color)) + cv.line(0, -10, 0, 20, PAL[color][2], 2, op=.6)
    body += cv.circle(0, -13, 8, "#2A3E49") + cv.circle(-3, -14, 1.8, "#fff") + cv.circle(3, -14, 1.8, "#fff")
    body += cv.circle(-5, 2, 2.4, "#2A3E49") + cv.circle(5, 8, 2.4, "#2A3E49") + cv.circle(-4, 11, 2, "#2A3E49")
    return cv.group(body, cx, cy, s)


def warning(cv, cx, cy, s=1.0):
    body = cv.poly([(0, -22), (23, 18), (-23, 18)], cv.g("sun"), stroke=PAL["sun"][2], sw=2.5)
    body += cv.rect(-2.4, -8, 4.8, 14, 2.4, INK) + cv.circle(0, 11, 2.6, INK)
    return cv.group(body, cx, cy, s)


def signpost(cv, x, y, labels, s=1.0, color="sun"):
    """A post with one board per label, pointing left or right alternately."""
    out = cv.rect(x - 5, y, 10, 30 + len(labels) * 42, 3, cv.g("wood", "deep"))
    for i, lab in enumerate(labels):
        w = max(80, len(lab) * 9.4 + 28)
        by = y + 6 + i * 42
        left = i % 2 == 1
        x0 = x - w + 10 if left else x - 10
        pts = ([(x0 + 14, by), (x0 + w, by), (x0 + w, by + 32), (x0 + 14, by + 32), (x0, by + 16)] if left
               else [(x0, by), (x0 + w - 14, by), (x0 + w, by + 16), (x0 + w - 14, by + 32), (x0, by + 32)])
        out += cv.poly(pts, cv.g(color), stroke=PAL[color][2], sw=2)
        out += cv.text(x0 + w / 2 + (7 if left else -7), by + 21, lab, 15, 800, fill=P._on(color), mono=True)
    return out


def stopwatch(cv, cx, cy, r=20, hand=-60):
    out = cv.rect(cx - 4, cy - r - 9, 8, 7, 2, PAL["slate"][2]) + cv.circle(cx, cy + 2, r + 2, "#10303A", op=.16)
    out += cv.circle(cx, cy, r, cv.g("metal")) + cv.circle(cx, cy, r - 4, "#FFFFFF")
    import math
    for k in range(12):
        a = math.radians(k * 30)
        out += cv.line(cx + math.cos(a) * (r - 6), cy + math.sin(a) * (r - 6), cx + math.cos(a) * (r - 9), cy + math.sin(a) * (r - 9), "#8AA0AC", 1.4)
    a = math.radians(hand)
    out += cv.line(cx, cy, cx + math.cos(a) * (r - 8), cy + math.sin(a) * (r - 8), "#E6574D", 2.6) + cv.circle(cx, cy, 2.6, INK)
    return out


def lockers(cv, x, y, n, w=84, h=96, gap=10, values=None, start=0, color="sky", hot=None, colors=None):
    """A row of numbered lockers, each holding a value. Returns markup and the centre x of each."""
    out, xs = "", []
    for i in range(n):
        lx = x + i * (w + gap)
        col = "sun" if hot == i else (colors or {}).get(i, color)
        out += cv.shadow(lx + w / 2, y + h + 8, w * .55, 4, .2)
        out += P.lift(cv, lx, y, w, h, col, 10, 6, hl=False)
        out += cv.rect(lx + 8, y + 8, w - 16, 16, 4, "#FFFFFF", op=.35)
        out += cv.circle(lx + w - 17, y + 16, 3.2, PAL[col][2], op=.7)
        v = None if values is None or i >= len(values) else values[i]
        if v is not None:
            out += cv.rect(lx + 10, y + 36, w - 20, h - 52, 7, "#FFFFFF")
            out += cv.text(lx + w / 2, y + 36 + (h - 52) / 2 + 8, str(v), 22 if len(str(v)) < 4 else 17, 800, fill=INK, mono=True)
        out += cv.text(lx + w / 2, y + h + 32, str(start + i), 17, 800, cls="il-ink", mono=True)
        xs.append(lx + w / 2)
    return out, xs


def cylinder(cv, cx, cy, w=64, h=70, color="sky", rows=3):
    """The database drum."""
    lo, base, hi = PAL[color]
    ry = w * .16
    out = cv.shadow(cx, cy + h / 2 + 8, w * .55, 4, .2)
    out += cv.rect(cx - w / 2, cy - h / 2 + ry, w, h - ry, 0, cv.g(color, "side"))
    out += cv.ellipse(cx, cy + h / 2, w / 2, ry, hi)
    out += cv.rect(cx - w / 2, cy - h / 2 + ry, w, h - ry - 1, 0, cv.g(color, "side"))
    for i in range(rows):
        yy = cy - h / 2 + ry + (i + 1) * (h - ry) / (rows + 1)
        out += cv.path("M%s %s Q%s %s %s %s" % (_n(cx - w / 2), _n(yy), _n(cx), _n(yy + ry * 2), _n(cx + w / 2), _n(yy)), stroke=hi, sw=2, op=.6)
    out += cv.ellipse(cx, cy - h / 2 + ry, w / 2, ry, lo)
    return out


def flag(cv, x, y, s=1.0, color="coral"):
    body = cv.rect(-1.5, 0, 3, 34, 1.5, PAL["dark"][1]) + cv.poly([(1.5, 1), (22, 6), (1.5, 14)], cv.g(color))
    return cv.group(body, x, y, s)


def arrow_ring(cv, cx, cy, r, a0=-60, a1=240, color="#25B3BB", w=6, head=14):
    """A circular arrow, for a loop."""
    import math
    p0 = (cx + r * math.cos(math.radians(a0)), cy + r * math.sin(math.radians(a0)))
    p1 = (cx + r * math.cos(math.radians(a1)), cy + r * math.sin(math.radians(a1)))
    big = 1 if (a1 - a0) % 360 > 180 else 0
    out = cv.path("M%s %s A%s %s 0 %d 1 %s %s" % (_n(p0[0]), _n(p0[1]), _n(r), _n(r), big, _n(p1[0]), _n(p1[1])), stroke=color, sw=w)
    t = math.radians(a1 + 90)
    tip = (p1[0] + math.cos(t) * head * .9, p1[1] + math.sin(t) * head * .9)
    nx, ny = math.cos(math.radians(a1)), math.sin(math.radians(a1))
    left = (p1[0] + nx * head * .6, p1[1] + ny * head * .6)
    right = (p1[0] - nx * head * .6, p1[1] - ny * head * .6)
    return out + cv.poly([tip, left, right], color)


def sun(cv, cx, cy, r=18):
    import math
    out = ""
    for k in range(10):
        a = math.radians(k * 36)
        out += cv.line(cx + math.cos(a) * (r + 5), cy + math.sin(a) * (r + 5), cx + math.cos(a) * (r + 12), cy + math.sin(a) * (r + 12), "#FFB020", 3.4)
    out += cv.circle(cx, cy, r, cv.rad("sunball", [(0, "#FFF3A8"), (1, "#FFC93C")], .4, .35, .75))
    return out


def umbrella(cv, cx, cy, s=1.0, color="sky"):
    body = cv.line(0, -6, 0, 22, "#4A5A64", 3.4) + cv.path("M0 22 q0 8 -7 7", stroke="#4A5A64", sw=3.4)
    body += cv.path("M-28 -4 A28 28 0 0 1 28 -4 Q21 -12 14 -4 Q7 -12 0 -4 Q-7 -12 -14 -4 Q-21 -12 -28 -4 Z", fill=cv.g(color, "deep"))
    body += cv.path("M-14 -22 q4 -10 14 -12", stroke="#fff", sw=3, op=.5)
    for dx in (-18, -6, 6, 18):
        body += cv.line(dx, 14 + abs(dx) * .05, dx - 1, 20, "#6FB8E6", 2.4, op=.0)
    return cv.group(body, cx, cy, s)


def plate_flat(cv, cx, cy, r=34, color="paper"):
    out = cv.ellipse(cx, cy + 4, r, r * .42, "#10303A", op=.16)
    out += cv.ellipse(cx, cy, r, r * .42, cv.g(color)) + cv.ellipse(cx, cy, r * .66, r * .26, "none", stroke=PAL["paper"][2], sw=1.6)
    return out


def cookie(cv, cx, cy, r=8):
    out = cv.circle(cx, cy + 1.5, r, "#8A5A2B") + cv.circle(cx, cy, r, cv.g("wood"))
    for dx, dy in ((-3, -2), (3, 1), (-1, 4), (3, -4)):
        out += cv.circle(cx + dx * r / 8, cy + dy * r / 8, max(1, r * .16), "#5B3A1B")
    return out


def fingerprint(cv, cx, cy, s=1.0, color="#1F3A44"):
    body = ""
    for k, r in enumerate((6, 11, 16, 21, 26)):
        body += cv.path("M%s %s A%s %s 0 1 1 %s %s" % (_n(-r), _n(6 - k), _n(r), _n(r * 1.12), _n(r - 1), _n(8 + k * 1.5)), stroke=color, sw=2.6, op=.9)
    body += cv.line(0, 2, 0, 24, color, 2.6)
    return cv.group(body, cx, cy, s)


def key_hole(cv, cx, cy, s=1.0):
    body = cv.circle(0, -6, 8, "#2A3E49") + cv.poly([(-4, 0), (4, 0), (6, 16), (-6, 16)], "#2A3E49")
    return cv.group(body, cx, cy, s)
