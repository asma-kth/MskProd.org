"""HTML rendering for the MskProd Computing revision site.

Every page is plain static HTML with server rendered content, so search engines
and students with JavaScript disabled both get the full text. JavaScript only
adds interactivity on top.
"""
import html
import json
import os
import re
from typing import List, Optional

from . import markup
from .models import Topic, Unit, Course, Q, EQ

SITE_NAME = "MskProd Computing"
SITE_URL = "https://mskprod.org"
TAGLINE = "UK computing revision, built for the top grade"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, "dist")

_ICONS_CACHE = None
_MASCOT_CACHE = None
_LOGO_CACHE = None


def _asset(name: str) -> str:
    with open(os.path.join(ROOT, "static", "img", name), encoding="utf-8") as fh:
        return fh.read()


def icons() -> str:
    global _ICONS_CACHE
    if _ICONS_CACHE is None:
        _ICONS_CACHE = _asset("icons.svg")
    return _ICONS_CACHE


def mascot_svg() -> str:
    global _MASCOT_CACHE
    if _MASCOT_CACHE is None:
        _MASCOT_CACHE = _asset("mascot.svg")
    return _MASCOT_CACHE


def logo_svg(cls: str = "brand-logo") -> str:
    global _LOGO_CACHE
    if _LOGO_CACHE is None:
        _LOGO_CACHE = _asset("logo.svg")
    return _LOGO_CACHE.replace("<svg ", '<svg class="%s" ' % cls, 1)


def ico(name: str, cls: str = "icon") -> str:
    return '<svg class="%s" aria-hidden="true" focusable="false"><use href="#%s"></use></svg>' % (cls, name)


def esc(s: str) -> str:
    return html.escape(str(s or ""), quote=True)


def slugify(s: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", str(s).lower()).strip("-")
    return s or "section"


# ===================================================================== nav

NAV = [
    ("KS3", "/ks3/", "i-layers"),
    ("GCSE CS", "/ks4/computer-science/", "i-cpu"),
    ("iMedia", "/ks4/imedia/", "i-palette"),
    ("A Level", "/ks5/", "i-brain"),
    ("Python", "/python/", "i-python"),
    ("Papers", "/exam-papers/", "i-paper"),
    ("Tools", "/tools/", "i-tools"),
    ("Progress", "/progress/", "i-target"),
]


def _nav(active: str) -> str:
    out = []
    for label, href, icon in NAV:
        # Exact match only: both KS4 courses share the /ks4/ prefix, so a
        # startswith test would highlight two navigation items at once.
        cur = ' aria-current="page"' if active and href == active else ""
        out.append('<a href="%s"%s><span>%s</span></a>' % (href, cur, esc(label)))
    return "".join(out)


# ================================================================== layout

def layout(*, title: str, description: str, path: str, body: str,
           active: str = "", topic_id: str = "", greeting: str = "",
           jsonld: Optional[list] = None, extra_head: str = "",
           scripts: Optional[list] = None, show_progress: bool = False) -> str:
    """Wrap page body in the full site chrome."""
    canonical = SITE_URL + path
    full_title = title if title.endswith(SITE_NAME) else "%s | %s" % (title, SITE_NAME)
    scripts = list(scripts or [])
    ld = jsonld or []

    # Interactive tools ship as one bundle, pulled in only by pages that mount
    # one, so a topic with no tool on it downloads nothing extra.
    if 'data-tool="' in body:
        extra_head += '<link rel="stylesheet" href="/assets/css/tools.css">'
        scripts.append("/assets/js/tools.js")

    # Runnable Python. The marker goes on <main>, and pyrun.js finds the Python
    # code blocks inside it. Pyodide itself is fetched only when a Run button is
    # pressed, so a page that is merely read costs nothing extra.
    py_attr = ""
    if '<span class="code-label">Python</span>' in body:
        py_attr = " data-pyrun"
        scripts.append("/assets/js/pyrun.js")
    ld_html = "".join(
        '<script type="application/ld+json">%s</script>' % json.dumps(x, separators=(",", ":"))
        for x in ld)

    return """<!doctype html>
<html lang="en-GB">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>{full_title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1">
<meta name="author" content="MskProd Computing">
<meta name="theme-color" content="#FCFBF8" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#15161A" media="(prefers-color-scheme: dark)">
<meta property="og:type" content="website">
<meta property="og:site_name" content="{site}">
<meta property="og:title" content="{ogtitle}">
<meta property="og:description" content="{desc}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{site_url}/assets/img/share.png">
<meta property="og:locale" content="en_GB">
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{ogtitle}">
<meta name="twitter:description" content="{desc}">
<meta name="twitter:image" content="{site_url}/assets/img/share.png">
<link rel="icon" href="/assets/img/favicon.svg" type="image/svg+xml">
<link rel="apple-touch-icon" href="/assets/img/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<link rel="sitemap" type="application/xml" href="/sitemap.xml">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Newsreader:opsz,wght@6..72,400;6..72,500;6..72,600&family=IBM+Plex+Sans:wght@400;450;500;600&family=IBM+Plex+Mono:wght@400;500&display=swap">
<link rel="stylesheet" href="/assets/css/site.css">
{extra_head}
{ld_html}
</head>
<body class="no-js"{topic_attr}{greet_attr}>
<script>document.body.classList.remove("no-js");</script>
<a class="skip-link" href="#main">Skip to content</a>
{icons}
{progress}
<header class="site-header">
  <div class="wrap header-inner">
    <a class="brand" href="/">
      {logo}
      <span class="brand-name"><b>MskProd</b><span>Computing</span></span>
    </a>
    <nav class="nav" id="primaryNav" aria-label="Main">{nav}</nav>
    <div class="header-tools">
      <button class="icon-btn" type="button" data-search-open aria-label="Search the site">{search_icon}</button>
      <button class="icon-btn" type="button" id="themeBtn" aria-label="Switch theme">{moon}</button>
      <button class="icon-btn nav-toggle" type="button" id="navToggle" aria-expanded="false"
              aria-controls="primaryNav" aria-label="Open menu">{menu}</button>
    </div>
  </div>
</header>
<main id="main"{py_attr}>
{body}
</main>
{footer}
{search_shell}
{mascot}
<script>window.MSK_BASE="/";</script>
<script src="/assets/js/app.js" defer></script>
<script src="/assets/js/mascot.js" defer></script>
{scripts}
</body>
</html>""".format(
        full_title=esc(full_title),
        ogtitle=esc(title),
        desc=esc(description[:300]),
        canonical=canonical,
        site=SITE_NAME,
        site_url=SITE_URL,
        extra_head=extra_head,
        ld_html=ld_html,
        topic_attr=' data-topic="%s"' % esc(topic_id) if topic_id else "",
        greet_attr=' data-cat-greeting="%s"' % esc(greeting) if greeting else "",
        icons=icons(),
        progress='<div class="progress-bar" id="readProgress"></div>' if show_progress else "",
        logo=logo_svg(),
        nav=_nav(active),
        search_icon=ico("i-search"),
        moon=ico("i-moon"),
        menu=ico("i-menu"),
        body=body,
        py_attr=py_attr,
        footer=footer(),
        search_shell=search_shell(),
        mascot=mascot(),
        scripts="".join('<script src="%s" defer></script>' % s for s in scripts),
    )


def search_shell() -> str:
    return """<div class="search-shell" id="searchShell" hidden role="dialog" aria-modal="true" aria-label="Search">
  <div class="search-panel">
    <input id="searchInput" type="search" placeholder="Search topics, quizzes and papers" autocomplete="off" spellcheck="false" aria-label="Search query">
    <div class="search-results" id="searchResults"><p class="search-empty">Start typing to find any topic, quiz or paper.</p></div>
    <div class="search-foot"><span>Enter to open</span><span>Arrow keys to move</span><span>Esc to close</span></div>
  </div>
</div>"""


def mascot() -> str:
    return """<div class="mascot-dock">
  <div class="mascot-bubble" id="mascotBubble" hidden role="status" aria-live="polite">
    <button class="bubble-close" type="button" aria-label="Close Pixel">%s</button>
    <b data-bubble-title>Pixel says</b>
    <p data-bubble-text></p>
    <div class="mascot-actions">
      <button type="button" data-cat="fact">Fun fact</button>
      <button type="button" data-cat="tip">Revision tip</button>
      <button type="button" data-cat="quiet">Not now</button>
    </div>
  </div>
  <button class="mascot-btn" id="mascotBtn" type="button" aria-expanded="false"
          aria-label="Pixel the robot cat: tap for a fun fact or a revision tip">%s</button>
</div>""" % (ico("i-cross"), mascot_svg())


def footer() -> str:
    return """<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <div class="footer-brand">%s<span>MskProd Computing</span></div>
        <p>Free computing revision for UK students at Key Stage 3, GCSE and A Level. Written board by board for OCR, AQA and Edexcel, structured as a journey to the top grade, and completely free to use with no account and no tracking.</p>
      </div>
      <div>
        <h4>Revise</h4>
        <ul>
          <li><a href="/ks3/">Key Stage 3</a></li>
          <li><a href="/ks4/computer-science/">GCSE Computer Science, OCR</a></li>
          <li><a href="/ks4/aqa-computer-science/">GCSE Computer Science, AQA</a></li>
          <li><a href="/ks4/edexcel-computer-science/">GCSE Computer Science, Edexcel</a></li>
          <li><a href="/ks4/imedia/">Creative iMedia</a></li>
          <li><a href="/ks5/">A Level Computer Science</a></li>
          <li><a href="/python/">Python from scratch</a></li>
        </ul>
      </div>
      <div>
        <h4>Practise</h4>
        <ul>
          <li><a href="/exam-papers/">Practice exam papers</a></li>
          <li><a href="/tools/">Interactive tools</a></li>
          <li><a href="/worksheets/">Printable worksheets</a></li>
          <li><a href="/progress/">Your progress</a></li>
          <li><a href="/how-to-revise/">How to revise properly</a></li>
          <li><a href="/glossary/">Computing glossary</a></li>
          <li><a href="/sitemap.xml">Sitemap</a></li>
        </ul>
      </div>
      <div>
        <h4>Site</h4>
        <ul>
          <li><a href="/assign/">Set an assignment</a></li>
          <li><a href="/about/">About</a></li>
          <li><a href="/privacy/">Privacy policy</a></li>
          <li><a href="/accessibility/">Accessibility</a></li>
        </ul>
      </div>
    </div>
    <div class="footer-bottom">
      <span>Copyright MskProd Computing. Content written independently and not endorsed by any exam board.</span>
      <span>No accounts. No cookies. No tracking.</span>
    </div>
  </div>
</footer>""" % logo_svg("")


# ============================================================== components

def crumbs(trail: List[tuple]) -> str:
    """trail: list of (label, href or None for the current page)."""
    parts = []
    for i, (label, href) in enumerate(trail):
        if i:
            parts.append('<span class="sep">/</span>')
        if href:
            parts.append('<a href="%s">%s</a>' % (href, esc(label)))
        else:
            parts.append("<span>%s</span>" % esc(label))
    return '<nav class="crumbs" aria-label="Breadcrumb">%s</nav>' % "".join(parts)


def crumbs_ld(trail: List[tuple]) -> dict:
    items = []
    for i, (label, href) in enumerate(trail):
        entry = {"@type": "ListItem", "position": i + 1, "name": label}
        if href:
            entry["item"] = SITE_URL + href
        items.append(entry)
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": items}


def render_quiz(topic_slug: str, questions: List[Q], title: str = "Knowledge check",
                lead: str = "") -> str:
    if not questions:
        return ""
    qs = []
    for i, q in enumerate(questions):
        opts = []
        for j, opt in enumerate(q.options):
            opts.append(
                '<label class="opt"%s>'
                '<input type="radio" name="%s-q%d" tabindex="-1">'
                '<span class="mark">%s</span><span>%s</span></label>'
                % (' data-correct="1"' if j == q.answer else "",
                   topic_slug, i, "ABCDEFGH"[j], markup.inline(opt)))
        qs.append(
            '<div class="q" tabindex="0"><div class="q-stem"><span class="n">%d</span>'
            '<span>%s</span></div><div class="q-opts">%s</div>'
            '<div class="q-feedback" data-explain="%s"></div></div>'
            % (i + 1, markup.inline(q.stem), "".join(opts), esc(markup.inline(q.explain))))
    return """<section class="quiz" id="quiz" data-quiz-id="%s" aria-labelledby="quizTitle">
  <div class="quiz-head">
    <div>
      <h2 id="quizTitle">%s</h2>
      <p>%s</p>
    </div>
    <span class="quiz-counter" data-counter>0 of %d answered</span>
  </div>
  %s
  <div class="q-feedback" data-quiz-done></div>
  <div class="quiz-foot">
    <span class="quiz-score" data-score>Score <span class="pct">0 / %d</span></span>
    <span class="scorebar"><i></i></span>
    <button class="btn btn-secondary btn-sm" type="button" data-quiz-reset>%s Try again</button>
    <button class="btn btn-ghost btn-sm" type="button" data-quiz-shuffle>%s Shuffle answers</button>
  </div>
</section>""" % (esc(topic_slug), esc(title),
                 esc(lead or "Ten questions on what you have just read. Pick an answer to see whether it is right and why."),
                 len(questions), "".join(qs), len(questions),
                 ico("i-repeat"), ico("i-shuffle"))


def render_exam(topic_slug: str, questions: List[EQ], title: str = "Exam-style questions",
                lead: str = "", heading_level: str = "h2") -> str:
    if not questions:
        return ""
    total = sum(q.marks for q in questions)
    qs = []
    for i, q in enumerate(questions):
        pts = "".join(
            '<li data-any=\'%s\'><span class="tick">%s</span><span>%s</span></li>'
            % (html.escape(json.dumps(p.any), quote=True), "L", markup.inline(p.text))
            for p in q.points)
        cmdbadge = '<span class="badge">%s</span>' % esc(q.command) if q.command else ""
        qs.append("""<div class="examq" data-marks="%d" data-exam-id="%s-e%d">
  <div class="examq-head"><span class="n">%d</span><span class="stem">%s</span><span class="marks">%d %s</span></div>
  %s
  <textarea placeholder="Write your answer here, the way you would in the exam." aria-label="Your answer to question %d"></textarea>
  <div class="examq-tools">
    <button class="btn btn-primary btn-sm" type="button" data-mark>%s Mark my answer</button>
    <button class="btn btn-ghost btn-sm" type="button" data-exam-reset>Clear</button>
    <span class="muted" style="font-size:.8rem">Ctrl and Enter also marks it</span>
  </div>
  <div class="examq-result">
    <p class="muted" data-verdict style="font-size:.9rem"></p>
    <div class="ms">
      <div class="ms-head">%s Mark scheme<span class="award">0 / %d</span></div>
      <ul>%s</ul>
      <div class="model-answer"><b>Model answer</b><p>%s</p></div>
      <div class="self-mark">
        <label for="self-%s-%d">Examiner override</label>
        <select data-self id="self-%s-%d"></select>
        <span>The marker looks for key phrases. If you said it another way and it is still right, give yourself the mark.</span>
      </div>
    </div>
  </div>
</div>""" % (q.marks, esc(topic_slug), i, i + 1, markup.inline(q.stem), q.marks,
             "mark" if q.marks == 1 else "marks", cmdbadge, i + 1, ico("i-check"),
             ico("i-paper"), q.marks, pts, markup.inline(q.model),
             esc(topic_slug), i, esc(topic_slug), i))

    return """<section class="quiz" id="exam" data-exam-set aria-labelledby="examTitle">
  <div class="quiz-head">
    <div>
      <%s id="examTitle">%s</%s>
      <p>%s</p>
    </div>
    <span class="quiz-counter">%d marks</span>
  </div>
  %s
  <div class="quiz-foot">
    <span class="quiz-score" data-exam-total>Machine mark <span class="pct">0 / %d</span></span>
    <span class="scorebar"><i data-exam-bar></i></span>
    <button class="btn btn-primary btn-sm" type="button" data-mark-all>%s Mark everything</button>
  </div>
</section>""" % (heading_level, esc(title), heading_level,
                 esc(lead or "Five written questions in the style of the real paper. Write a full answer, then let the marker check it against the mark scheme."),
                 total, "".join(qs), total, ico("i-check"))


def keyterms_block(terms) -> str:
    if not terms:
        return ""
    rows = "".join('<div class="keyterm"><dt>%s</dt><dd>%s</dd></div>'
                   % (markup.inline(t), markup.inline(d)) for t, d in terms)
    return '<h2 id="key-terms">Key terms you must be able to define</h2><dl class="keyterms">%s</dl>' % rows


def flashcards(terms, limit: int = 8) -> str:
    if not terms:
        return ""
    cards = "".join(
        '<div class="flashcard" tabindex="0" role="button" aria-label="Flashcard: %s. Activate to reveal the definition.">'
        '<div class="flashcard-inner">'
        '<div class="flashcard-face flashcard-front"><small>Define</small><span>%s</span></div>'
        '<div class="flashcard-face flashcard-back"><small>Answer</small><span>%s</span></div>'
        "</div></div>" % (esc(t), markup.inline(t), markup.inline(d))
        for t, d in terms[:limit])
    return ('<h2 id="flashcards">Flashcards</h2>'
            '<p>Say the definition out loud before you flip the card. Retrieving it from memory is what builds recall, reading it again is not.</p>'
            '<div class="flashdeck grid grid-2">%s</div>' % cards)


# ================================================================== pages

def topic_page(course: Course, unit: Unit, topic: Topic,
               prev_link=None, next_link=None) -> tuple:
    """Return (path, html) for one topic page."""
    path = "/%s/%s/" % (course.slug, topic.slug)
    # Progress is keyed by course and topic together: two courses can legitimately
    # use the same topic slug, and an unqualified key would merge their scores.
    tid = "%s/%s" % (course.slug, topic.slug)
    worksheet_link = (
        '<a class="btn btn-secondary" style="width:100%%;justify-content:center" '
        'href="/%s/%s/worksheet/">%s Printable worksheet</a>'
        % (course.slug, topic.slug, ico("i-paper"))
        if (topic.quiz or topic.exam) else "")
    trail = [("Home", "/"), (course.short, "/%s/" % course.slug),
             (unit.title, "/%s/#%s" % (course.slug, unit.slug)), (topic.title, None)]

    # sections
    sec_html, toc = [], []
    for s in topic.sections:
        sid = s.id or slugify(s.title)
        toc.append((sid, s.title))
        sec_html.append('<h2 id="%s">%s</h2>\n%s' % (sid, esc(s.title), markup.render(s.body)))

    if topic.keyterms:
        toc.append(("key-terms", "Key terms"))
        sec_html.append(keyterms_block(topic.keyterms))
        toc.append(("flashcards", "Flashcards"))
        sec_html.append(flashcards(topic.keyterms))

    if topic.grade:
        toc.append(("top-grade", "Reach the top grade"))
        sec_html.append('<h2 id="top-grade">Reach the top grade on this topic</h2>%s'
                        % markup.render(topic.grade))

    if topic.mistakes:
        toc.append(("mistakes", "Common mistakes"))
        sec_html.append(
            '<h2 id="mistakes">Mistakes that cost marks here</h2>'
            '<p>Every one of these is something students actually write. Read them now so you do not write them in May.</p>'
            '<div class="note note-warn"><div class="note-title">%s Avoid these</div><ul>%s</ul></div>'
            % (ico("i-warn"), "".join("<li>%s</li>" % markup.inline(m) for m in topic.mistakes)))

    if topic.quiz:
        toc.append(("quiz", "Knowledge check"))
    if topic.exam:
        toc.append(("exam", "Exam-style questions"))

    toc_html = '<div class="toc"><h4>On this page</h4><ol>%s</ol></div>' % "".join(
        '<li><a href="#%s">%s</a></li>' % (i, esc(t)) for i, t in toc)

    badges = ['<span class="badge badge-%s">%s</span>' % (course.stage.lower(), esc(course.stage))]
    if topic.spec:
        badges.append('<span class="badge badge-spec">%s %s</span>' % (esc(course.code or course.board), esc(topic.spec)))
    badges.append('<span class="badge">%s %d min read</span>' % (ico("i-clock"), topic.minutes))
    if topic.quiz:
        badges.append('<span class="badge">%s %d question quiz</span>' % (ico("i-check-circle"), len(topic.quiz)))
    if topic.exam:
        badges.append('<span class="badge">%s %d exam marks</span>' % (ico("i-paper"), sum(q.marks for q in topic.exam)))

    nav_html = ""
    if prev_link or next_link:
        bits = []
        if prev_link:
            bits.append('<a class="prev" href="%s"><span>%s Previous</span><b>%s</b></a>'
                        % (prev_link[1], ico("i-arrow-left"), esc(prev_link[0])))
        else:
            bits.append('<a class="prev" href="/%s/"><span>%s Back</span><b>%s</b></a>'
                        % (course.slug, ico("i-arrow-left"), esc(course.short)))
        if next_link:
            bits.append('<a class="next" href="%s"><span>Next %s</span><b>%s</b></a>'
                        % (next_link[1], ico("i-arrow-right"), esc(next_link[0])))
        nav_html = '<nav class="topic-nav" aria-label="Topic">%s</nav>' % "".join(bits)

    fact = ""
    if topic.fact:
        fact = ('<div class="note note-fact"><div class="note-title">%s Pixel fun fact</div><p>%s</p></div>'
                % (ico("i-sparkle"), markup.inline(topic.fact)))

    body = """<div class="wrap">
  %s
  <div class="topic-layout">
    <article class="prose">
      <header class="topic-header">
        <div class="badge-row">%s</div>
        <h1>%s</h1>
        <p class="lead">%s</p>
      </header>
      %s
      %s
      %s
      %s
      %s
    </article>
    <aside class="topic-aside">
      %s
      <div class="aside-block">
        <h4>Study order</h4>
        <p>Read the explanation, do the ten question check, then write the five exam answers from memory. Come back in three days and redo the quiz only.</p>
        %s
      </div>
    </aside>
  </div>
</div>""" % (crumbs(trail), "".join(badges), esc(topic.title), markup.inline(topic.blurb),
             "\n".join(sec_html), fact,
             render_quiz(tid, topic.quiz),
             render_exam(tid, topic.exam),
             nav_html, toc_html, worksheet_link)

    desc = topic.blurb if len(topic.blurb) > 70 else topic.blurb + " Full explanation, a ten question check and five auto marked exam-style questions."
    ld = [crumbs_ld(trail), {
        "@context": "https://schema.org",
        "@type": "LearningResource",
        "name": topic.title,
        "description": desc,
        "url": SITE_URL + path,
        "learningResourceType": "Revision guide",
        "educationalLevel": course.stage,
        "inLanguage": "en-GB",
        "isAccessibleForFree": True,
        "teaches": topic.title,
        "isPartOf": {"@type": "Course", "name": course.title, "url": SITE_URL + "/" + course.slug + "/"},
        "provider": {"@type": "Organization", "name": SITE_NAME, "url": SITE_URL},
    }]
    if topic.quiz:
        ld.append({
            "@context": "https://schema.org", "@type": "Quiz",
            "name": "%s knowledge check" % topic.title,
            "url": SITE_URL + path + "#quiz",
            "educationalLevel": course.stage,
            "about": {"@type": "Thing", "name": topic.title},
            "hasPart": [{
                "@type": "Question", "eduQuestionType": "Multiple choice",
                "text": q.stem,
                "acceptedAnswer": {"@type": "Answer", "text": q.options[q.answer]},
                "suggestedAnswer": [{"@type": "Answer", "text": o}
                                    for i, o in enumerate(q.options) if i != q.answer],
            } for q in topic.quiz[:10]],
        })

    greet = ("Welcome to %s. Read it once slowly, then do the quiz without scrolling back. That is where the learning happens."
             % topic.title)
    return path, layout(title="%s | %s revision" % (topic.title, course.short),
                        description=desc, path=path, body=body,
                        active="/%s/" % course.slug,
                        topic_id=tid, greeting=greet, jsonld=ld,
                        scripts=["/assets/js/quiz.js"], show_progress=True)


def unit_block(course: Course, unit: Unit) -> str:
    rows = []
    for i, t in enumerate(unit.topics):
        rows.append(
            '<a class="unit-row" href="/%s/%s/" data-topic-ref="%s">'
            '<span class="unit-num">%s</span>'
            '<span><b>%s</b><small>%s</small></span>'
            '<span data-done-slot>%s</span></a>'
            % (course.slug, t.slug, esc("%s/%s" % (course.slug, t.slug)),
               esc(t.spec or str(i + 1)),
               esc(t.title), esc(t.blurb), ico("i-arrow-right")))
    return """<section class="section" id="%s">
  <div class="section-head">
    <div class="badge-row"><span class="badge">%s</span>%s</div>
    <h2>%s</h2>
    <p>%s</p>
  </div>
  <div class="unit-list">%s</div>
</section>""" % (esc(unit.slug), esc(unit.term or course.short),
                 '<span class="badge">%s %d topics</span>' % (ico("i-list"), len(unit.topics)),
                 esc(unit.title), esc(unit.blurb), "".join(rows))


def course_page(course: Course) -> tuple:
    path = "/%s/" % course.slug
    trail = [("Home", "/"), (course.short, None)]
    total_topics = sum(len(u.topics) for u in course.units)
    total_quiz = sum(len(t.quiz) for u in course.units for t in u.topics)
    total_marks = sum(q.marks for u in course.units for t in u.topics for q in t.exam)

    journey = ""
    if course.journey:
        steps = "".join(
            '<div class="journey-step"><div class="journey-dot">%02d</div>'
            '<div class="journey-body"><h3>%s</h3><p>%s</p></div></div>'
            % (i + 1, esc(a), markup.inline(b)) for i, (a, b, _c) in enumerate(course.journey))
        journey = """<section class="section section-alt"><div class="wrap">
          <div class="section-head"><h2>Your route to %s</h2>
          <p>Revision works when it has an order. Follow these stages rather than opening topics at random.</p></div>
          <div class="journey">%s</div></div></section>""" % (esc(course.goal or "the top grade"), steps)

    units_html = "".join(unit_block(course, u) for u in course.units)

    body = """<div class="wrap">%s</div>
<section class="hero"><div class="wrap">
  <div class="hero-grid">
    <div>
      <span class="eyebrow">%s%s</span>
      <h1>%s</h1>
      <p class="lead">%s</p>
      <div class="btn-row" style="margin-top:1.6rem">
        <a class="btn btn-primary" href="/%s/%s/">%s Start the first topic</a>
        <a class="btn btn-secondary" href="/exam-papers/">%s Practice papers</a>
        <a class="btn btn-ghost" href="/worksheets/">%s Printable worksheets</a>
      </div>
    </div>
    <div class="stat-row">
      <div class="stat"><b>%d</b><span>Topics</span></div>
      <div class="stat"><b>%d</b><span>Quiz questions</span></div>
      <div class="stat"><b>%d</b><span>Exam marks</span></div>
      <div class="stat"><b>%s</b><span>Target grade</span></div>
    </div>
  </div>
</div></section>
%s
<div class="wrap">%s</div>""" % (
        crumbs(trail),
        ico("i-target"),
        esc(" %s %s" % (course.board, course.code)).strip() or " Revision course",
        esc(course.title), markup.inline(course.blurb),
        course.slug, course.units[0].topics[0].slug if course.units and course.units[0].topics else "",
        ico("i-play"), ico("i-paper"), ico("i-list"),
        total_topics, total_quiz, total_marks, esc(course.goal or "Top"),
        journey, units_html)

    ld = [crumbs_ld(trail), {
        "@context": "https://schema.org", "@type": "Course",
        "name": course.title, "description": course.blurb,
        "url": SITE_URL + path, "inLanguage": "en-GB",
        "educationalLevel": course.stage,
        "isAccessibleForFree": True,
        "provider": {"@type": "Organization", "name": SITE_NAME, "url": SITE_URL},
        "hasCourseInstance": {"@type": "CourseInstance", "courseMode": "online",
                              "courseWorkload": "PT%dH" % max(1, total_topics // 2)},
        "syllabusSections": [{"@type": "Syllabus", "name": u.title,
                              "description": u.blurb} for u in course.units],
    }]
    greet = ("This is the whole %s course mapped out. Start at the top and work down, it is ordered the way it is taught."
             % course.short)
    return path, layout(title=course.title, description=course.blurb, path=path,
                        body=body, active="/%s/" % course.slug,
                        greeting=greet, jsonld=ld)


def write(path: str, html_text: str):
    out = os.path.join(DIST, path.strip("/"), "index.html") if path != "/" \
        else os.path.join(DIST, "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(html_text)
    return out
