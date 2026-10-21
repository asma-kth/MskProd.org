"""The assignment link builder.

Choosing topics produces a link with the whole assignment encoded inside it.
There is no account, no database and no server side record: whoever opens the
link gets the list, and their own progress against it is read from their own
browser and shown only to them.
"""
from mskbuild import markup
from mskbuild.render import layout, crumbs, crumbs_ld, esc, write

LEAD = ("Pick the topics you want set, and this page builds a link that carries the "
        "whole assignment inside it. Send the link however you already send work.")

FOOT = """
!info How the link works :: The topics travel inside the link, so nothing is stored, and each student's ticks show only in their own browser.
"""


def build(register, add_search):
    trail = [("Home", "/"), ("Set an assignment", None)]
    body = """<div class="wrap">
  %s
  <header class="section-head" style="margin-bottom:var(--sp-5)">
    <h1>Set an assignment</h1>
    <p class="lead">%s</p>
  </header>
  <div id="assign" class="assign">
    <noscript><p class="muted">The builder needs JavaScript to encode your choices
    into a link.</p></noscript>
    <p class="muted">Loading the topic list.</p>
  </div>
  <div class="wrap-narrow" style="width:100%%;margin-inline:auto">
    <article class="prose" style="padding-bottom:var(--sp-8)">%s</article>
  </div>
</div>""" % (crumbs(trail), esc(LEAD), markup.render(FOOT))
    path = "/assign/"
    write(path, layout(
        title="Set a Revision Assignment", description=LEAD, path=path, body=body,
        scripts=["/assets/js/assign.js"],
        jsonld=[crumbs_ld(trail)]))
    register(path, 0.6, "monthly")
    add_search("Set an assignment", path,
               "Build a shareable revision list with no accounts",
               "assignment homework teacher set work link share class revision list")
