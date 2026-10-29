"""Key Stage 3 stretch tasks: one game for every Year 8 and Year 9 lesson.

Each lesson of a unit (a section of its topic page) gets a page of its own with
three rounds: a quiz game against the clock, short written answers, and long
written answers marked against a mark scheme. The game itself is
static/js/stretch.js; this module writes the pages, the hub that lists them,
and the link under each lesson on the topic pages.

Every page also carries the whole task as plain HTML: it is what a browser
without JavaScript shows, and what prints when a teacher wants it on paper.
"""
import json

from mskbuild import cat, markup
from mskbuild.render import (SITE_NAME, SITE_URL, crumbs, crumbs_ld, esc, ico, layout, write)
from mskbuild.util import slugify
from mskbuild import stretchcheck
from content import ks3
from content import ks3_stretch

HUB = "/ks3/stretch/"
HUB_TITLE = "Stretch tasks"
HUB_LEAD = "A quiz game, short answers and long answers for every Year 8 and Year 9 lesson."

ROUNDS = [("Quiz Blitz", "blitz"), ("Quick Fire", "short"), ("Big Think", "long")]

# Seconds on the clock for each kind of game question, before any extra for
# code to read or a long question.
TIME = {"choice": 20, "tf": 15, "multi": 30, "order": 40, "type": 30}

SHAPES = {
    "tri": '<path d="M12 3.5 21.5 20h-19Z"/>',
    "dia": '<path d="M12 2.5 21.5 12 12 21.5 2.5 12Z"/>',
    "cir": '<circle cx="12" cy="12" r="9.5"/>',
    "sq": '<rect x="3.5" y="3.5" width="17" height="17" rx="2.5"/>',
}


# The drifting shapes behind the lobby and the game.
BG = "".join('<i class="st-s-%s"></i>' % k for k in ("tri", "cir", "sq", "dia", "cir", "tri", "dia", "sq"))


def _round_icon(kind):
    """The drawn picture on each round's card."""
    if kind == "blitz":
        cells = [("tri", "#D7263D", "#fff", 0, 0), ("dia", "#1F5FD1", "#fff", 26, 0),
                 ("cir", "#F2B705", "#1F1A05", 0, 26), ("sq", "#1E7B34", "#fff", 26, 26)]
        inner = "".join('<g transform="translate(%d %d)"><rect width="24" height="24" rx="6" fill="%s"/>'
                        '<g transform="translate(4 4) scale(.67)" fill="%s">%s</g></g>' % (x, y, c, ink, SHAPES[s])
                        for s, c, ink, x, y in cells)
        return '<svg viewBox="0 0 50 50" aria-hidden="true" focusable="false">%s</svg>' % inner
    if kind == "short":
        return ('<svg viewBox="0 0 50 50" aria-hidden="true" focusable="false">'
                '<rect x="3" y="6" width="44" height="30" rx="9" fill="#FDE68A" stroke="#1E293B" stroke-width="2.4"/>'
                '<path d="M13 36 9 45 21 36Z" fill="#FDE68A" stroke="#1E293B" stroke-width="2.4" stroke-linejoin="round"/>'
                '<path d="M12 16h18M12 25h12" stroke="#1E293B" stroke-width="3" stroke-linecap="round"/>'
                '<path d="M33 27 41 12l4 2-8 15-5 2Z" fill="#F97316" stroke="#1E293B" stroke-width="2" stroke-linejoin="round"/>'
                '</svg>')
    return ('<svg viewBox="0 0 50 50" aria-hidden="true" focusable="false">'
            '<path d="M25 7a13 13 0 0 0-7.5 23.6c1.6 1.2 2.5 2.8 2.5 4.6V37h10v-1.8c0-1.8.9-3.4 2.5-4.6A13 13 0 0 0 25 7Z" '
            'fill="#C4B5FD" stroke="#1E293B" stroke-width="2.4" stroke-linejoin="round"/>'
            '<path d="M20 41h10M21.5 45h7" stroke="#1E293B" stroke-width="2.6" stroke-linecap="round"/>'
            '<path d="M21 20c1-3 3-4.5 5.5-4.5" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/>'
            '<path d="M5 20H1.5M48.5 20H45M9 6.5 6.5 4M41 6.5 43.5 4M25 2.5V0" stroke="#F59E0B" stroke-width="2.6" '
            'stroke-linecap="round"/></svg>')


def records():
    """Every stretch task in teaching order, with what its pages need to know."""
    topics = {t.slug: (u, t) for u in ks3.COURSE.units for t in u.topics}
    out = []
    for slug, lessons in ks3_stretch.units():
        unit, topic = topics[slug]
        for n, st in enumerate(lessons, 1):
            sec = next(s for s in topic.sections if s.title == st.lesson)
            out.append({
                "stretch": st, "topic": topic, "unit": unit, "n": n,
                "key": "%s/%d" % (slug, n),
                "url": "%s%s/lesson-%d/" % (HUB, slug, n),
                "lesson_url": "/ks3/%s/#%s" % (slug, sec.id or slugify(sec.title)),
                "year": unit.title,
            })
    return out


def attach_links():
    """Give each Year 8 and 9 topic a link to the stretch task for every lesson.

    Called before the topic pages are built, so each lesson can end with it."""
    for r in records():
        links = getattr(r["topic"], "stretch", None)
        if links is None:
            links = r["topic"].stretch = {}
        links[r["stretch"].lesson] = (r["url"], r["n"])


def check():
    """Prove every task, and that every Year 8 and 9 lesson has one."""
    units = ks3_stretch.units()
    topics = {t.slug: t for u in ks3.COURSE.units for t in u.topics}
    stretchcheck.validate(units, topics)
    have = {(slug, st.lesson) for slug, lessons in units for st in lessons}
    missing = []
    for u in ks3.COURSE.units:
        if u.slug not in ("year-8", "year-9"):
            continue
        for t in u.topics:
            for s in t.sections:
                if (t.slug, s.title) not in have and (t.slug, s.title) not in ks3_stretch.NOT_LESSONS:
                    missing.append("%s: %s" % (t.slug, s.title))
    return missing


# ------------------------------------------------------------------ payload

def _code(code, lang):
    if not code:
        return ""
    if lang in ("python", "pseudo"):
        return markup._highlight(code.strip("\n"), lang)
    return esc(code.strip("\n"))


def _seconds(b):
    t = b.time or TIME[b.kind]
    if not b.time:
        if b.code:
            t += 10 + 5 * max(0, b.code.count("\n") - 3)
        if len(b.q) > 140:
            t += 5
    return t


def _blitz(b):
    d = {"k": b.kind, "q": markup.inline(b.q), "x": markup.inline(b.explain), "t": _seconds(b)}
    if b.code:
        d["c"] = _code(b.code, b.lang)
    if b.kind in ("choice", "multi", "order"):
        d["o"] = [markup.inline(o) for o in b.options]
    if b.kind == "multi":
        d["n"] = b.n
    if b.kind == "tf":
        d["a"] = bool(b.answer)
    if b.kind == "type":
        d["a"] = list(b.accept)
    return d


def _written(w):
    d = {"q": markup.inline(w.q), "m": w.marks, "cmd": w.command,
         "p": [{"t": markup.inline(p.text), "a": p.any} for p in w.points],
         "model": markup.model(w.model)}
    if w.frame:
        d["f"] = list(w.frame)
    if w.code:
        d["c"] = _code(w.code, w.lang)
    return d


def payload(r, nxt):
    st = r["stretch"]
    return {
        "key": r["key"], "lesson": st.lesson, "n": r["n"],
        "unit": r["topic"].title, "spec": r["topic"].spec, "year": r["year"],
        "back": r["lesson_url"],
        "next": {"t": nxt["stretch"].lesson, "u": nxt["url"]} if nxt else None,
        "blitz": [_blitz(b) for b in st.blitz],
        "short": [_written(w) for w in st.short],
        "long": [_written(w) for w in st.long],
    }


# -------------------------------------------------------------- the sheet

def _sheet_code(code, lang):
    return '<pre class="st-sheet-code"><code>%s</code></pre>' % _code(code, lang) if code else ""


def _sheet(r):
    """The whole task as a worksheet, with its answers after it."""
    st = r["stretch"]
    qs, keys = [], []
    for i, b in enumerate(st.blitz, 1):
        body = ""
        if b.kind in ("choice", "multi"):
            body = '<ul class="st-sheet-opts">%s</ul>' % "".join(
                "<li><span class=\"st-box\"></span>%s</li>" % markup.inline(o) for o in _sheet_order(b))
            if b.kind == "multi":
                body = '<p class="st-sheet-hint">Tick %d.</p>' % b.n + body
        elif b.kind == "tf":
            body = '<ul class="st-sheet-opts st-sheet-tf"><li><span class="st-box"></span>True</li><li><span class="st-box"></span>False</li></ul>'
        elif b.kind == "order":
            body = ('<p class="st-sheet-hint">Number these 1 to %d.</p><ul class="st-sheet-opts">%s</ul>'
                    % (len(b.options), "".join("<li><span class=\"st-box\"></span>%s</li>" % markup.inline(o)
                                               for o in _sheet_order(b))))
        else:
            body = '<p class="st-line"></p>'
        qs.append('<li class="st-sheet-q"><p>%s</p>%s%s</li>' % (markup.inline(b.q), _sheet_code(b.code, b.lang), body))
        if b.kind == "choice":
            ans = markup.inline(b.options[0])
        elif b.kind == "multi":
            ans = "; ".join(markup.inline(o) for o in b.options[:b.n])
        elif b.kind == "tf":
            ans = "True" if b.answer else "False"
        elif b.kind == "order":
            ans = " &rarr; ".join(markup.inline(o) for o in b.options)
        else:
            ans = esc(b.accept[0])
        keys.append("<li><b>%s</b> %s</li>" % (ans, markup.inline(b.explain)))

    def written(items, lines):
        out, key = [], []
        for w in items:
            out.append('<li class="st-sheet-q"><p>%s <span class="st-sheet-marks">[%d mark%s]</span></p>%s%s</li>'
                       % (markup.inline(w.q), w.marks, "" if w.marks == 1 else "s", _sheet_code(w.code, w.lang),
                          '<p class="st-line"></p>' * lines))
            key.append('<li><ul class="st-sheet-ms">%s</ul><div class="st-sheet-model"><b>Model answer</b>%s</div></li>'
                       % ("".join("<li>%s</li>" % markup.inline(p.text) for p in w.points), markup.model(w.model)))
        return "".join(out), "".join(key)

    sq, sk = written(st.short, 3)
    lq, lk = written(st.long, 9)
    return """<section class="st-sheet" id="st-sheet" aria-labelledby="st-sheet-title">
  <h2 id="st-sheet-title">%s: the questions</h2>
  <h3>Round 1: Quiz Blitz</h3><ol class="st-sheet-list">%s</ol>
  <h3>Round 2: Quick Fire</h3><ol class="st-sheet-list">%s</ol>
  <h3>Round 3: Big Think</h3><ol class="st-sheet-list">%s</ol>
  <details class="st-key" id="st-key">
    <summary>Answers</summary>
    <h3>Round 1</h3><ol class="st-sheet-list">%s</ol>
    <h3>Round 2</h3><ol class="st-sheet-list">%s</ol>
    <h3>Round 3</h3><ol class="st-sheet-list">%s</ol>
  </details>
</section>""" % (esc(st.lesson), "".join(qs), sq, lq, "".join(keys), sk, lk)


def _sheet_order(b):
    """A fixed, deterministic order for options on paper, never the written one."""
    import hashlib
    opts = list(b.options)
    seed = int(hashlib.sha256(b.q.encode("utf-8")).hexdigest(), 16)
    shifted = opts[seed % len(opts):] + opts[:seed % len(opts)]
    if b.kind == "order" and shifted == opts:
        shifted = opts[1:] + opts[:1]
    return shifted


# -------------------------------------------------------------- the pages

def _lobby(r):
    st = r["stretch"]
    counts = {"blitz": "%d questions against the clock" % len(st.blitz),
              "short": "%d short answers" % len(st.short),
              "long": "%d long answers" % len(st.long)}
    rounds = "".join(
        '<li class="st-round st-round-%s"><span class="st-round-ico">%s</span>'
        '<span class="st-round-txt"><b>%s</b><span>%s</span></span></li>'
        % (kind, _round_icon(kind), name, counts[kind]) for name, kind in ROUNDS)
    return """<section class="st-lobby" id="st-lobby" aria-labelledby="st-title">
  <div class="st-bg" aria-hidden="true">%s</div>
  <div class="st-lobby-host" aria-hidden="true">%s</div>
  <div class="st-lobby-main">
    <p class="st-kicker">%s &middot; %s %s &middot; Lesson %d</p>
    <h1 id="st-title"><span class="st-h1-tag">Stretch task</span> %s</h1>
    <ol class="st-rounds">%s</ol>
    <div class="st-setup">
      <label class="st-name"><span>Your name</span><input type="text" id="st-name" maxlength="16" autocomplete="off" spellcheck="false" placeholder="Player"></label>
      <div class="st-toggles" role="group" aria-label="Game settings">
        <button type="button" class="st-toggle" data-st-opt="timer" aria-pressed="true">%s Timer</button>
        <button type="button" class="st-toggle" data-st-opt="sound" aria-pressed="false">%s Sound</button>
      </div>
    </div>
    <p class="st-best" data-st-best hidden></p>
    <div class="st-lobby-go">
      <button class="st-start" type="button" data-st-start>%s Start</button>
      <button class="st-link" type="button" data-st-print="sheet">%s Print the questions</button>
      <button class="st-link" type="button" data-st-print="answers">%s Print with answers</button>
    </div>
    <p class="st-nojs">The game needs JavaScript. Every question is below, with the answers at the end.</p>
  </div>
</section>""" % (BG, cat.rig(cls="px st-px"), esc(r["year"]), esc(r["topic"].spec), esc(r["topic"].title), r["n"],
                 esc(st.lesson), rounds, ico("i-timer"), ico("i-sound"), ico("i-play"), ico("i-paper"), ico("i-check"))


def _lesson_page(r, nxt, prev):
    st = r["stretch"]
    trail = [("Home", "/"), ("Key Stage 3", "/ks3/"), (HUB_TITLE, HUB),
             (r["topic"].title, "%s#%s" % (HUB, r["topic"].slug)), ("Lesson %d" % r["n"], None)]
    data = json.dumps(payload(r, nxt), separators=(",", ":"), ensure_ascii=False).replace("</", "<\\/")
    nav = []
    if prev:
        nav.append('<a class="prev" href="%s"><span>%s Previous</span><b>%s</b></a>' % (prev["url"], ico("i-arrow-left"), esc(prev["stretch"].lesson)))
    else:
        nav.append('<a class="prev" href="%s"><span>%s Back</span><b>%s</b></a>' % (HUB, ico("i-arrow-left"), HUB_TITLE))
    if nxt:
        nav.append('<a class="next" href="%s"><span>Next %s</span><b>%s</b></a>' % (nxt["url"], ico("i-arrow-right"), esc(nxt["stretch"].lesson)))
    body = """<div class="wrap">%s</div>
<div class="wrap st-page">
  <div class="st" id="st" data-motion="full">
    %s
    <div class="st-stage" id="st-stage" hidden></div>
  </div>
  <p class="st-back"><a href="%s">%s Read the lesson: %s</a></p>
  %s
  <nav class="topic-nav" aria-label="Stretch tasks">%s</nav>
</div>
<template id="st-pixel">%s</template>
<script type="application/json" id="st-data">%s</script>""" % (
        crumbs(trail), _lobby(r), r["lesson_url"], ico("i-book"), esc(st.lesson), _sheet(r), "".join(nav),
        cat.rig(), data)
    title = "Stretch task: %s" % st.lesson
    desc = "%s, %s lesson %d: a quiz game, short answers and long answers to stretch Key Stage 3 students." % (
        st.lesson, r["topic"].title, r["n"])
    ld = [crumbs_ld(trail), {
        "@context": "https://schema.org", "@type": "LearningResource",
        "name": title, "description": desc, "url": SITE_URL + r["url"], "inLanguage": "en-GB",
        "isAccessibleForFree": True, "learningResourceType": "Quiz",
        "educationalLevel": "Key Stage 3, %s" % r["year"], "teaches": st.lesson,
        "isPartOf": {"@type": "Course", "name": ks3.COURSE.title, "url": SITE_URL + "/ks3/"},
        "provider": {"@type": "Organization", "name": SITE_NAME, "url": SITE_URL},
    }]
    return layout(title=title, description=desc, path=r["url"], body=body, active="/ks3/",
                  extra_head='<link rel="stylesheet" href="/assets/css/stretch.css">',
                  scripts=["/assets/js/quiz.js", "/assets/js/stretch.js"], jsonld=ld)


def _stars_html():
    return '<span class="st-stars" data-st-stars aria-label="Not played yet">%s</span>' % (ico("i-star", "icon st-star") * 3)


def _hub(recs):
    trail = [("Home", "/"), ("Key Stage 3", "/ks3/"), (HUB_TITLE, None)]
    years = []
    for year in ("Year 8", "Year 9"):
        units = []
        seen = []
        for r in recs:
            if r["year"] != year or r["topic"].slug in seen:
                continue
            seen.append(r["topic"].slug)
            mine = [x for x in recs if x["topic"].slug == r["topic"].slug]
            cards = "".join(
                '<a class="st-hub-card" href="%s" data-st-key="%s">'
                '<span class="st-hub-n">Lesson %d</span><b>%s</b>%s</a>'
                % (x["url"], esc(x["key"]), x["n"], esc(x["stretch"].lesson), _stars_html()) for x in mine)
            units.append('<div class="st-hub-unit" id="%s"><h3><span class="badge badge-spec">%s</span> %s</h3>'
                         '<div class="st-hub-cards">%s</div></div>'
                         % (esc(r["topic"].slug), esc(r["topic"].spec), esc(r["topic"].title), cards))
        if units:
            years.append('<section class="section st-hub-year" id="%s"><h2>%s</h2>%s</section>'
                         % (slugify(year), year, "".join(units)))
    body = """<div class="wrap">%s</div>
<section class="hero st-hub-hero"><div class="wrap">
  <div class="st-hub-head">
    <div>
      <h1>%s</h1>
      <p class="lead">%s</p>
    </div>
    <div class="st-hub-art" aria-hidden="true">%s%s%s</div>
  </div>
</div></section>
<div class="wrap st-hub">%s</div>""" % (crumbs(trail), HUB_TITLE, HUB_LEAD,
                                        _round_icon("blitz"), _round_icon("short"), _round_icon("long"),
                                        "".join(years))
    ld = [crumbs_ld(trail), {
        "@context": "https://schema.org", "@type": "CollectionPage", "name": HUB_TITLE,
        "description": HUB_LEAD, "url": SITE_URL + HUB, "inLanguage": "en-GB",
        "isPartOf": {"@type": "Course", "name": ks3.COURSE.title, "url": SITE_URL + "/ks3/"},
    }]
    return layout(title="KS3 Computing stretch tasks", description=HUB_LEAD + " Free, no account needed.",
                  path=HUB, body=body, active="/ks3/",
                  extra_head='<link rel="stylesheet" href="/assets/css/stretch.css">',
                  scripts=["/assets/js/stretch.js"], jsonld=ld)


def build(register, add_search):
    missing = check()
    recs = records()
    for i, r in enumerate(recs):
        nxt = recs[i + 1] if i + 1 < len(recs) else None
        prev = recs[i - 1] if i else None
        write(r["url"], _lesson_page(r, nxt, prev))
        register(r["url"], 0.6, "monthly")
        add_search("Stretch task: %s" % r["stretch"].lesson, r["url"],
                   "%s %s, lesson %d" % (r["topic"].spec, r["topic"].title, r["n"]),
                   ("stretch task challenge quiz game ks3 %s %s %s"
                    % (r["year"], r["topic"].title, r["stretch"].lesson)).lower())
    write(HUB, _hub(recs))
    register(HUB, 0.8, "weekly")
    add_search(HUB_TITLE, HUB, "Year 8 and Year 9: a challenge for every lesson",
               "stretch tasks challenge extension fast finishers quiz game kahoot ks3 year 8 year 9 lessons")
    n_q = sum(len(r["stretch"].blitz) + len(r["stretch"].short) + len(r["stretch"].long) for r in recs)
    print("Stretch tasks: %d lessons, %d questions checked" % (len(recs), n_q))
    if missing:
        print("Stretch tasks still to write (%d): %s" % (len(missing), "; ".join(missing)))
