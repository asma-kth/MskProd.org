"""Diagrams and graphs for the OCR Data Analytics units.

Data analytics is the one subject on the site where the pictures are not an
aid to the content, they are the content: a distribution, a correlation, an
overfitted curve and a confusion matrix are things you have to see to reason
about. Several of these are therefore real plotted graphs with real numbers
rather than schematic boxes, drawn from a fixed dataset defined in the code so
the figures in the caption always match the picture.

Registered into the shared diagram registry, so `!diagram <name>` works as it
does everywhere else.
"""
import math

from .diagrams import (diagram, TEAL, TEAL_SOFT, LILAC, LILAC_SOFT, WARN,
                       WARN_SOFT, FILL, LINE, MUTED)
from .svg import (figure, figure_steps, step, box, text, line, path, circle,
                  chip)

FILL2 = "var(--dg-fill-2)"


# --------------------------------------------------------------- plot helpers

def axes(x0, y0, w, h, xlab, ylab, xticks=(), yticks=(), grid=True):
    """A pair of axes with labelled ticks, in SVG user units.

    x0, y0 is the origin at the bottom left. Everything else in these graphs
    is positioned through px() and py() so the data and the axes cannot drift
    apart when a figure is resized.
    """
    out = [line(x0, y0, x0 + w, y0, stroke=LINE, w=1.6),
           line(x0, y0, x0, y0 - h, stroke=LINE, w=1.6),
           text(x0 + w / 2, y0 + 38, xlab, 11, 650, fill=MUTED)]
    out.append('<text x="%d" y="%d" text-anchor="middle" font-size="11" '
               'font-weight="650" fill="%s" transform="rotate(-90 %d %d)">%s</text>'
               % (x0 - 44, y0 - h / 2, MUTED, x0 - 44, y0 - h / 2, ylab))
    for frac, lab in xticks:
        x = x0 + w * frac
        out.append(line(x, y0, x, y0 + 5, stroke=LINE, w=1.2))
        out.append(text(x, y0 + 19, lab, 9.5, 500, fill=MUTED))
        if grid and frac not in (0,):
            out.append(line(x, y0, x, y0 - h, stroke=LINE, w=0.7, dash="2 5"))
    for frac, lab in yticks:
        y = y0 - h * frac
        out.append(line(x0 - 5, y, x0, y, stroke=LINE, w=1.2))
        out.append(text(x0 - 10, y + 4, lab, 9.5, 500, anchor="end", fill=MUTED))
        if grid and frac not in (0,):
            out.append(line(x0, y, x0 + w, y, stroke=LINE, w=0.7, dash="2 5"))
    return "".join(out)


def _rng(seed):
    """A tiny deterministic generator, so a figure never changes between builds."""
    state = [seed]

    def nxt():
        state[0] = (state[0] * 1103515245 + 12345) % 2147483648
        return state[0] / 2147483648.0
    return nxt


# ============================================================ F200: DIKW

@diagram("data-dikw")
def _dikw():
    """Data, information, knowledge, wisdom, with one value carried up."""
    body = [text(380, 24, "The same reading, four times over", 12, 650,
                 fill=MUTED)]
    ROWS = [("DATA", "37.2", "a raw fact with no context", TEAL, TEAL_SOFT),
            ("INFORMATION", "Patient A1402: temperature 37.2 °C, 14 March",
             "context, units and a subject added", LILAC, LILAC_SOFT),
            ("KNOWLEDGE", "that is within the normal range for this patient",
             "interpretation, from experience", TEAL, TEAL_SOFT),
            ("WISDOM", "no action now; review if it rises for three days",
             "a judgement about what to do", LILAC, LILAC_SOFT)]
    for i, (k, val, note, tone, soft) in enumerate(ROWS):
        y = 50 + i * 74
        inset = i * 46
        w = 704 - inset * 2
        body.append(box(28 + inset, y, w, 58, None, fill=soft, stroke=tone, r=8))
        body.append(text(44 + inset, y + 22, k, 11, 750, anchor="start",
                         fill=tone))
        body.append(text(380, y + 22, val, 12, 600, fill="var(--dg-text)"))
        body.append(text(380, y + 42, note, 10, 450, fill=MUTED))
        if i < 3:
            body.append(path("M380 %d L380 %d" % (y + 58, y + 72),
                             stroke=tone, w=1.6, arrow=True))
    body.append(text(380, 352, "Each step adds something. Data is precise and "
                     "useless; wisdom is useful and cannot be stored in a table.",
                     11, 600, fill=MUTED))
    desc = ("The same measurement shown at four levels. As data it is the bare "
            "value 37.2, a raw fact with no context, which could be a "
            "temperature, a price or a percentage. As information it becomes "
            "'patient A1402: temperature 37.2 degrees Celsius, 14 March', because "
            "a subject, a unit and a time have been added. As knowledge it becomes "
            "'that is within the normal range for this patient', which is "
            "interpretation drawn from experience. As wisdom it becomes 'no action "
            "now, review if it rises for three consecutive days', which is a "
            "judgement about what to do. Each step upward adds something the "
            "previous level lacked: data is precise and useless on its own, while "
            "wisdom is useful and cannot be stored in a database.")
    return figure("data-dikw", 760, 366, "".join(body),
                  "Data, information, knowledge and wisdom", desc,
                  "The word the exam wants for the gap between data and "
                  "information is context.")


# ================================================= F200: types of data

@diagram("data-types-tree")
def _types():
    """Every classification of data in TA1, on one branching chart."""
    body = [text(380, 24, "How any field you meet is classified", 12, 650,
                 fill=MUTED)]
    body.append(box(300, 44, 160, 38, "DATA", fill=FILL, stroke=LINE, r=8,
                    label_size=12))
    # Quantitative branch.
    body.append(path("M300 63 L200 63 L200 96", stroke=LINE, arrow=True))
    body.append(box(96, 100, 208, 42, None, fill=TEAL_SOFT, stroke=TEAL, r=8))
    body.append(text(200, 118, "QUANTITATIVE", 11, 750, fill=TEAL))
    body.append(text(200, 133, "numbers you can calculate with", 9.5, 450,
                     fill=MUTED))
    for i, (k, v) in enumerate([("Discrete", "whole values only: 3 orders"),
                                ("Continuous", "any value in a range: 1.73 m")]):
        y = 158 + i * 50
        body.append(box(96, y, 208, 42, None, fill=FILL, stroke=TEAL, r=6))
        body.append(text(110, y + 18, k, 10.5, 700, anchor="start", fill=TEAL))
        body.append(text(110, y + 33, v, 9.5, 450, anchor="start", fill=MUTED))
        body.append(line(200, y - 16, 200, y - 2, stroke=LINE, w=1.2))
    # Qualitative branch.
    body.append(path("M460 63 L560 63 L560 96", stroke=LINE, arrow=True))
    body.append(box(456, 100, 208, 42, None, fill=LILAC_SOFT, stroke=LILAC, r=8))
    body.append(text(560, 118, "QUALITATIVE", 11, 750, fill=LILAC))
    body.append(text(560, 133, "words, categories, images", 9.5, 450, fill=MUTED))
    for i, (k, v) in enumerate([("Nominal", "no order: payment method"),
                                ("Ordinal", "ordered, uneven gaps: poor to good")]):
        y = 158 + i * 50
        body.append(box(456, y, 208, 42, None, fill=FILL, stroke=LILAC, r=6))
        body.append(text(470, y + 18, k, 10.5, 700, anchor="start", fill=LILAC))
        body.append(text(470, y + 33, v, 9.5, 450, anchor="start", fill=MUTED))
        body.append(line(560, y - 16, 560, y - 2, stroke=LINE, w=1.2))
    # Levels of measurement, as a scale.
    body.append(text(380, 276, "LEVELS OF MEASUREMENT, and what each one lets you "
                     "calculate", 11, 700, fill=MUTED))
    LEVELS = [("Nominal", "count only", "payment method"),
              ("Ordinal", "count, median", "satisfaction rating"),
              ("Interval", "+ and −, mean", "temperature in °C"),
              ("Ratio", "all of it, ratios", "height, income")]
    for i, (k, calc, ex) in enumerate(LEVELS):
        x = 28 + i * 178
        body.append(box(x, 290, 168, 58, None, fill=FILL, stroke=LINE, r=6))
        body.append(text(x + 84, 308, k, 11, 700, fill=TEAL))
        body.append(text(x + 84, 324, calc, 9.5, 500, fill="var(--dg-text)"))
        body.append(text(x + 84, 339, ex, 9.5, 450, fill=MUTED))
        if i < 3:
            body.append(line(x + 170, 319, x + 176, 319, stroke=LINE, arrow=True))
    # Structure.
    body.append(text(380, 376, "STRUCTURE", 11, 700, fill=MUTED))
    STRUCT = [("Structured", "fixed rows and columns", "database, CSV", TEAL),
              ("Semi-structured", "tags, no fixed schema", "JSON, XML, logs", LILAC),
              ("Unstructured", "no model at all", "text, image, audio", WARN)]
    for i, (k, v, ex, tone) in enumerate(STRUCT):
        x = 28 + i * 238
        body.append(box(x, 388, 228, 58, None, fill=FILL, stroke=tone, r=6))
        body.append(text(x + 114, 406, k, 11, 700, fill=tone))
        body.append(text(x + 114, 422, v, 9.5, 500, fill="var(--dg-text)"))
        body.append(text(x + 114, 437, ex, 9.5, 450, fill=MUTED))
    desc = ("A branching classification of data. At the top level data divides "
            "into quantitative, which is numbers you can calculate with, and "
            "qualitative, which is words, categories and images. Quantitative data "
            "divides again into discrete, taking whole values only such as three "
            "orders, and continuous, taking any value in a range such as 1.73 "
            "metres. Qualitative data divides into nominal, categories with no "
            "order such as payment method, and ordinal, ordered categories with "
            "uneven gaps such as a satisfaction rating from poor to good. "
            "Separately, the four levels of measurement set what calculations are "
            "legitimate: nominal allows counting only, ordinal allows counting and "
            "a median, interval allows addition, subtraction and a mean, and ratio "
            "allows everything including meaningful ratios because it has a true "
            "zero. Finally, data is classified by structure: structured data has "
            "fixed rows and columns, as in a database or CSV; semi-structured data "
            "has tags but no fixed schema, as in JSON, XML or log files; and "
            "unstructured data has no model at all, as in free text, images and "
            "audio.")
    return figure("data-types", 760, 462, "".join(body),
                  "Classifications of data", desc,
                  "The level of measurement decides which calculations are "
                  "legitimate. A mean of nominal data means nothing.")


# =============================================== F200: the analytics pipeline

@diagram("data-pipeline")
def _pipeline():
    """The seven steps, one at a time, with what each produces."""
    STEPS = [
        ("Define the question", "a decision somebody will make differently",
         "Without this, the output is a dashboard nobody opens."),
        ("Collect", "raw data from systems, surveys, sensors, APIs",
         "Every source brings its own definitions and its own gaps."),
        ("Clean and prepare", "typed, complete, consistent, deduplicated data",
         "This is where most of the time actually goes."),
        ("Transform", "joined, aggregated, derived fields at the right grain",
         "Getting the grain wrong double counts everything downstream."),
        ("Analyse", "patterns, comparisons, correlations, models",
         "The shortest step, and the one everybody pictures."),
        ("Visualise and communicate", "one chart and one sentence",
         "If the chart needs a paragraph to read, it is the wrong chart."),
        ("Act and monitor", "a decision, and a measurement of whether it worked",
         "An analysis nobody acts on has produced nothing."),
    ]
    base = [text(380, 24, "Seven steps, and what each one produces", 12, 650,
                 fill=MUTED)]
    for i, (name, out, _) in enumerate(STEPS):
        y = 46 + i * 44
        base.append(box(28, y, 36, 34, str(i + 1), fill=FILL2, stroke=LINE, r=6,
                        label_size=12))
        base.append(box(72, y, 260, 34, None, fill=FILL, stroke=LINE, r=6))
        base.append(text(86, y + 22, name, 11, 650, anchor="start",
                         fill="var(--dg-text)"))
        base.append(line(338, y + 17, 356, y + 17, stroke=LINE, arrow=True))
        base.append(box(362, y, 370, 34, None, fill=FILL2, stroke=LINE, r=6))
        base.append(text(376, y + 22, out, 10, 450, anchor="start", fill=MUTED))
    steps, L = [], []
    for i, (name, _, note) in enumerate(STEPS):
        y = 46 + i * 44
        L.append("%d. %s — %s" % (i + 1, name, note))
        steps.append(step(i + 1,
                          box(24, y - 4, 712, 42, None, fill="none",
                              stroke=TEAL, r=8)
                          + text(380, 360, note, 11, 600, fill=TEAL),
                          L[-1]))
    desc = ("The analytics pipeline in seven steps, each with what it produces. "
            "One, define the question, producing a decision somebody will make "
            "differently; without this the output is a dashboard nobody opens. "
            "Two, collect, producing raw data from systems, surveys, sensors and "
            "APIs, each source bringing its own definitions and gaps. Three, clean "
            "and prepare, producing typed, complete, consistent and deduplicated "
            "data, which is where most of the time actually goes. Four, transform, "
            "producing joined and aggregated data with derived fields at the right "
            "grain, since the wrong grain double counts everything downstream. "
            "Five, analyse, producing patterns, comparisons, correlations and "
            "models, which is the shortest step and the one everybody pictures. "
            "Six, visualise and communicate, producing one chart and one sentence. "
            "Seven, act and monitor, producing a decision and a measurement of "
            "whether it worked, because an analysis nobody acts on has produced "
            "nothing.")
    return figure_steps("data-pipe", 760, 374, "".join(base), steps,
                        "The analytics pipeline", desc,
                        "Steps three and four are most of the work. Step five is "
                        "the one that gets taught.", labels=L)


# ===================================================== F200: cleaning data

@diagram("data-cleaning")
def _cleaning():
    """One dirty extract, annotated, and then the same rows cleaned."""
    body = [text(380, 24, "The same six rows, before and after", 12, 650,
                 fill=MUTED)]
    COLS = [(30, 56, "id"), (86, 150, "name"), (236, 118, "country"),
            (354, 108, "joined"), (462, 94, "spend")]
    DIRTY = [("1", "A. Shah", "UK", "03/04/2026", "120.00"),
             ("2", "a. shah ", "U.K.", "2026-04-03", "120"),
             ("3", "L. Okafor", "United Kingdom", "4/3/26", ""),
             ("4", "M. Price", "GB", "03-04-2026", "99999"),
             ("5", "", "uk", "03/04/2026", "84.50"),
             ("6", "J. Ali", "Uk", "03/04/2026", "76.20")]
    CLEAN = [("1", "A. Shah", "GB", "2026-04-03", "120.00"),
             ("3", "L. Okafor", "GB", "2026-03-04", "unknown"),
             ("4", "M. Price", "GB", "2026-04-03", "flagged"),
             ("5", "unknown", "GB", "2026-04-03", "84.50"),
             ("6", "J. Ali", "GB", "2026-04-03", "76.20")]

    def table(x_off, rows, head_tone, head_soft, title):
        out = [text(x_off + 240, 52, title, 11.5, 750, fill=head_tone)]
        for x, w, label in COLS:
            out.append(box(x_off + x, 60, w, 24, None, fill=head_soft,
                           stroke=head_tone, r=3))
            out.append(text(x_off + x + w / 2, 77, label, 9.5, 700,
                            fill=head_tone))
        for r, row in enumerate(rows):
            y = 86 + r * 26
            for (x, w, _), val in zip(COLS, row):
                out.append(box(x_off + x, y, w, 24, None, fill=FILL,
                               stroke=LINE, r=3))
                out.append(text(x_off + x + w / 2, y + 16,
                                val if val else "—", 9.5, 450,
                                fill="var(--dg-text)" if val else WARN))
        return "".join(out)

    body.append(table(0, DIRTY, WARN, WARN_SOFT, "AS EXTRACTED"))
    body.append(table(190, CLEAN, TEAL, TEAL_SOFT, "AFTER CLEANING"))
    ISSUES = [("Duplicate", "rows 1 and 2 are the same person, differently cased"),
              ("Inconsistent category", "UK, U.K., United Kingdom, GB, uk, Uk"),
              ("Inconsistent dates", "03/04/2026 and 4/3/26 are ambiguous"),
              ("Missing values", "a blank name and a blank spend"),
              ("Outlier", "99999 is not a plausible spend"),
              ("Whitespace and case", "'a. shah ' will not match 'A. Shah'")]
    for i, (k, v) in enumerate(ISSUES):
        y = 262 + i * 26
        body.append(box(30, y, 702, 22, None,
                        fill=FILL2 if i % 2 == 0 else FILL, stroke="none", r=4))
        body.append(text(44, y + 15, k, 10, 700, anchor="start", fill=WARN))
        body.append(text(220, y + 15, v, 10, 450, anchor="start", fill=MUTED))
    body.append(box(30, 424, 702, 46, None, fill=TEAL_SOFT, stroke=TEAL, r=8))
    body.append(text(381, 443, "Note the decisions: the duplicate was merged, "
                     "the outlier was flagged not deleted, and the blanks were "
                     "kept as explicitly unknown.", 10.5, 650, fill=TEAL))
    body.append(text(381, 460, "Deleting every row with a blank would have "
                     "removed whichever source stopped capturing that field.",
                     10, 500, fill=MUTED))
    desc = ("One extract of six rows shown as it arrived and again after "
            "cleaning. The dirty version contains six distinct problems. Rows one "
            "and two are the same person recorded twice with different "
            "capitalisation and a trailing space, which is a duplicate that a "
            "naive exact match would miss. The country column holds one real "
            "category spelled six ways: UK, U.K., United Kingdom, GB, uk and Uk. "
            "The joined column mixes formats, and 03/04/2026 against 4/3/26 is "
            "genuinely ambiguous about which is the month. One name and one spend "
            "are blank. A spend of 99999 is not a plausible value and is an "
            "outlier. The cleaned version standardises the country to the code GB, "
            "converts every date to ISO format, merges the duplicate pair into one "
            "row, records the missing values explicitly as unknown rather than "
            "deleting the rows, and flags the outlier for investigation rather "
            "than silently removing it. The decisions matter more than the "
            "mechanics: deleting every row with a blank field would have removed "
            "whichever source had stopped capturing that field, which biases the "
            "result rather than cleaning it.")
    return figure("data-clean", 760, 482, "".join(body),
                  "A dirty extract and the same rows cleaned", desc,
                  "Cleaning is a set of decisions, not a button. Record which "
                  "ones you took and why.")


# ============================================= F200: distributions and averages

@diagram("data-distribution")
def _distribution():
    """A real right-skewed histogram with the mean and median marked.

    The gap between the two is the whole point, and it is only convincing when
    the bars are drawn from actual numbers rather than suggested, and when the
    tail is long enough to move the mean somewhere the median plainly is not.
    """
    X0, Y0, W, H = 96, 292, 576, 214
    # Order values in £20 bands: a long thin tail of large orders, which is
    # what a real order-value distribution looks like.
    COUNTS = [2, 18, 58, 84, 70, 50, 36, 27, 21, 17, 14, 12, 10, 9, 8, 7, 6,
              5, 4, 3]
    BAND = 20
    total = sum(COUNTS)
    mean = sum(c * (i * BAND + BAND / 2.0) for i, c in enumerate(COUNTS)) / total
    cum = 0
    for i, c in enumerate(COUNTS):
        prev, cum = cum, cum + c
        if cum >= total / 2.0:
            # interpolated inside the band, which is how a grouped median works
            median = i * BAND + (total / 2.0 - prev) / c * BAND
            break
    peak = max(COUNTS)
    span = len(COUNTS) * BAND
    bw = W / float(len(COUNTS))

    body = [text(380, 24, "Order values: a right-skewed distribution", 12, 650,
                 fill=MUTED)]
    body.append(axes(X0, Y0, W, H, "order value (\u00a3)", "number of orders",
                     xticks=[(i / float(len(COUNTS)), str(i * BAND))
                             for i in range(0, len(COUNTS) + 1, 4)],
                     yticks=[(c / float(peak), str(c))
                             for c in (0, 20, 40, 60, peak)]))
    for i, c in enumerate(COUNTS):
        h = H * c / float(peak)
        body.append('<rect x="%.1f" y="%.1f" width="%.1f" height="%.1f" rx="2" '
                    'fill="%s" stroke="%s" stroke-width="1"/>'
                    % (X0 + i * bw + 1, Y0 - h, bw - 2, h, TEAL_SOFT, TEAL))
    # The two markers sit inside the plot, stacked, so neither covers the
    # title above it nor the other.
    for val, label, tone, dy in ((median, "median \u00a3%.0f" % median, TEAL, 22),
                                 (mean, "mean \u00a3%.0f" % mean, WARN, 48)):
        x = X0 + W * val / span
        body.append(line(x, Y0, x, Y0 - H - 4, stroke=tone, w=2, dash="6 4"))
        body.append(chip(min(x + 54, X0 + W - 54), Y0 - H + dy, label,
                         fill=FILL, stroke=tone, text_fill=tone))
    body.append(box(96, 348, 576, 58, None, fill=WARN_SOFT, stroke=WARN, r=8))
    body.append(text(384, 370, "A long tail of a few very large orders drags "
                     "the mean \u00a3%.0f well above the median \u00a3%.0f."
                     % (mean, median), 11, 700, fill=WARN))
    body.append(text(384, 390, "Quote the mean to make the typical order look "
                     "bigger; quote the median to describe it honestly.",
                     10, 500, fill=MUTED))
    desc = ("A histogram of %d order values in twenty pound bands, with a "
            "pronounced right skew: the bars rise steeply to a peak in the sixty "
            "to eighty pound band and then fall away into a long thin tail of "
            "larger orders stretching to four hundred pounds. Two dashed lines "
            "are marked. The median, at about %.0f pounds, is the value with half "
            "the orders below it and half above. The mean, at about %.0f pounds, "
            "sits well to the right of it, because the orders in the tail pull it "
            "upward while they cannot move the median at all. That gap is why the "
            "choice of average is a presentational decision as much as a "
            "statistical one: quoting the mean makes the typical order look "
            "considerably larger than it is, while the median describes what a "
            "typical customer actually spends." % (total, median, mean))
    return figure("data-dist", 760, 418, "".join(body),
                  "A skewed distribution with the mean and median marked", desc,
                  "On a skewed distribution the mean and the median answer "
                  "different questions. Say which one you quoted.")


# =============================================== F200: correlation graphs

@diagram("data-correlation")
def _correlation():
    """Four scatter plots: positive, none, negative, and spurious."""
    base = [text(380, 24, "Correlation, and what it does not tell you", 12, 650,
                 fill=MUTED)]

    def plot(kind, title, note, tone, seed):
        X0, Y0, W, H = 150, 272, 470, 190
        out = [axes(X0, Y0, W, H, "advertising spend" if kind != "spurious"
                    else "ice cream sales",
                    "sales" if kind != "spurious" else "drownings",
                    xticks=[(f, "") for f in (0.25, 0.5, 0.75, 1.0)],
                    yticks=[(f, "") for f in (0.25, 0.5, 0.75, 1.0)])]
        nxt = _rng(seed)
        pts = []
        for _ in range(42):
            x = nxt()
            noise = (nxt() - 0.5)
            if kind == "positive":
                y = 0.12 + 0.76 * x + noise * 0.26
            elif kind == "negative":
                y = 0.88 - 0.76 * x + noise * 0.26
            elif kind == "none":
                y = 0.5 + noise * 0.8
            else:
                y = 0.1 + 0.8 * x + noise * 0.2
            pts.append((min(max(x, 0.02), 0.98), min(max(y, 0.02), 0.98)))
        for x, y in pts:
            out.append(circle(X0 + W * x, Y0 - H * y, 4.2, fill=tone,
                              stroke=tone, w=0))
        if kind != "none":
            # The least squares line, so the trend is drawn rather than implied.
            n = len(pts)
            mx = sum(p[0] for p in pts) / n
            my = sum(p[1] for p in pts) / n
            num = sum((p[0] - mx) * (p[1] - my) for p in pts)
            den = sum((p[0] - mx) ** 2 for p in pts) or 1e-9
            m = num / den
            c = my - m * mx
            out.append(line(X0, Y0 - H * c, X0 + W, Y0 - H * (m + c),
                            stroke=WARN if kind == "spurious" else tone, w=2.4))
        out.append(text(385, 50, title, 12, 750, fill=tone))
        out.append(text(385, 308, note, 11, 600, fill=MUTED))
        return "".join(out)

    L = ["Strong positive correlation: as one rises, so does the other.",
         "No correlation: knowing one tells you nothing about the other.",
         "Strong negative correlation: as one rises, the other falls.",
         "And a strong correlation that is not a cause at all."]
    steps = [
        step(1, plot("positive", "POSITIVE",
                     "More spend, more sales. The points cluster round a rising line.",
                     TEAL, 7), L[0]),
        step(2, plot("none", "NONE",
                     "The cloud has no direction, so there is nothing to predict from.",
                     LILAC, 19), L[1]),
        step(3, plot("negative", "NEGATIVE",
                     "More of one, less of the other. Still a relationship.",
                     TEAL, 31), L[2]),
        step(4, plot("spurious", "SPURIOUS",
                     "Ice cream and drownings rise together. Hot weather causes both.",
                     WARN, 43), L[3]),
    ]
    desc = ("Four scatter plots. The first shows a strong positive correlation "
            "between advertising spend and sales: the points cluster around a "
            "rising line, so a higher spend is associated with higher sales. The "
            "second shows no correlation: the points form a shapeless cloud, so "
            "knowing one variable tells you nothing about the other. The third "
            "shows a strong negative correlation, where the fitted line falls, so "
            "more of one variable goes with less of the other, which is still a "
            "relationship and still useful. The fourth shows ice cream sales "
            "plotted against drowning deaths, which produces a correlation as "
            "strong as the first plot and means nothing causal at all: hot weather "
            "independently causes more ice cream buying and more swimming. The "
            "shape of the graph cannot tell these two apart, which is why "
            "establishing cause needs a mechanism or a controlled experiment "
            "rather than a coefficient.")
    return figure_steps("data-corr", 760, 322, "".join(base), steps,
                        "Positive, negative, absent and spurious correlation",
                        desc,
                        "All four of these are correlations. Only three of them "
                        "are relationships, and none of them is proof of a cause.",
                        labels=L)


# ================================================= F200: storage and ETL

@diagram("data-store-choice")
def _stores():
    """Four stores, and the question each one is built to answer."""
    body = [text(380, 24, "Four stores, four different jobs", 12, 650,
                 fill=MUTED)]
    STORES = [
        ("OLTP DATABASE", "running the business", TEAL, TEAL_SOFT,
         ["Many small reads and writes", "Strict integrity and transactions",
          "Normalised, row oriented", "Schema enforced on write"],
         "Take an order, update a balance"),
        ("DATA WAREHOUSE", "analysing the business", LILAC, LILAC_SOFT,
         ["Large analytical queries", "Modelled, often star schema",
          "Columnar, compressed", "Schema enforced on write"],
         "Sales by region by month"),
        ("DATA LAKE", "keeping everything", WARN, WARN_SOFT,
         ["Any structure, raw as it arrived", "Cheap object storage",
          "Nothing rejected, nothing promised", "Schema applied on read"],
         "Images, logs, anything, for later"),
        ("LAKEHOUSE", "both at once", TEAL, TEAL_SOFT,
         ["Warehouse engine over lake files", "Open table formats",
          "One copy, two workloads", "Schema where it is needed"],
         "The common modern design"),
    ]
    for i, (name, job, tone, soft, points, example) in enumerate(STORES):
        x = 24 + (i % 2) * 368
        y = 46 + (i // 2) * 182
        body.append(box(x, y, 348, 168, None, fill=soft, stroke=tone, r=10))
        body.append(text(x + 174, y + 24, name, 11.5, 750, fill=tone))
        body.append(text(x + 174, y + 40, job, 10, 500, fill=MUTED))
        for j, p in enumerate(points):
            body.append(text(x + 18, y + 64 + j * 20, "• " + p, 9.8, 450,
                             anchor="start", fill="var(--dg-text)"))
        body.append(box(x + 14, y + 138, 320, 22, None, fill=FILL, stroke=tone,
                        r=11))
        body.append(text(x + 174, y + 153, example, 9.8, 650, fill=tone))
    body.append(text(380, 420, "Schema on write guarantees quality and rejects "
                     "what does not fit. Schema on read loses nothing and "
                     "guarantees nothing.", 11, 600, fill=MUTED))
    desc = ("Four data stores and the job each is built for. An OLTP database "
            "runs the business: many small reads and writes, strict integrity and "
            "transactions, normalised and row oriented, with the schema enforced "
            "when data is written, as when taking an order or updating a balance. "
            "A data warehouse analyses the business: large analytical queries over "
            "modelled data, often in a star schema, stored columnar and "
            "compressed, again with the schema enforced on write, as when "
            "reporting sales by region by month. A data lake keeps everything: any "
            "structure, raw as it arrived, on cheap object storage, rejecting "
            "nothing and promising nothing, with the schema applied only when the "
            "data is read, which suits images, logs and anything else being kept "
            "for later. A lakehouse does both, running a warehouse style engine "
            "over lake files in open table formats so one copy of the data serves "
            "two workloads, which is the common modern design. The underlying "
            "trade is that schema on write guarantees quality and rejects what "
            "does not fit, while schema on read loses nothing and guarantees "
            "nothing.")
    return figure("data-stores", 760, 436, "".join(body),
                  "OLTP, warehouse, lake and lakehouse compared", desc,
                  "Pick the store from the question. The one that runs the "
                  "business is almost never the one that should answer it.")


@diagram("data-etl-elt")
def _etl():
    """ETL against ELT, with the consequence of each order."""
    body = [text(380, 24, "Same three letters, different order, different "
                 "consequences", 12, 650, fill=MUTED)]

    def chain(y, label, order, tone, soft, note):
        out = [text(70, y + 30, label, 13, 750, anchor="start", fill=tone)]
        x = 170
        for i, (step_name, detail) in enumerate(order):
            out.append(box(x, y, 150, 58, None, fill=soft, stroke=tone, r=8))
            out.append(text(x + 75, y + 24, step_name, 11.5, 700, fill=tone))
            out.append(text(x + 75, y + 42, detail, 9.5, 450, fill=MUTED))
            if i < 2:
                out.append(line(x + 156, y + 29, x + 182, y + 29, stroke=tone,
                                w=2, arrow=True))
            x += 188
        out.append(text(380, y + 78, note, 10.5, 550, fill=MUTED))
        return "".join(out)

    body.append(chain(56, "ETL",
                      [("Extract", "read from the source"),
                       ("Transform", "clean and reshape first"),
                       ("Load", "only modelled data lands")],
                      TEAL, TEAL_SOFT,
                      "Only clean data ever reaches the warehouse. If you need a "
                      "field you discarded, you re-extract from the source."))
    body.append(chain(176, "ELT",
                      [("Extract", "read from the source"),
                       ("Load", "raw data lands first"),
                       ("Transform", "reshape inside the warehouse")],
                      LILAC, LILAC_SOFT,
                      "The raw data stays available, so a transformation can be "
                      "redone. You pay to store and process data you may not use."))
    ROWS = [("Where the work happens", "A separate processing step",
             "Inside the warehouse engine"),
            ("What is stored", "Modelled data only",
             "Raw data and modelled data"),
            ("Reprocessing", "Needs a new extract", "Rerun the transformation"),
            ("Storage cost", "Lower", "Higher"),
            ("Best when", "Compute is expensive, rules are settled",
             "Storage is cheap, requirements change")]
    body.append(text(255, 288, "ETL", 11, 750, fill=TEAL))
    body.append(text(570, 288, "ELT", 11, 750, fill=LILAC))
    for i, (k, a, b) in enumerate(ROWS):
        y = 300 + i * 26
        body.append(box(28, y, 704, 24, None,
                        fill=FILL2 if i % 2 == 0 else FILL, stroke="none", r=4))
        body.append(text(42, y + 16, k, 10, 700, anchor="start", fill=MUTED))
        body.append(text(255, y + 16, a, 10, 450, fill=TEAL))
        body.append(text(570, y + 16, b, 10, 450, fill=LILAC))
    desc = ("ETL and ELT compared. In ETL the data is extracted from the source, "
            "transformed to clean and reshape it, and only then loaded, so only "
            "modelled data ever reaches the warehouse; if a field that was "
            "discarded turns out to be needed, the source has to be extracted "
            "again. In ELT the data is extracted, loaded raw into the warehouse, "
            "and transformed in place using the warehouse engine, so the raw data "
            "remains available and a transformation can simply be rerun, at the "
            "cost of storing and processing data that may never be used. The "
            "comparison table: the work happens in a separate processing step for "
            "ETL and inside the warehouse engine for ELT; ETL stores modelled data "
            "only while ELT stores both raw and modelled; reprocessing needs a new "
            "extract under ETL but only a rerun under ELT; storage cost is lower "
            "for ETL and higher for ELT; and ETL suits settled requirements where "
            "compute is expensive, while ELT suits changing requirements where "
            "storage is cheap, which is why it has become the common choice.")
    return figure("data-etl", 760, 446, "".join(body),
                  "ETL and ELT compared", desc,
                  "The letters are the same. The question is whether you keep "
                  "the raw data, and that decides what you can redo.")


# ================================================ F200: an API request

@diagram("data-api-request")
def _api():
    """One REST request and response, with the status codes that come back."""
    body = [text(380, 24, "One API request, start to finish", 12, 650,
                 fill=MUTED)]
    body.append(box(40, 48, 190, 44, None, fill=TEAL_SOFT, stroke=TEAL, r=8))
    body.append(text(135, 76, "YOUR SYSTEM", 11, 750, fill=TEAL))
    body.append(box(530, 48, 190, 44, None, fill=LILAC_SOFT, stroke=LILAC, r=8))
    body.append(text(625, 76, "THEIR API", 11, 750, fill=LILAC))
    body.append(line(135, 100, 135, 300, stroke=LINE, w=1.2, dash="4 4"))
    body.append(line(625, 100, 625, 300, stroke=LINE, w=1.2, dash="4 4"))

    MSGS = [
        (120, True, "GET /api/v1/orders?since=2026-04-01&limit=100",
         "method, endpoint, version, parameters"),
        (164, True, "Authorization: Bearer ••••  (your API key)",
         "sent in a header, never in the URL"),
        (216, False, "200 OK",
         "authenticated, authorised, query ran"),
        (260, False, '{ "orders": [ … ], "next": "/v1/orders?page=2" }',
         "JSON body, and a link to the next page"),
    ]
    for y, outward, msg, note in MSGS:
        x1, x2 = (135, 625) if outward else (625, 135)
        tone = TEAL if outward else LILAC
        body.append(line(x1 + (12 if outward else -12), y,
                         x2 - (12 if outward else -12), y, stroke=tone, w=2,
                         arrow=True))
        body.append(box(222, y - 32, 316, 24, None, fill=FILL, stroke=tone, r=4))
        body.append(text(380, y - 15, msg, 9.6, 600, fill=tone))
        body.append(text(380, y + 16, note, 9.4, 450, fill=MUTED))

    CODES = [("200", "OK", TEAL), ("201", "Created", TEAL),
             ("400", "Bad request: your parameters", WARN),
             ("401", "No valid key: who are you?", WARN),
             ("403", "Valid key, not allowed", WARN),
             ("404", "Not found", WARN),
             ("429", "Rate limited: back off and retry", WARN),
             ("500", "Their server broke, not you", WARN)]
    body.append(text(380, 328, "The status codes worth knowing", 11, 700,
                     fill=MUTED))
    for i, (code, meaning, tone) in enumerate(CODES):
        x = 28 + (i % 4) * 178
        y = 340 + (i // 4) * 44
        body.append(box(x, y, 168, 36, None,
                        fill=TEAL_SOFT if tone == TEAL else WARN_SOFT,
                        stroke=tone, r=6))
        body.append(text(x + 24, y + 23, code, 12, 750, fill=tone))
        body.append(text(x + 96, y + 23, meaning, 9.2, 500, fill=MUTED))
    body.append(text(380, 444, "Handle paging or you will silently process only "
                     "the first hundred records.", 11, 650, fill=WARN))
    desc = ("A single REST API exchange drawn as a sequence between your system "
            "and their API. First your system sends a GET request to the endpoint "
            "slash api slash v1 slash orders with query parameters limiting it to "
            "orders since the first of April and a page size of one hundred, which "
            "carries the method, the endpoint, the API version and the filters. The "
            "API key is sent in an Authorization header rather than in the URL. "
            "The API replies with a status of 200 OK, meaning the caller was "
            "authenticated, the action authorised and the query run, followed by a "
            "JSON body containing the orders and a link to the next page. The "
            "status codes worth knowing are: 200 OK; 201 Created; 400 bad request, "
            "meaning your parameters are wrong; 401 unauthenticated, meaning no "
            "valid key was supplied; 403 forbidden, meaning the key is valid but "
            "the action is not permitted; 404 not found; 429 too many requests, "
            "meaning you have hit the rate limit and should back off and retry; and "
            "500, a server error at their end rather than yours. The practical "
            "warning is paging: code that reads only the first response silently "
            "processes one hundred records and ignores the rest.")
    return figure("data-api", 760, 460, "".join(body),
                  "A REST API request and response", desc,
                  "401 means it does not know you. 403 means it knows you and "
                  "the answer is still no.")


# ====================================================== F200: access control

@diagram("data-access-control")
def _access():
    """Who can reach the data, drawn as the layers a request passes through."""
    body = [text(380, 24, "Every request passes through all of these", 12, 650,
                 fill=MUTED)]
    LAYERS = [
        ("AUTHENTICATION", "who are you?", "password + MFA, passkey, token, "
         "certificate", TEAL),
        ("AUTHORISATION", "what may you do?", "role based access control, "
         "least privilege", LILAC),
        ("ROW AND COLUMN SECURITY", "which part may you see?",
         "your region's rows; the salary column masked", TEAL),
        ("ENCRYPTION", "can it be read if intercepted or stolen?",
         "TLS in transit, encrypted at rest, passwords hashed", LILAC),
        ("AUDIT LOGGING", "what did you actually do?",
         "every access attributable, reviewed, retained", TEAL),
    ]
    for i, (name, q, detail, tone) in enumerate(LAYERS):
        y = 50 + i * 62
        inset = 0
        body.append(box(28 + inset, y, 704 - inset * 2, 50, None,
                        fill=TEAL_SOFT if tone == TEAL else LILAC_SOFT,
                        stroke=tone, r=8))
        body.append(text(46, y + 22, name, 11, 750, anchor="start", fill=tone))
        body.append(text(46, y + 38, q, 9.8, 450, anchor="start", fill=MUTED))
        body.append(text(716, y + 31, detail, 10, 500, anchor="end",
                         fill="var(--dg-text)"))
        if i < 4:
            body.append(path("M380 %d L380 %d" % (y + 50, y + 60), stroke=tone,
                             w=1.6, arrow=True))
    body.append(box(28, 368, 348, 72, None, fill=FILL, stroke=TEAL, r=8))
    body.append(text(202, 390, "LEAST PRIVILEGE", 11, 750, fill=TEAL))
    body.append(text(202, 408, "Everyone gets the minimum their role needs,",
                     10, 450, fill=MUTED))
    body.append(text(202, 423, "so one compromised account exposes little.",
                     10, 450, fill=MUTED))
    body.append(box(384, 368, 348, 72, None, fill=WARN_SOFT, stroke=WARN, r=8))
    body.append(text(558, 390, "THE USUAL FAILURE", 11, 750, fill=WARN))
    body.append(text(558, 408, "Not a broken cipher: a storage bucket left",
                     10, 450, fill=MUTED))
    body.append(text(558, 423, "public, or a role nobody ever reviewed.",
                     10, 450, fill=MUTED))
    desc = ("Access control drawn as five layers every request passes through. "
            "Authentication asks who you are, using a password with multi-factor "
            "authentication, a passkey, a token or a certificate. Authorisation "
            "asks what you may do, expressed through role based access control on "
            "the principle of least privilege. Row and column level security asks "
            "which part of the data you may see, so a user sees only their "
            "region's rows and the salary column is masked. Encryption asks whether "
            "the data could be read if intercepted or stolen, which means TLS in "
            "transit, encryption at rest, and passwords hashed rather than "
            "encrypted. Audit logging asks what you actually did, making every "
            "access attributable, reviewed and retained. Least privilege means "
            "everyone gets the minimum access their role needs, so a single "
            "compromised account exposes very little. The usual real world failure "
            "is not a broken cipher but a storage location left publicly readable, "
            "or a role granted once and never reviewed.")
    return figure("data-access", 760, 452, "".join(body),
                  "The layers of access control", desc,
                  "The cipher is almost never the weak point. The "
                  "configuration is.")


# ==================================================== F200: the GDPR on a page

@diagram("data-gdpr")
def _gdpr():
    """Principles, lawful bases and rights, in the three groups that matter."""
    body = [text(380, 24, "The UK GDPR, in the three lists you need", 12, 650,
                 fill=MUTED)]
    PRINCIPLES = ["Lawfulness, fairness, transparency", "Purpose limitation",
                  "Data minimisation", "Accuracy", "Storage limitation",
                  "Integrity and confidentiality", "Accountability"]
    BASES = ["Consent", "Contract", "Legal obligation", "Vital interests",
             "Public task", "Legitimate interests"]
    RIGHTS = ["Access", "Rectification", "Erasure", "Restriction",
              "Portability", "Object", "Automated decisions"]

    def column(x, title, items, tone, soft, note):
        out = [box(x, 46, 230, 332, None, fill=soft, stroke=tone, r=10),
               text(x + 115, 70, title, 11.5, 750, fill=tone)]
        for i, t in enumerate(items):
            y = 86 + i * 36
            out.append(box(x + 14, y, 202, 30, None, fill=FILL, stroke=tone,
                           r=5))
            out.append(text(x + 115, y + 20,
                            t if len(t) < 30 else t[:28] + "…",
                            9.6, 550, fill="var(--dg-text)"))
        out.append(text(x + 115, 366, note, 9.6, 600, fill=tone))
        return "".join(out)

    body.append(column(24, "SEVEN PRINCIPLES", PRINCIPLES, TEAL, TEAL_SOFT,
                       "every one applies, always"))
    body.append(column(265, "SIX LAWFUL BASES", BASES, LILAC, LILAC_SOFT,
                       "you need exactly one"))
    body.append(column(506, "RIGHTS OF THE INDIVIDUAL", RIGHTS, WARN, WARN_SOFT,
                       "answer within one month"))
    body.append(box(24, 390, 712, 54, None, fill=FILL, stroke=LINE, r=8))
    body.append(text(380, 410, "Special category data (health, race, religion, "
                     "biometrics, sexual orientation) needs a condition as well "
                     "as a basis.", 10.5, 650, fill=MUTED))
    body.append(text(380, 428, "A reportable breach goes to the ICO within 72 "
                     "hours. Inferred data counts: inference is processing.",
                     10.5, 650, fill=WARN))
    desc = ("The UK GDPR summarised in three lists. The seven principles, all of "
            "which always apply: lawfulness, fairness and transparency; purpose "
            "limitation; data minimisation; accuracy; storage limitation; "
            "integrity and confidentiality; and accountability. The six lawful "
            "bases, of which exactly one is needed for any processing: consent, "
            "contract, legal obligation, vital interests, public task and "
            "legitimate interests. The rights of the individual, which must be "
            "answered within one month: access, rectification, erasure, "
            "restriction of processing, portability, the right to object, and "
            "rights relating to solely automated decisions. Two further points sit "
            "underneath. Special category data, covering health, racial or ethnic "
            "origin, religion, biometrics and sexual orientation, needs an "
            "additional condition as well as a lawful basis. And a reportable "
            "personal data breach must be notified to the Information "
            "Commissioner's Office within seventy two hours; inferred data counts "
            "as personal data, because generating an inference is itself "
            "processing.")
    return figure("data-gdpr", 760, 456, "".join(body),
                  "The UK GDPR principles, lawful bases and rights", desc,
                  "One lawful basis, seven principles, and a month to answer a "
                  "request. Those three facts answer most questions.")


# ============================================== F200: anonymisation

@diagram("data-anonymisation")
def _anon():
    """Removing the name does not anonymise anything, shown in three steps."""
    base = [text(380, 24, "Removing the name is not anonymisation", 12, 650,
                 fill=MUTED)]
    COLS = [(70, 150, "name"), (220, 130, "date of birth"),
            (350, 120, "postcode"), (470, 100, "sex"), (570, 120, "diagnosis")]

    def table(rows, hide=()):
        out = []
        for x, w, label in COLS:
            tone = WARN if label in hide else TEAL
            out.append(box(x, 70, w, 26, None,
                           fill=WARN_SOFT if label in hide else TEAL_SOFT,
                           stroke=tone, r=4))
            out.append(text(x + w / 2, 88, label, 9.8, 700, fill=tone))
        for r, row in enumerate(rows):
            y = 100 + r * 28
            for (x, w, label), val in zip(COLS, row):
                shown = "—" if label in hide else val
                out.append(box(x, y, w, 26, None, fill=FILL, stroke=LINE, r=4))
                out.append(text(x + w / 2, y + 18, shown, 9.6, 450,
                                fill=MUTED if label in hide
                                else "var(--dg-text)"))
        return "".join(out)

    ROWS = [("A. Shah", "14/03/1987", "LS6 2QB", "F", "Type 2 diabetes"),
            ("L. Okafor", "02/11/1994", "LS6 2QB", "M", "Asthma"),
            ("M. Price", "27/07/1961", "LS2 9JT", "F", "Hypertension")]

    L = ["The raw record: obviously identifying, and obviously sensitive.",
         "Delete the name. It feels anonymous, and it is not.",
         "Those three ordinary fields together identify almost anyone.",
         "Real anonymisation generalises, suppresses, or adds noise."]
    steps = [
        step(1, table(ROWS) + text(380, 212,
                                   "Name, date of birth, postcode, sex, diagnosis",
                                   11, 600, fill=MUTED), L[0]),
        step(2, table(ROWS, hide=("name",))
             + text(380, 212, "The name is gone. The record is not anonymous.",
                    11, 600, fill=WARN), L[1]),
        step(3, table(ROWS, hide=("name",))
             + box(220, 62, 350, 128, None, fill="none", stroke=WARN, r=8,
                   dash="5 4")
             + text(380, 212, "Date of birth + postcode + sex identifies the "
                    "large majority of the UK population.", 11, 650, fill=WARN),
             L[2]),
        step(4, text(380, 212, "So you generalise, suppress or add noise — "
                     "and lose some precision on purpose.", 11, 650, fill=TEAL),
             L[3]),
    ]
    FIX = [("Generalise", "1987 instead of 14/03/1987; LS6 instead of LS6 2QB"),
           ("Aggregate", "report counts by ward, not individual records"),
           ("Suppress", "hide any cell with fewer than five people in it"),
           ("Add noise", "differential privacy: deliberate, measured randomness"),
           ("Pseudonymise", "a study ID, key held separately — still "
            "personal data")]
    for i, (k, v) in enumerate(FIX):
        y = 236 + i * 26
        base.append(box(70, y, 620, 22, None,
                        fill=FILL2 if i % 2 == 0 else FILL, stroke="none", r=4))
        base.append(text(84, y + 15, k, 10, 700, anchor="start", fill=TEAL))
        base.append(text(220, y + 15, v, 10, 450, anchor="start", fill=MUTED))
    desc = ("Three patient records shown with name, date of birth, postcode, sex "
            "and diagnosis. Deleting the name column leaves a table that feels "
            "anonymous and is not: date of birth, postcode and sex together "
            "identify the large majority of the UK population, so the diagnosis is "
            "still attributable to an individual by anyone holding or able to "
            "obtain those three ordinary fields. Genuine anonymisation therefore "
            "has to reduce precision deliberately. Generalisation replaces the "
            "full date of birth with the year and the full postcode with its "
            "district. Aggregation reports counts by ward rather than individual "
            "records. Suppression hides any cell containing fewer than a minimum "
            "number of people. Adding noise, as in differential privacy, "
            "introduces measured randomness that protects individuals while "
            "preserving overall statistics. Pseudonymisation, replacing the name "
            "with a study identifier whose key is held separately, is useful but "
            "is not anonymisation at all: the data remains personal data and the "
            "whole of data protection law continues to apply to it.")
    return figure_steps("data-anon", 760, 376, "".join(base), steps,
                        "Why deleting the name is not anonymisation", desc,
                        "Date of birth, postcode and sex. Three ordinary fields, "
                        "and almost everybody is identifiable.", labels=L)


# ==================================================== F200: choosing a chart

@diagram("data-chart-choice")
def _charts():
    """Six charts drawn small, each labelled with what it is actually for."""
    body = [text(380, 24, "Six charts, and the one question each answers",
                 12, 650, fill=MUTED)]
    CW, CH = 228, 150

    def frame(col, row, title, answers, wrong, art):
        x = 32 + col * (CW + 14)
        y = 46 + row * (CH + 72)
        out = [box(x, y, CW, CH, None, fill=FILL, stroke=LINE, r=8),
               art(x, y),
               text(x + CW / 2, y + CH + 20, title, 11.5, 750, fill=TEAL),
               text(x + CW / 2, y + CH + 36, answers, 9.6, 500, fill=MUTED),
               text(x + CW / 2, y + CH + 52, "not for: " + wrong, 9.4, 450,
                    fill=WARN)]
        return "".join(out)

    def bars(x, y):
        out = []
        for i, h in enumerate((48, 86, 64, 104, 36)):
            out.append('<rect x="%d" y="%d" width="26" height="%d" rx="2" '
                       'fill="%s" stroke="%s"/>'
                       % (x + 22 + i * 38, y + CH - 18 - h, h, TEAL_SOFT, TEAL))
        out.append(line(x + 14, y + CH - 18, x + CW - 14, y + CH - 18,
                        stroke=LINE, w=1.4))
        return "".join(out)

    def lines(x, y):
        pts = [(0, 0.25), (0.2, 0.42), (0.4, 0.36), (0.6, 0.62), (0.8, 0.74),
               (1.0, 0.92)]
        d = " ".join(("M" if i == 0 else "L") + "%.1f %.1f"
                     % (x + 18 + p[0] * (CW - 40), y + CH - 18 - p[1] * 104)
                     for i, p in enumerate(pts))
        return (line(x + 14, y + CH - 18, x + CW - 14, y + CH - 18,
                     stroke=LINE, w=1.4)
                + path(d, stroke=TEAL, w=2.6))

    def scat(x, y):
        nxt = _rng(11)
        out = [line(x + 14, y + CH - 18, x + CW - 14, y + CH - 18, stroke=LINE,
                    w=1.4),
               line(x + 20, y + 14, x + 20, y + CH - 18, stroke=LINE, w=1.4)]
        for _ in range(26):
            a = nxt()
            b = 0.15 + 0.7 * a + (nxt() - 0.5) * 0.3
            out.append(circle(x + 24 + a * (CW - 48),
                              y + CH - 20 - min(max(b, 0.02), 0.98) * 100,
                              3.4, fill=LILAC, stroke=LILAC, w=0))
        return "".join(out)

    def hist(x, y):
        out = [line(x + 14, y + CH - 18, x + CW - 14, y + CH - 18, stroke=LINE,
                    w=1.4)]
        for i, h in enumerate((14, 38, 76, 98, 70, 44, 26, 14)):
            out.append('<rect x="%d" y="%d" width="23" height="%d" '
                       'fill="%s" stroke="%s"/>'
                       % (x + 20 + i * 24, y + CH - 18 - h, h, LILAC_SOFT,
                          LILAC))
        return "".join(out)

    def stack(x, y):
        out = [line(x + 14, y + CH - 18, x + CW - 14, y + CH - 18, stroke=LINE,
                    w=1.4)]
        for i, parts in enumerate(((40, 34, 20), (52, 26, 16), (30, 48, 22),
                                   (44, 30, 30))):
            base_y = y + CH - 18
            for j, h in enumerate(parts):
                col = (TEAL_SOFT, LILAC_SOFT, WARN_SOFT)[j]
                edge = (TEAL, LILAC, WARN)[j]
                out.append('<rect x="%d" y="%d" width="32" height="%d" '
                           'fill="%s" stroke="%s"/>'
                           % (x + 26 + i * 46, base_y - h, h, col, edge))
                base_y -= h
        return "".join(out)

    def boxp(x, y):
        out = [line(x + 14, y + CH - 18, x + CW - 14, y + CH - 18, stroke=LINE,
                    w=1.4)]
        for i, (lo, q1, med, q3, hi) in enumerate(
                ((14, 34, 52, 72, 96), (22, 42, 56, 66, 82),
                 (10, 28, 40, 58, 104))):
            cx = x + 48 + i * 58
            b = y + CH - 18
            out.append(line(cx, b - lo, cx, b - hi, stroke=TEAL, w=1.4))
            out.append('<rect x="%d" y="%d" width="28" height="%d" rx="2" '
                       'fill="%s" stroke="%s"/>'
                       % (cx - 14, b - q3, q3 - q1, TEAL_SOFT, TEAL))
            out.append(line(cx - 14, b - med, cx + 14, b - med, stroke=TEAL,
                            w=2.4))
        out.append(circle(x + 48 + 2 * 58, y + CH - 18 - 126, 3.6, fill=WARN,
                          stroke=WARN, w=0))
        return "".join(out)

    body.append(frame(0, 0, "Bar chart", "comparing categories",
                      "a trend over many points", bars))
    body.append(frame(1, 0, "Line chart", "change over time",
                      "unordered categories", lines))
    body.append(frame(2, 0, "Scatter plot", "relationship between two numbers",
                      "categories", scat))
    body.append(frame(0, 1, "Histogram", "the distribution of one variable",
                      "comparing categories", hist))
    body.append(frame(1, 1, "Stacked bar", "composition within a total",
                      "comparing middle segments", stack))
    body.append(frame(2, 1, "Box plot", "spread and outliers across groups",
                      "an audience you cannot explain it to", boxp))
    body.append(box(32, 492, 696, 44, None, fill=WARN_SOFT, stroke=WARN, r=8))
    body.append(text(380, 511, "And the pie chart: one part against a whole, "
                     "with at most about four slices.", 11, 700, fill=WARN))
    body.append(text(380, 528, "People compare angles badly, so almost any "
                     "comparison is clearer as a bar chart.", 10, 500,
                     fill=MUTED))
    desc = ("Six chart types drawn small, each labelled with the question it "
            "answers and the job it should not be used for. A bar chart compares "
            "categories and is wrong for a trend over many points. A line chart "
            "shows change over time and is wrong for unordered categories. A "
            "scatter plot shows the relationship between two numeric variables and "
            "is wrong for categorical data. A histogram shows the distribution of a "
            "single numeric variable and is not a way of comparing categories. A "
            "stacked bar shows composition within a total but makes the middle "
            "segments impossible to compare precisely. A box plot shows spread, "
            "median and outliers across groups, and should not be put in front of "
            "an audience it cannot be explained to. The pie chart is for one part "
            "against a whole with at most about four slices, because people compare "
            "angles badly and almost any comparison is clearer as a bar chart.")
    return figure("data-charts", 760, 548, "".join(body),
                  "Choosing the right chart", desc,
                  "If the chart needs a paragraph to interpret, it is the wrong "
                  "chart.")


# ============================================================ F201: the five Vs

@diagram("data-five-vs")
def _five_vs():
    """Each V, and the conventional tool it breaks."""
    body = [text(380, 24, "Each characteristic breaks something different",
                 12, 650, fill=MUTED)]
    VS = [("VOLUME", "terabytes to petabytes, growing",
           "breaks single machine storage and processing", TEAL),
          ("VELOCITY", "arriving continuously, needing a fast answer",
           "breaks nightly batch processing", LILAC),
          ("VARIETY", "structured, semi-structured and unstructured together",
           "breaks a fixed relational schema", TEAL),
          ("VERACITY", "noise, gaps, duplicates, bias",
           "breaks the assumption that stored data is correct", LILAC),
          ("VALUE", "worth that has to be extracted deliberately",
           "breaks the idea that collecting equals benefiting", TEAL)]
    for i, (name, what, breaks, tone) in enumerate(VS):
        y = 50 + i * 66
        body.append(box(28, y, 150, 54, None,
                        fill=TEAL_SOFT if tone == TEAL else LILAC_SOFT,
                        stroke=tone, r=8))
        body.append(text(103, y + 32, name, 12.5, 780, fill=tone))
        body.append(box(190, y, 272, 54, None, fill=FILL, stroke=LINE, r=8))
        body.append(text(326, y + 31, what, 10, 500, fill="var(--dg-text)"))
        body.append(line(468, y + 27, 492, y + 27, stroke=tone, w=1.8,
                         arrow=True))
        body.append(box(498, y, 234, 54, None, fill=WARN_SOFT, stroke=WARN, r=8))
        body.append(text(615, y + 31, breaks, 9.8, 600, fill=WARN))
    body.append(box(28, 388, 704, 50, None, fill=FILL, stroke=TEAL, r=8))
    body.append(text(380, 408, "The working definition: data whose volume, "
                     "velocity or variety prevents processing by conventional "
                     "single-machine methods.", 10.8, 700, fill=TEAL))
    body.append(text(380, 426, "Which is why distributed storage and distributed "
                     "processing are not optional extras but the definition.",
                     10, 500, fill=MUTED))
    desc = ("The five characteristics of big data, each paired with the "
            "conventional approach it breaks. Volume, terabytes to petabytes and "
            "growing, breaks single machine storage and processing. Velocity, data "
            "arriving continuously and needing a fast answer, breaks nightly batch "
            "processing. Variety, structured, semi-structured and unstructured data "
            "held together, breaks a fixed relational schema. Veracity, meaning "
            "noise, gaps, duplicates and bias, breaks the assumption that stored "
            "data is correct. Value, the worth that has to be extracted "
            "deliberately, breaks the idea that collecting data is the same as "
            "benefiting from it. Taken together they give the working definition: "
            "big data is data whose volume, velocity or variety prevents "
            "processing by conventional single-machine methods, which is why "
            "distributed storage and distributed processing are part of the "
            "definition rather than an optional extra.")
    return figure("data-vs", 760, 450, "".join(body),
                  "The five Vs of big data", desc,
                  "Define big data by what it breaks, not by how large it is.")


# =========================================== F201: scaling and moving the work

@diagram("data-scaling")
def _scaling():
    """Scale up, scale out, and why the computation goes to the data."""
    base = [text(380, 24, "Three ideas, in the order you need them", 12, 650,
                 fill=MUTED)]

    def server(x, y, w, h, label, tone, soft):
        return (box(x, y, w, h, None, fill=soft, stroke=tone, r=6)
                + text(x + w / 2, y + h / 2 + 4, label, 10, 650, fill=tone))

    # 1. Scaling up.
    up = [text(380, 56, "SCALING UP: one bigger machine", 12, 750, fill=TEAL)]
    for i, (w, h, lab) in enumerate([(70, 40, "4 cores"), (100, 60, "16 cores"),
                                     (140, 90, "64 cores")]):
        x = 110 + i * 190
        up.append(server(x, 200 - h, w, h, lab, TEAL, TEAL_SOFT))
        if i < 2:
            up.append(line(x + w + 10, 180, x + 180, 180, stroke=LINE,
                           arrow=True))
    up.append(box(110, 222, 540, 44, None, fill=WARN_SOFT, stroke=WARN, r=8))
    up.append(text(380, 242, "Simple, and it stops. There is a largest machine, "
                   "and no budget moves that ceiling.", 10.5, 650, fill=WARN))
    up.append(text(380, 258, "Big data begins at the point where this stopped "
                   "working.", 10, 500, fill=MUTED))

    # 2. Scaling out.
    out = [text(380, 56, "SCALING OUT: more machines, working together",
                12, 750, fill=LILAC)]
    for i in range(8):
        x = 96 + (i % 4) * 140
        y = 90 + (i // 4) * 62
        out.append(server(x, y, 110, 46, "node %d" % (i + 1), LILAC,
                          LILAC_SOFT))
    out.append(box(96, 222, 568, 44, None, fill=FILL, stroke=LILAC, r=8))
    out.append(text(380, 242, "Partitioned for parallel work, replicated so a "
                    "failure loses nothing.", 10.5, 650, fill=LILAC))
    out.append(text(380, 258, "The cost is consistency: replicas can briefly "
                    "disagree, which is eventual consistency.", 10, 500,
                    fill=MUTED))

    # 3. Move the computation.
    mv = [text(380, 56, "MOVE THE COMPUTATION TO THE DATA", 12, 750, fill=TEAL)]
    for i in range(4):
        x = 96 + i * 140
        mv.append(server(x, 92, 110, 58, "", TEAL, TEAL_SOFT))
        mv.append(text(x + 55, 114, "block %d" % (i + 1), 9.6, 600, fill=TEAL))
        mv.append(text(x + 55, 130, "250 TB", 9, 450, fill=MUTED))
        mv.append(chip(x + 55, 172, "count locally", fill=FILL, stroke=TEAL,
                       text_fill=TEAL))
        mv.append(line(x + 55, 186, x + 55, 198, stroke=TEAL, w=1.4,
                       arrow=True))
    mv.append(box(240, 202, 280, 36, None, fill=LILAC_SOFT, stroke=LILAC, r=8))
    mv.append(text(380, 224, "combine 4 small results", 10.5, 700, fill=LILAC))
    mv.append(text(380, 258, "One petabyte never moves. A few kilobytes come "
                   "back. That is the whole idea.", 10.5, 650, fill=MUTED))

    L = ["Scaling up: a bigger machine, until there isn't one.",
         "Scaling out: many machines, partitioned and replicated.",
         "And then send the query to the data, not the data to the query."]
    steps = [step(1, "".join(up), L[0]), step(2, "".join(out), L[1]),
             step(3, "".join(mv), L[2])]
    desc = ("Three ideas in sequence. Scaling up means replacing a machine with a "
            "bigger one, from four cores to sixteen to sixty four; it is simple and "
            "it stops, because there is a largest available machine and no budget "
            "moves that ceiling, and big data begins precisely where this "
            "approach failed. Scaling out means using many machines together as a "
            "cluster, with the data partitioned across them so work can run in "
            "parallel and replicated so that a machine failing loses nothing; the "
            "cost is consistency, because replicas can briefly disagree, which is "
            "what eventual consistency means. The third idea follows from the "
            "second: rather than pulling a petabyte to an analysis machine, the "
            "query is sent to the four machines that already hold the blocks, each "
            "counts its own quarter locally, and only the four small results are "
            "combined. The petabyte never moves and a few kilobytes come back, "
            "which is the organising principle of every distributed processing "
            "framework.")
    return figure_steps("data-scale", 760, 286, "".join(base), steps,
                        "Scaling up, scaling out, and moving the computation",
                        desc,
                        "Moving data is usually the binding constraint. The fix "
                        "is to not move it.", labels=L)


# ============================================= F201: types of machine learning

@diagram("data-ml-types")
def _ml_types():
    """Three kinds of learning, by what each one is given."""
    body = [text(380, 24, "Three kinds of learning, told apart by the input",
                 12, 650, fill=MUTED)]
    KINDS = [
        ("SUPERVISED", TEAL, TEAL_SOFT,
         "labelled examples: input + the right answer",
         "learns to predict the label for new data",
         ["Classification: spam or not, which digit, will churn",
          "Regression: a price, a demand, a time to failure"],
         "Spam filter, credit scoring, image diagnosis"),
        ("UNSUPERVISED", LILAC, LILAC_SOFT,
         "unlabelled data: no answers at all",
         "finds structure nobody specified",
         ["Clustering: groups of similar records",
          "Anomaly detection: records unlike the rest"],
         "Customer segmentation, fraud and fault detection"),
        ("REINFORCEMENT", WARN, WARN_SOFT,
         "an environment, actions, and a reward signal",
         "learns a policy that maximises long run reward",
         ["Trial and error, with delayed consequences",
          "No dataset: the data is generated by acting"],
         "Game playing, robotics, routing, energy control"),
    ]
    for i, (name, tone, soft, given, learns, tasks, apps) in enumerate(KINDS):
        y = 46 + i * 138
        body.append(box(28, y, 704, 126, None, fill=soft, stroke=tone, r=10))
        body.append(text(44, y + 26, name, 12, 780, anchor="start", fill=tone))
        body.append(box(180, y + 10, 266, 44, None, fill=FILL, stroke=tone, r=6))
        body.append(text(313, y + 28, "GIVEN", 9, 700, fill=tone))
        body.append(text(313, y + 44, given, 9.6, 450, fill=MUTED))
        body.append(line(452, y + 32, 472, y + 32, stroke=tone, arrow=True))
        body.append(box(478, y + 10, 240, 44, None, fill=FILL, stroke=tone, r=6))
        body.append(text(598, y + 28, "LEARNS", 9, 700, fill=tone))
        body.append(text(598, y + 44, learns, 9.6, 450, fill=MUTED))
        for j, t in enumerate(tasks):
            body.append(text(44, y + 76 + j * 17, "• " + t, 9.8, 450,
                             anchor="start", fill="var(--dg-text)"))
        body.append(box(430, y + 64, 288, 50, None, fill=FILL, stroke=tone, r=6))
        body.append(text(574, y + 84, "IN PRACTICE", 9, 700, fill=tone))
        body.append(text(574, y + 101, apps, 9.6, 500, fill=MUTED))
    desc = ("The three kinds of machine learning, distinguished by what each one "
            "is given. Supervised learning is given labelled examples, each input "
            "paired with the right answer, and learns to predict that label for "
            "new data; its two tasks are classification, predicting a category "
            "such as spam or not spam, and regression, predicting a number such as "
            "a price or a time to failure, with practical uses including spam "
            "filtering, credit scoring and image diagnosis. Unsupervised learning "
            "is given unlabelled data with no answers at all and finds structure "
            "nobody specified; its tasks include clustering, which groups similar "
            "records, and anomaly detection, which finds records unlike the rest, "
            "with practical uses including customer segmentation and fraud or "
            "fault detection. Reinforcement learning is given an environment, a "
            "set of possible actions and a reward signal, and learns a policy of "
            "actions that maximises long run reward through trial and error with "
            "delayed consequences; it has no fixed dataset, because the data is "
            "generated by acting, and it is used in game playing, robotics, "
            "routing and energy control.")
    return figure("data-mltypes", 760, 442, "".join(body),
                  "Supervised, unsupervised and reinforcement learning", desc,
                  "The question that tells them apart is simple: what was the "
                  "model given?")


# ======================================== F201: training, validation and test

@diagram("data-ml-workflow")
def _ml_workflow():
    """The split, the training loop, and why the test set is used once."""
    base = [text(380, 24, "How a model is actually trained and judged", 12, 650,
                 fill=MUTED)]
    # The split bar.
    base.append(text(380, 56, "THE SPLIT", 11, 750, fill=MUTED))
    SPLIT = [(0.70, "TRAINING  70%", "the model learns from this", TEAL,
              TEAL_SOFT),
             (0.15, "VALIDATION", "tuning and comparison", LILAC, LILAC_SOFT),
             (0.15, "TEST", "used once, at the end", WARN, WARN_SOFT)]
    x = 60
    for frac, label, note, tone, soft in SPLIT:
        w = 640 * frac
        base.append(box(x, 68, w - 4, 46, None, fill=soft, stroke=tone, r=6))
        base.append(text(x + w / 2 - 2, 90, label, 10.5, 750, fill=tone))
        base.append(text(x + w / 2 - 2, 105, note, 8.8, 450, fill=MUTED))
        x += w
    L = ["Split the data first, before looking at any of it.",
         "Train: the model adjusts itself to reduce its error on the training set.",
         "Validate: compare options and tune, using data it did not learn from.",
         "Test once, at the very end, to estimate how it will really perform.",
         "Deploy, then monitor: the world changes and the model drifts."]
    steps = []
    steps.append(step(1, box(56, 64, 648, 54, None, fill="none", stroke=TEAL,
                             r=8)
                      + text(380, 300, "Split before you explore. Anything you "
                             "learn from the test set leaks into the model.",
                             11, 650, fill=TEAL), L[0]))
    # The training loop.
    loop = [box(120, 146, 160, 48, None, fill=TEAL_SOFT, stroke=TEAL, r=8),
            text(200, 176, "predict", 11, 700, fill=TEAL),
            box(320, 146, 160, 48, None, fill=FILL, stroke=TEAL, r=8),
            text(400, 170, "measure the error", 10, 700, fill="var(--dg-text)"),
            text(400, 185, "against the labels", 9, 450, fill=MUTED),
            box(520, 146, 160, 48, None, fill=TEAL_SOFT, stroke=TEAL, r=8),
            text(600, 170, "adjust", 11, 700, fill=TEAL),
            text(600, 185, "the parameters", 9, 450, fill=MUTED),
            line(286, 170, 314, 170, stroke=TEAL, arrow=True),
            line(486, 170, 514, 170, stroke=TEAL, arrow=True),
            path("M600 194 L600 216 L200 216 L200 198", stroke=TEAL, w=1.8,
                 arrow=True),
            text(400, 232, "repeat, thousands of times", 9.6, 600, fill=MUTED)]
    steps.append(step(2, "".join(loop)
                      + text(380, 300, "Training is this loop: predict, measure "
                             "the error, adjust, repeat.", 11, 650, fill=TEAL),
                      L[1]))
    steps.append(step(3, box(60 + 640 * 0.70, 64, 640 * 0.15 - 4, 54, None,
                             fill="none", stroke=LILAC, r=8)
                      + text(380, 300, "Validation picks between models and "
                             "settings. Use it as often as you like.", 11, 650,
                             fill=LILAC), L[2]))
    steps.append(step(4, box(60 + 640 * 0.85, 64, 640 * 0.15 - 4, 54, None,
                             fill="none", stroke=WARN, r=8)
                      + text(380, 300, "Test once. Tune against the test set and "
                             "it becomes training data and tells you nothing.",
                             11, 650, fill=WARN), L[3]))
    steps.append(step(5, box(200, 250, 360, 36, None, fill=WARN_SOFT,
                             stroke=WARN, r=8)
                      + text(380, 273, "monitor for drift, and retrain", 10.5,
                             700, fill=WARN)
                      + text(380, 300, "A deployed model decays, because the "
                             "world it was trained on keeps moving.", 11, 650,
                             fill=WARN), L[4]))
    desc = ("How a supervised model is trained and judged. The data is split "
            "first, typically seventy per cent for training, which the model learns "
            "from, fifteen per cent for validation, used for tuning and comparing "
            "options, and fifteen per cent held back as a test set to be used once "
            "at the very end. The split happens before any exploration, because "
            "anything learned from the test set leaks into the model. Training "
            "itself is a loop: the model predicts, the error is measured against "
            "the known labels, the parameters are adjusted to reduce it, and the "
            "cycle repeats thousands of times. Validation data can be consulted as "
            "often as needed, since it is not learned from directly, and it is how "
            "model types and settings are chosen. The test set is used exactly "
            "once, because tuning against it turns it into training data and its "
            "estimate of real performance becomes worthless. After deployment the "
            "model must be monitored for drift and retrained, because the world it "
            "was trained on keeps changing.")
    return figure_steps("data-mlflow", 760, 316, "".join(base), steps,
                        "Training, validation, test and monitoring", desc,
                        "The test set is used once. That single rule is what "
                        "makes a performance figure mean anything.", labels=L)


# =================================================== F201: the confusion matrix

@diagram("data-confusion-matrix")
def _confusion():
    """The four cells, with one worked example carried right through."""
    TP, FP, FN, TN = 180, 20, 40, 760
    total = TP + FP + FN + TN
    acc = (TP + TN) / float(total) * 100
    prec = TP / float(TP + FP) * 100
    rec = TP / float(TP + FN) * 100
    f1 = 2 * prec * rec / (prec + rec)

    body = [text(380, 24, "1,000 emails through a spam filter", 12, 650,
                 fill=MUTED)]
    CX, CY, CW, CH = 240, 76, 200, 86
    body.append(text(CX + CW / 2, 62, "PREDICTED SPAM", 10, 700, fill=MUTED))
    body.append(text(CX + CW + CW / 2, 62, "PREDICTED NOT SPAM", 10, 700,
                     fill=MUTED))
    body.append('<text x="%d" y="%d" text-anchor="middle" font-size="10" '
                'font-weight="700" fill="%s" transform="rotate(-90 %d %d)">'
                'ACTUALLY SPAM</text>' % (CX - 22, CY + CH / 2, MUTED, CX - 22,
                                          CY + CH / 2))
    body.append('<text x="%d" y="%d" text-anchor="middle" font-size="10" '
                'font-weight="700" fill="%s" transform="rotate(-90 %d %d)">'
                'ACTUALLY NOT SPAM</text>' % (CX - 22, CY + CH * 1.5, MUTED,
                                              CX - 22, CY + CH * 1.5))
    CELLS = [(0, 0, "TRUE POSITIVE", TP, "caught spam", TEAL, TEAL_SOFT),
             (1, 0, "FALSE NEGATIVE", FN, "spam that got through", WARN,
              WARN_SOFT),
             (0, 1, "FALSE POSITIVE", FP, "real email wrongly blocked", WARN,
              WARN_SOFT),
             (1, 1, "TRUE NEGATIVE", TN, "correctly delivered", TEAL,
              TEAL_SOFT)]
    for col, row, name, n, note, tone, soft in CELLS:
        x, y = CX + col * CW, CY + row * CH
        body.append(box(x, y, CW - 4, CH - 4, None, fill=soft, stroke=tone, r=6))
        body.append(text(x + CW / 2 - 2, y + 22, name, 9.4, 750, fill=tone))
        body.append(text(x + CW / 2 - 2, y + 50, str(n), 22, 800, fill=tone))
        body.append(text(x + CW / 2 - 2, y + 68, note, 8.8, 450, fill=MUTED))

    MEASURES = [
        ("ACCURACY", "(TP + TN) / all", "(180 + 760) / 1000", "%.0f%%" % acc,
         "right overall", TEAL),
        ("PRECISION", "TP / (TP + FP)", "180 / 200", "%.0f%%" % prec,
         "when it says spam, how often right", TEAL),
        ("RECALL", "TP / (TP + FN)", "180 / 220", "%.0f%%" % rec,
         "of the real spam, how much found", LILAC),
        ("F1 SCORE", "harmonic mean", "of 90 and 82", "%.0f%%" % f1,
         "one figure balancing both", LILAC),
    ]
    for i, (name, formula, sub, val, note, tone) in enumerate(MEASURES):
        y = 268 + i * 44
        body.append(box(28, y, 150, 38, None,
                        fill=TEAL_SOFT if tone == TEAL else LILAC_SOFT,
                        stroke=tone, r=6))
        body.append(text(103, y + 24, name, 11, 750, fill=tone))
        body.append(text(200, y + 24, formula, 10.5, 600, anchor="start",
                         fill="var(--dg-text)", mono=True))
        body.append(text(390, y + 24, "=  " + sub, 10.5, 450, anchor="start",
                         fill=MUTED, mono=True))
        body.append(box(530, y, 76, 38, None, fill=FILL, stroke=tone, r=6))
        body.append(text(568, y + 24, val, 13, 780, fill=tone))
        body.append(text(620, y + 24, note, 9.2, 450, anchor="start",
                         fill=MUTED))
    body.append(box(28, 448, 704, 58, None, fill=WARN_SOFT, stroke=WARN, r=8))
    body.append(text(380, 468, "A filter that marked nothing as spam would score "
                     "78% accuracy and catch nothing at all.", 11, 700,
                     fill=WARN))
    body.append(text(380, 486, "On an imbalanced problem accuracy measures the "
                     "imbalance. Always report precision and recall.", 10, 500,
                     fill=MUTED))
    desc = ("A confusion matrix for a spam filter tested on one thousand emails. "
            "The four cells: 180 true positives, spam correctly caught; 40 false "
            "negatives, spam that got through; 20 false positives, real emails "
            "wrongly blocked; and 760 true negatives, legitimate mail correctly "
            "delivered. Four measures follow. Accuracy is true positives plus true "
            "negatives over the total, 180 plus 760 over 1000, which is 94 per "
            "cent. Precision is true positives over all predicted positives, 180 "
            "over 200, which is 90 per cent, and answers how often the filter is "
            "right when it declares something spam. Recall is true positives over "
            "all actual positives, 180 over 220, which is about 82 per cent, and "
            "answers how much of the real spam the filter found. The F1 score is "
            "the harmonic mean of precision and recall, about 86 per cent, giving "
            "one figure that balances the two. The warning underneath is the "
            "important part: a filter that simply marked nothing as spam would "
            "score 78 per cent accuracy on this same test while catching nothing "
            "at all, because on an imbalanced problem accuracy largely measures "
            "the imbalance, which is why precision and recall are always reported "
            "together.")
    return figure("data-conf", 760, 518, "".join(body),
                  "A confusion matrix with precision and recall worked through",
                  desc,
                  "Learn these four numbers and the four formulas. It is the "
                  "most reliable question in the unit.")


# ================================================= F201: overfitting, plotted

@diagram("data-overfitting")
def _overfitting():
    """Underfit, good fit and overfit, drawn over the same points."""
    base = [text(380, 24, "The same twenty points, three models", 12, 650,
                 fill=MUTED)]
    X0, Y0, W, H = 110, 290, 560, 220
    # A gentle rising curve with noise. Fixed, so the figure never changes.
    # An S shaped underlying relationship, so that a straight line is visibly
    # the wrong shape rather than merely a slightly worse one.
    def true_curve(t):
        # Kept clear of the top and bottom of the plot so that the straight
        # line fitted to it is not clipped into a shape of its own.
        return 0.17 + 0.66 / (1.0 + math.exp(-10.0 * (t - 0.5)))

    nxt = _rng(5)
    PTS = []
    for i in range(20):
        x = (i + 0.5) / 20.0
        PTS.append((x, min(max(true_curve(x) + (nxt() - 0.5) * 0.15, 0.04),
                           0.96)))
    base.append(axes(X0, Y0, W, H, "input", "output",
                     xticks=[(f, "") for f in (0.25, 0.5, 0.75, 1.0)],
                     yticks=[(f, "") for f in (0.25, 0.5, 0.75, 1.0)]))
    for x, y in PTS:
        base.append(circle(X0 + W * x, Y0 - H * y, 4.6, fill=FILL2,
                           stroke=MUTED, w=1.4))

    def curve(fn, tone, w=2.8):
        d = []
        for k in range(121):
            t = k / 120.0
            yv = min(max(fn(t), 0.02), 0.98)
            d.append(("M" if k == 0 else "L")
                     + "%.1f %.1f" % (X0 + W * t, Y0 - H * yv))
        return path(" ".join(d), stroke=tone, w=w)

    # A straight line: too simple.
    n = len(PTS)
    mx = sum(p[0] for p in PTS) / n
    my = sum(p[1] for p in PTS) / n
    m = (sum((p[0] - mx) * (p[1] - my) for p in PTS)
         / sum((p[0] - mx) ** 2 for p in PTS))
    c = my - m * mx
    # The real underlying shape: about right.
    good = true_curve
    # A curve that chases every point: too complex.
    def wiggly(t):
        v = good(t)
        for px, py in PTS:
            v += (py - good(px)) * math.exp(-((t - px) ** 2) / 0.0007)
        return v

    L = ["Underfitting: too simple to capture the real shape. Poor on everything.",
         "A good fit: it follows the pattern and ignores the noise.",
         "Overfitting: it passes through every point, including the noise.",
         "And on data it has never seen, the overfitted model is the worst of the three."]
    steps = [
        step(1, curve(lambda t: m * t + c, WARN)
             + chip(300, 72, "UNDERFIT: a straight line", fill=WARN_SOFT,
                    stroke=WARN, text_fill=WARN)
             + text(380, 344, "High error on the training data and on new data. "
                    "The model has too little capacity.", 10.8, 600, fill=WARN),
             L[0]),
        step(2, curve(good, TEAL)
             + chip(300, 72, "GOOD FIT: follows the pattern", fill=TEAL_SOFT,
                    stroke=TEAL, text_fill=TEAL)
             + text(380, 344, "Some error on the training data on purpose, "
                    "because the noise is not worth fitting.", 10.8, 600,
                    fill=TEAL),
             L[1]),
        step(3, curve(wiggly, LILAC, 2.2)
             + chip(300, 72, "OVERFIT: through every point", fill=LILAC_SOFT,
                    stroke=LILAC, text_fill=LILAC)
             + text(380, 344, "Near zero error on the training data, which is "
                    "exactly why it will fail on new data.", 10.8, 600,
                    fill=LILAC),
             L[2]),
        step(4, curve(wiggly, LILAC, 1.6) + curve(good, TEAL, 2.2)
             + circle(X0 + W * 0.62, Y0 - H * (good(0.62) + 0.17), 6,
                      fill=WARN, stroke=WARN, w=0)
             + chip(300, 72, "a new, unseen point", fill=WARN_SOFT, stroke=WARN,
                    text_fill=WARN)
             + text(380, 344, "Fix it with more data, a simpler model, or early "
                    "stopping on a validation set.", 10.8, 650, fill=MUTED),
             L[3]),
    ]
    desc = ("The same twenty noisy data points with three different models drawn "
            "over them. The underfitted model is a straight line: it is too simple "
            "to capture the gently curving shape of the data, so it has high error "
            "both on the training points and on anything new, because the model has "
            "too little capacity. The good fit is a smooth curve that follows the "
            "underlying pattern while passing between the points rather than "
            "through them; it accepts some error on the training data deliberately, "
            "because the noise is not worth fitting. The overfitted model is a "
            "wildly wiggling curve that passes through every single point, "
            "achieving almost zero error on the training data, and that is exactly "
            "why it fails on new data: it has learned the noise as though it were "
            "signal. A new unseen point lands far from the overfitted curve while "
            "sitting close to the good fit. Overfitting is reduced by training on "
            "more data, by using a simpler model with fewer features, and by "
            "stopping training when performance on a held-back validation set "
            "stops improving.")
    return figure_steps("data-overfit", 760, 360, "".join(base), steps,
                        "Underfitting, a good fit and overfitting", desc,
                        "A model with zero error on its training data has "
                        "usually memorised it rather than learned anything.",
                        labels=L)


# ========================================================= F201: bias

@diagram("data-bias-sources")
def _bias():
    """Where bias enters, and why dropping the protected field does not help."""
    body = [text(380, 24, "Bias enters at every stage, not just in the "
                 "algorithm", 12, 650, fill=MUTED)]
    STAGES = [("THE WORLD", "existing inequality", TEAL),
              ("COLLECTION", "who is in the data", LILAC),
              ("LABELS", "who decided the answers", TEAL),
              ("THE MODEL", "what it optimises", LILAC),
              ("DEPLOYMENT", "who it is used on", TEAL),
              ("FEEDBACK", "its output becomes tomorrow's data", WARN)]
    for i, (name, note, tone) in enumerate(STAGES):
        x = 24 + i * 120
        body.append(box(x, 48, 108, 56, None,
                        fill=TEAL_SOFT if tone == TEAL
                        else (LILAC_SOFT if tone == LILAC else WARN_SOFT),
                        stroke=tone, r=8))
        body.append(text(x + 54, 70, name, 9.6, 750, fill=tone))
        body.append(text(x + 54, 86, note, 8.4, 450, fill=MUTED))
        if i < 5:
            body.append(line(x + 110, 76, x + 120, 76, stroke=LINE, arrow=True))
    body.append(path("M78 104 L78 126 L684 126 L684 106", stroke=WARN, w=1.6,
                     dash="5 4", arrow=True))
    body.append(text(380, 142, "the feedback loop: the model's own decisions "
                     "become the next training set, and the bias compounds",
                     9.8, 600, fill=WARN))

    KINDS = [("Historic", "the data records past unfair human decisions"),
             ("Sampling", "a group is under-represented, so accuracy is lower "
              "for them"),
             ("Measurement", "the proxy is not the thing: arrests are not "
              "crime, clicks are not interest"),
             ("Label", "the labels carry the assumptions of whoever applied "
              "them"),
             ("Aggregation", "one model for groups that genuinely behave "
              "differently"),
             ("Deployment", "used on a population it was never trained for")]
    for i, (k, v) in enumerate(KINDS):
        y = 164 + i * 28
        body.append(box(28, y, 704, 24, None,
                        fill=FILL2 if i % 2 == 0 else FILL, stroke="none", r=4))
        body.append(text(44, y + 16, k, 10, 700, anchor="start", fill=WARN))
        body.append(text(170, y + 16, v, 10, 450, anchor="start", fill=MUTED))

    body.append(box(28, 340, 348, 92, None, fill=WARN_SOFT, stroke=WARN, r=8))
    body.append(text(202, 362, "DROPPING THE FIELD DOES NOT WORK", 10.5, 750,
                     fill=WARN))
    body.append(text(202, 382, "Postcode, school, first name and purchase",
                     9.8, 450, fill=MUTED))
    body.append(text(202, 397, "history all act as proxies, so a model can",
                     9.8, 450, fill=MUTED))
    body.append(text(202, 412, "discriminate without ever seeing the attribute.",
                     9.8, 450, fill=MUTED))
    body.append(box(384, 340, 348, 92, None, fill=TEAL_SOFT, stroke=TEAL, r=8))
    body.append(text(558, 362, "WHAT TO DO INSTEAD", 10.5, 750, fill=TEAL))
    body.append(text(558, 382, "Measure error rates per group, not just overall.",
                     9.8, 450, fill=MUTED))
    body.append(text(558, 397, "Recall 88% for one group and 61% for another",
                     9.8, 450, fill=MUTED))
    body.append(text(558, 412, "is a defect, whatever the headline figure says.",
                     9.8, 450, fill=MUTED))
    desc = ("Bias entering a machine learning system at every stage. It begins in "
            "the world, as existing inequality; passes into collection, through who "
            "is and is not in the data; into the labels, through whoever decided "
            "what the right answers were; into the model, through what it is set to "
            "optimise; into deployment, through who it is then used on; and finally "
            "into a feedback loop, where the model's own decisions become the next "
            "training set and the bias compounds. The named kinds are historic "
            "bias, where the data records past unfair human decisions; sampling "
            "bias, where a group is under-represented so accuracy is lower for "
            "them; measurement bias, where the chosen proxy is not the thing that "
            "matters, since arrests are not crime and clicks are not interest; "
            "label bias, where the labels carry the assumptions of whoever applied "
            "them; aggregation bias, where one model is used for groups that "
            "genuinely behave differently; and deployment bias, where a model is "
            "used on a population it was never trained for. Removing the protected "
            "characteristic from the feature list does not solve this, because "
            "postcode, school, first name and purchase history act as proxies, so a "
            "model can discriminate effectively without ever seeing the attribute. "
            "The workable approach is to measure error rates separately for each "
            "group: a recall of eighty eight per cent for one group and sixty one "
            "per cent for another is a defect, whatever the headline accuracy "
            "says.")
    return figure("data-bias", 760, 444, "".join(body),
                  "Where bias enters a machine learning system", desc,
                  "Removing the protected field removes your ability to measure "
                  "the bias, not the bias.")


# ======================================== F201: the environmental cost

@diagram("data-energy")
def _energy():
    """Where a data centre's power actually goes, and what PUE measures."""
    body = [text(380, 24, "Where a data centre's electricity goes", 12, 650,
                 fill=MUTED)]
    # Two stacked bars: a poor facility and an efficient one.
    def bar(y, label, pue, parts):
        out = [text(70, y + 28, label, 11.5, 750, anchor="start", fill=MUTED),
               text(70, y + 44, "PUE %.1f" % pue, 10, 600, anchor="start",
                    fill=TEAL if pue < 1.3 else WARN)]
        x = 200
        total = sum(p[1] for p in parts)
        for name, val, tone, soft in parts:
            w = 480 * val / float(total)
            out.append(box(x, y + 10, w - 2, 44, None, fill=soft, stroke=tone,
                           r=4))
            if w > 56:
                out.append(text(x + w / 2, y + 30, name, 9.6, 700, fill=tone))
                out.append(text(x + w / 2, y + 45, "%d%%"
                                % round(100.0 * val / total), 9, 500,
                                fill=MUTED))
            x += w
        return "".join(out)

    body.append(bar(50, "An older facility", 1.8,
                    [("computing", 56, TEAL, TEAL_SOFT),
                     ("cooling", 36, WARN, WARN_SOFT),
                     ("losses", 8, LILAC, LILAC_SOFT)]))
    body.append(bar(124, "A modern facility", 1.1,
                    [("computing", 91, TEAL, TEAL_SOFT),
                     ("cooling", 7, WARN, WARN_SOFT),
                     ("losses", 2, LILAC, LILAC_SOFT)]))
    body.append(box(70, 196, 620, 44, None, fill=FILL, stroke=TEAL, r=8))
    body.append(text(380, 215, "PUE = total facility power ÷ power "
                     "delivered to the computing equipment", 11, 700,
                     fill=TEAL))
    body.append(text(380, 232, "PUE 1.8 means 80% again on top of the computing "
                     "load. The best designs run close to 1.1.", 10, 500,
                     fill=MUTED))

    COSTS = [("Storage", "draws power every second for years, read or not"),
             ("Training", "weeks of thousands of accelerators, repeated at "
              "every retrain"),
             ("Inference", "tiny per query, and billions of queries exceed the "
              "training cost"),
             ("Water", "evaporative cooling consumes fresh water, sometimes "
              "where it is scarce"),
             ("Materials", "mined metals, a 3 to 5 year refresh, and e-waste"),
             ("Grid", "the same job emits several times more on a coal-heavy "
              "grid")]
    body.append(text(380, 262, "The costs beyond the servers themselves", 11,
                     700, fill=MUTED))
    for i, (k, v) in enumerate(COSTS):
        y = 274 + i * 28
        body.append(box(70, y, 620, 24, None,
                        fill=FILL2 if i % 2 == 0 else FILL, stroke="none", r=4))
        body.append(text(84, y + 16, k, 10, 700, anchor="start", fill=WARN))
        body.append(text(190, y + 16, v, 10, 450, anchor="start", fill=MUTED))
    body.append(box(70, 450, 620, 46, None, fill=TEAL_SOFT, stroke=TEAL, r=8))
    body.append(text(380, 470, "The honest caveat: efficiency has improved "
                     "steadily while total data centre energy use has kept "
                     "rising.", 10.5, 700, fill=TEAL))
    body.append(text(380, 487, "Cheaper computing gets used more. That is the "
                     "rebound effect, and a good answer names it.", 10, 500,
                     fill=MUTED))
    desc = ("Two stacked bars comparing where a data centre's electricity goes. "
            "In an older facility with a power usage effectiveness of 1.8, about "
            "56 per cent of the electricity reaches the computing equipment, 36 "
            "per cent goes on cooling and 8 per cent on distribution losses. In a "
            "modern facility with a PUE of 1.1, about 91 per cent reaches the "
            "computing equipment, 7 per cent goes on cooling and 2 per cent on "
            "losses. PUE is defined as total facility power divided by the power "
            "delivered to the computing equipment, so a PUE of 1.8 means eighty "
            "per cent again is spent on top of the computing load, while the best "
            "designs run close to 1.1. The costs beyond the servers are then "
            "listed: storage draws power every second for years whether or not it "
            "is read; training occupies thousands of accelerators for weeks and is "
            "repeated at every retrain; inference is tiny per query but billions of "
            "queries exceed the training cost; evaporative cooling consumes fresh "
            "water, sometimes where it is scarce; hardware depends on mined metals "
            "with a three to five year refresh cycle and produces e-waste; and the "
            "same job emits several times more carbon on a coal-heavy grid than on "
            "a clean one. The honest caveat is the rebound effect: efficiency has "
            "improved steadily while total data centre energy use has kept rising, "
            "because cheaper computing simply gets used more.")
    return figure("data-energy", 760, 506, "".join(body),
                  "Data centre energy, PUE and the costs beyond the servers",
                  desc,
                  "Name PUE, quantify something, and acknowledge the rebound "
                  "effect. That is the shape of a top band answer here.")


# =================================================== F201: green computing

@diagram("data-green-computing")
def _green():
    """The measures that work, ranked, with the rebound effect attached."""
    body = [text(380, 24, "What actually reduces the impact, in rough order of "
                 "effect", 12, 650, fill=MUTED)]
    MEASURES = [
        ("Delete what has no purpose", 96,
         "stored data draws power for years; retention policy is the cheapest "
         "saving there is", TEAL),
        ("Do not run what need not run", 88,
         "elastic capacity released when a job ends, instead of a cluster idling "
         "all night", TEAL),
        ("Scan less per query", 78,
         "partition and column pruning: a query touching one column costs a "
         "fraction of a full scan", TEAL),
        ("Reuse a pretrained model", 72,
         "fine-tuning instead of training from scratch avoids the single largest "
         "one-off cost", LILAC),
        ("Carbon aware placement", 64,
         "run flexible batch work where and when the grid is cleanest", LILAC),
        ("Consolidate and virtualise", 58,
         "many workloads on fewer machines, so fewer servers sit idle", LILAC),
        ("Better cooling, heat reuse", 46,
         "free air and liquid cooling cut the overhead; waste heat can warm "
         "buildings", TEAL),
        ("Longer hardware life", 34,
         "repair, resell and recycle: this is the materials and e-waste side, "
         "not the energy side", LILAC),
    ]
    for i, (name, weight, note, tone) in enumerate(MEASURES):
        y = 48 + i * 46
        body.append(box(28, y, 252, 38, None,
                        fill=TEAL_SOFT if tone == TEAL else LILAC_SOFT,
                        stroke=tone, r=6))
        body.append(text(42, y + 24, name, 10.5, 700, anchor="start", fill=tone))
        bw = 372 * weight / 100.0
        body.append(box(292, y + 8, 372, 22, None, fill=FILL2, stroke=LINE,
                        r=11))
        body.append('<rect x="292" y="%d" width="%.1f" height="22" rx="11" '
                    'fill="%s" stroke="%s" stroke-width="1"/>'
                    % (y + 8, bw, TEAL_SOFT if tone == TEAL else LILAC_SOFT,
                       tone))
        body.append(text(676, y + 24, "%d" % weight, 10, 700, anchor="start",
                         fill=tone))
        body.append(text(292, y + 44, note, 9.2, 450, anchor="start",
                         fill=MUTED))
    body.append(box(28, 424, 704, 56, None, fill=WARN_SOFT, stroke=WARN, r=8))
    body.append(text(380, 444, "The rebound effect: data centre efficiency has "
                     "improved markedly while total energy use has kept rising.",
                     11, 700, fill=WARN))
    body.append(text(380, 462, "Cheaper computing gets used more, so efficiency "
                     "alone is not a solution. Reducing the work is.", 10, 500,
                     fill=MUTED))
    desc = ("Green computing measures ranked by rough effect, each with the "
            "reason. Deleting data that has no purpose comes first, because "
            "stored data draws power continuously for years and a retention "
            "policy is the cheapest saving available. Not running what need not "
            "run comes next: elastic capacity released when a job ends rather "
            "than a cluster idling overnight. Scanning less per query follows, "
            "since partition and column pruning mean a query touching one column "
            "costs a fraction of a full scan. Reusing a pretrained model by fine "
            "tuning avoids the single largest one-off cost of training from "
            "scratch. Carbon aware placement runs flexible batch work where and "
            "when the electricity grid is cleanest. Consolidation and "
            "virtualisation put many workloads on fewer machines so fewer servers "
            "sit idle. Better cooling, including free air and liquid cooling, cuts "
            "the facility overhead, and waste heat can be reused to warm "
            "buildings. Extending hardware life through repair, resale and "
            "recycling addresses the materials and e-waste side rather than "
            "energy. The caveat underneath is the rebound effect: data centre "
            "efficiency has improved markedly while total energy use has kept "
            "rising, because cheaper computing simply gets used more, so "
            "efficiency alone is not a solution and reducing the work itself is.")
    return figure("data-green", 760, 492, "".join(body),
                  "Green computing measures, ranked", desc,
                  "The measures with the largest certain effect are the dull "
                  "ones: delete it, and do not run it.")


# ================================================= F201: sources of big data

@diagram("data-big-data-sources")
def _sources():
    """Where big data comes from, which V it stresses, and what it answers."""
    body = [text(380, 24, "Where it comes from, what it stresses, what it "
                 "answers", 12, 650, fill=MUTED)]
    SOURCES = [
        ("Transactions", "every order, payment, booking", "Volume",
         "what customers actually did", TEAL),
        ("Web and app telemetry", "taps, scroll depth, session paths",
         "Volume, velocity", "where users give up", TEAL),
        ("Sensors and IoT", "temperature, vibration, location", "Velocity",
         "a part failing before it fails", LILAC),
        ("Social media", "posts, reactions, images, networks",
         "Variety, veracity", "what people say unprompted", LILAC),
        ("Machine logs", "every request, error, state change", "Volume",
         "why the system misbehaved", TEAL),
        ("Media", "images, audio, video, CCTV", "Volume, variety",
         "what is in the picture", LILAC),
        ("Open data", "census, weather, transport, geography", "Value",
         "context you cannot generate", TEAL),
    ]
    for i, (name, what, stress, answers, tone) in enumerate(SOURCES):
        y = 48 + i * 48
        body.append(box(28, y, 176, 40, None,
                        fill=TEAL_SOFT if tone == TEAL else LILAC_SOFT,
                        stroke=tone, r=6))
        body.append(text(116, y + 18, name, 10.4, 700, fill=tone))
        body.append(text(116, y + 32, what, 8.8, 450, fill=MUTED))
        body.append(box(216, y, 150, 40, None, fill=FILL, stroke=LINE, r=6))
        body.append(text(291, y + 25, stress, 10, 600, fill=WARN))
        body.append(line(372, y + 20, 392, y + 20, stroke=tone, arrow=True))
        body.append(box(398, y, 334, 40, None, fill=FILL2, stroke=LINE, r=6))
        body.append(text(565, y + 25, answers, 10, 500,
                         fill="var(--dg-text)"))
    body.append(box(28, 388, 704, 56, None, fill=TEAL_SOFT, stroke=TEAL, r=8))
    body.append(text(380, 408, "The value is in the join: weather plus "
                     "transactions explains a sales dip that neither explains "
                     "alone.", 11, 700, fill=TEAL))
    body.append(text(380, 426, "And so is the risk, because joining datasets is "
                     "exactly what makes individuals re-identifiable.", 10, 500,
                     fill=WARN))
    desc = ("Sources of big data, each with the characteristic it stresses and "
            "the question it answers. Transactional systems produce every order, "
            "payment and booking, stressing volume, and tell you what customers "
            "actually did. Web and app telemetry produces taps, scroll depth and "
            "session paths, stressing volume and velocity, and tells you where "
            "users give up. Sensors and the Internet of Things produce "
            "temperature, vibration and location readings, stressing velocity, "
            "and tell you that a part is failing before it fails. Social media "
            "produces posts, reactions, images and network structure, stressing "
            "variety and veracity, and tells you what people say unprompted. "
            "Machine logs record every request, error and state change, stressing "
            "volume, and tell you why a system misbehaved. Media, meaning images, "
            "audio, video and CCTV, stresses volume and variety and tells you "
            "what is in the picture. Open data such as census, weather, transport "
            "and geography stresses value and supplies context an organisation "
            "cannot generate itself. The value is concentrated in the join: "
            "weather data combined with transaction data explains a sales dip that "
            "neither explains alone. So is the risk, because joining datasets is "
            "precisely what makes individuals re-identifiable.")
    return figure("data-sources", 760, 456, "".join(body),
                  "Sources of big data and what each one answers", desc,
                  "One source answers a narrow question. Two joined answer a "
                  "different kind of question, and create a different risk.")


# =============================================== F200: data file formats

@diagram("data-file-formats")
def _formats():
    """What each format can and cannot hold, and what it is actually for."""
    body = [text(380, 24, "Choose the format from the job, not from habit",
                 12, 650, fill=MUTED)]
    COLS = [(132, "format"), (104, "structure"), (90, "types?"),
            (90, "nesting?"), (104, "readable?"), (184, "use it for")]
    ROWS = [("CSV", "structured", "no", "no", "yes",
             "sharing a small table with anyone", TEAL),
            ("JSON", "semi", "some", "yes", "yes",
             "API responses, anything nested", TEAL),
            ("XML", "semi", "with a schema", "yes", "yes",
             "documents that must validate", LILAC),
            ("XLSX", "structured", "yes", "no", "in Excel",
             "a model a person will use", LILAC),
            ("SQL table", "structured", "yes", "via joins", "no",
             "many entities, many users", TEAL),
            ("Parquet", "columnar", "yes", "yes", "no",
             "hundreds of millions of rows", TEAL),
            ("PDF", "unstructured", "no", "no", "yes",
             "presentation, never as a data source", WARN)]
    x0 = (760 - sum(c[0] for c in COLS)) / 2
    cx = x0
    for w, label in COLS:
        body.append(box(cx, 46, w, 26, None, fill=FILL2, stroke=LINE, r=4))
        body.append(text(cx + w / 2, 63, label, 9.8, 700, fill=MUTED))
        cx += w
    for r, row in enumerate(ROWS):
        tone = row[-1]
        cx = x0
        y = 74 + r * 30
        for (w, _), val in zip(COLS, row[:-1]):
            first = cx == x0
            body.append(box(cx, y, w, 28, None,
                            fill=(TEAL_SOFT if tone == TEAL else
                                  LILAC_SOFT if tone == LILAC else WARN_SOFT)
                            if first else FILL, stroke=LINE, r=4))
            body.append(text(cx + w / 2, y + 18, val, 9.6,
                             700 if first else 450,
                             fill=tone if first else "var(--dg-text)"))
            cx += w
    body.append(box(x0, 294, sum(c[0] for c in COLS), 46, None,
                    fill=WARN_SOFT, stroke=WARN, r=8))
    body.append(text(380, 313, "CSV carries no type information at all.",
                     11, 700, fill=WARN))
    body.append(text(380, 330, "0123 becomes 123, and 03/04/2026 is March in "
                     "one tool and April in another. Declare the types on "
                     "import.", 10, 500, fill=MUTED))
    desc = ("A table comparing data file formats by structure, whether they "
            "carry type information, whether they support nesting, whether "
            "they are human readable, and what each is for. CSV is structured, "
            "carries no types, cannot nest, is readable, and is for sharing a "
            "small table with anyone. JSON is semi-structured, carries some "
            "type information, supports nesting, is readable, and is for API "
            "responses and anything nested. XML is semi-structured, typed with "
            "a schema, supports nesting, is readable, and is for documents that "
            "must validate. XLSX is structured, typed, does not nest, is "
            "readable only in a spreadsheet application, and is for a model a "
            "person will use. A SQL table is structured, typed, relates records "
            "through joins, is not directly readable, and is for many entities "
            "with many users. Parquet is columnar, typed, supports nesting, is "
            "not readable, and is for hundreds of millions of rows. PDF is "
            "unstructured, untyped, does not nest, is readable, and is for "
            "presentation, never as a data source. The warning underneath is "
            "that CSV carries no type information at all, so a product code of "
            "0123 becomes the number 123 and a date written 03/04/2026 is March "
            "in one tool and April in another, which is why types have to be "
            "declared on import.")
    return figure("data-fmt", 760, 352, "".join(body),
                  "Data file formats compared", desc,
                  "Nesting, types and who has to read it. Those three answer "
                  "almost every format question.")


# =============================================== F200: units and scale

@diagram("data-units-scale")
def _units():
    """What each unit of data actually looks like."""
    body = [text(380, 24, "The scale, in things you can picture", 12, 650,
                 fill=MUTED)]
    UNITS = [("Kilobyte", "KB", "a page of plain text", 0.012, TEAL),
             ("Megabyte", "MB", "a photograph, a minute of music", 0.055, TEAL),
             ("Gigabyte", "GB", "a film, or 250 songs", 0.14, TEAL),
             ("Terabyte", "TB", "a desktop hard drive", 0.3, LILAC),
             ("Petabyte", "PB", "a large organisation's whole estate", 0.56,
              LILAC),
             ("Exabyte", "EB", "a global platform, or the web in 2000", 0.86,
              WARN),
             ("Zettabyte", "ZB", "all the data created worldwide in a year",
              1.0, WARN)]
    for i, (name, abbr, example, frac, tone) in enumerate(UNITS):
        y = 50 + i * 42
        body.append(box(28, y, 150, 34, None,
                        fill=TEAL_SOFT if tone == TEAL else
                        (LILAC_SOFT if tone == LILAC else WARN_SOFT),
                        stroke=tone, r=6))
        body.append(text(88, y + 22, "%s (%s)" % (name, abbr), 10.5, 700,
                         fill=tone))
        body.append(box(190, y + 6, 240, 22, None, fill=FILL2, stroke=LINE,
                        r=11))
        body.append('<rect x="190" y="%d" width="%.1f" height="22" rx="11" '
                    'fill="%s" stroke="%s" stroke-width="1"/>'
                    % (y + 6, max(10, 240 * frac), 
                       TEAL_SOFT if tone == TEAL else
                       (LILAC_SOFT if tone == LILAC else WARN_SOFT), tone))
        body.append(text(444, y + 22, example, 10, 500, anchor="start",
                         fill="var(--dg-text)"))
        if i:
            body.append(text(180, y + 22, "×1000", 8.4, 600,
                             anchor="end", fill=MUTED))
    body.append(box(28, 348, 704, 44, None, fill=FILL, stroke=TEAL, r=8))
    body.append(text(380, 367, "Each step is a thousand times the one before, "
                     "which is why intuition fails above about a terabyte.",
                     10.8, 700, fill=TEAL))
    body.append(text(380, 384, "The bar lengths here are not to scale: drawn "
                     "to scale, a kilobyte would be invisible.", 9.8, 500,
                     fill=MUTED))
    desc = ("The units of data with an example of each: a kilobyte is a page "
            "of plain text; a megabyte is a photograph or a minute of music; a "
            "gigabyte is a film or 250 songs; a terabyte is a desktop hard "
            "drive; a petabyte is a large organisation's entire data estate; an "
            "exabyte is a global platform, or the whole web around the year "
            "2000; a zettabyte is roughly all the data created worldwide in a "
            "year. Each step is a thousand times the one before it, which is "
            "why intuition about size breaks down above about a terabyte. The "
            "bars shown are not drawn to scale, because at true scale a "
            "kilobyte would be invisible beside a zettabyte.")
    return figure("data-units", 760, 404, "".join(body),
                  "The units of data, with an example of each", desc,
                  "Every step is a factor of a thousand. Big data starts where "
                  "one machine stops.")


# ============================================ F200: interoperability levels

@diagram("data-interoperability")
def _interop():
    """Three levels of agreement, and what failure looks like at each."""
    body = [text(380, 24, "Two systems have to agree at three levels",
                 12, 650, fill=MUTED)]
    LEVELS = [
        ("TECHNICAL", "how it physically moves",
         "HTTPS, SFTP, the file format, the encoding",
         "Nothing transfers. It fails loudly, and somebody fixes it.",
         TEAL, TEAL_SOFT),
        ("SYNTACTIC", "how it is structured",
         "field names, order, nesting, date format",
         "It parses, and values land in the wrong columns. Usually visible.",
         LILAC, LILAC_SOFT),
        ("SEMANTIC", "what the values mean",
         "what counts as a customer, as active, as complete",
         "Everything imports cleanly and the numbers are wrong. Nothing errors.",
         WARN, WARN_SOFT),
    ]
    for i, (name, q, detail, fail, tone, soft) in enumerate(LEVELS):
        y = 50 + i * 104
        body.append(box(28, y, 200, 88, None, fill=soft, stroke=tone, r=10))
        body.append(text(128, y + 32, name, 12.5, 780, fill=tone))
        body.append(text(128, y + 52, q, 9.8, 450, fill=MUTED))
        body.append(box(246, y + 10, 240, 68, None, fill=FILL, stroke=tone,
                        r=8))
        body.append(text(366, y + 34, "AGREE ON", 9, 700, fill=tone))
        body.append(text(366, y + 52, detail, 9.6, 450, fill=MUTED))
        body.append(line(492, y + 44, 512, y + 44, stroke=tone, arrow=True))
        body.append(box(518, y + 10, 214, 68, None,
                        fill=WARN_SOFT if i == 2 else FILL2,
                        stroke=WARN if i == 2 else LINE, r=8))
        body.append(text(625, y + 30, "IF NOT", 9, 700,
                         fill=WARN if i == 2 else MUTED))
        # wrap the failure text onto two lines
        words, lines, cur = fail.split(), [], ""
        for w in words:
            if len(cur) + len(w) + 1 <= 34:
                cur = (cur + " " + w).strip()
            else:
                lines.append(cur)
                cur = w
        lines.append(cur)
        for j, ln in enumerate(lines[:3]):
            body.append(text(625, y + 46 + j * 13, ln, 9, 500, fill=MUTED))
    body.append(text(380, 372, "Semantic failure is the dangerous one, because "
                     "nothing anywhere reports an error.", 11, 700, fill=WARN))
    desc = ("Interoperability needs agreement at three levels. Technical "
            "agreement is how the data physically moves: the protocol, the file "
            "format and the character encoding. Without it nothing transfers at "
            "all, which fails loudly and gets fixed. Syntactic agreement is how "
            "the data is structured: the field names, their order, whether "
            "records nest and how dates are written. Without it the file parses "
            "but values land in the wrong columns, which is usually visible on "
            "inspection. Semantic agreement is what the values mean: what counts "
            "as a customer, what counts as active, what counts as complete. "
            "Without it everything imports cleanly and the numbers are simply "
            "wrong, and nothing anywhere reports an error, which is why semantic "
            "failure is the dangerous one.")
    return figure("data-interop", 760, 388, "".join(body),
                  "The three levels of interoperability", desc,
                  "The exchange that worked perfectly and produced the wrong "
                  "total failed at the level nobody checks.")


# ================================================ F200: retention and deletion

@diagram("data-retention")
def _retention():
    """How long data is kept, and what deleting it actually means."""
    body = [text(380, 24, "Every dataset needs an end date", 12, 650,
                 fill=MUTED)]
    ROWS = [("CCTV footage", "about 30 days", "unless needed for an incident",
             TEAL),
            ("Job applications, unsuccessful", "6 to 12 months",
             "to answer a discrimination claim", TEAL),
            ("Marketing contacts", "a set period after last engagement",
             "and removed on request, immediately", LILAC),
            ("Customer orders", "6 years", "a statutory accounting period",
             LILAC),
            ("Employee records", "6 years after leaving",
             "tax and employment law", TEAL),
            ("Analytics and logs", "as short as the question allows",
             "this is the one nobody sets", WARN)]
    for i, (what, how_long, why, tone) in enumerate(ROWS):
        y = 48 + i * 40
        body.append(box(28, y, 236, 32, None,
                        fill=TEAL_SOFT if tone == TEAL else
                        (LILAC_SOFT if tone == LILAC else WARN_SOFT),
                        stroke=tone, r=6))
        body.append(text(146, y + 21, what, 10.4, 650, fill=tone))
        body.append(box(276, y, 220, 32, None, fill=FILL, stroke=LINE, r=6))
        body.append(text(386, y + 21, how_long, 10, 600,
                         fill="var(--dg-text)"))
        body.append(text(512, y + 21, why, 9.8, 450, anchor="start",
                         fill=MUTED))
    body.append(text(380, 306, "WHAT “DELETED” HAS TO MEAN", 11, 700,
                     fill=MUTED))
    STEPS = [("Deleting a file", "only removes the pointer; the blocks remain "
              "until overwritten", WARN),
             ("Secure erase", "overwrites, or destroys the key the data was "
              "encrypted with", TEAL),
             ("Backups and archives", "are included, or the data is still "
              "there", WARN),
             ("Record it", "what was destroyed, when, by whom and under which "
              "policy", TEAL)]
    for i, (k, v, tone) in enumerate(STEPS):
        y = 320 + i * 28
        body.append(box(28, y, 704, 24, None,
                        fill=FILL2 if i % 2 == 0 else FILL, stroke="none", r=4))
        body.append(text(44, y + 16, k, 10, 700, anchor="start", fill=tone))
        body.append(text(220, y + 16, v, 10, 450, anchor="start", fill=MUTED))
    body.append(box(28, 438, 704, 40, None, fill=TEAL_SOFT, stroke=TEAL, r=8))
    body.append(text(380, 462, "“We keep everything in case it is "
                     "useful” breaches storage limitation, and makes every "
                     "future breach larger.", 10.8, 700, fill=TEAL))
    desc = ("Typical retention periods, with the reason for each. CCTV footage "
            "is usually kept about 30 days unless it is needed for an incident. "
            "Unsuccessful job applications are kept six to twelve months, long "
            "enough to answer a discrimination claim. Marketing contacts are "
            "kept for a set period after last engagement and removed "
            "immediately on request. Customer orders are kept six years, a "
            "statutory accounting period. Employee records are kept six years "
            "after leaving for tax and employment law. Analytics and logs "
            "should be kept only as long as the question requires, and this is "
            "the period organisations most often fail to set. Underneath, what "
            "deletion has to mean: deleting a file only removes the pointer and "
            "the blocks remain until overwritten; secure erase overwrites the "
            "data or destroys the key it was encrypted with; backups and "
            "archives must be included or the data is still held; and the "
            "destruction should be recorded, noting what was destroyed, when, "
            "by whom and under which policy. Keeping everything in case it "
            "proves useful breaches the storage limitation principle and makes "
            "every future breach larger.")
    return figure("data-retain", 760, 490, "".join(body),
                  "Retention periods and what deletion means", desc,
                  "The cheapest way to protect data is not to still have it.")


# ============================================ F201: processing models

@diagram("data-processing-models")
def _processing():
    """Four ways to process, and what each one is for."""
    body = [text(380, 24, "How quickly does the answer stop being useful?",
                 12, 650, fill=MUTED)]
    MODELS = [("BATCH", "hours to a day", "a large volume on a schedule",
               ["monthly billing", "model retraining", "overnight reports"],
               TEAL, TEAL_SOFT, 0.18),
              ("MICRO-BATCH", "seconds to minutes", "small batches, often",
               ["near-live dashboards", "frequent aggregates"],
               LILAC, LILAC_SOFT, 0.45),
              ("STREAM", "milliseconds", "each event as it arrives",
               ["fraud blocking", "sensor alerts", "live routing"],
               WARN, WARN_SOFT, 0.78),
              ("INTERACTIVE", "while someone waits", "a human asking a question",
               ["exploration", "a dashboard filter"],
               TEAL, TEAL_SOFT, 1.0)]
    for i, (name, latency, what, uses, tone, soft, _f) in enumerate(MODELS):
        x = 24 + i * 184
        body.append(box(x, 52, 172, 190, None, fill=soft, stroke=tone, r=10))
        body.append(text(x + 86, 78, name, 11.5, 780, fill=tone))
        body.append(box(x + 14, 90, 144, 24, None, fill=FILL, stroke=tone,
                        r=12))
        body.append(text(x + 86, 106, latency, 9.8, 700, fill=tone))
        body.append(text(x + 86, 132, what, 9.4, 450, fill=MUTED))
        for j, u in enumerate(uses):
            body.append(text(x + 86, 156 + j * 18, "• " + u, 9.4, 500,
                             fill="var(--dg-text)"))
    body.append(line(40, 268, 720, 268, stroke=LINE, w=1.6, arrow=True))
    body.append(text(40, 290, "answer needed slowly", 9.6, 600, anchor="start",
                     fill=MUTED))
    body.append(text(720, 290, "answer needed immediately", 9.6, 600,
                     anchor="end", fill=MUTED))
    body.append(box(24, 306, 708, 44, None, fill=FILL, stroke=TEAL, r=8))
    body.append(text(378, 325, "The choice is not about volume. It is about "
                     "how fast the value of the answer decays.", 11, 700,
                     fill=TEAL))
    body.append(text(378, 342, "A fraudulent transaction is settled before a "
                     "nightly batch ever sees it.", 10, 500, fill=MUTED))
    desc = ("Four processing models arranged by how quickly an answer is "
            "needed. Batch processes a large volume on a schedule with a "
            "latency of hours to a day, and suits monthly billing, model "
            "retraining and overnight reports. Micro-batch processes small "
            "batches frequently with a latency of seconds to minutes, and suits "
            "near-live dashboards and frequent aggregates. Stream processing "
            "handles each event as it arrives with a latency of milliseconds, "
            "and suits fraud blocking, sensor alerts and live routing. "
            "Interactive query answers while a person waits, and suits "
            "exploration and dashboard filtering. The choice between them is "
            "not about the volume of data but about how fast the value of the "
            "answer decays: a fraudulent transaction has been authorised and "
            "settled before a nightly batch ever sees it.")
    return figure("data-proc", 760, 362, "".join(body),
                  "Batch, micro-batch, stream and interactive processing", desc,
                  "Pick the model from how fast the answer goes stale, not "
                  "from how much data there is.")


# ========================================= F201: machine learning in use

@diagram("data-ml-applications")
def _ml_apps():
    """What machine learning is actually doing, sector by sector."""
    body = [text(380, 24, "The same few techniques, across every sector",
                 12, 650, fill=MUTED)]
    SECTORS = [
        ("Retail", "recommendation · demand forecasting · churn",
         "classification, regression", TEAL),
        ("Finance", "fraud detection · credit scoring · laundering checks",
         "classification, anomaly detection", LILAC),
        ("Healthcare", "image diagnosis · triage · readmission risk",
         "classification, deep learning", TEAL),
        ("Manufacturing", "predictive maintenance · visual inspection",
         "regression, anomaly detection", LILAC),
        ("Transport", "routing · demand prediction · autonomous control",
         "reinforcement, regression", TEAL),
        ("Energy", "load forecasting · grid balancing · fault prediction",
         "regression, anomaly detection", LILAC),
        ("Agriculture", "yield prediction · disease detection from imagery",
         "regression, deep learning", TEAL),
        ("Public sector", "demand planning · fraud · casework triage",
         "classification, clustering", LILAC),
    ]
    for i, (sector, uses, technique, tone) in enumerate(SECTORS):
        y = 46 + i * 40
        body.append(box(28, y, 144, 32, None,
                        fill=TEAL_SOFT if tone == TEAL else LILAC_SOFT,
                        stroke=tone, r=6))
        body.append(text(100, y + 21, sector, 10.6, 700, fill=tone))
        body.append(box(184, y, 348, 32, None, fill=FILL, stroke=LINE, r=6))
        body.append(text(358, y + 21, uses, 9.8, 450, fill="var(--dg-text)"))
        body.append(box(544, y, 188, 32, None, fill=FILL2, stroke=LINE, r=6))
        body.append(text(638, y + 21, technique, 9.4, 550, fill=MUTED))
    body.append(box(28, 376, 704, 44, None, fill=TEAL_SOFT, stroke=TEAL, r=8))
    body.append(text(380, 395, "Almost all of this is classification, "
                     "regression, clustering or anomaly detection.", 11, 700,
                     fill=TEAL))
    body.append(text(380, 412, "The sector changes the data and the cost of "
                     "being wrong. The technique barely changes at all.",
                     10, 500, fill=MUTED))
    desc = ("Machine learning applications by sector, with the techniques "
            "behind them. Retail: recommendation, demand forecasting and churn "
            "prediction, using classification and regression. Finance: fraud "
            "detection, credit scoring and money laundering checks, using "
            "classification and anomaly detection. Healthcare: image diagnosis, "
            "triage and readmission risk, using classification and deep "
            "learning. Manufacturing: predictive maintenance and visual quality "
            "inspection, using regression and anomaly detection. Transport: "
            "routing, demand prediction and autonomous control, using "
            "reinforcement learning and regression. Energy: load forecasting, "
            "grid balancing and fault prediction, using regression and anomaly "
            "detection. Agriculture: yield prediction and disease detection "
            "from imagery, using regression and deep learning. Public sector: "
            "demand planning, fraud detection and casework triage, using "
            "classification and clustering. Almost all of it reduces to "
            "classification, regression, clustering or anomaly detection: the "
            "sector changes the data and the cost of being wrong, while the "
            "technique barely changes at all.")
    return figure("data-mlapp", 760, 432, "".join(body),
                  "Machine learning applications by sector", desc,
                  "Learn the four task types properly and every application "
                  "in the paper becomes one of them.")


# ======================================= F201: society, both directions

@diagram("data-society-impacts")
def _society():
    """The same capability, with its benefit and its cost side by side."""
    body = [text(380, 24, "One capability, two consequences", 12, 650,
                 fill=MUTED)]
    body.append(text(214, 50, "WHAT IT MAKES POSSIBLE", 11, 750, fill=TEAL))
    body.append(text(566, 50, "WHAT IT COSTS", 11, 750, fill=WARN))
    PAIRS = [
        ("Population health data", "outbreaks detected in days, not months",
         "the most sensitive data anyone holds, in one place"),
        ("Personalisation", "people find what is actually relevant to them",
         "filter bubbles, and a catalogue that appears to shrink"),
        ("Smart cities", "transport, energy and waste matched to real demand",
         "continuous monitoring of everyone who lives there"),
        ("Automation of routine work", "new specialist roles, and tedium removed",
         "the roles automated are not the roles created"),
        ("Free services funded by data", "access regardless of ability to pay",
         "profiling most users never see and cannot inspect"),
        ("Online public services", "cheaper, available at any hour",
         "the digital divide deepens for those without access"),
    ]
    for i, (what, good, bad) in enumerate(PAIRS):
        y = 62 + i * 54
        body.append(box(28, y, 160, 46, None, fill=FILL2, stroke=LINE, r=6))
        body.append(text(108, y + 28, what, 9.6, 650,
                         fill="var(--dg-text)"))
        body.append(box(198, y, 268, 46, None, fill=TEAL_SOFT, stroke=TEAL,
                        r=6))
        body.append(text(332, y + 28, good, 9.4, 500, fill=TEAL))
        body.append(box(476, y, 256, 46, None, fill=WARN_SOFT, stroke=WARN,
                        r=6))
        body.append(text(604, y + 28, bad, 9.4, 500, fill=WARN))
    body.append(box(28, 390, 704, 46, None, fill=FILL, stroke=LINE, r=8))
    body.append(text(380, 410, "Both columns are true at once, and they are "
                     "produced by the same system.", 11, 700, fill=MUTED))
    body.append(text(380, 427, "A question asking you to evaluate wants both, "
                     "and then a judgement about this particular case.",
                     10, 500, fill=MUTED))
    desc = ("Six capabilities with the benefit and the cost of each set side "
            "by side. Population health data lets outbreaks be detected in days "
            "rather than months, and concentrates the most sensitive data "
            "anyone holds in one place. Personalisation helps people find what "
            "is genuinely relevant to them, and creates filter bubbles in which "
            "the catalogue appears to shrink. Smart cities match transport, "
            "energy and waste to real demand, and monitor everyone who lives "
            "there continuously. Automating routine work removes tedium and "
            "creates new specialist roles, but the roles automated are not the "
            "roles created. Services funded by data are free at the point of "
            "use regardless of ability to pay, and are paid for with profiling "
            "most users never see and cannot inspect. Online public services "
            "are cheaper and available at any hour, and deepen the digital "
            "divide for people without access or skills. Both columns are true "
            "at the same time and are produced by the same systems, which is "
            "why a question asking for an evaluation wants both sides and then "
            "a judgement about the particular case in front of you.")
    return figure("data-society", 760, 448, "".join(body),
                  "The benefits and the costs of data at scale", desc,
                  "Neither column is the answer on its own. The judgement at "
                  "the end is where the top band is.")
