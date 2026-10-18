"""AI course diagrams, Levels 8 and 9: convolutional networks, and language
as numbers.

Every feature map, pooled value and probability shown is computed here from
the kernels and data in the figure, as in the other AI diagram modules.
"""
import math

from .diagrams import diagram
from .svg import figure, figure_steps, step, text, line, path, circle
from .diagrams_ai_kit import (INK, MUTED, FILL, FILL2, LINE, VIOLET, PINK, BLUE,
                              TEAL, GREEN, ORANGE, RED, INDIGO, AMBER, LIME,
                              CYAN, ROSE, SKY, PURPLE, SLATE, WHITE, DARK, tv,
                              solid, tint, grad, glow, plasma, diverging, ink_on,
                              arrow, neuron, cube, project)
from .diagrams_ai2 import Plot, _halo


def _conv(img, k):
    n, m = len(img), len(k)
    w = len(img[0])
    return [[sum(img[r + i][c + j] * k[i][j] for i in range(m) for j in range(m))
             for c in range(w - m + 1)] for r in range(n - m + 1)]


def _grid(x, y, vals, cell, colour_fn, fmt="%g", size=10, gap=2, stroke=None):
    out = []
    for i, row in enumerate(vals):
        for j, v in enumerate(row):
            col = colour_fn(v)
            out.append('<rect x="%.1f" y="%.1f" width="%s" height="%s" rx="3" fill="%s"%s/>'
                       % (x + j * (cell + gap), y + i * (cell + gap), cell, cell, col,
                          ' stroke="%s"' % stroke if stroke else ""))
            if fmt:
                out.append(text(x + j * (cell + gap) + cell / 2.0, y + i * (cell + gap) + cell / 2.0
                                + size * 0.36, (fmt % v).replace("-", "−"), size, 700,
                                fill=ink_on(col)))
    return "".join(out)


def _grey(v, hi=9.0):
    t = max(0.0, min(1.0, v / hi))
    g = int(30 + 215 * t)
    return "#%02X%02X%02X" % (g, g, g)


# ======================================== Level 8: a kernel, sliding

_EDGE_IMG = [[0, 0, 0, 9, 9, 9], [0, 0, 0, 9, 9, 9], [0, 0, 0, 9, 9, 9],
             [0, 0, 9, 9, 9, 9], [0, 0, 9, 9, 9, 9], [0, 0, 9, 9, 9, 9]]
_EDGE_K = [[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]]


@diagram("ai-convolution")
def _convolution():
    """A 3 × 3 vertical edge kernel sliding over a 6 × 6 image, step by step."""
    out = _conv(_EDGE_IMG, _EDGE_K)
    C = 36
    IX, IY = 30, 58
    KX, KY = 300, 104
    OX, OY = 520, 76

    def out_colour(v):
        return diverging(max(-1, min(1, v / 27.0)))
    base = [text(380, 22, "Convolution: multiply the patch by the kernel, add, move on", 12, 650,
                 fill=MUTED)]
    base.append(text(IX + 3 * C, IY - 12, "input image, 6 × 6", 10.5, 800, fill=INK))
    base.append(_grid(IX, IY, _EDGE_IMG, C - 4, _grey, "%g", 11, 4))
    base.append(text(KX + 1.5 * C - 6, KY - 12, "kernel", 10.5, 800, fill=INK))
    base.append(_grid(KX, KY, _EDGE_K, C - 8, lambda v: diverging(v * 0.8), "%g", 11, 4))
    base.append(text(KX + 1.5 * C - 6, KY + 3 * C + 10, "vertical edges", 9.4, 650, fill=MUTED))
    base.append(text(OX + 2 * C, OY - 12, "feature map, 4 × 4", 10.5, 800, fill=INK))
    for i in range(4):
        for j in range(4):
            base.append('<rect x="%d" y="%d" width="%d" height="%d" rx="3" fill="none" '
                        'stroke="%s" stroke-dasharray="3 3"/>' % (OX + j * C, OY + i * C, C - 4, C - 4, LINE))
    order = [(0, 0), (0, 1), (0, 2), (0, 3), (1, 0), (1, 1), (2, 1), (3, 2)]
    stages, labels = [], []
    done = set()
    for n, (r, c) in enumerate(order):
        done.add((r, c))
        s = []
        s.append('<rect x="%.1f" y="%.1f" width="%d" height="%d" rx="6" fill="%s" '
                 'fill-opacity="0.12" stroke="%s" stroke-width="3.2"/>'
                 % (IX + c * C - 3, IY + r * C - 3, 3 * C + 2, 3 * C + 2, AMBER, AMBER))
        for (rr, cc) in done:
            v = out[rr][cc]
            col = out_colour(v)
            s.append('<rect x="%d" y="%d" width="%d" height="%d" rx="3" fill="%s" stroke="%s" '
                     'stroke-width="%s"/>' % (OX + cc * C, OY + rr * C, C - 4, C - 4, col,
                                              AMBER if (rr, cc) == (r, c) else "none",
                                              3 if (rr, cc) == (r, c) else 0))
            s.append(text(OX + cc * C + (C - 4) / 2.0, OY + rr * C + 21, str(v), 11, 750,
                          fill=ink_on(col)))
        terms = []
        for i in range(3):
            left, right = _EDGE_IMG[r + i][c], _EDGE_IMG[r + i][c + 2]
            terms.append("(%d − %d)" % (right, left))
        s.append(path("M%.1f %.1f C %.1f %.1f, %.1f %.1f, %.1f %.1f"
                      % (IX + c * C + 3 * C, IY + r * C + 1.5 * C, 440, 300, 470, 300,
                         OX + c * C + (C - 4) / 2.0, OY + r * C + C), stroke=AMBER, w=1.8, dash="4 3"))
        s.append(text(380, 318, "row by row: " + " + ".join(terms) + " = %d" % out[r][c], 10.5, 750,
                      fill=INK, mono=True))
        lab = ("Position row %d, column %d: %s = %d" % (r + 1, c + 1, " + ".join(terms), out[r][c]))
        stages.append(step(n + 1, "".join(s), lab))
        labels.append(lab)
    full = []
    for rr in range(4):
        for cc in range(4):
            v = out[rr][cc]
            col = out_colour(v)
            full.append('<rect x="%d" y="%d" width="%d" height="%d" rx="3" fill="%s"/>'
                        % (OX + cc * C, OY + rr * C, C - 4, C - 4, col))
            full.append(text(OX + cc * C + (C - 4) / 2.0, OY + rr * C + 21, str(v), 11, 750,
                             fill=ink_on(col)))
    full.append(text(380, 318, "the feature map is brightest exactly where the image has a "
                     "vertical edge", 10.5, 750, fill=INK))
    lab = "Complete: the feature map lights up along the edge, and is 0 on flat areas"
    stages.append(step(len(stages) + 1, "".join(full), lab))
    labels.append(lab)
    desc = ("A stepped animation. A 6 by 6 greyscale image is dark on the left and "
            "bright on the right, with the boundary one column further left in the "
            "bottom three rows. A 3 by 3 kernel with columns of minus 1, 0 and 1 "
            "detects vertical edges. An amber window slides across the image; at each "
            "position the sum of the right column minus the left column fills one cell "
            "of a 4 by 4 feature map. The finished map reads, row by row: %s. It is "
            "large where the window straddles the edge and 0 on flat areas."
            % "; ".join(", ".join(str(v) for v in row) for row in out))
    return figure_steps("ai-conv", 760, 334, "".join(base), stages,
                        "A convolution, step by step", desc,
                        "The same nine weights are used at every position: weight sharing.",
                        labels=labels)


# ================================================ Level 8: four kernels

def _house():
    n = 14
    img = [[0] * n for _ in range(n)]
    for r in range(6, 12):
        for c in range(3, 11):
            img[r][c] = 9
    for r in range(2, 6):
        half = r - 1
        for c in range(7 - half, 7 + half):
            img[r][c] = 9
    for r in range(8, 12):
        for c in range(6, 8):
            img[r][c] = 0
    return img


@diagram("ai-kernels")
def _kernels():
    """One picture through four kernels: two edge detectors, blur and sharpen."""
    img = _house()
    ks = [("vertical edges", [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]], 1.0),
          ("horizontal edges", [[-1, -2, -1], [0, 0, 0], [1, 2, 1]], 1.0),
          ("blur", [[1, 1, 1], [1, 1, 1], [1, 1, 1]], 1 / 9.0),
          ("sharpen", [[0, -1, 0], [-1, 5, -1], [0, -1, 0]], 1.0)]
    body = [text(380, 22, "One picture, four kernels, four different feature maps", 12, 650,
                 fill=MUTED)]
    c = 9
    body.append(tint(14, 40, 152, 210, SLATE, op=0.06, r=12))
    body.append(text(90, 60, "input", 10.5, 800, fill=INK))
    body.append(_grid(24, 76, img, c - 1, _grey, None, gap=1))
    for k, (name, kern, scale) in enumerate(ks):
        fm = _conv(img, kern)
        fm = [[v * scale for v in row] for row in fm]
        hi = max(abs(v) for row in fm for v in row) or 1
        x0 = 180 + k * 146
        body.append(tint(x0, 40, 138, 210, VIOLET, op=0.06, r=12))
        body.append(text(x0 + 69, 60, name, 10, 800, fill=INK))
        if name in ("blur", "sharpen"):
            body.append(_grid(x0 + 10, 76, fm, c - 1,
                              lambda v, hi=hi: plasma(max(0, min(1, v / hi))), None, gap=1))
        else:
            body.append(_grid(x0 + 10, 76, fm, c - 1,
                              lambda v, hi=hi: diverging(v / hi), None, gap=1))
        for r in range(3):
            row = " ".join(("%g" % v).replace("-", "−") for v in kern[r])
            if scale < 1 and r == 1:
                row += "  ÷ 9"
            body.append(text(x0 + 69, 206 + r * 12, row, 8.8, 650, fill=MUTED, mono=True))
    body.append(text(380, 272, "pink: strong positive response · blue: strong negative · "
                     "edge maps outline the house", 9.4, 650, fill=MUTED))
    desc = ("A 14 by 14 picture of a bright house on a dark background, with a pointed "
            "roof and a dark door, passed through four kernels. The vertical edge kernel "
            "lights up the walls and door edges, pink on the left of bright areas and "
            "blue on the right. The horizontal edge kernel lights up the roof line, the "
            "floor and the top of the door. The blur kernel, every weight one ninth, "
            "gives a softened copy. The sharpen kernel, 5 in the centre and minus 1 on "
            "four sides, exaggerates the outline.")
    return figure("ai-kern", 760, 290, "".join(body), "Kernels and their feature maps", desc,
                  "A CNN learns its own kernels, and the first layer's often look just like these.")


# =========================================== Level 8: stride and padding

@diagram("ai-stride-padding")
def _stride_padding():
    """Padding keeps the size; stride 2 halves it."""
    body = [text(380, 22, "Padding keeps the size; a bigger stride shrinks it", 12, 650,
                 fill=MUTED)]
    C = 24
    # padding: 5x5 image with a ring of zeros
    body.append(tint(14, 40, 360, 260, TEAL, op=0.06, r=12))
    body.append(text(194, 60, "padding 1, stride 1: 5 × 5 in, 5 × 5 out", 10.5, 800, fill=INK))
    x0, y0 = 40, 80
    for i in range(7):
        for j in range(7):
            pad = i in (0, 6) or j in (0, 6)
            body.append('<rect x="%d" y="%d" width="%d" height="%d" rx="3" fill="%s" '
                        'fill-opacity="%s" stroke="%s" %s/>'
                        % (x0 + j * C, y0 + i * C, C - 3, C - 3, FILL if pad else TEAL,
                           "1" if pad else "0.55", LINE, 'stroke-dasharray="3 2"' if pad else ""))
            if pad:
                body.append(text(x0 + j * C + 10.5, y0 + i * C + 15, "0", 9, 650, fill=MUTED))
    body.append('<rect x="%d" y="%d" width="%d" height="%d" rx="5" fill="none" stroke="%s" '
                'stroke-width="3"/>' % (x0 - 2, y0 - 2, 3 * C + 1, 3 * C + 1, AMBER))
    body.append(arrow(x0 + 7 * C + 8, y0 + 3.5 * C, x0 + 7 * C + 40, y0 + 3.5 * C, LINE, 2))
    ox = x0 + 7 * C + 48
    for i in range(5):
        for j in range(5):
            body.append('<rect x="%d" y="%d" width="%d" height="%d" rx="3" fill="%s" '
                        'fill-opacity="%s"/>' % (ox + j * 22, y0 + C + i * 22, 19, 19, VIOLET,
                                                 "0.9" if (i, j) == (0, 0) else "0.35"))
    body.append(text(194, 286, "the kernel can now sit on the corner pixel", 9.4, 650, fill=MUTED))
    # stride 2: 7x7 image, positions every 2
    body.append(tint(388, 40, 358, 260, ORANGE, op=0.06, r=12))
    body.append(text(567, 60, "no padding, stride 2: 7 × 7 in, 3 × 3 out", 10.5, 800, fill=INK))
    x1 = 404
    for i in range(7):
        for j in range(7):
            body.append('<rect x="%d" y="%d" width="%d" height="%d" rx="3" fill="%s" '
                        'fill-opacity="0.45"/>' % (x1 + j * C, y0 + i * C, C - 3, C - 3, ORANGE))
    for k, colour in enumerate((AMBER, PINK, CYAN)):
        body.append('<rect x="%d" y="%d" width="%d" height="%d" rx="5" fill="none" stroke="%s" '
                    'stroke-width="3"%s/>' % (x1 + 2 * k * C - 2, y0 - 2, 3 * C + 1, 3 * C + 1,
                                              colour, ' stroke-dasharray="6 3"' if k else ""))
    body.append(text(x1 + 3.5 * C, y0 + 7 * C + 16, "the window jumps 2 pixels each time", 9.4,
                     650, fill=MUTED))
    body.append(arrow(x1 + 7 * C + 6, y0 + 3.5 * C, x1 + 7 * C + 30, y0 + 3.5 * C, LINE, 2))
    ox = x1 + 7 * C + 36
    cols = [AMBER, PINK, CYAN]
    for i in range(3):
        for j in range(3):
            body.append('<rect x="%d" y="%d" width="%d" height="%d" rx="3" fill="%s" '
                        'fill-opacity="%s"/>' % (ox + j * 26, y0 + 2 * C + i * 26, 22, 22,
                                                 cols[j] if i == 0 else ORANGE,
                                                 "1" if i == 0 else "0.45"))
    body.append(text(567, 286, "(7 − 3) ÷ 2 + 1 = 3", 10, 750, fill=INK, mono=True))
    desc = ("Two panels. With padding 1 and stride 1, a 5 by 5 image is surrounded by a "
            "ring of zeros, so a 3 by 3 window can sit on the corner pixel, and the output "
            "is also 5 by 5. With no padding and stride 2, a 3 by 3 window on a 7 by 7 "
            "image jumps two pixels at a time, shown by three outlined positions along "
            "the top row, giving a 3 by 3 output: 7 minus 3, divided by 2, plus 1, "
            "equals 3.")
    return figure("ai-strpad", 760, 310, "".join(body), "Padding and stride", desc,
                  "Output size = (n + 2p − k) ÷ s + 1.")


# ======================================= Level 8: kernels over a volume

@diagram("ai-conv-volume")
def _conv_volume():
    """A 3 × 3 × 3 kernel over an RGB volume; 8 filters make 8 feature maps."""
    body = [text(380, 22, "On colour images a kernel is a small block; many filters make a "
                 "stack of maps", 12, 650, fill=MUTED)]
    # input volume: three channel slabs
    for k, colour in ((2, BLUE), (1, GREEN), (0, RED)):
        body.append(cube(60 + k * 22, 96 - k * 14, 168, 168, 14, colour, op=0.9))
    body.append(text(156, 300, "input: 32 × 32 × 3", 10.5, 800, fill=INK))
    body.append(text(156, 316, "red, green and blue channels", 9.4, 650, fill=MUTED))
    # the kernel block on the input
    body.append(cube(120, 150, 42, 42, 44, AMBER, op=0.92))
    body.append(text(141, 176, "3×3×3", 9, 800, fill=DARK))
    # output volume: 8 maps
    cols = [VIOLET, PINK, INDIGO, TEAL, ORANGE, BLUE, GREEN, RED]
    for k in reversed(range(8)):
        body.append(cube(486 + k * 12, 100 - k * 8, 150, 150, 6, cols[k], op=0.92))
    body.append('<rect x="%d" y="%d" width="20" height="20" fill="%s" stroke="%s" '
                'stroke-width="2"/>' % (520, 140, AMBER, DARK))
    body.append(path("M162 150 C 300 70, 400 80, 520 140", stroke=tv(ORANGE), w=2.2, dash="6 4"))
    body.append(path("M162 192 C 300 260, 420 220, 520 160", stroke=tv(ORANGE), w=2.2, dash="6 4"))
    body.append(tint(286, 120, 164, 92, ORANGE, op=0.1, r=12))
    body.append(text(368, 144, "27 weights + 1 bias", 10, 800, fill=INK))
    body.append(text(368, 162, "one number per position", 9.4, 650, fill=MUTED))
    body.append(text(368, 180, "× 8 different filters", 9.4, 650, fill=MUTED))
    body.append(text(368, 198, "= 224 parameters", 9.6, 750, fill=tv(ORANGE)))
    body.append(text(610, 300, "output: 32 × 32 × 8", 10.5, 800, fill=INK))
    body.append(text(610, 316, "8 feature maps, one per filter", 9.4, 650, fill=MUTED))
    desc = ("On the left an input volume of 32 by 32 by 3, three stacked slabs for the "
            "red, green and blue channels. A small amber block, a 3 by 3 by 3 kernel, sits "
            "on it, covering all three channels of a patch. Dashed lines lead from it to "
            "one cell of an output volume on the right, a stack of 8 coloured feature "
            "maps, 32 by 32 by 8, one per filter. A note says each filter has 27 weights "
            "and a bias, gives one number per position, and 8 filters make 224 "
            "parameters.")
    return figure("ai-cvol", 760, 330, "".join(body), "A convolutional layer on a colour image",
                  desc, "Each filter spans every input channel and produces one feature map.")


# ================================================ Level 8: max pooling

@diagram("ai-pooling")
def _pooling():
    """2 × 2 max pooling, with the winning value in each block highlighted."""
    fm = [[1, 3, 0, 2], [4, 6, 1, 0], [0, 2, 8, 5], [1, 1, 3, 7]]
    blocks = [[VIOLET, TEAL], [ORANGE, PINK]]
    C = 52
    body = [text(380, 22, "2 × 2 max pooling: keep the strongest value in each block", 12, 650,
                 fill=MUTED)]
    X0, Y0 = 80, 64
    for i in range(4):
        for j in range(4):
            col = blocks[i // 2][j // 2]
            bi, bj = (i // 2) * 2, (j // 2) * 2
            block = [fm[bi + a][bj + b] for a in range(2) for b in range(2)]
            win = fm[i][j] == max(block)
            body.append('<rect x="%d" y="%d" width="%d" height="%d" rx="6" fill="%s" '
                        'fill-opacity="%s"%s/>' % (X0 + j * C, Y0 + i * C, C - 6, C - 6, col,
                                                   "1" if win else "0.22",
                                                   ' stroke="%s" stroke-width="3"' % AMBER if win else ""))
            body.append(text(X0 + j * C + (C - 6) / 2.0, Y0 + i * C + 31, str(fm[i][j]), 15, 800,
                             fill=WHITE if win else INK))
    body.append(text(X0 + 2 * C - 3, Y0 + 4 * C + 18, "feature map, 4 × 4", 10.5, 800, fill=INK))
    body.append(arrow(X0 + 4 * C + 20, Y0 + 2 * C - 3, X0 + 4 * C + 120, Y0 + 2 * C - 3, LINE, 2.6))
    body.append(text(X0 + 4 * C + 70, Y0 + 2 * C - 14, "max", 11, 800, fill=MUTED))
    P0 = X0 + 4 * C + 140
    for i in range(2):
        for j in range(2):
            v = max(fm[i * 2 + a][j * 2 + b] for a in range(2) for b in range(2))
            body.append('<rect x="%d" y="%d" width="%d" height="%d" rx="8" fill="%s"/>'
                        % (P0 + j * 70, Y0 + 34 + i * 70, 62, 62, blocks[i][j]))
            body.append(text(P0 + j * 70 + 31, Y0 + 34 + i * 70 + 39, str(v), 18, 800, fill=WHITE))
    body.append(text(P0 + 66, Y0 + 4 * C + 18, "pooled, 2 × 2", 10.5, 800, fill=INK))
    body.append(tint(576, 70, 176, 150, SLATE, op=0.07, r=12))
    for i, t in enumerate(["16 values become 4", "no parameters to learn",
                           "small shifts matter less", "later layers see more"]):
        body.append(text(590, 104 + i * 28, "• " + t, 9.2, 700, anchor="start", fill=INK))
    desc = ("A 4 by 4 feature map divided into four coloured 2 by 2 blocks: 1, 3, 4, 6; 0, "
            "2, 1, 0; 0, 2, 1, 1; and 8, 5, 3, 7. In each block the largest value is "
            "highlighted: 6, 2, 2 and 8. Max pooling keeps only those, giving a 2 by 2 "
            "output of 6, 2, 2, 8. Notes: 16 values become 4, there are no parameters, "
            "small shifts change little, and the next layer sees a bigger patch.")
    return figure("ai-pool", 760, 300, "".join(body), "Max pooling", desc,
                  "Pooling summarises; it does not learn.")


# ============================================ Level 8: a whole CNN in 3D

@diagram("ai-cnn-architecture")
def _cnn_architecture():
    """Image to softmax: volumes shrink in size and grow in depth."""
    body = [text(380, 22, "A small CNN: the maps get smaller while the channels multiply",
                 12, 650, fill=MUTED)]
    stages = [  # x, size px, depth px, colour, name, shape
        (20, 120, 8, BLUE, "input", "32×32×3"),
        (130, 120, 26, VIOLET, "conv + ReLU", "32×32×16"),
        (252, 66, 26, TEAL, "max pool", "16×16×16"),
        (341, 66, 48, VIOLET, "conv + ReLU", "16×16×32"),
        (445, 36, 48, TEAL, "max pool", "8×8×32"),
    ]
    base_y = 230
    for x, s, d, colour, name, shape in stages:
        y = base_y - s
        body.append(cube(x, y, s * 0.62, s, d, colour, op=0.95))
        body.append(text(x + s * 0.31 + d * 0.35, base_y + 26, name, 9.6, 800, fill=tv(colour)))
        body.append(text(x + s * 0.31 + d * 0.35, base_y + 40, shape, 9, 650, fill=MUTED, mono=True))
    rights = [x + s * 0.62 + d * 0.7 for x, s, d, _c, _n, _s in stages]
    lefts = [x for x, _s, _d, _c, _n, _sh in stages] + [531]
    for x0, x1 in zip(rights, lefts[1:]):
        body.append(arrow(x0 + 4, base_y - 30, x1 - 4, base_y - 30, LINE, 1.8))
    # flatten, dense, softmax as bars
    bars = [(531, 150, PINK, "flatten", "2,048"), (582, 84, PINK, "dense", "128"),
            (633, 46, ORANGE, "softmax", "10")]
    for x, h, colour, name, shape in bars:
        body.append(cube(x, base_y - h, 14, h, 10, colour, op=0.95))
        body.append(text(x + 10, base_y + 26, name, 9.6, 800, fill=tv(colour)))
        body.append(text(x + 10, base_y + 40, shape, 9, 650, fill=MUTED, mono=True))
    body.append(arrow(556, base_y - 30, 578, base_y - 30, LINE, 1.8))
    body.append(arrow(607, base_y - 30, 629, base_y - 30, LINE, 1.8))
    for k, (lab, p) in enumerate([("cat", 0.82), ("dog", 0.11), ("fox", 0.04)]):
        y = base_y - 74 + k * 18
        body.append('<rect x="662" y="%d" width="%.1f" height="12" rx="3" fill="%s"/>'
                    % (y, p * 40, ORANGE))
        body.append(text(666 + p * 40 + 2, y + 10, "%s %.2f" % (lab, p), 9, 700, anchor="start",
                         fill=INK))
    body.append(tint(24, 286, 712, 34, VIOLET, op=0.08, r=10))
    body.append(text(380, 308, "feature detection: convolution, ReLU, pooling, repeated  →  "
                     "classification: flatten, dense, softmax", 10, 700, fill=INK))
    desc = ("A pipeline of 3D blocks from left to right. The input image, 32 by 32 by 3, is "
            "a tall thin blue block. A convolution with ReLU gives 32 by 32 by 16, the "
            "same height but deeper, in violet. Max pooling halves it to 16 by 16 by 16, "
            "in teal. Another convolution gives 16 by 16 by 32, deeper again, and pooling "
            "gives 8 by 8 by 32. Then the volume is flattened into 2,048 numbers, a thin "
            "pink bar, followed by a dense layer of 128 and a softmax layer of 10 classes, "
            "shown as probabilities cat 0.82, dog 0.11 and fox 0.04.")
    return figure("ai-cnnarch", 760, 330, "".join(body), "The architecture of a CNN", desc,
                  "Where becomes what: fewer positions, richer descriptions of each.")


# =========================================== Level 8: the receptive field

def _plane(x, y, n, cell, colour, hi=None, hi2=None, skew=0.55):
    """An n × n grid drawn as a tilted plane; hi is (r0, c0, size) to highlight."""
    out = []
    for i in range(n):
        for j in range(n):
            px = x + j * cell + i * cell * skew
            py = y + i * cell * 0.5
            pts = [(px, py), (px + cell, py), (px + cell + cell * skew, py + cell * 0.5),
                   (px + cell * skew, py + cell * 0.5)]
            on = hi and hi[0] <= i < hi[0] + hi[2] and hi[1] <= j < hi[1] + hi[2]
            out.append('<polygon points="%s" fill="%s" fill-opacity="%s" stroke="%s" '
                       'stroke-width="0.8"/>' % (" ".join("%.1f,%.1f" % p for p in pts),
                                                 colour, "0.95" if on else "0.18", FILL))
    return "".join(out)


@diagram("ai-receptive-field")
def _receptive_field():
    """One value two layers up sees a 5 × 5 patch of the input."""
    body = [text(380, 22, "Each layer up sees a bigger patch of the image", 12, 650,
                 fill=MUTED)]
    cell = 26
    body.append(_plane(250, 48, 3, cell, PINK, (1, 1, 1)))
    body.append(_plane(197, 112, 5, cell, VIOLET, (1, 1, 3)))
    body.append(_plane(144, 196, 7, cell, BLUE, (1, 1, 5)))
    for lab, sub, y, colour in (("layer 2", "1 value", 70, PINK),
                                ("layer 1", "sees 3 × 3 of layer 1 below it", 150, VIOLET),
                                ("input", "a 5 × 5 patch of the image", 250, BLUE)):
        body.append(text(540, y, lab, 11, 800, anchor="start", fill=tv(colour)))
    body.append(text(540, 86, "its receptive field grows", 9.4, 650, anchor="start", fill=MUTED))
    body.append(text(540, 166, "each of those sees 3 × 3", 9.4, 650, anchor="start", fill=MUTED))
    body.append(text(540, 266, "5 × 5 in total", 9.4, 650, anchor="start", fill=MUTED))
    # cone lines from the top cell to the bottom patch corners
    top = (250 + cell + cell * 0.55 + cell / 2, 48 + cell * 0.5 + cell * 0.25)
    for (i, j) in ((1, 1), (1, 6), (6, 1), (6, 6)):
        px = 144 + j * cell + i * cell * 0.55
        py = 196 + i * cell * 0.5
        body.append(line(top[0], top[1], px, py, stroke=tv(PINK), w=1.2, dash="4 3"))
    desc = ("Three tilted grids stacked like floors: the input, 7 by 7, at the bottom; "
            "layer 1, 5 by 5, in the middle; layer 2, 3 by 3, on top. One cell of layer "
            "2 is highlighted. It depends on a highlighted 3 by 3 block of layer 1, each "
            "of which depends on 3 by 3 of the input, so it sees a highlighted 5 by 5 "
            "patch of the input. Dashed lines from the top cell to the corners of that "
            "patch form a cone.")
    return figure("ai-rfield", 760, 330, "".join(body), "Receptive fields grow with depth", desc,
                  "Stacked 3 × 3 convolutions see 5 × 5, then 7 × 7: bigger things deeper down.")


# ============================================ Level 8: a residual block

@diagram("ai-resnet-block")
def _resnet_block():
    """F(x) + x, with the gradient flowing straight back along the shortcut."""
    body = [text(380, 22, "A residual block: learn the change, keep the original", 12, 650,
                 fill=MUTED)]
    y = 150
    body.append(solid(30, y - 22, 64, 44, BLUE, "x", r=12, size=16))
    boxes = [(150, VIOLET, "conv 3×3"), (276, TEAL, "ReLU"), (402, VIOLET, "conv 3×3")]
    prev = 94
    for x, colour, lab in boxes:
        body.append(arrow(prev, y, x - 4, y, LINE, 2.2))
        body.append(solid(x, y - 24, 100, 48, colour, lab, r=12, size=11.5))
        prev = x + 100
    body.append(arrow(prev, y, 556, y, LINE, 2.2))
    body.append('<circle cx="578" cy="%d" r="20" fill="%s"/>' % (y, ORANGE))
    body.append(text(578, y + 7, "+", 22, 800, fill=WHITE))
    body.append(arrow(598, y, 640, y, LINE, 2.2))
    body.append(solid(644, y - 22, 92, 44, PINK, "F(x) + x", r=12, size=12))
    body.append(text(326, y + 50, "F(x): the layers learn only the change", 10, 700,
                     fill=tv(VIOLET)))
    # shortcut
    body.append(path("M62 %d C 62 50, 578 50, 578 %d" % (y - 22, y - 20), stroke=tv(ORANGE), w=3.2))
    body.append(arrow(578, y - 40, 578, y - 22, tv(ORANGE), 3.2))
    body.append(text(320, 66, "identity shortcut: x skips the layers and is added back", 10.5,
                     800, fill=tv(ORANGE)))
    # gradient path
    body.append(path("M600 %d C 600 258, 40 258, 40 %d" % (y + 40, y + 26), stroke=tv(RED), w=2.4,
                     dash="7 5"))
    body.append(arrow(44, y + 40, 40, y + 24, tv(RED), 2.4))
    body.append(text(320, 268, "backward: the gradient also flows straight back along the "
                     "shortcut, so it cannot vanish", 10, 750, fill=tv(RED)))
    desc = ("An input x passes through a 3 by 3 convolution, a ReLU and another 3 by 3 "
            "convolution, which compute F of x, the change to learn. An orange shortcut "
            "arc carries x straight past the layers to an adding node, giving the output "
            "F of x plus x. A dashed red arrow below shows the gradient flowing straight "
            "back along the shortcut during training, so it cannot vanish.")
    return figure("ai-resblk", 760, 300, "".join(body), "A residual block", desc,
                  "If a block has nothing useful to add, it can learn F(x) = 0 and pass x "
                  "through untouched.")


# ============================================ Level 8: data augmentation

_CAT = ["..........", ".X......X.", ".XX....XX.", ".XXXXXXXX.", ".XGXXXXGX.",
        ".XXXXXXXX.", ".XXXPPXXX.", "..XXXXXX..", "...XXXX...", ".........."]


def _cat_pixels(x, y, s, palette):
    out = []
    for i, row in enumerate(_CAT):
        for j, ch in enumerate(row):
            if ch == ".":
                continue
            out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s"/>'
                       % (x + j * s, y + i * s, s + 0.2, s + 0.2, palette[ch]))
    return "".join(out)


@diagram("ai-augmentation")
def _augmentation():
    """One training image becomes six, each with the same label."""
    body = [text(380, 22, "Data augmentation: one labelled image, many training examples",
                 12, 650, fill=MUTED)]
    body.append('<defs><filter id="ai-aug-hue"><feColorMatrix type="hueRotate" values="70"/>'
                '</filter><clipPath id="ai-aug-clip"><rect x="0" y="0" width="80" height="80"/>'
                '</clipPath></defs>')
    pal = {"X": "#EA580C", "G": "#16A34A", "P": "#DB2777"}
    s = 8
    body.append(tint(20, 46, 130, 160, SLATE, op=0.07, r=12))
    body.append('<rect x="45" y="70" width="80" height="80" rx="6" fill="%s"/>' % SKY)
    body.append(_cat_pixels(45, 70, s, pal))
    body.append(text(85, 172, "original", 10, 800, fill=INK))
    body.append(text(85, 188, "label: cat", 9.4, 650, fill=MUTED))
    variants = [("flipped", "translate(80 0) scale(-1 1)", None),
                ("rotated", "rotate(14 40 40)", None),
                ("cropped and zoomed", "translate(-16 -10) scale(1.35)", "clip"),
                ("brighter", "", "bright"),
                ("colours shifted", "", "hue"),
                ("noisy", "", "noise")]
    import random
    rnd = random.Random(4)
    for k, (name, tr, extra) in enumerate(variants):
        col, row = k % 3, k // 3
        x0, y0 = 196 + col * 186, 46 + row * 128
        body.append(tint(x0, y0, 172, 116, VIOLET, op=0.06, r=12))
        gx, gy = x0 + 14, y0 + 14
        inner = ('<rect x="0" y="0" width="80" height="80" rx="6" fill="%s"/>' % SKY
                 + _cat_pixels(0, 0, s, pal))
        attrs = ""
        if extra == "hue":
            attrs = ' filter="url(#ai-aug-hue)"'
        g = '<g transform="translate(%d %d)"><g clip-path="url(#ai-aug-clip)"><g transform="%s"%s>%s</g>' \
            % (gx, gy, tr, attrs, inner)
        if extra == "bright":
            g += '<rect x="0" y="0" width="80" height="80" fill="#FFFFFF" fill-opacity="0.4"/>'
        if extra == "noise":
            for _ in range(70):
                g += ('<rect x="%.1f" y="%.1f" width="3" height="3" fill="%s" fill-opacity="0.8"/>'
                      % (rnd.uniform(0, 77), rnd.uniform(0, 77), rnd.choice(["#FFFFFF", "#111827"])))
        g += '</g></g>'
        body.append(g)
        body.append(text(x0 + 132, y0 + 48, "still", 9.4, 650, fill=MUTED))
        body.append(text(x0 + 132, y0 + 62, "a cat", 9.4, 800, fill=INK))
        body.append(text(x0 + 86, y0 + 108, name, 9.6, 750, fill=INK))
    desc = ("A pixel-art cat on a blue background, labelled cat, becomes six training "
            "examples: flipped left to right, rotated slightly, cropped and zoomed, made "
            "brighter, with its colours shifted, and with random noise added. Each is "
            "still labelled cat.")
    return figure("ai-aug", 760, 312, "".join(body), "Data augmentation", desc,
                  "The network learns that flips, crops and lighting do not change what "
                  "the object is.")


# ================================================ Level 9: tokenisation

@diagram("ai-tokenisation")
def _tokenisation():
    """One sentence split into characters, words and subword tokens."""
    body = [text(380, 22, "Three ways to cut text into pieces", 12, 650, fill=MUTED)]
    sentence = "Unbelievably, transformers tokenise text!"
    rows = [("characters", list(sentence[:30]) + ["…"], 9.2, 0),
            ("words", ["Unbelievably", ",", "transformers", "tokenise", "text", "!"], 10.5, 0),
            ("subword tokens", ["Un", "believ", "ably", ",", " transform", "ers", " token", "ise",
                                " text", "!"], 10.5, 1)]
    ids = [1844, 22324, 2915, 11, 6121, 364, 11241, 786, 2420, 0]
    cycle = [VIOLET, PINK, BLUE, TEAL, ORANGE, GREEN, INDIGO, RED]
    y = 58
    for name, pieces, size, show_ids in rows:
        body.append(text(20, y + 20, name, 10.5, 800, anchor="start", fill=INK))
        x = 146
        for k, p in enumerate(pieces):
            shown = p.replace(" ", "·") if p.strip() else "·"
            w = max(16, len(shown) * size * 0.62 + 12)
            col = cycle[k % len(cycle)]
            body.append(solid(x, y + 2, w, 28, col, shown, r=7, size=size))
            if show_ids:
                body.append(text(x + w / 2.0, y + 46, str(ids[k]), 8.6, 650, fill=MUTED, mono=True))
            x += w + 5
        count = len(pieces) if name != "characters" else len(sentence)
        body.append(text(740, y + 20, "%d pieces" % count, 9.6, 750, anchor="end",
                         fill=tv(VIOLET)))
        y += 72 if show_ids else 58
    body.append(text(20, y + 22, "· marks a space. Subword tokens keep common words whole and split "
                     "rare ones; each gets an ID number (shown here for illustration).", 9.4, 650,
                     anchor="start", fill=MUTED))
    desc = ("The sentence Unbelievably, transformers tokenise text! split three ways. As "
            "characters it is %d pieces, one per letter, space and punctuation mark. As "
            "words it is 6 pieces. As subword tokens it is 10 pieces: Un, believ, ably, "
            "comma, transform with its leading space, ers, token with its leading space, "
            "ise, text with its leading space, and an exclamation mark, each with an ID "
            "number." % len(sentence))
    return figure("ai-tok", 760, 260, "".join(body), "Tokenising a sentence", desc,
                  "Subwords are the compromise every modern language model uses.")


# ================================= Level 9: an embedding space in 3D

# The same hand-placed words as the embedding lab, so the picture and the
# tool agree. Directions are built in: woman = man + gender, king = man +
# royalty, and capital = country + capital-of.
WORDS3D = {
    "man": (-0.7, 0.3, 0.1), "woman": (-0.7, 0.3, 0.5), "boy": (-0.8, 0.15, 0.05),
    "girl": (-0.8, 0.15, 0.45), "king": (-0.4, 0.65, 0.1), "queen": (-0.4, 0.65, 0.5),
    "prince": (-0.5, 0.5, 0.05), "princess": (-0.5, 0.5, 0.45),
    "cat": (0.55, 0.45, -0.35), "kitten": (0.5, 0.33, -0.3), "dog": (0.66, 0.5, -0.45),
    "puppy": (0.6, 0.38, -0.42), "lion": (0.72, 0.72, -0.3), "tiger": (0.78, 0.66, -0.36),
    "horse": (0.82, 0.4, -0.62), "cow": (0.88, 0.28, -0.55),
    "apple": (0.45, -0.55, 0.5), "banana": (0.52, -0.48, 0.58), "bread": (0.6, -0.72, 0.3),
    "cheese": (0.68, -0.64, 0.36), "pizza": (0.74, -0.58, 0.24), "cake": (0.56, -0.78, 0.46),
    "car": (-0.5, -0.55, -0.35), "bus": (-0.56, -0.66, -0.28), "train": (-0.66, -0.72, -0.42),
    "bike": (-0.4, -0.48, -0.52), "plane": (-0.6, -0.38, -0.66), "boat": (-0.72, -0.56, -0.6),
    "France": (0.05, 0.0, 0.75), "Paris": (0.25, 0.2, 0.8), "Italy": (-0.1, -0.05, 0.85),
    "Rome": (0.1, 0.15, 0.9), "Germany": (0.15, -0.15, 0.7), "Berlin": (0.35, 0.05, 0.75),
}
GROUPS3D = [(VIOLET, ["man", "woman", "boy", "girl", "king", "queen", "prince", "princess"], "people"),
            (PINK, ["cat", "kitten", "dog", "puppy", "lion", "tiger", "horse", "cow"], "animals"),
            (ORANGE, ["apple", "banana", "bread", "cheese", "pizza", "cake"], "food"),
            (BLUE, ["car", "bus", "train", "bike", "plane", "boat"], "vehicles"),
            (TEAL, ["France", "Paris", "Italy", "Rome", "Germany", "Berlin"], "places")]


@diagram("ai-embedding-3d")
def _embedding_3d():
    """Word vectors as points in 3D: clusters of meaning, and a gender direction."""
    yaw, pitch, scale, ox, oy = 0.6, 0.42, 168, 330, 200

    def P(v):
        return project(v[0], v[1], v[2], yaw, pitch, scale, ox, oy)
    body = [text(380, 22, "An embedding space: similar meanings sit together", 12, 650,
                 fill=MUTED)]
    # floor grid at z = -1
    for k in range(-2, 3):
        a, b = P((k / 2.0, -1, -1)), P((k / 2.0, 1, -1))
        body.append(line(a[0], a[1], b[0], b[1], stroke=LINE, w=0.6, dash="2 4"))
        a, b = P((-1, k / 2.0, -1)), P((1, k / 2.0, -1))
        body.append(line(a[0], a[1], b[0], b[1], stroke=LINE, w=0.6, dash="2 4"))
    colour_of = {}
    for colour, ws, _n in GROUPS3D:
        for w in ws:
            colour_of[w] = colour
    items = sorted(WORDS3D.items(), key=lambda kv: -P(kv[1])[2])
    for w, v in items:
        x, y, _d = P(v)
        fx, fy, _ = P((v[0], v[1], -1))
        body.append(line(fx, fy, x, y, stroke=LINE, w=0.8, dash="1 3"))
        body.append(circle(fx, fy, 1.8, fill=LINE, stroke="none", w=0))
    for pair, colour in ((("man", "woman"), AMBER), (("king", "queen"), AMBER)):
        a, b = P(WORDS3D[pair[0]]), P(WORDS3D[pair[1]])
        body.append(arrow(a[0], a[1], b[0], b[1], colour, 2.4))
    for w, v in items:
        x, y, _d = P(v)
        body.append(circle(x, y, 5.2, fill=colour_of[w], stroke=FILL, w=1.4))
        body.append(_halo(x + 7, y - 6, w, 9, 700, "start"))
    body.append(tint(620, 56, 126, 176, SLATE, op=0.07, r=12))
    for i, (colour, _ws, name) in enumerate(GROUPS3D):
        body.append(circle(640, 80 + i * 26, 6, fill=colour, stroke=FILL, w=1.4))
        body.append(text(654, 84 + i * 26, name, 10, 700, anchor="start", fill=INK))
    body.append(line(634, 214, 656, 214, stroke=AMBER, w=2.4))
    body.append(text(662, 218, "same step", 9.4, 700, anchor="start", fill=INK))
    desc = ("A 3D scatter of 34 words, each a point with a dotted line down to a floor "
            "grid. They form five clusters: people such as man, woman, king and queen; "
            "animals such as cat, kitten, dog and lion; food such as apple, bread and "
            "pizza; vehicles such as car, bus and plane; and places such as France, "
            "Paris, Italy and Rome. Two amber arrows, from man to woman and from king to "
            "queen, point the same way and are the same length: the same step in "
            "meaning.")
    return figure("ai-emb3d", 760, 360, "".join(body), "Word embeddings in 3D", desc,
                  "Real embeddings have hundreds of dimensions; this hand-placed 3D toy "
                  "shows the idea.")


# =============================================== Level 9: cosine similarity

@diagram("ai-cosine")
def _cosine():
    """Cosine similarity at 0, 60, 90 and 180 degrees."""
    body = [text(380, 22, "Cosine similarity measures the angle, not the length", 12, 650,
                 fill=MUTED)]
    cases = [(0, "1", "same direction", GREEN, 1.6), (60, "0.5", "similar", TEAL, 1.0),
             (90, "0", "unrelated", SLATE, 1.0), (180, "−1", "opposite", RED, 1.0)]
    for k, (ang, val, lab, colour, len_b) in enumerate(cases):
        x0 = 20 + k * 184
        body.append(tint(x0, 40, 172, 190, colour, op=0.07, r=12))
        cx, cy = x0 + 86, 140
        body.append(arrow(cx, cy, cx + 62, cy, tv(VIOLET), 3))
        t = math.radians(ang)
        L = 62 * len_b * (0.7 if ang == 0 else 1)
        bx, by = cx + L * math.cos(t), cy - L * math.sin(t)
        if ang == 0:
            by -= 8
            body.append(arrow(cx, cy - 8, bx, by, tv(PINK), 3))
        else:
            body.append(arrow(cx, cy, bx, by, tv(PINK), 3))
        if 0 < ang < 180:
            body.append(path("M%.1f %.1f A 22 22 0 0 0 %.1f %.1f"
                             % (cx + 22, cy, cx + 22 * math.cos(t), cy - 22 * math.sin(t)),
                             stroke=AMBER, w=2))
        elif ang == 180:
            body.append(path("M%.1f %.1f A 22 22 0 0 0 %.1f %.1f" % (cx + 22, cy, cx - 22, cy),
                             stroke=AMBER, w=2))
        body.append(text(cx, 70, "%d°" % ang, 12, 800, fill=INK))
        body.append(text(cx, 196, "cos = " + val, 12, 800, fill=tv(colour), mono=True))
        body.append(text(cx, 214, lab, 9.6, 650, fill=MUTED))
    desc = ("Four panels, each with a violet vector and a pink vector from the same point. "
            "At 0 degrees they point the same way, cosine 1, same direction, even though "
            "the pink one is shorter. At 60 degrees, cosine 0.5, similar. At 90 degrees, "
            "cosine 0, unrelated. At 180 degrees, pointing opposite ways, cosine minus 1.")
    return figure("ai-cos", 760, 246, "".join(body), "Cosine similarity", desc,
                  "Dividing by the lengths means only the direction counts.")


# ========================================== Level 9: analogies as arrows

@diagram("ai-word-analogy")
def _word_analogy():
    """king − man + woman ≈ queen, and Paris − France + Italy ≈ Rome."""
    body = [text(380, 22, "Analogies are parallelograms: the same step from a different start",
                 12, 650, fill=MUTED)]
    panels = [(20, [("man", (0.1, 0.1)), ("woman", (0.1, 0.8)), ("king", (0.85, 0.15)),
                    ("queen", (0.85, 0.85))], ("man", "woman"), ("king", "queen"),
               "gender", "royalty", "king − man + woman ≈ queen"),
              (392, [("France", (0.1, 0.15)), ("Paris", (0.75, 0.25)), ("Italy", (0.2, 0.8)),
                     ("Rome", (0.85, 0.9))], ("France", "Paris"), ("Italy", "Rome"),
               "capital of", "country", "Paris − France + Italy ≈ Rome")]
    for x0, pts, e1, e2, lab1, lab2, eq in panels:
        body.append(tint(x0, 40, 348, 246, VIOLET, op=0.06, r=12))
        P = Plot(x0 + 40, 58, 270, 170, (0, 1), (0, 1))
        d = dict(pts)
        a, b = P.pt(*d[e1[0]]), P.pt(*d[e1[1]])
        c, f = P.pt(*d[e2[0]]), P.pt(*d[e2[1]])
        body.append(line(a[0], a[1], c[0], c[1], stroke=LINE, w=1.6, dash="5 4"))
        body.append(line(b[0], b[1], f[0], f[1], stroke=LINE, w=1.6, dash="5 4"))
        body.append(arrow(a[0], a[1], b[0], b[1], AMBER, 3))
        body.append(arrow(c[0], c[1], f[0], f[1], AMBER, 3))
        mx, my = (a[0] + b[0]) / 2.0, (a[1] + b[1]) / 2.0
        body.append(_halo(mx - 8, my, lab1, 9.4, 800, "end"))
        mx2, my2 = (a[0] + c[0]) / 2.0, (a[1] + c[1]) / 2.0
        body.append(_halo(mx2, my2 + 16, lab2, 9.4, 700))
        for name, (u, v) in pts:
            x, y = P.pt(u, v)
            body.append(circle(x, y, 7, fill=VIOLET if name not in (e2[1],) else PINK,
                               stroke=FILL, w=1.6))
            body.append(_halo(x + 11, y + 4, name, 10.5, 800, "start"))
        body.append(text(x0 + 174, 270, eq, 10.5, 800, fill=INK, mono=True))
    desc = ("Two panels. In the first, the points man, woman, king and queen form a "
            "parallelogram: an amber arrow labelled gender goes from man to woman, and an "
            "identical amber arrow goes from king to queen, so king minus man plus woman "
            "lands near queen. In the second, France, Paris, Italy and Rome form a "
            "parallelogram: the arrow labelled capital of goes from France to Paris and "
            "the same arrow from Italy to Rome, so Paris minus France plus Italy lands "
            "near Rome.")
    return figure("ai-analogy", 760, 300, "".join(body), "Word analogies as vector arithmetic",
                  desc, "In real embeddings the parallelograms are only approximate.")


# ============================================== Level 9: next token

@diagram("ai-next-token")
def _next_token():
    """A context, a model, and a probability for every candidate next word."""
    body = [text(380, 22, "A language model predicts a probability for every next token", 12,
                 650, fill=MUTED)]
    ctx = ["The", "keys", "to", "the", "cabinet"]
    x = 22
    for w in ctx:
        wd = 18 + len(w) * 8.6
        body.append(tint(x, 52, wd, 32, BLUE, w, r=8, size=11.5, op=0.14))
        x += wd + 6
    body.append(arrow(x + 4, 68, x + 40, 68, LINE, 2))
    body.append(solid(x + 46, 46, 104, 44, VIOLET, "model", r=12, size=12.5))
    mx = x + 150
    body.append(arrow(mx + 4, 68, mx + 40, 68, LINE, 2))
    cands = [("are", 0.62), ("is", 0.21), ("were", 0.08), ("in", 0.03), ("was", 0.02), ("…", 0.04)]
    bx = mx + 92
    for k, (w, p) in enumerate(cands):
        y = 44 + k * 26
        body.append(text(bx - 8, y + 14, w, 11, 750, anchor="end", fill=INK))
        body.append('<rect x="%d" y="%d" width="%.1f" height="18" rx="4" fill="%s"/>'
                    % (bx, y + 1, max(3, p * 220), plasma(0.2 + p)))
        body.append(text(bx + max(3, p * 220) + 6, y + 14, "%d%%" % round(p * 100), 9.6, 650,
                         anchor="start", fill=MUTED))
    body.append(tint(22, 222, 716, 62, GREEN, op=0.08, r=12))
    body.append(text(40, 246, "Then: choose one (say “are”), add it to the text, and predict again.",
                     10.5, 750, anchor="start", fill=INK))
    body.append(text(40, 266, "“The keys to the cabinet are …” → next prediction → next → … "
                     "That loop writes every chatbot answer.", 10, 600, anchor="start", fill=MUTED))
    desc = ("The words The keys to the cabinet go into a model, which outputs a probability "
            "for each possible next token: are 62 percent, is 21 percent, were 8 percent, in "
            "3 percent, was 2 percent, and everything else 4 percent. A note explains the "
            "loop: choose one, such as are, add it to the text, and predict again, which "
            "is how every chatbot writes its answers. The model must look back past "
            "cabinet to keys to choose the plural are.")
    return figure("ai-next", 760, 300, "".join(body), "Next-token prediction", desc,
                  "To choose “are”, the model must remember that the subject was “keys”, "
                  "not “cabinet”.")


# ================================================ Level 9: an RNN, unrolled

@diagram("ai-rnn-unrolled")
def _rnn_unrolled():
    """A recurrent cell and its unrolled form, carrying a hidden state."""
    body = [text(380, 22, "A recurrent network, unrolled: the same cell at every step", 12, 650,
                 fill=MUTED)]
    # compact form
    body.append(solid(40, 116, 70, 56, VIOLET, "RNN", r=12, size=13))
    body.append(path("M110 130 C 150 96, 150 60, 75 60 C 2 60, 0 96, 40 130", stroke=tv(ORANGE), w=2.4))
    body.append(arrow(44, 122, 40, 128, tv(ORANGE), 2.4))
    body.append(text(75, 52, "h", 11, 800, fill=tv(ORANGE)))
    body.append(arrow(75, 214, 75, 176, LINE, 2))
    body.append(text(75, 230, "xₜ", 11, 800, fill=INK))
    body.append(text(170, 150, "=", 22, 800, fill=MUTED))
    words = ["the", "cat", "sat", "on", "the"]
    preds = ["cat", "sat", "on", "the", "mat"]
    x0, gap = 214, 108
    for t, (w, pr) in enumerate(zip(words, preds)):
        x = x0 + t * gap
        body.append(solid(x, 116, 70, 56, VIOLET, "RNN", r=12, size=12))
        body.append(arrow(x + 35, 214, x + 35, 176, LINE, 2))
        body.append(tint(x + 6, 216, 58, 26, BLUE, w, r=8, size=10.5, op=0.14))
        body.append(arrow(x + 35, 112, x + 35, 80, tv(GREEN), 2))
        body.append(tint(x + 6, 50, 58, 26, GREEN, pr, r=8, size=10.5, op=0.14))
        if t < len(words) - 1:
            body.append(arrow(x + 72, 144, x + gap - 2, 144, tv(ORANGE), 3))
            body.append(text(x + 70 + (gap - 70) / 2.0, 136, "h%s" % "₁₂₃₄"[t], 10, 800,
                             fill=tv(ORANGE)))
    body.append(text(x0 - 16, 262, "inputs, one token at a time", 9.4, 650, anchor="start", fill=MUTED))
    body.append(text(x0 - 16, 40, "predicted next tokens", 9.4, 650, anchor="start", fill=MUTED))
    body.append(text(x0 + 2 * gap + 35, 290, "orange: the hidden state, the network's memory, "
                     "passed forward with the same weights each step", 9.6, 700, fill=tv(ORANGE)))
    desc = ("On the left, a recurrent cell labelled RNN takes an input x and loops its "
            "hidden state h back into itself. It equals the unrolled version on the right: "
            "five copies of the same cell in a row, reading the inputs the, cat, sat, on, "
            "the, one at a time. An orange hidden state, h1 to h4, passes from each copy to "
            "the next, and each copy predicts the next token: cat, sat, on, the, mat. The "
            "same weights are used at every step.")
    return figure("ai-rnn", 760, 300, "".join(body), "A recurrent neural network, unrolled",
                  desc, "The hidden state is the network's memory of everything so far.")


# =================================================== Level 9: an LSTM cell

@diagram("ai-lstm-cell")
def _lstm_cell():
    """The cell state highway, with forget, input and output gates."""
    body = [text(380, 22, "Inside an LSTM cell: a memory line and three gates", 12, 650,
                 fill=MUTED)]
    body.append(tint(110, 46, 540, 220, VIOLET, op=0.06, r=18))
    # cell state highway
    body.append(path("M40 84 L720 84", stroke=tv(TEAL), w=6))
    body.append(text(30, 74, "cell state (long-term memory)", 10, 800, anchor="start", fill=tv(TEAL)))
    for x, sym, colour in ((250, "×", RED), (400, "+", GREEN)):
        body.append('<circle cx="%d" cy="84" r="17" fill="%s"/>' % (x, colour))
        body.append(text(x, 91, sym, 18, 800, fill=WHITE))
    # hidden path
    body.append(path("M40 236 L720 236", stroke=tv(ORANGE), w=3))
    body.append(text(30, 254, "hidden state hₜ₋₁ and input xₜ", 9.6, 750, anchor="start", fill=tv(ORANGE)))
    gates = [(250, RED, "forget gate", "σ: what to erase"),
             (370, GREEN, "input gate", "σ: what to write"),
             (440, PURPLE, "candidate", "tanh: new info"),
             (560, BLUE, "output gate", "σ: what to reveal")]
    for x, colour, name, sub in gates:
        fill = colour if colour != PURPLE else VIOLET
        body.append(solid(x - 46, 150, 92, 46, fill, name, sub, r=10, size=10, sub_size=8.4))
        body.append(line(x, 236, x, 196, stroke=tv(ORANGE), w=2))
    body.append(arrow(250, 150, 250, 101, tv(RED), 2.2))
    body.append(path("M370 150 L370 120 L400 120 L400 101", stroke=tv(GREEN), w=2.2))
    body.append(path("M440 150 L440 120 L400 120", stroke=tv(VIOLET), w=2.2))
    body.append('<circle cx="400" cy="120" r="10" fill="%s"/>' % VIOLET)
    body.append(text(400, 124, "×", 11, 800, fill=WHITE))
    body.append(path("M560 84 L560 128", stroke=tv(TEAL), w=2.2))
    body.append(solid(536, 104, 48, 22, TEAL, "tanh", r=8, size=9.4))
    body.append('<circle cx="608" cy="173" r="11" fill="%s"/>' % BLUE)
    body.append(text(608, 177, "×", 11, 800, fill=WHITE))
    body.append(path("M584 115 L608 115 L608 162", stroke=tv(TEAL), w=2))
    body.append(path("M606 173 L606 173", stroke=tv(BLUE), w=2))
    body.append(arrow(619, 173, 700, 173, tv(ORANGE), 2.6))
    body.append(text(706, 177, "hₜ", 11, 800, anchor="start", fill=tv(ORANGE)))
    body.append(text(380, 288, "the memory line is changed only by × (forget) and + (add): "
                     "gradients travel along it far better than through a plain RNN", 9.6, 700,
                     fill=INK))
    desc = ("A schematic LSTM cell. A thick teal line, the cell state or long-term memory, "
            "runs across the top. It passes a red multiply node, controlled by the forget "
            "gate, a sigmoid deciding what to erase, then a green add node, where new "
            "information enters: the input gate, a sigmoid deciding what to write, "
            "multiplied by a candidate from a tanh layer. At the right, the cell state "
            "goes through tanh and is multiplied by the output gate, a sigmoid deciding "
            "what to reveal, to give the new hidden state h. Along the bottom runs the "
            "previous hidden state and the input, feeding all the gates.")
    return figure("ai-lstm", 760, 300, "".join(body), "An LSTM cell", desc,
                  "Each gate outputs numbers between 0 (block) and 1 (let through).")


# ============================================ Level 9: the seq2seq bottleneck

@diagram("ai-seq2seq")
def _seq2seq():
    """Encoder, one vector, decoder; and attention looking back at everything."""
    body = [text(380, 22, "Sequence to sequence: everything squeezed through one vector", 12,
                 650, fill=MUTED)]
    src = ["the", "black", "cat", "sleeps"]
    tgt = ["le", "chat", "noir", "dort"]
    for k, w in enumerate(src):
        x = 30 + k * 76
        body.append(solid(x, 140, 60, 40, BLUE, "enc", r=10, size=10.5))
        body.append(tint(x + 2, 200, 56, 26, BLUE, w, r=8, size=10.5, op=0.14))
        body.append(arrow(x + 30, 198, x + 30, 182, LINE, 1.6))
        if k < 3:
            body.append(arrow(x + 62, 160, x + 74, 160, tv(BLUE), 2))
    body.append(arrow(330, 160, 354, 160, tv(RED), 2.6))
    body.append('<circle cx="378" cy="160" r="22" fill="%s"/>' % RED)
    body.append(text(378, 165, "1 vec", 9.6, 800, fill=WHITE))
    body.append(text(378, 206, "the bottleneck", 10, 800, fill=tv(RED)))
    body.append(arrow(402, 160, 426, 160, tv(RED), 2.6))
    for k, w in enumerate(tgt):
        x = 432 + k * 76
        body.append(solid(x, 140, 60, 40, PINK, "dec", r=10, size=10.5))
        body.append(tint(x + 2, 94, 56, 26, PINK, w, r=8, size=10.5, op=0.14))
        body.append(arrow(x + 30, 138, x + 30, 122, LINE, 1.6))
        if k < 3:
            body.append(arrow(x + 62, 160, x + 74, 160, tv(PINK), 2))
    # attention lines from one decoder step back to every encoder state
    dx = 432 + 2 * 76 + 30
    for k in range(4):
        ex = 30 + k * 76 + 30
        wgt = [0.1, 0.55, 0.25, 0.1][k]
        body.append('<path d="M%d 182 C %d 262, %d 262, %d 182" fill="none" stroke="%s" '
                    'stroke-width="%.1f" stroke-opacity="0.85" stroke-dasharray="5 4"/>'
                    % (dx, dx - 40, ex + 40, ex, AMBER, 1 + wgt * 7))
    body.append(text(380, 286, "attention (2014): while writing “noir”, look back at every "
                     "encoder state, most strongly at “black”", 9.8, 750, fill=INK))
    body.append(text(180, 70, "encoder reads the source", 10, 800, fill=tv(BLUE)))
    body.append(text(588, 70, "decoder writes the translation", 10, 800, fill=tv(PINK)))
    desc = ("An encoder of four blue cells reads the, black, cat, sleeps, and passes its "
            "state along to a single red circle, one vector, labelled the bottleneck. A "
            "decoder of four pink cells starts from that vector and writes le, chat, noir, "
            "dort. Dashed amber curves of different thicknesses show attention: while "
            "writing noir, the decoder looks back at every encoder state, most strongly at "
            "black.")
    return figure("ai-s2s", 760, 300, "".join(body), "The sequence-to-sequence bottleneck",
                  desc, "Attention removed the bottleneck, and then replaced the RNNs entirely.")
