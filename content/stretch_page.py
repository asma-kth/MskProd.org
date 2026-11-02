"""Stretch tasks: games for every lesson at Key Stage 3 and Key Stage 4.

A Key Stage 3 lesson is a section of a unit's topic page; at Key Stage 4 a
lesson is a whole topic. Each lesson gets a page of its own. The Quiz
Challenge has three rounds: a quiz game against the clock, short written
answers, and long written answers marked against a mark scheme. In This or
That, Pixel the cat asks questions with two answers to choose from. Memory
Match is a card game: find each word's meaning. Key Stage 4 lessons add Sort
It: drag each statement into the right box, like the tick-box tables on GCSE
papers. The games themselves are static/js/stretch.js; this module writes the
pages, a hub for each key stage, and the links from the lessons to them.

Every page also carries the whole task as plain HTML: it is what a browser
without JavaScript shows, and what prints when a teacher wants it on paper.
"""
import importlib
import json

from mskbuild import cat, markup, render
from mskbuild.render import (SITE_NAME, SITE_URL, crumbs, crumbs_ld, esc, ico, layout, write)
from mskbuild.util import slugify
from mskbuild import stretchcheck
from content import ks3
from content import ks3_stretch
from content import ks4_stretch

HUB = "/ks3/stretch/"
HUB_TITLE = "Stretch tasks"
HUB_LEAD = ("Three tasks for every Year 7, 8 and 9 lesson: a quiz challenge, This or That with "
            "Pixel the cat, and Memory Match.")

HUB4 = "/ks4/stretch/"
HUB4_TITLE = "Key Stage 4 stretch tasks"

ROUNDS = [("Quiz Blitz", "blitz"), ("Quick Fire", "short"), ("Big Think", "long")]

# The tasks on a lesson's page, in the order they are offered. The key is also
# what the game and the saved results call each one. Sort It is the fourth
# task, at Key Stage 4 only.
TASKS = [("quiz", "Quiz Challenge"), ("cat", "This or That"), ("match", "Memory Match"), ("sort", "Sort It")]

# The module that defines each Key Stage 4 course.
KS4_SOURCES = {"ks4/computer-science": "ks4_cs", "ks4/aqa-computer-science": "aqa_gcse",
               "ks4/edexcel-computer-science": "edexcel_gcse", "ks4/imedia": "ks4_imedia"}


def _tasks(st):
    return TASKS if st.sort else TASKS[:3]


def _ks4_course(slug):
    return importlib.import_module("content." + KS4_SOURCES[slug]).COURSE

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
    if task == "sort":
        return ('<svg viewBox="0 0 50 50" aria-hidden="true" focusable="false">'
                '<path d="M2.5 30h19.5l-2.3 16.5H4.8Z" fill="#F97316" stroke="#1E293B" stroke-width="2.2" stroke-linejoin="round"/>'
                '<path d="M28 30h19.5l-2.3 16.5H30.3Z" fill="#1F5FD1" stroke="#1E293B" stroke-width="2.2" stroke-linejoin="round"/>'
                '<path d="M7 35.5h10.5M32.5 35.5H43" stroke="#fff" stroke-opacity=".65" stroke-width="2" stroke-linecap="round"/>'
                '<g transform="rotate(-12 21 13)"><rect x="9" y="4" width="24" height="17" rx="3.5" fill="#fff" '
                'stroke="#1E293B" stroke-width="2.2"/><path d="M14 10h14M14 15h9" stroke="#1E293B" stroke-width="2.4" '
                'stroke-linecap="round"/></g>'
                '<path d="M34 15.5c5.5 0 8.4 3.8 8.4 9.4" fill="none" stroke="#16A34A" stroke-width="3" stroke-linecap="round"/>'
                '<path d="M38.4 22.6l4 4.4 4-4.4" fill="none" stroke="#16A34A" stroke-width="3" stroke-linecap="round" '
                'stroke-linejoin="round"/></svg>')
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


def ks3_records():
    """Every Key Stage 3 stretch task in teaching order, with what its pages need to know."""
    topics = {t.slug: (u, t) for u in ks3.COURSE.units for t in u.topics}
    out = []
    for slug, lessons in ks3_stretch.units():
        unit, topic = topics[slug]
        for n, st in enumerate(lessons, 1):
            sec = next(s for s in topic.sections if s.title == st.lesson)
            url = "%s%s/lesson-%d/" % (HUB, slug, n)
            out.append({
                "stage": "ks3", "stretch": st, "topic": topic, "unit": unit, "n": n, "title": st.lesson,
                "key": "%s/%d" % (slug, n), "url": url,
                "lesson_url": "/ks3/%s/#%s" % (slug, sec.id or slugify(sec.title)),
                "year": unit.title,
                "kicker": [unit.title, "%s %s" % (topic.spec, topic.title), "Lesson %d" % n],
                "where": "%s %s, lesson %d" % (topic.spec, topic.title, n),
                "trail": [("Home", "/"), ("Key Stage 3", "/ks3/"), (HUB_TITLE, HUB),
                          (topic.title, "%s#%s" % (HUB, slug)), ("Lesson %d" % n, None)],
                "hub": HUB, "active": "/ks3/", "level": "Key Stage 3, %s" % unit.title,
                "course_name": ks3.COURSE.title, "course_url": "/ks3/",
                "desc": "%s, %s lesson %d: a quiz challenge, This or That with Pixel the cat, and Memory Match, "
                        "to stretch Key Stage 3 students." % (st.lesson, topic.title, n),
            })
    return out


def ks4_records():
    """Every Key Stage 4 stretch task, course by course in teaching order."""
    out = []
    for key, slug, name, lessons in ks4_stretch.courses():
        course = _ks4_course(slug)
        topics = {t.slug: (u, t) for u in course.units for t in u.topics}
        order = list(topics)
        unknown = [st.lesson for st in lessons if st.lesson not in topics]
        if unknown:
            raise SystemExit("content/ks4_stretch: %s has no topic called %s" % (slug, ", ".join(unknown)))
        audience = "Creative iMedia" if slug == "ks4/imedia" else "GCSE Computer Science"
        for n, st in enumerate(sorted(lessons, key=lambda st: order.index(st.lesson)), 1):
            unit, topic = topics[st.lesson]
            out.append({
                "stage": "ks4", "stretch": st, "topic": topic, "unit": unit, "n": n, "title": topic.title,
                "course": course, "ckey": key, "cname": name,
                "key": "ks4/%s/%s" % (key, topic.slug), "url": "%s%s/%s/" % (HUB4, key, topic.slug),
                "lesson_url": "/%s/%s/" % (slug, topic.slug),
                "kicker": [name, unit.title],
                "where": "%s %s" % (course.code, topic.spec),
                "trail": [("Home", "/"), (course.short, "/%s/" % slug), (HUB_TITLE, "%s#%s" % (HUB4, key)),
                          (topic.title, None)],
                "hub": HUB4, "active": "/%s/" % slug, "level": "Key Stage 4, %s" % name,
                "course_name": course.title, "course_url": "/%s/" % slug,
                "desc": "%s (%s %s): a quiz challenge, This or That with Pixel the cat, Memory Match and Sort It, "
                        "to stretch %s students." % (topic.title, course.board, topic.spec, audience),
            })
    return out


def records():
    """Every stretch task on the site: Key Stage 3, then Key Stage 4."""
    return ks3_records() + ks4_records()


def attach_links():
    """Link the lessons to their stretch tasks, before the topic pages are built.

    A Key Stage 3 lesson ends with a link to its own; a Key Stage 4 topic
    closes with one, and its course's page gets a button to the hub."""
    recs = records()
    for r in recs:
        if r["stage"] == "ks3":
            links = getattr(r["topic"], "stretch", None)
            if links is None:
                links = r["topic"].stretch = {}
            links[r["stretch"].lesson] = (r["url"], r["n"])
        else:
            r["topic"].stretch_all = r["url"]
            r["course"].extra_cta = ("Stretch tasks", "%s#%s" % (HUB4, r["ckey"]), "i-target")
    link = ("KS4 stretch tasks", HUB4)
    if any(r["stage"] == "ks4" for r in recs) and link not in render.PRACTISE_LINKS:
        render.PRACTISE_LINKS.append(link)


def check():
    """Prove every task, and that every lesson has one: every Key Stage 3
    lesson, and every lesson of a published Key Stage 4 course."""
    units = ks3_stretch.units()
    topics = {t.slug: t for u in ks3.COURSE.units for t in u.topics}
    stretchcheck.validate(units, topics)
    have = {(slug, st.lesson) for slug, lessons in units for st in lessons}
    missing = []
    for u in ks3.COURSE.units:
        for t in u.topics:
            for s in t.sections:
                if (t.slug, s.title) not in have and (t.slug, s.title) not in ks3_stretch.NOT_LESSONS:
                    missing.append("%s: %s" % (t.slug, s.title))
    lessons4, topics4 = [], {}
    for key, slug, name, lessons in ks4_stretch.courses():
        course = _ks4_course(slug)
        mine = [t.slug for u in course.units for t in u.topics]
        topics4.update({(slug, t.slug): t for u in course.units for t in u.topics})
        lessons4 += [(slug, st) for st in lessons]
        if ks4_stretch.complete(slug):
            done = {st.lesson for st in lessons}
            missing += ["%s: %s" % (slug, t) for t in mine if t not in done and (slug, t) not in ks4_stretch.NOT_LESSONS]
    stretchcheck.validate_ks4(lessons4, topics4)
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
    d = {
        "key": r["key"], "lesson": r["title"], "where": r["where"],
        "back": r["lesson_url"],
        "next": {"t": nxt["title"], "u": nxt["url"]} if nxt else None,
        "blitz": [_blitz(b) for b in st.blitz],
        "short": [_written(w) for w in st.short],
        "long": [_written(w) for w in st.long],
        "picks": [_pick(p) for p in st.picks],
        "pairs": [{"a": markup.inline(p.a), "b": markup.inline(p.b)} for p in st.pairs],
        "pn": list(st.pair_names),
    }
    if st.sort:
        d["sort"] = {"p": markup.inline(st.sort.prompt), "b": [markup.inline(b) for b in st.sort.bins],
                     "i": [{"t": markup.inline(i.text), "b": i.bin, "x": markup.inline(i.why)} for i in st.sort.items]}
    return d


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
    word, meaning = (_in_sentence(n) for n in st.pair_names)
    sort_q, sort_k = _sheet_sort(st.sort) if st.sort else ("", "")
    return """<section class="st-sheet" id="st-sheet" aria-labelledby="st-sheet-title">
  <h2 id="st-sheet-title">%s: the questions</h2>
  <h3>Quiz Challenge, round 1: Quiz Blitz</h3><ol class="st-sheet-list">%s</ol>
  <h3>Quiz Challenge, round 2: Quick Fire</h3><ol class="st-sheet-list">%s</ol>
  <h3>Quiz Challenge, round 3: Big Think</h3><ol class="st-sheet-list">%s</ol>
  <h3>This or That: tick the right answer</h3><ol class="st-sheet-list">%s</ol>
  <h3>Memory Match: match each %s to its %s</h3>
  <table class="st-sheet-match"><thead><tr><th scope="col">%s</th><th scope="col">%s</th></tr></thead><tbody>%s</tbody></table>
  %s
  <details class="st-key" id="st-key">
    <summary>Answers</summary>
    <h3>Round 1: Quiz Blitz</h3><ol class="st-sheet-list">%s</ol>
    <h3>Round 2: Quick Fire</h3><ol class="st-sheet-list">%s</ol>
    <h3>Round 3: Big Think</h3><ol class="st-sheet-list">%s</ol>
    <h3>This or That</h3><ol class="st-sheet-list">%s</ol>
    <h3>Memory Match</h3><ul class="st-sheet-list st-sheet-pairs">%s</ul>
    %s
  </details>
</section>""" % (esc(r["title"]), "".join(qs), sq, lq, "".join(picks), esc(word), esc(meaning),
                 esc(st.pair_names[0]), esc(st.pair_names[1]), rows, sort_q,
                 "".join(keys), sk, lk, "".join(pick_keys), match_key, sort_k)


def _sheet_sort(so):
    """Sort It on paper: a table with a box to tick in each row, as GCSE papers set it."""
    order = sorted(range(len(so.items)), key=lambda i: _seed(so.items[i].text))
    head = "".join('<th scope="col">%s</th>' % markup.inline(b) for b in so.bins)
    tick = '<td class="st-sheet-tick"><span class="st-box"></span></td>' * len(so.bins)
    rows = "".join("<tr><td>%s</td>%s</tr>" % (markup.inline(so.items[i].text), tick) for i in order)
    q = ('<h3>Sort It: tick one box in each row</h3><p class="st-sheet-hint">%s</p>'
         '<table class="st-sheet-sort"><thead><tr><th scope="col">Statement</th>%s</tr></thead><tbody>%s</tbody></table>'
         % (markup.inline(so.prompt), head, rows))
    key = ('<h3>Sort It</h3><ol class="st-sheet-list">%s</ol>'
           % "".join("<li><b>%s</b> %s %s</li>" % (markup.inline(so.bins[so.items[i].bin]), markup.inline(so.items[i].text),
                                                  markup.inline(so.items[i].why)) for i in order))
    return q, key


def _in_sentence(name):
    """A card label inside a sentence: Tag reads as tag, but CSS stays CSS."""
    return name if name.isupper() else name.lower()


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
    word, meaning = (_in_sentence(n) for n in st.pair_names)
    n_sort = len(st.sort.items) if st.sort else 0
    about = {
        "quiz": ("A quiz game against four computer players, then short and long written answers.",
                 "About 20 minutes"),
        "cat": ("Pixel the cat asks %d questions. Each has two answers: pick the right one." % len(st.picks),
                "About 4 minutes"),
        "match": ("Flip the cards two at a time to match each %s card to its %s card." % (word, meaning),
                  "%d pairs, about 4 minutes" % len(st.pairs)),
        "sort": ("Sort each statement into the right box, like the tick-box tables in the exam.",
                 "%d cards, about 4 minutes" % n_sort),
    }
    points = {
        "cat": ["Two answers to every question", "A fish treat for every right answer",
                "Streaks win Pixel shades, then a party hat"],
        "match": ["%d cards: each %s has a %s" % (2 * len(st.pairs), word, meaning), "One peek at every card",
                  "Combo points for pairs found in a row"],
        "sort": ["%d cards to sort into %d boxes" % (n_sort, len(st.sort.bins) if st.sort else 0),
                 "Drag a card, tap a box or press its number", "Combo points for cards sorted in a row"],
    }
    tasks = _tasks(st)
    cards = []
    for n, (task, name) in enumerate(tasks, 1):
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
    <p class="st-kicker">%s</p>
    <h1 id="st-title"><span class="st-h1-tag">Stretch tasks</span> %s</h1>
    <div class="st-setup">
      <label class="st-name"><span>Your name</span><input type="text" id="st-name" maxlength="16" autocomplete="off" spellcheck="false" placeholder="Player"></label>
      <div class="st-toggles" role="group" aria-label="Game settings">
        <button type="button" class="st-toggle" data-st-opt="timer" aria-pressed="true">%s Timer</button>
        <button type="button" class="st-toggle" data-st-opt="sound" aria-pressed="false">%s Sound</button>
      </div>
    </div>
  </div>
  <div class="st-tasks" data-n="%d">
      %s
  </div>
  <div class="st-lobby-go">
    <button class="st-link" type="button" data-st-print="sheet">%s Print the questions</button>
    <button class="st-link" type="button" data-st-print="answers">%s Print with answers</button>
  </div>
  <p class="st-nojs">The games need JavaScript. Every question is below, with the answers at the end.</p>
</section>""" % (BG, cat.rig(cls="px st-px"), " &middot; ".join(esc(k) for k in r["kicker"]),
                 esc(r["title"]), ico("i-timer"), ico("i-sound"), len(tasks), "\n      ".join(cards),
                 ico("i-paper"), ico("i-check"))


def _lesson_page(r, nxt, prev):
    trail = r["trail"]
    data = json.dumps(payload(r, nxt), separators=(",", ":"), ensure_ascii=False).replace("</", "<\\/")
    nav = []
    if prev:
        nav.append('<a class="prev" href="%s"><span>%s Previous</span><b>%s</b></a>' % (prev["url"], ico("i-arrow-left"), esc(prev["title"])))
    else:
        back = r["hub"] + ("#" + r["ckey"] if r["stage"] == "ks4" else "")
        nav.append('<a class="prev" href="%s"><span>%s Back</span><b>%s</b></a>' % (back, ico("i-arrow-left"), HUB_TITLE))
    if nxt:
        nav.append('<a class="next" href="%s"><span>Next %s</span><b>%s</b></a>' % (nxt["url"], ico("i-arrow-right"), esc(nxt["title"])))
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
        crumbs(trail), _lobby(r), r["lesson_url"], ico("i-book"), esc(r["title"]), _sheet(r), "".join(nav),
        cat.rig(), data)
    title = "Stretch tasks: %s" % r["title"]
    ld = [crumbs_ld(trail), {
        "@context": "https://schema.org", "@type": "LearningResource",
        "name": title, "description": r["desc"], "url": SITE_URL + r["url"], "inLanguage": "en-GB",
        "isAccessibleForFree": True, "learningResourceType": "Quiz",
        "educationalLevel": r["level"], "teaches": r["title"],
        "isPartOf": {"@type": "Course", "name": r["course_name"], "url": SITE_URL + r["course_url"]},
        "provider": {"@type": "Organization", "name": SITE_NAME, "url": SITE_URL},
    }]
    return layout(title=title, description=r["desc"], path=r["url"], body=body, active=r["active"],
                  extra_head='<link rel="stylesheet" href="/assets/css/stretch.css">',
                  scripts=["/assets/js/quiz.js", "/assets/js/stretch.js"], jsonld=ld)


# Small marks for the tasks on the hub's cards, drawn once and reused.
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
          'stroke-width="1.6" stroke-linecap="round" transform="rotate(8 16.5 11)"/></symbol>'
          '<symbol id="st-g-sort" viewBox="0 0 24 24"><path d="M1.5 14h9l-1 8.5h-7Z" fill="#F97316"/>'
          '<path d="M13.5 14h9l-1 8.5h-7Z" fill="#1F5FD1"/><rect x="7" y="2" width="10" height="8" rx="1.8" fill="#fff" '
          'stroke="#1E293B" stroke-width="1.5" transform="rotate(-10 12 6)"/></symbol></svg>')


def _hub_tasks(tasks):
    """Each task's best stars on a hub card, filled in from this device's results."""
    out = []
    for task, name in tasks:
        out.append('<span class="st-hub-task" data-st-task="%s"><svg class="st-g" aria-hidden="true" focusable="false">'
                   '<use href="#st-g-%s"></use></svg><span class="st-stars" data-st-stars aria-hidden="true">%s</span>'
                   '<span class="sr-only" data-st-sr>%s: not played yet.</span></span>'
                   % (task, task, ico("i-star", "icon st-star") * 3, name))
    return '<span class="st-hub-tasks%s">%s</span>' % (" is-four" if len(tasks) == 4 else "", "".join(out))


def _hub_card(r, label):
    return ('<a class="st-hub-card" href="%s" data-st-key="%s"><span class="st-hub-n">%s</span><b>%s</b>%s</a>'
            % (r["url"], esc(r["key"]), esc(label), esc(_card_title(r)), _hub_tasks(_tasks(r["stretch"]))))


def _card_title(r):
    """A Creative iMedia topic's title starts with its specification reference,
    which its hub card already shows."""
    t, spec = r["title"], r["topic"].spec
    return t[len(spec) + 2:] if r["stage"] == "ks4" and spec and t.startswith(spec + ": ") else t


def _hub_page(*, path, title, h1, lead, trail, sections, tasks, course_name, course_url, active, jump=""):
    body = """<div class="wrap">%s</div>
<section class="hero st-hub-hero"><div class="wrap">
  <div class="st-hub-head">
    <div>
      <h1>%s</h1>
      <p class="lead">%s</p>%s
    </div>
    <div class="st-hub-art" aria-hidden="true">%s</div>
  </div>
</div></section>
<div class="wrap st-hub">%s%s</div>""" % (crumbs(trail), esc(h1), esc(lead), jump,
                                          "".join(_task_icon(t) for t, _ in tasks), GLYPHS, sections)
    ld = [crumbs_ld(trail), {
        "@context": "https://schema.org", "@type": "CollectionPage", "name": h1,
        "description": lead, "url": SITE_URL + path, "inLanguage": "en-GB",
        "isPartOf": {"@type": "Course", "name": course_name, "url": SITE_URL + course_url},
    }]
    return layout(title=title, description=lead + " Free, no account needed.", path=path, body=body, active=active,
                  extra_head='<link rel="stylesheet" href="/assets/css/stretch.css">',
                  scripts=["/assets/js/stretch.js"], jsonld=ld)


def _hub(recs):
    years = []
    for year in ("Year 7", "Year 8", "Year 9"):
        units = []
        seen = []
        for r in recs:
            if r["year"] != year or r["topic"].slug in seen:
                continue
            seen.append(r["topic"].slug)
            cards = "".join(_hub_card(x, "Lesson %d" % x["n"]) for x in recs if x["topic"].slug == r["topic"].slug)
            units.append('<div class="st-hub-unit" id="%s"><h3><span class="badge badge-spec">%s</span> %s</h3>'
                         '<div class="st-hub-cards">%s</div></div>'
                         % (esc(r["topic"].slug), esc(r["topic"].spec), esc(r["topic"].title), cards))
        if units:
            years.append('<section class="section st-hub-year" id="%s"><h2>%s</h2>%s</section>'
                         % (slugify(year), year, "".join(units)))
    return _hub_page(path=HUB, title="KS3 Computing stretch tasks", h1=HUB_TITLE, lead=HUB_LEAD,
                     trail=[("Home", "/"), ("Key Stage 3", "/ks3/"), (HUB_TITLE, None)],
                     sections="".join(years), tasks=TASKS[:3], course_name=ks3.COURSE.title, course_url="/ks3/",
                     active="/ks3/")


def _hub4_lead(names):
    names = list(names)
    which = names[0] if len(names) == 1 else ", ".join(names[:-1]) + " and " + names[-1]
    return ("Four tasks for every lesson of %s: a quiz challenge, This or That with Pixel the cat, "
            "Memory Match and Sort It." % which)


def _hub4(recs):
    courses = []
    for r in recs:
        if r["ckey"] not in [c[0] for c in courses]:
            courses.append((r["ckey"], r["cname"]))
    sections = []
    for key, name in courses:
        mine = [r for r in recs if r["ckey"] == key]
        units = []
        for u in mine[0]["course"].units:
            cards = "".join(_hub_card(r, r["topic"].spec) for r in mine if r["unit"] is u)
            if cards:
                units.append('<div class="st-hub-unit" id="%s-%s"><h3>%s</h3><div class="st-hub-cards">%s</div></div>'
                             % (key, esc(u.slug), esc(u.title), cards))
        sections.append('<section class="section st-hub-year" id="%s"><h2>%s</h2>%s</section>'
                        % (key, esc(name), "".join(units)))
    jump = ""
    if len(courses) > 1:
        jump = ('\n      <p class="st-hub-jump">%s</p>'
                % "".join('<a class="btn btn-secondary" href="#%s">%s</a>' % (k, esc(n)) for k, n in courses))
    first = recs[0]
    title = "GCSE Computer Science%s stretch tasks" % (" and Creative iMedia" if "imedia" in [k for k, _ in courses] else "")
    return _hub_page(path=HUB4, title=title, h1=HUB4_TITLE,
                     lead=_hub4_lead(n for _, n in courses), trail=[("Home", "/"), (HUB4_TITLE, None)],
                     sections="".join(sections), tasks=TASKS, jump=jump,
                     course_name=first["course_name"], course_url=first["course_url"], active=first["active"])


def _publish(recs, register, add_search):
    for i, r in enumerate(recs):
        nxt = recs[i + 1] if i + 1 < len(recs) else None
        prev = recs[i - 1] if i else None
        write(r["url"], _lesson_page(r, nxt, prev))
        register(r["url"], 0.6, "monthly")
        if r["stage"] == "ks3":
            add_search("Stretch tasks: %s" % r["title"], r["url"],
                       "%s %s, lesson %d" % (r["topic"].spec, r["topic"].title, r["n"]),
                       ("stretch task challenge quiz game this or that pixel cat memory match pairs ks3 %s %s %s"
                        % (r["year"], r["topic"].title, r["title"])).lower())
        else:
            add_search("Stretch tasks: %s" % r["title"], r["url"], "%s %s" % (r["cname"], r["topic"].spec),
                       ("stretch task challenge quiz game this or that pixel cat memory match sort it ks4 gcse %s %s %s"
                        % (r["cname"], r["topic"].spec, r["title"])).lower())


def build(register, add_search):
    missing = check()
    if missing:
        raise SystemExit("Lessons with no stretch task:\n  " + "\n  ".join(missing))
    recs = records()
    ks3r = [r for r in recs if r["stage"] == "ks3"]
    ks4r = [r for r in recs if r["stage"] == "ks4"]
    _publish(ks3r, register, add_search)
    write(HUB, _hub(ks3r))
    register(HUB, 0.8, "weekly")
    add_search(HUB_TITLE, HUB, "Years 7, 8 and 9: three tasks for every lesson",
               "stretch tasks challenge extension fast finishers quiz game kahoot this or that pixel cat "
               "memory match pairs ks3 year 7 year 8 year 9 lessons")
    if ks4r:
        for key in dict.fromkeys(r["ckey"] for r in ks4r):
            _publish([r for r in ks4r if r["ckey"] == key], register, add_search)
        write(HUB4, _hub4(ks4r))
        register(HUB4, 0.8, "weekly")
        add_search(HUB4_TITLE, HUB4, "GCSE: four tasks for every topic",
                   "stretch tasks challenge extension fast finishers quiz game kahoot this or that pixel cat "
                   "memory match sort it ks4 gcse computer science revision games")
    n_q = sum(len(r["stretch"].blitz) + len(r["stretch"].short) + len(r["stretch"].long) for r in recs)
    n_p = sum(len(r["stretch"].picks) for r in recs)
    n_m = sum(len(r["stretch"].pairs) for r in recs)
    n_s = sum(len(r["stretch"].sort.items) for r in recs if r["stretch"].sort)
    print("Stretch tasks: %d lessons (%d at Key Stage 4), %d quiz questions, %d This or That questions, "
          "%d Memory Match pairs and %d Sort It cards checked" % (len(recs), len(ks4r), n_q, n_p, n_m, n_s))
