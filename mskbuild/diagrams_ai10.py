"""AI course diagrams, Level 15: responsible AI and the capstone.

The fairness figure, the explanation waterfall and the privacy curves use the
lesson's numbers, and the adversarial example quotes the 2014 paper's
confidences. The canvas, the roadmap and the course map are illustrations.
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
from .diagrams_ai7 import _art


# ===================================================== fairness metrics

_GROUPS = [("group A", {"tp": 360, "fn": 40, "fp": 120, "tn": 480}),
           ("group B", {"tp": 120, "fn": 80, "fp": 40, "tn": 760})]


@diagram("ai-fairness-metrics")
def _fairness_metrics():
    """Two waffle charts of outcomes, and the four fairness numbers side by side."""
    body = [text(380, 22, "One model, two groups: which kind of fairness does it meet?", 12, 650,
                 fill=MUTED)]
    kinds = [("tp", GREEN, "would repay, approved"), ("fn", AMBER, "would repay, refused"),
             ("fp", RED, "did not repay, approved"), ("tn", SLATE, "did not repay, refused")]
    for g, (name, d) in enumerate(_GROUPS):
        x0 = 30 + g * 190
        body.append(text(x0 + 80, 50, name, 11, 800, fill=INK))
        cells = []
        for k, col, _ in kinds:
            cells += [col] * (d[k] // 10)
        for i, col in enumerate(cells):
            r, c = divmod(i, 10)
            body.append('<rect x="%d" y="%d" width="13" height="13" rx="2" fill="%s"%s/>'
                        % (x0 + c * 16, 60 + r * 16, col if col != AMBER else FILL,
                           ' stroke="%s" stroke-width="2.4"' % AMBER if col == AMBER else ""))
    for k, (_, col, lab) in enumerate(kinds):
        y = 240 + k * 15
        body.append('<rect x="30" y="%d" width="11" height="11" rx="2" fill="%s"%s/>'
                    % (y - 9, col if col != AMBER else FILL, ' stroke="%s" stroke-width="2"' % AMBER if col == AMBER else ""))
        body.append(text(48, y, lab, 9, 700, fill=INK, anchor="start"))
    body.append(text(250, 262, "each square is 10 applicants", 9, 650, fill=MUTED))
    rows = [("approved", "demographic parity"), ("true positive rate", "equal opportunity"),
            ("false positive rate", "equalised odds"), ("precision", "predictive parity")]
    vals = []
    for name, d in _GROUPS:
        n = float(sum(d.values()))
        vals.append([(d["tp"] + d["fp"]) / n, d["tp"] / float(d["tp"] + d["fn"]),
                     d["fp"] / float(d["fp"] + d["tn"]), d["tp"] / float(d["tp"] + d["fp"])])
    X0 = 420
    for k, (metric, fairness) in enumerate(rows):
        y = 58 + k * 58
        body.append(text(X0, y, metric, 10.5, 800, fill=INK, anchor="start"))
        body.append(text(X0 + 320, y, fairness, 9.4, 700, fill=MUTED, anchor="end"))
        for g in range(2):
            v = vals[g][k]
            yy = y + 8 + g * 16
            col = BLUE if g == 0 else PINK
            body.append('<rect x="%d" y="%d" width="%.1f" height="12" rx="3" fill="%s"/>' % (X0 + 20, yy, 230 * v, col))
            body.append(text(X0 + 14, yy + 10, "AB"[g], 9, 800, fill=tv(col), anchor="end"))
            body.append(text(X0 + 26 + 230 * v, yy + 10, "%d%%" % round(100 * v), 9.4, 800, fill=INK, anchor="start"))
        equal = abs(vals[0][k] - vals[1][k]) < 0.005
        body.append(text(X0 + 320, y + 28, "equal ✓" if equal else "unequal ✗", 10, 800,
                         fill=tv(GREEN) if equal else tv(RED), anchor="end"))
    desc = ("Two waffle charts of 100 squares, each square ten applicants. Group A: 36 squares would "
            "repay and were approved, 4 would repay but were refused, 12 were approved but did not "
            "repay, and 48 were refused and would not have repaid. Group B: 12, 8, 4 and 76. Paired "
            "bars compare the groups: approved, 48% against 16%, unequal, so demographic parity fails; "
            "true positive rate 90% against 60%, unequal, so equal opportunity fails; false positive "
            "rate 20% against 5%, unequal, so equalised odds fails; precision 75% for both, equal, so "
            "predictive parity holds.")
    return figure("ai-fair", 760, 308, "".join(body), "Fairness measures for two groups", desc,
                  "The same numbers as the lesson's Python: fair by one definition, unfair by three "
                  "others.")


# ===================================================== an explanation

@diagram("ai-explanations")
def _explanations():
    """A waterfall of feature contributions, and a counterfactual."""
    body = [text(380, 22, "Explaining one decision: how each feature moved the score", 12, 650,
                 fill=MUTED)]
    pl = Plot(80, 50, 420, 200, (0, 5), (-4.6, 1.0))
    body.append(pl.axes(yticks=(-4, -3, -2, -1, 0, 1), fmt="%g"))
    body.append(line(pl.px(0), pl.py(0), pl.px(5), pl.py(0), stroke=tv(GREEN), w=2, dash="6 4"))
    body.append(_halo(pl.px(5) - 4, pl.py(0) - 6, "approve if the score is 0 or more", 9.4, 800, "end"))
    steps = [("start|bias", -4.0, SLATE), ("income|£38k", 3.04, BLUE), ("address|2 years", 0.60, TEAL),
             ("missed|1 payment", -1.20, RED)]
    run = 0.0
    for k, (lab, v, col) in enumerate(steps):
        a, b = (0.0, v) if k == 0 else (run, run + v)
        x0 = pl.px(k + 0.15)
        w = pl.px(k + 0.85) - x0
        top, bot = pl.py(max(a, b)), pl.py(min(a, b))
        body.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="3" fill="%s"/>' % (x0, top, w, bot - top, col))
        vy = top - 5 if v > 0 else bot + 14
        body.append(text(x0 + w / 2.0, vy, ("%+.2f" % v).replace("-", "−"), 9.6, 800, fill=INK))
        for j, part in enumerate(lab.split("|")):
            body.append(text(x0 + w / 2.0, pl.y + pl.h + 15 + j * 12, part, 8.8, 750 if j == 0 else 600,
                             fill=INK if j == 0 else MUTED))
        run = b if k else v
    x0 = pl.px(4.15)
    w = pl.px(4.85) - x0
    body.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="3" fill="%s"/>'
                % (x0, pl.py(0), w, pl.py(run) - pl.py(0), PINK))
    body.append(text(x0 + w / 2.0, pl.py(run) + 15, ("%.2f" % run).replace("-", "−"), 10, 800, fill=INK))
    body.append(text(x0 + w / 2.0, pl.y + pl.h + 15, "final", 8.8, 800, fill=INK))
    body.append(text(x0 + w / 2.0, pl.y + pl.h + 27, "refused", 8.8, 800, fill=tv(RED)))
    LX = 530
    body.append(_bubble(LX, 70, 214, 92, AMBER, ["Counterfactual:", "approved if income were", "£57,500 instead of £38,000,", "or 7.2 years at the address"]))
    body.append(_bubble(LX, 180, 214, 64, BLUE, ["Even with no missed", "payments: still refused"]))
    desc = ("A waterfall chart for one loan applicant. The score starts at minus 4. Income of 38 thousand "
            "pounds adds 3.04, two years at the address adds 0.60, and one missed payment subtracts "
            "1.20, ending at minus 1.56, below the approval line at 0, so the application is refused. "
            "A note gives the counterfactual: it would be approved if income were 57,500 pounds "
            "instead of 38,000, or with 7.2 years at the address; even with no missed payments it would "
            "still be refused.")
    return figure("ai-expl", 760, 294, "".join(body), "Explaining a decision", desc,
                  "The same model as the lesson's Python: a transparent score that explains itself.")


# ===================================================== differential privacy

@diagram("ai-differential-privacy")
def _differential_privacy():
    """Two neighbouring datasets give almost the same noisy answers."""
    body = [text(380, 22, "Differential privacy: the answer barely depends on any one person", 12, 650,
                 fill=MUTED)]
    body.append(_bubble(30, 54, 190, 46, BLUE, ["survey without Sam:", "true count 142"]))
    body.append(_bubble(30, 124, 190, 46, PINK, ["survey with Sam:", "true count 143"]))
    body.append(arrow(222, 77, 262, 100, LINE, 1.6))
    body.append(arrow(222, 147, 262, 124, LINE, 1.6))
    body.append(solid(266, 92, 110, 40, VIOLET, "add noise", "ε = 0.5", r=10, size=11, sub_size=9))
    body.append(arrow(378, 112, 404, 112, LINE, 1.6))
    pl = Plot(420, 46, 310, 150, (132, 153), (0, 0.27))
    body.append(pl.axes(xticks=(135, 140, 145, 150), fmt="%g", xlabel="released answer"))
    for c, col in [(142, BLUE), (143, PINK)]:
        b = 2.0
        xs = [132 + 21 * i / 200.0 for i in range(201)]
        d = "M%.1f %.1f " % pl.pt(132, 0) + " ".join("L%.1f %.1f" % pl.pt(x, math.exp(-abs(x - c) / b) / (2 * b)) for x in xs) \
            + " L%.1f %.1f Z" % pl.pt(153, 0)
        body.append('<path d="%s" fill="%s" fill-opacity="0.22" stroke="%s" stroke-width="2"/>' % (d, col, tv(col)))
    body.append(text(575, 246, "the two curves overlap almost completely,", 10, 800, fill=INK))
    body.append(text(575, 262, "so no answer reveals whether Sam took part", 10, 800, fill=INK))
    body.append(text(200, 214, "smaller ε: more noise, more privacy, less accuracy", 10, 750, fill=tv(VIOLET)))
    desc = ("Two surveys differ by one person, Sam: the true counts are 142 without Sam and 143 with "
            "Sam. Each count has random noise added, with epsilon 0.5. The graph shows the distribution "
            "of released answers for each: two pointed curves, centred on 142 and 143, that overlap "
            "almost completely, so no released answer reveals whether Sam took part. A smaller epsilon "
            "means more noise, more privacy and less accuracy.")
    return figure("ai-dp", 760, 274, "".join(body), "Differential privacy", desc,
                  "Laplace noise with scale 2, as in the lesson's Python with ε = 0.5.")


# ===================================================== federated learning

def _phone(x, y, col):
    return ('<rect x="%d" y="%d" width="42" height="74" rx="8" fill="%s"/>'
            '<rect x="%d" y="%d" width="34" height="56" rx="3" fill="%s"/>'
            '<circle cx="%d" cy="%d" r="2.5" fill="%s"/>'
            % (x, y, DARK, x + 4, y + 6, col, x + 21, y + 68, WHITE))


@diagram("ai-federated")
def _federated():
    """Phones train locally; only updates travel; the server averages them."""
    body = [text(380, 22, "Federated learning: the data stays on the phones; only updates travel", 12, 650,
                 fill=MUTED)]
    body.append(cube(310, 54, 140, 54, 16, VIOLET))
    body.append(text(370, 78, "server", 12, 800, fill=WHITE))
    body.append(text(370, 95, "averages the updates", 9, 650, fill=WHITE))
    cols = [BLUE, TEAL, PINK]
    for k, col in enumerate(cols):
        x = 120 + k * 230
        body.append(_phone(x, 190, _mix(col, "#FFFFFF", 0.35)))
        body.append(text(x + 21, 228, "data", 8.6, 800, fill=DARK))
        body.append(text(x + 21, 280, "trains on its", 9, 700, fill=INK))
        body.append(text(x + 21, 293, "own messages", 9, 700, fill=INK))
        body.append('<path d="M%d 186 C %d 150, %d 140, %d 116" fill="none" stroke="%s" stroke-width="2.4" '
                    'class="ai-flow" stroke-dasharray="6 8"/>' % (x + 30, x + 40, 360, 360 - 30 + k * 30, AMBER))
        body.append('<path d="M%d 116 C %d 150, %d 160, %d 186" fill="none" stroke="%s" stroke-width="2" '
                    'stroke-dasharray="3 4"/>' % (390 - 30 + k * 30, 400, x + 10, x + 12, tv(GREEN)))
    body.append(_halo(185, 140, "model updates go up", 10, 800))
    body.append(_halo(575, 140, "the improved model comes back", 10, 800))
    body.append(text(380, 318, "Raw messages never leave the phones. Noise can be added to updates for extra "
                     "privacy.", 10, 750, fill=INK))
    desc = ("Three phones each hold their own data and train the shared model on it. Amber arrows carry "
            "only model updates up to a violet server, which averages them; green arrows bring the "
            "improved model back down to every phone. Raw messages never leave the phones, and noise "
            "can be added to the updates for extra privacy.")
    return figure("ai-fed", 760, 330, "".join(body), "Federated learning", desc,
                  "Phone keyboards learn to predict your next word this way.")


# ===================================================== adversarial example

_PANDA = ["............",
          "..KK....KK..",
          ".KKKWWWWKKK.",
          "..WWWWWWWW..",
          ".WKKWWWWKKW.",
          ".WKDWWWWDKW.",
          ".WKKWWWWKKW.",
          ".WWWWKKWWWW.",
          "..WWWKKWWW..",
          "...WWWWWW...",
          "..KKWWWWKK..",
          "............"]
_PANDA_PAL = {".": "#BBF7D0", "K": "#111827", "W": "#F9FAFB", "D": "#F9FAFB"}


@diagram("ai-adversarial")
def _adversarial():
    """Picture + faint noise = a picture that looks the same but fools the model."""
    body = [text(380, 22, "An adversarial example: invisible to people, decisive for the model", 12, 650,
                 fill=MUTED)]
    S = 9
    body.append(_art(40, 60, S, _PANDA, _PANDA_PAL))
    body.append(text(94, 188, "“panda”", 11, 800, fill=INK))
    body.append(text(94, 204, "57.7% confident", 9.6, 700, fill=MUTED))
    body.append(text(200, 120, "+ 0.007 ×", 13, 800, fill=INK))
    rnd = random.Random(4)
    for i in range(12):
        for j in range(12):
            body.append('<rect x="%d" y="%d" width="%d" height="%d" fill="%s"/>'
                        % (254 + j * S, 60 + i * S, S, S, rnd.choice([PINK, BLUE, AMBER, TEAL, VIOLET, LIME])))
    body.append(text(308, 188, "a crafted pattern", 10, 800, fill=INK))
    body.append(text(308, 204, "of tiny changes", 9.6, 700, fill=MUTED))
    body.append(text(386, 120, "=", 18, 800, fill=INK))
    body.append(_art(408, 60, S, _PANDA, _PANDA_PAL))
    body.append(text(462, 188, "“gibbon”", 11, 800, fill=tv(RED)))
    body.append(text(462, 204, "99.3% confident", 9.6, 700, fill=tv(RED)))
    LX = 552
    for k, (s_, col, wgt) in enumerate([("To a person the two pictures", INK, 750), ("look identical.", INK, 750),
                                        ("To the model, the second is", tv(RED), 800), ("almost certainly a gibbon.", tv(RED), 800),
                                        ("Defences: adversarial training,", MUTED, 650), ("input checks, and never", MUTED, 650),
                                        ("relying on one model alone.", MUTED, 650)]):
        body.append(text(LX, 70 + k * 19 + (k // 2) * 8, s_, 10.5, wgt, fill=col, anchor="start"))
    desc = ("A picture of a panda, which a classifier labels panda with 57.7% confidence, plus 0.007 "
            "times a crafted pattern of tiny changes, equals a picture that looks identical to a person "
            "but which the classifier labels gibbon with 99.3% confidence. Defences include adversarial "
            "training, input checks, and never relying on one model alone.")
    return figure("ai-adv", 760, 222, "".join(body), "An adversarial example", desc,
                  "The confidences are from the 2014 paper that made the panda famous; the pictures here "
                  "are redrawn as pixel art.")


# ===================================================== EU AI Act

@diagram("ai-eu-ai-act")
def _eu_ai_act():
    """Four tiers of risk, with examples."""
    body = [text(380, 22, "The EU AI Act: the higher the risk, the stricter the rules", 12, 650, fill=MUTED)]
    tiers = [("unacceptable", "banned", RED, "social scoring by governments;|manipulating people's behaviour"),
             ("high", "strict requirements", ORANGE, "job screening, credit scoring,|exam marking, medical devices"),
             ("limited", "be transparent", AMBER, "chatbots must say they are AI;|deepfakes must be labelled"),
             ("minimal", "no new rules", GREEN, "spam filters, video games,|most everyday AI")]
    cx, top, h = 220, 50, 62
    for k, (name, rule, col, ex) in enumerate(tiers):
        y = top + k * h
        hw1, hw2 = 56 + k * 36, 56 + (k + 1) * 36
        body.append('<polygon points="%d,%d %d,%d %d,%d %d,%d" fill="%s" stroke="%s" stroke-width="2"/>'
                    % (cx - hw1, y, cx + hw1, y, cx + hw2, y + h, cx - hw2, y + h, col, FILL))
        ink = ink_on(col)
        body.append(text(cx, y + 28, name, 11.5, 800, fill=ink))
        body.append(text(cx, y + 44, rule, 9, 700, fill=ink))
        body.append(line(cx + (hw1 + hw2) / 2.0 + 6, y + h / 2.0, 470, y + h / 2.0, stroke=LINE, w=1, dash="3 3"))
        for j, part in enumerate(ex.split("|")):
            body.append(text(478, y + h / 2.0 - 3 + j * 14, part, 10, 700, fill=INK, anchor="start"))
    desc = ("A pyramid of four tiers. At the top, unacceptable risk: banned, for example social scoring "
            "by governments and manipulating people's behaviour. Then high risk: strict requirements, for "
            "job screening, credit scoring, exam marking and medical devices. Then limited risk: be "
            "transparent, so chatbots must say they are AI and deepfakes must be labelled. At the wide "
            "base, minimal risk: no new rules, for spam filters, video games and most everyday AI.")
    return figure("ai-euact", 760, 310, "".join(body), "The EU AI Act's risk tiers", desc,
                  "Most AI systems sit in the wide base; the rules concentrate on the narrow top.")


# ===================================================== project canvas

@diagram("ai-project-canvas")
def _project_canvas():
    """A one-page plan for an AI project."""
    body = [text(380, 22, "A project canvas: plan the whole project on one page", 12, 650, fill=MUTED)]
    boxes = [("1. Problem", "What decision or task?", "Why does it matter?", BLUE),
             ("2. Users", "Who uses it?", "Who else is affected?", TEAL),
             ("3. Data", "Where from? Labelled how?", "How much? Any personal data?", VIOLET),
             ("4. Success", "Which metric?", "What does a baseline score?", GREEN),
             ("5. Model", "The simplest that could work,", "then what next?", INDIGO),
             ("6. Risks", "Who could be harmed?", "Fair for every group?", RED),
             ("7. Evaluation", "Validation and test sets?", "Which errors matter most?", ORANGE),
             ("8. Demo", "How will you show it?", "What goes in the model card?", PINK),
             ("9. Timeline", "Eight milestones,", "with dates", SLATE)]
    for k, (title, q1, q2, col) in enumerate(boxes):
        r, c = divmod(k, 3)
        x, y = 24 + c * 242, 40 + r * 88
        body.append(tint(x, y, 230, 78, col, op=0.12, r=10))
        body.append(text(x + 12, y + 22, title, 11.5, 800, fill=tv(col), anchor="start"))
        body.append(text(x + 12, y + 44, q1, 9.8, 650, fill=INK, anchor="start"))
        body.append(text(x + 12, y + 60, q2, 9.8, 650, fill=INK, anchor="start"))
    desc = ("A grid of nine boxes. 1 Problem: what decision or task, and why does it matter? 2 Users: "
            "who uses it, and who else is affected? 3 Data: where from, labelled how, how much, any "
            "personal data? 4 Success: which metric, and what does a baseline score? 5 Model: the "
            "simplest that could work, then what next? 6 Risks: who could be harmed, is it fair for "
            "every group? 7 Evaluation: validation and test sets, which errors matter most? 8 Demo: "
            "how will you show it, what goes in the model card? 9 Timeline: eight milestones with dates.")
    return figure("ai-canvas", 760, 312, "".join(body), "A project canvas", desc,
                  "Fill in every box before writing code. Box 4 matters most.")


# ===================================================== capstone roadmap

@diagram("ai-capstone-roadmap")
def _capstone_roadmap():
    """A winding road with eight milestones and a trophy."""
    body = [text(380, 22, "Eight milestones from an idea to a finished AI project", 12, 650, fill=MUTED)]
    pts = []
    for i in range(161):
        t = i / 160.0
        x = 50 + 660 * t
        y = 160 + 70 * math.sin(t * 2.6 * math.pi)
        pts.append((x, y))
    d = "M" + " L".join("%.1f %.1f" % p for p in pts)
    body.append('<path d="%s" fill="none" stroke="%s" stroke-width="30" stroke-linecap="round" '
                'stroke-opacity="0.9"/>' % (d, SLATE))
    body.append('<path d="%s" fill="none" stroke="%s" stroke-width="2.4" stroke-dasharray="10 9" '
                'class="ai-flow"/>' % (d, WHITE))
    stones = [("define", BLUE), ("data", TEAL), ("baseline", GREEN), ("first model", VIOLET),
              ("evaluate", INDIGO), ("improve", ORANGE), ("check", RED), ("present", PINK)]
    for k, (name, col) in enumerate(stones):
        t = (k + 0.5) / 8.0 * 0.94
        x, y = pts[int(t * 160)]
        up = math.sin(t * 2.6 * math.pi) < 0
        fy = y - 46 if not up else y + 22
        body.append(line(x, y, x, fy + (26 if not up else 0), stroke=INK, w=1.6))
        body.append(circle(x, y, 13, fill=col, stroke=FILL, w=3))
        body.append(text(x, y + 4.5, str(k + 1), 11, 900, fill=WHITE))
        w = 14 + 6.6 * len(name)
        body.append(solid(x - w / 2.0, fy, w, 24, col, name, r=7, size=10.5))
    ex, ey = pts[-1]
    body.append('<path d="M%d %d h 30 l -4 22 h -22 z" fill="%s"/>' % (ex - 15, ey - 34, AMBER))
    body.append('<rect x="%d" y="%d" width="10" height="10" fill="%s"/>' % (ex - 5, ey - 12, AMBER))
    body.append('<rect x="%d" y="%d" width="26" height="6" rx="2" fill="%s"/>' % (ex - 13, ey - 3, AMBER))
    desc = ("A winding grey road from left to right with eight numbered milestones: 1 define, 2 data, 3 "
            "baseline, 4 first model, 5 evaluate, 6 improve, 7 check responsibly, 8 present, ending at "
            "a golden trophy.")
    return figure("ai-road", 760, 290, "".join(body), "The capstone roadmap", desc,
                  "Get to milestone 4 quickly with something simple, then spend your time on 5 and 6.")


# ===================================================== the course map

_MAP = [("Beginner", BLUE, ["1 The story of AI", "2 What AI is", "3 Data"]),
        ("Explorer", TEAL, ["4 Classic ML", "5 Gradient descent"]),
        ("Builder", GREEN, ["6 The neuron", "7 Neural networks"]),
        ("Practitioner", ORANGE, ["8 Seeing: CNNs", "9 Language as numbers"]),
        ("Advanced", PINK, ["10 Attention", "11 LLMs", "12 Generative AI"]),
        ("Expert", VIOLET, ["13 RL and agents", "14 AI engineering"]),
        ("Hero", INDIGO, ["15 Responsible AI and capstone"])]


@diagram("ai-course-map")
def _course_map():
    """Fifteen levels in seven stages, climbing to the certificate."""
    body = [text(380, 22, "Your journey: fifteen levels from zero to hero", 12, 650, fill=MUTED)]
    nodes = []
    k = 0
    for s, (stage, col, levels) in enumerate(_MAP):
        for lv in levels:
            col_x = 60 + (k % 5) * 160
            row = k // 5
            x = col_x if row % 2 == 0 else 60 + (4 - k % 5) * 160
            y = 70 + row * 104
            nodes.append((x, y, lv, col, stage))
            k += 1
    d = "M" + " L".join("%d %d" % (x, y) for x, y, _, _, _ in nodes)
    body.append('<path d="%s" fill="none" stroke="%s" stroke-width="5" stroke-linejoin="round" '
                'stroke-dasharray="2 10" stroke-linecap="round"/>' % (d, LINE))
    body.append('<path d="%s" fill="none" stroke="%s" stroke-width="2" stroke-dasharray="8 10" class="ai-flow"/>'
                % (d, AMBER))
    seen = set()
    for x, y, lv, col, stage in nodes:
        num, name = lv.split(" ", 1)
        body.append(circle(x, y, 20, fill=col, stroke=FILL, w=3))
        body.append(text(x, y + 6, num, 15, 900, fill=WHITE))
        lines_ = [name] if len(name) < 20 else [name[:name.rfind(" ", 0, 20)], name[name.rfind(" ", 0, 20) + 1:]]
        for j, ln in enumerate(lines_):
            body.append(text(x, y + 38 + j * 13, ln, 9.8, 800, fill=INK))
        if stage not in seen:
            seen.add(stage)
            body.append(text(x, y - 28, stage.upper(), 8.6, 900, fill=tv(col)))
    x, y = nodes[-1][0], nodes[-1][1]
    tx, ty = x - 150, y + 70
    body.append(path("M%d %d C %d %d, %d %d, %d %d" % (x - 14, y + 16, x - 40, y + 70, tx + 70, ty, tx + 34, ty),
                     stroke=AMBER, w=2.4))
    body.append(arrow(tx + 44, ty, tx + 30, ty, AMBER, 2.4))
    body.append('<path d="M%d %d h 40 l -6 30 h -28 z" fill="%s"/>' % (tx - 20, ty - 26, AMBER))
    body.append('<rect x="%d" y="%d" width="12" height="12" fill="%s"/>' % (tx - 6, ty + 4, AMBER))
    body.append('<rect x="%d" y="%d" width="34" height="8" rx="2" fill="%s"/>' % (tx - 17, ty + 16, AMBER))
    body.append(text(tx - 30, ty + 6, "your certificate", 11, 800, fill=tv(ORANGE), anchor="end"))
    desc = ("A winding path through fifteen numbered circles, coloured by stage. Beginner: 1 the story of "
            "AI, 2 what AI is, 3 data. Explorer: 4 classic machine learning, 5 gradient descent. Builder: 6 "
            "the neuron, 7 neural networks. Practitioner: 8 seeing with CNNs, 9 language as numbers. "
            "Advanced: 10 attention, 11 large language models, 12 generative AI. Expert: 13 reinforcement "
            "learning and agents, 14 AI engineering. Hero: 15 responsible AI and the capstone. The path "
            "ends at a golden trophy: the certificate.")
    return figure("ai-map", 760, 380, "".join(body), "The course map", desc,
                  "Every level built on the one before. Look how far you have come.")
