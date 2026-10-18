"""AI course diagrams, Levels 4 and 5: classic machine learning, loss and
gradient descent.

Where a figure shows what an algorithm does, the algorithm is run here, at
build time, on the figure's own data: the least squares line, the decision
boundaries, the k-means rounds and the descent paths are computed, not drawn
by eye, so the pictures always agree with the code in the lessons.
"""
import math

from .diagrams import diagram
from .svg import figure, figure_steps, step, text, line, path, circle
from .diagrams_ai_kit import (INK, MUTED, FILL, FILL2, LINE, VIOLET, PINK, BLUE,
                              TEAL, GREEN, ORANGE, RED, INDIGO, AMBER, LIME,
                              CYAN, ROSE, SKY, PURPLE, SLATE, WHITE, DARK, tv,
                              solid, tint, grad, plasma, diverging, ink_on, arrow,
                              project, surface)


# ----------------------------------------------------------------- helpers

class Plot:
    """A rectangle of the figure mapped to a range of data coordinates."""

    def __init__(self, x, y, w, h, xr, yr):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.xr, self.yr = xr, yr

    def px(self, v):
        return self.x + (v - self.xr[0]) / float(self.xr[1] - self.xr[0]) * self.w

    def py(self, v):
        return self.y + self.h - (v - self.yr[0]) / float(self.yr[1] - self.yr[0]) * self.h

    def pt(self, x, y):
        return self.px(x), self.py(y)

    def axes(self, xticks=(), yticks=(), xlabel="", ylabel="", grid=True, fmt="%g"):
        out = []
        for v in yticks:
            y = self.py(v)
            if grid:
                out.append(line(self.x, y, self.x + self.w, y, stroke=LINE, w=0.6, dash="2 4"))
            out.append(text(self.x - 6, y + 3.5, fmt % v, 9, 600, anchor="end", fill=MUTED))
        for v in xticks:
            x = self.px(v)
            out.append(line(x, self.y + self.h, x, self.y + self.h + 4, stroke=LINE, w=1))
            out.append(text(x, self.y + self.h + 15, fmt % v, 9, 600, fill=MUTED))
        out.append(line(self.x, self.y + self.h, self.x + self.w, self.y + self.h,
                        stroke=LINE, w=1.4))
        out.append(line(self.x, self.y, self.x, self.y + self.h, stroke=LINE, w=1.4))
        if xlabel:
            out.append(text(self.x + self.w / 2.0, self.y + self.h + 30, xlabel, 9.6, 650,
                            fill=MUTED))
        if ylabel:
            cx, cy = self.x - 34, self.y + self.h / 2.0
            out.append('<text x="%.1f" y="%.1f" text-anchor="middle" font-size="9.6" '
                       'font-weight="650" fill="%s" transform="rotate(-90 %.1f %.1f)">%s'
                       '</text>' % (cx, cy, MUTED, cx, cy, ylabel))
        return "".join(out)

    def curve(self, f, n=120, x0=None, x1=None):
        a = self.xr[0] if x0 is None else x0
        b = self.xr[1] if x1 is None else x1
        pts = []
        for i in range(n + 1):
            v = a + (b - a) * i / float(n)
            pts.append("%.1f %.1f" % self.pt(v, f(v)))
        return "M" + " L".join(pts)

    def clip(self, cid):
        return ('<defs><clipPath id="%s"><rect x="%.1f" y="%.1f" width="%.1f" height="%.1f"/>'
                '</clipPath></defs>' % (cid, self.x, self.y, self.w, self.h))


def _square(x, y, s, colour, stroke=FILL):
    return ('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="2" fill="%s" '
            'stroke="%s" stroke-width="1.3"/>' % (x - s / 2.0, y - s / 2.0, s, s, colour, stroke))


def _halo(x, y, s, size, weight, anchor="middle"):
    """Text with a halo in the page colour, readable on a busy coloured surface."""
    return ('<text x="%.1f" y="%.1f" text-anchor="%s" font-size="%s" font-weight="%s" '
            'fill="%s" stroke="%s" stroke-width="3.2" stroke-linejoin="round" '
            'paint-order="stroke">%s</text>' % (x, y, anchor, size, weight, INK, FILL, s))


def _solve(a, b):
    """Solve the linear system a x = b by Gaussian elimination with pivoting."""
    n = len(b)
    m = [list(row) + [b[i]] for i, row in enumerate(a)]
    for c in range(n):
        p = max(range(c, n), key=lambda r: abs(m[r][c]))
        m[c], m[p] = m[p], m[c]
        for r in range(n):
            if r != c and m[c][c]:
                f = m[r][c] / m[c][c]
                for k in range(c, n + 1):
                    m[r][k] -= f * m[c][k]
    return [m[i][n] / m[i][i] for i in range(n)]


def _polyfit(xs, ys, deg):
    """Least squares polynomial coefficients, lowest power first."""
    a = [[sum(x ** (i + j) for x in xs) for j in range(deg + 1)] for i in range(deg + 1)]
    b = [sum(y * x ** i for x, y in zip(xs, ys)) for i in range(deg + 1)]
    return _solve(a, b)


def _poly(c):
    return lambda x: sum(ci * x ** i for i, ci in enumerate(c))


def _lagrange(xs, ys):
    def f(x):
        total = 0.0
        for i, (xi, yi) in enumerate(zip(xs, ys)):
            term = yi
            for j, xj in enumerate(xs):
                if j != i:
                    term *= (x - xj) / (xi - xj)
            total += term
        return total
    return f


# ======================================== Level 4: the least squares line

HOURS = [1, 2, 2, 3, 4, 5, 6, 6, 7, 8]
SCORE = [38, 45, 50, 52, 61, 64, 70, 75, 78, 86]


def _least_squares(xs, ys):
    n = len(xs)
    mx, my = sum(xs) / float(n), sum(ys) / float(n)
    w = sum((x - mx) * (y - my) for x, y in zip(xs, ys)) / sum((x - mx) ** 2 for x in xs)
    return w, my - w * mx, mx, my


@diagram("ai-regression-line")
def _regression_line():
    """Revision hours against score, the least squares line and its residuals."""
    w, b, mx, my = _least_squares(HOURS, SCORE)
    P = Plot(84, 44, 430, 236, (0, 9), (30, 90))
    body = [text(380, 22, "Fitting a line: score = w × hours + b", 12, 650, fill=MUTED)]
    body.append(P.axes(range(0, 10), range(30, 91, 10), "hours of revision", "test score"))
    body.append(grad("ai-rl-g", [(0, VIOLET), (1, PINK)]))
    for x, y in zip(HOURS, SCORE):
        p = w * x + b
        colour = PINK if y >= p else BLUE
        body.append(line(P.px(x), P.py(p), P.px(x), P.py(y), stroke=tv(colour), w=2.2,
                         dash="3 2"))
    x0, x1 = 0, 9
    body.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="url(#ai-rl-g)" '
                'stroke-width="3.4" stroke-linecap="round"/>'
                % (P.px(x0), P.py(w * x0 + b), P.px(x1), P.py(w * x1 + b)))
    # slope triangle between 1 and 2 hours
    ax, ay = P.pt(1, w * 1 + b)
    bx, by = P.pt(2, w * 1 + b)
    cx, cy = P.pt(2, w * 2 + b)
    body.append(path("M%.1f %.1f L%.1f %.1f L%.1f %.1f" % (ax, ay, bx, by, cx, cy),
                     stroke=tv(ORANGE), w=2))
    body.append(text((ax + bx) / 2.0, ay + 13, "1 hour", 8.8, 700, fill=tv(ORANGE)))
    body.append(text(bx + 6, (by + cy) / 2.0 + 3, "+%.1f marks" % w, 8.8, 700, anchor="start",
                     fill=tv(ORANGE)))
    # intercept
    ix, iy = P.pt(0, b)
    body.append(circle(ix, iy, 5, fill=ORANGE, stroke=FILL, w=1.5))
    body.append(text(ix + 10, iy + 4, "b = %.1f" % b, 9.6, 750, anchor="start", fill=tv(ORANGE)))
    for x, y in zip(HOURS, SCORE):
        body.append(circle(P.px(x), P.py(y), 5.5, fill=VIOLET, stroke=FILL, w=1.5))
    # the mean point
    mpx, mpy = P.pt(mx, my)
    body.append('<rect x="%.1f" y="%.1f" width="11" height="11" fill="%s" stroke="%s" '
                'stroke-width="1.5" transform="rotate(45 %.1f %.1f)"/>'
                % (mpx - 5.5, mpy - 5.5, AMBER, DARK, mpx, mpy))
    body.append(text(mpx + 10, mpy + 18, "mean point (%.1f, %.1f)" % (mx, my), 8.8, 700,
                     anchor="start", fill=INK))
    # side panel
    body.append(tint(548, 52, 190, 92, VIOLET, op=0.1, r=12))
    body.append(text(643, 76, "the learned model", 10, 750, fill=tv(VIOLET)))
    body.append(text(643, 100, "w = %.2f" % w, 12, 800, fill=INK, mono=True))
    body.append(text(643, 122, "b = %.2f" % b, 12, 800, fill=INK, mono=True))
    body.append(tint(548, 160, 190, 112, SLATE, op=0.07, r=12))
    body.append(line(564, 184, 564, 200, stroke=tv(PINK), w=2.2, dash="3 2"))
    body.append(text(574, 196, "above the line", 9.6, 650, anchor="start", fill=INK))
    body.append(line(564, 212, 564, 228, stroke=tv(BLUE), w=2.2, dash="3 2"))
    body.append(text(574, 224, "below the line", 9.6, 650, anchor="start", fill=INK))
    body.append(text(564, 254, "each stick is a residual:", 9, 600, anchor="start", fill=MUTED))
    body.append(text(564, 266, "actual minus predicted", 9, 600, anchor="start", fill=MUTED))
    desc = ("A scatter plot of ten students' hours of revision, from 1 to 8, against "
            "test scores from 38 to 86. The least squares line rises from a score of "
            "%.1f at zero hours with a slope of %.2f marks per hour, shown by a small "
            "triangle: 1 hour along, %.1f marks up. Dashed vertical sticks join each "
            "point to the line: these are the residuals, pink where the point is above "
            "the line and blue where it is below. The line passes through the mean "
            "point, %.1f hours and %.1f marks." % (b, w, w, mx, my))
    return figure("ai-regl", 760, 330, "".join(body), "A least squares regression line",
                  desc, "Least squares chooses w and b to make the squared residuals "
                  "as small as possible.")


# ===================================== Level 4: a regression plane in 3D

@diagram("ai-regression-plane")
def _regression_plane():
    """Two features and a target: points above and below a fitted plane."""
    pts = [(60, 1, 180), (75, 2, 230), (90, 2, 265), (110, 3, 320), (130, 3, 352),
           (150, 4, 420), (70, 3, 255), (120, 2, 300), (160, 5, 470), (95, 4, 330),
           (140, 2, 330), (55, 2, 205)]
    xs = [[1, a, r] for a, r, _ in pts]
    ys = [p for _, _, p in pts]
    a = [[sum(row[i] * row[j] for row in xs) for j in range(3)] for i in range(3)]
    bb = [sum(row[i] * y for row, y in zip(xs, ys)) for i in range(3)]
    c0, c1, c2 = _solve(a, bb)

    def f(area, beds):
        return c0 + c1 * area + c2 * beds
    XR, YR, ZR = (50, 170), (1, 5), (100, 500)
    yaw, pitch, scale, ox, oy = -0.62, 0.42, 132, 290, 262

    def P(x, y, z):
        nx = (x - 110) / 60.0
        ny = (y - 3) / 2.0
        nz = (z - ZR[0]) / float(ZR[1] - ZR[0]) * 1.15
        return project(nx, ny, nz, yaw, pitch, scale, ox, oy)

    body = [text(380, 22, "Two features: the model is a tilted plane", 12, 650, fill=MUTED)]
    # floor and axes
    corners = [P(XR[0], YR[0], ZR[0]), P(XR[1], YR[0], ZR[0]), P(XR[1], YR[1], ZR[0]),
               P(XR[0], YR[1], ZR[0])]
    body.append('<polygon points="%s" fill="%s" fill-opacity="0.6" stroke="%s" '
                'stroke-width="1"/>' % (" ".join("%.1f,%.1f" % c[:2] for c in corners), FILL2, LINE))
    for k in range(1, 6):
        g0, g1 = P(50 + k * 20, YR[0], ZR[0]), P(50 + k * 20, YR[1], ZR[0])
        body.append(line(g0[0], g0[1], g1[0], g1[1], stroke=LINE, w=0.5, dash="2 3"))
    up0, up1 = P(XR[0], YR[1], ZR[0]), P(XR[0], YR[1], ZR[1])
    body.append(line(up0[0], up0[1], up1[0], up1[1], stroke=LINE, w=1.4))
    lx = P(110, YR[0], ZR[0])
    body.append(text(lx[0] - 6, lx[1] + 26, "floor area (m²)", 9.6, 700, fill=MUTED))
    ly = P(XR[1], 3, ZR[0])
    body.append(text(ly[0] + 26, ly[1] + 12, "bedrooms", 9.6, 700, anchor="start", fill=MUTED))
    body.append(text(up1[0] - 8, up1[1] - 6, "price (£k)", 9.6, 700, anchor="end", fill=MUTED))
    below = [p for p in pts if p[2] < f(p[0], p[1])]
    above = [p for p in pts if p[2] >= f(p[0], p[1])]

    def dot(p, colour):
        a_, r_, pr = p
        top = P(a_, r_, pr)
        on = P(a_, r_, f(a_, r_))
        return (line(on[0], on[1], top[0], top[1], stroke=tv(colour), w=1.8, dash="3 2")
                + circle(top[0], top[1], 5.5, fill=colour, stroke=FILL, w=1.4))
    for p in below:
        body.append(dot(p, BLUE))
    # the plane, as a grid of quads coloured by height
    n = 8
    quads = []
    for i in range(n):
        for j in range(n):
            xa = XR[0] + (XR[1] - XR[0]) * i / float(n)
            xb = XR[0] + (XR[1] - XR[0]) * (i + 1) / float(n)
            ya = YR[0] + (YR[1] - YR[0]) * j / float(n)
            yb = YR[0] + (YR[1] - YR[0]) * (j + 1) / float(n)
            cs = [P(xa, ya, f(xa, ya)), P(xb, ya, f(xb, ya)), P(xb, yb, f(xb, yb)),
                  P(xa, yb, f(xa, yb))]
            depth = sum(c[2] for c in cs) / 4.0
            t = (f((xa + xb) / 2, (ya + yb) / 2) - 150) / 330.0
            t = min(1.0, max(0.0, t))
            quads.append((depth, cs, t))
    quads.sort(key=lambda q: -q[0])
    for _, cs, t in quads:
        body.append('<polygon points="%s" fill="%s" fill-opacity="0.62" stroke="#FFFFFF" '
                    'stroke-opacity="0.5" stroke-width="0.6"/>'
                    % (" ".join("%.1f,%.1f" % c[:2] for c in cs), plasma(0.2 + 0.7 * t)))
    for p in above:
        body.append(dot(p, PINK))
    body.append(tint(548, 60, 192, 120, VIOLET, op=0.1, r=12))
    body.append(text(644, 84, "fitted by least squares", 10, 750, fill=tv(VIOLET)))
    body.append(text(644, 108, "price = %.2f × area" % c1, 10.5, 750, fill=INK, mono=True))
    body.append(text(644, 128, "+ %.1f × bedrooms" % c2, 10.5, 750, fill=INK, mono=True))
    body.append(text(644, 148, "%+.1f" % c0, 10.5, 750, fill=INK, mono=True))
    body.append(text(644, 168, "(in £ thousands)", 9, 600, fill=MUTED))
    body.append(tint(548, 196, 192, 72, SLATE, op=0.07, r=12))
    body.append(circle(566, 218, 5.5, fill=PINK, stroke=FILL, w=1.4))
    body.append(text(578, 222, "house above the plane", 9.4, 650, anchor="start", fill=INK))
    body.append(circle(566, 246, 5.5, fill=BLUE, stroke=FILL, w=1.4))
    body.append(text(578, 250, "house below the plane", 9.4, 650, anchor="start", fill=INK))
    desc = ("A 3D graph with floor area and bedrooms along the floor and price going "
            "up. A tilted plane, coloured from deep blue where prices are low to "
            "yellow where they are high, has been fitted through twelve houses by "
            "least squares: price in thousands of pounds = %.2f times floor area plus "
            "%.1f times bedrooms %+.1f. Each house is a dot joined to the plane by a "
            "dashed residual line, pink for houses above the plane and blue for "
            "houses below it." % (c1, c2, c0))
    return figure("ai-regp", 760, 340, "".join(body),
                  "Multiple linear regression as a plane", desc,
                  "Every extra feature adds a dimension. Beyond three, the plane "
                  "becomes a hyperplane we cannot draw.")


# ================================ Level 4: underfit, good fit, overfit

_FX = [0.5, 1.6, 2.4, 3.7, 4.9, 6.1, 7.2, 8.6, 9.5]
_NOISE = [0.35, -0.4, 0.3, -0.25, 0.45, -0.3, 0.2, -0.35, 0.3]


def _truth(x):
    return 6 - 0.13 * (x - 5) ** 2


@diagram("ai-fit-three")
def _fit_three():
    """The same data fitted by a line, a quadratic and an interpolating polynomial."""
    ys = [_truth(x) + e for x, e in zip(_FX, _NOISE)]
    tests = [(5.5, _truth(5.5) + 0.15), (9.1, _truth(9.1) - 0.1)]
    line_c = _polyfit(_FX, ys, 1)
    quad_c = _polyfit(_FX, ys, 2)
    models = [("Underfitting", "a straight line misses the curve", _poly(line_c), BLUE),
              ("A good fit", "a gentle curve follows the trend", _poly(quad_c), GREEN),
              ("Overfitting", "passes through every point, wildly", _lagrange(_FX, ys), RED)]
    body = [text(380, 22, "Too simple, about right, too flexible", 12, 650, fill=MUTED)]
    for k, (title, sub, f, colour) in enumerate(models):
        x0 = 20 + k * 246
        body.append(tint(x0, 38, 232, 222, colour, op=0.07, r=12))
        body.append(text(x0 + 116, 60, title, 11.5, 800, fill=tv(colour)))
        body.append(text(x0 + 116, 76, sub, 9, 600, fill=MUTED))
        P = Plot(x0 + 16, 88, 200, 150, (0, 10), (0, 8))
        cid = "ai-fit3-c%d" % k
        body.append(P.clip(cid))
        body.append(line(P.x, P.y + P.h, P.x + P.w, P.y + P.h, stroke=LINE, w=1.2))
        body.append(line(P.x, P.y, P.x, P.y + P.h, stroke=LINE, w=1.2))
        body.append('<path d="%s" fill="none" stroke="%s" stroke-width="3" '
                    'clip-path="url(#%s)" stroke-linecap="round"/>'
                    % (P.curve(f, 240), tv(colour), cid))
        for x, y in zip(_FX, ys):
            body.append(circle(P.px(x), P.py(y), 4.5, fill=VIOLET, stroke=FILL, w=1.2))
        for x, y in tests:
            body.append('<circle cx="%.1f" cy="%.1f" r="5" fill="none" stroke="%s" '
                        'stroke-width="2.2"/>' % (P.px(x), P.py(y), tv(ORANGE)))
        train = sum((f(x) - y) ** 2 for x, y in zip(_FX, ys)) / len(ys)
        test = sum((f(x) - y) ** 2 for x, y in tests) / len(tests)
        body.append(text(x0 + 116, 252, "training error %.2f · test error %.2f"
                         % (train, test), 8.8, 700, fill=INK))
    body.append(circle(250, 282, 4.5, fill=VIOLET, stroke=FILL, w=1.2))
    body.append(text(260, 286, "training points", 9.4, 650, anchor="start", fill=MUTED))
    body.append('<circle cx="400" cy="282" r="5" fill="none" stroke="%s" stroke-width="2.2"/>'
                % tv(ORANGE))
    body.append(text(410, 286, "unseen test points", 9.4, 650, anchor="start", fill=MUTED))
    desc = ("Three panels show the same nine training points, which follow a gentle "
            "hump, and two unseen test points. In the first, a straight line underfits: "
            "it misses the curve, so both its training and test errors are high. In "
            "the second, a gentle curve fits well, with low training and test errors. "
            "In the third, a high-degree polynomial passes exactly through every "
            "training point, giving zero training error, but swings wildly between "
            "them, so its test error is large.")
    return figure("ai-fit3", 760, 296, "".join(body),
                  "Underfitting, a good fit and overfitting", desc,
                  "The overfitted model has the lowest training error and the "
                  "highest test error.")


# =================================== Level 4: three decision boundaries

_CLS = [((1.0, 1.2), 0), ((1.6, 2.6), 0), ((2.2, 1.0), 0), ((0.8, 3.4), 0), ((2.8, 2.0), 0),
        ((1.4, 4.6), 0), ((3.4, 1.0), 0), ((2.2, 3.4), 0), ((4.2, 1.6), 0), ((0.6, 5.6), 0),
        ((3.2, 3.0), 0), ((5.0, 0.8), 0), ((4.6, 5.4), 1), ((5.6, 4.2), 1), ((6.4, 5.8), 1),
        ((3.8, 6.4), 1), ((6.8, 3.0), 1), ((5.2, 6.6), 1), ((7.0, 6.8), 1), ((6.0, 2.2), 1),
        ((2.8, 6.0), 1), ((7.2, 4.6), 1), ((4.4, 4.0), 1), ((1.8, 6.8), 1), ((3.6, 4.6), 0),
        ((5.4, 3.0), 1)]


def _logistic(data, steps=3000, lr=0.15):
    w1 = w2 = b = 0.0
    for _ in range(steps):
        g1 = g2 = gb = 0.0
        for (x1, x2), y in data:
            z = w1 * (x1 - 4) + w2 * (x2 - 4) + b
            p = 1 / (1 + math.exp(-z))
            g1 += (p - y) * (x1 - 4)
            g2 += (p - y) * (x2 - 4)
            gb += p - y
        n = float(len(data))
        w1 -= lr * g1 / n
        w2 -= lr * g2 / n
        b -= lr * gb / n
    return lambda x1, x2: 1 / (1 + math.exp(-(w1 * (x1 - 4) + w2 * (x2 - 4) + b)))


def _knn_prob(data, k):
    def f(x1, x2):
        near = sorted(data, key=lambda d: (d[0][0] - x1) ** 2 + (d[0][1] - x2) ** 2)[:k]
        return sum(y for _, y in near) / float(k)
    return f


def _gini(ys):
    if not ys:
        return 0.0
    p = sum(ys) / float(len(ys))
    return 1 - p * p - (1 - p) * (1 - p)


def _tree(data, depth):
    ys = [y for _, y in data]
    if depth == 0 or _gini(ys) == 0:
        p = sum(ys) / float(len(ys))
        return lambda x1, x2: p
    best = None
    for feat in (0, 1):
        for t in sorted(set(d[0][feat] for d in data)):
            left = [d for d in data if d[0][feat] < t]
            right = [d for d in data if d[0][feat] >= t]
            if not left or not right:
                continue
            g = (len(left) * _gini([y for _, y in left]) +
                 len(right) * _gini([y for _, y in right])) / float(len(data))
            if best is None or g < best[0]:
                best = (g, feat, t, left, right)
    if best is None:
        p = sum(ys) / float(len(ys))
        return lambda x1, x2: p
    _, feat, t, left, right = best
    lf, rf = _tree(left, depth - 1), _tree(right, depth - 1)
    return lambda x1, x2: lf(x1, x2) if (x1, x2)[feat] < t else rf(x1, x2)


@diagram("ai-boundaries")
def _boundaries():
    """Logistic regression, kNN and a decision tree on the same data."""
    models = [("Logistic regression", "a straight boundary", _logistic(_CLS)),
              ("k-nearest neighbours, k = 3", "follows the data closely", _knn_prob(_CLS, 3)),
              ("Decision tree, depth 3", "boxes with straight sides", _tree(_CLS, 3))]
    body = [text(380, 22, "Same data, three classifiers, three kinds of boundary", 12, 650,
                 fill=MUTED)]
    G = 30
    for k, (title, sub, f) in enumerate(models):
        x0 = 20 + k * 246
        P = Plot(x0 + 6, 70, 220, 196, (0, 8), (0, 8))
        body.append(text(x0 + 116, 46, title, 10.5, 800, fill=INK))
        body.append(text(x0 + 116, 62, sub, 9, 600, fill=MUTED))
        cw, ch = P.w / G, P.h / G
        cells = ['<g shape-rendering="crispEdges">']
        for j in range(G):
            row = []
            for i in range(G):
                p = f((i + 0.5) / G * 8, (j + 0.5) / G * 8)
                sure = 2 if abs(p - 0.5) > 0.3 else 1
                row.append((PINK if p >= 0.5 else BLUE, sure))
            i = 0
            while i < G:
                k2 = i
                while k2 + 1 < G and row[k2 + 1] == row[i]:
                    k2 += 1
                colour, sure = row[i]
                cells.append('<rect x="%.2f" y="%.2f" width="%.2f" height="%.2f" fill="%s" '
                             'fill-opacity="%s"/>' % (P.x + i * cw, P.y + P.h - (j + 1) * ch,
                                                      (k2 - i + 1) * cw, ch, colour,
                                                      "0.3" if sure == 2 else "0.16"))
                i = k2 + 1
        cells.append("</g>")
        body.append("".join(cells))
        body.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="none" '
                    'stroke="%s" stroke-width="1.2"/>' % (P.x, P.y, P.w, P.h, LINE))
        for (a, b), y in _CLS:
            if y:
                body.append(circle(P.px(a), P.py(b), 5, fill=PINK, stroke=FILL, w=1.4))
            else:
                body.append(_square(P.px(a), P.py(b), 9.5, BLUE))
    body.append(circle(268, 290, 5, fill=PINK, stroke=FILL, w=1.4))
    body.append(text(278, 294, "class A", 9.4, 650, anchor="start", fill=MUTED))
    body.append(_square(388, 290, 9.5, BLUE))
    body.append(text(398, 294, "class B", 9.4, 650, anchor="start", fill=MUTED))
    body.append(text(470, 294, "shading: the region each class gets", 9.4, 650,
                     anchor="start", fill=MUTED))
    desc = ("Three square panels show the same 26 points of two classes, pink circles "
            "mostly towards the top right and blue squares towards the bottom left, "
            "with some mixing in the middle. The background of each panel is shaded "
            "pink or blue by the class each model would predict there. Logistic "
            "regression divides the square with one straight diagonal boundary. "
            "k-nearest neighbours with k equal to 3 draws a wiggly boundary that bends "
            "around individual points. A decision tree of depth 3 divides the square "
            "into rectangles with edges parallel to the axes.")
    return figure("ai-bound", 760, 306, "".join(body), "Three kinds of decision boundary",
                  desc, "Each algorithm's assumptions decide what shape of boundary "
                  "it can learn.")


# ================================================ Level 4: kNN voting

_KNN_PTS = [((4.5, 4.1), 0), ((5.2, 4.95), 0), ((3.4, 5.2), 0), ((3.2, 3.6), 0),
            ((2.4, 5.0), 0), ((2.0, 3.2), 0), ((3.0, 6.4), 0), ((1.6, 5.8), 0),
            ((2.6, 2.2), 0), ((5.5, 4.0), 1), ((5.9, 5.0), 1), ((6.0, 3.6), 1),
            ((5.6, 5.6), 1), ((5.0, 2.95), 1), ((6.8, 4.4), 1), ((7.0, 2.6), 1),
            ((6.6, 6.2), 1), ((7.4, 5.4), 1)]
_QUERY = (4.9, 4.4)


@diagram("ai-knn")
def _knn():
    """A query point and its 3 and 7 nearest neighbours, which disagree."""
    P = Plot(46, 40, 420, 270, (1, 8.2), (1.4, 7.0))
    body = [text(380, 22, "Who are my neighbours? The answer depends on k", 12, 650,
                 fill=MUTED)]
    ranked = sorted(_KNN_PTS, key=lambda d: math.dist(d[0], _QUERY))
    qx, qy = P.pt(*_QUERY)
    scale = P.w / (P.xr[1] - P.xr[0])
    for k, colour in ((7, ORANGE), (3, VIOLET)):
        r = math.dist(ranked[k - 1][0], _QUERY) * scale + 9
        body.append('<circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" fill-opacity="0.08" '
                    'stroke="%s" stroke-width="2.2" stroke-dasharray="6 4"/>'
                    % (qx, qy, r, colour, tv(colour)))
        body.append(text(qx + r * 0.72 + 4, qy - r * 0.72 - 2, "k = %d" % k, 10.5, 800,
                         anchor="start", fill=tv(colour)))
    for (a, b), y in _KNN_PTS:
        x, yy = P.pt(a, b)
        if y:
            body.append(circle(x, yy, 6, fill=PINK, stroke=FILL, w=1.5))
        else:
            body.append(_square(x, yy, 11, BLUE))
    star = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = 11 if i % 2 == 0 else 4.8
        star.append("%.1f,%.1f" % (qx + rad * math.cos(ang), qy + rad * math.sin(ang)))
    body.append('<polygon points="%s" fill="%s" stroke="%s" stroke-width="1.2"/>'
                % (" ".join(star), AMBER, DARK))
    body.append(text(qx - 14, qy + 4, "new point", 9.4, 750, anchor="end", fill=INK))
    results = []
    for k in (3, 7):
        near = ranked[:k]
        pinks = sum(y for _, y in near)
        blues = k - pinks
        winner = "pink circle" if pinks > blues else "blue square"
        results.append((k, pinks, blues, winner))
    for i, (k, pinks, blues, winner) in enumerate(results):
        colour = VIOLET if k == 3 else ORANGE
        y0 = 70 + i * 112
        body.append(tint(500, y0, 238, 96, colour, op=0.1, r=12))
        body.append(text(619, y0 + 24, "k = %d nearest neighbours" % k, 11, 800, fill=tv(colour)))
        body.append(text(619, y0 + 46, "%d pink circle%s, %d blue square%s"
                         % (pinks, "" if pinks == 1 else "s", blues, "" if blues == 1 else "s"),
                         10, 650, fill=INK))
        body.append(text(619, y0 + 70, "prediction: %s" % winner, 10.5, 800,
                         fill=tv(PINK) if winner.startswith("pink") else tv(BLUE)))
    body.append(text(619, 312, "Same point, different k, different answer.", 9.6, 650,
                     fill=MUTED))
    desc = ("A scatter of blue squares on the left and pink circles on the right, with a "
            "new point, a star, near the middle. A small dashed circle encloses its 3 "
            "nearest neighbours: %d pink and %d blue, so with k equal to 3 the "
            "prediction is %s. A larger dashed circle encloses its 7 nearest "
            "neighbours: %d pink and %d blue, so with k equal to 7 the prediction is "
            "%s." % (results[0][1], results[0][2], results[0][3], results[1][1],
                     results[1][2], results[1][3]))
    return figure("ai-knn", 760, 330, "".join(body), "k-nearest neighbours voting", desc,
                  "k is a setting you choose, a hyperparameter, and it changes the "
                  "model's answers.")


# ============================================ Level 4: the sigmoid curve

@diagram("ai-sigmoid")
def _sigmoid():
    """The sigmoid squashes any score into a probability."""
    P = Plot(70, 44, 520, 220, (-6, 6), (0, 1))
    body = [text(380, 22, "The sigmoid: any score in, a probability out", 12, 650,
                 fill=MUTED)]
    body.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" '
                'fill-opacity="0.08"/>' % (P.x, P.y, P.w / 2, P.h, BLUE))
    body.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" '
                'fill-opacity="0.08"/>' % (P.x + P.w / 2, P.y, P.w / 2, P.h, PINK))
    body.append(P.axes(range(-6, 7, 2), [0, 0.25, 0.5, 0.75, 1], "score z = w·x + b",
                       "probability"))
    y5 = P.py(0.5)
    body.append(line(P.x, y5, P.x + P.w, y5, stroke=tv(ORANGE), w=1.6, dash="6 4"))
    body.append(text(P.x + P.w - 4, y5 - 6, "threshold 0.5", 9.4, 750, anchor="end",
                     fill=tv(ORANGE)))
    body.append(grad("ai-sig-g", [(0, BLUE), (0.5, VIOLET), (1, PINK)]))
    body.append('<path d="%s" fill="none" stroke="url(#ai-sig-g)" stroke-width="4" '
                'stroke-linecap="round"/>' % P.curve(lambda z: 1 / (1 + math.exp(-z)), 160))
    for z in (-2, 0, 2):
        s = 1 / (1 + math.exp(-z))
        x, y = P.pt(z, s)
        body.append(circle(x, y, 5.5, fill=AMBER, stroke=DARK, w=1.2))
        body.append(text(x + (10 if z <= 0 else -10), y + (16 if z < 0 else -9),
                         ("z = %d → %.2f" % (z, s)).replace("-", "−"), 9.4, 750,
                         anchor="start" if z <= 0 else "end", fill=INK))
    body.append(text(P.x + P.w / 4, P.y + 22, "predict class 0", 10, 800, fill=tv(BLUE)))
    body.append(text(P.x + 3 * P.w / 4, P.y + P.h - 12, "predict class 1", 10, 800,
                     fill=tv(PINK)))
    body.append(tint(612, 60, 130, 186, VIOLET, op=0.1, r=12))
    body.append(text(677, 86, "σ(z) =", 12, 800, fill=INK))
    body.append('<text x="677" y="112" text-anchor="middle" font-size="11" '
                'font-weight="750" fill="%s">1 ÷ (1 + e<tspan font-size="8" dy="-6">−z'
                '</tspan><tspan dy="6">)</tspan></text>' % INK)
    for i, (z, lab) in enumerate([("−6", "0.0025"), ("0", "0.5"), ("+6", "0.9975")]):
        body.append(text(632, 144 + i * 26, "z = " + z, 9.6, 700, anchor="start",
                         fill=MUTED))
        body.append(text(724, 144 + i * 26, lab, 9.6, 750, anchor="end", fill=INK))
    desc = ("A graph of the sigmoid function for scores z from minus 6 to 6. The curve "
            "is S-shaped, rising from almost 0 on the left through exactly 0.5 at z "
            "equal to 0 to almost 1 on the right. Marked points: z equal to minus 2 "
            "gives 0.12, z equal to 0 gives 0.50 and z equal to 2 gives 0.88. A "
            "dashed threshold line at 0.5 divides the graph: the left half, shaded "
            "blue, predicts class 0, and the right half, shaded pink, predicts class "
            "1. A side panel gives the formula sigma of z equals 1 divided by 1 plus "
            "e to the minus z.")
    return figure("ai-sig", 760, 306, "".join(body), "The sigmoid function", desc,
                  "Large positive scores mean nearly certain yes; large negative "
                  "scores, nearly certain no.")


# ================================================ Level 4: a decision tree

@diagram("ai-decision-tree")
def _decision_tree():
    """A spam tree with the class counts and Gini impurity at every node."""
    def gini(s, o):
        n = float(s + o)
        return 1 - (s / n) ** 2 - (o / n) ** 2

    body = [text(380, 22, "A decision tree for spam, with Gini impurity at every node",
                 12, 650, fill=MUTED)]

    def node(cx, y, q, s, o, w=200):
        x = cx - w / 2.0
        out = [tint(x, y, w, 64, VIOLET, op=0.1, r=10)]
        out.append(text(cx, y + 18, q, 10, 800, fill=INK))
        tot = float(s + o)
        out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="12" rx="3" fill="%s"/>'
                   % (x + 12, y + 28, (w - 24) * s / tot, RED))
        out.append('<rect x="%.1f" y="%.1f" width="%.1f" height="12" rx="3" fill="%s"/>'
                   % (x + 12 + (w - 24) * s / tot, y + 28, (w - 24) * o / tot, GREEN))
        out.append(text(cx, y + 56, "%d spam, %d not · Gini %.2f" % (s, o, gini(s, o)),
                        9, 650, fill=MUTED))
        return "".join(out)

    def leaf(cx, y, verdict, s, o, colour):
        w = 132
        out = [solid(cx - w / 2.0, y, w, 50, colour, verdict,
                     "%d spam, %d not" % (s, o), r=10, size=11, sub_size=8.8)]
        return "".join(out)

    def edge(x1, y1, x2, y2, lab, left):
        mx, my = (x1 + x2) / 2.0, (y1 + y2) / 2.0
        return (line(x1, y1, x2, y2, stroke=LINE, w=2)
                + solid(mx - 18, my - 10, 36, 20, SLATE if not left else INDIGO,
                        "yes" if left else "no", r=10, size=9.4))

    body.append(node(380, 40, "Is the sender in your contacts?", 40, 60, 236))
    body.append(edge(320, 104, 170, 150, "yes", True))
    body.append(edge(440, 104, 520, 150, "no", False))
    body.append(leaf(170, 150, "not spam", 2, 43, GREEN))
    body.append(node(520, 150, "More than 3 links?", 38, 17))
    body.append(edge(470, 214, 380, 252, "yes", True))
    body.append(edge(570, 214, 640, 252, "no", False))
    body.append(leaf(380, 252, "spam", 28, 2, RED))
    body.append(node(640, 252, "Contains the word 'free'?", 10, 15, 200))
    body.append(edge(600, 316, 560, 350, "yes", True))
    body.append(edge(680, 316, 716, 350, "no", False))
    body.append(leaf(546, 350, "spam", 8, 1, RED))
    body.append(leaf(690, 350, "not spam", 2, 13, GREEN))
    body.append('<rect x="24" y="248" width="14" height="12" rx="3" fill="%s"/>' % RED)
    body.append(text(44, 258, "spam", 9.4, 650, anchor="start", fill=MUTED))
    body.append('<rect x="24" y="270" width="14" height="12" rx="3" fill="%s"/>' % GREEN)
    body.append(text(44, 280, "not spam", 9.4, 650, anchor="start", fill=MUTED))
    body.append(text(24, 306, "The first question gives the", 9.4, 650, anchor="start", fill=INK))
    body.append(text(24, 320, "biggest drop in impurity.", 9.4, 650, anchor="start", fill=INK))
    desc = ("A decision tree for 100 emails, 40 spam and 60 not, Gini impurity 0.48. The "
            "root asks: is the sender in your contacts? Yes leads to a leaf, not spam, "
            "with 2 spam and 43 not. No leads to 38 spam and 17 not, Gini 0.43, which "
            "asks: more than 3 links? Yes leads to a leaf, spam, with 28 spam and 2 "
            "not. No leads to 10 spam and 15 not, Gini 0.48, which asks: does it "
            "contain the word free? Yes gives a spam leaf with 8 spam and 1 not; no "
            "gives a not spam leaf with 2 spam and 13 not. Each node shows a bar of "
            "the spam and not spam proportions.")
    return figure("ai-dtree", 760, 410, "".join(body), "A decision tree with Gini impurity",
                  desc, "Each question is the one that makes the groups below it as "
                  "pure as possible.")


# =========================================== Level 4: k-means, step by step

_KM_PTS = [(1.2, 1.5), (1.8, 2.4), (2.4, 1.2), (1.0, 2.8), (2.6, 2.2), (1.6, 0.8),
           (6.6, 6.8), (7.4, 6.2), (6.2, 7.6), (7.8, 7.4), (7.0, 5.6), (8.2, 6.6),
           (1.6, 7.0), (2.4, 7.8), (1.0, 6.2), (2.8, 6.6), (2.0, 8.4), (3.2, 7.4),
           (4.6, 3.6), (7.6, 2.0), (6.8, 1.4), (8.0, 1.2), (7.2, 2.8), (6.2, 2.2)]
_KM_START = [(1.2, 1.5), (2.4, 1.2), (6.6, 6.8), (7.4, 6.2)]
_KM_COLOURS = [VIOLET, ORANGE, TEAL, PINK]


def _kmeans_rounds(points, cents, rounds=8):
    """Every assignment and centroid position until nothing changes."""
    history = []
    for _ in range(rounds):
        assign = [min(range(len(cents)), key=lambda i: math.dist(p, cents[i])) for p in points]
        history.append(("assign", list(cents), assign))
        new = []
        for i in range(len(cents)):
            mine = [p for p, a in zip(points, assign) if a == i]
            new.append((sum(x for x, _ in mine) / len(mine), sum(y for _, y in mine) / len(mine))
                       if mine else cents[i])
        history.append(("update", list(new), assign, list(cents)))
        if all(math.dist(a, b) < 1e-9 for a, b in zip(new, cents)):
            break
        cents = new
    return history


@diagram("ai-kmeans-steps")
def _kmeans_steps():
    """k-means on four clusters from a poor start, one stage at a time."""
    hist = _kmeans_rounds(_KM_PTS, _KM_START)
    P = Plot(150, 40, 300, 260, (0, 9), (0, 9))
    base = [text(380, 22, "k-means with k = 4: assign, update, repeat", 12, 650,
                 fill=MUTED)]
    base.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="8" fill="%s" '
                'fill-opacity="0.5" stroke="%s"/>' % (P.x, P.y, P.w, P.h, FILL2, LINE))

    def cross(x, y, colour):
        return ('<g transform="translate(%.1f %.1f)"><circle r="11" fill="%s" stroke="%s" '
                'stroke-width="2"/><path d="M-5 -5 L5 5 M5 -5 L-5 5" stroke="#FFFFFF" '
                'stroke-width="2.6" stroke-linecap="round"/></g>' % (x, y, colour, FILL))

    stages, labels = [], []
    pts0 = "".join(circle(P.px(x), P.py(y), 5.5, fill=SLATE, stroke=FILL, w=1.3)
                   for x, y in _KM_PTS)
    stages.append(step(1, pts0, "24 points with no labels"))
    labels.append("24 points with no labels")
    s2 = pts0 + "".join(cross(P.px(x), P.py(y), _KM_COLOURS[i])
                        for i, (x, y) in enumerate(_KM_START))
    stages.append(step(2, s2, "Start: 4 centroids at random points"))
    labels.append("Start: 4 centroids at random points")
    rnd = 0
    for h in hist:
        if h[0] == "assign":
            rnd += 1
            _, cents, assign = h
            body = "".join(circle(P.px(x), P.py(y), 5.5, fill=_KM_COLOURS[a], stroke=FILL, w=1.3)
                           for (x, y), a in zip(_KM_PTS, assign))
            body += "".join(cross(P.px(x), P.py(y), _KM_COLOURS[i]) for i, (x, y) in enumerate(cents))
            lab = "Round %d, assign: each point joins its nearest centroid" % rnd
        else:
            _, new, assign, old = h
            body = "".join(circle(P.px(x), P.py(y), 5.5, fill=_KM_COLOURS[a], stroke=FILL, w=1.3)
                           for (x, y), a in zip(_KM_PTS, assign))
            moved = False
            for i, ((ox, oy), (nx, ny)) in enumerate(zip(old, new)):
                if math.dist((ox, oy), (nx, ny)) > 1e-6:
                    moved = True
                    body += arrow(P.px(ox), P.py(oy), P.px(nx), P.py(ny), tv(_KM_COLOURS[i]), 2)
            body += "".join(cross(P.px(x), P.py(y), _KM_COLOURS[i]) for i, (x, y) in enumerate(new))
            lab = ("Round %d, update: centroids move to the mean of their points" % rnd
                   if moved else "Converged: nothing moves, so k-means stops")
        stages.append(step(len(stages) + 1, body, lab))
        labels.append(lab)
    n_rounds = rnd
    note = [tint(476, 60, 266, 132, VIOLET, op=0.08, r=12),
            text(490, 84, "1. Assign each point to the", 10, 650, anchor="start", fill=INK),
            text(490, 100, "nearest centroid (the ×).", 10, 650, anchor="start", fill=INK),
            text(490, 124, "2. Move each centroid to the", 10, 650, anchor="start", fill=INK),
            text(490, 140, "mean of its points.", 10, 650, anchor="start", fill=INK),
            text(490, 164, "3. Repeat until nothing moves.", 10, 650, anchor="start", fill=INK),
            text(609, 222, "Two centroids started in the", 9.4, 600, fill=MUTED),
            text(609, 238, "same cluster; watch one leave.", 9.4, 600, fill=MUTED)]
    base.extend(note)
    desc = ("A stepped animation of k-means with k equal to 4 on 24 unlabelled points "
            "that form four groups: bottom left, top right, top left and bottom right. "
            "The four starting centroids are badly placed, two in the bottom left group "
            "and two in the top right group. In each round every point is coloured by "
            "its nearest centroid, then each centroid moves to the mean of its points, "
            "shown by arrows. Over %d rounds the centroids spread out until there is "
            "one in each group, and then nothing moves, so the algorithm stops." % n_rounds)
    return figure_steps("ai-km", 760, 320, "".join(base), stages,
                        "k-means clustering step by step", desc,
                        "Press Play to watch the centroids find the four groups.",
                        labels=labels)


# ================================================ Level 5: the loss curve

def _mse_b(w, b=33.2):
    return sum((w * x + b - y) ** 2 for x, y in zip(HOURS, SCORE)) / float(len(HOURS))


@diagram("ai-loss-curve")
def _loss_curve():
    """Three candidate lines and where each sits on the loss curve."""
    body = [text(380, 22, "Each value of w is a different line, with a different loss",
                 12, 650, fill=MUTED)]
    picks = [(3.0, BLUE, "w = 3"), (6.5, GREEN, "w = 6.5"), (10.0, ORANGE, "w = 10")]
    for k, (wv, colour, lab) in enumerate(picks):
        y0 = 40 + k * 92
        m = Plot(46, y0, 150, 70, (0, 9), (20, 120))
        body.append(tint(30, y0 - 8, 190, 86, colour, op=0.08, r=10))
        body.append(line(m.x, m.y + m.h, m.x + m.w, m.y + m.h, stroke=LINE, w=1))
        body.append(line(m.x, m.y, m.x, m.y + m.h, stroke=LINE, w=1))
        body.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
                    'stroke-width="2.6" stroke-linecap="round"/>'
                    % (m.px(0), m.py(33.2), m.px(9), m.py(33.2 + 9 * wv), tv(colour)))
        for x, y in zip(HOURS, SCORE):
            body.append(circle(m.px(x), m.py(y), 2.8, fill=VIOLET, stroke="none", w=0))
        body.append(text(m.x + m.w + 10, m.y + 16, lab, 10, 800, anchor="start",
                         fill=tv(colour)))
    P = Plot(300, 44, 420, 230, (2, 11), (0, 500))
    body.append(P.axes(range(2, 12), range(0, 501, 100), "the weight w", "loss (MSE)"))
    body.append(grad("ai-lc-g", [(0, BLUE), (0.5, GREEN), (1, ORANGE)]))
    body.append('<path d="%s" fill="none" stroke="url(#ai-lc-g)" stroke-width="3.4"/>'
                % P.curve(_mse_b, 160))
    for wv, colour, lab in picks:
        x, y = P.pt(wv, _mse_b(wv))
        body.append(circle(x, y, 7, fill=colour, stroke=FILL, w=2))
        if wv == 6.5:
            body.append(text(x, P.py(100), "%s: loss %.0f" % (lab, _mse_b(wv)), 9.6, 750,
                             fill=tv(colour)))
            body.append(text(x, P.py(100) + 14, "the bottom of the bowl", 9.4, 700,
                             fill=MUTED))
            continue
        body.append(text(x + (12 if wv < 6 else -12), y - 10,
                         "%s: loss %.0f" % (lab, _mse_b(wv)), 9.6, 750,
                         anchor="start" if wv < 6 else "end", fill=tv(colour)))
    desc = ("On the left, three small plots of the revision data with three candidate "
            "lines, all with b equal to 33.2: w equal to 3 is far too shallow, w equal "
            "to 6.5 fits well, and w equal to 10 is far too steep. On the right, the "
            "mean squared error plotted against w is a U-shaped bowl. The three lines "
            "appear as points on it: w equal to 3 has loss %.0f, w equal to 6.5 has "
            "loss %.0f at the bottom of the bowl, and w equal to 10 has loss %.0f."
            % (_mse_b(3), _mse_b(6.5), _mse_b(10)))
    return figure("ai-lcur", 760, 330, "".join(body), "Loss as a function of a parameter",
                  desc, "Training is the search for the bottom of this bowl.")


# ============================================ Level 5: cross-entropy curve

@diagram("ai-cross-entropy")
def _cross_entropy():
    """−ln p: tiny when confident and right, huge when confident and wrong."""
    P = Plot(80, 44, 520, 220, (0, 1), (0, 5))
    body = [text(380, 22, "Cross-entropy: −ln(probability given to the right answer)",
                 12, 650, fill=MUTED)]
    body.append(P.axes([0, 0.2, 0.4, 0.6, 0.8, 1.0], range(0, 6),
                       "probability the model gave the correct answer", "loss"))
    pts = []
    for i in range(1, 161):
        p = 0.0068 + (1 - 0.0068) * i / 160.0
        pts.append((p, -math.log(p)))
    area = "M%.1f %.1f " % P.pt(pts[0][0], 0) + " ".join("L%.1f %.1f" % P.pt(*q) for q in pts) \
        + " L%.1f %.1f Z" % P.pt(1, 0)
    body.append(grad("ai-ce-g", [(0, RED), (0.5, AMBER), (1, GREEN)]))
    body.append('<path d="%s" fill="url(#ai-ce-g)" fill-opacity="0.18"/>' % area)
    body.append('<path d="M%s" fill="none" stroke="url(#ai-ce-g)" stroke-width="3.6"/>'
                % " L".join("%.1f %.1f" % P.pt(*q) for q in pts))
    notes = [(0.9, "confident and right", "loss 0.11", GREEN, -1),
             (0.5, "unsure", "loss 0.69", ORANGE, -1),
             (0.05, "confident and wrong", "loss 3.00", RED, 1)]
    for p, l1, l2, colour, side in notes:
        x, y = P.pt(p, -math.log(p))
        body.append(circle(x, y, 6, fill=colour, stroke=FILL, w=1.6))
        tx = x + (14 if side > 0 else 0)
        ty = y - 34 if side < 0 else y + 4
        body.append(text(tx, ty, l1, 9.6, 750, anchor="start" if side > 0 else "middle",
                         fill=tv(colour)))
        body.append(text(tx, ty + 14, l2, 9.4, 650, anchor="start" if side > 0 else "middle",
                         fill=INK))
    body.append(tint(620, 70, 122, 150, VIOLET, op=0.1, r=12))
    rows = [("0.99", "0.01"), ("0.9", "0.11"), ("0.5", "0.69"), ("0.1", "2.30"), ("0.01", "4.61")]
    body.append(text(640, 92, "p", 10, 800, anchor="start", fill=INK))
    body.append(text(722, 92, "loss", 10, 800, anchor="end", fill=INK))
    for i, (a, b) in enumerate(rows):
        body.append(text(640, 116 + i * 22, a, 10, 650, anchor="start", fill=INK, mono=True))
        body.append(text(722, 116 + i * 22, b, 10, 650, anchor="end", fill=INK, mono=True))
    desc = ("A graph of cross-entropy loss, minus the natural log of p, against p, the "
            "probability the model gave the correct answer. The curve is near zero at "
            "p equal to 1 and shoots upwards as p approaches 0. Marked points: "
            "confident and right, p equal to 0.9, loss 0.11; unsure, p equal to 0.5, "
            "loss 0.69; confident and wrong, p equal to 0.05, loss 3.00. A table "
            "lists p of 0.99, 0.9, 0.5, 0.1 and 0.01 with losses 0.01, 0.11, 0.69, "
            "2.30 and 4.61.")
    return figure("ai-ce", 760, 306, "".join(body), "The cross-entropy loss curve", desc,
                  "Halving an already small probability costs far more than halving a "
                  "large one.")


# ======================================== Level 5: a loss surface in 3D

def _bowl(w, b):
    u = (w - 0.6) * 0.92 + (b - 0.3) * 0.38
    v = -(w - 0.6) * 0.38 + (b - 0.3) * 0.92
    return u * u * 0.55 + v * v * 1.6


def _bowl_grad(w, b, h=1e-5):
    return ((_bowl(w + h, b) - _bowl(w - h, b)) / (2 * h),
            (_bowl(w, b + h) - _bowl(w, b - h)) / (2 * h))


@diagram("ai-loss-surface")
def _loss_surface():
    """A two-parameter loss surface with a descent path rolling to the bottom."""
    body = [text(380, 22, "Two parameters: the loss is a landscape, and training rolls "
                 "downhill", 12, 650, fill=MUTED)]
    svg, proj = surface(_bowl, (-2, 2), (-2, 2), 26, yaw=0.72, pitch=0.5, scale=150,
                        ox=300, oy=262, zscale=1.15, stroke_op=0.28)
    body.append(svg)
    # the descent path, computed
    w, b = -1.7, 1.75
    path_pts = [(w, b)]
    for _ in range(14):
        gw, gb = _bowl_grad(w, b)
        w, b = w - 0.26 * gw, b - 0.26 * gb
        path_pts.append((w, b))
    pp = [proj(a, c, _bowl(a, c) + 0.04) for a, c in path_pts]
    body.append(path("M" + " L".join("%.1f %.1f" % (p[0], p[1]) for p in pp),
                     stroke=WHITE, w=4.2))
    body.append(path("M" + " L".join("%.1f %.1f" % (p[0], p[1]) for p in pp),
                     stroke=CYAN, w=2.4))
    for i, p in enumerate(pp):
        body.append(circle(p[0], p[1], 5.5 if i == 0 else 3.4,
                           fill=AMBER if i == 0 else CYAN, stroke=DARK, w=1))
    mx, my, _ = proj(0.6, 0.3, 0)
    star = []
    for i in range(10):
        ang = -math.pi / 2 + i * math.pi / 5
        rad = 10 if i % 2 == 0 else 4.4
        star.append("%.1f,%.1f" % (mx + rad * math.cos(ang), my + rad * math.sin(ang)))
    body.append('<polygon points="%s" fill="%s" stroke="%s" stroke-width="1.2"/>'
                % (" ".join(star), LIME, DARK))
    sx, sy = pp[0][0], pp[0][1]
    body.append(_halo(sx + 12, sy - 10, "start: a random model", 9.6, 750, "start"))
    body.append(_halo(mx + 14, my + 22, "minimum: the best model", 9.6, 750, "start"))
    body.append(tint(588, 74, 156, 184, SLATE, op=0.07, r=12))
    for i in range(6):
        body.append('<rect x="604" y="%d" width="22" height="18" rx="3" fill="%s"/>'
                    % (92 + i * 22, plasma(1 - i / 5.0)))
    body.append(text(636, 104, "high loss", 9.6, 650, anchor="start", fill=INK))
    body.append(text(636, 214, "low loss", 9.6, 650, anchor="start", fill=INK))
    body.append(text(666, 236, "height = loss", 9.4, 650, fill=MUTED))
    body.append(text(666, 250, "floor = w and b", 9.4, 650, fill=MUTED))
    desc = ("A 3D surface shaped like a tilted oval bowl, coloured by height from "
            "yellow for high loss at the rim down through pink and purple to deep blue "
            "for low loss at the bottom. The floor axes are the weight w and the bias "
            "b. A path of cyan dots starts high on the rim at a random model and "
            "steps downhill, with long steps on the steep sides and shorter steps as "
            "the bowl flattens, ending at a green star at the bottom, the minimum: the "
            "best model.")
    return figure("ai-lsurf", 760, 340, "".join(body), "A loss landscape in 3D", desc,
                  "Every point on the floor is one model. Its height is how wrong it is.")


# ============================================ Level 5: slope and tangents

@diagram("ai-tangent")
def _tangent():
    """Tangents to (w − 3)² at w = 1, 3 and 5, with the downhill direction."""
    P = Plot(70, 40, 470, 230, (-0.5, 6.5), (0, 12))
    body = [text(380, 22, "The derivative is the slope of the tangent", 12, 650, fill=MUTED)]
    body.append(P.axes(range(0, 7), range(0, 13, 2), "w", "loss L(w) = (w − 3)²"))
    cid = "ai-tan-c"
    body.append(P.clip(cid))
    body.append('<path d="%s" fill="none" stroke="%s" stroke-width="3.2"/>'
                % (P.curve(lambda w: (w - 3) ** 2, 160), tv(VIOLET)))
    for wv, colour, word in ((1, BLUE, "slope −4: move right"),
                             (3, GREEN, "slope 0: the bottom"),
                             (5, PINK, "slope +4: move left")):
        slope = 2 * (wv - 3)
        y0 = (wv - 3) ** 2
        xa, xb = wv - 1.1, wv + 1.1
        body.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" '
                    'stroke-width="2.4" stroke-dasharray="6 4" clip-path="url(#%s)"/>'
                    % (P.px(xa), P.py(y0 + slope * (xa - wv)), P.px(xb),
                       P.py(y0 + slope * (xb - wv)), tv(colour), cid))
        x, y = P.pt(wv, y0)
        body.append(circle(x, y, 6.5, fill=colour, stroke=FILL, w=1.8))
        if slope:
            d = -1 if slope > 0 else 1
            body.append(arrow(x, y + 22, x + d * 46, y + 22, tv(colour), 2.4))
    body.append(tint(568, 56, 176, 196, SLATE, op=0.07, r=12))
    for i, (colour, a, b) in enumerate([(BLUE, "at w = 1", "slope −4: move right"),
                                        (GREEN, "at w = 3", "slope 0: the bottom"),
                                        (PINK, "at w = 5", "slope +4: move left")]):
        y = 84 + i * 58
        body.append(circle(586, y - 4, 6, fill=colour, stroke=FILL, w=1.4))
        body.append(text(600, y, a, 10, 800, anchor="start", fill=tv(colour)))
        body.append(text(600, y + 16, b, 9.6, 650, anchor="start", fill=INK))
    body.append(text(656, 244, "dL/dw = 2(w − 3)", 10, 750, fill=INK, mono=True))
    desc = ("A U-shaped curve, the loss L of w equals w minus 3 squared, for w from 0 "
            "to 6. Dashed tangent lines touch it at three points. At w equal to 1 the "
            "tangent slopes down with slope minus 4, and an arrow points right: move "
            "right to go downhill. At w equal to 3, the bottom, the tangent is flat, "
            "slope 0. At w equal to 5 it slopes up with slope plus 4, and an arrow "
            "points left. The derivative is dL by dw equals 2 times w minus 3.")
    return figure("ai-tan", 760, 300, "".join(body), "Slopes of the loss curve", desc,
                  "Move against the slope: that is the whole idea of gradient descent.")


# ========================================= Level 5: the gradient field

@diagram("ai-gradient-field")
def _gradient_field():
    """Contours of a bowl with arrows of the negative gradient pointing downhill."""
    P = Plot(60, 40, 300, 260, (-2, 2), (-2, 2))
    body = [text(380, 22, "A contour map of the loss, with arrows pointing downhill",
                 12, 650, fill=MUTED)]
    body.append('<rect x="%d" y="%d" width="%d" height="%d" rx="8" fill="%s" '
                'fill-opacity="0.6" stroke="%s"/>' % (P.x, P.y, P.w, P.h, FILL2, LINE))
    cid = "ai-gf-c"
    body.append(P.clip(cid))
    # contours of the bowl: ellipses in the rotated (u, v) frame
    levels = [0.1, 0.35, 0.8, 1.5, 2.5, 3.8, 5.4]
    for i, L in enumerate(levels):
        pts = []
        for k in range(73):
            t = 2 * math.pi * k / 72.0
            u, v = math.sqrt(L / 0.55) * math.cos(t), math.sqrt(L / 1.6) * math.sin(t)
            w = 0.6 + u * 0.92 - v * 0.38
            b = 0.3 + u * 0.38 + v * 0.92
            pts.append("%.1f %.1f" % P.pt(w, b))
        body.append('<path d="M%s Z" fill="none" stroke="%s" stroke-width="1.6" '
                    'clip-path="url(#%s)"/>' % (" L".join(pts), plasma(0.15 + 0.12 * i), cid))
    for i in range(7):
        for j in range(7):
            w = -1.8 + i * 0.6
            b = -1.8 + j * 0.6
            gw, gb = _bowl_grad(w, b)
            mag = math.hypot(gw, gb)
            if mag < 0.25:
                continue
            L = min(26, 6 + mag * 4.2)
            x, y = P.pt(w, b)
            ux, uy = -gw / mag, gb / mag     # screen y runs downwards
            body.append(arrow(x - ux * L / 2, y - uy * L / 2, x + ux * L / 2, y + uy * L / 2,
                              plasma(min(1, 0.3 + mag / 6.0)), 1.8))
    mx, my = P.pt(0.6, 0.3)
    body.append(circle(mx, my, 6, fill=LIME, stroke=DARK, w=1.2))
    # one point with both arrows
    w0, b0 = -1.2, 1.2
    gw, gb = _bowl_grad(w0, b0)
    m = math.hypot(gw, gb)
    x0, y0 = P.pt(w0, b0)
    body.append(arrow(x0, y0, x0 + gw / m * 46, y0 - gb / m * 46, tv(RED), 2.8))
    body.append(arrow(x0, y0, x0 - gw / m * 46, y0 + gb / m * 46, tv(GREEN), 2.8))
    body.append(circle(x0, y0, 6, fill=AMBER, stroke=DARK, w=1.2))
    body.append(text(P.px(0.6) + 10, P.py(0.3) + 18, "minimum", 9.4, 750, anchor="start",
                     fill=INK))
    body.append(text(P.x + P.w / 2, P.y + P.h + 18, "weight w", 9.6, 650, fill=MUTED))
    body.append(tint(388, 52, 352, 220, SLATE, op=0.06, r=12))
    lines = [("the gradient ∇L", "points uphill, steepest way up"),
             ("the negative gradient −∇L", "points downhill: the way to step"),
             ("small arrows", "−∇L across the map; longer where steeper"),
             ("rings", "contours: every point on a ring has equal loss")]
    marks = [arrow(404, 78, 430, 78, tv(RED), 2.6), arrow(404, 126, 430, 126, tv(GREEN), 2.6),
             arrow(404, 174, 430, 174, plasma(0.6), 1.8),
             '<ellipse cx="417" cy="222" rx="13" ry="7" fill="none" stroke="%s" '
             'stroke-width="1.8"/>' % plasma(0.3)]
    for i, (a, b) in enumerate(lines):
        y = 82 + i * 48
        body.append(marks[i])
        body.append(text(438, y, a, 10, 800, anchor="start", fill=INK))
        body.append(text(438, y + 15, b, 9.4, 600, anchor="start", fill=MUTED))
    cx, cy = P.x - 14, P.y + P.h / 2.0
    body.append('<text x="%.1f" y="%.1f" text-anchor="middle" font-size="9.6" '
                'font-weight="650" fill="%s" transform="rotate(-90 %.1f %.1f)">bias b</text>'
                % (cx, cy, MUTED, cx, cy))
    desc = ("A contour map of a bowl-shaped loss: nested tilted ovals around the "
            "minimum, marked with a green dot. A grid of small arrows shows the negative "
            "gradient at each point; they all point downhill towards the minimum and "
            "are longer where the slope is steeper. At one highlighted point two "
            "arrows leave in opposite directions: a red arrow, the gradient, pointing "
            "steepest uphill, and a green arrow, the negative gradient, pointing "
            "steepest downhill, which is the way gradient descent steps.")
    return figure("ai-gfield", 760, 322, "".join(body), "Gradients on a contour map", desc,
                  "The arrows always cross the contours at right angles: the steepest "
                  "way down.")


# ======================================= Level 5: descent, step by step

def _ball(x, y, r=9, colour=AMBER):
    return ('<g><circle cx="%.1f" cy="%.1f" r="%.1f" fill="%s" stroke="%s" stroke-width="1.6"/>'
            '<circle cx="%.1f" cy="%.1f" r="%.1f" fill="#FFFFFF" fill-opacity="0.65"/></g>'
            % (x, y, r, colour, DARK, x - r * 0.35, y - r * 0.35, r * 0.3))


@diagram("ai-descent-steps")
def _descent_steps():
    """A ball stepping down a loss curve, one gradient step at a time."""
    def L(w):
        return 0.5 * (w - 4) ** 2 + 1

    def dL(w):
        return w - 4
    lr = 0.4
    ws = [-2.0]
    for _ in range(8):
        ws.append(ws[-1] - lr * dL(ws[-1]))
    P = Plot(70, 40, 440, 250, (-3, 9), (0, 21))
    base = [text(380, 22, "Gradient descent: feel the slope, step downhill, repeat", 12,
                 650, fill=MUTED)]
    base.append(P.axes(range(-2, 10, 2), range(0, 22, 5), "parameter w", "loss"))
    base.append(grad("ai-ds-g", [(0, PINK), (0.5, VIOLET), (1, BLUE)]))
    base.append('<path d="%s" fill="none" stroke="url(#ai-ds-g)" stroke-width="3.4"/>'
                % P.curve(L, 160, -3, 9))
    base.append(tint(536, 50, 206, 236, SLATE, op=0.07, r=12))
    base.append(text(639, 74, "learning rate = %.1f" % lr, 10.5, 800, fill=INK))
    base.append(text(639, 92, "w ← w − 0.4 × slope", 10, 700, fill=MUTED, mono=True))
    stages, labels = [], []
    cid = "ai-ds-c"
    base.append(P.clip(cid))
    for k in range(len(ws)):
        w = ws[k]
        out = []
        for j in range(k):
            a, b2 = P.pt(ws[j], L(ws[j]))
            c, d = P.pt(ws[j + 1], L(ws[j + 1]))
            out.append(path("M%.1f %.1f L%.1f %.1f" % (a, b2 - 12, c, d - 12), stroke=tv(ORANGE),
                            w=1.6, dash="3 3"))
            out.append(circle(a, b2 - 9, 4, fill=AMBER, stroke="none", w=0))
        x, y = P.pt(w, L(w))
        s = dL(w)
        xa, xb = w - 1.6, w + 1.6
        out.append('<line x1="%.1f" y1="%.1f" x2="%.1f" y2="%.1f" stroke="%s" stroke-width="2" '
                   'stroke-dasharray="5 4" clip-path="url(#%s)"/>'
                   % (P.px(xa), P.py(L(w) + s * (xa - w)), P.px(xb), P.py(L(w) + s * (xb - w)),
                      tv(GREEN), cid))
        out.append(_ball(x, y - 10))
        if k < len(ws) - 1:
            nxt = ws[k + 1]
            out.append(arrow(x, y + 22, P.px(nxt), y + 22, tv(ORANGE), 2.4))
        lines = ["step %d" % k if k else "start",
                 "w = %.2f" % w, "loss = %.2f" % L(w), "slope = %.2f" % s,
                 ("step = −0.4 × %.2f = %+.2f" % (s, -lr * s)) if k < len(ws) - 1 else "almost no slope left"]
        for i, t in enumerate(lines):
            out.append(text(552, 132 + i * 26, t.replace("-", "−") if i else t,
                            12 if i == 0 else 10.2, 800 if i == 0 else 650,
                            anchor="start", fill=tv(ORANGE) if i == 0 else INK,
                            mono=i > 0))
        lab = ("Start at w = −2, high on the left: the slope is steep" if k == 0 else
               "Step %d: w = %.2f, loss %.2f, the steps shrink as the slope flattens" % (k, w, L(w)))
        stages.append(step(k + 1, "".join(out), lab))
        labels.append(lab)
    desc = ("A stepped animation of gradient descent on a U-shaped loss curve with its "
            "minimum at w equal to 4. A ball starts at w equal to minus 2, high on the "
            "left, where the slope is steep. At each step a dashed green tangent shows "
            "the slope and an orange arrow shows the step, minus 0.4 times the slope. "
            "The ball moves to w = %s, and the steps shrink as the slope flattens, "
            "until it rests almost at the bottom." % ", ".join("%.2f" % w for w in ws[1:]))
    return figure_steps("ai-dsteps", 760, 320, "".join(base), stages,
                        "Gradient descent step by step", desc,
                        "Big steps where it is steep, small steps near the bottom, "
                        "with no extra rule needed.", labels=labels)


# ====================================== Level 5: three learning rates

@diagram("ai-learning-rates")
def _learning_rates():
    """Too small, about right and too big, on the same bowl."""
    def L(w):
        return (w - 3) ** 2
    body = [text(380, 22, "Same bowl, three learning rates, eight steps each", 12, 650,
                 fill=MUTED)]
    cases = [("Too small, 0.05", "creeping: far from the bottom after 8 steps", 0.05, 0.0, BLUE),
             ("About right, 0.35", "there in a few steps", 0.35, 0.0, GREEN),
             ("Too big, 1.05", "overshoots further every step", 1.05, 2.2, RED)]
    for k, (title, sub, lr, w0, colour) in enumerate(cases):
        x0 = 20 + k * 246
        body.append(tint(x0, 38, 232, 236, colour, op=0.07, r=12))
        body.append(text(x0 + 116, 60, title, 11.5, 800, fill=tv(colour)))
        body.append(text(x0 + 116, 76, sub, 9, 600, fill=MUTED))
        P = Plot(x0 + 16, 92, 200, 160, (-0.6, 6.6), (0, 13))
        cid = "ai-lr-c%d" % k
        body.append(P.clip(cid))
        body.append(line(P.x, P.y + P.h, P.x + P.w, P.y + P.h, stroke=LINE, w=1.2))
        body.append('<path d="%s" fill="none" stroke="%s" stroke-width="2.6" '
                    'clip-path="url(#%s)"/>' % (P.curve(L, 120), tv(VIOLET), cid))
        ws = [w0]
        for _ in range(8):
            ws.append(ws[-1] - lr * 2 * (ws[-1] - 3))
        shown = [w for w in ws if -0.6 <= w <= 6.6][:9]
        for a, b in zip(shown, shown[1:]):
            body.append(arrow(P.px(a), P.py(L(a)), P.px(b), P.py(L(b)), tv(ORANGE), 1.8))
        for i, w in enumerate(shown):
            body.append(circle(P.px(w), P.py(L(w)), 4.5 if i else 6,
                               fill=AMBER if i == 0 else ORANGE, stroke=FILL, w=1.2))
        body.append(text(x0 + 116, 268, "after 8 steps: loss %.2f" % L(ws[8]) if L(ws[8]) < 100
                         else "after 8 steps: loss %.0f and rising" % L(ws[8]), 9.4, 750, fill=INK))
    desc = ("Three panels show the same U-shaped loss curve, with the minimum at w equal "
            "to 3, and the path of eight gradient descent steps. With a learning rate "
            "that is too small, 0.05, the steps creep down from w equal to 0 and are "
            "still far from the bottom after 8 steps. With a learning rate of about "
            "0.35, the path reaches the bottom in a few steps. With a learning rate "
            "that is too big, 1.05, starting near the bottom at w equal to 2.2, each "
            "step jumps across the valley and lands higher up the other side, so the "
            "loss grows.")
    return figure("ai-lrs", 760, 286, "".join(body), "The effect of the learning rate", desc,
                  "The right learning rate is found by experiment, watching the loss.")


# ========================================= Level 5: training curves

@diagram("ai-training-curves")
def _training_curves():
    """Training and validation loss, the best epoch, and overfitting after it."""
    def tr(e):
        return 0.08 + 2.2 * math.exp(-e / 9.0)

    def va(e):
        return 0.34 + 2.0 * math.exp(-e / 8.0) + 0.0042 * max(0, e - 20) ** 1.5
    best = min(range(61), key=va)
    P = Plot(80, 44, 470, 230, (0, 60), (0, 2.5))
    body = [text(380, 22, "Watch both curves: stop where validation loss is lowest", 12,
                 650, fill=MUTED)]
    body.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" fill="%s" '
                'fill-opacity="0.08"/>' % (P.px(best), P.y, P.px(60) - P.px(best), P.h, RED))
    body.append(P.axes(range(0, 61, 10), [0, 0.5, 1.0, 1.5, 2.0, 2.5], "epoch", "loss"))
    body.append('<path d="%s" fill="none" stroke="%s" stroke-width="3.2"/>'
                % (P.curve(tr, 120), tv(BLUE)))
    body.append('<path d="%s" fill="none" stroke="%s" stroke-width="3.2"/>'
                % (P.curve(va, 120), tv(ORANGE)))
    bx, by = P.pt(best, va(best))
    body.append(line(bx, P.y, bx, P.y + P.h, stroke=tv(GREEN), w=2, dash="6 4"))
    body.append(circle(bx, by, 7, fill=GREEN, stroke=FILL, w=2))
    body.append(text(bx + 8, P.y + 16, "early stopping: keep the", 9.6, 750, anchor="start",
                     fill=tv(GREEN)))
    body.append(text(bx + 8, P.y + 30, "weights from epoch %d" % best, 9.6, 750,
                     anchor="start", fill=tv(GREEN)))
    body.append(text(P.px(46), P.py(va(46)) - 24, "overfitting", 10, 800, fill=tv(RED)))
    body.append(text(P.px(47), P.py(tr(47)) - 10, "training loss keeps falling", 9.4, 700,
                     fill=tv(BLUE)))
    body.append(tint(576, 60, 166, 138, SLATE, op=0.07, r=12))
    body.append(line(592, 86, 620, 86, stroke=tv(BLUE), w=3.2))
    body.append(text(628, 90, "training loss", 10, 700, anchor="start", fill=INK))
    body.append(line(592, 112, 620, 112, stroke=tv(ORANGE), w=3.2))
    body.append(text(628, 116, "validation loss", 10, 700, anchor="start", fill=INK))
    body.append(text(592, 146, "Gap growing after the", 9.4, 600, anchor="start", fill=MUTED))
    body.append(text(592, 160, "green line: the model is", 9.4, 600, anchor="start", fill=MUTED))
    body.append(text(592, 174, "memorising, not learning.", 9.4, 600, anchor="start", fill=MUTED))
    desc = ("Two loss curves over 60 epochs. The training loss, in blue, falls steeply "
            "and keeps falling slowly all the way to epoch 60. The validation loss, in "
            "orange, falls at first, reaches its lowest point at epoch %d, marked with "
            "a green dashed line labelled early stopping: keep the weights from epoch "
            "%d, and then rises again. The region after that line is shaded and "
            "labelled overfitting: the gap between the curves grows because the model "
            "is memorising the training data." % (best, best))
    return figure("ai-tcurves", 760, 306, "".join(body), "Training and validation loss curves",
                  desc, "The validation curve, not the training curve, tells you when to stop.")


# =================================== Level 5: a landscape with traps, in 3D

def _hills(x, y):
    return (1.55 - 1.25 * math.exp(-((x - 1.0) ** 2 + (y - 0.7) ** 2) / 0.55)
            - 0.75 * math.exp(-((x + 1.05) ** 2 + (y + 0.85) ** 2) / 0.42)
            + 0.38 * math.exp(-((x + 0.9) ** 2 + (y - 1.15) ** 2) / 0.3)
            + 0.06 * (x * x + y * y))


def _hills_grad(x, y, h=1e-5):
    return ((_hills(x + h, y) - _hills(x - h, y)) / (2 * h),
            (_hills(x, y + h) - _hills(x, y - h)) / (2 * h))


@diagram("ai-landscape-3d")
def _landscape():
    """A bumpy loss surface: two balls, two starts, two different valleys."""
    body = [text(380, 22, "A real loss landscape is bumpy: where you start decides where "
                 "you end", 12, 650, fill=MUTED)]
    svg, proj = surface(_hills, (-2.2, 2.2), (-2.2, 2.2), 30, yaw=0.62, pitch=0.62,
                        scale=132, ox=318, oy=246, zscale=1.0, stroke_op=0.22)
    body.append(svg)
    runs = [((-1.9, 0.1), PINK), ((1.9, -1.5), CYAN)]
    ends = []
    for (x, y), colour in runs:
        pts = [(x, y)]
        for _ in range(60):
            gx, gy = _hills_grad(x, y)
            x, y = x - 0.18 * gx, y - 0.18 * gy
            pts.append((x, y))
        pp = [proj(a, b, _hills(a, b) + 0.03) for a, b in pts]
        d = "M" + " L".join("%.1f %.1f" % (p[0], p[1]) for p in pp)
        body.append(path(d, stroke=WHITE, w=4.4))
        body.append(path(d, stroke=colour, w=2.6))
        body.append(_ball(pp[0][0], pp[0][1] - 6, 7, colour))
        body.append(_ball(pp[-1][0], pp[-1][1] - 6, 8, colour))
        ends.append((pts[-1], pp[-1]))
    (g_xy, g_p), (l_xy, l_p) = sorted(ends, key=lambda e: _hills(*e[0]))
    sp = proj(0.0, -0.05, _hills(0.0, -0.05))
    hp = proj(-0.9, 1.15, _hills(-0.9, 1.15))
    notes = [(g_p, "global minimum", "the deepest valley", 16, 22, "start"),
             (l_p, "local minimum", "a shallower dip: a trap", 16, 26, "start"),
             (sp, "saddle", "between the valleys", 0, -16, "middle"),
             (hp, "hill", "high loss", -12, -14, "end")]
    for (px, py, _d), a, b2, dx, dy, anchor in notes:
        body.append(circle(px, py, 3.2, fill=DARK, stroke=WHITE, w=1))
        body.append(_halo(px + dx, py + dy, a, 10, 800, anchor))
        body.append(_halo(px + dx, py + dy + 13, b2, 9, 650, anchor))
    desc = ("A colourful 3D loss surface with two valleys of different depths, a saddle "
            "between them and a hill. Two balls, one pink and one cyan, start on "
            "opposite sides and roll downhill by gradient descent, leaving trails. "
            "They end in different valleys: one in the deepest valley, the global "
            "minimum, and one in a shallower dip, a local minimum, where it is stuck "
            "because every direction from there is uphill.")
    return figure("ai-l3d", 760, 330, "".join(body), "A bumpy loss landscape in 3D", desc,
                  "Gradient descent finds a low point near where it starts, not "
                  "necessarily the lowest.")


# ============================================ Level 5: momentum vs plain

@diagram("ai-momentum")
def _momentum():
    """A narrow ravine: plain descent zigzags, momentum glides."""
    def f(x, y):
        return x * x + 20 * y * y

    def run(beta, steps=24, lr=0.045):
        x, y, vx, vy = -9.0, 1.0, 0.0, 0.0
        pts = [(x, y)]
        for _ in range(steps):
            vx = beta * vx + 2 * x
            vy = beta * vy + 40 * y
            x, y = x - lr * vx, y - lr * vy
            pts.append((x, y))
        return pts
    P = Plot(40, 56, 680, 196, (-10, 1.5), (-1.25, 1.25))
    body = [text(380, 22, "A narrow ravine: same learning rate, with and without momentum",
                 12, 650, fill=MUTED)]
    body.append('<rect x="%d" y="%d" width="%d" height="%d" rx="10" fill="%s" '
                'fill-opacity="0.55" stroke="%s"/>' % (P.x, P.y, P.w, P.h, FILL2, LINE))
    cid = "ai-mo-c"
    body.append(P.clip(cid))
    for i, L in enumerate([1, 4, 12, 25, 45, 70, 100]):
        pts = []
        for k in range(97):
            t = 2 * math.pi * k / 96.0
            pts.append("%.1f %.1f" % P.pt(math.sqrt(L) * math.cos(t),
                                          math.sqrt(L / 20.0) * math.sin(t)))
        body.append('<path d="M%s Z" fill="none" stroke="%s" stroke-width="1.4" '
                    'clip-path="url(#%s)"/>' % (" L".join(pts), plasma(0.12 + 0.1 * i), cid))
    for beta, colour, lab in ((0.0, RED, "plain gradient descent"),
                              (0.5, GREEN, "with momentum 0.5")):
        pts = run(beta)
        d = "M" + " L".join("%.1f %.1f" % P.pt(*p) for p in pts)
        body.append('<path d="%s" fill="none" stroke="%s" stroke-width="2.4" '
                    'clip-path="url(#%s)"/>' % (d, tv(colour), cid))
        for p in pts:
            x, y = P.pt(*p)
            if P.x <= x <= P.x + P.w:
                body.append(circle(x, y, 2.8, fill=colour, stroke="none", w=0))
    mx, my = P.pt(0, 0)
    body.append(circle(mx, my, 6, fill=LIME, stroke=DARK, w=1.2))
    body.append(text(mx - 8, my - 12, "minimum", 9.4, 750, anchor="end", fill=INK))
    sx, sy = P.pt(-9, 1)
    body.append(_ball(sx, sy, 7))
    body.append(text(sx + 10, sy - 8, "start", 9.4, 750, anchor="start", fill=INK))
    pf = run(0.0)[-1]
    mf = run(0.5)[-1]
    body.append(line(60, 280, 88, 280, stroke=tv(RED), w=3))
    body.append(text(96, 284, "plain: after 24 steps, loss %.2f, still zigzagging"
                     % f(*pf), 10, 700, anchor="start", fill=INK))
    body.append(line(420, 280, 448, 280, stroke=tv(GREEN), w=3))
    body.append(text(456, 284, "momentum: loss %.4f" % f(*mf), 10, 700, anchor="start",
                     fill=INK))
    desc = ("A contour map of a long, narrow valley with its minimum on the right. Both "
            "paths start at the far left. Plain gradient descent, in red, zigzags from "
            "wall to wall across the narrow direction while creeping slowly along the "
            "valley, and after 24 steps its loss is still %.2f. With momentum 0.5 and "
            "the same learning rate, the green path's zigzags die away quickly and it "
            "moves steadily along the valley floor, reaching a loss of %.4f."
            % (f(*pf), f(*mf)))
    return figure("ai-mom", 760, 300, "".join(body), "Momentum in a ravine", desc,
                  "The velocity averages the gradients: back-and-forth parts cancel, "
                  "the consistent part adds up.")
