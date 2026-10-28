"""AI course diagrams, Level 13: reinforcement learning, game search and agents.

The grid world values, the corridor backups, the Q-learning step, the bandit
run and the minimax and alpha-beta trees are computed here, with the same
rules and seeds as the lesson's Python. The robot, the Atari screen, the boat
race and the agent loop are illustrations.
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
from .diagrams_ai5 import _mix
from .diagrams_ai6 import _bubble



def _star(cx, cy, r, fill):
    """A five-pointed star drawn as a path, centred on cx, cy."""
    import math
    pts = []
    for i in range(10):
        a = -math.pi / 2 + i * math.pi / 5
        rr = r if i % 2 == 0 else r * 0.45
        pts.append("%.1f %.1f" % (cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return '<path d="M%sZ" fill="%s"/>' % (" L".join(pts), fill)

def _robot(cx, cy, s=1.0, colour=VIOLET):
    """A friendly robot head, for the agent."""
    w, h = 64 * s, 52 * s
    out = ['<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%.1f"/>'
           % (cx, cy - h / 2.0, cx, cy - h / 2.0 - 14 * s, tv(colour), 3 * s),
           '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (cx, cy - h / 2.0 - 16 * s, 5 * s, AMBER),
           '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" fill="%s"/>'
           % (cx - w / 2.0, cy - h / 2.0, w, h, 14 * s, colour),
           '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" fill="%s"/>'
           % (cx - w / 2.0 + 8 * s, cy - h / 2.0 + 9 * s, w - 16 * s, h - 22 * s, 9 * s, "#1E1B4B"),
           '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (cx - 11 * s, cy - 4 * s, 5 * s, CYAN),
           '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s"/>' % (cx + 11 * s, cy - 4 * s, 5 * s, CYAN),
           '<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="%.1f" fill="%s"/>'
           % (cx - 12 * s, cy + h / 2.0 - 10 * s, 24 * s, 4 * s, 2 * s, WHITE)]
    return "".join(out)


# ===================================================== the RL loop

@diagram("ai-rl-loop")
def _rl_loop():
    """Agent acts; environment answers with a new state and a reward."""
    body = [text(380, 22, "Reinforcement learning: act, see what happens, collect a reward", 12, 650,
                 fill=MUTED)]
    body.append(tint(60, 70, 180, 170, VIOLET, op=0.08, r=16))
    body.append(_robot(150, 150, 1.2))
    body.append(text(150, 228, "the agent", 12, 800, fill=tv(VIOLET)))
    body.append(tint(500, 70, 220, 170, TEAL, op=0.08, r=16))
    # a little world: a maze of cells with a goal
    rows = ["....G", ".##..", "...#.", "A...."]
    for i, r in enumerate(rows):
        for j, ch in enumerate(r):
            x, y = 540 + j * 28, 86 + i * 28
            col = {"#": SLATE, "G": AMBER, "A": VIOLET}.get(ch, FILL2)
            body.append('<rect x="%d" y="%d" width="26" height="26" rx="4" fill="%s"/>' % (x, y, col))
            if ch == "G":
                body.append(_star(x + 13, y + 13, 8, DARK))
    body.append(text(610, 228, "the environment", 12, 800, fill=tv(TEAL)))
    body.append('<path d="M240 110 C 330 60, 420 60, 498 110" fill="none" stroke="%s" stroke-width="3" '
                'class="ai-flow" stroke-dasharray="6 8"/>' % tv(VIOLET))
    body.append(arrow(486, 102, 500, 112, tv(VIOLET), 3))
    body.append(_halo(370, 62, "action: move right", 11, 800))
    body.append('<path d="M498 166 C 420 208, 330 208, 242 166" fill="none" stroke="%s" stroke-width="3" '
                'class="ai-flow" stroke-dasharray="6 8"/>' % tv(TEAL))
    body.append(arrow(254, 173, 240, 165, tv(TEAL), 3))
    body.append(_halo(370, 184, "new state: one cell further on", 11, 800))
    body.append('<path d="M498 204 C 420 272, 330 272, 242 204" fill="none" stroke="%s" stroke-width="3" '
                'class="ai-flow" stroke-dasharray="6 8"/>' % AMBER)
    body.append(arrow(254, 212, 240, 203, AMBER, 3))
    body.append(_halo(370, 278, "reward: −0.1 now, +10 at the star", 11, 800))
    desc = ("A robot, the agent, and a small maze, the environment, with a star as the goal. Arrows "
            "loop between them: the agent sends an action, move right; the environment sends back "
            "the new state, one cell further on, and a reward, minus 0.1 for an ordinary step and "
            "plus 10 at the star. The loop repeats for every step of every episode.")
    return figure("ai-rll", 760, 296, "".join(body), "The reinforcement learning loop", desc,
                  "No one tells the agent the right move: it learns from the rewards alone.")


# ===================================================== discounting

@diagram("ai-discounting")
def _discounting():
    """The same reward of 10, worth less the later it arrives, for two values of γ."""
    body = [text(380, 22, "Discounting: a reward of 10, worth less the longer you wait for it", 12,
                 650, fill=MUTED)]
    pl = Plot(80, 50, 560, 170, (0, 7), (0, 10.5))
    body.append(pl.axes(yticks=(0, 2.5, 5, 7.5, 10), fmt="%g"))
    for k in range(7):
        for g, col, dx in [(0.9, VIOLET, -13), (0.5, PINK, 13)]:
            v = 10 * g ** k
            x = pl.px(k + 0.5) + dx
            body.append('<rect x="%.1f" y="%.1f" width="24" height="%.1f" rx="3" fill="%s"/>'
                        % (x - 12, pl.py(v), pl.py(0) - pl.py(v), col))
            body.append(text(x, pl.py(v) - 4, ("%.2f" % v).rstrip("0").rstrip("."), 8.6, 750, fill=INK))
        body.append(text(pl.px(k + 0.5), pl.py(0) + 15, "%d" % (k + 1), 9.6, 700, fill=MUTED))
    body.append(text(pl.x + pl.w / 2.0, pl.py(0) + 32, "the step on which the reward arrives", 9.6, 700,
                     fill=MUTED))
    body.append('<rect x="660" y="80" width="14" height="14" rx="3" fill="%s"/>' % VIOLET)
    body.append(text(680, 92, "γ = 0.9", 10.5, 800, fill=INK, anchor="start"))
    body.append(text(660, 112, "patient", 9.6, 650, fill=MUTED, anchor="start"))
    body.append('<rect x="660" y="140" width="14" height="14" rx="3" fill="%s"/>' % PINK)
    body.append(text(680, 152, "γ = 0.5", 10.5, 800, fill=INK, anchor="start"))
    body.append(text(660, 172, "short-sighted", 9.6, 650, fill=MUTED, anchor="start"))
    desc = ("Paired bars show what a reward of 10 is worth today if it arrives on step 1 to 7. With "
            "gamma 0.9, in violet: 10, 9, 8.1, 7.29, 6.56, 5.9 and 5.31, a slow decline. With gamma "
            "0.5, in pink: 10, 5, 2.5, 1.25, 0.63, 0.31 and 0.16, falling away fast.")
    return figure("ai-disc", 760, 262, "".join(body), "Discounting future rewards", desc,
                  "Each step of delay multiplies the reward by γ once more.")


# ===================================================== grid world values

_GW = ["....G", ".#.#X", ".....", "S#..."]
_GW_REWARD = {"G": 10, "X": -10}
_GW_MOVES = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}


def _gw_step(r, c, m):
    dr, dc = _GW_MOVES[m]
    nr, nc = r + dr, c + dc
    if 0 <= nr < len(_GW) and 0 <= nc < len(_GW[0]) and _GW[nr][nc] != "#":
        return nr, nc
    return r, c


def _gw_values():
    cells = [(r, c) for r in range(len(_GW)) for c in range(len(_GW[0])) if _GW[r][c] != "#"]
    V = {cell: 0.0 for cell in cells}

    def score(r, c, m):
        nr, nc = _gw_step(r, c, m)
        return _GW_REWARD.get(_GW[nr][nc], -0.1) + 0.9 * V[(nr, nc)]
    for _ in range(40):
        V = {(r, c): (0.0 if _GW[r][c] in _GW_REWARD else max(score(r, c, m) for m in _GW_MOVES))
             for (r, c) in cells}
    pol = {(r, c): max(_GW_MOVES, key=lambda m: score(r, c, m)) for (r, c) in cells
           if _GW[r][c] not in _GW_REWARD}
    return V, pol


@diagram("ai-gridworld-values")
def _gridworld_values():
    """Values found by value iteration, and the policy that follows them."""
    V, pol = _gw_values()
    body = [text(380, 22, "Values and the policy they give: every arrow points uphill in value", 12,
                 650, fill=MUTED)]
    C = 62
    X0, Y0 = 70, 46
    for r, row in enumerate(_GW):
        for c, ch in enumerate(row):
            x, y = X0 + c * C, Y0 + r * C
            if ch == "#":
                body.append('<rect x="%d" y="%d" width="%d" height="%d" rx="6" fill="%s"/>'
                            % (x + 2, y + 2, C - 4, C - 4, SLATE))
                continue
            if ch == "G":
                body.append(solid(x + 2, y + 2, C - 4, C - 4, GREEN, "+10", r=6, size=14))
                continue
            if ch == "X":
                body.append(solid(x + 2, y + 2, C - 4, C - 4, RED, "−10", r=6, size=14))
                continue
            v = V[(r, c)]
            col = plasma(max(0.0, min(1.0, (v - 4.0) / 6.0)))
            body.append('<rect x="%d" y="%d" width="%d" height="%d" rx="6" fill="%s"/>'
                        % (x + 2, y + 2, C - 4, C - 4, col))
            ink = ink_on(col)
            body.append(text(x + C / 2.0, y + 22, "%.1f" % v, 12, 800, fill=ink))
            m = pol[(r, c)]
            dx, dy = {"^": (0, -1), "v": (0, 1), "<": (-1, 0), ">": (1, 0)}[m]
            cx, cy = x + C / 2.0, y + 42
            body.append(arrow(cx - 9 * dx, cy - 9 * dy, cx + 11 * dx, cy + 11 * dy, ink, 2.4))
            if ch == "S":
                body.append(text(x + 10, y + 16, "S", 9, 900, fill=ink, anchor="start"))
    LX = 410
    notes_ = [("Reach G: +10. Fall into X: −10.", INK, 750), ("Every other step: −0.1. γ = 0.9.", INK, 750),
              ("Bright cells are worth more:", MUTED, 650), ("they are closer to the goal.", MUTED, 650),
              ("From S the arrows lead up the", tv(VIOLET), 750), ("left side and along the top,", tv(VIOLET), 750),
              ("keeping away from X.", tv(VIOLET), 750)]
    for k, (s_, col, wgt) in enumerate(notes_):
        body.append(text(LX, 80 + k * 22 + (k // 2) * 8, s_, 10.5, wgt, fill=col, anchor="start"))
    desc = ("A 4 by 5 grid world. The goal G, worth plus 10, is at the top right and a trap X, minus "
            "10, is just below it; grey cells are walls; S is the start at the bottom left. Each open "
            "cell shows its value from value iteration, with gamma 0.9 and a cost of 0.1 per step, "
            "and an arrow for the best move. Values are highest beside the goal, %.1f, and lowest "
            "far from it, %.1f at the start. From S the arrows lead up the left side and along the "
            "top row to G, avoiding X." % (max(V.values()), V[(3, 0)]))
    return figure("ai-gwv", 760, 300, "".join(body), "Values in a grid world", desc,
                  "Computed by value iteration with the same rules as the lesson's Python.")


# ===================================================== Bellman backups, stepped

@diagram("ai-bellman-backup")
def _bellman_backup():
    """Value iteration in a corridor: the goal's value spreads back one cell per sweep."""
    n = 5
    C = 96
    X0, Y0 = 60, 92
    base = [text(380, 22, "Value iteration: each sweep carries the reward one more cell back", 12, 650,
                 fill=MUTED)]
    for k in range(n):
        base.append('<rect x="%d" y="%d" width="%d" height="%d" rx="8" fill="none" stroke="%s" '
                    'stroke-width="1.4"/>' % (X0 + k * C, Y0, C - 8, 70, LINE))
    base.append(solid(X0 + n * C, Y0, C - 8, 70, GREEN, "goal", r=8, size=13))
    base.append(text(X0 + n * C + (C - 8) / 2.0, Y0 + 92, "entering pays 10", 9.6, 700, fill=MUTED))
    base.append(text(380, 210, "V(cell) = 0.9 × V(next cell), or 10 for the cell next to the goal", 10.5,
                     750, fill=INK))
    stages, labels = [], []
    V = [0.0] * n
    for sweep in range(1, n + 1):
        new = []
        for k in range(n):
            new.append(10.0 if k == n - 1 else 0.9 * V[k + 1])
        V = new
        s = []
        for k in range(n):
            v = V[k]
            if v <= 0:
                s.append(text(X0 + k * C + (C - 8) / 2.0, Y0 + 42, "0", 16, 800, fill=MUTED))
                continue
            col = plasma(0.25 + 0.7 * v / 10.0)
            s.append('<rect x="%d" y="%d" width="%d" height="%d" rx="8" fill="%s"/>'
                     % (X0 + k * C, Y0, C - 8, 70, col))
            s.append(text(X0 + k * C + (C - 8) / 2.0, Y0 + 42, ("%.2f" % v).rstrip("0").rstrip("."), 16, 800,
                          fill=ink_on(col)))
        front = n - sweep
        s.append(path("M%d %d C %d %d, %d %d, %d %d" % (X0 + (front + 1) * C + 10, Y0 - 6, X0 + (front + 1) * C - 10,
                                                       Y0 - 34, X0 + front * C + 60, Y0 - 34, X0 + front * C + 44, Y0 - 6),
                      stroke=AMBER, w=2.4))
        s.append(arrow(X0 + front * C + 50, Y0 - 14, X0 + front * C + 44, Y0 - 4, AMBER, 2.4))
        lab = "Sweep %d: values %s" % (sweep, ", ".join(("%.2f" % v).rstrip("0").rstrip(".") for v in V))
        stages.append(step(sweep, "".join(s), lab))
        labels.append(lab)
    desc = ("A stepped corridor of five cells leading to a goal that pays 10 when entered, with gamma "
            "0.9. Every value starts at 0. Sweep 1: the cell next to the goal becomes 10. Sweep 2: "
            "the cell before it becomes 9. Sweep 3: 8.1. Sweep 4: 7.29. Sweep 5: the first cell "
            "becomes 6.56. Each sweep carries the reward one cell further back, shown by an amber "
            "arrow.")
    return figure_steps("ai-bell", 760, 226, "".join(base), stages, "Value iteration in a corridor", desc,
                        "After enough sweeps the values stop changing: they satisfy the Bellman equation.",
                        labels=labels)


# ===================================================== a Q-learning step

@diagram("ai-q-update")
def _q_update():
    """The worked Q-learning update, as a flow of numbers."""
    body = [text(380, 22, "One Q-learning update, worked through", 12, 650, fill=MUTED)]

    def qrow(x, y, name, vals, hi=None):
        out = [text(x - 8, y + 21, name, 11, 800, fill=INK, anchor="end")]
        for k, (lab, v) in enumerate(vals):
            col = AMBER if k == hi else FILL2
            out.append('<rect x="%d" y="%d" width="76" height="32" rx="6" fill="%s" stroke="%s"/>'
                       % (x + k * 82, y, col, LINE))
            out.append(text(x + k * 82 + 38, y + 14, lab, 8.6, 700, fill=DARK if k == hi else MUTED))
            out.append(text(x + k * 82 + 38, y + 27, ("%.1f" % v).replace("-", "−"), 11, 800,
                            fill=DARK if k == hi else INK))
        return "".join(out)
    body.append(qrow(90, 50, "Q(s, ·)", [("left", 0.5), ("right", 2.0)], hi=1))
    body.append(qrow(90, 120, "Q(s′, ·)", [("left", 1.5), ("right", 6.0)], hi=1))
    body.append(text(250, 101, "took “right”, reward −1", 9.6, 750, fill=tv(VIOLET), anchor="end"))
    body.append(arrow(210, 86, 210, 116, tv(VIOLET), 1.8))
    boxes = [(330, "target", "−1 + 0.9 × 6.0 = 4.4", BLUE),
             (330, "error", "4.4 − 2.0 = 2.4", PINK),
             (330, "new Q(s, right)", "2.0 + 0.5 × 2.4 = 3.2", GREEN)]
    for k, (x, title, sum_, col) in enumerate(boxes):
        y = 44 + k * 62
        body.append('<rect x="%d" y="%d" width="230" height="48" rx="10" fill="%s" fill-opacity="0.12" '
                    'stroke="%s" stroke-width="1.6"/>' % (x, y, col, tv(col)))
        body.append(text(x + 115, y + 19, title, 10, 800, fill=tv(col)))
        body.append(text(x + 115, y + 37, sum_, 12, 800, fill=INK, mono=True))
        if k < 2:
            body.append(arrow(x + 115, y + 50, x + 115, y + 60, LINE, 1.4))
    body.append(arrow(258, 136, 328, 70, LINE, 1.3))
    body.append(arrow(258, 66, 328, 130, LINE, 1.3))
    LX = 590
    for k, (s_, col, wgt) in enumerate([("α = 0.5: move halfway", INK, 750), ("towards the target", INK, 750),
                                        ("γ = 0.9: the future", MUTED, 650), ("is worth a bit less", MUTED, 650),
                                        ("A positive error means", tv(GREEN), 750),
                                        ("“better than expected”", tv(GREEN), 750)]):
        body.append(text(LX, 64 + k * 20 + (k // 2) * 10, s_, 10.5, wgt, fill=col, anchor="start"))
    desc = ("Two rows of Q-values. In state s, Q(s, left) is 0.5 and Q(s, right) is 2.0. The agent took "
            "right, received a reward of minus 1, and landed in s prime, where Q is 1.5 for left and "
            "6.0 for right, the best. The target is minus 1 plus 0.9 times 6.0, which is 4.4. The "
            "error is 4.4 minus 2.0, which is 2.4. With alpha 0.5, the new Q(s, right) is 2.0 plus "
            "0.5 times 2.4, which is 3.2.")
    return figure("ai-qup", 760, 236, "".join(body), "A Q-learning update", desc,
                  "The same three lines of arithmetic run millions of times in a real agent.")


# ===================================================== bandit

def _bandit_run():
    rnd = random.Random(1)
    true_payout = [0.2, 0.5, 0.35, 0.8, 0.1]
    est, pulls = [0.0] * 5, [0] * 5
    for _ in range(1000):
        if rnd.random() < 0.1:
            arm = rnd.randrange(5)
        else:
            arm = max(range(5), key=lambda a: est[a])
        r = 1 if rnd.random() < true_payout[arm] else 0
        pulls[arm] += 1
        est[arm] += (r - est[arm]) / pulls[arm]
    return true_payout, est, pulls


@diagram("ai-bandit")
def _bandit():
    """Five slot machines: true payout, estimate and pulls after ε-greedy."""
    true_p, est, pulls = _bandit_run()
    body = [text(380, 22, "A five-armed bandit after 1,000 pulls with ε-greedy (ε = 0.1)", 12, 650,
                 fill=MUTED)]
    cols = [BLUE, VIOLET, TEAL, PINK, ORANGE]
    for k in range(5):
        x = 60 + k * 136
        body.append(cube(x, 48, 76, 66, 14, cols[k]))
        for j in range(3):
            body.append('<rect x="%d" y="62" width="18" height="26" rx="3" fill="%s"/>' % (x + 8 + j * 21, WHITE))
            body.append(text(x + 17 + j * 21, 80, "7", 11, 900, fill=cols[k]) if k == 3 else _star(x + 17 + j * 21, 76, 6, cols[k]))
        body.append(text(x + 38, 106, "machine %d" % k, 9.4, 800, fill=WHITE))
        base, top = 250, 140
        hpx = (base - top)
        body.append('<rect x="%d" y="%d" width="34" height="%d" rx="3" fill="%s"/>' % (x + 21, top, hpx, FILL2))
        body.append('<rect x="%d" y="%.1f" width="34" height="%.1f" rx="3" fill="%s"/>'
                    % (x + 21, base - hpx * est[k], hpx * est[k], cols[k]))
        ty = base - hpx * true_p[k]
        body.append(line(x + 14, ty, x + 62, ty, stroke=INK, w=2.2, dash="4 3"))
        body.append(text(x + 38, 268, "est %.2f · true %.2f" % (est[k], true_p[k]), 9, 750, fill=INK))
        body.append(text(x + 38, 284, "%d pulls" % pulls[k], 9.6, 800, fill=tv(cols[k])))
    body.append(text(380, 306, "Machine 1 was tried only %d times, so its estimate (%.2f) is well below its true "
                     "rate (%.2f)." % (pulls[1], est[1], true_p[1]), 10, 700, fill=MUTED))
    desc = ("Five slot machines. Under each, a bar shows the estimated payout after 1,000 pulls with "
            "epsilon-greedy, and a dashed line the true payout. Machine 0: estimate %.2f, true %.2f, "
            "%d pulls. Machine 1: %.2f, %.2f, %d pulls. Machine 2: %.2f, %.2f, %d pulls. Machine 3, "
            "the best: %.2f, %.2f, %d pulls. Machine 4: %.2f, %.2f, %d pulls. The best machine got "
            "most of the pulls, but machine 1 was tried so rarely that its estimate is well below "
            "its true rate."
            % tuple(v for k in range(5) for v in (est[k], true_p[k], pulls[k])))
    return figure("ai-band", 760, 318, "".join(body), "A multi-armed bandit", desc,
                  "Exploit too soon and you misjudge the options you rarely try.")


# ===================================================== DQN

_BREAKOUT = ["RRRRRRRRRRRR",
             "OOOOOOOOOOOO",
             "YYYYYYYYYYYY",
             "GGGGG..GGGGG",
             "BBB......BBB",
             "............",
             "............",
             "......W.....",
             "............",
             "............",
             "....PPPP....",
             "............"]
_BREAKOUT_PAL = {"R": "#EF4444", "O": "#F97316", "Y": "#FACC15", "G": "#22C55E", "B": "#3B82F6",
                 "W": "#FFFFFF", "P": "#E879F9", ".": "#0F172A"}


@diagram("ai-dqn")
def _dqn():
    """Pixels in, a Q-value for each action out."""
    body = [text(380, 22, "A deep Q-network: the screen goes in, a Q-value for every action comes out",
                 12, 650, fill=MUTED)]
    s = 11
    for i, row in enumerate(_BREAKOUT):
        for j, ch in enumerate(row):
            body.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s"/>'
                        % (30 + j * s, 56 + i * s, s + 0.2, s + 0.2, _BREAKOUT_PAL[ch]))
    body.append(text(96, 210, "the game screen", 10, 800, fill=INK))
    body.append(text(96, 224, "(the state)", 9.4, 650, fill=MUTED))
    body.append(arrow(168, 122, 192, 122, LINE, 1.6))
    for k, (h, col) in enumerate([(120, BLUE), (90, INDIGO), (64, VIOLET)]):
        body.append(cube(198 + k * 54, 122 - h / 2.0, 28, h, 14, col))
    body.append(text(268, 210, "convolutional layers", 10, 800, fill=tv(BLUE)))
    body.append(text(268, 224, "see the bricks, ball, paddle", 9.4, 650, fill=MUTED))
    body.append(arrow(366, 122, 392, 122, LINE, 1.6))
    body.append(cube(398, 82, 40, 80, 14, PINK))
    body.append(text(426, 210, "dense layers", 10, 800, fill=tv(PINK)))
    body.append(arrow(458, 122, 484, 122, LINE, 1.6))
    acts = [("move left", 2.1), ("stay still", 3.4), ("move right", 5.8)]
    for k, (name, q) in enumerate(acts):
        y = 76 + k * 40
        best = k == 2
        body.append('<rect x="566" y="%d" width="%.1f" height="26" rx="5" fill="%s"/>'
                    % (y, 22 * q, AMBER if best else FILL2))
        body.append(text(566 + 22 * q + 8, y + 18, "Q = %.1f" % q, 10, 800, fill=INK, anchor="start"))
        body.append(text(558, y + 18, name, 10, 750, fill=INK, anchor="end"))
    body.append(text(640, 210, "pick the highest:", 10, 800, fill=tv(ORANGE)))
    body.append(text(640, 224, "move right", 10, 800, fill=tv(ORANGE)))
    desc = ("A pixel game screen with rows of coloured bricks, a ball and a paddle goes into "
            "convolutional layers, then dense layers, which output one Q-value per action: move left "
            "2.1, stay still 3.4, move right 5.8. The agent picks the highest, move right. The "
            "Q-values here are illustrative.")
    return figure("ai-dqn", 760, 240, "".join(body), "A deep Q-network", desc,
                  "One network replaces a table with more rows than there are atoms in the universe.")


# ===================================================== reward hacking

@diagram("ai-reward-hacking")
def _reward_hacking():
    """The intended race, and the loop the agent found instead."""
    body = [text(380, 22, "Reward hacking: the agent maximised points, not the race", 12, 650,
                 fill=MUTED)]
    cx, cy, rx, ry = 300, 160, 230, 104
    body.append('<ellipse cx="%d" cy="%d" rx="%d" ry="%d" fill="%s" fill-opacity="0.25"/>' % (cx, cy, rx, ry, SKY))
    body.append('<ellipse cx="%d" cy="%d" rx="%d" ry="%d" fill="%s"/>' % (cx, cy, rx - 56, ry - 46, "#86EFAC"))
    body.append('<ellipse cx="%d" cy="%d" rx="%d" ry="%d" fill="none" stroke="%s" stroke-width="2" '
                'stroke-dasharray="8 6"/>' % (cx, cy, rx - 28, ry - 23, tv(GREEN)))
    body.append(line(cx, cy - ry, cx, cy - ry + 46, stroke=INK, w=4, dash="4 4"))
    body.append(text(cx, cy - ry - 8, "finish", 10, 800, fill=INK))
    body.append(text(cx, cy + 4, "intended: race round and finish", 10.5, 800, fill=DARK))
    lx, ly = 130, 220
    for k, (dx, dy) in enumerate([(-22, -10), (16, -18), (6, 16)]):
        body.append(circle(lx + dx, ly + dy, 7, fill=AMBER, stroke=FILL, w=1.5))
        body.append(text(lx + dx, ly + dy + 3.5, "+", 9, 900, fill=DARK))
    body.append('<ellipse cx="%d" cy="%d" rx="44" ry="30" fill="none" stroke="%s" stroke-width="3" '
                'class="ai-flow" stroke-dasharray="6 8"/>' % (lx, ly, tv(RED)))
    body.append('<path d="M%d %d l 10 -6 l 0 12 z" fill="%s"/>' % (lx + 40, ly - 12, tv(RED)))
    body.append(text(lx + 4, ly + 54, "learned: circle the lagoon", 10, 800, fill=tv(RED)))
    body.append(text(lx + 4, ly + 68, "hitting the same targets", 10, 800, fill=tv(RED)))
    LX = 560
    rows = [("Reward given", "points scored", INK), ("Designer wanted", "win the race", tv(GREEN)),
            ("Agent learned", "loop for points", tv(RED)), ("Its score", "beat human players", INK),
            ("Races finished", "none", tv(RED))]
    for k, (a, b, col) in enumerate(rows):
        body.append(text(LX, 74 + k * 40, a, 9.6, 700, fill=MUTED, anchor="start"))
        body.append(text(LX, 90 + k * 40, b, 11, 800, fill=col, anchor="start"))
    desc = ("A race track around a grassy island, with a finish line at the top and a dashed green "
            "route showing the intended race. In a lagoon at the lower left, a red looping arrow "
            "circles past three bonus targets again and again. Notes: the reward given was points "
            "scored; the designer wanted the race won; the agent learned to loop for points; its "
            "score beat human players; races finished: none.")
    return figure("ai-rhack", 760, 290, "".join(body), "Reward hacking", desc,
                  "Based on OpenAI's 2016 CoastRunners experiment: the reward said points, so the "
                  "agent chased points.")


# ===================================================== game tree

def _ttt(x, y, s, cells, hi=None):
    out = ['<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="4" fill="%s" stroke="%s"/>'
           % (x, y, 3 * s, 3 * s, FILL, LINE)]
    for k in (1, 2):
        out.append(line(x + k * s, y + 3, x + k * s, y + 3 * s - 3, stroke=LINE, w=1.2))
        out.append(line(x + 3, y + k * s, x + 3 * s - 3, y + k * s, stroke=LINE, w=1.2))
    for i, ch in enumerate(cells):
        if ch == " ":
            continue
        r, c = divmod(i, 3)
        col = tv(PINK) if ch == "X" else tv(BLUE)
        weight = 900 if i == hi else 800
        out.append(text(x + c * s + s / 2.0, y + r * s + s * 0.72, ch, s * 0.7, weight, fill=col))
    return "".join(out)


@diagram("ai-game-tree")
def _game_tree():
    """A noughts and crosses game tree, three levels deep."""
    body = [text(380, 22, "A game tree: every position branches into every legal move", 12, 650,
                 fill=MUTED)]
    S = 14
    body.append(_ttt(359, 40, S, "         "))
    kids = [(4, 130), (0, 380), (1, 630)]
    for idx, (move, kx) in enumerate(kids):
        b = [" "] * 9
        b[move] = "X"
        body.append(line(380, 84, kx, 116, stroke=LINE, w=1.4))
        body.append(_ttt(kx - 21, 118, S, "".join(b), hi=move))
        replies = [m for m in range(9) if m != move][:3]
        for j, rep in enumerate(replies):
            bb = list(b)
            bb[rep] = "O"
            gx = kx - 80 + j * 80
            body.append(line(kx, 162, gx, 196, stroke=LINE, w=1.2))
            body.append(_ttt(gx - 21, 198, S, "".join(bb), hi=rep))
        body.append(text(kx + 112, 222, "…", 16, 800, fill=MUTED))
    body.append(text(560, 70, "…and 6 more first moves", 10, 700, fill=MUTED))
    body.append(text(380, 262, "X has 9 first moves; O has 8 replies to each (72 positions); then X has 7 "
                     "more (504 positions)", 10, 750, fill=tv(VIOLET)))
    body.append('<text x="380" y="282" text-anchor="middle" font-size="10.5" font-weight="750" fill="%s">'
                'Whole game: 255,168 possible games. Chess: about 10<tspan dy="-5" font-size="8">120</tspan>'
                '<tspan dy="5">. Go: far more.</tspan></text>' % INK)
    desc = ("An empty noughts and crosses board at the top branches into the first moves for X: three "
            "are drawn, centre, corner and edge, with six more indicated. Each of those branches into "
            "O's replies, three drawn for each. Labels: X to move has 9 choices; O has 8 replies to "
            "each, 72 positions; X then has 7, 504 positions. The whole game has 255,168 possible "
            "games; chess has about 10 to the power 120; Go far more.")
    return figure("ai-gtree", 760, 294, "".join(body), "A game tree", desc,
                  "The tree grows by a factor equal to the number of legal moves at every level.")


# ===================================================== minimax and alpha-beta

_LEAVES = [[3, 12, 8], [2, 4, 6], [14, 5, 2]]


def _tree_layout():
    root = (380, 66)
    mins = [(150, 156), (380, 156), (610, 156)]
    leaves = [[(mx - 64 + 64 * j, 246) for j in range(3)] for mx, _ in mins]
    return root, mins, leaves


def _node(x, y, kind, label, col, dim=False):
    op = ' opacity="0.35"' if dim else ""
    if kind == "max":
        shape = '<polygon points="%d,%d %d,%d %d,%d" fill="%s"%s/>' % (x, y - 20, x + 22, y + 14, x - 22, y + 14, col, op)
        ty = y + 8
    elif kind == "min":
        shape = '<polygon points="%d,%d %d,%d %d,%d" fill="%s"%s/>' % (x - 22, y - 14, x + 22, y - 14, x, y + 20, col, op)
        ty = y + 2
    else:
        shape = '<rect x="%d" y="%d" width="34" height="28" rx="6" fill="%s"%s/>' % (x - 17, y - 14, col, op)
        ty = y + 5
    return shape + (text(x, ty, label, 12, 800, fill=WHITE if not dim else MUTED) if label != "" else "")


@diagram("ai-minimax")
def _minimax():
    """Leaves, then MIN values, then the MAX root."""
    root, mins, leaves = _tree_layout()
    base = [text(380, 22, "Minimax: MAX takes the highest child, MIN takes the lowest", 12, 650,
                 fill=MUTED)]
    for (mx, my), lv in zip(mins, leaves):
        base.append(line(root[0], root[1] + 14, mx, my - 14, stroke=LINE, w=1.4))
        for (lx, ly) in lv:
            base.append(line(mx, my + 20, lx, ly - 14, stroke=LINE, w=1.2))
    for (mx, my), lv, vals in zip(mins, leaves, _LEAVES):
        for (lx, ly), v in zip(lv, vals):
            base.append(_node(lx, ly, "leaf", str(v), SLATE))
    base.append(text(14, 70, "MAX", 11, 800, fill=tv(BLUE), anchor="start"))
    base.append(text(14, 160, "MIN", 11, 800, fill=tv(PINK), anchor="start"))
    base.append(text(14, 250, "leaves", 11, 800, fill=MUTED, anchor="start"))
    stages, labels = [], []
    s1 = [_node(mx, my, "min", "", PINK) for mx, my in mins] + [_node(root[0], root[1], "max", "", BLUE)]
    lab1 = "The game's final scores are known at the leaves: 3, 12, 8; 2, 4, 6; 14, 5, 2"
    stages.append(step(1, "".join(s1), lab1))
    labels.append(lab1)
    mv = [min(v) for v in _LEAVES]
    s2 = [_node(mx, my, "min", str(v), PINK) for (mx, my), v in zip(mins, mv)] + [_node(root[0], root[1], "max", "", BLUE)]
    for (mx, my), lv, vals in zip(mins, leaves, _LEAVES):
        j = vals.index(min(vals))
        s2.append(line(mx, my + 20, lv[j][0], lv[j][1] - 14, stroke=tv(PINK), w=3.2))
    lab2 = "Each MIN node takes its lowest child: 3, 2 and 2"
    stages.append(step(2, "".join(s2), lab2))
    labels.append(lab2)
    s3 = list(s2[:3]) + [_node(root[0], root[1], "max", str(max(mv)), BLUE)] + s2[4:]
    s3.append(line(root[0], root[1] + 14, mins[0][0], mins[0][1] - 14, stroke=tv(BLUE), w=3.4))
    lab3 = "MAX takes the highest: 3, so the left move is best, and MAX is guaranteed at least 3"
    stages.append(step(3, "".join(s3), lab3))
    labels.append(lab3)
    desc = ("A stepped game tree. MAX, a blue triangle at the top, has three moves, each leading to "
            "a pink MIN node with three leaves. The leaves score 3, 12 and 8; 2, 4 and 6; and 14, 5 "
            "and 2. Each MIN node takes its lowest leaf: 3, 2 and 2. MAX takes the highest of those, "
            "3, so it chooses the left move and is guaranteed a score of at least 3.")
    return figure_steps("ai-mmx", 760, 276, "".join(base), stages, "Minimax", desc,
                        "The answer at the root is what MAX can guarantee against perfect play.",
                        labels=labels)


@diagram("ai-alpha-beta")
def _alpha_beta():
    """The same tree, with the two branches alpha-beta never looks at."""
    root, mins, leaves = _tree_layout()
    body = [text(380, 22, "Alpha-beta pruning: the same answer, without looking at everything", 12, 650,
                 fill=MUTED)]
    pruned = {(1, 1), (1, 2)}
    for i, ((mx, my), lv) in enumerate(zip(mins, leaves)):
        body.append(line(root[0], root[1] + 14, mx, my - 14, stroke=LINE, w=1.4))
        for j, (lx, ly) in enumerate(lv):
            cut = (i, j) in pruned
            body.append(line(mx, my + 20, lx, ly - 14, stroke=LINE, w=1.2, dash="4 4" if cut else None))
            body.append(_node(lx, ly, "leaf", str(_LEAVES[i][j]), SLATE, dim=cut))
            if cut:
                body.append(text(lx, ly + 34, "skipped", 9, 800, fill=tv(RED)))
    vals = [3, 2, 2]
    for (mx, my), v in zip(mins, vals):
        body.append(_node(mx, my, "min", ("≤ 2" if v == 2 and mx == 380 else str(v)), PINK))
    body.append(_node(root[0], root[1], "max", "3", BLUE))
    body.append(_bubble(150, 292, 460, 52, RED, ["MAX already has 3 from the left. The middle MIN node's first leaf is 2,",
                                                  "so it is worth at most 2, and its other leaves cannot matter."]))
    body.append(text(380, 366, "Minimax looked at 9 leaves; alpha-beta needed 7, and chose the same move.",
                     10.5, 750, fill=INK))
    desc = ("The same game tree as the minimax figure. After the left MIN node's value of 3 is known, "
            "the middle MIN node's first leaf is 2, so that node will be worth at most 2, which is "
            "worse for MAX than the 3 it already has. Its other two leaves, 4 and 6, are skipped, drawn "
            "faintly with dashed branches. The root still gets 3. Minimax looked at 9 leaves; "
            "alpha-beta needed only 7 and chose the same move.")
    return figure("ai-abp", 760, 378, "".join(body), "Alpha-beta pruning", desc,
                  "In big games, good move ordering lets alpha-beta skip most of the tree.")


# ===================================================== MCTS

def _mtree(x0, y0, nodes, edges, hi_nodes=(), hi_edges=(), new=None, labels=None):
    out = []
    for (a, b) in edges:
        (ax, ay), (bx, by) = nodes[a], nodes[b]
        hi = (a, b) in hi_edges
        out.append(line(x0 + ax, y0 + ay, x0 + bx, y0 + by, stroke=AMBER if hi else LINE, w=3 if hi else 1.4))
    for k, (x, y) in enumerate(nodes):
        if new is not None and k == new:
            out.append(circle(x0 + x, y0 + y, 13, fill=GREEN, stroke=FILL, w=2))
        else:
            out.append(circle(x0 + x, y0 + y, 13, fill=VIOLET if k in hi_nodes else SLATE, stroke=FILL, w=2))
        if labels and k in labels:
            out.append(text(x0 + x, y0 + y + 3.5, labels[k], 8, 800, fill=WHITE))
    return "".join(out)


@diagram("ai-mcts")
def _mcts():
    """Selection, expansion, simulation, backpropagation."""
    body = [text(380, 22, "Monte Carlo tree search: four phases, repeated thousands of times", 12, 650,
                 fill=MUTED)]
    nodes = [(80, 30), (40, 86), (120, 86), (20, 142), (60, 142), (110, 142)]
    edges = [(0, 1), (0, 2), (1, 3), (1, 4), (2, 5)]
    lab_before = {0: "5/9", 1: "3/5", 2: "2/4", 3: "1/2", 4: "2/3", 5: "1/2"}
    lab_after = {0: "6/10", 1: "4/6", 2: "2/4", 3: "1/2", 4: "3/4", 5: "1/2", 6: "1/1"}
    phases = [("1. Selection", "follow the best-looking", "children down the tree", BLUE),
              ("2. Expansion", "add one new move", "as a new node", GREEN),
              ("3. Simulation", "play quick random moves", "to the end of the game", ORANGE),
              ("4. Backpropagation", "add the result to every", "node on the path", PINK)]
    for k, (title, l1, l2, col) in enumerate(phases):
        x0 = 30 + k * 182
        body.append(tint(x0 - 12, 40, 172, 346, col, op=0.06, r=12))
        body.append(text(x0 + 74, 62, title, 11, 800, fill=tv(col)))
        body.append(text(x0 + 74, 80, l1, 9.4, 700, fill=INK))
        body.append(text(x0 + 74, 93, l2, 9.4, 700, fill=INK))
        ns = list(nodes)
        es = list(edges)
        new = None
        if k >= 1:
            ns.append((80, 198))
            es.append((4, 6))
            new = 6 if k >= 1 else None
        hi_e = {(0, 1), (1, 4)} if k == 0 else ({(0, 1), (1, 4), (4, 6)} if k == 3 else set())
        hi_n = {0, 1, 4} if k in (0, 3) else set()
        labels = lab_after if k == 3 else lab_before
        body.append(_mtree(x0, 100, ns, es, hi_n, hi_e, new=new if k >= 1 else None, labels=labels))
        if k == 2:
            pts = []
            for j in range(8):
                pts.append("%d %d" % (x0 + 80 + (8 if j % 2 else -8), 100 + 214 + j * 6))
            body.append(path("M" + " L".join(pts), stroke=tv(ORANGE), w=2, dash="3 3"))
            body.append(solid(x0 + 50, 100 + 258, 60, 22, ORANGE, "win", r=6, size=10))
    desc = ("Four panels show the same small tree, each node labelled wins over visits. 1, Selection: "
            "a path from the root, 5 out of 9, through 3 out of 5 to 2 out of 3, is highlighted. 2, "
            "Expansion: a new green node is added below. 3, Simulation: a dotted zig-zag of quick "
            "random moves runs from the new node to the end of the game, a win. 4, Backpropagation: "
            "every node on the path gains a win and a visit, so the root becomes 6 out of 10.")
    return figure("ai-mcts", 760, 396, "".join(body), "Monte Carlo tree search", desc,
                  "After thousands of iterations, the most-visited move at the root is played.")


# ===================================================== AlphaZero loop

@diagram("ai-alphazero-loop")
def _alphazero_loop():
    """Network guides search; search plays games; games train the network."""
    body = [text(380, 22, "AlphaZero: a loop that teaches itself", 12, 650, fill=MUTED)]
    cx, cy, R = 380, 166, 112
    items = [(-90, "neural network", "suggests moves, judges positions", VIOLET),
             (30, "tree search", "plays better moves than the network alone", BLUE),
             (150, "self-play games", "millions of them, against itself", TEAL)]
    for ang, title, sub, col in items:
        a = math.radians(ang)
        x, y = cx + R * math.cos(a) * 1.9, cy + R * math.sin(a)
        body.append(solid(x - 118, y - 26, 236, 52, col, title, sub, r=12, size=12, sub_size=9))
    for a0, a1, lab in [(-60, 0, "guides"), (60, 120, "generates"), (180, 240, "train the network")]:
        pts = []
        for i in range(21):
            a = math.radians(a0 + (a1 - a0) * i / 20.0)
            pts.append((cx + R * 1.25 * math.cos(a), cy + R * 0.82 * math.sin(a)))
        d = "M" + " L".join("%.1f %.1f" % p for p in pts)
        body.append('<path d="%s" fill="none" stroke="%s" stroke-width="3" class="ai-flow" '
                    'stroke-dasharray="6 8"/>' % (d, AMBER))
        (x1, y1), (x2, y2) = pts[-2], pts[-1]
        body.append(arrow(x1, y1, x2, y2, AMBER, 3))
        am = math.radians((a0 + a1) / 2.0)
        lx, ly = cx + R * 1.5 * math.cos(am), cy + R * 1.05 * math.sin(am)
        body.append(_halo(lx, ly, lab, 10.5, 800))
    body.append(text(cx, cy + 4, "only the rules", 11, 800, fill=INK))
    body.append(text(cx, cy + 20, "are given", 11, 800, fill=INK))
    body.append(text(380, 318, "Each lap makes the network better, which makes the next search stronger: "
                     "superhuman at chess within 24 hours.", 10, 700, fill=MUTED))
    desc = ("A loop of three boxes joined by amber arrows. A violet neural network, which suggests moves "
            "and judges positions, guides a blue tree search, which plays better moves than the "
            "network alone. The search generates teal self-play games, millions of them against "
            "itself. The games train the network on the search's moves and the winners, which brings "
            "the loop back to the network. In the centre: only the rules are given.")
    return figure("ai-azero", 760, 330, "".join(body), "The AlphaZero loop", desc,
                  "Self-play needs no human data, so it can keep improving beyond human play.")


# ===================================================== agent loop

@diagram("ai-agent-loop")
def _agent_loop():
    """Think, act, observe, with tools in a sandbox."""
    body = [text(380, 22, "An AI agent: think, act, observe, repeat until the goal is reached", 12, 650,
                 fill=MUTED)]
    body.append(_bubble(250, 40, 260, 34, SLATE, ["goal: “find and fix the failing test”"]))
    body.append(arrow(380, 76, 380, 96, LINE, 1.6))
    pos = {"think": (380, 128), "act": (560, 228), "observe": (200, 228)}
    body.append(solid(282, 100, 196, 56, VIOLET, "think", "language model plans the next step", r=14, size=13, sub_size=8.6))
    body.append(solid(480, 200, 160, 56, ORANGE, "act", "call a tool", r=14, size=13, sub_size=9))
    body.append(solid(120, 200, 160, 56, TEAL, "observe", "read the result", r=14, size=13, sub_size=9))
    for (a, b) in [((470, 150), (540, 196)), ((478, 238), (284, 238)), ((200, 198), (284, 150))]:
        body.append('<path d="M%d %d L %d %d" fill="none" stroke="%s" stroke-width="3" class="ai-flow" '
                    'stroke-dasharray="6 8"/>' % (a[0], a[1], b[0], b[1], AMBER))
        body.append(arrow(a[0] + (b[0] - a[0]) * 0.92, a[1] + (b[1] - a[1]) * 0.92, b[0], b[1], AMBER, 3))
    # sandbox with tools
    body.append('<rect x="500" y="276" width="244" height="64" rx="12" fill="none" stroke="%s" '
                'stroke-width="2" stroke-dasharray="6 4"/>' % tv(RED))
    body.append(text(512, 292, "sandbox, limited permissions", 9, 800, fill=tv(RED), anchor="start"))
    for k, name in enumerate(["search", "run code", "edit files", "tests"]):
        body.append(tint(510 + k * 58, 302, 52, 26, ORANGE, name, r=6, size=8.6, op=0.16))
    body.append(arrow(560, 258, 560, 274, LINE, 1.4))
    body.append(tint(24, 100, 150, 40, BLUE, "memory: notes,", "files, retrieval", r=10, size=10, sub_size=9))
    body.append(line(174, 120, 280, 124, stroke=tv(BLUE), w=1.4, dash="4 3"))
    body.append(_bubble(548, 86, 196, 50, GREEN, ["done: report the fix,", "or stop at the step limit"]))
    body.append(arrow(480, 116, 544, 110, tv(GREEN), 1.8))
    desc = ("A goal, find and fix the failing test, feeds a loop of three boxes joined by amber arrows: "
            "think, where the language model plans the next step; act, which calls a tool; and "
            "observe, which reads the result back. The tools, search, run code, edit files and tests, "
            "sit inside a red dashed sandbox with limited permissions. A memory of notes, files and "
            "retrieval connects to think. An exit arrow leads to done: report the fix, or stop at the "
            "step limit.")
    return figure("ai-agent", 760, 348, "".join(body), "The agent loop", desc,
                  "The model decides; the program acts, inside limits a person has set.")
