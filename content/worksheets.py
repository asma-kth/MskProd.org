"""Printable worksheets, generated from the question banks already on the site.

Each worksheet is one page per topic: the ten knowledge check questions with no
answers, the exam-style questions with ruled answer space, and a mark scheme on
a fresh sheet so it can be printed and handed out without the answers attached.
"""
from mskbuild import markup
from mskbuild.render import (layout, crumbs, crumbs_ld, ico, esc, write, SITE_NAME)

LETTERS = "ABCDEFGH"


def _lines(n):
    return '<div class="ws-lines">%s</div>' % ("".join('<span></span>' for _ in range(n)))


def _worksheet(course, unit, topic):
    path = "/%s/%s/worksheet/" % (course.slug, topic.slug)
    title = "%s worksheet" % topic.title
    trail = [("Home", "/"), (course.short, "/%s/" % course.slug),
             (topic.title, "/%s/%s/" % (course.slug, topic.slug)),
             ("Worksheet", None)]

    total_exam = sum(q.marks for q in topic.exam)

    head = """<header class="ws-head">
  <div class="ws-title">
    <p class="ws-course">%s%s</p>
    <h1>%s</h1>
    <p class="ws-meta">Section A: %d multiple choice questions, %d marks.
      Section B: %d written questions, %d marks. Total %d marks.</p>
  </div>
  <div class="ws-fields">
    <p><span>Name</span><b></b></p>
    <p><span>Class</span><b></b></p>
    <p><span>Date</span><b></b></p>
    <p><span>Mark</span><b>&nbsp; / %d</b></p>
  </div>
</header>""" % (esc(course.short), (" &middot; " + esc(topic.spec)) if topic.spec else "",
                esc(topic.title), len(topic.quiz), len(topic.quiz), len(topic.exam),
                total_exam, len(topic.quiz) + total_exam,
                len(topic.quiz) + total_exam)

    # ------------------------------------------------------------ section A
    a_items = []
    for i, q in enumerate(topic.quiz):
        opts = "".join(
            '<li><span class="ws-opt">%s</span>%s</li>' % (LETTERS[j], markup.inline(o))
            for j, o in enumerate(q.options))
        a_items.append(
            '<li class="ws-q"><div class="ws-stem"><span class="ws-n">%d</span>'
            '<span>%s</span><span class="ws-marks">1</span></div>'
            '<ol class="ws-opts">%s</ol></li>' % (i + 1, markup.inline(q.stem), opts))
    section_a = ('<section class="ws-section"><h2>Section A</h2>'
                 '<p class="ws-lead">Circle the letter of the correct answer. '
                 'One mark each.</p><ol class="ws-list">%s</ol></section>'
                 % "".join(a_items)) if topic.quiz else ""

    # ------------------------------------------------------------ section B
    b_items = []
    for i, q in enumerate(topic.exam):
        cmd = '<span class="ws-cmd">%s</span>' % esc(q.command) if q.command else ""
        b_items.append(
            '<li class="ws-q"><div class="ws-stem"><span class="ws-n">%d</span>'
            '<span>%s%s</span><span class="ws-marks">%d</span></div>%s</li>'
            % (i + 1, cmd, markup.inline(q.stem), q.marks, _lines(max(3, q.marks * 2))))
    section_b = ('<section class="ws-section ws-break"><h2>Section B</h2>'
                 '<p class="ws-lead">Answer in the space provided. The number of marks '
                 'tells you how many separate points to make.</p>'
                 '<ol class="ws-list">%s</ol></section>' % "".join(b_items)) if topic.exam else ""

    # -------------------------------------------------------- mark scheme
    ms = []
    if topic.quiz:
        cells = "".join(
            '<span class="ws-ans"><b>%d</b>%s</span>' % (i + 1, LETTERS[q.answer])
            for i, q in enumerate(topic.quiz))
        ms.append('<h3>Section A</h3><div class="ws-answers">%s</div>' % cells)
    if topic.exam:
        rows = []
        for i, q in enumerate(topic.exam):
            pts = "".join("<li>%s</li>" % markup.inline(p.text) for p in q.points)
            rows.append(
                '<div class="ws-ms"><p class="ws-ms-head"><b>%d</b> %s '
                '<span class="ws-marks">%d</span></p>'
                '<p class="ws-ms-note">One mark for each of the following, to a maximum '
                'of %d.</p><ul>%s</ul>'
                '<p class="ws-ms-model"><b>Model answer.</b> %s</p></div>'
                % (i + 1, markup.inline(q.stem), q.marks, q.marks, pts,
                   markup.inline(q.model)))
        ms.append('<h3>Section B</h3>%s' % "".join(rows))
    mark_scheme = ('<section class="ws-section ws-break"><h2>Mark scheme</h2>%s</section>'
                   % "".join(ms)) if ms else ""

    body = """<div class="wrap">
  %s
  <div class="ws-actions no-print">
    <button class="btn btn-primary" type="button" onclick="window.print()">%s Print this worksheet</button>
    <a class="btn btn-secondary" href="/%s/%s/">%s Back to the topic</a>
    <p class="muted">The mark scheme starts on a new page, so you can print pages one
      and two for a student and keep the last page yourself. Everything prints in black
      on white whichever theme you are using.</p>
  </div>
  <article class="worksheet">
    %s
    %s
    %s
    %s
    <footer class="ws-foot">%s &middot; mskprod.org &middot; %s</footer>
  </article>
</div>""" % (crumbs(trail), ico("i-paper"), course.slug, topic.slug,
             ico("i-arrow-left"), head, section_a, section_b, mark_scheme,
             esc(SITE_NAME), esc(topic.title))

    desc = ("A printable worksheet for %s, with %d multiple choice questions, %d "
            "exam-style questions and a full mark scheme."
            % (topic.title, len(topic.quiz), len(topic.exam)))
    return path, layout(title=title, description=desc, path=path, body=body,
                        active="/%s/" % course.slug, jsonld=[crumbs_ld(trail)])


def build(register, add_search, courses):
    index_rows = []
    for course in courses:
        rows = []
        for unit in course.units:
            for topic in unit.topics:
                if not topic.quiz and not topic.exam:
                    continue
                path, html = _worksheet(course, unit, topic)
                write(path, html)
                register(path, 0.5, "monthly")
                add_search("%s worksheet" % topic.title, path,
                           "Printable worksheet and mark scheme",
                           ("worksheet printable print %s %s mark scheme questions"
                            % (topic.title, course.short)).lower())
                rows.append(
                    '<a class="unit-row" href="%s"><span class="unit-num">%s</span>'
                    '<span><b>%s</b><small>%d multiple choice, %d written, %d marks'
                    '</small></span><span>%s</span></a>'
                    % (path, esc(topic.spec or ""), esc(topic.title), len(topic.quiz),
                       len(topic.exam), len(topic.quiz) + sum(q.marks for q in topic.exam),
                       ico("i-arrow-right")))
        if rows:
            index_rows.append(
                '<section class="section"><div class="section-head"><h2>%s</h2>'
                '<p>%s</p></div><div class="unit-list">%s</div></section>'
                % (esc(course.title), esc(course.blurb), "".join(rows)))

    trail = [("Home", "/"), ("Worksheets", None)]
    lead = ("Every topic on the site as a worksheet you can print: the knowledge check "
            "as multiple choice, the exam-style questions with ruled answer space, and "
            "the mark scheme on a separate sheet. Useful for revising away from a "
            "screen, and for teachers who want a ready made lesson resource.")
    body = """<div class="wrap">
  %s
  <header class="section-head"><h1>Printable worksheets</h1><p class="lead">%s</p></header>
  %s
</div>""" % (crumbs(trail), esc(lead), "".join(index_rows))
    path = "/worksheets/"
    write(path, layout(title="Printable Computing Worksheets", description=lead,
                       path=path, body=body,
                       greeting="Printing a worksheet and doing it with a pen beats "
                                "clicking through a quiz, because writing an answer out "
                                "is closer to what the exam actually asks of you.",
                       jsonld=[crumbs_ld(trail)]))
    register(path, 0.7, "monthly")
    add_search("Printable worksheets", path, "Every topic as a printable worksheet",
               "worksheets printable print pdf homework mark scheme paper practice")
