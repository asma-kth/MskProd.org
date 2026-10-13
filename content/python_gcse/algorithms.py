"""GCSE Python: searching and sorting, written, traced and counted."""
from mskbuild.models import Topic, Section, Q, EQ, MP

INPUTS = {}
EXPECT = {}

TOPIC = Topic(
    slug="searching-and-sorting",
    title="Searching and Sorting Algorithms",
    spec="GCSE 6",
    icon="i-search",
    minutes=45,
    blurb="Linear and binary search, bubble, insertion and merge sort: each one written in Python, traced by hand, and run on real data with a counter so you can see why one beats another.",
    fact="Sorting is thought to have taken up a quarter of all computer time in the 1960s. Which algorithm to use mattered so much that Donald Knuth gave a whole volume of The Art of Computer Programming to it, and it is still the standard reference.",
    sections=[
        Section("Linear and binary search", r"""
A **search** looks for one value in a list and reports where it is, or that it is missing.

### Linear search

Check each item in turn, starting at the front, until you find it or run out.

```python
def linear_search(items, target):
    comparisons = 0
    for i in range(len(items)):
        comparisons += 1
        if items[i] == target:
            return i, comparisons
    return -1, comparisons

data = [3, 8, 12, 17, 21, 25, 30, 36, 41, 47, 52, 58, 63, 70, 76]
print(linear_search(data, 63))      # (12, 13): found at position 12 after 13 comparisons
print(linear_search(data, 50))      # (-1, 15): not there, so all 15 items were checked
```

Linear search works on **any** list, sorted or not. In the worst case it checks every item.

### Binary search

Binary search needs the list to be **sorted**. It looks at the **middle** item, and that one comparison throws away half of the list: if the target is bigger, everything at or before the middle is ruled out, and if it is smaller, everything at or after it is.

!diagram py-binary-search

```python
def binary_search(items, target):
    low = 0
    high = len(items) - 1
    comparisons = 0
    while low <= high:
        mid = (low + high) // 2
        comparisons += 1
        if items[mid] == target:
            return mid, comparisons
        elif items[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1, comparisons

data = [3, 8, 12, 17, 21, 25, 30, 36, 41, 47, 52, 58, 63, 70, 76]
print(binary_search(data, 63))      # (12, 4)
print(binary_search(data, 50))      # (-1, 4)
```

Looking for 63, the middle positions checked are 7, 11, 13 and then 12. That is four comparisons where the linear search needed thirteen.

### A trace table for binary search

A trace table follows each variable through the algorithm. This is the one the exam asks for, for `target = 63`:

| Pass | `low` | `high` | `mid` | `items[mid]` | Decision |
| 1 | 0 | 14 | 7 | 36 | 36 < 63, so `low = 8` |
| 2 | 8 | 14 | 11 | 58 | 58 < 63, so `low = 12` |
| 3 | 12 | 14 | 13 | 70 | 70 > 63, so `high = 12` |
| 4 | 12 | 12 | 12 | 63 | Found at position 12 |

!warn Binary search on an unsorted list gives wrong answers :: It does not crash and it does not warn you. It simply discards the half of the list the item happened to be in. Always say "the list must be sorted" when an exam asks for the condition.

### How much faster?

Every comparison halves what is left, so doubling the size of the list adds only **one** more comparison.

```python
for n in [16, 256, 4096, 65536, 1048576]:
    steps = 0
    size = n
    while size > 0:
        size = size // 2
        steps += 1
    print(n, "items need at most", steps, "comparisons")
```

A million items in at most 21 comparisons. A linear search of the same list could need a million.
"""),
        Section("Bubble sort and insertion sort", r"""
**Sorting** puts a list in order. The exam names three algorithms, and you must be able to describe each, trace it by hand and complete code for it.

### Bubble sort

Compare each pair of **neighbours** and swap them if they are the wrong way round. After one pass the largest item has been carried to the end, like a bubble rising. Keep making passes until a whole pass has no swaps.

```python
def bubble_sort(items):
    items = items[:]
    n = len(items)
    passes = 0
    swapped = True
    while swapped:
        swapped = False
        for i in range(n - 1 - passes):
            if items[i] > items[i + 1]:
                temp = items[i]
                items[i] = items[i + 1]
                items[i + 1] = temp
                swapped = True
        passes += 1
        print("after pass", passes, items)
    return items

print(bubble_sort([5, 1, 4, 2, 8]))
```

Run it and watch. After pass 1 the 8 is in place, after pass 2 the 5 is, and pass 3 makes no swaps, so the loop stops.

Two details earn marks:

- **The swap needs a temporary variable.** `items[i] = items[i + 1]` followed by `items[i + 1] = items[i]` loses a value. Python can swap in one line, `items[i], items[i + 1] = items[i + 1], items[i]`, but the exam swap uses `temp`.
- **The `swapped` flag** lets the algorithm stop early. Without it, bubble sort always makes the full number of passes, even on a list that was sorted from the start. The `n - 1 - passes` shortens each pass because the end of the list is already final.

### Insertion sort

Take the items one at a time and **insert** each into its correct place among the ones before it, which are already in order, shifting larger items one place right to make room. It is how most people sort a hand of cards.

```python
def insertion_sort(items):
    items = items[:]
    for i in range(1, len(items)):
        current = items[i]
        j = i - 1
        while j >= 0 and items[j] > current:
            items[j + 1] = items[j]
            j = j - 1
        items[j + 1] = current
        print("inserted", current, "->", items)
    return items

print(insertion_sort([5, 1, 4, 2, 8]))
```

Notice the 8 does no shifting at all. Insertion sort is quick on a list that is already nearly in order, which bubble sort is not.
"""),
        Section("Merge sort", r"""
**Merge sort** uses **divide and conquer**. A list of one item is already sorted. So split the list in half again and again until every piece has a single item, then **merge** the pieces back together in order. Merging two sorted lists is easy: look at the front of each, and take the smaller.

!diagram py-merge-sort

```python
def merge(left, right):
    result = []
    i = 0
    j = 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            result.append(left[i])
            i = i + 1
        else:
            result.append(right[j])
            j = j + 1
    result.extend(left[i:])
    result.extend(right[j:])
    return result

def merge_sort(items):
    if len(items) <= 1:
        return items
    middle = len(items) // 2
    left = merge_sort(items[:middle])
    right = merge_sort(items[middle:])
    return merge(left, right)

print(merge_sort([38, 27, 43, 3, 9, 82, 10]))
```

`merge_sort` calls itself on each half. That technique is called recursion, and you are not required to write it at GCSE. What you must be able to do is show the splitting down to single items and the merging back up, as in the diagram.

### Choosing between them

| | Bubble sort | Insertion sort | Merge sort |
| Idea | Swap neighbours | Insert each item into the sorted part | Split, then merge |
| Easy to write | Very | Yes | Harder |
| Big lists | Very slow | Slow | Fast |
| Nearly sorted list | Fast, with the flag | Fast | Same as any |
| Extra memory | None | None | Yes, for the merged copies |

### Counting the work

Run a bubble sort on a reversed list, so it has the most to do, and count the comparisons as the list gets longer.

```python
def bubble_comparisons(items):
    items = items[:]
    comparisons = 0
    n = len(items)
    for p in range(n - 1):
        for i in range(n - 1 - p):
            comparisons += 1
            if items[i] > items[i + 1]:
                items[i], items[i + 1] = items[i + 1], items[i]
    return comparisons

for n in [10, 20, 40, 80]:
    print(n, "items:", bubble_comparisons(list(range(n, 0, -1))), "comparisons")
```

Doubling the list from 20 to 40 does not double the work, it **quadruples** it: 190 comparisons becomes 780. That is why bubble sort is fine for ten names and hopeless for a million. Merge sort's work grows far more slowly.

!exam Compare two sorts with a reason :: "Merge sort is faster" earns nothing. "Merge sort is faster on a large list because it does far fewer comparisons, since it halves the list each time, but it needs extra memory for the merged copies" earns three marks.
"""),
    ],
    keyterms=[
        ("Algorithm", "A step by step set of instructions for solving a problem."),
        ("Linear search", "Checking each item of a list in turn, from the start, until the wanted item is found or the end is reached."),
        ("Binary search", "Repeatedly comparing with the middle item of a sorted list and discarding the half that cannot contain the target."),
        ("Bubble sort", "A sort that repeatedly compares neighbouring items and swaps them if they are in the wrong order, until a pass makes no swaps."),
        ("Insertion sort", "A sort that takes each item in turn and inserts it into its correct place in the already sorted part of the list."),
        ("Merge sort", "A divide and conquer sort that splits a list into single items and merges them back together in order."),
        ("Divide and conquer", "Solving a problem by splitting it into smaller copies of itself, solving those and combining the answers."),
        ("Trace table", "A table that records the values of variables at each step of an algorithm."),
        ("Pass", "One complete run through the list by a sorting algorithm."),
    ],
    grade="""
Sorting and searching questions reward the exact order of events, so practise tracing until it is automatic.

+ State that a binary search needs a sorted list, every time it is mentioned
+ Show the middle position working: (low + high) DIV 2, and which half is discarded
+ Write the state of the whole list after each pass of a bubble sort
+ Say that a sort stops when a pass has no swaps, not when it has done n passes
+ Compare algorithms using number of comparisons and memory, not the word "faster" alone
""",
    mistakes=[
        "Using a binary search on a list that is not in order.",
        "Swapping two items without a temporary variable, so one value is lost.",
        "Forgetting to carry on until a pass makes no swaps, and stopping after one pass.",
        "Calculating the middle with / and not DIV, which gives a decimal position.",
        "Saying a linear search is always slower, when for one search of an unsorted list it is the better choice.",
    ],
    quiz=[
        Q("What must be true of a list before a binary search can be used?",
          ["It must be sorted", "It must hold only numbers", "It must have an even number of items", "It must have no duplicates"], 0,
          "Binary search throws half of the list away on the strength of one comparison, which only works if the list is in order."),
        Q("A binary search of `[2, 4, 6, 8, 10, 12, 14]` begins by comparing with which item?",
          ["8", "2", "14", "6"], 0,
          "The middle position is (0 + 6) DIV 2 = 3, and the item at position 3 is 8."),
        Q("Which search is the better choice for one search of a short list that is not sorted?",
          ["A linear search", "A binary search", "Either, because they are equally fast", "Neither can be used"], 0,
          "Binary search needs a sorted list, and sorting costs more than the single linear pass it would save."),
        Q("What does a bubble sort do on each pass?",
          ["Compares neighbouring items and swaps them if they are in the wrong order", "Splits the list in half",
           "Picks the smallest item and moves it to the front", "Searches for the middle item"], 0,
          "It repeatedly compares each pair of neighbours, which carries the largest item to the end like a bubble rising."),
        Q("What is the list `[5, 1, 4, 2, 8]` after the first pass of a bubble sort?",
          ["`[1, 4, 2, 5, 8]`", "`[1, 2, 4, 5, 8]`", "`[1, 5, 4, 2, 8]`", "`[5, 1, 4, 2, 8]`"], 0,
          "The 5 is swapped past 1, 4 and 2 but not past 8, which gives [1, 4, 2, 5, 8]."),
        Q("How does a bubble sort know it has finished?",
          ["A whole pass makes no swaps", "It has made one pass", "It has reached the middle of the list", "It has found the target"], 0,
          "If nothing needed swapping, every neighbouring pair is in order, so the list must be sorted."),
        Q("Which technique does a merge sort use?",
          ["Divide and conquer", "Swapping neighbours", "Inserting one item at a time", "Searching for the middle"], 0,
          "It splits the list into halves repeatedly, then conquers by merging sorted halves."),
        Q("What does an insertion sort do with each item in turn?",
          ["Inserts it into the correct place among the items already sorted",
           "Compares it with its neighbour and swaps them if they are in the wrong order",
           "Splits the list in half and sorts each half separately",
           "Looks for the smallest item left and swaps it into the next place"], 0,
          "The items before the current one are always in order, and the current one is slotted in among them."),
        Q("Why is a merge sort quicker than a bubble sort on a very large list?",
          ["It needs far fewer comparisons", "It uses no memory", "It does not compare items at all", "It only works on small lists"], 0,
          "Halving the list each time means the work grows slowly, where bubble sort's work is quadrupled when the list is doubled."),
        Q("Which of these sorts needs extra memory for copies of parts of the list?",
          ["Merge sort", "Bubble sort", "Insertion sort", "All three need the same"], 0,
          "Merging builds new lists. Bubble and insertion sort rearrange the items within the original list."),
    ],
    exam=[
        EQ("The list shown is sorted. Describe the steps a binary search takes to find the value 28.", 4, [
            MP("Finds the middle item, which is 17", ["middle", "17", "centre"]),
            MP("Compares 28 with 17 and discards the lower half because 28 is larger", ["larger", "greater", "bigger", "discard", "ignore", "upper half", "right half", "higher"]),
            MP("Takes the middle of the remaining items, which is 28", ["middle", "28", "22, 28, 35", "remaining"]),
            MP("Compares and finds 28, so the search is complete", ["found", "match", "equal", "stops", "complete", "position 5"]),
        ], "The middle item of the seven is 17, at position 3. 28 is larger than 17, so the lower half and 17 itself are discarded, leaving 22, 28 and 35. The middle of those is 28, which matches, so the search stops and reports that 28 is at position 5.",
           command="Describe",
           figure="""| Position | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
| Value | 3 | 9 | 14 | 17 | 22 | 28 | 35 |"""),
        EQ("Write a Python function called linear_search that takes a list and a target and returns the position of the target in the list, or -1 if it is not in the list.", 4, [
            MP("Defines a function with two parameters, the list and the target", ["def linear_search", "def", "target"]),
            MP("A loop that goes through the positions of the list", ["for", "range(len", "while", "loop"]),
            MP("Compares each item with the target and returns the position when equal", ["==", "return i", "return the position", "equal"]),
            MP("Returns -1 after the loop, once every item has been checked", ["-1", "after the loop", "outside"]),
        ], r"""```python
def linear_search(items, target):
    for i in range(len(items)):
        if items[i] == target:
            return i
    return -1

print(linear_search([4, 8, 15, 16], 15), linear_search([4, 8, 15, 16], 99))
```

Each position is checked in turn and returned as soon as the item matches. The return of -1 is outside the loop, so it only happens when every item has been checked and none matched. The calls shown print 2 and -1.""",
           command="Write"),
        EQ("Show the contents of the list after each of the first two passes of a bubble sort on the list [6, 2, 9, 4]. State whether a third pass is needed.", 3, [
            MP("After the first pass the list is [2, 6, 4, 9]", ["2, 6, 4, 9", "2 6 4 9"]),
            MP("After the second pass the list is [2, 4, 6, 9]", ["2, 4, 6, 9", "2 4 6 9"]),
            MP("A third pass is needed to confirm that no swaps are made", ["third", "no swaps", "no swap", "confirm", "check"]),
        ], "First pass: 6 and 2 swap to give 2, 6, 9, 4. 6 and 9 are in order. 9 and 4 swap, so the list is [2, 6, 4, 9]. Second pass: 2 and 6 are in order, 6 and 4 swap, giving [2, 4, 6, 9]. Another pass is needed, because the second pass made a swap, and it will confirm there are no swaps so the algorithm can stop.",
           command="Show"),
        EQ("A programmer must find one name in an unsorted list of 20 names, once. Explain why a linear search is a better choice than sorting the list and then using a binary search.", 3, [
            MP("A binary search can only be used on a sorted list", ["sorted", "in order", "needs to be sorted"]),
            MP("Sorting the list takes more steps than one linear search would", ["more steps", "takes longer", "time", "slower", "more work", "more comparisons", "not worth"]),
            MP("The search is only done once so there is no benefit from sorting", ["once", "one search", "only one", "single", "no benefit", "just once"]),
        ], "A binary search only works on a sorted list, so the names would have to be sorted first. Sorting 20 names takes more comparisons than simply checking all 20 once with a linear search. Because the search is only carried out once, there are no later searches to benefit from the sorted list, so the sorting would be wasted effort.",
           command="Explain"),
        EQ("Compare a merge sort with a bubble sort for sorting a list of one million names.", 4, [
            MP("Merge sort needs far fewer comparisons on a large list", ["fewer comparisons", "less comparisons", "faster", "quicker", "far fewer", "less time", "efficient"]),
            MP("Because it halves the list repeatedly, whereas a bubble sort compares neighbours over many passes", ["halves", "divide", "split", "many passes", "every pass", "passes"]),
            MP("Merge sort needs extra memory to hold the merged lists", ["extra memory", "more memory", "additional memory", "copies", "new lists"]),
            MP("Bubble sort sorts in place and is simpler to write, but is too slow for a million items", ["in place", "no extra", "simpler", "easier", "too slow", "simple"]),
        ], "A merge sort is much better for a million names because it needs far fewer comparisons. It splits the list in half repeatedly and merges sorted halves, so the work grows slowly as the list grows, where a bubble sort makes many passes comparing neighbours and its work quadruples when the list is doubled. The cost of merge sort is that it needs extra memory for the lists it builds, whereas a bubble sort works in place and is simpler to write, but it would be far too slow for a million items.",
           command="Compare"),
    ],
)
