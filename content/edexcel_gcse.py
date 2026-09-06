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


# ============================================ 2.2 data representation

T_DATAREP = Topic(
    slug="representing-text-images-and-sound",
    title="Representing Text, Images and Sound",
    spec="2.2",
    icon="i-palette",
    minutes=30,
    blurb="Character sets, bitmap images and sampled sound, and every calculation Edexcel can ask you to do on each, with the conversions set out step by step.",
    fact="The reason a screenshot of a paragraph of text is hundreds of times larger than the text itself is that the image stores a colour for every pixel, including all the white space, while the text stores one code per character.",
    sections=[
        Section("Representing text", """
A computer stores only numbers, so text is turned into numbers using a **character set**: an agreed table giving every character a unique binary code.

### ASCII

**ASCII** uses 7 bits, giving 2 to the power 7, which is 128 codes. That covers the English alphabet in both cases, the digits, punctuation and control characters such as carriage return. Extended ASCII uses 8 bits and has 256 codes.

The codes are assigned in order, which is useful:

- `'A'` is 65, so `'B'` is 66 and `'Z'` is 90.
- `'a'` is 97, so lower case is always upper case plus 32.
- `'0'` is 48, so the value of a digit character is its code minus 48.

!warn The character '7' is not the number 7 :: '7' is stored as the code 55. That is why anything typed at a keyboard must be converted before it can be used in arithmetic.

### Unicode

ASCII has no codes for Greek, Arabic, Chinese, Hindi or emoji. **Unicode** uses more bits per character and has room for over a million codes, which covers every writing system in current use.

The trade is storage: characters outside the basic set need more than one byte. The first 128 Unicode codes are deliberately identical to ASCII, so plain English text costs the same in both and every existing ASCII file is already valid Unicode.

### Calculating the size of a text file

**size in bits = number of characters x bits per character**

A 500 character message in 8 bit extended ASCII is 500 times 8, which is 4000 bits, or 500 bytes. Spaces and punctuation are characters and must be counted.
"""),
        Section("Representing images", """
A **bitmap** image is stored as a grid of **pixels**, with a binary value recorded for the colour of every pixel.

**Resolution** is the number of pixels, given as width by height. More pixels means more detail and proportionally more data.

**Colour depth** is the number of bits used per pixel, and it decides how many colours a pixel can be:

| Colour depth | Colours |
| 1 bit | 2 |
| 4 bit | 16 |
| 8 bit | 256 |
| 24 bit | 16 777 216 |

**Metadata** is data about the file: width, height, colour depth, format, date. Without the width, software cannot know where each row of pixels ends, so the picture cannot be reconstructed at all.

### Calculating image file size

**size in bits = width x height x colour depth**

An image 1024 by 768 at 24 bit colour:

```text
pixels        = 1024 x 768           = 786 432
size in bits  = 786 432 x 24         = 18 874 368 bits
size in bytes = 18 874 368 / 8       = 2 359 296 bytes
size in KiB   = 2 359 296 / 1024     = 2 304 KiB
size in MiB   = 2 304 / 1024         = 2.25 MiB
```

!key Edexcel uses binary prefixes :: A kibibyte is 1024 bytes, a mebibyte is 1024 kibibytes. Dividing by 1000 will not match the mark scheme.
"""),
        Section("Representing sound", """
Sound is an **analogue** wave: continuous, with a value at every instant. A computer cannot store something continuous, so the wave is **sampled**, meaning its height is measured at regular intervals and each measurement is stored as a binary number.

The result is a staircase that follows the wave without exactly matching it. How close it gets depends on two things.

**Sample rate** is how many samples are taken each second, in hertz. A higher rate means narrower steps, so rapid changes and higher frequencies survive. CD audio uses 44100 Hz.

**Bit depth**, also called sample resolution, is how many bits store each sample. Eight bits gives 256 possible levels, sixteen gives 65536. Every measured height is rounded to the nearest available level, so more bits means less rounding and a more faithful recording.

### Calculating sound file size

**size in bits = sample rate x bit depth x seconds x channels**

A 2 minute stereo recording at 44100 Hz and 16 bits:

```text
seconds       = 2 x 60                        = 120
size in bits  = 44100 x 16 x 120 x 2          = 169 344 000 bits
size in bytes = 169 344 000 / 8               = 21 168 000 bytes
size in KiB   = 21 168 000 / 1024             = 20 671.875 KiB
size in MiB   = 20 671.875 / 1024             ≈ 20.2 MiB
```

!exam Convert minutes to seconds first :: Write it as the first line of your working. It is the single most common lost mark on this question.
"""),
    ],
    keyterms=[
        ("Character set", "An agreed table giving every character a unique binary code."),
        ("ASCII", "A 7 bit character set with 128 codes covering English text and control characters."),
        ("Unicode", "A character set using more bits per character, covering over a million characters from every writing system."),
        ("Bitmap", "An image stored as a grid of pixels with a colour value recorded for each."),
        ("Resolution", "The number of pixels in an image, given as width by height."),
        ("Colour depth", "The number of bits used to store the colour of each pixel."),
        ("Metadata", "Data about a file, such as its width, height, colour depth and date."),
        ("Sampling", "Measuring an analogue wave at regular intervals and storing each measurement as a number."),
        ("Sample rate", "The number of samples taken per second, measured in hertz."),
        ("Bit depth", "The number of bits used to store each individual sample."),
        ("Kibibyte", "1024 bytes, the binary prefix unit Edexcel uses."),
    ],
    grade="""
Most of the marks here are arithmetic, and most of the lost marks are conversions.

**Label your units as you go.** Write "bits" and "bytes" beside each line of working. It makes a missing division by eight obvious to you before it is obvious to the examiner.

**Divide by 1024, not 1000.** Edexcel uses kibibytes and mebibytes. This is a genuine board difference and it changes your answer.

**Give the mechanism, not the label.** "Increasing colour depth adds bits to every single pixel, so the file grows in proportion" earns more than "more colours makes the file bigger".

**Name both sound controls with their separate effects.** Sample rate is detail across time, bit depth is detail in amplitude, and questions expect you to know which is which.
""",
    mistakes=[
        "Dividing by 1000 rather than 1024. Edexcel uses binary prefixes.",
        "Leaving the duration in minutes in a sound calculation.",
        "Forgetting to multiply by two for a stereo recording.",
        "Saying ASCII has 256 characters. Standard ASCII is 7 bit with 128.",
        "Treating a digit character as its numeric value without converting it.",
    ],
    quiz=[
        Q("How many characters can a 7 bit character set represent?", ["128", "127", "256", "64"], 0,
          "Seven bits give 2 to the power 7, which is 128 combinations numbered 0 to 127."),
        Q("If 'A' is 65 and 'a' is 97, what is the code for 'c'?", ["99", "67", "98", "100"], 0,
          "Lower case a is 97, so b is 98 and c is 99."),
        Q("What does colour depth control?", ["How many different colours each pixel can be", "How many pixels the image has", "The physical size of the image", "The file format"], 0,
          "Colour depth is the number of bits per pixel, which determines the number of possible colours for each pixel."),
        Q("An image is 500 by 400 pixels at 8 bit colour depth. What is its size in bits?", ["1600000", "200000", "160000", "3200000"], 0,
          "There are 500 times 400, which is 200000 pixels, and each needs 8 bits, giving 1600000 bits."),
        Q("Using Edexcel's units, how many bytes are in 2 kibibytes?", ["2048", "2000", "1024", "16000"], 0,
          "A kibibyte is 1024 bytes, so two kibibytes is 2048 bytes."),
        Q("What does a higher sample rate improve?", ["How closely the recording follows changes in the wave over time", "How precisely each individual height is stored", "The number of channels recorded", "The metadata stored with the file"], 0,
          "The rate is how often you measure, so raising it captures faster changes. Precision per measurement is bit depth, a separate control."),
        Q("A 30 second mono recording at 22050 Hz with 8 bit depth is how many bits?", ["5292000", "10584000", "2646000", "661500"], 0,
          "22050 times 8 times 30 times 1 gives 5292000 bits."),
        Q("Why must an image file store its width as metadata?", ["Without it, software cannot know where each row of pixels ends", "It reduces the file size", "It stores the average colour", "It is needed for compression"], 0,
          "The pixel values are one long sequence. The width is what folds that sequence back into a rectangle of the right shape."),
        Q("What is the main disadvantage of Unicode compared with ASCII?", ["Characters outside the basic set need more bits, so files can be larger", "It cannot represent English", "It is no longer supported", "It cannot be used for web pages"], 0,
          "More available codes means more bits per character for anything beyond the basic Latin set, increasing storage and transmission size."),
        Q("Doubling both the width and height of an image has what effect on file size?", ["It becomes four times larger", "It doubles", "It stays the same", "It becomes eight times larger"], 0,
          "Twice the width and twice the height gives four times as many pixels, and each still needs the same number of bits."),
    ],
    exam=[
        EQ("State what is meant by the term metadata in relation to an image file.", 2, [
            MP("Data about the file rather than the picture content itself", ["about the file", "data about data", "information about", "not the picture"]),
            MP("Gives an example such as width, height, colour depth or date", ["width", "height", "colour depth", "resolution", "date", "format"]),
        ], "Metadata is data stored in a file that describes the file itself rather than forming part of the picture, such as its width and height in pixels, its colour depth, its format and the date it was created.", command="State"),
        EQ("An image is 800 pixels wide, 600 pixels high and has a colour depth of 16 bits. Calculate its size in kibibytes. Show your working.", 4, [
            MP("Multiplies width by height", ["800 x 600", "480000", "pixels"]),
            MP("Multiplies by the colour depth to get bits", ["x 16", "7680000", "bits"]),
            MP("Divides by 8 to get bytes", ["/ 8", "960000", "bytes"]),
            MP("Divides by 1024 to give approximately 937.5 KiB", ["1024", "937.5", "937"]),
        ], "The number of pixels is 800 multiplied by 600, which is 480000. At 16 bits each that is 480000 multiplied by 16, giving 7680000 bits. Dividing by 8 gives 960000 bytes. Dividing by 1024 gives 937.5 kibibytes.", command="Calculate"),
        EQ("Explain the difference between sample rate and bit depth when recording sound.", 4, [
            MP("Sample rate is the number of samples taken each second", ["per second", "how often", "hertz", "frequency of sampling"]),
            MP("A higher sample rate captures faster changes and higher frequencies", ["faster changes", "higher frequencies", "closer to the wave", "detail over time"]),
            MP("Bit depth is the number of bits used to store each sample", ["bits per sample", "each sample", "number of bits"]),
            MP("A higher bit depth gives more possible levels, so each height is recorded more accurately", ["more levels", "accurate", "less rounding", "precise"]),
        ], "Sample rate is how many measurements of the wave are taken each second, measured in hertz. Raising it places the measurements closer together in time, so faster changes in the wave are captured and higher frequencies survive into the recording. Bit depth is how many bits are used to store each individual measurement. Raising it increases the number of levels a sample can take, so each measured height is rounded by a smaller amount and the recorded loudness is closer to the true value. The rate therefore controls detail across time and the bit depth controls detail in amplitude, and both increase the file size in direct proportion.", command="Explain"),
        EQ("Explain why a text file containing 2000 characters is much smaller than a screenshot of the same text.", 3, [
            MP("A text file stores one code per character", ["one code", "per character", "character set", "8 bits each"]),
            MP("An image stores a colour value for every pixel", ["every pixel", "each pixel", "colour value", "grid"]),
            MP("The image includes all the blank space, and there are far more pixels than characters", ["blank", "white space", "background", "far more pixels", "many more"]),
        ], "A text file stores one character code per character, so 2000 characters in extended ASCII takes 2000 bytes. A screenshot is a bitmap, which stores a colour value for every single pixel in the picture. A modest screenshot of 1000 by 800 pixels contains 800000 pixels, and at 24 bit colour that is 2.4 megabytes before any compression. Crucially the image also has to store the blank background between and around the letters, because a bitmap has no concept of a character at all: it records only colours at positions.", command="Explain"),
    ],
)


# ============================================ 2.3 storage and compression

T_STORAGE = Topic(
    slug="data-storage-and-compression",
    title="Data Storage and Compression",
    spec="2.3",
    icon="i-memory",
    minutes=26,
    blurb="Edexcel's binary storage units, the three types of secondary storage and how to choose between them, and lossy against lossless compression with the reasoning that earns the marks.",
    fact="A solid state drive has no moving parts at all, but each memory cell can only be rewritten a finite number of times. Drives spread writes evenly across every cell precisely so that no single one wears out first.",
    sections=[
        Section("Units of storage", """
A **bit** is one binary digit. A **nibble** is 4 bits. A **byte** is 8 bits.

Edexcel uses **binary prefixes**, in which each unit is 1024 of the one below:

| Unit | Size |
| kibibyte (KiB) | 1024 bytes |
| mebibyte (MiB) | 1024 KiB |
| gibibyte (GiB) | 1024 MiB |
| tebibyte (TiB) | 1024 GiB |

!warn 1024, not 1000 :: This is a genuine board difference and it changes every answer. Divide by 1024 at every step and label the unit with the correct name.

### Why 1024 and not 1000

Memory is addressed in binary, so its natural sizes are powers of two. 1024 is 2 to the power 10, which is the nearest power of two to a thousand, and that is why it became the unit.
"""),
        Section("Secondary storage", """
**Primary storage** is memory the processor can address directly, chiefly RAM, and it is volatile: its contents are lost when power is removed. **Secondary storage** is non volatile and holds programs and data permanently.

### Magnetic

A hard disk drive stores data as magnetised regions on spinning platters, read by a moving head.

- Very large capacities at a low cost per gigabyte.
- Slower than solid state, because the head must physically move to the data.
- Fragile when moved, since it contains moving parts.
- Suits desktop machines, servers and backups where capacity matters more than speed.

### Solid state

A solid state drive stores data in flash memory cells with no moving parts.

- Much faster access, and the same speed wherever the data is stored.
- Silent, durable and low power, which matters in a laptop.
- More expensive per gigabyte.
- A finite number of write cycles per cell, though modern drives outlast most machines.

### Optical

CDs, DVDs and Blu-ray discs store data as pits and lands read by a laser.

- Very cheap per disc and easy to distribute or post.
- Low capacity and slow.
- Read only formats cannot be altered, which suits distributing software or films.

### Choosing between them

The right answer to a "which should they use" question always comes from the situation given. Ask four questions: how much **capacity** is needed, how fast must **access** be, will the device be **carried around**, and what is the **budget**. A laptop for a travelling salesperson wants solid state for durability and speed. An archive of ten years of CCTV wants magnetic for cost per terabyte.
"""),
        Section("Compression", """
**Compression** reduces the number of bits needed to store a file, which saves storage, reduces transmission time and uses less bandwidth.

### Lossy

**Lossy** compression permanently removes data judged to be less important. The reduction is large and the original cannot be recovered exactly.

JPEG discards fine colour detail the eye barely registers. MP3 removes frequencies most people cannot hear and sounds masked by louder ones.

Appropriate for photographs, music and video, where human perception does not notice what has gone.

### Lossless

**Lossless** compression stores exactly the same information more efficiently, so the original file is reconstructed perfectly. The reduction is more modest.

Used by PNG, ZIP and FLAC, and essential for text, program code, spreadsheets and databases, where every character matters and removing any of it would corrupt the file.

### Run length encoding

A simple lossless method that replaces a run of repeated values with the value and a count.

`W W W W B B W W W W W W` becomes `4W 2B 6W`.

Twelve values become six, and nothing is lost. It works well on simple graphics with blocks of flat colour, and badly on photographs, where almost every run has length one and the result is larger than the original.

!exam Justify the choice from the file type :: "Lossless, because it is a spreadsheet and losing any value would make the figures wrong" is the full answer. Simply naming a method is half of it.
"""),
    ],
    keyterms=[
        ("Bit", "A single binary digit, either 0 or 1."),
        ("Byte", "Eight bits."),
        ("Kibibyte", "1024 bytes."),
        ("Mebibyte", "1024 kibibytes."),
        ("Volatile", "Losing its contents when power is removed, as RAM does."),
        ("Secondary storage", "Non volatile storage holding programs and data permanently."),
        ("Magnetic storage", "Storage using magnetised regions on spinning platters, read by a moving head."),
        ("Solid state storage", "Storage using flash memory cells with no moving parts."),
        ("Optical storage", "Storage using pits and lands on a disc, read by a laser."),
        ("Lossy compression", "Compression that permanently removes data, so the original cannot be recovered exactly."),
        ("Lossless compression", "Compression that stores the same information more efficiently, so the original is recovered exactly."),
        ("Run length encoding", "A lossless method replacing a run of repeated values with the value and a count."),
    ],
    grade="""
Storage questions are almost always scenario questions, and the marks are for matching the choice to the situation.

**Quote the situation back.** "The drive will be carried between sites, so solid state is the better choice because it has no moving parts to be damaged by being knocked" uses the question rather than reciting a table.

**Give capacity and cost together.** Magnetic wins on cost per terabyte, which only matters when the capacity required is large. Saying both makes the argument complete.

**Justify compression from what the file is.** Photographs and music tolerate loss because perception does not register it. Text and code cannot, because every character carries meaning.

**Use the right units.** Kibibyte, mebibyte, gibibyte, and divide by 1024.
""",
    mistakes=[
        "Dividing by 1000 rather than 1024.",
        "Saying lossless compression removes data. It removes redundancy in how data is stored.",
        "Recommending optical storage for anything needing speed or large capacity.",
        "Claiming solid state is always the right choice. Cost per gigabyte still favours magnetic for large archives.",
        "Assuming run length encoding always reduces size. On data without runs it makes the file larger.",
    ],
    quiz=[
        Q("How many bytes are in one mebibyte?", ["1048576", "1000000", "1024", "8192"], 0,
          "A mebibyte is 1024 kibibytes and a kibibyte is 1024 bytes, so it is 1024 times 1024, which is 1048576 bytes."),
        Q("Which storage type has no moving parts?", ["Solid state", "Magnetic", "Optical", "All three have moving parts"], 0,
          "Solid state uses flash memory cells. Magnetic drives spin platters and optical drives spin discs under a laser."),
        Q("Why is magnetic storage often chosen for large backups?", ["It offers the lowest cost per gigabyte at large capacities", "It is the fastest available", "It has no moving parts", "It cannot be overwritten"], 0,
          "For an archive that is written once and rarely read, capacity per pound matters far more than access speed."),
        Q("What is the defining feature of lossless compression?", ["The original file can be reconstructed exactly", "The file always becomes half the size", "It only works on images", "It removes unnecessary colours"], 0,
          "Lossless compression finds a more efficient way to store the same information, so nothing is discarded and the original returns intact."),
        Q("How would B B B W W B be written using run length encoding?", ["3B 2W 1B", "B3 W2 B", "6 values unchanged", "3B 2W"], 0,
          "There are three B, then two W, then one B, giving the pairs 3B, 2W and 1B."),
        Q("Why would run length encoding be a poor choice for a photograph?", ["Photographs contain very few runs of identical pixels, so the file could grow", "Photographs are already lossless", "RLE only works on text", "Photographs have no metadata"], 0,
          "Gradients and noise mean nearly every run has length one, so each pixel becomes a value and a count, doubling the data."),
        Q("Which is the correct term for storage whose contents are lost when power is removed?", ["Volatile", "Non volatile", "Optical", "Secondary"], 0,
          "RAM is volatile, which is why work must be saved to secondary storage before the machine is switched off."),
        Q("Which compression method would be appropriate for a spreadsheet of financial figures?", ["Lossless, because losing any value would make the figures wrong", "Lossy, because spreadsheets contain redundant cells", "Either, since the effect is the same", "Neither, spreadsheets cannot be compressed"], 0,
          "Every value in a spreadsheet carries meaning, so nothing can be discarded without corrupting the data."),
        Q("A file is 4 GiB. How many mebibytes is that?", ["4096", "4000", "1024", "4194304"], 0,
          "A gibibyte is 1024 mebibytes, so four gibibytes is 4 times 1024, which is 4096 mebibytes."),
        Q("Why does a solid state drive have a limited lifetime?", ["Each memory cell can only be rewritten a finite number of times", "The platters wear out from spinning", "The laser dims with use", "The magnetic coating degrades"], 0,
          "Flash cells degrade with each write, which is why drives distribute writes evenly across all cells to avoid wearing one out early."),
    ],
    exam=[
        EQ("State one advantage of solid state storage over magnetic storage.", 1, [
            MP("Faster access, or no moving parts so more durable, or lower power use", ["faster", "no moving parts", "durable", "silent", "less power", "robust"]),
        ], "Solid state storage has no moving parts, so it is far more durable when the device is carried around, and data is accessed considerably faster because there is no read head that must physically move to the right place.", command="State"),
        EQ("A film company needs to store 40 TiB of raw footage that will be archived and rarely accessed. Recommend a type of secondary storage and justify your choice.", 4, [
            MP("Recommends magnetic storage", ["magnetic", "hard disk", "hdd", "hard drive"]),
            MP("Justifies it on the very large capacity required", ["capacity", "40 tib", "large", "terabytes", "amount"]),
            MP("Justifies it on cost per gigabyte or terabyte", ["cost", "cheaper", "per gigabyte", "price", "affordable"]),
            MP("Notes that the slower access speed does not matter for an archive", ["rarely accessed", "archive", "speed does not matter", "not important", "slow is acceptable"]),
        ], "The company should use magnetic hard disk storage. The volume involved is very large, and magnetic drives offer by far the lowest cost per terabyte at that scale, so the whole archive can be held for a fraction of what solid state would cost. The main drawback of magnetic storage is that access is slower, because the read head has to move physically to the data, but that is close to irrelevant here since the footage is being archived and will rarely be read. Optical storage is unsuitable because a single disc holds only a few gigabytes, so 40 tebibytes would need thousands of them.", command="Recommend"),
        EQ("Explain the difference between lossy and lossless compression.", 4, [
            MP("Lossy compression permanently removes data", ["removes", "discards", "permanently", "deleted"]),
            MP("So the original file cannot be recovered exactly", ["cannot recover", "not exact", "original lost", "irreversible"]),
            MP("Lossless compression stores the same data more efficiently", ["same data", "more efficient", "no data lost", "redundancy"]),
            MP("So the original file can be reconstructed exactly", ["exactly", "identical", "perfectly", "recovered", "restored"]),
        ], "Lossy compression achieves a large reduction in size by permanently discarding data that is judged to be less important, such as colour detail in an image that the eye barely registers or frequencies in audio that most people cannot hear. Because that data is gone, the original file can never be reconstructed exactly. Lossless compression instead finds a more efficient way of storing exactly the same information, for example by replacing runs of repeated values with a value and a count. Nothing is discarded, so decompressing gives back a file identical to the original, but the reduction achieved is more modest than lossy compression can manage.", command="Explain"),
        EQ("A row of pixels contains B B B B B W W B B B. Show how it would be stored using run length encoding, and state how many values are saved.", 3, [
            MP("Identifies the runs as five B, two W, three B", ["5b", "2w", "3b", "five", "two", "three"]),
            MP("Writes them as value and count pairs", ["pairs", "count", "5 B 2 W 3 B"]),
            MP("States that six values replace ten, saving four", ["six", "10", "saves four", "4 fewer", "from 10 to 6"]),
        ], "The row contains five B, then two W, then three B, so under run length encoding it is stored as the pairs 5B, 2W, 3B. That is three pairs, which is six values in total, in place of the ten values in the original row, so four values are saved. Nothing has been lost, since the original row can be written out again exactly from the pairs.", command="Show"),
    ],
)


# ============================================ 3.1 hardware

T_HARDWARE = Topic(
    slug="hardware-and-the-processor",
    title="Hardware and the Processor",
    spec="3.1",
    icon="i-cpu",
    minutes=30,
    blurb="The components of a computer system, the von Neumann architecture, the fetch decode execute cycle, and what actually makes one processor faster than another.",
    fact="A processor running at 3 GHz completes a clock cycle in a third of a nanosecond. In that time light travels about ten centimetres, which is why the physical size of a chip is now a genuine limit on how fast it can run.",
    sections=[
        Section("Components of a computer system", """
Every computer system has the same shape: **input**, **process**, **output**, with **storage** alongside.

- **Input devices** bring data in: keyboard, mouse, microphone, sensor, camera.
- The **CPU** processes it.
- **Output devices** present the results: screen, printer, speaker, motor.
- **Memory** holds what is being worked on now.
- **Secondary storage** holds it permanently.

### The von Neumann architecture

Almost every computer follows the **von Neumann architecture**, whose central idea is the **stored program concept**: instructions and data are held in the **same memory**, and instructions are fetched one at a time to be executed.

Before this, a machine had to be rewired to do a different job. The stored program concept is why one laptop can be a browser, a compiler and a game without any physical change.

The cost is the **von Neumann bottleneck**: instructions and data share one route to memory, so they compete for it and the processor spends part of its time waiting.
"""),
        Section("Inside the CPU", """
| Component | Job |
| Control unit | Decodes instructions and sends the control signals that coordinate everything else |
| Arithmetic logic unit | Performs all calculations and all comparisons |
| Registers | Very small, very fast stores inside the CPU, each holding one value |
| Cache | Small, very fast memory holding recently and frequently used data and instructions |
| Buses | The connections carrying addresses, data and control signals |

### The registers that matter

- **Program counter (PC)**: the address of the **next** instruction to be fetched.
- **Memory address register (MAR)**: the address currently being accessed.
- **Memory data register (MDR)**: the data or instruction being moved to or from memory.
- **Accumulator (ACC)**: the result of the most recent calculation.

!warn MAR holds an address, MDR holds data :: The names tell you. Swapping them is the most commonly penalised error on this topic.

### The fetch decode execute cycle

**Fetch**
1. The address in the PC is copied into the MAR.
2. The PC is incremented.
3. The address goes out on the address bus and the instruction returns on the data bus into the MDR.

**Decode**
4. The control unit works out what the instruction means and what it applies to.

**Execute**
5. The instruction is carried out. A calculation is done by the ALU and the result goes into the accumulator. A jump writes a new address into the PC.

Then it repeats, billions of times a second.
"""),
        Section("What makes a processor faster", """
### Clock speed

The clock produces pulses and one stage of the cycle happens per pulse. A 3 GHz processor produces three billion pulses a second, so a higher clock speed means more instructions completed per second. Heat and power consumption rise faster than speed does, which is why clock speeds stopped climbing around 2005.

### Number of cores

A **core** is a complete processing unit. A quad core processor can genuinely execute four instructions simultaneously.

It rarely gives four times the performance. Some tasks are sequential, because each step needs the result of the last, and much software is not written to divide work across cores at all.

### Cache size

Cache holds recently and frequently used instructions and data close to the processor, where they can be reached far faster than main memory. More cache means the processor waits for RAM less often.

!key The framing that earns the mark :: Cache does not make the processor faster. It reduces the time the processor spends waiting, so more instructions are completed each second.

### Embedded systems

An **embedded system** is a computer built into a larger device to do one dedicated task: a washing machine controller, a traffic light, a pacemaker. Because the task never changes it can use a modest processor and very little memory, which makes it cheap, reliable and power efficient, at the cost of being unable to do anything else.
"""),
    ],
    keyterms=[
        ("Von Neumann architecture", "A design in which instructions and data share the same memory and instructions are fetched one at a time."),
        ("Stored program concept", "The idea that a program is held in memory alongside its data rather than wired into the machine."),
        ("Control unit", "The component that decodes instructions and coordinates the rest of the processor."),
        ("Arithmetic logic unit", "The component that performs calculations and comparisons."),
        ("Register", "A very small, very fast store inside the CPU holding one value."),
        ("Program counter", "The register holding the address of the next instruction to be fetched."),
        ("Cache", "Small, very fast memory close to the CPU holding recently and frequently used data."),
        ("Clock speed", "The number of clock pulses per second, measured in hertz."),
        ("Core", "A complete processing unit within a CPU."),
        ("Embedded system", "A computer built into a larger device to carry out one dedicated task."),
    ],
    grade="""
This topic is about naming things precisely and explaining performance as throughput.

**Use the register names inside the sentence.** "The address in the program counter is copied into the MAR, and the instruction at that address returns along the data bus into the MDR" is a full mark answer.

**Say what performance actually means.** More instructions completed per second, not vaguely "faster". Cache reduces waiting. Cores allow genuine parallelism where the software supports it. Clock speed raises the rate of stages.

**Qualify multi core claims.** Four cores are not four times faster, because sequential tasks and single threaded software cannot use them.
""",
    mistakes=[
        "Swapping MAR and MDR.",
        "Saying the program counter is incremented at the end of the cycle rather than during fetch.",
        "Writing that cache increases clock speed. It reduces waiting.",
        "Saying more cores always means proportionally more performance.",
        "Describing an embedded system as simply a small computer rather than one dedicated to a single task.",
    ],
    quiz=[
        Q("Which register holds the address of the next instruction to be fetched?", ["Program counter", "MAR", "MDR", "Accumulator"], 0,
          "The program counter tracks the position in the program, holding the address of the instruction to fetch next."),
        Q("What is held in the MDR?", ["Data or an instruction moving to or from memory", "The address being accessed", "The result of a calculation", "The number of cores"], 0,
          "The memory data register holds the actual data travelling between the processor and memory. Addresses are held in the MAR."),
        Q("What is the defining feature of the von Neumann architecture?", ["Instructions and data are held in the same memory", "It uses four registers", "It has more than one core", "It stores programs on an optical disc"], 0,
          "The stored program concept, with instructions and data in one memory, is what defines von Neumann and makes general purpose computing possible."),
        Q("Which component performs comparisons such as testing whether one value is greater than another?", ["The arithmetic logic unit", "The control unit", "The program counter", "Cache"], 0,
          "The ALU performs both arithmetic and logic, and a comparison is a logic operation."),
        Q("How does a larger cache improve performance?", ["More of what the processor needs is close by, so it waits for RAM less often", "It increases the clock speed", "It adds another core", "It reduces the number of instructions needed"], 0,
          "Cache reduces how often the processor has to wait for the much slower main memory, so more instructions complete each second."),
        Q("Why might a quad core processor not be twice as fast as a dual core one?", ["Some tasks are sequential and much software cannot use multiple cores", "The cores run at half speed each", "Cache is shared and therefore useless", "Quad core processors have a lower clock speed by design"], 0,
          "A task whose next step depends on the previous result cannot be split, and software must be written deliberately to use several cores."),
        Q("At what point is the program counter incremented?", ["During the fetch stage", "At the end of the execute stage", "Only after a jump instruction", "Once per program"], 0,
          "Incrementing during fetch means a jump executed afterwards can write its target address into the PC without being immediately overwritten."),
        Q("What is an embedded system?", ["A computer built into a larger device to perform one dedicated task", "Any computer without a screen", "A computer with only one core", "A computer that cannot be networked"], 0,
          "Being dedicated to one fixed task is the defining feature, and it is what allows the hardware to be modest, cheap and reliable."),
        Q("What travels along the address bus?", ["The memory location being read from or written to", "The instruction itself", "The result of a calculation", "The clock pulse"], 0,
          "The address bus carries memory addresses out of the processor. The instruction or data itself travels on the data bus."),
        Q("Why is the von Neumann bottleneck a limitation?", ["Instructions and data share one route to memory, so they compete and the CPU waits", "Only one program can be stored at a time", "Registers can hold only one value", "Memory cannot be written to"], 0,
          "Both instructions and data travel over the same connection, so only one can move at a time and the processor is idle for part of every cycle."),
    ],
    exam=[
        EQ("State the purpose of the accumulator.", 1, [
            MP("It holds the result of the most recent calculation", ["result", "calculation", "alu", "answer", "output of the alu"]),
        ], "The accumulator is the register that holds the result of the most recent calculation carried out by the arithmetic logic unit.", command="State"),
        EQ("Describe the fetch stage of the fetch decode execute cycle.", 4, [
            MP("The address in the program counter is copied into the MAR", ["program counter", "pc", "mar", "copied"]),
            MP("The program counter is incremented", ["incremented", "increased", "next address", "plus one"]),
            MP("The address is sent out on the address bus", ["address bus", "sent to memory", "out to memory"]),
            MP("The instruction is returned on the data bus into the MDR", ["data bus", "mdr", "returned", "brought back"]),
        ], "The address held in the program counter is copied into the memory address register. The program counter is then incremented so that it already points to the following instruction. The address in the MAR travels out along the address bus to main memory, and the instruction stored at that address is returned along the data bus into the memory data register, ready to be decoded by the control unit.", command="Describe"),
        EQ("Explain how increasing the size of the cache can improve the performance of a computer.", 3, [
            MP("Cache holds recently and frequently used data and instructions close to the CPU", ["recently used", "frequently", "close", "near the cpu"]),
            MP("Data in cache is accessed far faster than data in main memory", ["faster", "quicker than ram", "less time", "much faster"]),
            MP("A larger cache means fewer fetches from RAM, so the CPU spends less time waiting", ["fewer fetches", "less waiting", "idle", "more instructions per second"]),
        ], "Cache is small, very fast memory located inside or extremely close to the processor, holding copies of the instructions and data that have been used recently or are likely to be needed next. Reading from cache takes a small fraction of the time that reading from main memory takes. Making the cache larger means a greater proportion of what the processor asks for is already there, so it has to fetch from RAM less often. Since a fetch from RAM leaves the processor idle while it waits, reducing how often that happens means more instructions are completed each second, which is what performance actually measures.", command="Explain"),
        EQ("A manufacturer is designing a controller for a microwave oven. Explain why an embedded system is more suitable than a general purpose computer.", 4, [
            MP("The controller carries out one fixed, dedicated task", ["one task", "dedicated", "fixed", "specific"]),
            MP("It does not need to run other software or a general purpose operating system", ["no operating system", "one program", "no other software", "not general purpose"]),
            MP("So a modest processor and very little memory are sufficient, which reduces cost", ["cheaper", "less powerful", "small memory", "low cost"]),
            MP("It is also more reliable and uses less power, which matters for an appliance", ["reliable", "less to go wrong", "power", "efficient", "always on"]),
        ], "The controller in a microwave has exactly one job, which is to run the cooking programme, drive the turntable and magnetron and read the keypad. Because that job is fixed and will never change, the system does not need to run arbitrary software and does not need a general purpose operating system to manage whatever a user might install. The single program can be written to fit the hardware precisely, so a very modest processor and a few kilobytes of memory are enough, which makes the component far cheaper to manufacture at the volumes involved. It is also more reliable, since there is very little that can go wrong and no software to become corrupted, and it consumes far less power, which matters in an appliance that is connected to the mains continuously.", command="Explain"),
    ],
)


# ============================================ 3.2 to 3.3 software and languages

T_SOFTWARE = Topic(
    slug="software-and-programming-languages",
    title="Software and Programming Languages",
    spec="3.2 to 3.3",
    icon="i-layers",
    minutes=28,
    blurb="System software against application software, the four jobs of an operating system, utilities, and how high and low level languages are translated into something a processor can run.",
    fact="The first compiler was written in 1952 by Grace Hopper, who was told repeatedly that computers could not understand English-like instructions. Every high level language since exists because she was right and they were wrong.",
    sections=[
        Section("System and application software", """
**System software** manages the computer itself and includes the operating system and utility programs. **Application software** lets a user carry out a particular task: a browser, a word processor, a game.

The test is purpose. Application software serves the user's job. System software serves the machine, so that application software can run at all.

### What an operating system does

**Processor management.** Decides which process gets the processor and for how long, switching between them fast enough that they appear to run at once.

**Memory management.** Allocates memory to each running program and keeps them out of one another's memory, moving less used pages to virtual memory on the drive when physical memory runs out.

**Peripheral and device management.** Communicates with input and output devices through **device drivers**, so an application can say "print this" without knowing anything about the specific printer.

**User management and security.** Handles accounts, logins and permissions, so different users have different files and different rights on one machine.

It also provides the **user interface**, graphical or command line, through which everything else is reached.

!exam Do not stop at the word 'manages' :: Say what is managed and what would go wrong without it. "Memory management stops one program writing into another program's memory, which would crash it" is the complete answer.
"""),
        Section("Utility software", """
**Utility software** performs maintenance and housekeeping. It is system software, but it is not part of the operating system's core job.

| Utility | Purpose |
| Backup | Copies files to a separate location so they can be restored after loss, failure or ransomware |
| Anti-malware | Scans for and removes malicious software before it runs |
| Encryption | Scrambles data so it is unreadable without the key |
| Compression | Reduces file sizes to save storage and transmission time |
| Defragmentation | Rearranges the parts of files on a mechanical drive so each file is stored together |
| Disk clean up | Removes temporary and unnecessary files to reclaim space |

!warn Defragmentation is for mechanical drives only :: A solid state drive reaches every location in the same time, so gathering files together gains nothing, and the very large number of writes involved shortens the drive's life.
"""),
        Section("Programming languages and translators", """
### High and low level

A **high level language** such as Python is written close to human language. One statement usually becomes many machine instructions, which is why it is quick to write and easy to read, and why it runs on any machine that has a translator for it.

A **low level language** is close to the hardware. **Machine code** is the binary the processor executes. **Assembly language** replaces those binary opcodes with mnemonics such as ADD and LDA, roughly one mnemonic per machine instruction.

| | High level | Low level |
| Readability | Close to English | Difficult |
| Portability | Runs anywhere with a translator | Written for one processor |
| Speed of development | Fast | Slow |
| Control of hardware | Indirect | Complete |
| Memory management | Handled for you | The programmer's job |

Low level languages are still used for device drivers, for embedded systems with very little memory, and for small routines where the last few per cent of speed genuinely matters.

### Translators

A processor executes machine code and nothing else, so anything else must be translated.

**An assembler** translates assembly language into machine code, roughly one instruction at a time.

**A compiler** translates a whole high level program into machine code before it is run, producing an executable file.

- The finished program runs quickly, because translation has already happened.
- It can be distributed without the source code.
- No translator is needed on the machine that runs it.
- All errors are reported together at the end of compilation.
- The executable only runs on the platform it was compiled for.

**An interpreter** translates and executes one statement at a time, every time the program is run.

- Errors are reported as soon as the offending line is reached, which makes debugging far quicker.
- The same source runs anywhere the right interpreter exists.
- Execution is slower, because translation happens on every run and every time round a loop.
- The source code must be given to whoever runs it.

!key Development against execution :: Interpreters win while you are writing the program. Compilers win once it is finished. Answers that keep those two situations apart get full marks.
"""),
    ],
    keyterms=[
        ("System software", "Software that manages the computer itself, including the operating system and utilities."),
        ("Application software", "Software that lets the user carry out a particular task."),
        ("Operating system", "System software managing the processor, memory, peripherals and users, and providing the interface."),
        ("Device driver", "Software allowing the operating system to communicate with a particular hardware device."),
        ("Utility software", "System software carrying out maintenance tasks such as backup, encryption or compression."),
        ("High level language", "A language written close to human language, where one statement becomes many machine instructions."),
        ("Low level language", "A language close to the hardware, either machine code or assembly language."),
        ("Assembler", "A translator converting assembly language into machine code."),
        ("Compiler", "A translator converting a whole high level program into machine code before it runs."),
        ("Interpreter", "A translator converting and executing a high level program one statement at a time."),
    ],
    grade="""
Two habits earn the top marks on this topic.

**Explain a function by its consequence.** Memory management stops one program corrupting another. Device drivers mean an application need not know which printer is attached. Naming the outcome is what distinguishes a developed point.

**Separate development from execution when comparing translators.** "An interpreter is slower" is incomplete. "An interpreter is slower to execute because it translates each line every time it is run, but faster to develop with because it reports an error as soon as it reaches the line containing it" is the answer.
""",
    mistakes=[
        "Calling a device driver hardware. It is software.",
        "Saying a compiler is simply faster than an interpreter without saying at what.",
        "Describing assembly language as machine code. It uses mnemonics and still needs assembling.",
        "Saying utilities are application software. They maintain the machine, so they are system software.",
        "Claiming defragmentation speeds up a solid state drive.",
    ],
    quiz=[
        Q("Which of these is application software?", ["A photo editor", "A device driver", "The operating system", "A disk defragmenter"], 0,
          "A photo editor exists so the user can carry out a task. The other three exist to run or maintain the machine."),
        Q("What does memory management in an operating system do?", ["Allocates memory to programs and stops one writing into another's", "Increases the amount of RAM installed", "Stores files permanently", "Compresses files automatically"], 0,
          "The OS gives each process its own area and enforces the boundaries, which is what prevents one faulty program bringing down another."),
        Q("Why does an operating system use device drivers?", ["So applications can use hardware without knowing the details of a specific model", "To make devices physically faster", "To store the device's settings in the cloud", "To encrypt data sent to devices"], 0,
          "The driver translates general instructions into the exact commands one device understands, so software is written once for any printer."),
        Q("What is the main advantage of an interpreter during development?", ["Errors are reported as soon as the line containing them is reached", "The program runs faster", "The source code is hidden", "It produces a standalone executable"], 0,
          "An interpreter stops at the first problem line and reports it, which locates the fault immediately and allows an instant retry after a fix."),
        Q("Why does compiled code usually run faster than interpreted code?", ["Translation has already happened, so machine code runs directly", "Compilers rewrite the algorithm", "Compiled programs skip error checking", "Interpreters use slower hardware"], 0,
          "A compiled program is already machine code. An interpreter translates each line every time it runs, including every pass round a loop."),
        Q("What does an assembler translate?", ["Assembly language into machine code", "High level code into machine code", "Machine code into high level code", "One high level language into another"], 0,
          "An assembler converts mnemonics into the binary opcodes the processor executes, roughly one for one."),
        Q("Which utility would most directly help recover from a ransomware attack?", ["Backup software", "Defragmentation", "Compression", "Disk clean up"], 0,
          "Recent backups held separately can be restored, which removes the attacker's leverage entirely."),
        Q("Why would a programmer use a low level language for a device driver?", ["It gives direct control over specific hardware", "It is quicker to write", "It is more portable", "It handles memory automatically"], 0,
          "A driver must address particular hardware registers precisely, which is exactly what a low level language provides and a high level one hides."),
        Q("What is a disadvantage of a compiled program?", ["It only runs on the platform it was compiled for", "It cannot be distributed", "Errors are never reported", "It must be recompiled each time it runs"], 0,
          "The executable contains machine code for one instruction set and operating system, so a different platform needs a separate compilation."),
        Q("Which statement about a high level language statement is correct?", ["It usually translates into many machine code instructions", "It always becomes exactly one machine instruction", "It runs directly on the processor", "It cannot be translated"], 0,
          "The one to many relationship is what makes a language high level and is why such code is shorter and quicker to write."),
    ],
    exam=[
        EQ("State one difference between system software and application software.", 2, [
            MP("System software manages or maintains the computer itself", ["manages", "runs the computer", "maintains", "operating system"]),
            MP("Application software allows the user to complete a particular task", ["task", "user", "browser", "word processor", "job"]),
        ], "System software manages and maintains the computer itself, the operating system and utility programs being the main examples. Application software is installed so that the user can carry out a particular task such as browsing the web or editing a photograph.", command="State"),
        EQ("Describe two functions of an operating system.", 4, [
            MP("Memory management, allocating memory to each running program", ["memory", "allocate", "ram"]),
            MP("Explains the consequence, such as preventing programs interfering with each other", ["prevents", "separate", "crash", "protects"]),
            MP("Peripheral management, communicating with devices through drivers", ["peripheral", "device", "driver", "printer", "input output"]),
            MP("Explains the consequence, such as applications not needing to know the specific hardware", ["does not need to know", "any printer", "hides the detail", "one instruction"]),
        ], "The first is memory management. The operating system allocates an area of memory to each running program and keeps track of what is in use, which prevents one program from writing into memory belonging to another and crashing it, and it moves less used pages out to virtual memory when physical memory runs short. The second is peripheral management. The operating system communicates with input and output devices through device drivers, so an application can simply request that a page is printed without containing any knowledge of the particular printer attached, and a new device is supported by installing a driver rather than by rewriting every program.", command="Describe"),
        EQ("Explain one advantage of using an interpreter and one advantage of using a compiler.", 4, [
            MP("An interpreter reports an error as soon as it reaches the line containing it", ["as soon as", "line by line", "immediately", "stops at that line"]),
            MP("Which makes locating and fixing faults during development much quicker", ["easier to find", "locate", "debug", "quicker to fix", "test again"]),
            MP("A compiler translates the whole program once before it runs", ["once", "whole program", "before running", "in advance"]),
            MP("So the finished program executes faster, and can be distributed without the source code", ["faster", "executes quickly", "without source", "executable", "protects"]),
        ], "An interpreter translates and executes one statement at a time, so when it reaches a line it cannot process it stops there and reports it. That tells the programmer precisely where the fault is and allows an immediate retry after a change, with no compilation step in between, which makes the write, test and correct cycle much faster while a program is still being developed. A compiler translates the entire program into machine code once, before it is ever run. At run time the processor executes machine code directly with no translation happening at all, so the finished program is considerably faster, and it can be distributed as an executable without the source code, which protects the developer's work and means the user needs no translator installed.", command="Explain"),
        EQ("A company is writing software for a device with only 32 kilobytes of memory. Explain why part of the program might be written in a low level language.", 3, [
            MP("A low level language gives direct control over memory and hardware", ["direct control", "memory", "hardware", "registers", "precise"]),
            MP("The code can be made extremely compact, using far fewer bytes", ["compact", "small", "fewer bytes", "efficient", "fits"]),
            MP("Acknowledges the cost, that it is slow to write and not portable", ["slow to write", "harder", "not portable", "one processor", "difficult"]),
        ], "A low level language lets the programmer decide exactly how every byte of memory is used and exactly which instructions the processor executes, rather than leaving those decisions to a compiler making general purpose choices. With only 32 kilobytes available that control is what makes the program fit at all, since the equivalent high level program would very likely be several times larger. The cost is real: low level code takes far longer to write, is much harder to read and debug, and is written for one specific processor, so it cannot be recompiled for different hardware later. For that reason a company would usually write only the memory critical or timing critical routines this way and keep the rest of the program in a high level language.", command="Explain"),
    ],
)


# ============================================ 4.1 to 4.2 networks

T_NET = Topic(
    slug="networks-and-network-security",
    title="Networks and Network Security",
    spec="4.1 to 4.2",
    icon="i-network",
    minutes=32,
    blurb="Local and wide area networks, topologies, wired against wireless, protocols and layers, and every threat and defence Edexcel expects you to name.",
    fact="The first message ever sent over the network that became the internet was meant to be the word LOGIN. The system crashed after two characters, so the first thing ever transmitted was LO.",
    sections=[
        Section("Networks and topologies", """
A **network** is two or more computers connected so they can share data and resources.

A **LAN** covers a small area on one site, with hardware the organisation owns. A **WAN** covers a large geographical area, connecting sites using infrastructure hired from a provider. The internet is the largest WAN.

### Network hardware

- A **network interface card** provides the physical connection and the MAC address.
- A **switch** joins devices on a LAN and sends each frame only to its destination.
- A **router** joins networks together and directs packets between them.
- A **wireless access point** allows devices to join without a cable.

### Topologies

**Star.** Every device has its own cable to a central switch. Fast, because connections are dedicated; reliable, because one broken cable affects one device; easy to extend. More expensive, and the switch is a single point of failure.

**Mesh.** Every device connects to several or all others, so there are many possible routes. Extremely resilient, because traffic reroutes around a failure, and it scales well for wireless. Expensive and complex to cable in full.

!key Resilience against cost :: A star concentrates risk at the switch and saves cable. A full mesh removes the single point of failure and pays for it in cabling. Almost every topology question is that trade off.

### Wired and wireless

Wired is faster, more consistent and more secure, because interception needs physical access to the cable. It is expensive to install and the devices cannot move.

Wireless is cheap and quick to install and lets devices move freely. It is slower, degrades with distance and obstacles, is subject to interference and, by default, less secure because the signal travels through the air where anyone in range can receive it.
"""),
        Section("Protocols and layers", """
A **protocol** is a set of rules governing communication. Both ends must follow the same rules for anything to be understood.

| Protocol | Purpose |
| Ethernet | Wired local area networking |
| Wi-Fi | Wireless local area networking |
| TCP | Splits data into packets, checks delivery and reassembles them in order |
| IP | Addresses packets and routes them between networks |
| HTTP | Requests and delivers web pages |
| HTTPS | The same, encrypted so intercepted traffic cannot be read |
| FTP | Transfers files between computers |
| SMTP | **Sends** email |
| IMAP | **Retrieves** email, leaving it on the server |

### Layers

Protocols are organised into layers, each handling one part of the job and passing its result to the next.

| Layer | Job |
| Application | Services for the user's software: HTTP, FTP, SMTP, IMAP |
| Transport | Splitting into packets and managing the connection: TCP |
| Network | Addressing and routing: IP |
| Link | Sending over the physical medium: Ethernet, Wi-Fi |

Layering divides a huge problem into manageable parts, and lets any one layer be replaced without disturbing the others. Moving a laptop from Ethernet to Wi-Fi changes the link layer only: HTTP, TCP and IP carry on unchanged and no application has to be rewritten.

!warn Layers do not make a network faster :: They make it manageable, interoperable and independently changeable, and that is what the mark scheme rewards.
"""),
        Section("Threats and protection", """
### Threats

**Malware.** Viruses attach to files and spread when those files are shared. Worms spread across a network by themselves. Trojans pretend to be legitimate software. Ransomware encrypts files and demands payment. Spyware records activity such as keystrokes.

**Social engineering.** Manipulating people rather than technology. **Phishing** sends messages impersonating a legitimate organisation to obtain details. **Pretexting** invents a scenario to persuade someone to hand over information. **Shouldering** means watching someone type a password.

**Brute force attacks.** Trying every possible password until one works, which is why length matters far more than complexity.

**Denial of service.** Flooding a server with requests so it cannot serve legitimate users.

**Data interception.** Capturing data as it travels across a network, which is trivial on unencrypted wireless.

**SQL injection.** Entering SQL into an input box that the site passes straight to its database, allowing an attacker to read or destroy data.

### Protection

| Measure | What it achieves |
| Firewall | Inspects traffic entering and leaving and blocks what is not permitted |
| Anti-malware | Detects and removes known malicious software |
| Encryption | Makes intercepted or stolen data unreadable without the key |
| Strong passwords and authentication | Makes guessing and brute force impractical |
| User access levels | Limit what one compromised account can reach |
| Validation of inputs | Prevents SQL injection by rejecting or escaping what is entered |
| Penetration testing | Authorised simulated attacks that find weaknesses first |
| Physical security | Stops somebody simply walking in and taking a machine |
| Software updates | Close known weaknesses before they are exploited |

!key Say what each measure does, not just its name :: Encryption does not stop data being stolen, it stops stolen data being read. A firewall does not remove malware, it blocks traffic. That precision is where the marks are.
"""),
    ],
    keyterms=[
        ("LAN", "Local area network, covering one site with hardware the organisation owns."),
        ("WAN", "Wide area network, spanning sites using hired infrastructure."),
        ("Switch", "A device joining computers on a LAN and forwarding each frame only to its destination."),
        ("Router", "A device joining networks together and directing packets between them."),
        ("Star topology", "A layout in which every device has its own cable to a central switch."),
        ("Mesh topology", "A layout in which devices connect to several or all others, giving many routes."),
        ("Protocol", "A set of rules governing how devices communicate."),
        ("Layer", "One level of a networking model, handling one part of the communication task."),
        ("Phishing", "Sending messages that appear legitimate in order to obtain confidential details."),
        ("Brute force attack", "Trying every possible password until the correct one is found."),
        ("Denial of service", "Flooding a server with requests so that it cannot serve legitimate users."),
        ("SQL injection", "Entering SQL into an input field so that it is executed by the site's database."),
    ],
    grade="""
Network questions reward causal reasoning and precise vocabulary.

**Name the threat exactly.** Phishing, pretexting, brute force, denial of service and SQL injection are distinct named threats, and the exam expects the right word for the scenario.

**Match the defence to the threat in the question.** A stolen laptop needs encryption and physical security. Staff clicking links needs training and filtering. An input box needs validation. Listing every measure you know earns fewer marks than choosing two and justifying them.

**Explain layering with an example of change.** Swapping Wi-Fi for Ethernet changes the link layer and nothing above it, so no application needs rewriting. That single example demonstrates the whole idea.
""",
    mistakes=[
        "Calling every attack 'hacking' rather than naming the specific threat.",
        "Swapping SMTP and IMAP. SMTP sends, IMAP retrieves.",
        "Saying encryption prevents data being stolen. It prevents stolen data being read.",
        "Saying layering makes a network faster.",
        "Confusing a switch with a router.",
    ],
    quiz=[
        Q("What is the main difference between a LAN and a WAN?", ["A LAN covers one site with hardware the organisation owns, a WAN spans sites using hired infrastructure", "A LAN is always wireless", "A WAN has fewer than 50 devices", "A LAN cannot reach the internet"], 0,
          "The distinction combines geography with ownership: a WAN crosses land the organisation does not own, so it rents the connections."),
        Q("Which protocol is used to retrieve email while leaving it on the server?", ["IMAP", "SMTP", "FTP", "HTTP"], 0,
          "IMAP retrieves mail and keeps it on the server so it stays in sync across devices. SMTP is for sending."),
        Q("What is the advantage of a mesh topology?", ["Many possible routes, so traffic reroutes around a failure", "It uses the least cable", "It needs no network hardware", "Every device shares one connection"], 0,
          "Multiple routes mean no single link or device is a point of failure, which is why mesh is used where resilience matters."),
        Q("What is a brute force attack?", ["Trying every possible password until one works", "Flooding a server with requests", "Sending a fake email", "Entering SQL into an input box"], 0,
          "A brute force attack systematically tries combinations, which is why password length matters more than adding one unusual symbol."),
        Q("What does a denial of service attack do?", ["Floods a server with requests so it cannot serve legitimate users", "Steals passwords from a database", "Encrypts files and demands payment", "Redirects users to a fake website"], 0,
          "The aim is availability, not theft: the service is overwhelmed so that genuine users cannot reach it."),
        Q("How does validation of inputs help prevent SQL injection?", ["It rejects or neutralises input that would be executed as SQL", "It encrypts the database", "It blocks traffic at the firewall", "It requires a stronger password"], 0,
          "SQL injection works because text typed by a user reaches the database as code. Validating and escaping input stops that happening."),
        Q("Which layer does IP operate at?", ["Network", "Application", "Transport", "Link"], 0,
          "IP handles addressing and routing between networks, which is the network layer's job."),
        Q("Why is wireless less secure than wired by default?", ["The signal travels through the air and can be received by anyone in range", "Wireless cannot be encrypted", "Wireless uses weaker passwords", "Wireless has no protocols"], 0,
          "Intercepting a wireless signal requires only proximity, whereas intercepting a cable requires physical access to it."),
        Q("What does a firewall do?", ["Inspects traffic entering and leaving a network and blocks what is not permitted", "Removes malware already on a machine", "Encrypts stored files", "Backs up data automatically"], 0,
          "A firewall filters network traffic against rules. It does not clean an infected machine, which is anti-malware's job."),
        Q("A laptop is moved from a wired connection to Wi-Fi and every application still works. Which principle does this show?", ["Layers can be replaced independently of one another", "Protocols are optional", "TCP converts itself to Wi-Fi", "Applications contain their own drivers"], 0,
          "Only the link layer changed. Everything above it was untouched, which is precisely why networking is layered."),
    ],
    exam=[
        EQ("State two items of network hardware and describe the purpose of each.", 4, [
            MP("Names a switch", ["switch"]),
            MP("Describes it as joining devices on a LAN and sending frames to their destination", ["joins", "connects devices", "forwards", "destination", "lan"]),
            MP("Names a router", ["router"]),
            MP("Describes it as joining networks and directing packets between them", ["joins networks", "between networks", "routes", "directs packets", "internet"]),
        ], "A switch joins the devices on a local area network together and forwards each frame only to the device it is addressed to, which keeps traffic off the rest of the network. A router joins separate networks together and directs packets between them, deciding which route each packet should take, which is what connects a local network to the internet.", command="State"),
        EQ("Explain why network protocols are organised into layers.", 4, [
            MP("Each layer handles one part of the communication task", ["one part", "one job", "divides", "separate"]),
            MP("So a very complex problem is broken into manageable pieces", ["manageable", "simpler", "complex", "easier to develop"]),
            MP("A layer can be changed without affecting the layers above and below it", ["changed", "replaced", "independent", "without affecting"]),
            MP("Gives an example such as swapping Ethernet for Wi-Fi", ["ethernet", "wi-fi", "wireless", "link layer", "example"]),
        ], "Layering divides the problem of network communication into parts, each of which handles one aspect and interacts only with the layer directly above and below it. That means nobody has to understand the whole of networking at once, and different specialists can work on different layers. It also gives independence: because each layer only depends on the interface the next presents, one can be replaced entirely without disturbing the others. Moving a laptop from an Ethernet cable to Wi-Fi replaces the link layer completely, yet IP, TCP and HTTP carry on exactly as before and no application has to be rewritten.", command="Explain"),
        EQ("An online shop finds that an attacker has read its entire customer table by typing text into the site's search box. Name the attack and explain how it could be prevented.", 4, [
            MP("Names SQL injection", ["sql injection", "injection"]),
            MP("Explains that text entered by the user is being executed as part of a database query", ["executed", "part of the query", "database", "runs as sql", "passed to the database"]),
            MP("Prevention by validating or sanitising input", ["validation", "validate", "sanitise", "reject", "check input", "escape"]),
            MP("Or by using parameterised queries, and limiting the database account's permissions", ["parameterised", "prepared statement", "access rights", "permissions", "least privilege"]),
        ], "This is SQL injection. It happens because whatever the user types into the search box is being joined directly into an SQL query and sent to the database, so an attacker can type SQL of their own and have the database execute it, returning data the page was never meant to show. The primary prevention is to stop user input ever being treated as code: use parameterised queries, so the database is told in advance which part of the statement is a value and which is an instruction. Alongside that, input should be validated against what a search term is actually allowed to contain, and the account the website uses to reach the database should have only the permissions the site genuinely needs, so that even a successful injection cannot read the whole customer table.", command="Name"),
        EQ("A school is choosing between a star and a mesh topology for a new building. Discuss the advantages and disadvantages of each, and make a recommendation.", 6, [
            MP("A star gives each device a dedicated connection to a central switch", ["dedicated", "own cable", "central switch"]),
            MP("So it is fast and one cable failure affects only one device", ["fast", "one device", "reliable", "isolated"]),
            MP("But the switch is a single point of failure for the whole network", ["single point of failure", "switch fails", "whole network", "everything stops"]),
            MP("A mesh provides multiple routes between devices", ["multiple routes", "many paths", "several connections", "reroute"]),
            MP("So it is very resilient, but expensive and complex to cable in full", ["resilient", "no single point", "expensive", "complex", "lots of cable"]),
            MP("Reaches a justified recommendation for this situation", ["recommend", "conclusion", "therefore", "star because", "mesh because"]),
        ], "A star topology gives every device its own cable running to a central switch. Nothing is shared, so devices do not compete for the medium and performance stays consistent as machines are added, and a damaged cable disconnects only the one device on it. Extending the network means running one more cable. Its weakness is concentration of risk: everything passes through the switch, so if the switch fails the entire network stops until it is replaced. A mesh topology connects devices to several or all of the others, so there are multiple routes between any two points and traffic can be rerouted automatically around a broken link or a failed device. That resilience is genuine, but a full wired mesh needs an enormous amount of cable, which becomes impractical very quickly: ten devices would need forty five separate links. For a school building the recommendation is a star, and for two reasons specific to the situation. The cost and complexity of a wired mesh cannot be justified for classroom machines where a short outage is inconvenient rather than dangerous, and the failure the school is most likely to experience is a damaged patch lead, which a star already handles. The single point of failure should be managed rather than designed out: keep a spare switch on site, and if the school later adds wireless coverage across the building, a wireless mesh of access points is a sensible way to get resilience where cabling would be difficult.", command="Discuss"),
    ],
)


# ============================================ 5.1 issues and impact

T_IMPACT = Topic(
    slug="issues-and-impact-of-technology",
    title="Issues and Impact of Technology",
    spec="5.1",
    icon="i-shield",
    minutes=28,
    blurb="Environmental, ethical, cultural and privacy impacts of computing, emerging technologies, and a structure for the extended answer that carries the largest marks on Paper 1.",
    fact="Training a single large machine learning model can use as much electricity as several households do in a year. The environmental cost of computing is no longer only about the devices in front of you.",
    sections=[
        Section("Environmental impact", """
### The costs

**Manufacturing.** Devices need rare earth metals, and extracting them uses large amounts of energy and water and frequently causes serious pollution and human harm in the areas where mining happens.

**Energy in use.** Data centres consume very large quantities of electricity, both to run the servers and to cool them, and demand grows every year as more services move online.

**Electronic waste.** Devices are replaced long before they stop working. Much e-waste is exported and dismantled by hand without protection, releasing lead, mercury and cadmium into the ground and into the people doing the work.

### The benefits

**Fewer journeys.** Video conferencing and remote working remove commuting and business travel, and the carbon saved is substantial.

**Less material.** Digital documents, tickets, statements and music remove paper, plastic and physical distribution.

**Better efficiency elsewhere.** Smart meters, route optimisation for delivery fleets and automated building controls all reduce energy use by more than the computing they need consumes.

!exam A balanced answer is required :: An evaluate question about environmental impact that gives only the costs cannot reach the top band. The genuine position is that computing has significant costs and enables significant savings, and the question is whether the savings outweigh them in the case described.
"""),
        Section("Ethical, cultural and privacy issues", """
### Privacy

Almost every service collects data, and much of it is collected as a by-product of use rather than being asked for. Location history, search terms, purchase records and messages together build a picture more detailed than most people realise they have given away.

Three questions run through every privacy issue: **who holds the data**, **what may they do with it**, and **what happens when it leaks**. Data once released cannot be recalled.

### The digital divide

Access to technology is not equal. Cost, connection quality, disability and confidence all affect who can use online services well. As services move online by default, the people least able to access them are often those who most depend on them, and that is a genuine inequality rather than an inconvenience.

### Automation and employment

Automation removes some jobs and creates others, but rarely in the same place or for the same people. A warehouse worker displaced by robotics is not straightforwardly retrained as a robotics engineer, and answers that assume they are miss the actual issue.

### Emerging technologies

**Artificial intelligence and machine learning.** Systems trained on data rather than programmed with rules. They can find patterns people cannot, but they reproduce any bias in their training data and apply it consistently and at scale, which makes bias harder to notice and much larger in effect.

**Autonomous vehicles.** Potentially far safer than human drivers, and mobility for people who cannot drive. They raise unresolved questions about liability in a collision, about employment for professional drivers, and about how a vehicle should behave when harm is unavoidable.

**Wearables and implants.** Fitness trackers, smart watches and medical implants improve health and independence, and simultaneously produce a continuous record of a person's body that somebody else stores.

**Cloud computing.** Convenient, backed up and available anywhere, but personal data sits on servers owned by another company, possibly in another country under different laws, and nothing works without a connection.
"""),
        Section("Writing the extended answer", """
The impacts question carries the largest single mark allocation on Paper 1 and is marked by levels rather than by counting points.

**A structure that reliably reaches the top band:**

1. **One sentence setting out the situation.** Show you understood the question.
2. **The case for**, two or three points, each developed to a consequence.
3. **The case against**, developed to the same standard. This is where most answers thin out.
4. **Who is affected.** The company, the customer, the employee and the wider public want different things, and naming that tension is what top band answers do.
5. **A conclusion that commits.** A judgement, not a summary, and it must follow from what you actually argued.

!key Develop every point :: A claim is half a mark. A claim with a consequence is a whole one. Train yourself to write "which means" after every assertion and the marks follow automatically.

!warn A missing conclusion caps your grade :: However good the arguments, an evaluate question without a conclusion has not been answered. One sentence beginning "On balance" is enough, provided it commits to something.
"""),
    ],
    keyterms=[
        ("Electronic waste", "Discarded electronic equipment, containing toxic materials and often dismantled unsafely."),
        ("Digital divide", "The gap between those with good access to technology and those without."),
        ("Machine learning", "A system trained on data to find patterns, rather than programmed with explicit rules."),
        ("Algorithmic bias", "Unfair outcomes produced when a system learns patterns from biased training data."),
        ("Cloud computing", "Storing data and running software on remote servers owned by a provider."),
        ("Autonomous vehicle", "A vehicle that can drive itself without human control."),
        ("Stakeholder", "A person or group affected by a decision or a technology."),
    ],
    grade="""
This is where the largest marks on Paper 1 are, and where most are lost.

**Develop everything.** Never leave a claim standing on its own. "Data centres use a lot of electricity, which means the carbon cost of a service continues for as long as it runs, not just when it was built."

**Argue both sides even when you have a clear view.** A one sided answer to an evaluate question cannot reach the top band however well written it is.

**Name the stakeholders.** Saying explicitly that the company benefits while the employee bears the cost is the kind of observation that separates top band answers from competent ones.

**Conclude and commit.** The conclusion must follow from your own argument, and it must actually decide something.
""",
    mistakes=[
        "Giving only the negative side of an impacts question.",
        "Listing impacts without developing any into a consequence.",
        "Ending an extended answer without a conclusion.",
        "Treating retraining as a complete answer to job losses from automation.",
        "Assuming cloud storage is automatically safer, when it moves the data into someone else's control.",
    ],
    quiz=[
        Q("Which is an environmental cost of computing?", ["Electricity consumed by data centres for running and cooling servers", "Fewer journeys taken because of video conferencing", "Reduced paper use from digital documents", "Route optimisation for delivery vehicles"], 0,
          "The other three are benefits. Running and cooling large data centres is one of the largest ongoing energy costs of digital services."),
        Q("What is meant by the digital divide?", ["The gap between those with good access to technology and those without", "The difference between analogue and digital signals", "The split between hardware and software companies", "The gap between mobile and desktop performance"], 0,
          "Cost, connection quality, disability and confidence all affect who can use online services, which produces genuine inequality as services move online."),
        Q("Why can a machine learning system produce biased results?", ["It learns patterns from training data, and any bias in that data becomes the pattern", "It is programmed with unfair rules by its developers", "It cannot process numbers accurately", "It always favours the most recent data"], 0,
          "The system has no concept of fairness. It reproduces whatever relationship exists in the data it was shown, including historic bias."),
        Q("Why is algorithmic bias potentially more serious than an individual's bias?", ["The same bias is applied consistently to everyone the system processes", "Machines cannot be corrected", "It only affects online services", "It is always illegal"], 0,
          "One biased interviewer affects the people they meet. One biased system affects every application it processes, which makes the effect far larger and harder to see."),
        Q("Which is a genuine ethical issue raised by autonomous vehicles?", ["Deciding who is liable when the vehicle causes a collision", "That they cannot be manufactured at scale", "That they use more fuel than human driven cars", "That they require passengers to hold a licence"], 0,
          "Responsibility for a collision is genuinely unresolved when no human was driving, which makes it both an ethical and a legal question."),
        Q("What is a disadvantage of storing personal data in the cloud?", ["The data is held by another company, possibly under a different country's laws", "It cannot be backed up", "It can only be accessed from one device", "It cannot be encrypted"], 0,
          "Convenience comes at the cost of control: the data sits on infrastructure the user does not own, in a jurisdiction they may not have chosen."),
        Q("Why is electronic waste an environmental problem?", ["It contains toxic materials and is often dismantled unsafely", "It takes up too much space in offices", "It cannot be transported", "It is always incinerated in the UK"], 0,
          "Lead, mercury and cadmium in discarded devices are released when equipment is broken up by hand without protection, which is common where e-waste is exported."),
        Q("Which is an environmental benefit of computing?", ["Video conferencing removing the need to travel", "Rare metal extraction for device manufacture", "Growth in data centre electricity use", "Exporting electronic waste"], 0,
          "Removing journeys avoids carbon that would otherwise have been emitted, and the saving is often much larger than the energy the meeting itself uses."),
        Q("What must an extended evaluate answer contain to reach the top band?", ["Developed arguments on both sides and a justified conclusion", "The maximum possible number of separate points", "Only the strongest side of the argument", "A list of relevant legislation"], 0,
          "Evaluation means weighing both sides and then committing to a judgement that follows from the argument made."),
        Q("Why is 'they can be retrained' an incomplete answer to job losses from automation?", ["The new jobs are often in different places and need different skills from the ones lost", "Retraining is illegal in the UK", "Automation never removes jobs", "New jobs always pay less"], 0,
          "Automation creates work, but rarely for the same people in the same place, and treating retraining as automatic ignores the actual difficulty."),
    ],
    exam=[
        EQ("State two environmental impacts of the increasing use of computer technology.", 2, [
            MP("A negative impact such as energy use by data centres, e-waste or resource extraction", ["energy", "electricity", "data centres", "e-waste", "waste", "mining", "rare metals"]),
            MP("A positive impact such as fewer journeys or less paper", ["travel", "journeys", "video conferencing", "paper", "commuting", "digital documents"]),
        ], "One negative impact is the very large amount of electricity consumed by data centres, both to run servers and to cool them, which continues for as long as a service exists. One positive impact is the reduction in travel that video conferencing and remote working allow, which removes carbon that would otherwise have been emitted by commuting and business flights.", command="State"),
        EQ("Explain why an artificial intelligence system used to shortlist job applicants might produce unfair results.", 4, [
            MP("The system is trained on historic data from the organisation", ["trained", "training data", "historic", "past", "previous"]),
            MP("That data reflects past decisions which may themselves have been biased", ["biased data", "past bias", "mostly one group", "reflects", "unfair decisions"]),
            MP("The system learns the statistical pattern rather than judging fairness", ["learns the pattern", "no understanding", "copies", "statistical", "does not know"]),
            MP("So the bias is reproduced and applied to every application, at scale", ["reproduces", "every application", "at scale", "consistently", "amplifies"]),
        ], "A shortlisting system is trained on data about who the organisation has hired and promoted before. If those past decisions favoured one group, then the pattern present in the data is that successful candidates resemble that group, and that is precisely the pattern the system will learn. It has no concept of fairness and no way of knowing that the historic decisions were themselves unfair: it simply identifies the statistical relationship in what it was shown and applies it. The result is that a bias which previously depended on which manager happened to read an application is now applied identically to every single application, which makes it far larger in effect and much harder to detect, because the system produces a consistent and apparently objective output.", command="Explain"),
        EQ("A council plans to move all its services online, closing most of its physical offices. Evaluate this decision.", 8, [
            MP("Online services are available at any time without travelling", ["any time", "24 hours", "no travel", "from home", "convenient"]),
            MP("The council saves money on buildings and staff, which can be spent elsewhere", ["saves money", "cheaper", "buildings", "budget", "costs less"]),
            MP("There is an environmental benefit from fewer journeys and less paper", ["fewer journeys", "carbon", "paper", "environment", "travel"]),
            MP("Some residents have no reliable internet access or device", ["no internet", "no device", "cannot afford", "poor connection", "access"]),
            MP("Some residents lack the confidence or ability to use online services, including older and disabled people", ["confidence", "skills", "older", "disabled", "cannot use", "digital literacy"]),
            MP("The people most affected are often those who depend most on council services", ["most in need", "vulnerable", "depend", "rely on", "worst affected"]),
            MP("Personal data held online carries a security and privacy risk", ["data", "security", "breach", "privacy", "hacked"]),
            MP("Reaches a justified conclusion, such as moving online while retaining some access route", ["conclusion", "on balance", "should", "keep some", "hybrid", "telephone", "one office"]),
        ], "There is a strong practical case. Online services are available at any hour without anyone having to travel or take time off work, which suits most residents better than an office open between nine and five. Closing buildings removes rent, heating and reception staffing costs, and a council under financial pressure can redirect that money into services rather than premises. There is a genuine environmental benefit too, since thousands of individual journeys and a large volume of printed forms disappear. The case against rests on who is excluded. A significant minority of residents have no reliable internet connection or no suitable device, and cost is the usual reason. A further group has access but not confidence, and that group is disproportionately older residents, people with disabilities affecting sight or dexterity, and people whose first language is not English. The difficulty is that these are frequently the same residents who most depend on council services such as housing, social care and benefits, so a decision framed as efficiency lands hardest on the people least able to absorb it. Concentrating personal data in online systems also creates a single valuable target, and a breach would expose exactly the sensitive information residents had no realistic choice about handing over. Different groups are affected very differently, and that matters to the judgement. The council gains, most residents gain convenience, and a minority loses access to services they are entitled to. On balance the council should move services online, because the benefits to the majority and to its budget are real, but it should not close every route in. It should keep a staffed telephone line and at least one physical office covering the whole area, fund assisted digital support through libraries and community centres, and commit to publishing how many residents use each route so that the decision can be revisited on evidence rather than on assumption.", command="Evaluate"),
    ],
)


# ============================================ 5.2 legislation

T_LAW = Topic(
    slug="legislation-and-privacy",
    title="Legislation and Privacy",
    spec="5.2",
    icon="i-shield",
    minutes=24,
    blurb="The Acts you must be able to name and apply, what each one actually makes unlawful, and the difference between open source and proprietary software licensing.",
    fact="The Computer Misuse Act exists because of a prosecution that failed. Two journalists accessed a mailbox belonging to the Duke of Edinburgh in 1984, and the courts found no law clearly covered it. Parliament wrote one.",
    sections=[
        Section("The Acts", """
### Data Protection Act 2018

Governs how organisations collect, store and use **personal data**, implementing the UK's version of GDPR. Data must be:

- processed lawfully, fairly and transparently,
- collected for a specified purpose and not used for an unrelated one,
- adequate and limited to what is necessary,
- accurate and kept up to date,
- kept no longer than necessary,
- kept secure.

It also gives individuals the right to see the data held about them, to have inaccurate data corrected, to have data erased where there is no longer good reason to keep it, and to object to certain uses.

### Computer Misuse Act 1990

Creates three offences:

1. **Unauthorised access** to computer material.
2. **Unauthorised access with intent** to commit a further offence.
3. **Unauthorised modification** of computer material, which covers deleting files and spreading malware.

The decisive word in all three is *unauthorised*. Penetration testing carried out with written permission is lawful; the identical actions without permission are not.

### Copyright, Designs and Patents Act 1988

Protects the creator's ownership of original work, including software, music, images, video and text. Copying, distributing or adapting protected work without permission is an infringement. Software is protected as a literary work, which is what gives licence terms legal force.

!exam Apply the Act, do not just name it :: "This is an offence under section 1 of the Computer Misuse Act 1990, because the employee accessed records they had no authorisation to see" is a full answer. "It is illegal" is not.
"""),
        Section("Software licensing", """
**Proprietary** software is supplied under a licence that restricts what you may do with it. The source code is not provided, you may not modify or redistribute it, and the number of installations is usually limited.

**Open source** software is supplied with its source code, under a licence permitting use, modification and redistribution.

| | Proprietary | Open source |
| Source code | Not provided | Provided |
| Modification | Not permitted | Permitted |
| Redistribution | Not permitted | Permitted |
| Cost | Usually paid | Usually free of charge |
| Support | From the vendor, often contractual | From the community, no guarantee |
| Development | By one company on its own schedule | By anyone, often faster on fixes |

!warn Open source does not mean free of charge :: It means the source is open. Some open source software is sold with a support contract, and plenty of free software is not open source at all. Edexcel distinguishes the two.

### Choosing between them

For a school, the argument for open source is cost and freedom to install on any number of machines. The argument against is support: nobody is contractually obliged to fix anything, so the school depends on its own technical staff. For a hospital running critical systems, a support contract with guaranteed response times may be worth far more than the licence fee saved.
"""),
        Section("Privacy in practice", """
Legislation sets the floor. In practice, most privacy loss happens through choices that are entirely lawful.

**Data collected as a by-product.** Location history, search terms and browsing are collected because the service works better with them, and then retained.

**Consent that is not really a choice.** A service that is unusable without agreeing to tracking has not obtained a meaningful choice, which is why data protection law requires consent to be freely given.

**Aggregation.** Individually harmless pieces of data combine into something that is not. Where you are each morning, what you buy, who you message and what you search for together identify you far more precisely than any single one of them.

**Permanence.** Data once released cannot be recalled. A leaked dataset is copied within hours, and no legal remedy puts it back.

!key The three questions worth asking of any system :: What data is collected, who can see it, and what happens when it leaks. An answer that addresses all three is complete, and one that addresses only the first is not.
"""),
    ],
    keyterms=[
        ("Data Protection Act 2018", "Legislation governing how organisations collect, store and use personal data."),
        ("Personal data", "Information that can be used to identify a living individual."),
        ("Computer Misuse Act 1990", "Legislation creating offences of unauthorised access to and modification of computer material."),
        ("Copyright, Designs and Patents Act 1988", "Legislation protecting ownership of original work, including software."),
        ("Proprietary software", "Software supplied without source code under a licence restricting modification and redistribution."),
        ("Open source software", "Software supplied with source code under a licence permitting modification and redistribution."),
        ("Consent", "Permission that must be freely given, specific and informed for data processing to be lawful."),
    ],
    grade="""
Legislation questions are applied questions, and the marks are for applying rather than reciting.

**Name the Act and the specific breach.** Which Act, which principle or offence, and which fact in the scenario triggers it.

**Distinguish the Acts cleanly.** Personal data is the Data Protection Act. Unauthorised access is the Computer Misuse Act. Copying software or music is the Copyright Act. Mixing them up loses the mark even when the reasoning is sound.

**Get licensing right.** Open source means the source is available and may be modified, not that it costs nothing, and the disadvantage that carries marks is the absence of guaranteed support.
""",
    mistakes=[
        "Saying open source means free of charge.",
        "Using the Data Protection Act for a hacking scenario, or the Computer Misuse Act for a data handling one.",
        "Saying an organisation may keep personal data indefinitely. It must be kept no longer than necessary.",
        "Forgetting that authorisation is what makes penetration testing lawful.",
        "Naming an Act without saying what in the scenario breaches it.",
    ],
    quiz=[
        Q("Under which Act would somebody be prosecuted for accessing a school system without permission?", ["Computer Misuse Act 1990", "Data Protection Act 2018", "Copyright, Designs and Patents Act 1988", "Communications Act 2003"], 0,
          "Unauthorised access to computer material is the first offence created by the Computer Misuse Act."),
        Q("Which Act requires that personal data is kept no longer than necessary?", ["Data Protection Act 2018", "Computer Misuse Act 1990", "Copyright, Designs and Patents Act 1988", "Consumer Rights Act 2015"], 0,
          "Storage limitation is one of the data protection principles, alongside accuracy, security and purpose limitation."),
        Q("What is the defining feature of open source software?", ["The source code is provided and may be modified and redistributed", "It costs nothing in every case", "It has no licence at all", "It cannot be used by businesses"], 0,
          "Openness of the source and the freedoms to modify and redistribute define it. Cost is a separate question."),
        Q("What is a disadvantage of open source software for an organisation running critical systems?", ["There is no contractual guarantee that a fault will be fixed within a set time", "The source code cannot be inspected", "It cannot be installed on more than one machine", "It is always more expensive"], 0,
          "Community support has no obligation to respond, which is exactly what a vendor support contract provides and why some organisations pay for one."),
        Q("Sharing a paid film with thousands of people online would breach which Act?", ["Copyright, Designs and Patents Act 1988", "Computer Misuse Act 1990", "Data Protection Act 2018", "Freedom of Information Act 2000"], 0,
          "Distributing a protected work without the owner's permission is a copyright infringement."),
        Q("What makes penetration testing lawful?", ["It is carried out with the system owner's authorisation", "It is done by a qualified professional", "It only tests weaknesses that are already public", "It never accesses real data"], 0,
          "Every Computer Misuse Act offence turns on access being unauthorised, so written permission is what separates testing from an offence."),
        Q("Which right does the Data Protection Act give an individual?", ["The right to have inaccurate data about them corrected", "The right to access any organisation's database", "The right to be paid for their data", "The right to prevent all data collection by law"], 0,
          "Rectification is one of the individual rights, alongside access, erasure and objection."),
        Q("What is meant by personal data?", ["Information that can be used to identify a living individual", "Any data stored on a personal device", "Data belonging to a private company", "Data that has been encrypted"], 0,
          "The test is identifiability. A name with an address, a date of birth or an email address all identify a living person."),
        Q("Why is consent required to be freely given under data protection law?", ["A service that is unusable without agreeing has not offered a real choice", "Written consent takes longer to obtain", "It reduces the amount of data collected", "It is required by the Computer Misuse Act"], 0,
          "Consent obtained by making the service unusable otherwise is not meaningful, which is why the law sets that condition."),
        Q("Why is aggregation of data a privacy concern?", ["Individually harmless pieces of data combine into something that identifies a person precisely", "Aggregated data takes more storage", "It makes data harder to encrypt", "It slows down database queries"], 0,
          "Location, purchases, messages and searches are each limited alone, but together they build a far more revealing picture than any one of them."),
    ],
    exam=[
        EQ("State two principles of the Data Protection Act 2018.", 2, [
            MP("Data must be collected for a specified purpose and used only for that purpose", ["specified purpose", "not used for another", "limited purpose", "stated reason"]),
            MP("Data must be kept secure, accurate, or no longer than necessary", ["secure", "accurate", "up to date", "no longer than necessary", "not kept forever"]),
        ], "Personal data must be collected for a specified and lawful purpose and not then used for an unrelated one. It must also be kept secure, kept accurate and up to date, and retained no longer than is necessary for the purpose it was collected for.", command="State"),
        EQ("An employee at a hospital looks up the medical records of a neighbour who is not their patient. Explain which law this breaches and why.", 4, [
            MP("Identifies the Computer Misuse Act 1990", ["computer misuse", "misuse act"]),
            MP("Because the access was unauthorised, even though the employee has a legitimate account", ["unauthorised", "no permission", "not entitled", "outside their role", "no right"]),
            MP("Identifies the Data Protection Act 2018", ["data protection", "gdpr"]),
            MP("Because the personal data was used for a purpose other than the one it was collected for", ["purpose", "not the reason", "unrelated", "not for treatment", "misuse of data"]),
        ], "This breaches the Computer Misuse Act 1990, specifically the offence of unauthorised access to computer material. It does not matter that the employee has a legitimate account on the system: their authorisation extends only to the records they need for their own work, and accessing a record outside that is access they were not authorised to make. It also breaches the Data Protection Act 2018, because the neighbour's medical data was collected for the purpose of providing their care and was then used for an entirely unrelated personal purpose, which is not lawful, fair or transparent processing. The hospital itself may also be at fault if its access controls did not limit staff to the records their role requires.", command="Explain"),
        EQ("Explain one advantage and one disadvantage for a small business of using open source software instead of proprietary software.", 4, [
            MP("Open source software is usually free of licence charges", ["free", "no licence fee", "cost", "cheaper"]),
            MP("So it can be installed on any number of machines and the money spent elsewhere", ["any number", "all machines", "saves money", "budget", "spend elsewhere"]),
            MP("Support comes from the community rather than a vendor", ["community", "forums", "no vendor", "volunteers"]),
            MP("So there is no guaranteed response if something goes wrong, and more technical skill may be needed in house", ["no guarantee", "response time", "own staff", "technical skill", "no contract"]),
        ], "The advantage is cost and freedom of use. Open source software normally carries no licence fee and may be installed on as many machines as the business needs without counting them, so a small business can equip itself for nothing and spend the saved money on something else. It can also be modified if the business has, or can hire, the expertise. The disadvantage is support. Proprietary software is usually sold with a support contract that obliges the vendor to respond within an agreed time, whereas open source support comes from community forums where nobody has any obligation to help. If a critical system fails on a busy day the business is dependent on whatever technical skill it has in house, and for a small business that may be nobody at all.", command="Explain"),
        EQ("A fitness app collects location data continuously and sells it, in a form the company describes as anonymous, to advertisers. Discuss the privacy issues this raises.", 6, [
            MP("Continuous location data is highly revealing about a person's life", ["revealing", "where they live", "routine", "detailed", "sensitive"]),
            MP("Users may not realise how much is collected or what it is used for", ["not realise", "unaware", "buried in terms", "did not know", "transparency"]),
            MP("Consent must be freely given, specific and informed to be lawful", ["consent", "freely given", "informed", "specific", "lawful"]),
            MP("Anonymised location data can often be re-identified from patterns", ["re-identified", "identify", "pattern", "home and work", "not truly anonymous"]),
            MP("The Data Protection Act requires a specified purpose and adequate security", ["data protection", "purpose", "secure", "gdpr", "principles"]),
            MP("Reaches a reasoned conclusion about what the company should do", ["conclusion", "should", "therefore", "opt in", "clear", "stop", "recommend"]),
        ], "Continuous location data is among the most revealing information a person can give away. Where a phone spends every night is a home address, where it spends every weekday is a workplace or a school, and a regular visit to a particular clinic or place of worship reveals things a person may never have chosen to disclose. Users are unlikely to appreciate that when they install a fitness app, because the collection is a by-product of a feature they wanted and the resale is described in terms almost nobody reads. That matters legally as well as ethically: data protection law requires consent to be freely given, specific and informed, and consent buried in a long agreement for a purpose the user did not anticipate does not meet that standard. The company's claim that the data is anonymous deserves particular scrutiny. Stripping names from location traces does not make them anonymous, because the pattern itself identifies the person: the combination of one home and one workplace is close to unique. Data sold as anonymous can therefore be re-identified, at which point the protection the company relied on has never existed. The company should stop selling location data by default. If it wants to offer it commercially, it should be a separate, clearly explained, opt-in choice that is not required to use the app, the data should be genuinely aggregated rather than merely de-named, and the company should be able to show that it meets the requirements of purpose limitation and security under the Data Protection Act 2018.", command="Discuss"),
    ],
)


# ============================================ 6.2 programming in Python

T_PYFUND = Topic(
    slug="programming-fundamentals-in-python",
    title="Programming Fundamentals in Python",
    spec="6.2",
    icon="i-python",
    minutes=32,
    blurb="Everything Paper 2 assumes you can do without thinking: variables and types, every operator, the three constructs, and reading input safely. Every example here runs in the browser.",
    fact="Paper 2 is sat on a computer with Python 3 and a folder of starter files. You are not marked on remembering syntax you could look up, you are marked on producing a program that works, which is why practising by typing is the only preparation that counts.",
    sections=[
        Section("Variables, constants and data types", """
A **variable** is a named location whose value can change. Python creates one the moment you assign to it.

```python
name = "Amira"
age = 15
average = 68.4
member = True
```

Python decides the type from the value: `str`, `int`, `float` and `bool` respectively. Check one with `type()`.

A **constant** is a value that should not change. Python has no separate keyword for one, so the convention is a name in capitals, and the convention is what the exam expects to see.

```python
VAT_RATE = 0.2
MAX_ATTEMPTS = 3
```

### Reading input

```python
name = input("What is your name? ")
age = int(input("How old are you? "))
```

!warn input() always returns a string :: Even when the user types 15, what comes back is the two characters "1" and "5". Comparing that with a number or doing arithmetic on it will not behave as you expect, which is why `int()` or `float()` wraps it. This is the single most common cause of a Paper 2 program not working.

### Output

```python
score = 7
total = 10
print("You scored", score, "out of", total)
print(f"You scored {score} out of {total}")
```

The second form is an f-string, and it is the clearer one once a message contains more than a couple of values.
"""),
        Section("Operators", """
### Arithmetic

| Operator | Meaning | Example | Result |
| `+` | Add | `7 + 2` | `9` |
| `-` | Subtract | `7 - 2` | `5` |
| `*` | Multiply | `7 * 2` | `14` |
| `/` | Divide, always giving a float | `7 / 2` | `3.5` |
| `//` | Integer division | `7 // 2` | `3` |
| `%` | Modulus, the remainder | `7 % 2` | `1` |
| `**` | To the power of | `2 ** 3` | `8` |

`//` and `%` are worth real marks. `seconds // 60` gives whole minutes, `seconds % 60` gives the seconds left over, `n % 2 == 0` tests for even, and `n % 10` gives the last digit.

### Comparison

`==` equal to, `!=` not equal to, `<`, `>`, `<=`, `>=`. Each of these produces a Boolean.

!warn One equals sign assigns, two compare :: `x = 5` puts 5 into x. `x == 5` asks whether x holds 5. Writing one where you meant the other is the most common single error in Python.

### Logical

`and` is True only if both sides are True. `or` is True if at least one is. `not` reverses.

```python
if age >= 13 and age <= 19:
    print("teenager")
```

`if grade == "A" or "B":` does not work. Each side of `or` must be a complete comparison, so it has to be `if grade == "A" or grade == "B":`.
"""),
        Section("Sequence, selection and iteration", """
### Sequence

Statements run in the order written. A variable must be given a value before it is used.

### Selection

```python
mark = int(input("Enter the mark: "))

if mark >= 70:
    grade = "Distinction"
elif mark >= 50:
    grade = "Merit"
elif mark >= 40:
    grade = "Pass"
else:
    grade = "Fail"

print(f"Grade: {grade}")
```

The order of the conditions is doing real work. A mark of 80 satisfies all three tests and gets Distinction only because that test is first. Reverse them and every passing student gets a Pass.

!warn Indentation is the syntax :: Python uses indentation to decide what is inside an `if` or a loop. A line indented by the wrong amount is a different program, not an untidy one.

### Iteration

**Count controlled**, when the number of repeats is known:

```python
for i in range(1, 6):
    print(i, i * i)

for letter in "PYTHON":
    print(letter)
```

`range(1, 6)` gives 1, 2, 3, 4, 5. It stops **before** the second number, which is the detail that causes most off by one errors.

**Condition controlled**, when it is not:

```python
total = 0
number = int(input("Enter a number, or 0 to stop: "))
while number != 0:
    total = total + number
    number = int(input("Enter a number, or 0 to stop: "))
print("Total:", total)
```

Two things make a while loop work: the variable in the condition must have a value before the loop starts, and something inside the loop must be able to change it. Miss either and you have an infinite loop.
"""),
    ],
    keyterms=[
        ("Variable", "A named location in memory whose value can change while the program runs."),
        ("Constant", "A value that should not change, written by convention in capitals in Python."),
        ("Casting", "Converting a value from one data type to another, such as int() on a string."),
        ("Operator", "A symbol representing an operation, such as arithmetic, comparison or logic."),
        ("Integer division", "Division giving only the whole number part, written // in Python."),
        ("Modulus", "The remainder after an integer division, written % in Python."),
        ("Selection", "Choosing between paths through a program using if, elif and else."),
        ("Iteration", "Repeating statements, using for when the count is known and while when it is not."),
        ("f-string", "A Python string prefixed with f, in which values in braces are substituted."),
    ],
    grade="""
Paper 2 is marked on a program that works, so the habits that matter are the ones that prevent it not working.

**Cast every input immediately.** Write `int(input(...))` as one line rather than converting later, and the whole class of type error disappears.

**Test the boundaries yourself.** Run your program with the smallest and largest allowed value, and with one either side. Almost every logic error in a graded task shows up at a boundary and nowhere else.

**Name variables so the code reads.** `total_price` rather than `tp`. It costs three seconds and it is credited under maintainability.

**Trace before you rewrite.** When a program gives the wrong answer, add a print statement showing the value of the variable you suspect. Guessing at changes takes longer and usually introduces a second fault.
""",
    mistakes=[
        "Using = where == was meant, or the reverse.",
        "Forgetting to cast input() before doing arithmetic or a numeric comparison.",
        "Writing if x == 1 or 2. Each side of or must be a complete comparison.",
        "Expecting range(1, 5) to include 5. It stops before the second number.",
        "Changing the indentation of a line and assuming it makes no difference. In Python it changes what the line belongs to.",
    ],
    quiz=[
        Q("What is the value of 17 // 5 in Python?", ["3", "3.4", "2", "85"], 0,
          "The double slash is integer division, giving only the whole number part. Five goes into seventeen three times."),
        Q("What is the value of 17 % 5?", ["2", "3", "3.4", "12"], 0,
          "The percent sign gives the remainder. Five goes into seventeen three times with two left over."),
        Q("What does input() always return?", ["A string", "An integer", "A float", "The type the user typed"], 0,
          "Whatever the user types comes back as a string, which is why it must be cast before arithmetic or a numeric comparison."),
        Q("Which values does range(1, 5) produce?", ["1, 2, 3, 4", "1, 2, 3, 4, 5", "0, 1, 2, 3, 4", "1, 5"], 0,
          "range stops before the second number, so it produces 1, 2, 3 and 4."),
        Q("What is wrong with if grade == 'A' or 'B':?", ["The right hand side of or is not a complete comparison", "or is not valid in Python", "Strings cannot be compared", "grade has not been defined"], 0,
          "Each side of a logical operator must be a full condition, so it must be written if grade == 'A' or grade == 'B':."),
        Q("What does n % 2 == 0 test?", ["Whether n is even", "Whether n is positive", "Whether n is a whole number", "Whether n is greater than 2"], 0,
          "Dividing by two leaves no remainder exactly when the number is even, so this is the standard test for evenness."),
        Q("Which loop should be used when the number of repeats is not known in advance?", ["A while loop", "A for loop", "A range loop", "Either, they behave identically"], 0,
          "A while loop repeats for as long as its condition is True, which is what condition controlled iteration means."),
        Q("Why does Python indentation matter?", ["It decides which statements are inside an if or a loop", "It is only a style convention", "It affects how fast the program runs", "It determines the data type"], 0,
          "Indentation is part of Python's syntax. Changing it changes what the statement belongs to, which changes what the program does."),
        Q("What is the result of print('5' + '3') in Python?", ["53", "8", "An error", "5 3"], 0,
          "Both values are strings, so the plus sign joins them rather than adding them, which is exactly what happens when input is not cast."),
        Q("Why should a while loop's condition variable be given a value before the loop?", ["Otherwise the condition cannot be evaluated and the program fails", "So the loop runs faster", "To make the loop count controlled", "So indentation is correct"], 0,
          "The condition is tested before the first pass, so the variable it uses must already exist and hold a sensible value."),
    ],
    exam=[
        EQ("State the difference between a variable and a constant.", 2, [
            MP("A variable's value can change while the program is running", ["variable", "can change", "changes", "altered"]),
            MP("A constant holds a value that should not change while the program runs", ["constant", "does not change", "fixed", "stays the same"]),
        ], "A variable is a named location whose value can be changed while the program is running. A constant holds a value that is fixed and should not be changed during the run, and in Python this is shown by writing the name in capitals.", command="State"),
        EQ("Write a Python program that asks the user for a number of seconds and prints the equivalent number of whole minutes and remaining seconds.", 4, [
            MP("Reads input and casts it to an integer", ["int(input", "int(", "cast", "convert"]),
            MP("Uses integer division to find the minutes", ["//", "// 60", "integer division"]),
            MP("Uses modulus to find the remaining seconds", ["%", "% 60", "modulus", "remainder"]),
            MP("Prints both values with a clear message", ["print", "output", "message"]),
        ], "A correct program is: total = int(input(\"Enter the number of seconds: \")) then minutes = total // 60 then seconds = total % 60 then print(f\"That is {minutes} minutes and {seconds} seconds\"). The input must be cast with int() because input returns a string, integer division gives the number of complete minutes, and the modulus gives what is left over after those whole minutes have been taken out.", command="Write"),
        EQ("Explain the difference between a for loop and a while loop, and give one situation in which each would be the better choice.", 4, [
            MP("A for loop repeats a known number of times", ["known", "fixed", "set number", "count controlled", "in advance"]),
            MP("A while loop repeats while a condition is True, for an unknown number of repeats", ["condition", "while true", "unknown", "until", "not known"]),
            MP("Gives a sensible for loop use, such as processing every item in a list", ["list", "each item", "every element", "known length", "ten times"]),
            MP("Gives a sensible while loop use, such as validating input until it is acceptable", ["validation", "until valid", "password", "keeps asking", "user enters"]),
        ], "A for loop repeats a number of times that is known before the loop starts, which is why it is called count controlled. Working through every item in a list of forty names is a for loop task, because the length of the list is known. A while loop repeats for as long as its condition remains True, and the number of repeats is not known in advance, which makes it condition controlled. Repeatedly asking a user to enter a value until they enter a valid one is a while loop task, because there is no way to know how many attempts they will need.", command="Explain"),
        EQ("A student writes age = input(\"How old are you? \") and then if age >= 18:. The program crashes. Explain why and how to correct it.", 3, [
            MP("input returns a string, so age holds text rather than a number", ["string", "text", "not a number", "characters"]),
            MP("Comparing a string with an integer causes a type error in Python", ["type error", "cannot compare", "different types", "crashes", "error"]),
            MP("Cast the input to an integer, for example age = int(input(...))", ["int(", "cast", "convert", "int(input"]),
        ], "The input function always returns a string, so after the first line age holds the characters the user typed rather than a number. The comparison then asks Python to decide whether a string is greater than or equal to an integer, which is not a comparison Python can make, so it raises a TypeError and the program stops. The correction is to convert the input as it is read, by writing age = int(input(\"How old are you? \")), after which the comparison is between two integers and works as intended.", command="Explain"),
    ],
)


# ============================================ 6.2 data structures and files

T_PYDATA = Topic(
    slug="lists-strings-and-files-in-python",
    title="Lists, Strings and Files in Python",
    spec="6.2",
    icon="i-layers",
    minutes=30,
    blurb="One dimensional and two dimensional lists, every string operation Paper 2 expects, and reading and writing text files, with the off by one traps that break more programs than anything else.",
    fact="Python counts from zero because an index is really an offset from the start of the data. The first item sits zero places along, which is also why a slice like [0:3] gives three items and stops before index 3.",
    sections=[
        Section("Lists", """
A **list** holds many values under one name, each found by its **index**, counted from 0.

```python
scores = [14, 9, 21, 6, 18]
print(scores[0])
print(scores[-1])
scores[3] = 11
print(len(scores))
```

`scores[0]` is 14 and `scores[-1]` is the last item. `len(scores)` is 5, and the last index is 4.

!warn len gives the count, not the last index :: A five item list has len 5 and a highest index of 4. Looping to len(scores) runs one step too far and raises an IndexError.

### Working through a list

```python
total = 0
for score in scores:
    total = total + score
print("Average:", total / len(scores))
```

Loop over the items when you only need the values. Loop over `range(len(scores))` when you need the index as well, for example to change items in place.

### Useful list operations

```python
scores.append(25)
scores.insert(0, 3)
scores.remove(9)
value = scores.pop()
scores.sort()
print(max(scores), min(scores), sum(scores))
```

### Two dimensional lists

A list of lists, useful for anything grid shaped.

```python
board = [[1, 0, 0],
         [0, 1, 0],
         [0, 0, 1]]

print(board[1][2])

for row in board:
    for cell in row:
        print(cell, end=" ")
    print()
```

The first index selects the row, the second the position within it.
"""),
        Section("Strings", """
A string is a sequence of characters, indexed from 0 just like a list.

```python
word = "Computing"
print(len(word))
print(word[0])
print(word[0:3])
print(word[-1])
print(word.upper())
print(word.lower())
print(word.find("put"))
print(word.replace("ing", "er"))
print("put" in word)
```

`word[0:3]` is a **slice**, and it gives characters 0, 1 and 2. Like `range`, a slice stops **before** the second number.

### Splitting and joining

```python
line = "Amira,15,Year 10"
parts = line.split(",")
print(parts[0])
joined = "-".join(parts)
```

`split` is how you take a line read from a file apart, and it is needed in almost every Paper 2 task that involves a data file.

### Characters as numbers

```python
print(ord("A"))
print(chr(66))
```

`ord` gives the character set code and `chr` converts back, which is how case conversion and simple ciphers are done.
"""),
        Section("Files", """
A program that forgets everything when it closes is of limited use. Writing to a file makes data persist between runs.

### Reading

```python
file = open("scores.txt", "r")
for line in file:
    print(line.strip())
file.close()
```

`strip()` removes the newline character at the end of each line, and forgetting it is why comparisons against read values so often fail.

The safer form closes the file for you even if something goes wrong:

```python
with open("scores.txt", "r") as file:
    lines = file.readlines()
```

### Writing

```python
with open("scores.txt", "w") as file:
    file.write("Amira,18\\n")
    file.write("Ben,14\\n")
```

!warn "w" destroys the existing file :: Opening in write mode empties the file before you write anything. Use `"a"` to append to the end and keep what is already there. Losing a data file this way in a Paper 2 task costs a great deal of time.

### Putting it together

```python
totals = {}
with open("scores.txt", "r") as file:
    for line in file:
        parts = line.strip().split(",")
        name = parts[0]
        score = int(parts[1])
        totals[name] = score

for name in totals:
    print(name, totals[name])
```

Note the `int()` on the score. Everything read from a text file is a string, every time.
"""),
    ],
    keyterms=[
        ("List", "A Python data structure holding many values under one name, accessed by index."),
        ("Index", "The position of an item, counted from zero."),
        ("Two dimensional list", "A list whose items are themselves lists, used for grids and tables."),
        ("Slice", "A section of a list or string taken between two indexes, stopping before the second."),
        ("split", "A string method that divides a string into a list at a given separator."),
        ("strip", "A string method that removes whitespace, including the newline, from both ends."),
        ("append", "A list method that adds an item to the end."),
        ("Append mode", "Opening a file with \"a\" so that new data is added to the end rather than replacing it."),
    ],
    grade="""
Paper 2 tasks are almost always list or file tasks, so the details here are worth more than anywhere else.

**Strip and cast every line you read.** `int(line.strip())` handles both the newline and the type in one step, and skipping either produces a fault that is hard to see because the value looks correct when printed.

**Use len(list) - 1 when you need the last index.** Write it deliberately rather than by habit, and check it against a small example.

**Choose the loop that matches what you need.** `for item in list` when you only need values, `for i in range(len(list))` when you need to change items in place.

**Open files in the right mode.** Reading is `"r"`, appending is `"a"`, and `"w"` empties the file first. Say why you chose the mode if a question asks.
""",
    mistakes=[
        "Looping to len(list) rather than len(list) - 1 when using range with an index.",
        "Forgetting strip(), so a value read from a file carries a newline and never matches.",
        "Forgetting to cast a value read from a file before doing arithmetic with it.",
        "Opening a file in \"w\" mode when you meant to add to it, which deletes the existing contents.",
        "Expecting a slice like word[0:3] to include index 3. It stops before it.",
    ],
    quiz=[
        Q("A list called names holds 8 items. What is the index of the last one?", ["7", "8", "9", "0"], 0,
          "Indexes start at zero, so eight items occupy positions 0 to 7. The last index is always len minus one."),
        Q("What does scores[-1] return?", ["The last item in the list", "The first item", "An error", "The length of the list"], 0,
          "A negative index counts back from the end, so -1 is the last item and -2 the one before it."),
        Q("What does 'Computing'[0:3] give?", ["'Com'", "'Comp'", "'omp'", "'C'"], 0,
          "A slice starts at the first index and stops before the second, so it gives characters 0, 1 and 2."),
        Q("What does 'Amira,15'.split(',') return?", ["['Amira', '15']", "'Amira 15'", "['Amira,15']", "('Amira', 15)"], 0,
          "split divides the string at each occurrence of the separator and returns a list of the pieces, all of them strings."),
        Q("Why is strip() usually needed on a line read from a text file?", ["It removes the newline character at the end of the line", "It converts the line to an integer", "It splits the line into parts", "It closes the file"], 0,
          "Each line read from a file carries the newline that ended it, and that invisible character makes comparisons fail."),
        Q("What happens if a file is opened with mode 'w' when it already exists?", ["Its existing contents are deleted before anything is written", "The new data is added to the end", "An error is raised", "The file is opened read only"], 0,
          "Write mode truncates the file to empty first. Append mode, 'a', is what adds to the end."),
        Q("In a two dimensional list called grid, what does grid[2][0] refer to?", ["The first item of the third row", "The third item of the first row", "The second row, first column, counting from one", "An error, since two indexes are not allowed"], 0,
          "The first index selects the row and the second the position within it, both counted from zero."),
        Q("Which method adds an item to the end of a list?", ["append", "insert", "add", "extend"], 0,
          "append adds a single item to the end. insert places one at a given position, and extend joins another list on."),
        Q("Why must a number read from a text file be converted before it is used in a calculation?", ["Everything read from a text file is a string", "Files store numbers in hexadecimal", "Python cannot add two numbers from a file", "The file must be closed first"], 0,
          "A text file holds characters, so a value read from it is a string even when every character is a digit."),
        Q("What does ord('A') return, given that 'A' has the code 65?", ["65", "'A'", "1", "97"], 0,
          "ord returns the character set code for a character, and chr converts a code back into a character."),
    ],
    exam=[
        EQ("A list called marks holds 30 integers. Write a Python program that outputs the highest mark.", 4, [
            MP("Sets an initial highest value from the list, such as marks[0]", ["marks[0]", "first element", "highest =", "initialise"]),
            MP("Loops through the list", ["for", "in marks", "range", "loop"]),
            MP("Compares each item with the current highest", ["if", ">", "greater"]),
            MP("Updates the highest and outputs it after the loop", ["highest =", "print", "after the loop"]),
        ], "A correct program is: highest = marks[0], then for mark in marks: if mark > highest: highest = mark, then print(\"The highest mark is\", highest). Starting from marks[0] rather than from zero matters, because a list containing only negative values would otherwise report zero as the highest. The print statement must be outside the loop, otherwise it outputs a running maximum on every pass rather than the final answer. Python's built in max(marks) would also be accepted.", command="Write"),
        EQ("Explain why a program that reads a name from a file and compares it with a name typed by the user might never find a match, even when the names look identical.", 3, [
            MP("A line read from a file includes the newline character at the end", ["newline", "\\n", "line break", "invisible character", "end of line"]),
            MP("The typed name does not include that character, so the two strings differ", ["not equal", "different", "does not match", "differ", "extra character"]),
            MP("Using strip() removes it so the comparison works", ["strip", "removes", "rstrip", "trim"]),
        ], "When a line is read from a text file it includes the newline character that ended the line in the file. The name typed by the user does not include that character, so although the two look identical when printed, one is a character longer than the other and the comparison is False. The fix is to remove the whitespace at the ends of the line read from the file, using name = line.strip(), after which the two strings genuinely are equal and the comparison succeeds. The same problem causes numbers read from files to fail if they are compared before being cast.", command="Explain"),
        EQ("A text file called results.txt has one record per line in the form name,score. Write a Python program that reads the file and outputs the name of every student who scored more than 50.", 5, [
            MP("Opens the file for reading", ["open", "with open", "\"r\""]),
            MP("Loops through each line of the file", ["for line in", "readlines", "loop"]),
            MP("Splits each line on the comma", ["split", "split(\",\")", "parts"]),
            MP("Casts the score to an integer", ["int(", "cast", "convert"]),
            MP("Compares with 50 and outputs the name for those above it", ["> 50", "if", "print", "output"]),
        ], "A correct program is: with open(\"results.txt\", \"r\") as file: then for line in file: then parts = line.strip().split(\",\") then name = parts[0] then score = int(parts[1]) then if score > 50: print(name). Three details carry the marks. The line must be stripped before splitting, or the score picks up a trailing newline. The score must be cast with int(), because everything read from a text file is a string and comparing a string with 50 would fail. Using with open means the file is closed automatically even if an error occurs part way through.", command="Write"),
        EQ("Explain the difference between opening a file in write mode and in append mode, and give one situation where each is appropriate.", 4, [
            MP("Write mode empties the existing file before writing", ["deletes", "empties", "overwrites", "clears", "truncates"]),
            MP("Append mode adds new data to the end, keeping what is there", ["adds to the end", "keeps", "existing data", "after"]),
            MP("Gives a suitable use of write mode, such as creating a fresh report", ["fresh", "new file", "report", "start again", "replace"]),
            MP("Gives a suitable use of append mode, such as adding to a log of results", ["log", "adding a record", "each run", "history", "keeps adding"]),
        ], "Opening a file in write mode, using \"w\", deletes everything already in the file before a single character is written, so the file always ends up containing only what this run of the program put there. Append mode, using \"a\", leaves the existing contents alone and adds the new data to the end. Write mode is appropriate when the file is being regenerated in full each time, for example a report that should reflect only the current data. Append mode is appropriate when each run adds to a growing record, for example a log file that records the result of every game played, where opening in write mode would destroy the entire history every time the program ran.", command="Explain"),
    ],
)


# ============================================ 6.1 developing code

T_PYDEV = Topic(
    slug="developing-and-testing-programs",
    title="Developing and Testing Programs",
    spec="6.1",
    icon="i-check-circle",
    minutes=28,
    blurb="Subprograms, readable and maintainable code, validation and authentication, the three kinds of error, and how to build a test plan that finds faults before an examiner does.",
    fact="The cost of fixing a fault rises sharply the later it is found. A mistake caught while writing a function costs minutes. The same mistake caught after release can cost thousands of times more, which is the whole reason testing exists.",
    sections=[
        Section("Subprograms", """
A **subprogram** is a named block of code that can be called from elsewhere. Python has one keyword for both kinds.

A **procedure** carries out a task and returns nothing:

```python
def greet(name):
    print("Hello", name)

greet("Amira")
```

A **function** returns a value:

```python
def area(width, height):
    return width * height

size = area(4, 7)
```

**Parameters** are the names in the definition, `width` and `height`. **Arguments** are the values passed in, `4` and `7`. Parameters are what make a subprogram reusable: one that always calculates the area of a four by seven rectangle is useless.

### Scope

A variable created inside a subprogram is **local**: it exists only while that subprogram runs, and it cannot be seen from outside.

```python
def tally():
    count = 0
    count = count + 1
    return count
```

This returns 1 every time it is called, because `count` is created fresh on each call. Local variables are the right default: two subprograms can each use a variable called `i` without interfering, and each subprogram can be tested on its own.

### Why decomposition into subprograms matters

- Code written once is called wherever it is needed, so there is no repetition.
- A change is made in one place rather than in every copy.
- Each subprogram can be tested on its own before it is trusted.
- The main program reads as a list of named steps, which is far easier to follow.
"""),
        Section("Readable and maintainable code", """
Edexcel awards marks for code quality, not only for code that works.

**Meaningful identifiers.** `total_price` rather than `tp` or `x2`. The next reader, including you in a month, should not have to trace the program to work out what a variable holds.

**Comments that explain why.** `count = count + 1` does not need a comment saying it adds one. It may need one saying why the first record is skipped.

**Consistent indentation and blank lines** separating logical sections, so the structure of the program is visible on the page.

**Constants for fixed values.** `VAT_RATE = 0.2` at the top, used by name, changed in one place.

**Subprograms** so each task has one home and one name.

!exam Write the comments as you go :: Adding them at the end, under time pressure, produces the comments that restate the code and earn nothing. Written as you go they explain the decision you were actually making.
"""),
        Section("Validation, authentication and testing", """
### Validation

**Validation** checks that entered data is **reasonable**. It cannot check it is **true**.

| Check | Tests | Example |
| Range | Value lies between limits | `if 0 <= mark <= 100:` |
| Presence | Something was entered | `if name != "":` |
| Length | Correct number of characters | `if len(password) >= 8:` |
| Type | Data is of the expected type | `if entry.isdigit():` |
| Format | Matches a required pattern | `if "@" in email:` |
| Look up | Value is one of a known set | `if county in COUNTIES:` |

A validation loop is the standard pattern and is worth memorising:

```python
mark = -1
while mark < 0 or mark > 100:
    entry = input("Enter a mark between 0 and 100: ")
    if entry.isdigit():
        mark = int(entry)
    else:
        print("Please enter a whole number.")
```

### Authentication

**Authentication** checks the user is who they claim to be, usually with a username and password, strengthened by minimum length, mixed character types and a limit on failed attempts.

Validation asks "is that a sensible thing to type". Authentication asks "who are you". They are different jobs.

### The three kinds of error

**Syntax error.** Breaks the rules of Python, such as a missing colon or bracket. The program will not run and the error is reported with a line number.

**Logic error.** The program runs and gives the wrong answer. Using `+` where `-` was meant, or `<` where `<=` was meant. Nothing reports it, which is why these are the expensive ones.

**Runtime error.** The program starts and then stops: dividing by zero, an index out of range, opening a file that does not exist.

### Test data

| Type | Meaning | For a mark from 0 to 100 |
| Normal | Typical accepted data | 55 |
| Boundary | At the edge of what is allowed, on both sides | 0, 100, and -1, 101 |
| Erroneous | Should be rejected | "cat", blank, 3.5 |

!key Boundary data is where the bugs are :: Almost every off by one error appears at a boundary and nowhere else. A program tested only with 55 will happily reject 0 and accept 101.
"""),
    ],
    keyterms=[
        ("Subprogram", "A named block of code that can be called from elsewhere in a program."),
        ("Procedure", "A subprogram that carries out a task without returning a value."),
        ("Function", "A subprogram that returns a value to the code that called it."),
        ("Parameter", "A name in a subprogram definition that receives a value when it is called."),
        ("Argument", "The actual value passed to a subprogram when it is called."),
        ("Local variable", "A variable created inside a subprogram, existing only while it runs."),
        ("Validation", "An automatic check that entered data is reasonable and of the expected form."),
        ("Authentication", "Checking that a user is who they claim to be."),
        ("Syntax error", "An error breaking the rules of the language, preventing the program from running."),
        ("Logic error", "An error in which the program runs but produces the wrong result."),
        ("Runtime error", "An error occurring while the program is running, causing it to stop."),
        ("Boundary test data", "Data at the very edge of the acceptable range, on both sides of each limit."),
    ],
    grade="""
Paper 2 gives marks for a program that works and for a program that is readable, and the second is far easier to secure than most candidates realise.

**Decompose before you type.** Three named subprograms and a short main section will always score better than one long block, and it is quicker to debug.

**Validate every input the task mentions.** Use the while loop pattern, and say in a comment which check you are applying.

**Choose test data with a reason.** "0 and 100 because they are the boundaries, and -1 and 101 because an incorrect comparison operator would only show up there" is the answer a mark scheme wants.

**Be exact about the three errors.** Will not run at all is syntax. Runs and gives the wrong answer is logic. Starts and then stops is runtime.
""",
    mistakes=[
        "Saying validation checks that data is correct. It checks that data is reasonable.",
        "Giving only one boundary value. A boundary needs testing on both sides.",
        "Calling a crash a logic error. A program that stops while running has a runtime error.",
        "Writing comments that restate the code rather than explaining the decision.",
        "Initialising a counter inside the subprogram that is supposed to increase it, so it resets on every call.",
    ],
    quiz=[
        Q("What is the difference between a procedure and a function?", ["A function returns a value and a procedure does not", "A function is always longer", "A procedure cannot take parameters", "A procedure runs faster"], 0,
          "The return value is the defining difference. A function hands a result back to the caller; a procedure carries out a task and hands nothing back."),
        Q("In def area(width, height), what are width and height?", ["Parameters", "Arguments", "Global variables", "Return values"], 0,
          "Names in the definition are parameters. The values supplied at the call are the arguments."),
        Q("A program will not run and Python reports a missing colon. What kind of error is this?", ["Syntax error", "Logic error", "Runtime error", "Validation error"], 0,
          "A missing colon breaks the rules of the language, so the program cannot be interpreted at all."),
        Q("A program runs but calculates an average by dividing by the wrong number. What kind of error is this?", ["Logic error", "Syntax error", "Runtime error", "Type error"], 0,
          "The program runs perfectly and produces an answer, but the answer is wrong, and nothing reports it for you."),
        Q("For a value that must be between 1 and 20, which set is boundary test data?", ["0, 1, 20, 21", "10, 11, 12", "cat, blank, 2.5", "1, 2, 3"], 0,
          "Boundary data sits at each limit and just outside it, which is where an incorrect comparison operator shows up."),
        Q("What can validation never do?", ["Confirm that the data entered is truthful", "Check a value is within a range", "Check a field is not empty", "Check the data type"], 0,
          "Validation checks plausibility. A false but correctly formatted date of birth passes every check that can be written."),
        Q("Why does a subprogram that initialises its counter internally return the same value every call?", ["The counter is local and is created fresh on each call", "The return statement is misplaced", "Python does not support counters", "The parameter is missing"], 0,
          "A local variable exists only while the subprogram runs, so the value reached on one call is gone by the next."),
        Q("Which is the best example of a useful comment?", ["# skip the first line because it holds the column headings", "# add one to count", "# this is a loop", "# variable"], 0,
          "A useful comment explains a decision the code cannot show. The other three restate what is already obvious."),
        Q("A program stops with an error when it tries to open a file that has been deleted. What kind of error is this?", ["Runtime error", "Syntax error", "Logic error", "Design error"], 0,
          "The program started successfully and then failed while executing, which is what makes it a runtime error."),
        Q("What is erroneous test data used to check?", ["That the program correctly rejects data it should not accept", "That typical values are handled", "That the program is fast enough", "That the boundaries are right"], 0,
          "Erroneous data is deliberately invalid, so testing with it proves the validation actually rejects what it should."),
    ],
    exam=[
        EQ("State one advantage of using subprograms in a long program.", 2, [
            MP("Code written once can be called from many places, reducing repetition", ["reuse", "called", "many places", "no repetition", "written once"]),
            MP("Or each subprogram can be tested and maintained on its own", ["tested", "maintained", "one place", "easier to fix", "independently"]),
        ], "A task written once as a subprogram can be called from every point that needs it, which removes repeated code, and because that task lives in one named place a correction only has to be made once rather than in every copy.", command="State"),
        EQ("Write a Python validation loop that repeatedly asks the user for a whole number between 1 and 10 until a valid value is entered.", 4, [
            MP("Uses a while loop that repeats until the value is acceptable", ["while", "loop", "until", "repeat"]),
            MP("Checks that the entry is a whole number", ["isdigit", "int(", "try", "type", "whole number"]),
            MP("Checks that the value is within the range 1 to 10", ["1", "10", "range", ">= 1", "<= 10", "between"]),
            MP("Gives the user a message when the entry is rejected", ["print", "message", "try again", "invalid", "error"]),
        ], "A correct answer is: number = 0, then while number < 1 or number > 10:, then entry = input(\"Enter a number from 1 to 10: \"), then if entry.isdigit(): number = int(entry), then if number < 1 or number > 10: print(\"That is outside the range.\"), else: print(\"Please enter a whole number.\"). The loop condition must be false only for acceptable values, the entry must be checked for being numeric before int() is applied so that typing a word does not crash the program, and a message tells the user what was wrong rather than simply asking again.", command="Write"),
        EQ("Explain the difference between validation and authentication.", 3, [
            MP("Validation checks that data entered is reasonable or of the expected form", ["reasonable", "sensible", "expected form", "plausible", "correct format"]),
            MP("Authentication checks that a user is who they claim to be", ["who they say", "identity", "claim to be", "verify the user"]),
            MP("Gives an example of each, such as a range check and a password", ["range check", "presence", "password", "username", "biometric"]),
        ], "Validation is a check on the data itself, confirming that what has been entered is reasonable and of the form expected, for example that a mark lies between 0 and 100 or that a required field is not blank. It says nothing at all about who typed it. Authentication is a check on the person, confirming that the user is who they claim to be, usually through a username and password or a biometric check. The two are separate jobs: a system with perfect validation still has no idea who is using it, and a system with strong authentication will still accept a nonsensical value if it does not validate.", command="Explain"),
        EQ("Describe the three types of error a programmer may encounter, giving an example of each.", 6, [
            MP("A syntax error breaks the rules of the language", ["rules", "grammar", "language"]),
            MP("Gives an example such as a missing colon or bracket, and notes the program will not run", ["colon", "bracket", "misspelled", "will not run", "does not run"]),
            MP("A logic error means the program runs but gives the wrong result", ["runs", "wrong result", "incorrect answer"]),
            MP("Gives an example such as using the wrong operator, and notes nothing reports it", ["wrong operator", "plus instead of minus", "not reported", "no message", "wrong comparison"]),
            MP("A runtime error occurs while the program is executing and stops it", ["while running", "stops", "crashes", "during execution"]),
            MP("Gives an example such as dividing by zero or an index out of range", ["divide by zero", "index", "out of range", "file not found"]),
        ], "A syntax error breaks the rules of the programming language, for example a missing colon at the end of an if statement or an unclosed bracket. Python cannot interpret the line, so the program does not run at all and the error is reported with a line number, which makes it the easiest kind to fix. A logic error is different in kind: the code is valid, so the program runs from start to finish, but the instructions do not do what the programmer intended, so the output is wrong. Using a plus where a minus was meant, or less than where less than or equal to was meant, produces a logic error, and nothing reports it, which means it can only be found by testing with data whose correct answer is already known or by tracing the program by hand. A runtime error occurs while the program is executing and causes it to stop, for example dividing by zero, reading past the end of a list, or trying to open a file that does not exist. The program was valid and started normally, so a runtime error usually reflects data the programmer did not anticipate rather than a mistake in the code's structure, which is why validation and error handling reduce them.", command="Describe"),
    ],
)


# ================================================================== COURSE

COURSE = Course(
    slug="ks4/edexcel-computer-science",
    title="Edexcel GCSE Computer Science",
    short="Edexcel GCSE CS",
    stage="KS4",
    board="Pearson Edexcel",
    code="1CP2",
    goal="Grade 9",
    icon="i-cpu",
    accent="var(--lilac-deep)",
    blurb="All six topics of the Pearson Edexcel 1CP2 specification, written to Edexcel's own conventions: Edexcel pseudocode, binary storage prefixes, and Paper 2 taught in the Python you will actually sit it in.",
    intro="",
    journey=[
        ("Know what the two papers ask of you",
         "Paper 1, Principles of Computer Science, is 1 hour 30 minutes of written questions on Topics 1 to 5. Paper 2, Application of Computational Thinking, is 2 hours sat at a computer writing and fixing Python. They need different preparation and most students only prepare for the first.", ""),
        ("Use Edexcel's own conventions",
         "Edexcel pseudocode uses SET, SEND TO DISPLAY and RECEIVE FROM KEYBOARD, and Edexcel counts storage in kibibytes of 1024 bytes. Working from another board's material will cost you marks on questions you actually knew.", ""),
        ("Read a topic once, then close it and write",
         "What you can produce from memory is what you have learned. What you can only recognise on the page is not, and rereading will never show you which is which.", ""),
        ("Score full marks on every knowledge check",
         "Ten questions per topic with an explanation for every answer. Below ten out of ten means go back to that section rather than moving on.", ""),
        ("Type the Python, do not read it",
         "Paper 2 is marked on a program that runs. Every Python example on this site can be run and edited in the browser, and every hour spent typing is worth several spent reading.", ""),
        ("Sit whole papers to time, then fix what you dropped",
         "Mark honestly against the mark scheme, write down every mark you lost and the reason, and revise from that list. Your mistakes are your revision plan.", ""),
    ],
    units=[
        Unit("computational-thinking", "Topic 1: Computational Thinking",
             "Decomposition and abstraction, algorithms in flowcharts and pseudocode, searching and sorting, and truth tables.",
             [T_DECOMP, T_ALGOS, T_SEARCHSORT, T_TRUTH], icon="i-brain", term="Paper 1"),
        Unit("data", "Topic 2: Data",
             "Binary and hexadecimal, representing text, images and sound, and storage units and compression using Edexcel's binary prefixes.",
             [T_BINHEX, T_DATAREP, T_STORAGE], icon="i-binary", term="Paper 1"),
        Unit("computers", "Topic 3: Computers",
             "The components of a computer system, the processor and the fetch decode execute cycle, software, and programming languages and translators.",
             [T_HARDWARE, T_SOFTWARE], icon="i-cpu", term="Paper 1"),
        Unit("networks", "Topic 4: Networks",
             "Local and wide area networks, topologies, protocols and layers, and every network threat and defence in the specification.",
             [T_NET], icon="i-network", term="Paper 1"),
        Unit("issues-and-impact", "Topic 5: Issues and Impact",
             "Environmental, ethical, cultural and privacy impacts, emerging technologies, and the legislation you must be able to apply.",
             [T_IMPACT, T_LAW], icon="i-shield", term="Paper 1"),
        Unit("problem-solving-with-programming", "Topic 6: Problem Solving with Programming",
             "The on screen paper. Python from variables and constructs through lists, strings and files to subprograms, validation and testing.",
             [T_PYFUND, T_PYDATA, T_PYDEV], icon="i-python", term="Paper 2"),
    ],
)
