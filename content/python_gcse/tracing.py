"""GCSE Python: trace tables, finding the purpose of an algorithm, and debugging."""
from mskbuild.models import Topic, Section, Q, EQ, MP

INPUTS = {}
EXPECT = {"exam 4 figure": "SyntaxError"}

TOPIC = Topic(
    slug="tracing-and-debugging",
    title="Trace Tables and Debugging",
    spec="GCSE 7",
    icon="i-bug",
    minutes=35,
    blurb="Working through an algorithm by hand with a trace table, saying what it is for, and finding and fixing the errors a question hides in it. These are the marks other candidates lose.",
    fact="In 1969 the Apollo 11 guidance computer raised overload alarms on the way down to the Moon. Software written by Margaret Hamilton's team had been designed to drop the unimportant jobs and keep the vital ones running, so the landing went ahead. She is credited with coining the phrase software engineering.",
    sections=[
        Section("Trace tables", r"""
A **trace table** records the value of every variable after each step of an algorithm. It is how you find out what code really does, as opposed to what you think it does, and it is a standard question on every GCSE paper.

The method never changes:

1. One **column** for each variable, plus one for the output
2. One **row** for each pass of a loop, or each time a variable changes, working strictly in program order
3. Write the value a variable has *after* the pass, and put a dash in a box only if the variable does not have a value yet

### Worked example 1: a loop

```python
total = 0
for i in range(1, 5):
    total = total + i * 2
    print(i, total)
```

| `i` | `total` | Output |
| - | 0 | - |
| 1 | 2 | 1 2 |
| 2 | 6 | 2 6 |
| 3 | 12 | 3 12 |
| 4 | 20 | 4 20 |

The loop runs for 1, 2, 3 and 4. It does not run for 5, because `range` stops before its second value.

### Worked example 2: a while loop with MOD and DIV

```python
number = 4721
total = 0
while number > 0:
    digit = number % 10
    total = total + digit
    number = number // 10
    print(digit, total, number)
print("Digit sum:", total)
```

| `number` | `digit` | `total` | Output |
| 4721 | - | 0 | - |
| 472 | 1 | 1 | 1 1 472 |
| 47 | 2 | 3 | 2 3 47 |
| 4 | 7 | 10 | 7 10 4 |
| 0 | 4 | 14 | 4 14 0 |
| - | - | - | Digit sum: 14 |

`number % 10` peels off the last digit and `number // 10` throws it away. When `number` reaches 0 the test `number > 0` is false and the loop ends. Notice that the last row has `number` equal to 0 and yet the `digit` of that row is 4, because the loop body ran once more with `number` still 4 before it was cut to 0.

!diagram py-trace-table

### Finding the purpose

Often the question does not ask for the table. It asks **what the algorithm does**. Trace it with small numbers and then describe the *result*, not the *steps*.

```python
a = 48
b = 18
while b != 0:
    temp = b
    b = a % b
    a = temp
print(a)
```

| `a` | `b` | `temp` |
| 48 | 18 | - |
| 18 | 12 | 18 |
| 12 | 6 | 12 |
| 6 | 0 | 6 |

It prints 6, which is the highest number that divides both 48 and 18. The algorithm finds the **highest common factor** of two numbers. It is more than 2,000 years old and is named after Euclid.

!exam Describe the result, not the steps :: "It sets temp to b, then b to a MOD b" is a description of the lines and earns nothing. "It outputs the highest common factor of the two numbers" is a description of the purpose and earns the mark. Trace with small values to see the answer, then state it in one sentence.
"""),
        Section("Finding and fixing errors", r"""
The exam gives you an algorithm that does not work, asks you to find the error, and asks for the corrected line. Nearly all of them are one of these:

| Fault | What it does | How you spot it |
| Off by one | Loop runs one time too many or too few | Compare the first and last values with the specification |
| Wrong comparison | `>` for `>=`, `and` for `or` | Test at the boundary |
| Variable started wrong | A maximum that begins at 0 | Test with all negative numbers |
| Variable reset in the wrong place | A total set to 0 inside the loop | Trace two passes of the loop |
| Return in the loop | A function stops after one item | Check indentation of `return` |
| Wrong type | Adding text to a number | Read the error message |

### Six faults, each one running

An off by one error. The aim is 1 to 5:

```python
for i in range(1, 5):
    print(i, end=" ")        # 1 2 3 4: the 5 is missing
print()
for i in range(1, 6):
    print(i, end=" ")        # 1 2 3 4 5
print()
```

A total reset in the wrong place. The aim is the average of three marks:

```python
marks = [50, 60, 70]

total = 0
for mark in marks:
    total = 0                # fault: this wipes out the running total
    total = total + mark
print(total / len(marks))    # 23.333333333333332

total = 0
for mark in marks:
    total = total + mark
print(total / len(marks))    # 60.0
```

A return inside the loop. The aim is to add every number:

```python
def total_of(numbers):
    total = 0
    for n in numbers:
        total = total + n
        return total         # fault: leaves the function on the first pass
    return total

print(total_of([1, 2, 3]))   # 1
```

The `return` must line up with the `for`, so it runs once the loop has finished. Move it left by one level and the answer is 6.

A starting value that is wrong. The aim is the largest number:

```python
numbers = [-4, -9, -2, -7]

largest = 0
for n in numbers:
    if n > largest:
        largest = n
print(largest)               # 0, which is not even in the list

largest = numbers[0]
for n in numbers:
    if n > largest:
        largest = n
print(largest)               # -2
```

A type error. Text and numbers cannot be joined with a plus:

```python
# raises: TypeError
score = 7
print("Score: " + score)
```

The fix is `print("Score: " + str(score))`, or `print("Score:", score)`.

An assignment where a comparison was meant:

```python
# raises: SyntaxError
score = 7
if score = 7:
    print("Seven")
```

Python catches this one before it runs and says `Maybe you meant '==' instead of '='`. A logic error you have to find yourself, and a syntax error the computer finds for you.

!key Correct the line, then say why :: A question that says "identify the error and correct it" has a mark for naming the line, a mark for the correct replacement, and often a mark for the effect the error has. State all three.
"""),
        Section("Debugging tools and techniques", r"""
**Debugging** is finding out why a program is wrong. The tools and habits below are in the specification, and they work in this order.

### Read the error message

The last line names the error and the line above it gives the position. Python's messages are written to be read.

### Print to see inside

The most common technique, and the one professionals still use first: print a variable at the point you are unsure about.

```python
def average(marks):
    total = 0
    for mark in marks:
        total = total + mark
        print("added", mark, "total is now", total)
    return total / len(marks)

print(average([50, 60, 70]))
```

### Test small, test early

Run each subprogram on its own with values you can work out in your head, before you build the next one on top of it.

### Check with assert

`assert` states something that must be true. If it is not, the program stops at that exact line and says so, which is far better than a wrong answer appearing three screens later.

```python
def grade_for(mark):
    if mark >= 70:
        return "Distinction"
    elif mark >= 50:
        return "Merit"
    return "Fail"

assert grade_for(70) == "Distinction"
assert grade_for(69) == "Merit"
assert grade_for(50) == "Merit"
assert grade_for(49) == "Fail"
print("All four tests passed")
```

### What an IDE gives you

An **integrated development environment** puts the tools in one program. The exam names these:

| Tool | What it does for you |
| Editor | Writes the code, with colour and automatic indentation |
| Error diagnostics | Highlights faults and reports their line |
| Run time environment | Runs the program so you can see the output |
| Translator | Turns the code into machine code, reporting syntax errors as it does |
| Debugger | Lets you run one line at a time |
| Breakpoint | Pauses the program at a chosen line |
| Variable watch | Shows the value of variables while it is paused |

!key A breakpoint plus a watch is a live trace table :: Pause the program at the line you do not trust, step forward one line at a time, and watch each variable change. It does by machine what you do on paper in a trace table.
"""),
    ],
    keyterms=[
        ("Trace table", "A table that records the value of each variable after every step of an algorithm."),
        ("Dry run", "Working through an algorithm by hand, without running it, to check what it will do."),
        ("Debugging", "Finding and fixing faults in a program."),
        ("Syntax error", "A mistake in the rules of the language, which stops the program from running."),
        ("Logic error", "A mistake that lets the program run but produces the wrong result."),
        ("Breakpoint", "A point in a program where a debugger pauses it, so the programmer can inspect it."),
        ("Variable watch", "A debugging tool that shows the current value of chosen variables as the program runs."),
        ("Off by one error", "A fault where a loop or an index is one too many or one too few."),
        ("IDE", "Integrated development environment: a program that combines an editor, translator and debugging tools."),
    ],
    grade="""
Tracing questions are the most reliably gained marks on the paper, and the most reliably thrown away.

+ Give every variable its own column, and write each row in the order the program runs
+ Trace with the exact numbers you were given, never with ones you invent
+ State the purpose of an algorithm as a result: highest common factor, total, count, maximum
+ When asked to correct an error, name the line, write the fixed line, and say what it now does
+ Name the IDE tool and what it does: a breakpoint pauses, a watch shows a value
""",
    mistakes=[
        "Skipping the final pass of a loop, or doing one pass too many.",
        "Describing what each line does instead of what the algorithm achieves.",
        "Writing the value before a line runs in a trace table instead of after it.",
        "Correcting a symptom, such as adding one to an answer, instead of the fault that caused it.",
        "Confusing a syntax error, which stops the program, with a logic error, which does not.",
    ],
    quiz=[
        Q("What does a trace table record?",
          ["The value of each variable after every step of an algorithm",
           "The time each line takes to run, so slow lines can be found",
           "The errors the translator found, together with their line numbers",
           "The names of every subprogram and where each one is called from"], 0,
          "It shows exactly how the variables change, which is how you work out what code really does."),
        Q("`x = 1`, then `y = 10`, then `while y > 4:` with `x = x * 2` and `y = y - 3` inside. What is `x` at the end?",
          ["4", "2", "8", "1"], 0,
          "Pass 1 gives x=2, y=7. Pass 2 gives x=4, y=4. Then 4 > 4 is false, so the loop ends with x equal to 4."),
        Q("What does `number % 10` give for `4721`?",
          ["1", "4", "472", "10"], 0,
          "% is MOD, the remainder after dividing by 10, which is the last digit."),
        Q("A function adds up a list but has its `return` inside the loop. What does it return for `[1, 2, 3]`?",
          ["1", "6", "3", "None"], 0,
          "The return runs on the first pass, so the function stops with only the first item added."),
        Q("A program finds the largest number by starting `largest = 0`. For which list does it give the wrong answer?",
          ["A list of only negative numbers", "A list of only positive numbers",
           "A list with ten items", "A list with one item"], 0,
          "Nothing in a list of negatives is greater than 0, so the answer stays 0, which is not in the list."),
        Q("Which of these is a syntax error?",
          ["`if x = 5:`", "Adding 1 instead of 2 each time", "Using `>` instead of `>=`", "Starting a loop at 1 instead of 0"], 0,
          "Using = where == was meant breaks the rules of the language, so the program cannot run at all."),
        Q("What does a breakpoint do?",
          ["Pauses the program at a chosen line", "Deletes the line", "Reports every error in the program", "Speeds the program up"], 0,
          "It lets the programmer stop at the line they do not trust, and inspect everything at that moment."),
        Q("What does a variable watch show?",
          ["The current value of a variable while the program is paused", "A list of all the variables in the language",
           "The memory address of the program", "How long a variable has existed"], 0,
          "It is the debugging equivalent of a column in a trace table."),
        Q("What is the best description of the purpose of a loop that keeps taking `a MOD b` until `b` is 0?",
          ["It finds the highest common factor of two numbers", "It finds the lowest common multiple of two numbers",
           "It sorts two numbers into ascending order", "It counts how many times one number goes into another"], 0,
          "That is Euclid's algorithm. State the result it produces, not the steps it takes."),
        Q("Which is the most useful first step when a program gives an error message?",
          ["Read the last line and the line number", "Delete the line it mentions", "Run it again until it works", "Add more comments"], 0,
          "The last line names the error and the position tells you where, which is nearly always enough to start."),
    ],
    exam=[
        EQ("The program shown is run. Complete the values of x and y after each pass of the loop, and state the value that is output.", 3, [
            MP("x is 2 and y is 7 after the first pass", ["2", "7", "first pass"]),
            MP("x is 4 and y is 4 after the second pass, and the loop then stops because 4 is not greater than 4", ["4", "stops", "ends", "4 > 4", "not greater"]),
            MP("The value output is 4", ["output is 4", "outputs 4", "prints 4", "displays 4", "4"]),
        ], "After the first pass x is 2 and y is 7. After the second pass x is 4 and y is 4. The condition y > 4 is now false, because 4 is not greater than 4, so the loop stops without a third pass, and the value output is 4.",
           command="Complete",
           figure="""```python
x = 1
y = 10
while y > 4:
    x = x * 2
    y = y - 3
print(x)
```"""),
        EQ("The algorithm shown is run with a = 48 and b = 18. State what the algorithm does, and the value it outputs.", 3, [
            MP("It finds the highest common factor of the two numbers", ["highest common factor", "hcf", "greatest common divisor", "gcd", "greatest common factor"]),
            MP("Of a and b, or 48 and 18", ["48 and 18", "a and b", "two numbers", "both numbers"]),
            MP("The value output is 6", ["6"]),
        ], "The algorithm finds the highest common factor of the two numbers, which is the largest whole number that divides exactly into both. For 48 and 18 the values of b are 18, 12, 6 and 0, and the algorithm outputs 6.",
           command="State",
           figure="""```python
a = 48
b = 18
while b != 0:
    temp = b
    b = a % b
    a = temp
print(a)
```"""),
        EQ("The program is meant to display the largest number in the list. Identify the error, explain what output it gives for this list, and write a corrected version of the line.", 4, [
            MP("largest is set to 0 before the loop", ["largest = 0", "starts at 0", "set to 0", "zero", "initial"]),
            MP("All the numbers in the list are negative, so none is greater than 0", ["negative", "less than 0", "none is greater", "all below"]),
            MP("The program outputs 0, which is not in the list", ["outputs 0", "output is 0", "displays 0", "prints 0", "0"]),
            MP("The corrected line is largest = numbers[0]", ["numbers[0]", "first item", "first number", "first element"]),
        ], "The error is that largest starts as 0. Every number in the list is negative, so none of them is greater than 0, the test never succeeds, and the program outputs 0, which is not in the list at all. The line should be largest = numbers[0], so the comparison starts from a value that really is in the list. The correct output is -2.",
           command="Identify",
           figure="""```python
numbers = [-4, -9, -2, -7]
largest = 0
for n in numbers:
    if n > largest:
        largest = n
print(largest)
```"""),
        EQ("The line shown is part of a program and it stops the program from running. Name the type of error and write the corrected line.", 2, [
            MP("It is a syntax error", ["syntax"]),
            MP("The corrected line is if score == 7:", ["==", "if score == 7"]),
        ], "This is a syntax error. A single equals sign assigns a value, and a comparison needs two, so the line should read if score == 7: and the program can then run.",
           command="Name",
           figure="""```python
score = 7
if score = 7:
    print("Seven")
```"""),
        EQ("Describe two features of an integrated development environment (IDE) that help a programmer to find and correct errors.", 4, [
            MP("A breakpoint pauses the program at a chosen line", ["breakpoint", "pause", "stop at a line"]),
            MP("So the programmer can inspect the state, or step through one line at a time", ["step", "one line at a time", "inspect", "examine", "check the values"]),
            MP("Error diagnostics highlight the line with a fault and describe the problem", ["diagnostic", "highlight", "error message", "reports", "underline", "line number"]),
            MP("So the programmer is taken straight to the fault without searching", ["straight to", "quickly", "find", "locate", "without searching", "where"]),
        ], "A breakpoint pauses the program at a line chosen by the programmer, so the values of the variables can be inspected, and the program can then be stepped through one line at a time to see exactly where the values stop being what was expected. Error diagnostics highlight the line containing a fault and describe the problem, so the programmer is taken straight to where it is rather than having to search the whole program for it.",
           command="Describe"),
    ],
)
