"""AI course diagrams, Levels 1 to 3: the history of AI, what AI is and how
machines learn, and data.

Vivid colours and 3D come from diagrams_ai_kit, which explains the contrast
rules that keep them readable in both themes. Registered into the shared
diagram registry, so `!diagram <name>` works as everywhere else.
"""
import math

from .diagrams import diagram
from .svg import figure, text, line, path, circle, esc
from .diagrams_ai_kit import (INK, MUTED, FILL, FILL2, LINE, VIOLET, PINK, BLUE,
                              TEAL, GREEN, ORANGE, RED, INDIGO, AMBER, LIME,
                              CYAN, ROSE, SKY, PURPLE, SLATE, WHITE, DARK, tv, solid,
                              tint, grad, plasma, ink_on, arrow, cube, heat,
                              diverging, neuron, mlp, surface, project)


def _smooth(points):
    """A smooth path through points (Catmull-Rom turned into cubic Beziers)."""
    d = "M%.1f %.1f" % points[0]
    for i in range(len(points) - 1):
        p0 = points[i - 1] if i > 0 else points[i]
        p1, p2 = points[i], points[i + 1]
        p3 = points[i + 2] if i + 2 < len(points) else p2
        c1 = (p1[0] + (p2[0] - p0[0]) / 6.0, p1[1] + (p2[1] - p0[1]) / 6.0)
        c2 = (p2[0] - (p3[0] - p1[0]) / 6.0, p2[1] - (p3[1] - p1[1]) / 6.0)
        d += " C%.1f %.1f %.1f %.1f %.1f %.1f" % (c1 + c2 + p2)
    return d


def _legend(items, x, y, gap=22, size=10):
    """A row of coloured dots with labels."""
    out, cx = [], x
    for colour, label in items:
        out.append(circle(cx, y - 3.5, 5.5, fill=colour, stroke=FILL, w=1.4))
        out.append(text(cx + 10, y, label, size, 600, anchor="start", fill=MUTED))
        cx += 10 + len(label) * size * 0.62 + gap
    return "".join(out)


# ================================================== Level 1: early timeline

@diagram("ai-timeline-early")
def _timeline_early():
    """From Lovelace to Watson: events alternating above and below an axis."""
    AX = 214

    def X(year):
        return 34 if year < 1900 else 60 + (year - 1940) * 9.4

    EV = [(1843, "A1", 22, "Ada Lovelace", "can a machine create?", VIOLET),
          (1943, "B1", 30, "McCulloch and Pitts", "a neuron made of logic", PINK),
          (1950, "A2", 96, "Alan Turing asks", "can machines think?", VIOLET),
          (1956, "B2", 152, "Dartmouth workshop", "the field is named", VIOLET),
          (1958, "A3", 164, "Rosenblatt", "the perceptron learns", PINK),
          (1966, "A1", 246, "ELIZA", "chat by pattern rules", BLUE),
          (1969, "B3", 274, "Perceptrons book", "limits of one layer", PINK),
          (1973, "A2", 312, "Lighthill Report", "UK funding is cut", SLATE),
          (1980, "B1", 378, "Expert systems", "rules go commercial", BLUE),
          (1986, "A3", 434, "Backpropagation", "trains hidden layers", PINK),
          (1997, "B2", 538, "Deep Blue", "beats Kasparov at chess", ORANGE),
          (2009, "A1", 612, "ImageNet", "14 million labelled images", GREEN),
          (2011, "B3", 612, "IBM Watson", "wins at Jeopardy!", ORANGE)]
    TIER = {"A1": 44, "A2": 98, "A3": 152, "B1": 232, "B2": 286, "B3": 340}
    body = [text(380, 22, "Thinking machines: from Lovelace to Watson", 12, 650,
                 fill=MUTED)]
    body.append(grad("ai-tl1-g", [(0, VIOLET), (0.5, PINK), (1, ORANGE)]))
    body.append('<rect x="22" y="%d" width="718" height="6" rx="3" fill="url(#ai-tl1-g)"/>'
                % (AX - 3))
    # the break between 1843 and 1940
    body.append('<rect x="44" y="%d" width="10" height="14" fill="var(--dg-paper)"/>' % (AX - 7))
    body.append(path("M42 %d l4 -6 l4 12 l4 -6" % AX, stroke=MUTED, w=1.4))
    for y0, y1, label in ((1974, 1980, "winter 1"), (1987, 1993, "winter 2")):
        x0, x1 = X(y0), X(y1)
        body.append('<rect x="%.1f" y="%d" width="%.1f" height="18" rx="4" fill="%s"/>'
                    % (x0, AX - 9, x1 - x0, SLATE))
        body.append(text((x0 + x1) / 2, AX + 4, label, 8, 700, fill=WHITE))
    for year, tier, bx, title, detail, colour in EV:
        x = X(year)
        y = TIER[tier]
        above = tier.startswith("A")
        if above:
            body.append(line(x, y + 46, x, AX - 6, stroke=tv(colour), w=1.3))
        else:
            body.append(line(x, AX + 6, x, y, stroke=tv(colour), w=1.3))
        body.append(tint(bx, y, 132, 46, colour, r=8, op=0.12))
        body.append(text(bx + 10, y + 15, str(year), 11.5, 800, anchor="start",
                         fill=tv(colour)))
        body.append(text(bx + 10, y + 29, title, 9.6, 700, anchor="start", fill=INK))
        body.append(text(bx + 10, y + 41, detail, 8.8, 500, anchor="start", fill=MUTED))
        body.append(circle(x, AX, 6, fill=colour, stroke=FILL, w=1.8))
    body.append(_legend([(VIOLET, "ideas"), (PINK, "neural networks"),
                         (BLUE, "rules and symbols"), (ORANGE, "milestones"),
                         (GREEN, "data"), (SLATE, "AI winters")], 30, 420))
    desc = ("A timeline of artificial intelligence from 1843 to 2011, with "
            "events alternating above and below a coloured axis. 1843: Ada "
            "Lovelace asks whether a machine can create. 1943: McCulloch and "
            "Pitts describe a neuron made of logic. 1950: Alan Turing asks "
            "whether machines can think. 1956: the Dartmouth workshop names the "
            "field. 1958: Rosenblatt's perceptron learns. 1966: ELIZA chats "
            "using pattern rules. 1969: the book Perceptrons shows the limits of "
            "one layer. 1973: the Lighthill Report leads to UK funding cuts, and "
            "the first AI winter runs from 1974 to 1980. 1980: expert systems "
            "take rules commercial. 1986: backpropagation trains hidden layers. "
            "A second AI winter runs from 1987 to 1993. 1997: Deep Blue beats "
            "Kasparov at chess. 2009: ImageNet provides 14 million labelled "
            "images. 2011: IBM Watson wins at Jeopardy! The events are coloured "
            "as ideas, neural networks, rules and symbols, milestones, data and "
            "AI winters.")
    return figure("ai-tl1", 760, 440, "".join(body),
                  "AI history from 1843 to 2011", desc,
                  "Ideas, then rules, then learning: and two winters in between.")


# ================================================ Level 1: summers, winters

@diagram("ai-seasons")
def _seasons():
    """Excitement and funding over time, with the two winters shaded."""
    X0, X1, Y0, Y1 = 70, 720, 300, 60

    def X(year):
        return X0 + (year - 1950) * (X1 - X0) / 75.0

    def Y(v):
        return Y0 - v * (Y0 - Y1)

    PTS = [(1950, .22), (1956, .45), (1962, .6), (1966, .68), (1970, .55),
           (1974, .25), (1978, .2), (1981, .32), (1984, .62), (1986, .66),
           (1988, .42), (1990, .24), (1993, .2), (1997, .3), (2001, .33),
           (2006, .38), (2010, .46), (2013, .58), (2016, .72), (2019, .8),
           (2022, .92), (2025, .98)]
    pts = [(X(y), Y(v)) for y, v in PTS]
    body = [text(380, 22, "AI's summers and winters: excitement and funding over "
                 "time", 12, 650, fill=MUTED)]
    body.append(grad("ai-seasons-g", [(0, PINK), (1, VIOLET)], x2=0, y2=1))
    for y0, y1, label in ((1974, 1980, "first AI winter"), (1987, 1993, "second AI winter")):
        body.append('<rect x="%.1f" y="%d" width="%.1f" height="%d" fill="%s" '
                    'fill-opacity="0.16"/>' % (X(y0), Y1 - 10, X(y1) - X(y0), Y0 - Y1 + 10, SLATE))
        body.append(text((X(y0) + X(y1)) / 2, Y0 + 30, label, 9.4, 700, fill=tv(SLATE)))
    curve = _smooth(pts)
    body.append('<path d="%s L%.1f %d L%.1f %d Z" fill="url(#ai-seasons-g)" '
                'fill-opacity="0.22"/>' % (curve, pts[-1][0], Y0, pts[0][0], Y0))
    body.append(path(curve, stroke=tv(PINK), w=3))
    body.append(line(X0, Y0, X1 + 10, Y0, stroke=LINE, w=1.4))
    for year in range(1950, 2030, 10):
        body.append(line(X(year), Y0, X(year), Y0 + 5, stroke=LINE, w=1.2))
        body.append(text(X(year), Y0 + 18, str(year), 9.4, 600, fill=MUTED))
    body.append('<text x="34" y="%d" text-anchor="middle" font-size="10.5" '
                'font-weight="650" fill="%s" transform="rotate(-90 34 %d)">'
                'excitement and funding</text>' % ((Y0 + Y1) / 2, MUTED, (Y0 + Y1) / 2))
    NOTES = [(1956, .45, "Dartmouth names AI", -1, 18),
             (1966, .68, "big promises", -1, 14),
             (1973, .3, "Lighthill Report", 1, 36),
             (1985, .64, "expert systems boom", -1, 34),
             (1988, .42, "AI hardware collapses", 0, 0),
             (2012, .55, "deep learning", -1, 20),
             (2022, .92, "generative AI", -1, 14)]
    for year, v, label, side, off in NOTES:
        x, y = X(year), Y(v)
        body.append(circle(x, y, 4.5, fill=VIOLET, stroke=FILL, w=1.5))
        if side == 0:             # beside the dot, clear of a steep curve
            body.append(text(x + 10, y + 3.5, label, 9.6, 700, anchor="start", fill=INK))
            continue
        ty = y - off if side < 0 else y + off
        body.append(line(x, y + (-5 if side < 0 else 5), x, ty + (4 if side < 0 else -12),
                         stroke=LINE, w=1))
        body.append(text(x, ty, label, 9.6, 700, fill=INK))
    body.append(text(X1, Y0 + 44, "illustrative shape, not measured data", 8.8, 500,
                     anchor="end", fill=MUTED))
    desc = ("A curve of excitement and funding for AI from 1950 to 2025. It rises "
            "after Dartmouth names AI in 1956 and peaks in the mid 1960s amid big "
            "promises, then falls into the first AI winter, shaded from 1974 to "
            "1980, after the Lighthill Report. It rises again with the expert "
            "systems boom of the mid 1980s, then falls into the second AI winter, "
            "shaded from 1987 to 1993, after the market for AI hardware collapses. "
            "From the late 1990s it climbs slowly, then steeply with deep learning "
            "from 2012 and generative AI from 2022, reaching its highest point. "
            "The shape is illustrative rather than measured.")
    return figure("ai-seasons", 760, 360, "".join(body),
                  "AI's summers and winters", desc,
                  "Every winter followed promises the technology could not yet keep.")


# ============================================ Level 1: the three ingredients

@diagram("ai-three-ingredients")
def _ingredients():
    """Data, compute and algorithms overlapping, with deep learning in the middle."""
    body = [text(380, 22, "Why 2012? Three ingredients arrived at the same time", 12,
                 650, fill=MUTED)]
    C = [(240, 140, VIOLET), (360, 140, PINK), (300, 238, BLUE)]
    for cx, cy, col in C:
        body.append('<circle cx="%d" cy="%d" r="100" fill="%s" fill-opacity="0.26" '
                    'stroke="%s" stroke-width="2.2"/>' % (cx, cy, col, tv(col)))
    body.append(text(205, 110, "DATA", 14, 800, fill=tv(VIOLET)))
    body.append(text(205, 128, "labelled examples", 9.6, 600, fill=MUTED))
    body.append(text(398, 110, "COMPUTE", 14, 800, fill=tv(PINK)))
    body.append(text(398, 128, "parallel hardware", 9.6, 600, fill=MUTED))
    body.append(text(300, 290, "ALGORITHMS", 14, 800, fill=tv(BLUE)))
    body.append(text(300, 307, "better training ideas", 9.6, 600, fill=MUTED))
    body.append(solid(246, 158, 108, 38, INDIGO, "deep learning", "2012 onwards",
                      r=19, size=11, sub_size=8.8))
    ROWS = [(VIOLET, "Data", ["ImageNet: 14 million labelled", "images; the web; phones"]),
            (PINK, "Compute", ["GPUs built for games do", "thousands of sums at once"]),
            (BLUE, "Algorithms", ["ReLU, dropout, better start", "values; later, attention"])]
    for i, (col, k, lines) in enumerate(ROWS):
        y = 52 + i * 92
        body.append(tint(500, y, 236, 80, col, r=10, op=0.1))
        body.append(solid(512, y + 12, 86, 24, col, k, r=12, size=10.5))
        body.append(text(512, y + 52, lines[0], 9.6, 600, anchor="start", fill=INK))
        body.append(text(512, y + 68, lines[1], 9.6, 600, anchor="start", fill=INK))
    desc = ("A Venn diagram of three overlapping circles: data, meaning labelled "
            "examples; compute, meaning parallel hardware; and algorithms, "
            "meaning better training ideas. Where all three overlap sits deep "
            "learning, from 2012 onwards. Beside it, examples of each: for data, "
            "ImageNet's 14 million labelled images, the web and phones; for "
            "compute, GPUs built for games doing thousands of sums at once; for "
            "algorithms, ReLU, dropout and better starting values, and later "
            "attention.")
    return figure("ai-ingr", 760, 336, "".join(body),
                  "The three ingredients of deep learning", desc,
                  "Each ingredient existed before 2012. Having all three at once "
                  "was new.")


# ============================================== Level 1: modern timeline

@diagram("ai-timeline-modern")
def _timeline_modern():
    """2012 to 2025 as a vertical timeline, cards alternating left and right."""
    EV = [(2012, PINK, "AlexNet wins ImageNet", "15.3% error against 26.2%: deep learning arrives"),
          (2014, PINK, "GANs", "a forger network against a detective network"),
          (2016, ORANGE, "AlphaGo beats Lee Sedol", "4 games to 1 at Go, with the famous move 37"),
          (2017, VIOLET, "The Transformer", "Attention Is All You Need: the engine of LLMs"),
          (2018, VIOLET, "BERT and GPT", "pretrain on text, then adapt to many tasks"),
          (2020, VIOLET, "GPT-3", "175 billion parameters; learns from examples"),
          (2020, GREEN, "AlphaFold 2", "protein shapes at near-laboratory accuracy"),
          (2022, PINK, "Stable Diffusion", "text-to-image generation on a home computer"),
          (2022, ORANGE, "ChatGPT", "a chat window brings LLMs to millions"),
          (2023, VIOLET, "GPT-4 and open models", "text and images; open weights spread fast"),
          (2023, BLUE, "Bletchley Park safety summit", "28 countries and the EU sign a declaration"),
          (2024, GREEN, "Nobel Prizes and the EU AI Act", "AI research honoured; the first broad AI law"),
          (2025, VIOLET, "Reasoning models and agents", "step by step thinking, tools and actions")]
    body = [text(380, 22, "The deep learning era, 2012 to today", 12, 650, fill=MUTED)]
    body.append(grad("ai-tl2-g", [(0, PINK), (0.5, VIOLET), (1, ORANGE)], x2=0, y2=1))
    top, step = 62, 42
    body.append('<rect x="377" y="%d" width="6" height="%d" rx="3" fill="url(#ai-tl2-g)"/>'
                % (top - 18, step * (len(EV) - 1) + 36))
    for i, (year, col, title, detail) in enumerate(EV):
        y = top + i * step
        left = i % 2 == 0
        cx0 = 26 if left else 404
        body.append(line(356 if left else 404, y, 374 if left else 386, y,
                         stroke=tv(col), w=1.6))
        body.append(tint(cx0, y - 18, 330, 36, col, r=8, op=0.1))
        body.append(solid(cx0 + 8, y - 11, 46, 22, col, str(year), r=11, size=10.5))
        body.append(text(cx0 + 64, y - 2, title, 10.4, 750, anchor="start", fill=INK))
        body.append(text(cx0 + 64, y + 12, detail, 9, 500, anchor="start", fill=MUTED))
        body.append(circle(380, y, 7, fill=col, stroke=FILL, w=2))
    body.append(_legend([(PINK, "vision and generation"), (VIOLET, "language"),
                         (ORANGE, "games and products"), (GREEN, "science"),
                         (BLUE, "society and law")], 40, 618))
    desc = ("A vertical timeline from 2012 to 2025. 2012: AlexNet wins ImageNet "
            "with 15.3 percent error against 26.2 percent, and deep learning "
            "arrives. 2014: GANs set a forger network against a detective "
            "network. 2016: AlphaGo beats Lee Sedol 4 games to 1 at Go, with the "
            "famous move 37. 2017: the Transformer, from the paper Attention Is "
            "All You Need, becomes the engine of large language models. 2018: "
            "BERT and GPT pretrain on text and adapt to many tasks. 2020: GPT-3 "
            "has 175 billion parameters and learns from examples; AlphaFold 2 "
            "predicts protein shapes at near-laboratory accuracy. 2022: Stable "
            "Diffusion brings text-to-image generation to home computers, and "
            "ChatGPT brings language models to millions. 2023: GPT-4 handles text "
            "and images and open model weights spread fast; at the Bletchley Park "
            "safety summit 28 countries and the EU sign a declaration. 2024: AI "
            "research wins Nobel Prizes and the EU AI Act, the first broad AI law, "
            "enters into force. 2025: reasoning models and agents that think step "
            "by step, use tools and take actions.")
    return figure("ai-tl2", 760, 640, "".join(body),
                  "AI history from 2012 to today", desc,
                  "Thirteen years from a better image classifier to systems that "
                  "write, draw, reason and act.")


# ================================================ Level 1: growth of compute

@diagram("ai-growth-curve")
def _growth():
    """What four times a year looks like on a log scale, against Moore's law."""
    X0, Y0, W, H = 96, 292, 600, 232
    TOP = 8.0                     # log10 of the top of the axis

    def Y(v):
        return Y0 - H * math.log10(v) / TOP

    body = [text(380, 22, "What “four times more every year” means", 12, 650,
                 fill=MUTED)]
    for p in range(0, 9, 2):
        y = Y(10 ** p)
        body.append(line(X0, y, X0 + W, y, stroke=LINE, w=0.8, dash="2 5"))
        lab = "1" if p == 0 else "{:,}".format(10 ** p)
        body.append(text(X0 - 8, y + 3.5, "×" + lab, 9.4, 600, anchor="end",
                         fill=MUTED))
    bw = W / 13.0
    for i in range(13):
        v = 4 ** i
        x = X0 + i * bw + 5
        y = Y(v)
        col = plasma(0.15 + 0.8 * i / 12.0)
        body.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="3" fill="%s"/>'
                    % (x, y, bw - 10, Y0 - y, col))
        body.append(text(x + (bw - 10) / 2, Y0 + 16, str(2012 + i), 9, 600, fill=MUTED))
    for i, lab in ((0, "×1"), (4, "×256"), (8, "×65,536"),
                   (12, "×16.8 million")):
        x = X0 + i * bw + bw / 2
        body.append(text(x, Y(4 ** i) - 8, lab, 10, 800, fill=INK))
    # Moore's law: twice every two years
    moore = [(X0 + i * bw + bw / 2, Y(2 ** (i / 2.0))) for i in range(13)]
    body.append(path("M" + " L".join("%.1f %.1f" % p for p in moore), stroke=tv(TEAL),
                     w=2.4, dash="6 4"))
    body.append(path("M%d 42 h26" % (X0 + 10), stroke=tv(TEAL), w=2.4, dash="6 4"))
    body.append(text(X0 + 42, 45.5, "Moore's law pace, doubling every two years: "
                     "only ×64 by 2024", 9.6, 750, anchor="start", fill=tv(TEAL)))
    body.append(line(X0, Y0, X0 + W, Y0, stroke=LINE, w=1.4))
    body.append(text(X0 + W / 2, Y0 + 36, "each bar is four times the one before; "
                     "each grid line is 100 times the one below", 9.6, 600, fill=MUTED))
    desc = ("A bar chart on a logarithmic scale showing growth of four times a "
            "year from 2012 to 2024. Each bar is four times taller in value than "
            "the one before: times 1 in 2012, times 256 by 2016, times 65,536 by "
            "2020 and times 16.8 million by 2024, while each grid line is 100 "
            "times the one below it. A dashed line shows the pace of Moore's law, "
            "doubling every two years, which reaches only times 64 over the same "
            "period.")
    return figure("ai-growth", 760, 340, "".join(body),
                  "Exponential growth in training compute", desc,
                  "Epoch AI's tracking finds that training compute for notable "
                  "models grew about four to five times a year from 2010.")


# ================================================== Level 2: the AI family

def _shade(colour, f):
    """A darker (f < 1) or lighter (f > 1) version of a #RRGGBB colour."""
    r, g, b = (int(colour[i:i + 2], 16) for i in (1, 3, 5))
    if f < 1:
        return "#%02X%02X%02X" % tuple(int(c * f) for c in (r, g, b))
    return "#%02X%02X%02X" % tuple(int(c + (255 - c) * (f - 1)) for c in (r, g, b))


def _disc(cx, cy, rx, ry, t, colour):
    """A solid disc seen from above and in front: a side band, then the top."""
    side = ('<path d="M%.1f %.1f L%.1f %.1f A%.1f %.1f 0 0 0 %.1f %.1f L%.1f %.1f '
            'A%.1f %.1f 0 0 1 %.1f %.1f Z" fill="%s"/>'
            % (cx - rx, cy, cx - rx, cy + t, rx, ry, cx + rx, cy + t, cx + rx, cy,
               rx, ry, cx - rx, cy, _shade(colour, 0.62)))
    top = ('<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s"/>'
           % (cx, cy, rx, ry, colour))
    return side + top


@diagram("ai-family")
def _family():
    """AI, machine learning, deep learning and generative AI as stacked discs."""
    body = [text(380, 22, "Each field sits inside the one below it", 12, 650, fill=MUTED)]
    CX, T = 290, 30
    TIERS = [(VIOLET, 262, "ARTIFICIAL INTELLIGENCE"), (BLUE, 202, "MACHINE LEARNING"),
             (TEAL, 142, "DEEP LEARNING"), (PINK, 84, "GENERATIVE AI")]
    NOTES = [("Artificial intelligence", "any way to make machines act",
              "intelligently: search, rules, learning"),
             ("Machine learning", "learns its behaviour from data",
              "instead of following written rules"),
             ("Deep learning", "machine learning with many-",
              "layered neural networks"),
             ("Generative AI", "deep learning that creates text,",
              "images, audio, video and code")]
    y = 300
    tops = []
    for colour, rx, _label in TIERS:
        ry = rx * 0.26
        body.append(_disc(CX, y, rx, ry, T, colour))
        tops.append((y, rx, ry))
        y -= T + 14
    for i, (colour, rx, label) in enumerate(TIERS):
        y, rx, ry = tops[i]
        if i + 1 < len(tops):
            ly = y + (ry + tops[i + 1][2]) / 2.0 + 4
        else:
            ly = y + 4
        body.append(text(CX, ly, label, 11.5 if i < 3 else 11, 800, fill=WHITE))
        # leader line from the right rim to the note
        nx, ny = 584, 64 + (3 - i) * 74
        ex = CX + rx * 0.92
        ey = y + ry * 0.39
        body.append(path("M%.1f %.1f L%.1f %.1f L%d %.1f" % (ex, ey, ex + 14, ny - 4, nx - 8, ny - 4),
                         stroke=tv(colour), w=1.3))
        circle_dot = '<circle cx="%.1f" cy="%.1f" r="3.2" fill="%s"/>' % (ex, ey, colour)
        body.append(circle_dot)
        title, l1, l2 = NOTES[i]
        body.append(text(nx, ny, title, 10.5, 800, anchor="start", fill=tv(colour)))
        body.append(text(nx, ny + 15, l1, 9, 500, anchor="start", fill=MUTED))
        body.append(text(nx, ny + 28, l2, 9, 500, anchor="start", fill=MUTED))
    desc = ("Four solid discs stacked like a tiered cake, each smaller than the one "
            "below. The largest, at the bottom, is artificial intelligence: any way "
            "to make machines act intelligently, including search, rules and "
            "learning. On it sits machine learning, which learns its behaviour from "
            "data instead of following written rules. On that sits deep learning, "
            "machine learning with many-layered neural networks. On top is "
            "generative AI, deep learning that creates text, images, audio, video "
            "and code.")
    return figure("ai-family", 760, 380, "".join(body),
                  "The AI family: AI, machine learning, deep learning, generative AI",
                  desc, "All generative AI is deep learning, all deep learning is "
                  "machine learning, and all machine learning is AI. Not the other "
                  "way round.")


# ======================================= Level 2: rules versus learning

def _pill(x, y, w, colour, label, h=30):
    return solid(x, y, w, h, colour, label, r=h / 2.0, size=11)


@diagram("ai-rules-vs-learning")
def _rules_vs_learning():
    """Rules and data give answers; data and answers give rules."""
    body = [text(380, 22, "Turn the arrows around and you have machine learning", 12,
                 650, fill=MUTED)]
    rows = [(58, "Traditional programming", [(VIOLET, "Rules"), (BLUE, "Data")],
             SLATE, "Computer runs\nthe program", (GREEN, "Answers")),
            (186, "Machine learning", [(BLUE, "Data"), (GREEN, "Answers")],
             ORANGE, "Computer\nlearns", (VIOLET, "Rules: a model"))]
    for y, title, ins, mid_col, mid_label, out in rows:
        body.append(text(30, y - 10, title, 11.5, 800, anchor="start", fill=INK))
        for k, (col, lab) in enumerate(ins):
            body.append(_pill(30, y + k * 42, 120, col, lab))
            body.append(arrow(154, y + 15 + k * 42, 300, y + 36, tv(col), 2))
        body.append(cube(306, y + 4, 128, 64, 26, mid_col))
        l1, l2 = mid_label.split("\n")
        body.append(text(370, y + 32, l1, 11, 750, fill=WHITE))
        body.append(text(370, y + 48, l2, 11, 750, fill=WHITE))
        body.append(arrow(458, y + 36, 548, y + 36, tv(out[0]), 2.2))
        body.append(_pill(554, y + 21, 170, out[0], out[1]))
    # the learned model being used
    body.append(path("M639 253 C 639 300, 560 312, 470 312", stroke=tv(VIOLET), w=1.8,
                     dash="5 4"))
    body.append(arrow(476, 312, 444, 312, tv(VIOLET), 1.8))
    body.append(tint(206, 296, 236, 32, VIOLET, op=0.12, r=16))
    body.append(text(324, 316, "new data + model = predictions", 10.5, 700, fill=INK))
    body.append(text(640, 290, "then used on", 9.4, 600, anchor="start", fill=MUTED))
    body.append(text(640, 302, "data it has never seen", 9.4, 600, anchor="start",
                     fill=MUTED))
    desc = ("Two rows. Traditional programming: rules and data go into a computer "
            "that runs the program, and answers come out. Machine learning: data and "
            "answers go into a computer that learns, and rules come out, called a "
            "model. A dashed arrow shows the model then being used with new data to "
            "make predictions.")
    return figure("ai-rvl", 760, 344, "".join(body),
                  "Traditional programming compared with machine learning", desc,
                  "In machine learning the rules are the output, not the input.")


# =========================================== Level 2: the agent loop

@diagram("ai-agent-loop")
def _agent_loop():
    """An agent perceives its environment and acts on it, in a loop."""
    body = [text(380, 22, "An agent: perceive, decide, act, and again", 12, 650,
                 fill=MUTED)]
    body.append(tint(40, 86, 230, 190, VIOLET, op=0.12, r=16))
    body.append(text(155, 112, "AGENT", 13, 800, fill=tv(VIOLET)))
    for k, (col, lab, sub) in enumerate([(BLUE, "Sensors", "camera, microphone, text in"),
                                         (VIOLET, "Decide", "rules, search or a model"),
                                         (ORANGE, "Actuators", "wheels, speaker, text out")]):
        y = 126 + k * 48
        body.append(solid(58, y, 194, 40, col, lab, sub, r=10, size=11, sub_size=8.6))
    body.append(tint(490, 86, 230, 190, GREEN, op=0.12, r=16))
    body.append(text(605, 112, "ENVIRONMENT", 13, 800, fill=tv(GREEN)))
    for k, lab in enumerate(["a road and its traffic", "a chess board",
                             "a conversation", "a living room floor"]):
        body.append(tint(512, 128 + k * 36, 186, 28, GREEN, lab, r=14, size=10, op=0.18))
    # perceive (top arc) and act (bottom arc)
    body.append(path("M520 82 C 470 30, 330 30, 262 92", stroke=tv(BLUE), w=2.6))
    body.append(arrow(276, 80, 258, 96, tv(BLUE), 2.6))
    body.append(solid(330, 34, 100, 26, BLUE, "perceive", r=13, size=10.5))
    body.append(path("M262 268 C 330 330, 470 330, 512 286", stroke=tv(ORANGE), w=2.6))
    body.append(arrow(500, 296, 516, 280, tv(ORANGE), 2.6))
    body.append(solid(340, 304, 80, 26, ORANGE, "act", r=13, size=10.5))
    body.append(text(380, 182, "the loop repeats,", 9.6, 650, fill=MUTED))
    body.append(text(380, 196, "often many times a second", 9.6, 650, fill=MUTED))
    desc = ("On the left an agent, containing sensors such as a camera, microphone "
            "or text input, a decision part using rules, search or a model, and "
            "actuators such as wheels, a speaker or text output. On the right its "
            "environment, for example a road and its traffic, a chess board, a "
            "conversation or a living room floor. An arrow labelled perceive runs "
            "from the environment to the agent's sensors, and an arrow labelled act "
            "runs from the actuators back to the environment, forming a loop.")
    return figure("ai-agent", 760, 340, "".join(body), "The agent loop", desc,
                  "Every AI system, from a thermostat to a chatbot, can be described "
                  "by this loop.")


# ================================== Level 2: training versus inference

@diagram("ai-train-infer")
def _train_infer():
    """Training adjusts the parameters; inference only uses them."""
    body = [text(380, 22, "Training sets the numbers. Inference uses them.", 12, 650,
                 fill=MUTED)]
    # training row
    body.append(text(30, 54, "TRAINING", 11.5, 800, anchor="start", fill=tv(ORANGE)))
    body.append(text(110, 54, "slow, costly, done once or now and then", 9.6, 600,
                     anchor="start", fill=MUTED))
    for k in range(3):
        body.append(cube(36 + k * 8, 82 - k * 6, 96, 58, 0, BLUE, op=0.55 + 0.2 * k))
    body.append(text(96, 106, "labelled", 10, 700, fill=WHITE))
    body.append(text(96, 121, "examples", 10, 700, fill=WHITE))
    body.append(arrow(148, 106, 236, 106, tv(BLUE), 2.2))
    # the model with dials
    body.append(tint(242, 66, 196, 84, VIOLET, op=0.14, r=12))
    body.append(text(340, 84, "model", 11, 800, fill=tv(VIOLET)))
    for k, v in enumerate([0.3, 0.7, 0.5, 0.85]):
        x = 262 + k * 44
        body.append(line(x, 98, x, 140, stroke=LINE, w=3))
        body.append(circle(x, 140 - v * 42, 6.5, fill=AMBER, stroke=FILL, w=1.5))
    body.append(text(340, 162, "parameters (weights) being adjusted", 9, 600, fill=MUTED))
    body.append(arrow(444, 106, 520, 106, tv(VIOLET), 2.2))
    body.append(tint(526, 82, 108, 48, PINK, "prediction", r=10, size=10.5, op=0.16))
    body.append(arrow(640, 106, 676, 106, tv(PINK), 2))
    body.append(solid(680, 86, 56, 40, RED, "error", r=10, size=10.5))
    body.append(path("M708 130 C 708 196, 360 200, 352 168", stroke=tv(RED), w=2,
                     dash="6 4"))
    body.append(arrow(356, 180, 350, 166, tv(RED), 2))
    body.append(text(560, 210, "compare with the label, nudge the parameters, repeat",
                     9.6, 650, fill=tv(RED)))
    # inference row
    body.append(line(30, 226, 730, 226, stroke=LINE, w=1, dash="3 5"))
    body.append(text(30, 250, "INFERENCE", 11.5, 800, anchor="start", fill=tv(GREEN)))
    body.append(text(118, 250, "fast, cheap, every time someone uses it", 9.6, 600,
                     anchor="start", fill=MUTED))
    body.append(tint(36, 268, 120, 46, BLUE, "new input", r=10, size=10.5, op=0.16))
    body.append(arrow(160, 291, 236, 291, tv(BLUE), 2.2))
    body.append(solid(242, 266, 196, 50, VIOLET, "trained model", "parameters fixed",
                      r=12, size=11, sub_size=8.8))
    body.append(arrow(444, 291, 520, 291, tv(VIOLET), 2.2))
    body.append(solid(526, 268, 160, 46, GREEN, "prediction", "e.g. 'spam, 97%'",
                      r=10, size=11, sub_size=8.8))
    desc = ("Two rows. Training: labelled examples go into a model whose parameters "
            "are shown as sliders being adjusted; the model makes a prediction, the "
            "prediction is compared with the label to give an error, and a dashed "
            "arrow takes the error back to nudge the parameters, repeatedly. "
            "Training is slow and costly and done once or now and then. Inference: "
            "a new input goes into the trained model, whose parameters are fixed, "
            "and a prediction such as spam, 97 percent, comes out. Inference is fast "
            "and cheap and happens every time someone uses the model.")
    return figure("ai-ti", 760, 336, "".join(body), "Training compared with inference",
                  desc, "A model is learned once, then used millions of times.")


# ===================================== Level 2: three kinds of learning

@diagram("ai-learning-types")
def _learning_types():
    """Supervised, unsupervised and reinforcement learning side by side."""
    body = [text(380, 22, "Three ways to learn", 12, 650, fill=MUTED)]
    W = 228
    heads = [(VIOLET, "Supervised", "examples with answers"),
             (TEAL, "Unsupervised", "find the structure yourself"),
             (ORANGE, "Reinforcement", "try things, collect rewards")]
    for k, (col, h, sub) in enumerate(heads):
        x = 22 + k * (W + 14)
        body.append(tint(x, 40, W, 262, col, op=0.08, r=14))
        body.append(solid(x + 14, 52, W - 28, 30, col, h, r=15, size=11.5))
        body.append(text(x + W / 2.0, 100, sub, 9.6, 650, fill=MUTED))
    # supervised: two labelled classes and a boundary
    x0 = 22
    A = [(40, 150), (62, 132), (78, 168), (52, 196), (96, 140), (88, 196), (70, 222)]
    B = [(150, 176), (176, 152), (190, 200), (164, 230), (204, 236), (140, 252), (196, 270)]
    body.append(line(x0 + 66, 284, x0 + 206, 118, stroke=tv(VIOLET), w=2, dash="6 4"))
    for px, py in A:
        body.append(circle(x0 + px, py, 7, fill=PINK, stroke=FILL, w=1.5))
    for px, py in B:
        body.append('<rect x="%d" y="%d" width="13" height="13" rx="2" fill="%s" '
                    'stroke="var(--dg-fill)" stroke-width="1.5"/>' % (x0 + px - 6, py - 6, BLUE))
    body.append(text(x0 + 52, 290, "cat", 9.6, 700, fill=tv(PINK)))
    body.append(text(x0 + 186, 290, "dog", 9.6, 700, fill=tv(BLUE)))
    # unsupervised: three clusters circled
    x1 = 22 + W + 14
    clusters = [((70, 160), CYAN), ((160, 160), AMBER), ((112, 240), LIME)]
    offs = [(-16, -10), (8, -16), (14, 6), (-6, 14), (-20, 8), (20, 18), (2, -2)]
    for (cx, cy), col in clusters:
        body.append('<ellipse cx="%d" cy="%d" rx="38" ry="32" fill="%s" fill-opacity="0.16" '
                    'stroke="%s" stroke-width="1.8" stroke-dasharray="5 4"/>'
                    % (x1 + cx, cy, col, col))
        for ox, oy in offs:
            body.append(circle(x1 + cx + ox, cy + oy, 5.5, fill=SLATE, stroke=FILL, w=1.2))
    body.append(text(x1 + W / 2.0, 290, "no labels: groups found", 9.6, 700, fill=MUTED))
    # reinforcement: a grid world
    x2 = 22 + 2 * (W + 14)
    gx, gy, c = x2 + 38, 122, 38
    walls = {(1, 1), (2, 3), (3, 1)}
    for i in range(4):
        for j in range(4):
            fill = SLATE if (i, j) in walls else FILL2
            op = "0.85" if (i, j) in walls else "1"
            body.append('<rect x="%d" y="%d" width="%d" height="%d" rx="4" fill="%s" '
                        'fill-opacity="%s" stroke="var(--dg-line)" stroke-width="1"/>'
                        % (gx + i * c, gy + j * c, c - 3, c - 3, fill, op))
    route = [(0, 3), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0), (3, 0)]
    pts = ["%d %d" % (gx + i * c + 18, gy + j * c + 18) for i, j in route]
    body.append(path("M" + " L".join(pts), stroke=tv(ORANGE), w=2.6, dash="5 3"))
    body.append(circle(gx + 18, gy + 3 * c + 18, 11, fill=VIOLET, stroke=FILL, w=2))
    body.append(text(gx + 18, gy + 3 * c + 22, "A", 10, 800, fill=WHITE))
    star = []
    for k in range(10):
        ang = -math.pi / 2 + k * math.pi / 5
        rad = 13 if k % 2 == 0 else 5.5
        star.append("%.1f,%.1f" % (gx + 3 * c + 18 + rad * math.cos(ang),
                                   gy + 18 + rad * math.sin(ang)))
    body.append('<polygon points="%s" fill="%s" stroke="#92400E" stroke-width="1"/>'
                % (" ".join(star), AMBER))
    body.append(text(gx + 4 * c - 3, gy - 7, "+1 reward", 9.6, 800, anchor="end",
                     fill=tv(ORANGE)))
    body.append(text(x2 + W / 2.0, 290, "agent A learns the route", 9.6, 700, fill=MUTED))
    desc = ("Three panels. Supervised learning, examples with answers: pink circles "
            "labelled cat and blue squares labelled dog, separated by a dashed "
            "boundary line the model learns. Unsupervised learning, find the "
            "structure yourself: grey points with no labels, which the algorithm "
            "groups into three circled clusters. Reinforcement learning, try things "
            "and collect rewards: a four by four grid with walls, where agent A "
            "learns a route to a star worth a reward of plus one.")
    return figure("ai-types", 760, 312, "".join(body),
                  "Supervised, unsupervised and reinforcement learning", desc,
                  "Answers, no answers, or only a score: the three kinds of "
                  "learning differ in what feedback they get.")


# ==================================== Level 2: self-supervised learning

@diagram("ai-self-supervised")
def _self_supervised():
    """Hide a word and predict it: the hidden word is a free label."""
    body = [text(380, 22, "The data labels itself: hide a word, then predict it", 12,
                 650, fill=MUTED)]
    words = ["The", "cat", "sat", "on", "the"]
    x = 30
    for wd in words:
        w = 22 + len(wd) * 8.5
        body.append(tint(x, 52, w, 32, BLUE, wd, r=8, size=11.5, op=0.14))
        x += w + 8
    body.append('<rect x="%d" y="52" width="58" height="32" rx="8" fill="none" '
                'stroke="%s" stroke-width="2" stroke-dasharray="5 3"/>' % (x, tv(PINK)))
    body.append(text(x + 29, 73, "?", 15, 800, fill=tv(PINK)))
    hid = x
    body.append(arrow(x + 64, 68, 394, 68, LINE, 2))
    body.append(solid(398, 46, 104, 44, VIOLET, "model", r=12, size=12))
    body.append(arrow(506, 68, 540, 68, LINE, 2))
    probs = [("mat", 0.46), ("floor", 0.21), ("sofa", 0.14), ("bed", 0.09), ("dog", 0.01)]
    for k, (wd, p) in enumerate(probs):
        y = 44 + k * 22
        body.append(text(590, y + 13, wd, 10.5, 700, anchor="end", fill=INK))
        body.append('<rect x="598" y="%d" width="%.1f" height="16" rx="4" fill="%s"/>'
                    % (y + 1, p * 250, plasma(0.25 + p * 1.4)))
        body.append(text(604 + p * 250, y + 13, "%d%%" % round(p * 100), 9.6, 650,
                         anchor="start", fill=MUTED))
    body.append(text(hid + 29, 104, "real word: mat", 9.6, 750, fill=tv(GREEN)))
    body.append(text(hid + 29, 118, "(the free label)", 9, 600, fill=MUTED))
    body.append(tint(30, 160, 700, 74, GREEN, op=0.08, r=12))
    body.append(text(48, 184, "Training signal", 11, 800, anchor="start", fill=tv(GREEN)))
    body.append(text(48, 204, "The model gave the real word 46%. Training nudges its "
                     "parameters so that next time the real word", 10, 500,
                     anchor="start", fill=INK))
    body.append(text(48, 220, "gets a little more. Repeat for every word in trillions "
                     "of words of text, and no person ever labels anything.", 10, 500,
                     anchor="start", fill=INK))
    desc = ("The words The cat sat on the are shown, followed by a hidden word marked "
            "with a question mark. They go into a model, which outputs probabilities "
            "for the hidden word: mat 46 percent, floor 21 percent, sofa 14 percent, "
            "bed 9 percent and dog 1 percent. The real word was mat, which is the free "
            "label. Training nudges the parameters so the real word gets a higher "
            "probability next time, repeated for every word in trillions of words of "
            "text, with no person labelling anything.")
    return figure("ai-ssl", 760, 250, "".join(body), "Self-supervised learning", desc,
                  "Next-word prediction: the training method behind GPT-style models.")


# ================================================ Level 3: a dataset table

@diagram("ai-dataset-table")
def _dataset_table():
    """A small table with an example row, a feature column and the label column."""
    body = [text(380, 22, "A dataset: rows are examples, columns are features, one "
                 "column is the label", 12, 650, fill=MUTED)]
    cols = ["floor area m²", "bedrooms", "garden", "km to station", "price £k"]
    rows = [(68, 2, 0, 1.2, 215), (112, 3, 1, 3.5, 340), (95, 3, 1, 0.8, 330),
            (150, 4, 1, 6.1, 425), (54, 1, 0, 0.4, 190)]
    X0, Y0, CW, RH = 120, 66, 104, 34
    for j, c in enumerate(cols):
        col = PINK if j == 4 else VIOLET
        body.append(solid(X0 + j * CW + 3, Y0, CW - 6, RH - 4, col, c, r=7, size=10.5))
    for i, r in enumerate(rows):
        y = Y0 + (i + 1) * RH
        for j, v in enumerate(r):
            fill = PINK if j == 4 else BLUE
            body.append('<rect x="%d" y="%d" width="%d" height="%d" rx="5" fill="%s" '
                        'fill-opacity="%s"/>' % (X0 + j * CW + 3, y, CW - 6, RH - 4, fill,
                                                 "0.16" if j == 4 else "0.08"))
            label = ("yes" if v else "no") if j == 2 else (("%g" % v) if j != 4 else "%d" % v)
            body.append(text(X0 + j * CW + CW / 2.0, y + 20, label, 11, 650, fill=INK))
        body.append(text(X0 - 14, y + 20, "house %d" % (i + 1), 10, 650, anchor="end",
                         fill=MUTED))
    # highlight one example (row 2) and one feature (column 1)
    ry = Y0 + 2 * RH - 3
    body.append('<rect x="%d" y="%d" width="%d" height="%d" rx="8" fill="none" '
                'stroke="%s" stroke-width="3"/>' % (X0 - 2, ry, 5 * CW + 4, RH + 2, AMBER))
    body.append('<rect x="%d" y="%d" width="%d" height="%d" rx="8" fill="none" '
                'stroke="%s" stroke-width="3" stroke-dasharray="7 4"/>'
                % (X0 + CW - 1, Y0 - 4, CW + 2, 6 * RH + 4, CYAN))
    by = Y0 + 6 * RH + 22
    body.append(solid(X0 + CW + 6, by, CW - 12, 26, TEAL, "a feature", r=13, size=10.5))
    body.append(path("M%d %d L%d %d" % (X0 + 1.5 * CW, by, X0 + 1.5 * CW, Y0 + 6 * RH + 2),
                     stroke=CYAN, w=2))
    body.append(solid(X0 + 4 * CW + 6, by, CW - 12, 26, PINK, "the label", r=13, size=10.5))
    body.append(text(X0 + 4 * CW + CW / 2.0, by + 42, "what we predict", 9.6, 650,
                     fill=MUTED))
    body.append(text(X0 + 1.5 * CW, by + 42, "one property, every house", 9.6, 650,
                     fill=MUTED))
    body.append(solid(X0 + 5 * CW + 14, ry + 4, 96, 26, ORANGE, "an example", r=13,
                      size=10.5))
    body.append(text(X0 + 5 * CW + 62, ry + 48, "one house", 9.6, 650, fill=MUTED))
    desc = ("A table of five houses. The columns are floor area in square metres, "
            "bedrooms, garden, kilometres to the station, and price in thousands of "
            "pounds. The first four column headers are violet: they are the features, "
            "the inputs. The price column is pink: it is the label, what we predict. "
            "One row, house 2 with 112 square metres, 3 bedrooms, a garden, 3.5 km to "
            "the station and a price of 340 thousand pounds, is outlined as an "
            "example. The bedrooms column is outlined as a feature: one property of "
            "every house.")
    return figure("ai-dstab", 760, 330, "".join(body), "A dataset of houses", desc,
                  "The model's job: learn to predict the pink column from the violet "
                  "ones.")


# ============================================ Level 3: image as a tensor

_ART = ["SSSSYY", "SSSSYY", "SSSSSS", "SRSSSS", "GgGGGG", "GGGGGG"]
_RGB = {"S": (120, 190, 240), "Y": (250, 204, 21), "R": (225, 29, 72),
        "G": (34, 160, 60), "g": (20, 110, 40)}


@diagram("ai-image-tensor")
def _image_tensor():
    """A pixel picture split into its red, green and blue channel grids."""
    body = [text(380, 22, "A colour image is three grids of numbers stacked into a "
                 "block", 12, 650, fill=MUTED)]
    C = 26
    # the picture as we see it
    px, py = 34, 92
    for i, row in enumerate(_ART):
        for j, k in enumerate(row):
            body.append('<rect x="%d" y="%d" width="%d" height="%d" fill="rgb(%d,%d,%d)"/>'
                        % ((px + j * C, py + i * C, C, C) + _RGB[k]))
    body.append('<rect x="%d" y="%d" width="%d" height="%d" fill="none" stroke="%s" '
                'stroke-width="1.5"/>' % (px, py, 6 * C, 6 * C, LINE))
    body.append(text(px + 3 * C, py - 14, "what you see", 10.5, 750, fill=INK))
    body.append(text(px + 3 * C, py + 6 * C + 22, "6 × 6 pixels", 10, 600, fill=MUTED))
    body.append(arrow(214, 170, 284, 170, LINE, 2.4))
    body.append(text(249, 160, "split", 9.6, 700, fill=MUTED))
    # three channel planes, back to front: blue, green, red
    planes = [(2, "blue", lambda v: "rgb(0,0,%d)" % v, BLUE),
              (1, "green", lambda v: "rgb(0,%d,0)" % v, GREEN),
              (0, "red", lambda v: "rgb(%d,0,0)" % v, RED)]
    channel = {"red": 0, "green": 1, "blue": 2}
    X, Y, DX, DY = 316, 96, 46, -30
    for k, name, fill_fn, col in planes:
        ox, oy = X + k * DX, Y + k * DY + 2 * 30
        for i, row in enumerate(_ART):
            for j, key in enumerate(row):
                v = _RGB[key][channel[name]]
                body.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s" '
                            'stroke="#FFFFFF" stroke-opacity="0.35" stroke-width="0.8"/>'
                            % (ox + j * C, oy + i * C, C, C, fill_fn(v)))
                if k == 0:
                    body.append(text(ox + j * C + C / 2.0, oy + i * C + C / 2.0 + 3.4,
                                     str(v), 8.4, 650,
                                     fill=WHITE if v < 150 else DARK))
        body.append('<rect x="%d" y="%d" width="%d" height="%d" fill="none" stroke="%s" '
                    'stroke-width="2"/>' % (ox, oy, 6 * C, 6 * C, tv(col)))
        body.append(text(ox + 6 * C + 6, oy + 6 * C - 6, name, 10.5, 800, anchor="start",
                         fill=tv(col)))
    # dimension labels
    fx, fy = X, Y + 60
    body.append(text(fx + 3 * C, fy + 6 * C + 22, "width 6", 10, 700, fill=INK))
    body.append(text(fx - 10, fy + 3 * C, "height 6", 10, 700, anchor="end", fill=INK))
    body.append(line(fx, fy - 4, fx + 2 * DX - 2, fy + 2 * DY - 2, stroke=LINE, w=1.4,
                     dash="4 3"))
    body.append(text(fx + DX - 8, fy + DY - 10, "3 channels", 10, 700, anchor="end",
                     fill=INK))
    body.append(tint(560, 268, 176, 52, VIOLET, "shape (6, 6, 3)", "6 × 6 × 3 = 108 numbers",
                     r=12, size=12, sub_size=9.6, op=0.14))
    desc = ("On the left, a tiny picture of 6 by 6 pixels: blue sky, a yellow sun in "
            "the top right, a red flower and green grass along the bottom. An arrow "
            "labelled split leads to three stacked grids, the red, green and blue "
            "channels, each 6 by 6, drawn one behind the other. The front red grid "
            "shows its numbers: sky pixels are 120, the sun 250, the flower 225 and "
            "the grass 34 or 20. Together the block has shape 6 by 6 by 3, which is "
            "108 numbers.")
    return figure("ai-imgt", 760, 340, "".join(body),
                  "An image as red, green and blue channels", desc,
                  "Every pixel is three numbers from 0 to 255. Each channel is a "
                  "greyscale image of how much of that colour is present.")


# ========================================= Level 3: scalar to tensor

def _block(x, y, cols, rows, layers, s, colour, values=None):
    """A block of unit cubes, painted back to front, bottom to top, left to right."""
    out = []
    dx, dy = s * 0.7 * 0.62, -s * 0.45 * 0.62
    for k in reversed(range(layers)):
        for r in reversed(range(rows)):
            for c in range(cols):
                cx, cy = x + c * s + k * dx, y + r * s + k * dy
                lab = None
                if values is not None and k == 0:
                    lab = str(values[r][c])
                out.append(cube(cx, cy, s, s, s * 0.62, colour, lab, size=10))
    return "".join(out)


@diagram("ai-tensor-ranks")
def _tensor_ranks():
    """Scalar, vector, matrix and 3D tensor drawn as blocks of cubes."""
    body = [text(380, 22, "Scalar, vector, matrix, tensor: the same idea with more "
                 "dimensions", 12, 650, fill=MUTED)]
    S = 26
    items = [
        (46, 150, 1, 1, 1, AMBER, [[7]], "scalar", "shape ()", "one number"),
        (150, 150, 4, 1, 1, PINK, [[3, 1, 4, 1]], "vector", "shape (4,)", "a list"),
        (318, 98, 4, 3, 1, VIOLET, [[2, 7, 1, 8], [2, 8, 1, 8], [4, 5, 9, 0]],
         "matrix", "shape (3, 4)", "a table"),
        (520, 98, 4, 3, 3, BLUE, [[1, 6, 1, 8], [0, 3, 3, 9], [8, 8, 7, 4]],
         "tensor", "shape (3, 3, 4)", "a block, such as an image"),
    ]
    for x, y, c, r, l, col, vals, name, shape, sub in items:
        body.append(_block(x, y, c, r, l, S, col, vals))
        cx = x + c * S / 2.0 + (l - 1) * S * 0.22
        body.append(text(cx, 214, name, 13, 800, fill=tv(col) if col != AMBER else INK))
        body.append(text(cx, 232, shape, 10.5, 650, fill=INK, mono=True))
        body.append(text(cx, 248, sub, 9.6, 600, fill=MUTED))
    for x in (112, 278, 478):
        body.append(arrow(x, 162, x + 26, 162, LINE, 1.8))
    body.append(text(380, 284, "Rank = number of dimensions: 0, 1, 2 and 3. A batch of "
                     "colour images is rank 4.", 10, 600, fill=MUTED))
    desc = ("Four drawings made of cubes, each holding a number. A scalar is a single "
            "cube holding 7, shape empty brackets, one number. A vector is a row of 4 "
            "cubes, 3 1 4 1, shape (4,), a list. A matrix is a 3 by 4 grid of cubes, "
            "shape (3, 4), a table. A tensor is a solid block 3 cubes deep, 3 high and "
            "4 wide, shape (3, 3, 4), a block such as an image. Rank is the number of "
            "dimensions: 0, 1, 2 and 3, and a batch of colour images is rank 4.")
    return figure("ai-ranks", 760, 300, "".join(body), "Scalars, vectors, matrices and tensors",
                  desc, "AI libraries call all of these tensors and keep track of each "
                  "one's shape.")


# ============================================= Level 3: feature scaling

@diagram("ai-feature-scaling")
def _feature_scaling():
    """Before scaling, one feature swamps distance; after, both count."""
    body = [text(380, 22, "Before scaling, bedrooms hardly count. After scaling, they "
                 "do.", 12, 650, fill=MUTED)]
    pts = [("A", 100, 2), ("B", 102, 5), ("C", 130, 2), ("", 70, 1), ("", 160, 4),
           ("", 220, 5), ("", 260, 6), ("", 85, 3), ("", 190, 3)]
    # left: true scale, 1 bedroom drawn the same length as 1 square metre
    L0, LW, LY = 40, 320, 190
    body.append(tint(24, 46, 352, 254, SLATE, op=0.06, r=12))
    body.append(text(200, 68, "Raw values, drawn to the same scale", 11, 750, fill=INK))
    k = LW / 250.0
    body.append(line(L0, LY, L0 + LW, LY, stroke=LINE, w=1.4))
    for v in (50, 100, 150, 200, 250, 300):
        x = L0 + (v - 50) * k
        body.append(line(x, LY, x, LY + 5, stroke=LINE, w=1))
        body.append(text(x, LY + 18, str(v), 9, 600, fill=MUTED))
    body.append(text(L0 + LW / 2.0, LY + 34, "floor area (m²): range 250", 9.6, 650,
                     fill=MUTED))
    for name, a, b in pts:
        x, y = L0 + (a - 50) * k, LY - 8 - (b - 1) * k
        colr = {"A": VIOLET, "B": PINK, "C": TEAL}.get(name, SLATE)
        body.append(circle(x, y, 5 if name else 3.5, fill=colr, stroke=FILL, w=1.2))
        if name:
            body.append(text(x + (-9 if name == "A" else 9), y - 8, name, 10, 800,
                             fill=tv(colr)))
    body.append(path("M%d %d l0 -6 m0 6 l0 0" % (L0 + LW + 4, LY - 8), stroke=LINE, w=1))
    body.append(text(200, 112, "bedrooms (range 5) is squashed", 10, 650, fill=tv(PINK)))
    body.append(text(200, 128, "into a strip 6 pixels tall", 10, 650, fill=tv(PINK)))
    body.append(text(200, 262, "nearest to A: B (3.6 away), though B has", 9.6, 650,
                     fill=INK))
    body.append(text(200, 277, "3 more bedrooms; C is 30 away", 9.6, 650, fill=INK))
    # right: both features scaled to 0..1
    R0, RY, RS = 446, 270, 200
    body.append(tint(410, 46, 330, 254, GREEN, op=0.06, r=12))
    body.append(text(575, 68, "Both scaled to 0 to 1", 11, 750, fill=INK))
    body.append(line(R0, RY, R0 + RS, RY, stroke=LINE, w=1.4))
    body.append(line(R0, RY, R0, RY - RS + 20, stroke=LINE, w=1.4))
    body.append(text(R0 + RS / 2.0, RY + 16, "floor area, scaled", 9, 600, fill=MUTED))
    body.append('<text x="%d" y="%d" text-anchor="middle" font-size="9" font-weight="600" '
                'fill="%s" transform="rotate(-90 %d %d)">bedrooms, scaled</text>'
                % (R0 - 10, RY - 90, MUTED, R0 - 10, RY - 90))
    sc = [(name, R0 + (a - 50) / 250.0 * RS, RY - (b - 1) / 5.0 * (RS - 20))
          for name, a, b in pts]
    where = {name: (x, y) for name, x, y in sc if name}
    ax, ay = where["A"]
    for nm, colr in (("B", PINK), ("C", TEAL)):
        bx, by = where[nm]
        body.append(line(ax, ay, bx, by, stroke=tv(colr), w=1.8, dash="4 3"))
    for name, x, y in sc:
        colr = {"A": VIOLET, "B": PINK, "C": TEAL}.get(name, SLATE)
        body.append(circle(x, y, 6 if name else 4, fill=colr, stroke=FILL, w=1.4))
        if name:
            right = name == "C"
            body.append(text(x + (10 if right else -10), y + 4, name, 10, 800,
                             anchor="start" if right else "end", fill=tv(colr)))
    body.append(text(706, 172, "A to B: 0.60", 9.6, 700, anchor="end", fill=tv(PINK)))
    body.append(text(706, 188, "A to C: 0.12", 9.6, 700, anchor="end", fill=tv(TEAL)))
    body.append(text(706, 204, "now C is nearest", 9.6, 700, anchor="end", fill=INK))
    desc = ("Two scatter plots of nine houses by floor area and bedrooms. On the left "
            "the raw values are drawn to the same scale, so the floor area axis runs "
            "across 250 units while the 5 unit range of bedrooms is squashed into a "
            "strip 6 pixels tall. House B, with 3 more bedrooms than house A, looks "
            "nearest to A at a distance of 3.6, while house C is 30 away. On the right "
            "both features are scaled to 0 to 1 and the points spread out. Dashed lines "
            "show A to B is now 0.60 and A to C is 0.12, so C is nearest.")
    return figure("ai-scale", 760, 320, "".join(body), "Why features are scaled", desc,
                  "Any method that measures distance needs its features on comparable "
                  "scales.")


# =============================================== Level 3: the data split

def _padlock(x, y, colour):
    return ('<path d="M%.1f %.1f v-6 a7 7 0 0 1 14 0 v6" fill="none" stroke="%s" '
            'stroke-width="2.4"/><rect x="%.1f" y="%.1f" width="20" height="15" rx="3" '
            'fill="%s"/>' % (x + 3, y, colour, x, y, colour))


@diagram("ai-data-split")
def _data_split():
    """Shuffle, then split into training, validation and test sets."""
    body = [text(380, 22, "Shuffle once, then split before any training happens", 12,
                 650, fill=MUTED)]
    order = [3, 17, 8, 12, 1, 19, 5, 14, 0, 10, 7, 16, 2, 18, 11, 6, 13, 4, 9, 15]
    for i, v in enumerate(order):
        x = 40 + i * 34
        colr = plasma(0.1 + 0.8 * v / 19.0)
        body.append('<rect x="%d" y="44" width="28" height="28" rx="5" fill="%s"/>' % (x, colr))
    body.append(text(380, 92, "every example, in a random order", 9.6, 650, fill=MUTED))
    segs = [(0, 14, BLUE, "TRAINING  70%"), (14, 17, ORANGE, "VALIDATION  15%"),
            (17, 20, PINK, "TEST  15%")]
    for a, b, colr, lab in segs:
        x0, x1 = 40 + a * 34, 40 + b * 34 - 6
        body.append(path("M%d 104 L%d 104" % (x0, x1), stroke=tv(colr), w=3))
        if b - a > 3:
            body.append(solid(x0, 114, x1 - x0, 40, colr, lab, r=10, size=11.5))
        else:
            name, share = lab.split("  ")
            body.append(solid(x0, 114, x1 - x0, 40, colr, name, share, r=10, size=10,
                              sub_size=9.6))
    uses = [(40, 470, BLUE, "Learn the parameters", "the model sees these thousands of times",
             "like practice questions"),
            (516, 98, ORANGE, "Tune and choose", "settings, model, when to stop",
             "like mock exams"),
            (618, 98, PINK, "Final score, once", "never used to make choices",
             "like the real exam")]
    for x, w, colr, h, l1, l2 in uses:
        body.append(tint(x, 176, w if w > 100 else w + 2, 96, colr, op=0.1, r=10))
        cx = x + (w if w > 100 else w + 2) / 2.0
        body.append(text(cx, 200, h, 10.5 if w > 100 else 9.6, 800, fill=tv(colr)))
        if w > 100:
            body.append(text(cx, 222, l1, 9.6, 600, fill=INK))
            body.append(text(cx, 240, l2, 9.6, 600, fill=MUTED))
        else:
            for k, wd in enumerate(_wrap(l1, 16)):
                body.append(text(cx, 218 + k * 13, wd, 8.8, 600, fill=INK))
            body.append(text(cx, 262, l2, 8.6, 600, fill=MUTED))
    body.append(_padlock(716, 128, tv(PINK)))
    desc = ("A row of twenty coloured squares, every example in a random order, is "
            "split into three parts: training, the first 70 percent; validation, the "
            "next 15 percent; and test, the last 15 percent, marked with a padlock. "
            "Training data is used to learn the parameters, seen thousands of times, "
            "like practice questions. Validation data is used to tune and choose "
            "settings, the model and when to stop, like mock exams. Test data gives "
            "the final score, once, and is never used to make choices, like the real "
            "exam.")
    return figure("ai-split", 760, 290, "".join(body),
                  "Training, validation and test sets", desc,
                  "The test set is locked away until the very end.")


def _wrap(s, n):
    """Split a short string into lines of at most n characters."""
    out, cur = [], ""
    for w in s.split():
        if cur and len(cur) + 1 + len(w) > n:
            out.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    if cur:
        out.append(cur)
    return out


# =============================================== Level 3: the accuracy trap

@diagram("ai-imbalance")
def _imbalance():
    """100 payments, one fraud: a model that never says fraud scores 99%."""
    body = [text(380, 22, "100 payments, 1 fraud. The lazy model: always say “OK”.",
                 12, 650, fill=MUTED)]
    X0, Y0, C = 40, 46, 25
    for i in range(10):
        for j in range(10):
            fraud = (i, j) == (6, 7)
            colr = ROSE if fraud else TEAL
            body.append('<rect x="%d" y="%d" width="%d" height="%d" rx="4" fill="%s" '
                        'fill-opacity="%s"/>' % (X0 + j * C, Y0 + i * C, C - 4, C - 4, colr,
                                                 "1" if fraud else "0.72"))
    fx, fy = X0 + 7 * C, Y0 + 6 * C
    body.append('<rect x="%d" y="%d" width="%d" height="%d" rx="6" fill="none" '
                'stroke="%s" stroke-width="3"/>' % (fx - 5, fy - 5, C + 6, C + 6, ROSE))
    body.append(text(X0 + 5 * C - 2, Y0 + 10 * C + 18, "99 genuine, 1 fraud", 10, 650,
                     fill=MUTED))
    body.append(path("M%d %d C 330 210, 360 214, 392 214" % (fx + C + 2, fy + 10),
                     stroke=ROSE, w=1.8, dash="4 3"))
    body.append(text(396, 218, "missed", 10, 800, anchor="start", fill=tv(RED)))
    cards = [(GREEN, "99%", "accuracy", "right about 99 of 100"),
             (RED, "0%", "of fraud caught", "recall: misses every one"),
             (VIOLET, "?", "what to measure", "precision and recall")]
    for k, (colr, big, lab, sub) in enumerate(cards):
        x = 470 + (k % 2) * 136
        y = 54 + (k // 2) * 126
        if k == 2:
            x = 470
            body.append(tint(x, y, 266, 96, colr, op=0.1, r=12))
            body.append(text(x + 133, y + 36, "Measure the rare class directly:", 10.5,
                             750, fill=INK))
            body.append(text(x + 133, y + 58, "recall: how much fraud is caught", 10, 600,
                             fill=MUTED))
            body.append(text(x + 133, y + 76, "precision: how many alerts are real", 10,
                             600, fill=MUTED))
            continue
        body.append(tint(x, y, 128, 110, colr, op=0.12, r=12))
        body.append(text(x + 64, y + 50, big, 30, 850, fill=tv(colr)))
        body.append(text(x + 64, y + 74, lab, 10.5, 750, fill=INK))
        body.append(text(x + 64, y + 92, sub, 8.8, 600, fill=MUTED))
    desc = ("A grid of 100 squares, 99 teal for genuine payments and 1 pink for fraud, "
            "which is circled and marked missed. A lazy model that always says OK is "
            "right about 99 of the 100, so its accuracy is 99 percent, but it catches "
            "0 percent of the fraud: its recall is zero. The lesson: measure the rare "
            "class directly with recall, how much fraud is caught, and precision, how "
            "many alerts are real.")
    return figure("ai-imb", 760, 330, "".join(body), "The accuracy trap", desc,
                  "On imbalanced data, accuracy mostly measures the imbalance.")


# ============================================== Level 3: where bias enters

@diagram("ai-bias-pipeline")
def _bias_pipeline():
    """The stages from the world to a decision, and the bias each can add."""
    body = [text(380, 22, "Bias can enter at every stage, and decisions feed back into "
                 "the world", 12, 650, fill=MUTED)]
    stages = [("The world", "who is affected", GREEN, "historical bias",
               "past unfairness, faithfully recorded"),
              ("Collection", "what gets recorded", BLUE, "sampling bias",
               "some people missing or rare"),
              ("Labelling", "what counts as right", VIOLET, "labelling bias",
               "labellers' assumptions"),
              ("Features", "what is measured", INDIGO, "measurement bias",
               "a poor stand-in, e.g. spend for need"),
              ("Training", "what is optimised", PINK, "evaluation bias",
               "one average hides groups"),
              ("Decisions", "what happens next", ORANGE, "feedback loops",
               "decisions shape new data")]
    W, G = 112, 14
    for k, (h, sub, colr, bias, why) in enumerate(stages):
        x = 18 + k * (W + G)
        body.append(solid(x, 60, W, 56, colr, h, sub, r=12, size=11.5, sub_size=8.6))
        if k < len(stages) - 1:
            body.append(arrow(x + W + 1, 88, x + W + G - 1, 88, LINE, 1.8))
        # warning triangle and the bias that can enter here
        tx, ty = x + W / 2.0, 140
        body.append('<polygon points="%.1f,%.1f %.1f,%.1f %.1f,%.1f" fill="%s"/>'
                    % (tx, ty, tx - 11, ty + 19, tx + 11, ty + 19, AMBER))
        body.append(text(tx, ty + 16, "!", 12, 900, fill=DARK))
        body.append(tint(x, 168, W, 66, colr, op=0.1, r=10))
        body.append(text(tx, 188, bias, 9.6, 800, fill=tv(colr)))
        for i, wd in enumerate(_wrap(why, 19)):
            body.append(text(tx, 204 + i * 12, wd, 8.4, 600, fill=MUTED))
    # feedback arrow from decisions back to the world
    body.append(path("M%d 248 C %d 280, 74 280, 74 248" % (18 + 5 * (W + G) + W / 2, 18 + 5 * (W + G) + W / 2),
                     stroke=tv(ORANGE), w=2.2, dash="7 4"))
    body.append(arrow(74, 256, 74, 240, tv(ORANGE), 2.2))
    body.append(text(380, 294, "the system's decisions change what happens, which "
                     "becomes tomorrow's data", 9.6, 700, fill=tv(ORANGE)))
    desc = ("Six stages in a row, joined by arrows: the world, who is affected; "
            "collection, what gets recorded; labelling, what counts as right; "
            "features, what is measured; training, what is optimised; and decisions, "
            "what happens next. Under each a warning sign names the bias that can "
            "enter there: historical bias, past unfairness faithfully recorded; "
            "sampling bias, some people missing or rare; labelling bias, labellers' "
            "assumptions; measurement bias, a poor stand-in such as spending for need; "
            "evaluation bias, one average hiding groups; and feedback loops, decisions "
            "shaping new data. A dashed arrow runs from decisions back to the world, "
            "because the system's decisions change what happens, which becomes "
            "tomorrow's data.")
    return figure("ai-biasp", 760, 306, "".join(body), "Where bias enters an AI system",
                  desc, "Fixing bias means checking every stage, not only the model.")
