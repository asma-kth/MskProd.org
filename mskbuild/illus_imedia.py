"""Illustrations for the iMedia units: navigation, storyboards and the production phases."""
import math

from .illus import Canvas, PAL, INK, figure, illustration, _n
from . import illus_props as P


def house(cv, cx, cy, s=1.0, color="#FFFFFF"):
    body = cv.poly([(-7, .5), (0, -6.5), (7, .5)], color) + cv.rect(-4.6, 0, 9.2, 6.5, 0, color)
    return cv.group(body, cx, cy, s)


# ------------------------------------------------------------- navigation

LEVEL = {0: ("teal", 1), 1: ("sky", 1), 2: ("lilac", 1), 3: ("slate", .8), 4: ("slate", .62)}


def screen(cv, cx, cy, label, level, exit_=True):
    """One screen of the product as a small card with its own navigation bar."""
    col, op = LEVEL[level]
    x, y, w, h = cx - 46, cy - 29, 92, 58
    body = P.lift(cv, x, y, w, h, col, 10, 5, hl=False)
    body += cv.rect(x + 5, y + 5, w - 10, 11, 5, "#FFFFFF", op=.65)
    body += cv.circle(x + 12, y + 10.5, 2, PAL[col][2]) + cv.circle(x + 19, y + 10.5, 2, PAL[col][2])
    body += house(cv, x + w - 15, y + 10.5, 1, PAL[col][2]) if exit_ else P.cross(cv, x + w - 15, y + 10.5, 6)
    return '<g opacity="%s">%s</g>%s' % (op, body, cv.text(cx, cy + 12, label, 13, 800, fill=P._on(col)))


def link(cv, a, b, level):
    (ax, ay), (bx, by) = a, b
    col, op = PAL["teal"][2], {1: 1, 2: .95, 3: .8, 4: .6}[level]
    if abs(ay - by) < 1:
        return P.arrow(cv, [(ax + 49, ay), (bx - 52, by)], col, 4.5, 12, op=op)
    return P.curve_arrow(cv, (ax + 49, ay), (ax + 83, ay), (bx - 83, by), (bx - 52, by), col, 4.5, 12, op=op)


@illustration("imedia-navigation-depth")
def _nav():
    cv = Canvas(800, 500).backdrop()
    cols = [84, 244, 404, 564, 724]
    for i in (0, 2, 4):
        cv.add(P.band(cv, cols[i] - 74, 58, 148, 384, 16))
    pos = {"Home": (84, 272), "Shop": (244, 138), "About": (244, 272), "Contact": (244, 396),
           "Products": (404, 112), "Basket": (404, 192), "Team": (404, 272),
           "Product": (564, 112), "Order done": (564, 192), "Sizes": (724, 112)}
    lvl = {"Home": 0, "Shop": 1, "About": 1, "Contact": 1, "Products": 2, "Basket": 2, "Team": 2, "Product": 3, "Order done": 3, "Sizes": 4}
    edges = [("Home", "Shop"), ("Home", "About"), ("Home", "Contact"), ("Shop", "Products"), ("Shop", "Basket"),
             ("About", "Team"), ("Products", "Product"), ("Basket", "Order done"), ("Product", "Sizes")]
    for a, b in edges:
        cv.add(link(cv, pos[a], pos[b], lvl[b]))
    for name, (cx, cy) in pos.items():
        cv.add(screen(cv, cx, cy, name, lvl[name], exit_=(name != "Order done")))
    # a screen nothing links to
    ox, oy = 564, 380
    cv.add(cv.rect(ox - 46, oy - 29, 92, 58, 10, "#FFFFFF", op=.9, stroke="#C84B43", sw=2.5, dash="6 5"))
    cv.add(house(cv, ox + 31, oy - 18.5, 1, "#8A9AA5"), cv.text(ox, oy + 12, "Old offers", 13, 800, fill=INK))
    # the ruler across the top
    for i, (t, (c, _)) in enumerate(zip(("0 clicks", "1 click", "2 clicks", "3 clicks", "4 clicks"), LEVEL.values())):
        cv.add(P.pill(cv, cols[i], 36, t, c, 14, 13, 28, 800))
    cv.add(cv.text(244, 72, "most visitors stop here", 12.5, 700, cls="il-ink"))
    # the two faults
    cv.add(P.pill(cv, 564, 240, "dead end: no way out", "coral", 13, 12, 26, 800))
    cv.add(P.pill(cv, 564, 428, "orphan: nothing links to it", "coral", 13, 12, 26, 800))
    # visitors drain away with every click
    grad = cv.lin("nav-drain", [(0, "#25B3BB"), (1, "#C3CFD8")], 0, 0, 1, 0)
    cv.add(cv.rect(40, 450, 720, 14, 7, grad))
    cv.add(cv.text(40, 484, "most visitors", 13, 700, anchor="start", cls="il-ink2"), cv.text(400, 484, "every extra click loses people", 13, 800, cls="il-ink"),
           cv.text(760, 484, "almost nobody", 13, 700, anchor="end", cls="il-ink2"))
    cv.add(P.badge(cv, 28, 36, 1), P.badge(cv, 186, 36, 2), P.badge(cv, 346, 36, 3), P.badge(cv, 660, 36, 4),
           P.badge(cv, 676, 240, 5), P.badge(cv, 700, 428, 5))
    return figure(
        "imedia-navigation-depth", cv, "How deep is your navigation",
        "A navigation diagram drawn as columns of screens, one column for each number of clicks away from the home screen. The home screen "
        "is the entry point and everything is measured from it. One click away are the main sections, Shop, About and Contact, which is where "
        "most visitors stop. Two clicks away is the content itself, a product list, a basket and a team page, still comfortably reachable. "
        "Further right the screens fade: a product page three clicks away and a size guide four clicks away, which is buried content that "
        "almost nobody reaches however good it is, because every extra click loses visitors, shown by the bar along the bottom fading from "
        "many visitors to almost nobody. Two faults are also shown. The order done screen is a dead end: it has no home button and no way "
        "onward, so the user is stuck. The old offers screen is an orphan: nothing links to it, so it can never be reached at all. Both are "
        "immediately visible on a navigation diagram drawn before building, and both are very hard to spot in a product that is half built.",
        ["The home screen is the entry point. Everything is measured from here.",
         "One click down: the main sections. This is where most visitors stop.",
         "Two clicks down: the content itself. Still comfortable.",
         "Four clicks down: almost nobody gets here, however good it is.",
         "And watch for a screen with no way out, or no way in at all."],
        "Three or four clicks from the entry point is the practical limit. Deeper than that and the content may as well not exist.")


# --------------------------------------------------------------- storyboard

FW, FH = 160, 90


def frame_art(cv, kind, fade=False):
    """A frame of the little café scene, in a 160 x 90 box."""
    wall = cv.lin("sb-wall", [(0, "#FFF3D9"), (1, "#F6DBAC")])
    wood = cv.lin("sb-wood", [(0, "#E2AE6C"), (1, "#C58B47")])
    out = cv.rect(0, 0, FW, FH, 0, wall)
    if kind == "close":
        for (x, y, r, c) in ((20, 22, 16, "#FFD27A"), (138, 18, 12, "#9BD9F2"), (128, 70, 18, "#FFB8A8"), (14, 72, 10, "#B7E8C9")):
            out += cv.circle(x, y, r, c, op=.55)
        out += P.person(cv, 26, -5, .86, "tan", "black", "teal", "bun", False, mood="open")
        return out
    out += cv.rect(0, 64, FW, 26, 0, wood) + cv.rect(0, 64, FW, 2, 0, "#fff", op=.35)
    if kind == "wide":
        out += cv.rect(12, 10, 42, 34, 4, cv.lin("sb-sky", [(0, "#9EDCF7"), (1, "#E3F5FC")])) + cv.rect(12, 10, 42, 34, 4, "none", stroke="#8E5B2B", sw=2.5)
        out += cv.line(33, 10, 33, 44, "#8E5B2B", 2) + cv.line(12, 27, 54, 27, "#8E5B2B", 2) + cv.circle(44, 18, 4.5, "#FFD75E")
        out += cv.line(100, 0, 100, 12, "#6B4A2B", 1.6) + cv.path("M92 22 L96 12 L104 12 L108 22 Z", fill="#FFC93C")
        out += cv.rect(118, 46, 42, 24, 3, "#9A6A3B") + cv.rect(118, 46, 42, 4, 2, "#C48B52")
        out += cv.rect(124, 36, 10, 10, 2, "#F77F72") + cv.rect(140, 38, 8, 8, 2, "#7CC3F0")
        out += P.person(cv, 52, 38, .18, "light", "black", "coral", "short") + P.person(cv, 80, 38, .18, "brown", "black", "sky", "bun")
        out += cv.ellipse(76, 64, 32, 7, "#B97B45") + cv.rect(73, 64, 6, 10, 2, "#8E5B2B") + cv.ellipse(76, 62, 30, 5.5, "#D79A5A")
    else:  # mid
        out += cv.rect(100, 8, 48, 36, 4, cv.lin("sb-sky", [(0, "#9EDCF7"), (1, "#E3F5FC")])) + cv.rect(100, 8, 48, 36, 4, "none", stroke="#8E5B2B", sw=2.5)
        out += P.person(cv, 14, 12, .46, "light", "black", "coral", "short") + P.person(cv, 92, 12, .46, "brown", "black", "sky", "bun", True)
        out += cv.rect(0, 66, FW, 24, 0, "#B97B45") + cv.rect(0, 66, FW, 4, 0, "#D79A5A")
        out += cv.ellipse(56, 70, 9, 3, "#fff") + cv.ellipse(108, 70, 9, 3, "#fff") + cv.rect(51, 62, 10, 8, 2, "#fff") + cv.rect(103, 62, 10, 8, 2, "#fff")
    if fade:
        out += cv.rect(0, 0, FW, FH, 0, cv.lin("sb-fade", [(0, "#0B1A20", .2), (1, "#0B1A20", .82)]))
    return out


def corners(cv, x, y, w, h, c="#FFFFFF"):
    out = ""
    for (px, py, dx, dy) in ((x + 7, y + 7, 1, 1), (x + w - 7, y + 7, -1, 1), (x + 7, y + h - 7, 1, -1), (x + w - 7, y + h - 7, -1, -1)):
        out += cv.path("M%s %s L%s %s L%s %s" % (_n(px + dx * 11), _n(py), _n(px), _n(py), _n(px), _n(py + dy * 11)), stroke=c, sw=2.4, op=.9)
    return out


@illustration("imedia-storyboard")
def _story():
    cv = Canvas(800, 500).backdrop()
    clip = cv._def("fclip", '<clipPath id="{id}"><rect width="%d" height="%d" rx="9"/></clipPath>' % (FW, FH))
    frames = [("Wide shot", "teal", "wide", False, "pan left", 4, "café chatter", "cut"),
              ("Mid shot", "sky", "mid", False, "static", 3, "dialogue", "cut"),
              ("Close-up", "coral", "close", False, "static", 2, "gasp", "cut"),
              ("Wide shot", "plum", "wide", True, "static", 3, "music swells", "fade out")]
    for i, (title, col, kind, fade, move, secs, sound, nxt) in enumerate(frames):
        x = 14 + i * 194
        cv.add(P.card(cv, x, 34, 180, 262, 20, title, col))
        fx, fy = x + 10, 62
        cv.add(cv.rect(fx - 2, fy + 2, FW + 4, FH + 4, 11, "#10303A", op=.18))
        cv.add(cv.group(frame_art(cv, kind, fade), fx, fy, extra=' clip-path="%s"' % clip))
        cv.add(cv.rect(fx, fy, FW, FH, 9, "none", stroke="#FFFFFF", sw=3), corners(cv, fx, fy, FW, FH))
        if i == 0:
            cv.add(P.pill(cv, fx + 80, fy + 76, "pan left", "paper", 11, 8, 18, 800))
        for r, (lab, val) in enumerate((("Move", move), ("Time", "%d s" % secs), ("Sound", sound), ("Next", nxt))):
            yy = 190 + r * 26
            cv.add(cv.rect(x + 10, yy - 16, 160, 22, 7, "var(--il-band)"))
            cv.add(cv.text(x + 18, yy, lab, 12, 700, anchor="start", cls="il-ink2"), cv.text(x + 70, yy, val, 13, 800, anchor="start", cls="il-ink"))
    # the same four frames along a clock
    cv.add(P.pill(cv, 52, 324, "time", "paper", 13, 12, 24, 800))
    cv.add(P.arrow(cv, [(92, 324), (770, 324)], PAL["ink"][1], 3, 10, op=.55))
    scale = 740 / 12.0
    x = 30
    marks = [(30, "0 s")]
    for i, (title, col, kind, fade, move, secs, sound, nxt) in enumerate(frames):
        w = secs * scale
        cv.add(P.lift(cv, x + 1.5, 342, w - 3, 34, col, 9, 5, hl=False))
        short = {"Wide shot": "wide", "Mid shot": "mid", "Close-up": "close-up"}[title]
        cv.add(cv.text(x + w / 2, 364, "%d · %s · %d s" % (i + 1, short, secs), 13, 800, fill=P._on(col)))
        # the sound track under it
        cv.add(P.lift(cv, x + 1.5, 436, w - 3, 30, col, 9, 4, hl=False))
        wave = "M%s 451 q4 -9 8 0 t8 0 t8 0" % _n(x + 12)
        cv.add(cv.path(wave, stroke=P._on(col), sw=2, op=.8), cv.text(x + 46, 456, sound, 12.5, 750, anchor="start", fill=P._on(col)))
        x += w
        marks.append((x, "%d s" % round(x / scale - 30 / scale)))
    for mx, t in marks:
        cv.add(cv.line(mx, 380, mx, 392, PAL["ink"][1], 2, op=.55), cv.text(mx if mx not in (30, 770) else mx + (8 if mx == 30 else -8), 410, t, 12.5, 750, cls="il-ink2", mono=True))
    cv.add(cv.text(30, 428, "sound track", 12, 700, anchor="start", cls="il-ink2"))
    cv.add(P.badge(cv, 30, 36, 1), P.badge(cv, 224, 36, 2), P.badge(cv, 418, 36, 3), P.badge(cv, 612, 36, 4), P.badge(cv, 102, 296, 5))
    return figure(
        "imedia-storyboard", cv, "A storyboard runs along time",
        "A storyboard laid out along the axis it actually uses, which is time. Four frames stand in order. Frame one is a wide shot with a "
        "pan to the left, held for four seconds, to the sound of café chatter, and it establishes where the scene is. Frame two is a mid shot, "
        "static, three seconds, where the dialogue begins. Frame three is a close up, static, two seconds, holding the reaction. Frame four "
        "returns to a wide shot, held for three seconds as the music swells, and fades out to end the sequence. Each frame carries the same set "
        "of annotations: the shot type, the camera movement, the duration, the sound and the transition into the next frame. Underneath, the "
        "same four frames are laid along a clock, twelve seconds in all, with the sound track below them. This is what separates a storyboard "
        "from a visualisation diagram: a storyboard describes a sequence over time, while a visualisation diagram describes a single static "
        "surface.",
        ["Frame 1, a wide shot: it establishes where we are.",
         "Frame 2, a mid shot: we move in, and the dialogue starts.",
         "Frame 3, a close up: the reaction, held for two seconds.",
         "Frame 4, a wide shot again, fading out to end the sequence.",
         "Each frame carries its shot type, its movement, its duration and its sound."],
        "Moving image gets a storyboard. A poster gets a visualisation diagram. The axis is the difference.")


# ----------------------------------------------------------------- phases

def calendar(cv, cx, cy, s=1.0):
    body = cv.shadow(0, 30, 24, 3, .18) + cv.rect(-22, -24, 44, 50, 6, "#FFFFFF", stroke="#DCE6EC", sw=1.2)
    body += cv.rect(-22, -24, 44, 14, 6, cv.g("red")) + cv.rect(-22, -17, 44, 7, 0, PAL["red"][1])
    for r in range(3):
        for c in range(4):
            body += cv.rect(-16 + c * 10, -4 + r * 9, 6, 5, 1.5, "#FFC933" if (r, c) == (1, 2) else "#C5D1D9")
    return cv.group(body, cx, cy, s)


def camera(cv, cx, cy, s=1.0):
    body = cv.shadow(0, 38, 30, 4, .2)
    for dx in (-16, 0, 16):
        body += cv.line(dx * .3, 12, dx * 1.9, 36, "#4A5A64", 3)
    body += cv.rect(-26, -20, 46, 30, 7, cv.g("dark", "deep")) + cv.rect(16, -14, 16, 18, 4, "#202C34")
    body += cv.circle(34, -5, 8, "#1A242B") + cv.circle(34, -5, 4, "#4FA3D9") + cv.circle(-16, -12, 3, "#FF5A4F")
    body += cv.rect(-20, -34, 22, 14, 6, cv.g("dark")) + cv.circle(-9, -27, 4, "#202C34") + cv.circle(-18, -27, 4, "#202C34")
    return cv.group(body, cx, cy, s)


def boom_mic(cv, cx, cy, s=1.0):
    body = cv.shadow(0, 36, 22, 3, .16)
    body += cv.line(-26, 30, 18, -22, "#4A5A64", 4)
    body += cv.rect(8, -34, 22, 30, 11, cv.g("slate", "deep"))
    for k in range(4):
        body += cv.line(11, -28 + k * 7, 27, -28 + k * 7, "#5B6D79", 1.6, op=.7)
    body += cv.rect(-34, 26, 18, 8, 3, "#2A3E49")
    return cv.group(body, cx, cy, s)


def mixer(cv, cx, cy, s=1.0):
    body = cv.shadow(0, 30, 28, 3, .16) + cv.rect(-30, -24, 60, 52, 8, cv.g("dark", "deep"))
    for i, h in enumerate((-10, 4, -2, 10)):
        x = -22 + i * 14.5
        body += cv.rect(x, -16, 4, 36, 2, "#0E171C") + cv.rect(x - 4, h - 3, 12, 7, 2, cv.g("coral"))
    return cv.group(body, cx, cy, s)


def colour_wheel(cv, cx, cy, r=24):
    cols = ["#F0584B", "#FFA23C", "#FFD93D", "#5BD58B", "#4FA3D9", "#A06BD5"]
    out = cv.circle(cx, cy + 3, r + 2, "#10303A", op=.16)
    for i, c in enumerate(cols):
        a0, a1 = math.radians(i * 60 - 90), math.radians(i * 60 - 30)
        out += cv.path("M%s %s L%s %s A%s %s 0 0 1 %s %s Z" % (_n(cx), _n(cy), _n(cx + r * math.cos(a0)), _n(cy + r * math.sin(a0)), _n(r), _n(r),
                                                                _n(cx + r * math.cos(a1)), _n(cy + r * math.sin(a1))), fill=c)
    return out + cv.circle(cx, cy, r * .36, "#FFFFFF") + cv.circle(cx, cy, r + 1, "none", stroke="#FFFFFF", sw=2.5)


def room(cv, x, y, w, h):
    out = cv.rect(x, y, w, h, 12, cv.lin("room", [(0, "#FFFDF7"), (1, "#F4ECD9")]))
    d = "M%s %s L%s %s L%s %s Q%s %s %s %s L%s %s Q%s %s %s %s Z" % (_n(x), _n(y + h - 18), _n(x + w), _n(y + h - 18), _n(x + w), _n(y + h - 12), _n(x + w), _n(y + h),
                                                                        _n(x + w - 12), _n(y + h), _n(x + 12), _n(y + h), _n(x), _n(y + h), _n(x), _n(y + h - 12))
    return out + cv.path(d, fill="#DDB27A") + cv.rect(x, y + h - 18, w, 2.5, 0, "#B98A4E", op=.55)


def tag(cv, cx, y, label):
    return P.pill(cv, cx, y, label, "paper", 11.5, 7, 19, 750)


@illustration("imedia-phases")
def _phases():
    cv = Canvas(800, 500).backdrop()
    floors = [  # top to bottom
        (36, "plum", ("Post-", "production"), "finishes it"),
        (170, "coral", ("Production", ""), "makes it"),
        (304, "sky", ("Pre-", "production"), "plans it"),
    ]
    for y, col, (l1, l2), verb in floors:
        cv.add(P.lift(cv, 24, y, 512, 122, col, 16, 8))
        if l2:
            cv.add(cv.text(46, y + 56, l1, 17, 800, anchor="start", fill=P._on(col)), cv.text(46, y + 78, l2, 17, 800, anchor="start", fill=P._on(col)))
        else:
            cv.add(cv.text(46, y + 66, l1, 17, 800, anchor="start", fill=P._on(col)))
        cv.add(cv.text(46, y + 102, verb, 13, 650, anchor="start", fill=P._on(col)))
        cv.add(room(cv, 156, y + 10, 372, 102))
    # pre-production: the paperwork
    y = 304 + 10
    cv.add(P.doc(cv, 168, y + 12, .6, lines=3, head="sky"), tag(cv, 190, y + 90, "brief"))
    cv.add(P.magnifier(cv, 262, y + 32, .95, 16), P.doc(cv, 258, y + 18, .5, lines=2), tag(cv, 262, y + 90, "research"))
    cv.add(P.doc(cv, 316, y + 12, .6, lines=3, head="coral"), tag(cv, 338, y + 90, "shot list"))
    cv.add(calendar(cv, 410, y + 42, .85), tag(cv, 410, y + 90, "schedule"))
    cv.add(P.doc(cv, 468, y + 12, .6, lines=3, head="sun"), cv.circle(498, y + 56, 8, cv.g("red", "deep")), cv.circle(498, y + 56, 3.5, "#FFD9D5"), tag(cv, 490, y + 90, "licences"))
    # production: the shoot
    y = 170 + 10
    cv.add(camera(cv, 196, y + 36, .88), tag(cv, 196, y + 90, "filming"))
    cv.add(boom_mic(cv, 282, y + 34, .88), tag(cv, 282, y + 90, "recording"))
    cv.add(P.laptop(cv, 330, y + 22, .36), tag(cv, 368, y + 90, "designing"))
    cv.add(P.gear(cv, 450, y + 44, 24, "slate"), P.gear(cv, 478, y + 28, 14, "metal"), tag(cv, 462, y + 90, "building"))
    # post-production: the finish
    y = 36 + 10
    timeline = (cv.rect(0, 0, 200, 130, 0, "#17252D")
                + "".join(cv.rect(14 + a, 22 + r * 24, b, 16, 4, c) for r, (a, b, c) in enumerate(((0, 70, "#F77F72"), (50, 90, "#66B8EC"), (20, 120, "#62CFA3"))))
                + "".join(cv.rect(14 + a, 22 + r * 24, b, 16, 4, c) for r, (a, b, c) in enumerate(((84, 80, "#FFCC4A"), (146, 30, "#BA9ED9"), (150, 36, "#F77F72"))))
                + cv.rect(98, 12, 3, 100, 0, "#FFFFFF"))
    cv.add(P.monitor(cv, 166, y + 8, .34, timeline), tag(cv, 200, y + 90, "editing"))
    cv.add(mixer(cv, 282, y + 38, .92), tag(cv, 282, y + 90, "mixing"))
    cv.add(colour_wheel(cv, 364, y + 40, 25), tag(cv, 364, y + 90, "grading"))
    cv.add(P.lift(cv, 430, y + 18, 62, 44, "dark", 9, 5, hl=False), cv.poly([(452, y + 30), (452, y + 52), (472, y + 41)], "#7CF0B0"), tag(cv, 462, y + 90, "testing"))
    # what each floor hands up
    for yy, lab in ((297, "shot list"), (163, "footage")):
        w = len(lab) * 13 * .58 + 54
        cv.add(P.pill(cv, 340 + 10, yy, lab, "sun", 13, 24, 26, 800))
        cv.add(cv.poly([(340 + 10 - w / 2 + 12, yy + 5), (340 + 10 - w / 2 + 24, yy + 5), (340 + 10 - w / 2 + 18, yy - 6)], PAL["sun"][2]))
    # why the order cannot change
    cv.add(P.card(cv, 556, 34, 230, 448, 20, "Cost of change", "coral"))
    base = 372
    for i, (col, h, t, price) in enumerate((("sky", 44, "plan", "£"), ("coral", 118, "shoot", "££"), ("plum", 214, "edit", "£££"))):
        x = 586 + i * 66
        cv.add(cv.shadow(x + 24, base + 6, 28, 3, .2), P.lift(cv, x, base - h, 48, h, col, 10, 6, hl=h > 60))
        cv.add(cv.text(x + 24, base - h - 10, price, 18, 800, cls="il-ink"), cv.text(x + 24, base + 30, t, 14, 800, cls="il-ink"))
    for i, t in enumerate(("Skip the ground floor and", "the decisions arrive late,", "with more built on top.")):
        cv.add(cv.text(671, 432 + i * 18, t, 13, 700, cls="il-ink"))
    cv.add(P.badge(cv, 30, 308, 1), P.badge(cv, 30, 174, 2), P.badge(cv, 30, 40, 3), P.badge(cv, 262, 297, 4), P.badge(cv, 570, 36, 5))
    return figure(
        "imedia-phases", cv, "Pre-production, production, post-production",
        "The three phases of production drawn as three floors of a building. The bottom floor is pre-production, which plans the work: the "
        "brief, the research, the shot list, the schedule and the licences for anything borrowed. The middle floor is production, which makes "
        "it: filming, recording, designing and building. The top floor is post-production, which finishes it: editing, mixing, grading and "
        "testing before the export. Each floor hands something specific to the one above it, and those handovers are dependencies: "
        "pre-production hands production a shot list, and production hands post-production the footage. That is why the order cannot be "
        "rearranged. A bar chart on the right shows what happens when planning is skipped: the same change costs a little at the planning "
        "stage, more once it has been shot, and most of all in the edit, because every decision that should have been made early has to be "
        "made late with more already built on top of it.",
        ["Pre-production plans it: brief, research, documents, schedule, licences.",
         "Production makes it: filming, recording, designing, building.",
         "Post-production finishes it: editing, mixing, testing, export.",
         "Each floor hands something specific to the one above it.",
         "Skip the bottom floor and the decisions do not disappear: they arrive late."],
        "Each phase exists to hand the next one something. That is the whole reason for the order.")
