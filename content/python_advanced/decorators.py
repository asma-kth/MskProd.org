"""Advanced Python: closures, decorators, context managers and callbacks."""
from mskbuild.models import Topic, Section, Q, EQ, MP

INPUTS = {}
EXPECT = {}

TOPIC = Topic(
    slug="closures-decorators-and-context-managers",
    title="Closures, Decorators and Context Managers",
    spec="Advanced 3",
    icon="i-tools",
    minutes=60,
    blurb="Functions that carry memory with them, functions that wrap other functions, and the with statement that guarantees clean-up. Build a counter from a closure, write decorators for counting, validating, retrying and registering, then make your own context managers, including a database transaction that rolls back.",
    fact="The at sign decorator syntax was added to Python in version 2.4 in 2004, after one of the longest debates in the language's history. The same idea, wrapping a function in another one, is what lets web frameworks such as Flask turn a function into a web page with a single line above it.",
    sections=[
        Section("Functions are objects, and closures", r"""
In Python a function is an **object** like any other. You can give it a second name, store it in a list or dictionary, pass it to another function and return it from one. A function that takes or returns functions is a **higher-order function**, such as the `key=` argument of `sorted`.

That makes something powerful possible. A function defined **inside** another can use the variables of the outer one, and it **keeps them** even after the outer function has finished. This is a **closure**: a function bundled together with the variables it uses from the scope around it.

```python
def make_counter():
    count = 0
    def counter():
        nonlocal count            # use the count from the enclosing function
        count += 1
        return count
    return counter               # hand back the inner function itself

first = make_counter()
second = make_counter()
print(first(), first(), first())
print(second())
print("the closure holds:", first.__code__.co_freevars, first.__closure__[0].cell_contents)
```

`make_counter` finished long ago, yet `count` lives on, hidden inside `counter`. Each call to `make_counter` makes a **separate** count, so `second` was not affected by `first`. A closure is a way of giving a function private memory without writing a class.

`nonlocal` is needed because assigning to `count` would otherwise create a new local variable. It tells Python to use the one in the enclosing function.

### Where Python looks for a name: LEGB

When a name is used, Python searches four scopes in order: **L**ocal (the current function), **E**nclosing (any functions around it), **G**lobal (the module) and **B**uilt-in (`len`, `print`, ...). The first match wins.

```python
x = "global"

def outer():
    x = "enclosing"
    def inner():
        x = "local"
        print(x)
    inner()
    print(x)

outer()
print(x)
```

### A famous trap: late binding

A closure remembers the **variable**, not its value at the time. If you make several functions in a loop, they all share the same loop variable, which has its final value by the time any of them is called:

```python
funcs = [lambda: i for i in range(3)]
print([f() for f in funcs])               # all three see the final i

funcs = [lambda i=i: i for i in range(3)]  # a default argument captures the value NOW
print([f() for f in funcs])
```

The fix, `i=i`, saves the *current* value of `i` as a default for each function.
"""),
        Section("Decorators", r"""
A **decorator** is a function that takes a function and returns a **new function** that adds behaviour around it, without changing the original's code. The `@` syntax is a shortcut:

```text
@decorator
def f(): ...          means the same as:    f = decorator(f)
```

Here is the usual shape: a wrapper that accepts any arguments, does something before or after, and calls the original. This decorator counts how many times a function is called.

```python
import functools

def count_calls(func):
    @functools.wraps(func)                 # copy the name and docstring onto the wrapper
    def wrapper(*args, **kwargs):
        wrapper.calls += 1
        return func(*args, **kwargs)       # pass everything through to the real function
    wrapper.calls = 0
    return wrapper

@count_calls
def greet(name):
    '''Say hello.'''
    return "Hello, " + name

greet("Ana")
greet("Raj")
print("called", greet.calls, "times")
print(greet.__name__, "-", greet.__doc__)
```

`*args, **kwargs` collects any positional and keyword arguments, so the wrapper works for a function with any signature. Without `functools.wraps`, the decorated function would show up as `wrapper`, with its docstring lost, which makes debugging much harder:

```python
def bare(func):
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@bare
def other():
    '''A helpful docstring.'''

print(other.__name__, "-", other.__doc__)
```

### Decorators that check

A decorator is a good home for a rule that applies to many functions, such as validating arguments:

```python
import functools

def positive_args(func):
    @functools.wraps(func)
    def wrapper(*args):
        for value in args:
            if value <= 0:
                raise ValueError(func.__name__ + " needs positive numbers, got " + str(value))
        return func(*args)
    return wrapper

@positive_args
def area(width, height):
    return width * height

print(area(3, 4))
try:
    area(3, -1)
except ValueError as problem:
    print(problem)
```

### Timing

The best known decorator measures how long a function takes:

```python
# varies
import functools
import time

def timed(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(func.__name__, "took", round((time.perf_counter() - start) * 1000, 2), "ms")
        return result
    return wrapper

@timed
def total(n):
    return sum(range(n))

print(total(1000000))
```

### Stacking

Several decorators can be stacked. They are applied from the bottom upwards, so the one nearest the function wraps it first:

```python
def bracket(func):
    return lambda: "[" + func() + "]"

def exclaim(func):
    return lambda: func() + "!"

@bracket
@exclaim
def first():
    return "hello"

@exclaim
@bracket
def second():
    return "hello"

print(first())
print(second())
```

!key The pattern :: A decorator is a function that returns a function. The wrapper inside it is a closure, which is how it remembers the original function. Everything in this topic so far has been a use of that one idea.
"""),
        Section("Decorators with arguments, caching and registries", r"""
Sometimes a decorator needs settings of its own, such as `@repeat(3)`. That needs **one more layer**: a function that takes the settings and returns the actual decorator.

```python
import functools

def repeat(times):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            result = None
            for _ in range(times):
                result = func(*args, **kwargs)
            return result
        return wrapper
    return decorator

@repeat(3)
def cheer():
    print("hip hip hooray")

cheer()
```

`repeat(3)` runs first and returns `decorator`, which is then applied to `cheer`. A useful real example is **retrying** a task that sometimes fails, such as a network request:

```python
import functools

def retry(attempts):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, attempts + 1):
                try:
                    return func(*args, **kwargs)
                except ConnectionError as problem:
                    print("attempt", attempt, "failed:", problem)
            raise ConnectionError("gave up after " + str(attempts) + " attempts")
        return wrapper
    return decorator

state = {"calls": 0}

@retry(4)
def flaky():
    state["calls"] += 1
    if state["calls"] < 3:
        raise ConnectionError("no signal")
    return "connected"

print(flaky())
```

### Caching

You met `functools.lru_cache` in the recursion topic. It is a decorator that remembers results, so a repeated call with the same arguments costs nothing:

```python
import functools

@functools.lru_cache(maxsize=None)
def fib(n):
    return n if n < 2 else fib(n - 1) + fib(n - 2)

print(fib(30))
print(fib.cache_info())
```

### Registries: decorators that collect functions

A decorator does not have to wrap anything. It can simply **record** the function in a table, and return it unchanged. This is how web frameworks know which function handles which address, and how plug-in systems and command lines are built.

```python
commands = {}

def command(name):
    def register(func):
        commands[name] = func
        return func
    return register

@command("hello")
def hello(argument):
    return "Hello, " + argument + "!"

@command("shout")
def shout(argument):
    return argument.upper()

def run(line):
    name, _, argument = line.partition(" ")
    handler = commands.get(name)
    return handler(argument) if handler else "unknown command: " + name

for line in ["hello Ana", "shout quiet please", "dance now"]:
    print(run(line))
print("registered:", sorted(commands))
```

This is the routing table from the networks topic, built by decorators. In Flask, `@app.get("/api/scores")` does exactly this: it registers the function under that method and path.

### A class as a decorator

Anything **callable** can be a decorator, including a class with a `__call__` method. It suits decorators that need to keep state:

```python
import functools

class CountCalls:
    def __init__(self, func):
        functools.update_wrapper(self, func)
        self.func = func
        self.calls = 0

    def __call__(self, *args, **kwargs):
        self.calls += 1
        return self.func(*args, **kwargs)

@CountCalls
def add(a, b):
    return a + b

add(1, 2)
add(3, 4)
print(add.calls, add.__name__)
```
"""),
        Section("Context managers and the with statement", r"""
Some things must be undone however a block of code ends: a file closed, a lock released, a database change committed or abandoned. Writing `try` and `finally` every time is easy to forget. The **`with` statement** guarantees the clean-up.

```python
with open("notes.txt", "w") as handle:       # the file is closed when the block ends,
    handle.write("hello")                    # even if an error happens inside

print("closed afterwards:", handle.closed)
```

An object works with `with` if it is a **context manager**: it has `__enter__`, which runs at the start, and `__exit__`, which runs at the end, **always**, and is told about any exception.

```python
class Section:
    def __init__(self, name):
        self.name = name

    def __enter__(self):
        print("enter", self.name)
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print("exit", self.name, "| error:", exc_type.__name__ if exc_type else None)
        return False                          # False: do not hide an exception

with Section("A"):
    print("working")

try:
    with Section("B"):
        raise ValueError("oops")
except ValueError:
    print("caught outside")
```

Section B's `exit` still ran, then the error carried on up. If `__exit__` returned `True`, the exception would be swallowed.

### The short way: contextlib

A class is a lot of code for a simple idea. `contextlib.contextmanager` turns a **generator** into a context manager. Everything before the `yield` is the entry, everything after is the exit, and a `try`/`finally` makes sure the exit always runs.

```python
from contextlib import contextmanager

@contextmanager
def indent(level):
    print("  " * level + "{")
    try:
        yield
    finally:
        print("  " * level + "}")

with indent(0):
    with indent(1):
        print("    inside")

settings = {"debug": False, "colour": "blue"}

@contextmanager
def override(**changes):
    saved = dict(settings)
    settings.update(changes)
    try:
        yield settings
    finally:
        settings.clear()
        settings.update(saved)           # put everything back

with override(debug=True):
    print(settings)
print(settings)
```

### Ready made ones

```python
import io
from contextlib import redirect_stdout, suppress

with suppress(FileNotFoundError):         # ignore one kind of error on purpose
    open("missing.txt")
print("carried on")

buffer = io.StringIO()
with redirect_stdout(buffer):             # capture what print would show
    print("captured")
print(repr(buffer.getvalue()))
```

### A transaction

A database connection is a context manager too. Leaving the block normally **commits** the changes, and leaving it with an exception **rolls them back**, so the money cannot be taken from one account without being added to the other.

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.execute("create table accounts (name text, balance int)")
conn.executemany("insert into accounts values (?, ?)", [("amy", 100), ("ben", 50)])
conn.commit()

def transfer(amount):
    with conn:
        conn.execute("update accounts set balance = balance - ? where name = 'amy'", (amount,))
        if amount > 100:
            raise ValueError("amy cannot afford that")
        conn.execute("update accounts set balance = balance + ? where name = 'ben'", (amount,))

transfer(30)
print(conn.execute("select * from accounts").fetchall())

try:
    transfer(500)
except ValueError as problem:
    print(problem)
print(conn.execute("select * from accounts").fetchall())
```

The failed transfer had already taken 500 from Amy before the check, yet her balance is unchanged: the rollback undid it.
"""),
        Section("Callbacks and partial application", r"""
Because functions are objects, you can hand one to another piece of code to be **called back** later. The code that calls it does not need to know what it does. This is how buttons in tkinter and keys in pygame call your code, and how sorting calls your `key` function.

### Fixing some arguments: partial

`functools.partial` takes a function and fixes some of its arguments, returning a new function with fewer to supply. `operator.itemgetter` builds a function that picks items out, which is neater than a `lambda` for sort keys:

```python
from functools import partial
from operator import itemgetter

def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
cube = partial(power, exponent=3)
print(square(5), cube(2))

students = [("Ana", 82), ("Raj", 91), ("Mia", 82)]
print(sorted(students, key=itemgetter(1, 0)))                 # by mark, then by name
print(sorted(students, key=itemgetter(1), reverse=True))      # highest mark first
```

### Events: an observer in a few lines

A common design has some code **announce** that something happened, and any number of other pieces **subscribe** to listen. Nobody has to know about each other. This uses a dictionary of lists of functions, and a decorator to subscribe:

```python
handlers = {}

def on(event):
    def register(func):
        handlers.setdefault(event, []).append(func)
        return func
    return register

def emit(event, *args):
    for handler in handlers.get(event, []):
        handler(*args)

@on("score")
def update_board(points):
    print("board shows", points)

@on("score")
def play_sound(points):
    print("ding!" if points >= 100 else "tick")

emit("score", 120)
emit("score", 40)
```

Adding a new reaction, such as saving a high score, means writing one more function with `@on("score")`. The code that calls `emit` does not change at all. This is the **observer** pattern.

!exam Closure, decorator, callback :: A closure is a function that remembers variables from its enclosing scope. A decorator is a function that takes a function and returns a wrapped one. A callback is a function passed to other code to be called later. Questions ask for a definition and a use, and for the output of a short example.
"""),
    ],
    keyterms=[
        ("Higher-order function", "A function that takes another function as an argument, or returns one."),
        ("Closure", "A function together with the variables it uses from its enclosing scope, which it keeps after the outer function has finished."),
        ("nonlocal", "A statement that makes an assignment in an inner function use a variable of the enclosing function."),
        ("Decorator", "A function that takes a function and returns a new function that adds behaviour around it, applied with the @ syntax."),
        ("functools.wraps", "A decorator for wrappers that copies the original function's name and docstring onto the wrapper."),
        ("Context manager", "An object with __enter__ and __exit__ methods, used with `with` so that clean-up always happens."),
        ("Transaction", "A group of database changes that are either all made (commit) or all undone (rollback)."),
        ("Callback", "A function passed to other code, to be called when something happens."),
        ("Partial application", "Fixing some of a function's arguments to make a new function that needs fewer."),
        ("Observer pattern", "A design in which code announces events and any number of other functions subscribe to react to them."),
    ],
    grade="""
Decorator and closure questions ask you to trace code and to explain the mechanism.

+ Define a closure as a function that remembers the variables of its enclosing scope after that scope has ended
+ State that @decorator above def f means f = decorator(f), and trace what the wrapper does around the call
+ Say what functools.wraps is for: preserving the name and docstring
+ For with, say the exit always runs, even after an exception
+ Say each call to the outer function makes a separate closure with its own variables
""",
    mistakes=[
        "Forgetting `return func(...)` in a wrapper, so the decorated function always returns None.",
        "Forgetting `nonlocal`, so an assignment inside the inner function creates a new local instead of changing the outer variable.",
        "Writing `@repeat` when a decorator that takes arguments needs `@repeat(3)`.",
        "Expecting a lambda made in a loop to remember the loop's earlier values. It sees the final one.",
        "Writing `try` and `finally` by hand for every file or lock, when `with` does it correctly.",
    ],
    quiz=[
        Q("What is a closure?",
          ["A function that remembers variables from the scope it was defined in", "A function that has no return value", "A function that closes a file", "A function with no parameters"], 0,
          "The inner function keeps the variables it uses from the enclosing function, even after that function has returned."),
        Q("What does `nonlocal count` do inside an inner function?",
          ["Makes assignments to count change the enclosing function's variable", "Makes count a global variable", "Deletes count", "Prevents count being used"], 0,
          "Without it, assigning to count would create a new local variable instead."),
        Q("A function make_counter() returns a closure with its own count. If you call it twice, what do the two closures share?",
          ["Nothing: each has its own count", "The same count", "Only the function name", "The return value"], 0,
          "Each call to make_counter creates a separate set of variables."),
        Q("What does `@my_decorator` above `def f():` mean?",
          ["f = my_decorator(f)", "my_decorator = f(my_decorator)", "f runs my_decorator once", "f is deleted"], 0,
          "The @ line is a shortcut that replaces f with whatever the decorator returns."),
        Q("Why is `functools.wraps` used in a decorator?",
          ["To keep the original function's name and docstring on the wrapper", "To make the function run faster", "To make the function private", "To catch exceptions"], 0,
          "Without it the decorated function would be reported as wrapper and its documentation lost."),
        Q("What does `*args, **kwargs` allow a wrapper function to do?",
          ["Accept and pass on any arguments", "Accept only keyword arguments", "Return several values", "Skip the original function"], 0,
          "It collects every positional and keyword argument so that the wrapper works for any function."),
        Q("What is the extra layer needed for a decorator such as @repeat(3)?",
          ["A function that takes the argument and returns the actual decorator", "A global variable to hold the 3", "A class to wrap the function", "A second @ line"], 0,
          "repeat(3) is called first, and the decorator it returns is then applied to the function."),
        Q("When does the __exit__ method of a context manager run?",
          ["At the end of the with block, even if an exception occurred", "Only if no exception occurred", "At the start of the block", "When the program ends"], 0,
          "That guarantee is the reason for using with."),
        Q("In a database transaction used in a with block, what happens if an exception is raised inside the block?",
          ["The changes are rolled back", "The changes are committed", "The database is deleted", "The changes are kept but not saved"], 0,
          "Either all the changes in the transaction are made, or none of them are."),
        Q("What is a callback?",
          ["A function passed to other code, to be called later", "A function that calls itself", "A function that returns its arguments", "An error handler for files"], 0,
          "The code that calls it does not need to know what it does."),
    ],
    exam=[
        EQ("Explain what is meant by a closure in Python.", 3, [
            MP("A closure is a function defined inside another function", ["inside another", "inner function", "nested", "defined inside"]),
            MP("It uses variables from the enclosing function", ["enclosing", "outer function", "variables from", "scope"]),
            MP("It keeps (remembers) those variables even after the outer function has finished", ["keeps", "remembers", "after", "finished", "returned"]),
        ], "A closure is a function that is defined inside another function and uses variables from the enclosing function. It keeps, or remembers, those variables even after the outer function has finished running, so the inner function can carry on using them when it is called later.",
           command="Explain"),
        EQ("The program shown is run. State the output and explain why the second and third values printed are different.", 4, [
            MP("The output is 1 2 1", ["1 2 1", "1, 2, 1"]),
            MP("Each call of make_counter creates a new function with its own variable count", ["own", "separate", "new count", "each call", "different count"]),
            MP("a() adds 1 to the count that belongs to a, so the second call gives 2", ["a()", "belongs to a", "increases", "adds 1", "second call"]),
            MP("b has its own count, which starts again at 0, so its first call gives 1", ["b has", "b's", "starts at 0", "starts again", "first call"]),
        ], "The output is 1 2 1. Each call of make_counter creates a new inner function with its own variable count. The first two calls to a each add 1 to the count that belongs to a, giving 1 and then 2. The function b has its own separate count, which starts at 0, so its first call gives 1.",
           command="State",
           figure="""```python
def make_counter():
    count = 0
    def counter():
        nonlocal count
        count += 1
        return count
    return counter

a = make_counter()
b = make_counter()
print(a(), a(), b())
```"""),
        EQ("Write a decorator called log_calls that prints the name of the function it decorates each time that function is called, and then calls the function and returns its result. The decorated function may have any parameters.", 5, [
            MP("A function that takes a function as a parameter", ["def log_calls", "func", "def"]),
            MP("Defines a wrapper function inside it which accepts any arguments (*args, **kwargs)", ["*args", "**kwargs", "wrapper"]),
            MP("The wrapper prints the name of the function", ["print", "__name__"]),
            MP("The wrapper calls the original function with the arguments and returns its result", ["return func", "func(*args", "return"]),
            MP("The decorator returns the wrapper", ["return wrapper"]),
        ], r"""```python
def log_calls(func):
    def wrapper(*args, **kwargs):
        print("calling", func.__name__)
        return func(*args, **kwargs)
    return wrapper

@log_calls
def add(a, b):
    return a + b

print(add(2, 3))
```

log_calls takes the function as a parameter and defines a wrapper inside it. The wrapper accepts any arguments, prints the function's name, calls the original function with those arguments and returns what it returns. log_calls then returns the wrapper, which replaces the original function when the @ syntax is used.""",
           command="Write"),
        EQ("Explain why using a with statement to open a file is better than calling open and close separately.", 3, [
            MP("The file is closed automatically at the end of the with block", ["automatically", "closed", "end of the block"]),
            MP("This happens even if an error (exception) occurs inside the block", ["even if", "error", "exception", "always"]),
            MP("With separate open and close, the close call could be skipped, leaving the file open and data possibly not saved", ["skipped", "left open", "not saved", "forget", "never closed", "locked"]),
        ], "With a with statement the file is closed automatically as soon as the block ends, and this happens even if an error occurs inside the block. If open and close are called separately, an error between them can mean the close call is never reached, or the programmer may forget it, leaving the file open so that data may not be saved and the file may stay locked.",
           command="Explain"),
        EQ("Discuss the advantages and disadvantages of using decorators in a large program.", 6, [
            MP("A decorator lets the same extra behaviour, such as logging, timing or checking, be added to many functions without repeating the code", ["without repeating", "reuse", "many functions", "repeat", "same code", "reduces duplication"]),
            MP("The original function stays simple and focused on its own job (separation of concerns)", ["simple", "focused", "separation", "own job", "cleaner"]),
            MP("The behaviour can be added or removed by adding or removing one line", ["one line", "added or removed", "easy to change", "switch off"]),
            MP("Disadvantage: the behaviour is hidden above the function so a reader may not realise it is there, and it can be harder to follow", ["hidden", "harder to read", "harder to follow", "not realise", "confusing", "obscure"]),
            MP("Disadvantage: the extra layer of function calls can make debugging more difficult and slightly slower, and a poorly written one can lose the function's name", ["debug", "slower", "overhead", "wraps", "name", "stack trace"]),
            MP("A reasoned conclusion: worthwhile for behaviour shared across many functions, but should be kept small and documented", ["conclusion", "worthwhile", "overall", "therefore", "documented", "use them for", "i would"]),
        ], "A decorator lets the same extra behaviour, such as logging, timing, checking arguments or caching, be added to many functions without repeating the code in each, so the program is shorter and the code is easier to maintain. Each original function stays simple and concentrates on its own job, and the extra behaviour can be added or removed by adding or removing a single line. There are disadvantages. The behaviour is hidden above the function, so a reader may not realise it is there, which can make the code harder to follow. The extra layer of function calls can also make debugging more difficult and slightly slower, and a badly written decorator can lose the original function's name and documentation. Decorators are therefore worthwhile for behaviour shared by many functions, provided each is kept small and documented.",
           command="Discuss"),
    ],
)
