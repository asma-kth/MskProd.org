"""GCSE Computer Science, taught through Python.

One module per topic. TOPICS is the teaching order, and content/python_course.py
builds the GCSE unit from it. INPUTS is only read by tools/check_python_examples.py.
"""
from . import pseudocode, arrays, subprograms, robust, sql, algorithms, tracing

MODULES = [
    pseudocode,
    arrays,
    subprograms,
    robust,
    sql,
    algorithms,
    tracing,
]
TOPICS = [m.TOPIC for m in MODULES]
INPUTS = {m.TOPIC.slug: getattr(m, "INPUTS", {}) for m in MODULES}
EXPECT = {m.TOPIC.slug: getattr(m, "EXPECT", {}) for m in MODULES}
