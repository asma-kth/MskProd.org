"""GCSE Python: reading exam pseudocode and writing the Python for it."""
from mskbuild.models import Topic, Section, Q, EQ, MP

# What to type in when tools/check_python_examples.py runs a program that
# calls input(), keyed by the block's position on the page.
INPUTS = {"exam 3 model": ["18"], "exam 5 model": ["3", "9", "7"]}

TOPIC = Topic(
    slug="pseudocode-to-python",
    title="Exam Pseudocode to Python",
    spec="GCSE 1",
    icon="i-swap",
    minutes=30,
    blurb="Every exam board prints algorithms in its own pseudocode. Every construct it uses, next to the Python that does the same job, with the traps where they differ.",
    fact="Python went thirty years without anything like a switch statement. match only arrived in Python 3.10, in 2021, and there is still no do...until loop, which is why exam answers use while True and break.",
    sections=[
        Section("Reading exam pseudocode", r"""
OCR prints algorithms in its **Exam Reference Language** (ERL). AQA prints its own **pseudocode**. Edexcel's Paper 2 is sat on a computer, in Python itself. The ideas are identical. Only the spelling differs, and the exam is easier once you can translate without thinking.

| Idea | OCR reference language | AQA pseudocode | Python |
| Assign a value | `x = 5` | `x ← 5` | `x = 5` |
| Output | `print("Hi")` | `OUTPUT "Hi"` | `print("Hi")` |
| Input | `name = input("Name? ")` | `name ← USERINPUT` | `name = input("Name? ")` |
| Count loop | `for i = 1 to 5` ... `next i` | `FOR i ← 1 TO 5` ... `ENDFOR` | `for i in range(1, 6):` |
| Loop, test first | `while x < 10` ... `endwhile` | `WHILE x < 10` ... `ENDWHILE` | `while x < 10:` |
| Loop, test last | `do` ... `until x >= 10` | `REPEAT` ... `UNTIL x >= 10` | `while True:` then `break` |
| Selection | `if` `elseif` `else` `endif` | `IF` `ELSE IF` `ELSE` `ENDIF` | `if` `elif` `else` |
| Subprogram | `function` or `procedure` | `SUBROUTINE` | `def` |

### The loop that costs the most marks

```python
# for i = 1 to 5
#     print(i)
# next i
for i in range(1, 6):
    print(i)              # 1 2 3 4 5, one per line
```

!warn The stop value is one past the last number :: In the exam `for i = 1 to 5` runs for 1, 2, 3, 4 **and 5**. In Python `range(1, 5)` stops at 4, so the Python for that loop is `range(1, 6)`. Whenever you translate a count loop, write down the last value you want and add one.

!diagram py-range-numbers

A step is the third value in `range`:

```python
# for i = 0 to 20 step 5
for i in range(0, 21, 5):
    print(i, end=" ")     # 0 5 10 15 20
print()
```

Counting down needs a negative step, and the stop value is still one past the end, in the direction you are going:

```python
# for i = 10 to 1 step -3
for i in range(10, 0, -3):
    print(i, end=" ")     # 10 7 4 1
print()
```

### Loop, test last

Python has no `do ... until`. The body must run at least once and the test comes at the bottom, so you build it from a loop that never ends on its own and a `break`:

```python
# do
#     total = total + 7
# until total > 30
total = 0
while True:
    total = total + 7
    if total > 30:
        break
print(total)              # 35
```

The condition is **the one you stop on**. `until total > 30` becomes `if total > 30: break`. Do not flip it into the loop header unless you also set up the variable first:

```python
total = 7
while total <= 30:
    total = total + 7
print(total)              # 35
```

That version gives the same answer, but only because the variable was primed to the value the first pass would have produced. The `while True` form is safer, because it cannot be wrong that way.

### Selection with many branches

```pseudo
switch day:
    case "Sat":
        print("Weekend")
    case "Sun":
        print("Weekend")
    default:
        print("Weekday")
endswitch
```

```python
day = "Sat"
if day == "Sat" or day == "Sun":
    print("Weekend")
else:
    print("Weekday")
```

Python 3.10 added `match`, which reads more like the exam's `switch`. The `|` means "or" and `_` is the default:

```python
day = "Sat"
match day:
    case "Sat" | "Sun":
        print("Weekend")
    case _:
        print("Weekday")
```
"""),
        Section("Data types, casting and operators", r"""
The exam names five data types. Python has four of them, because it has no separate character type.

| Exam name | Python type | Example |
| Integer | `int` | `42` |
| Real | `float` | `3.14` |
| Boolean | `bool` | `True` |
| Character | `str` of length one | `"A"` |
| String | `str` | `"Computing"` |

```python
print(type(7), type(7.0), type(True), type("7"), type("A"))
# <class 'int'> <class 'float'> <class 'bool'> <class 'str'> <class 'str'>
```

### Casting

**Casting** converts a value from one type to another. `input` always gives back a string, so anything you want to calculate with must be cast first.

```python
age_text = "15"
print(int(age_text) + 1)     # 16
print(str(15) + "!")         # 15!
print(float("2.5") * 2)      # 5.0
print(int(7.9))              # 7
print(round(7.9))            # 8
```

`int(7.9)` throws the decimal part away, giving 7. `round(7.9)` rounds, giving 8. They are different operations, and an exam question about a price or an average will care which one you meant.

!warn Casting a string to a bool is almost always true :: `bool("False")` is `True`, because any string with something in it counts as true. Only the empty string `""`, the number `0` and `None` give `False`.

```python
print(bool(0), bool(1), bool(""), bool("False"))     # False True False True
```

### MOD, DIV and exponent

| Exam | Meaning | Python | `17` and `5` give |
| `+` `-` `*` | add, subtract, multiply | `+` `-` `*` | `22` `12` `85` |
| `/` | real division | `/` | `3.4` |
| `DIV` | whole number division | `//` | `3` |
| `MOD` | remainder | `%` | `2` |
| `^` | to the power of | `**` | `1419857` |

!warn In Python, ^ is not "to the power of" :: It is the bitwise XOR operator. `2 ** 3` is 8 but `2 ^ 3` is 1. If a translation of an exam `^` gives you a strange small number, this is the reason.

```python
print(17 / 5, 17 // 5, 17 % 5)     # 3.4 3 2
print(2 ** 3)                      # 8
print(2 ^ 3)                       # 1, which is XOR
```

**MOD and DIV are exam favourites** because one pair of lines splits a quantity into units:

```python
total_seconds = 3725
hours = total_seconds // 3600
minutes = (total_seconds % 3600) // 60
seconds = total_seconds % 60
print(hours, "h", minutes, "m", seconds, "s")     # 1 h 2 m 5 s
```

Learn the five uses of MOD, because the question rarely says "use MOD":

| To find out | Write |
| Is `n` even? | `n % 2 == 0` |
| Is `n` a multiple of 3? | `n % 3 == 0` |
| What is the last digit of `n`? | `n % 10` |
| What is `n` without its last digit? | `n // 10` |
| Wrap round after a limit (clock, alphabet) | `(position + shift) % 26` |

### Boolean operators

`not` binds tightest, then `and`, then `or`. Brackets make the intention clear and change the result:

```python
a, b, c = True, False, False
print(a or b and c)         # True, because and goes first: a or (b and c)
print((a or b) and c)       # False
print(not a or b)           # False, because not goes first: (not a) or b
```

### Text handling

| Exam | Python |
| `name.length` | `len(name)` |
| `name.substring(2, 3)` | `name[2:5]` |
| `name.left(3)` | `name[:3]` |
| `name.right(3)` | `name[-3:]` |
| `name.upper` and `name.lower` | `name.upper()` and `name.lower()` |
| `ASC("A")` | `ord("A")` |
| `CHR(65)` | `chr(65)` |

```python
word = "Computing"
print(len(word))                     # 9
print(word[2:5])                     # mpu
print(word[:3], word[-3:])           # Com ing
print(word.upper(), word.lower())    # COMPUTING computing
print(ord("A"), chr(66))             # 65 B
```

!key substring counts, a slice stops :: The exam's `substring(2, 3)` means start at position 2 and take **three characters**. A Python slice `[2:5]` means start at 2 and stop **before** 5. Same three letters, two different ways of saying it.

Putting `ord`, `chr` and MOD together gives the classic Caesar shift, where `% 26` is what makes `Y` wrap round to `B`:

```python
def shift_letter(letter, shift):
    position = ord(letter) - ord("A")
    new_position = (position + shift) % 26
    return chr(new_position + ord("A"))

print(shift_letter("C", 3), shift_letter("Y", 3))     # F B
```
"""),
        Section("Translating whole algorithms", r"""
The exam gives you pseudocode to read, to trace, to correct or to complete, and asks you to write your own. In a written paper, an answer in Python is accepted if the logic is unambiguous. In Edexcel Paper 2 the code has to run.

### 1. A count loop with a running total

```pseudo
total = 0
for i = 1 to 5
    mark = input("Enter mark")
    total = total + int(mark)
next i
average = total / 5
print("Average: " + str(average))
```

The program below is the same algorithm. A list stands in for the keyboard so that it gives the same output every time you run it.

```python
marks = [60, 72, 85, 41, 90]
total = 0
for i in range(1, 6):
    mark = marks[i - 1]
    total = total + mark
average = total / 5
print("Average: " + str(average))     # Average: 69.6
```

### 2. Selection with a compound condition

```pseudo
if mark >= 80 AND attendance >= 90 then
    print("Distinction")
elseif mark >= 50 then
    print("Pass")
else
    print("Fail")
endif
```

```python
def result(mark, attendance):
    if mark >= 80 and attendance >= 90:
        return "Distinction"
    elif mark >= 50:
        return "Pass"
    else:
        return "Fail"

print(result(85, 95), result(85, 70), result(30, 100))     # Distinction Pass Fail
```

The second call shows why the order matters. A mark of 85 with 70 per cent attendance fails the first test, so it falls through to the second and earns a Pass.

### 3. A loop that tests first

```pseudo
secret = 7
guess = 0
tries = 0
while guess != secret
    guess = int(input("Guess"))
    tries = tries + 1
endwhile
print("Found in " + str(tries))
```

```python
feed = iter([3, 9, 7])
secret = 7
guess = 0
tries = 0
while guess != secret:
    guess = next(feed)
    tries = tries + 1
print("Found in " + str(tries))     # Found in 3
```

`guess` is set to 0 before the loop so that the first test has something to compare. A test-first loop needs its variable to exist, and to start at a value that lets the loop begin.

### 4. Random numbers

The exam's `random(1, 6)` includes both ends. So does Python's `randint`, which is unusual, because `range` does not.

```python
import random
roll = random.randint(1, 6)
print(1 <= roll <= 6)     # True, whichever number came up
```

### The translation checklist

1. **Loops.** Add one to the stop value of a count loop. Turn `until` into `if ... break`.
2. **Operators.** `DIV` is `//`, `MOD` is `%`, `^` is `**`.
3. **Text.** `substring(start, length)` is `[start:start + length]`. `ASC` is `ord` and `CHR` is `chr`.
4. **Types.** `input` gives a string. Cast it before comparing or calculating.
5. **Equality.** `=` assigns and `==` compares, in both the exam and Python.

!exam Do not use shortcuts that hide the algorithm :: If the question asks you to total a list, write the loop. `sum(marks)` is perfectly good Python, but the mark scheme is looking for an accumulator that starts at 0 and gains each value. The same goes for `max`, `min` and `sorted` on a question about finding or sorting.
"""),
    ],
    keyterms=[
        ("Pseudocode", "A way of writing an algorithm in structured, language-neutral English so it can be read without knowing a programming language."),
        ("Casting", "Converting a value from one data type to another, such as int(\"7\") or str(7)."),
        ("MOD", "The remainder after whole number division. 17 MOD 5 is 2. Written % in Python."),
        ("DIV", "Whole number division, discarding the remainder. 17 DIV 5 is 3. Written // in Python."),
        ("Count-controlled loop", "A loop that repeats a set number of times, such as for i = 1 to 5."),
        ("Condition-controlled loop", "A loop that repeats until or while a condition is met, such as while or do...until."),
        ("Concatenation", "Joining two strings end to end, using + in the exam and in Python."),
        ("Substring", "A part of a string, taken by position and length."),
        ("ASCII code", "The number that stands for a character. ord gives it and chr turns it back into a character."),
    ],
    grade="""
Full marks on translation questions come from checking the five places where the notations disagree.

+ Add one to the stop value of every count loop, and say why in a comment
+ Turn do...until into while True with a break on the exit condition
+ Know that MOD is the remainder, DIV drops it, and ^ is not power in Python
+ Cast the result of input before comparing or calculating with it
+ Write the loop for a total or a count rather than reaching for sum or len
""",
    mistakes=[
        "Writing range(1, 5) for for i = 1 to 5, so the loop stops one short.",
        "Using ^ for a power in Python, which is XOR and gives a strange small number.",
        "Comparing input directly with a number without casting, which is a TypeError.",
        "Swapping the start and the length in substring(start, length).",
        "Writing = when comparing, so the condition assigns instead of testing.",
    ],
    quiz=[
        Q("Which Python expression is the same as `17 MOD 5` in exam pseudocode?",
          ["`17 % 5`", "`17 // 5`", "`17 / 5`", "`17 ** 5`"], 0,
          "MOD is the remainder after division, and % is Python's remainder operator. 17 divided by 5 is 3 remainder 2."),
        Q("What is the value of `17 // 5` in Python?",
          ["3", "3.4", "2", "4"], 0,
          "// is whole number division, the same as DIV in the exam. It drops the remainder."),
        Q("Which line is the Python for the exam loop `for i = 1 to 5`?",
          ["`for i in range(1, 6):`", "`for i in range(1, 5):`", "`for i in range(5):`", "`for i in range(0, 5):`"], 0,
          "range stops one before its second value, so to include 5 the stop value must be 6."),
        Q("What does `2 ^ 3` evaluate to in Python?",
          ["1", "8", "6", "5"], 0,
          "In Python ^ is the bitwise XOR operator. 2 is 10 in binary, 3 is 11, and XOR gives 01, which is 1. Use ** for powers."),
        Q("Which structure replaces an exam `do ... until x > 10` loop in Python?",
          ["`while True:` with `if x > 10: break` at the bottom", "`for x in range(10):`",
           "`if x > 10:` placed before the loop", "`while x > 10:` and nothing else"], 0,
          "Python has no loop that tests at the bottom, so you loop forever and break out when the exit condition is true."),
        Q("Which function turns the character `\"A\"` into its ASCII code 65?",
          ["`ord`", "`chr`", "`int`", "`str`"], 0,
          "ord gives the code for a character and chr is the reverse, matching the exam's ASC and CHR."),
        Q("What is `bool(\"False\")` in Python?",
          ["`True`", "`False`", "An error", "`None`"], 0,
          "Any string that is not empty counts as true, whatever it says. Only the empty string is false."),
        Q("If `word = \"Computing\"`, what is `word[2:5]`?",
          ["`\"mpu\"`", "`\"omp\"`", "`\"mput\"`", "`\"put\"`"], 0,
          "The slice starts at position 2, which is m, and stops before position 5. Positions start at 0, so C=0, o=1, m=2, p=3, u=4."),
        Q("How does Python store a single character such as `\"A\"`?",
          ["As a string of length one", "As a `char`", "As an integer", "As a Boolean"], 0,
          "There is no separate character type. A character is just a string with one thing in it."),
        Q("What are the values of `7 // 2` and `7 / 2`?",
          ["3 and 3.5", "3.5 and 3", "3 and 3", "4 and 3.5"], 0,
          "// drops the remainder and gives 3. / is real division and gives 3.5."),
    ],
    exam=[
        EQ("A program contains the lines minutes = total_seconds DIV 60 and seconds = total_seconds MOD 60. State the value of minutes and the value of seconds when total_seconds is 185.", 2, [
            MP("minutes is 3", ["minutes 3", "3 minutes", "3"]),
            MP("seconds is 5", ["seconds 5", "5 seconds", "5"]),
        ], "185 DIV 60 is 3, because 60 goes into 185 three times. 185 MOD 60 is 5, because three lots of 60 make 180 and the remainder is 5. So minutes is 3 and seconds is 5.",
           command="State"),
        EQ("Write the Python equivalent of the following OCR reference language.", 3, [
            MP("Uses range(1, 11) so that 10 is included", ["range 1 11", "11"]),
            MP("Adds i * i to the total inside the loop", ["total + i * i", "total += i * i", "i * i", "i ** 2", "i*i"]),
            MP("Prints the total after the loop, not inside it", ["print total", "print(total)", "outside the loop", "after the loop"]),
        ], r"""The Python loop must run to 10 inclusive, so the stop value is 11.

```python
total = 0
for i in range(1, 11):
    total = total + i * i
print(total)
```

The print is not indented, so it happens once after the loop has finished. The program prints 385.""",
           command="Write",
           figure="""```pseudo
total = 0
for i = 1 to 10
    total = total + i * i
next i
print(total)
```"""),
        EQ("A student writes age = input(\"Age: \") followed by if age >= 18:. Explain why this raises an error and show how to correct it.", 4, [
            MP("input always returns a string", ["string", "text", "str"]),
            MP("A string cannot be compared with an integer using >=", ["compare", "comparing", "typeerror", "type error", "cannot"]),
            MP("The value must be cast to an integer", ["int(", "int", "cast", "convert", "integer"]),
            MP("Corrected code is age = int(input(\"Age: \"))", ["int input", "age int input", "int(input"]),
        ], r"""The input function always returns a string, even when the user types digits. Python cannot compare a string with the integer 18 using >=, so it raises a TypeError. The string has to be converted to an integer first, by casting it.

```python
age = int(input("Age: "))
if age >= 18:
    print("Adult")
```""",
           command="Explain"),
        EQ("A Caesar cipher shifts every letter along the alphabet and wraps round after Z. Describe how the MOD operator is used to make the shifted letter wrap round.", 3, [
            MP("Each letter is converted to a position from 0 to 25", ["position", "number", "0 to 25", "ord", "ascii"]),
            MP("The shift is added and the total is MOD 26", ["mod 26", "% 26", "remainder", "26"]),
            MP("The remainder is always between 0 and 25 so Y plus 3 wraps to B", ["wraps", "wrap", "back to a", "between 0 and 25", "start"]),
        ], "Each letter is first turned into its position in the alphabet, from 0 for A to 25 for Z. The shift is added, then the total is taken MOD 26. The remainder after dividing by 26 can only be between 0 and 25, so a total that goes past 25 comes back round to the start of the alphabet. For example Y is position 24, 24 plus 3 is 27, and 27 MOD 26 is 1, which is B.",
           command="Describe"),
        EQ("Convert the following loop into Python. The loop must behave exactly as the original does.", 3, [
            MP("Uses a loop that cannot end by itself such as while True", ["while true", "while 1", "loop forever"]),
            MP("Reads the guess inside the loop and casts it to an integer", ["int(input", "int input", "input"]),
            MP("Uses an if with break when the guess equals 7", ["break", "if guess == 7", "guess 7", "exit"]),
        ], r"""The body must run once before the test, so the loop is a while True with the exit condition checked at the bottom.

```python
while True:
    guess = int(input("Guess: "))
    if guess == 7:
        break
```""",
           command="Convert",
           figure="""```pseudo
do
    guess = int(input("Guess: "))
until guess == 7
```"""),
    ],
)
