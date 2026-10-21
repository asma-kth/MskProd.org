"""Key Stage 3 unit exams: two for every unit, each 25 marks in 25 minutes.

Most questions are closed (tick boxes, a tick per row, typed answers and short
programs that are run), so the marking is exact. A few short written answers
are marked against a mark scheme in the same style as a GCSE paper. Exam A and
Exam B cover the same unit with different questions, so a student can sit one,
revise from what they dropped, and sit the other.
"""
from mskbuild.models import Paper


def _titles():
    from content import ks3
    course = [getattr(ks3, n) for n in dir(ks3) if getattr(ks3, n).__class__.__name__ == "Course"][0]
    return {t.slug: (t.title, u.title) for u in course.units for t in u.topics}


def exam(unit, letter, blurb, questions):
    """One unit exam. The slug, title and timing follow from the unit."""
    title, year = _titles()[unit]
    return Paper(
        slug="ks3-%s-exam-%s" % (unit, letter.lower()),
        title="%s: Unit Exam %s" % (title, letter),
        course="Key Stage 3", board="MskProd", code="%s unit exam" % year,
        minutes=25, marks=sum(q.marks for q in questions),
        blurb=blurb, questions=questions,
        calculator="No calculator is permitted.", accent="var(--lilac-deep)",
        spec="KS3", unit=unit)


def all_exams():
    from content.ks3_exams_y7 import EXAMS as Y7
    from content.ks3_exams_y8 import EXAMS as Y8
    from content.ks3_exams_y9 import EXAMS as Y9
    return Y7 + Y8 + Y9
