"""A Level Python: linked lists, hash tables, dictionaries and JSON."""
from mskbuild.models import Topic, Section, Q, EQ, MP

INPUTS = {}
EXPECT = {}

TOPIC = Topic(
    slug="linked-lists-and-hash-tables",
    title="Linked Lists and Hash Tables",
    spec="A Level 5",
    icon="i-route",
    minutes=55,
    blurb="Nodes and pointers, in classes and in the array form the exam draws; then hash functions, collisions, chaining and linear probing, and how a Python dictionary is the same idea, finishing with sets and JSON.",
    fact="Python's own dictionary is a hash table, and since Python 3.7 it also remembers the order keys were added. The change came from a redesign that made dictionaries use less memory, and the ordering was a free side effect that was later promised in the language.",
    sections=[
        Section("Linked lists", r"""
An array keeps its items side by side in memory, which makes finding item *n* instant and makes inserting in the middle slow, because everything after the gap has to shuffle along. A **linked list** makes the opposite trade.

Each item is held in a **node**, which has two parts: the **data**, and a **pointer** to the next node. The list is found through a **head** pointer to the first node, and the last node's pointer is **null**, which means "no next node", and which Python writes as `None`.

!diagram py-linked-list

Nodes can be anywhere in memory. The pointers are what put them in order.

```python
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def add_front(self, data):
        node = Node(data)
        node.next = self.head          # the new node points at the old first node
        self.head = node               # and becomes the new head

    def add_end(self, data):
        node = Node(data)
        if self.head is None:
            self.head = node
            return
        current = self.head
        while current.next is not None:
            current = current.next
        current.next = node

    def insert_sorted(self, data):
        node = Node(data)
        if self.head is None or data < self.head.data:
            node.next = self.head
            self.head = node
            return
        current = self.head
        while current.next is not None and current.next.data < data:
            current = current.next
        node.next = current.next        # point the new node onward first
        current.next = node             # then point the previous node at it

    def delete(self, data):
        if self.head is None:
            return False
        if self.head.data == data:
            self.head = self.head.next
            return True
        current = self.head
        while current.next is not None:
            if current.next.data == data:
                current.next = current.next.next      # bypass the node
                return True
            current = current.next
        return False

    def find(self, data):
        current = self.head
        position = 0
        while current is not None:
            if current.data == data:
                return position
            current = current.next
            position += 1
        return -1

    def to_list(self):
        items = []
        current = self.head
        while current is not None:
            items.append(current.data)
            current = current.next
        return items

numbers = LinkedList()
for value in [30, 10, 20]:
    numbers.insert_sorted(value)
numbers.add_front(5)
numbers.add_end(40)
print(numbers.to_list())            # [5, 10, 20, 30, 40]
numbers.delete(20)
print(numbers.to_list())            # [5, 10, 30, 40]
print(numbers.find(30), numbers.find(99))     # 2 -1
```

!warn The order of the two pointer changes matters :: In `insert_sorted`, point the new node at the rest of the list **before** pointing the previous node at the new node. Do it the other way round and the only pointer to the rest of the list is overwritten, so everything after the new node is lost.

### Arrays against linked lists

| | Array | Linked list |
| Access item *n* | Immediate | Walk from the head, one node at a time |
| Insert in the middle | Shift everything after it | Change two pointers |
| Size | Fixed, or copied when it grows | Grows one node at a time |
| Memory | Just the data | Data plus a pointer for every node |
| Search | Binary search, if sorted | Linear search only |

### A linked list in arrays

The exam usually draws a linked list as two arrays, one for the **data** and one for the **next pointers**, with a **head** variable for the list and a **free** variable for the unused places. Index -1 stands for null.

| Index | Data | Next |
| 0 | 17 | 3 |
| 1 | (unused) | 4 |
| 2 | 9 | 0 |
| 3 | 23 | -1 |
| 4 | (unused) | 5 |
| 5 | (unused) | -1 |

With `head = 2`: start at index 2 (9), then its next is 0 (17), then 3 (23), then -1, the end. The list in order is 9, 17, 23. The unused places are linked into a second list of their own: with `free = 1`, they are 1, then 4, then 5.

```python
data = [17, None, 9, 23, None, None]
nxt = [3, 4, 0, -1, 5, -1]
head = 2
free = 1

def places(start):
    found = []
    index = start
    while index != -1:
        found.append(index)
        index = nxt[index]
    return found

print([data[i] for i in places(head)])      # [9, 17, 23]
print(places(free))                         # [1, 4, 5]

# insert 20 after 17 (index 0), using the first free place
new = free
free = nxt[free]                    # the free list moves on to the next unused place
data[new] = 20
nxt[new] = nxt[0]                   # 20 points at what 17 pointed at
nxt[0] = new                        # 17 now points at 20
print([data[i] for i in places(head)], free)      # [9, 17, 20, 23] 4
```

Four assignments and no shuffling. That is the point of a linked list.
"""),
        Section("Hash tables", r"""
To find something in a list you search, which takes time that grows with the length of the list. A **hash table** goes straight to the right place without searching, by **calculating** where the item is stored from the item itself.

A **hash function** turns a **key**, such as a name or a product code, into a number between 0 and the size of the table minus 1. That number is the index where the record is kept, and the same key always gives the same index, so looking it up repeats the calculation.

```python
def hash_key(key, size):
    total = 0
    for ch in key:
        total = total + ord(ch)
    return total % size

for name in ["Asha", "Ben", "Chloe", "Dev"]:
    print(name, "goes in slot", hash_key(name, 7))
```

### A good hash function is

- **deterministic**, giving the same index every time for the same key
- **fast** to calculate
- **uniform**, spreading keys evenly across the table, so that few land in the same place

### Collisions

Two different keys will sometimes give the same index. That is a **collision**, and it cannot be designed away, because there are far more possible keys than slots. A hash table needs a way to cope.

!diagram py-hash-table

**Chaining** keeps a list in every slot, and a colliding key is added to the list.

```python
class ChainedTable:
    def __init__(self, size):
        self.size = size
        self.slots = [[] for _ in range(size)]

    def index(self, key):
        return sum(ord(ch) for ch in key) % self.size

    def put(self, key, value):
        chain = self.slots[self.index(key)]
        for pair in chain:
            if pair[0] == key:
                pair[1] = value
                return
        chain.append([key, value])

    def get(self, key):
        for stored_key, value in self.slots[self.index(key)]:
            if stored_key == key:
                return value
        return None

table = ChainedTable(5)
for name, age in [("Asha", 15), ("Ben", 16), ("Chloe", 15), ("Dev", 17), ("Esme", 16)]:
    table.put(name, age)
print(table.get("Chloe"), table.get("Zoe"))
print([len(chain) for chain in table.slots])
```

**Open addressing with linear probing** keeps one record per slot. When the slot is taken, try the next one, wrapping at the end, and keep going until a free one is found. Looking a key up follows exactly the same path, and stops at an empty slot.

```python
class ProbingTable:
    def __init__(self, size):
        self.keys = [None] * size
        self.values = [None] * size

    def put(self, key, value):
        size = len(self.keys)
        i = key % size
        for step in range(size):
            spot = (i + step) % size
            if self.keys[spot] is None or self.keys[spot] == key:
                self.keys[spot] = key
                self.values[spot] = value
                return spot
        raise OverflowError("the table is full")

    def get(self, key):
        size = len(self.keys)
        i = key % size
        for step in range(size):
            spot = (i + step) % size
            if self.keys[spot] is None:
                return None
            if self.keys[spot] == key:
                return self.values[spot]
        return None

table = ProbingTable(7)
for key in [15, 22, 8, 29]:
    print("key", key, "stored in slot", table.put(key, "record " + str(key)))
print(table.get(8), table.get(36))
```

Each key is 1 more than a multiple of 7, so every one of them hashes to slot 1. They end up in slots 1, 2, 3 and 4, a run of occupied slots called a **cluster**. A long cluster slows every later search that lands in it back towards a linear search.

| | Chaining | Linear probing |
| Where collided items go | In a list at the same slot | In the next free slot |
| Table can hold more items than slots | Yes | No |
| Deleting | Remove from the list | Needs a marker, or later searches stop too early |
| Weakness | Long chains | Clusters |

The **load factor**, the fraction of slots in use, is what decides performance. When it passes about three quarters, real hash tables **rehash**: build a bigger table and re-insert every key, since each key's index depends on the table size.
"""),
        Section("Dictionaries, sets and JSON", r"""
A Python **dictionary** is a hash table. Keys must be **hashable**, which in practice means immutable, because a key that could change after it was stored would no longer be in the slot its hash points to.

```python
# raises: TypeError
lookup = {}
lookup[[1, 2]] = "a list cannot be a key"
```

Lookup, insertion and deletion each take, on average, **constant time**, whatever the size of the dictionary. That is why `key in some_dict` is fast and `value in some_list` is not.

```python
words = "the cat sat on the mat and the cat slept".split()

counts = {}
for word in words:
    counts[word] = counts.get(word, 0) + 1
print(counts)                               # {'the': 3, 'cat': 2, ...}
print(max(counts, key=counts.get))          # the
```

### Sets

A **set** is a hash table with keys and no values. It holds each item at most once, tests membership in constant time, and supports the maths of sets:

```python
a = {1, 2, 3, 4}
b = {3, 4, 5}
print(a | b, a & b, a - b, a ^ b)     # union, intersection, difference, symmetric difference
print(3 in a, 9 in a)
print(len(set([4, 4, 7, 7, 7])))      # 2, which is a quick way to remove duplicates
```

### JSON

Programs exchange data as text. **JSON** writes dictionaries, lists, strings, numbers and Booleans in a form that every language reads, and a Python dictionary becomes JSON almost word for word.

```python
import json

record = {"name": "Asha", "year": 12, "subjects": ["Computing", "Maths"], "prefect": True}

text = json.dumps(record)
print(text)

back = json.loads(text)
print(back["subjects"][0], back == record)
```

`dumps` turns the dictionary into a string, and `loads` rebuilds the dictionary from that string. Note that `True` became `true`, which is how JSON writes a Boolean.

!exam Hash table questions are worked examples :: Show the calculation, such as 22 MOD 7 = 1, state that slot 1 is occupied, and say where the key goes next. The method mark is for showing the collision being resolved, not just the final slot.
"""),
    ],
    keyterms=[
        ("Linked list", "A data structure of nodes, each holding data and a pointer to the next node, reached through a head pointer."),
        ("Node", "One element of a linked list, tree or graph, holding data and one or more pointers."),
        ("Pointer", "A value that gives the location of another item, such as the next node in a linked list."),
        ("Null pointer", "A pointer that points to nothing, marking the end of a linked list."),
        ("Hash function", "A function that turns a key into an index in a hash table."),
        ("Hash table", "A data structure that stores each record at an index calculated from its key, giving fast lookup."),
        ("Collision", "When two different keys produce the same index from the hash function."),
        ("Chaining", "Resolving collisions by keeping a list of the items in each slot."),
        ("Linear probing", "Resolving collisions by trying the next slot, and the next, until a free one is found."),
        ("Load factor", "The proportion of a hash table's slots that are in use."),
        ("JSON", "A text format for exchanging data, built from objects, arrays, strings, numbers and Booleans."),
    ],
    grade="""
These are structures you are expected to draw, trace and code. Top marks come from showing the pointers.

+ When inserting into a linked list, name every pointer that changes, in the order it changes
+ Give the cost of each operation for an array and for a linked list, and the reason
+ In a hash table question, write the calculation for each key before saying which slot it goes in
+ Say that a collision is when two keys give the same index, and name the method of dealing with it
+ Explain why the hash function must be deterministic and spread keys evenly
""",
    mistakes=[
        "Changing the pointer of the previous node before saving where it pointed, so the rest of the list is lost.",
        "Treating a linked list as having direct access to item n.",
        "Forgetting the null pointer at the end of the list, so the traversal never stops.",
        "Saying a good hash function avoids all collisions, when no function can.",
        "Using a changeable object, such as a list, as a dictionary key.",
    ],
    quiz=[
        Q("What does each node of a singly linked list contain?",
          ["Data and a pointer to the next node", "Data and its index", "Two copies of the data",
           "A pointer to the head only"], 0,
          "The data is the item stored, and the pointer is what links the nodes in order."),
        Q("Which is an advantage of a linked list over an array?",
          ["Items can be inserted in the middle without shifting other items", "Any item can be reached immediately",
           "It uses less memory", "It can be searched using a binary search"], 0,
          "Inserting only needs two pointers to change. In an array every item after the gap has to move."),
        Q("Which is a disadvantage of a linked list compared with an array?",
          ["Reaching an item means following the pointers from the head of the list",
           "It cannot grow, because the number of nodes is fixed when it is created",
           "It can only hold numbers, because each node needs a numeric pointer",
           "It has to be sorted before any item can be inserted or deleted"], 0,
          "There is no index to jump to, so reaching item n takes n steps."),
        Q("What does the pointer of the last node of a linked list hold?",
          ["Null, meaning there is no next node", "The address of the head", "The number of nodes", "The data of the first node"], 0,
          "Null, written None in Python, is what tells a traversal that it has reached the end."),
        Q("What is the purpose of a hash function?",
          ["To turn a key into an index in the table", "To sort the keys", "To encrypt the key so it cannot be read",
           "To count how many keys are stored"], 0,
          "It calculates where a record belongs, so it can be found again without searching."),
        Q("What is a collision in a hash table?",
          ["Two different keys producing the same index", "The table running out of memory", "A key being deleted twice",
           "A hash function returning a negative number"], 0,
          "Collisions are unavoidable, because there are many more possible keys than slots."),
        Q("How does chaining deal with a collision?",
          ["Each slot holds a list, and the colliding key is added to that list",
           "The new key overwrites the old one, which is then lost from the table",
           "The whole table is deleted and rebuilt from the beginning each time",
           "The key is rejected with an error and the program stops running"], 0,
          "Several keys can share a slot because each slot holds a list of the records that hashed there."),
        Q("How does linear probing deal with a collision?",
          ["It tries the next slot, and the next, until a free one is found", "It searches the table for the oldest key and removes it",
           "It uses a second hash function on every key", "It waits until a slot becomes free"], 0,
          "The table wraps round at the end, and a lookup follows the same path from the same starting slot."),
        Q("What is the average time to look up a key in a good hash table as the table grows?",
          ["Constant, it does not depend on the number of items", "Proportional to the number of items",
           "Proportional to the logarithm of the number of items", "Proportional to the square of the number of items"], 0,
          "The index is calculated directly. Only a lot of collisions slow it down."),
        Q("Why can a Python list not be used as a dictionary key?",
          ["It is mutable, so its hash could change after it had been stored",
           "It is too long, and keys are limited to a fixed number of items",
           "It cannot contain numbers, which every key is required to use",
           "It is not sorted, so the table cannot work out where to put it"], 0,
          "A key must have a hash that never changes, which means the key itself must be immutable."),
    ],
    exam=[
        EQ("Describe one advantage and one disadvantage of storing a list of items in a linked list rather than in an array.", 3, [
            MP("Advantage: an item can be inserted or deleted by changing pointers, without shifting other items", ["insert", "delete", "pointers", "without shifting", "no shifting", "change pointers"]),
            MP("Advantage: the list can grow and shrink one node at a time, so no size has to be fixed", ["grow", "shrink", "dynamic", "size", "fixed", "one node"]),
            MP("Disadvantage: items cannot be accessed directly by index, so each one must be reached by following pointers from the head", ["directly", "index", "traverse", "follow", "from the head", "slower", "search"]),
            MP("Disadvantage: each node needs extra memory for a pointer", ["extra memory", "more memory", "pointer takes", "space for the pointer"]),
        ], "An advantage is that an item can be inserted or removed by changing a couple of pointers, without shifting all the other items along as an array would need to. A disadvantage is that items cannot be accessed directly by their position, so to reach the fifth item the program must follow the pointers from the head through the four nodes before it.",
           command="Describe"),
        EQ("The linked list shown is held in two arrays. The head pointer is 2, the free pointer is 1, and -1 indicates the end of a list. State the items in the list, in order. A new item, 20, is to be stored so that it comes between 17 and 23, using the first free location. State the value that must be stored in each of data[1] and next[1], the change that must be made to next[0], and the new value of the free pointer.", 5, [
            MP("The items in order are 9, 17, 23", ["9, 17, 23", "9 17 23"]),
            MP("data[1] is 20", ["data[1] = 20", "data[1]", "20"]),
            MP("next[1] is 3, the old pointer of 17", ["next[1] = 3", "3"]),
            MP("next[0] is changed to 1", ["next[0] = 1", "1"]),
            MP("The free pointer moves on to 4", ["free = 4", "free pointer", "4"]),
        ], "Starting at head 2 gives 9, whose pointer is 0, which gives 17, whose pointer is 3, which gives 23, whose pointer is -1. The items in order are 9, 17, 23. To insert 20, the first free location is index 1, so data[1] is set to 20, and next[1] is set to 3, which is what 17 currently points at. Then next[0] is changed to 1 so that 17 now points at the new item, and the free pointer moves on to 4, the next unused place. If next[0] were changed first, the pointer to 23 would be lost.",
           command="State",
           figure="""| Index | data | next |
| 0 | 17 | 3 |
| 1 | (unused) | 4 |
| 2 | 9 | 0 |
| 3 | 23 | -1 |
| 4 | (unused) | 5 |
| 5 | (unused) | -1 |"""),
        EQ("The hash function for a hash table of size 7 is the key MOD 7, and a collision is resolved by linear probing, moving to the next slot and wrapping from slot 6 to slot 0. The table is empty. Show where the keys 15, 22, 8 and 29 are stored, if they are added in that order.", 4, [
            MP("15 is stored in slot 1, because 15 MOD 7 is 1", ["slot 1", "15 mod 7", "1"]),
            MP("22 hashes to slot 1, which is taken, so it is stored in slot 2", ["slot 2", "22"]),
            MP("8 hashes to slot 1, and slots 1 and 2 are taken, so it is stored in slot 3", ["slot 3", "8"]),
            MP("29 hashes to slot 1, and slots 1, 2 and 3 are taken, so it is stored in slot 4", ["slot 4", "29"]),
        ], "15 MOD 7 is 1, so 15 goes in slot 1. 22 MOD 7 is also 1, which is occupied, so linear probing moves on and 22 is stored in slot 2. 8 MOD 7 is 1, and slots 1 and 2 are occupied, so 8 goes in slot 3. 29 MOD 7 is 1 as well, and slots 1, 2 and 3 are occupied, so 29 is stored in slot 4.",
           command="Show"),
        EQ("Explain how a hash table stores and retrieves a record, and describe one way of dealing with collisions.", 6, [
            MP("A hash function is applied to the key of the record", ["hash function", "applied to the key", "key", "calculates"]),
            MP("The result is used as the index of the position in the table where the record is stored", ["index", "position", "slot", "location", "address"]),
            MP("To retrieve it, the same hash function is applied to the key, so the position is found directly without searching", ["same hash", "same function", "directly", "without searching", "retrieve", "recalculat"]),
            MP("A collision occurs when two keys give the same index", ["collision", "same index", "same position", "same slot"]),
            MP("In chaining, each position holds a list of the records that hash to it, and a new record is added to that list", ["chaining", "list", "chain", "linked list"]),
            MP("Alternatively with linear probing the next free slot is used, and a lookup follows the same sequence until it finds the key or an empty slot", ["probing", "next free", "next slot", "open addressing", "empty slot", "same sequence"]),
        ], "To store a record, a hash function is applied to its key, and the result is used as the index of the position in the table where the record is kept. To retrieve it, the same hash function is applied to the key again, which gives the position directly, so there is no need to search through the other records. A collision happens when two keys produce the same index. With chaining, each position in the table holds a list of all the records that hash to it, and a new record is added to the end of that list, so a lookup calculates the position and then searches the short list. With linear probing, the record is instead put in the next free slot, and a lookup follows the same sequence of slots until it finds the key or reaches an empty slot.",
           command="Explain"),
        EQ("A linked list is made of nodes. Each node has the attributes data and next, and next is None for the last node. Write a Python function called count_nodes that takes the first node, called head, of a linked list and returns the number of nodes in the list.", 4, [
            MP("Defines a function with the head as a parameter", ["def count_nodes", "def", "head"]),
            MP("A counter that starts at 0", ["count = 0", "= 0", "counter"]),
            MP("A loop that moves to the next node until the end, which is None", ["while", "is not none", "!= none", "current", "is None"]),
            MP("Counts each node and returns the result", ["+= 1", "+ 1", "return count", "return"]),
        ], r"""```python
class Node:
    def __init__(self, data, next=None):
        self.data = data
        self.next = next

def count_nodes(head):
    count = 0
    current = head
    while current is not None:
        count = count + 1
        current = current.next
    return count

print(count_nodes(Node(4, Node(8, Node(15)))), count_nodes(None))
```

The function follows the next pointers from the head, adding one to the counter for each node, and stops when the pointer is None. An empty list, with a head of None, gives 0. The calls shown print 3 0.""",
           command="Write"),
    ],
)
