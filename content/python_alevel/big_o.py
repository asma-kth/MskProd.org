"""A Level Python: algorithm complexity and Big-O notation."""
from mskbuild.models import Topic, Section, Q, EQ, MP

INPUTS = {}
EXPECT = {}

TOPIC = Topic(
    slug="big-o-and-complexity",
    title="Big-O and Algorithm Complexity",
    spec="A Level 8",
    icon="i-gauge",
    minutes=50,
    blurb="How to measure the cost of an algorithm without a stopwatch: counting steps, the growth classes from constant to factorial, reading the class straight from code, space complexity, and why some problems cannot be brute forced.",
    fact="Doubling a computer's speed lets an exponential algorithm handle exactly one more item. Nothing about faster hardware rescues it, which is why a cleverer algorithm is worth more than any amount of waiting for faster processors.",
    sections=[
        Section("Counting steps, not seconds", r"""
How long a program takes depends on the computer, the language, what else is running, and the input. None of that tells you whether the **algorithm** is any good. **Complexity** measures it directly: how the number of basic steps grows as the **size of the input**, *n*, grows.

**Big-O notation** writes down that growth, using two simplifications:

1. **Drop constant factors.** Doing 3 steps per item or 5 steps per item is the same *shape* of growth.
2. **Keep only the fastest growing term.** For large *n* the biggest term swamps the rest.

So an algorithm that takes 3n² + 5n + 2 steps is **O(n²)**, said "order n squared". Big-O describes an **upper bound**, and unless it says otherwise, for the **worst case**.

### The growth classes

| Class | Name | Example | Doubling n |
| O(1) | Constant | Reading `items[5]`, a dictionary lookup | No change |
| O(log n) | Logarithmic | Binary search | One extra step |
| O(n) | Linear | Linear search, one loop through the data | Twice as long |
| O(n log n) | Linearithmic | Merge sort, quick sort on average | A little over twice |
| O(n²) | Quadratic | Bubble sort, a loop inside a loop | Four times as long |
| O(2ⁿ) | Exponential | Naive recursive Fibonacci, trying every subset | The square of the time |
| O(n!) | Factorial | Trying every ordering, as in a brute force salesman | Unimaginable |

Rather than quote this table, count it. Each function below does one thing in a way that gives the growth in its name, and returns the number of steps it took.

```python
def constant(n):
    return 1

def logarithmic(n):
    steps = 0
    while n > 1:
        n = n // 2
        steps += 1
    return steps

def linear(n):
    steps = 0
    for i in range(n):
        steps += 1
    return steps

def linearithmic(n):
    steps = 0
    for level in range(logarithmic(n)):
        for i in range(n):
            steps += 1
    return steps

def quadratic(n):
    steps = 0
    for i in range(n):
        for j in range(n):
            steps += 1
    return steps

def exponential(n):
    if n == 0:
        return 1
    return exponential(n - 1) + exponential(n - 1)

def row(*values):
    print("".join(str(v).ljust(11) for v in values))

row("n", "O(1)", "O(log n)", "O(n)", "O(n log n)", "O(n sq.)", "O(2 to n)")
for n in [4, 8, 12, 16]:
    row(n, constant(n), logarithmic(n), linear(n), linearithmic(n), quadratic(n), exponential(n))
```

Read down the last column. By *n* = 16 the exponential algorithm has taken 65 536 steps, where the linear one took 16. Add four more to *n* and it is a million.

!diagram py-growth-curves

### Where the big ones come from

| Pattern in the code | Complexity |
| A statement that runs once | O(1) |
| A loop over the n items | O(n) |
| A loop that halves (or doubles) the problem each time | O(log n) |
| A loop inside a loop, both over n | O(n²) |
| A loop over n items, each step doing an O(log n) job | O(n log n) |
| A recursive function that calls itself twice on a problem one smaller | O(2ⁿ) |
| A recursive function that halves the problem and does n work to combine | O(n log n) |
"""),
        Section("Reading complexity from code", r"""
In the exam you are given code, or a description, and you state its complexity. The method is to find the part that repeats, and ask how many times it repeats for an input of size *n*.

```python
def first_item(items):                 # O(1)
    return items[0]

def total(items):                      # O(n): one pass
    result = 0
    for item in items:
        result += item
    return result

def has_duplicate(items):              # O(n squared): compares every pair
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            if items[i] == items[j]:
                return True
    return False

def has_duplicate_fast(items):         # O(n): a set remembers what has been seen
    seen = set()
    for item in items:
        if item in seen:
            return True
        seen.add(item)
    return False

data = [3, 8, 1, 9, 4, 8]
print(first_item(data), total(data), has_duplicate(data), has_duplicate_fast(data))
```

Both duplicate checkers give the same answer. The first compares every pair, so for a million items it makes about 500 billion comparisons. The second looks at each item once, relying on the set's constant time membership test, so it makes a million. Same task, completely different cost, and the only difference is the **data structure**.

### Best, average and worst case

The same algorithm can behave differently on different inputs of the same size.

| Algorithm | Best case | Worst case |
| Linear search | O(1): the item is first | O(n): last or missing |
| Binary search | O(1): the item is in the middle | O(log n) |
| Bubble sort with a swapped flag | O(n): already sorted, one pass | O(n²): reversed |
| Quick sort | O(n log n) | O(n²): bad pivots, such as an already sorted list |
| Merge sort | O(n log n) | O(n log n) |

!exam The worst case is the default :: When the question just says "state the time complexity of" an algorithm, give the worst case, and write it as O( ). If it asks for the best case, or the average, it will say so.

### Space complexity

**Space complexity** is how the **memory** an algorithm needs grows with *n*, apart from the input itself. A time saving is often paid for in space, and the exam asks you to say which.

| Algorithm | Extra space | Why |
| Bubble sort, insertion sort | O(1) | Swaps items in the same list |
| Merge sort | O(n) | Builds new lists as it merges |
| Recursive factorial | O(n) | One stack frame for each pending call |
| Iterative factorial | O(1) | One variable |
| Memoised Fibonacci | O(n) | Stores every result, to save time |

### Python's own operations

The built in types have costs too, and the wrong choice is a common cause of slow programs.

| Operation | Cost |
| `items.append(x)` | O(1) |
| `items.insert(0, x)` | O(n): everything after shifts |
| `x in items` for a list | O(n) |
| `x in some_set`, `key in some_dict` | O(1) on average |
| `sorted(items)` | O(n log n) |
| `len(items)` | O(1) |
"""),
        Section("Measuring, and the problems that cannot be solved by trying everything", r"""
### A stopwatch confirms it

Timing a program is no substitute for analysis, because the result varies from run to run and machine to machine. It can confirm the difference between two growth classes when it is large:

```python
import time

def linear_search(items, target):
    for i in range(len(items)):
        if items[i] == target:
            return i
    return -1

def binary_search(items, target):
    low = 0
    high = len(items) - 1
    while low <= high:
        mid = (low + high) // 2
        if items[mid] == target:
            return mid
        elif items[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1

data = list(range(200000))

start = time.perf_counter()
linear_search(data, 199999)
linear_time = time.perf_counter() - start

start = time.perf_counter()
binary_search(data, 199999)
binary_time = time.perf_counter() - start

print(linear_time > binary_time, linear_time > 50 * binary_time)
```

Rather than print the times themselves, which are different on every machine, the program asks two yes or no questions: is linear search slower, and is it **more than fifty times** slower? The answer is True to both, and the gap grows with the data.

### Tractable and intractable problems

A problem is **tractable** if there is an algorithm that solves it in **polynomial time**, such as O(n) or O(n²) or O(n³): the cost grows quickly but stays manageable. It is **intractable** if the only known algorithms are **exponential** or worse: for any but small inputs they cannot finish in a useful time, however fast the computer.

The classic example is the **travelling salesman problem**: find the shortest route that visits every one of *n* cities once and returns. Checking every route is the obvious algorithm, and for *n* cities there are (n - 1)! divided by 2 different routes.

```python
import math

def readable(seconds):
    for name, size in [("years", 31_557_600), ("days", 86_400), ("hours", 3_600), ("minutes", 60)]:
        if seconds >= size:
            amount = seconds / size
            if amount > 1000:
                return format(round(amount, -3), ",.0f") + " " + name
            return format(amount, ",.3g") + " " + name
    return "under a minute"

for cities in [5, 10, 15, 20, 25]:
    routes = math.factorial(cities - 1) // 2
    print(cities, "cities:", format(routes, ","), "routes, at a billion a second:", readable(routes / 1_000_000_000))
```

Going from 20 cities to 25 takes the time from about two years to about ten million years. A computer a thousand times faster would not help.

When a problem is intractable, programmers use a **heuristic**: a method that finds a good answer, not necessarily the best, in reasonable time. For the salesman, "always go to the nearest city not yet visited" is fast, and is usually within a quarter of the best route. `A*` search, which you have already met, is another way of using a heuristic to avoid exploring everything.

### Why this matters for design

A better algorithm beats a better computer. Moving from O(n²) to O(n log n) on a million items is a gain of about fifty thousand times. At the historic rate of hardware doubling every two years, that is about thirty years of progress, gained from one rewrite.
"""),
    ],
    keyterms=[
        ("Complexity", "A measure of how the resources an algorithm needs, time or memory, grow as the size of its input grows."),
        ("Big-O notation", "A way of describing the upper bound on the growth of an algorithm's cost, ignoring constants and lower order terms."),
        ("Time complexity", "How the number of steps an algorithm takes grows as the size of the input grows."),
        ("Space complexity", "How the amount of memory an algorithm needs grows as the size of the input grows."),
        ("Constant time", "A cost that does not depend on the size of the input, written O(1)."),
        ("Logarithmic time", "A cost that grows by a fixed amount each time the input doubles, written O(log n), as in binary search."),
        ("Polynomial time", "A cost that grows as a power of n, such as n or n squared, which is considered tractable."),
        ("Exponential time", "A cost that multiplies each time n increases by one, such as 2 to the power n, which is considered intractable."),
        ("Tractable", "Describes a problem that can be solved in polynomial time or better."),
        ("Intractable", "Describes a problem for which the only known algorithms take exponential time or worse, so only small cases can be solved."),
        ("Heuristic", "A method that finds a good, not necessarily optimal, answer quickly, used when finding the best answer is intractable."),
    ],
    grade="""
Complexity questions are about shape, so show your reasoning rather than just the label.

+ State the complexity in the form O( ) and say which case it is, usually the worst case
+ Justify it from the code: name the loop, say how many times it runs, and what is inside it
+ Drop constants and lower terms, and say that you have done so
+ When comparing algorithms, give a time cost and a space cost for each, and choose with a reason
+ Describe an intractable problem by its exponential cost, and name the heuristic as the way round it
""",
    mistakes=[
        "Writing O(2n) or O(n + 5), when constants and lower terms are dropped: O(n).",
        "Giving the best case when the question means the usual one, the worst case.",
        "Saying a nested loop is always O(n squared), when the inner loop may run a fixed number of times.",
        "Confusing time and space complexity, or forgetting the stack space used by recursion.",
        "Claiming a faster computer solves an exponential problem, when it adds only one more item.",
    ],
    quiz=[
        Q("What does Big-O notation describe?",
          ["How the cost of an algorithm grows as the size of the input grows", "The exact time an algorithm takes in seconds",
           "The number of lines of code in an algorithm", "The amount of memory a computer has available"], 0,
          "It is about the shape of the growth, which is why constants and the speed of the computer do not matter."),
        Q("What is the time complexity of reading `items[5]` from a list?",
          ["O(1)", "O(n)", "O(log n)", "O(n squared)"], 0,
          "A list reaches any position directly, so the cost does not depend on the length of the list."),
        Q("What is the worst case time complexity of a binary search?",
          ["O(log n)", "O(n)", "O(1)", "O(n log n)"], 0,
          "Every comparison halves the data that is left, so doubling the list adds only one more comparison."),
        Q("A function has one loop that runs n times, and inside it another loop that runs n times. What is its complexity?",
          ["O(n squared)", "O(n)", "O(2n)", "O(log n)"], 0,
          "The inner loop runs in full for each pass of the outer loop, so n times n steps are taken."),
        Q("What is the complexity of an algorithm that takes 5n + 20 steps?",
          ["O(n)", "O(5n)", "O(n + 20)", "O(20)"], 0,
          "Constants and lower order terms are dropped, because for large n the term in n dominates."),
        Q("Which of these growth rates is the worst for a large input?",
          ["O(2 to the power n)", "O(n squared)", "O(n log n)", "O(n)"], 0,
          "An exponential cost multiplies with every extra item, so it becomes impossible for even quite small n."),
        Q("What is the average time complexity of merge sort?",
          ["O(n log n)", "O(n)", "O(n squared)", "O(log n)"], 0,
          "It halves the list log n times and does n work at each level to merge."),
        Q("If an O(n) algorithm takes 2 seconds for an input of size n, roughly how long does it take for 2n?",
          ["4 seconds", "2 seconds", "8 seconds", "16 seconds"], 0,
          "Linear growth means doubling the input doubles the time."),
        Q("What does space complexity measure?",
          ["How the amount of memory needed grows as the size of the input grows",
           "How many steps the algorithm takes as the size of the input grows",
           "The amount of space that the program's code takes up when it is stored on a disk",
           "How many variables have been given names in the source code of the program"], 0,
          "A recursive function that goes n deep, for example, needs O(n) space for its stack frames."),
        Q("What is an intractable problem?",
          ["One where the only known algorithms take exponential time, so only small cases can be solved",
           "One that no algorithm can ever solve", "One that is solved in polynomial time but takes a long time to code",
           "One that needs more than one programmer"], 0,
          "An intractable problem can be solved in principle, but not in a practical time for any but small inputs."),
    ],
    exam=[
        EQ("State what is meant by Big-O notation.", 2, [
            MP("It describes how the time or memory an algorithm needs grows as the size of the input grows", ["grows", "growth", "increases", "scale", "size of the input"]),
            MP("It ignores constants and gives an upper bound, usually the worst case", ["upper bound", "worst case", "ignores constants", "constants", "lower terms", "dominant"]),
        ], "Big-O notation describes how the time, or the memory, that an algorithm needs grows as the size of its input grows. It ignores constant factors and smaller terms and gives an upper bound, which is usually the worst case.",
           command="State"),
        EQ("State the time complexity, using Big-O notation, of each of the following. (a) Reading an item from an array when its index is known. (b) A linear search of a list of n items. (c) A binary search of a sorted list of n items. (d) A bubble sort of n items, in the worst case.", 4, [
            MP("(a) O(1)", ["o(1)", "constant"]),
            MP("(b) O(n)", ["o(n)", "linear"]),
            MP("(c) O(log n)", ["o(log n)", "logarithmic", "log n", "log2 n"]),
            MP("(d) O(n squared)", ["o(n squared)", "n squared", "n^2", "n2", "quadratic", "n²", "o(n²)"]),
        ], "(a) O(1), constant time, because the position is calculated directly. (b) O(n), linear, because in the worst case every item is checked. (c) O(log n), logarithmic, because each comparison halves the items that remain. (d) O(n squared), quadratic, because there is a pass of up to n comparisons for each of up to n passes.",
           command="State"),
        EQ("The subprogram shown is called with a list of n items. State its time complexity, and explain how you decided.", 4, [
            MP("The time complexity is O(n squared)", ["o(n squared)", "n squared", "n^2", "n2", "quadratic", "n²", "o(n²)"]),
            MP("There is a loop inside another loop", ["nested", "loop inside", "two loops", "inner loop", "outer loop"]),
            MP("Both loops go through all n items", ["both", "n items", "each loop", "n times", "each runs n"]),
            MP("So the inner loop runs n times for each of the n passes of the outer loop, a total of n times n steps", ["n times n", "n * n", "n x n", "for each", "every pass", "multiplied"]),
        ], "The time complexity is O(n squared). The subprogram contains one loop nested inside another, and both loops go through all n items. The inner loop runs n times for each of the n passes of the outer loop, so the total number of steps is n times n. This means that doubling the length of the list would make it take about four times as long.",
           command="State",
           figure="""```python
def mystery(items):
    count = 0
    for a in items:
        for b in items:
            if a == b:
                count += 1
    return count
```"""),
        EQ("Explain what is meant by an intractable problem, and describe one way in which programmers deal with such problems.", 4, [
            MP("A problem for which the only known algorithms take exponential time, or worse", ["exponential", "factorial", "not polynomial", "very quickly", "grows"]),
            MP("The time needed grows so quickly that only small inputs can be solved in a reasonable time", ["small inputs", "reasonable time", "practical", "too long", "not realistic", "years"]),
            MP("A heuristic can be used instead", ["heuristic", "approximation", "rule of thumb", "approximate"]),
            MP("It finds a good, but not necessarily the best, solution in a reasonable time", ["good", "not necessarily the best", "not necessarily optimal", "reasonable", "quickly", "close"]),
        ], "An intractable problem is one for which the only known algorithms take exponential time or worse, so the time needed grows so quickly with the size of the input that only small cases can be solved in a reasonable time, however fast the computer. A programmer can use a heuristic instead, which is a rule of thumb that finds a good solution, though not necessarily the best one, in a reasonable time. For the travelling salesman problem, always travelling to the nearest unvisited city is an example.",
           command="Explain"),
        EQ("Two subprograms check whether a list of n items contains a duplicate. The first compares every pair of items. The second adds each item to a set as it goes, and stops if an item is already in the set. Compare the two subprograms in terms of time and space complexity.", 6, [
            MP("The first compares every pair, so takes O(n squared) time", ["o(n squared)", "n squared", "quadratic", "every pair", "n²"]),
            MP("The second looks at each item once, so takes O(n) time", ["o(n)", "linear", "once", "each item once", "one pass"]),
            MP("Checking whether an item is in a set takes constant time on average, which is what makes the second one fast", ["constant", "o(1)", "hash", "set lookup", "average"]),
            MP("The first needs almost no extra memory, O(1) space", ["o(1)", "no extra", "little extra", "constant space", "no additional"]),
            MP("The second needs a set that could hold every item, O(n) space", ["o(n)", "stores every", "extra memory", "set holds", "up to n"]),
            MP("A conclusion: the second is better for a long list because the time saved outweighs the memory, though the first could suit a very small or a memory limited device", ["conclusion", "better", "outweighs", "trade off", "tradeoff", "memory limited", "long list", "overall"]),
        ], "The first subprogram compares every pair of items, so it takes O(n squared) time, but it needs almost no extra memory, O(1) space. The second looks at each item once, so it takes O(n) time, because checking whether an item is in a set takes constant time on average. However, the set may end up holding every item, so it needs O(n) space. The second is the better choice for a long list, because the saving in time is enormous and outweighs the cost in memory. The first could still suit a very short list, or a device with very little memory, where the extra memory is the greater concern.",
           command="Compare"),
    ],
)
