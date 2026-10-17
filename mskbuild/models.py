"""Content model for the MskProd Computing revision site."""
from dataclasses import dataclass, field
from typing import Dict, List, Tuple, Optional


@dataclass
class Q:
    """One multiple choice knowledge-check question."""
    stem: str
    options: List[str]
    answer: int          # index of the correct option
    explain: str         # shown after answering, whatever the student picked
    # Content is written correct answer first. quizshuffle.apply() reorders the
    # options once before the build and sets this, so it can never run twice.
    arranged: bool = False


@dataclass
class MP:
    """One mark point in a mark scheme.

    `text` is what the examiner is looking for, written the way a real mark
    scheme writes it. `any` lists acceptable phrasings the auto marker will
    accept for that point.
    """
    text: str
    any: List[str]


@dataclass
class Blank:
    """One box a student types an answer into, marked exactly.

    `accept` lists every answer an examiner would credit. Comparison ignores
    case, spaces and a trailing full stop; a numeric blank compares values, so
    0.5, .5 and 0.50 are the same answer.
    """
    accept: List[str]
    label: str = ""           # printed in front of the box
    unit: str = ""            # printed after the box, eg "MB"
    numeric: bool = False
    tol: float = 0.0          # absolute tolerance for a numeric blank
    width: int = 8            # roughly how many characters the box should show


@dataclass
class Check:
    """One mark point of a programming question, proved by running the program.

    `expr` is a Python expression evaluated by mskbuild/codemark.py against the
    student's program, for example `has(run(["4", "5"]), "9")`. It is worth one
    mark. The same file runs the check in the build, where the model solution
    must pass it, and in the browser, where the student's code is marked.
    """
    text: str                 # the mark scheme line, as an examiner would write it
    expr: str


@dataclass
class CodeTask:
    """A program to write or amend, marked by running it (Python 3, or one SQL statement)."""
    starter: str              # the code file the student is given
    solution: str             # a complete answer: must pass every check
    checks: List[Check]
    # Plausible wrong answers. Each must lose at least one mark, which proves
    # the checks can tell a near miss from a correct answer.
    wrong: List[str] = field(default_factory=list)
    files: Dict[str, str] = field(default_factory=dict)   # data files the program may open
    filename: str = "answer.py"                            # the name of the code file, as printed
    lang: str = "python"      # or "sql": one statement, run against the database below
    setup: str = ""           # for SQL, the script that creates and fills the tables


@dataclass
class EQ:
    """One exam-style question.

    Most questions are written answers, marked against mark points. A paper can
    also use the closed formats the real papers print, each marked exactly:

      choice   tick one box, or tick n boxes; `options` and `correct` (indexes)
      matrix   one tick per row of a table; `rows`, `cols` and `correct` (a
               column index per row)
      blanks   boxes to type into, optionally laid out as a table (`grid`, with
               an int in a cell meaning blank number n); `working` adds a box
               for method, and `points` then hold the method marks
      code     a program to write or amend, marked by running it (`code`)
    """
    stem: str
    marks: int
    points: List[MP]
    model: str
    command: str = ""     # describe / explain / compare / justify ...
    # Resource material printed with the question: a chart to read, a table
    # to find the faults in, a confusion matrix to calculate from. Written in
    # the same mini-markup as topic content, so "!diagram <name>" works here.
    figure: str = ""
    kind: str = "text"
    options: List[str] = field(default_factory=list)
    correct: List[int] = field(default_factory=list)
    rows: List[str] = field(default_factory=list)
    cols: List[str] = field(default_factory=list)
    blanks: List[Blank] = field(default_factory=list)
    grid: List[list] = field(default_factory=list)      # rows of cells: str, or int for a blank
    grid_head: List[str] = field(default_factory=list)
    # Several blanks that earn one mark together, eg "1 mark per correct row".
    # Each entry is (mark scheme text, [blank numbers]). Without groups every
    # blank is worth a mark of its own.
    groups: List[Tuple[str, List[int]]] = field(default_factory=list)
    working: bool = False
    code: Optional[CodeTask] = None
    # Paper layout: the printed question number ("1(a)", "03.2"), the shared
    # context of a question's parts, printed above it, and a section heading.
    label: str = ""
    lead: str = ""
    section: str = ""
    section_note: str = ""


@dataclass
class Section:
    title: str
    body: str            # mini-markup, parsed at build time
    id: str = ""


@dataclass
class Topic:
    slug: str
    title: str
    blurb: str
    sections: List[Section]
    quiz: List[Q] = field(default_factory=list)
    exam: List[EQ] = field(default_factory=list)
    spec: str = ""
    icon: str = "i-book"
    keyterms: List[Tuple[str, str]] = field(default_factory=list)
    grade: str = ""            # how to reach the top grade on this topic
    mistakes: List[str] = field(default_factory=list)
    fact: str = ""             # a Pixel fun fact tied to this topic
    minutes: int = 25
    # R094 and R097 are internally assessed: there is no written paper, so
    # their written practice is not called "exam-style questions".
    exam_title: str = "Exam-style questions"


@dataclass
class Unit:
    slug: str
    title: str
    blurb: str
    topics: List[Topic]
    icon: str = "i-book"
    term: str = ""             # eg "Year 7, Autumn 1"


@dataclass
class Course:
    slug: str
    title: str
    short: str
    blurb: str
    intro: str
    units: List[Unit]
    icon: str = "i-book"
    accent: str = "var(--teal)"
    stage: str = ""            # KS3 / KS4 / KS5
    board: str = ""
    code: str = ""
    goal: str = ""             # the top grade for this course
    # The phrase a student actually types into Google for this course. Exam
    # board plus specification code is the highest intent search there is:
    # somebody searching "OCR J277 boolean logic" wants exactly our page, and
    # the code appeared in no page title at all before. Kept short, because a
    # title has about sixty characters before Google truncates it and the
    # topic name has to survive that cut.
    seo: str = ""
    journey: List[Tuple[str, str, str]] = field(default_factory=list)
    # One extra button in the course hero: (label, href, icon). The Python
    # course uses it to point at the game that practises it.
    extra_cta: Tuple[str, str, str] = ()


@dataclass
class Paper:
    """One practice examination paper.

    Lives here rather than in content/papers.py so that the modules defining
    papers can import it without importing the module that collects them,
    which was a circular import waiting to be tripped over.
    """
    slug: str
    title: str
    course: str
    board: str
    code: str
    minutes: int
    marks: int
    blurb: str
    advice: str
    questions: List[EQ]
    calculator: str = "No calculator is permitted."
    accent: str = "var(--teal)"
    # Grouping on the papers page: "J277", "8525", "1CP2", "H446", "R093",
    # "F200", "F201", "KS3".
    spec: str = ""
    # A full length paper: its marks and time allowed are the real paper's,
    # and the build checks them against the official figures.
    full: bool = False
    # Extra lines for the front cover, worded as the real paper words them.
    instructions: List[str] = field(default_factory=list)
    # Key Stage 3 unit exams: the topic slug of the unit the exam belongs to.
    unit: str = ""
