"""The progress dashboard page.

The page ships empty. Everything on it is drawn in the browser from the
manifest at /assets/data/progress.json and whatever this browser has saved in
local storage, so no score ever leaves the student's own machine and there is
nothing to sign in to.
"""
from mskbuild.render import layout, crumbs, crumbs_ld, write

LEAD = "What you have covered, your weakest topics and what to revise today."


def build(register, add_search):
    trail = [("Home", "/"), ("Progress", None)]
    body = """<div class="wrap">
  %s
  <header class="section-head" style="margin-bottom:var(--sp-5)">
    <h1>Your progress</h1>
  </header>
  <div id="dash" class="dash">
    <noscript><p class="muted">This page needs JavaScript.</p></noscript>
    <p class="muted">Working out where you are.</p>
  </div>
</div>""" % crumbs(trail)
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
