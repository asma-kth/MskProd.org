"""GCSE Python: databases and SQL, run for real with sqlite3."""
from mskbuild.models import Topic, Section, Q, EQ, MP

INPUTS = {}
EXPECT = {}

TOPIC = Topic(
    slug="databases-and-sql",
    title="Databases and SQL",
    spec="GCSE 5",
    icon="i-database",
    minutes=40,
    blurb="Tables, records, fields and keys, then SQL that actually runs: SELECT, WHERE, LIKE, ORDER BY, INSERT, UPDATE and DELETE, and how a Python program talks to a database without being hacked.",
    fact="Python ships with a complete SQL database engine, SQLite, built in. It is probably the most widely deployed database in the world, and one sits inside every Android phone, every iPhone and every copy of Chrome and Firefox.",
    sections=[
        Section("Tables, records, fields and keys", r"""
A **database** is an organised collection of data. At GCSE it is made of **tables**, and a table is a grid where:

- each **column** is a **field**, a single kind of fact, with a data type
- each **row** is a **record**, all the facts about one thing
- one field is chosen as the **primary key**, whose value is unique to each record

| StudentID | Name | Year | Mark |
| 1 | Asha | 10 | 56 |
| 2 | Ben | 11 | 71 |
| 3 | Chloe | 10 | 38 |

`StudentID` is the primary key. There may be two students called Asha, and two with a mark of 56, but never two with the same `StudentID`, so a key finds exactly one record.

!key Why a key and not a name :: Anything that could be repeated cannot identify a record. Names, dates of birth and marks all repeat. That is why every table is given a number or a code that is unique by design.

### A real database in Python

Python has SQLite built in. `":memory:"` makes a database that exists only while the program runs, which is ideal for learning. Everything in this topic can be run with the button.

```python
import sqlite3

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE Student (StudentID INTEGER PRIMARY KEY, Name TEXT, Year INTEGER, Mark INTEGER)")
db.executemany("INSERT INTO Student VALUES (?, ?, ?, ?)", [
    (1, "Asha", 10, 56),
    (2, "Ben", 11, 71),
    (3, "Chloe", 10, 38),
    (4, "Dev", 11, 90),
    (5, "Esme", 10, 64),
    (6, "Alan", 11, 45),
])

for record in db.execute("SELECT * FROM Student"):
    print(record)
```

Each record comes back as a tuple, in the order of the fields. The data types SQLite uses are `INTEGER` for whole numbers, `REAL` for decimals and `TEXT` for strings.
"""),
        Section("Searching with SELECT", r"""
The exam asks you to **search** a table with `SELECT`. The three parts, always in this order:

| Clause | What it says | Example |
| `SELECT` | Which fields to show | `SELECT Name, Mark` |
| `FROM` | Which table | `FROM Student` |
| `WHERE` | Which records to include | `WHERE Mark >= 60` |

`SELECT *` means every field. A query with no `WHERE` returns every record.

!diagram py-sql-anatomy

This program sets the same table up and runs five queries, printing each query and its result. Run it and match each result to the table.

```python
import sqlite3

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE Student (StudentID INTEGER PRIMARY KEY, Name TEXT, Year INTEGER, Mark INTEGER)")
db.executemany("INSERT INTO Student VALUES (?, ?, ?, ?)", [
    (1, "Asha", 10, 56), (2, "Ben", 11, 71), (3, "Chloe", 10, 38),
    (4, "Dev", 11, 90), (5, "Esme", 10, 64), (6, "Alan", 11, 45),
])

def run(sql):
    print(sql)
    for record in db.execute(sql):
        print("    ", record)

run("SELECT Name, Mark FROM Student WHERE Mark >= 60")
run("SELECT * FROM Student WHERE Year = 10 AND Mark < 50")
run("SELECT Name FROM Student WHERE Year = 11 OR Mark > 60")
run("SELECT Name FROM Student WHERE Name LIKE 'A%'")
run("SELECT Name, Mark FROM Student ORDER BY Mark DESC")
```

### The operators in a WHERE

| Need | Write | Notes |
| Compare | `=` `<>` `<` `<=` `>` `>=` | One equals sign, not two. Not equal is `<>` |
| Both | `AND` | `Year = 10 AND Mark < 50` |
| Either | `OR` | `Year = 11 OR Mark > 60` |
| Pattern | `LIKE` | `%` matches any run of characters |
| Order | `ORDER BY` | `ASC` is the default, `DESC` is highest first |

!warn Text goes in quotes, numbers do not :: `WHERE Name = 'Asha'` but `WHERE Year = 10`. Wrong the other way round and the query either fails or silently finds nothing.

`LIKE 'A%'` means "starts with A". `'%a'` ends with a, and `'%an%'` contains an anywhere. That is the whole of pattern matching at GCSE.
"""),
        Section("Changing data: INSERT, UPDATE and DELETE", r"""
Three statements change the table. All three come up in the exam.

```pseudo
INSERT INTO Student (StudentID, Name, Year, Mark) VALUES (7, 'Femi', 10, 58)
UPDATE Student SET Mark = Mark + 5 WHERE Year = 10
DELETE FROM Student WHERE Mark < 45
```

!warn Forget the WHERE and it applies to every record :: `UPDATE Student SET Mark = 0` sets every mark in the whole table to zero, and `DELETE FROM Student` empties it. There is no undo. Always write the WHERE first, then the rest.

The program below counts the records each statement touches, which is a good habit before trusting an UPDATE or DELETE.

```python
import sqlite3

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE Student (StudentID INTEGER PRIMARY KEY, Name TEXT, Year INTEGER, Mark INTEGER)")
db.executemany("INSERT INTO Student VALUES (?, ?, ?, ?)", [
    (1, "Asha", 10, 56), (2, "Ben", 11, 71), (3, "Chloe", 10, 38),
    (4, "Dev", 11, 90), (5, "Esme", 10, 64), (6, "Alan", 11, 45),
])

db.execute("INSERT INTO Student (StudentID, Name, Year, Mark) VALUES (7, 'Femi', 10, 58)")

changed = db.execute("UPDATE Student SET Mark = Mark + 5 WHERE Year = 10").rowcount
print(changed, "records updated")

removed = db.execute("DELETE FROM Student WHERE Mark < 45").rowcount
print(removed, "record deleted")

for record in db.execute("SELECT Name, Mark FROM Student WHERE Year = 10"):
    print(record)
```

Year 10 had four students once Femi joined, so four records were updated. Chloe's 38 became 43, which is under 45, so she was then deleted.

### Two tables and a foreign key

A school has far more than students: subjects, results, teachers. Putting every fact in one table repeats the same details over and over. A **relational database** splits the facts across several tables and links them with a **foreign key**, a field in one table that holds the primary key of another.

```python
import sqlite3

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE Student (StudentID INTEGER PRIMARY KEY, Name TEXT)")
db.execute('''CREATE TABLE Result (
    ResultID INTEGER PRIMARY KEY,
    StudentID INTEGER,
    Subject TEXT,
    Mark INTEGER,
    FOREIGN KEY (StudentID) REFERENCES Student(StudentID))''')
db.executemany("INSERT INTO Student VALUES (?, ?)", [(1, "Asha"), (2, "Ben")])
db.executemany("INSERT INTO Result VALUES (?, ?, ?, ?)", [
    (1, 1, "Computing", 56), (2, 1, "Maths", 71),
    (3, 2, "Computing", 64), (4, 2, "Maths", 48),
])

sql = '''SELECT Student.Name, Result.Subject, Result.Mark
         FROM Student JOIN Result ON Student.StudentID = Result.StudentID
         WHERE Result.Mark >= 60'''
for record in db.execute(sql):
    print(record)
```

`StudentID` in `Result` is the foreign key. Asha's name is stored once, however many results she has. A `JOIN` joins the tables back together for a query. Joins go beyond what the GCSE examines, but the key idea, that a foreign key links two tables, does not.
"""),
        Section("SQL from a program, safely", r"""
Real programs build queries out of what the user typed. That is dangerous if done carelessly. Suppose a program looks a student up by name, and somebody types this as the name:

```text
x' OR '1'='1
```

Joined into the query as text, the query becomes `SELECT * FROM Student WHERE Name = 'x' OR '1'='1'`, and `'1'='1'` is always true, so every record is returned. This is **SQL injection**.

```python
import sqlite3

db = sqlite3.connect(":memory:")
db.execute("CREATE TABLE Student (StudentID INTEGER PRIMARY KEY, Name TEXT, Mark INTEGER)")
db.executemany("INSERT INTO Student VALUES (?, ?, ?)",
               [(1, "Asha", 56), (2, "Ben", 71), (3, "Chloe", 38)])

name = "x' OR '1'='1"

unsafe = "SELECT * FROM Student WHERE Name = '" + name + "'"
print(len(db.execute(unsafe).fetchall()), "records returned by the unsafe query")

safe = db.execute("SELECT * FROM Student WHERE Name = ?", (name,))
print(len(safe.fetchall()), "records returned by the safe query")
```

The `?` is a **placeholder**. The database is given the query and the value separately, and treats the value only ever as data, never as part of the instruction. Whatever the user types, it cannot change what the query does.

!key Sanitise by never mixing :: At GCSE you may be asked to describe sanitising input. In a database program the best sanitising is not to clean the text but to keep it out of the instruction altogether.
"""),
    ],
    keyterms=[
        ("Database", "An organised collection of data that can be searched, sorted and updated."),
        ("Table", "A grid in a database, with a column for each field and a row for each record."),
        ("Record", "One row of a table, holding all the facts about one thing."),
        ("Field", "One column of a table, holding one kind of fact."),
        ("Primary key", "A field whose value is unique for every record, so it identifies exactly one."),
        ("Foreign key", "A field in one table that holds the primary key of a record in another, linking the two."),
        ("SQL", "Structured Query Language, used to search and change data in a relational database."),
        ("Wildcard", "A symbol that stands for any characters in a pattern. In SQL LIKE, the % sign."),
        ("SQL injection", "An attack in which text typed by a user is run as part of a database query."),
    ],
    grade="""
SQL questions are about precision: one wrong keyword costs the mark, and every clause is worth one.

+ Write SELECT, FROM and WHERE in the right order, and a field name exactly as the table gives it
+ Put quotation marks around text values and none around numbers
+ Use AND and OR to build conditions, and LIKE with the percent sign for a pattern
+ Never write UPDATE or DELETE without a WHERE unless every record is meant
+ Explain a primary key as unique, and a foreign key as the link to another table
""",
    mistakes=[
        "Writing == in a WHERE clause. SQL uses a single = to compare.",
        "Leaving out the quotation marks around a text value, or adding them round a number.",
        "Writing UPDATE or DELETE with no WHERE, which changes every record.",
        "Describing a primary key as the first field, when it is the field that is unique.",
        "Joining user input into the query text instead of using placeholders.",
    ],
    quiz=[
        Q("What is a primary key?",
          ["A field whose value is unique for every record", "The first field in a table",
           "A field that links to another table", "A password for the database"], 0,
          "A primary key identifies exactly one record. The foreign key is the one that links to another table."),
        Q("What is one row of a table called?",
          ["A record", "A field", "A key", "A query"], 0,
          "A row is a record, all the facts about one thing. A column is a field."),
        Q("What does `SELECT Name FROM Student WHERE Mark > 50` return?",
          ["The name of every student with a mark over 50", "Every field of every student",
           "The marks of every student called Name", "Nothing, because the query is invalid"], 0,
          "SELECT names the fields to show, FROM the table, and WHERE which records qualify."),
        Q("Which wildcard in a LIKE pattern matches any run of characters?",
          ["%", "*", "?", "#"], 0,
          "LIKE 'A%' finds every value that starts with A. The percent sign stands for any characters, including none."),
        Q("Which clause shows the highest marks first?",
          ["`ORDER BY Mark DESC`", "`ORDER BY Mark ASC`", "`GROUP BY Mark`", "`SORT Mark`"], 0,
          "ORDER BY sorts, and DESC means descending, highest first. ASC, the default, is lowest first."),
        Q("What does `UPDATE Student SET Mark = 0` do when it has no WHERE clause?",
          ["Sets the mark of every student to 0", "Sets the mark of the first student to 0",
           "Does nothing", "Causes a syntax error"], 0,
          "With no WHERE, every record qualifies. This is the most common and most damaging SQL mistake."),
        Q("Which statement removes records from a table?",
          ["`DELETE FROM`", "`REMOVE`", "`DROP RECORD`", "`CLEAR`"], 0,
          "DELETE FROM table WHERE condition removes the matching records."),
        Q("What is a foreign key?",
          ["A field that holds the primary key of a record in another table",
           "A second primary key, used when the first one has already been taken",
           "A key that is stored in a separate file so that it cannot be copied",
           "A field that can hold any value because the database does not check it"], 0,
          "The foreign key is what links two tables together, such as StudentID inside a Result table."),
        Q("Why should a Python program use `?` placeholders in an SQL query?",
          ["It stops typed text being run as part of the query", "It makes the query run faster",
           "It lets the query return more records", "It is only needed for numbers"], 0,
          "The value is handed to the database separately, so it can only ever be treated as data."),
        Q("What does the `*` in `SELECT * FROM Student` mean?",
          ["Every field", "Multiply", "Every table", "The first field only"], 0,
          "The star is a shorthand for all the fields of the table."),
    ],
    exam=[
        EQ("State what is meant by a primary key, and why every table needs one.", 2, [
            MP("A field that holds a value that is unique to each record", ["unique", "different for every record", "no two", "identif"]),
            MP("So that each record can be identified or found without confusion", ["identif", "find", "distinguish", "no confusion", "link", "exactly one"]),
        ], "A primary key is a field whose value is unique to each record in the table. Every table needs one so that each record can be identified exactly, because other fields such as a name could be repeated.",
           command="State"),
        EQ("A table called Book has the fields BookID, Title, Author and Pages. Write an SQL query that displays the title of every book that has more than 300 pages, with the book with the most pages first.", 3, [
            MP("SELECT Title FROM Book", ["select title from book", "select title"]),
            MP("WHERE Pages > 300", ["where pages > 300", "pages > 300", "pages >300"]),
            MP("ORDER BY Pages DESC", ["order by pages desc", "desc", "descending"]),
        ], r"""```text
SELECT Title
FROM Book
WHERE Pages > 300
ORDER BY Pages DESC
```

SELECT names the field to display and FROM the table. WHERE restricts the records to those with more than 300 pages, and ORDER BY with DESC puts the longest book first.""",
           command="Write"),
        EQ("Write an SQL statement that changes the author of the book with BookID 7 to the text A. Khan.", 3, [
            MP("UPDATE Book", ["update book", "update"]),
            MP("SET Author = 'A. Khan'", ["set author", "author = ", "a. khan"]),
            MP("WHERE BookID = 7", ["where bookid = 7", "bookid = 7", "bookid=7"]),
        ], r"""```text
UPDATE Book
SET Author = 'A. Khan'
WHERE BookID = 7
```

The WHERE clause is essential. Without it every book in the table would be given A. Khan as its author.""",
           command="Write"),
        EQ("The records in the Student table are shown. State the result of the query SELECT Name FROM Student WHERE Year = 11 AND Mark >= 60.", 2, [
            MP("Ben is included", ["ben"]),
            MP("Dev is included, and no other names", ["dev"]),
        ], "Only Ben and Dev are in Year 11 with a mark of 60 or more. Alan is in Year 11 but scored 45, and Esme scored 64 but is in Year 10.",
           command="State",
           figure="""| StudentID | Name | Year | Mark |
| 1 | Asha | 10 | 56 |
| 2 | Ben | 11 | 71 |
| 3 | Chloe | 10 | 38 |
| 4 | Dev | 11 | 90 |
| 5 | Esme | 10 | 64 |
| 6 | Alan | 11 | 45 |"""),
        EQ("A program asks the user to type a name and joins it into an SQL query using string concatenation. Explain the security risk, and describe how it should be done instead.", 4, [
            MP("The user could type SQL code instead of a name", ["sql code", "type code", "instructions", "commands", "malicious", "sql injection"]),
            MP("This would be run as part of the query, so data could be read or changed that should not be", ["run as part", "executed", "all records", "delete", "change", "see all", "expose"]),
            MP("Use placeholders or a parameterised query", ["placeholder", "parameter", "parameteris"]),
            MP("The value is passed separately so it is treated only as data", ["separately", "only as data", "data not code", "treated as data", "not part of the query"]),
        ], "A user could type SQL code into the name box instead of a name. Because the text is joined into the query, it is run as part of the instruction, which is called SQL injection, and it could return every record or change or delete data. The query should instead use a placeholder, or parameterised query, where the value is passed to the database separately, so whatever is typed is treated only as data and never as part of the query.",
           command="Explain"),
    ],
)
