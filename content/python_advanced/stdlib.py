"""Advanced Python: the standard library toolbox."""
from mskbuild.models import Topic, Section, Q, EQ, MP

INPUTS = {}
EXPECT = {}

TOPIC = Topic(
    slug="the-standard-library-toolbox",
    title="The Standard Library Toolbox",
    spec="Advanced 6",
    icon="i-tools",
    minutes=70,
    blurb="Python comes with batteries included, and knowing what is in the box saves hours of work. Count with Counter, queue with deque, search with bisect, pick with heapq, parse with re, json and csv, calculate with decimal and statistics, handle files with pathlib, and build command line tools and safe database queries.",
    fact="Python's motto for its standard library is 'batteries included'. It ships with modules for sending email, parsing web addresses, compressing files, running a web server, reading databases and even playing with turtles. A program that does the same job with the standard library is usually shorter, faster and better tested than one written from scratch.",
    sections=[
        Section("collections: the right container for the job", r"""
Lists, dictionaries and sets cover most jobs. The `collections` module adds containers for the jobs they do awkwardly.

| Need | Use |
| count how many times each thing appears | `Counter` |
| a dictionary that creates missing entries itself | `defaultdict` |
| add and remove at **both ends** quickly | `deque` |
| a light record with named fields | `namedtuple` |
| look in several dictionaries in order | `ChainMap` |

```python
from collections import Counter, defaultdict

words = "the cat sat on the mat the end".split()

counts = Counter(words)
print(counts.most_common(2))
print(counts["the"], counts["dog"])                # a missing item counts as 0
print(Counter("mississippi").most_common(3))

by_length = defaultdict(list)                      # a missing key starts as an empty list
for word in words:
    by_length[len(word)].append(word)
print(dict(by_length))
```

With a plain dictionary, both of those jobs need an `if key in ...` before every update. `Counter` and `defaultdict` remove that code.

### deque: a queue that is fast at both ends

A list is slow at the front: `list.pop(0)` has to shift every other item along, which costs O(n). A **deque** (double ended queue) adds and removes at either end in O(1). With `maxlen` it also keeps only the newest items, which is perfect for a "last three readings" window:

```python
from collections import deque

window = deque(maxlen=3)
for reading in range(6):
    window.append(reading)
    print(list(window))

line = deque([1, 2, 3])
line.appendleft(0)
print(line.popleft(), line.pop(), list(line))
```

You can see the difference on a big queue (the exact times will vary on your computer):

```python
# varies
import time
from collections import deque

n = 20000
as_list = list(range(n))
start = time.perf_counter()
while as_list:
    as_list.pop(0)
list_time = time.perf_counter() - start

as_deque = deque(range(n))
start = time.perf_counter()
while as_deque:
    as_deque.popleft()
deque_time = time.perf_counter() - start

print("deque was faster:", deque_time < list_time)
print("by about", round(list_time / deque_time), "times")
```

Use a `deque` for the queue in a breadth first search.

### namedtuple and ChainMap

```python
from collections import ChainMap, namedtuple

Point = namedtuple("Point", "x y")
p = Point(3, 4)
print(p, p.x, p._asdict(), p._replace(x=9))

defaults = {"colour": "blue", "size": 3}
user = {"size": 7}
settings = ChainMap(user, defaults)                # look in user first, then defaults
print(settings["size"], settings["colour"])
```
"""),
        Section("Searching and ordering: bisect, heapq and functools", r"""
### bisect: binary search on a sorted list

`bisect` finds where a value belongs in an already sorted list, in O(log n). It is a ready made binary search. A neat use is turning **ranges** into answers, such as grade boundaries, without a chain of `if` statements:

```python
import bisect

boundaries = [40, 55, 70, 85]          # marks at which the grade changes
letters = "FDCBA"

def grade(mark):
    return letters[bisect.bisect(boundaries, mark)]

print([grade(mark) for mark in (10, 40, 69, 70, 99)])

items = [10, 20, 30]
bisect.insort(items, 25)               # insert and keep the list sorted
print(items, bisect.bisect_left(items, 20))

def contains(sorted_items, target):
    position = bisect.bisect_left(sorted_items, target)
    return position < len(sorted_items) and sorted_items[position] == target

print(contains(items, 25), contains(items, 26))
```

### heapq: the smallest and the largest

`heapq` is the heap from the data structures topic. Besides a priority queue it has `nlargest` and `nsmallest`, which pick the top few without sorting everything, and `merge`, which joins sorted inputs lazily:

```python
import heapq

scores = {"Ana": 82, "Raj": 91, "Mia": 77, "Joe": 91}
print(heapq.nlargest(2, scores, key=scores.get))
print(heapq.nsmallest(1, scores, key=scores.get))
print(list(heapq.merge([1, 4, 9], [2, 3, 10])))
```

### functools: tools for functions

You have met `lru_cache`, `partial` and `wraps`. Three more are worth knowing:

```python
from functools import cached_property, reduce, singledispatch

print(reduce(lambda a, b: a * b, range(1, 6)))     # 1 * 2 * 3 * 4 * 5

class Report:
    def __init__(self, data):
        self.data = data

    @cached_property                               # worked out once, then remembered
    def total(self):
        print("calculating...")
        return sum(self.data)

report = Report([1, 2, 3])
print(report.total)
print(report.total)

@singledispatch                                      # a different function for each type
def describe(thing):
    return "something else"

@describe.register
def _(thing: int):
    return "an integer"

@describe.register
def _(thing: list):
    return "a list of " + str(len(thing))

print(describe(5), describe([1, 2]), describe("text"))
```

`cached_property` is a property that runs its method only the **first** time and keeps the answer, which suits a value that is expensive to calculate and does not change. `singledispatch` chooses a function by the type of the first argument, so you avoid a chain of `isinstance` tests.
"""),
        Section("Text and data formats: re, json and csv", r"""
### Regular expressions in practice

You met `re` with finite state machines. These are the features that matter in everyday use: **groups** pull out parts of a match, **named groups** label them, and `sub` can call a function on every match:

```python
import re

text = "Contact: ana@school.org, raj.k@uni.ac.uk; call 0161 496 0123 or 07700 900123."
print(re.findall(r"[\w.]+@[\w.]+\w", text))
print(re.findall(r"\b0\d{3,4} ?\d{3} ?\d{3,4}\b", text))

found = re.search(r"(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})", "due 2025-03-14 sharp")
print(found.group("year"), found.groupdict(), found.span())

print(re.sub(r"(\d+)", lambda match: str(int(match.group(1)) * 2), "3 apples and 10 pears"))
print(re.split(r"[,;]\s*", "a, b;c,  d"))
```

### JSON: data in text

**JSON** is the format of web services and configuration files. `json.dumps` turns Python data into text and `json.loads` turns it back. Dictionaries, lists, strings, numbers, `True`/`False` and `None` map to objects, arrays, strings, numbers, `true`/`false` and `null`. Turning data into text to store or send it is called **serialisation**.

```python
import json
from dataclasses import asdict, dataclass

@dataclass
class Player:
    name: str
    score: int
    items: list

player = Player("Ana", 120, ["sword", "map"])
text = json.dumps(asdict(player), indent=2)
print(text)
print(Player(**json.loads(text)) == player)                 # the round trip is lossless

print(json.dumps({"b": 1, "a": [1, 2, None, True]}, sort_keys=True))
data = json.loads('{"x": 1.5, "tags": ["a"], "ok": true, "none": null}')
print(data, type(data["ok"]).__name__)
```

JSON has no dates or sets. A `default` function says how to encode anything else:

```python
import datetime
import json

def encode(thing):
    if isinstance(thing, datetime.date):
        return thing.isoformat()
    raise TypeError("cannot encode " + type(thing).__name__)

print(json.dumps({"due": datetime.date(2025, 3, 14)}, default=encode))
```

### CSV: tables in text

`csv` reads and writes comma separated tables, and gets the awkward cases right: fields that contain commas or quotes. Reading by **column name** with `DictReader` is far safer than counting positions:

```python
import csv
import io

raw = "name,score,year\nAna,82,10\nRaj,91,11\nMia,77,10\n"
rows = list(csv.DictReader(io.StringIO(raw)))
print(rows[0])
print("average:", round(sum(int(row["score"]) for row in rows) / len(rows), 2))

out = io.StringIO()
writer = csv.DictWriter(out, fieldnames=["name", "grade"], lineterminator="\n")
writer.writeheader()
for row in rows:
    writer.writerow({"name": row["name"], "grade": "A" if int(row["score"]) >= 80 else "B"})
print(out.getvalue())

awkward = io.StringIO()
csv.writer(awkward, lineterminator="\n").writerow(["Smith, Jo", 5, 'said "hi"'])
print(awkward.getvalue())
```

(`io.StringIO` is a file that lives in memory, so these examples need no files. With a real file you would write `open("scores.csv", newline="")`.) Notice that every value read from a CSV file is a **string**, so scores are converted with `int`.

### Tidying text

```python
import textwrap
from string import Template

print(textwrap.fill("Python's standard library is called batteries included because it ships with so much.", 30))
print(textwrap.shorten("a very long title for a very small box", 20, placeholder="..."))
print(Template("Dear $name, you scored $score").substitute(name="Ana", score=82))
```
"""),
        Section("Numbers, dates and statistics", r"""
### Dates and times

The `datetime` module does the awkward arithmetic of calendars: months of different lengths, leap years, weekdays. Subtracting two dates gives a `timedelta`.

```python
import datetime as dt

day = dt.date(2025, 3, 14)
print(day.strftime("%A %d %B %Y"))
print("weekday number:", day.weekday())                   # Monday is 0
print(day + dt.timedelta(days=30))
print("days to Christmas:", (dt.date(2025, 12, 25) - day).days)
print(dt.datetime(2025, 3, 14, 15, 30).isoformat())
print(dt.date.fromisoformat("2024-02-29").isocalendar().week)
```

Store and send dates as **ISO 8601** text (`2025-03-14`). It sorts correctly as plain text and cannot be confused between day and month. Be very careful with times across time zones, and store them in UTC.

### Exact arithmetic: decimal and fractions

Floating point numbers cannot store most decimal fractions exactly, so `0.1 + 0.2` is not exactly `0.3`. That is unacceptable for money. `Decimal` works in base ten and is exact, and `Fraction` keeps a ratio of whole numbers:

```python
from decimal import ROUND_HALF_UP, Decimal
from fractions import Fraction

print(0.1 + 0.2 == 0.3)
print(Decimal("0.1") + Decimal("0.2") == Decimal("0.3"))

price = Decimal("19.99")
print(price * 3)
print((price * 3 * Decimal("1.2")).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))

print(Fraction(1, 3) + Fraction(1, 6), float(Fraction(1, 3)))
```

Always build a `Decimal` from a **string**: `Decimal(0.1)` starts from the already inexact float.

### math

```python
import math

print(math.gcd(48, 18), math.lcm(4, 6), math.comb(5, 2))
print(math.isqrt(99), math.prod([1, 2, 3, 4]), round(math.log2(1024)))
```

`math.isqrt` is an exact integer square root, `comb(n, k)` counts the ways to choose k from n, and `prod` multiplies a sequence.

### statistics

```python
import statistics as st

marks = [62, 71, 71, 85, 90, 55, 71, 68]
print(st.mean(marks), st.median(marks), st.mode(marks))
print(round(st.stdev(marks), 2), st.quantiles(marks, n=4))

x = [1, 2, 3, 4, 5]
y = [2, 4, 5, 4, 6]
print("correlation:", round(st.correlation(x, y), 3))
slope, intercept = st.linear_regression(x, y)
print("best fit line: y =", round(slope, 2), "x +", round(intercept, 2))
```

The standard deviation says how spread out the marks are, `quantiles` splits them into four equal groups, and the correlation and best fit line measure how closely two lists move together. You will use these again in the machine learning topic.

### Random numbers: repeatable and secure

A `random.Random` object created with a **seed** gives the same sequence every time, which makes a simulation or a test **repeatable**. For anything security related, use the `secrets` module instead, which draws on the operating system's unpredictable source.

```python
import random

rng = random.Random(7)
print(rng.randint(1, 6), rng.choice(["rock", "paper", "scissors"]))
print(rng.sample(range(1, 50), 6))
print(round(rng.gauss(100, 15), 2))

cards = list(range(10))
rng.shuffle(cards)
print(cards)
```
"""),
        Section("Files, command lines and databases", r"""
### pathlib: files as objects

`pathlib.Path` treats a file path as an object. The `/` operator joins parts and works on every operating system, and methods read, write, list and search:

```python
import json
import tempfile
from pathlib import Path, PurePosixPath

folder = Path(tempfile.mkdtemp())              # a scratch folder
notes = folder / "notes"
notes.mkdir()
(notes / "a.txt").write_text("alpha\nbeta\n")
(notes / "b.txt").write_text("gamma\n")
(folder / "data.json").write_text(json.dumps({"n": 2}))

for path in sorted(folder.rglob("*")):
    print(path.relative_to(folder), path.suffix or "(folder)")

lines = sum(len(p.read_text().splitlines()) for p in notes.glob("*.txt"))
print(lines, "lines in all the text files")

name = PurePosixPath("reports/2025/summary.final.txt")
print(name.name, name.stem, name.suffix, name.parent, name.parts)
```

### Command line programs: argparse

A script that takes its settings from the **command line** can be reused and automated. `argparse` handles the options, checks their types, and writes the `--help` for you. `parse_args` can take a list, so you can test it here; in a real program you call it with no arguments and it reads `sys.argv`:

```python
import argparse

parser = argparse.ArgumentParser(prog="counter", description="Count words")
parser.add_argument("text")
parser.add_argument("-n", "--top", type=int, default=3, help="how many to show")
parser.add_argument("--lower", action="store_true", help="ignore case")

args = parser.parse_args(["the cat the dog", "-n", "1", "--lower"])
print(args)
print(args.text, args.top, args.lower)
```

### sqlite3: a database in the standard library

`sqlite3` gives you a full SQL database in a single file, or in memory. The most important lesson is how to put **values** into a query. Never build SQL by joining strings. Put a `?` placeholder where the value goes, and pass the values separately:

```python
import sqlite3

db = sqlite3.connect(":memory:")
db.execute("create table scores (name text, score int)")
db.executemany("insert into scores values (?, ?)", [("Ana", 82), ("Raj", 91), ("Mia", 77)])

name = "Ana'; DROP TABLE scores; --"                    # a typical injection attempt
print(db.execute("select * from scores where name = ?", (name,)).fetchall())

print(db.execute("select name, score from scores order by score desc limit 2").fetchall())
print(db.execute("select round(avg(score), 1), max(score) from scores").fetchone())
```

The attack text was treated as a *name to look for*, found nothing, and did no harm. Had the query been built as `"... where name = '" + name + "'"`, the quote in the input would have ended the string and the rest would have run as SQL. This is **SQL injection**, and for years it has been one of the most common causes of data breaches.

### zipfile: archives

```python
import io
import zipfile

buffer = io.BytesIO()
with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:
    archive.writestr("a.txt", "hello " * 100)
    archive.writestr("b/c.txt", "world")

with zipfile.ZipFile(io.BytesIO(buffer.getvalue())) as archive:
    for entry in archive.infolist():
        print(entry.filename, entry.file_size, "shrank:", entry.compress_size < entry.file_size)
```

!key Look before you write :: Before you write a utility, search the standard library and the Python documentation for it. The tested, documented, widely understood version is nearly always better than your own, and the next person to read the code will thank you.
"""),
    ],
    keyterms=[
        ("Counter", "A dictionary subclass for counting hashable items, where a missing item counts as zero."),
        ("defaultdict", "A dictionary that creates a default value for a missing key the first time it is used."),
        ("deque", "A double ended queue that adds and removes items at either end in constant time."),
        ("bisect", "A module for finding the position of a value in a sorted list by binary search."),
        ("Serialisation", "Converting data structures into a format, such as JSON text, that can be stored or sent and rebuilt later."),
        ("JSON", "A text format for structured data using objects, arrays, strings, numbers, true, false and null."),
        ("CSV", "Comma separated values: a text format for tables, with one row per line."),
        ("Decimal", "A number type that stores decimal fractions exactly, used for money."),
        ("Seed", "A starting value that makes a pseudo-random number generator produce the same sequence every time."),
        ("Command line argument", "A value or option supplied when a program is started, read by a program with argparse."),
        ("SQL injection", "An attack in which input is treated as part of an SQL command. It is prevented by using parameters in queries."),
        ("Parameterised query", "An SQL statement with placeholders for values, which are supplied separately and never treated as SQL."),
    ],
    grade="""
This topic gives practical, short questions. Show that you know which tool fits and why.

+ Name the right structure for the job: a Counter for tallies, a deque for a queue, a dictionary for lookup, a set for uniqueness
+ For money, say Decimal, and give the reason: floats cannot store most decimal fractions exactly
+ For databases, say parameters, and explain that this stops input being run as SQL
+ For file formats, say what each is for: JSON for nested data, CSV for tables
+ Mention repeatability when you seed a random number generator
""",
    mistakes=[
        "Using a list as a queue with pop(0), which is slow for long queues. Use a deque.",
        "Building SQL queries by joining strings, which allows SQL injection.",
        "Using floats for money, so that totals are off by tiny amounts.",
        "Forgetting that csv values are all strings.",
        "Using random for passwords or tokens. Use the secrets module.",
    ],
    quiz=[
        Q("Which collections type is best for counting how many times each word appears?",
          ["Counter", "deque", "namedtuple", "ChainMap"], 0,
          "Counter is a dictionary built for tallying, and a missing item counts as zero."),
        Q("Why is a deque better than a list for a queue with many items?",
          ["Removing from the front is O(1) instead of O(n)", "It uses less memory", "It keeps the items sorted", "It cannot overflow"], 0,
          "list.pop(0) shifts every other item along, whereas a deque removes from either end in constant time."),
        Q("What does `defaultdict(list)` do when you use a key that is not there yet?",
          ["Creates an empty list for that key", "Raises a KeyError", "Returns None", "Returns 0"], 0,
          "It supplies a default value, so you can append without checking first."),
        Q("What is the purpose of bisect?",
          ["To find where a value belongs in a sorted list by binary search", "To split a list into two halves", "To sort a list", "To remove duplicates"], 0,
          "It takes O(log n) steps because it uses binary search."),
        Q("Which module should be used to generate a password reset token?",
          ["secrets", "random", "math", "time"], 0,
          "random is predictable. secrets uses the operating system's secure source of randomness."),
        Q("What does `json.loads` do?",
          ["Turns JSON text into Python data", "Writes Python data to a file", "Turns Python data into JSON text", "Loads a file from the internet"], 0,
          "loads means load from a string. dumps does the reverse."),
        Q("When the csv module reads a file, what type are the values?",
          ["Strings", "Integers where possible", "Floats where possible", "Whatever type they look like"], 0,
          "Every value is text, so numbers must be converted."),
        Q("Why should `Decimal` be created from a string, as in `Decimal('0.1')`?",
          ["A float such as 0.1 is already inexact", "Strings are faster", "Decimal cannot take numbers", "It saves memory"], 0,
          "Decimal(0.1) would faithfully copy the tiny error already in the float."),
        Q("What does a seed do for a random number generator?",
          ["Makes it produce the same sequence every time", "Makes it more random", "Makes it faster", "Limits the range of numbers"], 0,
          "That is useful for tests and for repeatable simulations."),
        Q("Why use `cursor.execute('... where name = ?', (name,))` instead of joining the name into the SQL string?",
          ["The value cannot be treated as SQL, so injection is prevented", "It runs faster", "It is shorter", "Strings cannot contain quotes"], 0,
          "The database treats the value strictly as data, whatever characters it contains."),
    ],
    exam=[
        EQ("A program uses a list as a queue, removing items from the front with pop(0). Explain why a deque would be a better choice when the queue is very long.", 3, [
            MP("Removing the first item of a list means every other item has to be moved along one place", ["moved", "shifted", "every other item", "all the other items", "along"]),
            MP("So the time for this grows with the length of the list, O(n)", ["o(n)", "grows", "longer", "slow", "linear", "length"]),
            MP("A deque can remove from either end in constant time, O(1)", ["o(1)", "constant", "quick", "either end", "same time"]),
        ], "Removing the first item of a list means that every other item has to be moved along one place, so the time taken grows with the length of the list, which is O(n) and slow for a long queue. A deque can add and remove at either end in constant time, O(1), no matter how long it is, so it is a much better choice.",
           command="Explain"),
        EQ("The program shown is run. State the values output by each of the two print statements.", 3, [
            MP("The first print outputs [('the', 2), ('cat', 1)]", ["the", "2", "cat", "1"]),
            MP("The word the appears twice, and the first print shows the two most common", ["most common", "two", "twice", "2 times"]),
            MP("The second print outputs {3: ['the', 'cat', 'sat'], 2: ['on']}", ["3:", "2:", "on", "the', 'cat', 'sat"]),
        ], "The first print outputs [('the', 2), ('cat', 1)] because Counter counts the words and most_common(2) gives the two commonest, the appearing twice and cat (the first of the words that appear once) after it. The second print outputs {3: ['the', 'cat', 'sat'], 2: ['on']} because the defaultdict groups the words by their length, creating a new list for each length when it is first used.",
           command="State",
           figure="""```python
from collections import Counter, defaultdict

words = "the cat sat on the".split()
print(Counter(words).most_common(2))

groups = defaultdict(list)
for word in words:
    if word not in groups[len(word)]:
        groups[len(word)].append(word)
print(dict(groups))
```"""),
        EQ("A shop's program stores prices and calculates totals using floating point numbers. Explain why this can produce incorrect totals, and describe how Python's decimal module avoids the problem.", 4, [
            MP("Floating point numbers are stored in binary, and many decimal fractions such as 0.1 cannot be stored exactly", ["binary", "cannot be stored exactly", "exactly", "approximate", "0.1"]),
            MP("So small errors (rounding errors) are introduced, which can build up in calculations", ["rounding", "errors", "small errors", "build up", "inaccurate"]),
            MP("The decimal module stores numbers as decimal digits, so values like 19.99 are held exactly", ["decimal digits", "base ten", "exactly", "exact"]),
            MP("The results of calculations are exact and rounding can be controlled, which is important for money", ["money", "rounding can be controlled", "controlled", "exact", "currency"]),
        ], "Floating point numbers are stored in binary, and many decimal fractions, such as 0.1 or 19.99, cannot be stored exactly in binary. Small rounding errors are therefore introduced, and these can build up in calculations so that totals are slightly wrong. The decimal module stores numbers as decimal digits, so a value such as 19.99 is held exactly, and the results of calculations are exact and the way they are rounded can be controlled, which is important for money.",
           command="Explain"),
        EQ("Explain what is meant by serialisation, and give one example of a format that is used for it.", 3, [
            MP("Serialisation is converting data structures (objects) into a format that can be stored or sent", ["converting", "convert", "turn", "format", "transform"]),
            MP("so that the data can be saved to a file or sent over a network", ["file", "network", "stored", "sent", "transmit", "saved"]),
            MP("and later rebuilt, for example JSON, XML or CSV", ["json", "xml", "csv", "rebuilt", "reconstructed"]),
        ], "Serialisation is converting a data structure, such as a dictionary or an object, into a format that can be stored in a file or sent over a network, so that it can later be rebuilt from that format. JSON is an example of a format used for it, in which data is written as text using objects and arrays.",
           command="Explain"),
        EQ("A web application builds an SQL query by joining the text that a user types into a login form to the rest of the query. Discuss why this is a problem, and how the program should be changed.", 6, [
            MP("The user can type SQL commands into the form, which are then run by the database (SQL injection)", ["sql injection", "type sql", "commands", "injection", "run by the database"]),
            MP("An attacker could log in without a password, or read, change or delete data", ["without a password", "read", "delete", "change", "steal", "log in"]),
            MP("The input is not treated as data but as part of the command", ["part of the command", "not treated as data", "treated as sql", "code"]),
            MP("The program should use a parameterised query, with a placeholder for the value", ["parameterised", "parameter", "placeholder", "?", "prepared"]),
            MP("The database then treats the input only as data, whatever characters it contains", ["only as data", "as data", "never run", "cannot be run", "safe"]),
            MP("Input should also be validated, and the database account given only the permissions it needs", ["validate", "validation", "permissions", "least privilege", "limited"]),
        ], "If the text typed by the user is simply joined into the query, the user can type SQL commands into the form and the database will run them. This is called SQL injection. An attacker could log in without knowing a password, or read, change or delete data. The problem is that the input is not treated as data but as part of the command. The program should be changed to use a parameterised query, with a placeholder where the value goes and the typed value supplied separately, so that the database treats it only as data whatever characters it contains. The input should also be validated, and the database account used by the application should be given only the permissions that it needs.",
           command="Discuss"),
    ],
)
