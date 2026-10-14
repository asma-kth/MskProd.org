"""More OCR Data Analytics illustrations: who does what in a data team, and what big data
does for and to organisations."""
import math

from .illus import Canvas, PAL, INK, ARROW, figure, illustration, _n
from . import illus_props as P
from . import illus_glyphs as G
from .illus_society import scales


def wrap(text, n):
    out, cur = [], ""
    for w in text.split():
        if len(cur) + len(w) + 1 > n and cur:
            out.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    out.append(cur)
    return out


@illustration("data-roles")
def _roles():
    cv = Canvas(800, 500).backdrop()
    cv.add(P.card(cv, 14, 24, 772, 56, 16), P.badge(cv, 36, 52, 1))
    cv.add(P.lift(cv, 60, 36, 150, 32, "sun", 9, 3, hl=False), cv.text(135, 57, "Data architect", 14, 800, fill=INK), cv.text(222, 57, "decides how data is modelled and how the systems fit together", 14, 700, anchor="start", cls="il-ink"))
    roles = [("Data engineer", "teal", "builds the pipelines that deliver reliable data", "SQL, Python, cloud tools", ("tan", "black", "teal")),
             ("Database administrator", "sky", "keeps the databases fast, backed up and secure", "SQL, monitoring tools", ("light", "brown", "sky")),
             ("Data analyst", "mint", "answers questions from existing data", "SQL, spreadsheets, BI tools", ("brown", "black", "mint")),
             ("Data scientist", "lilac", "predicts with statistics and models", "Python or R, ML libraries", ("pale", "blond", "plum")),
             ("BI analyst", "coral", "builds the dashboards the business runs on", "BI platforms, SQL", ("deep", "black", "coral"))]
    for i, (name, col, does, tools, (skin, hair, shirt)) in enumerate(roles):
        x = 14 + i * 156
        cv.add(P.card(cv, x, 100, 148, 270, 16))
        cv.add(cv.circle(x + 74, 164, 40, "var(--il-band)"), P.person(cv, x + 44, 126, .5, skin, hair, shirt, ("short", "long", "bun", "curly", "short")[i]))
        label = "DB administrator" if name.startswith("Database") else name
        cv.add(P.lift(cv, x + 8, 212, 132, 26, col, 8, 3, hl=False), cv.text(x + 74, 230, label, 12, 800, fill=INK))
        for j, ln in enumerate(wrap(does, 19)):
            cv.add(cv.text(x + 74, 262 + j * 16, ln, 12.5, 700, cls="il-ink"))
        for j, ln in enumerate(wrap(tools, 20)):
            cv.add(cv.text(x + 74, 338 + j * 14, ln, 11.5, 650, cls="il-ink2", mono=True))
        if i < 4:
            cv.add(P.arrow(cv, [(x + 150, 164), (x + 156, 164)], ARROW, 3, 6))
    cv.add(P.card(cv, 14, 390, 772, 92, 16), P.badge(cv, 36, 416, 2))
    cv.add(P.lift(cv, 60, 404, 190, 32, "red", 9, 3, hl=False), cv.text(155, 425, "Governance and security", 13, 800, fill="#FFFFFF"), cv.text(262, 425, "policy, quality standards, protection against loss, breach and misuse", 13.5, 700, anchor="start", cls="il-ink"))
    cv.add(cv.text(60, 458, "Analyst or scientist?", 13.5, 800, anchor="start", cls="il-ink"), cv.text(222, 454, "the analyst explains what happened, and why", 13.5, 650, anchor="start", cls="il-ink2"), cv.text(222, 472, "the scientist predicts what will happen", 13.5, 650, anchor="start", cls="il-ink2"))
    return figure(
        "data-roles", cv, "Who does what in a data team: architect, engineer, administrator, analyst, scientist and BI analyst",
        "The main roles in a data team. A data architect decides how data is modelled and how the systems fit together. The data engineer builds "
        "the pipelines that deliver reliable data, using SQL, Python and cloud tools. The database administrator keeps the databases fast, backed up and "
        "secure. The data analyst answers questions from existing data, using SQL, spreadsheets and BI tools. The data scientist predicts using "
        "statistics and models, in Python or R. The business intelligence analyst builds the dashboards the business runs on. Governance and "
        "security cover the whole team: policy, quality standards and protection against loss, breach and misuse. The analyst explains what "
        "happened and why, and the scientist predicts what will happen.",
        ["The architect designs how it all fits together.", "Engineers, administrators, analysts, scientists and BI analysts each do one part of getting value from data.",
         "Governance and security look after quality, compliance and protection across all of it."],
        "The engineer makes the data available and trustworthy. The analyst uses it. The scientist builds models from it.")


@illustration("big-data-impacts")
def _impacts():
    cv = Canvas(800, 500).backdrop()
    cv.add(P.card(cv, 14, 30, 360, 330, 20, "Benefits", "green"), P.badge(cv, 36, 56, 1))
    for i, (a_, b_) in enumerate((("Better decisions", "evidence, not instinct"), ("Personalisation", "recommendations and tailored prices"), ("Efficiency", "routing, stock and energy fitted to demand"),
                                   ("Predictive maintenance", "fix a part before it fails"), ("Fraud detection", "patterns no reviewer could see"))):
        y = 92 + i * 52
        cv.add(P.tick(cv, 42, y + 8, 10), cv.text(62, y + 6, a_, 14.5, 800, anchor="start", cls="il-ink"), cv.text(62, y + 25, b_, 12.5, 650, anchor="start", cls="il-ink2"))
    cv.add(P.card(cv, 426, 30, 360, 330, 20, "Costs and risks", "coral"), P.badge(cv, 448, 56, 2))
    for i, (a_, b_) in enumerate((("Cost", "storage, compute, staff, governance"), ("Skills shortage", "people are scarcer than the data"), ("Concentrated risk", "one breach exposes far more"),
                                   ("Surveillance", "profiling people without their say"), ("Bias and error", "decisions that look neutral but are not"))):
        y = 92 + i * 52
        cv.add(P.cross(cv, 454, y + 8, 10), cv.text(474, y + 6, a_, 14.5, 800, anchor="start", cls="il-ink"), cv.text(474, y + 25, b_, 12.5, 650, anchor="start", cls="il-ink2"))
    cv.add(cv.circle(400, 195, 36, "var(--il-bg1)"), cv.group(scales(cv, 0, 4), 400, 190, .55))
    cv.add(P.card(cv, 14, 380, 772, 102, 18, "Across sectors", "sky"), P.badge(cv, 36, 406, 3))
    for i, (a_, b_) in enumerate((("Healthcare", "screening, outbreaks"), ("Transport", "live routing"), ("Retail", "demand forecasts"), ("Finance", "fraud, credit scores"), ("Energy", "smart grids"), ("Public services", "planning, targeting"))):
        x = 28 + i * 126
        cv.add(P.lift(cv, x, 418, 116, 54, "paper", 10, 4, hl=False), cv.text(x + 58, 440, a_, 13, 800, fill=INK), cv.text(x + 58, 458, b_, 11, 650, fill="#4A6470"))
    return figure(
        "big-data-impacts", cv, "The benefits and the costs and risks of big data, and some sectors that use it",
        "Big data has benefits and costs, drawn as the two sides of a balance. The benefits are better decisions made on evidence instead of "
        "instinct, personalisation, efficiency from routing, stock and energy fitted to demand, predictive maintenance that fixes a part before it "
        "fails, and fraud detection from patterns no reviewer could see. The costs and risks are the ongoing cost of storage, compute, staff and "
        "governance, a shortage of skilled people, concentrated risk because one breach exposes far more, surveillance and profiling of people "
        "without their say, and bias and error in decisions that look neutral. Sectors that use big data include healthcare for screening and "
        "outbreaks, transport for live routing, retail for demand forecasts, finance for fraud and credit scores, energy for smart grids and "
        "public services for planning and targeting support.",
        ["The benefits are real: better decisions, personalisation, efficiency, predictive maintenance and fraud detection.",
         "So are the costs and risks: ongoing cost, scarce skills, concentrated risk, surveillance and bias.", "Every sector uses big data in its own way."],
        "A strong answer weighs both sides for a named organisation, then reaches a judgement.")
