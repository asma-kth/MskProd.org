"""Stretch tasks for every Key Stage 4 lesson.

At Key Stage 4 a lesson is a whole topic page, and it gets four tasks: the
three Key Stage 3 has, and Sort It. Each module holds the lessons for some of
one course's topics: it defines COURSE, the course's slug, and LESSONS, one
Stretch per topic, whose `lesson` is the topic's slug.

A course is published once every one of its lessons is written, which is
what `complete` records. While a course is being written, setting
STRETCH_DRAFT=1 builds its finished lessons too, to try them out.
"""
import importlib
import os

# key in URLs and saved results, course slug, name on the pages, modules, complete
COURSES = [
    ("ocr", "ks4/computer-science", "OCR J277 GCSE Computer Science", ["ocr_systems_architecture", "ocr_memory_storage", "ocr_data_representation", "ocr_networks", "ocr_software_impacts", "ocr_algorithms", "ocr_programming", "ocr_robust_logic_languages"], True),
    ("aqa", "ks4/aqa-computer-science", "AQA 8525 GCSE Computer Science", ["aqa_algorithms", "aqa_programming", "aqa_data", "aqa_systems", "aqa_networks_security", "aqa_databases_impacts"], True),
    ("edexcel", "ks4/edexcel-computer-science", "Pearson Edexcel 1CP2 GCSE Computer Science", ["edexcel_thinking"], False),
    ("imedia", "ks4/imedia", "OCR J834 Creative iMedia", [], False),
]

# Topics that are not lessons: the guides to Creative iMedia's assessed
# coursework tasks, which say how to do the assignment rather than teach.
NOT_LESSONS = {
    ("ks4/imedia", "r094-task-1-visual-identity"),
    ("ks4/imedia", "r094-task-2-digital-graphics"),
    ("ks4/imedia", "r097-task-1-planning-interactive-media"),
    ("ks4/imedia", "r097-task-2-creating-interactive-media"),
    ("ks4/imedia", "r097-task-3-reviewing-interactive-media"),
}


def draft():
    return bool(os.environ.get("STRETCH_DRAFT"))


def courses():
    """The courses whose lessons go on the site: the complete ones, and in
    draft mode the rest too. [(key, course slug, name, [Stretch])]"""
    out = []
    for key, slug, name, modules, complete in COURSES:
        if not (complete or draft()):
            continue
        lessons = []
        for m in modules:
            mod = importlib.import_module("content.ks4_stretch." + m)
            if mod.COURSE != slug:
                raise SystemExit("content/ks4_stretch/%s.py says it belongs to %s, not %s" % (m, mod.COURSE, slug))
            lessons += mod.LESSONS
        out.append((key, slug, name, lessons))
    return out


def complete(slug):
    return any(c[1] == slug and c[4] for c in COURSES)
