"""The printable certificate for Artificial Intelligence: Zero to Hero.

Like the progress page, it ships with nothing personal in it. The browser reads
the quiz scores saved on this device, unlocks the certificate once every lesson
quiz in the course has been passed at 70 per cent or more, and fills in the
name, school, date and colours the student chooses. The certificate itself is
one A4 landscape SVG, drawn here, so it looks the same on screen and on paper.
"""
import json
import math
import re

from mskbuild import markup
from mskbuild.render import layout, crumbs, crumbs_ld, esc, ico, logo_svg, write

PASS = 70
W, H = 1123, 794           # A4 landscape at 96 dots per inch
CX = W / 2

# (id, name, three colours from deep to bright)
THEMES = [
    ("nebula", "Nebula", ("#6D28D9", "#DB2777", "#F59E0B")),
    ("ocean", "Ocean", ("#1D4ED8", "#0891B2", "#10B981")),
    ("forest", "Forest", ("#065F46", "#059669", "#84CC16")),
    ("sunset", "Sunset", ("#B91C1C", "#EA580C", "#EAB308")),
    ("royal", "Royal", ("#1E1B4B", "#7C3AED", "#D4A017")),
]

LEAD = ("Pass every lesson quiz in the AI course with at least 70% and your certificate "
        "unlocks here. Add your name, choose your colours and print it, or save it as a PDF.")

FOOT = """
## How the certificate works

- **What unlocks it.** A score of at least 70% on the quiz at the end of each of the 30 lessons, across all 15 levels. Your best score on each quiz counts, so retaking one for practice never takes a pass away.
- **Where your scores live.** In this browser's storage on this device, like everything else on the site. Nothing is uploaded and there is no account, so use the same browser and device for the whole course. Clearing your browsing data, or using a private window, starts the count again.
- **The date.** It starts as the day you completed your last quiz. You can change it, for example to the date of a presentation.
- **The certificate number.** It is worked out from your name and the date, so the same details always print the same number.

## Printing it well

1. Press **Print or save as PDF**.
2. Choose your printer, or **Save as PDF** to keep a copy.
3. Check the layout is **landscape** and the paper is **A4**.
4. Switch **headers and footers** off, and switch **background graphics** on if your browser offers it.

!info Teachers :: The certificate needs no sign-in, so a student can print it at home or in school. If you would like the whole class to finish together, set two lessons a week and the course takes about fifteen weeks.
"""


def _mix(colours, t):
    """The colour a fraction t of the way along the theme's three colours."""
    def rgb(h):
        return [int(h[i:i + 2], 16) for i in (1, 3, 5)]
    a, b = (colours[0], colours[1]) if t <= 0.5 else (colours[1], colours[2])
    u = t * 2 if t <= 0.5 else (t - 0.5) * 2
    ca, cb = rgb(a), rgb(b)
    return "#%02X%02X%02X" % tuple(round(x + (y - x) * u) for x, y in zip(ca, cb))


def _text(x, y, txt, cls, anchor="middle", ident=None, extra=""):
    return '<text x="%g" y="%g" text-anchor="%s" class="%s"%s%s>%s</text>' % (
        x, y, anchor, cls, ' id="%s"' % ident if ident else "", extra, esc(txt))


def _network(c):
    """A small neural network for one corner, drawn pointing into the page."""
    l0 = [(0, 0), (0, 44), (0, 88)]
    l1 = [(48, 22), (48, 66)]
    l2 = [(96, 44)]
    out = ['<g class="ct-net">']
    for a in l0:
        for b in l1:
            out.append('<line x1="%d" y1="%d" x2="%d" y2="%d" data-stroke="1" stroke="%s"/>' % (a + b + (c[0],)))
    for a in l1:
        for b in l2:
            out.append('<line x1="%d" y1="%d" x2="%d" y2="%d" data-stroke="2" stroke="%s"/>' % (a + b + (c[1],)))
    for i, (x, y) in enumerate(l0 + l1 + l2):
        k = (0, 1, 2, 1, 2, 2)[i]
        out.append('<circle cx="%d" cy="%d" r="7.5" data-fill="%d" fill="%s"/>' % (x, y, k + 1, c[k]))
    out.append("</g>")
    return "".join(out)


def _seal(cx, cy, c):
    """A scalloped rosette with the course name running round its edge."""
    n, r_in, r_out = 22, 52, 61
    pts = []
    for k in range(n):
        a0 = 2 * math.pi * k / n
        a1 = 2 * math.pi * (k + 1) / n
        am = (a0 + a1) / 2
        if not pts:
            pts.append("M%.1f %.1f" % (cx + r_in * math.cos(a0), cy + r_in * math.sin(a0)))
        pts.append("Q%.1f %.1f %.1f %.1f" % (cx + r_out * math.cos(am), cy + r_out * math.sin(am),
                                             cx + r_in * math.cos(a1), cy + r_in * math.sin(a1)))
    rosette = '<path d="%sZ" fill="url(#cg-seal)"/>' % " ".join(pts)
    r = 40
    arc = ('<path id="cg-seal-arc" d="M%g %g a%d %d 0 1 1 %d 0 a%d %d 0 1 1 %d 0" fill="none"/>'
           % (cx - r, cy, r, r, 2 * r, r, r, -2 * r))
    ribbons = (
        '<path d="M%g %g l-12 44 l13 -8 l9 11 l8 -45z" data-fill="1" fill="%s"/>' % (cx - 26, cy + 34, c[0]) +
        '<path d="M%g %g l12 44 l-13 -8 l-9 11 l-8 -45z" data-fill="2" fill="%s"/>' % (cx + 26, cy + 34, c[1]))
    star = []
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 5
        rr = 9 if k % 2 == 0 else 3.8
        star.append("%.1f,%.1f" % (cx + rr * math.cos(a), cy - 22 + rr * math.sin(a)))
    return "".join([
        ribbons, rosette,
        '<circle cx="%g" cy="%g" r="46" fill="none" stroke="#FFFFFF" stroke-opacity=".75" stroke-width="1.5"/>' % (cx, cy),
        '<circle cx="%g" cy="%g" r="32" fill="none" stroke="#FFFFFF" stroke-opacity=".75" stroke-width="1"/>' % (cx, cy),
        arc,
        '<text class="ct-seal-arc"><textPath href="#cg-seal-arc" startOffset="0" textLength="246" '
        'lengthAdjust="spacing">ARTIFICIAL INTELLIGENCE · ZERO TO HERO · </textPath></text>',
        '<polygon points="%s" fill="#FFFFFF"/>' % " ".join(star),
        _text(cx, cy + 11, "15", "ct-seal-num"),
        _text(cx, cy + 23, "LEVELS", "ct-seal-sub"),
    ])


def _logo(x, y, size):
    """The site's cat logo, nested at a fixed place and size."""
    svg = logo_svg("ct-logo")
    return re.sub(r"^<svg [^>]*>",
                  '<svg class="ct-logo" x="%g" y="%g" width="%g" height="%g" viewBox="0 0 100 100" '
                  'aria-hidden="true">' % (x, y, size, size), svg, count=1)


def certificate_svg(levels):
    c = THEMES[0][2]
    stops = ('<stop offset="0" data-c="1" stop-color="%s"/><stop offset=".5" data-c="2" stop-color="%s"/>'
             '<stop offset="1" data-c="3" stop-color="%s"/>' % c)
    defs = (
        '<defs>'
        '<linearGradient id="cg-frame" x1="0" y1="0" x2="1" y2="1">%s</linearGradient>'
        '<linearGradient id="cg-line" x1="0" y1="0" x2="1" y2="0">%s</linearGradient>'
        '<radialGradient id="cg-seal" cx=".38" cy=".32" r=".75">'
        '<stop offset="0" data-c="3" stop-color="%s"/><stop offset=".55" data-c="2" stop-color="%s"/>'
        '<stop offset="1" data-c="1" stop-color="%s"/></radialGradient>'
        '<radialGradient id="cg-wash1"><stop offset="0" data-c="1" stop-color="%s" stop-opacity=".16"/>'
        '<stop offset="1" data-c="1" stop-color="%s" stop-opacity="0"/></radialGradient>'
        '<radialGradient id="cg-wash2"><stop offset="0" data-c="3" stop-color="%s" stop-opacity=".18"/>'
        '<stop offset="1" data-c="3" stop-color="%s" stop-opacity="0"/></radialGradient>'
        '<pattern id="cg-dots" width="22" height="22" patternUnits="userSpaceOnUse">'
        '<circle cx="11" cy="11" r="1.1" fill="#1E1B4B" fill-opacity=".06"/></pattern>'
        '</defs>' % (stops, stops, c[2], c[1], c[0], c[0], c[0], c[2], c[2]))

    corners = [
        "translate(70 66)",
        "translate(%g 66) scale(-1 1)" % (W - 70),
        "translate(70 %g) scale(1 -1)" % (H - 66),
        "translate(%g %g) scale(-1 -1)" % (W - 70, H - 66),
    ]
    nets = "".join('<g transform="%s">%s</g>' % (t, _network(c)) for t in corners)

    # one badge per level, joined like a chain of neurons
    n = len(levels)
    gap = 44
    x0 = CX - gap * (n - 1) / 2
    yb = 536
    # a gradient stroke on a perfectly level line draws nothing (its box has no
    # height), so the rules on the certificate are thin rectangles instead
    badges = ['<rect x="%g" y="%g" width="%g" height="3" rx="1.5" fill="url(#cg-line)"/>'
              % (x0, yb - 1.5, gap * (n - 1))]
    for i in range(n):
        t = i / max(1, n - 1)
        bx = x0 + gap * i
        badges.append('<circle cx="%g" cy="%g" r="16" data-mix="%.4f" fill="%s" stroke="#FFFFFF" stroke-width="2.5"/>'
                      % (bx, yb, t, _mix(c, t)))
        badges.append(_text(bx, yb + 4.6, str(i + 1), "ct-badge"))

    body = [
        '<rect width="%d" height="%d" fill="#FFFDF8"/>' % (W, H),
        '<rect width="%d" height="%d" fill="url(#cg-dots)"/>' % (W, H),
        '<circle cx="80" cy="80" r="360" fill="url(#cg-wash1)"/>',
        '<circle cx="%d" cy="%d" r="380" fill="url(#cg-wash2)"/>' % (W - 80, H - 80),
        '<rect x="22" y="22" width="%d" height="%d" rx="18" fill="none" stroke="url(#cg-frame)" stroke-width="14"/>'
        % (W - 44, H - 44),
        '<rect x="46" y="46" width="%d" height="%d" rx="10" fill="none" data-stroke="1" stroke="%s" '
        'stroke-opacity=".5" stroke-width="1.5"/>' % (W - 92, H - 92, c[0]),
        nets,
        _logo(CX - 31, 62, 62),
        _text(CX, 146, "MSKPROD COMPUTING", "ct-brand"),
        _text(CX, 200, "CERTIFICATE OF ACHIEVEMENT", "ct-title", extra=' fill="url(#cg-line)"'),
        _text(CX, 240, "This is to certify that", "ct-lead"),
        _text(CX, 306, "Your name", "ct-name is-empty", ident="cert-name"),
        '<rect x="%g" y="324.75" width="600" height="2.5" rx="1.25" fill="url(#cg-line)"/>' % (CX - 300),
        '<rect x="%g" y="321" width="10" height="10" transform="rotate(45 %g 326)" data-fill="2" fill="%s"/>'
        % (CX - 5, CX, c[1]),
        _text(CX, 356, "", "ct-org", ident="cert-org"),
        _text(CX, 392, "has completed all %d levels and %d lessons of"
              % (n, sum(len(L["lessons"]) for L in levels)), "ct-lead"),
        _text(CX, 434, "Artificial Intelligence: Zero to Hero", "ct-course", extra=' data-fill="1" fill="%s"' % c[0]),
        _text(CX, 468, "from the history of AI through machine learning, neural networks, transformers and "
              "large language models", "ct-desc"),
        _text(CX, 490, "to generative AI, agents, AI engineering and responsible AI, and built an AI of their own.",
              "ct-desc"),
        "".join(badges),
        _text(CX, 582, "", "ct-avg", ident="cert-avg"),
        # date on the left, the seal in the middle, the course author on the right
        _text(290, 668, "", "ct-sig", ident="cert-date"),
        '<line x1="190" y1="682" x2="390" y2="682" stroke="#94A3B8" stroke-width="1.2"/>',
        _text(290, 702, "Date", "ct-label"),
        _text(290, 724, "", "ct-no", ident="cert-no"),
        _seal(CX, 664, c),
        _text(833, 668, "Asma Kethiri", "ct-sig"),
        '<line x1="733" y1="682" x2="933" y2="682" stroke="#94A3B8" stroke-width="1.2"/>',
        _text(833, 702, "Course author, MskProd Computing", "ct-label"),
        _text(833, 724, "mskprod.org/ai", "ct-no"),
        # shown until every quiz is passed
        '<g id="cert-mark" class="ct-mark">'
        '<text x="%g" y="%g" text-anchor="middle" transform="rotate(-16 %g %g)" class="ct-mark-big">PREVIEW</text>'
        '<text x="%g" y="%g" text-anchor="middle" transform="rotate(-16 %g %g)" class="ct-mark-sub">'
        'Pass every lesson quiz to unlock</text></g>' % (CX, 430, CX, 400, CX, 476, CX, 400),
    ]
    return ('<svg class="cert-svg" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" role="img" '
            'aria-labelledby="cert-svg-title"><title id="cert-svg-title">Certificate of achievement for '
            'Artificial Intelligence: Zero to Hero</title>%s%s</svg>' % (W, H, defs, "".join(body)))


def _levels():
    from content.ai_course import UNITS
    out = []
    for u in UNITS:
        out.append({
            "title": u.title,
            "lessons": [{"id": "ai/%s" % t.slug, "t": t.title, "u": "/ai/%s/" % t.slug} for t in u.topics],
        })
    return out


def build(register, add_search):
    levels = _levels()
    data = {"pass": PASS, "levels": levels, "themes": {k: list(c) for k, _, c in THEMES}}
    swatches = "".join(
        '<label class="cert-swatch"><input type="radio" name="cert-theme" value="%s"%s>'
        '<span class="cert-chip" style="background:linear-gradient(135deg,%s,%s,%s)"></span>'
        '<span class="cert-swatch-name">%s</span></label>'
        % (k, " checked" if i == 0 else "", c[0], c[1], c[2], esc(name))
        for i, (k, name, c) in enumerate(THEMES))
    trail = [("Home", "/"), ("AI", "/ai/"), ("Certificate", None)]
    body = """<div class="wrap">
  %s
  <header class="section-head cert-head">
    <h1>%s Your AI certificate</h1>
    <p class="lead">%s</p>
  </header>
  <noscript><p class="muted">The certificate reads your saved quiz scores using JavaScript, so it needs
  JavaScript switched on. Every lesson in the course works without it.</p></noscript>
  <div id="cert" class="cert-app">
    <div class="card cert-status" id="cert-status" role="status" aria-live="polite">
      <p class="muted">Checking your quiz scores.</p>
    </div>
    <div class="card cert-form">
      <h2>Make it yours</h2>
      <div class="cert-fields">
        <div class="cert-field cert-field-wide">
          <label for="cert-in-name">Your name, as it should appear</label>
          <input id="cert-in-name" type="text" maxlength="60" autocomplete="name" spellcheck="false">
        </div>
        <div class="cert-field cert-field-wide">
          <label for="cert-in-org">School, class or club (optional)</label>
          <input id="cert-in-org" type="text" maxlength="70" autocomplete="organization">
        </div>
        <div class="cert-field">
          <label for="cert-in-date">Date</label>
          <input id="cert-in-date" type="date">
        </div>
      </div>
      <fieldset class="cert-themes">
        <legend>Colours</legend>
        <div class="cert-swatches">%s</div>
      </fieldset>
      <label class="cert-check"><input id="cert-in-avg" type="checkbox"> Show my average quiz score</label>
      <div class="btn-row">
        <button class="btn btn-primary" id="cert-print" type="button" disabled>%s Print or save as PDF</button>
      </div>
      <p class="cert-hint" id="cert-hint"></p>
    </div>
  </div>
</div>
<div class="cert-print-area">
  <div class="wrap"><div class="cert-sheet" id="cert-sheet">%s</div></div>
</div>
<div class="wrap">
  <section class="cert-progress" aria-labelledby="cert-progress-h">
    <h2 id="cert-progress-h">Your lessons</h2>
    <div class="cert-levels" id="cert-levels"></div>
  </section>
  <div class="wrap-narrow" style="width:100%%;margin-inline:auto">
    <article class="prose" style="padding-bottom:var(--sp-8)">%s</article>
  </div>
</div>
<script type="application/json" id="cert-data">%s</script>""" % (
        crumbs(trail), ico("i-trophy"), esc(LEAD), swatches, ico("i-download"),
        certificate_svg(levels), markup.render(FOOT),
        json.dumps(data, separators=(",", ":")).replace("</", "<\\/"))
    path = "/ai/certificate/"
    write(path, layout(
        title="AI Course Certificate", description=LEAD, path=path, body=body,
        active="/ai/",
        extra_head='<link rel="stylesheet" href="/assets/css/certificate.css">',
        scripts=["/assets/js/certificate.js"],
        jsonld=[crumbs_ld(trail)]))
    register(path, 0.5, "monthly")
    add_search("Your AI certificate", path,
               "Artificial Intelligence: Zero to Hero",
               "certificate print award ai course zero to hero pdf name")
