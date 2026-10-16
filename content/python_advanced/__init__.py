"""Advanced Python skills, beyond the exam specifications.

One module per topic, grouped into units in content/python_course.py.
INPUTS and EXPECT are only read by tools/check_python_examples.py.
"""
MODULES = []
TOPICS = [m.TOPIC for m in MODULES]
INPUTS = {m.TOPIC.slug: getattr(m, "INPUTS", {}) for m in MODULES}
EXPECT = {m.TOPIC.slug: getattr(m, "EXPECT", {}) for m in MODULES}
