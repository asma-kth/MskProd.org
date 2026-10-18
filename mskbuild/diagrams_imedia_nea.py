"""Diagrams for the Creative iMedia coursework units, R094 and R097.

R094 and R097 are internally assessed set assignments, so these pictures show
the work itself: a visual identity developing from three concepts into a style
guide, a poster annotated with the conventions it follows, one master file
exported three ways, a navigation diagram, a screen built in three passes, and
the shape of a review that scores.

The worked examples use two invented clients, deliberately unlike any OCR set
assignment: Spokes, a community bike repair workshop (R094), and Castle Hill
Community Garden's touchscreen visitor guide (R097). They show the quality of
each piece of evidence without answering anybody's real brief.

Brand colours in the Spokes figures are fixed values rather than theme
variables, because a colour palette that changed with dark mode would not be a
colour palette. Every piece of text on them has been chosen to keep its
contrast in both themes.
"""
from .diagrams import (diagram, TEAL, TEAL_SOFT, LILAC, LILAC_SOFT, WARN,
                       WARN_SOFT, FILL, LINE, MUTED)
from .svg import figure, box, text, line, path, circle, chip, marker, notes

FILL2 = "var(--dg-fill-2)"
INK = "var(--dg-text)"

# The Spokes palette, as the style guide defines it.
GREEN = "#1F6F50"
ORANGE = "#F28C28"
TARMAC = "#2B2F33"
PAPER = "#F7F4EC"


def _wheel(cx, cy, r, stroke, w=2.0, spokes=8, fill="none"):
    """A bicycle wheel: rim, hub and spokes."""
    out = [circle(cx, cy, r, fill=fill, stroke=stroke, w=w),
           circle(cx, cy, max(1.5, r * 0.12), fill=stroke, stroke=stroke, w=0)]
    import math
    for i in range(spokes):
        a = math.pi * 2 * i / spokes
        out.append(line(cx, cy, cx + r * 0.92 * math.cos(a),
                        cy + r * 0.92 * math.sin(a), stroke=stroke,
                        w=max(0.8, w * 0.5)))
    return "".join(out)


def _bike(x, y, s, stroke, w=2.2):
    """A side-on bicycle whose rear wheel is centred on (x, y), scaled by s."""
    r = 22 * s
    fx = x + 64 * s
    out = [_wheel(x, y, r, stroke, w, spokes=10),
           _wheel(fx, y, r, stroke, w, spokes=10)]
    seat = (x + 22 * s, y - 34 * s)
    head = (x + 54 * s, y - 32 * s)
    crank = (x + 28 * s, y)
    out.append(path("M%.1f %.1f L%.1f %.1f L%.1f %.1f L%.1f %.1f Z"
                    % (x, y, seat[0], seat[1], head[0], head[1], crank[0],
                       crank[1]), stroke=stroke, w=w))
    out.append(path("M%.1f %.1f L%.1f %.1f" % (x, y, crank[0], crank[1]),
                    stroke=stroke, w=w))
    out.append(path("M%.1f %.1f L%.1f %.1f" % (head[0], head[1], fx, y),
                    stroke=stroke, w=w))
    out.append(path("M%.1f %.1f l-7 -6 l12 0" % (seat[0], seat[1]),
                    stroke=stroke, w=w))
    out.append(path("M%.1f %.1f l-4 -9 l9 -2" % (head[0], head[1]),
                    stroke=stroke, w=w))
    out.append(circle(crank[0], crank[1], 5 * s, fill="none", stroke=stroke,
                      w=w * 0.8))
    return "".join(out)


def _badge(cx, cy, r, ring=GREEN, mark="#FFFFFF", accent=ORANGE, spokes=6):
    """The Spokes logo mark: a wheel inside a solid badge, with one orange spoke."""
    import math
    out = [circle(cx, cy, r, fill=ring, stroke=ring, w=0),
           circle(cx, cy, r * 0.66, fill="none", stroke=mark, w=max(1.2, r * 0.1))]
    for i in range(spokes):
        a = math.pi * 2 * i / spokes - math.pi / 2
        out.append(line(cx, cy, cx + r * 0.62 * math.cos(a),
                        cy + r * 0.62 * math.sin(a),
                        stroke=accent if i == 1 else mark,
                        w=max(1.0, r * (0.09 if i == 1 else 0.06))))
    out.append(circle(cx, cy, r * 0.14, fill=accent, stroke=accent, w=0))
    return "".join(out)


def _wordmark(x, y, size, fill=TARMAC, sub=True, anchor="start"):
    out = [text(x, y, "spokes", size, 800, anchor=anchor, fill=fill)]
    if sub:
        out.append(text(x, y + size * 0.62, "BIKE KITCHEN", size * 0.34, 750,
                        anchor=anchor, fill=fill))
    return "".join(out)


# ============================================================ task maps

@diagram("r094-tasks-map")
def _r094_tasks():
    """R094's three topic areas, and the two tasks that assess them."""
    body = [text(380, 22, "R094: three topic areas, assessed through two tasks",
                 12, 650, fill=MUTED)]
    TAS = [("TA1", "Develop visual identity", TEAL, TEAL_SOFT),
           ("TA2", "Plan digital graphics for products", TEAL, TEAL_SOFT),
           ("TA3", "Create visual identity and digital graphics", LILAC,
            LILAC_SOFT)]
    for i, (k, v, tone, soft) in enumerate(TAS):
        y = 50 + i * 74
        body.append(box(24, y, 250, 58, None, fill=soft, stroke=tone, r=8))
        body.append(text(38, y + 24, k, 11, 750, anchor="start", fill=tone))
        body.append(text(38, y + 43, v, 9.8, 600, anchor="start"))
    TASKS = [(46, 116, "TASK 1", "design and plan", TEAL, TEAL_SOFT,
              ["client needs and audience", "design concepts",
               "concepts justified", "visualisation diagram",
               "asset table, licences", "other planning documents"]),
             (176, 96, "TASK 2", "create and export", LILAC, LILAC_SOFT,
              ["the identity, built", "the graphic, built",
               "a range of techniques", "saved and exported"])]
    for y, h, name, sub, tone, soft, items in TASKS:
        body.append(box(400, y, 336, h, None, fill=soft, stroke=tone, r=8))
        body.append(text(414, y + 22, name, 11, 750, anchor="start", fill=tone))
        body.append(text(472, y + 22, sub, 9.8, 600, anchor="start", fill=MUTED))
        for j, item in enumerate(items):
            col, row = j % 2, j // 2
            body.append(text(414 + col * 164, y + 44 + row * 20, "\u2022 " + item,
                             9.2, 520, anchor="start"))
    body.append(path("M274 79 L396 92", stroke=TEAL, w=1.8, arrow=True,
                     marker="ah-accent"))
    body.append(path("M274 147 L396 122", stroke=TEAL, w=1.8, arrow=True,
                     marker="ah-accent"))
    body.append(path("M274 159 L396 214", stroke=LILAC, w=1.6, dash="5 4",
                     arrow=True, marker="ah-alt"))
    body.append(path("M274 227 L396 236", stroke=LILAC, w=1.8, arrow=True,
                     marker="ah-alt"))
    body.append(text(330, 200, "applied", 9, 650, fill=LILAC))
    body.append(box(24, 288, 712, 44, None, fill=WARN_SOFT, stroke=WARN, r=8))
    body.append(text(380, 306, "Task 1 is 20 of the 50 marks and Task 2 the other "
                     "30, on OCR's current recording sheet.", 10, 650, fill=WARN))
    body.append(text(380, 323, "Your own assignment and its marking grid are what "
                     "count: check them with your teacher.", 9.6, 500, fill=INK))
    desc = ("How R094 Visual identity and digital graphics is assessed. Its "
            "three topic areas are TA1, develop visual identity; TA2, plan "
            "digital graphics for products; and TA3, create visual identity and "
            "digital graphics. Task 1, design and plan, assesses TA1 and the "
            "planning in TA2: the client's needs and audience, design concepts, "
            "the justification of those concepts, a visualisation diagram, an "
            "asset table with licences and any other planning documents. Task "
            "2, create and export, assesses TA3, applying what TA2 teaches about "
            "the properties of digital graphics: the identity and the graphic "
            "built in software with a range of techniques, then saved and "
            "exported properly. On OCR's current recording sheet Task 1 is worth "
            "20 of the 50 marks and Task 2 the other 30, but your own assignment "
            "and its marking grid are what count, so check them with your "
            "teacher.")
    return figure("r094-map", 760, 344, "".join(body),
                  "R094 topic areas and tasks", desc,
                  "Task 1 designs the identity and plans the graphic. Task 2 "
                  "builds them.")


@diagram("r097-tasks-map")
def _r097_tasks():
    """R097's three topic areas, one task each."""
    body = [text(380, 22, "R097: three topic areas, three tasks, in order", 12,
                 650, fill=MUTED)]
    ROWS = [("TASK 1", "TA1 Plan interactive digital media", TEAL, TEAL_SOFT,
             ["client requirements and audience", "the product and its structure",
              "navigation diagram", "wireframes for each screen",
              "asset table, sources, licences"]),
            ("TASK 2", "TA2 Create interactive digital media", LILAC, LILAC_SOFT,
             ["assets prepared and optimised", "structure and navigation built",
              "interactive features working", "content and styling",
              "saved and exported to run"]),
            ("TASK 3", "TA3 Review interactive digital media", TEAL, TEAL_SOFT,
             ["test plan and results", "users testing real tasks",
              "review against the brief", "strengths and weaknesses",
              "improvements, further development"])]
    for i, (name, ta, tone, soft, items) in enumerate(ROWS):
        x = 24 + i * 242
        body.append(box(x, 46, 228, 216, None, fill=soft, stroke=tone, r=8))
        body.append(text(x + 114, 70, name, 11.5, 750, fill=tone))
        body.append(text(x + 114, 88, ta, 9.4, 600, fill=MUTED))
        for j, s in enumerate(items):
            body.append(box(x + 10, 100 + j * 31, 208, 26, None, fill=FILL,
                            stroke=tone, r=4))
            body.append(text(x + 114, 117 + j * 31, s, 9.4, 550))
        if i < 2:
            body.append(line(x + 228, 154, x + 240, 154, stroke=LINE, w=1.6,
                             arrow=True))
    body.append(box(24, 274, 712, 40, None, fill=WARN_SOFT, stroke=WARN, r=8))
    body.append(text(380, 299, "Each task builds on the last: the plan in Task 1 "
                     "is what Task 3 tests and reviews against.", 10.2, 650,
                     fill=WARN))
    desc = ("How R097 Interactive digital media is assessed: three topic areas, "
            "each with its own task, done in order. Task 1 covers TA1, plan "
            "interactive digital media: the client requirements and audience, "
            "the product and its structure, a navigation diagram, wireframes for "
            "each screen, and an asset table with sources and licences. Task 2 "
            "covers TA2, create interactive digital media: assets prepared and "
            "optimised, the structure and navigation built, interactive "
            "features working, content and styling, and the product saved and "
            "exported so it runs. Task 3 covers TA3, review interactive digital "
            "media: a test plan and its results, users testing real tasks, a "
            "review against the brief, strengths and weaknesses, and "
            "improvements and further development. Each task builds on the "
            "last, because the plan made in Task 1 is what Task 3 tests and "
            "reviews against.")
    return figure("r097-map", 760, 326, "".join(body),
                  "R097 topic areas and tasks", desc,
                  "Plan, create, review: and the review measures the product "
                  "against the plan.")


# ===================================================== R094: the identity

@diagram("r094-logo-development")
def _logo_dev():
    """Three genuinely different concepts, one chosen and refined."""
    body = [text(380, 22, "Logo development: three different concepts, one "
                 "chosen, then refined", 12, 650, fill=MUTED)]
    CON = [("A  WORDMARK", "name only; wheel as the 'o'",
            "+ simple  − no symbol alone"),
           ("B  COMBINATION", "badge beside the name",
            "+ works small, one colour"),
           ("C  ABSTRACT", "two wheels make a leaf",
            "+ eco  − not clearly bikes")]
    for i, (k, v, verdict) in enumerate(CON):
        x = 24 + i * 176
        chosen = i == 1
        body.append(box(x, 44, 164, 170, None, fill=FILL,
                        stroke=TEAL if chosen else LINE, r=8))
        body.append(text(x + 82, 64, k, 10, 750, fill=TEAL if chosen else MUTED))
        # Logos are shown on paper, the background they were designed for, so
        # the dark wordmark stays visible in the dark theme as well.
        body.append(box(x + 10, 80, 144, 72, None, fill=PAPER, stroke=LINE, r=6))
        cx, cy = x + 82, 118
        if i == 0:
            body.append(text(cx - 19, cy + 10, "sp", 30, 800, anchor="end",
                             fill=TARMAC))
            body.append(_wheel(cx - 6, cy + 1, 11, ORANGE, w=2.4, spokes=6))
            body.append(text(cx + 7, cy + 10, "kes", 30, 800, anchor="start",
                             fill=TARMAC))
        elif i == 1:
            body.append(_badge(cx - 44, cy, 24, spokes=12))
            body.append(_wordmark(cx - 14, cy + 4, 22))
        else:
            body.append(circle(cx - 12, cy, 26, fill="none", stroke=GREEN, w=3))
            body.append(circle(cx + 12, cy, 26, fill="none", stroke=GREEN, w=3))
            body.append(path("M%.1f %.1f A26 26 0 0 1 %.1f %.1f A26 26 0 0 1 %.1f %.1f Z"
                             % (cx, cy - 23.1, cx, cy + 23.1, cx, cy - 23.1),
                             stroke=ORANGE, w=0, fill=ORANGE))
        body.append(text(x + 82, 168, v, 9.2, 500, fill=MUTED))
        body.append(text(x + 82, 196, verdict, 9, 650,
                         fill=TEAL if chosen else INK))
    body.append(path("M282 214 L282 236 L644 236 L644 218", stroke=TEAL, w=1.6,
                     dash="5 4", arrow=True, marker="ah-accent"))
    body.append(chip(463, 236, "B chosen, then refined", size=9.6))
    # Refinement panel.
    body.append(box(552, 44, 184, 170, None, fill=TEAL_SOFT, stroke=TEAL, r=8))
    body.append(text(644, 64, "REFINED", 10, 750, fill=TEAL))
    body.append(box(556, 76, 176, 84, None, fill=PAPER, stroke=LINE, r=6))
    body.append(_badge(604, 108, 22))
    body.append(text(604, 149, "6 spokes, not 12", 8.8, 600, fill=TARMAC))
    body.append(_badge(662, 102, 10))
    body.append(text(662, 126, "32 px", 8.8, 600, fill=TARMAC))
    body.append(_badge(704, 102, 10, ring=TARMAC, mark="#FFFFFF", accent="#FFFFFF"))
    body.append(text(704, 126, "1 colour", 8.8, 600, fill=TARMAC))
    body.append(text(644, 176, "detail removed until it", 9, 500, fill=MUTED))
    body.append(text(644, 190, "survives at favicon size", 9, 500, fill=MUTED))
    body.append(box(24, 254, 712, 58, None, fill=FILL, stroke=LINE, r=8))
    body.append(text(380, 276, "Each concept is judged against the brief, not "
                     "against taste: brand values, audience, and where the logo "
                     "has to work.", 10.2, 700, fill=TEAL))
    body.append(text(380, 296, "The rejected concepts stay in your evidence. They "
                     "show the alternatives you explored.", 9.8, 500, fill=MUTED))
    desc = ("Logo development for an invented client, Spokes, a community bike "
            "repair workshop. Three genuinely different concepts are shown. "
            "Concept A is a wordmark: the name 'spokes' with a bicycle wheel "
            "standing in for the letter o; it is simple but has no symbol that "
            "could be used on its own. Concept B is a combination mark: a round "
            "green badge containing a white wheel with one orange spoke, beside "
            "the name 'spokes' and the words 'bike kitchen'; it works small and "
            "in one colour. Concept C is an abstract mark: two overlapping "
            "wheels whose overlap forms an orange leaf shape, suggesting "
            "sustainability, but it is hard to read as bikes. Concept B is "
            "chosen and refined: the spokes are reduced from twelve to six, and "
            "it is checked at 32 pixels and in a single colour, removing detail "
            "until it survives at favicon size. Each concept is judged against "
            "the brief, the brand values, the audience and where the logo has "
            "to work, not against taste, and the rejected concepts stay in the "
            "evidence because they show the alternatives explored.")
    return figure("r094-logos", 760, 324, "".join(body),
                  "Developing a logo from three concepts", desc,
                  "Three different ideas, judged against the brief, then one "
                  "refined until it works everywhere it has to.")


@diagram("r094-style-guide")
def _style_guide():
    """A one-page style guide: logo, clear space, palette, type, do and don't."""
    body = [text(380, 22, "A one-page style guide: the visual identity, defined "
                 "so anyone can apply it", 12, 650, fill=MUTED)]
    # Logo and clear space.
    body.append(box(24, 40, 300, 160, None, fill=FILL, stroke=LINE, r=8))
    body.append(text(36, 60, "LOGO AND CLEAR SPACE", 10, 750, anchor="start",
                     fill=TEAL))
    body.append(box(56, 78, 236, 92, None, fill=PAPER, stroke=WARN, r=2,
                    dash="4 3"))
    body.append(_badge(106, 124, 28))
    body.append(_wordmark(142, 128, 28))
    body.append(text(174, 188, "clear space = badge radius; minimum width 30 mm",
                     8.8, 500, fill=MUTED))
    # Palette.
    body.append(box(336, 40, 400, 160, None, fill=FILL, stroke=LINE, r=8))
    body.append(text(348, 60, "COLOUR PALETTE", 10, 750, anchor="start",
                     fill=TEAL))
    PAL = [("Spokes Green", GREEN, "#1F6F50", "31, 111, 80", "#FFFFFF"),
           ("Chain Orange", ORANGE, "#F28C28", "242, 140, 40", TARMAC),
           ("Tarmac", TARMAC, "#2B2F33", "43, 47, 51", "#FFFFFF"),
           ("Paper", PAPER, "#F7F4EC", "247, 244, 236", TARMAC)]
    for i, (name, col, hexv, rgb, ink) in enumerate(PAL):
        x = 348 + i * 96
        body.append(box(x, 72, 88, 84, None, fill=col, stroke=LINE, r=6))
        body.append(text(x + 8, 92, name, 9.2, 750, anchor="start", fill=ink))
        body.append(text(x + 8, 120, hexv, 9.4, 700, anchor="start", fill=ink,
                         mono=True))
        body.append(text(x + 8, 138, rgb, 8.4, 500, anchor="start", fill=ink))
    body.append(text(536, 178, "green leads; orange only for highlights and "
                     "calls to action", 8.8, 500, fill=MUTED))
    # Typography.
    body.append(box(24, 212, 360, 120, None, fill=FILL, stroke=LINE, r=8))
    body.append(text(36, 232, "TYPOGRAPHY", 10, 750, anchor="start", fill=TEAL))
    body.append(text(36, 262, "Fix it. Ride it.", 22, 800, anchor="start",
                     fill=INK))
    body.append(text(372, 262, "Headings: Poppins Bold", 9.2, 600,
                     anchor="end", fill=MUTED))
    body.append(text(36, 288, "Free repair sessions every Saturday.", 12, 400,
                     anchor="start", fill=INK))
    body.append(text(36, 306, "Body: Source Sans 3 Regular, 11 pt minimum", 9.2,
                     600, anchor="start", fill=MUTED))
    body.append(text(36, 322, "Both free for commercial use under the SIL Open "
                     "Font Licence", 8.8, 500, anchor="start", fill=MUTED))
    # Do and don't.
    body.append(box(396, 212, 340, 120, None, fill=FILL, stroke=LINE, r=8))
    body.append(text(408, 232, "NEVER", 10, 750, anchor="start", fill=WARN))
    # stretched
    body.append('<g transform="translate(446 284) scale(1.6 0.8)">%s</g>'
                % _badge(0, 0, 18))
    body.append(text(446, 322, "stretch it", 9, 650, fill=WARN))
    # recoloured
    body.append(_badge(560, 280, 18, ring="#7A3EA8", mark="#FFFFFF",
                       accent="#53C1E8"))
    body.append(text(560, 322, "recolour it", 9, 650, fill=WARN))
    # busy background
    for k in range(7):
        body.append(line(640 + k * 12, 252, 652 + k * 12, 306, stroke=ORANGE,
                         w=5))
    body.append(_badge(676, 280, 18))
    body.append(text(676, 322, "put it on clutter", 9, 650, fill=WARN))
    for x in (446, 560, 676):
        body.append(path("M%d 238 l9 9 m0 -9 l-9 9" % (x + 30), stroke=WARN,
                         w=2.2))
    desc = ("A one-page style guide for the invented client Spokes, a community "
            "bike repair workshop. The logo, a green badge containing a white "
            "wheel with one orange spoke beside the name 'spokes, bike kitchen', "
            "is shown inside a dashed clear-space box, with the rule: keep clear "
            "space equal to the badge's radius, and never use it narrower than "
            "30 millimetres. The colour palette has four colours, each with its "
            "hex code and RGB values: Spokes Green, hex 1F6F50, RGB 31, 111, 80; "
            "Chain Orange, hex F28C28, RGB 242, 140, 40; Tarmac, hex 2B2F33, RGB "
            "43, 47, 51; and Paper, hex F7F4EC, RGB 247, 244, 236. Green leads, "
            "and orange is used only for highlights and calls to action. Typography: headings in Poppins Bold, shown "
            "with the slogan 'Fix it. Ride it.', and body text in Source Sans 3 "
            "Regular at 11 point minimum, both free for commercial use under the "
            "SIL Open Font Licence. A 'never' panel shows three misuses, each "
            "crossed out: the logo stretched, the logo recoloured in purple and "
            "blue, and the logo placed on a cluttered striped background.")
    return figure("r094-style", 760, 344, "".join(body),
                  "A visual identity style guide", desc,
                  "Exact values, named fonts with their licences, and rules for "
                  "using the logo: that is what makes an identity consistent.")


# =============================================== R094: properties, layout

@diagram("r094-graphic-properties")
def _properties():
    """Pixels, print size and resolution, worked out properly."""
    body = [text(380, 22, "Resolution: how many pixels a graphic needs depends "
                 "on where it is going", 12, 650, fill=MUTED)]
    # Panel 1: A4 at 300 dpi.
    body.append(box(24, 40, 230, 236, None, fill=FILL, stroke=LINE, r=8))
    body.append(text(139, 60, "PRINT: A4 POSTER", 10, 750, fill=TEAL))
    body.append(box(94, 74, 90, 127, None, fill=PAPER, stroke=TARMAC, r=2))
    body.append(line(84, 74, 84, 201, stroke=MUTED, w=1, arrow=True))
    body.append(text(76, 142, "297 mm", 8.8, 600, anchor="end", fill=MUTED))
    body.append(line(94, 212, 184, 212, stroke=MUTED, w=1, arrow=True))
    body.append(text(139, 226, "210 mm", 8.8, 600, fill=MUTED))
    body.append(text(139, 246, "at 300 dpi:", 9.4, 600, fill=INK))
    body.append(text(139, 264, "2480 × 3508 pixels", 10.4, 750, fill=TEAL))
    # Panel 2: the photo that is too small.
    body.append(box(266, 40, 230, 236, None, fill=WARN_SOFT, stroke=WARN, r=8))
    body.append(text(381, 60, "A 1200 × 800 PHOTO", 10, 750, fill=WARN))
    body.append(text(381, 84, "printed at 300 dpi:", 9.4, 600))
    body.append(text(381, 102, "102 × 68 mm", 10.4, 750, fill=INK))
    body.append(box(330, 112, 50, 34, None, fill=FILL, stroke=WARN, r=2))
    body.append(text(381, 166, "stretched to A4 width:", 9.4, 600))
    body.append(text(381, 184, "about 145 dpi, and soft", 10.4, 750, fill=WARN))
    for k in range(6):
        for j in range(4):
            body.append('<rect x="%d" y="%d" width="10" height="10" fill="%s" '
                        'opacity="0.8"/>' % (330 + k * 12, 196 + j * 12,
                                             GREEN if (k + j) % 2 else ORANGE))
    body.append(text(381, 268, "enlarging cannot add detail", 9.2, 650,
                     fill=WARN))
    # Panel 3: screen sizes.
    body.append(box(508, 40, 228, 236, None, fill=FILL, stroke=LINE, r=8))
    body.append(text(622, 60, "SCREEN: PIXELS ONLY", 10, 750, fill=LILAC))
    SIZES = [("Square social post", "1080 × 1080"),
             ("Story or reel", "1080 × 1920"),
             ("Web banner", "1500 × 500"),
             ("Full-screen slide", "1920 × 1080")]
    for i, (k, v) in enumerate(SIZES):
        y = 74 + i * 38
        body.append(box(520, y, 204, 32, None, fill=LILAC_SOFT, stroke=LILAC, r=5))
        body.append(text(530, y + 20, k, 9.4, 600, anchor="start"))
        body.append(text(714, y + 20, v, 9.4, 750, anchor="end", fill=LILAC))
    body.append(text(622, 244, "dpi means nothing on a screen:", 9.2, 600,
                     fill=MUTED))
    body.append(text(622, 260, "only the pixel dimensions count", 9.2, 600,
                     fill=MUTED))
    body.append(box(24, 290, 712, 52, None, fill=TEAL_SOFT, stroke=TEAL, r=8))
    body.append(text(380, 311, "pixels needed = print size in inches × dpi    "
                     "(inches = mm ÷ 25.4)", 10.6, 750, fill=TEAL))
    body.append(text(380, 330, "Work it out at the planning stage, so you "
                     "source images big enough before you need them.", 9.8, 500,
                     fill=INK))
    desc = ("Three panels on resolution. First, print: an A4 poster is 210 by "
            "297 millimetres, and at 300 dots per inch it needs 2480 by 3508 "
            "pixels. Second, a warning: a photograph of 1200 by 800 pixels "
            "printed at 300 dpi is only about 102 by 68 millimetres; stretched "
            "to the full width of A4 it drops to about 145 dpi and looks soft, "
            "because enlarging an image cannot add detail that was never "
            "captured. Third, screen: only pixel dimensions count, and dpi means "
            "nothing. Typical sizes are a square social post of 1080 by 1080, a "
            "story or reel of 1080 by 1920, a web banner of 1500 by 500 and a "
            "full-screen slide of 1920 by 1080. The formula: pixels needed "
            "equals print size in inches times dpi, where inches are "
            "millimetres divided by 25.4. Work it out at the planning stage, so "
            "that images big enough are sourced before they are needed.")
    return figure("r094-props", 760, 354, "".join(body),
                  "Resolution for print and for screen", desc,
                  "Print is measured in millimetres and dpi. Screen is measured "
                  "in pixels.")


@diagram("r094-poster-anatomy")
def _poster():
    """The finished poster, with the conventions it follows marked on it."""
    body = [text(380, 22, "Layout conventions, marked on the finished poster",
                 12, 650, fill=MUTED)]
    X, Y, W, H = 60, 40, 262, 370
    # Bleed and safe area.
    body.append(box(X - 8, Y - 8, W + 16, H + 16, None, fill="none", stroke=WARN,
                    r=2, dash="3 3"))
    body.append(box(X, Y, W, H, None, fill=PAPER, stroke=TARMAC, r=0))
    body.append(box(X + 14, Y + 14, W - 28, H - 28, None, fill="none",
                    stroke=LILAC, r=0, dash="2 4"))
    # Grid columns (faint).
    for k in (1, 2):
        gx = X + 14 + (W - 28) * k / 3.0
        body.append(line(gx, Y + 14, gx, Y + H - 14, stroke=LILAC, w=0.6,
                         dash="2 5"))
    # Top band with logo.
    body.append('<rect x="%d" y="%d" width="%d" height="58" fill="%s"/>'
                % (X, Y, W, GREEN))
    body.append(_badge(X + 40, Y + 29, 18, ring=PAPER, mark=GREEN, accent=ORANGE))
    body.append(_wordmark(X + 66, Y + 31, 20, fill=PAPER))
    # Headline.
    body.append(text(X + 22, Y + 100, "FREE REPAIR", 30, 850, anchor="start",
                     fill=TARMAC))
    body.append(text(X + 22, Y + 132, "SATURDAYS", 30, 850, anchor="start",
                     fill=ORANGE))
    # Focal image.
    body.append(_bike(X + 66, Y + 222, 1.55, GREEN, w=3))
    # Details.
    body.append(text(X + 22, Y + 280, "Every Saturday, 10am–2pm", 13, 750,
                     anchor="start", fill=TARMAC))
    body.append(text(X + 22, Y + 300, "Bring your bike. Learn to fix it.", 11,
                     500, anchor="start", fill=TARMAC))
    body.append(box(X + 22, Y + 314, 150, 30, None, fill=ORANGE, stroke=ORANGE,
                    r=15))
    body.append(text(X + 97, Y + 334, "Unit 4, Mill Lane", 11, 800,
                     fill=TARMAC))
    body.append(text(X + W - 22, Y + 348, "Fix it. Ride it.", 9.5, 700,
                     anchor="end", fill=GREEN))
    # Markers.
    MARKS = [(X + W - 14, Y + 70), (X + 200, Y + 172), (X + 14, Y + 252),
             (X + 190, Y + 318), (X + W - 16, Y + 16), (X + W + 8, Y + H - 40)]
    for n, (mx, my) in enumerate(MARKS, 1):
        body.append(marker(n, mx, my))
    body.append(notes(354, 62, 62, 382, [
        ("Hierarchy: the headline is largest, in the",
         "palette's two strongest colours, read first"),
        ("Focal point: the bike sits on the lower third",
         "line and leads the eye to the details"),
        ("Alignment: everything sits on a three-column",
         "grid, left-aligned to the same margin"),
        ("Call to action: what, when and where, with",
         "white space around it so it stands out"),
        ("Identity: logo, colours and fonts all come",
         "from the style guide, used consistently"),
        ("Print: 3 mm bleed beyond the trim (dashed)",
         "and a safe area inside it for all text")]))
    desc = ("A finished A4 poster for the invented client Spokes, advertising "
            "free repair Saturdays, with six numbered annotations explaining "
            "the layout conventions it follows. One, hierarchy: the headline, "
            "'Free repair Saturdays', is the largest element, in the palette's "
            "two strongest colours, so it is read first. Two, focal point: a "
            "drawing of a bicycle sits on the lower third line and leads the eye "
            "down to the details. Three, alignment: every element sits on a "
            "three-column grid, left-aligned to the same margin. Four, call to "
            "action: 'Every Saturday, 10am to 2pm. Bring your bike. Learn to fix "
            "it.' and the address, Unit 4, Mill Lane, in an orange pill, with "
            "white space around them so they stand out. Five, identity: the "
            "logo in the green band at the top, the colours and the fonts all "
            "come from the style guide. Six, print: a dashed line shows 3 "
            "millimetres of bleed beyond the trim, and a dotted inner line the "
            "safe area that all text stays inside.")
    return figure("r094-poster", 760, 432, "".join(body),
                  "Layout conventions on a finished poster", desc,
                  "Every placement on the page is a decision you can explain.")


@diagram("r094-technique-evidence")
def _technique():
    """Evidence of one technique, as four annotated stages."""
    body = [text(380, 22, "Evidencing a technique: removing a background, "
                 "non-destructively", 12, 650, fill=MUTED)]
    STAGES = [("1  ORIGINAL", "own photo, 4000 × 3000"),
              ("2  SELECTION", "quick selection, then refine edge"),
              ("3  LAYER MASK", "mask hides, nothing deleted"),
              ("4  PLACED", "on the poster, on its own layer")]
    for i, (k, v) in enumerate(STAGES):
        x = 24 + i * 180
        body.append(box(x, 40, 168, 176, None, fill=FILL, stroke=LINE, r=8))
        body.append(text(x + 84, 60, k, 10, 750, fill=TEAL))
        px, py = x + 14, 72
        if i in (0, 1):
            for k2 in range(7):
                body.append('<rect x="%d" y="%d" width="20" height="104" fill="%s"/>'
                            % (px + k2 * 20, py, "#C9B79C" if k2 % 2 else "#A8C3A0"))
        elif i == 2:
            for k2 in range(10):
                for j in range(7):
                    body.append('<rect x="%d" y="%d" width="14" height="15" '
                                'fill="%s"/>' % (px + k2 * 14, py + j * 15,
                                                 "#DDDDDD" if (k2 + j) % 2
                                                 else "#FFFFFF"))
        else:
            body.append('<rect x="%d" y="%d" width="140" height="104" fill="%s"/>'
                        % (px, py, PAPER))
            body.append('<rect x="%d" y="%d" width="140" height="22" fill="%s"/>'
                        % (px, py, GREEN))
        body.append(_bike(px + 30, py + 74, 0.95, TARMAC, w=2.4))
        if i == 1:
            body.append(box(px + 4, py + 28, 132, 72, None, fill="none",
                            stroke="#111111", r=4, dash="4 3"))
        body.append(text(x + 84, 196, v, 9, 550, fill=MUTED))
    for i in range(3):
        x = 24 + i * 180 + 168
        body.append(line(x + 1, 128, x + 11, 128, stroke=LINE, w=1.6, arrow=True))
    body.append(box(24, 230, 712, 64, None, fill=TEAL_SOFT, stroke=TEAL, r=8))
    body.append(text(380, 252, "For each technique, show the tool, the settings "
                     "and the result, and say why you used it.", 10.4, 700,
                     fill=TEAL))
    body.append(text(380, 272, "\"I used a layer mask rather than the eraser so "
                     "the background can be restored if the client changes "
                     "the crop.\"", 9.8, 500, fill=INK))
    desc = ("Four stages of one technique, removing the background from a "
            "photograph without destroying any pixels, each captured as "
            "evidence. One, the original: the student's own photo of a bicycle, "
            "4000 by 3000 pixels, against a striped background. Two, the "
            "selection: made with the quick selection tool and then refined at "
            "the edges, shown as a dashed outline. Three, the layer mask: the "
            "background is hidden by a mask, shown as a checkerboard of "
            "transparency, and nothing is deleted. Four, placed: the cut-out "
            "bike on the poster, on its own layer. For each technique, show the "
            "tool, the settings and the result, and say why it was used, for "
            "example: 'I used a layer mask rather than the eraser so the "
            "background can be restored if the client changes the crop.'")
    return figure("r094-tech", 760, 306, "".join(body),
                  "Evidencing a technique in stages", desc,
                  "Screenshots of the process, annotated, are the evidence that "
                  "you used the tools, and that you know why.")


@diagram("r094-export-settings")
def _exports():
    """One layered master, three exports, each set up for its destination."""
    body = [text(380, 22, "One layered master file, exported three ways for "
                 "three destinations", 12, 650, fill=MUTED)]
    body.append(box(24, 120, 176, 96, None, fill=LILAC_SOFT, stroke=LILAC, r=8))
    body.append(text(112, 142, "MASTER", 10.4, 750, fill=LILAC))
    body.append(text(112, 162, "spokes-poster-v07", 9.4, 650, mono=True))
    body.append(text(112, 180, "layers, masks, live text", 9, 500, fill=MUTED))
    body.append(text(112, 198, "never overwritten", 9, 650, fill=WARN))
    OUTS = [("PRINT", "spokes-poster-print-v07.pdf",
             ["A4 plus 3 mm bleed", "CMYK, 300 dpi", "fonts embedded"]),
            ("SOCIAL", "spokes-poster-social-1080.jpg",
             ["1080 × 1080 pixels", "RGB, compressed", "text resized to read"]),
            ("LOGO PACK", "spokes-logo-primary.svg + .png",
             ["SVG: any size", "PNG with transparency", "one-colour version"])]
    for i, (k, fname, items) in enumerate(OUTS):
        y = 40 + i * 92
        body.append(box(268, y, 468, 80, None, fill=FILL, stroke=TEAL, r=8))
        body.append(text(282, y + 22, k, 10.4, 750, anchor="start", fill=TEAL))
        body.append(text(370, y + 22, fname, 9.4, 650, anchor="start", mono=True))
        for j, s in enumerate(items):
            body.append(text(282 + j * 152, y + 54, "• " + s, 9.4, 520,
                             anchor="start"))
        body.append(path("M200 168 L264 %d" % (y + 40), stroke=TEAL, w=1.6,
                         arrow=True, marker="ah-accent"))
    body.append(box(24, 322, 712, 46, None, fill=WARN_SOFT, stroke=WARN, r=8))
    body.append(text(380, 342, "A naming convention that sorts, says what each "
                     "file is for, and never contains the word 'final'.", 10.2,
                     700, fill=WARN))
    body.append(text(380, 359, "Lower case, no spaces, a version number: "
                     "spokes-poster-v07, not 'poster FINAL new (2)'.", 9.6, 500,
                     fill=INK))
    desc = ("One layered master file, spokes-poster-v07, with its layers, masks "
            "and live text, which is never overwritten, exported three ways. "
            "For print: spokes-poster-print-v07.pdf, A4 plus 3 millimetres of "
            "bleed, CMYK at 300 dpi, with fonts embedded. For social media: "
            "spokes-poster-social-1080.jpg, 1080 by 1080 pixels, RGB and "
            "compressed, with the text resized so it can be read on a phone. A "
            "logo pack: spokes-logo-primary as an SVG that works at any size and "
            "a PNG with transparency, plus a one-colour version. Underneath, the "
            "naming rule: a convention that sorts, says what each file is for "
            "and never contains the word final; lower case, no spaces, and a "
            "version number, so spokes-poster-v07 rather than 'poster FINAL new "
            "(2)'.")
    return figure("r094-export", 760, 380, "".join(body),
                  "Saving and exporting for each destination", desc,
                  "Export settings come from the destination: print, screen or "
                  "any size.")


# ================================================== R097: product types

@diagram("r097-product-types")
def _product_types():
    """Interactive products, and the features that make each interactive."""
    body = [text(380, 22, "Interactive products: the user's input changes what "
                 "happens next", 12, 650, fill=MUTED)]
    P = [("Website", ["hyperlinks and menus", "forms and search",
                      "works on any screen"]),
         ("Mobile app", ["tab bar, gestures", "notifications",
                         "works offline"]),
         ("Information kiosk", ["large touch targets", "attract loop",
                                "resets when idle"]),
         ("E-learning", ["progress tracking", "quizzes with feedback",
                         "next and back"]),
         ("Interactive video", ["hotspots and choices", "branching paths",
                                "play, pause, captions"]),
         ("Game or quiz", ["controls and score", "levels, lives",
                           "instant feedback"])]
    for i, (name, feats) in enumerate(P):
        col, row = i % 3, i // 3
        x, y = 24 + col * 240, 40 + row * 132
        tone, soft = (TEAL, TEAL_SOFT) if (col + row) % 2 == 0 else (LILAC,
                                                                     LILAC_SOFT)
        body.append(box(x, y, 228, 120, None, fill=soft, stroke=tone, r=8))
        # A small screen glyph.
        if name in ("Mobile app",):
            body.append(box(x + 16, y + 16, 34, 58, None, fill=FILL, stroke=tone,
                            r=6))
            body.append(circle(x + 33, y + 66, 3, fill=tone, stroke=tone, w=0))
        elif name == "Information kiosk":
            body.append(box(x + 14, y + 14, 40, 46, None, fill=FILL, stroke=tone,
                            r=3))
            body.append(line(x + 34, y + 60, x + 34, y + 84, stroke=tone, w=3))
            body.append(line(x + 22, y + 86, x + 46, y + 86, stroke=tone, w=3))
        else:
            body.append(box(x + 12, y + 18, 46, 34, None, fill=FILL, stroke=tone,
                            r=3))
            body.append(line(x + 26, y + 58, x + 44, y + 58, stroke=tone, w=3))
            if name == "Interactive video":
                body.append(path("M%d %d l12 7 l-12 7 Z" % (x + 30, y + 28),
                                 stroke=tone, w=1, fill=tone))
            if name == "Game or quiz":
                body.append(text(x + 35, y + 41, "?", 16, 800, fill=tone))
        body.append(text(x + 70, y + 30, name.upper(), 10.2, 750,
                         anchor="start", fill=tone))
        for j, f in enumerate(feats):
            body.append(text(x + 70, y + 54 + j * 20, "• " + f, 9.4, 520,
                             anchor="start"))
    body.append(box(24, 306, 712, 40, None, fill=FILL, stroke=LINE, r=8))
    body.append(text(380, 331, "Choose the product from the client's purpose and "
                     "audience, then plan the features that product needs.",
                     10.2, 650, fill=TEAL))
    desc = ("Six kinds of interactive product and the features that make each "
            "interactive. A website: hyperlinks and menus, forms and search, and "
            "a layout that works on any screen. A mobile app: a tab bar and "
            "gestures, notifications, and working offline. An information "
            "kiosk: large touch targets, an attract loop, and resetting itself "
            "when idle. E-learning: progress tracking, quizzes with feedback, "
            "and next and back controls. Interactive video: hotspots and "
            "choices, branching paths, and play, pause and captions. A game or "
            "quiz: controls and a score, levels and lives, and instant feedback. "
            "The product is chosen from the client's purpose and audience, and "
            "then the features that product needs are planned.")
    return figure("r097-types", 760, 358, "".join(body),
                  "Types of interactive product", desc,
                  "Interactive means the user decides what happens next.")


@diagram("r097-garden-navigation")
def _garden_nav():
    """A hub and spoke navigation diagram for a touchscreen kiosk."""
    body = [text(380, 22, "Navigation diagram: Castle Hill Community Garden "
                 "visitor kiosk", 12, 650, fill=MUTED)]

    def home_tag(x, y):
        """The small 'H' tag marking a screen that carries a Home button."""
        return (box(x, y, 18, 16, None, fill=TEAL, stroke=TEAL, r=4)
                + text(x + 9, y + 12, "H", 9, 800, fill=FILL))

    body.append(box(24, 126, 108, 44, "Attract loop", fill=LILAC_SOFT,
                    stroke=LILAC, r=8, label_size=10.4, text_fill=LILAC))
    body.append(line(132, 148, 174, 148, stroke=LILAC, w=1.6, arrow=True,
                     marker="ah-alt"))
    body.append(text(153, 140, "tap", 9, 650, fill=LILAC))
    body.append(box(178, 122, 108, 52, None, fill=TEAL_SOFT, stroke=TEAL, r=8))
    body.append(text(232, 144, "HOME", 11, 750, fill=TEAL))
    body.append(text(232, 161, "the hub", 9, 500, fill=MUTED))
    SPOKES = ["Garden map", "What's growing", "Wildlife", "Events"]
    for i, s in enumerate(SPOKES):
        y = 44 + i * 50
        body.append(box(360, y, 128, 38, s, fill=FILL, stroke=TEAL, r=6,
                        label_size=10))
        body.append(home_tag(476, y - 6))
        body.append(path("M286 148 L%d %d" % (356, y + 19), stroke=TEAL, w=1.4,
                         arrow=True, marker="ah-accent"))
    # The quiz: a short linear sequence.
    body.append(box(360, 250, 110, 36, "Quiz: question 1", fill=FILL,
                    stroke=LILAC, r=6, label_size=9.4))
    body.append(home_tag(458, 244))
    body.append(path("M286 156 L356 266", stroke=LILAC, w=1.4, arrow=True,
                     marker="ah-alt"))
    prev = 470
    for i, s in enumerate(["Question 2", "Question 3", "Your score"]):
        x = 492 + i * 80
        body.append(line(prev, 268, x - 4, 268, stroke=LILAC, w=1.4, arrow=True,
                         marker="ah-alt"))
        body.append(box(x, 252, 64, 32, s, fill=FILL, stroke=LILAC, r=6,
                        label_size=9))
        body.append(home_tag(x + 52, 246))
        prev = x + 64
    body.append(box(552, 52, 184, 92, None, fill=FILL, stroke=LINE, r=8))
    body.append(home_tag(566, 66))
    body.append(text(592, 79, "Home button on this", 9.4, 650, anchor="start"))
    body.append(text(566, 100, "screen: one tap back to the", 9.4, 500,
                     anchor="start", fill=MUTED))
    body.append(text(566, 116, "hub from anywhere, including", 9.4, 500,
                     anchor="start", fill=MUTED))
    body.append(text(566, 132, "the quiz and the score", 9.4, 500,
                     anchor="start", fill=MUTED))
    body.append(path("M232 174 C 232 236, 78 236, 78 174", stroke=WARN, w=1.4,
                     dash="6 4", arrow=True))
    body.append(text(156, 244, "60 s with no touch: back to attract", 9.4, 650,
                     fill=WARN))
    body.append(box(24, 300, 712, 40, None, fill=FILL, stroke=LINE, r=8))
    body.append(text(380, 325, "Check it: every screen reachable, a route back "
                     "from each, nothing deeper than two taps except the quiz.",
                     10.2, 650, fill=TEAL))
    desc = ("A navigation diagram for an invented product, a touchscreen "
            "visitor guide for Castle Hill Community Garden. An attract loop "
            "plays until someone taps, which opens the Home screen, the hub. "
            "From Home, four spokes lead to Garden map, What's growing, Wildlife "
            "and Events, and a fifth starts a quiz, which runs in a short linear "
            "sequence: question 1, question 2, question 3, and a score screen. "
            "Every screen, including the quiz and the score, is tagged as "
            "carrying a Home button, so the visitor is always one tap from the "
            "hub. After 60 seconds without a touch, the kiosk returns to the "
            "attract loop for the next visitor. The check underneath: every "
            "screen can be reached, every screen has a route back, and nothing "
            "is deeper than two taps except the quiz.")
    return figure("r097-nav", 760, 352, "".join(body),
                  "A navigation diagram for a kiosk", desc,
                  "Every screen a box, every link an arrow, and the timeout "
                  "drawn as well.")


@diagram("r097-ui-conventions")
def _ui_conventions():
    """One screen of the kiosk, annotated with the conventions it follows."""
    body = [text(380, 22, "Interface conventions on one screen of the kiosk", 12,
                 650, fill=MUTED)]
    X, Y, W, H = 24, 40, 430, 300
    body.append(box(X, Y, W, H, None, fill=FILL, stroke=TARMAC, r=10))
    body.append('<rect x="%d" y="%d" width="%d" height="44" rx="10" fill="%s"/>'
                % (X, Y, W, GREEN))
    body.append('<rect x="%d" y="%d" width="%d" height="12" fill="%s"/>'
                % (X, Y + 32, W, GREEN))
    body.append(text(X + 18, Y + 28, "Castle Hill Community Garden", 12, 750,
                     anchor="start", fill="#FFFFFF"))
    body.append(box(X + W - 94, Y + 8, 80, 28, None, fill=PAPER, stroke=PAPER,
                    r=14))
    body.append(text(X + W - 54, Y + 27, "Home", 11, 800, fill=GREEN))
    body.append(text(X + 18, Y + 66, "Home  ›  What's growing", 10, 600,
                     anchor="start", fill=MUTED))
    body.append(text(X + 18, Y + 92, "What's growing this month", 15, 800,
                     anchor="start", fill=INK))
    CARDS = [("Sunflowers", ORANGE), ("Runner beans", GREEN),
             ("Lavender", "#7A5FA8")]
    for i, (name, col) in enumerate(CARDS):
        cx = X + 18 + i * 134
        body.append(box(cx, Y + 108, 124, 120, None, fill=FILL2, stroke=LINE,
                        r=8))
        body.append('<rect x="%d" y="%d" width="108" height="64" rx="5" '
                    'fill="%s" opacity="0.85"/>' % (cx + 8, Y + 116, col))
        body.append(text(cx + 62, Y + 200, name, 10.4, 700, fill=INK))
        body.append(text(cx + 62, Y + 217, "tap to find out more", 8.8, 500,
                         fill=MUTED))
    # Button states.
    body.append(box(X + 18, Y + 246, 92, 38, "‹ Back", fill=PAPER,
                    stroke=TARMAC, r=19, label_size=11, text_fill=TARMAC))
    body.append(text(X + 285, Y + 252, "BUTTON STATES", 9, 750, fill=MUTED))
    STATES = [("normal", FILL, LINE, INK), ("pressed", GREEN, GREEN, "#FFFFFF"),
              ("focus", FILL, ORANGE, INK)]
    for i, (k, f, s, ink) in enumerate(STATES):
        bx = X + 166 + i * 82
        body.append(box(bx, Y + 260, 74, 28, None, fill=f, stroke=s, r=14))
        if k == "focus":
            body.append(box(bx - 3, Y + 257, 80, 34, None, fill="none",
                            stroke=ORANGE, r=17))
        body.append(text(bx + 37, Y + 279, k, 9.4, 700, fill=ink))
    MARKS = [(X + W - 94, Y + 8), (X + 8, Y + 62), (X + 142, Y + 108),
             (X + 18, Y + 246), (X + 166, Y + 260)]
    for n, (mx, my) in enumerate(MARKS, 1):
        body.append(marker(n, mx, my))
    body.append(notes(474, 62, 60, 262, [
        ("Home in the same place on every", "screen, top right, always visible"),
        ("A breadcrumb shows where you are,", "and is a route back in itself"),
        ("Cards look tappable, at least 44 px,", "with labels under every image"),
        ("Back bottom left, where the thumb", "of a standing visitor reaches"),
        ("Every button shows pressed and", "focus states, so taps feel answered")]))
    desc = ("One screen of the invented garden kiosk, 'What's growing this "
            "month', annotated with five interface conventions. One: the Home "
            "button sits in the same place on every screen, top right in the "
            "green title bar, always visible. Two: a breadcrumb, 'Home, then "
            "What's growing', shows where the visitor is and is itself a route "
            "back. Three: three large cards, Sunflowers, Runner beans and "
            "Lavender, each with an image and a label and the hint 'tap to find "
            "out more', look tappable and are at least 44 pixels in every "
            "direction. Four: the Back button is at the bottom left, where a "
            "standing visitor's thumb reaches. Five: every button has visible "
            "states, shown as normal, pressed in solid green, and focus with an "
            "orange outline for keyboard users, so every tap feels answered.")
    return figure("r097-ui", 760, 352, "".join(body),
                  "Interface conventions on a kiosk screen", desc,
                  "Conventions are what users already expect. Follow them, and "
                  "the product needs no instructions.")


@diagram("r097-asset-pipeline")
def _assets():
    """From source asset to optimised file in the product."""
    body = [text(380, 22, "Preparing assets: edit, optimise, then export for "
                 "the product", 12, 650, fill=MUTED)]
    HEAD = ["Source", "Edit", "Optimise", "In the product"]
    for i, h in enumerate(HEAD):
        x = 24 + i * 180
        body.append(box(x, 40, 168, 26, None, fill=TEAL_SOFT, stroke=TEAL, r=5))
        body.append(text(x + 84, 58, h.upper(), 9.8, 750, fill=TEAL))
    ROWS = [("IMAGE", ["own photo", "6000 × 4000 JPG, 9.6 MB"],
             ["crop, straighten,", "correct the colour"],
             ["resize to 1600 px wide", "JPG quality 80: ~300 KB"],
             ["images/sunflowers.jpg", "alt text written"]),
            ("AUDIO", ["recorded narration", "WAV, 2 min, about 21 MB"],
             ["trim the silences,", "normalise the level"],
             ["MP3 at 128 kbps", "about 1.9 MB"],
             ["audio/welcome.mp3", "transcript on screen"]),
            ("VIDEO", ["4K phone clip, 60 s", "several hundred MB"],
             ["trim, add titles,", "balance the audio"],
             ["1080p MP4 (H.264)", "5 Mbps: about 37 MB"],
             ["video/tour.mp4", "captions added"])]
    for r, (kind, *cols) in enumerate(ROWS):
        y = 76 + r * 70
        for i, lines in enumerate(cols):
            x = 24 + i * 180
            body.append(box(x, y, 168, 60, None, fill=FILL,
                            stroke=LILAC if i == 2 else LINE, r=6))
            body.append(text(x + 84, y + 25, lines[0], 9.6, 650))
            body.append(text(x + 84, y + 44, lines[1], 9.2, 500,
                             fill=LILAC if i == 2 else MUTED))
            if i < 3:
                body.append(line(x + 169, y + 30, x + 179, y + 30, stroke=LINE,
                                 w=1.4, arrow=True))
        body.append(chip(108, y + 1, kind, size=8.8))
    body.append(box(24, 290, 712, 52, None, fill=WARN_SOFT, stroke=WARN, r=8))
    body.append(text(380, 311, "Keep every original and source file. Optimised "
                     "exports are for the product, not for editing.", 10.2, 700,
                     fill=WARN))
    body.append(text(380, 330, "Record each asset's source, licence and final "
                     "format in the asset table as you go.", 9.6, 500, fill=INK))
    desc = ("How three kinds of asset are prepared for an interactive product, "
            "in four stages: source, edit, optimise, and in the product. An "
            "image: the student's own photo, 6000 by 4000 pixels as a 9.6 "
            "megabyte JPG, is cropped, straightened and colour corrected, then "
            "resized to 1600 pixels wide and saved as a JPG at quality 80, "
            "about 300 kilobytes, and placed as images/sunflowers.jpg with alt "
            "text written. Audio: recorded narration, a two minute WAV of about "
            "21 megabytes, has its silences trimmed and its level normalised, "
            "then is saved as an MP3 at 128 kilobits per second, about 1.9 "
            "megabytes, as audio/welcome.mp3 with a transcript on screen. "
            "Video: a 60 second 4K phone clip of several hundred megabytes is "
            "trimmed, given titles and has its audio balanced, then exported as "
            "a 1080p H.264 MP4 at 5 megabits per second, about 37 megabytes, as "
            "video/tour.mp4 with captions. Every original and source file is "
            "kept, because optimised exports are for the product, not for "
            "editing, and each asset's source, licence and final format go in "
            "the asset table as the work progresses.")
    return figure("r097-assets", 760, 354, "".join(body),
                  "Preparing assets for an interactive product", desc,
                  "An image twenty times bigger than it needs to be makes the "
                  "product slow, and slow loses users.")


@diagram("r097-build-stages")
def _build_stages():
    """The same screen in three passes: structure, content, styling."""
    body = [text(380, 22, "Build in three passes: structure, then content, then "
                 "styling", 12, 650, fill=MUTED)]
    PASSES = [("1  STRUCTURE", "every link works, nothing styled"),
              ("2  CONTENT", "real text, images, audio"),
              ("3  STYLING", "the identity applied last")]
    for i, (k, v) in enumerate(PASSES):
        x = 24 + i * 242
        body.append(text(x + 114, 50, k, 10.4, 750, fill=TEAL))
        body.append(text(x + 114, 66, v, 9.2, 500, fill=MUTED))
        styled = i == 2
        body.append(box(x, 78, 228, 186, None, fill=PAPER if styled else FILL,
                        stroke=TARMAC if styled else LINE, r=8))
        # Title bar.
        body.append('<rect x="%d" y="78" width="228" height="28" rx="8" fill="%s"/>'
                    % (x, GREEN if styled else FILL2))
        body.append(text(x + 12, 97, "Wildlife" if i else "[title]", 10.4,
                         750 if i else 500, anchor="start",
                         fill="#FFFFFF" if styled else (INK if i else MUTED)))
        body.append(box(x + 160, 83, 60, 18, "Home", fill=PAPER if styled else FILL,
                        stroke=GREEN if styled else LINE, r=9, label_size=8.8,
                        text_fill=GREEN if styled else INK))
        if i == 0:
            body.append(box(x + 12, 116, 96, 70, None, fill=FILL2, stroke=LINE,
                            r=3))
            body.append(line(x + 12, 116, x + 108, 186, stroke=LINE, w=1))
            body.append(line(x + 108, 116, x + 12, 186, stroke=LINE, w=1))
            for j in range(4):
                body.append('<rect x="%d" y="%d" width="%d" height="8" rx="2" '
                            'fill="%s"/>' % (x + 118, 120 + j * 16,
                                             98 - (j % 2) * 24, LINE))
            body.append(box(x + 12, 200, 94, 26, "[button]", fill=FILL,
                            stroke=LINE, r=4, label_size=9))
            body.append(box(x + 118, 200, 98, 26, "[button]", fill=FILL,
                            stroke=LINE, r=4, label_size=9))
        else:
            body.append('<rect x="%d" y="116" width="96" height="70" rx="3" '
                        'fill="%s"/>' % (x + 12, "#7FA37A" if styled else "#A0A0A0"))
            body.append(circle(x + 60, 150, 12, fill="#5A4632" if styled
                               else "#6E6E6E", stroke="none", w=0))
            body.append(text(x + 118, 128, "Hedgehogs visit", 9.4,
                             750 if styled else 600, anchor="start",
                             fill=GREEN if styled else INK))
            body.append(text(x + 118, 144, "after dark. Look", 9, 500,
                             anchor="start", fill=TARMAC if styled else INK))
            body.append(text(x + 118, 158, "for the house by", 9, 500,
                             anchor="start", fill=TARMAC if styled else INK))
            body.append(text(x + 118, 172, "the compost bins.", 9, 500,
                             anchor="start", fill=TARMAC if styled else INK))
            body.append(box(x + 12, 200, 94, 26, "Listen",
                            fill=ORANGE if styled else FILL,
                            stroke=ORANGE if styled else LINE, r=13 if styled
                            else 4, label_size=9.4,
                            text_fill=TARMAC if styled else INK))
            body.append(box(x + 118, 200, 98, 26, "Next animal ›",
                            fill=GREEN if styled else FILL,
                            stroke=GREEN if styled else LINE, r=13 if styled
                            else 4, label_size=9.4,
                            text_fill="#FFFFFF" if styled else INK))
        body.append(text(x + 114, 250, ["clickable end to end",
                                        "checked against the plan",
                                        "fonts and colours from the guide"][i],
                         9, 600, fill=TARMAC if styled else MUTED))
        if i < 2:
            body.append(line(x + 229, 170, x + 240, 170, stroke=LINE, w=1.6,
                             arrow=True))
    body.append(box(24, 278, 712, 46, None, fill=WARN_SOFT, stroke=WARN, r=8))
    body.append(text(380, 299, "Styling before the structure is settled means "
                     "restyling every screen each time the structure changes.",
                     10.2, 700, fill=WARN))
    body.append(text(380, 316, "Screenshots of each pass are good evidence of "
                     "your process.", 9.6, 500, fill=INK))
    desc = ("The same Wildlife screen of the invented garden kiosk, built in "
            "three passes. Pass one, structure: grey placeholder boxes for the "
            "title, an image, text and two buttons, nothing styled, but every "
            "link works so the product is clickable end to end. Pass two, "
            "content: the real title, a photograph of a hedgehog, the text "
            "'Hedgehogs visit after dark. Look for the house by the compost "
            "bins.', a Listen button for narration and a Next animal button, "
            "checked against the plan. Pass three, styling: the visual identity "
            "applied last, with the green title bar, rounded orange and green "
            "buttons, and the fonts and colours from the style guide. Styling "
            "before the structure is settled means restyling every screen each "
            "time the structure changes, and screenshots of each pass are good "
            "evidence of the process.")
    return figure("r097-build", 760, 336, "".join(body),
                  "Building a screen in three passes", desc,
                  "Structure, content, styling, and testing all the way "
                  "through.")


@diagram("r097-review-structure")
def _review():
    """The five moves of a review paragraph that scores."""
    body = [text(380, 22, "The shape of a review point that scores", 12, 650,
                 fill=MUTED)]
    STEPS = [("REQUIREMENT", "quote it from the brief", TEAL, TEAL_SOFT),
             ("EVIDENCE", "a test result, feedback", LILAC, LILAC_SOFT),
             ("JUDGEMENT", "met, partly, not met", TEAL, TEAL_SOFT),
             ("IMPROVEMENT", "what, how, what effect", LILAC, LILAC_SOFT),
             ("FURTHER", "beyond the brief", TEAL, TEAL_SOFT)]
    for i, (k, v, tone, soft) in enumerate(STEPS):
        x = 20 + i * 146
        body.append(box(x, 40, 132, 64, None, fill=soft, stroke=tone, r=8))
        body.append(text(x + 66, 64, k, 10.4, 750, fill=tone))
        body.append(text(x + 66, 84, v, 9.2, 550, fill=MUTED))
        if i < 4:
            body.append(line(x + 132, 72, x + 144, 72, stroke=LINE, w=1.6,
                             arrow=True))
    EX = [("REQUIREMENT", "“Visitors must find this month's events within "
           "two taps.”"),
          ("EVIDENCE", "Test 6 passed. Four of five testers did it unaided; the "
           "fifth looked for 'What's on'."),
          ("JUDGEMENT", "Partly met: the route is short, but its label does not "
           "match the visitor's words."),
          ("IMPROVEMENT", "Rename Events to 'What's on', then retest with new "
           "visitors to confirm it helps."),
          ("FURTHER", "A QR code on each event, so visitors can take the "
           "details home on a phone.")]
    for i, (k, v) in enumerate(EX):
        y = 120 + i * 36
        tone = TEAL if i % 2 == 0 else LILAC
        body.append(box(24, y, 712, 30, None, fill=FILL, stroke=LINE, r=6))
        body.append(text(38, y + 20, k, 9.4, 750, anchor="start", fill=tone))
        body.append(text(148, y + 20, v, 9.8, 500, anchor="start"))
    body.append(box(24, 306, 712, 34, None, fill=WARN_SOFT, stroke=WARN, r=8))
    body.append(text(380, 328, "\"It worked well and my friends liked it\" has "
                     "none of the five, so it scores nothing.", 10.2, 700,
                     fill=WARN))
    desc = ("The five moves of a review point that scores, with a worked "
            "example from the invented garden kiosk. Requirement: quote it from "
            "the brief: 'Visitors must find this month's events within two "
            "taps.' Evidence: a test result or feedback: test 6 passed, and four "
            "of five testers did it unaided, while the fifth looked for 'What's "
            "on'. Judgement: met, partly met or not met: partly met, because the "
            "route is short but its label does not match the visitor's words. "
            "Improvement: what, how and with what effect: rename Events to "
            "'What's on', then retest with new visitors to confirm it helps. "
            "Further development, beyond the brief: a QR code on each event so "
            "visitors can take the details home on a phone. A warning "
            "underneath: 'It worked well and my friends liked it' has none of "
            "the five, so it scores nothing.")
    return figure("r097-review", 760, 352, "".join(body),
                  "The structure of a review point", desc,
                  "Requirement, evidence, judgement, improvement, further "
                  "development: for every requirement.")


@diagram("r094-graphic-workflow")
def _graphic_workflow():
    """Six steps from plan to export, and the evidence each one leaves."""
    body = [text(380, 22, "Creating the graphic: six steps, and the evidence "
                 "each one leaves", 12, 650, fill=MUTED)]
    STEPS = [("1  SET UP", ["size, resolution, colour", "mode and bleed from the plan"],
              "document settings"),
             ("2  BUILD THE LOGO", ["vector shapes, paths,", "nodes and Booleans"],
              "editable master kept"),
             ("3  PREPARE IMAGES", ["crop, adjust, mask,", "non-destructively"],
              "before and after"),
             ("4  ASSEMBLE", ["on a grid, following the", "visualisation diagram"],
              "changes explained"),
             ("5  CHECK", ["100%, final size, proof,", "against the brief"],
              "what you fixed"),
             ("6  SAVE AND EXPORT", ["layered master, then one", "export per destination"],
              "named, versioned files")]
    for i, (k, lines, ev) in enumerate(STEPS):
        col, row = i % 3, i // 3
        x, y = 24 + col * 242, 40 + row * 132
        tone, soft = (TEAL, TEAL_SOFT) if row == 0 else (LILAC, LILAC_SOFT)
        body.append(box(x, y, 228, 116, None, fill=soft, stroke=tone, r=8))
        body.append(text(x + 14, y + 24, k, 10.4, 750, anchor="start", fill=tone))
        body.append(text(x + 14, y + 46, lines[0], 9.6, 550, anchor="start"))
        body.append(text(x + 14, y + 62, lines[1], 9.6, 550, anchor="start"))
        body.append(box(x + 10, y + 76, 208, 28, None, fill=FILL, stroke=tone,
                        r=5))
        body.append(text(x + 20, y + 95, "evidence: " + ev, 9.2, 650,
                         anchor="start", fill=tone))
        if col < 2:
            body.append(line(x + 228, y + 58, x + 240, y + 58, stroke=LINE,
                             w=1.6, arrow=True))
    body.append(path("M622 156 L622 164 L138 164 L138 170", stroke=LINE, w=1.6,
                     arrow=True))
    body.append(box(24, 312, 712, 36, None, fill=WARN_SOFT, stroke=WARN, r=8))
    body.append(text(380, 335, "Screenshot as you go. Evidence recreated at the "
                     "end is thinner, and harder to believe.", 10.2, 700,
                     fill=WARN))
    desc = ("Creating a digital graphic in six steps, each with the evidence it "
            "leaves. One, set up: size, resolution, colour mode and bleed taken "
            "from the plan; evidence, the document settings. Two, build the "
            "logo: vector shapes, paths, node editing and Boolean operations; "
            "evidence, an editable master kept. Three, prepare the images: "
            "crop, adjust and mask, non-destructively; evidence, before and "
            "after. Four, assemble: on a grid, following the visualisation "
            "diagram; evidence, the changes from the plan explained. Five, "
            "check: at 100 percent, at final size, as a printed proof and "
            "against the brief; evidence, what was fixed. Six, save and export: "
            "the layered master, then one export per destination; evidence, "
            "named and versioned files. A note underneath: screenshot as you "
            "go, because evidence recreated at the end is thinner and harder to "
            "believe.")
    return figure("r094-flow", 760, 360, "".join(body),
                  "Six steps to create a digital graphic", desc,
                  "Each step is a skill to evidence, not only a stage to get "
                  "through.")


@diagram("r097-garden-wireframes")
def _garden_wireframes():
    """Two annotated wireframes: the hub and one content screen."""
    body = [text(380, 22, "Wireframes for two screens, annotated with what every "
                 "control does", 12, 650, fill=MUTED)]

    def frame(x, y, title):
        out = [box(x, y, 226, 300, None, fill=FILL, stroke=LINE, r=8),
               box(x, y, 226, 30, None, fill=FILL2, stroke=LINE, r=8),
               text(x + 12, y + 20, title, 10, 700, anchor="start"),
               box(x + 160, y + 6, 58, 18, "Home", fill=FILL, stroke=LINE, r=9,
                   label_size=8.6)]
        return "".join(out)

    # Home screen.
    X1, Y1 = 24, 40
    body.append(frame(X1, Y1, "[Castle Hill Garden]"))
    body.append(text(X1 + 113, Y1 + 52, "Welcome: tap a picture", 9.4, 600,
                     fill=MUTED))
    for i, lab in enumerate(["Garden map", "What's growing", "Wildlife",
                             "Events"]):
        col, row = i % 2, i // 2
        bx, by = X1 + 12 + col * 104, Y1 + 64 + row * 92
        body.append(box(bx, by, 98, 84, None, fill=FILL2, stroke=LINE, r=6))
        body.append(line(bx + 8, by + 8, bx + 90, by + 56, stroke=LINE, w=0.8))
        body.append(line(bx + 90, by + 8, bx + 8, by + 56, stroke=LINE, w=0.8))
        body.append(text(bx + 49, by + 74, lab, 8.8, 650))
    body.append(box(X1 + 12, Y1 + 252, 202, 34, "Try the garden quiz",
                    fill=FILL, stroke=LINE, r=6, label_size=9.6))
    # Wildlife screen.
    X2, Y2 = 268, 40
    body.append(frame(X2, Y2, "Wildlife"))
    body.append(box(X2 + 12, Y2 + 42, 120, 92, None, fill=FILL2, stroke=LINE,
                    r=4))
    body.append(line(X2 + 12, Y2 + 42, X2 + 132, Y2 + 134, stroke=LINE, w=0.8))
    body.append(line(X2 + 132, Y2 + 42, X2 + 12, Y2 + 134, stroke=LINE, w=0.8))
    body.append(box(X2 + 142, Y2 + 42, 72, 34, "Listen", fill=FILL, stroke=LINE,
                    r=6, label_size=9.4))
    for j in range(5):
        body.append('<rect x="%d" y="%d" width="%d" height="8" rx="2" fill="%s"/>'
                    % (X2 + 12, Y2 + 148 + j * 16, 202 - (j % 2) * 40, LINE))
    body.append(box(X2 + 12, Y2 + 252, 92, 34, "Back", fill=FILL, stroke=LINE,
                    r=6, label_size=9.6))
    body.append(box(X2 + 112, Y2 + 252, 102, 34, "Next animal", fill=FILL,
                    stroke=LINE, r=6, label_size=9.6))
    MARKS = [(X1 + 12, Y1 + 64), (X1 + 12, Y1 + 252), (X2 + 160, Y2 + 6),
             (X2 + 142, Y2 + 42), (X2 + 112, Y2 + 252)]
    for n, (mx, my) in enumerate(MARKS, 1):
        body.append(marker(n, mx, my))
    body.append(notes(512, 66, 62, 224, [
        ("Each picture opens its section;", "pressed state shows at once"),
        ("Starts the quiz at question 1;", "Home ends it at any point"),
        ("Home on every screen, in the", "same place: one tap to the hub"),
        ("Plays the narration; the label", "changes to Pause while playing"),
        ("Cycles through six animals,", "then returns to the first")]))
    body.append(box(24, 352, 712, 30, None, fill=FILL, stroke=LINE, r=8))
    body.append(text(380, 372, "No colour, no fonts, no final images: structure "
                     "and behaviour only. Styling is decided later.", 10, 650,
                     fill=TEAL))
    desc = ("Two annotated wireframes for the invented garden kiosk, drawn in "
            "grey boxes with no styling. The Home screen has a title bar with a "
            "Home button, the line 'Welcome: tap a picture', four large picture "
            "tiles labelled Garden map, What's growing, Wildlife and Events, and "
            "a wide button, 'Try the garden quiz'. The Wildlife screen has the "
            "title bar and Home button, an image placeholder, a Listen button "
            "beside it, lines of text, and Back and Next animal buttons along "
            "the bottom. Five numbered notes explain the interactions: each "
            "picture opens its section and shows a pressed state at once; the "
            "quiz button starts at question 1, and Home ends the quiz at any "
            "point; Home is on every screen in the same place, one tap from the "
            "hub; Listen plays the narration and its label changes to Pause "
            "while playing; Next animal cycles through six animals and then "
            "returns to the first. Underneath: no colour, no fonts and no final "
            "images, only structure and behaviour, because styling is decided "
            "later.")
    return figure("r097-wire", 760, 394, "".join(body),
                  "Annotated wireframes for two screens", desc,
                  "A wireframe with the interactions written on it is a "
                  "specification, not just a sketch.")


@diagram("r097-user-testing")
def _user_testing():
    """A usability test record: one task, five users, what they did."""
    body = [text(380, 22, "Usability test record: one task, five users from the "
                 "audience", 12, 650, fill=MUTED)]
    body.append(box(24, 38, 712, 30, None, fill=TEAL_SOFT, stroke=TEAL, r=6))
    body.append(text(38, 58, "TASK", 9.6, 750, anchor="start", fill=TEAL))
    body.append(text(84, 58, "“Find out what is happening at the garden "
                     "this month.”  Started from the attract screen; no help "
                     "given.", 9.8, 550, anchor="start"))
    COLS = [70, 132, 64, 54, 92, 300]
    X0 = 24
    head = ["Tester", "Who", "Time", "Taps", "Result", "What they did and said"]
    x = X0
    for w, h in zip(COLS, head):
        body.append(box(x, 76, w, 24, None, fill=FILL2, stroke=LINE, r=3))
        body.append(text(x + w / 2, 92, h, 9.2, 700, fill=MUTED))
        x += w
    ROWS = [("T1", "Year 9 student", "8 s", "2", "unaided",
             "“Easy.” Went straight to Events."),
            ("T2", "Parent with toddler", "11 s", "2", "unaided",
             "Paused on Home, then chose Events."),
            ("T3", "Retired volunteer", "32 s", "5", "with a hint",
             "Tried Garden map first. “I wanted 'What's on'.”"),
            ("T4", "First-time visitor", "9 s", "2", "unaided",
             "No hesitation."),
            ("T5", "Year 11 student", "7 s", "2", "unaided",
             "“Could the text be bigger?”")]
    for r, row in enumerate(ROWS):
        y = 100 + r * 30
        warn = row[4] != "unaided"
        x = X0
        for c, (w, v) in enumerate(zip(COLS, row)):
            body.append(box(x, y, w, 30, None,
                            fill=WARN_SOFT if warn and c == 4 else FILL,
                            stroke=LINE, r=3))
            body.append(text(x + (8 if c == 5 else w / 2), y + 19, v,
                             9.2 if c == 5 else 9.6,
                             700 if c == 4 else 500,
                             anchor="start" if c == 5 else "middle",
                             fill=(WARN if warn else TEAL) if c == 4 else INK))
            x += w
    body.append(box(24, 260, 350, 64, None, fill=TEAL_SOFT, stroke=TEAL, r=8))
    body.append(text(38, 280, "FINDING", 9.6, 750, anchor="start", fill=TEAL))
    body.append(text(38, 298, "4 of 5 unaided, all in under 12 seconds.", 9.6,
                     600, anchor="start"))
    body.append(text(38, 314, "1 needed a hint: the label, not the route.", 9.6,
                     600, anchor="start"))
    body.append(box(386, 260, 350, 64, None, fill=LILAC_SOFT, stroke=LILAC, r=8))
    body.append(text(400, 280, "ACTION", 9.6, 750, anchor="start", fill=LILAC))
    body.append(text(400, 298, "Rename Events to 'What's on', then retest", 9.6,
                     600, anchor="start"))
    body.append(text(400, 314, "with new visitors. Review text size (T5).", 9.6,
                     600, anchor="start"))
    desc = ("A usability test record for the invented garden kiosk. The task: "
            "'Find out what is happening at the garden this month', starting "
            "from the attract screen with no help given. Five testers from the "
            "audience. T1, a Year 9 student: 8 seconds, 2 taps, unaided, said "
            "'Easy' and went straight to Events. T2, a parent with a toddler: 11 "
            "seconds, 2 taps, unaided, paused on Home and then chose Events. T3, "
            "a retired volunteer: 32 seconds, 5 taps, needed a hint, tried "
            "Garden map first and said 'I wanted What's on'. T4, a first-time "
            "visitor: 9 seconds, 2 taps, unaided, no hesitation. T5, a Year 11 "
            "student: 7 seconds, 2 taps, unaided, asked whether the text could "
            "be bigger. The finding: four of five completed the task unaided, "
            "all in under 12 seconds, and the one who needed a hint was let down "
            "by the label rather than the route. The action: rename Events to "
            "'What's on' and retest with new visitors, and review the text size "
            "in response to T5.")
    return figure("r097-users", 760, 336, "".join(body),
                  "A usability test record", desc,
                  "Record what people do, how long it takes and what they say. "
                  "That is the evidence the review is built on.")


@diagram("r094-poster-visualisation")
def _poster_visualisation():
    """The poster's visualisation diagram: the plan the Task 2 build follows."""
    body = [text(380, 22, "Visualisation diagram for the Spokes poster: the plan, "
                 "before anything is built", 12, 650, fill=MUTED)]
    X, Y, W, H = 60, 44, 250, 354
    body.append(box(X - 8, Y - 8, W + 16, H + 16, None, fill="none", stroke=WARN,
                    r=2, dash="3 3"))
    body.append(box(X, Y, W, H, None, fill=FILL, stroke=INK, r=0))
    # The plan, drawn as a sketch: shapes and labels, no finished artwork.
    body.append(box(X, Y, W, 54, None, fill=FILL2, stroke=LINE, r=0))
    body.append(circle(X + 30, Y + 27, 16, fill="none", stroke=INK, w=1.4))
    body.append(text(X + 54, Y + 32, "LOGO + NAME", 10, 700, anchor="start"))
    body.append(box(X + W - 92, Y + 14, 80, 26, "ADDRESS", fill="none",
                    stroke=WARN, r=4, label_size=9, text_fill=WARN, dash="4 3"))
    body.append(text(X + 18, Y + 92, "FREE REPAIR", 24, 800, anchor="start"))
    body.append(text(X + 18, Y + 120, "SATURDAYS", 24, 800, anchor="start"))
    body.append(box(X + 18, Y + 138, 214, 120, None, fill="none", stroke=INK,
                    r=4))
    body.append(line(X + 18, Y + 138, X + 232, Y + 258, stroke=LINE, w=1))
    body.append(line(X + 232, Y + 138, X + 18, Y + 258, stroke=LINE, w=1))
    body.append(box(X + 46, Y + 188, 158, 22, None, fill=FILL, stroke=LINE,
                    r=4))
    body.append(text(X + 125, Y + 203, "own photo of a bike, cut out", 9.4, 650,
                     fill=MUTED))
    for j, w in enumerate((176, 150, 120)):
        body.append('<rect x="%d" y="%d" width="%d" height="9" rx="2" fill="%s"/>'
                    % (X + 18, Y + 276 + j * 18, w, LINE))
    body.append(text(X + W - 18, Y + H - 16, "slogan", 9.4, 650, anchor="end",
                     fill=MUTED))
    MARKS = [(X + W + 8, Y + 8), (X + 8, Y + 28), (X + 8, Y + 84),
             (X + 8, Y + 150), (X + 8, Y + 282), (X + W - 92, Y + 14)]
    for n, (mx, my) in enumerate(MARKS, 1):
        body.append(marker(n, mx, my))
    body.append(notes(344, 64, 64, 392, [
        ("A4 portrait, 210 \u00d7 297 mm, CMYK, 300 dpi,",
         "3 mm bleed (dashed) and 5 mm safe area"),
        ("Header band Spokes Green #1F6F50, 54 mm",
         "deep; logo 30 mm wide, top left"),
        ("Headline Poppins Bold 60 pt on two lines:",
         "Tarmac #2B2F33, then Chain Orange #F28C28"),
        ("Photo: own, 4000 \u00d7 3000 px, cut out with a",
         "mask; enough pixels for 180 mm at 300 dpi"),
        ("Details Source Sans 3 Bold 18 pt: the day,",
         "the time, what to bring. Left aligned"),
        ("Address top right, in the header: the build",
         "moved it, with the reason recorded")]))
    desc = ("A visualisation diagram for the invented Spokes poster, drawn as an "
            "annotated sketch rather than finished artwork. The page is A4 "
            "portrait, 210 by 297 millimetres, CMYK at 300 dpi, with 3 "
            "millimetres of bleed shown dashed and a 5 millimetre safe area. A "
            "header band in Spokes Green, hex 1F6F50, 54 millimetres deep, holds "
            "the logo, 30 millimetres wide, at the top left. The headline, "
            "'Free repair Saturdays', is set in Poppins Bold at 60 point on two "
            "lines, the first in Tarmac, hex 2B2F33, the second in Chain Orange, "
            "hex F28C28. A large box with a cross marks the student's own photo "
            "of a bike, 4000 by 3000 pixels, cut out with a mask, which has "
            "enough pixels to print 180 millimetres wide at 300 dpi. Lines below "
            "it show the details in Source Sans 3 Bold at 18 point, left "
            "aligned: the day, the time and what to bring. The address is "
            "planned for the top right of the header; a note says the build "
            "moved it, with the reason recorded, and the slogan sits at the "
            "bottom right.")
    return figure("r094-vis", 760, 420, "".join(body),
                  "A visualisation diagram for a poster", desc,
                  "Exact sizes, values, fonts and positions, each one numbered "
                  "and explained. Compare it with the finished poster in the "
                  "Task 2 guide.")
