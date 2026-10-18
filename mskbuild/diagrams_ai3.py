"""AI course diagrams, Levels 6 and 7: the artificial neuron, activation
functions, neural networks and backpropagation.

As in diagrams_ai2, every number a figure shows is computed here from the
same formulas the lessons use, so a picture and its worked example agree.
"""
import math

from .diagrams import diagram
from .svg import figure, figure_steps, step, text, line, path, circle
from .diagrams_ai_kit import (INK, MUTED, FILL, FILL2, LINE, VIOLET, PINK, BLUE,
                              TEAL, GREEN, ORANGE, RED, INDIGO, AMBER, LIME,
                              CYAN, ROSE, SKY, PURPLE, SLATE, WHITE, DARK, tv,
                              solid, tint, grad, glow, plasma, diverging, ink_on,
                              arrow, neuron, mlp, cube)
from .diagrams_ai2 import Plot, _solve, _halo, _ball, _square


def _sig(z):
    return 1 / (1 + math.exp(-z))


def _gelu(z):
    return 0.5 * z * (1 + math.erf(z / math.sqrt(2)))


# ================================== Level 6: biological and artificial

@diagram("ai-neuron-bio")
def _neuron_bio():
    """A brain cell beside the artificial neuron it inspired, part by part."""
    body = [text(380, 22, "The brain cell, and the maths it inspired", 12, 650, fill=MUTED)]
    body.append(tint(20, 38, 340, 250, PINK, op=0.06, r=14))
    body.append(text(190, 60, "Biological neuron", 11.5, 800, fill=tv(PINK)))
    # dendrites
    cx, cy = 130, 168
    dend = [(-1, -1), (-1.2, -0.2), (-1.1, 0.7), (-0.4, -1.3), (-0.45, 1.0)]
    for dx, dy in dend:
        x1, y1 = cx + dx * 34, cy + dy * 34
        x2, y2 = cx + dx * 78, cy + dy * 62
        body.append(path("M%.1f %.1f Q %.1f %.1f %.1f %.1f" % (x1, y1, (x1 + x2) / 2 + dy * 8,
                                                              (y1 + y2) / 2 - dx * 8, x2, y2),
                         stroke=tv(BLUE), w=4))
        for k in (-1, 1):
            body.append(path("M%.1f %.1f l%.1f %.1f" % (x2, y2, dx * 14 + k * 8, dy * 10 - k * 6),
                             stroke=tv(BLUE), w=2.4))
    body.append('<circle cx="%d" cy="%d" r="34" fill="%s"/>' % (cx, cy, PINK))
    body.append('<circle cx="%d" cy="%d" r="11" fill="%s"/>' % (cx - 6, cy - 4, "#9D174D"))
    # axon and terminals
    body.append(path("M%d %d C 200 150, 240 190, 300 168" % (cx + 34, cy), stroke=tv(ORANGE), w=5))
    for k in (-1, 0, 1):
        body.append(path("M300 168 l22 %d" % (k * 22), stroke=tv(ORANGE), w=2.6))
        body.append(circle(323, 168 + k * 22, 4.5, fill=ORANGE, stroke="none", w=0))
    for lab, x, y, colour in (("dendrites", 52, 92, BLUE), ("cell body", 196, 220, PINK),
                              ("axon", 238, 148, ORANGE), ("synapses", 320, 214, ORANGE)):
        body.append(text(x, y, lab, 9.6, 750, fill=tv(colour)))
    body.append(text(190, 268, "fires when the combined signal is strong enough", 9.2, 600,
                     fill=MUTED))
    # the artificial neuron
    body.append(tint(400, 38, 340, 250, VIOLET, op=0.06, r=14))
    body.append(text(570, 60, "Artificial neuron", 11.5, 800, fill=tv(VIOLET)))
    ins = [(440, 110, "x₁"), (440, 168, "x₂"), (440, 226, "x₃")]
    for (x, y, lab), wlab in zip(ins, ("w₁", "w₂", "w₃")):
        body.append(line(x + 16, y, 560, 168, stroke=tv(BLUE), w=2.4))
        body.append(text((x + 560) / 2.0 - 6, (y + 168) / 2.0 - 6, wlab, 10, 800,
                         fill=tv(ORANGE)))
        body.append(neuron(x, y, 15, BLUE, lab, 10.5))
    body.append(line(576, 168, 618, 168, stroke=tv(VIOLET), w=2.4))
    body.append(neuron(560, 168, 22, PINK, "Σ", 15))
    body.append(text(560, 132, "+ b", 10.5, 800, fill=tv(PINK)))
    body.append(solid(618, 148, 46, 40, VIOLET, "f", r=10, size=15))
    body.append(arrow(664, 168, 712, 168, tv(ORANGE), 2.6))
    body.append(text(712, 158, "output", 9.6, 750, anchor="end", fill=tv(ORANGE)))
    for lab, x, y, colour in (("inputs", 440, 262, BLUE), ("weights", 500, 96, ORANGE),
                              ("sum + bias", 560, 210, PINK), ("activation", 641, 206, VIOLET)):
        body.append(text(x, y, lab, 9.6, 750, fill=tv(colour)))
    body.append(text(570, 268, "a = f(w₁x₁ + w₂x₂ + w₃x₃ + b)", 10, 750, fill=INK, mono=True))
    desc = ("Two panels. On the left a biological neuron: branching dendrites in blue "
            "receive signals, the cell body in pink combines them, and the axon in "
            "orange carries a pulse to synapses at its tips; the cell fires when the "
            "combined signal is strong enough. On the right an artificial neuron: "
            "three inputs x1, x2 and x3 in blue are joined by lines labelled with "
            "weights w1, w2 and w3 to a pink summing node, which also adds a bias b; "
            "the sum passes through an activation function f to give the output a "
            "equals f of w1 x1 plus w2 x2 plus w3 x3 plus b. Matching colours show "
            "dendrites as inputs, synapses as weights, the cell body as the sum and "
            "firing as the activation.")
    return figure("ai-nbio", 760, 300, "".join(body),
                  "A biological neuron and an artificial neuron", desc,
                  "The artificial neuron keeps the idea, not the biology.")


# ======================================== Level 6: inside one neuron

@diagram("ai-neuron-anatomy")
def _neuron_anatomy():
    """The film example: inputs, weights, products, sum, sigmoid, output."""
    x = [0.9, 0.2, 2.5]
    w = [1.5, 0.8, -0.6]
    b = -0.5
    z = sum(a * c for a, c in zip(x, w)) + b
    a_out = _sig(z)
    body = [text(380, 22, "One neuron, worked through: will Sam enjoy this film?", 12, 650,
                 fill=MUTED)]
    body.append(glow("ai-na-glow", PINK, 6))
    names = ["action", "comedy", "hours"]
    ys = [86, 166, 246]
    for i in range(3):
        y = ys[i]
        colour = PINK if w[i] >= 0 else BLUE
        width = 1.5 + abs(w[i]) * 3
        body.append(line(118, y, 380, 166, stroke=tv(colour), w=width))
        body.append(neuron(92, y, 26, BLUE, "%g" % x[i], 12))
        body.append(text(92, y + 42, names[i], 9.6, 750, fill=MUTED))
        mx, my = 118 + (380 - 118) * 0.3, y + (166 - y) * 0.3
        body.append(solid(mx - 34, my - 11, 68, 22, colour,
                          ("w = %+g" % w[i]).replace("-", "−"), r=11, size=10))
        body.append(_halo(mx + 44, my + (18 if i == 2 else -10),
                          ("x × w = %+.2f" % (x[i] * w[i])).replace("-", "−"), 9.4, 750, "start"))
    body.append(line(410, 60, 410, 140, stroke=tv(ORANGE), w=2.2, dash="4 3"))
    body.append(solid(372, 40, 76, 24, ORANGE, "bias −0.5", r=12, size=10))
    body.append('<circle cx="410" cy="166" r="34" fill="%s" filter="url(#ai-na-glow)"/>' % PINK)
    body.append(text(410, 160, "Σ", 18, 800, fill=WHITE))
    body.append(text(410, 180, ("z = %.2f" % z).replace("-", "−"), 10, 750, fill=WHITE))
    body.append(arrow(446, 166, 494, 166, tv(VIOLET), 2.6))
    # activation box with a little sigmoid
    body.append(tint(500, 116, 112, 100, VIOLET, op=0.12, r=12))
    pts = []
    for i in range(41):
        zz = -6 + 12 * i / 40.0
        pts.append("%.1f %.1f" % (512 + i * 2.2, 200 - _sig(zz) * 64))
    body.append(path("M" + " L".join(pts), stroke=tv(VIOLET), w=2.6))
    zx = 512 + (z + 6) / 12.0 * 88
    body.append(circle(zx, 200 - a_out * 64, 4.5, fill=AMBER, stroke=DARK, w=1))
    body.append(text(556, 134, "sigmoid", 10, 800, fill=tv(VIOLET)))
    body.append(arrow(616, 166, 662, 166, tv(GREEN), 2.6))
    body.append('<circle cx="700" cy="166" r="34" fill="%s"/>' % GREEN)
    body.append(text(700, 164, "%.2f" % a_out, 15, 800, fill=WHITE))
    body.append(text(700, 182, "38%", 9.6, 700, fill=WHITE))
    body.append(text(700, 222, "probably", 9.6, 750, fill=INK))
    body.append(text(700, 236, "not", 9.6, 750, fill=INK))
    body.append(text(380, 300, ("z = 0.9 × 1.5 + 0.2 × 0.8 + 2.5 × (−0.6) − 0.5 = %.2f,"
                     "   σ(z) = %.2f" % (z, a_out)).replace("= -", "= −"), 10.5, 750, fill=INK,
                     mono=True))
    desc = ("A neuron drawn left to right. Three input nodes hold the film's action "
            "0.9, comedy 0.2 and length 2.5 hours. Lines join them to a glowing summing "
            "node, labelled with Sam's weights: plus 1.5 for action, giving plus 1.35; "
            "plus 0.8 for comedy, giving plus 0.16; and minus 0.6 for hours, giving "
            "minus 1.50. Positive weights are pink and negative blue, and thicker "
            "lines are larger weights. A bias of minus 0.5 joins from above. The sum z "
            "is %.2f. It passes through a small sigmoid curve to give an output of "
            "%.2f, a 38 percent chance: probably not." % (z, a_out))
    return figure("ai-nana", 760, 316, "".join(body), "Inside an artificial neuron", desc,
                  "Multiply, add, squash. Every neuron in every network does exactly this.")


# ============================================ Level 6: a neuron's line

@diagram("ai-neuron-boundary")
def _neuron_boundary():
    """Weights turn the boundary and the bias slides it."""
    P = Plot(60, 40, 300, 260, (-1, 4), (-1, 3.4))
    body = [text(380, 22, "A neuron's decision boundary: weights turn it, the bias slides it",
                 12, 650, fill=MUTED)]
    w1, w2, b = 1.0, 2.0, -3.0
    G = 40
    cells = ['<g shape-rendering="crispEdges">']
    cw, ch = P.w / G, P.h / G
    for j in range(G):
        for i in range(G):
            x1 = P.xr[0] + (i + 0.5) / G * (P.xr[1] - P.xr[0])
            x2 = P.yr[0] + (j + 0.5) / G * (P.yr[1] - P.yr[0])
            s = _sig(2.2 * (w1 * x1 + w2 * x2 + b))
            cells.append('<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" fill="%s" '
                         'fill-opacity="0.55"/>' % (P.x + i * cw, P.y + P.h - (j + 1) * ch,
                                                    cw, ch, diverging(2 * s - 1)))
    cells.append("</g>")
    body.append("".join(cells))
    body.append('<rect x="%d" y="%d" width="%d" height="%d" fill="none" stroke="%s"/>'
                % (P.x, P.y, P.w, P.h, LINE))
    cid = "ai-nb-c"
    body.append(P.clip(cid))

    def bline(a, c, bb, colour, dash=None, wd=3):
        # a x1 + c x2 + bb = 0  ->  x2 = -(a x1 + bb) / c
        xa, xb = P.xr
        d = ' stroke-dasharray="%s"' % dash if dash else ""
        return ('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="%s"%s '
                'clip-path="url(#%s)"/>' % (P.px(xa), P.py(-(a * xa + bb) / c), P.px(xb),
                                            P.py(-(a * xb + bb) / c), colour, wd, d, cid))
    body.append(bline(w1, w2, -1.5, tv(TEAL), "6 4", 2))
    body.append(bline(w1, w2, -4.5, tv(TEAL), "6 4", 2))
    body.append(bline(2.0, 1.0, -3.0, tv(ORANGE), "3 4", 2))
    body.append(bline(w1, w2, b, INK, None, 3.2))
    # the weight vector, perpendicular to the boundary
    fx, fy = 1.0, 1.0
    L = math.hypot(w1, w2)
    body.append(arrow(P.px(fx), P.py(fy), P.px(fx + w1 / L * 1.1), P.py(fy + w2 / L * 1.1),
                      tv(VIOLET), 3))
    body.append(_halo(P.px(fx + w1 / L * 1.1) + 6, P.py(fy + w2 / L * 1.1), "w = (1, 2)", 10,
                      800, "start"))
    body.append(_halo(P.px(3.2), P.py(2.9), "yes side", 10, 800))
    body.append(_halo(P.px(0.0), P.py(-0.6), "no side", 10, 800))
    body.append(text(P.x + P.w / 2, P.y + P.h + 18, "input x₁", 9.6, 650, fill=MUTED))
    body.append(tint(392, 52, 350, 236, SLATE, op=0.06, r=12))
    rows = [(INK, None, "boundary: x₁ + 2x₂ − 3 = 0", "where z = 0 and the output is 0.5"),
            (tv(TEAL), "6 4", "same weights, bias −1.5 and −4.5", "the line slides, its angle unchanged"),
            (tv(ORANGE), "3 4", "weights (2, 1), same bias", "the line turns"),
            (tv(VIOLET), None, "the weight vector w", "at right angles to the line, towards yes")]
    for i, (colour, dash, a, b2) in enumerate(rows):
        y = 84 + i * 52
        d = ' stroke-dasharray="%s"' % dash if dash else ""
        body.append('<line x1="408" y1="%d" x2="436" y2="%d" stroke="%s" stroke-width="3"%s/>'
                    % (y - 4, y - 4, colour, d))
        body.append(text(446, y, a, 10, 800, anchor="start", fill=INK))
        body.append(text(446, y + 15, b2, 9.2, 600, anchor="start", fill=MUTED))
    desc = ("A square map of two inputs, shaded from blue where the neuron says no to "
            "pink where it says yes, with the boundary line x1 plus 2 x2 minus 3 equals "
            "0 drawn in black, where the output is 0.5. Two dashed teal lines parallel "
            "to it show the same weights with biases minus 1.5 and minus 4.5: the line "
            "slides without turning. A dotted orange line shows weights 2 and 1 with "
            "the same bias: the line turns. A violet arrow, the weight vector 1, 2, "
            "points at right angles to the boundary towards the yes side.")
    return figure("ai-nbound", 760, 320, "".join(body), "How weights and bias move the boundary",
                  desc, "One neuron, one straight line: that is all a single neuron can draw.")


# ============================================ Level 6: logic gates

@diagram("ai-neuron-gates")
def _neuron_gates():
    """AND, OR and NAND as one neuron each, on the unit square."""
    gates = [("AND", (1, 1), -1.5, lambda a, b: a and b),
             ("OR", (1, 1), -0.5, lambda a, b: a or b),
             ("NAND", (-1, -1), 1.5, lambda a, b: not (a and b))]
    body = [text(380, 22, "Three logic gates, each a single neuron with a step activation",
                 12, 650, fill=MUTED)]
    for k, (name, (w1, w2), b, fn) in enumerate(gates):
        x0 = 20 + k * 246
        body.append(tint(x0, 38, 232, 250, VIOLET, op=0.06, r=12))
        body.append(text(x0 + 116, 62, name, 13, 800, fill=tv(VIOLET)))
        body.append(text(x0 + 116, 80, "w = (%g, %g), b = %g" % (w1, w2, b), 10, 700, fill=INK,
                         mono=True))
        P = Plot(x0 + 50, 96, 150, 150, (-0.4, 1.4), (-0.4, 1.4))
        cid = "ai-gate-c%d" % k
        body.append(P.clip(cid))
        # shade the 'yes' side
        poly = []
        xs = [P.xr[0], P.xr[1]]
        y_at = [-(w1 * xx + b) / w2 for xx in xs]
        if w2 > 0:
            poly = [(xs[0], y_at[0]), (xs[1], y_at[1]), (xs[1], P.yr[1]), (xs[0], P.yr[1])]
        else:
            poly = [(xs[0], y_at[0]), (xs[1], y_at[1]), (xs[1], P.yr[0]), (xs[0], P.yr[0])]
        body.append('<polygon points="%s" fill="%s" fill-opacity="0.16" clip-path="url(#%s)"/>'
                    % (" ".join("%.1f,%.1f" % P.pt(*q) for q in poly), PINK, cid))
        body.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="none" stroke="%s"/>'
                    % (P.x, P.y, P.w, P.h, LINE))
        body.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
                    'stroke-width="2.6" clip-path="url(#%s)"/>'
                    % (P.px(xs[0]), P.py(y_at[0]), P.px(xs[1]), P.py(y_at[1]), INK, cid))
        for a in (0, 1):
            for c in (0, 1):
                on = bool(fn(a, c))
                x, y = P.pt(a, c)
                if on:
                    body.append(circle(x, y, 9, fill=PINK, stroke=FILL, w=2))
                else:
                    body.append('<circle cx="%.1f" cy="%.1f" r="8" fill="%s" stroke="%s" '
                                'stroke-width="2.6"/>' % (x, y, FILL, tv(BLUE)))
                body.append(text(x + (15 if a else -15), y + 4, "%d%d" % (a, c), 9.4, 700,
                                 anchor="start" if a else "end", fill=MUTED, mono=True))
        body.append(text(x0 + 116, 272, "pink: output 1 · hollow: output 0", 9, 650,
                         fill=MUTED))
    desc = ("Three panels, each showing the four input pairs 00, 01, 10 and 11 as "
            "points on a square, with the neuron's boundary line and its output-1 side "
            "shaded pink. AND, with weights 1 and 1 and bias minus 1.5: only 11 is on "
            "the pink side. OR, with weights 1 and 1 and bias minus 0.5: everything "
            "except 00 is on the pink side. NAND, with weights minus 1 and minus 1 and "
            "bias 1.5: everything except 11 is on the pink side. Filled pink points "
            "output 1 and hollow points output 0.")
    return figure("ai-gates", 760, 300, "".join(body), "Logic gates as single neurons", desc,
                  "Each gate is a straight line that puts the 1s on one side.")


# ================================================ Level 6: XOR

@diagram("ai-xor")
def _xor():
    """No single line separates XOR; two lines from a hidden layer do."""
    body = [text(380, 22, "XOR: one line always fails, two lines succeed", 12, 650, fill=MUTED)]
    pts = [((0, 0), 0), ((0, 1), 1), ((1, 0), 1), ((1, 1), 0)]
    for k in range(2):
        x0 = 30 + k * 370
        body.append(tint(x0, 38, 330, 262, RED if k == 0 else GREEN, op=0.06, r=12))
        body.append(text(x0 + 165, 62, "One neuron: one straight line" if k == 0 else
                         "A hidden layer: two lines", 11.5, 800, fill=tv(RED if k == 0 else GREEN)))
        P = Plot(x0 + 80, 82, 180, 180, (-0.5, 1.5), (-0.5, 1.5))
        cid = "ai-xor-c%d" % k
        body.append(P.clip(cid))
        body.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="none" stroke="%s"/>'
                    % (P.x, P.y, P.w, P.h, LINE))
        if k == 0:
            for (a1, b1, a2, b2), colour in (((-0.5, 0.4, 1.5, 0.9), ORANGE),
                                             ((0.2, -0.5, 1.2, 1.5), PURPLE),
                                             ((-0.5, 1.1, 1.5, 0.2), SKY)):
                body.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
                            'stroke-width="2.4" stroke-dasharray="6 4" clip-path="url(#%s)"/>'
                            % (P.px(a1), P.py(b1), P.px(a2), P.py(b2), colour, cid))
            body.append(text(x0 + 165, 290, "every line leaves a point on the wrong side",
                             9.4, 650, fill=MUTED))
        else:
            # the band between x1 + x2 = 0.5 (OR) and x1 + x2 = 1.5 (AND)
            stripe = [(-0.5, 1.0), (1.0, -0.5), (2.0, -0.5), (-0.5, 2.0)]
            body.append('<polygon points="%s" fill="%s" fill-opacity="0.18" clip-path="url(#%s)"/>'
                        % (" ".join("%.1f,%.1f" % P.pt(*q) for q in stripe), PINK, cid))
            for c0, colour, lab in ((0.5, ORANGE, "OR neuron: x₁ + x₂ > 0.5"),
                                    (1.5, VIOLET, "AND neuron: x₁ + x₂ > 1.5")):
                body.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
                            'stroke-width="2.8" clip-path="url(#%s)"/>'
                            % (P.px(-0.5), P.py(c0 + 0.5), P.px(1.5), P.py(c0 - 1.5),
                               tv(colour), cid))
            body.append(text(x0 + 165, 280, "output = OR and not AND:", 9.6, 750, fill=INK))
            body.append(text(x0 + 165, 294, "the pink band between the lines", 9.4, 650,
                             fill=MUTED))
            body.append(line(x0 + 284, 110, x0 + 306, 110, stroke=tv(ORANGE), w=2.8))
            body.append(text(x0 + 300, 126, "OR", 9.4, 800, fill=tv(ORANGE)))
            body.append(line(x0 + 284, 146, x0 + 306, 146, stroke=tv(VIOLET), w=2.8))
            body.append(text(x0 + 300, 162, "AND", 9.4, 800, fill=tv(VIOLET)))
        for (a, c), y in pts:
            x, yy = P.pt(a, c)
            if y:
                body.append(circle(x, yy, 9, fill=PINK, stroke=FILL, w=2))
            else:
                body.append('<circle cx="%.1f" cy="%.1f" r="8" fill="%s" stroke="%s" '
                            'stroke-width="2.6"/>' % (x, yy, FILL, tv(BLUE)))
    desc = ("Two panels showing the four XOR points: 01 and 10 output 1 and are pink; "
            "00 and 11 output 0 and are hollow blue, so the pink points lie on one "
            "diagonal and the hollow points on the other. In the first panel, three "
            "dashed attempts at a single straight line each leave a point on the wrong "
            "side. In the second panel, two parallel lines from two hidden neurons, an "
            "OR neuron at x1 plus x2 greater than 0.5 and an AND neuron at x1 plus x2 "
            "greater than 1.5, enclose a pink band containing exactly the two pink "
            "points: the output is OR and not AND.")
    return figure("ai-xor", 760, 310, "".join(body), "The XOR problem", desc,
                  "Two hidden neurons, two lines: the smallest network that beats the "
                  "1969 objection.")


# ===================================== Level 6: the activation functions

@diagram("ai-activations")
def _activations():
    """Step, sigmoid, tanh, ReLU, leaky ReLU and GELU, each in its own plot."""
    funcs = [("Step", lambda z: 1.0 if z > 0 else 0.0, BLUE, (-0.4, 1.4), "0 or 1"),
             ("Sigmoid", _sig, VIOLET, (-0.4, 1.4), "0 to 1"),
             ("Tanh", math.tanh, TEAL, (-1.4, 1.4), "−1 to 1"),
             ("ReLU", lambda z: max(0.0, z), ORANGE, (-1, 3), "0 to ∞"),
             ("Leaky ReLU", lambda z: z if z > 0 else 0.1 * z, PINK, (-1, 3), "slope 0.01 below 0 (drawn 0.1)"),
             ("GELU", _gelu, GREEN, (-1, 3), "smooth, dips to −0.17")]
    body = [text(380, 22, "Six activation functions", 12, 650, fill=MUTED)]
    for k, (name, f, colour, yr, rng) in enumerate(funcs):
        col, row = k % 3, k // 3
        x0, y0 = 20 + col * 246, 38 + row * 150
        body.append(tint(x0, y0, 232, 138, colour, op=0.07, r=12))
        body.append(text(x0 + 16, y0 + 22, name, 11.5, 800, anchor="start", fill=tv(colour)))
        body.append(text(x0 + 216, y0 + 22, rng, 8.8, 650, anchor="end", fill=MUTED))
        P = Plot(x0 + 20, y0 + 32, 192, 96, (-3, 3), yr)
        body.append(line(P.x, P.py(0), P.x + P.w, P.py(0), stroke=LINE, w=1))
        body.append(line(P.px(0), P.y, P.px(0), P.y + P.h, stroke=LINE, w=1))
        if name == "Step":
            body.append(path("M%.1f %.1f L%.1f %.1f" % (P.px(-3), P.py(0), P.px(0), P.py(0)),
                             stroke=tv(colour), w=3.2))
            body.append(path("M%.1f %.1f L%.1f %.1f" % (P.px(0), P.py(1), P.px(3), P.py(1)),
                             stroke=tv(colour), w=3.2))
            body.append('<circle cx="%.1f" cy="%.1f" r="3.4" fill="%s" stroke="%s" stroke-width="1.8"/>'
                        % (P.px(0), P.py(1), FILL, tv(colour)))
        else:
            body.append('<path d="%s" fill="none" stroke="%s" stroke-width="3.2" '
                        'stroke-linecap="round"/>' % (P.curve(f, 120), tv(colour)))
    desc = ("Six small graphs, each of an activation function for inputs from minus 3 "
            "to 3. Step jumps from 0 to 1 at zero. Sigmoid is an S-curve from 0 to 1. "
            "Tanh is an S-curve from minus 1 to 1. ReLU is flat at zero for negative "
            "inputs and a straight line of slope 1 for positive inputs. Leaky ReLU is "
            "the same but with a small slope below zero. GELU is a smooth version of "
            "ReLU that dips slightly below zero, to about minus 0.17, before rising.")
    return figure("ai-acts", 760, 344, "".join(body), "Activation functions", desc,
                  "Each one adds a bend. ReLU's bend is the simplest, and it is enough.")


# =================================== Level 6: a curve from ReLU hinges

@diagram("ai-relu-sum")
def _relu_sum():
    """Six ReLU neurons, weighted and added, trace a smooth curve."""
    def target(x):
        return math.sin(x) + 0.3 * x

    hinges = [0.0, 1.05, 2.1, 3.15, 4.2, 5.25]
    xs = [i * 6.28 / 60.0 for i in range(61)]

    def feats(x):
        return [1.0] + [max(0.0, x - h) for h in hinges]
    a = [[sum(feats(x)[i] * feats(x)[j] for x in xs) for j in range(7)] for i in range(7)]
    bb = [sum(feats(x)[i] * target(x) for x in xs) for i in range(7)]
    c = _solve(a, bb)

    def approx(x):
        return sum(ci * fi for ci, fi in zip(c, feats(x)))
    body = [text(380, 22, "Hinges make curves: weighted ReLUs, added up", 12, 650,
                 fill=MUTED)]
    body.append(tint(20, 36, 350, 270, SLATE, op=0.05, r=12))
    # one hidden neuron: flat, then a ramp
    A = Plot(56, 70, 120, 70, (0, 3), (-0.2, 2.2))
    body.append(text(116, 58, "one ReLU neuron", 10, 800, fill=INK))
    body.append(line(A.x, A.py(0), A.x + A.w, A.py(0), stroke=LINE, w=1))
    body.append(path("M%.1f %.1f L%.1f %.1f L%.1f %.1f" % (A.px(0), A.py(0), A.px(1), A.py(0),
                                                       A.px(3), A.py(2)), stroke=tv(VIOLET), w=3))
    body.append(circle(A.px(1), A.py(0), 4, fill=VIOLET, stroke=FILL, w=1.2))
    body.append(text(A.px(1), A.py(0) + 16, "its hinge", 8.8, 650, fill=MUTED))
    body.append(text(254, 92, "flat until its hinge,", 9.4, 650, fill=MUTED))
    body.append(text(254, 106, "then a straight ramp", 9.4, 650, fill=MUTED))
    # three neurons make a bump
    B = Plot(56, 192, 290, 100, (0, 4.2), (-4.2, 3.2))
    body.append(text(195, 180, "relu(x−1) − 2·relu(x−2) + relu(x−3)", 9.6, 750, fill=INK,
                     mono=True))
    body.append(line(B.x, B.py(0), B.x + B.w, B.py(0), stroke=LINE, w=1))
    cid = "ai-rs-c"
    body.append(B.clip(cid))
    for f, colour in ((lambda x: max(0.0, x - 1), BLUE), (lambda x: -2 * max(0.0, x - 2), PINK),
                      (lambda x: max(0.0, x - 3), TEAL)):
        body.append('<path d="%s" fill="none" stroke="%s" stroke-width="1.8" '
                    'stroke-dasharray="5 3" clip-path="url(#%s)"/>' % (B.curve(f, 84), tv(colour), cid))
    bump = lambda x: max(0.0, x - 1) - 2 * max(0.0, x - 2) + max(0.0, x - 3)
    body.append('<path d="%s" fill="none" stroke="%s" stroke-width="3.4"/>'
                % (B.curve(bump, 84), tv(VIOLET)))
    body.append(_halo(B.px(2) + 8, B.py(1) - 4, "the sum: a bump", 9.4, 800, "start"))
    R = Plot(440, 70, 290, 200, (0, 6.28), (-1.2, 2.4))
    body.append(tint(400, 36, 350, 270, VIOLET, op=0.06, r=12))
    body.append(text(575, 58, "their sum, against the target", 10.5, 800, fill=INK))
    body.append(line(R.x, R.py(0), R.x + R.w, R.py(0), stroke=LINE, w=1))
    body.append('<path d="%s" fill="none" stroke="%s" stroke-width="7" stroke-opacity="0.35" '
                'stroke-linecap="round"/>' % (R.curve(target, 120), AMBER))
    body.append('<path d="%s" fill="none" stroke="%s" stroke-width="2.6"/>'
                % (R.curve(approx, 240), tv(VIOLET)))
    for h in hinges:
        body.append(circle(R.px(h), R.py(approx(h)), 4, fill=VIOLET, stroke=FILL, w=1.2))
    body.append(line(452, 286, 476, 286, stroke=AMBER, w=7))
    body.append(text(482, 290, "target curve", 9.4, 650, anchor="start", fill=MUTED))
    body.append(line(582, 286, 606, 286, stroke=tv(VIOLET), w=2.6))
    body.append(text(612, 290, "network output", 9.4, 650, anchor="start", fill=MUTED))
    desc = ("On the left, six straight-line pieces, each a ReLU neuron that is zero up "
            "to its hinge point and then rises or falls with its own weight; the hinges "
            "are evenly spaced from 0 to about 5.3. On the right, the sum of the six "
            "pieces plus a constant, drawn as a violet line made of straight segments "
            "that bend at the hinges, follows a thick amber target curve, a wave "
            "rising overall, closely.")
    return figure("ai-relusum", 760, 318, "".join(body), "Building a curve from ReLUs", desc,
                  "More hidden neurons mean more hinges and a closer fit: the universal "
                  "approximation idea.")


# ============================ Level 6: derivatives and vanishing gradients

@diagram("ai-activation-derivs")
def _activation_derivs():
    """Slopes of sigmoid, tanh and ReLU, and what repeated slopes do."""
    body = [text(380, 22, "Slopes matter: the sigmoid's is never more than 0.25", 12, 650,
                 fill=MUTED)]
    P = Plot(70, 50, 300, 210, (-5, 5), (0, 1.1))
    body.append(P.axes([-4, -2, 0, 2, 4], [0, 0.25, 0.5, 0.75, 1.0], "input z", "slope"))
    for f, colour in ((lambda z: _sig(z) * (1 - _sig(z)), VIOLET),
                      (lambda z: 1 - math.tanh(z) ** 2, TEAL)):
        body.append('<path d="%s" fill="none" stroke="%s" stroke-width="3"/>'
                    % (P.curve(f, 140), tv(colour)))
    body.append(path("M%.1f %.1f L%.1f %.1f M%.1f %.1f L%.1f %.1f"
                     % (P.px(-5), P.py(0), P.px(0), P.py(0), P.px(0), P.py(1), P.px(5), P.py(1)),
                     stroke=tv(ORANGE), w=3, dash="7 3"))
    body.append(_halo(P.px(0) + 6, P.py(0.25) - 8, "sigmoid′: at most 0.25", 9.6, 750, "start"))
    body.append(_halo(P.px(-1.4), P.py(0.62), "tanh′", 9.6, 750, "end"))
    body.append(_halo(P.px(3), P.py(1) - 8, "ReLU′ = 1", 9.6, 750))
    # repeated multiplication, log scale bars
    Q = Plot(470, 84, 260, 180, (0.5, 10.5), (-7, 0))
    body.append(tint(420, 38, 330, 262, RED, op=0.05, r=12))
    body.append(text(585, 58, "gradient left after n layers", 10.5, 800, fill=INK))
    for n in range(1, 11):
        v = 0.25 ** n
        x = Q.px(n) - 9
        y = Q.py(math.log10(v))
        body.append('<rect x="%.1f" y="%.1f" width="18" height="%.1f" rx="3" fill="%s"/>'
                    % (x, Q.py(0), y - Q.py(0), plasma(0.85 - n * 0.07)))
        body.append(text(x + 9, Q.y + Q.h + 14, str(n), 9, 650, fill=MUTED))
    for e in range(0, -8, -2):
        body.append(text(Q.x - 6, Q.py(e) + 3.5, "10" + {0: "⁰", -2: "⁻²", -4: "⁻⁴", -6: "⁻⁶"}[e],
                         9, 650, anchor="end", fill=MUTED))
    body.append(line(Q.x, Q.py(0), Q.x + Q.w, Q.py(0), stroke=tv(ORANGE), w=2.4, dash="7 3"))
    body.append(text(Q.x + Q.w, Q.py(0) - 6, "ReLU: stays at 1", 9.4, 750, anchor="end",
                     fill=tv(ORANGE)))
    body.append(text(585, 292, "sigmoid layers: 0.25ⁿ (log scale)", 9.4, 650, fill=MUTED))
    desc = ("On the left, the slopes of three activation functions. The sigmoid's slope "
            "is a low hump peaking at only 0.25 at zero. Tanh's slope is a taller hump "
            "peaking at 1. ReLU's slope is 0 for negative inputs and exactly 1 for "
            "positive inputs. On the right, bars on a logarithmic scale show the "
            "gradient left after passing back through 1 to 10 sigmoid layers, 0.25 to "
            "the power n, shrinking from 0.25 to under one millionth, while through "
            "ReLU layers it stays at 1.")
    return figure("ai-adiff", 760, 306, "".join(body), "Activation slopes and vanishing gradients",
                  desc, "Multiply small numbers enough times and the learning signal vanishes.")


# ================================================ Level 6: softmax

@diagram("ai-softmax")
def _softmax_fig():
    """Logits turned into probabilities at three temperatures."""
    classes = ["cat", "dog", "fox", "owl"]
    logits = [2.0, 1.0, 0.1, -1.0]
    colours = [VIOLET, PINK, ORANGE, TEAL]

    def softmax(zs, T):
        ex = [math.exp(z / T) for z in zs]
        s = sum(ex)
        return [e / s for e in ex]
    body = [text(380, 22, "Softmax turns raw scores into probabilities that add up to 1", 12,
                 650, fill=MUTED)]
    # logits
    body.append(tint(20, 38, 200, 262, SLATE, op=0.06, r=12))
    body.append(text(120, 60, "logits (raw scores)", 10.5, 800, fill=INK))
    zero = 196
    for i, (c, z) in enumerate(zip(classes, logits)):
        x = 44 + i * 42
        h = z * 44
        y = zero - max(h, 0)
        body.append('<rect x="%d" y="%.1f" width="30" height="%.1f" rx="4" fill="%s"/>'
                    % (x, y, abs(h), colours[i]))
        body.append(text(x + 15, (zero - h - 6) if z >= 0 else (zero - h + 14),
                         ("%g" % z).replace("-", "−"),
                         9.6, 750, fill=INK))
        body.append(text(x + 15, 290, c, 9.6, 700, fill=MUTED))
    body.append(line(36, zero, 212, zero, stroke=LINE, w=1.4))
    body.append(arrow(226, 170, 262, 170, LINE, 2.2))
    for k, T in enumerate([0.5, 1.0, 2.0]):
        x0 = 268 + k * 162
        probs = softmax(logits, T)
        body.append(tint(x0, 38, 150, 262, VIOLET, op=0.06 + 0.02 * (k == 1), r=12))
        body.append(text(x0 + 75, 60, "T = %g" % T, 11, 800, fill=tv(VIOLET)))
        body.append(text(x0 + 75, 76, ["sharper", "standard", "flatter"][k], 9.2, 650, fill=MUTED))
        for i, p in enumerate(probs):
            x = x0 + 14 + i * 33
            h = p * 170
            body.append('<rect x="%d" y="%.1f" width="25" height="%.1f" rx="4" fill="%s"/>'
                        % (x, 270 - h, h, colours[i]))
            body.append(text(x + 12.5, 264 - h, "%.2f" % p, 8.6, 750, fill=INK))
            body.append(text(x + 12.5, 290, classes[i], 8.6, 650, fill=MUTED))
        body.append(line(x0 + 10, 270, x0 + 140, 270, stroke=LINE, w=1.2))
    desc = ("On the left, four logits as bars: cat 2, dog 1, fox 0.1 and owl minus 1. An "
            "arrow leads to three panels of softmax probabilities. At temperature 0.5, "
            "sharper: cat %.2f, dog %.2f, fox %.2f, owl %.2f. At temperature 1, "
            "standard: cat %.2f, dog %.2f, fox %.2f, owl %.2f. At temperature 2, "
            "flatter: cat %.2f, dog %.2f, fox %.2f, owl %.2f. In every panel the "
            "probabilities add up to 1 and keep the same order."
            % tuple(softmax(logits, 0.5) + softmax(logits, 1.0) + softmax(logits, 2.0)))
    return figure("ai-smax", 760, 306, "".join(body), "Softmax and temperature", desc,
                  "Same scores, same order: temperature only changes how confident the "
                  "probabilities are.")


# ========================================= Level 7: a network, in depth

@diagram("ai-mlp-anatomy")
def _mlp_anatomy():
    """Input, two hidden layers and a softmax output, on tilted layer slabs."""
    import random
    rnd = random.Random(11)
    sizes = [4, 6, 6, 3]
    weights = [[[rnd.uniform(-1, 1) for _ in range(sizes[l + 1])] for _ in range(sizes[l])]
               for l in range(3)]
    body = [text(380, 22, "A multi-layer perceptron: every neuron feeds every neuron in the "
                 "next layer", 12, 650, fill=MUTED)]
    xs = [90, 270, 450, 610]
    colours = [BLUE, VIOLET, PINK, ORANGE]
    for x, colour in zip(xs, colours):
        body.append('<polygon points="%d,62 %d,44 %d,266 %d,284" fill="%s" fill-opacity="0.1" '
                    'stroke="%s" stroke-opacity="0.5"/>' % (x - 24, x + 24, x + 24, x - 24, colour,
                                                            tv(colour)))
    net, pos = mlp(sizes, xs[0], xs[-1], 50, 280, colours, weights=weights, r=12, edge_op=0.42)
    body.append(net)
    for li in (1, 2):
        for (x, y) in pos[li]:
            body.append('<circle cx="%.1f" cy="%.1f" r="12" fill="none" stroke="%s" '
                        'stroke-width="1.6" class="ai-flow"/>' % (x, y, AMBER))
    labels = [("input layer", "4 features"), ("hidden layer 1", "6 neurons, ReLU"),
              ("hidden layer 2", "6 neurons, ReLU"), ("output layer", "3 classes, softmax")]
    for (a, b), x, colour in zip(labels, xs, colours):
        body.append(text(x, 304, a, 10, 800, fill=tv(colour)))
        body.append(text(x, 318, b, 9, 600, fill=MUTED))
    probs = [0.71, 0.21, 0.08]
    for k, (p, name) in enumerate(zip(probs, ["cat", "dog", "fox"])):
        (x, y) = pos[3][k]
        body.append('<rect x="%.1f" y="%.1f" width="%.1f" height="12" rx="3" fill="%s"/>'
                    % (x + 22, y - 6, p * 90, ORANGE))
        body.append(text(x + 28 + p * 90, y + 4, "%s %.2f" % (name, p), 9.4, 700, anchor="start",
                         fill=INK))
    body.append(line(668, 66, 690, 66, stroke=tv(PINK), w=2.6))
    body.append(text(694, 70, "+ weight", 9, 650, anchor="start", fill=MUTED))
    body.append(line(668, 84, 690, 84, stroke=tv(BLUE), w=2.6))
    body.append(text(694, 88, "− weight", 9, 650, anchor="start", fill=MUTED))
    desc = ("A neural network drawn left to right on four tinted, slightly tilted slabs. "
            "The input layer has 4 neurons for 4 features, two hidden layers have 6 "
            "neurons each using ReLU, and the output layer has 3 neurons with softmax, "
            "giving probabilities cat 0.71, dog 0.21 and fox 0.08 as bars. Every neuron "
            "connects to every neuron in the next layer; lines are pink for positive "
            "weights and blue for negative weights, thicker for larger weights.")
    return figure("ai-mlpa", 760, 330, "".join(body), "A multi-layer perceptron", desc,
                  "4 × 6 + 6 × 6 + 6 × 3 = 78 weights and 15 biases: 93 parameters.")


# =============================================== Level 7: W x + b

@diagram("ai-matmul")
def _matmul():
    """A 4 × 3 weight matrix times an input vector, plus bias, through ReLU."""
    W = [[0.2, -0.5, 1.0], [0.5, -1.0, 2.0], [-0.3, 0.8, 0.1], [1.0, 0.0, -0.5]]
    x = [1, 2, 0.5]
    b = [0.1, 0.0, -0.2, 0.3]
    wx = [sum(a * c for a, c in zip(row, x)) for row in W]
    z = [v + bb for v, bb in zip(wx, b)]
    a = [max(0.0, v) for v in z]
    HL = 2
    body = [text(380, 22, "A whole layer at once: f(W x + b)", 12, 650, fill=MUTED)]
    C = 40

    def cellfill(v):
        return diverging(max(-1, min(1, v / 2.0)))

    def column(x0, y0, vals, label, hi=None):
        out = []
        for i, v in enumerate(vals):
            col = cellfill(v)
            out.append('<rect x="%d" y="%d" width="%d" height="%d" rx="5" fill="%s" '
                       'stroke="%s" stroke-width="%s"/>' % (x0, y0 + i * C, C - 4, C - 4, col,
                                                            AMBER if hi == i else "none",
                                                            3 if hi == i else 0))
            out.append(text(x0 + (C - 4) / 2.0, y0 + i * C + 23, ("%g" % v).replace("-", "−"),
                            11, 750, fill=ink_on(col)))
        out.append(text(x0 + (C - 4) / 2.0, y0 - 10, label, 10, 800, fill=INK))
        return "".join(out)
    X0, Y0 = 40, 70
    for i, row in enumerate(W):
        for j, v in enumerate(row):
            col = cellfill(v)
            body.append('<rect x="%d" y="%d" width="%d" height="%d" rx="5" fill="%s" stroke="%s" '
                        'stroke-width="%s"/>' % (X0 + j * C, Y0 + i * C, C - 4, C - 4, col,
                                                 AMBER if i == HL else "none", 3 if i == HL else 0))
            body.append(text(X0 + j * C + 18, Y0 + i * C + 23, ("%g" % v).replace("-", "−"), 11,
                             750, fill=ink_on(col)))
    body.append(text(X0 + 58, Y0 - 10, "W (4 neurons × 3 inputs)", 10, 800, fill=INK))
    body.append(text(X0 + 3 * C + 12, Y0 + 2 * C + 6, "×", 18, 800, fill=MUTED))
    body.append(column(X0 + 3 * C + 30, Y0 + C // 2, x, "x"))
    body.append(text(X0 + 4 * C + 46, Y0 + 2 * C + 6, "+", 18, 800, fill=MUTED))
    body.append(column(X0 + 4 * C + 64, Y0, b, "b"))
    body.append(text(X0 + 5 * C + 80, Y0 + 2 * C + 6, "=", 18, 800, fill=MUTED))
    body.append(column(X0 + 5 * C + 98, Y0, [round(v, 2) for v in z], "z", HL))
    body.append(arrow(X0 + 6 * C + 104, Y0 + 2 * C, X0 + 6 * C + 150, Y0 + 2 * C, tv(VIOLET), 2.4))
    body.append(text(X0 + 6 * C + 127, Y0 + 2 * C - 10, "ReLU", 10, 800, fill=tv(VIOLET)))
    body.append(column(X0 + 6 * C + 158, Y0, [round(v, 2) for v in a], "output", HL))
    row = W[HL]
    body.append(tint(40, 252, 680, 40, AMBER, op=0.12, r=10))
    body.append(text(380, 277, ("neuron 3: z = (−0.3)(1) + (0.8)(2) + (0.1)(0.5) + (−0.2) = %.2f, "
                                "ReLU keeps it: %.2f" % (z[HL], a[HL])), 10.5, 750, fill=INK,
                     mono=True))
    desc = ("A 4 by 3 weight matrix W, each cell coloured blue for negative and pink for "
            "positive, multiplied by an input vector x of 1, 2 and 0.5, plus a bias "
            "vector b of 0.1, 0, minus 0.2 and 0.3, gives z: %s. ReLU turns the "
            "negatives to zero, giving the output %s. The third row is highlighted: "
            "neuron 3 computes minus 0.3 times 1 plus 0.8 times 2 plus 0.1 times 0.5 "
            "minus 0.2, which is %.2f, and ReLU keeps it."
            % (", ".join("%.2f" % v for v in z), ", ".join("%.2f" % v for v in a), z[HL]))
    return figure("ai-matmul", 760, 304, "".join(body), "A layer as a matrix multiplication",
                  desc, "Each row of W is one neuron. One multiplication computes them all.")


# ====================================== Level 7: XOR, solved by a layer

@diagram("ai-xor-solved")
def _xor_solved():
    """The hidden layer moves the four points so that one line separates them."""
    pts = [((0, 0), 0), ((0, 1), 1), ((1, 0), 1), ((1, 1), 0)]

    def hid(x):
        return (max(0, x[0] + x[1]), max(0, x[0] + x[1] - 1))
    body = [text(380, 22, "The hidden layer moves the points; then one line is enough", 12,
                 650, fill=MUTED)]
    A = Plot(60, 70, 190, 190, (-0.4, 1.4), (-0.4, 1.4))
    B = Plot(510, 70, 210, 190, (-0.3, 2.3), (-0.4, 1.4))
    for P, title in ((A, "input space (x₁, x₂)"), (B, "hidden space (h₁, h₂)")):
        body.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="8" fill="%s" '
                    'fill-opacity="0.5" stroke="%s"/>' % (P.x, P.y, P.w, P.h, FILL2, LINE))
        body.append(text(P.x + P.w / 2, P.y - 12, title, 10.5, 800, fill=INK))
    cid = "ai-xs-c"
    body.append(B.clip(cid))
    # separating line in hidden space: h1 - 2 h2 = 0.5
    body.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="3" '
                'clip-path="url(#%s)"/>' % (B.px(0.5), B.py(0), B.px(2.3), B.py(0.9), tv(GREEN), cid))
    body.append(_halo(B.px(1.95), B.py(0.4), "h₁ − 2h₂ = 0.5", 9.6, 800))
    for (x, y) in pts:
        for P, p in ((A, x), (B, hid(x))):
            px_, py_ = P.pt(*p)
            if y:
                body.append(circle(px_, py_, 9, fill=PINK, stroke=FILL, w=2))
            else:
                body.append('<circle cx="%.1f" cy="%.1f" r="8" fill="%s" stroke="%s" '
                            'stroke-width="2.6"/>' % (px_, py_, FILL, tv(BLUE)))
        body.append(_halo(A.px(x[0]) + (14 if x[0] else -14), A.py(x[1]) + 4,
                          "%d%d" % x, 9.4, 700, "start" if x[0] else "end"))
    body.append(_halo(B.px(1) + 2, B.py(0) + 24, "01 and 10 land together", 9, 700))
    body.append(_halo(B.px(2) - 8, B.py(1) - 14, "11", 9.4, 700))
    body.append(_halo(B.px(0) + 2, B.py(0) - 14, "00", 9.4, 700))
    body.append(tint(282, 112, 196, 104, VIOLET, op=0.1, r=12))
    body.append(text(380, 136, "hidden layer", 10.5, 800, fill=tv(VIOLET)))
    body.append(text(380, 160, "h₁ = ReLU(x₁ + x₂)", 10, 700, fill=INK, mono=True))
    body.append(text(380, 182, "h₂ = ReLU(x₁ + x₂ − 1)", 10, 700, fill=INK, mono=True))
    body.append(arrow(254, 166, 280, 166, tv(VIOLET), 2.4))
    body.append(arrow(480, 166, 506, 166, tv(VIOLET), 2.4))
    body.append(text(380, 290, "output = h₁ − 2h₂: positive on one side of the green line, "
                     "zero on the other", 9.6, 650, fill=MUTED))
    desc = ("On the left, the four XOR inputs in the input space: 01 and 10, the pink 1s, "
            "on one diagonal and 00 and 11, the hollow 0s, on the other, which no line "
            "separates. In the middle, the hidden layer: h1 equals ReLU of x1 plus x2 and "
            "h2 equals ReLU of x1 plus x2 minus 1. On the right, the same points in the "
            "hidden space: 00 goes to (0, 0), 01 and 10 both land on (1, 0), and 11 goes "
            "to (2, 1). Now a single green line, h1 minus 2 h2 equals 0.5, separates the "
            "pink point from the hollow ones.")
    return figure("ai-xorsol", 760, 304, "".join(body), "How a hidden layer solves XOR", desc,
                  "Each layer re-represents the data so the next layer's job is easier.")


# ============================================ Level 7: model sizes

@diagram("ai-model-sizes")
def _model_sizes():
    """Parameter counts from a perceptron to GPT-3, on a log scale."""
    models = [("Perceptron for AND", "2 weights + 1 bias", 3),
              ("Digit MLP, 784-128-64-10", "this lesson", 109386),
              ("LeNet-5 (1998)", "read handwritten cheques", 60000),
              ("AlexNet (2012)", "the ImageNet breakthrough", 6.0e7),
              ("BERT-large (2018)", "language understanding", 3.4e8),
              ("GPT-2 (2019)", "fluent paragraphs", 1.5e9),
              ("GPT-3 (2020)", "few-shot learning", 1.75e11)]
    models.sort(key=lambda m: m[2])
    body = [text(380, 22, "How many parameters? Every grid line is ten times the last", 12,
                 650, fill=MUTED)]
    X0, X1, Y0 = 250, 730, 50
    def X(v):
        return X0 + math.log10(v) / 12.0 * (X1 - X0)
    for e in range(0, 13, 2):
        x = X(10 ** e)
        body.append(line(x, Y0 - 6, x, Y0 + len(models) * 34, stroke=LINE, w=0.6, dash="2 4"))
        lab = {0: "1", 2: "100", 4: "10 thousand", 6: "1 million", 8: "100 million",
               10: "10 billion", 12: "1 trillion"}[e]
        body.append(text(x, Y0 + len(models) * 34 + 16, lab, 8.8, 650, fill=MUTED))
    for i, (name, sub, v) in enumerate(models):
        y = Y0 + i * 34
        colour = plasma(0.12 + 0.13 * i)
        body.append(text(X0 - 10, y + 12, name, 10, 750, anchor="end", fill=INK))
        body.append(text(X0 - 10, y + 25, sub, 8.6, 600, anchor="end", fill=MUTED))
        body.append('<rect x="%d" y="%d" width="%.1f" height="22" rx="5" fill="%s"/>'
                    % (X0, y + 2, max(4, X(v) - X0), colour))
        lab = ("{:,}".format(int(v)) if v < 1e6 else
               ("%.0f million" % (v / 1e6) if v < 1e9 else "%.1f billion" % (v / 1e9)))
        lab = lab.replace(".0 billion", " billion")
        tx = X(v) + 6
        body.append(text(tx, y + 18, lab, 9.6, 750, anchor="start", fill=INK))
    desc = ("Horizontal bars on a logarithmic scale, where each grid line is ten times the "
            "one before, from 1 to 1 trillion parameters: a perceptron for AND, 3; "
            "LeNet-5 from 1998, which read handwritten cheques, about 60 thousand; the "
            "digit network from this lesson, 109,386; AlexNet from 2012, about 60 "
            "million; BERT-large from 2018, 340 million; GPT-2 from 2019, 1.5 billion; "
            "and GPT-3 from 2020, 175 billion.")
    return figure("ai-msize", 760, 330, "".join(body), "Model sizes, from 3 to 175 billion",
                  desc, "Modern frontier models are larger still, though most of their "
                  "makers no longer publish the numbers.")


# ============================================= Level 7: chain-rule gears

def _gear(cx, cy, r, teeth, colour, spin=None, rev=False):
    pts = []
    for k in range(teeth * 2):
        ang = math.pi * k / teeth
        rr = r + (5 if k % 2 == 0 else -3)
        a1, a2 = ang - math.pi / teeth * 0.45, ang + math.pi / teeth * 0.45
        pts.append("%.1f,%.1f" % (cx + rr * math.cos(a1), cy + rr * math.sin(a1)))
        pts.append("%.1f,%.1f" % (cx + rr * math.cos(a2), cy + rr * math.sin(a2)))
    cls = ' class="ai-spin%s" style="--ai-spin:%s"' % (" ai-rev" if rev else "", spin) if spin else ""
    return ('<g%s><polygon points="%s" fill="%s"/><circle cx="%.1f" cy="%.1f" r="%.1f" '
            'fill="%s" fill-opacity="0.35"/><circle cx="%.1f" cy="%.1f" r="5" fill="%s"/>'
            '<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="#FFFFFF" stroke-width="3" '
            'stroke-linecap="round"/></g>'
            % (cls, " ".join(pts), colour, cx, cy, r * 0.55, WHITE, cx, cy, DARK,
               cx, cy, cx + r * 0.75, cy))


@diagram("ai-chain-gears")
def _chain_gears():
    """A compound gear train: rates of turning multiply, like derivatives."""
    body = [text(380, 22, "The chain rule as gears: rates multiply along the chain", 12, 650,
                 fill=MUTED)]
    # 36, 12 and 6 teeth of the same size: B turns 3 times per turn of A, C twice per turn of B
    body.append(_gear(140, 150, 90, 36, VIOLET, "24s"))
    body.append(_gear(260, 150, 30, 12, PINK, "8s", rev=True))
    body.append(_gear(305, 150, 15, 6, ORANGE, "4s"))
    for x, lab, sub, colour in ((140, "A: x", "turns once", VIOLET),
                                (252, "B: u", "turns 3 times", PINK),
                                (330, "C: y", "turns 6 times", ORANGE)):
        body.append(text(x, 262, lab, 11, 800, fill=tv(colour)))
        body.append(text(x, 278, sub, 9.4, 650, fill=MUTED))
    body.append(tint(420, 56, 320, 196, SLATE, op=0.07, r=12))
    rows = [("du/dx = 3", "B turns 3 times for each turn of A", PINK),
            ("dy/du = 2", "C turns 2 times for each turn of B", ORANGE),
            ("dy/dx = 3 × 2 = 6", "so C turns 6 times for each turn of A", VIOLET)]
    for i, (a, b, colour) in enumerate(rows):
        y = 92 + i * 56
        body.append(text(440, y, a, 13, 800, anchor="start", fill=tv(colour), mono=True))
        body.append(text(440, y + 18, b, 9.6, 650, anchor="start", fill=MUTED))
    desc = ("A gear train. A large violet gear A, standing for x, turns a small gear on "
            "the axle of gear B, standing for u, so B turns 3 times for each turn of A. A "
            "larger gear on B's axle turns a small orange gear C, standing for y, 2 times "
            "for each turn of B, so C turns 6 times for each turn of A. Beside it: du by "
            "dx equals 3, dy by du equals 2, so dy by dx equals 3 times 2 equals 6. When "
            "motion is allowed, the gears turn at those speeds.")
    return figure("ai-gears", 760, 296, "".join(body), "The chain rule as gears", desc,
                  "Backpropagation multiplies the local rates along every path from a "
                  "weight to the loss.")


# ==================================== Level 7: forward then backward

@diagram("ai-backprop-graph")
def _backprop_graph():
    """L = (w·x + b − y)², forward values then backward gradients, step by step."""
    nodes = {"x": (60, 90), "w": (60, 190), "mul": (200, 140), "b": (200, 250),
             "add": (340, 170), "y": (340, 280), "sub": (480, 200), "sq": (620, 200)}
    labels = {"x": "x", "w": "w", "mul": "×", "b": "b", "add": "+", "y": "y", "sub": "−", "sq": "( )²"}
    edges = [("x", "mul"), ("w", "mul"), ("mul", "add"), ("b", "add"), ("add", "sub"),
             ("y", "sub"), ("sub", "sq")]
    fwd = {"x": "2", "w": "0.5", "b": "0.1", "y": "1", "mul": "u = 1", "add": "z = 1.1",
           "sub": "e = 0.1", "sq": "L = 0.01"}
    bwd = {"sq": "1", "sub": "0.2", "add": "0.2", "b": "0.2", "mul": "0.2", "w": "0.4",
           "x": "0.1", "y": "−0.2"}
    base = [text(380, 22, "Forward values (blue), then backward gradients (orange)", 12, 650,
                 fill=MUTED)]
    for a, b in edges:
        (x1, y1), (x2, y2) = nodes[a], nodes[b]
        base.append(line(x1, y1, x2, y2, stroke=LINE, w=2))
    for k, (x, y) in nodes.items():
        op = k in ("mul", "add", "sub", "sq")
        base.append(neuron(x, y, 24, VIOLET if op else SLATE, labels[k], 13 if op else 12))
    base.append(arrow(650, 200, 700, 200, LINE, 2))
    base.append(text(716, 205, "loss", 10, 800, anchor="start", fill=INK))

    def tag(k, val, colour, below):
        x, y = nodes[k]
        dy = 42 if below else -34
        return (solid(x - 38, y + dy - 13, 76, 22, colour, val, r=11, size=10))
    order_f = ["x", "w", "b", "y", "mul", "add", "sub", "sq"]
    order_b = ["sq", "sub", "add", "b", "mul", "w", "x", "y"]
    stages, labels_out = [], []
    shown_f = []
    for k in order_f[:4]:
        shown_f.append(k)
    s = "".join(tag(k, fwd[k], BLUE, False) for k in shown_f)
    stages.append(step(1, s, "Inputs: x = 2, w = 0.5, b = 0.1, target y = 1"))
    labels_out.append("Inputs: x = 2, w = 0.5, b = 0.1, target y = 1")
    texts = {"mul": "Forward: u = w × x = 1", "add": "Forward: z = u + b = 1.1",
             "sub": "Forward: e = z − y = 0.1", "sq": "Forward: L = e² = 0.01"}
    for k in order_f[4:]:
        shown_f.append(k)
        s = "".join(tag(j, fwd[j], BLUE, False) for j in shown_f)
        stages.append(step(len(stages) + 1, s, texts[k]))
        labels_out.append(texts[k])
    btexts = {"sq": "Backward: start with dL/dL = 1",
              "sub": "Backward: dL/de = 2e = 0.2",
              "add": "Backward: dL/dz = 0.2 × 1 = 0.2",
              "b": "Backward: dL/db = 0.2 × 1 = 0.2",
              "mul": "Backward: dL/du = 0.2",
              "w": "Backward: dL/dw = 0.2 × x = 0.4",
              "x": "Backward: dL/dx = 0.2 × w = 0.1",
              "y": "Backward: dL/dy = −0.2, though the target is never changed"}
    shown_b = []
    for k in order_b:
        shown_b.append(k)
        s = "".join(tag(j, fwd[j], BLUE, False) for j in shown_f)
        s += "".join(tag(j, bwd[j], ORANGE, True) for j in shown_b)
        stages.append(step(len(stages) + 1, s, btexts[k]))
        labels_out.append(btexts[k])
    desc = ("A computational graph for the loss L equals w times x plus b minus y, all "
            "squared. Inputs x equals 2 and w equals 0.5 feed a multiply node giving u "
            "equals 1; u and b equals 0.1 feed an add node giving z equals 1.1; z and the "
            "target y equals 1 feed a subtract node giving e equals 0.1; a square node "
            "gives L equals 0.01. Stepping through, forward values appear in blue left to "
            "right, then gradients appear in orange right to left: 1 at L, 0.2 at e, z, "
            "b and u, 0.4 at w and 0.1 at x.")
    return figure_steps("ai-bpg", 760, 330, "".join(base), stages,
                        "Forward and backward through a computational graph", desc,
                        "Each node multiplies the gradient it receives by its own local "
                        "derivative.", labels=labels_out)


# ============================================ Level 7: the training loop

@diagram("ai-training-loop")
def _training_loop():
    """Forward, loss, backward, update: around and around."""
    cx, cy, RX, RY = 262, 168, 176, 104
    body = [text(380, 22, "The training loop: thousands of times, for every batch", 12, 650,
                 fill=MUTED)]
    body.append('<ellipse cx="%d" cy="%d" rx="%d" ry="%d" fill="none" stroke="%s" '
                'stroke-width="3" class="ai-flow" stroke-dasharray="6 8"/>' % (cx, cy, RX, RY, tv(VIOLET)))
    stations = [(-90, BLUE, "1  Forward pass", "predict for a batch"),
                (0, RED, "2  Loss", "how wrong?"),
                (90, ORANGE, "3  Backward pass", "backprop: the gradients"),
                (180, GREEN, "4  Update", "the optimiser steps")]
    for ang, colour, a, b2 in stations:
        t = math.radians(ang)
        x, y = cx + RX * math.cos(t), cy + RY * math.sin(t)
        body.append(solid(x - 72, y - 22, 144, 44, colour, a, b2, r=14, size=11, sub_size=8.6))
    for ang in (-45, 45, 135, 225):
        t = math.radians(ang)
        x, y = cx + RX * math.cos(t), cy + RY * math.sin(t)
        dx, dy = -RX * math.sin(t), RY * math.cos(t)
        n = math.hypot(dx, dy)
        body.append(arrow(x - dx / n * 10, y - dy / n * 10, x + dx / n * 10, y + dy / n * 10,
                          tv(VIOLET), 3))
    body.append(text(cx, cy - 4, "repeat for every", 10, 700, fill=MUTED))
    body.append(text(cx, cy + 12, "batch and epoch", 10, 700, fill=MUTED))
    P = Plot(548, 80, 180, 160, (0, 50), (0, 2.4))
    body.append(tint(530, 44, 220, 236, VIOLET, op=0.06, r=12))
    body.append(text(640, 62, "and the loss falls", 10.5, 800, fill=INK))
    body.append(line(P.x, P.y + P.h, P.x + P.w, P.y + P.h, stroke=LINE, w=1.2))
    body.append(line(P.x, P.y, P.x, P.y + P.h, stroke=LINE, w=1.2))
    import random
    rnd = random.Random(5)
    pts = []
    for i in range(51):
        v = 0.1 + 2.1 * math.exp(-i / 9.0) + rnd.uniform(-0.07, 0.07) * (1 + 2 * math.exp(-i / 9.0))
        pts.append("%.1f %.1f" % P.pt(i, v))
    body.append(path("M" + " L".join(pts), stroke=tv(VIOLET), w=2.4))
    body.append(text(P.x + P.w / 2, P.y + P.h + 16, "training steps", 9.4, 650, fill=MUTED))
    desc = ("A circular loop with four stations: 1, forward pass, predict for a batch; 2, "
            "loss, how wrong; 3, backward pass, backpropagation computes the gradients; "
            "4, update, the optimiser steps the weights; then back to 1. Arrows run "
            "clockwise between them, and when motion is allowed the dashes flow round the "
            "loop. In the centre: repeat for every batch and epoch. Beside it, a noisy "
            "loss curve falls steeply and then levels off over the training steps.")
    return figure("ai-tloop", 760, 300, "".join(body), "The training loop", desc,
                  "Every model in this course, from a line to a transformer, is trained "
                  "by this loop.")
