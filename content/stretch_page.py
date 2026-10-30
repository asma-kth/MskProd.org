"""Key Stage 3 stretch tasks: three for every Year 8 and Year 9 lesson.

Each lesson of a unit (a section of its topic page) gets a page of its own with
three tasks. The Quiz Challenge has three rounds: a quiz game against the
clock, short written answers, and long written answers marked against a mark
scheme. In This or That, Pixel the cat asks questions with two answers to
choose from. Memory Match is a card game: find each word's meaning. The games
themselves are static/js/stretch.js; this module writes the pages, the hub
that lists them, and the link under each lesson on the topic pages.

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
HUB_LEAD = ("Three tasks for every Year 8 and Year 9 lesson: a quiz challenge, This or That with "
            "Pixel the cat, and Memory Match.")

ROUNDS = [("Quiz Blitz", "blitz"), ("Quick Fire", "short"), ("Big Think", "long")]

# The tasks on every lesson's page, in the order they are offered. The key is
# also what the game and the saved results call each one.
TASKS = [("quiz", "Quiz Challenge"), ("cat", "This or That"), ("match", "Memory Match")]

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


def _task_icon(task):
    """The drawn picture on each task's card: the quiz's four shapes, Pixel's
    head for This or That, and two playing cards for Memory Match."""
    if task == "quiz":
        return _round_icon("blitz")
    if task == "cat":
        head = cat.flat(head_only=True, cls="st-cat-head")
        return head.replace(' role="img" aria-label="Pixel the robot cat"', ' aria-hidden="true" focusable="false"')
    return ('<svg viewBox="0 0 50 50" aria-hidden="true" focusable="false">'
            '<g transform="rotate(-11 17 27)"><rect x="4" y="9" width="25" height="33" rx="5" fill="#1F5FD1" '
            'stroke="#1E293B" stroke-width="2.2"/><rect x="8" y="13" width="17" height="25" rx="3" fill="none" '
            'stroke="#fff" stroke-opacity=".5" stroke-width="1.6" stroke-dasharray="3 2"/>'
            '<path d="M13.4 21.6a3.6 3.6 0 1 1 5 3.3c-1.1.5-1.6 1.2-1.6 2.4" fill="none" stroke="#fff" stroke-width="2.6" '
            'stroke-linecap="round"/><circle cx="16.8" cy="31.4" r="1.6" fill="#fff"/></g>'
            '<g transform="rotate(9 33 25)"><rect x="21" y="8" width="25" height="33" rx="5" fill="#fff" '
            'stroke="#1E293B" stroke-width="2.2"/><path d="M26.5 17h14M26.5 23h10M26.5 29h12" stroke="#1E293B" '
            'stroke-width="2.6" stroke-linecap="round"/></g>'
            '<circle cx="40" cy="40" r="7.5" fill="#16A34A" stroke="#fff" stroke-width="2.2"/>'
            '<path d="M36.4 40.2l2.5 2.5 4.6-4.8" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" '
            'stroke-linejoin="round"/></svg>')


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


def _pick(p):
    d = {"q": markup.inline(p.q), "r": markup.inline(p.right), "w": markup.inline(p.wrong), "x": markup.inline(p.why)}
    if p.code:
        d["c"] = _code(p.code, p.lang)
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
        "picks": [_pick(p) for p in st.picks],
        "pairs": [{"a": markup.inline(p.a), "b": markup.inline(p.b)} for p in st.pairs],
        "pn": list(st.pair_names),
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

    picks, pick_keys = [], []
    for p in st.picks:
        two = [p.right, p.wrong] if _seed(p.q) % 2 else [p.wrong, p.right]
        picks.append('<li class="st-sheet-q"><p>%s</p>%s<ul class="st-sheet-opts st-sheet-tf">%s</ul></li>'
                     % (markup.inline(p.q), _sheet_code(p.code, p.lang),
                        "".join('<li><span class="st-box"></span>%s</li>' % markup.inline(o) for o in two)))
        pick_keys.append("<li><b>%s</b> %s</li>" % (markup.inline(p.right), markup.inline(p.why)))

    # Meanings in a fixed order in which none sits beside its own word.
    n_pairs = len(st.pairs)
    mixed = sorted(range(n_pairs), key=lambda i: _seed(st.pairs[i].b))
    order = next((mixed[r:] + mixed[:r] for r in range(n_pairs)
                  if all(i != k for k, i in enumerate(mixed[r:] + mixed[:r]))),
                 [(k + 1) % n_pairs for k in range(n_pairs)])
    letters = "ABCDEFGH"
    rows = "".join('<tr><td><b>%s</b> %s</td><td><b>%d</b> %s</td></tr>'
                   % (letters[k], markup.inline(st.pairs[k].a), n + 1, markup.inline(st.pairs[i].b))
                   for n, (k, i) in enumerate(zip(range(len(st.pairs)), order)))
    match_key = "".join("<li><b>%s %d</b> %s: %s</li>" % (letters[k], order.index(k) + 1, markup.inline(p.a), markup.inline(p.b))
                        for k, p in enumerate(st.pairs))
    word, meaning = (n.lower() for n in st.pair_names)
    return """<section class="st-sheet" id="st-sheet" aria-labelledby="st-sheet-title">
  <h2 id="st-sheet-title">%s: the questions</h2>
  <h3>Quiz Challenge, round 1: Quiz Blitz</h3><ol class="st-sheet-list">%s</ol>
  <h3>Quiz Challenge, round 2: Quick Fire</h3><ol class="st-sheet-list">%s</ol>
  <h3>Quiz Challenge, round 3: Big Think</h3><ol class="st-sheet-list">%s</ol>
  <h3>This or That: tick the right answer</h3><ol class="st-sheet-list">%s</ol>
  <h3>Memory Match: match each %s to its %s</h3>
  <table class="st-sheet-match"><thead><tr><th scope="col">%s</th><th scope="col">%s</th></tr></thead><tbody>%s</tbody></table>
  <details class="st-key" id="st-key">
    <summary>Answers</summary>
    <h3>Round 1: Quiz Blitz</h3><ol class="st-sheet-list">%s</ol>
    <h3>Round 2: Quick Fire</h3><ol class="st-sheet-list">%s</ol>
    <h3>Round 3: Big Think</h3><ol class="st-sheet-list">%s</ol>
    <h3>This or That</h3><ol class="st-sheet-list">%s</ol>
    <h3>Memory Match</h3><ul class="st-sheet-list st-sheet-pairs">%s</ul>
  </details>
</section>""" % (esc(st.lesson), "".join(qs), sq, lq, "".join(picks), esc(word), esc(meaning),
                 esc(st.pair_names[0]), esc(st.pair_names[1]), rows,
                 "".join(keys), sk, lk, "".join(pick_keys), match_key)


def _seed(text):
    import hashlib
    return int(hashlib.sha256(text.encode("utf-8")).hexdigest(), 16)


def _sheet_order(b):
    """A fixed, deterministic order for options on paper, never the written one."""
    opts = list(b.options)
    seed = _seed(b.q)
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
    word, meaning = (n.lower() for n in st.pair_names)
    about = {
        "quiz": ("A quiz game against four computer players, then short and long written answers.",
                 "About 20 minutes"),
        "cat": ("Pixel the cat asks %d questions. Each has two answers: pick the right one." % len(st.picks),
                "About 4 minutes"),
        "match": ("Flip the cards two at a time to match each %s card to its %s card." % (word, meaning),
                  "%d pairs, about 4 minutes" % len(st.pairs)),
    }
    points = {
        "cat": ["Two answers to every question", "A fish treat for every right answer",
                "Streaks win Pixel shades, then a party hat"],
        "match": ["%d cards: each %s has a %s" % (2 * len(st.pairs), word, meaning), "One peek at every card",
                  "Combo points for pairs found in a row"],
    }
    cards = []
    for n, (task, name) in enumerate(TASKS, 1):
        cards.append("""<div class="st-task st-task-%(t)s" role="group" aria-labelledby="st-t-%(t)s">
        <div class="st-task-head"><span class="st-task-art" data-st-art="%(t)s" aria-hidden="true">%(art)s</span><span class="st-task-n">Task %(n)d</span></div>
        <h2 id="st-t-%(t)s">%(name)s</h2>
        <p class="st-task-sum">%(sum)s</p>
        %(rounds)s<p class="st-task-time">%(clock)s %(time)s</p>
        <p class="st-best" data-st-best="%(t)s" hidden></p>
        <button class="st-start" type="button" data-st-start="%(t)s">%(play)s Play<span class="sr-only"> %(name)s</span></button>
      </div>""" % dict(t=task, n=n, name=name, art=_task_icon(task), sum=esc(about[task][0]), time=about[task][1],
                       rounds=('<ol class="st-rounds">%s</ol>' % rounds if task == "quiz" else
                               '<ul class="st-points">%s</ul>' % "".join("<li>%s%s</li>" % (ico("i-check"), esc(t))
                                                                         for t in points[task])),
                       clock=ico("i-clock"), play=ico("i-play")))
    return """<section class="st-lobby" id="st-lobby" aria-labelledby="st-title">
  <div class="st-bg" aria-hidden="true">%s</div>
  <div class="st-lobby-host" aria-hidden="true">%s</div>
  <div class="st-lobby-main">
    <p class="st-kicker">%s &middot; %s %s &middot; Lesson %d</p>
    <h1 id="st-title"><span class="st-h1-tag">Stretch tasks</span> %s</h1>
    <div class="st-setup">
      <label class="st-name"><span>Your name</span><input type="text" id="st-name" maxlength="16" autocomplete="off" spellcheck="false" placeholder="Player"></label>
      <div class="st-toggles" role="group" aria-label="Game settings">
        <button type="button" class="st-toggle" data-st-opt="timer" aria-pressed="true">%s Timer</button>
        <button type="button" class="st-toggle" data-st-opt="sound" aria-pressed="false">%s Sound</button>
      </div>
    </div>
  </div>
  <div class="st-tasks">
      %s
  </div>
  <div class="st-lobby-go">
    <button class="st-link" type="button" data-st-print="sheet">%s Print the questions</button>
    <button class="st-link" type="button" data-st-print="answers">%s Print with answers</button>
  </div>
  <p class="st-nojs">The games need JavaScript. Every question is below, with the answers at the end.</p>
</section>""" % (BG, cat.rig(cls="px st-px"), esc(r["year"]), esc(r["topic"].spec), esc(r["topic"].title), r["n"],
                 esc(st.lesson), ico("i-timer"), ico("i-sound"), "\n      ".join(cards), ico("i-paper"), ico("i-check"))


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
    title = "Stretch tasks: %s" % st.lesson
    desc = "%s, %s lesson %d: a quiz challenge, This or That with Pixel the cat, and Memory Match, to stretch Key Stage 3 students." % (
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


# Small marks for the three tasks on the hub's cards, drawn once and reused.
GLYPHS = ('<svg class="st-glyphs" width="0" height="0" aria-hidden="true" focusable="false">'
          '<symbol id="st-g-quiz" viewBox="0 0 24 24"><rect x="2" y="2" width="9" height="9" rx="2.4" fill="#D7263D"/>'
          '<rect x="13" y="2" width="9" height="9" rx="2.4" fill="#1F5FD1"/><rect x="2" y="13" width="9" height="9" rx="2.4" '
          'fill="#F2B705"/><rect x="13" y="13" width="9" height="9" rx="2.4" fill="#1E7B34"/></symbol>'
          '<symbol id="st-g-cat" viewBox="0 0 24 24"><path d="M3.6 10 4.3 2.8l5.2 3.6h5L19.7 2.8l.7 7.2A8.6 8.2 0 0 1 '
          '12 21.6 8.6 8.2 0 0 1 3.6 10Z" fill="#02848B"/><circle cx="8.8" cy="12.6" r="1.7" fill="#fff"/>'
          '<circle cx="15.2" cy="12.6" r="1.7" fill="#fff"/><path d="M10.9 15.8h2.2L12 17.1Z" fill="#fff"/></symbol>'
          '<symbol id="st-g-match" viewBox="0 0 24 24"><rect x="1.5" y="4" width="11" height="15" rx="2.4" fill="#1F5FD1" '
          'transform="rotate(-9 7 11.5)"/><rect x="11" y="3.5" width="11" height="15" rx="2.4" fill="#fff" stroke="#1E293B" '
          'stroke-width="1.6" transform="rotate(8 16.5 11)"/><path d="M14 8.5h5M14 11.5h3.6" stroke="#1E293B" '
          'stroke-width="1.6" stroke-linecap="round" transform="rotate(8 16.5 11)"/></symbol></svg>')


def _hub_tasks():
    """Each task's best stars on a hub card, filled in from this device's results."""
    out = []
    for task, name in TASKS:
        out.append('<span class="st-hub-task" data-st-task="%s"><svg class="st-g" aria-hidden="true" focusable="false">'
                   '<use href="#st-g-%s"></use></svg><span class="st-stars" data-st-stars aria-hidden="true">%s</span>'
                   '<span class="sr-only" data-st-sr>%s: not played yet.</span></span>'
                   % (task, task, ico("i-star", "icon st-star") * 3, name))
    return '<span class="st-hub-tasks">%s</span>' % "".join(out)


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
                % (x["url"], esc(x["key"]), x["n"], esc(x["stretch"].lesson), _hub_tasks()) for x in mine)
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
<div class="wrap st-hub">%s%s</div>""" % (crumbs(trail), HUB_TITLE, HUB_LEAD,
                                          _task_icon("quiz"), _task_icon("cat"), _task_icon("match"),
                                          GLYPHS, "".join(years))
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
    if missing:
        raise SystemExit("Year 8 and 9 lessons with no stretch task:\n  " + "\n  ".join(missing))
    recs = records()
    for i, r in enumerate(recs):
        nxt = recs[i + 1] if i + 1 < len(recs) else None
        prev = recs[i - 1] if i else None
        write(r["url"], _lesson_page(r, nxt, prev))
        register(r["url"], 0.6, "monthly")
        add_search("Stretch tasks: %s" % r["stretch"].lesson, r["url"],
                   "%s %s, lesson %d" % (r["topic"].spec, r["topic"].title, r["n"]),
                   ("stretch task challenge quiz game this or that pixel cat memory match pairs ks3 %s %s %s"
                    % (r["year"], r["topic"].title, r["stretch"].lesson)).lower())
    write(HUB, _hub(recs))
    register(HUB, 0.8, "weekly")
    add_search(HUB_TITLE, HUB, "Year 8 and Year 9: three tasks for every lesson",
               "stretch tasks challenge extension fast finishers quiz game kahoot this or that pixel cat "
               "memory match pairs ks3 year 8 year 9 lessons")
    n_q = sum(len(r["stretch"].blitz) + len(r["stretch"].short) + len(r["stretch"].long) for r in recs)
    n_p = sum(len(r["stretch"].picks) for r in recs)
    n_m = sum(len(r["stretch"].pairs) for r in recs)
    print("Stretch tasks: %d lessons, %d quiz questions, %d This or That questions and %d Memory Match pairs checked"
          % (len(recs), n_q, n_p, n_m))
