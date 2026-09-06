"""The progress dashboard page.

The page ships empty. Everything on it is drawn in the browser from the
manifest at /assets/data/progress.json and whatever this browser has saved in
local storage, so no score ever leaves the student's own machine and there is
nothing to sign in to.
"""
from mskbuild import markup
from mskbuild.render import layout, crumbs, crumbs_ld, esc, write

LEAD = ("What you have covered, what you are weak at, and the five topics worth "
        "opening today. Everything here is worked out in your browser from what "
        "you have done on this site. Nothing is uploaded and there is no account.")

FOOT = """
### How the five picks are chosen

The list is not random and it is not simply your lowest scores. Each topic you have
quizzed gets a next-review date based on how well you did: a score of 90 per cent or
more is not shown again for ten days, 80 per cent for six days, 65 per cent for three,
50 per cent for two, and anything lower comes back tomorrow. Topics are then ranked by
how weak the score was and how far past that date they are.

!key Why the gaps get longer :: Reviewing something just as you are starting to forget it strengthens the memory far more than reviewing it while it is still fresh. That is the spacing effect, and it is the reason a weak topic comes back tomorrow while a strong one waits a week and a half.

!warn A low score is information, not a verdict :: Getting five out of ten tells you exactly which half of a topic to reread. Getting ten out of ten tells you nothing you did not already know. The uncomfortable score is the useful one.

### Where this is stored

Your scores live in this browser's local storage under keys beginning with
`mskprod:`. They are not sent to a server, they are not shared, and no cookie is
set. That also means they do not follow you to another device or survive clearing
your browsing data, and a private window always starts empty. You can wipe
everything at any time from the [privacy page](/privacy/).
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
        greeting="Start with the five topics at the top. They are the ones where an "
                 "hour buys you the most marks.",
        scripts=["/assets/js/dashboard.js"],
        jsonld=[crumbs_ld(trail)]))
    register(path, 0.6, "weekly")
    add_search("Your progress", path,
               "Completion, weakest topics and what to revise today",
               "progress dashboard streak spaced repetition revision plan weakest "
               "topics what to revise today")
