"""Put the correct answer somewhere other than A.

Every quiz question in the content files is written correct answer first,
because that is the quickest way to write one and the hardest way to get it
wrong. Shipped as written, a student who always taps A scores full marks on
all 1,340 of them. This module reorders the options once, centrally, before
anything is built, so that the quiz on the page, the JSON-LD on the page and
the answer key on the printable worksheet all see the same arrangement.

The arrangement is deterministic. It is seeded from the topic, so the same
content gives the same page on every build and a diff between two deploys
shows only what was actually edited.

What it does, in order of how much it matters:

  Balance. Within each topic the correct answers are spread across A to D as
  evenly as the question count allows, and never three in a row. Pure
  randomness would do neither: ten fair coin tosses land on one side seven
  times often enough that a quiz would look rigged.

  Pinned options. "Both", "Neither" and "None of them" only read sensibly
  after the options they refer to, so they keep their place at the end and
  the arrangement works around them.

  Numbers stay in order. Where every option is a plain number the options are
  sorted ascending, as an exam paper prints them, and the correct answer goes
  wherever its value puts it. Those questions are counted when the rest are
  balanced, so a topic full of them still comes out even.
"""
import hashlib
import random
import re
from collections import Counter
from decimal import Decimal, InvalidOperation

LETTERS = "ABCDEFGH"

# Options that refer to other options. They stay last, in their original order.
_PIN = re.compile(
    r"^\s*(both|neither)(\s+of\s+(them|these))?\s*[.,]?\s*$"
    r"|^\s*(all|none)\s+of\s+(them|these|the\s+above|the\s+options)\b",
    re.I)

# A plain number: digits, thousands commas, an optional decimal part and an
# optional percent sign. Units are deliberately not accepted, because ordering
# "700 MB" against "4.7 GB" needs a conversion this module does not attempt.
_NUMBER = re.compile(r"^[-+]?\d[\d,]*(\.\d+)?%?$")


def _value(text):
    """The numeric value of a plain-number option, or None."""
    t = text.strip()
    if not _NUMBER.match(t):
        return None
    try:
        return Decimal(t.replace(",", "").rstrip("%"))
    except InvalidOperation:
        return None


def _rng(seed):
    return random.Random(int(hashlib.sha256(seed.encode("utf-8")).hexdigest(), 16))


def _plan(q):
    """Work out how one question's options are constrained.

    Returns (kind, data):
      ("numeric", order)   every option is a number; `order` is the new order
      ("pinned", info)     the correct answer is itself a pinned option
      ("free", info)       the correct answer can go in any unpinned slot
    """
    opts = q.options
    values = [_value(o) for o in opts]
    if all(v is not None for v in values) and len(set(values)) > 1:
        order = sorted(range(len(opts)), key=lambda i: (values[i], i))
        return "numeric", order
    pinned = [i for i, o in enumerate(opts) if _PIN.search(o)]
    free = [i for i in range(len(opts)) if i not in pinned]
    if q.answer in pinned:
        return "pinned", (free, pinned)
    return "free", (free, pinned)


def _score(pos):
    """Lower is better: triples first, then lopsidedness, then adjacent pairs."""
    triples = sum(1 for i in range(len(pos) - 2) if pos[i] == pos[i + 1] == pos[i + 2])
    pairs = sum(1 for i in range(len(pos) - 1) if pos[i] == pos[i + 1])
    counts = Counter(pos)
    spread = max(counts.values()) - min(counts.get(p, 0) for p in range(max(pos) + 1))
    return (triples, spread, pairs)


def _targets(rng, forced, limit):
    """Choose a position for every question that is free to be anywhere.

    `forced[i]` is a fixed position or None; `limit[i]` is how many slots
    question i can use. Several randomised greedy passes are tried and the best
    kept, so the result is balanced without being a visible pattern.
    """
    n = len(forced)
    best = None
    for _ in range(60):
        pos = list(forced)
        used = Counter(p for p in pos if p is not None)
        order = [i for i in range(n) if pos[i] is None]
        rng.shuffle(order)
        for i in order:
            cands = list(range(limit[i]))
            rng.shuffle(cands)
            cands.sort(key=lambda p: used[p])          # stable: ties stay random
            pos[i] = cands[0]
            used[cands[0]] += 1
        score = _score(pos)
        if best is None or score < best[0]:
            best = (score, pos)
        if score[0] == 0 and score[1] <= 1 and score[2] <= max(1, n // 4):
            break
    return best[1]


def arrange_topic(topic, seed):
    """Reorder the options of every question in one topic, in place."""
    qs = [q for q in topic.quiz if not getattr(q, "arranged", False)]
    if not qs:
        return
    rng = _rng(seed)
    plans = [_plan(q) for q in qs]

    forced, limit = [], []
    for q, (kind, data) in zip(qs, plans):
        if kind == "numeric":
            forced.append(data.index(q.answer))
            limit.append(len(q.options))
        elif kind == "pinned":
            free, pinned = data
            forced.append(len(free) + pinned.index(q.answer))
            limit.append(len(q.options))
        else:
            free, _ = data
            forced.append(None)
            limit.append(len(free))
    target = _targets(rng, forced, limit)

    for q, (kind, data), t in zip(qs, plans, target):
        opts = q.options
        if kind == "numeric":
            new = [opts[i] for i in data]
            q.answer = data.index(q.answer)
        elif kind == "pinned":
            free, pinned = data
            body = [opts[i] for i in free]
            rng.shuffle(body)
            new = body + [opts[i] for i in pinned]
            q.answer = len(free) + pinned.index(q.answer)
        else:
            free, pinned = data
            correct = opts[q.answer]
            others = [opts[i] for i in free if i != q.answer]
            rng.shuffle(others)
            slots = [None] * len(free)
            slots[t] = correct
            it = iter(others)
            slots = [s if s is not None else next(it) for s in slots]
            new = slots + [opts[i] for i in pinned]
            q.answer = t
        q.options = new
        q.arranged = True


def apply(course):
    """Arrange every quiz in a course."""
    for unit in course.units:
        for topic in unit.topics:
            arrange_topic(topic, "%s/%s" % (course.slug, topic.slug))


def histogram(courses):
    """Counts of where the correct answer sits, over every question."""
    c = Counter()
    for course in courses:
        for unit in course.units:
            for topic in unit.topics:
                for q in topic.quiz:
                    c[q.answer] += 1
    return c


def check(courses):
    """Fail the build if the arrangement did not happen or came out lopsided.

    A quiz written correct answer first and never passed through apply() looks
    perfectly fine on the page until a student notices, so this is the guard
    that stops it quietly coming back.
    """
    problems = []
    for course in courses:
        for unit in course.units:
            for topic in unit.topics:
                qs = topic.quiz
                if len(qs) < 4:
                    continue
                where = "%s/%s" % (course.slug, topic.slug)
                if not all(getattr(q, "arranged", False) for q in qs):
                    problems.append("%s: quiz was never arranged" % where)
                    continue
                pos = [q.answer for q in qs]
                counts = Counter(pos)
                top, n = counts.most_common(1)[0]
                if len(qs) >= 6 and n > 0.6 * len(qs):
                    problems.append("%s: %d of %d correct answers are %s"
                                    % (where, n, len(qs), LETTERS[top]))
                for i in range(len(pos) - 2):
                    if pos[i] == pos[i + 1] == pos[i + 2]:
                        problems.append("%s: three correct answers in a row at "
                                        "question %d (%s)" % (where, i + 1, LETTERS[pos[i]]))
                        break
    if problems:
        raise SystemExit("Quiz answer placement:\n  " + "\n  ".join(problems[:20]))
    hist = histogram(courses)
    total = sum(hist.values())
    return "  ".join("%s %.1f%%" % (LETTERS[k], 100.0 * hist[k] / total)
                     for k in sorted(hist)), total
