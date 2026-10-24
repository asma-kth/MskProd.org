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
    print("Computational Thinking Adventure: %d levels checked, page written to %s" % (n, PATH))
