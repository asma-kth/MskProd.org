"""The assignment link builder.

Choosing topics produces a link with the whole assignment encoded inside it.
There is no account, no database and no server side record: whoever opens the
link gets the list, and their own progress against it is read from their own
browser and shown only to them.
"""
from mskbuild.render import layout, crumbs, crumbs_ld, write

LEAD = "Pick topics and send one link."


def build(register, add_search):
    trail = [("Home", "/"), ("Set an assignment", None)]
    body = """<div class="wrap">
  %s
  <header class="section-head" style="margin-bottom:var(--sp-5)">
    <h1>Set an assignment</h1>
  </header>
  <div id="assign" class="assign">
    <noscript><p class="muted">This page needs JavaScript.</p></noscript>
    <p class="muted">Loading the topic list.</p>
  </div>
</div>""" % crumbs(trail)
    path = "/assign/"
    write(path, layout(
        title="Set a Revision Assignment", description=LEAD, path=path, body=body,
        scripts=["/assets/js/assign.js"],
        jsonld=[crumbs_ld(trail)]))
    register(path, 0.6, "monthly")
    add_search("Set an assignment", path,
               "Build a shareable revision list with no accounts",
               "assignment homework teacher set work link share class revision list")
