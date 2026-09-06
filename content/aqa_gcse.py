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
