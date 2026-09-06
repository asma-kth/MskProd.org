"""A complete Python course, from the first line of code to OOP, tkinter and pygame.

Written so that a Year 7 student can start at the beginning and an A Level
student can pick up at object oriented programming, with everything runnable.
"""
from mskbuild.models import Topic, Section, Unit, Course, Q, EQ, MP

P_FIRST = Topic(
    slug="first-steps",
    title="First Steps: Output, Comments and Errors",
    spec="1.1",
    icon="i-play",
    minutes=16,
    blurb="Your first program, how to read an error message instead of panicking at it, and the habits that will save you hours later.",
    fact="The tradition of making Hello World your first program comes from a 1972 tutorial by Brian Kernighan. Over fifty years later it is still the first thing almost every programmer ever writes.",
    sections=[
        Section("Your first program", """
```python
print("Hello, world!")
```

That is a complete program. Run it and the text appears.

### What each part does

- `print` is a **function**, a built in piece of code that does a job
- The **brackets** hold what you are giving it
- The **quotation marks** mark the start and end of the text

### Printing several things

```python
print("Hello", "world", "again")
print("The answer is", 42)
print("Line one")
print("Line two")
```

A comma puts a space between items and lets you mix text and numbers freely.

### Comments

A **comment** is a note for humans. Python ignores everything after a `#`.

```python
# Ask the player for their name
name = input("Name: ")     # input always gives back text
```

Comment **why**, not what. `count = count + 1  # add one` is useless. `# skip the header row` is worth having.
"""),
        Section("Reading error messages", """
Beginners see a red error and panic. Experienced programmers read it, because it usually says exactly what is wrong and on which line.

```text
  File "main.py", line 4
    print("Hello"
                 ^
SyntaxError: '(' was never closed
```

That tells you the file, the line, the position and the problem.

### The errors you will meet first

| Error | Usual cause |
| `SyntaxError` | A missing bracket, quote or colon |
| `IndentationError` | Lines under an if or a loop are not lined up |
| `NameError` | A variable used before it exists, or a typo in its name |
| `TypeError` | Mixing incompatible types, such as text plus a number |
| `ValueError` | The right type but an impossible value, such as `int("hello")` |
| `ZeroDivisionError` | Dividing by zero |

!key The rule that saves the most time :: Read the last line of the error first. It names the problem. Then read the line number. Fix that line before looking anywhere else.

### Three habits worth building now

1. **Run your code often.** After every few lines, not after fifty. Then you know exactly what broke it.
2. **Name things properly.** `total_score` is better than `ts` every single time.
3. **Print things to check.** If you are unsure what a variable holds, print it. This is the single most useful debugging technique there is, and professionals still use it daily.
"""),
    ],
    keyterms=[
        ("Function", "A named piece of code that performs a job, such as print."),
        ("Argument", "A value you give to a function inside its brackets."),
        ("String", "Text data, written inside quotation marks."),
        ("Comment", "A note in the code for humans, ignored by Python, starting with a hash."),
        ("Syntax error", "A mistake in how the code is written, which stops it running at all."),
        ("Runtime error", "An error that occurs while the program is running, such as dividing by zero."),
    ],
    grade="""
Getting good at Python early is mostly about habits rather than knowledge.

+ Run your code every few lines so you always know what broke it
+ Read the last line of an error message first, then the line number
+ Use full descriptive variable names from the very beginning
+ Print variables when you are not sure what they contain
+ Comment why you did something, never what the line obviously does
""",
    mistakes=[
        "Forgetting the quotation marks around text.",
        "Forgetting a closing bracket, which produces a syntax error on the following line.",
        "Ignoring the error message and just changing things at random.",
        "Writing fifty lines before running any of it.",
    ],
    quiz=[
        Q("What does `print(\"Hello\")` do?", ["Displays Hello on the screen", "Sends Hello to a printer",
                                              "Stores Hello in a variable", "Nothing"], 0,
          "print sends text to the output, which in most environments means the screen."),
        Q("What symbol starts a comment in Python?", ["#", "//", "--", "/*"], 0,
          "Everything after a hash on that line is ignored by Python."),
        Q("Which error means you used a variable that does not exist?",
          ["NameError", "TypeError", "ValueError", "SyntaxError"], 0,
          "It is usually a typo in the name, or using the variable before you created it."),
        Q("What does `print(\"Score\", 10)` display?", ["Score 10", "Score10", "Score, 10", "An error"], 0,
          "A comma separates items with a space and lets you mix text and numbers."),
        Q("What kind of error is a missing colon at the end of an if line?",
          ["A syntax error", "A logic error", "A runtime error", "A name error"], 0,
          "It breaks the rules of the language, so the program will not run at all."),
        Q("Which is the best comment?",
          ["# skip the header row", "# add one to i", "# this is a loop", "# code"], 0,
          "A good comment explains why. What the line does should already be obvious from the code."),
        Q("What causes a ValueError in `int(\"hello\")`?",
          ["The text cannot be converted into a number", "hello is too long",
           "int is spelled wrongly", "The quotes are wrong"], 0,
          "The type is right, a string, but the value cannot possibly represent a number."),
        Q("Why should you run your code frequently?",
          ["So you know exactly which few lines caused a new error",
           "It makes the program faster", "Python requires it", "It saves the file"], 0,
          "Finding a bug in three new lines is easy. Finding it in fifty is not."),
        Q("What does the last line of an error message tell you?",
          ["The type of error and a description of the problem",
           "The name of the file", "How long the program ran", "The next line to write"], 0,
          "Read that line first, then look at the line number given above it."),
        Q("Which variable name is best?", ["total_score", "ts", "x", "a1"], 0,
          "Descriptive names make code readable, and readable code is code you can actually debug."),
    ],
    exam=[
        EQ("State the purpose of a comment in a program.", 2, [
            MP("A note for humans reading the code", ["human", "programmer", "note", "explain", "reader"]),
            MP("Ignored by the computer when the program runs", ["ignored", "not run", "not executed", "no effect"]),
        ], "A comment is a note written in the code to explain something to a person reading it, such as why a particular approach was taken. It is completely ignored by Python when the program runs, so it has no effect on what the program does.",
           command="State"),
        EQ("Explain the difference between a syntax error and a runtime error, giving an example of each.", 4, [
            MP("A syntax error breaks the rules of the language", ["rules", "syntax", "invalid", "grammar"]),
            MP("So the program will not run at all", ["will not run", "cannot run", "does not start"]),
            MP("A runtime error occurs while the program is running", ["while running", "during", "when it runs", "crashes"]),
            MP("Gives valid examples such as a missing bracket and dividing by zero", ["missing bracket", "colon", "divide by zero", "zerodivision", "quote"]),
        ], "A syntax error is a mistake in the way the code is written, such as a missing closing bracket or a missing colon at the end of an if statement. Because the code does not follow the rules of the language, Python cannot interpret it at all and the program will not run, so the error appears before anything happens. A runtime error occurs in code that is perfectly valid but which fails while it is executing, for example dividing by zero or trying to convert the text hello into a number. The program starts normally and then crashes at the point the problem occurs.",
           command="Explain"),
        EQ("A student writes `print(\"Hello)` and gets an error. Identify the error and correct it.", 2, [
            MP("The closing quotation mark is missing", ["quotation", "quote", "missing", "not closed", "speech mark"]),
            MP("Correct code is print(\"Hello\")", ["print(\"hello\")", "add the quote", "close the string"]),
        ], "The string has an opening quotation mark but no closing one, so Python reaches the end of the line still expecting the text to continue and reports a syntax error. The corrected line is print(\"Hello\") with a closing quotation mark before the closing bracket.",
           command="Identify"),
        EQ("Explain why printing the value of a variable is a useful way to find errors in a program.", 3, [
            MP("It shows what the variable actually contains at that point", ["shows", "actual value", "contains", "what it holds"]),
            MP("This may be different from what the programmer assumed", ["assumed", "expected", "thought", "different"]),
            MP("It narrows down which part of the program is wrong", ["narrows", "which line", "locate", "where", "isolate"]),
        ], "Printing a variable shows exactly what it holds at that moment in the program, which is frequently not what the programmer assumed it held. Many bugs come from a variable containing text when a number was expected, or holding a value from an earlier iteration, and these are invisible just by reading the code. By printing values at several points, the programmer can see where the value first becomes wrong, which narrows the problem down to a small section rather than the whole program.",
           command="Explain"),
        EQ("Write a program that displays your name and your favourite subject on two separate lines, with a comment explaining what it does.", 3, [
            MP("Includes a comment", ["#", "comment"]),
            MP("Uses print correctly with quotation marks", ["print(", "\"", "quotation"]),
            MP("Produces output on two separate lines", ["two print", "separate lines", "two statements"]),
        ], "# Display some information about me\nprint(\"My name is Aisha\")\nprint(\"My favourite subject is Computing\")\n\nThe comment on the first line explains the purpose of the program and is ignored when it runs. Each print statement outputs its text and then moves to a new line, so using two separate print statements produces two lines of output.",
           command="Write"),
    ],
)

P_VARS = Topic(
    slug="variables-and-data-types",
    title="Variables and Data Types",
    spec="1.2",
    icon="i-list",
    minutes=20,
    blurb="Storing values, the five types you need, and why the equals sign does not mean what it meant in maths.",
    fact="In Python a variable is really a label attached to a value, not a box containing it. That is why two variables can point at the same list, and changing it through one changes what you see through the other.",
    sections=[
        Section("Variables", """
```python
name = "Aisha"
age = 14
height = 1.62
is_student = True
```

The **equals sign is not equality**. It means: work out the right hand side, then attach the name on the left to that value.

That is why this makes sense in programming but not in maths:

```python
score = 10
score = score + 5     # work out 10 + 5, then make score refer to 15
print(score)          # 15
```

### Naming rules

- Must start with a letter or underscore
- May contain letters, digits and underscores, but no spaces
- Case sensitive, so `Score` and `score` are different
- Cannot be a Python keyword such as `if`, `for` or `class`

### Naming well

```python
n = 25                    # bad
num_students = 25         # good
d = 3.5                   # bad
distance_km = 3.5         # good
```

Python convention is `lower_case_with_underscores` for variables and `UPPER_CASE` for constants.

### Shortcuts

```python
score += 10     # same as score = score + 10
lives -= 1      # same as lives = lives - 1
total *= 2      # same as total = total * 2
```
"""),
        Section("Data types", """
| Type | Name | Example |
| Whole number | `int` | `42`, `-7`, `0` |
| Decimal number | `float` | `3.14`, `-0.5` |
| Text | `str` | `"hello"`, `"42"` |
| True or False | `bool` | `True`, `False` |
| Nothing | `NoneType` | `None` |

```python
print(type(42))          # <class 'int'>
print(type("42"))        # <class 'str'>
print(type(3.14))        # <class 'float'>
print(type(True))        # <class 'bool'>
```

!warn `42` and `"42"` are completely different :: One is a number you can do arithmetic on. The other is text. `42 + 1` gives 43. `"42" + "1"` gives `"421"`.

### Converting between types

```python
int("42")        # 42
int(3.9)         # 3, it cuts off rather than rounding
float("3.5")     # 3.5
str(42)          # "42"
bool(0)          # False
bool(1)          # True
round(3.7)       # 4, this rounds properly
```

### Choosing the right type

- A person's age: `int`, because ages are whole numbers
- A price: `float`, because it needs pence
- A phone number: `str`, because it may start with 0 and you never do arithmetic on it
- Whether the game is over: `bool`, because there are only two states

!key The phone number rule :: If you would never add or multiply it, store it as a string. Postcodes, ID numbers, phone numbers and card numbers are all strings.
"""),
    ],
    keyterms=[
        ("Variable", "A name attached to a value that can change while the program runs."),
        ("Assignment", "Giving a variable a value using the equals sign."),
        ("int", "The whole number data type."),
        ("float", "The decimal number data type."),
        ("str", "The text data type, called a string."),
        ("bool", "The data type holding only True or False."),
        ("Casting", "Converting a value from one data type to another, such as int() or str()."),
        ("Constant", "A value that should not change, written in upper case by convention."),
    ],
    grade="""
+ Choose the correct data type for any piece of data and justify it
+ Explain why `42 + 1` and `"42" + "1"` give different results
+ Use `+=` and `-=` correctly to update a running total
+ Name every variable so that someone reading your code needs no explanation
""",
    mistakes=[
        "Storing a phone number as an int, which removes the leading zero.",
        "Assuming int(3.9) rounds to 4. It truncates to 3. Use round() to round.",
        "Using a variable before assigning it a value, which gives a NameError.",
        "Naming variables x, y and z in a program with twenty of them.",
    ],
    quiz=[
        Q("What does `score = score + 5` do if score was 10?",
          ["Makes score refer to 15", "Checks whether score equals 15",
           "Creates a new variable called score + 5", "Causes an error"], 0,
          "The right hand side is worked out first, then the name is attached to the result."),
        Q("What type is `3.14`?", ["float", "int", "str", "bool"], 0,
          "A float is a number with a decimal part. An int is a whole number."),
        Q("What does `\"5\" + \"3\"` give?", ["\"53\"", "8", "\"8\"", "An error"], 0,
          "Both are strings, so the plus sign joins them rather than adding."),
        Q("What does `int(7.9)` give?", ["7", "8", "7.9", "An error"], 0,
          "int() cuts off the decimal part rather than rounding. Use round() to round properly."),
        Q("Which type should store whether a user is logged in?",
          ["bool", "int", "str", "float"], 0,
          "There are exactly two possible states, which is what a bool represents."),
        Q("Why store a phone number as a string?",
          ["A leading zero would be lost if it were an int",
           "Strings use less memory", "Phone numbers are too long for an int", "It runs faster"], 0,
          "07700 900123 as an int becomes 7700900123, and you never do arithmetic on a phone number anyway."),
        Q("What is `score += 3` short for?",
          ["score = score + 3", "score == score + 3", "score = 3", "print(score + 3)"], 0,
          "It is a shortcut for updating a variable using its own current value."),
        Q("Which variable name is invalid in Python?",
          ["2nd_score", "second_score", "_score", "scoreTwo"], 0,
          "A variable name cannot start with a digit."),
        Q("What does `type(\"42\")` return?", ["str", "int", "float", "bool"], 0,
          "The quotation marks make it text, even though the characters look like a number."),
        Q("Which is the Python convention for a constant?",
          ["MAX_LIVES", "maxLives", "max_lives", "Maxlives"], 0,
          "Upper case with underscores signals that the value is not meant to change."),
    ],
    exam=[
        EQ("State the most suitable data type for each of: a student's age, a product price, whether an order is paid.", 3, [
            MP("Age is an integer", ["age", "int", "integer", "whole"]),
            MP("Price is a float", ["price", "float", "decimal", "real"]),
            MP("Paid is a boolean", ["paid", "bool", "boolean", "true or false"]),
        ], "A student's age should be an integer, because ages are whole numbers and arithmetic is performed on them. A product price should be a float, because prices include pence and therefore need a decimal part. Whether an order is paid should be a boolean, because there are only two possible states and a boolean makes that meaning completely clear while using the least memory.",
           command="State"),
        EQ("Explain why `\"10\" + \"5\"` gives a different result from `10 + 5`.", 3, [
            MP("The first pair are strings", ["strings", "text", "quotation marks"]),
            MP("The plus operator joins strings together rather than adding", ["joins", "concatenate", "sticks", "combines"]),
            MP("The second pair are integers so the plus operator performs addition", ["integers", "numbers", "addition", "adds"]),
        ], "In the first case both values are strings, because they are written inside quotation marks. When the plus operator is applied to two strings it concatenates them, joining them end to end, so the result is the string \"105\". In the second case both values are integers, so the plus operator performs ordinary numerical addition and the result is 15. This is why input from the user must be converted with int() before any arithmetic is done on it.",
           command="Explain"),
        EQ("Explain why a phone number should be stored as a string rather than an integer.", 3, [
            MP("Phone numbers often begin with a zero", ["leading zero", "starts with 0", "zero"]),
            MP("An integer would discard the leading zero, changing the number", ["discard", "lost", "removed", "changed", "different"]),
            MP("No arithmetic is ever performed on a phone number", ["no arithmetic", "never add", "not calculated", "no maths"]),
        ], "Phone numbers in the UK begin with a zero, and an integer stores only the numeric value with no record of leading zeros, so 07700900123 would be stored and displayed as 7700900123, which is not the correct number and would fail to match records held elsewhere. In addition, no arithmetic is ever carried out on a phone number, so there is no benefit at all to storing it as a number. A string preserves every character exactly as entered, which is what is needed.",
           command="Explain"),
        EQ("Write Python code that creates a variable for a player's score starting at zero, adds 25 to it, and prints the result.", 3, [
            MP("Initialises the variable to 0", ["score = 0", "= 0", "zero"]),
            MP("Adds 25 to it", ["+= 25", "score + 25", "add"]),
            MP("Prints the result", ["print"]),
        ], "score = 0\nscore += 25\nprint(\"Your score is\", score)\n\nThe variable is created and set to 0 first, which matters because a variable cannot be used before it exists. The += shortcut adds 25 to whatever the score currently is, and the print statement then displays the updated value.",
           command="Write"),
        EQ("A program uses `int(4.8)` and the programmer expects the result 5. Explain what actually happens and how to get the intended result.", 3, [
            MP("int() removes the decimal part rather than rounding", ["truncates", "cuts off", "removes", "does not round", "discards"]),
            MP("The result is therefore 4", ["4"]),
            MP("Use round() to round to the nearest whole number", ["round", "round(4.8)"]),
        ], "The int() function converts a value to a whole number by discarding everything after the decimal point rather than rounding, so int(4.8) gives 4 rather than 5. To round to the nearest whole number the programmer should use round(4.8), which correctly gives 5. This distinction matters in any calculation involving averages or prices, where truncating instead of rounding can produce noticeably wrong results.",
           command="Explain"),
    ],
)

P_INPUT = Topic(
    slug="input-and-selection",
    title="Input, Operators and Selection",
    spec="1.3",
    icon="i-flow",
    minutes=24,
    blurb="Getting data from the user, every operator you need, and making decisions with if, elif and else.",
    fact="The single most common beginner bug in the world is forgetting that input returns text. If you remember only one thing from this page, make it that.",
    sections=[
        Section("Input", """
```python
name = input("What is your name? ")
print("Hello,", name)
```

!warn input always returns a string :: Even if the user types 42, you get the text `"42"`. Convert it before doing arithmetic.

```python
age = int(input("How old are you? "))
price = float(input("Enter the price: "))
```

If the user types something that cannot be converted, the program crashes with a `ValueError`. Handling that properly comes later, but be aware of it now.

### A safe pattern

```python
entry = input("Enter your age: ")
while not entry.isdigit():
    print("Please enter a whole number.")
    entry = input("Enter your age: ")
age = int(entry)
```
"""),
        Section("Operators", """
### Arithmetic

| Operator | Meaning | Example | Result |
| `+` | Add | `7 + 3` | 10 |
| `-` | Subtract | `7 - 3` | 4 |
| `*` | Multiply | `7 * 3` | 21 |
| `/` | Divide, always gives a float | `7 / 2` | 3.5 |
| `//` | Integer division | `7 // 2` | 3 |
| `%` | Modulus, the remainder | `7 % 2` | 1 |
| `**` | Power | `2 ** 3` | 8 |

**Modulus is more useful than it looks:**

```python
if number % 2 == 0:
    print("Even")

minutes = seconds // 60
remaining = seconds % 60

if turn % 4 == 0:
    print("Every fourth turn")
```

### Comparison

| Operator | Meaning |
| `==` | Equal to |
| `!=` | Not equal to |
| `<` `>` | Less than, greater than |
| `<=` `>=` | Less than or equal to, greater than or equal to |

!warn One equals sign assigns, two compare :: `x = 5` puts 5 into x. `x == 5` asks whether x is 5.

### Logical

```python
if age >= 13 and age <= 19:
    print("Teenager")

if day == "Saturday" or day == "Sunday":
    print("Weekend")

if not logged_in:
    print("Please sign in")
```

- `and` needs **both** sides true
- `or` needs **at least one** true
- `not` reverses it
"""),
        Section("Selection", """
```python
mark = int(input("Enter the mark: "))

if mark >= 70:
    print("Distinction")
elif mark >= 50:
    print("Merit")
elif mark >= 40:
    print("Pass")
else:
    print("Fail")
```

### The three rules

1. The **colon** at the end of each condition line
2. The **indentation** of the block underneath, four spaces
3. Conditions are checked **top to bottom**, and the first true one runs while the rest are skipped

!key Order the conditions from most restrictive to least :: If `mark >= 40` came first, a mark of 95 would print "Pass" and never reach the distinction branch, because Python stops at the first true condition.

### Nested selection

```python
if logged_in:
    if is_admin:
        print("Admin dashboard")
    else:
        print("User dashboard")
else:
    print("Please log in")
```

### Combining rather than nesting

Often clearer:

```python
if logged_in and is_admin:
    print("Admin dashboard")
elif logged_in:
    print("User dashboard")
else:
    print("Please log in")
```

### match, an alternative for many fixed options

```python
command = input("Enter a command: ").lower()

match command:
    case "go":
        print("You move forward.")
    case "look":
        print("You see a door.")
    case "quit":
        print("Goodbye.")
    case _:
        print("I do not understand.")
```

The underscore case runs when nothing else matched.
"""),
    ],
    keyterms=[
        ("input()", "A function that displays a prompt and returns whatever the user types, always as a string."),
        ("Modulus", "The % operator, which returns the remainder after division."),
        ("Integer division", "The // operator, which returns only the whole number part of a division."),
        ("Condition", "An expression that evaluates to True or False."),
        ("Selection", "Choosing between different paths through a program based on a condition."),
        ("elif", "Short for else if. Checks another condition only if the previous ones were false."),
        ("Nested selection", "An if statement placed inside another if statement."),
    ],
    grade="""
+ Always convert input before doing arithmetic on it
+ Order elif conditions from most restrictive to least
+ Use modulus to test for even numbers, extract time units and cycle values
+ Use `and` and `or` to combine conditions rather than deeply nesting ifs
+ Check the boundary: if a condition uses a number, test exactly that number
""",
    mistakes=[
        "Forgetting int() around input, then comparing a string with a number.",
        "Using a single equals sign in a condition.",
        "Ordering elif branches from least restrictive to most.",
        "Forgetting the colon at the end of the if line.",
        "Using `>` where `>=` was needed, which fails at exactly the boundary value.",
    ],
    quiz=[
        Q("What does `input()` always return?", ["A string", "An integer", "A float", "A boolean"], 0,
          "Even when the user types digits, you get text and must convert it yourself."),
        Q("What does `17 % 5` give?", ["2", "3", "3.4", "85"], 0,
          "Modulus gives the remainder. 5 goes into 17 three times with 2 left over."),
        Q("What does `17 // 5` give?", ["3", "2", "3.4", "12"], 0,
          "Integer division gives only the whole number part of the division."),
        Q("Which condition correctly tests whether n is even?",
          ["n % 2 == 0", "n / 2 == 0", "n % 2 == 1", "n == 2"], 0,
          "An even number leaves no remainder when divided by two."),
        Q("A program has `if mark >= 40` before `elif mark >= 70`. What does a mark of 90 print?",
          ["The message for 40, because the first true condition runs",
           "The message for 70", "Both messages", "An error"], 0,
          "Python runs the first true branch and skips the rest, so the most restrictive must come first."),
        Q("What is wrong with `if score = 10:`?",
          ["A comparison needs two equals signs", "There should be no colon",
           "score must be in quotes", "Nothing"], 0,
          "One equals sign assigns a value, which is not valid inside a condition."),
        Q("When is `age >= 13 and age <= 19` true?",
          ["When age is between 13 and 19 inclusive", "When age is 13 or 19 only",
           "When age is above 13 or below 19", "Always"], 0,
          "`and` requires both sides to be true at once, so the value must be inside the range."),
        Q("What does `not True` evaluate to?", ["False", "True", "0", "An error"], 0,
          "`not` reverses a boolean value."),
        Q("How would you get the seconds part of a total number of seconds?",
          ["total % 60", "total // 60", "total / 60", "total * 60"], 0,
          "Modulus 60 gives the remainder after taking out whole minutes."),
        Q("In a match statement, what does `case _:` do?",
          ["Runs when nothing else matched", "Runs first", "Runs always", "Ends the program"], 0,
          "The underscore is the default case, equivalent to else."),
    ],
    exam=[
        EQ("Explain why `age = input(\"Age: \")` followed by `if age > 18:` causes an error.", 3, [
            MP("input returns a string", ["string", "text", "input returns"]),
            MP("A string cannot be compared with a number", ["cannot compare", "different types", "type error", "not a number"]),
            MP("Convert with int() first", ["int(", "cast", "convert"]),
        ], "The input function always returns a string, so age holds the text \"20\" rather than the number 20 even if the user types digits. Python cannot compare a string with an integer using a greater than operator, because there is no meaningful way to order text against a number, so it raises a TypeError. The fix is to convert the input as it is read, writing age = int(input(\"Age: \")), after which the comparison works as intended.",
           command="Explain"),
        EQ("Write a program that asks for a number and states whether it is even or odd.", 4, [
            MP("Asks for input and converts it to an integer", ["int(input", "input", "convert"]),
            MP("Uses the modulus operator to test divisibility by 2", ["% 2", "modulus", "remainder"]),
            MP("Prints Even when the remainder is 0", ["even", "== 0", "print"]),
            MP("Uses else to print Odd otherwise", ["else", "odd"]),
        ], "number = int(input(\"Enter a number: \"))\n\nif number % 2 == 0:\n    print(\"Even\")\nelse:\n    print(\"Odd\")\n\nThe input is converted to an integer so arithmetic can be performed. The modulus operator gives the remainder after dividing by 2, and a remainder of exactly 0 means the number divides evenly and is therefore even. Any other remainder means it is odd, which the else branch handles.",
           command="Write"),
        EQ("Explain the difference between the / operator and the // operator in Python.", 2, [
            MP("/ performs normal division and always gives a float", ["float", "decimal", "normal division", "3.5"]),
            MP("// performs integer division, giving only the whole number part", ["integer division", "whole number", "truncates", "3"]),
        ], "The single slash performs ordinary division and always produces a float, so 7 / 2 gives 3.5 and even 6 / 2 gives 3.0 rather than 3. The double slash performs integer division, discarding anything after the decimal point and returning only the whole number part, so 7 // 2 gives 3. Integer division is useful when a fractional result makes no sense, for example working out how many whole minutes are in a number of seconds.",
           command="Explain"),
        EQ("Write a program that asks for a mark out of 100 and prints Distinction for 70 or above, Merit for 50 to 69, Pass for 40 to 49 and Fail below 40.", 5, [
            MP("Reads and converts the input", ["int(input", "input"]),
            MP("Tests for 70 or above first", [">= 70", "70"]),
            MP("Uses elif for the 50 boundary", ["elif", ">= 50", "50"]),
            MP("Uses elif for the 40 boundary", ["elif", ">= 40", "40"]),
            MP("Uses else for everything below 40", ["else", "fail"]),
        ], "mark = int(input(\"Enter the mark: \"))\n\nif mark >= 70:\n    print(\"Distinction\")\nelif mark >= 50:\n    print(\"Merit\")\nelif mark >= 40:\n    print(\"Pass\")\nelse:\n    print(\"Fail\")\n\nThe conditions are ordered from most restrictive to least, which is essential. Python checks each condition in turn and runs the first one that is true, skipping the rest, so a mark of 85 is correctly caught by the first branch. If the 40 test came first, every mark of 40 or above would print Pass and the higher grades would never be reached.",
           command="Write"),
        EQ("Explain what the modulus operator does and give two situations where it is useful.", 4, [
            MP("Modulus returns the remainder after division", ["remainder", "left over", "modulus"]),
            MP("Gives a correct example such as 17 % 5 being 2", ["17 % 5", "example", "2", "remainder is"]),
            MP("First use such as testing whether a number is even", ["even", "odd", "divisible"]),
            MP("Second use such as extracting time units or cycling a value", ["seconds", "minutes", "time", "cycle", "wrap", "every nth"]),
        ], "The modulus operator performs a division and returns the remainder rather than the quotient, so 17 % 5 gives 2 because 5 goes into 17 three times with 2 left over. One common use is testing divisibility: if a number modulus 2 equals 0 then it divides exactly by two and is therefore even, and the same technique checks whether something should happen every third or every tenth time round a loop. A second use is extracting units from a total, for example converting a total number of seconds into minutes and seconds, where total // 60 gives the whole minutes and total % 60 gives the seconds remaining. Modulus is also used to wrap a value around a fixed range, such as moving a player back to the start of a board after the last square.",
           command="Explain"),
    ],
)

P_LOOPS = Topic(
    slug="loops",
    title="Loops: for and while",
    spec="2.1",
    icon="i-repeat",
    minutes=24,
    blurb="Repetition done properly, including nested loops, break and continue, and how to avoid the infinite loop that eats your afternoon.",
    fact="A nested loop with 1000 iterations on each level runs its inner body one million times. This is why an algorithm that seems fine on ten items can freeze completely on ten thousand.",
    sections=[
        Section("for loops", """
A **for loop** repeats once for each item in a collection.

```python
for i in range(5):
    print(i)          # 0 1 2 3 4
```

### range

```python
range(5)          # 0, 1, 2, 3, 4
range(2, 6)       # 2, 3, 4, 5
range(0, 10, 2)   # 0, 2, 4, 6, 8
range(10, 0, -1)  # 10, 9, 8 ... 1
```

!warn range never includes the end value :: `range(1, 6)` gives 1 to 5. This is the source of most off by one errors.

### Looping over other things

```python
for name in ["Aisha", "Ben", "Chloe"]:
    print("Hello,", name)

for letter in "Python":
    print(letter)

for index, name in enumerate(["a", "b", "c"]):
    print(index, name)      # 0 a, 1 b, 2 c
```

### Nested loops

```python
for row in range(3):
    for col in range(4):
        print("*", end=" ")
    print()
```

The inner loop completes fully for every single iteration of the outer loop, so this prints twelve stars in three rows of four.
"""),
        Section("while loops", """
A **while loop** repeats for as long as a condition is true. Use it when you do not know how many repetitions are needed.

```python
total = 0
number = int(input("Enter a number, 0 to stop: "))

while number != 0:
    total += number
    number = int(input("Enter a number, 0 to stop: "))

print("Total:", total)
```

### Infinite loops

```python
count = 0
while count < 10:
    print(count)      # count never changes, so this never ends
```

The fix is `count += 1` inside the loop. Always check that something inside the loop changes the value being tested.

Press Ctrl and C to stop a runaway program.

### break and continue

```python
while True:
    command = input("Command: ")
    if command == "quit":
        break             # leave the loop immediately
    if command == "":
        continue          # skip the rest of this iteration
    print("You typed", command)
```

`while True` with a `break` is a common and readable pattern for menus and validation.

!key Choosing a loop :: Known number of repetitions, or looping over a collection, means for. Unknown number, depending on something that happens while running, means while.
"""),
        Section("Loops in practice", """
### Running totals and counters

```python
numbers = [4, 8, 15, 16, 23, 42]

total = 0
count_over_10 = 0

for n in numbers:
    total += n
    if n > 10:
        count_over_10 += 1

print("Total:", total)
print("Average:", total / len(numbers))
print("Over ten:", count_over_10)
```

### Finding a maximum

```python
highest = numbers[0]        # start from the first item, never from 0
for n in numbers:
    if n > highest:
        highest = n
print("Highest:", highest)
```

!warn Never initialise a maximum to 0 :: If every value is negative, nothing is ever greater than 0 and the answer will be wrong. Start from the first element.

### Validation

```python
while True:
    entry = input("Enter a mark between 0 and 100: ")
    if entry.isdigit() and 0 <= int(entry) <= 100:
        mark = int(entry)
        break
    print("That is not a valid mark.")
```

### Building a times table

```python
number = int(input("Which table? "))
for i in range(1, 13):
    print(number, "x", i, "=", number * i)
```

### A simple menu

```python
while True:
    print("\\n1. Add   2. View   3. Quit")
    choice = input("Choose: ")

    if choice == "1":
        print("Adding...")
    elif choice == "2":
        print("Viewing...")
    elif choice == "3":
        print("Goodbye")
        break
    else:
        print("Please choose 1, 2 or 3.")
```
"""),
    ],
    keyterms=[
        ("for loop", "A loop that repeats once for each item in a collection or range."),
        ("while loop", "A loop that repeats for as long as its condition remains true."),
        ("range()", "A function producing a sequence of numbers for a for loop to work through."),
        ("Nested loop", "A loop placed inside another loop."),
        ("Infinite loop", "A loop whose condition never becomes false, so it never ends."),
        ("break", "A statement that leaves a loop immediately."),
        ("continue", "A statement that skips the rest of the current iteration and starts the next."),
        ("Iteration", "One single pass through the body of a loop."),
    ],
    grade="""
+ Choose for or while correctly and be able to justify the choice
+ Write a validation loop that keeps asking until the input is acceptable
+ Trace a nested loop and state exactly how many times the inner body runs
+ Initialise a maximum from the first element of the data, never from zero
+ Check every while loop for something that changes the condition
""",
    mistakes=[
        "Assuming range(5) includes 5.",
        "Writing a while loop where nothing inside changes the condition.",
        "Initialising a maximum to 0 when the data could be negative.",
        "Using a for loop when the number of repetitions is not known in advance.",
        "Putting code that should run once inside the loop, so it runs every time.",
    ],
    quiz=[
        Q("How many times does `for i in range(6)` repeat?", ["6", "5", "7", "0"], 0,
          "range(6) produces 0 to 5, which is six values."),
        Q("What does `range(2, 8)` produce?", ["2, 3, 4, 5, 6, 7", "2 to 8 including 8",
                                               "2, 4, 6, 8", "8, 7, 6, 5, 4, 3, 2"], 0,
          "The start is included, the end is not."),
        Q("Which loop should be used when the number of repetitions is unknown?",
          ["A while loop", "A for loop", "A nested for loop", "No loop"], 0,
          "A while loop repeats until its condition changes, which is exactly the case for validation or menus."),
        Q("What causes an infinite loop?",
          ["Nothing inside the loop changes the value the condition tests",
           "The loop uses range()", "The loop contains an if", "The counter starts at 0"], 0,
          "If the condition can never become false, the loop cannot end."),
        Q("What does `break` do?",
          ["Leaves the loop immediately", "Skips to the next iteration",
           "Ends the program", "Restarts the loop"], 0,
          "break exits the loop entirely. continue skips only the current iteration."),
        Q("In a nested loop where the outer runs 5 times and the inner runs 3, how many times does the inner body run?",
          ["15", "8", "5", "3"], 0,
          "The inner loop completes fully on each outer iteration, so 5 multiplied by 3."),
        Q("Why should a maximum be initialised to the first element rather than 0?",
          ["If all values are negative, nothing is greater than 0 and the answer is wrong",
           "0 is not a valid number", "It runs faster", "The list might be empty"], 0,
          "Starting from a value that is actually in the list guarantees a correct answer whatever the data."),
        Q("What does `continue` do?",
          ["Skips the rest of the current iteration and starts the next",
           "Leaves the loop", "Repeats the current iteration", "Ends the program"], 0,
          "It is useful for skipping unwanted items without adding another level of indentation."),
        Q("What does `for letter in \"cat\"` loop over?",
          ["Each character of the string in turn", "The whole word once",
           "The length of the string", "Nothing"], 0,
          "A string is a sequence of characters, so a for loop walks through it one character at a time."),
        Q("What does `enumerate()` give you?",
          ["Both the index and the item on each iteration", "Only the index",
           "Only the item", "The length of the list"], 0,
          "It is the clean way to loop through a list when you also need to know each item's position."),
    ],
    exam=[
        EQ("State the difference between a for loop and a while loop and give one situation for each.", 4, [
            MP("A for loop repeats a known number of times or over a collection", ["known", "fixed", "collection", "each item", "set number"]),
            MP("Situation such as processing every item in a list", ["list", "each item", "10 times", "every"]),
            MP("A while loop repeats while a condition is true", ["condition", "true", "until", "unknown"]),
            MP("Situation such as validating input until it is correct", ["validation", "until correct", "password", "menu", "quit"]),
        ], "A for loop repeats a known number of times, or once for each item in a collection, so the number of iterations is decided before the loop begins. It would be used to work through every mark in a list of 30 students, because the number of repetitions is known from the length of the list. A while loop repeats for as long as its condition remains true, so the number of iterations is not known in advance and depends on what happens while the program is running. It would be used to keep asking a user to enter a valid password until they get it right, since there is no way to know how many attempts they will need.",
           command="State"),
        EQ("Write a program that keeps asking the user for numbers until they enter -1, then prints how many numbers were entered and their total.", 5, [
            MP("Initialises a total and a counter", ["total = 0", "count = 0", "initialise"]),
            MP("Uses a while loop", ["while", "loop"]),
            MP("Reads and converts input inside the loop", ["int(input", "input"]),
            MP("Stops when -1 is entered without counting it", ["-1", "!= -1", "break", "stop"]),
            MP("Prints the count and total after the loop", ["print", "count", "total"]),
        ], "total = 0\ncount = 0\nnumber = int(input(\"Enter a number, -1 to finish: \"))\n\nwhile number != -1:\n    total += number\n    count += 1\n    number = int(input(\"Enter a number, -1 to finish: \"))\n\nprint(\"You entered\", count, \"numbers\")\nprint(\"Their total is\", total)\n\nThe first number is read before the loop so the condition has something to test. The loop continues while the number is not -1, adding to the total and increasing the counter each time before reading the next value. Because the read happens at the end of the loop body, the -1 that ends the loop is never counted or added.",
           command="Write"),
        EQ("Explain what causes an infinite loop and how to prevent one.", 3, [
            MP("The condition never becomes false", ["never false", "always true", "never ends"]),
            MP("Because nothing inside the loop changes the value being tested", ["nothing changes", "not updated", "never changes", "same value"]),
            MP("Prevent it by ensuring the loop body updates the variable in the condition", ["update", "increment", "change", "count += 1", "modify"]),
        ], "An infinite loop happens when the condition a while loop tests never becomes false, so the loop has no way to end. This is almost always because nothing inside the loop body changes the value that the condition depends on, for example writing while count is less than 10 but never increasing count. It can also happen when the change moves the value in the wrong direction. To prevent it, always check that the loop body contains a statement that alters the variable in the condition, and that it alters it in a direction that will eventually make the condition false.",
           command="Explain"),
        EQ("A program has a loop inside another loop. The outer loop runs 4 times and the inner loop runs 6 times. State how many times the inner loop body executes in total and explain why.", 3, [
            MP("The inner body runs 24 times", ["24"]),
            MP("The inner loop completes fully for each outer iteration", ["each outer", "completes", "every time", "fully"]),
            MP("So the totals are multiplied together", ["multiplied", "4 x 6", "times", "product"]),
        ], "The inner loop body executes 24 times in total. Each time the outer loop runs one iteration, the inner loop starts from the beginning and completes all six of its own iterations before control returns to the outer loop. Since the outer loop repeats four times, the inner body runs six times on each of those four occasions, and 4 multiplied by 6 gives 24. This multiplication is why nested loops become expensive very quickly on large amounts of data.",
           command="State"),
        EQ("Write a program that finds and prints the largest number in the list [12, -5, 33, 8, -47, 21] without using the max function.", 4, [
            MP("Initialises the largest to the first element of the list", ["numbers[0]", "first element", "first item"]),
            MP("Loops through every item in the list", ["for", "in numbers", "loop"]),
            MP("Compares each item with the current largest", ["if", ">", "greater", "compare"]),
            MP("Updates the largest when a bigger value is found and prints the result", ["largest =", "update", "print"]),
        ], "numbers = [12, -5, 33, 8, -47, 21]\nlargest = numbers[0]\n\nfor n in numbers:\n    if n > largest:\n        largest = n\n\nprint(\"The largest number is\", largest)\n\nThe variable largest is initialised to the first element of the list rather than to 0, which matters because the list contains negative numbers and initialising to 0 would give a wrong answer if every value were negative. The loop then compares each value with the current largest and replaces it whenever a bigger one is found, so after the loop finishes largest holds the maximum.",
           command="Write"),
    ],
)

P_LISTS = Topic(
    slug="lists-and-strings",
    title="Lists and Strings",
    spec="2.2",
    icon="i-list",
    minutes=26,
    blurb="Storing many values, slicing, the string methods you will actually use, and the list comprehension that replaces four lines with one.",
    fact="Strings in Python cannot be changed once created. Every method that appears to modify a string actually builds a brand new one, which is why you must assign the result to something.",
    sections=[
        Section("Lists", """
```python
scores = [45, 78, 12, 90, 33]
names = ["Aisha", "Ben", "Chloe"]
mixed = [1, "two", 3.0, True]
empty = []
```

### Accessing items

```python
print(scores[0])      # 45, the first
print(scores[-1])     # 33, the last
print(scores[1:4])    # [78, 12, 90], a slice
print(len(scores))    # 5
```

!key Indexes start at 0 :: A list of 5 items has indexes 0 to 4. Negative indexes count backwards, so -1 is the last item.

### Changing a list

```python
scores[0] = 50            # replace an item
scores.append(60)         # add to the end
scores.insert(1, 99)      # insert at a position
scores.remove(12)         # remove the first occurrence of the value 12
popped = scores.pop()     # remove and return the last item
del scores[0]             # delete by index
scores.sort()             # sort in place
scores.reverse()          # reverse in place
scores.clear()            # empty it
```

### Useful functions

```python
print(sum(scores), max(scores), min(scores), len(scores))
print(sorted(scores))              # a sorted copy, original untouched
print(scores.count(45))            # how many times 45 appears
print(scores.index(78))            # position of the first 78
print(78 in scores)                # True or False
```

### List comprehensions

A compact way to build a list from another list.

```python
squares = [n * n for n in range(1, 6)]           # [1, 4, 9, 16, 25]
evens = [n for n in scores if n % 2 == 0]        # only the even scores
upper = [name.upper() for name in names]         # every name in capitals
```

The long form of the first one is:

```python
squares = []
for n in range(1, 6):
    squares.append(n * n)
```

Both are correct. Use whichever is clearer for the situation.
"""),
        Section("Strings", """
### Slicing

Strings work like lists of characters.

```python
word = "Computing"
print(word[0])        # C
print(word[-1])       # g
print(word[0:4])      # Comp
print(word[4:])       # uting
print(word[:4])       # Comp
print(word[::-1])     # gnitupmoC, reversed
print(len(word))      # 9
```

### Methods

```python
text = "  Hello World  "

print(text.strip())            # "Hello World", removes surrounding spaces
print(text.upper())            # "  HELLO WORLD  "
print(text.lower())
print(text.title())            # capitalises each word
print(text.replace("l", "L"))
print(text.strip().split(" ")) # ["Hello", "World"]
print("-".join(["a", "b", "c"]))  # "a-b-c"
print(text.count("l"))         # 3
print(text.find("World"))      # position, or -1 if not found
print("Hello" in text)         # True
```

### Checking what a string contains

```python
"42".isdigit()      # True
"abc".isalpha()     # True
"abc123".isalnum()  # True
" ".isspace()       # True
```

`isdigit()` is the standard way to check that input can safely be converted to a number.

!warn Strings cannot be changed in place :: `text.upper()` does not change `text`, it returns a new string. You must write `text = text.upper()` to keep the result.

### f-strings

The clearest way to build text containing values.

```python
name = "Aisha"
score = 92

print(f"{name} scored {score} out of 100")
print(f"That is {score / 100:.1%}")        # 92.0%
print(f"Rounded: {3.14159:.2f}")           # 3.14
```
"""),
        Section("Putting them together", """
### Counting vowels

```python
word = input("Enter a word: ").lower()
vowels = 0

for letter in word:
    if letter in "aeiou":
        vowels += 1

print(f"{word} contains {vowels} vowels")
```

### Checking a palindrome

```python
phrase = input("Enter a phrase: ").lower().replace(" ", "")

if phrase == phrase[::-1]:
    print("That is a palindrome")
else:
    print("That is not a palindrome")
```

### Reading a list of names and sorting them

```python
names = []

while True:
    entry = input("Enter a name, or press enter to finish: ").strip()
    if entry == "":
        break
    names.append(entry.title())

names.sort()
print(f"\\n{len(names)} names, in order:")
for i, name in enumerate(names, start=1):
    print(f"{i}. {name}")
```

### Basic statistics

```python
marks = [67, 82, 45, 91, 58, 73]

marks_sorted = sorted(marks)
middle = len(marks_sorted) // 2

if len(marks_sorted) % 2 == 1:
    median = marks_sorted[middle]
else:
    median = (marks_sorted[middle - 1] + marks_sorted[middle]) / 2

print(f"Mean:   {sum(marks) / len(marks):.1f}")
print(f"Median: {median}")
print(f"Range:  {max(marks) - min(marks)}")
```
"""),
    ],
    keyterms=[
        ("List", "An ordered collection of values accessed by index, which can be changed."),
        ("Index", "The position of an item in a list or string, counting from 0."),
        ("Slice", "A section of a list or string, taken with a start and end index."),
        ("append", "A list method that adds an item to the end."),
        ("List comprehension", "A compact expression that builds a new list from an existing one."),
        ("Immutable", "Cannot be changed after creation. Strings in Python are immutable."),
        ("split", "A string method that breaks text into a list at a chosen separator."),
        ("join", "A string method that combines a list of strings into one string."),
        ("f-string", "A string beginning with f where values in braces are inserted directly."),
    ],
    grade="""
+ Use negative indexes and slices confidently on both lists and strings
+ Remember that string methods return a new string rather than changing the original
+ Use split and join to move between text and lists
+ Use f-strings for all output that mixes text and values
+ Know when a list comprehension is clearer than a loop, and when it is not
""",
    mistakes=[
        "Writing `text.upper()` and expecting text to change. Assign the result.",
        "Using an index equal to the length of the list, which is out of range.",
        "Using `remove()` with an index. It removes by value, `del` removes by index.",
        "Forgetting that `sort()` changes the list while `sorted()` returns a copy.",
        "Building output with lots of + and str() instead of an f-string.",
    ],
    quiz=[
        Q("What does `scores[-1]` give?", ["The last item", "The first item",
                                          "An error", "The length"], 0,
          "Negative indexes count backwards from the end, so -1 is the last item."),
        Q("What does `\"Computing\"[0:4]` give?", ["Comp", "Compu", "omput", "puting"], 0,
          "A slice includes the start index and excludes the end index."),
        Q("What does `text.upper()` do to the variable text?",
          ["Nothing, it returns a new string", "Changes text to upper case",
           "Deletes text", "Causes an error"], 0,
          "Strings are immutable, so you must assign the result to keep it."),
        Q("What does `\"a,b,c\".split(\",\")` produce?",
          ["['a', 'b', 'c']", "'abc'", "['a,b,c']", "An error"], 0,
          "split breaks the string at each separator and returns a list of the pieces."),
        Q("What does `scores.append(5)` do?", ["Adds 5 to the end of the list",
                                               "Inserts 5 at the start", "Removes 5", "Sorts the list"], 0,
          "append always adds to the end and makes the list one longer."),
        Q("What is the difference between `sort()` and `sorted()`?",
          ["sort() changes the list, sorted() returns a new sorted copy",
           "sorted() changes the list, sort() returns a copy",
           "They are identical", "sorted() only works on strings"], 0,
          "Use sorted() when the original order still matters elsewhere."),
        Q("What does `word[::-1]` give?", ["The string reversed", "The first character",
                                           "The last character", "An error"], 0,
          "A step of -1 walks through the sequence backwards."),
        Q("Which method checks that a string contains only digits?",
          ["isdigit()", "isnumber()", "isint()", "digit()"], 0,
          "It is the standard way to check that input can be safely converted with int()."),
        Q("What does `f\"Score: {points}\"` do?",
          ["Inserts the value of points into the text", "Prints the word points",
           "Creates a list", "Causes an error"], 0,
          "An f-string evaluates whatever is inside the braces and inserts the result."),
        Q("What does `[n * 2 for n in [1, 2, 3]]` produce?",
          ["[2, 4, 6]", "[1, 2, 3]", "6", "[1, 4, 9]"], 0,
          "A list comprehension applies the expression to each item and collects the results."),
    ],
    exam=[
        EQ("State what is meant by saying that strings in Python are immutable.", 2, [
            MP("A string cannot be changed after it is created", ["cannot be changed", "immutable", "not modified", "fixed"]),
            MP("Methods return a new string rather than altering the original", ["new string", "returns", "does not alter", "must assign"]),
        ], "Immutable means that once a string has been created its contents cannot be altered. Methods such as upper, replace and strip do not change the original string at all: they build and return a brand new string, which is why the result must be assigned to a variable if it is to be kept.",
           command="State"),
        EQ("Write a program that counts how many vowels are in a word entered by the user.", 4, [
            MP("Reads the word and converts it to lower case", ["input", "lower()"]),
            MP("Initialises a counter to zero", ["= 0", "count", "vowels = 0"]),
            MP("Loops through each character in the word", ["for", "in word", "each letter"]),
            MP("Increases the counter when the character is a vowel and prints the total", ["aeiou", "in \"aeiou\"", "+= 1", "print"]),
        ], "word = input(\"Enter a word: \").lower()\nvowels = 0\n\nfor letter in word:\n    if letter in \"aeiou\":\n        vowels += 1\n\nprint(f\"{word} contains {vowels} vowels\")\n\nConverting the input to lower case means capital letters are counted too. The loop walks through the string one character at a time, and the in operator checks whether the current character appears in the string of vowels, which is much shorter than writing five separate comparisons.",
           command="Write"),
        EQ("Explain the difference between the list methods sort() and the function sorted().", 3, [
            MP("sort() rearranges the original list in place", ["in place", "original", "changes the list", "rearranges"]),
            MP("sorted() returns a new sorted list", ["new list", "copy", "returns", "leaves the original"]),
            MP("Use sorted() when the original order must be kept", ["keep", "original order", "unchanged", "still need"]),
        ], "The sort method rearranges the items of the list it is called on, changing the original list permanently and returning nothing. The sorted function leaves the original list completely untouched and returns a brand new list containing the same items in order. Which one to use depends on whether the original order still matters: if it does, sorted must be used, otherwise the original ordering is lost and cannot be recovered.",
           command="Explain"),
        EQ("Write a program that reads a line of text containing names separated by commas and prints each name on its own line, numbered.", 5, [
            MP("Reads the line of input", ["input", "line"]),
            MP("Splits it on commas into a list", ["split(\",\")", "split", "comma"]),
            MP("Loops through the resulting list", ["for", "loop", "each"]),
            MP("Removes surrounding spaces from each name", ["strip", "trim", "spaces"]),
            MP("Prints each name with a number", ["print", "enumerate", "number", "count"]),
        ], "line = input(\"Enter names separated by commas: \")\nnames = line.split(\",\")\n\nfor i, name in enumerate(names, start=1):\n    print(f\"{i}. {name.strip()}\")\n\nThe split method breaks the line into a list at every comma. Because the user is likely to type a space after each comma, strip is used to remove any surrounding whitespace from each name before it is printed. Using enumerate with start set to 1 gives a counter beginning at 1 rather than 0, which is more natural for a numbered list shown to a user.",
           command="Write"),
        EQ("A program uses `numbers[5]` on a list containing five items and crashes. Explain why and state the valid range of indexes.", 3, [
            MP("List indexes start at 0", ["start at 0", "zero", "first is 0"]),
            MP("Five items therefore occupy indexes 0 to 4", ["0 to 4", "four", "0,1,2,3,4"]),
            MP("Index 5 is out of range so an IndexError occurs", ["out of range", "indexerror", "does not exist", "no item"]),
        ], "Python lists are indexed from 0, so the first item is at index 0 rather than index 1. A list containing five items therefore occupies indexes 0, 1, 2, 3 and 4, and there is no item at index 5. Attempting to access it raises an IndexError and the program stops. The highest valid index is always the length of the list minus one, which is why loops over a list use range(len(numbers)) rather than range(1, len(numbers) + 1).",
           command="Explain"),
    ],
)

P_FUNCTIONS = Topic(
    slug="functions",
    title="Functions and Structure",
    spec="2.3",
    icon="i-layers",
    minutes=26,
    blurb="Writing your own functions, parameters and return values, scope, default arguments, and structuring a program that stays readable at 300 lines.",
    fact="A function that does one thing and has a name that says what it does is the single most powerful tool in programming. Almost every difficult codebase in the world got that way because someone stopped doing this.",
    sections=[
        Section("Defining and calling", """
```python
def greet(name):
    print(f"Hello, {name}!")

greet("Aisha")
greet("Ben")
```

- `def` starts the definition
- `name` is a **parameter**, a value the function needs
- `"Aisha"` is an **argument**, the actual value passed in

### Returning a value

```python
def area_of_rectangle(width, height):
    return width * height

a = area_of_rectangle(5, 3)
print(a)                          # 15
print(area_of_rectangle(2, 8))    # 16
```

A function that **returns** gives a value back so it can be used in a calculation, stored, or printed. A function that only prints has thrown the answer away.

!key print is not return :: `print` shows something to the user. `return` hands a value back to the program. A function that calculates something should almost always return it.

### Multiple return values

```python
def stats(numbers):
    return min(numbers), max(numbers), sum(numbers) / len(numbers)

lowest, highest, mean = stats([4, 8, 15, 16, 23])
print(lowest, highest, mean)
```

### Default and named arguments

```python
def greet(name, greeting="Hello"):
    print(f"{greeting}, {name}!")

greet("Aisha")                      # Hello, Aisha!
greet("Ben", "Good morning")        # Good morning, Ben!
greet(greeting="Hi", name="Chloe")  # Hi, Chloe!
```
"""),
        Section("Scope", """
A **local** variable exists only inside the function that created it.

```python
def calculate():
    result = 42          # local
    return result

calculate()
print(result)            # NameError, result does not exist out here
```

A **global** variable exists everywhere.

```python
TAX_RATE = 0.2           # global constant

def add_tax(amount):
    return amount * (1 + TAX_RATE)
```

Reading a global is fine. Changing one from inside a function requires the `global` keyword and is almost always a sign the design could be better.

```python
score = 0

def add_point():
    global score         # avoid this where you can
    score += 1
```

Better:

```python
def add_point(score):
    return score + 1

score = add_point(score)
```

### Why local is better

- Nothing outside the function can change it by accident
- Two functions can use the same name without interfering
- The function's behaviour depends only on what you pass in, so it is far easier to test
"""),
        Section("Structuring a program", """
### One function, one job

```python
def load_scores(filename):
    ...

def calculate_average(scores):
    ...

def find_top_student(scores):
    ...

def display_report(scores):
    ...

def main():
    scores = load_scores("scores.txt")
    display_report(scores)

main()
```

The `main()` function at the bottom reads like a summary of the program. That is the goal.

### A complete example

```python
def get_valid_number(prompt, low, high):
    # Keep asking until the answer is a whole number in range
    while True:
        entry = input(prompt).strip()
        if entry.lstrip("-").isdigit():
            value = int(entry)
            if low <= value <= high:
                return value
        print(f"Please enter a whole number between {low} and {high}.")


def grade_for(mark):
    if mark >= 70:
        return "Distinction"
    elif mark >= 50:
        return "Merit"
    elif mark >= 40:
        return "Pass"
    return "Fail"


def summarise(marks):
    return {
        "count": len(marks),
        "mean": sum(marks) / len(marks),
        "highest": max(marks),
        "lowest": min(marks),
    }


def main():
    marks = []
    how_many = get_valid_number("How many marks? ", 1, 30)

    for i in range(how_many):
        mark = get_valid_number(f"Mark {i + 1}: ", 0, 100)
        marks.append(mark)

    stats = summarise(marks)
    print(f"\\n{stats['count']} marks entered")
    print(f"Mean:    {stats['mean']:.1f} ({grade_for(stats['mean'])})")
    print(f"Highest: {stats['highest']} ({grade_for(stats['highest'])})")
    print(f"Lowest:  {stats['lowest']} ({grade_for(stats['lowest'])})")


main()
```

Every function does one thing, is named after what it does, and can be tested on its own. That is what makes a program maintainable.

### Docstrings

```python
def area_of_circle(radius):
    '''Return the area of a circle with the given radius.'''
    return 3.14159 * radius ** 2

help(area_of_circle)
```
"""),
    ],
    keyterms=[
        ("Function", "A named block of code that performs a task and can be called from anywhere."),
        ("Parameter", "A variable in a function definition that receives a value when it is called."),
        ("Argument", "The actual value passed to a function when it is called."),
        ("return", "A statement that sends a value back to the code that called the function."),
        ("Local variable", "A variable that exists only within the function where it was created."),
        ("Global variable", "A variable accessible from anywhere in the program."),
        ("Scope", "The region of a program in which a variable can be accessed."),
        ("Default argument", "A parameter given a value in the definition, used when no argument is supplied."),
        ("Docstring", "A string at the top of a function describing what it does."),
    ],
    grade="""
+ Write functions that return rather than print, so results can be reused
+ Give every function one job and a name that says exactly what that job is
+ Keep variables local, and pass values in as parameters instead of using globals
+ Write a main() function that reads like a summary of the whole program
+ Add a docstring to any function whose purpose is not obvious from its name
""",
    mistakes=[
        "Printing inside a function that should return, so the value cannot be reused.",
        "Forgetting return entirely, so the function silently gives back None.",
        "Using global variables to pass values around instead of parameters.",
        "Writing one function that does five things, which then cannot be tested or reused.",
        "Calling a function before defining it.",
    ],
    quiz=[
        Q("What keyword defines a function in Python?", ["def", "function", "func", "define"], 0,
          "def is followed by the name, the parameters in brackets and a colon."),
        Q("What is the difference between a parameter and an argument?",
          ["A parameter is in the definition, an argument is the value passed in",
           "An argument is in the definition", "They are the same", "Parameters only work with numbers"], 0,
          "The definition lists parameters. The call supplies arguments to fill them."),
        Q("What does a function return if it has no return statement?",
          ["None", "0", "An empty string", "An error"], 0,
          "Python returns None automatically, which is a common cause of confusing bugs."),
        Q("Why should a calculation function return rather than print?",
          ["So the value can be stored, reused or used in further calculations",
           "print is slower", "return uses less memory", "Python requires it"], 0,
          "A function that prints has thrown the answer away and cannot be used as a building block."),
        Q("What is a local variable?",
          ["One that exists only inside the function where it was created",
           "One available everywhere", "One that never changes", "One stored in a file"], 0,
          "Its limited scope is what stops other parts of the program interfering with it."),
        Q("In `def greet(name, greeting=\"Hello\")`, what is greeting?",
          ["A parameter with a default value", "A global variable",
           "A return value", "An error"], 0,
          "If no argument is supplied for it, the default is used."),
        Q("What happens if you access a local variable outside its function?",
          ["A NameError, because it does not exist there", "It returns 0",
           "It returns None", "Nothing happens"], 0,
          "The variable is destroyed when the function ends, so the name is undefined outside."),
        Q("Why are globals usually avoided?",
          ["Any part of the program can change them, which causes hard to find bugs",
           "They are slower", "They cannot hold numbers", "Python does not support them"], 0,
          "When anything can change a value, tracking down what did becomes very difficult."),
        Q("What does `return min(x), max(x)` do?",
          ["Returns both values together, which can be unpacked into two variables",
           "Returns only the minimum", "Causes an error", "Prints both values"], 0,
          "Python returns them as a tuple, which can be unpacked with two names on the left."),
        Q("What is a docstring?",
          ["A string at the top of a function describing what it does",
           "A comment starting with a hash", "A variable name", "A type of error"], 0,
          "It is accessible with help() and is the standard way to document a function."),
    ],
    exam=[
        EQ("Explain the difference between print and return in a function.", 3, [
            MP("print displays a value to the user", ["display", "shows", "screen", "output to the user"]),
            MP("return sends a value back to the code that called the function", ["sends back", "returns", "calling code", "gives back"]),
            MP("A returned value can be stored or used again, a printed value cannot", ["stored", "reused", "used again", "assigned", "further calculation"]),
        ], "The print function displays a value on the screen for the user to read, and once it has been displayed the program has no further access to it. The return statement sends a value back to whatever code called the function, so it can be stored in a variable, passed into another function or used in a further calculation. A function that calculates something should almost always return it, because a function that only prints has effectively thrown the result away and cannot be used as a building block anywhere else in the program.",
           command="Explain"),
        EQ("Write a function called convert_to_celsius that takes a temperature in Fahrenheit as a parameter and returns the equivalent in Celsius. The formula is (F - 32) multiplied by 5 divided by 9.", 4, [
            MP("Uses def with a suitable name and a parameter", ["def", "convert_to_celsius", "parameter", "(f"]),
            MP("Applies the subtraction of 32 first", ["- 32", "minus 32"]),
            MP("Multiplies by 5 and divides by 9", ["* 5", "/ 9", "5/9"]),
            MP("Returns the result rather than printing it", ["return"]),
        ], "def convert_to_celsius(fahrenheit):\n    return (fahrenheit - 32) * 5 / 9\n\nprint(convert_to_celsius(212))    # 100.0\n\nThe brackets around the subtraction are essential, because without them Python would multiply by 5 before subtracting 32 and give the wrong answer. The function returns the value rather than printing it, so the result can be stored, rounded, or used in a further calculation by whatever called it.",
           command="Write"),
        EQ("Explain what is meant by the scope of a variable and why local variables are usually preferred.", 4, [
            MP("Scope is the region of the program where a variable can be accessed", ["region", "where", "accessed", "visible", "part of the program"]),
            MP("A local variable exists only inside its function", ["local", "inside", "only within", "function"]),
            MP("A global variable can be accessed from anywhere", ["global", "anywhere", "whole program", "everywhere"]),
            MP("Local variables cannot be changed accidentally elsewhere, so bugs are easier to avoid", ["accidentally", "cannot be changed", "protected", "bugs", "isolated", "easier to test"]),
        ], "The scope of a variable is the part of the program in which that variable can be accessed. A local variable is created inside a function and exists only while that function is running, so nothing outside can see or alter it. A global variable is created outside all functions and can be read and modified from anywhere in the program. Local variables are usually preferred because their limited scope means no other part of the program can change them by accident, which removes a very common and difficult to trace source of bugs. It also means two different functions can safely use the same variable name without interfering, and it makes each function far easier to test, because its behaviour depends only on the arguments passed into it rather than on the state of the rest of the program.",
           command="Explain"),
        EQ("Explain two benefits of splitting a program into several functions.", 4, [
            MP("Code that is needed more than once is written only once", ["once", "reuse", "not repeated", "duplication"]),
            MP("A change only needs to be made in one place", ["one place", "single edit", "easier to change", "maintain"]),
            MP("Each function can be tested on its own", ["test", "separately", "individually", "isolate"]),
            MP("The program becomes easier to read and understand", ["readable", "understand", "clearer", "organised", "structure"]),
        ], "The first benefit is the removal of duplication. Code that is needed in several places can be written once as a function and called wherever it is required, so the program is shorter, and crucially any correction or improvement only has to be made in one place rather than being repeated in every copy, which removes the risk of leaving an old version behind. The second benefit is that a program built from small functions is far easier to develop, test and read. Each function does one clearly defined job and can be tested independently with a range of inputs until it is known to be correct, and the main program then reads as a sequence of well named steps that describe what the program does without the reader having to follow every line of detail.",
           command="Explain"),
        EQ("Write a function that takes a list of numbers and returns the mean, and explain why it should return rather than print the result.", 4, [
            MP("Defines a function with a list parameter", ["def", "(numbers", "parameter"]),
            MP("Calculates the total and divides by the number of items", ["sum", "len", "/", "average"]),
            MP("Uses return", ["return"]),
            MP("Explains that returning allows the value to be reused elsewhere", ["reused", "stored", "further calculation", "used again", "flexible"]),
        ], "def mean(numbers):\n    return sum(numbers) / len(numbers)\n\naverage = mean([4, 8, 15, 16, 23])\nprint(f\"The mean is {average:.2f}\")\n\nThe function should return the value rather than printing it because returning keeps the function general and reusable. The calling code can then decide what to do with the answer: display it, round it, compare it with another average, store it in a file or use it in a further calculation. A function that printed the mean directly would be locked to one use and could not be built on, and it would also be far harder to test automatically, because a test can compare a returned value against an expected one but cannot easily check what was printed.",
           command="Write"),
    ],
)

P_DATA = Topic(
    slug="dictionaries-files-and-errors",
    title="Dictionaries, Files and Error Handling",
    spec="3.1",
    icon="i-database",
    minutes=28,
    blurb="Storing structured data, saving it between runs, and writing programs that survive things going wrong.",
    fact="Almost every real program you use stores its data as key and value pairs. Settings files, web APIs, save games and configuration are all essentially dictionaries.",
    sections=[
        Section("Dictionaries", """
A **dictionary** stores pairs of **keys** and **values**. You look a value up by its key rather than by a numeric position, which makes the code far more readable.

```python
student = {
    "name": "Aisha",
    "year": 11,
    "grades": [8, 9, 7],
    "active": True
}

print(student["name"])          # Aisha
student["year"] = 12            # change a value
student["house"] = "Blue"       # add a new pair
del student["active"]           # remove a pair
```

### Safe access

```python
print(student.get("email"))                 # None, no crash
print(student.get("email", "not given"))    # a default value
print("name" in student)                    # True
```

Using square brackets on a missing key raises a `KeyError`. Use `get()` when the key might not be there.

### Looping

```python
for key in student:
    print(key, "=", student[key])

for key, value in student.items():
    print(f"{key}: {value}")

print(list(student.keys()))
print(list(student.values()))
```

### A list of dictionaries

This is how most real data is shaped.

```python
students = [
    {"name": "Aisha", "mark": 92},
    {"name": "Ben", "mark": 68},
    {"name": "Chloe", "mark": 77},
]

for s in students:
    print(f"{s['name']:<8} {s['mark']}")

best = max(students, key=lambda s: s["mark"])
print("Top:", best["name"])

average = sum(s["mark"] for s in students) / len(students)
print(f"Average: {average:.1f}")
```

### Tuples and sets

```python
point = (3, 7)              # a tuple, cannot be changed
x, y = point                # unpacking

unique = {1, 2, 2, 3, 3}    # a set, duplicates removed
print(unique)               # {1, 2, 3}
```
"""),
        Section("Files", """
### Writing and reading

```python
# Write, which ERASES the file first
with open("scores.txt", "w") as file:
    file.write("Aisha,92\\n")
    file.write("Ben,68\\n")

# Append, which adds to the end
with open("scores.txt", "a") as file:
    file.write("Chloe,77\\n")

# Read line by line
with open("scores.txt", "r") as file:
    for line in file:
        name, mark = line.strip().split(",")
        print(f"{name} scored {mark}")

# Read the whole file
with open("scores.txt", "r") as file:
    contents = file.read()

# Read into a list of lines
with open("scores.txt", "r") as file:
    lines = file.readlines()
```

`with open(...)` closes the file automatically, even if an error happens. Always use it.

| Mode | Meaning |
| `"r"` | Read. Fails if the file does not exist. |
| `"w"` | Write. Creates the file, and erases anything already in it. |
| `"a"` | Append. Creates if needed, adds to the end. |

!warn Write mode destroys the file :: If a question or a program needs to add a record without losing existing data, the mode must be `"a"`.

### CSV files

```python
import csv

with open("students.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(["Name", "Mark"])
    writer.writerow(["Aisha", 92])

with open("students.csv", "r") as file:
    reader = csv.reader(file)
    next(reader)                     # skip the header row
    for row in reader:
        print(row[0], row[1])
```

### JSON, for saving structured data

```python
import json

data = {"players": ["Aisha", "Ben"], "high_score": 4200}

with open("save.json", "w") as file:
    json.dump(data, file)

with open("save.json", "r") as file:
    loaded = json.load(file)

print(loaded["high_score"])
```

JSON is ideal for saving dictionaries and lists exactly as they are, which makes it the natural way to save game state or settings.
"""),
        Section("Error handling", """
A robust program does not crash when something goes wrong. It handles it.

```python
try:
    age = int(input("Enter your age: "))
    print(f"Next year you will be {age + 1}")
except ValueError:
    print("That was not a whole number.")
```

### Handling several kinds of error

```python
try:
    with open("data.txt", "r") as file:
        numbers = [int(line) for line in file]
    print(sum(numbers) / len(numbers))

except FileNotFoundError:
    print("The file does not exist yet.")
except ValueError:
    print("The file contains something that is not a number.")
except ZeroDivisionError:
    print("The file is empty.")
else:
    print("Everything worked.")
finally:
    print("Finished.")
```

- `except` runs when that error occurs
- `else` runs only if there was no error
- `finally` runs either way, which is useful for tidying up

### Errors worth catching

| Error | When |
| `ValueError` | Converting text that is not a number |
| `FileNotFoundError` | Opening a file that does not exist |
| `ZeroDivisionError` | Dividing by zero |
| `KeyError` | Looking up a key that is not in a dictionary |
| `IndexError` | Using an index beyond the end of a list |
| `TypeError` | An operation between incompatible types |

!key Catch specific errors, not everything :: A bare `except:` hides real bugs, including typos in your own code, and makes problems far harder to find. Name the error you expect.

### A robust input function

```python
def get_int(prompt, low, high):
    while True:
        try:
            value = int(input(prompt))
            if low <= value <= high:
                return value
            print(f"Please enter a number between {low} and {high}.")
        except ValueError:
            print("That is not a whole number.")
```

This function cannot crash and cannot return an invalid value. That is what robust means.
"""),
    ],
    keyterms=[
        ("Dictionary", "A collection storing pairs of keys and values, looked up by key."),
        ("Key", "The name used to look up a value in a dictionary."),
        ("Tuple", "An ordered collection that cannot be changed after creation."),
        ("Set", "An unordered collection with no duplicate values."),
        ("with open()", "A statement that opens a file and closes it automatically when finished."),
        ("Append mode", "Opening a file so new data is added to the end without erasing existing content."),
        ("CSV", "Comma separated values, a simple text format for tabular data."),
        ("JSON", "A text format for storing structured data such as dictionaries and lists."),
        ("Exception", "An error raised while a program is running."),
        ("try and except", "A structure that attempts code and handles an error rather than crashing."),
    ],
    grade="""
+ Use a dictionary whenever data has named fields, rather than remembering list positions
+ Always use `with open()` so files close even when something fails
+ Choose append mode whenever existing data must be preserved
+ Catch the specific exception you expect, never a bare except
+ Write input functions that cannot crash and cannot return an invalid value
""",
    mistakes=[
        "Opening a file in write mode when the existing contents matter.",
        "Using square brackets on a dictionary key that might not exist, causing a KeyError.",
        "Using a bare except, which hides typos and real bugs.",
        "Forgetting to strip the newline character when reading lines from a file.",
        "Assuming a file exists, so the program crashes the very first time it runs.",
    ],
    quiz=[
        Q("What does a dictionary store?", ["Pairs of keys and values", "Only numbers",
                                            "An ordered list of items", "A grid of values"], 0,
          "You look values up by a meaningful key rather than a numeric index."),
        Q("What does `student.get(\"email\")` return if there is no email key?",
          ["None", "An empty string", "A KeyError", "0"], 0,
          "get() returns None rather than crashing, and you can supply your own default instead."),
        Q("Which file mode preserves existing content?", ["\"a\"", "\"w\"", "\"r\"", "\"x\""], 0,
          "Append adds to the end. Write erases the file before writing."),
        Q("Why use `with open(...)` rather than `open(...)`?",
          ["The file is closed automatically even if an error occurs",
           "It reads faster", "It allows more modes", "It compresses the file"], 0,
          "Forgetting to close a file can mean data is never actually written to disk."),
        Q("Which error occurs when converting the text 'hello' to an integer?",
          ["ValueError", "TypeError", "KeyError", "IndexError"], 0,
          "The type is right, a string, but the value cannot represent a number."),
        Q("What does `finally` do in a try block?",
          ["Runs whether or not an error occurred", "Runs only if there was an error",
           "Runs only if there was no error", "Ends the program"], 0,
          "It is used for tidying up, such as closing a connection, that must happen either way."),
        Q("Why should you avoid a bare `except:`?",
          ["It hides real bugs including your own typos",
           "It is slower", "Python does not allow it", "It only catches one error"], 0,
          "Catching everything means a NameError from a spelling mistake gets silently swallowed."),
        Q("What is a tuple?", ["An ordered collection that cannot be changed",
                               "A collection with no duplicates", "A key value store", "A type of file"], 0,
          "Tuples are immutable, which makes them suitable for fixed data such as coordinates."),
        Q("What format is best for saving a dictionary to a file so it can be loaded back exactly?",
          ["JSON", "A plain text file", "A CSV file", "An image file"], 0,
          "JSON preserves the structure, so nested lists and dictionaries come back exactly as they were."),
        Q("Which error occurs when you look up a dictionary key that does not exist using square brackets?",
          ["KeyError", "IndexError", "ValueError", "NameError"], 0,
          "Use get() instead if the key might legitimately be missing."),
    ],
    exam=[
        EQ("State one advantage of using a dictionary rather than a list to store a student's details.", 2, [
            MP("Values are accessed by a meaningful name rather than a numeric position", ["name", "key", "meaningful", "not position", "not index"]),
            MP("This makes the code easier to read and less error prone", ["readable", "easier", "clearer", "less error", "no need to remember"]),
        ], "A dictionary lets each value be accessed by a meaningful key, so writing student[\"mark\"] makes the intention completely clear. With a list you would have to remember that the mark happened to be stored at index 2, which is far harder to read and very easy to get wrong, especially if the order of the fields ever changes.",
           command="State"),
        EQ("Explain why the try and except structure is used, and give an example of when it would be needed.", 4, [
            MP("It attempts code that might cause an error", ["try", "attempts", "might fail", "could cause"]),
            MP("If the error occurs the except block runs instead of the program crashing", ["except", "instead of crashing", "handles", "does not crash"]),
            MP("Gives a valid example such as converting user input or opening a file", ["input", "int(", "file", "not a number", "does not exist"]),
            MP("Explains that this makes the program robust", ["robust", "keeps working", "message", "try again", "handles gracefully"]),
        ], "The try and except structure is used so a program can attempt something that might fail without crashing if it does. The code inside try is executed, and if it raises the named exception then Python jumps straight to the matching except block instead of stopping the program. A common example is converting user input to a number: if the user types letters, int() raises a ValueError, and without handling it the program would crash and the user would lose their work. With try and except the program can display a clear message and ask again. Handling errors like this is what makes a program robust, which means it continues to behave sensibly even when things go wrong.",
           command="Explain"),
        EQ("Write a program that reads a file called marks.txt containing one number per line and prints the average, handling the case where the file does not exist.", 5, [
            MP("Uses try and except around the file operation", ["try", "except"]),
            MP("Opens the file for reading", ["open", "\"r\"", "with open"]),
            MP("Converts each line into a number", ["int(", "float(", "strip", "convert"]),
            MP("Calculates and prints the average", ["sum", "len", "average", "print"]),
            MP("Catches FileNotFoundError with a helpful message", ["filenotfounderror", "does not exist", "not found", "message"]),
        ], "try:\n    with open(\"marks.txt\", \"r\") as file:\n        marks = [int(line.strip()) for line in file if line.strip()]\n    if len(marks) == 0:\n        print(\"The file is empty.\")\n    else:\n        print(f\"Average: {sum(marks) / len(marks):.1f}\")\nexcept FileNotFoundError:\n    print(\"marks.txt could not be found.\")\nexcept ValueError:\n    print(\"The file contains something that is not a number.\")\n\nUsing with open means the file closes automatically. Each line is stripped of its newline before being converted, and blank lines are skipped. The empty file case is checked separately, because dividing by zero would otherwise raise its own error. Two specific exceptions are caught rather than using a bare except, so genuine bugs in the code are not hidden.",
           command="Write"),
        EQ("Explain the difference between opening a file in write mode and append mode.", 3, [
            MP("Write mode erases everything already in the file", ["erases", "deletes", "overwrites", "clears", "removes"]),
            MP("Append mode adds to the end and keeps existing content", ["adds to the end", "keeps", "preserves", "existing"]),
            MP("Append should be used when previous data must be kept", ["must be kept", "high scores", "records", "add a record", "preserve"]),
        ], "Opening a file in write mode empties it completely before anything is written, so every piece of data previously stored in that file is lost. Opening in append mode leaves the existing contents intact and adds anything written to the end. Write mode is appropriate when the entire contents are being replaced, such as saving a complete updated set of records. Append mode is essential whenever a single new record is being added to data that must be preserved, for example writing one more high score to a file that already contains a list of them.",
           command="Explain"),
        EQ("Explain why catching a specific exception is better than using a bare except that catches everything.", 3, [
            MP("A bare except catches every error including ones you did not anticipate", ["every error", "all errors", "anything", "unexpected"]),
            MP("This hides genuine bugs such as typos in variable names", ["hides", "bugs", "typo", "mistake", "namerror", "conceals"]),
            MP("Catching a specific exception means only the expected problem is handled and other errors are still reported", ["specific", "expected", "still reported", "still shown", "only that"]),
        ], "A bare except catches absolutely every exception, including ones the programmer never anticipated. That means a genuine bug elsewhere in the try block, such as a misspelled variable name raising a NameError, is silently swallowed and replaced with whatever message the except block prints. The program appears to handle the situation while actually hiding a real fault, which can take a very long time to track down. Naming the specific exception, such as except ValueError, means only the problem you actually expected is handled, and any other error still stops the program and reports itself properly so it can be found and fixed.",
           command="Explain"),
    ],
)

P_OOP1 = Topic(
    slug="classes-and-objects",
    title="Object Oriented Programming: Classes and Objects",
    spec="4.1",
    icon="i-cube",
    minutes=30,
    blurb="What a class actually is, how objects hold their own data, and why this way of organising code took over the software industry.",
    fact="The idea of objects came from a 1960s language called Simula, written to simulate real world systems such as ships in a harbour. Modelling real things as objects with their own state turned out to be useful for almost everything.",
    sections=[
        Section("The idea", """
So far, data and the code that works on it have been separate. **Object oriented programming** puts them together.

A **class** is a blueprint. An **object** is a thing built from that blueprint.

Think of a class as the plan for a house and objects as the actual houses. One plan, many houses, each with its own address, its own occupants and its own front door colour.

```python
class Dog:
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed

    def bark(self):
        print(f"{self.name} says woof!")


rex = Dog("Rex", "Labrador")
bella = Dog("Bella", "Collie")

rex.bark()             # Rex says woof!
bella.bark()           # Bella says woof!
print(rex.breed)       # Labrador
```

### The parts

- `class Dog:` defines the blueprint. Class names use CapitalCase by convention.
- `__init__` is the **constructor**. It runs automatically whenever a new object is created, and it sets up that object's starting data.
- `self` refers to **this particular object**. Every method takes it as its first parameter.
- `self.name` is an **attribute**, a piece of data belonging to this object.
- `bark` is a **method**, a function belonging to the class.

!key Why self matters :: `rex` and `bella` share the same methods but have completely separate data. When `rex.bark()` runs, `self` is `rex`, so `self.name` is Rex. The same code produces different behaviour because the data is different.
"""),
        Section("Building a useful class", """
```python
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance
        self.transactions = []

    def deposit(self, amount):
        if amount <= 0:
            return False
        self.balance += amount
        self.transactions.append(("deposit", amount))
        return True

    def withdraw(self, amount):
        if amount <= 0 or amount > self.balance:
            return False
        self.balance -= amount
        self.transactions.append(("withdraw", amount))
        return True

    def statement(self):
        lines = [f"Account: {self.owner}"]
        for kind, amount in self.transactions:
            lines.append(f"  {kind:<9} {amount:>8.2f}")
        lines.append(f"Balance: {self.balance:.2f}")
        return "\\n".join(lines)


account = BankAccount("Aisha", 100)
account.deposit(50)
account.withdraw(30)
account.withdraw(9999)        # refused, returns False
print(account.statement())
```

Notice that the account cannot go overdrawn, because the rule lives inside the class alongside the data it protects. That is the real value of OOP: the object looks after its own correctness.

### Special methods

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"({self.x}, {self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y


p = Point(3, 4)
print(p)                        # (3, 4), because of __str__
print(Point(1, 2) == Point(1, 2))   # True, because of __eq__
```

`__str__` decides what `print()` shows. Without it you get something unhelpful like `<__main__.Point object at 0x7f...>`.
"""),
        Section("Encapsulation", """
**Encapsulation** means bundling data together with the methods that operate on it, and controlling access to that data from outside.

### Why it matters

If any part of a program can reach in and change an object's data directly, the object cannot guarantee anything about itself.

```python
account.balance = -5000     # nothing stops this
```

### Private attributes by convention

A leading underscore signals that an attribute is internal and should not be touched from outside. Two underscores makes Python actively mangle the name to discourage it.

```python
class Temperature:
    def __init__(self, celsius=0):
        self._celsius = celsius

    def get_celsius(self):
        return self._celsius

    def set_celsius(self, value):
        if value < -273.15:
            raise ValueError("Below absolute zero")
        self._celsius = value

    def get_fahrenheit(self):
        return self._celsius * 9 / 5 + 32


t = Temperature(20)
print(t.get_fahrenheit())      # 68.0
t.set_celsius(25)
```

### Properties, the Pythonic way

```python
class Temperature:
    def __init__(self, celsius=0):
        self._celsius = celsius

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Below absolute zero")
        self._celsius = value

    @property
    def fahrenheit(self):
        return self._celsius * 9 / 5 + 32


t = Temperature(20)
print(t.celsius)        # 20, looks like an attribute
print(t.fahrenheit)     # 68.0, calculated on demand
t.celsius = 30          # runs the setter, which validates
```

This gives clean syntax with full control. The validation runs every time, but the code using it reads like a simple attribute.

!key The benefit in one sentence :: Encapsulation means an object controls its own data, so it can guarantee that data stays valid no matter what the rest of the program does.
"""),
    ],
    keyterms=[
        ("Class", "A blueprint defining the attributes and methods that objects of that type will have."),
        ("Object", "A specific instance created from a class, with its own data."),
        ("Instance", "Another word for an object created from a class."),
        ("Attribute", "A piece of data belonging to an object."),
        ("Method", "A function defined inside a class that operates on an object."),
        ("Constructor", "The __init__ method, which runs automatically when an object is created."),
        ("self", "The parameter referring to the particular object a method is operating on."),
        ("Encapsulation", "Bundling data with the methods that act on it, and controlling access from outside."),
        ("Property", "A method that is accessed like an attribute, allowing validation on assignment."),
    ],
    grade="""
+ Explain the difference between a class and an object using a concrete example
+ Write a constructor that sets up every attribute the object needs
+ Put validation inside the class so the object cannot be put into an invalid state
+ Add `__str__` to every class so printing an object is useful
+ Explain encapsulation as the object controlling its own data, not just as hiding
""",
    mistakes=[
        "Forgetting self as the first parameter of every method.",
        "Forgetting self when referring to an attribute inside a method.",
        "Confusing a class with an object. The class is the blueprint, the object is built from it.",
        "Putting validation in the calling code rather than inside the class, so any other caller can bypass it.",
        "Defining attributes outside __init__, so different objects end up with different attributes.",
    ],
    quiz=[
        Q("What is the difference between a class and an object?",
          ["A class is a blueprint, an object is a specific thing built from it",
           "An object is a blueprint for a class", "They are the same",
           "A class can only be used once"], 0,
          "One class can produce any number of objects, each with its own data."),
        Q("What does `__init__` do?",
          ["Runs automatically when a new object is created and sets up its data",
           "Deletes an object", "Prints the object", "Defines a new class"], 0,
          "It is the constructor, and its job is to give the new object its starting attributes."),
        Q("What does `self` refer to?",
          ["The particular object the method is being called on",
           "The class itself", "The program", "The last object created"], 0,
          "It is how a method knows whose data it should be working with."),
        Q("What is an attribute?", ["A piece of data belonging to an object",
                                    "A function inside a class", "The name of the class", "A type of loop"], 0,
          "Methods are the behaviour, attributes are the data."),
        Q("What does `__str__` control?",
          ["What is displayed when the object is printed", "How the object is created",
           "Whether two objects are equal", "The object's attributes"], 0,
          "Without it, printing an object shows an unhelpful memory address."),
        Q("What is encapsulation?",
          ["Bundling data with the methods that act on it and controlling outside access",
           "Creating many objects from one class",
           "One class inheriting from another",
           "Hiding a program's source code"], 0,
          "The point is that the object can guarantee its own data stays valid."),
        Q("Why put validation inside a class rather than in the code that uses it?",
          ["Every use of the class then gets the validation automatically",
           "It runs faster", "Python requires it", "It uses less memory"], 0,
          "If validation lives outside, any caller who forgets it can put the object into an invalid state."),
        Q("What does a leading underscore on an attribute name signal?",
          ["That it is internal and should not be accessed from outside",
           "That it is a constant", "That it is a method", "That it cannot be changed"], 0,
          "Python does not enforce privacy, so the underscore is a convention that other programmers respect."),
        Q("What does the `@property` decorator allow?",
          ["A method to be accessed like an attribute", "A class to inherit",
           "An object to be deleted", "A method to run automatically"], 0,
          "It gives clean syntax while still allowing validation or calculation behind the scenes."),
        Q("Two objects created from the same class:",
          ["Share the same methods but have their own separate data",
           "Share the same data", "Cannot exist at the same time", "Must have identical attributes values"], 0,
          "This is exactly why the same method call produces different results on different objects."),
    ],
    exam=[
        EQ("Explain the difference between a class and an object, using an example.", 3, [
            MP("A class is a template or blueprint defining attributes and methods", ["template", "blueprint", "plan", "defines", "describes"]),
            MP("An object is a specific instance created from that class", ["instance", "created from", "specific", "actual", "built from"]),
            MP("Gives a valid example such as a Dog class with individual dogs as objects", ["example", "dog", "car", "student", "account"]),
        ], "A class is a blueprint that defines what attributes and methods every object of that type will have, but it does not itself hold any particular data. An object is a specific instance created from that class, with its own values for each attribute. For example, a Dog class might define that every dog has a name and a breed and can bark. Creating rex = Dog(\"Rex\", \"Labrador\") and bella = Dog(\"Bella\", \"Collie\") produces two separate objects from that one class, sharing the same methods but each holding its own name and breed.",
           command="Explain"),
        EQ("Write a class called Rectangle with a constructor taking width and height, and a method that returns the area.", 5, [
            MP("Defines the class with a suitable name", ["class rectangle", "class"]),
            MP("Defines __init__ with self, width and height", ["__init__", "self", "width", "height"]),
            MP("Assigns the parameters to attributes using self", ["self.width", "self.height", "self."]),
            MP("Defines a method taking self", ["def area(self)", "def", "self"]),
            MP("Returns width multiplied by height", ["return", "* self.height", "width * height"]),
        ], "class Rectangle:\n    def __init__(self, width, height):\n        self.width = width\n        self.height = height\n\n    def area(self):\n        return self.width * self.height\n\n\nr = Rectangle(5, 3)\nprint(r.area())     # 15\n\nThe constructor runs automatically when a Rectangle is created and stores the width and height as attributes of that particular object. The area method takes self as its first parameter so that it can access those attributes, and it returns the result rather than printing it, so the value can be used in further calculations.",
           command="Write"),
        EQ("Explain what is meant by encapsulation and why it is useful.", 4, [
            MP("Data and the methods that operate on it are bundled together in a class", ["bundled", "together", "combined", "in one place", "data and methods"]),
            MP("Access to the data from outside is controlled", ["controlled", "restricted", "private", "not direct", "through methods"]),
            MP("The object can therefore validate any change to its data", ["validate", "checks", "rules", "invalid", "guarantee"]),
            MP("This prevents other parts of the program putting the object into an invalid state", ["invalid state", "prevents", "cannot", "protects", "corrupt"]),
        ], "Encapsulation means bundling an object's data together with the methods that operate on that data inside a single class, and controlling how the data can be accessed from outside. Rather than allowing any part of the program to change an attribute directly, changes are made through methods or properties belonging to the class. This is useful because it means the object can validate every change before accepting it, so a bank account can refuse a withdrawal that would take the balance below zero, and a temperature can refuse a value below absolute zero. Because the rule lives inside the class, it applies automatically everywhere the class is used, and no other part of the program can accidentally or deliberately put the object into a state that should be impossible.",
           command="Explain"),
        EQ("Explain the purpose of the self parameter in a Python class.", 3, [
            MP("It refers to the particular object the method is being called on", ["particular", "the object", "this object", "instance"]),
            MP("It allows the method to access that object's own attributes", ["attributes", "own data", "access", "its data"]),
            MP("Different objects therefore produce different results from the same method", ["different objects", "different results", "own data", "separate"]),
        ], "The self parameter refers to the specific object on which a method has been called. When rex.bark() is executed, Python passes rex in as self, so inside the method self.name refers to rex's name rather than any other dog's. This is what allows every object created from the same class to share the same method code while behaving differently, because each one has its own set of attribute values. Without self, a method would have no way of knowing whose data it was supposed to be working with.",
           command="Explain"),
        EQ("A class stores a student's mark. Describe how you would ensure the mark can never be set to a value outside 0 to 100.", 4, [
            MP("Store the mark in a private attribute with a leading underscore", ["underscore", "private", "_mark", "internal"]),
            MP("Provide a setter method or property to change it", ["setter", "method", "property", "set_mark"]),
            MP("Validate the value inside that method before assigning it", ["validate", "check", "if", "between", "0 and 100"]),
            MP("Reject or raise an error for invalid values", ["reject", "raise", "error", "refuse", "message", "not accepted"]),
        ], "The mark would be stored in a private attribute such as self._mark, with the leading underscore signalling that it is internal and should not be accessed directly from outside the class. Access would then be provided through a property, with a getter that simply returns the value and a setter that checks the new value before accepting it. The setter would test whether the value is between 0 and 100 inclusive and assign it only if so, raising a ValueError otherwise. Because the check lives inside the class, every piece of code that ever sets a mark goes through it automatically, so it is impossible for any part of the program to leave a student object holding an invalid mark.",
           command="Describe"),
    ],
)

P_OOP2 = Topic(
    slug="inheritance-and-polymorphism",
    title="Inheritance and Polymorphism",
    spec="4.2",
    icon="i-layers",
    minutes=28,
    blurb="Building new classes from existing ones, overriding behaviour, and why a single loop can correctly handle a dozen different kinds of object.",
    fact="Polymorphism means many forms. It is what allows a game to loop through a list containing players, enemies, bullets and explosions and simply call update() on each, without ever asking what any of them actually is.",
    sections=[
        Section("Inheritance", """
**Inheritance** lets a new class take on all the attributes and methods of an existing one, then add or change what it needs.

The existing class is the **parent**, **superclass** or **base class**. The new one is the **child**, **subclass** or **derived class**.

```python
class Animal:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def speak(self):
        return "Some sound"

    def describe(self):
        return f"{self.name} is {self.age} years old"


class Dog(Animal):
    def speak(self):
        return "Woof"


class Cat(Animal):
    def __init__(self, name, age, indoor=True):
        super().__init__(name, age)      # run the parent constructor
        self.indoor = indoor

    def speak(self):
        return "Meow"

    def describe(self):
        base = super().describe()        # reuse the parent version
        where = "indoor" if self.indoor else "outdoor"
        return f"{base} and is an {where} cat"


rex = Dog("Rex", 3)
tom = Cat("Tom", 5, indoor=False)

print(rex.describe())    # Rex is 3 years old
print(rex.speak())       # Woof
print(tom.describe())    # Tom is 5 years old and is an outdoor cat
```

### What is happening

- `class Dog(Animal)` means Dog inherits everything from Animal
- Dog does not define `describe`, so it uses Animal's
- Dog defines its own `speak`, which **overrides** the parent version
- `super()` calls the parent's version of a method, which lets you extend rather than replace

!key Why inheritance is useful :: Shared behaviour is written once in the parent. Every subclass gets it automatically, and a fix in the parent fixes it everywhere at once.
"""),
        Section("Polymorphism", """
**Polymorphism** means objects of different classes can be used through the same interface, each responding in its own way.

```python
animals = [Dog("Rex", 3), Cat("Tom", 5), Dog("Bella", 1)]

for animal in animals:
    print(f"{animal.name}: {animal.speak()}")
```

The loop never checks what kind of animal it has. It calls `speak()` and each object runs its own version. Adding a `Horse` class later requires no change to this loop at all.

### Why this matters enormously

Without polymorphism the loop would need:

```python
for animal in animals:
    if isinstance(animal, Dog):
        print("Woof")
    elif isinstance(animal, Cat):
        print("Meow")
    # and another branch for every new animal, forever
```

Every new type of animal would mean editing every loop in the program. With polymorphism, new behaviour is added by writing a new class and nothing else changes.

### An abstract base class

Sometimes the parent should never be instantiated on its own, only inherited from.

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

    def describe(self):
        return f"{type(self).__name__} with area {self.area():.2f}"


class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14159 * self.radius ** 2


class Square(Shape):
    def __init__(self, side):
        self.side = side

    def area(self):
        return self.side ** 2


for shape in [Circle(3), Square(4)]:
    print(shape.describe())
```

`Shape` guarantees that every subclass provides an `area` method. Trying to create a `Shape()` directly raises an error, which is exactly right because a shape with no specific form has no area.
"""),
        Section("Designing with classes", """
### Composition, an alternative to inheritance

Inheritance means **is a**. Composition means **has a**.

```python
class Engine:
    def start(self):
        return "Engine running"


class Car:
    def __init__(self, make):
        self.make = make
        self.engine = Engine()      # a Car HAS an Engine

    def start(self):
        return f"{self.make}: {self.engine.start()}"
```

A Car is not a kind of Engine, so inheritance would be wrong here. It has one, so composition is right.

!key The test :: If you can say "a Dog is an Animal", inheritance fits. If you can only say "a Car has an Engine", use composition. Getting this wrong produces class hierarchies nobody can understand.

### A worked example: a game

```python
class Entity:
    def __init__(self, name, x, y, health):
        self.name = name
        self.x = x
        self.y = y
        self.health = health

    @property
    def alive(self):
        return self.health > 0

    def take_damage(self, amount):
        self.health = max(0, self.health - amount)

    def update(self):
        pass


class Player(Entity):
    def __init__(self, name, x, y):
        super().__init__(name, x, y, health=100)
        self.score = 0

    def update(self):
        self.score += 1


class Enemy(Entity):
    def __init__(self, name, x, y, damage):
        super().__init__(name, x, y, health=30)
        self.damage = damage

    def update(self):
        self.x += 1        # patrol


entities = [Player("Aisha", 0, 0), Enemy("Slime", 10, 0, damage=5), Enemy("Bat", 20, 5, damage=3)]

for step in range(3):
    for e in entities:
        e.update()

entities = [e for e in entities if e.alive]
for e in entities:
    print(f"{e.name} at ({e.x}, {e.y}) with {e.health} health")
```

One loop updates everything, whatever it is. That is the pattern behind every game engine you have ever used.

### The four pillars, summarised

| Pillar | Meaning |
| **Abstraction** | Exposing only what is needed and hiding the complexity behind it |
| **Encapsulation** | Bundling data with its methods and controlling access to it |
| **Inheritance** | A class taking on the attributes and methods of another |
| **Polymorphism** | Objects of different classes responding to the same method call in their own way |
"""),
    ],
    keyterms=[
        ("Inheritance", "A class taking on the attributes and methods of an existing class."),
        ("Superclass", "The parent class that another class inherits from."),
        ("Subclass", "A class that inherits from another class."),
        ("Override", "Redefining a parent's method in a subclass so the subclass version is used."),
        ("super()", "A function that calls the parent class's version of a method."),
        ("Polymorphism", "Objects of different classes responding to the same method call in their own way."),
        ("Abstract class", "A class that cannot be instantiated and exists only to be inherited from."),
        ("Composition", "Building a class by giving it other objects as attributes, expressing a has a relationship."),
        ("Abstraction", "Exposing only what is needed and hiding the underlying complexity."),
    ],
    grade="""
+ Explain inheritance in terms of code reuse and a single place to fix shared behaviour
+ Explain polymorphism with the argument about not needing to edit existing loops
+ Use super() to extend a parent method rather than duplicating its code
+ Choose inheritance for is a relationships and composition for has a
+ Be able to name and explain all four pillars with a concrete example of each
""",
    mistakes=[
        "Forgetting to call super().__init__() so the parent's attributes are never set up.",
        "Using inheritance for a has a relationship, producing hierarchies that make no sense.",
        "Copying the parent's code into the subclass instead of calling super().",
        "Writing isinstance checks everywhere, which is exactly what polymorphism is meant to remove.",
        "Creating a deep chain of subclasses when one or two levels would do.",
    ],
    quiz=[
        Q("What does inheritance allow?",
          ["A class to take on the attributes and methods of an existing class",
           "Two objects to share the same data", "A method to have several names",
           "A class to be deleted automatically"], 0,
          "The subclass gets everything from the parent and can add or change what it needs."),
        Q("What does `super().__init__(name, age)` do?",
          ["Calls the parent class's constructor", "Creates a new parent object",
           "Deletes the parent class", "Renames the class"], 0,
          "It runs the parent's setup so its attributes are properly initialised."),
        Q("What is overriding?",
          ["Redefining a parent's method in a subclass", "Creating two objects with the same name",
           "Deleting a method", "Calling a method twice"], 0,
          "The subclass version is used instead of the parent's when called on a subclass object."),
        Q("What is polymorphism?",
          ["Objects of different classes responding to the same method call in their own way",
           "A class inheriting from two parents", "Hiding data inside a class",
           "Creating many objects from one class"], 0,
          "It is what lets one loop handle many different types without checking what each one is."),
        Q("A Car and an Engine are best related by:",
          ["Composition, because a Car has an Engine",
           "Inheritance, because a Car is an Engine",
           "They should be the same class", "They cannot be related"], 0,
          "Inheritance expresses is a. A Car is not a kind of Engine, so composition is correct."),
        Q("What happens if a subclass does not define a method the parent has?",
          ["The parent's version is used", "An error occurs",
           "The method does nothing", "The object cannot be created"], 0,
          "That is the point of inheritance: shared behaviour is written once in the parent."),
        Q("Why is polymorphism useful when adding a new type of object to a game?",
          ["Existing loops need no changes at all",
           "It makes the game run faster", "It uses less memory", "It removes the need for classes"], 0,
          "Behaviour is added by writing a new class, and code that calls the shared method keeps working."),
        Q("What is an abstract class?",
          ["A class that cannot be instantiated and exists only to be inherited from",
           "A class with no methods", "A class stored in a separate file", "A class with private attributes"], 0,
          "It defines an interface that subclasses must implement, without providing a usable object itself."),
        Q("Which is NOT one of the four pillars of OOP?",
          ["Iteration", "Abstraction", "Encapsulation", "Polymorphism"], 0,
          "The four are abstraction, encapsulation, inheritance and polymorphism. Iteration is a programming construct."),
        Q("What is the main benefit of putting shared behaviour in a parent class?",
          ["It is written once, so a fix there fixes it in every subclass",
           "Subclasses run faster", "It uses less memory", "It prevents inheritance"], 0,
          "Avoiding duplication means one correction rather than the same correction in ten places."),
    ],
    exam=[
        EQ("Explain what is meant by inheritance in object oriented programming.", 3, [
            MP("A new class is based on an existing class", ["based on", "derived", "from an existing", "parent"]),
            MP("It takes on the attributes and methods of that class", ["attributes", "methods", "inherits", "takes on"]),
            MP("It can add new members or override existing ones", ["add", "override", "change", "extend", "new methods"]),
        ], "Inheritance is a relationship in which a new class, the subclass, is based on an existing class, the superclass. The subclass automatically takes on all the attributes and methods defined in the superclass, so shared behaviour only has to be written once. The subclass can then add attributes and methods of its own, and it can override any inherited method by defining its own version, which is then used in place of the parent's when called on a subclass object.",
           command="Explain"),
        EQ("Explain what polymorphism is and why it is useful, using an example.", 4, [
            MP("Objects of different classes respond to the same method call", ["same method", "different classes", "same interface", "same call"]),
            MP("Each provides its own implementation of that method", ["own version", "own implementation", "different behaviour", "overridden"]),
            MP("Gives a valid example such as a list of shapes or animals", ["shapes", "animals", "example", "loop", "list"]),
            MP("Explains that existing code does not need changing when a new class is added", ["no change", "existing code", "new class", "without modifying", "still works"]),
        ], "Polymorphism means that objects of different classes can be used through the same interface, with each one responding to a method call in its own way. For example, a list might contain Circle, Square and Triangle objects, all inheriting from a Shape class, and a loop can simply call area() on each without ever asking what type it is holding, because each class provides its own version of the method. This is useful because it removes the need for long chains of type checks. Without polymorphism, every loop that processed shapes would need an if statement for each type, and adding a new shape would mean finding and editing every one of those loops. With polymorphism, a new shape is added by writing one new class, and all the existing code continues to work unchanged.",
           command="Explain"),
        EQ("A program has an Animal class with a speak method. Write a Dog subclass that overrides speak, and explain what overriding means.", 4, [
            MP("Defines the subclass inheriting from Animal", ["class dog(animal)", "(animal)", "inherits"]),
            MP("Defines a speak method with the same name", ["def speak", "speak(self)"]),
            MP("Returns or prints a dog specific sound", ["woof", "bark", "return"]),
            MP("Explains that the subclass version replaces the parent version for objects of that class", ["replaces", "instead of", "used in place", "subclass version", "overrides"]),
        ], "class Dog(Animal):\n    def speak(self):\n        return \"Woof\"\n\nOverriding means defining a method in a subclass that has the same name as one in its parent class. When that method is called on an object of the subclass, Python uses the subclass version rather than the inherited one, so a Dog object returns Woof while another Animal subclass returns something different. The parent's version is not removed and can still be reached using super().speak() if the subclass wants to extend the original behaviour rather than replace it entirely.",
           command="Write"),
        EQ("Explain the difference between inheritance and composition, and state when each should be used.", 4, [
            MP("Inheritance expresses an is a relationship", ["is a", "kind of", "type of", "inherits"]),
            MP("Composition expresses a has a relationship, where an object contains another", ["has a", "contains", "made up of", "part of"]),
            MP("Use inheritance when the subclass genuinely is a kind of the parent", ["genuinely", "is a kind", "dog is an animal", "correct"]),
            MP("Use composition when one object simply uses or contains another", ["contains", "uses", "car has an engine", "part"]),
        ], "Inheritance expresses an is a relationship: a Dog is a kind of Animal, so making Dog a subclass of Animal makes sense and Dog inherits everything an Animal can do. Composition expresses a has a relationship, where one object holds another as an attribute: a Car has an Engine, so the Car class creates an Engine object and stores it. The test for which to use is whether the sentence with is a makes sense. A Car is not a kind of Engine, so inheriting from Engine would produce a class hierarchy that is confusing and would give Car methods that make no sense for it. Choosing the wrong one is a common source of class hierarchies that nobody can follow, so the general advice is to prefer composition unless the is a relationship is genuinely true.",
           command="Explain"),
        EQ("Name and briefly explain the four principles of object oriented programming.", 8, [
            MP("Abstraction is exposing only what is needed", ["abstraction", "exposing", "hiding complexity", "only what is needed"]),
            MP("Abstraction hides underlying complexity from the user of a class", ["complexity", "hidden", "internal", "do not need to know"]),
            MP("Encapsulation is bundling data with the methods that act on it", ["encapsulation", "bundling", "together", "data and methods"]),
            MP("Encapsulation controls access so data stays valid", ["access", "controlled", "private", "validate", "valid"]),
            MP("Inheritance is a class taking on the attributes and methods of another", ["inheritance", "takes on", "subclass", "parent"]),
            MP("Inheritance avoids duplication because shared code is written once", ["duplication", "written once", "reuse", "shared"]),
            MP("Polymorphism is different classes responding to the same call in their own way", ["polymorphism", "same method", "different classes", "own way"]),
            MP("Polymorphism means new classes can be added without changing existing code", ["without changing", "existing code", "new class", "extensible"]),
        ], "Abstraction means exposing only what is needed to use a class while hiding the complexity behind it. Someone using a list does not need to know how it stores items in memory, only that append adds one, and a well designed class works the same way. Encapsulation means bundling an object's data together with the methods that operate on it, and controlling how that data can be accessed from outside. Because changes go through the class's own methods, it can validate them and guarantee that the object never enters an invalid state, such as a bank account with a negative balance. Inheritance means a class can be built from an existing one, automatically taking on its attributes and methods and then adding or overriding whatever it needs. This avoids duplication, because behaviour shared by many classes is written once in the parent, and a correction made there applies everywhere at once. Polymorphism means that objects of different classes can respond to the same method call, each in its own way. A loop can call update on every object in a list without knowing or caring what type each one is, and because of this a new type can be added simply by writing a new class, with no change at all to the code that already uses them. Together these four principles produce code that is easier to reuse, easier to extend and far easier to keep correct as it grows.",
           command="Name"),
    ],
)

P_TKINTER = Topic(
    slug="tkinter-gui-programming",
    title="Building Interfaces with tkinter",
    spec="5.1",
    icon="i-web",
    minutes=32,
    blurb="Windows, widgets, layout and events. Turning a console program into something with buttons that a real person would use.",
    fact="tkinter has been part of Python's standard library since 1994, which means it is already installed on almost every computer running Python. No pip install, no dependencies, nothing to go wrong on the school network.",
    sections=[
        Section("Your first window", """
```python
import tkinter as tk

window = tk.Tk()
window.title("My First App")
window.geometry("400x300")

label = tk.Label(window, text="Hello, world!", font=("Arial", 16))
label.pack(pady=20)

window.mainloop()
```

### What each line does

- `tk.Tk()` creates the main window
- `title()` sets the text in the title bar
- `geometry("400x300")` sets the width and height in pixels
- `tk.Label(window, ...)` creates a label **inside** that window
- `pack()` places the widget on screen. **Nothing appears until it is placed.**
- `mainloop()` starts the event loop, which waits for the user to do something. Everything after it runs only when the window closes.

!warn Creating a widget is not enough :: A widget you never `pack`, `grid` or `place` will not appear. This is the single most common beginner problem with tkinter.
"""),
        Section("Widgets and layout", """
### The widgets you will use most

```python
tk.Label(window, text="Some text")
tk.Button(window, text="Click me", command=do_something)
tk.Entry(window, width=30)                 # single line text box
tk.Text(window, height=5, width=40)        # multi line
tk.Checkbutton(window, text="Agree", variable=agreed)
tk.Radiobutton(window, text="Red", variable=colour, value="red")
tk.Listbox(window)
tk.Scale(window, from_=0, to=100, orient="horizontal")
tk.Frame(window)                           # a container for grouping
```

### Three layout managers

**pack** stacks widgets in order.

```python
label.pack(side="top", pady=10)
button.pack(side="bottom", fill="x")
```

**grid** arranges widgets in rows and columns. This is the one to use for forms.

```python
tk.Label(window, text="Name:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
name_entry = tk.Entry(window)
name_entry.grid(row=0, column=1, padx=5, pady=5)

tk.Label(window, text="Age:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
age_entry = tk.Entry(window)
age_entry.grid(row=1, column=1, padx=5, pady=5)

tk.Button(window, text="Submit").grid(row=2, column=0, columnspan=2, pady=10)
```

**place** positions by exact pixel coordinates. Avoid it, because the layout breaks the moment the window is resized.

!key Never mix pack and grid in the same container :: tkinter will freeze with no error message. Use one or the other per frame.

### Reading and writing widget values

```python
name = name_entry.get()          # read an Entry
name_entry.delete(0, tk.END)     # clear it
name_entry.insert(0, "default")  # put text in

label.config(text="Updated!")    # change a Label after creation
```

### Variables that update automatically

```python
score = tk.IntVar(value=0)
message = tk.StringVar(value="Ready")

tk.Label(window, textvariable=message).pack()

def add_point():
    score.set(score.get() + 1)
    message.set(f"Score: {score.get()}")
```

Changing the variable updates every widget bound to it, with no manual refresh.
"""),
        Section("Events and a complete app", """
### Buttons

```python
def on_click():
    print("Clicked")

tk.Button(window, text="Go", command=on_click).pack()
```

Note there are **no brackets** after `on_click`. You are passing the function itself, not calling it.

### Passing arguments

```python
tk.Button(window, text="Add 5", command=lambda: add_score(5)).pack()
```

### Binding other events

```python
window.bind("<Return>", lambda event: submit())
window.bind("<Key>", on_keypress)
canvas.bind("<Button-1>", on_left_click)
```

### Message boxes

```python
from tkinter import messagebox

messagebox.showinfo("Saved", "Your work has been saved.")
messagebox.showerror("Error", "That is not a valid number.")
if messagebox.askyesno("Confirm", "Delete this record?"):
    delete_record()
```

### A complete application

```python
import tkinter as tk
from tkinter import messagebox


class MarkBookApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mark Book")
        self.root.geometry("420x420")
        self.marks = []
        self.build_interface()

    def build_interface(self):
        form = tk.Frame(self.root, padx=12, pady=12)
        form.pack(fill="x")

        tk.Label(form, text="Student name:").grid(row=0, column=0, sticky="e", pady=4)
        self.name_entry = tk.Entry(form, width=22)
        self.name_entry.grid(row=0, column=1, pady=4)

        tk.Label(form, text="Mark out of 100:").grid(row=1, column=0, sticky="e", pady=4)
        self.mark_entry = tk.Entry(form, width=22)
        self.mark_entry.grid(row=1, column=1, pady=4)

        tk.Button(form, text="Add", width=12, command=self.add_mark)\\
            .grid(row=2, column=0, columnspan=2, pady=8)

        self.listbox = tk.Listbox(self.root, height=10)
        self.listbox.pack(fill="both", expand=True, padx=12)

        self.summary = tk.StringVar(value="No marks yet")
        tk.Label(self.root, textvariable=self.summary, pady=8).pack()

        self.root.bind("<Return>", lambda event: self.add_mark())

    def add_mark(self):
        name = self.name_entry.get().strip()
        entry = self.mark_entry.get().strip()

        if name == "":
            messagebox.showerror("Missing name", "Please enter a student name.")
            return
        if not entry.isdigit() or not 0 <= int(entry) <= 100:
            messagebox.showerror("Invalid mark", "Enter a whole number between 0 and 100.")
            return

        mark = int(entry)
        self.marks.append(mark)
        self.listbox.insert(tk.END, f"{name:<20} {mark}")

        average = sum(self.marks) / len(self.marks)
        self.summary.set(f"{len(self.marks)} marks, average {average:.1f}, highest {max(self.marks)}")

        self.name_entry.delete(0, tk.END)
        self.mark_entry.delete(0, tk.END)
        self.name_entry.focus()


root = tk.Tk()
app = MarkBookApp(root)
root.mainloop()
```

This program validates every input, gives clear error messages, updates its summary automatically and supports the enter key. That is the standard to aim for.
"""),
    ],
    keyterms=[
        ("tkinter", "Python's standard library for building graphical user interfaces."),
        ("Widget", "A single interface component such as a label, button or text box."),
        ("Window", "The top level container created with Tk(), holding all the widgets."),
        ("mainloop", "The event loop that waits for user actions and keeps the window open."),
        ("pack", "A layout manager that stacks widgets in the order they are added."),
        ("grid", "A layout manager that places widgets in rows and columns."),
        ("Event", "Something the user does, such as a click or a key press, which the program responds to."),
        ("command", "The Button option naming the function to call when the button is pressed."),
        ("StringVar", "A tkinter variable that automatically updates any widget bound to it."),
    ],
    grade="""
+ Use grid for anything form shaped, and never mix grid and pack in one container
+ Pass the function name without brackets to command, and use lambda when arguments are needed
+ Validate every Entry before using its value, since get() always returns a string
+ Use StringVar and IntVar so labels update themselves
+ Structure a larger app as a class, so widgets are attributes rather than globals
""",
    mistakes=[
        "Creating a widget but never calling pack or grid, so it never appears.",
        "Writing command=on_click() with brackets, which calls the function immediately instead of on click.",
        "Mixing pack and grid in the same container, which freezes the program with no error.",
        "Forgetting that Entry.get() returns a string, then comparing it with a number.",
        "Putting code after mainloop() and wondering why it never runs.",
    ],
    quiz=[
        Q("What does `window.mainloop()` do?",
          ["Starts the event loop and keeps the window open waiting for user actions",
           "Creates the window", "Closes the window", "Draws all the widgets"], 0,
          "Nothing after mainloop runs until the window is closed, because it blocks there waiting for events."),
        Q("Why might a widget not appear on screen?",
          ["It was created but never packed, gridded or placed",
           "The window is too small", "It needs a colour set", "Widgets appear automatically"], 0,
          "Creating a widget only builds it. A layout manager is what actually puts it on screen."),
        Q("What is wrong with `tk.Button(window, command=save())`?",
          ["The brackets call save immediately instead of when the button is clicked",
           "command is not a valid option", "Buttons cannot call functions", "Nothing is wrong"], 0,
          "Pass the function itself without brackets, or use a lambda if arguments are needed."),
        Q("Which layout manager is best for a form with labels and text boxes?",
          ["grid", "pack", "place", "mainloop"], 0,
          "grid arranges widgets in rows and columns, which is exactly the shape of a form."),
        Q("What happens if you use both pack and grid in the same container?",
          ["The program freezes with no error message", "The last one used wins",
           "An exception is raised immediately", "Both work fine"], 0,
          "This is a notoriously confusing bug because there is no error to tell you what went wrong."),
        Q("What does `entry.get()` return?", ["A string", "An integer", "A float", "A widget"], 0,
          "Just like input(), it always returns text, so convert it before doing arithmetic."),
        Q("What is a StringVar used for?",
          ["Automatically updating any widget bound to it when its value changes",
           "Storing a string permanently", "Converting text to numbers", "Naming a window"], 0,
          "Setting the variable refreshes every widget using it, with no manual update needed."),
        Q("How do you pass an argument to a button's command function?",
          ["Use a lambda, for example command=lambda: add(5)",
           "command=add(5)", "command=add, args=5", "It is not possible"], 0,
          "A lambda creates a small function that is called later with the argument already fixed."),
        Q("What does `label.config(text=\"New\")` do?",
          ["Changes the label's text after it has been created",
           "Creates a new label", "Deletes the label", "Moves the label"], 0,
          "config is how you change any widget option after the widget exists."),
        Q("Which line creates the main application window?",
          ["window = tk.Tk()", "window = tk.Window()", "window = tk.Frame()", "window = tk.Label()"], 0,
          "Tk() creates the top level window. Frame is a container inside it."),
    ],
    exam=[
        EQ("Explain the purpose of the mainloop method in a tkinter program.", 3, [
            MP("It starts the event loop", ["event loop", "loop", "starts"]),
            MP("It keeps the window open and waits for user actions such as clicks and key presses", ["waits", "keeps open", "clicks", "key presses", "user actions", "responds"]),
            MP("Code after it does not run until the window closes", ["after", "does not run", "until closed", "blocks"]),
        ], "The mainloop method starts tkinter's event loop, which is what makes the interface interactive. It keeps the window on screen and continuously waits for events such as button clicks, key presses and mouse movements, dispatching each one to whatever function has been bound to it. Because the program stays inside mainloop until the window is closed, any code written after the mainloop call will not run while the application is open, which is a common source of confusion for beginners.",
           command="Explain"),
        EQ("A student creates a label with `label = tk.Label(window, text=\"Hello\")` but nothing appears when the program runs. Explain why and give the correction.", 2, [
            MP("The widget has not been added to the window with a layout manager", ["not packed", "layout", "pack", "grid", "not placed", "not added"]),
            MP("Add label.pack() or label.grid() to display it", ["pack()", "grid()", "place()"]),
        ], "Creating a widget builds it in memory but does not put it on screen. A layout manager must be called to add it to the window, so the student needs to add a line such as label.pack() or label.grid(row=0, column=0) after creating the label. Without this the label exists but is never displayed.",
           command="Explain"),
        EQ("Explain the difference between the pack and grid layout managers, and state when each is most suitable.", 4, [
            MP("pack stacks widgets in the order they are added", ["stacks", "order", "one after", "top to bottom"]),
            MP("grid places widgets in rows and columns", ["rows", "columns", "grid", "table"]),
            MP("pack suits simple stacked layouts", ["simple", "stacked", "vertical", "one column", "quick"]),
            MP("grid suits forms where labels and inputs must line up", ["form", "labels", "line up", "aligned", "table", "entries"]),
        ], "The pack layout manager stacks widgets one after another in the order they are added, using a side such as top, bottom, left or right. It is quick and suits simple layouts where widgets sit in a single column or row, such as a title, a list and a status bar down the window. The grid layout manager places widgets in numbered rows and columns like a table, which makes it far better for forms where a column of labels must line up neatly against a column of entry boxes. Grid also allows a widget to span several columns and to be aligned within its cell. The two managers must never be used within the same container, because tkinter will hang without producing an error message.",
           command="Explain"),
        EQ("Write a tkinter program that displays a text box and a button, and when the button is clicked shows the entered text in a label.", 6, [
            MP("Imports tkinter and creates the main window", ["import tkinter", "tk.Tk()"]),
            MP("Creates an Entry widget and displays it", ["tk.Entry", "entry", "pack", "grid"]),
            MP("Creates a Label to show the result", ["tk.Label", "label"]),
            MP("Defines a function that reads the entry", ["def", "get()", "function"]),
            MP("Updates the label using config or a StringVar", ["config", "stringvar", "set("]),
            MP("Attaches the function to the button with command and starts mainloop", ["command=", "mainloop"]),
        ], "import tkinter as tk\n\ndef show_text():\n    result.config(text=\"You typed: \" + entry.get())\n\nwindow = tk.Tk()\nwindow.title(\"Echo\")\n\nentry = tk.Entry(window, width=30)\nentry.pack(pady=10)\n\ntk.Button(window, text=\"Show\", command=show_text).pack()\n\nresult = tk.Label(window, text=\"\")\nresult.pack(pady=10)\n\nwindow.mainloop()\n\nThe function is passed to command without brackets, so it is called when the button is clicked rather than immediately when the program starts. The function reads the current contents of the entry with get and updates the label using config. Every widget is packed, otherwise none of them would appear.",
           command="Write"),
        EQ("Explain why input taken from a tkinter Entry widget should be validated before it is used.", 3, [
            MP("Entry.get() always returns a string, whatever the user typed", ["string", "text", "always returns"]),
            MP("The user may type letters or leave it blank when a number is expected", ["letters", "blank", "empty", "wrong type", "anything"]),
            MP("Without validation the program may crash or produce incorrect results", ["crash", "error", "incorrect", "fails", "wrong"]),
        ], "The get method of an Entry widget always returns a string, no matter what the user typed, so any value intended as a number must be converted before it can be used in a calculation. Users can type anything at all into an entry box, including letters, symbols or nothing, so if the program calls int on the contents without checking it first, a ValueError will be raised and the application will crash. Validating the input, for example by checking isdigit and then checking the value falls within an acceptable range, allows the program to display a clear message asking the user to correct the entry instead, which is what makes the application robust.",
           command="Explain"),
    ],
)

P_PYGAME = Topic(
    slug="pygame-game-programming",
    title="Making Games with pygame",
    spec="5.2",
    icon="i-play",
    minutes=34,
    blurb="The game loop, drawing, movement, keyboard input, collision detection and sprites, ending with a complete playable game.",
    fact="Every game ever made runs the same three step loop thousands of times a second: handle input, update the world, draw the world. Once you have seen it, you cannot unsee it.",
    sections=[
        Section("The game loop", """
```python
import pygame

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("My Game")
clock = pygame.time.Clock()

TEAL = (3, 150, 157)
LILAC = (202, 171, 213)
DEEP = (3, 92, 88)

running = True
while running:
    # 1. HANDLE EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 2. UPDATE
    # game logic goes here

    # 3. DRAW
    screen.fill(DEEP)
    pygame.draw.circle(screen, LILAC, (400, 300), 40)
    pygame.display.flip()

    clock.tick(60)      # cap at 60 frames per second

pygame.quit()
```

### Every game does these three things, in this order

1. **Handle events.** What did the player do? Keys, mouse, closing the window.
2. **Update.** Move everything, check collisions, update the score, apply the rules.
3. **Draw.** Clear the screen, draw everything in its new position, show it.

!key Why you must clear the screen every frame :: If you do not call `screen.fill()`, everything from the previous frame is still there, so a moving object leaves a smear behind it. Clear, draw, show, every single frame.

### Coordinates

Pygame's origin (0, 0) is the **top left** corner. x increases to the right and **y increases downwards**, which is the opposite of maths graphs. Moving something down means increasing y.
"""),
        Section("Drawing and movement", """
### Shapes

```python
pygame.draw.rect(screen, TEAL, (x, y, width, height))
pygame.draw.rect(screen, TEAL, (x, y, w, h), 3)          # outline, 3 pixels
pygame.draw.circle(screen, LILAC, (cx, cy), radius)
pygame.draw.line(screen, TEAL, (x1, y1), (x2, y2), 2)
pygame.draw.polygon(screen, LILAC, [(0, 0), (50, 0), (25, 40)])
```

### Text

```python
font = pygame.font.Font(None, 36)
text = font.render(f"Score: {score}", True, (255, 255, 255))
screen.blit(text, (10, 10))
```

### Images

```python
player_image = pygame.image.load("player.png").convert_alpha()
player_image = pygame.transform.scale(player_image, (48, 48))
screen.blit(player_image, (x, y))
```

### Keyboard input, two ways

**Continuous**, for movement, checked every frame:

```python
keys = pygame.key.get_pressed()
if keys[pygame.K_LEFT]:
    player_x -= speed
if keys[pygame.K_RIGHT]:
    player_x += speed
if keys[pygame.K_UP]:
    player_y -= speed
if keys[pygame.K_DOWN]:
    player_y += speed
```

**Single press**, for actions that should happen once:

```python
for event in pygame.event.get():
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_SPACE:
            fire_bullet()
```

!warn Use the right one :: If firing is handled with `get_pressed()`, holding the key fires sixty bullets a second. If movement is handled with `KEYDOWN`, the player moves one pixel per press.

### Keeping things on screen

```python
player_x = max(0, min(WIDTH - player_width, player_x))
player_y = max(0, min(HEIGHT - player_height, player_y))
```
"""),
        Section("Rects, collisions and sprites", """
### Rect, the most useful object in pygame

```python
player = pygame.Rect(100, 100, 40, 40)      # x, y, width, height

player.x += 5
player.centerx = WIDTH // 2
player.bottom = HEIGHT

pygame.draw.rect(screen, TEAL, player)
```

Rects have `left`, `right`, `top`, `bottom`, `centerx`, `centery`, `center`, `size` and more, and setting any of them moves the rectangle sensibly.

### Collision detection

```python
if player.colliderect(enemy):
    lives -= 1

if player.collidepoint(mouse_x, mouse_y):
    print("Clicked the player")

hit_index = player.collidelist(coin_rects)
if hit_index != -1:
    score += 10
    coin_rects.pop(hit_index)
```

### Sprites

For anything beyond a few objects, use pygame's sprite system.

```python
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 40))
        self.image.fill((3, 150, 157))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 5

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x))


class Coin(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.circle(self.image, (202, 171, 213), (10, 10), 10)
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self, keys):
        self.rect.y += 3
        if self.rect.top > HEIGHT:
            self.kill()


all_sprites = pygame.sprite.Group()
coins = pygame.sprite.Group()

player = Player(380, 540)
all_sprites.add(player)

# in the loop
all_sprites.update(keys)
collected = pygame.sprite.spritecollide(player, coins, dokill=True)
score += len(collected) * 10
all_sprites.draw(screen)
```

`Group.update()` calls `update()` on every sprite, and `Group.draw()` draws them all. This is polymorphism doing real work.
"""),
        Section("A complete game", """
```python
import pygame
import random

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Catcher")
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 72)

DEEP = (3, 92, 88)
TEAL = (3, 150, 157)
LILAC = (202, 171, 213)
AQUA = (107, 196, 202)
WHITE = (244, 241, 248)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((90, 18))
        self.image.fill(AQUA)
        self.rect = self.image.get_rect(midbottom=(WIDTH // 2, HEIGHT - 20))
        self.speed = 8

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        self.rect.x = max(0, min(WIDTH - self.rect.width, self.rect.x))


class Falling(pygame.sprite.Sprite):
    def __init__(self, good=True):
        super().__init__()
        self.good = good
        size = 22 if good else 26
        self.image = pygame.Surface((size, size), pygame.SRCALPHA)
        colour = LILAC if good else (163, 48, 73)
        pygame.draw.circle(self.image, colour, (size // 2, size // 2), size // 2)
        self.rect = self.image.get_rect(topleft=(random.randint(0, WIDTH - size), -size))
        self.speed = random.randint(3, 7)

    def update(self, keys):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()


def draw_text(text, font_obj, colour, y):
    surface = font_obj.render(text, True, colour)
    screen.blit(surface, surface.get_rect(center=(WIDTH // 2, y)))


def run_game():
    player = Player()
    all_sprites = pygame.sprite.Group(player)
    falling = pygame.sprite.Group()

    score = 0
    lives = 3
    spawn_timer = 0
    running = True
    game_over = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False
                if game_over and event.key == pygame.K_RETURN:
                    return True

        keys = pygame.key.get_pressed()

        if not game_over:
            spawn_timer += 1
            if spawn_timer >= 30:
                spawn_timer = 0
                item = Falling(good=random.random() > 0.25)
                falling.add(item)
                all_sprites.add(item)

            all_sprites.update(keys)

            for item in pygame.sprite.spritecollide(player, falling, dokill=True):
                if item.good:
                    score += 10
                else:
                    lives -= 1
                    if lives <= 0:
                        game_over = True

        screen.fill(DEEP)
        all_sprites.draw(screen)

        screen.blit(font.render(f"Score: {score}", True, WHITE), (14, 12))
        screen.blit(font.render(f"Lives: {lives}", True, WHITE), (WIDTH - 130, 12))

        if game_over:
            draw_text("Game Over", big_font, LILAC, HEIGHT // 2 - 30)
            draw_text(f"Final score: {score}", font, WHITE, HEIGHT // 2 + 30)
            draw_text("Enter to play again, Escape to quit", font, AQUA, HEIGHT // 2 + 70)

        pygame.display.flip()
        clock.tick(60)

    return False


play_again = True
while play_again:
    play_again = run_game()

pygame.quit()
```

### What to notice

- **One class per kind of thing**, each with its own `update`
- **Groups** handle updating and drawing everything, whatever it is
- **`dokill=True`** removes the caught item automatically
- **Off screen sprites call `kill()`**, so they do not accumulate forever and slow the game down
- The **game over state** stays inside the same loop rather than needing a separate one
- `clock.tick(60)` caps the frame rate, so the game runs at the same speed on every machine
"""),
    ],
    keyterms=[
        ("Game loop", "The loop that repeatedly handles events, updates the game state and draws the frame."),
        ("Surface", "An image in memory that can be drawn onto and then drawn onto the screen."),
        ("blit", "Copying one surface onto another, which is how images and text are drawn."),
        ("Rect", "A rectangle object holding position and size, used for placement and collision detection."),
        ("Sprite", "An object in a game with an image and a rect, usually with its own update method."),
        ("Group", "A collection of sprites that can be updated and drawn together."),
        ("colliderect", "A Rect method that returns True when two rectangles overlap."),
        ("Frame rate", "How many times per second the game loop runs, capped with clock.tick."),
        ("Event queue", "The list of things the player has done since the last frame, read with pygame.event.get()."),
    ],
    grade="""
+ Always structure the loop as events, then update, then draw, in that order
+ Clear the screen at the start of every draw phase or you get smearing
+ Use get_pressed for continuous movement and KEYDOWN for one off actions
+ Remove sprites that leave the screen with kill(), or the game slows down over time
+ Cap the frame rate with clock.tick so the game runs the same speed on any machine
+ Put each kind of object in its own class so a group can update everything polymorphically
""",
    mistakes=[
        "Forgetting screen.fill(), so moving objects leave trails behind them.",
        "Forgetting pygame.display.flip(), so nothing ever appears.",
        "Using KEYDOWN for movement, so the player moves one pixel per key press.",
        "Never removing off screen sprites, so the game gradually slows to a crawl.",
        "Forgetting that y increases downwards, so everything moves the wrong way vertically.",
        "Leaving out clock.tick, so the game runs at a completely different speed on a faster computer.",
    ],
    quiz=[
        Q("What are the three stages of a game loop, in order?",
          ["Handle events, update, draw", "Draw, update, handle events",
           "Update, draw, handle events", "Handle events, draw, update"], 0,
          "Input first so the update uses it, then draw the result of that update."),
        Q("Why must `screen.fill()` be called each frame?",
          ["Otherwise the previous frame remains and moving objects leave trails",
           "It makes the game run faster", "It creates the window", "It reads the keyboard"], 0,
          "The screen is not cleared automatically, so every frame is drawn on top of the last."),
        Q("In pygame, moving an object down the screen means:",
          ["Increasing its y coordinate", "Decreasing its y coordinate",
           "Increasing its x coordinate", "Decreasing its x coordinate"], 0,
          "The origin is the top left and y increases downwards, unlike a maths graph."),
        Q("Which should be used for continuous player movement?",
          ["pygame.key.get_pressed()", "The KEYDOWN event", "The KEYUP event", "colliderect"], 0,
          "get_pressed reports which keys are held down right now, checked every frame."),
        Q("What does `player.colliderect(enemy)` return?",
          ["True if the two rectangles overlap", "The distance between them",
           "The overlapping area", "The enemy's position"], 0,
          "It is the simplest and fastest form of collision detection in pygame."),
        Q("What does `clock.tick(60)` do?",
          ["Limits the loop to 60 iterations per second",
           "Runs the loop 60 times then stops", "Waits 60 seconds", "Sets the score to 60"], 0,
          "Without it the loop runs as fast as the machine allows, so the game speed varies between computers."),
        Q("What does `pygame.display.flip()` do?",
          ["Shows everything that has been drawn since the last frame",
           "Clears the screen", "Reverses the image", "Ends the game"], 0,
          "Drawing happens off screen, and flip makes the finished frame visible."),
        Q("Why should sprites that move off screen be removed with kill()?",
          ["Otherwise they accumulate and gradually slow the game down",
           "They would reappear on the other side", "It is required by pygame", "It saves disk space"], 0,
          "Every sprite still in a group is updated and drawn every frame, whether or not it is visible."),
        Q("What does `all_sprites.update(keys)` do?",
          ["Calls the update method on every sprite in the group",
           "Draws every sprite", "Removes every sprite", "Creates new sprites"], 0,
          "Each sprite runs its own version of update, which is polymorphism in practice."),
        Q("Which should be used for firing a single shot when space is pressed?",
          ["The KEYDOWN event", "pygame.key.get_pressed()", "colliderect", "clock.tick"], 0,
          "KEYDOWN fires once per press. get_pressed would fire on every frame the key is held."),
    ],
    exam=[
        EQ("Describe the three stages of a game loop.", 3, [
            MP("Handle events such as key presses and closing the window", ["events", "input", "key", "mouse", "quit"]),
            MP("Update the game state, moving objects and checking collisions", ["update", "move", "collision", "logic", "score"]),
            MP("Draw everything to the screen and display the frame", ["draw", "render", "display", "flip", "blit"]),
        ], "The first stage handles events, reading everything the player has done since the last frame, such as key presses, mouse clicks and the window being closed. The second stage updates the game state: objects are moved according to input and their own behaviour, collisions are checked, and things such as the score and the number of lives are adjusted. The third stage draws the frame, clearing the screen and then drawing every object in its new position before calling display.flip to make the completed frame visible. These three stages repeat, typically sixty times a second.",
           command="Describe"),
        EQ("Explain why the screen must be cleared at the start of each frame in a pygame program.", 2, [
            MP("Pygame does not clear the screen automatically between frames", ["not cleared", "automatically", "remains", "stays"]),
            MP("Without clearing, previous frames remain visible so moving objects leave trails", ["trails", "smear", "previous", "left behind", "streak"]),
        ], "Pygame does not clear the display between frames, so whatever was drawn last time is still there when the next frame is drawn on top of it. If the screen is not cleared with screen.fill at the start of the drawing stage, an object that has moved will be drawn in its new position while its old position is still visible, so it leaves a continuous trail across the screen rather than appearing to move.",
           command="Explain"),
        EQ("Explain the difference between using pygame.key.get_pressed() and the KEYDOWN event, and state when each should be used.", 4, [
            MP("get_pressed reports which keys are currently held down", ["held", "currently", "down now", "every frame"]),
            MP("It is checked every frame so the action repeats while the key is held", ["every frame", "repeats", "continuous", "while held"]),
            MP("KEYDOWN fires once at the moment a key is pressed", ["once", "moment", "single", "when pressed"]),
            MP("Use get_pressed for movement and KEYDOWN for one off actions such as firing or jumping", ["movement", "firing", "jumping", "one off", "single action", "menu"]),
        ], "The get_pressed function returns the current state of every key, so checking it inside the game loop tells you which keys are being held down at that moment, and any action taken repeats on every frame the key remains down. The KEYDOWN event, by contrast, appears in the event queue once at the instant a key is pressed and does not repeat while it is held. Movement should use get_pressed, so that holding the left arrow moves the player smoothly and continuously. One off actions such as firing a shot, jumping or selecting a menu item should use KEYDOWN, because using get_pressed for firing would produce sixty shots a second while the key was held.",
           command="Explain"),
        EQ("Write pygame code for a sprite class representing a coin that falls down the screen and removes itself when it goes off the bottom.", 5, [
            MP("Defines a class inheriting from pygame.sprite.Sprite", ["sprite.sprite", "class", "inherits"]),
            MP("Calls super().__init__() in the constructor", ["super()", "__init__"]),
            MP("Creates an image and a rect for the sprite", ["self.image", "self.rect", "get_rect"]),
            MP("Defines update to increase the y coordinate", ["def update", "rect.y +=", "moves down"]),
            MP("Removes the sprite with kill() when it passes the bottom of the screen", ["kill()", "top > height", "off screen"]),
        ], "class Coin(pygame.sprite.Sprite):\n    def __init__(self, x, y):\n        super().__init__()\n        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)\n        pygame.draw.circle(self.image, (202, 171, 213), (10, 10), 10)\n        self.rect = self.image.get_rect(topleft=(x, y))\n        self.speed = 4\n\n    def update(self):\n        self.rect.y += self.speed\n        if self.rect.top > HEIGHT:\n            self.kill()\n\nThe class inherits from pygame.sprite.Sprite so it can be added to a group, and super().__init__() must be called or the sprite machinery will not be set up. Every sprite needs an image and a rect, because groups use those to draw and position it. The update method increases y each frame, since y increases downwards in pygame, and calls kill once the top of the coin has passed the bottom of the screen, which removes it from every group it belongs to so it is no longer updated or drawn.",
           command="Write"),
        EQ("Explain why clock.tick(60) is used in a pygame game loop and what would happen without it.", 3, [
            MP("It limits the loop to a maximum of 60 iterations per second", ["limits", "caps", "60 times", "frames per second", "maximum"]),
            MP("This makes the game run at the same speed on different computers", ["same speed", "consistent", "different computers", "hardware", "fair"]),
            MP("Without it the loop runs as fast as possible, so the game is far too fast on a powerful machine", ["as fast as possible", "too fast", "unplayable", "varies", "faster machine"]),
        ], "The tick method limits the game loop to a maximum number of iterations per second, in this case sixty, by pausing briefly at the end of each pass if the frame was completed early. This matters because the amount an object moves per frame is fixed in the code, so the speed things appear to travel depends entirely on how many frames happen each second. Without the cap, the loop would run as fast as the hardware allows, which might be several hundred frames a second on a modern machine, and the game would be completely unplayable while running at a totally different speed on a slower computer. Capping the frame rate makes the game behave identically regardless of the hardware it is running on.",
           command="Explain"),
    ],
)

# ================================================================== COURSE

COURSE = Course(
    slug="python",
    title="Python from Scratch",
    short="Python",
    stage="All",
    board="",
    code="",
    goal="Fluency",
    icon="i-python",
    accent="var(--aqua)",
    blurb="A complete Python course, from your very first line of code through to object oriented programming, desktop applications with tkinter and games with pygame. Every example runs, and every topic has a quiz and written questions.",
    intro="",
    journey=[
        ("Type it out, do not copy and paste",
         "Typing code out is slow and that is exactly the point. You notice the colons, the indentation and the brackets, and your fingers learn the patterns. Copying teaches you nothing.", ""),
        ("Break it deliberately",
         "Once an example works, change something and predict what will happen before you run it. Being wrong is the fastest way to find out what you actually understood.", ""),
        ("Build something you want to exist",
         "A quiz about your favourite subject, a tool that does your maths homework, a game you would actually play. Motivation matters far more than the size of the project.", ""),
        ("Learn to read errors, not fear them",
         "Read the last line first, then the line number. Nine errors in ten are a missing bracket, a wrong type or a name spelled differently from where you defined it.", ""),
        ("Get through OOP properly",
         "Classes are the boundary between writing scripts and writing programs. Give this section the time it needs, because everything at A Level and beyond assumes it.", ""),
        ("Finish something",
         "A small finished project teaches you more than five abandoned big ones, because the last ten per cent is where all the real problems live.", ""),
    ],
    units=[
        Unit("foundations", "Foundations",
             "Output, variables, types, input, operators and making decisions. The bit everything else is built on.",
             [P_FIRST, P_VARS, P_INPUT], icon="i-play", term="Beginner"),
        Unit("core", "Core Programming",
             "Loops, lists, strings and your own functions. After this unit you can write real programs.",
             [P_LOOPS, P_LISTS, P_FUNCTIONS], icon="i-repeat", term="Beginner to intermediate"),
        Unit("real-programs", "Real Programs",
             "Dictionaries for structured data, files so your program remembers things, and error handling so it does not crash.",
             [P_DATA], icon="i-database", term="Intermediate"),
        Unit("oop", "Object Oriented Programming",
             "Classes, objects, encapsulation, inheritance and polymorphism. The step from scripts to software.",
             [P_OOP1, P_OOP2], icon="i-cube", term="Intermediate to advanced"),
        Unit("applications", "Applications and Games",
             "Desktop programs with tkinter and games with pygame, each ending in a complete working project.",
             [P_TKINTER, P_PYGAME], icon="i-web", term="Advanced"),
    ],
)
