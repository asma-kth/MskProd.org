"""The contact page and the page for teachers.

The site has no server, so the contact form sends nothing itself: it writes the
message, with the page and question it came from, and opens the reader's own
email program addressed to the site's contact address.
"""
from mskbuild import markup
from mskbuild.render import (layout, crumbs, crumbs_ld, ico, esc, write, SITE_NAME, SITE_URL,
                             CONTACT_EMAIL)

TYPES = [
    ("answer", "An incorrect answer or mark scheme"),
    ("broken", "A broken link, page, tool or program"),
    ("access", "An accessibility problem"),
    ("teacher", "A teacher resource request"),
    ("other", "Something else"),
]


TEACHERS = """
## Ready to use

+ [Timed exam papers](/exam-papers/)
+ [Stretch tasks for every Key Stage 3 lesson](/ks3/stretch/)
+ [Printable worksheets](/worksheets/)
+ [Assignment links](/assign/)
+ [Interactive tools](/tools/)
+ [The Python course](/python/) and [Pixel Run](/pixel-run/)
+ [Computational Thinking Adventure](/computational-thinking/) and its [teacher mode](/computational-thinking/teacher/)
+ [How to revise](/how-to-revise/) and the [glossary](/glossary/)

## Resources on request

Email [{email}](mailto:{email}?subject=Teacher%20resource%20request) or use the [request form](/contact/?type=teacher).
"""


def _contact_page():
    trail = [("Home", "/"), ("Contact", None)]
    options = "".join('<option value="%s">%s</option>' % (v, esc(t)) for v, t in TYPES)
    lead = "Report a wrong answer, a broken link or an accessibility problem, or ask for a resource."
    body = """<div class="wrap">
  %s
  <div class="wrap-narrow" style="width:100%%;margin-inline:auto">
    <header class="topic-header">
      <h1>Contact and report a problem</h1>
    </header>
    <div class="grid grid-2" style="margin-bottom:var(--sp-5)">
      <div class="card contact-card">
        <h2>%s Email</h2>
        <p><a class="contact-email" href="mailto:%s">%s</a></p>
        <p class="muted">Read by Ms Kethiri, head of the computing department at a school in London.</p>
      </div>
      <div class="card contact-card">
        <h2>%s Teachers</h2>
        <p><a href="/teachers/">Resources for teachers</a></p>
      </div>
    </div>
    <form class="card contact-form" data-contact-form data-to="%s">
      <h2>Report a problem or ask for something</h2>
      <label for="cf-type">What is it about?</label>
      <select id="cf-type" name="type">%s</select>
      <label for="cf-page">Page address</label>
      <input id="cf-page" name="page" type="text" inputmode="url" autocomplete="off" placeholder="https://mskprod.org/...">
      <label for="cf-question">Question number, if there is one</label>
      <input id="cf-question" name="question" type="text" autocomplete="off">
      <label for="cf-details">What is wrong, or what do you need?</label>
      <textarea id="cf-details" name="details" rows="6" required></textarea>
      <label for="cf-role">I am a</label>
      <select id="cf-role" name="role"><option>Student</option><option>Teacher</option><option>Parent or carer</option><option>Other</option></select>
      <div class="btn-row">
        <button class="btn btn-primary" type="submit">%s Open in my email app</button>
        <button class="btn btn-secondary" type="button" data-contact-copy>%s Copy the message</button>
      </div>
      <p class="contact-status" data-contact-status aria-live="polite"></p>
      <noscript><p>Email <a href="mailto:%s">%s</a>.</p></noscript>
    </form>
  </div>
</div>""" % (crumbs(trail), ico("i-mail"), CONTACT_EMAIL, CONTACT_EMAIL, ico("i-user"), CONTACT_EMAIL,
             options, ico("i-mail"), ico("i-copy"), CONTACT_EMAIL, CONTACT_EMAIL)
    ld = [crumbs_ld(trail), {
        "@context": "https://schema.org", "@type": "ContactPage", "name": "Contact " + SITE_NAME,
        "url": SITE_URL + "/contact/",
        "mainEntity": {"@type": "Person", "name": "Ms Kethiri", "jobTitle": "Head of the computing department",
                       "email": "mailto:" + CONTACT_EMAIL}}]
    return body, lead, ld


def build(register, add_search):
    body, lead, ld = _contact_page()
    path = "/contact/"
    write(path, layout(title="Contact and Report a Problem", description=lead, path=path, body=body,
                       scripts=["/assets/js/contact.js"], jsonld=ld))
    register(path, 0.5, "yearly")
    add_search("Contact and report a problem", path, "Report a wrong answer, a broken page or an accessibility problem",
               "contact email report problem mistake error wrong answer mark scheme broken link accessibility teacher request")

    trail = [("Home", "/"), ("For teachers", None)]
    lead = "Free resources for teachers, and resources on request."
    body = """<div class="wrap">
  %s
  <div class="page-panel">
    <article class="prose">
      <header class="topic-header"><h1>For teachers</h1></header>
      %s
    </article>
  </div>
</div>""" % (crumbs(trail), markup.render(TEACHERS.replace("{email}", CONTACT_EMAIL)))
    path = "/teachers/"
    write(path, layout(title="For Teachers: Free Computing Resources", description=lead, path=path, body=body,
                       jsonld=[crumbs_ld(trail)]))
    register(path, 0.7, "monthly")
    add_search("For teachers", path, "Free resources for classes, and resources on request",
               "teacher teachers resources request school class department worksheets assessment mock scheme of work")
