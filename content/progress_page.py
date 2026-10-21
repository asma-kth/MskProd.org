"""The progress dashboard page.

The page ships empty. Everything on it is drawn in the browser from the
manifest at /assets/data/progress.json and whatever this browser has saved in
local storage, so no score ever leaves the student's own machine and there is
nothing to sign in to.
"""
from mskbuild import markup
from mskbuild.render import layout, crumbs, crumbs_ld, esc, write

LEAD = ("What you have covered, what you are weak at, and the five topics worth "
        "opening today. It is worked out in your browser, and nothing is uploaded.")

FOOT = """
!info How the five picks work :: A topic you scored well on comes back after up to ten days, and a weak one comes back tomorrow.
"""


def build(register, add_search):
    trail = [("Home", "/"), ("Progress", None)]
    body = """<div class="wrap">
  %s
  <header class="section-head" style="margin-bottom:var(--sp-5)">
    <h1>Your progress</h1>
    <p class="lead">%s</p>
  </header>
  <div id="dash" class="dash">
    <noscript><p class="muted">The dashboard reads your saved scores using JavaScript,
    so it needs JavaScript switched on. Every topic, quiz and exam paper on the rest of
    the site works without it.</p></noscript>
    <p class="muted">Working out where you are.</p>
  </div>
  <div class="wrap-narrow" style="width:100%%;margin-inline:auto">
    <article class="prose" style="padding-bottom:var(--sp-8)">%s</article>
  </div>
</div>""" % (crumbs(trail), esc(LEAD), markup.render(FOOT))
    path = "/progress/"
    write(path, layout(
        title="Your Revision Progress", description=LEAD, path=path, body=body,
        active="/progress/",
        scripts=["/assets/js/dashboard.js"],
        jsonld=[crumbs_ld(trail)]))
    register(path, 0.6, "weekly")
    add_search("Your progress", path,
               "Completion, weakest topics and what to revise today",
               "progress dashboard streak spaced repetition revision plan weakest "
               "topics what to revise today")
