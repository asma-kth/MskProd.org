"""HTML rendering for the MskProd Computing revision site.

Every page is plain static HTML with server rendered content, so search engines
and students with JavaScript disabled both get the full text. JavaScript only
adds interactivity on top.
"""
import html
from urllib.parse import quote
import json
import os
import re
from typing import List, Optional

from . import cat
from . import markup
from .util import slugify
from .models import Topic, Unit, Course, Q, EQ

SITE_NAME = "MskProd Computing"
SITE_URL = "https://mskprod.org"
CONTACT_EMAIL = "a.kethiri@mskprod.org"
TAGLINE = "UK computing revision, built for the top grade"

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, "dist")

_ICONS_CACHE = None


def _asset(name: str) -> str:
    with open(os.path.join(ROOT, "static", "img", name), encoding="utf-8") as fh:
        return fh.read()


def icons() -> str:
    global _ICONS_CACHE
    if _ICONS_CACHE is None:
        _ICONS_CACHE = _asset("icons.svg")
    return _ICONS_CACHE


def mascot_svg() -> str:
    """The dock cat: one flat drawing, because it is 44px in a corner."""
    return cat.flat()


def logo_svg(cls: str = "brand-logo") -> str:
    """The same cat's head, on its cream plate. Generated rather than read
    from a file, so the logo and the mascot cannot drift into two cats.

    Not cached: each instance needs its own gradient ids, and the logo appears
    twice on every page.
    """
    return cat.flat(head_only=True, plate=True,
                    label="MskProd Computing", cls=cls)


def ico(name: str, cls: str = "icon") -> str:
    return '<svg class="%s" aria-hidden="true" focusable="false"><use href="#%s"></use></svg>' % (cls, name)


def esc(s: str) -> str:
    return html.escape(str(s or ""), quote=True)




# ===================================================================== nav

NAV = [
    ("KS3", "/ks3/", "i-layers"),
    ("GCSE CS", "/ks4/computer-science/", "i-cpu"),
    ("iMedia", "/ks4/imedia/", "i-palette"),
    ("A Level", "/ks5/", "i-brain"),
    ("Data", "/data-analytics/", "i-chart"),
    ("Python", "/python/", "i-python"),
    ("AI", "/ai/", "i-sparkle"),
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
        out.append('<a href="%s"%s>%s<span>%s</span></a>' % (href, cur, ico(icon), esc(label)))
    return "".join(out)


# ================================================================== layout


# A search result shows roughly the first 60 characters of a title and the
# first 160 of a description. Anything past that is cut, so the brand suffix is
# only worth adding when the words that win the click still fit in front of it.
TITLE_MAX = 60
DESC_MAX = 160


def _title(title: str) -> str:
    if title.endswith(SITE_NAME):
        return title
    suffix = " | " + SITE_NAME
    return title + suffix if len(title) + len(suffix) <= TITLE_MAX else title


def _meta_description(desc: str) -> str:
    """Trim a description to what a result actually shows.

    Several hub blurbs run past 250 characters, so the useful half was being
    cut mid sentence by Google. Cutting here, at a sentence end where one
    exists and a word boundary otherwise, keeps the page copy untouched and
    the snippet readable.
    """
    desc = " ".join(desc.split())
    if len(desc) <= DESC_MAX:
        return desc
    window = desc[:DESC_MAX]
    stop = max(window.rfind(". "), window.rfind("? "), window.rfind("! "))
    if stop >= 90:
        return window[:stop + 1]
    return window[:window.rfind(" ")].rstrip(",;:") + "."


def layout(*, title: str, description: str, path: str, body: str,
           active: str = "", topic_id: str = "",
           jsonld: Optional[list] = None, extra_head: str = "",
           scripts: Optional[list] = None, show_progress: bool = False,
           noindex: bool = False) -> str:
    """Wrap page body in the full site chrome."""
    canonical = SITE_URL + path
    full_title = _title(title)
    description = _meta_description(description)
    scripts = list(scripts or [])
    ld = jsonld or []

    # Interactive tools ship as one bundle, pulled in only by pages that mount
    # one, so a topic with no tool on it downloads nothing extra.
    if 'data-tool="' in body:
        extra_head += '<link rel="stylesheet" href="/assets/css/tools.css">'
        scripts.append("/assets/js/tools.js")

    # Stepped diagrams ship their stages inline and are usable without this
    # script, so it is only pulled in by pages that actually contain one.
    if 'diagram-steps' in body:
        scripts.append("/assets/js/diagrams.js")

    # Runnable Python. The marker goes on <main>, and pyrun.js finds the Python
    # code blocks inside it. Pyodide itself is fetched only when a Run button is
    # pressed, so a page that is merely read costs nothing extra.
    py_attr = ""
    if '<span class="code-label">Python</span>' in body:
        py_attr = " data-pyrun"
        if "/assets/js/pyrun.js" not in scripts:
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
<meta name="robots" content="{robots}">
<meta name="author" content="MskProd Computing">
<meta name="theme-color" content="#FDFAF0" media="(prefers-color-scheme: light)">
<meta name="theme-color" content="#0C2B2E" media="(prefers-color-scheme: dark)">
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
<link rel="preload" href="/assets/fonts/inter-400-700-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preload" href="/assets/fonts/poppins-700-latin.woff2" as="font" type="font/woff2" crossorigin>
<link rel="preconnect" href="https://pagead2.googlesyndication.com" crossorigin>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-6941224638209377"
     crossorigin="anonymous"></script>
<link rel="stylesheet" href="/assets/css/site.css">
{extra_head}
{ld_html}
</head>
<body class="no-js"{topic_attr}>
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
<div class="page-loader" id="pageLoader" aria-hidden="true">
{loader}
  <p>Waking Pixel…</p>
  <span class="loader-bar"><i></i></span>
</div>
<script>window.MSK_BASE="/";</script>
<script src="/assets/js/app.js" defer></script>
<script src="/assets/js/mascot.js" defer></script>
{scripts}
</body>
</html>""".format(
        full_title=esc(full_title),
        ogtitle=esc(title),
        desc=esc(description),
        loader=cat.stack("asleep", 170, zzz=True,
                         label="Pixel the robot cat, asleep"),
        robots=("noindex, follow" if noindex
                else "index, follow, max-image-preview:large, max-snippet:-1"),
        canonical=canonical,
        site=SITE_NAME,
        site_url=SITE_URL,
        extra_head=extra_head,
        ld_html=ld_html,
        topic_attr=' data-topic="%s"' % esc(topic_id) if topic_id else "",
        icons=icons(),
        progress='<div class="progress-bar" id="readProgress"></div>' if show_progress else "",
        logo=logo_svg(),
        nav=_nav(active),
        search_icon=ico("i-search"),
        menu=ico("i-menu"),
        body=body,
        py_attr=py_attr,
        footer=footer(path),
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


def footer(path: str = "") -> str:
    report = "/contact/?page=" + quote(path, safe="/") if path else "/contact/"
    return """<footer class="site-footer">
  <div class="wrap">
    <div class="footer-grid">
      <div>
        <div class="footer-brand">%s<span>MskProd Computing</span></div>
        <p>Free computing revision for UK students at Key Stage 3, GCSE and A Level, written board by board for OCR, AQA and Edexcel. No account, no subscription.</p>
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
          <li><a href="/data-analytics/">OCR Data Analytics, F200 to F202</a></li>
          <li><a href="/python/">Python from scratch</a></li>
          <li><a href="/ai/">Artificial Intelligence, zero to hero</a></li>
        </ul>
      </div>
      <div>
        <h4>Practise</h4>
        <ul>
          <li><a href="/exam-papers/">Practice exam papers</a></li>
          <li><a href="/pixel-run/">Pixel Run, the Python game</a></li>
          <li><a href="/progress/">Your progress</a></li>
          <li><a href="/how-to-revise/">How to revise properly</a></li>
          <li><a href="/glossary/">Computing glossary</a></li>
        </ul>
      </div>
      <div>
        <h4>Site</h4>
        <ul>
          <li><a href="/about/">About</a></li>
          <li><a href="/teachers/">For teachers</a></li>
          <li><a href="/contact/">Contact</a></li>
          <li><a href="/accessibility/">Accessibility</a></li>
          <li><a href="/privacy/">Privacy policy</a></li>
        </ul>
      </div>
    </div>
    <p class="footer-report">Spotted a mistake, a broken link or something you cannot use? <a href="%s">Report a problem with this page</a>, or email <a href="mailto:%s">%s</a>.</p>
    <div class="footer-bottom">
      <span>Copyright MskProd Computing. Content written independently and not endorsed by any exam board.</span>
      <span>No accounts and no subscription. Adverts are served by Google, as set out in the <a href="/privacy/">privacy policy</a>.</span>
    </div>
  </div>
</footer>""" % (logo_svg(""), esc(report), CONTACT_EMAIL, CONTACT_EMAIL)


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
      <h2 id="quizTitle">%s</h2>%s
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
                 ("<p>%s</p>" % esc(lead)) if lead else "",
                 len(questions), "".join(qs), len(questions),
                 ico("i-repeat"), ico("i-shuffle"))


def _stem_html(stem: str) -> str:
    """A question stem, with its scenario separated from what it asks.

    Exam questions are written as a scenario and then an instruction, with a
    blank line between. Rendered inline that blank line collapses and the two
    run together as one paragraph, which is not how the paper prints it and
    not how it reads. Everything before the final block is the scenario.
    """
    blocks = _stem_blocks(stem)
    if len(blocks) < 2 and (not blocks or blocks[0][0] == "para"):
        return markup.inline(stem.strip())
    # The instruction is the last paragraph, with any list or code that follows
    # it: "Write a program that:" and the bullet points it introduces.
    paras = [i for i, (kind, _) in enumerate(blocks) if kind == "para"]
    k = paras[-1] if paras else 0
    out = ['<span class="examq-scenario">%s</span>' % _stem_block(b) for b in blocks[:k]]
    out.append('<span class="examq-ask">%s</span>' % "".join(_stem_block(b) for b in blocks[k:]))
    return "".join(out)


def _stem_blocks(stem: str) -> list:
    """Split a stem into ("para" | "list" | "code", text) blocks."""
    blocks, buf, fence = [], [], None
    for line in stem.strip().split("\n"):
        if fence is not None:
            if line.strip().startswith("```"):
                blocks.append(("code", "\n".join(fence)))
                fence = None
            else:
                fence.append(line)
            continue
        if line.strip().startswith("```"):
            if buf:
                blocks.append(("para", "\n".join(buf)))
                buf = []
            fence = []
        elif not line.strip():
            if buf:
                blocks.append(("para", "\n".join(buf)))
                buf = []
        else:
            buf.append(line)
    if fence is not None:
        blocks.append(("code", "\n".join(fence)))
    if buf:
        blocks.append(("para", "\n".join(buf)))
    return [("list", b) if kind == "para" and all(ln.lstrip().startswith("- ") for ln in b.split("\n")) else (kind, b)
            for kind, b in blocks]


def _stem_block(block: tuple) -> str:
    # Only inline elements, because the stem sits inside a span; CSS lays them out as blocks.
    kind, text = block
    if kind == "code":
        return '<span class="examq-pre"><code>%s</code></span>' % html.escape(text, quote=False)
    if kind == "list":
        return '<span class="examq-list">%s</span>' % "".join(
            '<span class="examq-li">%s</span>' % markup.inline(ln.lstrip()[2:]) for ln in text.split("\n"))
    return markup.inline(text)


LETTERS = "ABCDEFGHIJ"


def _attr(value) -> str:
    """JSON for a data attribute, escaped for single quoted HTML."""
    return html.escape(json.dumps(value, separators=(",", ":")), quote=True)


def _ms_item(text: str, data: str = "") -> str:
    return '<li%s><span class="tick">L</span><span>%s</span></li>' % (data, markup.inline(text))


def _choice_html(q: EQ, qid: str) -> tuple:
    q.correct = sorted(q.correct)
    multi = len(q.correct) > 1
    typ = "checkbox" if multi else "radio"
    opts = "".join(
        '<label class="xq-opt"><input type="%s" name="%s" value="%d"%s>'
        '<span class="xq-letter">%s</span><span class="xq-text">%s</span></label>'
        % (typ, qid, i, ' data-c="1"' if i in q.correct else "", LETTERS[i], markup.inline(o))
        for i, o in enumerate(q.options))
    hint = ("Tick %s boxes." % ("two" if len(q.correct) == 2 else str(len(q.correct)))) if multi else "Tick one box."
    area = ('<div class="xq-opts" role="group" aria-label="Options for question %s">%s</div>'
            '<p class="xq-hint">%s</p>' % (esc(q.label or ""), opts, hint))
    if multi:
        items = "".join(_ms_item("**%s** %s" % (LETTERS[c], q.options[c])) for c in q.correct)
        items += _ms_item("No marks if more than %d boxes are ticked" % len(q.correct), ' class="xq-rule"')
    else:
        items = _ms_item("**%s** %s" % (LETTERS[q.correct[0]], q.options[q.correct[0]]))
    return area, items


def _matrix_html(q: EQ, qid: str) -> tuple:
    head = "<th></th>" + "".join('<th scope="col">%s</th>' % markup.inline(c) for c in q.cols)
    body = []
    for r, row in enumerate(q.rows):
        cells = "".join(
            '<td><label class="xq-cell"><input type="radio" name="%s-r%d" value="%d"%s>'
            '<span class="sr-only">%s</span></label></td>'
            % (qid, r, c, ' data-c="1"' if q.correct[r] == c else "", esc(col))
            for c, col in enumerate(q.cols))
        body.append('<tr data-row="%d"><th scope="row">%s</th>%s</tr>' % (r, markup.inline(row), cells))
    area = ('<div class="table-wrap xq-matrix-wrap"><table class="xq-matrix"><thead><tr>%s</tr></thead>'
            '<tbody>%s</tbody></table></div><p class="xq-hint">Tick one box in each row.</p>' % (head, "".join(body)))
    per = len(q.rows) // q.marks if q.marks and len(q.rows) % q.marks == 0 else 1
    if per == 1:
        items = "".join(_ms_item("%s: **%s**" % (row, q.cols[q.correct[r]]), ' data-rows="[%d]"' % r)
                        for r, row in enumerate(q.rows))
    else:
        items = ""
        for m in range(q.marks):
            rows = list(range(m * per, (m + 1) * per))
            text = "; ".join("%s: **%s**" % (q.rows[r], q.cols[q.correct[r]]) for r in rows)
            items += _ms_item("1 mark for both: " + text if per == 2 else "1 mark for all of: " + text,
                              ' data-rows="%s"' % _attr(rows))
    return area, items


def _blank_input(b, n: int, qid: str) -> str:
    return ('<input class="xq-blank" type="text" autocomplete="off" spellcheck="false" data-b="%d" '
            'data-accept="%s"%s%s size="%d" aria-label="%s">'
            % (n, _attr(b.accept), ' data-numeric="1"' if b.numeric else "",
               (' data-tol="%s"' % b.tol) if b.tol else "", max(3, b.width),
               esc(b.label or "Answer %d" % (n + 1))))


def _blanks_html(q: EQ, qid: str) -> tuple:
    if q.grid:
        head = ("<thead><tr>%s</tr></thead>" % "".join('<th scope="col">%s</th>' % markup.inline(h) for h in q.grid_head)
                if q.grid_head else "")
        rows = []
        for row in q.grid:
            cells = []
            for cell in row:
                if isinstance(cell, int):
                    cells.append("<td>%s</td>" % _blank_input(q.blanks[cell], cell, qid))
                else:
                    cells.append("<td>%s</td>" % markup.inline(str(cell)))
            rows.append("<tr>%s</tr>" % "".join(cells))
        area = '<div class="table-wrap"><table class="xq-grid">%s<tbody>%s</tbody></table></div>' % (head, "".join(rows))
    else:
        area = '<div class="xq-blanks">%s</div>' % "".join(
            '<label class="xq-blank-row">%s%s%s</label>' % (
                ('<span class="xq-blank-label">%s</span>' % markup.inline(b.label)) if b.label else "",
                _blank_input(b, n, qid),
                ('<span class="xq-unit">%s</span>' % esc(b.unit)) if b.unit else "")
            for n, b in enumerate(q.blanks))
    if q.working:
        area = ('<label class="xq-working-label" for="%s-w">Show your working</label>'
                '<textarea class="xq-working" id="%s-w" rows="3" placeholder="Working: method marks are given even when the final answer is wrong."></textarea>'
                % (qid, qid)) + area
    groups = q.groups or [("", [n]) for n in range(len(q.blanks))]
    items = ""
    for text, nums in groups:
        answer = ", ".join(q.blanks[n].accept[0] + (" " + q.blanks[n].unit if q.blanks[n].unit else "") for n in nums)
        line = "%s: **%s**" % (text, answer) if text else "**%s**" % answer
        if q.working and len(groups) == 1:
            line = "Correct answer, full marks: **%s**" % answer
        items += _ms_item(line, ' data-blanks="%s"' % _attr(nums))
    if q.working:
        items += "".join(_ms_item("Method: " + p.text, " data-any='%s'" % html.escape(json.dumps(p.any), quote=True))
                         for p in q.points)
    return area, items


def _code_html(q: EQ, qid: str) -> tuple:
    t = q.code
    is_sql = t.lang == "sql"
    rows = min(26, max(5 if is_sql else 8, t.starter.count("\n") + 3))
    feed = ("" if is_sql else
            '<div class="xq-code-in"><label class="tool-label" for="%s-in">Input for Run, one value per line</label>'
            '<textarea id="%s-in" rows="2" spellcheck="false"></textarea></div>' % (qid, qid))
    area = ('<div class="xq-code" data-lang="%s" data-checks="%s" data-files="%s"%s>'
            '<div class="xq-code-bar"><span class="xq-file">%s</span>'
            '<button class="tool-btn" type="button" data-code-run>Run</button>'
            '<button class="tool-btn" type="button" data-code-reset>Start again</button></div>'
            '<textarea class="xq-code-area" spellcheck="false" autocapitalize="off" autocomplete="off" rows="%d" '
            'aria-label="Your %s for question %s">%s</textarea>%s'
            '<pre class="xq-code-out" hidden><code></code></pre>'
            '<template class="xq-starter">%s</template></div>'
            % (esc(t.lang), _attr([c.expr for c in t.checks]), _attr(t.files),
               (' data-setup="%s"' % html.escape(t.setup, quote=True)) if is_sql else "", esc(t.filename),
               rows, "SQL" if is_sql else "program", esc(q.label or ""), esc(t.starter), feed, esc(t.starter)))
    items = "".join(_ms_item(c.text) for c in t.checks)
    return area, items


def _examq_html(q: EQ, i: int, slug: str) -> str:
    qid = "%s-e%d" % (slug, i)
    label = q.label or str(i + 1)
    kind = q.kind or "text"
    if kind == "choice":
        area, items = _choice_html(q, qid)
    elif kind == "matrix":
        area, items = _matrix_html(q, qid)
    elif kind == "blanks":
        area, items = _blanks_html(q, qid)
    elif kind == "code":
        area, items = _code_html(q, qid)
    else:
        area = ('<textarea placeholder="Write your answer as you would in the exam." aria-label="Your answer to question %s"></textarea>'
                % esc(label))
        items = "".join(
            "<li data-any='%s'><span class=\"tick\">L</span><span>%s</span></li>"
            % (html.escape(json.dumps(p.any), quote=True), markup.inline(p.text))
            for p in q.points)
    cmdbadge = '<span class="badge">%s</span>' % esc(q.command) if q.command else ""
    fig = ('<div class="examq-figure">%s</div>' % markup.render(q.figure)) if q.figure else ""
    model = markup.model(q.model) if q.model else ""
    if kind == "code":
        model += markup.code_block(q.code.solution.rstrip(), q.code.lang)
    self_mark = ('<div class="self-mark"><label for="self-%s">Examiner override</label>'
                 '<select data-self id="self-%s"></select><span>%s</span></div>'
                 % (qid, qid, "The marker looks for key phrases. If you said it another way and it is still right, give yourself the mark."
                    if kind == "text" or (kind == "blanks" and q.working) else
                    "Marked exactly against the mark scheme. Change it only if an examiner would accept your answer."))
    return """<div class="examq" data-kind="%s" data-marks="%d" data-exam-id="%s">
  <div class="examq-head"><span class="n">%s</span><span class="stem">%s</span><span class="marks">%d %s</span></div>
  %s%s
  %s
  <div class="examq-tools">
    <button class="btn btn-primary btn-sm" type="button" data-mark>%s Mark my answer</button>
    <button class="btn btn-ghost btn-sm" type="button" data-exam-reset>Clear</button>
  </div>
  <div class="examq-result">
    <p class="muted" data-verdict style="font-size:.9rem"></p>
    <div class="ms">
      <div class="ms-head">%s Mark scheme<span class="award">0 / %d</span></div>
      <ul>%s</ul>
      %s
      %s
      <p class="xq-report"><a href="/contact/?type=answer&amp;q=%s" data-report>Think this answer or mark scheme is wrong? Report it</a></p>
    </div>
  </div>
</div>""" % (esc(kind), q.marks, esc(qid), esc(label), _stem_html(q.stem), q.marks,
             "mark" if q.marks == 1 else "marks", cmdbadge, fig, area, ico("i-check"),
             ico("i-paper"), q.marks, items,
             ('<div class="model-answer"><b>%s</b>%s</div>' % ("Model answer" if kind != "code" else
                                                               "An answer that scores full marks" if q.code.lang == "sql" else
                                                               "A program that scores full marks", model)) if model else "",
             self_mark, quote(label, safe=""))


def render_exam(topic_slug: str, questions: List[EQ], title: str = "Exam-style questions",
                lead: str = "", heading_level: str = "h2") -> str:
    if not questions:
        return ""
    total = sum(q.marks for q in questions)
    qs = []
    for i, q in enumerate(questions):
        if q.section:
            sec_marks = 0
            for later in questions[i:]:
                if later is not q and later.section:
                    break
                sec_marks += later.marks
            qs.append('<div class="xq-section"><h3>%s <span>%d marks</span></h3>%s</div>'
                      % (esc(q.section), sec_marks,
                         ('<p>%s</p>' % markup.inline(q.section_note)) if q.section_note else ""))
        if q.lead:
            qs.append('<div class="xq-lead">%s</div>' % markup.render(q.lead))
        qs.append(_examq_html(q, i, topic_slug))

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
                 esc(lead or "Write a full answer, then let the marker check it against the mark scheme."),
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
            '<p>Say the definition out loud before you flip the card.</p>'
            '<div class="flashdeck grid grid-2">%s</div>' % cards)


# ================================================================== pages

from .illus_banners import banner as banner_for, course_banner


def _unit_exams_aside(topic) -> str:
    """Key Stage 3 units link to their two unit exams."""
    exams = getattr(topic, "exams", None)
    if not exams:
        return ""
    links = "".join(
        '<a class="btn %s" style="width:100%%;justify-content:center;margin-top:.5rem" href="%s">%s %s</a>'
        % ("btn-primary" if i == 0 else "btn-secondary", href, ico("i-clock"), esc(label))
        for i, (label, href, meta) in enumerate(exams))
    return ('<div class="aside-block"><h4>Unit exams</h4><p>%s</p>%s</div>'
            % (esc(exams[0][2]), links))


def _unit_exams_note(topic) -> str:
    exams = getattr(topic, "exams", None)
    if not exams:
        return ""
    links = " or ".join('<a href="%s">%s</a>' % (href, esc(label)) for label, href, meta in exams)
    return ('<div class="note note-exam" style="margin-top:var(--sp-5)"><div class="note-title">%s Sit a unit exam</div>'
            '<p>When you have finished this unit, sit %s. %s</p></div>' % (ico("i-clock"), links, esc(exams[0][2])))


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
        if course.levels:
            # A levelled course has no grades: the same slot holds the deeper
            # engineering notes for students who want more.
            toc.append(("go-further", "Go further"))
            sec_html.append('<h2 id="go-further">Go further: notes for future AI engineers</h2>%s'
                            % markup.render(topic.grade))
        else:
            toc.append(("top-grade", "Reach the top grade"))
            sec_html.append('<h2 id="top-grade">Reach the top grade on this topic</h2>%s'
                            % markup.render(topic.grade))

    if topic.mistakes:
        toc.append(("mistakes", "Misconceptions" if course.levels else "Common mistakes"))
        sec_html.append(
            '<h2 id="mistakes">%s</h2>'
            '<div class="note note-warn"><div class="note-title">%s Avoid these</div><ul>%s</ul></div>'
            % ("Misconceptions to avoid" if course.levels else "Mistakes that cost marks here",
               ico("i-warn"), "".join("<li>%s</li>" % markup.inline(m) for m in topic.mistakes)))

    if topic.quiz:
        toc.append(("quiz", "Knowledge check"))
    if topic.exam:
        toc.append(("exam", topic.exam_title))

    toc_html = '<div class="toc"><h4>On this page</h4><ol>%s</ol></div>' % "".join(
        '<li><a href="#%s">%s</a></li>' % (i, esc(t)) for i, t in toc)

    if course.levels:
        # "Level 3 · Explorer" and "Lesson 3.2" read better than a key stage
        # and a specification reference the course does not have.
        badges = ['<span class="badge badge-ks3">%s</span>' % esc(unit.term or unit.title)]
        if topic.spec:
            badges.append('<span class="badge badge-spec">Lesson %s</span>' % esc(topic.spec))
    else:
        badges = ['<span class="badge badge-%s">%s</span>' % (course.stage.lower(), esc(course.stage))]
        if topic.spec:
            badges.append('<span class="badge badge-spec">%s %s</span>' % (esc(course.code or course.board), esc(topic.spec)))
    badges.append('<span class="badge">%s %d min read</span>' % (ico("i-clock"), topic.minutes))
    if topic.quiz:
        badges.append('<span class="badge">%s %d question quiz</span>' % (ico("i-check-circle"), len(topic.quiz)))
    if topic.exam:
        # Coursework topics have no exam, so their written practice is not
        # counted as exam marks.
        kind = "exam marks" if topic.exam_title == "Exam-style questions" else "marks of written practice"
        badges.append('<span class="badge">%s %d %s</span>' % (ico("i-paper"), sum(q.marks for q in topic.exam), kind))

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
        fact = ('<div class="note note-fact"><div class="note-title">%s Fun fact</div><p>%s</p></div>'
                % (ico("i-sparkle"), markup.inline(topic.fact)))

    body = """<div class="wrap">
  %s
  <div class="topic-layout">
    <article class="prose">
      <header class="topic-header">
        %s
        <div class="badge-row">%s</div>
        <h1>%s</h1>
        <p class="lead">%s</p>
      </header>
      %s
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
        <p>%s</p>
        %s
      </div>
      %s
    </aside>
  </div>
</div>""" % (crumbs(trail), banner_for(course.slug, topic.slug), "".join(badges), esc(topic.title), markup.inline(topic.blurb),
             "\n".join(sec_html), fact,
             render_quiz(tid, topic.quiz),
             render_exam(tid, topic.exam, topic.exam_title),
             _unit_exams_note(topic),
             nav_html, toc_html,
             ("Read, run every example, then score 70% or more in the knowledge check "
              "to count this lesson towards your certificate."
              if course.levels else
              "Read the explanation, do the ten question check, then write the exam answers "
              "from memory."),
             worksheet_link, _unit_exams_aside(topic))

    desc = topic.blurb if len(topic.blurb) > 70 else topic.blurb + " Full explanation, a ten question check and five auto marked exam-style questions."
    ld = [crumbs_ld(trail), {
        "@context": "https://schema.org",
        "@type": "LearningResource",
        "name": topic.title,
        "description": desc,
        "url": SITE_URL + path,
        "learningResourceType": "Lesson" if course.levels else "Revision guide",
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
                "text": _plain(q.stem),
                "acceptedAnswer": {"@type": "Answer", "text": _plain(q.options[q.answer])},
                "suggestedAnswer": [{"@type": "Answer", "text": _plain(o)}
                                    for i, o in enumerate(q.options) if i != q.answer],
            } for q in topic.quiz[:10]],
        })

    return path, layout(title="%s | %s" % (topic.title, course.seo or course.short),
                        description=desc, path=path, body=body,
                        active="/%s/" % course.slug,
                        topic_id=tid, jsonld=ld,
                        scripts=["/assets/js/quiz.js"], show_progress=True)


def _plain(text: str) -> str:
    """Quiz text for structured data, without the site's own markup.

    The question is authored with `code` and **bold** marks that the page
    renders. A search engine reading the Quiz markup gets the raw string, so
    it would see the backticks. Subscripts and superscripts become the usual
    plain-text d_k and e^2.
    """
    text = re.sub(r"~([0-9A-Za-z]+)~", r"_\1", text)
    text = re.sub(r"\^([0-9A-Za-z+\-/()]+)\^", r"^\1", text)
    return text.replace("`", "").replace("**", "")


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
    noun = "lessons" if course.levels else "topics"
    return """<section class="section" id="%s">
  <div class="section-head">
    <div class="badge-row"><span class="badge">%s</span>%s</div>
    <h2>%s</h2>
    <p>%s</p>
  </div>
  <div class="unit-list">%s</div>
</section>""" % (esc(unit.slug), esc(unit.term or course.short),
                 '<span class="badge">%s %d %s</span>' % (ico("i-list"), len(unit.topics), noun),
                 esc(unit.title), esc(unit.blurb), "".join(rows))


def course_page(course: Course) -> tuple:
    path = "/%s/" % course.slug
    trail = [("Home", "/"), (course.short, None)]
    total_topics = sum(len(u.topics) for u in course.units)
    total_quiz = sum(len(t.quiz) for u in course.units for t in u.topics)
    total_marks = sum(q.marks for u in course.units for t in u.topics for q in t.exam)

    units_html = "".join(unit_block(course, u) for u in course.units)
    first = "/%s/%s/" % (course.slug, course.units[0].topics[0].slug) if course.units and course.units[0].topics else "/"
    if course.levels:
        buttons = ('<a class="btn btn-primary" href="%s">%s Start Level 1</a>\n'
                   '        <a class="btn btn-secondary" href="/tools/">%s Interactive tools</a>'
                   % (first, ico("i-play"), ico("i-tools")))
        stats = ('<div class="stat"><b>%d</b><span>Levels</span></div>\n'
                 '      <div class="stat"><b>%d</b><span>Lessons</span></div>\n'
                 '      <div class="stat"><b>%d</b><span>Quiz questions</span></div>\n'
                 '      <div class="stat"><b>%s</b><span>Your goal</span></div>'
                 % (len(course.units), total_topics, total_quiz, esc(course.goal or "Mastery")))
    else:
        buttons = ('<a class="btn btn-primary" href="%s">%s Start the first topic</a>\n'
                   '        <a class="btn btn-secondary" href="/exam-papers/">%s Practice papers</a>\n'
                   '        <a class="btn btn-ghost" href="/worksheets/">%s Printable worksheets</a>'
                   % (first, ico("i-play"), ico("i-paper"), ico("i-list")))
        stats = ('<div class="stat"><b>%d</b><span>Topics</span></div>\n'
                 '      <div class="stat"><b>%d</b><span>Quiz questions</span></div>\n'
                 '      <div class="stat"><b>%d</b><span>Exam marks</span></div>\n'
                 '      <div class="stat"><b>%s</b><span>Target grade</span></div>'
                 % (total_topics, total_quiz, total_marks, esc(course.goal or "Top")))

    body = """<div class="wrap">%s</div>
<section class="hero"><div class="wrap">
  <div class="hero-grid">
    <div>
      <span class="eyebrow">%s%s</span>
      <h1>%s</h1>
      <p class="lead">%s</p>
      <div class="btn-row" style="margin-top:1.6rem">
        %s%s
      </div>
    </div>
    <div class="stat-row">
      %s
    </div>
  </div>
</div></section>
<div class="wrap course-banner">%s</div>
<div class="wrap">%s</div>""" % (
        crumbs(trail),
        ico("i-target"),
        (" %d levels, zero to hero" % len(course.units) if course.levels else
         esc(" %s %s" % (course.board, course.code)).strip() or " Revision course"),
        esc(course.title), markup.inline(course.blurb),
        buttons,
        ('\n        <a class="btn btn-secondary" href="%s">%s %s</a>'
         % (course.extra_cta[1], ico(course.extra_cta[2]), esc(course.extra_cta[0]))) if course.extra_cta else "",
        stats,
        course_banner(course.slug), units_html)

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
    hub_title = course.title
    if course.board and course.code:
        board = "Edexcel" if course.board == "Pearson Edexcel" else course.board
        hub_title = "%s | %s %s Revision" % (course.title, board, course.code)
    return path, layout(title=hub_title, description=course.blurb, path=path,
                        body=body, active="/%s/" % course.slug,
                        jsonld=ld)


def write(path: str, html_text: str):
    out = os.path.join(DIST, path.strip("/"), "index.html") if path != "/" \
        else os.path.join(DIST, "index.html")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(html_text)
    return out
