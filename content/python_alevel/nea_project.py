"""A Level Python: planning, building, testing and evaluating the programming project."""
from mskbuild.models import Topic, Section, Q, EQ, MP

INPUTS = {}
EXPECT = {}

TOPIC = Topic(
    slug="programming-project",
    title="The Programming Project (NEA)",
    spec="A Level 13",
    icon="i-flag",
    minutes=60,
    exam_title="Check you could explain this",
    blurb="How the independent project is judged, and a worked example of every stage: analysis with measurable success criteria, design before code, a working solution built in small tested steps, unit tests, and an evaluation that argues from evidence.",
    fact="The project is worth a fifth of the A Level and is the part of the course where every student has the same chance to beat the exam: the marks are for work you can plan, and none of it is lost to nerves. The students who do best usually start it earlier than they think they need to.",
    sections=[
        Section("What the project rewards", r"""
The programming project is **non exam assessment**: you choose a real problem, solve it by writing a program, and document the whole process. It is worth **20 per cent** of both the OCR (H446) and AQA (7517) A Levels. Check your own board's current specification for the exact mark allocation, but every board marks the same five stages.

| Stage | A top mark answer shows | The usual weakness |
| **Analysis** | A clear problem, **real stakeholders** who were consulted, research into existing solutions, and success criteria that can be **measured** | A description of the program instead of the problem |
| **Design** | The problem **decomposed**, algorithms and data structures chosen and explained, interfaces drawn, and a **test plan written before coding** | Design drawn after the code was finished |
| **Development** | A solution built in **stages**, with evidence of each, in code that is modular, validated, annotated and makes use of appropriate techniques | One long program, with no record of how it grew |
| **Testing** | A systematic test plan run against the solution, with evidence, and **faults found and fixed**, shown | Testing that only shows the program working |
| **Evaluation** | Each success criterion judged against **evidence**, stakeholder feedback, limitations stated honestly, and improvements suggested | "It works well and I am happy with it" |

### Choosing the project

The project is marked on the **technical difficulty** of what you build as well as on how well you document it. A good project:

- has a **real user** who will tell you what they need and tell you if you got it right
- needs more than a form that saves to a file. Look for a **real algorithm or data structure**: a graph, a tree, a queue, a recursive solution, a database with several linked tables, a simulation
- is **small enough to finish**. A working, tested solution to a modest problem beats an unfinished plan for a huge one

!warn Do not borrow the solution :: Using code you did not write is allowed only if it is clearly identified, and the marks are for your own work. A library such as `sqlite3` is a tool. A tutorial program with the names changed is plagiarism, and the boards check.

### Keeping the evidence

The documentation is not an extra written afterwards. It is made **as you go**.

| Habit | Why |
| A **project diary**, dated, of what you did, what went wrong and how you fixed it | It becomes the evidence of iterative development, and it is the best source for the evaluation |
| **Screenshots** with annotations, after each stage | Marks cannot be given for work that is not shown |
| **Version control**, with small commits and clear messages | A history of the code, and a way back from a mistake |
| **Backups** in two places | A lost project cannot be marked |
| A **time plan** that you revisit | The project has a deadline and you do not control it |
"""),
        Section("Analysis and design: a worked brief", r"""
A worked example runs through the rest of this topic, a program that is small enough to read in full but has the features a real project needs. The problem is **revision**: students forget what they have learned, and revise by re reading, which does not help them remember.

### Analysis

**The problem.** A student revising for several exams wants to practise recalling facts, and to spend time on the facts they are most likely to forget, instead of the ones they already know.

**Stakeholders.** Students revising for A Levels, who use the program, and a teacher who may recommend it. A questionnaire to twenty students, and an interview with a teacher, would give the requirements. It matters to write down what they said and what you decided as a result.

**Research.** Paper flashcards have no memory of which cards are hard. Some apps use **spaced repetition**: the better you know a card, the longer until it is shown again. The **Leitner system** does it with boxes. A new card is in box 1. Answer it correctly and it moves up a box, wrong and it returns to box 1. The higher the box, the longer the gap before it is due again.

**Success criteria.** These are the heart of the analysis, because the evaluation will judge the finished program against **each one**. A good criterion is **measurable**: someone else can test it and agree whether it was met.

| No. | Success criterion |
| S1 | A card with a question and an answer can be added. A blank question or answer, or a question already in the deck, is refused with a clear message |
| S2 | A card answered correctly moves up one box, to a maximum of box 5, and is next due after 1, 2, 4, 8 or 16 days for boxes 1 to 5 |
| S3 | A card answered wrongly goes back to box 1 and is due the next day |
| S4 | Only the cards due today are offered for review, with the lowest boxes first |
| S5 | The cards survive closing the program |
| S6 | A summary shows how many cards are in each box |

Compare "the program should be easy to use", which no one can say they have measured, with S2, which can be checked in a minute.

### Design

**Decomposition.** Break the problem into parts that can be built and tested separately.

!diagram py-nea-structure

**Data.** Cards are stored in a database table, so they survive (S5) and can be searched by due date.

| Column | Type | Rule |
| `card_id` | integer | primary key |
| `question` | text | not empty, and unique, for S1 |
| `answer` | text | not empty |
| `box` | integer | between 1 and 5 |
| `due` | text, in the form 2025-03-01 | the date the card is next shown |

**Algorithm.** Written in pseudocode before any Python:

```pseudo
procedure record(card, correct, today)
    if correct then
        card.box = min(card.box + 1, 5)
    else
        card.box = 1
    endif
    card.due = today + interval[card.box] days
endprocedure
```

**Test plan**, written now and not after:

| Test | Purpose | Data | Expected |
| T1 | Add a card (S1) | "What is RAM?" and "Memory" | Added |
| T2 | Blank question refused (S1, erroneous) | Question of three spaces | Refused, with a message |
| T3 | Duplicate refused (S1) | The same question twice | Second is refused |
| T4 | Correct answer in box 1 (S2) | Box 1, answered right | Box 2, due in 2 days |
| T5 | Correct answer in box 5 (S2, boundary) | Box 5, answered right | Stays in box 5, due in 16 days |
| T6 | Wrong answer in box 4 (S3) | Box 4, answered wrong | Box 1, due in 1 day |
| T7 | Only due cards offered (S4) | Cards due today and tomorrow | Only today's offered |
"""),
        Section("Development: a working solution in small steps", r"""
Build it in **stages**, and make each stage work and be tested before the next begins. Stage 1 is storage. Stage 2 is the rules of the boxes. Stage 3 is the review. The interface comes last, because the parts it depends on are then known to be right.

The program below is the solution so far, as it might appear in the final version, and a short demonstration of three days of use. Read the code before you run it, and notice what is in it that is there for the marks.

```python
import sqlite3
from datetime import date, timedelta

BOX_INTERVALS = {1: 1, 2: 2, 3: 4, 4: 8, 5: 16}     # days until a card is due again
MAX_BOX = 5


class DeckError(Exception):
    '''Raised when the user asks the deck to do something it cannot.'''


class Deck:
    '''A set of flashcards stored in a database, using the Leitner system.'''

    def __init__(self):
        self.db = sqlite3.connect(":memory:")
        self.db.execute('''CREATE TABLE card (
            card_id INTEGER PRIMARY KEY,
            question TEXT NOT NULL UNIQUE,
            answer TEXT NOT NULL,
            box INTEGER NOT NULL DEFAULT 1 CHECK (box BETWEEN 1 AND 5),
            due TEXT NOT NULL)''')

    def add(self, question, answer, today):
        '''Add a card, due today. Refuses a blank or duplicate question.'''
        question, answer = question.strip(), answer.strip()
        if not question or not answer:
            raise DeckError("a card needs a question and an answer")
        try:
            self.db.execute("INSERT INTO card (question, answer, due) VALUES (?, ?, ?)",
                            (question, answer, today.isoformat()))
        except sqlite3.IntegrityError:
            raise DeckError("that question is already in the deck")
        self.db.commit()

    def due(self, today):
        '''The cards to be reviewed today, lowest box first.'''
        rows = self.db.execute(
            "SELECT card_id, question, box FROM card WHERE due <= ? ORDER BY box, card_id",
            (today.isoformat(),))
        return rows.fetchall()

    def record(self, card_id, correct, today):
        '''Move a card after it has been answered, and return its new box and due date.'''
        (box,) = self.db.execute("SELECT box FROM card WHERE card_id = ?", (card_id,)).fetchone()
        box = min(box + 1, MAX_BOX) if correct else 1
        due = today + timedelta(days=BOX_INTERVALS[box])
        self.db.execute("UPDATE card SET box = ?, due = ? WHERE card_id = ?",
                        (box, due.isoformat(), card_id))
        self.db.commit()
        return box, due

    def summary(self):
        '''How many cards are in each box.'''
        return self.db.execute("SELECT box, COUNT(*) FROM card GROUP BY box ORDER BY box").fetchall()


day1 = date(2025, 3, 1)
deck = Deck()
deck.add("What does CPU stand for?", "Central processing unit", day1)
deck.add("What is the base of hexadecimal?", "16", day1)
deck.add("Which sort has an O(n log n) worst case?", "Merge sort", day1)

for bad in [("   ", "blank"), ("What is the base of hexadecimal?", "sixteen")]:
    try:
        deck.add(bad[0], bad[1], day1)
    except DeckError as error:
        print("refused:", error)

print("Day 1, due:", len(deck.due(day1)))
deck.record(1, True, day1)
deck.record(2, True, day1)
deck.record(3, False, day1)
print("after day 1:", deck.summary())

day2 = day1 + timedelta(days=1)
print("Day 2, due:", [q for _, q, _ in deck.due(day2)])
box, due = deck.record(3, True, day2)
print("card 3 is now in box", box, "due", due.isoformat())

day3 = day2 + timedelta(days=1)
for card_id, question, box in deck.due(day3):
    deck.record(card_id, True, day3)
print("after day 3:", deck.summary())
```

### What the code shows, for the marks

| Feature | Where | Why it earns credit |
| **Meaningful names** and a **constant** | `BOX_INTERVALS`, `MAX_BOX`, `due`, `record` | The code reads like the design, and the rules are changed in one place |
| **Docstrings** and comments | The triple quoted lines | Another programmer, or a marker, can see what each part is for |
| **Classes**, one job each | `Deck` holds the data and the rules | A coherent, maintainable structure |
| **Validation** that refuses bad data | `add` checks for blank and duplicate questions, S1 | Robust against the erroneous data in the test plan |
| A **custom exception** | `DeckError` | A clear signal to the interface, which decides how to tell the user |
| **Parameterised SQL** | Every `?` | No SQL injection, and no quoting errors |
| An appropriate **data structure** | A dictionary of intervals, a database table | The choices are justified in the design |
| Dates in **ISO form** | `2025-03-01` | They sort and compare correctly as text, which the `due <= ?` test relies on |

### A development log

This is the sort of dated entry that turns into evidence of **iterative development**. It records the problem as well as the progress.

| Date | Stage | What I did | Problem found | How I fixed it |
| 3 Oct | 1. Storage | Created the table and `add` | Two cards with the same question were accepted | Added `UNIQUE` and caught `IntegrityError` |
| 10 Oct | 2. Rules | Wrote `record` | A card in box 5 moved to box 6 and caused a key error | Used `min(box + 1, MAX_BOX)` after test T5 |
| 17 Oct | 3. Review | Wrote `due` | Cards due tomorrow were being offered | The comparison was `<` instead of `<=`, and after fixing it test T7 passed |
"""),
        Section("Testing and evaluation", r"""
### Run the plan

Testing is where the plan from the design is **carried out and recorded**. Python's `unittest` can run the plan, and the output is the evidence. The program repeats the `Deck` class so that it runs on its own, and then runs the tests from the plan.

```python
import sqlite3
import unittest
from datetime import date, timedelta

BOX_INTERVALS = {1: 1, 2: 2, 3: 4, 4: 8, 5: 16}
MAX_BOX = 5

class DeckError(Exception):
    pass

class Deck:
    def __init__(self):
        self.db = sqlite3.connect(":memory:")
        self.db.execute('''CREATE TABLE card (card_id INTEGER PRIMARY KEY,
            question TEXT NOT NULL UNIQUE, answer TEXT NOT NULL,
            box INTEGER NOT NULL DEFAULT 1 CHECK (box BETWEEN 1 AND 5), due TEXT NOT NULL)''')

    def add(self, question, answer, today):
        question, answer = question.strip(), answer.strip()
        if not question or not answer:
            raise DeckError("a card needs a question and an answer")
        try:
            self.db.execute("INSERT INTO card (question, answer, due) VALUES (?, ?, ?)",
                            (question, answer, today.isoformat()))
        except sqlite3.IntegrityError:
            raise DeckError("that question is already in the deck")
        self.db.commit()

    def due(self, today):
        return self.db.execute("SELECT card_id, question, box FROM card WHERE due <= ? ORDER BY box, card_id",
                               (today.isoformat(),)).fetchall()

    def record(self, card_id, correct, today):
        (box,) = self.db.execute("SELECT box FROM card WHERE card_id = ?", (card_id,)).fetchone()
        box = min(box + 1, MAX_BOX) if correct else 1
        due = today + timedelta(days=BOX_INTERVALS[box])
        self.db.execute("UPDATE card SET box = ?, due = ? WHERE card_id = ?", (box, due.isoformat(), card_id))
        self.db.commit()
        return box, due

TODAY = date(2025, 3, 1)

class TestDeck(unittest.TestCase):
    def setUp(self):
        self.deck = Deck()
        self.deck.add("What is RAM?", "Memory", TODAY)

    def test_t2_blank_question_refused(self):
        with self.assertRaises(DeckError):
            self.deck.add("   ", "anything", TODAY)

    def test_t3_duplicate_refused(self):
        with self.assertRaises(DeckError):
            self.deck.add("What is RAM?", "Random access memory", TODAY)

    def test_t4_correct_in_box_1_moves_to_box_2(self):
        self.assertEqual(self.deck.record(1, True, TODAY), (2, TODAY + timedelta(days=2)))

    def test_t5_correct_in_box_5_stays_in_box_5(self):
        for _ in range(4):
            self.deck.record(1, True, TODAY)
        self.assertEqual(self.deck.record(1, True, TODAY), (5, TODAY + timedelta(days=16)))
        self.assertEqual(self.deck.record(1, True, TODAY)[0], 5)

    def test_t6_wrong_answer_returns_to_box_1(self):
        for _ in range(3):
            self.deck.record(1, True, TODAY)
        self.assertEqual(self.deck.record(1, False, TODAY), (1, TODAY + timedelta(days=1)))

    def test_t7_only_due_cards_offered(self):
        self.deck.add("What is ROM?", "Read only memory", TODAY)
        self.deck.record(2, True, TODAY)
        self.assertEqual([q for _, q, _ in self.deck.due(TODAY)], ["What is RAM?"])

suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestDeck)
result = unittest.TestResult()
suite.run(result)
print(result.testsRun, "tests,", len(result.failures), "failed,", len(result.errors), "errors")
for test, trace in result.failures + result.errors:
    print("  FAILED", test.id().split(".")[-1])
```

The test names carry the numbers from the test plan, so the evidence can be matched to the plan. Test T5 is the **boundary**: the top box, where a careless `box + 1` would reach 6 and fail the database's `CHECK`.

### The test table

In the write up, results are shown as a table, with a screenshot beside it for each test. A test that **failed first time**, and the fix, is worth more than a table in which everything passed first time.

| Test | Expected | Actual | Result | Action |
| T4 | Box 2, due in 2 days | Box 2, due in 2 days | Pass | None |
| T5 | Stays in box 5 | Raised an error, box 6 | **Fail** | Used `min(box + 1, MAX_BOX)` |
| T5, again | Stays in box 5 | Stays in box 5 | Pass | None, and all tests re run for regression |

### Evaluating the solution

The evaluation is **not a review of how you felt**. It judges the solution against the success criteria, one by one, and **backs each judgement with evidence**.

| Criterion | Met? | Evidence |
| S1: add, refuse blank and duplicate | **Met** | Tests T1 to T3 all pass. In the feedback session, one user typed a question with trailing spaces and it was still caught as a duplicate |
| S2: correct answers move up, to a maximum of 5 | **Met** | T4 and T5, after the fix |
| S5: cards survive closing the program | **Not met** | The prototype uses an in memory database. Changing the path to a file is the next step |
| S6: summary | **Partly met** | It shows the count in each box, but the users wanted it shown as a bar chart |

After the table, the evaluation covers:

- **Stakeholder feedback**: what the users said, in their words, and what you would change because of it
- **Limitations**: there is no way to edit a card, and no import from a spreadsheet
- **Maintenance and future development**: how the structure would let another programmer add an interface or a new rule for the boxes
- **Your own process**: what you would do differently with the time again

!key Evidence in, judgement out :: Every claim in an evaluation should have a test result, a screenshot or a quotation behind it. "Users liked it" is an opinion. "Four of five users completed a review without help, and the fifth asked how to add a card" is evidence.
"""),
    ],
    keyterms=[
        ("Stakeholder", "A person or group with an interest in a system, such as a user, the client or the people who maintain it."),
        ("Success criteria", "Measurable statements of what the finished solution must do, used to judge it in the evaluation."),
        ("Decomposition", "Breaking a problem down into smaller parts that can be designed, built and tested separately."),
        ("Iterative development", "Building a solution in repeated stages, with testing and review, each building on the one before."),
        ("Modular", "Built from separate parts, each with one job, which can be developed and tested independently."),
        ("Test plan", "A table of tests, with their data and the expected results, written before the solution is tested."),
        ("Remedial action", "The change made to the solution to fix a fault that testing has revealed."),
        ("Maintainability", "How easily a solution can be understood, corrected and extended by somebody else."),
        ("Version control", "A system that records the history of changes to code, so that earlier versions can be recovered."),
        ("Evaluation", "A reasoned judgement of the finished solution against its success criteria, supported by evidence."),
    ],
    grade="""
The project is marked on evidence, so work towards documents that prove each claim.

+ Write every success criterion so that someone else could test it and agree if it was met
+ Finish the design, including the test plan, before writing the code it describes
+ Keep a dated log of what went wrong as well as what worked, with annotated screenshots
+ Show the faults that testing found, and the changes that fixed them
+ Judge every success criterion in the evaluation, with evidence, including the ones not met
""",
    mistakes=[
        "Writing success criteria that cannot be measured, such as the program should be easy to use.",
        "Producing the design and the test plan after the code has been written.",
        "Showing only tests that pass first time, which suggests that nothing was found or tested.",
        "Evaluating how the project felt, without judging the solution against each success criterion.",
        "Using code from elsewhere without identifying where it came from.",
    ],
    quiz=[
        Q("What makes a success criterion good?",
          ["It is measurable, so another person could test it and agree whether it was met",
           "It is written in general terms, so that it is hard to argue that it was not met",
           "It describes how the solution will be coded, in as much detail as possible",
           "It is chosen once the program has been finished, so that it can be met"], 0,
          "The evaluation will judge the solution against each criterion, so each one must be checkable."),
        Q("Who are the stakeholders of a project?",
          ["The people who use it, or have an interest in it, such as the client and the users",
           "Only the programmer who writes the code", "Only the teacher who marks the project",
           "Only the people who find out about it after it has been released"], 0,
          "Stakeholders are consulted in the analysis, to find out what the solution must do."),
        Q("What is decomposition?",
          ["Breaking a problem into smaller parts that can be solved and tested separately",
           "Removing the parts of a program that are never used",
           "Writing the program from the end to the beginning",
           "Testing the program by running it on the slowest computer"], 0,
          "A decomposed problem gives a modular program in which each part has a single job."),
        Q("When should the test plan be written?",
          ["During the design, before the solution is built", "After all of the code has been written",
           "Only after the user has reported a fault", "At the same time as the final evaluation"], 0,
          "Expected results worked out before the code exists are real tests. Written afterwards, they only copy the output."),
        Q("What is iterative development?",
          ["Building a solution in stages, testing and reviewing each stage before the next",
           "Writing all of the code first and testing it once at the end",
           "Writing the same code several times in different languages",
           "Asking a different programmer to write each stage of the solution"], 0,
          "Each cycle builds on a part that is known to work, and the log of cycles is the evidence."),
        Q("Why is a test that failed and was then fixed valuable evidence?",
          ["It shows that testing found a fault, and that the fault was corrected", "It shows that the solution is poorly written",
           "It proves that the test plan was written after the code", "It shows that the stakeholders were not consulted"], 0,
          "Testing that never finds a fault suggests the tests were not hard enough."),
        Q("How should an evaluation judge the finished solution?",
          ["Against each success criterion, using evidence such as test results and user feedback",
           "By stating that the solution works and the programmer is pleased with it",
           "By comparing it with another student's project",
           "By counting the number of lines of code that were written"], 0,
          "Evidence in, judgement out: every claim needs a test result, a screenshot or a quotation."),
        Q("Which of these is evidence of good maintainability?",
          ["Meaningful names, comments, constants and a modular structure", "A single long program with no comments",
           "Variable names that are as short as possible", "Placing all of the data in global variables"], 0,
          "Another programmer can then understand, change and extend the code."),
        Q("What is the purpose of version control in a project?",
          ["To record a history of changes, so that earlier versions can be recovered",
           "To make the program run faster on older computers", "To check that the program has no syntax errors",
           "To make sure that the program is the only copy that exists"], 0,
          "If a change breaks something, version control lets you go back to the last version that worked."),
        Q("What should a student do if they use a piece of code from a website in their project?",
          ["Clearly identify it, and say where it came from", "Change the variable names so that it looks different",
           "Leave it out of the documentation, as it is only a small part", "Delete any comments that it came with"], 0,
          "The marks are for your own work, and anything that is not must be openly acknowledged."),
    ],
    exam=[
        EQ("Explain why success criteria should be measurable, and write one measurable success criterion for a program that stores a student's revision flashcards.", 4, [
            MP("The finished solution is judged against the success criteria in the evaluation", ["evaluation", "judged", "evaluate", "assess", "compared"]),
            MP("A measurable criterion can be tested, so there is evidence of whether it was met", ["tested", "evidence", "checked", "proved", "measure"]),
            MP("A vague criterion, such as easy to use, cannot be tested and so cannot be judged", ["vague", "easy to use", "cannot be tested", "opinion", "subjective"]),
            MP("A suitable example, such as a card answered correctly moves up one box and is due again after the interval for that box", ["moves up", "due", "box", "example", "refused", "within", "seconds", "must"]),
        ], "Success criteria are what the finished solution is judged against in the evaluation. A measurable criterion can be tested, so there is evidence of whether or not it was met, whereas a vague criterion, such as the program being easy to use, is an opinion that cannot be tested. A measurable criterion for the flashcard program is that a card answered correctly moves up one box and is next due after the number of days set for that box.",
           command="Explain"),
        EQ("Describe two things that should be included in the design of a programming project before any code is written.", 4, [
            MP("A decomposition of the problem into smaller parts, such as a structure diagram", ["decomposition", "structure diagram", "modules", "parts", "break down"]),
            MP("This shows how the program will be organised, so that each part can be built and tested separately", ["organised", "separately", "each part", "built", "structure"]),
            MP("A test plan, listing the test data and the expected results", ["test plan", "test data", "expected result", "tests"]),
            MP("Written before coding so that the expected results are worked out from the design and not from the program's output", ["before", "not from the output", "worked out", "design", "specification"]),
            MP("Other acceptable items, such as algorithms in pseudocode, data design or interface designs", ["algorithm", "pseudocode", "flowchart", "database", "data structure", "interface", "screen", "layout"]),
        ], "The design should include a decomposition of the problem into smaller parts, for example a structure diagram, which shows how the program will be organised so that each part can be built and tested on its own. It should also include a test plan, listing the test data and the expected results, which are worked out from the design before the code is written, so that the tests are not just a copy of whatever the program happens to output. Algorithms in pseudocode, data design and interface designs would also be suitable.",
           command="Describe"),
        EQ("Explain what is meant by iterative development, and why it is a suitable way of building a project.", 4, [
            MP("The solution is built in stages, and each stage is tested before the next is started", ["stages", "tested", "each stage", "step", "cycle", "small parts"]),
            MP("Each stage builds on a part that is already known to work", ["builds on", "known to work", "working", "previous"]),
            MP("Faults are found while only a small amount of new code could be responsible", ["small amount", "found early", "a few lines", "easier to find", "early"]),
            MP("Feedback from the stakeholders can be used to change what is built next, and the stages give evidence of the development", ["feedback", "stakeholder", "evidence", "log", "diary", "change"]),
        ], "Iterative development means that the solution is built in stages, with each stage tested, and reviewed before the next is started, so that each stage builds on a part that is already known to work. It is suitable for a project because faults are found early, when only a small amount of new code could be the cause, and feedback from the stakeholders can be used to change what is built next. The record of the stages is also the evidence of development.",
           command="Explain"),
        EQ("A student's evaluation says that the project was successful and the users liked it. Explain why this would earn few marks, and describe what the evaluation should contain instead.", 4, [
            MP("It makes a claim with no evidence to support it", ["no evidence", "not supported", "opinion", "claim", "unsupported"]),
            MP("It does not judge the solution against the success criteria", ["success criteria", "each criterion", "criteria", "judge"]),
            MP("It should say whether each success criterion was met, with evidence such as test results or user feedback", ["met", "evidence", "test results", "feedback", "screenshots"]),
            MP("It should also describe limitations and possible improvements", ["limitation", "improvement", "future", "next", "extend", "maintain"]),
        ], "The statement makes a claim without any evidence to support it, and it does not judge the solution against the success criteria. A good evaluation goes through each success criterion in turn and says whether it was met, with evidence such as the results of the tests, screenshots or quotations from the stakeholders. It should also describe the limitations of the solution, and the improvements that could be made to it.",
           command="Explain"),
        EQ("Describe how the use of version control and regular backups helps a student who is developing a programming project.", 3, [
            MP("Version control records a history of the changes made to the code", ["history", "changes", "record", "versions", "log"]),
            MP("An earlier working version can be recovered if a change breaks the program", ["recover", "restore", "go back", "earlier version", "previous version", "revert", "roll back"]),
            MP("Backups mean that the work is not lost if a file or device fails", ["backup", "lost", "failure", "fails", "second copy", "stored in two places"]),
        ], "Version control keeps a history of the changes made to the code, so that if a change breaks the program an earlier working version can be recovered. Regular backups, stored in more than one place, mean that the work is not lost if a file is deleted or a device fails.",
           command="Describe"),
    ],
)
