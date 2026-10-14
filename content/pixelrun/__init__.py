"""Pixel Run: a platformer where every obstacle is a Python function to write.

LEVELS are the ten stages, BANK is the fifty challenges (five per level), and
validate_all() is the proof that the bank is sound. The build runs it every time.
"""
from .bank_a import BANK as _A
from .bank_b import BANK as _B
from .levels import LEVELS
from .model import BankError, fallback, test_records, validate

BANK = _A + _B


def validate_all(verbose=False):
    """Raise BankError unless all fifty challenges are structurally and logically sound."""
    problems = []
    ids = [c.id for c in BANK]
    for dup in sorted({i for i in ids if ids.count(i) > 1}):
        problems.append("duplicate challenge id: %s" % dup)
    for lv in LEVELS:
        n = sum(1 for c in BANK if c.level == lv.n)
        if n != 5:
            problems.append("level %d has %d challenges, not five" % (lv.n, n))
    for c in BANK:
        for p in validate(c):
            problems.append("%s: %s" % (c.id, p))
        if verbose:
            print("  ok  %-20s level %d" % (c.id, c.level))
    if problems:
        raise BankError("Pixel Run challenge bank is not sound:\n  " + "\n  ".join(problems))
    return len(BANK)
