"""Pixel, the robot cat: one character, drawn once, used everywhere.

The logo and the mascot had drifted into two different cats with the same
idea. Both now come out of this module, off one set of coordinates, so the
face in the browser tab is the face in the corner of the screen is the face
asleep on the 404 page.

Two renderings:

  flat()    one <svg>, for the logo, the favicon and the small dock mascot.
            Depth comes from shading: a lit top left, a rim along the head
            and a contact shadow. Cheap enough for a 16px browser tab.

  stack()   the same cat cut into layers held apart on the Z axis inside a
            preserve-3d container. The container sways a few degrees and the
            layers move at different rates, so the ears and the headphones
            shift against the face: real parallax rather than a drawing of
            it. Used only where the cat is large and is the point of the
            screen, because it costs eight nodes instead of one.

Both read the same palette and the same geometry constants below, so the two
cannot drift apart again.
"""

# ------------------------------------------------------------------ palette
TEAL_LIT = "#7FCDD3"
TEAL = "#02848B"
TEAL_DARK = "#01646A"
VISOR_LIT = "#EFE4F4"
VISOR = "#C3A2D0"
PURPLE = "#6F6291"
PURPLE_LIT = "#8E7FAB"
LILAC_PALE = "#D7C4E2"
INK = "#2E2545"
CREAM = "#FBF4E2"
DEEP = "#024E52"

# ------------------------------------------------------------------ geometry
# One hundred unit square. Every part is positioned in these coordinates and
# the logo simply renders a crop of them, so the proportions are shared.
HEAD = dict(x=15, y=21, w=70, h=57, r=27)
EYE = dict(lx=36.5, rx_=63.5, cy=53, rx=9.4, ry=10.6)
EAR_L = "M22 32 L24 10 Q24.4 7.2 27.2 8.9 L41.5 19 Z"
EAR_L_IN = "M26.4 27.6 L27.8 16.4 L36 22 Z"
EAR_R = "M78 32 L76 10 Q75.6 7.2 72.8 8.9 L58.5 19 Z"
EAR_R_IN = "M73.6 27.6 L72.2 16.4 L64 22 Z"


# Which gradient each part actually needs. A layer that uses none emits no
# <defs> at all, which matters because the loader ships on every page and
# eight copies of four unused gradients is most of its weight.
NEEDS = {"tail": (), "body": ("Body",), "ears": (), "head": ("Head",),
         "visor": ("Visor",), "cans": (), "eyes": ("Eye",), "muzzle": ()}


# Each rendered cat needs its own gradient ids. The logo appears twice on
# every page, in the header and in the footer, so a fixed prefix declared
# id="clHead" twice per page: invalid HTML, and the second set unreachable.
_SEQ = [0]


def _uid(tag):
    _SEQ[0] += 1
    return "%s%d" % (tag, _SEQ[0])


def _defs(pfx, which=None):
    """Gradients that put a light source at the top left of the head."""
    if which is not None:
        picked = "".join(_GRAD[k] % _GRAD_ARGS[k](pfx) for k in which)
        return ('<defs>%s</defs>' % picked) if picked else ""
    return (
        '<defs>'
        '<linearGradient id="%sHead" x1="0.12" y1="0" x2="0.88" y2="1">'
        '<stop offset="0" stop-color="%s"/><stop offset="0.62" stop-color="%s"/>'
        '<stop offset="1" stop-color="%s"/></linearGradient>'
        '<linearGradient id="%sVisor" x1="0.1" y1="0" x2="0.9" y2="1">'
        '<stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>'
        '<linearGradient id="%sBody" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>'
        '<radialGradient id="%sEye" cx="0.34" cy="0.3" r="0.85">'
        '<stop offset="0" stop-color="#4A3E68"/><stop offset="1" stop-color="%s"/>'
        '</radialGradient>'
        '</defs>'
        % (pfx, TEAL_LIT, TEAL, TEAL_DARK, pfx, VISOR_LIT, VISOR,
           pfx, PURPLE_LIT, PURPLE, pfx, INK))


_GRAD = {
    "Head": '<linearGradient id="%sHead" x1="0.12" y1="0" x2="0.88" y2="1">'
            '<stop offset="0" stop-color="%s"/><stop offset="0.62" stop-color="%s"/>'
            '<stop offset="1" stop-color="%s"/></linearGradient>',
    "Visor": '<linearGradient id="%sVisor" x1="0.1" y1="0" x2="0.9" y2="1">'
             '<stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>',
    "Body": '<linearGradient id="%sBody" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0" stop-color="%s"/><stop offset="1" stop-color="%s"/></linearGradient>',
    "Eye": '<radialGradient id="%sEye" cx="0.34" cy="0.3" r="0.85">'
           '<stop offset="0" stop-color="#4A3E68"/><stop offset="1" stop-color="%s"/>'
           '</radialGradient>',
}
_GRAD_ARGS = {
    "Head": lambda p: (p, TEAL_LIT, TEAL, TEAL_DARK),
    "Visor": lambda p: (p, VISOR_LIT, VISOR),
    "Body": lambda p: (p, PURPLE_LIT, PURPLE),
    "Eye": lambda p: (p, INK),
}

# ------------------------------------------------------------------- pieces

def _ears(pfx):
    return ('<path d="%s" fill="%s"/><path d="%s" fill="%s"/>'
            '<path d="%s" fill="%s"/><path d="%s" fill="%s"/>'
            % (EAR_L, TEAL, EAR_L_IN, VISOR, EAR_R, TEAL, EAR_R_IN, VISOR))


def _head(pfx):
    h = HEAD
    return (
        '<rect x="%(x)s" y="%(y)s" width="%(w)s" height="%(h)s" rx="%(r)s" fill="url(#%(p)sHead)"/>'
        # a rim of light along the top edge, which is what makes it read as
        # a rounded solid rather than a flat rounded rectangle
        '<path d="M%(x)s 44 A%(r)s %(r)s 0 0 1 %(mx)s %(y)s h16 A%(r)s %(r)s 0 0 1 %(x2)s 44"'
        ' fill="none" stroke="#BFEAEC" stroke-width="2" stroke-linecap="round" opacity=".55"/>'
        % dict(h, p=pfx, mx=h["x"] + h["r"], x2=h["x"] + h["w"]))


def _visor(pfx):
    h = HEAD
    return ('<path d="M%s 38 A%s %s 0 0 1 %s %s h16 A%s %s 0 0 1 %s 38 Z" fill="url(#%sVisor)"/>'
            '<circle cx="50" cy="28" r="2.2" fill="%s" opacity=".5"/>'
            % (h["x"], h["r"], h["r"], h["x"] + h["r"], h["y"], h["r"], h["r"],
               h["x"] + h["w"], pfx, TEAL))


def _eyes(pfx, asleep=False):
    e = EYE
    if asleep:
        # Closed eyes are two downward curves. Lashes make the difference
        # between asleep and merely eyeless.
        return "".join(
            '<path d="M%s %s q6 7 12 0" fill="none" stroke="%s" stroke-width="3.1" '
            'stroke-linecap="round"/>' % (cx - 6, e["cy"], INK)
            for cx in (e["lx"], e["rx_"]))
    out = []
    for cx in (e["lx"], e["rx_"]):
        out.append('<ellipse class="cat-eye" cx="%s" cy="%s" rx="%s" ry="%s" fill="url(#%sEye)"/>'
                   % (cx, e["cy"], e["rx"], e["ry"], pfx))
        out.append('<ellipse cx="%s" cy="%s" rx="3.2" ry="3.6" fill="#FDFAF0"/>'
                   % (cx - 3.1, e["cy"] - 4))
        out.append('<ellipse cx="%s" cy="%s" rx="1.5" ry="1.7" fill="#FDFAF0" opacity=".6"/>'
                   % (cx + 2.9, e["cy"] + 4.4))
    return "".join(out)


def _muzzle(pfx, asleep=False):
    mouth = ('<path d="M50 67 v2.6 M50 69.6 q-3 2.4 -5.2 0 M50 69.6 q3 2.4 5.2 0"'
             if not asleep else
             '<path d="M50 67 v2.6 M46.4 70.4 q3.6 2.6 7.2 0"')
    return ('<path d="M50 67 l-3.2-2.8 h6.4 Z" fill="%s"/>'
            '%s fill="none" stroke="%s" stroke-width="2" stroke-linecap="round"/>'
            % (DEEP, mouth, DEEP))


def _cans(pfx):
    return ('<rect x="6" y="43" width="12" height="20" rx="6" fill="%s"/>'
            '<rect x="8.8" y="46.6" width="6.4" height="12.8" rx="3.2" fill="%s"/>'
            '<rect x="82" y="43" width="12" height="20" rx="6" fill="%s"/>'
            '<rect x="84.8" y="46.6" width="6.4" height="12.8" rx="3.2" fill="%s"/>'
            % (PURPLE, LILAC_PALE, PURPLE, LILAC_PALE))


def _body(pfx):
    return ('<ellipse cx="50" cy="88" rx="30" ry="4.5" fill="%s" opacity=".16"/>'
            '<path d="M27 86 q0-19 23-19 t23 19 z" fill="url(#%sBody)"/>'
            '<path d="M36 86 q0-10 14-10 t14 10 z" fill="%s"/>'
            % (DEEP, pfx, LILAC_PALE))


def _tail(pfx):
    return ('<g class="cat-tail"><path d="M71 81 q15 3 14-12 q-1-10-9-10" fill="none" '
            'stroke="%s" stroke-width="6.5" stroke-linecap="round"/>'
            '<circle cx="76" cy="59" r="3.6" fill="%s"/></g>' % (TEAL_LIT, VISOR))


# ----------------------------------------------------------------- renderers

def flat(label="Pixel the robot cat", head_only=False, plate=False, cls="cat"):
    """One flat SVG of the whole cat, or just the head for the logo."""
    pfx = _uid("cl" if head_only else "cf")
    parts = [_defs(pfx)]
    if plate:
        parts.append('<rect x="2" y="2" width="96" height="96" rx="23" fill="%s"/>' % CREAM)
    if not head_only:
        parts += [_tail(pfx), _body(pfx)]
    parts += [_ears(pfx), _cans(pfx), _head(pfx), _visor(pfx),
              _eyes(pfx), _muzzle(pfx)]
    box = "6 4 88 84" if head_only else "0 0 100 100"
    if head_only and plate:
        box = "0 0 100 100"
    return ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="%s" class="%s" role="img" '
            'aria-label="%s">%s</svg>' % (box, cls, label, "".join(parts)))


# Back to front, with how far each sits off the page. The gaps are what the
# parallax is made of: too little and it is flat, too much and he comes apart.
LAYERS = [
    ("tail", -34, _tail),
    ("body", -20, _body),
    ("ears", -10, _ears),
    ("head", 0, _head),
    ("visor", 7, _visor),
    ("cans", 13, _cans),
    ("eyes", 15, _eyes),
    ("muzzle", 19, _muzzle),
]


def stack(state="awake", size=240, label=None, zzz=False):
    """The cat as layers held apart in 3D, swaying so the depth is visible."""
    pfx = _uid("c3")
    asleep = state == "asleep"
    out = ['<div class="cat3d is-%s" style="--cat-size:%dpx" role="img" aria-label="%s">'
           % (state, size,
              label or ("Pixel the robot cat, asleep" if asleep
                        else "Pixel the robot cat"))]
    out.append('<div class="cat3d-world">')
    for name, z, fn in LAYERS:
        # Each layer is its own <svg>, so each needs its own gradient ids or
        # the last one defined wins for all of them.
        lp = pfx + name
        body = fn(lp, asleep) if name in ("eyes", "muzzle") else fn(lp)
        out.append('<svg class="cat3d-layer cat3d-%s" style="--z:%dpx" viewBox="0 0 100 100" '
                   'aria-hidden="true">%s%s</svg>'
                   % (name, z, _defs(lp, NEEDS[name]), body))
    out.append('</div>')
    if zzz:
        out.append('<div class="cat3d-zzz" aria-hidden="true">'
                   '<span>Z</span><span>Z</span><span>Z</span></div>')
    out.append('</div>')
    return "".join(out)


# ---------------------------------------------------------------------- rig
# The Computational Thinking Adventure needs a Pixel who can act: wave, think,
# dance and hold up a trophy. rig() is the flat cat cut into named groups that
# CSS can move, plus the extra pieces the poses need (arms in four positions,
# happy eyes, two more mouths, a trophy, sparkles) and the five accessories a
# student can unlock. Everything still comes from the coordinates above, so the
# adventure's Pixel is the same cat as the logo.

ARM = TEAL
PAW = TEAL_LIT
GOLD = "#F5B700"
GOLD_DEEP = "#C98A00"

# (pose, side) -> the arm as a bendy cable from the shoulder, and where its paw ends
_ARMS = {
    ("rest", "l"): ("M31 78 Q24 84 22 90", (22, 90)),
    ("rest", "r"): ("M69 78 Q76 84 78 90", (78, 90)),
    ("wave", "r"): ("M70 77 Q93 76 99 52", (99, 50)),
    ("cheer", "l"): ("M30 77 Q4 70 2 40", (2, 38)),
    ("cheer", "r"): ("M70 77 Q96 70 98 40", (98, 38)),
    ("scratch", "l"): ("M30 77 Q-2 68 9 36", (10, 34)),
    ("hold", "r"): ("M70 77 Q94 78 98 60", (98, 58)),
}


def _arm(pose, side):
    d, (px, py) = _ARMS[(pose, side)]
    return ('<g class="px-arm px-arm-%s px-arm-%s">'
            '<path d="%s" fill="none" stroke="%s" stroke-width="6.4" stroke-linecap="round"/>'
            '<circle cx="%s" cy="%s" r="6" fill="%s" stroke="%s" stroke-width="1.4"/>'
            '<circle cx="%s" cy="%s" r="2.3" fill="%s"/></g>'
            % (side, pose, d, ARM, px, py, PAW, TEAL_DARK, px, py + 1, VISOR))


def _happy_eyes():
    return "".join('<path d="M%s %s q8.5 -10 17 0" fill="none" stroke="%s" stroke-width="3.6" '
                   'stroke-linecap="round"/>' % (cx - 8.5, EYE["cy"] + 3, INK)
                   for cx in (EYE["lx"], EYE["rx_"]))


def _mouths():
    return (
        # the everyday smile, from _muzzle
        '<path class="px-m px-m-smile" d="M50 67 v2.6 M50 69.6 q-3 2.4 -5.2 0 M50 69.6 q3 2.4 5.2 0" '
        'fill="none" stroke="%s" stroke-width="2" stroke-linecap="round"/>'
        # an open grin for celebrating
        '<path class="px-m px-m-grin" d="M43.5 68 q6.5 9 13 0 z" fill="%s" stroke="%s" '
        'stroke-width="1.6" stroke-linejoin="round"/>'
        '<path class="px-m px-m-grin" d="M46.5 71.5 q3.5 3.2 7 0" fill="#F28AA0"/>'
        # a small o for thinking
        '<ellipse class="px-m px-m-o" cx="50" cy="70.5" rx="2.4" ry="2.8" fill="%s"/>'
        % (DEEP, DEEP, DEEP, DEEP))


def _trophy():
    # held up beside the head in the right paw
    return (
        '<g class="px-trophy">'
        '<path d="M92 26 h20 v6 q0 13 -10 15 q-10 -2 -10 -15 z" fill="%s" stroke="%s" stroke-width="1.4"/>'
        '<path d="M92 29 q-6 0 -5 6 q1 5 6 6 M112 29 q6 0 5 6 q-1 5 -6 6" fill="none" stroke="%s" stroke-width="2.2"/>'
        '<rect x="99.5" y="46" width="5" height="6" fill="%s"/>'
        '<rect x="95" y="51" width="14" height="5" rx="1.6" fill="%s"/>'
        '<path d="M97 30 q0 9 5 12" fill="none" stroke="#FFF6C9" stroke-width="2" stroke-linecap="round" opacity=".8"/>'
        '</g>' % (GOLD, GOLD_DEEP, GOLD_DEEP, GOLD_DEEP, GOLD_DEEP))


def _sparkle(x, y, s, cls):
    return ('<path class="%s" d="M%s %s q%s %s %s %s q%s %s %s %s q%s %s %s %s q%s %s %s %s z" fill="%s"/>'
            % (cls, x, y - s, s * .15, s * .85, s, s, -s * .85, s * .15, -s, s, -s * .15, -s * .85,
               -s, -s, s * .85, -s * .15, s, -s, GOLD))


def _accessories():
    return (
        # party hat
        '<g class="px-acc px-acc-party"><path d="M38 23 L52 -12 L64 21 Z" fill="#EC4899"/>'
        '<path d="M42.5 12 L60.5 10 M46.5 1 L57.5 0" stroke="#FDE047" stroke-width="3.2"/>'
        '<circle cx="52" cy="-13" r="4.2" fill="#FDE047"/></g>'
        # sunglasses
        '<g class="px-acc px-acc-shades"><rect x="25" y="45" width="23" height="15" rx="6" fill="#111827"/>'
        '<rect x="52" y="45" width="23" height="15" rx="6" fill="#111827"/>'
        '<path d="M48 50 h4" stroke="#111827" stroke-width="3"/>'
        '<path d="M29 48 l6 0" stroke="#fff" stroke-width="2" stroke-linecap="round" opacity=".7"/>'
        '<path d="M56 48 l6 0" stroke="#fff" stroke-width="2" stroke-linecap="round" opacity=".7"/></g>'
        # scarf
        '<g class="px-acc px-acc-scarf"><path d="M29 75 q21 9 42 0 v7 q-21 9 -42 0 z" fill="#DC2626"/>'
        '<path d="M36 78 v7 M44 80 v7 M52 80 v7 M60 79 v7" stroke="#fff" stroke-width="2.4" opacity=".85"/>'
        '<path d="M62 80 l4 16 l7 -3 l-3 -14 z" fill="#DC2626"/></g>'
        # wizard hat
        '<g class="px-acc px-acc-wizard"><path d="M30 24 q20 -6 40 0 l-6 -4 L52 -20 L36 20 z" fill="#5B21B6"/>'
        '<ellipse cx="50" cy="23" rx="26" ry="4.5" fill="#4C1D95"/>'
        '<path d="M49 0 l1.5 3.5 3.6 .4 -2.7 2.4 .8 3.6 -3.2 -1.8 -3.2 1.8 .8 -3.6 -2.7 -2.4 3.6 -.4 z" fill="#FDE047"/>'
        '<circle cx="58" cy="12" r="1.6" fill="#FDE047"/><circle cx="42" cy="15" r="1.3" fill="#FDE047"/></g>'
        # crown
        '<g class="px-acc px-acc-crown"><path d="M33 22 L35 4 L43 13 L50 0 L57 13 L65 4 L67 22 Z" fill="%s" '
        'stroke="%s" stroke-width="1.5" stroke-linejoin="round"/>'
        '<circle cx="50" cy="15" r="2.6" fill="#EF4444"/><circle cx="40" cy="17" r="2" fill="#3B82F6"/>'
        '<circle cx="60" cy="17" r="2" fill="#10B981"/></g>' % (GOLD, GOLD_DEEP))


def rig(label="Pixel the robot cat", cls="px"):
    """Pixel cut into named groups, with every pose's extra pieces, for CSS to animate."""
    pfx = _uid("px")
    h = HEAD
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="-14 -28 132 134" class="%s" role="img" aria-label="%s">' % (cls, label),
        _defs(pfx),
        '<ellipse class="px-shadow" cx="50" cy="91" rx="31" ry="4.6" fill="%s" opacity=".16"/>' % DEEP,
        '<g class="px-all">',
        _tail(pfx),
        '<path d="M27 86 q0-19 23-19 t23 19 z" fill="url(#%sBody)"/>' % pfx,
        '<path d="M36 86 q0-10 14-10 t14 10 z" fill="%s"/>' % LILAC_PALE,
        _arm("rest", "l"), _arm("cheer", "l"), _arm("scratch", "l"),
        '<g class="px-head">',
        _ears(pfx), _cans(pfx), _head(pfx), _visor(pfx),
        '<g class="px-eyes">%s</g>' % _eyes(pfx),
        '<g class="px-eyes-happy">%s</g>' % _happy_eyes(),
        '<path d="M50 67 l-3.2-2.8 h6.4 Z" fill="%s"/>' % DEEP,
        _mouths(),
        '</g>',
        _accessories(),
        _arm("rest", "r"), _arm("wave", "r"), _arm("cheer", "r"), _arm("hold", "r"),
        _trophy(),
        '</g>',
        '<g class="px-fx">',
        '<g class="px-q"><circle cx="92" cy="2" r="11" fill="#fff" stroke="%s" stroke-width="2"/>'
        '<text x="92" y="7.5" text-anchor="middle" font-size="15" font-weight="800" fill="%s" '
        'font-family="Poppins, sans-serif">?</text></g>' % (TEAL, TEAL),
        _sparkle(4, 4, 5, "px-spark px-spark-1"), _sparkle(100, 18, 4, "px-spark px-spark-2"),
        _sparkle(-4, 56, 3.5, "px-spark px-spark-3"),
        '</g>',
        '</svg>',
    ]
    return "".join(parts)
