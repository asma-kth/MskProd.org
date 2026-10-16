"""A Level Python: Turing machines, the limits of computation, and abstraction."""
from mskbuild.models import Topic, Section, Q, EQ, MP

INPUTS = {}
EXPECT = {}

TOPIC = Topic(
    slug="turing-machines-and-halting",
    title="Turing Machines and the Limits of Computation",
    spec="A Level 18",
    icon="i-brain",
    minutes=60,
    blurb="The simplest computer that can compute anything, simulated in Python. Build and trace Turing machines, see why programs can be data, watch the proof that no program can decide whether another will finish, then meet tractable and intractable problems, abstraction and automation.",
    fact="Alan Turing described his machine in 1936, nearly ten years before the first electronic computers were built. He invented the idea of a general purpose computer, and proved that some problems can never be solved by one, using nothing but pencil and paper.",
    sections=[
        Section("The Turing machine", r"""
In 1936 Alan Turing asked a precise question: *what does it mean to compute something?* His answer was the simplest machine that could still do it. A **Turing machine** has four parts:

- a **tape**: an endless row of cells, each holding one symbol (or a blank)
- a **read/write head** that sits over one cell, reads it, writes a symbol, and moves one cell left or right
- a **state**, from a finite list, that includes a *start* state and one or more *halting* states
- a table of **rules** (the transition function): given the current state and the symbol under the head, what to write, which way to move, and what state to go to next

Each step is: *read, write, move, change state.* The machine stops when it enters a halting state.

Nothing in the machine is more than a few lines of Python. The tape is a dictionary from position to symbol, so that it can grow in either direction.

```python
BLANK = "_"

def tape_text(cells, head):
    low = min(list(cells) + [head])
    high = max(list(cells) + [head])
    out = ""
    for i in range(low, high + 1):
        symbol = cells.get(i, BLANK)
        out += "[" + symbol + "]" if i == head else symbol     # the head is in brackets
    return out

def run_turing(rules, tape, start="start", limit=500, trace=False):
    cells = dict(enumerate(tape))
    head, state, steps = 0, start, 0
    while state not in ("halt", "accept", "reject") and steps < limit:
        symbol = cells.get(head, BLANK)
        if (state, symbol) not in rules:
            state = "reject"                       # no rule: the machine is stuck
            break
        write, move, state = rules[(state, symbol)]
        cells[head] = write
        head += {"R": 1, "L": -1, "S": 0}[move]
        steps += 1
        if trace:
            print(steps, state.ljust(7), tape_text(cells, head))
    final = "".join(cells.get(i, BLANK) for i in range(min(cells), max(cells) + 1)).strip(BLANK)
    return state, final, steps

# rules: (state, symbol read) -> (symbol to write, move, next state)
flip = {
    ("start", "0"): ("1", "R", "start"),
    ("start", "1"): ("0", "R", "start"),
    ("start", BLANK): (BLANK, "S", "halt"),
}

print(run_turing(flip, "1011", trace=True))
```

This machine inverts every bit: it walks right, replacing 0 with 1 and 1 with 0, and halts when it reaches a blank. Its whole program is the three rules.

### A machine that adds one

A more useful machine goes to the right-hand end of a binary number, then walks back left turning 1s into 0s until it finds a 0 (or the blank before the number) to turn into a 1. That is column addition with a carry.

```python
BLANK = "_"

def run_turing(rules, tape, start="start", limit=500):
    cells = dict(enumerate(tape))
    head, state, steps = 0, start, 0
    while state not in ("halt", "accept", "reject") and steps < limit:
        symbol = cells.get(head, BLANK)
        if (state, symbol) not in rules:
            state = "reject"
            break
        write, move, state = rules[(state, symbol)]
        cells[head] = write
        head += {"R": 1, "L": -1, "S": 0}[move]
        steps += 1
    final = "".join(cells.get(i, BLANK) for i in range(min(cells), max(cells) + 1)).strip(BLANK)
    return state, final, steps

add_one = {
    ("start", "0"): ("0", "R", "start"),       # walk right to the end
    ("start", "1"): ("1", "R", "start"),
    ("start", BLANK): (BLANK, "L", "carry"),   # step back onto the last digit
    ("carry", "1"): ("0", "L", "carry"),       # 1 + 1 = 0, carry on
    ("carry", "0"): ("1", "S", "halt"),        # 0 + 1 = 1, done
    ("carry", BLANK): ("1", "S", "halt"),      # ran off the front: the number grew a digit
}

for number in ["1011", "111", "0", "100"]:
    print(number, "->", run_turing(add_one, number))
```

### A machine that does what no finite state machine can

An FSM cannot check that a string is some `a`s followed by *the same number* of `b`s. A Turing machine can, because it can write on its tape. It crosses off one `a` (writing X), travels right to cross off one `b` (writing Y), returns, and repeats. If both run out together, the string is accepted.

```python
BLANK = "_"

def run_turing(rules, tape, start="start", limit=500):
    cells = dict(enumerate(tape))
    head, state, steps = 0, start, 0
    while state not in ("halt", "accept", "reject") and steps < limit:
        symbol = cells.get(head, BLANK)
        if (state, symbol) not in rules:
            state = "reject"
            break
        write, move, state = rules[(state, symbol)]
        cells[head] = write
        head += {"R": 1, "L": -1, "S": 0}[move]
        steps += 1
    return state, steps

same_number = {
    ("q0", "a"): ("X", "R", "q1"),         # cross off an a
    ("q0", "Y"): ("Y", "R", "q3"),         # no a's left: check only Y's remain
    ("q0", BLANK): (BLANK, "S", "accept"),
    ("q1", "a"): ("a", "R", "q1"),         # travel right to the first b
    ("q1", "Y"): ("Y", "R", "q1"),
    ("q1", "b"): ("Y", "L", "q2"),         # cross off a b
    ("q2", "a"): ("a", "L", "q2"),         # go back to the last X
    ("q2", "Y"): ("Y", "L", "q2"),
    ("q2", "X"): ("X", "R", "q0"),
    ("q3", "Y"): ("Y", "R", "q3"),
    ("q3", BLANK): (BLANK, "S", "accept"),
}

for text in ["", "ab", "aabb", "aaabbb", "aab", "abb", "ba", "abab"]:
    print(repr(text).ljust(10), run_turing(same_number, text, start="q0"))
```

The steps grow quickly with the length, because the head keeps travelling up and down the tape. A Turing machine is not a practical design. It is a design for *reasoning*.
"""),
        Section("Programs as data: the universal machine", r"""
Every machine so far had its rules written into the Python program. But the rules are just a dictionary: **data**. Write them as text, and one simulator can run any machine whose description you hand it.

```python
BLANK = "_"

def load(description):
    rules = {}
    for line in description.strip().split("\n"):
        state, read, arrow, write, move, new_state = line.split()
        rules[(state, read)] = (write, move, new_state)
    return rules

def run_turing(rules, tape, start="start", limit=500):
    cells = dict(enumerate(tape))
    head, state, steps = 0, start, 0
    while state != "halt" and steps < limit:
        symbol = cells.get(head, BLANK)
        write, move, state = rules[(state, symbol)]
        cells[head] = write
        head += {"R": 1, "L": -1, "S": 0}[move]
        steps += 1
    return "".join(cells.get(i, BLANK) for i in range(min(cells), max(cells) + 1)).strip(BLANK)

machine = '''
start 0 -> 1 R start
start 1 -> 0 R start
start _ -> _ S halt
'''

print(run_turing(load(machine), "0110"))
```

`run_turing` is now a **universal Turing machine**: a machine that reads the description of *another* machine, as data, and behaves exactly like it. Turing described this idea in 1936. It is the **stored program concept**: instructions and data held in the same kind of memory. A modern computer is a universal machine. The program you download is data until the processor fetches it and treats it as instructions.

### The Church-Turing thesis

Turing and the logician Alonzo Church, working separately, reached the same conclusion: anything that can be computed by following a clear, step by step method can be computed by a Turing machine. It is called a **thesis**, not a theorem, because "a clear step by step method" is an informal idea that cannot be proved equal to a mathematical definition. Every attempt to find a more powerful model of computation has failed.

A language or machine is **Turing complete** if it can simulate a Turing machine. Python is, and so is a spreadsheet with loops, and so is Conway's Game of Life. Turing completeness means it can compute *anything* that can be computed, given enough time and memory. It does not make it fast.

!key Why bother with a machine nobody builds? :: Because it is simple enough to prove things about. If a problem cannot be solved by a Turing machine, then by the Church-Turing thesis no computer, however fast or large, and in any language, will ever solve it. The next section is a problem like that.
"""),
        Section("The halting problem", r"""
Every programmer has written a loop that never ends. A natural wish: *a tool that reads any program and its input and warns you whether it will ever finish.* This is the **halting problem**:

> Given a program and an input, decide whether the program will eventually **halt** or will run **forever**.

Some cases are easy. `countdown(5)` stops. `forever()` plainly does not. Others are not. The Collatz process (halve even numbers, triple-and-add-one to odd ones, stop at 1) is a three line loop, and nobody on Earth knows whether it halts for *every* starting number.

Here are programs written as generators, so that each `yield` is one step. A runner can then give a program a limit on the steps it may take:

```python
def run_limited(program, limit):
    steps = 0
    for _ in program:
        steps += 1
        if steps >= limit:
            return None                  # still going: no verdict
    return steps

def countdown(n):
    while n > 0:
        n -= 1
        yield

def forever():
    while True:
        yield

def collatz(n):
    while n != 1:
        n = n // 2 if n % 2 == 0 else 3 * n + 1
        yield

print("countdown(5):", run_limited(countdown(5), 1000))
print("forever():", run_limited(forever(), 1000))
print("collatz(27) with a limit of 100:", run_limited(collatz(27), 100))
print("collatz(27) with a limit of 200:", run_limited(collatz(27), 200))

longest = max(range(1, 10000), key=lambda n: sum(1 for _ in collatz(n)))
print("below 10000, the longest is", longest, "with", sum(1 for _ in collatz(longest)), "steps")
```

Running a program for a while can prove that it **does** halt. It can never prove that it does not: when the limit is reached, the program might still stop on the very next step. That is why a timeout is a guess, not an answer. (The Run button on this site stops a program after ten seconds for the same reason.)

### Why no perfect checker can exist

Turing proved that **no program can solve the halting problem for all programs**. The proof is a contradiction. Suppose someone claimed to have written `halts(program)`, a function that always answers correctly. Use it to build a troublemaker that does the *opposite* of whatever the checker predicts about the troublemaker itself:

```python
def run_limited(program, limit):
    steps = 0
    for _ in program:
        steps += 1
        if steps >= limit:
            return None
    return steps

def make_paradox(halts):
    def paradox():
        if halts(paradox):           # the checker says: "paradox halts"
            while True:              # so do the opposite and never stop
                yield
        # the checker says: "paradox runs forever", so halt at once
    return paradox

candidates = {
    "always says halts": lambda program: True,
    "always says loops": lambda program: False,
}

for name, checker in candidates.items():
    paradox = make_paradox(checker)
    verdict = "halts" if checker(paradox) else "loops"
    steps = run_limited(paradox(), 10000)
    actual = "runs forever" if steps is None else "halts"
    print(name, "| predicted:", verdict, "| actually:", actual)
```

Both checkers are wrong about `paradox`. The proof works for *any* checker, because `make_paradox` builds a program that disagrees with whatever answer it is given. If `halts(paradox)` says yes, `paradox` loops. If it says no, `paradox` stops. There is no correct answer, so the checker cannot exist.

### What this means

A problem that no algorithm can solve is **undecidable** (or **non-computable**). The halting problem was the first one found, and it has consequences:

- No tool can find *every* infinite loop in *every* program.
- No tool can decide, for every program, whether it will ever do something harmful. A perfect virus scanner is impossible.
- No tool can decide whether two programs do exactly the same thing.

Practical tools do not try to be perfect. They find the common cases, use timeouts, or work on restricted languages where the question *can* be answered.
"""),
        Section("Tractable and intractable problems", r"""
Some problems can be solved in theory but not in practice. **Tractable** problems have an algorithm whose time grows as a **polynomial** in the size of the input (n, n squared, n cubed), so a computer can still cope when the input gets big. **Intractable** problems only have known algorithms whose time grows **exponentially** (2^n) or worse (n!), which become impossible long before the input is large.

```python
import math

print("n".ljust(6), "n squared".ljust(11), "2 to the n".ljust(12), "n factorial")
for n in (10, 20, 50, 100):
    print(str(n).ljust(6), ("%.1e" % n ** 2).ljust(11), ("%.1e" % 2 ** n).ljust(12), "%.1e" % math.factorial(n))
```

Suppose a computer carries out a billion steps a second. How long does an algorithm that needs 2^n steps take?

```python
def readable(seconds):
    for unit, size in (("years", 31536000), ("days", 86400), ("hours", 3600), ("minutes", 60)):
        if seconds >= size:
            amount = seconds / size
            return ("{:.1e}" if amount >= 1e6 else "{:,.0f}").format(amount) + " " + unit
    return "{:.1f} seconds".format(seconds)

for n in (30, 40, 50, 70, 100):
    print(n, "items:", readable(2 ** n / 1e9))
print("for comparison, the universe is about 1.4e+10 years old")
```

Doubling the speed of the computer adds *one* to the size of problem it can handle. For an exponential algorithm, no hardware upgrade is the answer.

### Checking is easier than finding

Many intractable problems share a pattern. Given an answer, **checking** it is quick. **Finding** the answer seems to need a huge search. Take the *subset sum* problem: is there a group of these numbers that adds up to the target?

```python
from itertools import combinations

numbers = [267, 493, 869, 961, 1000, 1153, 1246, 1598, 1766, 1922,
           2070, 2457, 2659, 2923, 3020, 3121, 3350, 3562, 3630, 3980]
answer = [869, 1153, 1766, 2457, 2923, 3350, 3562, 3980]
target = 20060

def verify(subset):
    return sum(subset) == target

print("checking a given answer:", verify(answer), "(one addition per number)")

checked = 0
found = None
for size in range(1, len(numbers) + 1):
    for subset in combinations(numbers, size):
        checked += 1
        if sum(subset) == target:
            found = subset
            break
    if found:
        break
print("searching from scratch took", checked, "checks to find", found)
```

Problems whose answers can be checked in polynomial time are called **NP**. Problems that can be *solved* in polynomial time are called **P**. Every problem in P is also in NP, but nobody knows whether P and NP are the same set, which is to say whether every problem with a quickly checkable answer also has a quick way of finding it. **P versus NP** is the best known unsolved problem in computer science, with a million dollar prize for solving it. Most experts think the answer is no.

### Living with intractable problems

When the exact answer is out of reach there are three honest options: solve a **smaller** version, use a **heuristic** that gives a good answer quickly (the nearest neighbour route in the dynamic programming topic), or accept an **approximation** with a known worst case. Delivery companies do exactly this for every van they send out.
"""),
        Section("Abstraction and automation", r"""
The skill behind all of computer science is deciding **what to ignore**.

**Abstraction** means removing details that are not needed so that you can concentrate on the ones that are. A map of the London Underground is the standard example. It leaves out distance, direction and the streets above, and keeps what a traveller needs: which stations connect, and on which lines. Several kinds are named in the specifications:

| Kind | Meaning | Example |
| **Representational abstraction** | A simplified version of the real thing | The Underground map; a variable standing for a bank balance |
| **Abstraction by generalisation** | Grouping things by what they share | A `Shape` class that `Circle` and `Square` inherit from |
| **Information hiding** | Hiding how something works from whoever uses it | Private attributes; the inside of a function |
| **Procedural abstraction** | A named procedure stands for a set of steps | `sort()` instead of the sorting code |
| **Functional abstraction** | A function seen only as inputs mapped to outputs | `sqrt(x)` |
| **Data abstraction** | Using data through its operations, not how it is stored | A stack with `push` and `pop` |
| **Problem abstraction (reduction)** | Stripping a problem until it matches one already solved | A maze becomes a graph, and finding the way out becomes a shortest path |

### Data abstraction in code

The same code can work on a stack regardless of how the stack is stored, because it uses only the operations:

```python
class ListStack:
    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        return self._items.pop()

    def is_empty(self):
        return not self._items

class LinkedStack:
    def __init__(self):
        self._top = None

    def push(self, item):
        self._top = (item, self._top)

    def pop(self):
        item, self._top = self._top
        return item

    def is_empty(self):
        return self._top is None

def reverse_word(word, stack):
    for letter in word:
        stack.push(letter)
    result = ""
    while not stack.is_empty():
        result = result + stack.pop()
    return result

print(reverse_word("abstraction", ListStack()))
print(reverse_word("abstraction", LinkedStack()))
```

`reverse_word` has no idea which kind of stack it was given, and does not need to. That is **information hiding** protecting the rest of the program from a change.

### Automation

**Automation** means putting an abstraction to work: *model* the problem, *design* an algorithm for the model, *implement* it in code, then *execute* it. A journey planner abstracts a transport network into a graph of stations and connections, which reduces "how do I get there?" to a shortest path problem, then the computer runs a search.

```python
network = {
    "Angel": ["Bank", "King's Cross"],
    "Bank": ["Angel", "Monument", "Liverpool Street"],
    "King's Cross": ["Angel", "Euston"],
    "Euston": ["King's Cross", "Warren Street"],
    "Warren Street": ["Euston", "Oxford Circus"],
    "Oxford Circus": ["Warren Street", "Green Park"],
    "Green Park": ["Oxford Circus", "Westminster"],
    "Westminster": ["Green Park", "Monument"],
    "Monument": ["Westminster", "Bank"],
    "Liverpool Street": ["Bank"],
}

def fewest_stops(start, goal):
    queue = [[start]]
    seen = {start}
    while queue:
        route = queue.pop(0)
        if route[-1] == goal:
            return route
        for neighbour in network[route[-1]]:
            if neighbour not in seen:
                seen.add(neighbour)
                queue.append(route + [neighbour])

route = fewest_stops("Angel", "Westminster")
print(" -> ".join(route))
print(len(route) - 1, "stops")
```

!exam Name the abstraction and say what was left out :: A mark for naming the kind of abstraction, such as representational or problem abstraction, and a mark for the detail removed (distances, streets, the storage method) and why that is safe to ignore.
"""),
    ],
    keyterms=[
        ("Turing machine", "An abstract machine with an endless tape, a read/write head and a table of rules, used as a model of what can be computed."),
        ("Transition function", "The table of rules that says, for each state and symbol read, what to write, which way to move and which state to enter."),
        ("Universal Turing machine", "A Turing machine that reads the description of any other Turing machine and simulates it."),
        ("Stored program concept", "Holding instructions and data in the same memory, so the instructions can be fetched and changed like data."),
        ("Church-Turing thesis", "The claim that anything that can be computed by a clear step by step method can be computed by a Turing machine."),
        ("Turing complete", "Able to simulate a Turing machine, and so able to compute anything that is computable."),
        ("Halting problem", "The problem of deciding, for any program and input, whether the program will halt or run forever. It is undecidable."),
        ("Undecidable (non-computable)", "A problem for which no algorithm can give a correct answer for every input."),
        ("Tractable", "A problem that can be solved by an algorithm whose running time grows polynomially with the input size."),
        ("Intractable", "A problem whose only known algorithms take exponential or worse time, so they are impractical for large inputs."),
        ("Abstraction", "Removing unnecessary detail so that you can concentrate on what matters."),
        ("Automation", "Putting an abstraction to work: modelling a problem, designing an algorithm, implementing it in code and executing it."),
    ],
    grade="""
This topic rewards precise definitions and a reason for every claim.

+ Define a Turing machine by its parts: tape, head, state and rules, and say each rule writes, moves and changes state
+ For the halting problem, say that no algorithm can decide it for all programs, and give the consequence
+ Do not say 'we have not found a way yet': the proof shows it is impossible
+ For intractable problems, give the growth (exponential or factorial) and the practical remedy (a heuristic)
+ For abstraction, name the kind and name what has been left out
""",
    mistakes=[
        "Saying the halting problem cannot be solved for any program. It can be solved for many; it cannot be solved for all of them with one algorithm.",
        "Describing an intractable problem as one with no solution. A solution exists; it just takes too long to find.",
        "Treating undecidable and intractable as the same. Undecidable means no algorithm at all; intractable means one exists but is far too slow.",
        "Writing 'a computer program that runs forever' for a Turing machine. A machine can stop; the point is that we cannot always tell.",
        "Giving the definition of abstraction without saying what is hidden or removed in the example.",
    ],
    quiz=[
        Q("Which of these is NOT part of a Turing machine?",
          ["A stack", "A tape", "A read/write head", "A table of rules"], 0,
          "A Turing machine has a tape, a head, a state and a table of rules. It has no separate stack."),
        Q("What does a rule of a Turing machine specify?",
          ["The symbol to write, the direction to move and the next state", "Only the next state", "The address of the next instruction", "The symbol to read and the next symbol to read"], 0,
          "A rule is chosen by the current state and the symbol under the head, and gives those three things."),
        Q("What is special about a universal Turing machine?",
          ["It can simulate any other Turing machine given its description", "It runs faster than other Turing machines",
           "It has a tape of unlimited size and other machines do not", "It can solve the halting problem"], 0,
          "It reads a description of another machine as data, which is the idea behind stored programs."),
        Q("What does it mean for a programming language to be Turing complete?",
          ["It can compute anything that a Turing machine can", "It has no syntax errors", "It can only be compiled", "It runs on every computer"], 0,
          "A Turing complete language can simulate a Turing machine, so it can compute anything computable."),
        Q("What is the halting problem?",
          ["Deciding whether any given program will finish or run forever", "Stopping a program that has a bug", "Finding the fastest way to halt a processor", "Deciding which algorithm is quickest"], 0,
          "Turing proved that no algorithm can answer this correctly for every program and input."),
        Q("Why can a time limit not solve the halting problem?",
          ["A program that is still running at the limit might stop just afterwards", "Time limits cannot be set on programs",
           "A program that halts always does so immediately", "Computers cannot measure time"], 0,
          "Running out of time proves nothing about whether the program would ever have stopped."),
        Q("What does 'undecidable' mean?",
          ["No algorithm can always give the correct answer", "The answer is a matter of opinion", "The algorithm is too slow to be useful", "The problem has no input"], 0,
          "An undecidable problem cannot be solved by any algorithm, however much time and memory are available."),
        Q("An algorithm takes 2^n steps for n items. What kind of problem is this likely to be?",
          ["Intractable", "Tractable", "Undecidable", "Impossible to write down"], 0,
          "Exponential growth makes the algorithm impractical for all but small inputs."),
        Q("A tube map leaves out distances and streets. What is this an example of?",
          ["Representational abstraction", "Encryption", "Compression", "Decomposition"], 0,
          "It is a simplified model of the real thing that keeps only what the traveller needs."),
        Q("Which statement about heuristics is correct?",
          ["They give a good answer quickly but not necessarily the best", "They always give the best answer", "They only work for tractable problems", "They are slower than checking every possibility"], 0,
          "A heuristic is a practical shortcut used when the exact answer would take too long to find."),
    ],
    exam=[
        EQ("Describe the components of a Turing machine.", 4, [
            MP("A tape divided into cells, each holding a symbol, which is unlimited in length", ["tape", "cells", "unlimited", "infinite", "endless"]),
            MP("A read/write head that reads the symbol in one cell, writes a symbol, and moves left or right", ["head", "read", "write", "move"]),
            MP("A state (from a finite set), including a start state and a halt (accepting) state", ["state", "start", "halt", "finite"]),
            MP("A table of rules (transition function) that gives the symbol to write, the move and the next state for each state and symbol", ["rules", "transition", "table", "instructions", "next state"]),
        ], "A Turing machine has a tape that is divided into cells, each of which holds one symbol, and which is unlimited in length. It has a read/write head, which reads the symbol in the current cell, can write a new symbol and then moves one cell left or right. It has a current state, from a finite set of states, which includes a start state and one or more halting states. It has a table of rules, the transition function, which says for each combination of state and symbol read what symbol to write, which way to move and which state to go to next.",
           command="Describe"),
        EQ("The transition table shows a Turing machine. The tape holds the symbols 1 0 1 1 followed by blanks, the head is over the first 1 and the machine is in the state S0. State the contents of the tape when the machine halts, and describe what the machine does.", 4, [
            MP("Reads 1, writes 0 and moves right, staying in S0 (and similarly for each symbol)", ["1", "0", "right", "s0"]),
            MP("Each 0 becomes a 1 and each 1 becomes a 0 as the head moves right", ["flip", "invert", "swap", "changes", "each"]),
            MP("When the head reaches a blank the machine halts", ["blank", "halt"]),
            MP("The tape then holds 0 1 0 0", ["0100", "0 1 0 0"]),
        ], "The machine reads each symbol in turn, writes the opposite bit, moves right and stays in S0. So 1 becomes 0, 0 becomes 1, 1 becomes 0 and 1 becomes 0. When it reaches the blank at the end of the data it halts. The tape then holds 0 1 0 0. The machine inverts every bit of a binary number.",
           command="State",
           figure="""```text
state   read   write   move   next state
S0      0      1       R      S0
S0      1      0       R      S0
S0      blank  blank   -      HALT
```"""),
        EQ("Explain what is meant by the halting problem, and why it is important.", 4, [
            MP("It is the problem of deciding whether a given program, with a given input, will eventually stop or run forever", ["stop", "finish", "halt", "run forever", "infinite loop"]),
            MP("Turing proved that it is impossible to write one algorithm that answers correctly for every program and input", ["impossible", "no algorithm", "cannot be solved", "proved", "undecidable", "not possible"]),
            MP("So it is an example of a problem that is non-computable (undecidable)", ["non-computable", "noncomputable", "undecidable", "not computable"]),
            MP("It shows there are limits to what computers can do, for example a program cannot be written that finds every infinite loop (or every virus)", ["limits", "infinite loops", "virus", "bugs", "every", "cannot be written"]),
        ], "The halting problem is the problem of deciding, for any program and any input, whether the program will eventually stop or will run forever. Alan Turing proved, by contradiction, that it is impossible to write a single algorithm that gives the correct answer for every program and input, which makes it an example of an undecidable, or non-computable, problem. It is important because it shows that there are limits to what computers can do, whatever their speed or memory. For example, it is impossible to write a program that is able to find every infinite loop in every other program.",
           command="Explain"),
        EQ("Explain the difference between a tractable problem and an intractable problem, giving an example of an intractable problem.", 4, [
            MP("A tractable problem can be solved by an algorithm in polynomial time (a reasonable amount of time)", ["polynomial", "reasonable", "practical", "n squared", "n^2"]),
            MP("An intractable problem has no known algorithm that solves it in polynomial time; the time grows exponentially or worse as the input grows", ["exponential", "factorial", "2^n", "grows", "no known"]),
            MP("So an intractable problem cannot be solved in a sensible time except for small inputs", ["small", "impractical", "too long", "unreasonable", "large inputs"]),
            MP("An example, such as the travelling salesperson problem (or timetabling, or cracking a password by brute force)", ["travelling salesperson", "salesman", "timetabling", "brute force", "knapsack"]),
        ], "A tractable problem is one that can be solved by an algorithm whose running time grows polynomially with the size of the input, so it can be solved in a reasonable amount of time even for large inputs. An intractable problem is one where there is no known algorithm that runs in polynomial time. The time needed grows exponentially or worse as the input grows, so it can only be solved in a sensible time for small inputs. An example of an intractable problem is the travelling salesperson problem, where the number of possible routes grows factorially with the number of towns.",
           command="Explain"),
        EQ("A company is developing a journey planner for a city's tram network. Discuss how abstraction and automation would be used in the development of the planner.", 6, [
            MP("Representational abstraction: the network is shown as a graph of stops and connections, leaving out detail such as the shape of the track and the buildings", ["graph", "stops", "connections", "leaving out", "detail", "remove"]),
            MP("Details such as distance or time between stops are kept as weights because they are needed", ["weight", "distance", "time", "needed", "kept"]),
            MP("Problem abstraction (reduction): finding a journey becomes a shortest path problem, which is already solved", ["shortest path", "reduce", "reduction", "already solved", "known algorithm"]),
            MP("An algorithm such as Dijkstra's (or A star) is chosen to solve the shortest path problem", ["dijkstra", "a star", "a*", "algorithm", "breadth first"]),
            MP("Automation: the model and algorithm are implemented in code and executed so that routes are found automatically, quickly and consistently", ["automation", "implement", "code", "executed", "program", "automatically"]),
            MP("A reasoned point about the limits: the abstraction might leave out something important (delays, walking time), so the model must be checked", ["delays", "walking", "important", "accuracy", "checked", "limit", "too simple"]),
        ], "Abstraction would be used to turn the real tram network into a simple model. The network can be represented as a graph, with stops as vertices and the connections between them as edges, leaving out details that a passenger does not need such as the shape of the track or the buildings, but keeping the travel time between stops as the weight of each edge. Problem abstraction then reduces the question 'what is the quickest way from A to B?' to a shortest path problem, for which there is already an algorithm such as Dijkstra's. Automation is then the process of implementing the model and the algorithm in code and executing it, so that the best route can be found automatically, quickly and consistently for any journey. The company would need to check that the abstraction has not left out something that matters, such as delays or the time spent walking between stops, since an over simplified model will give poor journeys.",
           command="Discuss"),
    ],
)
