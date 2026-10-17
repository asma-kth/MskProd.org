"""Advanced Python: special methods, properties, dataclasses, enums, type hints and modern syntax."""
from mskbuild.models import Topic, Section, Q, EQ, MP

INPUTS = {}
EXPECT = {}

TOPIC = Topic(
    slug="special-methods-dataclasses-and-typing",
    title="Special Methods, Dataclasses and Type Hints",
    spec="Advanced 4",
    icon="i-cube",
    minutes=65,
    blurb="Make your own classes behave like built-in types, with operators, len, indexing and sorting. Then use properties, class methods, dataclasses and enums to cut boilerplate, add type hints and write your own runtime checker, and finish with modern syntax: match statements, unpacking and the walrus operator.",
    fact="Python's special methods are nicknamed 'dunder' methods, short for double underscore. When you write a + b, Python really calls a.__add__(b). Every operator, every len(), every for loop and even printing an object is a call to one of them, which is why your own classes can behave exactly like numbers or lists.",
    sections=[
        Section("The data model: special methods", r"""
Built-in types seem to have powers that your own classes lack: you can add numbers, take the `len` of a list, loop over a string, compare and sort. None of this is magic. Each is a call to a **special method**, whose name starts and ends with two underscores. If your class defines the right ones, it joins in too.

| You write | Python calls |
| `print(x)`, `str(x)` | `x.__str__()` |
| `repr(x)`, and a list of objects | `x.__repr__()` |
| `a == b` | `a.__eq__(b)` |
| `a < b` | `a.__lt__(b)` |
| `a + b`, `a * 3` | `a.__add__(b)`, `a.__mul__(3)` |
| `3 * a` | `a.__rmul__(3)` |
| `abs(a)` | `a.__abs__()` |
| `len(x)` | `x.__len__()` |
| `x[i]` | `x.__getitem__(i)` |
| `for item in x`, `item in x` | `x.__iter__()`, `x.__contains__(item)` |
| `if x:` | `x.__bool__()` |
| `x(5)` | `x.__call__(5)` |
| `hash(x)`, set and dictionary keys | `x.__hash__()` |

A class for two dimensional vectors uses several at once:

```python
import math

class Vector:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __repr__(self):                       # for programmers: unambiguous
        return "Vector(%r, %r)" % (self.x, self.y)

    def __str__(self):                        # for users: readable
        return "(%s, %s)" % (self.x, self.y)

    def __eq__(self, other):
        return isinstance(other, Vector) and (self.x, self.y) == (other.x, other.y)

    def __hash__(self):                       # equal objects must have equal hashes
        return hash((self.x, self.y))

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __mul__(self, k):
        return Vector(self.x * k, self.y * k)

    __rmul__ = __mul__                        # so that 3 * v works as well as v * 3

    def __abs__(self):
        return math.hypot(self.x, self.y)

    def __bool__(self):
        return bool(self.x or self.y)

a, b = Vector(1, 2), Vector(3, 4)
print(a + b, a * 3, 3 * a)
print(abs(b))
print(a == Vector(1, 2), a is Vector(1, 2))
print(repr(a), "|", str(a), "|", [a, b])
print(len({a, Vector(1, 2), b}), bool(Vector(0, 0)))
```

`__repr__` is for the person debugging, and ideally looks like the code that would build the object. `__str__` is for the person using the program. If only `__repr__` is defined, it is used for both. A list prints its items with `__repr__`, which is why the list above shows `Vector(1, 2)`.

!warn Equal means equal hash :: If you define `__eq__` you should define `__hash__` to match, or objects that compare equal could land in different places in a set or dictionary. A class that defines `__eq__` alone becomes unhashable.

### Sequences: len and indexing

If a class defines `__len__` and `__getitem__` it behaves like a sequence. Indexing, slicing, `in`, `for` and `sorted` all work, without writing anything else.

```python
class Deck:
    suits = "SHDC"
    ranks = [str(n) for n in range(2, 11)] + list("JQKA")

    def __init__(self):
        self.cards = [rank + suit for suit in self.suits for rank in self.ranks]

    def __len__(self):
        return len(self.cards)

    def __getitem__(self, position):
        return self.cards[position]

deck = Deck()
print(len(deck), deck[0], deck[-1], deck[:3])
print("AS" in deck, "ZZ" in deck)
print(sorted(deck)[:3])
print(sum(1 for card in deck if card.endswith("H")), "hearts")
```

### Ordering: define one comparison and let Python supply the rest

To sort your own objects you need `__lt__`. The decorator `functools.total_ordering` then fills in `<=`, `>`, and `>=` from `__eq__` and `__lt__`. This class sorts version numbers *numerically*, which plain strings do not:

```python
from functools import total_ordering

@total_ordering
class Version:
    def __init__(self, text):
        self.text = text
        self.parts = tuple(int(part) for part in text.split("."))

    def __eq__(self, other):
        return self.parts == other.parts

    def __lt__(self, other):
        return self.parts < other.parts

    def __repr__(self):
        return "Version(%r)" % self.text

versions = [Version("1.10.0"), Version("1.2.5"), Version("1.2.10")]
print(sorted(versions))
print(max(versions))
print(sorted(["1.10.0", "1.2.5", "1.2.10"]))          # as text, 1.10 sorts before 1.2
print(Version("2.0") >= Version("1.9.9"))
```

### Objects that act like functions

Defining `__call__` makes an object callable, so it can carry settings and still be used where a function is expected, such as in `map`:

```python
class Multiplier:
    def __init__(self, k):
        self.k = k

    def __call__(self, x):
        return x * self.k

double = Multiplier(2)
print(double(21), callable(double))
print(list(map(double, [1, 2, 3])))
```
"""),
        Section("Properties, class methods and static methods", r"""
### Properties: attributes with rules

A **property** looks like an ordinary attribute from the outside, but runs a method when it is read or assigned. It lets a class **validate** values, or **calculate** them, without callers ever writing `get_` and `set_`.

```python
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius                # this goes through the setter below

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("below absolute zero")
        self._celsius = value

    @property
    def fahrenheit(self):                     # no setter: read only, and always up to date
        return self._celsius * 9 / 5 + 32

t = Temperature(100)
print(t.fahrenheit)
t.celsius = 0
print(t.fahrenheit)

try:
    t.celsius = -300
except ValueError as problem:
    print(problem)

try:
    t.fahrenheit = 5
except AttributeError:
    print("fahrenheit is read only")
```

This is **encapsulation** the Python way. You start with a plain public attribute. If you later need a rule, you turn it into a property, and **no code that uses the class has to change**. Python has no truly private attributes. A single leading underscore (`_celsius`) is a convention meaning *internal, please do not touch*. A double underscore (`__balance`) triggers **name mangling**, which renames it to `_Class__balance` to avoid clashes in subclasses. That is not security.

### Class methods and static methods

| Kind | First parameter | Use |
| ordinary method | `self`, the object | work with one object's data |
| `@classmethod` | `cls`, the class | alternative **constructors**, and things that concern the whole class |
| `@staticmethod` | nothing special | a utility that belongs with the class but needs neither |

```python
class Date:
    def __init__(self, year, month, day):
        self.year, self.month, self.day = year, month, day

    @classmethod
    def from_string(cls, text):               # a second way to build a Date
        year, month, day = (int(part) for part in text.split("-"))
        return cls(year, month, day)

    @staticmethod
    def is_leap(year):
        return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)

    def __repr__(self):
        return "Date(%d, %d, %d)" % (self.year, self.month, self.day)

print(Date.from_string("2024-02-29"))
print(Date.is_leap(2100), Date.is_leap(2024))
```

### Class attributes and instance attributes

An attribute set inside `__init__` belongs to **one object**. An attribute set in the class body belongs to the **class** and is shared by every object. Use it for constants and for counting how many objects have been made:

```python
class Ticket:
    issued = 0                                # shared by the whole class

    def __init__(self):
        Ticket.issued += 1
        self.number = Ticket.issued           # belongs to this object

first, second = Ticket(), Ticket()
print(first.number, second.number)
print(Ticket.issued, first.issued)
```

!warn The same trap again :: A class attribute that is a list or dictionary is shared by every object, exactly like a mutable default argument. Create mutable attributes inside `__init__`.
"""),
        Section("Dataclasses and enums", r"""
Many classes exist only to hold some data. Writing `__init__`, `__repr__` and `__eq__` for each is dull, repetitive work. The **`@dataclass`** decorator writes them for you from a list of annotated fields:

```python
from dataclasses import dataclass, field, asdict, replace

@dataclass(order=True)
class Item:
    name: str
    price: float
    tags: list = field(default_factory=list, compare=False)

    def __post_init__(self):                  # runs after the generated __init__
        if self.price < 0:
            raise ValueError("price cannot be negative")

pen = Item("pen", 1.5, ["stationery"])
print(pen)
print(pen == Item("pen", 1.5))
print(pen < Item("pencil", 0.5))              # ordering compares the fields in order
print(asdict(pen))
print(replace(pen, price=2.0))

try:
    Item("bad", -1)
except ValueError as problem:
    print(problem)
```

You got `__init__`, `__repr__`, `__eq__` and, because of `order=True`, all the comparison methods, from six lines. `field(default_factory=list)` is how a dataclass avoids the mutable default trap: it builds a new list for each object. `replace` makes a changed copy.

A **frozen** dataclass cannot be changed after creation, which also makes it hashable and so usable as a dictionary key:

```python
from dataclasses import dataclass

@dataclass(frozen=True)
class Point:
    x: int
    y: int

p = Point(1, 2)
try:
    p.x = 5
except Exception as problem:
    print(type(problem).__name__)

print({p: "usable as a key"})
```

### Enums: a fixed set of named values

When a variable can only take one of a few values, such as the state of a traffic light or the suit of a card, a **string** invites typos (`"gren"`) and a bare number means nothing. An **`Enum`** gives each value a name, and a typo becomes an error.

```python
from enum import Enum, auto

class Light(Enum):
    RED = auto()
    GREEN = auto()
    AMBER = auto()

NEXT = {Light.RED: Light.GREEN, Light.GREEN: Light.AMBER, Light.AMBER: Light.RED}

state = Light.RED
for _ in range(4):
    print(state.name, state.value)
    state = NEXT[state]

print(list(Light))
print(Light["GREEN"], Light(2), Light.RED is Light.RED)
```

This is the finite state machine from the theory topic, with proper names for its states. Members are unique, can be looped over, and compared with `is`.

### Named tuples

For a small immutable record that should also behave like a tuple, `typing.NamedTuple` gives you named fields:

```python
from typing import NamedTuple

class Point3(NamedTuple):
    x: int
    y: int
    z: int = 0

p = Point3(1, 2)
x, y, z = p                                   # still unpacks like a tuple
print(p, p.x, p[1], x, y, z)
```

| Choose | When |
| `NamedTuple` | a small, fixed, immutable record, used like a tuple |
| `@dataclass` | a record you may want to change, or that needs methods, defaults or ordering |
| a full class | behaviour matters more than the data |
"""),
        Section("Type hints", r"""
Python decides types while the program runs. **Type hints** are optional notes saying what types a function expects and returns. They are for people and for tools, and Python **does not enforce them**:

```python
def double(x: int) -> int:
    return x * 2

print(double(4))
print(double("ha"))               # a str, not an int: Python does not mind
print(double.__annotations__)
```

The call with `"ha"` worked, and returned `haha`. The hints are stored on the function, and ignored when it runs. Their value is elsewhere:

- **documentation** that can never be out of date with the code the way a comment can
- **editors** use them for auto-completion and to underline mistakes as you type
- **checkers** such as mypy and pyright read the whole program and report type errors *before* it runs

```text
pip install mypy
mypy program.py
program.py:5: error: Argument 1 to "double" has incompatible type "str"; expected "int"
```

| Hint | Means |
| `int`, `str`, `float`, `bool` | the plain types |
| `list[int]`, `dict[str, float]`, `tuple[int, int]` | containers, with the types inside |
| `int \| None` | an int, or None (it might be missing) |
| `Callable[[int], str]` | a function taking an int and returning a str |
| `Any` | anything: turns checking off for that value |

### Hints are data: write your own checker

Because hints are kept on the function, a decorator can read them with `inspect` and `typing.get_type_hints`, and **enforce** them while the program runs:

```python
import functools
import inspect
from typing import get_type_hints

def enforce(func):
    hints = get_type_hints(func)
    signature = inspect.signature(func)

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        bound = signature.bind(*args, **kwargs)
        for name, value in bound.arguments.items():
            expected = hints.get(name)
            if isinstance(expected, type) and not isinstance(value, expected):
                raise TypeError(name + " must be " + expected.__name__ + ", not " + type(value).__name__)
        return func(*args, **kwargs)
    return wrapper

@enforce
def double(x: int) -> int:
    return x * 2

print(double(4))
try:
    double("ha")
except TypeError as problem:
    print(problem)
```

### Generic containers and protocols

A **type variable** lets a class work for any type while promising consistency: a `Stack[int]` only holds ints. A **protocol** describes *what an object can do* rather than what it is, which is Python's duck typing written down: anything with a `speak` method will do.

```python
from typing import Generic, Protocol, TypeVar

T = TypeVar("T")

class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

numbers = Stack[int]()
numbers.push(1)
numbers.push(2)
print(numbers.pop())

class Speaker(Protocol):
    def speak(self) -> str: ...

class Dog:
    def speak(self) -> str:
        return "Woof"

class Robot:
    def speak(self) -> str:
        return "Beep"

def announce(thing: Speaker) -> None:
    print(thing.speak())

announce(Dog())
announce(Robot())
```

`Dog` and `Robot` share no parent class. Both satisfy `Speaker` simply by having the method, which is **polymorphism** without inheritance.
"""),
        Section("Modern syntax and Python idioms", r"""
Python has grown a number of features that make everyday code shorter and clearer. These are the ones worth using.

### match: structural pattern matching

`match` compares a value against **patterns**, and can pull it apart at the same time. It is a much tidier replacement for a long chain of `if` and `elif` that inspects the shape of data:

```python
def handle(command):
    match command.split():
        case ["go", direction]:
            return "walking " + direction
        case ["take", *items]:                     # *items collects the rest
            return "taking " + ", ".join(items)
        case ["quit"] | ["exit"]:                  # either pattern
            return "bye"
        case [verb, *_]:
            return "I do not know how to " + verb
        case []:
            return "say something"

for line in ["go north", "take lamp rope", "exit", "dance wildly", ""]:
    print(repr(line), "->", handle(line))

def area(shape):
    match shape:
        case {"type": "circle", "r": r}:           # a dictionary pattern binds r
            return round(3.14159 * r * r, 2)
        case {"type": "rect", "w": w, "h": h}:
            return w * h
        case _:                                    # the underscore matches anything
            return None

print(area({"type": "circle", "r": 2}), area({"type": "rect", "w": 3, "h": 4}), area({"type": "blob"}))
```

### Unpacking, the walrus and friends

```python
data = [4, 8, 15, 16, 23, 42]

if (n := len(data)) > 5:                  # the walrus := assigns and tests in one step
    print(n, "items")

first, *middle, last = data               # extended unpacking
print(first, middle, last)

a, b = 1, 2
a, b = b, a                               # swap without a temporary variable
print(a, b)

for position, (name, score) in enumerate([("Ana", 82), ("Raj", 91)], start=1):
    print(position, name, score)

defaults = {"colour": "blue", "size": 3}
print(defaults | {"size": 5})             # merge two dictionaries
print(list(zip(*[[1, 2, 3], [4, 5, 6]]))) # transpose a table
```

### Formatting with f-strings

An f-string can format as it inserts. After the colon come a width, alignment, precision and type:

```python
name, score, ratio, big = "Ana", 82.456, 0.4567, 1234567

print(f"{name:>6}|{score:8.2f}|{ratio:.1%}|{big:,}")
print(f"{score = }")                      # prints the expression and its value: great for debugging
print("test_file.py".removesuffix(".py"), max([], default=0), 0 <= 5 < 10)
```

| Spec | Effect |
| `>6`, `<6`, `^6` | right, left, centre in 6 characters |
| `8.2f` | a float, 8 wide, 2 decimal places |
| `.1%` | as a percentage with 1 decimal place |
| `,` | thousands separators |
| `05d` | integer padded with zeros to 5 digits |

### What makes code Pythonic

| Instead of | Write |
| `for i in range(len(items)):` then `items[i]` | `for item in items:` |
| a counter you update by hand | `for i, item in enumerate(items):` |
| a loop that builds a list | a comprehension |
| `if len(items) == 0:` | `if not items:` |
| `if x == True:` | `if x:` |
| `if a < x and x < b:` | `if a < x < b:` |
| a `for` loop with a flag, to test any | `any(...)` or `all(...)` |
| joining strings with `+` in a loop | `"".join(parts)` |

!key Readability counts :: Idioms are not about being clever. They are about writing code that says what it means, in the way other Python programmers expect to read it.
"""),
    ],
    keyterms=[
        ("Special (dunder) method", "A method with double underscores at each end, such as __add__, that Python calls for an operator or built-in function."),
        ("__repr__ and __str__", "Special methods that give the programmer's and the user's text forms of an object."),
        ("Operator overloading", "Defining special methods such as __add__ so that operators work on objects of your own class."),
        ("Property", "A method accessed like an attribute, used to validate a value being set or to calculate one when it is read."),
        ("Class method", "A method that receives the class instead of an object, often used as an alternative constructor."),
        ("Static method", "A function that is placed in a class for organisation but receives neither the object nor the class."),
        ("Dataclass", "A class whose __init__, __repr__ and comparison methods are generated from its annotated fields by the @dataclass decorator."),
        ("Enum", "A class that defines a fixed set of named constant values."),
        ("Type hint", "An optional annotation stating the type a parameter or return value should have, used by people and tools but not enforced by Python."),
        ("Duck typing", "Using an object because it has the methods needed, whatever its class."),
        ("Structural pattern matching", "The match statement, which tests a value against patterns and can unpack it at the same time."),
    ],
    grade="""
Advanced class features are tested as short coding tasks and as reasons for a design choice.

+ When you write __eq__, say it should be paired with __hash__ if the objects will go in sets or dictionaries
+ For a property, give the reason: validation or calculation, with no change for the users of the class
+ For type hints, say they are not enforced at run time, and name who uses them: people, editors and checkers
+ For a dataclass, name the methods it generates and say what it saves
+ For polymorphism, mention duck typing: any object with the right methods will do
""",
    mistakes=[
        "Writing `__eq__` without `__hash__` and then putting the objects in a set, where they become unhashable.",
        "Returning a string from `__repr__` that gives no clue how to rebuild the object.",
        "Using a mutable class attribute such as a list, which every object then shares.",
        "Thinking type hints stop a wrong type being used. They do not, unless a tool or your own code checks them.",
        "Forgetting `return NotImplemented` or a type check in `__eq__`, so comparing with another type raises an error.",
    ],
    quiz=[
        Q("Which special method is called by `print(obj)`?",
          ["__str__", "__print__", "__repr__ only", "__show__"], 0,
          "print uses __str__, and falls back to __repr__ if __str__ is not defined."),
        Q("Which special method makes `a + b` work for objects of your own class?",
          ["__add__", "__plus__", "__sum__", "__concat__"], 0,
          "Python turns a + b into a call to a.__add__(b)."),
        Q("What is needed for `len(obj)` and `obj[0]` to both work on your own class?",
          ["__len__ and __getitem__", "__size__ and __index__", "__iter__ only", "__call__"], 0,
          "Defining these two makes a class behave like a sequence."),
        Q("What is the point of `__repr__`?",
          ["An unambiguous text form for programmers, ideally showing how to rebuild the object", "To print a friendly message for users", "To copy the object", "To compare two objects"], 0,
          "__str__ is for users, __repr__ is for debugging and lists."),
        Q("What does a property allow a class to do?",
          ["Run code when an attribute is read or assigned, without changing how it is used", "Make an attribute private", "Stop a class being inherited", "Make an attribute constant"], 0,
          "Callers still write obj.value, but the class can validate or calculate."),
        Q("What does the @dataclass decorator generate?",
          ["__init__, __repr__ and __eq__ from the annotated fields", "A database table", "A copy of the class", "A test for the class"], 0,
          "It saves writing the repetitive methods for a class that mostly holds data."),
        Q("Why use an Enum for the states of a traffic light instead of strings?",
          ["A misspelt name is an error, and the set of values is fixed", "Enums run faster", "Strings cannot be compared", "Enums use no memory"], 0,
          "A typo such as 'gren' silently works as a string but fails immediately as an enum member."),
        Q("Python is run with this function: `def f(x: int) -> int: return x * 2` and called as `f('ha')`. What happens?",
          ["It returns 'haha', because hints are not enforced", "A TypeError is raised", "A SyntaxError is raised", "It returns None"], 0,
          "Type hints are ignored when the program runs. Only a checker or your own code uses them."),
        Q("What does a Protocol such as `Speaker` describe?",
          ["What methods an object must have, whatever its class", "A class that every other class must inherit from", "How to send data over a network", "A rule for naming variables"], 0,
          "It states a structure, which is duck typing in a form that a checker can verify."),
        Q("What does `first, *rest = [1, 2, 3, 4]` give rest?",
          ["[2, 3, 4]", "[1]", "2", "[3, 4]"], 0,
          "The star collects all the items that are not assigned to the other names."),
    ],
    exam=[
        EQ("Explain the purpose of the special methods __str__ and __repr__ in a Python class.", 4, [
            MP("__str__ returns a readable text version of the object, for the user", ["readable", "user", "friendly", "human"]),
            MP("It is used by print() and str()", ["print", "str("]),
            MP("__repr__ returns an unambiguous text version of the object, for the programmer (debugging)", ["unambiguous", "programmer", "debug", "developer"]),
            MP("It is used by repr() and when objects are shown in a list, and ideally shows how to recreate the object", ["repr(", "list", "recreate", "rebuild", "interpreter"]),
        ], "The __str__ method returns a readable text version of the object, intended for the user, and it is the one used by print() and str(). The __repr__ method returns an unambiguous text version intended for the programmer when debugging, and ideally it looks like the code needed to recreate the object. It is used by repr(), by the interactive prompt, and when objects are shown inside a list.",
           command="Explain"),
        EQ("Write a class called Vector with a constructor that takes two numbers, x and y, and stores them. Add a method so that two Vector objects can be added using the + operator, giving a new Vector whose x and y are the sums of the x and y values of the two vectors.", 4, [
            MP("A class with an __init__ method taking x and y", ["class vector", "__init__", "def __init__"]),
            MP("The values are stored as attributes (self.x and self.y)", ["self.x", "self.y"]),
            MP("Defines __add__ with a parameter for the other vector", ["__add__", "other"]),
            MP("Returns a new Vector made from the two sums", ["return vector", "vector(", "self.x + other.x", "self.y + other.y"]),
        ], r"""```python
class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

total = Vector(1, 2) + Vector(3, 4)
print(total.x, total.y)
```

The constructor stores x and y as attributes. The special method __add__ is called when the + operator is used with a Vector on the left. It builds and returns a new Vector whose x and y are the sums of the two vectors' values. Here the result is a Vector with x of 4 and y of 6.""",
           command="Write"),
        EQ("A programmer has an attribute called age in a class. Explain what a property is, and why the programmer might replace the attribute with a property.", 4, [
            MP("A property is a method that is accessed like an attribute (without brackets)", ["like an attribute", "without brackets", "accessed", "looks like an attribute"]),
            MP("It runs code when the value is read or assigned", ["runs code", "when it is read", "when it is assigned", "getter", "setter"]),
            MP("This allows the value to be validated, for example rejecting a negative age", ["validat", "negative", "check", "reject", "rule"]),
            MP("Code that uses the class does not need to change, because it is used in the same way as before", ["does not need to change", "no change", "same way", "unchanged", "still"]),
        ], "A property is a method that is accessed like an attribute, without brackets. It runs code whenever the value is read or assigned. The programmer might replace age with a property so that the value can be validated when it is set, for example by rejecting a negative age. Code that uses the class does not need to change, because the age is read and assigned in exactly the same way as when it was a plain attribute.",
           command="Explain"),
        EQ("Describe two benefits of using a dataclass instead of a normal class for a class that is mostly used to store data.", 3, [
            MP("The __init__ method (constructor) is generated automatically from the fields, so less code needs to be written", ["__init__", "constructor", "generated", "automatically", "less code", "boilerplate"]),
            MP("Other methods such as __repr__ and __eq__ are also generated, giving a readable output and comparison of the objects", ["__repr__", "__eq__", "readable", "compar", "printing"]),
            MP("Options such as frozen and order make the objects immutable or sortable with one word", ["frozen", "order", "immutable", "sortable", "hashable", "default"]),
        ], "A dataclass generates the __init__ method automatically from the fields, so a lot less code has to be written. It also generates methods such as __repr__ and __eq__, so the objects print readably and can be compared without writing those methods. Options such as frozen=True, which makes the objects immutable and hashable, and order=True, which makes them sortable, can be added with one word.",
           command="Describe"),
        EQ("A team is deciding whether to add type hints to a large Python program. Discuss the advantages and disadvantages of doing so.", 6, [
            MP("Type hints document what types each function expects and returns", ["document", "documentation", "what types", "clear", "self-documenting"]),
            MP("A checker such as mypy can find type errors before the program is run", ["mypy", "checker", "before", "find errors", "static", "catch"]),
            MP("Editors can use them to give better auto-completion and warnings, helping developers", ["editor", "auto-completion", "autocomplete", "ide", "warnings"]),
            MP("Disadvantage: Python does not enforce them, so wrong types can still be used while the program runs", ["not enforce", "does not enforce", "not checked", "ignored", "still run"]),
            MP("Disadvantage: extra code and effort to write and keep up to date, and hints that are wrong are misleading", ["extra", "effort", "time", "out of date", "misleading", "longer"]),
            MP("A reasoned conclusion: worthwhile in a large program with several developers, if a checker is used", ["conclusion", "worthwhile", "large program", "overall", "therefore", "i would"]),
        ], "Type hints document what type each function expects and returns, which makes a large program easier for a team to understand. A checker such as mypy can use them to find type errors before the program is run, and editors can use them to give better auto-completion and warnings. The disadvantages are that Python does not enforce them, so a value of the wrong type can still be used when the program runs, and that they take extra effort to write and keep up to date, and hints that are out of date or wrong are misleading. For a large program with several developers, type hints are worthwhile, provided a checker is run regularly so that they are kept correct.",
           command="Discuss"),
    ],
)
