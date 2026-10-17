"""A Level Python: the functional programming paradigm."""
from mskbuild.models import Topic, Section, Q, EQ, MP

INPUTS = {}
EXPECT = {}

TOPIC = Topic(
    slug="functional-programming",
    title="Functional Programming",
    spec="A Level 2",
    icon="i-gate",
    minutes=45,
    blurb="Functions as values, map, filter and reduce, pure functions and immutability, composition, partial application and closures: the whole of the functional paradigm in the A Level specification, in working Python.",
    fact="The lambda in Python's lambda keyword comes from the lambda calculus, a system for describing computation using only functions that Alonzo Church published in the 1930s. It is equivalent in power to Alan Turing's machine, which Turing proved in 1937.",
    sections=[
        Section("Functions are values", r"""
In **imperative** programming, a program is a sequence of commands that change variables. In **functional** programming, a program is built out of **functions**, in the maths sense: give one the same input and it always gives the same output, and it does nothing else.

The idea that makes this work is that a function is a **first-class object**. It can be treated like any other value:

- assigned to a variable
- stored in a list or a dictionary
- passed to another function as an argument
- returned from a function as a result

```python
def double(x):
    return x * 2

fn = double                  # no brackets: the function itself, not a call to it
print(fn(5))                 # 10

operations = [double, abs, str]
for op in operations:
    print(op(-3))            # -6, then 3, then -3
```

### Function types

A function takes values from one set, the **domain**, and gives back values from another, the **codomain**. The specification writes this as a **function type**:

| Function | Written as | Meaning |
| `double` | `int → int` | takes an integer, gives an integer |
| `len` | `str → int` | takes a string, gives an integer |
| `add(a, b)` | `int × int → int` | takes two integers, gives an integer |
| `is_even` | `int → bool` | takes an integer, gives a Boolean |

Python can record this in the code itself, with **type hints**. They do not change how the program runs, but they state the function type:

```python
def add(a: int, b: int) -> int:
    return a + b

print(add(2, 3))             # 5
```

**Function application** is simply the act of giving a function its argument: `double(5)` is the application of `double` to 5.

### Higher order functions

A function is **higher order** if it takes a function as an argument, or returns one. It is what first class objects make possible.

```python
def apply_twice(f, x):
    return f(f(x))

print(apply_twice(lambda n: n * 2, 3))                # 12
print(apply_twice(lambda s: s + "!", "hi"))            # hi!!
```

`lambda` makes a small anonymous function in one expression: `lambda n: n * 2` is the function that takes `n` and returns `n * 2`. It is the same thing as a `def`, without a name.
"""),
        Section("Map, filter and reduce", r"""
Three higher order functions do nearly everything a loop over a list is used for. Each takes a function and a list.

!diagram py-map-filter-reduce

| Function | Does | Returns |
| `map(f, items)` | applies `f` to every item | a new list of the results, the same length |
| `filter(f, items)` | keeps the items for which `f` returns `True` | a new list, the same length or shorter |
| `reduce(f, items)` | combines the items, two at a time, with `f` | a single value |

```python
from functools import reduce

numbers = [1, 2, 3, 4, 5, 6]

squares = list(map(lambda n: n * n, numbers))
evens = list(filter(lambda n: n % 2 == 0, numbers))
total = reduce(lambda a, b: a + b, numbers)

print(squares)               # [1, 4, 9, 16, 25, 36]
print(evens)                 # [2, 4, 6]
print(total)                 # 21
print(numbers)               # [1, 2, 3, 4, 5, 6], untouched
```

None of the three changes `numbers`. Each builds something new. That is deliberate, and it is the next section.

### How reduce works

`reduce` carries a running result along the list. It starts with the first two items, then combines that with the third, and so on. Printing inside the function shows it:

```python
from functools import reduce

def add_and_show(a, b):
    print(a, "+", b, "=", a + b)
    return a + b

print(reduce(add_and_show, [1, 2, 3, 4]))
```

### Chaining them

The output of one is the input of the next, so they combine into a **pipeline**. The sum of the squares of the even numbers:

```python
from functools import reduce

numbers = [1, 2, 3, 4, 5, 6]

evens = filter(lambda n: n % 2 == 0, numbers)
squares = map(lambda n: n * n, evens)
total = reduce(lambda a, b: a + b, squares)
print(total)                 # 56: 4 + 16 + 36
```

Python programmers often use a **list comprehension** for the same job. It is the same idea in a different spelling:

```python
numbers = [1, 2, 3, 4, 5, 6]

print([n * n for n in numbers])                    # map
print([n for n in numbers if n % 2 == 0])          # filter
print(sum(n * n for n in numbers if n % 2 == 0))   # filter, map and reduce
```

!exam Describe what each one does, with its result type :: A typical mark scheme wants: map returns a list of the same length with the function applied to each item, filter returns the items for which the function was true, reduce returns one value. Say that each takes a function as an argument, because that is what makes it higher order.
"""),
        Section("Pure functions, immutability and lists", r"""
A function is **pure** if:

1. it always returns the **same output** for the same input, and
2. it has **no side effects**: it does not change anything outside itself, such as a global variable, a list it was given, a file or the screen.

```python
def add_item_impure(basket, item):
    basket.append(item)          # changes the caller's own list: a side effect
    return basket

def add_item_pure(basket, item):
    return basket + [item]       # builds a new list and leaves the old one alone

original = ["milk"]
add_item_impure(original, "eggs")
print(original)                  # ['milk', 'eggs'], changed behind our back

original = ["milk"]
new_basket = add_item_pure(original, "eggs")
print(original, new_basket)      # ['milk'] ['milk', 'eggs']
```

A pure function has **referential transparency**: every call can be replaced by the value it returns, and the program means the same. `square(4)` can be swapped for `16` anywhere.

### Why bother

| Benefit | Because |
| Easy to test | Same input, same output, with nothing else to set up or check |
| Easy to reason about | A bug cannot be caused by a hidden change from somewhere else |
| Safe in parallel | Two calls cannot interfere with each other |
| Cacheable | A result can be remembered, as memoisation does, since it never changes |

The cost is that creating new values rather than changing old ones uses more memory and time.

### Immutability

Functional programs prefer **immutable** data, which cannot change once created. In Python, tuples and strings are immutable:

```python
# raises: TypeError
point = (3, 4)
point[0] = 9
```

You make a changed copy instead: `point = (9,) + point[1:]`.

### Lists as head and tail

In functional languages a list is built from the **head**, its first item, and the **tail**, the list of everything else. A list with nothing in it is the **empty list**, and `cons` builds a new list by putting an item on the front.

```python
def head(items):
    return items[0]

def tail(items):
    return items[1:]

def cons(item, items):
    return [item] + items

def length(items):
    if items == []:
        return 0
    return 1 + length(tail(items))

def total(items):
    if items == []:
        return 0
    return head(items) + total(tail(items))

print(head([4, 5, 6]), tail([4, 5, 6]), cons(3, [4, 5, 6]))     # 4 [5, 6] [3, 4, 5, 6]
print(length([4, 5, 6]), total([4, 5, 6]))                      # 3 15
```

There is no loop and no variable that changes. The list is taken apart by recursion, which is how a language with no loops repeats anything.
"""),
        Section("Composition, partial application and closures", r"""
### Composition

**Composition** joins two functions so that the output of one becomes the input of the next. Written in maths as `f ∘ g`, it means "apply g, then apply f".

```python
def compose(f, g):
    return lambda x: f(g(x))

add_one = lambda x: x + 1
double = lambda x: x * 2

double_then_add = compose(add_one, double)     # first double, then add one
add_then_double = compose(double, add_one)     # first add one, then double

print(double_then_add(5))        # 11
print(add_then_double(5))        # 12
```

Notice that `compose` is itself a higher order function: it takes two functions and returns a new one. And the order matters. `f ∘ g` is generally not the same as `g ∘ f`.

### Partial application

**Partial application** fixes some of a function's arguments and gives back a new function that waits for the rest.

```python
from functools import partial

def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
cube = partial(power, exponent=3)

print(square(5), cube(2))        # 25 8
```

`square` is a function from one number to one number, made from a function of two numbers by supplying one of them in advance.

### Closures and currying

A function written inside another can **remember** the variables of the function that made it, even after that function has finished. That is a **closure**.

```python
def add(a):
    def inner(b):
        return a + b
    return inner

add5 = add(5)
print(add5(3))                   # 8
print(add(2)(10))                # 12
```

`add5` has not been given `a` since it was created, but it still has it. `add` is a **curried** function: instead of taking two arguments at once, it takes one and returns a function that takes the other. `add(2)(10)` applies them one after the other.

A closure can hold changing state too, which is how a function with a memory is built without a class:

```python
def make_counter():
    count = 0
    def counter():
        nonlocal count
        count += 1
        return count
    return counter

first = make_counter()
second = make_counter()
print(first(), first(), first(), second())     # 1 2 3 1
```

Each counter has its own `count`, hidden inside its closure where nothing else can reach it.

### Summary of the paradigm

!key The defining ideas :: Functions are first class objects. Programs are built by applying and composing functions, and by passing functions to higher order functions such as map, filter and reduce. Data is immutable and functions are pure, so a function's result depends only on its arguments. Repetition is done by recursion, not by changing a counter.
"""),
    ],
    keyterms=[
        ("First-class object", "A value that can be assigned to a variable, stored in a data structure, passed as an argument and returned from a function. In functional languages, functions are first-class."),
        ("Higher-order function", "A function that takes one or more functions as arguments, or returns a function as its result."),
        ("Map", "A higher-order function that applies a function to every item of a list and returns the list of results."),
        ("Filter", "A higher-order function that returns the items of a list for which a given function returns true."),
        ("Reduce", "A higher-order function that combines all the items of a list into a single value by repeatedly applying a function."),
        ("Pure function", "A function that always gives the same result for the same arguments and has no side effects."),
        ("Side effect", "Any change a function makes outside itself, such as altering a global variable, its arguments, a file or the display."),
        ("Immutable", "Describes data that cannot be changed once it has been created."),
        ("Composition", "Combining two functions so that the output of one is the input of the other."),
        ("Partial application", "Supplying some of a function's arguments to produce a new function that takes the remaining ones."),
        ("Closure", "A function together with the variables of the surrounding scope that it can still use after that scope has ended."),
    ],
    grade="""
Functional programming is a paradigm question: you are marked on defining each idea exactly and on using it.

+ Define first-class, higher-order, pure and immutable separately and precisely, with an example of each
+ Give the type of map, filter and reduce results: a list, a shorter list, and a single value
+ Trace a pipeline stage by stage, writing down the intermediate list after each one
+ Connect purity to benefits: testing, reasoning, parallel processing and caching
+ Remember that composition order matters, and apply the right-most function first
""",
    mistakes=[
        "Saying map changes the original list, when it builds a new one.",
        "Describing a function that prints, or changes a global, as pure.",
        "Applying composed functions in the wrong order.",
        "Confusing a higher-order function with any function that is complicated.",
        "Forgetting that reduce returns one value, not a list.",
    ],
    quiz=[
        Q("What does it mean for a function to be a first-class object?",
          ["It can be stored in a variable, passed to a function and returned from a function",
           "It is the first function that the program calls when it starts to run",
           "It is a function that can only be called once and is then deleted",
           "It is a function that takes no parameters and returns no value"], 0,
          "A first-class value is treated like any other value, and that is what makes higher-order functions possible."),
        Q("What does `map(f, items)` return?",
          ["The results of applying f to every item", "Only the items for which f is true",
           "A single value combining every item", "The first item with f applied"], 0,
          "Map builds a new list, the same length as the original, with the function applied to each item."),
        Q("What does `filter(f, items)` return?",
          ["The items for which f returns True", "The results of applying f to every item",
           "The items for which f returns False", "A single combined value"], 0,
          "Filter keeps the items that pass the test, so its result can be shorter than the original list."),
        Q("What does `reduce(lambda a, b: a + b, [1, 2, 3, 4])` return?",
          ["10", "[1, 2, 3, 4]", "[3, 6, 10]", "24"], 0,
          "It combines the items two at a time: 1+2=3, 3+3=6, 6+4=10. The result is a single value."),
        Q("Which describes a pure function?",
          ["It gives the same output for the same input and has no side effects",
           "It uses only local variables but may print to the screen",
           "It changes a global variable only once", "It never takes any arguments"], 0,
          "Both conditions must hold. A function that prints, or changes anything outside itself, has a side effect."),
        Q("Which of these is a side effect?",
          ["Changing the contents of a list that was passed in as an argument",
           "Building and returning a brand new list from the arguments",
           "Creating a local variable inside the body of the function",
           "Calling a different function that is itself pure"], 0,
          "A side effect is any change made outside the function's own result, and mutating an argument is one."),
        Q("Why is immutable data useful in functional programming?",
          ["A value cannot be changed unexpectedly by another part of the program",
           "It always uses less memory than mutable data", "It allows a function to have side effects",
           "It makes recursion unnecessary"], 0,
          "If nothing can change, a function's result can only depend on its arguments."),
        Q("What are `head([4, 5, 6])` and `tail([4, 5, 6])`?",
          ["4 and [5, 6]", "6 and [4, 5]", "[4] and [5, 6]", "4 and 6"], 0,
          "The head is the first item and the tail is the list of everything after it."),
        Q("What is partial application?",
          ["Supplying some of a function's arguments to get a new function that takes the rest",
           "Applying a function to the first half of a list and ignoring the rest",
           "Calling a function with no arguments so that it uses its default values",
           "Running only the first part of a function and then stopping early"], 0,
          "partial(power, exponent=2) gives a new function of one argument, made from a function of two."),
        Q("What is composition of two functions?",
          ["Combining them so that the output of one is the input of the other", "Defining both in the same file",
           "Applying both to the same input and adding the results", "Writing one inside the other so neither can be called"], 0,
          "Composing f and g gives a function that computes f(g(x)), applying g first."),
    ],
    exam=[
        EQ("State what is meant by a first-class object.", 2, [
            MP("A value that can be assigned to a variable", ["assigned", "variable", "stored", "store"]),
            MP("It can be passed as an argument to, or returned as the result of, a function", ["passed", "argument", "parameter", "returned", "result", "return"]),
        ], "A first-class object is a value that can be treated like any other data. It can be assigned to a variable or stored in a data structure, passed as an argument to a function and returned as the result of a function. In functional programming, functions are first-class objects.",
           command="State"),
        EQ("Describe what the higher-order function filter does.", 3, [
            MP("It takes a function and a list as arguments", ["takes a function", "function and a list", "function as an argument", "two arguments", "function and list"]),
            MP("The function is applied to each item and returns true or false", ["true or false", "boolean", "test", "condition", "each item"]),
            MP("It returns a new list containing only the items for which the function returned true", ["new list", "only the items", "items for which", "keeps", "returns the items", "those items"]),
        ], "Filter takes a function that returns true or false, and a list. It applies the function to each item in the list, and returns a new list that contains only those items for which the function returned true. The original list is not changed.",
           command="Describe"),
        EQ("The program shown is run. Show the result of each stage of the pipeline and state the value that is output.", 4, [
            MP("filter keeps 3, 8 and 6", ["3, 8, 6", "3 8 6", "[3, 8, 6]"]),
            MP("map doubles them to 6, 16 and 12", ["6, 16, 12", "6 16 12", "[6, 16, 12]"]),
            MP("reduce adds them together", ["adds", "sum", "total", "combine", "6 + 16", "22"]),
            MP("The output is 34", ["34"]),
        ], "filter keeps the numbers greater than 2, which gives 3, 8 and 6. map doubles each of them, giving 6, 16 and 12. reduce then adds the values together, 6 + 16 = 22 and 22 + 12 = 34, so the value output is 34.",
           command="Show",
           figure="""```python
from functools import reduce

nums = [3, 8, 1, 6]
result = reduce(lambda a, b: a + b,
                map(lambda n: n * 2,
                    filter(lambda n: n > 2, nums)))
print(result)
```"""),
        EQ("Explain why a pure function is easier to test than a function that has side effects.", 4, [
            MP("A pure function always returns the same output for the same input", ["same output", "same result", "same input", "predictable", "always returns"]),
            MP("So a test only needs to supply the arguments and check the returned value", ["only needs", "supply the arguments", "check the value", "check the result", "simple", "returned value"]),
            MP("A function with side effects may change or depend on something outside it, such as a global variable or file", ["outside", "global", "file", "depends on", "state", "changes"]),
            MP("So the test would have to set up and check that outside state as well, and results may differ between runs", ["set up", "check the state", "different results", "differ", "more complicated", "depends on when", "also have to"]),
        ], "A pure function always returns the same output for the same arguments and does nothing else, so a test only has to supply the arguments and compare the returned value with what is expected. A function with side effects may depend on or change something outside itself, such as a global variable or a file, so a test would also have to set up that state beforehand and check it afterwards, and the same call might give different results on different runs.",
           command="Explain"),
        EQ("Write a Python function called make_multiplier that takes a number n and returns a new function. The new function takes a value x and returns x multiplied by n. Show how it could be used to create a function that triples a number.", 4, [
            MP("Defines make_multiplier with parameter n", ["def make_multiplier", "make_multiplier", "def"]),
            MP("Defines an inner function, or a lambda, that takes x", ["def multiply", "lambda x", "inner", "def"]),
            MP("The inner function returns x * n, using n from the enclosing function", ["x * n", "n * x", "return"]),
            MP("The outer function returns the inner function, and triple = make_multiplier(3) is used", ["return multiply", "return inner", "make_multiplier(3)", "triple", "return lambda"]),
        ], r"""```python
def make_multiplier(n):
    def multiply(x):
        return x * n
    return multiply

triple = make_multiplier(3)
print(triple(7))
```

make_multiplier returns the inner function multiply, which still has access to n after make_multiplier has finished. That is a closure. triple is a function that multiplies by 3, so triple(7) outputs 21.""",
           command="Write"),
    ],
)
