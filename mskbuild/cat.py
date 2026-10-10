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
    pfx = "cl" if head_only else "cf"
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
    pfx = "c3"
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
