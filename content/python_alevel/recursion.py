"""A Level Python: recursion, the call stack and backtracking."""
from mskbuild.models import Topic, Section, Q, EQ, MP

INPUTS = {}
EXPECT = {}

TOPIC = Topic(
    slug="recursion",
    title="Recursion",
    spec="A Level 1",
    icon="i-repeat",
    minutes=45,
    blurb="Functions that call themselves: the base case, the call stack and why it can overflow, memoisation, Tower of Hanoi and a backtracking maze solver, with every example runnable.",
    fact="Recursion is so central to how computers are described that a classic joke has the dictionary entry for it read: recursion, see recursion. LISP, designed in 1958, was the first widely used language built around functions that call themselves.",
    sections=[
        Section("Recursion and the call stack", r"""
A **recursive** subprogram is one that **calls itself**. It solves a problem by solving a smaller version of the same problem, and it needs two things:

- a **base case**, a version of the problem small enough to answer directly, with no further call
- a **recursive case**, which does a little work and calls itself with an argument that is **closer to the base case**

```python
def factorial(n):
    if n <= 1:                     # base case
        return 1
    return n * factorial(n - 1)    # recursive case

print(factorial(5))                # 120
```

`factorial(4)` cannot give its answer until `factorial(3)` has, and that waits on `factorial(2)`. The answer is built as the calls **unwind**:

```text
factorial(4)
= 4 * factorial(3)
= 4 * (3 * factorial(2))
= 4 * (3 * (2 * factorial(1)))
= 4 * (3 * (2 * 1))
= 24
```

### The call stack

Every call needs somewhere to keep its own parameters, local variables and the place to return to. The computer keeps these in a **stack frame**, and the frames are held on the **call stack**. A call pushes a frame. A return pops one.

!diagram py-call-stack

This version prints each call and each return, indented by how deep it is, so you can watch the stack grow and shrink:

```python
def factorial(n, depth=0):
    print("  " * depth + "call factorial(" + str(n) + ")")
    if n <= 1:
        print("  " * depth + "base case, return 1")
        return 1
    result = n * factorial(n - 1, depth + 1)
    print("  " * depth + "return " + str(result))
    return result

factorial(4)
```

### Without a base case

If the recursion never reaches a base case, frames pile up until the stack is full. Python stops it at about a thousand frames and raises a `RecursionError`. Other languages call the same event a **stack overflow**.

```python
# raises: RecursionError
def runaway(n):
    return runaway(n + 1)

runaway(0)
```

!warn The base case is not enough on its own :: Every recursive call must move **towards** it. `factorial(n)` that calls `factorial(n + 1)` has a perfectly good base case and will never reach it.

### More small examples

The same pattern, a base case and a smaller problem, solves many things. In each, find the base case first.

```python
def sum_list(items):
    if items == []:
        return 0
    return items[0] + sum_list(items[1:])     # the head, plus the sum of the tail

def reverse(text):
    if len(text) <= 1:
        return text
    return reverse(text[1:]) + text[0]

def gcd(a, b):
    if b == 0:
        return a
    return gcd(b, a % b)

print(sum_list([4, 8, 15, 16]))      # 43
print(reverse("recursion"))          # noisrucer
print(gcd(48, 18))                   # 6
```

`sum_list` splits a list into its **head** (`items[0]`) and its **tail** (`items[1:]`). You will meet that pair again in functional programming.
"""),
        Section("The cost of recursion, and how to cut it", r"""
Recursion is elegant and it is not free. The call stack takes memory, and the naive version of some recursive functions repeats the same work again and again.

### The Fibonacci trap

Each Fibonacci number is the sum of the two before it, so the definition is recursive. The code writes itself:

```python
calls = 0

def fib(n):
    global calls
    calls += 1
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

print(fib(20), calls)       # 6765 21891
```

Twenty one thousand calls to get an answer that needs twenty additions. `fib(5)` calls `fib(3)` and `fib(4)`, and `fib(4)` calls `fib(3)` again. The tree of calls roughly doubles with each step, so the work grows as 2 to the power of n.

### Memoisation

**Memoisation** stores each result the first time it is worked out, so a repeat call is answered from the store. Python's `functools.lru_cache` does it with one line.

```python
from functools import lru_cache

calls = 0

@lru_cache(maxsize=None)
def fib(n):
    global calls
    calls += 1
    if n < 2:
        return n
    return fib(n - 1) + fib(n - 2)

print(fib(80), calls)       # 23416728348467685 81
```

`fib(80)` would take longer than a human lifetime without the cache. With it, the function body runs just 81 times, once for each value from 0 to 80. This trades **memory** for **time**.

### Recursion or iteration

Anything recursion can do, a loop can do, and the reverse. Choosing between them is a judgement.

| | Recursion | Iteration |
| Code for tree shaped or self similar problems | Short and close to the definition | Needs a stack you manage yourself |
| Memory | One stack frame per call | A fixed amount |
| Speed | A call has overhead | Faster |
| Risk | `RecursionError` if too deep | None |
| Easy to trace | Harder | Easier |

```python
def factorial_loop(n):
    result = 1
    for i in range(2, n + 1):
        result = result * i
    return result

print(factorial_loop(5))     # 120
```

In Python the limit matters in practice, because the language does not optimise a call that is the last thing a function does:

```python
# raises: RecursionError
def depth(n):
    if n == 0:
        return 0
    return 1 + depth(n - 1)

print(depth(900))
print(depth(5000))
```

!key Which to choose :: Prefer recursion when the problem is naturally made of smaller copies of itself, such as a tree, a file system, or splitting a list in half. Prefer a loop when the problem is simply "repeat this n times", or when n could be large.
"""),
        Section("Problems that recurse: Hanoi, nesting and backtracking", r"""
### Tower of Hanoi

Three pegs and a stack of disks, largest at the bottom. Move the whole stack to another peg, one disk at a time, never putting a bigger disk on a smaller one. The recursive idea: to move *n* disks, move the top *n - 1* out of the way, move the biggest, then move the *n - 1* back on top.

```python
def hanoi(n, source, target, spare):
    if n == 0:
        return 0
    moves = hanoi(n - 1, source, spare, target)
    print("move disk", n, "from", source, "to", target)
    moves = moves + 1
    moves = moves + hanoi(n - 1, spare, target, source)
    return moves

total = hanoi(3, "A", "C", "B")
print(total, "moves")       # 7 moves
```

Each extra disk doubles the number of moves and adds one: n disks need 2 to the n minus 1. Sixty four disks, the legend's number, needs 18 quintillion moves.

### Nested data

A loop cannot easily handle lists inside lists inside lists, because you do not know how deep it goes. Recursion does not need to.

```python
def flatten(items):
    result = []
    for item in items:
        if isinstance(item, list):
            result.extend(flatten(item))
        else:
            result.append(item)
    return result

print(flatten([1, [2, [3, 4]], [5], 6]))     # [1, 2, 3, 4, 5, 6]
```

### Backtracking

**Backtracking** tries a choice, carries on, and if it reaches a dead end it undoes the choice and tries another. It is a recursive search, and the `path.pop()` below is the undo.

```python
maze = [
    "S.#.....",
    ".##.###.",
    "....#...",
    ".####.#.",
    "......#E",
]

def solve(row, col, path, seen):
    if not (0 <= row < len(maze) and 0 <= col < len(maze[0])):
        return False
    if maze[row][col] == "#" or (row, col) in seen:
        return False
    seen.add((row, col))
    path.append((row, col))
    if maze[row][col] == "E":
        return True
    for step_row, step_col in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        if solve(row + step_row, col + step_col, path, seen):
            return True
    path.pop()                  # dead end: undo this square and back up
    return False

path = []
seen = set()
if solve(0, 0, path, seen):
    grid = [list(line) for line in maze]
    for row, col in path[1:-1]:
        grid[row][col] = "*"
    for line in grid:
        print("".join(line))
    print("path of", len(path), "squares; tried", len(seen), "to find it")
```

The solver tries right, then down, then left, then up. At the start it goes right, finds a wall, and backs up. The gap between the two numbers printed is the squares it tried and had to abandon.

!exam State the base case, and say why it works :: Every recursion question awards a mark for the base case and a mark for showing that the recursive call gets closer to it. Say both, in words, before you write the code: "when n is 0 return 1, and each call reduces n by one".
"""),
    ],
    keyterms=[
        ("Recursion", "A technique in which a subprogram solves a problem by calling itself with a smaller version of the same problem."),
        ("Base case", "The case in a recursive subprogram that is answered directly, without another recursive call, and which stops the recursion."),
        ("Recursive case", "The case in a recursive subprogram that makes a call to itself, with an argument closer to the base case."),
        ("Call stack", "The area of memory that holds a stack frame for each active call, with its parameters, locals and return address."),
        ("Stack frame", "The block of the call stack belonging to one call of a subprogram."),
        ("Stack overflow", "An error when the call stack runs out of space, usually from recursion that never reaches its base case."),
        ("Memoisation", "Storing the result of each call so that a repeated call with the same argument is answered without recalculating."),
        ("Backtracking", "Trying a choice, and undoing it to try another if it leads to a dead end."),
        ("Divide and conquer", "Splitting a problem into smaller copies of itself, solving each and combining the results."),
    ],
    grade="""
Recursion is examined as tracing, writing and judging. The top marks come from precision about the stack.

+ Identify the base case and the recursive case separately, and say that each call moves towards the base case
+ When tracing, write the calls going down and then the values returning back up
+ Explain a stack overflow as the stack frames using up the available memory
+ In a comparison, give a cost and a benefit of each: memory and speed against clarity
+ Recognise when memoisation applies: the same arguments are being recalculated
""",
    mistakes=[
        "Writing a recursive case but no base case, or a base case that is never reached.",
        "Tracing only the way down and forgetting that nothing is returned until the base case is reached.",
        "Saying recursion is always slower, or always better, without a reason tied to the problem.",
        "Thinking each call shares the same local variables, when each has its own frame.",
        "Forgetting to return the result of the recursive call, so the function gives back None.",
    ],
    quiz=[
        Q("What two parts must every recursive subprogram have?",
          ["A base case, and a recursive case that moves closer to it", "A loop, and a counter",
           "A global variable, and a return statement", "A parameter, and a local variable"], 0,
          "Without the base case it never stops. Without progress towards it, it never reaches it."),
        Q("What happens when a recursive function has no reachable base case?",
          ["The call stack fills up and a stack overflow error occurs", "The function returns 0 once it gets bored",
           "The function becomes an infinite loop that uses no memory", "The program compiles faster"], 0,
          "Every call adds a stack frame and none ever returns, so the stack eventually runs out of space."),
        Q("What does `factorial(4)` return, given `factorial(n)` returns 1 for n <= 1, otherwise `n * factorial(n - 1)`?",
          ["24", "10", "4", "1"], 0,
          "4 * 3 * 2 * 1 = 24. The calls go down to factorial(1), which returns 1, and the answer is built on the way back up."),
        Q("Where does the computer store the parameters and return address of each call?",
          ["On the call stack, in a stack frame", "In the CPU registers only", "On the hard disk", "In the program counter"], 0,
          "Each call gets a stack frame, pushed when the call is made and popped when it returns."),
        Q("Which is a disadvantage of recursion compared with iteration?",
          ["Each call uses stack memory, so deep recursion can overflow the stack", "It can never solve the same problems as a loop",
           "It cannot be used with lists", "It makes code longer than a loop in every case"], 0,
          "Every pending call holds a frame. A loop uses a fixed amount of memory however many times it repeats."),
        Q("In `gcd(a, b)`, which returns `a` when `b == 0` and otherwise `gcd(b, a % b)`, what is the base case?",
          ["`b == 0`", "`a % b`", "`gcd(b, a % b)`", "`a == 0`"], 0,
          "The base case is the one that returns without calling the function again."),
        Q("Why is the naive recursive Fibonacci function slow for large n?",
          ["It recalculates the same values many times", "It uses too many global variables",
           "It cannot reach its base case", "It sorts the numbers first"], 0,
          "fib(4) and fib(5) both call fib(3), and so on down, so the number of calls roughly doubles with each step."),
        Q("What does memoisation do?",
          ["Stores earlier results so they are not recalculated", "Converts recursion into a loop automatically",
           "Removes the base case", "Increases the stack depth"], 0,
          "It trades memory for time: a repeated call with the same argument is answered from the stored result."),
        Q("How many moves does the Tower of Hanoi need for 4 disks?",
          ["15", "8", "16", "12"], 0,
          "n disks need 2 to the power n, minus 1 moves. For 4 disks that is 16 - 1 = 15."),
        Q("Which technique tries a path and undoes it if it reaches a dead end?",
          ["Backtracking", "Memoisation", "Iteration", "Hashing"], 0,
          "Backtracking is a recursive search where each failed choice is taken back before the next is tried."),
    ],
    exam=[
        EQ("State what is meant by the base case of a recursive subprogram, and explain why every recursive subprogram needs one.", 3, [
            MP("The base case is the case where the answer is returned without a further recursive call", ["without", "no further", "no more", "does not call", "stops", "direct", "returns"]),
            MP("Without a base case the subprogram would keep calling itself forever", ["forever", "never stop", "infinite", "endless", "keep calling"]),
            MP("This fills the call stack, causing a stack overflow", ["stack", "overflow", "memory", "crash", "run out"]),
        ], "The base case is the version of the problem that is small enough to be answered directly, so it returns a value without making another recursive call. Every recursive subprogram needs one because otherwise it would keep calling itself with no way to stop. Each call adds a stack frame, so the call stack would eventually be filled and the program would fail with a stack overflow.",
           command="State"),
        EQ("The subprogram shown is called with mystery(4). Show the sequence of calls, and the values that are returned, and state the value that is output.", 4, [
            MP("Identifies that mystery(0) is the base case and returns 0", ["base case", "n == 0", "0 returns", "returns 0", "mystery(0)"]),
            MP("Shows the chain of calls from mystery(4) down to mystery(0)", ["mystery(3)", "mystery(2)", "mystery(1)", "4 + mystery", "chain"]),
            MP("Shows the returns unwinding, 0, 1, 3, 6, 10", ["1, 3, 6", "0, 1, 3", "1 3 6", "unwind", "6", "3"]),
            MP("States that the output is 10", ["10"]),
        ], "mystery(4) calls mystery(3), which calls mystery(2), then mystery(1), then mystery(0). mystery(0) is the base case and returns 0. The calls then return: mystery(1) returns 1 + 0 = 1, mystery(2) returns 2 + 1 = 3, mystery(3) returns 3 + 3 = 6 and mystery(4) returns 4 + 6 = 10. The value output is 10, which is the sum of the numbers from 1 to 4.",
           command="Show",
           figure="""```python
def mystery(n):
    if n == 0:
        return 0
    return n + mystery(n - 1)

print(mystery(4))
```"""),
        EQ("Write a recursive function called power that takes a number, base, and a whole number, exponent, that is 0 or more, and returns base raised to the power exponent. You must not use the ** operator or a loop.", 4, [
            MP("Defines a function with the two parameters", ["def power", "def", "base", "exponent"]),
            MP("Has a base case: when exponent is 0 the result is 1", ["exponent == 0", "== 0", "return 1", "base case"]),
            MP("Has a recursive case that multiplies base by power of exponent - 1", ["base * power", "power(base", "exponent - 1", "- 1"]),
            MP("Returns the result of the recursive case", ["return base", "return"]),
        ], r"""```python
def power(base, exponent):
    if exponent == 0:
        return 1
    return base * power(base, exponent - 1)

print(power(2, 10))
```

When the exponent is 0 the answer is 1, which is the base case. Otherwise the function multiplies base by base to the power one less, so each call moves the exponent closer to 0. power(2, 10) returns 1024.""",
           command="Write"),
        EQ("Explain what a stack overflow is, and how it can happen in a program that uses recursion.", 3, [
            MP("Each call to a subprogram adds a stack frame to the call stack", ["stack frame", "frame", "added", "pushed", "each call"]),
            MP("The call stack has a limited size", ["limited", "finite", "fixed", "full", "run out", "capacity"]),
            MP("A recursive subprogram with no reachable base case, or too deep a recursion, uses up all of it", ["no base case", "never reaches", "too many", "too deep", "does not stop", "never stops", "infinite"]),
        ], "Each time a subprogram is called, a stack frame holding its parameters, local variables and return address is added to the call stack, and it is only removed when the call returns. The call stack has a limited size. If a recursive subprogram never reaches its base case, or the recursion is simply too deep, the frames use up all the space available and the program fails with a stack overflow.",
           command="Explain"),
        EQ("A programmer must write a subprogram to total the numbers in a list. Discuss whether the programmer should use recursion or iteration.", 6, [
            MP("Iteration uses a fixed amount of memory however long the list is", ["fixed", "constant", "less memory", "no stack", "memory"]),
            MP("Recursion adds a stack frame for every item, so a long list could cause a stack overflow", ["stack frame", "stack overflow", "every item", "long list", "too deep", "each call"]),
            MP("A loop is quicker because there is no overhead of calling a subprogram repeatedly", ["quicker", "faster", "overhead", "speed", "calling"]),
            MP("A loop is simple and easy to trace and debug for this problem", ["simple", "easy", "trace", "debug", "straightforward", "readable"]),
            MP("Recursion could be shorter for a nested or tree shaped list", ["nested", "tree", "shorter", "elegant", "natural", "self similar"]),
            MP("A reasoned conclusion: iteration is the better choice for a flat list", ["conclusion", "better choice", "should use iteration", "iteration is better", "therefore", "overall", "i would"]),
        ], "For a simple list of numbers iteration is the better choice. A loop uses a fixed amount of memory, whereas a recursive solution adds a stack frame for each item, so a very long list could fill the call stack and cause a stack overflow. A loop is also quicker, because it avoids the overhead of making a subprogram call for every item, and it is simple to trace and debug. Recursion has the advantage of being shorter and closer to the definition of the problem, which would make it a better choice if the list were nested to unknown depth or tree shaped. Since the list here is flat, the programmer should use iteration.",
           command="Discuss"),
    ],
)
