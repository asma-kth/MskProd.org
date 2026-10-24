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

CONTACT_MORE = """
Include the page address and the question number; your email is used only to reply to you, as the [privacy policy](/privacy/) explains.
"""

TEACHERS = """
## Ready to use now

| Resource | What it gives you |
|---|---|
| [Timed exam papers](/exam-papers/) | Full length papers for every specification, with the real marks, time allowed and sections, a countdown clock and automatic marking. Two unit exams for every Key Stage 3 unit. |
| [Printable worksheets](/worksheets/) | One for every topic: the knowledge check, the exam-style questions with ruled answer space, and the mark scheme on a separate sheet so it can be handed out without the answers. |
| [Assignment links](/assign/) | Pick the topics you want revised and send one link. No accounts, and nothing is stored. |
| [Interactive tools](/tools/) | A number base converter, file size calculator, Little Man Computer simulator and more, built for showing on the board. |
| [The Python course](/python/) and [Pixel Run](/pixel-run/) | Python from a first program to A Level, with every example runnable in the browser, and a platform game that teaches it. |
| [Computational Thinking Adventure](/computational-thinking/) and [teacher mode](/computational-thinking/teacher/) | Forty game levels on decomposition, abstraction, pattern recognition and algorithms, with answers, previews and printable certificates. |
| [How to revise](/how-to-revise/) and the [glossary](/glossary/) | What actually works when revising, and every key term defined the way a mark scheme wants it. |

## Resources on request

Need a unit test, a mock paper or extra practice on a hard topic? Email [{email}](mailto:{email}?subject=Teacher%20resource%20request) with the subject **Teacher resource request**, or use the [request form](/contact/?type=teacher).

## Using the site with a class

There are no accounts, and scores stay on each student's own device, so ask for a screenshot or collect a printed worksheet.
"""


def _contact_page():
    trail = [("Home", "/"), ("Contact", None)]
    options = "".join('<option value="%s">%s</option>' % (v, esc(t)) for v, t in TYPES)
    lead = ("Found a wrong answer, a broken link or something you cannot use? Tell me and it will be fixed. "
            "Teachers can ask for resources here too.")
    body = """<div class="wrap">
  %s
  <div class="wrap-narrow" style="width:100%%;margin-inline:auto">
    <header class="topic-header">
      <h1>Contact and report a problem</h1>
      <p class="lead">%s</p>
    </header>
    <div class="grid grid-2" style="margin-bottom:var(--sp-5)">
      <div class="card contact-card">
        <h2>%s Email</h2>
        <p><a class="contact-email" href="mailto:%s">%s</a></p>
        <p class="muted">Every message is read by me, Asma Kethiri, Head of Computing and the author of this site.</p>
      </div>
      <div class="card contact-card">
        <h2>%s Teachers</h2>
        <p>Everything here is free to use with your classes, and you can ask for resources that are not on the site yet.</p>
        <p><a href="/teachers/">Resources for teachers</a></p>
      </div>
    </div>
    <form class="card contact-form" data-contact-form data-to="%s">
      <h2>Report a problem or ask for something</h2>
      <p class="muted">This writes the email and opens it in your own email program, so nothing is sent from this page.</p>
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
      <noscript><p>This form needs JavaScript. Please email <a href="mailto:%s">%s</a> directly instead.</p></noscript>
    </form>
    <article class="prose" style="padding-bottom:var(--sp-6)">%s</article>
  </div>
</div>""" % (crumbs(trail), esc(lead), ico("i-mail"), CONTACT_EMAIL, CONTACT_EMAIL, ico("i-user"), CONTACT_EMAIL,
             options, ico("i-mail"), ico("i-copy"), CONTACT_EMAIL, CONTACT_EMAIL, markup.render(CONTACT_MORE))
    ld = [crumbs_ld(trail), {
        "@context": "https://schema.org", "@type": "ContactPage", "name": "Contact " + SITE_NAME,
        "url": SITE_URL + "/contact/",
        "mainEntity": {"@type": "Person", "name": "Asma Kethiri", "jobTitle": "Head of Computing",
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
    lead = ("Everything on MskProd Computing is free to use with your classes, in lessons, for homework and for revision. "
            "Here is what is ready now, and what you can ask for.")
    body = """<div class="wrap">
  %s
  <div class="page-panel">
    <article class="prose">
      <header class="topic-header"><h1>For teachers</h1><p class="lead">%s</p></header>
      %s
    </article>
  </div>
</div>""" % (crumbs(trail), esc(lead), markup.render(TEACHERS.replace("{email}", CONTACT_EMAIL)))
    path = "/teachers/"
    write(path, layout(title="For Teachers: Free Computing Resources", description=lead, path=path, body=body,
                       jsonld=[crumbs_ld(trail)]))
    register(path, 0.7, "monthly")
    add_search("For teachers", path, "Free resources for classes, and resources on request",
               "teacher teachers resources request school class department worksheets assessment mock scheme of work")
