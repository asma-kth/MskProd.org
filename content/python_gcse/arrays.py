"""GCSE Python: arrays, two dimensional arrays, records and text files."""
from mskbuild.models import Topic, Section, Q, EQ, MP

INPUTS = {}

TOPIC = Topic(
    slug="arrays-records-and-files",
    title="Arrays, Records and Files",
    spec="GCSE 2",
    icon="i-table",
    minutes=40,
    blurb="One and two dimensional arrays, records, and text files: the three ways a GCSE program holds a lot of data, with the lists, dictionaries and files that do the work in Python.",
    fact="A 1 megabyte text file of names and marks is about the same size as a single photograph from an old phone, yet it can hold more than fifty thousand records. Text is a very compact way to store data.",
    sections=[
        Section("One dimensional arrays", r"""
An **array** is a numbered row of boxes that all hold the same type of data. In the exam you declare one with a fixed size, and the first box is number **0**:

```pseudo
array scores[5]
scores[0] = 12
scores[1] = 18
scores[4] = 7
```

Python has no fixed-size array. A **list** does the same job and can also grow, so when you write an exam answer in Python, *behave like an array*: make the list the right size at the start, and do not use `append` or `insert`.

```python
# array scores[5]
scores = [0] * 5
scores[0] = 12
scores[1] = 18
scores[4] = 7
print(scores)             # [12, 18, 0, 0, 7]
print(len(scores))        # 5
```

The positions of a five box array are 0, 1, 2, 3 and 4. Asking for a position that does not exist is an error:

```python
# raises: IndexError
scores = [12, 18, 0, 0, 7]
print(scores[5])
```

### Going through an array

Use the index when the position matters, and the value when it does not.

```python
scores = [12, 18, 0, 0, 7]

for i in range(len(scores)):
    print("Position", i, "holds", scores[i])

for score in scores:
    print(score)
```

### The array algorithms the exam keeps asking for

Every one of these is a loop with something carried from one pass to the next. Learn the shape of each.

```python
marks = [56, 71, 38, 90, 64]

total = 0
for mark in marks:
    total = total + mark
average = total / len(marks)
print(total, average)                       # 319 63.8

highest = marks[0]
position = 0
for i in range(1, len(marks)):
    if marks[i] > highest:
        highest = marks[i]
        position = i
print(highest, "at position", position)     # 90 at position 3

passes = 0
for mark in marks:
    if mark >= 50:
        passes = passes + 1
print(passes, "passed")                     # 4 passed
```

Notice that `highest` starts as the **first item**, not as 0. Starting at 0 fails if every value is negative, and starting at the first item is always right.

### Linear search

Check every item in turn. Return its position when found, and only say "not found" after the whole array has been checked.

```python
def find(names, target):
    for i in range(len(names)):
        if names[i] == target:
            return i
    return -1

names = ["Asha", "Ben", "Chloe", "Dev"]
print(find(names, "Chloe"))     # 2
print(find(names, "Zoe"))       # -1
```

!warn The return -1 goes outside the loop :: If it sits inside the loop, in an else branch, the function gives up after the first item that does not match.

### Parallel arrays

Two arrays can describe the same set of things, if the box at one position in one array belongs with the box at the same position in the other.

```python
names = ["Asha", "Ben", "Chloe", "Dev"]
marks = [56, 71, 38, 90]

best = 0
for i in range(1, len(marks)):
    if marks[i] > marks[best]:
        best = i
print(names[best], "scored", marks[best])     # Dev scored 90
```

They only stay in step if every change is made to both. Sort one array on its own and the names no longer match the marks. That fragility is the reason records exist.
"""),
        Section("Two dimensional arrays", r"""
A **two dimensional array** is a table: rows and columns. OCR writes the row first and the column second, `grid[1,2]`. Python uses a list of lists, so the same box is `grid[1][2]`.

```pseudo
array grid[3,4]
grid[1,2] = 9
```

```python
# array grid[3,4]: 3 rows, 4 columns
grid = [[0] * 4 for row in range(3)]
grid[1][2] = 9
print(grid)               # [[0, 0, 0, 0], [0, 0, 9, 0], [0, 0, 0, 0]]
```

!diagram py-array-grid

!warn Never build the grid as `[[0] * 4] * 3` :: That does not make three rows. It makes three names for **one** row, so changing a box in one row changes it in all of them.

```python
wrong = [[0] * 4] * 3
wrong[1][2] = 9
print(wrong)              # [[0, 0, 9, 0], [0, 0, 9, 0], [0, 0, 9, 0]]
```

### Going through a table

An outer loop for the rows, and an inner loop for the columns. The inner loop runs all the way round for every single pass of the outer one.

```python
marks = [
    [56, 61, 70],
    [72, 68, 75],
    [38, 45, 40],
    [90, 85, 94],
]

for row in range(len(marks)):
    total = 0
    for col in range(len(marks[row])):
        total = total + marks[row][col]
    print("Student", row, "average", round(total / 3, 1))
```

The total is set to 0 inside the outer loop, so each student starts afresh. Move that line above the outer loop and every student's total includes the one before.

To go down the columns instead, swap the loops, and the outer loop is now the column:

```python
marks = [
    [56, 61, 70],
    [72, 68, 75],
    [38, 45, 40],
    [90, 85, 94],
]

for col in range(3):
    best = 0
    for row in range(4):
        if marks[row][col] > best:
            best = marks[row][col]
    print("Best in test", col, "is", best)
```

### A board game

Noughts and crosses is a 3 by 3 array of characters. Checking a row is one comparison:

```python
board = [["X", "X", "X"],
         ["O", "X", "O"],
         [" ", "O", " "]]

for row in range(3):
    if board[row][0] == board[row][1] == board[row][2] == "X":
        print("X wins on row", row)
```

!key Rows first, then columns :: `marks[row][col]`. The first index picks a list inside the big list, and the second picks an item inside that list. If you are unsure which is which, draw the table and write the row and column numbers round the outside before you write any code.
"""),
        Section("Records", r"""
An array holds many items of **one** type. A **record** holds the facts about **one** thing, and those facts can be of different types. Each fact is a **field**.

```pseudo
record Student
    name : string
    age : integer
    passed : Boolean
endrecord
```

Python has no record type at this level. A dictionary does the job, with the field names as keys.

```python
student = {"name": "Asha", "age": 15, "passed": True}
print(student["name"], student["age"])      # Asha 15
student["age"] = 16
print(student)             # {'name': 'Asha', 'age': 16, 'passed': True}
```

### An array of records

A list of dictionaries is a table where each row is one record. This is the structure behind nearly every real program that stores people, products or scores.

```python
students = [
    {"name": "Asha", "age": 15, "mark": 56},
    {"name": "Ben", "age": 16, "mark": 71},
    {"name": "Chloe", "age": 15, "mark": 38},
]

for s in students:
    print(s["name"], "is", s["age"], "and scored", s["mark"])

print(students[1]["name"])          # Ben, the second record

for s in students:
    if s["mark"] < 50:
        print(s["name"], "needs a resit")      # Chloe needs a resit
```

A class gives a record named, checked fields. It is more than the GCSE needs, but it is how larger programs do it:

```python
from dataclasses import dataclass

@dataclass
class Student:
    name: str
    age: int
    passed: bool

asha = Student("Asha", 15, True)
print(asha.name, asha.age)      # Asha 15
print(asha)                     # Student(name='Asha', age=15, passed=True)
```

### Why records beat parallel arrays

| | Parallel arrays | Array of records |
| Keeping items together | Only by discipline, one index at a time | The record moves as one unit |
| Sorting | Every array has to be swapped in step | Swap whole records |
| Adding a field | A new array and new code everywhere | A new key |
| Resemblance to a database | Little | A table: record is a row, field is a column |

!key A record is a row of a database table :: When you reach SQL in a later topic, the table is the array, each row is a record, and each column is a field. The ideas are the same.
"""),
        Section("Text files", r"""
Variables vanish when a program ends. A **file** keeps data after it does. The exam uses text files: lines of characters, read and written one at a time.

| OCR reference language | Python |
| `newFile("scores.txt")` | `open("scores.txt", "w")` |
| `myFile = open("scores.txt")` | `file = open("scores.txt")` |
| `myFile.readLine()` | `file.readline()` or `for line in file` |
| `myFile.endOfFile()` | the `for line in file` loop ends by itself |
| `myFile.writeLine("text")` | `file.write("text\n")` |
| `myFile.close()` | `file.close()` |

`writeLine` adds the end of line for you. Python's `write` does not, so you add `\n` yourself.

### Open modes

| Mode | Does | If the file already exists |
| `"r"` | Read only | Reads it. Error if it does not exist |
| `"w"` | Write | **Erases everything** and starts again |
| `"a"` | Append | Keeps it and adds to the end |

```python
file = open("scores.txt", "w")
file.write("Asha,56\n")
file.write("Ben,71\n")
file.write("Chloe,38\n")
file.close()

file = open("scores.txt", "r")
for line in file:
    print(line.strip())
file.close()
```

Each line read from a file still has its `\n` on the end. `strip()` takes it off. Forget it and every printed line is followed by a blank one, and a number read this way carries a newline into every comparison.

!info Files in the browser :: When you press Run on this page the file is created in a small private disk that lives in your browser tab. It disappears when you close the tab, so write it and read it back in the same program, as these examples do.

### Reading records from a file

Each line is one record and the commas separate the fields. `split(",")` cuts a line into a list, and everything read from a file is text, so a number must be cast.

```python
file = open("scores.txt", "w")
file.write("Asha,56\nBen,71\nChloe,38\n")
file.close()

students = []
file = open("scores.txt")
for line in file:
    name, mark = line.strip().split(",")
    students.append({"name": name, "mark": int(mark)})
file.close()

total = 0
for s in students:
    total = total + s["mark"]
print(students[0])                    # {'name': 'Asha', 'mark': 56}
print("Average", total / len(students))      # Average 55.0
```

### Closing for you

The `with` statement closes the file when its block ends, even if something goes wrong inside it, so you cannot forget.

```python
with open("log.txt", "w") as file:
    file.write("first\n")

with open("log.txt", "a") as file:
    file.write("second\n")

with open("log.txt") as file:
    first = file.readline()
    rest = file.readlines()
print(repr(first), rest)           # 'first\n' ['second\n']
```

### A file that is not there

```python
try:
    file = open("missing.txt")
except FileNotFoundError:
    print("That file does not exist yet")
```

!exam Closing the file is a mark :: If a question says "write a program that reads a file", the mark scheme has a separate mark for closing it. Either call `close()` or use `with`.
"""),
    ],
    keyterms=[
        ("Array", "A fixed size, numbered collection of items that are all the same data type, indexed from 0."),
        ("Index", "The number that identifies one item in an array. The first is 0."),
        ("Two dimensional array", "An array of arrays, organised as rows and columns, accessed with two indexes."),
        ("Record", "A collection of related fields, which may be different data types, describing one thing."),
        ("Field", "One named item of data inside a record, such as name or age."),
        ("Parallel arrays", "Two or more arrays where the items at the same index belong together."),
        ("Linear search", "Checking each item in turn from the start until the one wanted is found or the end is reached."),
        ("Text file", "A file of characters organised in lines, read and written by a program one line at a time."),
        ("Append mode", "Opening a file so that new data is added to the end and existing data is kept."),
    ],
    grade="""
Marks on data structure questions are awarded for the shape of the loop and for the details that beginners drop.

+ Start a maximum or minimum at the first item of the array, never at zero
+ Reset a running total inside the outer loop of a two dimensional array
+ Put the not found result after the loop, never inside it
+ Cast every value read from a file, and strip the newline from every line
+ Close every file you open, or use with, and say which mode you want and why
""",
    mistakes=[
        "Treating positions as starting at 1, so the last item is one position out of range.",
        "Starting a highest value at 0, which fails when the values are all negative.",
        "Opening a file in write mode to add a line, which erases everything already in it.",
        "Swapping the row and column indexes in a two dimensional array.",
        "Forgetting to cast a value read from a file, so that 56 is added as text.",
    ],
    quiz=[
        Q("What is the index of the first item in an array?",
          ["0", "1", "-1", "It depends on the size of the array"], 0,
          "Arrays are indexed from 0 in the exam and in Python, so a five item array has positions 0 to 4."),
        Q("`names = [\"Ann\", \"Bo\", \"Cy\"]`. What happens when `names[3]` runs?",
          ["An IndexError", "It returns `\"Cy\"`", "It returns `None`", "It adds a fourth item"], 0,
          "Valid positions are 0, 1 and 2. Position 3 does not exist, so Python stops with an index error."),
        Q("Which line builds a 3 row by 4 column grid of zeros with three separate rows?",
          ["`[[0] * 4 for row in range(3)]`", "`[[0] * 4] * 3`", "`[[0 for col in range(3)] for row in range(4)]`", "`[[0 for col in range(4)] * 3]`"], 0,
          "A list comprehension makes a new inner list on every pass. Multiplying the outer list copies one reference three times."),
        Q("In OCR reference language `grid[1,2]` is row 1, column 2. How is it written in Python?",
          ["`grid[1][2]`", "`grid[1, 2]`", "`grid(1, 2)`", "`grid[2][1]`"], 0,
          "A Python grid is a list of lists, so you index twice: the row first, then the column."),
        Q("Two parallel arrays hold names and marks. What makes them work?",
          ["The same index in each array refers to the same person", "They must have different lengths",
           "One must hold only text and the other only numbers", "They must be sorted"], 0,
          "Nothing links them except position. That is why sorting or deleting from one but not the other breaks the data."),
        Q("What is a record?",
          ["A set of related fields about one thing, which can be different data types",
           "A numbered list of values that must all be the same data type",
           "A stored file of text that a program reads one line at a time",
           "A value that is stored in one variable for the whole program"], 0,
          "An array is many of one type. A record is many facts, of any types, about one thing."),
        Q("Which file mode erases the existing contents of the file?",
          ["`\"w\"`", "`\"r\"`", "`\"a\"`", "None of them"], 0,
          "Write mode starts the file from empty every time. Use append mode to keep what is there and add to the end."),
        Q("A line read from a file is `\"Asha,56\\n\"`. Which method removes the newline?",
          ["`strip()`", "`split()`", "`upper()`", "`close()`"], 0,
          "strip removes whitespace from both ends of a string, including the end of line character."),
        Q("`students` is a list of dictionaries. Which expression is the mark of the third student?",
          ["`students[2][\"mark\"]`", "`students[3][\"mark\"]`", "`students[\"mark\"][2]`", "`students.mark[2]`"], 0,
          "The third item is at position 2. That item is a dictionary, and the field name picks the value."),
        Q("What is the main advantage of using `with open(...) as file`?",
          ["The file is closed automatically when the block ends", "The file opens faster because Python skips the usual checks",
           "The file can hold more data than one opened the normal way", "The file is made read only so it cannot be changed by accident"], 0,
          "Closing is easy to forget, and an error in the block would skip it. with closes the file whatever happens."),
    ],
    exam=[
        EQ("Give two differences between an array and a record.", 2, [
            MP("An array holds items that are all the same data type, a record can hold different data types", ["same data type", "same type", "different data types", "different types", "mixed"]),
            MP("An array is accessed by a numeric index, a record by the name of a field", ["index", "position", "field name", "name of the field", "numeric"]),
            MP("An array holds many values of one kind, a record holds the facts about one item", ["many", "one item", "one thing", "collection of fields", "one entity"]),
        ], "An array stores a number of items that must all be the same data type and each is found by its numeric position. A record stores a set of related fields about one thing, and the fields can be different data types, such as a string for a name and an integer for an age, each found by the name of the field.",
           command="Give"),
        EQ("A two dimensional array named marks stores the results of 5 students in 3 tests, one student on each row. Write a program that outputs the total of each student's three marks.", 4, [
            MP("Outer loop that repeats once for each of the 5 students", ["range(5)", "range 5", "for student", "outer loop", "for row", "5 times"]),
            MP("Sets the total to 0 inside the outer loop, before the inner loop", ["total = 0", "total 0", "reset", "= 0"]),
            MP("Inner loop over the 3 tests adding marks[student][test] to the total", ["range(3)", "range 3", "marks[", "inner loop", "+ marks", "total +"]),
            MP("Outputs the total after the inner loop, once per student", ["print", "output", "after the inner loop"]),
        ], r"""The outer loop picks a student, the inner loop adds up that student's three tests, and the total is printed once the inner loop has finished.

```python
marks = [[56, 61, 70], [72, 68, 75], [38, 45, 40], [90, 85, 94], [60, 60, 62]]   # given in the question

for student in range(5):
    total = 0
    for test in range(3):
        total = total + marks[student][test]
    print(total)
```""",
           command="Write"),
        EQ("A text file called scores.txt holds one whole number on each line. Write a program that reads the file and outputs the highest number in it.", 4, [
            MP("Opens the file for reading and closes it", ["open", "close", "with open"]),
            MP("Reads each line using a loop until the end of the file", ["for line", "while", "readline", "loop", "each line"]),
            MP("Converts each line to an integer", ["int(", "int", "integer", "cast"]),
            MP("Compares with the highest so far, updates it, and outputs it after the loop", ["highest", "max", "if", "greater", "print"]),
        ], r"""Everything read from a file is text, so each line is cast to an integer before it is compared. The highest value is output once the whole file has been read.

```python
file = open("scores.txt", "w")        # set up the file the question describes
file.write("56\n71\n38\n90\n64\n")
file.close()

file = open("scores.txt", "r")
highest = int(file.readline())
for line in file:
    number = int(line)
    if number > highest:
        highest = number
file.close()
print(highest)
```""",
           command="Write"),
        EQ("A program stores student names in one array and their marks in a second array. Describe one problem with parallel arrays and explain how using records solves it.", 3, [
            MP("The arrays are only linked by position", ["position", "index", "linked by", "same index"]),
            MP("If one array is changed or sorted and the other is not, the data no longer matches", ["out of step", "no longer match", "sorted", "mismatch", "wrong person", "not match", "separate"]),
            MP("A record keeps all the fields for one student together so they cannot separate", ["together", "one record", "single record", "same record", "moved as one", "kept together"]),
        ], "In parallel arrays the only thing connecting a name to a mark is that they sit at the same index. If the names are sorted or one item is deleted but the marks array is not changed in the same way, the data goes out of step and a mark is attached to the wrong student. With a record, the name and the mark are fields of one record, so they are always kept together and move as one unit.",
           command="Describe"),
        EQ("Describe the difference between opening a file in write mode and in append mode.", 3, [
            MP("Write mode replaces any existing contents of the file", ["erase", "overwrite", "replace", "delete", "wipe", "start from empty"]),
            MP("Append mode keeps the existing contents", ["keeps", "retain", "existing", "already", "preserve"]),
            MP("Append mode adds new data to the end of the file", ["end of the file", "end", "add", "after"]),
        ], "Opening a file in write mode removes everything that was already stored in it and starts again from an empty file, so only the newly written data remains. Opening it in append mode keeps everything that is already there, and any new data is added after it, at the end of the file.",
           command="Describe"),
    ],
)
