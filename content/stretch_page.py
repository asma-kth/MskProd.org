"""Stretch tasks: games for every lesson at Key Stage 3 and Key Stage 4.

A Key Stage 3 lesson is a section of a unit's topic page; at Key Stage 4 a
lesson is a whole topic. Each lesson gets a page of its own. The Quiz
Challenge has three rounds: a quiz game against the clock, short written
answers, and long written answers marked against a mark scheme. In This or
That, Pixel the cat asks questions with two answers to choose from. Memory
Match is a card game: find each word's meaning. Key Stage 4 lessons add Sort
It: drag each statement into the right box, like the tick box tables on GCSE
papers. Then every lesson adds three games: Code Word, where each guess at a
secret word shows which letters are right; Link Up, where twelve tiles hide
three groups of four; and Bug Hunt, where two statements are true and one has
a mistake to catch. Last come three brain games, which replay the lesson as
brain training: Odd One Out (logic), Memory Flash (memory) and Fact or Fib
(speed); content/brain_games.py builds and checks them. Key Stage 3 lessons
end with City Run: a robot cat races through a neon cyber city and every
lane is an answer, twenty questions from the lesson's own tasks; content/city_run.py
builds and checks them. Results are rated out of three diamonds. The games themselves are static/js/stretch.js; this module
writes the pages, a hub for each key stage, and the links from the lessons to
them.

Every page also carries the whole task as plain HTML: it is what a browser
without JavaScript shows, and what prints when a teacher wants it on paper.
"""
import importlib
import json

from mskbuild import cat, markup, render, robocat
from mskbuild.render import (SITE_NAME, SITE_URL, crumbs, crumbs_ld, esc, ico, layout, write)
from mskbuild.util import slugify
from mskbuild import stretchcheck
from content import ks3
from content import ks3_stretch
from content import ks4_stretch
from content import brain_games
from content import city_run

HUB = "/ks3/stretch/"
DESC_LIMIT = 160   # characters a search result shows; a longer description is cut mid phrase


def _desc(name, games, short):
    """A lesson's description, naming every game when it fits in a search result."""
    full = "%s. %s%s" % (name, games[0].upper(), games[1:])
    return full if len(full) <= DESC_LIMIT else "%s. %s%s" % (name, short[0].upper(), short[1:])
HUB_TITLE = "Stretch tasks"
HUB_LEAD3 = ("Three tasks for every Year 7, 8 and 9 lesson: a quiz challenge, This or That with "
             "Pixel the cat, and Memory Match.")
HUB_LEAD = ("Ten tasks for every Year 7, 8 and 9 lesson: a quiz challenge, This or That with Pixel the cat, "
            "Memory Match, Code Word, Link Up and Bug Hunt, three brain games (Odd One Out, Memory Flash and "
            "Fact or Fib), then City Run, a robot cat's race through a neon cyber city. Every result is rated out of "
            "three diamonds.")

HUB4 = "/ks4/stretch/"
HUB4_TITLE = "Key Stage 4 stretch tasks"

ROUNDS = [("Quiz Blitz", "blitz"), ("Quick Fire", "short"), ("Big Think", "long")]

# The tasks on a lesson's page, in the order they are offered. The key is also
# what the game and the saved results call each one. Sort It is the fourth
# task at Key Stage 4. Code Word, Link Up and Bug Hunt follow: the fourth,
# fifth and sixth at Key Stage 3, the fifth, sixth and seventh at Key Stage 4.
# The three brain games come next, in a band of their own, and City Run, at
# Key Stage 3, last of all.
TASKS = [("quiz", "Quiz Challenge"), ("cat", "This or That"), ("match", "Memory Match"), ("sort", "Sort It"),
         ("word", "Code Word"), ("link", "Link Up"), ("bug", "Bug Hunt"),
         ("odd", "Odd One Out"), ("flash", "Memory Flash"), ("fib", "Fact or Fib"), ("run", "City Run")]
GAMES = ("word", "link", "bug")
BRAIN = ("odd", "flash", "fib")
SKILL = {"odd": "Logic", "flash": "Memory", "fib": "Speed"}

# The module that defines each Key Stage 4 course.
KS4_SOURCES = {"ks4/computer-science": "ks4_cs", "ks4/aqa-computer-science": "aqa_gcse",
               "ks4/edexcel-computer-science": "edexcel_gcse", "ks4/imedia": "ks4_imedia"}


def _tasks(r):
    """The tasks one lesson has, in the order its page offers them."""
    st = r["stretch"]
    brain = bool(st.groups and st.bugs and len(st.pairs) >= max(brain_games.FLASH_LEVELS))
    has = {"sort": bool(st.sort), "word": bool(st.words), "link": bool(st.groups), "bug": bool(st.bugs),
           "odd": brain, "flash": brain, "fib": brain, "run": city_run.available(r["stage"], brain)}
    return [t for t in TASKS if has.get(t[0], True)]


def _has_run(r):
    return any(t == "run" for t, _ in _tasks(r))


def _tasks_of(recs):
    """The tasks any of these lessons has: what a hub's cards make room for."""
    keys = {k for r in recs for k, _ in _tasks(r)}
    return [t for t in TASKS if t[0] in keys]


def _ks4_course(slug):
    return importlib.import_module("content." + KS4_SOURCES[slug]).COURSE

# Seconds on the clock for each kind of game question, before any extra for
# code to read or a long question.
TIME = {"choice": 20, "tf": 15, "multi": 30, "order": 40, "type": 30}

SHAPES = {
    "tri": '<path d="M12 3.5 21.5 20h-19Z"/>',
    "dia": '<path d="M12 2.5 21.5 12 12 21.5 2.5 12Z"/>',
    "cir": '<circle cx="12" cy="12" r="9.5"/>',
    "sq": '<rect x="3.5" y="3.5" width="17" height="17" rx="2.5"/>',
}


# The drifting shapes behind the lobby and the game.
BG = "".join('<i class="st-s-%s"></i>' % k for k in ("tri", "cir", "sq", "dia", "cir", "tri", "dia", "sq"))


# The bug of Bug Hunt, drawn in a 50 by 50 box: a green beetle seen from above.
BUG_ART = ('<path d="M14 20 6.5 15.5M12.5 28H4.5M14.5 36l-7 5.5M36 20l7.5-4.5M37.5 28h8M35.5 36l7 5.5" fill="none" '
           'stroke="#1E293B" stroke-width="2.6" stroke-linecap="round"/>'
           '<path d="M21 9.5C20 6 18 4.5 15.5 4M29 9.5C30 6 32 4.5 34.5 4" fill="none" stroke="#1E293B" stroke-width="2.2" '
           'stroke-linecap="round"/>'
           '<circle cx="25" cy="13.5" r="7" fill="#1E293B"/>'
           '<circle cx="22" cy="12" r="1.9" fill="#fff"/><circle cx="28" cy="12" r="1.9" fill="#fff"/>'
           '<ellipse cx="25" cy="30" rx="13" ry="15.5" fill="#84CC16" stroke="#1E293B" stroke-width="2.4"/>'
           '<path d="M25 15v30" stroke="#1E293B" stroke-width="2.2"/>'
           '<circle cx="19" cy="25" r="2.6" fill="#1E293B"/><circle cx="31" cy="25" r="2.6" fill="#1E293B"/>'
           '<circle cx="18.5" cy="35" r="2.2" fill="#1E293B"/><circle cx="31.5" cy="35" r="2.2" fill="#1E293B"/>'
           '<path d="M17.5 19.5c1.5-2 3.5-3 6-3.2" fill="none" stroke="#ECFCCB" stroke-width="2" stroke-linecap="round"/>')


# The brain of the brain games band: two halves and a bolt of lightning.
BRAIN_ART = ('<svg viewBox="0 0 64 56" aria-hidden="true" focusable="false">'
             '<path d="M30 6c-4-3-11-2-13 3-5-1-10 3-9 8-5 2-6 9-2 12-2 5 2 10 7 10 1 5 7 8 12 5 2 3 5 4 5 4V6Z" '
             'fill="#F9A8D4" stroke="#1E293B" stroke-width="2.4" stroke-linejoin="round"/>'
             '<path d="M34 6c4-3 11-2 13 3 5-1 10 3 9 8 5 2 6 9 2 12 2 5-2 10-7 10-1 5-7 8-12 5-2 3-5 4-5 4V6Z" '
             'fill="#F472B6" stroke="#1E293B" stroke-width="2.4" stroke-linejoin="round"/>'
             '<path d="M17 18c3 0 5 2 5 5M13 30c3-2 7-1 8 2M23 41c0-3 2-5 5-5M47 18c-3 0-5 2-5 5M51 30c-3-2-7-1-8 2'
             'M41 41c0-3-2-5-5-5" fill="none" stroke="#1E293B" stroke-width="2" stroke-linecap="round"/>'
             '<path d="M35.5 13 27 29.5h6.5l-3.2 12.5L41 25h-6.5l3.2-12Z" fill="#FDE047" stroke="#1E293B" '
             'stroke-width="2" stroke-linejoin="round"/></svg>')

# A cut diamond, for ratings out of three. Its facets are coloured by custom
# properties, so one drawing serves lit and unlit diamonds everywhere.
GEM_FACETS = ('<path d="M2 7.5 6.5 2h3L8 7.5Z" style="fill:var(--g2,#7DD3FC)"/>'
              '<path d="M9.5 2h5L16 7.5H8Z" style="fill:var(--g1,#E0F2FE)"/>'
              '<path d="M14.5 2h3L22 7.5h-6Z" style="fill:var(--g3,#38BDF8)"/>'
              '<path d="M2 7.5h6l4 13Z" style="fill:var(--g3,#38BDF8)"/>'
              '<path d="M8 7.5h8l-4 13Z" style="fill:var(--g2,#7DD3FC)"/>'
              '<path d="M16 7.5h6l-10 13Z" style="fill:var(--g4,#0284C7)"/>'
              '<path d="M6.5 2h11L22 7.5 12 20.5 2 7.5Z" fill="none" style="stroke:var(--g5,#075985)" stroke-width="1.3" '
              'stroke-linejoin="round"/>')
GEM_DEFS = ('<svg class="st-glyphs" width="0" height="0" aria-hidden="true" focusable="false">'
            '<symbol id="st-gem" viewBox="0 0 24 22">%s</symbol></svg>' % GEM_FACETS)


def _gem(cls="st-gem"):
    return '<svg class="%s" viewBox="0 0 24 22" aria-hidden="true" focusable="false"><use href="#st-gem"></use></svg>' % cls


def _round_icon(kind):
    """The drawn picture on each round's card."""
    if kind == "blitz":
        cells = [("tri", "#D7263D", "#fff", 0, 0), ("dia", "#1F5FD1", "#fff", 26, 0),
                 ("cir", "#F2B705", "#1F1A05", 0, 26), ("sq", "#1E7B34", "#fff", 26, 26)]
        inner = "".join('<g transform="translate(%d %d)"><rect width="24" height="24" rx="6" fill="%s"/>'
                        '<g transform="translate(4 4) scale(.67)" fill="%s">%s</g></g>' % (x, y, c, ink, SHAPES[s])
                        for s, c, ink, x, y in cells)
        return '<svg viewBox="0 0 50 50" aria-hidden="true" focusable="false">%s</svg>' % inner
    if kind == "short":
        return ('<svg viewBox="0 0 50 50" aria-hidden="true" focusable="false">'
                '<rect x="3" y="6" width="44" height="30" rx="9" fill="#FDE68A" stroke="#1E293B" stroke-width="2.4"/>'
                '<path d="M13 36 9 45 21 36Z" fill="#FDE68A" stroke="#1E293B" stroke-width="2.4" stroke-linejoin="round"/>'
                '<path d="M12 16h18M12 25h12" stroke="#1E293B" stroke-width="3" stroke-linecap="round"/>'
                '<path d="M33 27 41 12l4 2-8 15-5 2Z" fill="#F97316" stroke="#1E293B" stroke-width="2" stroke-linejoin="round"/>'
                '</svg>')
    return ('<svg viewBox="0 0 50 50" aria-hidden="true" focusable="false">'
            '<path d="M25 7a13 13 0 0 0-7.5 23.6c1.6 1.2 2.5 2.8 2.5 4.6V37h10v-1.8c0-1.8.9-3.4 2.5-4.6A13 13 0 0 0 25 7Z" '
            'fill="#C4B5FD" stroke="#1E293B" stroke-width="2.4" stroke-linejoin="round"/>'
            '<path d="M20 41h10M21.5 45h7" stroke="#1E293B" stroke-width="2.6" stroke-linecap="round"/>'
            '<path d="M21 20c1-3 3-4.5 5.5-4.5" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/>'
            '<path d="M5 20H1.5M48.5 20H45M9 6.5 6.5 4M41 6.5 43.5 4M25 2.5V0" stroke="#F59E0B" stroke-width="2.6" '
            'stroke-linecap="round"/></svg>')


def _task_icon(task):
    """The drawn picture on each task's card: the quiz's four shapes, Pixel's
    head for This or That, two playing cards for Memory Match, two boxes for
    Sort It, a board of letter tiles for Code Word, four joined tiles for Link
    Up and a beetle for Bug Hunt."""
    if task == "quiz":
        return _round_icon("blitz")
    if task == "cat":
        head = cat.flat(head_only=True, cls="st-cat-head")
        return head.replace(' role="img" aria-label="Pixel the robot cat"', ' aria-hidden="true" focusable="false"')
    if task == "word":
        # A board of letter tiles: two guesses closing in, then the word found.
        rows = [("#64748B", "#F59E0B", "#64748B"), ("#F59E0B", "#16A34A", "#64748B"), ("#16A34A", "#16A34A", "#16A34A")]
        tiles = "".join('<rect x="%d" y="%d" width="13" height="13" rx="3.2" fill="%s" stroke="#1E293B" stroke-width="1.8"/>'
                        % (3.5 + 15 * c, 3.5 + 15 * r, colour) for r, row in enumerate(rows) for c, colour in enumerate(row))
        return ('<svg viewBox="0 0 50 50" aria-hidden="true" focusable="false">%s'
                '<path d="M7.2 40.2l2.3 2.3 4-4.4M22.2 40.2l2.3 2.3 4-4.4M37.2 40.2l2.3 2.3 4-4.4" fill="none" stroke="#fff" '
                'stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>' % tiles)
    if task == "link":
        # Four tiles that belong together, joined by a ring, with a tick where they meet.
        return ('<svg viewBox="0 0 50 50" aria-hidden="true" focusable="false">'
                '<path d="M14 14h22v22H14Z" fill="none" stroke="#F59E0B" stroke-width="4" stroke-linejoin="round"/>'
                '<rect x="5" y="5" width="18" height="18" rx="4.5" fill="#DC2626" stroke="#1E293B" stroke-width="2.2"/>'
                '<rect x="27" y="5" width="18" height="18" rx="4.5" fill="#DC2626" stroke="#1E293B" stroke-width="2.2"/>'
                '<rect x="5" y="27" width="18" height="18" rx="4.5" fill="#DC2626" stroke="#1E293B" stroke-width="2.2"/>'
                '<rect x="27" y="27" width="18" height="18" rx="4.5" fill="#DC2626" stroke="#1E293B" stroke-width="2.2"/>'
                '<path d="M10 14h8M32 14h8M10 36h8M32 36h8" stroke="#fff" stroke-width="2.6" stroke-linecap="round"/>'
                '<circle cx="25" cy="25" r="6.5" fill="#FDE047" stroke="#1E293B" stroke-width="2.2"/>'
                '<path d="M22 25.2l2.2 2.2 3.9-4.2" fill="none" stroke="#1E293B" stroke-width="2.2" stroke-linecap="round" '
                'stroke-linejoin="round"/></svg>')
    if task == "bug":
        return ('<svg viewBox="0 0 50 50" aria-hidden="true" focusable="false">%s</svg>' % BUG_ART)
    if task == "odd":
        # Three violet tiles that match, and one amber tile that does not, tipped out of line.
        same = "".join('<rect x="%d" y="%d" width="19" height="19" rx="5" fill="#7C3AED" stroke="#1E293B" stroke-width="2.2"/>'
                       '<circle cx="%.1f" cy="%.1f" r="4.6" fill="#fff"/>' % (x, y, x + 9.5, y + 9.5)
                       for x, y in ((4, 4), (4, 27), (27, 27)))
        return ('<svg viewBox="0 0 50 50" aria-hidden="true" focusable="false">%s'
                '<g transform="rotate(14 36.5 13)"><rect x="27" y="3.5" width="19" height="19" rx="5" fill="#F59E0B" '
                'stroke="#1E293B" stroke-width="2.2"/><path d="M36.5 8.2l5 8.6h-10Z" fill="#fff"/></g>'
                '<path d="M25 22.5l1 2.2 2.2 1-2.2 1-1 2.2-1-2.2-2.2-1 2.2-1Z" fill="#FDE047" stroke="#1E293B" '
                'stroke-width=".9"/></svg>' % same)
    if task == "flash":
        # A card face down, and one turned over in a flash.
        return ('<svg viewBox="0 0 50 50" aria-hidden="true" focusable="false">'
                '<g transform="rotate(-10 17 26)"><rect x="5" y="10" width="23" height="31" rx="5" fill="#0891B2" '
                'stroke="#1E293B" stroke-width="2.2"/><rect x="9" y="14" width="15" height="23" rx="3" fill="none" '
                'stroke="#fff" stroke-opacity=".55" stroke-width="1.6" stroke-dasharray="3 2"/></g>'
                '<g transform="rotate(9 33 25)"><rect x="21" y="9" width="23" height="31" rx="5" fill="#fff" '
                'stroke="#1E293B" stroke-width="2.2"/><path d="M34.5 13.5 27 26h5.2l-2.6 9.5 8.4-13.6h-5.7Z" '
                'fill="#FDE047" stroke="#1E293B" stroke-width="1.7" stroke-linejoin="round"/></g>'
                '<path d="M44.5 7.5l3-3M46 13.5h3.5M40.5 3.5 41.5.8" stroke="#F59E0B" stroke-width="2.4" '
                'stroke-linecap="round"/></svg>')
    if task == "fib":
        # A statement card with a red fib stamp and a green fact stamp.
        return ('<svg viewBox="0 0 50 50" aria-hidden="true" focusable="false">'
                '<rect x="5" y="3.5" width="40" height="27" rx="6" fill="#fff" stroke="#1E293B" stroke-width="2.2"/>'
                '<path d="M11.5 11.5h27M11.5 17.5h21M11.5 23.5h14" stroke="#1E293B" stroke-width="2.6" stroke-linecap="round"/>'
                '<circle cx="14" cy="38.5" r="9" fill="#DC2626" stroke="#1E293B" stroke-width="2.2"/>'
                '<path d="M10.6 35.1l6.8 6.8M17.4 35.1l-6.8 6.8" stroke="#fff" stroke-width="2.8" stroke-linecap="round"/>'
                '<circle cx="36" cy="38.5" r="9" fill="#16A34A" stroke="#1E293B" stroke-width="2.2"/>'
                '<path d="M31.8 38.7l3 3 5.4-5.8" fill="none" stroke="#fff" stroke-width="2.8" stroke-linecap="round" '
                'stroke-linejoin="round"/></svg>')
    if task == "run":
        # The silver robot cat's head at speed, a neon arch behind it: tall
        # ears with panels of cyan lights, and goggles with pixel eyes.
        return ('<svg viewBox="0 0 50 50" aria-hidden="true" focusable="false">'
                '<path d="M30 48V24a9 9 0 0 1 18 0v24" fill="none" stroke="#E879F9" stroke-width="3"/>'
                '<path d="M33.5 48V25a5.5 5.5 0 0 1 11 0v23" fill="none" stroke="#22D3EE" stroke-width="2"/>'
                '<path d="M1.5 22h5M0.5 29h5.5M1.5 36h4.5" stroke="#22D3EE" stroke-width="2.6" stroke-linecap="round"/>'
                '<path d="M10.5 25 11.8 5Q12.4 3 14.2 4.4L24.5 14Z" fill="#D5D8EA" stroke="#2A2D4A" stroke-width="2" '
                'stroke-linejoin="round"/>'
                '<path d="M13.6 20.5 14.3 8.8 20.8 14.6Z" fill="#67E8F9"/>'
                '<path d="M39.5 25 38.2 5Q37.6 3 35.8 4.4L25.5 14Z" fill="#D5D8EA" stroke="#2A2D4A" stroke-width="2" '
                'stroke-linejoin="round"/>'
                '<path d="M36.4 20.5 35.7 8.8 29.2 14.6Z" fill="#67E8F9"/>'
                '<path d="M14.6 18.6h3M14.6 15.6h4.2M14.8 12.6h3M35.4 18.6h-3M35.4 15.6h-4.2M35.2 12.6h-3" stroke="#0E7490" '
                'stroke-width=".9" stroke-dasharray="1 1"/>'
                '<ellipse cx="25" cy="29.5" rx="17" ry="14.5" fill="#CDD0E3" stroke="#2A2D4A" stroke-width="2.2"/>'
                '<path d="M12.5 22.5Q25 14.5 37.5 22.5" fill="none" stroke="#8A8EAE" stroke-width="1.6"/>'
                '<ellipse cx="18" cy="19.6" rx="5" ry="2" fill="#F4F5FB" opacity=".8"/>'
                '<circle cx="18.6" cy="30.5" r="6.4" fill="#5A5F86" stroke="#2A2D4A" stroke-width="1.6"/>'
                '<circle cx="18.6" cy="30.5" r="4.4" fill="#071420"/>'
                '<circle cx="31.4" cy="30.5" r="6.4" fill="#5A5F86" stroke="#2A2D4A" stroke-width="1.6"/>'
                '<circle cx="31.4" cy="30.5" r="4.4" fill="#071420"/>'
                '<path d="M16.6 28.2v4.6M20.6 28.2v4.6M16.6 30.5h4M29.4 28.2v4.6M33.4 28.2v4.6M29.4 30.5h4" stroke="#67E8F9" '
                'stroke-width="1.4" stroke-linecap="round"/>'
                '<path d="M23.6 37.2h2.8L25 38.8Z" fill="#3B3346" stroke="#3B3346" stroke-width="1" stroke-linejoin="round"/>'
                '<path d="M12.5 37.5 6 36.5M12.5 39.5 6.5 41M37.5 37.5 44 36.5M37.5 39.5 43.5 41" stroke="#7A7E9E" '
                'stroke-width="1" stroke-linecap="round"/>'
                '</svg>')
    if task == "sort":
        return ('<svg viewBox="0 0 50 50" aria-hidden="true" focusable="false">'
                '<path d="M2.5 30h19.5l-2.3 16.5H4.8Z" fill="#F97316" stroke="#1E293B" stroke-width="2.2" stroke-linejoin="round"/>'
                '<path d="M28 30h19.5l-2.3 16.5H30.3Z" fill="#1F5FD1" stroke="#1E293B" stroke-width="2.2" stroke-linejoin="round"/>'
                '<path d="M7 35.5h10.5M32.5 35.5H43" stroke="#fff" stroke-opacity=".65" stroke-width="2" stroke-linecap="round"/>'
                '<g transform="rotate(-12 21 13)"><rect x="9" y="4" width="24" height="17" rx="3.5" fill="#fff" '
                'stroke="#1E293B" stroke-width="2.2"/><path d="M14 10h14M14 15h9" stroke="#1E293B" stroke-width="2.4" '
                'stroke-linecap="round"/></g>'
                '<path d="M34 15.5c5.5 0 8.4 3.8 8.4 9.4" fill="none" stroke="#16A34A" stroke-width="3" stroke-linecap="round"/>'
                '<path d="M38.4 22.6l4 4.4 4-4.4" fill="none" stroke="#16A34A" stroke-width="3" stroke-linecap="round" '
                'stroke-linejoin="round"/></svg>')
    return ('<svg viewBox="0 0 50 50" aria-hidden="true" focusable="false">'
            '<g transform="rotate(-11 17 27)"><rect x="4" y="9" width="25" height="33" rx="5" fill="#1F5FD1" '
            'stroke="#1E293B" stroke-width="2.2"/><rect x="8" y="13" width="17" height="25" rx="3" fill="none" '
            'stroke="#fff" stroke-opacity=".5" stroke-width="1.6" stroke-dasharray="3 2"/>'
            '<path d="M13.4 21.6a3.6 3.6 0 1 1 5 3.3c-1.1.5-1.6 1.2-1.6 2.4" fill="none" stroke="#fff" stroke-width="2.6" '
            'stroke-linecap="round"/><circle cx="16.8" cy="31.4" r="1.6" fill="#fff"/></g>'
            '<g transform="rotate(9 33 25)"><rect x="21" y="8" width="25" height="33" rx="5" fill="#fff" '
            'stroke="#1E293B" stroke-width="2.2"/><path d="M26.5 17h14M26.5 23h10M26.5 29h12" stroke="#1E293B" '
            'stroke-width="2.6" stroke-linecap="round"/></g>'
            '<circle cx="40" cy="40" r="7.5" fill="#16A34A" stroke="#fff" stroke-width="2.2"/>'
            '<path d="M36.4 40.2l2.5 2.5 4.6-4.8" fill="none" stroke="#fff" stroke-width="2.4" stroke-linecap="round" '
            'stroke-linejoin="round"/></svg>')


# City Run's picture: the silver robot cat standing, sprinting and skating
# away on its inline skates, for its band in the lobby and the start of a run.
RUN_ART = ('<img class="st-run-shot" src="/assets/img/city-run-cat.jpg" width="1144" height="560" alt="" '
           'loading="lazy" decoding="async">')


def ks3_records():
    """Every Key Stage 3 stretch task in teaching order, with what its pages need to know."""
    topics = {t.slug: (u, t) for u in ks3.COURSE.units for t in u.topics}
    out = []
    for slug, lessons in ks3_stretch.units():
        unit, topic = topics[slug]
        for n, st in enumerate(lessons, 1):
            sec = next(s for s in topic.sections if s.title == st.lesson)
            url = "%s%s/lesson-%d/" % (HUB, slug, n)
            out.append({
                "stage": "ks3", "stretch": st, "topic": topic, "unit": unit, "n": n, "title": st.lesson,
                "key": "%s/%d" % (slug, n), "url": url,
                "lesson_url": "/ks3/%s/#%s" % (slug, sec.id or slugify(sec.title)),
                "year": unit.title,
                "kicker": [unit.title, "%s %s" % (topic.spec, topic.title), "Lesson %d" % n],
                "where": "%s %s, lesson %d" % (topic.spec, topic.title, n),
                "trail": [("Home", "/"), ("Key Stage 3", "/ks3/"), (HUB_TITLE, HUB),
                          (topic.title, "%s#%s" % (HUB, slug)), ("Lesson %d" % n, None)],
                "hub": HUB, "active": "/ks3/", "level": "Key Stage 3, %s" % unit.title,
                "course_name": ks3.COURSE.title, "course_url": "/ks3/",
                "desc": _desc("%s (%s, lesson %d)" % (st.lesson, topic.title, n),
                              "ten stretch games: a quiz, This or That, Memory Match, Code Word, Link Up, Bug Hunt, "
                              "three brain games and City Run." if st.words else
                              "a quiz challenge, This or That with Pixel the cat, and Memory Match.",
                              "ten stretch games, from a quiz to City Run, a neon city race." if st.words
                              else "three stretch games."),
            })
    return out


def ks4_records():
    """Every Key Stage 4 stretch task, course by course in teaching order."""
    out = []
    for key, slug, name, lessons in ks4_stretch.courses():
        course = _ks4_course(slug)
        topics = {t.slug: (u, t) for u in course.units for t in u.topics}
        order = list(topics)
        unknown = [st.lesson for st in lessons if st.lesson not in topics]
        if unknown:
            raise SystemExit("content/ks4_stretch: %s has no topic called %s" % (slug, ", ".join(unknown)))
        for n, st in enumerate(sorted(lessons, key=lambda st: order.index(st.lesson)), 1):
            unit, topic = topics[st.lesson]
            out.append({
                "stage": "ks4", "stretch": st, "topic": topic, "unit": unit, "n": n, "title": topic.title,
                "course": course, "ckey": key, "cname": name,
                "key": "ks4/%s/%s" % (key, topic.slug), "url": "%s%s/%s/" % (HUB4, key, topic.slug),
                "lesson_url": "/%s/%s/" % (slug, topic.slug),
                "kicker": [name, unit.title],
                "where": "%s %s" % (course.code, topic.spec),
                "trail": [("Home", "/"), (course.short, "/%s/" % slug), (HUB_TITLE, "%s#%s" % (HUB4, key)),
                          (topic.title, None)],
                "hub": HUB4, "active": "/%s/" % slug, "level": "Key Stage 4, %s" % name,
                "course_name": course.title, "course_url": "/%s/" % slug,
                "desc": _desc(topic.title if topic.title.startswith(topic.spec)
                              else "%s (%s %s)" % (topic.title, course.board, topic.spec),
                              "ten stretch games: a quiz, This or That, Memory Match, Sort It, Code Word, Link Up, "
                              "Bug Hunt and three brain games." if st.words else
                              "a quiz challenge, This or That with Pixel the cat, Memory Match and Sort It.",
                              "ten stretch games, from a quiz to three brain games." if st.words else "four stretch games."),
            })
    return out


def records():
    """Every stretch task on the site: Key Stage 3, then Key Stage 4."""
    return ks3_records() + ks4_records()


def attach_links():
    """Link the lessons to their stretch tasks, before the topic pages are built.

    A Key Stage 3 lesson ends with a link to its own; a Key Stage 4 topic
    closes with one, and its course's page gets a button to the hub."""
    recs = records()
    for r in recs:
        if r["stage"] == "ks3":
            links = getattr(r["topic"], "stretch", None)
            if links is None:
                links = r["topic"].stretch = {}
            links[r["stretch"].lesson] = (r["url"], r["n"])
        else:
            r["topic"].stretch_all = r["url"]
            r["course"].extra_cta = ("Stretch tasks", "%s#%s" % (HUB4, r["ckey"]), "i-target")
    link = ("KS4 stretch tasks", HUB4)
    if any(r["stage"] == "ks4" for r in recs) and link not in render.PRACTISE_LINKS:
        render.PRACTISE_LINKS.append(link)


def check():
    """Prove every task, and that every lesson has one: every Key Stage 3
    lesson, and every lesson of a published Key Stage 4 course."""
    units = ks3_stretch.units()
    topics = {t.slug: t for u in ks3.COURSE.units for t in u.topics}
    stretchcheck.validate(units, topics)
    have = {(slug, st.lesson) for slug, lessons in units for st in lessons}
    missing = []
    for u in ks3.COURSE.units:
        for t in u.topics:
            for s in t.sections:
                if (t.slug, s.title) not in have and (t.slug, s.title) not in ks3_stretch.NOT_LESSONS:
                    missing.append("%s: %s" % (t.slug, s.title))
    if ks3_stretch.GAMES_COMPLETE:
        missing += ["%s: %s has no Code Word, Link Up and Bug Hunt" % (slug, st.lesson)
                    for slug, lessons in units for st in lessons if not st.words]
    lessons4, topics4 = [], {}
    for key, slug, name, lessons in ks4_stretch.courses():
        course = _ks4_course(slug)
        mine = [t.slug for u in course.units for t in u.topics]
        topics4.update({(slug, t.slug): t for u in course.units for t in u.topics})
        lessons4 += [(slug, st) for st in lessons]
        if ks4_stretch.complete(slug):
            done = {st.lesson for st in lessons}
            missing += ["%s: %s" % (slug, t) for t in mine if t not in done and (slug, t) not in ks4_stretch.NOT_LESSONS]
        if ks4_stretch.games_complete(slug):
            missing += ["%s: %s has no Code Word, Link Up and Bug Hunt" % (slug, st.lesson)
                        for st in lessons if not st.words]
    stretchcheck.validate_ks4(lessons4, topics4)
    brain = brain_games.check(records())
    if brain:
        raise SystemExit("The brain games failed their checks:\n  " + "\n  ".join(brain))
    run = city_run.check(records(), _has_run)
    if run:
        raise SystemExit("City Run failed its checks:\n  " + "\n  ".join(run))
    return missing


# ------------------------------------------------------------------ payload

def _code(code, lang):
    if not code:
        return ""
    if lang in ("python", "pseudo"):
        return markup._highlight(code.strip("\n"), lang)
    return esc(code.strip("\n"))


def _seconds(b):
    t = b.time or TIME[b.kind]
    if not b.time:
        if b.code:
            t += 10 + 5 * max(0, b.code.count("\n") - 3)
        if len(b.q) > 140:
            t += 5
    return t


def _blitz(b):
    d = {"k": b.kind, "q": markup.inline(b.q), "x": markup.inline(b.explain), "t": _seconds(b)}
    if b.code:
        d["c"] = _code(b.code, b.lang)
    if b.kind in ("choice", "multi", "order"):
        d["o"] = [markup.inline(o) for o in b.options]
    if b.kind == "multi":
        d["n"] = b.n
    if b.kind == "tf":
        d["a"] = bool(b.answer)
    if b.kind == "type":
        d["a"] = list(b.accept)
    return d


def _written(w):
    d = {"q": markup.inline(w.q), "m": w.marks, "cmd": w.command,
         "p": [{"t": markup.inline(p.text), "a": p.any} for p in w.points],
         "model": markup.model(w.model)}
    if w.frame:
        d["f"] = list(w.frame)
    if w.code:
        d["c"] = _code(w.code, w.lang)
    return d


def _pick(p):
    d = {"q": markup.inline(p.q), "r": markup.inline(p.right), "w": markup.inline(p.wrong), "x": markup.inline(p.why)}
    if p.code:
        d["c"] = _code(p.code, p.lang)
    return d


def payload(r, nxt):
    st = r["stretch"]
    d = {
        # Inside the games a title is written without dashes, as all game text is
        "key": r["key"], "lesson": brain_games.tidy(r["title"]), "where": r["where"],
        "back": r["lesson_url"],
        "next": {"t": brain_games.tidy(nxt["title"]), "u": nxt["url"]} if nxt else None,
        "blitz": [_blitz(b) for b in st.blitz],
        "short": [_written(w) for w in st.short],
        "long": [_written(w) for w in st.long],
        "picks": [_pick(p) for p in st.picks],
        "pairs": [{"a": markup.inline(p.a), "b": markup.inline(p.b)} for p in st.pairs],
        "pn": list(st.pair_names),
    }
    if st.sort:
        d["sort"] = {"p": markup.inline(st.sort.prompt), "b": [markup.inline(b) for b in st.sort.bins],
                     "i": [{"t": markup.inline(i.text), "b": i.bin, "x": markup.inline(i.why)} for i in st.sort.items]}
    if st.words:
        d["words"] = [{"w": w.word, "c": markup.inline(w.clue)} for w in st.words]
    if st.groups:
        d["link"] = [{"n": markup.inline(g.name), "t": [markup.inline(t) for t in g.tiles]} for g in st.groups]
    if st.bugs:
        d["bugs"] = [{"t": [markup.inline(t) for t in b.truths], "b": markup.inline(b.bug), "x": markup.inline(b.fix)}
                     for b in st.bugs]
    if any(t == "odd" for t, _ in _tasks(r)):
        # Odd One Out: for each group, the tiles of other groups that may be the odd one out among three of its tiles
        d["odd"] = [[[g, t] for g, t in ok] for ok in brain_games.odd_intruders(r["key"], st)]
        # Fact or Fib: every statement it may deal, whether it is true, and the fix or explanation
        d["fib"] = [{"s": markup.inline(t), "t": 1 if ok else 0, "x": markup.inline(why)}
                    for t, ok, why in brain_games.fib_deck(st)]
        # Memory Flash: its question, the cards at each level, and the pairs it plays
        fp = brain_games.flash_pairs(r["key"], st)
        d["flash"] = {"q": brain_games.flash_ask(st), "l": brain_games.flash_levels(len(fp)),
                      "p": [{"a": markup.inline(a), "b": markup.inline(b)} for a, b in fp]}
    if _has_run(r):
        # City Run: the quiz's and This or That's questions it may ask, the right
        # answer first, and how many of each kind a run asks. Its statements and
        # pairs are Fact or Fib's and Memory Flash's, above.
        def opt(t):
            return markup.inline(t)
        d["run"] = {
            "c": [dict({"q": opt(q), "o": [opt(right)] + [opt(w) for w in wrongs], "x": opt(why)},
                       **({"c": _code(code, lang)} if code else {}))
                  for q, right, wrongs, why, code, lang in city_run.choices(st)],
            "p": [dict({"q": opt(q), "o": [opt(right), opt(wrong)], "x": opt(why)},
                       **({"c": _code(code, lang)} if code else {}))
                  for q, right, wrong, why, code, lang in city_run.picks(st)],
            "n": city_run.QUESTIONS, "mix": [list(m) for m in city_run.MIX], "d": list(city_run.DISTRICTS),
        }
    return d


# -------------------------------------------------------------- the sheet

def _sheet_code(code, lang):
    return '<pre class="st-sheet-code"><code>%s</code></pre>' % _code(code, lang) if code else ""


def _sheet(r):
    """The whole task as a worksheet, with its answers after it."""
    st = r["stretch"]
    qs, keys = [], []
    for i, b in enumerate(st.blitz, 1):
        body = ""
        if b.kind in ("choice", "multi"):
            body = '<ul class="st-sheet-opts">%s</ul>' % "".join(
                "<li><span class=\"st-box\"></span><span>%s</span></li>" % markup.inline(o) for o in _sheet_order(b))
            if b.kind == "multi":
                body = '<p class="st-sheet-hint">Tick %d.</p>' % b.n + body
        elif b.kind == "tf":
            body = '<ul class="st-sheet-opts st-sheet-tf"><li><span class="st-box"></span>True</li><li><span class="st-box"></span>False</li></ul>'
        elif b.kind == "order":
            body = ('<p class="st-sheet-hint">Number these 1 to %d.</p><ul class="st-sheet-opts">%s</ul>'
                    % (len(b.options), "".join("<li><span class=\"st-box\"></span><span>%s</span></li>" % markup.inline(o)
                                               for o in _sheet_order(b))))
        else:
            body = '<p class="st-line"></p>'
        qs.append('<li class="st-sheet-q"><p>%s</p>%s%s</li>' % (markup.inline(b.q), _sheet_code(b.code, b.lang), body))
        if b.kind == "choice":
            ans = markup.inline(b.options[0])
        elif b.kind == "multi":
            ans = "; ".join(markup.inline(o) for o in b.options[:b.n])
        elif b.kind == "tf":
            ans = "True" if b.answer else "False"
        elif b.kind == "order":
            ans = " &rarr; ".join(markup.inline(o) for o in b.options)
        else:
            ans = esc(b.accept[0])
        keys.append("<li><b>%s</b> %s</li>" % (ans, markup.inline(b.explain)))

    def written(items, lines):
        out, key = [], []
        for w in items:
            out.append('<li class="st-sheet-q"><p>%s <span class="st-sheet-marks">[%d mark%s]</span></p>%s%s</li>'
                       % (markup.inline(w.q), w.marks, "" if w.marks == 1 else "s", _sheet_code(w.code, w.lang),
                          '<p class="st-line"></p>' * lines))
            key.append('<li><ul class="st-sheet-ms">%s</ul><div class="st-sheet-model"><b>Model answer</b>%s</div></li>'
                       % ("".join("<li>%s</li>" % markup.inline(p.text) for p in w.points), markup.model(w.model)))
        return "".join(out), "".join(key)

    sq, sk = written(st.short, 3)
    lq, lk = written(st.long, 9)

    picks, pick_keys = [], []
    for p in st.picks:
        two = [p.right, p.wrong] if _seed(p.q) % 2 else [p.wrong, p.right]
        picks.append('<li class="st-sheet-q"><p>%s</p>%s<ul class="st-sheet-opts st-sheet-tf">%s</ul></li>'
                     % (markup.inline(p.q), _sheet_code(p.code, p.lang),
                        "".join('<li><span class="st-box"></span><span>%s</span></li>' % markup.inline(o) for o in two)))
        pick_keys.append("<li><b>%s</b> %s</li>" % (markup.inline(p.right), markup.inline(p.why)))

    # Meanings in a fixed order in which none sits beside its own word.
    n_pairs = len(st.pairs)
    mixed = sorted(range(n_pairs), key=lambda i: _seed(st.pairs[i].b))
    order = next((mixed[r:] + mixed[:r] for r in range(n_pairs)
                  if all(i != k for k, i in enumerate(mixed[r:] + mixed[:r]))),
                 [(k + 1) % n_pairs for k in range(n_pairs)])
    letters = "ABCDEFGH"
    rows = "".join('<tr><td><b>%s</b> %s</td><td><b>%d</b> %s</td></tr>'
                   % (letters[k], markup.inline(st.pairs[k].a), n + 1, markup.inline(st.pairs[i].b))
                   for n, (k, i) in enumerate(zip(range(len(st.pairs)), order)))
    match_key = "".join("<li><b>%s %d</b> %s: %s</li>" % (letters[k], order.index(k) + 1, markup.inline(p.a), markup.inline(p.b))
                        for k, p in enumerate(st.pairs))
    word, meaning = (_in_sentence(n) for n in st.pair_names)
    sort_q, sort_k = _sheet_sort(st.sort) if st.sort else ("", "")
    if st.words:
        games_q, games_k = _sheet_games(st)
        sort_q, sort_k = sort_q + games_q, sort_k + games_k
    if any(t == "odd" for t, _ in _tasks(r)):
        brain_q, brain_k = _sheet_brain(r)
        sort_q, sort_k = sort_q + brain_q, sort_k + brain_k
    if _has_run(r):
        sort_q += ('<h3>City Run</h3><p class="st-sheet-hint">City Run is a race through a neon cyber city, played on screen. '
                   'It asks %d of the questions above, from the quiz, This or That, Memory Flash and Fact or Fib.</p>'
                   % city_run.QUESTIONS)
    return """<section class="st-sheet" id="st-sheet" aria-labelledby="st-sheet-title">
  <h2 id="st-sheet-title">%s: the questions</h2>
  <h3>Quiz Challenge, round 1: Quiz Blitz</h3><ol class="st-sheet-list">%s</ol>
  <h3>Quiz Challenge, round 2: Quick Fire</h3><ol class="st-sheet-list">%s</ol>
  <h3>Quiz Challenge, round 3: Big Think</h3><ol class="st-sheet-list">%s</ol>
  <h3>This or That: tick the right answer</h3><ol class="st-sheet-list">%s</ol>
  <h3>Memory Match: match each %s to its %s</h3>
  <table class="st-sheet-match"><thead><tr><th scope="col">%s</th><th scope="col">%s</th></tr></thead><tbody>%s</tbody></table>
  %s
  <details class="st-key" id="st-key">
    <summary>Answers</summary>
    <h3>Round 1: Quiz Blitz</h3><ol class="st-sheet-list">%s</ol>
    <h3>Round 2: Quick Fire</h3><ol class="st-sheet-list">%s</ol>
    <h3>Round 3: Big Think</h3><ol class="st-sheet-list">%s</ol>
    <h3>This or That</h3><ol class="st-sheet-list">%s</ol>
    <h3>Memory Match</h3><ul class="st-sheet-list st-sheet-pairs">%s</ul>
    %s
  </details>
</section>""" % (esc(r["title"]), "".join(qs), sq, lq, "".join(picks), esc(word), esc(meaning),
                 esc(st.pair_names[0]), esc(st.pair_names[1]), rows, sort_q,
                 "".join(keys), sk, lk, "".join(pick_keys), match_key, sort_k)


def _sheet_sort(so):
    """Sort It on paper: a table with a box to tick in each row, as GCSE papers set it."""
    order = sorted(range(len(so.items)), key=lambda i: _seed(so.items[i].text))
    head = "".join('<th scope="col">%s</th>' % markup.inline(b) for b in so.bins)
    tick = '<td class="st-sheet-tick"><span class="st-box"></span></td>' * len(so.bins)
    rows = "".join("<tr><td>%s</td>%s</tr>" % (markup.inline(so.items[i].text), tick) for i in order)
    q = ('<h3>Sort It: tick one box in each row</h3><p class="st-sheet-hint">%s</p>'
         '<table class="st-sheet-sort"><thead><tr><th scope="col">Statement</th>%s</tr></thead><tbody>%s</tbody></table>'
         % (markup.inline(so.prompt), head, rows))
    key = ('<h3>Sort It</h3><ol class="st-sheet-list">%s</ol>'
           % "".join("<li><b>%s</b> %s %s</li>" % (markup.inline(so.bins[so.items[i].bin]), markup.inline(so.items[i].text),
                                                  markup.inline(so.items[i].why)) for i in order))
    return q, key


def _sheet_games(st):
    """Code Word, Link Up and Bug Hunt on paper: a clue and a box for each
    letter, twelve tiles to copy into three groups, and a box to tick beside
    the statement that is wrong."""
    words = "".join('<li class="st-sheet-q"><p>%s <span class="st-sheet-marks">(%d letters)</span></p>'
                    '<p class="st-letters" aria-hidden="true">%s</p></li>'
                    % (markup.inline(w.clue), len(w.word), "<span></span>" * len(w.word)) for w in st.words)
    word_key = "".join("<li><b>%s</b> %s</li>" % (esc(w.word), markup.inline(w.clue)) for w in st.words)

    tiles = sorted((t for g in st.groups for t in g.tiles), key=_seed)
    n, each = len(st.groups), len(st.groups[0].tiles)
    rows = "".join('<tr><th scope="row">Group %d</th><td></td><td></td></tr>' % (k + 1) for k in range(n))
    link = ('<p class="st-sheet-hint">These %d tiles make %d groups of %d. Write each group in the table, and what '
            'links its tiles.</p><ul class="st-sheet-tiles">%s</ul>'
            '<table class="st-sheet-link"><thead><tr><th scope="col">Group</th><th scope="col">The %d tiles</th>'
            '<th scope="col">What links them</th></tr></thead><tbody>%s</tbody></table>'
            % (len(tiles), n, each, "".join("<li>%s</li>" % markup.inline(t) for t in tiles), each, rows))
    link_key = "".join("<li><b>%s</b> %s</li>" % (markup.inline(g.name), "; ".join(markup.inline(t) for t in g.tiles))
                       for g in st.groups)

    bugs, bug_key = [], []
    for b in st.bugs:
        three = sorted(list(b.truths) + [b.bug], key=_seed)
        bugs.append('<li class="st-sheet-q"><ul class="st-sheet-opts">%s</ul></li>'
                    % "".join('<li><span class="st-box"></span><span>%s</span></li>' % markup.inline(t) for t in three))
        bug_key.append("<li><b>%s</b> %s</li>" % (markup.inline(b.bug), markup.inline(b.fix)))

    q = ('<h3>Code Word: write the word that fits each clue</h3><ol class="st-sheet-list">%s</ol>'
         '<h3>Link Up: find the three groups</h3>%s'
         '<h3>Bug Hunt: tick the statement that is wrong</h3>'
         '<p class="st-sheet-hint">In each set, two statements are true and one has a mistake in it.</p>'
         '<ol class="st-sheet-list">%s</ol>'
         % (words, link, "".join(bugs)))
    key = ('<h3>Code Word</h3><ol class="st-sheet-list">%s</ol>'
           '<h3>Link Up</h3><ul class="st-sheet-list st-sheet-pairs">%s</ul>'
           '<h3>Bug Hunt: the wrong statement, and why</h3><ol class="st-sheet-list">%s</ol>'
           % (word_key, link_key, "".join(bug_key)))
    return q, key


def _sheet_brain(r):
    """The brain games on paper: six odd ones out to circle, a word to write
    for each meaning from memory, and twelve statements to mark fact or fib.
    The choices are fixed by the lesson, so a printout always matches its key."""
    st = r["stretch"]
    intruders = brain_games.odd_intruders(r["key"], st)
    usable = [b for b, ok in enumerate(intruders) if ok]
    rounds, seen = [], set()
    k = 0
    while len(rounds) < 6 and k < 60:
        b = usable[k % len(usable)]
        seed = _seed("%s odd %d" % (r["key"], k))
        k += 1
        keep = [i for i in range(len(st.groups[b].tiles)) if i != seed % len(st.groups[b].tiles)]
        g, t = intruders[b][(seed // 7) % len(intruders[b])]
        key = (b, tuple(keep), g, t)
        if key in seen:
            continue
        seen.add(key)
        four = [st.groups[b].tiles[i] for i in keep] + [st.groups[g].tiles[t]]
        rounds.append((b, g, st.groups[g].tiles[t], sorted(four, key=_seed)))
    odd_q = "".join('<li class="st-sheet-q"><ul class="st-sheet-opts st-sheet-four">%s</ul>'
                    '<p class="st-sheet-hint">What links the other three?</p><p class="st-line"></p></li>'
                    % "".join('<li><span class="st-box"></span><span>%s</span></li>' % markup.inline(x) for x in four)
                    for _, _, _, four in rounds)
    odd_k = "".join("<li><b>%s</b> is the odd one out: it goes with %s. The other three: %s.</li>"
                    % (markup.inline(t), markup.inline(st.groups[g].name), markup.inline(st.groups[b].name))
                    for b, g, t, _ in rounds)

    word, meaning = (_in_sentence(n) for n in st.pair_names)
    fp = sorted(brain_games.flash_pairs(r["key"], st), key=lambda p: _seed(p[1]))
    flash_q = "".join('<li class="st-sheet-q"><p>%s</p><p class="st-line"></p></li>' % markup.inline(b) for _, b in fp)
    flash_k = "".join("<li><b>%s</b> %s</li>" % (markup.inline(a), markup.inline(b)) for a, b in fp)

    deck = brain_games.fib_deck(st)
    fibs = sorted((x for x in deck if not x[1]), key=lambda x: _seed(x[0]))[:brain_games.FIB_MAX_FIBS]
    facts = sorted((x for x in deck if x[1]), key=lambda x: _seed(x[0]))[:brain_games.FIB_DEAL - len(fibs)]
    dealt = sorted(fibs + facts, key=lambda x: _seed("fib " + x[0]))
    fib_q = "".join('<li class="st-sheet-q"><p>%s</p><ul class="st-sheet-opts st-sheet-tf"><li><span class="st-box">'
                    '</span>Fact</li><li><span class="st-box"></span>Fib</li></ul></li>' % markup.inline(t)
                    for t, _, _ in dealt)
    fib_k = "".join("<li><b>%s</b> %s%s</li>" % ("Fact" if ok else "Fib", markup.inline(t),
                                                 (" <i>The fix:</i> %s" % markup.inline(why)) if not ok else "")
                    for t, ok, why in dealt)
    q = ('<h3>Brain game: Odd One Out</h3><p class="st-sheet-hint">Three tiles in each set share a link. Tick the '
         'odd one out, then write what links the other three.</p><ol class="st-sheet-list">%s</ol>'
         '<h3>Brain game: Memory Flash, on paper</h3><p class="st-sheet-hint">%s Write your answer from memory.</p>'
         '<ol class="st-sheet-list">%s</ol>'
         '<h3>Brain game: Fact or Fib</h3><p class="st-sheet-hint">Tick Fact if the statement is true and Fib if it '
         'is not.</p><ol class="st-sheet-list">%s</ol>' % (odd_q, esc(brain_games.flash_ask(st)), flash_q, fib_q))
    key = ('<h3>Odd One Out</h3><ol class="st-sheet-list">%s</ol>'
           '<h3>Memory Flash</h3><ol class="st-sheet-list">%s</ol>'
           '<h3>Fact or Fib</h3><ol class="st-sheet-list">%s</ol>' % (odd_k, flash_k, fib_k))
    return q, key


def _in_sentence(name):
    """A card label inside a sentence: Tag reads as tag, but CSS stays CSS."""
    return name if name.isupper() else name.lower()


def _seed(text):
    import hashlib
    return int(hashlib.sha256(text.encode("utf-8")).hexdigest(), 16)


def _sheet_order(b):
    """A fixed, deterministic order for options on paper, never the written one."""
    opts = list(b.options)
    seed = _seed(b.q)
    shifted = opts[seed % len(opts):] + opts[:seed % len(opts)]
    if b.kind == "order" and shifted == opts:
        shifted = opts[1:] + opts[:1]
    return shifted


# -------------------------------------------------------------- the pages

def _lobby(r):
    st = r["stretch"]
    counts = {"blitz": "%d questions against the clock" % len(st.blitz),
              "short": "%d short answers" % len(st.short),
              "long": "%d long answers" % len(st.long)}
    rounds = "".join(
        '<li class="st-round st-round-%s"><span class="st-round-ico">%s</span>'
        '<span class="st-round-txt"><b>%s</b><span>%s</span></span></li>'
        % (kind, _round_icon(kind), name, counts[kind]) for name, kind in ROUNDS)
    word, meaning = (_in_sentence(n) for n in st.pair_names)
    n_sort = len(st.sort.items) if st.sort else 0
    flash_levels = brain_games.flash_levels(len(brain_games.flash_pairs(r["key"], st)))
    about = {
        "quiz": ("A quiz game against four computer players, then short and long written answers.",
                 "About 20 minutes"),
        "cat": ("Pixel the cat asks %d questions. Each has two answers: pick the right one." % len(st.picks),
                "About 4 minutes"),
        "match": ("Flip the cards two at a time to match each %s card to its %s card." % (word, meaning),
                  "%d pairs, about 4 minutes" % len(st.pairs)),
        "sort": ("Sort each statement into the right box, like the tick box tables in the exam.",
                 "%d cards, about 4 minutes" % n_sort),
        "word": ("Guess the lesson's secret words. Every guess shows which letters are right.",
                 "%d words, about 4 minutes" % len(st.words)),
        "link": ("%d tiles hide %d groups of %d. Work out what links them."
                 % (sum(len(g.tiles) for g in st.groups), len(st.groups), len(st.groups[0].tiles) if st.groups else 0),
                 "%d groups, about 3 minutes" % len(st.groups)),
        "bug": ("Two statements are true and one has a bug. Catch the bug before it gets away.",
                "%d rounds, about 4 minutes" % len(st.bugs)),
        "odd": ("Four tiles: three share a link and one does not. Spot the odd one out, then see what links the rest.",
                "%d rounds, about 3 minutes" % brain_games.ODD_ROUNDS),
        "flash": ("Study the %s cards, then they flip over. Find the card that goes with each clue, from memory." % word,
                  "%d levels, about 4 minutes" % len(flash_levels)),
        "fib": ("Statements fly in one at a time. Is each one a fact or a fib? Decide fast.",
                "%d statements, about 3 minutes" % brain_games.FIB_DEAL),
        "run": ("Race a robot cat on inline skates through a neon cyber city, from Neon Station to the Hyper "
                "Tunnel. Every question is a row of neon gates across the tracks: skate through the one with the "
                "right answer, dodge the trains and barriers, and grab diamonds.",
                "%d questions, about 6 minutes" % city_run.QUESTIONS),
    }
    points = {
        "cat": ["Two answers to every question", "A fish treat for every right answer",
                "Streaks win Pixel shades, then a party hat"],
        "match": ["%d cards: each %s has a %s" % (2 * len(st.pairs), word, meaning), "One peek at every card",
                  "Combo points for pairs found in a row"],
        "sort": ["%d cards to sort into %d boxes" % (n_sort, len(st.sort.bins) if st.sort else 0),
                 "Drag a card, tap a box or press its number", "Combo points for cards sorted in a row"],
        "word": ["A clue for every word", "Tiles turn green, amber or grey after each guess",
                 "Fewer guesses win more points"],
        "link": ["Pick four tiles that belong together", "Four slips and the round is over",
                 "Fewer slips win more points"],
        "bug": ["Three statements in every round", "Tap the one with the mistake",
                "Streaks win bonus points"],
        "odd": ["Three belong together, one does not", "A hint shows the link, for fewer points",
                "Quick answers and streaks win more"],
        "flash": ["Three levels: %s cards" % _and(str(n) for n in flash_levels),
                  "Two tries to find each card", "Streaks win bonus points"],
        "fib": ["Swipe, tap or use the arrow keys", "Every fib comes with its fix", "Streaks multiply your points"],
        "run": ["%d questions from this lesson, in four parts of the city" % city_run.QUESTIONS,
                "Swipe, tap or use the arrow keys", "Dodge trains and holograms, and jump crates and cones"],
    }
    tasks = _tasks(r)

    def card(task, name, tag, h):
        return """<div class="st-task st-task-%(t)s" role="group" aria-labelledby="st-t-%(t)s">
        <div class="st-task-head"><span class="st-task-art" data-st-art="%(t)s" aria-hidden="true">%(art)s</span><span class="st-task-n">%(tag)s</span></div>
        <%(h)s id="st-t-%(t)s">%(name)s</%(h)s>
        <p class="st-task-sum">%(sum)s</p>
        %(rounds)s<p class="st-task-time">%(clock)s %(time)s</p>
        <p class="st-best" data-st-best="%(t)s" hidden></p>
        <button class="st-start" type="button" data-st-start="%(t)s">%(play)s Play<span class="sr-only"> %(name)s</span></button>
      </div>""" % dict(t=task, tag=tag, h=h, name=name, art=_task_icon(task), sum=esc(about[task][0]), time=about[task][1],
                       rounds=('<ol class="st-rounds">%s</ol>' % rounds if task == "quiz" else
                               '<ul class="st-points">%s</ul>' % "".join("<li>%s%s</li>" % (ico("i-check"), esc(t))
                                                                         for t in points[task])),
                       clock=ico("i-clock"), play=ico("i-play"))
    main = [t for t in tasks if t[0] not in BRAIN and t[0] != "run"]
    cards = [card(task, name, "Task %d" % n, "h2") for n, (task, name) in enumerate(main, 1)]
    brain = [t for t in tasks if t[0] in BRAIN]
    band = ""
    if brain:
        band = """<section class="st-brain" aria-labelledby="st-brain-h">
    <div class="st-brain-head">
      <span class="st-brain-ico" aria-hidden="true">%s</span>
      <div><p class="st-brain-tag">Brain games</p><h2 id="st-brain-h">Train your brain on this lesson</h2>
      <p>Logic, memory and speed, built from this lesson's own key ideas. Win up to three diamonds in each game.</p></div>
      <span class="st-brain-gems" aria-hidden="true">%s</span>
    </div>
    <div class="st-tasks st-brain-tasks" data-n="%d">
      %s
    </div>
  </section>""" % (BRAIN_ART, _gem("st-gem is-on") * 3, len(brain),
                   "\n      ".join(card(task, name, SKILL[task], "h3") for task, name in brain))
    run = teaser = ""
    if any(t == "run" for t, _ in tasks):
        run = """<section class="st-run-band st-task-run" id="st-run" aria-labelledby="st-run-h">
    <div class="st-run-art" aria-hidden="true">%s</div>
    <div class="st-run-body">
      <h2 class="st-run-tag" id="st-run-h"><span class="st-run-ico" data-st-art="run">%s</span>The final challenge</h2>
      <h3 id="st-t-run">City Run</h3>
      <p class="st-task-sum">%s</p>
      <ul class="st-points">%s</ul>
      <p class="st-task-time">%s %s</p>
      <p class="st-best" data-st-best="run" hidden></p>
      <button class="st-start" type="button" data-st-start="run">%s Play<span class="sr-only"> City Run</span></button>
    </div>
  </section>""" % (RUN_ART, _task_icon("run"), esc(about["run"][0]),
                   "".join("<li>%s%s</li>" % (ico("i-check"), esc(t)) for t in points["run"]),
                   ico("i-clock"), about["run"][1], ico("i-play"))
        teaser = ('\n    <a class="st-run-teaser" href="#st-run">%s<span><b>City Run</b> Race a skating robot cat through a neon city</span></a>'
                  % robocat.head(cls="rc rc-head-only st-run-teaser-cat"))
    return """<section class="st-lobby" id="st-lobby" aria-labelledby="st-title">
  <div class="st-bg" aria-hidden="true">%s</div>
  <div class="st-lobby-host" aria-hidden="true">%s</div>
  <div class="st-lobby-main">
    <p class="st-kicker">%s</p>
    <h1 id="st-title"><span class="st-h1-tag">Stretch tasks</span> %s</h1>
    <div class="st-setup">
      <label class="st-name"><span>Your name</span><input type="text" id="st-name" maxlength="16" autocomplete="off" spellcheck="false" placeholder="Player"></label>
      <div class="st-toggles" role="group" aria-label="Game settings">
        <button type="button" class="st-toggle" data-st-opt="timer" aria-pressed="true">%s Timer</button>
        <button type="button" class="st-toggle" data-st-opt="sound" aria-pressed="false">%s Sound</button>
      </div>
    </div>%s
  </div>
  <div class="st-tasks" data-n="%d">
      %s
  </div>
  %s
  %s
  <div class="st-lobby-go">
    <button class="st-link" type="button" data-st-print="sheet">%s Print the questions</button>
    <button class="st-link" type="button" data-st-print="answers">%s Print with answers</button>
  </div>
  <p class="st-nojs">The games need JavaScript. Every question is below, with the answers at the end.</p>
</section>""" % (BG, cat.rig(cls="px st-px"), " &middot; ".join(esc(k) for k in r["kicker"]),
                 esc(r["title"]), ico("i-timer"), ico("i-sound"), teaser, len(main), "\n      ".join(cards), band, run,
                 ico("i-paper"), ico("i-check"))


def _lesson_page(r, nxt, prev):
    trail = r["trail"]
    data = json.dumps(payload(r, nxt), separators=(",", ":"), ensure_ascii=False).replace("</", "<\\/")
    nav = []
    if prev:
        nav.append('<a class="prev" href="%s"><span>%s Previous</span><b>%s</b></a>' % (prev["url"], ico("i-arrow-left"), esc(prev["title"])))
    else:
        back = r["hub"] + ("#" + r["ckey"] if r["stage"] == "ks4" else "")
        nav.append('<a class="prev" href="%s"><span>%s Back</span><b>%s</b></a>' % (back, ico("i-arrow-left"), HUB_TITLE))
    if nxt:
        nav.append('<a class="next" href="%s"><span>Next %s</span><b>%s</b></a>' % (nxt["url"], ico("i-arrow-right"), esc(nxt["title"])))
    body = """<div class="wrap">%s</div>
<div class="wrap st-page">
  <div class="st" id="st" data-motion="full">
    %s
    <div class="st-stage" id="st-stage" hidden></div>
  </div>
  <p class="st-back"><a href="%s">%s Read the lesson: %s</a></p>
  %s
  <nav class="topic-nav" aria-label="Stretch tasks">%s</nav>
</div>
<template id="st-pixel">%s</template>%s
%s
<script type="application/json" id="st-data">%s</script>""" % (
        crumbs(trail), _lobby(r), r["lesson_url"], ico("i-book"), esc(r["title"]), _sheet(r), "".join(nav),
        cat.rig(), ('\n<template id="st-robocat">%s</template>' % robocat.svg("idle")) if _has_run(r) else "",
        GEM_DEFS, data)
    title = "Stretch tasks: %s" % r["title"]
    ld = [crumbs_ld(trail), {
        "@context": "https://schema.org", "@type": "LearningResource",
        "name": title, "description": r["desc"], "url": SITE_URL + r["url"], "inLanguage": "en-GB",
        "isAccessibleForFree": True, "learningResourceType": "Quiz",
        "educationalLevel": r["level"], "teaches": r["title"],
        "isPartOf": {"@type": "Course", "name": r["course_name"], "url": SITE_URL + r["course_url"]},
        "provider": {"@type": "Organization", "name": SITE_NAME, "url": SITE_URL},
    }]
    return layout(title=title, description=r["desc"], path=r["url"], body=body, active=r["active"],
                  extra_head='<link rel="stylesheet" href="/assets/css/stretch.css">',
                  scripts=["/assets/js/quiz.js"] + (["/assets/js/cityrun.js"] if _has_run(r) else []) + ["/assets/js/stretch.js"],
                  jsonld=ld)


# Small marks for the tasks on the hub's cards, drawn once and reused.
GLYPHS = ('<svg class="st-glyphs" width="0" height="0" aria-hidden="true" focusable="false">'
          '<symbol id="st-g-quiz" viewBox="0 0 24 24"><rect x="2" y="2" width="9" height="9" rx="2.4" fill="#D7263D"/>'
          '<rect x="13" y="2" width="9" height="9" rx="2.4" fill="#1F5FD1"/><rect x="2" y="13" width="9" height="9" rx="2.4" '
          'fill="#F2B705"/><rect x="13" y="13" width="9" height="9" rx="2.4" fill="#1E7B34"/></symbol>'
          '<symbol id="st-g-cat" viewBox="0 0 24 24"><path d="M3.6 10 4.3 2.8l5.2 3.6h5L19.7 2.8l.7 7.2A8.6 8.2 0 0 1 '
          '12 21.6 8.6 8.2 0 0 1 3.6 10Z" fill="#02848B"/><circle cx="8.8" cy="12.6" r="1.7" fill="#fff"/>'
          '<circle cx="15.2" cy="12.6" r="1.7" fill="#fff"/><path d="M10.9 15.8h2.2L12 17.1Z" fill="#fff"/></symbol>'
          '<symbol id="st-g-match" viewBox="0 0 24 24"><rect x="1.5" y="4" width="11" height="15" rx="2.4" fill="#1F5FD1" '
          'transform="rotate(-9 7 11.5)"/><rect x="11" y="3.5" width="11" height="15" rx="2.4" fill="#fff" stroke="#1E293B" '
          'stroke-width="1.6" transform="rotate(8 16.5 11)"/><path d="M14 8.5h5M14 11.5h3.6" stroke="#1E293B" '
          'stroke-width="1.6" stroke-linecap="round" transform="rotate(8 16.5 11)"/></symbol>'
          '<symbol id="st-g-sort" viewBox="0 0 24 24"><path d="M1.5 14h9l-1 8.5h-7Z" fill="#F97316"/>'
          '<path d="M13.5 14h9l-1 8.5h-7Z" fill="#1F5FD1"/><rect x="7" y="2" width="10" height="8" rx="1.8" fill="#fff" '
          'stroke="#1E293B" stroke-width="1.5" transform="rotate(-10 12 6)"/></symbol>'
          '<symbol id="st-g-word" viewBox="0 0 24 24"><rect x="1.5" y="8" width="6.4" height="8" rx="1.6" fill="#64748B"/>'
          '<rect x="8.8" y="8" width="6.4" height="8" rx="1.6" fill="#F59E0B"/><rect x="16.1" y="8" width="6.4" height="8" '
          'rx="1.6" fill="#16A34A"/></symbol>'
          '<symbol id="st-g-link" viewBox="0 0 24 24"><rect x="2" y="2" width="9" height="9" rx="2.4" fill="#DC2626"/>'
          '<rect x="13" y="2" width="9" height="9" rx="2.4" fill="#DC2626"/><rect x="2" y="13" width="9" height="9" rx="2.4" '
          'fill="#DC2626"/><rect x="13" y="13" width="9" height="9" rx="2.4" fill="#DC2626"/>'
          '<circle cx="12" cy="12" r="3.6" fill="#FDE047" stroke="#1E293B" stroke-width="1.4"/></symbol>'
          '<symbol id="st-g-bug" viewBox="0 0 24 24"><path d="M6.5 9.5 2.5 7.5M5.5 14H1.5M6.5 18l-4 2.5M17.5 9.5l4-2M18.5 14h4'
          'M17.5 18l4 2.5" fill="none" stroke="#1E293B" stroke-width="1.6" stroke-linecap="round"/>'
          '<circle cx="12" cy="6.5" r="3.4" fill="#1E293B"/><ellipse cx="12" cy="14.5" rx="6.4" ry="7.4" fill="#65A30D" '
          'stroke="#1E293B" stroke-width="1.4"/><path d="M12 7.5v14.2" stroke="#1E293B" stroke-width="1.3"/></symbol>'
          '<symbol id="st-g-odd" viewBox="0 0 24 24"><rect x="2" y="2" width="9" height="9" rx="2.4" fill="#7C3AED"/>'
          '<rect x="2" y="13" width="9" height="9" rx="2.4" fill="#7C3AED"/><rect x="13" y="13" width="9" height="9" rx="2.4" '
          'fill="#7C3AED"/><rect x="13" y="2" width="9" height="9" rx="2.4" fill="#F59E0B" transform="rotate(14 17.5 6.5)"/>'
          '</symbol>'
          '<symbol id="st-g-flash" viewBox="0 0 24 24"><rect x="4" y="1.5" width="16" height="21" rx="3" fill="#0891B2"/>'
          '<path d="M13.5 4.5 8 13h3.6l-1.8 6.5 6.2-9.4h-3.9Z" fill="#FDE047" stroke="#1E293B" stroke-width="1.1" '
          'stroke-linejoin="round"/></symbol>'
          '<symbol id="st-g-fib" viewBox="0 0 24 24"><circle cx="7" cy="12" r="6" fill="#DC2626"/>'
          '<path d="M4.8 9.8l4.4 4.4M9.2 9.8l-4.4 4.4" stroke="#fff" stroke-width="1.8" stroke-linecap="round"/>'
          '<circle cx="17" cy="12" r="6" fill="#16A34A"/><path d="M14.3 12.2l2 2 3.6-3.8" fill="none" stroke="#fff" '
          'stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></symbol>'
          '<symbol id="st-g-run" viewBox="0 0 24 24"><path d="M3.3 11.6 3.6 2.6Q3.9 1.6 4.8 2.3L10.6 6.6Z" fill="#D5D8EA" '
          'stroke="#2A2D4A" stroke-width="1" stroke-linejoin="round"/><path d="M5 9.4 5.2 4.5 8.6 7.2Z" fill="#22D3EE"/>'
          '<path d="M20.7 11.6 20.4 2.6Q20.1 1.6 19.2 2.3L13.4 6.6Z" fill="#D5D8EA" stroke="#2A2D4A" stroke-width="1" '
          'stroke-linejoin="round"/><path d="M19 9.4 18.8 4.5 15.4 7.2Z" fill="#22D3EE"/>'
          '<ellipse cx="12" cy="14" rx="9.4" ry="8.2" fill="#CDD0E3" stroke="#2A2D4A" stroke-width="1"/>'
          '<circle cx="8.4" cy="14.6" r="3.5" fill="#5A5F86" stroke="#2A2D4A" stroke-width=".8"/>'
          '<circle cx="8.4" cy="14.6" r="2.4" fill="#071420"/>'
          '<circle cx="15.6" cy="14.6" r="3.5" fill="#5A5F86" stroke="#2A2D4A" stroke-width=".8"/>'
          '<circle cx="15.6" cy="14.6" r="2.4" fill="#071420"/>'
          '<path d="M7.3 13.3v2.6M9.5 13.3v2.6M7.3 14.6h2.2M14.5 13.3v2.6M16.7 13.3v2.6M14.5 14.6h2.2" stroke="#67E8F9" '
          'stroke-width=".8" stroke-linecap="round"/><path d="M11.3 18.9h1.4l-.7.8Z" fill="#3B3346"/></symbol>'
          '<symbol id="st-gem" viewBox="0 0 24 22">' + GEM_FACETS + '</symbol></svg>')


def _hub_tasks(tasks):
    """Each task's best diamonds on a hub card, filled in from this device's
    results. The brain games take a row of their own."""
    def badge(task, name):
        return ('<span class="st-hub-task" data-st-task="%s"><svg class="st-g" aria-hidden="true" focusable="false">'
                '<use href="#st-g-%s"></use></svg><span class="st-gems" data-st-gems aria-hidden="true">%s</span>'
                '<span class="sr-only" data-st-sr>%s: not played yet.</span></span>' % (task, task, _gem() * 3, name))
    main = [t for t in tasks if t[0] not in BRAIN and t[0] != "run"]
    brain = [t for t in tasks if t[0] in BRAIN or t[0] == "run"]
    cls = {4: " is-four", 6: " is-six", 7: " is-seven"}.get(len(main), "")
    out = '<span class="st-hub-tasks%s">%s</span>' % (cls, "".join(badge(*t) for t in main))
    if brain:
        out += '<span class="st-hub-tasks is-brain">%s</span>' % "".join(badge(*t) for t in brain)
    return out


def _hub_card(r, label):
    return ('<a class="st-hub-card" href="%s" data-st-key="%s"><span class="st-hub-n">%s</span><b>%s</b>%s</a>'
            % (r["url"], esc(r["key"]), esc(label), esc(_card_title(r)), _hub_tasks(_tasks(r))))


def _card_title(r):
    """A Creative iMedia topic's title starts with its specification reference,
    which its hub card already shows."""
    t, spec = r["title"], r["topic"].spec
    return t[len(spec) + 2:] if r["stage"] == "ks4" and spec and t.startswith(spec + ": ") else t


def _hub_page(*, path, title, h1, lead, trail, sections, tasks, course_name, course_url, active, jump="", summary=""):
    body = """<div class="wrap">%s</div>
<section class="hero st-hub-hero"><div class="wrap">
  <div class="st-hub-head">
    <div>
      <h1>%s</h1>
      <p class="lead">%s</p>%s
    </div>
    <div class="st-hub-art" data-n="%d" aria-hidden="true">%s</div>
  </div>
</div></section>
<div class="wrap st-hub">%s%s</div>""" % (crumbs(trail), esc(h1), esc(lead), jump, len(tasks),
                                          "".join(_task_icon(t) for t, _ in tasks), GLYPHS, sections)
    ld = [crumbs_ld(trail), {
        "@context": "https://schema.org", "@type": "CollectionPage", "name": h1,
        "description": lead, "url": SITE_URL + path, "inLanguage": "en-GB",
        "isPartOf": {"@type": "Course", "name": course_name, "url": SITE_URL + course_url},
    }]
    return layout(title=title, description=(summary or lead) + " Free, no account needed.", path=path, body=body, active=active,
                  extra_head='<link rel="stylesheet" href="/assets/css/stretch.css">',
                  scripts=["/assets/js/stretch.js"], jsonld=ld)


def _hub(recs):
    years = []
    for year in ("Year 7", "Year 8", "Year 9"):
        units = []
        seen = []
        for r in recs:
            if r["year"] != year or r["topic"].slug in seen:
                continue
            seen.append(r["topic"].slug)
            cards = "".join(_hub_card(x, "Lesson %d" % x["n"]) for x in recs if x["topic"].slug == r["topic"].slug)
            units.append('<div class="st-hub-unit" id="%s"><h3><span class="badge badge-spec">%s</span> %s</h3>'
                         '<div class="st-hub-cards">%s</div></div>'
                         % (esc(r["topic"].slug), esc(r["topic"].spec), esc(r["topic"].title), cards))
        if units:
            years.append('<section class="section st-hub-year" id="%s"><h2>%s</h2>%s</section>'
                         % (slugify(year), year, "".join(units)))
    tasks = _tasks_of(recs)
    # The lead is too long for a search snippet, so the description says it shorter
    summary = ("Ten stretch tasks for every Year 7, 8 and 9 lesson, from a quiz to City Run, a robot cat's neon "
               "city race, with diamonds to win." if len(tasks) > 3 else "")
    return _hub_page(path=HUB, title="KS3 Computing stretch tasks", h1=HUB_TITLE, summary=summary,
                     lead=HUB_LEAD if len(tasks) > 3 else HUB_LEAD3,
                     trail=[("Home", "/"), ("Key Stage 3", "/ks3/"), (HUB_TITLE, None)],
                     sections="".join(years), tasks=tasks, course_name=ks3.COURSE.title, course_url="/ks3/",
                     active="/ks3/")


def _and(names):
    names = list(names)
    return names[0] if len(names) == 1 else ", ".join(names[:-1]) + " and " + names[-1]


def _hub4_lead(courses):
    """courses: [(name, every lesson has the games)]"""
    courses = list(courses)
    names = [n for n, _ in courses]
    played = [n for n, g in courses if g]
    if played and len(played) == len(names):
        return ("Ten tasks for every lesson of %s: a quiz challenge, This or That with Pixel the cat, "
                "Memory Match, Sort It, Code Word, Link Up and Bug Hunt, then three brain games: Odd One Out, "
                "Memory Flash and Fact or Fib. Every result is rated out of three diamonds." % _and(names))
    lead = ("Four tasks for every lesson of %s: a quiz challenge, This or That with Pixel the cat, "
            "Memory Match and Sort It." % _and(names))
    if played:
        lead += " Lessons of %s add Code Word, Link Up and Bug Hunt." % _and(played)
    return lead


def _hub4(recs):
    courses = []
    for r in recs:
        if r["ckey"] not in [c[0] for c in courses]:
            courses.append((r["ckey"], r["cname"]))
    sections = []
    for key, name in courses:
        mine = [r for r in recs if r["ckey"] == key]
        units = []
        for u in mine[0]["course"].units:
            cards = "".join(_hub_card(r, r["topic"].spec) for r in mine if r["unit"] is u)
            if cards:
                units.append('<div class="st-hub-unit" id="%s-%s"><h3>%s</h3><div class="st-hub-cards">%s</div></div>'
                             % (key, esc(u.slug), esc(u.title), cards))
        sections.append('<section class="section st-hub-year" id="%s"><h2>%s</h2>%s</section>'
                        % (key, esc(name), "".join(units)))
    jump = ""
    if len(courses) > 1:
        jump = ('\n      <p class="st-hub-jump">%s</p>'
                % "".join('<a class="btn btn-secondary" href="#%s">%s</a>' % (k, esc(n)) for k, n in courses))
    first = recs[0]
    title = "GCSE Computer Science%s stretch tasks" % (" and Creative iMedia" if "imedia" in [k for k, _ in courses] else "")
    # The lead names every course, too long for a search snippet once all four carry the games
    summary = ("Ten stretch tasks for every %s lesson, from a quiz to three brain games with diamonds to win."
               % title[:-len(" stretch tasks")] if all(r["stretch"].words for r in recs) else "")
    return _hub_page(path=HUB4, title=title, h1=HUB4_TITLE,
                     lead=_hub4_lead((n, all(r["stretch"].words for r in recs if r["ckey"] == k)) for k, n in courses),
                     trail=[("Home", "/"), (HUB4_TITLE, None)],
                     sections="".join(sections), tasks=_tasks_of(recs), jump=jump, summary=summary,
                     course_name=first["course_name"], course_url=first["course_url"], active=first["active"])


def _publish(recs, register, add_search):
    for i, r in enumerate(recs):
        nxt = recs[i + 1] if i + 1 < len(recs) else None
        prev = recs[i - 1] if i else None
        write(r["url"], _lesson_page(r, nxt, prev))
        register(r["url"], 0.6, "monthly")
        if r["stage"] == "ks3":
            add_search("Stretch tasks: %s" % r["title"], r["url"],
                       "%s %s, lesson %d" % (r["topic"].spec, r["topic"].title, r["n"]),
                       ("stretch task challenge quiz game this or that pixel cat memory match pairs code word "
                        "link up bug hunt word puzzle brain games odd one out memory flash fact or fib diamonds "
                        "city run cyber city neon runner robot cat inline skates ks3 %s %s %s" % (r["year"], r["topic"].title, r["title"])).lower())
        else:
            add_search("Stretch tasks: %s" % r["title"], r["url"], "%s %s" % (r["cname"], r["topic"].spec),
                       ("stretch task challenge quiz game this or that pixel cat memory match sort it code word link up "
                        "bug hunt brain games odd one out memory flash fact or fib diamonds ks4 gcse %s %s %s"
                        % (r["cname"], r["topic"].spec, r["title"])).lower())


def build(register, add_search):
    missing = check()
    if missing:
        raise SystemExit("Lessons with no stretch task:\n  " + "\n  ".join(missing))
    recs = records()
    ks3r = [r for r in recs if r["stage"] == "ks3"]
    ks4r = [r for r in recs if r["stage"] == "ks4"]
    _publish(ks3r, register, add_search)
    write(HUB, _hub(ks3r))
    register(HUB, 0.8, "weekly")
    add_search(HUB_TITLE, HUB, "Years 7, 8 and 9: %s tasks for every lesson"
               % ("ten" if len(_tasks_of(ks3r)) > 3 else "three"),
               "stretch tasks challenge extension fast finishers quiz game kahoot this or that pixel cat "
               "memory match pairs code word link up bug hunt word puzzle games brain games odd one out "
               "memory flash fact or fib diamonds city run cyber city neon runner robot cat inline skates ks3 year 7 year 8 year 9 lessons")
    if ks4r:
        for key in dict.fromkeys(r["ckey"] for r in ks4r):
            _publish([r for r in ks4r if r["ckey"] == key], register, add_search)
        write(HUB4, _hub4(ks4r))
        register(HUB4, 0.8, "weekly")
        games4 = all(r["stretch"].words for r in ks4r)
        add_search(HUB4_TITLE, HUB4, "GCSE: %s tasks for every topic" % ("ten" if games4 else "four"),
                   "stretch tasks challenge extension fast finishers quiz game kahoot this or that pixel cat "
                   "memory match sort it ks4 gcse computer science revision games"
                   + (" code word link up bug hunt word puzzle connections brain games odd one out memory flash "
                      "fact or fib diamonds" if games4 else ""))
    n_q = sum(len(r["stretch"].blitz) + len(r["stretch"].short) + len(r["stretch"].long) for r in recs)
    n_p = sum(len(r["stretch"].picks) for r in recs)
    n_m = sum(len(r["stretch"].pairs) for r in recs)
    n_s = sum(len(r["stretch"].sort.items) for r in recs if r["stretch"].sort)
    n_w = sum(len(r["stretch"].words) for r in recs)
    n_g = sum(len(r["stretch"].groups) for r in recs)
    n_b = sum(len(r["stretch"].bugs) for r in recs)
    n_odd = sum(brain_games.odd_puzzles(brain_games.odd_intruders(r["key"], r["stretch"]), r["stretch"].groups)
                for r in recs if r["stretch"].groups)
    n_fib = sum(len(brain_games.fib_deck(r["stretch"])) for r in recs if r["stretch"].bugs)
    print("Stretch tasks: %d lessons (%d at Key Stage 4), %d quiz questions, %d This or That questions, "
          "%d Memory Match pairs, %d Sort It cards, %d Code Word words, %d Link Up groups and %d Bug Hunt rounds checked"
          % (len(recs), len(ks4r), n_q, n_p, n_m, n_s, n_w, n_g, n_b))
    print("Brain games: %d possible Odd One Out rounds and %d Fact or Fib statements checked" % (n_odd, n_fib))
    runs = [r for r in recs if _has_run(r)]
    n_run = sum(sum(city_run.counts(r["key"], r["stretch"]).values()) for r in runs)
    print("City Run: %d lessons, %d questions to draw from checked" % (len(runs), n_run))
