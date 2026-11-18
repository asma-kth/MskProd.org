"""The City Run cat: a silver robot kitten with big blue eyes.

Polished metal plates held on with rivets, red and blue wires showing at the
joints and a gear in the top of its head. City Run draws the same cat from
behind as it runs (static/js/cityrun.js); this module draws it from the
front, for the lobby, the start of a run and the results.

Two drawings share the palette:

  svg()   the whole cat, standing. Its eyes can be open or closed in a
          smile: the class on the <svg> picks which (is-happy closes them).
  head()  just the head, for small icons.

Every gradient id carries a prefix, so the cat can appear more than once on
a page; the game copies it with fresh ids for the same reason.
"""

SILVER_HI = "#F8FAFC"
SILVER = "#CBD5E1"
SILVER_MID = "#94A3B8"
STEEL = "#64748B"
SLATE = "#475569"
INK = "#334155"
DEEP = "#1E293B"
WIRE_RED = "#DC2626"
WIRE_BLUE = "#2563EB"
EAR_IN = "#BE123C"
EAR_DEEP = "#881337"
NOSE = "#F472B6"
BLUSH = "#F9A8D4"

_SEQ = [0]


def _uid(prefix):
    _SEQ[0] += 1
    return "%s%d" % (prefix, _SEQ[0])


def _defs(u):
    return ('<defs>'
            '<radialGradient id="%(u)s-m" cx="38%%" cy="28%%" r="78%%">'
            '<stop offset="0" stop-color="#FFFFFF"/><stop offset=".35" stop-color="%(hi)s"/>'
            '<stop offset=".75" stop-color="%(s)s"/><stop offset="1" stop-color="%(mid)s"/></radialGradient>'
            '<linearGradient id="%(u)s-b" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0" stop-color="%(hi)s"/><stop offset=".55" stop-color="%(s)s"/>'
            '<stop offset="1" stop-color="%(mid)s"/></linearGradient>'
            '<radialGradient id="%(u)s-i" cx="50%%" cy="58%%" r="60%%">'
            '<stop offset="0" stop-color="#BAE6FD"/><stop offset=".38" stop-color="#38BDF8"/>'
            '<stop offset=".78" stop-color="#2563EB"/><stop offset="1" stop-color="#1E3A8A"/></radialGradient>'
            '<linearGradient id="%(u)s-e" x1="0" y1="0" x2="0" y2="1">'
            '<stop offset="0" stop-color="%(ed)s"/><stop offset="1" stop-color="%(ei)s"/></linearGradient>'
            '</defs>' % dict(u=u, hi=SILVER_HI, s=SILVER, mid=SILVER_MID, ed=EAR_DEEP, ei=EAR_IN))


def _gear(cx, cy, r, teeth=8, fill=SLATE, hub=SILVER):
    """A small gear: a toothed ring with a hub."""
    import math
    pts = []
    for k in range(teeth * 2):
        a = math.pi * k / teeth
        rr = r if k % 2 == 0 else r * 0.74
        a1, a2 = a - math.pi / (teeth * 2.6), a + math.pi / (teeth * 2.6)
        pts.append("%.1f %.1f" % (cx + rr * math.cos(a1), cy + rr * math.sin(a1)))
        pts.append("%.1f %.1f" % (cx + rr * math.cos(a2), cy + rr * math.sin(a2)))
    return ('<path d="M%sZ" fill="%s"/><circle cx="%g" cy="%g" r="%.1f" fill="%s"/>'
            '<circle cx="%g" cy="%g" r="%.1f" fill="%s"/>'
            % (" L".join(pts), fill, cx, cy, r * 0.45, hub, cx, cy, r * 0.18, DEEP))


def _rivet(x, y, r=1.7):
    return ('<circle cx="%g" cy="%g" r="%g" fill="%s"/><circle cx="%g" cy="%g" r="%g" fill="#fff" opacity=".8"/>'
            % (x, y, r, STEEL, x - r * 0.3, y - r * 0.35, r * 0.4))


def _head(u):
    """The head in the whole cat's coordinates, centred on x = 112."""
    m = "url(#%s-m)" % u
    ear = ('<path d="M58 74 L54 22 Q55 11 65 16 L98 44 Z" fill="%(m)s" stroke="%(ink)s" stroke-width="2.4" '
           'stroke-linejoin="round"/><path d="M63 64 L61 28 L89 47 Z" fill="url(#%(u)s-e)"/>'
           '<path d="M61 28 L89 47" stroke="#FDA4AF" stroke-width="1.4" opacity=".55"/>'
           % dict(m=m, ink=INK, u=u))
    ears = ('<g class="rc-ear rc-ear-l">%s</g><g class="rc-ear rc-ear-r" transform="translate(224 0) scale(-1 1)">%s</g>'
            % (ear, ear))
    skull = ('<path d="M52 102 C50 62 78 40 112 40 C146 40 174 62 172 102 C170 134 146 152 112 152 '
             'C78 152 54 134 52 102Z" fill="%s" stroke="%s" stroke-width="2.6"/>' % (m, INK))
    seams = ('<path d="M70 70 Q112 56 154 70M112 41v13M60 112 Q66 138 92 147M164 112 Q158 138 132 147" fill="none" '
             'stroke="%s" stroke-width="1.5" stroke-linecap="round" opacity=".75"/>' % SILVER_MID)
    hatch = ('<ellipse cx="112" cy="58" rx="15" ry="9" fill="%s" stroke="%s" stroke-width="1.6"/>%s'
             '<path d="M100 60 Q106 50 112 59M124 60 Q118 50 112 59" fill="none" stroke-width="2.2" '
             'stroke-linecap="round" stroke="%s"/><path d="M103 63 Q112 55 121 63" fill="none" stroke-width="2" '
             'stroke-linecap="round" stroke="%s"/>'
             % (DEEP, INK, _gear(112, 58, 6.5, 8, SLATE, SILVER), WIRE_RED, WIRE_BLUE))
    bolts = ('<circle cx="56" cy="112" r="8.5" fill="%(mid)s" stroke="%(ink)s" stroke-width="1.8"/>'
             '<circle cx="56" cy="112" r="4" fill="%(sl)s"/><path d="M53 112h6M56 109v6" stroke="%(s)s" '
             'stroke-width="1.4" stroke-linecap="round"/>'
             '<circle cx="168" cy="112" r="7" fill="%(mid)s" stroke="%(ink)s" stroke-width="1.6"/>'
             '<circle cx="168" cy="112" r="3.2" fill="%(sl)s"/>'
             % dict(mid=SILVER_MID, ink=INK, sl=SLATE, s=SILVER))
    rivets = "".join(_rivet(x, y) for x, y in ((78, 64), (146, 64), (67, 86), (157, 86), (88, 146), (136, 146)))

    def eye(cx):
        return ('<circle cx="%(x)g" cy="98" r="22.5" fill="%(mid)s" stroke="%(ink)s" stroke-width="2"/>'
                '<circle cx="%(x)g" cy="98" r="19.5" fill="%(deep)s"/>'
                '<circle class="rc-iris" cx="%(x)g" cy="99" r="17.5" fill="url(#%(u)s-i)"/>'
                '<circle class="rc-pupil" cx="%(x)g" cy="100" r="9.5" fill="#020617"/>'
                '<circle cx="%(x1)g" cy="90.5" r="5.2" fill="#fff"/><circle cx="%(x2)g" cy="106" r="2.4" fill="#fff" opacity=".85"/>'
                '<path d="M%(l)g 87 Q%(x)g 74 %(r)g 87" fill="none" stroke="%(s)s" stroke-width="3.2" stroke-linecap="round"/>'
                % dict(x=cx, x1=cx - 6.5, x2=cx + 6.5, l=cx - 17, r=cx + 17, mid=SILVER_MID, ink=INK, deep=DEEP,
                       u=u, s=SILVER_HI))
    open_eyes = '<g class="rc-open">%s%s</g>' % (eye(90), eye(134))
    happy = ('<g class="rc-happy"><path d="M74 103 Q90 84 106 103M118 103 Q134 84 150 103" fill="none" stroke="%s" '
             'stroke-width="5.5" stroke-linecap="round"/><ellipse cx="72" cy="124" rx="9" ry="5" fill="%s" opacity=".75"/>'
             '<ellipse cx="152" cy="124" rx="9" ry="5" fill="%s" opacity=".75"/></g>' % (DEEP, BLUSH, BLUSH))
    muzzle = ('<ellipse cx="112" cy="128" rx="22" ry="14.5" fill="%s" stroke="%s" stroke-width="1.2"/>'
              '%s'
              '<path d="M104 118 Q112 112.5 120 118 Q119 125.5 112 127.5 Q105 125.5 104 118Z" fill="%s" '
              'stroke="#BE185D" stroke-width="1.2"/><ellipse cx="109" cy="118.5" rx="3" ry="1.5" fill="#fff" opacity=".7"/>'
              '<path d="M112 127.5v4M112 131.5q-4.5 4.5 -9.5 1M112 131.5q4.5 4.5 9.5 1" fill="none" stroke="%s" '
              'stroke-width="1.9" stroke-linecap="round"/>'
              % (SILVER_HI, SILVER_MID,
                 "".join('<circle cx="%g" cy="%g" r="1.3" fill="%s"/>' % (x, y, STEEL)
                         for x, y in ((99, 126), (96.5, 131), (101.5, 133), (125, 126), (127.5, 131), (122.5, 133))),
                 NOSE, INK))
    whiskers = ('<path class="rc-whisk" d="M94 125 L46 117M94 130 L44 131M95 135 L48 145M130 125 L178 117M130 130 L180 131'
                'M129 135 L176 145" stroke="%s" stroke-width="1.7" stroke-linecap="round"/>' % STEEL)
    return ('<g class="rc-head">%s%s%s%s%s%s%s%s%s%s</g>'
            % (ears, skull, seams, hatch, bolts, rivets, open_eyes, happy, muzzle, whiskers))


def svg(mood="idle", cls="rc", label=None, size=None):
    """The whole cat, standing, in a 224 by 232 box."""
    u = _uid("rc")
    m = "url(#%s-m)" % u
    b = "url(#%s-b)" % u
    tail = ('<g class="rc-tail"><path d="M76 172 C48 174 30 158 32 134 C34 114 48 102 44 82" fill="none" stroke="%(ink)s" '
            'stroke-width="15" stroke-linecap="round"/><path d="M76 172 C48 174 30 158 32 134 C34 114 48 102 44 82" '
            'fill="none" stroke="%(s)s" stroke-width="10.5" stroke-linecap="round"/>'
            '<path d="M76 172 C48 174 30 158 32 134 C34 114 48 102 44 82" fill="none" stroke="%(deep)s" '
            'stroke-width="11" stroke-dasharray="3.5 10" stroke-dashoffset="4"/>'
            '<path d="M76 172 C48 174 30 158 32 134 C34 114 48 102 44 82" fill="none" stroke="%(red)s" '
            'stroke-width="3" stroke-dasharray="3.5 10" stroke-dashoffset="4"/>'
            '<path d="M74 168 C50 169 36 156 37 134 C38 116 50 104 47 86" fill="none" stroke="#fff" '
            'stroke-width="2.2" stroke-linecap="round" opacity=".55"/>'
            '<circle cx="44" cy="80" r="7.5" fill="%(m)s" stroke="%(ink)s" stroke-width="2.2"/></g>'
            % dict(ink=INK, s=SILVER, deep=DEEP, red=WIRE_RED, m=m))

    def leg(x, back=False):
        shade = ' opacity=".9"' if back else ""
        return ('<g class="rc-leg"%s><rect x="%g" y="176" width="21" height="32" rx="9.5" fill="%s" stroke="%s" '
                'stroke-width="2.2"/><circle cx="%g" cy="190" r="6" fill="%s" stroke="%s" stroke-width="1.6"/>'
                '<circle cx="%g" cy="190" r="2.2" fill="%s"/>'
                '<ellipse cx="%g" cy="208" rx="13.5" ry="7.5" fill="%s" stroke="%s" stroke-width="2.2"/>'
                '<path d="M%g 204v5M%g 203v6M%g 204v5" stroke="%s" stroke-width="1.5" stroke-linecap="round"/></g>'
                % (shade, x - 10.5, b, INK, x, SILVER_MID, INK, x, DEEP, x, m, INK, x - 5, x, x + 5, SILVER_MID))
    legs_back = leg(70, True) + leg(154, True)
    body = ('<ellipse cx="112" cy="172" rx="54" ry="31" fill="%s" stroke="%s" stroke-width="2.6"/>'
            '<path d="M70 160 Q112 146 154 160" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" opacity=".6"/>'
            '<ellipse cx="80" cy="176" rx="15" ry="12" fill="%s" stroke="%s" stroke-width="1.6"/>%s'
            '<path d="M68 180 Q76 170 84 182M72 186 Q82 176 92 186" fill="none" stroke-width="2.2" stroke-linecap="round" '
            'stroke="%s"/><path d="M70 172 Q80 184 90 172" fill="none" stroke-width="2" stroke-linecap="round" stroke="%s"/>'
            '<ellipse cx="124" cy="176" rx="22" ry="18" fill="%s" stroke="%s" stroke-width="1.4" opacity=".95"/>%s'
            % (m, INK, DEEP, INK, _gear(81, 175, 7.5, 9, SLATE, SILVER), WIRE_RED, WIRE_BLUE, SILVER_HI, SILVER_MID,
               "".join(_rivet(x, y, 1.6) for x, y in ((110, 166), (138, 166), (110, 186), (138, 186)))))
    neck = ('<ellipse cx="112" cy="150" rx="31" ry="9" fill="%s"/>%s'
            '<path d="M90 150 Q100 158 110 150M114 151 Q124 159 134 151" fill="none" stroke-width="2.2" stroke-linecap="round" '
            'stroke="%s"/><path d="M98 147 Q112 156 126 147" fill="none" stroke-width="2" stroke="%s"/>'
            % (DEEP, _gear(84, 150, 6, 7, SLATE, SILVER) + _gear(140, 150, 6, 7, SLATE, SILVER), WIRE_RED, WIRE_BLUE))
    legs_front = leg(98) + leg(126)
    shadow = '<ellipse class="rc-shadow" cx="112" cy="216" rx="76" ry="8" fill="#0F172A" opacity=".22"/>'
    size_attr = ' width="%d" height="%d"' % (size, round(size * 232 / 224)) if size else ""
    aria = ' role="img" aria-label="%s"' % label if label else ' aria-hidden="true" focusable="false"'
    return ('<svg class="%s is-%s" viewBox="0 0 224 232"%s%s>%s%s<g class="rc-bob">%s%s%s%s%s%s</g></svg>'
            % (cls, mood, size_attr, aria, _defs(u), shadow, tail, legs_back, body, legs_front, neck, _head(u)))


def head(cls="rc rc-head-only", mood="idle"):
    """Just the head, cropped from the whole cat, for small icons."""
    u = _uid("rh")
    return ('<svg class="%s is-%s" viewBox="40 6 144 152" aria-hidden="true" focusable="false">%s%s</svg>'
            % (cls, mood, _defs(u), _head(u)))
