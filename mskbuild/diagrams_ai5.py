"""AI course diagrams, Level 10: attention and transformers.

The worked attention example, the masks, the positional encodings and the
parameter counts are computed here. Where a figure shows the pattern a trained
head learns, the scores are set by hand to show that pattern, and the figure's
description says so.
"""
import math
import random

from .diagrams import diagram
from .svg import figure, figure_steps, step, text, line, path, circle, esc
from .diagrams_ai_kit import (INK, MUTED, FILL, FILL2, LINE, VIOLET, PINK, BLUE,
                              TEAL, GREEN, ORANGE, RED, INDIGO, AMBER, LIME,
                              CYAN, ROSE, SKY, PURPLE, SLATE, WHITE, DARK, tv,
                              solid, tint, grad, plasma, diverging, ink_on,
                              arrow, cube)
from .diagrams_ai2 import Plot, _halo


def _softmax(xs):
    m = max(xs)
    e = [math.exp(x - m) if x != float("-inf") else 0.0 for x in xs]
    s = sum(e)
    return [v / s for v in e]


def _wsub(x, y, base, sub, size=12, weight=750, fill=INK, anchor="middle"):
    """Text with a subscript, such as W with Q below it."""
    return ('<text x="%s" y="%s" text-anchor="%s" font-size="%s" font-weight="%s" '
            'fill="%s">%s<tspan dy="%.1f" font-size="%.1f">%s</tspan></text>'
            % (x, y, anchor, size, weight, fill, esc(base), size * 0.3, size * 0.72, esc(sub)))


def _rot(x, y, s, size=10, weight=650, fill=INK, angle=-45):
    """Text rotated about its start, for column labels."""
    return ('<text x="%.1f" y="%.1f" text-anchor="start" font-size="%s" font-weight="%s" '
            'fill="%s" transform="rotate(%s %.1f %.1f)">%s</text>'
            % (x, y, size, weight, fill, angle, x, y, esc(s)))


def _chips(words, cy, size=11.5, gap=8, width=760, char=6.6):
    """Lay out word chips centred on a row; returns [(word, x, w)]."""
    ws = [14 + char * len(w) for w in words]
    total = sum(ws) + gap * (len(words) - 1)
    x = (width - total) / 2.0
    out = []
    for w, cw in zip(words, ws):
        out.append((w, x, cw))
        x += cw + gap
    return out


def _mix(a, b, t):
    ca = [int(a[i:i + 2], 16) for i in (1, 3, 5)]
    cb = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02X%02X%02X" % tuple(int(round(x + (y - x) * t)) for x, y in zip(ca, cb))


# ===================================================== attention lines

_SENT = ["The", "animal", "didn't", "cross", "the", "street", "because", "it", "was", "too"]
_TIRED = [0.02, 0.46, 0.03, 0.04, 0.02, 0.12, 0.05, 0.08, 0.04, 0.04, 0.10]
_WIDE = [0.02, 0.10, 0.03, 0.06, 0.04, 0.48, 0.05, 0.07, 0.04, 0.03, 0.08]


@diagram("ai-attention-lines")
def _attention_lines():
    """The same word attends to different words in different contexts."""
    body = [text(380, 22, "Attention: “it” looks at every word and weighs each one", 12, 650,
                 fill=MUTED)]
    rows = [(_SENT + ["tired"], _TIRED, PINK, 170, "animal"),
            (_SENT + ["wide"], _WIDE, BLUE, 356, "street")]
    for words, wts, col, cy, target in rows:
        chips = _chips(words, cy)
        it = [c for c in chips if c[0] == "it"][0]
        itx = it[1] + it[2] / 2.0
        top = cy - 12
        wmax = max(wts)
        order = sorted(range(len(words)), key=lambda k: wts[k])
        for k in order:
            w, x, cw = chips[k]
            tx = x + cw / 2.0
            if w == "it":
                continue
            h = 16 + 0.26 * abs(tx - itx)
            body.append('<path d="M%.1f %.1f C %.1f %.1f, %.1f %.1f, %.1f %.1f" fill="none" '
                        'stroke="%s" stroke-width="%.1f" stroke-opacity="%.2f" '
                        'stroke-linecap="round"/>'
                        % (itx, top, itx, top - h, tx, top - h, tx, top, tv(col),
                           1.2 + 11 * wts[k], 0.3 + 0.7 * wts[k] / wmax))
            if wts[k] >= 0.1:
                body.append(_halo((itx + tx) / 2.0, top - 0.75 * h - 6, "%.2f" % wts[k], 10.5, 800))
        for k, (w, x, cw) in enumerate(chips):
            if w == "it":
                body.append(solid(x, cy - 12, cw, 24, col, w, r=7, size=11.5))
            elif w == target or w in ("tired", "wide"):
                body.append(tint(x, cy - 12, cw, 24, col, w, r=7, size=11.5, op=0.2))
            else:
                body.append(tint(x, cy - 12, cw, 24, SLATE, w, r=7, size=11.5, op=0.08))
    body.append(text(380, 206, "“tired” fits an animal, so “it” attends most to “animal” (0.46)",
                     10.5, 750, fill=tv(PINK)))
    body.append(text(380, 392, "“wide” fits a street, so “it” attends most to “street” (0.48)",
                     10.5, 750, fill=tv(BLUE)))
    desc = ("Two copies of the sentence: The animal didn't cross the street because it was too "
            "tired, and the same sentence ending too wide. From the word it, curved lines run to "
            "every other word, thicker for higher attention weights. In the first sentence the "
            "thickest line goes to animal, weight 0.46, then street 0.12 and tired 0.10. In the "
            "second the thickest goes to street, weight 0.48, then animal 0.10. The weights are "
            "illustrative values for one attention head, and in each sentence they add up to 1.")
    return figure("ai-attl", 760, 404, "".join(body), "Attention depends on context", desc,
                  "Illustrative weights for one head: one changed word moves the attention.")


# ===================================================== queries, keys, values

_X = [0.8, -0.3, 0.5, 0.1, -0.6, 0.9]


def _proj_matrix(seed):
    rnd = random.Random(seed)
    return [[rnd.uniform(-0.9, 0.9) for _ in range(4)] for _ in _X]


@diagram("ai-qkv")
def _qkv():
    """One embedding, three learned matrices, three new vectors."""
    body = [text(380, 22, "Every token makes a query, a key and a value from its embedding",
                 12, 650, fill=MUTED)]
    body.append(text(57, 50, "x", 13, 800, fill=INK))
    for i, v in enumerate(_X):
        col = diverging(max(-1, min(1, v)))
        y = 60 + i * 30
        body.append('<rect x="40" y="%d" width="34" height="26" rx="4" fill="%s"/>' % (y, col))
        body.append(text(57, y + 17, ("%.1f" % v).replace("-", "−"), 10, 700, fill=ink_on(col)))
    body.append(text(57, 258, "embedding", 9.6, 750, fill=INK))
    body.append(text(57, 272, "of “it”", 9.6, 650, fill=MUTED))
    rows = [("Q", VIOLET, "q", "query: what “it” is looking for", 1),
            ("K", BLUE, "k", "key: what “it” offers to others", 2),
            ("V", TEAL, "v", "value: what “it” will pass on", 3)]
    for r, (sub, col, name, note, seed) in enumerate(rows):
        cy = 86 + r * 72
        W = _proj_matrix(seed)
        vec = [sum(_X[i] * W[i][j] for i in range(6)) for j in range(4)]
        body.append(arrow(78, 150, 146, cy, LINE, 1.6))
        body.append(cube(150, cy - 22, 96, 44, 16, col))
        body.append(_wsub(198, cy + 5, "× W", sub, 13, 800, fill=WHITE))
        body.append(arrow(262, cy, 296, cy, tv(col), 2))
        for j, v in enumerate(vec):
            c = diverging(max(-1, min(1, v / 1.2)))
            x = 302 + j * 44
            body.append('<rect x="%d" y="%d" width="40" height="30" rx="5" fill="%s"/>'
                        % (x, cy - 15, c))
            body.append(text(x + 20, cy + 4.5, ("%.2f" % v).replace("-", "−"), 10, 700,
                             fill=ink_on(c)))
        body.append(text(490, cy + 5, name, 15, 800, fill=tv(col)))
        body.append(text(508, cy + 4, note, 10.5, 700, fill=INK, anchor="start"))
    body.append(text(380, 292, "The same three matrices are used for every token; training tunes "
                     "their numbers.", 10, 650, fill=MUTED))
    desc = ("An embedding vector x for the word it, six numbers, has arrows to three 3D blocks: "
            "multiply by W Q in violet, by W K in blue and by W V in teal. Each block produces a "
            "new vector of four numbers: q, the query, what it is looking for; k, the key, what "
            "it offers to other tokens; and v, the value, what it will pass on. The same three "
            "matrices are used for every token.")
    return figure("ai-qkv", 760, 304, "".join(body), "Queries, keys and values", desc,
                  "Three learned matrices turn one embedding into three vectors with three jobs.")


# ===================================================== the four steps

_STEP_WORDS = ["animal", "cross", "street", "it"]
_STEP_KEYS = [[2, 1], [0, 1], [1, -1], [1, 1]]
_STEP_VALS = [[4, 0], [2, 2], [0, 4], [1, 1]]
_STEP_Q = [2, 1]


def _value_colour(v):
    """Values as colour: the first number pink, the second blue, size as strength."""
    a, b = v
    if a + b == 0:
        return FILL2
    hue = _mix(PINK, BLUE, b / float(a + b))
    return _mix("#FFFFFF", hue, min(1.0, 0.35 + (a + b) / 5.0))


@diagram("ai-attention-steps")
def _attention_steps():
    """Score, scale, softmax, blend for the query of "it"."""
    dots = [sum(q * k for q, k in zip(_STEP_Q, key)) for key in _STEP_KEYS]
    scaled = [d / math.sqrt(2) for d in dots]
    wts = _softmax(scaled)
    out = [sum(w * v[i] for w, v in zip(wts, _STEP_VALS)) for i in range(2)]
    ys = [128, 176, 224, 272]
    cols = {"tok": 78, "key": 172, "dot": 256, "scl": 336, "bar": 400, "val": 640}
    base = [text(380, 22, "Scaled dot-product attention for the token “it”", 12, 650, fill=MUTED)]
    base.append(solid(28, 38, 214, 30, PINK, "query of “it”:  q = [2, 1]", r=8, size=11.5))
    for name, x, lab in [("tok", cols["tok"], "token"), ("key", cols["key"], "key"),
                         ("dot", cols["dot"], "q · k"), ("scl", cols["scl"], "÷ √2"),
                         ("bar", cols["bar"] + 90, "softmax weight"), ("val", cols["val"] + 20, "value")]:
        base.append(text(x, 98, lab, 10.5, 800, fill=MUTED))
    base.append(line(28, 106, 732, 106, stroke=LINE, w=1))
    for k, w in enumerate(_STEP_WORDS):
        y = ys[k]
        base.append(tint(cols["tok"] - 42, y - 14, 84, 28, BLUE, w, r=7, size=11, op=0.12))
        base.append(text(cols["key"], y + 4, ("[%d, %d]" % tuple(_STEP_KEYS[k])).replace("-", "−"),
                         11.5, 700, fill=INK, mono=True))

    def col_dot():
        s = []
        for k in range(4):
            s.append(text(cols["dot"], ys[k] + 5, "%d" % dots[k], 14, 800,
                          fill=tv(VIOLET) if k == 0 else INK))
        return "".join(s)

    def col_scl():
        return "".join(text(cols["scl"], ys[k] + 5, "%.2f" % scaled[k], 13, 750,
                            fill=tv(VIOLET) if k == 0 else INK) for k in range(4))

    def col_bar():
        s = []
        for k in range(4):
            wpx = 150 * wts[k]
            s.append('<rect x="%d" y="%d" width="150" height="20" rx="4" fill="%s"/>'
                     % (cols["bar"], ys[k] - 10, FILL2))
            s.append('<rect x="%d" y="%d" width="%.1f" height="20" rx="4" fill="%s"/>'
                     % (cols["bar"], ys[k] - 10, max(3, wpx), AMBER))
            s.append(text(cols["bar"] + 158, ys[k] + 5, "%.3f" % wts[k], 11.5, 800, fill=INK,
                          anchor="start"))
        return "".join(s)

    def col_val():
        s = []
        for k in range(4):
            c = _value_colour(_STEP_VALS[k])
            s.append('<rect x="%d" y="%d" width="26" height="26" rx="6" fill="%s" stroke="%s"/>'
                     % (cols["val"] - 18, ys[k] - 13, c, LINE))
            s.append(text(cols["val"] + 14, ys[k] + 4, "[%d, %d]" % tuple(_STEP_VALS[k]), 11, 700,
                          fill=INK, anchor="start", mono=True))
        oc = _value_colour(out)
        s.append('<rect x="28" y="298" width="704" height="52" rx="10" fill="%s" '
                 'fill-opacity="0.1" stroke="%s" stroke-width="1.6"/>' % (PINK, tv(PINK)))
        s.append('<rect x="40" y="309" width="30" height="30" rx="7" fill="%s" stroke="%s"/>'
                 % (oc, LINE))
        s.append(text(82, 318, "0.735 × [4, 0] + 0.043 × [2, 2] + 0.043 × [0, 4] + 0.179 × [1, 1]",
                      10.5, 700, fill=INK, anchor="start", mono=True))
        s.append(text(82, 338, "= [%.2f, %.2f]: the new vector for “it” is mostly “animal”"
                      % tuple(out), 11.5, 800, fill=INK, anchor="start"))
        # how much of each value went into the blend
        x = 566
        s.append(text(566, 313, "share of each value", 8.6, 700, fill=MUTED, anchor="start"))
        for k in range(4):
            wpx = 156 * wts[k]
            s.append('<rect x="%.1f" y="320" width="%.1f" height="18" fill="%s"/>'
                     % (x, wpx, _value_colour(_STEP_VALS[k])))
            x += wpx
        return "".join(s)

    parts = [col_dot, col_scl, col_bar, col_val]
    labels = ["Step 1, score: the dot product of q = [2, 1] with each key: 5, 1, 1 and 3",
              "Step 2, scale: divide each score by √2 ≈ 1.41, because the keys have 2 numbers",
              "Step 3, softmax: e to the power of each scaled score, divided by their total, 46.71",
              "Step 4, blend: 0.735 × [4, 0] + 0.043 × [2, 2] + 0.043 × [0, 4] + 0.179 × [1, 1] "
              "= [3.20, 0.44]"]
    stages = [step(n + 1, "".join(f() for f in parts[:n + 1]), labels[n]) for n in range(4)]
    desc = ("A stepped table for the query of it, q = 2, 1, against four tokens. Animal has key "
            "2, 1; cross 0, 1; street 1, minus 1; it 1, 1. Step 1, the dot products are 5, 1, 1 "
            "and 3. Step 2, divided by the square root of 2 they are 3.54, 0.71, 0.71 and 2.12. "
            "Step 3, softmax gives weights 0.735, 0.043, 0.043 and 0.179, drawn as amber bars. "
            "Step 4, the values 4, 0; 2, 2; 0, 4; and 1, 1, shown as colours from pink to blue, "
            "are blended by those weights into the new vector 3.20, 0.44, which is mostly the "
            "value of animal.")
    return figure_steps("ai-atts", 760, 356, "".join(base), stages,
                        "Scaled dot-product attention, step by step", desc,
                        "Score, scale, softmax, blend: the whole of attention for one token.",
                        labels=labels)


# ===================================================== attention matrix

_HEAT_WORDS = ["The", "animal", "didn't", "cross", "the", "street", "because", "it", "was",
               "too", "tired"]


def _heat_scores():
    n = len(_HEAT_WORDS)
    s = [[0.0] * n for _ in range(n)]
    for i in range(n):
        s[i][i] = 1.2
        if i > 0:
            s[i][i - 1] = 0.7
        if i < n - 1:
            s[i][i + 1] = 0.4
    special = {(0, 1): 1.6, (1, 3): 1.4, (2, 3): 1.8, (3, 1): 1.7, (3, 5): 1.9,
               (4, 5): 2.0, (5, 3): 1.5, (6, 2): 1.1, (6, 10): 1.0, (7, 1): 3.3,
               (7, 10): 1.6, (8, 7): 1.7, (8, 10): 1.3, (9, 10): 2.2, (10, 1): 2.4,
               (10, 7): 1.9}
    for (i, j), v in special.items():
        s[i][j] = v
    return s


@diagram("ai-attention-heatmap")
def _attention_heatmap():
    """An 11 by 11 attention matrix with each row summing to 1."""
    A = [_softmax(row) for row in _heat_scores()]
    n = len(_HEAT_WORDS)
    C, G = 26, 2
    X0, Y0 = 150, 118
    body = [text(380, 22, "The attention matrix: every token's weights over every token", 12,
                 650, fill=MUTED)]
    for j, w in enumerate(_HEAT_WORDS):
        body.append(_rot(X0 + j * (C + G) + C / 2.0 - 2, Y0 - 8, w, 10, 700, fill=INK))
    body.append(text(X0 - 10, Y0 - 30, "query ↓  key →", 9.6, 750, fill=MUTED, anchor="end"))
    for i, w in enumerate(_HEAT_WORDS):
        y = Y0 + i * (C + G)
        body.append(text(X0 - 8, y + C / 2.0 + 4, w, 10.5, 700 if w == "it" else 600,
                         fill=INK, anchor="end"))
        for j in range(n):
            v = A[i][j]
            col = plasma(min(1.0, v / 0.6))
            x = X0 + j * (C + G)
            body.append('<rect x="%d" y="%d" width="%d" height="%d" rx="3" fill="%s"/>'
                        % (x, y, C, C, col))
            if v >= 0.2:
                body.append(text(x + C / 2.0, y + C / 2.0 + 3.5, ("%.2f" % v)[1:], 9, 800,
                                 fill=ink_on(col)))
    iy = Y0 + 7 * (C + G)
    body.append('<rect x="%d" y="%d" width="%d" height="%d" rx="5" fill="none" stroke="%s" '
                'stroke-width="2.6"/>' % (X0 - 3, iy - 3, n * (C + G) + 4, C + 6, AMBER))
    # legend and notes
    LX = 494
    body.append(grad("ai-heat-g", [(i / 4.0, plasma(i / 4.0)) for i in range(5)]))
    body.append('<rect x="%d" y="122" width="200" height="14" rx="4" fill="url(#ai-heat-g)"/>' % LX)
    body.append(text(LX, 152, "0", 9.6, 650, fill=MUTED, anchor="start"))
    body.append(text(LX + 200, 152, "0.6 or more", 9.6, 650, fill=MUTED, anchor="end"))
    body.append(text(LX, 110, "attention weight", 10, 800, fill=INK, anchor="start"))
    notes_ = [("Each row is one token's query.", INK, 750),
              ("Each row adds up to 1.", INK, 750),
              ("Most tokens look at themselves", MUTED, 600),
              ("and their neighbours.", MUTED, 600),
              ("“it” (outlined) looks mostly at", tv(PINK), 750),
              ("“animal”, %.2f, and “tired”, %.2f." % (A[7][1], A[7][10]), tv(PINK), 750),
              ("“tired” looks back at “animal”.", MUTED, 600)]
    for k, (s, col, wgt) in enumerate(notes_):
        body.append(text(LX, 190 + k * 22, s, 10.5, wgt, fill=col, anchor="start"))
    body.append(text(LX, 360, "Weights here come from scores set by", 9.4, 600, fill=MUTED,
                     anchor="start"))
    body.append(text(LX, 374, "hand, to show patterns trained heads learn.", 9.4, 600,
                     fill=MUTED, anchor="start"))
    desc = ("An 11 by 11 grid of coloured cells, rows and columns labelled with the words of the "
            "sentence The animal didn't cross the street because it was too tired. Each row is "
            "one query token, each column a key, and colour runs from dark blue for 0 to yellow "
            "for high weights. Every row adds up to 1. The diagonal and the cells beside it are "
            "moderately bright, because tokens attend to themselves and their neighbours. The row "
            "for it, outlined in amber, is brightest under animal, %.2f, then tired, %.2f. The "
            "row for tired is brightest under animal. The weights are softmaxes of scores set by "
            "hand to illustrate patterns that trained attention heads learn."
            % (A[7][1], A[7][10]))
    return figure("ai-atth", 760, 432, "".join(body), "An attention matrix", desc,
                  "One head's attention matrix: a row per query, a column per key, each row "
                  "summing to 1.")


# ===================================================== causal mask

_MASK_WORDS = ["the", "cat", "sat", "on", "the", "mat"]


def _mask_scores():
    rnd = random.Random(12)
    return [[round(rnd.uniform(-1.2, 2.2), 1) for _ in _MASK_WORDS] for _ in _MASK_WORDS]


@diagram("ai-causal-mask")
def _causal_mask():
    """Scores with minus infinity above the diagonal, and the weights after softmax."""
    S = _mask_scores()
    n = len(_MASK_WORDS)
    masked = [[S[i][j] if j <= i else float("-inf") for j in range(n)] for i in range(n)]
    A = [_softmax(r) for r in masked]
    C, G = 34, 3
    body = [text(380, 22, "A causal mask: no token may attend to a later token", 12, 650,
                 fill=MUTED)]

    def grid(x0, y0, title, cell):
        out = [text(x0 + n * (C + G) / 2.0, y0 - 40, title, 11, 800, fill=INK)]
        for j, w in enumerate(_MASK_WORDS):
            out.append(text(x0 + j * (C + G) + C / 2.0, y0 - 10, w, 9.6, 700, fill=MUTED))
        for i, w in enumerate(_MASK_WORDS):
            out.append(text(x0 - 8, y0 + i * (C + G) + C / 2.0 + 4, w, 9.6, 700, fill=MUTED,
                            anchor="end"))
            for j in range(n):
                out.append(cell(x0 + j * (C + G), y0 + i * (C + G), i, j))
        return "".join(out)

    def score_cell(x, y, i, j):
        if j > i:
            return ('<rect x="%d" y="%d" width="%d" height="%d" rx="4" fill="%s" stroke="%s" '
                    'stroke-dasharray="3 3"/>' % (x, y, C, C, FILL2, LINE)
                    + text(x + C / 2.0, y + C / 2.0 + 4, "−∞", 11, 800, fill=MUTED))
        v = S[i][j]
        col = diverging(max(-1, min(1, v / 2.2)))
        return ('<rect x="%d" y="%d" width="%d" height="%d" rx="4" fill="%s"/>' % (x, y, C, C, col)
                + text(x + C / 2.0, y + C / 2.0 + 4, ("%.1f" % v).replace("-", "−"), 10, 750,
                       fill=ink_on(col)))

    def weight_cell(x, y, i, j):
        v = A[i][j]
        if j > i:
            return ('<rect x="%d" y="%d" width="%d" height="%d" rx="4" fill="%s"/>'
                    % (x, y, C, C, FILL2) + text(x + C / 2.0, y + C / 2.0 + 4, "0", 10, 700,
                                                 fill=MUTED))
        col = plasma(min(1.0, v / 0.8))
        return ('<rect x="%d" y="%d" width="%d" height="%d" rx="4" fill="%s"/>' % (x, y, C, C, col)
                + text(x + C / 2.0, y + C / 2.0 + 4, "%.2f" % v, 9.6, 750, fill=ink_on(col)))

    body.append(grid(80, 96, "scores, with the mask added", score_cell))
    body.append(grid(486, 96, "attention weights", weight_cell))
    body.append(arrow(318, 200, 440, 200, tv(VIOLET), 2.6))
    body.append(text(379, 190, "softmax, row by row", 10.5, 800, fill=tv(VIOLET)))
    body.append(text(379, 218, "e to the power −∞ is 0", 9.6, 650, fill=MUTED))
    body.append(text(380, 336, "Row 1 (“the”) can only see itself, so its weight is 1. The last "
                     "row sees all six tokens. Every row still adds up to 1.", 10, 650, fill=INK))
    rows = "; ".join("%s: %s" % (_MASK_WORDS[i], ", ".join("%.2f" % A[i][j] for j in range(i + 1)))
                     for i in range(n))
    desc = ("Two 6 by 6 grids for the tokens the cat sat on the mat. The left grid holds scores; "
            "every cell above the diagonal, where the key comes after the query, is replaced by "
            "minus infinity and drawn grey. An arrow labelled softmax, row by row, leads to the "
            "right grid of attention weights, where those cells are exactly 0. The weights on and "
            "below the diagonal, row by row, are %s." % rows)
    return figure("ai-mask", 760, 350, "".join(body), "A causal mask", desc,
                  "Masking happens before the softmax, so each row's weights still add up to 1.")


# ===================================================== multi-head

_HEADS = [
    ("head 1: the previous word", VIOLET,
     [[1, 0, 0, 0], [0.85, 0.15, 0, 0], [0.05, 0.85, 0.1, 0], [0.03, 0.05, 0.85, 0.07]]),
    ("head 2: the subject", PINK,
     [[1, 0, 0, 0], [0.8, 0.2, 0, 0], [0.7, 0.1, 0.2, 0], [0.75, 0.1, 0.05, 0.1]]),
    ("head 3: the word itself", TEAL,
     [[1, 0, 0, 0], [0.2, 0.8, 0, 0], [0.1, 0.1, 0.8, 0], [0.05, 0.1, 0.05, 0.8]]),
]
_MH_TOK = ["she", "saw", "the", "bird"]


def _stack(x, y, cell, colours, rows=4, cols=6, gap=2):
    out = []
    for i in range(rows):
        for j in range(cols):
            out.append('<rect x="%.1f" y="%.1f" width="%d" height="%d" rx="2" fill="%s"/>'
                       % (x + j * (cell + gap), y + i * (cell + gap), cell, cell, colours(i, j)))
    return "".join(out)


@diagram("ai-multi-head")
def _multi_head():
    """Three heads with their own weights, concatenated and mixed by W_O."""
    rnd = random.Random(3)
    tone = [[rnd.random() for _ in range(6)] for _ in range(4)]
    body = [text(380, 22, "Multi-head attention: several heads look for different things at "
                 "once", 12, 650, fill=MUTED)]
    # input
    body.append(text(84, 128, "input", 10.5, 800, fill=INK))
    body.append(text(84, 142, "4 tokens × 6", 9.4, 650, fill=MUTED))
    body.append(_stack(48, 156, 10, lambda i, j: plasma(0.2 + 0.7 * tone[i][j])))
    for i, w in enumerate(_MH_TOK):
        body.append(text(42, 156 + i * 12 + 9, w, 8.6, 700, fill=MUTED, anchor="end"))
    for h, (title, col, pat) in enumerate(_HEADS):
        y0 = 40 + h * 104
        body.append(arrow(122, 178, 196, y0 + 48, LINE, 1.5))
        body.append(tint(200, y0, 236, 94, col, op=0.1, r=12))
        body.append(text(318, y0 + 18, title, 10.5, 800, fill=tv(col)))
        for k, sub in enumerate("QKV"):
            body.append(solid(212 + k * 38, y0 + 32, 34, 24, col, r=5))
            body.append(_wsub(229 + k * 38, y0 + 48, "W", sub, 11, 800, fill=WHITE))
        body.append(text(268, y0 + 76, "its own weights", 9, 650, fill=MUTED))
        hx, hy = 344, y0 + 28
        for i in range(4):
            for j in range(4):
                v = pat[i][j]
                body.append('<rect x="%d" y="%d" width="13" height="13" rx="2" fill="%s"/>'
                            % (hx + j * 15, hy + i * 15, plasma(min(1.0, v / 0.85))))
        body.append(arrow(436, y0 + 48, 486, 178, tv(col), 1.6))
    # concatenate
    hc = [VIOLET, VIOLET, PINK, PINK, TEAL, TEAL]
    body.append(text(532, 128, "concatenate", 10.5, 800, fill=INK))
    body.append(text(532, 142, "2 + 2 + 2 = 6", 9.4, 650, fill=MUTED))
    body.append(_stack(492, 156, 12, lambda i, j: _mix("#FFFFFF", hc[j], 0.55 + 0.4 * tone[3 - i][j])))
    body.append(arrow(578, 178, 600, 178, LINE, 1.6))
    body.append(cube(604, 158, 54, 40, 12, INDIGO))
    body.append(_wsub(631, 183, "× W", "O", 11.5, 800, fill=WHITE))
    body.append(arrow(668, 178, 684, 178, LINE, 1.6))
    body.append(text(714, 128, "output", 10.5, 800, fill=INK))
    body.append(text(714, 142, "4 tokens × 6", 9.4, 650, fill=MUTED))
    body.append(_stack(688, 156, 8, lambda i, j: plasma(0.15 + 0.8 * tone[(i + 1) % 4][(j + 2) % 6])))
    body.append(text(612, 300, "Each head works on 6 ÷ 3 = 2 numbers, so", 10, 650, fill=MUTED))
    body.append(text(612, 315, "three heads cost about the same as one.", 10, 650, fill=MUTED))
    desc = ("Four input tokens, she, saw, the, bird, each a vector of 6 numbers, fan out to three "
            "attention heads, each with its own W Q, W K and W V. Head 1 attends to the previous "
            "word, so its 4 by 4 pattern is bright just below the diagonal. Head 2 attends to the "
            "subject, so its first column is bright. Head 3 attends to each word itself, so its "
            "diagonal is bright. Each head outputs 2 numbers per token; the three outputs are "
            "concatenated into 6 numbers, coloured violet, pink and teal, then multiplied by W O "
            "to give the output, 4 tokens by 6 numbers. The patterns are illustrations of the "
            "kinds of pattern found in trained models.")
    return figure("ai-mha", 760, 360, "".join(body), "Multi-head attention", desc,
                  "Illustrative patterns: trained models contain heads much like these.")


# ===================================================== positional encoding

def _pe(pos, i, d):
    k = i // 2
    ang = pos / 10000 ** (2.0 * k / d)
    return math.sin(ang) if i % 2 == 0 else math.cos(ang)


@diagram("ai-positional-encoding")
def _positional_encoding():
    """A heatmap of sinusoidal encodings, and four of its waves."""
    D, P = 24, 20
    CW, CH = 13, 9
    X0, Y0 = 62, 78
    body = [text(380, 22, "Sinusoidal positional encoding: a unique wave pattern for every "
                 "position", 12, 650, fill=MUTED)]
    for p in range(P):
        for i in range(D):
            v = _pe(p, i, D)
            body.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>'
                        % (X0 + i * CW, Y0 + p * CH, CW - 1, CH - 1, diverging(v)))
    body.append(text(X0 + D * CW / 2.0, 52, "dimension →", 10, 750, fill=MUTED))
    for i in (0, 8, 16, 23):
        body.append(text(X0 + i * CW + CW / 2.0, Y0 - 6, str(i), 8.6, 650, fill=MUTED))
    for p in (0, 5, 10, 15, 19):
        body.append(text(X0 - 6, Y0 + p * CH + 7, str(p), 8.6, 650, fill=MUTED, anchor="end"))
    cx, cy = 26, Y0 + P * CH / 2.0
    body.append('<text x="%d" y="%.1f" text-anchor="middle" font-size="10" font-weight="750" '
                'fill="%s" transform="rotate(-90 %d %.1f)">position ↓</text>' % (cx, cy, MUTED, cx, cy))
    picks = [(0, PINK), (2, VIOLET), (4, BLUE), (8, TEAL)]
    for i, col in picks:
        x = X0 + i * CW + CW / 2.0
        body.append('<polygon points="%.1f,%d %.1f,%d %.1f,%d" fill="%s"/>'
                    % (x - 4, Y0 + P * CH + 10, x + 4, Y0 + P * CH + 10, x, Y0 + P * CH + 3, tv(col)))
    body.append(text(X0 + D * CW / 2.0, Y0 + P * CH + 28, "blue −1, white 0, pink +1", 9.4, 650,
                     fill=MUTED))
    pl = Plot(450, 70, 280, 170, (0, 19), (-1.15, 1.15))
    body.append(pl.axes(xticks=(0, 5, 10, 15), yticks=(-1, 0, 1), xlabel="position"))
    for i, col in picks:
        body.append(path(pl.curve(lambda p, i=i: _pe(p, i, D), 160), stroke=tv(col), w=2.4))
    leg = [("dimension 0: fast", PINK), ("dimension 2", VIOLET), ("dimension 4", BLUE),
           ("dimension 8: slow", TEAL)]
    for k, (s, col) in enumerate(leg):
        lx, ly = 450 + (k % 2) * 150, 290 + (k // 2) * 18
        body.append(line(lx, ly - 4, lx + 18, ly - 4, stroke=tv(col), w=3))
        body.append(text(lx + 24, ly, s, 9.8, 700, fill=INK, anchor="start"))
    desc = ("Left: a grid of 20 rows, positions 0 to 19, by 24 columns, dimensions 0 to 23, "
            "coloured blue for minus 1, white for 0 and pink for plus 1. The left-hand columns "
            "alternate colour quickly down the rows; the right-hand columns hardly change. "
            "Right: four of the columns drawn as waves against position: dimension 0 in pink "
            "repeats about every 6 positions, dimension 2 in violet every 13 or so, dimension 4 "
            "in blue more slowly, and dimension 8 in teal is almost flat. Together they give "
            "every position a different pattern.")
    return figure("ai-pe", 760, 330, "".join(body), "Sinusoidal positional encoding", desc,
                  "Like the hands of a clock: fast waves tell nearby positions apart, slow waves "
                  "tell distant ones apart.")


# ===================================================== transformer block

@diagram("ai-transformer-block")
def _transformer_block():
    """The block, bottom to top, with residual connections."""
    body = [text(380, 22, "Inside a transformer: a stack of identical blocks", 12, 650,
                 fill=MUTED)]
    for k, w in enumerate(["The", "cat", "sat"]):
        body.append(tint(222 + k * 64, 520, 52, 24, SLATE, w, r=7, size=11, op=0.1))
    body.append(arrow(290, 518, 290, 498, LINE, 1.6))
    body.append(cube(190, 462, 200, 32, 14, BLUE, "Token embeddings", size=11.5))
    body.append(arrow(290, 456, 290, 446, LINE, 1.6))
    body.append(circle(290, 434, 11, fill=AMBER, stroke=FILL, w=2))
    body.append(text(290, 439, "+", 15, 900, fill=DARK))
    wave = " ".join("%s%.1f %.1f" % ("M" if i == 0 else "L", 312 + i * 1.2,
                                    434 - 7 * math.sin(i * 0.22)) for i in range(50))
    body.append(path(wave, stroke=tv(ORANGE), w=2))
    body.append(text(378, 438, "positional encoding", 10, 750, fill=INK, anchor="start"))
    # the block
    body.append('<rect x="150" y="150" width="292" height="268" rx="16" fill="%s" '
                'fill-opacity="0.05" stroke="%s" stroke-width="2" stroke-dasharray="7 5"/>'
                % (VIOLET, tv(VIOLET)))
    body.append(text(96, 290, "× N", 24, 900, fill=tv(VIOLET)))
    body.append(text(96, 310, "12 in GPT-2 small", 9, 650, fill=MUTED))
    body.append(text(96, 323, "96 in GPT-3", 9, 650, fill=MUTED))
    body.append(arrow(290, 423, 290, 406, LINE, 1.8))
    body.append(cube(190, 366, 200, 38, 14, VIOLET, "Multi-head self-attention", size=11.5))
    body.append(arrow(290, 360, 290, 343, LINE, 1.8))
    body.append(cube(190, 318, 200, 22, 10, TEAL, "Add & norm", size=10.5))
    body.append(arrow(290, 312, 290, 289, LINE, 1.8))
    body.append(cube(190, 249, 200, 38, 14, PINK, "Feed-forward network", size=11.5))
    body.append(arrow(290, 243, 290, 226, LINE, 1.8))
    body.append(cube(190, 201, 200, 22, 10, TEAL, "Add & norm", size=10.5))
    # residual connections
    for d, ay in [("M290 414 H 424 V 329 H 410", 329), ("M290 300 H 424 V 212 H 410", 212)]:
        body.append(path(d, stroke=AMBER, w=2.6))
        # a white dash that runs along the connection when motion is allowed
        body.append('<path d="%s" fill="none" stroke="%s" stroke-width="1.2" stroke-opacity="0.9" '
                    'stroke-dasharray="0 1000" class="ai-flow"/>' % (d, WHITE))
        body.append(arrow(412, ay, 401, ay, AMBER, 2.6))
    body.append(circle(290, 414, 3.5, fill=AMBER, stroke=AMBER, w=1))
    body.append(circle(290, 300, 3.5, fill=AMBER, stroke=AMBER, w=1))
    # out of the stack
    body.append(arrow(290, 195, 290, 132, LINE, 1.8))
    body.append(cube(210, 100, 160, 28, 10, INDIGO, "Linear: unembed", size=10.5))
    body.append(arrow(290, 94, 290, 76, LINE, 1.6))
    body.append(solid(214, 46, 152, 28, ORANGE, "softmax", r=8, size=11))
    for k, (w, p) in enumerate([("on", 0.62), ("down", 0.3), ("still", 0.16)]):
        y = 42 + k * 13
        body.append(text(398, y + 8, w, 9, 700, fill=INK, anchor="end"))
        body.append('<rect x="404" y="%d" width="%.1f" height="9" rx="2" fill="%s"/>'
                    % (y, 70 * p, AMBER))
    # notes
    notes_ = [(113, "a score for every token in the vocabulary", INK),
              (61, "probabilities for the next token", INK),
              (268, "each token on its own: d → 4d → d", INK),
              (284, "about 8 × d² parameters", MUTED),
              (385, "tokens exchange information", INK),
              (401, "about 4 × d² parameters", MUTED),
              (333, "add the input back, then rescale", INK),
              (478, "one vector of d numbers per token", INK)]
    for y, s, col in notes_:
        body.append(text(486, y, s, 10.5, 750 if col == INK else 600, fill=col, anchor="start"))
    body.append(line(460, 500, 484, 500, stroke=AMBER, w=3))
    body.append(text(490, 504, "residual connection", 10, 750, fill=INK, anchor="start"))
    desc = ("A tall diagram read from bottom to top. Tokens The, cat, sat enter a blue block, "
            "token embeddings, then a positional encoding is added. A dashed violet box marked "
            "times N, 12 in GPT-2 small and 96 in GPT-3, contains: multi-head self-attention, "
            "where tokens exchange information, about 4 d squared parameters; add and norm; a "
            "feed-forward network that processes each token on its own, d to 4d to d, about 8 d "
            "squared parameters; and add and norm again. Amber residual connections run around "
            "the right side of each sublayer from its input to its add and norm. Above the stack, "
            "a linear unembedding layer gives a score for every vocabulary token and a softmax "
            "turns the scores into next-token probabilities, shown as bars for on, down and "
            "still.")
    return figure("ai-tblk", 760, 556, "".join(body), "A transformer block", desc,
                  "Attention, then a feed-forward network, each wrapped in a residual connection "
                  "and normalisation, stacked N times.")


# ===================================================== residual stream

@diagram("ai-residual-stream")
def _residual_stream():
    """Token lanes flowing up; attention between lanes, feed-forward on each."""
    toks = ["The", "cat", "sat", "on"]
    xs = [130, 240, 350, 460]
    body = [text(380, 22, "The residual stream: one lane per token, flowing upward", 12, 650,
                 fill=MUTED)]
    body.append('<defs><linearGradient id="ai-rs-lane" x1="0" y1="0" x2="1" y2="0">'
                '<stop offset="0" stop-color="%s" stop-opacity="0.55"/>'
                '<stop offset="0.5" stop-color="%s" stop-opacity="0.18"/>'
                '<stop offset="1" stop-color="%s" stop-opacity="0.55"/>'
                '</linearGradient></defs>' % (SKY, SKY, SKY))
    for x in xs:
        body.append('<rect x="%d" y="58" width="46" height="318" rx="23" fill="url(#ai-rs-lane)" '
                    'stroke="%s" stroke-width="1.2"/>' % (x - 23, tv(BLUE)))
        body.append('<line x1="%d" y1="368" x2="%d" y2="66" stroke="%s" stroke-width="2.4" '
                    'class="ai-flow" stroke-dasharray="6 8"/>' % (x, x, tv(BLUE)))
    for k, (x, t) in enumerate(zip(xs, toks)):
        body.append(tint(x - 26, 384, 52, 24, SLATE, t, r=7, size=11, op=0.12))
    links = [(0, 1, 0.9), (1, 2, 0.6), (0, 3, 0.5), (2, 3, 0.9), (0, 2, 0.4)]
    for ly, (ay, fy) in enumerate([(312, 262), (196, 146)]):
        body.append('<rect x="92" y="%d" width="406" height="30" rx="10" fill="%s" fill-opacity="0.16" '
                    'stroke="%s" stroke-width="1.4"/>' % (ay - 15, VIOLET, tv(VIOLET)))
        for a, b, wgt in links:
            x1, x2 = xs[a] + 8, xs[b] - 8
            body.append('<path d="M%d %d C %d %d, %d %d, %d %d" fill="none" stroke="%s" '
                        'stroke-width="%.1f" stroke-linecap="round"/>'
                        % (x1, ay + 6, x1 + 20, ay - 26 - 6 * (b - a), x2 - 20, ay - 26 - 6 * (b - a),
                           x2, ay + 6, tv(VIOLET), 1 + 2.4 * wgt))
            body.append('<circle cx="%d" cy="%d" r="3" fill="%s"/>' % (x2, ay + 6, tv(VIOLET)))
        for x in xs:
            body.append(solid(x - 22, fy - 13, 44, 26, PINK, "FF", r=7, size=10.5))
            body.append(circle(x + 22, fy - 13, 7, fill=AMBER, stroke=FILL, w=1.5))
            body.append(text(x + 22, fy - 9.5, "+", 10, 900, fill=DARK))
        body.append(text(76, ay + 4, "layer %d" % (ly + 1), 10, 800, fill=MUTED, anchor="end"))
    body.append(arrow(460, 56, 460, 40, tv(BLUE), 2))
    body.append(solid(500, 28, 150, 26, ORANGE, "next token: “the”", r=8, size=10.5))
    body.append(path("M468 40 C 480 40, 488 41, 498 41", stroke=tv(ORANGE), w=2))
    notes_ = [(312, "attention: the only place", tv(VIOLET)),
              (327, "information moves between lanes", tv(VIOLET)),
              (258, "feed-forward: each lane", tv(PINK)),
              (273, "processed on its own", tv(PINK)),
              (142, "+ every sublayer adds its", INK),
              (157, "result into the stream", INK),
              (78, "the last lane ends up holding", INK),
              (93, "what is needed to predict", INK),
              (108, "the next token", INK)]
    for y, s, col in notes_:
        body.append(text(536, y, s, 10.5, 750, fill=col, anchor="start"))
    desc = ("Four translucent blue lanes rise from the tokens The, cat, sat and on, with dashes "
            "flowing upward along each. Two layers cross the lanes. In each, a violet attention "
            "band carries curved arrows from earlier lanes to later ones: attention is the only "
            "place information moves between lanes. Above each band, every lane passes through "
            "its own pink feed-forward box, marked with a plus sign because each sublayer adds "
            "its result into the stream. At the top, the lane for the last token, on, leads to "
            "the prediction of the next token, the.")
    return figure("ai-rstr", 760, 420, "".join(body), "The residual stream", desc,
                  "Attention moves information between tokens; feed-forward layers work on each "
                  "token; everything is added into the stream.")


# ===================================================== three families

@diagram("ai-transformer-family")
def _transformer_family():
    """Encoder-only, encoder-decoder and decoder-only, with their masks."""
    body = [text(380, 22, "Three families built from the same block", 12, 650, fill=MUTED)]
    rnd = random.Random(8)

    def mask(x0, y0, n, cell, colour, causal):
        out = []
        for i in range(n):
            for j in range(n):
                on = (not causal) or j <= i
                fillc = _mix("#FFFFFF", colour, 0.45 + 0.5 * rnd.random()) if on else FILL2
                out.append('<rect x="%d" y="%d" width="%d" height="%d" rx="2" fill="%s"/>'
                           % (x0 + j * (cell + 2), y0 + i * (cell + 2), cell, cell, fillc))
        return "".join(out)
    cards = [("Encoder-only", BLUE, ["sees every token, both ways", "trained to fill in hidden words",
                                     "BERT (2018)", "good at understanding:", "classifying, searching"]),
             ("Encoder-decoder", VIOLET, ["encoder sees everything; the", "decoder is masked and looks",
                                          "back with cross-attention", "2017 transformer, T5 (2019)",
                                          "good at translating, summarising"]),
             ("Decoder-only", PINK, ["each token sees only earlier", "tokens: a causal mask",
                                     "trained to predict the next token", "the GPT series, most chatbots",
                                     "good at generating text and code"])]
    for c, (title, col, lines) in enumerate(cards):
        x0 = 20 + c * 250
        body.append(tint(x0, 40, 220, 282, col, op=0.07, r=14))
        body.append(solid(x0, 40, 220, 34, col, title, r=12, size=12.5))
        if c == 1:
            body.append(mask(x0 + 26, 96, 5, 13, BLUE, False))
            body.append(mask(x0 + 122, 96, 5, 13, PINK, True))
            body.append(text(x0 + 63, 186, "encoder", 9, 700, fill=MUTED))
            body.append(text(x0 + 159, 186, "decoder", 9, 700, fill=MUTED))
            body.append(path("M%d 104 C %d 84, %d 84, %d 104" % (x0 + 98, x0 + 106, x0 + 114, x0 + 120),
                             stroke=AMBER, w=2.2))
            body.append(text(x0 + 110, 88, "cross", 8.6, 750, fill=INK))
        else:
            body.append(mask(x0 + 66, 90, 5, 16, col, c == 2))
            body.append(text(x0 + 110, 192, "full attention" if c == 0 else "causal mask", 9.4,
                             700, fill=MUTED))
        for k, s in enumerate(lines):
            body.append(text(x0 + 110, 222 + k * 19, s, 10, 750 if k in (2, 3) else 600,
                             fill=INK if k != 3 else tv(col)))
    desc = ("Three cards. Encoder-only, in blue: a 5 by 5 grid fully coloured, because every token "
            "sees every token both ways; trained to fill in hidden words; BERT, 2018; good at "
            "understanding tasks such as classifying and searching. Encoder-decoder, in violet: a "
            "full encoder grid and a lower-triangle decoder grid joined by an amber cross-attention "
            "arc; the 2017 transformer and T5, 2019; good at translating and summarising. "
            "Decoder-only, in pink: a lower-triangle grid, the causal mask, where each token sees "
            "only earlier tokens; trained to predict the next token; the GPT series and most "
            "chatbots; good at generating text and code.")
    return figure("ai-tfam", 760, 334, "".join(body), "Three families of transformer", desc,
                  "The masks are the difference: full attention for understanding, causal "
                  "attention for generating.")


# ===================================================== vision transformer

_CAT12 = ["............",
          ".XX......XX.",
          ".XXX....XXX.",
          ".XXXXXXXXXX.",
          ".XXXXXXXXXX.",
          ".XGGXXXXGGX.",
          ".XGDXXXXGDX.",
          ".XXXXWWXXXX.",
          ".XXXWPPWXXX.",
          "..XXXDDXXX..",
          "...XXXXXX...",
          "............"]
_CAT_PAL = {"X": "#EA580C", "G": "#22C55E", "D": "#1F2937", "P": "#DB2777", "W": "#FDE68A",
            ".": "#38BDF8"}


def _pixels(x, y, s, r0, c0, n):
    out = []
    for i in range(n):
        for j in range(n):
            ch = _CAT12[r0 + i][c0 + j]
            out.append('<rect x="%.1f" y="%.1f" width="%.2f" height="%.2f" fill="%s"/>'
                       % (x + j * s, y + i * s, s + 0.15, s + 0.15, _CAT_PAL[ch]))
    return "".join(out)


@diagram("ai-vit-patches")
def _vit_patches():
    """An image cut into nine patches, read as nine tokens."""
    body = [text(380, 22, "A Vision Transformer reads an image as a sequence of patches", 12,
                 650, fill=MUTED)]
    S = 11
    IX, IY = 30, 70
    body.append(_pixels(IX, IY, S, 0, 0, 12))
    for k in (1, 2):
        body.append(line(IX + k * 4 * S, IY, IX + k * 4 * S, IY + 12 * S, stroke=WHITE, w=2.5))
        body.append(line(IX, IY + k * 4 * S, IX + 12 * S, IY + k * 4 * S, stroke=WHITE, w=2.5))
    body.append('<rect x="%d" y="%d" width="%d" height="%d" fill="none" stroke="%s" stroke-width="1.5"/>'
                % (IX, IY, 12 * S, 12 * S, LINE))
    body.append(text(IX + 6 * S, IY + 12 * S + 18, "12 × 12 pixels", 9.6, 700, fill=INK))
    body.append(text(IX + 6 * S, IY + 12 * S + 32, "cut into 9 patches", 9.6, 650, fill=MUTED))
    body.append(path("M%d %d C %d %d, %d %d, %d %d" % (IX + 12 * S + 6, IY + 100, 200, 230, 190, 262, 206, 262),
                     stroke=LINE, w=1.6, arrow=True))
    TX, TY, T = 216, 244, 36
    body.append(solid(TX, TY, T, T, AMBER, "cls", r=6, size=10))
    body.append(text(TX + T / 2.0, TY + T + 14, "class", 8.6, 700, fill=MUTED))
    for p in range(9):
        r0, c0 = (p // 3) * 4, (p % 3) * 4
        x = TX + (p + 1) * (T + 8)
        body.append(_pixels(x, TY, T / 4.0, r0, c0, 4))
        body.append('<rect x="%d" y="%d" width="%d" height="%d" fill="none" stroke="%s"/>'
                    % (x, TY, T, T, LINE))
        body.append(text(x + T / 2.0, TY + T + 14, "+ pos %d" % (p + 1), 8.6, 700, fill=MUTED))
    for p in range(10):
        x = TX + p * (T + 8) + T / 2.0
        body.append(arrow(x, TY - 4, x, 180, LINE, 1.3))
    body.append(cube(TX - 4, 132, 444, 44, 18, VIOLET))
    body.append(text(TX + 218, 159, "Transformer encoder: the same blocks used for text", 11.5,
                     800, fill=WHITE))
    body.append(path("M%d 128 C %d 98, %d 86, %d 86" % (TX + 18, TX + 18, 640, 668),
                     stroke=tv(PINK), w=2.2, arrow=True))
    body.append(solid(672, 70, 72, 32, PINK, "“cat”", r=8, size=12))
    body.append(text(708, 60, "prediction", 9.4, 700, fill=MUTED))
    body.append(text(380, 318, "A real ViT cuts a 224 × 224 image into 16 × 16 patches: 196 tokens.",
                     10, 650, fill=MUTED))
    desc = ("A 12 by 12 pixel picture of an orange cat on a blue background is cut by white "
            "lines into a 3 by 3 grid of patches, each 4 by 4 pixels. The nine patches are laid "
            "out in a row as tokens, each with its position added, after an extra amber class "
            "token. Arrows lead from every token up into a violet transformer encoder, the same "
            "kind of blocks used for text, and from the class token's output to the prediction, "
            "cat. A real Vision Transformer cuts a 224 by 224 image into 16 by 16 patches, "
            "giving 196 tokens.")
    return figure("ai-vit", 760, 332, "".join(body), "A Vision Transformer", desc,
                  "Patches play the part of words, so the same architecture reads images.")


# ===================================================== the cost of attention

@diagram("ai-attention-cost")
def _attention_cost():
    """n tokens need n × n scores: the square law."""
    body = [text(380, 22, "Attention's cost grows with the square of the number of tokens", 12,
                 650, fill=MUTED)]
    rnd = random.Random(5)
    base_y = 236
    for n, x0 in [(4, 30), (8, 92), (16, 194)]:
        cell = 7
        size = n * (cell + 1)
        y0 = base_y - size
        for i in range(n):
            for j in range(n):
                body.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>'
                            % (x0 + j * (cell + 1), y0 + i * (cell + 1), cell, cell,
                               plasma(0.25 + 0.7 * rnd.random())))
        body.append(text(x0 + size / 2.0, base_y + 18, "%d tokens" % n, 10, 800, fill=INK))
        body.append(text(x0 + size / 2.0, base_y + 33, "%d scores" % (n * n), 9.6, 650,
                         fill=MUTED))
    body.append(text(190, 290, "Double the tokens, four times the scores.", 10.5, 750,
                     fill=tv(VIOLET)))
    pl = Plot(470, 56, 250, 180, (0, 128), (0, 18))
    body.append(pl.axes(xticks=(0, 32, 64, 96, 128), yticks=(0, 5, 10, 15),
                        xlabel="context length, thousands of tokens"))
    cx, cy = 432, 56 + 90
    body.append('<text x="%d" y="%d" text-anchor="middle" font-size="9.6" font-weight="650" '
                'fill="%s" transform="rotate(-90 %d %d)">billions of scores</text>'
                % (cx, cy, MUTED, cx, cy))
    body.append(path(pl.curve(lambda k: (k * 1000.0) ** 2 / 1e9, 120), stroke=tv(PINK), w=2.8))
    for k in (8, 32, 128):
        x, y = pl.pt(k, (k * 1000.0) ** 2 / 1e9)
        body.append(circle(x, y, 4.5, fill=PINK, stroke=FILL, w=1.5))
        body.append(_halo(x if k != 128 else x - 8, y - 10, "%dk" % k, 9.6, 800,
                          "middle" if k != 128 else "end"))
    for i, s_ in enumerate(["8k tokens: 0.06 billion", "32k tokens: 1 billion",
                            "128k tokens: 16.4 billion"]):
        body.append(text(484, 76 + i * 16, s_, 9.6, 750, fill=INK, anchor="start"))
    body.append(text(596, 290, "per head, per layer, for every forward pass", 9.6, 650,
                     fill=MUTED))
    desc = ("Left: three square grids of coloured cells at the same cell size. 4 tokens need a 4 "
            "by 4 grid, 16 scores; 8 tokens need 64 scores; 16 tokens need 256 scores. Double "
            "the tokens, four times the scores. Right: a curve of the number of scores against "
            "context length rising ever more steeply: 8 thousand tokens need about 0.06 billion "
            "scores, 32 thousand about 1 billion, and 128 thousand about 16.4 billion, per head, "
            "per layer.")
    return figure("ai-acost", 760, 304, "".join(body), "The cost of attention", desc,
                  "This square law is why long contexts are expensive, and why so much research "
                  "goes into faster attention.")
