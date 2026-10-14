"""Where the concept illustrations go, topic by topic and board by board.

OCR, AQA, Edexcel, Key Stage 3 and the Python course teach the same variable,
the same loop and the same translator, so one drawing is placed on every topic
that teaches it. Each call below adds one or more illustrations to the end of a
named section.

This is written as calls rather than as a big dictionary on purpose. A dict
literal silently keeps only the last of a repeated key, which already lost
diagrams from pages twice; a call that adds to what is there cannot.
placements.apply() still raises if a topic or a section named here does not
exist, so a typo fails the build instead of dropping a picture.
"""

OCR = "ks4/computer-science"
AQA = "ks4/aqa-computer-science"
EDX = "ks4/edexcel-computer-science"
KS3 = "ks3"
IMEDIA = "ks4/imedia"
ALEVEL = "ks5"
DATA = "data-analytics"
PY = "python"

PLAN = {}
_SEEN = set()


def put(course, topic, section, *names):
    """Add illustrations to the end of a section."""
    for name in names:
        key = (course, topic, name)
        if key in _SEEN:
            raise ValueError("illustration %r is placed twice on %s/%s" % (name, course, topic))
        _SEEN.add(key)
        PLAN.setdefault((course, topic), {}).setdefault(section, []).append("!illus " + name)


def merge(into):
    """Fold the plan into the main placement table without replacing anything."""
    for key, sections in PLAN.items():
        target = into.setdefault(key, {})
        for title, items in sections.items():
            target.setdefault(title, []).extend(items)


# ================================================================ programming
# ---- OCR GCSE
put(OCR, "programming-fundamentals", "Variables and constants", "variables-boxes")
put(OCR, "programming-fundamentals", "The three constructs", "three-constructs")
put(OCR, "programming-fundamentals", "Operators", "operators")
put(OCR, "data-types-and-casting", "The five data types", "data-types")
put(OCR, "additional-programming-techniques", "String manipulation", "strings-tiles")
put(OCR, "additional-programming-techniques", "Arrays and lists", "lists-lockers")
put(OCR, "additional-programming-techniques", "File handling", "files-flow")
put(OCR, "additional-programming-techniques", "Subroutines and random numbers", "function-machine")
put(OCR, "producing-robust-programs", "Defensive design", "validation-checks", "authentication")
put(OCR, "producing-robust-programs", "Testing", "error-types", "test-data")
put(OCR, "languages-and-ides", "High and low level languages", "language-levels")
put(OCR, "languages-and-ides", "Translators", "translators")
put(OCR, "languages-and-ides", "Integrated development environments", "ide-tour")

# ---- AQA GCSE
put(AQA, "programming-fundamentals", "Data types", "data-types")
put(AQA, "programming-fundamentals", "Variables and constants", "variables-boxes")
put(AQA, "programming-fundamentals", "Operators", "operators")
put(AQA, "programming-fundamentals", "The three constructs", "three-constructs")
put(AQA, "data-structures-and-file-handling", "String handling", "strings-tiles")
put(AQA, "data-structures-and-file-handling", "Files and random numbers", "files-flow")
put(AQA, "subroutines-and-structured-programming", "Procedures and functions", "function-machine")
put(AQA, "subroutines-and-structured-programming", "Scope", "scope-rooms")
put(AQA, "robust-and-secure-programming", "Validation and authentication", "validation-checks", "authentication")
put(AQA, "robust-and-secure-programming", "Testing and the three kinds of error", "error-types", "test-data")
put(AQA, "classification-of-programming-languages", "High and low level languages", "language-levels")
put(AQA, "classification-of-programming-languages", "Translators", "translators")

# ---- Edexcel GCSE
put(EDX, "programming-fundamentals-in-python", "Variables, constants and data types", "variables-boxes", "data-types")
put(EDX, "programming-fundamentals-in-python", "Operators", "operators")
put(EDX, "programming-fundamentals-in-python", "Sequence, selection and iteration", "three-constructs", "selection-fork", "loops-track")
put(EDX, "lists-strings-and-files-in-python", "Lists", "lists-lockers")
put(EDX, "lists-strings-and-files-in-python", "Strings", "strings-tiles")
put(EDX, "lists-strings-and-files-in-python", "Files", "files-flow")
put(EDX, "developing-and-testing-programs", "Subprograms", "function-machine")
put(EDX, "developing-and-testing-programs", "Validation, authentication and testing", "validation-checks", "authentication", "test-data")
put(EDX, "software-and-programming-languages", "Programming languages and translators", "language-levels", "translators")

# ---- Key Stage 3
put(KS3, "introduction-to-python", "Output and variables", "hello-world", "variables-boxes")
put(KS3, "introduction-to-python", "Input and data types", "input-types")
put(KS3, "introduction-to-python", "Making decisions", "selection-fork")
put(KS3, "python-loops-and-lists", "Loops", "loops-track")
put(KS3, "python-loops-and-lists", "Lists", "lists-lockers")
put(KS3, "python-loops-and-lists", "Functions and validation", "function-machine", "validation-checks")
put(KS3, "python-programming", "Structuring a program", "scope-rooms")
put(KS3, "python-programming", "Lists, 2D lists and dictionaries", "dictionary-drawers")
put(KS3, "python-programming", "Files and building a real program", "files-flow")

# ---- A Level
put(ALEVEL, "applications-generation", "Translators and the stages of compilation", "translators")

# ---- the Python course
put(PY, "first-steps", "Your first program", "hello-world")
put(PY, "first-steps", "Reading error messages", "error-types")
put(PY, "variables-and-data-types", "Variables", "variables-boxes")
put(PY, "variables-and-data-types", "Data types", "data-types")
put(PY, "input-and-operators", "Input", "input-types")
put(PY, "input-and-operators", "Operators", "operators")
put(PY, "selection", "Making a decision", "selection-fork")
put(PY, "loops", "for loops", "loops-track")
put(PY, "string-manipulation", "Indexing and slicing", "strings-tiles")
put(PY, "lists", "Lists", "lists-lockers")
put(PY, "functions", "Defining and calling", "function-machine")
put(PY, "functions", "Scope", "scope-rooms")
put(PY, "dictionaries-files-and-errors", "Dictionaries", "dictionary-drawers")
put(PY, "dictionaries-files-and-errors", "Files", "files-flow")
put(PY, "dictionaries-files-and-errors", "Error handling", "try-except")
put(PY, "validation-authentication-and-testing", "Validation and sanitisation", "validation-checks")
put(PY, "validation-authentication-and-testing", "Authentication", "authentication")
put(PY, "tracing-and-debugging", "Finding and fixing errors", "error-types")
put(PY, "tracing-and-debugging", "Debugging tools and techniques", "ide-tour")
put(PY, "subprograms-and-parameters", "Procedures and functions", "function-machine")
put(PY, "arrays-records-and-files", "One dimensional arrays", "lists-lockers")
put(PY, "arrays-records-and-files", "Text files", "files-flow")
put(PY, "pseudocode-to-python", "Data types, casting and operators", "data-types", "operators")
