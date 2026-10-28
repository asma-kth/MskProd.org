"""The Computational Thinking Adventure: the game page, teacher mode and certificates.

The game is one page. Everything a search engine or a screen reader without
scripts needs (the four worlds and their forty levels) is ordinary HTML inside
#ct-app, and the script replaces it with the playable adventure.
"""
import json

from mskbuild import cat
from mskbuild.render import layout, crumbs, crumbs_ld, esc, write, SITE_NAME, SITE_URL
from content import ct_adventure as A

PATH = "/computational-thinking/"
TITLE = "Computational Thinking Adventure"
LEAD = ("Think like a computer scientist: four worlds and forty playable levels of decomposition, "
        "abstraction, pattern recognition and algorithms, with Pixel the robot cat.")


def _outline():
    out = ['<div class="ct-static">',
           '<h1>Computational Thinking Adventure</h1>',
           '<p class="lead">Think Like a Computer Scientist. Play. Solve. Level Up!</p>']
    lv = A.levels()
    for w in A.WORLDS:
        out.append('<h2>World %d: %s. %s</h2><p>%s</p><ol>' % (w["n"], esc(w["name"]), esc(w["tag"]), esc(w["about"])))
        for l in lv:
            if l["world"] == w["id"]:
                out.append('<li><b>%s</b> (%s): %s</li>' % (esc(l["title"]), l["band"], esc(l["objective"])))
        out.append('</ol>')
    out.append('</div>')
    return "".join(out)


def build(register, add_search):
    n = A.validate()
    trail = [("Home", "/"), ("Computational Thinking Adventure", None)]
    data = json.dumps(A.payload(), separators=(",", ":"), ensure_ascii=False).replace("</", "<\\/")
    body = """<div class="wrap ct-shell">
  %s
  <div id="ct-app" class="ct" data-motion="calm">
    <noscript><p class="ct-noscript">The adventure's games need JavaScript switched on. Here is what is inside.</p></noscript>
    %s
  </div>
</div>
<template id="ct-pixel">%s</template>
<script type="application/json" id="ct-data">%s</script>""" % (crumbs(trail), _outline(), cat.rig(), data)
    ld = [crumbs_ld(trail), {
        "@context": "https://schema.org", "@type": "LearningResource",
        "name": TITLE, "description": LEAD, "url": SITE_URL + PATH, "inLanguage": "en-GB",
        "isAccessibleForFree": True, "learningResourceType": "Educational game",
        "educationalLevel": "Key Stage 3 and GCSE",
        "teaches": "Computational thinking: decomposition, abstraction, pattern recognition and algorithms",
        "provider": {"@type": "Organization", "name": SITE_NAME, "url": SITE_URL},
    }]
    write(PATH, layout(title=TITLE, description=LEAD, path=PATH, body=body, active=PATH,
                       extra_head='<link rel="stylesheet" href="/assets/css/ct.css">',
                       scripts=["/assets/js/ct.js"], jsonld=ld))
    register(PATH, 0.9, "weekly")
    add_search(TITLE, PATH, "Forty game levels: decomposition, abstraction, patterns and algorithms",
               "computational thinking adventure game decomposition abstraction pattern recognition algorithms "
               "flowchart pseudocode puzzles levels pixel ks3 gcse j277")
    build_teacher(register, add_search)
    build_certificate(register, add_search)
    print("Computational Thinking Adventure: %d levels checked; game, teacher mode and certificate pages written" % n)


# ================================================================ teacher mode
ACTIVITY = {
    "group": "Drag-and-drop sorting", "order": "Put the steps in order", "tree": "Build a structure diagram",
    "assembly": "Production-line simulation", "maze": "Plan a route, then steer through a maze",
    "select": "Keep or remove details", "identify": "Choose the details or sensors that tell things apart",
    "graph": "Find the quickest route on a graph", "fields": "Choose data columns, then make decisions",
    "model": "Design a product for a user", "datamaze": "Filter a database to unlock doors",
    "quest": "Multi-stage challenge", "sequence": "Pattern gaps, predictions and bug hunts",
    "dance": "Program a dance and write it as a loop", "snakepat": "Snake game: keep the pattern going",
    "codepat": "Replace repeated code with a loop", "program": "Program a robot on a grid",
    "flowbuild": "Build and run a flowchart", "flowfix": "Test, find and fix a flowchart bug",
    "botcode": "One pseudocode algorithm for several boards", "trace": "Complete a trace table",
}
TEACHER_PATH = PATH + "teacher/"
TEACHER_LEAD = ("Every level of the adventure, with its objective, difficulty, activity, curriculum links and answers. "
                "Preview any level as a student sees it without saving anything. "
                "Progress is kept only in each student's own browser, so nothing is collected.")

GUIDE_ROWS = [
    ("Store a value", "score = 0"), ("Output", 'print("Hello")'), ("Input", 'name = input("Name? ")'),
    ("Text to a number", 'age = int(input("Age? "))'), ("Number to text", 'print("You are " + str(age))'),
    ("Selection", 'if x > 5 then\n    print("big")\nelseif x == 5 then\n    print("five")\nelse\n    print("small")\nendif'),
    ("Count-controlled loop", "for i = 1 to 10 step 2\n    print(i)\nnext i"),
    ("Condition-controlled loop", "while x < 100\n    x = x * 2\nendwhile"),
    ("Loop that runs at least once", "do\n    x = x - 1\nuntil x == 0"),
    ("Comparison", "==  !=  <  <=  >  >="), ("Arithmetic", "+  -  *  /  ^  MOD  DIV"), ("Boolean", "AND  OR  NOT"),
    ("Arrays", 'array names[3]\nnames[0] = "Ada"'),
    ("Strings", "s.length  s.upper  s.lower  s.substring(start, length)  s.left(n)  s.right(n)"),
]


def _guide_html():
    rows = "".join('<tr><th scope="row">%s</th><td><pre><code>%s</code></pre></td></tr>' % (esc(a), esc(b)) for a, b in GUIDE_ROWS)
    return ('<section class="ctt-sec" id="pseudocode"><h2>The pseudocode convention</h2>'
            '<div class="table-scroll"><table class="ctt-guide">%s</table></div></section>' % rows)


def _level_card(lv, preview_base):
    cur = "".join("<li>%s</li>" % esc(c) for c in lv.get("curriculum", [])) or "<li>Enrichment</li>"
    hints = "".join("<li>%s</li>" % esc(h) for h in lv["hints"])
    return """<article class="ctt-level" id="%s">
  <header><span class="ctt-n">%s</span><h3>%s</h3><span class="ctt-band ctt-band-%s">%s</span></header>
  <p class="ctt-act"><b>Activity:</b> %s</p>
  <p><b>Objective:</b> %s</p>
  <p><b>Student task:</b> %s</p>
  <details><summary>What students read first</summary><p>%s</p></details>
  <details><summary>Pixel's three hints</summary><ol>%s</ol></details>
  <details><summary>Answer</summary><p>%s</p></details>
  <ul class="ctt-cur">%s</ul>
  <p class="ctt-actions"><a class="btn btn-secondary" href="%s#/play/%s?preview">Preview this level</a></p>
</article>""" % (lv["id"], lv["n"], esc(lv["title"]), esc(lv["band"]).lower(), esc(lv["band"]), esc(ACTIVITY.get(lv["engine"], lv["engine"])),
                 esc(lv["objective"]), esc(lv["task"]), esc(lv["learn"]), hints, esc(lv["solution"]), cur, preview_base, lv["id"])


def build_teacher(register, add_search):
    trail = [("Home", "/"), ("Computational Thinking Adventure", PATH), ("Teacher mode", None)]
    lv = A.levels()
    sections = []
    for w in A.WORLDS:
        cards = "".join(_level_card(l, PATH) for l in lv if l["world"] == w["id"])
        sections.append('<section class="ctt-sec ctt-world" style="--w:%s;--wd:%s;--wl:%s" id="%s"><h2>World %d: %s</h2>'
                        '<p class="ctt-tag">%s %s</p><div class="ctt-grid">%s</div></section>' % (
                            w["colour"], w["deep"], w["light"], w["id"], w["n"], esc(w["name"]), esc(w["tag"]), esc(w["about"]), cards))
    bonus = "".join('<li><b>%s</b> (%s, unlocked by chest %d): %s <a href="%s#/bonus/%d?preview">Preview</a></li>' % (
        esc(b["title"]), esc(ACTIVITY.get(b["engine"], b["engine"])), b["n"], esc(b["objective"]), PATH, b["n"]) for b in A.bonus_levels())
    badges = "".join("<li><b>%s</b>: %s</li>" % (esc(b["name"]), esc(b["desc"])) for b in A.BADGES)
    toc = "".join('<li><a href="#%s">World %d: %s</a></li>' % (w["id"], w["n"], esc(w["name"])) for w in A.WORLDS)
    body = """<div class="wrap ctt">
  %s
  <header class="page-head">
    <h1>Teacher mode</h1>
  </header>
  <section class="ctt-sec ctt-how">
    <nav class="ctt-toc" aria-label="Worlds"><ol>%s<li><a href="#bonus">Bonus puzzles</a></li><li><a href="#pseudocode">Pseudocode convention</a></li><li><a href="#reset">Reset a device</a></li></ol></nav>
  </section>
  %s
  <section class="ctt-sec" id="bonus"><h2>Bonus puzzles</h2><ul>%s</ul></section>
  <section class="ctt-sec"><h2>Labs</h2><ul><li><a href="%s#/lab/pseudocode">Pseudocode Playground</a></li><li><a href="%s#/lab/flowchart">Flowchart Lab</a></li></ul></section>
  <section class="ctt-sec"><h2>Badges</h2><ul>%s</ul></section>
  %s
  <section class="ctt-sec" id="reset"><h2>Reset a shared device</h2>
    <p><button type="button" class="btn btn-secondary" id="ct-reset">Reset the adventure on this device</button> <span id="ct-reset-msg" role="status"></span></p>
  </section>
</div>""" % (crumbs(trail), toc, "".join(sections), bonus, PATH, PATH, badges, _guide_html())
    write(TEACHER_PATH, layout(title="Computational Thinking Adventure: teacher mode", description=TEACHER_LEAD, path=TEACHER_PATH, body=body,
                               active=PATH, extra_head='<link rel="stylesheet" href="/assets/css/ct-pages.css">',
                               scripts=["/assets/js/ct-pages.js"], jsonld=[crumbs_ld(trail)]))
    register(TEACHER_PATH, 0.6, "monthly")
    add_search("Computational Thinking Adventure: teacher mode", TEACHER_PATH, "All 40 levels with objectives, answers and previews",
               "teacher computational thinking adventure answers solutions objectives curriculum preview reset pseudocode convention")


# ================================================================ certificates
CERT_PATH = PATH + "certificate/"
CERT_LEAD = ("Finish every level in a world to unlock its certificate, or all forty to become a Computational Thinking Champion. "
             "Add your name and print it, or save it as a PDF. Progress is read from this browser, so use the device you played on.")


def _cert_svg():
    W, H = 1123, 794
    cat_svg = cat.flat(label="Pixel the robot cat", cls="ctc-cat").replace("<svg ", '<svg x="860" y="520" width="190" height="190" ', 1)
    stars = "".join('<path transform="translate(%d %d) scale(1.1)" d="M0 -12 L3.5 -4 L12 -3.7 L5.5 2 L7.4 10.5 L0 6 L-7.4 10.5 L-5.5 2 L-12 -3.7 L-3.5 -4 Z" class="ctc-star"/>' % (x, 112)
                    for x in (470, 511, 552, 593, 634))
    return """<svg id="ctc-cert" class="ctc-cert" viewBox="0 0 %d %d" role="img" aria-labelledby="ctc-cert-t">
  <title id="ctc-cert-t">Your Computational Thinking Adventure certificate</title>
  <rect width="%d" height="%d" class="ctc-bg"/>
  <rect x="22" y="22" width="%d" height="%d" rx="26" class="ctc-frame"/>
  <rect x="40" y="40" width="%d" height="%d" rx="18" class="ctc-frame2"/>
  <path d="M40 160 Q 300 90 561 150 T 1083 120 V 40 H 40 Z" class="ctc-wave"/>
  %s
  <text x="561" y="200" text-anchor="middle" class="ctc-kicker">MSKPROD COMPUTING · COMPUTATIONAL THINKING ADVENTURE</text>
  <text x="561" y="262" text-anchor="middle" class="ctc-title">Certificate of Achievement</text>
  <text x="561" y="318" text-anchor="middle" class="ctc-small">This certifies that</text>
  <text x="561" y="392" text-anchor="middle" class="ctc-name" id="ctc-name">Your name</text>
  <line x1="300" y1="414" x2="822" y2="414" class="ctc-line"/>
  <text x="561" y="462" text-anchor="middle" class="ctc-small" id="ctc-has">has completed every level of</text>
  <text x="561" y="516" text-anchor="middle" class="ctc-world" id="ctc-world">World</text>
  <text x="561" y="556" text-anchor="middle" class="ctc-small" id="ctc-tag"></text>
  <text x="561" y="604" text-anchor="middle" class="ctc-stars" id="ctc-stars"></text>
  %s
  <path d="M112 640 L92 712 L122 698 L140 724 L152 652 Z M188 640 L208 712 L178 698 L160 724 L148 652 Z" class="ctc-ribbon"/>
  <circle cx="150" cy="590" r="66" class="ctc-medal"/><circle cx="150" cy="590" r="51" class="ctc-medal2"/>
  <text x="150" y="606" text-anchor="middle" class="ctc-medal-t" id="ctc-medal-t">1</text>
  <text x="420" y="690" text-anchor="middle" class="ctc-sig">Pixel</text>
  <line x1="320" y1="702" x2="520" y2="702" class="ctc-line2"/>
  <text x="420" y="724" text-anchor="middle" class="ctc-tiny">Pixel the robot cat, Chief Computational Thinker</text>
  <text x="680" y="690" text-anchor="middle" class="ctc-date" id="ctc-date"></text>
  <line x1="590" y1="702" x2="770" y2="702" class="ctc-line2"/>
  <text x="680" y="724" text-anchor="middle" class="ctc-tiny">Date</text>
</svg>""" % (W, H, W, H, W - 44, H - 44, W - 80, H - 80, stars, cat_svg)


def build_certificate(register, add_search):
    trail = [("Home", "/"), ("Computational Thinking Adventure", PATH), ("Certificate", None)]
    data = dict(worlds=[dict(id=w["id"], n=w["n"], name=w["name"], tag=w["tag"], place=w["place"], colour=w["colour"],
                             deep=w["deep"], light=w["light"], levels=["%s-%d" % (w["id"], i) for i in range(1, len(w["levels"]) + 1)])
                        for w in A.WORLDS])
    body = """<div class="wrap ctc">
  %s
  <header class="page-head"><h1>Your certificate</h1></header>
  <div id="ctc-app">
    <div class="ctc-tabs" id="ctc-tabs" role="group" aria-label="Choose a certificate"></div>
    <p class="ctc-status" id="ctc-status" role="status"></p>
    <div class="ctc-form" id="ctc-form" hidden>
      <label for="ctc-name-in">Name on the certificate</label>
      <input id="ctc-name-in" type="text" maxlength="40" autocomplete="off" placeholder="Type your name">
      <button type="button" class="btn btn-primary" id="ctc-print">Print or save as PDF</button>
    </div>
    <div class="ctc-paper" id="ctc-paper">%s</div>
  </div>
</div>
<script type="application/json" id="ctc-data">%s</script>""" % (crumbs(trail), _cert_svg(),
                                                                json.dumps(data, separators=(",", ":")).replace("</", "<\\/"))
    write(CERT_PATH, layout(title="Computational Thinking Adventure certificate", description=CERT_LEAD, path=CERT_PATH, body=body,
                            active=PATH, extra_head='<link rel="stylesheet" href="/assets/css/ct-pages.css">',
                            scripts=["/assets/js/ct-pages.js"], jsonld=[crumbs_ld(trail)]))
    register(CERT_PATH, 0.4, "monthly")
    add_search("Your Computational Thinking Adventure certificate", CERT_PATH, "Print a certificate for each world",
               "certificate computational thinking adventure print champion world award")
