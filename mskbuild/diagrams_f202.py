"""Diagrams and graphs for F202, Spreadsheet data modelling.

F202 is the coursework unit of the Data Analytics qualification, so these
pictures are of the things a student actually builds: a workbook laid out one
job per sheet, an input sheet with its validation, a test plan with a failure
in it, a dashboard, an evaluation that quotes its evidence.

Every worked figure uses one invented model, a ticket price model for a one
day community music festival. It is deliberately nothing like any OCR set
assignment: the point is to show the quality of each piece of evidence, never
to hand anybody an answer to their own brief. The model is defined once below,
so the graph, the goal seek, the scenarios and the test plan cannot disagree
with each other or with the text.

Registered into the shared diagram registry, so `!diagram <name>` works as it
does everywhere else.
"""
from .diagrams import (diagram, TEAL, TEAL_SOFT, LILAC, LILAC_SOFT, WARN,
                       WARN_SOFT, FILL, LINE, MUTED)
from .svg import figure, box, text, line, path, circle, chip, marker, notes
from .diagrams_data import axes

FILL2 = "var(--dg-fill-2)"
INK = "var(--dg-text)"


# ------------------------------------------------------------ the model

DEMAND_AT_ZERO = 600      # people who would come if it were free (survey)
LOST_PER_POUND = 12       # people lost for every extra pound on the price
CAPACITY = 400            # licensed capacity of the field
COST_PER_HEAD = 5.0       # wristband, toilets and security, per person
FIXED = 4000.0            # stage, licence and insurance


def tickets(price, demand=DEMAND_AT_ZERO, lost=LOST_PER_POUND, cap=CAPACITY):
    """=MIN(Capacity, MAX(0, DemandAtZero - LostPerPound * TicketPrice))"""
    return min(cap, max(0.0, demand - lost * price))


def profit(price, demand=DEMAND_AT_ZERO, lost=LOST_PER_POUND, cap=CAPACITY,
           per_head=COST_PER_HEAD, fixed=FIXED):
    t = tickets(price, demand, lost, cap)
    return t * price - (fixed + t * per_head)


def seek(target, lo, hi):
    """The price between lo and hi where profit equals target, by bisection.

    This is what Goal Seek does: trial and improvement on one input until the
    formula cell reaches the target.
    """
    flo = profit(lo) - target
    for _ in range(80):
        mid = (lo + hi) / 2.0
        fm = profit(mid) - target
        if (fm < 0) == (flo < 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return (lo + hi) / 2.0


def money(v, pence=False):
    """£2,075 or -£845, the way a spreadsheet formats currency."""
    s = "{:,.2f}".format(abs(v)) if pence else "{:,.0f}".format(abs(v))
    return ("−£" if v < 0 else "£") + s


def _cells(x0, y, cols, values, fills, h=24, size=9.4, tones=None, mono=None,
           anchor="middle"):
    """One row of a drawn table. Values containing a newline take two lines."""
    out, x = [], x0
    for i, (w, val) in enumerate(zip(cols, values)):
        out.append(box(x, y, w, h, None, fill=fills[i] if isinstance(fills, list)
                       else fills, stroke=LINE, r=3))
        tone = tones[i] if tones else INK
        is_mono = bool(mono and mono[i])
        tx = x + w / 2 if anchor == "middle" else x + 7
        parts = str(val).split("\n")
        if len(parts) == 1:
            out.append(text(tx, y + h / 2 + 3.5, val, size, 500, anchor=anchor,
                            fill=tone, mono=is_mono))
        else:
            out.append(text(tx, y + h / 2 - 3, parts[0], size, 500,
                            anchor=anchor, fill=tone, mono=is_mono))
            out.append(text(tx, y + h / 2 + 10, parts[1], size - 0.6, 450,
                            anchor=anchor, fill=MUTED, mono=is_mono))
        x += w
    return "".join(out)


# ============================================================ TA1: shape

@diagram("f202-model-ipo")
def _model_ipo():
    """Inputs and assumptions, processing, outputs, and the what-if loop."""
    p = 27.5
    t = tickets(p)
    rev = t * p
    cost = FIXED + t * COST_PER_HEAD
    body = [text(380, 24, "Every spreadsheet model has the same shape", 12, 650,
                 fill=MUTED)]
    # Inputs the user changes.
    body.append(box(24, 44, 220, 92, None, fill=TEAL_SOFT, stroke=TEAL, r=8))
    body.append(text(36, 64, "INPUT VARIABLES", 10.5, 750, anchor="start",
                     fill=TEAL))
    body.append(text(36, 79, "what the user experiments with", 9.2, 450,
                     anchor="start", fill=MUTED))
    for i, s in enumerate(["Ticket price: £27.50", "Scenario: expected"]):
        body.append(box(36, 88 + i * 22, 196, 19, None, fill=FILL, stroke=TEAL,
                        r=4))
        body.append(text(46, 101 + i * 22, s, 9.6, 600, anchor="start"))
    # Assumptions and constants.
    body.append(box(24, 146, 220, 154, None, fill=LILAC_SOFT, stroke=LILAC, r=8))
    body.append(text(36, 166, "ASSUMPTIONS AND CONSTANTS", 10.5, 750,
                     anchor="start", fill=LILAC))
    body.append(text(36, 181, "taken as given, each with a source", 9.2, 450,
                     anchor="start", fill=MUTED))
    for i, s in enumerate(["Demand: 600 − 12 × price",
                           "Capacity: 400 people",
                           "Cost per head: £5",
                           "Fixed costs: £4,000"]):
        body.append(box(36, 190 + i * 26, 196, 21, None, fill=FILL,
                        stroke=LILAC, r=4))
        body.append(text(46, 204.5 + i * 26, s, 9.6, 600, anchor="start"))
    # Processing.
    body.append(box(270, 44, 220, 256, None, fill=FILL, stroke=LINE, r=8))
    body.append(text(282, 64, "PROCESSING", 10.5, 750, anchor="start",
                     fill="var(--dg-text)"))
    body.append(text(282, 79, "formulas, in the order they run", 9.2, 450,
                     anchor="start", fill=MUTED))
    STEPS = [("tickets = MIN(capacity, demand)", "%d tickets" % t),
             ("revenue = tickets × price", money(rev)),
             ("costs = fixed + tickets × £5", money(cost)),
             ("profit = revenue − costs", money(rev - cost))]
    for i, (f, v) in enumerate(STEPS):
        y = 90 + i * 51
        body.append(box(282, y, 196, 44, None, fill=FILL2, stroke=LINE, r=5))
        body.append(text(292, y + 18, f, 9.3, 600, anchor="start", mono=True))
        body.append(text(292, y + 35, "→ " + v, 9.6, 700, anchor="start",
                         fill=TEAL))
    # Outputs.
    body.append(box(516, 44, 220, 256, None, fill=TEAL_SOFT, stroke=TEAL, r=8))
    body.append(text(528, 64, "OUTPUTS", 10.5, 750, anchor="start", fill=TEAL))
    body.append(text(528, 79, "what the client actually reads", 9.2, 450,
                     anchor="start", fill=MUTED))
    body.append(box(528, 90, 196, 58, None, fill=FILL, stroke=TEAL, r=6))
    body.append(text(626, 112, "PROFIT", 9.5, 750, fill=MUTED))
    body.append(text(626, 137, money(rev - cost), 20, 750, fill=TEAL))
    for i, s in enumerate(["Tickets sold: %d of %d" % (t, CAPACITY),
                           "Status: PROFIT (green)",
                           "Break-even: £15.00 to £40.65",
                           "Chart: profit against price"]):
        body.append(box(528, 158 + i * 34, 196, 28, None, fill=FILL,
                        stroke=TEAL, r=4))
        body.append(text(538, 176 + i * 34, s, 9.6, 600, anchor="start"))
    # Flow arrows.
    body.append(path("M244 92 L266 120", stroke=TEAL, w=1.8, arrow=True,
                     marker="ah-accent"))
    body.append(path("M244 222 L266 196", stroke=LILAC, w=1.8, arrow=True,
                     marker="ah-alt"))
    body.append(path("M490 172 L512 172", stroke=TEAL, w=1.8, arrow=True,
                     marker="ah-accent"))
    # The what-if loop.
    body.append(path("M626 300 L626 322 L134 322 L134 304", stroke=WARN, w=1.8,
                     dash="6 4", arrow=True))
    body.append(chip(380, 322, "change an input: every output recalculates",
                     fill=WARN_SOFT, stroke=WARN, text_fill=WARN, size=10))
    p2 = 35.0
    body.append(text(380, 356, "At £35 the same formulas give %d tickets and "
                     "%s profit: that loop makes it a model, not a table."
                     % (tickets(p2), money(profit(p2))), 10.2, 550, fill=MUTED))
    desc = ("A spreadsheet model drawn as four groups of cells. On the left, the "
            "input variables the user experiments with: a ticket price of 27 "
            "pounds 50 and a scenario, set to expected. Beneath them, the "
            "assumptions and constants, each of which should have a source: "
            "demand of 600 minus 12 people for every pound on the price, a "
            "capacity of 400 people, a cost of 5 pounds per person and fixed "
            "costs of 4,000 pounds. In the middle, the processing: four formulas "
            "in the order they run. Tickets sold is the smaller of capacity and "
            "demand, giving 270 tickets. Revenue is tickets times price, 7,425 "
            "pounds. Costs are the fixed costs plus 5 pounds per ticket, 5,350 "
            "pounds. Profit is revenue minus costs, 2,075 pounds. On the right, "
            "the outputs the client reads: profit of 2,075 pounds, 270 of 400 "
            "tickets sold, a green profit status, the break-even prices of 15 "
            "pounds and 40 pounds 65, and a chart of profit against price. A "
            "dashed arrow runs from the outputs back to the inputs: change any "
            "input and every output recalculates. At a price of 35 pounds the "
            "same formulas give 180 tickets and 1,400 pounds profit. That loop "
            "is what makes a spreadsheet a model rather than a table of numbers.")
    return figure("f202-ipo", 760, 372, "".join(body),
                  "The parts of a spreadsheet model", desc,
                  "Inputs, assumptions, processing and outputs. Keep them in "
                  "separate, labelled places and the model explains itself.")


@diagram("f202-model-uses")
def _model_uses():
    """Six kinds of model and the question each one answers."""
    body = [text(380, 24, "What spreadsheet models are for: each one answers a "
                 "question", 12, 650, fill=MUTED)]
    USES = [("Budget", "Will we overspend this year?",
             "planned against actual, by month", TEAL, TEAL_SOFT),
            ("Cash flow forecast", "When does the money run out?",
             "opening balance + in − out", LILAC, LILAC_SOFT),
            ("Break-even", "How many sales cover the costs?",
             "fixed costs ÷ (price − cost per unit)", TEAL, TEAL_SOFT),
            ("Pricing", "Which price makes the most profit?",
             "demand changes as price changes", LILAC, LILAC_SOFT),
            ("Stock control", "When should we reorder?",
             "reorder level, lead time, usage", TEAL, TEAL_SOFT),
            ("Simulation", "What if things go differently?",
             "scenarios, random variation", LILAC, LILAC_SOFT)]
    for i, (name, q, how, tone, soft) in enumerate(USES):
        col, row = i % 3, i // 3
        x, y = 24 + col * 240, 44 + row * 118
        body.append(box(x, y, 228, 106, None, fill=soft, stroke=tone, r=8))
        body.append(text(x + 14, y + 24, name.upper(), 10.5, 750, anchor="start",
                         fill=tone))
        body.append(text(x + 14, y + 48, q, 9.8, 650, anchor="start"))
        body.append(box(x + 12, y + 62, 204, 32, None, fill=FILL, stroke=tone,
                        r=5))
        body.append(text(x + 114, y + 82, how, 9.2, 500, fill=MUTED))
    body.append(box(24, 288, 708, 46, None, fill=FILL, stroke=LINE, r=8))
    body.append(text(378, 307, "Start from the question the client needs "
                     "answered, not from the spreadsheet features you know.",
                     10.6, 700, fill=TEAL))
    body.append(text(378, 324, "The question decides the inputs, the outputs and "
                     "which what-if tools the model needs.", 9.8, 500,
                     fill=MUTED))
    desc = ("Six kinds of spreadsheet model, each with the question it answers "
            "and how it works. A budget answers 'will we overspend this year?' by "
            "comparing planned and actual spending month by month. A cash flow "
            "forecast answers 'when does the money run out?' by adding money in "
            "and subtracting money out from an opening balance. A break-even "
            "model answers 'how many must we sell to cover our costs?' by "
            "dividing fixed costs by the difference between price and cost per "
            "unit. A pricing model answers 'which price makes the most profit?' "
            "by letting demand change as the price changes. A stock control "
            "model answers 'when should we reorder?' from the reorder level, "
            "lead time and usage. A simulation answers 'what if demand is not "
            "what we expect?' with scenarios and random variation. The lesson "
            "underneath: start from the question the client needs answered, "
            "because the question decides the inputs, the outputs and which "
            "what-if tools the model needs.")
    return figure("f202-uses", 760, 346, "".join(body),
                  "Kinds of spreadsheet model", desc,
                  "A model exists to answer a question. Name the question first.")


# ======================================================= TA1: references

@diagram("f202-cell-references")
def _references():
    """Relative, absolute and mixed references, each copied the way it is used."""
    body = [text(380, 22, "What happens to a reference when the formula is "
                 "copied", 12, 650, fill=MUTED)]

    def grid(x0, y0, col_w, heads, rows, fills=None, mono_col=None):
        out = [box(x0, y0, 22, 22, None, fill=FILL2, stroke=LINE, r=2)]
        cx = x0 + 22
        for h, w in zip(heads, col_w):
            out.append(box(cx, y0, w, 22, None, fill=FILL2, stroke=LINE, r=2))
            out.append(text(cx + w / 2, y0 + 15, h, 9.5, 700, fill=MUTED))
            cx += w
        for r, row in enumerate(rows):
            y = y0 + 22 + r * 26
            out.append(box(x0, y, 22, 26, None, fill=FILL2, stroke=LINE, r=2))
            out.append(text(x0 + 11, y + 17, str(r + 1), 9.5, 700, fill=MUTED))
            cx = x0 + 22
            for c, (val, w) in enumerate(zip(row, col_w)):
                f = fills[r][c] if fills else FILL
                out.append(box(cx, y, w, 26, None, fill=f, stroke=LINE, r=2))
                is_f = str(val).startswith("=")
                out.append(text(cx + w / 2, y + 17, val, 9 if is_f else 9.6,
                                650 if is_f else 500,
                                fill=TEAL if is_f else INK, mono=is_f))
                cx += w
        return "".join(out)

    S, H = TEAL_SOFT, FILL
    # Panel 1: relative.
    body.append(text(132, 50, "RELATIVE  A2", 11, 750, fill=TEAL))
    body.append(text(132, 66, "both parts move with the formula", 9.4, 500,
                     fill=MUTED))
    body.append(grid(24, 78, [56, 62, 78], ["A", "B", "C"],
                     [["Tickets", "Price", "Revenue"],
                      ["270", "£27.50", "=A2*B2"],
                      ["180", "£35.00", "=A3*B3"],
                      ["360", "£20.00", "=A4*B4"]],
                     fills=[[H, H, H], [H, H, S], [H, H, S], [H, H, S]]))
    body.append(path("M252 140 L252 194", stroke=TEAL, w=1.6, arrow=True,
                     marker="ah-accent"))
    body.append(text(132, 222, "Filled down, row 2 becomes row 3, then 4.", 9.4,
                     550, fill=MUTED))
    body.append(text(132, 238, "Right for a calculation repeated per row.", 9.4,
                     550, fill=MUTED))
    # Panel 2: absolute.
    body.append(text(380, 50, "ABSOLUTE  $F$1", 11, 750, fill=LILAC))
    body.append(text(380, 66, "the dollar signs pin column and row", 9.4, 500,
                     fill=MUTED))
    body.append(grid(272, 78, [56, 84, 56], ["A", "B", "F"],
                     [["Tickets", "Costs", "£5.00"],
                      ["270", "=A2*$F$1", ""],
                      ["180", "=A3*$F$1", ""],
                      ["360", "=A4*$F$1", ""]],
                     fills=[[H, H, LILAC_SOFT], [H, S, H], [H, S, H],
                            [H, S, H]]))
    body.append(chip(380, 219, "without $: row 3 reads =A3*F2, which is empty",
                     fill=WARN_SOFT, stroke=WARN, text_fill=WARN, size=9))
    body.append(text(380, 244, "F1 holds cost per head: one cell, used by all.",
                     9.4, 550, fill=MUTED))
    # Panel 3: mixed.
    body.append(text(628, 50, "MIXED  $A2 and B$1", 11, 750, fill=TEAL))
    body.append(text(628, 66, "pin only the part that must not move", 9.4, 500,
                     fill=MUTED))
    body.append(grid(522, 78, [52, 44, 44, 44], ["A", "B", "C", "D"],
                     [["price", "£4", "£5", "£6"],
                      ["£20", "16", "15", "14"],
                      ["£25", "21", "20", "19"],
                      ["£30", "26", "25", "24"]],
                     fills=[[H, LILAC_SOFT, LILAC_SOFT, LILAC_SOFT],
                            [LILAC_SOFT, S, H, H], [LILAC_SOFT, H, H, H],
                            [LILAC_SOFT, H, H, H]]))
    body.append(text(628, 222, "B2 holds =$A2-B$1 (margin per ticket).", 9.4,
                     550, fill=MUTED))
    body.append(text(628, 238, "Copy it anywhere: still price minus cost.",
                     9.4, 550, fill=MUTED))
    body.append(box(24, 258, 712, 64, None, fill=FILL, stroke=LINE, r=8))
    body.append(text(380, 280, "In Excel on Windows, F4 cycles a selected "
                     "reference: A1 → $A$1 → A$1 → $A1 → A1",
                     10.6, 700, fill=TEAL))
    body.append(text(380, 300, "A named range such as CostPerHead is absolute "
                     "already, and far easier to read than $F$1.", 10, 500,
                     fill=MUTED))
    desc = ("Three small spreadsheet grids showing what happens to a reference "
            "when a formula is copied. Relative: column C holds revenue. C2 "
            "contains =A2*B2, and filled down it becomes =A3*B3 and then =A4*B4, "
            "because both the column and the row move with the formula, which "
            "is right for a calculation repeated on every row. Absolute: F1 holds "
            "a cost per head of 5 pounds. B2 contains =A2*$F$1, and filled down "
            "it becomes =A3*$F$1 and =A4*$F$1, because the dollar signs pin both "
            "the column and the row to F1. Without them the copy in row 3 would "
            "read =A3*F2, an empty cell, and give zero. Mixed: a two way table "
            "with prices of 20, 25 and 30 pounds down column A and costs per "
            "head of 4, 5 and 6 pounds across row 1. B2 contains =$A2-B$1, the "
            "margin per ticket. The dollar before A keeps the column on the "
            "prices, and the dollar before 1 keeps the row on the costs, so one "
            "formula copied across and down fills the whole table: 16, 15, 14; "
            "21, 20, 19; 26, 25, 24. In Excel on Windows, F4 cycles a selected "
            "reference through A1, $A$1, A$1 and $A1. A named range such as "
            "CostPerHead is already absolute and is easier to read than $F$1.")
    return figure("f202-refs", 760, 334, "".join(body),
                  "Relative, absolute and mixed cell references", desc,
                  "Ask of every reference: when this formula is copied, which "
                  "part should move?")


# ===================================================== TA2: structure

@diagram("f202-workbook-structure")
def _workbook():
    """One job per sheet, with data flowing one way."""
    body = [text(380, 24, "One job per sheet, and the data flows one way", 12,
                 650, fill=MUTED)]
    SHEETS = [
        (24, 50, "INPUTS", TEAL, TEAL_SOFT,
         ["every value a user may change", "shaded, unlocked, validated",
          "each assumption with a source"]),
        (24, 196, "DATA", LILAC, LILAC_SOFT,
         ["lookup tables: ticket types", "imported raw data, untouched",
          "formatted as tables, named"]),
        (280, 112, "CALCULATIONS", INK, FILL,
         ["every formula, step by step", "uses names, not typed numbers",
          "locked and protected", "no one types here"]),
        (536, 50, "DASHBOARD", TEAL, TEAL_SOFT,
         ["the four numbers that matter", "charts, traffic lights",
          "scenario drop-down"]),
        (536, 196, "GUIDE", LILAC, LILAC_SOFT,
         ["how to use the model", "what each output means",
          "assumptions and limits"]),
    ]
    for x, y, name, tone, soft, lines in SHEETS:
        h = 128 if name != "CALCULATIONS" else 148
        body.append(box(x, y, 200, h, None, fill=soft, stroke=tone, r=8))
        body.append(box(x + 12, y - 9, 96, 20, None, fill=FILL, stroke=tone,
                        r=4))
        body.append(text(x + 60, y + 5, name, 9.6, 750,
                         fill=tone if tone != INK else MUTED))
        for i, s in enumerate(lines):
            body.append(text(x + 16, y + 36 + i * 24, "• " + s, 9.8, 520,
                             anchor="start"))
    body.append(path("M224 112 L276 160", stroke=TEAL, w=1.8, arrow=True,
                     marker="ah-accent"))
    body.append(path("M224 258 L276 214", stroke=LILAC, w=1.8, arrow=True,
                     marker="ah-alt"))
    body.append(path("M480 170 L532 116", stroke=TEAL, w=1.8, arrow=True,
                     marker="ah-accent"))
    body.append(path("M536 262 L484 232", stroke=LINE, w=1.4, dash="4 4"))
    body.append(text(508, 280, "explains", 9, 600, fill=MUTED))
    # Colour key.
    KEY = [(TEAL_SOFT, TEAL, "Input cell", "unlocked, pale fill, validated"),
           (FILL2, LINE, "Formula cell", "locked: never typed over"),
           (FILL, TEAL, "Output cell", "bold, formatted, on the dashboard")]
    for i, (f, s, k, v) in enumerate(KEY):
        x = 24 + i * 240
        body.append(box(x, 340, 30, 24, None, fill=f, stroke=s, r=4))
        body.append(text(x + 40, 350, k, 10, 700, anchor="start"))
        body.append(text(x + 40, 364, v, 9.2, 450, anchor="start", fill=MUTED))
    desc = ("A workbook planned as five sheets, each with one job. The Inputs "
            "sheet holds every value a user may change, shaded, unlocked and "
            "validated, with a source for each assumption. The Data sheet holds "
            "lookup tables such as ticket types and any imported raw data, left "
            "untouched and formatted as named tables. Both feed the Calculations "
            "sheet, which holds every formula step by step, refers to names "
            "rather than typed numbers, and is locked so that no one types "
            "there. Calculations feeds the Dashboard, which shows the four "
            "numbers that matter, charts, traffic light formatting and a "
            "scenario drop-down. A Guide sheet explains how to use the model, "
            "what each output means and the assumptions and limits. A colour key "
            "underneath: input cells unlocked with a pale fill and validation; "
            "formula cells locked and never typed over; output cells bold and "
            "formatted on the dashboard.")
    return figure("f202-book", 760, 378, "".join(body),
                  "Planning a workbook one job per sheet", desc,
                  "If a number is typed in two places, the model will one day "
                  "disagree with itself.")


@diagram("f202-input-sheet-mockup")
def _input_sheet():
    """An annotated design of the input sheet, as it would appear in a plan."""
    body = [text(380, 22, "Design sketch: the input sheet, annotated before "
                 "anything is built", 12, 650, fill=MUTED)]
    X, Y, CW = 24, 40, [176, 82, 196]
    W = 22 + sum(CW)
    body.append(box(X, Y, W, 330, None, fill=FILL, stroke=LINE, r=8))
    body.append(box(X, Y, W, 24, None, fill=FILL2, stroke=LINE, r=8))
    body.append(text(X + 12, Y + 16, "festival-model-v03.xlsx · Inputs", 9.6,
                     650, anchor="start", fill=MUTED))
    body.append(_cells(X, Y + 24, [22] + CW, ["", "A", "B", "C"], FILL2, h=20,
                       size=9, tones=[MUTED] * 4))
    ROWS = [("Harbour Lights ticket model", "", "", "title"),
            ("", "", "", ""),
            ("Ticket price (£)", "27.50", "between £5 and £60", "in"),
            ("Demand at £0 (people)", "600", "residents' survey, May", "in"),
            ("Tickets lost per £1", "12", "residents' survey, May", "in"),
            ("Venue capacity (people)", "400", "premises licence", "in"),
            ("Cost per attendee (£)", "5.00", "wristband, toilets, security", "in"),
            ("Fixed costs (£)", "4,000", "stage, licence, insurance", "in"),
            ("", "", "", ""),
            ("Profit (£)", "2,075", "from Calculations", "out"),
            ("Status", "PROFIT", "red if profit < 0", "out")]
    for r, (a, b, c, kind) in enumerate(ROWS):
        y = Y + 44 + r * 23
        fills = [FILL2, FILL, TEAL_SOFT if kind == "in" else FILL, FILL]
        tones = [MUTED, INK, TEAL if kind == "out" else INK, MUTED]
        body.append(_cells(X, y, [22] + CW, [str(r + 1), "", "", ""], fills,
                           h=23, size=9, tones=tones))
        body.append(text(X + 30, y + 15.5, a, 9.8 if kind != "title" else 10.2,
                         700 if kind in ("title", "out") else 520,
                         anchor="start", fill=INK))
        if b:
            body.append(text(X + 22 + CW[0] + CW[1] - 8, y + 15.5, b, 9.8,
                             750 if kind == "out" else 600, anchor="end",
                             fill=TEAL if kind == "out" else INK))
        if c:
            body.append(text(X + 22 + CW[0] + CW[1] + 8, y + 15.5, c, 9.2, 450,
                             anchor="start", fill=MUTED))
    # Sheet tabs.
    for i, tab in enumerate(["Inputs", "Data", "Calculations", "Dashboard",
                             "Guide"]):
        x = X + 10 + i * 84
        body.append(box(x, Y + 302, 80, 20, None,
                        fill=TEAL_SOFT if i == 0 else FILL2,
                        stroke=TEAL if i == 0 else LINE, r=3))
        body.append(text(x + 40, Y + 316, tab, 9, 650 if i == 0 else 500,
                         fill=TEAL if i == 0 else MUTED))
    # Numbered markers on the cells, and the notes they refer to.
    colB = X + 22 + CW[0] + CW[1]
    row = lambda r: Y + 44 + r * 23
    for n, (mx, my) in enumerate([(colB, row(2)), (X + 22 + CW[0], row(2)),
                                  (X + W - 8, row(2)), (X + W - 8, row(3) + 2),
                                  (colB, row(9))], 1):
        body.append(marker(n, mx, my))
    body.append(notes(512, 82, 56, 224, [
        ("Inputs shaded and unlocked;", "every other cell is protected"),
        ("Units in the label, so nobody", "types pence into a pounds cell"),
        ("Validation: decimal, 5 to 60,", "with an input message"),
        ("Every assumption has a", "source the client can check"),
        ("Outputs repeated here: change", "a value, see the effect at once")]))
    desc = ("A design sketch of a spreadsheet's input sheet, drawn as a grid with "
            "columns A, B and C and annotated before anything is built. Row 1 is "
            "the title, Harbour Lights ticket model. Rows 3 to 8 are the inputs, "
            "each with a label including its unit in column A, a shaded input "
            "cell in column B and a note in column C: ticket price 27 pounds 50, "
            "between 5 and 60 pounds; demand at zero pounds 600 people, from the "
            "residents' survey in May; tickets lost per pound 12, from the same "
            "survey; venue capacity 400 people, from the premises licence; cost "
            "per attendee 5 pounds, for wristband, toilets and security; fixed "
            "costs 4,000 pounds for stage, licence and insurance. Rows 10 and 11 "
            "repeat the outputs: profit 2,075 pounds and a status of PROFIT, "
            "which turns red if profit falls below zero. Sheet tabs along the "
            "bottom read Inputs, Data, Calculations, Dashboard and Guide. Five "
            "annotations explain the design: input cells are shaded and unlocked "
            "while every other cell is protected; units go in the label so "
            "nobody types pence into a pounds cell; the price has decimal "
            "validation from 5 to 60 with an input message; every assumption has "
            "a source the client can check; and the outputs are repeated on the "
            "input sheet so the effect of a change is visible at once.")
    return figure("f202-input", 760, 382, "".join(body),
                  "An annotated design for an input sheet", desc,
                  "A design is detailed enough when somebody else could build "
                  "the sheet from it without asking you a question.")


# ===================================================== TA3: decisions

@diagram("f202-nested-if")
def _nested_if():
    """A nested IF drawn as the decision flowchart it really is."""
    body = [text(380, 22, "A nested IF is a chain of decisions: group discount "
                 "by group size", 12, 650, fill=MUTED)]
    body.append(box(20, 74, 110, 48, None, fill=FILL, stroke=LINE, r=8))
    body.append(text(75, 94, "group size", 10, 700))
    body.append(text(75, 110, "in cell B2", 9.4, 450, fill=MUTED))
    body.append(line(130, 98, 156, 98, stroke=LINE, arrow=True))
    TESTS = [(218, "B2 >= 20", "20% off"), (388, "B2 >= 10", "10% off"),
             (558, "B2 >= 5", "5% off")]
    for i, (cx, cond, res) in enumerate(TESTS):
        body.append(path("M%d 98 L%d 62 L%d 98 L%d 134 Z"
                         % (cx - 60, cx, cx + 60, cx), stroke=TEAL, w=1.6,
                         fill=TEAL_SOFT))
        body.append(text(cx, 102, cond, 10.2, 700, mono=True))
        body.append(line(cx, 134, cx, 176, stroke=TEAL, w=1.6, arrow=True,
                         marker="ah-accent"))
        body.append(text(cx + 10, 158, "yes", 9.4, 700, anchor="start",
                         fill=TEAL))
        body.append(box(cx - 52, 178, 104, 38, res, fill=FILL, stroke=TEAL, r=8,
                        label_size=11, text_fill=TEAL))
        nx = TESTS[i + 1][0] - 64 if i < 2 else 642
        body.append(line(cx + 60, 98, nx, 98, stroke=LINE, arrow=True))
        body.append(text((cx + 60 + nx) / 2, 90, "no", 9.4, 700, fill=MUTED))
    body.append(box(644, 78, 96, 40, "no discount", fill=FILL, stroke=LINE,
                    r=8, label_size=10.5))
    body.append(box(20, 236, 720, 76, None, fill=FILL, stroke=LINE, r=8))
    body.append(text(36, 258, "=IF(B2>=20, 20%, IF(B2>=10, 10%, IF(B2>=5, 5%, 0%)))",
                     11, 650, anchor="start", fill=TEAL, mono=True))
    body.append(text(36, 280, "=IFS(B2>=20, 20%, B2>=10, 10%, B2>=5, 5%, TRUE, 0%)",
                     11, 650, anchor="start", fill=LILAC, mono=True))
    body.append(text(36, 300, "The same logic twice: nested IF works everywhere; "
                     "IFS is easier to read where it exists.", 9.6, 500,
                     anchor="start", fill=MUTED))
    body.append(box(20, 322, 720, 40, None, fill=WARN_SOFT, stroke=WARN, r=8))
    body.append(text(380, 347, "Test the largest threshold first. In the other "
                     "order a group of 25 passes B2>=5 first and gets only 5%.",
                     10.2, 650, fill=WARN))
    desc = ("A flowchart of a nested IF that works out a group discount from the "
            "group size in cell B2. The first decision asks whether B2 is at "
            "least 20; if yes the discount is 20 percent. If no, the second "
            "decision asks whether B2 is at least 10; if yes, 10 percent. If no, "
            "the third asks whether B2 is at least 5; if yes, 5 percent, and if "
            "no there is no discount. The same logic is written as a formula two "
            "ways: =IF(B2>=20, 20%, IF(B2>=10, 10%, IF(B2>=5, 5%, 0%))), and "
            "with the IFS function as =IFS(B2>=20, 20%, B2>=10, 10%, B2>=5, 5%, "
            "TRUE, 0%). Nested IF works in every spreadsheet; IFS is easier to "
            "read where it is available. A warning underneath: test the largest "
            "threshold first, because in the opposite order a group of 25 would "
            "pass the test B2>=5 first and receive only 5 percent.")
    return figure("f202-nif", 760, 374, "".join(body),
                  "A nested IF as a decision flowchart", desc,
                  "Draw the decisions before you write the brackets. The "
                  "flowchart belongs in your design, too.")


@diagram("f202-lookup")
def _lookup():
    """Exact match for a ticket type, approximate match for a discount band."""
    body = [text(380, 22, "Two kinds of lookup: find an exact item, or find "
                 "the band a value falls in", 12, 650, fill=MUTED)]
    # Exact match.
    body.append(text(196, 50, "EXACT MATCH: the price of a ticket type", 10.6,
                     750, fill=TEAL))
    body.append(_cells(24, 62, [120, 90], ["Type", "Price"], TEAL_SOFT, h=24,
                       size=9.6, tones=[TEAL, TEAL]))
    TYPES = [("Adult", "£27.50"), ("Child", "£12.00"),
             ("Concession", "£18.00"), ("Family (2+2)", "£70.00")]
    for i, (k, v) in enumerate(TYPES):
        hit = k == "Concession"
        body.append(_cells(24, 86 + i * 24, [120, 90], [k, v],
                           WARN_SOFT if hit else FILL, h=24, size=9.6))
    body.append(text(129, 200, "table named Tickets", 9.2, 500, fill=MUTED))
    body.append(box(258, 98, 112, 44, None, fill=FILL, stroke=LINE, r=6))
    body.append(text(314, 116, "B2: Concession", 9.6, 650))
    body.append(text(314, 133, "typed by the user", 9, 450, fill=MUTED))
    body.append(path("M258 120 L238 146", stroke=WARN, w=1.6, arrow=True))
    body.append(box(24, 212, 346, 50, None, fill=FILL, stroke=TEAL, r=6))
    body.append(text(36, 232, "=XLOOKUP(B2, Tickets[Type], Tickets[Price])", 9.4,
                     650, anchor="start", fill=TEAL, mono=True))
    body.append(text(36, 251, "=VLOOKUP(B2, Tickets, 2, FALSE)  →  £18.00",
                     9.4, 650, anchor="start", fill=INK, mono=True))
    # Approximate match.
    body.append(text(572, 50, "APPROXIMATE: which discount band?", 10.6, 750,
                     fill=LILAC))
    body.append(_cells(404, 62, [120, 90], ["Group from", "Discount"],
                       LILAC_SOFT, h=24, size=9.6, tones=[LILAC, LILAC]))
    BANDS = [("0", "0%"), ("5", "5%"), ("10", "10%"), ("20", "20%")]
    for i, (k, v) in enumerate(BANDS):
        hit = k == "10"
        body.append(_cells(404, 86 + i * 24, [120, 90], [k, v],
                           WARN_SOFT if hit else FILL, h=24, size=9.6))
    body.append(text(509, 200, "sorted smallest first: essential", 9.2, 600,
                     fill=WARN))
    body.append(box(632, 98, 104, 44, None, fill=FILL, stroke=LINE, r=6))
    body.append(text(684, 116, "group of 14", 9.6, 650))
    body.append(text(684, 133, "between bands", 9, 450, fill=MUTED))
    body.append(path("M632 120 L618 146", stroke=WARN, w=1.6, arrow=True))
    body.append(box(404, 212, 332, 50, None, fill=FILL, stroke=LILAC, r=6))
    body.append(text(416, 232, "=VLOOKUP(14, Bands, 2, TRUE)  →  10%", 9.4, 650,
                     anchor="start", fill=LILAC, mono=True))
    body.append(text(416, 251, "finds the largest band not above 14", 9.4, 500,
                     anchor="start", fill=MUTED))
    body.append(box(24, 276, 712, 76, None, fill=WARN_SOFT, stroke=WARN, r=8))
    body.append(text(380, 298, "Leave out FALSE and VLOOKUP does an approximate "
                     "match: wrong answers, and no error to warn you.", 10.4, 700,
                     fill=WARN))
    body.append(text(380, 318, "#N/A means not found. Catch it for the user: "
                     "=IFERROR(XLOOKUP(…), \"Check the ticket type\")", 9.8,
                     550, fill=INK))
    body.append(text(380, 338, "Prices live once, in the table. Change the "
                     "table and every booking updates.", 9.8, 500, fill=MUTED))
    desc = ("Two lookups side by side. On the left, an exact match: a table "
            "named Tickets lists Adult at 27 pounds 50, Child at 12 pounds, "
            "Concession at 18 pounds and Family, two adults and two children, at "
            "70 pounds. The user types Concession into cell B2, and "
            "=XLOOKUP(B2, Tickets[Type], Tickets[Price]), or the older "
            "=VLOOKUP(B2, Tickets, 2, FALSE), finds the Concession row and "
            "returns 18 pounds. On the right, an approximate match: a table of "
            "bands sorted smallest first, with groups from 0 getting no "
            "discount, from 5 getting 5 percent, from 10 getting 10 percent and "
            "from 20 getting 20 percent. A group of 14 falls between bands, and "
            "=VLOOKUP(14, Bands, 2, TRUE) finds the largest band not above 14 "
            "and returns 10 percent. The table must be sorted smallest first for "
            "this to work. Warnings underneath: leaving out FALSE makes VLOOKUP "
            "do an approximate match, which gives wrong answers with no error; "
            "#N/A means the value was not found and can be caught with IFERROR, "
            "for example showing 'Check the ticket type'; and because prices are "
            "stored once in the table, changing the table updates every booking.")
    return figure("f202-look", 760, 364, "".join(body),
                  "Exact and approximate lookups", desc,
                  "A lookup replaces a nest of IFs whenever the answers come "
                  "from a table.")


@diagram("f202-validation")
def _validation():
    """The input message, the rule, and the stop alert, for one input cell."""
    body = [text(380, 22, "Validation on one input cell: the message, the rule "
                 "and the alert", 12, 650, fill=MUTED)]
    # 1. the cell and its input message
    body.append(text(124, 50, "1  BEFORE TYPING", 10.4, 750, fill=TEAL))
    body.append(_cells(24, 62, [110, 90], ["Ticket price (£)", "27.50"],
                       [FILL, TEAL_SOFT], h=26, size=9.6))
    body.append(box(60, 98, 170, 66, None, fill=FILL, stroke=TEAL, r=6))
    body.append(path("M130 98 L138 90 L146 98", stroke=TEAL, w=1.4, fill=FILL))
    body.append(text(72, 117, "Ticket price", 9.8, 750, anchor="start",
                     fill=TEAL))
    body.append(text(72, 134, "Enter a price in pounds", 9.4, 500,
                     anchor="start"))
    body.append(text(72, 150, "between 5.00 and 60.00", 9.4, 500,
                     anchor="start"))
    # 2. the rule
    body.append(text(380, 50, "2  THE RULE", 10.4, 750, fill=LILAC))
    body.append(box(270, 62, 220, 140, None, fill=FILL, stroke=LILAC, r=8))
    RULE = [("Allow", "Decimal"), ("Data", "between"), ("Minimum", "5"),
            ("Maximum", "60"), ("Error style", "Stop")]
    for i, (k, v) in enumerate(RULE):
        y = 76 + i * 24
        body.append(text(284, y + 14, k, 9.6, 600, anchor="start", fill=MUTED))
        body.append(box(370, y, 106, 20, None, fill=LILAC_SOFT, stroke=LILAC,
                        r=3))
        body.append(text(380, y + 14, v, 9.6, 650, anchor="start"))
    # 3. the alert
    body.append(text(628, 50, "3  A BAD VALUE", 10.4, 750, fill=WARN))
    body.append(_cells(530, 62, [110, 90], ["Ticket price (£)", "75"],
                       [FILL, WARN_SOFT], h=26, size=9.6))
    body.append(box(530, 98, 206, 104, None, fill=FILL, stroke=WARN, r=8))
    body.append(box(530, 98, 206, 22, None, fill=WARN_SOFT, stroke=WARN, r=8))
    body.append('<circle cx="545" cy="109.5" r="6" fill="%s"/><rect x="541.5" y="108.3" width="7" height="2.4" fill="#FFFFFF"/>' % WARN)
    body.append(text(556, 113, "Price out of range", 9.8, 750,
                     anchor="start", fill=WARN))
    body.append(text(542, 140, "Ticket prices must be between", 9.4, 500,
                     anchor="start"))
    body.append(text(542, 156, "£5 and £60. Please re-enter.", 9.4, 500,
                     anchor="start"))
    for i, b in enumerate(["Retry", "Cancel"]):
        body.append(box(600 + i * 66, 170, 58, 22, b, fill=FILL2, stroke=LINE,
                        r=4, label_size=9.4))
    body.append(path("M494 132 L524 132", stroke=LINE, arrow=True))
    body.append(path("M234 132 L264 132", stroke=LINE, arrow=True))
    # Types table.
    TYPES = [("Whole number", "capacity: whole number 1 to 2,000"),
             ("Decimal", "price: decimal 5.00 to 60.00"),
             ("List", "ticket type: Adult, Child, Concession, Family"),
             ("Date", "booking date: on or before the festival date"),
             ("Text length", "booking reference: exactly 8 characters"),
             ("Custom", "=COUNTIF(Refs, A2)=1: no duplicates")]
    for i, (k, v) in enumerate(TYPES):
        col, row = i % 2, i // 2
        x, y = 24 + col * 360, 218 + row * 30
        body.append(box(x, y, 352, 26, None, fill=FILL, stroke=LINE, r=4))
        body.append(text(x + 10, y + 17, k, 9.6, 750, anchor="start",
                         fill=TEAL))
        body.append(text(x + 98, y + 17, v, 9.2, 500, anchor="start",
                         mono=v.startswith("=")))
    body.append(box(24, 312, 712, 40, None, fill=WARN_SOFT, stroke=WARN, r=8))
    body.append(text(380, 337, "Validation checks what is typed. A value pasted "
                     "over the cell can slip past it, so test that too.", 10.2,
                     650, fill=WARN))
    desc = ("Validation set up on one input cell, the ticket price, in three "
            "stages. First, before typing: selecting the cell shows an input "
            "message, 'Ticket price: enter a price in pounds between 5.00 and "
            "60.00'. Second, the rule itself: allow decimal, data between, "
            "minimum 5, maximum 60, error style Stop. Third, a bad value: typing "
            "75 brings up a stop alert titled 'Price out of range' saying ticket "
            "prices must be between 5 and 60 pounds, with Retry and Cancel "
            "buttons, and the value is refused. Below, six types of validation "
            "with an example of each: whole number, capacity between 1 and "
            "2,000; decimal, price between 5.00 and 60.00; list, ticket type "
            "chosen from Adult, Child, Concession and Family; date, booking date "
            "on or before the festival; text length, a booking reference of "
            "exactly 8 characters; and custom, =COUNTIF(Refs, A2)=1 so that no "
            "booking reference appears twice. A warning: validation checks what "
            "is typed, and a value pasted over the cell can slip past it, so "
            "that should be tested as well.")
    return figure("f202-valid", 760, 364, "".join(body),
                  "Data validation on an input cell", desc,
                  "The input message prevents most errors. The alert catches "
                  "the rest.")


# ================================================ TA3: what-if analysis

PX0, PY0, PW, PH = 96, 372, 600, 300
VMIN, VMAX = -4000.0, 2500.0


def _px(p):
    return PX0 + PW * p / 50.0


def _py(v):
    return PY0 - PH * (v - VMIN) / (VMAX - VMIN)


@diagram("f202-what-if-chart")
def _what_if_chart():
    """Profit against ticket price, plotted from the model's own formula."""
    body = [text(380, 24, "Profit against ticket price, from the model's own "
                 "formulas", 12, 650, fill=MUTED)]
    body.append(axes(PX0, PY0, PW, PH, "ticket price (£)", "",
                     xticks=[(p / 50.0, "£%d" % p) for p in range(0, 51, 10)],
                     yticks=[((v - VMIN) / (VMAX - VMIN), money(v))
                             for v in (-4000, -2000, 0, 2000)]))
    body.append('<text x="26" y="%d" text-anchor="middle" font-size="11" '
                'font-weight="650" fill="%s" transform="rotate(-90 26 %d)">'
                'profit (£)</text>' % (PY0 - PH / 2, MUTED, PY0 - PH / 2))
    body.append(line(PX0, _py(0), PX0 + PW, _py(0), stroke=MUTED, w=1.4))
    # The curve, sampled finely; a polygon under the profitable stretch.
    pts = [(p / 20.0, profit(p / 20.0)) for p in range(100, 1001)]
    lo, hi = 15.0, 40.65
    area = ["M%.1f %.1f" % (_px(lo), _py(0))]
    area += ["L%.1f %.1f" % (_px(p), _py(v)) for p, v in pts if lo <= p <= hi]
    area.append("L%.1f %.1f Z" % (_px(hi), _py(0)))
    body.append('<path d="%s" fill="%s" stroke="none" opacity="0.7"/>'
                % (" ".join(area), TEAL_SOFT))
    curve = "M" + " L".join("%.1f %.1f" % (_px(p), _py(v)) for p, v in pts)
    body.append(path(curve, stroke=TEAL, w=2.6))
    # Equal profit at £20 and £35.
    y14 = _py(profit(20))
    body.append(line(_px(20), y14, _px(35), y14, stroke=LILAC, w=1.6,
                     dash="5 4"))
    for p, anchor, dx in ((20, "end", -9), (35, "start", 9)):
        body.append(circle(_px(p), y14, 4.5, fill=LILAC, stroke=LILAC, w=0))
        body.append(text(_px(p) + dx, y14 - 6, "£%d: %d sold" % (p, tickets(p)),
                         9.6, 700, anchor=anchor, fill=LILAC))
    body.append(text(_px(27.5), y14 + 20, "same profit, half the crowd", 9.6, 650,
                     fill=LILAC))
    # Maximum.
    body.append(circle(_px(27.5), _py(profit(27.5)), 5, fill=TEAL, stroke=TEAL,
                       w=0))
    body.append(chip(_px(27.5), 56, "maximum %s at £27.50 (270 sold)"
                     % money(profit(27.5)), size=10))
    body.append(line(_px(27.5), 67, _px(27.5), _py(profit(27.5)) - 6,
                     stroke=TEAL, w=1.2, dash="2 3"))
    # Break-even points.
    for p, cx in ((15.0, 196), (40.65, 664)):
        body.append(circle(_px(p), _py(0), 5, fill=WARN, stroke=WARN, w=0))
        body.append(chip(cx, 164, "break-even £%.2f" % p, fill=FILL,
                         stroke=WARN, text_fill=WARN, size=9.6))
    # The capacity kink.
    kink = (DEMAND_AT_ZERO - CAPACITY) / float(LOST_PER_POUND)
    body.append(circle(_px(kink), _py(profit(kink)), 3.5, fill=FILL, stroke=TEAL,
                       w=1.6))
    body.append(text(246, 300, "below £16.67 it sells out:", 9.6, 650,
                     anchor="start", fill=MUTED))
    body.append(text(246, 314, "400 tickets, whatever the price", 9.6, 500,
                     anchor="start", fill=MUTED))
    body.append(text(214, 226, "loss", 10, 700, fill=WARN))
    body.append(text(636, 232, "loss", 10, 700, fill=WARN))
    body.append(text(430, 176, "profit", 10, 700, fill=TEAL))
    body.append(box(24, 430, 712, 30, None, fill=FILL, stroke=LINE, r=6))
    body.append(text(380, 449, "profit = MIN(400, 600 − 12 × price) × "
                     "(price − £5) − £4,000", 10.4, 650,
                     fill=TEAL, mono=True))
    desc = ("A line graph of profit against ticket price, drawn from the "
            "model's own formula: profit equals the smaller of 400 and 600 minus "
            "12 times the price, multiplied by the price minus 5 pounds, minus "
            "4,000 pounds. The horizontal axis runs from 0 to 50 pounds and the "
            "vertical axis from a loss of 4,000 pounds to a profit of 2,500. "
            "From 5 pounds to 16 pounds 67 the line is straight and rising, "
            "because demand is higher than the capacity of 400, so the festival "
            "sells out whatever the price and every extra pound is extra profit. "
            "It crosses zero, the first break-even point, at exactly 15 pounds. "
            "Above 16 pounds 67 the line curves: each price rise brings more per "
            "ticket but fewer people. Profit peaks at 2,075 pounds at 27 pounds "
            "50, with 270 tickets sold, then falls, crossing zero again at the "
            "second break-even point of 40 pounds 65 and reaching a loss of "
            "4,000 pounds at 50 pounds, where nobody comes. A dashed line joins "
            "two points of equal profit: 20 pounds with 360 tickets sold and 35 "
            "pounds with 180 sold both make 1,400 pounds, so the higher price "
            "earns the same with half the crowd. The area between the two "
            "break-even points, where the event makes a profit, is shaded.")
    return figure("f202-whatif", 760, 472, "".join(body),
                  "Profit against ticket price", desc,
                  "A chart of the model's output against one input is the "
                  "quickest way to see the best value, the break-even points "
                  "and how sensitive the result is.")


@diagram("f202-goal-seek")
def _goal_seek():
    """Goal Seek: from the answer you want back to the input that gives it."""
    body = [text(380, 22, "Goal Seek works backwards: which price gives a "
                 "£1,000 profit?", 12, 650, fill=MUTED)]
    # Dialog.
    body.append(box(24, 44, 260, 196, None, fill=FILL, stroke=LINE, r=8))
    body.append(box(24, 44, 260, 26, None, fill=FILL2, stroke=LINE, r=8))
    body.append(text(38, 62, "Goal Seek", 10.4, 750, anchor="start"))
    FIELDS = [("Set cell:", "$B$14", "profit"),
              ("To value:", "1000", "the target"),
              ("By changing cell:", "$B$3", "ticket price")]
    for i, (k, v, note) in enumerate(FIELDS):
        y = 84 + i * 44
        body.append(text(38, y + 14, k, 9.8, 600, anchor="start", fill=MUTED))
        body.append(box(150, y, 120, 24, None, fill=TEAL_SOFT, stroke=TEAL,
                        r=4))
        body.append(text(160, y + 16, v, 10, 700, anchor="start", mono=True))
        body.append(text(150, y + 36, note, 8.8, 500, anchor="start",
                         fill=MUTED))
    for i, b in enumerate(["OK", "Cancel"]):
        body.append(box(140 + i * 70, 212, 62, 22, b, fill=FILL2, stroke=LINE,
                        r=4, label_size=9.4))
    # Mini graph.
    X0, Y0, W, H = 344, 236, 380, 176
    lo_v, hi_v = -500.0, 2400.0

    def mx(p):
        return X0 + W * (p - 14.0) / 28.0

    def my(v):
        return Y0 - H * (v - lo_v) / (hi_v - lo_v)
    body.append(line(X0, Y0, X0 + W, Y0, stroke=LINE, w=1.4))
    body.append(line(X0, Y0, X0, Y0 - H, stroke=LINE, w=1.4))
    for p in (15, 20, 25, 30, 35, 40):
        body.append(text(mx(p), Y0 + 15, "£%d" % p, 9, 500, fill=MUTED))
    body.append(text(X0 + W / 2, Y0 + 32, "ticket price", 9.6, 650, fill=MUTED))
    pts = [(p / 20.0, profit(p / 20.0)) for p in range(290, 821)]
    pts = [(p, v) for p, v in pts if v >= lo_v]
    body.append(path("M" + " L".join("%.1f %.1f" % (mx(p), my(v))
                                      for p, v in pts), stroke=TEAL, w=2.4))
    body.append(line(X0, my(1000), X0 + W, my(1000), stroke=WARN, w=1.6,
                     dash="6 4"))
    body.append(text(535, 166, "target profit £1,000", 9.6, 700, fill=WARN))
    low, high = seek(1000, 16.7, 27.5), seek(1000, 27.5, 50)
    for start, ans, dx, anchor in ((20.0, low, 7, "start"),
                                   (35.0, high, -7, "end")):
        body.append(circle(mx(start), my(profit(start)), 4, fill=FILL,
                           stroke=LILAC, w=1.6))
        body.append(path("M%.1f %.1f L%.1f %.1f" % (mx(start), my(profit(start)),
                                                    mx(ans), my(1000) - 1),
                         stroke=LILAC, w=1.4, dash="3 3", arrow=True,
                         marker="ah-alt"))
        body.append(circle(mx(ans), my(1000), 5, fill=WARN, stroke=WARN, w=0))
        body.append(text(mx(ans) + dx, my(1000) + 16, "£%.2f" % ans, 9.6, 750,
                         anchor=anchor, fill=WARN))
    body.append(text(535, 196, "start at £20: Goal Seek finds £%.2f" % low,
                     9.6, 650, fill=LILAC))
    body.append(text(535, 214, "start at £35: it finds £%.2f" % high, 9.6, 650,
                     fill=LILAC))
    body.append(box(24, 282, 712, 70, None, fill=FILL, stroke=LINE, r=8))
    body.append(text(380, 304, "Goal Seek changes ONE input cell, by repeated "
                     "trial, until the formula cell reaches the target.", 10.4,
                     700, fill=TEAL))
    body.append(text(380, 323, "It finds one answer. This model has two, and "
                     "which one you get depends on where the price started.",
                     10, 500, fill=INK))
    body.append(text(380, 341, "Record the starting value in your evidence, and "
                     "check the answer by putting it back into the model.", 9.8,
                     500, fill=MUTED))
    desc = ("Goal Seek answering the question: which ticket price gives a "
            "profit of 1,000 pounds? The dialog box has three fields: set cell "
            "$B$14, the profit; to value 1000, the target; by changing cell "
            "$B$3, the ticket price. Beside it, a graph of profit against price "
            "between 14 and 42 pounds, with a dashed horizontal line at the "
            "1,000 pound target. The curve crosses the target twice. Starting "
            "from a price of 20 pounds, Goal Seek moves the price down and finds "
            "%.2f pounds. Starting from 35 pounds, it moves up and finds %.2f "
            "pounds. Goal Seek changes one input cell by repeated trial until "
            "the formula cell reaches the target. It finds one answer, and when "
            "a model has two, which one you get depends on where the input "
            "started, so the starting value belongs in your evidence, and the "
            "answer should be checked by putting it back into the model." % (low, high))
    return figure("f202-goal", 760, 364, "".join(body),
                  "Goal Seek on the ticket model", desc,
                  "What-if analysis runs forwards: change an input, read the "
                  "output. Goal Seek runs backwards.")


@diagram("f202-scenarios")
def _scenarios():
    """Three scenarios at the same price, and the honest range they give."""
    price = 27.5
    SC = [("PESSIMISTIC", 500, 6.0, 4500.0, WARN, WARN_SOFT),
          ("EXPECTED", 600, 5.0, 4000.0, TEAL, TEAL_SOFT),
          ("OPTIMISTIC", 700, 4.5, 3800.0, LILAC, LILAC_SOFT)]
    body = [text(380, 22, "Scenarios: the same price, three sets of assumptions",
                 12, 650, fill=MUTED)]
    results = []
    for i, (name, d, ph, fx, tone, soft) in enumerate(SC):
        x = 24 + i * 152
        t = tickets(price, demand=d)
        pr = profit(price, demand=d, per_head=ph, fixed=fx)
        results.append((name, pr, tone))
        body.append(box(x, 44, 140, 196, None, fill=soft, stroke=tone, r=8))
        body.append(text(x + 70, 64, name, 10, 750, fill=tone))
        ROWS = [("demand at £0", str(d)), ("cost per head", money(ph, True)),
                ("fixed costs", money(fx)), ("price", "£27.50"),
                ("tickets sold", str(int(t)))]
        for r, (k, v) in enumerate(ROWS):
            y = 76 + r * 26
            body.append(text(x + 10, y + 14, k, 9.2, 500, anchor="start",
                             fill=MUTED))
            body.append(text(x + 130, y + 14, v, 9.8, 700, anchor="end"))
        body.append(box(x + 8, 210, 124, 24, None, fill=FILL, stroke=tone, r=5))
        body.append(text(x + 70, 226, "profit " + money(pr), 10.2, 750,
                         fill=tone))
    # Bar chart of the three results.
    BX0, BY0, BW = 500, 222, 236
    zero = 186.0
    scale = 100.0 / 4710.0
    body.append(text(BX0 + BW / 2, 58, "profit by scenario", 10, 700,
                     fill=MUTED))
    body.append(line(BX0, zero, BX0 + BW, zero, stroke=MUTED, w=1.4))
    body.append(text(BX0 - 4, zero + 4, "£0", 9, 600, anchor="end",
                     fill=MUTED))
    for i, (name, pr, tone) in enumerate(results):
        x = BX0 + 18 + i * 74
        h = abs(pr) * scale
        y = zero - h if pr >= 0 else zero
        body.append('<rect x="%d" y="%.1f" width="50" height="%.1f" rx="3" '
                    'fill="%s" stroke="%s" stroke-width="1.2"/>'
                    % (x, y, h, FILL2 if pr < 0 else FILL, tone))
        ly = y - 6 if pr >= 0 else y + h + 14
        body.append(text(x + 25, ly, money(pr), 9.6, 750, fill=tone))
        body.append(text(x + 25, BY0 + 14, name.lower(), 9, 600, fill=MUTED))
    body.append(box(24, 254, 712, 66, None, fill=FILL, stroke=LINE, r=8))
    body.append(text(380, 276, "The single answer is %s. The honest answer is "
                     "'anything from a loss of %s to a profit of %s'."
                     % (money(results[1][1]), money(abs(results[0][1])),
                        money(results[2][1])), 10.4, 700, fill=TEAL))
    body.append(text(380, 296, "Scenario Manager stores each set of inputs under "
                     "a name and builds this summary in one click.", 10, 500,
                     fill=INK))
    body.append(text(380, 313, "A recommendation that survives the pessimistic "
                     "case is worth more than one that only works in the "
                     "expected case.", 9.6, 500, fill=MUTED))
    desc = ("Three scenarios for the ticket model, all at the same price of 27 "
            "pounds 50. Pessimistic: demand at zero pounds of 500 people, a cost "
            "per head of 6 pounds and fixed costs of 4,500 pounds give 170 "
            "tickets and a loss of 845 pounds. Expected: demand of 600, 5 pounds "
            "per head and 4,000 pounds fixed give 270 tickets and a profit of "
            "2,075 pounds. Optimistic: demand of 700, 4 pounds 50 per head and "
            "3,800 pounds fixed give 370 tickets and a profit of 4,710 pounds. A "
            "bar chart shows the three profits, the pessimistic bar falling "
            "below zero. The single answer is 2,075 pounds; the honest answer is "
            "anything from a loss of 845 pounds to a profit of 4,710 pounds. "
            "Scenario Manager stores each set of inputs under a name and builds "
            "this summary in one click, and a recommendation that survives the "
            "pessimistic case is worth more than one that only works in the "
            "expected case.")
    return figure("f202-scen", 760, 332, "".join(body),
                  "Three scenarios for one model", desc,
                  "Scenarios turn one number into a range, which is what a "
                  "client deciding under uncertainty actually needs.")


@diagram("f202-pivot")
def _pivot():
    """A flat list of sales summarised by a pivot table."""
    body = [text(380, 22, "A pivot table summarises a long list without a "
                 "single formula", 12, 650, fill=MUTED)]
    COLS = [56, 98, 44, 76]
    body.append(_cells(24, 44, COLS, ["Date", "Type", "Qty", "Revenue"],
                       TEAL_SOFT, h=24, size=9.4, tones=[TEAL] * 4))
    RAW = [("01/06", "Adult", 2, 55.0), ("01/06", "Child", 3, 36.0),
           ("02/06", "Adult", 4, 110.0), ("02/06", "Family", 1, 70.0),
           ("03/06", "Child", 2, 24.0), ("03/06", "Adult", 1, 27.5)]
    for i, (d, k, q, r) in enumerate(RAW):
        body.append(_cells(24, 68 + i * 24, COLS,
                           [d, k, str(q), money(r, True)], FILL, h=24, size=9.4))
    body.append(text(161, 228, "… and 4,000 more rows", 9.4, 500,
                     fill=MUTED))
    body.append(path("M306 140 L378 140", stroke=TEAL, w=2, arrow=True,
                     marker="ah-accent"))
    body.append(text(342, 128, "PivotTable", 9.6, 750, fill=TEAL))
    body.append(box(388, 44, 128, 96, None, fill=FILL, stroke=LILAC, r=6))
    body.append(text(400, 62, "Rows: Type", 9.6, 650, anchor="start",
                     fill=LILAC))
    body.append(text(400, 82, "Values:", 9.6, 650, anchor="start", fill=LILAC))
    body.append(text(400, 100, "Sum of Qty", 9.4, 500, anchor="start"))
    body.append(text(400, 118, "Sum of Revenue", 9.4, 500, anchor="start"))
    PCOLS = [80, 50, 76]
    body.append(_cells(528, 44, PCOLS, ["Type", "Qty", "Revenue"], LILAC_SOFT,
                       h=24, size=9.4, tones=[LILAC] * 3))
    agg = {}
    for _, k, q, r in RAW:
        a = agg.setdefault(k, [0, 0.0])
        a[0] += q
        a[1] += r
    for i, k in enumerate(["Adult", "Child", "Family"]):
        q, r = agg[k]
        body.append(_cells(528, 68 + i * 24, PCOLS, [k, str(q), money(r, True)],
                           FILL, h=24, size=9.4))
    tq = sum(a[0] for a in agg.values())
    tr = sum(a[1] for a in agg.values())
    body.append(_cells(528, 140, PCOLS, ["Grand total", str(tq), money(tr, True)],
                       FILL2, h=24, size=9.4, tones=[INK, INK, TEAL]))
    body.append(box(388, 176, 346, 56, None, fill=FILL, stroke=LINE, r=6))
    body.append(text(400, 196, "The same numbers as formulas:", 9.6, 650,
                     anchor="start"))
    body.append(text(400, 216, "=SUMIFS(Sales[Revenue], Sales[Type], \"Adult\")",
                     9.2, 650, anchor="start", fill=TEAL, mono=True))
    body.append(box(24, 248, 712, 46, None, fill=WARN_SOFT, stroke=WARN, r=8))
    body.append(text(380, 268, "A pivot table does not update by itself. "
                     "Refresh it after the data changes, and test that you did.",
                     10.2, 700, fill=WARN))
    body.append(text(380, 285, "SUMIFS updates automatically, which is why a "
                     "dashboard is usually built from formulas.", 9.6, 500,
                     fill=MUTED))
    desc = ("A pivot table summarising a list of ticket sales. The list has "
            "columns date, type, quantity and revenue, and six of its rows are "
            "shown: 1 June, adult, 2, 55 pounds; 1 June, child, 3, 36 pounds; 2 "
            "June, adult, 4, 110 pounds; 2 June, family, 1, 70 pounds; 3 June, "
            "child, 2, 24 pounds; 3 June, adult, 1, 27 pounds 50; and a note "
            "that there are thousands more. The pivot table is set with type as "
            "its rows and the sums of quantity and revenue as its values. It "
            "produces: adult 7 tickets, 192 pounds 50; child 5, 60 pounds; family "
            "1, 70 pounds; grand total 13 tickets, 322 pounds 50. The same "
            "numbers can be produced by formulas such as =SUMIFS(Sales[Revenue], "
            "Sales[Type], \"Adult\"). A warning: a pivot table does not update "
            "by itself and must be refreshed after the data changes, whereas "
            "SUMIFS updates automatically, which is why dashboards are usually "
            "built from formulas.")
    return figure("f202-pivot", 760, 306, "".join(body),
                  "A pivot table summarising sales", desc,
                  "Use a pivot table to explore; use formulas for anything the "
                  "client relies on.")


# ============================================== TA2 and TA4: testing

@diagram("f202-test-plan")
def _test_plan():
    """A test plan with every type of test data, and one honest failure."""
    body = [text(380, 22, "Test plan: written before building, completed while "
                 "testing", 12, 650, fill=MUTED)]
    COLS = [26, 150, 98, 80, 210, 148]
    X0 = (760 - sum(COLS)) / 2.0
    body.append(_cells(X0, 40, COLS, ["#", "Purpose", "Test data", "Type",
                                      "Expected result", "Actual result"],
                       TEAL_SOFT, h=26, size=9.4, tones=[TEAL] * 6))
    ROWS = [("1", "Profit at expected price", "price 27.50", "Normal",
             "270 tickets, profit £2,075", "As expected", True),
            ("2", "Hand-checked calculation", "price 20.00", "Normal",
             "360 tickets, revenue £7,200,\nprofit £1,400",
             "As expected", True),
            ("3", "Capacity limit applied", "price 10.00", "Normal",
             "demand 480, so 400 tickets", "As expected", True),
            ("4", "Lowest valid price", "price 5.00", "Boundary",
             "accepted; 400 tickets", "As expected", True),
            ("5", "Highest valid price", "price 60.00", "Boundary",
             "accepted; 0 tickets,\nprofit −£4,000",
             "−120 tickets shown: failed\nMAX(0, …) added; retest passed",
             False),
            ("6", "Price above the range", "price 75", "Invalid",
             "rejected with stop alert", "As expected", True),
            ("7", "Wrong data type", "\"twenty\"", "Erroneous",
             "rejected with stop alert", "As expected", True),
            ("8", "Break-even check", "price 15.00", "Normal",
             "400 tickets, profit £0", "As expected", True)]
    for i, (n, pur, dat, typ, exp, act, ok) in enumerate(ROWS):
        y = 66 + i * 36
        fills = [FILL] * 5 + [FILL if ok else WARN_SOFT]
        tones = [INK, INK, INK, LILAC if typ != "Normal" else TEAL, INK,
                 TEAL if ok else WARN]
        body.append(_cells(X0, y, COLS, [n, pur, dat, typ, exp, act], fills,
                           h=36, size=9.2, tones=tones))
    body.append(box(X0, 366, sum(COLS), 54, None, fill=TEAL_SOFT, stroke=TEAL,
                    r=8))
    body.append(text(380, 387, "Expected results are worked out by hand before "
                     "the test is run, or there is nothing to compare against.",
                     10.2, 700, fill=TEAL))
    body.append(text(380, 406, "Test 5 failed. The record shows the fault, the "
                     "fix and the retest, which is what makes the log believable.",
                     9.8, 500, fill=INK))
    desc = ("A test plan for the ticket model with seven tests and the columns "
            "number, purpose, test data, type, expected result and actual result. "
            "Test 1, normal data: a price of 27.50 should give 270 tickets and a "
            "profit of 2,075 pounds, and did. Test 2, normal: a price of 20.00 "
            "should give 360 tickets, revenue of 7,200 pounds and a profit of "
            "1,400 pounds, worked out by hand, and did. Test 3, normal: a price "
            "of 10.00 gives demand of 480, so the capacity limit should cap "
            "tickets at 400, and did. Test 4, boundary: the lowest valid price, "
            "5.00, should be accepted with 400 tickets, and was. Test 5, "
            "boundary: the highest valid price, 60.00, should be accepted with 0 "
            "tickets and a loss of 4,000 pounds; instead minus 120 tickets were "
            "shown, so MAX of 0 was added to the formula and the retest passed. "
            "Test 6, invalid: a price of 75 should be rejected with a stop "
            "alert, and was. Test 7, erroneous: the text 'twenty' should be "
            "rejected with a stop alert, and was. Test 8, normal: a price of 15.00 "
            "should give 400 tickets and a profit of exactly zero, the "
            "break-even point, and did. Expected results are worked "
            "out by hand before the test is run, and the failed test, with its "
            "fault, fix and retest, is what makes the log believable.")
    return figure("f202-tests", 760, 432, "".join(body),
                  "A test plan for a spreadsheet model", desc,
                  "Normal, boundary, invalid and erroneous data, plus a hand "
                  "check of every calculation.")


@diagram("f202-dashboard")
def _dashboard():
    """A one-screen dashboard with its design decisions annotated."""
    body = [text(380, 22, "A dashboard: the decisions the client needs, on one "
                 "screen", 12, 650, fill=MUTED)]
    X, Y, W, H = 24, 40, 500, 338
    body.append(box(X, Y, W, H, None, fill=FILL, stroke=LINE, r=8))
    body.append(box(X, Y, W, 26, None, fill=FILL2, stroke=LINE, r=8))
    body.append(text(X + 12, Y + 17, "Harbour Lights · Dashboard", 10, 700,
                     anchor="start"))
    body.append(box(X + 330, Y + 4, 160, 18, None, fill=FILL, stroke=LILAC,
                    r=4))
    body.append(text(X + 338, Y + 17, "Scenario: Expected", 9.2, 650,
                     anchor="start", fill=LILAC))
    body.append('<path d="M%g %g h8 l-4 5 z" fill="%s"/>' % (X + 474, Y + 10, LILAC))
    KPI = [("PROFIT", money(profit(27.5)), TEAL, TEAL_SOFT),
           ("TICKETS", "270 / 400", INK, FILL2),
           ("BREAK-EVEN", "£15.00–£40.65", INK, FILL2),
           ("SPARE PLACES", "130", INK, FILL2)]
    for i, (k, v, tone, soft) in enumerate(KPI):
        x = X + 12 + i * 120
        body.append(box(x, Y + 38, 112, 58, None, fill=soft,
                        stroke=TEAL if i == 0 else LINE, r=6))
        body.append(text(x + 56, Y + 56, k, 8.8, 750, fill=MUTED))
        body.append(text(x + 56, Y + 82, v, 12.5 if i != 2 else 10.6, 750,
                         fill=tone))
    # Mini chart.
    CX, CY, CW, CH = X + 30, Y + 290, 300, 160
    body.append(line(CX, CY, CX + CW, CY, stroke=LINE, w=1.2))
    body.append(line(CX, CY, CX, CY - CH, stroke=LINE, w=1.2))

    def cx(p):
        return CX + CW * (p - 5) / 45.0

    def cy(v):
        return CY - CH * (v + 4000) / 6500.0
    body.append(line(CX, cy(0), CX + CW, cy(0), stroke=LINE, w=0.8, dash="3 3"))
    pts = [(p / 10.0, profit(p / 10.0)) for p in range(50, 501, 2)]
    body.append(path("M" + " L".join("%.1f %.1f" % (cx(p), cy(v)) for p, v in pts),
                     stroke=TEAL, w=2))
    body.append(circle(cx(27.5), cy(profit(27.5)), 4.5, fill=WARN, stroke=WARN,
                       w=0))
    body.append(text(cx(27.5) + 8, cy(profit(27.5)) - 6, "current price", 8.8,
                     650, anchor="start", fill=WARN))
    body.append(text(CX + CW / 2, CY + 16, "profit against price", 9, 600,
                     fill=MUTED))
    # Side panel: inputs and status.
    body.append(box(X + 352, Y + 116, 136, 100, None, fill=FILL2, stroke=LINE,
                    r=6))
    body.append(text(X + 362, Y + 134, "Ticket price", 9.2, 650, anchor="start"))
    body.append(line(X + 364, Y + 152, X + 476, Y + 152, stroke=LINE, w=3))
    body.append(circle(X + 364 + 112 * (27.5 - 5) / 55.0, Y + 152, 6, fill=TEAL,
                       stroke=TEAL, w=0))
    body.append(text(X + 362, Y + 176, "£27.50", 11, 750, anchor="start",
                     fill=TEAL))
    body.append(text(X + 362, Y + 200, "a scroll bar form control", 8.6, 500,
                     anchor="start", fill=MUTED))
    body.append(box(X + 352, Y + 228, 136, 34, "PROFIT", fill=TEAL_SOFT,
                    stroke=TEAL, r=6, label_size=11, text_fill=TEAL))
    body.append(box(X + 352, Y + 270, 136, 34, "Find price for target",
                    fill=FILL, stroke=LILAC, r=17, label_size=9.4,
                    text_fill=LILAC))
    # Numbered markers on the dashboard, and the notes they refer to.
    for n, (mx, my) in enumerate([(X + 12, Y + 38), (X + 488, Y + 228),
                                  (cx(27.5), cy(profit(27.5)) - 20),
                                  (X + 330, Y + 4), (X + 488, Y + 270)], 1):
        body.append(marker(n, mx, my))
    body.append(notes(538, 70, 64, 200, [
        ("Four numbers the client asked", "for, most important first"),
        ("Conditional formatting turns", "the status red below £0"),
        ("The chart shows where the", "current price sits"),
        ("A validation drop-down", "switches the scenario"),
        ("A macro button runs Goal Seek", "for users who never would")]))
    desc = ("A one screen dashboard for the ticket model, with its design "
            "decisions annotated. Across the top, a scenario drop-down set to "
            "Expected, built with a validation list. Below it, four tiles in "
            "order of importance: profit 2,075 pounds, highlighted; tickets 270 "
            "of 400; break-even prices 15 pounds to 40 pounds 65; and 130 spare "
            "places. A small chart of profit against price marks "
            "where the current price sits on the curve. A side panel holds a "
            "ticket price control set to 27 pounds 50, a status box reading "
            "PROFIT, and a button labelled 'Find price for target', which runs a "
            "macro. The annotations explain each choice: the four numbers the "
            "client asked for, most important first; conditional formatting "
            "that turns the tile and status red when profit falls below zero; "
            "the chart showing the current price in context; the drop-down that "
            "switches scenario; and a macro button that runs Goal Seek for users "
            "who would never open the Goal Seek dialog themselves.")
    return figure("f202-dash", 760, 390, "".join(body),
                  "A spreadsheet dashboard, annotated", desc,
                  "Design the dashboard for the client's decision, not to show "
                  "off every feature you used.")


# ================================================== TA5: evaluation

@diagram("f202-evaluation-matrix")
def _evaluation():
    """Requirement, verdict, evidence, improvement: every row, every time."""
    body = [text(380, 22, "Evaluating against the requirements: verdict, "
                 "evidence, improvement", 12, 650, fill=MUTED)]
    COLS = [200, 66, 220, 226]
    X0 = (760 - sum(COLS)) / 2.0
    body.append(_cells(X0, 40, COLS, ["Requirement (quoted)", "Met?",
                                      "Evidence", "Improvement and effect"],
                       TEAL_SOFT, h=26, size=9.4, tones=[TEAL] * 4))
    ROWS = [("Calculate profit for any price", "Fully",
             "Tests 1 and 2 match my\nhand calculations", "—"),
            ("Show the break-even price", "Fully",
             "Dashboard tile; test 8:\n£0 profit at £15", "Mark both break-even\npoints on the chart"),
            ("Compare best and worst cases", "Partly",
             "Scenario summary exists;\nthe client wanted a chart",
             "Add a scenario bar chart:\nthe range seen at a glance"),
            ("Usable by untrained volunteers", "Partly",
             "2 of 3 testers needed\nhelp to run Goal Seek",
             "Macro button 'Find price':\nno dialog to learn"),
            ("Protect the formulas", "Fully",
             "Sheet protection: typing in\na formula cell is refused", "—")]
    for i, (req, met, ev, imp) in enumerate(ROWS):
        y = 66 + i * 42
        tone = TEAL if met == "Fully" else WARN
        body.append(_cells(X0, y, COLS, [req, met, ev, imp],
                           [FILL, TEAL_SOFT if met == "Fully" else WARN_SOFT,
                            FILL, FILL], h=42, size=9.2,
                           tones=[INK, tone, INK, INK]))
    body.append(box(X0, 286, sum(COLS), 52, None, fill=FILL, stroke=LINE, r=8))
    body.append(text(380, 306, "An honest \"partly\", with evidence and a fix, "
                     "shows more understanding than \"everything worked\".",
                     10.2, 700, fill=TEAL))
    body.append(text(380, 325, "\"The model works well\" has no requirement, no "
                     "evidence and no improvement, so it earns nothing.", 9.8,
                     500, fill=MUTED))
    desc = ("An evaluation table with the columns requirement, quoted from the "
            "brief; met; evidence; and improvement with its effect. Calculate "
            "profit for any price: fully met, because tests 1 and 2 match the "
            "hand calculations. Show the break-even price: fully met, shown on "
            "a dashboard tile and checked by test 8, which gives zero profit at "
            "15 pounds; the improvement is "
            "to mark both break-even points on the chart. Compare best and worst "
            "cases: partly met, because a scenario summary exists but the client "
            "wanted a chart; the improvement is a scenario bar chart so the "
            "range is seen at a glance. Usable by untrained volunteers: partly "
            "met, because two of three testers needed help to run Goal Seek; the "
            "improvement is a macro button labelled Find price, so there is no "
            "dialog to learn. Protect the formulas: fully met, by sheet "
            "protection, so typing in a formula cell is refused. An honest "
            "partly, with evidence and a fix, shows more understanding than a "
            "claim that everything worked, and 'the model works well' has no "
            "requirement, no evidence and no improvement, so it earns nothing.")
    return figure("f202-eval", 760, 350, "".join(body),
                  "An evaluation matrix", desc,
                  "Quote the requirement, give a verdict, point to the evidence, "
                  "and say how you would improve it.")


# ============================================= the assignment journey

@diagram("f202-nea-journey")
def _journey():
    """The assignment as five stages, with what each one produces."""
    body = [text(380, 22, "The coursework journey, and the evidence each stage "
                 "leaves behind", 12, 650, fill=MUTED)]
    STAGES = [("1 UNDERSTAND", "the brief", ["who the client is", "the problem",
                                             "what success means"], LILAC,
               LILAC_SOFT),
              ("2 PLAN", "Topic Area 2", ["requirements list", "sheet designs",
                                          "data dictionary", "test plan"], TEAL,
               TEAL_SOFT),
              ("3 CREATE", "Topic Area 3", ["formulas, lookups", "validation",
                                            "automation", "charts, what-if"],
               TEAL, TEAL_SOFT),
              ("4 DELIVER", "Topic Area 4", ["tests run, fixed", "dashboard",
                                             "user guide", "results presented"],
               TEAL, TEAL_SOFT),
              ("5 EVALUATE", "Topic Area 5", ["against each need", "feedback used",
                                              "improvements", "own process"],
               LILAC, LILAC_SOFT)]
    for i, (name, sub, items, tone, soft) in enumerate(STAGES):
        x = 20 + i * 146
        body.append(box(x, 44, 132, 182, None, fill=soft, stroke=tone, r=8))
        body.append(text(x + 66, 66, name, 10.4, 750, fill=tone))
        body.append(text(x + 66, 82, sub, 9.2, 500, fill=MUTED))
        for j, s in enumerate(items):
            body.append(box(x + 8, 94 + j * 32, 116, 26, None, fill=FILL,
                            stroke=tone, r=4))
            body.append(text(x + 66, 111 + j * 32, s, 9.2, 550))
        if i < 4:
            body.append(line(x + 132, 135, x + 144, 135, stroke=LINE, w=1.6,
                             arrow=True))
    body.append(path("M686 226 L686 250 L378 250 L378 230", stroke=WARN,
                     w=1.4, dash="5 4", arrow=True))
    body.append(chip(532, 250, "testing and feedback send you back to improve",
                     fill=WARN_SOFT, stroke=WARN, text_fill=WARN, size=9.6))
    body.append(box(20, 272, 716, 40, None, fill=FILL, stroke=LILAC, r=8))
    body.append(text(378, 297, "Topic Area 1, the principles of modelling, sits "
                     "under every stage: the vocabulary, the features, why each "
                     "choice is right.", 10, 650, fill=LILAC))
    desc = ("The spreadsheet modelling coursework as five stages, each with the "
            "evidence it leaves behind. One, understand the brief: who the "
            "client is, the problem, and what success means. Two, plan, which is "
            "Topic Area 2: a requirements list, sheet designs, a data dictionary "
            "and a test plan. Three, create, Topic Area 3: formulas and lookups, "
            "validation, automation, and charts and what-if analysis. Four, "
            "deliver, Topic Area 4: tests run and faults fixed, a dashboard, a "
            "user guide, and the results presented to the client. Five, "
            "evaluate, Topic Area 5: against each requirement, using feedback, "
            "with improvements and reflection on your own process. Topic Area 1, "
            "the principles of modelling, sits under every stage, supplying the "
            "vocabulary, the features and the reasons each choice is right. A "
            "dashed arrow runs from evaluation back to creating: testing and "
            "feedback send you back to improve the model.")
    return figure("f202-nea", 760, 324, "".join(body),
                  "The F202 coursework journey", desc,
                  "Your teacher gives you the current OCR set assignment. Its "
                  "tasks follow this same order.")
