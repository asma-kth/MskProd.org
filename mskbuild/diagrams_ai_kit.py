"""Drawing kit for the AI course diagrams: a vivid palette and 3D helpers.

The rest of the site draws in calm theme colours. The AI course asked for
vivid colour and depth, so its figures use saturated hues, gradients and
isometric or perspective 3D. The rules that keep them readable in both the
light and the dark theme:

  * a vivid colour is used as a fill only behind white text, and each fill
    colour here has at least 4.5:1 contrast with white;
  * the brightest hues (amber, lime, cyan) are used for strokes, points and
    surfaces, or behind dark text, never behind white text;
  * a tinted panel is the vivid colour at low opacity over the page, so it
    darkens in the dark theme with everything else, and its text uses the
    theme's own text colour.

Nothing here registers a diagram. The diagram modules import these helpers.
"""
import math

from .svg import box, text, line, path, circle

INK = "var(--dg-text)"
MUTED = "var(--dg-muted)"
FILL = "var(--dg-fill)"
FILL2 = "var(--dg-fill-2)"
LINE = "var(--dg-line)"

# Fills that carry white text (each at least 4.5:1 against white).
VIOLET = "#6D28D9"
PINK = "#BE185D"
BLUE = "#1D4ED8"
TEAL = "#0F766E"
GREEN = "#15803D"
RED = "#B91C1C"
ORANGE = "#C2410C"
INDIGO = "#4338CA"
# Bright hues for strokes, points and surfaces, or behind dark text.
AMBER = "#F59E0B"
LIME = "#84CC16"
CYAN = "#06B6D4"
ROSE = "#F43F5E"
SKY = "#38BDF8"
PURPLE = "#A855F7"
DARK = "#111827"
WHITE = "#FFFFFF"

SERIES = [VIOLET, PINK, BLUE, TEAL, ORANGE, GREEN, INDIGO, RED]
SLATE = "#475569"

# The same hues as theme-aware variables (static/css/site.css), for text and
# lines drawn straight onto the page: deep in the light theme, light in the
# dark theme, so they keep their contrast in both.
_THEMED = {VIOLET: "var(--ai-violet)", PINK: "var(--ai-pink)", BLUE: "var(--ai-blue)",
           TEAL: "var(--ai-teal)", GREEN: "var(--ai-green)", ORANGE: "var(--ai-orange)",
           RED: "var(--ai-red)", INDIGO: "var(--ai-indigo)", SLATE: "var(--ai-slate)"}


def tv(colour):
    """The theme-aware version of a palette colour, for text and lines."""
    return _THEMED.get(colour, colour)
BRIGHT = [PURPLE, ROSE, SKY, CYAN, AMBER, LIME]


# ------------------------------------------------------------- colour maps

_PLASMA = [(0.00, (13, 8, 135)), (0.25, (126, 3, 168)), (0.50, (204, 71, 120)),
           (0.75, (248, 149, 64)), (1.00, (240, 249, 33))]
_COOLWARM = [(0.0, (29, 78, 216)), (0.5, (243, 244, 246)), (1.0, (190, 24, 93))]


def _lerp_stops(stops, t):
    t = min(1.0, max(0.0, t))
    for (a, ca), (b, cb) in zip(stops, stops[1:]):
        if t <= b:
            u = (t - a) / (b - a) if b > a else 0
            return tuple(int(round(ca[i] + (cb[i] - ca[i]) * u)) for i in range(3))
    return stops[-1][1]


def plasma(t):
    """A vivid sequential colour, deep blue through purple and pink to yellow."""
    return "#%02X%02X%02X" % _lerp_stops(_PLASMA, t)


def diverging(t):
    """Blue for negative, near white for zero, magenta for positive (t in -1..1)."""
    return "#%02X%02X%02X" % _lerp_stops(_COOLWARM, (t + 1) / 2.0)


def ink_on(hex_colour):
    """White or near black, whichever reads better on the given fill."""
    r, g, b = (int(hex_colour[i:i + 2], 16) / 255.0 for i in (1, 3, 5))

    def lin(c):
        return c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4
    lum = 0.2126 * lin(r) + 0.7152 * lin(g) + 0.0722 * lin(b)
    return WHITE if (1.05 / (lum + 0.05)) >= 4.5 else DARK


# ------------------------------------------------------------------- panels

def solid(x, y, w, h, colour, label=None, sub=None, r=10, size=12, sub_size=10):
    """A vivid filled box with white (or dark) text chosen for contrast."""
    ink = ink_on(colour)
    out = ['<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s"/>'
           % (x, y, w, h, r, colour)]
    if label is not None and sub is not None:
        out.append(text(x + w / 2.0, y + h / 2.0 - 3, label, size, 750, fill=ink))
        out.append(text(x + w / 2.0, y + h / 2.0 + 13, sub, sub_size, 500, fill=ink))
    elif label is not None:
        out.append(text(x + w / 2.0, y + h / 2.0 + size * 0.35, label, size, 750,
                        fill=ink))
    return "".join(out)


def tint(x, y, w, h, colour, label=None, sub=None, r=10, size=12, sub_size=10,
         op=0.14, dash=None):
    """A box tinted with a vivid colour, outlined in it, with theme text."""
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    out = ['<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" '
           'fill-opacity="%s" stroke="%s" stroke-width="1.6"%s/>'
           % (x, y, w, h, r, colour, op, tv(colour), d)]
    if label is not None and sub is not None:
        out.append(text(x + w / 2.0, y + h / 2.0 - 3, label, size, 750, fill=INK))
        out.append(text(x + w / 2.0, y + h / 2.0 + 13, sub, sub_size, 500,
                        fill=MUTED))
    elif label is not None:
        out.append(text(x + w / 2.0, y + h / 2.0 + size * 0.35, label, size, 700,
                        fill=INK))
    return "".join(out)


def grad(gid, stops, x2=1, y2=0):
    """A linear gradient definition. `stops` is a list of (offset, colour)."""
    s = "".join('<stop offset="%s" stop-color="%s"/>' % (o, c) for o, c in stops)
    return ('<defs><linearGradient id="%s" x1="0" y1="0" x2="%s" y2="%s">%s'
            '</linearGradient></defs>' % (gid, x2, y2, s))


def glow(gid, colour, std=4):
    """A soft glow filter for points that should look lit."""
    return ('<defs><filter id="%s" x="-50%%" y="-50%%" width="200%%" height="200%%">'
            '<feGaussianBlur stdDeviation="%s" result="b"/><feFlood flood-color="%s" '
            'flood-opacity="0.65"/><feComposite in2="b" operator="in"/><feMerge>'
            '<feMergeNode/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>'
            % (gid, std, colour))


# ----------------------------------------------------------------- neurons

def neuron(cx, cy, r, colour, label="", size=11):
    """A node: a vivid disc with a lighter rim and an optional label inside."""
    ink = ink_on(colour) if colour.startswith("#") else INK
    out = [circle(cx, cy, r, fill=colour, stroke=FILL, w=2)]
    if label:
        out.append(text(cx, cy + size * 0.36, label, size, 750, fill=ink))
    return "".join(out)


def mlp(layers, x0, x1, y0, y1, colours, weights=None, r=13, labels=None,
        edge_op=0.55, edge_w=None):
    """A fully connected network drawn left to right.

    `layers` is the number of nodes per layer. Edges are drawn first and
    coloured by the sign of `weights[l][i][j]` when given (magenta for
    positive, blue for negative, width by size), otherwise neutral.
    """
    xs = [x0 + (x1 - x0) * i / float(max(1, len(layers) - 1)) for i in range(len(layers))]
    pos = []
    for li, n in enumerate(layers):
        gap = (y1 - y0) / float(n + 1)
        pos.append([(xs[li], y0 + gap * (k + 1)) for k in range(n)])
    out = []
    for li in range(len(layers) - 1):
        for i, (ax, ay) in enumerate(pos[li]):
            for j, (bx, by) in enumerate(pos[li + 1]):
                if weights:
                    wv = weights[li][i][j]
                    col = PINK if wv >= 0 else BLUE
                    wd = edge_w or (0.8 + min(3.5, abs(wv) * 1.6))
                else:
                    col, wd = LINE, edge_w or 1.2
                out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
                           'stroke-width="%.2f" stroke-opacity="%s"/>'
                           % (ax, ay, bx, by, col, wd, edge_op))
    for li, layer in enumerate(pos):
        for k, (x, y) in enumerate(layer):
            lab = labels[li][k] if labels and labels[li] else ""
            out.append(neuron(x, y, r, colours[li % len(colours)], lab, 10))
    return "".join(out), pos


def heat(x, y, values, cell, colour_fn, fmt="%.1f", size=10, gap=2, lo=None,
         hi=None):
    """A grid of coloured cells, each showing its value."""
    flat = [v for row in values for v in row]
    lo = min(flat) if lo is None else lo
    hi = max(flat) if hi is None else hi
    out = []
    for i, row in enumerate(values):
        for j, v in enumerate(row):
            t = (v - lo) / float(hi - lo) if hi > lo else 0.5
            col = colour_fn(t)
            cx, cy = x + j * (cell + gap), y + i * (cell + gap)
            out.append('<rect x="%.1f" y="%.1f" width="%s" height="%s" rx="3" fill="%s"/>'
                       % (cx, cy, cell, cell, col))
            if fmt:
                out.append(text(cx + cell / 2.0, cy + cell / 2.0 + size * 0.36,
                                fmt % v, size, 650, fill=ink_on(col)))
    return "".join(out)


# ---------------------------------------------------------------------- 3D

def cube(x, y, w, h, d, colour, label=None, ink=None, size=11, op=1.0):
    """An isometric box whose front face has its top left corner at (x, y).

    `d` is the depth drawn up and to the right. The top and side faces are
    the same hue, lighter and darker, which is what reads as solid.
    """
    dx, dy = d * 0.7, -d * 0.45
    r, g, b = (int(colour[i:i + 2], 16) for i in (1, 3, 5))

    def shade(f):
        return "#%02X%02X%02X" % tuple(int(max(0, min(255, c * f + (255 * (f - 1) if f > 1 else 0))))
                                       for c in (r, g, b))
    top = shade(1.25)
    side = shade(0.72)
    out = ['<g opacity="%s">' % op,
           '<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="%s"/>'
           % (x, y, x + dx, y + dy, x + w + dx, y + dy, x + w, y, top),
           '<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="%s"/>'
           % (x + w, y, x + w + dx, y + dy, x + w + dx, y + h + dy, x + w, y + h, side),
           '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s"/>'
           % (x, y, w, h, colour),
           '</g>']
    if label:
        out.append(text(x + w / 2.0, y + h / 2.0 + size * 0.36, label, size, 750,
                        fill=ink or ink_on(colour)))
    return "".join(out)


def project(x, y, z, yaw, pitch, scale, ox, oy):
    """Rotate a point about the vertical axis, tilt it, and project it."""
    cy, sy = math.cos(yaw), math.sin(yaw)
    cp, sp = math.cos(pitch), math.sin(pitch)
    x1 = x * cy - y * sy
    y1 = x * sy + y * cy
    # tilt: depth is y1, height is z
    y2 = y1 * cp - z * sp
    z2 = y1 * sp + z * cp
    return ox + x1 * scale, oy - z2 * scale, y2


def surface(f, xr, yr, n, yaw, pitch, scale, ox, oy, zscale=1.0, zr=None,
            colour_fn=plasma, stroke_op=0.35):
    """A 3D surface z = f(x, y), as shaded quadrilaterals drawn back to front.

    Returns the SVG and a projector for overlaying points on the surface.
    """
    xs = [xr[0] + (xr[1] - xr[0]) * i / float(n) for i in range(n + 1)]
    ys = [yr[0] + (yr[1] - yr[0]) * j / float(n) for j in range(n + 1)]
    zs = [[f(x, y) for x in xs] for y in ys]
    flat = [z for row in zs for z in row]
    zlo, zhi = (min(flat), max(flat)) if zr is None else zr
    span = (zhi - zlo) or 1.0
    xm, ym = (xr[0] + xr[1]) / 2.0, (yr[0] + yr[1]) / 2.0
    xs_norm = max(xr[1] - xr[0], yr[1] - yr[0]) / 2.0

    def to3(x, y, z):
        return ((x - xm) / xs_norm, (y - ym) / xs_norm, (z - zlo) / span * zscale)

    def proj(x, y, z):
        px, py, depth = project(*to3(x, y, z), yaw=yaw, pitch=pitch, scale=scale,
                                ox=ox, oy=oy)
        return px, py, depth

    quads = []
    for j in range(n):
        for i in range(n):
            corners = [(xs[i], ys[j], zs[j][i]), (xs[i + 1], ys[j], zs[j][i + 1]),
                       (xs[i + 1], ys[j + 1], zs[j + 1][i + 1]), (xs[i], ys[j + 1], zs[j + 1][i])]
            pts = [proj(*c) for c in corners]
            depth = sum(p[2] for p in pts) / 4.0
            zavg = sum(c[2] for c in corners) / 4.0
            quads.append((depth, pts, (zavg - zlo) / span))
    quads.sort(key=lambda q: -q[0])
    out = []
    for _, pts, t in quads:
        col = colour_fn(t)
        out.append('<polygon points="%s" fill="%s" stroke="#FFFFFF" '
                   'stroke-opacity="%s" stroke-width="0.6"/>'
                   % (" ".join("%.1f,%.1f" % (p[0], p[1]) for p in pts), col, stroke_op))
    return "".join(out), proj


def arrow(x1, y1, x2, y2, colour=LINE, w=1.8, dash=None):
    """A straight arrow in any colour (the shared markers are fixed colours)."""
    ang = math.atan2(y2 - y1, x2 - x1)
    hx, hy = x2 - 9 * math.cos(ang), y2 - 9 * math.sin(ang)
    left = (hx + 4.5 * math.sin(ang), hy - 4.5 * math.cos(ang))
    right = (hx - 4.5 * math.sin(ang), hy + 4.5 * math.cos(ang))
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    return ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s/>'
            '<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="%s"/>'
            % (x1, y1, hx, hy, colour, w, d, x2, y2, left[0], left[1], right[0],
               right[1], colour))
