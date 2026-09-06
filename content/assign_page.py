"""The assignment link builder.

Choosing topics produces a link with the whole assignment encoded inside it.
There is no account, no database and no server side record: whoever opens the
link gets the list, and their own progress against it is read from their own
browser and shown only to them.
"""
from mskbuild import markup
from mskbuild.render import layout, crumbs, crumbs_ld, esc, write

LEAD = ("Pick the topics you want set, and this page builds a link that carries the "
        "whole assignment inside it. Send the link however you already send work. "
        "There is nothing to sign up for and nothing is stored anywhere.")

FOOT = """
### How the link works

Everything you choose is packed into the part of the address after the hash symbol.
A browser never sends that part to a server, so the assignment travels from you to
your students and stops there. No copy of it is kept on this site, which also means
a link cannot be edited or withdrawn once you have sent it: to change an assignment,
build a new link.

### What a student sees

The list of topics, with the number of questions on each, and a tick against every
one where their knowledge check is already at 80 per cent or better. That tick is
read from their own browser's storage.

!warn It cannot be used as a register :: A student's progress lives in their browser and is never sent anywhere, so you cannot see who has done what. That is the price of having no accounts and collecting no data, and for a revision site it is the right trade. Ask for a screenshot, or set the written questions as the thing you actually collect in.

!key Good assignments are small :: Three or four topics with a deadline gets done. Twenty topics with no deadline does not. The link takes ten seconds to make, so make several small ones.

### Ideas

+ One topic a week through a term, sent every Monday
+ The six topics a class did worst on in a mock, sent as a targeted catch up
+ A whole paper's worth of topics two weeks before a mock
+ The prerequisite topics for the unit you are about to start, set as preparation
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
    into a link. Every topic, quiz and worksheet on the rest of the site works
    without it.</p></noscript>
    <p class="muted">Loading the topic list.</p>
  </div>
  <div class="wrap-narrow" style="width:100%%;margin-inline:auto">
    <article class="prose" style="padding-bottom:var(--sp-8)">%s</article>
  </div>
</div>""" % (crumbs(trail), esc(LEAD), markup.render(FOOT))
    path = "/assign/"
    write(path, layout(
        title="Set a Revision Assignment", description=LEAD, path=path, body=body,
        greeting="Teachers: three topics and a deadline beats twenty topics and good "
                 "intentions. Students: if somebody sent you here, the list is above.",
        scripts=["/assets/js/assign.js"],
        jsonld=[crumbs_ld(trail)]))
    register(path, 0.6, "monthly")
    add_search("Set an assignment", path,
               "Build a shareable revision list with no accounts",
               "assignment homework teacher set work link share class revision list")
