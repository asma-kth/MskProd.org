"""A Level Python: quick sort, comparing the sorts with counters, and stability."""
from mskbuild.models import Topic, Section, Q, EQ, MP

INPUTS = {}
EXPECT = {}

TOPIC = Topic(
    slug="sorting-algorithms",
    title="Sorting Algorithms in Depth",
    spec="A Level 9",
    icon="i-shuffle",
    minutes=55,
    blurb="Quick sort in two forms, the four sorts counted on random, sorted and reversed data so you can see their best and worst cases, then stability, in place sorting, and what Python's own sort does.",
    fact="Python's built in sort is called Timsort, written by Tim Peters in 2002 for Python and now used by Java, Android and the V8 engine in Chrome. It looks for runs of already ordered data in real life input, which is why sorting a nearly sorted list is nearly free.",
    sections=[
        Section("Quick sort", r"""
You know bubble sort, insertion sort and merge sort. **Quick sort** is the fourth sort in the specification, and the one most often used in practice. Like merge sort it is **divide and conquer**, but it does its work at a different moment.

1. Choose one item, the **pivot**.
2. **Partition**: put every item smaller than the pivot on its left, and every other item on its right. The pivot is now in its **final position**.
3. Sort the left part and the right part by calling quick sort on each, **recursively**.
4. A part of one item, or none, is already sorted, which is the base case.

Merge sort does the easy split and the hard merge. Quick sort does the hard split, the partition, and the merge is nothing at all.

```python
def quick_sort(items):
    if len(items) <= 1:
        return items
    pivot = items[0]
    smaller = [x for x in items[1:] if x < pivot]
    larger = [x for x in items[1:] if x >= pivot]
    return quick_sort(smaller) + [pivot] + quick_sort(larger)

print(quick_sort([6, 3, 9, 1, 8, 4]))
```

Partitioning `[6, 3, 9, 1, 8, 4]` around the first item gives `[3, 1, 4]` on the left, 6 in its place, and `[9, 8]` on the right. Each is then sorted in the same way.

### Sorting in place

The version above builds new lists, which costs memory. The standard version rearranges the original list by **swapping**. It keeps a `boundary` that has everything smaller than the pivot on its left, and moves it along whenever it finds another small item.

```python
def partition(items, low, high):
    pivot = items[high]                 # take the last item as the pivot
    boundary = low
    for i in range(low, high):
        if items[i] < pivot:
            items[i], items[boundary] = items[boundary], items[i]
            boundary += 1
    items[boundary], items[high] = items[high], items[boundary]
    return boundary                     # the pivot's final position

def quick_sort_in_place(items, low=0, high=None):
    if high is None:
        high = len(items) - 1
    if low < high:
        p = partition(items, low, high)
        quick_sort_in_place(items, low, p - 1)
        quick_sort_in_place(items, p + 1, high)

data = [6, 3, 9, 1, 8, 4]
print(partition(data, 0, 5), data)          # the pivot 4 goes to position 2
quick_sort_in_place(data)
print(data)
```

### The pivot decides everything

If the pivot lands near the **middle** of the data, each part is half the size and there are about log n levels of recursion, each doing n work: **O(n log n)**.

If it keeps landing at an **end**, one part is empty and the other has everything except the pivot. The recursion is n levels deep, and the work is n + (n - 1) + (n - 2) and so on, which is **O(n²)**. That happens when the first item is the pivot and the data is **already sorted**, which is a very common input.

!warn The worst case is not exotic :: Quick sort with the first item as pivot is at its slowest on a list that is already in order. Real implementations choose the pivot at random, or use the median of the first, middle and last items, so that no ordinary input triggers it.
"""),
        Section("Counting the work", r"""
The claims above can be tested. This program counts the comparisons each of the four sorts makes on the **same** 200 numbers: in random order, already sorted, and in reverse order. The numbers come from a small formula rather than from `random`, so every run gives the same answer.

```python
def pseudo_random_list(n, seed=12345):
    values = []
    x = seed
    for _ in range(n):
        x = (x * 1103515245 + 12345) % 2147483648
        values.append(x % 1000)
    return values

def bubble(items):
    items = items[:]
    n = len(items)
    comparisons = 0
    swapped = True
    passes = 0
    while swapped:
        swapped = False
        for i in range(n - 1 - passes):
            comparisons += 1
            if items[i] > items[i + 1]:
                items[i], items[i + 1] = items[i + 1], items[i]
                swapped = True
        passes += 1
    return items, comparisons

def insertion(items):
    items = items[:]
    comparisons = 0
    for i in range(1, len(items)):
        current = items[i]
        j = i - 1
        while j >= 0:
            comparisons += 1
            if items[j] > current:
                items[j + 1] = items[j]
                j -= 1
            else:
                break
        items[j + 1] = current
    return items, comparisons

def merge_sort(items):
    comparisons = 0
    def sort(part):
        nonlocal comparisons
        if len(part) <= 1:
            return part
        middle = len(part) // 2
        left = sort(part[:middle])
        right = sort(part[middle:])
        merged = []
        i = j = 0
        while i < len(left) and j < len(right):
            comparisons += 1
            if left[i] <= right[j]:
                merged.append(left[i])
                i += 1
            else:
                merged.append(right[j])
                j += 1
        merged.extend(left[i:])
        merged.extend(right[j:])
        return merged
    return sort(items), comparisons

def quick_sort(items):
    comparisons = 0
    def sort(part):
        nonlocal comparisons
        if len(part) <= 1:
            return part
        pivot = part[0]
        smaller = []
        larger = []
        for x in part[1:]:
            comparisons += 1
            if x < pivot:
                smaller.append(x)
            else:
                larger.append(x)
        return sort(smaller) + [pivot] + sort(larger)
    return sort(items), comparisons

numbers = pseudo_random_list(200)
cases = [("random", numbers), ("sorted", sorted(numbers)), ("reversed", sorted(numbers, reverse=True))]

print("comparisons".ljust(14) + "".join(name.ljust(10) for name, data in cases))
for label, sort in [("bubble", bubble), ("insertion", insertion), ("merge", merge_sort), ("quick", quick_sort)]:
    row = label.ljust(14)
    for name, data in cases:
        result, comparisons = sort(data)
        assert result == sorted(data)
        row += str(comparisons).ljust(10)
    print(row)
```

Read the table the program prints and compare it with the claims.

| Comparisons for 200 items | Random | Already sorted | Reversed |
| Bubble sort, with the swapped flag | 19 900 | **199** | 19 900 |
| Insertion sort | 9 913 | **199** | 19 900 |
| Merge sort | 1 272 | 732 | 822 |
| Quick sort, first item as pivot | 1 493 | **19 900** | 17 977 |

- **Bubble and insertion sort** need only 199 comparisons, n - 1, on a list that is already sorted: their best case is O(n). Their worst case is about n squared over two, 19 900.
- **Merge sort** hardly cares what order the data is in. It always splits and merges, so it is O(n log n) in every case. That consistency is its selling point.
- **Quick sort** is fastest on random data, and worst of all on sorted data, where it matches bubble sort's worst case. That is the pivot problem from the first section.

### Choosing

| | Bubble | Insertion | Merge | Quick |
| Average time | O(n squared) | O(n squared) | O(n log n) | O(n log n) |
| Worst time | O(n squared) | O(n squared) | O(n log n) | O(n squared) |
| Best time | O(n) | O(n) | O(n log n) | O(n log n) |
| Extra space | O(1) | O(1) | O(n) | O(log n) for the recursion |
| Stable | Yes | Yes | Yes | Not in the in place form |
| Best used | Teaching | Short or nearly sorted lists | Big data, or when the worst case must be guaranteed | General purpose, in memory |
"""),
        Section("Stability, and the sort you will actually use", r"""
A sort is **stable** if items that compare equal stay in their **original order**. It sounds minor and it is what makes sorting by two keys possible. Take people with a name and a grade, already in alphabetical order:

```python
people = [("Asha", "B"), ("Ben", "A"), ("Chloe", "B"), ("Dev", "A")]

by_grade = sorted(people, key=lambda person: person[1])
print(by_grade)
```

The two A grades are still in alphabetical order, Ben before Dev, and so are the two Bs. A **stable** sort kept the earlier order among the ties, so sorting by grade did not undo sorting by name. An unstable sort is allowed to give Dev before Ben, and would, from time to time.

This gives the standard method for sorting on **two keys**: sort by the less important key first, then by the more important. Stability is what carries the first sort through the second.

```python
people = [("Asha", "B"), ("Ben", "A"), ("Chloe", "B"), ("Dev", "A")]

people.sort(key=lambda person: person[0])         # first by name
people.sort(key=lambda person: person[1])         # then by grade; names stay in order
print(people)

print(sorted([3, 1, 2], reverse=True))
print(sorted(["pear", "fig", "banana"], key=len))
```

### What Python does

Python's `sorted` and `list.sort` use **Timsort**, a hybrid of merge sort and insertion sort. It looks for stretches of the data that are already in order, called **runs**, and merges them. On random data it is O(n log n). On data that is already sorted it is **O(n)**, because the whole list is one run. It is stable. In real programs, data is rarely random, and that is why Timsort is quick.

!key The right answer in exam and in practice :: Know how to write each sort, because the exam asks for it. In a program, call `sorted`. A hand written sort is slower than the built in one, and a likelier place for a bug.

### Searching a sorted list

Sorting pays for itself when you search the same data many times, because a **binary search** can be used. You wrote it with a loop. Here it is recursively, and with the library function `bisect`, which finds the position where a value is, or belongs, in a sorted list.

```python
from bisect import bisect_left

def binary_search(items, target, low=0, high=None):
    if high is None:
        high = len(items) - 1
    if low > high:
        return -1
    mid = (low + high) // 2
    if items[mid] == target:
        return mid
    if items[mid] < target:
        return binary_search(items, target, mid + 1, high)
    return binary_search(items, target, low, mid - 1)

data = [3, 8, 12, 17, 21, 25, 30, 36, 41]
print(binary_search(data, 25), binary_search(data, 26))
print(bisect_left(data, 25), bisect_left(data, 26))
```

`bisect_left(data, 26)` gives 6: the position where 26 **would** be inserted to keep the list sorted. A sorted list plus `bisect` is a way to find the nearest value, or to keep a list in order as items are added.
"""),
    ],
    keyterms=[
        ("Quick sort", "A divide and conquer sort that partitions a list around a pivot and then sorts each part recursively."),
        ("Pivot", "The item in quick sort that the others are compared with when the list is partitioned."),
        ("Partition", "Rearranging a list so that items smaller than the pivot come before it and the others after it."),
        ("In-place sort", "A sort that rearranges the items within the original list, using only a small amount of extra memory."),
        ("Stable sort", "A sort that keeps equal items in the same relative order that they had before the sort."),
        ("Best case", "The input of a given size for which an algorithm does the least work."),
        ("Worst case", "The input of a given size for which an algorithm does the most work."),
        ("Divide and conquer", "Solving a problem by dividing it into smaller copies of the same problem, solving them and combining the results."),
        ("Timsort", "A stable hybrid of merge sort and insertion sort that exploits runs of ordered data, and is the sort used by Python."),
    ],
    grade="""
A Level sorting answers are about cases and trade offs, with the numbers to back them.

+ Describe quick sort in the right order: choose a pivot, partition, sort the two parts recursively
+ Give the best, average and worst case of each sort, and the input that causes the worst case
+ Explain the quick sort worst case: the pivot is always the smallest or largest, so one part is empty
+ Compare time and space together, as merge sort needs O(n) extra memory and quick sort does not
+ Say what stable means, and why it matters when sorting on more than one key
""",
    mistakes=[
        "Saying quick sort is always O(n log n), forgetting the worst case.",
        "Choosing the first item as pivot and then claiming sorted data is the best case.",
        "Stating that merge sort is in place, when it needs extra memory for the merged lists.",
        "Describing a stable sort as one that does not crash, instead of one that keeps equal items in order.",
        "Forgetting that the pivot is in its final position after the partition and does not move again.",
    ],
    quiz=[
        Q("What is the pivot in a quick sort?",
          ["The item that the other items are compared with when the list is partitioned",
           "The item in the exact middle of the list, which is never moved",
           "The last item that is placed in order when the sort is complete",
           "The smallest item in the list, which is always moved to the front"], 0,
          "Items smaller than the pivot go before it and the rest go after it, which places the pivot in its final position."),
        Q("What is the average time complexity of quick sort?",
          ["O(n log n)", "O(n squared)", "O(n)", "O(log n)"], 0,
          "A pivot near the middle halves the problem each time, giving about log n levels of n work."),
        Q("When is the worst case of quick sort with the first item as pivot?",
          ["When the list is already sorted", "When the list is in random order", "When the list has only one item",
           "When the list has exactly two items"], 0,
          "Every pivot is the smallest remaining item, so one part is always empty and there are n levels of recursion."),
        Q("What is the worst case time complexity of merge sort?",
          ["O(n log n)", "O(n squared)", "O(n)", "O(2 to the power n)"], 0,
          "Merge sort always splits into halves and merges, so it does the same amount of work whatever the order of the data."),
        Q("Which of these sorts needs O(n) extra memory?",
          ["Merge sort", "Insertion sort", "Bubble sort", "In place quick sort"], 0,
          "Merging builds new lists as it goes. The others rearrange items within the original list."),
        Q("What does it mean for a sort to be stable?",
          ["Items with equal keys stay in their original order", "It never crashes on invalid data",
           "It always takes the same time whatever the data is", "It does not use any extra memory"], 0,
          "Stability is what lets you sort by one key and then another without losing the first order."),
        Q("Which sort needs the fewest comparisons on a list that is already sorted?",
          ["Insertion sort, with n - 1 comparisons", "Quick sort with the first item as pivot",
           "Merge sort, with exactly one comparison", "All of them need the same number"], 0,
          "Insertion sort only compares each item with its left neighbour once, and then moves on."),
        Q("Why do real quick sort implementations choose the pivot randomly or by median of three?",
          ["To avoid the worst case on data that is already in order", "To make the sort stable",
           "To reduce the amount of memory used", "To make the list fit in the cache"], 0,
          "A pivot that is not always at an end of the data stops sorted input from causing the O(n squared) behaviour."),
        Q("Which algorithm does Python's built in `sorted` use?",
          ["Timsort, a hybrid of merge sort and insertion sort", "Bubble sort", "Quick sort with the first item as pivot",
           "Selection sort"], 0,
          "Timsort is stable, O(n log n) in the worst case, and close to O(n) on data that is already nearly in order."),
        Q("A list of records is sorted by name, then the sort is repeated with grade as the key using a stable sort. What is the result?",
          ["Sorted by grade, with records of the same grade still in name order",
           "Sorted by grade, with records of the same grade in a random order",
           "Sorted by name, with the grades ignored completely",
           "An error, because a list cannot be sorted twice"], 0,
          "The second sort leaves ties as they were, and they were already in name order."),
    ],
    exam=[
        EQ("Describe how a quick sort works.", 4, [
            MP("An item is chosen as the pivot", ["pivot"]),
            MP("The list is partitioned so that items smaller than the pivot are on one side and larger items on the other", ["partition", "smaller", "larger", "less than", "greater than", "either side", "split"]),
            MP("The pivot is then in its final position", ["final position", "correct position", "sorted position", "in place"]),
            MP("The same process is repeated recursively on each part until the parts have one item or none", ["recursive", "recursively", "repeated", "each part", "sublist", "until"]),
        ], "An item is chosen as the pivot. The list is partitioned, so that all the items smaller than the pivot are on one side of it and all the larger items on the other, which puts the pivot in its final position. The same process is then repeated recursively on each of the two parts, until each part has one item or none, at which point the whole list is sorted.",
           command="Describe"),
        EQ("A quick sort uses the first item of the list as its pivot. State the two lists that are formed, and the position of the pivot, when the list [6, 3, 9, 1, 8, 4] is partitioned.", 3, [
            MP("The items smaller than the pivot are 3, 1 and 4", ["3, 1, 4", "3 1 4", "1, 3, 4"]),
            MP("The items larger than the pivot are 9 and 8", ["9, 8", "9 8", "8, 9"]),
            MP("The pivot, 6, is placed between them, in position 3", ["6", "position 3", "between"]),
        ], "The pivot is 6. The items smaller than 6, in their original order, are 3, 1 and 4, and the items larger are 9 and 8. The pivot is placed between the two lists, so the arrangement is 3, 1, 4, then 6, then 9, 8, and 6 is now in its final position, index 3.",
           command="State"),
        EQ("Write a recursive Python function called quick_sort that takes a list and returns a new list with the same items in ascending order. It must use the first item as the pivot.", 4, [
            MP("Base case: a list of 0 or 1 items is returned as it is", ["<= 1", "len(items)", "return items", "base case", "== 1", "== 0"]),
            MP("The first item is chosen as the pivot and the rest are split into smaller and larger lists", ["items[0]", "pivot", "smaller", "larger", "less", "greater"]),
            MP("The function calls itself on both the smaller and the larger list", ["quick_sort(smaller)", "quick_sort(larger)", "recursive call", "calls itself"]),
            MP("The results are joined with the pivot between them", ["+ [pivot] +", "pivot between", "join", "concatenate", "return"]),
        ], r"""```python
def quick_sort(items):
    if len(items) <= 1:
        return items
    pivot = items[0]
    smaller = [x for x in items[1:] if x < pivot]
    larger = [x for x in items[1:] if x >= pivot]
    return quick_sort(smaller) + [pivot] + quick_sort(larger)

print(quick_sort([6, 3, 9, 1, 8, 4]))
```

A list of 0 or 1 items is already sorted, which is the base case. Otherwise the first item is the pivot, the others are split into those smaller than it and the rest, each part is sorted by a recursive call, and the pivot is placed between the two sorted results. The call shown prints [1, 3, 4, 6, 8, 9].""",
           command="Write"),
        EQ("Compare the merge sort and quick sort algorithms.", 6, [
            MP("Both use divide and conquer, and both are O(n log n) on average", ["divide and conquer", "n log n", "average", "both"]),
            MP("The worst case of merge sort is still O(n log n)", ["o(n log n)", "worst case of merge", "always n log n", "guaranteed", "consistent"]),
            MP("The worst case of quick sort is O(n squared), for example with a poor pivot on sorted data", ["o(n squared)", "n squared", "poor pivot", "sorted data", "worst case of quick", "already sorted"]),
            MP("Merge sort needs O(n) extra memory for the merged lists, while quick sort can be done in place", ["extra memory", "o(n) space", "in place", "in-place", "memory"]),
            MP("Merge sort is stable, but the usual in place quick sort is not", ["stable", "stability", "equal items", "order of equal"]),
            MP("A conclusion, such as quick sort being faster in practice for memory held data, but merge sort being better when the worst case must be avoided or a stable sort is needed", ["conclusion", "faster in practice", "better when", "overall", "preferred", "choose", "suits"]),
        ], "Both are divide and conquer algorithms and both take O(n log n) time on average. The worst case of merge sort is still O(n log n), because it always splits into halves, whereas the worst case of quick sort is O(n squared), which happens when the pivot is repeatedly the smallest or largest item, as with the first item as pivot on data that is already sorted. Merge sort needs O(n) extra memory for the merged lists, while quick sort can be done in place and needs little extra memory. Merge sort is stable, so equal items stay in order, and the usual in place quick sort is not. Quick sort is often faster in practice for data held in memory, so it suits general use, but merge sort is the better choice when the worst case must be avoided, when the sort must be stable or when the data is too big to hold in memory.",
           command="Compare"),
        EQ("A list of student records is sorted by name, and is then sorted again by grade using a stable sort. Explain what is meant by a stable sort, and what the order of the final list will be.", 3, [
            MP("A stable sort keeps items with equal keys in their original relative order", ["equal", "same key", "original order", "relative order", "keeps"]),
            MP("The final list is in order of grade", ["grade", "sorted by grade", "ordered by grade"]),
            MP("Students with the same grade remain in alphabetical order of name", ["alphabetical", "name order", "by name", "still in order of name"]),
        ], "A stable sort keeps items that have equal keys in the same relative order that they had before the sort. After the second sort the list is in order of grade, and students with the same grade are still in alphabetical order of name, because they were in that order before the second sort and the stable sort did not change it.",
           command="Explain"),
    ],
)
