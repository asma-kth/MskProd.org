"""AI course diagrams, Level 14: AI engineering and architecture.

The threshold trade-off uses the same simulated payments as the lesson's
Python, and the search, latency and cost figures use the lesson's numbers.
The system diagrams are illustrations of common designs.
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
from .diagrams_ai5 import _mix
from .diagrams_ai6 import _bubble, _cylinder


# ===================================================== the small box of ML code

@diagram("ai-ml-system-boxes")
def _ml_system_boxes():
    """Many large boxes around one tiny box of model code."""
    body = [text(380, 22, "A real machine learning system: the model code is the small box in the middle",
                 12, 650, fill=MUTED)]
    boxes = [(30, 44, 150, 96, BLUE, "data collection"), (190, 44, 120, 58, SKY, "configuration"),
             (320, 44, 150, 58, TEAL, "data verification"), (480, 44, 250, 96, VIOLET, "serving infrastructure"),
             (190, 112, 120, 112, INDIGO, "feature extraction"), (30, 150, 150, 74, ORANGE, "machine resources"),
             (480, 150, 250, 74, PINK, "monitoring"), (30, 234, 220, 54, GREEN, "analysis tools"),
             (260, 234, 210, 54, AMBER, "process management"), (480, 234, 250, 54, RED, "testing and debugging")]
    for x, y, w, h, col, lab in boxes:
        body.append(tint(x, y, w, h, col, lab, r=10, size=10.5, op=0.16))
    body.append('<rect x="320" y="112" width="150" height="112" rx="10" fill="none" stroke="%s" '
                'stroke-dasharray="4 4"/>' % LINE)
    body.append(solid(366, 150, 58, 36, PINK, "ML code", r=7, size=10))
    body.append(text(395, 212, "the model itself", 9, 700, fill=MUTED))
    desc = ("Ten large tinted boxes fill the picture: data collection, configuration, data verification, "
            "serving infrastructure, feature extraction, machine resource management, monitoring, "
            "analysis tools, process management, and testing and debugging. In the middle, a small "
            "pink box labelled ML code, the model itself, takes up only a tiny part of the space.")
    return figure("ai-mlbox", 760, 300, "".join(body), "The parts of a machine learning system", desc,
                  "After a well-known 2015 paper from Google: everything around the model is most of "
                  "the work.")


# ===================================================== the lifecycle ring

@diagram("ai-ml-lifecycle")
def _ml_lifecycle():
    """Seven stages in a loop, with monitoring feeding back into data."""
    body = [text(380, 22, "The machine learning lifecycle is a loop, not a line", 12, 650, fill=MUTED)]
    stages = [("frame the problem", SLATE), ("collect and label data", BLUE), ("prepare features", TEAL),
              ("train and tune", VIOLET), ("evaluate", INDIGO), ("deploy", ORANGE), ("monitor", PINK)]
    cx, cy, rx, ry = 380, 178, 260, 112
    pts = []
    for k, (name, col) in enumerate(stages):
        a = -math.pi / 2 + 2 * math.pi * k / len(stages)
        pts.append((cx + rx * math.cos(a), cy + ry * math.sin(a)))
    for k in range(len(stages)):
        (x1, y1), (x2, y2) = pts[k], pts[(k + 1) % len(stages)]
        mx, my = (x1 + x2) / 2.0, (y1 + y2) / 2.0
        ox, oy = (mx - cx) * 0.12, (my - cy) * 0.12
        d = "M%.1f %.1f Q %.1f %.1f %.1f %.1f" % (x1, y1, mx + ox, my + oy, x2, y2)
        col = tv(PINK) if k == len(stages) - 1 else AMBER
        body.append('<path d="%s" fill="none" stroke="%s" stroke-width="3" class="ai-flow" '
                    'stroke-dasharray="6 8"/>' % (d, col))
        # an arrowhead just before the next stage, pointing along the curve
        t = 0.78
        qx = (1 - t) ** 2 * x1 + 2 * (1 - t) * t * (mx + ox) + t * t * x2
        qy = (1 - t) ** 2 * y1 + 2 * (1 - t) * t * (my + oy) + t * t * y2
        dx = 2 * (1 - t) * ((mx + ox) - x1) + 2 * t * (x2 - (mx + ox))
        dy = 2 * (1 - t) * ((my + oy) - y1) + 2 * t * (y2 - (my + oy))
        n = math.hypot(dx, dy) or 1.0
        body.append(arrow(qx - 8 * dx / n, qy - 8 * dy / n, qx + 4 * dx / n, qy + 4 * dy / n, col, 2.4))
    for (x, y), (name, col) in zip(pts, stages):
        w = 14 + 6.6 * len(name)
        body.append(solid(x - w / 2.0, y - 16, w, 32, col, name, r=16, size=10.5))
    body.append(_halo((pts[-1][0] + pts[0][0]) / 2.0 - 30, (pts[-1][1] + pts[0][1]) / 2.0 - 14,
                      "drift found: back to data", 10, 800, "end"))
    body.append(text(cx, cy - 6, "every stage is", 11, 800, fill=INK))
    body.append(text(cx, cy + 10, "revisited, again and again", 11, 800, fill=INK))
    desc = ("Seven stages in an oval loop joined by amber arrows: frame the problem; collect and label "
            "data; prepare features; train and tune; evaluate; deploy; monitor. A pink arrow runs from "
            "monitor back to the start, labelled drift found: back to data. In the centre: every stage "
            "is revisited, again and again.")
    return figure("ai-mllc", 760, 316, "".join(body), "The machine learning lifecycle", desc,
                  "Monitoring is what turns a one-off model into a system that keeps working.")


# ===================================================== threshold trade-off

def _payments():
    rnd = random.Random(5)
    out = []
    for _ in range(10000):
        fraud = rnd.random() < 0.01
        out.append((rnd.gauss(0.7 if fraud else 0.3, 0.15), fraud))
    return out


@diagram("ai-threshold-tradeoff")
def _threshold_tradeoff():
    """Two score distributions, a threshold, and precision and recall at three settings."""
    pays = _payments()
    body = [text(380, 22, "Moving the threshold trades precision against recall", 12, 650, fill=MUTED)]
    pl = Plot(60, 46, 420, 190, (-0.1, 1.1), (0, 2.8))
    body.append(pl.axes(xticks=(0, 0.2, 0.4, 0.6, 0.8, 1.0), fmt="%g", xlabel="risk score"))

    def dens(x, m):
        return math.exp(-0.5 * ((x - m) / 0.15) ** 2) / (0.15 * math.sqrt(2 * math.pi))
    xs = [-0.1 + 1.2 * i / 200.0 for i in range(201)]
    for m, col, scale in [(0.3, BLUE, 0.99), (0.7, PINK, 0.2)]:
        d = "M%.1f %.1f " % pl.pt(-0.1, 0) + " ".join("L%.1f %.1f" % pl.pt(x, scale * dens(x, m)) for x in xs) \
            + " L%.1f %.1f Z" % pl.pt(1.1, 0)
        body.append('<path d="%s" fill="%s" fill-opacity="0.28" stroke="%s" stroke-width="2"/>'
                    % (d, col, tv(col)))
    body.append(_halo(pl.px(0.3), pl.py(2.75), "genuine payments", 10, 800))
    body.append(_halo(pl.px(0.78), pl.py(0.75), "fraud (drawn 20 times taller)", 9.6, 800))
    tx = pl.px(0.6)
    body.append(line(tx, pl.y - 4, tx, pl.y + pl.h, stroke=tv(RED), w=2.4, dash="6 4"))
    body.append(_halo(tx + 6, pl.py(1.7), "threshold 0.6:", 9.6, 800, "start"))
    body.append(_halo(tx + 6, pl.py(1.7) + 13, "flag everything to the right", 9.6, 800, "start"))
    LX = 510
    body.append(text(LX, 64, "threshold", 9.6, 800, fill=MUTED, anchor="start"))
    body.append(text(LX + 92, 64, "precision", 9.6, 800, fill=MUTED, anchor="start"))
    body.append(text(LX + 172, 64, "recall", 9.6, 800, fill=MUTED, anchor="start"))
    for k, t in enumerate((0.5, 0.6, 0.7)):
        tp = sum(1 for s, f in pays if s > t and f)
        fp = sum(1 for s, f in pays if s > t and not f)
        fn = sum(1 for s, f in pays if s <= t and f)
        y = 92 + k * 28
        body.append(text(LX + 20, y, "%.1f" % t, 11, 800, fill=INK, anchor="start"))
        body.append(text(LX + 100, y, "%.1f%%" % (100.0 * tp / (tp + fp)), 11, 800, fill=tv(BLUE), anchor="start"))
        body.append(text(LX + 172, y, "%.1f%%" % (100.0 * tp / (tp + fn)), 11, 800, fill=tv(PINK), anchor="start"))
    notes_ = [("Lower threshold: catch more fraud,", INK), ("but many more false alarms.", MUTED),
              ("Higher threshold: fewer false alarms,", INK), ("but more fraud missed.", MUTED),
              ("“Never flag” is 98.9% accurate", tv(RED)), ("and catches nothing.", tv(RED))]
    for k, (s_, col) in enumerate(notes_):
        body.append(text(LX, 196 + k * 17 + (k // 2) * 6, s_, 9.8, 750 if col != MUTED else 600, fill=col, anchor="start"))
    desc = ("Two bell-shaped distributions of risk scores: genuine payments, in blue, centred on 0.3, "
            "and fraud, in pink, centred on 0.7 and drawn 20 times taller than its real size because "
            "only 1% of payments are fraud. A dashed red threshold at 0.6 flags everything to its "
            "right. A table gives precision and recall on 10,000 simulated payments: threshold 0.5, "
            "precision 9.4%, recall 90.7%; threshold 0.6, 24.5% and 75.0%; threshold 0.7, 54.5% and "
            "50.9%. Lowering the threshold catches more fraud but raises many more false alarms; a "
            "rule that never flags anything is 98.9% accurate and catches nothing.")
    return figure("ai-thr", 760, 300, "".join(body), "The threshold trade-off", desc,
                  "The same simulated payments as the lesson's Python.")


# ===================================================== time split

@diagram("ai-time-split")
def _time_split():
    """A random split leaks the future; a time split does not."""
    body = [text(380, 22, "Splitting data that changes over time", 12, 650, fill=MUTED)]
    months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
    X0, W = 130, 50
    for k, m in enumerate(months):
        body.append(text(X0 + k * W + W / 2.0, 52, m, 9.6, 700, fill=MUTED))
    rnd = random.Random(3)
    body.append(text(120, 92, "random split", 10.5, 800, fill=INK, anchor="end"))
    for k in range(12):
        for j in range(4):
            test = rnd.random() < 0.25
            col = RED if test else BLUE
            body.append('<rect x="%d" y="%d" width="10" height="10" rx="2" fill="%s"/>'
                        % (X0 + k * W + 5 + j * 11, 82, col))
    body.append(text(X0 + 6 * W, 118, "test examples scattered through the year: the model has seen the future",
                     9.6, 750, fill=tv(RED)))
    body.append(text(120, 162, "time split", 10.5, 800, fill=INK, anchor="end"))
    for k in range(12):
        col = BLUE if k < 9 else (AMBER if k == 9 else GREEN)
        for j in range(4):
            body.append('<rect x="%d" y="%d" width="10" height="10" rx="2" fill="%s"/>'
                        % (X0 + k * W + 5 + j * 11, 152, col))
    for x0, x1, lab, col in [(0, 9, "train: January to September", BLUE), (9, 10, "validate", AMBER),
                             (10, 12, "test: the future", GREEN)]:
        body.append(path("M%d 172 V 178 H %d V 172" % (X0 + x0 * W + 4, X0 + x1 * W - 4), stroke=tv(col), w=1.6))
        body.append(text(X0 + (x0 + x1) * W / 2.0, 194, lab, 9.6, 800, fill=tv(col)))
    desc = ("Twelve months of examples in two rows. In a random split, red test examples are scattered "
            "through the whole year among blue training examples, so the model has seen the future. In "
            "a time split, January to September is training, October is validation, and November and "
            "December are the test, so the model is tested only on the future, as it will be in use.")
    return figure("ai-tsplit", 760, 208, "".join(body), "A time-based split", desc,
                  "Test on what comes after the training data, exactly as in real use.")


# ===================================================== grid against random search

def _score(lr_log, dropout):
    return 0.9 - 0.08 * (lr_log + 2.5) ** 2 - 0.01 * (dropout - 0.3) ** 2


@diagram("ai-hyperparameter-search")
def _hyperparameter_search():
    """Nine grid trials hit three learning rates; nine random trials hit nine."""
    body = [text(380, 22, "Nine trials each: a grid repeats values, random search spreads them out", 12,
                 650, fill=MUTED)]
    grid = [(lr, d) for lr in (-4, -3, -2) for d in (0.1, 0.3, 0.5)]
    rnd = random.Random(1)
    rand = [(rnd.uniform(-4, -2), rnd.uniform(0.1, 0.5)) for _ in range(9)]
    for p, (title, trials, col) in enumerate([("grid search", grid, BLUE), ("random search", rand, PINK)]):
        x0 = 60 + p * 370
        top = Plot(x0, 50, 280, 70, (-4.2, -1.8), (0.6, 0.92))
        body.append(text(x0 + 140, 44, title, 11, 800, fill=tv(col)))
        body.append(path(top.curve(lambda v: _score(v, 0.3), 80), stroke=tv(VIOLET), w=2.2))
        main = Plot(x0, 132, 280, 140, (-4.2, -1.8), (0.05, 0.55))
        body.append('<rect x="%d" y="132" width="280" height="140" rx="6" fill="%s" fill-opacity="0.05" '
                    'stroke="%s"/>' % (x0, col, LINE))
        best = max(trials, key=lambda t: _score(*t))
        for lr, d in trials:
            x, y = main.pt(lr, d)
            body.append(line(x, y, x, top.py(_score(lr, 0.3)), stroke=tv(col), w=0.8, dash="2 3"))
            body.append(circle(x, top.py(_score(lr, 0.3)), 3.5, fill=col, stroke=FILL, w=1))
            body.append(circle(x, y, 6 if (lr, d) == best else 4.5, fill=AMBER if (lr, d) == best else col,
                               stroke=FILL, w=1.5))
        body.append(text(x0 + 140, 290, "learning rate (matters a lot) →", 9.4, 700, fill=MUTED))
        body.append('<text x="%d" y="202" text-anchor="middle" font-size="9.4" font-weight="700" fill="%s" '
                    'transform="rotate(-90 %d 202)">dropout (barely matters)</text>' % (x0 - 14, MUTED, x0 - 14))
        distinct = len({round(t[0], 3) for t in trials})
        body.append(text(x0 + 140, 308, "%d different learning rates tried; best score %.3f"
                         % (distinct, _score(*best)), 10, 800, fill=INK))
    desc = ("Two panels, each with nine trials plotted by learning rate across and dropout up the side. "
            "Above each, a violet curve shows how the score depends on the learning rate, which matters "
            "a lot; dropout barely matters. The grid's nine trials sit in three columns, so they test "
            "only three learning rates, and the best scores 0.880. The random search's nine trials are "
            "spread out, testing nine learning rates, and the best, marked in amber, scores 0.900.")
    return figure("ai-hps", 760, 320, "".join(body), "Grid search against random search", desc,
                  "When few hyperparameters matter, random search explores those few far better.")


# ===================================================== parallelism

def _gpu(x, y, w, h, label):
    return ('<rect x="%d" y="%d" width="%d" height="%d" rx="10" fill="none" stroke="%s" stroke-width="1.6" '
            'stroke-dasharray="5 4"/>' % (x, y, w, h, LINE) + text(x + w / 2.0, y + h + 14, label, 9, 700, fill=MUTED))


@diagram("ai-parallelism")
def _parallelism():
    """Data, tensor and pipeline parallelism."""
    body = [text(380, 22, "Three ways to split training across GPUs", 12, 650, fill=MUTED)]
    layer_cols = [BLUE, VIOLET, PINK]
    # data parallel
    body.append(text(130, 50, "data parallelism", 11, 800, fill=tv(BLUE)))
    for g in range(3):
        x = 30 + g * 68
        body.append(_gpu(x, 64, 58, 132, "GPU %d" % (g + 1)))
        for k, col in enumerate(layer_cols):
            body.append('<rect x="%d" y="%d" width="42" height="26" rx="4" fill="%s"/>' % (x + 8, 76 + k * 36, col))
        body.append(tint(x + 6, 216, 46, 20, AMBER, "batch %d" % (g + 1), r=5, size=8.4, op=0.2))
    body.append(path("M40 246 H 220", stroke=tv(GREEN), w=2))
    body.append(text(130, 262, "average the gradients", 9.6, 800, fill=tv(GREEN)))
    body.append(text(130, 278, "full copy on every GPU", 9.4, 650, fill=MUTED))
    # tensor parallel
    body.append(text(380, 50, "tensor parallelism", 11, 800, fill=tv(VIOLET)))
    for g in range(2):
        x = 300 + g * 86
        body.append(_gpu(x, 64, 76, 132, "GPU %d" % (g + 1)))
        for k, col in enumerate(layer_cols):
            body.append('<rect x="%d" y="%d" width="60" height="26" rx="4" fill="%s"/>' % (x + 8, 76 + k * 36, col))
            body.append(text(x + 38, 76 + k * 36 + 17, "½ layer %d" % (k + 1), 9, 800, fill=WHITE))
    body.append(arrow(378, 168, 386, 168, LINE, 1.4))
    body.append(text(380, 262, "each layer's matrices split", 9.6, 800, fill=tv(VIOLET)))
    body.append(text(380, 278, "GPUs swap results every layer", 9.4, 650, fill=MUTED))
    # pipeline parallel
    body.append(text(630, 50, "pipeline parallelism", 11, 800, fill=tv(PINK)))
    for g in range(3):
        x = 536 + g * 68
        body.append(_gpu(x, 64, 58, 132, "GPU %d" % (g + 1)))
        body.append('<rect x="%d" y="%d" width="42" height="26" rx="4" fill="%s"/>' % (x + 8, 116, layer_cols[g]))
        body.append(text(x + 29, 133, "layer %d" % (g + 1), 8.4, 800, fill=WHITE))
        if g < 2:
            body.append(arrow(x + 52, 129, x + 74, 129, AMBER, 2))
    body.append(text(630, 262, "each GPU holds some layers", 9.6, 800, fill=tv(PINK)))
    body.append(text(630, 278, "activations passed along", 9.4, 650, fill=MUTED))
    desc = ("Three panels. Data parallelism: three GPUs each hold a full copy of a three-layer model and "
            "train on different batches; their gradients are averaged. Tensor parallelism: two GPUs each "
            "hold half of every layer's matrices and swap results at every layer. Pipeline parallelism: "
            "three GPUs each hold one layer, passing activations from one to the next.")
    return figure("ai-par", 760, 292, "".join(body), "Splitting training across GPUs", desc,
                  "Frontier models use all three at once across thousands of GPUs.")


# ===================================================== drift

@diagram("ai-drift")
def _drift():
    """An input distribution shifting, and accuracy decaying until retraining."""
    body = [text(380, 22, "Drift: the world moves on, and accuracy quietly falls", 12, 650, fill=MUTED)]
    pl = Plot(50, 50, 300, 180, (10, 70), (0, 0.06))
    body.append(pl.axes(xticks=(20, 30, 40, 50, 60), fmt="%g", xlabel="customer age"))
    xs = [10 + 60 * i / 150.0 for i in range(151)]
    for m, s, col, lab, lx in [(38, 10, BLUE, "at training", 50), (31, 9, PINK, "now", 22)]:
        d = "M%.1f %.1f " % pl.pt(10, 0) + " ".join(
            "L%.1f %.1f" % pl.pt(x, math.exp(-0.5 * ((x - m) / s) ** 2) / (s * math.sqrt(2 * math.pi))) for x in xs) \
            + " L%.1f %.1f Z" % pl.pt(70, 0)
        body.append('<path d="%s" fill="%s" fill-opacity="0.22" stroke="%s" stroke-width="2.2"/>' % (d, col, tv(col)))
        body.append(_halo(pl.px(lx), pl.py(0.05), lab, 10, 800))
    body.append(text(200, 286, "data drift: the inputs have shifted (PSI 0.5)", 10, 800, fill=tv(PINK)))
    p2 = Plot(440, 50, 290, 180, (0, 12), (0.70, 0.95))
    body.append(p2.axes(xticks=(0, 3, 6, 9, 12), yticks=(0.75, 0.85, 0.95), fmt="%g", xlabel="months after release"))
    acc = []
    for k in range(13):
        v = 0.92 - 0.012 * k - (0.03 if k >= 5 else 0) if k < 8 else 0.92 - 0.004 * (k - 8)
        acc.append((k, v))
    body.append(path("M" + " L".join("%.1f %.1f" % p2.pt(k, v) for k, v in acc[:8]), stroke=tv(BLUE), w=2.6))
    body.append(path("M" + " L".join("%.1f %.1f" % p2.pt(k, v) for k, v in acc[8:]), stroke=tv(GREEN), w=2.6))
    body.append(line(p2.px(0), p2.py(0.82), p2.px(12), p2.py(0.82), stroke=tv(RED), w=1.6, dash="6 4"))
    body.append(_halo(p2.px(0.3), p2.py(0.82) + 14, "alert level", 9.4, 800, "start"))
    body.append(line(p2.px(8), p2.y, p2.px(8), p2.y + p2.h, stroke=tv(GREEN), w=1.6, dash="3 3"))
    body.append(_halo(p2.px(8) + 4, p2.py(0.94), "retrained on fresh data", 9.4, 800, "start"))
    body.append(text(585, 286, "accuracy falls until the alert triggers retraining", 10, 800, fill=tv(BLUE)))
    desc = ("Left: the distribution of customer ages at training, centred on 38, and now, centred on 31: "
            "the inputs have drifted, with a PSI of about 0.5. Right: accuracy over twelve months after "
            "release, falling from 0.92, with a sudden drop at month 5, until it crosses a dashed red "
            "alert level and the model is retrained on fresh data at month 8, restoring accuracy. The "
            "accuracy curve is illustrative.")
    return figure("ai-drift", 760, 298, "".join(body), "Data drift and its effect", desc,
                  "Monitoring turns a silent decline into an alert, and an alert into a fix.")


# ===================================================== system architecture

@diagram("ai-system-architecture")
def _system_architecture():
    """The layers around the model in an AI application."""
    body = [text(380, 22, "The layers of an AI application: the model is one of seven", 12, 650,
                 fill=MUTED)]
    layers = [("interface", "app or website", SLATE), ("gateway", "who is asking? rate limits", BLUE),
              ("orchestration", "build the prompt, choose models and tools", VIOLET)]
    for k, (name, sub, col) in enumerate(layers):
        y = 44 + k * 58
        body.append(cube(150, y, 420, 40, 14, col))
        body.append(text(170, y + 25, name, 12, 800, fill=WHITE, anchor="start"))
        body.append(text(550, y + 25, sub, 9.8, 650, fill=WHITE, anchor="end"))
    body.append(cube(150, 222, 200, 48, 14, TEAL))
    body.append(text(250, 243, "retrieval", 12, 800, fill=WHITE))
    body.append(text(250, 259, "vector database", 9.4, 650, fill=WHITE))
    body.append(cube(370, 222, 200, 48, 14, PINK))
    body.append(text(470, 243, "model serving", 12, 800, fill=WHITE))
    body.append(text(470, 259, "GPUs or a provider's API", 9.4, 650, fill=WHITE))
    body.append(cube(150, 296, 420, 34, 12, INDIGO))
    body.append(text(360, 318, "observability: logs, cost, latency, errors, feedback", 10.5, 800, fill=WHITE))
    # guardrails band
    body.append('<rect x="606" y="44" width="58" height="286" rx="12" fill="%s" fill-opacity="0.16" '
                'stroke="%s" stroke-width="1.6"/>' % (ORANGE, tv(ORANGE)))
    body.append('<text x="635" y="187" text-anchor="middle" font-size="11" font-weight="800" fill="%s" '
                'transform="rotate(-90 635 187)">guardrails: check inputs and outputs</text>' % tv(ORANGE))
    body.append(arrow(110, 60, 110, 240, tv(BLUE), 2.2))
    body.append('<text x="96" y="150" text-anchor="middle" font-size="9.6" font-weight="750" fill="%s" '
                'transform="rotate(-90 96 150)">request</text>' % tv(BLUE))
    body.append(arrow(128, 240, 128, 60, tv(GREEN), 2.2))
    body.append('<text x="142" y="150" text-anchor="middle" font-size="9.6" font-weight="750" fill="%s" '
                'transform="rotate(90 142 150)">answer</text>' % tv(GREEN))
    desc = ("Stacked 3D layers. From the top: the interface, an app or website; the gateway, which checks "
            "who is asking and applies rate limits; orchestration, which builds the prompt and chooses "
            "models and tools; then side by side, retrieval from a vector database and model serving on "
            "GPUs or a provider's API; and at the bottom, observability: logs, cost, latency, errors and "
            "feedback. A tall orange band beside them is labelled guardrails: check inputs and outputs. "
            "Arrows show the request travelling down and the answer travelling back up.")
    return figure("ai-arch", 760, 344, "".join(body), "The layers of an AI application", desc,
                  "Most of the engineering, and most of the safety, lives outside the model.")


# ===================================================== latency budget

@diagram("ai-latency-budget")
def _latency_budget():
    """Each step before the first token, then streaming."""
    body = [text(380, 22, "A latency budget: where the time goes before and after the first word", 12, 650,
                 fill=MUTED)]
    pl = Plot(210, 50, 520, 150, (0, 6000), (0, 6))
    for v in range(0, 6001, 1000):
        x = pl.px(v)
        body.append(line(x, 46, x, 214, stroke=LINE, w=0.6, dash="2 4"))
        body.append(text(x, 230, "%g s" % (v / 1000.0), 9.4, 700, fill=MUTED))
    steps = [("network, both ways", 80, SLATE), ("input safety check", 60, ORANGE),
             ("embed and retrieve", 150, TEAL), ("read the prompt", 350, VIOLET)]
    t = 0
    for k, (name, ms, col) in enumerate(steps):
        y = 56 + k * 26
        body.append(text(200, y + 14, name, 10, 750, fill=INK, anchor="end"))
        body.append('<rect x="%.1f" y="%d" width="%.1f" height="18" rx="4" fill="%s"/>'
                    % (pl.px(t), y, max(3, pl.px(t + ms) - pl.px(t)), col))
        body.append(text(pl.px(t + ms) + 6, y + 13, "%d ms" % ms, 9, 750, fill=INK, anchor="start"))
        t += ms
    y = 56 + 4 * 26
    body.append(text(200, y + 14, "generate 300 tokens", 10, 750, fill=INK, anchor="end"))
    body.append('<rect x="%.1f" y="%d" width="%.1f" height="18" rx="4" fill="%s"/>'
                % (pl.px(t), y, pl.px(t + 5000) - pl.px(t), PINK))
    for k in range(25):
        x = pl.px(t + 200 * k)
        body.append('<rect x="%.1f" y="%d" width="2" height="18" fill="%s" fill-opacity="0.45"/>' % (x, y, WHITE))
    body.append('<text x="%.1f" y="%d" text-anchor="middle" font-size="9" font-weight="800" fill="%s" stroke="%s" '
                'stroke-width="3" paint-order="stroke">streamed: tokens appear one by one at 60 per second</text>'
                % (pl.px(t + 2500), y + 13, WHITE, PINK))
    body.append(line(pl.px(t), 46, pl.px(t), 214, stroke=tv(GREEN), w=2.2))
    body.append(_halo(pl.px(t) + 6, 196, "first word after 0.64 s", 10, 800, "start"))
    body.append(text(470, 252, "Without streaming, nothing would appear for 5.6 seconds.", 10, 750, fill=tv(RED)))
    desc = ("A timeline from 0 to 6 seconds. Before the first token: network 80 milliseconds, input "
            "safety check 60, embedding and retrieval 150, and reading the prompt 350, so the first word "
            "appears after 0.64 seconds, marked by a green line. Then generating 300 tokens at 60 per "
            "second takes another 5 seconds, streamed so tokens appear one by one. Without streaming, "
            "nothing would appear for 5.6 seconds.")
    return figure("ai-lat", 760, 264, "".join(body), "A latency budget", desc,
                  "The same numbers as the lesson's Python.")


# ===================================================== model cascade

@diagram("ai-model-cascade")
def _model_cascade():
    """A router sends easy questions to a small model and hard ones to a large one."""
    body = [text(380, 22, "A model cascade: pay for the big model only when it is needed", 12, 650,
                 fill=MUTED)]
    body.append(_bubble(24, 110, 150, 46, SLATE, ["300,000 questions", "a month"]))
    body.append(arrow(176, 133, 214, 133, LINE, 1.8))
    body.append(cube(218, 106, 92, 54, 14, ORANGE))
    body.append(text(258, 130, "router", 11, 800, fill=WHITE))
    body.append(text(258, 146, "easy or hard?", 8.6, 650, fill=WHITE))
    body.append(path("M324 120 C 360 90, 380 76, 414 74", stroke=tv(GREEN), w=6))
    body.append(text(370, 66, "80%", 11, 800, fill=tv(GREEN)))
    body.append(path("M324 146 C 360 176, 380 192, 414 194", stroke=tv(VIOLET), w=2.4))
    body.append(text(370, 206, "20%", 11, 800, fill=tv(VIOLET)))
    body.append(cube(420, 50, 150, 48, 12, GREEN))
    body.append(text(488, 72, "small model", 11, 800, fill=WHITE))
    body.append(text(488, 87, "£225 a month for all", 8.6, 650, fill=WHITE))
    body.append(cube(420, 170, 150, 48, 12, VIOLET))
    body.append(text(488, 192, "large model", 11, 800, fill=WHITE))
    body.append(text(488, 207, "£2,700 a month for all", 8.6, 650, fill=WHITE))
    body.append(arrow(586, 74, 622, 120, LINE, 1.6))
    body.append(arrow(586, 194, 622, 146, LINE, 1.6))
    body.append(solid(626, 112, 110, 42, AMBER, "£720", "a month", r=10, size=14, sub_size=9))
    body.append(text(380, 252, "0.8 × £225 + 0.2 × £2,700 = £720: a quarter of the cost of the large model "
                     "alone", 10.5, 800, fill=INK))
    desc = ("300,000 questions a month go to an orange router that judges each one easy or hard. 80% go "
            "along a thick green path to a small model, which would cost 225 pounds a month for all the "
            "questions; 20% go to a large model, which would cost 2,700 pounds for all of them. The "
            "combined cost is 0.8 times 225 plus 0.2 times 2,700, which is 720 pounds a month, a quarter "
            "of the cost of using the large model alone.")
    return figure("ai-casc", 760, 266, "".join(body), "A model cascade", desc,
                  "Using the lesson's example prices. The router itself must be cheap and reliable.")


# ===================================================== guardrails

@diagram("ai-guardrails")
def _guardrails():
    """Layered checks around a model with limited access."""
    body = [text(380, 22, "Guardrails in layers: no single check is trusted on its own", 12, 650,
                 fill=MUTED)]
    body.append(_bubble(18, 120, 120, 44, SLATE, ["a student's", "question"]))
    body.append(arrow(140, 142, 162, 142, LINE, 1.8))
    body.append(solid(166, 98, 112, 88, ORANGE, None, r=12))
    body.append(text(222, 122, "input checks", 10.5, 800, fill=WHITE))
    for k, s_ in enumerate(["abuse", "attacks", "personal data"]):
        body.append(text(222, 142 + k * 14, s_, 9, 650, fill=WHITE))
    body.append(arrow(280, 142, 302, 142, LINE, 1.8))
    body.append('<rect x="306" y="66" width="196" height="160" rx="14" fill="none" stroke="%s" '
                'stroke-width="2" stroke-dasharray="6 4"/>' % tv(RED))
    body.append(text(404, 84, "least privilege", 9.6, 800, fill=tv(RED)))
    body.append(cube(336, 100, 128, 50, 14, VIOLET))
    body.append(text(392, 130, "model", 12, 800, fill=WHITE))
    body.append(tint(318, 170, 84, 40, TEAL, "course notes", "allowed", r=8, size=9, sub_size=8.4, op=0.16))
    body.append(tint(410, 170, 84, 40, SLATE, "grades", "no access", r=8, size=9, sub_size=8.4, op=0.1, dash="4 3"))
    body.append(line(410, 170, 494, 210, stroke=tv(RED), w=1.6))
    body.append(arrow(504, 142, 526, 142, LINE, 1.8))
    body.append(solid(530, 98, 112, 88, ORANGE, None, r=12))
    body.append(text(586, 122, "output checks", 10.5, 800, fill=WHITE))
    for k, s_ in enumerate(["harmful content", "leaked data", "real citations"]):
        body.append(text(586, 142 + k * 14, s_, 9, 650, fill=WHITE))
    body.append(arrow(644, 142, 666, 142, LINE, 1.8))
    body.append(_bubble(670, 120, 82, 44, GREEN, ["answer"]))
    body.append(_bubble(306, 248, 196, 44, RED, ["text from documents and web", "pages: data, never orders"]))
    body.append(arrow(404, 246, 404, 228, tv(RED), 1.6))
    body.append(text(380, 312, "If a trick gets past one layer, the next one limits the damage.", 10.5, 750,
                     fill=INK))
    desc = ("A student's question passes orange input checks for abuse, attacks and personal data, then "
            "reaches the violet model inside a red dashed boundary labelled least privilege: it may read "
            "the course notes but has no access to grades. Text from documents and web pages enters as "
            "data, never as orders. The answer passes orange output checks for harmful content, leaked "
            "data and real citations before reaching the student. If a trick gets past one layer, the "
            "next one limits the damage.")
    return figure("ai-guard", 760, 324, "".join(body), "Layered guardrails", desc,
                  "Defence in depth: the same principle that protects banks and power stations.")
