"""Pearson Edexcel GCSE Computer Science revision content.

Written to the Pearson Edexcel GCSE (9 to 1) Computer Science specification
1CP2, first teaching 2020. Paper 1, Principles of Computer Science, covers
Topics 1 to 5. Paper 2, Application of Computational Thinking, is an on screen
practical programming examination sat in Python 3 and covers Topic 6.

Two things are deliberately board specific. Pseudocode follows the Edexcel
command set, so SET ... TO, SEND ... TO DISPLAY, RECEIVE ... FROM (TYPE)
KEYBOARD, END IF, END WHILE and END FOR. Storage units follow the Edexcel
binary prefixes, so kibibyte, mebibyte, gibibyte and tebibyte, each 1024 of
the unit below it.
"""
from mskbuild.models import Topic, Section, Unit, Course, Q, EQ, MP

# ================================================== 1.1 Decomposition

T_DECOMP = Topic(
    slug="decomposition-and-abstraction",
    title="Decomposition and Abstraction",
    spec="1.1",
    icon="i-brain",
    minutes=22,
    blurb="The two thinking skills the whole course rests on, what each one actually does to a problem, and how to write about them in a way that scores.",
    fact="Harry Beck's 1933 London Underground map is the most famous abstraction ever drawn. He threw away the true distances and the real geography, kept only the order of the stations and which lines meet where, and produced something far more useful for the one job passengers actually have.",
    sections=[
        Section("Decomposition: breaking the problem up", """
**Decomposition** means breaking a large, complex problem down into smaller sub problems that can each be solved on their own.

The reason this works is worth understanding properly, because the exam asks for it. A large problem is hard to hold in your head all at once. Once it is split, each sub problem is small enough to be understood, solved and, crucially, **tested in isolation**. If the finished system is wrong, you can test each part separately to find which one is at fault instead of staring at the whole thing.

### What decomposition buys you

- **Each part can be solved separately.** A sub problem that fits on one screen is a problem you can actually finish.
- **Work can be shared out.** Several programmers can write different sub programs at the same time, which is impossible if the program is one enormous block.
- **Faults are easier to find.** If the total is wrong but the input and the sorting are right, the fault is in the calculation. You have narrowed a whole program down to a few lines.
- **Parts can be reused.** A sub program that validates a date works in every system that needs a date.
- **Maintenance is cheaper.** Changing the way discounts are worked out means editing one sub program, not hunting through a thousand lines.

### A worked decomposition

Take "write a program to run a school library". That is far too big to start coding. Decompose it:

1. Store the details of every book.
2. Store the details of every borrower.
3. Issue a book to a borrower.
4. Take a book back in.
5. Work out whether a book is overdue and calculate the fine.
6. Search the catalogue by title or author.

Each of those is now a sub problem you could genuinely sit down and write. Numbers 5 and 6 could even be given to two different people on the same afternoon.

!key The sentence examiners want :: Decomposition breaks a complex problem into smaller sub problems, each of which can be solved, tested and maintained independently.
"""),
        Section("Abstraction: deciding what to ignore", """
**Abstraction** means removing or hiding unnecessary detail so that only the information needed to solve the problem is left.

The word "unnecessary" is doing all the work in that definition. Abstraction is not simply "making things simpler". It is a judgement about **which details matter for this particular problem** and deliberately throwing the rest away.

### Why hiding detail helps

- The problem becomes **easier to understand**, because there is less to think about.
- The solution becomes **quicker to design and program**, because there is less to represent.
- The program needs **less memory and less processing**, because it is not storing or calculating things nobody will use.
- The same solution can then be **applied to similar problems**, because it is no longer tied to one set of irrelevant specifics.

### Abstraction in practice

| Real situation | Kept | Removed | Why |
| Sat nav routing | Junctions, road lengths, speed limits | Building colours, hedges, road surface | None of the removed detail changes which route is shortest |
| Chess program | Piece type, square, whose turn it is | The weight of the pieces, the wood grain | The rules of chess do not depend on them |
| School register | Name, tutor group, present or absent | Eye colour, favourite subject | The register only has to record attendance |
| A racing game | Position, speed, direction, grip | Real tyre chemistry, exact engine thermodynamics | A believable feel matters more than physical accuracy, and full physics would be too slow to compute |

!warn Abstraction is not compression :: Compression squeezes data so that the same information takes fewer bits. Abstraction throws information away on purpose because it was never needed. Saying "abstraction makes the file smaller" scores nothing.

### Abstraction inside a program

Every time you call a sub program you are using abstraction. When you write `total = calculate_fine(days_late)` you do not care how the fine is worked out at that moment. The detail is hidden inside the sub program, so the part of the code you are reading only shows *what* happens, not *how*.
"""),
        Section("Using both in an exam answer", """
Almost every question on this part of the specification gives you a scenario and asks how decomposition or abstraction would be used **in that scenario**. General definitions on their own score badly.

### The two step answer

1. Give the definition in one clean sentence.
2. Apply it to the scenario using nouns from the question.

Take: *"A company is writing an app that tells cyclists the safest route across a city. Explain how abstraction would be used when designing this app."*

A weak answer says "abstraction removes unnecessary detail to make the problem simpler". True, and worth about one mark.

A strong answer says: "Abstraction means keeping only the detail needed to solve the problem. The app would store the junctions, the length of each road, whether there is a cycle lane and the accident history of each road, because all of those affect which route is safest. It would leave out the names of the shops on each street, the colour of the buildings and the exact shape of every bend, because none of them change the answer. Removing that detail means less data has to be stored and the routing calculation runs faster on a phone."

!exam Name the detail you are removing :: The single quickest way to lift a scenario answer is to say which specific things are kept and which specific things are discarded. Examiners cannot award application marks for an answer that would fit any scenario at all.

### Telling the two apart under pressure

Ask yourself: has the problem been **split into parts** (decomposition), or has **detail been left out** (abstraction)? Splitting a shopping app into login, basket and payment is decomposition. Deciding the basket only needs the product code, quantity and price is abstraction.
"""),
    ],
    keyterms=[
        ("Decomposition", "Breaking a large, complex problem down into smaller sub problems that can each be solved and tested separately."),
        ("Abstraction", "Removing or hiding unnecessary detail so that only the information needed to solve the problem remains."),
        ("Sub problem", "One of the smaller, self contained problems produced when a larger problem is decomposed."),
        ("Computational thinking", "The process of analysing a problem so that it can be solved by a computer, using decomposition, abstraction and algorithmic thinking."),
        ("Algorithm", "A precise sequence of steps that solves a problem or completes a task."),
        ("Model", "A simplified representation of a real system that keeps only the features relevant to the problem being solved."),
        ("Subprogram", "A named block of code that performs one task and can be called from elsewhere, hiding its internal detail from the caller."),
        ("Maintainability", "How easily a program can be understood and changed later, which decomposition improves by keeping each task in its own block."),
    ],
    grade="""
Average answers define the words. Grade 9 answers **use** them on the scenario in front of them.

**Say what is removed and why it does not matter.** "Abstraction removes unnecessary detail" is a definition. "The app ignores the colour of each building because it has no effect on the length of a route" is an application, and application marks are where the grade is won.

**Give the consequence.** Every point should end in a benefit: easier to test, faster to run, less memory needed, several programmers can work at once, one change fixes every use. A point without a consequence is half a point.

**Do not mix the two up.** If your answer to an abstraction question contains the phrase "split into smaller parts", you have written about decomposition and you will get nothing for it.

+ Be able to define decomposition and abstraction in one sentence each, without using the other word in the definition
+ Be able to decompose any given scenario into at least four named sub problems in under a minute
+ Be able to name three specific details you would keep and three you would remove for any given scenario
+ Be able to state a consequence for every point you make, such as faster processing or independent testing
""",
    mistakes=[
        "Defining abstraction as 'making something simpler'. Say what is removed, that it is unnecessary detail, and that what remains is what is needed to solve the problem.",
        "Using the words decomposition and abstraction as if they mean the same thing. One splits a problem into parts, the other removes detail from it.",
        "Writing a definition with no reference to the scenario in the question, which loses every application mark.",
        "Claiming abstraction makes a program more accurate. It usually makes it less accurate on purpose, in exchange for being faster and simpler.",
        "Saying decomposition 'makes the code shorter'. It usually does not. It makes the code easier to test, reuse and maintain.",
    ],
    quiz=[
        Q("Which of these best defines decomposition?",
          ["Breaking a complex problem into smaller sub problems that can be solved separately",
           "Removing unnecessary detail from a problem",
           "Reducing the size of a file so it takes less storage",
           "Writing a program in a low level language"], 0,
          "Decomposition is about splitting a problem up. Removing detail is abstraction, and reducing file size is compression."),
        Q("A game designer decides that cars in a racing game will not model the chemistry of tyre rubber. This is an example of:",
          ["Abstraction", "Decomposition", "Compression", "Validation"], 0,
          "Detail that does not affect how the game plays has been deliberately left out, which is exactly what abstraction means."),
        Q("Why does decomposition make a large program easier to debug?",
          ["Each sub problem can be tested on its own, so a fault can be traced to one part",
           "It automatically removes syntax errors",
           "It makes the program run faster",
           "It reduces the number of variables needed"], 0,
          "Testing parts separately narrows a fault down to a small section of code instead of leaving you searching the whole program."),
        Q("Which detail would a program that calculates the shortest driving route most likely abstract away?",
          ["The colour of the buildings along each road",
           "The length of each road",
           "The speed limit on each road",
           "Which junctions connect to which"], 0,
          "Length, speed limit and connections all change the answer. Building colour cannot, so it is unnecessary detail."),
        Q("A team splits a shopping website into login, product search, basket and payment. This is:",
          ["Decomposition", "Abstraction", "Iteration", "Encryption"], 0,
          "The problem has been divided into smaller sub problems, each of which can be built and tested by itself."),
        Q("Which is a genuine benefit of abstraction when writing a program?",
          ["Less data needs to be stored and processed, so the program runs faster",
           "The program will contain no logic errors",
           "The source code becomes impossible to copy",
           "Every variable is automatically validated"], 0,
          "Ignoring detail that does not matter means fewer values to store and fewer calculations to perform."),
        Q("What is the main risk of abstracting away too much detail?",
          ["The model may no longer behave enough like the real system to be useful",
           "The program will not compile",
           "The file will become larger",
           "The program will need more memory"], 0,
          "Abstraction is a judgement. Remove something that actually mattered and the results stop matching reality."),
        Q("Which statement about sub programs and abstraction is correct?",
          ["Calling a sub program hides how the task is done from the code that calls it",
           "Sub programs remove the need for variables",
           "Sub programs make a program run in less memory in every case",
           "Sub programs can only be used once in a program"], 0,
          "A call such as calculate_fine(days) says what happens without showing how, which is abstraction applied inside code."),
        Q("A hospital system is decomposed into 'store patient records', 'book appointments' and 'issue prescriptions'. What is the clearest advantage?",
          ["Three developers can work on the three parts at the same time",
           "The system will need no testing",
           "The records will automatically be encrypted",
           "The system will use less electricity"], 0,
          "Independent sub problems can be developed in parallel, which is one of the main practical reasons to decompose."),
        Q("Which pair correctly matches the technique to the action?",
          ["Abstraction: storing only a product code, price and quantity in a basket",
           "Decomposition: storing only a product code, price and quantity in a basket",
           "Abstraction: dividing a system into login, basket and payment",
           "Decomposition: ignoring the colour of the packaging"], 0,
          "Choosing which fields to keep is a decision about detail, so it is abstraction. Dividing the system into parts is decomposition."),
    ],
    exam=[
        EQ("State what is meant by the term decomposition.", 2, [
            MP("Breaking a large or complex problem into smaller parts or sub problems",
               ["breaking", "break down", "smaller problems", "sub problems", "split", "divided"]),
            MP("So that each part can be solved, tested or understood separately",
               ["solved separately", "individually", "on their own", "one at a time", "tested separately", "easier to solve"]),
        ], "Decomposition means breaking a large and complex problem down into a number of smaller sub problems. Each sub problem is small enough to be understood, solved and tested on its own, and the solutions are then combined to solve the original problem.",
           command="State"),
        EQ("A supermarket is developing an app that lets customers scan items and pay without visiting a till. Explain how decomposition would be used when developing this app.", 4, [
            MP("The overall problem is broken into smaller sub problems",
               ["broken into", "smaller sub problems", "split into parts", "divided into tasks"]),
            MP("Names sensible sub problems for this scenario, such as scanning a barcode, keeping a running total, taking payment or checking the customer out",
               ["scanning barcode", "scan item", "running total", "taking payment", "process payment", "receipt", "checkout"]),
            MP("Each sub problem can be written and tested independently",
               ["tested independently", "tested separately", "individually", "each part works", "own testing"]),
            MP("Different developers can work on different parts at the same time, and a fault can be traced to a single part",
               ["different developers", "at the same time", "team", "parallel", "locate the fault", "trace the error", "one part"]),
        ], "Decomposition would be used to break the whole app down into smaller sub problems that can each be tackled on their own. Sensible sub problems here would be reading a barcode from the camera, looking that barcode up to find the product and its price, keeping a running total of the basket, applying any offers, taking a card payment and producing a digital receipt. Each of these can be written and tested independently, so the payment code can be proved correct before it is ever joined to the scanning code. Splitting the work this way also allows several developers to build different parts at the same time, and if the finished app produces a wrong total the fault can be traced to a single sub program rather than searched for across the whole system.",
           command="Explain"),
        EQ("Explain what is meant by abstraction and give one reason why it is used.", 3, [
            MP("Removing or hiding detail that is not needed to solve the problem",
               ["removing detail", "hiding detail", "unnecessary detail", "irrelevant detail", "not needed"]),
            MP("Only the information relevant to the problem is kept",
               ["only relevant", "keeps important", "essential information", "what is needed", "focus on"]),
            MP("So the problem is simpler to solve, or the solution needs less storage or processing",
               ["simpler", "easier to understand", "less storage", "less memory", "faster", "quicker to develop"]),
        ], "Abstraction means removing or hiding the detail that is not needed to solve a particular problem, so that only the information that is genuinely relevant remains. It is used because a problem with less detail in it is easier to understand and quicker to design a solution for, and because the resulting program stores and processes less data, so it runs faster and uses less memory.",
           command="Explain"),
        EQ("A weather app models rainfall across a country. Describe two details the developers would keep and two they would remove, and justify your choices.", 4, [
            MP("Names a relevant detail that is kept, such as location, rainfall amount, time or temperature",
               ["location", "coordinates", "rainfall", "millimetres", "time", "temperature", "wind"]),
            MP("Justifies keeping it because it affects the forecast or the output the user needs",
               ["affects the forecast", "needed to predict", "user needs", "determines", "required for"]),
            MP("Names an irrelevant detail that is removed, such as building colours, street names or the shape of individual clouds",
               ["colour", "building", "street names", "shape of clouds", "names of shops", "terrain detail"]),
            MP("Justifies removing it because it does not change the result and would waste storage or processing",
               ["does not affect", "no effect", "wastes storage", "waste memory", "slower", "unnecessary"]),
        ], "The developers would keep the location of each measurement and the amount of rain recorded there, because the whole purpose of the app is to tell a user how much rain is expected at a place, so neither can be removed without breaking the app. They would also keep the time of each reading, since a forecast is meaningless without knowing when it applies. They would remove details such as the colour of the buildings in each town and the exact shape of individual clouds, because neither changes the rainfall figure a user is shown. Storing and processing that extra detail would use more memory and slow the forecast calculation down for no benefit at all.",
           command="Describe"),
        EQ("Compare decomposition and abstraction, making clear how they differ.", 4, [
            MP("Decomposition splits a problem into smaller sub problems",
               ["splits", "breaks", "smaller parts", "sub problems", "divides"]),
            MP("Abstraction removes or hides detail that is not needed",
               ["removes detail", "hides detail", "unnecessary", "irrelevant", "not needed"]),
            MP("Both reduce the complexity the programmer has to deal with at once",
               ["reduce complexity", "simpler", "easier to manage", "less to think about", "manageable"]),
            MP("They are usually used together, with a problem first broken up and detail then removed from each part",
               ["used together", "both", "combined", "after decomposing", "then abstraction"]),
        ], "Decomposition and abstraction are both ways of making a large problem manageable, but they act on it differently. Decomposition splits the problem into smaller sub problems, so a library system becomes separate tasks for issuing books, returning books and calculating fines. Abstraction does not split anything: it removes detail from the problem, so the book record keeps the title, author and ISBN but not the colour of the cover. What they share is that each reduces how much a programmer has to hold in mind at one time, which makes the solution quicker to design and easier to test. In practice they are used together, because a problem is normally decomposed into parts first and then unnecessary detail is stripped out of each part.",
           command="Compare"),
    ],
)

# ============================ 1.2 Algorithms, flowcharts and pseudocode

T_ALGOS = Topic(
    slug="algorithms-flowcharts-and-pseudocode",
    title="Algorithms, Flowcharts and Pseudocode",
    spec="1.2",
    icon="i-flow",
    minutes=34,
    blurb="Reading and writing algorithms in the two forms Edexcel uses, the exact pseudocode command set the papers are written in, and how to trace a program without guessing.",
    fact="The word algorithm comes from al-Khwarizmi, a mathematician working in Baghdad around the year 820. When his book on Indian numerals was translated into Latin, his name became algorismus, and for centuries that word simply meant doing arithmetic with the digits 0 to 9 instead of Roman numerals.",
    sections=[
        Section("What an algorithm is, and what it is not", """
An **algorithm** is a precise sequence of steps that solves a problem or completes a task. Two things make it precise: every step must be unambiguous, and the algorithm must always finish.

An algorithm is **not** a program. A program is an algorithm written in a particular programming language so a computer can run it. The same algorithm can be written as a flowchart, as pseudocode or as Python, and it is still the same algorithm. This distinction earns marks: an exam question that asks you to "write an algorithm" is not asking for perfect Python syntax, it is asking for correct logic.

### The three things every algorithm needs

- **Input**: the data it starts with.
- **Processing**: what it does to that data.
- **Output**: what it produces.

If you can name the input, the processing and the output before you write a line, the algorithm is usually half written already.

!key Correct versus efficient :: An algorithm can be correct and still be poor. Two algorithms that both produce the right answer can differ enormously in how many steps they take, and Edexcel asks you to compare them on exactly that basis.
"""),
        Section("Flowcharts", """
A **flowchart** shows an algorithm as a diagram. Edexcel uses a fixed set of symbols and you are expected to draw them correctly, not approximately.

| Symbol | Shape | Used for |
| Terminal | Rounded rectangle | START and STOP, one at each end |
| Process | Rectangle | A calculation or an assignment, such as `total = total + price` |
| Input or output | Parallelogram | Reading data in or sending data out |
| Decision | Diamond | A question with exactly two labelled outputs, Yes and No |
| Subprogram | Rectangle with a double line at each side | A call to a separate named routine |
| Flow line | Arrow | The direction the algorithm moves in |

### Rules that catch people out

- A decision diamond must contain a **question or a condition**, never a statement. `count > 10` is fine, `add one to count` is not.
- Both branches out of a decision must be **labelled** Yes and No, or True and False. An unlabelled branch is not a mark.
- Every arrow must point somewhere. A loop is drawn as an arrow going **back up** to a point above the decision.
- There is one START and normally one STOP.

### A worked flowchart, described in words

An algorithm that keeps asking for a password until it is correct looks like this: START, then an input parallelogram reading the password, then a decision diamond asking `password = "letmein"`. The No branch runs back up to just above the input, so the user is asked again. The Yes branch goes to an output parallelogram saying "Access granted" and then to STOP.

Notice where the arrow returns to. If it returned to a point *below* the input the program would loop forever comparing the same wrong password. Where a loop arrow rejoins the flow is the most common place to lose a mark in a flowchart question.
"""),
        Section("The Edexcel pseudocode command set", """
Edexcel writes the algorithms in its papers in a specific pseudocode. You do not have to answer in it, but you absolutely have to be able to **read** it, and writing in it makes your intent unmistakable. It is not the same as the pseudocode other boards use, so material written for OCR or AQA will mislead you here.

### Assignment, input and output

```pseudocode
SET total TO 0
SET name TO 'Asma'
CONST VAT_RATE = 0.2

SEND 'Enter your age' TO DISPLAY
RECEIVE age FROM (INTEGER) KEYBOARD
SEND 'Hello ' & name TO DISPLAY
```

Three points to notice. Assignment is `SET ... TO`, not an equals sign. Input states the type it expects, so `(INTEGER) KEYBOARD` reads a whole number and `(STRING) KEYBOARD` reads text. The `&` symbol joins values together, so `'Hello ' & name` produces `Hello Asma`.

### Selection

```pseudocode
IF score >= 70 THEN
    SEND 'Distinction' TO DISPLAY
ELSE IF score >= 50 THEN
    SEND 'Pass' TO DISPLAY
ELSE
    SEND 'Fail' TO DISPLAY
END IF
```

The closing keyword is `END IF`, two words. Conditions use `=` for comparison and `<>` for not equal.

### Iteration

```pseudocode
WHILE attempts < 3 DO
    RECEIVE guess FROM (INTEGER) KEYBOARD
    SET attempts TO attempts + 1
END WHILE

REPEAT
    RECEIVE answer FROM (STRING) KEYBOARD
UNTIL answer = 'yes'

FOR index FROM 0 TO 9 DO
    SEND index TO DISPLAY
END FOR

FOREACH mark FROM marks DO
    SET total TO total + mark
END FOREACH
```

`WHILE` tests the condition **before** the loop body, so it can run zero times. `REPEAT ... UNTIL` tests **after** the body, so it always runs at least once. `FOR` is count controlled, and `FOREACH` walks through every element of a data structure without you handling an index at all.

### Data structures and subprograms

```pseudocode
SET scores TO [12, 7, 19, 3]
SEND scores[0] TO DISPLAY      # indices start at 0, so this sends 12

FUNCTION doubleIt(number)
    RETURN number * 2
END FUNCTION

PROCEDURE greet(name)
    SEND 'Hello ' & name TO DISPLAY
END PROCEDURE
```

A **function** returns a value with `RETURN`. A **procedure** does a job but returns nothing. Indices start at zero, exactly as they do in Python, so `scores[3]` is the last element of a four element list.

!warn Do not import OCR habits :: `endif`, `endwhile`, `print`, `input` and `x = 5` are OCR reference language, not Edexcel. In an Edexcel answer write `END IF`, `END WHILE`, `SEND ... TO DISPLAY`, `RECEIVE ... FROM (TYPE) KEYBOARD` and `SET x TO 5`.
"""),
        Section("Trace tables", """
A **trace table** records the value of every variable after each step of an algorithm. It is how you work out what a program actually does rather than what you assume it does, and Edexcel asks for one regularly.

### How to do it without going wrong

1. Draw one column per variable, plus a column for any output.
2. Write the starting value of every variable in the first row.
3. Work through the algorithm **one line at a time**, in the order the computer would.
4. Write a new row every time a value changes. Never overwrite a value, because the history is the point.
5. Test every condition literally, using the values currently in the table, not the values you expect.

### Worked example

```pseudocode
SET total TO 0
SET count TO 1
WHILE count <= 4 DO
    SET total TO total + count
    SET count TO count + 1
END WHILE
SEND total TO DISPLAY
```

| Line | total | count | Condition count <= 4 | Output |
| Start | 0 | 1 | | |
| Loop 1 | 1 | 2 | True | |
| Loop 2 | 3 | 3 | True | |
| Loop 3 | 6 | 4 | True | |
| Loop 4 | 10 | 5 | True | |
| Test | 10 | 5 | False, loop ends | |
| Send | 10 | 5 | | 10 |

The algorithm adds 1 + 2 + 3 + 4 and outputs 10. Notice that the loop ran four times even though `count` finishes on 5, because the final test is what stops it.

!exam Trace tables are marked on the rows, not the answer :: If you write only the final answer and it is wrong you get nothing. If you show every row and make one slip, the rest of the working can still earn marks. Always fill the table in.

### Amending an algorithm

Questions often give you a working algorithm and ask you to change it, for example to also count how many numbers were entered or to reject negative values. Three habits keep this reliable:

- Declare and initialise any new variable **before** the loop, not inside it, or it resets every pass.
- Put the new statement in the right place: inside the loop if it happens every time, after the loop if it happens once at the end.
- Trace your amended version on a small example before you move on. It takes ninety seconds and it catches nearly every error.
"""),
    ],
    keyterms=[
        ("Algorithm", "A precise sequence of unambiguous steps that solves a problem or completes a task and always terminates."),
        ("Flowchart", "A diagram that represents an algorithm using standard symbols joined by arrows showing the flow of control."),
        ("Pseudocode", "A structured, language independent way of writing an algorithm using set keywords, designed to be read by people rather than run by a computer."),
        ("Trace table", "A table used to record the value of each variable after every step of an algorithm so its behaviour can be checked by hand."),
        ("Variable", "A named location in memory whose value can change while the program is running."),
        ("Constant", "A named value that is set once and cannot be changed while the program is running."),
        ("Selection", "A construct that chooses between different sets of instructions based on whether a condition is true."),
        ("Iteration", "A construct that repeats a set of instructions, either a fixed number of times or while a condition holds."),
        ("Decision symbol", "The diamond in a flowchart that contains a condition and has two labelled outputs, one for true and one for false."),
        ("Terminal symbol", "The rounded rectangle used for START and STOP at each end of a flowchart."),
    ],
    grade="""
This topic is marked on precision, and precision is a habit rather than a talent.

**Trace literally.** The commonest reason a grade 7 student drops these marks is deciding what a loop "obviously" does instead of evaluating the condition with the values actually in the table. Write the condition out, write True or False next to it, then move.

**Use the right dialect.** Writing `endwhile` in an Edexcel answer will usually still be accepted, because the mark scheme rewards correct logic, but reading the paper is harder if the command set is unfamiliar. Learn `SET ... TO`, `SEND ... TO DISPLAY` and `RECEIVE ... FROM (TYPE) KEYBOARD` until they are automatic.

**Know why one loop rather than another.** A `WHILE` loop can execute zero times and a `REPEAT ... UNTIL` loop always executes at least once. Menu systems and password prompts use `REPEAT` because the question has to be asked before it can be answered.

**Draw flowcharts with the right shapes.** A diamond that contains a statement instead of a condition, or a branch with no Yes or No label, loses the mark even when the logic is right.

+ Be able to write a trace table for a nested loop without hesitating
+ Be able to name every flowchart symbol and what it is used for
+ Be able to convert a flowchart into Edexcel pseudocode and back again
+ Be able to explain when a WHILE loop is right and when a REPEAT loop is right
+ Be able to amend a given algorithm by adding a counter, a total or a validation check
""",
    mistakes=[
        "Putting a statement such as 'add one to count' inside a decision diamond. A diamond holds a condition with two possible answers.",
        "Drawing a loop arrow that rejoins the flow below the input, so the same value is tested forever.",
        "Overwriting values in a trace table instead of adding a new row, which destroys the working the marks are for.",
        "Forgetting that indices start at zero, so treating scores[1] as the first element of a list.",
        "Initialising a total or counter inside the loop, so it resets on every pass and the final answer is always wrong.",
        "Confusing WHILE and REPEAT UNTIL. WHILE tests first and may run zero times, REPEAT tests last and always runs once.",
    ],
    quiz=[
        Q("In the Edexcel pseudocode command set, how is a value assigned to a variable?",
          ["SET total TO 0", "total = 0", "total := 0", "LET total BE 0"], 0,
          "Edexcel uses SET followed by TO for assignment. An equals sign is used for comparison, not assignment."),
        Q("Which flowchart symbol is used for a decision?",
          ["A diamond", "A parallelogram", "A rectangle", "A rounded rectangle"], 0,
          "A diamond holds a condition and has two labelled outputs. A parallelogram is input or output and a rectangle is a process."),
        Q("What does RECEIVE age FROM (INTEGER) KEYBOARD do?",
          ["Reads a value typed by the user and treats it as a whole number",
           "Outputs the value of age to the screen",
           "Sets age to the integer zero",
           "Checks whether age is an integer and reports an error"], 0,
          "RECEIVE reads input, and the type in brackets states how the typed characters should be interpreted, here as an integer."),
        Q("Which loop always executes its body at least once?",
          ["REPEAT ... UNTIL", "WHILE ... END WHILE", "FOR ... END FOR", "FOREACH ... END FOREACH"], 0,
          "REPEAT tests its condition after the body has run, so the body has already executed once by the time the test happens."),
        Q("A trace table is used to:",
          ["Record the value of each variable after every step so the algorithm can be checked by hand",
           "Convert pseudocode into machine code",
           "Measure how much memory a program uses",
           "Store test data for the final program"], 0,
          "Tracing by hand is how you find out what an algorithm really does, which is how logic errors are located."),
        Q("What is output by this algorithm? SET x TO 5, WHILE x > 8 DO, SEND x TO DISPLAY, SET x TO x + 1, END WHILE",
          ["Nothing at all", "5", "5 6 7 8", "It loops forever"], 0,
          "The condition 5 > 8 is false the first time it is tested, so a WHILE loop body never runs. This is exactly why WHILE can execute zero times."),
        Q("In Edexcel pseudocode, what does the symbol & do in SEND 'Total: ' & total TO DISPLAY?",
          ["Joins the two values together into one string for output",
           "Adds the two values as numbers",
           "Compares the two values",
           "Marks the end of the statement"], 0,
          "The ampersand is the append operator, so the text and the value are combined into a single string before being displayed."),
        Q("Which element of a flowchart is drawn as a parallelogram?",
          ["Input or output", "A process", "A decision", "The start of the algorithm"], 0,
          "Parallelograms are used wherever data comes in from the user or goes out to the screen."),
        Q("A program must ask a user for a menu choice and keep asking until the choice is valid. Which construct fits best?",
          ["REPEAT ... UNTIL", "A FOR loop", "A single IF statement", "FOREACH"], 0,
          "The question must be asked once before it can be judged, and then repeated only if it was wrong, which is the exact shape of a post conditioned loop."),
        Q("Why is an algorithm not the same thing as a program?",
          ["An algorithm is the logic, and a program is that logic written in a specific language a computer can run",
           "An algorithm always contains a loop and a program does not",
           "Algorithms are written by computers and programs by people",
           "An algorithm cannot contain selection"], 0,
          "The same algorithm can be expressed as a flowchart, as pseudocode or as Python, and it is the same algorithm each time."),
    ],
    exam=[
        EQ("State two differences between a WHILE loop and a REPEAT UNTIL loop.", 2, [
            MP("A WHILE loop tests its condition before the body runs and a REPEAT loop tests it afterwards",
               ["tests before", "condition first", "tested at the start", "tests after", "condition at the end", "tested at the end"]),
            MP("A WHILE loop may run zero times, a REPEAT loop always runs at least once",
               ["zero times", "never run", "not run at all", "at least once", "always runs once", "minimum of one"]),
        ], "A WHILE loop tests its condition before the body is executed, whereas a REPEAT UNTIL loop executes the body first and tests the condition afterwards. As a result, the body of a WHILE loop may never run at all if the condition is false to begin with, while the body of a REPEAT UNTIL loop always runs at least once.",
           command="State"),
        EQ("Describe the purpose of a trace table and explain how it helps a programmer find a logic error.", 3, [
            MP("It records the value of each variable at each step of the algorithm",
               ["records values", "values of variables", "each step", "line by line", "after each instruction"]),
            MP("The programmer can compare the actual values with the values expected",
               ["compare", "expected values", "should be", "actual value", "check"]),
            MP("The step at which a value first becomes wrong identifies where the error is",
               ["where it goes wrong", "identify the line", "locate the error", "first wrong value", "pinpoint"]),
        ], "A trace table records the value held by every variable after each step of an algorithm, together with anything the algorithm outputs. Working through the algorithm by hand and filling the table in lets the programmer compare the values the program actually produces with the values it should be producing at that point. The first row where a value differs from what was expected shows exactly which instruction is at fault, which is what makes a trace table so effective at locating logic errors, since a logic error produces a wrong answer without producing any error message at all.",
           command="Describe"),
        EQ("Describe three rules that must be followed when drawing a flowchart.", 3, [
            MP("A decision is shown as a diamond containing a condition with two labelled outputs",
               ["diamond", "decision", "two outputs", "yes and no", "true and false", "condition"]),
            MP("Input and output use a parallelogram and a process uses a rectangle",
               ["parallelogram", "input output", "rectangle", "process"]),
            MP("The flowchart begins and ends with a terminal symbol and every step is joined by arrows showing the flow",
               ["terminal", "start and stop", "rounded", "arrows", "flow lines", "direction"]),
        ], "A flowchart must begin and end with a terminal symbol, a rounded rectangle containing START or STOP, so that it is clear where the algorithm starts and finishes. Each type of step must use the correct shape: a rectangle for a process such as a calculation, a parallelogram for input or output, and a diamond for a decision. A decision must contain a condition rather than an instruction and must have exactly two outputs, each labelled Yes or No, and every symbol must be connected by arrows that show the direction the algorithm flows in, with any loop drawn as an arrow returning to a point earlier in the sequence.",
           command="Describe"),
        EQ("Write an algorithm, using pseudocode or a flowchart, that asks the user for ten numbers, adds them up and outputs the total.", 5, [
            MP("A total is initialised to zero before the loop",
               ["set total to 0", "total = 0", "initialise total", "starts at zero", "total is zero"]),
            MP("A loop that repeats exactly ten times",
               ["for", "from 1 to 10", "ten times", "while count", "repeat 10", "count < 10"]),
            MP("A number is input from the user inside the loop",
               ["receive", "input", "keyboard", "user enters", "read number"]),
            MP("The number is added to the running total inside the loop",
               ["total to total", "total = total +", "add to total", "running total", "adds the number"]),
            MP("The total is output after the loop has finished",
               ["send total", "display total", "output total", "print total", "after the loop"]),
        ], "SET total TO 0, then FOR count FROM 1 TO 10 DO, and inside that loop SEND 'Enter a number' TO DISPLAY, RECEIVE number FROM (INTEGER) KEYBOARD and SET total TO total + number, then END FOR, and finally SEND total TO DISPLAY. The total must be set to zero before the loop begins so that it is not reset on each pass, the input and the addition both sit inside the loop so that they happen ten times, and the output sits after END FOR so that the total is displayed once, when all ten numbers have been added.",
           command="Write"),
        EQ("Explain why an algorithm might be written as pseudocode before it is written as a program in Python.", 4, [
            MP("Pseudocode is not tied to any one programming language",
               ["not tied", "language independent", "any language", "no specific language", "not python"]),
            MP("The programmer can concentrate on the logic without worrying about syntax",
               ["focus on logic", "without syntax", "no syntax errors", "structure", "think about the steps"]),
            MP("It is easier for other people, including non programmers, to read and check",
               ["easier to read", "understand", "other people", "team", "checked by", "non programmer"]),
            MP("Errors in the design can be found and corrected before time is spent coding",
               ["find errors early", "before coding", "correct mistakes", "saves time", "cheaper to fix"]),
        ], "Pseudocode is deliberately not tied to any particular programming language, so the programmer can set out the logic of the solution without having to be correct about the syntax of Python at the same time. That separation matters because it means the design can be judged on whether the steps are right, rather than on whether a colon or a bracket is missing. Pseudocode is also far easier for other people to read, including team members who work in a different language and clients who do not program at all, so the design can be reviewed and agreed before any code exists. Finding a flaw in the logic at that stage costs a few minutes, whereas finding the same flaw after the program has been written, tested and documented costs a great deal more.",
           command="Explain"),
    ],
)

# ==================================== 1.2 Searching and sorting algorithms

T_SEARCHSORT = Topic(
    slug="searching-and-sorting-algorithms",
    title="Searching and Sorting Algorithms",
    spec="1.2",
    icon="i-shuffle",
    minutes=36,
    blurb="Linear search, binary search, bubble sort and merge sort: how each one moves through the data, how to trace it, and how to justify choosing one over another.",
    fact="Binary search halves the list every comparison, so ten comparisons cover 1024 items and twenty cover just over a million. That is why a phone can look a word up in a dictionary of half a million entries the instant you stop typing.",
    sections=[
        Section("Linear search and binary search", """
### Linear search

Linear search starts at the first item and checks each one in turn until it finds the target or runs out of list.

```pseudocode
FUNCTION linearSearch(items, target)
    FOR position FROM 0 TO LENGTH(items) - 1 DO
        IF items[position] = target THEN
            RETURN position
        END IF
    END FOR
    RETURN -1
END FUNCTION
```

Its strength is that it makes no demands on the data. The list can be in any order, and no preparation is needed. Its weakness is speed: on a list of n items the worst case is n comparisons, so searching a million records could mean a million checks.

### Binary search

Binary search only works on a **sorted** list. It looks at the middle item, and because the list is sorted, one comparison tells it which half the target must be in. The other half is discarded entirely.

1. Find the middle item of the search area.
2. If it is the target, stop.
3. If the target is smaller, discard the middle item and everything above it.
4. If the target is larger, discard the middle item and everything below it.
5. Repeat on what is left, until the target is found or nothing remains.

```pseudocode
FUNCTION binarySearch(items, target)
    SET low TO 0
    SET high TO LENGTH(items) - 1
    WHILE low <= high DO
        SET mid TO (low + high) DIV 2
        IF items[mid] = target THEN
            RETURN mid
        ELSE IF items[mid] < target THEN
            SET low TO mid + 1
        ELSE
            SET high TO mid - 1
        END IF
    END WHILE
    RETURN -1
END FUNCTION
```

### Worked example

Find 23 in `[4, 8, 15, 16, 23, 42, 50]`.

| Step | Search area | Middle | Comparison | Action |
| 1 | 4 to 50 | 16 | 23 is greater than 16 | Discard 4, 8, 15, 16 |
| 2 | 23 to 50 | 42 | 23 is less than 42 | Discard 42, 50 |
| 3 | 23 only | 23 | Found | Stop |

Three comparisons. Linear search would have taken five.

!key Why halving wins :: Each linear comparison rules out one item. Each binary comparison rules out half of everything that is left. On large lists that difference is the whole ball game, but it is bought with the requirement that the list is sorted first.
"""),
        Section("Bubble sort", """
Bubble sort repeatedly walks through the list comparing each pair of neighbours and swapping them if they are the wrong way round. After the first full pass the largest value has been carried all the way to the end, which is where the name comes from.

```pseudocode
PROCEDURE bubbleSort(items)
    SET swapped TO TRUE
    WHILE swapped = TRUE DO
        SET swapped TO FALSE
        FOR i FROM 0 TO LENGTH(items) - 2 DO
            IF items[i] > items[i + 1] THEN
                SET temp TO items[i]
                SET items[i] TO items[i + 1]
                SET items[i + 1] TO temp
                SET swapped TO TRUE
            END IF
        END FOR
    END WHILE
END PROCEDURE
```

### Tracing one pass

Start with `[7, 3, 9, 2]`.

- Compare 7 and 3. Wrong order, swap: `[3, 7, 9, 2]`
- Compare 7 and 9. Correct order, leave: `[3, 7, 9, 2]`
- Compare 9 and 2. Wrong order, swap: `[3, 7, 2, 9]`

End of pass one. 9 is now in its final position. Pass two produces `[3, 2, 7, 9]`, pass three produces `[2, 3, 7, 9]`, and pass four makes no swaps at all, which is how the algorithm knows it has finished.

### Why the swapped flag matters

Without the flag the algorithm has no way of knowing the list is already sorted, and would carry on making pointless passes. With it, a list that is already in order is confirmed sorted in a single pass. This is why bubble sort is respectable on nearly sorted data and dreadful on everything else.

!warn A pass is not a comparison :: Questions ask both "how many passes" and "how many comparisons". One pass over a list of n items makes n minus 1 comparisons. Read which one is being asked for.
"""),
        Section("Merge sort", """
Merge sort uses **divide and conquer**. It splits the list in half over and over until every piece holds a single item, then builds the answer back up by merging pairs of sorted pieces.

The insight it rests on is that **a list of one item is already sorted**, and that merging two sorted lists is easy: compare the first item of each, take the smaller, repeat.

### Divide

`[6, 2, 8, 4, 1]` splits into `[6, 2]` and `[8, 4, 1]`, which split into `[6]`, `[2]`, `[8]` and `[4, 1]`, and finally `[4, 1]` splits into `[4]` and `[1]`.

### Merge

- Merge `[6]` and `[2]` to get `[2, 6]`
- Merge `[4]` and `[1]` to get `[1, 4]`
- Merge `[8]` and `[1, 4]` to get `[1, 4, 8]`
- Merge `[2, 6]` and `[1, 4, 8]` to get `[1, 2, 4, 6, 8]`

### Why it is fast, and what it costs

Splitting a list of n items in half repeatedly takes about log~2~n rounds, and each round of merging touches every item once. On a list of 1000 items that is roughly 10 rounds of 1000 operations, about 10000 steps, against bubble sort's worst case of nearly 500000. The comparison is not close.

The cost is **memory**. Merge sort has to hold the sub lists separately while it merges them, so it needs additional space roughly the size of the original list. Bubble sort works in place and needs room for a single temporary variable. On a device with very little RAM that trade off can decide the choice.
"""),
        Section("Choosing and comparing", """
Edexcel asks you to compare algorithms and justify a choice. The marks are in the reasoning, so learn the trade offs rather than a ranking.

| | Linear search | Binary search |
| List must be sorted | No | Yes |
| Worst case on n items | n comparisons | About log~2~n comparisons |
| Best case | 1 comparison | 1 comparison |
| Good for | Small or unsorted lists, one off searches | Large lists that are already sorted or searched repeatedly |

| | Bubble sort | Merge sort |
| Method | Repeated swapping of neighbours | Divide the list, then merge sorted pieces |
| Speed on large lists | Very slow | Much faster and consistent |
| Extra memory | Almost none, sorts in place | Significant, sub lists are held separately |
| Easiest to write | Yes | No |
| Good for | Small or nearly sorted lists | Large lists where speed matters |

### Building the justification

The structure that scores is: name the algorithm, give the property of the data that makes it suitable, then give the consequence.

*"For a list of 50000 sorted product codes searched thousands of times a day, binary search is the better choice. The list is already sorted, so the precondition costs nothing, and each comparison eliminates half of the remaining codes, so a search takes at most about 16 comparisons instead of up to 50000. Over thousands of searches that difference is enormous."*

!exam Never answer 'binary search is faster' and stop :: That is one mark. The marks after it come from saying why it is faster, that it requires a sorted list, and what that requirement costs if the data is not already sorted.
"""),
    ],
    keyterms=[
        ("Linear search", "A search that checks each item in a list in turn from the start until the target is found or the end is reached."),
        ("Binary search", "A search that repeatedly examines the middle item of a sorted list and discards the half that cannot contain the target."),
        ("Bubble sort", "A sort that repeatedly compares adjacent items and swaps them if they are in the wrong order until a pass makes no swaps."),
        ("Merge sort", "A sort that repeatedly divides the list into halves until each holds one item, then merges the pieces back together in order."),
        ("Divide and conquer", "A strategy that solves a problem by breaking it into smaller instances of the same problem and combining the results."),
        ("Pass", "One complete run through the list by a sorting algorithm."),
        ("Comparison", "One test of two values against each other, used as the standard measure of how much work a search or sort does."),
        ("Efficiency", "A measure of the resources an algorithm uses, usually the number of comparisons or steps and the amount of memory required."),
        ("In place", "A description of an algorithm that rearranges the data using almost no additional memory."),
    ],
    grade="""
Every question here rewards the same two moves: **trace accurately** and **justify with a trade off**.

**Traces must show the state after each step.** A merge sort question asking you to show the divide stage wants every level of splitting written out, not just the final answer. A bubble sort question asking for the list after two passes wants the list after pass one as well, because that is where the working marks live.

**Every advantage has a matching cost.** Binary search is faster but demands a sorted list. Merge sort is faster but demands more memory. Bubble sort is slow but simple and works in place. An answer that gives an advantage without acknowledging the cost is an average answer.

**Quote numbers when you can.** "Binary search would take at most 17 comparisons on 100000 records instead of up to 100000" is far stronger than "binary search is quicker", and it takes the same amount of time to write.

+ Be able to trace a binary search on a sorted list of nine items and state the number of comparisons
+ Be able to give the list after each pass of a bubble sort on a list of five values
+ Be able to draw the full divide and merge stages of a merge sort on six values
+ Be able to state the worst case number of comparisons for linear and binary search on n items
+ Be able to justify a choice of algorithm for a stated scenario in three sentences
""",
    mistakes=[
        "Using binary search on an unsorted list. It does not simply run more slowly, it returns the wrong answer.",
        "Confusing passes with comparisons. A single pass over n items makes n minus 1 comparisons.",
        "Saying merge sort is better than bubble sort in every way. Merge sort needs considerably more memory because the sub lists must be stored.",
        "Forgetting that bubble sort stops early when a pass makes no swaps, which is what makes it acceptable on nearly sorted data.",
        "Writing that linear search is 'always slow'. On a small list, or when the target is near the front, it is perfectly efficient and needs no sorting first.",
        "Splitting a merge sort list into groups of two and stopping there. The division continues until every sub list holds exactly one item.",
    ],
    quiz=[
        Q("What is the essential requirement before a binary search can be used?",
          ["The list must already be sorted", "The list must contain numbers only",
           "The list must have an even number of items", "The list must be stored in RAM"], 0,
          "Binary search decides which half to discard by assuming the order is known. On an unsorted list that assumption is false and the result is unreliable."),
        Q("A sorted list contains 1000 items. Approximately how many comparisons does a binary search need in the worst case?",
          ["10", "100", "500", "1000"], 0,
          "Each comparison halves the search area, and 2 to the power 10 is 1024, so ten comparisons are enough to cover 1000 items."),
        Q("After one complete pass of a bubble sort on [7, 3, 9, 2], the list is:",
          ["[3, 7, 2, 9]", "[2, 3, 7, 9]", "[3, 2, 7, 9]", "[7, 3, 2, 9]"], 0,
          "Compare 7 and 3 and swap, compare 7 and 9 and leave, compare 9 and 2 and swap. The largest value has bubbled to the end."),
        Q("How does merge sort know when to stop dividing the list?",
          ["When every sub list contains exactly one item",
           "When every sub list contains two items",
           "When the list is in order",
           "After a fixed number of divisions"], 0,
          "A one item list is sorted by definition, which is the base case that makes the merging stage possible."),
        Q("Which is the main disadvantage of merge sort compared with bubble sort?",
          ["It uses considerably more memory because sub lists must be stored",
           "It cannot sort text",
           "It only works on sorted lists",
           "It is slower on large lists"], 0,
          "Merge sort is much faster on large lists, but it is not in place, so it needs additional memory roughly the size of the original list."),
        Q("A programmer must search an unsorted list of 20 names once. Which is the sensible choice?",
          ["Linear search, because sorting the list first would cost more than the search saves",
           "Binary search, because it is always faster",
           "Bubble sort, because sorting is a kind of searching",
           "Merge sort, because the list is small"], 0,
          "Twenty comparisons at most is trivial, whereas sorting the list purely to enable a single binary search is wasted effort."),
        Q("What does the swapped flag in a bubble sort allow the algorithm to do?",
          ["Stop as soon as a complete pass makes no swaps",
           "Count how many items are in the list",
           "Sort the list in reverse order",
           "Use less memory than an in place sort"], 0,
          "If nothing needed swapping, everything is already in order, so continuing would be wasted work."),
        Q("Binary search is applied to [2, 5, 9, 14, 20, 27, 31] looking for 5. What is the first item examined?",
          ["14", "2", "5", "20"], 0,
          "The middle item of a seven item list is the fourth, which is 14. Only after that comparison does the algorithm move to the lower half."),
        Q("Which statement about linear search is correct?",
          ["It works on any list, whether sorted or not",
           "It requires the list to be sorted",
           "It halves the search area with each comparison",
           "It cannot be used on lists of more than 100 items"], 0,
          "Making no assumptions about order is linear search's one real advantage over binary search."),
        Q("In the worst case, how many comparisons does a linear search make on a list of n items?",
          ["n", "n divided by 2", "log to base 2 of n", "n multiplied by n"], 0,
          "The worst case is that the target is the last item or is absent, so every item must be checked."),
    ],
    exam=[
        EQ("State two advantages of a binary search over a linear search on a large sorted list.", 2, [
            MP("Fewer comparisons are needed so the search is faster",
               ["fewer comparisons", "faster", "quicker", "less time", "fewer checks"]),
            MP("Each comparison eliminates half of the remaining items",
               ["half", "halves", "eliminates", "discards", "divides the list"]),
        ], "A binary search needs far fewer comparisons than a linear search on a large list, so it finds the item much more quickly. This is because each comparison removes half of the remaining items from the search, whereas a linear search only removes one item at a time.",
           command="State"),
        EQ("Describe how a bubble sort would sort the list [5, 1, 4, 2] into ascending order.", 4, [
            MP("Adjacent pairs of items are compared",
               ["adjacent", "next to each other", "pairs", "neighbouring", "side by side"]),
            MP("They are swapped if they are in the wrong order",
               ["swap", "swapped", "exchange", "change places", "wrong order"]),
            MP("This is repeated in further passes through the list",
               ["pass", "passes", "repeat", "again", "another run"]),
            MP("The algorithm stops when a complete pass makes no swaps",
               ["no swaps", "no changes", "nothing swapped", "already sorted", "stops when"]),
        ], "The algorithm compares the first two items, 5 and 1, finds them in the wrong order and swaps them to give 1, 5, 4, 2. It then compares 5 and 4, swaps them to give 1, 4, 5, 2, and compares 5 and 2, swapping them to give 1, 4, 2, 5, which completes the first pass and leaves the largest value at the end. A second pass compares 1 and 4 with no swap, then 4 and 2 with a swap, giving 1, 2, 4, 5. A third pass makes no swaps at all, and because nothing needed to move the algorithm knows the list is sorted and stops.",
           command="Describe"),
        EQ("Explain how a merge sort sorts a list of numbers.", 4, [
            MP("The list is repeatedly divided in half",
               ["divided", "split in half", "halves", "broken down", "divide"]),
            MP("Until each sub list contains only one item, which is sorted by definition",
               ["one item", "single item", "individual", "size of one", "one element"]),
            MP("Pairs of sub lists are then merged back together",
               ["merged", "combined", "joined", "put back together", "recombined"]),
            MP("During each merge the first item of each sub list is compared and the smaller is taken first",
               ["compared", "smaller first", "smallest", "in order", "lowest value"]),
        ], "A merge sort begins by dividing the list into two halves, then dividing each of those halves again, and continuing until every sub list contains exactly one item. A list of one item is already in order, which is why this is a sensible place to stop. The algorithm then merges the sub lists back together in pairs: to merge two sorted sub lists it compares the first item of each, takes whichever is smaller and places it into the new list, then repeats until both sub lists are empty. Each merge produces a longer sorted list, and the process continues until a single sorted list containing every original item remains.",
           command="Explain"),
        EQ("A company stores 200000 customer records sorted by customer number. The records are searched several thousand times each day. Justify the use of a binary search rather than a linear search.", 4, [
            MP("The records are already sorted, so the requirement of binary search is met at no extra cost",
               ["already sorted", "sorted order", "requirement met", "no need to sort", "precondition"]),
            MP("Each comparison halves the number of records still to be searched",
               ["halves", "half", "eliminates half", "divides"]),
            MP("At most about 18 comparisons are needed instead of up to 200000",
               ["18", "eighteen", "20 comparisons", "far fewer", "200000 comparisons", "thousands fewer"]),
            MP("Because the search is repeated thousands of times a day the saving is large, reducing processing time and server load",
               ["thousands of times", "repeated", "saving", "processing time", "server", "faster response"]),
        ], "A binary search is the right choice here because the records are already held in order of customer number, so the one condition binary search imposes is already satisfied and costs nothing to meet. Each comparison in a binary search discards half of the records still under consideration, so a file of 200000 records is reduced to one in at most about eighteen comparisons, since two to the power eighteen is greater than 200000. A linear search would in the worst case examine all 200000 records to reach the same answer. Because the search runs several thousand times a day the difference is not a technicality: it is the difference between a few tens of thousands of comparisons a day and hundreds of millions, which directly affects response time for the user and the processing load on the company's servers.",
           command="Justify"),
        EQ("Compare bubble sort and merge sort, and state one situation in which each would be the better choice.", 5, [
            MP("Bubble sort repeatedly swaps adjacent items while merge sort divides and merges",
               ["adjacent", "swaps", "divide", "merge", "splits"]),
            MP("Merge sort is significantly faster on large lists",
               ["faster", "more efficient", "quicker", "fewer steps", "large lists"]),
            MP("Bubble sort uses almost no extra memory because it sorts in place",
               ["in place", "no extra memory", "little memory", "less memory", "same list"]),
            MP("Merge sort requires additional memory to store the sub lists",
               ["extra memory", "more memory", "sub lists stored", "additional space"]),
            MP("Bubble sort is better on small or nearly sorted lists, merge sort on large lists where speed matters",
               ["small list", "nearly sorted", "almost in order", "large list", "speed matters", "big data"]),
        ], "Bubble sort works by repeatedly comparing adjacent items and swapping any that are in the wrong order, continuing until a pass makes no swaps, whereas merge sort divides the list in half until each part holds one item and then merges the parts back together in order. On a large list merge sort is dramatically faster, because the number of steps grows roughly in proportion to n multiplied by the logarithm of n rather than n squared. The trade off is memory: bubble sort works in place and needs room for only a single temporary variable, while merge sort must hold the sub lists separately and so needs extra space roughly equal to the size of the original list. Bubble sort is therefore the better choice for a short list, or one that is already nearly in order, where its simplicity and low memory use matter more than raw speed, for example sorting a class of thirty test scores on a microcontroller. Merge sort is the better choice when a large volume of data must be sorted quickly and there is memory to spare, for example ordering a hundred thousand search results on a server.",
           command="Compare"),
    ],
)

# =============================================== 1.3 Truth tables and logic

T_TRUTH = Topic(
    slug="truth-tables-and-logic",
    title="Truth Tables and Logic",
    spec="1.3",
    icon="i-logic",
    minutes=24,
    blurb="NOT, AND and OR, how to build a truth table for a combined expression without losing a row, and how the same logic turns up inside program conditions.",
    fact="George Boole worked out this algebra in 1854 in a book called An Investigation of the Laws of Thought. There were no electronic computers and no transistors. It took until 1937 for Claude Shannon, then a master's student, to notice that Boole's algebra described exactly what a network of electrical switches does.",
    sections=[
        Section("The three logical operators", """
Boolean logic deals in exactly two values: **true** and **false**, usually written as **1** and **0**. Every decision a computer makes reduces to combinations of three operators.

### NOT

NOT inverts its input. True becomes false and false becomes true.

| A | NOT A |
| 0 | 1 |
| 1 | 0 |

### AND

AND gives 1 only when **both** inputs are 1. Think of two switches in series: the current only flows if both are closed.

| A | B | A AND B |
| 0 | 0 | 0 |
| 0 | 1 | 0 |
| 1 | 0 | 0 |
| 1 | 1 | 1 |

### OR

OR gives 1 when **at least one** input is 1. Two switches in parallel: current flows if either path is open.

| A | B | A OR B |
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 1 |

!key One sentence each :: AND is true only when everything is true. OR is false only when everything is false. NOT flips whatever it is given. If you can say those three from memory you can build any truth table on the paper.
"""),
        Section("Building a truth table that is right", """
A truth table lists **every possible combination** of inputs and the output each one produces. Getting one wrong is almost never a failure of understanding, it is a failure of method, so use a method.

### Step 1: work out how many rows

With n inputs there are 2 to the power n rows. One input gives 2 rows, two inputs give 4, three inputs give 8. If your table has any other number of rows it is already wrong.

### Step 2: fill the input columns in the standard pattern

For three inputs the reliable pattern is: the last column alternates 0, 1, 0, 1 and so on; the middle column alternates in pairs, 0, 0, 1, 1; the first column alternates in fours, 0, 0, 0, 0 then 1, 1, 1, 1. Doing it this way guarantees you produce all eight combinations and never repeat one.

### Step 3: add a working column for each bracket

Do not try to evaluate a combined expression in your head. Give every sub expression its own column and fill it in before you touch the final answer.

Here is `(A AND B) OR (NOT C)` done properly.

| A | B | C | A AND B | NOT C | (A AND B) OR (NOT C) |
| 0 | 0 | 0 | 0 | 1 | 1 |
| 0 | 0 | 1 | 0 | 0 | 0 |
| 0 | 1 | 0 | 0 | 1 | 1 |
| 0 | 1 | 1 | 0 | 0 | 0 |
| 1 | 0 | 0 | 0 | 1 | 1 |
| 1 | 0 | 1 | 0 | 0 | 0 |
| 1 | 1 | 0 | 1 | 1 | 1 |
| 1 | 1 | 1 | 1 | 0 | 1 |

The working columns cost about thirty seconds and remove almost every chance of an error. Look at the last row: the AND is true, so the OR is true even though NOT C is false. That is the row people get wrong when they rush.

!warn Brackets change the answer :: `A AND (B OR C)` and `(A AND B) OR C` are different expressions. Set A to 0, B to 0 and C to 1, and the first gives 0 while the second gives 1. Always evaluate the brackets first.
"""),
        Section("Logic in real systems and real programs", """
### Reading a scenario into an expression

Exam questions describe a system in English and expect an expression or a truth table. Translate one clause at a time.

*"A fire door unlocks if the fire alarm is sounding, or if the manual release is pressed and the building is not in lockdown."*

- Let A be "fire alarm sounding", M be "manual release pressed", L be "building in lockdown".
- Unlock = `A OR (M AND NOT L)`.

Check it against sense: with the alarm sounding the door unlocks whatever else is true, which is what a fire door must do. With the manual release pressed during a lockdown it stays locked, because `NOT L` is 0. The expression behaves like the description, so it is right.

### The same logic inside a program

Program conditions are Boolean expressions, and every rule above applies to them unchanged.

```python
if age >= 13 and (has_consent or is_supervised):
    allow_access()
```

That condition is `A AND (B OR C)`. Removing the brackets changes its meaning completely: `age >= 13 and has_consent or is_supervised` would let an unsupervised infant in, because `and` binds more tightly than `or`, so it reads as `(A AND B) OR C`.

### Common patterns worth recognising

| English | Expression |
| Both conditions must hold | A AND B |
| Either condition will do | A OR B |
| Neither condition holds | NOT A AND NOT B |
| Exactly one of the two holds | (A OR B) AND NOT (A AND B) |
| The condition must not hold | NOT A |

!exam Show the working columns :: In a truth table question the marks are usually awarded per column, not per table. An intermediate column that is correct earns its mark even if the final column contains a slip.
"""),
    ],
    keyterms=[
        ("Boolean", "A data type or value that can only be true or false, often represented as 1 and 0."),
        ("Logical operator", "A symbol or keyword such as AND, OR or NOT that combines or inverts Boolean values."),
        ("AND", "A logical operation whose output is true only when every input is true."),
        ("OR", "A logical operation whose output is true when at least one input is true."),
        ("NOT", "A logical operation that inverts its input, turning true into false and false into true."),
        ("Truth table", "A table listing every possible combination of inputs to a logical expression together with the resulting output."),
        ("Logic gate", "An electronic component that performs a logical operation on one or more binary inputs and produces one binary output."),
        ("Condition", "A Boolean expression tested by a program to decide which instructions to execute next."),
    ],
    grade="""
Truth table marks are lost to carelessness rather than to ignorance, so the top grade here is a matter of discipline.

**Count your rows before you write anything.** Two inputs is four rows, three inputs is eight. Half the errors in this topic are a missing combination.

**Give every bracket its own column.** Evaluating `(A AND B) OR NOT C` in your head across eight rows is a guaranteed slip, and the working columns are separately creditable.

**Translate scenarios one clause at a time.** Define your letters explicitly, write the expression, then test it against two or three sentences from the question to check it behaves as described. Stating what each letter stands for takes one line and often earns a mark on its own.

**Know the effect of the brackets.** Being able to say that `A AND (B OR C)` differs from `(A AND B) OR C`, and give a set of inputs that proves it, is the kind of specific detail that separates the top band.

+ Be able to write the truth tables for NOT, AND and OR from memory in under a minute
+ Be able to produce all eight input combinations for three inputs in the standard order without thinking
+ Be able to build a truth table for an expression with two operators and brackets, with working columns
+ Be able to turn a described system such as an alarm or a door lock into a Boolean expression
""",
    mistakes=[
        "Producing six or seven rows for a three input table. There are always exactly eight.",
        "Treating OR as meaning one or the other but not both. In Boolean logic OR is true when both inputs are true as well.",
        "Ignoring brackets and evaluating an expression left to right, which changes the answer.",
        "Applying NOT to the whole expression when it only applies to one variable, or the other way round.",
        "Writing an expression without saying what each letter stands for, so the examiner cannot tell whether it matches the scenario.",
        "Assuming AND and OR mean in code what they mean in casual English. 'Under 13 or over 65' is an OR, but 'between 13 and 65' is two conditions joined by AND.",
    ],
    quiz=[
        Q("What is the output of 1 AND 0?",
          ["0", "1", "It depends on the other inputs", "Both 0 and 1"], 0,
          "AND produces 1 only when every input is 1, so a single 0 forces the output to 0."),
        Q("How many rows does a truth table with three inputs have?",
          ["8", "3", "6", "9"], 0,
          "Each input can be 0 or 1, so the number of combinations is 2 to the power 3, which is 8."),
        Q("What is the output of NOT (1 OR 0)?",
          ["0", "1", "Undefined", "It depends on NOT being applied first"], 0,
          "The bracket is evaluated first and 1 OR 0 gives 1, then NOT inverts that to 0."),
        Q("Which expression is true only when both A and B are false?",
          ["NOT A AND NOT B", "NOT A OR NOT B", "A AND B", "NOT (A AND B)"], 0,
          "Both inversions must be true at once, which happens only when both original values are false."),
        Q("For A equals 0, B equals 0 and C equals 1, what is the value of (A AND B) OR C?",
          ["1", "0", "It cannot be evaluated", "2"], 0,
          "A AND B gives 0, but C is 1, and OR is true whenever at least one input is true."),
        Q("Which statement about the OR operation is correct?",
          ["It outputs 1 when one or both inputs are 1",
           "It outputs 1 only when exactly one input is 1",
           "It outputs 1 only when both inputs are 1",
           "It outputs 0 when either input is 1"], 0,
          "Boolean OR is inclusive, so it is true when both inputs are true as well as when only one is."),
        Q("A door opens if a valid card is presented AND the door is not locked down. Which expression is correct?",
          ["card AND NOT lockdown", "card OR NOT lockdown", "NOT (card AND lockdown)", "card AND lockdown"], 0,
          "Both requirements must hold at once, and the second requirement is the inverse of lockdown, so NOT is applied to that variable alone."),
        Q("Why is a working column added when building a truth table for (A OR B) AND NOT C?",
          ["It records the value of each sub expression so the final column is less error prone",
           "It is required by the specification for every table",
           "It reduces the number of rows needed",
           "It converts the expression to binary"], 0,
          "Evaluating a sub expression once per row and writing it down is far more reliable than holding the whole expression in your head, and the columns earn marks in their own right."),
        Q("In Python, why does the condition age > 12 and consent or supervised behave differently from age > 12 and (consent or supervised)?",
          ["Because and is evaluated before or, so the first reads as (age > 12 and consent) or supervised",
           "Because Python evaluates conditions from right to left",
           "Because or is not a valid operator without brackets",
           "Because and can only be used once in a condition"], 0,
          "Operator precedence makes and bind more tightly than or, so without brackets the grouping is not the one the programmer intended."),
        Q("Which set of inputs makes A AND (B OR C) different in value from (A AND B) OR C?",
          ["A equals 0, B equals 0, C equals 1", "A equals 1, B equals 1, C equals 1",
           "A equals 0, B equals 0, C equals 0", "A equals 1, B equals 0, C equals 0"], 0,
          "The first expression gives 0 because A is 0, while the second gives 1 because C is 1, which proves the brackets matter."),
    ],
    exam=[
        EQ("Complete a truth table for the expression A AND NOT B, and state for which inputs the output is 1.", 2, [
            MP("Shows all four combinations of A and B",
               ["four rows", "00 01 10 11", "all combinations", "four combinations"]),
            MP("Identifies that the output is 1 only when A is 1 and B is 0",
               ["a is 1 and b is 0", "1 and 0", "only when a true b false", "a true b false"]),
        ], "The table has four rows because there are two inputs. When A is 0 and B is 0 the output is 0, when A is 0 and B is 1 the output is 0, when A is 1 and B is 0 the output is 1, and when A is 1 and B is 1 the output is 0. The output is therefore 1 for exactly one combination, where A is 1 and B is 0, because AND requires both of its inputs to be true and NOT B is only true when B is false.",
           command="Calculate"),
        EQ("Explain the difference between the AND and the OR logical operations.", 3, [
            MP("AND outputs true only when all of its inputs are true",
               ["and requires both", "all inputs true", "only when both", "both must be"]),
            MP("OR outputs true when at least one of its inputs is true",
               ["at least one", "either", "one or more", "or requires one"]),
            MP("OR is therefore true in more cases, and is only false when every input is false",
               ["only false when both false", "more cases", "three of four", "false when all false"]),
        ], "AND produces an output of true only when every one of its inputs is true, so with two inputs it is true in just one of the four possible combinations. OR produces an output of true whenever at least one of its inputs is true, including the case where both are true, so with two inputs it is true in three of the four combinations. Put the other way round, AND is false as soon as any input is false, while OR is false only when every input is false.",
           command="Explain"),
        EQ("A greenhouse system opens a vent if the temperature is above 28 degrees, or if the humidity is above 80 per cent and the fan is not running. Write a Boolean expression for this system, defining each variable you use.", 4, [
            MP("Defines a variable for each condition, such as T for high temperature, H for high humidity and F for the fan running",
               ["let t", "t represents", "variable for temperature", "h is humidity", "f is fan", "define"]),
            MP("Uses AND to combine the humidity condition with the fan condition",
               ["h and", "and not f", "and", "both humidity and fan"]),
            MP("Applies NOT to the fan variable only",
               ["not f", "not fan", "fan is not running", "inverts fan"]),
            MP("Uses OR to combine the temperature condition with the humidity and fan condition, with correct bracketing",
               ["t or", "or", "brackets", "t or (h and not f)"]),
        ], "Let T represent the temperature being above 28 degrees, H represent the humidity being above 80 per cent, and F represent the fan running. The vent opens when T is true on its own, or when H is true at the same time as F is false. The expression is therefore vent equals T OR (H AND NOT F). The brackets are essential, because they keep the humidity and fan conditions together as a single requirement: without them the expression would open the vent whenever the humidity was high, regardless of the fan.",
           command="Write"),
        EQ("Complete the truth table for the expression (A OR B) AND NOT C and describe the pattern in the output.", 4, [
            MP("Recognises that three inputs give eight rows",
               ["eight rows", "8 rows", "2 to the power 3", "eight combinations"]),
            MP("Evaluates A OR B correctly as true whenever A or B is 1",
               ["a or b", "true when either", "at least one of a b"]),
            MP("Evaluates NOT C correctly as the inverse of C",
               ["not c", "inverse of c", "opposite", "1 when c is 0"]),
            MP("States that the output is 1 only when C is 0 and at least one of A and B is 1",
               ["c is 0", "c false", "and a or b is 1", "at least one of a and b"]),
        ], "There are three inputs so the table has eight rows. The column for A OR B is 0 only in the two rows where both A and B are 0, and 1 in the other six. The column for NOT C is 1 in the four rows where C is 0 and 0 in the four where C is 1. The final column is the AND of those two working columns, so it is 1 only where both are 1. That gives an output of 1 in exactly three rows: A equals 0 with B equals 1 and C equals 0, A equals 1 with B equals 0 and C equals 0, and A equals 1 with B equals 1 and C equals 0. In words, the output is true only when C is false and at least one of A and B is true.",
           command="Calculate"),
        EQ("A student writes the condition if age > 65 or age < 16 and has_pass: in a program that should give a discount to anyone over 65, and to anyone under 16 who holds a pass. Explain why this condition does not do what the student intended, and how to correct it.", 5, [
            MP("Identifies that AND is evaluated before OR",
               ["and before or", "precedence", "and binds", "evaluated first", "priority"]),
            MP("So the condition is treated as age > 65 OR (age < 16 AND has_pass)",
               ["age > 65 or", "grouped as", "treated as", "interpreted as"]),
            MP("States that this actually matches the intention for the under 16 case",
               ["under 16 needs a pass", "pass required", "matches", "correct for under 16"]),
            MP("Notes the risk that a reader cannot see the grouping, so the code is easy to misread and to break when edited",
               ["hard to read", "misread", "unclear", "maintain", "future changes", "ambiguous"]),
            MP("Corrects it by adding brackets, for example if age > 65 or (age < 16 and has_pass)",
               ["brackets", "parentheses", "add brackets", "or (age < 16 and has_pass)"]),
        ], "In Python the AND operator has higher precedence than OR, so the condition is evaluated as age greater than 65, OR the pair age less than 16 AND has_pass taken together. In this particular case that grouping happens to match what the student wanted, since a person under 16 does need a pass while a person over 65 does not. The problem is that nothing in the code says so. Anyone reading the line has to know the precedence rules to work out the grouping, and a small future edit, such as adding a third condition, can silently change the meaning and introduce a fault that produces no error message. The correction is to make the grouping explicit by writing if age > 65 or (age < 16 and has_pass), which behaves identically but states the intention on the page rather than leaving it to be inferred.",
           command="Explain"),
    ],
)

# ================================================ 2.1 Binary and hexadecimal

T_BINHEX = Topic(
    slug="binary-and-hexadecimal",
    title="Binary and Hexadecimal",
    spec="2.1",
    icon="i-binary",
    minutes=28,
    blurb="Why a computer has only two digits to work with, how to convert in both directions without a calculator, and what hexadecimal is actually for.",
    fact="A single hexadecimal digit represents exactly four bits, which is why hex is used for colour codes and MAC addresses. The colour written as FF8000 is 11111111 10000000 00000000 in binary, which is why nobody writes colours in binary.",
    sections=[
        Section("Why binary", """
A computer stores and processes everything as **binary**, a number system with only two digits, 0 and 1. This is not a design preference, it is a consequence of the hardware.

Inside a computer, data is held as an electrical state: a transistor conducting or not conducting, a capacitor charged or discharged, a region of a disc magnetised one way or the other. Each of those is a **two state** device, so it can represent exactly two values. Call them 0 and 1 and you have binary.

### Why not ten states instead

You could in principle build a component with ten distinguishable voltage levels and use denary directly. It would be a bad idea. Two states can be told apart even when the signal is noisy or the voltage drifts, because anything below a threshold reads as 0 and anything above it reads as 1. Ten states would need nine thresholds packed into the same voltage range, so a small amount of electrical interference would produce a wrong value. Binary is used because it is **reliable**, cheap to manufacture and easy to design circuits for.

### The vocabulary

- A **bit** is a single binary digit, a 0 or a 1.
- A **nibble** is 4 bits.
- A **byte** is 8 bits.

An 8 bit binary number can represent 2 to the power 8, that is 256, different values, so as an unsigned integer it covers 0 to 255.

!key The exam sentence :: Computers use binary because the components they are built from have two stable states, on and off, and binary digits map directly onto those states, which makes the circuits reliable and simple.
"""),
        Section("Converting between denary and binary", """
### Place values

An 8 bit binary number has these place values, each double the one to its right:

| 128 | 64 | 32 | 16 | 8 | 4 | 2 | 1 |
| 1 | 1 | 0 | 0 | 1 | 0 | 1 | 0 |

### Binary to denary

Add up the place values wherever there is a 1. For `11001010`: 128 + 64 + 8 + 2 = **202**.

Write the place values above the digits before you start. Every mark lost on this question is lost by someone who tried to do it from memory and slipped a column.

### Denary to binary

Work from the **largest** place value down, asking one question at a time: does this fit into what is left?

Converting 202:

| Place value | Does it fit into what remains? | Bit | Remaining |
| 128 | 128 fits into 202 | 1 | 74 |
| 64 | 64 fits into 74 | 1 | 10 |
| 32 | 32 does not fit into 10 | 0 | 10 |
| 16 | 16 does not fit into 10 | 0 | 10 |
| 8 | 8 fits into 10 | 1 | 2 |
| 4 | 4 does not fit into 2 | 0 | 2 |
| 2 | 2 fits into 2 | 1 | 0 |
| 1 | 1 does not fit into 0 | 0 | 0 |

The answer is `11001010`. The remainder reaching zero exactly is your check that you have not made an error.

!warn Pad to eight bits :: If the question says 8 bit, write all eight digits. `1010` is a correct value but an incomplete answer; write `00001010`.
"""),
        Section("Hexadecimal", """
**Hexadecimal**, or hex, is base 16. It uses the digits 0 to 9 and then the letters A to F for the values 10 to 15.

| Denary | 10 | 11 | 12 | 13 | 14 | 15 |
| Hex | A | B | C | D | E | F |

### Why it exists

Hex is not used because computers understand it. They do not: everything is still binary underneath. Hex exists because **people** make mistakes reading long strings of 0s and 1s.

The number `11001010` is easy to mistype, hard to say out loud and difficult to compare with a similar value at a glance. The same number in hex is `CA`, two characters. The conversion works because one hex digit represents exactly four bits, so any binary number can be split into nibbles and translated straight across with no arithmetic.

This is why hex is used for MAC addresses, colour codes in web design, memory addresses and machine code listings.

### Binary to hex

Split into nibbles of four bits from the right, then convert each nibble.

`11001010` splits into `1100` and `1010`. `1100` is 8 + 4 = 12, which is C. `1010` is 8 + 2 = 10, which is A. The answer is **CA**.

### Hex to binary

Convert each digit into four bits. `2F` becomes `0010` and `1111`, so `00101111`.

### Hex to denary

Multiply the left digit by 16 and add the right digit. `CA` is (12 multiplied by 16) plus 10, which is 192 + 10 = **202**. `2F` is (2 multiplied by 16) plus 15 = **47**.

### Denary to hex

The safe route is through binary: convert to 8 bit binary, split into two nibbles, convert each. Converting 181 directly is error prone, but 181 is `10110101`, which splits into `1011` and `0101`, giving **B5**.

!exam Route your conversions through binary :: In an exam, denary to hex and hex to denary are both quicker and safer via binary, because you already know the place values cold and there is no multiplication to slip up on.
"""),
    ],
    keyterms=[
        ("Binary", "A number system with base 2 that uses only the digits 0 and 1."),
        ("Bit", "A single binary digit, either 0 or 1, and the smallest unit of data a computer can store."),
        ("Nibble", "A group of four bits, which is exactly the amount represented by one hexadecimal digit."),
        ("Byte", "A group of eight bits, able to represent 256 different values."),
        ("Denary", "The everyday number system with base 10, using the digits 0 to 9."),
        ("Hexadecimal", "A number system with base 16 that uses the digits 0 to 9 and the letters A to F."),
        ("Place value", "The value a digit represents because of its position, doubling with each move to the left in binary."),
        ("Unsigned integer", "A whole number with no sign bit, so an 8 bit unsigned integer represents values from 0 to 255."),
        ("Most significant bit", "The leftmost bit of a binary number, which carries the largest place value."),
    ],
    grade="""
Conversions are marked right or wrong, so accuracy under pressure is the whole skill.

**Write the place values down every time.** Every single time, even when you are sure. It costs four seconds and it is the difference between 202 and 234.

**Check your answer by converting it back.** If you convert 181 to `10110101`, add up 128 + 32 + 16 + 4 + 1 and confirm you get 181. Two conversions take less than a minute and turn a guess into a certainty.

**Explain hexadecimal in terms of people, not machines.** The reason hex exists is that humans read and write it more reliably than binary, and one hex digit maps to exactly four bits so the translation needs no calculation. An answer claiming that computers use hex, or that hex saves storage space, is wrong: the value in memory is identical.

**Be precise about ranges.** An 8 bit unsigned value covers 0 to 255, which is 256 different values. Saying "up to 256" is the classic slip.

+ Be able to convert any denary value from 0 to 255 into 8 bit binary in under thirty seconds
+ Be able to convert 8 bit binary to denary and to hexadecimal
+ Be able to convert two hexadecimal digits to binary and to denary
+ Be able to give three real uses of hexadecimal and explain why hex rather than binary is used there
""",
    mistakes=[
        "Reading binary place values from the left as 1, 2, 4, 8. The place values increase from right to left, so the leftmost bit of a byte is 128.",
        "Giving a binary answer with fewer than eight bits when the question specifies an 8 bit number.",
        "Saying computers use hexadecimal. Computers use binary. Hex is a shorthand for people reading and writing binary values.",
        "Claiming hexadecimal saves memory. CA and 11001010 occupy exactly the same eight bits in the machine.",
        "Saying an 8 bit unsigned number can store values up to 256. It stores 256 different values, from 0 to 255.",
        "Splitting binary into nibbles from the left rather than the right, which gives the wrong answer whenever the number has fewer than eight digits.",
    ],
    quiz=[
        Q("What is 11001010 in denary?",
          ["202", "212", "198", "234"], 0,
          "Adding the place values where a 1 appears gives 128 + 64 + 8 + 2, which is 202."),
        Q("What is 181 in 8 bit binary?",
          ["10110101", "10110011", "11010101", "10011101"], 0,
          "128 fits leaving 53, 32 fits leaving 21, 16 fits leaving 5, 4 fits leaving 1, and 1 fits exactly, giving 10110101."),
        Q("Why do computers use binary rather than denary?",
          ["Their components have two stable states, which map directly onto 0 and 1",
           "Binary numbers take up less storage than denary numbers",
           "Binary is easier for people to read",
           "Denary cannot represent negative numbers"], 0,
          "Transistors and other components are two state devices, and telling two states apart is far more reliable than telling ten apart."),
        Q("How many bits are represented by a single hexadecimal digit?",
          ["4", "2", "8", "16"], 0,
          "One hex digit covers the values 0 to 15, which is exactly what four bits can represent, so the translation needs no arithmetic."),
        Q("What is the hexadecimal equivalent of the binary number 10110101?",
          ["B5", "5B", "A5", "B6"], 0,
          "Split into 1011 and 0101. 1011 is 11, which is B, and 0101 is 5, giving B5."),
        Q("What is 2F in denary?",
          ["47", "31", "215", "35"], 0,
          "The left digit is worth 2 multiplied by 16, which is 32, and F is 15, so the total is 47."),
        Q("How many different values can be represented by one byte?",
          ["256", "255", "128", "64"], 0,
          "Eight bits give 2 to the power 8 combinations, which is 256 values, running from 0 to 255."),
        Q("Which statement about hexadecimal is correct?",
          ["It is used because people read and write it more reliably than long binary strings",
           "It allows a computer to store more data in the same space",
           "It is the number system processors work in",
           "It can represent values that binary cannot"], 0,
          "Hex is a human convenience. The stored value is identical binary either way."),
        Q("What is the largest value that can be stored in a nibble?",
          ["15", "16", "8", "255"], 0,
          "Four bits have place values 8, 4, 2 and 1, and 1111 adds up to 15."),
        Q("Which of these is a genuine use of hexadecimal?",
          ["Writing colour values in web pages, such as FF8000",
           "Storing text more efficiently than ASCII",
           "Encrypting data so it cannot be read",
           "Compressing images without losing quality"], 0,
          "Colour codes, MAC addresses and memory addresses are all written in hex because it is a compact and readable form of the underlying binary."),
    ],
    exam=[
        EQ("Convert the denary number 156 into an 8 bit binary number. Show your working.", 2, [
            MP("Correct binary answer 10011100",
               ["10011100", "1001 1100"]),
            MP("Working shown using place values, subtracting 128, 16, 8 and 4",
               ["128", "place value", "16 8 4", "subtract", "remainder"]),
        ], "Starting from the highest place value, 128 fits into 156 and leaves 28, so the first bit is 1. 64 does not fit into 28 and 32 does not fit into 28, so the next two bits are 0. 16 fits into 28 and leaves 12, 8 fits into 12 and leaves 4, and 4 fits into 4 and leaves 0, so those three bits are 1. The final two place values, 2 and 1, do not fit into 0, so both are 0. The answer is 10011100.",
           command="Calculate"),
        EQ("Explain why computers represent all data in binary.", 3, [
            MP("Computer components such as transistors have two states, on and off",
               ["two states", "on and off", "transistor", "switch", "high and low"]),
            MP("These two states map directly onto the digits 0 and 1",
               ["0 and 1", "represent", "maps onto", "correspond"]),
            MP("Two states can be distinguished reliably even with electrical noise, so circuits are simpler and less error prone",
               ["reliable", "noise", "errors", "simpler circuits", "cheaper", "distinguish"]),
        ], "The components a computer is built from, such as transistors and memory cells, are two state devices: they are either conducting or not conducting, charged or discharged. Those two states map directly onto the two digits of binary, 0 and 1, so no translation is needed between the data and the hardware holding it. Two states are used rather than ten because a circuit only has to distinguish between a voltage above a threshold and one below it, which remains reliable even when the signal is affected by electrical noise or by voltage drifting slightly, and circuits that only have to make that one distinction are simpler and cheaper to manufacture.",
           command="Explain"),
        EQ("Convert the binary number 11100101 into hexadecimal and into denary.", 4, [
            MP("Splits the binary number into the nibbles 1110 and 0101",
               ["1110", "0101", "nibbles", "four bits", "split"]),
            MP("Correctly gives the hexadecimal answer E5",
               ["e5"]),
            MP("Adds the place values 128, 64, 32, 4 and 1",
               ["128", "64", "32", "place values", "adds"]),
            MP("Correctly gives the denary answer 229",
               ["229"]),
        ], "To convert to hexadecimal the byte is split into two nibbles from the right, giving 1110 and 0101. The nibble 1110 is 8 plus 4 plus 2, which is 14, and 14 is written as E in hexadecimal. The nibble 0101 is 4 plus 1, which is 5. The hexadecimal value is therefore E5. To convert to denary the place values where a 1 appears are added together: 128 plus 64 plus 32 plus 4 plus 1, which gives 229. This can be checked against the hexadecimal answer, since E is 14 and 14 multiplied by 16 is 224, and 224 plus 5 is 229.",
           command="Calculate"),
        EQ("Explain why hexadecimal is used by programmers when working with binary data.", 4, [
            MP("One hexadecimal digit represents exactly four bits",
               ["four bits", "one digit four", "nibble", "exactly four"]),
            MP("So binary values can be written far more briefly, two digits instead of eight",
               ["shorter", "briefer", "two digits", "compact", "fewer characters"]),
            MP("Shorter values are easier for people to read, write, remember and compare, so fewer mistakes are made",
               ["easier to read", "fewer errors", "less error prone", "remember", "type", "mistakes"]),
            MP("Conversion between hexadecimal and binary is direct and requires no calculation",
               ["direct conversion", "no calculation", "straightforward", "simple to convert", "maps directly"]),
        ], "Hexadecimal is base 16, and because 16 is 2 to the power 4, one hexadecimal digit represents exactly four bits. That relationship means a byte can always be written as two hexadecimal digits, so a value such as 11001010 becomes simply CA. Programmers work with binary values constantly, in memory addresses, colour codes and MAC addresses, and long strings of ones and zeros are extremely easy to misread, mistype or lose your place in. Writing the same value in a quarter of the characters makes it far easier to read aloud, note down and compare with another value. The conversion is also completely mechanical: each group of four bits translates straight into one hexadecimal digit with no arithmetic at all, so nothing is lost or risked in moving between the two.",
           command="Explain"),
        EQ("A student claims that storing a value in hexadecimal saves memory compared with storing it in binary. Explain why this claim is incorrect.", 3, [
            MP("All data is stored in the computer as binary regardless of how it is written down",
               ["stored as binary", "always binary", "computer stores binary", "underlying"]),
            MP("Hexadecimal is a way of writing or displaying a value for people, not a way of storing it",
               ["for people", "notation", "representation", "display", "shorthand", "written"]),
            MP("The value CA and the value 11001010 occupy the same eight bits in memory",
               ["same eight bits", "same amount", "identical", "same space", "one byte either way"]),
        ], "The claim is incorrect because every value inside a computer is held as binary, whatever notation a person uses when writing it down. Hexadecimal is a human readable shorthand for binary, not a separate storage format, so writing a byte as CA rather than as 11001010 changes nothing about the memory the value occupies. Both notations describe the same eight bits, and those eight bits take up one byte of memory in either case. What hexadecimal saves is not space in the machine but effort and errors for the person reading and writing the value.",
           command="Explain"),
    ],
)
