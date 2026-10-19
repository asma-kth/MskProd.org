"""AI course diagrams, Level 12: generative AI.

The noisy pictures use the 2020 diffusion schedule, the GAN curves use the
optimal discriminator D*(x) = p_data / (p_data + p_g), and the generated
point clouds come from the exact denoiser for their small datasets, the same
sampler as the lesson's Python. The latent-space grid and the network
diagrams are illustrations.
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
from .diagrams_ai5 import _softmax, _wsub, _mix, _CAT12, _CAT_PAL
from .diagrams_ai6 import _bubble


def _hex(c):
    return tuple(int(c[i:i + 2], 16) for i in (1, 3, 5))


def _art(x, y, s, rows, pal, alpha=None):
    """Pixel art: each character of each row is a pixel coloured from the palette."""
    out = []
    for i, row in enumerate(rows):
        for j, ch in enumerate(row):
            col = pal.get(ch)
            if col is None:
                continue
            out.append('<rect x="%.1f" y="%.1f" width="%.2f" height="%.2f" fill="%s"/>'
                       % (x + j * s, y + i * s, s + 0.15, s + 0.15, col))
    return "".join(out)


def _grid_rgb(x, y, s, cells):
    """A grid of (r, g, b) tuples."""
    out = []
    for i, row in enumerate(cells):
        for j, c in enumerate(row):
            out.append('<rect x="%.1f" y="%.1f" width="%.2f" height="%.2f" fill="#%02X%02X%02X"/>'
                       % (x + j * s, y + i * s, s + 0.15, s + 0.15, c[0], c[1], c[2]))
    return "".join(out)


_DIGIT = ["............",
          "...######...",
          "..##....##..",
          "..#......##.",
          ".........##.",
          "........##..",
          "......##....",
          "....##......",
          "...##.......",
          "..##........",
          "..#########.",
          "............"]

_SCENE = ["BBBBBBBBBBBB",
          "BBBBBBBYYBBB",
          "BBBBBBYYYYBB",
          "BBBBBBYYYYBB",
          "BBBBBBBYYBBB",
          "BBBBBBBBBBBB",
          "BBGGBBBBBBBB",
          "BGGGGBBBBGGB",
          "GGGGGGBBGGGG",
          "GGGDGGGGGGGG",
          "GGGGGGDGGGGG",
          "GGGGGGGGGGGG"]
_SCENE_PAL = {"B": "#38BDF8", "Y": "#FACC15", "G": "#22C55E", "D": "#15803D"}

_FOX = ["SSSSSSSSSSSS",
        "SOSSSSSSSSOS",
        "SOOSSSSSSOOS",
        "SOOOOOOOOOOS",
        "SOODOOOODOOS",
        "SOOOOOOOOOOS",
        "SSWWOOOOWWSS",
        "SSSWWWWWWSSS",
        "SSSSWWKWSSSS",
        "SSSSSWWSSSSS",
        "SSSSSSSSSSSS",
        "SSSSSSSSSSSS"]
_FOX_PAL = {"S": "#E0F2FE", "O": "#EA580C", "D": "#1F2937", "W": "#FFFFFF", "K": "#111827"}


def _noisy(rows, pal, abar, seed):
    """The picture mixed with Gaussian noise as the forward process would."""
    rnd = random.Random(seed)
    a, s = math.sqrt(abar), math.sqrt(1 - abar)
    out = []
    for row in rows:
        line_ = []
        for ch in row:
            c = _hex(pal[ch])
            px = []
            for v in c:
                u = a * (2 * v / 255.0 - 1) + s * rnd.gauss(0, 1)
                px.append(int(round((max(-1.0, min(1.0, u)) + 1) / 2 * 255)))
            line_.append(tuple(px))
        out.append(line_)
    return out


def _ddpm_abar(t):
    keep = 1.0
    for k in range(t):
        keep *= 1 - (0.0001 + (0.02 - 0.0001) * k / 999.0)
    return keep


# ===================================================== autoencoder

@diagram("ai-autoencoder")
def _autoencoder():
    """Encoder narrowing to a code, decoder widening back."""
    body = [text(380, 22, "An autoencoder: squeeze through a bottleneck, then rebuild", 12, 650,
                 fill=MUTED)]
    pal = {"#": "#FFFFFF", ".": "#1E1B4B"}
    body.append(_art(28, 86, 9, _DIGIT, pal))
    body.append(text(82, 206, "input", 10.5, 800, fill=INK))
    body.append(text(82, 220, "784 numbers", 9.4, 650, fill=MUTED))
    # encoder slabs
    for k, (h, col) in enumerate([(120, BLUE), (82, INDIGO), (50, VIOLET)]):
        x = 158 + k * 58
        body.append(cube(x, 140 - h / 2.0, 30, h, 14, col))
    body.append(text(214, 222, "encoder", 10.5, 800, fill=tv(BLUE)))
    body.append(text(214, 236, "784 → 128 → 32", 9.4, 650, fill=MUTED))
    rnd = random.Random(4)
    for k in range(8):
        body.append('<rect x="%d" y="%d" width="16" height="12" rx="2" fill="%s"/>'
                    % (372, 92 + k * 13, plasma(rnd.random())))
    body.append(text(380, 82, "code", 10.5, 800, fill=INK))
    body.append(text(380, 210, "latent code", 10, 800, fill=tv(PINK)))
    body.append(text(380, 224, "32 numbers", 9.4, 650, fill=MUTED))
    body.append(arrow(140, 140, 154, 140, LINE, 1.6))
    body.append(arrow(330, 140, 366, 140, LINE, 1.6))
    body.append(arrow(394, 140, 428, 140, LINE, 1.6))
    for k, (h, col) in enumerate([(50, VIOLET), (82, INDIGO), (120, BLUE)]):
        x = 434 + k * 58
        body.append(cube(x, 140 - h / 2.0, 30, h, 14, col))
    body.append(text(546, 222, "decoder", 10.5, 800, fill=tv(BLUE)))
    body.append(text(546, 236, "32 → 128 → 784", 9.4, 650, fill=MUTED))
    body.append(arrow(608, 140, 624, 140, LINE, 1.6))
    # rebuilt digit: a slightly blurred copy
    n = len(_DIGIT)
    vals = [[1.0 if _DIGIT[i][j] == "#" else 0.0 for j in range(n)] for i in range(n)]
    cells = []
    for i in range(n):
        row = []
        for j in range(n):
            acc, wsum = 0.0, 0.0
            for di in (-1, 0, 1):
                for dj in (-1, 0, 1):
                    ii, jj = i + di, j + dj
                    if 0 <= ii < n and 0 <= jj < n:
                        wgt = 4.0 if (di, dj) == (0, 0) else 1.0
                        acc += wgt * vals[ii][jj]
                        wsum += wgt
            v = acc / wsum
            base, top = _hex("#1E1B4B"), _hex("#FFFFFF")
            row.append(tuple(int(base[c] + (top[c] - base[c]) * min(1.0, v * 1.5)) for c in range(3)))
        cells.append(row)
    body.append(_grid_rgb(628, 86, 9, cells))
    body.append(text(682, 206, "rebuilt", 10.5, 800, fill=INK))
    body.append(text(682, 220, "784 numbers", 9.4, 650, fill=MUTED))
    body.append(path("M82 248 V 262 H 682 V 248", stroke=tv(RED), w=1.8))
    body.append(text(382, 280, "loss: the reconstruction error, how different the rebuilt image is from "
                     "the input", 10.5, 800, fill=tv(RED)))
    desc = ("A pixel image of the digit 2, 784 numbers, passes through an encoder drawn as three "
            "shrinking 3D blocks, 784 to 128 to 32 numbers, into a latent code of 32 numbers shown "
            "as a short coloured column. A decoder of three growing blocks, 32 to 128 to 784, "
            "rebuilds a slightly blurred copy of the digit. A red bracket joins the input and the "
            "rebuilt image: the loss is the reconstruction error between them.")
    return figure("ai-ae", 760, 292, "".join(body), "An autoencoder", desc,
                  "With only 32 numbers in the middle, the network must keep what matters and drop "
                  "the rest.")


# ===================================================== latent space

def _superellipse(cx, cy, rx, ry, n, colour, pts=48):
    p = []
    for k in range(pts):
        t = 2 * math.pi * k / pts
        c, s = math.cos(t), math.sin(t)
        x = cx + rx * math.copysign(abs(c) ** (2.0 / n), c)
        y = cy + ry * math.copysign(abs(s) ** (2.0 / n), s)
        p.append("%.1f,%.1f" % (x, y))
    return '<polygon points="%s" fill="%s" stroke="%s" stroke-width="1"/>' % (" ".join(p), colour, FILL)


@diagram("ai-latent-space")
def _latent_space():
    """A grid of shapes decoded from a two-number latent space."""
    body = [text(380, 22, "A latent space: every point decodes to something, and neighbours look "
                 "alike", 12, 650, fill=MUTED)]
    N, C = 7, 40
    X0, Y0 = 76, 50
    for i in range(N):
        for j in range(N):
            u, v = j / (N - 1.0), i / (N - 1.0)
            n = 1.0 + 5.0 * u
            asp = 0.6 + 0.8 * v
            col = plasma(0.15 + 0.75 * (0.6 * u + 0.4 * (1 - v)))
            body.append(_superellipse(X0 + j * C + C / 2.0, Y0 + i * C + C / 2.0, 15 * asp ** 0.5,
                                      15 / asp ** 0.5, n, col))
    body.append('<rect x="%d" y="%d" width="%d" height="%d" rx="8" fill="none" stroke="%s" '
                'stroke-width="1.4"/>' % (X0 - 4, Y0 - 4, N * C + 8, N * C + 8, LINE))
    body.append(text(X0 + N * C / 2.0, Y0 + N * C + 22, "latent number 1 →", 10, 750, fill=MUTED))
    cx, cy = X0 - 22, Y0 + N * C / 2.0
    body.append('<text x="%d" y="%.1f" text-anchor="middle" font-size="10" font-weight="750" fill="%s" '
                'transform="rotate(-90 %d %.1f)">latent number 2 →</text>' % (cx, cy, MUTED, cx, cy))
    # a straight walk between two codes
    a = (X0 + 0.5 * C, Y0 + 5.5 * C)
    b = (X0 + 6.5 * C, Y0 + 1.5 * C)
    body.append(line(a[0], a[1], b[0], b[1], stroke=AMBER, w=3, dash="7 5"))
    body.append(circle(a[0], a[1], 7, fill=AMBER, stroke=FILL, w=2))
    body.append(circle(b[0], b[1], 7, fill=AMBER, stroke=FILL, w=2))
    LX = 400
    body.append(text(LX, 74, "Each cell shows what the decoder makes", 10.5, 750, fill=INK, anchor="start"))
    body.append(text(LX, 90, "from that point of a two-number latent space.", 10.5, 750, fill=INK, anchor="start"))
    body.append(text(LX, 120, "Moving right makes shapes squarer;", 10.5, 650, fill=MUTED, anchor="start"))
    body.append(text(LX, 136, "moving down makes them wider.", 10.5, 650, fill=MUTED, anchor="start"))
    body.append(text(LX, 166, "The amber walk between two codes morphs", 10.5, 750, fill=tv(ORANGE), anchor="start"))
    body.append(text(LX, 182, "a narrow diamond into a wide square,", 10.5, 750, fill=tv(ORANGE), anchor="start"))
    body.append(text(LX, 198, "through every shape in between.", 10.5, 750, fill=tv(ORANGE), anchor="start"))
    body.append(text(LX, 228, "In a model of faces, directions like these", 10.5, 650, fill=MUTED, anchor="start"))
    body.append(text(LX, 244, "might add a smile, or turn the head.", 10.5, 650, fill=MUTED, anchor="start"))
    desc = ("An illustration of a decoder's two-number latent space as a 7 by 7 grid. Each cell shows "
            "the shape decoded from that point: from left to right the shapes change from diamonds "
            "through circles to rounded squares, and from top to bottom from tall and narrow to wide, "
            "with colours shifting gradually. A dashed amber line from one code to another crosses "
            "the grid: decoding the points along it morphs a narrow diamond into a wide square "
            "through every shape in between.")
    return figure("ai-lat", 760, 352, "".join(body), "A latent space", desc,
                  "An illustration: real latent spaces have dozens or hundreds of dimensions, but "
                  "the idea is the same.")


# ===================================================== VAE

@diagram("ai-vae")
def _vae():
    """Mean and spread, a sampled code, and a smooth latent space."""
    body = [text(380, 22, "A variational autoencoder encodes a cloud, not a point", 12, 650,
                 fill=MUTED)]
    body.append(_art(28, 58, 6, _DIGIT, {"#": "#FFFFFF", ".": "#1E1B4B"}))
    body.append(arrow(104, 94, 124, 94, LINE, 1.6))
    body.append(cube(128, 70, 70, 48, 12, BLUE))
    body.append(text(163, 98, "encoder", 10, 800, fill=WHITE))
    body.append(arrow(212, 84, 246, 70, LINE, 1.4))
    body.append(arrow(212, 104, 246, 118, LINE, 1.4))
    body.append(solid(250, 56, 92, 26, VIOLET, "mean", r=7, size=10.5))
    body.append(solid(250, 106, 92, 26, PINK, "spread", r=7, size=10.5))
    # the bell and the sample
    bx, by = 420, 112
    pts = " ".join("%.1f,%.1f" % (bx + u * 40, by - 44 * math.exp(-u * u / 0.5)) for u in [k / 10.0 - 1.6 for k in range(33)])
    body.append('<polyline points="%s" fill="%s" fill-opacity="0.25" stroke="%s" stroke-width="2"/>'
                % (pts, VIOLET, tv(VIOLET)))
    body.append(line(bx, by, bx, by - 46, stroke=tv(VIOLET), w=1.4, dash="3 3"))
    body.append(circle(bx + 18, by - 26, 6, fill=AMBER, stroke=FILL, w=1.5))
    body.append(arrow(346, 69, 386, 92, LINE, 1.3))
    body.append(arrow(346, 119, 386, 104, LINE, 1.3))
    body.append(text(bx + 22, by + 26, "sample z = mean + spread × random", 9.6, 750, fill=INK))
    body.append(arrow(478, 86, 512, 86, LINE, 1.6))
    body.append(cube(516, 62, 70, 48, 12, BLUE))
    body.append(text(551, 90, "decoder", 10, 800, fill=WHITE))
    body.append(arrow(600, 86, 620, 86, LINE, 1.6))
    body.append(_art(626, 50, 6, _DIGIT, {"#": "#E0E7FF", ".": "#1E1B4B"}))
    # two latent maps
    rnd = random.Random(7)
    for k, (title, col) in enumerate([("plain autoencoder: codes scattered, with gaps", SLATE),
                                      ("VAE: clouds pulled into one smooth bell", VIOLET)]):
        x0 = 40 + k * 370
        body.append(tint(x0, 168, 330, 132, col, op=0.06, r=12))
        body.append(text(x0 + 165, 188, title, 10.5, 800, fill=tv(col) if k else INK))
        cx, cy = x0 + 165, 246
        if k == 0:
            centres = [(-90, -20), (-40, 30), (60, -30), (110, 25), (10, 0)]
            for (dx, dy), c in zip(centres, [BLUE, PINK, ORANGE, TEAL, VIOLET]):
                for _ in range(9):
                    body.append(circle(cx + dx + rnd.gauss(0, 5), cy + dy + rnd.gauss(0, 4), 2.6,
                                       fill=c, stroke="none", w=0))
            body.append(circle(cx - 30, cy - 24, 6, fill="none", stroke=tv(RED), w=1.6))
            body.append(text(cx - 30, cy - 36, "a gap: decodes to nonsense", 9, 700, fill=tv(RED)))
        else:
            body.append('<ellipse cx="%d" cy="%d" rx="96" ry="40" fill="%s" fill-opacity="0.12" '
                        'stroke="%s" stroke-dasharray="4 3"/>' % (cx, cy, VIOLET, tv(VIOLET)))
            for (dx, dy), c in zip([(-50, -12), (-14, 12), (24, -10), (56, 10), (0, -2)],
                                   [BLUE, PINK, ORANGE, TEAL, VIOLET]):
                body.append('<ellipse cx="%d" cy="%d" rx="30" ry="16" fill="%s" fill-opacity="0.35"/>'
                            % (cx + dx, cy + dy, c))
            body.append(circle(cx + 6, cy + 2, 5, fill=AMBER, stroke=FILL, w=1.5))
            body.append(text(cx, cy + 48, "any random point decodes to something sensible", 9, 700,
                             fill=tv(VIOLET)))
    desc = ("Top: a digit enters an encoder, which outputs a mean and a spread instead of one code. "
            "A code z is sampled from the bell curve they describe, z equals the mean plus the "
            "spread times a random number, and the decoder rebuilds the digit from it. Bottom left: "
            "a plain autoencoder's codes form separate clumps with gaps, and a point in a gap "
            "decodes to nonsense. Bottom right: a VAE's clouds overlap inside one smooth bell, so "
            "any random point decodes to something sensible.")
    return figure("ai-vae", 760, 312, "".join(body), "A variational autoencoder", desc,
                  "The extra loss term packs the clouds together, which is what makes sampling work.")


# ===================================================== GAN

@diagram("ai-gan")
def _gan():
    """A generator and a discriminator in a contest."""
    body = [text(380, 22, "A GAN: a forger and a detective, trained against each other", 12, 650,
                 fill=MUTED)]
    rnd = random.Random(2)
    for i in range(8):
        for j in range(4):
            body.append('<rect x="%d" y="%d" width="9" height="9" fill="%s"/>'
                        % (30 + j * 10, 120 + i * 10, plasma(rnd.random())))
    body.append(text(50, 112, "noise", 10, 800, fill=INK))
    body.append(arrow(74, 160, 100, 160, LINE, 1.6))
    body.append(cube(104, 132, 100, 56, 16, VIOLET))
    body.append(text(154, 156, "generator", 11, 800, fill=WHITE))
    body.append(text(154, 172, "the forger", 9.6, 650, fill=WHITE))
    body.append(arrow(220, 160, 248, 160, LINE, 1.6))
    fake = [r.replace("G", "X") if k in (5, 6) else r for k, r in enumerate(_CAT12)]
    body.append(_art(252, 130, 5, fake, _CAT_PAL))
    body.append(text(282, 204, "a fake", 10, 800, fill=tv(VIOLET)))
    body.append(_art(252, 52, 5, _CAT12, _CAT_PAL))
    body.append(text(282, 46, "a real photo", 10, 800, fill=tv(TEAL)))
    body.append(arrow(316, 82, 386, 140, LINE, 1.5))
    body.append(arrow(316, 160, 386, 160, LINE, 1.5))
    body.append(cube(390, 132, 108, 56, 16, ORANGE))
    body.append(text(444, 156, "discriminator", 11, 800, fill=WHITE))
    body.append(text(444, 172, "the detective", 9.6, 650, fill=WHITE))
    body.append(arrow(514, 160, 540, 160, LINE, 1.6))
    body.append(text(600, 142, "“real” or “fake”?", 10.5, 800, fill=INK))
    body.append('<rect x="550" y="152" width="110" height="14" rx="7" fill="%s"/>' % FILL2)
    body.append('<rect x="550" y="152" width="%d" height="14" rx="7" fill="%s"/>' % (int(110 * 0.3), AMBER))
    body.append(text(600, 184, "P(real) = 0.30", 10, 750, fill=MUTED))
    body.append(path("M600 196 C 600 270, 160 270, 154 196", stroke=tv(PINK), w=2.4))
    body.append(arrow(155, 206, 154, 192, tv(PINK), 2.4))
    body.append(text(380, 262, "the generator follows the gradient of the verdict to make its next fakes "
                     "look more real", 10.5, 800, fill=tv(PINK)))
    body.append(path("M612 134 C 640 96, 520 90, 470 124", stroke=tv(ORANGE), w=2))
    body.append(arrow(478, 118, 468, 126, tv(ORANGE), 2))
    body.append(text(598, 88, "the detective learns from", 9.6, 750, fill=tv(ORANGE)))
    body.append(text(598, 101, "its mistakes too", 9.6, 750, fill=tv(ORANGE)))
    desc = ("Random noise enters a violet generator, the forger, which outputs a fake picture of a "
            "cat. An orange discriminator, the detective, is shown real photos and fakes and outputs "
            "how likely each is to be real: for this fake, 0.30. A pink arrow carries the gradient "
            "of that verdict back to the generator, which changes so its next fakes look more real, "
            "while the discriminator also learns from its mistakes.")
    return figure("ai-gan", 760, 280, "".join(body), "A generative adversarial network", desc,
                  "The generator never sees a real photo: everything it learns comes through the "
                  "discriminator's verdicts.")


# ===================================================== GAN training, stepped

def _gauss(x, m, s):
    return math.exp(-0.5 * ((x - m) / s) ** 2) / (s * math.sqrt(2 * math.pi))


def _p_data(x):
    return 0.5 * _gauss(x, 3.0, 0.7) + 0.5 * _gauss(x, 6.0, 0.7)


@diagram("ai-gan-training")
def _gan_training():
    """The generator's distribution moving onto the data, with D* drawn over it."""
    pl = Plot(70, 50, 560, 200, (-1, 9), (0, 0.6))
    base = [text(380, 22, "Training a GAN: the fakes' distribution moves onto the real one", 12, 650,
                 fill=MUTED)]
    base.append(pl.axes(xticks=range(0, 10), yticks=(0, 0.2, 0.4, 0.6), fmt="%g", xlabel="value"))
    xs = [-1 + 10 * i / 200.0 for i in range(201)]
    area = "M%.1f %.1f " % pl.pt(-1, 0) + " ".join("L%.1f %.1f" % pl.pt(x, _p_data(x)) for x in xs) \
        + " L%.1f %.1f Z" % pl.pt(9, 0)
    base.append('<path d="%s" fill="%s" fill-opacity="0.22" stroke="%s" stroke-width="2.2"/>'
                % (area, TEAL, tv(TEAL)))
    base.append(text(650, 70, "real data", 10.5, 800, fill=tv(TEAL), anchor="start"))
    base.append(text(650, 90, "fakes", 10.5, 800, fill=tv(PINK), anchor="start"))
    base.append(text(650, 110, "discriminator", 10.5, 800, fill=tv(ORANGE), anchor="start"))
    base.append(text(650, 124, "D*(x), right axis", 9.4, 650, fill=MUTED, anchor="start"))
    for v in (0, 0.5, 1):
        y = pl.y + pl.h - v * pl.h
        base.append(text(pl.x + pl.w + 8, y + 3.5, "%g" % v, 9, 650, fill=tv(ORANGE), anchor="start"))
    stages_def = [
        (lambda x: _gauss(x, 0.5, 1.0), "Start: the fakes are nothing like the data, and D* is near 1 "
         "over the data and near 0 over the fakes"),
        (lambda x: _gauss(x, 2.6, 1.5), "Following D*'s gradient, the fakes move towards the data"),
        (lambda x: 0.5 * _gauss(x, 3.3, 0.9) + 0.5 * _gauss(x, 5.5, 0.9),
         "The fakes split to cover both bumps; D* flattens"),
        (_p_data, "Equilibrium: the fakes match the data and D* = 0.5 everywhere"),
    ]
    stages, labels = [], []
    for n, (pg, lab) in enumerate(stages_def):
        s = []
        d = "M" + " L".join("%.1f %.1f" % pl.pt(x, pg(x)) for x in xs)
        s.append('<path d="%s" fill="none" stroke="%s" stroke-width="2.6" stroke-dasharray="%s"/>'
                 % (d, tv(PINK), "" if n < 3 else "6 4"))
        dd = []
        for x in xs:
            a, b = _p_data(x), pg(x)
            v = a / (a + b) if a + b > 1e-9 else 0.5
            dd.append((pl.px(x), pl.y + pl.h - v * pl.h))
        s.append('<path d="M%s" fill="none" stroke="%s" stroke-width="2.4" stroke-dasharray="7 4"/>'
                 % (" L".join("%.1f %.1f" % p for p in dd), AMBER))
        stages.append(step(n + 1, "".join(s), lab))
        labels.append(lab)
    desc = ("A stepped graph over values from minus 1 to 9. The real data, in teal, has two bumps, "
            "at 3 and 6. The fakes, in pink, start as one bump at 0.5; the optimal discriminator "
            "D*(x) = p_data / (p_data + p_fake), drawn dashed in amber against a 0 to 1 scale, is near "
            "1 over the data and near 0 over the fakes. The fakes then move to a wide bump around "
            "2.6, then split into two bumps near 3.3 and 5.5 while D* flattens, and finally match "
            "the data exactly, where D* is 0.5 everywhere.")
    return figure_steps("ai-gant", 760, 290, "".join(base), stages, "Training a GAN", desc,
                        "The amber curve is the best possible discriminator for each stage: "
                        "p_data ÷ (p_data + p_fake).", labels=labels)


# ===================================================== mode collapse

@diagram("ai-mode-collapse")
def _mode_collapse():
    """Eight clusters; a healthy generator; a collapsed one."""
    body = [text(380, 22, "Mode collapse: fooling the detective with only a few kinds of output", 12,
                 650, fill=MUTED)]
    rnd = random.Random(11)
    centres = [(math.cos(2 * math.pi * k / 8), math.sin(2 * math.pi * k / 8)) for k in range(8)]
    panels = [("real data: 8 clusters", TEAL, list(range(8)), 30),
              ("healthy generator: all 8", PINK, list(range(8)), 30),
              ("mode collapse: only 2", RED, [1, 2], 120)]
    for p, (title, col, which, n) in enumerate(panels):
        cx, cy = 130 + p * 250, 160
        body.append(tint(cx - 112, 44, 224, 212, col, op=0.06, r=12))
        body.append(text(cx, 66, title, 10.5, 800, fill=tv(col)))
        for k in range(8):
            body.append(circle(cx + 72 * centres[k][0], cy + 72 * centres[k][1], 16, fill="none",
                               stroke=LINE, w=1))
        for k in which:
            for _ in range(n if p else 30):
                body.append(circle(cx + 72 * centres[k][0] + rnd.gauss(0, 6),
                                   cy + 72 * centres[k][1] + rnd.gauss(0, 6), 2.2, fill=col,
                                   stroke="none", w=0))
    body.append(text(380, 276, "Each fake on its own looks real, but the variety of the data is lost.",
                     10.5, 750, fill=INK))
    desc = ("Three panels, each with eight faint rings arranged in a circle. Real data, in teal, has "
            "points in all eight clusters. A healthy generator, in pink, also fills all eight. A "
            "collapsed generator, in red, piles all its points into just two of the clusters: each "
            "fake looks real, but the variety of the data is lost.")
    return figure("ai-modec", 760, 290, "".join(body), "Mode collapse", desc,
                  "A classic test: real data in a ring of clusters makes collapse easy to see.")


# ===================================================== diffusion forward

@diagram("ai-diffusion-forward")
def _diffusion_forward():
    """One picture at six points of the forward process."""
    body = [text(380, 22, "The forward process: a little more noise at every step", 12, 650,
                 fill=MUTED)]
    steps_ = [0, 50, 100, 250, 500, 1000]
    for k, t in enumerate(steps_):
        ab = _ddpm_abar(t)
        x0 = 30 + k * 122
        cells = _noisy(_SCENE, _SCENE_PAL, ab, seed=5)
        body.append(_grid_rgb(x0, 50, 8.5, cells))
        body.append('<rect x="%d" y="50" width="102" height="102" fill="none" stroke="%s"/>' % (x0, LINE))
        body.append(text(x0 + 51, 170, "step %d" % t if t else "original", 10.5, 800, fill=INK))
        body.append(text(x0 + 51, 186, "%.2f image" % math.sqrt(ab), 9.4, 700, fill=tv(BLUE)))
        body.append(text(x0 + 51, 200, "%.2f noise" % math.sqrt(1 - ab), 9.4, 700, fill=tv(PINK)))
        if k < 5:
            body.append(arrow(x0 + 104, 101, x0 + 120, 101, LINE, 1.5))
    body.append(text(380, 228, "No learning here: noise is simply mixed in. The network learns the "
                     "reverse.", 10.5, 750, fill=INK))
    desc = ("Six copies of a small picture of a yellow sun over green hills and blue sky, each with "
            "more noise. The original; step 50, 0.99 image and 0.17 noise; step 100, 0.95 and 0.32; "
            "step 250, 0.72 and 0.69, where the picture is still faintly visible; step 500, 0.28 "
            "and 0.96, mostly noise; and step 1000, pure noise. Adding noise needs no learning; the "
            "network learns the reverse.")
    return figure("ai-dfwd", 760, 240, "".join(body), "The forward process", desc,
                  "Amounts from the 1,000-step schedule of the 2020 diffusion paper.")


# ===================================================== denoiser training

@diagram("ai-denoiser-training")
def _denoiser_training():
    """Image plus noise, a U-Net, and the loss on the noise."""
    body = [text(380, 22, "Training the denoiser: guess the noise that was added", 12, 650,
                 fill=MUTED)]
    S = 6.5
    body.append(_art(24, 50, S, _SCENE, _SCENE_PAL))
    body.append(text(63, 142, "image", 10, 800, fill=INK))
    rnd = random.Random(3)
    eps = [[tuple(int(128 + 60 * rnd.gauss(0, 1)) for _ in range(3)) for _ in range(12)] for _ in range(12)]
    eps = [[tuple(max(0, min(255, v)) for v in c) for c in row] for row in eps]
    body.append(_grid_rgb(24, 168, S, eps))
    body.append(text(63, 260, "random noise", 10, 800, fill=INK))
    body.append(text(124, 132, "+", 22, 800, fill=INK))
    body.append(arrow(110, 96, 150, 120, LINE, 1.4))
    body.append(arrow(110, 206, 150, 150, LINE, 1.4))
    body.append(_grid_rgb(156, 96, S, _noisy(_SCENE, _SCENE_PAL, _ddpm_abar(250), seed=3)))
    body.append(text(195, 188, "noisy image", 10, 800, fill=INK))
    body.append(text(195, 202, "at a random step t", 9.4, 650, fill=MUTED))
    body.append(arrow(240, 135, 272, 135, LINE, 1.6))
    # the U-Net
    blocks = [(280, 70, 26, 110, BLUE), (318, 96, 22, 70, INDIGO), (352, 116, 20, 34, VIOLET),
              (384, 96, 22, 70, INDIGO), (418, 70, 26, 110, BLUE)]
    for x, y, w, h, col in blocks:
        body.append('<rect x="%d" y="%d" width="%d" height="%d" rx="5" fill="%s"/>' % (x, y, w, h, col))
    for (x1, y1), (x2, y2) in [((306, 76), (418, 76)), ((340, 100), (384, 100))]:
        body.append(path("M%d %d C %d %d, %d %d, %d %d" % (x1, y1, x1 + 20, y1 - 22, x2 - 20, y2 - 22, x2, y2),
                         stroke=AMBER, w=2))
    body.append(text(362, 206, "U-Net", 11, 800, fill=tv(BLUE)))
    body.append(text(362, 220, "skip connections carry detail", 9.4, 650, fill=MUTED))
    body.append(arrow(448, 135, 480, 135, LINE, 1.6))
    pred = [[tuple(max(0, min(255, int(v + rnd.gauss(0, 14)))) for v in c) for c in row] for row in eps]
    body.append(_grid_rgb(486, 96, S, pred))
    body.append(text(525, 188, "predicted noise", 10, 800, fill=INK))
    body.append(path("M63 270 V 284 H 700 V 172", stroke=tv(PINK), w=1.8, dash="5 4"))
    body.append(arrow(700, 180, 700, 168, tv(PINK), 1.8))
    body.append(solid(630, 118, 140 - 10, 44, PINK, "loss", r=10, size=12))
    body.append(text(695, 112, "(real − predicted)²", 9.6, 750, fill=INK))
    body.append(arrow(570, 140, 626, 140, LINE, 1.6))
    body.append(text(380, 300, "the real noise is the answer the prediction is marked against", 9.6, 700,
                     fill=tv(PINK)))
    desc = ("A picture and a grid of random noise are mixed into a noisy picture at a random step. "
            "A U-Net, drawn as blocks that shrink and then grow again with amber skip connections "
            "between matching sizes, predicts the noise. The loss is the squared difference between "
            "the predicted noise and the real noise, which a dashed pink line carries round from the "
            "start.")
    return figure("ai-dtrain", 760, 312, "".join(body), "Training a denoiser", desc,
                  "Every training example asks the same small question: what noise was added here?")


# ===================================================== reverse: noise to a shape

def _heart(n):
    pts = []
    for k in range(n):
        t = 2 * math.pi * k / n
        x = 16 * math.sin(t) ** 3
        y = 13 * math.cos(t) - 5 * math.cos(2 * t) - 2 * math.cos(3 * t) - math.cos(4 * t)
        pts.append((x / 17.0, y / 17.0 + 0.1))
    return pts


def _sample_paths(data, n, T=40, seed=1):
    rnd = random.Random(seed)

    def ab(t):
        return math.cos((t / float(T) + 0.008) / 1.008 * math.pi / 2) ** 2

    paths = []
    for _ in range(n):
        x = (rnd.gauss(0, 1), rnd.gauss(0, 1))
        trail = [x]
        for t in range(T, 0, -1):
            a, s = math.sqrt(ab(t)), math.sqrt(1 - ab(t))
            sc = [-((x[0] - a * d[0]) ** 2 + (x[1] - a * d[1]) ** 2) / (2 * s * s) for d in data]
            w = _softmax(sc)
            x0 = (sum(wi * d[0] for wi, d in zip(w, data)), sum(wi * d[1] for wi, d in zip(w, data)))
            e = ((x[0] - a * x0[0]) / s, (x[1] - a * x0[1]) / s)
            a2, s2 = math.sqrt(ab(t - 1)), math.sqrt(1 - ab(t - 1))
            x = (a2 * x0[0] + s2 * e[0], a2 * x0[1] + s2 * e[1])
            trail.append(x)
        paths.append(trail)
    return paths


@diagram("ai-diffusion-reverse")
def _diffusion_reverse():
    """Points flowing from noise into a heart, in four snapshots."""
    data = _heart(80)
    paths = _sample_paths(data, 90, 40, seed=4)
    body = [text(380, 22, "The reverse process: every point starts as noise and flows into the shape",
                 12, 650, fill=MUTED)]
    snaps = [(0, "step 40: pure noise"), (24, "step 16"), (34, "step 6"), (40, "step 0: a heart")]
    for k, (idx, title) in enumerate(snaps):
        cx, cy, sc = 100 + k * 186, 150, 52
        body.append(tint(cx - 86, 44, 172, 196, VIOLET, op=0.05, r=12))
        body.append(text(cx, 64, title, 10.5, 800, fill=INK))
        body.append('<defs><clipPath id="ai-drev-c%d"><rect x="%d" y="72" width="168" height="164"/>'
                    '</clipPath></defs><g clip-path="url(#ai-drev-c%d)">' % (k, cx - 84, k))
        if k == 3:
            for tr in paths[::3]:
                d = "M" + " L".join("%.1f %.1f" % (cx + sc * p[0], cy - sc * p[1]) for p in tr)
                body.append('<path d="%s" fill="none" stroke="%s" stroke-width="0.8" stroke-opacity="0.35"/>'
                            % (d, tv(VIOLET)))
        for j, tr in enumerate(paths):
            p = tr[idx]
            x, y = cx + sc * p[0], cy - sc * p[1]
            body.append(circle(x, y, 2.4, fill=plasma(0.2 + 0.7 * j / len(paths)), stroke="none", w=0))
        body.append("</g>")
        if k < 3:
            body.append(arrow(cx + 88, 150, cx + 98, 150, LINE, 1.6))
    body.append(text(380, 262, "Each step, the denoiser guesses the clean point and the sampler moves a "
                     "little way towards it.", 10.5, 750, fill=INK))
    desc = ("Four snapshots of 90 points. At step 40 they are a shapeless cloud of random noise. At "
            "step 16 they have drawn together into a rough blob; at step 6 a heart shape is clearly "
            "forming; at step 0 the points lie on the outline of a heart, with faint lines tracing "
            "the path each point took from the noise. Each step, the denoiser guesses the clean point "
            "and the sampler moves a little way towards it.")
    return figure("ai-drev", 760, 274, "".join(body), "From noise to a shape", desc,
                  "Computed with the exact denoiser for 80 points on a heart, the same sampler as "
                  "the lesson's Python.")


# ===================================================== guidance

@diagram("ai-guidance")
def _guidance():
    """Guided noise = unconditional + w × (conditional − unconditional)."""
    body = [text(380, 22, "Classifier-free guidance: go further in the direction the prompt points",
                 12, 650, fill=MUTED)]
    O = (100, 232)
    U = (240, 196)
    Cp = (280, 156)
    w = 3.0
    G = (U[0] + w * (Cp[0] - U[0]), U[1] + w * (Cp[1] - U[1]))
    body.append(circle(O[0], O[1], 6, fill=INK, stroke=FILL, w=1.5))
    body.append(_halo(O[0] - 4, O[1] + 22, "current noisy image", 10, 750, "start"))
    body.append(arrow(O[0], O[1], U[0], U[1], SLATE, 2.6))
    body.append(_halo(U[0] + 10, U[1] + 16, "step with no prompt", 10, 750, "start"))
    body.append(arrow(O[0], O[1], Cp[0], Cp[1], tv(PINK), 2.6))
    body.append(_halo(Cp[0] + 12, Cp[1] + 4, "step with the prompt", 10, 750, "start"))
    body.append(line(U[0], U[1], G[0], G[1], stroke=AMBER, w=1.6, dash="5 4"))
    body.append(arrow(O[0], O[1], G[0], G[1], AMBER, 3.2))
    body.append(_halo(G[0] - 12, G[1] - 6, "guided step, w = 3", 10.5, 800, "end"))
    LX = 500
    lines_ = [("w = 1: plain prompt-following,", INK, 750), ("varied results", MUTED, 650),
              ("w ≈ 7: a common setting:", INK, 750), ("closely matches the prompt", MUTED, 650),
              ("w = 20: very literal, little", INK, 750), ("variety, harsh colours", MUTED, 650)]
    for k, (s, col, wgt) in enumerate(lines_):
        body.append(text(LX, 84 + k * 22 + (k // 2) * 12, s, 10.5, wgt, fill=col, anchor="start"))
    body.append(text(380, 262, "guided = no prompt + w × (with prompt − no prompt)", 11, 800,
                     fill=tv(ORANGE)))
    desc = ("From a dot marking the current noisy image, a grey arrow shows the denoising step "
            "predicted with no prompt and a pink arrow the step predicted with the prompt. The "
            "difference between them is the direction the prompt points. A thick amber arrow, the "
            "guided step with w = 3, goes three times as far along that difference. Notes: w = 1 "
            "follows the prompt plainly with varied results; w around 7 is common and matches the "
            "prompt closely; w = 20 is very literal with little variety. The formula: guided equals "
            "no prompt plus w times, with prompt minus no prompt.")
    return figure("ai-guide", 760, 276, "".join(body), "Classifier-free guidance", desc,
                  "Two predictions per step, combined: the price of guidance is twice the work.")


# ===================================================== latent diffusion

@diagram("ai-latent-diffusion")
def _latent_diffusion():
    """Text encoder, denoising loop in latent space, decoder."""
    body = [text(380, 22, "Latent diffusion: denoise a small latent, then decode it into pixels", 12,
                 650, fill=MUTED)]
    body.append(_bubble(24, 52, 170, 34, PINK, ["“a red fox in the snow”"]))
    body.append(arrow(110, 88, 110, 104, LINE, 1.5))
    body.append(cube(52, 108, 112, 40, 12, PINK))
    body.append(text(102, 133, "text encoder", 10.5, 800, fill=WHITE))
    for k in range(6):
        body.append('<rect x="%d" y="170" width="14" height="14" rx="2" fill="%s"/>'
                    % (60 + k * 16, plasma(0.2 + 0.12 * k)))
    body.append(text(108, 202, "word embeddings", 9.6, 700, fill=MUTED))
    rnd = random.Random(8)
    for i in range(6):
        for j in range(6):
            body.append('<rect x="%d" y="%d" width="11" height="11" fill="%s"/>'
                        % (236 + j * 12, 64 + i * 12, diverging(rnd.uniform(-1, 1))))
    body.append(text(272, 152, "random latent", 9.8, 800, fill=INK))
    body.append(text(272, 166, "64 × 64 × 4", 9.4, 650, fill=MUTED))
    body.append(arrow(312, 100, 352, 100, LINE, 1.6))
    body.append(cube(356, 70, 120, 60, 16, VIOLET))
    body.append(text(410, 96, "denoiser", 11, 800, fill=WHITE))
    body.append(text(410, 112, "U-Net or transformer", 9, 650, fill=WHITE))
    body.append(path("M482 92 C 520 60, 520 150, 482 118", stroke=tv(VIOLET), w=2.2))
    body.append(arrow(488, 116, 480, 120, tv(VIOLET), 2.2))
    body.append(text(538, 108, "× 30 steps", 10.5, 800, fill=tv(VIOLET), anchor="start"))
    body.append(path("M164 180 C 230 240, 330 200, 360 140", stroke=AMBER, w=2, dash="5 4"))
    body.append(arrow(357, 148, 362, 136, AMBER, 2))
    body.append(text(244, 240, "cross-attention reads the words", 9.6, 750, fill=tv(ORANGE)))
    body.append(arrow(416, 140, 416, 176, LINE, 1.6))
    for i in range(6):
        for j in range(6):
            v = math.sin(i * 0.9) * math.cos(j * 0.7)
            body.append('<rect x="%d" y="%d" width="11" height="11" fill="%s"/>'
                        % (380 + j * 12, 182 + i * 12, diverging(v * 0.8)))
    body.append(text(416, 268, "clean latent", 9.8, 800, fill=INK))
    body.append(arrow(458, 218, 498, 218, LINE, 1.6))
    body.append(cube(502, 196, 92, 44, 12, BLUE))
    body.append(text(544, 222, "decoder", 10.5, 800, fill=WHITE))
    body.append(arrow(606, 218, 626, 218, LINE, 1.6))
    body.append(_art(632, 168, 9, _FOX, _FOX_PAL))
    body.append(text(686, 290, "512 × 512 image", 9.8, 800, fill=INK))
    body.append(text(380, 298, "Denoising 16,384 latent numbers instead of 786,432 pixel values: 48 "
                     "times less work per step.", 10, 700, fill=MUTED))
    desc = ("A prompt, a red fox in the snow, goes through a pink text encoder into word embeddings. "
            "A random latent of 64 by 64 by 4 numbers goes into a violet denoiser, a U-Net or "
            "transformer, which runs about 30 times, reading the words through cross-attention, "
            "shown as a dashed amber line. The clean latent goes through a blue decoder, which "
            "outputs a 512 by 512 picture of a fox. Denoising 16,384 latent numbers instead of "
            "786,432 pixel values is 48 times less work per step.")
    return figure("ai-ldm", 760, 310, "".join(body), "Latent diffusion", desc,
                  "The autoencoder from Lesson 12.1 is what makes the small latent possible.")


# ===================================================== CLIP

_ICONS = {
    "dog": (["........", ".BB..BB.", ".BBBBBB.", ".BDBBDB.", ".BBBBBB.", "..BKKB..", "..BBBB..", "........"],
            {"B": "#A16207", "D": "#111827", "K": "#111827"}),
    "cat": ([".O....O.", ".OO..OO.", ".OOOOOO.", ".OGOOGO.", ".OOOOOO.", "..OPPO..", "...OO...", "........"],
            {"O": "#EA580C", "G": "#22C55E", "P": "#DB2777"}),
    "car": (["........", "...RRR..", "..RWWRR.", ".RRRRRRR", ".RRRRRRR", "..K...K.", "........", "........"],
            {"R": "#DC2626", "W": "#BAE6FD", "K": "#111827"}),
    "tree": (["...GG...", "..GGGG..", ".GGGGGG.", "GGGGGGGG", "..GGGG..", "...TT...", "...TT...", "........"],
             {"G": "#16A34A", "T": "#92400E"}),
}


@diagram("ai-clip")
def _clip():
    """Image and text encoders, and a similarity matrix with a bright diagonal."""
    body = [text(380, 22, "CLIP: matching pictures and captions in one shared space", 12, 650,
                 fill=MUTED)]
    names = ["dog", "cat", "car", "tree"]
    caps = ["a photo of a dog", "a photo of a cat", "a red car", "a tree in a field"]
    rnd = random.Random(6)
    base = [[(1.0 if j == i else 0.0) + rnd.uniform(-0.3, 0.3) for j in range(6)] for i in range(4)]
    img = [[v + rnd.gauss(0, 0.12) for v in b] for b in base]
    txt = [[v + rnd.gauss(0, 0.12) for v in b] for b in base]

    def cos(a, b):
        return sum(x * y for x, y in zip(a, b)) / math.sqrt(sum(x * x for x in a) * sum(y * y for y in b))
    sims = [[cos(img[i], txt[j]) for j in range(4)] for i in range(4)]
    MX, MY, C = 300, 120, 54
    body.append(cube(130, 44, 120, 34, 12, BLUE))
    body.append(text(184, 66, "text encoder", 10.5, 800, fill=WHITE))
    body.append(cube(26, 150, 34, 160, 12, PINK))
    body.append('<text x="43" y="230" text-anchor="middle" font-size="10.5" font-weight="800" fill="%s" '
                'transform="rotate(-90 43 230)">image encoder</text>' % WHITE)
    for j, cpt in enumerate(caps):
        x = MX + j * C + C / 2.0
        body.append('<text x="%.1f" y="%d" text-anchor="start" font-size="9.6" font-weight="700" fill="%s" '
                    'transform="rotate(-28 %.1f %d)">%s</text>' % (x - 10, MY - 8, INK, x - 10, MY - 8, esc(cpt)))
    for i, nm in enumerate(names):
        rows, pal = _ICONS[nm]
        body.append('<rect x="%d" y="%d" width="44" height="44" rx="6" fill="%s"/>' % (240, MY + i * C + 5, "#E0F2FE"))
        body.append(_art(244, MY + i * C + 9, 4.5, rows, pal))
        body.append(arrow(80, 230, 232, MY + i * C + 27, LINE, 1))
        for j in range(4):
            v = sims[i][j]
            col = plasma(max(0.0, min(1.0, (v + 0.4) / 1.4)))
            x, y = MX + j * C, MY + i * C
            body.append('<rect x="%d" y="%d" width="%d" height="%d" rx="5" fill="%s"%s/>'
                        % (x + 2, y + 2, C - 4, C - 4, col,
                           ' stroke="%s" stroke-width="3"' % AMBER if i == j else ""))
            body.append(text(x + C / 2.0, y + C / 2.0 + 4, ("%.2f" % v).replace("-", "−"), 10, 800,
                             fill=ink_on(col)))
    body.append(path("M262 61 H %d" % (MX + 2 * C), stroke=LINE, w=1.4))
    body.append(arrow(MX + 2 * C, 61, MX + 2 * C, 70, LINE, 1.4))
    LX = 540
    notes_ = [("Each cell: the cosine similarity", INK, 750), ("of one picture and one caption.", INK, 750),
              ("Training pulls the matching pairs,", tv(ORANGE), 800), ("on the diagonal, together,", tv(ORANGE), 800),
              ("and pushes every other pair", MUTED, 650), ("apart.", MUTED, 650),
              ("400 million pairs later, pictures", INK, 750), ("and words share one space.", INK, 750)]
    for k, (s, col, wgt) in enumerate(notes_):
        body.append(text(LX, 140 + k * 20 + (k // 2) * 10, s, 10.5, wgt, fill=col, anchor="start"))
    desc = ("Four small pictures, a dog, a cat, a red car and a tree, go through a pink image "
            "encoder, and four captions go through a blue text encoder. A 4 by 4 grid shows the "
            "cosine similarity of every picture with every caption. The diagonal cells, where picture "
            "and caption match, are outlined in amber and are the brightest, %s; the others are "
            "low. Training pulls matching pairs together and pushes the rest apart; after 400 "
            "million pairs, pictures and words share one space."
            % ", ".join("%.2f" % sims[i][i] for i in range(4)))
    return figure("ai-clip", 760, 344, "".join(body), "CLIP", desc,
                  "Illustrative numbers: real CLIP embeddings have 512 dimensions or more.")
