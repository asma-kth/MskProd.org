"""A Level Python: finite state machines and regular expressions."""
from mskbuild.models import Topic, Section, Q, EQ, MP

INPUTS = {}
EXPECT = {}

TOPIC = Topic(
    slug="finite-state-machines-and-regex",
    title="Finite State Machines and Regular Expressions",
    spec="A Level 14",
    icon="i-flow",
    minutes=55,
    blurb="The simplest model of a computer: states, transitions and an input. Build acceptors and machines with output, write regular expressions in Python, prove with a test that the two describe the same languages, and see exactly what a finite machine cannot do.",
    fact="The pattern matching you use every day in search boxes and code editors comes from a 1951 paper by the mathematician Stephen Kleene, who proved that regular expressions and finite state machines can describe exactly the same things. Ken Thompson put the idea into a text editor in 1968.",
    sections=[
        Section("Finite state machines", r"""
A **finite state machine** (FSM) is a model of something that is always in exactly **one state** out of a fixed, finite list. It reads an **input**, and the current state plus that input decide the **next state**. Nothing else is remembered.

Many things work this way: a turnstile is *locked* or *unlocked*, a traffic light is *red*, *red and amber*, *green* or *amber*, a game enemy is *patrolling*, *chasing* or *fleeing*.

An FSM is described by:

- a set of **states**
- one **start state**
- the **inputs** it can read
- the **transitions**: for each state and input, the next state

A **state transition diagram** shows states as circles and transitions as labelled arrows. The same information fits in a **state transition table**, which is easy to put straight into code as a dictionary.

| Current state | Input | Next state |
| locked | coin | unlocked |
| locked | push | locked |
| unlocked | coin | unlocked |
| unlocked | push | locked |

```python
transitions = {
    ("locked", "coin"): "unlocked",
    ("locked", "push"): "locked",
    ("unlocked", "coin"): "unlocked",
    ("unlocked", "push"): "locked",
}

state = "locked"
for event in ["push", "coin", "coin", "push", "push"]:
    state = transitions[(state, event)]
    print(event, "->", state)
```

The whole behaviour of the turnstile is in that table. There are no `if` statements deciding what to do: the machine is *data*, and one short loop runs any machine you give it.

!key Finite means finite memory :: An FSM knows only which state it is in. It cannot remember how many coins it has seen, or what the last ten inputs were, unless there is a separate state for each possibility. That limit is what makes it simple, and it is also what stops it solving some problems, as the last section shows.
"""),
        Section("Machines that accept or reject", r"""
An **acceptor** has a set of **accepting states**, drawn with a double circle. It reads a whole string. If it finishes in an accepting state it **accepts** the string, otherwise it **rejects** it. The set of every string a machine accepts is its **language**.

This machine accepts binary strings that contain an **even number of 1s**. It has two states, because all it needs to remember is whether it has seen an even or an odd number so far.

```python
def accepts(machine, text):
    state = machine["start"]
    for symbol in text:
        if (state, symbol) not in machine["table"]:
            return False                        # no transition: the string is rejected
        state = machine["table"][(state, symbol)]
    return state in machine["accepting"]

even_ones = {
    "start": "even",
    "accepting": {"even"},
    "table": {("even", "0"): "even", ("even", "1"): "odd",
              ("odd", "0"): "odd", ("odd", "1"): "even"},
}

for text in ["", "0", "1", "11", "1011", "10101"]:
    print(repr(text), accepts(even_ones, text))
```

If a state has no transition for an input, the machine rejects. Drawings usually leave out this **dead state** (a state that can never lead back to acceptance) to keep the diagram readable.

### A surprising machine: is a binary number divisible by 3?

Read a binary number one bit at a time, from the left. Keep only its **remainder when divided by 3**. Reading another bit doubles the number and adds the bit, so the new remainder is `(2 * r + bit) % 3`. Three possible remainders means three states, and that is all the memory needed to test a number of any length.

```python
def accepts(machine, text):
    state = machine["start"]
    for symbol in text:
        state = machine["table"][(state, symbol)]
    return state in machine["accepting"]

def divisible_by_3():
    table = {}
    for remainder in range(3):
        for bit in "01":
            table[(remainder, bit)] = (2 * remainder + int(bit)) % 3
    return {"start": 0, "accepting": {0}, "table": table}

machine = divisible_by_3()
wrong = [n for n in range(200) if accepts(machine, bin(n)[2:]) != (n % 3 == 0)]
print("numbers the machine got wrong:", wrong)
print("transitions:", len(machine["table"]))
print(accepts(machine, "1100"), accepts(machine, "1101"))     # 12 and 13
```

### Machines with output: Mealy machines

An acceptor only answers yes or no. A **Mealy machine** also **writes an output on every transition**, so it can transform its input. This one adds 1 to a binary number. It reads the bits starting from the *least significant* end, as a column addition does, and carries as it goes.

```python
RULES = {
    ("carry", "0"): ("done", "1"),      # 0 plus the carry is 1, and the carry is used up
    ("carry", "1"): ("carry", "0"),     # 1 plus the carry is 0, and the carry moves on
    ("done", "0"): ("done", "0"),       # nothing left to add: copy the bit
    ("done", "1"): ("done", "1"),
}

def add_one(bits_lsb_first):
    state, out = "carry", []
    for bit in bits_lsb_first:
        state, written = RULES[(state, bit)]
        out.append(written)
    if state == "carry":
        out.append("1")                 # the carry ran off the end
    return "".join(out)

for n in [5, 6, 7]:
    lsb = bin(n)[2:][::-1]
    result = add_one(lsb)
    print(n, "->", int(result[::-1], 2))
```

On a transition diagram a Mealy machine's arrows are labelled `input / output`.
"""),
        Section("Regular expressions", r"""
A **regular expression** (regex) is a compact way of writing a *set of strings*. Instead of listing them, you describe their pattern. There are only three building blocks, and everything else is shorthand for them:

| Building block | Written | Meaning |
| **Concatenation** | `ab` | `a` followed by `b` |
| **Alternation** | `a\|b` | `a` or `b` |
| **Repetition** | `a*` | zero or more `a`s |

The shorthand most worth knowing:

| Pattern | Matches |
| `a+` | one or more `a` |
| `a?` | zero or one `a` |
| `a{3}` | exactly three `a` |
| `[abc]` or `[a-z]` | any one character from the set |
| `.` | any one character |
| `\d` | a digit |
| `\s` | white space |
| `( )` | a group, so that `(ab)*` repeats `ab` |
| `^` and `$` | the start and the end of the text |

Python's `re` module runs them. The key question is *how much of the text must match*:

```python
import re

print(re.fullmatch(r"\d+", "12abc"))             # None: the whole string must match
print(re.match(r"\d+", "12abc") is not None)     # True: matches at the start only
print(re.search(r"\d+", "ab12c").group())        # 12: finds it anywhere
print(re.findall(r"\b[A-Z][a-z]+\b", "Alice met Bob in Paris"))
print(re.sub(r"\s+", " ", "too    many   spaces"))
```

An acceptor decides whether the **whole** string is in its language, so `re.fullmatch` is the Python equivalent.

### Patterns that validate

```python
import re

plate = re.compile(r"[A-Z]{2}[0-9]{2} [A-Z]{3}")        # a current UK number plate
clock = re.compile(r"([01][0-9]|2[0-3]):[0-5][0-9]")    # a 24 hour time

for text in ["AB12 CDE", "ab12 cde", "AB12CDE", "XY99 ZZZ"]:
    print(text, bool(plate.fullmatch(text)))
for text in ["09:30", "23:59", "24:00", "7:05", "12:60"]:
    print(text, bool(clock.fullmatch(text)))
```

### Two traps

```python
import re

print(re.findall("a.c", "abc a.c"))        # the dot matches any character
print(re.findall(r"a\.c", "abc a.c"))      # \. matches only a real full stop

html = "<b>bold</b> and <i>it</i>"
print(re.findall(r"<.+>", html))           # greedy: takes as much as it can
print(re.findall(r"<.+?>", html))          # lazy: takes as little as it can
```

!warn Use raw strings :: Write patterns as `r"..."`. Without the `r`, Python reads `\d` and `\b` as string escapes before the regex engine sees them, and `"\b"` becomes a backspace character.
"""),
        Section("Two descriptions of the same languages", r"""
Regular expressions and finite state machines look like different tools: one is written text, the other a diagram. In fact, they describe **exactly the same sets of strings**. Any language you can write as a regular expression, some FSM accepts, and the other way round. These are called the **regular languages**.

You can test the claim. The regular expression `(0|10*1)*` says: any number of repeats of either a lone `0`, or a `1`, then any 0s, then another `1`. Each repeat uses 1s in pairs, so it should match exactly the strings with an even number of 1s: the language of the first machine in this topic. Try every binary string up to length 8:

```python
import re
from itertools import product

def accepts(machine, text):
    state = machine["start"]
    for symbol in text:
        state = machine["table"][(state, symbol)]
    return state in machine["accepting"]

even_ones = {
    "start": "even",
    "accepting": {"even"},
    "table": {("even", "0"): "even", ("even", "1"): "odd",
              ("odd", "0"): "odd", ("odd", "1"): "even"},
}
pattern = re.compile(r"(0|10*1)*")

disagree = []
tested = 0
for length in range(9):
    for chars in product("01", repeat=length):
        text = "".join(chars)
        tested += 1
        if (pattern.fullmatch(text) is not None) != accepts(even_ones, text):
            disagree.append(text)

print(tested, "strings tested;", len(disagree), "disagreements")
```

A second pair: the regex `(ab)*c` is `ab` repeated any number of times, then a `c`. Draw it as a machine: from the start, `a` leads to a state that expects `b`, and `b` leads back to the start. A `c` from the start reaches the only accepting state.

```python
import re
from itertools import product

machine = {
    "start": "S0",
    "accepting": {"S2"},
    "table": {("S0", "a"): "S1", ("S1", "b"): "S0", ("S0", "c"): "S2"},
}

def accepts(machine, text):
    state = machine["start"]
    for symbol in text:
        if (state, symbol) not in machine["table"]:
            return False
        state = machine["table"][(state, symbol)]
    return state in machine["accepting"]

pattern = re.compile(r"(ab)*c")
tested = 0
different = []
for length in range(7):
    for chars in product("abc", repeat=length):
        text = "".join(chars)
        tested += 1
        if (pattern.fullmatch(text) is not None) != accepts(machine, text):
            different.append(text)
print(tested, "strings tested;", len(different), "disagreements")
```

This is more than a curiosity. When you compile a regular expression, the engine builds a state machine from it and runs the input through that machine. The first stage of a compiler, which splits source code into words, is built the same way, as the next topic shows.

!key Where you meet FSMs :: Lexers and regex engines, network protocols (a TCP connection moves through states such as LISTEN, ESTABLISHED and CLOSED), vending machines and lifts, and the behaviour of characters in games.
"""),
        Section("What a finite state machine cannot do", r"""
Because an FSM has only a fixed number of states, it cannot count without a limit. Take a simple task: decide whether a string of brackets is **balanced**, meaning every `(` is closed by a matching `)`. `(())()` is balanced. `(()` and `())(` are not.

To check it you must remember how deeply nested you are. That depth could be 5, or 500, or 5 million. A machine with a fixed number of states can only count up to a fixed depth.

Here is a machine built for a maximum depth. Its state is the current depth:

```python
def make_machine(max_depth):
    table = {}
    for depth in range(max_depth + 1):
        if depth < max_depth:
            table[(depth, "(")] = depth + 1
        if depth > 0:
            table[(depth, ")")] = depth - 1
    return {"start": 0, "accepting": {0}, "table": table}

def accepts(machine, text):
    state = machine["start"]
    for symbol in text:
        if (state, symbol) not in machine["table"]:
            return False
        state = machine["table"][(state, symbol)]
    return state in machine["accepting"]

def balanced(text):
    depth = 0
    for symbol in text:
        depth += 1 if symbol == "(" else -1
        if depth < 0:
            return False
    return depth == 0

deep = "((((" + "))))"
for limit in (2, 3, 5):
    machine = make_machine(limit)
    print("depth limit", limit, ":", accepts(machine, "(())"), accepts(machine, deep), "| really balanced:", balanced(deep))
```

The machine with a limit of 2 wrongly rejects a perfectly good string of depth 4, and the machine with a limit of 3 does too. Raising the limit helps, but whatever limit you pick, there is a deeper string to defeat it. The function `balanced` has no such limit because the variable `depth` is a number that can grow, which is **unbounded memory**.

The extra memory that bracket matching needs behaves like a **stack**: push on `(`, pop on `)`. A machine with a stack is more powerful than an FSM. It can recognise languages such as the balanced brackets or `aaabbb` (n letter `a`s followed by n letter `b`s), which no FSM and no regular expression can. These are described by *grammars* instead, which is where the next topic starts.

!exam Say why, not just that :: 'An FSM cannot match balanced brackets' earns one mark. The second mark is the reason: it has a finite number of states, so it cannot count to an unlimited depth of nesting.
"""),
    ],
    keyterms=[
        ("Finite state machine", "An abstract machine that is in one of a finite number of states, and changes state in response to inputs according to a set of transitions."),
        ("State", "One of the conditions the machine can be in. It is the machine's only memory."),
        ("Transition", "A change from one state to another, triggered by an input."),
        ("State transition diagram", "A drawing of an FSM with circles for states and labelled arrows for transitions."),
        ("State transition table", "A table giving the next state for every combination of current state and input."),
        ("Accepting state", "A state, drawn as a double circle, in which finishing means that the input string is accepted."),
        ("Mealy machine", "A finite state machine that produces an output on each transition, as well as changing state."),
        ("Regular expression", "A pattern, built from concatenation, alternation and repetition, that describes a set of strings."),
        ("Regular language", "A set of strings that can be described by a regular expression and accepted by a finite state machine."),
        ("Greedy match", "A repetition that matches as much text as it can. Adding a question mark makes it lazy."),
    ],
    grade="""
FSM questions are about reading and drawing accurately, with a short reason for the limits.

+ Trace an input by writing the state after each symbol, and state the final state before you say accepted or rejected
+ In a diagram, mark the start state with an arrow, the accepting states with double circles, and label every arrow
+ For a Mealy machine, label arrows with input and output, and trace both
+ For regular expressions, say what each part does: `[0-9]{2}` is exactly two digits
+ Explain a limit with a cause: finite states, therefore no unbounded counting
""",
    mistakes=[
        "Saying an FSM 'remembers' its input. It only knows its state, which may have forgotten most of the history.",
        "Forgetting the start state, or drawing no accepting state, so the diagram cannot be read.",
        "Using `re.match` when the whole string has to match. Use `fullmatch`, or anchor with `^` and `$`.",
        "Leaving a full stop unescaped in a regex. `.` means any character; a literal full stop is `\\.`.",
        "Claiming regular expressions can match nested brackets. They cannot, because that needs a stack.",
    ],
    quiz=[
        Q("What does a finite state machine remember about the inputs it has already read?",
          ["Only which state it is currently in", "Every input in the order it arrived", "The last three inputs only", "How many inputs it has read"], 0,
          "The state is the machine's only memory. Anything it needs to remember must be built into the states."),
        Q("In a state transition diagram, what is a double circle used for?",
          ["An accepting state", "The start state", "A dead state", "An error message"], 0,
          "If the machine finishes reading the input in a double circled state, the input is accepted."),
        Q("What is the difference between an acceptor and a Mealy machine?",
          ["A Mealy machine produces an output on each transition, an acceptor only accepts or rejects", "An acceptor has more states than a Mealy machine",
           "A Mealy machine has no start state", "An acceptor can only read binary"], 0,
          "A Mealy machine transforms its input into an output as it goes. An acceptor just says yes or no at the end."),
        Q("What does the regular expression `ab*` match?",
          ["An a followed by any number of b, including none", "An a followed by at least one b", "The text ab repeated any number of times", "Either a or b, once"], 0,
          "The star applies only to the b before it, and means zero or more."),
        Q("Which regular expression matches exactly three digits?",
          ["[0-9]{3}", "[0-9]*3", "[0-9]+3", "3[0-9]"], 0,
          "A character class for the digits, followed by {3} for exactly three of them."),
        Q("What does `re.fullmatch(r'\\d+', '12abc')` return?",
          ["None, because the whole string is not digits", "A match for 12", "A match for 12abc", "An error"], 0,
          "fullmatch requires the entire string to fit the pattern, and abc is not digits."),
        Q("What does it mean to say a language is regular?",
          ["It can be described by a regular expression and accepted by a finite state machine", "Every string in it has the same length",
           "It has no more than ten strings", "It can only use the letters a and b"], 0,
          "Regular expressions and finite state machines describe exactly the same sets of strings."),
        Q("Why can a finite state machine not check that any string of brackets is balanced?",
          ["It has a finite number of states, so cannot count an unlimited depth of nesting", "It cannot read brackets",
           "It has no start state", "It can only read each symbol once"], 0,
          "To match unlimited nesting it would need unlimited memory, such as a stack."),
        Q("An FSM tracks a binary number's remainder when divided by 3. How many states does it need?",
          ["3", "2", "1", "As many as there are bits"], 0,
          "One state for each possible remainder: 0, 1 and 2. The length of the number does not matter."),
        Q("Which regex quantifier is lazy, matching as little as it can?",
          ["`.+?`", "`.+`", "`.*`", "`.{3}`"], 0,
          "Adding a question mark after a repetition turns it from greedy into lazy."),
    ],
    exam=[
        EQ("Describe what is meant by a finite state machine.", 3, [
            MP("It has a finite number of states and is in exactly one of them at a time", ["finite", "one state", "one at a time", "set of states", "number of states"]),
            MP("It reads inputs, and each input causes a transition to another (or the same) state", ["input", "transition", "changes state", "moves"]),
            MP("It has a start state, and may have accepting states or outputs", ["start", "accepting", "final", "output"]),
        ], "A finite state machine is an abstract model that has a finite number of states and is in exactly one of them at any time. It reads a sequence of inputs, and each input causes a transition from the current state to the next state (which may be the same state). It has a start state and may have one or more accepting states, or produce outputs, to show the result.",
           command="Describe"),
        EQ("The state transition table shows a finite state machine with states S0, S1 and S2. S0 is the start state and S2 is the only accepting state. Trace the input 0110, giving the state after each symbol, and state whether it is accepted.", 3, [
            MP("Starts in S0 and 0 leads to S0 (or follows the table correctly for the first symbols)", ["s0", "start"]),
            MP("Shows the states S0, S0, S1, S2, S2 (or follows the table correctly to the end)", ["s1", "s2", "s0, s0, s1, s2"]),
            MP("Concludes that it finishes in S2, an accepting state, so the input is accepted", ["accepted", "accept", "finishes in s2"]),
        ], "The machine starts in S0. Reading 0 from S0 gives S0. Reading 1 from S0 gives S1. Reading 1 from S1 gives S2. Reading 0 from S2 gives S2. The machine has finished in S2, which is an accepting state, so the input 0110 is accepted.",
           command="Trace",
           figure="""```text
current   input   next
S0        0       S0
S0        1       S1
S1        0       S0
S1        1       S2
S2        0       S2
S2        1       S2
```"""),
        EQ("Write a regular expression that matches a time in the 24 hour clock format HH:MM, where HH is from 00 to 23 and MM is from 00 to 59, for example 07:45 or 23:59.", 4, [
            MP("Hours: first digit 0 or 1 followed by any digit, giving 00 to 19", ["[01][0-9]", "0|1", "[0-1]"]),
            MP("Hours: or a 2 followed by 0 to 3, giving 20 to 23", ["2[0-3]", "20", "23"]),
            MP("Alternation between the two hour patterns, grouped with brackets", ["|", "(", ")", "alternation", "group"]),
            MP("A colon followed by minutes: 0 to 5 then any digit", [":", "[0-5][0-9]", "minutes"]),
        ], r"""```python
import re

clock = re.compile(r"([01][0-9]|2[0-3]):[0-5][0-9]")
print(bool(clock.fullmatch("07:45")), bool(clock.fullmatch("24:00")))
```

The hours are either a 0 or 1 followed by any digit (00 to 19), or a 2 followed by a digit from 0 to 3 (20 to 23), joined with | and grouped in brackets. These are followed by a colon, then the minutes: a digit from 0 to 5 followed by any digit.""",
           command="Write"),
        EQ("Explain why a finite state machine cannot be used to decide whether any string of brackets is balanced.", 3, [
            MP("To check the brackets the machine must keep count of how deeply they are nested", ["count", "depth", "nested", "nesting", "remember"]),
            MP("The nesting could be to any depth, but an FSM has a finite number of states", ["finite", "fixed number", "limited", "number of states"]),
            MP("So it would run out of states and cannot count without a limit (a stack is needed)", ["run out", "cannot count", "no limit", "unlimited", "stack", "more memory"]),
        ], "To check that brackets are balanced the machine needs to keep count of how many brackets are still open, which is how deeply they are nested. The nesting could go to any depth, but a finite state machine only has a fixed number of states, and its state is its only memory. It therefore runs out of states for a deep enough string and cannot count without a limit. A stack, which can grow as far as needed, is required instead.",
           command="Explain"),
        EQ("A game developer is deciding how to control the behaviour of an enemy character, which can patrol, chase the player, attack and flee. Discuss the use of a finite state machine for this.", 6, [
            MP("Each behaviour is a state, such as patrol, chase, attack and flee", ["state", "patrol", "chase", "attack", "flee"]),
            MP("Events, such as seeing the player or low health, trigger transitions between states", ["event", "transition", "trigger", "sees the player", "low health", "input"]),
            MP("Simple to design, draw and implement, for example as a table", ["simple", "easy", "table", "clear", "diagram"]),
            MP("Easy to test and debug, because the enemy is in exactly one known state at a time", ["test", "debug", "predictable", "one state", "known"]),
            MP("Disadvantage: the number of states and transitions grows quickly as behaviour becomes more complex", ["grows", "complex", "many states", "too many", "difficult to manage", "state explosion"]),
            MP("A reasoned conclusion: suitable for simple behaviour, but predictable, so something more advanced may be needed for complex enemies", ["conclusion", "suitable", "predictable", "overall", "therefore", "i would"]),
        ], "The enemy's behaviours can each be a state: patrol, chase, attack and flee. Events such as seeing the player, getting close, or health dropping low cause transitions between the states, so the whole behaviour can be written as a simple state transition table or drawn as a diagram. This is simple to design and implement, and because the enemy is always in exactly one known state it is easy to test and debug. The disadvantage is that as the behaviour becomes more complicated the number of states and the number of transitions between them grows quickly and becomes hard to manage, and the behaviour can become predictable. A finite state machine is therefore a good choice for an enemy with a handful of simple behaviours, but a more advanced technique may be needed if the characters have to behave in complicated ways.",
           command="Discuss"),
    ],
)
