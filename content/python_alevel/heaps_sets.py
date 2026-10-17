"""A Level Python: heaps, tries and disjoint sets, and the minimum spanning tree."""
from mskbuild.models import Topic, Section, Q, EQ, MP

INPUTS = {}
EXPECT = {}

TOPIC = Topic(
    slug="heaps-tries-and-disjoint-sets",
    title="Heaps, Tries and Disjoint Sets",
    spec="A Level 7",
    icon="i-layers",
    minutes=50,
    blurb="Three structures that make real programs fast: the binary heap behind every priority queue, the trie behind autocomplete, and union-find for spotting connected groups, finishing with Kruskal's and Prim's minimum spanning trees.",
    fact="Every time your phone suggests the rest of a word, a structure very like a trie is doing the work. Typing three letters narrows millions of words to a handful, and the lookup takes the same few steps whether the dictionary holds a thousand words or a billion.",
    sections=[
        Section("The binary heap", r"""
A priority queue has to answer one question again and again: *which waiting item is the smallest?* A sorted list answers it instantly but is slow to insert into, because everything after the new item has to shift along. An unsorted list inserts instantly but needs a full scan to find the smallest. A **binary heap** is the compromise: it keeps the items only *partly* ordered, which is just enough.

A heap is a **complete binary tree**: every level is full except possibly the last, which fills from the left. In a **min-heap** it also obeys the **heap property**:

!key The heap property :: Every parent is less than or equal to both of its children. So the smallest item is always at the root, and nothing is promised about the order of items that are not directly above or below each other.

Because the tree is complete, it needs no pointers. It is stored in a plain list, level by level, and the position of a node tells you where its relatives are:

| Node at index `i` | Index |
| left child | `2 * i + 1` |
| right child | `2 * i + 2` |
| parent | `(i - 1) // 2` |

```python
heap = [1, 3, 8, 5, 4, 9]
i = 1
print("node", heap[i])
print("left child", heap[2 * i + 1])
print("right child", heap[2 * i + 2])
print("parent", heap[(i - 1) // 2])
```

### Adding an item: sift up

Put the new item at the end, so the tree stays complete. It may now be smaller than its parent, which breaks the property, so swap it with its parent, and repeat until it is in place or reaches the root. This is **sifting up**.

### Removing the smallest: sift down

The smallest is the root. Take it out, move the *last* item into the root's place so the tree stays complete, then swap that item downwards with its smaller child until the property holds again. This is **sifting down**.

```python
class MinHeap:
    def __init__(self):
        self.items = []

    def push(self, value):
        self.items.append(value)
        child = len(self.items) - 1
        while child > 0:
            parent = (child - 1) // 2
            if self.items[parent] <= self.items[child]:
                break
            self.items[parent], self.items[child] = self.items[child], self.items[parent]
            child = parent

    def pop(self):
        top = self.items[0]
        last = self.items.pop()
        if self.items:
            self.items[0] = last
            parent = 0
            size = len(self.items)
            while True:
                left, right = 2 * parent + 1, 2 * parent + 2
                smallest = parent
                if left < size and self.items[left] < self.items[smallest]:
                    smallest = left
                if right < size and self.items[right] < self.items[smallest]:
                    smallest = right
                if smallest == parent:
                    break
                self.items[parent], self.items[smallest] = self.items[smallest], self.items[parent]
                parent = smallest
        return top

h = MinHeap()
for value in [5, 3, 8, 1, 9, 2]:
    h.push(value)
    print("after pushing", value, "->", h.items)

print("removed", h.pop(), "->", h.items)
print("removed", h.pop(), "->", h.items)
```

Notice that the list is not sorted, and does not need to be. Only the smallest is guaranteed to be at the front.

### The cost

Both operations move an item at most the **height** of the tree, and a complete tree of n items has a height of about log~2~ n. Looking at the smallest is just `items[0]`.

| | Unsorted list | Sorted list | Binary heap |
| Find the smallest | O(n) | O(1) | O(1) |
| Add an item | O(1) | O(n) | O(log n) |
| Remove the smallest | O(n) | O(1) or O(n) | O(log n) |

"""),
        Section("Heap sort and the top k problem", r"""
### Heap sort

Push everything into a heap, then pop everything out. The items leave smallest first, so they come out sorted. Each of the n pushes and n pops costs O(log n), so the whole sort is **O(n log n)**, the same as merge sort, and unlike quick sort it has no bad case.

```python
import heapq

def heap_sort(values):
    heap = list(values)
    heapq.heapify(heap)           # turns a list into a heap in O(n)
    return [heapq.heappop(heap) for _ in range(len(heap))]

print(heap_sort([9, 4, 7, 1, 8, 2, 6]))
```

`heapq` is Python's built in heap. It works on an ordinary list and keeps a **min-heap**. `heapify` builds a heap from a list in O(n), faster than pushing items one at a time.

### The top k problem

How would you find the five highest scores out of a hundred thousand? Sorting everything costs O(n log n) and holds every score in memory. A heap does better. Keep a small min-heap of the best k seen so far. Its root is the *weakest* of the best, so a new score only matters if it beats the root, and then it replaces it.

```python
import heapq

def top_k(stream, k):
    best = []
    for score in stream:
        if len(best) < k:
            heapq.heappush(best, score)
        elif score > best[0]:
            heapq.heapreplace(best, score)
    return sorted(best, reverse=True)

scores = [(i * 7919) % 100003 for i in range(100000)]
print(top_k(scores, 5))
print(sorted(scores, reverse=True)[:5] == top_k(scores, 5))
```

The heap never holds more than five items, however long the stream. That makes it usable on data too big to fit in memory, such as a log file read one line at a time. Python wraps the idea up as `heapq.nlargest(k, data)` and `heapq.nsmallest(k, data)`.

### Priority with a payload

A heap compares whatever it stores. Store a tuple and it compares the first item, then the second if there is a tie, which is how the task queue in the stacks and queues topic works.

```python
import heapq

jobs = []
heapq.heappush(jobs, (2, "send newsletter"))
heapq.heappush(jobs, (1, "restart server"))
heapq.heappush(jobs, (2, "back up database"))

while jobs:
    priority, name = heapq.heappop(jobs)
    print(priority, name)
```

!warn A heap is not a sorted list :: Printing a heap shows a list that looks nearly sorted and is not. Reading `items[1]` does not give you the second smallest. The only guarantee is at the root. To get items in order you must pop them.
"""),
        Section("Tries: searching by prefix", r"""
A hash table finds a *whole* key fast. It cannot answer "which words start with `car`?" without checking every key. A **trie** (pronounced "try", from re*trie*val) is a tree built for exactly that question.

Each node stands for one letter, and the path from the root spells a prefix. Words that share a beginning share the nodes for it, so `car`, `card`, `care` and `cart` all hang from the same `c`, `a`, `r`. A marker records where a real word ends.

```python
class Trie:
    def __init__(self):
        self.root = {}

    def insert(self, word):
        node = self.root
        for letter in word:
            node = node.setdefault(letter, {})
        node["$"] = True                 # a word ends here

    def find(self, prefix):
        node = self.root
        for letter in prefix:
            if letter not in node:
                return None
            node = node[letter]
        return node

    def contains(self, word):
        node = self.find(word)
        return node is not None and "$" in node

    def suggest(self, prefix):
        found = []

        def walk(node, text):
            for letter in sorted(node):
                if letter == "$":
                    found.append(text)
                else:
                    walk(node[letter], text + letter)

        start = self.find(prefix)
        if start is not None:
            walk(start, prefix)
        return found

words = Trie()
for w in ["car", "card", "care", "careful", "cart", "cat", "do", "dog"]:
    words.insert(w)

print(words.contains("care"), words.contains("ca"))
print(words.suggest("car"))
print(words.suggest("d"))
print(words.suggest("x"))
```

`contains("ca")` is `False` even though the path exists, because no word ends there. That is the job of the `"$"` marker.

### Why it is quick

Looking up a word takes one step per letter, so the cost depends on the **length of the word**, not on how many words are stored. A trie of ten words and a trie of ten million both find `care` in four steps. Autocomplete uses this: follow the letters typed so far, then collect everything below that node.

| | Hash table of words | Trie |
| Is this exact word present? | O(1) on average | O(length) |
| All words starting with a prefix | Must check every key, O(n) | Follow the prefix, then walk the sub-tree |
| Words in alphabetical order | Needs a separate sort | Free, by visiting letters in order |
| Memory | Compact | Heavier: a node for every letter, though shared prefixes are stored once |

!key When to choose a trie :: Choose it when the questions are about *prefixes*: autocomplete, spell checking suggestions, phone number lookup, IP routing tables. If you only ever ask "is this exact key here?", a dictionary is simpler and smaller.
"""),
        Section("Disjoint sets and union-find", r"""
A social network wants to know whether two people are connected through a chain of friends. A game wants to know whether two rooms are joined. A network engineer wants to know whether adding a cable would join two groups that are already connected. All are asking: **are these two items in the same group?**, with groups that keep merging.

A **disjoint set** structure, usually called **union-find**, answers it with two operations:

- `find(x)` returns the **representative** (the root) of the group that holds x
- `union(a, b)` merges the groups that hold a and b

Each group is a tree stored in a list. `parent[x]` points at x's parent, and a root points at itself. Two items are in the same group if and only if `find` gives them the same root.

```python
class DisjointSets:
    def __init__(self, n):
        self.parent = list(range(n))     # at the start everyone is alone
        self.size = [1] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])    # path compression
        return self.parent[x]

    def union(self, a, b):
        root_a, root_b = self.find(a), self.find(b)
        if root_a == root_b:
            return False                 # already in the same group
        if self.size[root_a] < self.size[root_b]:
            root_a, root_b = root_b, root_a
        self.parent[root_b] = root_a     # hang the smaller tree under the bigger
        self.size[root_a] += self.size[root_b]
        return True

friends = DisjointSets(8)
for a, b in [(0, 1), (2, 3), (1, 2), (5, 6)]:
    friends.union(a, b)

print(friends.find(0) == friends.find(3))     # 0 - 1 - 2 - 3
print(friends.find(0) == friends.find(5))
groups = {friends.find(x) for x in range(8)}
print(len(groups), "groups")
```

### Two small ideas make it fast

- **Union by size.** Hang the smaller tree under the root of the bigger one, so trees stay shallow.
- **Path compression.** While `find` walks up to the root, it points every item it passes straight at the root. The next `find` from any of them takes one step.

```python
parent = [1, 2, 3, 4, 5, 6, 7, 8, 9, 9]      # a chain: 0 -> 1 -> 2 -> ... -> 9

def find(x):
    steps = 0
    path = []
    while parent[x] != x:
        path.append(x)
        x = parent[x]
        steps += 1
    for p in path:
        parent[p] = x                 # compress the path
    return x, steps

print(find(0))       # the first search walks the whole chain
print(find(0))       # now it is one step
print(find(4))
```

Together these make `find` and `union` run in close to constant time, however large the sets become.
"""),
        Section("Minimum spanning trees", r"""
A **spanning tree** of a graph joins *every* vertex using just enough edges to stay connected and no cycles: always one fewer edge than vertices. A **minimum spanning tree** (MST) is the spanning tree whose edges have the smallest possible total weight.

It is the answer to: *what is the cheapest way to connect all of these places?* Laying cable between offices, pipes between houses, or roads between villages. It is not the same as Dijkstra's algorithm, which finds the cheapest route from *one* vertex to another.

Both algorithms below are **greedy**: they repeatedly take the cheapest choice available, and for this problem that is provably enough.

### Kruskal's algorithm

Sort all edges by weight. Take them in order, and **accept an edge unless it would form a cycle**. Union-find answers "would it form a cycle?" in one call: if both ends are already in the same group, the edge is a cycle.

```python
class DisjointSets:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        return True

vertices = ["A", "B", "C", "D", "E", "F", "G"]
edges = [("A", "B", 7), ("A", "D", 5), ("B", "C", 8), ("B", "D", 9), ("B", "E", 7),
         ("C", "E", 5), ("D", "E", 15), ("D", "F", 6), ("E", "F", 8), ("E", "G", 9),
         ("F", "G", 11)]

def kruskal(vertices, edges):
    number = {v: i for i, v in enumerate(vertices)}
    groups = DisjointSets(len(vertices))
    chosen, total = [], 0
    for a, b, weight in sorted(edges, key=lambda e: e[2]):
        if groups.union(number[a], number[b]):
            print("accept", a + b, weight)
            chosen.append((a, b, weight))
            total += weight
        else:
            print("reject", a + b, weight, "(would make a cycle)")
    return chosen, total

tree, cost = kruskal(vertices, edges)
print(len(tree), "edges, total weight", cost)
```

### Prim's algorithm

Prim grows a single tree outwards. Start at any vertex. Repeatedly take the **cheapest edge that leads out of the tree to a new vertex**. A priority queue holds the candidate edges, so this is the same shape as Dijkstra's algorithm.

```python
import heapq

edges = [("A", "B", 7), ("A", "D", 5), ("B", "C", 8), ("B", "D", 9), ("B", "E", 7),
         ("C", "E", 5), ("D", "E", 15), ("D", "F", 6), ("E", "F", 8), ("E", "G", 9),
         ("F", "G", 11)]

def prim(edges, start):
    graph = {}
    for a, b, weight in edges:
        graph.setdefault(a, []).append((weight, a, b))
        graph.setdefault(b, []).append((weight, b, a))
    inside = {start}
    queue = list(graph[start])
    heapq.heapify(queue)
    total = 0
    while queue and len(inside) < len(graph):
        weight, a, b = heapq.heappop(queue)
        if b in inside:
            continue
        inside.add(b)
        total += weight
        print("add", b, "via", a + b, weight)
        for edge in graph[b]:
            if edge[2] not in inside:
                heapq.heappush(queue, edge)
    return total

print("total weight", prim(edges, "A"))
```

Different algorithms, same total: when edge weights tie, there can be more than one minimum spanning tree, but they all cost the same.

| | Kruskal | Prim |
| Grows | a forest of trees that merge | one tree |
| Key structure | sorted edges and union-find | priority queue |
| Suits | sparse graphs, few edges | dense graphs, many edges |
"""),
    ],
    keyterms=[
        ("Heap", "A complete binary tree stored in a list, in which every parent is ordered with respect to its children."),
        ("Heap property", "In a min-heap, every parent is less than or equal to its children, so the smallest item is at the root."),
        ("Sift up", "Swapping a newly added item with its parent until the heap property holds."),
        ("Sift down", "Swapping the item moved to the root with its smaller child until the heap property holds."),
        ("Heap sort", "Sorting by building a heap and repeatedly removing the smallest item. O(n log n)."),
        ("Trie", "A tree in which each node is a letter and each path from the root spells a prefix, used to search by prefix."),
        ("Disjoint set (union-find)", "A structure that keeps items in non overlapping groups, supporting find (which group?) and union (merge two groups)."),
        ("Path compression", "Making every item passed during a find point directly at the root, so later finds are quicker."),
        ("Spanning tree", "A tree that connects every vertex of a graph using the fewest edges, with no cycles."),
        ("Minimum spanning tree", "The spanning tree with the smallest total edge weight."),
        ("Greedy algorithm", "An algorithm that makes the best looking choice at each step and never reconsiders it."),
    ],
    grade="""
Heaps and trees of this kind are an extension beyond the specification list, so they appear as unseen structures. The marks go to reasoning, not memory.

+ State the property in one sentence: every parent is at most its children, so the minimum is at the root
+ When tracing an insertion, write the array after each swap and name the parent index you compared with
+ Compare costs with the alternatives: a heap gives O(log n) for both add and remove, where each list gives O(n) for one of them
+ For a trie, say the cost depends on word length, not on how many words are stored
+ For a spanning tree, say how many edges the answer has: one fewer than the number of vertices
""",
    mistakes=[
        "Saying a heap is sorted. Only the root is guaranteed to be the smallest.",
        "Getting the child index formulas wrong. They are 2i + 1 and 2i + 2 when the first index is 0.",
        "Forgetting the end of word marker in a trie, so that every prefix of a word counts as a word.",
        "Accepting a Kruskal edge that joins two vertices already in the same group, which makes a cycle.",
        "Mixing up a minimum spanning tree with a shortest path: one connects everything cheaply, the other goes from A to B cheaply.",
    ],
    quiz=[
        Q("In a min-heap, which item is always at the root?",
          ["The smallest item", "The largest item", "The item added first", "The item added most recently"], 0,
          "The heap property says every parent is no larger than its children, so the smallest item rises to the root."),
        Q("A heap is stored in a list with the first item at index 0. Where is the left child of the item at index 3?",
          ["Index 7", "Index 6", "Index 4", "Index 1"], 0,
          "The left child is at 2 * i + 1, which is 2 * 3 + 1 = 7."),
        Q("What does 'sifting up' do?",
          ["Swaps a new item with its parent until the heap property holds", "Sorts the whole heap into ascending order",
           "Removes the smallest item from the heap", "Moves the root to the end of the list"], 0,
          "A new item is added at the end and then moved up past every larger parent."),
        Q("Why is a heap a better choice than a sorted list for a priority queue with many insertions?",
          ["Inserting into a heap is O(log n) but into a sorted list is O(n)", "A heap keeps every item in alphabetical order",
           "A heap never needs to compare two items", "A heap can hold duplicates and a list cannot"], 0,
          "A sorted list has to shift items along to make room. A heap only moves the new item up one branch of the tree."),
        Q("What is the time complexity of heap sort?",
          ["O(n log n)", "O(n)", "O(n squared)", "O(log n)"], 0,
          "There are n insertions and n removals, each costing O(log n)."),
        Q("What is a trie mainly used for?",
          ["Finding all the words that begin with a given prefix", "Sorting numbers into ascending order",
           "Finding the shortest path in a weighted graph", "Detecting cycles in a graph"], 0,
          "Following the prefix letter by letter leads to a node whose sub-tree holds every word with that prefix."),
        Q("A trie holds 50 000 words. About how many steps does it take to check whether the 4 letter word 'care' is in it?",
          ["About 4", "About 50 000", "About 16", "About 200 000"], 0,
          "One step per letter. The cost depends on the length of the word, not on the number of words stored."),
        Q("What does path compression do in a union-find structure?",
          ["Points every item passed during a find straight at the root", "Merges two groups into one",
           "Removes an item from its group", "Sorts the groups by size"], 0,
          "It flattens the tree, so the next find from any of those items takes a single step."),
        Q("A connected graph has 9 vertices. How many edges does a spanning tree of it have?",
          ["8", "9", "10", "18"], 0,
          "A tree that connects n vertices has n - 1 edges. Any more would make a cycle."),
        Q("In Kruskal's algorithm, when is the next cheapest edge rejected?",
          ["When both of its ends are already in the same group, so it would form a cycle", "When it is the heaviest edge in the graph",
           "When it touches the starting vertex", "When another edge has the same weight"], 0,
          "Union-find reports that the two ends are already connected, so adding the edge would only create a cycle."),
    ],
    exam=[
        EQ("State what is meant by the heap property of a min-heap.", 2, [
            MP("Every parent is less than or equal to (smaller than) its children", ["parent", "less than", "smaller", "children", "child", "no larger"]),
            MP("So the smallest item is at the root", ["root", "smallest", "top", "minimum", "lowest"]),
        ], "In a min-heap every parent node is less than or equal to each of its children. This means that the smallest item in the heap is always at the root.",
           command="State"),
        EQ("The array shown holds a min-heap, with the first item at index 0. The value 3 is added to the heap and the heap property is restored by sifting up. Show the contents of the array after the value has been added and the heap property restored.", 4, [
            MP("3 is added at the end of the array (index 6)", ["end", "index 6", "last", "added at"]),
            MP("3 is compared with its parent 4 (index 2) and the two are swapped", ["4", "swap", "parent", "index 2"]),
            MP("3 is compared with its new parent 2 and no swap is needed", ["2", "no swap", "stops", "smaller than 3", "less than 3"]),
            MP("Final array is 2, 5, 3, 9, 7, 8, 4", ["2, 5, 3, 9, 7, 8, 4", "2 5 3 9 7 8 4"]),
        ], "3 is added at the end of the array, at index 6. Its parent is at index (6 - 1) // 2 = 2, which holds 4. Since 3 is less than 4 the two are swapped, so 3 is at index 2 and 4 is at index 6. The parent of index 2 is index 0, which holds 2. Since 2 is less than 3 no further swap is needed. The array is now 2, 5, 3, 9, 7, 8, 4.",
           command="Show",
           figure="""```text
index:  0  1  2  3  4  5
value:  2  5  4  9  7  8
```"""),
        EQ("Explain why a binary heap is a better data structure than a sorted list for implementing a priority queue in which items are frequently added and removed.", 4, [
            MP("Adding to a sorted list means shifting items along to make room, which is O(n)", ["shift", "O(n)", "linear", "move along", "make room"]),
            MP("Adding to a heap is O(log n) because the item only moves up one branch of the tree", ["log n", "O(log n)", "branch", "height", "levels"]),
            MP("Both can find the highest priority item quickly (it is at the front or the root)", ["root", "front", "quickly", "O(1)", "smallest"]),
            MP("A heap only keeps the items partly ordered, so it does less work than keeping every item in order", ["partly", "partially", "less work", "not fully sorted", "does not need to"]),
        ], "In a sorted list a new item has to be put in its correct place, which means shifting every item after it along to make room. This takes O(n) time. In a heap the new item is added at the end and only moves up a single branch of the tree, which is at most log n levels, so adding is O(log n). Both structures can find the highest priority item immediately, since it is at the front of the list or the root of the heap. The heap is quicker overall because it only keeps the items partly ordered, instead of keeping all of them in order.",
           command="Explain"),
        EQ("Write a subprogram find(parent, x) for a disjoint set structure. The list parent holds the parent of each item, and an item that is the root of its group is its own parent. The subprogram must return the root of the group that x belongs to and must use path compression.", 4, [
            MP("Subprogram takes parent and x and returns a root", ["def find", "return", "parent", "root"]),
            MP("Base case or loop end: x is its own parent so it is the root", ["parent[x] == x", "== x", "own parent", "is the root"]),
            MP("Recursive call (or loop) on the parent of x", ["find(parent, parent[x])", "find(", "parent[x]", "while"]),
            MP("Sets parent[x] to the root found (path compression)", ["parent[x] =", "compress", "root", "directly"]),
        ], r"""```python
def find(parent, x):
    if parent[x] != x:
        parent[x] = find(parent, parent[x])
    return parent[x]

parent = [1, 2, 3, 3]
print(find(parent, 0))
print(parent)
```

If x is its own parent it is the root and is returned. Otherwise find is called on the parent of x, and the root it returns is stored in parent[x], so that x now points straight at the root. This is path compression.""",
           command="Write"),
        EQ("A web site offers search suggestions as a user types. Discuss whether a trie or a hash table would be the better structure to hold the dictionary of search terms.", 6, [
            MP("A trie can find every term beginning with the typed prefix by following the letters", ["prefix", "follow", "begin", "starts with", "typed so far"]),
            MP("A hash table can only look up a whole key, so it would have to check every key for a prefix match", ["whole key", "every key", "all keys", "exact", "scan", "O(n)"]),
            MP("The trie lookup time depends on the length of the prefix, not the number of terms", ["length", "not the number", "independent", "regardless"]),
            MP("The trie returns the suggestions in alphabetical order without extra sorting", ["alphabetical", "order", "sorted", "sort"]),
            MP("A trie uses more memory because it has a node for each letter, although shared prefixes are stored once", ["memory", "space", "nodes", "shared", "more"]),
            MP("A reasoned conclusion: a trie is better for suggestions, a hash table for exact matches only", ["conclusion", "trie is better", "better choice", "overall", "therefore", "i would"]),
        ], "A trie is the better choice. As the user types, the program follows the letters typed so far down the trie, and every term in the sub-tree below that point is a suggestion. The time taken depends on the length of the prefix and not on how many terms are stored, and the terms can be produced in alphabetical order without sorting them. A hash table can only look up a whole key, so to find the terms starting with a prefix it would have to check every key, which is O(n) for each keystroke. The trie does use more memory, because it needs a node for every letter, although terms that share a beginning share those nodes. A hash table would only be better if the program needed exact matches, so for search suggestions the trie should be used.",
           command="Discuss"),
    ],
)
