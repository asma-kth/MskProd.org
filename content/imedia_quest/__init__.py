"""The Media Realms: an adventure through Creative iMedia R093, topic by topic.

The battle questions are not written afresh. Each place draws on its lesson's
own checked material: the topic quiz, the stretch quiz challenge, This or That,
Memory Match, Sort It, Link Up and Bug Hunt. Questions are built from those
here, tidied of dashes, and checked before the page is written, so the game
asks exactly what the lessons teach, with the same explanations.
"""
import hashlib
import html
import random
import re

from mskbuild import markup
from content import ks4_imedia, ks4_stretch
from content.imedia_quest import world as W

DASH = re.compile(r"[-\u2010-\u2015\u2212]")
# Dashed terms that read the same with a space, as the rest of the site's games write them.
FIXES = [("Pre-production", "Pre production"), ("pre-production", "pre production"),
         ("Post-production", "Post production"), ("post-production", "post production"),
         ("Multi-platform", "Multi platform"), ("multi-platform", "multi platform"),
         ("re-save", "resave"), ("sub-sections", "sub sections")]

# A Sort It card becomes a question: this is asked, the card is shown, the bins are the options.
SORT_ASK = {
    "the-media-industry": "What is the main purpose of this product?",
    "job-roles-in-media": "Which stage does this role mainly work in?",
    "client-requirements-and-the-brief": "A charity's poster brief: is this requirement explicit (written in the brief) or implicit (just expected)?",
    "target-audience-and-segmentation": "Is this a demographic, a psychographic or a behaviour?",
    "research-methods-and-sources": "For your own project, is this primary or secondary research?",
    "style-content-and-layout": "Which type of media code is this?",
    "pre-production-documents": "Which planning document does this product need?",
    "work-planning-and-workflow": "Which phase does this task belong to?",
    "legislation-and-permissions": "Which body would deal with this case?",
    "file-formats-and-properties": "Is this format lossy, lossless or uncompressed?",
    "distribution-platforms": "Is this a feature of physical or online distribution?",
}
PAIR_ASK = {"Term": ("What does this term mean?", "Which term means this?"),
            "Document": ("What is this document?", "Which document is this?")}

MIN_QUESTIONS = 50   # per place, so three battles rarely repeat a question
LIMITS = {"q": 200, "item": 200, "o": 130, "w": 320}


def tidy(text):
    text = " ".join(str(text or "").split())
    for a, b in FIXES:
        text = text.replace(a, b)
    return text


def plain(text):
    return html.unescape(re.sub(r"<[^>]+>|[`*_]", "", tidy(text))).strip()


def rich(text):
    return markup.inline(tidy(text))


def _topics():
    unit = next(u for u in ks4_imedia.COURSE.units if u.slug == "r093")
    return {t.slug: t for t in unit.topics}


def _stretch():
    for key, slug, name, lessons in ks4_stretch.courses():
        if key == "imedia":
            return {st.lesson: st for st in lessons}
    raise SystemExit("imedia_quest: no Creative iMedia stretch tasks")


def _bank(topic, st):
    """Every question one place can ask, as plain records before tidying."""
    rng = random.Random(topic.slug)
    out = []

    def add(src, q, opts, a, why="", fixed=False, item=""):
        out.append({"src": src, "q": q, "item": item, "o": list(opts), "a": a, "w": why, "fix": fixed})

    for q in topic.quiz:
        add("quiz", q.stem, q.options, q.answer, q.explain, q.arranged)
    for b in st.blitz:
        if b.code:
            continue
        if b.kind == "choice" and 2 <= len(b.options) <= 4:
            add("blitz", b.q, b.options, 0, b.explain)
        elif b.kind == "tf":
            add("blitz", "True or false?", ["True", "False"], 0 if b.answer else 1, b.explain, True, b.q)
    for p in st.picks:
        if not p.code:
            add("pick", p.q, [p.right, p.wrong], 0, p.why)
    fwd, rev = PAIR_ASK.get(st.pair_names[0], PAIR_ASK["Term"])
    for i, p in enumerate(st.pairs):
        others = [x for j, x in enumerate(st.pairs) if j != i]
        d = rng.sample(others, 3)
        add("pair", fwd, [p.b] + [x.b for x in d], 0, "%s: %s." % (p.a, p.b.rstrip(".")), False, p.a)
        d = rng.sample(others, 3)
        add("pair", rev, [p.a] + [x.a for x in d], 0, "%s: %s." % (p.a, p.b.rstrip(".")), False, p.b)
    if st.sort:
        for it in st.sort.items:
            add("sort", SORT_ASK[topic.slug], st.sort.bins, it.bin, it.why, True, it.text)
    for gi, g in enumerate(st.groups):
        others = [x for j, x in enumerate(st.groups) if j != gi]
        for t in g.tiles:
            add("group", 'Which of these belongs with "%s"?' % g.name, [t] + [rng.choice(x.tiles) for x in others], 0,
                "%s belongs with %s. The others belong with %s." % (t, g.name, " and ".join(x.name for x in others)))
    for b in st.bugs:
        for t in b.truths:
            add("bug", "True or false?", ["True", "False"], 0, "", True, t)
        add("bug", "True or false?", ["True", "False"], 1, b.fix, True, b.bug)
    return out


def _finish(lesson, raw):
    """Tidy, drop what cannot be shown without a dash, remove repeats, render and number."""
    seen, out, dropped = set(), [], 0
    for r in raw:
        texts = [r["q"], r["item"], r["w"]] + r["o"]
        if any(DASH.search(tidy(t)) for t in texts):
            dropped += 1
            continue
        key = (plain(r["q"]) + "|" + plain(r["item"])).lower()
        if key in seen:
            continue
        seen.add(key)
        qid = hashlib.sha1((lesson + "|" + key).encode("utf-8")).hexdigest()[:8]
        rec = {"id": qid, "q": rich(r["q"]), "o": [rich(o) for o in r["o"]], "a": r["a"]}
        if r["item"]:
            rec["i"] = rich(r["item"])
        if r["w"]:
            rec["w"] = rich(r["w"])
        if r["fix"]:
            rec["f"] = 1
        out.append(rec)
    return out, dropped


def _strip_spec(title):
    return re.sub(r"^R093 TA\d:\s*", "", title)


def payload():
    topics, stretch = _topics(), _stretch()
    places = []
    for p in W.PLACES:
        t, st = topics[p["lesson"]], stretch[p["lesson"]]
        qs, dropped = _finish(p["lesson"], _bank(t, st))
        guide = dict(p["guide"])
        guide["look"] = dict(guide["look"], skin=guide["look"]["skin"] - 1)
        places.append({
            "id": p["lesson"], "realm": p["realm"], "name": p["name"], "x": p["x"], "y": p["y"],
            "topic": tidy(_strip_spec(t.title)), "spec": t.spec, "url": "/ks4/imedia/%s/" % t.slug,
            "guide": guide, "intro": [tidy(x) for x in p["intro"]],
            "fact": "" if DASH.search(tidy(t.fact)) else tidy(t.fact),
            "terms": [[tidy(a), tidy(b)] for a, b in t.keyterms],
            "monsters": p["monsters"], "qs": qs, "dropped": dropped,
        })
    return {
        "title": W.TITLE, "tagline": W.TAGLINE, "story": W.STORY, "elements": W.ELEMENTS,
        "realms": W.REALMS, "places": places, "final": W.FINAL, "starters": W.STARTERS,
        "shop": W.SHOP, "skins": W.SKINS, "hairs": W.HAIRS,
    }


def validate(data=None):
    """Raise SystemExit listing every problem; return the number of questions checked."""
    data = data or payload()
    problems = []
    lessons = [t.slug for t in _topics().values()]
    if sorted(p["id"] for p in data["places"]) != sorted(lessons):
        problems.append("the places do not match the R093 lessons one for one")
    monster_ids, names = set(), set()

    def texts(obj):
        if isinstance(obj, str):
            yield obj
        elif isinstance(obj, dict):
            for k, v in obj.items():
                if k not in ("art", "c", "c2", "colour", "deep", "ground", "url", "id", "realm", "look", "qs"):
                    yield from texts(v)
        elif isinstance(obj, list):
            for v in obj:
                yield from texts(v)

    for s in texts({k: v for k, v in data.items() if k not in ("places", "skins", "hairs")}):
        if DASH.search(s):
            problems.append("a dash in the game text: %r" % s)
    n = 0
    for p in data["places"]:
        where = p["id"]
        for s in texts(p):
            if DASH.search(s):
                problems.append("%s: a dash in the game text: %r" % (where, s))
        if len(p["monsters"]) != 3 or not p["monsters"][2].get("tamed"):
            problems.append("%s: needs two wild monsters and a guardian with a tamed name" % where)
        for m in p["monsters"]:
            if m["id"] in monster_ids or m["name"] in names:
                problems.append("%s: monster %s is not unique" % (where, m["id"]))
            monster_ids.add(m["id"]); names.add(m["name"])
            if m["el"] not in data["elements"]:
                problems.append("%s: %s has no element" % (where, m["id"]))
            if len(m["taunts"]) < 2 or not m["cleared"].endswith("."):
                problems.append("%s: %s needs two taunts and a cleared line ending in a full stop" % (where, m["id"]))
        if len(p["qs"]) < MIN_QUESTIONS:
            problems.append("%s: only %d questions" % (where, len(p["qs"])))
        ids = set()
        for q in p["qs"]:
            n += 1
            w = "%s %s" % (where, q["id"])
            if q["id"] in ids:
                problems.append("%s: repeated id" % w)
            ids.add(q["id"])
            opts = [plain(o).lower() for o in q["o"]]
            if not 2 <= len(opts) <= 4 or len(set(opts)) != len(opts) or not all(opts):
                problems.append("%s: options must be 2 to 4 different, non empty answers: %s" % (w, q["o"]))
            if not 0 <= q["a"] < len(q["o"]):
                problems.append("%s: the answer is not one of the options" % w)
            for key in ("q", "i", "w"):
                if key in q and len(plain(q[key])) > LIMITS["item" if key == "i" else key]:
                    problems.append("%s: %s is too long" % (w, key))
            for o in q["o"]:
                if len(plain(o)) > LIMITS["o"]:
                    problems.append("%s: an option is too long: %s" % (w, o))
            if not plain(q["q"]):
                problems.append("%s: no question" % w)
    if problems:
        raise SystemExit("The Media Realms failed its checks:\n  " + "\n  ".join(problems[:60]))
    return n
