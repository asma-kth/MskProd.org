"""GCSE Python: procedures, functions, parameters, scope and libraries."""
from mskbuild.models import Topic, Section, Q, EQ, MP

INPUTS = {}
# Blocks that are meant to fail, without a marker on the page giving it away.
EXPECT = {"exam 4 figure": "UnboundLocalError"}

TOPIC = Topic(
    slug="subprograms-and-parameters",
    title="Subprograms: Procedures, Functions and Parameters",
    spec="GCSE 3",
    icon="i-flow",
    minutes=35,
    blurb="Procedures and functions, parameters and return values, local and global variables, and how to split a program into subprograms the way the specification asks.",
    fact="The first book about programming, published in 1951 by the Cambridge team that built the EDSAC computer, was mostly about a library of subroutines: pieces of code written once and reused by everyone.",
    sections=[
        Section("Procedures and functions", r"""
A **subprogram** is a named block of code that does one job and can be called whenever it is needed. The exam distinguishes two kinds:

| | Procedure | Function |
| Does a job | Yes | Yes |
| Hands a value back | **No** | **Yes**, with `return` |
| Used as | A statement on its own: `greet("Asha")` | Part of an expression: `y = triple(7)` |

```pseudo
function triple(number)
    return number * 3
endfunction

procedure greet(name)
    print("Hello " + name)
endprocedure

y = triple(7)
greet("Asha")
```

Python uses `def` for both. What makes it a function is that it ends with a `return` that carries a value back to the caller.

```python
def triple(number):
    return number * 3

def greet(name):
    print("Hello " + name)

y = triple(7)
greet("Asha")
print(y)
```

### Parameters and arguments

A **parameter** is the variable named in the definition, waiting for a value. An **argument** is the actual value supplied when the subprogram is called.

```python
def area(width, height):
    return width * height

print(area(4, 5))                # 20: 4 is the argument for width, 5 for height
print(area(height=5, width=4))   # 20: named arguments can go in any order
```

Arguments are matched to parameters by **position**, so `area(5, 4)` and `area(4, 5)` give the same answer only because multiplication does not care. In `divide(10, 2)` the order matters a great deal.

### Return is not print

!warn A function that prints has not returned anything :: `print` shows a value to a person. `return` hands it to the program. A function that only prints gives back `None`, so you cannot use its result in a calculation.

```python
def double_print(n):
    print(n * 2)

def double_return(n):
    return n * 2

a = double_print(4)         # prints 8
b = double_return(4)        # prints nothing
print(a, b)                 # None 8
print(double_return(4) + 1) # 9
```

### Returning several values

`return` can carry more than one value. They arrive as a **tuple**, which you can unpack into separate variables.

```python
def stats(numbers):
    return min(numbers), max(numbers), sum(numbers) / len(numbers)

low, high, mean = stats([4, 9, 2, 7])
print(low, high, mean)      # 2 9 5.5
```

### Why split a program into subprograms

| Benefit | What it means in practice |
| Reuse | Write it once and call it from ten places, instead of copying it ten times |
| Easier to test | Each subprogram can be checked on its own with known inputs |
| Easier to read | `calculate_tax(price)` says what happens without showing how |
| Easier to change | A fix is made in one place and works everywhere |
| Team working | Different people write different subprograms at the same time |
"""),
        Section("Local and global variables", r"""
**Scope** is the part of the program where a variable can be used.

- A **local** variable is created inside a subprogram, and exists only while that subprogram runs. Its parameters are local too.
- A **global** variable is created outside every subprogram, and can be read from anywhere.

!diagram py-scope

```python
# raises: NameError
def make_total():
    total = 10
    return total

make_total()
print(total)
```

`total` was created inside the function and was thrown away when it finished. Outside, the name does not exist.

### Changing a global needs permission

A subprogram can *read* a global, but the moment it assigns to the name, Python treats the name as a new local variable instead. So this fails:

```python
# raises: UnboundLocalError
count = 0

def add_one():
    count = count + 1

add_one()
```

Python sees `count = ...` in the function, decides `count` is local, and then finds that the right hand side uses it before it has a value. OCR's reference language declares a global where it is created, as `global count = 0`. Python wants the word **inside the subprogram that needs to change it**, to say that the name means the global one:

```python
count = 0

def add_one():
    global count
    count = count + 1

add_one()
add_one()
print(count)            # 2
```

### Better: pass it in and return it

```python
def add_one(count):
    return count + 1

count = 0
count = add_one(count)
count = add_one(count)
print(count)            # 2
```

!key Why exam questions prefer local variables :: A subprogram that only uses its parameters and its own locals can be understood, tested and reused on its own. A global can be changed by any line anywhere, so when a global is wrong you have to search the whole program. Locals also release their memory when the subprogram ends, and two subprograms can use the same variable name without interfering.

### Constants

A **constant** is a value that never changes while the program runs, such as a tax rate. The exam writes `const VAT = 0.2`. Python has no enforcement, so the convention is capital letters:

```python
VAT = 0.2

def price_with_vat(price):
    return round(price * (1 + VAT), 2)

print(price_with_vat(50))     # 60.0
```

If the rate changes, one line changes. Had `0.2` been typed into twenty places, you would have to find all twenty.
"""),
        Section("Library subprograms and random numbers", r"""
Python comes with hundreds of subprograms already written. Some are always available, such as `len`, `round` and `abs`. The rest live in **libraries**, which you `import` before using.

```python
import math

print(math.sqrt(144))        # 12.0
print(math.pi)               # 3.141592653589793
print(math.ceil(7.1))        # 8
print(math.floor(7.9))       # 7
print(abs(-12), max(4, 9, 2), min(4, 9, 2))     # 12 9 2
```

### Random numbers

The exam writes `random(1, 6)`. The Python function is `random.randint`, and like the exam's it includes both ends.

```python
import random

random.seed(5)               # fixes the sequence so that this example repeats
rolls = []
for i in range(5):
    rolls.append(random.randint(1, 6))
print(len(rolls), all(1 <= r <= 6 for r in rolls))     # 5 True
print(random.choice(["red", "green", "blue"]) in ["red", "green", "blue"])    # True
```

`random.seed(5)` makes the "random" sequence the same every time the program runs, which is exactly what you want when testing. Remove it for the real game and each run is different.

### A program built from subprograms

Here is a complete program for a grading task, split the way an exam question wants it. Each subprogram does one job, and `report` is the only one that prints.

```python
def average(marks):
    total = 0
    for mark in marks:
        total = total + mark
    return total / len(marks)

def grade_for(mark):
    if mark >= 70:
        return "Distinction"
    elif mark >= 50:
        return "Merit"
    elif mark >= 40:
        return "Pass"
    return "Fail"

def report(name, marks):
    avg = average(marks)
    print(name, "averaged", round(avg, 1), "-", grade_for(avg))

report("Asha", [56, 71, 80])
report("Ben", [35, 42, 30])
```

The main program is now two lines, and each of the three subprograms can be tested alone: `grade_for(70)` should give `"Distinction"` and `grade_for(69.9)` should give `"Merit"`.

!exam Decomposition and subprograms go together :: A question that says "describe how the problem can be broken down" wants the pieces named, and a question that says "write the program" gives a mark for using a subprogram sensibly. Naming each piece with a verb (`calculate_tax`, `display_menu`, `validate_age`) tells the examiner what it does.
"""),
    ],
    keyterms=[
        ("Subprogram", "A named block of code that does one job and can be called from elsewhere in a program."),
        ("Procedure", "A subprogram that does a job but does not return a value."),
        ("Function", "A subprogram that returns a value to the code that called it."),
        ("Parameter", "A variable named in a subprogram's definition that receives a value when it is called."),
        ("Argument", "The actual value passed to a subprogram when it is called."),
        ("Local variable", "A variable declared inside a subprogram, which only exists while it runs."),
        ("Global variable", "A variable declared outside all subprograms, which can be used anywhere in the program."),
        ("Return value", "The value a function hands back to the code that called it."),
        ("Library", "A collection of ready made subprograms that is imported into a program."),
        ("Constant", "A named value that does not change while the program is running."),
    ],
    grade="""
Full marks on subprogram questions come from stating the exact term and linking it to the consequence.

+ Say parameter for the definition and argument for the call, and never swap them
+ State that a function returns a value and a procedure does not, with an example of each
+ Give a reason for local variables: they cannot be changed by accident and they free memory
+ Call a subprogram rather than copying its code, and say that is the reason
+ Write return, not print, when the question says "returns" or "calculates"
""",
    mistakes=[
        "Using print inside a function when the question asks it to return a value.",
        "Writing the call with the wrong number of arguments or in the wrong order.",
        "Assigning to a global variable inside a subprogram without declaring it global.",
        "Saying a parameter and an argument are the same thing.",
        "Putting the return inside the loop so the function stops after the first pass.",
    ],
    quiz=[
        Q("What is the difference between a function and a procedure?",
          ["A function returns a value and a procedure does not", "A procedure returns a value and a function does not",
           "A function uses parameters and a procedure cannot", "A procedure can only be called once"], 0,
          "Both do a job and both can take parameters. Only the function hands a value back to the caller."),
        Q("In `def triple(number):` and the call `triple(7)`, what is `7`?",
          ["An argument", "A parameter", "A return value", "A local variable"], 0,
          "The argument is the value supplied in the call. number is the parameter that receives it."),
        Q("What does a Python function that has no `return` statement give back?",
          ["`None`", "`0`", "An empty string", "An error"], 0,
          "A function with no return still finishes normally, and its result is None."),
        Q("Which keyword lets a subprogram change a global variable?",
          ["`global`", "`const`", "`return`", "`import`"], 0,
          "Without it, an assignment inside the subprogram creates a new local variable instead."),
        Q("Why are local variables preferred to global ones?",
          ["They cannot be changed by accident by other parts of the program", "They run faster in every case",
           "They are the only ones that can be numbers", "They are easier to type"], 0,
          "A local variable can only be touched by its own subprogram, so a bug in it cannot come from anywhere else."),
        Q("`def f(x): return x * 2`. What does `print(f(f(3)))` display?",
          ["12", "6", "3", "9"], 0,
          "The inner call f(3) gives 6, and that becomes the argument of the outer call, giving 12."),
        Q("Where can a local variable be used?",
          ["Only inside the subprogram where it is created", "Anywhere in the program after the line that created it",
           "Only in the main program, never inside a subprogram", "Inside any subprogram that is called by the one that created it"], 0,
          "Its scope is the subprogram. Outside it the name does not exist."),
        Q("Which is a benefit of using subprograms?",
          ["Code can be reused instead of copied", "The program always runs faster",
           "Variables no longer need names", "The program needs no testing"], 0,
          "Writing a job once and calling it many times means one fix works everywhere."),
        Q("What does `random.randint(1, 6)` produce?",
          ["A whole number from 1 to 6, including both", "A whole number from 1 to 5, because the top value is excluded",
           "A decimal number somewhere between 1 and 6", "A whole number from 0 to 6, including 0 and 6"], 0,
          "randint includes both ends, unlike range, which stops before its second value."),
        Q("A function ends with `return a, b`. What does it send back?",
          ["Both values, which can be unpacked into two variables", "Only the first value",
           "Only the last value", "An error, because return takes one value"], 0,
          "Python packs the two values into a tuple, and `x, y = f()` unpacks them again."),
    ],
    exam=[
        EQ("State two benefits of using subprograms in a program.", 2, [
            MP("Code can be reused without being written again", ["reuse", "reused", "re-use", "written once", "called", "again"]),
            MP("Each subprogram can be tested separately", ["test", "tested", "debug", "isolated"]),
            MP("Makes the program easier to read or maintain", ["read", "maintain", "understand", "shorter", "easier to change"]),
            MP("Different programmers can write different subprograms at the same time", ["team", "different programmers", "different people", "same time"]),
        ], "Subprograms let the same code be reused by calling it, rather than copying it each time it is needed. They also make a program easier to test, because each subprogram can be checked on its own with known values, and easier to read and maintain, because a fault only has to be fixed in one place.",
           command="State"),
        EQ("Write a Python function called circle_area that takes a radius as a parameter and returns the area of the circle, rounded to 2 decimal places. The area is pi multiplied by the radius squared.", 3, [
            MP("Defines a function with a parameter for the radius", ["def circle_area", "def", "radius"]),
            MP("Calculates pi * radius squared correctly", ["pi *", "* radius", "radius ** 2", "radius * radius", "math.pi", "3.14"]),
            MP("Rounds to 2 decimal places and returns the result", ["round", "return"]),
        ], r"""```python
import math

def circle_area(radius):
    return round(math.pi * radius ** 2, 2)

print(circle_area(3))
```

The function takes the radius as a parameter, calculates pi times the radius squared and rounds it to two decimal places. It uses return, so the caller can use the value. The call shown prints 28.27.""",
           command="Write"),
        EQ("Explain the difference between a local variable and a global variable.", 3, [
            MP("A local variable is declared inside a subprogram", ["inside", "within", "subprogram", "function"]),
            MP("A local variable can only be used in that subprogram and is lost when it ends", ["only", "ends", "finishes", "destroyed", "lost", "scope"]),
            MP("A global variable is declared outside subprograms and can be used throughout the program", ["outside", "throughout", "anywhere", "whole program", "any part"]),
        ], "A local variable is declared inside a subprogram. It can only be used within that subprogram and it stops existing when the subprogram finishes. A global variable is declared outside all subprograms, so it can be used from any part of the program, and it exists for as long as the program is running.",
           command="Explain"),
        EQ("The program shown produces an error. Explain why, and describe two ways it could be corrected.", 4, [
            MP("Assigning to total inside the function makes it a new local variable", ["local", "new variable", "assign", "inside the function"]),
            MP("The local total has no value when total + amount is worked out, so there is an error", ["no value", "before it", "not defined", "unbound", "not assigned", "error"]),
            MP("Correction one: declare total as global inside the function", ["global total", "global", "declare"]),
            MP("Correction two: pass total in as a parameter and return the new value", ["parameter", "return", "pass", "argument"]),
        ], r"""Because the function assigns to total, Python treats total as a new local variable. The right hand side then uses that local variable before it has been given a value, so the program stops with an error.

It can be corrected by declaring the variable global inside the function:

```python
total = 0

def add(amount):
    global total
    total = total + amount

add(5)
print(total)
```

A better correction is to pass the value in and return the result, so the function does not depend on a global at all:

```python
def add(total, amount):
    return total + amount

total = add(0, 5)
print(total)
```""",
           command="Explain",
           figure="""```python
total = 0

def add(amount):
    total = total + amount

add(5)
print(total)
```"""),
        EQ("Write a procedure called draw_box that takes a width and a height as parameters and displays a rectangle made of asterisks with that many columns and rows. For example, a width of 5 and a height of 3 displays three rows of five asterisks.", 4, [
            MP("Defines a subprogram with two parameters, width and height", ["def draw_box", "def", "width", "height"]),
            MP("A loop that repeats height times, one per row", ["range(height)", "for row", "for", "height times", "loop"]),
            MP("Displays width asterisks on each row", ["* width", "width *", "width", "inner loop"]),
            MP("Does not return a value, because it is a procedure", ["print", "no return", "does not return", "display"]),
        ], r"""```python
def draw_box(width, height):
    for row in range(height):
        print("*" * width)

draw_box(5, 3)
```

The loop runs once for each row. Multiplying a string by a number repeats it, so "*" * width makes one row of width asterisks, and print moves to a new line. It displays the box rather than returning anything, so it is a procedure.""",
           command="Write"),
    ],
)
