"""Stretch tasks for every lesson of the Key Stage 3 course, Year 7 to Year 9.

One module per unit, in the order the units are taught. Each defines TOPIC,
the slug of its unit, and LESSONS, one Stretch per lesson of that unit in the
order the unit teaches them. A lesson is a section of the unit's topic page.

Beside each unit's module sits one whose name ends in _games. It defines
GAMES, one Games per lesson: the words for Code Word, the groups for Link Up
and the rounds of Bug Hunt. They are joined to the lesson of the same name.
"""
import importlib

MODULES = [
    "y7_using_computers", "y7_scratch", "y7_python", "y7_understanding_computers", "y7_vector_graphics",
    "y8_digital_literacy", "y8_computational_thinking", "y8_python", "y8_spreadsheets",
    "y8_networks", "y8_web",
    "y9_law", "y9_data_representation", "y9_python", "y9_apps", "y9_ai", "y9_3d",
]

# Sections that are not lessons. The computational thinking unit ends by
# pointing at the adventure game, which is its own puzzle practice.
NOT_LESSONS = {("computational-thinking", "Practise it as a game")}


# Every Key Stage 3 lesson must have its three extra games before the site
# is built. Set to False only while they are still being written.
GAMES_COMPLETE = True


def _module(name):
    """A module of this package, or None if it has not been written."""
    full = "content.ks3_stretch." + name
    try:
        return importlib.import_module(full)
    except ModuleNotFoundError as e:
        if e.name != full:
            raise
        return None


def units():
    """[(topic slug, [Stretch])] for every unit module written so far, each
    lesson carrying the games written for it."""
    out = []
    for name in MODULES:
        mod = _module(name)
        if mod is None:
            continue
        games = _module(name + "_games")
        if games is not None:
            lessons = {st.lesson: st for st in mod.LESSONS}
            seen = set()
            for g in games.GAMES:
                st = lessons.get(g.lesson)
                if st is None:
                    raise SystemExit("content/ks3_stretch/%s_games.py: no lesson of %s is called %r"
                                     % (name, mod.TOPIC, g.lesson))
                if g.lesson in seen:
                    raise SystemExit("content/ks3_stretch/%s_games.py: two sets of games for %r" % (name, g.lesson))
                seen.add(g.lesson)
                st.words, st.groups, st.bugs = g.words, g.groups, g.bugs
        out.append((mod.TOPIC, mod.LESSONS))
    return out
