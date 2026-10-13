"""A Level Python: binary trees, graphs and how to traverse them."""
from mskbuild.models import Topic, Section, Q, EQ, MP

INPUTS = {}
EXPECT = {}

TOPIC = Topic(
    slug="trees-and-graphs",
    title="Trees and Graphs",
    spec="A Level 6",
    icon="i-network",
    minutes=60,
    blurb="Binary search trees with insert, search, delete and the three traversals; graphs held as matrices and lists; and breadth first against depth first search, each written and run on a small example you can follow by hand.",
    fact="Every file system you have used is a tree: one root, with folders inside folders. The web is a graph, because pages link to each other in loops. Google's first ranking idea, PageRank, was a calculation over that graph of links.",
    sections=[
        Section("Binary trees and binary search trees", r"""
A **tree** is a data structure of **nodes** joined by **edges**, with one special node at the top, the **root**, and no loops. Each node can have child nodes below it. A node with no children is a **leaf**. Any node and everything below it is a **subtree**.

A **binary tree** allows each node **at most two** children, a **left** and a **right**. A **binary search tree** (BST) adds a rule that makes searching fast:

!key The BST rule :: For every node, everything in its **left** subtree is **smaller** and everything in its **right** subtree is **larger**.

!diagram py-bst

Searching follows the rule. At each node, compare: if the target is smaller go left, if larger go right, and stop when you find it or run out of tree. Each step discards a whole subtree, which is why a balanced tree of a million nodes needs only about twenty comparisons.

```python
class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def insert(node, value):
    if node is None:
        return TreeNode(value)
    if value < node.value:
        node.left = insert(node.left, value)
    elif value > node.value:
        node.right = insert(node.right, value)
    return node

def contains(node, value):
    while node is not None:
        if value == node.value:
            return True
        if value < node.value:
            node = node.left
        else:
            node = node.right
    return False

root = None
for value in [50, 30, 70, 20, 40, 60, 80, 35]:
    root = insert(root, value)

print(contains(root, 35), contains(root, 65))      # True False
```

### Three ways to visit every node

A **traversal** visits every node exactly once. The three depth first orders differ only in **when the node itself is visited**, relative to its two subtrees.

| Traversal | Order | For the tree above | Use |
| Pre-order | root, left, right | 50 30 20 40 35 70 60 80 | Copying a tree |
| **In-order** | left, root, right | 20 30 35 40 50 60 70 80 | Reading a BST **in sorted order** |
| Post-order | left, right, root | 20 35 40 30 60 80 70 50 | Deleting a tree, and postfix expressions |

```python
class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def insert(node, value):
    if node is None:
        return TreeNode(value)
    if value < node.value:
        node.left = insert(node.left, value)
    elif value > node.value:
        node.right = insert(node.right, value)
    return node

def pre_order(node):
    if node is None:
        return []
    return [node.value] + pre_order(node.left) + pre_order(node.right)

def in_order(node):
    if node is None:
        return []
    return in_order(node.left) + [node.value] + in_order(node.right)

def post_order(node):
    if node is None:
        return []
    return post_order(node.left) + post_order(node.right) + [node.value]

def height(node):
    if node is None:
        return 0
    return 1 + max(height(node.left), height(node.right))

root = None
for value in [50, 30, 70, 20, 40, 60, 80, 35]:
    root = insert(root, value)

print(pre_order(root))
print(in_order(root))
print(post_order(root))
print("height", height(root))
```

The in-order result is sorted, which is the whole point of the structure: **inserting into a BST and reading it in order sorts the data**.

### Deleting a node

There are three cases, and the third is the one that needs thought.

| The node has | Do |
| No children | Remove it |
| One child | Replace it with that child |
| Two children | Replace its value with its **in-order successor**, the smallest value in its right subtree, and delete that node instead |

```python
class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def insert(node, value):
    if node is None:
        return TreeNode(value)
    if value < node.value:
        node.left = insert(node.left, value)
    elif value > node.value:
        node.right = insert(node.right, value)
    return node

def in_order(node):
    if node is None:
        return []
    return in_order(node.left) + [node.value] + in_order(node.right)

def delete(node, value):
    if node is None:
        return None
    if value < node.value:
        node.left = delete(node.left, value)
    elif value > node.value:
        node.right = delete(node.right, value)
    else:
        if node.left is None:
            return node.right
        if node.right is None:
            return node.left
        successor = node.right
        while successor.left is not None:
            successor = successor.left
        node.value = successor.value
        node.right = delete(node.right, successor.value)
    return node

root = None
for value in [50, 30, 70, 20, 40, 60, 80, 35]:
    root = insert(root, value)

root = delete(root, 20)          # a leaf
root = delete(root, 40)          # a node with one child, 35
root = delete(root, 50)          # the root, which has two children
print(in_order(root), root.value)
```

Deleting the root, 50, leaves a gap that is filled by 60: the smallest value in the right subtree, and the only value that keeps everything on its left smaller and everything on its right larger.

### The tree must stay balanced

A search is fast only if the tree is **balanced**, with its two sides about the same height. Add already sorted data and every value is larger than the last, so every node goes to the right and the tree becomes a **linked list** with a search time proportional to the number of nodes.

```python
class TreeNode:
    def __init__(self, value):
        self.value = value
        self.left = None
        self.right = None

def insert(node, value):
    if node is None:
        return TreeNode(value)
    if value < node.value:
        node.left = insert(node.left, value)
    else:
        node.right = insert(node.right, value)
    return node

def height(node):
    if node is None:
        return 0
    return 1 + max(height(node.left), height(node.right))

sorted_order = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
balanced_order = [8, 4, 12, 2, 6, 10, 14, 1, 3, 5, 7, 9, 11, 13, 15]

for name, order in [("sorted", sorted_order), ("balanced", balanced_order)]:
    root = None
    for value in order:
        root = insert(root, value)
    print(name, "order gives a tree of height", height(root))
```

The same fifteen values, two different heights. Real systems use **self balancing** trees that rearrange themselves as they grow, so the worst case never happens.

### An expression tree

A tree can hold an arithmetic expression, with operators in the inner nodes and numbers in the leaves. Evaluating it is recursion, and a **post-order** traversal gives Reverse Polish notation.

```python
tree = ("*", ("+", 3, 4), 2)

def evaluate(node):
    if isinstance(node, tuple):
        operator, left, right = node
        a = evaluate(left)
        b = evaluate(right)
        if operator == "+":
            return a + b
        if operator == "-":
            return a - b
        if operator == "*":
            return a * b
        return a / b
    return node

def postfix(node):
    if isinstance(node, tuple):
        operator, left, right = node
        return postfix(left) + " " + postfix(right) + " " + operator
    return str(node)

print(evaluate(tree), postfix(tree))
```
"""),
        Section("Graphs", r"""
A **graph** is a set of **vertices** (nodes) joined by **edges** (arcs). Where a tree must have a root and no loops, a graph can connect anything to anything. A tree is simply a connected graph with no cycles.

| Term | Meaning |
| **Directed** | Edges have a direction, like one way streets or "follows" |
| **Undirected** | Edges go both ways, like friendships |
| **Weighted** | Each edge has a value, such as a distance or a cost |
| **Path** | A sequence of edges from one vertex to another |
| **Cycle** | A path that returns to where it started |
| **Connected** | There is a path between every pair of vertices |
| **Degree** | The number of edges meeting a vertex |

Graphs model anything that is a set of things with relationships between them: roads and junctions, network cables and routers, people and friendships, web pages and links, tasks and the order they depend on.

### Storing a graph

The graph used through the rest of this topic has six vertices and seven edges:

```text
A --- B
|     |
C --- D --- F
|           |
E ----------+
```

**An adjacency matrix** is a table with a row and a column for every vertex. A 1 in row *X*, column *Y* means there is an edge between them.

**An adjacency list** stores, for every vertex, only the vertices it is joined to.

```python
vertices = ["A", "B", "C", "D", "E", "F"]
edges = [("A", "B"), ("A", "C"), ("B", "D"), ("C", "D"),
         ("C", "E"), ("D", "F"), ("E", "F")]

matrix = [[0] * 6 for _ in range(6)]
adjacency = {v: [] for v in vertices}
for a, b in edges:
    matrix[vertices.index(a)][vertices.index(b)] = 1
    matrix[vertices.index(b)][vertices.index(a)] = 1
    adjacency[a].append(b)
    adjacency[b].append(a)

print("  ", " ".join(vertices))
for v, row in zip(vertices, matrix):
    print(v, "", " ".join(str(x) for x in row))
print(adjacency)
print({v: len(adjacency[v]) for v in vertices})      # the degree of each vertex
```

An undirected graph's matrix is **symmetric**: the table is the same flipped over its diagonal. The degree of a vertex is the sum of its row.

| | Adjacency matrix | Adjacency list |
| Memory | One cell for every pair of vertices: V times V | One entry per edge: V plus E |
| Is there an edge between X and Y? | Immediate | Search X's list |
| List all the neighbours of X | Scan a whole row | Read X's list |
| Best for | **Dense** graphs, with many edges | **Sparse** graphs, with few |

A road network of a million junctions, where each junction meets about four roads, would need a matrix of a million million cells and a list of about four million entries. Almost every real graph is sparse.
"""),
        Section("Breadth first and depth first traversal", r"""
Visiting every vertex of a graph needs a rule for **what to visit next**, and one more thing a tree does not need: a record of the vertices **already visited**, because a graph can loop back and a traversal that forgets would go round forever.

!diagram py-graph-traversal

### Depth first: go as deep as you can

Follow one path until it runs out, then **back up** to the last place with an unexplored branch. A **stack** does the backing up, and recursion is a stack in disguise.

```python
adjacency = {"A": ["B", "C"], "B": ["A", "D"], "C": ["A", "D", "E"],
             "D": ["B", "C", "F"], "E": ["C", "F"], "F": ["D", "E"]}

def depth_first(graph, vertex, visited=None):
    if visited is None:
        visited = []
    visited.append(vertex)
    for neighbour in graph[vertex]:
        if neighbour not in visited:
            depth_first(graph, neighbour, visited)
    return visited

def depth_first_stack(graph, start):
    visited = []
    stack = [start]
    while stack:
        vertex = stack.pop()
        if vertex not in visited:
            visited.append(vertex)
            for neighbour in reversed(graph[vertex]):
                stack.append(neighbour)
    return visited

print(depth_first(adjacency, "A"))
print(depth_first_stack(adjacency, "A"))
```

### Breadth first: all the neighbours first

Visit the start, then everything one step away, then everything two steps away. Each **ring** is finished before the next begins. A **queue** keeps the order.

```python
from collections import deque

adjacency = {"A": ["B", "C"], "B": ["A", "D"], "C": ["A", "D", "E"],
             "D": ["B", "C", "F"], "E": ["C", "F"], "F": ["D", "E"]}

def breadth_first(graph, start):
    visited = [start]
    queue = deque([start])
    while queue:
        vertex = queue.popleft()
        for neighbour in graph[vertex]:
            if neighbour not in visited:
                visited.append(neighbour)
                queue.append(neighbour)
    return visited

print(breadth_first(adjacency, "A"))
```

### Shortest path in an unweighted graph

Because breadth first search finishes every vertex one step away before any that is two steps away, the **first** time it reaches a vertex is by a **shortest route** (fewest edges). Remembering where each vertex was reached from lets you read the path back.

```python
from collections import deque

adjacency = {"A": ["B", "C"], "B": ["A", "D"], "C": ["A", "D", "E"],
             "D": ["B", "C", "F"], "E": ["C", "F"], "F": ["D", "E"]}

def shortest_path(graph, start, goal):
    came_from = {start: None}
    queue = deque([start])
    while queue:
        vertex = queue.popleft()
        if vertex == goal:
            break
        for neighbour in graph[vertex]:
            if neighbour not in came_from:
                came_from[neighbour] = vertex
                queue.append(neighbour)
    if goal not in came_from:
        return None
    path = []
    while goal is not None:
        path.append(goal)
        goal = came_from[goal]
    return path[::-1]

print(shortest_path(adjacency, "A", "F"))
```

### Choosing between them

| | Depth first | Breadth first |
| Keeps its place with | A stack, or recursion | A queue |
| Explores | One branch to its end, then backs up | All vertices one step away, then two |
| Finds the shortest path (fewest edges) | No | **Yes** |
| Memory | Proportional to the longest path | Proportional to the widest level |
| Typical use | Does a path exist, finding cycles, solving mazes, ordering tasks | Fewest hops, social network distance, web crawling |

!exam Traversal questions are traces :: State the data structure, then write the order the vertices are visited and, at each step, the contents of the stack or queue. If two neighbours are possible, take them in the order the question gives, usually alphabetical. A change of that order changes the answer.
"""),
    ],
    keyterms=[
        ("Tree", "A connected data structure of nodes and edges with a single root and no cycles."),
        ("Binary search tree", "A binary tree in which every node's left subtree holds smaller values and its right subtree holds larger values."),
        ("Root", "The node at the top of a tree, which has no parent."),
        ("Leaf", "A node of a tree that has no children."),
        ("Traversal", "Visiting every node of a data structure exactly once in a defined order."),
        ("In-order traversal", "Visiting the left subtree, then the node, then the right subtree. For a binary search tree this gives sorted order."),
        ("Graph", "A set of vertices joined by edges, which may be directed or undirected, weighted or unweighted."),
        ("Adjacency matrix", "A table with a row and column for each vertex, with 1, or the weight, where there is an edge."),
        ("Adjacency list", "A record, for each vertex, of the vertices it is joined to."),
        ("Breadth first search", "A traversal that visits all vertices one step from the start, then two steps away, using a queue."),
        ("Depth first search", "A traversal that follows one path as far as possible before backing up, using a stack or recursion."),
    ],
    grade="""
Trees and graphs are always examined as a trace, a drawing and a comparison, so practise all three by hand.

+ Apply the BST rule at every node as you insert: smaller left, larger right
+ Write each traversal as its rule first, and then the order of nodes, for the same tree
+ Say that in-order traversal of a binary search tree returns the values in sorted order
+ Justify matrix against list with the graph's density: dense graphs suit a matrix, sparse ones a list
+ Name the data structure behind each traversal, and why, when asked to trace breadth first or depth first
""",
    mistakes=[
        "Putting a smaller value on the right of its parent when drawing a binary search tree.",
        "Mixing up pre-order, in-order and post-order, which differ only in where the root goes.",
        "Forgetting to record visited vertices, so the traversal of a graph with a cycle never ends.",
        "Saying depth first search finds the shortest path.",
        "Choosing an adjacency matrix for a large sparse graph, where it wastes most of its memory.",
    ],
    quiz=[
        Q("What is the rule that defines a binary search tree?",
          ["Each node's left subtree holds smaller values and its right subtree holds larger values",
           "Each node has exactly two children, and the leaves are all at the same depth",
           "Each node's value is larger than both of its children's values",
           "Each node's value is the sum of the values in its two subtrees"], 0,
          "This rule is what lets a search discard a whole subtree at each comparison."),
        Q("What is a leaf in a tree?",
          ["A node that has no children", "The node at the top of the tree", "A node that has exactly one child",
           "An edge that joins two nodes"], 0,
          "The root is at the top and the leaves are at the bottom, where the branches end."),
        Q("What does an in-order traversal of a binary search tree produce?",
          ["The values in ascending order", "The values in the order they were inserted",
           "The values in descending order", "The root followed by the leaves"], 0,
          "Left subtree, then node, then right subtree, visits the smaller values before the larger at every level."),
        Q("Which traversal visits the root first, then the left subtree, then the right subtree?",
          ["Pre-order", "In-order", "Post-order", "Breadth first"], 0,
          "The name tells you where the root goes: before its subtrees."),
        Q("What is the worst case for searching an unbalanced binary search tree of n nodes?",
          ["Every node may have to be visited, so the time is proportional to n", "Only one node has to be visited",
           "The time is proportional to the logarithm of n", "The search can never succeed"], 0,
          "If the data was inserted in sorted order the tree is a long chain, which is no better than a linked list."),
        Q("What is the difference between a tree and a graph?",
          ["A tree is a connected graph with no cycles and a single root", "A tree has weighted edges and a graph has not",
           "A graph can only be stored as a matrix", "A tree has no edges"], 0,
          "A tree is a special case of a graph, where there is exactly one path between any two nodes."),
        Q("What does the weight of an edge in a weighted graph represent?",
          ["A value such as a distance or a cost", "The number of edges joined to a vertex", "The direction of the edge",
           "The order in which the edge was added"], 0,
          "Weights let a graph model real distances, times or prices, which shortest path algorithms use."),
        Q("How many cells does an adjacency matrix for a graph with 100 vertices have?",
          ["10 000", "100", "200", "1 000"], 0,
          "A matrix has a row and a column for every vertex, so 100 times 100 cells, however few edges there are."),
        Q("Which data structure does a breadth first traversal use to hold the vertices still to be visited?",
          ["A queue", "A stack", "A binary tree", "A hash table"], 0,
          "A queue visits vertices in the order they were discovered, which finishes each ring before the next."),
        Q("Which traversal can be written with recursion, or with an explicit stack?",
          ["Depth first", "Breadth first", "Neither", "Both of them equally"], 0,
          "Recursion uses the call stack to back up, and an explicit stack does the same job in a loop."),
    ],
    exam=[
        EQ("A binary search tree is built by adding the values 40, 25, 60, 10, 30, 50, 70 in that order to an empty tree. State the order in which the values are visited by an in-order traversal, and by a post-order traversal.", 4, [
            MP("In-order: 10, 25, 30, 40, 50, 60, 70", ["10, 25, 30, 40, 50, 60, 70", "10 25 30 40 50 60 70"]),
            MP("The in-order traversal is in ascending order", ["ascending", "sorted", "order"]),
            MP("Post-order: 10, 30, 25, 50, 70, 60, 40", ["10, 30, 25, 50, 70, 60, 40", "10 30 25 50 70 60 40"]),
            MP("In post-order each node is visited after both of its subtrees, so the root 40 is last", ["root is last", "last", "after", "40 last"]),
        ], "The tree has 40 as the root, 25 and 60 as its children, 10 and 30 under 25, and 50 and 70 under 60. An in-order traversal visits the left subtree, the node, then the right subtree, which gives 10, 25, 30, 40, 50, 60, 70, the values in ascending order. A post-order traversal visits the left subtree, the right subtree and then the node, which gives 10, 30, 25, 50, 70, 60, 40, with the root last.",
           command="State"),
        EQ("Write a recursive Python function called count_nodes that takes the root of a binary tree and returns the number of nodes in it. An empty tree is represented by None, and each node has the attributes left and right.", 4, [
            MP("Defines a function with the node as a parameter", ["def count_nodes", "def", "node"]),
            MP("Base case: an empty tree has 0 nodes", ["is none", "== none", "return 0", "base case"]),
            MP("Recursive case: counts the left subtree and the right subtree", ["count_nodes(node.left)", "count_nodes(node.right)", "left", "right"]),
            MP("Adds 1 for the current node and returns the total", ["1 +", "+ 1", "return 1", "return"]),
        ], r"""```python
class Node:
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right

def count_nodes(node):
    if node is None:
        return 0
    return 1 + count_nodes(node.left) + count_nodes(node.right)

tree = Node(Node(Node(), None), Node())
print(count_nodes(tree), count_nodes(None))
```

The base case is an empty tree, which has no nodes. Otherwise the answer is one for this node plus the number of nodes in each subtree. The calls shown print 4 and 0.""",
           command="Write"),
        EQ("A graph has 1 000 vertices and 2 000 edges. Compare using an adjacency matrix and an adjacency list to store it.", 4, [
            MP("A matrix needs 1 000 times 1 000, which is 1 000 000, cells", ["1 000 000", "1000000", "million", "1000 x 1000", "1000 * 1000"]),
            MP("Most of the cells would be 0, so the matrix wastes memory for a sparse graph", ["wastes", "mostly 0", "mostly empty", "sparse", "zeros"]),
            MP("An adjacency list needs entries only for the edges and so uses far less memory", ["only for the edges", "fewer", "far less", "less memory", "4 000", "proportional to the edges"]),
            MP("A matrix tells you whether two vertices are joined immediately, whereas a list must be searched", ["immediately", "quickly", "directly", "instant", "searched", "constant", "faster to check"]),
        ], "An adjacency matrix would need a cell for every pair of vertices, 1 000 times 1 000, which is 1 000 000 cells, and with only 2 000 edges almost all of them would be 0. This graph is sparse, so the matrix wastes a lot of memory. An adjacency list stores only the edges, about 4 000 entries as each edge appears for two vertices, so it uses far less memory. The one advantage of the matrix is that it tells you if two vertices are joined immediately, whereas with the list the neighbours of one vertex must be searched. For this graph the list is the better choice.",
           command="Compare"),
        EQ("The graph shown is stored as an adjacency list. Neighbours are always taken in alphabetical order. State the order in which the vertices are visited by a breadth first traversal starting at A, and by a depth first traversal starting at A.", 4, [
            MP("Breadth first: A, B, C, D, E, F", ["a, b, c, d, e, f", "a b c d e f"]),
            MP("The breadth first traversal uses a queue", ["queue"]),
            MP("Depth first: A, B, D, C, E, F", ["a, b, d, c, e, f", "a b d c e f"]),
            MP("The depth first traversal uses a stack or recursion, going as deep as possible before backing up", ["stack", "recursion", "deep", "back"]),
        ], "A breadth first traversal visits A, then the neighbours of A, B and C, then the unvisited neighbours of B and C, which are D and E, and finally F, so the order is A, B, C, D, E, F. It uses a queue. A depth first traversal goes from A to B, then from B to D, from D to C, from C to E and from E to F, so the order is A, B, D, C, E, F. It uses a stack, or recursion, and goes as deep as it can before backing up.",
           command="State",
           figure="""| Vertex | Neighbours |
| A | B, C |
| B | A, D |
| C | A, D, E |
| D | B, C, F |
| E | C, F |
| F | D, E |"""),
        EQ("Explain why a binary search tree that is built from a list of values that was already in order is not efficient to search, and describe how this problem can be avoided.", 4, [
            MP("Each new value is larger than the one before, so it is always added to the right", ["always right", "right", "larger", "one side", "same side"]),
            MP("The tree becomes a long chain, like a linked list", ["chain", "linked list", "line", "unbalanced", "degenerate"]),
            MP("A search may then have to visit every node, so it takes time proportional to the number of nodes instead of the logarithm", ["every node", "all the nodes", "n comparisons", "proportional", "linear", "slow", "o(n)"]),
            MP("It can be avoided by keeping the tree balanced, such as using a self balancing tree, or by inserting values in a random or median first order", ["balanced", "self balancing", "random", "median", "rebalance", "avl", "red black"]),
        ], "If the values arrive in order, each new value is larger than all those already in the tree, so it is always added on the right and the tree becomes a long chain, no better than a linked list. A search may then need to visit every node, so the time is proportional to the number of nodes rather than to the logarithm of the number of nodes. The problem can be avoided by keeping the tree balanced, for example by using a self balancing tree that rearranges itself as values are added, or by inserting the values in a random order or middle value first.",
           command="Explain"),
    ],
)
