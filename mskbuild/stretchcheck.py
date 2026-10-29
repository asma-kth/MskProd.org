"""Prove every Key Stage 3 stretch task before it is published.

A stretch task is played, not read, so a fault in one is a fault a student
meets with the clock running: a question with two right answers, a puzzle
that cannot be solved, a written answer the marker can never award. This
module stops the build on any of them.

Written answers are marked in the browser by the keyword marker in
static/js/quiz.js. `score()` below is the same marker in Python, kept line for
line in step with it (tools/check_stretch.mjs runs both on every answer and
fails if they ever disagree). Three things are proved for every written
question:

  The model answer earns full marks, so the mark points can be reached.
  Copying the question back as the answer earns nothing on a short answer and
  at most one mark on a long one, so no mark is given for repeating the
  question.
  A blank or "I don't know" answer earns nothing.
"""
import re

from mskbuild.models import Blitz, Written, Stretch

# ------------------------------------------------------------------ marker
# Mirrors SYNONYMS, normalise, stem, stemSet, containsPhrase and pointHit in
# static/js/quiz.js.
SYNONYMS = {
    "cpu": ["processor", "central processing unit"],
    "processor": ["cpu", "central processing unit"],
    "ram": ["main memory", "primary memory", "random access memory"],
    "rom": ["read only memory"],
    "hdd": ["hard disk", "hard disk drive", "magnetic hard drive"],
    "ssd": ["solid state drive", "solid state"],
    "os": ["operating system"],
    "gui": ["graphical user interface"],
    "url": ["web address"],
    "ip": ["internet protocol"],
    "lan": ["local area network"],
    "wan": ["wide area network"],
    "isp": ["internet service provider"],
    "alu": ["arithmetic logic unit"],
    "cu": ["control unit"],
    "mar": ["memory address register"],
    "mdr": ["memory data register"],
    "pc": ["program counter"],
    "dbms": ["database management system"],
    "sql": ["structured query language"],
    "ide": ["integrated development environment"],
    "nea": ["non exam assessment", "coursework"],
    "loop": ["iteration", "repeat", "repetition"],
    "iteration": ["loop", "repeat", "repetition"],
    "selection": ["if statement", "condition", "conditional"],
    "quicker": ["faster", "quick", "fast", "speed"],
    "faster": ["quicker", "quick", "fast", "speed"],
}


def normalise(s):
    s = str(s or "").lower()
    s = re.sub(r"[‘’“”]", "'", s)
    s = re.sub(r"[^a-z0-9'+\-<>=\s]", " ", s)
    s = re.sub(r"\s+", " ", s)
    return " " + s + " "


def stem(w):
    if len(w) > 5 and w.endswith("ies"):
        return w[:-3] + "y"
    if len(w) > 4 and (w.endswith("ing") or w.endswith("ed")):
        return re.sub(r"(ing|ed)$", "", w)
    if len(w) > 3 and w.endswith("es") and not (w.endswith("ss") or w.endswith("us")):
        return w[:-2]
    if len(w) > 3 and w.endswith("s") and not (w.endswith("ss") or w.endswith("us")):
        return w[:-1]
    return w


def stem_set(text):
    out = set()
    for w in normalise(text).strip().split(" "):
        if w:
            out.add(w)
            out.add(stem(w))
    return out


def contains_phrase(answer_norm, answer_stems, phrase, via_synonym=False):
    p = normalise(phrase).strip()
    if not p:
        return False
    if (" " + p + " ") in answer_norm:
        return True
    words = p.split(" ")
    if len(words) == 1:
        w = words[0]
        if w in answer_stems or stem(w) in answer_stems:
            return True
        if via_synonym:
            return False
        return any(contains_phrase(answer_norm, answer_stems, s, True) for s in SYNONYMS.get(w, []))
    return all(w in answer_stems or stem(w) in answer_stems for w in words)


def hits(text, points):
    """Which mark points an answer earns: a list of booleans, one per point."""
    if not str(text or "").strip():
        return [False] * len(points)
    a, s = normalise(text), stem_set(text)
    return [any(contains_phrase(a, s, ph) for ph in p.any) for p in points]


def score(text, q):
    return min(q.marks, sum(hits(text, q.points)))


# -------------------------------------------------------------- validation
KINDS = ("choice", "multi", "tf", "order", "type")
# Options that point at other options. The game shuffles every question's
# options, so "both of these" would end up pointing at nothing in particular.
_POINTING = re.compile(r"^\s*(both|neither)\b|\b(all|none)\s+of\s+(the\s+)?(above|these|them)\b", re.I)
_IDK = ("I don't know", "not sure", "yes")

Q_MAX = 240          # characters in a game question, so it fits above four tiles
OPTION_MAX = 90      # characters on a tile


class StretchError(Exception):
    pass


def _blitz_problems(where, b):
    out = []
    if b.kind not in KINDS:
        return ["%s: unknown kind %r" % (where, b.kind)]
    if not b.q.strip():
        out.append("%s: no question" % where)
    if len(b.q) > Q_MAX:
        out.append("%s: question is %d characters, the game shows at most %d" % (where, len(b.q), Q_MAX))
    if not b.explain.strip():
        out.append("%s: no explanation" % where)
    if b.time and not 5 <= b.time <= 120:
        out.append("%s: time %d is outside 5 to 120 seconds" % (where, b.time))
    opts = [o.strip() for o in b.options]
    if b.kind in ("choice", "multi", "order"):
        if any(not o for o in opts):
            out.append("%s: an empty option" % where)
        if len(set(o.lower() for o in opts)) != len(opts):
            out.append("%s: two options are the same" % where)
        for o in opts:
            if len(o) > OPTION_MAX:
                out.append("%s: option is %d characters, a tile shows at most %d: %s" % (where, len(o), OPTION_MAX, o))
            if _POINTING.search(o):
                out.append("%s: option points at other options, which shuffling breaks: %s" % (where, o))
    if b.kind == "choice" and not 3 <= len(opts) <= 4:
        out.append("%s: a choice question needs three or four options" % where)
    if b.kind == "multi" and not (2 <= b.n < len(opts) <= 6):
        out.append("%s: a multi question needs at least two right options and at least one wrong one" % where)
    if b.kind == "order" and not 3 <= len(opts) <= 6:
        out.append("%s: an order question needs three to six items" % where)
    if b.kind == "tf" and (opts or not isinstance(b.answer, bool)):
        out.append("%s: a true or false question has no options and a True or False answer" % where)
    if b.kind == "type":
        if not b.accept or any(not a.strip() for a in b.accept):
            out.append("%s: a typed answer needs at least one accepted answer" % where)
        if opts:
            out.append("%s: a typed answer has no options" % where)
    return out


def _written_problems(where, w, long_answer):
    out = []
    if w.marks < 1:
        out.append("%s: no marks" % where)
    if len(w.points) < w.marks:
        out.append("%s: %d marks but only %d mark points" % (where, w.marks, len(w.points)))
    for p in w.points:
        if not p.any or any(not ph.strip() for ph in p.any):
            out.append("%s: mark point with an empty phrasing: %s" % (where, p.text))
    if not w.model.strip():
        out.append("%s: no model answer" % where)
        return out
    got = score(w.model, w)
    if got < w.marks:
        missed = [p.text for p, h in zip(w.points, hits(w.model, w.points)) if not h]
        out.append("%s: the model answer earns %d of %d; it misses: %s" % (where, got, w.marks, "; ".join(missed)))
    echo = score(w.q, w)
    if echo > (1 if long_answer else 0):
        found = [p.text for p, h in zip(w.points, hits(w.q, w.points)) if h]
        out.append("%s: copying the question earns %d mark(s), from: %s" % (where, echo, "; ".join(found)))
    for idk in _IDK:
        if score(idk, w):
            out.append("%s: the answer %r earns a mark" % (where, idk))
    return out


def validate(units, topics):
    """units: [(topic slug, [Stretch])]; topics: {slug: Topic}. Raises StretchError."""
    problems = []
    for slug, lessons in units:
        topic = topics.get(slug)
        if topic is None:
            problems.append("%s: no such topic" % slug)
            continue
        titles = [s.title for s in topic.sections]
        for i, st in enumerate(lessons):
            where = "%s lesson %d (%s)" % (slug, i + 1, st.lesson)
            if st.lesson not in titles:
                problems.append("%s: no section of %s is called that" % (where, slug))
            if not 10 <= len(st.blitz) <= 14:
                problems.append("%s: %d game questions, expected 10 to 14" % (where, len(st.blitz)))
            if not 3 <= len(st.short) <= 5:
                problems.append("%s: %d short answers, expected 3 to 5" % (where, len(st.short)))
            if not 2 <= len(st.long) <= 3:
                problems.append("%s: %d long answers, expected 2 or 3" % (where, len(st.long)))
            seen = set()
            for n, b in enumerate(st.blitz):
                problems += _blitz_problems("%s game question %d" % (where, n + 1), b)
                key = (b.q.strip().lower(), b.code.strip())
                if key in seen:
                    problems.append("%s: game question %d repeats an earlier one" % (where, n + 1))
                seen.add(key)
            for n, w in enumerate(st.short):
                problems += _written_problems("%s short answer %d" % (where, n + 1), w, False)
            for n, w in enumerate(st.long):
                problems += _written_problems("%s long answer %d" % (where, n + 1), w, True)
                if w.marks < 3:
                    problems.append("%s long answer %d: a long answer is worth at least 3 marks" % (where, n + 1))
        order = [titles.index(s.lesson) for s in lessons if s.lesson in titles]
        if order != sorted(order):
            problems.append("%s: lessons are not in the order the topic teaches them" % slug)
    if problems:
        raise StretchError("Stretch tasks failed their checks:\n  " + "\n  ".join(problems))
