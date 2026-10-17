"""GCSE Python: validation, authentication, maintainable code and testing."""
from mskbuild.models import Topic, Section, Q, EQ, MP

INPUTS = {}
EXPECT = {}

TOPIC = Topic(
    slug="validation-authentication-and-testing",
    title="Validation, Authentication and Testing",
    spec="GCSE 4",
    icon="i-shield",
    minutes=40,
    blurb="Writing programs that cope with the wrong input, prove who the user is, can be maintained by somebody else, and are tested with the right data. This is the whole of producing robust programs.",
    fact="The word bug has been used for a technical fault since at least the 1870s, long before computers, when Thomas Edison used it in letters about his inventions. The famous 1947 moth in a Harvard computer was a joke on a word already in use.",
    sections=[
        Section("Validation and sanitisation", r"""
**Defensive design** means writing a program that carries on behaving sensibly when people do the wrong thing, and they will. The first line of defence is **input validation**: checking that data is acceptable before the program uses it.

!key Validation checks that data is sensible, not that it is true :: A validation check will accept an age of 40 for a ten year old, because 40 is a sensible age. Nothing a program can check by itself catches that. **Verification** is about checking data was entered the way the person meant, for example by typing a password twice.

| Check | Question it asks | Example |
| Range | Is it between a lowest and a highest value? | Age from 0 to 120 |
| Length | Is it a sensible number of characters? | Password at least 8 characters |
| Type | Is it the right data type? | Quantity is a whole number |
| Presence | Was anything entered at all? | Name must not be empty |
| Format | Does it follow a pattern? | A date is dd/mm/yyyy |
| Lookup | Is it one of an allowed list? | Size is S, M or L |

Each check is a small function that returns `True` or `False`:

```python
def in_range(n, low, high):
    return low <= n <= high

def right_length(text, low, high):
    return low <= len(text) <= high

def is_whole_number(text):
    return text.isdigit()

def is_present(text):
    return text.strip() != ""

def in_list(value, allowed):
    return value in allowed

print(in_range(15, 0, 120), right_length("abc", 8, 20))      # True False
print(is_whole_number("42"), is_whole_number("4.2"))         # True False
print(is_present("   "), in_list("M", ["S", "M", "L"]))      # False True
```

### A validation loop

Keep asking until the answer is acceptable. The type check has to come **before** the range check, because `int("abc")` would crash the program before the range was ever looked at.

```python
feed = iter(["abc", "-5", "200", "15"])      # stands in for the keyboard

age = -1
while age < 0 or age > 120:
    text = next(feed)                        # in the exam: input("Age: ")
    if text.isdigit():
        age = int(text)
        if age < 0 or age > 120:
            print("Age must be between 0 and 120")
    else:
        print("Please type a whole number")
print("Accepted:", age)
```

Run it and follow the four attempts. `"abc"` fails the type check. `"-5"` fails it too, because a minus sign is not a digit. `"200"` is a whole number but fails the range check. `"15"` passes both.

### Sanitisation

**Sanitising** input means cleaning it so it is safe and consistent before it is used. Remove stray spaces, fix the case, and strip out anything the program should never receive.

```python
raw = "   aShA  kETHIRI "
clean = " ".join(raw.split()).title()
print(repr(clean))               # 'Asha Kethiri'
```

The most important reason to sanitise is that an attacker can type program code into a text box. A name field that is pasted into a database query can become an instruction, which is called **SQL injection**. The SQL topic shows the proper fix, which is never to build a query out of typed text at all.
"""),
        Section("Authentication", r"""
**Authentication** proves that a user is who they say they are. Validation asks "is this input acceptable?" and authentication asks "is this person allowed in?"

| Method | How it works | Weakness |
| Password | A secret only the user should know | Guessed, shared or reused |
| Biometrics | A fingerprint or face is checked | Cannot be changed if copied |
| Two factor | A password plus a code sent to a phone | Needs the second device |
| Lockout | The account locks after a few wrong tries | Can be used to lock out the real user |

A login with limited attempts, using a dictionary of users:

```python
users = {"asha": "Tr1angle!", "ben": "kEy2024#"}

def check_login(username, password):
    return username in users and users[username] == password

attempts = [("asha", "wrong"), ("asha", "also wrong"), ("asha", "Tr1angle!")]
tries = 0
logged_in = False
while tries < 3 and not logged_in:
    username, password = attempts[tries]
    tries = tries + 1
    if check_login(username, password):
        logged_in = True
    else:
        print("Incorrect, attempt", tries, "of 3")

if logged_in:
    print("Welcome")
else:
    print("Account locked")
```

The loop stops for two different reasons, a correct login or three failures, and the `if` after it has to work out which. That is a typical shape for an exam question.

### Password rules

A strong password rule is a validation check on the password. Check one property at a time.

```python
def strong_password(password):
    has_digit = False
    has_upper = False
    for ch in password:
        if ch.isdigit():
            has_digit = True
        if ch.isupper():
            has_upper = True
    return len(password) >= 8 and has_digit and has_upper

print(strong_password("password"))      # False
print(strong_password("Tr1angle!"))     # True
```

!warn Real systems never store the password itself :: A database that holds passwords as typed is stolen in full the day it is breached. Real systems store a **hash**, a one way scrambling of the password, and compare the hash of what was typed. That is covered at A Level.
"""),
        Section("Writing code that can be maintained", r"""
Programs are read many more times than they are written, often by a different person, and often by you months later. **Maintainability** is how easily the code can be understood and changed. The exam wants these named every time:

| Technique | What it does for the reader |
| Meaningful names | `vat_rate` says what it holds, `x` does not |
| Comments | Explain why, so the reader does not have to guess |
| Indentation and white space | Shows the structure of the loops and decisions |
| Subprograms | One job per subprogram, each with a name |
| Constants | `VAT = 0.2` in one place, not `0.2` in twenty |

Both of these give the same answer:

```python
def f(a,b):
    c=a*b*0.2
    return c
x=f(50,2)
print(x)
```

```python
VAT_RATE = 0.2

def vat_on_order(unit_price, quantity):
    # VAT is charged on the whole order, not on each item
    order_total = unit_price * quantity
    return order_total * VAT_RATE

vat = vat_on_order(50, 2)
print(vat)
```

Only the second tells you what is going on.
"""),
        Section("Testing", r"""
Testing proves the program works and finds where it does not. Two kinds of testing, at two points:

- **Iterative testing** happens *during* development. Each subprogram is tested as soon as it is written, so a fault is found while only a few lines could be responsible.
- **Final testing**, also called terminal testing, happens at the end on the whole program, against the original requirements.

### Three kinds of error

| Error | What happens | Example |
| Syntax | The program will not run at all | A missing bracket or colon |
| Runtime | It starts, then crashes | Dividing by zero |
| Logic | It runs and gives the wrong answer | Writing `>` where `>=` was meant |

A logic error is the dangerous one, because nothing tells you. This function is meant to say whether somebody may vote at 18:

```python
def is_adult(age):
    return age > 18

print(is_adult(17), is_adult(30))      # False True, which looks fine
print(is_adult(18))                    # False, but an 18 year old is an adult
```

Only a test at the **boundary** finds it.

### Types of test data

Imagine a program that accepts a whole number from 1 to 10.

| Type | What it is | Test data | Expected |
| Normal | Typical and valid | `5`, `7` | Accepted |
| Boundary | At the edge of the valid range | `1`, `10` | Accepted |
| Boundary, just outside | One step beyond the edge | `0`, `11` | Rejected |
| Invalid | The right type but not allowed | `-3`, `250` | Rejected |
| Erroneous | The wrong type altogether | `"ten"`, `""`, `4.5` | Rejected |

!diagram py-test-data

!warn Boundary data means two values at each edge :: The value on the boundary, which is valid, and the value just beyond it, which is not. Most logic errors, like the `>` that should have been `>=`, hide exactly there.

### A test plan, run by the computer

A test plan has the test data, what you **expect**, what **actually** happened and a pass or fail. Python can run the plan for you, which is how professionals do it.

```python
def valid_age(text):
    if not text.isdigit():
        return False
    return 0 <= int(text) <= 120

tests = [
    ("normal", "15", True),
    ("normal", "60", True),
    ("boundary", "0", True),
    ("boundary", "120", True),
    ("boundary", "121", False),
    ("invalid", "150", False),
    ("erroneous", "abc", False),
    ("erroneous", "12.5", False),
    ("erroneous", "", False),
]

failed = 0
for kind, data, expected in tests:
    actual = valid_age(data)
    if actual == expected:
        result = "pass"
    else:
        result = "FAIL"
        failed = failed + 1
    print(kind.ljust(10), repr(data).ljust(7), expected, actual, result)
print(failed, "tests failed")
```

!exam What a test table must have :: A test number, the purpose, the test data, the **expected** result and the **actual** result. Expected is worked out from the specification *before* you run anything. If you write expected after seeing the output, you are not testing, you are copying.
"""),
    ],
    keyterms=[
        ("Validation", "Checking that data entered is reasonable and allowed, such as within a range, before the program uses it."),
        ("Verification", "Checking that data has been entered as the user intended, such as typing a password twice."),
        ("Sanitisation", "Cleaning input so that it is safe and consistent, by removing unwanted characters and fixing its form."),
        ("Authentication", "Proving that a user is who they claim to be, for example with a password or a fingerprint."),
        ("Maintainability", "How easily a program can be understood, corrected and improved by somebody else."),
        ("Iterative testing", "Testing each part of a program during development, as soon as it is written."),
        ("Boundary data", "Test data on the edge of what is allowed, and the value just beyond it."),
        ("Erroneous data", "Test data of the wrong type, which the program should reject."),
        ("Logic error", "A fault that lets a program run but makes it give the wrong result."),
    ],
    grade="""
Top marks on robust program questions are for exact terms and for test data that would really find a fault.

+ Name the check: range, length, type, presence, format or lookup, and write the condition for it
+ Do the type check first, so the range check never receives data it cannot compare
+ Give boundary data as a pair at each edge: the last valid value and the first invalid one
+ State the expected result before the actual result in every test table
+ Say why, not just what: meaningful names help because another programmer must understand the code
""",
    mistakes=[
        "Saying validation checks that data is correct, rather than reasonable.",
        "Choosing only one value from the boundary, so the off by one bug is never exposed.",
        "Mixing up invalid data, which is the right type but not allowed, with erroneous data, which is the wrong type.",
        "Writing a test plan with no expected result, or one worked out after running the program.",
        "Describing maintainability as making the program faster, which it is not.",
    ],
    quiz=[
        Q("What does validation check?",
          ["That data is reasonable and allowed", "That data is true", "That the user is who they claim to be", "That the program has no bugs"], 0,
          "Validation can reject an age of 400 but it cannot tell that 40 is the wrong age for a ten year old."),
        Q("Which validation check is `len(password) >= 8`?",
          ["A length check", "A range check", "A presence check", "A lookup check"], 0,
          "It tests the number of characters, which is a length check."),
        Q("Which check makes sure something has been entered at all?",
          ["A presence check", "A range check", "A format check", "A lookup check"], 0,
          "A presence check rejects an empty value, which is different from rejecting a wrong value."),
        Q("A program accepts whole numbers from 1 to 10. Which value is boundary test data?",
          ["10", "5", "-3", "ten"], 0,
          "10 is on the edge of the valid range. 5 is normal, -3 is invalid and the word ten is erroneous."),
        Q("A program expects a whole number from 1 to 10. Which is erroneous test data?",
          ["`\"ten\"`", "`5`", "`11`", "`10`"], 0,
          "Erroneous data is the wrong type. 11 is the right type but outside the range, so it is invalid."),
        Q("What is the difference between validation and verification?",
          ["Verification checks data was entered as intended, validation checks it is reasonable",
           "Validation checks data was entered as intended, verification checks it is reasonable",
           "Validation is done by the user and verification is done by the program",
           "Validation checks the data type and verification checks the data range"], 0,
          "Verification asks if the data matches what the person meant, for example by double entry. Validation asks if it is acceptable."),
        Q("What is authentication?",
          ["Proving the identity of a user", "Checking that a number is in range",
           "Removing spaces from input", "Testing a program"], 0,
          "A password, a fingerprint or a code sent to a phone are all ways of authenticating."),
        Q("What is a logic error?",
          ["The program runs but gives the wrong result", "The program will not start",
           "The program crashes on a certain line", "The program has no comments"], 0,
          "No error message appears, which is why logic errors are found only by checking results against what was expected."),
        Q("When does iterative testing take place?",
          ["During development, as each part is finished", "Only once the whole program is finished",
           "Only by the end user", "Only before any code is written"], 0,
          "Testing each part when it is written means a fault can only be in the few lines just added."),
        Q("Which of these makes code easier to maintain?",
          ["Meaningful variable names and comments", "Single letter variable names",
           "Putting everything in one long block", "Removing all indentation"], 0,
          "The aim is that a different programmer can understand the code, so it must say what it is doing."),
    ],
    exam=[
        EQ("Explain the difference between validation and verification.", 3, [
            MP("Validation checks that data is reasonable or allowed", ["reasonable", "sensible", "acceptable", "allowed", "range", "meets rules"]),
            MP("Verification checks that data was entered as the user intended", ["intended", "same as", "matches", "double entry", "typed twice", "entered correctly", "accurate"]),
            MP("Validation cannot tell whether the data is actually correct", ["not correct", "cannot check", "still wrong", "may be wrong", "does not mean correct", "actually correct", "true"]),
        ], "Validation is an automatic check that the data entered is reasonable and allowed, such as a number being in range, but it cannot tell if the data is actually correct, because a wrong age that is still between 0 and 120 will pass. Verification checks that the data was entered as the user intended, for example by asking for a password to be typed twice and comparing the two.",
           command="Explain"),
        EQ("Write a Python function called good_password that takes a password and returns True if it is at least 8 characters long and contains at least one digit, and False otherwise.", 4, [
            MP("Defines a function with a parameter for the password", ["def good_password", "def", "password"]),
            MP("Checks the length is 8 or more using len", ["len(", ">= 8", "len"]),
            MP("Loops through the characters checking for a digit, such as with isdigit", ["isdigit", "for", "digit", "loop"]),
            MP("Returns True only when both conditions are met", ["return", "and", "true"]),
        ], r"""```python
def good_password(password):
    has_digit = False
    for ch in password:
        if ch.isdigit():
            has_digit = True
    return len(password) >= 8 and has_digit

print(good_password("Tr1angle!"), good_password("password"), good_password("a1"))
```

The loop sets a flag if any character is a digit. The function returns True only when the length check and the digit check are both true. The calls shown print True False False.""",
           command="Write"),
        EQ("A program asks the user to enter their test mark, which must be a whole number from 0 to 100 inclusive. Give one item of normal data, one item of boundary data, one item of invalid data and one item of erroneous data that could be used to test it. State whether each should be accepted.", 4, [
            MP("Normal data accepted, such as 50", ["50", "normal", "75", "accepted", "20"]),
            MP("Boundary data such as 0 or 100 accepted, or 101 or -1 rejected", ["0", "100", "101", "-1", "boundary"]),
            MP("Invalid data such as 150 or -20 rejected", ["150", "-20", "invalid", "250", "rejected"]),
            MP("Erroneous data such as a word or a decimal rejected", ["abc", "word", "text", "letters", "ten", "4.5", "decimal", "erroneous"]),
        ], "Normal data, for example 50, should be accepted. Boundary data is on the edge of the range: 0 or 100 should be accepted, and the values just outside, -1 or 101, should be rejected. Invalid data is a whole number outside the range, such as 150, and should be rejected. Erroneous data is the wrong type altogether, such as the word ten or the decimal 7.5, and should be rejected.",
           command="Give"),
        EQ("A login system gives users three attempts to enter the correct password. Describe two other ways that the system could be made more secure.", 4, [
            MP("Two factor authentication such as a code sent to a phone", ["two factor", "2fa", "second", "code", "phone", "text message"]),
            MP("Explains that a stolen password alone is then not enough", ["stolen", "not enough", "also need", "device", "second step", "extra"]),
            MP("Rules for password strength such as minimum length, digits or capitals", ["length", "digit", "capital", "uppercase", "strong", "special", "complexity"]),
            MP("Explains that stronger passwords are harder to guess", ["harder to guess", "guess", "brute force", "crack", "predict"]),
        ], "Two factor authentication asks for something in addition to the password, such as a code sent to the user's phone, so a person who has stolen or guessed the password still cannot log in without the second device. Enforcing password rules, such as a minimum length and a mix of capitals, digits and symbols, makes the password much harder to guess or to crack by trying many combinations.",
           command="Describe"),
        EQ("The program shown works but is difficult to maintain. Explain two changes that would make it easier to maintain.", 4, [
            MP("Use meaningful names for the function, parameters and variables", ["meaningful", "descriptive", "names", "identifier", "rename"]),
            MP("So that another programmer can tell what each one is for", ["understand", "tell what", "purpose", "read", "clear", "obvious"]),
            MP("Replace 0.2 with a named constant, or add comments and white space", ["constant", "0.2", "vat", "comments", "white space", "whitespace", "indent"]),
            MP("So the value is only changed in one place, or the reader knows why the code is there", ["one place", "change", "explain", "why", "once"]),
        ], "The names f, a, b, c and x say nothing about what the program does, so they should be replaced with meaningful names such as calculate_vat, price, quantity and vat, so another programmer can tell what each is for without working it out. The number 0.2 is unexplained, so it should be stored in a named constant such as VAT_RATE, which explains it and means it only has to be changed in one place if the tax rate changes. Comments and white space around the operators would also make the code easier to follow.",
           command="Explain",
           figure="""```python
def f(a,b):
    c=a*b*0.2
    return c
x=f(50,2)
print(x)
```"""),
    ],
)
