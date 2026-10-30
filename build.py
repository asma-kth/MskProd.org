#!/usr/bin/env python3
"""Build the MskProd Computing static site into dist/.

Everything is plain HTML with the content rendered server side, so the site is
fully crawlable and works without JavaScript. Run with: python3 build.py
"""
import hashlib
import json
import os
import re
import shutil
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from mskbuild import render
from mskbuild.render import (SITE_URL, SITE_NAME, DIST, ROOT, layout, crumbs,
                             crumbs_ld, ico, esc, write, logo_svg)
from mskbuild import markup
from mskbuild import placements

TWA_PACKAGE = "org.mskprod.computing"

COURSES = []
PAGES = []          # (path, priority, changefreq)
SEARCH = []         # {t, u, s, k}
MANIFEST = []       # course records for the progress dashboard
PLACED = set()      # placement keys that matched a real topic


def register(path, priority=0.7, freq="monthly"):
    PAGES.append((path, priority, freq))


def add_search(title, url, subtitle, keywords=""):
    SEARCH.append({"t": title, "u": url.lstrip("/"), "s": subtitle, "k": keywords})


# ---------------------------------------------------------------- courses

def build_course(course):
    PLACED.update(placements.apply(course))
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
    MANIFEST.append({
        "slug": course.slug,
        "title": course.short,
        "url": "/%s/" % course.slug,
        "stage": course.stage,
        "topics": [{
            "id": "%s/%s" % (course.slug, t.slug),
            "t": t.title,
            "u": "/%s/%s/" % (course.slug, t.slug),
            "unit": u.title,
            "q": len(t.quiz),
            "e": sum(x.marks for x in t.exam),
            "m": t.minutes,
        } for u in course.units for t in u.topics],
    })
    COURSES.append(course)


# ------------------------------------------------------------------ home

def _pixel_run_band():
    """The home page's way into the game: a picture of it, and two buttons."""
    return """<section class="section">
  <div class="wrap">
    <div class="grid grid-2" style="align-items:center;gap:var(--sp-6)">
      <div>
        <span class="eyebrow">%s Game</span>
        <h2>Pixel Run: learn Python by playing</h2>
        <div class="btn-row" style="margin-top:1.4rem">
          <a class="btn btn-primary" href="/pixel-run/">%s Play Pixel Run</a>
          <a class="btn btn-secondary" href="/python/">%s The Python course</a>
        </div>
      </div>
      <figure class="hero-figure">
        <img src="/assets/img/pixel-run.jpg" width="1200" height="675" loading="lazy" decoding="async"
             alt="Pixel the robot cat jumping onto a green pipe in a grassy platformer level, with a green tick block above the pipe and gold coins ahead.">
      </figure>
    </div>
  </div>
</section>""" % (ico("i-flag"), ico("i-play"), ico("i-python"))


def _adventure_band():
    """The home page's way into the Computational Thinking Adventure."""
    return """<section class="section section-alt">
  <div class="wrap">
    <div class="grid grid-2" style="align-items:center;gap:var(--sp-6)">
      <figure class="hero-figure ct-home-fig">%s</figure>
      <div>
        <span class="eyebrow">%s Game</span>
        <h2>The Computational Thinking Adventure</h2>
        <div class="btn-row" style="margin-top:1.4rem">
          <a class="btn btn-primary" href="/computational-thinking/">%s Start the adventure</a>
          <a class="btn btn-secondary" href="/computational-thinking/teacher/">%s Teacher mode</a>
        </div>
      </div>
    </div>
  </div>
</section>""" % (_adventure_art(), ico("i-map"), ico("i-play"), ico("i-user"))


def _adventure_art():
    """Four islands on a sea, one per world, joined by a dotted route."""
    K = 'stroke="#1E293B" stroke-width="2.4" stroke-linejoin="round" stroke-linecap="round"'
    # A small picture for each world, drawn on a 32 by 32 grid around its centre.
    pics = {
        "puzzle": '<path d="M-12 -12 H-3 C-4 -18 4 -18 3 -12 H12 V-3 C18 -4 18 4 12 3 V12 H-12 Z" fill="#FDBA74" %s/>' % K,
        "telescope": ('<path d="M-13 4 L10 -9 L13 -4 L-10 9 Z" fill="#7DD3FC" %s/>'
                      '<path d="M-1 4 L-7 15 M1 4 L7 15" fill="none" %s/>' % (K, K)),
        "gem": ('<path d="M-12 -5 L-6 -12 H6 L12 -5 L0 12 Z" fill="#C4B5FD" %s/>'
                '<path d="M-12 -5 H12 M-6 -12 L-3 -5 L0 12 L3 -5 L6 -12" fill="none" stroke="#1E293B" stroke-width="1.4"/>' % K),
        "robot": ('<rect x="-11" y="-9" width="22" height="18" rx="5" fill="#CBD5E1" %s/>'
                  '<rect x="-7" y="-5" width="14" height="7" rx="3" fill="#334155"/>'
                  '<circle cx="-3.5" cy="-1.5" r="1.8" fill="#5EEAD4"/><circle cx="3.5" cy="-1.5" r="1.8" fill="#5EEAD4"/>'
                  '<path d="M0 -9 V-14" fill="none" %s/>' % (K, K)),
    }
    isles = [("#EA580C", 70, 150, "puzzle", "Decomposition"), ("#0284C7", 190, 80, "telescope", "Abstraction"),
             ("#9333EA", 310, 150, "gem", "Patterns"), ("#059669", 430, 80, "robot", "Algorithms")]
    out = ['<svg viewBox="0 0 500 230" role="img" aria-label="Four islands, one for each world of the adventure: '
           'Decomposition, Abstraction, Patterns and Algorithms, joined by a dotted route">',
           '<rect width="500" height="230" rx="22" fill="#BAE6FD"/>',
           '<path d="M70 150 Q130 60 190 80 T310 150 T430 80" fill="none" stroke="#0F172A" stroke-width="3" stroke-dasharray="2 9" stroke-linecap="round"/>']
    for c, x, y, pic, name in isles:
        out.append('<ellipse cx="%d" cy="%d" rx="58" ry="26" fill="#FDE68A"/><ellipse cx="%d" cy="%d" rx="44" ry="18" fill="%s"/>'
                   '<g transform="translate(%d %d)">%s</g>' % (x, y + 14, x, y + 8, c, x, y - 6, pics[pic]))
        out.append('<text x="%d" y="%d" font-size="15" font-weight="700" fill="#0F172A" text-anchor="middle" '
                   'font-family="system-ui, sans-serif">%s</text>' % (max(x, 80), y + 64 if y > 100 else y - 40, name))
    out.append("</svg>")
    return "".join(out)


def build_home():
    cards = []
    meta = {
        "ks3": ("Key Stage 3", "/ks3/", "i-layers",
                "Years 7, 8 and 9"),
        "ks4/computer-science": ("GCSE Computer Science", "/ks4/computer-science/", "i-cpu",
                                 "OCR J277"),
        "ks4/aqa-computer-science": ("AQA GCSE Computer Science", "/ks4/aqa-computer-science/", "i-cpu",
                                     "AQA 8525"),
        "ks4/edexcel-computer-science": ("Edexcel GCSE Computer Science", "/ks4/edexcel-computer-science/", "i-cpu",
                                         "Pearson Edexcel 1CP2"),
        "ks4/imedia": ("Creative iMedia", "/ks4/imedia/", "i-palette",
                       "OCR J834"),
        "ks5": ("A Level Computer Science", "/ks5/", "i-brain",
                "OCR H446"),
        "data-analytics": ("Data Analytics", "/data-analytics/", "i-chart",
                           "OCR H019 and H119"),
        "python": ("Python from scratch", "/python/", "i-python",
                   "First program to A Level"),
        "ai": ("Artificial Intelligence: Zero to Hero", "/ai/", "i-sparkle",
               "Fifteen levels"),
    }
    for slug, (title, href, icon, label) in meta.items():
        course = next((c for c in COURSES if c.slug == slug), None)
        if course is None:
            continue
        n_top = sum(len(u.topics) for u in course.units)
        n_q = sum(len(t.quiz) for u in course.units for t in u.topics)
        cards.append(
            '<a class="tile" href="%s">'
            '<span class="tile-icon">%s</span><h3>%s</h3><p>%s</p>'
            '<span class="tile-meta"><span>%d %s</span><span>%d quiz questions</span></span></a>'
            % (href, ico(icon, "icon"), esc(title), esc(label), n_top,
               "lessons" if course.levels else "topics", n_q))

    body = """<section class="hero">
  <div class="wrap hero-grid">
    <div>
      <h1>Computing revision</h1>
      <p class="lead">Key Stage 3, GCSE and A Level, for OCR, AQA and Edexcel.</p>
      <div class="btn-row" style="margin-top:1.8rem">
        <a class="btn btn-primary" href="/ks4/computer-science/">%s Start GCSE Computer Science</a>
        <a class="btn btn-secondary" href="/exam-papers/">%s Exam papers</a>
      </div>
    </div>
    <figure class="hero-figure">
      <img src="/assets/img/teaching.jpg" width="1120" height="625" loading="eager" decoding="async"
           alt="Two teachers at an interactive whiteboard showing a lesson on computing and algorithms, with an algorithm design flowchart and Python code on screen.">
    </figure>
  </div>
</section>

<section class="section">
  <div class="wrap">
    <div class="section-head"><h2>Courses</h2></div>
    <div class="grid grid-3">%s</div>
  </div>
</section>

%s

%s

<section class="section section-alt">
  <div class="wrap">
    <div class="grid grid-2" style="align-items:center;gap:var(--sp-6)">
      <div>
        <span class="eyebrow">%s Who writes this</span>
        <h2>Ms Kethiri</h2>
        <p class="lead">Head of the computing department at a school in London.</p>
      </div>
      <div class="card">
        <h3 style="font-size:var(--step-1)">Teachers</h3>
        <div class="btn-row"><a class="btn btn-primary btn-sm" href="/teachers/">For teachers</a>
        <a class="btn btn-secondary btn-sm" href="/contact/?type=teacher">Request a resource</a></div>
      </div>
    </div>
  </div>
</section>""" % (
        ico("i-play"), ico("i-paper"),
        "".join(cards),
        _adventure_band(),
        _pixel_run_band(),
        ico("i-user"),
    )

    ld = [{
        "@context": "https://schema.org", "@type": "EducationalOrganization",
        "name": SITE_NAME, "url": SITE_URL,
        "description": "Free computing revision for UK students at Key Stage 3, GCSE and A Level.",
        "logo": SITE_URL + "/assets/img/logo.svg",
        "email": render.CONTACT_EMAIL,
        "founder": {"@type": "Person", "name": "Ms Kethiri", "jobTitle": "Head of the computing department"},
    }, {
        "@context": "https://schema.org", "@type": "WebSite",
        "name": SITE_NAME, "url": SITE_URL, "inLanguage": "en-GB",
    }]
    write("/", layout(
        title="GCSE, KS3 and A Level Computing Revision",
        description="Free computing revision for UK students. KS3, OCR GCSE Computer Science J277, Creative iMedia J834, OCR A Level H446 and a full Python course. Explanations, quizzes, auto marked exam questions and practice papers.",
        path="/", body=body, active="/",
        jsonld=ld))
    register("/", 1.0, "weekly")


# --------------------------------------------------------------- offline

def _cat_offline():
    from mskbuild import cat
    return cat.stack("asleep", 230, zzz=True)


def build_pwa():
    """Write the service worker, the offline fallback page and assetlinks.

    The worker has to sit at the site root to control every URL, so it cannot
    live under static/ (which is published at /assets/). Its cache names carry
    a hash of the built shell, so a deploy that changes the CSS or JS lands in
    fresh caches and the stale ones are dropped on activate.
    """
    write("/offline/", layout(
        title="Offline",
        description="You are offline and this page has not been saved to this device yet.",
        path="/offline/", noindex=True,
        body="""<div class="wrap"><div class="empty-screen">
  %s
  <h1>You are offline</h1>
  <div class="btn-row">
    <a class="btn btn-primary" href="/">Go to the home page</a>
  </div>
</div></div>""" % _cat_offline()))


    shell = []
    for rel in ("css/site.css", "js/app.js", "js/mascot.js", "js/tools.js",
                "css/game.css", "js/game.js", "js/game-art.js",
                "css/certificate.css", "js/certificate.js", "css/ct.css", "js/ct.js", "css/ct-pages.css", "js/ct-pages.js",
                "css/stretch.css", "js/stretch.js", "js/quiz.js"):
        f = os.path.join(DIST, "assets", rel)
        if os.path.exists(f):
            with open(f, "rb") as fh:
                shell.append(fh.read())
    build_id = hashlib.sha256(b"".join(shell)).hexdigest()[:12]

    with open(os.path.join(ROOT, "sw.js"), encoding="utf-8") as fh:
        sw = fh.read().replace("__BUILD_ID__", build_id)
    with open(os.path.join(DIST, "sw.js"), "w", encoding="utf-8") as fh:
        fh.write(sw)

    # Digital Asset Links proves to Android that this site and the Play app are
    # the same owner, which is what removes the URL bar from the TWA. It needs
    # the SHA-256 of the signing certificate, which only exists once the app has
    # been uploaded, so the file is written only when that fingerprint is known.
    fp_file = os.path.join(ROOT, "twa", "sha256.txt")
    fingerprints = []
    if os.path.exists(fp_file):
        with open(fp_file, encoding="utf-8") as fh:
            for line in fh:
                line = line.strip().upper()
                if line and not line.startswith("#"):
                    fingerprints.append(line)
    if fingerprints:
        wk = os.path.join(DIST, ".well-known")
        os.makedirs(wk, exist_ok=True)
        links = [{
            "relation": ["delegate_permission/common.handle_all_urls"],
            "target": {"namespace": "android_app",
                       "package_name": TWA_PACKAGE,
                       "sha256_cert_fingerprints": fingerprints},
        }]
        with open(os.path.join(wk, "assetlinks.json"), "w", encoding="utf-8") as fh:
            json.dump(links, fh, indent=2)
        print("Wrote .well-known/assetlinks.json (%d fingerprint(s))" % len(fingerprints))
    else:
        print("No twa/sha256.txt: skipping assetlinks.json "
              "(the Android app will show a URL bar until it exists)")
    print("Service worker build id: %s" % build_id)



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
        "id": "/", "name": SITE_NAME, "short_name": "MskProd",
        "description": "Free UK computing revision for KS3, GCSE and A Level.",
        "start_url": "/", "scope": "/", "display": "standalone",
        "lang": "en-GB", "dir": "ltr", "orientation": "any",
        "categories": ["education"],
        # Matches the frosted header and the top of the page gradient, so the
        # Android status bar and splash screen line up with the site.
        "theme_color": "#FDFAF0", "background_color": "#FBF6E9",
        "icons": [
            {"src": "/assets/img/favicon.svg", "sizes": "any", "type": "image/svg+xml"},
            {"src": "/assets/img/icon-192.png", "sizes": "192x192", "type": "image/png",
             "purpose": "any"},
            {"src": "/assets/img/icon-512.png", "sizes": "512x512", "type": "image/png",
             "purpose": "any"},
            # Android crops launcher icons; this one keeps the logo inside the
            # safe circle so it is not clipped.
            {"src": "/assets/img/icon-maskable-512.png", "sizes": "512x512",
             "type": "image/png", "purpose": "maskable"},
        ],
    }
    with open(os.path.join(DIST, "site.webmanifest"), "w", encoding="utf-8") as fh:
        json.dump(manifest, fh)

    with open(os.path.join(DIST, "search-index.json"), "w", encoding="utf-8") as fh:
        json.dump(SEARCH, fh, separators=(",", ":"))

    # GitHub Pages runs Jekyll unless told not to, and Jekyll drops paths that
    # begin with a dot, which would silently remove /.well-known/assetlinks.json
    # and leave the Android app showing a URL bar.
    with open(os.path.join(DIST, ".nojekyll"), "w", encoding="utf-8") as fh:
        fh.write("")

    with open(os.path.join(DIST, "CNAME"), "w", encoding="utf-8") as fh:
        fh.write("mskprod.org\n")

    # Pages whose address has changed. GitHub Pages cannot issue a real 301, so
    # the 404 page checks this list and forwards, which keeps old links and
    # anything already in a search index working.
    moved = {
        "/python/input-and-selection/": "/python/input-and-operators/",
        "/python/lists-and-strings/": "/python/lists/",
    }
    redirect_js = (
        "<script>(function(){var m=%s;var p=location.pathname;"
        "if(!p.endsWith('/'))p+='/';"
        "if(m[p]){location.replace(m[p]+location.search+location.hash);}})();</script>"
        % json.dumps(moved, separators=(",", ":")))

    # 404
    from mskbuild import cat
    body = """<div class="wrap"><div class="empty-screen">
  %s
  <h1>Page not found</h1>
  <div class="btn-row">
    <a class="btn btn-primary" href="/">Back to the home page</a>
    <a class="btn btn-secondary" href="#" data-search-open>Search the site</a>
  </div>
</div></div>""" % cat.stack("asleep", 260, zzz=True)
    with open(os.path.join(DIST, "404.html"), "w", encoding="utf-8") as fh:
        fh.write(layout(title="Page not found", noindex=True,
                        description="That page could not be found on MskProd Computing.",
                        path="/404.html", body=body, extra_head=redirect_js))


def build_manifest():
    """A list of every course and topic, read by the progress dashboard.

    The dashboard holds no data of its own: it compares this manifest against
    what the browser has saved locally, so nothing about a student ever leaves
    their own machine.
    """
    out = os.path.join(DIST, "assets", "data")
    os.makedirs(out, exist_ok=True)
    with open(os.path.join(out, "progress.json"), "w", encoding="utf-8") as fh:
        json.dump({"courses": MANIFEST}, fh, separators=(",", ":"))



def copy_static():
    src = os.path.join(ROOT, "static")
    dst = os.path.join(DIST, "assets")
    if os.path.exists(dst):
        shutil.rmtree(dst)
    shutil.copytree(src, dst)

    # One bundle for every interactive tool. layout() links it only on pages that
    # mount a tool, so an ordinary topic page downloads none of it.
    from mskbuild import tools as tool_reg
    with open(os.path.join(dst, "js", "tools.js"), "w", encoding="utf-8") as fh:
        fh.write(tool_reg.bundle(ROOT, "js"))
    with open(os.path.join(dst, "css", "tools.css"), "w", encoding="utf-8") as fh:
        fh.write(tool_reg.bundle(ROOT, "css"))

    # The Computational Thinking Adventure ships as one script and one stylesheet.
    from mskbuild import ctbundle
    with open(os.path.join(dst, "js", "ct.js"), "w", encoding="utf-8") as fh:
        fh.write(ctbundle.bundle(ROOT, "js"))
    with open(os.path.join(dst, "css", "ct.css"), "w", encoding="utf-8") as fh:
        fh.write(ctbundle.bundle(ROOT, "css"))
    # The stretch tasks are hosted by the adventure's Pixel, so they share his
    # pose sheet rather than keeping a second copy of it.
    with open(os.path.join(src, "css", "ct", "10-pixel.css"), encoding="utf-8") as fh:
        pixel_css = fh.read()
    stretch_css = os.path.join(dst, "css", "stretch.css")
    with open(stretch_css, encoding="utf-8") as fh:
        rest = fh.read()
    with open(stretch_css, "w", encoding="utf-8") as fh:
        fh.write(pixel_css + "\n" + rest)
    # The parts are in the bundles now, so they are not published one by one.
    shutil.rmtree(os.path.join(dst, "js", "ct"))
    shutil.rmtree(os.path.join(dst, "css", "ct"))

    # The @font-face rules go at the head of the one stylesheet every page
    # already loads, so self hosting the fonts costs no extra request.
    css_dir = os.path.join(dst, "css")
    fonts_css = os.path.join(css_dir, "fonts.css")
    site_css = os.path.join(css_dir, "site.css")
    with open(fonts_css, encoding="utf-8") as fh:
        head = fh.read()
    with open(site_css, encoding="utf-8") as fh:
        rest = fh.read()
    with open(site_css, "w", encoding="utf-8") as fh:
        fh.write(head + "\n" + rest)
    os.remove(fonts_css)

    # The favicon is the same cat, generated from the same source as the logo
    # and the mascot, so a change to the character reaches the browser tab too.
    from mskbuild import cat as _cat
    with open(os.path.join(dst, "img", "favicon.svg"), "w", encoding="utf-8") as fh:
        fh.write(_cat.flat(head_only=True, plate=True, label="MskProd Computing"))



def check_icons():
    """Fail the build on an icon name that is not in the sprite.

    An unknown name renders as <use href="#i-nope">, which draws nothing at
    all and raises no error anywhere, so a typo in a topic's icon is invisible
    until somebody notices a blank square on a card. Cheaper to catch here.
    """
    sprite = os.path.join(ROOT, "static", "img", "icons.svg")
    with open(sprite, encoding="utf-8") as fh:
        have = set(re.findall(r'id="(i-[a-z0-9-]+)"', fh.read()))
    bad = []
    for course in COURSES:
        for name, where in ([(course.icon, course.slug)]
                            + [(u.icon, "%s/%s" % (course.slug, u.slug))
                               for u in course.units]
                            + [(t.icon, "%s/%s" % (course.slug, t.slug))
                               for u in course.units for t in u.topics]):
            if name and name not in have:
                bad.append("%s uses %s" % (where, name))
    if bad:
        raise SystemExit("Unknown icon names (not in static/img/icons.svg):\n  "
                         + "\n  ".join(bad))


def main():
    if os.path.exists(DIST):
        shutil.rmtree(DIST)
    os.makedirs(DIST)

    from content import ks4_cs
    modules = [ks4_cs]
    for name in ("aqa_gcse", "edexcel_gcse", "ks3", "ks4_imedia", "ks5",
                 "data_analytics", "python_course", "ai_course"):
        try:
            mod = __import__("content." + name, fromlist=["COURSE"])
            modules.append(mod)
        except ImportError:
            pass

    # Content is written correct answer first. Reorder every quiz once, here,
    # before anything reads it, so the page, its JSON-LD and the printable
    # worksheet answer keys all see the same arrangement.
    from mskbuild import quizshuffle
    for mod in modules:
        quizshuffle.apply(mod.COURSE)
    _spread, _n = quizshuffle.check([m.COURSE for m in modules])
    print("Quiz answers placed, %d questions: %s" % (_n, _spread))

    # Key Stage 3 units link to their unit exams, so attach those links
    # before any topic page is written.
    from content import papers
    papers.attach_exam_links()
    # Every Key Stage 3 lesson ends with a link to its stretch tasks.
    from content import stretch_page
    stretch_page.attach_links()

    for mod in modules:
        build_course(mod.COURSE)

    try:
        from content import pages
        pages.build(register, add_search, COURSES)
        pages.build_attributions(write, register)
    except ImportError:
        pass

    papers.build(register, add_search)

    from content import tools_page
    tools_page.build(register, add_search)

    from content.pixelrun import page as pixelrun_page
    pixelrun_page.build(register, add_search)

    from content import progress_page
    progress_page.build(register, add_search)

    from content import ai_certificate
    ai_certificate.build(register, add_search)

    from content import ct_page
    ct_page.build(register, add_search)

    stretch_page.build(register, add_search)

    from content import worksheets
    worksheets.build(register, add_search, COURSES)

    from content import assign_page
    assign_page.build(register, add_search)

    from content import contact_page
    contact_page.build(register, add_search)

    placements.check(PLACED)
    check_icons()

    from mskbuild import photos as _photos
    _waiting = _photos.pending()
    if _waiting:
        from mskbuild import illus as _illus
        _illus.load_all()
        _drawn = [w for w in _waiting if "pic-" + w in _illus.REGISTRY]
        _blank = [w for w in _waiting if w not in _drawn]
        print("Photographs pending (%d of %d). %d show a drawing of the object until the "
              "file exists, %d show nothing.\n  drawn: %s\n  blank: %s"
              % (len(_waiting), len(_photos.PHOTOS), len(_drawn), len(_blank),
                 ", ".join(_drawn) or "none", ", ".join(_blank) or "none"))

    build_home()
    copy_static()
    build_pwa()
    build_manifest()
    build_sitemap()

    n_files = sum(len(f) for _, _, f in os.walk(DIST))
    print("Built %d pages, %d files into dist/" % (len(PAGES), n_files))
    print("Search index: %d entries" % len(SEARCH))


if __name__ == "__main__":
    main()
