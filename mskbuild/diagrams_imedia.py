"""Diagrams for Creative iMedia and the planning topics that go with it.

Kept in their own module because the Creative iMedia specification is almost
entirely about looking at things: the difference between a storyboard and a
visualisation diagram, between a low angle and a high angle, between CMYK and
RGB. Describing any of those in prose is harder than drawing it, so this unit
earns more pictures per topic than any other on the site.

Registered into the same registry as every other diagram, so `!diagram <name>`
works exactly as it does elsewhere.
"""
from .diagrams import (diagram, TEAL, TEAL_SOFT, LILAC, LILAC_SOFT, WARN,
                       WARN_SOFT, FILL, LINE, MUTED)
from .svg import (figure, figure_steps, step, box, text, line, path, circle,
                  chip)

FILL2 = "var(--dg-fill-2)"


# ====================================================== sectors and products

@diagram("imedia-sectors-products")
def _sectors():
    """Sector, product and purpose are three different answers.

    Students lose marks by giving a product when asked for a sector, so the
    three are drawn as three separate columns with the arrows between them,
    which makes the distinction structural rather than something to remember.
    """
    body = [text(380, 26, "Sector, product, purpose: three different questions",
                 12, 650, fill=MUTED)]

    SECTORS = ["Television and film", "Publishing", "Advertising",
               "Music", "Video games", "Web and apps"]
    PRODUCTS = ["Trailer, series, advert", "Magazine, book, e-book",
                "Campaign, banner, post", "Album art, music video",
                "Game, in-game assets", "Website, mobile app"]
    PURPOSE = ["Entertain", "Inform", "Educate", "Advertise",
               "Persuade", "Provide a service"]

    for i, (s, p) in enumerate(zip(SECTORS, PRODUCTS)):
        y = 56 + i * 44
        body.append(box(28, y, 190, 34, s, fill=TEAL_SOFT, stroke=TEAL, r=6,
                        label_size=11, text_fill=TEAL))
        body.append(box(250, y, 240, 34, p, fill=FILL, stroke=LINE, r=6,
                        label_size=11))
        body.append(line(222, y + 17, 246, y + 17, stroke=LINE, arrow=True))
        body.append(box(522, y, 200, 34, PURPOSE[i], fill=LILAC_SOFT,
                        stroke=LILAC, r=6, label_size=11, text_fill=LILAC))
        body.append(line(494, y + 17, 518, y + 17, stroke=LINE, arrow=True))

    body += [text(123, 46, "SECTOR", 11, 700, fill=TEAL),
             text(370, 46, "PRODUCT it makes", 11, 700, fill=MUTED),
             text(622, 46, "PURPOSE it serves", 11, 700, fill=LILAC),
             text(380, 332, "A sector is part of the industry. A product is the "
                            "thing. A purpose is the job it does.",
                  11, 600, fill=MUTED)]
    desc = ("Three columns showing that a sector, a product and a purpose are "
            "three different answers. The left column lists sectors of the media "
            "industry: television and film, publishing, advertising, music, video "
            "games, and web and apps. The middle column lists products each of "
            "those sectors makes, such as trailers and series for television and "
            "film, magazines and books for publishing, campaigns and banner "
            "adverts for advertising, album artwork and music videos for music, "
            "games and in-game assets for video games, and websites and mobile "
            "apps for web and app development. The right column lists the purposes "
            "a product can have: to entertain, inform, educate, advertise, persuade "
            "or provide a service. A question asking for a sector is not answered "
            "by naming a product, and a question asking for a purpose is not "
            "answered by describing the product.")
    return figure("imedia-sectors", 760, 350, "".join(body),
                  "Sectors, products and purposes", desc,
                  "Netflix is a company. Television and film is the sector. A "
                  "series is the product. To entertain is the purpose.")


# ============================================================ the client brief

@diagram("imedia-brief-anatomy")
def _brief():
    """What is in a brief, and what the client expects anyway.

    The explicit and implicit distinction is reliably examined and reliably
    muddled. Drawing the implicit requirements outside the document, pointing
    in, is the clearest way to fix which is which.
    """
    body = [text(380, 26, "The client brief: what is written, and what is assumed",
                 12, 650, fill=MUTED)]

    # The document itself.
    body.append(box(236, 48, 290, 262, None, fill=FILL, stroke=TEAL, r=10))
    body.append(text(381, 72, "CLIENT BRIEF", 12, 700, fill=TEAL))
    body.append(line(256, 84, 506, 84, stroke=TEAL, w=1.2))
    ROWS = [("Purpose", "what it is for"),
            ("Audience", "who it is for, in detail"),
            ("Message", "the one idea to land"),
            ("Content", "what must appear"),
            ("Deliverables", "formats and sizes"),
            ("Constraints", "deadline, budget, style")]
    for i, (k, v) in enumerate(ROWS):
        y = 98 + i * 35
        body.append(box(254, y, 254, 28, None, fill=TEAL_SOFT, stroke=TEAL, r=5))
        body.append(text(266, y + 18, k, 11, 700, anchor="start", fill=TEAL))
        body.append(text(496, y + 18, v, 10, 450, anchor="end", fill=MUTED))
    body.append(chip(381, 326, "EXPLICIT: it is written down"))

    # Implicit requirements, outside the document, pointing in.
    IMP = ["Spelled correctly", "Works on a phone",
           "Legible at real size", "Assets legally cleared",
           "Accessible contrast", "Opens on their software"]
    for i, t in enumerate(IMP):
        col = 0 if i < 3 else 1
        y = 110 + (i % 3) * 64
        x = 18 if col == 0 else 560
        body.append(box(x, y, 176, 44, None, fill=WARN_SOFT, stroke=WARN, r=6))
        body.append(text(x + 88, y + 19, t, 10.5, 600, fill=WARN))
        body.append(text(x + 88, y + 34, "never stated", 9.5, 450, fill=MUTED))
        if col == 0:
            body.append(line(196, y + 22, 232, y + 22, stroke=WARN, w=1.2,
                             dash="4 3", arrow=True))
        else:
            body.append(line(556, y + 22, 530, y + 22, stroke=WARN, w=1.2,
                             dash="4 3", arrow=True))
    body.append(text(106, 326, "IMPLICIT", 11, 700, fill=WARN))
    body.append(text(648, 326, "IMPLICIT", 11, 700, fill=WARN))

    desc = ("A client brief drawn as a document with six rows inside it, and the "
            "unwritten expectations drawn outside it pointing in. Inside the "
            "document, written down and therefore explicit, are the purpose of the "
            "product, the audience in detail, the single message it must carry, the "
            "content that must appear, the deliverables with their formats and "
            "sizes, and the constraints such as deadline, budget and house style. "
            "Outside the document are six implicit requirements the client expects "
            "without ever stating them: that the text is spelled correctly, that a "
            "website works on a phone, that the design is legible at its real size, "
            "that every asset is legally cleared, that colour contrast is "
            "accessible, and that the files open in the client's own software. "
            "Meeting every explicit requirement while failing an implicit one still "
            "counts as failing the job.")
    return figure("imedia-brief", 760, 344, "".join(body),
                  "Explicit and implicit requirements in a brief", desc,
                  "Nobody writes down what they assume. That is exactly why the "
                  "implicit requirements are the ones that get missed.")


# =========================================================== audience factors

@diagram("imedia-audience-segments")
def _audience():
    """Audience description on the left, design decision on the right.

    An audience fact is worth nothing in an exam until it is attached to a
    decision, so the diagram pairs them and shows nothing on its own.
    """
    base = [text(380, 26, "Three ways to describe an audience, and what each one "
                 "decides", 12, 650, fill=MUTED)]

    def panel(title, tone, soft, items):
        out = [box(28, 52, 300, 236, None, fill=soft, stroke=tone, r=10),
               text(178, 78, title, 13, 700, fill=tone)]
        for i, (k, v) in enumerate(items):
            y = 96 + i * 48
            out.append(box(44, y, 268, 38, None, fill=FILL, stroke=tone, r=6))
            out.append(text(58, y + 17, k, 11, 650, anchor="start", fill=tone))
            out.append(text(58, y + 31, v, 10, 450, anchor="start", fill=MUTED))
        return out

    def decisions(items, tone):
        out = [box(432, 52, 300, 236, None, fill=FILL, stroke=LINE, r=10),
               text(582, 78, "SO THE PRODUCT", 13, 700, fill=MUTED)]
        for i, t in enumerate(items):
            y = 96 + i * 48
            out.append(box(448, y, 268, 38, None, fill=FILL2, stroke=LINE, r=6))
            out.append(text(582, y + 23, t, 10.5, 550, fill="var(--dg-text)"))
            out.append(line(336, y + 19, 426, y + 19, stroke=tone, w=1.4,
                            arrow=True))
        return out

    DEMO = [("Age 65+", "measurable fact"),
            ("Income and education", "what they can afford, and read"),
            ("Location", "local, national, international"),
            ("Family status", "parents, single, retired")]
    DEMO_D = ["Type set at 18pt, contrast above 7:1",
              "Plain language, no assumed jargon",
              "Local place names and local pricing",
              "Shown in a context they recognise"]
    PSY = [("Values sustainability", "an attitude, not an age"),
           ("Sees running as identity", "aspiration"),
           ("Distrusts advertising", "learned scepticism"),
           ("Buys on quality", "not on price")]
    PSY_D = ["Materials and sourcing stated plainly",
             "Real people, not studio athletes",
             "Peer tone, no corporate voice",
             "Detail and craft shown, not discounts"]
    BEH = [("Watches on a phone", "measured, not guessed"),
           ("Sound off", "the default in a feed"),
           ("Leaves within 3 seconds", "if nothing happens"),
           ("Shares what flatters them", "behaviour, not opinion")]
    BEH_D = ["Mastered vertical at 9:16, not cropped",
             "Captions burned in, message in text",
             "The hook lands in the first second",
             "Built to be posted, not just watched"]

    steps = [
        step(1, "".join(panel("DEMOGRAPHICS", TEAL, TEAL_SOFT, DEMO)
                        + decisions(DEMO_D, TEAL)),
             "Demographics: the measurable facts, and what they force."),
        step(2, "".join(panel("PSYCHOGRAPHICS", LILAC, LILAC_SOFT, PSY)
                        + decisions(PSY_D, LILAC)),
             "Psychographics: values and attitudes, and what they force."),
        step(3, "".join(panel("BEHAVIOUR", WARN, WARN_SOFT, BEH)
                        + decisions(BEH_D, WARN)),
             "Behaviour: what they actually do, and what it forces."),
    ]
    L = [s_.split('" ')[-1] for s_ in []] or [
        "Demographics: the measurable facts, and what they force.",
        "Psychographics: values and attitudes, and what they force.",
        "Behaviour: what they actually do, and what it forces."]
    desc = ("Audience description paired with the design decision it produces, in "
            "three stages. Demographics are the measurable facts: an audience aged "
            "65 and over means type set around 18 point with very high contrast; "
            "income and education decide how plain the language has to be; location "
            "decides whether place names and pricing are local; family status "
            "decides the context the product is shown in. Psychographics are values "
            "and attitudes: an audience that values sustainability needs materials "
            "and sourcing stated plainly; one that treats running as part of its "
            "identity responds to real people rather than studio athletes; one that "
            "distrusts advertising needs a peer tone rather than a corporate voice; "
            "one that buys on quality needs craft shown rather than discounts. "
            "Behaviour is what the audience measurably does: watching on a phone "
            "means mastering vertical video at nine by sixteen rather than cropping "
            "a widescreen master; watching with the sound off means captions burned "
            "in and the message carried in text; leaving within three seconds means "
            "the hook has to land immediately; sharing what flatters them means "
            "building something they would willingly post. In every case the "
            "audience fact on its own is worth nothing until the decision is "
            "attached to it.")
    return figure_steps("imedia-aud", 760, 300, "".join(base), steps,
                        "Audience factors and the decisions they force", desc,
                        "An audience fact earns no marks on its own. The mark is "
                        "for the decision it forces.", labels=L)


# ============================================================ research methods

@diagram("imedia-research-matrix")
def _research():
    """Primary against secondary, quantitative against qualitative.

    Two independent distinctions that students merge into one. A two by two
    grid makes it obvious that a method has one of each, never one of two.
    """
    body = [text(380, 24, "Two separate questions: who collected it, and what kind "
                 "of data it is", 12, 650, fill=MUTED)]
    body += [text(60, 92, "PRIMARY", 12, 700, anchor="start", fill=TEAL),
             text(60, 108, "you collected it", 10, 450, anchor="start", fill=MUTED),
             text(60, 222, "SECONDARY", 12, 700, anchor="start", fill=LILAC),
             text(60, 238, "somebody else did", 10, 450, anchor="start", fill=MUTED),
             text(320, 56, "QUANTITATIVE", 12, 700, fill=MUTED),
             text(320, 72, "numbers: how many, how long", 10, 450, fill=MUTED),
             text(590, 56, "QUALITATIVE", 12, 700, fill=MUTED),
             text(590, 72, "words: why, how it felt", 10, 450, fill=MUTED)]

    CELLS = [
        (200, 84, TEAL, TEAL_SOFT, ["Your closed-question survey",
                                    "Counts from your own test",
                                    "Your analytics setup"]),
        (470, 84, TEAL, TEAL_SOFT, ["Your interviews",
                                    "Focus group you ran",
                                    "Watching users attempt a task"]),
        (200, 214, LILAC, LILAC_SOFT, ["Census and Ofcom data",
                                       "Published market reports",
                                       "Industry statistics"]),
        (470, 214, LILAC, LILAC_SOFT, ["Reviews and comments",
                                       "Published case studies",
                                       "Competitor product analysis"]),
    ]
    for x, y, tone, soft, items in CELLS:
        body.append(box(x, y, 240, 112, None, fill=soft, stroke=tone, r=8))
        for i, t in enumerate(items):
            body.append(text(x + 120, y + 30 + i * 28, t, 10.5, 550,
                             fill="var(--dg-text)"))
    body += [line(190, 84, 190, 326, stroke=LINE, w=1.2),
             line(60, 196, 720, 196, stroke=LINE, w=1.2),
             text(380, 346, "A questionnaire is primary if you ran it, and "
                            "secondary to anyone reading its published results.",
                  11, 600, fill=MUTED)]
    desc = ("A two by two grid separating two distinctions that are often "
            "confused. The rows are primary research, which you collected "
            "yourself, and secondary research, which somebody else collected for "
            "their own purposes. The columns are quantitative data, which is "
            "numbers answering how many and how long, and qualitative data, which "
            "is words answering why and how it felt. Primary quantitative examples "
            "include your own closed question survey, counts from your own test and "
            "analytics you set up. Primary qualitative examples include interviews "
            "and focus groups you ran, and watching users attempt a task. Secondary "
            "quantitative examples include census and Ofcom data, published market "
            "reports and industry statistics. Secondary qualitative examples include "
            "reviews and comments, published case studies and analysis of competitor "
            "products. Every method sits in one cell: it has one value from each "
            "distinction, never two from the same one. The same questionnaire is "
            "primary research to the person who ran it and secondary research to "
            "anyone who later reads its published results.")
    return figure("imedia-research", 760, 360, "".join(body),
                  "Primary and secondary, quantitative and qualitative", desc,
                  "Primary or secondary is about who collected it. Quantitative "
                  "or qualitative is about what it is. Every method has one of "
                  "each.")


# ======================================================= layout and compositon

@diagram("imedia-layout-conventions")
def _layout():
    """The four layout ideas, each shown on the same page.

    Composition is the one part of the specification where a description is
    strictly worse than a picture, so the same rectangle is redrawn four times
    with one idea applied each time.
    """
    base = [text(380, 24, "The same page, four composition ideas", 12, 650,
                 fill=MUTED)]
    PX, PY, PW, PH = 230, 44, 300, 240

    def page():
        return box(PX, PY, PW, PH, None, fill=FILL, stroke=LINE, r=6)

    # 1. Rule of thirds.
    thirds = [page()]
    for i in (1, 2):
        thirds.append(line(PX + PW * i / 3, PY, PX + PW * i / 3, PY + PH,
                           stroke=LILAC, w=1.1, dash="4 4"))
        thirds.append(line(PX, PY + PH * i / 3, PX + PW, PY + PH * i / 3,
                           stroke=LILAC, w=1.1, dash="4 4"))
    thirds += [circle(PX + PW / 3, PY + PH / 3, 20, fill=TEAL_SOFT, stroke=TEAL),
               text(PX + PW / 3, PY + PH / 3 + 4, "subject", 9, 650, fill=TEAL),
               text(380, 306, "Rule of thirds: the subject sits on an "
                    "intersection, not in the middle", 11, 600, fill=MUTED)]

    # 2. Grid and alignment.
    grid = [page()]
    for i in range(4):
        gx = PX + 16 + i * 70
        grid.append(box(gx, PY + 70, 54, 150, None, fill=FILL2, stroke=LINE, r=3))
    grid += [box(PX + 16, PY + 20, 268, 36, None, fill=TEAL_SOFT, stroke=TEAL, r=3),
             text(PX + 150, PY + 42, "headline spans the full grid", 10, 600,
                  fill=TEAL),
             line(PX + 16, PY + 16, PX + 16, PY + 230, stroke=WARN, w=1,
                  dash="3 3"),
             line(PX + 284, PY + 16, PX + 284, PY + 230, stroke=WARN, w=1,
                  dash="3 3"),
             text(380, 306, "Grid and alignment: columns, gutters, and a shared "
                  "left and right edge", 11, 600, fill=MUTED)]

    # 3. Visual hierarchy.
    hier = [page(),
            text(PX + 150, PY + 54, "FIRST", 30, 750, fill=TEAL),
            text(PX + 150, PY + 92, "Second, and smaller", 15, 600,
                 fill="var(--dg-text)")]
    for i in range(6):
        hier.append(line(PX + 30, PY + 124 + i * 16, PX + 270, PY + 124 + i * 16,
                         stroke=LINE, w=3))
    hier += [chip(PX + 150, PY + 226, "then the detail", fill=FILL2,
                  stroke=LINE, text_fill=MUTED),
             text(380, 306, "Hierarchy: size and weight decide what is read "
                  "first, second and third", 11, 600, fill=MUTED)]

    # 4. Z pattern and white space.
    zed = [page()]
    zed += [path("M%d %d L%d %d L%d %d L%d %d"
                 % (PX + 26, PY + 40, PX + 274, PY + 40,
                    PX + 26, PY + 190, PX + 274, PY + 190),
                 stroke=TEAL, w=2.4, dash="7 5", arrow=True),
            circle(PX + 26, PY + 40, 13, fill=TEAL_SOFT, stroke=TEAL),
            text(PX + 26, PY + 44, "1", 11, 700, fill=TEAL),
            circle(PX + 274, PY + 40, 13, fill=TEAL_SOFT, stroke=TEAL),
            text(PX + 274, PY + 44, "2", 11, 700, fill=TEAL),
            circle(PX + 26, PY + 190, 13, fill=TEAL_SOFT, stroke=TEAL),
            text(PX + 26, PY + 194, "3", 11, 700, fill=TEAL),
            circle(PX + 274, PY + 190, 13, fill=LILAC_SOFT, stroke=LILAC),
            text(PX + 274, PY + 194, "4", 11, 700, fill=LILAC),
            text(PX + 150, PY + 218, "call to action", 10, 650, fill=LILAC),
            text(380, 306, "Z pattern: the eye crosses, drops and crosses again, "
                 "so the action goes last", 11, 600, fill=MUTED)]

    L = ["Rule of thirds: place the subject off centre, on an intersection.",
         "Grid and alignment: everything shares an edge, which is what looks professional.",
         "Visual hierarchy: size and weight set the reading order.",
         "Z pattern: the eye crosses, drops and crosses again, so the action sits bottom right."]
    steps = [step(1, "".join(thirds), L[0]), step(2, "".join(grid), L[1]),
             step(3, "".join(hier), L[2]), step(4, "".join(zed), L[3])]
    desc = ("Four composition ideas applied to the same rectangular page. The rule "
            "of thirds divides the page into a three by three grid and places the "
            "subject on an intersection rather than in the centre, which reads as "
            "more dynamic. Grid and alignment place the content in columns with "
            "gutters between them, with the headline spanning the full width and "
            "every element sharing the same left and right edge, which is the "
            "single clearest difference between amateur and professional layout. "
            "Visual hierarchy uses size and weight so the largest element is read "
            "first, a smaller subheading second and the body text last, which "
            "controls the order information arrives in. The Z pattern describes how "
            "the eye moves across a poster: along the top, diagonally down, then "
            "along the bottom, which is why the call to action is placed at the "
            "bottom right where the eye finishes.")
    return figure_steps("imedia-layout", 760, 322, "".join(base), steps,
                        "Composition: thirds, grid, hierarchy and the Z pattern",
                        desc,
                        "Composition is why two pages with identical content can "
                        "read completely differently.", labels=L)


# =========================================================== camera and codes

@diagram("imedia-camera-codes")
def _camera():
    """Shot size and camera angle, with the meaning each one carries.

    Shot size is drawn the way a camera actually produces it: one figure, one
    frame, and a clip. Scaling the subject up inside a fixed rectangle is
    exactly what moving the camera closer does, so a wide shot really does
    contain a small whole person and an extreme close up really does contain
    part of a face.
    """
    body = [text(380, 24, "Technical codes: the shot is the meaning", 12, 650,
                 fill=MUTED)]
    FW, FH1, FY1 = 170, 128, 58
    FH2, FY2 = 104, 262
    GAP = 14
    X0 = (760 - (4 * FW + 3 * GAP)) / 2

    def person(cx, head_cy, s, tone=LILAC, soft=LILAC_SOFT, face=False):
        """A figure whose head sits at head_cy, drawn at scale s."""
        r = 7.0 * s
        out = [circle(cx, head_cy, r, fill=soft, stroke=tone, w=max(1.2, s * 0.9))]
        if face:
            out.append(circle(cx - r * 0.34, head_cy - r * 0.14, r * 0.12,
                              fill=tone, stroke=tone, w=0))
            out.append(circle(cx + r * 0.34, head_cy - r * 0.14, r * 0.12,
                              fill=tone, stroke=tone, w=0))
            out.append(path("M%.1f %.1f q%.1f %.1f %.1f 0"
                            % (cx - r * 0.3, head_cy + r * 0.34, r * 0.3,
                               r * 0.26, r * 0.6),
                            stroke=tone, w=max(1.4, s * 0.5)))
        w = max(2.0, s * 1.9)
        out.append(line(cx, head_cy + r, cx, head_cy + 30 * s, stroke=tone, w=w))
        out.append(line(cx - 10 * s, head_cy + 17 * s, cx + 10 * s,
                        head_cy + 17 * s, stroke=tone, w=w * 0.9))
        out.append(line(cx, head_cy + 30 * s, cx - 8 * s, head_cy + 46 * s,
                        stroke=tone, w=w * 0.9))
        out.append(line(cx, head_cy + 30 * s, cx + 8 * s, head_cy + 46 * s,
                        stroke=tone, w=w * 0.9))
        return "".join(out)

    SHOTS = [("Wide shot", "context, scale, isolation", 1.0, 30, False),
             ("Mid shot", "the standard, neutral", 2.3, 36, False),
             ("Close up", "emotion and detail", 4.6, 60, True),
             ("Extreme close up", "one detail, pressure", 10.0, 74, True)]
    for i, (label, meaning, sc, head_off, face) in enumerate(SHOTS):
        x = X0 + i * (FW + GAP)
        cid = "imcam-clip%d" % i
        body.append(box(x, FY1, FW, FH1, None, fill=FILL, stroke=LILAC, r=6))
        body.append('<clipPath id="%s"><rect x="%d" y="%d" width="%d" '
                    'height="%d" rx="6"/></clipPath>'
                    % (cid, x, FY1, FW, FH1))
        body.append('<g clip-path="url(#%s)">%s</g>'
                    % (cid, person(x + FW / 2, FY1 + head_off, sc, face=face)))
        if sc <= 2.5:
            body.append(line(x + 10, FY1 + FH1 - 10, x + FW - 10,
                             FY1 + FH1 - 10, stroke=LINE, w=1.6))
        body.append(text(x + FW / 2, FY1 + FH1 + 20, label, 11.5, 700,
                         fill=LILAC))
        body.append(text(x + FW / 2, FY1 + FH1 + 36, meaning, 9.8, 450,
                         fill=MUTED))
    body.append(text(380, 46, "SHOT SIZE: how much of the subject is in frame",
                     11, 700, fill=LILAC))

    body.append(text(380, 248, "CAMERA ANGLE: where the camera is in relation "
                     "to the subject", 11, 700, fill=TEAL))
    ANGLES = [("Low angle", "power, dominance, threat", "low"),
              ("Eye level", "neutral, equal", "level"),
              ("High angle", "small, vulnerable", "high"),
              ("Dutch angle", "unease, something wrong", "dutch")]
    for i, (label, meaning, kind) in enumerate(ANGLES):
        x = X0 + i * (FW + GAP)
        body.append(box(x, FY2, FW, FH2, None, fill=FILL, stroke=TEAL, r=6))
        cx = x + FW / 2 + 16
        ground = FY2 + FH2 - 14
        inner = [line(x + 14, ground, x + FW - 14, ground, stroke=LINE, w=1.6),
                 person(cx, FY2 + 26, 1.3, TEAL, TEAL_SOFT)]
        if kind != "dutch":
            cam_y = {"low": ground - 6, "level": FY2 + 48,
                     "high": FY2 + 16}[kind]
            inner.append(box(x + 14, cam_y - 9, 22, 18, None, fill=TEAL_SOFT,
                             stroke=TEAL, r=3))
            inner.append(path("M%d %d L%d %d" % (x + 36, cam_y, cx - 13,
                                                 FY2 + 30),
                              stroke=TEAL, w=1.3, dash="4 3", arrow=True))
        group = "".join(inner)
        if kind == "dutch":
            group = ('<g transform="rotate(-13 %d %d)">%s</g>'
                     % (x + FW / 2, FY2 + FH2 / 2, group))
            cid = "imcam-dclip"
            body.append('<clipPath id="%s"><rect x="%d" y="%d" width="%d" '
                        'height="%d" rx="6"/></clipPath>'
                        % (cid, x, FY2, FW, FH2))
            group = '<g clip-path="url(#%s)">%s</g>' % (cid, group)
        body.append(group)
        body.append(text(x + FW / 2, FY2 + FH2 + 20, label, 11.5, 700,
                         fill=TEAL))
        body.append(text(x + FW / 2, FY2 + FH2 + 36, meaning, 9.8, 450,
                         fill=MUTED))

    desc = ("Technical codes drawn as eight frames. The first row shows shot "
            "size, which is how much of the subject the frame contains: a wide "
            "shot holds a small whole figure in a large space and conveys "
            "context, scale or isolation; a mid shot frames the figure from the "
            "waist up and is the neutral standard; a close up fills the frame "
            "with the face and conveys emotion and detail; an extreme close up "
            "holds only part of the face and creates pressure. Each is the same "
            "figure at a different size inside the same rectangle, which is "
            "exactly what moving the camera closer does. The second row shows "
            "camera angle, which is where the camera sits relative to the "
            "subject: a low angle looks up at the subject and conveys power, "
            "dominance or threat; eye level is neutral and equal; a high angle "
            "looks down and makes the subject appear small or vulnerable; and a "
            "Dutch angle tilts the horizon so the whole frame leans, conveying "
            "unease that something is wrong. In the exam the name of the shot "
            "earns little on its own; the effect on the audience is the mark.")
    return figure("imedia-camera", 760, 422, "".join(body),
                  "Shot sizes and camera angles, and what each one means", desc,
                  "Name the shot, then say what the audience reads from it. The "
                  "second half is where the marks are.")


# ================================================ the visualisation diagram

@diagram("imedia-visualisation-anatomy")
def _vis():
    """What has to be written on a visualisation diagram.

    Students draw the layout and stop. The annotations are the assessed part,
    so here they are drawn as the annotations they are, in the margin.
    """
    body = [text(380, 24, "A visualisation diagram: the annotations are the "
                 "document", 12, 650, fill=MUTED)]
    PX, PY, PW, PH = 250, 48, 250, 300
    body.append(box(PX - 10, PY - 10, PW + 20, PH + 20, None, fill=FILL2,
                    stroke=LINE, r=4, dash="5 4"))
    body.append(text(PX + PW / 2, PY - 18, "bleed 3mm", 9.5, 500, fill=WARN))
    body.append(box(PX, PY, PW, PH, None, fill=FILL, stroke=TEAL, r=3))
    body += [box(PX + 18, PY + 16, PW - 36, 52, None, fill=TEAL_SOFT,
                 stroke=TEAL, r=3),
             text(PX + PW / 2, PY + 48, "MASTHEAD", 16, 750, fill=TEAL),
             box(PX + 18, PY + 80, PW - 36, 124, None, fill=FILL2, stroke=LINE,
                 r=3),
             text(PX + PW / 2, PY + 138, "hero image", 11, 550, fill=MUTED),
             text(PX + PW / 2, PY + 156, "2480 x 1240 px", 9.5, 450, fill=MUTED)]
    for i in range(5):
        body.append(line(PX + 18, PY + 222 + i * 14, PX + PW - 36,
                         PY + 222 + i * 14, stroke=LINE, w=3))
    body.append(box(PX + 18, PY + 258, 104, 28, None, fill=LILAC_SOFT,
                    stroke=LILAC, r=14))
    body.append(text(PX + 70, PY + 276, "call to action", 9.5, 600, fill=LILAC))

    NOTES_L = [(PY + 40, "Masthead: Poppins SemiBold 42pt"),
               (PY + 100, "Fill #02848B"),
               (PY + 150, "Image: own photograph, CC0"),
               (PY + 232, "Body: Inter Regular 11pt / 15pt"),
               (PY + 274, "Button #6F6291, 14px radius")]
    for y, t in NOTES_L:
        body.append(line(PX - 14, y, 198, y, stroke=LILAC, w=1.1, dash="3 3"))
        body.append(circle(PX - 14, y, 3.5, fill=LILAC, stroke=LILAC))
        body.append(text(192, y + 4, t, 10, 500, anchor="end", fill=LILAC))

    NOTES_R = [(PY + 20, "A4 portrait, 210 x 297 mm"),
               (PY + 70, "CMYK, 300 ppi"),
               (PY + 128, "Safe margin 10mm"),
               (PY + 200, "Grid: 2 columns, 6mm gutter"),
               (PY + 290, "Export: press-ready PDF")]
    for y, t in NOTES_R:
        body.append(line(PX + PW + 14, y, 560, y, stroke=TEAL, w=1.1, dash="3 3"))
        body.append(circle(PX + PW + 14, y, 3.5, fill=TEAL, stroke=TEAL))
        body.append(text(566, y + 4, t, 10, 500, anchor="start", fill=TEAL))

    body.append(text(380, 368, "If another designer could not build it from your "
                     "diagram, it is not finished", 11, 600, fill=MUTED))
    desc = ("An annotated visualisation diagram for an A4 portrait poster. The page "
            "itself shows a masthead band across the top, a hero image below it, "
            "five lines of body text and a rounded call to action button, with a "
            "dashed bleed area drawn outside the trim edge. Every element carries an "
            "annotation in the margin. On one side: the masthead is Poppins SemiBold "
            "at 42 point, the band is filled with the exact colour hash zero two "
            "eight four eight B, the image is the designer's own photograph released "
            "under CC zero, the body text is Inter Regular at 11 point on 15 point "
            "leading, and the button is filled with hash six F six two nine one with "
            "a 14 pixel corner radius. On the other side: the canvas is A4 portrait "
            "at 210 by 297 millimetres, the colour mode is CMYK at 300 pixels per "
            "inch, a 10 millimetre safe margin is marked, the layout sits on a two "
            "column grid with a 6 millimetre gutter, and the file will be exported "
            "as a press ready PDF. The test of the document is whether another "
            "designer could produce the poster from it without asking a question.")
    return figure("imedia-vis", 760, 384, "".join(body),
                  "What must be annotated on a visualisation diagram", desc,
                  "Exact colour values, named fonts with sizes, real dimensions. "
                  "Writing 'blue' and 'a bold font' is where the marks go.")


# ================================================================ work planning

@diagram("imedia-work-plan")
def _gantt():
    """A Gantt chart with the dependency, the milestone and the contingency.

    A list of tasks is not a work plan. What makes it one is visible here: the
    bars that cannot overlap, the fixed checkpoints and the spare days.
    """
    body = [text(380, 24, "A work plan: tasks against time, with dependencies",
                 12, 650, fill=MUTED)]
    X0, Y0, DAY, ROW = 212, 70, 36, 30
    DAYS = 14
    for d in range(DAYS + 1):
        x = X0 + d * DAY
        body.append(line(x, Y0 - 8, x, Y0 + 8 * ROW, stroke=LINE, w=0.8,
                         dash="2 4"))
        if d % 2 == 0:
            body.append(text(x, Y0 - 14, "day %d" % d, 9, 500, fill=MUTED))

    TASKS = [
        ("Brief and research", 0, 2, TEAL, TEAL_SOFT),
        ("Ideas and mood board", 1, 2, TEAL, TEAL_SOFT),
        ("Storyboard and script", 2, 2, TEAL, TEAL_SOFT),
        ("Book location and crew", 2, 1, LILAC, LILAC_SOFT),
        ("Filming", 4, 2, LILAC, LILAC_SOFT),
        ("Edit", 6, 4, LILAC, LILAC_SOFT),
        ("Contingency", 10, 2, WARN, WARN_SOFT),
        ("Client review and delivery", 12, 2, TEAL, TEAL_SOFT),
    ]
    for i, (name, start, dur, tone, soft) in enumerate(TASKS):
        y = Y0 + i * ROW
        body.append(text(200, y + 18, name, 10.5, 550, anchor="end",
                         fill="var(--dg-text)"))
        body.append(box(X0 + start * DAY + 2, y + 5, dur * DAY - 4, 20, None,
                        fill=soft, stroke=tone, r=4))
        if name == "Contingency":
            body.append(text(X0 + start * DAY + dur * DAY / 2, y + 19, "spare",
                             9.5, 650, fill=WARN))

    # Dependencies: edit cannot start until filming finishes.
    body.append(path("M%d %d L%d %d L%d %d"
                     % (X0 + 6 * DAY, Y0 + 4 * ROW + 25, X0 + 6 * DAY,
                        Y0 + 5 * ROW + 8, X0 + 6 * DAY + 4, Y0 + 5 * ROW + 8),
                     stroke=WARN, w=1.6, arrow=True))
    body.append(text(X0 + 6 * DAY + 56, Y0 + 5 * ROW + 2,
                     "edit depends on filming", 9.5, 600, fill=WARN))
    body.append(path("M%d %d L%d %d L%d %d"
                     % (X0 + 3 * DAY, Y0 + 3 * ROW + 25, X0 + 4 * DAY - 10,
                        Y0 + 3 * ROW + 25, X0 + 4 * DAY - 10, Y0 + 4 * ROW + 6),
                     stroke=WARN, w=1.6, arrow=True))

    # Milestones.
    for day, label in ((2, "brief signed off"), (6, "rushes in"),
                       (12, "client sign off")):
        x = X0 + day * DAY
        body.append(path("M%d %d l7 8 l-7 8 l-7 -8 z" % (x, Y0 + 8 * ROW + 4),
                         stroke=LILAC, w=1.4, fill=LILAC_SOFT))
        body.append(text(x, Y0 + 8 * ROW + 34, label, 9.5, 600, fill=LILAC))
    body.append(text(140, Y0 + 8 * ROW + 20, "milestones", 10, 650,
                     anchor="end", fill=LILAC))
    desc = ("A Gantt chart for a two week video project. Tasks run down the left "
            "and days across the top, with one bar per task. Brief and research "
            "runs on days zero to two, ideas and mood board overlap it on days one "
            "to three, and the storyboard and script run on days two to four. "
            "Booking the location and crew happens on day two, and filming on days "
            "four to six, which means the booking has to be complete before filming "
            "starts. Editing runs from day six to day ten, and an arrow marks that "
            "the edit depends on filming: it cannot begin until the footage exists. "
            "Two contingency days sit on days ten to twelve, deliberately placed "
            "before the client review and delivery on days twelve to fourteen "
            "rather than at the very end, because that is where a delay cannot be "
            "absorbed. Three milestones are marked underneath: the brief signed off "
            "on day two, the rushes in on day six and client sign off on day "
            "twelve. The bars that cannot overlap, the fixed checkpoints and the "
            "spare days are what make this a work plan rather than a list of "
            "tasks.")
    return figure("imedia-gantt", 760, 356, "".join(body),
                  "A Gantt chart with dependencies, milestones and contingency",
                  desc,
                  "A plan that finishes exactly on the deadline has no "
                  "contingency in it at all.")


# ============================================================ licences and law

@diagram("imedia-licence-check")
def _licence():
    """Can I use this asset? A decision tree with the real answers.

    Every year students write that an image is fine because they found it on
    Google. Drawn as a tree, the answer has to be reached rather than assumed.
    """
    body = [text(380, 24, "Can I use this asset?", 12, 650, fill=MUTED)]

    def node(x, y, w, label, sub="", tone=TEAL, soft=TEAL_SOFT, h=46):
        return (box(x, y, w, h, None, fill=soft, stroke=tone, r=8)
                + text(x + w / 2, y + (20 if sub else h / 2 + 4), label, 11, 650,
                       fill=tone)
                + (text(x + w / 2, y + 34, sub, 9.5, 450, fill=MUTED) if sub
                   else ""))

    body.append(node(280, 44, 200, "Did you make it?", "and own it outright"))
    body.append(text(214, 86, "no", 10, 650, fill=MUTED))
    body.append(text(548, 86, "yes", 10, 650, fill=MUTED))
    body.append(path("M480 67 L560 67 L560 100", stroke=LINE, arrow=True))
    body.append(node(488, 104, 150, "Use it", "record it as own work",
                     LILAC, LILAC_SOFT))
    body.append(path("M280 67 L200 67 L200 100", stroke=LINE, arrow=True))
    body.append(node(104, 104, 192, "What licence does it have?",
                     "not 'I found it online'", h=46))

    OPTS = [
        (28, "All rights reserved", "Ask, or pay for a licence", WARN, WARN_SOFT),
        (208, "CC BY", "Use it, credit the creator", TEAL, TEAL_SOFT),
        (388, "CC BY-NC", "NOT on a site with adverts", WARN, WARN_SOFT),
        (568, "Royalty free / CC0", "Use it, check the terms", TEAL, TEAL_SOFT),
    ]
    for x, label, answer, tone, soft in OPTS:
        body.append(path("M200 150 L200 176 L%d 176 L%d 202" % (x + 82, x + 82),
                         stroke=LINE, arrow=True))
        body.append(node(x, 206, 164, label, "", tone, soft, h=36))
        body.append(box(x, 250, 164, 44, None, fill=FILL, stroke=tone, r=6))
        body.append(text(x + 82, 268, answer.split(",")[0], 10, 650, fill=tone))
        body.append(text(x + 82, 283,
                         answer.split(",")[1].strip() if "," in answer else "",
                         9.5, 450, fill=MUTED))

    body.append(box(28, 312, 704, 54, None, fill=WARN_SOFT, stroke=WARN, r=8))
    body.append(text(380, 332, "Does the asset show an identifiable person, or "
                     "private property?", 11, 700, fill=WARN))
    body.append(text(380, 350, "Then you also need a model release, or a property "
                     "release. For under 16s, a parent or guardian must consent.",
                     10, 500, fill=MUTED))
    desc = ("A decision tree for whether an asset may be used. The first question "
            "is whether you made it and own it outright; if so, use it and record "
            "it in the asset table as your own work. If not, the question is what "
            "licence it carries, which is never answered by saying it was found "
            "online. An all rights reserved asset needs permission or a paid "
            "licence. A Creative Commons BY asset may be used provided the creator "
            "is credited. A Creative Commons BY-NC asset is restricted to non "
            "commercial use, so it cannot be used on a site that carries "
            "advertising or sells anything. A royalty free or CC zero asset may be "
            "used, subject to checking the specific terms, and royalty free means "
            "no repeat fee rather than free of charge. Separately from the licence, "
            "if the asset shows an identifiable person or private property, a model "
            "release or property release is also needed, and for anyone under 16 "
            "consent must come from a parent or guardian.")
    return figure("imedia-licence", 760, 378, "".join(body),
                  "Checking whether an asset can legally be used", desc,
                  "'I found it on Google' is not a licence. Copyright is "
                  "automatic, so the default answer is no.")


# ======================================================= colour modes and gamut

@diagram("imedia-colour-modes")
def _colour():
    """RGB adds light, CMYK subtracts it, and that is why colours shift.

    The explanation only lands when the two sets of overlapping circles are
    side by side, because the centres are opposite: white and black.
    """
    body = [text(380, 24, "RGB adds light. CMYK subtracts it.", 12, 650,
                 fill=MUTED)]

    def wheel(cx, cy, cols, centre, centre_label, mode, blurb):
        out = []
        r, d = 56, 32
        pts = [(cx, cy - d), (cx - d, cy + d * 0.7), (cx + d, cy + d * 0.7)]
        for (px, py), col in zip(pts, cols):
            out.append('<circle cx="%d" cy="%d" r="%d" fill="%s" '
                       'fill-opacity="0.72"/>' % (px, py, r, col))
        out.append(circle(cx, cy + 14, 16, fill=centre, stroke="none", w=0))
        out.append(text(cx, cy + 18, centre_label, 9.5, 700,
                        fill="#111" if centre_label == "white" else "#fff"))
        out.append(text(cx, cy + 114, mode, 14, 750, fill=MUTED))
        out.append(text(cx, cy + 132, blurb, 10.5, 500, fill=MUTED))
        return "".join(out)

    body.append(wheel(196, 128, ["#FF3B30", "#34C759", "#0A84FF"], "#ffffff",
                      "white", "RGB", "screens emit light: add all three and you "
                      "get white"))
    body.append(wheel(564, 128, ["#00AEEF", "#EC008C", "#FFF200"], "#1a1a1a",
                      "black", "CMYK", "ink absorbs light: add all three and you "
                      "approach black"))
    body.append(line(380, 72, 380, 262, stroke=LINE, w=1, dash="4 4"))

    ROWS = [("Used by", "screens, phones, projectors", "printing presses, "
             "office printers"),
            ("Channels", "red, green, blue", "cyan, magenta, yellow, key (black)"),
            ("Gamut", "wider: bright greens and cyans", "narrower: those colours "
             "dull down"),
            ("Resolution", "72 to 144 ppi is plenty", "about 300 ppi at final size"),
            ("Deliver as", "JPG, PNG, WEBP, SVG", "press-ready PDF or TIFF")]
    for i, (k, a, b) in enumerate(ROWS):
        y = 292 + i * 30
        body.append(box(28, y, 704, 26, None,
                        fill=FILL if i % 2 else FILL2, stroke="none", r=4))
        body.append(text(40, y + 18, k, 10.5, 700, anchor="start", fill=MUTED))
        body.append(text(200, y + 18, a, 10.5, 500, anchor="start", fill=TEAL))
        body.append(text(452, y + 18, b, 10.5, 500, anchor="start", fill=LILAC))
    body.append(text(380, 462, "Choose the mode from the destination at the start. "
                     "Converting at the end is where the surprise happens.",
                     11, 600, fill=MUTED))
    desc = ("Two sets of three overlapping circles, comparing additive and "
            "subtractive colour. On the left, RGB: red, green and blue circles "
            "overlap and their centre is white, because screens emit light and "
            "adding all three gives white. On the right, CMYK: cyan, magenta and "
            "yellow circles overlap and their centre is black, because ink absorbs "
            "light and adding all three approaches black. The table underneath "
            "compares them. RGB is used by screens, phones and projectors; CMYK by "
            "printing presses and office printers. RGB has three channels; CMYK has "
            "four, the fourth being key, or black. RGB has the wider gamut, so "
            "bright greens and cyans visible on screen dull down when converted to "
            "CMYK. RGB artwork needs only 72 to 144 pixels per inch; CMYK print "
            "artwork needs around 300 pixels per inch at final size. RGB is "
            "delivered as JPG, PNG, WEBP or SVG; CMYK as a press ready PDF or TIFF. "
            "The colour mode should be chosen from the destination at the start of "
            "the project, because converting at the end is when the colour shift "
            "becomes a surprise.")
    return figure("imedia-colour", 760, 478, "".join(body),
                  "RGB and CMYK compared", desc,
                  "Design a poster in RGB and the greens you chose will not be "
                  "the greens that print.")


# ====================================================== raster against vector

@diagram("imedia-raster-vector")
def _rastervector():
    """The same logo, enlarged, in both kinds of file.

    One is drawn as actual squares getting bigger and one as a path staying
    smooth, which is the whole argument in a single picture.
    """
    body = [text(380, 24, "The same mark, enlarged four times", 12, 650,
                 fill=MUTED)]

    def mark_vector(cx, cy, s, tone=TEAL):
        """A smooth quarter-arc mark, drawn at any size without loss."""
        return path("M%.1f %.1f a%.1f %.1f 0 0 1 %.1f %.1f L%.1f %.1f Z"
                    % (cx - s, cy + s, s * 2, s * 2, s * 2, 0, cx - s, cy + s),
                    stroke=tone, w=max(1.4, s * 0.16), fill="none")

    def mark_raster(cx, cy, s, px):
        """The same shape sampled onto a grid of px-sized squares."""
        out = []
        n = int(s * 2 / px) + 1
        for i in range(n):
            for j in range(n):
                x = cx - s + i * px
                y = cy - s + j * px
                # Keep the squares that straddle the arc.
                dx, dy = (x + px / 2) - (cx - s), (y + px / 2) - (cy + s)
                d = (dx * dx + dy * dy) ** 0.5
                if abs(d - s * 2) < max(px * 0.8, s * 0.17) and dy <= 0:
                    out.append('<rect x="%.1f" y="%.1f" width="%.1f" '
                               'height="%.1f" fill="%s"/>'
                               % (x, y, px - 0.6, px - 0.6, LILAC))
        return "".join(out)

    SIZES = [(96, 20, 2.4), (242, 34, 4.4), (436, 54, 7.6), (654, 78, 11.4)]
    for cx, s, px in SIZES:
        body.append(mark_raster(cx, 136, s, px))
        body.append(mark_vector(cx, 300, s))
        body.append(text(cx, 196, "%dx" % (1 if s == 20 else
                                           (2 if s == 34 else
                                            (3 if s == 54 else 4))),
                         10, 600, fill=MUTED))
    body += [text(44, 60, "RASTER", 13, 750, anchor="start", fill=LILAC),
             text(44, 78, "pixels: enlarging makes the pixels bigger",
                  10.5, 500, anchor="start", fill=MUTED),
             text(44, 232, "VECTOR", 13, 750, anchor="start", fill=TEAL),
             text(44, 250, "paths: enlarging recalculates the curve",
                  10.5, 500, anchor="start", fill=MUTED)]
    body.append(box(28, 344, 352, 72, None, fill=LILAC_SOFT, stroke=LILAC, r=8))
    body.append(text(204, 366, "Raster is right for photographs", 11, 700,
                     fill=LILAC))
    body.append(text(204, 384, "JPG, PNG, WEBP, TIFF", 10, 500, fill=MUTED))
    body.append(text(204, 402, "Detail per pixel is exactly what a photo is",
                     10, 450, fill=MUTED))
    body.append(box(392, 344, 340, 72, None, fill=TEAL_SOFT, stroke=TEAL, r=8))
    body.append(text(562, 366, "Vector is right for logos and type", 11, 700,
                     fill=TEAL))
    body.append(text(562, 384, "SVG, AI, EPS, PDF", 10, 500, fill=MUTED))
    body.append(text(562, 402, "Favicon to billboard from one file", 10, 450,
                     fill=MUTED))
    desc = ("The same mark enlarged four times, drawn twice. The top row is a "
            "raster version: the shape is stored as a grid of pixels, so enlarging "
            "it simply makes each pixel bigger, and by four times the curve has "
            "become a visible staircase of squares. The bottom row is a vector "
            "version: the shape is stored as a mathematical path, so at every size "
            "the curve is recalculated and stays perfectly smooth. Raster formats, "
            "JPG, PNG, WEBP and TIFF, are the right choice for photographs, because "
            "a photograph genuinely is detail recorded per pixel. Vector formats, "
            "SVG, AI, EPS and PDF, are the right choice for logos, icons, diagrams "
            "and type, because one file then serves everything from a sixteen pixel "
            "favicon to a billboard.")
    return figure("imedia-rv", 760, 428, "".join(body),
                  "Raster and vector under enlargement", desc,
                  "A logo delivered only as a JPG is a logo that cannot go on a "
                  "van.")


# ============================================================ file compression

@diagram("imedia-compression-types")
def _compression():
    """Lossless restores exactly; lossy throws away and keeps throwing away.

    The generational part is the bit that matters in practice, so the lossy
    path is drawn as three successive saves getting worse.
    """
    body = [text(380, 24, "Lossless gives it back. Lossy never does.", 12, 650,
                 fill=MUTED)]

    def blocks(x, y, n, tone, step_fade=0.0):
        out = []
        for i in range(n):
            op = max(0.25, 1.0 - step_fade * i)
            out.append('<rect x="%d" y="%d" width="13" height="26" rx="2" '
                       'fill="%s" fill-opacity="%.2f"/>'
                       % (x + i * 16, y, tone, op))
        return "".join(out)

    body.append(box(28, 56, 704, 128, None, fill=TEAL_SOFT, stroke=TEAL, r=10))
    body.append(text(60, 80, "LOSSLESS", 12, 750, anchor="start", fill=TEAL))
    body.append(text(140, 80, "PNG · FLAC · ZIP · TIFF", 10.5, 500,
                     anchor="start", fill=MUTED))
    body.append(text(118, 112, "original", 10, 600, fill=MUTED))
    body.append(blocks(60, 124, 7, TEAL))
    body.append(line(188, 136, 236, 136, stroke=TEAL, arrow=True))
    body.append(text(212, 126, "compress", 9.5, 550, fill=TEAL))
    body.append(box(244, 118, 110, 38, None, fill=FILL, stroke=TEAL, r=5))
    body.append(text(299, 141, "smaller file", 10, 600, fill=TEAL))
    body.append(line(360, 136, 408, 136, stroke=TEAL, arrow=True))
    body.append(text(384, 126, "open", 9.5, 550, fill=TEAL))
    body.append(blocks(416, 124, 7, TEAL))
    body.append(text(474, 112, "identical to the original", 10, 600, fill=TEAL))
    body.append(text(620, 141, "nothing was discarded", 10.5, 600, fill=TEAL))

    body.append(box(28, 200, 704, 150, None, fill=WARN_SOFT, stroke=WARN, r=10))
    body.append(text(60, 224, "LOSSY", 12, 750, anchor="start", fill=WARN))
    body.append(text(116, 224, "JPG · MP3 · MP4 · AAC", 10.5, 500,
                     anchor="start", fill=MUTED))
    for i, label in enumerate(["original", "save 1", "save 2", "save 3"]):
        x = 60 + i * 176
        body.append(text(x + 56, 254, label, 10, 600, fill=MUTED))
        body.append(blocks(x, 264, 7, WARN if i else TEAL, step_fade=0.12 * i))
        if i < 3:
            body.append(line(x + 120, 276, x + 168, 276, stroke=WARN, arrow=True))
            body.append(text(x + 144, 266, "re-save", 9, 550, fill=WARN))
    body.append(text(380, 322, "Each save discards more. The detail is gone and "
                     "cannot be recovered, which is why you edit the master and "
                     "export a copy.", 10.5, 600, fill=WARN))
    desc = ("Two rows comparing lossless and lossy compression. The lossless row, "
            "covering PNG, FLAC, ZIP and TIFF, shows an original sequence of blocks "
            "compressed into a smaller file and then opened again, with the result "
            "identical to the original, because nothing was discarded. The lossy "
            "row, covering JPG, MP3, MP4 and AAC, shows the original being saved "
            "three times in succession, and the blocks fade a little more with each "
            "save: every re-save discards more detail permanently, so the quality "
            "degrades generation by generation and nothing can be recovered. That "
            "is the practical reason for keeping a lossless master and exporting a "
            "lossy copy for delivery, rather than editing and re-saving the "
            "export.")
    return figure("imedia-comp", 760, 362, "".join(body),
                  "Lossless and lossy compression compared", desc,
                  "Open and re-save the same JPG two hundred times and it turns "
                  "into coloured blocks.")


# ========================================================= distribution routes

@diagram("imedia-distribution-routes")
def _distribution():
    """One finished product, two routes out, and what each route demands.

    Students treat distribution as an afterthought. Drawing the demands on
    each branch shows that the route decides properties set weeks earlier.
    """
    body = [text(380, 24, "One product, two routes, two sets of requirements",
                 12, 650, fill=MUTED)]
    body.append(box(290, 44, 180, 46, None, fill=FILL, stroke=LINE, r=8))
    body.append(text(380, 72, "FINISHED PRODUCT", 11, 700, fill="var(--dg-text)"))
    body.append(path("M290 67 L200 67 L200 104", stroke=LINE, arrow=True))
    body.append(path("M470 67 L560 67 L560 104", stroke=LINE, arrow=True))

    def branch(x, title, tone, soft, needs, pros, cons):
        out = [box(x, 108, 320, 40, None, fill=soft, stroke=tone, r=8),
               text(x + 160, 133, title, 12, 750, fill=tone)]
        out.append(text(x + 160, 170, "DEMANDS", 10, 700, fill=MUTED))
        for i, t in enumerate(needs):
            out.append(box(x, 180 + i * 28, 320, 24, None, fill=FILL,
                           stroke=tone, r=4))
            out.append(text(x + 160, 196 + i * 28, t, 10, 500,
                            fill="var(--dg-text)"))
        y = 180 + len(needs) * 28 + 10
        out.append(text(x + 160, y + 12, "GOOD: " + pros, 10, 600, fill=tone))
        out.append(text(x + 160, y + 30, "BAD: " + cons, 10, 600, fill=WARN))
        return "".join(out)

    body.append(branch(40, "PHYSICAL", LILAC, LILAC_SOFT,
                       ["CMYK, 300 ppi, bleed and trim",
                        "Press deadline, no late changes",
                        "Manufacturing, storage, shipping",
                        "A separate large-print version",
                        "Barcode, price, legal lines"],
                       "tangible, no device, reaches ad-blocked audiences",
                       "costs money, slow, cannot be corrected"))
    body.append(branch(400, "ONLINE", TEAL, TEAL_SOFT,
                       ["RGB, right aspect ratio per platform",
                        "Compressed to load on mobile data",
                        "Captions, alt text, keyboard access",
                        "Responsive layout, HTTPS, SEO",
                        "Metadata, thumbnail, store artwork"],
                       "global, cheap, measurable, updateable",
                       "pirated, ignored, platform rules change"))
    desc = ("One finished product with two distribution routes branching from it, "
            "each with its own requirements. The physical route demands CMYK "
            "artwork at around 300 pixels per inch with bleed and trim marks, a "
            "press deadline after which no changes are possible, manufacturing, "
            "storage and shipping, a separate large print version for accessibility "
            "because the printed size is fixed, and compliance items such as a "
            "barcode, a price and legal lines. Its advantages are that it is "
            "tangible, needs no device and reaches audiences who block online "
            "advertising; its drawbacks are cost, slowness and the fact that it "
            "cannot be corrected once printed. The online route demands RGB assets "
            "in the correct aspect ratio for each platform, compression so the "
            "product loads on mobile data, captions, alternative text and keyboard "
            "access, a responsive layout served over HTTPS with search metadata, "
            "and platform specific items such as thumbnails and store artwork. Its "
            "advantages are global reach, low cost, measurability and the ability to "
            "update after publication; its drawbacks are piracy, enormous "
            "competition for attention, and platform rules that can change without "
            "notice. Both lists are decided weeks before delivery, which is why "
            "distribution is a planning decision rather than a final step.")
    return figure("imedia-dist", 760, 372, "".join(body),
                  "Physical and online distribution requirements", desc,
                  "The route out decides properties you had to choose at the "
                  "start. That is why it belongs in the plan.")


# ================================================================== logo types

@diagram("imedia-logo-types")
def _logos():
    """Six kinds of logo, drawn, with what each one asks of the audience."""
    body = [text(380, 24, "Six kinds of logo, and what each asks of the audience",
                 12, 650, fill=MUTED)]
    CELL_W, CELL_H = 228, 132

    def cell(col, row, kind, note, art):
        x = 32 + col * (CELL_W + 14)
        y = 48 + row * (CELL_H + 22)
        out = [box(x, y, CELL_W, CELL_H, None, fill=FILL, stroke=LINE, r=8),
               art(x + CELL_W / 2, y + 52),
               text(x + CELL_W / 2, y + 100, kind, 11.5, 700, fill=TEAL),
               text(x + CELL_W / 2, y + 118, note, 9.5, 450, fill=MUTED)]
        return "".join(out)

    def wordmark(cx, cy):
        return text(cx, cy + 8, "KERNFORD", 22, 750, fill=TEAL)

    def lettermark(cx, cy):
        return (box(cx - 42, cy - 22, 84, 44, None, fill=TEAL_SOFT, stroke=TEAL,
                    r=6) + text(cx, cy + 8, "KF", 22, 800, fill=TEAL))

    def pictorial(cx, cy):
        return (path("M%d %d q18 -26 36 0 q-18 10 -36 0 Z" % (cx - 18, cy),
                     stroke=TEAL, w=2.4, fill=TEAL_SOFT)
                + circle(cx, cy - 2, 4, fill=TEAL, stroke=TEAL))

    def abstract(cx, cy):
        return (path("M%d %d a22 22 0 0 1 44 0 Z" % (cx - 22, cy + 12),
                     stroke=LILAC, w=2.4, fill=LILAC_SOFT)
                + path("M%d %d a14 14 0 0 0 28 0 Z" % (cx - 14, cy + 12),
                       stroke=LILAC, w=2, fill=FILL))

    def mascot(cx, cy):
        return (circle(cx, cy - 4, 17, fill=LILAC_SOFT, stroke=LILAC)
                + circle(cx - 6, cy - 7, 2.6, fill=LILAC, stroke=LILAC)
                + circle(cx + 6, cy - 7, 2.6, fill=LILAC, stroke=LILAC)
                + path("M%d %d q6 6 12 0" % (cx - 6, cy + 2), stroke=LILAC, w=2)
                + path("M%d %d l4 -12 l9 7 Z" % (cx - 17, cy - 12),
                       stroke=LILAC, w=1.6, fill=LILAC_SOFT)
                + path("M%d %d l-4 -12 l-9 7 Z" % (cx + 17, cy - 12),
                       stroke=LILAC, w=1.6, fill=LILAC_SOFT))

    def combination(cx, cy):
        return (circle(cx - 44, cy, 15, fill=TEAL_SOFT, stroke=TEAL)
                + path("M%d %d l9 -9 l9 9 l-9 9 Z" % (cx - 53, cy),
                       stroke=TEAL, w=1.8, fill=TEAL)
                + text(cx + 18, cy + 7, "KERNFORD", 14, 700, fill=TEAL))

    body.append(cell(0, 0, "Wordmark", "the name, styled: needs a memorable name",
                     wordmark))
    body.append(cell(1, 0, "Lettermark", "initials: needs people to know them "
                    "already", lettermark))
    body.append(cell(2, 0, "Pictorial mark", "a real object: needs a relevant one",
                     pictorial))
    body.append(cell(0, 1, "Abstract mark", "a shape with no meaning: needs years "
                    "of spend", abstract))
    body.append(cell(1, 1, "Mascot", "a character: friendly, harder to scale down",
                     mascot))
    body.append(cell(2, 1, "Combination", "symbol plus name: safest for a new "
                    "brand", combination))
    body.append(box(32, 368, 700, 44, None, fill=TEAL_SOFT, stroke=TEAL, r=8))
    body.append(text(382, 388, "Whichever you choose, it has to work at 16 pixels "
                     "and in one colour.", 11, 700, fill=TEAL))
    body.append(text(382, 404, "That is why logos lose detail as they develop "
                     "rather than gaining it.", 10, 500, fill=MUTED))
    desc = ("Six kinds of logo, each drawn with a note on what it asks of the "
            "audience. A wordmark is the organisation's name styled distinctively, "
            "and it needs a memorable name to work. A lettermark uses initials, "
            "which only functions if the audience already knows the organisation. A "
            "pictorial mark uses a recognisable real object, which needs the object "
            "to be genuinely relevant. An abstract mark is a shape with no literal "
            "meaning, which takes years of marketing spend before it means "
            "anything. A mascot is a character, which reads as friendly but is "
            "harder to scale down. A combination mark pairs a symbol with the name, "
            "which is the safest choice for a new brand because the name teaches "
            "the audience who you are and the symbol can later stand alone. "
            "Whichever type is chosen, the mark has to remain legible at sixteen "
            "pixels and in a single colour, which is why logos lose detail as they "
            "develop rather than gaining it.")
    return figure("imedia-logos", 760, 424, "".join(body),
                  "Six kinds of logo", desc,
                  "A combination mark is the safest first logo, because the name "
                  "does the teaching until the symbol can stand alone.")


# ================================================================ the review

@diagram("imedia-review-quality")
def _review():
    """What a weak review says, and what the same point looks like with evidence.

    The review carries real marks in both coursework units and loses them for
    being positive. Side by side, the difference is impossible to miss.
    """
    body = [text(380, 24, "The same three points, written two ways", 12, 650,
                 fill=MUTED)]
    body.append(text(206, 54, "WHAT LOSES MARKS", 11, 750, fill=WARN))
    body.append(text(560, 54, "WHAT EARNS THEM", 11, 750, fill=TEAL))
    PAIRS = [
        ("“The navigation worked well.”",
         "“Four of five testers reached booking in under three taps. The "
         "fifth looked for a Book button in the header, where the convention "
         "puts it. I would add one.”"),
        ("“I would add more content.”",
         "“Each topic has text and one image. Two testers asked for "
         "sources, so I would add a references panel under each topic, "
         "collapsed by default.”"),
        ("“It all went to plan.”",
         "“I styled the topic screens before the navigation was finished, "
         "so adding the video screen meant restyling three. Next time I would "
         "leave styling until the structure is signed off.”"),
    ]

    def wrapped(x, y, w, s, size, fill, weight=500):
        """Very simple greedy wrap, because SVG will not do it for us."""
        words, lines, cur = s.split(), [], ""
        per = max(8, int(w / (size * 0.50)))
        for word in words:
            if len(cur) + len(word) + 1 <= per:
                cur = (cur + " " + word).strip()
            else:
                lines.append(cur)
                cur = word
        if cur:
            lines.append(cur)
        return "".join(text(x, y + i * (size + 4), ln, size, weight,
                            anchor="start", fill=fill)
                       for i, ln in enumerate(lines)), len(lines)

    y = 70
    for weak, strong in PAIRS:
        wtxt, wn = wrapped(48, y + 26, 300, weak, 11, WARN, 550)
        stxt, sn = wrapped(414, y + 26, 304, strong, 10.5, "var(--dg-text)", 500)
        h = max(wn, sn) * 15 + 28
        body.append(box(32, y, 332, h, None, fill=WARN_SOFT, stroke=WARN, r=8))
        body.append(box(398, y, 334, h, None, fill=TEAL_SOFT, stroke=TEAL, r=8))
        body.append(wtxt)
        body.append(stxt)
        body.append(line(368, y + h / 2, 392, y + h / 2, stroke=LINE,
                         arrow=True))
        y += h + 14
    body.append(text(380, y + 20, "Evidence, a specific weakness, and the change "
                     "you would make. All three, every time.", 11, 650,
                     fill=MUTED))
    desc = ("Three review comments shown twice, in a weak version and a strong "
            "version. The weak comment 'the navigation worked well' becomes 'four "
            "of five testers reached booking in under three taps; the fifth looked "
            "for a Book button in the header, where the convention puts it, so I "
            "would add one'. The weak comment 'I would add more content' becomes "
            "'each topic has text and one image, and two testers asked for sources, "
            "so I would add a references panel under each topic, collapsed by "
            "default'. The weak comment 'it all went to plan' becomes 'I styled the "
            "topic screens before the navigation was finished, so adding the video "
            "screen meant restyling three, and next time I would leave styling "
            "until the structure is signed off'. Every strong version contains the "
            "same three things: measured evidence, a specific weakness, and the "
            "change that would be made.")
    return figure("imedia-review", 760, y + 34, "".join(body),
                  "Weak and strong review writing compared", desc,
                  "A review that finds nothing wrong reads as a review that was "
                  "never carried out.")


# ==================================================================== purpose

@diagram("imedia-purpose-wheel")
def _purpose():
    """Six purposes, and one product that is quietly doing three of them."""
    body = [text(380, 24, "Six purposes, and why most products have more than one",
                 12, 650, fill=MUTED)]
    PURPOSES = [("Entertain", "drama, game, comedy podcast"),
                ("Inform", "news bulletin, documentary"),
                ("Educate", "training video, revision site"),
                ("Advertise", "poster, trailer, sponsored post"),
                ("Persuade", "charity appeal, campaign"),
                ("Provide a service", "banking app, council website")]
    for i, (p, ex) in enumerate(PURPOSES):
        col, row = i % 3, i // 3
        x, y = 32 + col * 234, 50 + row * 72
        body.append(box(x, y, 222, 58, None, fill=TEAL_SOFT, stroke=TEAL, r=8))
        body.append(text(x + 111, y + 24, p, 12, 700, fill=TEAL))
        body.append(text(x + 111, y + 42, ex, 9.5, 450, fill=MUTED))

    body.append(box(32, 212, 700, 128, None, fill=FILL, stroke=LILAC, r=10))
    body.append(text(382, 236, "One 30 second charity advert, three purposes at "
                     "once", 12, 700, fill=LILAC))
    LAYERS = [("Entertains", "enough that you do not skip it in the first "
               "two seconds"),
              ("Informs", "a voiceover and captions give the statistic"),
              ("Persuades", "the closing shot and the donation number on screen")]
    for i, (k, v) in enumerate(LAYERS):
        y = 254 + i * 28
        body.append(box(48, y, 150, 22, None, fill=LILAC_SOFT, stroke=LILAC, r=11))
        body.append(text(123, y + 15, k, 10, 700, fill=LILAC))
        body.append(text(212, y + 15, v, 10, 450, anchor="start", fill=MUTED))
    body.append(text(382, 356, "A question worth three marks is asking for three "
                     "purposes, not one said three ways.", 11, 600, fill=MUTED))
    desc = ("Six purposes a media product can have, each with example products: to "
            "entertain, as in a drama, a game or a comedy podcast; to inform, as in "
            "a news bulletin or a documentary; to educate, as in a training video "
            "or a revision site; to advertise, as in a poster, a trailer or a "
            "sponsored post; to persuade, as in a charity appeal or a campaign; and "
            "to provide a service, as in a banking app or a council website. "
            "Underneath, one thirty second charity advert is shown doing three of "
            "them at once: it entertains enough that the viewer does not skip it in "
            "the first two seconds, it informs through a voiceover and captions "
            "giving a statistic, and it persuades through the closing shot and the "
            "donation number on screen. A question worth three marks is asking for "
            "three different purposes rather than one purpose stated three ways.")
    return figure("imedia-purpose", 760, 372, "".join(body),
                  "The purposes of a media product", desc,
                  "Almost nothing has only one purpose. Saying only 'to "
                  "advertise' leaves marks on the table.")


# ================================================================ constraints

@diagram("imedia-constraints")
def _constraints():
    """A constraint is only worth a mark once you say what it forces."""
    body = [text(380, 24, "Name the constraint, then name the decision it forces",
                 12, 650, fill=MUTED)]
    ROWS = [("Time", "three weeks, not three months",
             "Fewer concepts, earlier sign off, no reshoot window"),
            ("Budget", "no money for a shoot",
             "Typography and one licensed stock image, not photography"),
            ("Resources", "one camera, one editor",
             "A single location, a shot list that one person can cover"),
            ("Technical", "under 2 MB, 9:16, 60 seconds",
             "Heavier compression, vertical master, tighter edit"),
            ("Legal", "under 16s appear on camera",
             "Parental consent collected before the shoot, not after"),
            ("House style", "the client's fonts and palette",
             "No new typeface, no new colour, work within the system"),
            ("Platform", "a feed, not a cinema",
             "Captions, the hook in the first second, sound off by default")]
    for i, (k, detail, forced) in enumerate(ROWS):
        y = 48 + i * 44
        body.append(box(28, y, 150, 36, None, fill=WARN_SOFT, stroke=WARN, r=6))
        body.append(text(103, y + 16, k, 11, 700, fill=WARN))
        body.append(text(103, y + 30, detail, 9, 450, fill=MUTED))
        body.append(line(182, y + 18, 214, y + 18, stroke=WARN, arrow=True))
        body.append(box(218, y, 514, 36, None, fill=FILL, stroke=TEAL, r=6))
        body.append(text(234, y + 22, forced, 10.5, 550, anchor="start",
                         fill="var(--dg-text)"))
    body.append(text(380, 368, "“The budget was limited” earns nothing. "
                     "The sentence after it earns the mark.", 11, 650, fill=MUTED))
    desc = ("Seven constraints paired with the decision each one forces. A time "
            "constraint of three weeks rather than three months means fewer "
            "concepts, earlier sign off and no window for a reshoot. A budget with "
            "no money for a shoot means building the work around typography and one "
            "licensed stock image rather than original photography. Resources of "
            "one camera and one editor mean a single location and a shot list one "
            "person can cover. Technical constraints such as a two megabyte limit, "
            "a nine by sixteen frame and a sixty second maximum mean heavier "
            "compression, a vertical master and a tighter edit. A legal constraint "
            "such as under sixteens appearing on camera means parental consent "
            "collected before the shoot rather than after it. A house style "
            "constraint means working within the client's existing fonts and "
            "palette rather than introducing new ones. A platform constraint such "
            "as a social feed rather than a cinema means captions, a hook in the "
            "first second and a product that works with the sound off. In every "
            "case the constraint on its own earns nothing; the decision that "
            "follows from it earns the mark.")
    return figure("imedia-constraints", 760, 384, "".join(body),
                  "Constraints and the decisions they force", desc,
                  "Every constraint rules some options out and forces others. "
                  "That is the answer the question wants.")


# ============================================================ judging a source

@diagram("imedia-source-check")
def _source():
    """Six tests for a secondary source, applied to one real-looking claim."""
    body = [text(380, 24, "Six tests, applied to one claim", 12, 650, fill=MUTED)]
    body.append(box(140, 44, 480, 56, None, fill=FILL2, stroke=LINE, r=8))
    body.append(text(380, 68, "“90% of teenagers prefer this platform”",
                     13, 700, fill="var(--dg-text)"))
    body.append(text(380, 88, "found on a blog, no date visible", 10, 450,
                     fill=MUTED))
    TESTS = [("Authority", "Who wrote it, and what do they know?",
              "A blog post with no named author"),
             ("Currency", "How old is it?",
              "Platform figures age in months, not years"),
             ("Purpose", "Why was it published, and who paid?",
              "A platform publishing its own popularity"),
             ("Evidence", "Does it say where the number came from?",
              "No sample size, no method, no link"),
             ("Corroboration", "Does an independent source agree?",
              "Check Ofcom; if nothing agrees, drop it"),
             ("Bias", "Does the publisher gain if you believe it?",
              "If yes, treat the number as marketing")]
    for i, (k, q, verdict) in enumerate(TESTS):
        col, row = i % 2, i // 2
        x, y = 28 + col * 356, 120 + row * 86
        body.append(box(x, y, 348, 74, None, fill=FILL, stroke=TEAL, r=8))
        body.append(text(x + 16, y + 22, k, 11.5, 700, anchor="start", fill=TEAL))
        body.append(text(x + 16, y + 40, q, 10, 500, anchor="start", fill=MUTED))
        body.append(box(x + 12, y + 48, 324, 20, None, fill=WARN_SOFT,
                        stroke=WARN, r=10))
        body.append(text(x + 174, y + 62, verdict, 9.5, 600, fill=WARN))
    body.append(text(380, 400, "Reliable is not the same as relevant. A perfect "
                     "source about a different year is still the wrong source.",
                     11, 600, fill=MUTED))
    desc = ("Six tests for judging a secondary source, applied to the claim that "
            "ninety per cent of teenagers prefer a particular platform, found on a "
            "blog with no visible date. Authority asks who wrote it and what they "
            "know; here it is a blog post with no named author. Currency asks how "
            "old it is; platform figures age in months rather than years. Purpose "
            "asks why it was published and who paid for it; a platform publishing "
            "research about its own popularity has an obvious interest. Evidence "
            "asks whether the source says where the number came from; here there is "
            "no sample size, no method and no link. Corroboration asks whether an "
            "independent source agrees, so the figure should be checked against "
            "Ofcom and dropped if nothing supports it. Bias asks whether the "
            "publisher gains if you believe it, and if the answer is yes the number "
            "should be treated as marketing. Finally, reliability is not the same as "
            "relevance: a perfectly reliable source about a different year or a "
            "different age group is still the wrong source.")
    return figure("imedia-source", 760, 416, "".join(body),
                  "Judging whether a source can be trusted", desc,
                  "Copyright is automatic and so is scepticism. Check the date "
                  "first; it fails more sources than anything else.")


# ============================================================== accessibility

@diagram("imedia-accessibility")
def _accessibility():
    """The same screen, failing and passing, with the reason on each fix."""
    body = [text(380, 24, "The same screen, before and after", 12, 650,
                 fill=MUTED)]

    def screen(x, ok):
        tone = TEAL if ok else WARN
        soft = TEAL_SOFT if ok else WARN_SOFT
        out = [box(x, 48, 300, 258, None, fill=FILL, stroke=tone, r=10),
               text(x + 150, 42, "PASSES" if ok else "FAILS", 11, 750, fill=tone)]
        # Heading.
        out.append(text(x + 150, 82, "Book your visit", 17 if ok else 13,
                        750 if ok else 400,
                        fill="var(--dg-text)" if ok else MUTED))
        # Body text, thin and pale when failing.
        for i in range(4):
            out.append(line(x + 24, 104 + i * (16 if ok else 12),
                            x + 276, 104 + i * (16 if ok else 12),
                            stroke=LINE if ok else FILL2, w=4 if ok else 2))
        # Image, with or without alt text.
        iy = 178 if ok else 162
        out.append(box(x + 24, iy, 120, 68, None, fill=FILL2, stroke=LINE, r=4))
        out.append(text(x + 84, iy + 32, "image", 10, 500, fill=MUTED))
        out.append(text(x + 84, iy + 48, 'alt="..."' if ok else "no alt text",
                        9, 600, fill=TEAL if ok else WARN))
        # Status, by colour alone or by colour plus text.
        out.append(circle(x + 172, iy + 14, 7, fill=tone, stroke=tone))
        out.append(text(x + 186, iy + 18,
                        "Sold out" if ok else "(colour only)", 9.5, 600,
                        anchor="start", fill=tone))
        # The button and its focus ring.
        out.append(box(x + 160, iy + 36, 116, 30 if ok else 20, None,
                       fill=soft, stroke=tone, r=6))
        out.append(text(x + 218, iy + (56 if ok else 50),
                        "Book tickets" if ok else "Go", 10.5, 650, fill=tone))
        if ok:
            out.append(box(x + 155, iy + 31, 126, 40, None, fill="none",
                           stroke=LILAC, r=9, dash="4 3"))
            out.append(text(x + 218, iy + 84, "visible keyboard focus", 9, 600,
                            fill=LILAC))
        return "".join(out)

    body.append(screen(28, False))
    body.append(screen(432, True))
    FIXES = [("Contrast at least 4.5:1", "pale grey on white is invisible to "
              "many readers"),
             ("Body text 16px or more, resizable", "and the layout still works "
              "at 200%"),
             ("Alt text on every meaningful image", "a screen reader has nothing "
              "else to read"),
             ("Never colour alone", "8% of men cannot separate red from green"),
             ("Tap targets around 44px", "a thumb is not a mouse pointer"),
             ("Visible keyboard focus", "many users never touch a mouse")]
    for i, (k, why) in enumerate(FIXES):
        y = 326 + i * 28
        body.append(box(28, y, 704, 24, None,
                        fill=FILL2 if i % 2 == 0 else FILL, stroke="none", r=4))
        body.append(text(44, y + 16, k, 10.5, 700, anchor="start", fill=TEAL))
        body.append(text(330, y + 16, why, 10, 450, anchor="start", fill=MUTED))
    desc = ("The same booking screen drawn twice, failing and passing "
            "accessibility. The failing version has a small, light heading, thin "
            "pale body text, an image with no alternative text, a status indicated "
            "by colour alone, a small button and no visible keyboard focus. The "
            "passing version has a large bold heading, body text at a readable "
            "weight and size, an image with alternative text, a status given as "
            "both a colour and the word 'sold out', a larger button and a visible "
            "focus ring around it. The fixes, with the reason for each: contrast of "
            "at least four and a half to one, because pale grey on white is "
            "effectively invisible to many readers; body text of sixteen pixels or "
            "more that can be resized, with the layout still working at two hundred "
            "per cent; alternative text on every meaningful image, because a screen "
            "reader has nothing else to read; never using colour alone, because "
            "around eight per cent of men cannot separate red from green; tap "
            "targets of about forty four pixels, because a thumb is not a mouse "
            "pointer; and a visible keyboard focus indicator, because many users "
            "never touch a mouse at all.")
    return figure("imedia-a11y", 760, 500, "".join(body),
                  "An inaccessible screen and the same screen fixed", desc,
                  "Accessibility is part of designing for the audience, and "
                  "under the Equality Act it is also a legal duty.")


# ================================================== streaming and downloading

@diagram("imedia-streaming-download")
def _streaming():
    """Where the file sits, and what that means for the viewer."""
    body = [text(380, 24, "Streaming and downloading: where the file actually is",
                 12, 650, fill=MUTED)]

    def row(y, title, tone, soft, server_note, device_note, flow_label, dashed):
        out = [text(70, y + 6, title, 13, 750, anchor="start", fill=tone),
               box(170, y - 18, 160, 64, None, fill=soft, stroke=tone, r=8),
               text(250, y + 4, "SERVER", 11, 700, fill=tone),
               text(250, y + 22, server_note, 9.5, 450, fill=MUTED),
               box(470, y - 18, 190, 64, None, fill=FILL, stroke=tone, r=8),
               text(565, y + 4, "DEVICE", 11, 700, fill=tone),
               text(565, y + 22, device_note, 9.5, 450, fill=MUTED)]
        out.append(line(334, y + 14, 464, y + 14, stroke=tone, w=2,
                        dash="5 4" if dashed else None, arrow=True))
        out.append(chip(399, y - 2, flow_label, fill=soft, stroke=tone,
                        text_fill=tone))
        return "".join(out)

    body.append(row(76, "STREAMING", TEAL, TEAL_SOFT,
                    "keeps the file", "a small buffer only",
                    "continuous", True))
    body.append(row(186, "DOWNLOADING", LILAC, LILAC_SOFT,
                    "sends it once", "holds the whole file",
                    "once, then done", False))

    ROWS = [("Starts playing", "almost at once", "only when the transfer finishes"),
            ("Storage used", "almost none", "the full file size"),
            ("Needs a connection", "throughout", "only while downloading"),
            ("Works offline", "no", "yes, as often as you like"),
            ("Who holds the copy", "the platform", "the user"),
            ("Suits", "watch once, live, discovery",
             "offline use, repeat listening, archiving")]
    body.append(text(250, 272, "STREAMING", 11, 750, fill=TEAL))
    body.append(text(560, 272, "DOWNLOADING", 11, 750, fill=LILAC))
    for i, (k, a, b) in enumerate(ROWS):
        y = 284 + i * 28
        body.append(box(28, y, 704, 24, None,
                        fill=FILL2 if i % 2 == 0 else FILL, stroke="none", r=4))
        body.append(text(44, y + 16, k, 10.5, 700, anchor="start", fill=MUTED))
        body.append(text(250, y + 16, a, 10.5, 500, fill=TEAL))
        body.append(text(560, y + 16, b, 10.5, 500, fill=LILAC))
    desc = ("Streaming and downloading compared by where the file sits. In "
            "streaming, the server keeps the file and sends it continuously while "
            "the device holds only a small buffer. In downloading, the server sends "
            "the file once and the device then holds the whole thing. The table "
            "compares them. Streaming starts playing almost at once, while a "
            "download only plays when the transfer finishes. Streaming uses almost "
            "no storage; a download uses the full file size. Streaming needs a "
            "connection throughout; a download needs one only while downloading. "
            "Streaming does not work offline; a download does, as often as the user "
            "likes. With streaming the platform holds the copy; with downloading "
            "the user does. Streaming suits watch once content, live events and "
            "discovery; downloading suits offline use, repeat listening and "
            "archiving.")
    return figure("imedia-stream", 760, 468, "".join(body),
                  "Streaming compared with downloading", desc,
                  "Streaming trades storage and offline access for an instant "
                  "start. That trade is the whole answer.")


# =============================================================== test records

@diagram("imedia-test-record")
def _testrecord():
    """A test record that an assessor believes, and one they do not."""
    body = [text(380, 24, "A test record with no failures in it is not a test "
                 "record", 12, 650, fill=MUTED)]
    COLS = [(30, 60, "#"), (90, 190, "Test"), (280, 150, "Data or action"),
            (430, 140, "Expected"), (570, 160, "Actual and fix")]
    for x, w, label in COLS:
        body.append(box(x, 48, w, 28, None, fill=TEAL_SOFT, stroke=TEAL, r=4))
        body.append(text(x + w / 2, 67, label, 10.5, 700, fill=TEAL))
    ROWS = [("1", "Home to Topic 3", "Tap Topic 3", "Topic 3 opens",
             "As expected", True),
            ("2", "Back during video", "Tap Back while playing",
             "Returns, audio stops", "Audio kept playing → stop on unload, "
             "retested", False),
            ("3", "Form, empty field", "Submit with name blank",
             "Error message shown", "Form submitted → validation added",
             False),
            ("4", "Form, 300 characters", "Paste 300 chars into name",
             "Rejected or truncated", "As expected", True),
            ("5", "Keyboard only", "Tab through every control",
             "All reachable, focus visible", "Menu skipped → tabindex fixed",
             False),
            ("6", "Phone, 360px wide", "Open on a 360px screen",
             "Single column, no scroll", "As expected", True)]
    for i, (n, t, d, e, a, ok) in enumerate(ROWS):
        y = 80 + i * 36
        tone = TEAL if ok else WARN
        soft = FILL if ok else WARN_SOFT
        for (x, w, _), val in zip(COLS, (n, t, d, e, a)):
            body.append(box(x, y, w, 32, None, fill=soft, stroke=LINE, r=4))
            body.append(text(x + w / 2, y + 20, val, 9 if len(val) > 26 else 9.8,
                             550 if x == 30 else 450,
                             fill=tone if x == 570 else "var(--dg-text)"))
    body.append(box(30, 302, 700, 56, None, fill=TEAL_SOFT, stroke=TEAL, r=8))
    body.append(text(380, 322, "The expected result is written BEFORE the test is "
                     "run", 11, 700, fill=TEAL))
    body.append(text(380, 340, "Otherwise there is nothing to compare against, and "
                     "the test only confirms whatever happened.", 10, 500,
                     fill=MUTED))
    desc = ("A test record table with six rows, three of which record failures and "
            "their fixes. The columns are the test number, the test, the data or "
            "action used, the expected result and the actual result with the fix. "
            "Test one navigates from home to topic three and passes. Test two taps "
            "Back during video playback, expecting the audio to stop; the audio kept "
            "playing, so a stop on unload was added and the test repeated. Test "
            "three submits the form with the name field blank, expecting an error "
            "message; the form submitted anyway, so validation was added. Test four "
            "pastes three hundred characters into the name field and passes. Test "
            "five tabs through every control using the keyboard only, expecting all "
            "controls reachable with a visible focus; the menu was skipped, so the "
            "tab order was fixed. Test six opens the product on a three hundred and "
            "sixty pixel wide phone screen and passes. The important discipline is "
            "that the expected result is written before the test is run, because "
            "otherwise there is nothing to compare the outcome against and the test "
            "merely confirms whatever happened.")
    return figure("imedia-test", 760, 372, "".join(body),
                  "A believable test record", desc,
                  "Record the failures and the fixes. A log of six passes "
                  "convinces nobody, including the assessor.")
