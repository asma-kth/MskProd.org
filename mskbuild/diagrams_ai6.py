"""AI course diagrams, Level 11: large language models.

The sampling probabilities, the scaling curves (from the loss formula fitted
in the Chinchilla paper), the LoRA and quantisation sizes and the data mix
(from the LLaMA paper) are computed or quoted exactly; the conversations and
the pipelines are illustrations.
"""
import math
import random

from .diagrams import diagram
from .svg import figure, text, line, path, circle, esc
from .diagrams_ai_kit import (INK, MUTED, FILL, FILL2, LINE, VIOLET, PINK, BLUE,
                              TEAL, GREEN, ORANGE, RED, INDIGO, AMBER, LIME,
                              CYAN, ROSE, SKY, PURPLE, SLATE, WHITE, DARK, tv,
                              solid, tint, grad, plasma, diverging, ink_on,
                              arrow, cube)
from .diagrams_ai2 import Plot, _halo
from .diagrams_ai5 import _softmax, _wsub, _mix


def _cylinder(cx, top, w, h, colour, label=None, sub=None):
    """A 3D drum, for a pile of data or a database."""
    rx, ry = w / 2.0, w * 0.16
    out = ['<path d="M%.1f %.1f V %.1f A %.1f %.1f 0 0 0 %.1f %.1f V %.1f Z" fill="%s"/>'
           % (cx - rx, top, top + h, rx, ry, cx + rx, top + h, top, colour),
           '<path d="M%.1f %.1f A %.1f %.1f 0 0 0 %.1f %.1f" fill="none" stroke="%s" '
           'stroke-width="1.2" stroke-opacity="0.5"/>' % (cx - rx, top + h * 0.5, rx, ry, cx + rx,
                                                         top + h * 0.5, WHITE),
           '<ellipse cx="%.1f" cy="%.1f" rx="%.1f" ry="%.1f" fill="%s"/>'
           % (cx, top, rx, ry, _mix(colour, "#FFFFFF", 0.35))]
    if label:
        out.append(text(cx, top + h * 0.5 + 8, label, 11, 800, fill=ink_on(colour)))
    if sub:
        out.append(text(cx, top - ry - 8, sub, 9.6, 700, fill=MUTED))
    return "".join(out)


def _bubble(x, y, w, h, colour, lines, tail=None):
    out = ['<rect x="%d" y="%d" width="%d" height="%d" rx="12" fill="%s" fill-opacity="0.12" '
           'stroke="%s" stroke-width="1.5"/>' % (x, y, w, h, colour, tv(colour))]
    if tail:
        tx = tail
        out.append('<path d="M%d %d L %d %d L %d %d" fill="%s" fill-opacity="0.12" stroke="%s" '
                   'stroke-width="1.5" stroke-linejoin="round"/>'
                   % (tx - 8, y, tx, y - 10, tx + 8, y, colour, tv(colour)))
    for k, s in enumerate(lines):
        out.append(text(x + w / 2.0, y + 19 + k * 15, s, 10, 650 if k else 750, fill=INK))
    return "".join(out)


# ===================================================== the three stages

@diagram("ai-llm-pipeline")
def _llm_pipeline():
    """Pretraining, instruction tuning, preference tuning, with what each adds."""
    body = [text(380, 22, "From a transformer to an assistant: three stages of training", 12,
                 650, fill=MUTED)]
    stages = [(130, BLUE, "Pretraining", "next-token prediction", 100, 92,
               "trillions of tokens", "web, books, code", "most of the compute"),
              (380, VIOLET, "Instruction tuning", "supervised fine-tuning", 74, 46,
               "example conversations", "prompt + ideal reply", "a small fraction"),
              (630, PINK, "Preference tuning", "RLHF or DPO", 56, 28,
               "people's comparisons", "answer A or answer B?", "a small fraction")]
    for k, (cx, col, name, sub, w, h, d1, d2, cost) in enumerate(stages):
        body.append(_cylinder(cx, 176 - h, w, h, col))
        body.append(text(cx, 176 - h - w * 0.16 - 22, d1, 10.5, 800, fill=INK))
        body.append(text(cx, 176 - h - w * 0.16 - 8, d2, 9.4, 650, fill=MUTED))
        body.append(arrow(cx, 192 + w * 0.16 - 14, cx, 206, LINE, 1.6))
        body.append(cube(cx - 90, 212, 168, 44, 14, col))
        body.append(text(cx - 6, 232, name, 12, 800, fill=WHITE))
        body.append(text(cx - 6, 248, sub, 9.6, 650, fill=WHITE))
        body.append(text(cx - 6, 274, cost, 9.4, 700, fill=MUTED))
        if k < 2:
            body.append(arrow(cx + 92, 234, cx + 156, 234, tv(col), 2.4))
    body.append(text(255, 222, "base model", 9.6, 800, fill=tv(BLUE)))
    body.append(text(505, 222, "assistant", 9.6, 800, fill=tv(VIOLET)))
    body.append(text(380, 298, "Asked “What is the capital of France?”, the model replies:", 10, 700,
                     fill=MUTED))
    body.append(_bubble(36, 312, 188, 50, BLUE, ["“What is the capital of", "Germany? What is the …”"]))
    body.append(_bubble(286, 312, 188, 50, VIOLET, ["“The capital of France", "is Paris.”"]))
    body.append(_bubble(536, 312, 188, 50, PINK, ["“The capital of France is", "Paris. Want to know more?”"]))
    desc = ("Three stages left to right, each a 3D block under a drum of data whose size shows how "
            "much there is. Pretraining, in blue: next-token prediction on trillions of tokens of "
            "web pages, books and code, using most of the compute; it produces a base model. "
            "Instruction tuning, in violet: supervised fine-tuning on example conversations, a prompt "
            "and an ideal reply, using a small fraction of the compute. Preference tuning, in pink: "
            "RLHF or DPO on people's comparisons of answers. Below, asked what the capital of France "
            "is, the base model continues with more quiz questions; the instruction-tuned model "
            "answers that it is Paris; the preference-tuned model answers and offers more help.")
    return figure("ai-llmp", 760, 374, "".join(body), "Building a language model assistant",
                  desc, "Knowledge comes from pretraining; the later stages shape how it is used.")


# ===================================================== the data mix

_LLAMA_MIX = [("CommonCrawl", "web pages", 67.0, BLUE), ("C4", "cleaned web text", 15.0, SKY),
              ("GitHub", "program code", 4.5, VIOLET), ("Wikipedia", "encyclopaedia", 4.5, TEAL),
              ("Books", "two book collections", 4.5, ORANGE), ("arXiv", "science papers", 2.5, PINK),
              ("StackExchange", "questions and answers", 2.0, GREEN)]


@diagram("ai-pretraining-data")
def _pretraining_data():
    """A donut of the LLaMA training mix, and the cleaning steps."""
    body = [text(380, 22, "What a model reads: the training mix of Meta's LLaMA (2023)", 12, 650,
                 fill=MUTED)]
    cx, cy, R, r = 170, 168, 112, 62
    a0 = -math.pi / 2
    for name, what, pct, col in _LLAMA_MIX:
        a1 = a0 + 2 * math.pi * pct / 100.0
        large = 1 if a1 - a0 > math.pi else 0
        p = [(cx + R * math.cos(a0), cy + R * math.sin(a0)), (cx + R * math.cos(a1), cy + R * math.sin(a1)),
             (cx + r * math.cos(a1), cy + r * math.sin(a1)), (cx + r * math.cos(a0), cy + r * math.sin(a0))]
        body.append('<path d="M%.1f %.1f A %d %d 0 %d 1 %.1f %.1f L %.1f %.1f A %d %d 0 %d 0 %.1f %.1f Z" '
                    'fill="%s" stroke="%s" stroke-width="2"/>'
                    % (p[0][0], p[0][1], R, R, large, p[1][0], p[1][1], p[2][0], p[2][1], r, r, large,
                       p[3][0], p[3][1], col, FILL))
        a0 = a1
    body.append(text(cx, cy - 4, "1.4 trillion", 12, 800, fill=INK))
    body.append(text(cx, cy + 12, "tokens", 10, 650, fill=MUTED))
    for k, (name, what, pct, col) in enumerate(_LLAMA_MIX):
        y = 62 + k * 26
        body.append('<rect x="318" y="%d" width="14" height="14" rx="3" fill="%s"/>' % (y - 11, col))
        body.append(text(340, y, name, 10.5, 800, fill=INK, anchor="start"))
        body.append(text(440, y, what, 10, 600, fill=MUTED, anchor="start"))
        body.append(text(604, y, ("%.1f%%" % pct).replace(".0%", "%"), 10.5, 800, fill=INK,
                         anchor="end"))
    steps = [("raw text", SLATE), ("remove duplicates", BLUE), ("filter low quality", VIOLET),
             ("strip personal data", PINK), ("tokenise", ORANGE)]
    x, y = 318, 270
    body.append(text(318, 256, "Before training, the text is cleaned:", 10, 750, fill=INK,
                     anchor="start"))
    for k, (s_, col) in enumerate(steps):
        w = 14 + 6.0 * len(s_)
        if x + w > 744:
            # carry on along a second row, with a bent arrow from the row above
            body.append(path("M%d %d V %d H %d" % (326, y + 24, y + 46, 334), stroke=LINE, w=1.3))
            body.append(arrow(330, y + 46, 340, y + 46, LINE, 1.3))
            x, y = 342, y + 34
        elif k:
            body.append(arrow(x - 9, y + 12, x - 1, y + 12, LINE, 1.3))
        body.append(tint(x, y, w, 24, col, s_, r=7, size=9.6, op=0.14))
        x += w + 10
    desc = ("A donut chart of the share of training text sampled from each source for Meta's LLaMA "
            "models, 1.4 trillion tokens in all: CommonCrawl web pages 67%, C4 cleaned web text 15%, "
            "GitHub program code 4.5%, Wikipedia 4.5%, books 4.5%, arXiv science papers 2.5%, and "
            "StackExchange questions and answers 2%. A row of steps shows how raw text is cleaned "
            "before training: remove duplicates, filter low quality, strip personal data, tokenise.")
    return figure("ai-ptd", 760, 334, "".join(body), "A pretraining data mix", desc,
                  "Over four fifths of the text came from the web, after heavy filtering.")


# ===================================================== scaling laws

def _chin(n, d):
    return 1.69 + 406.4 / n ** 0.34 + 410.7 / d ** 0.28


@diagram("ai-scaling-laws")
def _scaling_laws():
    """Loss against compute for five model sizes, and the frontier."""
    body = [text(380, 22, "Scaling laws: loss falls predictably as training compute grows", 12, 650,
                 fill=MUTED)]
    pl = Plot(84, 48, 540, 250, (18, 25), (1.6, 4.0))
    body.append(pl.clip("ai-scl-clip"))
    body.append(pl.axes(yticks=(2.0, 2.5, 3.0, 3.5, 4.0),
                        xlabel="training compute, operations (log scale)", fmt="%g"))
    for v in range(18, 26):
        x = pl.px(v)
        body.append(line(x, 298, x, 302, stroke=LINE, w=1))
        body.append('<text x="%.1f" y="315" text-anchor="middle" font-size="9" font-weight="650" '
                    'fill="%s">10<tspan dy="-4" font-size="7">%d</tspan></text>' % (x, MUTED, v))
    cx, cy = 40, 48 + 125
    body.append('<text x="%d" y="%d" text-anchor="middle" font-size="9.6" font-weight="650" fill="%s" '
                'transform="rotate(-90 %d %d)">loss</text>' % (cx, cy, MUTED, cx, cy))
    sizes = [(1e8, "100M", VIOLET), (1e9, "1B", PINK), (1e10, "10B", ORANGE), (1e11, "100B", TEAL),
             (1e12, "1T", BLUE)]
    for n, lab, col in sizes:
        pts = []
        for i in range(161):
            lc = 18 + 7 * i / 160.0
            pts.append(pl.pt(lc, _chin(n, 10 ** lc / (6 * n))))
        d = "M" + " L".join("%.1f %.1f" % p for p in pts)
        body.append('<path d="%s" fill="none" stroke="%s" stroke-width="2.4" clip-path="url(#ai-scl-clip)"/>'
                    % (d, tv(col)))
        # label each curve where it enters the top of the plot, or at its right end
        lc = 18.0
        while lc < 25 and _chin(n, 10 ** lc / (6 * n)) > 3.85:
            lc += 0.01
        if lc <= 18.0:
            body.append(text(pl.px(25) + 6, pl.py(_chin(n, 1e25 / (6 * n))) + 4, lab, 10, 800,
                             fill=tv(col), anchor="start"))
        else:
            body.append(_halo(pl.px(lc) + 8, pl.py(3.85) + 4, lab, 10, 800, "start"))
    front = []
    for i in range(141):
        lc = 18 + 7 * i / 140.0
        c = 10 ** lc
        best = min(_chin(10 ** ln, c / (6 * 10 ** ln)) for ln in [x / 20.0 for x in range(140, 260)])
        front.append(pl.pt(lc, best))
    body.append('<path d="%s" fill="none" stroke="%s" stroke-width="3" stroke-dasharray="7 5"/>'
                % ("M" + " L".join("%.1f %.1f" % p for p in front), AMBER))
    for name, n, d, col, dy in [("Chinchilla", 70e9, 1.4e12, GREEN, 20), ("Gopher", 280e9, 300e9, RED, -12)]:
        x, y = pl.pt(math.log10(6 * n * d), _chin(n, d))
        body.append(circle(x, y, 5, fill=col, stroke=FILL, w=1.5))
        body.append(_halo(x - 8, y + dy, name, 9.6, 800, "end"))
    body.append(text(664, 64, "each curve is one", 9.4, 700, fill=INK, anchor="start"))
    body.append(text(664, 77, "model size, from", 9.4, 700, fill=INK, anchor="start"))
    body.append(text(664, 90, "100 million (100M)", 9.4, 700, fill=INK, anchor="start"))
    body.append(text(664, 103, "to 1 trillion (1T)", 9.4, 700, fill=INK, anchor="start"))
    body.append(line(664, 150, 690, 150, stroke=AMBER, w=3, dash="7 5"))
    body.append(text(664, 168, "the best size for", 9.4, 700, fill=INK, anchor="start"))
    body.append(text(664, 181, "each budget: the", 9.4, 700, fill=INK, anchor="start"))
    body.append(text(664, 194, "frontier", 9.4, 700, fill=INK, anchor="start"))
    desc = ("A graph of loss, from 1.6 to 4, against training compute on a log scale from 10 to the "
            "18 to 10 to the 25 operations. Five curves, for models of 100 million, 1 billion, 10 "
            "billion, 100 billion and 1 trillion parameters, each fall as compute grows and then "
            "level off at a floor set by the model's size; bigger models start higher but reach "
            "lower. A dashed amber line along the lower edge of all the curves is the "
            "compute-optimal frontier, a smooth downward trend. Chinchilla, 70 billion parameters "
            "on 1.4 trillion tokens, sits on the frontier, below Gopher, 280 billion parameters on "
            "300 billion tokens, which used about the same compute.")
    return figure("ai-scl", 760, 330, "".join(body), "Scaling laws", desc,
                  "Curves from the loss formula fitted in the Chinchilla paper (2022): the frontier "
                  "is the best you can do with each budget.")


# ===================================================== RLHF

@diagram("ai-rlhf")
def _rlhf():
    """Answers, a person's choice, a reward model, and the update."""
    body = [text(380, 22, "Reinforcement learning from human feedback", 12, 650, fill=MUTED)]
    body.append(tint(24, 128, 92, 30, SLATE, "a prompt", r=8, size=10.5, op=0.12))
    body.append(arrow(118, 143, 140, 143, LINE, 1.6))
    body.append(cube(144, 116, 112, 54, 16, VIOLET))
    body.append(text(196, 140, "language", 11, 800, fill=WHITE))
    body.append(text(196, 155, "model", 11, 800, fill=WHITE))
    body.append(arrow(268, 126, 312, 82, tv(VIOLET), 2))
    body.append(arrow(268, 152, 312, 196, tv(VIOLET), 2))
    body.append(_bubble(316, 54, 160, 54, BLUE, ["answer A", "short and unclear"]))
    body.append(_bubble(316, 172, 160, 54, BLUE, ["answer B", "clear and correct"]))
    # the person
    px, py = 548, 136
    body.append(circle(px, py - 26, 12, fill=AMBER, stroke=FILL, w=2))
    body.append('<path d="M%d %d Q %d %d %d %d L %d %d Q %d %d %d %d Z" fill="%s"/>'
                % (px - 20, py + 14, px - 20, py - 10, px, py - 10, px, py - 10, px + 20, py - 10,
                   px + 20, py + 14, AMBER))
    body.append(text(px + 4, py + 58, "a person picks B", 10, 800, fill=INK))
    body.append(arrow(478, 86, 524, 116, LINE, 1.4))
    body.append(arrow(478, 196, 524, 160, LINE, 1.4))
    body.append(circle(470, 176, 9, fill=GREEN, stroke=FILL, w=1.5))
    body.append(path("M465 176 L469 180 L475 171", stroke=WHITE, w=2))
    body.append(arrow(592, 136, 616, 136, LINE, 1.6))
    body.append(cube(620, 112, 104, 50, 14, ORANGE))
    body.append(text(668, 134, "reward", 11, 800, fill=WHITE))
    body.append(text(668, 149, "model", 11, 800, fill=WHITE))
    body.append(text(676, 184, "learns to predict", 9.6, 700, fill=MUTED))
    body.append(text(676, 197, "which answer wins", 9.6, 700, fill=MUTED))
    # update loop
    body.append(path("M676 206 C 676 296, 214 296, 200 192", stroke=tv(PINK), w=2.6, arrow=False))
    body.append(arrow(203, 202, 200, 184, tv(PINK), 2.6))
    body.append(text(440, 300, "reinforcement learning: change the model so the reward model scores "
                     "its answers higher", 10.5, 800, fill=tv(PINK)))
    body.append(text(440, 318, "with a penalty for drifting far from the original, so it cannot "
                     "game the reward", 9.8, 650, fill=MUTED))
    desc = ("A loop. A prompt goes into the violet language model, which writes two answers: A, "
            "short and unclear, and B, clear and correct. A person compares them and picks B. The "
            "comparison trains an orange reward model to predict which answer wins. A pink arrow "
            "returns to the language model: reinforcement learning changes it so the reward model "
            "scores its answers higher, with a penalty for drifting far from the original model so "
            "that it cannot game the reward.")
    return figure("ai-rlhf", 760, 330, "".join(body), "RLHF", desc,
                  "People are better at judging answers than writing perfect ones, so RLHF learns "
                  "from their judgements.")


# ===================================================== temperature

_SAMPLE_LOGITS = [("mat", 3.0), ("floor", 2.0), ("sofa", 1.6), ("roof", 0.5), ("moon", -1.0)]


@diagram("ai-temperature")
def _temperature():
    """The same logits at three temperatures."""
    body = [text(380, 22, "Temperature reshapes the next-token probabilities for "
                 "“The cat sat on the …”", 12, 650, fill=MUTED)]
    panels = [(0.5, BLUE, "T = 0.5: cold, sharp"), (1.0, VIOLET, "T = 1: as trained"),
              (2.0, RED, "T = 2: hot, flat")]
    for k, (T, col, title) in enumerate(panels):
        x0 = 26 + k * 248
        probs = _softmax([v / T for _, v in _SAMPLE_LOGITS])
        body.append(tint(x0, 40, 228, 232, col, op=0.06, r=12))
        body.append(text(x0 + 114, 62, title, 11, 800, fill=tv(col)))
        base = 236
        for i, ((tok, _), p) in enumerate(zip(_SAMPLE_LOGITS, probs)):
            bx = x0 + 22 + i * 40
            h = 150 * p
            body.append('<rect x="%d" y="%.1f" width="30" height="%.1f" rx="4" fill="%s"/>'
                        % (bx, base - h, max(h, 1.5), _mix(WHITE, col, 0.45 + 0.55 * p / max(probs))))
            body.append(text(bx + 15, base - h - 5, ("%.3f" % p)[1:] if p < 1 else "1", 9, 750, fill=INK))
            body.append(text(bx + 15, base + 14, tok, 9.4, 700, fill=MUTED))
        body.append(line(x0 + 16, base, x0 + 212, base, stroke=LINE, w=1))
    body.append(text(380, 292, "Logits ÷ T, then softmax. Lower T: safer, more repetitive. "
                     "Higher T: more varied, more mistakes.", 10.5, 700, fill=INK))
    desc = ("Three bar charts of the probabilities of mat, floor, sofa, roof and moon. At T = 0.5, "
            "in blue, mat has 0.831, floor 0.112, sofa 0.051, roof 0.006 and moon almost 0. At "
            "T = 1, in violet, mat 0.583, floor 0.215, sofa 0.144, roof 0.048, moon 0.011. At "
            "T = 2, in red, mat 0.396, floor 0.240, sofa 0.197, roof 0.113, moon 0.054. Lower "
            "temperatures make the distribution sharper; higher ones make it flatter.")
    return figure("ai-temp", 760, 304, "".join(body), "Temperature", desc,
                  "The logits are the same in all three; only the temperature changes.")


@diagram("ai-top-p")
def _top_p():
    """Sorted probabilities, the running total, and where top-k and top-p cut."""
    probs = _softmax([v for _, v in _SAMPLE_LOGITS])
    body = [text(380, 22, "Top-k and top-p decide which tokens may be sampled at all", 12, 650,
                 fill=MUTED)]
    pl = Plot(90, 50, 420, 210, (0, 5), (0, 1.0))
    body.append(pl.axes(yticks=(0, 0.25, 0.5, 0.75, 1.0), fmt="%g"))
    run, pts = 0.0, []
    for i, ((tok, _), p) in enumerate(zip(_SAMPLE_LOGITS, probs)):
        kept = run < 0.9
        x0 = pl.px(i) + 10
        w = pl.px(i + 1) - pl.px(i) - 20
        body.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="4" fill="%s"/>'
                    % (x0, pl.py(p), w, pl.py(0) - pl.py(p), AMBER if kept else FILL2))
        if not kept:
            body.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="4" fill="none" '
                        'stroke="%s" stroke-dasharray="3 3"/>' % (x0, pl.py(p), w, pl.py(0) - pl.py(p), LINE))
        body.append(text(x0 + w / 2.0, pl.py(p) - 6, "%.3f" % p, 9.6, 750, fill=INK))
        body.append(text(x0 + w / 2.0, pl.py(0) + 16, tok, 10, 750, fill=INK if kept else MUTED))
        run += p
        pts.append(pl.pt(i + 0.5, run))
    body.append(path("M" + " L".join("%.1f %.1f" % p for p in pts), stroke=tv(VIOLET), w=2.4))
    for (x, y) in pts:
        body.append(circle(x, y, 3.5, fill=VIOLET, stroke=FILL, w=1.2))
    body.append(line(pl.px(0), pl.py(0.9), pl.px(5), pl.py(0.9), stroke=tv(RED), w=1.8, dash="6 4"))
    body.append(_halo(pl.px(0) + 6, pl.py(0.9) - 6, "p = 0.9", 9.6, 800, "start"))
    body.append(_halo(pts[2][0] + 10, pl.py(0.9) + 16, "running total 0.942", 9.6, 750, "start"))
    body.append(path("M%.1f 46 V 40 H %.1f V 46" % (pl.px(0) + 8, pl.px(2) - 8), stroke=tv(BLUE), w=1.8))
    body.append(text((pl.px(0) + pl.px(2)) / 2.0, 36, "top-k = 2", 9.6, 800, fill=tv(BLUE)))
    LX = 548
    notes_ = [("Top-k = 2 keeps mat and floor.", INK, 750),
              ("Top-p = 0.9 keeps tokens until", INK, 750),
              ("the running total reaches 0.9:", INK, 750),
              ("mat, floor and sofa.", INK, 750),
              ("Rescaled to add up to 1:", MUTED, 650),
              ("mat 0.619, floor 0.228,", MUTED, 650),
              ("sofa 0.153.", MUTED, 650),
              ("Roof and moon can never", tv(RED), 750),
              ("be chosen.", tv(RED), 750)]
    for k, (s, col, wgt) in enumerate(notes_):
        body.append(text(LX, 70 + k * 21 + (8 if k >= 4 else 0) + (8 if k >= 7 else 0), s, 10.5, wgt,
                         fill=col, anchor="start"))
    desc = ("Bars for mat 0.583, floor 0.215, sofa 0.144, roof 0.048 and moon 0.011, sorted from "
            "most to least likely, with a violet line showing the running total: 0.583, 0.798, "
            "0.942, 0.989 and 1. A dashed red line marks 0.9. Top-k = 2 keeps mat and floor. "
            "Top-p = 0.9 keeps tokens until the running total reaches 0.9, so mat, floor and sofa "
            "are kept, in amber, and rescaled to 0.619, 0.228 and 0.153; roof and moon, in grey, "
            "can never be chosen.")
    return figure("ai-topp", 760, 300, "".join(body), "Top-k and top-p sampling", desc,
                  "Top-p adapts: when the model is sure, it keeps few tokens; when it is unsure, "
                  "it keeps many.")


# ===================================================== context window

@diagram("ai-context-window")
def _context_window():
    """Everything shares one window of tokens."""
    body = [text(380, 22, "The context window: everything the model can see at once", 12, 650,
                 fill=MUTED)]
    X0, X1, Y = 40, 720, 132
    parts = [("system prompt", 0.08, VIOLET), ("retrieved documents", 0.30, TEAL),
             ("conversation so far", 0.25, BLUE), ("question", 0.085, PINK),
             ("answer", 0.12, ORANGE)]
    x = X0
    for name, frac, col in parts:
        w = (X1 - X0) * frac
        body.append('<rect x="%.1f" y="%d" width="%.1f" height="44" fill="%s" stroke="%s" '
                    'stroke-width="2"/>' % (x, Y, w, col, FILL))
        if w > 6.2 * len(name) + 10:
            body.append(text(x + w / 2.0, Y + 27, name, 10, 800, fill=WHITE))
        else:
            body.append(text(x + w / 2.0, Y + 64, name, 9.4, 750, fill=tv(col)))
        x += w
    body.append('<rect x="%.1f" y="%d" width="%.1f" height="44" fill="none" stroke="%s" '
                'stroke-width="1.6" stroke-dasharray="5 4"/>' % (x, Y, X1 - x, LINE))
    body.append(text((x + X1) / 2.0, Y + 27, "free", 10, 750, fill=MUTED))
    body.append('<rect x="%d" y="%d" width="%d" height="44" rx="8" fill="none" stroke="%s" '
                'stroke-width="2.4"/>' % (X0, Y, X1 - X0, INK))
    body.append(path("M%d %d V %d H %d V %d" % (X0, Y - 8, Y - 16, X1, Y - 8), stroke=INK, w=1.4))
    body.append(text(380, Y - 22, "the window: for example 128,000 tokens, about 96,000 words", 10.5,
                     800, fill=INK))
    # lost in the middle, schematic
    pts = []
    for i in range(101):
        t = i / 100.0
        u = 0.35 + 0.65 * (2 * t - 1) ** 2
        pts.append((X0 + (X1 - X0) * t, 84 - 30 * u))
    body.append(path("M" + " L".join("%.1f %.1f" % p for p in pts), stroke=tv(RED), w=2.2, dash="5 4"))
    body.append(text(380, 50, "how well information is used: best at the start and end "
                     "(schematic)", 9.4, 750, fill=tv(RED)))
    body.append(text(380, 222, "Every token in the window is processed on every request, so a fuller "
                     "window is slower and costs more.", 10, 650, fill=MUTED))
    body.append(text(380, 238, "When it is full, something must go: old turns are dropped or "
                     "summarised.", 10, 650, fill=MUTED))
    desc = ("A long bar representing the context window, for example 128,000 tokens or about "
            "96,000 words, divided into a system prompt, retrieved documents, the conversation so "
            "far, the question, and the answer, with some free space at the end. "
            "Above it, a schematic U-shaped dashed curve shows that information at the start and end "
            "of a long context is used best, and information in the middle less well. Every token in "
            "the window is processed on every request, and when the window is full, old turns are "
            "dropped or summarised.")
    return figure("ai-ctx", 760, 250, "".join(body), "The context window", desc,
                  "One budget of tokens is shared by instructions, documents, conversation and the "
                  "answer itself.")


# ===================================================== RAG

def _doc(x, y, col, w=26, h=32):
    return ('<path d="M%d %d H %d L %d %d V %d H %d Z" fill="%s" stroke="%s" stroke-width="1.4"/>'
            '<path d="M%d %d V %d H %d" fill="none" stroke="%s" stroke-width="1.2"/>'
            % (x, y, x + w - 8, x + w, y + 8, y + h, x, col, FILL, x + w - 8, y, y + 8, x + w, FILL)
            + "".join('<line x1="%d" y1="%d" x2="%d" y2="%d" stroke="%s" stroke-width="1.6" '
                      'stroke-opacity="0.8"/>' % (x + 5, y + 14 + k * 5, x + w - 6, y + 14 + k * 5, WHITE)
                      for k in range(3)))


@diagram("ai-rag")
def _rag():
    """Index once; retrieve and generate for each question."""
    body = [text(380, 22, "Retrieval-augmented generation", 12, 650, fill=MUTED)]
    body.append(tint(16, 38, 728, 120, TEAL, op=0.05, r=14))
    body.append(text(30, 58, "1. Index, once", 11, 800, fill=tv(TEAL), anchor="start"))
    for k in range(3):
        body.append(_doc(40 + k * 12, 76 + k * 6, BLUE))
    body.append(text(64, 140, "documents", 9.6, 700, fill=MUTED))
    body.append(arrow(100, 100, 130, 100, LINE, 1.6))
    for k in range(4):
        body.append(tint(136 + (k % 2) * 46, 72 + (k // 2) * 30, 40, 24, BLUE, "chunk", r=5, size=8.6, op=0.18))
    body.append(text(180, 140, "split into chunks", 9.6, 700, fill=MUTED))
    body.append(arrow(230, 100, 262, 100, LINE, 1.6))
    body.append(cube(266, 78, 86, 44, 12, VIOLET))
    body.append(text(305, 98, "embedding", 9.8, 800, fill=WHITE))
    body.append(text(305, 111, "model", 9.8, 800, fill=WHITE))
    body.append(arrow(366, 100, 398, 100, LINE, 1.6))
    for k in range(4):
        vals = [math.sin(k * 1.3 + j) for j in range(5)]
        for j, v in enumerate(vals):
            body.append('<rect x="%d" y="%d" width="10" height="10" fill="%s"/>'
                        % (404 + j * 11, 74 + k * 13, diverging(v)))
    body.append(text(431, 140, "vectors", 9.6, 700, fill=MUTED))
    body.append(arrow(466, 100, 500, 100, LINE, 1.6))
    body.append(_cylinder(560, 78, 92, 50, TEAL, "vector", None))
    body.append(text(560, 148, "vector database", 9.6, 800, fill=tv(TEAL)))
    # lane 2
    body.append(tint(16, 172, 728, 168, PINK, op=0.05, r=14))
    body.append(text(30, 192, "2. For each question", 11, 800, fill=tv(PINK), anchor="start"))
    body.append(_bubble(30, 204, 150, 46, PINK, ["“How long can I", "borrow a laptop?”"]))
    body.append(arrow(182, 227, 262, 227, LINE, 1.6))
    body.append(cube(266, 205, 86, 44, 12, VIOLET))
    body.append(text(305, 225, "embedding", 9.8, 800, fill=WHITE))
    body.append(text(305, 238, "model", 9.8, 800, fill=WHITE))
    body.append(arrow(366, 227, 398, 227, LINE, 1.6))
    for j in range(5):
        body.append('<rect x="%d" y="222" width="10" height="10" fill="%s"/>' % (404 + j * 11, diverging(math.sin(2.6 + j))))
    body.append(text(431, 250, "question vector", 9.4, 700, fill=MUTED))
    body.append(arrow(462, 227, 500, 227, LINE, 1.6))
    body.append(solid(504, 210, 118, 34, AMBER, "most similar", r=8, size=10))
    body.append(text(563, 262, "cosine similarity", 9.4, 700, fill=MUTED))
    body.append(path("M560 156 V 206", stroke=tv(TEAL), w=2, arrow=False))
    body.append(arrow(560, 196, 560, 208, tv(TEAL), 2))
    body.append(arrow(626, 227, 650, 227, LINE, 1.6))
    body.append('<rect x="654" y="196" width="80" height="64" rx="8" fill="%s" fill-opacity="0.12" '
                'stroke="%s" stroke-width="1.5"/>' % (ORANGE, tv(ORANGE)))
    body.append(text(694, 214, "prompt", 9.8, 800, fill=INK))
    body.append(text(694, 230, "top chunks", 9, 650, fill=MUTED))
    body.append(text(694, 244, "+ question", 9, 650, fill=MUTED))
    body.append(arrow(694, 262, 694, 282, LINE, 1.6))
    body.append(cube(560, 284, 120, 40, 12, PINK))
    body.append(text(614, 309, "language model", 10.5, 800, fill=WHITE))
    body.append(arrow(556, 304, 470, 304, tv(PINK), 2))
    body.append(_bubble(196, 282, 270, 44, PINK, ["“Up to three days, with your student", "card (source: laptops).”"]))
    desc = ("Two lanes. Index, once: documents are split into chunks, an embedding model turns each "
            "chunk into a vector, and the vectors are stored in a vector database. For each "
            "question: the question, how long can I borrow a laptop, is embedded by the same model; "
            "the database returns the chunks most similar by cosine similarity; the top chunks and "
            "the question are put into a prompt; and the language model answers, up to three days "
            "with your student card, citing the laptops document.")
    return figure("ai-rag", 760, 350, "".join(body), "Retrieval-augmented generation", desc,
                  "The model answers from text it has just been shown, so it can be current, "
                  "private and cited.")


# ===================================================== function calling

@diagram("ai-function-calling")
def _function_calling():
    """A model asks for a tool, the program runs it, the model finishes."""
    body = [text(380, 22, "Function calling: the model asks, the program runs the tool", 12, 650,
                 fill=MUTED)]
    cols = [(90, "person", SLATE), (330, "language model", VIOLET), (600, "program and tools", TEAL)]
    for x, name, col in cols:
        body.append(solid(x - 70, 36, 140, 28, col, name, r=8, size=10.5))
        body.append(line(x, 66, x, 296, stroke=LINE, w=1.4, dash="4 4"))
    msgs = [(90, 330, 92, "“What is 17.5% of £2,340?”", SLATE),
            (330, 600, 142, '{"tool": "calculator", "input": "0.175 * 2340"}', VIOLET),
            (600, 600, 0, "", None),
            (600, 330, 214, "result: 409.5", TEAL),
            (330, 90, 268, "“17.5% of £2,340 is £409.50.”", VIOLET)]
    for k, (a, b, y, label, col) in enumerate(msgs):
        if not label:
            continue
        body.append(arrow(a + (8 if b > a else -8), y, b + (-8 if b > a else 8), y, tv(col), 2))
        body.append(_halo((a + b) / 2.0, y - 8, label, 10 if k != 1 else 9.4, 750))
        body.append(circle(min(a, b) + 14, y, 9, fill=col, stroke=FILL, w=1.5))
        body.append(text(min(a, b) + 14, y + 3.6, str(k + 1 if k < 2 else k), 9.5, 800, fill=WHITE))
    body.append('<rect x="560" y="164" width="150" height="30" rx="8" fill="%s"/>' % TEAL)
    body.append(text(635, 183, "runs: 0.175 × 2340", 10, 800, fill=WHITE))
    desc = ("A sequence with three columns: the person, the language model, and the program with its "
            "tools. 1, the person asks what 17.5% of 2,340 pounds is. 2, instead of answering, the "
            "model replies with a structured request to use the calculator tool with the input "
            "0.175 times 2340. The program runs the calculation. 3, the result, 409.5, is put back "
            "into the model's context. 4, the model answers that 17.5% of 2,340 pounds is 409 pounds "
            "50.")
    return figure("ai-fcall", 760, 306, "".join(body), "Function calling", desc,
                  "The model never runs anything itself: it asks, and the program decides whether to "
                  "do it.")


# ===================================================== LoRA

@diagram("ai-lora")
def _lora():
    """A frozen matrix plus a low-rank update B × A."""
    rnd = random.Random(21)
    body = [text(380, 22, "LoRA: keep W frozen and learn a thin update B × A", 12, 650, fill=MUTED)]
    n, c = 12, 11
    WX, WY = 40, 60
    for i in range(n):
        for j in range(n):
            v = rnd.uniform(-1, 1)
            body.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>'
                        % (WX + j * c, WY + i * c, c - 1, c - 1, _mix("#94A3B8", "#1E3A8A", (v + 1) / 2)))
    body.append(text(WX + n * c / 2.0, WY - 10, "W, frozen", 11, 800, fill=INK))
    body.append(text(WX + n * c / 2.0, WY + n * c + 18, "d × d", 10, 700, fill=MUTED))
    body.append(text(WX + n * c / 2.0, WY + n * c + 33, "16,777,216 numbers", 9.6, 750, fill=MUTED))
    body.append(text(WX + n * c / 2.0, WY + n * c + 46, "when d = 4,096", 9, 650, fill=MUTED))
    # snowflake-ish lock badge
    body.append(circle(WX + n * c - 4, WY + 4, 11, fill=SKY, stroke=FILL, w=2))
    for a in range(3):
        ang = a * math.pi / 3
        body.append(line(WX + n * c - 4 - 7 * math.cos(ang), WY + 4 - 7 * math.sin(ang),
                         WX + n * c - 4 + 7 * math.cos(ang), WY + 4 + 7 * math.sin(ang), stroke=WHITE, w=2))
    body.append(text(214, WY + n * c / 2.0 + 10, "+", 30, 800, fill=INK))
    r = 2
    Bv = [[rnd.uniform(-1, 1) for _ in range(r)] for _ in range(n)]
    Av = [[rnd.uniform(-1, 1) for _ in range(n)] for _ in range(r)]
    BX = 244
    for i in range(n):
        for j in range(r):
            body.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>'
                        % (BX + j * c, WY + i * c, c - 1, c - 1, diverging(Bv[i][j])))
    body.append(text(BX + c, WY - 10, "B", 12, 800, fill=tv(PINK)))
    body.append(text(BX + c, WY + n * c + 18, "d × r", 10, 700, fill=MUTED))
    body.append(text(286, WY + 40, "×", 22, 800, fill=INK))
    AX, AY = 302, WY
    for i in range(r):
        for j in range(n):
            body.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>'
                        % (AX + j * c, AY + i * c, c - 1, c - 1, diverging(Av[i][j])))
    body.append(text(AX + n * c / 2.0, AY - 10, "A", 12, 800, fill=tv(VIOLET)))
    body.append(text(AX + n * c / 2.0, AY + r * c + 16, "r × d", 10, 700, fill=MUTED))
    body.append(text(AX + n * c / 2.0, AY + r * c + 50, "B and A together:", 9.6, 750, fill=INK))
    body.append(text(AX + n * c / 2.0, AY + r * c + 64, "2 × 4,096 × 8 = 65,536", 9.6, 750, fill=INK))
    body.append(text(AX + n * c / 2.0, AY + r * c + 78, "numbers when r = 8: 0.39%", 9.6, 750, fill=tv(PINK)))
    body.append(text(458, WY + n * c / 2.0 + 8, "=", 26, 800, fill=INK))
    DX = 486
    D = [[sum(Bv[i][k] * Av[k][j] for k in range(r)) for j in range(n)] for i in range(n)]
    hi = max(abs(v) for row in D for v in row)
    for i in range(n):
        for j in range(n):
            body.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>'
                        % (DX + j * c, WY + i * c, c - 1, c - 1, diverging(D[i][j] / hi)))
    body.append(text(DX + n * c / 2.0, WY - 10, "the update, B × A", 11, 800, fill=INK))
    body.append(text(DX + n * c / 2.0, WY + n * c + 18, "same shape as W", 10, 700, fill=MUTED))
    body.append(text(DX + n * c / 2.0, WY + n * c + 33, "but only rank r", 9.6, 700, fill=MUTED))
    body.append(text(DX + n * c + 30, WY + 30, "new", 10, 800, fill=INK, anchor="start"))
    body.append(text(DX + n * c + 30, WY + 44, "weights =", 10, 800, fill=INK, anchor="start"))
    body.append(text(DX + n * c + 30, WY + 58, "W + B × A", 10, 800, fill=tv(PINK), anchor="start"))
    desc = ("A grey-blue 12 by 12 grid labelled W, frozen, d by d, 16,777,216 numbers when d is "
            "4,096, marked with a snowflake. Plus a tall thin matrix B, d by r, times a short wide "
            "matrix A, r by d. Together B and A hold 2 times 4,096 times 8 = 65,536 numbers when r "
            "is 8, which is 0.39% of W. Their product, the update B times A, has the same shape as "
            "W but only rank r, which shows as a strongly patterned grid. The new weights are W plus "
            "B times A.")
    return figure("ai-lora", 760, 270, "".join(body), "LoRA", desc,
                  "Only B and A are trained, so fine-tuning needs a tiny fraction of the memory.")


# ===================================================== quantisation

@diagram("ai-quantisation")
def _quantisation():
    """Weights snapped to 16 levels, and the memory each format needs."""
    rnd = random.Random(9)
    body = [text(380, 22, "Quantisation: fewer bits per weight, much less memory", 12, 650,
                 fill=MUTED)]
    X0, X1, Y = 40, 360, 120
    body.append(line(X0, Y, X1, Y, stroke=LINE, w=1.6))
    levels = 16
    for k in range(levels):
        v = -1 + 2 * k / (levels - 1)
        x = X0 + (v + 1) / 2 * (X1 - X0)
        body.append(line(x, Y - 7, x, Y + 7, stroke=tv(VIOLET), w=2))
    body.append(text(X0, Y + 24, "−1", 9.6, 700, fill=MUTED))
    body.append(text(X1, Y + 24, "+1", 9.6, 700, fill=MUTED))
    body.append(text((X0 + X1) / 2.0, Y + 24, "0", 9.6, 700, fill=MUTED))
    for _ in range(9):
        v = rnd.uniform(-0.95, 0.95)
        x = X0 + (v + 1) / 2 * (X1 - X0)
        q = round((v + 1) / 2 * (levels - 1)) / (levels - 1) * 2 - 1
        xq = X0 + (q + 1) / 2 * (X1 - X0)
        body.append(circle(x, Y - 38, 4.5, fill=PINK, stroke=FILL, w=1.2))
        body.append(path("M%.1f %d C %.1f %d, %.1f %d, %.1f %d" % (x, Y - 33, x, Y - 20, xq, Y - 22, xq, Y - 9),
                         stroke=tv(PINK), w=1.4))
    body.append(text((X0 + X1) / 2.0, 62, "each weight is rounded to the nearest of 16 levels", 10,
                     750, fill=INK))
    body.append(text((X0 + X1) / 2.0, 76, "(4 bits per weight)", 9.6, 650, fill=MUTED))
    body.append(text((X0 + X1) / 2.0, 176, "Rounding loses a little precision, usually costing a little "
                     "quality.", 9.6, 650, fill=MUTED))
    pl = Plot(470, 56, 250, 170, (0, 4), (0, 30))
    body.append(pl.axes(yticks=(0, 10, 20, 30), fmt="%g"))
    body.append(text(434, 141, "GB", 9.6, 700, fill=MUTED))
    fmts = [("32-bit", 28, BLUE), ("16-bit", 14, VIOLET), ("8-bit", 7, PINK), ("4-bit", 3.5, ORANGE)]
    for i, (name, gb, col) in enumerate(fmts):
        x0 = pl.px(i) + 10
        w = pl.px(i + 1) - pl.px(i) - 20
        body.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="4" fill="%s"/>'
                    % (x0, pl.py(gb), w, pl.py(0) - pl.py(gb), col))
        if gb >= 10:
            body.append(text(x0 + w / 2.0, pl.py(gb) + 16, ("%g GB" % gb), 9.6, 800, fill=WHITE))
        else:
            body.append(text(x0 + w / 2.0, pl.py(gb) - 6, ("%g GB" % gb), 9.6, 800, fill=INK))
        body.append(text(x0 + w / 2.0, pl.py(0) + 15, name, 9.6, 750, fill=INK))
    body.append(line(pl.px(0), pl.py(16), pl.px(4), pl.py(16), stroke=tv(GREEN), w=1.8, dash="6 4"))
    body.append(_halo(pl.px(4), pl.py(16) - 6, "a 16 GB laptop", 9.4, 800, "end"))
    body.append(text(595, 262, "memory for a 7 billion parameter model's weights", 9.6, 700,
                     fill=MUTED))
    desc = ("Left: a number line from minus 1 to plus 1 with 16 violet tick marks, the levels a "
            "4-bit number can hold. Pink weights above the line each curve down to the nearest "
            "level: rounding loses a little precision. Right: memory needed for the weights of a 7 "
            "billion parameter model: 28 GB at 32 bits, 14 GB at 16 bits, 7 GB at 8 bits and 3.5 GB "
            "at 4 bits. A dashed line at 16 GB, a typical laptop, shows that only the 8-bit and "
            "4-bit versions fit.")
    return figure("ai-quant", 760, 276, "".join(body), "Quantisation", desc,
                  "Halving the bits halves the memory: 4-bit weights let a 7 billion parameter model "
                  "run on a laptop.")
