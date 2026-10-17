"""Resource material for the practice papers.

A teaching diagram explains; a resource figure only presents. These carry the
data a question is asked about and nothing else: no labelled answer, no
caption that gives the reasoning away, and a text alternative that describes
what is printed rather than what it means. That distinction matters, because a
blind candidate reading the alt text must be answering the same question as a
sighted one, not an easier one.

Named `exam-*` and registered in the shared diagram registry, so a paper
embeds one with `!diagram exam-<name>` in a question's `figure`.
"""
import math

from .diagrams import (diagram, TEAL, TEAL_SOFT, LILAC, LILAC_SOFT, WARN,
                       WARN_SOFT, FILL, LINE, MUTED)
from .svg import figure, box, text, line, path, circle

FILL2 = "var(--dg-fill-2)"


def _rng(seed):
    state = [seed]

    def nxt():
        state[0] = (state[0] * 1103515245 + 12345) % 2147483648
        return state[0] / 2147483648.0
    return nxt


def _axes(x0, y0, w, h, xlab="", ylab="", xticks=(), yticks=()):
    out = [line(x0, y0, x0 + w, y0, stroke=LINE, w=1.6),
           line(x0, y0, x0, y0 - h, stroke=LINE, w=1.6)]
    if xlab:
        out.append(text(x0 + w / 2, y0 + 38, xlab, 10.5, 600, fill=MUTED))
    if ylab:
        out.append('<text x="%d" y="%d" text-anchor="middle" font-size="10.5" '
                   'font-weight="600" fill="%s" transform="rotate(-90 %d %d)">'
                   '%s</text>' % (x0 - 42, y0 - h / 2, MUTED, x0 - 42,
                                  y0 - h / 2, ylab))
    for frac, lab in xticks:
        x = x0 + w * frac
        out.append(line(x, y0, x, y0 + 5, stroke=LINE, w=1.2))
        out.append(text(x, y0 + 19, lab, 9.5, 500, fill=MUTED))
    for frac, lab in yticks:
        y = y0 - h * frac
        out.append(line(x0 - 5, y, x0, y, stroke=LINE, w=1.2))
        out.append(text(x0 - 10, y + 4, lab, 9.5, 500, anchor="end", fill=MUTED))
        if frac:
            out.append(line(x0, y, x0 + w, y, stroke=LINE, w=0.7, dash="2 5"))
    return "".join(out)


def _table(x, y, cols, rows, head_tone=TEAL, head_soft=TEAL_SOFT, rh=26):
    """A plain data table. cols is a list of (width, header)."""
    out = []
    cx = x
    for w, label in cols:
        out.append(box(cx, y, w, rh, None, fill=head_soft, stroke=head_tone,
                       r=4))
        out.append(text(cx + w / 2, y + rh / 2 + 4, label, 9.8, 700,
                        fill=head_tone))
        cx += w
    for r, row in enumerate(rows):
        cx = x
        ry = y + rh + r * rh
        for (w, _), val in zip(cols, row):
            out.append(box(cx, ry, w, rh, None,
                           fill=FILL if r % 2 else FILL2, stroke=LINE, r=4))
            out.append(text(cx + w / 2, ry + rh / 2 + 4, str(val), 9.6, 450,
                            fill="var(--dg-text)"))
            cx += w
    return "".join(out)


# ============================================================ data quality

def _dirty(name, title, cols, rows, desc_rows, width=700):
    x = (760 - width) / 2
    body = [text(380, 24, title, 11.5, 700, fill=MUTED),
            _table(x, 40, cols, rows)]
    h = 40 + (len(rows) + 1) * 26 + 20
    desc = ("A short data extract printed as a table with the columns %s. The "
            "rows are: %s." % (", ".join(c[1] for c in cols), desc_rows))
    return figure(name, 760, h, "".join(body),
                  "Data extract: " + title.lower(), desc)


@diagram("exam-extract-members")
def _ex_members():
    return _dirty(
        "ex-mem", "Extract from the membership file",
        [(60, "id"), (150, "name"), (140, "joined"), (130, "postcode"),
         (110, "fee paid"), (110, "email")],
        [("1", "R. Nkemdirim", "07/08/2025", "NE1 4ST", "45.00", "r.n@ex.org"),
         ("2", "r. nkemdirim", "2025-08-07", "ne1 4st", "45", "R.N@ex.org"),
         ("3", "H. Baptiste", "11/9/25", "NE2 1QQ", "", "h.b@ex.org"),
         ("4", "T. Olawale", "02/02/2026", "NE4 8PP", "4500.00", ""),
         ("5", "", "19/11/2025", "NE1 4ST", "45.00", "not supplied"),
         ("6", "S. Mihai", "19/11/2025", "N E 3 2 R L", "45.00", "s.mihai@ex")],
        "row 1, id 1, R. Nkemdirim, joined 07/08/2025, postcode NE1 4ST, fee "
        "paid 45.00, email r.n@ex.org; row 2, id 2, lower case r. nkemdirim, joined 2025-08-07, postcode in lower case ne1 "
        "4st, fee paid 45, email R.N@ex.org; row 3, id 3, H. Baptiste, joined "
        "11/9/25, postcode NE2 1QQ, fee paid blank, email h.b@ex.org; row 4, "
        "id 4, T. Olawale, joined 02/02/2026, postcode NE4 8PP, fee paid "
        "4500.00, email blank; row 5, id 5, name blank, joined 19/11/2025, "
        "postcode NE1 4ST, fee paid 45.00, email given as the words not "
        "supplied; row 6, id 6, S. Mihai, joined 19/11/2025, postcode written "
        "with spaces as N E 3 2 R L, fee paid 45.00, email s.mihai@ex")


@diagram("exam-extract-sensors")
def _ex_sensors():
    return _dirty(
        "ex-sen", "Extract from the sensor log",
        [(140, "timestamp"), (110, "sensor"), (120, "temp °C"),
         (120, "humidity %"), (110, "status")],
        [("08:00:00", "T-01", "18.4", "41", "ok"),
         ("08:00:01", "T-02", "18.9", "43", "ok"),
         ("08:00:02", "T-01", "-999", "41", "ok"),
         ("08:00:03", "T-03", "19.1", "410", "ok"),
         ("08:00:04", "T-02", "18.9", "43", "OK"),
         ("08:00:04", "T-02", "18.9", "43", "ok"),
         ("08:00:06", "T-04", "", "", "offline")],
        "08:00:00 sensor T-01 temperature 18.4 humidity 41 status ok; "
        "08:00:01 sensor T-02 temperature 18.9 humidity 43 status ok; "
        "08:00:02 sensor T-01 temperature minus 999 humidity 41 status ok; "
        "08:00:03 sensor T-03 temperature 19.1 humidity 410 status ok; "
        "08:00:04 sensor T-02 temperature 18.9 humidity 43 status OK in "
        "capitals; 08:00:04 sensor T-02 temperature 18.9 humidity 43 status "
        "ok, an identical reading at the same timestamp; 08:00:06 sensor T-04 "
        "temperature blank humidity blank status offline. The timestamp "
        "08:00:05 does not appear",
        width=600)


@diagram("exam-extract-orders")
def _ex_orders():
    return _dirty(
        "ex-ord", "Extract from the orders export",
        [(90, "order"), (120, "date"), (110, "country"), (110, "total"),
         (130, "payment"), (130, "customer")],
        [("A1001", "01/03/2026", "UK", "£42.50", "Card", "C-204"),
         ("A1002", "01/03/2026", "U.K.", "42.50", "card", "C-204"),
         ("A1003", "03/01/2026", "United Kingdom", "£0.00", "Card",
          "C-311"),
         ("A1004", "02/03/2026", "GB", "£118.00", "PayPal", ""),
         ("A1005", "02/03/2026", "uk", "£ 71.20", "Card", "C-118"),
         ("A1001", "01/03/2026", "UK", "£42.50", "Card", "C-204")],
        "A1001 dated 01/03/2026, country UK, total 42 pounds 50, payment "
        "Card, customer C-204; A1002 dated 01/03/2026, country U.K., total "
        "42.50 with no currency symbol, payment card in lower case, customer "
        "C-204; A1003 dated 03/01/2026, country United Kingdom, total 0 "
        "pounds, payment Card, customer C-311; A1004 dated 02/03/2026, "
        "country GB, total 118 pounds, payment PayPal, customer blank; A1005 "
        "dated 02/03/2026, country uk in lower case, total written with a "
        "space as 71.20, payment Card, customer C-118; and A1001 appears "
        "again, identical to the first row")


# =============================================================== charts

@diagram("exam-chart-monthly")
def _ex_monthly():
    """A bar chart of monthly figures, to be read and described."""
    VALS = [("Apr", 182), ("May", 196), ("Jun", 241), ("Jul", 288),
            ("Aug", 302), ("Sep", 214), ("Oct", 203), ("Nov", 259),
            ("Dec", 418), ("Jan", 142), ("Feb", 151), ("Mar", 177)]
    X0, Y0, W, H = 86, 290, 600, 220
    peak = 440
    bw = W / float(len(VALS))
    body = [text(380, 24, "Online orders per month, thousands", 11.5, 700,
                 fill=MUTED)]
    body.append(_axes(X0, Y0, W, H, "month", "orders (000s)",
                      xticks=[((i + 0.5) / len(VALS), m)
                              for i, (m, _) in enumerate(VALS)],
                      yticks=[(v / float(peak), str(v))
                              for v in (0, 100, 200, 300, 400)]))
    for i, (m, v) in enumerate(VALS):
        h = H * v / float(peak)
        body.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="2" '
                    'fill="%s" stroke="%s" stroke-width="1"/>'
                    % (X0 + i * bw + 4, Y0 - h, bw - 8, h, TEAL_SOFT, TEAL))
        body.append(text(X0 + i * bw + bw / 2, Y0 - h - 6, str(v), 8.6, 600,
                         fill=MUTED))
    desc = ("A bar chart of online orders per month in thousands, from April "
            "through to the following March. The values are: April 182, May "
            "196, June 241, July 288, August 302, September 214, October 203, "
            "November 259, December 418, January 142, February 151, March "
            "177.")
    return figure("ex-month", 760, 338, "".join(body),
                  "Bar chart of online orders per month", desc)


@diagram("exam-chart-response")
def _ex_response():
    """Two lines over time, to be compared."""
    A = [42, 44, 41, 46, 52, 61, 74, 96, 128, 151, 162, 168]
    B = [40, 41, 40, 42, 43, 44, 46, 47, 49, 50, 51, 52]
    X0, Y0, W, H = 92, 282, 592, 214
    peak = 180
    body = [text(380, 24, "Mean page response time, milliseconds, by hour",
                 11.5, 700, fill=MUTED)]
    body.append(_axes(X0, Y0, W, H, "hour of the day", "response (ms)",
                      xticks=[(i / 11.0, str(8 + i)) for i in range(0, 12, 2)],
                      yticks=[(v / float(peak), str(v))
                              for v in (0, 50, 100, 150)]))
    for vals, tone, label in ((A, WARN, "server A"), (B, TEAL, "server B")):
        d = " ".join(("M" if i == 0 else "L")
                     + "%.1f %.1f" % (X0 + W * i / 11.0,
                                      Y0 - H * v / float(peak))
                     for i, v in enumerate(vals))
        body.append(path(d, stroke=tone, w=2.6))
        for i, v in enumerate(vals):
            body.append(circle(X0 + W * i / 11.0, Y0 - H * v / float(peak), 3.2,
                               fill=tone, stroke=tone, w=0))
        body.append(text(X0 + W + 8, Y0 - H * vals[-1] / float(peak) + 4,
                         label, 9.6, 650, anchor="start", fill=tone))
    desc = ("A line chart of mean page response time in milliseconds against "
            "hour of the day from 8 to 19, with two series. Server A reads 42, "
            "44, 41, 46, 52, 61, 74, 96, 128, 151, 162 and 168 milliseconds "
            "across those hours. Server B reads 40, 41, 40, 42, 43, 44, 46, "
            "47, 49, 50, 51 and 52 milliseconds across the same hours.")
    return figure("ex-resp", 760, 330, "".join(body),
                  "Line chart of response time for two servers", desc)


@diagram("exam-chart-growth")
def _ex_growth():
    """Data volume over five years, with a linear and an actual series."""
    YEARS = ["2021", "2022", "2023", "2024", "2025", "2026"]
    VALS = [12, 19, 34, 68, 141, 310]
    X0, Y0, W, H = 96, 272, 580, 200
    peak = 340
    body = [text(380, 24, "Data held by one organisation, terabytes", 11.5,
                 700, fill=MUTED)]
    body.append(_axes(X0, Y0, W, H, "year", "terabytes held",
                      xticks=[(i / 5.0, y) for i, y in enumerate(YEARS)],
                      yticks=[(v / float(peak), str(v))
                              for v in (0, 100, 200, 300)]))
    d = " ".join(("M" if i == 0 else "L")
                 + "%.1f %.1f" % (X0 + W * i / 5.0, Y0 - H * v / float(peak))
                 for i, v in enumerate(VALS))
    body.append(path(d, stroke=TEAL, w=2.8))
    for i, v in enumerate(VALS):
        body.append(circle(X0 + W * i / 5.0, Y0 - H * v / float(peak), 4.4,
                           fill=TEAL_SOFT, stroke=TEAL))
        body.append(text(X0 + W * i / 5.0, Y0 - H * v / float(peak) - 12,
                         str(v), 9.4, 650, fill=TEAL))
    desc = ("A line chart of the total data held by one organisation in "
            "terabytes, by year. 2021: 12 terabytes. 2022: 19. 2023: 34. "
            "2024: 68. 2025: 141. 2026: 310.")
    return figure("ex-grow", 760, 320, "".join(body),
                  "Line chart of data volume held, by year", desc)


@diagram("exam-scatter-describe")
def _ex_scatter():
    """A scatter with a clear negative relationship and one odd point."""
    X0, Y0, W, H = 112, 276, 540, 208
    body = [text(380, 24, "Price against units sold, one product, 30 weeks",
                 11.5, 700, fill=MUTED)]
    body.append(_axes(X0, Y0, W, H, "price (£)", "units sold per week",
                      xticks=[(f, str(v)) for f, v in
                              ((0, "0"), (0.25, "5"), (0.5, "10"),
                               (0.75, "15"), (1.0, "20"))],
                      yticks=[(f, str(v)) for f, v in
                              ((0, "0"), (0.25, "50"), (0.5, "100"),
                               (0.75, "150"), (1.0, "200"))]))
    nxt = _rng(97)
    for _ in range(29):
        x = 0.12 + 0.8 * nxt()
        y = 0.9 - 0.72 * x + (nxt() - 0.5) * 0.18
        body.append(circle(X0 + W * x, Y0 - H * min(max(y, 0.03), 0.97), 4.4,
                           fill=TEAL_SOFT, stroke=TEAL))
    body.append(circle(X0 + W * 0.78, Y0 - H * 0.88, 4.4, fill=TEAL_SOFT,
                       stroke=TEAL))
    desc = ("A scatter plot of weekly units sold against price in pounds for "
            "one product over thirty weeks. Price runs from 0 to 20 pounds "
            "along the horizontal axis and units sold from 0 to 200 up the "
            "vertical axis. Twenty nine of the points form a band running from "
            "the upper left to the lower right: at low prices the weekly sales "
            "are high, around 150 to 190 units, and at high prices they are "
            "low, around 20 to 50 units. One further point sits apart from "
            "that band, at a price of about 16 pounds with sales of about 176 "
            "units.")
    return figure("ex-scat", 760, 326, "".join(body),
                  "Scatter plot of units sold against price", desc)


@diagram("exam-cluster-plot")
def _ex_clusters():
    """Three visible groups, unlabelled, for a technique-naming question."""
    X0, Y0, W, H = 108, 274, 544, 208
    body = [text(380, 24, "Customers plotted by average basket value and "
                 "visits per month", 11.5, 700, fill=MUTED)]
    body.append(_axes(X0, Y0, W, H, "visits per month", "average basket (£)",
                      xticks=[(f, str(v)) for f, v in
                              ((0, "0"), (0.33, "5"), (0.66, "10"),
                               (1.0, "15"))],
                      yticks=[(f, str(v)) for f, v in
                              ((0, "0"), (0.33, "40"), (0.66, "80"),
                               (1.0, "120"))]))
    CENTRES = [(0.18, 0.22, 24, 3), (0.72, 0.34, 22, 11), (0.4, 0.82, 18, 29)]
    for cx, cy, n, seed in CENTRES:
        nxt = _rng(seed)
        for _ in range(n):
            x = cx + (nxt() - 0.5) * 0.2
            y = cy + (nxt() - 0.5) * 0.2
            body.append(circle(X0 + W * min(max(x, 0.02), 0.98),
                               Y0 - H * min(max(y, 0.03), 0.97), 4.2,
                               fill=LILAC_SOFT, stroke=LILAC))
    desc = ("A scatter plot of customers, with visits per month from 0 to 15 "
            "along the horizontal axis and average basket value from 0 to 120 "
            "pounds up the vertical axis. The points fall into three separate "
            "groups with clear space between them: one group of about 24 "
            "customers with few visits and a low basket value, one group of "
            "about 22 customers with many visits and a low to moderate basket "
            "value, and one group of about 18 customers with a moderate number "
            "of visits and a high basket value. No group is labelled.")
    return figure("ex-clus", 760, 326, "".join(body),
                  "Scatter plot of customers by visits and basket value", desc)


@diagram("exam-training-curves")
def _ex_curves():
    """Training and validation error against epochs."""
    X0, Y0, W, H = 100, 268, 560, 196
    TR = [0.62, 0.44, 0.33, 0.26, 0.21, 0.17, 0.14, 0.11, 0.09, 0.07, 0.05,
          0.04]
    VA = [0.64, 0.48, 0.38, 0.32, 0.29, 0.28, 0.29, 0.32, 0.36, 0.41, 0.47,
          0.53]
    body = [text(380, 24, "Error against training epoch, one model", 11.5, 700,
                 fill=MUTED)]
    body.append(_axes(X0, Y0, W, H, "training epoch", "error",
                      xticks=[(i / 11.0, str(i + 1)) for i in range(0, 12, 2)],
                      yticks=[(f, "%.1f" % (f * 0.7))
                              for f in (0, 0.286, 0.571, 0.857)]))
    for vals, tone, label in ((TR, TEAL, "training set"),
                              (VA, WARN, "validation set")):
        d = " ".join(("M" if i == 0 else "L")
                     + "%.1f %.1f" % (X0 + W * i / 11.0, Y0 - H * v / 0.7)
                     for i, v in enumerate(vals))
        body.append(path(d, stroke=tone, w=2.6))
        body.append(text(X0 + W + 8, Y0 - H * vals[-1] / 0.7 + 4, label, 9.4,
                         650, anchor="start", fill=tone))
    desc = ("A line chart of error against training epoch for one model, with "
            "two series over twelve epochs. The training set error falls "
            "steadily throughout: 0.62, 0.44, 0.33, 0.26, 0.21, 0.17, 0.14, "
            "0.11, 0.09, 0.07, 0.05, 0.04. The validation set error falls at "
            "first and then rises: 0.64, 0.48, 0.38, 0.32, 0.29, 0.28, 0.29, "
            "0.32, 0.36, 0.41, 0.47, 0.53.")
    return figure("ex-curv", 760, 318, "".join(body),
                  "Training and validation error against epoch", desc)


# ================================================= confusion matrices

def _conf(name, title, tp, fp, fn, tn, pos, neg, desc_tail):
    """A confusion matrix with the counts and nothing worked out."""
    CX, CY, CW, CH = 236, 86, 210, 78
    body = [text(380, 24, title, 11.5, 700, fill=MUTED),
            text(CX + CW / 2, 72, "PREDICTED " + pos.upper(), 9.6, 700,
                 fill=MUTED),
            text(CX + CW * 1.5, 72, "PREDICTED " + neg.upper(), 9.6, 700,
                 fill=MUTED)]
    # Horizontal, to the left. Rotated row labels collide with each other
    # the moment one of the class names is more than a word long.
    for i, lab in enumerate((pos.upper(), neg.upper())):
        y = CY + CH * (i + 0.5)
        body.append(text(CX - 16, y - 4, "ACTUALLY", 9, 600, anchor="end",
                         fill=MUTED))
        body.append(text(CX - 16, y + 10, lab, 10, 750, anchor="end",
                         fill="var(--dg-text)"))
    CELLS = [(0, 0, tp), (1, 0, fn), (0, 1, fp), (1, 1, tn)]
    for col, row, n in CELLS:
        x, y = CX + col * CW, CY + row * CH
        body.append(box(x, y, CW - 4, CH - 4, None, fill=FILL2, stroke=LINE,
                        r=6))
        body.append(text(x + CW / 2 - 2, y + CH / 2 + 8, "{:,}".format(n), 22,
                         780, fill="var(--dg-text)"))
    body.append(text(380, CY + CH * 2 + 26,
                     "Total cases: {:,}".format(tp + fp + fn + tn), 10.5, 650,
                     fill=MUTED))
    desc = ("A two by two table of results. Of the cases that were actually "
            "%s, %s were predicted %s and %s were predicted %s. Of the cases "
            "that were actually %s, %s were predicted %s and %s were predicted "
            "%s. %s"
            % (pos, "{:,}".format(tp), pos, "{:,}".format(fn), neg,
               neg, "{:,}".format(fp), pos, "{:,}".format(tn), neg, desc_tail))
    return figure(name, 760, CY + CH * 2 + 44, "".join(body),
                  "Results table: " + title.lower(), desc)


@diagram("exam-conf-fraud")
def _conf_fraud():
    return _conf("ex-cf1", "Results of the fraud model on 10,000 transactions",
                 tp=96, fp=304, fn=24, tn=9576, pos="fraud", neg="genuine",
                 desc_tail="The total number of cases is 10,000.")


@diagram("exam-conf-disease")
def _conf_disease():
    return _conf("ex-cf2", "Results of the screening model on 4,000 patients",
                 tp=152, fp=468, fn=38, tn=3342, pos="positive",
                 neg="negative",
                 desc_tail="The total number of cases is 4,000.")


@diagram("exam-conf-churn")
def _conf_churn():
    return _conf("ex-cf3", "Results of the churn model on 2,000 customers",
                 tp=210, fp=90, fn=140, tn=1560, pos="will leave",
                 neg="will stay",
                 desc_tail="The total number of cases is 2,000.")


# =============================================== other resource material

@diagram("exam-api-exchange")
def _ex_api():
    """A request and two responses, printed as they would arrive."""
    body = [text(380, 24, "Two attempts to call the same endpoint", 11.5, 700,
                 fill=MUTED)]
    LINES = [
        (60, "REQUEST", "GET /api/v2/orders?since=2026-03-01&limit=500", TEAL),
        (86, "", "Authorization: Bearer 9f2c…", TEAL),
        (128, "RESPONSE 1", "429 Too Many Requests", WARN),
        (154, "", "Retry-After: 60", WARN),
        (196, "RESPONSE 2", "200 OK", TEAL),
        (222, "", '{ "orders": [ … 100 items … ],', TEAL),
        (246, "", '  "next": "/api/v2/orders?page=2" }', TEAL),
    ]
    for y, label, txt, tone in LINES:
        if label:
            body.append(text(68, y + 4, label, 9.6, 750, anchor="start",
                             fill=tone))
        body.append(box(176, y - 14, 516, 24, None,
                        fill=FILL2 if tone == TEAL else WARN_SOFT,
                        stroke=LINE if tone == TEAL else WARN, r=4))
        body.append(text(190, y + 4, txt, 10, 500, anchor="start",
                         fill="var(--dg-text)", mono=True))
    body.append(text(380, 288, "The client code reads the orders array and "
                     "stops.", 10.5, 600, fill=MUTED))
    desc = ("A printed API exchange. The request is GET slash api slash v2 "
            "slash orders, with query parameters since equals 2026-03-01 and "
            "limit equals 500, and an Authorization header carrying a bearer "
            "token. The first response is status 429 Too Many Requests, with a "
            "Retry-After header of 60. The second response is status 200 OK "
            "with a JSON body containing an orders array of 100 items and a "
            "next field pointing at slash api slash v2 slash orders question "
            "mark page equals 2. A note states that the client code reads the "
            "orders array and stops.")
    return figure("ex-api", 760, 306, "".join(body),
                  "An API request and two responses", desc)


@diagram("exam-access-matrix")
def _ex_access():
    """A role and permission matrix to be critiqued."""
    COLS = [(170, "role"), (110, "read orders"), (120, "read payroll"),
            (120, "export all data"), (120, "delete records")]
    ROWS = [("Analyst", "yes", "yes", "yes", "yes"),
            ("Marketing assistant", "yes", "no", "yes", "no"),
            ("Developer", "yes", "yes", "yes", "yes"),
            ("Temporary intern", "yes", "no", "yes", "no"),
            ("Former employee (account active)", "yes", "yes", "yes", "yes")]
    body = [text(380, 24, "Current access permissions at one company", 11.5,
                 700, fill=MUTED),
            _table(30, 42, COLS, ROWS, head_tone=LILAC, head_soft=LILAC_SOFT,
                   rh=28)]
    desc = ("A table of access permissions by role, with the columns read "
            "orders, read payroll, export all data and delete records. "
            "Analyst: yes, yes, yes, yes. Marketing assistant: yes, no, yes, "
            "no. Developer: yes, yes, yes, yes. Temporary intern: yes, no, "
            "yes, no. Former employee whose account is still active: yes, yes, "
            "yes, yes.")
    return figure("ex-acc", 760, 42 + 6 * 28 + 24, "".join(body),
                  "Access permission matrix", desc)


@diagram("exam-two-tables")
def _ex_join():
    """Two tables from two systems, with definitions that disagree."""
    body = [text(380, 24, "The same customers, as held by two systems", 11.5,
                 700, fill=MUTED),
            text(200, 52, "SALES SYSTEM", 10.5, 750, fill=TEAL),
            _table(28, 62, [(90, "cust_id"), (130, "surname"),
                            (90, "status"), (70, "since")],
                   [("204", "Nkemdirim", "active", "2024"),
                    ("311", "Baptiste", "active", "2025"),
                    ("118", "Olawale", "lapsed", "2023"),
                    ("455", "Mihai", "active", "2026")]),
            text(566, 52, "SUPPORT SYSTEM", 10.5, 750, fill=LILAC),
            _table(404, 62, [(110, "customerId"), (130, "lastName"),
                             (110, "isActive")],
                   [("C-204", "NKEMDIRIM", "TRUE"),
                    ("C-311", "Baptiste", "TRUE"),
                    ("C-118", "Olawale", "TRUE"),
                    ("C-902", "Hargreaves", "FALSE")],
                   head_tone=LILAC, head_soft=LILAC_SOFT)]
    body.append(box(28, 196, 704, 54, None, fill=FILL2, stroke=LINE, r=8))
    body.append(text(380, 216, "Sales counts a customer as active if they "
                     "ordered in the last 12 months.", 10, 500, fill=MUTED))
    body.append(text(380, 234, "Support counts a customer as active if their "
                     "account has not been closed.", 10, 500, fill=MUTED))
    desc = ("Two tables holding the same customers. The sales system table has "
            "the columns cust_id, surname, status and since, and contains 204 "
            "Nkemdirim active since 2024; 311 Baptiste active since 2025; 118 "
            "Olawale lapsed since 2023; and 455 Mihai active since 2026. The "
            "support system table has the columns customerId, lastName and "
            "isActive, and contains C-204 NKEMDIRIM in capitals TRUE; C-311 "
            "Baptiste TRUE; C-118 Olawale TRUE; and C-902 Hargreaves FALSE. "
            "Two notes state the definitions: sales counts a customer as "
            "active if they ordered in the last twelve months, while support "
            "counts a customer as active if their account has not been "
            "closed.")
    return figure("ex-join", 760, 262, "".join(body),
                  "The same customers held by two systems", desc)


@diagram("exam-energy-figures")
def _ex_energy():
    """Two data centres' figures, for a PUE calculation."""
    COLS = [(220, ""), (150, "Site A"), (150, "Site B")]
    ROWS = [("Total facility power (kW)", "2,400", "1,980"),
            ("Power to IT equipment (kW)", "1,500", "1,800"),
            ("Renewable share of supply", "20%", "85%"),
            ("Mean inlet temperature", "18 °C", "27 °C"),
            ("Hardware refresh cycle", "3 years", "6 years"),
            ("Idle servers (of 900)", "310", "40")]
    body = [text(380, 24, "Two data centres, same workload", 11.5, 700,
                 fill=MUTED),
            _table(120, 42, COLS, ROWS, rh=28)]
    desc = ("A table comparing two data centres running the same workload. "
            "Total facility power: Site A 2,400 kilowatts, Site B 1,980 "
            "kilowatts. Power delivered to IT equipment: Site A 1,500 "
            "kilowatts, Site B 1,800 kilowatts. Renewable share of supply: "
            "Site A 20 per cent, Site B 85 per cent. Mean inlet temperature: "
            "Site A 18 degrees Celsius, Site B 27 degrees Celsius. Hardware "
            "refresh cycle: Site A 3 years, Site B 6 years. Idle servers out "
            "of 900: Site A 310, Site B 40.")
    return figure("ex-nrg", 760, 42 + 7 * 28 + 24, "".join(body),
                  "Figures for two data centres", desc)


@diagram("exam-pipeline-gaps")
def _ex_pipeline():
    """A pipeline with two stages left blank."""
    STAGES = ["Define the question", "Collect", "?", "Transform", "Analyse",
              "?", "Act and monitor"]
    body = [text(380, 24, "An analytics pipeline with two stages missing",
                 11.5, 700, fill=MUTED)]
    y = 54
    for i, name in enumerate(STAGES):
        x = 24 + (i % 4) * 182
        row = i // 4
        yy = y + row * 92
        blank = name == "?"
        body.append(box(x, yy, 164, 52, None,
                        fill=WARN_SOFT if blank else FILL,
                        stroke=WARN if blank else LINE, r=8,
                        dash="5 4" if blank else None))
        body.append(text(x + 82, yy + 32,
                         "stage %d" % (i + 1) if blank else name,
                         11 if not blank else 10.5, 700 if blank else 600,
                         fill=WARN if blank else "var(--dg-text)"))
        if blank:
            body.append(text(x + 82, yy + 16, "?", 15, 800, fill=WARN))
        if i % 4 != 3 and i != len(STAGES) - 1:
            body.append(line(x + 168, yy + 26, x + 178, yy + 26, stroke=LINE,
                             arrow=True))
    body.append(path("M752 80 L752 120 L18 120 L18 146", stroke=LINE, w=1.4,
                     dash="4 4", arrow=True))
    desc = ("An analytics pipeline drawn as seven stages in order, with the "
            "third and the sixth left blank and marked with a question mark. "
            "The stages given are: one, define the question; two, collect; "
            "three, missing; four, transform; five, analyse; six, missing; "
            "seven, act and monitor.")
    return figure("ex-pipe", 760, 212, "".join(body),
                  "An analytics pipeline with two stages missing", desc)
