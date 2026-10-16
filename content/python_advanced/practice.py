"""Advanced Python: readable code, modules, version control, performance and packaging."""
from mskbuild.models import Topic, Section, Q, EQ, MP

INPUTS = {}
EXPECT = {}

TOPIC = Topic(
    slug="working-like-a-professional",
    title="Working Like a Professional",
    spec="Advanced 7",
    icon="i-flag",
    minutes=65,
    blurb="The habits that separate a program that works from a program that lasts. Readable code with docstrings and doctests, modules and virtual environments, version control (including a small one built from scratch), measuring performance before changing anything, and shipping a command line tool with documentation.",
    fact="Donald Knuth, who wrote the standard reference on algorithms, warned in 1974 that 'premature optimization is the root of all evil'. Programmers waste far more time making the wrong part of a program fast than they ever save, which is why professionals measure first and optimise second.",
    sections=[
        Section("Readable code: style, naming and docstrings", r"""
Code is read many more times than it is written, usually by someone who has forgotten what it does. That someone is often **you**, six months later. Readable code is not a luxury. It is how a program stays correct as it grows.

Python's style guide is **PEP 8**. These are the rules that matter most:

| Rule | Example |
| `snake_case` for variables and functions | `total_cost`, `read_scores()` |
| `PascalCase` for classes | `ShoppingBasket` |
| `UPPER_CASE` for constants | `VAT_RATE = 0.2` |
| a leading underscore for "internal" | `_cache` |
| 4 spaces per indent, never tabs mixed in | `if ready:` then four spaces |
| lines under about 80 to 100 characters | break a long call over several lines |
| imports at the top, one per line, standard library first | `import os` then `import sys` |
| spaces around operators, none inside brackets | `x = (a + b) * c` |

Here is the same function written badly and well. Read the first and try to say what it does:

```python
def calc(d, r):
    x = 0
    for k in d:
        if d[k][1] == 1:
            x = x + d[k][0] * (1 + r)
        else:
            x = x + d[k][0]
    return x

def basket_total(basket, vat_rate):
    '''Return the cost of a basket of shopping.

    basket maps an item name to a pair of (price, is_taxable).
    VAT is added only to the taxable items.
    '''
    total = 0
    for price, is_taxable in basket.values():
        if is_taxable:
            total += price * (1 + vat_rate)
        else:
            total += price
    return total

shopping = {"bread": (1.5, 0), "pen": (2.0, 1), "toy": (10.0, 1)}
print(round(calc(shopping, 0.2), 2), round(basket_total(shopping, 0.2), 2))
```

The two give the same answer. The second is far easier to trust, because every name says what it holds and the docstring says what the data looks like. The difference is only *names, structure and a docstring*.

### The habits of clear code

- **Name things for what they mean**, not for how they are used: `days_overdue`, not `d`. A long accurate name beats a short vague one.
- **Replace magic numbers** with named constants. `if age >= 18:` becomes `if age >= VOTING_AGE:`.
- **One function, one job**, short enough to see on a screen. If you describe it with "and", split it.
- **Return early** instead of nesting: a check that fails can `return` straight away, keeping the main path unindented.
- **Do not repeat yourself** (DRY). Code that appears twice will one day be fixed in only one place.
- **Comments say why**, not what. `# the API counts from 1` is useful. `# add one to x` is noise.

### Docstrings

A **docstring** is a string in the first line of a function, class or module. It becomes the object's built-in documentation, shown by `help()` and by editors. The first line is a short summary. After it come the arguments and what is returned.

### Doctests: documentation that tests itself

A docstring can hold an example written as an interactive session, starting `>>>`. The `doctest` module runs these examples and checks the answers, so the documentation can never quietly go out of date:

```python
import doctest

def clamp(value, low, high):
    '''Return value, limited to the range from low to high.

    >>> clamp(5, 0, 10)
    5
    >>> clamp(-3, 0, 10)
    0
    >>> clamp(99, 0, 10)
    10
    '''
    return max(low, min(value, high))

finder = doctest.DocTestFinder()
runner = doctest.DocTestRunner(verbose=False)
for test in finder.find(clamp, "clamp", globs=globals()):
    runner.run(test)
print(runner.summarize(verbose=False))
```

`attempted=3, failed=0` means the three examples in the docstring all gave the answers shown. On a real project you run `python -m doctest module.py`, or put the checks in a test suite. A failing example is reported like this:

```text
File "clamp.py", line 5, in clamp
Failed example:
    clamp(5, 0, 10)
Expected:
    6
Got:
    5
```

### Tools that do the checking for you

```text
pip install ruff black
black program.py        reformats the file in the standard style
ruff check program.py   finds unused imports, undefined names, and many bugs
```

!key Style is for people :: The interpreter does not mind `calc(d, r)`. The person who has to fix it at midnight does. A team agrees a style, lets a tool apply it, and spends its energy on the problem instead.
"""),
        Section("Modules, packages and virtual environments", r"""
Any Python file is a **module**. Importing it runs its code once and gives you its names. Several modules in a folder with an `__init__.py` file make a **package**. Breaking a program into modules keeps each file small, lets you reuse code, and gives every name a home.

```text
shop/
    pyproject.toml          how the project is built and what it needs
    README.md               what it is and how to use it
    src/shop/
        __init__.py
        basket.py           the Basket class
        pricing.py          VAT and discounts
        cli.py              the command line
    tests/
        test_pricing.py
    .gitignore
```

### Ways to import

| Statement | Gives you |
| `import math` | the module: use `math.sqrt(2)` |
| `from math import sqrt` | just that name: use `sqrt(2)` |
| `import numpy as np` | the module under a shorter name |
| `from shop.pricing import vat` | a name from inside a package |
| `from math import *` | everything: **avoid it**, as it hides where names came from |

### Running a file or importing it

Every module has a `__name__`. When you run a file directly it is `"__main__"`. When another file imports it, it is the module's own name. That lets one file be both a **library** and a **program**:

```python
import sys
import types

source = '''
PI = 3.14159

def area(radius):
    return PI * radius ** 2

if __name__ == "__main__":
    print("running as a script")
'''

shapes = types.ModuleType("shapes")            # make a module in memory
exec(source, shapes.__dict__)
sys.modules["shapes"] = shapes                  # register it so that import can find it

import shapes as imported
print(imported.area(2), "| name is", imported.__name__)

print("--- the same code, run directly:")
exec(source, {"__name__": "__main__"})
```

When imported, the guard `if __name__ == "__main__":` is false, so the script part does not run. A file you intend to import should never do real work at the top level.

!warn Circular imports :: If `a.py` imports `b.py` and `b.py` imports `a.py`, Python meets one of them half built and fails. The cure is a design one: move what they share into a third module, or import inside the function that needs it.

### Virtual environments and dependencies

Different projects need different versions of the same library. If they all install into the one Python on your computer, they collide. A **virtual environment** is a private copy of Python and its libraries for one project. You create it, activate it, and install into it, and nothing else on your computer is touched.

```text
python -m venv .venv
source .venv/bin/activate         (on Windows: .venv\Scripts\activate)
pip install requests
pip freeze > requirements.txt     records the exact versions in use
pip install -r requirements.txt   rebuilds the same environment elsewhere
```

A modern project describes itself in `pyproject.toml`:

```text
[project]
name = "shop"
version = "1.2.0"
dependencies = ["requests>=2.31"]

[project.scripts]
shop = "shop.cli:main"
```

**Version numbers** follow a convention, **semantic versioning**: in `1.2.0`, the first number changes when something breaks, the second when features are added, the third for fixes. Each library you depend on is also a risk. Keep the list short, and check it for known security problems with a tool such as `pip-audit`.
"""),
        Section("Version control with Git", r"""
**Version control** records every change to a project, who made it and why. You can see what the code was last Tuesday, find the change that broke something, and undo it. It also lets several people work on one project at once without overwriting each other. **Git** is the standard tool.

| Term | Meaning |
| **Repository** | the project folder together with its whole history |
| **Commit** | a saved **snapshot** of every file, with a message and a unique id |
| **Branch** | a separate line of work, so that a new feature does not disturb the working version |
| **Merge** | joining one branch's changes into another |
| **Remote** | a copy of the repository on a server, such as GitHub |
| **Clone / pull / push** | copy a remote, fetch new changes from it, send your changes to it |
| **Pull request** | a request for someone to review a branch before it is merged |
| **Conflict** | two changes to the same lines that Git cannot combine alone, so a person must choose |

The commands for a normal day:

```text
git init                       start a repository here
git status                     what has changed?
git add scoring.py             choose what goes in the next snapshot
git commit -m "Reject scores below zero"
git log --oneline              the history, one line per commit
git diff                       exactly what changed
git switch -c high-scores      start a new branch
git merge high-scores          bring it back
git push                       send commits to the server
```

A good **commit message** says *what* and, when it is not obvious, *why*: `Reject scores below zero`, not `fixed stuff`. Commit small, often, and only things that work. A `.gitignore` file lists what never to commit: virtual environments, compiled files, and above all **passwords and keys**.

For a coursework project the commit history is **evidence**. It shows the project was developed step by step, and when each part was written.

### How it works inside

Git is built on ideas you already know. Each commit stores a **snapshot** of the files, named by a **hash** of their content. A commit also records its **parent**, so the history is a linked list. Two files with identical content have the same hash and are stored once. Here is a tiny version control system in a few lines:

```python
import difflib
import hashlib
import json

class Repo:
    def __init__(self):
        self.snapshots = {}               # hash of the content -> the files
        self.commits = []

    def commit(self, files, message):
        content = json.dumps(files, sort_keys=True)
        tree = hashlib.sha1(content.encode()).hexdigest()[:7]
        self.snapshots[tree] = dict(files)       # the same content is stored only once
        parent = self.commits[-1]["id"] if self.commits else None
        ident = hashlib.sha1((content + str(parent) + message).encode()).hexdigest()[:7]
        self.commits.append({"id": ident, "parent": parent, "message": message, "tree": tree})
        return ident

    def log(self):
        for commit in reversed(self.commits):
            print(commit["id"], "<-", commit["parent"], commit["message"])

    def checkout(self, ident):
        for commit in self.commits:
            if commit["id"] == ident:
                return dict(self.snapshots[commit["tree"]])

    def diff(self, old_id, new_id):
        old, new = self.checkout(old_id), self.checkout(new_id)
        for name in sorted(set(old) | set(new)):
            before = old.get(name, "").splitlines()
            after = new.get(name, "").splitlines()
            for line in difflib.unified_diff(before, after, "a/" + name, "b/" + name, lineterm="", n=0):
                print(line)

repo = Repo()
first = repo.commit({"main.py": "print('hello')\n"}, "first version")
second = repo.commit({"main.py": "print('hello')\nprint('world')\n", "notes.txt": "todo\n"}, "say world, add notes")
third = repo.commit({"main.py": "print('hello, world')\n", "notes.txt": "todo\n"}, "merge the two prints")

repo.log()
print()
repo.diff(first, third)
print()
print("going back to the first commit:", repo.checkout(first))

repo.commit({"main.py": "print('hello, world')\n", "notes.txt": "todo\n"}, "no change")
print(len(repo.snapshots), "snapshots stored for", len(repo.commits), "commits")
```

The last line shows the saving. Four commits, but only three snapshots, because the fourth is identical to the third. A **branch**, in Git, is nothing more than a movable label pointing at one commit, which is why creating one is instant.
"""),
        Section("Measuring and improving performance", r"""
Programmers are famously bad at guessing which part of a program is slow. The rule is **measure, then change**. The steps are:

1. **Make it correct first.** A fast wrong answer is no use.
2. **Measure** with real data, to see whether there is a problem at all.
3. **Find the bottleneck**, the small part where most of the time goes.
4. **Change one thing**, and measure again.
5. Stop when it is fast enough.

### Timing with timeit

`timeit` runs a small piece of code many times to average out the noise. This compares looking for a value in a list and in a set:

```python
# varies
import timeit

in_list = timeit.timeit("99999 in data", setup="data = list(range(100000))", number=200)
in_set = timeit.timeit("99999 in data", setup="data = set(range(100000))", number=200)

print("set lookup was faster:", in_set < in_list)
print("by roughly", round(in_list / in_set), "times")
```

A list has to be searched item by item, O(n). A set finds the item from its hash, O(1). Your computer will give different times, but the comparison will not change.

### Algorithms beat tuning

Counting the **steps** is more reliable than timing, because it does not depend on the computer. Find two numbers in a list that add up to a target. The obvious way tries every pair. A smarter way remembers the numbers it has seen:

```python
numbers = list(range(0, 1200, 2))              # 600 even numbers
target = 1                                     # no two even numbers can add up to 1

def pair_by_brute_force(numbers, target):
    checks = 0
    for i in range(len(numbers)):
        for j in range(i + 1, len(numbers)):
            checks += 1
            if numbers[i] + numbers[j] == target:
                return (numbers[i], numbers[j]), checks
    return None, checks

def pair_with_a_set(numbers, target):
    seen = set()
    checks = 0
    for number in numbers:
        checks += 1
        if target - number in seen:
            return (target - number, number), checks
        seen.add(number)
    return None, checks

print("brute force :", pair_by_brute_force(numbers, target))
print("with a set  :", pair_with_a_set(numbers, target))
```

Nearly 180 thousand checks against 600. That is the difference between O(n squared) and O(n), and it grows: with 6000 numbers it would be 18 million checks against 6000. No amount of clever micro tuning will find a gap that size.

### Profiling: find the bottleneck

A **profiler** records how long each function takes and how often it was called, so you can see where the time goes instead of guessing:

```python
# varies
import cProfile
import pstats

def parse(line):
    return [int(part) for part in line.split(",")]

def total(lines):
    return sum(sum(parse(line)) for line in lines)

lines = ["1,2,3,4,5,6,7,8"] * 20000

profiler = cProfile.Profile()
profiler.runcall(total, lines)
pstats.Stats(profiler).sort_stats("cumulative").print_stats(5)
```

In the table, `ncalls` is how many times a function ran, `tottime` is the time spent in the function itself, and `cumtime` includes everything it called. Look for the functions with a large `cumtime`. On your own computer, `python -m cProfile -s cumulative program.py` profiles a whole program.

### Quick wins worth knowing

| Slow | Faster |
| searching a list with `in` | a `set` or a `dict` |
| `list.pop(0)` in a loop | a `deque` |
| building a string with `+=` in a long loop | collect the pieces and `"".join(pieces)` |
| working out the same thing again and again | `functools.lru_cache`, or store it |
| a loop that appends to a list | a list comprehension |
| reading a whole huge file | iterate over it line by line |

!warn Premature optimisation :: Do not make code harder to read for a speed gain you have not measured. Code that is 5% faster and half as clear is a bad trade nearly every time. Choose the right algorithm and data structure first. Everything else only after a profiler has pointed at it.
"""),
        Section("Command line tools, packaging and documentation", r"""
A program that runs from the command line can be scheduled, chained with others and used by people who never see the code. The shape of a well made one is always the same:

```python
import argparse
import sys
from collections import Counter

def count_words(text, top, lower):
    '''Return the most common words in text.'''
    words = text.lower().split() if lower else text.split()
    return Counter(words).most_common(top)

def main(argv=None):
    parser = argparse.ArgumentParser(prog="counter", description="Count the words in some text")
    parser.add_argument("text", help="the text to count")
    parser.add_argument("-n", "--top", type=int, default=3, help="how many words to show")
    parser.add_argument("--lower", action="store_true", help="ignore the case of the words")
    args = parser.parse_args(argv)

    if args.top < 1:
        print("counter: --top must be at least 1", file=sys.stderr)
        return 2                                  # a non zero exit code means failure

    for word, count in count_words(args.text, args.top, args.lower):
        print(count, word)
    return 0

print("exit code:", main(["The cat saw the dog and the bird", "-n", "2", "--lower"]))
print("exit code:", main(["anything", "-n", "0"]))
try:
    main(["anything", "-n", "lots"])
except SystemExit as stop:
    print("argparse stopped the program with code", stop.code)
```

In a file of its own, the last two lines would be the entry point. They run only when the file is started directly:

```text
if __name__ == "__main__":
    sys.exit(main())
```

This pattern has several good features:

- the real work is in **small functions** that can be tested without a command line
- `main` takes the arguments as a **parameter**, so it can be tested too
- it **returns an exit code**: 0 for success, non zero for a failure, which is how other programs and scripts tell what happened
- errors go to the **error stream** (`stderr`), not to the normal output, so they do not mix into data that is being piped to another program
- `if __name__ == "__main__"` makes the file importable as well as runnable

### Packaging

A project with a `pyproject.toml` can be **built** into a file that others install with `pip`. A `[project.scripts]` entry creates a command, such as `shop`, that runs your `main`. Choose a **licence**, because code without one is by default not free for others to use. Licences such as MIT allow nearly anything, and others, such as the GPL, require changes to be shared too.

### Documentation

Documentation has different readers, and each needs something different:

| Document | For | Contains |
| **README** | anyone arriving at the project | what it does, how to install it, a short example, how to run the tests, the licence |
| **User guide** | the person using the program | tasks, step by step, with screenshots |
| **Technical documentation** | the next developer | the design, the data structures, how the parts fit, how to extend it |
| **Docstrings** | whoever calls a function | what it takes and returns |
| **Changelog** | users upgrading | what is new, changed and fixed in each version |

For a coursework project the final report is made of exactly these. A project that keeps its README, its tests and its commit history up to date while it is built finds the write-up is largely done by the end.

!exam Name the practice and its benefit :: Professional practice questions ask you to link a practice to a benefit for a project: version control to history and teamwork, a virtual environment to isolation, tests to confidence when changing code, documentation to maintainability.
"""),
    ],
    keyterms=[
        ("PEP 8", "The style guide for Python code, covering naming, layout and imports."),
        ("Docstring", "A string at the start of a function, class or module that documents it."),
        ("Doctest", "An example in a docstring, written as an interactive session, which is run automatically to check it."),
        ("Module", "A single Python file whose code and names can be imported and used elsewhere."),
        ("Package", "A folder of modules with an __init__.py file."),
        ("Virtual environment", "A private copy of Python and its libraries for one project, so that projects do not interfere."),
        ("Version control", "A system that records every change to files, so that earlier versions can be recovered and teams can work together."),
        ("Commit", "A saved snapshot of a project at a point in time, with a message and unique identifier."),
        ("Branch", "A separate line of development that can later be merged back."),
        ("Profiler", "A tool that measures how often each function is called and how long it takes."),
        ("Exit code", "A number returned by a program when it finishes, where 0 means success."),
        ("Semantic versioning", "A version number scheme of major.minor.patch, where the numbers show how big a change is."),
    ],
    grade="""
Professional practice questions want a practice linked to a specific benefit.

+ For version control, give two benefits: a history that can be restored, and several people working without overwriting each other
+ For readability, name features: meaningful names, docstrings, small functions, constants instead of magic numbers
+ For a virtual environment, say it isolates the project's libraries so that versions cannot clash
+ For performance, say to measure with a profiler before changing code, then change the algorithm before the details
+ For a third party library, give a benefit and a risk
""",
    mistakes=[
        "Committing passwords, keys or a whole virtual environment to a repository.",
        "Writing comments that repeat the code, such as '# add 1' above x += 1.",
        "Optimising before measuring, so that effort goes to the wrong part of the program.",
        "Putting real work at the top level of a module, so that importing it runs it.",
        "Using a single message such as 'update' for every commit, which makes the history useless.",
    ],
    quiz=[
        Q("Which naming style does PEP 8 recommend for a function?",
          ["snake_case", "PascalCase", "UPPER_CASE", "camelCase"], 0,
          "Functions and variables use lower case words separated by underscores. Classes use PascalCase."),
        Q("Why replace a 'magic number' such as 0.2 with a named constant?",
          ["The name explains what it means, and it can be changed in one place", "Constants run faster", "Python requires it", "It saves memory"], 0,
          "VAT_RATE is clearer than 0.2, and changing the rate means editing one line."),
        Q("What does a doctest do?",
          ["Runs the examples in a docstring and checks their output", "Documents the tests", "Tests the docs for spelling mistakes", "Counts the lines in a file"], 0,
          "It keeps the documentation honest, because an out of date example fails."),
        Q("What does `if __name__ == '__main__':` achieve?",
          ["The code in it runs when the file is run directly, but not when it is imported", "It makes the file run twice", "It stops the file being imported", "It marks the main function for the compiler"], 0,
          "When a file is imported, its __name__ is the module's name, so the condition is false."),
        Q("What is the purpose of a virtual environment?",
          ["To keep each project's libraries separate from others", "To make programs run faster", "To run Python in a browser", "To encrypt the code"], 0,
          "Different projects can then use different versions of the same library without clashing."),
        Q("What is a commit in Git?",
          ["A saved snapshot of the project with a message", "A copy of the project on a server", "A conflict between two branches", "A request for a review"], 0,
          "Each commit records the state of every file at a moment, and what was changed."),
        Q("What is a branch used for?",
          ["A separate line of work, so a feature can be developed without disturbing the working version", "Deleting old code", "Sending code to a server", "Checking spelling"], 0,
          "When the feature is ready it is merged back."),
        Q("Which should you do first when a program is too slow?",
          ["Measure it, to find which part is the bottleneck", "Rewrite it in a different language", "Remove the comments", "Buy a faster computer"], 0,
          "A profiler shows where the time is really going, which is often a surprise."),
        Q("What does an exit code of 0 mean?",
          ["The program finished successfully", "The program found no input", "The program crashed", "The program did nothing"], 0,
          "Any non zero code signals a failure, which scripts can test."),
        Q("In the version number 2.5.1, which number changes for a bug fix that adds no features?",
          ["The last one, 1", "The first one, 2", "The middle one, 5", "None of them"], 0,
          "In semantic versioning, the last number is the patch number, used for fixes."),
    ],
    exam=[
        EQ("Describe two features of readable program code and explain why readable code is important.", 4, [
            MP("Meaningful names for variables, functions and classes", ["names", "meaningful", "descriptive", "identifier"]),
            MP("Comments or docstrings that explain what the code does or why", ["comment", "docstring", "documentation", "explain"]),
            MP("Other features such as consistent layout (indentation), short subprograms, and constants instead of magic numbers", ["indent", "layout", "short", "constants", "magic number", "white space", "structure"]),
            MP("Readable code is easier to understand, test, debug and maintain, especially by someone other than the original programmer", ["maintain", "understand", "debug", "other programmer", "easier"]),
        ], "One feature is the use of meaningful names for variables, subprograms and classes, so that a reader can tell what each one holds or does. Another is comments and docstrings, which explain what the code does or why it was written that way, together with consistent indentation and layout and short subprograms that each do one job. Readable code is important because it is easier to understand, test, debug and maintain, especially for someone other than the original programmer, or for the same programmer returning months later.",
           command="Describe"),
        EQ("A student is developing a coursework project in a team of three. Explain two benefits of the team using version control.", 4, [
            MP("It keeps a history of every change, so an earlier working version can be restored if something goes wrong", ["history", "restore", "earlier version", "go back", "revert", "undo"]),
            MP("It shows who made each change and when, and why (the commit message)", ["who", "when", "message", "record", "log"]),
            MP("Team members can work on separate branches at the same time without overwriting each other's work", ["branch", "same time", "without overwriting", "separate", "at once"]),
            MP("Changes can then be merged, and conflicts identified, so that the work is combined safely", ["merge", "conflict", "combine", "combined"]),
        ], "Version control keeps a history of every change made to the project, so that an earlier working version can be restored if a change introduces a fault. It also records who made each change, when, and why, using the commit message. In a team, each member can work on a separate branch at the same time without overwriting anyone else's work, and the changes can later be merged, with any conflicts being identified, so the work is combined safely.",
           command="Explain"),
        EQ("Explain what the statement if __name__ == '__main__': does in a Python file, and why it is used.", 3, [
            MP("The code inside it only runs when the file is run directly as a program", ["directly", "run as a program", "run as a script", "main program"]),
            MP("It does not run when the file is imported as a module into another program", ["imported", "import", "module", "not run"]),
            MP("This allows the same file to be used both as a program and as a library of reusable functions", ["both", "library", "reuse", "reusable", "functions"]),
        ], "The code inside the statement only runs when the file is run directly as a program. It does not run when the file is imported as a module by another program, because then the name of the module is not '__main__'. This allows the same file to be used both as a program and as a library of functions that other programs can import and reuse.",
           command="Explain"),
        EQ("A program is running too slowly. Explain why the programmer should use a profiler before changing any of the code.", 3, [
            MP("A profiler measures how long each part of the program takes and how often it is called", ["measures", "how long", "time", "how often", "calls"]),
            MP("This shows where the bottleneck is, because programmers are often wrong when they guess", ["bottleneck", "guess", "wrong", "where the time"]),
            MP("So effort is spent on the part that will make a real difference, instead of making other code harder to read for no benefit", ["effort", "real difference", "waste", "harder to read", "worthwhile", "no benefit"]),
        ], "A profiler measures how long each part of the program takes and how many times each subprogram is called. This shows where the bottleneck really is, because programmers are often wrong when they guess which part is slow. The programmer's effort can then be spent on the part that will make a real difference, instead of wasting it on, and perhaps making harder to read, code that makes no noticeable difference to the speed.",
           command="Explain"),
        EQ("A programmer is deciding whether to use a third party library to handle a complex task or to write the code themselves. Discuss the advantages and disadvantages of using the library.", 6, [
            MP("It saves development time, because the code already exists", ["saves time", "already exists", "quicker", "faster to develop", "development time"]),
            MP("A widely used library has been tested by many users, so it is likely to contain fewer faults than new code", ["tested", "fewer faults", "fewer bugs", "reliable", "widely used"]),
            MP("It may include expert knowledge, such as security or efficiency, that the programmer does not have", ["expert", "security", "efficient", "specialist", "knowledge"]),
            MP("Disadvantage: the project depends on code written by others, which might be abandoned, change or contain security flaws", ["depends", "abandoned", "changes", "security flaw", "vulnerab", "no longer supported", "dependency"]),
            MP("Disadvantage: it may add size and complexity, and the licence may limit how the program can be used", ["licence", "license", "size", "complexity", "limit", "restrict"]),
            MP("A reasoned conclusion: use the library for a complex task, checking its licence and keeping it up to date", ["conclusion", "should use", "overall", "therefore", "i would", "up to date"]),
        ], "Using the library saves development time because the code already exists. A widely used library has been tested by many users, so it is likely to contain fewer faults than new code written by the programmer, and it may include expert knowledge, for example about security or efficiency, which the programmer does not have. However, the project then depends on code written by other people, which might be abandoned, change in ways that break the program, or contain security flaws, and the library may add size and complexity, while its licence may limit how the program can be used. For a complex task, the programmer should use the library, as long as its licence is checked and it is kept up to date.",
           command="Discuss"),
    ],
)
