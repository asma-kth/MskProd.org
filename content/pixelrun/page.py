"""The Pixel Run page: the game, and the written explanation around it.

Everything a search engine or a screen reader needs (how it works, the ten
levels, the questions people ask) is ordinary HTML. The game itself is built by
static/js/game.js from the JSON that this module embeds.
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
    example = BANK[0]
    tests = test_records(example)
    ex_rows = "\n".join("| `%s` | `%s` |" % (t["c"], t["e"].replace("|", "\\|")) for t in tests[:3])
    return """
## How the game works

1. **Pixel runs by herself.** You never have to time a jump. All of the skill is in the code.
2. **Every obstacle is a function to write.** The task, a few worked examples and some starter code are on screen.
3. **Press Run tests.** Your function is marked against every test. If they all pass, Pixel jumps the obstacle and runs on.
4. **Three obstacles clear a level, and ten levels clear the game.** The first level asks you to join two pieces of text. The last asks you to write Dijkstra's algorithm.
5. **If the obstacle wins, you go back a level.** Use up your three attempts, or give up, and Pixel is knocked back to the start of the **previous level**. You are shown a working solution first, so the setback teaches you something.

!key Replays are never the same :: Every level has five challenges and a run uses three of them. When you are sent back, the level you replay deals the challenges you have not met yet, so remembering answers will not get you through.

## The ten levels

%s

The first three levels are the foundations every program is made of. Levels 4 to 8 are the Python that the GCSE specifications (OCR J277, AQA 8525 and Edexcel 1CP2) expect you to write, up to the searching and sorting algorithms by name. Levels 9 and 10 are A Level: recursion, stacks, queues, graphs, shortest paths and two's complement.

## What a challenge looks like

Level 1, first obstacle: *write a function that greets someone.* You are given the function's name and a comment, and you fill in the rest.

```text
def greet(name):
    # return "Hello, " then the name then "!"
    pass
```

Your function is then run on a set of calls, and each answer is compared with what the tests expect:

| Call | The test expects |
%s

A test passes only when the answer matches exactly. `True` is not `1`, a list is not a tuple, and `"5"` is not `5`. Numbers are compared as numbers, so `2` and `2.0` are the same answer.

!warn Some challenges have rules :: A level about loops asks you to use a loop, a recursion level asks the function to call itself, and a sorting level will not accept `sorted()`. If your answers are right but you broke a rule, the game says so, and it counts as an attempt.

## Attempts, hints and stars

Every challenge gives you **three attempts**. An attempt is a run where your code ran and a test failed, or a rule was broken. A syntax error, or forgetting to define the function, does not use an attempt, because nothing was marked.

| Stars | How you earned them |
| 3 stars | Passed with no slips and no hints |
| 2 stars | Passed after one slip or one hint |
| 1 star | Passed after more than that |

There are two hints on every challenge, and each one costs a star. A level is worth up to nine stars, and the whole game is worth ninety.

## Questions

### Does my code leave my computer?

No. Python runs inside your browser tab, using Pyodide, which is Python compiled to WebAssembly. The tests arrive with the page and your code is marked on your own device. Nothing you write is sent anywhere, stored on a server or seen by anyone.

### Do I need to install anything or make an account?

No. The first time you play, your browser downloads Python once (roughly ten megabytes, which it then keeps). That happens while Pixel is running towards the first obstacle.

### What if Python will not load?

Some school networks block the download. If Python cannot be loaded, the game offers **quiz mode**: instead of writing the function you read a short piece of code and choose what it returns. The levels, the stars and the going-back-a-level rule all work the same way.

### Is my progress saved?

On your own device only, in your browser's local storage, so you can pick up from the level you reached. Clearing your site data, or switching to a different browser, starts again.

### Can I use it in a lesson?

Yes. It is free, there is nothing to sign up for, and every student plays on their own device. It works well as a starter, a plenary, or revision for a unit on programming. Because nothing is recorded centrally, a teacher cannot see who has played, and the best check is to ask students to show their level and star count.

!key Stuck on a level? :: Each level lists the topics to read first. Reading the topic and then playing the level is the fastest way through, and the game links straight to it whenever a level beats you.
""" % (_level_table(), ex_rows)


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
      <span>Calm mode stops the scrolling and the jumps. It switches on by itself if your device asks for less motion.</span></p>
  </div>
  <div class="pr-console" id="pr-console" tabindex="-1">
    <noscript><p>Pixel Run needs JavaScript, because the game and the Python it uses both run in your browser.
    The rest of the page explains how it works, and every topic and quiz on this site works without scripts.</p></noscript>
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
