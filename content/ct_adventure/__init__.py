"""The Computational Thinking Adventure: four worlds of ten playable levels.

Each world module holds a list of LEVELS. A level is plain data: what the
student reads (learn, task, hints), how the game is set up (engine and data),
what counts as right (the solution inside data), and what Pixel says when it is
done. The JavaScript in static/js/ct/ draws and plays it; nothing here knows
about the page. tools/check_ct.mjs proves every level's solution passes its own
checker and that wrong answers fail.
"""
import re

from . import decomposition, abstraction, patterns, algorithms, bonus

WORLDS = [
    dict(id="decomposition", n=1, name="Decomposition", tag="Break It Down!", place="Builder Bay",
         colour="#EA580C", light="#FFEDD5", deep="#9A3412",
         badge="decomp", levels=decomposition.LEVELS,
         about="Break a big problem into smaller problems you can solve one at a time."),
    dict(id="abstraction", n=2, name="Abstraction", tag="Focus on What Matters!", place="Lookout Peaks",
         colour="#0284C7", light="#E0F2FE", deep="#075985",
         badge="abstract", levels=abstraction.LEVELS,
         about="Keep the details that matter for the problem and leave out the rest."),
    dict(id="patterns", n=3, name="Pattern Recognition", tag="Spot the Pattern!", place="Crystal Caves",
         colour="#9333EA", light="#F3E8FF", deep="#6B21A8",
         badge="pattern", levels=patterns.LEVELS,
         about="Find what repeats or stays the same, and use the rule to predict and to save work."),
    dict(id="algorithms", n=4, name="Algorithms", tag="Think Step by Step!", place="Robot City",
         colour="#059669", light="#D1FAE5", deep="#065F46",
         badge="algo", levels=algorithms.LEVELS,
         about="Design precise steps, as flowcharts and pseudocode, then test and fix them."),
]

BANDS = {1: "Beginner", 2: "Beginner", 3: "Beginner", 4: "Intermediate", 5: "Intermediate",
         6: "Intermediate", 7: "Advanced", 8: "Advanced", 9: "Expert", 10: "Expert"}

BADGES = [
    dict(id="decomp", name="Decomposition Detective", icon="puzzle",
         desc="Finish all ten Decomposition levels.", rule=dict(world="decomposition")),
    dict(id="abstract", name="Abstraction Architect", icon="map",
         desc="Finish all ten Abstraction levels.", rule=dict(world="abstraction")),
    dict(id="pattern", name="Pattern Hunter", icon="gem",
         desc="Finish all ten Pattern Recognition levels.", rule=dict(world="patterns")),
    dict(id="algo", name="Algorithm Engineer", icon="gear",
         desc="Finish all ten Algorithms levels.", rule=dict(world="algorithms")),
    dict(id="flow", name="Flowchart Master", icon="flow",
         desc="Finish every flowchart level: Algorithms 4, 5, 7 and 10.",
         rule=dict(levels=["algorithms-4", "algorithms-5", "algorithms-7", "algorithms-10"])),
    dict(id="pseudo", name="Pseudocode Pro", icon="code",
         desc="Finish Pattern Recognition 9 and Algorithms 8 and 9, and run a program in the Pseudocode Playground.",
         rule=dict(levels=["patterns-9", "algorithms-8", "algorithms-9"], stat="playground")),
    dict(id="debug", name="Debugging Genius", icon="bug",
         desc="Earn three stars on every debugging level: Pattern Recognition 8 and Algorithms 7 and 8.",
         rule=dict(levels=["patterns-8", "algorithms-7", "algorithms-8"], stars=3)),
    dict(id="champion", name="Computational Thinking Champion", icon="trophy",
         desc="Finish all forty levels.", rule=dict(all=True)),
]

# Opened in this order as a student completes 5, 10, 20, 30 and 40 levels.
CHESTS = [
    dict(at=5, wear="party", wear_name="Party hat"),
    dict(at=10, wear="shades", wear_name="Cool shades"),
    dict(at=20, wear="scarf", wear_name="Explorer's scarf"),
    dict(at=30, wear="wizard", wear_name="Wizard hat"),
    dict(at=40, wear="crown", wear_name="Golden crown"),
]

REQUIRED = ("title", "engine", "objective", "learn", "task", "data", "hints", "skill", "cheer",
            "remember", "curriculum", "solution")


def _sentences(text):
    text = re.sub(r"\b(e\.g|i\.e|etc)\.", "x", text)
    return len([s for s in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"'(])", text.strip()) if s])


def levels():
    out = []
    for w in WORLDS:
        for i, lv in enumerate(w["levels"], 1):
            d = dict(lv)
            d["id"] = "%s-%d" % (w["id"], i)
            d["world"] = w["id"]
            d["n"] = i
            d["band"] = BANDS[i]
            out.append(d)
    return out


def validate():
    """Stop the build if a level is missing a part or explains itself at length."""
    problems = []
    for lv in levels():
        lid = lv["id"]
        for k in REQUIRED:
            if k not in lv or lv[k] in ("", None, [], {}):
                problems.append("%s: missing %s" % (lid, k))
        if len(lv.get("hints", [])) != 3:
            problems.append("%s: needs exactly three hints" % lid)
        if _sentences(lv.get("learn", "")) > 3:
            problems.append("%s: learn is more than three sentences" % lid)
        if _sentences(lv.get("task", "")) > 2:
            problems.append("%s: task is more than two sentences" % lid)
        rem = lv.get("remember") or {}
        if not (rem.get("q") and len(rem.get("options", [])) >= 3 and 0 <= rem.get("answer", -1) < len(rem.get("options", []))):
            problems.append("%s: remember question incomplete" % lid)
    if problems:
        raise ValueError("Computational Thinking Adventure:\n  " + "\n  ".join(problems))
    return len(levels())


def bonus_levels():
    out = []
    for i, b in enumerate(bonus.BONUS, 1):
        d = dict(b)
        d.update(id="bonus-%d" % i, n=i, band="Bonus", bonus=True)
        out.append(d)
    return out


def payload():
    """Everything the page needs, as one JSON-ready dict."""
    worlds = [{k: v for k, v in w.items() if k != "levels"} for w in WORLDS]
    for w in worlds:
        w["count"] = len(next(x for x in WORLDS if x["id"] == w["id"])["levels"])
    return dict(worlds=worlds, levels=levels(), bonus=bonus_levels(), badges=BADGES, chests=CHESTS)
