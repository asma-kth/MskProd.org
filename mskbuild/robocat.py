"""The City Run cat: a white robot cat from a neon cyber city.

A white helmet with tall pointed ears that glow cyan inside, a dark visor
with two big glowing eyes, lights at the sides of its head, a glowing core
on its chest, a backpack, and a thin tail with a glowing tip. City Run
draws the same cat from behind as it runs (static/js/cityrun.js); this
module draws it from the front, for the start of a run, the results and
the small icons.

Two drawings share the palette:

  svg()   the whole cat, standing. The class on the <svg> picks its mood:
          is-happy closes its eyes in a smile and throws its arms out.
  head()  just the head, for small icons.

Every gradient id carries a prefix, so the cat can appear more than once on
a page; the game copies it with fresh ids for the same reason.
"""

WHITE = "#FFFFFF"
ARMOUR = "#EEF4FB"
ARMOUR_LO = "#C3D3E8"
STEEL = "#B9C9DE"
JOINT = "#2D4A86"
HAND = "#3B5BA5"
BOOT = "#2B3F75"
INK = "#1E2B4F"
VISOR_HI = "#1C2B5A"
VISOR = "#0B1533"
GLOW = "#22D3EE"
GLOW_HI = "#67E8F9"
GLOW_PALE = "#A5F3FC"
CORE_DEEP = "#0E7490"
NOSE = "#F9A8D4"
BLUSH = "#F472B6"

_SEQ = [0]


def _uid(prefix):
    _SEQ[0] += 1
    return "%s%d" % (prefix, _SEQ[0])


def _defs(u):
    return ('<defs>'
            '<linearGradient id="%(u)s-w" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0" stop-color="%(w)s"/><stop offset=".5" stop-color="%(a)s"/>'
            '<stop offset="1" stop-color="%(lo)s"/></linearGradient>'
            '<linearGradient id="%(u)s-v" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0" stop-color="%(vh)s"/><stop offset=".6" stop-color="%(v)s"/>'
            '<stop offset="1" stop-color="#070D24"/></linearGradient>'
            '</defs>' % dict(u=u, w=WHITE, a=ARMOUR, lo=ARMOUR_LO, vh=VISOR_HI, v=VISOR))


def _head(u):
    """The head in the whole cat's coordinates, centred on x = 110."""
    w = "url(#%s-w)" % u
    ear = ('<path d="M60 72 L56 16 Q58 8 66 13 L98 44 Z" fill="%(w)s" stroke="%(ink)s" stroke-width="2.4" '
           'stroke-linejoin="round"/><path d="M63.5 63 L61.5 26 L90 46 Z" fill="%(g)s" opacity=".35"/>'
           '<path d="M66.5 57 L65 32 L84 46 Z" fill="%(gh)s"/>' % dict(w=w, ink=INK, g=GLOW, gh=GLOW_HI))
    ears = ('<g class="rc-ear rc-ear-l">%s</g><g class="rc-ear rc-ear-r" transform="translate(220 0) scale(-1 1)">%s</g>'
            % (ear, ear))
    helmet = ('<path d="M44 100 C44 62 72 40 110 40 C148 40 176 62 176 100 C176 132 150 150 110 150 '
              'C70 150 44 132 44 100Z" fill="%s" stroke="%s" stroke-width="2.6"/>'
              '<ellipse cx="90" cy="58" rx="26" ry="9" transform="rotate(-12 90 58)" fill="#fff" opacity=".7"/>'
              '<path d="M98 52h24" stroke="%s" stroke-width="7" stroke-linecap="round" opacity=".3"/>'
              '<path d="M98 52h24" stroke="%s" stroke-width="3.2" stroke-linecap="round"/>'
              % (w, INK, GLOW, GLOW))
    lights = "".join('<circle cx="%d" cy="104" r="13" fill="%s" stroke="%s" stroke-width="2.2"/>'
                     '<circle cx="%d" cy="104" r="7.5" fill="%s"/>'
                     '<circle cx="%d" cy="104" r="7.5" fill="none" stroke="%s" stroke-width="2.4"/>'
                     % (x, STEEL, INK, x, INK, x, GLOW) for x in (46, 174))
    visor = ('<path d="M64 98 C64 76 84 66 110 66 C136 66 156 76 156 98 C156 122 138 136 110 136 '
             'C82 136 64 122 64 98Z" fill="url(#%s-v)" stroke="%s" stroke-width="2"/>'
             '<path d="M74 88 Q80 75 96 71" fill="none" stroke="#fff" stroke-width="4" stroke-linecap="round" opacity=".22"/>'
             % (u, INK))

    def eye(x):
        return ('<circle cx="%(x)g" cy="100" r="18" fill="%(g)s" opacity=".25"/>'
                '<circle cx="%(x)g" cy="100" r="13" fill="%(g)s"/>'
                '<circle cx="%(x)g" cy="100" r="8.5" fill="%(d)s"/>'
                '<circle cx="%(x1)g" cy="96" r="3.6" fill="#fff"/><circle cx="%(x2)g" cy="104" r="1.7" fill="#E0FBFF"/>'
                % dict(x=x, x1=x - 3.5, x2=x + 4, g=GLOW, d=CORE_DEEP))
    open_eyes = '<g class="rc-open">%s%s</g>' % (eye(90), eye(130))
    happy = ('<g class="rc-happy"><path d="M78 105 Q90 88 102 105M118 105 Q130 88 142 105" fill="none" stroke="%(g)s" '
             'stroke-width="11" stroke-linecap="round" opacity=".3"/><path d="M78 105 Q90 88 102 105M118 105 Q130 88 142 105" '
             'fill="none" stroke="%(gh)s" stroke-width="5.5" stroke-linecap="round"/>'
             '<ellipse cx="80" cy="119" rx="7" ry="3.5" fill="%(b)s" opacity=".55"/>'
             '<ellipse cx="140" cy="119" rx="7" ry="3.5" fill="%(b)s" opacity=".55"/></g>'
             % dict(g=GLOW, gh=GLOW_HI, b=BLUSH))
    face = ('<path d="M107 112.5h6l-3 3.2Z" fill="%s"/>'
            '<path d="M103 119q3.5 4 7 0q3.5 4 7 0" fill="none" stroke="%s" stroke-width="2.4" stroke-linecap="round"/>'
            % (NOSE, GLOW_PALE))
    return ('<g class="rc-head">%s%s%s%s%s%s%s</g>'
            % (ears, helmet, lights, visor, open_eyes, happy, face))


def svg(mood="idle", cls="rc", label=None, size=None):
    """The whole cat, standing, in a 220 by 250 box."""
    u = _uid("rc")
    w = "url(#%s-w)" % u
    tail = ('<g class="rc-tail"><path d="M84 200 C58 206 40 190 42 166 C44 146 58 136 54 118" fill="none" '
            'stroke="%(ink)s" stroke-width="10" stroke-linecap="round"/>'
            '<path d="M84 200 C58 206 40 190 42 166 C44 146 58 136 54 118" fill="none" stroke="%(a)s" '
            'stroke-width="6" stroke-linecap="round"/>'
            '<circle cx="54" cy="118" r="10" fill="%(g)s" opacity=".35"/><circle cx="54" cy="118" r="5.5" fill="%(gh)s"/></g>'
            % dict(ink=INK, a=ARMOUR, g=GLOW, gh=GLOW_HI))

    def leg(x):
        return ('<rect x="%g" y="196" width="18" height="32" rx="8" fill="%s" stroke="%s" stroke-width="2.2"/>'
                '<circle cx="%g" cy="211" r="5" fill="%s"/>'
                '<rect x="%g" y="226" width="30" height="13" rx="5" fill="%s" stroke="%s" stroke-width="2.2"/>'
                '<rect x="%g" y="236.5" width="24" height="2.6" rx="1.3" fill="%s"/>'
                % (x - 9, w, INK, x, JOINT, x - 15, BOOT, INK, x - 12, GLOW))
    legs = leg(98) + leg(122)
    body = ('<path d="M78 162 Q78 148 92 147 H128 Q142 148 142 162 V192 Q142 204 128 205 H92 Q78 204 78 192Z" '
            'fill="%(w)s" stroke="%(ink)s" stroke-width="2.4"/>'
            '<path d="M85 150 L92 196M135 150 L128 196" stroke="%(j)s" stroke-width="5" stroke-linecap="round"/>'
            '<rect x="96" y="157" width="28" height="30" rx="7" fill="#DCE7F5" stroke="#9FB3D1" stroke-width="1.4"/>'
            '<rect x="98" y="163" width="24" height="20" rx="6" fill="%(g)s" opacity=".35"/>'
            '<rect x="103" y="166" width="14" height="13" rx="3" fill="%(gh)s"/>'
            '<rect x="105" y="168" width="6" height="3" rx="1.5" fill="#fff" opacity=".85"/>'
            '<rect x="79" y="192" width="62" height="7" fill="%(j)s"/>'
            % dict(w=w, ink=INK, j=JOINT, g=GLOW, gh=GLOW_HI))

    def arm(x1, y1, x2, y2, cls):
        mx, my = (x1 + x2) / 2.0, (y1 + y2) / 2.0
        return ('<g class="%s"><path d="M%g %gL%g %g" stroke="%s" stroke-width="17" stroke-linecap="round"/>'
                '<path d="M%g %gL%g %g" stroke="%s" stroke-width="12.5" stroke-linecap="round"/>'
                '<circle cx="%g" cy="%g" r="5" fill="%s"/>'
                '<circle cx="%g" cy="%g" r="9" fill="%s" stroke="%s" stroke-width="2.2"/></g>'
                % (cls, x1, y1, x2, y2, INK, x1, y1, x2, y2, ARMOUR, mx, my, JOINT, x2, y2 + 2, HAND, INK))
    arms = (arm(82, 156, 68, 192, "rc-arm-down") + arm(138, 156, 152, 192, "rc-arm-down")
            + arm(82, 156, 46, 170, "rc-arm-up") + arm(138, 156, 174, 170, "rc-arm-up"))
    neck = '<ellipse cx="110" cy="148" rx="18" ry="5" fill="%s"/>' % INK
    shadow = '<ellipse class="rc-shadow" cx="110" cy="241" rx="60" ry="7" fill="#020617" opacity=".3"/>'
    size_attr = ' width="%d" height="%d"' % (size, round(size * 250 / 220)) if size else ""
    aria = ' role="img" aria-label="%s"' % label if label else ' aria-hidden="true" focusable="false"'
    return ('<svg class="%s is-%s" viewBox="0 0 220 250"%s%s>%s%s<g class="rc-bob">%s%s%s%s%s%s</g></svg>'
            % (cls, mood, size_attr, aria, _defs(u), shadow, tail, legs, body, arms, neck, _head(u)))


def head(cls="rc rc-head-only", mood="idle"):
    """Just the head, cropped from the whole cat, for small icons."""
    u = _uid("rh")
    return ('<svg class="%s is-%s" viewBox="34 4 152 152" aria-hidden="true" focusable="false">%s%s</svg>'
            % (cls, mood, _defs(u), _head(u)))
