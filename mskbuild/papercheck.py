"""Prove every practice paper before it is published.

A full length paper promises the real paper's marks and time allowed, so both
are checked against the official figures below. Every closed question must have
a consistent answer key, and every programming question is marked by running
its model solution (a program, or an SQL statement run against its database)
through mskbuild/codemark.py, the same code the browser uses:
the solution must score full marks, and the starter code and each listed wrong
answer must lose at least one mark. The build stops if anything is unsound.
"""
import collections
import re

from . import codemark

# (total marks, minutes allowed), from each board's specification.
OFFICIAL = {
    "J277/01": (80, 90), "J277/02": (80, 90),                 # OCR GCSE Computer Science
    "8525/1B": (90, 120), "8525/2": (90, 105),                # AQA GCSE Computer Science
    "1CP2/01": (75, 90), "1CP2/02": (75, 120),                # Pearson Edexcel GCSE Computer Science
    "H446/01": (140, 150), "H446/02": (140, 150),             # OCR A Level Computer Science
    "R093": (70, 90),                                          # OCR Cambridge National Creative iMedia
    "F200": (60, 75), "F201": (60, 90),                        # OCR Cambridge Advanced National IT: Data Analytics
}

# Papers with printed sections must total each section exactly.
SECTIONS = {
    "J277/02": {"Section A": 50, "Section B": 30},
    "R093": {"Section A": 10, "Section B": 60},
    "1CP2/01": {"Question %d" % n: 15 for n in range(1, 6)},
}

KS3_UNIT = (25, 25)       # every Key Stage 3 unit exam: 25 marks in 25 minutes


class PaperError(Exception):
    pass


def _check_question(paper, n, q, problems):
    where = "%s question %s" % (paper.slug, q.label or n + 1)
    kind = q.kind or "text"
    if q.marks < 1:
        problems.append("%s: no marks" % where)
    if kind == "text":
        if len(q.points) < q.marks:
            problems.append("%s: %d marks but only %d mark points" % (where, q.marks, len(q.points)))
        for p in q.points:
            if not p.any:
                problems.append("%s: mark point with no phrasings: %s" % (where, p.text))
    elif kind == "choice":
        if len(q.options) < 2 or len(set(q.options)) != len(q.options):
            problems.append("%s: needs at least two different options" % where)
        if not q.correct or len(set(q.correct)) != len(q.correct) or any(not 0 <= c < len(q.options) for c in q.correct):
            problems.append("%s: answer key %r does not fit the options" % (where, q.correct))
        if q.marks != len(q.correct):
            problems.append("%s: %d marks for %d correct boxes" % (where, q.marks, len(q.correct)))
    elif kind == "matrix":
        if len(q.correct) != len(q.rows) or any(not 0 <= c < len(q.cols) for c in q.correct):
            problems.append("%s: needs one correct column per row" % where)
        if q.marks and len(q.rows) % q.marks:
            problems.append("%s: %d rows cannot share %d marks evenly" % (where, len(q.rows), q.marks))
    elif kind == "blanks":
        if not q.blanks:
            problems.append("%s: no answer boxes" % where)
        for b in q.blanks:
            if not b.accept:
                problems.append("%s: an answer box accepts nothing" % where)
            if b.numeric:
                for a in b.accept:
                    try:
                        float(a)
                    except ValueError:
                        problems.append("%s: numeric box accepts %r" % (where, a))
        used = [c for row in q.grid for c in row if isinstance(c, int)]
        if q.grid and sorted(used) != list(range(len(q.blanks))):
            problems.append("%s: the grid must place every box exactly once" % where)
        groups = q.groups or [("", [i]) for i in range(len(q.blanks))]
        covered = sorted(i for _, nums in groups for i in nums)
        if covered != list(range(len(q.blanks))):
            problems.append("%s: every box must belong to exactly one mark" % where)
        if q.working:
            if len(groups) != 1:
                problems.append("%s: a question with working has one final answer" % where)
            if q.marks > 1 and len(q.points) < q.marks - 1:
                problems.append("%s: needs %d method marks" % (where, q.marks - 1))
        elif q.marks != len(groups):
            problems.append("%s: %d marks for %d marked boxes" % (where, q.marks, len(groups)))
    elif kind == "code":
        t = q.code
        if t is None:
            problems.append("%s: no code task" % where)
            return
        if q.marks != len(t.checks):
            problems.append("%s: %d marks for %d checks" % (where, q.marks, len(t.checks)))
        exprs = [c.expr for c in t.checks]
        res = codemark.mark(t.solution, exprs, t.files, t.lang, t.setup)
        for c, (ok, why) in zip(t.checks, res):
            if not ok:
                problems.append("%s: the model solution fails '%s' (%s)" % (where, c.text, why or "check is false"))
        if all(ok for ok, _ in codemark.mark(t.starter, exprs, t.files, t.lang, t.setup)):
            problems.append("%s: the starter code already scores full marks" % where)
        for k, w in enumerate(t.wrong):
            if all(ok for ok, _ in codemark.mark(w, exprs, t.files, t.lang, t.setup)):
                problems.append("%s: wrong answer %d scores full marks" % (where, k + 1))
    else:
        problems.append("%s: unknown kind %r" % (where, kind))


def validate(papers):
    """Raise PaperError listing every problem; return a short report otherwise."""
    problems = []
    slugs = collections.Counter(p.slug for p in papers)
    for slug, n in slugs.items():
        if n > 1:
            problems.append("%s: used by %d papers" % (slug, n))
    letters = collections.Counter()
    for paper in papers:
        total = sum(q.marks for q in paper.questions)
        if total != paper.marks:
            problems.append("%s: questions add up to %d, paper says %d" % (paper.slug, total, paper.marks))
        if paper.full:
            want = OFFICIAL.get(paper.code)
            if not want:
                problems.append("%s: no official figures for %s" % (paper.slug, paper.code))
            elif (paper.marks, paper.minutes) != want:
                problems.append("%s: %d marks in %d minutes, but the real %s is %d marks in %d minutes"
                                % (paper.slug, paper.marks, paper.minutes, paper.code, want[0], want[1]))
            sec = SECTIONS.get(paper.code)
            if sec:
                got = collections.OrderedDict()
                current = None
                for q in paper.questions:
                    if q.section:
                        current = q.section
                    got[current] = got.get(current, 0) + q.marks
                if dict(got) != sec:
                    problems.append("%s: sections %s, but the real paper has %s" % (paper.slug, dict(got), sec))
        if paper.spec == "KS3" and paper.unit and (paper.marks, paper.minutes) != KS3_UNIT:
            problems.append("%s: a unit exam should be %d marks in %d minutes" % ((paper.slug,) + KS3_UNIT))
        labels = [q.label for q in paper.questions if q.label]
        if len(labels) != len(set(labels)):
            problems.append("%s: repeated question labels" % paper.slug)
        for n, q in enumerate(paper.questions):
            _check_question(paper, n, q, problems)
            if q.kind == "choice":
                for c in q.correct:
                    letters["ABCDEFGH"[c]] += 1
    if problems:
        raise PaperError("\n".join(problems))
    return letters
