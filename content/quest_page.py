"""The Media Realms: the R093 adventure page.

Everything a search engine or a reader without scripts needs (the four realms,
the eleven places and what each one teaches) is ordinary HTML inside #mq-app,
and quest.js replaces it with the playable adventure.
"""
import json

from mskbuild import cat
from mskbuild.render import layout, crumbs, crumbs_ld, esc, write, SITE_NAME, SITE_URL
from content import imedia_quest as Q
from content.imedia_quest import world as W

PATH = "/ks4/imedia/quest/"
TITLE = "The Media Realms: an R093 adventure"
LEAD = ("A fantasy adventure through Creative iMedia R093, topic by topic. Answer questions to cast spells, "
        "clear the muddles with your pet, and master every R093 lesson on the way to the Studio Spire.")


def _outline(data):
    out = ['<div class="mq-static-page mq-outline">',
           '<h1>%s</h1>' % esc(TITLE),
           '<p class="lead">%s</p>' % esc(LEAD),
           '<noscript><p>The adventure needs JavaScript switched on. Here is what it covers.</p></noscript>']
    for r in data["realms"]:
        out.append('<h2>%s %s</h2><p>%s</p><ol>' % (esc(r["ta"]), esc(r["name"]), esc(r["about"])))
        for p in data["places"]:
            if p["realm"] == r["id"]:
                names = ", ".join(esc(m["name"]) for m in p["monsters"])
                out.append('<li><b>%s</b>: <a href="%s">%s</a>. Muddles to clear: %s.</li>' % (
                    esc(p["name"]), p["url"], esc(p["topic"]), names))
        out.append('</ol>')
    out.append('<h2>The Studio Spire</h2><p>%s</p>' % esc(" ".join(data["final"]["intro"])))
    out.append('</div>')
    return "".join(out)


def attach_links():
    """Before the topic pages are built: each R093 topic links to its place in
    the adventure, the Creative iMedia course page gets a button, and the
    footer lists the game."""
    from mskbuild import render
    from content import ks4_imedia
    unit = next(u for u in ks4_imedia.COURSE.units if u.slug == "r093")
    for t in unit.topics:
        t.quest = "%s#/place/%s" % (PATH, t.slug)
    ks4_imedia.COURSE.quest_cta = ("The R093 adventure", PATH, "i-map")
    link = ("The Media Realms, the R093 game", PATH)
    if link not in render.PRACTISE_LINKS:
        render.PRACTISE_LINKS.append(link)


def build(register, add_search):
    data = Q.payload()
    n = Q.validate(data)
    for p in data["places"]:
        p.pop("dropped", None)
    trail = [("Home", "/"), ("Creative iMedia", "/ks4/imedia/"), ("The Media Realms", None)]
    blob = json.dumps(data, separators=(",", ":"), ensure_ascii=False).replace("</", "<\\/")
    body = """<div class="wrap mq-shell">
  %s
  <div id="mq-app" class="mq" data-motion="calm">
    %s
  </div>
</div>
<template id="mq-pixel">%s</template>
<script type="application/json" id="mq-data">%s</script>""" % (crumbs(trail), _outline(data), cat.rig(), blob)
    ld = [crumbs_ld(trail), {
        "@context": "https://schema.org", "@type": "LearningResource",
        "name": TITLE, "description": LEAD, "url": SITE_URL + PATH, "inLanguage": "en-GB",
        "isAccessibleForFree": True, "learningResourceType": "Educational game",
        "educationalLevel": "GCSE, Cambridge National Level 1/2",
        "teaches": "OCR Creative iMedia R093: the media industry, product design, pre production planning and distribution",
        "provider": {"@type": "Organization", "name": SITE_NAME, "url": SITE_URL},
    }]
    write(PATH, layout(title=TITLE, description=LEAD, path=PATH, body=body, active="/ks4/imedia/",
                       extra_head='<link rel="stylesheet" href="/assets/css/quest.css">',
                       scripts=["/assets/js/quest.js"], jsonld=ld))
    register(PATH, 0.8, "monthly")
    add_search("The Media Realms", PATH, "Creative iMedia R093 adventure game, topic by topic",
               "media realms adventure game rpg wizard pet battle spells creative imedia r093 j834 revision "
               "sectors job roles client brief audience research style planning documents work plan "
               "legislation copyright file formats distribution")
    print("The Media Realms: %d places, %d questions checked" % (len(data["places"]), n))
