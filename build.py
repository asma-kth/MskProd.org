#!/usr/bin/env python3
"""Build the MskProd Computing static site into dist/.

Everything is plain HTML with the content rendered server side, so the site is
fully crawlable and works without JavaScript. Run with: python3 build.py
"""
import json
import os
import shutil
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mskbuild import render
from mskbuild.render import (SITE_URL, SITE_NAME, DIST, ROOT, layout, crumbs,
                             crumbs_ld, ico, esc, write, logo_svg)
from mskbuild import markup

COURSES = []
PAGES = []          # (path, priority, changefreq)
SEARCH = []         # {t, u, s, k}


def register(path, priority=0.7, freq="monthly"):
    PAGES.append((path, priority, freq))


def add_search(title, url, subtitle, keywords=""):
    SEARCH.append({"t": title, "u": url.lstrip("/"), "s": subtitle, "k": keywords})


# ---------------------------------------------------------------- courses

def build_course(course):
    path, html = render.course_page(course)
    write(path, html)
    register(path, 0.9, "weekly")
    add_search(course.title, path, "%s %s course overview" % (course.board, course.code),
               course.blurb.lower() + " " + course.stage.lower())

    flat = [(u, t) for u in course.units for t in u.topics]
    for i, (unit, topic) in enumerate(flat):
        prev_link = None
        next_link = None
        if i > 0:
            p = flat[i - 1][1]
            prev_link = (p.title, "/%s/%s/" % (course.slug, p.slug))
        if i < len(flat) - 1:
            n = flat[i + 1][1]
            next_link = (n.title, "/%s/%s/" % (course.slug, n.slug))
        tpath, thtml = render.topic_page(course, unit, topic, prev_link, next_link)
        write(tpath, thtml)
        register(tpath, 0.8, "monthly")
        kws = " ".join([topic.title, topic.blurb, unit.title,
                        " ".join(t for t, _ in topic.keyterms)]).lower()
        add_search(topic.title, tpath,
                   "%s %s" % (course.short, ("spec " + topic.spec) if topic.spec else ""),
                   kws)
    COURSES.append(course)


# ------------------------------------------------------------------ home

def build_home():
    cards = []
    meta = {
        "ks3": ("Key Stage 3", "/ks3/", "i-layers", "var(--lilac-deep)",
                "Years 7, 8 and 9. Build the foundation that makes GCSE feel easy instead of sudden."),
        "ks4/computer-science": ("GCSE Computer Science", "/ks4/computer-science/", "i-cpu", "var(--teal)",
                                 "OCR J277. Every topic on both papers, written as a route to grade 9."),
        "ks4/imedia": ("Creative iMedia", "/ks4/imedia/", "i-palette", "var(--purple)",
                       "OCR J834. The R093 exam unit in full, plus coursework guidance for R094 and R097."),
        "ks5": ("A Level Computer Science", "/ks5/", "i-brain", "var(--deep)",
                "OCR H446. Both components, the NEA, and the depth an A star actually needs."),
        "python": ("Python from scratch", "/python/", "i-python", "var(--aqua)",
                   "First line of code through to object oriented programming, tkinter and pygame."),
    }
    for slug, (title, href, icon, accent, blurb) in meta.items():
        course = next((c for c in COURSES if c.slug == slug), None)
        if course is None:
            continue
        n_top = sum(len(u.topics) for u in course.units)
        n_q = sum(len(t.quiz) for u in course.units for t in u.topics)
        cards.append(
            '<a class="tile" href="%s" style="--tile-accent:%s">'
            '<span class="tile-icon">%s</span><h3>%s</h3><p>%s</p>'
            '<span class="tile-meta"><span>%d topics</span><span>%d quiz questions</span></span></a>'
            % (href, accent, ico(icon, "icon"), esc(title), esc(blurb), n_top, n_q))

    total_topics = sum(len(u.topics) for c in COURSES for u in c.units)
    total_quiz = sum(len(t.quiz) for c in COURSES for u in c.units for t in u.topics)
    total_marks = sum(q.marks for c in COURSES for u in c.units for t in u.topics for q in t.exam)

    body = """<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <span class="eyebrow">%s Free UK computing revision</span>
      <h1>Revise computing properly.<br><span class="gradient-text">Then go and get the top grade.</span></h1>
      <p class="lead">Key Stage 3, GCSE and A Level, written to the OCR specifications. Every topic explained
      in full, then a ten question check and five exam-style questions marked against the real mark scheme.
      No account, no adverts, no tracking. Just the work.</p>
      <div class="btn-row" style="margin-top:1.8rem">
        <a class="btn btn-primary" href="/ks4/computer-science/">%s Start GCSE Computer Science</a>
        <a class="btn btn-secondary" href="/how-to-revise/">%s How to revise properly</a>
      </div>
      <div class="pill-row" style="margin-top:1.6rem">
        <span class="pill">%s OCR J277</span>
        <span class="pill">%s OCR H446</span>
        <span class="pill">%s OCR J834 iMedia</span>
        <span class="pill">%s KS3 Years 7 to 9</span>
      </div>
    </div>
    <div>
      <div class="stat-row" style="grid-template-columns:1fr 1fr">
        <div class="stat"><b>%d</b><span>Topics explained</span></div>
        <div class="stat"><b>%d</b><span>Quiz questions</span></div>
        <div class="stat"><b>%d</b><span>Exam marks to practise</span></div>
        <div class="stat"><b>Free</b><span>No sign up, ever</span></div>
      </div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head">
      <h2>Choose where you are</h2>
      <p>Each course follows the order it is taught in school, so you can revise alongside your lessons or work through the whole thing from the start.</p>
    </div>
    <div class="grid grid-3">%s</div>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap">
    <div class="section-head">
      <h2>How every topic is built</h2>
      <p>The same structure every time, because a revision routine only works when you stop having to decide what to do next.</p>
    </div>
    <div class="grid grid-4">
      <div class="card"><span class="tile-icon" style="--tile-accent:var(--teal)">%s</span>
        <h3 style="font-size:var(--step-1)">Explanation</h3>
        <p style="color:var(--ink-3);font-size:.94rem;margin:0">Written to be understood, not skimmed. Every idea is explained with the reason behind it, because the reason is where the marks are.</p></div>
      <div class="card"><span class="tile-icon" style="--tile-accent:var(--purple)">%s</span>
        <h3 style="font-size:var(--step-1)">Key terms and flashcards</h3>
        <p style="color:var(--ink-3);font-size:.94rem;margin:0">Exam ready definitions, plus flip cards so you can practise recalling them rather than rereading them.</p></div>
      <div class="card"><span class="tile-icon" style="--tile-accent:var(--aqua)">%s</span>
        <h3 style="font-size:var(--step-1)">Ten question check</h3>
        <p style="color:var(--ink-3);font-size:.94rem;margin:0">Instant feedback on every answer, right or wrong, explaining why. Anything under ten out of ten means go back.</p></div>
      <div class="card"><span class="tile-icon" style="--tile-accent:var(--deep)">%s</span>
        <h3 style="font-size:var(--step-1)">Auto marked exam questions</h3>
        <p style="color:var(--ink-3);font-size:.94rem;margin:0">Write a full answer and the marker checks it against the mark scheme point by point, then shows you a model answer.</p></div>
    </div>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="grid grid-2" style="align-items:center;gap:var(--sp-6)">
      <div>
        <h2>Practice papers you can actually sit</h2>
        <p class="lead">Full length original papers written to match the real format exactly, with complete
        mark schemes and a built in timer. Sit one properly, mark it honestly, and you will learn more in
        ninety minutes than in a week of rereading notes.</p>
        <div class="btn-row" style="margin-top:1.4rem">
          <a class="btn btn-primary" href="/exam-papers/">%s Go to exam papers</a>
        </div>
      </div>
      <div class="card">
        <h3 style="font-size:var(--step-1)">Why original papers</h3>
        <p style="color:var(--ink-3);font-size:.95rem">Real past papers belong to the exam boards and cannot be
        republished here. Every paper on this site is written from scratch to the same structure, question
        style, command words and mark allocation as the real thing, and each comes with a full mark scheme.
        Links to the official past papers on the exam board's own site are provided alongside them.</p>
      </div>
    </div>
  </div>
</section>

<section class="section section-alt">
  <div class="wrap">
    <div class="grid grid-2" style="align-items:center;gap:var(--sp-6)">
      <div class="center">%s</div>
      <div>
        <span class="eyebrow">%s Meet Pixel</span>
        <h2>You are not doing this alone</h2>
        <p class="lead">Pixel is the small robot cat in the corner of every page. Tap for a fun fact, a
        revision tip that is actually backed by evidence, or a reminder that finding this hard is normal and
        not a sign that you cannot do it.</p>
        <p class="muted" style="font-size:.9rem">Pixel runs entirely on your own device. Nothing you do on this site is sent anywhere.</p>
      </div>
    </div>
  </div>
</section>""" % (
        ico("i-sparkle"), ico("i-play"), ico("i-bulb"),
        ico("i-cpu"), ico("i-brain"), ico("i-palette"), ico("i-layers"),
        total_topics, total_quiz, total_marks,
        "".join(cards),
        ico("i-book"), ico("i-list"), ico("i-check-circle"), ico("i-paper"),
        ico("i-arrow-right"),
        render.mascot_svg().replace('<svg ', '<svg style="max-width:260px;margin:0 auto" ', 1),
        ico("i-sparkle"),
    )

    ld = [{
        "@context": "https://schema.org", "@type": "EducationalOrganization",
        "name": SITE_NAME, "url": SITE_URL,
        "description": "Free computing revision for UK students at Key Stage 3, GCSE and A Level.",
        "logo": SITE_URL + "/assets/img/logo.svg",
    }, {
        "@context": "https://schema.org", "@type": "WebSite",
        "name": SITE_NAME, "url": SITE_URL, "inLanguage": "en-GB",
        "potentialAction": {"@type": "SearchAction",
                            "target": {"@type": "EntryPoint", "urlTemplate": SITE_URL + "/search/?q={search_term_string}"},
                            "query-input": "required name=search_term_string"},
    }]
    write("/", layout(
        title="MskProd Computing | UK computing revision for KS3, GCSE and A Level",
        description="Free computing revision for UK students. KS3, OCR GCSE Computer Science J277, Creative iMedia J834, OCR A Level H446 and a full Python course. Explanations, quizzes, auto marked exam questions and practice papers.",
        path="/", body=body, active="/",
        greeting="Hello. I am Pixel. Pick your key stage below, and tap me any time for a fun fact or a revision tip.",
        jsonld=ld))
    register("/", 1.0, "weekly")


# -------------------------------------------------------------- site meta

def build_sitemap():
    today = date.today().isoformat()
    urls = "".join(
        "<url><loc>%s%s</loc><lastmod>%s</lastmod><changefreq>%s</changefreq><priority>%.1f</priority></url>"
        % (SITE_URL, p, today, f, pr) for p, pr, f in sorted(set(PAGES)))
    xml = ('<?xml version="1.0" encoding="UTF-8"?>'
           '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">%s</urlset>' % urls)
    with open(os.path.join(DIST, "sitemap.xml"), "w", encoding="utf-8") as fh:
        fh.write(xml)

    with open(os.path.join(DIST, "robots.txt"), "w", encoding="utf-8") as fh:
        fh.write("User-agent: *\nAllow: /\n\nSitemap: %s/sitemap.xml\n" % SITE_URL)

    manifest = {
        "name": SITE_NAME, "short_name": "MskProd",
        "description": "Free UK computing revision for KS3, GCSE and A Level.",
        "start_url": "/", "display": "standalone",
        "background_color": "#FBFAFC", "theme_color": "#03969D",
        "icons": [{"src": "/assets/img/favicon.svg", "sizes": "any", "type": "image/svg+xml"}],
    }
    with open(os.path.join(DIST, "site.webmanifest"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh)

    with open(os.path.join(DIST, "search-index.json"), "w", encoding="utf-8") as fh:
        json.dump(SEARCH, fh, separators=(",", ":"))

    with open(os.path.join(DIST, "CNAME"), "w", encoding="utf-8") as fh:
        fh.write("mskprod.org\n")

    # 404
    body = """<div class="wrap" style="padding:var(--sp-8) 0;text-align:center;max-width:640px">
  <div style="max-width:180px;margin:0 auto var(--sp-4)">%s</div>
  <h1>That page does not exist</h1>
  <p class="lead" style="margin-inline:auto">Pixel has checked twice. The link may be old, or there may be a typo in the address.</p>
  <div class="btn-row" style="justify-content:center;margin-top:var(--sp-4)">
    <a class="btn btn-primary" href="/">Back to the home page</a>
    <a class="btn btn-secondary" href="#" data-search-open>Search the site</a>
  </div>
</div>""" % render.mascot_svg()
    with open(os.path.join(DIST, "404.html"), "w", encoding="utf-8") as fh:
        fh.write(layout(title="Page not found", description="That page could not be found on MskProd Computing.",
                        path="/404.html", body=body))


def copy_static():
    src = os.path.join(ROOT, "static")
    dst = os.path.join(DIST, "assets")
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)


def main():
    if os.path.exists(DIST):
        shutil.rmtree(DIST)
    os.makedirs(DIST)

    from content import ks4_cs
    modules = [ks4_cs]
    for name in ("ks3", "ks4_imedia", "ks5", "python_course"):
        try:
            mod = __import__("content." + name, fromlist=["COURSE"])
            modules.append(mod)
        except ImportError:
            pass

    for mod in modules:
        build_course(mod.COURSE)

    try:
        from content import pages
        pages.build(register, add_search, COURSES)
    except ImportError:
        pass

    try:
        from content import papers
        papers.build(register, add_search)
    except ImportError:
        pass

    build_home()
    copy_static()
    build_sitemap()

    n_files = sum(len(f) for _, _, f in os.walk(DIST))
    print("Built %d pages, %d files into dist/" % (len(PAGES), n_files))
    print("Search index: %d entries" % len(SEARCH))


if __name__ == "__main__":
    main()
