"""Advanced Python: names, objects, mutability, copying and memory."""
from mskbuild.models import Topic, Section, Q, EQ, MP

INPUTS = {}
EXPECT = {}

TOPIC = Topic(
    slug="names-objects-and-memory",
    title="Names, Objects and Memory",
    spec="Advanced 1",
    icon="i-memory",
    minutes=55,
    blurb="What a Python variable really is: a name tied to an object. Identity against equality, mutable against immutable, the default argument trap, aliases, shallow and deep copies, how arguments are passed, and how Python frees memory with reference counting and a garbage collector.",
    fact="The default argument trap is so well known that Python programmers call it the 'mutable default'. It has surprised beginners and experts since the 1990s, and every serious Python code checker warns about it. Understanding why it happens is the quickest route to understanding how Python really works.",
    sections=[
        Section("Variables are names, not boxes", r"""
In many languages a variable is a **box** that holds a value. In Python it is closer to a **label** attached to an object. The object lives in memory, and a name is just a way of finding it. Assignment does not copy anything. It attaches a name.

```python
a = [1, 2, 3]
b = a                     # no copy: b is a second name for the same list
b.append(4)

print(a)                  # the change shows up under both names
print(a is b)             # True: one object with two names

c = [1, 2, 3, 4]
print(a == c)             # True: the values are equal
print(a is c)             # False: but they are two different objects
```

Two operators answer two different questions:

| Operator | Asks | Example |
| `==` | do the two objects have **equal values**? | `[1, 2] == [1, 2]` is `True` |
| `is` | are the two names bound to the **very same object**? | `[1, 2] is [1, 2]` is `False` |

Use `==` to compare values. Use `is` only to check for `None` (`if x is None:`), because there is only ever one `None`.

### Rebinding is not mutating

These two lines look the same and behave differently. Adding with `+` builds a **new** list and rebinds `a` to it. The shorthand `+=` on a list **changes the existing list**, so every name for it sees the change.

```python
a = [1, 2]
b = a
a = a + [3]               # a new list is made, and the name a is moved to it
print(a, b)

a = [1, 2]
b = a
a += [3]                  # the same list is extended in place
print(a, b)
```

### Some objects can never change

An **immutable** object cannot be altered after it is made. Numbers, strings and tuples are immutable, so something that looks like a change always makes a **new** object and rebinds the name:

```python
s = "cat"
t = s
s += "s"                  # builds a new string "cats"; the old one is untouched
print(s, t)
```

That is why `t` is still `cat`. With a list, both names would have seen the change.

!key Where things live :: Names live in the scope of a function or module: its stack frame. Objects live on the **heap**. A name holds a reference to an object, never the object itself. That is why passing, assigning and storing things in Python is cheap, whatever their size.
"""),
        Section("Mutable or immutable, and why it matters", r"""
| Immutable (cannot change in place) | Mutable (can change in place) |
| `int`, `float`, `bool` | `list` |
| `str` | `dict` |
| `tuple` | `set` |
| `frozenset`, `bytes` | most objects you make from your own classes |

### Dictionary keys must be immutable

A dictionary finds a key from its **hash**, a number worked out from its value. If a key could change, its hash would change and the dictionary could never find it again. So only **hashable** (in practice, immutable) objects may be keys:

```python
# raises: TypeError
scores = {[1, 2]: "a list cannot be a key"}
```

A tuple is a perfectly good key, which is handy for coordinates: `grid[(3, 4)]`.

### Immutable containers can hold mutable things

A tuple stops *its own* contents being swapped, but if one item is a list, that list can still be changed:

```python
t = ([1], 2)
t[0].append(9)            # allowed: the list inside is mutable
print(t)

try:
    t[0] = [5]            # not allowed: this tries to replace what the tuple holds
except TypeError as problem:
    print(problem)
```

### The mutable default argument trap

Python makes a default value **once**, when the function is *defined*, not each time it is called. If the default is a list, every call that uses it shares that one list:

```python
def add_item(item, basket=[]):
    basket.append(item)
    return basket

print(add_item("apple"))
print(add_item("bread"))         # the apple is still there!
```

The standard fix is `None` as a signal, with a new list made inside the function each time:

```python
def add_item(item, basket=None):
    if basket is None:
        basket = []
    basket.append(item)
    return basket

print(add_item("apple"))
print(add_item("bread"))
```

### By value or by reference?

Exams ask how a parameter is passed. **By value** means the subprogram gets a **copy**, so changing the parameter never affects the caller. **By reference** means it gets a link to the caller's variable itself, so changes do. Python does neither exactly. It passes a **reference to the object**, sometimes called *call by object reference*, so what happens depends on whether the object is mutable and on what the function does with it:

```python
def change(numbers, count):
    numbers.append(99)        # mutates the object the caller also has
    count = count + 1         # rebinds a local name; the caller's name is unaffected

data = [1]
total = 5
change(data, total)
print(data, total)
```

The list was altered, because the function changed the one shared object. The number was not, because `count + 1` made a *new* integer and attached the local name to it.

| | What the subprogram receives | A change to the parameter |
| By value | a copy | does not affect the caller |
| By reference | the caller's variable | affects the caller |
| Python | a reference to the same object | **mutating** it affects the caller; **rebinding** the name does not |
"""),
        Section("Copying: aliases, shallow and deep", r"""
Because assignment only attaches a name, getting a real copy needs a deliberate step. There are three levels:

| What you write | Result |
| `b = a` | an **alias**: one object, two names |
| `b = a.copy()`, `b = a[:]`, `b = list(a)`, `copy.copy(a)` | a **shallow copy**: a new outer list, but the items in it are still shared |
| `b = copy.deepcopy(a)` | a **deep copy**: new copies of everything inside, to any depth |

For a list of numbers or strings, a shallow copy is enough, because those items are immutable. The difference only shows when the items are themselves mutable, such as a grid made of lists:

```python
import copy

grid = [[0, 0], [0, 0]]
alias = grid
shallow = grid[:]
deep = copy.deepcopy(grid)

grid[0][0] = 9

print("grid   ", grid)
print("alias  ", alias)
print("shallow", shallow)           # the outer list is new, but the rows are shared
print("deep   ", deep)
```

The shallow copy has its own outer list, but both outer lists hold the **same two row objects**, so changing a row through one is visible through the other. Only the deep copy is fully independent.

### The grid bug

This is one of the most common bugs in student programs. Multiplying a list repeats the *reference*, not the contents:

```python
bad = [[0] * 3] * 3             # three names for the SAME row
bad[0][0] = 1
print(bad)

good = [[0] * 3 for _ in range(3)]    # a new row is built each time round
good[0][0] = 1
print(good)
```

`[0] * 3` is safe because the zeros are immutable. But `[[0] * 3] * 3` repeats one *row*, so all three rows are the same object. A comprehension builds a fresh row each time.

### Copying your own objects

An object made from your own class is also shared by default. `copy.copy` makes a shallow copy of it, and `copy.deepcopy` a full one. For a class built with `@dataclass`, `dataclasses.replace` makes a modified copy in one line.

```python
import copy

class Player:
    def __init__(self, name, items):
        self.name = name
        self.items = items

hero = Player("Ana", ["sword"])
twin = copy.copy(hero)              # a new Player, but the SAME items list
clone = copy.deepcopy(hero)         # a new Player with its own items list

hero.items.append("shield")
print(twin.items)
print(clone.items)
```

!warn Copies cost something :: A deep copy duplicates every object inside, so it is slower and uses more memory. Take the shallowest copy that is safe, and when you can, avoid the problem by building new objects instead of changing shared ones.
"""),
        Section("How Python manages memory", r"""
Python never asks you to free memory. It keeps track of every object by counting how many references it has. This is **reference counting**:

- binding a name, putting it in a list, or passing it to a function **adds** a reference
- deleting a name, leaving a function, or removing it from a list **removes** one
- when the count reaches **zero**, nothing can reach the object any more, so Python frees it at once

```python
import sys

items = [1, 2, 3]
before = sys.getrefcount(items)

second = items                           # one more reference
third = items                            # and another
print("added:", sys.getrefcount(items) - before)

del second                               # removes the name, not the list
print("added:", sys.getrefcount(items) - before)
```

(`getrefcount` itself holds a temporary reference while it runs, which is why programs compare two counts rather than reading one.)

`del` removes a **name**. The object is only freed if that was its last reference. You can watch an object disappear using a **weak reference**, which does not keep it alive:

```python
import weakref

class Node:
    def __init__(self, name):
        self.name = name

node = Node("a")
watcher = weakref.ref(node)
print("alive:", watcher() is node)

del node                                  # the last reference goes, and so does the object
print("after del:", watcher())
```

### Reference cycles and the garbage collector

Reference counting has one weakness. If two objects refer to *each other*, each keeps the other's count above zero, even when nothing else in the program can reach either of them. Python adds a **garbage collector** that periodically looks for such cycles and frees them.

```python
import gc
import weakref

class Node:
    def __init__(self, name):
        self.name = name
        self.other = None

gc.disable()                              # so that nothing happens until we choose

first, second = Node("p"), Node("q")
first.other, second.other = second, first         # a cycle
watcher = weakref.ref(first)

del first, second
print("after del:", watcher() is not None, "(the cycle keeps itself alive)")

gc.collect()                              # run the cycle detector now
print("after gc.collect():", watcher() is not None)
gc.enable()
```

**Garbage collection** is automatic memory management: the language finds the memory that is no longer needed and reclaims it, so there are no dangling pointers and no forgotten `free` calls. The costs are some time spent counting and collecting, and less control over when memory is released.

### Memory leaks still happen

If something still holds a reference, the object is never freed, even if you have forgotten about it. A global list or cache that only ever grows is the usual cause.

### Saving memory with `__slots__`

An ordinary object keeps its attributes in a hidden dictionary, which is flexible but takes space. Declaring `__slots__` gives a class a fixed set of attributes instead, and no dictionary:

```python
import tracemalloc

class Plain:
    def __init__(self, a, b):
        self.a = a
        self.b = b

class Slim:
    __slots__ = ("a", "b")
    def __init__(self, a, b):
        self.a = a
        self.b = b

def memory_used(cls):
    tracemalloc.start()
    objects = [cls(i, i) for i in range(5000)]
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return current

print("slots use less memory:", memory_used(Slim) < memory_used(Plain))

slim = Slim(1, 2)
try:
    slim.c = 3                           # not in __slots__
except AttributeError as problem:
    print(type(problem).__name__)
```

The saving matters when a program makes hundreds of thousands of small objects. The price is that you cannot add attributes that were not declared.
"""),
        Section("Hunting an aliasing bug", r"""
Almost every aliasing bug looks the same: *a change in one place shows up somewhere you did not touch.* Here is a noughts and crosses board that does it. Read it, predict the output, then run it.

```python
class Board:
    def __init__(self):
        self.cells = [["."] * 3] * 3

    def place(self, row, col, mark):
        self.cells[row][col] = mark

    def show(self):
        for row in self.cells:
            print(" ".join(row))

board = Board()
board.place(0, 0, "X")
board.show()
```

One `X` was placed, but three appear. The method did nothing wrong: the fault is in `__init__`, where `[["."] * 3] * 3` makes three names for one row.

### A method for finding these bugs

1. **Reproduce it** with the smallest program you can. Here, three lines.
2. **Ask whether two names are the same object**, using `is`, or compare the identity of two rows:

```python
board_cells = [["."] * 3] * 3
print(board_cells[0] is board_cells[1])
print(board_cells[0] is board_cells[2])
```

3. **Fix the construction** so that every row is its own object, and prove it with a test:

```python
class Board:
    def __init__(self):
        self.cells = [["."] * 3 for _ in range(3)]

    def place(self, row, col, mark):
        self.cells[row][col] = mark

    def show(self):
        for row in self.cells:
            print(" ".join(row))

board = Board()
board.place(0, 0, "X")
board.show()
print("rows are separate objects:", board.cells[0] is not board.cells[1])
```

### A checklist for the next time

| Warning sign | Likely cause |
| A change appears in a variable you did not change | an **alias**: two names, one object |
| A list or dictionary default in a `def` line | the **mutable default** trap |
| `[[...]] * n` | a repeated **reference** to one inner object |
| A copy that still changes with the original | a **shallow** copy of nested data |
| A function that returns the list it was given, changed | it **mutated** its argument: copy first, or document it |
| Memory growing without end | something still **references** objects you thought were gone |

!exam Say which of the two it is :: When an exam gives code with an unexpected output, the mark is for saying whether a name was **rebound** to a new object or the existing object was **mutated**, and whether two names share one object.
"""),
    ],
    keyterms=[
        ("Reference", "A link from a name (or another object) to an object in memory. A Python variable holds a reference, not the object."),
        ("Identity", "Whether two names refer to the very same object, tested with `is`."),
        ("Mutable", "An object that can be changed in place after it is created, such as a list or dictionary."),
        ("Immutable", "An object that cannot be changed after it is created, such as a number, string or tuple."),
        ("Alias", "A second name for an object that already has one."),
        ("Shallow copy", "A copy of a container that creates a new outer object but shares the items inside it."),
        ("Deep copy", "A copy that duplicates the container and everything inside it, to any depth."),
        ("Call by object reference", "How Python passes arguments: the parameter is bound to the same object the caller passed."),
        ("Reference counting", "Keeping a count of how many references an object has, and freeing it when the count reaches zero."),
        ("Garbage collection", "Automatic recovery of memory that a program can no longer reach, including objects in reference cycles."),
        ("Heap", "The area of memory where objects are created."),
    ],
    grade="""
This topic produces unexpected-output questions. The marks are for explaining the cause in terms of objects and names.

+ Use the words object, name and reference, rather than saying a variable 'contains' a list
+ Say whether an operation mutates an existing object or rebinds a name to a new one
+ For parameter passing, say what is passed (a reference to an object) and give the mutate or rebind consequence
+ For copies, name the level: alias, shallow or deep, and say which parts are shared
+ For memory, name the mechanism: reference counting, and a cycle detector for the cases it cannot handle
""",
    mistakes=[
        "Saying `b = a` copies the list. It gives the same list a second name.",
        "Using `is` to compare numbers or strings. It tests identity, so use `==` to compare values.",
        "Writing a mutable default such as `def f(x, items=[])`, which is created once and shared by every call.",
        "Making a grid with `[[0] * 3] * 3`, so every row is the same row.",
        "Thinking `del x` destroys the object. It only removes the name x.",
    ],
    quiz=[
        Q("After `a = [1, 2]` and `b = a`, what does `a.append(3)` do to b?",
          ["b shows [1, 2, 3] too, because both names refer to one list", "Nothing: b is a separate copy", "It raises an error", "It sets b to None"], 0,
          "Assignment attaches a second name to the same object, so a change made through one name is visible through the other."),
        Q("What is the difference between `==` and `is`?",
          ["`==` compares values; `is` tests whether two names refer to the same object", "They are the same", "`==` tests identity; `is` compares values", "`is` can only be used with numbers"], 0,
          "Two equal lists are two objects, so `==` is True and `is` is False."),
        Q("Which of these is immutable?",
          ["A tuple", "A list", "A dictionary", "A set"], 0,
          "Tuples cannot be changed in place, though they may hold mutable items."),
        Q("Why can a list not be used as a dictionary key?",
          ["It is mutable, so its hash could change", "It is too large", "Lists have no length", "Keys must be strings"], 0,
          "A dictionary finds keys by hash, which would stop working if the key could change."),
        Q("What does this print? `def f(x=[]): x.append(1); return x` then `f(); print(f())`",
          ["[1, 1]", "[1]", "[]", "An error"], 0,
          "The default list is created once and is shared, so the second call adds to the same list."),
        Q("What is the safe way to give a function a default empty list?",
          ["Use None as the default and create the list inside the function", "Use [] but copy it after", "Use a global list", "It cannot be done"], 0,
          "Checking for None and creating a new list gives every call its own."),
        Q("Which copy shares the inner lists with the original?",
          ["A shallow copy", "A deep copy", "Neither", "Both"], 0,
          "A shallow copy makes a new outer list but its items are the same objects."),
        Q("Why is `[[0] * 3] * 3` a poor way to build a grid?",
          ["All three rows are the same list object", "It makes the grid too small", "It makes a tuple", "It uses too much memory"], 0,
          "The multiplication repeats the reference to the one inner list."),
        Q("What happens to an object when its reference count reaches zero?",
          ["It is freed immediately", "It is kept until the program ends", "It is copied", "It is moved to the disk"], 0,
          "Nothing can reach it any more, so Python reclaims its memory straight away."),
        Q("Why does Python need a garbage collector as well as reference counting?",
          ["Objects in a reference cycle never reach a count of zero", "Reference counting is too fast", "Reference counting cannot free lists", "Reference counting only works for numbers"], 0,
          "Two objects that refer to each other keep each other alive, so a separate collector finds and frees such cycles."),
    ],
    exam=[
        EQ("Explain the difference between passing a parameter by value and passing it by reference.", 4, [
            MP("By value: the subprogram receives a copy of the value", ["copy", "copied", "duplicate"]),
            MP("So changes made to the parameter inside the subprogram do not affect the original variable", ["do not affect", "not change", "original is unchanged", "unchanged", "does not change"]),
            MP("By reference: the subprogram receives a reference (the address) to the original variable or object", ["reference", "address", "pointer", "the original", "link"]),
            MP("So changes made to the parameter do affect the original", ["do affect", "changes the original", "original is changed", "changed", "modified"]),
        ], "When a parameter is passed by value, the subprogram receives a copy of the value, so any changes made to the parameter inside the subprogram do not affect the original variable. When a parameter is passed by reference, the subprogram receives a reference to the original variable or object, such as its address, so changes made to the parameter do affect the original. Python passes a reference to the object, so a mutable object such as a list can be changed by the subprogram, though rebinding the parameter to a new object does not affect the caller.",
           command="Explain"),
        EQ("The program shown is run. State what is output by each of the two print statements, and explain why the outputs are different.", 4, [
            MP("The first print outputs [1, 2, 3, 4]", ["[1, 2, 3, 4]", "1, 2, 3, 4"]),
            MP("The second print outputs [1, 2, 3, 5]", ["[1, 2, 3, 5]", "1, 2, 3, 5"]),
            MP("b = a makes b another name for the same list, so appending through b changes the list a refers to", ["same list", "same object", "another name", "alias", "refers to the same"]),
            MP("a[:] makes a (shallow) copy, so c is a separate list and the append to c does not affect a", ["copy", "separate", "new list", "different list", "independent"]),
        ], r"""The first print outputs [1, 2, 3, 4] and the second outputs [1, 2, 3, 5]. The statement b = a does not copy the list: it makes b a second name for the same list, so b.append(4) changes the one list that both a and b refer to. The statement c = a[:] makes a copy of the list, so c is a separate list. The append of 5 changes only c, and a is not affected.""",
           command="State",
           figure="""```python
a = [1, 2, 3]
b = a
c = a[:]
b.append(4)
c.append(5)
print(a)
print(c)
```"""),
        EQ("The subprogram shown is called twice, first with add('apple') and then with add('bread'). State what is returned by the second call, explain why, and show how the subprogram could be rewritten to avoid the problem.", 5, [
            MP("The second call returns ['apple', 'bread']", ["['apple', 'bread']", "apple", "both"]),
            MP("The default list is created only once, when the subprogram is defined", ["once", "defined", "when the function is defined", "created when"]),
            MP("So every call that uses the default shares the same list, which keeps the earlier item", ["same list", "shared", "shares", "keeps"]),
            MP("Rewrite with a default of None", ["none", "basket=None", "= None"]),
            MP("and create a new empty list inside the subprogram if the parameter is None", ["new list", "basket = []", "if basket is none", "inside", "empty list"]),
        ], r"""```python
def add(item, basket=None):
    if basket is None:
        basket = []
    basket.append(item)
    return basket

print(add("apple"))
print(add("bread"))
```

The second call to the original returns ['apple', 'bread']. The default list is created only once, when the subprogram is defined, so every call that does not supply its own list shares that one list, and the apple from the first call is still in it. The rewritten version uses None as the default and creates a new empty list inside the subprogram each time, so each call starts with its own list.""",
           command="Explain",
           figure="""```python
def add(item, basket=[]):
    basket.append(item)
    return basket
```"""),
        EQ("Describe the difference between a shallow copy and a deep copy of a list of lists.", 4, [
            MP("A shallow copy creates a new outer list", ["new outer", "new list", "new container"]),
            MP("but the inner lists in it are the same objects as in the original (they are shared)", ["same", "shared", "share", "references", "same objects"]),
            MP("so changing an inner list through one copy is visible through the other", ["changing", "change", "visible", "affect", "both"]),
            MP("A deep copy creates new copies of the inner lists as well, so the two are completely independent", ["deep", "independent", "inner lists as well", "everything", "completely"]),
        ], "A shallow copy creates a new outer list, but the inner lists in it are the same objects as the ones in the original list, so they are shared. Changing an inner list through one copy is therefore visible through the other. A deep copy creates new copies of the inner lists as well, and of anything inside them, so the original and the copy are completely independent and a change to one never affects the other.",
           command="Describe"),
        EQ("Explain how reference counting is used to recover memory, and explain why a garbage collector is also needed.", 5, [
            MP("Each object keeps a count of the number of references to it", ["count", "number of references", "how many references"]),
            MP("The count goes up when a new reference is made and down when one is removed", ["goes up", "increases", "decreases", "goes down", "removed", "added"]),
            MP("When the count reaches zero the object cannot be reached, so its memory is freed", ["zero", "freed", "reclaimed", "released", "cannot be reached"]),
            MP("Objects that refer to each other (a cycle) keep each other's counts above zero even when nothing else can reach them", ["cycle", "refer to each other", "circular", "each other"]),
            MP("A garbage collector finds such unreachable cycles and frees them", ["garbage collector", "finds", "detects", "periodically", "unreachable"]),
        ], "Each object keeps a count of how many references there are to it. The count goes up when a new reference is made, for example by assigning it to a name, and goes down when a reference is removed. When the count reaches zero the object can no longer be reached by the program, so its memory is freed immediately. This does not work for objects that refer to each other in a cycle, because each keeps the other's count above zero even when nothing else in the program can reach either of them. A garbage collector is therefore also needed, which periodically finds groups of unreachable objects such as these and frees them.",
           command="Explain"),
    ],
)
