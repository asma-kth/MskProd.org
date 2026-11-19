"""The City Run cat: a silver robot cat on inline skates.

Weathered silver plates with seams and rivets, tall ears whose insides are
panels of glowing cyan lights, big round goggle eyes that are little pixel
screens, a small nose and whiskers, a segmented tail, a backpack with a
glowing ring, and inline skates with teal wheels. City Run draws the same
cat from behind as it skates (static/js/cityrun.js); this module draws it
from the front, for the results and the small icons.

Two drawings share the palette:

  svg()   the whole cat, standing on its skates. The class on the <svg> picks
          its mood: is-happy turns its pixel eyes into smiles and throws its
          arms out.
  head()  just the head, for small icons.

Every gradient and clip id carries a prefix, so the cat can appear more than
once on a page; the game copies it with fresh ids for the same reason.
"""

METAL_HI = "#F4F5FB"
METAL = "#CDD0E3"
METAL_MID = "#A3A7C3"
METAL_LO = "#7A7E9E"
SEAM = "#8A8EAE"
JOINT = "#2E3150"
INK = "#2A2D4A"
RING_HI = "#7C82A6"
RING_LO = "#3A3E5E"
SCREEN = "#071420"
LED = "#67E8F9"
LED_DIM = "#123E4C"
GLOW = "#22D3EE"
WHEEL = "#2DD4BF"
PACK = "#7F89B2"
NOSE = "#3B3346"

# The pixel patterns on the eye screens, five by five.
EYES = {"open": ["X...X", "X...X", "XXXXX", "X...X", "X...X"],
        "happy": [".....", "..X..", ".X.X.", "X...X", "....."]}

_SEQ = [0]


def _uid(prefix):
    _SEQ[0] += 1
    return "%s%d" % (prefix, _SEQ[0])


def _defs(u):
    return ('<defs>'
            '<radialGradient id="%(u)s-m" cx="38%%" cy="28%%" r="80%%">'
            '<stop offset="0" stop-color="%(hi)s"/><stop offset=".45" stop-color="%(m)s"/>'
            '<stop offset=".8" stop-color="%(mid)s"/><stop offset="1" stop-color="%(lo)s"/></radialGradient>'
            '<linearGradient id="%(u)s-b" x1="0" y1="0" x2="1" y2="1">'
            '<stop offset="0" stop-color="%(hi)s"/><stop offset=".5" stop-color="%(m)s"/>'
            '<stop offset="1" stop-color="%(mid)s"/></linearGradient>'
            '<linearGradient id="%(u)s-r" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0" stop-color="%(rh)s"/><stop offset="1" stop-color="%(rl)s"/></linearGradient>'
            '<clipPath id="%(u)s-e"><path d="M64.5 66 L65.5 27 L92 47 Z"/></clipPath>'
            '</defs>' % dict(u=u, hi=METAL_HI, m=METAL, mid=METAL_MID, lo=METAL_LO, rh=RING_HI, rl=RING_LO))


def _pixels(cx, cy, pattern, cls):
    """A five by five screen of lights, lit where the pattern says."""
    out = []
    for r, row in enumerate(pattern):
        for c, ch in enumerate(row):
            x, y = cx + (c - 2) * 5.2, cy + (r - 2) * 5.2
            if ch == "X":
                out.append('<rect x="%.1f" y="%.1f" width="5" height="5" rx="1.2" fill="%s" opacity=".35"/>'
                           '<rect x="%.1f" y="%.1f" width="3.6" height="3.6" rx=".8" fill="%s"/>'
                           % (x - 2.5, y - 2.5, GLOW, x - 1.8, y - 1.8, LED))
            else:
                out.append('<rect x="%.1f" y="%.1f" width="3.2" height="3.2" rx=".8" fill="%s"/>' % (x - 1.6, y - 1.6, LED_DIM))
    return '<g class="%s">%s</g>' % (cls, "".join(out))


def _head(u):
    """The head in the whole cat's coordinates, centred on x = 110."""
    m = "url(#%s-m)" % u
    dots = "".join('<rect x="%.1f" y="%.1f" width="2.3" height="2.3" fill="%s"/>' % (x, y, LED)
                   for y in range(27, 66, 4) for x in range(63, 93, 4))
    ear = ('<path d="M56 80 L58 18 Q60 9 69 14 L104 46 Z" fill="%(m)s" stroke="%(ink)s" stroke-width="2.4" '
           'stroke-linejoin="round"/>'
           '<path d="M64.5 66 L65.5 27 L92 47 Z" fill="%(dim)s"/>'
           '<g clip-path="url(#%(u)s-e)">%(dots)s</g>'
           '<path d="M64.5 66 L65.5 27 L92 47 Z" fill="%(g)s" opacity=".3"/>'
           % dict(m=m, ink=INK, dim="#0E3B46", u=u, dots=dots, g=GLOW))
    # The right ear is the left one mirrored. The mirror sits on an inner
    # group, because the page's CSS turns the outer one when the ear twitches.
    ears = ('<g class="rc-ear rc-ear-l">%s</g><g class="rc-ear rc-ear-r"><g transform="translate(220 0) scale(-1 1)">%s</g></g>'
            % (ear, ear))
    skull = ('<path d="M46 102 C44 62 74 40 110 40 C146 40 176 62 174 102 C172 134 146 154 110 154 '
             'C74 154 48 134 46 102Z" fill="%s" stroke="%s" stroke-width="2.6"/>' % (m, INK))
    seams = ('<path d="M58 80 Q110 56 162 80" fill="none" stroke="%(s)s" stroke-width="3"/>'
             '<path d="M58 80 Q110 56 162 80" fill="none" stroke="#fff" stroke-width="1" opacity=".5" transform="translate(0 -1.6)"/>'
             '<path d="M110 41 V64M64 126 Q74 146 96 151M156 126 Q146 146 124 151" fill="none" stroke="%(s)s" '
             'stroke-width="1.5" stroke-linecap="round"/>'
             % dict(s=SEAM))
    rivets = "".join('<circle cx="%g" cy="%g" r="2" fill="%s"/><circle cx="%g" cy="%g" r=".8" fill="#fff" opacity=".7"/>'
                     % (x, y, SEAM, x - .5, y - .6) for x, y in ((70, 72), (150, 72), (90, 62), (130, 62)))
    grime = ('<g fill="%s" opacity=".18"><circle cx="78" cy="58" r="3"/><circle cx="142" cy="130" r="4"/>'
             '<circle cx="60" cy="118" r="2.5"/><circle cx="128" cy="50" r="2"/><circle cx="96" cy="140" r="2.2"/></g>'
             % METAL_LO)

    def eye(x):
        return ('<circle cx="%(x)g" cy="106" r="26" fill="url(#%(u)s-r)" stroke="%(ink)s" stroke-width="2.2"/>'
                '<circle cx="%(x)g" cy="106" r="20.5" fill="#23264A"/>'
                '<circle cx="%(x)g" cy="106" r="17.5" fill="%(scr)s"/>'
                % dict(x=x, u=u, ink=INK, scr=SCREEN))
    glass = ('<path d="M64 96 Q70 84 82 82M120 96 Q126 84 138 82" fill="none" stroke="#fff" stroke-width="3" '
             'stroke-linecap="round" opacity=".35"/>')
    screens = (_pixels(84, 106, EYES["open"], "rc-open") + _pixels(136, 106, EYES["open"], "rc-open")
               + _pixels(84, 106, EYES["happy"], "rc-happy") + _pixels(136, 106, EYES["happy"], "rc-happy"))
    face = ('<path d="M104.5 125 h11 l-5.5 6.2 Z" fill="%(n)s" stroke="%(n)s" stroke-width="1.5" stroke-linejoin="round"/>'
            '<path d="M110 131 v3.4 M110 134.4 q-5 5 -10 1.4 M110 134.4 q5 5 10 1.4" fill="none" stroke="%(ink)s" '
            'stroke-width="1.8" stroke-linecap="round"/>'
            '<path class="rc-whisk" d="M92 130 L46 122 M92 135 L44 138 M128 130 L174 122 M128 135 L176 138" '
            'stroke="%(w)s" stroke-width="1.3" stroke-linecap="round"/>'
            % dict(n=NOSE, ink=INK, w=METAL_LO))
    return ('<g class="rc-head">%s%s%s%s%s%s%s%s%s%s</g>'
            % (ears, skull, grime, seams, rivets, eye(84), eye(136), screens, glass, face))


def svg(mood="idle", cls="rc", label=None, size=None):
    """The whole cat, standing on its skates, in a 220 by 268 box."""
    u = _uid("rc")
    m = "url(#%s-m)" % u
    b = "url(#%s-b)" % u
    tail = ('<g class="rc-tail"><path d="M84 210 C60 214 44 200 44 180 C44 160 58 150 55 132" fill="none" stroke="%(ink)s" '
            'stroke-width="12" stroke-linecap="round"/>'
            '<path d="M84 210 C60 214 44 200 44 180 C44 160 58 150 55 132" fill="none" stroke="%(m)s" '
            'stroke-width="8.5" stroke-linecap="round"/>'
            '<path d="M84 210 C60 214 44 200 44 180 C44 160 58 150 55 132" fill="none" stroke="%(j)s" '
            'stroke-width="9" stroke-dasharray="2.6 9"/>'
            '<circle cx="55" cy="130" r="6" fill="%(m)s" stroke="%(ink)s" stroke-width="2"/></g>'
            % dict(ink=INK, m=METAL, j=JOINT))
    pack = ('<rect x="72" y="150" width="76" height="56" rx="12" fill="%s" stroke="%s" stroke-width="2.2"/>'
            '<circle cx="146" cy="168" r="7" fill="%s" opacity=".5"/><circle cx="146" cy="168" r="4" fill="%s"/>'
            % (PACK, INK, GLOW, LED))

    def leg(x, sd):
        # hip, thigh, knee, shin, then a skate turned a little outwards
        w0 = x - 12 + sd * 2
        wheels = "".join('<circle cx="%.1f" cy="%.1f" r="4.2" fill="%s" stroke="%s" stroke-width="1.6"/>'
                         '<circle cx="%.1f" cy="%.1f" r="1.4" fill="#E0FBFF"/>'
                         % (w0 + i * 8 + sd * i * 1.2, 260 - i * 0.6, WHEEL, INK, w0 + i * 8 + sd * i * 1.2, 260 - i * 0.6)
                         for i in range(4))
        return ('<circle cx="%(x)g" cy="216" r="7.5" fill="%(j)s"/>'
                '<rect x="%(x0)g" y="218" width="16" height="16" rx="6" fill="%(b)s" stroke="%(ink)s" stroke-width="2"/>'
                '<circle cx="%(x)g" cy="236" r="5.5" fill="%(j)s"/>'
                '<rect x="%(x1)g" y="238" width="14" height="8" rx="3" fill="%(b)s" stroke="%(ink)s" stroke-width="2"/>'
                '<path d="M%(bx0)g 244 h22 a4 4 0 0 1 4 4 v4 h-30 v-4 a4 4 0 0 1 4 -4Z" fill="%(m)s" stroke="%(ink)s" stroke-width="2"/>'
                '<rect x="%(bx1)g" y="244.5" width="22" height="3" fill="%(j)s"/>'
                '<rect x="%(fx)g" y="252" width="32" height="4" rx="1.5" fill="%(rl)s"/>%(wheels)s'
                % dict(x=x, x0=x - 8, x1=x - 7, bx0=x - 13, bx1=x - 11, fx=x - 16, j=JOINT, b=b, m=m, ink=INK,
                       rl=RING_LO, wheels=wheels))
    legs = leg(97, -1) + leg(123, 1)
    body = ('<path d="M80 172 Q80 156 95 154 H125 Q140 156 140 172 V198 Q140 208 128 209 H92 Q80 208 80 198Z" '
            'fill="%(m)s" stroke="%(ink)s" stroke-width="2.4"/>'
            '<path d="M86 160 Q110 152 134 160" fill="none" stroke="#fff" stroke-width="2" opacity=".55"/>'
            '<circle cx="124" cy="172" r="6.5" fill="%(rl)s" stroke="%(s)s" stroke-width="1.6"/>'
            '<circle cx="124" cy="172" r="2.8" fill="%(rh)s"/>'
            '<rect x="96" y="186" width="28" height="15" rx="4" fill="%(s)s" stroke="%(ink)s" stroke-width="1.4"/>'
            '<path d="M101 190 v7 M106 190 v7 M111 190 v7 M116 190 v7 M120 190 v7" stroke="%(j)s" stroke-width="2"/>'
            '<rect x="82" y="205" width="56" height="9" rx="3" fill="%(j)s"/>'
            '<path d="M86 209.5 H134" stroke="#4A4E70" stroke-width="1.4"/>'
            % dict(m=m, ink=INK, rl=RING_LO, rh=RING_HI, s=SEAM, j=JOINT))

    def arm(sx, sy, ex, ey, hx, hy, cls):
        return ('<g class="%(c)s"><circle cx="%(sx)g" cy="%(sy)g" r="9.5" fill="%(m)s" stroke="%(ink)s" stroke-width="2"/>'
                '<path d="M%(sx)g %(sy)gL%(ex)g %(ey)g" stroke="%(ink)s" stroke-width="15" stroke-linecap="round"/>'
                '<path d="M%(sx)g %(sy)gL%(ex)g %(ey)g" stroke="%(mc)s" stroke-width="11" stroke-linecap="round"/>'
                '<circle cx="%(ex)g" cy="%(ey)g" r="5.5" fill="%(j)s"/>'
                '<path d="M%(ex)g %(ey)gL%(hx)g %(hy)g" stroke="%(ink)s" stroke-width="13" stroke-linecap="round"/>'
                '<path d="M%(ex)g %(ey)gL%(hx)g %(hy)g" stroke="%(mc)s" stroke-width="9.5" stroke-linecap="round"/>'
                '<circle cx="%(hx)g" cy="%(hy)g" r="6.5" fill="%(rl)s" stroke="%(ink)s" stroke-width="1.8"/>'
                '<path d="M%(f1)s" stroke="%(ink)s" stroke-width="2.6" stroke-linecap="round"/></g>'
                % dict(c=cls, sx=sx, sy=sy, ex=ex, ey=ey, hx=hx, hy=hy, m=m, mc=METAL, ink=INK, j=JOINT, rl=RING_LO,
                       f1="%g %gl-2 6M%g %gl0 6.5M%g %gl2 6" % (hx - 3, hy + 3, hx, hy + 4, hx + 3, hy + 3)))
    arms = (arm(80, 162, 72, 186, 68, 206, "rc-arm-down") + arm(140, 162, 148, 186, 152, 206, "rc-arm-down")
            + arm(80, 162, 58, 156, 42, 142, "rc-arm-up") + arm(140, 162, 162, 156, 178, 142, "rc-arm-up"))
    neck = '<ellipse cx="110" cy="154" rx="20" ry="6" fill="%s"/>' % JOINT
    shadow = '<ellipse class="rc-shadow" cx="110" cy="264" rx="58" ry="4.5" fill="#020617" opacity=".3"/>'
    size_attr = ' width="%d" height="%d"' % (size, round(size * 268 / 220)) if size else ""
    aria = ' role="img" aria-label="%s"' % label if label else ' aria-hidden="true" focusable="false"'
    return ('<svg class="%s is-%s" viewBox="0 0 220 268"%s%s>%s%s<g class="rc-bob">%s%s%s%s%s%s%s</g></svg>'
            % (cls, mood, size_attr, aria, _defs(u), shadow, tail, pack, legs, body, arms, neck, _head(u)))


def head(cls="rc rc-head-only", mood="idle"):
    """Just the head, cropped from the whole cat, for small icons."""
    u = _uid("rh")
    return ('<svg class="%s is-%s" viewBox="38 6 144 152" aria-hidden="true" focusable="false">%s%s</svg>'
            % (cls, mood, _defs(u), _head(u)))
