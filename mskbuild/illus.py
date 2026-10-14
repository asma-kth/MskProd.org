"""Illustrations: drawn scenes for topics that are easier to see than to read.

Each one is a single inline SVG, drawn in code in one consistent style: soft
gradients, a darker lip under every shape so it looks raised off the page, a
gentle shadow, and the site's own colours. Nothing is loaded from anywhere, so
an illustration costs a few kilobytes of markup and works with scripts off.

A picture never carries the explanation alone. Under it sits a numbered list that
matches the numbered badges drawn into the picture, the caption says what to
take away, and the SVG itself holds a full text description for a screen reader.

The panel behind every picture follows the page theme (light or dark). The
objects keep their own colours in both, because a laptop is the same laptop in
either theme.
"""
import itertools

from .svg import esc

REGISTRY = {}
_SEQ = itertools.count(1)


def illustration(name):
    def wrap(fn):
        REGISTRY[name] = fn
        return fn
    return wrap


# Each colour is (light, base, dark): the light end catches the top of a shape,
# the dark end is the lip underneath it and the shading on its far side.
PAL = {
    "teal":  ("#8EE1E5", "#25B3BB", "#0F7C84"),
    "deep":  ("#3C9DA1", "#14707A", "#07474E"),
    "mint":  ("#C9F3E0", "#62CFA3", "#2F9F77"),
    "lilac": ("#EEE2F8", "#BA9ED9", "#8061A9"),
    "plum":  ("#8B6BB8", "#6B4C9E", "#4A3376"),
    "coral": ("#FFC6BB", "#F77F72", "#C84B43"),
    "sun":   ("#FFF0AD", "#FFCC4A", "#DFA000"),
    "sky":   ("#C9EAFB", "#66B8EC", "#2F82C0"),
    "navy":  ("#6684AA", "#3B5779", "#243B58"),
    "slate": ("#F1F5F8", "#C3CFD8", "#8799A7"),
    "metal": ("#F7FAFB", "#CDD8DF", "#94A6B3"),
    "dark":  ("#5B6D79", "#36464F", "#202C34"),
    "wood":  ("#F7D6A6", "#DDA45F", "#AD7536"),
    "green": ("#A5E6B8", "#41B56D", "#248049"),
    "paper": ("#FFFFFF", "#FBF8F0", "#E6DFCD"),
    "pcb":   ("#6FD6A6", "#3BB57F", "#17754E"),
    "gold":  ("#FFEBA6", "#EABC3C", "#B98A12"),
    "red":   ("#D44A41", "#BA352D", "#8F2923"),
    "ink":   ("#4B6572", "#2A3E49", "#17252D"),
}

INK = "#1F3A44"


def _n(v):
    s = "%.1f" % v
    return s[:-2] if s.endswith(".0") else s


class Canvas:
    """One illustration being drawn."""

    def __init__(self, w=800, h=500):
        self.w, self.h = w, h
        self.id = "il%d" % next(_SEQ)
        self._defs = {}
        self.out = []

    # ------------------------------------------------------------ plumbing
    def add(self, *parts):
        self.out.extend(parts)
        return self

    def ref(self, key):
        return "url(#%s-%s)" % (self.id, key)

    def _def(self, key, xml):
        if key not in self._defs:
            self._defs[key] = xml.replace("{id}", "%s-%s" % (self.id, key))
        return self.ref(key)

    def lin(self, key, stops, x1=0, y1=0, x2=0, y2=1):
        """A linear gradient. stops are (offset, colour) or (offset, colour, opacity)."""
        st = "".join('<stop offset="%s" stop-color="%s"%s/>'
                     % (_n(s[0] * 100) + "%", s[1],
                        ' stop-opacity="%s"' % s[2] if len(s) > 2 else "") for s in stops)
        return self._def(key, '<linearGradient id="{id}" x1="%s" y1="%s" x2="%s" y2="%s">%s</linearGradient>'
                         % (x1, y1, x2, y2, st))

    def rad(self, key, stops, cx=.5, cy=.5, r=.5, fx=None, fy=None):
        st = "".join('<stop offset="%s" stop-color="%s"%s/>'
                     % (_n(s[0] * 100) + "%", s[1],
                        ' stop-opacity="%s"' % s[2] if len(s) > 2 else "") for s in stops)
        f = ' fx="%s" fy="%s"' % (fx, fy) if fx is not None else ""
        return self._def(key, '<radialGradient id="{id}" cx="%s" cy="%s" r="%s"%s>%s</radialGradient>'
                         % (cx, cy, r, f, st))

    def g(self, name, mode="soft"):
        """A gradient from the palette. soft: light on top. deep: base to dark."""
        lo, base, hi = PAL[name]
        if mode == "soft":
            return self.lin("%s-soft" % name, [(0, lo), (1, base)])
        if mode == "deep":
            return self.lin("%s-deep" % name, [(0, base), (1, hi)])
        if mode == "round":      # a cylinder lit from the left
            return self.lin("%s-round" % name, [(0, hi), (.3, lo), (.7, base), (1, hi)], 0, 0, 1, 0)
        if mode == "side":
            return self.lin("%s-side" % name, [(0, lo), (1, base)], 0, 0, 1, 0)
        raise KeyError(mode)

    def c(self, name, i=1):
        return PAL[name][i]

    # -------------------------------------------------------- primitives
    def rect(self, x, y, w, h, r=0, fill="#fff", stroke=None, sw=1.5, op=None, extra="", dash=None):
        s = ' stroke="%s" stroke-width="%s"' % (stroke, sw) if stroke else ""
        o = ' opacity="%s"' % op if op is not None else ""
        d = ' stroke-dasharray="%s"' % dash if dash else ""
        return ('<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s"%s%s%s%s/>'
                % (_n(x), _n(y), _n(w), _n(h), _n(r), fill, s, d, o, extra))

    def circle(self, cx, cy, r, fill="#fff", stroke=None, sw=1.5, op=None, dash=None):
        s = ' stroke="%s" stroke-width="%s"' % (stroke, sw) if stroke else ""
        o = ' opacity="%s"' % op if op is not None else ""
        d = ' stroke-dasharray="%s"' % dash if dash else ""
        return '<circle cx="%s" cy="%s" r="%s" fill="%s"%s%s%s/>' % (_n(cx), _n(cy), _n(r), fill, s, d, o)

    def ellipse(self, cx, cy, rx, ry, fill="#fff", stroke=None, sw=1.5, op=None, dash=None):
        s = ' stroke="%s" stroke-width="%s"' % (stroke, sw) if stroke else ""
        o = ' opacity="%s"' % op if op is not None else ""
        d = ' stroke-dasharray="%s"' % dash if dash else ""
        return ('<ellipse cx="%s" cy="%s" rx="%s" ry="%s" fill="%s"%s%s%s/>'
                % (_n(cx), _n(cy), _n(rx), _n(ry), fill, s, d, o))

    def path(self, d, fill="none", stroke=None, sw=2, cap="round", op=None, dash=None, extra=""):
        s = (' stroke="%s" stroke-width="%s" stroke-linecap="%s" stroke-linejoin="round"'
             % (stroke, sw, cap)) if stroke else ""
        o = ' opacity="%s"' % op if op is not None else ""
        dd = ' stroke-dasharray="%s"' % dash if dash else ""
        return '<path d="%s" fill="%s"%s%s%s%s/>' % (d, fill, s, o, dd, extra)

    def poly(self, pts, fill="#fff", stroke=None, sw=1.5, op=None):
        d = "M" + " L".join("%s %s" % (_n(x), _n(y)) for x, y in pts) + " Z"
        return self.path(d, fill=fill, stroke=stroke, sw=sw, op=op)

    def line(self, x1, y1, x2, y2, stroke=INK, sw=2, op=None, dash=None, cap="round"):
        o = ' opacity="%s"' % op if op is not None else ""
        dd = ' stroke-dasharray="%s"' % dash if dash else ""
        return ('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s" '
                'stroke-linecap="%s"%s%s/>' % (_n(x1), _n(y1), _n(x2), _n(y2), stroke, sw, cap, o, dd))

    def text(self, x, y, s, size=17, weight=650, fill=None, anchor="middle", cls="il-ink",
             mono=False, op=None, spacing=None):
        f = ' fill="%s"' % fill if fill else ""
        c = cls if not fill else ""
        if mono:
            c = (c + " il-m").strip()
        o = ' opacity="%s"' % op if op is not None else ""
        ls = ' letter-spacing="%s"' % spacing if spacing else ""
        return ('<text x="%s" y="%s" text-anchor="%s" font-size="%s" font-weight="%s"%s%s%s%s>%s</text>'
                % (_n(x), _n(y), anchor, size, weight, f, (' class="%s"' % c) if c else "", o, ls, esc(s)))

    def group(self, body, x=0, y=0, s=1.0, rot=0, extra=""):
        t = "translate(%s %s)" % (_n(x), _n(y))
        if rot:
            t += " rotate(%s)" % _n(rot)
        if s != 1:
            t += " scale(%s)" % s
        return '<g transform="%s"%s>%s</g>' % (t, extra, body)

    # ---------------------------------------------------------- the panel
    def backdrop(self, tint="teal"):
        bg = self.lin("bg", [(0, "var(--il-bg1)"), (1, "var(--il-bg2)")], 0, 0, 1, 1)
        # the stops above are CSS variables, which gradients take through style
        self._defs["bg"] = self._defs["bg"].replace('stop-color="var(--il-bg1)"', 'style="stop-color:var(--il-bg1)"') \
                                           .replace('stop-color="var(--il-bg2)"', 'style="stop-color:var(--il-bg2)"')
        dots = self._def("dots", '<pattern id="{id}" width="26" height="26" patternUnits="userSpaceOnUse">'
                                 '<circle cx="3" cy="3" r="1.4" style="fill:var(--il-dot)"/></pattern>')
        a, b = ("var(--il-blob1)", "var(--il-blob2)") if tint == "teal" else ("var(--il-blob2)", "var(--il-blob1)")
        self.out.insert(0,
            self.rect(0, 0, self.w, self.h, 0, bg)
            + self.rect(0, 0, self.w, self.h, 0, dots)
            + self.circle(self.w * .86, self.h * .08, 150, a, op=1)
            + self.circle(self.w * .08, self.h * .98, 190, b, op=1))
        return self

    def shadow(self, cx, cy, rx, ry=None, o=.26):
        ry = ry if ry is not None else max(4, rx * .16)
        k = "shadow%d" % int(o * 100)
        fill = self.rad(k, [(0, "#10303A", o), (.6, "#10303A", o * .45), (1, "#10303A", 0)])
        return self.ellipse(cx, cy, rx, ry, fill)

    # ---------------------------------------------------------- the render
    def svg_body(self):
        return "<defs>%s</defs>%s" % ("".join(self._defs.values()), "".join(self.out))


# --------------------------------------------------------------- the figure

def figure(name, cv, title, desc, steps, caption=None, max_w=820):
    """Wrap a drawn canvas in its accessible figure, numbered list and caption."""
    tid, did = "il-%s-t" % name, "il-%s-d" % name
    li = "".join("<li>%s</li>" % esc(s) for s in steps)
    steps_html = ('<ol class="illus-steps" aria-label="What the numbers in the picture show">%s</ol>' % li) if steps else ""
    cap = '<figcaption>%s</figcaption>' % esc(caption) if caption else ""
    return (
        '<figure class="illus" style="--il-max:%dpx">'
        '<div class="illus-art"><svg viewBox="0 0 %d %d" role="img" aria-labelledby="%s" aria-describedby="%s">'
        '<title id="%s">%s</title><desc id="%s">%s</desc>%s</svg></div>'
        '<p class="illus-hint" aria-hidden="true">Swipe sideways to see the whole picture.</p>%s%s</figure>'
        % (max_w, cv.w, cv.h, tid, did, tid, esc(title), did, esc(desc), cv.svg_body(), steps_html, cap))
