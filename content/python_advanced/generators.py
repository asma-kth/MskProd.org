"""Advanced Python: iterators, generators, itertools and lazy pipelines."""
from mskbuild.models import Topic, Section, Q, EQ, MP

INPUTS = {}
EXPECT = {}

TOPIC = Topic(
    slug="iterators-and-generators",
    title="Iterators and Generators",
    spec="Advanced 2",
    icon="i-repeat",
    minutes=55,
    blurb="How a for loop really works, and how to write functions that produce values one at a time with yield. Build your own iterators, write infinite generators, use generator expressions and itertools, and chain generators into a lazy pipeline that handles data of any size.",
    fact="In Python 2, range(1000000) built a list of a million numbers before the loop started, and a separate xrange gave the lazy version. Python 3 made range lazy by default. The change shows how much of the language rests on producing values one at a time instead of all at once.",
    sections=[
        Section("The iteration protocol", r"""
A `for` loop works on lists, strings, dictionaries, files, ranges and more. They have something in common, and it is a small protocol of two ideas:

- an **iterable** is anything you can loop over. It can produce an **iterator** when asked, with `iter()`.
- an **iterator** is the object that does the work. Each call to `next()` gives the next item, and when there are none left it raises **`StopIteration`**.

```python
numbers = [10, 20, 30]
iterator = iter(numbers)

print(next(iterator))
print(next(iterator))
print(next(iterator))

try:
    next(iterator)
except StopIteration:
    print("no more items")
```

A `for` loop is a neat way of writing exactly that. Here it is written out by hand:

```python
def my_for(iterable, body):
    iterator = iter(iterable)
    while True:
        try:
            item = next(iterator)
        except StopIteration:
            break
        body(item)

my_for("abc", print)
```

### Writing your own iterator

Any class with two methods works anywhere Python expects something to loop over: `__iter__` (returning the iterator itself) and `__next__` (returning the next value, or raising `StopIteration`).

```python
class Countdown:
    def __init__(self, start):
        self.current = start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current < 0:
            raise StopIteration
        value = self.current
        self.current -= 1
        return value

print(list(Countdown(3)))
for n in Countdown(2):
    print("liftoff in", n)
```

### Iterators are used up

A list can be looped over again and again, because every call to `iter()` on it gives a **fresh** iterator. An iterator itself remembers its place and does not rewind:

```python
items = iter([1, 2, 3])
print(sum(items))
print(sum(items))                  # nothing is left

numbers = [1, 2, 3]
print(iter(numbers) is iter(numbers))      # each call makes a new iterator
print(iter(items) is items)                # an iterator is its own iterator
```

!key Iterable or iterator? :: A list is an **iterable**: you can start over as often as you like. What `iter()` gives you is an **iterator**: a one way, one use cursor. Passing an iterator to two different loops means the second one finds nothing.
"""),
        Section("Generators: functions that pause", r"""
Writing a class with `__iter__` and `__next__` takes a lot of code for a simple idea. A **generator function** does the same thing with far less. Put `yield` where you would put `return`, and the function becomes a factory for iterators.

```python
def countdown(n):
    while n >= 0:
        yield n               # hand back a value, and pause here
        n -= 1

gen = countdown(3)
print(type(gen).__name__)
print(next(gen), next(gen))
print(list(gen))              # whatever is left
```

Calling a generator function does **not run it**. It returns a **generator object**. The body only runs when something asks for a value with `next()` (or a loop does). It runs until the next `yield`, hands the value over, and **freezes**, with all its local variables intact, until it is asked again. Watch the order of the prints:

```python
def noisy():
    print("start")
    yield 1
    print("middle")
    yield 2
    print("end")

g = noisy()
print("created")
print(next(g))
print(next(g))
try:
    next(g)
except StopIteration:
    print("finished")
```

When the function runs off the end, or reaches `return`, the generator raises `StopIteration` for you. That is the sign to a loop to stop.

### Lazy means on demand

A list holds all its items in memory at once. A generator makes each value only when it is wanted. That has two big benefits. The first is that a generator can be **infinite**, because it never has to hold everything:

```python
from itertools import islice

def fibonacci():
    a, b = 0, 1
    while True:                # no end: it stops only when the caller stops asking
        yield a
        a, b = b, a + b

print(list(islice(fibonacci(), 12)))      # take just the first twelve
```

The second is that work can be **avoided**. This program wants the first square above 50. Compare how many squares each version calculates:

```python
work = {"squares": 0}

def squares_list(n):
    result = []
    for i in range(n):
        work["squares"] += 1
        result.append(i * i)
    return result

def squares_gen(n):
    for i in range(n):
        work["squares"] += 1
        yield i * i

def first_over(values, limit):
    for value in values:
        if value > limit:
            return value

first_over(squares_list(100000), 50)
print("list version worked out", work["squares"], "squares")

work["squares"] = 0
first_over(squares_gen(100000), 50)
print("generator version worked out", work["squares"], "squares")
```

The list version built all 100 000 squares before the search began. The generator stopped as soon as it found one. The same applies to memory: a generator holds one value at a time, however long the sequence.

| | List | Generator |
| Values | all made at once | made one at a time, when asked |
| Memory | grows with the size | one value |
| Can be infinite | no | yes |
| Can be used again | yes | **no**: it is used up |
| Index or length | `items[3]`, `len(items)` | not available |
"""),
        Section("Generator expressions, yield from and send", r"""
A **list comprehension** builds a whole list. Change the square brackets to round ones and you have a **generator expression**, which builds nothing until asked:

```python
import sys

squares_list = [n * n for n in range(5)]
squares_gen = (n * n for n in range(5))
print(squares_list)
print(type(squares_gen).__name__)

total = sum(n * n for n in range(1, 100001))       # a hundred thousand squares, never held at once
print(total)

big_list = list(range(100000))
small = (n for n in range(100000))
print("generator is smaller:", sys.getsizeof(small) < sys.getsizeof(big_list))
```

When a generator expression is the only argument to a function, the extra brackets can go: `sum(n * n for n in ...)`.

### Short-circuiting

`any` and `all` stop as soon as the answer is known. With a generator they also stop the *work*:

```python
def check(n):
    print("checking", n)
    return n > 2

print(any(check(n) for n in [1, 2, 3, 4, 5]))
```

Items 4 and 5 were never even checked.

### yield from

A generator can hand over to another generator with **`yield from`**, which passes on every value it produces. It makes recursive generators short. This one flattens lists nested to any depth:

```python
def flatten(items):
    for item in items:
        if isinstance(item, list):
            yield from flatten(item)       # delegate to the inner generator
        else:
            yield item

print(list(flatten([1, [2, [3, 4]], 5])))
```

### send: values going in as well

`yield` can also **receive** a value. The caller uses `send()`, which resumes the generator and makes the `yield` expression equal to whatever was sent. A generator used like this is called a **coroutine**. This one keeps a running average:

```python
def running_average():
    total, count, average = 0, 0, None
    while True:
        value = yield average         # hand back the average, wait for the next value
        total += value
        count += 1
        average = total / count

avg = running_average()
next(avg)                              # run to the first yield
print(avg.send(10))
print(avg.send(20))
print(avg.send(60))
```

Coroutines like this are the idea behind the tasks in the scheduling topic, and behind `async` and `await`.
"""),
        Section("itertools: building blocks", r"""
The `itertools` module is a toolbox of fast, lazy building blocks for working with iterators. Each one takes iterables and returns an iterator, so they can be chained.

| Tool | What it produces |
| `count(10, 5)` | 10, 15, 20, 25, ... without end |
| `cycle("AB")` | A, B, A, B, ... without end |
| `islice(it, 4)` | just the first 4 items of any iterator |
| `chain(a, b)` | the items of a, then the items of b |
| `accumulate(items)` | running totals |
| `groupby(items)` | runs of equal neighbours, each with its group |
| `product(a, b)` | every pairing of one item from each (a nested loop) |
| `permutations(items, r)` | every ordering of r items |
| `combinations(items, r)` | every choice of r items, ignoring order |
| `pairwise(items)` | each item with the next one |
| `takewhile(test, items)` | items until the test first fails |

```python
from itertools import count, cycle, islice, chain, accumulate, groupby
from itertools import product, permutations, combinations, pairwise, takewhile, zip_longest

print(list(islice(count(10, 5), 4)))
print(list(islice(cycle("AB"), 5)))
print(list(chain([1, 2], "ab", (3,))))
print(list(accumulate([1, 2, 3, 4])))
print([(letter, len(list(group))) for letter, group in groupby("aaabbc")])
print(len(list(product("ab", repeat=3))), len(list(permutations("abcd", 2))), len(list(combinations(range(5), 2))))
print(list(pairwise([1, 4, 9, 16])))
print(list(takewhile(lambda n: n < 20, (n * n for n in count(1)))))
print(list(zip_longest("ab", [1, 2, 3], fillvalue="-")))
```

Notice what `groupby` did there: `("a", 3), ("b", 2), ("c", 1)` is run length encoding, from the compression topic, in one line. It only groups **neighbours**, so sort first if you want every equal item together.

`product` is the lazy form of a nested loop, and counting is a quick way to size a search. A four digit PIN has `len(list(product(range(10), repeat=4)))` possibilities:

```python
from itertools import product, islice

pins = product(range(10), repeat=4)
print(len(list(product(range(10), repeat=4))), "possible four digit PINs")
print(list(islice(pins, 3)))
```

!key Iterators in, iterators out :: Because every tool returns an iterator, you can combine them without ever making a big list. `sum(x for x in chain(a, b) if x > 0)` touches each item once, one at a time.
"""),
        Section("Pipelines: processing data of any size", r"""
Generators fit together like the stages of a factory line. Each takes an iterable and **yields** its output, and the next stage pulls from it. Items flow through **one at a time**. A pipeline can process a file of a hundred gigabytes using almost no memory, because only the item in each stage exists at any moment.

This pipeline reads log lines, turns each into a record, and keeps only the errors. The `print` in the first stage shows *when* each line is read:

```python
log = '''2025-03-01 INFO login ok user=amy
2025-03-01 ERROR disk full path=/var
2025-03-01 INFO upload ok user=ben size=40
2025-03-02 ERROR timeout host=db1
2025-03-02 WARN slow query ms=900
2025-03-02 ERROR timeout host=db2'''

def read_lines(text):
    for line in text.split("\n"):
        print("read:   ", line[:24])
        yield line

def parse(lines):
    for line in lines:
        date, level, message = line.split(" ", 2)
        yield {"date": date, "level": level, "message": message}

def only(level, records):
    for record in records:
        if record["level"] == level:
            yield record

pipeline = only("ERROR", parse(read_lines(log)))
print("pipeline built, nothing has run yet")
for record in pipeline:
    print("ERROR:  ", record["message"])
```

Nothing happens when the pipeline is built. Then, as the loop asks for each error, a line is read, parsed and tested, and the process repeats. The reads and the results are interleaved. A normal function-by-function version would read, and store, every line first.

Because each stage does one small job, each stage can be tested and reused on its own. The last stage can be any consumer: a loop, `sum`, `max`, `list`, or a `Counter`:

```python
from collections import Counter

log = '''2025-03-01 INFO login ok user=amy
2025-03-01 ERROR disk full path=/var
2025-03-01 INFO upload ok user=ben size=40
2025-03-02 ERROR timeout host=db1
2025-03-02 WARN slow query ms=900
2025-03-02 ERROR timeout host=db2'''

def parse(lines):
    for line in lines:
        date, level, message = line.split(" ", 2)
        yield {"date": date, "level": level, "message": message}

records = parse(log.split("\n"))
by_level = Counter(record["level"] for record in records)
print(by_level)
print("errors:", by_level["ERROR"], "| warnings:", by_level["WARN"])
```

### Files are already lazy

When you write `for line in open("big.log")`, Python does not read the whole file. A file object is an iterator that reads one line at a time. A pipeline that starts with a file keeps that benefit all the way down.

!exam Say what is evaluated when :: A generator question usually asks for the output of a program that prints inside the generator. The marks are for the *order*: nothing prints when the generator is created, each `next` runs up to the next `yield`, and a value is returned there.
"""),
    ],
    keyterms=[
        ("Iterable", "An object that can be looped over, because it can produce an iterator when `iter()` is called on it."),
        ("Iterator", "An object that returns the next item from a sequence each time `next()` is called, and raises `StopIteration` when there are no more."),
        ("StopIteration", "The exception that signals that an iterator has no more items. A for loop catches it and ends."),
        ("Generator", "A function containing `yield`, which returns an iterator that produces its values one at a time and pauses between them."),
        ("yield", "Hands a value back to the caller and pauses the generator, keeping its state, until the next value is requested."),
        ("Lazy evaluation", "Working out values only when they are needed, instead of all at once."),
        ("Generator expression", "A compact form like a list comprehension, written in round brackets, which produces values on demand."),
        ("yield from", "Delegates to another iterator, passing each of its values on as if they came from this generator."),
        ("Coroutine", "A generator that can also receive values, using `send()`, and so can be paused and resumed in both directions."),
        ("Pipeline", "A chain of generators in which each stage takes values from the one before and passes results on one at a time."),
    ],
    grade="""
Generator questions ask what is produced, and in what order, and why it is worth doing.

+ Say that calling a generator function does not run its body: it creates a generator object
+ For tracing, write the output in the order things happen: each `next` runs to the next `yield`
+ Give two benefits of laziness: low memory use, and no wasted work when the loop stops early
+ Say a generator can be used only once, and cannot be indexed or measured with `len`
+ For a pipeline, say each item passes through every stage before the next one is read
""",
    mistakes=[
        "Expecting a generator function to print something or do work when it is called. Nothing happens until the first `next`.",
        "Looping over the same generator twice. The second loop finds it empty.",
        "Using `return value` in a generator when `yield value` was meant, which ends it at once.",
        "Turning a generator into a list out of habit, which throws away the memory saving.",
        "Using `len()` or an index on a generator. It has neither.",
    ],
    quiz=[
        Q("What happens when a generator function is called?",
          ["It returns a generator object and does not yet run the body", "It runs the whole body and returns a list", "It runs to the first yield and prints a value", "It raises StopIteration"], 0,
          "The code only runs when something asks for a value with next() or a loop."),
        Q("What does the `yield` statement do?",
          ["Returns a value and pauses the function, keeping its state", "Ends the function for good", "Prints a value to the screen", "Restarts the function"], 0,
          "Unlike return, the local variables are kept so the generator can carry on from the same place."),
        Q("What does a for loop do when the iterator raises StopIteration?",
          ["Ends normally", "Crashes with an error", "Starts again from the beginning", "Skips the next item"], 0,
          "StopIteration is the signal that there are no more items, and the loop handles it."),
        Q("What is the main advantage of a generator over a list for a very long sequence?",
          ["It holds one value at a time, so uses very little memory", "It can be indexed quickly", "It can be sorted without a function", "It can be used again and again"], 0,
          "Values are produced on demand, so the whole sequence never exists in memory."),
        Q("A generator is used in a for loop which is finished. A second for loop is then run over the same generator. What happens?",
          ["The second loop does nothing, because the generator is used up", "The generator restarts", "An error is raised", "The loop runs twice as fast"], 0,
          "A generator is a one way iterator and cannot be rewound."),
        Q("Which of these is a generator expression?",
          ["(n * n for n in range(5))", "[n * n for n in range(5)]", "{n * n for n in range(5)}", "n * n in range(5)"], 0,
          "Round brackets make a generator expression. Square brackets make a list and curly ones a set."),
        Q("What does `yield from other()` do?",
          ["Passes on every value that other() produces", "Calls other() and discards the result", "Stops the generator", "Returns the first value of other()"], 0,
          "It delegates to another iterator, so a generator can be built from other generators."),
        Q("What does `any(check(n) for n in items)` do once check returns True?",
          ["Stops, without checking the remaining items", "Checks every item anyway", "Raises StopIteration", "Starts again from the first item"], 0,
          "any short-circuits, and since the generator is lazy the remaining checks are never made."),
        Q("In a pipeline of generators, in what order are items processed?",
          ["Each item goes through every stage before the next is read", "Every item goes through the first stage, then the second", "The stages run at the same time on different items", "In the reverse order"], 0,
          "Values are pulled through the chain one at a time."),
        Q("What does `itertools.islice(fibonacci(), 10)` give you?",
          ["The first ten items of an infinite generator", "A list of ten random numbers", "The tenth item only", "An error, since the generator is infinite"], 0,
          "islice takes a limited slice of any iterator, even one that never ends."),
    ],
    exam=[
        EQ("Explain what is meant by a generator in Python, and give one advantage of using a generator instead of building a list.", 3, [
            MP("A generator is a function that uses yield to produce a sequence of values one at a time", ["yield", "one at a time", "sequence", "produces values"]),
            MP("It pauses after each value and carries on from the same place when the next is requested", ["pause", "resume", "carries on", "remembers", "state"]),
            MP("Advantage: the values are made only when needed, so it uses far less memory than a list holding them all", ["memory", "only when needed", "on demand", "lazy", "one at a time", "less space"]),
        ], "A generator is a function that uses yield to produce a sequence of values one at a time. After each value it pauses, keeping its local variables, and carries on from the same place when the next value is requested. An advantage is that the values are only made when they are needed, so a generator uses far less memory than a list that holds every value at once, and can even produce an infinite sequence.",
           command="Explain"),
        EQ("The program shown is run. State the output, in the order it is displayed.", 4, [
            MP("start is output first, because calling the generator function does not run its body", ["start"]),
            MP("making 0 is output when the first next is called", ["making 0"]),
            MP("then 0 is output by the print statement", ["0"]),
            MP("making 1 and then 2 are output for the second next. The output is start, making 0, 0, making 1, 2", ["making 1", "2", "start, making 0, 0, making 1, 2"]),
        ], "The output is: start, making 0, 0, making 1, 2 (each on a separate line). Calling mystery(3) only creates the generator, so start is printed first. The first call of next runs the body until the first yield, which prints making 0 and returns 0, and that value is printed. The second call of next carries on from the yield, prints making 1 and returns 2, which is printed. The third item is never asked for, so making 2 is never printed.",
           command="State",
           figure="""```python
def mystery(n):
    for i in range(n):
        print("making", i)
        yield i * 2

g = mystery(3)
print("start")
print(next(g))
print(next(g))
```"""),
        EQ("Write a generator function called evens that takes a number, limit, and yields each of the even numbers from 0 up to but not including limit.", 3, [
            MP("A function definition with a parameter and a loop", ["def evens", "def", "for", "while", "range"]),
            MP("Selects the even numbers (steps of 2 or a modulus test)", ["% 2", "range(0, limit, 2)", ", 2)", "even"]),
            MP("Uses yield to produce each value", ["yield"]),
        ], r"""```python
def evens(limit):
    for n in range(0, limit, 2):
        yield n

print(list(evens(9)))
```

The function loops through the numbers from 0 in steps of 2 and uses yield to produce each one, so it is a generator. list(evens(9)) gives [0, 2, 4, 6, 8].""",
           command="Write"),
        EQ("Explain the difference between an iterable and an iterator in Python.", 3, [
            MP("An iterable is an object that can be looped over, such as a list or string", ["iterable", "can be looped", "list", "string", "loop over"]),
            MP("An iterator is the object that produces the items one at a time, using next()", ["iterator", "next", "one at a time", "produces"]),
            MP("An iterator is used up: it keeps its position and raises StopIteration at the end, but an iterable can be looped over again and again", ["stopiteration", "used up", "position", "again", "cannot be restarted", "remembers"]),
        ], "An iterable is an object that can be looped over, such as a list or a string, and it can give a new iterator whenever one is needed. An iterator is the object that produces the items one at a time each time next() is called, and it remembers its position. When it has no more items it raises StopIteration, and it is then used up, whereas an iterable such as a list can be looped over again and again.",
           command="Explain"),
        EQ("A program has to find the first line containing the word ERROR in a log file that is many gigabytes in size. Discuss whether the program should read the whole file into a list or process it using a generator.", 6, [
            MP("Reading the whole file into a list would need enough memory to hold every line", ["memory", "ram", "hold every line", "all of the file", "whole file"]),
            MP("The file might be larger than the available memory, so the program could crash or become very slow", ["crash", "larger than", "slow", "not fit", "too big"]),
            MP("A generator reads and processes one line at a time, so memory use stays small whatever the size of the file", ["one line at a time", "small", "constant", "whatever the size", "one at a time"]),
            MP("The generator stops as soon as the first matching line is found, so the rest of the file is never read", ["stops", "first", "as soon as", "rest of the file", "avoids", "wasted"]),
            MP("A list would allow the lines to be used again or looked up by index, which is not needed for this task", ["again", "index", "reused", "random access", "not needed", "repeat"]),
            MP("A reasoned conclusion: use a generator (or iterate over the file line by line)", ["conclusion", "should use", "generator", "better choice", "therefore", "overall"]),
        ], "A program that reads the whole file into a list would need enough memory to hold every line at once. If the file is several gigabytes this might be more than the computer has, so the program could crash or become very slow. A generator reads and handles one line at a time, so the memory used stays small whatever the size of the file. It also stops as soon as the first line containing ERROR is found, so the rest of the file is never read, saving time. A list would have the advantage that the lines could be used again or looked up by position, but this task does not need that. The program should therefore process the file with a generator, for example by looping over the file line by line.",
           command="Discuss"),
    ],
)
