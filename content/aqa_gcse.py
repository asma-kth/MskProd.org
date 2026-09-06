"""AQA GCSE Computer Science 8525 revision content.

Written to the AQA 8525 subject content headings 3.1 to 3.8. Pseudo-code
follows AQA's own reference language, not OCR's, and units of information use
AQA's decimal convention in which 1 kB is 1000 bytes.
"""
from mskbuild.models import Topic, Section, Unit, Course, Q, EQ, MP

# ================================================ 3.1.1 computational thinking

T_COMPTHINK = Topic(
    slug="computational-thinking",
    title="Computational Thinking",
    spec="3.1.1",
    icon="i-brain",
    minutes=22,
    blurb="What AQA means by an algorithm, why a program is not the same thing, and how decomposition and abstraction turn a problem you cannot see the end of into one you can actually code.",
    fact="The word algorithm comes from al-Khwarizmi, a ninth century scholar working in Baghdad. When his book on Indian numerals was translated into Latin the translator wrote his name as 'Algoritmi', and the word stuck to the methods rather than the man.",
    sections=[
        Section("Algorithms and programs", """
AQA defines an **algorithm** as a sequence of steps that can be followed to complete a task. Learn that wording. Mark schemes accept "sequence of steps" and are far less generous with vaguer phrases such as "instructions for a computer".

Two consequences follow from that definition, and both get examined.

**An algorithm does not have to involve a computer.** A recipe is an algorithm. The instructions for changing a tyre are an algorithm. What makes something an algorithm is that the steps are unambiguous, they are in a definite order, and following them eventually finishes.

**A computer program is an implementation of an algorithm.** The algorithm is the method. The program is that method written down in a language a machine can run. The same algorithm can be implemented in Python, in C#, in VB.NET, or drawn as a flowchart, and it is still the same algorithm.

!key The distinction examiners look for :: An algorithm is the method. A program is one implementation of that method in a particular programming language. Getting this the wrong way round costs a mark in one of the easiest questions on the paper.

### Why this matters when you are actually coding

If you design the algorithm first you can check it works before writing a line of code. Tracing a plan on paper takes two minutes. Debugging an unplanned program takes an afternoon, because you end up guessing at what the code was supposed to do at the same time as working out what it actually does.

This is also why AQA can set a question that says "write an algorithm" and accept pseudo-code, program code or a flowchart. It is testing whether you can produce the method, not whether you can remember Python punctuation.
"""),
        Section("Decomposition", """
**Decomposition** means breaking a problem down into smaller, more manageable sub problems, each of which is easier to solve than the whole.

Take "write a quiz game". As a single instruction that is unusable. Nobody can sit down and write a quiz game, because "quiz game" is not a task, it is a category. Decomposed, it becomes a list of things you could each do in twenty minutes:

1. Load the questions from a file
2. Pick a question that has not been asked yet
3. Display the question and the four options
4. Read the player's answer
5. Check the answer against the correct one
6. Update the score
7. Repeat until the questions run out
8. Display the final score and save the high score

### Why decomposition earns marks

You must be able to say what it gives you, not just what it is. There are four standard benefits and any of them can be credited:

- **Each sub problem is simpler**, so it can be solved and tested on its own.
- **Work can be split between programmers**, because different people can take different sub problems at the same time.
- **Errors are easier to find**, because a fault shows up inside one small routine rather than somewhere in a thousand lines.
- **Sub problems can be reused**, since a routine that loads a file of questions will load a file of anything.

!warn Do not stop at 'breaking it into smaller parts' :: That sentence alone is one mark. The second mark comes from saying what the smaller parts let you do: solve, test, reuse or share them out.

Decomposition maps directly onto subroutines in code. Each sub problem in the list above becomes a procedure or a function, which is exactly why structured programming and decomposition are examined as the same idea in different clothes.
"""),
        Section("Abstraction", """
**Abstraction** means removing unnecessary detail from a problem so that only the parts needed to solve it remain.

The classic example is the London Underground map. It is geographically wrong: the distances are invented, the lines are straightened, and the river is a rough blue ribbon. All of that is deliberate. A passenger only needs to know which stations are on which line and where the lines cross. Everything else is detail that would make the map harder to use, so it is thrown away.

### Abstraction in a program

Suppose you are writing a program that works out bus fares. The real world facts about a passenger include their name, hair colour, shoe size, favourite band, home address and age. For the fare calculation you need the age, the zones travelled and whether they hold a pass. Everything else is discarded. That decision is abstraction.

!key One sentence definition :: Abstraction is the process of removing or hiding unnecessary detail so that only the information required to solve the problem remains.

### Why it is worth doing

- The program is **simpler to write**, because there is less to represent.
- It **runs faster and uses less memory**, because less data is stored and processed.
- It is **easier to understand and maintain**, because the code only mentions things that matter.
- It makes the solution **more general**, so the same fare model works for a different city.

!warn Abstraction is not the same as decomposition :: Decomposition splits a problem into parts. Abstraction throws detail away. A question that asks for both wants two clearly different answers, and the marker will not give the same point twice.

!exam Naming what was removed :: If a question shows a scenario and asks you to give an example of abstraction, name a specific detail that has been left out and say why it does not matter. "The map does not show the real distance between stations because a passenger only needs to know the order of the stops" is a full answer. "It removes detail" is not.
"""),
    ],
    keyterms=[
        ("Algorithm", "A sequence of steps that can be followed to complete a task."),
        ("Program", "An implementation of an algorithm written in a programming language so that a computer can run it."),
        ("Decomposition", "Breaking a problem down into smaller sub problems, each of which is easier to solve."),
        ("Abstraction", "Removing unnecessary detail from a problem so that only the information needed to solve it remains."),
        ("Sub problem", "One of the smaller, self contained tasks produced by decomposing a larger problem."),
        ("Computational thinking", "The approach of solving problems using decomposition, abstraction and algorithmic thinking."),
        ("Algorithmic thinking", "Working out the sequence of steps needed to solve a problem so that the method can be repeated reliably."),
        ("Unambiguous", "Having only one possible meaning, which is why every step of an algorithm must be written precisely."),
    ],
    grade="""
This topic looks easy and is marked strictly, which is why it separates candidates.

**Use AQA's definitions word for word.** "A sequence of steps that can be followed to complete a task" is worth learning by heart. Paraphrasing it into "a set of rules a computer follows" loses the mark because it smuggles in the computer, which is not part of the definition.

**Always give the benefit as well as the definition.** Almost every question on this topic is worth two or three marks, and the extra marks are for consequences: easier to test, quicker to find errors, work can be shared, code can be reused, less memory used.

**Tie the answer to the scenario in the question.** If the scenario is a hospital appointment system, your abstraction example must be about appointments, not about tube maps. Generic examples that ignore the stem are the single most common reason a three mark answer scores one.

+ State AQA's definition of an algorithm from memory in one sentence
+ Explain the difference between an algorithm and a program without hesitating
+ Give three distinct benefits of decomposition
+ Give a scenario specific example of abstraction that names the detail removed and says why it can be removed
""",
    mistakes=[
        "Defining an algorithm as 'instructions for a computer'. The definition is a sequence of steps to complete a task, and it need not involve a computer at all.",
        "Saying a program and an algorithm are the same thing. The program is one implementation of the algorithm.",
        "Confusing abstraction with decomposition. Abstraction removes detail, decomposition splits the problem up.",
        "Giving the tube map as an abstraction example when the question is about a completely different scenario, so none of the detail relates to the stem.",
        "Stating a definition and stopping, when the question is worth three marks and the other two are for benefits.",
    ],
    quiz=[
        Q("Which is AQA's definition of an algorithm?",
          ["A sequence of steps that can be followed to complete a task",
           "A set of instructions written in a programming language",
           "A diagram showing the flow of data through a system",
           "A method of storing data efficiently in memory"], 0,
          "AQA's wording is 'a sequence of steps that can be followed to complete a task'. Nothing in the definition mentions a computer, because a recipe is an algorithm too."),
        Q("What is the relationship between an algorithm and a program?",
          ["A program is an implementation of an algorithm",
           "An algorithm is an implementation of a program",
           "They are two words for the same thing",
           "A program is always shorter than its algorithm"], 0,
          "The algorithm is the method. Writing it in Python, C# or VB.NET produces a program, which is one implementation of that method."),
        Q("A developer splits a shopping app into a login routine, a basket routine and a payment routine. This is an example of:",
          ["Decomposition", "Abstraction", "Iteration", "Validation"], 0,
          "Breaking one large problem into smaller sub problems that can be solved separately is decomposition."),
        Q("Which of these is a benefit of decomposition?",
          ["Different programmers can work on different sub problems at the same time",
           "The program will always run faster",
           "It removes the need to test the program",
           "It guarantees the program contains no logic errors"], 0,
          "Because each sub problem is independent, the work can be shared out and each part can be tested on its own."),
        Q("A weather app stores only a town's name and its coordinates, ignoring its population and history. This is an example of:",
          ["Abstraction", "Decomposition", "Compression", "Encryption"], 0,
          "Detail that is not needed to solve the problem has been removed, which is exactly what abstraction means."),
        Q("Why is the London Underground map a good example of abstraction?",
          ["Real distances and geography are removed because passengers only need the order of stations",
           "It is drawn using only two colours to save ink",
           "It splits the network into separate lines that can be printed separately",
           "It compresses the data so the file is smaller"], 0,
          "The map deliberately discards geographic accuracy, keeping only the connections and the ordering, which are the only things a passenger needs."),
        Q("Which statement about abstraction is correct?",
          ["It makes a solution simpler because less data has to be stored and processed",
           "It always increases the amount of memory a program needs",
           "It means writing the algorithm in a low level language",
           "It means splitting a problem into sub problems"], 0,
          "Removing unnecessary detail means fewer things to represent, so the program is simpler and uses less memory."),
        Q("Which of these is NOT a property that every algorithm must have?",
          ["It must be written in a programming language",
           "Its steps must be unambiguous",
           "Its steps must be in a definite order",
           "It must eventually finish"], 0,
          "An algorithm can be written in pseudo-code, in English or as a flowchart. Being written in a programming language is what turns it into a program."),
        Q("A student writes: 'Decomposition means removing detail you do not need.' What is wrong with this?",
          ["That is the definition of abstraction, not decomposition",
           "Nothing, it is correct",
           "Decomposition only applies to hardware",
           "Decomposition means translating code into machine code"], 0,
          "Decomposition breaks the problem into smaller sub problems. Removing unneeded detail is abstraction."),
        Q("Why does designing an algorithm before coding reduce development time overall?",
          ["Errors in the method are found on paper, before they are built into code that has to be debugged",
           "It removes the need for a translator",
           "It makes the finished program run at a higher clock speed",
           "It means the program does not need testing"], 0,
          "A fault in the plan costs two minutes to fix while it is still a plan, and can cost hours once it is buried inside working code."),
    ],
    exam=[
        EQ("State what is meant by the term algorithm.", 1, [
            MP("A sequence of steps that can be followed to complete a task",
               ["sequence of steps", "series of steps", "set of steps", "steps to complete a task", "ordered steps"]),
        ], "An algorithm is a sequence of steps that can be followed to complete a task.",
           command="State"),
        EQ("Explain the difference between an algorithm and a computer program.", 2, [
            MP("An algorithm is the method or sequence of steps for solving the problem",
               ["method", "sequence of steps", "plan", "set of steps", "solution design"]),
            MP("A program is an implementation of that algorithm in a programming language",
               ["implementation", "written in a programming language", "code", "programming language", "implemented"]),
        ], "An algorithm is the method itself: the sequence of steps that solves the problem, which can be written as pseudo-code, as a flowchart or in plain English. A computer program is an implementation of that algorithm in a particular programming language, so that a computer can actually execute it. The same algorithm can therefore be implemented as many different programs.",
           command="Explain"),
        EQ("A team is writing software for an online supermarket. Describe how decomposition would help them develop the software.", 4, [
            MP("The problem is broken down into smaller sub problems",
               ["broken down", "smaller sub problems", "split into parts", "divided into", "smaller tasks"]),
            MP("Each sub problem is simpler and can be solved on its own",
               ["simpler", "easier to solve", "solved individually", "manageable", "own right"]),
            MP("Different programmers can work on different sub problems at the same time",
               ["different programmers", "work at the same time", "share the work", "team members", "in parallel"]),
            MP("Each part can be tested separately so errors are easier to locate",
               ["tested separately", "easier to find errors", "locate errors", "test each part", "debug"]),
        ], "Decomposition means breaking the supermarket system down into smaller sub problems such as searching the product catalogue, managing the basket, taking payment and booking a delivery slot. Each of those sub problems is far simpler than the whole system, so a programmer can understand it, solve it and finish it without holding the entire project in their head. Because the sub problems are independent, different members of the team can work on different parts at the same time, which shortens development. Each part can also be tested on its own, so when something fails the fault is known to lie inside one small routine rather than anywhere in the finished system.",
           command="Describe"),
        EQ("Explain what is meant by abstraction, using an example.", 3, [
            MP("Abstraction is removing or hiding unnecessary detail",
               ["removing detail", "hiding detail", "unnecessary detail", "ignoring detail", "leaving out detail"]),
            MP("Only the information needed to solve the problem is kept",
               ["only the information needed", "relevant detail", "what is required", "key details", "essential information"]),
            MP("A valid example is given, such as a tube map keeping station order but discarding real distances",
               ["tube map", "underground map", "sat nav", "example", "distances removed", "not to scale"]),
        ], "Abstraction is the process of removing unnecessary detail from a problem so that only the information needed to solve it remains. For example, the London Underground map is not drawn to scale and shows none of the real geography above ground, because a passenger only needs to know which stations lie on which line and where the lines cross. Removing the rest makes the map far quicker to read, and in the same way removing irrelevant data from a program makes it simpler to write and less demanding on memory.",
           command="Explain"),
        EQ("A student says: 'Abstraction and decomposition mean the same thing.' Explain why the student is wrong.", 3, [
            MP("Decomposition breaks a problem into smaller sub problems",
               ["decomposition breaks", "smaller sub problems", "splits the problem", "divides", "smaller parts"]),
            MP("Abstraction removes detail that is not needed",
               ["removes detail", "unnecessary detail", "hides detail", "ignores irrelevant"]),
            MP("They are different processes that can both be applied to the same problem",
               ["different processes", "both used", "not the same", "used together", "separate techniques"]),
        ], "The student is wrong because the two techniques do different jobs. Decomposition takes one large problem and breaks it into smaller sub problems, each of which can be solved, tested and reused on its own, so the size of the problem changes but the detail does not. Abstraction leaves the problem whole but strips out the detail that is not needed to solve it, so that only relevant information is represented. Both techniques are usually applied to the same project, and a good solution will decompose the system into subroutines while abstracting away the data that has no bearing on the result.",
           command="Explain"),
    ],
)

# ================================================ 3.1.1 representing algorithms

T_REPRESENT = Topic(
    slug="representing-algorithms",
    title="Representing Algorithms",
    spec="3.1.1",
    icon="i-flow",
    minutes=36,
    blurb="AQA pseudo-code written the way AQA writes it, the six flowchart symbols and what each one is for, and a method for trace tables that does not fall apart under time pressure.",
    fact="AQA publishes its own pseudo-code guide and uses it in every exam paper, so the pseudo-code you read in a question is guaranteed to follow it. You are not required to answer in AQA pseudo-code, but you are required to be able to read it.",
    sections=[
        Section("AQA pseudo-code", """
Pseudo-code is a way of writing an algorithm that has the structure of a program without the fussy punctuation of a real language. AQA publishes its own version and every algorithm printed in an exam paper uses it, so being able to read it fluently is worth marks on every paper.

The single most important thing to notice is the **assignment arrow**. AQA never uses `=` for assignment. It uses a left arrow, so `=` only ever means "is equal to".

```aqa pseudo-code
score ← 0
score ← score + 10
name ← USERINPUT
OUTPUT 'Hello ' + name
```

### Selection

```aqa pseudo-code
IF mark > 79 THEN
    grade ← 9
ELSE IF mark > 69 THEN
    grade ← 8
ELSE
    grade ← 7
ENDIF
```

Note `ELSE IF` as two words, and `ENDIF` as one. Every AQA block structure closes with an `END` keyword: `ENDIF`, `ENDWHILE`, `ENDFOR`, `ENDSUBROUTINE`. The one exception is `REPEAT`, which is closed by `UNTIL`.

### Iteration

```aqa pseudo-code
# definite iteration: you know how many times before you start
FOR i ← 1 TO 10
    OUTPUT i
ENDFOR

# indefinite iteration: condition tested before the body runs
WHILE guess ≠ answer
    guess ← USERINPUT
ENDWHILE

# indefinite iteration: condition tested after the body runs
REPEAT
    guess ← USERINPUT
UNTIL guess = answer
```

The difference between the last two is examined constantly. A `WHILE` loop may run zero times, because the condition is checked first. A `REPEAT` loop always runs at least once, because the condition is checked at the end.

### Arrays, subroutines and strings

```aqa pseudo-code
scores ← [4, 8, 15, 16, 23, 42]
OUTPUT scores[0]
OUTPUT LEN(scores)

SUBROUTINE average(values)
    total ← 0
    FOR i ← 0 TO LEN(values) - 1
        total ← total + values[i]
    ENDFOR
    RETURN total / LEN(values)
ENDSUBROUTINE

mean ← average(scores)
```

AQA arrays and strings are **indexed from 0**. Three string routines appear repeatedly:

| Routine | What it does | Example | Result |
| `LEN(s)` | Number of characters, including spaces | `LEN('computer')` | 8 |
| `POSITION(s, c)` | Index of the first occurrence of a character | `POSITION('computer', 'm')` | 2 |
| `SUBSTRING(a, b, s)` | Characters from index a to index b **inclusive** | `SUBSTRING(2, 4, 'computer')` | 'mpu' |

!warn SUBSTRING takes a finish position, not a length :: This is the trap AQA sets most often. `SUBSTRING(2, 4, 'computer')` returns three characters, indexes 2, 3 and 4, because both ends are included. If you read the second number as a length you get the wrong answer every time.

!key Arithmetic you must recognise :: `DIV` is integer division, so `17 DIV 5` is 3. `MOD` gives the remainder, so `17 MOD 5` is 2. Ordinary `/` gives the real answer 3.4.
"""),
        Section("Flowcharts", """
A flowchart shows the same algorithm as a diagram. AQA can ask you to complete one, to read one, or to convert between a flowchart and pseudo-code, so you need the symbols exactly.

| Symbol | Shape | Used for |
| Terminal | Rounded rectangle | Start and Stop, one of each |
| Process | Rectangle | A calculation or an assignment, such as `total ← total + 1` |
| Input or output | Parallelogram | Reading a value from the user or displaying one |
| Decision | Diamond | A question with exactly two labelled exits, Yes and No |
| Subroutine | Rectangle with two extra vertical lines | A call to a named subroutine defined elsewhere |
| Flow line | Arrow | The order the steps are carried out in |

### Reading one properly

Loops in a flowchart are drawn as an arrow going backwards from somewhere below a decision to somewhere above it. That is the only way a loop can appear, so if you see a backward arrow you are looking at iteration, and the decision it returns to is the loop condition.

The decision diamond is where marks are lost. Every diamond must contain a question that can only be answered Yes or No, and both exits must be labelled. A diamond containing `total` is wrong. A diamond containing `total > 100` is right.

!exam Converting a flowchart into pseudo-code :: Work out first whether the decision is a loop or an `IF`. If an arrow comes back to it from below, it is a loop, so write `WHILE` or `REPEAT`. If both exits carry on downwards and meet again lower down, it is an `IF`.

!warn One Start and one Stop :: A flowchart with two Stop terminals is usually a sign that you have drawn an `IF` where the two branches never rejoin. It is not automatically wrong, but check the logic before you leave it.
"""),
        Section("Trace tables", """
A trace table records the value of every variable after every step of an algorithm. AQA uses them to test whether you can execute code in your head, and there are marks available for a table that has been filled in mechanically and correctly even if you have no idea what the algorithm is for.

The method that works under pressure has four rules.

1. **Draw one column per variable, plus a column for any output.** Get the columns from the code, not from the question.
2. **Write a new row every time any variable changes.** Do not overwrite. The examiner is marking the history, not the final state.
3. **Leave a cell blank if that variable did not change on that line.** Repeating the old value is not wrong, but blanks make errors much easier to spot.
4. **Evaluate the condition out loud before you follow a branch.** Most trace table errors are loop control errors, not arithmetic errors.

### Worked example

```aqa pseudo-code
a ← 12
b ← 8
WHILE b ≠ 0
    temp ← b
    b ← a MOD b
    a ← temp
ENDWHILE
OUTPUT a
```

| a | b | temp | Output |
| 12 | 8 | | |
| | 4 | 8 | |
| 8 | | | |
| | 0 | 4 | |
| 4 | | | |
| | | | 4 |

Reading the table back: `12 MOD 8` is 4, so b becomes 4 and a becomes 8. Then `8 MOD 4` is 0, so b becomes 0 and a becomes 4. The condition `b ≠ 0` is now false, the loop ends and 4 is output. The algorithm finds the highest common factor of 12 and 8, which is indeed 4, but you did not need to know that to fill the table in correctly.

!key Work out what it does at the end, not the start :: Never try to guess the purpose of an algorithm before tracing it. Trace it mechanically, then look at the output column and ask what that output is. That is how the "state the purpose of this algorithm" mark is earned.

!warn Off by one on the loop exit :: The commonest single error is running the loop one extra time. Before you write a new row, check the condition against the values in the row above, not the values you are about to write.
"""),
    ],
    keyterms=[
        ("Pseudo-code", "A way of writing an algorithm that has the structure of program code but is not tied to any one programming language."),
        ("Assignment", "Storing a value in a variable, written in AQA pseudo-code with a left arrow."),
        ("Flowchart", "A diagram that represents an algorithm using standard symbols joined by flow lines."),
        ("Decision", "A flowchart symbol, drawn as a diamond, containing a question with exactly two exits labelled Yes and No."),
        ("Trace table", "A table that records the value of every variable after each step of an algorithm so that its behaviour can be checked by hand."),
        ("Definite iteration", "A loop that repeats a known number of times, written in AQA pseudo-code with FOR and ENDFOR."),
        ("Indefinite iteration", "A loop that repeats until a condition is met, written with WHILE or REPEAT."),
        ("DIV", "The integer division operator, which gives the whole number of times one value divides into another."),
        ("MOD", "The modulus operator, which gives the remainder after integer division."),
        ("SUBSTRING", "An AQA string routine that returns the characters between two given index positions inclusive."),
    ],
    grade="""
Two things separate top answers here, and both are habits rather than knowledge.

**Read AQA pseudo-code as AQA wrote it.** The arrow means assignment, `=` means comparison, indexes start at 0 and `SUBSTRING` takes a finishing index rather than a length. Candidates who quietly translate the code into Python in their heads lose marks on exactly these four points, because Python does the opposite on two of them.

**Trace mechanically, interpret afterwards.** Strong candidates fill in the whole table without thinking about meaning, then read the output column and describe what the algorithm does. Weak candidates decide what the algorithm probably does, then fill the table in to match, and get both parts wrong together.

**Say what changed and when.** In a "describe what this algorithm does" question, the marks are for the effect, not for a line by line commentary. "It counts how many values in the array are greater than the average" is worth more than six lines of "then it adds one to i".

+ Read and write all four AQA loop and selection structures without checking
+ State the difference between WHILE and REPEAT in one sentence, including the zero times point
+ Work out LEN, POSITION and SUBSTRING results for a given string with no hesitation
+ Complete a trace table for a nested loop without losing track of the inner counter
""",
    mistakes=[
        "Using = for assignment in AQA pseudo-code. AQA uses a left arrow, and = only ever means equal to.",
        "Reading the second argument of SUBSTRING as a length. It is the index of the last character, and it is included.",
        "Starting array or string indexing at 1. AQA indexes from 0.",
        "Filling in only the final value of each variable in a trace table instead of a row per change, which throws away most of the marks.",
        "Putting a variable name rather than a condition inside a decision diamond, so the two exits cannot be labelled Yes and No.",
        "Saying a WHILE loop always runs at least once. That is REPEAT. A WHILE loop can run zero times.",
    ],
    quiz=[
        Q("In AQA pseudo-code, what does the left arrow mean?",
          ["Assignment: store the value on the right in the variable on the left",
           "Comparison: test whether two values are equal",
           "Output the value to the screen",
           "Return a value from a subroutine"], 0,
          "AQA reserves the arrow for assignment so that = can only ever mean 'is equal to', which removes a whole class of ambiguity from exam questions."),
        Q("What is the value of `SUBSTRING(1, 3, 'binary')`?",
          ["'ina'", "'in'", "'bin'", "'nar'"], 0,
          "Indexing starts at 0, and both ends are included, so indexes 1, 2 and 3 of 'binary' are i, n and a."),
        Q("What is the value of `POSITION('computer', 'm')`?",
          ["2", "3", "1", "4"], 0,
          "Indexing starts at 0, so c is 0, o is 1 and m is 2."),
        Q("Which loop is guaranteed to run at least once?",
          ["REPEAT ... UNTIL", "WHILE ... ENDWHILE", "FOR ... ENDFOR", "IF ... ENDIF"], 0,
          "REPEAT tests its condition at the end of the body, so the body has already run once before the test happens."),
        Q("What is the result of `17 DIV 5`?",
          ["3", "3.4", "2", "85"], 0,
          "DIV is integer division, so it gives the whole number of times 5 goes into 17 and discards the remainder."),
        Q("What is the result of `17 MOD 5`?",
          ["2", "3", "3.4", "0"], 0,
          "MOD returns the remainder, and 5 goes into 17 three times with 2 left over."),
        Q("Which flowchart symbol is drawn as a parallelogram?",
          ["Input or output", "Process", "Decision", "Terminal"], 0,
          "The parallelogram is reserved for reading a value in or displaying one. Calculations go in a rectangle."),
        Q("In a flowchart, what does an arrow that travels back up the page to an earlier decision indicate?",
          ["Iteration", "Selection", "A subroutine call", "The end of the algorithm"], 0,
          "A backward flow line is the only way a loop can be drawn, so the decision it returns to is the loop condition."),
        Q("When completing a trace table, what should you write each time a variable changes?",
          ["A new row showing the changed value", "Nothing, only the final value matters",
           "The value in the same cell, overwriting the old one", "Only the loop counter"], 0,
          "The examiner is marking the sequence of changes, so overwriting cells throws away most of the available marks."),
        Q("Which AQA keyword closes a FOR loop?",
          ["ENDFOR", "NEXT", "LOOP", "UNTIL"], 0,
          "Every AQA block closes with an END keyword, with the single exception of REPEAT, which is closed by UNTIL."),
    ],
    exam=[
        EQ("State the difference between a WHILE loop and a REPEAT UNTIL loop.", 2, [
            MP("A WHILE loop tests its condition before the body runs, so it may run zero times",
               ["before", "at the start", "zero times", "may not run", "tested first"]),
            MP("A REPEAT loop tests its condition after the body runs, so it always runs at least once",
               ["after", "at the end", "at least once", "always runs once", "tested last"]),
        ], "A WHILE loop tests its condition before the body is executed, so if the condition is false at the start the body never runs at all. A REPEAT UNTIL loop tests its condition after the body has been executed, so the body always runs at least once whatever the condition.",
           command="State"),
        EQ("Describe the purpose of a trace table and explain how it is used to find an error in an algorithm.", 4, [
            MP("A trace table records the value of each variable at each step of the algorithm",
               ["records the value", "each variable", "step by step", "values of variables", "each line"]),
            MP("The algorithm is executed by hand rather than run on a computer",
               ["by hand", "manually", "dry run", "on paper", "without running"]),
            MP("The recorded values are compared with the values that were expected",
               ["compared", "expected values", "should be", "check against", "predicted"]),
            MP("The first row where the value differs identifies the line containing the error",
               ["first row", "where it differs", "identifies the line", "locate the error", "pinpoint"]),
        ], "A trace table is a table with one column for each variable, and one for any output, in which the value of every variable is written down after each step of the algorithm. The algorithm is executed by hand rather than run on a computer, so the programmer can see exactly what happens inside it. Each recorded value is then compared with what was expected at that point, and the first row in which the actual value differs from the expected value shows precisely where the algorithm first goes wrong. That narrows a fault down to a single line, which is far quicker than reading the whole algorithm and guessing.",
           command="Describe"),
        EQ("A flowchart contains a diamond shaped symbol. Describe the purpose of this symbol and state what must be true of the paths leaving it.", 3, [
            MP("The diamond represents a decision",
               ["decision", "condition", "question", "selection"]),
            MP("It contains a condition that evaluates to either true or false",
               ["true or false", "yes or no", "condition", "boolean", "either"]),
            MP("Exactly two paths leave it and both must be labelled",
               ["two paths", "two exits", "labelled", "yes and no", "true and false"]),
        ], "The diamond is the decision symbol and it contains a condition that can only evaluate to true or false, such as whether a total is greater than one hundred. Exactly two flow lines leave the symbol, one followed when the condition is true and one when it is false, and both must be clearly labelled Yes and No so that the reader can tell which path is which. If a backward flow line returns to the diamond from below then the decision is controlling a loop rather than a simple selection.",
           command="Describe"),
        EQ("Explain two advantages of writing an algorithm in pseudo-code before writing it in a programming language.", 4, [
            MP("Pseudo-code is not tied to one programming language",
               ["not tied", "any language", "language independent", "not specific", "no particular language"]),
            MP("So the same design can be implemented in Python, C# or VB.NET",
               ["python", "different languages", "implemented in", "translated into", "any programmer"]),
            MP("The logic can be checked before any code is written",
               ["checked", "logic", "before coding", "test the design", "spot errors early"]),
            MP("Which saves time because errors in the method are corrected on paper rather than debugged in code",
               ["saves time", "on paper", "cheaper to fix", "easier to correct", "less debugging"]),
        ], "The first advantage is that pseudo-code is not tied to any one programming language, so the designer does not have to worry about the exact syntax of Python or C# while working out the method. The same pseudo-code can then be handed to any programmer and implemented in whichever language the project uses. The second advantage is that the logic of the solution can be checked, for example with a trace table, before a single line of real code exists. A mistake in the method costs a couple of minutes to fix while it is still pseudo-code, but once it has been built into working code it has to be found by debugging, which takes far longer.",
           command="Explain"),
        EQ("Look at this algorithm.\n\nn ← 5\ntotal ← 1\nWHILE n > 1\n    total ← total * n\n    n ← n - 1\nENDWHILE\nOUTPUT total\n\nState the value output and explain what the algorithm calculates.", 3, [
            MP("The output is 120",
               ["120", "one hundred and twenty"]),
            MP("The algorithm repeatedly multiplies the running total by n while decreasing n",
               ["multiplies", "running total", "decreases", "counts down", "each time"]),
            MP("It calculates the factorial of the starting value of n",
               ["factorial", "5 times 4 times 3", "product of all", "all the integers", "5 4 3 2"]),
        ], "The loop multiplies total by 5, then by 4, then by 3, then by 2, stopping when n reaches 1, so total becomes 120. The algorithm therefore calculates the factorial of the starting value of n, that is the product of every whole number from n down to 1. Tracing it row by row confirms this: total takes the values 5, 20, 60 and 120 as n falls from 5 to 1.",
           command="Explain"),
    ],
)

# ============================================ 3.1.2 / 3.1.3 searching algorithms

T_SEARCH = Topic(
    slug="searching-algorithms",
    title="Efficiency and Searching Algorithms",
    spec="3.1.2, 3.1.3",
    icon="i-search",
    minutes=30,
    blurb="What efficiency actually means for an algorithm, how linear and binary search work step by step, and the exact conditions under which each one is the right choice.",
    fact="Binary search on a list of one billion items needs at most 30 comparisons. Linear search on the same list needs up to one billion. That is the difference between a task finishing before you have looked up from the keyboard and a task you would abandon.",
    sections=[
        Section("What efficiency means", """
Two algorithms can produce exactly the same correct answer and still be worlds apart in usefulness. The **efficiency** of an algorithm is how much of a resource it consumes to get that answer, and at GCSE the resource that matters is the number of steps, which translates into time.

The reason this is worth measuring is that the difference between algorithms grows with the size of the data. On ten items nothing matters. On ten million items the choice of algorithm decides whether a program is instant or unusable.

!key How to compare efficiency without maths :: Count the number of comparisons each algorithm makes on the same data, in the worst case. The one that makes fewer comparisons as the list grows is the more efficient algorithm.

### Worst case, best case

- **Best case** is the luckiest possible input. For linear search that is the item being first.
- **Worst case** is the least lucky input. For linear search that is the item being last, or absent altogether.

Examiners nearly always ask about the worst case, because the best case is a matter of luck and tells you nothing useful about the algorithm.

### The point that earns the mark

A faster algorithm does not need faster hardware. Changing from linear search to binary search on a large sorted list makes a program dramatically quicker on exactly the same machine, because it does less work rather than doing the same work faster. That is the sentence to write when a question asks why algorithm choice matters.
"""),
        Section("Linear search", """
A **linear search** starts at the beginning of the list and compares each item in turn with the value being looked for, stopping when it finds a match or when it reaches the end of the list.

```aqa pseudo-code
SUBROUTINE linearSearch(items, target)
    FOR i ← 0 TO LEN(items) - 1
        IF items[i] = target THEN
            RETURN i
        ENDIF
    ENDFOR
    RETURN -1
ENDSUBROUTINE
```

Searching for 23 in `[4, 8, 15, 16, 23, 42]` compares 4, then 8, then 15, then 16, then 23. Five comparisons, then it stops.

### The properties that matter

- The list **does not have to be sorted**. This is linear search's one real advantage and it is a big one.
- The worst case is **n comparisons** on a list of n items, when the target is last or missing.
- It is simple to write and hard to get wrong.

!key When linear search is the right choice :: When the data is unsorted, when the list is short, or when the list changes so often that keeping it sorted would cost more than the searches save.
"""),
        Section("Binary search", """
A **binary search** works on a **sorted** list. It compares the target with the middle item, and then discards half the list.

1. Find the middle item of the list.
2. If it is the target, stop.
3. If the target is smaller than the middle item, repeat using only the left half.
4. If the target is larger, repeat using only the right half.
5. If there are no items left to check, the target is not in the list.

### Traced on a real list

Searching for 23 in the sorted list `[4, 8, 15, 16, 23, 42]`:

| Step | List being searched | Middle item | Comparison | Action |
| 1 | 4, 8, 15, 16, 23, 42 | 15 | 23 is greater than 15 | Keep the right half: 16, 23, 42 |
| 2 | 16, 23, 42 | 23 | 23 equals 23 | Found, stop |

Two comparisons instead of five. On six items that is barely worth mentioning. The reason binary search matters is what happens as the list grows.

| Items in list | Linear search, worst case | Binary search, worst case |
| 100 | 100 | 7 |
| 1 000 | 1 000 | 10 |
| 1 000 000 | 1 000 000 | 20 |
| 1 000 000 000 | 1 000 000 000 | 30 |

Every time the list doubles, binary search needs just **one** extra comparison, because one extra comparison halves the list one more time. Linear search needs twice as many.

!warn Binary search requires a sorted list :: This is the condition examiners test. If a question describes data arriving in a random order and never being sorted, binary search is not available, however efficient it would be.

!exam Choosing between them in a scenario question :: Ask two questions of the scenario. Is the data sorted? How big is it? Sorted and large means binary. Unsorted, or so small that sorting would cost more than searching, means linear. Say which condition in the scenario made you choose, because that is where the mark is.

### The hidden cost

If the data is not already sorted, binary search is only worth it when you will search many times. Sorting a list takes considerably more work than one linear search, so sorting purely to run a single binary search is slower overall than just doing the linear search.
"""),
    ],
    keyterms=[
        ("Efficiency", "A measure of how much of a resource, usually time or number of steps, an algorithm uses to solve a problem."),
        ("Linear search", "A search that examines each item in a list in turn until the target is found or the end of the list is reached."),
        ("Binary search", "A search on a sorted list that repeatedly compares the target with the middle item and discards the half that cannot contain it."),
        ("Worst case", "The input that causes an algorithm to perform the greatest number of steps."),
        ("Comparison", "One test of whether an item matches or is greater or less than the value being searched for, used as the unit for measuring search efficiency."),
        ("Sorted list", "A list whose items are in ascending or descending order, which is the condition binary search requires."),
        ("Middle item", "The item at the centre of the section of the list currently being searched by a binary search."),
    ],
    grade="""
The knowledge on this topic is small and the marks are almost all in the comparison.

**Never say binary search is 'better'.** Say it is more efficient on a large sorted list, and then name the condition it needs. An answer that recommends binary search without checking that the data is sorted is throwing away the whole point of the question.

**Quantify the difference.** "Binary search is faster" is one mark at most. "Binary search halves the number of remaining items with each comparison, so a list of one million needs about twenty comparisons rather than up to one million" is the top level answer.

**Handle the sorting cost honestly.** Top candidates notice that if the data must be sorted first, and it is only searched once, linear search wins. That single observation is often the difference between four marks and six on an evaluate question.

+ Trace a binary search on a given sorted list and count the comparisons correctly
+ State the one advantage of linear search in a single sentence
+ Explain why binary search only needs one more comparison when the list doubles in size
+ Decide between the two algorithms for a described scenario and justify it using the scenario's own details
""",
    mistakes=[
        "Recommending binary search on unsorted data. Binary search is only defined for a sorted list.",
        "Saying binary search 'splits the list in half once'. It halves the remaining list repeatedly, at every comparison.",
        "Claiming linear search has no advantages. It works on unsorted data and it is faster than sort plus binary search for a one off lookup.",
        "Comparing algorithms on tiny lists and concluding one is better. Efficiency questions are about behaviour as the list grows.",
        "Counting the comparisons wrongly in a trace by forgetting that the middle item is itself compared before the list is halved.",
    ],
    quiz=[
        Q("What condition must be met before a binary search can be used?",
          ["The list must be sorted", "The list must contain only numbers",
           "The list must have an even number of items", "The list must be stored in RAM"], 0,
          "Binary search decides which half to discard by comparing with the middle item, and that decision is only valid if the list is in order."),
        Q("A linear search is performed on a list of 500 unsorted names. What is the maximum number of comparisons needed?",
          ["500", "250", "9", "1"], 0,
          "In the worst case the target is the last item, or is not present at all, so every one of the 500 items must be compared."),
        Q("Roughly how many comparisons does a binary search need in the worst case on a sorted list of 1000 items?",
          ["10", "100", "500", "1000"], 0,
          "Each comparison halves the list, and 1000 can be halved about ten times before one item remains."),
        Q("Which is the single advantage of linear search over binary search?",
          ["It works on data that is not sorted", "It needs fewer comparisons",
           "It uses less memory per comparison", "It can search two lists at once"], 0,
          "Linear search makes no assumption about order, which is why it is the only option when the data arrives unsorted."),
        Q("A binary search is looking for 30 in [10, 20, 30, 40, 50, 60, 70]. Which item is compared first?",
          ["40", "10", "30", "70"], 0,
          "The middle of a list of seven items is the fourth item, which is 40, so that comparison happens before anything else."),
        Q("If a sorted list doubles in size, how does the worst case for a binary search change?",
          ["It increases by one comparison", "It doubles",
           "It stays exactly the same", "It increases by half the list length"], 0,
          "One extra comparison provides one extra halving, which is exactly what is needed to cope with twice as many items."),
        Q("Which statement about the efficiency of an algorithm is correct?",
          ["A more efficient algorithm completes the same task in fewer steps on the same hardware",
           "A more efficient algorithm requires a faster processor",
           "Efficiency only matters for programs that use the internet",
           "Efficiency is measured in bytes of source code"], 0,
          "Efficiency is about the amount of work done, so a better algorithm speeds a program up without any change to the machine it runs on."),
        Q("Data arrives in a random order and each item is searched for only once before the data is replaced. Which approach is best?",
          ["Linear search, because sorting first would cost more than the search saves",
           "Sort the data then use binary search, because binary search is always faster",
           "Sort the data twice then use linear search",
           "Neither search can be used on random data"], 0,
          "Sorting is far more expensive than a single linear pass, so sorting purely to enable one binary search makes the program slower overall."),
        Q("How many comparisons does a linear search need to find 4 at the start of [4, 8, 15, 16, 23, 42]?",
          ["1", "3", "6", "0"], 0,
          "Linear search checks the first item first, so a target at the front is the best case and needs a single comparison."),
        Q("Why is the worst case, rather than the best case, normally used to compare algorithms?",
          ["The best case depends on luck and says nothing about how the algorithm behaves in general",
           "The best case is impossible to calculate",
           "The worst case is always the same for every algorithm",
           "The best case only applies to sorted data"], 0,
          "Any search can get lucky and find the target immediately, so only the worst case reveals a genuine difference between the methods."),
    ],
    exam=[
        EQ("Describe how a binary search finds a value in a sorted list.", 4, [
            MP("The middle item of the list is examined",
               ["middle item", "midpoint", "centre", "middle value"]),
            MP("If it matches the target the search stops",
               ["matches", "found", "equal", "stop", "same as target"]),
            MP("If the target is smaller the upper half is discarded, and if larger the lower half is discarded",
               ["smaller", "larger", "discard", "half is removed", "left half", "right half"]),
            MP("The process repeats on the remaining half until the item is found or no items remain",
               ["repeats", "until found", "no items remain", "again", "continues"]),
        ], "A binary search first examines the item in the middle of the sorted list. If that item is the one being searched for, the search stops and reports success. If the target is smaller than the middle item then every item to the right of the middle can be discarded, and if it is larger then every item to the left can be discarded, because the list is in order. The search then repeats on whichever half remains, examining its middle item, and continues halving until the target is found or until no items are left, at which point the value is known not to be in the list.",
           command="Describe"),
        EQ("A list of 1024 sorted values is searched. State the maximum number of comparisons required by a linear search and by a binary search.", 2, [
            MP("Linear search requires up to 1024 comparisons",
               ["1024", "one thousand and twenty four", "every item", "all of them"]),
            MP("Binary search requires up to 10 or 11 comparisons",
               ["10", "11", "ten", "eleven"]),
        ], "A linear search must compare every item in the worst case, so it requires up to 1024 comparisons. A binary search halves the remaining list at each step, and 1024 can be halved ten times to reach a single item, so it requires at most about ten or eleven comparisons.",
           command="State"),
        EQ("Explain one advantage of a linear search over a binary search.", 2, [
            MP("A linear search does not require the data to be sorted",
               ["not sorted", "unsorted", "any order", "no need to sort", "does not require sorting"]),
            MP("So it can be used on data that arrives in a random order, or where sorting would cost more time than it saves",
               ["random order", "cost of sorting", "sorting takes time", "saves time", "arrives unsorted"]),
        ], "The advantage of a linear search is that it does not require the list to be in any particular order, whereas a binary search only works on sorted data. This means a linear search can be used immediately on data that arrives in a random order, and for a list that is searched only once it is often faster overall, because sorting the list first would take considerably more time than the linear search itself.",
           command="Explain"),
        EQ("A company stores 5 million customer records, sorted by customer number, and looks up records thousands of times each hour. Justify which search algorithm they should use.", 5, [
            MP("Binary search should be used",
               ["binary search", "binary"]),
            MP("The data is already sorted, which is the condition binary search requires",
               ["already sorted", "sorted by", "in order", "condition met", "requires sorted"]),
            MP("Binary search halves the number of remaining records with each comparison",
               ["halves", "half", "divides in two", "each comparison removes"]),
            MP("So it needs about 23 comparisons rather than up to 5 million",
               ["23", "twenty three", "far fewer", "about twenty", "5 million comparisons"]),
            MP("The saving is repeated on every one of thousands of lookups per hour",
               ["thousands of lookups", "every search", "repeated", "each hour", "many times"]),
        ], "The company should use a binary search. The records are already sorted by customer number, so the one condition that binary search requires is satisfied and no sorting cost has to be paid. Binary search compares the target with the middle record and then discards half of the remaining records, repeating until the record is found, so the number of comparisons grows extremely slowly as the data grows. On five million records it needs roughly twenty three comparisons in the worst case, whereas a linear search would need up to five million. Because the system performs thousands of lookups every hour, that saving is multiplied thousands of times over, so the difference between the two algorithms is the difference between an instant response and a system that cannot keep up.",
           command="Justify"),
        EQ("Explain why comparing the efficiency of two algorithms is more useful than comparing how long each takes to run on a particular computer.", 3, [
            MP("Run time depends on the hardware the program is tested on",
               ["hardware", "processor speed", "computer used", "machine", "specification"]),
            MP("Efficiency counts the number of steps or comparisons, which is independent of the machine",
               ["number of steps", "comparisons", "independent", "regardless of hardware", "operations"]),
            MP("So efficiency predicts how the algorithm will behave as the amount of data grows",
               ["as data grows", "larger data", "scales", "size of the list", "grows"]),
        ], "The time a program takes to run depends on the computer it is tested on, so a poor algorithm on a fast processor can appear quicker than a good algorithm on a slow one, which tells you nothing about the algorithms themselves. Measuring efficiency instead counts the number of steps or comparisons the algorithm performs, and that count is a property of the algorithm rather than of the hardware. It also shows how the work grows as the data set grows, which is what actually matters, because two algorithms that look identical on a hundred items can differ by a factor of thousands on a million.",
           command="Explain"),
    ],
)

# ============================================ 3.1.4 sorting algorithms

T_SORT = Topic(
    slug="sorting-algorithms",
    title="Sorting Algorithms",
    spec="3.1.4",
    icon="i-shuffle",
    minutes=32,
    blurb="Bubble sort and merge sort traced pass by pass, why merge sort wins on large lists, and how to answer the compare question without repeating yourself.",
    fact="Merge sort was described by John von Neumann in 1945, on the same machine project that gave us the stored program computer. It is still the algorithm behind the sort routines in several standard libraries today, eighty years later.",
    sections=[
        Section("Bubble sort", """
A **bubble sort** works through the list comparing each pair of adjacent items and swapping them if they are in the wrong order. Each complete pass through the list is called a pass, and after each pass the largest remaining value has moved to its final position at the end.

The name comes from that behaviour: large values rise to the end of the list like bubbles rising to the surface.

### Traced properly

Sorting `[5, 3, 8, 1]` into ascending order.

**Pass 1**

| Compare | List after the comparison |
| 5 and 3, swap | 3, 5, 8, 1 |
| 5 and 8, no swap | 3, 5, 8, 1 |
| 8 and 1, swap | 3, 5, 1, 8 |

8 is now in its final position, so the next pass does not need to look at it.

**Pass 2**

| Compare | List after the comparison |
| 3 and 5, no swap | 3, 5, 1, 8 |
| 5 and 1, swap | 3, 1, 5, 8 |

**Pass 3**

| Compare | List after the comparison |
| 3 and 1, swap | 1, 3, 5, 8 |

A pass then completes with no swaps at all, which tells the algorithm the list is sorted and it stops.

!key The stopping condition :: A bubble sort finishes when a complete pass is made with no swaps. Mentioning this earns a mark, because it is the only way the algorithm knows it is done.

```aqa pseudo-code
SUBROUTINE bubbleSort(items)
    swapped ← True
    WHILE swapped = True
        swapped ← False
        FOR i ← 0 TO LEN(items) - 2
            IF items[i] > items[i + 1] THEN
                temp ← items[i]
                items[i] ← items[i + 1]
                items[i + 1] ← temp
                swapped ← True
            ENDIF
        ENDFOR
    ENDWHILE
    RETURN items
ENDSUBROUTINE
```

### What is good and bad about it

- **Good**: very simple to write and understand, and it needs almost no extra memory because items are swapped inside the original list.
- **Bad**: slow on large lists. Sorting n items takes roughly n squared comparisons, so ten times more data means about a hundred times more work.
"""),
        Section("Merge sort", """
A **merge sort** repeatedly splits the list in half until every sub list contains one item, then merges the sub lists back together in order.

A list of one item is by definition already sorted, which is what makes the strategy work. All the actual sorting happens during the merging.

### The two phases

**Split**: divide the list in half, then halve each half, and keep going until every sub list holds a single item.

```text
        7  3  9  1  5  2
       /                \
   7  3  9            1  5  2
   /     \            /     \
 7      3  9        1      5  2
        /   \              /   \
       3     9            5     2
```

**Merge**: take pairs of sub lists and combine them by repeatedly comparing the front item of each and taking the smaller.

```text
 3 + 9   ->  3 9
 5 + 2   ->  2 5
 7 + 3 9 ->  3 7 9
 1 + 2 5 ->  1 2 5
 3 7 9 + 1 2 5 -> 1 2 3 5 7 9
```

Look closely at the last merge. Compare 3 and 1, take 1. Compare 3 and 2, take 2. Compare 3 and 5, take 3. Compare 7 and 5, take 5. Compare 7 and nothing left on the right, so take 7 then 9. Six comparisons to merge six items, and that is the pattern: each merge costs roughly as many comparisons as there are items in it.

!key Why merge sort is fast :: There are only about log n rounds of merging, because the list can only be halved that many times, and each round costs about n comparisons. Doubling the data therefore roughly doubles the work rather than quadrupling it.
"""),
        Section("Comparing the two", """
This comparison is examined almost every year and the marks come from giving different points rather than repeating one point in three ways.

| | Bubble sort | Merge sort |
| Method | Repeatedly swaps adjacent items | Splits into single items then merges in order |
| Efficiency on large lists | Poor, roughly n squared comparisons | Good, roughly n log n comparisons |
| Memory used | Very little, sorts in place | More, because sub lists are held in memory during merging |
| Ease of writing | Simple, few lines | More complex, usually recursive |
| Best use | Very small lists, or lists that are almost sorted already | Large lists where speed matters |

### How to structure the answer

An examiner wants a genuine trade off, not a preference. The structure that always scores is:

1. Merge sort is more efficient on large lists, and say why: it halves the problem instead of walking the whole list on every pass.
2. Bubble sort uses less memory, and say why: it swaps items inside the existing list rather than building new sub lists.
3. Conclude by naming the condition that decides it: list size and available memory.

!warn Do not say bubble sort is 'useless' :: On a list of eight items, or on a list that is already nearly in order, a bubble sort finishes almost immediately and needs no extra memory. Blanket statements lose the evaluation marks.

!exam Number of passes questions :: If asked how many passes a bubble sort needs on a list of n items, the answer is at most n minus 1, because after n minus 1 items are in place the last one has nowhere else to be.
"""),
    ],
    keyterms=[
        ("Bubble sort", "A sort that repeatedly compares adjacent items and swaps them if they are in the wrong order until a pass produces no swaps."),
        ("Pass", "One complete run through the list by a bubble sort, after which the largest remaining item is in its final position."),
        ("Swap", "Exchanging the positions of two adjacent items, which requires a temporary variable to avoid losing one of the values."),
        ("Merge sort", "A sort that divides the list into single item sub lists and then repeatedly merges pairs of sub lists in order."),
        ("Merge", "Combining two sorted sub lists into one sorted list by repeatedly taking the smaller of the two front items."),
        ("In place", "Sorting that rearranges the original list without needing significant extra memory, as a bubble sort does."),
        ("Divide and conquer", "The strategy of splitting a problem into smaller parts, solving each, and combining the results, as merge sort does."),
    ],
    grade="""
The trace marks are free if you are systematic, and the comparison marks are where grades are decided.

**Show every pass, not every swap.** When asked to show the list after each pass, write the state of the whole list at the end of each complete pass. Writing every individual swap wastes time and often loses the mark because the examiner cannot find the pass boundaries.

**Give the reason with the property.** "Merge sort is faster" is not a mark. "Merge sort is faster on large lists because halving the list means the number of rounds grows very slowly, while a bubble sort has to walk the whole list once per pass" is two.

**Always concede something.** An evaluation that says merge sort is better in every way is wrong: it uses more memory and is harder to implement. Naming that cost is what moves an answer into the top band.

+ Trace a bubble sort on six items showing the list at the end of each pass
+ Trace a merge sort showing both the splitting and the merging stages
+ State the stopping condition of a bubble sort
+ Give three genuinely different points of comparison between the two algorithms
""",
    mistakes=[
        "Showing the list after each swap rather than after each pass when the question asks for passes.",
        "Forgetting the temporary variable when describing a swap, which would overwrite one of the two values.",
        "Saying merge sort sorts each half and then joins them, without explaining that the halving continues until each sub list holds one item.",
        "Claiming merge sort is better in every respect. It needs more memory and is harder to program.",
        "Saying a bubble sort finishes after a fixed number of passes. It finishes when a pass completes with no swaps, which may be sooner.",
    ],
    quiz=[
        Q("After one complete pass of a bubble sort in ascending order, which item is guaranteed to be in its final position?",
          ["The largest item, at the end of the list", "The smallest item, at the start of the list",
           "The middle item", "No item is guaranteed to be in place"], 0,
          "Each comparison pushes the larger value one place to the right, so by the end of the pass the largest value has been carried all the way to the end."),
        Q("What tells a bubble sort that the list is now sorted?",
          ["A complete pass finishes with no swaps made", "The first pass has finished",
           "The list length has been reached", "The middle item stops changing"], 0,
          "If nothing needed swapping during a whole pass then no pair is out of order, which is precisely the definition of sorted."),
        Q("In a merge sort, what is the list repeatedly divided into?",
          ["Sub lists, until each contains a single item", "Two halves, only once",
           "Sub lists of four items", "Sorted and unsorted sections"], 0,
          "The division continues all the way down because a single item is trivially sorted, which gives the merging stage something valid to start from."),
        Q("During the merge stage, how is the next item chosen?",
          ["The smaller of the two items at the front of the sub lists is taken",
           "The first item of the left sub list is always taken",
           "The largest item in either sub list is taken",
           "Items are taken at random and then checked"], 0,
          "Because both sub lists are already sorted, the smallest remaining item overall must be at the front of one of them."),
        Q("Which sort generally requires more memory?",
          ["Merge sort, because sub lists are held during merging",
           "Bubble sort, because it stores every swap",
           "They use exactly the same amount",
           "Neither uses any extra memory"], 0,
          "A bubble sort rearranges items inside the original list, while merge sort has to hold the sub lists it is building."),
        Q("How many passes at most does a bubble sort need on a list of 6 items?",
          ["5", "6", "36", "3"], 0,
          "After five items have been placed the sixth has nowhere else to go, so n minus 1 passes are enough."),
        Q("Which statement about bubble sort is correct?",
          ["It is simple to implement and sorts the list in place",
           "It is the fastest known sorting algorithm",
           "It requires the list to be partly sorted first",
           "It cannot sort text, only numbers"], 0,
          "Simplicity and low memory use are its genuine advantages, which is why it survives despite being slow on large data."),
        Q("Roughly how does the work done by a bubble sort grow when the list size is doubled?",
          ["It roughly quadruples", "It roughly doubles", "It stays the same", "It increases by one pass"], 0,
          "Bubble sort does about n squared comparisons, and squaring a doubled value multiplies the work by four."),
        Q("A merge sort is applied to [8, 2, 5, 1]. What are the sub lists immediately before merging begins?",
          ["[8], [2], [5], [1]", "[8, 2], [5, 1]", "[8, 2, 5], [1]", "[1, 2, 5, 8]"], 0,
          "Splitting continues until every sub list holds exactly one item, because a single item is already sorted."),
        Q("Which situation most favours a bubble sort over a merge sort?",
          ["A very short list on a device with very little memory",
           "A list of ten million items",
           "A list that must be sorted as quickly as possible",
           "A list that is in completely random order and very large"], 0,
          "Its low memory use and tiny code size matter most exactly where its poor efficiency does not, which is on small lists."),
    ],
    exam=[
        EQ("Describe how a bubble sort sorts a list of numbers into ascending order.", 4, [
            MP("Adjacent pairs of items are compared",
               ["adjacent", "next to each other", "pairs", "two items", "side by side"]),
            MP("If they are in the wrong order they are swapped",
               ["swapped", "swap", "exchanged", "wrong order", "switch"]),
            MP("This is repeated for the whole list, which is called a pass",
               ["pass", "through the list", "repeated", "whole list", "end of the list"]),
            MP("Passes continue until a pass is completed with no swaps",
               ["no swaps", "until sorted", "pass with no", "nothing is swapped", "no changes"]),
        ], "A bubble sort starts at the beginning of the list and compares the first two items. If they are in the wrong order it swaps them, then moves along one position and compares the next adjacent pair, continuing to the end of the list. One complete journey through the list is called a pass, and at the end of each pass the largest remaining value has been carried to its correct position at the end. The algorithm then begins another pass, and it keeps going until a whole pass is completed without a single swap being made, which shows that no pair is out of order and the list is sorted.",
           command="Describe"),
        EQ("Describe how a merge sort works.", 4, [
            MP("The list is repeatedly divided in half",
               ["divided", "split", "halved", "in half", "broken up"]),
            MP("Until each sub list contains only one item",
               ["one item", "single item", "single element", "sub lists of one"]),
            MP("Pairs of sub lists are then merged back together",
               ["merged", "combined", "joined", "put back together", "pairs"]),
            MP("During each merge the smaller of the two front items is taken first, so the result stays in order",
               ["smaller", "compared", "in order", "front item", "smallest first"]),
        ], "A merge sort repeatedly divides the list in half, then divides each half in half, and continues until every sub list contains only one item, at which point every sub list is trivially in order. It then merges the sub lists back together in pairs. To merge two sub lists it compares the item at the front of each and takes whichever is smaller, repeating until one sub list is empty and then taking whatever is left in the other. Because both inputs to every merge are already sorted, the merged result is sorted too, and after the final merge the whole list is in order.",
           command="Describe"),
        EQ("The list [6, 2, 9, 4] is sorted using a bubble sort. Show the contents of the list after each of the first two passes.", 2, [
            MP("After pass 1 the list is 2, 6, 4, 9",
               ["2 6 4 9", "2, 6, 4, 9"]),
            MP("After pass 2 the list is 2, 4, 6, 9",
               ["2 4 6 9", "2, 4, 6, 9"]),
        ], "During the first pass 6 and 2 are swapped to give 2, 6, 9, 4, then 6 and 9 are left alone, then 9 and 4 are swapped, so the list after pass one is 2, 6, 4, 9. During the second pass 2 and 6 are left alone, then 6 and 4 are swapped, so the list after pass two is 2, 4, 6, 9.",
           command="Write"),
        EQ("Compare a bubble sort and a merge sort. Your answer should refer to efficiency and memory use.", 6, [
            MP("A bubble sort repeatedly swaps adjacent items, while a merge sort divides the list and merges it back",
               ["adjacent", "divides", "swaps", "merges", "splits"]),
            MP("A merge sort is more efficient on large lists",
               ["more efficient", "faster on large", "quicker", "fewer comparisons"]),
            MP("Because halving the list means the number of rounds grows very slowly as the list grows",
               ["halving", "halves", "grows slowly", "log", "rounds", "doubling"]),
            MP("A bubble sort needs roughly n squared comparisons, so doubling the data quadruples the work",
               ["n squared", "quadruples", "four times", "squared", "much slower"]),
            MP("A bubble sort uses less memory because it sorts in place",
               ["less memory", "in place", "no extra", "same list", "little memory"]),
            MP("A merge sort needs additional memory to hold the sub lists while merging",
               ["additional memory", "extra memory", "sub lists", "more memory", "stores"]),
        ], "A bubble sort works by repeatedly comparing adjacent pairs of items and swapping any that are in the wrong order, whereas a merge sort divides the list until each sub list holds one item and then merges the sub lists back together in order. On large lists a merge sort is considerably more efficient, because each round of merging halves the number of sub lists, so the number of rounds grows extremely slowly even as the list becomes very large. A bubble sort has to walk the whole list once per pass and may need almost as many passes as there are items, which means roughly n squared comparisons, so doubling the size of the list roughly quadruples the work. The trade off is memory. A bubble sort rearranges items inside the original list and so needs almost no extra memory, while a merge sort has to hold the sub lists it is building as well as the original data. For a small list, or on a device with very little memory, a bubble sort is therefore a reasonable choice, but for a large list where speed matters a merge sort is far better.",
           command="Compare"),
        EQ("Explain why a bubble sort may need fewer passes on a list that is already almost in order.", 3, [
            MP("A bubble sort stops when a pass completes with no swaps",
               ["no swaps", "stops", "pass with no", "terminates", "finishes early"]),
            MP("An almost sorted list needs few swaps, so that condition is reached quickly",
               ["few swaps", "almost sorted", "quickly", "already in order", "reached sooner"]),
            MP("So the algorithm can finish after only one or two passes rather than n minus 1",
               ["one or two passes", "fewer passes", "n minus 1", "early", "does not need"]),
        ], "A bubble sort does not run a fixed number of passes. It keeps making passes until one complete pass finishes without a single swap, because that shows no adjacent pair is out of order and the list must therefore be sorted. If the list is already almost in order then very few items need swapping, so the algorithm reaches a swap free pass after only one or two passes rather than after the n minus 1 passes it would need in the worst case. This is one of the few situations in which a bubble sort performs well.",
           command="Explain"),
    ],
)


# ================================================== 3.2.1 to 3.2.5 programming

T_PROGFUND = Topic(
    slug="programming-fundamentals",
    title="Programming Fundamentals",
    spec="3.2.1 to 3.2.5",
    icon="i-python",
    minutes=30,
    blurb="Data types, variables and constants, every operator AQA can ask about, and the three programming constructs that between them can express any algorithm ever written.",
    fact="The three construct rule is not a teaching simplification. In 1966 Bohm and Jacopini proved mathematically that sequence, selection and iteration are enough to express every computable function. Nothing else is strictly necessary.",
    sections=[
        Section("Data types", """
A **data type** tells the computer what kind of value a variable holds, which decides how many bits it uses, what operations are legal on it and how the bits are interpreted.

AQA names five data types. Learn the names exactly.

| Data type | Holds | Example |
| Integer | A whole number, positive or negative | `-40`, `0`, `2025` |
| Real | A number with a fractional part | `3.14`, `-0.5`, `2.0` |
| Boolean | One of exactly two values | `True`, `False` |
| Character | A single character | `'K'`, `'7'`, `' '` |
| String | A sequence of characters | `"Hello"`, `"7"`, `""` |

!warn 7 and "7" are not the same thing :: The integer 7 can be multiplied. The string "7" is a single character that happens to look like a digit, and multiplying it either fails or repeats it. Nearly every "why does my program crash" question in an exam turns on this.

### Why the type matters to the machine

The bit pattern `01000001` is the integer 65, the character A, or part of a real number, depending entirely on what type the program says it is. The bits alone mean nothing. The type is what gives them meaning.

That is also why type errors are so common: the computer will happily do something with a value, it just may not be the thing you meant.
"""),
        Section("Variables and constants", """
A **variable** is a named location in memory whose value can change while the program runs. A **constant** is a named value that is fixed when the program is written and cannot change while it runs.

```pseudo
CONSTANT vat ← 0.2
price ← 40
total ← price + (price * vat)
OUTPUT total
```

### Why constants exist at all

You could simply write `0.2` everywhere it is needed. Three reasons not to:

- **Readability.** `price * vat` says what is happening. `price * 0.2` does not.
- **One place to change.** If the rate changes, you edit one line rather than hunting through a program for every `0.2`, and you cannot miss one.
- **Safety.** The compiler or interpreter will stop you accidentally assigning to a constant, which catches a whole class of bug before the program ever runs.

!key Use a constant when the value is fixed for the whole run :: The test is not "does it change" but "should the program be allowed to change it". A VAT rate, the number of players in a game, the maximum length of a password: all constants.

### Assignment

The `←` symbol in AQA pseudo-code means assignment: work out the value on the right, then store it in the name on the left. It does not mean equality.

```pseudo
count ← count + 1
```

As mathematics that is nonsense. As assignment it is perfectly sensible: take the current value of count, add one, put the answer back into count.
"""),
        Section("Operators", """
AQA divides operators into three groups, and the specification names all of them.

### Arithmetic operators

| Operator | Meaning | Example | Result |
| `+` | Add | `7 + 2` | `9` |
| `-` | Subtract | `7 - 2` | `5` |
| `*` | Multiply | `7 * 2` | `14` |
| `/` | Real division | `7 / 2` | `3.5` |
| `DIV` | Integer division, the whole part only | `7 DIV 2` | `3` |
| `MOD` | Modulus, the remainder | `7 MOD 2` | `1` |

DIV and MOD are examined constantly, because together they let you take a number apart. `seconds DIV 60` gives whole minutes and `seconds MOD 60` gives the seconds left over. `n MOD 2 = 0` tests whether n is even. `n MOD 10` gives the last digit.

### Relational operators

`=` equal to, `≠` not equal to, `<` less than, `>` greater than, `≤` less than or equal to, `≥` greater than or equal to.

Every one of these produces a Boolean. That is the whole point of them: they turn a comparison into something selection and iteration can test.

### Boolean operators

`AND` is true only when both sides are true. `OR` is true when at least one side is true. `NOT` reverses.

```pseudo
IF age ≥ 13 AND age ≤ 19 THEN
    OUTPUT 'teenager'
ENDIF
```

!warn The classic mistake :: `IF grade = 'A' OR 'B'` does not work. The right hand side of the OR must be a complete comparison, so it has to be `IF grade = 'A' OR grade = 'B'`. Examiners set this deliberately.
"""),
        Section("The three constructs", """
Every program ever written is built from three things.

### Sequence

Statements run in the order they are written, one after another. Order matters: you cannot use a variable before you have given it a value.

### Selection

The program chooses between paths based on a condition.

```pseudo
IF mark ≥ 70 THEN
    grade ← 'Distinction'
ELSE IF mark ≥ 50 THEN
    grade ← 'Merit'
ELSE IF mark ≥ 40 THEN
    grade ← 'Pass'
ELSE
    grade ← 'Fail'
ENDIF
```

The order of those conditions is doing real work. A mark of 80 satisfies all three tests, and it gets Distinction only because that test comes first. Reverse the order and every passing student gets a Pass.

### Iteration

The program repeats statements. AQA distinguishes two kinds, and the distinction is examined.

**Count controlled** iteration repeats a number of times known before the loop starts.

```pseudo
FOR i ← 1 TO 5
    OUTPUT i * i
ENDFOR
```

**Condition controlled** iteration repeats while a condition holds, and nothing decides in advance how many times that will be.

```pseudo
REPEAT
    password ← USERINPUT
UNTIL password = stored
```

A `WHILE` loop tests the condition before the body, so it may run zero times. A `REPEAT UNTIL` loop tests afterwards, so it always runs at least once. That difference is worth a mark on its own.

!exam Choosing the loop in an exam answer :: "The number of items in the list is known, so a count controlled FOR loop is appropriate" earns the mark. "I would use a for loop" does not.
"""),
    ],
    keyterms=[
        ("Variable", "A named memory location whose value can change while the program is running."),
        ("Constant", "A named value fixed when the program is written, which cannot be changed while it runs."),
        ("Assignment", "Working out the value of an expression and storing the result in a named location."),
        ("Data type", "A classification that tells the computer how to interpret and store a value."),
        ("Integer", "A whole number, with no fractional part."),
        ("Real", "A number that may have a fractional part."),
        ("Boolean", "A data type with exactly two possible values, True and False."),
        ("DIV", "Integer division, giving only the whole number part of the result."),
        ("MOD", "The modulus operator, giving the remainder after an integer division."),
        ("Sequence", "Statements carried out one after another in the order written."),
        ("Selection", "Choosing between different paths through a program based on a condition."),
        ("Iteration", "Repeating a section of a program, either a set number of times or while a condition holds."),
        ("Count controlled iteration", "A loop that repeats a number of times known before it starts."),
        ("Condition controlled iteration", "A loop that repeats while a condition is true, for an unknown number of repeats."),
    ],
    grade="""
Top answers on this topic are precise in three ways.

**They name the construct and justify it.** Not "use a loop" but "use a condition controlled loop, because the number of attempts the user needs is not known in advance".

**They talk about types as constraints, not labels.** A grade 9 answer says that casting the input to an integer is necessary because `USERINPUT` returns a string and a string cannot be compared numerically. A grade 5 answer says "you need to change it to a number".

**They read code before judging it.** Most "explain why this program does not work" questions have their answer in the order of the lines or the direction of a comparison. Trace two or three values through by hand before writing anything.
""",
    mistakes=[
        "Writing IF x = 1 OR 2. Each side of a Boolean operator must be a complete comparison.",
        "Confusing DIV and MOD. DIV gives the whole number of times it goes in, MOD gives what is left over.",
        "Treating = as equality in an assignment. In pseudo-code AQA uses an arrow precisely to stop this confusion.",
        "Saying a WHILE loop always runs at least once. It is REPEAT UNTIL that guarantees one pass.",
        "Calling something a constant because it does not happen to change. A constant is declared as one and cannot be changed.",
    ],
    quiz=[
        Q("What is the result of 17 DIV 5?", ["3", "3.4", "2", "85"], 0,
          "DIV is integer division and gives only the whole number part. Five goes into seventeen three times, so the answer is 3. The remainder, 2, is what 17 MOD 5 would give."),
        Q("What is the result of 17 MOD 5?", ["2", "3", "3.4", "12"], 0,
          "MOD gives the remainder after integer division. Five goes into seventeen three times with two left over, so 17 MOD 5 is 2."),
        Q("Which data type would be most appropriate for storing a student's average grade of 68.4?", ["Real", "Integer", "String", "Boolean"], 0,
          "A real number can hold a fractional part. An integer would lose the .4, and while a string could hold the characters, you could not then do arithmetic with it."),
        Q("Which of these is true of a REPEAT UNTIL loop but not a WHILE loop?", ["The body always runs at least once", "It can repeat forever", "It uses a condition", "It is count controlled"], 0,
          "A REPEAT UNTIL loop tests its condition after the body, so the body has always run once before the test happens. A WHILE loop tests first, so it may run zero times."),
        Q("What does the expression n MOD 2 = 0 test?", ["Whether n is even", "Whether n is positive", "Whether n is a whole number", "Whether n is divisible by 10"], 0,
          "Dividing by 2 leaves a remainder of 0 exactly when the number is even, so n MOD 2 = 0 is the standard test for evenness."),
        Q("Why would a programmer declare the number of players in a game as a constant?", ["Because it is fixed for the whole run and giving it a name makes the code readable and safe to change", "Because constants use less memory than variables", "Because the game will run faster", "Because integers must always be constants"], 0,
          "A constant is used when a value should be fixed for the run. It makes the code readable, it can be changed in one place, and the language will stop the program accidentally assigning to it."),
        Q("A program contains total ← total + price. What happens?", ["The current values of total and price are added and the result is stored back in total", "total is compared with total plus price", "price is copied into total", "An error occurs because total appears twice"], 0,
          "The right hand side is evaluated first using the current values, and the result is then assigned to the name on the left. Using a variable on both sides is completely normal."),
        Q("Which construct would be most appropriate for processing every item in a list of 40 names?", ["Count controlled iteration", "Condition controlled iteration", "Selection", "Sequence"], 0,
          "The number of repeats is known before the loop starts, which is exactly the definition of count controlled iteration."),
        Q("What is wrong with IF grade = 'A' OR 'B' THEN?", ["The right hand side of the OR is not a complete comparison", "OR is not a valid operator", "Characters cannot be compared", "grade has not been declared"], 0,
          "Boolean operators join two complete conditions. The line must be written IF grade = 'A' OR grade = 'B' THEN."),
        Q("A variable holds the value \"25\" as a string. What happens if the program tries to add 5 to it?", ["It fails or produces unexpected output, because a string is not a number", "It gives 30", "It gives 255", "It converts automatically and gives 30 in every language"], 0,
          "A string is a sequence of characters, not a number. Depending on the language the operation fails or joins the values together, which is why input must be cast to a number before arithmetic."),
    ],
    exam=[
        EQ("State the difference between a variable and a constant.", 2, [
            MP("A variable can change value while the program is running", ["variable", "can change", "changes", "altered", "varies"]),
            MP("A constant is fixed when the program is written and cannot change while it runs", ["constant", "cannot change", "fixed", "stays the same", "not altered"]),
        ], "A variable is a named memory location whose value can be changed while the program is running. A constant is a named value that is set when the program is written and cannot be changed while the program runs.", command="State"),
        EQ("A program needs to work out how many complete minutes and how many remaining seconds there are in a total of 500 seconds. Write the two expressions needed and give their values.", 4, [
            MP("Uses DIV for the minutes, for example 500 DIV 60", ["div", "500 div 60", "integer division", "whole"]),
            MP("Gives 8 minutes", ["8"]),
            MP("Uses MOD for the seconds, for example 500 MOD 60", ["mod", "500 mod 60", "remainder"]),
            MP("Gives 20 seconds", ["20"]),
        ], "The number of whole minutes is 500 DIV 60, which is 8, because sixty goes into five hundred eight complete times. The seconds left over are 500 MOD 60, which is 20, because eight lots of sixty is four hundred and eighty and five hundred minus four hundred and eighty is twenty.", command="Write"),
        EQ("Explain the difference between count controlled and condition controlled iteration, giving one example of when each would be used.", 4, [
            MP("Count controlled iteration repeats a number of times known before the loop starts", ["known", "fixed number", "set number", "in advance", "how many"]),
            MP("Condition controlled iteration repeats while a condition is true, for an unknown number of repeats", ["condition", "while", "until", "unknown", "not known"]),
            MP("Gives a sensible count controlled example, such as processing every item in a list of known length", ["list", "every item", "ten times", "known length", "each of the"]),
            MP("Gives a sensible condition controlled example, such as repeating until valid input is entered", ["valid input", "password", "until correct", "user enters", "keeps asking"]),
        ], "Count controlled iteration repeats a fixed number of times that is known before the loop begins, so a FOR loop is used. Working through all forty names in a list is a count controlled task, because the length of the list is known. Condition controlled iteration repeats for as long as a condition remains true, and the number of repeats is not known in advance. Asking a user to re-enter a password until it matches is condition controlled, because there is no way to know how many attempts they will need.", command="Explain"),
        EQ("A student writes IF temperature > 30 OR temperature < 10 THEN. Explain what this condition tests and give one situation in which it would be false.", 3, [
            MP("It is true when the temperature is above 30", ["above 30", "greater than 30", "over 30", "hot"]),
            MP("It is also true when the temperature is below 10", ["below 10", "less than 10", "under 10", "cold"]),
            MP("It is false for any value from 10 to 30 inclusive, for example 20", ["between", "10 to 30", "20", "15", "neither", "inclusive"]),
        ], "The condition uses OR, so it is true when at least one of the two comparisons is true. It is therefore true when the temperature is greater than 30 and true when the temperature is less than 10, which means it detects any temperature outside the comfortable range. It is false for any value from 10 to 30 inclusive, so a temperature of 20 would make it false.", command="Explain"),
        EQ("A program asks the user for their age and then tests whether they can vote. The programmer finds that the test never succeeds, even when 18 is entered. Explain the most likely cause and how it would be corrected.", 4, [
            MP("USERINPUT or the equivalent returns a string", ["string", "text", "characters", "not a number"]),
            MP("The program is comparing a string with an integer, which does not behave as expected", ["comparing", "string with number", "different types", "type mismatch"]),
            MP("The input must be cast or converted to an integer", ["cast", "convert", "int", "change to a number", "STRING_TO_INT"]),
            MP("Then the numeric comparison works correctly", ["comparison works", "then it compares", "correct result", "works properly"]),
        ], "The most likely cause is that input is returned as a string, so the variable holds the two characters '1' and '8' rather than the number eighteen. Comparing a string with an integer either fails outright or compares character by character, so the test does not behave as intended and never succeeds. The correction is to cast the input to an integer as soon as it is read, for example age ← STRING_TO_INT(USERINPUT), after which the comparison age ≥ 18 works on two numbers and gives the right answer.", command="Explain"),
    ],
)


# ============================================ 3.2.6 to 3.2.9 data and files

T_DATASTRUCT = Topic(
    slug="data-structures-and-file-handling",
    title="Data Structures, Strings and Files",
    spec="3.2.6 to 3.2.9",
    icon="i-layers",
    minutes=28,
    blurb="Arrays and records, every string operation AQA can ask for, reading and writing text files, and generating random numbers, with the traps that cost marks in each.",
    fact="Almost every programming language counts array positions from zero rather than one. The reason is historical: early languages stored an index as an offset from the start of the block, and the first item sits zero places along.",
    sections=[
        Section("Arrays and records", """
An **array** is a data structure holding many values of the **same type** under one identifier, with each value found by its **index**.

```pseudo
scores ← [14, 9, 21, 6, 18]
OUTPUT scores[0]
scores[3] ← 11
```

Indexing starts at 0, so the five items above are at positions 0, 1, 2, 3 and 4. There is no position 5, and asking for one is an out of range error.

### Why arrays exist

Without an array, thirty scores means thirty separately named variables and thirty near identical lines of code. With an array, one loop handles any number of items and nothing breaks when the number changes.

```pseudo
total ← 0
FOR i ← 0 TO LEN(scores) - 1
    total ← total + scores[i]
ENDFOR
```

!warn LEN gives the number of items, not the last index :: A five item array has LEN 5 and a last index of 4. Looping `TO LEN(scores)` runs one step too far. This single mistake accounts for a large share of runtime errors in exam code.

### Two dimensional arrays

A two dimensional array is an array of arrays, useful for anything grid shaped: a seating plan, a game board, a table of results.

```pseudo
board ← [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
OUTPUT board[1][2]
```

The first index selects the row, the second selects the position within it, so `board[1][2]` is 0.

### Records

A **record** holds several values of **different** types that belong together, each with its own field name.

```pseudo
student.name ← 'Amira'
student.year ← 10
student.average ← 68.4
```

An array holds many of the same thing. A record holds the several different things that describe one thing. A common structure is an array of records: one entry per student, each with a name, a year and an average.
"""),
        Section("String handling", """
AQA names a specific set of string operations, and the exam expects you to use them by name.

| Operation | Meaning | Example on "Computing" |
| `LEN(s)` | Length in characters | `9` |
| `POSITION(s, c)` | Index of the first occurrence of a character | `POSITION('Computing', 'p')` gives `3` |
| `SUBSTRING(a, b, s)` | The characters from index a to index b inclusive | `SUBSTRING(0, 2, 'Computing')` gives `'Com'` |
| Concatenation | Joining strings together | `'Comp' + 'uting'` gives `'Computing'` |
| `STRING_TO_INT` | Converts a string to an integer | `'25'` becomes `25` |
| `INT_TO_STRING` | Converts an integer to a string | `25` becomes `'25'` |
| `CHAR_TO_CODE` | The character set code for a character | `'A'` becomes `65` |
| `CODE_TO_CHAR` | The character for a code | `65` becomes `'A'` |

String indexes also start at 0, so in "Computing" the C is at index 0 and the g is at index 8.

### Converting case with character codes

Because the codes for the letters are in order and the gap between an upper case letter and its lower case partner is always 32, you can change case with arithmetic alone.

```pseudo
code ← CHAR_TO_CODE(letter)
IF code ≥ 65 AND code ≤ 90 THEN
    letter ← CODE_TO_CHAR(code + 32)
ENDIF
```

That is not a curiosity. It is the sort of question AQA sets to check you understand that characters are numbers underneath.
"""),
        Section("Files and random numbers", """
### Reading and writing text files

A program that forgets everything when it closes is of limited use. Writing to a file makes data persist.

```pseudo
scores ← OPEN('results.txt')
line ← scores.readLine()
WHILE NOT scores.endOfFile()
    OUTPUT line
    line ← scores.readLine()
ENDWHILE
scores.close()
```

Three points get marks:

- A file must be **opened** before use and **closed** afterwards. Not closing it can leave data unwritten, because output is often buffered.
- Reading past the end of a file is an error, which is why a loop must test for the end of file.
- Everything read from a text file arrives as a **string**, so numbers have to be converted before arithmetic.

### Random numbers

```pseudo
roll ← RANDOM_INT(1, 6)
```

Computers cannot produce genuinely random numbers. They produce **pseudo-random** numbers from an algorithm and a starting value called a seed, which means the same seed gives the same sequence every time.

!key Why pseudo-random matters :: For a dice game it does not matter. For anything security related it matters enormously, because a predictable sequence means predictable keys. That is the reason AQA distinguishes the two words.
"""),
    ],
    keyterms=[
        ("Array", "A data structure holding multiple values of the same data type under one identifier, accessed by index."),
        ("Index", "The position of an item within an array or string, counted from zero."),
        ("Two dimensional array", "An array whose elements are themselves arrays, used to represent grids and tables."),
        ("Record", "A data structure holding several related values of different data types, each in a named field."),
        ("Concatenation", "Joining two strings together end to end."),
        ("SUBSTRING", "An operation returning the characters of a string between two given positions."),
        ("Casting", "Converting a value from one data type to another, such as a string to an integer."),
        ("End of file", "The marker showing that there is no more data to read from a file."),
        ("Pseudo-random", "Generated by an algorithm so that it appears random, but is fully determined by the starting seed."),
    ],
    grade="""
The strongest answers here are the ones that keep types straight.

**They say where data came from.** Anything read from a file or from the user is a string until it is cast. Saying so explicitly is what turns a partially correct answer into a full one.

**They count indexes carefully.** Off by one errors are the single most common fault in exam code, and an answer that writes `LEN(x) - 1` where it belongs shows the examiner that you understand indexing rather than remembering a pattern.

**They choose the structure and justify it.** "An array of records, because each student has several different pieces of information but every student has the same fields" is a complete answer. "An array" is half of one.
""",
    mistakes=[
        "Looping FOR i to LEN(array) rather than LEN(array) - 1, which reads past the end.",
        "Using an array for values of different types. That is a record's job.",
        "Forgetting that data read from a file is a string and must be converted before arithmetic.",
        "Forgetting to close a file, which can leave buffered output unwritten.",
        "Saying computers generate random numbers. They generate pseudo-random numbers from a seed.",
    ],
    quiz=[
        Q("An array called names holds 6 items. What is the index of the last one?", ["5", "6", "7", "0"], 0,
          "Indexing starts at zero, so six items occupy positions 0 to 5. The last index is always the length minus one."),
        Q("Which data structure would you use to store a student's name, year group and average mark together?", ["A record", "An array", "A two dimensional array", "A constant"], 0,
          "Those three values have different data types but describe one thing, which is exactly what a record is for. An array requires every item to be the same type."),
        Q("What does SUBSTRING(2, 4, 'Computing') return?", ["'mpu'", "'omp'", "'mput'", "'mp'"], 0,
          "Indexing starts at zero, so C is 0, o is 1, m is 2, p is 3 and u is 4. Characters 2 to 4 inclusive are m, p and u."),
        Q("What is LEN('Computer Science')?", ["16", "15", "14", "17"], 0,
          "LEN counts every character including the space, so Computer is 8, the space is 1 and Science is 7, giving 16."),
        Q("Why must a number read from a text file be converted before it is used in a calculation?", ["Everything read from a text file arrives as a string", "Files store numbers in hexadecimal", "Text files cannot contain numbers", "The file must be closed first"], 0,
          "A text file holds characters, so a line read from it is a string. It must be cast to an integer or real before arithmetic will behave correctly."),
        Q("Why are computer generated random numbers described as pseudo-random?", ["They are produced by an algorithm from a seed, so the same seed always gives the same sequence", "They are not really numbers", "They only work for small ranges", "They repeat after exactly one hundred values"], 0,
          "A deterministic algorithm cannot produce true randomness. Given the same starting seed it produces the same sequence, which is why the numbers are called pseudo-random."),
        Q("In a two dimensional array board, what does board[2][0] refer to?", ["The first item of the third row", "The third item of the first row", "The second row and the first column of a one based grid", "An error, since two indexes are not allowed"], 0,
          "The first index selects the row and the second the position within it. Counting from zero, index 2 is the third row and index 0 is its first item."),
        Q("What is the value of CHAR_TO_CODE('B') if 'A' is 65?", ["66", "65", "97", "42"], 0,
          "The letters are given consecutive codes in the character set, so B is one more than A, which is 66."),
        Q("Why should a file be closed after a program has finished writing to it?", ["Output may be buffered, so data can be lost if the file is not closed", "Closing a file deletes it from memory", "The file cannot be read by another program until it is closed forever", "Closing a file converts it to binary"], 0,
          "Writes are often held in a buffer and only committed when the file is closed, so failing to close it can leave data unwritten."),
        Q("A program needs the last digit of an integer n. Which expression gives it?", ["n MOD 10", "n DIV 10", "LEN(n)", "n MOD 2"], 0,
          "Dividing by ten and taking the remainder leaves exactly the units digit, so n MOD 10 gives the last digit."),
    ],
    exam=[
        EQ("State one difference between an array and a record.", 2, [
            MP("An array stores values that are all of the same data type", ["same type", "same data type", "identical type", "one type"]),
            MP("A record stores values of different data types in named fields", ["different types", "various types", "mixed", "fields", "named fields"]),
        ], "An array holds many values that must all be of the same data type, accessed by an index. A record holds several values of different data types that belong to one thing, each stored in its own named field.", command="State"),
        EQ("A program stores 30 test scores in an array called scores. Write an algorithm that outputs the highest score.", 4, [
            MP("Sets a starting highest value, for example the first element", ["highest ← scores[0]", "first element", "sets highest", "initialise", "start"]),
            MP("Loops through the array using the correct index range", ["for", "loop", "0 to", "len", "each"]),
            MP("Compares each element with the current highest", ["if", "greater than", ">", "compare"]),
            MP("Updates the highest and outputs it at the end", ["highest ←", "output", "print", "after the loop"]),
        ], "Set highest to scores[0], then loop i from 1 to LEN(scores) minus 1. Inside the loop, if scores[i] is greater than highest then set highest to scores[i]. After the loop finishes, output highest. Starting from the first element rather than from zero matters, because a list of negative scores would otherwise report zero as the highest.", command="Write"),
        EQ("Explain why a program that reads a number from a text file must cast it before performing a calculation.", 3, [
            MP("A text file stores characters, so the value read is a string", ["string", "characters", "text", "not a number"]),
            MP("Arithmetic operators do not behave as intended on strings", ["arithmetic", "cannot add", "joins", "concatenates", "error", "unexpected"]),
            MP("Casting converts the string into an integer or real so the calculation works", ["cast", "convert", "STRING_TO_INT", "changes type", "becomes a number"]),
        ], "A text file holds characters, so a line read from it is a string even when every character in it is a digit. Applying an arithmetic operator to a string either causes an error or joins values together rather than adding them, so the result is wrong. Casting the string to an integer or a real converts it into a numeric value, after which the calculation behaves as intended.", command="Explain"),
        EQ("A programmer needs to store the names, ages and email addresses of 200 club members. Describe a suitable data structure and justify your choice.", 4, [
            MP("Uses records to hold the three fields for one member", ["record", "fields", "structure", "name age email together"]),
            MP("Justifies the record because the fields have different data types", ["different types", "string and integer", "mixed types", "not all the same"]),
            MP("Uses an array to hold the 200 records", ["array", "list", "200", "collection"]),
            MP("Justifies the array because every member has the same set of fields and a loop can process them all", ["same fields", "loop", "iterate", "process all", "one identifier"]),
        ], "The right structure is an array of records. Each member is one record with three named fields: name as a string, age as an integer and email as a string. A record is needed rather than an array for the individual member because the three values have different data types and belong together as a description of one person. The two hundred records are then held in an array, because every member has exactly the same set of fields, which means one loop can process all of them and the program does not have to change if the club gains or loses members.", command="Describe"),
        EQ("Explain why pseudo-random numbers are unsuitable for generating encryption keys.", 3, [
            MP("They are produced by an algorithm from a seed value", ["algorithm", "seed", "formula", "deterministic"]),
            MP("The same seed always produces the same sequence, so the numbers are predictable", ["same seed", "predictable", "repeat", "same sequence", "can be worked out"]),
            MP("An attacker who works out or guesses the seed can reproduce the keys", ["attacker", "reproduce", "guess the seed", "recreate", "break", "predict the key"]),
        ], "Pseudo-random numbers come from a deterministic algorithm applied to a starting seed, so they only appear random. Give the algorithm the same seed and it produces exactly the same sequence every time. If an attacker can work out or guess the seed, perhaps because it was taken from the system clock, they can regenerate the whole sequence and therefore every key the program produced. Cryptographic use requires a source of genuine unpredictability rather than a repeatable formula.", command="Explain"),
    ],
)


# ================================== 3.2.10 to 3.2.11 subroutines and structure

T_SUBROUTINES = Topic(
    slug="subroutines-and-structured-programming",
    title="Subroutines and Structured Programming",
    spec="3.2.10 to 3.2.11",
    icon="i-layers",
    minutes=26,
    blurb="Procedures and functions, parameters and return values, local and global scope, and why breaking a program into named pieces is the difference between code you can maintain and code you cannot.",
    fact="The word 'bug' predates computing, but the most famous one is real. In 1947 a moth was found stuck in a relay of the Harvard Mark II, and the operators taped it into the logbook with the note 'first actual case of bug being found'.",
    sections=[
        Section("Procedures and functions", """
A **subroutine** is a named block of code that can be called from elsewhere in a program. AQA distinguishes two kinds.

A **procedure** carries out a task and does not return a value.

```pseudo
SUBROUTINE greet(name)
    OUTPUT 'Hello ' + name
ENDSUBROUTINE

greet('Amira')
```

A **function** carries out a calculation and **returns** a value, which the calling code then uses.

```pseudo
SUBROUTINE area(width, height)
    RETURN width * height
ENDSUBROUTINE

size ← area(4, 7)
```

The difference is exactly that: a function has a RETURN and its call appears where a value is expected. A procedure is called as a statement on its own.

### Parameters and arguments

A **parameter** is the name in the subroutine definition. An **argument** is the actual value passed in when it is called. In the example above, `width` and `height` are parameters and `4` and `7` are arguments.

Parameters are what make a subroutine reusable. A subroutine that always calculates the area of a four by seven rectangle is useless. One that takes any two numbers can be called anywhere.
"""),
        Section("Scope", """
The **scope** of a variable is the region of the program in which it can be accessed.

A **local** variable is declared inside a subroutine and exists only while that subroutine is running. A **global** variable is declared outside every subroutine and can be accessed anywhere.

```pseudo
SUBROUTINE tally()
    count ← 0
    count ← count + 1
    RETURN count
ENDSUBROUTINE
```

`count` here is local. It is created when the subroutine starts and destroyed when it ends, so the subroutine returns 1 every single time it is called.

### Why local variables are the better default

- **No accidental interference.** Two subroutines can each have a variable called `i` without either affecting the other.
- **Memory is reclaimed.** A local variable stops using memory as soon as the subroutine ends.
- **The subroutine is self contained.** Everything it needs comes in as a parameter and everything it produces comes back as a return value, so it can be moved, tested and reused without dragging the rest of the program along with it.

!warn Global variables are not simply wrong :: They are the right answer when genuinely many parts of the program need one shared value, such as a running total in a game. What makes them dangerous is that any subroutine can change one, so a bug can be caused from anywhere in the program.
"""),
        Section("Structured programming", """
**Structured programming** means building a program from separate, named, self contained subroutines with clearly defined inputs and outputs, rather than as one long block.

The advantages come up in exams constantly, and they are worth learning as reasons rather than as a list.

**It is easier to write.** Decomposing the problem gives you a set of small tasks, each of which is achievable. Two people can work on different subroutines at the same time without colliding.

**It is easier to test.** A subroutine with defined inputs and one output can be tested on its own with a handful of values. A tangled program can only be tested as a whole, which means a fault could be anywhere.

**It is easier to maintain.** A change to how VAT is calculated means editing one subroutine, not searching a thousand lines. Because the subroutine is self contained, you can be confident the change has not broken something elsewhere.

**Code can be reused.** A validation subroutine written once can be called from every point in the program that needs it, and reused in the next program entirely.

**It is easier to read.** A main program that reads `loadQuestions()`, `askQuestion()`, `updateScore()` explains itself. The same logic written inline does not.

!exam Answer with the reason, not the label :: "It is easier to maintain" is one mark at best. "It is easier to maintain, because a change only has to be made in the one subroutine responsible for that task rather than in every place the code was repeated" is the full answer.
"""),
    ],
    keyterms=[
        ("Subroutine", "A named block of code that can be called from elsewhere in a program."),
        ("Procedure", "A subroutine that performs a task and does not return a value."),
        ("Function", "A subroutine that performs a calculation and returns a value to the code that called it."),
        ("Parameter", "A named value in a subroutine definition that receives an argument when the subroutine is called."),
        ("Argument", "The actual value passed to a subroutine when it is called."),
        ("Return value", "The value a function sends back to the code that called it."),
        ("Scope", "The region of a program in which a variable can be accessed."),
        ("Local variable", "A variable declared inside a subroutine, which exists only while that subroutine runs."),
        ("Global variable", "A variable declared outside all subroutines, accessible anywhere in the program."),
        ("Structured programming", "Building a program from separate, self contained subroutines with defined inputs and outputs."),
    ],
    grade="""
There are two things that separate a full mark answer here.

**Naming the direction of data.** A parameter carries data in. A return value carries data out. An answer that says which is which, and names the actual values in the question, is complete.

**Explaining scope as a consequence rather than a rule.** "Local variables cannot be accessed outside the subroutine" is the rule. "Which means two subroutines can each use a variable called total without one overwriting the other" is the reason it is worth having, and that is what a high mark answer says.
""",
    mistakes=[
        "Calling every subroutine a function. A function returns a value, a procedure does not.",
        "Mixing up parameter and argument. The parameter is in the definition, the argument is the value passed in.",
        "Saying a local variable is 'deleted' when the program ends. It ends when the subroutine ends, not the program.",
        "Listing the advantages of structured programming without giving a reason for any of them.",
        "Assuming global variables are always bad practice. They are appropriate for genuinely shared state and dangerous only because any part of the program can change one.",
    ],
    quiz=[
        Q("What is the difference between a procedure and a function?", ["A function returns a value and a procedure does not", "A function is longer than a procedure", "A procedure can take parameters and a function cannot", "A procedure runs faster"], 0,
          "The defining difference is the return value. A function computes something and hands the result back to the caller. A procedure carries out a task and hands nothing back."),
        Q("In SUBROUTINE area(width, height), what are width and height?", ["Parameters", "Arguments", "Global variables", "Return values"], 0,
          "Names in the definition are parameters. The values supplied when the subroutine is called are the arguments."),
        Q("A variable declared inside a subroutine is described as having what kind of scope?", ["Local", "Global", "Public", "Static"], 0,
          "A variable declared inside a subroutine is local to it, existing only while that subroutine runs and inaccessible from outside."),
        Q("Why can two different subroutines both use a local variable called count?", ["Each exists only within its own subroutine, so they do not interfere", "The compiler renames one of them", "Only one of them actually works", "Local variables are stored in different files"], 0,
          "Local variables are created when the subroutine starts and destroyed when it ends, so the two are separate storage locations that happen to share a name."),
        Q("Which of these is a genuine advantage of structured programming?", ["A fault in one task only needs correcting in the subroutine responsible for it", "Programs written this way always run faster", "It removes the need for testing", "It means variables never need names"], 0,
          "Because each task lives in one subroutine, a change or a correction is made in one place rather than everywhere the logic was repeated."),
        Q("A subroutine returns 1 every time it is called, even though it should count upwards. What is the most likely cause?", ["The counter is a local variable that is re-created each call", "The subroutine is a procedure", "The parameter is missing", "The return statement is in the wrong place"], 0,
          "A local variable is created fresh each time the subroutine runs, so initialising it inside the subroutine resets it on every call."),
        Q("What is passed to a subroutine when it is called?", ["Arguments", "Parameters", "Fields", "Records"], 0,
          "The values supplied at the point of the call are arguments. They are received by the parameters named in the definition."),
        Q("Which statement about global variables is correct?", ["Any part of the program can change one, which makes some bugs hard to trace", "They cannot be used in structured programs", "They use less memory than local variables", "They are destroyed when a subroutine ends"], 0,
          "A global variable is accessible everywhere, so when one holds an unexpected value the cause could be anywhere in the program."),
        Q("Why does using parameters make a subroutine more useful?", ["It can be called with different values rather than working on one fixed case", "It runs faster", "It uses less memory", "It removes the need for a return value"], 0,
          "Parameters generalise a subroutine. Without them it can only ever do the one specific job it was written for."),
        Q("A program calls validate(age) and stores the result. What must validate be?", ["A function, because its result is stored", "A procedure, because it takes a parameter", "A global variable", "A record"], 0,
          "Storing the result of a call means the call produced a value, which means the subroutine returned one, which makes it a function."),
    ],
    exam=[
        EQ("State one difference between a parameter and an argument.", 2, [
            MP("A parameter is the name given in the subroutine definition", ["definition", "parameter is the name", "declared", "in the subroutine header"]),
            MP("An argument is the actual value passed in when the subroutine is called", ["value passed", "actual value", "when called", "supplied"]),
        ], "A parameter is the named variable listed in the subroutine's definition, which receives a value when the subroutine runs. An argument is the actual value supplied at the point where the subroutine is called.", command="State"),
        EQ("Explain why it is usually better to use local variables than global variables inside a subroutine.", 4, [
            MP("A local variable exists only while the subroutine runs", ["only while", "exists", "created and destroyed", "within the subroutine"]),
            MP("So it cannot be changed by any other part of the program", ["cannot be changed elsewhere", "no interference", "protected", "other subroutines"]),
            MP("Two subroutines can use the same variable name without conflict", ["same name", "no clash", "independent", "does not overwrite"]),
            MP("The subroutine becomes self contained, so it is easier to test and reuse", ["self contained", "reuse", "test on its own", "portable", "independent"]),
        ], "A local variable is created when the subroutine starts and destroyed when it finishes, so it cannot be read or altered by any other part of the program. That removes a whole class of bug in which one section of a program changes a value another section was relying on, and it means two subroutines can each use a variable called total without either affecting the other. It also makes the subroutine self contained: everything it needs arrives as a parameter and everything it produces leaves as a return value, so it can be tested on its own and reused in another program without dragging the rest of the code along with it.", command="Explain"),
        EQ("Describe two advantages of breaking a long program into subroutines.", 4, [
            MP("Code written once can be called from several places, so there is less repetition", ["reuse", "called many times", "less repetition", "written once", "duplicate"]),
            MP("A change or correction only has to be made in one place", ["one place", "one subroutine", "easier to maintain", "fix once"]),
            MP("Each subroutine can be tested independently", ["tested separately", "test each", "on its own", "isolate"]),
            MP("The program is easier to read and several people can work on it at once", ["easier to read", "understand", "team", "at the same time", "clearer"]),
        ], "The first advantage is maintenance. A task written once as a subroutine is called wherever it is needed, so there is no repeated code, and when that task has to change it is corrected in exactly one place rather than in every copy. The second is testing and readability. Each subroutine has one clear job and defined inputs and outputs, so it can be tested on its own with a small set of values before it is trusted, and the main program reads as a list of named steps, which makes it far easier for another programmer, or for you in six months, to follow.", command="Describe"),
        EQ("A subroutine is written to count how many times it has been called, but it returns 1 every time. Explain the cause and how it could be corrected.", 4, [
            MP("The counter is declared as a local variable inside the subroutine", ["local", "inside", "declared in the subroutine"]),
            MP("It is therefore created again each time the subroutine is called", ["re-created", "reset", "each call", "starts again", "new each time"]),
            MP("The value from the previous call is lost when the subroutine ends", ["lost", "destroyed", "does not persist", "forgotten"]),
            MP("Correct it by making the counter global, or by passing the count in and returning it", ["global", "pass it in", "parameter and return", "outside the subroutine", "persist"]),
        ], "The counter has been declared and initialised inside the subroutine, which makes it local. A local variable is created when the subroutine starts and destroyed when it ends, so the value reached on one call is gone by the next and the counter is reset to zero every time, which is why it always returns one. There are two reasonable corrections. Declaring the counter as a global variable outside every subroutine means it persists between calls. Alternatively, and more safely, the current count can be passed in as a parameter and the new count returned, which keeps the subroutine self contained.", command="Explain"),
    ],
)


# ================================================ 3.2.12 robust programming

T_ROBUST = Topic(
    slug="robust-and-secure-programming",
    title="Robust and Secure Programming",
    spec="3.2.12",
    icon="i-shield",
    minutes=24,
    blurb="Validation, authentication, defensive design and testing, plus the three kinds of error and how to find each one, written around the idea that a program must survive users who do the wrong thing.",
    fact="In 1996 the first Ariane 5 rocket destroyed itself 39 seconds after launch. The cause was a 64 bit real number being converted into a 16 bit integer that could not hold it, in code that was not even needed after lift off.",
    sections=[
        Section("Validation and authentication", """
**Validation** checks that data entered is *reasonable*. It cannot check that data is *correct*, and knowing the difference is worth marks.

| Check | What it tests | Example |
| Range | The value falls between two limits | An age between 0 and 120 |
| Presence | Something was actually entered | A name box is not left blank |
| Length | The right number of characters | A password of at least 8 characters |
| Type | The data is of the expected type | A quantity is a whole number |
| Format | The data matches a required pattern | An email contains an at sign |
| Look up | The value is one of a known set | A county chosen from a list |

!warn Validation cannot detect a lie :: A date of birth of 01/01/1990 passes every check you can write, and is wrong if the person was born in 1991. Validation checks plausibility, nothing more. Say that in an exam and you will separate yourself from most candidates.

### Authentication

**Authentication** checks that a user is who they claim to be. Usernames and passwords are the common method, often strengthened by:

- requiring a minimum length and a mixture of character types,
- limiting the number of failed attempts before an account is locked,
- asking for specific characters from a memorable word,
- two factor authentication, which requires something you know and something you have.

Authentication answers "who are you". Validation answers "is that a sensible thing to type". They are different jobs and questions distinguish them.
"""),
        Section("Defensive design and maintainability", """
Defensive design means writing a program that keeps working when things go wrong, rather than one that only works when everything goes right.

**Anticipate misuse.** Assume every input will eventually receive an empty string, a negative number, a word where a number was expected and a value a thousand times larger than you planned for. Handle each of those deliberately.

**Fail helpfully.** A message saying what was wrong and what to do lets the user recover. A crash does not.

**Authenticate before acting.** Check permission before doing anything sensitive, not after.

### Maintainability

Maintainable code is code that another programmer, or you in a year, can safely change.

- **Meaningful identifiers.** `totalPrice` rather than `tp` or `x2`.
- **Comments that explain why, not what.** `count ← count + 1` does not need a comment saying it adds one. It might need one saying why the first record is skipped.
- **Indentation** that reveals structure, so the body of a loop is visibly inside it.
- **Subroutines** so each task lives in one named place.

!exam Comments are examined :: A question asking how a program could be made more maintainable expects specific examples, so name a poor identifier in the code you have been given and say what you would rename it to.
"""),
        Section("Testing and the three kinds of error", """
### Syntax errors

A **syntax error** breaks the rules of the language, such as a missing bracket or a misspelled keyword. The program will not run at all, and the translator reports the error, usually with a line number.

### Logic errors

A **logic error** means the program runs perfectly and produces the wrong answer. Using `+` where you meant `-`, or `<` where you meant `≤`, gives a logic error. Nothing reports it, which is precisely why these are the expensive ones.

### Runtime errors

A **runtime error** happens while the program is executing: dividing by zero, reading past the end of an array, opening a file that does not exist. The program starts and then stops.

### Test data

Every test plan needs three kinds of data, and AQA asks for them by name.

| Type | Meaning | Example for an age between 0 and 120 |
| Normal | Typical data the program should accept | 35 |
| Boundary | Data at the very edge of what is acceptable | 0, 120, and just outside, -1 and 121 |
| Erroneous | Data the program should reject | "cat", an empty entry, 3.5 |

!key Boundary data is where the bugs live :: Almost every off by one error shows up at a boundary and nowhere else. A program tested only with 35 will pass while rejecting every newborn and accepting every age up to 121.

### Iterative and final testing

**Iterative testing** happens during development, module by module, so faults are found while the code is still fresh and small. **Final testing** happens once the program is complete and checks the whole thing against the original requirements. Both are needed: iterative testing finds faults cheaply, final testing proves the program does the job it was asked to do.
"""),
    ],
    keyterms=[
        ("Validation", "An automatic check that data entered is reasonable and of the expected form."),
        ("Authentication", "Checking that a user is who they claim to be, usually with a username and password."),
        ("Range check", "A validation check that a value falls between an upper and a lower limit."),
        ("Presence check", "A validation check that a required value has actually been entered."),
        ("Format check", "A validation check that data matches a required pattern."),
        ("Syntax error", "An error that breaks the rules of the programming language, preventing the program from running."),
        ("Logic error", "An error in which the program runs but produces the wrong result."),
        ("Runtime error", "An error that occurs while the program is executing, causing it to stop."),
        ("Normal test data", "Typical data that the program should accept and process correctly."),
        ("Boundary test data", "Data at the very edge of the acceptable range, on both sides of the limit."),
        ("Erroneous test data", "Data the program should reject, used to check the validation works."),
        ("Iterative testing", "Testing carried out repeatedly during development as each part is written."),
    ],
    grade="""
The strongest answers here understand what each technique can and cannot do.

**They limit validation honestly.** A grade 9 answer says validation confirms data is plausible, and explicitly adds that it cannot confirm data is true. That single sentence appears in mark schemes.

**They choose test data with a reason.** Not "I would test with 0 and 120" but "I would test with 0 and 120 because they are the boundaries, and with -1 and 121 because an off by one error in the comparison would only show up there".

**They tell the three errors apart by symptom.** Will not run at all is syntax. Runs and gives the wrong answer is logic. Starts and then stops is runtime. Answering by symptom rather than by definition shows understanding.
""",
    mistakes=[
        "Saying validation makes sure data is correct. It makes sure data is reasonable.",
        "Confusing validation with verification. Verification checks data was entered accurately, for example by typing it twice.",
        "Giving only one boundary value. A boundary needs testing on both sides of the limit.",
        "Calling a crash a logic error. If the program stops while running it is a runtime error.",
        "Writing comments that restate the code. A useful comment explains why, not what.",
    ],
    quiz=[
        Q("A program will not run and the translator reports a missing bracket. What kind of error is this?", ["Syntax error", "Logic error", "Runtime error", "Validation error"], 0,
          "A missing bracket breaks the rules of the language, so the program cannot be translated at all. That is a syntax error."),
        Q("A program runs but calculates the average by dividing by the wrong number. What kind of error is this?", ["Logic error", "Syntax error", "Runtime error", "Type error"], 0,
          "The program runs perfectly and produces an answer, but the answer is wrong. That is a logic error, and nothing reports it for you."),
        Q("Which validation check would stop a user leaving a name box empty?", ["Presence check", "Range check", "Format check", "Length check"], 0,
          "A presence check confirms that something has actually been entered in a required field."),
        Q("For an input that must be between 1 and 10, which set is boundary test data?", ["0, 1, 10, 11", "5, 6, 7", "cat, empty, 3.5", "1, 2, 3"], 0,
          "Boundary data sits at the very edge of the acceptable range, on both sides of each limit, which is where off by one errors show up."),
        Q("What can validation never do?", ["Confirm that the data entered is truthful", "Check a value is within a range", "Check a required field is not empty", "Check data is of the right type"], 0,
          "Validation checks plausibility. A false date of birth in a sensible format passes every check that can be written."),
        Q("What is the purpose of authentication?", ["To check that a user is who they claim to be", "To check that data entered is sensible", "To make a program run faster", "To find syntax errors"], 0,
          "Authentication establishes identity. Validation is about the data itself, which is a different job."),
        Q("A program stops with an error when it tries to open a file that has been deleted. What kind of error is this?", ["Runtime error", "Syntax error", "Logic error", "Design error"], 0,
          "The program translated and started successfully, then failed while executing, which makes it a runtime error."),
        Q("Which of these most improves the maintainability of a program?", ["Using meaningful identifier names", "Making the program shorter by removing indentation", "Using single letter variable names to save typing", "Removing all comments"], 0,
          "An identifier that says what the value is makes the code readable without needing to trace it, which is the main thing maintainability depends on."),
        Q("Why is iterative testing carried out during development rather than only at the end?", ["Faults are found while the code is small and recent, so they are cheaper to fix", "It removes the need for final testing", "It makes the program run faster", "It is required by law"], 0,
          "Testing each part as it is written means a fault is found in a few lines you wrote minutes ago, rather than somewhere in a finished program."),
        Q("What is erroneous test data used to check?", ["That the program correctly rejects data it should not accept", "That the program handles typical values", "That the program is fast enough", "That the boundaries are correct"], 0,
          "Erroneous data is deliberately invalid. Testing with it proves that the validation actually rejects what it is supposed to reject."),
    ],
    exam=[
        EQ("State what is meant by validation.", 1, [
            MP("An automatic check that data entered is sensible or reasonable", ["sensible", "reasonable", "plausible", "acceptable", "of the expected form"]),
        ], "Validation is an automatic check carried out by a program to make sure that data entered is reasonable and of the form expected.", command="State"),
        EQ("A program asks for a percentage mark between 0 and 100. Give one item of normal test data, one item of boundary test data and one item of erroneous test data.", 3, [
            MP("Normal data is a typical value inside the range, such as 55", ["55", "50", "72", "inside", "typical", "normal value"]),
            MP("Boundary data is at the edge of the range, such as 0, 100, -1 or 101", ["0", "100", "101", "-1", "edge", "boundary"]),
            MP("Erroneous data is something that should be rejected, such as a word or a blank entry", ["cat", "word", "letters", "blank", "empty", "text", "abc"]),
        ], "Normal test data would be 55, a value comfortably inside the acceptable range that the program should accept. Boundary test data would be 0 and 100, the two limits, together with -1 and 101 just outside them, since an incorrect comparison would only show up there. Erroneous test data would be a word such as cat, or a blank entry, which the program should reject rather than process.", command="Give"),
        EQ("Explain the difference between a logic error and a syntax error.", 4, [
            MP("A syntax error breaks the rules of the programming language", ["rules", "grammar", "language", "misspelled", "missing bracket"]),
            MP("A program containing a syntax error will not run, and the translator reports it", ["will not run", "does not run", "reported", "translator", "compiler", "cannot translate"]),
            MP("A logic error means the program runs but produces the wrong result", ["runs", "wrong result", "incorrect answer", "unexpected output"]),
            MP("Nothing reports a logic error, so it must be found by testing or by tracing the program", ["not reported", "no error message", "testing", "trace", "harder to find"]),
        ], "A syntax error breaks the rules of the programming language, for example a missing bracket or a misspelled keyword. The translator cannot make sense of the line, so the program will not run at all and the error is reported, usually with a line number, which makes it comparatively easy to fix. A logic error is different in kind. The code is perfectly valid, so the program translates and runs, but the instructions do not do what the programmer intended, so the output is wrong. Nothing reports it, which means it can only be found by testing with data whose correct answer is already known, or by tracing the program by hand.", command="Explain"),
        EQ("A shopping website validates the postcode a customer enters. Explain why validation alone cannot guarantee the parcel will arrive.", 3, [
            MP("Validation only checks that the data is of a reasonable form", ["form", "format", "reasonable", "plausible", "pattern"]),
            MP("A postcode can be correctly formatted but not be the customer's actual postcode", ["wrong postcode", "someone else", "not theirs", "valid but wrong", "typed the wrong one"]),
            MP("Validation cannot check truthfulness, only plausibility", ["cannot check truth", "not correct", "only plausible", "does not know"]),
        ], "Validation checks the shape of the data, so a format check can confirm that the entry looks like a postcode and a look up check can confirm that it is a postcode that exists. Neither of those establishes that it is the right postcode for this customer. Somebody can enter a real, correctly formatted postcode belonging to a different address, either by mistake or deliberately, and every check will pass. Validation tests whether data is plausible, and no automatic check on the data alone can test whether it is true.", command="Explain"),
        EQ("Describe two ways in which a programmer can make a program easier to maintain.", 4, [
            MP("Use meaningful identifier names that say what the value holds", ["meaningful names", "identifiers", "sensible names", "descriptive", "variable names"]),
            MP("So another programmer can understand the code without tracing it", ["understand", "read", "without tracing", "clearer", "obvious"]),
            MP("Use comments to explain why the code does what it does", ["comments", "annotate", "explain", "notes"]),
            MP("Use subroutines and indentation so the structure is visible and each task lives in one place", ["subroutines", "indentation", "structure", "one place", "modules", "functions"]),
        ], "The first is to use meaningful identifiers. A variable called totalPrice tells the next reader what it holds, whereas one called tp or x2 has to be traced through the whole program before it can be safely changed. The second is to use subroutines with sensible indentation, so that each task lives in one named place and the structure of the program is visible on the page. Together those mean that a change to how something is calculated is made once, in an obviously named place, with far less risk of breaking something elsewhere. Comments explaining why an unusual decision was taken support both.", command="Describe"),
    ],
)


# =========================================== 3.2.13 classification of languages

T_LANGUAGES = Topic(
    slug="classification-of-programming-languages",
    title="Classification of Programming Languages",
    spec="3.2.13",
    icon="i-list",
    minutes=22,
    blurb="High and low level languages, machine code and assembly language, and the three translators, with a clear account of why anyone would still write low level code today.",
    fact="The first assembler was written in 1947 by Kathleen Booth, who also designed the assembly language it translated. Every low level language since is a descendant of that idea: give the numbers names a person can read.",
    sections=[
        Section("High and low level languages", """
A **high level language** such as Python, C# or VB.NET is written in a form close to human language, one statement of which usually becomes many machine instructions.

A **low level language** is close to the hardware. There are two kinds: **machine code**, which is the binary the processor actually executes, and **assembly language**, which replaces those binary opcodes with short mnemonics such as ADD, LDA and STA.

| | High level | Low level |
| Readability | Close to English, easy to follow | Difficult, one line does very little |
| Portability | Runs on any machine with a translator | Written for one processor family |
| Development speed | Fast, one statement does a lot | Slow, everything is manual |
| Memory management | Handled for you | The programmer's job |
| Control of hardware | Limited and indirect | Complete and direct |
| Efficiency | Good, but the translator decides | Can be optimised precisely |

!key One high level statement is many machine instructions :: That single fact explains most of the table. It is why high level code is quicker to write and shorter to read, and why the programmer has less direct control over what the processor actually does.

### Why low level languages are still used

Not for ordinary applications. They are used where the extra control is worth the cost:

- **Embedded systems** with very little memory, where every byte matters,
- **Device drivers**, which must talk to specific hardware registers directly,
- **Small, critical routines** inside a larger program, where the last few per cent of speed matters,
- **Malware analysis and security work**, where you only have the machine code.
"""),
        Section("Translators", """
A processor executes machine code and nothing else, so anything written in another language must be translated. AQA names three translators.

### Assembler

An **assembler** translates assembly language into machine code. The relationship is close to one to one: each mnemonic becomes one machine instruction. That is why assembly is a low level language rather than a high level one.

### Compiler

A **compiler** translates a whole high level program into machine code in one go, producing an executable file.

- Translation happens once, so the finished program runs quickly.
- The program can be distributed without the source code, which protects the developer's work.
- No translator is needed on the machine that runs it.
- All errors are reported together at the end of compilation, which can be daunting.
- The executable only runs on the type of machine it was compiled for.

### Interpreter

An **interpreter** translates and executes a high level program one statement at a time, every time it is run.

- Errors are reported as soon as the offending line is reached, which makes debugging much easier.
- The same source runs on any machine that has the right interpreter.
- Execution is slower, because translation happens every run and every time round a loop.
- The source code has to be given to whoever runs the program.

!exam The comparison question :: The most common question is "state one advantage of an interpreter over a compiler". The answer is about development, not about running: errors are reported line by line as they are met, which makes finding a fault far quicker.
"""),
    ],
    keyterms=[
        ("High level language", "A programming language written close to human language, where one statement becomes many machine instructions."),
        ("Low level language", "A language close to the hardware, either machine code or assembly language."),
        ("Machine code", "The binary instructions a processor executes directly."),
        ("Assembly language", "A low level language using short mnemonics in place of binary opcodes."),
        ("Assembler", "A translator that converts assembly language into machine code."),
        ("Compiler", "A translator that converts a whole high level program into machine code before it is run."),
        ("Interpreter", "A translator that converts and executes a high level program one statement at a time."),
        ("Portability", "The ability of a program to run on different types of computer."),
    ],
    grade="""
Two things lift an answer here.

**Reasoning from the one to one relationship.** Assembly maps almost one instruction to one machine instruction, and a high level statement maps to many. Almost every advantage and disadvantage in the topic follows from that, and saying so is worth more than reciting a list.

**Distinguishing development from execution.** Interpreters win during development because errors surface immediately. Compilers win at execution because translation has already happened. Answers that keep those two situations apart get full marks; answers that say "interpreters are slower" without saying slower at what do not.
""",
    mistakes=[
        "Saying a compiler is faster than an interpreter without saying at what. Compiling itself is slow, the resulting program is fast.",
        "Describing assembly language as machine code. Assembly uses mnemonics and still needs assembling.",
        "Saying an interpreter produces an executable file. It does not: it executes as it translates.",
        "Claiming low level languages are obsolete. They are used wherever direct hardware control or minimal memory use is essential.",
        "Forgetting that compiled code only runs on the platform it was compiled for.",
    ],
    quiz=[
        Q("What does an assembler translate?", ["Assembly language into machine code", "High level code into machine code", "Machine code into assembly language", "One high level language into another"], 0,
          "An assembler converts assembly language mnemonics into the machine code the processor executes, roughly one instruction at a time."),
        Q("Which is an advantage of an interpreter over a compiler?", ["Errors are reported as soon as the line containing them is reached", "The program runs faster", "The source code can be kept private", "No translator is needed on the target machine"], 0,
          "An interpreter stops at the first problem line and reports it, which makes finding a fault far quicker during development."),
        Q("Why is a compiled program usually faster to run than an interpreted one?", ["Translation has already been done, so the machine code runs directly", "Compilers optimise the algorithm for you", "Compiled programs use less memory in every case", "Interpreters run on slower hardware"], 0,
          "A compiled program is already machine code, so nothing has to be translated while it runs. An interpreter translates every line each time it is executed, including every pass round a loop."),
        Q("Which of these is a reason to write part of a program in a low level language?", ["Direct control of specific hardware is needed", "The code needs to be portable", "The program must be written quickly", "The programmer wants automatic memory management"], 0,
          "Low level code is chosen when direct hardware control or extremely tight memory use matters more than speed of development and portability."),
        Q("What is machine code?", ["The binary instructions a processor executes directly", "A high level language with short keywords", "The output of an interpreter", "Another name for assembly language"], 0,
          "Machine code is the binary the processor actually executes. Assembly language is a readable representation of it and still needs assembling."),
        Q("Why is a high level program more portable than a low level one?", ["It can be translated for any processor that has a suitable translator", "It uses less memory", "It is shorter", "Portability depends only on the operating system"], 0,
          "High level source is independent of any particular processor. A low level program is written for one instruction set and will not run on another."),
        Q("A compiled program is distributed without its source code. Why is this an advantage for the developer?", ["The developer's work cannot be read or copied directly", "The program runs on more platforms", "It removes the need for testing", "Errors are reported line by line"], 0,
          "Distributing only the executable means the original instructions are not handed over, which protects the developer's intellectual property."),
        Q("Which statement about one line of high level code is correct?", ["It usually translates into many machine code instructions", "It always translates into exactly one machine code instruction", "It cannot be translated at all", "It runs directly on the processor"], 0,
          "The one to many relationship is what makes a language high level, and it is the reason high level code is shorter and quicker to write."),
        Q("Where would an assembly language most likely be used today?", ["In a device driver that must access hardware registers directly", "In a website's front end", "In a school database", "In a word processor's spell checker"], 0,
          "Device drivers need precise, direct access to particular hardware, which is exactly what a low level language provides and a high level one hides."),
        Q("What happens to errors when a program is compiled?", ["They are all reported together at the end of compilation", "They are reported one at a time as each line runs", "They are ignored until the program is run", "They are corrected automatically"], 0,
          "A compiler translates the whole program before producing an executable, so it reports the errors it found as a list once compilation finishes."),
    ],
    exam=[
        EQ("State one difference between a high level language and a low level language.", 2, [
            MP("A high level language is close to human language and easier to read", ["human", "english", "readable", "easier", "close to"]),
            MP("A low level language is close to the hardware, and one instruction does very little", ["hardware", "machine", "processor", "one instruction", "does less", "specific"]),
        ], "A high level language is written in a form close to human language, so it is easier to read and one statement performs a substantial amount of work. A low level language is close to the hardware, so each instruction does very little and the code is written for one particular processor.", command="State"),
        EQ("Explain two advantages of using a compiler rather than an interpreter to translate a finished program.", 4, [
            MP("Translation happens once before the program runs", ["once", "before running", "in advance", "whole program"]),
            MP("So the compiled program executes faster than an interpreted one", ["faster", "quicker", "no translation while running", "executes directly"]),
            MP("The program can be distributed as an executable without the source code", ["executable", "without source", "source code hidden", "protects"]),
            MP("No translator is needed on the machine that runs the program", ["no interpreter needed", "does not need a translator", "runs on its own", "standalone"]),
        ], "The first advantage is speed of execution. A compiler translates the whole program into machine code once, before it is ever run, so at run time the processor executes machine code directly with no translation happening at all. An interpreter has to translate each line every time it is reached, including every pass round a loop, which is considerably slower. The second advantage is distribution. The compiled executable can be given to users without the source code, which protects the developer's work and means the user does not need a translator installed on their own machine.", command="Explain"),
        EQ("A programmer is developing and testing a new program. Explain why they might prefer an interpreter during this stage.", 3, [
            MP("An interpreter translates and runs one statement at a time", ["line by line", "one statement", "as it goes", "statement at a time"]),
            MP("It stops and reports an error as soon as the line containing it is reached", ["stops", "reports immediately", "as soon as", "straight away", "at that line"]),
            MP("So the fault is easy to locate and the program can be re-run quickly after a change", ["easy to find", "locate", "quick", "re-run", "no recompiling", "faster to test"]),
        ], "An interpreter translates and executes one statement at a time, so when it meets a line it cannot process it stops there and reports the problem. That tells the programmer exactly where the fault is, rather than presenting a list of errors after a full compilation. It also means a small change can be tested immediately by running the program again, with no compilation step in between, which makes the write, test, correct cycle much faster while the program is still being developed.", command="Explain"),
        EQ("A company is writing software to control a washing machine, which has a very small amount of memory. Discuss whether they should use a high level or a low level language.", 6, [
            MP("A low level language gives direct control over the hardware", ["direct control", "hardware", "registers", "precise"]),
            MP("Low level code can be made very small and memory efficient", ["small", "memory", "efficient", "compact", "few bytes"]),
            MP("Low level code is slow to write and hard to read or maintain", ["slow to write", "hard to read", "difficult", "maintain", "time consuming"]),
            MP("A high level language is faster to develop in and easier to maintain", ["faster to develop", "quicker", "easier to maintain", "readable"]),
            MP("But a high level program is generally larger and gives less direct hardware control", ["larger", "more memory", "less control", "indirect"]),
            MP("Reaches a justified conclusion for this specific situation", ["therefore", "conclusion", "recommend", "should use", "because the memory"]),
        ], "A low level language has two real advantages here. It gives direct control over the specific hardware in the machine, which matters when the software must operate motors, valves and sensors precisely, and it allows the finished code to be made extremely small, which matters when the memory available is measured in kilobytes. The cost is development. Low level code takes far longer to write, is much harder to read, and is tied to one processor, so moving to a different controller later would mean rewriting rather than recompiling. A high level language reverses all of that: development is quick, the code is readable and maintainable, and it can be recompiled for different hardware, but the compiled program is generally larger and the programmer has less direct control over what the processor does. For a washing machine controller, where memory is severely limited, the hardware is fixed and the program is small and unlikely to change often, the low level route is defensible. In practice most manufacturers take a middle path: write the bulk of the program in a high level language such as C so it stays maintainable, and drop into assembly only for the few routines that must be tightly optimised or must touch the hardware directly.", command="Discuss"),
    ],
)


# ============================================== 3.3.1 to 3.3.2 number bases

T_NUMBASES = Topic(
    slug="number-bases-and-units",
    title="Number Bases and Units of Information",
    spec="3.3.1 to 3.3.2",
    icon="i-binary",
    minutes=28,
    blurb="Why computers use binary at all, how to convert between denary, binary and hexadecimal in both directions, and the units of information using AQA's decimal convention.",
    fact="AQA is one of the boards that uses 1000 bytes to a kilobyte rather than 1024. That is not a simplification: it matches the international standard, in which 1024 bytes is properly a kibibyte.",
    sections=[
        Section("Why binary", """
Computers use **binary**, base 2, because the components they are built from have two reliable states. A transistor is either conducting or it is not. A voltage is either above the threshold or below it. A region of a disc is magnetised one way or the other.

Two states can be told apart even when the signal is noisy. Ten states would need nine thresholds, and a small amount of interference would push a value across one of them. Every extra state makes the electronics more expensive and less reliable, and binary is the point at which reliability is maximised.

!key The exam sentence :: Computers use binary because their components have two easily distinguishable states, which makes storing and transmitting data reliable even when the signal degrades.

### Base 2, base 10 and base 16

A **number base** is how many different digits a system uses.

- **Denary**, base 10, uses the digits 0 to 9. Place values are 1, 10, 100, 1000.
- **Binary**, base 2, uses 0 and 1. Place values are 1, 2, 4, 8, 16, 32, 64, 128.
- **Hexadecimal**, base 16, uses 0 to 9 then A to F for ten to fifteen. Place values are 1, 16, 256.
"""),
        Section("Converting between the bases", """
### Binary to denary

Write the place values above the bits and add up every column holding a 1.

```text
128  64  32  16   8   4   2   1
  1   0   1   1   0   1   0   0
128     + 32 + 16     +  4        = 180
```

### Denary to binary

Work from the left. Take the largest place value that fits, write a 1, subtract it, and carry on.

180 minus 128 leaves 52, so the 128 column is 1. 64 does not fit into 52, so 0. 52 minus 32 leaves 20, so 1. 20 minus 16 leaves 4, so 1. 8 does not fit, so 0. 4 minus 4 leaves 0, so 1. Then 0 and 0. The answer is 10110100.

### Binary to hexadecimal

Split into groups of four bits from the right and convert each group on its own.

`10110100` becomes `1011` and `0100`. `1011` is 11, which is B. `0100` is 4. So the answer is **B4**.

### Hexadecimal to binary

Reverse it. Each hex digit becomes exactly four bits. `2F` becomes `0010` and `1111`, so `00101111`.

### Hexadecimal to denary and back

`B4` is 11 times 16, plus 4, which is 180. Going the other way, 180 divided by 16 is 11 remainder 4, so the digits are B and 4.

!key Always go through binary :: Denary to hex is denary to binary to hex. Hex to denary is hex to binary to denary. That way you only ever need two conversions rather than six.

### Why hexadecimal is used

Sixteen is two to the power of four, so one hexadecimal digit stands for exactly four bits and one byte is always two hex digits. A value written in hex takes a quarter of the characters, which makes memory addresses, colour codes and MAC addresses far easier for people to read, write and compare without mistakes.
"""),
        Section("Units of information", """
A **bit** is a single binary digit, a 0 or a 1. A **nibble** is 4 bits. A **byte** is 8 bits.

| Unit | Size |
| kilobyte (kB) | 1000 bytes |
| megabyte (MB) | 1000 kilobytes |
| gigabyte (GB) | 1000 megabytes |
| terabyte (TB) | 1000 gigabytes |

!warn AQA uses 1000, not 1024 :: This is a genuine board difference and it changes your answers. Divide by 1000 at every step, and if you use 1024 you will not match the mark scheme.

### Calculating a file size

Every file size question follows the same three steps.

1. Work out the total number of **bits** using the right formula.
2. Divide by 8 to get **bytes**.
3. Divide by 1000 for each unit you go up.

The formulas themselves come in the images, sound and compression topics, but the conversion at the end is always the same, and it is where most marks are lost.
"""),
    ],
    keyterms=[
        ("Bit", "A single binary digit, either 0 or 1."),
        ("Nibble", "Four bits, which is one hexadecimal digit."),
        ("Byte", "Eight bits."),
        ("Binary", "Base 2, using only the digits 0 and 1."),
        ("Denary", "Base 10, the everyday number system using the digits 0 to 9."),
        ("Hexadecimal", "Base 16, using 0 to 9 and then A to F."),
        ("Place value", "The value a digit represents because of its position in a number."),
        ("Kilobyte", "One thousand bytes in the convention AQA uses."),
    ],
    grade="""
The marks here are almost entirely method marks, and the students who lose them are the ones working in their heads.

**Write the place values down every time.** 128, 64, 32, 16, 8, 4, 2, 1 above the columns. It takes five seconds and it removes almost every conversion error.

**Show the subtraction.** In denary to binary, writing 180 minus 128 equals 52 earns method credit even if a later column goes wrong.

**Check the other way.** A conversion takes ten seconds to verify by converting back, and a wrong answer you caught costs nothing.

**Say which convention you used.** If a file size question is ambiguous, write "using 1 kB as 1000 bytes" beside your working. AQA's mark schemes expect 1000, and stating it protects you either way.
""",
    mistakes=[
        "Using 1024 rather than 1000 when converting units for AQA.",
        "Forgetting to divide by 8 when converting bits to bytes.",
        "Reading binary from the wrong end. The leftmost bit has the largest place value.",
        "Writing hex digits above F. Hexadecimal stops at F, which is fifteen.",
        "Splitting binary into groups of four from the left rather than from the right, which puts every digit in the wrong column.",
    ],
    quiz=[
        Q("Convert 10011010 into denary.", ["154", "156", "146", "158"], 0,
          "The place values holding a 1 are 128, 16, 8 and 2. Adding those gives 154."),
        Q("Convert 200 into 8 bit binary.", ["11001000", "11000100", "10011000", "11010000"], 0,
          "200 minus 128 is 72, minus 64 is 8, and 8 fits the 8 column exactly, so the ones are in the 128, 64 and 8 columns, giving 11001000."),
        Q("Convert 11101011 into hexadecimal.", ["EB", "BE", "E11", "D11"], 0,
          "Split into 1110 and 1011. 1110 is 14, which is E, and 1011 is 11, which is B, giving EB."),
        Q("Convert hexadecimal 3C into denary.", ["60", "48", "62", "56"], 0,
          "3 times 16 is 48, plus C which is 12, gives 60."),
        Q("How many bits are there in a nibble?", ["4", "8", "16", "2"], 0,
          "A nibble is four bits, which is exactly what one hexadecimal digit represents."),
        Q("Using AQA's convention, how many bytes are in 3 kilobytes?", ["3000", "3072", "24000", "1024"], 0,
          "AQA takes a kilobyte as 1000 bytes, so three kilobytes is 3000 bytes. The value 3072 uses the 1024 convention, which AQA does not use."),
        Q("Why do computers use binary rather than denary?", ["Their components have two easily distinguishable states, which is reliable", "Binary numbers are shorter than denary ones", "Binary uses less electricity than any other base", "Denary cannot represent negative numbers"], 0,
          "Two states can be told apart even when a signal is degraded, which makes storage and transmission reliable. Ten states would need nine thresholds and would be far more fragile."),
        Q("Why is hexadecimal used to write memory addresses?", ["One hex digit represents exactly four bits, so values are shorter and easier to read", "Hexadecimal is what the processor actually stores", "Hexadecimal uses less memory than binary", "Memory addresses cannot be written in binary"], 0,
          "Because sixteen is two to the fourth, each hex digit maps to exactly four bits. The value takes a quarter of the characters, which makes it far less error prone for a person to handle."),
        Q("A file is 4500000 bits. What is its size in megabytes, using AQA's convention?", ["0.5625 MB", "4.5 MB", "0.5369 MB", "5.625 MB"], 0,
          "Divide by 8 to get 562500 bytes, then by 1000 to get 562.5 kilobytes, then by 1000 again to get 0.5625 megabytes."),
        Q("What is the largest denary value that can be stored in one byte?", ["255", "256", "128", "127"], 0,
          "Eight bits give 2 to the power 8, which is 256 different values, running from 0 to 255."),
    ],
    exam=[
        EQ("Explain why computers use the binary number system.", 2, [
            MP("The components a computer is built from have two distinguishable states", ["two states", "on or off", "high or low", "transistor", "voltage"]),
            MP("This makes storing and transmitting data reliable even when the signal degrades", ["reliable", "less error", "noise", "degrades", "easily told apart"]),
        ], "Computers are built from components such as transistors that have two clearly distinguishable states, either conducting or not conducting. Representing data with just two symbols means a value can still be read correctly even when the signal has been weakened or has picked up interference, which makes storage and transmission far more reliable than a system with many states would be.", command="Explain"),
        EQ("Convert the denary number 214 into 8 bit binary. Show your working.", 2, [
            MP("Shows a valid method, such as subtracting place values", ["128", "subtract", "place value", "64 32 16", "remainder"]),
            MP("Gives the answer 11010110", ["11010110"]),
        ], "Starting from the largest place value, 128 fits into 214 leaving 86, so the 128 column is 1. 64 fits into 86 leaving 22, so 1. 32 does not fit, so 0. 16 fits into 22 leaving 6, so 1. 8 does not fit, so 0. 4 fits leaving 2, so 1. 2 fits leaving 0, so 1. Then 0. The answer is 11010110.", command="Convert"),
        EQ("Convert the binary number 01111010 into hexadecimal. Show your working.", 2, [
            MP("Splits into two groups of four bits, 0111 and 1010", ["0111", "1010", "four bits", "nibbles", "groups"]),
            MP("Gives the answer 7A", ["7A", "7a"]),
        ], "Splitting the eight bits into groups of four from the right gives 0111 and 1010. The group 0111 is 4 plus 2 plus 1, which is 7. The group 1010 is 8 plus 2, which is 10, and 10 is written as A in hexadecimal. So the answer is 7A.", command="Convert"),
        EQ("Explain why programmers often write binary values in hexadecimal.", 3, [
            MP("One hexadecimal digit represents exactly four bits", ["four bits", "one digit four", "nibble", "16 is 2 to the 4"]),
            MP("So a value can be written in a quarter of the characters", ["shorter", "quarter", "fewer characters", "briefer", "compact"]),
            MP("Shorter values are easier for people to read and less likely to be mistyped", ["easier to read", "fewer mistakes", "misread", "mistype", "remember", "compare"]),
        ], "Sixteen is two to the power of four, so each hexadecimal digit corresponds to exactly four bits and a byte is always written as two hexadecimal digits. A long run of ones and zeros is extremely easy to lose your place in, and a single misread digit gives a completely different value. Written in hexadecimal the same value takes a quarter of the characters, so it is quicker to read aloud, quicker to write down and far easier to compare with another value, which is why memory addresses, colour codes and MAC addresses are all written this way.", command="Explain"),
        EQ("A file is 6 megabytes in size. Calculate how many bits this is, using 1 kilobyte as 1000 bytes.", 3, [
            MP("Converts megabytes to kilobytes by multiplying by 1000", ["6000", "x 1000", "kilobytes"]),
            MP("Converts kilobytes to bytes by multiplying by 1000", ["6000000", "6 million", "bytes"]),
            MP("Multiplies bytes by 8 to get 48000000 bits", ["48000000", "48 million", "x 8"]),
        ], "Six megabytes is 6 times 1000, which is 6000 kilobytes. That is 6000 times 1000, which is 6000000 bytes. Each byte is 8 bits, so the file is 6000000 times 8, which is 48000000 bits.", command="Calculate"),
    ],
)


# ============================================== 3.3.3 binary arithmetic

T_BINARITH = Topic(
    slug="binary-arithmetic-and-shifts",
    title="Binary Arithmetic and Shifts",
    spec="3.3.3",
    icon="i-binary",
    minutes=26,
    blurb="Adding binary numbers with carries, recognising overflow, and binary shifts, including exactly what happens to the bits that fall off the end.",
    fact="A binary left shift multiplies by two because every place value is twice the one to its right, which is the same reason adding a zero to the end of a denary number multiplies it by ten.",
    sections=[
        Section("Binary addition", """
There are only four rules, and every binary addition uses them.

```text
0 + 0 = 0
1 + 0 = 1
1 + 1 = 0 carry 1
1 + 1 + 1 = 1 carry 1
```

Work from the right hand column, exactly as in denary, carrying into the next column to the left.

```text
carry   1 1 1 1 1
        0 1 1 0 1 1 0 1     = 109
    +   0 0 1 1 0 1 1 0     =  54
      -------------------
        1 0 1 0 0 0 1 1     = 163
```

AQA requires you to be able to add **up to three** binary numbers. The method is unchanged, but three ones in a column give 1 carry 1, and three ones plus a carry give 0 carry 2, which means writing a 1 into each of the next two columns. Doing the addition in two stages, adding the first two numbers and then adding the third to that result, is usually safer and is fully acceptable.

!exam Always write the carry row :: It is the difference between a method mark and nothing. Examiners can see where a correct method went wrong only if the working is on the page.
"""),
        Section("Overflow", """
**Overflow** happens when the result of a calculation needs more bits than are available.

```text
        1 1 0 0 0 0 0 0     = 192
    +   1 0 0 0 0 0 0 0     = 128
      -------------------
      1 0 1 0 0 0 0 0 0     = 320, which needs nine bits
```

With only eight bits available, the carry out of the leftmost column has nowhere to go. It is lost, and the value actually stored is 01000000, which is 64. The program has not crashed and nothing has been reported: it simply now holds a wrong answer.

!key The definition worth memorising :: Overflow occurs when the result of an addition is too large to be stored in the number of bits available, so a carry is produced out of the most significant bit and the stored result is incorrect.

That last clause matters. Plenty of answers say the number is too big. Fewer say that the consequence is a wrong value being stored and used, which is what makes overflow dangerous rather than merely inconvenient.
"""),
        Section("Binary shifts", """
A **binary shift** moves every bit a given number of places left or right.

### Left shift

A left shift multiplies by 2 for each place shifted. Zeros come in on the right, and bits shifted off the left hand end are lost.

```text
00001011  = 11
shift left 1
00010110  = 22
shift left 2 more
01011000  = 88
```

Eleven times two is 22, and 22 times four is 88. The pattern holds until a 1 falls off the left hand end, at which point the value is wrong, and that is overflow again.

### Right shift

A right shift divides by 2 for each place shifted. Zeros come in on the left, and bits shifted off the right hand end are lost.

```text
00011001  = 25
shift right 1
00001100  = 12
```

Twenty five divided by two is 12.5, but there is nowhere to store the half. The 1 that fell off the right hand end is gone, so the result is 12. The division is integer division, and the lost bit is the remainder.

!warn Say what happens to the lost bits :: A full mark answer states that bits shifted out of the register are discarded and zeros are introduced at the other end, and that a right shift therefore loses precision. Saying only "it divides by two" is a partial answer.

### Why shifts are used

Shifting is far cheaper for a processor than a general multiply or divide, because it is a single hardware operation rather than a repeated one. Compilers replace multiplication by a power of two with a shift for exactly that reason.
"""),
    ],
    keyterms=[
        ("Binary addition", "Adding binary numbers column by column from the right, carrying into the next column."),
        ("Carry", "A 1 passed into the next column to the left when a column total is too large for one bit."),
        ("Overflow", "A result too large to be stored in the number of bits available, so the stored value is wrong."),
        ("Most significant bit", "The leftmost bit, which has the largest place value."),
        ("Least significant bit", "The rightmost bit, which has a place value of 1."),
        ("Binary shift", "Moving every bit in a value a number of places left or right."),
        ("Left shift", "A shift towards the most significant bit, multiplying by two for each place."),
        ("Right shift", "A shift towards the least significant bit, dividing by two for each place."),
    ],
    grade="""
Three habits separate full marks from most of a mark here.

**Write the carry row.** Every time, without exception. It is the method mark.

**Name the consequence of overflow, not just the cause.** The cause is that the result needs more bits. The consequence is that the carry is lost and an incorrect value is stored and then used, with no error reported.

**Describe a shift in three parts.** What direction the bits move, what fills the vacated positions, and what happens to the bits that leave. An answer with all three cannot be marked down.
""",
    mistakes=[
        "Adding from left to right. Binary addition works from the least significant bit, exactly like denary.",
        "Writing 1 + 1 = 2 in a column. There is no digit 2 in binary: it is 0 carry 1.",
        "Saying overflow means the program crashes. It usually does not, which is what makes it dangerous.",
        "Forgetting that bits shifted off the end are discarded rather than wrapping round.",
        "Claiming a right shift always divides exactly by two. It performs integer division, and an odd number loses its remainder.",
    ],
    quiz=[
        Q("What is 01011100 + 00101101 in binary?", ["10001001", "10001011", "01111001", "10000101"], 0,
          "92 plus 45 is 137, and 137 in binary is 10001001, which fits in eight bits so there is no overflow."),
        Q("What is the result of 1 + 1 + 1 in one binary column?", ["1 carry 1", "0 carry 1", "1 carry 0", "3"], 0,
          "Three ones make three, which is 11 in binary, so you write 1 in the column and carry 1 into the next."),
        Q("When does overflow occur?", ["When the result needs more bits than are available", "When a program divides by zero", "When a shift moves bits to the right", "When two negative numbers are added"], 0,
          "Overflow is specifically about the result being too large for the number of bits allocated, so the carry out of the most significant bit is lost."),
        Q("What is 00010110 shifted left by 2 places?", ["01011000", "00000101", "10110000", "00101100"], 0,
          "Every bit moves two places left and zeros come in on the right, giving 01011000. In denary 22 becomes 88, which is 22 times four."),
        Q("What happens to a bit that is shifted off the end of a register?", ["It is discarded", "It wraps round to the other end", "It is stored in a carry flag permanently", "It becomes the sign bit"], 0,
          "Bits shifted out of the register are lost. That is why a left shift can cause overflow and a right shift loses precision."),
        Q("What is 00011011 shifted right by 1 place, and what does it show in denary?", ["00001101, showing 27 becomes 13", "00110110, showing 27 becomes 54", "00001110, showing 27 becomes 14", "10001101, showing 27 becomes 141"], 0,
          "A right shift divides by two using integer division. 27 divided by two is 13.5, and the half is lost because the bit that fell off the right hand end is discarded."),
        Q("Why does a left shift of one place multiply a binary number by two?", ["Each place value is twice the one to its right", "Because a zero is added on the right", "Because binary uses only two digits", "Because the most significant bit is doubled"], 0,
          "Moving a bit one place left moves it into a column worth twice as much, so the whole value doubles. The zero coming in is a consequence, not the cause."),
        Q("A program adds two 8 bit values and stores 00000010, but the correct answer is 258. What has happened?", ["Overflow, and the ninth bit has been lost", "A right shift was applied", "The values were added in the wrong order", "The carry row was written incorrectly"], 0,
          "258 needs nine bits. With only eight available the carry out of the most significant bit is discarded, leaving the wrong value stored and no error reported."),
        Q("Why do processors use shifts instead of multiplication where they can?", ["A shift is a single hardware operation and is much faster", "A shift gives a more accurate answer", "Multiplication is not supported by most processors", "Shifts use fewer bits of storage"], 0,
          "Shifting is a single cheap hardware operation, whereas a general multiply takes many more cycles, so compilers replace multiplication by powers of two with shifts."),
        Q("What is 11000000 + 01000000 in 8 bits?", ["00000000 with overflow", "100000000", "10000000", "01000000"], 0,
          "192 plus 64 is 256, which needs nine bits. In eight bits the carry out of the leftmost column is lost and 00000000 is stored, so overflow has occurred."),
    ],
    exam=[
        EQ("Add the binary numbers 00110110 and 01001101. Give your answer in binary.", 2, [
            MP("Shows column addition with the carries", ["carry", "column", "working"]),
            MP("Gives the answer 10000011", ["10000011"]),
        ], "Working from the right: 0 plus 1 is 1, 1 plus 0 is 1, 1 plus 1 is 0 carry 1, 0 plus 1 plus the carry is 0 carry 1, 1 plus 0 plus the carry is 0 carry 1, 1 plus 0 plus the carry is 0 carry 1, 0 plus 1 plus the carry is 0 carry 1, and 0 plus 0 plus the carry is 1. The answer is 10000011, which is 131, and 54 plus 77 does equal 131.", command="Add"),
        EQ("Explain what is meant by overflow, and why it is a problem.", 3, [
            MP("The result of the calculation needs more bits than are available", ["more bits", "too large", "does not fit", "exceeds"]),
            MP("A carry is produced out of the most significant bit and is lost", ["carry", "most significant", "leftmost", "lost", "discarded", "no ninth bit"]),
            MP("The value stored is therefore incorrect, and usually no error is reported", ["incorrect", "wrong value", "no error", "not reported", "silently"]),
        ], "Overflow occurs when the result of a calculation is too large to be represented in the number of bits allocated to it. A carry is produced out of the most significant bit, and because there is no further bit to hold it the carry is simply discarded. The value that ends up stored is therefore wrong. What makes this a serious problem rather than a minor one is that the program normally carries on running with no error reported at all, so the incorrect value is used in later calculations and the fault can go unnoticed for a long time.", command="Explain"),
        EQ("The binary value 00101100 is shifted left by two places. Give the result and explain the effect on the denary value.", 3, [
            MP("Gives the result 10110000", ["10110000"]),
            MP("States that a left shift of two multiplies by four", ["multiplies by four", "x 4", "times four", "doubles twice"]),
            MP("Relates it to the denary values, 44 becomes 176", ["44", "176"]),
        ], "Shifting every bit two places to the left and filling the two vacated positions on the right with zeros gives 10110000. Each place a value is shifted left doubles it, because every column is worth twice the one to its right, so a shift of two places multiplies by four. In denary the original value is 44, and 44 times four is 176, which is what 10110000 represents.", command="Give"),
        EQ("Explain why a right shift can produce a result that is not exactly the original value divided by two.", 3, [
            MP("Bits shifted off the right hand end are discarded", ["discarded", "lost", "falls off", "removed"]),
            MP("For an odd number the least significant bit is a 1, which represents the remainder", ["odd", "least significant", "remainder", "the 1", "half"]),
            MP("So the result is the integer part of the division and precision is lost", ["integer", "rounded down", "precision", "loses", "whole number"]),
        ], "A right shift moves every bit one place towards the least significant end, and the bit that moves out of the rightmost position is discarded rather than stored anywhere. For an even number that bit is a 0 and nothing is lost, so the division by two is exact. For an odd number the least significant bit is a 1, and that 1 represents the remainder of the division. Discarding it means the result is the whole number part of the division only, so 25 shifted right by one gives 12 rather than 12.5 and precision has been lost.", command="Explain"),
    ],
)


# ============================================== 3.3.4 character encoding

T_CHARS = Topic(
    slug="character-encoding",
    title="Character Encoding",
    spec="3.3.4",
    icon="i-list",
    minutes=20,
    blurb="Character sets, ASCII and Unicode, why the codes for letters and digits are in order, and why the character '7' is not the number 7.",
    fact="The ASCII code for a capital letter and its lower case partner always differ by exactly 32, which is one bit. That was deliberate: it let 1960s hardware change case by flipping a single bit rather than by looking anything up.",
    sections=[
        Section("Character sets", """
A computer stores only numbers, so text has to be turned into numbers first. A **character set** is an agreed table giving every character a unique binary code.

Two machines can only exchange text if they use the same character set. Send text encoded in one set and display it using another and you get the wrong characters, which is exactly what the box symbols and question marks in badly handled text are.

!key A character set is an agreement, not a property of the machine :: There is nothing about the number 65 that makes it an A. It is an A because everybody agreed it would be.
"""),
        Section("ASCII", """
**ASCII** is a 7 bit character set, so it has 2 to the power 7, which is 128 codes, numbered 0 to 127. That covers the upper and lower case English alphabet, the digits, punctuation and a set of control characters such as carriage return.

Extended ASCII uses 8 bits and so has 256 codes, adding accented letters and box drawing characters.

### The codes are in order, and that is useful

- `'A'` is 65, so `'B'` is 66 and `'Z'` is 90.
- `'a'` is 97, so lower case is always the upper case code plus 32.
- `'0'` is 48, so the numeric value of a digit character is its code minus 48.

Those relationships get examined, because they let you do things with arithmetic instead of a lookup table.

```pseudo
code ← CHAR_TO_CODE(letter)
IF code ≥ 65 AND code ≤ 90 THEN
    letter ← CODE_TO_CHAR(code + 32)
ENDIF
```

!warn '7' is not 7 :: The character '7' has the ASCII code 55. The integer 7 is stored as the value seven. They are different things, which is why input has to be cast before it can be used in arithmetic.
"""),
        Section("Unicode", """
ASCII was designed for English. It has no code for Greek, Arabic, Chinese, Hindi, or for the symbols used in mathematics and music.

**Unicode** solves this by using far more bits per character, which gives it room for well over a million codes, enough for every writing system in current use and a great many that are not.

| | ASCII | Unicode |
| Bits per character | 7, or 8 for extended | Typically 8 to 32, variable |
| Number of characters | 128, or 256 extended | Over a million available |
| Languages covered | English and a little more | Effectively all of them |
| Storage per character | Small | Larger for characters outside the basic set |

The trade off is size. A document in Unicode can take more storage than the same document in ASCII, because some characters need more bytes. The first 128 Unicode codes are deliberately identical to ASCII, so plain English text costs the same in both and older files still open correctly.

!exam The comparison answer :: Unicode represents far more characters, so it supports languages ASCII cannot, at the cost of using more bits per character and therefore more storage. Both halves are needed for full marks.
"""),
    ],
    keyterms=[
        ("Character set", "An agreed table giving every character a unique binary code."),
        ("ASCII", "A 7 bit character set with 128 codes, covering English letters, digits, punctuation and control characters."),
        ("Extended ASCII", "An 8 bit version of ASCII with 256 codes."),
        ("Unicode", "A character set using more bits per character, able to represent over a million characters from every writing system."),
        ("Character code", "The number a character set assigns to a particular character."),
        ("Control character", "A character code that causes an action, such as a new line, rather than printing a symbol."),
    ],
    grade="""
The examinable subtlety here is the difference between a character and the value it looks like, and the strongest answers make it explicit.

**They say what is actually stored.** Not "the letter A is stored" but "the code 65 is stored as 01000001, and software uses the same character set to draw an A when it is displayed".

**They quantify Unicode's cost.** A grade 9 comparison names the benefit and the price in the same sentence: more characters, therefore more languages, therefore more bits per character and a larger file.

**They exploit the ordering.** When a question asks how a program could convert case or find the numeric value of a digit character, the answer is arithmetic on the code, and saying so shows you understand what a character set is.
""",
    mistakes=[
        "Saying ASCII has 256 characters. Standard ASCII is 7 bit and has 128; extended ASCII has 256.",
        "Treating the character '5' as the number 5.",
        "Saying Unicode replaced ASCII entirely. The first 128 Unicode codes are the same as ASCII by design.",
        "Claiming Unicode always uses more storage. For plain English text in a variable width encoding it uses the same.",
        "Forgetting that both machines must use the same character set for text to display correctly.",
    ],
    quiz=[
        Q("How many different characters can a 7 bit character set represent?", ["128", "127", "256", "64"], 0,
          "Seven bits give 2 to the power 7, which is 128 different combinations, numbered 0 to 127."),
        Q("If 'A' has the code 65, what is the code for 'D'?", ["68", "67", "69", "97"], 0,
          "The codes for the letters run in order, so D is three places after A, giving 68."),
        Q("If 'A' is 65 and 'a' is 97, what is the difference between an upper case and lower case code?", ["32", "26", "16", "64"], 0,
          "97 minus 65 is 32, and that gap is the same for every letter, which is why case can be changed by adding or subtracting 32."),
        Q("What is the main advantage of Unicode over ASCII?", ["It can represent characters from a far wider range of languages", "It uses fewer bits per character", "It stores images as well as text", "It compresses text automatically"], 0,
          "Unicode has room for over a million codes, so it can represent writing systems that ASCII, designed for English, has no codes for."),
        Q("What is the main disadvantage of Unicode compared with ASCII?", ["Characters outside the basic set need more bits, so files can be larger", "It cannot represent English letters", "It is not supported by modern computers", "It cannot be used on the internet"], 0,
          "More available codes means more bits per character for anything outside the basic set, which increases storage and transmission size."),
        Q("Why can the same file appear as the wrong characters on a different computer?", ["The two computers are using different character sets", "The file has been compressed", "The file size was calculated wrongly", "The characters were stored as images"], 0,
          "The stored codes only mean anything against a particular character set. Interpret them with a different set and different characters appear."),
        Q("What is actually stored when a computer saves the letter K?", ["The binary code the character set assigns to K", "A small picture of the letter K", "The word K in plain text", "The position of K in the alphabet as a shape"], 0,
          "Only the numeric code is stored. Software redraws the shape when the character is displayed, using the same character set to look it up."),
        Q("If '0' has the code 48, how would a program get the numeric value of a digit character?", ["Subtract 48 from its character code", "Add 48 to its character code", "Multiply the code by 10", "Divide the code by 8"], 0,
          "The digits are consecutive from 48, so the code for '7' is 55 and 55 minus 48 gives the value seven."),
        Q("What is a control character?", ["A code that causes an action such as a new line rather than printing a symbol", "A character that can only be typed with the control key", "A character used to control the CPU", "The first character of every file"], 0,
          "Control characters occupy the low codes in ASCII and represent actions such as carriage return, tab and backspace."),
        Q("Why are the first 128 Unicode codes the same as ASCII?", ["So that existing ASCII text remains valid and readable", "Because Unicode is a kind of ASCII", "To save memory when storing Chinese characters", "Because 128 is the maximum any character set can hold"], 0,
          "Keeping the codes identical means every existing ASCII file is already valid Unicode, which made adoption possible without rewriting the world's text."),
    ],
    exam=[
        EQ("State what is meant by a character set.", 1, [
            MP("An agreed set of codes giving every character a unique binary value", ["unique", "code for each", "agreed", "table", "binary value"]),
        ], "A character set is an agreed table that gives every character a unique binary code, so that text can be stored and exchanged as numbers.", command="State"),
        EQ("A character set uses 8 bits per character. Calculate how many different characters it can represent.", 2, [
            MP("Shows that the number of combinations is 2 to the power of the number of bits", ["2^8", "2 to the 8", "two to the power", "doubling"]),
            MP("Gives 256", ["256"]),
        ], "Each bit can be 0 or 1, so eight bits give 2 multiplied by itself eight times, which is 2 to the power 8. That is 256, so the character set can represent 256 different characters, numbered 0 to 255.", command="Calculate"),
        EQ("Explain one advantage and one disadvantage of using Unicode rather than ASCII.", 4, [
            MP("Unicode can represent far more characters", ["more characters", "over a million", "larger set", "many more"]),
            MP("So it supports languages and symbols ASCII has no codes for", ["languages", "chinese", "arabic", "emoji", "symbols", "worldwide"]),
            MP("Unicode uses more bits per character for characters outside the basic set", ["more bits", "more bytes", "larger", "16 bits", "32 bits"]),
            MP("So files can take more storage and take longer to transmit", ["storage", "file size", "larger files", "bandwidth", "slower to send"]),
        ], "The advantage is coverage. Unicode has room for well over a million codes, so it can represent Chinese, Arabic, Greek, mathematical symbols and emoji, none of which ASCII has any code for at all. That makes it possible to store and exchange text in any language rather than only in English. The disadvantage is size. Characters outside the basic Latin set need more than one byte, so a document containing them takes more storage and more bandwidth to send than the equivalent ASCII file would, if ASCII could represent it at all.", command="Explain"),
        EQ("A program reads the character '9' from a keyboard and adds 1 to it, expecting 10. Explain why this does not work and how it should be corrected.", 4, [
            MP("The keyboard returns the character '9', not the number 9", ["character", "string", "text", "not a number"]),
            MP("The character is stored as its character code, for example 57", ["character code", "57", "ascii value", "code"]),
            MP("Adding 1 either produces the next character or joins values rather than adding them", ["next character", "colon", "58", "concatenates", "joins", "wrong result"]),
            MP("The character must be converted to an integer first, for example with STRING_TO_INT", ["convert", "cast", "STRING_TO_INT", "change to a number", "int"]),
        ], "What arrives from the keyboard is the character '9', which is stored as its character set code rather than as the value nine. In ASCII that code is 57. Adding one to it therefore gives 58, which is the code for a colon, or in a language that treats the value as a string it joins the two values rather than adding them. Either way the result is not ten. The correction is to convert the character to an integer before doing arithmetic, for example value ← STRING_TO_INT(input), after which adding one gives ten as intended.", command="Explain"),
    ],
)


# ============================================== 3.3.5 representing images

T_IMAGES = Topic(
    slug="representing-images",
    title="Representing Images",
    spec="3.3.5",
    icon="i-palette",
    minutes=24,
    blurb="How a bitmap stores a picture as numbers, what resolution and colour depth actually control, why metadata is needed, and every step of an image file size calculation.",
    fact="The very first digital image was made in 1957 by Russell Kirsch, who scanned a photograph of his baby son at 176 by 176 pixels. The square pixel, which we are still using, was his practical choice at the time and he later called it a mistake.",
    sections=[
        Section("Bitmap images", """
A **bitmap** image is stored as a grid of **pixels**, and a binary value is recorded for the colour of every single pixel. A photograph is a bitmap, as is a screenshot or a scanned document.

The word bitmap is literal: the file is a map of which bits belong to which position in the grid.

### Resolution

**Resolution** is the number of pixels in the image, given as width by height. An image that is 1920 by 1080 has 1920 times 1080, which is 2073600 pixels.

More pixels means more detail, because there are more separate points at which the picture can change. It also means proportionally more data, since every pixel needs its own colour value.

!warn Resolution is a count, not a size on screen :: The same 1920 by 1080 image can fill a wall or a phone screen. What changes is how large each pixel appears, not how many there are.

### Colour depth

**Colour depth** is the number of bits used to store the colour of each pixel. It decides how many different colours a pixel can be, and the relationship is a power of two.

| Colour depth | Colours available | Typical use |
| 1 bit | 2 | Black and white line art |
| 4 bit | 16 | Very simple icons |
| 8 bit | 256 | Old games, indexed images |
| 24 bit | 16777216 | Photographs, true colour |

In 24 bit colour, 8 bits are given to red, 8 to green and 8 to blue, so each channel has 256 levels and every combination is possible. That is where the value 16.7 million comes from: 256 times 256 times 256.
"""),
        Section("Metadata", """
**Metadata** is data about the data. An image file cannot be opened correctly without it, because the raw pixel values alone do not say how they are arranged.

An image file typically stores:

- the **width** and **height** in pixels, so software knows where each row ends,
- the **colour depth**, so it knows how many bits belong to each pixel,
- the file format,
- and often the date, the camera settings, and the location the photograph was taken.

!key Why metadata is essential, in one sentence :: Without the width, a run of colour values is just a list. The width is what turns it back into a rectangle, so software cannot reconstruct the image without it.

The extra metadata raises privacy questions worth knowing about. A photograph taken on a phone commonly records the exact location and time, and those travel with the file when it is shared.
"""),
        Section("Calculating image file size", """
The formula AQA expects is:

**file size in bits = width in pixels x height in pixels x colour depth**

Then convert: divide by 8 for bytes, then by 1000 for each unit upwards, since AQA uses 1000.

### A worked example

An image is 800 by 600 pixels with a colour depth of 24 bits.

```text
pixels        = 800 x 600            = 480 000
size in bits  = 480 000 x 24         = 11 520 000 bits
size in bytes = 11 520 000 / 8       = 1 440 000 bytes
size in kB    = 1 440 000 / 1000     = 1 440 kB
size in MB    = 1 440 / 1000         = 1.44 MB
```

If the question gives a metadata size, add it after converting it to the same unit. Metadata is usually given in bytes, so convert your image data to bytes first and then add.

!exam Show every line :: There are method marks for the multiplication and for each conversion. A single number on the page, even a correct one, risks losing them if it is not the exact answer expected.

### Why the size grows so fast

Doubling the width and the height gives four times as many pixels, so four times the file size. Adding one bit of colour depth adds one bit to every pixel in the image. Both explain why raw uncompressed images are so large, and why compression matters.
"""),
    ],
    keyterms=[
        ("Bitmap", "An image stored as a grid of pixels, with a colour value recorded for every pixel."),
        ("Pixel", "The smallest individual element of a bitmap image, holding one colour value."),
        ("Resolution", "The number of pixels in an image, given as width by height."),
        ("Colour depth", "The number of bits used to store the colour of each pixel."),
        ("Metadata", "Data about the file itself, such as its width, height, colour depth and date."),
        ("True colour", "24 bit colour, giving 8 bits each to red, green and blue and around 16.7 million colours."),
    ],
    grade="""
Two things earn the last marks on this topic.

**Explaining size in terms of every pixel.** Increasing colour depth by one bit does not add one bit to the file, it adds one bit to every single pixel. Answers that say so are giving the mechanism rather than the fact.

**Being precise about metadata.** The strong answer names a specific item and says what would break without it: without the width, software cannot know where each row of pixels ends and the image cannot be reconstructed.

**Keeping units visible.** Write "bits" and "bytes" beside your numbers as you go. Most lost marks in this topic are a missing division by eight, and labelling the units makes the omission obvious to you before it is obvious to the examiner.
""",
    mistakes=[
        "Giving the answer in bits when the question asked for bytes, or the reverse.",
        "Forgetting to add the metadata when the question supplies a size for it.",
        "Confusing resolution with the physical size of the image on screen.",
        "Saying a higher colour depth means more pixels. It means more bits per pixel.",
        "Using 1024 rather than 1000 when converting units for AQA.",
    ],
    quiz=[
        Q("What does colour depth control?", ["The number of different colours each pixel can be", "The number of pixels in the image", "The physical size of the image on screen", "The file format used"], 0,
          "Colour depth is the number of bits stored per pixel, so it decides how many distinct colours a pixel can take."),
        Q("How many colours can be represented with a colour depth of 4 bits?", ["16", "8", "4", "256"], 0,
          "Four bits give 2 to the power 4, which is 16 different combinations and therefore 16 possible colours."),
        Q("An image is 400 by 300 pixels with a colour depth of 8 bits. What is its size in bits?", ["960000", "120000", "1200000", "480000"], 0,
          "There are 400 times 300, which is 120000 pixels, and each needs 8 bits, so the total is 960000 bits."),
        Q("Why does an image file need to store its width as metadata?", ["Without it, software cannot know where each row of pixels ends", "It makes the file smaller", "It is required by law", "It stores the colour of the first pixel"], 0,
          "The pixel values are a single sequence. The width is what tells software how to fold that sequence back into a rectangle."),
        Q("What happens to the file size if the colour depth is increased from 8 bits to 16 bits?", ["It doubles", "It increases by 8 bytes", "It stays the same", "It quadruples"], 0,
          "Every pixel now stores twice as many bits, and there are the same number of pixels, so the total doubles."),
        Q("An image of 2 megabytes is described as 1000 by 500 pixels. What is the colour depth, using 1 kB as 1000 bytes?", ["32 bits", "24 bits", "16 bits", "8 bits"], 0,
          "Two megabytes is 16000000 bits. There are 500000 pixels, and 16000000 divided by 500000 is 32."),
        Q("What is a pixel?", ["The smallest individual element of a bitmap image, holding one colour value", "The number of colours available", "A unit of file size", "A type of metadata"], 0,
          "A pixel is one point in the grid, and a bitmap stores a colour value for every one of them."),
        Q("Doubling both the width and the height of an image has what effect on its file size?", ["It becomes four times larger", "It doubles", "It stays the same", "It becomes eight times larger"], 0,
          "Twice the width and twice the height gives four times as many pixels, and each pixel still needs the same number of bits."),
        Q("Which of these is metadata rather than image data?", ["The date the photograph was taken", "The colour of the top left pixel", "The blue value of pixel 200", "The list of colour values"], 0,
          "Metadata is information about the file rather than the picture content itself, and the date is a classic example."),
        Q("Why can sharing a photograph raise a privacy concern even if the picture itself is harmless?", ["The metadata may include the exact location and time it was taken", "The colour depth reveals the camera model", "Pixels can be decoded into text", "The file size shows where the photograph was stored"], 0,
          "Phones commonly record the location and time in the file's metadata, and that information travels with the image when it is shared."),
    ],
    exam=[
        EQ("State what is meant by the resolution of an image.", 1, [
            MP("The number of pixels in the image, given as width by height", ["number of pixels", "width by height", "how many pixels", "pixels across and down"]),
        ], "The resolution of an image is the number of pixels it contains, expressed as the width in pixels multiplied by the height in pixels.", command="State"),
        EQ("An image is 640 pixels wide, 480 pixels high and uses a colour depth of 24 bits. Calculate the file size in kilobytes, using 1 kilobyte as 1000 bytes. Show your working.", 4, [
            MP("Multiplies width by height to get the number of pixels", ["640 x 480", "307200", "pixels"]),
            MP("Multiplies by the colour depth to get the size in bits", ["x 24", "7372800", "bits"]),
            MP("Divides by 8 to get bytes", ["/ 8", "divide by 8", "921600", "bytes"]),
            MP("Divides by 1000 to give 921.6 kB", ["921.6", "/ 1000", "kilobytes"]),
        ], "The number of pixels is 640 multiplied by 480, which is 307200. Each pixel needs 24 bits, so the image data is 307200 multiplied by 24, which is 7372800 bits. Dividing by 8 gives 921600 bytes, and dividing by 1000 gives 921.6 kilobytes.", command="Calculate"),
        EQ("Explain why increasing the colour depth of an image increases its file size.", 3, [
            MP("Colour depth is the number of bits stored for each pixel", ["bits per pixel", "each pixel", "number of bits"]),
            MP("Increasing it adds bits to every pixel in the image, not just to some", ["every pixel", "all pixels", "each one", "whole image"]),
            MP("So the total number of bits, and therefore the file size, increases in proportion", ["total", "file size", "proportion", "larger", "increases"]),
        ], "Colour depth is the number of bits used to store the colour of each individual pixel. Increasing the colour depth therefore adds those extra bits to every single pixel in the image rather than to the file as a whole, so an image containing two million pixels gains two million extra bits for each extra bit of colour depth. Since the file size is the number of pixels multiplied by the colour depth, raising the depth raises the size in direct proportion.", command="Explain"),
        EQ("Explain why metadata must be stored with an image file.", 3, [
            MP("The pixel data on its own is just a sequence of values", ["sequence", "list of values", "just numbers", "no structure"]),
            MP("The width and height tell software how the pixels are arranged into a grid", ["width", "height", "grid", "rows", "arrangement"]),
            MP("The colour depth tells software how many bits belong to each pixel", ["colour depth", "how many bits", "per pixel", "split the data"]),
        ], "Stored on its own, the pixel data is only a long sequence of binary values with nothing to say how they should be arranged. The metadata supplies that missing information. The width tells the software where one row of pixels ends and the next begins, which is what turns the sequence back into a rectangle, and the height confirms how many rows there should be. The colour depth tells the software how many bits belong to each pixel, without which it cannot divide the sequence into pixels at all. Without metadata the same file could be read as a completely different picture.", command="Explain"),
    ],
)


# ============================================== 3.3.6 representing sound

T_SOUND = Topic(
    slug="representing-sound",
    title="Representing Sound",
    spec="3.3.6",
    icon="i-play",
    minutes=24,
    blurb="How an analogue wave becomes a stream of numbers, what sample rate and sample resolution each control, and how to calculate a sound file size without losing a mark on the conversions.",
    fact="CD audio uses 44100 samples a second because of a rule from signal theory: to reconstruct a wave you must sample at more than twice its highest frequency. Human hearing tops out near 20000 Hz, so 44100 leaves a margin.",
    sections=[
        Section("From analogue to digital", """
Sound in the real world is a continuous wave of changing air pressure. It is **analogue**: at every instant it has some value, and between any two instants there are infinitely many more.

A computer cannot store something infinite, so the wave has to be **sampled**. Sampling means measuring the height of the wave at regular intervals and recording each measurement as a binary number.

The result is a staircase that follows the shape of the original wave without ever exactly matching it. Playing the file back reconstructs a wave from those measurements, and how close that reconstruction is to the original depends entirely on how often you measured and how precisely you recorded each measurement.

!key The two controls, and what each one does :: Sample rate controls how often you measure, which is detail across time. Sample resolution controls how precisely each measurement is recorded, which is detail in amplitude. Questions expect both, and expect you to know which is which.
"""),
        Section("Sample rate and sample resolution", """
### Sample rate

**Sample rate** is the number of samples taken each second, measured in hertz.

| Sample rate | Typical use |
| 8000 Hz | Telephone speech |
| 22050 Hz | Basic voice recording |
| 44100 Hz | CD quality music |
| 48000 Hz | Video soundtracks |

A higher sample rate means narrower steps in the staircase, so the digital version follows the original wave more closely and higher frequencies survive. It also means proportionally more samples to store.

### Sample resolution

**Sample resolution**, also called bit depth, is the number of bits used to store each individual sample. AQA uses the term sample resolution, so use it.

- 8 bits gives 256 possible levels for a sample's height.
- 16 bits gives 65536 levels.

Every measured height has to be rounded to the nearest available level, and the difference between the true height and the recorded one is the error introduced by digitising. More bits means more levels, so smaller rounding, so a more faithful recording.

!warn Do not swap the two terms :: Increasing the sample rate does not give a finer measurement of loudness, and increasing the resolution does not capture higher frequencies. Mark schemes distinguish them carefully.
"""),
        Section("Calculating sound file size", """
The formula AQA expects is:

**file size in bits = sample rate x sample resolution x duration in seconds**

If the recording is in stereo, multiply by 2 for the two channels.

### A worked example

A 3 minute recording at 44100 Hz with a sample resolution of 16 bits, in mono.

```text
duration      = 3 x 60               = 180 seconds
size in bits  = 44100 x 16 x 180     = 127 008 000 bits
size in bytes = 127 008 000 / 8      = 15 876 000 bytes
size in kB    = 15 876 000 / 1000    = 15 876 kB
size in MB    = 15 876 / 1000        = 15.876 MB
```

!exam Convert minutes to seconds first :: It is the single most common error on this question. The formula uses seconds, and a question that says three minutes is testing whether you noticed.

### Why quality costs so much

Doubling the sample rate doubles the file. Doubling the resolution doubles it again. Recording in stereo doubles it once more. That is why a few minutes of uncompressed CD quality audio runs to tens of megabytes, and why almost all music is distributed compressed.
"""),
    ],
    keyterms=[
        ("Analogue", "A continuously varying signal, which has a value at every instant."),
        ("Sampling", "Measuring the height of an analogue wave at regular intervals and recording each measurement as a number."),
        ("Sample rate", "The number of samples taken per second, measured in hertz."),
        ("Sample resolution", "The number of bits used to store each individual sample."),
        ("Duration", "The length of the recording in seconds, used in the file size calculation."),
        ("Channel", "One stream of audio. Mono has one, stereo has two."),
    ],
    grade="""
Almost every mark beyond the basics on this topic comes from keeping the two controls straight and from careful arithmetic.

**Say which control does what, in the same sentence as its effect.** "A higher sample rate takes more measurements each second, so rapid changes in the wave are captured and higher frequencies are preserved." That is a complete answer. "Better quality" is not.

**Name the price alongside the benefit.** Every improvement in quality has a proportional cost in file size, and questions asking you to evaluate a choice want both sides plus a decision.

**Convert to seconds before anything else.** Write it as the first line of your working so you cannot forget it.
""",
    mistakes=[
        "Leaving the duration in minutes when the formula needs seconds.",
        "Confusing sample rate with sample resolution.",
        "Forgetting to multiply by two for a stereo recording.",
        "Forgetting to divide the total bits by eight to get bytes.",
        "Saying that sampling captures the wave exactly. It approximates it, and the difference is the error introduced by digitising.",
    ],
    quiz=[
        Q("What does sample rate measure?", ["The number of samples taken each second", "The number of bits stored per sample", "The loudness of the recording", "The length of the file in seconds"], 0,
          "Sample rate is how often the wave is measured, given in hertz. How precisely each measurement is stored is the sample resolution."),
        Q("What does increasing the sample resolution do?", ["Gives more possible levels for each sample, so heights are recorded more precisely", "Takes more measurements each second", "Adds a second audio channel", "Reduces the file size"], 0,
          "Sample resolution is the number of bits per sample, so more bits gives more available levels and less rounding of each measured height."),
        Q("A 2 minute mono recording is made at 44100 Hz with 16 bit resolution. What is the size in bits?", ["84672000", "1411200", "705600", "42336000"], 0,
          "Two minutes is 120 seconds, so the calculation is 44100 times 16 times 120, which gives 84672000 bits."),
        Q("How many different levels can a 16 bit sample resolution represent?", ["65536", "16", "256", "32768"], 0,
          "Sixteen bits give 2 to the power 16, which is 65536 distinct levels for the height of a sample."),
        Q("What effect does recording in stereo rather than mono have on file size?", ["It doubles it, because two channels are stored", "It halves it", "It has no effect", "It quadruples it"], 0,
          "Stereo stores two separate streams of samples, one for each channel, so the file is twice the size of the mono equivalent."),
        Q("Why can a digital recording never be identical to the original analogue sound?", ["The wave is measured only at intervals and each measurement is rounded to an available level", "Microphones are not accurate enough", "Binary cannot represent sound", "The file is always compressed"], 0,
          "Sampling takes measurements at intervals rather than continuously, and each height is rounded to the nearest level the resolution allows, so some information is lost."),
        Q("A recording is made at 8000 Hz. What is the likely consequence?", ["It is suitable for speech but higher frequencies will be lost", "The file will be larger than a 44100 Hz recording", "Each sample will be stored more precisely", "The recording will be in stereo"], 0,
          "A low sample rate takes few measurements per second, so rapid changes are missed and high frequencies cannot be reconstructed. It remains adequate for speech, which is why telephones use it."),
        Q("Which change would improve the quality of a recording without affecting how precisely each individual height is stored?", ["Increasing the sample rate", "Increasing the sample resolution", "Recording in mono", "Reducing the duration"], 0,
          "The sample rate controls how often measurements are taken. Precision per measurement is the sample resolution, which is a separate control."),
        Q("A 30 second stereo recording at 44100 Hz and 16 bits is how large in megabytes, using 1 kB as 1000 bytes?", ["5.292 MB", "2.646 MB", "10.584 MB", "0.529 MB"], 0,
          "44100 times 16 times 30 times 2 is 42336000 bits. Divide by 8 for 5292000 bytes, then by 1000 twice to get 5.292 megabytes."),
        Q("Which unit is a sample rate measured in?", ["Hertz", "Bits", "Bytes per second", "Decibels"], 0,
          "Hertz means events per second, so a sample rate of 44100 Hz means 44100 measurements every second."),
    ],
    exam=[
        EQ("State what is meant by sample resolution.", 1, [
            MP("The number of bits used to store each sample", ["bits per sample", "number of bits", "each sample", "bit depth"]),
        ], "Sample resolution is the number of bits used to store each individual sample taken from the sound wave.", command="State"),
        EQ("A recording lasts 4 minutes. It is sampled at 44100 Hz with a sample resolution of 16 bits, in mono. Calculate the file size in megabytes, using 1 kilobyte as 1000 bytes. Show your working.", 4, [
            MP("Converts 4 minutes to 240 seconds", ["240", "4 x 60", "seconds"]),
            MP("Multiplies sample rate by resolution by duration", ["44100 x 16", "169344000", "x 240"]),
            MP("Divides by 8 to get bytes", ["/ 8", "divide by 8", "21168000"]),
            MP("Gives approximately 21.168 MB", ["21.168", "21.17", "21.2"]),
        ], "Four minutes is 4 times 60, which is 240 seconds. The size in bits is 44100 times 16 times 240, which is 169344000 bits. Dividing by 8 gives 21168000 bytes, dividing by 1000 gives 21168 kilobytes, and dividing by 1000 again gives 21.168 megabytes.", command="Calculate"),
        EQ("Explain the difference between sample rate and sample resolution, and the effect each has on the quality of a recording.", 4, [
            MP("Sample rate is how many samples are taken each second", ["per second", "how often", "frequency of sampling", "hertz"]),
            MP("A higher sample rate captures rapid changes and higher frequencies", ["rapid changes", "higher frequencies", "detail over time", "closer to the wave"]),
            MP("Sample resolution is how many bits are used for each sample", ["bits per sample", "each sample", "number of bits"]),
            MP("A higher resolution gives more levels, so each height is recorded more accurately", ["more levels", "more accurate", "less rounding", "precise", "closer to the true height"]),
        ], "Sample rate is the number of measurements taken from the wave each second, measured in hertz. Raising it means the measurements are closer together in time, so rapid changes in the wave are captured and higher frequencies survive into the recording. Sample resolution is the number of bits used to store each individual measurement. Raising it increases the number of levels a sample can take, so each measured height is rounded by a smaller amount and the recorded amplitude is closer to the true one. The two controls therefore improve different things: the rate improves detail across time and the resolution improves detail in loudness, and both increase the file size in direct proportion.", command="Explain"),
        EQ("A music streaming service wants to reduce the amount of data it sends to users on slow connections. Discuss two changes it could make to the audio and the effect each would have.", 6, [
            MP("It could reduce the sample rate", ["sample rate", "fewer samples", "lower rate", "22050", "hertz"]),
            MP("This reduces the file size in proportion but loses higher frequencies", ["proportion", "smaller", "loses high frequencies", "duller", "less detail"]),
            MP("It could reduce the sample resolution", ["resolution", "bit depth", "fewer bits", "8 bit"]),
            MP("This gives fewer levels, so loudness is recorded less accurately and the sound is noticeably worse", ["fewer levels", "less accurate", "rounding", "noise", "worse quality"]),
            MP("It could send mono rather than stereo, halving the data", ["mono", "one channel", "halves", "single channel"]),
            MP("Reaches a reasoned conclusion about the trade off for this situation", ["trade off", "conclusion", "acceptable", "recommend", "depends", "user would"]),
        ], "The first change is to reduce the sample rate, for example from 44100 Hz to 22050 Hz. That halves the number of samples and therefore halves the data sent, but it also halves the highest frequency that can be reconstructed, so cymbals and consonants sound dull and the recording loses its brightness. The second change is to reduce the sample resolution, for example from 16 bits to 8. That also halves the data, but it cuts the number of available levels from 65536 to 256, so every measured height is rounded much more coarsely, which is heard as a hiss behind quiet passages. A third option is to send mono rather than stereo, which halves the data again without touching the accuracy of any individual sample, at the cost of losing the sense of position in the mix. For a user on a slow connection the sensible order is to drop to mono first, because the loss is the least noticeable on phone speakers or a single earpiece, then reduce the sample rate, and only reduce the resolution as a last resort since that is where the audible damage is worst. Better still is to offer several quality levels and let the player choose automatically, so the user gets the best the connection can carry.", command="Discuss"),
    ],
)


# ============================================== 3.3.7 data compression

T_COMPRESS = Topic(
    slug="data-compression",
    title="Data Compression, Huffman and RLE",
    spec="3.3.7",
    icon="i-layers",
    minutes=30,
    blurb="Why compression matters, the difference between lossy and lossless, and full worked methods for both Huffman coding and run length encoding, including how to calculate the saving.",
    fact="Huffman coding was invented in 1951 by David Huffman, a student who took it on rather than sit a final exam. His method turned out to be provably optimal, which his own professor had failed to find.",
    sections=[
        Section("Why compress at all", """
**Compression** means reducing the number of bits needed to store a file.

Three reasons it matters, and questions expect the reason rather than just the word:

- **Storage.** More files fit in the same space.
- **Transmission time.** A smaller file takes less time to send, which matters most on a slow connection.
- **Bandwidth.** Less data sent means lower cost and less congestion, which is why streaming services compress heavily.

### Lossy and lossless

**Lossy** compression permanently removes data judged to be less important. The file gets much smaller and the original cannot be recovered exactly. JPEG images and MP3 audio are lossy: MP3 removes frequencies most people cannot hear, and JPEG discards fine colour detail the eye is poor at noticing.

**Lossless** compression stores the same information more efficiently, so the original file is reconstructed exactly. PNG images and ZIP archives are lossless.

| | Lossy | Lossless |
| Original recoverable | No | Yes |
| Size reduction | Large | More modest |
| Suitable for | Photographs, music, video | Text, program code, spreadsheets, archives |

!warn Never use lossy compression on text or code :: Removing "less important" characters from a program is not a smaller program, it is a broken one. That is exactly the reasoning a question about choosing a method wants.
"""),
        Section("Run length encoding", """
**Run length encoding**, or RLE, replaces a run of repeated values with a single value and a count of how many times it occurs.

Take a row of pixels: `W W W W W B B W W W W W W B B B`

That is 16 values. Written as run length pairs it becomes:

```text
5W 2B 6W 3B
```

Four pairs, eight values in total, storing exactly the same information. Nothing has been lost, so RLE is lossless.

### Working out the saving

Count what each version costs in the same unit. If each character costs one byte and each count costs one byte:

- Original: 16 bytes.
- Compressed: 4 pairs of 2 bytes, which is 8 bytes.
- Saving: 8 bytes, which is 50 per cent.

!warn RLE can make a file bigger :: Apply it to `A B A B A B A B` and every run has length one, so eight values become eight pairs and sixteen values. RLE only helps when the data contains long runs, which is why it suits simple graphics with blocks of flat colour and is useless on photographs.
"""),
        Section("Huffman coding", """
**Huffman coding** gives the most frequent characters the shortest binary codes and the least frequent the longest, so the total number of bits needed falls.

### Building the tree

Take the string `BANANA`. The frequencies are A three times, N twice and B once.

1. Write each character as a node with its frequency.
2. Repeatedly take the **two lowest** frequencies and join them under a new node whose frequency is their total.
3. Carry on until one node remains, which is the root.
4. Label every left branch 0 and every right branch 1.
5. A character's code is the sequence of labels from the root down to it.

For BANANA that gives A as `0`, N as `10` and B as `11`, or a mirror image of that depending on which side you place each pair. Either is acceptable as long as it is consistent and you read it off your own tree.

### Reading a code off the tree

Start at the root and follow the bits. When you reach a leaf, that is your character, and you go back to the root for the next one. Because no character's code is the start of another character's code, the stream can be decoded without any separators.

### Calculating the saving

`BANANA` in ASCII: 6 characters at 7 bits each is **42 bits**.

With the codes above:

```text
B  11        2 bits
A  0         1 bit  x 3  = 3 bits
N  10        2 bits x 2  = 4 bits
total                     = 9 bits
```

The saving is 42 minus 9, which is **33 bits**.

!exam The three things a Huffman question asks :: Build the tree, give a character's code by reading down from the root, and calculate the number of bits needed compared with ASCII. Practise all three, because a single question usually asks for all three.
"""),
    ],
    keyterms=[
        ("Compression", "Reducing the number of bits needed to store a file."),
        ("Lossy compression", "Compression that permanently removes data, so the original cannot be recovered exactly."),
        ("Lossless compression", "Compression that stores the same information more efficiently, so the original can be reconstructed exactly."),
        ("Run length encoding", "A lossless method that replaces a run of repeated values with the value and a count."),
        ("Huffman coding", "A lossless method that gives frequent characters shorter binary codes and rare characters longer ones."),
        ("Huffman tree", "A binary tree built from character frequencies, from which each character's code is read off."),
        ("Bandwidth", "The amount of data that can be transmitted in a given time."),
    ],
    grade="""
Huffman and RLE are the two places on this specification where careful working is worth several marks at once.

**Build the tree by always combining the two lowest frequencies.** Write the running totals as you go, so the examiner can follow your method even if one branch ends up on the wrong side.

**Say why your codes have no separators.** A top answer notes that no code is a prefix of another, which is what makes the stream decodable, and that is a mark most candidates never earn.

**Compare against the right baseline.** A saving question means comparing your total against the same string in ASCII, so state the ASCII cost, state the Huffman cost, and subtract.

**Justify lossy or lossless from the file type.** Photographs and music tolerate lossy compression because human perception does not notice the loss. Text and code cannot, because every character carries meaning.
""",
    mistakes=[
        "Saying lossless compression removes data. It removes redundancy in how data is stored, not the data itself.",
        "Combining the two highest frequencies when building a Huffman tree instead of the two lowest.",
        "Forgetting that a Huffman code is read from the root downwards, not from the leaf upwards.",
        "Assuming RLE always reduces the size. On data with no runs it makes the file larger.",
        "Comparing a Huffman total against 8 bits per character when the question specified 7 bit ASCII, or the reverse.",
    ],
    quiz=[
        Q("What is the defining feature of lossy compression?", ["Data is permanently removed and the original cannot be recovered exactly", "The file gets smaller with no change to the data", "It only works on text files", "It uses a Huffman tree"], 0,
          "Lossy compression discards information judged less important, which is why the original cannot be reconstructed exactly."),
        Q("Why must a text document be compressed losslessly?", ["Every character carries meaning, so removing any of them changes the content", "Text files are already small", "Lossy compression only works on binary files", "Text cannot be compressed"], 0,
          "There is no such thing as an unimportant character in a document or a program, so nothing can be discarded without changing what the file says."),
        Q("How would W W W B B B B W be written using run length encoding?", ["3W 4B 1W", "W3 B4 W1 with no counts", "8 values unchanged", "3W 4B"], 0,
          "There are three W, then four B, then one W, so the run length pairs are 3W, 4B and 1W."),
        Q("When does run length encoding make a file larger?", ["When the data contains few or no repeated runs", "When the data is a photograph in colour", "When the file is already compressed with Huffman", "When the runs are longer than ten"], 0,
          "Every run of length one becomes a pair, so data that alternates constantly ends up taking twice the space."),
        Q("In Huffman coding, which characters get the shortest codes?", ["The most frequent ones", "The least frequent ones", "The ones earliest in the alphabet", "All characters get equal length codes"], 0,
          "Giving the common characters short codes is what makes the total smaller, since those codes are used most often."),
        Q("When building a Huffman tree, which two nodes are combined at each step?", ["The two with the lowest frequencies", "The two with the highest frequencies", "The first two alphabetically", "Any two that are adjacent"], 0,
          "Repeatedly combining the two lowest frequencies pushes rare characters deeper into the tree, giving them the longer codes."),
        Q("The word MISSISSIPPI is 11 characters. In 7 bit ASCII, how many bits does it take?", ["77", "88", "11", "44"], 0,
          "Eleven characters at seven bits each is 77 bits, which is the baseline a Huffman saving would be measured against."),
        Q("Why can a Huffman coded stream be decoded without separators between characters?", ["No character's code is the beginning of another character's code", "Every code is the same length", "The codes are stored alphabetically", "A separator bit is added automatically"], 0,
          "Because every character sits at a leaf of the tree, no code is a prefix of another, so following bits from the root always reaches exactly one character."),
        Q("Which pair of file types are most appropriately compressed lossily?", ["A photograph and a music track", "A spreadsheet and a program", "A database and a text file", "A program and a photograph"], 0,
          "Photographs and music can lose detail that human perception does not register. Spreadsheets, programs and databases cannot lose anything at all."),
        Q("A file compresses from 2000 bits to 750 bits. What is the percentage saving?", ["62.5 per cent", "37.5 per cent", "26.6 per cent", "75 per cent"], 0,
          "The saving is 2000 minus 750, which is 1250. As a fraction of the original that is 1250 divided by 2000, which is 62.5 per cent."),
    ],
    exam=[
        EQ("State two reasons why a file might be compressed before being sent over the internet.", 2, [
            MP("It takes less time to transmit", ["quicker", "faster", "less time", "transmission time"]),
            MP("It uses less bandwidth, or takes less storage space at the other end", ["bandwidth", "less data", "storage", "space", "cheaper"]),
        ], "A compressed file contains fewer bits, so it takes less time to send, which matters particularly on a slow connection. It also uses less bandwidth, which reduces congestion on the network and lowers the cost for anybody paying for the data they use.", command="State"),
        EQ("Explain the difference between lossy and lossless compression, and give one appropriate use of each.", 4, [
            MP("Lossy compression permanently removes data, so the original cannot be recovered", ["removes", "permanently", "cannot recover", "lost", "discarded"]),
            MP("Gives a suitable lossy use such as photographs, music or video", ["photograph", "jpeg", "music", "mp3", "video", "streaming"]),
            MP("Lossless compression stores the same data more efficiently, so the original is recovered exactly", ["exactly", "recovered", "identical", "no data lost", "same file back"]),
            MP("Gives a suitable lossless use such as text, program code or a spreadsheet", ["text", "code", "program", "spreadsheet", "zip", "document", "database"]),
        ], "Lossy compression achieves a large reduction by permanently discarding data judged to be less important, which means the original file cannot be reconstructed exactly. It is appropriate for photographs and music, where human perception does not register the detail that is removed, which is why JPEG and MP3 are used. Lossless compression instead finds a more efficient way of storing exactly the same information, so the original is recovered perfectly, at the cost of a more modest reduction in size. It is essential for text documents, program code and spreadsheets, where every character carries meaning and discarding any of it would corrupt the file.", command="Explain"),
        EQ("A row of an image contains the pixels W W W W B B W W W W W W. Show how this row would be stored using run length encoding, and state one reason why RLE would be a poor choice for a photograph.", 4, [
            MP("Identifies the runs correctly as four W, two B, six W", ["4W", "2B", "6W", "four", "two", "six"]),
            MP("Writes them as value and count pairs", ["pairs", "count", "4 W 2 B 6 W", "value and number"]),
            MP("A photograph has very few long runs of identical pixels", ["few runs", "no repeats", "varies", "gradients", "every pixel different"]),
            MP("So RLE would give little saving and could make the file larger", ["no saving", "larger", "bigger", "worse", "increases"]),
        ], "The row contains four W, then two B, then six W, so under run length encoding it is stored as the pairs 4W, 2B, 6W. That is three pairs, six values in total, in place of the original twelve, and nothing has been lost. Run length encoding would be a poor choice for a photograph because photographs contain gradients and noise rather than blocks of identical colour, so almost every run has a length of one. Each single pixel would then be stored as a value and a count, which is two values where one was needed, and the compressed file would be larger than the original.", command="Show"),
        EQ("The word ABRACADABRA is to be compressed using Huffman coding. Describe how the Huffman tree would be constructed, and explain how the code for a character is obtained from it.", 5, [
            MP("Counts the frequency of each character", ["frequency", "count", "how many times", "occurrences"]),
            MP("Creates a node for each character with its frequency", ["node", "leaf", "each character"]),
            MP("Repeatedly combines the two nodes with the lowest frequencies under a new parent", ["two lowest", "smallest two", "combine", "join", "add together"]),
            MP("Continues until one root node remains, and labels branches 0 and 1", ["root", "one node", "0 and 1", "left and right", "label"]),
            MP("A character's code is read by following the branch labels from the root down to that character", ["from the root", "down to", "follow", "path", "sequence of labels"]),
        ], "First count how often each character occurs: A appears five times, B twice, R twice, C once and D once. Each character becomes a node carrying its frequency. The two nodes with the lowest frequencies, C and D, are then joined under a new parent node whose frequency is their total of two. That process repeats, always taking the two lowest frequencies still available, until a single root node remains holding the total of eleven. Every left branch is then labelled 0 and every right branch 1. To obtain the code for a character you start at the root and follow the branches down to that character's leaf, writing down each label as you pass it. Because A is the most frequent it ends up nearest the root and gets the shortest code, while C and D are deepest and get the longest, which is what makes the total number of bits smaller than fixed length coding would need.", command="Describe"),
        EQ("A message of 40 characters is stored in 7 bit ASCII. After Huffman coding it needs 148 bits. Calculate the number of bits saved and the saving as a percentage of the original.", 3, [
            MP("Calculates the ASCII size as 280 bits", ["280", "40 x 7"]),
            MP("Calculates the saving as 132 bits", ["132", "280 - 148"]),
            MP("Gives approximately 47 per cent", ["47", "47.1", "0.471"]),
        ], "In 7 bit ASCII the message takes 40 multiplied by 7, which is 280 bits. Huffman coding needs 148 bits, so the saving is 280 minus 148, which is 132 bits. As a percentage of the original that is 132 divided by 280, which is 0.4714, or approximately 47 per cent.", command="Calculate"),
    ],
)


# ==================================== 3.4.1 and 3.4.3 hardware and software

T_HWSW = Topic(
    slug="hardware-software-and-the-operating-system",
    title="Hardware, Software and the Operating System",
    spec="3.4.1 and 3.4.3",
    icon="i-layers",
    minutes=24,
    blurb="What separates hardware from software, the four jobs an operating system does that nothing else can, and the utility programs that keep a machine usable.",
    fact="The first operating system, GM-NAA I/O, was written in 1956 by General Motors and North American Aviation, not by a computer manufacturer. Customers built it because loading each program by hand was wasting more time than the programs took to run.",
    sections=[
        Section("Hardware and software", """
**Hardware** is the physical components of a computer system: the parts you could pick up. The processor, the memory modules, the drive, the keyboard, the screen, the cables.

**Software** is the programs and data that run on that hardware. Software has no physical existence of its own. It is a pattern of bits held in hardware, which is exactly why a single machine can be a games console, a word processor and a calculator without any physical change.

!key The relationship worth stating :: Hardware does nothing useful without software to tell it what to do, and software cannot run without hardware to run on. Each is useless alone.
"""),
        Section("System software and the operating system", """
Software divides into two categories.

**System software** manages the computer itself. It includes the operating system and utility programs.

**Application software** lets a user carry out a particular task: a browser, a word processor, a game, a photo editor.

The test is who the software is for. Application software serves the user's purpose. System software serves the machine, so that application software can run at all.

### What an operating system does

AQA names four core functions, and every one is examinable.

**Processor management.** The OS decides which process gets the processor and for how long, switching between them fast enough that they appear to run at once. Without this, one program would occupy the machine until it finished.

**Memory management.** The OS allocates memory to each running program and keeps them out of one another's memory. When physical memory runs out it moves less used pages to virtual memory on the drive.

**Peripheral management.** The OS talks to input and output devices through **device drivers**, so an application can simply say "print this" without knowing anything about the specific printer attached.

**User management.** The OS handles accounts, logins and permissions, so different users have different files and different rights on the same machine.

It also provides the user interface, whether graphical or command line, through which everything else is reached.

!exam The word 'manages' is not enough :: Say what is being managed and why it matters. "Memory management allocates memory to each program and prevents one program writing into another's memory, which would crash it" is the full answer.
"""),
        Section("Utility software", """
**Utility software** performs maintenance and housekeeping on the computer. It is system software, but it is not part of the operating system's core job.

| Utility | What it does | Why it is needed |
| Encryption software | Scrambles data so it is unreadable without the key | Protects data if a device is stolen or intercepted |
| Defragmentation | Rearranges files so their parts are stored together | Reduces the movement a mechanical drive's head must make, so files load faster |
| Data compression | Reduces file sizes | Saves storage and transmission time |
| Backup | Copies files to a separate location, often on a schedule | Allows recovery after failure, deletion or a ransomware attack |
| Anti-malware | Scans for and removes malicious software | Detects known threats before they run |

!warn Defragmentation is for mechanical drives :: A solid state drive has no moving head, so there is nothing to be gained by moving files together, and the extra writes actually shorten the drive's life. AQA has asked exactly this.
"""),
    ],
    keyterms=[
        ("Hardware", "The physical components that make up a computer system."),
        ("Software", "The programs and data that run on hardware and tell it what to do."),
        ("System software", "Software that manages the computer itself, including the operating system and utilities."),
        ("Application software", "Software that lets the user carry out a particular task."),
        ("Operating system", "System software that manages the processor, memory, peripherals and users, and provides the user interface."),
        ("Device driver", "Software that lets the operating system communicate with a particular hardware device."),
        ("Utility software", "System software that carries out maintenance tasks such as backup, compression or defragmentation."),
        ("Defragmentation", "Rearranging the parts of files on a mechanical drive so each file is stored together."),
    ],
    grade="""
Answers on this topic separate on specificity.

**Name the function and its consequence.** Not "the OS manages memory" but "the OS allocates each program its own area of memory and stops one program writing into another's, which would otherwise crash it".

**Say who the software is for.** The distinction between application and system software is about purpose, not about complexity, and a top answer says so.

**Be careful with defragmentation.** Any question that mentions a solid state drive is testing whether you know that defragmenting it is pointless and mildly harmful.
""",
    mistakes=[
        "Calling a device driver hardware. It is software that lets the OS talk to hardware.",
        "Saying utility software is application software. Utilities maintain the machine, so they are system software.",
        "Describing the operating system as 'the desktop'. The interface is one part of what it does.",
        "Saying defragmentation speeds up a solid state drive. It does not, and it wears the drive out faster.",
        "Listing OS functions without saying what each one achieves.",
    ],
    quiz=[
        Q("Which of these is system software?", ["A device driver", "A web browser", "A spreadsheet", "A photo editor"], 0,
          "A device driver exists so that the operating system can communicate with hardware, which makes it system software rather than something a user runs for a task."),
        Q("What is the purpose of memory management in an operating system?", ["To allocate memory to each program and stop one program writing into another's", "To increase the amount of physical RAM installed", "To store files permanently", "To defragment the hard drive"], 0,
          "The OS gives each running process its own area of memory and enforces the boundaries, which is what stops one faulty program bringing down another."),
        Q("Why does an operating system use device drivers?", ["So an application can use a device without knowing the details of that specific model", "To make devices run faster", "To store the device's data", "To encrypt data sent to a device"], 0,
          "The driver translates general instructions into the particular commands one device understands, so applications can be written once for any printer or graphics card."),
        Q("Which utility rearranges the parts of files so each file is stored together?", ["Defragmentation", "Compression", "Encryption", "Backup"], 0,
          "Defragmentation collects the scattered parts of each file into contiguous space, reducing how far a mechanical drive's read head must travel."),
        Q("Why is defragmenting a solid state drive not worthwhile?", ["It has no moving parts, so location does not affect access time, and the extra writes shorten its life", "Solid state drives never become fragmented", "It would delete the files", "Solid state drives defragment themselves every hour"], 0,
          "Access time on a solid state drive is the same wherever data sits, so there is nothing to gain, and every write uses up a little of the drive's limited write endurance."),
        Q("What distinguishes application software from system software?", ["Application software helps the user carry out a task, system software manages the computer", "Application software is always larger", "System software cannot be installed by the user", "Application software runs without an operating system"], 0,
          "The distinction is purpose. One serves the user's job, the other serves the machine so the user's job is possible."),
        Q("Which operating system function decides which process uses the processor next?", ["Processor management", "Memory management", "Peripheral management", "User management"], 0,
          "Scheduling processes onto the processor is processor management, and it is what makes several programs appear to run at the same time."),
        Q("What does user management in an operating system provide?", ["Accounts, logins and permissions so different users have different rights", "Faster processing for the main user", "Automatic backups of user files", "Extra memory for the current user"], 0,
          "User management keeps accounts separate, so each person has their own files and their own permissions on the same machine."),
        Q("Which utility would most directly help a school recover from a ransomware attack?", ["Backup software", "Defragmentation software", "Compression software", "A device driver"], 0,
          "Recent backups held separately from the network can simply be restored, which removes any reason to pay for a decryption key."),
        Q("Why can the same hardware run a game one minute and a word processor the next?", ["Because software is only a pattern of stored instructions, so it can be replaced without changing the hardware", "Because the processor physically reconfigures itself", "Because the operating system rebuilds the hardware", "Because games and word processors use different processors"], 0,
          "This is the stored program idea. Nothing physical changes: a different set of instructions is loaded and executed."),
    ],
    exam=[
        EQ("State one difference between system software and application software.", 2, [
            MP("System software manages or maintains the computer itself", ["manages the computer", "runs the computer", "maintains", "operating system", "controls"]),
            MP("Application software allows the user to carry out a particular task", ["task", "user", "job", "browser", "word processor", "purpose"]),
        ], "System software manages and maintains the computer itself, the operating system and utilities being the main examples. Application software is installed so that the user can carry out a particular task, such as writing a document or browsing the web.", command="State"),
        EQ("Describe two functions of an operating system.", 4, [
            MP("Memory management, allocating memory to running programs", ["memory", "allocate", "ram", "space for programs"]),
            MP("Explains a consequence, such as preventing one program writing into another's memory", ["prevents", "separate", "crash", "protects", "boundaries"]),
            MP("Processor management, scheduling which process runs and for how long", ["processor", "cpu", "scheduling", "which process", "time"]),
            MP("Explains a consequence, such as several programs appearing to run at the same time", ["appear to run at once", "multitasking", "share", "switching", "simultaneously"]),
        ], "The first function is memory management. The operating system allocates an area of memory to each running program and keeps track of what is in use, which prevents one program from writing into memory belonging to another and crashing it. When physical memory is exhausted it moves less recently used pages to virtual memory on the drive so that programs can continue. The second is processor management. The operating system schedules which process gets the processor and for how long, switching between them fast enough that they appear to the user to be running at the same time, which is what makes multitasking possible on a single core.", command="Describe"),
        EQ("A technician suggests defragmenting the solid state drive in a laptop to make it faster. Explain why this is not a good idea.", 3, [
            MP("Defragmentation moves file parts together to reduce read head movement", ["read head", "moving parts", "together", "contiguous", "mechanical"]),
            MP("A solid state drive has no moving parts, so access time is the same wherever data is stored", ["no moving parts", "same access time", "no head", "electronic"]),
            MP("The extra writes use up the drive's limited write endurance and shorten its life", ["writes", "wear", "shorten its life", "endurance", "damages"]),
        ], "Defragmentation exists to reduce how far the read head of a mechanical hard drive has to travel, by gathering the scattered parts of each file into one place. A solid state drive has no moving parts at all, and every location on it is reached in the same time, so bringing the parts of a file together gains nothing whatsoever. Worse, defragmentation involves rewriting a very large amount of data, and the memory cells in a solid state drive can only be written a finite number of times, so the operation actively shortens the life of the drive in exchange for no benefit.", command="Explain"),
        EQ("Explain why an operating system uses device drivers rather than communicating with hardware directly.", 3, [
            MP("Each hardware device has its own specific set of commands", ["specific", "different", "own commands", "varies", "each model"]),
            MP("The driver translates general instructions into the commands that device understands", ["translates", "converts", "interface", "understands"]),
            MP("So software can be written once and work with any device of that type", ["written once", "any device", "any printer", "does not need to know", "portable"]),
        ], "Every piece of hardware has its own particular set of commands and its own way of being addressed, and those differ between manufacturers and even between models from the same manufacturer. A device driver is software supplied for one specific device that translates the general instructions the operating system issues into the exact commands that device understands. That means an application can simply ask the operating system to print a page without knowing anything about the printer attached, and a new printer can be supported by installing a new driver rather than by rewriting every program.", command="Explain"),
    ],
)


# ============================================================ 3.4.2 logic

T_LOGIC = Topic(
    slug="boolean-logic",
    title="Boolean Logic",
    spec="3.4.2",
    icon="i-gate",
    minutes=28,
    blurb="NOT, AND, OR and XOR, how to build and read a logic circuit diagram, and a reliable method for completing the truth table of a combined circuit without guessing.",
    fact="Boolean algebra was published by George Boole in 1854 as a way of expressing logical reasoning mathematically. It had no practical application at all until Claude Shannon connected it to electrical switching circuits, eighty five years later.",
    sections=[
        Section("The four gates", """
A **logic gate** is a physical circuit taking one or more binary inputs and producing one binary output according to a fixed rule.

### NOT

Inverts its single input. Written as `NOT A`.

| A | Q |
| 0 | 1 |
| 1 | 0 |

### AND

Output is 1 only when **both** inputs are 1. Written as `A AND B`.

| A | B | Q |
| 0 | 0 | 0 |
| 0 | 1 | 0 |
| 1 | 0 | 0 |
| 1 | 1 | 1 |

### OR

Output is 1 when **at least one** input is 1. Written as `A OR B`.

| A | B | Q |
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 1 |

### XOR

Exclusive OR. Output is 1 when the inputs are **different**. Written as `A XOR B`.

| A | B | Q |
| 0 | 0 | 0 |
| 0 | 1 | 1 |
| 1 | 0 | 1 |
| 1 | 1 | 0 |

!key OR and XOR differ in exactly one row :: Both give 1 when one input is 1. Only OR also gives 1 when both are. Learn the bottom row and you have learned the difference.
"""),
        Section("Reading and drawing circuit diagrams", """
A logic circuit joins gates together, with the output of one becoming the input of the next.

To read a circuit, work from the inputs on the left towards the output on the right, naming the output of each gate as you go. Never try to see the whole thing at once.

For the circuit `Q = (A AND B) OR (NOT C)`:

- A and B go into an AND gate. Call its output `X`.
- C goes into a NOT gate. Call its output `Y`.
- X and Y go into an OR gate, and its output is Q.

Writing the expression from the diagram is the same process in reverse, working outwards from the inputs and bracketing each gate's output before it feeds the next.

!warn Brackets change the answer :: `(A AND B) OR C` and `A AND (B OR C)` are different circuits with different truth tables. If you are asked to write an expression from a diagram, the brackets are part of the answer.
"""),
        Section("Truth tables for combined circuits", """
This is where marks are won and lost, and there is a method that removes the guesswork entirely.

**Step 1: work out how many rows.** Two inputs give 4 rows, three inputs give 8, four give 16. It is 2 to the power of the number of inputs.

**Step 2: fill the input columns systematically.** With three inputs, the right hand column alternates 0 1 0 1, the middle alternates in pairs 0 0 1 1, and the left in fours 0 0 0 0 1 1 1 1. That guarantees every combination appears exactly once.

**Step 3: add a column for every intermediate gate output.** This is the step most candidates skip and it is where the method marks live.

**Step 4: fill each column completely before starting the next.** Working across a row means holding three rules in your head at once. Working down a column means applying one rule sixteen times, which is far harder to get wrong.

For `Q = (A AND B) OR (NOT C)`:

| A | B | C | A AND B | NOT C | Q |
| 0 | 0 | 0 | 0 | 1 | 1 |
| 0 | 0 | 1 | 0 | 0 | 0 |
| 0 | 1 | 0 | 0 | 1 | 1 |
| 0 | 1 | 1 | 0 | 0 | 0 |
| 1 | 0 | 0 | 0 | 1 | 1 |
| 1 | 0 | 1 | 0 | 0 | 0 |
| 1 | 1 | 0 | 1 | 1 | 1 |
| 1 | 1 | 1 | 1 | 0 | 1 |

!exam Never rub out an intermediate column :: The examiner cannot award method marks for working that is not there. Leave every column you added on the page.
"""),
    ],
    keyterms=[
        ("Logic gate", "A circuit that takes binary inputs and produces a binary output according to a fixed rule."),
        ("NOT gate", "A gate with one input whose output is the opposite of that input."),
        ("AND gate", "A gate whose output is 1 only when both inputs are 1."),
        ("OR gate", "A gate whose output is 1 when at least one input is 1."),
        ("XOR gate", "A gate whose output is 1 when its two inputs are different."),
        ("Truth table", "A table listing the output of a circuit for every possible combination of inputs."),
        ("Logic circuit", "Two or more gates joined together, with the output of one feeding the input of another."),
        ("Boolean expression", "A written form of a logic circuit, using NOT, AND, OR and XOR with brackets."),
    ],
    grade="""
Logic questions are the most mechanical on the paper, so the marks go to whoever is most systematic.

**Fill columns, not rows.** One rule applied many times beats many rules applied once. It is faster and it is far more accurate.

**Always add intermediate columns.** They are worth method marks in their own right, and they make the final column almost impossible to get wrong.

**Check two rows against the circuit at the end.** Pick the all zeros row and the all ones row and trace them through the diagram. If both match, the rest almost certainly does.

**When comparing two circuits, put the truth tables side by side.** "The output columns are identical for every combination of inputs, so the circuits are equivalent" is the sentence a mark scheme is looking for.
""",
    mistakes=[
        "Confusing OR with XOR. They differ only when both inputs are 1.",
        "Getting the wrong number of rows. Three inputs need eight rows, not six.",
        "Filling the input columns unsystematically, so a combination is missed or repeated.",
        "Rubbing out intermediate columns before handing in, which throws away method marks.",
        "Ignoring brackets when writing an expression from a diagram.",
    ],
    quiz=[
        Q("What is the output of an AND gate when its inputs are 1 and 0?", ["0", "1", "It depends on the circuit", "Both 0 and 1"], 0,
          "An AND gate gives 1 only when both inputs are 1. With one input at 0 the output is 0."),
        Q("Which gate gives an output of 1 only when its two inputs are different?", ["XOR", "OR", "AND", "NOT"], 0,
          "Exclusive OR is true when exactly one input is true, which is the same as saying the inputs differ."),
        Q("How many rows does a truth table need for a circuit with 4 inputs?", ["16", "8", "4", "12"], 0,
          "Each input doubles the number of combinations, so four inputs give 2 to the power 4, which is 16."),
        Q("What is the output of NOT (A OR B) when A is 0 and B is 1?", ["0", "1", "It cannot be determined", "2"], 0,
          "A OR B with inputs 0 and 1 gives 1, and NOT applied to 1 gives 0."),
        Q("In how many rows of a two input truth table do OR and XOR give different outputs?", ["1", "2", "3", "0"], 0,
          "They agree on three rows and differ only when both inputs are 1, where OR gives 1 and XOR gives 0."),
        Q("For the expression (A AND B) OR C, what is the output when A is 1, B is 0 and C is 1?", ["1", "0", "It depends on the order of the gates", "Undefined"], 0,
          "A AND B gives 0 because B is 0. That 0 is then ORed with C, which is 1, so the output is 1."),
        Q("Why should you add a column for each intermediate gate output when completing a truth table?", ["It reduces errors and earns method marks", "It is required by the specification", "It makes the table shorter", "Intermediate outputs are the final answer"], 0,
          "Breaking the circuit into stages means applying one simple rule at a time, and the working itself is creditworthy."),
        Q("Which expression matches a circuit where A and B feed an OR gate, whose output and C feed an AND gate?", ["(A OR B) AND C", "A OR (B AND C)", "A AND B AND C", "(A AND B) OR C"], 0,
          "The OR happens first and its output becomes one input of the AND, which is exactly what the brackets in (A OR B) AND C say."),
        Q("What is the output of A XOR B when both inputs are 1?", ["0", "1", "It alternates", "Undefined"], 0,
          "XOR gives 1 only when the inputs differ. Two ones are the same, so the output is 0."),
        Q("Two circuits are shown to be equivalent. What does this mean?", ["They produce the same output for every possible combination of inputs", "They contain the same number of gates", "They use the same type of gate", "They have the same number of inputs"], 0,
          "Equivalence is about behaviour. If the output columns of the two truth tables match on every row, the circuits do the same job however they are built."),
    ],
    exam=[
        EQ("Complete a truth table for the Boolean expression Q = NOT A AND B.", 4, [
            MP("Uses four rows covering all combinations of A and B", ["four rows", "00 01 10 11", "all combinations"]),
            MP("Includes a column for NOT A", ["not a", "intermediate", "extra column"]),
            MP("Gives Q as 1 only when A is 0 and B is 1", ["0 1", "only when a is 0 and b is 1", "one row"]),
            MP("Gives Q as 0 in the other three rows", ["0", "three rows", "otherwise 0"]),
        ], "With A and B as inputs the table has four rows. Adding a column for NOT A gives 1, 1, 0, 0 as A runs 0, 0, 1, 1. Q is that column ANDed with B, so Q is 0 when A is 0 and B is 0, Q is 1 when A is 0 and B is 1, Q is 0 when A is 1 and B is 0, and Q is 0 when A is 1 and B is 1. The output is therefore 1 in exactly one row, the one where A is 0 and B is 1.", command="Complete"),
        EQ("Explain the difference between an OR gate and an XOR gate.", 2, [
            MP("An OR gate outputs 1 when at least one input is 1", ["at least one", "either", "one or both", "any"]),
            MP("An XOR gate outputs 1 only when the inputs are different, so 0 when both are 1", ["different", "only one", "not both", "0 when both are 1", "exclusive"]),
        ], "An OR gate gives an output of 1 whenever at least one of its inputs is 1, including when both are. An XOR gate gives an output of 1 only when its two inputs are different, so when both inputs are 1 its output is 0. The two gates therefore agree on three of the four rows of the truth table and differ only on the last.", command="Explain"),
        EQ("A logic circuit has three inputs A, B and C. A and B feed an AND gate. The output of the AND gate and input C feed an XOR gate, whose output is Q. Write the Boolean expression for Q and state how many rows its truth table would have.", 3, [
            MP("Writes the AND operation in brackets", ["(a and b)", "a and b", "brackets"]),
            MP("Applies XOR with C to that output", ["xor c", "xor", "exclusive or"]),
            MP("States 8 rows", ["8", "eight", "2^3"]),
        ], "The AND gate acts first on A and B, so its output is written as A AND B and must be bracketed because it becomes a single input to the next gate. That output is then combined with C by the XOR gate, giving Q equals (A AND B) XOR C. With three inputs there are 2 to the power 3 combinations, so the truth table would have 8 rows.", command="Write"),
        EQ("Explain why it is good practice to include a column for each intermediate gate output when completing a truth table for a combined circuit.", 3, [
            MP("Each column applies one simple rule rather than several at once", ["one rule", "one gate", "simpler", "step by step", "one at a time"]),
            MP("This makes errors far less likely", ["fewer mistakes", "less likely", "more accurate", "reduces errors"]),
            MP("The working is creditworthy, so method marks can be awarded even if the final column is wrong", ["method marks", "working", "credit", "marks for working", "examiner can see"]),
        ], "Adding a column for each gate turns the problem into a series of single steps, so at each column you are applying one gate's rule repeatedly rather than holding two or three rules in your head while working across a row. That is both faster and considerably less error prone. It also matters for marks: the intermediate columns are the visible working, so an examiner can award method marks for a correct approach even if a slip appears in the final output column. Working that has been rubbed out cannot earn anything.", command="Explain"),
    ],
)


# ================================================== 3.4.4 systems architecture

T_ARCH = Topic(
    slug="systems-architecture",
    title="Systems Architecture",
    spec="3.4.4",
    icon="i-cpu",
    minutes=32,
    blurb="The von Neumann architecture, every register named in the specification, the fetch execute cycle in full, the three factors affecting CPU performance and what an embedded system actually is.",
    fact="The clock speed of desktop processors stopped climbing around 2005, not because engineers ran out of ideas but because the heat produced rises faster than the speed does. Adding cores was the way round the wall.",
    sections=[
        Section("The von Neumann architecture", """
Almost every computer follows the **von Neumann architecture**, whose defining feature is the **stored program concept**: instructions and data are held in the **same memory**, and instructions are fetched from that memory one at a time and executed.

Before this, changing what a machine did meant physically rewiring it. The stored program concept is why one laptop can be a word processor, a games console and a compiler without any physical change at all.

The consequence is the **von Neumann bottleneck**: because instructions and data share one bus to memory, they compete for it, and the processor can spend a substantial part of its time waiting.
"""),
        Section("Registers and the fetch execute cycle", """
A **register** is a very small, extremely fast storage location inside the CPU holding one value. AQA names four.

| Register | Full name | Holds |
| PC | Program Counter | The address of the **next** instruction to be fetched |
| MAR | Memory Address Register | The address currently being read from or written to |
| MDR | Memory Data Register | The data or instruction just fetched, or about to be written |
| ACC | Accumulator | The result of the most recent calculation |

!warn MAR holds an address, MDR holds data :: The names say so. Swapping them is one of the most commonly penalised errors on this topic, and it is entirely avoidable.

### The fetch execute cycle

**Fetch**

1. The address in the **PC** is copied into the **MAR**.
2. The **PC is incremented**, so it already points at the next instruction.
3. The address in the MAR travels out along the **address bus**, and the instruction at that address comes back along the **data bus** into the **MDR**.

**Decode**

4. The instruction in the MDR is decoded by the **control unit**, which works out what operation is required and what data it applies to.

**Execute**

5. The instruction is carried out. If it is a calculation the **ALU** performs it and the result goes into the **accumulator**. If it is a jump, a new address is written into the PC.

Then the cycle repeats, billions of times a second.

!exam The PC is incremented during fetch :: Not at the end of the cycle. If it waited, a jump instruction executed later would have its new address immediately overwritten.
"""),
        Section("CPU performance and embedded systems", """
Three factors affect how much work a processor gets done, and questions almost always ask you to compare two of them.

### Clock speed

The clock generates pulses, and one instruction stage happens per pulse. A 3 GHz processor produces three billion pulses a second. Doubling the clock speed roughly doubles the instructions completed per second, but power consumption and heat rise faster than the speed does, which is why clock speeds stopped climbing.

### Number of cores

A **core** is a complete processing unit. A quad core processor can genuinely execute four instructions at the same instant.

It rarely gives four times the performance, for two reasons worth stating: not all software is written to split work across cores, and some tasks are inherently sequential because each step needs the result of the last.

### Cache size

**Cache** is small, very fast memory inside or extremely close to the CPU holding recently and frequently used instructions and data. Fetching from cache takes a fraction of the time of fetching from RAM.

More cache means more of what the processor needs is already close by, so it spends less time waiting. Cache is expensive per byte, which is why there is not simply more of it.

!key The framing that earns marks :: Cache does not make the processor faster. It reduces the time the processor spends waiting, so more instructions are completed per second.

### Embedded systems

An **embedded system** is a computer built into a larger device to perform one specific, dedicated task: the controller in a washing machine, a microwave, a traffic light, a pacemaker, a digital camera.

Because the task is fixed, an embedded system can use a much less powerful processor, very little memory and no general purpose operating system. That makes it cheaper, more reliable and far more power efficient than a general purpose computer would be. The trade off is that it cannot be repurposed: a washing machine controller will never run anything else.
"""),
    ],
    keyterms=[
        ("Von Neumann architecture", "A design in which instructions and data share the same memory and instructions are fetched one at a time."),
        ("Stored program concept", "The idea that a program is held in memory alongside its data rather than being wired into the machine."),
        ("Register", "A very small, very fast storage location inside the CPU holding a single value."),
        ("Program Counter", "The register holding the address of the next instruction to be fetched."),
        ("Memory Address Register", "The register holding the address currently being read from or written to."),
        ("Memory Data Register", "The register holding data or an instruction that has just been fetched or is about to be written."),
        ("Accumulator", "The register holding the result of the most recent calculation."),
        ("Clock speed", "The number of clock pulses per second, measured in hertz."),
        ("Core", "A complete processing unit within a CPU, able to execute instructions independently."),
        ("Cache", "Small, very fast memory close to the CPU holding recently and frequently used data and instructions."),
        ("Embedded system", "A computer built into a larger device to carry out one dedicated task."),
    ],
    grade="""
This is the topic where naming things precisely is worth the most.

**Use the register names as part of the sentence.** "The address held in the Program Counter is copied into the MAR, and the instruction at that address returns along the data bus into the MDR" is a full mark answer. "The CPU gets the instruction from memory" is one mark at best.

**Explain performance as work completed, not as speed.** Cache reduces waiting. More cores allow genuine parallel execution but only where the software can use it. Clock speed raises the rate of stages but costs heat.

**Qualify the multi core claim.** A grade 9 answer says four cores do not give four times the performance because some tasks are sequential and not all software is written to use them.
""",
    mistakes=[
        "Swapping MAR and MDR. The Address Register holds an address, the Data Register holds data.",
        "Saying the Program Counter is incremented at the end of the cycle. It is incremented during fetch.",
        "Writing that cache makes the CPU faster. It reduces the time the CPU spends waiting.",
        "Claiming a quad core processor is always four times faster. It depends entirely on the software and the task.",
        "Describing an embedded system as simply a small computer. It is dedicated to one task, which is the point.",
    ],
    quiz=[
        Q("Which register holds the address of the next instruction to be fetched?", ["Program Counter", "MAR", "MDR", "Accumulator"], 0,
          "The Program Counter tracks where the processor is in the program, holding the address of the instruction to fetch next."),
        Q("What does the MDR hold?", ["Data or an instruction just fetched from memory", "The address being accessed", "The result of a calculation", "The next instruction's address"], 0,
          "The Memory Data Register holds the actual data or instruction travelling to or from memory. Addresses go in the MAR."),
        Q("At what point in the cycle is the Program Counter incremented?", ["During the fetch stage", "At the very end of the execute stage", "Only when a jump instruction runs", "Once per program"], 0,
          "Incrementing during fetch means a jump executed later can overwrite the PC without its new value being immediately replaced."),
        Q("What is the defining feature of the von Neumann architecture?", ["Instructions and data are stored in the same memory", "There are exactly four registers", "Programs are stored on a hard drive", "It uses more than one core"], 0,
          "The stored program concept, with instructions and data sharing one memory, is what defines von Neumann and what makes general purpose computers possible."),
        Q("Why does doubling the number of cores rarely double performance?", ["Some tasks are sequential and not all software can split work across cores", "Cores always share one clock pulse", "The extra cores run at half speed", "Cache is disabled when using multiple cores"], 0,
          "A task whose next step depends on the result of the last cannot be parallelised, and software must be written deliberately to use several cores."),
        Q("How does increasing cache size improve performance?", ["More of the data and instructions the CPU needs are already close by, so it waits less", "It increases the clock speed", "It adds extra cores", "It reduces the number of instructions in the program"], 0,
          "Cache reduces how often the processor has to wait for the much slower main memory, so more instructions complete each second."),
        Q("What is an embedded system?", ["A computer built into a larger device to carry out one dedicated task", "Any computer smaller than a laptop", "A computer with no operating system at all", "A computer that cannot be connected to a network"], 0,
          "The defining feature is that it is dedicated to one task within a larger device, which is why it can be cheap, reliable and power efficient."),
        Q("What travels along the address bus?", ["The location in memory being read from or written to", "The instruction being fetched", "The result of a calculation", "Control signals from the control unit"], 0,
          "The address bus carries memory addresses out of the processor. The instruction or data itself travels on the data bus."),
        Q("Where is the result of a calculation placed after the ALU performs it?", ["The accumulator", "The MAR", "The Program Counter", "Cache"], 0,
          "The accumulator holds the result of the most recent calculation, ready for it to be stored or used again."),
        Q("Why is the von Neumann bottleneck a limitation?", ["Instructions and data share one bus, so they compete for it and the CPU waits", "Only one program can be stored at a time", "Registers can hold only one value", "Memory can only be written, not read"], 0,
          "Because both instructions and data travel over the same connection to memory, only one can move at a time and the processor spends part of its time idle."),
    ],
    exam=[
        EQ("State the purpose of the Program Counter.", 1, [
            MP("It holds the address of the next instruction to be fetched", ["address", "next instruction", "where the next", "location of the next"]),
        ], "The Program Counter holds the memory address of the next instruction to be fetched from memory.", command="State"),
        EQ("Describe the fetch stage of the fetch execute cycle.", 4, [
            MP("The address in the Program Counter is copied into the MAR", ["program counter", "pc", "mar", "copied", "address register"]),
            MP("The Program Counter is incremented", ["incremented", "increased", "plus one", "next address"]),
            MP("The address travels out on the address bus to main memory", ["address bus", "sent to memory", "out to memory", "bus"]),
            MP("The instruction returns on the data bus into the MDR", ["data bus", "mdr", "returns", "brought back", "data register"]),
        ], "The address held in the Program Counter is copied into the Memory Address Register. The Program Counter is then incremented, so that it already holds the address of the following instruction. The address in the MAR travels out along the address bus to main memory, and the instruction stored at that address is returned along the data bus into the Memory Data Register, from where it is passed to the control unit to be decoded.", command="Describe"),
        EQ("Explain two factors that affect the performance of a CPU.", 4, [
            MP("Clock speed determines how many instruction stages happen per second", ["clock speed", "pulses", "hertz", "per second", "cycles"]),
            MP("A higher clock speed means more instructions completed in the same time", ["more instructions", "faster", "more work", "per second"]),
            MP("Cache size affects how often the CPU has to wait for main memory", ["cache", "close to the cpu", "fast memory", "waiting"]),
            MP("More cache means less waiting, so more instructions are completed per second", ["less waiting", "fewer fetches", "more instructions", "improves throughput"]),
        ], "The first factor is clock speed, which is the number of pulses the clock generates each second. One stage of the fetch execute cycle happens per pulse, so a processor running at 3 GHz gets through three billion stages a second and a faster clock means more instructions completed in the same time. The second is cache size. Cache is small, very fast memory close to the processor holding recently and frequently used data and instructions, and fetching from it takes a fraction of the time of fetching from RAM. A larger cache means more of what the processor needs is already close by, so it spends less time waiting for main memory and completes more instructions per second. Note that cache does not change the clock speed: it reduces idle time.", command="Explain"),
        EQ("A manufacturer replaces a dual core processor with a quad core processor of the same clock speed. Explain why the computer may not be twice as fast.", 3, [
            MP("Not all software is written to divide work across multiple cores", ["software", "written for", "not designed", "single threaded", "cannot use"]),
            MP("Some tasks are sequential, so each step needs the result of the previous one", ["sequential", "depends on", "cannot be split", "in order", "one after another"]),
            MP("So the additional cores may be idle for part of the time", ["idle", "unused", "not used", "wasted", "no benefit"]),
        ], "Adding cores only helps when there is work that can genuinely run at the same time. A great deal of software is written to run as a single sequence of instructions and simply will not use more than one core, so the extra cores sit idle while it runs. Even in software that is written for multiple cores, some tasks are inherently sequential, because each step needs the result of the one before it and cannot start until that result exists. Doubling the number of cores therefore doubles the theoretical maximum but rarely doubles the performance actually seen.", command="Explain"),
        EQ("Explain why an embedded system can use a less powerful processor than a general purpose computer.", 3, [
            MP("It is designed to carry out one specific dedicated task", ["one task", "dedicated", "specific", "single purpose"]),
            MP("It does not need to run a range of different software or a full operating system", ["no operating system", "one program", "not general purpose", "does not run other software"]),
            MP("So it needs less processing power and memory, which makes it cheaper and more power efficient", ["cheaper", "less memory", "power efficient", "reliable", "less powerful"]),
        ], "An embedded system exists to perform one fixed task within a larger device, such as running the wash cycle in a washing machine. Because that task never changes, the system does not have to run arbitrary software, does not need a full general purpose operating system and does not need to handle whatever a user might install next. The single program it runs can be written to fit the hardware exactly, so a modest processor and a very small amount of memory are sufficient. That makes the device cheaper to manufacture, more reliable because there is far less that can go wrong, and much more power efficient, which matters when the controller must run continuously.", command="Explain"),
    ],
)


# ================================================ 3.5.1 to 3.5.2 networks

T_NETWORKS = Topic(
    slug="computer-networks",
    title="Computer Networks and Topologies",
    spec="3.5.1 to 3.5.2",
    icon="i-network",
    minutes=26,
    blurb="Local and wide area networks, star and bus topologies compared properly, wired against wireless, and the three ways a wireless network is secured.",
    fact="Wi-Fi is not short for anything. The name was invented by a branding company in 1999 because the standard's real name, IEEE 802.11b Direct Sequence, was never going to appear on a box in a shop.",
    sections=[
        Section("Networks", """
A **network** is two or more computers connected together so that they can share data and resources such as files, printers and an internet connection.

A **LAN**, or local area network, covers a small geographical area on a single site, such as a school or an office. The organisation owns and maintains the cables and equipment itself.

A **WAN**, or wide area network, covers a large geographical area and connects sites that may be in different towns or countries. Because the connections cross land the organisation does not own, a WAN uses infrastructure hired from a telecommunications provider. The internet is the largest WAN of all.

!key The distinction is geography and ownership :: A LAN is on one site and the organisation owns the hardware. A WAN spans sites and uses infrastructure it rents. Size alone is not the answer.

### Network hardware

- A **network interface card** gives a device a physical connection and its MAC address.
- A **switch** joins devices on a LAN and sends each frame only to the device it is addressed to.
- A **router** joins networks together and directs packets between them, which is what connects a LAN to the internet.
- A **wireless access point** allows devices to join the network without a cable.
"""),
        Section("Star and bus topologies", """
A **topology** is the shape of the connections between devices. AQA examines two.

### Star

Every device has its own cable running to a central point, normally a switch. Nothing connects directly to anything else.

- **Fast**, because each device has a dedicated connection that nothing else is using.
- **Reliable**, because if one cable fails only that one device is affected.
- **Easy to add a device**, since you simply run another cable to the switch.
- **More expensive**, because every device needs its own cable and a switch is required.
- **The switch is a single point of failure**: if it fails, the whole network stops.

### Bus

Every device connects to a single shared cable, called the backbone, with a terminator at each end.

- **Cheap**, because it uses far less cable and needs no central device.
- **Simple to set up** for a small number of devices.
- **Slow when busy**, because every device shares one cable and only one can transmit at a time.
- **Data collisions** occur when two devices transmit at once, and both must wait and try again.
- **The backbone is a single point of failure**: a break in it brings down the whole network.
- **Less secure**, because every frame travels past every device.

!exam Compare, do not list :: A comparison question wants the two put beside each other. "A star is faster because each device has a dedicated connection, whereas on a bus every device shares one cable so they compete for it" is worth more than two separate lists of features.
"""),
        Section("Wired and wireless", """
### Wired

A wired connection carries data along a cable, usually copper Ethernet or fibre optic.

- **Faster and more consistent**, because the connection is not shared with the air.
- **More reliable**, since the signal is not weakened by distance, walls or interference.
- **More secure**, because an attacker needs physical access to the cable to intercept data.
- **Expensive and disruptive to install**, since cables must be run through the building.
- **Devices cannot move.**

### Wireless

A wireless connection carries data as radio waves through a wireless access point.

- **Convenient**, since devices can move freely and no cabling is needed.
- **Cheap and quick to install**, especially in an existing building.
- **Slower and less consistent**, and it degrades with distance and obstacles.
- **Subject to interference** from other networks and equipment.
- **Less secure by default**, because the signal travels through the air where anyone in range can receive it.

### Securing a wireless network

AQA names three measures:

- **Encryption**, so that intercepted data cannot be read without the key. WPA2 and WPA3 are the current standards.
- **MAC address filtering**, so that only devices on an approved list may join. It is a weak measure on its own, because a MAC address can be spoofed, but it raises the effort required.
- **A strong password on the access point**, since a default or guessable one makes every other measure pointless.
"""),
    ],
    keyterms=[
        ("Network", "Two or more computers connected together to share data and resources."),
        ("LAN", "Local area network, covering a small geographical area on a single site where the organisation owns the hardware."),
        ("WAN", "Wide area network, covering a large geographical area using infrastructure hired from a provider."),
        ("Topology", "The arrangement of the connections between devices on a network."),
        ("Star topology", "A layout in which every device has its own cable to a central switch."),
        ("Bus topology", "A layout in which every device connects to one shared backbone cable."),
        ("Switch", "A device that joins computers on a LAN and forwards each frame only to its destination."),
        ("Router", "A device that joins networks together and directs packets between them."),
        ("MAC address filtering", "Allowing only devices whose hardware addresses appear on an approved list to join a network."),
        ("WPA2", "A wireless encryption standard that protects data travelling over a Wi-Fi network."),
    ],
    grade="""
Marks here come from causal links rather than lists.

**Give the reason inside the claim.** "A bus network slows down as devices are added, because they all share one cable and only one can transmit at a time" is a full answer. "Bus networks are slow" is a fragment.

**Be honest about weaknesses.** MAC address filtering can be defeated by spoofing a permitted address, and saying so shows genuine understanding rather than a memorised list.

**Answer the situation in the question.** A room of fixed desktops, a building that cannot be rewired and a cafe offering guest access all have different right answers, and the marks for evaluation come from choosing on the evidence given.
""",
    mistakes=[
        "Defining a LAN purely by size. Ownership of the infrastructure is part of the distinction.",
        "Confusing a switch with a router. A switch connects devices within a network, a router connects networks together.",
        "Saying a star network has no single point of failure. The switch is one.",
        "Claiming MAC address filtering makes a network secure. It can be bypassed by spoofing.",
        "Saying wireless is always slower. A modern wireless standard can beat an old wired one, so the answer is about consistency and interference as much as raw speed.",
    ],
    quiz=[
        Q("What is the main difference between a LAN and a WAN?", ["A LAN covers one site with hardware the organisation owns, a WAN spans sites using hired infrastructure", "A LAN is wireless and a WAN is wired", "A LAN has fewer than 100 devices", "A WAN cannot connect to the internet"], 0,
          "The distinction combines geography and ownership. A WAN crosses land the organisation does not own, so it uses connections rented from a provider."),
        Q("In a star topology, what happens if one cable fails?", ["Only the device on that cable is disconnected", "The whole network stops", "Data collisions increase", "The switch reroutes traffic through another device"], 0,
          "Each device has its own dedicated cable to the switch, so a break affects only that one device."),
        Q("Why does a bus network slow down as more devices are added?", ["Every device shares one cable and only one can transmit at a time", "The backbone cable gets physically longer", "Each device needs its own switch port", "Bus networks cannot use fibre optic cable"], 0,
          "With one shared medium, devices compete for it and collisions become more frequent as traffic grows."),
        Q("What is the single point of failure in a star network?", ["The central switch", "Any one cable", "The terminator", "The network interface card"], 0,
          "Every device connects through the switch, so if the switch fails nothing can communicate."),
        Q("Which device connects two different networks together?", ["A router", "A switch", "A network interface card", "A wireless access point"], 0,
          "A router directs packets between networks, which is what connects a home or school LAN to the internet."),
        Q("Why is a wired connection generally more secure than a wireless one?", ["An attacker needs physical access to the cable rather than just being in range", "Wired connections are always encrypted", "Wireless signals cannot be recorded", "Cables cannot carry personal data"], 0,
          "A wireless signal travels through the air and can be received by anyone within range, whereas intercepting a cable means getting to the cable."),
        Q("What is the purpose of MAC address filtering?", ["To allow only devices on an approved list to join the network", "To encrypt data travelling over the network", "To speed up wireless transmission", "To assign IP addresses automatically"], 0,
          "The access point checks each device's hardware address against a list and refuses any that is not on it. It is a control on who may join, not a protection for the data."),
        Q("Why is MAC address filtering not a strong security measure on its own?", ["A MAC address can be spoofed to imitate an approved device", "It only works on wired networks", "It slows the network down too much", "It prevents legitimate devices from connecting"], 0,
          "MAC addresses travel in the clear and can be observed and then copied, so an attacker can present an approved address."),
        Q("Which topology needs the least cable?", ["Bus", "Star", "Both need the same amount", "It depends on the number of switches"], 0,
          "A bus uses one shared backbone with short drops to each device, whereas a star needs a separate run from every device to the switch."),
        Q("A school wants to connect twenty fixed desktop computers in one room, and speed and security matter most. Which is the better choice?", ["Wired connections in a star topology", "Wireless connections through one access point", "A bus topology using wireless", "Wireless with MAC filtering only"], 0,
          "The machines never move, so mobility gains nothing, and wired star gives each one a dedicated, fast, interference free and physically protected connection."),
    ],
    exam=[
        EQ("State one advantage and one disadvantage of a star topology compared with a bus topology.", 2, [
            MP("An advantage such as each device having a dedicated connection, so it is faster and a cable failure affects one device only", ["dedicated", "faster", "one device", "reliable", "no collisions"]),
            MP("A disadvantage such as needing more cable and a switch, so it costs more", ["more cable", "expensive", "switch", "cost", "single point of failure"]),
        ], "An advantage is that every device has its own dedicated cable to the switch, so devices do not compete for the medium and a single cable failure disconnects only the device on it. A disadvantage is cost: a star needs a separate cable run for every device plus a central switch, which is considerably more expensive than one shared backbone.", command="State"),
        EQ("Explain why a bus network becomes slower as more devices are added.", 3, [
            MP("All devices share a single backbone cable", ["one cable", "shared", "backbone", "single medium"]),
            MP("Only one device can transmit successfully at a time", ["one at a time", "cannot both", "share", "take turns"]),
            MP("More devices means more collisions, and after a collision data must be resent", ["collisions", "resend", "retransmit", "wait", "congestion"]),
        ], "Every device on a bus network is attached to the same backbone cable, so they all share one transmission medium and only one device can be transmitting successfully at any moment. As devices are added, the chance that two of them try to transmit at the same instant rises, and when that happens the signals interfere and both transmissions are lost. Each device then has to wait and send again, which adds further traffic to the same cable, so throughput falls away noticeably once the network becomes busy.", command="Explain"),
        EQ("A company is setting up a network in a listed building where cables cannot be run through the walls. Discuss whether a wireless network would be suitable.", 6, [
            MP("Wireless needs no cabling, so it can be installed without altering the building", ["no cables", "no drilling", "listed", "without altering", "quick to install"]),
            MP("It allows devices to move around the building", ["move", "mobility", "laptops", "tablets", "anywhere"]),
            MP("Wireless is generally slower and less consistent than a wired connection", ["slower", "inconsistent", "variable", "lower speed"]),
            MP("The signal is weakened by thick walls and by distance from the access point", ["walls", "distance", "thick", "weakened", "obstacles", "signal"]),
            MP("Wireless is less secure by default because the signal travels through the air", ["through the air", "intercept", "in range", "less secure", "anyone nearby"]),
            MP("Reaches a justified conclusion, including measures such as encryption and multiple access points", ["conclusion", "recommend", "therefore", "encryption", "wpa", "several access points", "strong password"]),
        ], "Wireless is the obvious fit for the constraint. No cabling has to be run, so the fabric of a listed building is untouched, installation is quick and cheap, and staff can move around with laptops and tablets rather than being tied to a desk. There are three real costs to weigh. Wireless is generally slower and less consistent than a wired connection, so a task that moves large files will take longer. The signal is weakened by distance and by obstacles, and the thick masonry typical of a listed building is exactly the kind of obstacle that causes dead spots. And the signal travels through the air, so anyone within range can receive it, which makes the network easier to attack than one where an intruder would have to reach a cable. None of those is decisive against wireless here, because the alternative is effectively unavailable. The company should install wireless, but should plan for it properly: several access points positioned to give overlapping coverage rather than one central unit, WPA2 or WPA3 encryption so that intercepted traffic cannot be read, a strong non default password on every access point, and a separate guest network so that visitors never reach company systems. If any single task genuinely needs sustained high bandwidth, a small number of surface mounted cable runs to those specific machines would be a sensible exception.", command="Discuss"),
    ],
)


# ================================================ 3.5.3 to 3.5.4 protocols

T_PROTOCOLS = Topic(
    slug="protocols-and-layers",
    title="Protocols and Layers",
    spec="3.5.3 to 3.5.4",
    icon="i-network",
    minutes=26,
    blurb="Every protocol named in the specification and what each one is actually for, why TCP and UDP are different jobs rather than rivals, and what layering buys you.",
    fact="TCP and IP were originally a single protocol. They were split in 1978 precisely so that applications needing speed more than reliability could use IP without paying for TCP's guarantees, which is where UDP came from.",
    sections=[
        Section("What a protocol is", """
A **protocol** is a set of rules governing how devices communicate. Both ends must follow the same rules or nothing can be understood.

That is more than a definition. It is why standards matter: a laptop made in one country can talk to a server made in another because both implement the same agreed rules.

### The protocols AQA names

| Protocol | Stands for | What it does |
| Ethernet | | The family of protocols for wired LANs, defining how frames are sent over cable |
| Wi-Fi | | The family of protocols for wireless LANs |
| TCP | Transmission Control Protocol | Splits data into packets, checks they all arrive, and reassembles them in order |
| UDP | User Datagram Protocol | Sends packets with no checking and no reassembly, which is faster |
| IP | Internet Protocol | Addresses packets and routes them between networks |
| HTTP | Hypertext Transfer Protocol | Requests and delivers web pages |
| HTTPS | HTTP Secure | The same, but encrypted so it cannot be read if intercepted |
| FTP | File Transfer Protocol | Transfers files between computers |
| SMTP | Simple Mail Transfer Protocol | **Sends** email |
| IMAP | Internet Message Access Protocol | **Retrieves** email, leaving it on the server so it syncs across devices |

!key SMTP sends, IMAP retrieves :: The single most commonly asked pair on this topic. Sending goes out with SMTP, reading comes back with IMAP.
"""),
        Section("TCP and UDP", """
These are not competitors. They are different tools for different jobs, and a question asking you to choose is really asking whether reliability or speed matters more.

**TCP** guarantees delivery. It numbers each packet, waits for the receiver to acknowledge each one, resends anything that does not arrive, and puts the packets back into order at the far end.

Use it when every byte must arrive: a web page, a file download, an email, a bank transfer. A missing byte in a downloaded program is a corrupt program.

**UDP** sends packets and does not check. Nothing is acknowledged, nothing is resent and nothing is reordered.

Use it when speed matters more than completeness: live video, voice calls, online gaming. A resent video frame would arrive after the moment it belonged to had passed, so resending it is worse than useless.

!exam The reasoning examiners want :: "UDP is used for a live video call because a lost packet would arrive too late to be useful, and waiting for it would add delay to the whole call." That is the mark, not "UDP is faster".
"""),
        Section("Layers", """
Network protocols are organised into **layers**, each of which handles one part of the job and passes its result to the layer below.

A four layer model is used:

| Layer | Job | Protocols |
| Application | Provides services to the user's software | HTTP, HTTPS, FTP, SMTP, IMAP |
| Transport | Splits data into packets and manages the connection | TCP, UDP |
| Network | Adds addresses and routes packets between networks | IP |
| Link | Sends the data over the physical medium | Ethernet, Wi-Fi |

Each layer wraps what it receives from the layer above in its own header. The receiving computer unwraps them in the reverse order, so each layer only ever deals with the header its counterpart added.

### Why layering is used

**It divides a huge problem into manageable parts.** Nobody has to understand the whole of networking at once.

**Layers can be changed independently.** Moving a laptop from Ethernet to Wi-Fi changes the link layer only. HTTP, TCP and IP carry on exactly as before, and no application has to be rewritten.

**It allows specialisation and competition.** Different manufacturers can build products for different layers, and as long as each follows the standard for its layer, everything interoperates.

**It makes faults easier to isolate.** If a website loads by its IP address but not by its name, the problem is in name resolution, not in the cable.

!warn Do not say layers make the network faster :: They do not. Layering is about manageability, interoperability and independent change, and that is what the mark scheme rewards.
"""),
    ],
    keyterms=[
        ("Protocol", "A set of rules governing how devices communicate, which both ends must follow."),
        ("TCP", "Transmission Control Protocol, which splits data into packets, checks delivery and reassembles them in order."),
        ("UDP", "User Datagram Protocol, which sends packets without checking delivery or reassembling them."),
        ("IP", "Internet Protocol, which addresses packets and routes them between networks."),
        ("HTTP", "The protocol used to request and deliver web pages."),
        ("HTTPS", "HTTP with encryption, so intercepted traffic cannot be read."),
        ("SMTP", "The protocol used to send email."),
        ("IMAP", "The protocol used to retrieve email while leaving it on the server."),
        ("Layer", "One level of a networking model, handling one part of the communication task."),
        ("Encapsulation", "Each layer wrapping the data it receives in its own header before passing it on."),
    ],
    grade="""
This topic rewards knowing why, not just what.

**Justify TCP or UDP from the consequence of loss.** Ask what happens if a packet goes missing. If the result is corrupt data, TCP. If the result is a moment that has already passed, UDP.

**Explain layering with a change.** The clearest evidence of understanding is an example: swapping Wi-Fi for Ethernet changes the link layer and nothing above it, so no application needs rewriting.

**Give HTTPS its mechanism.** Not "it is secure" but "the data is encrypted before transmission, so intercepted traffic cannot be read without the key".
""",
    mistakes=[
        "Swapping SMTP and IMAP. SMTP sends, IMAP retrieves.",
        "Saying UDP is better than TCP. They serve different purposes, and the right one depends on whether loss or delay is worse.",
        "Saying layering makes a network faster. It makes it manageable and interoperable.",
        "Describing HTTPS as a different protocol from HTTP. It is HTTP with encryption added.",
        "Saying IP guarantees delivery. IP addresses and routes packets; TCP is what checks they arrived.",
    ],
    quiz=[
        Q("Which protocol is used to send an email?", ["SMTP", "IMAP", "HTTP", "FTP"], 0,
          "Simple Mail Transfer Protocol handles sending. Retrieving mail from a server is IMAP's job."),
        Q("What is the main difference between TCP and UDP?", ["TCP checks that packets arrive and reassembles them, UDP does not", "TCP is used for websites and UDP for files", "UDP encrypts data and TCP does not", "TCP works only on wired networks"], 0,
          "TCP numbers packets, acknowledges them, resends anything missing and reorders them. UDP does none of that, which is why it is faster."),
        Q("Why is UDP used for live video calls?", ["A resent packet would arrive too late to be useful, and waiting for it would add delay", "UDP encrypts the video automatically", "Video files are too large for TCP", "TCP does not work with cameras"], 0,
          "In a live call the moment a lost frame belonged to has already passed, so resending it adds delay for no benefit."),
        Q("What does the Internet Protocol do?", ["Addresses packets and routes them between networks", "Guarantees that packets arrive", "Encrypts data before it is sent", "Delivers web pages to a browser"], 0,
          "IP handles addressing and routing. Checking that packets actually arrived is TCP's responsibility, at a different layer."),
        Q("At which layer of the four layer model does HTTP operate?", ["Application", "Transport", "Network", "Link"], 0,
          "HTTP provides a service directly to the user's software, which is what the application layer is for."),
        Q("What is added by each layer as data passes down the stack?", ["Its own header", "A copy of the data", "A checksum only", "The user's IP address"], 0,
          "Each layer wraps what it received in its own header, and the receiving machine unwraps them in reverse order."),
        Q("Why is layering used in network protocols?", ["It breaks a complex task into parts that can be changed independently", "It makes the network transmit faster", "It reduces the number of protocols needed to one", "It encrypts data automatically"], 0,
          "Layering means each layer can be replaced without disturbing the others, which is why switching from Ethernet to Wi-Fi needs no change to any application."),
        Q("What does HTTPS add to HTTP?", ["Encryption, so intercepted traffic cannot be read", "Faster page loading", "Automatic compression of images", "A guarantee that packets arrive"], 0,
          "HTTPS is HTTP carried over an encrypted connection, so anyone intercepting the traffic sees only unreadable data."),
        Q("Which protocol would be most appropriate for downloading a program installer?", ["TCP, because every byte must arrive intact", "UDP, because speed matters most", "SMTP, because it handles large files", "IMAP, because it leaves a copy on the server"], 0,
          "A single missing byte would corrupt the installer, so the guaranteed delivery and reordering TCP provides is essential."),
        Q("A laptop is moved from a wired connection to Wi-Fi and everything still works. Which principle does this demonstrate?", ["Layers can be changed independently of one another", "Protocols are optional", "TCP converts itself to UDP", "Wireless and wired use the same cable standard"], 0,
          "Only the link layer changed. The transport, network and application layers above it were untouched, which is exactly what layering is for."),
    ],
    exam=[
        EQ("State what is meant by a protocol.", 1, [
            MP("A set of rules governing how devices communicate", ["rules", "standards", "agreed", "how devices communicate", "govern"]),
        ], "A protocol is a set of rules that governs how devices communicate, which both the sending and the receiving device must follow for the communication to be understood.", command="State"),
        EQ("Explain why TCP would be used to download a file but UDP would be used for a live video call.", 4, [
            MP("TCP checks that every packet arrives and reassembles them in order", ["checks", "acknowledges", "resends", "in order", "guarantees"]),
            MP("A downloaded file would be corrupt if any part were missing", ["corrupt", "missing", "incomplete", "damaged", "every byte"]),
            MP("UDP sends packets without checking or resending, so it is faster", ["no checking", "does not resend", "faster", "no acknowledgement"]),
            MP("A resent video packet would arrive too late to be useful, and waiting for it would add delay", ["too late", "already passed", "delay", "lag", "live"]),
        ], "TCP numbers every packet, waits for the receiver to acknowledge each one, resends anything that fails to arrive and puts the packets back into the right order at the far end. That is essential for a file download, because a file with a missing or misordered section is corrupt and will not work at all. UDP does none of that checking, which makes it faster and removes the delay that waiting for acknowledgements introduces. For a live video call that trade is the right one: a packet that was lost and then resent would arrive after the fraction of a second it belonged to had already been displayed, so it is useless, and the delay caused by waiting for it would degrade the whole call for everyone.", command="Explain"),
        EQ("Describe two reasons why network protocols are arranged in layers.", 4, [
            MP("Each layer handles one part of the task, so the problem is broken into manageable parts", ["one part", "manageable", "divide", "simpler", "specialise"]),
            MP("Developers can work on one layer without understanding the whole system", ["one layer", "without", "specialists", "focus"]),
            MP("A layer can be changed or replaced without affecting the layers above or below", ["changed", "replaced", "independent", "without affecting", "swap"]),
            MP("Gives an example, such as changing from Ethernet to Wi-Fi affecting only the link layer", ["ethernet", "wi-fi", "link layer", "example", "no change to"]),
        ], "The first reason is that layering divides a very large problem into parts small enough to handle. Each layer is responsible for one aspect of communication and only has to interact with the layer directly above and below it, so a developer working on an email client does not need to understand how a signal is placed onto a cable. The second is independence. Because each layer only relies on the interface the next one presents, a layer can be replaced entirely without disturbing the others. Moving a laptop from an Ethernet cable to Wi-Fi changes the link layer completely, but IP, TCP and HTTP carry on unchanged, which is why no application has to be rewritten when the connection type changes.", command="Describe"),
        EQ("A school website changes from HTTP to HTTPS. Explain the benefit to users.", 3, [
            MP("HTTPS encrypts the data before it is transmitted", ["encrypts", "encryption", "scrambled", "coded"]),
            MP("Intercepted traffic cannot be read without the key", ["intercepted", "cannot be read", "unreadable", "meaningless", "without the key"]),
            MP("So personal data such as logins and messages is protected in transit", ["login", "password", "personal data", "protected", "in transit", "safe"]),
        ], "HTTPS carries the same HTTP requests and responses over an encrypted connection, so the data is scrambled before it leaves the user's device and is only unscrambled at the far end. Anybody who intercepts the traffic in between, for example on a shared public network, sees only unreadable data rather than the actual content. That matters because users log in to the school site and may send personal information through it, and under plain HTTP a username and password would travel as readable text that anyone on the same network could capture.", command="Explain"),
    ],
)


# ============================================================ 3.6 cyber security

T_CYBER = Topic(
    slug="cyber-security",
    title="Cyber Security",
    spec="3.6",
    icon="i-shield",
    minutes=30,
    blurb="Social engineering and malware named threat by threat, plus every detection and prevention method in the specification, with the reason each one works.",
    fact="The single most common way into an organisation is not a technical flaw. Year after year, the attack that succeeds most often is somebody being persuaded to hand over a password, which is why social engineering is a specification topic in its own right.",
    sections=[
        Section("What cyber security is, and social engineering", """
**Cyber security** is the processes, practices and technologies used to protect networks, computers, programs and data from attack, damage and unauthorised access.

### Social engineering

**Social engineering** means manipulating a person into giving away information or access, rather than attacking the technology. It works because people are helpful, busy and reluctant to challenge someone who sounds authoritative.

| Threat | What it is |
| Blagging | Inventing a scenario to persuade someone to hand over information, for example pretending to be from IT and needing the password to fix an urgent fault |
| Phishing | Sending a message that appears to come from a legitimate organisation, to trick the recipient into revealing details or clicking a malicious link |
| Pharming | Redirecting a user to a fake website even though they typed the correct address, by altering DNS or the host file |
| Shouldering | Watching someone enter a PIN or password over their shoulder, at a cash machine or on a train |

!key Why social engineering works :: It bypasses every technical control. Encryption, firewalls and strong passwords all protect data from an attacker who does not have the password. None of them help once somebody has been persuaded to give it away.
"""),
        Section("Malicious code and other threats", """
**Malware** is any software written with the intention of causing harm.

| Type | Behaviour |
| Virus | Attaches itself to a file and spreads when that file is opened or shared |
| Worm | Spreads by itself across a network without needing a user to do anything |
| Trojan | Pretends to be legitimate software so the user installs it willingly |
| Ransomware | Encrypts the victim's files and demands payment for the key |
| Spyware | Records activity such as keystrokes and sends it to the attacker |

### Other weaknesses AQA names

**Weak and default passwords.** A password that is short, common or left as the manufacturer set it can be guessed or brute forced in seconds.

**Misconfigured access rights.** Giving users more permission than their job needs means a single compromised account exposes far more than it should.

**Removable media.** A USB stick can carry malware straight past the firewall, because it never touches the network at all.

**Unpatched or outdated software.** Most successful attacks exploit weaknesses that were fixed months earlier in an update the victim never installed.

!exam Name the threat precisely :: A question describing a fake email asking a user to confirm bank details is phishing. One describing a phone call from a supposed colleague is blagging. Using the general word "hacking" throws away the mark.
"""),
        Section("Detecting and preventing attacks", """
| Method | How it helps |
| Biometric measures | Uses a physical characteristic such as a fingerprint, which cannot be guessed or easily shared |
| Password systems | Requiring length, mixed character types and a limit on failed attempts makes guessing and brute force impractical |
| CAPTCHA | Distinguishes a human from an automated script, blocking bulk automated attacks |
| Email confirmations | Confirms that the person requesting an account or a change controls that address |
| Automatic software updates | Closes known weaknesses promptly, without relying on anyone remembering |
| Penetration testing | Authorised simulated attacks that find weaknesses before an attacker does |
| Anti-malware software | Scans files against known threats and removes them before they run |
| Firewalls | Inspect traffic entering and leaving the network and block anything not permitted |
| User access levels | Give each user only the permissions their role requires, limiting the damage one compromised account can do |
| Encryption | Scrambles data so it is unreadable without the key, even if it is stolen |
| Physical security | Locks, alarms and controlled access stop somebody simply walking in and taking a machine |

### Two ideas that carry most of the marks

**Encryption does not stop data being stolen.** It makes stolen data useless. Saying that distinguishes a strong answer from a vague one.

**Penetration testing is authorised.** The same actions without permission are a criminal offence under the Computer Misuse Act. Questions rely on that distinction.

!key Defence in depth :: No single measure is sufficient. A firewall does not help against a user who installs a trojan, anti-malware does not help against a stolen laptop, and encryption does not help against a phished password. The answer to "how should this organisation protect itself" is always several measures, each covering a different route in.
"""),
    ],
    keyterms=[
        ("Cyber security", "The processes and technologies used to protect networks, computers, programs and data from attack and unauthorised access."),
        ("Social engineering", "Manipulating people into giving away information or access rather than attacking technology."),
        ("Blagging", "Inventing a scenario to persuade someone to give away information."),
        ("Phishing", "Sending messages that appear legitimate in order to trick the recipient into revealing details."),
        ("Pharming", "Redirecting a user to a fake website even when they type the correct address."),
        ("Shouldering", "Observing someone entering a password or PIN in order to steal it."),
        ("Malware", "Software written with the intention of causing harm."),
        ("Ransomware", "Malware that encrypts the victim's files and demands payment for the key."),
        ("Penetration testing", "Authorised simulated attacks carried out to find weaknesses before an attacker does."),
        ("Firewall", "A system that inspects traffic entering and leaving a network and blocks anything not permitted."),
        ("User access level", "The set of permissions granted to a user, limiting what they may see and do."),
        ("Encryption", "Scrambling data so that it cannot be read without the correct key."),
    ],
    grade="""
Three things lift an answer on this topic.

**Name the specific threat.** Blagging, phishing, pharming and shouldering are separate named threats, and the exam expects the right word for the scenario described.

**Say what a measure actually achieves.** Encryption does not prevent theft, it makes theft useless. A firewall does not remove malware, it blocks traffic. Access levels do not stop an account being compromised, they limit what a compromised account can reach.

**Match the measure to the threat in the question.** A question about a stolen laptop wants encryption and physical security. One about staff clicking links wants training and email filtering. Listing every measure you know earns fewer marks than choosing two and justifying them.
""",
    mistakes=[
        "Calling every attack 'hacking'. The specification names the individual threats and expects them.",
        "Saying anti-malware prevents all attacks. It detects known threats, so a brand new one may get through.",
        "Saying encryption stops data being stolen. It stops stolen data being read.",
        "Describing penetration testing as illegal hacking. It is carried out with permission, which is precisely the difference.",
        "Offering only one measure when a question asks how an organisation should protect itself. Different routes in need different defences.",
    ],
    quiz=[
        Q("A user receives an email that looks like it is from their bank, asking them to confirm their login details. What is this?", ["Phishing", "Pharming", "Blagging", "Shouldering"], 0,
          "Phishing is a message that impersonates a legitimate organisation to trick the recipient into revealing details or clicking a malicious link."),
        Q("Someone telephones an employee pretending to be from the IT department and asks for their password. What is this?", ["Blagging", "Phishing", "Pharming", "A trojan"], 0,
          "Blagging is inventing a plausible scenario to persuade a person to hand over information, and a phone call from fake IT support is the classic example."),
        Q("What distinguishes a worm from a virus?", ["A worm spreads across a network by itself without user action", "A worm encrypts files and demands payment", "A worm cannot spread between computers", "A worm only affects mobile phones"], 0,
          "A virus needs a user to open or share an infected file. A worm propagates on its own, which is why it can spread through an organisation very quickly."),
        Q("What does ransomware do?", ["Encrypts the victim's files and demands payment for the key", "Records keystrokes and sends them to an attacker", "Pretends to be legitimate software", "Redirects a user to a fake website"], 0,
          "Ransomware makes the data unusable and sells the means to restore it, which is why good backups defeat it entirely."),
        Q("Why does encryption help even if data is stolen?", ["The stolen data cannot be read without the key", "It prevents the data being copied", "It alerts the owner that data has been taken", "It deletes the data automatically"], 0,
          "Encryption does nothing to stop theft. What it does is make the stolen copy meaningless to whoever has it."),
        Q("What is the purpose of user access levels?", ["To limit what each user can see and do, so a compromised account exposes less", "To speed up logging in", "To encrypt files automatically", "To detect malware on a network"], 0,
          "Granting only the permissions a role needs means that if one account is compromised, the attacker reaches only that user's area rather than everything."),
        Q("What makes penetration testing legal when the same actions would otherwise be a crime?", ["It is carried out with the owner's authorisation", "It is done by an employee", "It only tests known weaknesses", "It does not access any real data"], 0,
          "Permission is exactly what separates penetration testing from an offence under the Computer Misuse Act."),
        Q("Why is unpatched software a serious weakness?", ["Attacks commonly exploit weaknesses that were fixed in updates the victim never installed", "Older software runs more slowly", "Unpatched software cannot use a firewall", "It uses more storage space"], 0,
          "Once a fix is published the weakness it addresses becomes public knowledge, so unpatched systems become easier targets rather than harder ones."),
        Q("What is the main purpose of a CAPTCHA?", ["To distinguish a human user from an automated script", "To encrypt a password before it is sent", "To check an email address is genuine", "To scan an uploaded file for malware"], 0,
          "CAPTCHA blocks automated bulk attacks such as mass account creation or password guessing by requiring something scripts handle poorly."),
        Q("Why is a firewall not sufficient protection on its own?", ["It cannot stop threats that do not arrive over the network, such as malware on a USB stick", "It only works on wireless networks", "It slows the network to an unusable speed", "It cannot inspect outgoing traffic"], 0,
          "A firewall inspects network traffic, so anything arriving by another route, or a user persuaded to install something themselves, is outside what it can see."),
    ],
    exam=[
        EQ("State what is meant by social engineering.", 2, [
            MP("Manipulating or tricking people rather than attacking technology", ["people", "tricking", "manipulating", "persuading", "human"]),
            MP("In order to obtain information or access", ["information", "access", "passwords", "details", "credentials"]),
        ], "Social engineering means manipulating people into giving away confidential information or access, rather than attacking the technology directly. It works because it bypasses technical protections entirely.", command="State"),
        EQ("Describe two forms of social engineering.", 4, [
            MP("Phishing, sending a message that appears to come from a legitimate organisation", ["phishing", "email", "appears legitimate", "pretends to be", "fake message"]),
            MP("The recipient is tricked into revealing details or clicking a malicious link", ["reveal", "details", "link", "login", "tricked"]),
            MP("Blagging, inventing a scenario to persuade someone to hand over information", ["blagging", "invents", "scenario", "pretends", "story", "pretext"]),
            MP("Shouldering, watching someone enter a password or PIN", ["shouldering", "watching", "over the shoulder", "observing", "pin"]),
        ], "Phishing is sending a message, usually an email or text, that appears to come from a legitimate organisation such as a bank or a school. The message creates a reason to act quickly and directs the recipient to a fake site or asks them to reply with their details, so that the attacker obtains their credentials. Blagging is different in that it is targeted and interactive: the attacker invents a plausible scenario, for example telephoning an employee while pretending to be from the IT department and claiming to need their password to fix an urgent fault, and relies on the victim wanting to be helpful and not wanting to challenge someone who sounds authoritative.", command="Describe"),
        EQ("Explain why keeping software up to date is an important cyber security measure.", 3, [
            MP("Updates fix known weaknesses in the software", ["fix", "patch", "close", "vulnerabilities", "weaknesses", "flaws"]),
            MP("Those weaknesses become public knowledge once a fix is released", ["public", "known", "published", "attackers learn"]),
            MP("So unpatched systems are easier targets, and most successful attacks exploit weaknesses that were already fixed", ["unpatched", "easier target", "already fixed", "months earlier", "most attacks"]),
        ], "Software updates exist largely to close security weaknesses that have been discovered since the software was released. Once an update is published, the existence and often the details of the weakness it fixes become public, so attackers know precisely what to look for on systems that have not applied it. That makes an unpatched system a considerably easier target than it was before the fix existed. The great majority of successful attacks do not use previously unknown flaws at all: they exploit weaknesses for which a fix had been available for months, which is why applying updates promptly, or setting them to install automatically, is one of the most effective measures available.", command="Explain"),
        EQ("A small business stores customer records on laptops that staff take home. Recommend three security measures the business should take, justifying each.", 6, [
            MP("Encrypt the data on the laptops", ["encrypt", "encryption", "scrambled"]),
            MP("So that if a laptop is lost or stolen the records cannot be read", ["stolen", "lost", "cannot be read", "unreadable", "useless"]),
            MP("Use strong passwords or biometric login on each laptop", ["strong password", "biometric", "fingerprint", "login", "authentication"]),
            MP("So that an unauthorised person cannot simply switch the laptop on and use it", ["unauthorised", "cannot log in", "prevents access", "switch on"]),
            MP("Use user access levels so each member of staff sees only what their role needs", ["access levels", "permissions", "only what they need", "restrict"]),
            MP("Keep regular backups, or keep software updated, and justify it", ["backup", "restore", "updates", "patch", "ransomware", "recover"]),
        ], "The first measure is to encrypt the data held on each laptop. A laptop taken home can be lost or stolen, and physical possession would otherwise give an attacker the entire customer database. Encryption does not prevent the theft, but it makes the stolen copy unreadable without the key, which turns a serious data breach into the loss of a piece of hardware. The second is strong authentication on each machine, either a long password meeting complexity rules or a biometric login. That stops somebody who picks the laptop up from simply switching it on and reading whatever is open, and it should be combined with a limit on failed attempts so the password cannot be guessed repeatedly. The third is user access levels, so that each member of staff has access only to the records their role actually requires. That limits the damage a single compromised account can do, and it also protects against honest mistakes. Alongside those, the business should keep regular backups held separately and ensure operating system and application updates install automatically, since backups are the only reliable defence against ransomware and updates close the weaknesses most attacks rely on.", command="Recommend"),
    ],
)


# ============================================== 3.7 relational databases and SQL

T_DATABASES = Topic(
    slug="relational-databases-and-sql",
    title="Relational Databases and SQL",
    spec="3.7",
    icon="i-memory",
    minutes=28,
    blurb="Tables, records, fields, primary and foreign keys, why splitting data across related tables removes whole categories of error, and every SQL statement the specification requires.",
    fact="SQL was designed at IBM in the 1970s to be readable by people who were not programmers, which is why it reads almost like English. That decision is the main reason it is still in daily use fifty years later.",
    sections=[
        Section("Relational database structure", """
A **database** is an organised, persistent store of data. A **relational database** stores data in linked tables.

| Term | Meaning |
| Table | A set of data about one type of thing, such as Students or Books |
| Record | One row of a table, describing one instance of that thing |
| Field | One column of a table, holding one attribute |
| Primary key | A field whose value is unique for every record, identifying that record |
| Foreign key | A field in one table that holds the primary key of a record in another table, creating the link |

### Why data is split across tables

Suppose a library keeps everything in one table, with the borrower's name and address repeated on every loan.

Three problems follow immediately, and each has a name worth using:

- **Redundancy.** The same address is stored dozens of times, wasting space.
- **Update anomalies.** When a borrower moves, every one of those copies must be changed. Miss one and the database now holds two contradictory addresses with no way to tell which is right.
- **Insertion problems.** A new borrower who has not yet taken a book out cannot be recorded at all, because there is no loan row to put them in.

Splitting the data into a Borrowers table and a Loans table solves all three. The address is stored exactly once, changing it is one edit, and a borrower can exist without any loans.

The Loans table then holds a **foreign key**, the borrower's ID, which links each loan back to exactly one borrower.

!key The one sentence justification :: Storing each fact once and linking tables by key removes redundancy and makes inconsistent data impossible, because there is only one copy to change.
"""),
        Section("SQL: retrieving data", """
**SQL**, Structured Query Language, is the language used to work with a relational database.

### SELECT

```text
SELECT firstName, surname
FROM Students
WHERE yearGroup = 11
ORDER BY surname ASC
```

- `SELECT` lists the **fields** you want. `SELECT *` means every field.
- `FROM` names the **table**.
- `WHERE` filters which **records** are returned.
- `ORDER BY` sorts the results, `ASC` for ascending and `DESC` for descending.

### Conditions in WHERE

```text
WHERE mark >= 70 AND yearGroup = 11
WHERE surname = 'Patel' OR surname = 'Khan'
WHERE title LIKE '%computing%'
```

`LIKE` with `%` as a wildcard matches part of a value, which is how you search for text containing something rather than exactly equal to it.

### Joining two tables

```text
SELECT Borrowers.surname, Loans.dueDate
FROM Borrowers, Loans
WHERE Borrowers.borrowerID = Loans.borrowerID
```

The condition matching the primary key to the foreign key is what performs the join. Leave it out and every borrower is paired with every loan, which is almost never what you want.

!warn Text values need quotation marks, numbers do not :: `WHERE surname = 'Khan'` but `WHERE yearGroup = 11`. Getting this wrong is a guaranteed lost mark.
"""),
        Section("SQL: changing data", """
### INSERT

```text
INSERT INTO Students(studentID, firstName, surname, yearGroup)
VALUES (4102, 'Amira', 'Hassan', 10)
```

The list of fields and the list of values must be in the same order and of matching types.

### UPDATE

```text
UPDATE Students
SET yearGroup = 11
WHERE yearGroup = 10
```

### DELETE

```text
DELETE FROM Students
WHERE studentID = 4102
```

!warn Never write DELETE or UPDATE without WHERE :: `DELETE FROM Students` deletes every record in the table. `UPDATE Students SET yearGroup = 11` sets every student to year 11. Both statements are valid SQL and both run instantly, which is why the WHERE clause is the most important line in either.

### Writing SQL in an exam

1. Which **table or tables** hold the data. That is your FROM.
2. Which **records** do you want. That is your WHERE.
3. Which **fields** should appear. That is your SELECT.
4. Does the order matter. That is your ORDER BY.

Answering in that order rather than left to right stops the most common error, which is selecting the right fields from the wrong table.
"""),
    ],
    keyterms=[
        ("Relational database", "A database storing data in tables that are linked to one another by keys."),
        ("Table", "A set of data about one type of thing, arranged in records and fields."),
        ("Record", "One row of a table, describing a single instance."),
        ("Field", "One column of a table, holding one attribute of every record."),
        ("Primary key", "A field whose value uniquely identifies each record in a table."),
        ("Foreign key", "A field holding the primary key of a record in another table, creating a link between them."),
        ("Redundancy", "The same data being stored more than once, wasting space and risking inconsistency."),
        ("SQL", "Structured Query Language, used to retrieve and modify data in a relational database."),
        ("Wildcard", "A symbol such as % that stands for any sequence of characters in a LIKE comparison."),
    ],
    grade="""
Two things separate full marks here.

**Justify table splitting with a named consequence.** Not "it is tidier" but "the address is stored once, so it cannot become inconsistent when a borrower moves, and a borrower can exist before they have taken out any loans".

**Write SQL that would actually run.** Quotation marks round text, none round numbers, field names spelled exactly as the question gives them, and a WHERE clause on every UPDATE and DELETE. Examiners mark SQL strictly because a query that does not run does not retrieve anything.

**Explain a foreign key as the mechanism, not the label.** It holds the primary key of a record in another table, and matching the two in a WHERE clause is what joins them.
""",
    mistakes=[
        "Putting quotation marks round numeric values, or leaving them off text values.",
        "Forgetting the WHERE clause on an UPDATE or DELETE, which affects every record in the table.",
        "Forgetting the join condition when selecting from two tables.",
        "Saying a primary key is 'the first field'. It is the field whose value is unique for every record.",
        "Confusing a record with a field. A record is a row, a field is a column.",
    ],
    quiz=[
        Q("What is a primary key?", ["A field whose value uniquely identifies each record in a table", "The first field in a table", "A field that links to another table", "The field used to sort the table"], 0,
          "The primary key must be unique for every record, which is what allows any single record to be identified without ambiguity."),
        Q("What is a foreign key?", ["A field holding the primary key of a record in another table", "A key used to encrypt the database", "The last field in a table", "A field that must be unique"], 0,
          "A foreign key is what creates the link between tables, by holding the primary key value of the related record."),
        Q("Which SQL clause filters which records are returned?", ["WHERE", "SELECT", "FROM", "ORDER BY"], 0,
          "SELECT chooses fields, FROM chooses the table, ORDER BY sorts, and WHERE decides which records qualify."),
        Q("What does SELECT * mean?", ["Return every field of the matching records", "Return every record in the database", "Multiply the values", "Return only the primary key"], 0,
          "The asterisk is a shorthand for all fields. Which records are returned is still decided by the WHERE clause."),
        Q("What is wrong with UPDATE Students SET yearGroup = 11?", ["It has no WHERE clause, so every record would be changed", "SET is not a valid keyword", "yearGroup must be in quotation marks", "UPDATE cannot be used on numbers"], 0,
          "Without a WHERE clause the statement applies to every record in the table, setting every student to year 11."),
        Q("Which query returns all books with 'python' anywhere in the title?", ["SELECT * FROM Books WHERE title LIKE '%python%'", "SELECT * FROM Books WHERE title = 'python'", "SELECT title FROM Books ORDER BY python", "SELECT * FROM Books WHERE title CONTAINS python"], 0,
          "LIKE with the percent wildcard on both sides matches any title containing that sequence of characters."),
        Q("Why is customer data split into separate tables rather than stored in one?", ["It removes redundancy and prevents the same fact becoming inconsistent", "It makes queries impossible to write", "It doubles the storage needed", "It removes the need for keys"], 0,
          "Storing each fact once means there is only one copy to update, so contradictory versions of the same data cannot arise."),
        Q("In SQL, which values need quotation marks?", ["Text values", "Numeric values", "All values", "Field names only"], 0,
          "Text is written in quotation marks and numbers are not, which is why WHERE surname = 'Khan' and WHERE yearGroup = 11 look different."),
        Q("What happens if you select from two tables without a join condition?", ["Every record from the first table is paired with every record from the second", "The query returns nothing", "SQL reports a syntax error", "Only matching records are returned automatically"], 0,
          "Without a condition matching the keys, the database produces every possible combination of rows, which is almost never what was wanted."),
        Q("Which statement adds a new record to a table?", ["INSERT INTO", "UPDATE", "SELECT", "ADD RECORD"], 0,
          "INSERT INTO with a VALUES list adds a new record. UPDATE changes existing ones."),
    ],
    exam=[
        EQ("State the difference between a primary key and a foreign key.", 2, [
            MP("A primary key uniquely identifies each record in its own table", ["unique", "identifies", "own table", "each record"]),
            MP("A foreign key holds the primary key of a record in another table, linking the two", ["another table", "link", "relates", "holds the primary key"]),
        ], "A primary key is a field whose value is unique for every record in its own table, so it identifies that record without ambiguity. A foreign key is a field in one table that holds the primary key value of a record in another table, which is what creates the link between the two tables.", command="State"),
        EQ("A Students table has the fields studentID, firstName, surname, yearGroup and tutorGroup. Write an SQL query to return the first name and surname of every student in year 11, sorted by surname.", 4, [
            MP("Selects the correct two fields", ["select firstname, surname", "firstname", "surname"]),
            MP("Uses FROM Students", ["from students"]),
            MP("Filters on yearGroup with no quotation marks round the number", ["where yeargroup = 11", "yeargroup = 11"]),
            MP("Sorts by surname", ["order by surname", "order by"]),
        ], "The query is: SELECT firstName, surname FROM Students WHERE yearGroup = 11 ORDER BY surname. The two field names appear after SELECT because only those columns are wanted, Students follows FROM because that is where the data is, the WHERE clause filters to year 11 with no quotation marks because the value is numeric, and ORDER BY surname sorts the results alphabetically, which is ascending by default.", command="Write"),
        EQ("Explain why a library database stores borrower details in a separate table from loans, rather than repeating them on every loan record.", 4, [
            MP("Repeating the details would store the same data many times, which is redundancy", ["redundancy", "repeated", "many times", "duplicated", "wastes space"]),
            MP("Wasted storage is one cost", ["storage", "space", "larger", "wasteful"]),
            MP("If a detail changes it would have to be corrected in every copy", ["every copy", "all records", "change everywhere", "update each"]),
            MP("Missing one copy would leave the database inconsistent, with no way to tell which version is right", ["inconsistent", "contradictory", "which is right", "conflict", "wrong data"]),
        ], "Repeating the borrower's name and address on every loan record means storing the same facts dozens of times over, which wastes storage but, far more importantly, creates a maintenance problem. When a borrower moves house, every single copy of their address has to be found and changed. If one is missed the database then holds two different addresses for the same person with nothing to say which is correct, and any report using the data may be wrong. Storing the borrower once in its own table and linking each loan to it by a foreign key means each fact exists in exactly one place, so a change is a single edit and inconsistency is impossible. It also allows a borrower to be recorded before they have taken out any books, which a combined table could not do.", command="Explain"),
        EQ("Write an SQL statement to change the year group of the student whose studentID is 4102 to 11.", 3, [
            MP("Uses UPDATE on the correct table", ["update students"]),
            MP("Uses SET to change yearGroup to 11", ["set yeargroup = 11", "set"]),
            MP("Includes a WHERE clause identifying the single student", ["where studentid = 4102", "where"]),
        ], "The statement is: UPDATE Students SET yearGroup = 11 WHERE studentID = 4102. The WHERE clause is essential rather than optional here: without it the statement would set the year group of every student in the table to 11, and it would do so immediately with no confirmation.", command="Write"),
    ],
)


# ============================================== 3.8 impacts of technology

T_IMPACTS = Topic(
    slug="ethical-legal-and-environmental-impacts",
    title="Ethical, Legal and Environmental Impacts",
    spec="3.8",
    icon="i-shield",
    minutes=28,
    blurb="The four Acts you must be able to name, open source against proprietary licensing, and how to structure the extended answer that carries the most marks on the paper.",
    fact="The Computer Misuse Act was passed in 1990 after two journalists accessed the Duke of Edinburgh's mailbox and could not be convicted, because at the time no law clearly covered unauthorised access to a computer.",
    sections=[
        Section("The four Acts", """
### Data Protection Act 2018

Governs how organisations handle personal data, implementing the UK's version of GDPR. It requires that data is:

- processed lawfully, fairly and transparently,
- collected for a specified purpose and not used for another,
- adequate and limited to what is necessary,
- accurate and kept up to date,
- kept no longer than necessary,
- kept secure.

It also gives individuals rights: to see the data held about them, to have inaccurate data corrected, to have data erased, and to object to certain uses.

### Computer Misuse Act 1990

Creates three offences:

1. **Unauthorised access** to computer material.
2. **Unauthorised access with intent** to commit a further offence.
3. **Unauthorised modification** of computer material, which covers deleting files and spreading malware.

The word doing the work in all three is *unauthorised*. It is why penetration testing with written permission is lawful and the same actions without it are not.

### Copyright, Designs and Patents Act 1988

Protects the creator's ownership of original work, including software, music, images and text. Copying, distributing or adapting protected work without permission is an infringement. Software is covered as a literary work, which is why licence terms have legal force.

### Software licences

**Proprietary** software is sold under a licence that restricts what you may do. The source code is not provided, you may not modify or redistribute it, and support comes from the vendor.

**Open source** software is distributed with its source code and a licence that permits use, modification and redistribution. It is usually free of charge, and support comes from the community rather than a company.

| | Proprietary | Open source |
| Source code | Not available | Available |
| Modification | Not permitted | Permitted |
| Cost | Usually paid | Usually free |
| Support | From the vendor, often guaranteed | From the community, no guarantee |
| Security | Fewer people can inspect it | Anyone can inspect it, but anyone can also find flaws |

!warn Open source does not mean free of charge :: It means the source is open. Some open source software is sold, and much free software is not open source. The exam distinguishes them.
"""),
        Section("Ethical and environmental issues", """
The specification names a set of technologies and expects you to discuss their impacts.

**Cyber security and hacking.** Attacks cost organisations money and cost individuals their privacy. The same skills used to defend systems are used to attack them, which is why authorisation is the ethical line.

**Mobile technologies and wireless networking.** They allow work and contact from anywhere, which brings flexibility but also the expectation of being permanently available. Wireless coverage is uneven, so those in poorer or more rural areas get a worse service, which is one form of the digital divide.

**Cloud storage.** Convenient, backed up and reachable from anywhere, but it places personal data in the hands of a company that may be in another country under different laws, and it is unusable without a connection.

**Wearable technologies and computer based implants.** A fitness tracker or a smart insulin pump can improve health and independence enormously. Both also generate a continuous record of a person's body, which raises questions about who may see it, how long it is kept and what happens if it is breached or if a device fails.

**Autonomous vehicles.** They could reduce collisions caused by human error and give mobility to people who cannot drive. They also raise questions about liability when one crashes, about the loss of driving jobs, and about how a vehicle should be programmed to behave in a situation where harm is unavoidable.

### Environmental impacts

- Manufacturing devices consumes rare metals, extracted with significant environmental and human cost.
- Data centres consume very large amounts of electricity for both power and cooling.
- Electronic waste is often exported and dismantled unsafely, releasing toxic material.
- Against that: video conferencing removes journeys, smart systems reduce energy use, and digital documents remove paper.
"""),
        Section("Writing the extended answer", """
The impacts question carries the largest single mark allocation on the paper, and it is marked by levels rather than by counting points.

**Structure that reliably reaches the top band:**

1. **Set out the situation in one sentence.** Show you understand what is being asked.
2. **Give the case for.** Two or three developed points, each with a consequence: not "it is convenient" but "it is convenient, which means staff can work from home and the company needs less office space".
3. **Give the case against.** The same standard of development. This is where most answers thin out.
4. **Say who is affected.** Different stakeholders want different things. The company, the customer, the employee and the wider public rarely agree, and naming that tension is what level three answers do.
5. **Reach a conclusion and justify it.** A conclusion is not a summary. It is a judgement, and it must follow from what you actually wrote.

!exam A conclusion is compulsory :: An answer with excellent arguments and no conclusion cannot reach the top band, because the question asked you to evaluate and you did not. One sentence beginning "On balance" is enough, provided it commits.

!key Use the named categories :: Ethical, legal, cultural, environmental and privacy. Explicitly labelling which one each of your points falls under makes the range of your answer visible to the examiner in a way that prose alone does not.
"""),
    ],
    keyterms=[
        ("Data Protection Act 2018", "Legislation governing how organisations collect, store and use personal data."),
        ("Computer Misuse Act 1990", "Legislation creating offences of unauthorised access to and modification of computer material."),
        ("Copyright, Designs and Patents Act 1988", "Legislation protecting the creator's ownership of original work, including software."),
        ("Proprietary software", "Software supplied without source code under a licence restricting modification and redistribution."),
        ("Open source software", "Software supplied with its source code under a licence permitting use, modification and redistribution."),
        ("Digital divide", "The gap between those with good access to technology and those without."),
        ("Electronic waste", "Discarded electronic equipment, which contains toxic materials and is often disposed of unsafely."),
        ("Stakeholder", "A person or group affected by a decision or a technology."),
    ],
    grade="""
This topic is where the largest marks are, and where the most are thrown away.

**Develop every point.** A claim is half a mark. A claim with a consequence is a whole one. Get into the habit of writing "which means" after every assertion.

**Name the Act, do not describe it vaguely.** "This would be an offence under the Computer Misuse Act 1990, specifically unauthorised access to computer material" is precise. "It is illegal" is not.

**Argue both sides even when you have a clear view.** An answer that only argues one way cannot reach the top band however well written it is, because evaluation requires weighing.

**Conclude, and make the conclusion follow.** The examiner is looking for a judgement supported by your own argument, not a restatement of the question.
""",
    mistakes=[
        "Saying open source means free of charge. It means the source code is available.",
        "Giving one sided answers to an evaluate question, which caps the mark however good the writing is.",
        "Listing impacts without developing any of them into consequences.",
        "Confusing the Acts. Personal data is the Data Protection Act, unauthorised access is the Computer Misuse Act, copying software is the Copyright Act.",
        "Ending an extended answer without a conclusion.",
    ],
    quiz=[
        Q("Under which Act would a person be prosecuted for accessing a computer system without permission?", ["Computer Misuse Act 1990", "Data Protection Act 2018", "Copyright, Designs and Patents Act 1988", "Freedom of Information Act 2000"], 0,
          "Unauthorised access to computer material is the first offence created by the Computer Misuse Act."),
        Q("Which Act gives you the right to see the personal data an organisation holds about you?", ["Data Protection Act 2018", "Computer Misuse Act 1990", "Copyright, Designs and Patents Act 1988", "Consumer Rights Act 2015"], 0,
          "The right of access is one of the individual rights created by data protection law."),
        Q("What is the defining feature of open source software?", ["The source code is available and may be modified and redistributed", "It is always free of charge", "It has no licence conditions at all", "It cannot be used commercially"], 0,
          "Openness of the source and the freedom to modify and redistribute are the defining features. Cost is a separate matter."),
        Q("What is a disadvantage of open source software for a business?", ["Support comes from the community, with no guaranteed response", "It cannot be modified to suit the business", "The source code is hidden", "It is always more expensive"], 0,
          "A business that needs a guaranteed fix within a set time may prefer a vendor contract, which community support cannot promise."),
        Q("Copying and selling software without the owner's permission would breach which Act?", ["Copyright, Designs and Patents Act 1988", "Computer Misuse Act 1990", "Data Protection Act 2018", "Trade Descriptions Act 1968"], 0,
          "Software is protected as a literary work under copyright law, so copying and distributing it without permission is an infringement."),
        Q("What is meant by the digital divide?", ["The gap between those with good access to technology and those without", "The difference between analogue and digital signals", "The split between hardware and software", "The gap between mobile and desktop users"], 0,
          "Uneven access to devices, connectivity and skills means technology does not benefit everyone equally, which is what the term describes."),
        Q("Which is an environmental disadvantage of cloud storage?", ["Data centres consume large amounts of electricity for power and cooling", "It requires users to buy more hard drives", "It increases the amount of paper used", "It cannot be recycled"], 0,
          "The energy used to run and cool very large data centres is the main environmental cost of moving storage to the cloud."),
        Q("Why is authorisation the key word in the Computer Misuse Act?", ["It is what separates lawful security testing from a criminal offence", "It refers to the strength of the password used", "It means the data must be encrypted", "It applies only to government systems"], 0,
          "All three offences turn on access being unauthorised, which is exactly why penetration testing is carried out under written permission."),
        Q("An ethical concern about autonomous vehicles is:", ["Deciding who is liable when the vehicle causes a collision", "That they use more fuel than human drivers", "That they cannot be manufactured", "That they require a driving licence"], 0,
          "Responsibility for a collision is genuinely unresolved when no human was driving, which makes it an ethical and legal question rather than a technical one."),
        Q("What must an extended evaluate answer include to reach the top band?", ["Developed arguments on both sides and a justified conclusion", "As many separate points as possible", "Only the advantages, argued strongly", "A list of relevant Acts"], 0,
          "Evaluation means weighing both sides and then committing to a judgement supported by the argument you made."),
    ],
    exam=[
        EQ("State two rights that the Data Protection Act 2018 gives an individual.", 2, [
            MP("The right to see the data held about them", ["see", "access", "view", "copy of", "find out"]),
            MP("The right to have inaccurate data corrected, or to have data erased", ["corrected", "rectified", "erased", "deleted", "removed", "put right"]),
        ], "An individual has the right to see the personal data an organisation holds about them, and the right to have inaccurate data corrected. They also have the right to have data erased where there is no longer a good reason to keep it, and to object to certain uses such as marketing.", command="State"),
        EQ("Explain one advantage and one disadvantage of a school using open source software rather than proprietary software.", 4, [
            MP("Open source software is usually free of licence cost", ["free", "no licence", "cost", "cheaper", "no fee"]),
            MP("Which allows the school to spend the money on something else, or install it on any number of machines", ["saves money", "any number", "more machines", "spend elsewhere", "budget"]),
            MP("Support comes from the community rather than a vendor", ["community", "no vendor", "forums", "no company"]),
            MP("So there is no guaranteed response time if something goes wrong, and staff may need more technical skill", ["no guarantee", "response time", "slower", "technical skill", "no support contract", "on their own"]),
        ], "The advantage is cost and freedom of installation. Open source software is normally free of licence charges and may be installed on any number of machines without counting them, so a school can equip an entire suite for nothing and spend the saved budget elsewhere. It can also be modified if the school has the expertise, for example to remove features that confuse younger pupils. The disadvantage is support. Proprietary software is usually backed by a vendor with a support contract and a guaranteed response time, whereas open source support comes from community forums and volunteers with no obligation to respond at all. If something breaks the week before an exam, the school is dependent on its own technical staff, and that risk is exactly what many organisations pay a licence fee to avoid.", command="Explain"),
        EQ("A company plans to monitor its employees' work laptops, recording every website visited and every key pressed. Discuss the ethical and legal issues this raises.", 8, [
            MP("The company has legitimate reasons, such as protecting data and preventing misuse", ["protect", "security", "misuse", "legitimate", "data", "productivity"]),
            MP("Monitoring can detect an attack or a leak early", ["detect", "early", "leak", "attack", "breach", "evidence"]),
            MP("Employees have a reasonable expectation of privacy, particularly for incidental personal use", ["privacy", "personal", "expectation", "private messages", "intrusive"]),
            MP("Keystroke logging could capture personal passwords and private information", ["passwords", "personal", "banking", "private", "capture", "sensitive"]),
            MP("The Data Protection Act requires processing to be lawful, fair, transparent and proportionate", ["data protection", "lawful", "fair", "transparent", "proportionate", "necessary"]),
            MP("Employees would have to be informed, and the data secured and kept only as long as needed", ["informed", "told", "notified", "secured", "not kept", "policy"]),
            MP("Monitoring can damage trust and morale, and change how people behave at work", ["trust", "morale", "surveillance", "stress", "behaviour", "relationship"]),
            MP("Reaches a justified conclusion, such as proportionate monitoring with clear notice", ["conclusion", "on balance", "proportionate", "should", "therefore", "recommend"]),
        ], "The company has a genuine case. It is responsible for the data on those laptops and can be held to account if that data is lost, so being able to see when a large file is copied to an unauthorised location or when an employee visits a site known to distribute malware allows a problem to be caught early rather than discovered months later. Monitoring also provides evidence if misuse is alleged, which protects the accused employee as much as the company. Against that, employees have a reasonable expectation of privacy even on a work device, because in practice almost every organisation tolerates some incidental personal use, and a keystroke logger does not distinguish between a work document and a personal banking password typed at lunchtime. Capturing credentials for systems the company has no business seeing is a serious intrusion, and it also creates a new risk: the company now holds a store of passwords that would be extremely damaging if it were breached. Legally the Data Protection Act requires that processing personal data is lawful, fair, transparent and proportionate to a specified purpose. Recording every keystroke is very difficult to defend as proportionate when a narrower measure, such as logging access to sensitive files, would achieve the same aim. Employees would have to be told clearly what is recorded and why, the data would have to be kept securely and deleted when no longer needed, and the company would need to be able to justify the necessity of each element. There is also a cultural cost that is easy to overlook. Comprehensive surveillance signals distrust, and organisations that adopt it often find that morale falls and that people become cautious rather than productive. On balance, the company should not implement keystroke logging. It should adopt proportionate monitoring focused on the specific risk it is trying to manage, such as logging access to confidential systems and blocking known malicious sites, set it out in a written policy that every employee is shown and asked to acknowledge, restrict who can see the logs, and delete them on a defined schedule. That protects the company's data and its legal position while remaining defensible as necessary and proportionate.", command="Discuss"),
    ],
)


# ================================================================== COURSE

COURSE = Course(
    slug="ks4/aqa-computer-science",
    title="AQA GCSE Computer Science",
    short="AQA GCSE CS",
    stage="KS4",
    board="AQA",
    code="8525",
    goal="Grade 9",
    icon="i-cpu",
    accent="var(--purple)",
    blurb="Every section of the AQA 8525 specification, from 3.1 fundamentals of algorithms through to 3.8 impacts, written to AQA's own conventions: AQA pseudo-code, AQA's decimal units, and Huffman and RLE worked through in full.",
    intro="",
    journey=[
        ("Know which board you are sitting",
         "AQA and OCR cover similar computer science but they are not interchangeable. AQA uses its own pseudo-code, counts a kilobyte as 1000 bytes, examines star and bus topologies rather than star and mesh, and requires Huffman coding and run length encoding in detail. Work from the right course and none of that catches you out.", ""),
        ("Read a topic once, then close it",
         "Write down everything you can remember before you look again. What you cannot produce from memory is what you have not learned yet, and rereading will never show you the difference.", ""),
        ("Score full marks on the knowledge check",
         "Ten questions per topic with an explanation for every answer. Anything below ten out of ten is a signal to go back to that section rather than to move on.", ""),
        ("Write the exam answers before reading the model",
         "Every topic ends with exam-style questions marked against real mark scheme points. Produce your answer first. Reading a model answer feels productive and teaches you very little until you have attempted one yourself.", ""),
        ("Practise the calculations until they are automatic",
         "Number bases, binary addition and shifts, file sizes, Huffman savings. These are the most reliable marks on Paper 1 and they are entirely method. Use the tools on this site until you stop having to think about them.", ""),
        ("Sit whole papers to time, then fix what you dropped",
         "Paper 1 is 2 hours of computational thinking and programming, Paper 2 is 1 hour 45 of computing concepts. Mark honestly, list every mark you lost and why, and revise from that list rather than from the specification.", ""),
    ],
    units=[
        Unit("fundamentals-of-algorithms", "3.1 Fundamentals of Algorithms",
             "What an algorithm is, how to express one in pseudo-code and as a flowchart, and the four searching and sorting algorithms AQA names.",
             [T_COMPTHINK, T_REPRESENT, T_SEARCH, T_SORT], icon="i-brain", term="Paper 1"),
        Unit("programming", "3.2 Programming",
             "Everything from data types and the three constructs to arrays, files, subroutines, robust programming and the languages themselves.",
             [T_PROGFUND, T_DATASTRUCT, T_SUBROUTINES, T_ROBUST, T_LANGUAGES],
             icon="i-python", term="Paper 1"),
        Unit("data-representation", "3.3 Fundamentals of Data Representation",
             "Number bases and units, binary arithmetic and shifts, characters, images, sound, and compression including Huffman and run length encoding.",
             [T_NUMBASES, T_BINARITH, T_CHARS, T_IMAGES, T_SOUND, T_COMPRESS],
             icon="i-binary", term="Paper 2"),
        Unit("computer-systems", "3.4 Computer Systems",
             "Hardware and software, the operating system and utilities, Boolean logic, and the architecture of the processor itself.",
             [T_HWSW, T_LOGIC, T_ARCH], icon="i-layers", term="Paper 2"),
        Unit("computer-networks", "3.5 Fundamentals of Computer Networks",
             "Local and wide area networks, star and bus topologies, wired against wireless, every named protocol, and why networking is layered.",
             [T_NETWORKS, T_PROTOCOLS], icon="i-network", term="Paper 2"),
        Unit("cyber-security", "3.6 Cyber Security",
             "Social engineering and malicious code threat by threat, and every method of detection and prevention in the specification.",
             [T_CYBER], icon="i-shield", term="Paper 2"),
        Unit("databases", "3.7 Relational Databases and SQL",
             "Tables, records, fields and keys, why data is split across linked tables, and writing SQL that would actually run.",
             [T_DATABASES], icon="i-memory", term="Paper 2"),
        Unit("impacts", "3.8 Ethical, Legal and Environmental Impacts",
             "The four Acts, software licensing, the impacts of the technologies AQA names, and how to structure the extended answer.",
             [T_IMPACTS], icon="i-shield", term="Paper 2"),
    ],
)
