"""Small helpers for building the site's inline SVG diagrams.

Every diagram is plain inline SVG with no external dependency. Colours are
written as CSS custom properties so the diagram re-themes automatically when
the page switches between light and dark, and text inherits the page font.
"""
import html


def esc(s):
    return html.escape(str(s), quote=True)


# --------------------------------------------------------------- primitives

def defs(extra=""):
    """Arrowhead markers, shared by every diagram."""
    return (
        '<defs>'
        '<marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" '
        'markerHeight="6" orient="auto-start-reverse">'
        '<path d="M0 0 L10 5 L0 10 z" fill="var(--dg-line)"/></marker>'
        '<marker id="ah-accent" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" '
        'markerHeight="6" orient="auto-start-reverse">'
        '<path d="M0 0 L10 5 L0 10 z" fill="var(--dg-accent)"/></marker>'
        '<marker id="ah-alt" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="6" '
        'markerHeight="6" orient="auto-start-reverse">'
        '<path d="M0 0 L10 5 L0 10 z" fill="var(--dg-alt)"/></marker>'
        + extra + '</defs>')


def text(x, y, s, size=13, weight=500, anchor="middle", fill="var(--dg-text)",
         mono=False, cls=""):
    fam = ' class="dg-mono"' if mono else ""
    c = ' class="%s"' % cls if cls else ""
    return ('<text x="%s" y="%s" text-anchor="%s" font-size="%s" font-weight="%s" '
            'fill="%s"%s%s>%s</text>' % (x, y, anchor, size, weight, fill, fam, c, esc(s)))


def box(x, y, w, h, label=None, sub=None, fill="var(--dg-fill)",
        stroke="var(--dg-line)", r=8, label_size=13, sub_size=11, dash=None,
        text_fill="var(--dg-text)"):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    out = ['<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" '
           'stroke="%s" stroke-width="1.5"%s/>' % (x, y, w, h, r, fill, stroke, d)]
    cx = x + w / 2
    if label is not None and sub is not None:
        out.append(text(cx, y + h / 2 - 3, label, label_size, 620, fill=text_fill))
        out.append(text(cx, y + h / 2 + 14, sub, sub_size, 450, fill="var(--dg-muted)"))
    elif label is not None:
        out.append(text(cx, y + h / 2 + 4.5, label, label_size, 620, fill=text_fill))
    return "".join(out)


def line(x1, y1, x2, y2, stroke="var(--dg-line)", w=1.5, dash=None, arrow=False,
         marker="ah"):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    a = ' marker-end="url(#%s)"' % marker if arrow else ""
    return ('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke="%s" stroke-width="%s"%s%s/>'
            % (x1, y1, x2, y2, stroke, w, d, a))


def path(d, stroke="var(--dg-line)", w=1.5, fill="none", dash=None, arrow=False,
         marker="ah"):
    ds = ' stroke-dasharray="%s"' % dash if dash else ""
    a = ' marker-end="url(#%s)"' % marker if arrow else ""
    return ('<path d="%s" fill="%s" stroke="%s" stroke-width="%s" stroke-linecap="round" '
            'stroke-linejoin="round"%s%s/>' % (d, fill, stroke, w, ds, a))


def circle(cx, cy, r, fill="var(--dg-fill)", stroke="var(--dg-line)", w=1.5):
    return ('<circle cx="%s" cy="%s" r="%s" fill="%s" stroke="%s" stroke-width="%s"/>'
            % (cx, cy, r, fill, stroke, w))


def chip(x, y, label, fill="var(--dg-accent-soft)", stroke="var(--dg-accent)",
         text_fill="var(--dg-accent)", pad=9, size=11):
    """A small pill used for labelling a connection or a step."""
    w = len(str(label)) * size * 0.60 + pad * 2
    return (box(x - w / 2, y - 11, w, 22, None, fill=fill, stroke=stroke, r=11)
            + text(x, y + 4, label, size, 620, fill=text_fill))


# ------------------------------------------------------------------ wrapper

def figure(name, width, height, body, title, desc, caption=None, max_w=760):
    """Wrap diagram body in an accessible, responsive figure.

    `title` becomes the accessible name, `desc` the long description used by
    screen readers in place of the picture, so a non sighted reader receives the
    same information rather than being told only that an image exists.
    """
    tid, did = "dg-%s-t" % name, "dg-%s-d" % name
    cap = '<figcaption>%s</figcaption>' % esc(caption) if caption else ""
    return (
        '<figure class="diagram" style="--dg-max:%dpx">'
        '<svg viewBox="0 0 %s %s" role="img" aria-labelledby="%s" aria-describedby="%s" '
        'preserveAspectRatio="xMidYMid meet">'
        '<title id="%s">%s</title><desc id="%s">%s</desc>%s%s</svg>%s</figure>'
        % (max_w, width, height, tid, did, tid, esc(title), did, esc(desc),
           defs(), body, cap))
