"""City Run: a robot cat races through a neon cyber city, and every lane is an answer.

Twenty questions a run, all from the lesson's own checked tasks, so each one
is already correct and on the lesson's topic:

  c  the quiz's pick one questions. The run shows the right answer and two of
     the wrong ones. Every wrong answer is wrong, so any two of them will do.
  p  This or That: a right answer and a wrong one.
  m  Memory Flash's pairs: which card goes with this clue. Memory Flash has
     already left out every clue that fits more than one of the lesson's
     cards, so a clue fits only its own card out of any three.
  f  Fact or Fib's statements: is it a fact or a fib.

Game text has no dashes, as in the brain games. A question is left out if
its wording, right answer, explanation or code cannot be written without
one, and so is any wrong answer that cannot. Code taller or wider than a
phone can show beside the road is left out too.

Key Stage 3 lessons have City Run. A key stage joins by adding it to STAGES.
"""
import re

from content import brain_games
from content.brain_games import DASH

STAGES = ("ks3",)
QUESTIONS = 20                               # asked in one run
MIX = (("c", 6), ("p", 5), ("m", 4))         # the most of each kind a run asks; Fact or Fib fills the rest
LEAST = {"c": 3, "p": 4, "m": 4, "f": 8}     # each lesson needs at least this many of each kind
DISTRICTS = ("Neon Station", "Ramen Row", "Arcade Alley", "Hyper Tunnel")   # five questions in each
QUESTION_MAX = 150
OPTION_MAX = 90
CODE_LINES = 6
CODE_WIDTH = 44

_PLAIN = brain_games._plain

# Words that read as well without their dash, on top of the brain games' own
# list. They are kept apart from it so the brain games' audited decks do not
# change. Numbers, file names, web addresses, CSS properties and passphrases
# keep their dashes, so the questions that show them are left out.
RUN_FIXES = [("in-game", "in game"), ("Too-good-to-be-true", "Too good to be true"),
             ("human-friendly", "human friendly"), ("Anti-malware", "Anti malware"),
             ("anti-malware", "anti malware"), ("self-driving", "self driving"), ("self-checkouts", "self checkouts"),
             ("well-structured", "well structured"), ("well-named", "well named"), ("to-do", "to do"),
             ("five-year-olds", "five year olds"), ("hand-written", "handwritten"),
             ("lighter-skinned", "lighter skinned"), ("likely-sounding", "likely sounding"),
             ("non-destructive", "non destructive"), ("three-point", "three point"), ("in-between", "in between")]
_BITS = re.compile(r"\b(\d+)-bit\b")


def clean(text):
    """The text with its dashes written out, or None if a dash is left."""
    text = _BITS.sub(r"\1 bit", text or "")
    for a, b in RUN_FIXES:
        text = text.replace(a, b)
    return brain_games.clean(text)


def available(stage, brain):
    """Whether a lesson has City Run: its key stage runs it, and it has the
    brain games, whose statements and pairs it shares."""
    return stage in STAGES and brain


def _code(code):
    """The code, if it fits beside the road and has no minus sign; else None."""
    if not code:
        return ""
    lines = code.strip("\n").split("\n")
    if len(lines) > CODE_LINES or max(len(line) for line in lines) > CODE_WIDTH or DASH.search(code):
        return None
    return code


def choices(st):
    """The quiz's pick one questions a run can ask:
    (question, right answer, wrong answers, explanation, code, language)."""
    out = []
    for b in st.blitz:
        if b.kind != "choice":
            continue
        q, right, why, code = clean(b.q), clean(b.options[0]), clean(b.explain), _code(b.code)
        if q is None or right is None or why is None or code is None:
            continue
        wrongs = [w for w in (clean(o) for o in b.options[1:]) if w is not None]
        if len(wrongs) >= 2:
            out.append((q, right, wrongs, why, code, b.lang))
    return out


def picks(st):
    """This or That's questions a run can ask:
    (question, right answer, wrong answer, why, code, language)."""
    out = []
    for p in st.picks:
        q, right, wrong, why, code = clean(p.q), clean(p.right), clean(p.wrong), clean(p.why), _code(p.code)
        if None not in (q, right, wrong, why, code):
            out.append((q, right, wrong, why, code, p.lang))
    return out


def counts(key, st):
    """How many questions of each kind the lesson can ask."""
    return {"c": len(choices(st)), "p": len(picks(st)), "m": len(brain_games.flash_pairs(key, st)),
            "f": len(brain_games.fib_deck(st))}


def problems(key, st):
    """Everything that stops this lesson's City Run being played fairly."""
    out = []
    n = counts(key, st)
    for kind, least in LEAST.items():
        if n[kind] < least:
            out.append("%s: City Run has %d questions of kind %s, at least %d needed" % (key, n[kind], kind, least))
    asked = sum(min(n[k], most) for k, most in MIX)
    if asked + n["f"] < QUESTIONS:
        out.append("%s: City Run can ask only %d questions, %d needed" % (key, asked + n["f"], QUESTIONS))
    for q, right, wrongs, why, code, lang in choices(st):
        texts = [" ".join(t.lower().split()) for t in [right] + wrongs]
        if len(set(texts)) != len(texts):
            out.append("%s: a City Run question has the same answer twice: %s" % (key, q))
        if len(_PLAIN(q)) > QUESTION_MAX:
            out.append("%s: a City Run question is longer than %d characters: %s" % (key, QUESTION_MAX, q))
        for t in [right] + wrongs:
            if len(_PLAIN(t)) > OPTION_MAX:
                out.append("%s: a City Run answer is longer than %d characters: %s" % (key, OPTION_MAX, t))
        if not why.strip():
            out.append("%s: a City Run question has no explanation: %s" % (key, q))
    for q, right, wrong, why, code, lang in picks(st):
        if " ".join(right.lower().split()) == " ".join(wrong.lower().split()):
            out.append("%s: a This or That question in City Run has the same answer twice: %s" % (key, q))
        if len(_PLAIN(q)) > QUESTION_MAX:
            out.append("%s: a City Run question is longer than %d characters: %s" % (key, QUESTION_MAX, q))
        for t in (right, wrong):
            if len(_PLAIN(t)) > OPTION_MAX:
                out.append("%s: a City Run answer is longer than %d characters: %s" % (key, OPTION_MAX, t))
    terms = [" ".join(a.lower().split()) for a, b in brain_games.flash_pairs(key, st)]
    if len(set(terms)) != len(terms):
        out.append("%s: City Run would show the same card twice" % key)
    for t in (_PLAIN(t) for t, ok, why in brain_games.fib_deck(st)):
        if len(t) > QUESTION_MAX:
            out.append("%s: a City Run statement is longer than %d characters: %s" % (key, QUESTION_MAX, t))
    return out


def check(records, has_run):
    """records: the stretch pages; has_run(r) says whether a page has City Run.
    Returns a list of problems, and proves that every lesson of a key stage
    in STAGES has the run."""
    out = []
    for r in records:
        if has_run(r):
            out += problems(r["key"], r["stretch"])
        elif r["stage"] in STAGES and r["stretch"].words:
            out.append("%s: a %s lesson with games has no City Run" % (r["key"], r["stage"].upper()))
    return out
