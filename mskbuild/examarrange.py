"""Place the correct answer of every tick box question so that no letter is favoured.

Questions are written with the options in whatever order reads naturally, and
that order nearly always puts the answer near the top. Left alone, a student who
always ticks B would beat one who knows the work. Within each paper, every
single answer question has its key moved to the least used letter so far (ties
broken by a generator seeded with the paper's slug, so every build is the same),
and the other options are shuffled around it. Questions whose options are all
numbers keep the order they were written in, because a number line reads best in
order. Each question is arranged once, however many times this runs.
"""
import collections
import random
import re

_NUMERIC = re.compile(r"^\s*-?[\d.,]+")


def _numeric(options):
    return all(_NUMERIC.match(o) for o in options)


def arrange(paper):
    rng = random.Random("msk:" + paper.slug)
    used = collections.Counter()
    for q in paper.questions:
        if q.kind != "choice":
            continue
        n = len(q.options)
        if getattr(q, "_arranged", False) or _numeric(q.options):
            q._arranged = True
            for c in q.correct:
                used[c] += 1
            continue
        if len(q.correct) == 1:
            least = min(used[i] for i in range(n))
            target = rng.choice([i for i in range(n) if used[i] == least])
            key = q.options[q.correct[0]]
            others = [o for i, o in enumerate(q.options) if i != q.correct[0]]
            rng.shuffle(others)
            others.insert(target, key)
            q.options, q.correct = others, [target]
        else:
            order = list(range(n))
            rng.shuffle(order)
            q.options = [q.options[i] for i in order]
            q.correct = sorted(order.index(c) for c in q.correct)
        for c in q.correct:
            used[c] += 1
        q._arranged = True


def arrange_all(papers):
    for p in papers:
        arrange(p)
