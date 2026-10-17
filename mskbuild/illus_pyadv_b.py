"""Illustrations for the Advanced Python topics, set two: simulation and machine learning.

Every number in these pictures is worked out by the same rules the lesson's programs use (seeded random numbers, the
same step and update functions), so a picture never disagrees with the output printed under its code."""
import math
import random
from collections import Counter
from functools import lru_cache

from .illus import Canvas, INK, ARROW, figure, illustration, _n
from . import illus_props as P

RED, GREEN, GOLD, BLUE, PLUM = "#C84B43", "#2F9F77", "#DFA000", "#2F82C0", "#6B4C9E"
GOOD = "#2F7F5F"        # a green that reads on white


def _axes(cv, x0, y0, w, h, xlabel, ylabel, ylx):
    """An L shaped pair of axes with a label on each. (x0, y0) is the corner where they meet, ylx the x of the rotated label."""
    out = cv.line(x0, y0, x0 + w, y0, "#4A6470", 2.5) + cv.line(x0, y0, x0, y0 - h, "#4A6470", 2.5)
    out += cv.text(x0 + w / 2, y0 + 34, xlabel, 13, 700, cls="il-ink2")
    out += cv.group(cv.text(0, 0, ylabel, 13, 700, cls="il-ink2"), ylx, y0 - h / 2, rot=-90)
    return out


def _line(cv, pts, color, sw, dash=None):
    return cv.path("M" + " L".join("%s %s" % (_n(a), _n(b)) for a, b in pts), stroke=color, sw=sw, dash=dash)


# ------------------------------------------------------------------ Monte Carlo estimate of pi

@lru_cache(maxsize=None)
def _pi_run():
    """The lesson's own estimate_pi calls, with its seed, so the table matches the printed output."""
    rng, rows = random.Random(2024), []
    for darts in (100, 1000, 10000, 100000):
        inside = 0
        for _ in range(darts):
            x, y = rng.random(), rng.random()
            if x * x + y * y <= 1:
                inside += 1
        est = 4 * inside / darts
        rows.append((darts, est, abs(est - math.pi)))
    return rows


@illustration("monte-carlo-pi")
def _montecarlo():
    cv = Canvas(800, 500).backdrop()
    rng = random.Random(1)
    n = 220
    pts = [(rng.random(), rng.random()) for _ in range(n)]
    hit = [x * x + y * y <= 1 for x, y in pts]
    inside = sum(hit)
    left, top, side = 54, 92, 330
    bottom = top + side
    cv.add(P.card(cv, 14, 24, 410, 452, 20, "darts thrown at random", "teal"))
    cv.add(cv.rect(left, top, side, side, 6, "#FFFFFF", stroke="#6F8794", sw=2.2))
    cv.add(cv.path("M%d %d L%d %d A%d %d 0 0 1 %d %d Z" % (left, bottom, left, top, side, side, left + side, bottom), fill="#C9F3E0", stroke=GREEN, sw=2.6))
    for (x, y), h in zip(pts, hit):
        cv.add(cv.circle(left + x * side, bottom - y * side, 4.2, GREEN if h else RED, stroke="#FFFFFF", sw=1))
    cv.add(P.pill(cv, left + 78, bottom - 34, "quarter circle", "paper", 13, 12, 26, 800))
    cv.add(cv.text(left - 12, bottom + 5, "0", 13, 700, cls="il-ink2"), cv.text(left - 12, top + 5, "1", 13, 700, cls="il-ink2"), cv.text(left + side, bottom + 22, "1", 13, 700, cls="il-ink2"))
    cv.add(cv.circle(left + 34, bottom + 38, 6, GREEN, stroke="#FFFFFF", sw=1), cv.text(left + 48, bottom + 43, "inside: %d" % inside, 14, 800, anchor="start", cls="il-ink"))
    cv.add(cv.circle(left + 168, bottom + 38, 6, RED, stroke="#FFFFFF", sw=1), cv.text(left + 182, bottom + 43, "outside: %d" % (n - inside), 14, 800, anchor="start", cls="il-ink"))
    cv.add(P.badge(cv, 42, 64, 1))

    cv.add(P.card(cv, 440, 24, 346, 452, 20, "count them, then multiply by 4", "sun"))
    cv.add(P.lift(cv, 462, 84, 302, 46, "sky", 12, 5, hl=False), cv.text(613, 114, "inside ÷ all darts  ≈  π ÷ 4", 17, 800, fill=INK))
    cv.add(P.lift(cv, 462, 150, 302, 46, "mint", 12, 5, hl=False), cv.text(613, 180, "π  ≈  4 × inside ÷ all darts", 17, 800, fill=INK))
    cv.add(cv.text(613, 226, "here: 4 × %d ÷ %d = %.2f" % (inside, n, 4 * inside / n), 15, 800, cls="il-ink", mono=True))
    cv.add(P.badge(cv, 468, 66, 2))
    cv.add(cv.rect(462, 246, 302, 176, 14, "#FFFFFF", stroke="#9FB3BE", sw=1.4))
    for c, label in ((520, "darts"), (610, "estimate"), (704, "error")):
        cv.add(cv.text(c, 272, label, 13, 800, fill=INK))
    cv.add(cv.line(476, 282, 750, 282, "#9FB3BE", 1.4))
    for i, (d, est, err) in enumerate(_pi_run()):
        y = 310 + i * 34
        cv.add(cv.text(520, y, "{:,}".format(d), 15, 800, fill=INK, mono=True), cv.text(610, y, "%.4f" % est, 15, 800, fill=INK, mono=True),
               cv.text(704, y, "%.4f" % err, 15, 800, fill=RED if err > .1 else GOOD, mono=True))
    cv.add(P.badge(cv, 476, 252, 3))
    cv.add(P.pill(cv, 613, 450, "100 × the darts: about 10 × less error", "paper", 13.5, 12, 26, 800))
    return figure(
        "monte-carlo-pi", cv, "A Monte Carlo estimate of pi: random darts, and the fraction that land inside a quarter circle",
        "Left, a square of side 1 with a quarter circle of radius 1 drawn in one corner, and %d random darts shown as dots. Green dots landed inside "
        "the quarter circle, %d of them, and red dots landed outside, %d of them. Right, the idea in two lines: the fraction of darts inside should "
        "be about pi divided by 4, which is the area of the quarter circle compared with the area of the square, so pi is about 4 times the number "
        "inside divided by the number thrown. For these darts that is 4 times %d divided by %d, which is %.2f. A table from the lesson's program "
        "shows 100 darts giving %.4f, 1,000 giving %.4f, 10,000 giving %.4f and 100,000 giving %.4f, with the error shrinking each time. A hundred "
        "times as many darts makes the error only about ten times smaller."
        % ((n, inside, n - inside, inside, n, 4 * inside / n) + tuple(e for _, e, _ in _pi_run())),
        ["Throw darts at random at the square. The share that land inside the quarter circle should be about π ÷ 4.",
         "So π is about 4 × inside ÷ all. Here, %d darts give %.2f." % (n, 4 * inside / n),
         "More darts give a better answer, but slowly: the error shrinks with the square root of the number of darts."],
        "A Monte Carlo method answers a question by random sampling, which works even when the exact mathematics is hard.")


# ------------------------------------------------------------------ the SIR model of an epidemic

def _sir(beta, gamma, days, population=1000, infected=1):
    """The lesson's sir function."""
    s, i, r = population - infected, infected, 0
    out = []
    for day in range(days + 1):
        out.append((day, s, i, r))
        new, rec = beta * s * i / population, gamma * i
        s -= new
        i += new - rec
        r += rec
    return out


@illustration("epidemic-curves")
def _epidemic():
    cv = Canvas(800, 520).backdrop()
    cv.add(P.card(cv, 14, 24, 772, 324, 20, "flattening the curve: the same disease, spreading less", "coral"))
    X0, Y0, PW, PH = 84, 292, 430, 210
    days, top, limit = 120, 270.0, 120
    cv.add(_axes(cv, X0, Y0, PW, PH, "days since the first case", "people ill at once", 38))
    for g in range(1, 5):
        cv.add(cv.line(X0, Y0 - g * PH / 4, X0 + PW, Y0 - g * PH / 4, "var(--il-line)", 1.2))
    for v in (0, 100, 200):
        cv.add(cv.text(X0 - 8, Y0 - v / top * PH + 5, str(v), 12, 700, anchor="end", cls="il-ink2"))
    ly = Y0 - limit / top * PH
    cv.add(cv.line(X0, ly, X0 + PW, ly, RED, 2.4, dash="8 6"))
    cv.add(cv.text(X0 + PW - 6, ly + 18, "an example limit: 120 at once", 12.5, 800, anchor="end", cls="il-bad"))
    runs = [(0.5, RED, "no care"), (0.35, "#C98A00", "some care"), (0.25, GREEN, "a lot of care")]
    stats = []
    for beta, col, name in runs:
        hist = _sir(beta, 0.2, days)
        cv.add(_line(cv, [(X0 + d / days * PW, Y0 - min(i, top) / top * PH) for d, s, i, r in hist], col, 4.2))
        full = _sir(beta, 0.2, 200)
        peak = max(full, key=lambda row: row[2])
        stats.append((beta, col, name, peak[0], round(peak[2]), round(1000 - full[-1][1])))
        cv.add(cv.circle(X0 + peak[0] / days * PW, Y0 - peak[2] / top * PH, 5.5, col, stroke="#FFFFFF", sw=1.6))
    for tick in (0, 30, 60, 90, 120):
        cv.add(cv.text(X0 + tick / days * PW, Y0 + 17, str(tick), 12, 700, cls="il-ink2"))
    cv.add(P.badge(cv, 42, 64, 1))
    # the legend, on the right
    cv.add(cv.text(666, 80, "spread rate β", 14, 800, cls="il-ink"))
    for k, (beta, col, name, day, ill, total) in enumerate(stats):
        y = 94 + k * 70
        cv.add(cv.rect(552, y, 216, 58, 12, "#FFFFFF", stroke=col, sw=2.6), cv.rect(552, y, 10, 58, 4, col))
        cv.add(cv.text(574, y + 23, "β = %s  (%s)" % (beta, name), 13.5, 800, anchor="start", fill=INK))
        cv.add(cv.text(574, y + 43, "peak %d ill, on day %d" % (ill, day), 13, 700, anchor="start", fill=INK))
    cv.add(cv.text(660, 322, "lower and later: the hospital copes", 12.5, 800, cls="il-ok"))
    # the model
    cv.add(P.card(cv, 14, 376, 772, 128, 20, "the model, one day at a time", "teal"))
    boxes = [("S", "susceptible", "sky", 66), ("I", "infected", "coral", 306), ("R", "recovered", "mint", 546)]
    for letter, word, color, x in boxes:
        cv.add(P.lift(cv, x, 414, 188, 54, color, 12, 5, hl=False), cv.text(x + 32, 450, letter, 28, 800, fill=INK), cv.text(x + 112, 448, word, 16, 800, fill=INK))
    cv.add(P.arrow(cv, [(260, 441), (300, 441)], ARROW, 3, 10), P.arrow(cv, [(500, 441), (540, 441)], ARROW, 3, 10))
    cv.add(cv.text(280, 408, "catch it", 12.5, 700, cls="il-ink2"), cv.text(520, 408, "recover", 12.5, 700, cls="il-ink2"))
    cv.add(cv.text(280, 492, "β × S × I ÷ N", 12.5, 800, cls="il-ink", mono=True), cv.text(520, 492, "γ × I", 12.5, 800, cls="il-ink", mono=True))
    cv.add(P.badge(cv, 42, 398, 2))
    return figure(
        "epidemic-curves", cv, "The SIR model: lowering the spread rate makes the peak of an epidemic lower and later",
        "A chart of the number of people ill at once, over 120 days, for three runs of the SIR model in a population of 1,000 with a recovery rate of "
        "0.2. With no care, a spread rate of 0.5, the curve rises fast, peaks at %d people ill on day %d, and %d people catch it in all. With some "
        "care, 0.35, it peaks at %d on day %d, and %d catch it. With a lot of care, 0.25, it peaks at only %d on day %d, and %d catch it. A dashed "
        "red line marks an example limit of 120 patients at once: only the curves for some care and a lot of care stay below it. Below the chart "
        "the model is drawn as three boxes: susceptible people become infected at a rate of beta times S times I divided by N, and infected "
        "people recover at a rate of gamma times I." % tuple(v for _, _, _, d, ill, total in stats for v in (ill, d, total)),
        ["Each curve is the number ill at once. Reducing the spread rate β lowers the peak and moves it later, and fewer people catch it overall.",
         "Each day, some susceptible people catch it, and some of the infected recover. Everyone is in one of the three boxes, S, I or R."],
        "What overwhelms a hospital is the number ill at once, so a lower, later peak saves lives even when many people still catch it.")


# ------------------------------------------------------------------ the Game of Life glider

def _life_step(live):
    near = Counter((x + dx, y + dy) for x, y in live for dx in (-1, 0, 1) for dy in (-1, 0, 1) if (dx, dy) != (0, 0))
    return {c for c, k in near.items() if k == 3 or (k == 2 and c in live)}


def _life_grid(cv, x, y, cells, size=5, cell=22, ghost=()):
    """A square grid of cells. (x, y) is the top left. Ghost cells are drawn as a dashed red outline."""
    w = size * cell
    out = cv.rect(x - 3, y - 3, w + 6, w + 6, 8, "#FFFFFF", stroke="#9FB3BE", sw=1.6)
    for i in range(1, size):
        out += cv.line(x + i * cell, y, x + i * cell, y + w, "#D5DEE4", 1) + cv.line(x, y + i * cell, x + w, y + i * cell, "#D5DEE4", 1)
    for cx, cy in ghost:
        out += cv.rect(x + cx * cell + 3, y + cy * cell + 3, cell - 6, cell - 6, 4, "none", stroke=RED, sw=2, dash="4 3")
    for cx, cy in cells:
        out += cv.rect(x + cx * cell + 2, y + cy * cell + 2, cell - 4, cell - 4, 4, "#14707A")
    return out


@illustration("life-glider")
def _life():
    cv = Canvas(800, 520).backdrop()
    cv.add(P.card(cv, 14, 24, 772, 236, 20, "a glider walks across the grid", "teal"))
    g, gens = {(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)}, []
    for _ in range(5):
        gens.append(g)
        g = _life_step(g)
    shift = (min(x for x, _ in gens[4]) - min(x for x, _ in gens[0]), min(y for _, y in gens[4]) - min(y for _, y in gens[0]))
    assert shift == (1, 1) and all(len(c) == 5 for c in gens)
    for k, cells in enumerate(gens):
        x = 44 + k * 152
        cv.add(_life_grid(cv, x, 84, cells, 5, 22, ghost=gens[0] if k == 4 else ()))
        cv.add(cv.text(x + 55, 224, "generation %d" % k, 14, 800, cls="il-ink"))
        if k < 4:
            cv.add(P.arrow(cv, [(x + 122, 139), (x + 146, 139)], ARROW, 2.8, 9))
    cv.add(cv.text(44 + 4 * 152 + 55, 246, "red: where it began", 12.5, 800, cls="il-bad"))
    cv.add(P.badge(cv, 42, 64, 1))

    cv.add(P.card(cv, 14, 290, 772, 208, 20, "three rules, and that is the whole game", "sun"))
    rules = [("survives", "mint", [(0, 0), (2, 0), (2, 2)], True, "a live cell with 2 or 3", "live neighbours survives", GREEN),
             ("dies", "coral", [(0, 0), (1, 0), (2, 0), (0, 2), (2, 2)], True, "a live cell with fewer than 2", "or more than 3 neighbours dies", RED),
             ("is born", "sky", [(0, 0), (2, 1), (1, 2)], False, "a dead cell with exactly 3", "live neighbours is born", BLUE)]
    for k, (verdict, color, around, alive, l1, l2, col) in enumerate(rules):
        x0 = 34 + k * 252
        cv.add(cv.rect(x0, 322, 234, 160, 14, "#FFFFFF", stroke=col, sw=2.2))
        gx, gy, c = x0 + 18, 338, 26
        cv.add(cv.rect(gx - 3, gy - 3, 3 * c + 6, 3 * c + 6, 6, "#F4F8FA", stroke="#9FB3BE", sw=1.4))
        for i in range(1, 3):
            cv.add(cv.line(gx + i * c, gy, gx + i * c, gy + 3 * c, "#D5DEE4", 1), cv.line(gx, gy + i * c, gx + 3 * c, gy + i * c, "#D5DEE4", 1))
        for cx, cy in around + ([(1, 1)] if alive else []):
            cv.add(cv.rect(gx + cx * c + 2, gy + cy * c + 2, c - 4, c - 4, 4, "#14707A"))
        cv.add(cv.rect(gx + c + 1, gy + c + 1, c - 2, c - 2, 4, "none", stroke=col, sw=3.2))
        cv.add(P.pill(cv, x0 + 168, gy + 39, verdict, color, 15, 14, 28, 800))
        cv.add(cv.text(x0 + 117, 442, l1, 12.5, 700, fill=INK), cv.text(x0 + 117, 462, l2, 12.5, 700, fill=INK))
    cv.add(P.badge(cv, 42, 312, 2))
    return figure(
        "life-glider", cv, "Conway's Game of Life: a five-cell glider moves across the grid because of three simple rules",
        "Five small grids show the same five live cells, the glider, in generations 0 to 4. Its shape changes in each of the first four steps and "
        "in generation 4 it is the original shape again, moved one square down and one square right. A red dashed outline in the last grid marks "
        "where it started. Below, the three rules. A live cell with 2 or 3 live neighbours survives. A live cell with fewer than 2 or more than 3 "
        "neighbours dies. A dead cell with exactly 3 live neighbours is born. Nothing in the rules mentions movement: the glider's travel emerges "
        "from them.",
        ["The glider has five cells in every generation. After four steps it has the same shape, one square further along the diagonal.",
         "Every cell is updated at the same moment, using only the count of its eight neighbours. In each small grid the outlined centre cell is the one being judged."],
        "Simple local rules can produce complex behaviour that nobody wrote into the program. That is called emergence.")


# ------------------------------------------------------------------ k nearest neighbours

APPLES = [(0.18, 0.78), (0.30, 0.88), (0.42, 0.70), (0.55, 0.82), (0.70, 0.75), (0.82, 0.88), (0.35, 0.58), (0.62, 0.62)]
LEMONS = [(0.15, 0.28), (0.28, 0.15), (0.45, 0.32), (0.58, 0.18), (0.72, 0.30), (0.85, 0.20), (0.40, 0.45), (0.74, 0.43)]
NEW = (0.50, 0.52)


def _star(cv, cx, cy, r, fill):
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * .46
        pts.append((cx + math.cos(a) * rr, cy + math.sin(a) * rr))
    return cv.poly(pts, fill=fill, stroke="#FFFFFF", sw=2)


def _apple(cv, x, y, r=9):
    return cv.circle(x, y, r, "#F77F72", stroke="#C84B43", sw=2.2)


def _lemon(cv, x, y, r=9):
    return cv.rect(x - r, y - r, 2 * r, 2 * r, 4, "#FFCC4A", stroke="#DFA000", sw=2.2)


@illustration("knn-vote")
def _knn():
    cv = Canvas(800, 480).backdrop()
    items = sorted([(math.dist(p, NEW), "apple") for p in APPLES] + [(math.dist(p, NEW), "lemon") for p in LEMONS])
    k = 3
    nearest = items[:k]
    votes = Counter(label for _, label in nearest)
    winner = votes.most_common(1)[0][0]
    assert items[0][1] == "lemon" and winner == "apple" and votes["apple"] == 2 and votes["lemon"] == 1, (items[:5], votes)
    near_pts = [p for p in APPLES + LEMONS if math.dist(p, NEW) <= nearest[-1][0] + 1e-9]
    assert len(near_pts) == k
    left, top, size = 112, 86, 280          # a square plot, so a circle of distance really is round

    def pos(p):
        return left + p[0] * size, top + (1 - p[1]) * size

    cv.add(P.card(cv, 14, 24, 470, 432, 20, "a new fruit and its three nearest", "teal"))
    cv.add(cv.rect(left, top, size, size, 8, "#FFFFFF", stroke="#9FB3BE", sw=1.6))
    cv.add(_axes(cv, left, top + size, size, size, "weight (scaled)", "sweetness (scaled)", 62))
    nx, ny = pos(NEW)
    cv.add(cv.circle(nx, ny, (items[k - 1][0] + items[k][0]) / 2 * size, "#EEE2F8", stroke=PLUM, sw=2.4, dash="7 5"))
    for p in near_pts:
        px, py = pos(p)
        cv.add(cv.line(nx, ny, px, py, PLUM, 2.4))
    for p in APPLES:
        cv.add(_apple(cv, *pos(p)))
    for p in LEMONS:
        cv.add(_lemon(cv, *pos(p)))
    cv.add(_star(cv, nx, ny, 17, PLUM))
    ly = top + size + 66
    cv.add(_apple(cv, 112, ly - 5, 8), cv.text(128, ly, "apple", 14, 800, anchor="start", cls="il-ink"))
    cv.add(_lemon(cv, 214, ly - 5, 8), cv.text(230, ly, "lemon", 14, 800, anchor="start", cls="il-ink"))
    cv.add(_star(cv, 322, ly - 5, 10, PLUM), cv.text(338, ly, "new, unknown", 14, 800, anchor="start", cls="il-ink"))
    cv.add(P.badge(cv, 42, 64, 1))

    cv.add(P.card(cv, 500, 24, 286, 432, 20, "k = 3: let them vote", "sun"))
    steps = [("1  measure the distance", "to every stored fruit", "sky"), ("2  keep the k = 3 nearest", "the ones joined by lines", "mint"), ("3  the most common label", "wins the vote", "sun")]
    for i, (a, b, color) in enumerate(steps):
        y = 84 + i * 96
        cv.add(P.lift(cv, 520, y, 246, 56, color, 12, 5, hl=False), cv.text(643, y + 24, a, 14.5, 800, fill=INK), cv.text(643, y + 44, b, 13, 650, fill=INK))
        if i < 2:
            cv.add(P.arrow(cv, [(643, y + 66), (643, y + 90)], ARROW, 3, 10))
    cv.add(cv.rect(520, 366, 246, 76, 12, "#FFFFFF", stroke="#9FB3BE", sw=1.4))
    for i, label in enumerate(("apple", "lemon")):
        y = 376 + i * 30
        cv.add(cv.text(536, y + 18, label, 14, 800, anchor="start", fill=INK))
        for j in range(votes[label]):
            cv.add((_apple if label == "apple" else _lemon)(cv, 628 + j * 28, y + 12, 9))
        cv.add(cv.text(750, y + 18, str(votes[label]), 15, 800, anchor="end", fill=INK, mono=True))
    cv.add(P.badge(cv, 528, 66, 2))
    return figure(
        "knn-vote", cv, "k-nearest neighbours: a new fruit is classified by a vote of the three stored fruits closest to it",
        "A scatter chart of stored fruit with weight along the bottom and sweetness up the side. Apples are red circles, mostly high up, and lemons "
        "are yellow squares, mostly low down. A purple star marks a new fruit that has not been classified yet, in the middle of the chart. A "
        "dashed circle around it holds its three nearest neighbours, joined to it by lines: one lemon and two apples. On the right, the three "
        "steps: measure the distance to every stored fruit, keep the three nearest, and let them vote. Apple gets 2 votes and lemon gets 1, so the "
        "new fruit is predicted to be an apple. The single nearest neighbour is a lemon, so with k equal to 1 the answer would have been wrong.",
        ["k-NN stores the examples and does no training. To classify a new item it looks at the items closest to it.",
         "The k nearest each get one vote and the most common label wins. A small k trusts one odd neighbour, so a larger k is steadier."],
        "Both features must be scaled to the same range first, or the one with the biggest numbers decides every distance.")


# ------------------------------------------------------------------ gradient descent

def _descent(rate, steps, start=0.5):
    """The positions of w as gradient descent walks down the cost (w - 3) squared."""
    w, out = start, [start]
    for _ in range(steps):
        w -= rate * 2 * (w - 3)
        out.append(w)
    return out


@illustration("gradient-descent")
def _gradient():
    cv = Canvas(800, 480).backdrop()
    cost = lambda w: (w - 3) ** 2

    def mapper(x0, y0, w, h, wlo, whi, top):
        """Turns (w, cost) into a point on a chart. The cost is clipped at the top of the chart."""
        return lambda wv, c=None: (x0 + (wv - wlo) / (whi - wlo) * w, y0 - min(cost(wv) if c is None else c, top) / top * h)

    cv.add(P.card(cv, 14, 24, 470, 432, 20, "walking downhill on the cost", "teal"))
    X0, Y0, PW, PH = 74, 356, 390, 252
    cv.add(_axes(cv, X0, Y0, PW, PH, "the number being learned", "cost (how wrong)", 44))
    f = mapper(X0, Y0, PW, PH, -0.3, 6.3, 11.0)
    cv.add(_line(cv, [f(-0.3 + i * 6.6 / 80) for i in range(81)], "#4A6470", 4.2))
    path = _descent(0.15, 4)
    spots = [f(v) for v in path] + [f(3.0)]
    cv.add(_line(cv, spots, PLUM, 2.4, "5 4"))
    slope = 2 * (path[0] - 3)
    a, b = f(path[0] - .4, cost(path[0]) - slope * .4), f(path[0] + .4, cost(path[0]) + slope * .4)
    cv.add(cv.line(a[0], a[1], b[0], b[1], RED, 3.4))
    for i, (sx, sy) in enumerate(spots):
        last = i == len(spots) - 1
        cv.add(cv.circle(sx, sy, 7, "#62CFA3" if last else "#FFCC4A", stroke="#2F9F77" if last else "#8F2923", sw=2.4))
    cv.add(cv.text(spots[0][0] - 14, spots[0][1] - 4, "start", 13, 800, anchor="end", cls="il-ink"))
    cv.add(cv.text(spots[0][0] + 32, spots[0][1] + 34, "steep: a big step", 13, 800, anchor="start", cls="il-bad"))
    cv.add(cv.text(270, 150, "the steeper the slope,", 13.5, 800, cls="il-ink"), cv.text(270, 170, "the bigger the step", 13.5, 800, cls="il-ink"))
    ly = Y0 + 68
    cv.add(cv.circle(84, ly - 5, 7, "#FFCC4A", stroke="#8F2923", sw=2.4), cv.text(98, ly, "a step", 13.5, 800, anchor="start", cls="il-ink"))
    cv.add(cv.line(166, ly - 5, 188, ly - 5, RED, 3.4), cv.text(196, ly, "the slope", 13.5, 800, anchor="start", cls="il-ink"))
    cv.add(cv.circle(290, ly - 5, 7, "#62CFA3", stroke="#2F9F77", sw=2.4), cv.text(304, ly, "the bottom: slope 0", 13.5, 800, anchor="start", cls="il-ink"))
    cv.add(P.badge(cv, 42, 64, 1))

    cv.add(P.card(cv, 500, 24, 286, 432, 20, "the learning rate", "sun"))
    minis = [("too small", "creeps down: very slow", 0.04, 10, "#8A6400"), ("about right", "arrives in a few steps", 0.4, 5, GOOD), ("too big", "overshoots: cost grows", 1.1, 3, RED)]
    for k, (title, note, rate, nsteps, col) in enumerate(minis):
        y0 = 102 + k * 118
        cv.add(cv.text(518, y0 + 6, title, 14, 800, anchor="start", cls="il-ink"), cv.text(768, y0 + 6, note, 12.5, 700, anchor="end", cls="il-ink2"))
        bx, by, bw, bh = 518, y0 + 16, 250, 90
        cv.add(cv.rect(bx, by, bw, bh, 8, "#FFFFFF", stroke=col, sw=2.2))
        m = mapper(bx + 8, by + bh - 8, bw - 16, bh - 16, -1.0, 7.0, 20.0)
        cv.add(_line(cv, [m(-1 + i * 8.0 / 50) for i in range(51)], "#6F8794", 2.4))
        seq = [v for v in _descent(rate, nsteps) if -1.0 <= v <= 7.0]
        cv.add(_line(cv, [m(v) for v in seq], col, 2.2, "4 3"))
        for i, v in enumerate(seq):
            cv.add(cv.circle(*m(v), 4.6, col, stroke="#FFFFFF", sw=1.3))
    cv.add(P.badge(cv, 528, 66, 2))
    return figure(
        "gradient-descent", cv, "Gradient descent: step downhill on the cost, with a step size called the learning rate",
        "Left, a bowl shaped curve of cost against a number w that the program is learning. A point starts high on the left side at w0. At each "
        "step it moves downhill, in the direction opposite to the slope, by an amount that depends on how steep the slope is. The first steps are "
        "big because the slope is steep there, and they get smaller as the curve flattens, until the point reaches the bottom, where the cost "
        "is lowest and the slope is zero. Right, three small charts show the learning rate, which is the size of each step. Too small, and the "
        "point creeps down the side very slowly. About right, and it reaches the bottom in a few steps. Too big, and each step jumps over the "
        "bottom and lands higher up the other side, so the cost grows instead of shrinking.",
        ["Work out the slope, step the opposite way, and repeat. Steep slopes make big steps and flat slopes make small ones.",
         "The learning rate scales the step. Too small is slow, and too big overshoots the bottom and never settles."],
        "This one loop is how every neural network is trained, however many billions of numbers it has to find.")


# ------------------------------------------------------------------ confusion matrix

@illustration("confusion-matrix")
def _confusion():
    cv = Canvas(800, 500).backdrop()
    tp, fn, fp, tn = 4, 1, 5, 90
    total = tp + fn + fp + tn
    acc, prec, rec = (tp + tn) / total, tp / (tp + fp), tp / (tp + fn)
    cv.add(P.card(cv, 14, 24, 424, 452, 20, "a screening test on 100 people", "teal"))
    gx, gy, cw, ch, gap = 124, 150, 140, 118, 6
    cv.add(cv.text(gx + cw + gap / 2, 98, "the test says", 14, 800, cls="il-ink2"))
    cv.add(cv.text(gx + cw / 2, 130, "ill", 15, 800, cls="il-ink"), cv.text(gx + cw * 1.5 + gap, 130, "healthy", 15, 800, cls="il-ink"))
    cv.add(cv.group(cv.text(0, 0, "in fact", 14, 800, cls="il-ink2"), 36, gy + ch + gap / 2, rot=-90))
    cv.add(cv.text(gx - 12, gy + ch / 2 + 5, "ill", 15, 800, anchor="end", cls="il-ink"), cv.text(gx - 12, gy + ch * 1.5 + gap + 5, "healthy", 15, 800, anchor="end", cls="il-ink"))
    cells = [(0, 0, tp, "true positive", "caught", "mint", "TP"), (1, 0, fn, "false negative", "missed", "coral", "FN"),
             (0, 1, fp, "false positive", "false alarm", "sun", "FP"), (1, 1, tn, "true negative", "cleared", "mint", "TN")]
    for cx, cy, n, name, note, color, short in cells:
        x, y = gx + cx * (cw + gap), gy + cy * (ch + gap)
        cv.add(P.lift(cv, x, y, cw, ch, color, 14, 5, hl=False))
        cv.add(cv.text(x + 14, y + 26, short, 14, 800, anchor="start", fill=INK, mono=True))
        cv.add(cv.text(x + cw / 2, y + 68, str(n), 38, 800, fill=INK))
        cv.add(cv.text(x + cw / 2, y + 92, name, 13, 800, fill=INK), cv.text(x + cw / 2, y + 108, "(" + note + ")", 12, 650, fill=INK))
    cv.add(cv.text(gx + cw + gap / 2, gy + 2 * ch + gap + 44, "5 people are really ill, and 95 are healthy", 13.5, 750, cls="il-ink"))
    cv.add(P.badge(cv, 42, 64, 1))
    cv.add(P.card(cv, 454, 24, 332, 452, 20, "three scores", "sun"))
    scores = [("accuracy", "(TP + TN) ÷ all", "(%d + %d) ÷ %d" % (tp, tn, total), acc, "sky"),
              ("precision", "TP ÷ (TP + FP)", "%d ÷ (%d + %d)" % (tp, tp, fp), prec, "coral"),
              ("recall", "TP ÷ (TP + FN)", "%d ÷ (%d + %d)" % (tp, tp, fn), rec, "mint")]
    for i, (name, formula, working, val, color) in enumerate(scores):
        y = 84 + i * 86
        cv.add(cv.text(474, y + 14, name, 16, 800, anchor="start", cls="il-ink"), cv.text(766, y + 14, "%d%%" % round(val * 100), 18, 800, anchor="end", cls="il-ink", mono=True))
        cv.add(cv.rect(474, y + 24, 292, 16, 8, "#FFFFFF", stroke="#9FB3BE", sw=1.4), cv.rect(474, y + 24, max(10, 292 * val), 16, 8, cv.g(color)))
        cv.add(cv.text(474, y + 60, formula, 12.5, 700, anchor="start", cls="il-ink2", mono=True), cv.text(766, y + 60, working, 12.5, 700, anchor="end", cls="il-ink2", mono=True))
    cv.add(P.badge(cv, 480, 66, 2))
    cv.add(cv.rect(474, 350, 292, 100, 14, "#FFE9E5", stroke=RED, sw=2.2))
    cv.add(cv.text(620, 376, "the accuracy paradox", 14.5, 800, fill="#8F2923"))
    cv.add(cv.text(620, 398, "a test that always says “healthy”", 13, 700, fill=INK), cv.text(620, 418, "is 95% accurate, yet its recall is 0%:", 13, 700, fill=INK), cv.text(620, 438, "it finds nobody", 13, 800, fill=INK))
    cv.add(P.badge(cv, 480, 352, 3))
    return figure(
        "confusion-matrix", cv, "A confusion matrix for a screening test, and the three scores worked out from it",
        "A two by two grid. Of 100 people, 5 are really ill and 95 are healthy. The test said ill for 4 of the ill people, which are true positives, "
        "and healthy for 1 of them, a false negative, a case that was missed. It said ill for 5 healthy people, false positives or false alarms, and "
        "healthy for the other 90, true negatives. On the right, three scores. Accuracy is true positives plus true negatives divided by everyone: "
        "94 out of 100, 94 percent. Precision is true positives divided by true positives plus false positives: 4 out of 9, 44 percent, meaning "
        "that fewer than half of the people it flagged were really ill. Recall is true positives divided by true positives plus false negatives: "
        "4 out of 5, 80 percent, the share of the ill people it found. A warning box explains the accuracy paradox: a test that always says healthy "
        "is 95 percent accurate but finds nobody, so its recall is 0 percent.",
        ["The matrix counts every kind of right and wrong answer, not just how many were right.",
         "Precision asks: of those it flagged, how many were right? Recall asks: of the real cases, how many did it find?",
         "When one outcome is rare, accuracy hides the failure, so always look at the matrix."],
        "Which mistake matters more depends on the job: a missed cancer is worse than a false alarm, but a deleted real email is worse than a spam message let through.")
