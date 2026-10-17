"""Key Stage 3 illustrations: lighting a 3D scene, keyframe animation, logo design and vector shapes."""
import math

from .illus import Canvas, PAL, INK, ARROW, figure, illustration, _n
from . import illus_props as P
from . import illus_glyphs as G


def glow(cv, cx, cy, r, color, o=.8):
    return cv.circle(cx, cy, r, cv.rad("glow%s" % color.lstrip("#"), [(0, color, o), (1, color, 0)]))


# ------------------------------------------------------------------ lights and camera

def cube(cv, cx, cy, s=1.0):
    top = [(cx, cy - 40 * s), (cx + 48 * s, cy - 16 * s), (cx, cy + 8 * s), (cx - 48 * s, cy - 16 * s)]
    left = [(cx - 48 * s, cy - 16 * s), (cx, cy + 8 * s), (cx, cy + 62 * s), (cx - 48 * s, cy + 38 * s)]
    right = [(cx, cy + 8 * s), (cx + 48 * s, cy - 16 * s), (cx + 48 * s, cy + 38 * s), (cx, cy + 62 * s)]
    return cv.poly(left, "#66B8EC", stroke="#2F82C0", sw=1.4) + cv.poly(right, "#2F82C0", stroke="#1F5F9A", sw=1.4) + cv.poly(top, "#C9EAFB", stroke="#66B8EC", sw=1.4)


def camera(cv, cx, cy):
    out = cv.rect(cx - 34, cy - 18, 68, 38, 8, cv.g("dark", "deep")) + cv.rect(cx - 14, cy - 28, 28, 12, 4, cv.g("dark"))
    return out + cv.circle(cx, cy + 1, 13, "#0F1A20") + cv.circle(cx, cy + 1, 8, cv.rad("lens", [(0, "#9FD3F0"), (1, "#2F82C0")], .35, .3, .8)) + cv.circle(cx + 22, cy - 9, 3, "#F0584B")


def sphere(cv, cx, cy, r, key=True, fill=0.0, rim=False):
    dark = ("#16293A", "#46657D", "#46657D")[0 if fill == 0 else 1]
    g = cv.rad("sph%d" % int(fill * 10 + (5 if rim else 0)), [(0, "#FFFFFF"), (.22, "#BFD8E8"), (.7, "#4A6F8A"), (1, dark)], .34, .3, .78, .3, .26)
    out = cv.shadow(cx, cy + r + 8, r * .9, 5, .22) + cv.circle(cx, cy, r, g)
    if rim:
        out += cv.path("M%s %s A%s %s 0 0 1 %s %s" % (_n(cx + r * .2), _n(cy - r * .97), r, r, _n(cx + r * .97), _n(cy + r * .22)), stroke="#FFFFFF", sw=4, op=.85)
    return out


@illustration("lights-camera")
def _lights():
    cv = Canvas(800, 500).backdrop()
    cv.add(P.card(cv, 14, 28, 506, 454, 20, "Three point lighting", "sun"))
    cv.add(P.badge(cv, 36, 54, 1))
    sx, sy = 267, 258
    # the beams first
    cv.add(cv.poly([(96, 150), (228, 214), (232, 290)], "#FFD24A", op=.34), cv.poly([(440, 176), (306, 224), (312, 292)], "#FFD24A", op=.17), cv.poly([(267, 124), (232, 206), (302, 206)], "#FFD24A", op=.2))
    cv.add(cv.poly([(267, 420), (176, 296), (358, 296)], "#25B3BB", op=.15))
    cv.add(cube(cv, sx, sy - 16, 1.0))
    cv.add(glow(cv, 85, 114, 38, "#FFE680", .5), P.bulb(cv, 60, 90, 1.0, True))
    cv.add(cv.text(20, 196, "key light", 15, 800, anchor="start", cls="il-ink"), cv.text(20, 214, "the main, brightest source", 12.5, 650, anchor="start", cls="il-ink2"))
    cv.add(glow(cv, 445, 134, 38, "#FFE680", .3), P.bulb(cv, 420, 110, 1.0, True))
    cv.add(cv.text(500, 222, "fill light", 15, 800, anchor="end", cls="il-ink"), cv.text(500, 240, "softer: lifts the shadows", 12.5, 650, anchor="end", cls="il-ink2"))
    cv.add(glow(cv, 267, 82, 38, "#FFE680", .5), P.bulb(cv, 242, 58, 1.0, True))
    cv.add(cv.text(312, 92, "back light", 15, 800, anchor="start", cls="il-ink"), cv.text(312, 110, "separates it from", 12.5, 650, anchor="start", cls="il-ink2"), cv.text(312, 126, "the background", 12.5, 650, anchor="start", cls="il-ink2"))
    cv.add(camera(cv, 267, 438))
    cv.add(cv.text(318, 436, "camera", 15, 800, anchor="start", cls="il-ink"), cv.text(318, 454, "frames the shot", 12.5, 650, anchor="start", cls="il-ink2"))
    # what each light adds
    cv.add(P.card(cv, 536, 28, 250, 454, 20, "What each light adds", "plum"))
    cv.add(P.badge(cv, 558, 54, 2))
    for i, (lab, sub, kw) in enumerate((("key light only", "hard shadow on one side", dict(fill=0.0, rim=False)), ("+ fill light", "shadow softened", dict(fill=1.0, rim=False)), ("+ back light", "bright edge lifts it off the background", dict(fill=1.0, rim=True)))):
        y = 124 + i * 126
        cv.add(sphere(cv, 596, y, 40, **kw))
        cv.add(cv.text(650, y - 8, lab, 14, 800, anchor="start", cls="il-ink"))
        for j, ln in enumerate(wrap(sub, 17)):
            cv.add(cv.text(650, y + 12 + j * 16, ln, 12.5, 650, anchor="start", cls="il-ink2"))
    return figure(
        "lights-camera", cv, "Three point lighting around a cube with a camera, and what each light adds to a sphere",
        "A scene seen from above with three lights and a camera around a cube. The key light, at upper left, is the main and brightest source. "
        "The fill light, on the right, is softer and lifts the shadows on the other side. The back light is behind the subject and separates "
        "it from the background. The camera is at the bottom and its cone shows what it frames. On the right three spheres show what each light "
        "adds. With the key light only, one side is bright and the other has a hard dark shadow. Adding the fill light softens the shadow. "
        "Adding the back light puts a bright edge on the sphere that lifts it off the background.",
        ["Three point lighting uses a key light, a fill light and a back light, and a camera frames the shot.",
         "The key light makes the shape, the fill light softens its shadows, and the back light gives it a bright edge."],
        "Lighting does more than make a scene visible. It makes shapes readable and sets the mood.")


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


# ------------------------------------------------------------------ keyframes

def bez(p0, p1, p2, t):
    return ((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * p1[0] + t * t * p2[0], (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * p1[1] + t * t * p2[1])


def ball(cv, x, y, r=17, op=None):
    out = cv.circle(x, y, r, cv.rad("ball", [(0, "#FFC6BB"), (.6, "#F77F72"), (1, "#C84B43")], .35, .3, .8))
    out += cv.circle(x - r * .35, y - r * .35, r * .22, "#FFFFFF", op=.6)
    return '<g opacity="%s">%s</g>' % (op, out) if op is not None else out


@illustration("keyframes")
def _keyframes():
    cv = Canvas(800, 500).backdrop()
    cv.add(P.card(cv, 14, 28, 772, 290, 20, "You set keyframes. The computer fills in the rest.", "coral"))
    p0, p1, p2 = (90, 214), (400, -34), (710, 214)
    cv.add(cv.path("M%s %s Q%s %s %s %s" % (p0[0], p0[1], p1[0], p1[1], p2[0], p2[1]), stroke="#8AA0AC", sw=2, dash="3 7"))
    for k in range(1, 12):
        if k == 6:
            continue
        x, y = bez(p0, p1, p2, k / 12.0)
        cv.add(cv.shadow(x, 236, 14, 3, .1))
        cv.add(ball(cv, x, y, 17, .32), cv.circle(x, y, 17, "none", stroke="#C84B43", sw=1.4, dash="3 4", op=.6))
    for k, t in enumerate((0, .5, 1)):
        x, y = bez(p0, p1, p2, t)
        cv.add(cv.shadow(x, 236, 20, 4, .22), ball(cv, x, y, 19))
    # the timeline
    cv.add(cv.line(90, 268, 710, 268, "#8AA0AC", 3))
    for k in range(0, 49, 4):
        xx = 90 + k / 47.0 * 620
        cv.add(cv.line(xx, 263, xx, 273, "#8AA0AC", 1.6))
    for f, t in ((1, 0), (24, 23 / 47.0), (48, 1)):
        xx = 90 + t * 620
        cv.add(cv.poly([(xx, 256), (xx + 11, 268), (xx, 280), (xx - 11, 268)], cv.g("sun", "deep"), stroke="#8C6400", sw=1.6))
        cv.add(cv.text(xx, 300, "frame %d" % f, 13.5, 800, cls="il-ink", mono=True))
    cv.add(P.pill(cv, 400, 150, "keyframe: a key moment you set", "sun", 13, 12, 26, 750), P.pill(cv, 400, 188, "in-between frames: worked out for you", "paper", 13, 12, 26, 700))
    cv.add(P.badge(cv, 36, 54, 1))
    # easing
    for x, title, col, ease in ((14, "Linear: constant speed", "slate", False), (406, "Easing: slow in, slow out", "teal", True)):
        cv.add(P.card(cv, x, 342, 380, 144, 20, title, col))
        ox, oy, w, h = x + 40, 462, 150, 90
        cv.add(cv.line(ox, oy - h - 8, ox, oy, ARROW, 2), cv.line(ox, oy, ox + w + 8, oy, ARROW, 2))
        cv.add(cv.text(ox + w + 4, oy + 16, "time", 12, 650, anchor="end", cls="il-ink2"), cv.text(ox + 10, oy - h + 6, "position", 12, 650, anchor="start", cls="il-ink2"))
        f = (lambda t: t * t * (3 - 2 * t)) if ease else (lambda t: t)
        cv.add(cv.path("M" + " L".join("%s %s" % (_n(ox + t / 40.0 * w), _n(oy - f(t / 40.0) * h)) for t in range(41)), stroke="#C84B43" if not ease else "#0F7C84", sw=3.6))
        for k in range(11):
            t = k / 10.0
            cv.add(cv.circle(ox + t * w, oy - f(t) * h, 4.4, "#FFFFFF", stroke=INK, sw=2))
        lines = ("starts and stops suddenly,", "like a machine") if not ease else ("starts and stops gently,", "like real things do")
        cv.add(cv.text(x + 206, 410, lines[0], 12.5, 700, anchor="start", cls="il-ink"), cv.text(x + 206, 429, lines[1], 12.5, 700, anchor="start", cls="il-ink"))
        cv.add(cv.text(x + 206, 454, "dots: equal steps in time", 11.5, 650, anchor="start", cls="il-ink2"))
    cv.add(P.badge(cv, 36, 344, 2), P.badge(cv, 428, 344, 3))
    return figure(
        "keyframes", cv, "A bouncing ball animated with three keyframes, and the difference between linear motion and easing",
        "How keyframe animation works. An animator sets keyframes at the key moments: here frame 1 with the ball on the left, frame 24 with the "
        "ball at the top of its arc, and frame 48 with the ball on the right. The software works out all the in-between frames, drawn as "
        "faded balls along the arc. Below, two graphs of position against time compare linear motion, a straight line where the dots are "
        "evenly spaced, so it starts and stops suddenly like a machine, with easing, an S shaped curve where the dots bunch up at the start "
        "and end, so it starts and stops gently like real things do.",
        ["Keyframes are the key moments the animator sets. The computer works out the frames in between, which is called interpolation or tweening.",
         "Linear motion has constant speed. It starts and stops suddenly, which looks like a machine.",
         "Easing starts and stops gradually, because real objects speed up and slow down."],
        "An animator does not draw every frame. Set the keyframes, then ease the movement between them.")


# ------------------------------------------------------------------ logo design

def logo(cv, cx, cy, s=1.0, mode="colour"):
    ink = {"colour": "#14707A", "mono": INK, "rev": "#FFFFFF"}[mode]
    body = ""
    if mode == "colour":
        body += cv.circle(0, 0, 50, cv.g("deep", "deep"))
    else:
        body += cv.circle(0, 0, 46, "none", stroke=ink, sw=6)
    fg = "#FFFFFF" if mode == "colour" else ink
    body += cv.path("M-22 -6 L22 -6 L18 22 Q16 30 8 30 L-8 30 Q-16 30 -18 22 Z", fill=fg)
    body += cv.path("M22 0 q14 0 12 12 q-2 10 -14 8", stroke=fg, sw=5)
    body += cv.path("M-8 -13 q-6 -8 0 -14 M6 -13 q-6 -8 0 -14", stroke=fg, sw=3.6)
    body += cv.path("M-14 40 Q0 28 16 36 Q8 49 -14 40 Z", fill="#8CE3C0" if mode == "colour" else ink)
    return cv.group(body, cx, cy, s)


@illustration("logo-design")
def _logo():
    cv = Canvas(800, 500).backdrop()
    cv.add(P.card(cv, 14, 28, 262, 222, 20, "Full colour", "teal"))
    cv.add(logo(cv, 145, 142, 1.35, "colour"))
    cv.add(cv.text(145, 232, "a simple vector shape", 13, 650, cls="il-ink2"))
    cv.add(P.card(cv, 290, 28, 246, 222, 20, "Test it small", "sky"))
    for (cx, s, lab) in ((350, .8, "poster"), (432, .32, "app icon"), (490, .16, "tab")):
        cv.add(logo(cv, cx, 134, s, "colour"), cv.text(cx, 190, lab, 12, 650, cls="il-ink2"))
    cv.add(cv.text(413, 232, "still readable at 16 pixels", 13, 650, cls="il-ink2"))
    cv.add(P.card(cv, 552, 28, 234, 454, 20, "What makes it work", "mint"))
    for i, (t, sub) in enumerate((("Simple", "recognised at 16 pixels"), ("One colour", "works on a stamp or a fax"), ("Distinctive", "not like ten others"), ("Appropriate", "suits audience and purpose"), ("A vector", "so it scales to any size"))):
        y = 82 + i * 76
        cv.add(P.tick(cv, 580, y + 8, 12), cv.text(604, y + 6, t, 15.5, 800, anchor="start", cls="il-ink"), cv.text(604, y + 26, sub, 12.5, 650, anchor="start", cls="il-ink2"))
    cv.add(P.card(cv, 14, 272, 522, 210, 20, "Test it in one colour", "coral"))
    for i, (bg, mode, lab) in enumerate((("#FFFFFF", "mono", "black on white"), (INK, "rev", "white on dark"), ("#F77F72", "mono", "on a colour"))):
        x = 34 + i * 164
        cv.add(cv.rect(x, 306, 148, 130, 12, bg, stroke="#B9C6CE", sw=1.4), logo(cv, x + 74, 366, .95, mode))
        cv.add(cv.text(x + 74, 462, lab, 13, 700, cls="il-ink"))
    cv.add(P.badge(cv, 36, 52, 1), P.badge(cv, 312, 52, 2), P.badge(cv, 574, 52, 3), P.badge(cv, 36, 274, 4))
    return figure(
        "logo-design", cv, "A café logo in full colour, at small sizes and in one colour, with five rules for a good logo",
        "A logo of a coffee cup with steam and a leaf inside a circle, shown in full colour, then tested at three sizes: a poster, an app icon "
        "and a 16 pixel browser tab, where it must still be readable. It is also tested in one colour: black on white, white on dark, and on a "
        "coloured background. Five rules for a good logo are listed: it is simple, it works in one colour, it is distinctive, it is "
        "appropriate for the audience and purpose, and it is a vector so it scales to any size.",
        ["A logo should be a simple shape.", "Test it small: it must still be recognised at 16 pixels.", "It must be a vector so it can scale, and work in one colour.",
         "Test it in one colour, reversed out, and on a colour, because it will be used in all of them."],
        "Sketch first, on paper. Ten minutes of rough ideas beats an hour of dragging shapes about.")


# ------------------------------------------------------------------ vector shapes

@illustration("vector-nodes")
def _nodes():
    cv = Canvas(800, 500).backdrop()
    cv.add(P.card(cv, 14, 28, 446, 454, 20, "A shape is made of nodes", "plum"))
    cv.add(P.badge(cv, 36, 54, 1))
    d = "M120 330 C120 200 250 120 410 120 C410 250 330 380 200 400 C150 405 120 380 120 330 Z"
    for i in range(10):
        cv.add(cv.line(34 + i * 42, 70, 34 + i * 42, 470, "var(--il-line)", .8, op=.5), cv.line(30, 74 + i * 40, 450, 74 + i * 40, "var(--il-line)", .8, op=.5))
    cv.add(cv.path(d, fill=cv.g("coral"), stroke="#8F2923", sw=5))
    for (hx, hy) in ((250, 120), (410, 250)):
        cv.add(cv.line(410, 120, hx, hy, "#0F7C84", 2.4), cv.circle(hx, hy, 6, "#FFFFFF", stroke="#0F7C84", sw=3))
    for (nx, ny, sel) in ((120, 330, False), (410, 120, True), (200, 400, False)):
        cv.add(cv.rect(nx - 8, ny - 8, 16, 16, 2, "#25B3BB" if sel else "#FFFFFF", stroke=INK, sw=2.4))
    cv.add(cv.text(424, 104, "node", 14, 800, anchor="start", cls="il-ink"))
    cv.add(cv.text(250, 100, "handle: drag to bend the curve", 13, 750, cls="il-ink"))
    cv.add(cv.text(430, 266, "handle", 13, 750, anchor="start", cls="il-ink"))
    cv.add(cv.text(250, 296, "fill: the colour inside", 13, 750, fill=INK))
    cv.add(P.arrow(cv, [(84, 400), (116, 372)], "#8F2923", 3, 9), cv.text(30, 418, "stroke: the outline", 13, 750, anchor="start", cls="il-ink"))
    # combining shapes
    cv.add(P.card(cv, 476, 28, 310, 224, 20, "Combine shapes", "teal"))
    cv.add(P.badge(cv, 498, 54, 2))
    ra, rb = 26, 26
    for i, name in enumerate(("Union", "Difference", "Intersection")):
        cx = 524 + i * 100
        ax, bx_, y = cx - 14, cx + 14, 130
        clip = cv._def("cb%d" % i, '<clipPath id="{id}"><circle cx="%s" cy="%s" r="%s"/></clipPath>' % (bx_, y, rb))
        mask = cv._def("mk%d" % i, '<mask id="{id}"><rect x="%s" y="%s" width="120" height="100" fill="#FFFFFF"/><circle cx="%s" cy="%s" r="%s" fill="#000000"/></mask>' % (cx - 60, y - 50, bx_, y, rb))
        cv.add(cv.circle(ax, y, ra, "none", stroke="#8AA0AC", sw=1.6, dash="3 4"), cv.circle(bx_, y, rb, "none", stroke="#8AA0AC", sw=1.6, dash="3 4"))
        if i == 0:
            cv.add(cv.circle(ax, y, ra, cv.g("teal")), cv.circle(bx_, y, rb, cv.g("teal")), cv.circle(ax, y, ra, "none", stroke="#0F7C84", sw=2.4), cv.circle(bx_, y, rb, "none", stroke="#0F7C84", sw=2.4))
        elif i == 1:
            cv.add('<g mask="%s">%s</g>' % (mask, cv.circle(ax, y, ra, cv.g("teal"))))
        else:
            cv.add('<g clip-path="%s">%s</g>' % (clip, cv.circle(ax, y, ra, cv.g("teal"))))
        cv.add(cv.text(cx, 188, name, 13, 750, cls="il-ink"))
    cv.add(cv.text(631, 220, "two shapes in, one new shape out", 12.5, 650, cls="il-ink2"))
    # layers
    cv.add(P.card(cv, 476, 274, 310, 208, 20, "Layers and grouping", "sun"))
    cv.add(P.badge(cv, 498, 300, 3))
    for i, (col, dx, lab) in enumerate((("sky", 0, "bottom"), ("mint", 22, "middle"), ("coral", 44, "top"))):
        cv.add(P.lift(cv, 498 + dx, 332 + dx * .7, 62, 62, col, 10, 5, hl=False))
    cv.add(cv.text(620, 358, "the last one drawn", 12.5, 700, anchor="start", cls="il-ink"), cv.text(620, 376, "sits on top", 12.5, 700, anchor="start", cls="il-ink"))
    cv.add(cv.text(620, 406, "raise and lower", 12.5, 650, anchor="start", cls="il-ink2"), cv.text(620, 424, "change the order", 12.5, 650, anchor="start", cls="il-ink2"))
    cv.add(cv.text(631, 462, "group: join shapes so they move as one", 12.5, 700, cls="il-ink"))
    return figure(
        "vector-nodes", cv, "A vector shape as nodes and handles, combining shapes, and layers",
        "How vector shapes are built. A shape is a path made of nodes, the corners and curve points, joined by curves. A selected node shows "
        "its handles, which you drag to bend the curve. The fill is the colour inside the shape and the stroke is the outline. Shapes can be "
        "combined: union merges two shapes into one, difference cuts the top shape out of the one beneath, and intersection keeps only the "
        "overlap. Shapes also stack in layers: the last one drawn sits on top, raise and lower change the order, and group joins shapes so "
        "they move and scale together.",
        ["A path is made of nodes. Select a node and its handles appear, and dragging a handle bends the curve. Fill is the colour inside and stroke is the outline.",
         "Union merges shapes, difference cuts one out of the other, and intersection keeps only the overlap.",
         "Shapes stack. The last one drawn is on top, and raise, lower and group change that."],
        "Because a vector is described by points and curves, not pixels, it can be scaled to any size without going blurry.")
