"""A Level Python: greedy algorithms and dynamic programming."""
from mskbuild.models import Topic, Section, Q, EQ, MP

INPUTS = {}
EXPECT = {}

TOPIC = Topic(
    slug="dynamic-programming-and-greedy",
    title="Dynamic Programming and Greedy Algorithms",
    spec="A Level 15",
    icon="i-route",
    minutes=55,
    blurb="Two ways of solving optimisation problems: the greedy algorithm that grabs the best choice now, and dynamic programming that remembers sub-answers. Coin change, the knapsack problem, edit distance and the travelling salesperson, each with runnable code and a table to read.",
    fact="Richard Bellman invented dynamic programming in the 1950s while working for a government research organisation. He picked the word 'dynamic' partly because it sounded impressive and could not be used in a negative way, which helped when he needed funding for mathematics.",
    sections=[
        Section("Greedy algorithms", r"""
An **optimisation problem** asks for the *best* answer: the fewest coins, the shortest route, the highest value. A **greedy algorithm** builds the answer one step at a time and always takes the **best looking choice right now**, never going back to reconsider it.

### Giving change

To give 68p in change, take the biggest coin that still fits, and repeat.

```python
def greedy_change(amount, coins):
    given = []
    for coin in sorted(coins, reverse=True):
        while amount >= coin:
            given.append(coin)
            amount = amount - coin
    return given

uk = [1, 2, 5, 10, 20, 50]
print(greedy_change(68, uk))
print(len(greedy_change(68, uk)), "coins")
```

For British coins that gives the fewest coins every time. But greedy is only as good as the problem allows. Suppose a country has coins worth 1, 3 and 4, and you must give 6:

```python
def greedy_change(amount, coins):
    given = []
    for coin in sorted(coins, reverse=True):
        while amount >= coin:
            given.append(coin)
            amount = amount - coin
    return given

print(greedy_change(6, [1, 3, 4]))     # 4 + 1 + 1
print("but 3 + 3 uses only two coins")
```

Greedy took the 4 because it looked best, and then it was stuck with two 1s. It never went back.

!warn Fast does not mean correct :: A greedy algorithm is quick and simple, but it is only guaranteed to give the best answer for problems where taking the best local choice is provably safe. Otherwise it is a **heuristic**: a sensible shortcut that usually gives a good answer.

### A greedy algorithm that is correct: choosing meetings

A room can host one meeting at a time. Given the start and end of every request, how can you fit in the **most** meetings? Taking the shortest meeting first fails. Taking the earliest start fails. The rule that works is to **always take the meeting that finishes earliest**, because it leaves the most room for the rest.

```python
meetings = [("maths", 9, 11), ("art", 9, 10), ("history", 10, 12), ("science", 11, 13),
            ("music", 12, 14), ("drama", 13, 15)]

def most_meetings(meetings):
    chosen, free_from = [], 0
    for name, start, end in sorted(meetings, key=lambda m: m[2]):
        if start >= free_from:
            chosen.append(name)
            free_from = end
    return chosen

print(most_meetings(meetings))
```

### Where greedy shows up

You have already met greedy algorithms. **Dijkstra's** algorithm always settles the closest unvisited vertex. **Kruskal's** and **Prim's** take the cheapest edge that is safe. **Huffman coding**, in the compression topic, always merges the two rarest symbols. In each, the greedy choice has been *proved* to be safe.
"""),
        Section("Dynamic programming", r"""
**Dynamic programming** (DP) solves a big problem by solving its smaller pieces first and **remembering** the answers, so no piece is ever solved twice. It applies when a problem has two features:

- **Overlapping subproblems.** The same smaller problem comes up again and again. (You saw this with `fib(3)` inside both `fib(4)` and `fib(5)`.)
- **Optimal substructure.** The best answer to the big problem is built from the best answers to smaller ones.

### The fewest coins, properly

Let `best[a]` be the fewest coins that make amount `a`. To make `a`, the last coin must be one of the coins, say `c`. Then what is left is `a - c`, and its best answer is already in the table. Try every coin and keep the smallest:

`best[a] = 1 + min(best[a - c])` for every coin `c` with `c <= a`

```python
def fewest_coins(amount, coins):
    best = [0] + [None] * amount
    for a in range(1, amount + 1):
        options = [best[a - c] + 1 for c in coins if c <= a and best[a - c] is not None]
        best[a] = min(options) if options else None
    return best

table = fewest_coins(10, [1, 3, 4])
for a, n in enumerate(table):
    print("amount", a, "needs", n, "coins")
```

This **bottom-up** method fills a table from the smallest amount upwards. Every entry takes only a few steps because the entries it needs are already there. It costs O(amount x number of coins), and it gets 6p right: two coins.

### Top-down: recursion with memoisation

The same idea can be written as a recursive function with a cache, which is exactly the **memoisation** from the recursion topic. This is **top-down**: start from the question and only work out the sub-answers that are actually needed.

```python
from functools import lru_cache

calls = 0

@lru_cache(maxsize=None)
def fewest(amount):
    global calls
    calls += 1
    if amount == 0:
        return 0
    options = [fewest(amount - c) + 1 for c in (1, 3, 4) if c <= amount]
    return min(options)

print(fewest(40), "coins for 40p, using", calls, "calls")
```

Without the cache, `fewest(40)` would make over 300 million calls. With it, each of the 41 amounts is worked out once.

| | Top-down (memoisation) | Bottom-up (tabulation) |
| Written as | Recursion plus a cache | Loops filling a table |
| Works out | Only the sub-answers needed | Every sub-answer |
| Risk | Deep recursion can overflow the stack | None |

### Counting the ways

Dynamic programming can also *count*. How many different ways are there to make 10p from 1p, 2p and 5p coins? Let `ways[a]` be the number of ways to make `a`. Add the coins one kind at a time:

```python
def count_ways(amount, coins):
    ways = [1] + [0] * amount          # one way to make 0: use nothing
    for coin in coins:
        for a in range(coin, amount + 1):
            ways[a] += ways[a - coin]
    return ways[amount]

print(count_ways(10, [1, 2, 5]))
print(count_ways(100, [1, 2, 5, 10, 20, 50]))
```
"""),
        Section("The knapsack problem", r"""
A hiker's bag can carry 50 kg. Each item has a weight and a value. Which items should go in to make the **total value as high as possible** without going over the weight limit? Each item is taken whole or left behind. This is the **0/1 knapsack problem**, and a version of it hides inside loading lorries, choosing investments and cutting stock.

### Greedy fails here

An obvious rule is to take the items with the best value for their weight first.

```python
items = [("tent", 10, 60), ("stove", 20, 100), ("food", 30, 120)]    # name, kg, value
limit = 50

def greedy_by_ratio(items, limit):
    taken, weight, value = [], 0, 0
    for name, kg, worth in sorted(items, key=lambda i: i[2] / i[1], reverse=True):
        if weight + kg <= limit:
            taken.append(name)
            weight += kg
            value += worth
    return taken, value

print(greedy_by_ratio(items, limit))
print("but stove and food together are worth", 100 + 120, "and weigh", 20 + 30)
```

### The dynamic programming table

Let `table[i][w]` be the best value using only the first `i` items with a bag that holds `w`. For item `i` there are two choices: **leave it** (the answer is the row above) or **take it** (its value, plus the best for the space that remains).

```python
items = [("tent", 10, 60), ("stove", 20, 100), ("food", 30, 120)]
limit = 50

def knapsack(items, limit):
    table = [[0] * (limit + 1) for _ in range(len(items) + 1)]
    for i, (name, kg, worth) in enumerate(items, start=1):
        for w in range(limit + 1):
            table[i][w] = table[i - 1][w]                         # leave it
            if kg <= w:
                table[i][w] = max(table[i][w], table[i - 1][w - kg] + worth)   # take it
    # walk back up the table to see which items were taken
    taken, w = [], limit
    for i in range(len(items), 0, -1):
        if table[i][w] != table[i - 1][w]:
            name, kg, worth = items[i - 1]
            taken.append(name)
            w = w - kg
    return table[len(items)][limit], taken

print(knapsack(items, limit))
```

The table is filled once, row by row, so the cost is **O(n x W)** for n items and a limit of W. Compare it with trying every combination:

```python
limit = 60

for n in (10, 20, 30, 40):
    print(n, "items: brute force", 2 ** n, "subsets, table", n * limit, "cells")
```

!key The trade :: Brute force checks all 2^n subsets, which doubles with every extra item. Dynamic programming turns that into a table of n x W cells, at the price of memory for the table. It is fast when W is a modest number, which is the usual case.
"""),
        Section("Strings: common subsequences and edit distance", r"""
Dynamic programming is at its best when comparing two sequences.

### Longest common subsequence

A **subsequence** keeps letters in order but may skip some. The longest common subsequence (LCS) of `AGGTAB` and `GXTXAYB` is `GTAB`, four letters. Tools that compare two versions of a file, such as `git diff`, are built on this idea.

Let `t[i][j]` be the LCS length of the first `i` letters of one word and the first `j` of the other. If the next two letters match, extend the diagonal. If not, take the better of dropping a letter from either word.

```python
def lcs(a, b):
    t = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            if a[i - 1] == b[j - 1]:
                t[i][j] = t[i - 1][j - 1] + 1
            else:
                t[i][j] = max(t[i - 1][j], t[i][j - 1])
    # read the answer back out
    i, j, letters = len(a), len(b), []
    while i > 0 and j > 0:
        if a[i - 1] == b[j - 1]:
            letters.append(a[i - 1])
            i, j = i - 1, j - 1
        elif t[i - 1][j] >= t[i][j - 1]:
            i -= 1
        else:
            j -= 1
    return "".join(reversed(letters))

print(lcs("AGGTAB", "GXTXAYB"))
```

### Edit distance

How different are two words? The **edit distance** (Levenshtein distance) is the fewest single letter **insertions, deletions and substitutions** that turn one into the other. `kitten` becomes `sitting` in three: k to s, e to i, and add g.

```python
def edit_distance(a, b):
    d = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(len(a) + 1):
        d[i][0] = i                       # delete every letter
    for j in range(len(b) + 1):
        d[0][j] = j                       # insert every letter
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            same = 0 if a[i - 1] == b[j - 1] else 1
            d[i][j] = min(d[i - 1][j] + 1,           # delete
                          d[i][j - 1] + 1,           # insert
                          d[i - 1][j - 1] + same)    # substitute, or keep if equal
    return d[len(a)][len(b)]

print(edit_distance("kitten", "sitting"))
print(edit_distance("python", "pyhton"))
```

A spell checker uses it to offer "did you mean": measure the distance from what was typed to every dictionary word and offer the closest.

```python
def edit_distance(a, b):
    d = [[0] * (len(b) + 1) for _ in range(len(a) + 1)]
    for i in range(len(a) + 1):
        d[i][0] = i
    for j in range(len(b) + 1):
        d[0][j] = j
    for i in range(1, len(a) + 1):
        for j in range(1, len(b) + 1):
            same = 0 if a[i - 1] == b[j - 1] else 1
            d[i][j] = min(d[i - 1][j] + 1, d[i][j - 1] + 1, d[i - 1][j - 1] + same)
    return d[len(a)][len(b)]

dictionary = ["algorithm", "logarithm", "rhythm", "alright", "arithmetic"]

def did_you_mean(word):
    return min(dictionary, key=lambda w: (edit_distance(word, w), w))

for typed in ["algoritm", "arithmatic", "rythm"]:
    print(typed, "->", did_you_mean(typed))
```
"""),
        Section("Choosing a strategy", r"""
There is no single best way to solve a problem. The question to ask is *what kind of problem is it?*

| Strategy | Idea | Works when | Examples |
| **Brute force** | Try every possibility | The problem is small | Cracking a short PIN |
| **Greedy** | Take the best choice now | The local best is provably safe | Dijkstra, Kruskal, Huffman, choosing meetings |
| **Divide and conquer** | Split into independent halves, solve each, combine | The pieces do not overlap | Merge sort, binary search, quick sort |
| **Dynamic programming** | Solve small pieces once and reuse them | The pieces overlap | Knapsack, edit distance, shortest paths |
| **Heuristic** | A good enough shortcut with no guarantee | The exact answer is out of reach | Route planning for delivery vans |

Divide and conquer and dynamic programming look alike. The difference: merge sort splits a list into halves that never share anything, so there is nothing to remember. Fibonacci splits into pieces that overlap heavily, so remembering them is the whole point.

### When even a table is not enough: the travelling salesperson

A delivery driver must visit every one of n towns and return home by the shortest route. The only known way that always finds the *best* route is, in effect, to check them all, and there are (n - 1)! routes.

```python
import math

for n in (5, 8, 10, 15, 20, 25):
    print(n, "towns:", math.factorial(n - 1), "routes")
```

At 20 towns that is over a hundred quadrillion routes. No computer can check them in a lifetime, so real systems use a **heuristic**. The simplest is *nearest neighbour*: always drive to the closest town not yet visited. It is greedy, it is fast, and it is not always good.

```python
import itertools
import math

towns = {"A": (0, 0), "B": (1, 5), "C": (4, 1), "D": (5, 6), "E": (8, 2), "F": (9, 7), "G": (3, 8)}

def length(route):
    pairs = zip(route, route[1:] + route[:1])
    return sum(math.dist(towns[a], towns[b]) for a, b in pairs)

def nearest_neighbour(start):
    route = [start]
    left = set(towns) - {start}
    while left:
        here = towns[route[-1]]
        route.append(min(left, key=lambda t: math.dist(here, towns[t])))
        left.remove(route[-1])
    return route

best = min((["A"] + list(p) for p in itertools.permutations(sorted(set(towns) - {"A"}))), key=length)
quick = nearest_neighbour("A")
print("best route    ", best, round(length(best), 1))
print("nearest first ", quick, round(length(quick), 1))
```

The shortcut found a route about a third longer than the best one. For a few towns you can afford to be exact. For hundreds you accept a good answer. Knowing which situation you are in, and being able to explain the trade, is the skill the examiner is looking for.

!exam Name the strategy and justify it :: Questions on algorithm choice reward a named strategy and a reason tied to the problem: 'dynamic programming, because the same sub-problems are needed repeatedly', or 'a heuristic, because checking every route is not feasible for this many towns'.
"""),
    ],
    keyterms=[
        ("Optimisation problem", "A problem that asks for the best answer by some measure, such as the shortest, cheapest or highest value."),
        ("Greedy algorithm", "An algorithm that makes the best looking choice at each step and never reconsiders it."),
        ("Heuristic", "A practical shortcut that finds a good answer quickly but does not guarantee the best one."),
        ("Dynamic programming", "Solving a problem by solving its overlapping smaller problems once each and storing the answers."),
        ("Overlapping subproblems", "A property of a problem where the same smaller problem has to be solved many times."),
        ("Optimal substructure", "A property where the best answer to a problem is built from the best answers to smaller versions of it."),
        ("Memoisation (top-down)", "Recursion that stores each result when it is first worked out."),
        ("Tabulation (bottom-up)", "Filling in a table from the smallest sub-problem upwards."),
        ("Knapsack problem", "Choosing items of different weights and values to give the greatest value within a weight limit."),
        ("Edit distance", "The fewest single letter insertions, deletions and substitutions that turn one string into another."),
        ("Brute force", "Trying every possible answer and keeping the best."),
    ],
    grade="""
These problems are about choosing and justifying an approach, so the top marks are for reasons.

+ Name the strategy, then tie it to a property of the problem: overlapping sub-problems for dynamic programming, a provable local choice for greedy
+ Give a counter example when asked why greedy fails: coins 1, 3 and 4 making 6, where greedy gives 4 + 1 + 1 but 3 + 3 is better
+ Compare costs in numbers: 2^n subsets against an n x W table
+ Say what the trade is. Dynamic programming exchanges memory for time
+ For an intractable problem, say a heuristic gives a good answer, not the best, in a sensible time
""",
    mistakes=[
        "Assuming a greedy algorithm always finds the best answer. It only does when the greedy choice is provably safe.",
        "Describing dynamic programming as 'just recursion'. The point is that the sub-answers are stored and reused.",
        "Forgetting that memoisation and tabulation need memory to hold the results.",
        "Saying a heuristic is wrong because it is not optimal. It is a deliberate trade of quality for speed.",
        "Mixing up divide and conquer with dynamic programming. The first has independent pieces, the second overlapping ones.",
    ],
    quiz=[
        Q("What does a greedy algorithm do at each step?",
          ["Takes the choice that looks best at that moment and never reconsiders it", "Tries every possible choice and keeps the best",
           "Stores every earlier result in a table", "Splits the problem into two equal halves"], 0,
          "Greedy builds its answer one locally best step at a time without ever going back."),
        Q("Coins are worth 1p, 3p and 4p. A greedy algorithm gives change for 6p. How many coins does it give, and is that the fewest?",
          ["3 coins (4, 1, 1), and the fewest is 2 coins (3, 3)", "2 coins (3, 3), which is the fewest",
           "3 coins (3, 3, 1), which is the fewest", "2 coins (4, 1), which is the fewest"], 0,
          "Greedy grabs the 4 first and then needs two 1p coins. Two 3p coins do the job in fewer."),
        Q("Which of these is a greedy algorithm?",
          ["Kruskal's algorithm for a minimum spanning tree", "Merge sort", "Binary search", "Bubble sort"], 0,
          "Kruskal always takes the cheapest edge that does not make a cycle."),
        Q("What two features suggest that dynamic programming will work for a problem?",
          ["Overlapping subproblems and optimal substructure", "A sorted input and a small output",
           "A base case and a stack", "A large number of loops and a queue"], 0,
          "The same smaller problems recur, and the best answer is built from the best smaller answers."),
        Q("What is the difference between memoisation and tabulation?",
          ["Memoisation is top-down recursion with a cache; tabulation fills a table from the smallest case up", "Memoisation uses loops and tabulation uses recursion",
           "Memoisation is faster for every problem", "Tabulation does not store any results"], 0,
          "Both store sub-answers. They differ in direction: from the question downwards, or from the smallest case upwards."),
        Q("Why does dynamic programming make the naive recursive Fibonacci function so much quicker?",
          ["Each value is calculated once and then looked up", "It uses fewer variables", "It removes the base case", "It sorts the values first"], 0,
          "The number of calls drops from exponential to linear because repeated calls are answered from the store."),
        Q("The 0/1 knapsack has n items and a weight limit of W. What is the cost of the table method?",
          ["O(n x W)", "O(2^n)", "O(n)", "O(log n)"], 0,
          "The table has n rows and about W columns and each cell takes a fixed number of steps."),
        Q("What does the edit distance between two words measure?",
          ["The fewest insertions, deletions and substitutions to turn one word into the other", "The number of letters the words share",
           "The difference in length between the words", "The number of vowels that differ"], 0,
          "It is the size of the smallest set of single letter changes that turns one string into the other."),
        Q("A travelling salesperson problem has 20 towns. Why is a heuristic used instead of checking every route?",
          ["There are far too many routes to check in a reasonable time", "Heuristics always give the shortest route",
           "A computer cannot store the coordinates of 20 towns", "Checking every route needs a sorted list"], 0,
          "There are 19! routes, about 1.2 x 10^17. A heuristic gives a good route in a fraction of a second."),
        Q("What is a heuristic?",
          ["A shortcut that gives a good answer quickly but with no guarantee of the best", "A proof that an algorithm is correct",
           "An algorithm that always finds the best answer", "A way of storing results in a table"], 0,
          "Heuristics trade the guarantee of an optimal answer for speed."),
    ],
    exam=[
        EQ("Explain what is meant by a greedy algorithm.", 3, [
            MP("It builds the solution one step at a time", ["step", "one at a time", "stage", "builds"]),
            MP("At each step it takes the choice that looks best at that moment", ["best", "locally", "immediate", "right now", "current"]),
            MP("It never goes back to change a choice it has made", ["never", "back", "reconsider", "undo", "backtrack", "change"]),
        ], "A greedy algorithm builds a solution one step at a time. At each step it makes the choice that looks best at that moment, without looking ahead, and it never goes back to change a choice it has already made. It is usually quick and simple, but it only gives the best answer when the problem is one where the locally best choice is safe.",
           command="Explain"),
        EQ("A country has coins worth 1p, 3p and 4p. A greedy algorithm gives change by always using the largest coin that fits. Show, with a worked example, that this does not always give the fewest coins.", 3, [
            MP("Chooses an amount where it fails, such as 6p", ["6p", "6", "six"]),
            MP("Shows greedy gives 4 + 1 + 1, which is three coins", ["4 + 1 + 1", "4, 1, 1", "three coins", "3 coins"]),
            MP("Shows 3 + 3 uses only two coins, so greedy is not optimal", ["3 + 3", "3, 3", "two coins", "2 coins", "fewer"]),
        ], "For 6p the greedy algorithm first takes the largest coin that fits, which is 4p, leaving 2p. It then has to use two 1p coins, so it gives 4 + 1 + 1, three coins in total. But 3 + 3 makes 6p using only two coins, so the greedy answer is not the fewest.",
           command="Show"),
        EQ("The table shows the fewest coins needed to make each amount from 0p to 5p using coins of 1p, 3p and 4p. Calculate the values for 6p and 7p, showing your working.", 4, [
            MP("Uses the rule best[a] = 1 + the smallest best[a - coin] over the coins", ["1 +", "smallest", "minimum", "min", "previous", "a - coin"]),
            MP("For 6p considers best[5] + 1, best[3] + 1 and best[2] + 1", ["best[5]", "best[3]", "best[2]", "3, 1 and 2", "5p, 3p and 2p"]),
            MP("States the value for 6p is 2", ["2"]),
            MP("States the value for 7p is 2 (best[4] + 1 or best[3] + 1)", ["2", "best[4]", "best[3]", "3 + 4", "4 + 3"]),
        ], "Each value is 1 plus the smallest value found by taking one coin away. For 6p, taking away a 1p coin leaves 5p, which needs 2 coins, so that gives 3. Taking away a 3p coin leaves 3p, which needs 1 coin, so that gives 2. Taking away a 4p coin leaves 2p, which needs 2 coins, so that gives 3. The smallest is 2, so 6p needs 2 coins. For 7p, taking away 1p leaves 6p, which needs 2, giving 3. Taking away 3p leaves 4p, which needs 1, giving 2. Taking away 4p leaves 3p, which needs 1, giving 2. The smallest is 2, so 7p needs 2 coins (3 + 4).",
           command="Calculate",
           figure="""```text
amount:        0  1  2  3  4  5  6  7
fewest coins:  0  1  2  1  1  2  ?  ?
```"""),
        EQ("Describe two features of a problem that mean it can be solved using dynamic programming.", 4, [
            MP("Overlapping subproblems: the same smaller problem is needed more than once", ["overlapping", "same", "repeated", "more than once", "again"]),
            MP("So the answer to each is stored and reused instead of being recalculated", ["stored", "store", "reuse", "remember", "table", "cache", "memoisation"]),
            MP("Optimal substructure: the best solution is made from the best solutions to the smaller problems", ["optimal substructure", "substructure", "best solution", "built from"]),
            MP("An example such as Fibonacci, knapsack or edit distance", ["fibonacci", "knapsack", "edit distance", "coin", "longest common"]),
        ], "The first feature is overlapping sub-problems: the same smaller problem has to be solved many times, as fib(3) is needed by both fib(4) and fib(5). Dynamic programming stores each answer in a table or cache the first time it is worked out and reuses it, instead of recalculating it. The second feature is optimal substructure: the best solution to the whole problem can be built from the best solutions to its smaller sub-problems, as the fewest coins for 6p is built from the fewest for smaller amounts.",
           command="Describe"),
        EQ("A programmer must write a program to choose which of 40 items to load onto a lorry so that the total value is as high as possible without exceeding the weight limit. Discuss the approaches the programmer could take.", 6, [
            MP("Brute force would test every combination, 2^40 of them, which is over a trillion", ["brute force", "every combination", "2^40", "trillion", "all subsets", "every subset"]),
            MP("This is far too slow, because the work doubles with every extra item", ["too slow", "doubles", "exponential", "not feasible", "impractical"]),
            MP("A greedy method that takes items with the best value per kilogram first is fast, but may not give the best answer", ["greedy", "value per", "ratio", "not the best", "not optimal", "may not"]),
            MP("Dynamic programming builds a table of the best value for each weight limit using the first i items", ["dynamic programming", "table", "each weight", "first i", "sub-problems", "subproblems"]),
            MP("It finds the best answer in O(n x W), which is quick when the weight limit is a modest number", ["n x w", "n * w", "o(n", "quick", "efficient", "polynomial"]),
            MP("A reasoned conclusion: dynamic programming, since it is exact and fast enough, using more memory", ["conclusion", "best choice", "dynamic programming is", "therefore", "overall", "i would", "memory"]),
        ], "Brute force would check every combination of items. With 40 items there are 2^40, over a trillion combinations, and the number doubles with each extra item, so it is not feasible. A greedy method, taking the items with the best value for their weight first, is very quick, but it can fill the lorry badly and so may not give the highest value. Dynamic programming builds a table holding the best value for each possible weight limit using the first i items, and reads the answer from the last cell. It is guaranteed to give the best answer and takes O(n x W) steps, which is fast when the weight limit is a modest number, at the cost of the memory for the table. The programmer should therefore use dynamic programming.",
           command="Discuss"),
    ],
)
