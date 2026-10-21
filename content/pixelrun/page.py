"""The Pixel Run page: the game, and the table of its ten levels.

The levels table is ordinary HTML, for search engines and screen readers. The
game itself is built by static/js/game.js from the JSON that this module embeds.
"""
import json
import re

from mskbuild import cat, markup
from mskbuild.render import SITE_NAME, SITE_URL, crumbs, crumbs_ld, esc, ico, layout, write

from . import BANK, LEVELS, fallback, test_records, validate_all
from .harness import HARNESS

PATH = "/pixel-run/"
TITLE = "Pixel Run: Learn Python by Playing a Platformer"
LEAD = ("Pixel the robot cat runs through ten levels, and every obstacle is a Python function for you "
        "to write. Pass the tests and she jumps on. Fail three times and you are sent back a level.")
DESCRIPTION = ("Play Pixel Run, a free Python platformer. Write a function to clear each obstacle, "
               "from print and loops to recursion and graphs. Ten levels, GCSE to A Level.")


def _sprite():
    """Pixel as one SVG, without the contact shadow, which would not follow a jump."""
    svg = cat.flat(label="Pixel")
    svg, n = re.subn(r'<ellipse cx="50" cy="88"[^>]*/>', "", svg, count=1)
    assert n == 1, "the shadow ellipse moved: update the sprite filter"
    return svg.replace("<svg ", '<svg width="256" height="256" ', 1)


def _rendered(text):
    """Challenge text goes through the same inline markup as the rest of the site."""
    out = markup.inline(text)
    # The inline markup turns *x* into italics and ~x~ into subscripts. Nothing
    # in the bank means to use either, so one appearing means a stray symbol.
    for tag in ("<em>", "<sub>", "<sup>"):
        assert tag not in out, "unintended %s in challenge text: %r" % (tag, text)
    return out


def data():
    levels = [{
        "n": lv.n, "name": lv.name, "concept": lv.concept, "stage": lv.stage,
        "blurb": lv.blurb, "palette": lv.palette, "obstacles": lv.obstacles,
        "revise": [list(r) for r in lv.revise],
    } for lv in LEVELS]
    challenges = []
    for k, c in enumerate(BANK):
        challenges.append({
            "id": c.id, "level": c.level, "title": c.title, "fn": c.fn,
            "story": _rendered(c.story), "task": _rendered(c.task),
            "hints": [_rendered(h) for h in c.hints],
            "starter": c.starter, "solution": c.solution,
            "rules": c.rules, "tests": test_records(c),
            "fb": fallback(c, k),
        })
    return {"levels": levels, "challenges": challenges, "harness": HARNESS, "sprite": _sprite()}


# ------------------------------------------------------------------ prose

def _level_table():
    rows = ["| Level | Name | The idea | Revise first |"]
    for lv in LEVELS:
        links = ", ".join("[%s](%s)" % (label, url) for label, url in lv.revise)
        rows.append("| %d | **%s** | %s | %s |" % (lv.n, lv.name, lv.concept, links))
    return "\n".join(rows)


def _prose():
    return """
## The ten levels

%s
""" % _level_table()


def _app_ld():
    return {
        "@context": "https://schema.org", "@type": "WebApplication",
        "name": "Pixel Run", "url": SITE_URL + PATH,
        "description": DESCRIPTION,
        "applicationCategory": "EducationalApplication",
        "operatingSystem": "Any, in a web browser",
        "isAccessibleForFree": True,
        "inLanguage": "en-GB",
        "teaches": "Python programming for GCSE and A Level Computer Science",
        "audience": {"@type": "EducationalAudience", "educationalRole": "student"},
        "offers": {"@type": "Offer", "price": "0", "priceCurrency": "GBP"},
        "provider": {"@type": "Organization", "name": SITE_NAME, "url": SITE_URL},
    }


def _shell():
    return """<section class="pr" id="pixelrun" aria-labelledby="pr-title" data-ready="no">
  <h2 id="pr-title" class="sr-only">The game</h2>
  <div class="pr-hud" role="group" aria-label="Game status">
    <span class="pr-chip" id="pr-level">Level 1 of 10</span>
    <span class="pr-name" id="pr-name">Print Plains</span>
    <span class="pr-pips" id="pr-pips" role="img" aria-label="Obstacles cleared: 0 of 3"><i></i><i></i><i></i></span>
    <span class="pr-chip pr-stars" id="pr-stars" title="Stars earned this run">%s <b>0</b></span>
    <span class="pr-chip pr-coins" id="pr-coins" title="Coins collected this run"><i aria-hidden="true"></i> <b>0</b></span>
    <span class="pr-chip pr-py" id="pr-py" role="status">Python: waiting</span>
  </div>
  <div class="pr-stagecol">
    <div class="pr-stage">
      <canvas id="pr-canvas" width="640" height="360" role="img"
              aria-label="Pixel the robot cat runs along a side scrolling level. A description of what is happening is read out below the picture."></canvas>
    </div>
    <p class="pr-foot"><button class="tool-btn" type="button" id="pr-calm" aria-pressed="false">Calm mode</button>
      <span>Calm mode stops the scrolling and the jumps.</span></p>
  </div>
  <div class="pr-console" id="pr-console" tabindex="-1">
    <noscript><p>Pixel Run needs JavaScript, because the game and the Python it uses both run in your browser.</p></noscript>
    <p class="pr-boot">Loading the game.</p>
  </div>
  <p class="sr-only" id="pr-live" role="status" aria-live="polite"></p>
</section>""" % ico("i-star", "icon")


def build(register, add_search):
    n = validate_all()
    trail = [("Home", "/"), ("Python", "/python/"), ("Pixel Run", None)]
    payload = json.dumps(data(), separators=(",", ":")).replace("</", "<\\/")
    body = """<div class="wrap">
  %s
  <header class="section-head pr-head"><h1>Pixel Run</h1><p class="lead">%s</p></header>
  %s
  <div class="wrap-narrow" style="width:100%%;margin-inline:auto">
    <article class="prose" style="padding-bottom:var(--sp-8)">%s</article>
  </div>
  <script type="application/json" id="pr-data">%s</script>
</div>""" % (crumbs(trail), esc(LEAD), _shell(), markup.render(_prose()), payload)
    write(PATH, layout(
        title=TITLE, description=DESCRIPTION, path=PATH, body=body, active="/python/",
        extra_head='<link rel="stylesheet" href="/assets/css/game.css">',
        scripts=["/assets/js/game-art.js", "/assets/js/game.js"],
        jsonld=[crumbs_ld(trail), _app_ld()]))
    register(PATH, 0.8, "monthly")
    add_search("Pixel Run: the Python platformer", PATH,
               "A game: write Python to clear every obstacle",
               "game platformer python play fun levels coding challenges pixel run functions loops "
               "recursion practice gcse a level")
    print("Pixel Run: %d challenges proven, page written to %s" % (n, PATH))
