"""Stretch tasks for every A Level topic.

As at Key Stage 4, a lesson is a whole topic page, and it gets every task:
the quiz challenge, This or That, Memory Match and Sort It, then Code Word,
Link Up and Bug Hunt, the three brain games and City Run. Each module holds
the lessons for one unit of the course: it defines COURSE, the course's
slug, and LESSONS, one Stretch per topic, whose `lesson` is the topic's slug.
Beside each sits a module whose name ends in _games, defining GAMES: the
words for Code Word, the groups for Link Up and the rounds of Bug Hunt.

A course is published once every one of its lessons is written, which is
what `complete` records. While a course is being written, setting
STRETCH_DRAFT=1 builds its finished lessons too, to try them out.
"""
import importlib
import os

# key in URLs and saved results, course slug, name on the pages, modules, complete
COURSES = [
    ("ocr", "ks5", "OCR H446 A Level Computer Science",
     ["h446_processors", "h446_software", "h446_exchanging", "h446_data_logic", "h446_issues",
      "h446_thinking", "h446_algorithms"], True),
]

# Topics that are not lessons: the guide to the programming project, which
# says how the coursework is marked rather than teaching a topic.
NOT_LESSONS = {("ks5", "nea-programming-project")}


def _module(name):
    """A module of this package, or None if it has not been written yet."""
    full = "content.ks5_stretch." + name
    try:
        return importlib.import_module(full)
    except ModuleNotFoundError as e:
        if e.name != full:
            raise
        return None


def _join_games(name, lessons):
    """Give each lesson of a module the games written for it."""
    games = _module(name + "_games")
    if games is None:
        return
    by_slug = {st.lesson: st for st in lessons}
    seen = set()
    for g in games.GAMES:
        st = by_slug.get(g.lesson)
        if st is None:
            raise SystemExit("content/ks5_stretch/%s_games.py: %s has no lesson %r" % (name, name, g.lesson))
        if g.lesson in seen:
            raise SystemExit("content/ks5_stretch/%s_games.py: two sets of games for %r" % (name, g.lesson))
        seen.add(g.lesson)
        st.words, st.groups, st.bugs = g.words, g.groups, g.bugs


def draft():
    return bool(os.environ.get("STRETCH_DRAFT"))


def courses():
    """The courses whose lessons go on the site: the complete ones, and in
    draft mode the rest too, as far as they are written. [(key, course slug, name, [Stretch])]"""
    out = []
    for key, slug, name, modules, complete in COURSES:
        if not (complete or draft()):
            continue
        lessons = []
        for m in modules:
            mod = _module(m)
            if mod is None:
                if complete:
                    raise SystemExit("content/ks5_stretch/%s.py is missing" % m)
                continue
            if mod.COURSE != slug:
                raise SystemExit("content/ks5_stretch/%s.py says it belongs to %s, not %s" % (m, mod.COURSE, slug))
            _join_games(m, mod.LESSONS)
            lessons += mod.LESSONS
        if lessons:
            out.append((key, slug, name, lessons))
    return out


def complete(slug):
    return any(c[1] == slug and c[4] for c in COURSES)
