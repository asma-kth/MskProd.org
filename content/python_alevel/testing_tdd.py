"""A Level Python: testing strategies, unittest, test driven development and exceptions."""
from mskbuild.models import Topic, Section, Q, EQ, MP

INPUTS = {}
EXPECT = {}

TOPIC = Topic(
    slug="testing-and-tdd",
    title="Testing, Unit Tests and Test-Driven Development",
    spec="A Level 12",
    icon="i-check-circle",
    minutes=55,
    blurb="The levels and kinds of testing the specification names, then unit tests written and run with unittest, the red, green, refactor cycle of test driven development worked through on a real function, and exceptions that fail loudly instead of quietly.",
    fact="Software testing is expensive for a reason. In 1996 the first launch of the Ariane 5 rocket was destroyed 37 seconds after lift off by a conversion of a 64 bit number to a 16 bit integer that had been safe in the older Ariane 4 and was never tested against the new rocket's flight path.",
    sections=[
        Section("Levels and kinds of testing", r"""
Testing is not one activity. The specification names several, and the exam asks you to say which one a scenario describes, and why.

### The levels of testing

| Level | What is tested | By whom | Typical question |
| **Unit** | One subprogram or class, on its own | The programmer | Does `calculate_tax` return the right figure? |
| **Integration** | Several units **working together** | The programmer, or a tester | Does the basket pass the right total to the payment module? |
| **System** | The **whole** program, against the requirements | A tester | Does the finished shop do everything the specification said? |
| **Acceptance** | The finished system, by the **client**, in their own setting | The customer | Is this what we asked for, and will we accept it? |

Two named stages of testing a finished product with real users:

- **Alpha testing** is carried out **inside** the development organisation, by staff who are not the programmers. It finds the problems before outsiders see them.
- **Beta testing** is carried out by a **selected group of real users**, in their own environment, before the general release. It finds the problems that the developers' own machines and habits could not.

### Black box and white box

| | Black box testing | White box testing |
| The tester knows | Only the **specification**: what goes in and what should come out | The **code**: its branches, loops and paths |
| Test data chosen from | The requirements | The structure, so that every path is taken |
| Finds | Missing or wrong behaviour | Faulty logic, and code that was never run |
| Example | Enter 49 and check that "Fail" is shown | Make sure a test reaches the `elif` for a pass mark |

A white box test aims for **coverage**: every statement, every branch, and every path executed by at least one test. 100 per cent coverage proves the code was **run**. It does not prove that it is **right**.

### Other words the exam uses

| Term | Means |
| **Regression testing** | Re running the earlier tests after a change, to check that the change has not **broken** something that used to work |
| **Static testing** | Examining code **without running it**: reading it, a walkthrough, a trace table, or a tool that checks it |
| **Dynamic testing** | Running the code with test data and checking the results |
| **Normal, boundary, erroneous data** | The three kinds of test data, as at GCSE, now applied to every unit |

!exam Match the test to the scenario :: Questions describe a situation and ask for the type of testing. A group of the company's own staff trying the software is alpha. Chosen customers trying it at home is beta. The client signing it off against what they ordered is acceptance. Re running old tests after a bug fix is regression.
"""),
        Section("Unit tests with unittest", r"""
A **unit test** is a small program that calls one piece of your code with chosen inputs and checks the result **automatically**. Python's `unittest` module provides the framework. A test case is a class that inherits from `unittest.TestCase`, and each method whose name starts with `test` is one test.

```python
import unittest

def grade_for(mark):
    if mark < 0 or mark > 100:
        raise ValueError("mark must be between 0 and 100")
    if mark >= 70:
        return "Distinction"
    if mark >= 50:
        return "Merit"
    if mark >= 40:
        return "Pass"
    return "Fail"

class TestGradeFor(unittest.TestCase):
    def test_normal(self):
        self.assertEqual(grade_for(85), "Distinction")
        self.assertEqual(grade_for(55), "Merit")

    def test_boundaries(self):
        self.assertEqual(grade_for(70), "Distinction")
        self.assertEqual(grade_for(69), "Merit")
        self.assertEqual(grade_for(49), "Pass")
        self.assertEqual(grade_for(39), "Fail")
        self.assertEqual(grade_for(0), "Fail")
        self.assertEqual(grade_for(100), "Distinction")

    def test_invalid(self):
        with self.assertRaises(ValueError):
            grade_for(101)
        with self.assertRaises(ValueError):
            grade_for(-1)

def run(case):
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(case)
    result = unittest.TestResult()
    suite.run(result)
    print(result.testsRun, "tests,", len(result.failures), "failed,", len(result.errors), "errors")
    for test, trace in result.failures:
        print("  FAILED", test.id().split(".")[-1], "-", [line for line in trace.split("\n") if line.startswith("AssertionError")][0])

run(TestGradeFor)
```

Run it: three tests, none failed. The `run` function is only there to give a short, readable summary. In a normal program you would end the file with `unittest.main()` and let the framework print its own report.

### A test that finds a bug

Change one character in the function, the classic boundary mistake of `>=` written as `>`, and run the same tests again.

```python
import unittest

def grade_for(mark):
    if mark >= 70:
        return "Distinction"
    if mark > 50:
        return "Merit"
    return "Pass"

class TestGradeFor(unittest.TestCase):
    def test_normal(self):
        self.assertEqual(grade_for(85), "Distinction")
        self.assertEqual(grade_for(55), "Merit")

    def test_boundaries(self):
        self.assertEqual(grade_for(70), "Distinction")
        self.assertEqual(grade_for(50), "Merit")

def run(case):
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(case)
    result = unittest.TestResult()
    suite.run(result)
    print(result.testsRun, "tests,", len(result.failures), "failed")
    for test, trace in result.failures:
        print("  FAILED", test.id().split(".")[-1], "-", [line for line in trace.split("\n") if line.startswith("AssertionError")][0])

run(TestGradeFor)
```

The normal test passes. The **boundary** test fails, and the report says exactly which assertion and what it received: `'Pass' != 'Merit'`. A mark of 50 earned a Pass instead of a Merit. It is the boundary test that catches it, every time.

### The assertions

| Method | Passes when |
| `assertEqual(a, b)` | `a == b` |
| `assertTrue(x)`, `assertFalse(x)` | `x` is true, or false |
| `assertAlmostEqual(a, b)` | `a` and `b` are equal to 7 decimal places, for floats |
| `assertIn(a, b)` | `a` is in `b` |
| `assertIsNone(x)` | `x` is `None` |
| `assertRaises(Error)` | the code inside the `with` block raises that error |

### A fresh start for every test

Tests must be **independent**: one must not depend on the leftovers of another, or the order they run in changes the result. `setUp` runs before each test and builds a fresh object.

```python
import unittest

class Stack:
    def __init__(self):
        self.items = []
    def push(self, item):
        self.items.append(item)
    def pop(self):
        if not self.items:
            raise IndexError("stack is empty")
        return self.items.pop()

class TestStack(unittest.TestCase):
    def setUp(self):
        self.stack = Stack()

    def test_last_in_first_out(self):
        self.stack.push(1)
        self.stack.push(2)
        self.assertEqual(self.stack.pop(), 2)
        self.assertEqual(self.stack.pop(), 1)

    def test_pop_from_empty_raises(self):
        with self.assertRaises(IndexError):
            self.stack.pop()

    def test_a_new_stack_is_empty(self):
        self.assertEqual(self.stack.items, [])

suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestStack)
result = unittest.TestResult()
suite.run(result)
print(result.testsRun, "tests,", len(result.failures) + len(result.errors), "problems")
```

!key A test is a specification you can run :: Reading the test names above tells you what a `Stack` must do. That is the point of writing tests with the **expected** result decided first. If the test and the code disagree, the specification says which one is wrong.
"""),
        Section("Test-driven development", r"""
**Test-driven development** (TDD) turns the order of work round. You write the **test first**, watch it **fail**, and only then write the code. It is a short cycle repeated many times:

1. **Red.** Write one small test for a behaviour that does not exist yet. Run it. It **fails**, which proves that the test can fail.
2. **Green.** Write the **simplest** code that makes the test pass. No more.
3. **Refactor.** Tidy the code, with every test still passing, so that the tests protect the clean up.

### A worked cycle: leap years

The rule: a year is a leap year if it divides by 4, **except** centuries, which must also divide by 400. So 2024 is, 1900 is not, 2000 is.

**Red.** The function does not do anything yet, so the very first test fails.

```python
import unittest

def is_leap_year(year):
    return False

class TestLeapYear(unittest.TestCase):
    def test_ordinary_leap_year(self):
        self.assertTrue(is_leap_year(2024))

suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestLeapYear)
result = unittest.TestResult()
suite.run(result)
print(result.testsRun, "tests,", len(result.failures), "failed")
for test, trace in result.failures:
    print("  FAILED", test.id().split(".")[-1], "-", [line for line in trace.split("\n") if line.startswith("AssertionError")][0])
```

**Green.** The simplest code that passes is to divide by 4. Add the next tests, which fail for 1900 and then pass for 2000, and each makes the function a little more right.

```python
import unittest

def is_leap_year(year):
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

class TestLeapYear(unittest.TestCase):
    def test_ordinary_leap_year(self):
        self.assertTrue(is_leap_year(2024))

    def test_ordinary_year(self):
        self.assertFalse(is_leap_year(2023))

    def test_century_is_not_a_leap_year(self):
        self.assertFalse(is_leap_year(1900))

    def test_every_fourth_century_is(self):
        self.assertTrue(is_leap_year(2000))

suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestLeapYear)
result = unittest.TestResult()
suite.run(result)
print(result.testsRun, "tests,", len(result.failures), "failed")
```

**Refactor.** With four tests watching, the condition could be rewritten as clearer code, and the tests would say at once if the rewrite broke it.

### Why do it this way round

| Benefit | Because |
| Every feature has a test | There is no code that was written without one |
| Tests are written against the specification | Not against what the code happens to do |
| Small steps | A failure is always in the few lines just written |
| Fearless change | The tests tell you at once if a clean up breaks anything, which is regression testing built in |
| Better design | Code that is easy to test is made of small, independent units |

The cost is time at the start, and the discipline to write a test when it is not wanted. TDD does not remove the need for the other levels of testing: unit tests do not show that the units fit together.

### Exceptions, and failing loudly

A function that cannot do its job should say so, not return something plausible. **Raise an exception** with a message that explains what was wrong, and let the caller decide what to do. A custom exception gives the problem a name.

```python
class InsufficientFunds(Exception):
    pass

class Account:
    def __init__(self, balance):
        self.balance = balance

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("amount must be positive")
        if amount > self.balance:
            raise InsufficientFunds("balance is " + str(self.balance) + ", asked for " + str(amount))
        self.balance -= amount
        return self.balance

account = Account(100)
print(account.withdraw(30))

for amount in [500, -5, 20]:
    try:
        print("left:", account.withdraw(amount))
    except InsufficientFunds as error:
        print("refused:", error)
    except ValueError as error:
        print("invalid:", error)
    finally:
        print("   checked", amount)
```

| Part | Does |
| `raise` | Stops the function and hands an exception to the caller |
| `try` | The code that may raise one |
| `except Name as error` | Runs only if that kind of exception was raised |
| `finally` | Runs **whatever happened**, which is where tidying up goes |

Catching the **specific** exception matters. A bare `except:` hides every bug, including ones you did not know about, and is a common reason for a program that fails silently.
"""),
    ],
    keyterms=[
        ("Unit testing", "Testing a single subprogram or class in isolation, with chosen inputs and expected outputs."),
        ("Integration testing", "Testing that several units work correctly together."),
        ("System testing", "Testing the whole program against its requirements."),
        ("Acceptance testing", "Testing by the client, to decide whether the finished system meets what they asked for."),
        ("Alpha testing", "Testing of software by people within the development organisation, before release to outsiders."),
        ("Beta testing", "Testing of software by a selected group of real users, in their own environment, before general release."),
        ("Black box testing", "Testing based only on the specification, without knowledge of the code."),
        ("White box testing", "Testing designed using knowledge of the code, so that every path is exercised."),
        ("Regression testing", "Repeating earlier tests after a change, to check that nothing has been broken."),
        ("Test-driven development", "A way of working in which a failing test is written first, then the code to pass it, then the code is tidied."),
        ("Exception", "An event that stops the normal flow of a program, raised when something cannot be done and handled elsewhere."),
    ],
    grade="""
Testing answers are marked on matching the term to the situation, and on tests that would really find a fault.

+ Name the level of testing from the scenario: unit, integration, system, acceptance, alpha or beta
+ Say what the tester knows in black box and in white box testing, and what each can and cannot find
+ In a test plan, include normal, boundary and erroneous data, and write the expected result first
+ Describe test driven development as red, green, refactor, with the test written before the code
+ Say that regression testing is repeating earlier tests after a change, and why that is needed
""",
    mistakes=[
        "Mixing up alpha testing, done by staff inside the company, and beta testing, done by outside users.",
        "Saying white box testing is done by the customer, or that black box testing needs the source code.",
        "Writing the expected result after seeing the output, which tests nothing.",
        "Testing only normal data, and never the boundary where a comparison is easily written wrongly.",
        "Describing test driven development as writing the tests at the end of the project.",
    ],
    quiz=[
        Q("Which level of testing checks one subprogram on its own?",
          ["Unit testing", "Integration testing", "System testing", "Acceptance testing"], 0,
          "A unit is the smallest testable part, and a unit test calls it with chosen inputs and checks the result."),
        Q("Which testing is carried out by the customer to decide whether to accept the finished system?",
          ["Acceptance testing", "Unit testing", "White box testing", "Regression testing"], 0,
          "The customer checks the system against what they ordered, usually in their own environment."),
        Q("What is the difference between alpha and beta testing?",
          ["Alpha is done within the development organisation, beta is done by selected real users",
           "Alpha is done by real users, beta is done within the development organisation",
           "Alpha tests the hardware and beta tests the software",
           "Alpha is done before any code is written and beta after it is complete"], 0,
          "Alpha comes first and finds the problems before outsiders see the software. Beta is the first test by real users."),
        Q("What does a black box tester know?",
          ["The specification, but not the code", "The code, but not the specification", "Both the code and the specification",
           "Neither the code nor the specification"], 0,
          "Black box tests are chosen from the requirements alone, so they test what the software does, not how."),
        Q("What is the aim of white box testing?",
          ["To make sure that every path through the code is exercised", "To check the program without looking at any of its code",
           "To check that the customer is satisfied with the program", "To measure how fast the program runs"], 0,
          "The tester can see the code, so tests are chosen to take every branch and loop."),
        Q("What is regression testing?",
          ["Repeating earlier tests after a change to check that nothing has been broken", "Testing the oldest part of a program first",
           "Testing a program on an older version of the operating system", "Testing a program only once it has been released"], 0,
          "Fixing one fault can create another, and the old tests are how that is caught."),
        Q("In test driven development, what is written first?",
          ["A test that fails", "The code that is to be tested", "The user documentation", "A flowchart of the whole program"], 0,
          "The red stage proves that the test can fail, and then code is written to make it pass."),
        Q("What are the three stages of the test driven development cycle, in order?",
          ["Red, green, refactor", "Green, red, refactor", "Refactor, red, green", "Plan, build, release"], 0,
          "Red is a failing test, green is the simplest code to pass it, and refactor is tidying with the tests still passing."),
        Q("Which `unittest` method checks that a piece of code raises a particular error?",
          ["assertRaises", "assertEqual", "assertIn", "assertAlmostEqual"], 0,
          "It is used with a with block, and the test passes only if the code inside raises the named exception."),
        Q("Why is a bare `except:` that catches every error a bad idea?",
          ["It hides bugs that the programmer did not know about, so the program fails silently",
           "It makes the program run too slowly for the results to be of any use",
           "It is only allowed to appear once in each program that is written",
           "It stops the finally block from running when an error is raised"], 0,
          "Catching only the exceptions you expect lets the unexpected ones come to the surface where they can be fixed."),
    ],
    exam=[
        EQ("Describe the difference between black box testing and white box testing.", 4, [
            MP("In black box testing the tester does not know, or does not use, the code", ["does not know", "no knowledge", "without", "cannot see", "not use the code"]),
            MP("Tests are chosen from the specification, checking that the right output is given for an input", ["specification", "requirements", "input and output", "expected output"]),
            MP("In white box testing the tester knows the code", ["knows the code", "can see the code", "knowledge of the code", "uses the code", "structure"]),
            MP("Tests are chosen so that every path, branch or statement in the code is executed", ["every path", "every branch", "every statement", "all paths", "coverage", "all branches"]),
        ], "In black box testing the tester has no knowledge of the code and chooses tests from the specification, checking that each input gives the output that the requirements say it should. In white box testing the tester can see the code, and chooses tests so that every path, branch or statement in it is executed at least once.",
           command="Describe"),
        EQ("A company develops a new mobile app. State, with a reason, whether each of the following is an example of alpha testing, beta testing or acceptance testing. (a) Employees of the company who did not write the app use it for a week and report faults. (b) A group of 500 members of the public are given the app before its public release and report faults. (c) The client who ordered the app uses it in their own business and then signs to confirm that it does what they asked.", 3, [
            MP("(a) Alpha testing, because it is carried out within the organisation, by staff", ["alpha", "within", "employees", "inside", "staff"]),
            MP("(b) Beta testing, because it is carried out by real users before release", ["beta", "members of the public", "real users", "before release", "selected"]),
            MP("(c) Acceptance testing, because the client confirms that it meets the requirements they ordered", ["acceptance", "client", "customer", "requirements", "signs"]),
        ], "(a) is alpha testing, because it is carried out by staff inside the company, who are not the programmers, before anyone outside sees the app. (b) is beta testing, because a group of real users outside the company try the app in their own environment before the general release. (c) is acceptance testing, because the client checks that the app does what they asked for, and accepts it.",
           command="State"),
        EQ("A function is_palindrome(text) returns True if the text reads the same forwards and backwards, ignoring case, and False otherwise. Write a unittest test case class with at least three tests that use normal, boundary and erroneous data. Include the function as well.", 5, [
            MP("Imports unittest, and a class that inherits from unittest.TestCase", ["import unittest", "unittest.testcase", "testcase"]),
            MP("Test methods whose names start with test", ["def test", "test_"]),
            MP("A normal data test, such as racecar or Level, with assertTrue or assertFalse", ["racecar", "level", "asserttrue", "assertfalse", "normal"]),
            MP("A boundary test, such as an empty string or one character", ["empty", "empty string", "one character", "single character", "boundary", "'a'"]),
            MP("A test for erroneous or unusual data, using assertRaises or a check of the expected result", ["assertraises", "erroneous", "number", "none", "123", "expected"]),
        ], r"""```python
import unittest

def is_palindrome(text):
    cleaned = text.lower()
    return cleaned == cleaned[::-1]

class TestIsPalindrome(unittest.TestCase):
    def test_normal(self):
        self.assertTrue(is_palindrome("racecar"))
        self.assertTrue(is_palindrome("Level"))
        self.assertFalse(is_palindrome("python"))

    def test_boundary(self):
        self.assertTrue(is_palindrome(""))
        self.assertTrue(is_palindrome("a"))
        self.assertFalse(is_palindrome("ab"))

    def test_erroneous(self):
        with self.assertRaises(AttributeError):
            is_palindrome(12321)

suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestIsPalindrome)
result = unittest.TestResult()
suite.run(result)
print(result.testsRun, "tests,", len(result.failures) + len(result.errors), "problems")
```

The normal test uses words that are and are not palindromes, including a capital letter. The boundary test uses an empty string, one character and the shortest string that is not a palindrome. The erroneous test passes a number, which has no lower method, and checks that the function fails with an error rather than giving an answer. The three tests all pass.""",
           command="Write"),
        EQ("Explain how test driven development works, and give one advantage of working in this way.", 4, [
            MP("A test is written first, for a feature that does not yet exist", ["test first", "test is written first", "written first", "before the code", "before writing"]),
            MP("The test is run and fails, which shows that it can detect the absence of the feature", ["fails", "red", "failing", "shows it can fail"]),
            MP("The simplest code needed to make the test pass is then written, and the code is tidied up afterwards", ["simplest", "minimum", "just enough", "pass", "refactor", "tidied", "green"]),
            MP("An advantage, such as all of the code being covered by tests, or tests protecting later changes", ["covered", "every feature", "protect", "regression", "advantage", "confidence", "changes", "fewer faults"]),
        ], "In test driven development a test for a small piece of behaviour is written first, before the code exists. The test is run and fails, which shows that the test can detect the missing feature. The simplest code that makes the test pass is then written, and once it passes the code is refactored, which means tidied up with the tests still passing. The cycle repeats for the next feature. An advantage is that all of the code is covered by tests, so later changes can be made with confidence, because the tests show straight away if anything has been broken.",
           command="Explain"),
        EQ("A programmer fixes a fault in the calculation of delivery charges in an online shop. Explain why the programmer should carry out regression testing before the shop is updated.", 3, [
            MP("Regression testing repeats the earlier tests on the program after it has been changed", ["repeat", "re-run", "rerun", "run again", "earlier tests", "existing tests", "previous tests"]),
            MP("A change in one part of a program can cause a fault in a part that was working", ["break", "broken", "cause", "new fault", "other parts", "something else", "was working"]),
            MP("It confirms that the delivery charge fix has not affected, for example, the basket total or the payment", ["not affected", "still works", "still work", "confirm", "other features", "basket", "payment"]),
        ], "Regression testing means repeating the earlier tests on the program after it has been changed. A change to one part of a program can cause a fault in another part that was working before, for example the fix to the delivery charge might alter the basket total or the payment. By repeating the tests, the programmer confirms that everything that worked before still works before the update is released.",
           command="Explain"),
    ],
)
