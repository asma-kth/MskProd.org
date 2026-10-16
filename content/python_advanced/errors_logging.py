"""Advanced Python: exceptions, custom exceptions, assertions, logging and debugging."""
from mskbuild.models import Topic, Section, Q, EQ, MP

INPUTS = {}
EXPECT = {}

TOPIC = Topic(
    slug="exceptions-logging-and-defensive-code",
    title="Exceptions, Logging and Defensive Code",
    spec="Advanced 5",
    icon="i-bug",
    minutes=60,
    blurb="Handle errors on purpose. The full try, except, else and finally statement, custom exception hierarchies, raising from another error, assertions and design by contract, the logging module with levels and handlers, and a method for reading a traceback and testing the failure paths.",
    fact="The most famous bug is a moth. In 1947 operators of the Harvard Mark II computer found one trapped in a relay and taped it into the logbook, with the note 'first actual case of bug being found'. The joke worked because engineers had been calling faults bugs for at least seventy years, and Edison used the word in the 1870s.",
    sections=[
        Section("The try statement in full", r"""
You have used `try` and `except` to stop a program crashing. The full statement has four parts, and each has a job:

```text
try:        the code that might fail
except:     what to do if it does
else:       what to do if it did NOT fail
finally:    what must happen either way
```

```python
def divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("cannot divide by zero")
        return None
    except TypeError as problem:
        print("bad types:", problem)
        return None
    else:
        print("division worked")
        return result
    finally:
        print("done with", repr(a), repr(b))

print(divide(10, 2))
print(divide(1, 0))
print(divide("a", 2))
```

Watch the order of the output. `else` runs only when there was no exception, so the *success* code goes there, which keeps `try` as short as possible and stops it hiding unrelated errors. `finally` runs **always**, even if the function returns or an error is not caught, which is why it is where clean-up goes.

```python
def f():
    try:
        return "try"
    finally:
        print("finally runs before the function returns")

print(f())
```

### Exceptions form a family tree

Every exception is a class, and they inherit from each other. Catching a parent catches all its children:

```python
for kind in (ZeroDivisionError, KeyError, FileNotFoundError):
    parents = " <- ".join(c.__name__ for c in kind.__mro__[1:-1])
    print(kind.__name__, "<-", parents)
```

`except LookupError` catches both `KeyError` and `IndexError`. `except Exception` catches nearly everything. That is why **order matters**: put the specific handlers first, because Python uses the first one that fits.

```python
try:
    {}["x"]
except LookupError:
    print("LookupError caught first")
except KeyError:
    print("never reached: a KeyError is also a LookupError")
```

!warn Never write a bare except :: `except:` on its own catches everything, including the keyboard interrupt that lets you stop a runaway program, and hides real bugs. Catch the specific errors you can deal with, and let the rest crash loudly where you can see them.

### Raising, re-raising and chaining

`raise` throws an exception of your own. Inside an `except` block, a bare `raise` re-throws the one being handled, which is useful for logging an error and then letting it carry on. `raise ... from ...` throws a *new* exception while keeping the original as its **cause**, so nothing is lost:

```python
def load_age(text):
    try:
        return int(text)
    except ValueError as problem:
        raise ValueError("age must be a whole number, got " + repr(text)) from problem

try:
    load_age("abc")
except ValueError as error:
    print(error)
    print("caused by:", repr(error.__cause__))
```

The new message is meaningful to whoever called `load_age`, and the technical reason is still attached.
"""),
        Section("Custom exceptions and where to catch them", r"""
The built-in exceptions describe *Python's* problems: `ValueError`, `KeyError`. Your program has its own: an overdrawn account, an unknown product, a game that is over. A **custom exception** is a class that inherits from `Exception`, and it names a problem in your program's own words.

```python
class BankError(Exception):
    '''Everything that can go wrong in the bank.'''

class InsufficientFunds(BankError):
    def __init__(self, balance, wanted):
        super().__init__("balance " + str(balance) + " is less than " + str(wanted))
        self.balance = balance                 # keep the facts, for whoever catches it
        self.wanted = wanted

class AccountClosed(BankError):
    pass

class Account:
    def __init__(self, balance):
        self.balance = balance
        self.open = True

    def withdraw(self, amount):
        if not self.open:
            raise AccountClosed("account is closed")
        if amount > self.balance:
            raise InsufficientFunds(self.balance, amount)
        self.balance -= amount
        return self.balance

account = Account(50)
for amount in (20, 100):
    try:
        print("left:", account.withdraw(amount))
    except InsufficientFunds as problem:
        print("short by", problem.wanted - problem.balance, "|", problem)
    except BankError as problem:               # anything else the bank can raise
        print("bank problem:", problem)

account.open = False
try:
    account.withdraw(1)
except BankError as problem:
    print(type(problem).__name__, "-", problem)
```

A **hierarchy** with one base class (`BankError`) lets a caller choose how precisely to catch. Handle `InsufficientFunds` to offer a loan. Handle `BankError` to show a generic apology. And an exception object can carry data, so the handler does not have to parse a message.

### Where should an exception be caught?

Catch an exception **at the level that knows what to do about it**. The function that discovers the problem usually does not: `withdraw` cannot know whether to show a message, ask for another amount or cancel an order. So it raises, the exception travels up the call stack through the callers that cannot deal with it, and the first one that can, catches it.

### Ask forgiveness, not permission

There are two styles for code that might fail:

| Style | Looks like | Python's preference |
| **LBYL**: look before you leap | `if key in config:` then `config[key]` | for cheap, clear checks |
| **EAFP**: easier to ask forgiveness than permission | `try: config[key]` `except KeyError:` | the usual Python style |

EAFP avoids a gap in time. If you check that a file exists and then open it, the file might be deleted in between. Opening it and handling `FileNotFoundError` has no gap.
"""),
        Section("Assertions and defensive design", r"""
An **assertion** states something that *must* be true. If it is false, the program stops at once with an `AssertionError`:

```python
def average(marks):
    assert len(marks) > 0, "average needs at least one mark"
    return sum(marks) / len(marks)

print(average([7, 9]))
try:
    average([])
except AssertionError as problem:
    print("assertion failed:", problem)
```

### An assertion is not input validation

Exceptions and assertions look alike but answer different questions:

| | Exception | Assertion |
| For | things that can go wrong **at run time**, such as bad input, a missing file, a network failure | things that can **only** be false if the **programmer made a mistake** |
| Example | the user typed `abc` for an age | this list should never be empty at this point |
| Can be switched off? | no | **yes** |

Python can **remove assertions** when it runs with the `-O` option, to save time. A program that relies on an `assert` to reject bad input would then accept it. See it happen:

```python
source = "assert False, 'boom'\nprint('the assertion was skipped')"

try:
    exec(compile(source, "<demo>", "exec"))
except AssertionError as problem:
    print("normal run:", problem)

exec(compile(source, "<demo>", "exec", optimize=1))       # what python -O does
```

So check **user input** with `if` and `raise`, and use `assert` for your own **sanity checks** while developing.

### Design by contract

A useful way to think about a function is as a **contract**:

- a **precondition**: what must be true when it is called (the caller's duty)
- a **postcondition**: what will be true when it returns (the function's duty)
- an **invariant**: something that stays true throughout, such as "the balance is never negative"

```python
def integer_sqrt(n):
    assert n >= 0, "precondition: n must not be negative"
    result = 0
    while (result + 1) * (result + 1) <= n:
        result += 1
    assert result * result <= n < (result + 1) * (result + 1), "postcondition failed"
    return result

print(integer_sqrt(50), integer_sqrt(64))
```

### Defensive programming

**Defensive programming** assumes things will go wrong, and arranges for them to fail safely and visibly:

- **validate at the boundary**, where data enters the program (input, files, the network), and then trust it inside
- **fail fast**: stop at the first sign of trouble instead of carrying bad data further
- **use safe defaults**, and never silently swallow an error
- **do not trust the caller**, or the client, or the file
- write the **tests** for the failure paths as well as for the normal ones

!key Fail loudly, not silently :: A crash with a clear message is far cheaper to fix than a wrong answer that nobody notices. The worst code is `except: pass`.
"""),
        Section("Logging", r"""
Debugging with `print` is quick, and it has problems. The output cannot be switched off without editing the code, it all looks the same, it mixes with the real output, and it goes nowhere once the program is running on a server. The **`logging`** module is the professional answer.

Each message has a **level**, saying how serious it is. A **logger** has a threshold and ignores anything below it:

| Level | Number | Use |
| `DEBUG` | 10 | detail useful only while developing |
| `INFO` | 20 | normal events: an order was accepted |
| `WARNING` | 30 | something unexpected, but the program carries on |
| `ERROR` | 40 | something failed |
| `CRITICAL` | 50 | the program cannot continue |

There are three parts to set up. A **logger** receives your messages, a **handler** decides where they go (the screen, a file, the network), and a **formatter** decides how they look.

```python
import logging
import sys

class Short(logging.Formatter):                       # keeps this demo's output short
    def formatException(self, exc_info):
        return "  (a traceback would follow: " + exc_info[0].__name__ + ")"

def make_logger(name, level):
    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.propagate = False
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(Short("%(levelname)-8s %(name)s: %(message)s"))
    logger.handlers = [handler]
    return logger

log = make_logger("orders", logging.DEBUG)
log.debug("checking stock")
log.info("order %d accepted", 17)
log.warning("stock for %s is low", "pens")
log.error("payment failed for order %d", 17)

try:
    1 / 0
except ZeroDivisionError:
    log.exception("unexpected error")                  # logs at ERROR, with the traceback

quiet = make_logger("quiet", logging.WARNING)
quiet.info("this is below the threshold, so it is hidden")
quiet.warning("this is shown")
```

Notice `log.info("order %d accepted", 17)`: the values are passed **separately** from the message, so Python only builds the string if the message is actually going to be used.

`log.exception` is meant for use inside an `except` block, and records the full **traceback**, which a `print` of the error message does not.

### Logging to a file

On your own computer, a real program logs to a file, so that you can read what happened after it has run. A **rotating** handler starts a new file when the old one is full, so that logs never fill the disk:

```pylocal
import logging
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler("app.log", maxBytes=100000, backupCount=3)
handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(name)s: %(message)s"))

log = logging.getLogger("shop")
log.setLevel(logging.INFO)
log.addHandler(handler)

log.info("server started")
log.warning("disk space is low")
```

!warn What not to log :: Never write passwords, keys, card numbers or personal details into a log. Logs get copied, emailed and kept for years, and are a favourite target. Data protection law applies to log files too.

### Logger names

A common pattern is `logging.getLogger(__name__)` at the top of each module. Each module then logs under its own name, and you can turn up the detail for just one of them while debugging, leaving the rest quiet.
"""),
        Section("Reading tracebacks and debugging professionally", r"""
When an exception is not caught, Python prints a **traceback**: the chain of calls that led to it, **oldest first**, ending with the error itself:

```text
Traceback (most recent call last):
  File "shop.py", line 22, in <module>
    total = checkout(basket)
  File "shop.py", line 14, in checkout
    return sum(price_of(item) for item in basket)
  File "shop.py", line 9, in price_of
    return PRICES[item]
KeyError: 'pencil'
```

Read it **from the bottom**. The last line says what happened: a `KeyError` for `'pencil'`. The line above says where: `price_of`, line 9. The frames above that explain how the program *got* there. The bug is at the bottom, but the cause might be anywhere above it. Perhaps `checkout` was given an item that was never in the price list.

A program can examine a traceback too:

```python
import traceback

def level3():
    return 1 / 0

def level2():
    return level3()

def level1():
    return level2()

try:
    level1()
except ZeroDivisionError as error:
    frames = traceback.extract_tb(error.__traceback__)
    print([frame.name for frame in frames])
    print(type(error).__name__, "-", error)
```

### A method for debugging

1. **Reproduce it.** If you cannot make it fail, you cannot know you have fixed it.
2. **Isolate it.** Cut the program down to the smallest version that still fails. Half the bugs are found at this stage.
3. **Read the evidence**: the traceback, the logs, the values of the variables.
4. **Form a hypothesis**, a specific guess about the cause, and **test one thing at a time**.
5. **Fix the cause**, not the symptom.
6. **Write a test** that fails without the fix and passes with it, so the bug cannot come back.

For step 3 the debugger is better than scattered prints. Call `breakpoint()` where you want to stop, and Python opens an interactive prompt there:

```pylocal
def total(prices):
    result = 0
    for price in prices:
        breakpoint()          # the program pauses here
        result += price
    return result

total([3, 4, 5])
```

At the `(Pdb)` prompt: `p price` prints a variable, `n` runs the next line, `s` steps into a call, `c` continues, `l` lists the code around you and `q` quits.

### Test the failure paths

The tests that matter most are often the ones for what should go *wrong*. `assertRaises` checks that the right exception is raised:

```python
import io
import unittest

class InsufficientFunds(Exception):
    pass

class AccountClosed(Exception):
    pass

class Account:
    def __init__(self, balance):
        self.balance = balance
        self.open = True

    def withdraw(self, amount):
        if not self.open:
            raise AccountClosed("account is closed")
        if amount > self.balance:
            raise InsufficientFunds("not enough money")
        self.balance -= amount
        return self.balance

class TestAccount(unittest.TestCase):
    def test_too_much(self):
        with self.assertRaises(InsufficientFunds):
            Account(50).withdraw(100)

    def test_normal(self):
        self.assertEqual(Account(50).withdraw(20), 30)

    def test_closed(self):
        account = Account(50)
        account.open = False
        with self.assertRaises(AccountClosed):
            account.withdraw(1)

suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestAccount)
result = unittest.TextTestRunner(stream=io.StringIO(), verbosity=0).run(suite)
print("tests run:", result.testsRun, "| failures:", len(result.failures), "| errors:", len(result.errors))
```

!exam Name the type, then the cause :: An error question gives marks for naming the type of error (syntax, runtime or logic), and for saying what caused it. A traceback gives you both, if you read it from the last line.
"""),
    ],
    keyterms=[
        ("Exception", "An object that represents an error or unusual event, which interrupts normal flow until it is caught."),
        ("try / except / else / finally", "The statement that runs code, handles errors, runs code only on success, and always runs clean-up code."),
        ("Custom exception", "A class that inherits from Exception and names a problem specific to a program."),
        ("Exception chaining", "Raising a new exception from inside a handler while keeping the original as its cause, with raise ... from ..."),
        ("Assertion", "A statement that a condition must be true, which stops the program with an AssertionError if it is false."),
        ("Precondition and postcondition", "What must be true when a subprogram is called, and what it promises will be true when it returns."),
        ("Invariant", "A condition that stays true throughout the execution of a part of a program."),
        ("Defensive programming", "Writing code that expects errors and unreliable input, and handles them safely."),
        ("Logging", "Recording messages with a level and a destination as a program runs, so that its behaviour can be reviewed."),
        ("Traceback", "The list of calls that were active when an exception occurred, printed with the error."),
    ],
    grade="""
Error handling questions reward knowing which tool is for which job.

+ Say that `else` runs only when no exception was raised and `finally` always runs
+ Put the specific except clauses before the general one, and say why
+ Distinguish exceptions (bad input and run-time failures) from assertions (programmer mistakes, which can be switched off)
+ For logging, name the level and say what the handler and formatter do
+ For a traceback, say you read it from the bottom: the error first, then where
""",
    mistakes=[
        "Writing a bare `except:` or `except Exception: pass`, which hides the bugs you most need to see.",
        "Using `assert` to validate input from the user, when assertions can be turned off.",
        "Putting too much code in the `try` block, so that an unrelated error is caught by accident.",
        "Printing a message instead of raising, so the caller carries on as if nothing went wrong.",
        "Logging passwords or personal data.",
    ],
    quiz=[
        Q("When does the `else` block of a try statement run?",
          ["When no exception was raised in the try block", "When an exception was raised", "Always", "Only when there is a finally block"], 0,
          "else is for the code that should run only if the try block succeeded."),
        Q("When does a `finally` block run?",
          ["Always, whether or not an exception occurred", "Only if there was an error", "Only if there was no error", "Only when the program ends"], 0,
          "It is used for clean-up that must happen however the block ends."),
        Q("Why should `except KeyError` be placed before `except LookupError`?",
          ["Python uses the first matching handler, and KeyError is a kind of LookupError", "KeyError is faster", "LookupError cannot be caught", "It makes no difference"], 0,
          "If LookupError came first it would catch the KeyError and the more specific handler would never run."),
        Q("What does `raise ValueError('bad') from original` do?",
          ["Raises a new exception while keeping the original as its cause", "Ignores the original error", "Raises the original error again", "Logs the error to a file"], 0,
          "The cause is stored in __cause__, so the technical detail is not lost."),
        Q("Why create a custom exception class, such as InsufficientFunds?",
          ["It names the problem in the program's own terms and can carry data", "It runs faster than a built-in one", "Python requires it", "It stops the error being raised"], 0,
          "Callers can catch it precisely, and the object can hold facts such as the balance."),
        Q("Which is the correct use of an assertion?",
          ["Checking something that should never be false unless the code has a bug", "Checking that the user typed a valid age", "Checking that a file exists", "Checking that a network connection works"], 0,
          "Assertions are for programmer mistakes and can be disabled, so they must not be used for input."),
        Q("What does 'fail fast' mean?",
          ["Stop at the first sign of a problem instead of carrying on with bad data", "Make the program run quickly", "Ignore errors to save time", "Restart the program after every error"], 0,
          "Catching a problem where it begins makes it far easier to find."),
        Q("Which logging level is for something unexpected where the program can carry on?",
          ["WARNING", "DEBUG", "CRITICAL", "INFO"], 0,
          "DEBUG and INFO are for detail and normal events, ERROR for failures, and CRITICAL when the program cannot go on."),
        Q("In which direction should a Python traceback be read to find the error first?",
          ["From the last line upwards", "From the first line downwards", "From the middle", "It cannot be read"], 0,
          "The final line names the error and the line above shows where it happened."),
        Q("Why is logging usually better than print for recording what a program does?",
          ["Levels and handlers let you control what is recorded and where, without changing the code", "Print cannot show numbers", "Logging is faster than print", "Print is not allowed in a program"], 0,
          "Messages can be filtered by level, formatted consistently, and sent to a file or server."),
    ],
    exam=[
        EQ("Describe the purpose of the try, except, else and finally parts of a Python try statement.", 4, [
            MP("try contains the code that might cause an error (raise an exception)", ["try", "might", "may cause", "could fail", "risky"]),
            MP("except contains the code that handles a particular error if one occurs", ["except", "handles", "handle", "catch", "deals with"]),
            MP("else runs only if no exception occurred in the try block", ["else", "no exception", "no error", "only if"]),
            MP("finally always runs, whether or not an exception occurred, and is used for clean-up", ["finally", "always", "clean", "whether or not"]),
        ], "The try block contains the code that might cause an error. The except block contains the code that handles a particular error if one occurs. The else block runs only if no exception occurred in the try block. The finally block always runs, whether or not an exception occurred, and is used for clean-up such as closing a file.",
           command="Describe"),
        EQ("The subprogram divide is called three times, as shown. State the output of the program.", 4, [
            MP("The first call outputs division worked, then done with 10 2, then 5.0", ["division worked", "5.0"]),
            MP("The second call outputs cannot divide by zero, then done with 1 0, then None", ["cannot divide by zero", "none"]),
            MP("The finally block runs in each case, after the try or except code but before the value is returned", ["done with", "finally", "always"]),
            MP("The third call outputs bad types, with the message about the operand types, then done with 'a' 2 and None", ["bad types", "operand", "unsupported", "'a'"]),
        ], "For divide(10, 2) the output is division worked, then done with 10 2, and then 5.0 is printed. For divide(1, 0) the output is cannot divide by zero, then done with 1 0, and then None is printed. For divide('a', 2) the output is bad types: unsupported operand type(s) for /: 'str' and 'int', then done with 'a' 2, and then None is printed. The finally block runs in every case, after the try or except code and just before the value is returned.",
           command="State",
           figure="""```python
def divide(a, b):
    try:
        result = a / b
    except ZeroDivisionError:
        print("cannot divide by zero")
        return None
    except TypeError as problem:
        print("bad types:", problem)
        return None
    else:
        print("division worked")
        return result
    finally:
        print("done with", repr(a), repr(b))

print(divide(10, 2))
print(divide(1, 0))
print(divide("a", 2))
```"""),
        EQ("Explain the difference between an exception and an assertion, and state when each should be used.", 4, [
            MP("An exception is raised when something goes wrong while the program is running, such as invalid input or a missing file", ["run time", "runtime", "invalid input", "missing file", "something goes wrong"]),
            MP("Exceptions should be used for problems that can occur even when the program is correct, and can be handled with try and except", ["handled", "try", "except", "even when", "expected"]),
            MP("An assertion checks that a condition that should always be true is true, and stops the program if it is not", ["condition", "always be true", "stops", "checks"]),
            MP("Assertions are for finding programmer mistakes and can be switched off, so must not be used to validate input", ["mistake", "bug", "switched off", "disabled", "not to validate", "must not"]),
        ], "An exception is raised when something goes wrong while the program is running, such as invalid input or a missing file, and it can be caught and handled using try and except. Exceptions should be used for problems that can happen even when the program is correct. An assertion checks that a condition that should always be true really is, and stops the program if it is not. Assertions are for finding mistakes made by the programmer, and because they can be switched off they must not be used to validate input.",
           command="Explain"),
        EQ("Write a custom exception class called InvalidAgeError, and a subprogram check_age that takes an age and raises an InvalidAgeError with a suitable message if the age is less than 0 or greater than 130. Otherwise the subprogram should return the age.", 4, [
            MP("A class InvalidAgeError that inherits from Exception", ["class invalidageerror", "(exception)", "exception"]),
            MP("A subprogram check_age with a parameter", ["def check_age", "def"]),
            MP("Tests whether the age is less than 0 or greater than 130", ["< 0", "> 130", "or", "age < 0"]),
            MP("Raises InvalidAgeError with a message, otherwise returns the age", ["raise invalidageerror", "raise", "return age"]),
        ], r"""```python
class InvalidAgeError(Exception):
    pass

def check_age(age):
    if age < 0 or age > 130:
        raise InvalidAgeError("age must be between 0 and 130, not " + str(age))
    return age

print(check_age(15))
try:
    check_age(200)
except InvalidAgeError as problem:
    print(problem)
```

The new class inherits from Exception. check_age tests whether the age is less than 0 or greater than 130 and raises the new exception with a message if so, and otherwise returns the age.""",
           command="Write"),
        EQ("A programmer records what a program is doing using print statements. Discuss whether the programmer should use the logging module instead.", 6, [
            MP("Logging messages have levels (debug, info, warning, error), so the amount of detail can be changed without editing the code", ["level", "debug", "info", "warning", "error", "threshold"]),
            MP("Print statements have to be found and removed or commented out when they are no longer wanted", ["removed", "edit", "commented out", "remove", "switched off"]),
            MP("Logging can send messages to a file or a server, so they can be reviewed after the program has run", ["file", "server", "after", "reviewed", "handler", "stored"]),
            MP("Log messages can carry formatting such as the time, level and module, which helps to find the cause of a problem", ["time", "format", "timestamp", "module", "date"]),
            MP("Disadvantage: logging takes more effort to set up than a print statement, and logs can grow large or contain sensitive data", ["effort", "set up", "setup", "large", "sensitive", "more complicated", "personal"]),
            MP("A reasoned conclusion: logging is better for anything beyond a small, short lived program", ["conclusion", "better", "should use", "therefore", "overall", "i would"]),
        ], "The logging module gives each message a level such as debug, info, warning or error, so the programmer can change how much detail is recorded without editing the code, whereas print statements have to be found and removed when they are no longer wanted. Logging can send messages to a file or a server, so they can be reviewed after the program has run, and each message can be formatted to include the time, the level and the module, which helps in finding the cause of a problem. On the other hand it takes more effort to set up than a print statement, and log files can become large or contain sensitive data if the programmer is not careful. For anything more than a small, short lived program the programmer should therefore use logging.",
           command="Discuss"),
    ],
)
