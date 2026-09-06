"""Key Stage 3 Computing revision content.

Follows the department long term plan for Years 7, 8 and 9, covering the three
strands of the national curriculum: computer science, information technology
and digital literacy.
"""
from mskbuild.models import Topic, Section, Unit, Course, Q, EQ, MP

# ============================================================ YEAR 7

Y7_USING = Topic(
    slug="using-computers",
    title="Using Computers",
    spec="Y7.1",
    icon="i-software",
    minutes=22,
    blurb="Hardware and software, input and output, file management and staying safe and organised on a school network.",
    fact="The first computer mouse, built in 1964, was a wooden box with two metal wheels. Its inventor Douglas Engelbart never earned a penny from it, because the patent expired before mice became common.",
    sections=[
        Section("Hardware and software", """
Every computer is made of two things working together.

**Hardware** is the physical parts you can touch: the screen, keyboard, processor, memory and hard drive.

**Software** is the instructions that tell the hardware what to do. You cannot touch software. It is stored as data.

### Two kinds of software

- **System software** runs the computer itself. The operating system, such as Windows, macOS, Linux, Android or iOS, is the most important example.
- **Application software** lets you do a task: a browser, a word processor, a game, a photo editor.

!key A useful test :: If you would install it to get a job done, it is an application. If the computer needs it to work at all, it is system software.

### Input, process, output, storage

Every computer system follows the same pattern.

| Stage | What happens | Examples |
| Input | Data goes in | Keyboard, mouse, microphone, camera, sensor, scanner |
| Process | The CPU works on the data | Calculating, sorting, comparing |
| Output | Results come out | Monitor, speaker, printer, motor, light |
| Storage | Data is kept for later | Hard drive, SSD, USB stick, cloud |

A digital camera takes light in (input), turns it into an image (process), shows it on the screen (output) and saves it to a card (storage).
"""),
        Section("Files and folders", """
Files get lost when they have no system. A good system takes seconds to set up and saves hours later.

### File names

- Use names that say what the file is: `year7-homework-networks.docx`, not `doc1.docx`
- Avoid spaces at the start and unusual symbols
- Keep the **file extension**, the bit after the dot, because it tells the computer which program opens it

| Extension | Type of file |
| .docx | Word processed document |
| .xlsx | Spreadsheet |
| .pptx | Presentation |
| .png .jpg | Image |
| .mp3 .wav | Sound |
| .mp4 | Video |
| .py | Python program |
| .txt | Plain text |
| .pdf | Portable document |

### Folder structure

Folders inside folders make a **hierarchy**. Group by subject, then by topic:

    Documents
      Computing
        Year 7
          Networks
          Python
      English

### Saving

- **Save As** creates a new copy with a new name. Use it to keep versions.
- **Save** overwrites the file you already have.
- Save often. Work only exists once it has been written to storage, because RAM is wiped when the power goes.
"""),
        Section("Staying safe and being organised", """
### Passwords

A strong password is **long** and **not guessable**.

- Three unrelated words joined together are strong and easy to remember: `copper-badger-lantern`
- Avoid your name, your birthday, your pet, and anything on your social media
- Never use the same password for two important accounts
- Never share your password, not even with a friend

### On the school network

- Your account is **yours**. Anything done while logged in as you looks like you did it, so always log off.
- Files on the network are usually backed up. Files on a USB stick are not.
- Your school can see what you do on its network. That is not spying, it is safeguarding.

### Being a decent person online

- Anything you post can be screenshotted and kept forever, even on apps that promise otherwise
- If you would not say it to someone's face in front of a teacher, do not type it
- If something online makes you uncomfortable, tell an adult. You will not be in trouble for reporting.
"""),
    ],
    keyterms=[
        ("Hardware", "The physical parts of a computer system that you can touch."),
        ("Software", "The programs and instructions that tell the hardware what to do."),
        ("Operating system", "The system software that manages the computer and lets you run programs."),
        ("Input device", "Hardware that puts data into a computer, such as a keyboard or a sensor."),
        ("Output device", "Hardware that gets results out of a computer, such as a monitor or a speaker."),
        ("File extension", "The letters after the dot in a file name that tell the computer what type of file it is."),
        ("Hierarchy", "A structure of folders inside folders used to organise files."),
    ],
    grade="""
To reach the top level at Key Stage 3 on this unit, you need to do more than name parts.

**Classify with a reason.** A touchscreen is both an input device and an output device, because it displays information and detects where you touch. Saying that shows real understanding.

**Explain what would go wrong.** Why does a computer need storage as well as memory? Because memory is wiped when the power goes, so without storage all your work would disappear every time you switched off.

**Apply file organisation to a real situation.** Given a messy list of files, group them sensibly and explain your grouping.

+ Sort any device into input, output, storage or processing, and justify it
+ Explain the difference between Save and Save As and when to use each
+ Design a folder structure for a set of school subjects
+ Explain what makes a password strong, using an example
""",
    mistakes=[
        "Calling the whole computer 'the hard drive'. The hard drive is only the storage.",
        "Saying a printer is an input device. It takes data out of the computer, so it is output.",
        "Deleting a file extension when renaming a file, which stops the computer knowing how to open it.",
        "Thinking that closing a program saves your work. It does not unless you tell it to.",
    ],
    quiz=[
        Q("Which of these is hardware?", ["A keyboard", "A web browser", "An operating system", "A Python program"], 0,
          "Hardware is any physical part you can touch. The other three are all software."),
        Q("Which is an example of system software?",
          ["The operating system", "A photo editor", "A web browser", "A game"], 0,
          "System software runs the computer itself. The others are applications you install to do a task."),
        Q("A microphone is which kind of device?",
          ["Input", "Output", "Storage", "Processing"], 0,
          "It captures sound and puts that data into the computer, so it is an input device."),
        Q("What does the file extension .py tell you?",
          ["It is a Python program", "It is a picture", "It is a presentation", "It is a spreadsheet"], 0,
          "The extension tells the computer which program should open the file."),
        Q("Why should you save your work regularly?",
          ["Work in memory is lost if the power goes off",
           "Saving makes the computer faster",
           "Files get smaller each time you save",
           "It stops other people opening your file"], 0,
          "RAM is wiped when the power is removed, so anything not written to storage disappears."),
        Q("Which of these is the strongest password?",
          ["copper-badger-lantern", "password123", "Sam2011", "qwerty"], 0,
          "Three unrelated words make a long password that is hard to guess but easy for you to remember."),
        Q("A touchscreen is:",
          ["Both an input and an output device", "Only an input device",
           "Only an output device", "A storage device"], 0,
          "It displays information, which is output, and detects where you touch, which is input."),
        Q("What is the correct order of the four stages of a computer system?",
          ["Input, process, output, with storage available throughout",
           "Output, process, input, storage",
           "Process, input, storage, output",
           "Storage, output, input, process"], 0,
          "Data goes in, is worked on, results come out, and storage keeps data for later at any stage."),
        Q("What does Save As do that Save does not?",
          ["It creates a new copy with a new name", "It makes the file smaller",
           "It closes the program", "It prints the file"], 0,
          "Save As is how you keep versions, because the original file stays exactly as it was."),
        Q("Why should you always log off a school computer?",
          ["Anything done while logged in as you appears to have been done by you",
           "It saves electricity", "It deletes your files", "It speeds up the network"], 0,
          "Your account is your identity on the network, and leaving it open lets someone else act as you."),
    ],
    exam=[
        EQ("State one difference between hardware and software.", 2, [
            MP("Hardware is the physical parts you can touch", ["physical", "touch", "parts", "components"]),
            MP("Software is the programs or instructions that tell the hardware what to do", ["programs", "instructions", "code", "tell it what to do", "cannot touch"]),
        ], "Hardware is the physical parts of a computer system that you can actually touch, such as the keyboard, monitor and processor. Software is the set of programs and instructions that tell the hardware what to do, and it cannot be touched because it is stored as data.",
           command="State"),
        EQ("Name two input devices and two output devices, and state what each is used for.", 4, [
            MP("First input device named with a use", ["keyboard", "mouse", "microphone", "scanner", "camera", "sensor"]),
            MP("Second input device named with a use", ["keyboard", "mouse", "microphone", "scanner", "camera", "sensor"]),
            MP("First output device named with a use", ["monitor", "screen", "printer", "speaker", "headphones"]),
            MP("Second output device named with a use", ["monitor", "screen", "printer", "speaker", "headphones", "motor"]),
        ], "Two input devices are a keyboard, which is used to type text and numbers into the computer, and a microphone, which is used to record sound. Two output devices are a monitor, which displays images and text so the user can see the results, and a printer, which produces a paper copy of a document.",
           command="Name"),
        EQ("Explain why a computer needs storage as well as memory.", 3, [
            MP("Memory is wiped when the power is switched off", ["wiped", "lost", "erased", "power", "switched off", "volatile"]),
            MP("Storage keeps data permanently", ["permanently", "keeps", "saved", "stays", "not lost"]),
            MP("Without storage all work would be lost every time the computer was turned off", ["lost", "every time", "start again", "gone"]),
        ], "A computer needs memory to hold the programs and data it is working with right now, but memory is wiped as soon as the power is switched off. Storage keeps data permanently, so it is still there the next time the computer is turned on. Without storage, every document, photo and program would be lost every time the computer was shut down and everything would have to be created again from scratch.",
           command="Explain"),
        EQ("A student has saved all their work in one folder with names like doc1, doc2 and doc3. Describe two problems this causes and suggest how they should organise their files instead.", 4, [
            MP("It is hard to find a particular file", ["find", "search", "locate", "hard to", "difficult"]),
            MP("The names do not say what the files contain", ["do not say", "no idea", "meaningless", "unclear", "what it is"]),
            MP("Suggests using meaningful file names", ["meaningful", "descriptive", "sensible names", "say what"]),
            MP("Suggests using folders for different subjects or topics", ["folders", "subfolders", "subjects", "topics", "organise"]),
        ], "The first problem is that the student cannot tell what any file contains without opening it, because names like doc1 give no information at all. The second problem is that with everything in one folder, finding a particular piece of work means scrolling through a long list, and this gets worse every week as more files are added. Instead the student should give each file a meaningful name that describes it, such as year7-computing-networks-homework, and create a folder structure with a folder for each subject and subfolders inside for each topic, so that related work is grouped together and easy to find.",
           command="Describe"),
        EQ("Explain what makes a password strong, and give an example of a strong password.", 3, [
            MP("It should be long", ["long", "length", "many characters", "at least"]),
            MP("It should not be guessable from personal information", ["guess", "personal", "name", "birthday", "pet", "not obvious"]),
            MP("Gives a suitable example", ["example", "three words", "random", "mix", "unrelated"]),
        ], "A strong password is long, because every extra character makes it far harder for a computer to guess by trying every combination. It should also not contain anything someone could find out about you, such as your name, your date of birth or the name of your pet, because those are the first things an attacker would try. A good method is to join three unrelated words together, for example copper-badger-lantern, which is long and very difficult to guess but still easy for you to remember.",
           command="Explain"),
    ],
)

Y7_SCRATCH = Topic(
    slug="programming-in-scratch",
    title="Programming Essentials in Scratch",
    spec="Y7.2",
    icon="i-play",
    minutes=24,
    blurb="Sequence, selection and iteration using blocks, plus variables and events. Everything you learn here transfers directly to Python.",
    fact="Scratch was made at MIT and released in 2007. It now has over 100 million registered projects, which makes it one of the largest collections of programs ever written by children anywhere in the world.",
    sections=[
        Section("Sequence", """
A **sequence** is a set of instructions carried out **in order**, one after another.

Computers are extremely literal. They do exactly what you say, in exactly the order you say it, which is why a program that seems obviously correct can still do something ridiculous.

    when green flag clicked
    say "Hello!" for 2 seconds
    move 100 steps
    turn 90 degrees
    move 100 steps

Swap two of those blocks and the sprite ends up somewhere completely different.

!key Order is part of the instruction :: Putting the right steps in the wrong order is just as wrong as having the wrong steps.
"""),
        Section("Selection and variables", """
### Selection

**Selection** means the program **chooses** what to do based on a condition.

    if <touching edge?> then
        turn 180 degrees

    if <score > 10> then
        say "You win!"
    else
        say "Keep going"

The `if ... else` block gives two paths. Only one of them runs.

### Conditions

A condition is a question with a yes or no answer:

- `touching edge?`
- `key space pressed?`
- `score > 10`
- `answer = "blue"`

### Variables

A **variable** is a named box that stores a value which can change while the program runs.

    set score to 0
    change score by 1
    set lives to 3
    change lives by -1

Common uses: score, lives, timer, player name, level number.

!warn Set your variables at the start :: If you do not `set score to 0` when the green flag is clicked, the score carries over from the last time you played, which is one of the most common bugs in Scratch projects.
"""),
        Section("Iteration and events", """
### Iteration

**Iteration** means **repeating** instructions. Scratch has three loop blocks.

| Block | What it does |
| `repeat 10` | Runs exactly 10 times, a count controlled loop |
| `forever` | Runs until the program is stopped |
| `repeat until <condition>` | Runs until the condition becomes true |

Drawing a square:

    repeat 4
        move 100 steps
        turn 90 degrees

Four sides, four identical steps. Writing it out four times would work, but the loop is shorter, clearer and easier to change into a pentagon.

### Events

An **event** starts a script when something happens.

- `when green flag clicked`
- `when space key pressed`
- `when this sprite clicked`
- `when I receive [message]`

**Broadcasting** lets one sprite tell another sprite to do something, which is how sprites work together in a game.

### Debugging

When a Scratch program does not work:

1. Check the **order** of the blocks
2. Check every **variable is set** at the start
3. Check the **condition** is the right way round, for example `>` where you meant `<`
4. Check the script is attached to the **right sprite**
5. Click blocks individually to see what each one actually does
"""),
    ],
    keyterms=[
        ("Algorithm", "A set of step by step instructions for solving a problem."),
        ("Sequence", "Instructions carried out one after another in order."),
        ("Selection", "Choosing what to do based on whether a condition is true."),
        ("Iteration", "Repeating a set of instructions."),
        ("Variable", "A named store for a value that can change while the program runs."),
        ("Condition", "A question with a true or false answer, used to make a decision."),
        ("Event", "Something that happens, such as a key press, that starts a script."),
        ("Sprite", "An object in Scratch that can be moved, costumed and given its own scripts."),
        ("Broadcast", "A message one sprite sends so that other sprites can respond."),
        ("Debugging", "Finding and fixing errors in a program."),
    ],
    grade="""
The top level at Key Stage 3 is about **explaining choices**, not just making things work.

**Say which construct you used and why.** "I used a repeat until loop rather than a repeat 10 loop, because the player might reach the target at any time and I do not know how many attempts they will need."

**Predict before you run.** Read a script and say what it will do before clicking the green flag. Being able to predict is what shows you understand it rather than having got there by trial and error.

**Debug systematically.** Do not just move blocks around until it works. Say what you expected, what actually happened, and what that difference tells you about where the fault is.

+ Explain the difference between repeat, forever and repeat until, with an example use for each
+ Predict the output of a script containing a loop and an if block
+ Explain why a variable must be reset at the start of a game
+ Find and describe a fault in a given script
""",
    mistakes=[
        "Forgetting to set variables back to their starting value when the green flag is clicked.",
        "Using forever when the loop needs to stop, so the rest of the script never runs.",
        "Attaching a script to the wrong sprite and then wondering why nothing happens.",
        "Putting the if block outside the loop when it needs to be checked on every repeat.",
        "Getting a condition the wrong way round, such as using less than when greater than was meant.",
    ],
    quiz=[
        Q("Which construct means repeating instructions?",
          ["Iteration", "Selection", "Sequence", "Variable"], 0,
          "Iteration is repetition. Selection is choosing, and sequence is order."),
        Q("What does `repeat until <touching edge?>` do?",
          ["Repeats the blocks inside until the sprite touches the edge",
           "Repeats exactly ten times",
           "Repeats forever",
           "Runs once when the edge is touched"], 0,
          "It keeps repeating while the condition is false, and stops as soon as it becomes true."),
        Q("Why should a score variable be set to 0 when the green flag is clicked?",
          ["Otherwise the score from the previous game carries over",
           "Otherwise the program will not run",
           "To make the game faster",
           "To create the variable"], 0,
          "Variables keep their value between runs, so without resetting, the new game starts with the old score."),
        Q("Which blocks would draw a triangle?",
          ["repeat 3 [move 100 steps, turn 120 degrees]",
           "repeat 4 [move 100 steps, turn 90 degrees]",
           "repeat 3 [move 100 steps, turn 90 degrees]",
           "forever [move 100 steps, turn 120 degrees]"], 0,
          "A triangle has three sides and the sprite must turn through 360 degrees in total, so 360 divided by 3 gives 120 degrees each time."),
        Q("What is an event in Scratch?",
          ["Something that happens which starts a script, such as a key press",
           "A variable that stores a number",
           "A loop that repeats forever",
           "An error in the program"], 0,
          "Event blocks are the hat blocks at the top of scripts, and they decide when a script begins."),
        Q("Which condition would check that a player has more than 5 lives?",
          ["lives > 5", "lives < 5", "lives = 5", "lives > 5 or lives < 5"], 0,
          "The greater than sign tests whether the value is above 5, not including 5 itself."),
        Q("What does broadcasting allow you to do?",
          ["Send a message so other sprites can respond",
           "Save the project online",
           "Make the sprite move faster",
           "Change the background colour"], 0,
          "Broadcasting is how sprites coordinate, for example one sprite finishing so another can start."),
        Q("A sprite should bounce when it hits the edge. Which construct is needed?",
          ["Selection, to check whether it is touching the edge",
           "Only sequence", "Only a variable", "Only an event"], 0,
          "You need an if block to test the condition, and it needs to be inside a loop so the check happens continuously."),
        Q("What is debugging?",
          ["Finding and fixing errors in a program", "Adding more sprites",
           "Making a program run faster", "Saving a project"], 0,
          "Debugging is systematic fault finding, not random rearranging of blocks."),
        Q("Which loop should be used when you do not know how many repetitions are needed?",
          ["repeat until", "repeat 10", "A single if block", "No loop is needed"], 0,
          "Repeat until keeps going for as long as it takes, which is exactly what an unknown number of repetitions requires."),
    ],
    exam=[
        EQ("State what is meant by sequence, selection and iteration.", 3, [
            MP("Sequence is instructions carried out in order one after another", ["order", "one after", "sequence", "step by step"]),
            MP("Selection is choosing what to do based on a condition", ["choose", "condition", "decision", "if", "depends"]),
            MP("Iteration is repeating instructions", ["repeat", "repeating", "loop", "again"]),
        ], "Sequence means carrying out instructions one after another in the order they are written. Selection means the program chooses between different paths depending on whether a condition is true or false, using an if block. Iteration means repeating a set of instructions, either a fixed number of times or until a condition is met.",
           command="State"),
        EQ("Explain why a variable is useful in a game, giving an example.", 3, [
            MP("A variable stores a value that can change while the program runs", ["stores", "value", "changes", "holds"]),
            MP("Gives a valid example such as score, lives or a timer", ["score", "lives", "timer", "level", "health"]),
            MP("Explains how it is used, such as increasing the score when a target is hit", ["change by", "increase", "add", "when", "each time"]),
        ], "A variable is a named store that holds a value which can change while the program is running, which is exactly what a game needs to keep track of what is happening. For example, a score variable would be set to 0 when the green flag is clicked, and then changed by 1 every time the player catches a falling object. The current value can then be checked in a condition, so the game can end or move to the next level when the score reaches a target.",
           command="Explain"),
        EQ("A student's Scratch game keeps the score from the previous game when it is restarted. Explain the cause of this problem and how to fix it.", 3, [
            MP("Variables keep their value between runs", ["keep", "remember", "stays", "carries over", "not reset"]),
            MP("The score is never set back to zero when the game starts", ["not set", "no set to 0", "never reset", "missing"]),
            MP("Fix by adding a set score to 0 block after the green flag is clicked", ["set score to 0", "set to 0", "green flag", "at the start", "reset"]),
        ], "The cause is that a variable keeps whatever value it was last given, and that value is remembered even after the program stops. Because the student's script never sets the score back to zero, the new game simply continues from the value left over at the end of the previous one. The fix is to add a set score to 0 block immediately after the when green flag clicked block, so that the score is reset every time a new game begins.",
           command="Explain"),
        EQ("Describe how you would use a repeat block to draw a square, and explain why using a loop is better than repeating the blocks four times.", 4, [
            MP("Uses a repeat 4 block", ["repeat 4", "four times", "loop 4"]),
            MP("Contains a move block and a turn 90 degrees block", ["move", "turn 90", "90 degrees"]),
            MP("A loop means less code to write and read", ["shorter", "less code", "fewer blocks", "quicker", "tidier"]),
            MP("It is easier to change, for example altering the size or number of sides in one place", ["easier to change", "one place", "edit once", "change the number", "modify"]),
        ], "To draw a square you would use a repeat 4 block containing a move 100 steps block followed by a turn 90 degrees block. Each pass draws one side and turns the corner, and after four passes the sprite has turned through 360 degrees and returned to where it started. Using a loop is better than writing the two blocks out four times because the script is much shorter and easier to read, and more importantly it is far easier to change. If you wanted a larger square you would only have to edit one move block instead of four, and if you wanted a different shape you would only have to change the repeat number and the turn angle.",
           command="Describe"),
        EQ("A game should say 'Well done' when the score reaches 10, and 'Keep trying' otherwise. Write the blocks you would use.", 3, [
            MP("Uses an if else block", ["if", "else", "if else"]),
            MP("Condition tests whether the score is 10 or more", ["score", "> 9", ">= 10", "= 10", "10"]),
            MP("Correct message in each branch", ["well done", "keep trying", "say"]),
        ], "if <score > 9> then\n    say \"Well done\"\nelse\n    say \"Keep trying\"\n\nThe if else block gives two paths and only one of them runs. The condition checks whether the score has reached 10, and because Scratch has a greater than block rather than a greater than or equal to block, testing for greater than 9 is the usual way to include 10 itself.",
           command="Write"),
    ],
)

Y7_PYTHON = Topic(
    slug="introduction-to-python",
    title="Introduction to Python",
    spec="Y7.3",
    icon="i-python",
    minutes=26,
    blurb="Your first real code. Printing, variables, input, data types and simple if statements, with every common beginner error explained.",
    fact="Python was released in 1991 and its creator wrote most of it over a Christmas holiday. He named it after Monty Python, which is why the official documentation is full of references to spam and eggs.",
    sections=[
        Section("Output and variables", """
### Printing

```python
print("Hello, world!")
print("My name is Sam")
```

Text must go inside **quotation marks**. Numbers do not need them.

```python
print(42)
print("42")     # this is text, not a number
```

### Variables

A **variable** stores a value under a name.

```python
name = "Aisha"
age = 12
height = 1.52
```

The equals sign means **put this value into this box**. It does not mean the two sides are equal.

Rules for variable names:

- Start with a letter
- No spaces, use `first_name` or `firstName`
- Case sensitive: `Score` and `score` are different variables
- Choose names that say what they hold

```python
score = 0
score = score + 10     # score is now 10
print(score)
```

The line `score = score + 10` looks strange in maths, but in programming it means: work out `score + 10`, then put the answer back into `score`.
"""),
        Section("Input and data types", """
### Getting input

```python
name = input("What is your name? ")
print("Hello " + name)
```

!warn input always gives you text :: Even if the user types 7, Python stores it as the text `"7"`, not the number 7. That single fact causes most beginner bugs.

```python
age = input("How old are you? ")
print(age + 1)      # ERROR, you cannot add 1 to text
```

The fix is to **convert** it:

```python
age = int(input("How old are you? "))
print(age + 1)      # works
```

### The main data types

| Type | Holds | Example |
| `int` | Whole numbers | `7`, `-3`, `0` |
| `float` | Numbers with decimals | `3.14`, `1.5` |
| `str` | Text, called a string | `"hello"`, `"7"` |
| `bool` | True or False | `True`, `False` |

### Converting

```python
int("7")        # the number 7
float("3.5")    # the number 3.5
str(7)          # the text "7"
```

### Joining text and numbers

```python
score = 15
print("You scored " + str(score))     # convert the number to text first
print("You scored", score)            # or use a comma, which Python handles for you
```
"""),
        Section("Making decisions", """
### if statements

```python
age = int(input("How old are you? "))

if age >= 13:
    print("You can have an account")
else:
    print("You are too young")
```

Three things to notice:

1. The **colon** at the end of the `if` line
2. The **indentation** of the lines underneath, four spaces
3. **Two equals signs** for comparison, one for assignment

### Comparison operators

| Operator | Means |
| `==` | is equal to |
| `!=` | is not equal to |
| `<` | is less than |
| `>` | is greater than |
| `<=` | is less than or equal to |
| `>=` | is greater than or equal to |

### More than two options

```python
mark = int(input("Enter your mark: "))

if mark >= 70:
    print("Excellent")
elif mark >= 50:
    print("Good")
elif mark >= 30:
    print("Keep working")
else:
    print("See your teacher")
```

`elif` means else if. Python checks each condition in order and runs the **first one** that is true, then skips the rest.

!key The order matters enormously :: If `mark >= 30` came first, a mark of 95 would print "Keep working", because 95 is greater than 30 and Python stops at the first true condition. Always put the most restrictive condition first.

### Common beginner errors

| Error message | What it usually means |
| `SyntaxError: invalid syntax` | Missing colon, or missing bracket |
| `IndentationError` | The lines under an if or a loop are not indented consistently |
| `NameError: name 'x' is not defined` | Variable used before it was created, or a typo in the name |
| `TypeError: can only concatenate str` | Trying to join text and a number without converting |
| `ValueError: invalid literal for int()` | Trying to convert text like "hello" into a number |
"""),
    ],
    keyterms=[
        ("Variable", "A named store for a value that can change while the program runs."),
        ("String", "Text data, written inside quotation marks."),
        ("Integer", "A whole number, with no decimal part."),
        ("Float", "A number with a decimal part."),
        ("Input", "Data entered by the user, which Python always stores as text."),
        ("Casting", "Converting a value from one data type to another, such as int() or str()."),
        ("Indentation", "Spaces at the start of a line that tell Python which lines belong inside an if or a loop."),
        ("Syntax error", "A mistake in the way the code is written, which stops the program running at all."),
    ],
    grade="""
Reaching the top level in Year 7 Python is about **explaining what your code does**, not just getting it to run.

**Read error messages properly.** They tell you the line number and the type of error. Learning to read them turns a frustrating hour into a two minute fix.

**Test your program with awkward input.** What happens if someone types letters when you asked for a number? What if they type nothing at all? Thinking about that is what separates a working program from a good one.

**Explain your conditions.** Why did you use `>=` rather than `>`? Because a mark of exactly 50 should count as a pass, and `>` would exclude it.

+ Write a program that asks for input, converts it and uses it in a calculation
+ Write an if elif else chain in the correct order and explain why the order matters
+ Identify the cause of each of the five common error messages
+ Explain what int() and str() do and when each is needed
""",
    mistakes=[
        "Forgetting the colon at the end of an if line.",
        "Using one equals sign in a condition when two are needed.",
        "Forgetting to convert input to a number before doing arithmetic.",
        "Indenting inconsistently, mixing tabs and spaces.",
        "Putting elif conditions in the wrong order, so higher values are caught by the wrong branch.",
    ],
    quiz=[
        Q("What does `print(\"7\" + \"3\")` display?", ["73", "10", "7 3", "An error"], 0,
          "Both values are strings, so the plus sign joins them together rather than adding them."),
        Q("What is stored in `age` after `age = input(\"Age? \")` if the user types 14?",
          ["The text \"14\"", "The number 14", "Nothing", "True"], 0,
          "The input function always returns a string, even when the user types digits."),
        Q("Which line correctly converts input into a whole number?",
          ["age = int(input(\"Age? \"))", "age = input(int(\"Age? \"))",
           "age = str(input(\"Age? \"))", "age = input(\"Age? \").number"], 0,
          "The input is collected first, then int() converts the resulting string into an integer."),
        Q("What is wrong with `if score = 10:`?",
          ["A comparison needs two equals signs", "There should be no colon",
           "score should be in quotes", "Nothing is wrong"], 0,
          "One equals sign assigns a value. Comparison requires ==."),
        Q("What does `elif` mean?", ["else if", "end if", "element if", "either if"], 0,
          "It lets you check another condition if the previous ones were false."),
        Q("A program uses `if mark >= 30` before `if mark >= 70`. What happens with a mark of 85?",
          ["The first condition is true, so the wrong message is shown",
           "Both messages are shown",
           "The program crashes",
           "The correct message is shown"], 0,
          "Python runs the first true branch and skips the rest, so the most restrictive condition must come first."),
        Q("Which data type is `3.5`?", ["float", "int", "str", "bool"], 0,
          "A float is a number with a decimal part. An int is a whole number."),
        Q("What causes a NameError?",
          ["Using a variable that has not been created, or a typo in its name",
           "Forgetting a colon", "Adding a string to a number", "Bad indentation"], 0,
          "Python is telling you the name does not exist, which is usually a spelling mistake or using it too early."),
        Q("Why must lines inside an if statement be indented?",
          ["Indentation tells Python which lines belong inside the if",
           "It makes the code look nicer", "It makes the program run faster",
           "Python ignores indentation"], 0,
          "In Python the indentation is the structure, not just formatting, which is unusual among programming languages."),
        Q("What does `str(42)` produce?", ["The text \"42\"", "The number 42", "An error", "True"], 0,
          "str() converts a value into a string so it can be joined to other text with a plus sign."),
    ],
    exam=[
        EQ("Explain why the following code causes an error: age = input(\"Age? \") then print(age + 1)", 3, [
            MP("The input function returns a string", ["string", "text", "input returns"]),
            MP("Python cannot add a number to a string", ["cannot add", "type error", "different types", "not a number"]),
            MP("The fix is to convert the input using int()", ["int(", "convert", "cast", "integer"]),
        ], "The input function always returns a string, so age holds the text \"14\" rather than the number 14 even when the user types digits. Python cannot add the integer 1 to a string, so it raises a TypeError. The fix is to convert the input to a whole number as it is read, by writing age = int(input(\"Age? \")), after which the addition works correctly.",
           command="Explain"),
        EQ("Write a Python program that asks the user for their name and their age, then prints a message saying whether they are old enough to watch a 12 rated film.", 5, [
            MP("Asks for the name using input", ["input", "name"]),
            MP("Asks for the age and converts it to an integer", ["int(input", "age", "convert"]),
            MP("Uses an if statement with a correct condition", ["if", ">= 12", "> 11"]),
            MP("Prints a suitable message when old enough", ["print", "can watch", "old enough", "yes"]),
            MP("Uses else to print a message when not old enough", ["else", "too young", "cannot", "not old enough"]),
        ], "name = input(\"What is your name? \")\nage = int(input(\"How old are you? \"))\n\nif age >= 12:\n    print(name + \", you can watch a 12 rated film.\")\nelse:\n    print(name + \", you are too young for a 12 rated film.\")\n\nThe name is read as a string, which is correct because it is text. The age is converted to an integer so it can be compared with a number. The condition uses greater than or equal to, so someone who is exactly 12 is correctly allowed.",
           command="Write"),
        EQ("State the purpose of the int() function and the str() function in Python.", 2, [
            MP("int() converts a value into a whole number", ["int", "whole number", "integer", "converts to a number"]),
            MP("str() converts a value into text or a string", ["str", "string", "text", "converts to text"]),
        ], "The int() function converts a value into a whole number, which is needed when input has been read from the user as text but arithmetic or a numerical comparison has to be performed on it. The str() function does the opposite, converting a value such as a number into a string, which is needed when you want to join it to other text using the plus operator.",
           command="State"),
        EQ("A program should print 'Pass' for a mark of 50 or more and 'Fail' otherwise, but a mark of exactly 50 prints 'Fail'. Explain the likely cause and the correction.", 3, [
            MP("The condition uses greater than rather than greater than or equal to", ["greater than", ">", "not >=", "wrong operator"]),
            MP("A mark of exactly 50 is not greater than 50, so it fails the test", ["exactly 50", "not greater", "equal", "boundary"]),
            MP("Change the condition to mark >= 50", [">= 50", "greater than or equal", "change to"]),
        ], "The likely cause is that the condition has been written as if mark > 50 rather than if mark >= 50. A mark of exactly 50 is not greater than 50, so the condition is false and the else branch runs, printing Fail. The correction is to change the operator to greater than or equal to, writing if mark >= 50, so that a mark of exactly 50 is correctly counted as a pass.",
           command="Explain"),
        EQ("Explain why indentation matters in Python.", 2, [
            MP("Indentation shows which lines belong inside a structure such as an if statement or a loop", ["belong", "inside", "part of", "structure", "block"]),
            MP("Incorrect indentation causes an error or makes the program behave incorrectly", ["error", "indentation error", "wrong", "will not run", "behave"]),
        ], "In Python, indentation is not just formatting: it is how the language knows which lines belong inside an if statement, a loop or a function. Lines indented under an if only run when the condition is true, while a line that is not indented runs regardless. If the indentation is inconsistent Python raises an IndentationError and the program will not run at all, and if it is consistent but wrong the program will run while doing something the programmer did not intend.",
           command="Explain"),
    ],
)

Y7_UNDERSTAND = Topic(
    slug="understanding-computers",
    title="Understanding Computers",
    spec="Y7.4",
    icon="i-cpu",
    minutes=22,
    blurb="What is inside the box, how binary works, and why every computer is really just a very fast machine for moving 1s and 0s around.",
    fact="If you counted on your fingers in binary instead of one per finger, you could count to 1023 on two hands. Each finger becomes a place value: 1, 2, 4, 8, 16 and so on.",
    sections=[
        Section("Inside the computer", """
| Component | Job |
| **CPU** | The brain. Processes all instructions and does all the calculating. |
| **RAM** | Holds the programs and data being used right now. Wiped when the power goes. |
| **Hard drive or SSD** | Stores files permanently, even when switched off. |
| **Motherboard** | The main circuit board that everything plugs into and communicates through. |
| **Power supply** | Converts mains electricity to the low voltages the parts need. |
| **Graphics card** | Handles images and video, which matters most in games and video editing. |

### The CPU

The **Central Processing Unit** does three things over and over, billions of times per second:

1. **Fetch** the next instruction from memory
2. **Decode** it to work out what it means
3. **Execute** it, actually doing the work

This never stops while the computer is on.

**Clock speed** measures how many of those cycles happen per second. 3 GHz means three billion per second.

**Cores** are complete processing units. A quad core CPU has four, so it can work on four things at once, as long as the software is written to make use of them.

!warn RAM and storage are not the same :: RAM is temporary and fast, and it is emptied when the power goes. Storage is permanent and slower. Buying more storage will not make a slow computer faster if the problem is not enough RAM.
"""),
        Section("Binary", """
Computers use **binary**, which has only two digits: 0 and 1.

The reason is electrical. A circuit is either **on** or **off**, and those two states are easy to tell apart reliably. Ten different voltage levels for our normal digits would be far harder to build and far easier to get wrong.

### Place values

In denary each column is ten times the one to its right: 1, 10, 100, 1000.

In binary each column is **twice** the one to its right:

| 128 | 64 | 32 | 16 | 8 | 4 | 2 | 1 |

### Binary to denary

Add the place values where there is a 1.

    1 0 1 1 0 1 0 0
    128 + 32 + 16 + 4 = 180

### Denary to binary

Work from the left, asking whether each place value fits.

Convert 45:

- 128? No. Write 0.
- 64? No. Write 0.
- 32? Yes. Write 1. 45 - 32 = 13
- 16? No. Write 0.
- 8? Yes. Write 1. 13 - 8 = 5
- 4? Yes. Write 1. 5 - 4 = 1
- 2? No. Write 0.
- 1? Yes. Write 1. 1 - 1 = 0

Result: `00101101`. Check: 32 + 8 + 4 + 1 = 45.

!key Always write the place values down first :: Every mistake on this comes from trying to do it in your head.
"""),
        Section("Units and how everything is stored", """
| Unit | Size |
| Bit | One 1 or 0 |
| Nibble | 4 bits |
| Byte | 8 bits |
| Kilobyte (KB) | 1000 bytes |
| Megabyte (MB) | 1000 KB |
| Gigabyte (GB) | 1000 MB |
| Terabyte (TB) | 1000 GB |

### Text

Each character is given a number, and that number is stored in binary. The agreed list of characters and their numbers is called a **character set**. In ASCII, capital A is 65, B is 66, and so on.

### Images

An image is a grid of **pixels**. Each pixel has a colour, and that colour is stored as a binary number.

- **More pixels** means more detail and a bigger file.
- **More bits per pixel** means more possible colours and a bigger file.

With 1 bit per pixel you get two colours, black and white. With 8 bits you get 256 colours. With 24 bits you get over 16 million.

### Sound

Sound is a wave. A computer measures the height of the wave many thousands of times per second and stores each measurement as a number. This is called **sampling**.

- **More samples per second** means a more accurate recording and a bigger file.
- CD quality takes 44,100 measurements every second.

!key The pattern to notice :: Text, images and sound are all stored as numbers, and all numbers are stored in binary. Better quality always means more numbers, which always means a bigger file.
"""),
    ],
    keyterms=[
        ("CPU", "The Central Processing Unit, which processes all instructions and does all the calculating."),
        ("RAM", "Temporary fast memory holding what the computer is using now. Emptied when the power goes."),
        ("Binary", "A number system using only 0 and 1, which matches the on and off states of electronic circuits."),
        ("Bit", "A single binary digit, either 0 or 1."),
        ("Byte", "Eight bits."),
        ("Pixel", "The smallest single dot of colour in an image."),
        ("Sampling", "Measuring a sound wave at regular intervals and storing each measurement as a number."),
        ("Character set", "The agreed list of characters and the number used to represent each one."),
    ],
    grade="""
The top level here comes from **explaining causes**, not just stating facts.

**Why binary?** Not "because computers like it". Because circuits are either on or off, and those two states can be told apart reliably.

**Why does a higher quality image have a bigger file?** Because every extra pixel and every extra bit of colour is more data that has to be stored.

**Check your conversions.** Convert back and see whether you get the original number. It takes ten seconds and catches almost every mistake.

+ Convert any 8 bit binary number to denary and back, reliably
+ Explain why computers use binary rather than denary
+ Explain how text, images and sound are all stored as numbers
+ Explain the difference between RAM and storage using volatility
""",
    mistakes=[
        "Writing the place values the wrong way round. The 1 is on the right.",
        "Saying RAM stores files permanently. It is wiped when the power goes.",
        "Confusing bits and bytes. Eight bits make one byte.",
        "Saying a bigger image file is 'better quality' without explaining that it holds more pixels or more colours.",
    ],
    quiz=[
        Q("What is the denary value of 00101101?", ["45", "43", "53", "41"], 0,
          "32 + 8 + 4 + 1 = 45. Write the place values above the digits and add where there is a 1."),
        Q("Why do computers use binary?",
          ["Electronic circuits are either on or off, which matches 1 and 0",
           "Binary numbers are shorter", "Binary is easier for people to read",
           "Binary uses less electricity"], 0,
          "Two clearly different states are reliable to detect. Ten different voltage levels would be far harder."),
        Q("How many bits are in a byte?", ["8", "4", "16", "1000"], 0,
          "Eight bits make a byte. Four bits is a nibble."),
        Q("What is 1 in binary as an 8 bit number?", ["00000001", "10000000", "00000010", "11111111"], 0,
          "The rightmost column has the place value 1, so only that column holds a 1."),
        Q("What does the CPU do?",
          ["Fetches, decodes and executes instructions",
           "Stores files permanently", "Displays images on the screen",
           "Supplies power to the components"], 0,
          "The fetch decode execute cycle is what a processor does continuously while the computer is on."),
        Q("Which statement about RAM is correct?",
          ["It holds what the computer is using now and is wiped when the power goes",
           "It stores files permanently",
           "It is slower than a hard drive",
           "It is where the CPU is stored"], 0,
          "RAM is volatile, which is why unsaved work disappears in a power cut."),
        Q("An image with more pixels will:",
          ["Have more detail and a larger file size", "Have less detail and a smaller file",
           "Have the same file size", "Only work in black and white"], 0,
          "Every pixel is stored data, so more pixels means more detail and more storage."),
        Q("What is sampling?",
          ["Measuring a sound wave at regular intervals and storing each measurement",
           "Copying part of one song into another",
           "Reducing the number of colours in an image",
           "Testing a program with different data"], 0,
          "The wave is continuous, so it must be measured at intervals and each measurement stored as a number."),
        Q("How many colours can be stored using 8 bits per pixel?",
          ["256", "8", "16", "1000"], 0,
          "Each bit doubles the possibilities, so 2 to the power 8 is 256."),
        Q("Which is the largest?", ["1 gigabyte", "500 megabytes", "10,000 kilobytes", "1,000,000 bytes"], 0,
          "1 GB is 1000 MB. The others are 500 MB, 10 MB and 1 MB."),
    ],
    exam=[
        EQ("Explain why computers use binary to store data.", 2, [
            MP("Electronic components have two states, on and off", ["two states", "on and off", "circuit", "voltage", "switch"]),
            MP("These two states can represent 1 and 0 reliably", ["1 and 0", "represent", "reliable", "easily", "tell apart"]),
        ], "Computers are built from electronic components that have exactly two reliable states: a circuit is either carrying current or it is not. These two states can be used to represent the digits 1 and 0, and because there are only two of them they can be told apart reliably even if the voltage varies a little. Trying to use ten different levels for ordinary denary digits would be far harder to build and far more likely to produce errors.",
           command="Explain"),
        EQ("Convert the denary number 89 into 8 bit binary. Show your working.", 3, [
            MP("Uses place values starting from 128", ["128", "64", "place value", "32"]),
            MP("Shows subtraction working", ["89 - 64", "25", "subtract", "leaves"]),
            MP("Correct answer 01011001", ["01011001"]),
        ], "Working from the largest place value downwards: 128 does not fit into 89, so write 0. 64 fits, leaving 25, so write 1. 32 does not fit into 25, so write 0. 16 fits into 25, leaving 9, so write 1. 8 fits into 9, leaving 1, so write 1. 4 does not fit, write 0. 2 does not fit, write 0. 1 fits, leaving 0, so write 1. The answer is 01011001, and checking gives 64 + 16 + 8 + 1 = 89.",
           command="Convert"),
        EQ("Describe the difference between RAM and a hard drive.", 3, [
            MP("RAM holds the data and programs currently in use", ["currently", "in use", "right now", "open", "running"]),
            MP("RAM is wiped when the power is switched off", ["wiped", "lost", "erased", "temporary", "power off"]),
            MP("A hard drive stores data permanently and is much larger but slower", ["permanent", "keeps", "larger", "slower", "stays"]),
        ], "RAM holds the programs and data that the computer is using at that moment, and the CPU reads directly from it because it is very fast. However, RAM is temporary: its contents are wiped as soon as the power is switched off, which is why unsaved work is lost in a power cut. A hard drive stores data permanently, so files are still there when the computer is switched back on. It has a much larger capacity than RAM but is far slower to access, which is why programs are copied from the hard drive into RAM when they are opened.",
           command="Describe"),
        EQ("Explain how an image is stored in a computer.", 4, [
            MP("The image is divided into a grid of pixels", ["pixels", "grid", "dots", "squares"]),
            MP("Each pixel is given a colour stored as a binary number", ["colour", "binary", "number", "each pixel"]),
            MP("More pixels means more detail", ["more pixels", "detail", "resolution", "sharper"]),
            MP("More bits per pixel means more possible colours, and both increase file size", ["bits per pixel", "more colours", "colour depth", "file size", "bigger"]),
        ], "An image is stored as a grid of tiny squares called pixels. Each pixel holds a single colour, and that colour is represented by a binary number, so the whole image becomes a long list of binary values. The number of pixels is called the resolution, and using more pixels means the picture captures finer detail and looks sharper. The number of bits used for each pixel decides how many different colours are available, so 8 bits gives 256 colours while 24 bits gives over 16 million. Increasing either the number of pixels or the number of bits per pixel improves the quality of the image but also increases the amount of data that has to be stored, so the file becomes larger.",
           command="Explain"),
        EQ("State what the CPU does and explain what clock speed measures.", 3, [
            MP("The CPU processes instructions", ["processes", "instructions", "carries out", "executes"]),
            MP("It fetches, decodes and executes instructions repeatedly", ["fetch", "decode", "execute", "cycle"]),
            MP("Clock speed measures how many cycles the CPU performs each second", ["cycles per second", "how many", "per second", "hertz", "speed"]),
        ], "The CPU is the part of the computer that processes all the instructions, and it does this by repeatedly fetching the next instruction from memory, decoding it to work out what it means, and then executing it. Clock speed measures how many of these cycles the CPU carries out each second, and it is given in hertz. A processor running at 3 gigahertz completes three billion cycles every second, so a higher clock speed generally means more instructions are processed and the computer feels faster.",
           command="State"),
    ],
)

Y7_VECTOR = Topic(
    slug="vector-graphics",
    title="Vector Graphics",
    spec="Y7.5",
    icon="i-palette",
    minutes=20,
    blurb="Why a logo stays sharp at any size while a photograph turns blocky, and the tools you need to design your own vector artwork.",
    fact="Every road sign, company logo and app icon you see is a vector graphic. They have to be, because the same design must work on a business card and on the side of a building without being redrawn.",
    sections=[
        Section("Bitmap against vector", """
There are two completely different ways to store a picture.

### Bitmap, also called raster

The image is a **grid of pixels**, each with its own colour. Photographs are bitmaps.

- Great for photographs, where colour changes constantly across the image
- File size depends on the number of pixels
- **Becomes blocky when enlarged**, because there is no extra detail to reveal
- File types: JPG, PNG, GIF, BMP

### Vector

The image is stored as a **list of instructions and mathematical shapes**: draw a circle at this position with this radius, this fill colour and this outline.

- **Stays perfectly sharp at any size**, because the shapes are redrawn from the maths every time
- Usually much smaller files for simple graphics
- Every shape can be selected and edited individually afterwards
- Not suitable for photographs, which have far too much irregular detail
- File types: SVG, AI, EPS, and Inkscape's own format

| | Bitmap | Vector |
| Made of | Pixels | Shapes and instructions |
| Enlarging | Becomes blocky | Stays sharp |
| Best for | Photographs | Logos, icons, diagrams, signs |
| Editing | Change individual pixels | Move and edit whole shapes |
| Typical file size | Larger | Smaller for simple images |

!key The reason a vector stays sharp :: A vector file does not store a picture. It stores the instructions for drawing one, so when the size changes the shapes are simply drawn again at the new size.
"""),
        Section("Working with vector shapes", """
### The tools

- **Shape tools** for rectangles, ellipses, stars and polygons
- **The pen or Bezier tool** for drawing custom paths with curves
- **Node editing** to move the individual points that make up a shape
- **Fill** is the colour inside a shape, **stroke** is the outline

### Layers and order

Shapes stack. The one drawn most recently sits on top.

- **Raise** and **lower** change the stacking order
- **Group** joins several shapes so they move and scale together
- **Ungroup** separates them again

### Operations that combine shapes

| Operation | What it does |
| **Union** | Merges shapes into one |
| **Difference** | Cuts the top shape out of the one beneath |
| **Intersection** | Keeps only the overlapping part |
| **Exclusion** | Keeps everything except the overlap |

These are how most professional logos are actually made. A crescent moon is simply one circle with another circle subtracted from it.

### Alignment

Use align and distribute tools rather than dragging by eye. Centring things properly is one of the fastest ways to make a design look professional.
"""),
        Section("Designing a good logo", """
### What makes a logo work

1. **Simple.** It must be recognisable at 16 pixels on a browser tab as well as on a poster.
2. **Works in one colour.** If it only reads in full colour it will fail on a fax, a stamp or an engraving.
3. **Distinctive.** It should not look like ten other logos in the same industry.
4. **Appropriate.** The style must suit the audience and the purpose.
5. **Scalable**, which is exactly why it must be a vector.

### The design process

1. **Client brief.** What does the client want, who is it for, what must it convey?
2. **Research.** Look at what similar organisations do, and what the audience expects.
3. **Mood board.** Collect colours, fonts, shapes and images that capture the feel.
4. **Sketches.** Draw many rough ideas quickly on paper. Quantity first, quality later.
5. **Digital version.** Build the strongest idea as a vector.
6. **Review.** Test it small, test it in one colour, and get feedback.

!warn Do not start on the computer :: The single biggest mistake in logo design is opening the software first. Ten minutes of rough sketching produces better ideas than an hour of dragging shapes around.
"""),
    ],
    keyterms=[
        ("Bitmap", "An image stored as a grid of pixels, each with its own colour."),
        ("Vector", "An image stored as mathematical shapes and instructions rather than pixels."),
        ("Pixel", "The smallest single dot of colour in a bitmap image."),
        ("Scalable", "Able to be resized without any loss of quality."),
        ("Fill", "The colour inside a shape."),
        ("Stroke", "The outline of a shape."),
        ("Node", "A point on a path that can be moved to change the shape."),
        ("Group", "Joining several shapes so they can be moved and resized together."),
        ("Mood board", "A collection of images, colours and fonts gathered to capture the intended feel of a design."),
    ],
    grade="""
The top level here is about **justifying design decisions**.

**Explain why vector, not just that it is vector.** "A logo must be a vector because it will be used at many different sizes, from a website favicon to a shop sign, and a vector is redrawn from its shape instructions at every size so it never loses sharpness."

**Talk about the audience.** A logo for a children's nursery and a logo for a law firm should not look the same, and being able to say why shows real design thinking.

**Describe your process.** Client brief, research, mood board, sketches, digital version, review. Being able to explain what each stage is for is worth more than the finished artwork alone.

+ Explain the difference between bitmap and vector, with a use for each
+ Justify choosing vector format for a specific purpose
+ Describe how to make a crescent shape using difference
+ Explain what a mood board is for and why sketching comes before software
""",
    mistakes=[
        "Saying vectors 'have better quality'. They stay sharp at any size, which is not the same thing. For a photograph a bitmap is far better.",
        "Saying a vector file is always smaller. For a very complex illustration it can be larger than a bitmap.",
        "Starting a logo design in the software instead of sketching first.",
        "Designing a logo that only works in colour and at large size.",
    ],
    quiz=[
        Q("What is a vector graphic made of?",
          ["Mathematical shapes and instructions", "A grid of pixels",
           "Compressed photographs", "Layers of text"], 0,
          "Vectors store how to draw the picture, not the picture itself, which is why they can be redrawn at any size."),
        Q("Why does a vector image stay sharp when enlarged?",
          ["The shapes are redrawn from their instructions at the new size",
           "It contains more pixels than a bitmap",
           "It uses lossless compression",
           "It automatically adds detail"], 0,
          "Nothing is stretched. The maths is simply recalculated, so the edges stay perfectly crisp."),
        Q("Which format is best for a photograph?",
          ["Bitmap", "Vector", "Either works equally well", "Neither"], 0,
          "Photographs have irregular detail in every pixel, which is exactly what bitmaps store well and vectors cannot."),
        Q("Which file type is a vector format?", ["SVG", "JPG", "PNG", "GIF"], 0,
          "SVG stands for Scalable Vector Graphics. The other three are all bitmap formats."),
        Q("What does the difference operation do?",
          ["Cuts the top shape out of the shape beneath",
           "Merges two shapes into one",
           "Keeps only the overlapping part",
           "Separates a group"], 0,
          "Difference is how you make a crescent from two circles, or a hole in a shape."),
        Q("What is the fill of a shape?",
          ["The colour inside it", "The outline colour", "Its position", "Its transparency"], 0,
          "Fill is inside, stroke is the outline."),
        Q("Why should a logo work in a single colour?",
          ["It may be used where colour is unavailable, such as engraving or a stamp",
           "Single colour files are smaller",
           "Colour logos are illegal",
           "It makes the logo a vector"], 0,
          "A logo has to survive being printed, embroidered, engraved and faxed, and a design that depends on colour fails in all of those."),
        Q("What is a mood board used for?",
          ["Collecting colours, fonts and images that capture the intended feel",
           "Testing a program", "Storing the final logo files", "Recording client payments"], 0,
          "It is a visual reference that helps the designer and the client agree on a direction before work begins."),
        Q("Why should you sketch ideas on paper before using design software?",
          ["Sketching produces many ideas quickly, while software slows exploration down",
           "Paper produces higher resolution images",
           "Software cannot draw curves",
           "Clients only accept paper designs"], 0,
          "Rough sketches let you try twenty ideas in ten minutes, which is where good design actually comes from."),
        Q("What does grouping shapes do?",
          ["Lets them be moved and resized together as one object",
           "Merges them permanently into one shape",
           "Deletes the overlapping parts",
           "Converts them into a bitmap"], 0,
          "Grouping is reversible. Union permanently merges shapes into a single path."),
    ],
    exam=[
        EQ("State two differences between a bitmap image and a vector image.", 2, [
            MP("A bitmap is made of pixels, a vector is made of shapes and instructions", ["pixels", "shapes", "instructions", "mathematical"]),
            MP("A vector stays sharp when resized, a bitmap becomes blocky", ["sharp", "blocky", "pixelated", "resize", "quality"]),
        ], "A bitmap image is made up of a grid of individual pixels, each storing its own colour, whereas a vector image is stored as a set of mathematical shapes and instructions for drawing them. As a result, a vector image stays perfectly sharp when it is enlarged because the shapes are simply redrawn at the new size, while a bitmap becomes blocky and pixelated because the existing pixels just get bigger.",
           command="State"),
        EQ("A company needs a logo that will be used on a website, on business cards and on the side of a lorry. Explain why the logo should be created as a vector graphic.", 3, [
            MP("The logo will be used at many different sizes", ["different sizes", "small and large", "range of sizes", "many sizes"]),
            MP("A vector can be resized without any loss of quality", ["no loss", "stays sharp", "quality", "scalable", "resized"]),
            MP("A bitmap would become blocky when enlarged for the lorry", ["blocky", "pixelated", "lose quality", "bitmap would", "poor"]),
        ], "The logo needs to appear at hugely different sizes, from a tiny favicon on a website through to a design several metres wide on the side of a lorry. A vector graphic stores the logo as mathematical shapes and instructions rather than fixed pixels, so it can be redrawn at any size with no loss of quality at all and the edges remain perfectly crisp. If the logo were created as a bitmap it would be fixed at one resolution, and enlarging it to lorry size would make the individual pixels visible so the design would look blocky and unprofessional.",
           command="Explain"),
        EQ("Describe how you would use vector shape operations to create a crescent moon shape.", 3, [
            MP("Draw two overlapping circles", ["two circles", "overlapping", "circle", "ellipse"]),
            MP("Position the second circle so it overlaps part of the first", ["position", "overlap", "offset", "move", "on top"]),
            MP("Use the difference operation to cut the top circle out of the one beneath", ["difference", "subtract", "cut out", "remove"]),
        ], "First draw a circle to form the outer edge of the moon. Then draw a second circle of a similar size and position it so that it overlaps a large part of the first, offset to one side. With the second circle selected on top, apply the difference operation, which cuts the shape of the top circle out of the one beneath it. What remains is a crescent, and because it is still a vector path it can be recoloured and resized freely afterwards.",
           command="Describe"),
        EQ("Explain three things that make a logo effective.", 6, [
            MP("It should be simple", ["simple", "not cluttered", "clean", "uncomplicated"]),
            MP("So that it is recognisable even at very small sizes", ["small", "recognisable", "favicon", "still clear", "tiny"]),
            MP("It should work in a single colour", ["one colour", "single colour", "black and white", "monochrome"]),
            MP("Because it may be printed, engraved or embroidered where colour is unavailable", ["printed", "engraved", "embroidered", "no colour", "stamp", "fax"]),
            MP("It should be appropriate for the audience and purpose", ["audience", "appropriate", "suits", "purpose", "target"]),
            MP("It should be distinctive so it is not confused with competitors", ["distinctive", "different", "stand out", "unique", "competitors", "memorable"]),
        ], "First, an effective logo is simple. It has to be recognisable when displayed as a browser tab icon only sixteen pixels across as well as on a large sign, and a design with fine detail or many elements simply turns into a smudge at small sizes. Second, it should work in a single colour. Logos are not only used on screens: they are printed in black and white, embroidered onto uniforms, engraved into metal and stamped onto packaging, and a design that relies on colour differences to be readable will fail completely in all of those situations. Third, it should be appropriate for its audience and distinctive within its field. A logo for a children's nursery needs a very different style from one for a law firm, because the audience and the message are different, and it must also be different enough from competitors that customers do not confuse the two, which is the whole reason a company has a logo in the first place.",
           command="Explain"),
        EQ("Describe two stages of the design process that should be completed before opening design software.", 4, [
            MP("Client brief to establish what is required", ["brief", "client", "requirements", "what they want", "purpose"]),
            MP("Including the audience and the message", ["audience", "message", "who it is for", "convey"]),
            MP("Mood board or research to gather visual ideas", ["mood board", "research", "inspiration", "collect", "examples"]),
            MP("Sketches to explore many ideas quickly on paper", ["sketch", "paper", "rough", "draw", "ideas"]),
        ], "The first stage is establishing the client brief. This means finding out exactly what the client needs, who the audience is, what message the design should convey and any constraints such as colours the company already uses or where the design will appear. Without this the designer is guessing, and work will have to be redone. The second stage is gathering ideas through research and a mood board, followed by rough sketching. A mood board collects colours, fonts, images and existing designs that capture the intended feel, which gives the designer and the client a shared reference before any work starts. Sketching on paper then allows many different ideas to be tried out very quickly, and because a rough sketch takes seconds rather than minutes, far more possibilities get explored than would ever be attempted directly in the software.",
           command="Describe"),
    ],
)

# ============================================================ YEAR 8

Y8_DIGLIT = Topic(
    slug="digital-literacy",
    title="Digital Literacy and Online Safety",
    spec="Y8.1",
    icon="i-shield",
    minutes=24,
    blurb="Your digital footprint, spotting scams and fake news, protecting your accounts, and what to do when something online goes wrong.",
    fact="Every photograph taken on a phone can store the exact location where it was taken, hidden inside the file as metadata. Posting a holiday photo can therefore tell a stranger precisely where you are.",
    sections=[
        Section("Your digital footprint", """
Your **digital footprint** is the trail of data you leave behind online. It is far larger than most people realise, and much of it is permanent.

### Two kinds

- **Active footprint.** Things you deliberately post: messages, photos, comments, videos, profiles.
- **Passive footprint.** Data collected without you doing anything: which pages you visit, how long you stay, your location, your device, what you search for.

### Why it matters

- Universities and employers do look at public social media
- Anything can be screenshotted, even on apps that promise messages disappear
- Deleting a post does not delete copies other people have made
- Data collected about you is used to target advertising, and is sometimes sold on

### Reducing it

- Check your privacy settings, and check them again after every app update
- Think before posting: would you be happy for a teacher, a parent and a future employer to see this?
- Turn off location tagging on photos
- Do not fill in quizzes that ask for your first pet or your mother's maiden name, because those are security question answers
- Log out of accounts on shared devices

!key The permanence rule :: Assume that anything you put online is permanent and public, even when the app tells you it is not.
"""),
        Section("Scams, phishing and misinformation", """
### Phishing

A **phishing** message pretends to be from an organisation you trust, in order to steal your details.

Warning signs:

- **Urgency**: "your account will be closed in 24 hours"
- A generic greeting such as "Dear customer"
- Spelling and grammar mistakes
- A link whose address does not match the organisation, for example `amaz0n-security.net`
- Asking for a password. **No legitimate organisation ever asks for your password.**
- An attachment you were not expecting

If in doubt, do not click the link. Go to the organisation's website by typing the address yourself.

### Other scams

- **Fake competitions** asking for personal details to claim a prize
- **In game offers** of free currency in exchange for your account details
- **Fake shops** with prices that are too good to be true
- **Requests for money** from a friend's hacked account

### Misinformation

**Misinformation** is false information shared by someone who believes it is true. **Disinformation** is false information spread deliberately to mislead.

How to check a claim:

1. **Who published it?** A recognised news organisation, or an account with no history?
2. **Is it reported anywhere else?** Real news is covered by many independent sources.
3. **When was it published?** Old stories are constantly recirculated as if they were new.
4. **What is the evidence?** Does it link to a source, or just assert?
5. **How does it make you feel?** Content designed to make you angry is designed to be shared before you think.

!warn Images prove nothing on their own :: Photographs are easily edited, taken out of context, or generated entirely by AI. A reverse image search takes ten seconds and often shows a photo is years old and from a different country.
"""),
        Section("Protecting yourself", """
### Account security

- **Long passwords**, different for every important account
- **Two factor authentication** wherever it is offered, so a stolen password alone is not enough
- A **password manager** is safer than reusing one password everywhere
- Never share a password, not even with your closest friend

### Cyberbullying

If it is happening to you, or you see it happening:

1. **Do not reply.** A response is what the bully wants.
2. **Screenshot everything.** Evidence matters, and deleted posts cannot be reported.
3. **Block and report** through the platform.
4. **Tell an adult** you trust. A teacher, a parent or a carer.

You are not in trouble for reporting something. The person doing it is the one with the problem.

### The law

- The **Computer Misuse Act 1990** makes it a crime to access someone else's account without permission, even if you change nothing.
- The **Data Protection Act 2018** controls how organisations use your personal data and gives you the right to see what they hold about you.
- The **Copyright, Designs and Patents Act 1988** makes it illegal to copy or share music, films, games or images without permission.

Logging into a friend's account to post something as a joke is a criminal offence, not a prank.
"""),
    ],
    keyterms=[
        ("Digital footprint", "The trail of data a person leaves behind through their online activity."),
        ("Active footprint", "Data you deliberately share, such as posts and photographs."),
        ("Passive footprint", "Data collected about you without any action on your part, such as browsing history."),
        ("Phishing", "A fraudulent message pretending to be from a trusted organisation, designed to steal personal information."),
        ("Misinformation", "False information shared by someone who believes it to be true."),
        ("Disinformation", "False information spread deliberately in order to mislead."),
        ("Two factor authentication", "A security method requiring a second proof of identity as well as a password."),
        ("Computer Misuse Act 1990", "The law making unauthorised access to a computer or account a criminal offence."),
    ],
    grade="""
The strongest answers here are **specific and practical**.

**Give the warning sign, not just the label.** Not "you can tell it is phishing", but "the greeting says Dear Customer rather than your name, and the link points to amaz0n-security.net rather than amazon.co.uk".

**Explain why the advice works.** Two factor authentication helps because even if someone steals your password they still cannot log in without the code sent to your phone.

**Know the law by name.** Being able to say "logging into someone else's account without permission breaks the Computer Misuse Act 1990" is far stronger than "it is against the rules".

+ List four warning signs of a phishing message
+ Explain the difference between an active and a passive digital footprint
+ Give the four steps to take if you are being cyberbullied, in order
+ Name the three acts and say what each protects
""",
    mistakes=[
        "Saying deleted posts are gone. Screenshots and archives outlive the original.",
        "Thinking a message must be a scam only if it is badly written. The most effective ones are perfectly written.",
        "Replying to a bully to defend yourself, which escalates the situation and gives them what they want.",
        "Confusing misinformation with disinformation. The difference is whether the person knew it was false.",
    ],
    quiz=[
        Q("What is a passive digital footprint?",
          ["Data collected about you without you actively sharing it",
           "Photographs you choose to post",
           "Messages you send to friends",
           "Your username"], 0,
          "Browsing history, location data and search terms are gathered automatically as you use services."),
        Q("Which is the strongest warning sign of a phishing email?",
          ["It asks you to confirm your password", "It has a subject line",
           "It was sent in the morning", "It contains an image"], 0,
          "No legitimate organisation will ever ask you for your password, so this alone is enough to reject the message."),
        Q("What is the difference between misinformation and disinformation?",
          ["Disinformation is spread deliberately, misinformation is shared by someone who believes it",
           "Misinformation is always about politics",
           "Disinformation is legal and misinformation is not",
           "There is no difference"], 0,
          "The distinction is intent. Both are false, but only one is deliberate."),
        Q("Why does two factor authentication improve security?",
          ["A stolen password alone is not enough to log in",
           "It makes your password longer",
           "It encrypts your files",
           "It hides your IP address"], 0,
          "The attacker would also need the second factor, usually a code sent to a device only you have."),
        Q("What should you do first if you receive abusive messages online?",
          ["Screenshot them as evidence and do not reply",
           "Reply and defend yourself",
           "Delete your account immediately",
           "Send an abusive message back"], 0,
          "Evidence is what allows the platform and the school to act, and replying gives the bully the reaction they want."),
        Q("Logging into a friend's account without permission, even as a joke, breaks which law?",
          ["The Computer Misuse Act 1990", "The Data Protection Act 2018",
           "The Copyright, Designs and Patents Act 1988", "No law is broken"], 0,
          "Unauthorised access is an offence in itself, whether or not anything is changed or taken."),
        Q("Why is it risky to answer online quizzes asking for your first pet's name?",
          ["Those answers are often used as security questions on real accounts",
           "Quizzes contain viruses",
           "It uses too much data",
           "It is illegal"], 0,
          "This is called a name generator attack, and it collects the exact answers used to reset passwords."),
        Q("A photograph posted online can reveal your location because:",
          ["Metadata stored in the file can include GPS coordinates",
           "The image compresses differently in different places",
           "Photos always contain your name",
           "The colours change by region"], 0,
          "Phones record where a photo was taken inside the file itself, unless location tagging is switched off."),
        Q("What is the best way to check whether a news story is true?",
          ["See whether several independent, recognised sources report it",
           "Check how many people shared it",
           "See whether it has a photograph",
           "Check whether it makes you feel strongly"], 0,
          "Independent corroboration is the strongest test. Shares and strong feelings are what fake stories are designed to produce."),
        Q("Which law controls how organisations store and use your personal data?",
          ["The Data Protection Act 2018", "The Computer Misuse Act 1990",
           "The Copyright, Designs and Patents Act 1988", "The Freedom of Information Act 2000"], 0,
          "It also gives you the right to see the data an organisation holds about you and to have errors corrected."),
    ],
    exam=[
        EQ("Explain what is meant by a digital footprint.", 2, [
            MP("The trail of data left behind by online activity", ["trail", "data", "left behind", "record", "online activity"]),
            MP("Includes both what you post and data collected automatically", ["post", "collected", "automatically", "active", "passive", "browsing"]),
        ], "A digital footprint is the trail of data that a person leaves behind through everything they do online. It includes an active part, made up of the things you deliberately share such as posts, photographs and comments, and a passive part made up of data collected about you automatically, such as the pages you visit, how long you spend on them, your searches and your location.",
           command="Explain"),
        EQ("Describe three ways to identify a phishing email.", 3, [
            MP("It creates a sense of urgency", ["urgent", "urgency", "immediately", "24 hours", "act now", "threat"]),
            MP("The link address does not match the real organisation", ["link", "address", "url", "does not match", "spelling of the website"]),
            MP("It asks for personal details or a password, or uses a generic greeting", ["password", "personal details", "dear customer", "generic", "greeting"]),
        ], "A phishing email usually creates a sense of urgency, warning that an account will be closed or money will be lost unless you act immediately, because panic stops people checking carefully. The link in the message will point to an address that does not belong to the real organisation, for example a domain with an extra word or a substituted character. Phishing emails also commonly use a generic greeting such as Dear Customer rather than your actual name, and they ask you to confirm personal details or a password, which no legitimate organisation ever does.",
           command="Describe"),
        EQ("A student is being sent abusive messages by another student on social media. Describe the steps they should take.", 4, [
            MP("Do not reply to the messages", ["do not reply", "not respond", "ignore", "no reply"]),
            MP("Take screenshots as evidence", ["screenshot", "evidence", "record", "save", "proof"]),
            MP("Block the person and report them to the platform", ["block", "report", "platform"]),
            MP("Tell a trusted adult such as a parent or teacher", ["adult", "parent", "teacher", "tell someone", "trusted"]),
        ], "The student should not reply to the messages, because a reaction is what the sender is looking for and responding usually makes the situation worse. They should take screenshots of every message first, because this is the evidence that allows the platform and the school to act, and messages can be deleted by the sender at any time. They should then block the person and report them through the platform's own reporting tools. Finally they should tell a trusted adult such as a parent, carer or teacher, who can help them deal with it properly. Reporting is not getting someone into trouble unfairly, and the person being bullied is never the one at fault.",
           command="Describe"),
        EQ("Explain why you should use a different password for each important account.", 3, [
            MP("If one service is breached, the password becomes known to attackers", ["breach", "hacked", "leaked", "stolen", "one site"]),
            MP("Attackers try that same password on other accounts", ["try", "other accounts", "same password", "reuse", "test"]),
            MP("Using different passwords means only one account is affected", ["only one", "limits", "contained", "others safe", "still secure"]),
        ], "Companies do get hacked, and when a service is breached the usernames and passwords it stored can end up in the hands of attackers. Those attackers then automatically try the same email address and password combination on hundreds of other popular sites, because they know most people reuse passwords. If you use the same password everywhere, a breach at one small website you barely remember signing up to can give someone access to your email, your bank and your social media. Using a different password for each important account means a breach only ever affects the single account it came from.",
           command="Explain"),
        EQ("Explain two reasons why you should think carefully before posting a photograph online.", 4, [
            MP("It can be copied or screenshotted and shared beyond your control", ["screenshot", "copied", "shared", "cannot control", "saved"]),
            MP("Deleting the original does not remove copies other people have", ["delete", "copies", "still exists", "permanent", "forever"]),
            MP("Photographs can contain metadata revealing the location", ["metadata", "location", "gps", "where", "geotag"]),
            MP("Future employers or universities may see it", ["employer", "university", "job", "future", "college"]),
        ], "The first reason is that once a photograph is posted you lose control of it. Anyone who can see it can screenshot it and share it anywhere, and deleting your original post does nothing about the copies that other people already have, so the picture may still exist years later. The second reason is that photographs can reveal more than you intend. Phones store metadata inside the image file, which often includes the exact GPS coordinates of where the picture was taken, so a photograph posted publicly can tell a stranger precisely where you live or where you are right now. Beyond both of these, universities and employers do look at what people have posted publicly, so a photograph posted at fourteen can still be found at twenty two.",
           command="Explain"),
    ],
)

Y8_COMPTHINK = Topic(
    slug="computational-thinking",
    title="Computational Thinking",
    spec="Y8.2",
    icon="i-brain",
    minutes=24,
    blurb="The four techniques that let you solve problems the way a computer scientist does, plus flowcharts and pseudocode for planning before you code.",
    fact="The word algorithm comes from the name of a Persian mathematician, al-Khwarizmi, who died around the year 850. His book on solving equations also gave us the word algebra.",
    sections=[
        Section("The four techniques", """
### 1. Decomposition

Breaking a big problem into smaller problems that are easier to solve.

Planning a school trip decomposes into: choose a destination, book transport, collect permission slips, arrange staff, plan the timetable, handle payments.

Each of those is small enough to actually do.

### 2. Abstraction

Removing detail that does not matter, so you can focus on what does.

A map of the school for a fire drill needs the rooms, corridors and exits. It does not need the colour of the walls, where the sockets are, or what is on the noticeboards.

The skill is deciding what to leave out. Detail that is irrelevant for one problem may be essential for another.

### 3. Pattern recognition

Spotting things that are the same or similar, so a solution can be reused.

If you need to calculate the area of six different rectangles, you notice they all follow `width x height` and write one method rather than six.

### 4. Algorithmic thinking

Working out the steps needed, in the right order.

!key How they fit together :: Decompose the problem, abstract away what does not matter, look for patterns you can reuse, then write the algorithm.
"""),
        Section("Flowcharts", """
A **flowchart** shows an algorithm as a diagram.

| Symbol | Shape | Use |
| Terminal | Rounded rectangle | Start and Stop |
| Process | Rectangle | A calculation or action |
| Input or output | Parallelogram | Getting data in or showing results |
| Decision | Diamond | A question with Yes and No branches |
| Arrow | Arrow | Direction of flow |

### Rules

- Every flowchart starts with Start and ends with Stop
- A decision diamond always has **exactly two** labelled exits
- Arrows show the direction, and a loop is an arrow going back up

### Example: is a number even?

    Start
    Input number
    Is number MOD 2 = 0?
        Yes -> Output "Even"
        No  -> Output "Odd"
    Stop

!warn Label both branches :: An unlabelled diamond means the reader cannot tell which way is yes. It is the most common mistake in flowchart questions.
"""),
        Section("Pseudocode and testing", """
**Pseudocode** describes an algorithm in plain, structured English. It is not a real language, so it will not run, but it lets you plan the logic without worrying about syntax.

```pseudo
total = 0
for i = 1 to 5
    number = input("Enter a number")
    total = total + number
next i
average = total / 5
print("The average is " + average)
```

### Why plan first

- Mistakes in logic are far cheaper to fix on paper than in code
- You can show your plan to someone else and get feedback quickly
- The same plan works in any programming language
- Writing the plan often reveals a step you had forgotten

### Trace tables

A **trace table** shows the value of every variable at every step, which is how you check an algorithm actually works.

For `total = 0` then `for i = 1 to 3: total = total + i`:

| i | total |
| 1 | 1 |
| 2 | 3 |
| 3 | 6 |

### Testing

Choose test data of three kinds:

- **Normal**: a typical value that should work, such as 25 for an age
- **Boundary**: right at the edge of what is allowed, such as 0 and 120
- **Erroneous**: something that should be rejected, such as "hello" or -5

Boundary data is the most useful, because that is exactly where mistakes hide.
"""),
    ],
    keyterms=[
        ("Decomposition", "Breaking a large problem into smaller problems that are easier to solve."),
        ("Abstraction", "Removing detail that is not needed so you can focus on what matters."),
        ("Pattern recognition", "Spotting similarities between problems so that a solution can be reused."),
        ("Algorithm", "A set of step by step instructions in the correct order for solving a problem."),
        ("Flowchart", "A diagram showing an algorithm using standard symbols joined by arrows."),
        ("Pseudocode", "A plain English description of an algorithm, used for planning before coding."),
        ("Trace table", "A table showing the value of each variable at every step of an algorithm."),
        ("Boundary data", "Test data at the very edge of what is acceptable, where errors are most likely."),
    ],
    grade="""
The top level here comes from **applying the techniques to a specific problem**, not defining them.

**Use the words from the question.** If the problem is about a vending machine, your decomposition should mention accepting coins, checking stock and dispensing the product, not generic phrases.

**Justify what abstraction removes.** Say what you took out and why it does not matter for this particular problem.

**Complete every row of a trace table.** Even when you can see the answer, the working is what earns credit.

+ Decompose any described problem into at least four sensible sub problems
+ Draw a flowchart with a decision and a loop, with both branches labelled
+ Complete a trace table for a loop without skipping iterations
+ Choose normal, boundary and erroneous test data for a given range
""",
    mistakes=[
        "Confusing decomposition with abstraction. Decomposition splits the problem up, abstraction removes detail.",
        "Using the wrong flowchart symbol, particularly a rectangle where a diamond is needed.",
        "Forgetting to label the yes and no branches of a decision.",
        "Filling in only the last row of a trace table.",
        "Choosing test data that is nowhere near the boundary.",
    ],
    quiz=[
        Q("What is decomposition?",
          ["Breaking a large problem into smaller problems", "Removing unnecessary detail",
           "Spotting similarities between problems", "Putting steps in order"], 0,
          "Decomposition is about splitting the problem up so each part is small enough to solve."),
        Q("Which flowchart symbol is used for a decision?",
          ["A diamond", "A rectangle", "A parallelogram", "A rounded rectangle"], 0,
          "A diamond always has exactly two exits, one for yes and one for no."),
        Q("For an age field accepting 11 to 18, which is boundary test data?",
          ["10 and 11", "15", "\"twelve\"", "100"], 0,
          "Boundary data sits right at the edge of the allowed range, which is where off by one errors show up."),
        Q("Noticing that six different shapes all need the same area formula is an example of:",
          ["Pattern recognition", "Decomposition", "Abstraction", "Iteration"], 0,
          "Recognising the shared structure means one solution can be reused rather than six written separately."),
        Q("What is pseudocode used for?",
          ["Planning the logic of a program before writing real code",
           "Running a program faster", "Compressing a program", "Testing hardware"], 0,
          "It lets you work out the steps without getting stuck on the syntax of a particular language."),
        Q("A fire escape map leaves out the colour of the walls. This is an example of:",
          ["Abstraction", "Decomposition", "Pattern recognition", "Debugging"], 0,
          "Detail that does not help you leave the building quickly has been deliberately removed."),
        Q("What does a trace table show?",
          ["The value of each variable at each step of an algorithm",
           "The time a program takes to run",
           "The layout of the user interface",
           "Which flowchart symbols to use"], 0,
          "It lets you follow exactly what happens step by step, which is how logic errors get found."),
        Q("Which is erroneous test data for a field that accepts a whole number between 1 and 10?",
          ["\"seven\"", "5", "1", "10"], 0,
          "Erroneous data is the wrong type entirely. 5 is normal, and 1 and 10 are boundary values."),
        Q("How many exits does a decision diamond have?",
          ["Two", "One", "Three", "It depends on the question"], 0,
          "Yes and no, and both must be labelled so the reader knows which is which."),
        Q("Why plan an algorithm before writing code?",
          ["Logic mistakes are much cheaper to fix on paper than in code",
           "Planning makes the program run faster",
           "The teacher requires it",
           "It reduces the file size"], 0,
          "Finding a missing step in a five line plan takes seconds. Finding it in fifty lines of code takes far longer."),
    ],
    exam=[
        EQ("State what is meant by decomposition and abstraction.", 2, [
            MP("Decomposition is breaking a problem into smaller parts", ["breaking", "smaller", "parts", "split", "sub problems"]),
            MP("Abstraction is removing detail that is not needed", ["removing", "detail", "not needed", "unnecessary", "hiding"]),
        ], "Decomposition means breaking a large, complex problem down into smaller sub problems, each of which is easier to understand and solve on its own. Abstraction means removing or hiding detail that is not relevant to the problem you are solving, so that you can concentrate only on what actually matters.",
           command="State"),
        EQ("A school wants a program to record how many students take a packed lunch each day. Describe how decomposition could be used to plan this program.", 4, [
            MP("The problem is broken into smaller sub problems", ["broken", "smaller", "split", "sub problems", "parts"]),
            MP("First sub problem such as entering the class name or date", ["class", "date", "entering", "input", "name"]),
            MP("Second sub problem such as counting or storing the numbers", ["count", "store", "total", "record", "add"]),
            MP("Third sub problem such as displaying or saving a report", ["display", "report", "output", "save", "show", "total"]),
        ], "The overall problem would be broken into several smaller sub problems that can each be solved separately. One sub problem is collecting the input: asking for the date and the class, and entering how many students in that class have a packed lunch. A second is validating and storing that data, checking the number entered is sensible and saving it so it is still there tomorrow. A third is calculating totals, adding up the numbers across all the classes to get a daily figure. A fourth is producing output, displaying the daily total on screen and perhaps saving a weekly summary to a file. Each of these parts is small enough to write and test on its own, and they can then be joined together into the finished program.",
           command="Describe"),
        EQ("Complete a trace table for this algorithm: total = 0, then for i = 1 to 4, total = total + (i * 2), next i. State the final value of total.", 4, [
            MP("After i = 1 total is 2", ["2"]),
            MP("After i = 2 total is 6", ["6"]),
            MP("After i = 3 total is 12", ["12"]),
            MP("Final value of total is 20", ["20"]),
        ], "When i is 1, i times 2 is 2, so total becomes 0 plus 2 which is 2. When i is 2, i times 2 is 4, so total becomes 2 plus 4 which is 6. When i is 3, i times 2 is 6, so total becomes 6 plus 6 which is 12. When i is 4, i times 2 is 8, so total becomes 12 plus 8 which is 20. The final value of total is therefore 20.",
           command="Complete"),
        EQ("Describe the purpose of the diamond and the parallelogram symbols in a flowchart.", 2, [
            MP("The diamond represents a decision with two labelled branches", ["decision", "question", "yes", "no", "two branches"]),
            MP("The parallelogram represents input or output", ["input", "output", "data in", "display"]),
        ], "The diamond represents a decision. It contains a question with a true or false answer and always has exactly two exits, one labelled Yes and one labelled No, so the flow of the algorithm splits depending on the answer. The parallelogram represents input or output, meaning either data being entered into the system, such as a user typing a number, or results being displayed, such as a message shown on screen.",
           command="Describe"),
        EQ("A program accepts a mark between 0 and 100. Give one example each of normal, boundary and erroneous test data, and explain what each tests.", 6, [
            MP("Normal data such as 57", ["normal", "57", "50", "typical", "middle"]),
            MP("Explains that normal data checks the program works with a typical value", ["typical", "should be accepted", "works normally", "usual"]),
            MP("Boundary data such as 0 or 100", ["boundary", "0", "100", "edge", "101", "-1"]),
            MP("Explains that boundary data tests the exact edge of the allowed range", ["edge", "exactly", "limit", "off by one", "just outside"]),
            MP("Erroneous data such as the word hello", ["erroneous", "hello", "letters", "text", "blank", "abc"]),
            MP("Explains that erroneous data checks the program rejects the wrong type without crashing", ["reject", "wrong type", "crash", "error message", "handled"]),
        ], "Normal test data would be a mark of 57. This is a typical value well inside the allowed range, and it tests that the program accepts and processes ordinary input correctly. Boundary test data would be 0 and 100, and also 101, because these sit exactly at the edge of what is allowed. Boundary data is the most valuable kind, since the difference between a condition written as less than 100 and one written as less than or equal to 100 only shows up at exactly that value, and off by one errors are extremely common. Erroneous test data would be entering the word hello. This is the wrong type of data entirely and should never be accepted, so the test checks that the program rejects it with a helpful message rather than crashing when it tries to treat text as a number.",
           command="Give"),
    ],
)

Y8_PYTHON = Topic(
    slug="python-loops-and-lists",
    title="Python: Loops, Lists and Functions",
    spec="Y8.3",
    icon="i-python",
    minutes=30,
    blurb="Moving beyond the basics into for loops, while loops, lists, functions and simple validation. This is the point where you can start writing real programs.",
    fact="The `for` loop in Python does not count on its own. It walks through a collection of items, and `range()` simply makes a collection of numbers for it to walk through. Understanding that makes loops far easier.",
    sections=[
        Section("Loops", """
### for loops

A **for loop** repeats a known number of times.

```python
for i in range(5):
    print("Hello", i)
```

This prints Hello 0 through to Hello 4. That is five times, but it never reaches 5.

```python
range(5)        # 0, 1, 2, 3, 4
range(1, 6)     # 1, 2, 3, 4, 5
range(0, 10, 2) # 0, 2, 4, 6, 8
```

### while loops

A **while loop** repeats for as long as a condition is true. Use it when you do not know how many repetitions are needed.

```python
password = ""
while password != "letmein":
    password = input("Enter the password: ")
print("Welcome")
```

!warn Infinite loops :: If nothing inside the loop can make the condition false, it runs forever. Always check that something inside the loop changes the value being tested.

### Choosing which loop

| Situation | Loop |
| Repeat exactly 10 times | for |
| Loop through every item in a list | for |
| Keep asking until the input is valid | while |
| Run until the player quits | while |
"""),
        Section("Lists", """
A **list** stores many values under one name.

```python
scores = [12, 45, 3, 78, 20]
names = ["Aisha", "Ben", "Chloe"]

print(scores[0])      # 12, the first item
print(scores[4])      # 20, the last item
print(len(scores))    # 5
```

!key Lists start at 0 :: The first item is at index 0, so a list of 5 items has indexes 0 to 4. There is no index 5.

### Changing a list

```python
scores.append(99)     # add to the end
scores[1] = 50        # change the second item
scores.remove(3)      # remove the value 3
del scores[0]         # remove the item at index 0
```

### Looping through a list

```python
for score in scores:
    print(score)
```

### Useful built in functions

```python
print(sum(scores))         # adds them all up
print(max(scores))         # largest
print(min(scores))         # smallest
print(len(scores))         # how many
print(sorted(scores))      # a sorted copy

average = sum(scores) / len(scores)
```
"""),
        Section("Functions and validation", """
### Functions

A **function** is a named block of code you can use over and over.

```python
def area_of_rectangle(width, height):
    return width * height

print(area_of_rectangle(5, 3))     # 15
print(area_of_rectangle(10, 2))    # 20
```

- `def` starts the definition
- `width` and `height` are **parameters**, the values the function needs
- `return` sends an answer back

Some functions do not return anything, they just do something:

```python
def show_menu():
    print("1. Play")
    print("2. Scores")
    print("3. Quit")

show_menu()
```

### Why functions help

- Write the code once and use it many times
- Fix a bug in one place instead of ten
- The program becomes shorter and easier to read
- Each function can be tested on its own

### Validation

**Validation** checks that input is sensible before the program uses it.

```python
age = input("Enter your age: ")

while not age.isdigit() or int(age) < 0 or int(age) > 120:
    print("Please enter a whole number between 0 and 120.")
    age = input("Enter your age: ")

age = int(age)
print("Thank you")
```

This loops until the input is acceptable, rather than crashing.

| Check | What it does |
| Presence check | Something has been entered |
| Range check | The value is between two limits |
| Type check | The data is the right type |
| Length check | The right number of characters |
"""),
    ],
    keyterms=[
        ("for loop", "A loop that repeats a known number of times, or once for each item in a collection."),
        ("while loop", "A loop that repeats for as long as a condition remains true."),
        ("List", "A data structure that stores many values under one name, accessed by index."),
        ("Index", "The position of an item in a list, counting from 0."),
        ("Function", "A named block of code that performs a task and can be called many times."),
        ("Parameter", "A value passed into a function so it can do its work."),
        ("Return", "Sending a result back from a function to the code that called it."),
        ("Validation", "Checking that input is sensible before the program uses it."),
        ("Infinite loop", "A loop whose condition never becomes false, so it never stops."),
    ],
    grade="""
The top level in Year 8 Python is about **choosing the right tool and explaining why**.

**Justify your loop choice.** "I used a while loop because I do not know how many attempts the user will need to type a valid password."

**Use functions before you are told to.** If the same three lines appear twice in your program, make them a function. Being able to spot repetition and remove it is exactly what pattern recognition means in practice.

**Validate everything the user types.** A program that crashes when someone types letters instead of a number is not finished.

+ Explain when to use a for loop and when to use a while loop
+ Write a validation loop that keeps asking until the input is acceptable
+ Write a function with parameters and a return value, and explain each part
+ Loop through a list and calculate the total, average and highest value
""",
    mistakes=[
        "Thinking range(5) includes 5. It gives 0 to 4.",
        "Forgetting that list indexes start at 0, so the last index is one less than the length.",
        "Writing a while loop where nothing inside changes the condition, creating an infinite loop.",
        "Forgetting to use return, so the function calculates the answer and then throws it away.",
        "Initialising a highest score variable to 0 when the values could be negative.",
    ],
    quiz=[
        Q("How many times does `for i in range(4)` repeat?", ["4", "3", "5", "0"], 0,
          "range(4) produces 0, 1, 2 and 3, so the loop body runs four times."),
        Q("What is `scores[0]` if `scores = [10, 20, 30]`?", ["10", "20", "0", "30"], 0,
          "Lists start at index 0, so scores[0] is the first item."),
        Q("Which loop should be used to keep asking until the user types a valid answer?",
          ["A while loop", "A for loop", "A nested for loop", "No loop is needed"], 0,
          "You do not know how many attempts they will need, which is exactly when a while loop is correct."),
        Q("What does `scores.append(50)` do?",
          ["Adds 50 to the end of the list", "Replaces the first item with 50",
           "Removes 50 from the list", "Sorts the list"], 0,
          "append always adds to the end and makes the list one item longer."),
        Q("What does the `return` keyword do in a function?",
          ["Sends a result back to the code that called the function",
           "Prints a value on the screen", "Ends the program", "Starts a loop"], 0,
          "Without return, the function calculates the answer and then discards it."),
        Q("What is wrong with `while x < 10: print(x)` if x is 0?",
          ["x never changes, so it is an infinite loop",
           "print cannot be used inside a while loop",
           "x should be a string", "Nothing is wrong"], 0,
          "Nothing inside the loop changes x, so the condition stays true forever."),
        Q("How would you find the highest value in a list called marks?",
          ["max(marks)", "high(marks)", "marks.top()", "sort(marks)"], 0,
          "max() is a built in function that returns the largest value in a collection."),
        Q("A list has 7 items. What is the index of the last item?", ["6", "7", "8", "0"], 0,
          "Indexes run from 0 to 6, so the last index is always the length minus one."),
        Q("What is validation?",
          ["Checking that input is sensible before the program uses it",
           "Checking the spelling of variable names",
           "Making the program run faster",
           "Saving data to a file"], 0,
          "Validation prevents crashes and nonsense results by rejecting unsuitable input."),
        Q("Why are functions useful?",
          ["Code can be written once and used many times, so it is easier to fix",
           "They make the program run at a higher clock speed",
           "They remove the need for variables",
           "They automatically validate input"], 0,
          "Avoiding duplication means a change or a bug fix happens in one place instead of many."),
    ],
    exam=[
        EQ("State the difference between a for loop and a while loop.", 2, [
            MP("A for loop repeats a known number of times", ["known", "set number", "fixed", "specific number"]),
            MP("A while loop repeats while a condition is true, and the number of repetitions may not be known", ["condition", "while", "until", "not known", "unknown"]),
        ], "A for loop repeats a known, fixed number of times, or once for every item in a collection such as a list. A while loop repeats for as long as a condition remains true, so the number of repetitions is not necessarily known in advance and depends on what happens while the program runs.",
           command="State"),
        EQ("Write a Python program that asks the user for five numbers, stores them in a list, and then prints the total and the average.", 5, [
            MP("Creates an empty list", ["= []", "list", "empty"]),
            MP("Uses a for loop to repeat five times", ["for", "range(5)", "loop", "5"]),
            MP("Takes input and converts it to a number", ["int(input", "input", "convert"]),
            MP("Adds each number to the list", ["append", "add", "store"]),
            MP("Calculates and prints the total and average", ["sum", "total", "len", "average", "print", "/ 5"]),
        ], "numbers = []\n\nfor i in range(5):\n    value = int(input(\"Enter a number: \"))\n    numbers.append(value)\n\ntotal = sum(numbers)\naverage = total / len(numbers)\n\nprint(\"Total:\", total)\nprint(\"Average:\", average)\n\nAn empty list is created first. The for loop runs five times, and each time it reads a number, converts it from the text returned by input into an integer, and appends it to the list. After the loop the built in sum function adds up the list and dividing by len gives the average.",
           command="Write"),
        EQ("Explain what validation is and describe one validation check that could be used when asking for a percentage mark.", 3, [
            MP("Validation checks that input is sensible before it is used", ["checks", "sensible", "before", "suitable", "acceptable"]),
            MP("Names a suitable check such as a range check", ["range check", "type check", "presence check", "between"]),
            MP("Explains the check, such as ensuring the value is between 0 and 100", ["0 and 100", "between", "not negative", "not above", "whole number"]),
        ], "Validation means checking that the data a user has entered is sensible and in the expected form before the program tries to use it, so that the program does not crash or produce meaningless results. For a percentage mark, a range check would be used to confirm that the value entered is between 0 and 100 inclusive, since a mark of 150 or -20 is impossible. A type check would also be needed to confirm that a whole number has been entered rather than letters, because trying to convert text such as hello into a number would cause the program to crash.",
           command="Explain"),
        EQ("Explain two reasons why a programmer would use functions in a program.", 4, [
            MP("Code can be written once and called many times", ["once", "reuse", "many times", "repeat", "call"]),
            MP("This avoids duplication so the program is shorter", ["shorter", "duplication", "less code", "tidier"]),
            MP("If a change is needed it only has to be made in one place", ["one place", "easier to fix", "change once", "maintain"]),
            MP("Each function can be tested on its own, making errors easier to find", ["test", "separately", "on its own", "find errors", "debug"]),
        ], "The first reason is that a function lets code be written once and then used as many times as needed, simply by calling its name. This avoids the same lines being copied out repeatedly, so the program is much shorter and easier to read, and crucially it means that if the code ever needs correcting or changing, the edit is made in one place rather than being repeated everywhere the code appears. The second reason is that functions make a program much easier to develop and test. Each function does one clearly defined job, so it can be tested on its own with different inputs until it is known to work, which makes faults far easier to locate than in one long program where everything is mixed together.",
           command="Explain"),
        EQ("A program uses `while count < 10:` and prints count inside the loop, but the program never stops. Explain why and how to fix it.", 3, [
            MP("The value of count is never changed inside the loop", ["never changed", "not increased", "stays the same", "not updated"]),
            MP("So the condition remains true forever and the loop never ends", ["always true", "never false", "forever", "infinite"]),
            MP("Fix by adding a line inside the loop that increases count", ["count = count + 1", "count += 1", "increase", "increment", "add 1"]),
        ], "The loop never stops because nothing inside it changes the value of count. The condition count less than 10 is tested before every repetition, but since count keeps the same value it stays true forever, producing an infinite loop that prints the same number endlessly. The fix is to add a line inside the loop that increases count each time, such as count = count + 1, so that count rises towards 10 and the condition eventually becomes false, allowing the loop to end.",
           command="Explain"),
    ],
)

Y8_SPREAD = Topic(
    slug="spreadsheets",
    title="Spreadsheets and Data Modelling",
    spec="Y8.4",
    icon="i-grid",
    minutes=26,
    blurb="Formulas, functions, absolute and relative references, conditional logic and charts. Spreadsheets are the most widely used programming tool on Earth.",
    fact="A spreadsheet is a program. Every formula is a small piece of code, and a spreadsheet with logic in it is a working computer model. The first one, VisiCalc, sold so many Apple II computers that it is credited with creating the personal computer market.",
    sections=[
        Section("Formulas and functions", """
Every formula starts with an **equals sign**. Without it, the spreadsheet treats what you type as text.

```text
=B2+C2
=B2*0.2
=(B2+C2+D2)/3
```

### Cell references

Referring to a **cell** rather than typing a number means the formula updates automatically when the data changes. This is the single most important idea in spreadsheets.

Bad: `=45*0.2`
Good: `=B2*0.2`

### Common functions

| Function | What it does | Example |
| `SUM` | Adds a range | `=SUM(B2:B20)` |
| `AVERAGE` | Mean of a range | `=AVERAGE(B2:B20)` |
| `MAX` | Largest value | `=MAX(B2:B20)` |
| `MIN` | Smallest value | `=MIN(B2:B20)` |
| `COUNT` | How many cells contain numbers | `=COUNT(B2:B20)` |
| `COUNTIF` | How many meet a condition | `=COUNTIF(B2:B20,">50")` |
| `ROUND` | Rounds to a number of decimals | `=ROUND(B2,2)` |
| `IF` | Chooses between two results | `=IF(B2>=50,"Pass","Fail")` |

### The IF function

    =IF(condition, value if true, value if false)

```text
=IF(B2>=50,"Pass","Fail")
=IF(C2>100,"Over budget","Within budget")
```

IFs can be nested for more than two outcomes:

```text
=IF(B2>=70,"Merit",IF(B2>=50,"Pass","Fail"))
```
"""),
        Section("Absolute and relative references", """
This is the idea that separates people who fight with spreadsheets from people who use them properly.

### Relative references

`B2` is **relative**. Copy the formula down one row and it becomes `B3`. Copy it right one column and it becomes `C2`.

This is usually what you want. A column of totals copied down should refer to each row in turn.

### Absolute references

`$B$2` is **absolute**. The dollar signs lock it, so copying the formula never changes it.

Use this when every row must refer to the **same** cell, such as a VAT rate stored once at the top of the sheet.

```text
=B2*$E$1        copied down becomes =B3*$E$1, =B4*$E$1
=B2*E1          copied down becomes =B3*E2, =B4*E3   which is wrong
```

### Mixed references

- `$B2` locks the column but not the row
- `B$2` locks the row but not the column

!key How to spot when you need an absolute reference :: If a formula works in the first row and produces nonsense when copied down, you almost certainly needed dollar signs on a reference that should not have moved.
"""),
        Section("Modelling, charts and good design", """
### What a model is

A spreadsheet **model** represents a real situation so you can ask what if questions.

Examples: a household budget, the cost of running a school trip, projected profits for a business, the population of an island over ten years.

The point of a model is that you change one input and every dependent figure updates instantly. Working out the effect of a 10 per cent price rise takes one keystroke rather than an hour with a calculator.

### Choosing a chart

| Chart | Best for |
| Bar or column | Comparing separate categories |
| Line | Showing change over time |
| Pie | Showing parts of one whole, with only a few categories |
| Scatter | Showing whether two things are related |

Every chart needs a **title**, **axis labels** and, where there is more than one series, a **legend**. A chart without labels communicates nothing.

!warn Do not use a pie chart for ten categories :: The slices become impossible to compare. Pie charts work with three or four segments at most.

### Designing a good spreadsheet

- Put **inputs** together at the top or on a separate sheet, clearly labelled
- Never bury a number inside a formula. Put it in a cell and reference it.
- Use headings, borders and shading so the structure is visible
- Format currency, percentages and dates properly
- Use **conditional formatting** to highlight important values automatically
- Freeze the header row so it stays visible while scrolling
- Use **data validation** to restrict what can be typed into a cell
"""),
    ],
    keyterms=[
        ("Formula", "A calculation in a cell, always beginning with an equals sign."),
        ("Function", "A built in operation such as SUM or AVERAGE that performs a common calculation."),
        ("Cell reference", "The address of a cell, such as B2, used in a formula."),
        ("Relative reference", "A reference that changes when the formula is copied to another cell."),
        ("Absolute reference", "A reference locked with dollar signs so it does not change when copied."),
        ("Range", "A block of cells, written as the top left and bottom right separated by a colon."),
        ("Model", "A spreadsheet that represents a real situation so that what if questions can be asked."),
        ("Conditional formatting", "Automatically changing the appearance of a cell based on its value."),
        ("Data validation", "Restricting what can be entered into a cell to prevent invalid data."),
    ],
    grade="""
The top level here comes from **explaining why a spreadsheet is the right tool**, not just using one.

**Explain the power of cell references.** A model built on cell references updates every dependent figure the instant an input changes, which is the entire reason spreadsheets exist. Typing numbers into formulas throws that away.

**Justify your chart choice.** "A line chart because the data shows change over time, and the trend is what matters more than the individual values."

**Explain absolute references properly.** Say what would go wrong without them: the reference would shift down with each row and point at an empty or wrong cell.

+ Write an IF formula with a sensible condition and two outcomes
+ Explain when to use an absolute reference and what goes wrong without one
+ Choose and justify a chart type for a given set of data
+ Design a model with clearly separated inputs and calculations
""",
    mistakes=[
        "Forgetting the equals sign, so the spreadsheet stores the formula as text.",
        "Typing values directly into formulas instead of referencing a cell.",
        "Copying a formula down without an absolute reference, so a fixed value slides down the column.",
        "Using a pie chart for data that is not parts of one whole.",
        "Producing a chart with no title and no axis labels.",
    ],
    quiz=[
        Q("What must every formula start with?", ["=", "+", "#", "$"], 0,
          "Without the equals sign the spreadsheet treats what you typed as ordinary text."),
        Q("What does `=SUM(B2:B10)` do?",
          ["Adds up all the values from B2 to B10", "Counts the cells from B2 to B10",
           "Finds the average of B2 to B10", "Finds the largest of B2 to B10"], 0,
          "SUM adds a range. The colon means everything from the first cell to the last."),
        Q("What is the difference between B2 and $B$2 when a formula is copied?",
          ["$B$2 stays the same, B2 changes to match the new position",
           "B2 stays the same, $B$2 changes",
           "They behave identically",
           "$B$2 makes the value a currency"], 0,
          "The dollar signs lock the reference so it cannot move when the formula is copied."),
        Q("Which formula would display Pass for 50 or more, and Fail otherwise?",
          ["=IF(B2>=50,\"Pass\",\"Fail\")", "=IF(B2>50,\"Pass\",\"Fail\")",
           "=IF(B2=50,\"Pass\",\"Fail\")", "=SUM(B2>=50)"], 0,
          "Greater than or equal to includes exactly 50, which the question requires."),
        Q("Which chart type is best for showing how sales changed each month over a year?",
          ["Line", "Pie", "Scatter", "Doughnut"], 0,
          "Line charts show change over time, which is exactly what monthly sales data represents."),
        Q("A VAT rate is stored in cell E1 and a formula in C2 is `=B2*E1`. What happens when it is copied down?",
          ["E1 becomes E2, E3 and so on, which gives wrong answers",
           "It works correctly",
           "The spreadsheet shows an error message",
           "The VAT rate doubles"], 0,
          "E1 is a relative reference, so it slides down with the formula. It should be written as $E$1."),
        Q("What does `=COUNTIF(B2:B20,\">50\")` do?",
          ["Counts how many cells in the range hold a value above 50",
           "Adds up all values above 50",
           "Finds the largest value above 50",
           "Highlights cells above 50"], 0,
          "COUNTIF counts cells meeting a condition. SUMIF would add them up instead."),
        Q("Why should values be put in cells rather than typed into formulas?",
          ["Changing the value once updates every formula that uses it",
           "Formulas cannot contain numbers",
           "It makes the file smaller",
           "It makes the spreadsheet calculate faster"], 0,
          "A single input cell referenced everywhere means a change ripples through the whole model instantly."),
        Q("What is conditional formatting?",
          ["Automatically changing a cell's appearance based on its value",
           "Formatting a cell as currency",
           "Restricting what can be typed into a cell",
           "Adding a chart to a spreadsheet"], 0,
          "It highlights important values automatically, for example colouring every mark below 40 in red."),
        Q("A spreadsheet is used to work out the effect of a price rise on profit. What is this an example of?",
          ["Modelling", "Validation", "Formatting", "Compression"], 0,
          "A model represents a real situation so that what if questions can be answered quickly."),
    ],
    exam=[
        EQ("State what a formula in a spreadsheet must begin with, and give one example of a formula that adds cells B2 and C2.", 2, [
            MP("A formula must begin with an equals sign", ["equals", "=", "equal sign"]),
            MP("Correct example such as =B2+C2", ["=b2+c2", "b2+c2", "=sum(b2:c2)"]),
        ], "Every formula must begin with an equals sign, which is what tells the spreadsheet that the contents of the cell should be calculated rather than treated as ordinary text. An example that adds cells B2 and C2 together is =B2+C2.",
           command="State"),
        EQ("Explain the difference between a relative and an absolute cell reference, and give an example of when an absolute reference is needed.", 4, [
            MP("A relative reference changes when the formula is copied", ["changes", "adjusts", "moves", "updates", "shifts"]),
            MP("An absolute reference stays the same because it is locked with dollar signs", ["stays", "does not change", "locked", "dollar", "$", "fixed"]),
            MP("Gives an example such as a VAT rate or a fixed price stored in one cell", ["vat", "rate", "fixed value", "one cell", "constant", "tax"]),
            MP("Explains that without the dollar signs the reference would move and give wrong results", ["move", "wrong", "empty cell", "incorrect", "slide", "shift down"]),
        ], "A relative reference such as B2 adjusts automatically when a formula is copied, so copying a formula down one row changes B2 to B3. This is usually what you want, because each row of a calculation should refer to its own data. An absolute reference such as $E$1 is locked by the dollar signs, so it stays pointing at exactly the same cell no matter where the formula is copied. An absolute reference is needed when every row must refer to the same single value, for example a VAT rate stored once in cell E1. If the formula were written as =B2*E1 and copied down, the reference would slide to E2, then E3, which are empty cells, so every result after the first row would be wrong.",
           command="Explain"),
        EQ("Write a formula that displays Merit if the mark in B2 is 70 or above, Pass if it is 50 or above, and Fail otherwise.", 3, [
            MP("Uses a nested IF function", ["if(", "nested", "if within"]),
            MP("Tests the highest condition first", ["70", ">=70", "merit first"]),
            MP("Correct outcomes for all three cases", ["merit", "pass", "fail"]),
        ], "=IF(B2>=70,\"Merit\",IF(B2>=50,\"Pass\",\"Fail\"))\n\nThe outer IF tests the most restrictive condition first, so a mark of 85 is correctly given Merit. Only if that condition is false does the spreadsheet evaluate the inner IF, which then checks for 50 or above and gives Pass, with Fail as the final alternative. Testing the conditions in the wrong order would mean a mark of 85 was caught by the 50 test and wrongly labelled Pass.",
           command="Write"),
        EQ("A student has created a spreadsheet to model the cost of a school trip. Explain two features of a well designed spreadsheet model.", 4, [
            MP("Input values are kept in clearly labelled cells rather than inside formulas", ["input", "separate", "labelled", "own cells", "not in formulas"]),
            MP("So a value can be changed once and every calculation updates", ["change once", "updates", "automatically", "recalculates", "what if"]),
            MP("Cell references are used in formulas rather than typed numbers", ["cell references", "references", "not typed numbers", "refer to cells"]),
            MP("Formatting such as currency, headings and conditional formatting makes it clear and reduces errors", ["formatting", "currency", "headings", "conditional", "clear", "readable"]),
        ], "The first feature is that all the input values, such as the coach hire cost, the entry price per student and the number of students, are kept in their own clearly labelled cells, usually grouped together at the top or on a separate sheet. This means the model can answer what if questions instantly: changing the number of students in one cell updates every dependent calculation automatically, which is the entire point of building a model rather than working the figures out by hand. The second feature is that every formula uses cell references rather than typed numbers, so no value is buried where it cannot be seen or updated. Alongside this, sensible formatting matters: currency values formatted as currency, clear headings and borders so the structure is obvious, and conditional formatting to highlight if the total goes over budget, all of which make the model easier to read and much less likely to be misused.",
           command="Explain"),
        EQ("A spreadsheet records the temperature recorded each day for a month. Recommend a suitable chart type and justify your choice.", 3, [
            MP("Recommends a line chart", ["line chart", "line graph"]),
            MP("The data shows change over time", ["over time", "each day", "trend", "time series", "days"]),
            MP("A line chart makes the trend and any patterns easy to see", ["trend", "pattern", "rise", "fall", "easy to see", "clear"]),
        ], "A line chart is the most suitable choice. The data consists of one measurement taken at regular intervals across a month, so it is a time series, and a line chart is specifically designed to show how a value changes over time. Joining the points with a line makes any trend immediately visible, so it is easy to see whether temperatures rose through the month, whether there was a cold spell, and how much the values varied day to day. A pie chart would be completely unsuitable because the daily temperatures are not parts of a single whole, and a bar chart, while readable, would make the overall trend harder to follow than a continuous line.",
           command="Recommend"),
    ],
)

Y8_NETWORKS = Topic(
    slug="networks-and-cyber-security",
    title="Networks and Cyber Security",
    spec="Y8.5",
    icon="i-network",
    minutes=28,
    blurb="How computers talk to each other, what happens when you type a web address, and the attacks and defences you need to understand.",
    fact="When you load a web page, the data is broken into packets that may each take a completely different route across the world and arrive out of order. Your computer reassembles them so fast that it looks instant.",
    sections=[
        Section("Networks", """
A **network** is two or more computers connected so they can share data and resources.

### LAN and WAN

- **LAN**, local area network, covers a small area such as one school or one house, and the organisation owns the equipment.
- **WAN**, wide area network, covers a large area such as a whole country. The internet is the largest WAN in the world.

### Why network computers

- Share files and work
- Share hardware such as printers, which saves money
- Share one internet connection
- Back up everything centrally
- Manage user accounts and updates from one place

The downsides are the cost of setting it up, the fact that malware spreads quickly across a network, and that if the server fails everyone is affected.

### The hardware

| Device | Job |
| **Router** | Connects different networks together and directs data between them |
| **Switch** | Connects devices within one network and sends data only to the right device |
| **NIC** | Network interface card, letting a device connect to a network at all |
| **WAP** | Wireless access point, letting devices connect without cables |
| **Server** | A powerful computer that provides files, web pages or other services |

### Wired and wireless

| | Wired | Wireless |
| Speed | Faster and more consistent | Slower and more variable |
| Reliability | Very reliable | Signal weakens with distance and through walls |
| Security | More secure, physical access needed | Less secure, signal travels through the air |
| Convenience | Devices cannot move | Devices can move freely |
"""),
        Section("The internet and the web", """
!warn The internet and the web are not the same :: The **internet** is the global network of connected computers. The **World Wide Web** is one service that runs on it, made of web pages linked together. Email, streaming and online gaming also run on the internet but are not part of the web.

### What happens when you type an address

1. You type `www.example.com` into a browser.
2. Your computer asks a **DNS** server to look up the **IP address** for that name, because computers route by number, not by name.
3. DNS replies with something like `93.184.216.34`.
4. Your computer sends a request to that address.
5. The web server sends back the page, broken into **packets**.
6. Packets travel by different routes and may arrive out of order.
7. Your computer reassembles them in the right order and the browser displays the page.

### Packets

Data is split into small **packets**. Each contains:

- Part of the data
- The destination address
- The sender's address
- A packet number, so they can be reassembled in order

Splitting data up means a single large file cannot block the network, and if one packet is lost only that packet needs resending rather than the whole file.

### IP addresses and protocols

An **IP address** identifies a device on a network. A **protocol** is a set of rules for how data is sent, so that different computers can understand each other.

- **HTTP** transfers web pages
- **HTTPS** does the same but encrypted, so intercepted data cannot be read
- **TCP/IP** splits data into packets, addresses them and makes sure they all arrive
- **SMTP** sends email, and **IMAP** retrieves it
"""),
        Section("Cyber security", """
### Threats

| Threat | How it works |
| **Virus** | Attaches to a file and spreads when that file is opened or shared |
| **Worm** | Spreads across a network by itself, with no user action needed |
| **Trojan** | Pretends to be useful software so the user installs it willingly |
| **Ransomware** | Encrypts your files and demands payment to unlock them |
| **Spyware** | Secretly records what you do, including what you type |
| **Phishing** | A fake message tricking you into giving away your details |
| **Brute force** | Trying millions of password combinations automatically |
| **DoS attack** | Flooding a server with requests so real users cannot get through |

### Defences

| Defence | What it does |
| **Anti malware software** | Scans files against known threats and removes them. Must be kept updated. |
| **Firewall** | Checks traffic entering and leaving the network and blocks anything against its rules |
| **Strong passwords** | Long and unguessable, defeating brute force attacks |
| **Two factor authentication** | A stolen password alone is not enough to log in |
| **Encryption** | Scrambles data so intercepted information cannot be read |
| **User access levels** | Each person can only reach what their role needs |
| **Backups** | Data can be restored after ransomware or hardware failure |
| **Software updates** | Close the security holes that malware exploits |

!key Encryption does not prevent interception :: It makes intercepted data useless, because without the key it is meaningless. That distinction matters, and it earns marks.

### The weakest point is always a person

The most sophisticated firewall in the world cannot stop an employee who types their password into a convincing fake login page. This is why **training** is a genuine security measure, not an afterthought.
"""),
    ],
    keyterms=[
        ("Network", "Two or more computers connected so they can share data and resources."),
        ("LAN", "Local area network, covering a small area with hardware owned by the organisation."),
        ("WAN", "Wide area network, covering a large geographical area. The internet is the largest."),
        ("Router", "A device that connects different networks and directs data between them."),
        ("Switch", "A device that connects computers within one network and sends data only to the intended device."),
        ("Packet", "A small piece of data sent across a network, containing addresses and a sequence number."),
        ("IP address", "A number identifying a device on a network."),
        ("DNS", "The Domain Name System, which converts a web address into an IP address."),
        ("Protocol", "A set of rules governing how data is sent between devices."),
        ("Encryption", "Scrambling data with a key so it cannot be understood by anyone who intercepts it."),
        ("Firewall", "Hardware or software that inspects network traffic and blocks anything against its rules."),
    ],
    grade="""
The top level here is about **explaining mechanisms**.

**Say what a device actually does.** Not "a router connects to the internet", but "a router connects two different networks and uses IP addresses to decide where each packet should be sent next".

**Explain why packets are used.** Because a large file split into packets cannot block the network for everyone else, and because if one packet is lost only that packet has to be resent.

**Match the defence to the threat.** A firewall does not stop phishing, because phishing works on the person rather than the network. The defence there is training.

+ Explain the difference between the internet and the World Wide Web
+ Describe what happens between typing a web address and the page appearing
+ Explain the difference between a virus and a worm
+ Match any threat to the defence that actually addresses it
""",
    mistakes=[
        "Using the words internet and web as if they mean the same thing.",
        "Saying a switch and a router do the same job. A switch works inside one network, a router works between networks.",
        "Saying encryption stops data being intercepted. It stops it being understood.",
        "Recommending antivirus software as the defence against phishing, which attacks the person rather than the machine.",
        "Saying a virus and a worm are the same. A worm spreads on its own with no user action.",
    ],
    quiz=[
        Q("What is the difference between the internet and the World Wide Web?",
          ["The internet is the network, the web is one service that runs on it",
           "They are the same thing",
           "The web is the network and the internet is a service",
           "The internet is wired and the web is wireless"], 0,
          "Email, streaming and gaming also use the internet, but they are not part of the web."),
        Q("What does DNS do?",
          ["Converts a web address into an IP address", "Encrypts web traffic",
           "Blocks unwanted network traffic", "Splits data into packets"], 0,
          "Computers route by number, so the human readable name must be looked up first."),
        Q("Which device connects two different networks together?",
          ["A router", "A switch", "A network interface card", "A wireless access point"], 0,
          "Routers work between networks. Switches work within one network."),
        Q("Why is data split into packets?",
          ["One large file cannot block the network, and only lost packets need resending",
           "Packets are encrypted automatically",
           "It makes the file smaller",
           "Routers can only handle small files"], 0,
          "Splitting data shares the network fairly and makes recovery from errors far more efficient."),
        Q("What is the difference between a virus and a worm?",
          ["A worm spreads by itself, a virus needs a user to open an infected file",
           "A virus spreads by itself, a worm needs a user",
           "A worm only affects phones",
           "There is no difference"], 0,
          "Self spreading is what makes worms so fast at infecting a whole network."),
        Q("What does a firewall do?",
          ["Checks traffic entering and leaving and blocks anything against its rules",
           "Scans files for viruses",
           "Encrypts data before sending it",
           "Backs up important files"], 0,
          "A firewall is a traffic filter. Scanning files is what anti malware software does."),
        Q("Which defence is most effective against staff being tricked by fake emails?",
          ["Training staff to recognise phishing", "A stronger firewall",
           "A faster internet connection", "More storage space"], 0,
          "Phishing attacks the person, so the defence has to address the person too."),
        Q("What does HTTPS provide that HTTP does not?",
          ["The data is encrypted so it cannot be read if intercepted",
           "Pages load faster", "It works without an IP address", "It uses fewer packets"], 0,
          "The S stands for secure, and it means anyone capturing the traffic sees only scrambled data."),
        Q("Which is an advantage of a wired connection over wireless?",
          ["Faster and more reliable, and more secure", "Devices can move around freely",
           "It is cheaper to install in an old building", "It works through walls better"], 0,
          "Cable gives higher and steadier speeds with no interference, and needs physical access to tap."),
        Q("What is ransomware?",
          ["Malware that encrypts your files and demands payment to unlock them",
           "Software that records what you type",
           "A fake email asking for your password",
           "Flooding a server so it cannot respond"], 0,
          "Regular backups are the best defence, because you can restore rather than pay."),
    ],
    exam=[
        EQ("State two differences between a LAN and a WAN.", 2, [
            MP("A LAN covers a small area and a WAN covers a large geographical area", ["small", "large", "area", "geographical", "one building", "country"]),
            MP("LAN equipment is owned by the organisation, WAN infrastructure is not", ["owned", "not owned", "leased", "rented", "third party"]),
        ], "A LAN covers a small geographical area such as a single school or house, whereas a WAN covers a large area and may span whole countries, with the internet being the largest example. In addition, the organisation using a LAN owns all of the cabling and hardware itself, while a WAN uses infrastructure belonging to other companies.",
           command="State"),
        EQ("Describe what happens when a user types a web address into a browser and presses enter.", 4, [
            MP("The browser asks a DNS server to look up the address", ["dns", "look up", "domain name"]),
            MP("DNS returns the IP address of the web server", ["ip address", "returns", "number", "address"]),
            MP("A request is sent to that IP address and the server responds", ["request", "sends", "server", "responds", "returns the page"]),
            MP("The page is sent as packets which are reassembled by the browser", ["packets", "reassembled", "put back together", "order"]),
        ], "When the user presses enter, the browser first needs to turn the human readable address into a number, because networks route data by IP address rather than by name. It therefore sends a request to a DNS server, which looks the name up and returns the IP address of the web server. The browser then sends a request to that IP address asking for the page. The web server responds by sending the page back, but the data is split into small packets, each carrying a sequence number and the destination address. These packets may travel by different routes and arrive out of order, so the receiving computer uses the sequence numbers to reassemble them correctly before the browser displays the finished page.",
           command="Describe"),
        EQ("Explain why data is split into packets when sent across a network.", 3, [
            MP("Large files would otherwise block the network for other users", ["block", "hog", "monopolise", "other users", "share"]),
            MP("Packets can take different routes, using the network efficiently", ["different routes", "efficient", "alternative", "spread"]),
            MP("If a packet is lost only that packet needs resending, not the whole file", ["lost", "resend", "only that", "not the whole", "corrupted"]),
        ], "Splitting data into packets means that a single very large file cannot occupy a connection completely and block everyone else, because packets from different transfers can be interleaved and the network is shared fairly. Packets can also travel by different routes depending on which parts of the network are congested, which uses the available capacity efficiently and means a fault on one route does not stop the transfer. Finally, if a packet is damaged or lost in transit, only that individual packet has to be sent again rather than the entire file, which is far quicker and far less wasteful.",
           command="Explain"),
        EQ("A school is worried about malware on its network. Describe three measures it could take.", 6, [
            MP("Install anti malware software", ["anti malware", "antivirus", "scanner"]),
            MP("Keep it updated so new threats are recognised", ["updated", "up to date", "new threats", "latest"]),
            MP("Use a firewall to filter network traffic", ["firewall", "filter", "block traffic"]),
            MP("Restrict user access levels so students cannot install software", ["access levels", "permissions", "cannot install", "restrict", "rights"]),
            MP("Train staff and students to recognise suspicious emails and links", ["train", "educate", "awareness", "suspicious", "recognise"]),
            MP("Keep backups so data can be restored if it is encrypted or lost", ["backup", "restore", "copies", "recover"]),
        ], "The first measure is to install anti malware software on every computer and set it to update automatically. This scans files against a database of known malware and removes or quarantines anything it finds, but because new malware appears constantly the software is only effective if that database is kept current. The second measure is to use a firewall between the school network and the internet. A firewall examines all the traffic going in and out and blocks anything that does not match its rules, which stops many threats reaching the network at all and prevents malware that does get in from communicating with outside servers. The third measure is to set user access levels so that students, and most staff, cannot install software or change system files. That means that even if someone is tricked into running something harmful, it only has the limited permissions of that account and cannot spread across the whole system. Alongside these, training people to recognise suspicious emails addresses the route most infections actually take, and keeping regular backups means that if ransomware does encrypt the school's files they can be restored rather than paid for.",
           command="Describe"),
        EQ("Explain the purpose of encryption and state whether it prevents data from being intercepted.", 3, [
            MP("Encryption scrambles data using a key", ["scrambles", "key", "codes", "converts", "cipher"]),
            MP("Without the key the data cannot be understood", ["cannot be understood", "unreadable", "meaningless", "without the key"]),
            MP("It does not prevent interception, it makes intercepted data useless", ["does not prevent", "still intercepted", "useless", "cannot read it", "no use"]),
        ], "Encryption scrambles data using a key so that what is actually transmitted is a meaningless sequence of characters. Only someone who has the correct key can convert it back into the original information, so an attacker who captures the traffic cannot understand any of it. Encryption does not prevent data from being intercepted: anyone in a position to capture the traffic can still capture it. What encryption does is make that interception pointless, because the attacker ends up with data they cannot read.",
           command="Explain"),
    ],
)

Y8_WEB = Topic(
    slug="web-development",
    title="Web Development",
    spec="Y8.6",
    icon="i-web",
    minutes=28,
    blurb="HTML for structure and CSS for style, how a browser turns your code into a page, and how to build a site that works for everyone.",
    fact="The very first web page is still online at its original address, published in 1991. It is plain text with a few links and no styling at all, because CSS had not been invented yet.",
    sections=[
        Section("HTML: structure", """
**HTML**, HyperText Markup Language, describes the **structure** of a page. It says what things are, not what they look like.

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <title>My First Page</title>
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <h1>Welcome</h1>
  <p>This is a paragraph of text.</p>
  <img src="cat.jpg" alt="A ginger cat asleep on a keyboard">
  <a href="page2.html">Go to page two</a>
</body>
</html>
```

### Key elements

| Tag | Purpose |
| `<h1>` to `<h6>` | Headings, h1 most important |
| `<p>` | A paragraph |
| `<a href="...">` | A link |
| `<img src="..." alt="...">` | An image |
| `<ul>` and `<li>` | An unordered list and its items |
| `<ol>` and `<li>` | A numbered list |
| `<div>` | A block section of the page |
| `<span>` | A small inline section |
| `<table>`, `<tr>`, `<td>` | A table, a row, a cell |

### Rules

- Most tags come in pairs: `<p>` opens and `</p>` closes
- Tags must be **nested** correctly. `<p><strong>text</strong></p>` is right, `<p><strong>text</p></strong>` is wrong
- Some tags are self closing, such as `<img>` and `<br>`
- The `alt` attribute on an image is **not optional**. Screen readers use it, and it displays if the image fails to load.

!key Structure and style are separate jobs :: HTML says what something is. CSS says what it looks like. Keeping them separate means you can restyle an entire website by editing one CSS file.
"""),
        Section("CSS: style", """
**CSS**, Cascading Style Sheets, controls **appearance**.

```css
body {
  font-family: Arial, sans-serif;
  background-color: #f4f4f4;
  color: #222222;
}

h1 {
  color: #03969d;
  text-align: center;
}

p {
  font-size: 16px;
  line-height: 1.6;
}

.highlight {
  background-color: yellow;
  padding: 10px;
}

#header {
  border-bottom: 2px solid #83749f;
}
```

### Selectors

| Selector | Selects |
| `p` | Every paragraph |
| `.highlight` | Every element with `class="highlight"` |
| `#header` | The single element with `id="header"` |

Use a **class** when several elements share a style. Use an **id** when there is exactly one such element on the page.

### Common properties

- `color` sets the text colour, `background-color` sets the background
- `font-family`, `font-size`, `font-weight`
- `margin` is space outside an element, `padding` is space inside it
- `border`, `text-align`, `width`, `height`

### Where CSS goes

- **External** in a separate `.css` file linked from the head. Best, because one file styles every page.
- **Internal** inside `<style>` tags in the head. Only affects that page.
- **Inline** using a `style` attribute on a tag. Avoid it, because it mixes structure with style and cannot be reused.
"""),
        Section("Building a site people can use", """
### Accessibility

A website should work for everyone, including people using a screen reader, people who cannot use a mouse, and people with limited vision.

- **Alt text on every image** that carries meaning
- **Good colour contrast** between text and background
- **Headings in order**, h1 then h2 then h3, because screen readers use them to navigate
- **Links that describe their destination.** "Read the safety guidance" is useful, "click here" is not.
- Everything reachable by **keyboard**, not just by mouse
- Text that can be **enlarged** without the layout breaking

### Navigation

- The same navigation on every page, in the same place
- No more than a few clicks to reach anything
- The user should always be able to tell where they are

### Testing

- Check every link works
- View the site on a phone as well as a computer
- Ask someone else to find something on it and watch where they struggle
- Check it still makes sense with images turned off

!warn Do not judge your own site :: You know where everything is because you built it. Watching one other person try to use it will teach you more than an hour of looking at it yourself.
"""),
    ],
    keyterms=[
        ("HTML", "HyperText Markup Language, used to describe the structure and content of a web page."),
        ("CSS", "Cascading Style Sheets, used to control the appearance of a web page."),
        ("Tag", "An HTML instruction written in angle brackets, usually in an opening and closing pair."),
        ("Attribute", "Extra information inside a tag, such as href on a link or src on an image."),
        ("Class", "A CSS selector used to style several elements that share the same appearance."),
        ("Id", "A CSS selector used to style one unique element on a page."),
        ("Alt text", "A written description of an image, used by screen readers and shown if the image fails to load."),
        ("External stylesheet", "A separate CSS file linked from a page so one file can style an entire website."),
        ("Accessibility", "Designing so that a website can be used by everyone, including people with disabilities."),
    ],
    grade="""
The top level here is about **explaining why**, not just knowing which tag does what.

**Explain the separation of HTML and CSS properly.** HTML defines structure and CSS defines appearance, and keeping them separate means a single external stylesheet can restyle a hundred page site in one edit.

**Justify class against id.** A class can be used many times, an id identifies one unique element. Using an id for something that appears repeatedly is invalid.

**Take accessibility seriously.** Alt text is not a box to tick. Without it, a person using a screen reader has no idea what the image shows, and the page becomes unusable to them.

+ Write valid HTML with correctly nested tags
+ Write CSS using an element selector, a class and an id
+ Explain three ways to make a website accessible and why each matters
+ Explain the advantage of an external stylesheet over inline styles
""",
    mistakes=[
        "Forgetting to close tags, or closing them in the wrong order.",
        "Leaving out alt text on images.",
        "Using inline styles everywhere, which makes the site impossible to restyle consistently.",
        "Using the same id on more than one element. Ids must be unique.",
        "Using headings for their size rather than their meaning, which breaks screen reader navigation.",
    ],
    quiz=[
        Q("What does HTML control on a web page?",
          ["The structure and content", "The colours and fonts",
           "The server the page is stored on", "How fast the page loads"], 0,
          "HTML says what things are. CSS controls how they look."),
        Q("Which tag creates a link?", ["<a>", "<link>", "<href>", "<p>"], 0,
          "The anchor tag with an href attribute creates a hyperlink."),
        Q("What is the purpose of the alt attribute on an image?",
          ["It describes the image for screen readers and if the image fails to load",
           "It sets the image size", "It links the image to a page", "It sets the border colour"], 0,
          "Without alt text, a person using a screen reader has no idea what the image shows."),
        Q("Which CSS selector targets every element with class=\"note\"?",
          [".note", "#note", "note", "<note>"], 0,
          "A full stop selects a class. A hash selects an id."),
        Q("What is the main advantage of an external stylesheet?",
          ["One file can style every page, so a change is made once",
           "It loads faster than inline styles",
           "It works without HTML",
           "It cannot be edited by mistake"], 0,
          "Editing one CSS file restyles the whole site, which is impossible with inline styles."),
        Q("Which is correctly nested HTML?",
          ["<p><strong>Hello</strong></p>", "<p><strong>Hello</p></strong>",
           "<strong><p>Hello</strong>", "<p>Hello</strong></p>"], 0,
          "Tags must close in the reverse order they were opened."),
        Q("What is the difference between a class and an id in CSS?",
          ["A class can be used on many elements, an id identifies one unique element",
           "An id can be used many times, a class only once",
           "They are identical",
           "A class only works on text"], 0,
          "Ids must be unique on a page. Classes are for styles shared by several elements."),
        Q("Why should headings be used in order, h1 then h2 then h3?",
          ["Screen readers use the heading structure to navigate the page",
           "Browsers refuse to display them otherwise",
           "It makes the page load faster",
           "It changes the colour automatically"], 0,
          "Heading levels convey the structure of the document, which is how many users move around a page."),
        Q("What does padding control in CSS?",
          ["Space inside an element, between its content and its border",
           "Space outside an element",
           "The thickness of the border",
           "The font size"], 0,
          "Padding is inside, margin is outside. Mixing them up is one of the most common CSS errors."),
        Q("Which link text is best for accessibility?",
          ["Read the safety guidance", "Click here", "Link", "More"], 0,
          "Screen reader users often browse by jumping between links, so each link must make sense on its own."),
    ],
    exam=[
        EQ("State the difference between the purpose of HTML and the purpose of CSS.", 2, [
            MP("HTML defines the structure and content of the page", ["structure", "content", "what things are", "layout of content"]),
            MP("CSS defines the appearance or style", ["appearance", "style", "look", "colours", "formatting"]),
        ], "HTML is used to define the structure and content of a web page, describing what each part of the page is, such as a heading, a paragraph, a list or an image. CSS is used to control the appearance of those elements, setting things such as colours, fonts, spacing and layout.",
           command="State"),
        EQ("Write the HTML needed to display a level one heading saying Welcome, a paragraph of text, and an image of a dog with suitable alternative text.", 4, [
            MP("Correct h1 tag with the text Welcome", ["<h1>welcome</h1>", "h1"]),
            MP("Correct paragraph tags", ["<p>", "</p>", "paragraph"]),
            MP("Correct img tag with a src attribute", ["<img", "src="]),
            MP("Suitable alt text describing the image", ["alt=", "alt text", "describing"]),
        ], "<h1>Welcome</h1>\n<p>This is a paragraph of text about the website.</p>\n<img src=\"dog.jpg\" alt=\"A golden retriever running across a field\">\n\nThe h1 tag marks the most important heading on the page. The paragraph tags open and close around the text. The img tag is self closing and needs a src attribute giving the file name, plus an alt attribute describing what the image shows so that people using a screen reader still receive the information.",
           command="Write"),
        EQ("Explain why it is better to use an external stylesheet than to write styles inline on each element.", 3, [
            MP("One stylesheet can be linked from every page of the site", ["every page", "all pages", "one file", "shared"]),
            MP("A style change only has to be made in one place", ["one place", "change once", "single edit", "update once"]),
            MP("It keeps structure and appearance separate, making the code easier to read and maintain", ["separate", "structure", "appearance", "readable", "maintain", "tidier"]),
        ], "An external stylesheet is a single CSS file that every page of the website links to, so the same styles are applied consistently across the whole site. This means that if the design needs to change, for example altering the heading colour or the body font, the edit is made once in that one file and every page updates immediately, whereas inline styles would have to be found and changed on every element on every page. It also keeps the HTML focused purely on structure and content while the CSS handles appearance, which makes both files considerably shorter, easier to read and far easier to maintain.",
           command="Explain"),
        EQ("Describe three features that make a website accessible to people with disabilities.", 6, [
            MP("Alternative text on images", ["alt text", "alt", "alternative text", "image description"]),
            MP("So that screen reader users know what the image shows", ["screen reader", "read out", "blind", "visually impaired", "know what"]),
            MP("Good colour contrast between text and background", ["contrast", "colour", "background", "readable"]),
            MP("So that text is readable for people with limited vision or colour blindness", ["limited vision", "colour blind", "read", "see", "sight"]),
            MP("Full keyboard access without needing a mouse", ["keyboard", "without a mouse", "tab", "navigate"]),
            MP("Headings used in the correct order so screen readers can navigate the structure", ["headings", "h1 h2", "order", "structure", "navigate"]),
        ], "The first feature is alternative text on every meaningful image. A screen reader cannot interpret a picture, so it reads out the alt text instead, which means a blind user receives the same information as everyone else. Without it, the image is announced simply as an image and the content is lost. The second feature is strong colour contrast between text and its background. People with limited vision, and anyone reading a screen in bright sunlight, cannot read light grey text on a white background, so choosing colours with sufficient contrast makes the site readable for far more people. The third feature is full keyboard access. Many people cannot use a mouse, whether because of a motor impairment or because they rely on assistive technology, so every link, button and form field must be reachable and usable with the keyboard alone. Alongside these, using headings in the correct order matters greatly, because screen reader users navigate a page by jumping between headings, and skipping levels or using headings purely for their size makes that structure meaningless.",
           command="Describe"),
        EQ("Explain the difference between a class and an id in CSS, and state when each should be used.", 3, [
            MP("A class can be applied to many elements", ["many", "several", "multiple", "reused", "more than one"]),
            MP("An id must be unique to one element on the page", ["unique", "one element", "only once", "single"]),
            MP("Use a class for a shared style and an id for a single unique element", ["shared", "same style", "unique element", "one particular"]),
        ], "A class is used when several elements on a page should share the same appearance, and the same class can be applied to as many elements as needed, so a class called warning could style every warning box on the site. An id is used to identify one specific element, and each id must be unique within a page, so an id called mainHeader would apply to the single header at the top. In CSS a class is selected with a full stop before its name and an id with a hash. In practice classes are used far more often, because most styling applies to groups of similar elements, and ids are reserved for unique landmarks or for linking to a particular point in the page.",
           command="Explain"),
    ],
)

# ============================================================ YEAR 9

Y9_DIGLIT = Topic(
    slug="digital-literacy-and-the-law",
    title="Digital Literacy and the Law",
    spec="Y9.1",
    icon="i-scales",
    minutes=26,
    blurb="The four laws that govern computing, how your data is collected and used, and the ethical questions technology forces on all of us.",
    fact="Under the Data Protection Act you can send any organisation a subject access request asking for every piece of personal data they hold about you. They must respond within one month, and it is free.",
    sections=[
        Section("The four laws", """
### Data Protection Act 2018

Controls how organisations collect, store and use **personal data**. It brings GDPR into UK law.

Organisations must ensure data is:

- Used **fairly and lawfully**
- Collected for a **specified purpose** and not used for something else
- **Adequate and not excessive**, so only what is actually needed
- **Accurate and kept up to date**
- **Not kept longer than necessary**
- Kept **secure**

You have the right to see the data held about you, to have mistakes corrected, and in many cases to have it deleted.

### Computer Misuse Act 1990

Three offences:

1. **Unauthorised access** to computer material, such as logging into someone else's account
2. **Unauthorised access with intent to commit a further offence**, such as breaking in to commit fraud
3. **Unauthorised modification**, such as deleting files or spreading a virus

!warn Guessing a friend's password is a criminal offence :: Even if you change nothing and it was meant as a joke. The offence is the access itself.

### Copyright, Designs and Patents Act 1988

Protects the work of creators: music, films, games, software, images, writing and designs. Copying, sharing or using someone's work without permission is illegal.

This covers downloading films illegally, using a photograph from a search engine in a project you publish, and copying software.

**Creative Commons** licences are the exception. The creator gives permission in advance, usually on the condition that you credit them.

### Freedom of Information Act 2000

Gives the public the right to request information held by **public bodies** such as councils, schools and the NHS. It is about transparency in public organisations, not about personal data.
"""),
        Section("How your data is used", """
### What is collected

- What you search for and which pages you visit
- How long you spend looking at each thing
- Your location, often continuously
- Who you interact with
- What you buy, and what you almost bought

### Why it is collected

Mostly **targeted advertising**. A service that knows your interests can sell far more valuable advertising space than one that does not, which is why so many services are free.

It is also used to recommend content, to improve products, and sometimes it is sold to other companies.

### Cookies

A **cookie** is a small file stored on your device by a website.

- **Necessary cookies** make the site work, for example remembering what is in your basket
- **Tracking cookies** follow you across different websites to build a profile of your interests

This is why cookie banners exist, and why you can usually reject everything except the necessary ones.

### The trade

You are not paying money for most online services. You are paying with your data and your attention. That is not automatically wrong, but it should be a decision you make knowingly rather than one made for you.
"""),
        Section("Ethics and the impact of technology", """
### Ethical questions have no legal answer

- Should employers read employees' messages?
- Should facial recognition be used in public spaces?
- Should an algorithm decide who gets a job interview, a loan or a place at university?
- Is it acceptable to automate a job that thousands of people depend on?
- Who is responsible when a self driving car causes a crash?

None of these has a single right answer, which is exactly why they matter and why you should be able to argue both sides.

### The digital divide

Not everyone has reliable internet, a suitable device or the skills to use them. As more services move online, those people are excluded from things they need, including applying for support, booking appointments and doing schoolwork.

This affects some groups far more than others: low income households, elderly people, rural communities, and people with disabilities.

### Environmental impact

- Manufacturing devices uses rare earth metals, and mining them damages habitats and pollutes water
- Data centres consume enormous amounts of electricity
- **E-waste** contains toxic materials such as lead and mercury, and much of it is shipped to countries with weaker environmental protections
- Replacing devices every two years makes all of this worse

Positives exist too: video calls replace flights, digital documents replace paper, and smart systems reduce energy use in buildings.

!key How to write a good answer on impact :: Give both sides, name the specific group affected, and finish with a judgement. "Online council services save money and are available at any hour, however elderly residents without internet access are excluded, so a telephone option should be kept."
"""),
    ],
    keyterms=[
        ("Data Protection Act 2018", "The law controlling how organisations collect, store and use personal data."),
        ("Computer Misuse Act 1990", "The law making unauthorised access to and modification of computer material a criminal offence."),
        ("Copyright, Designs and Patents Act 1988", "The law protecting the work of creators from being copied or used without permission."),
        ("Personal data", "Information that can be used to identify a living person."),
        ("Cookie", "A small file stored on your device by a website, used to remember settings or to track you."),
        ("Creative Commons", "A licence where the creator gives permission in advance for their work to be used, usually with conditions."),
        ("Digital divide", "The gap between those with reliable access to technology and those without."),
        ("E-waste", "Discarded electronic equipment, often containing toxic materials."),
    ],
    grade="""
The top level here is about **arguing, not listing**.

**Name the law correctly, with its year.** Getting the Computer Misuse Act mixed up with the Copyright Act loses marks that are otherwise free.

**Give both sides of every ethical question.** An answer that only says technology is bad, or only says it is good, cannot reach the top level however many points it makes.

**Name the specific group affected.** Not "some people", but "elderly residents in rural areas without reliable broadband".

**Finish with a judgement.** Say what you think should happen and why, based on what you have just argued.

+ Match any scenario to the correct law instantly
+ Explain three principles of the Data Protection Act
+ Write a balanced answer on an ethical question with a clear conclusion
+ Explain the digital divide and name the groups it affects most
""",
    mistakes=[
        "Confusing the Computer Misuse Act with the Copyright Act. Hacking is Misuse, piracy is Copyright.",
        "Saying it is only illegal to access someone's account if you change something. Access alone is the offence.",
        "Writing a one sided answer to an impact question.",
        "Saying 'it affects people' instead of naming the specific group.",
        "Forgetting that technology has positive environmental impacts as well as negative ones.",
    ],
    quiz=[
        Q("Which law makes it illegal to log into someone else's account without permission?",
          ["Computer Misuse Act 1990", "Data Protection Act 2018",
           "Copyright, Designs and Patents Act 1988", "Freedom of Information Act 2000"], 0,
          "Unauthorised access is an offence in itself, even if nothing is changed or taken."),
        Q("Which law protects a musician's song from being copied and shared without permission?",
          ["Copyright, Designs and Patents Act 1988", "Computer Misuse Act 1990",
           "Data Protection Act 2018", "Freedom of Information Act 2000"], 0,
          "Copyright protects creative work, including music, films, games, software and images."),
        Q("Under the Data Protection Act, organisations must:",
          ["Only collect data that is adequate and not excessive for a stated purpose",
           "Keep all data forever in case it is useful",
           "Share data freely with other companies",
           "Collect as much data as possible"], 0,
          "Collecting more than you need for the stated purpose is itself a breach of the principles."),
        Q("What is a tracking cookie used for?",
          ["Following you across different websites to build a profile of your interests",
           "Making the website load faster",
           "Encrypting your password",
           "Storing your files"], 0,
          "This is what cookie banners are asking permission for, and why you can usually reject them."),
        Q("What is the digital divide?",
          ["The gap between those with reliable access to technology and those without",
           "The difference between hardware and software",
           "The split between free and paid apps",
           "The gap between wired and wireless networks"], 0,
          "It matters because services increasingly assume everyone has a device and a connection."),
        Q("Which is an environmental impact of computing?",
          ["E-waste containing toxic materials being shipped to developing countries",
           "Employers reading employee emails",
           "Software being copied illegally",
           "Cookies tracking your browsing"], 0,
          "The others are ethical, legal and privacy issues respectively."),
        Q("What does a Creative Commons licence allow?",
          ["Use of the work under conditions the creator has set in advance",
           "Unlimited use with no conditions at all",
           "Only use by schools",
           "Nothing, it prevents all use"], 0,
          "The creator gives permission ahead of time, usually requiring that you credit them."),
        Q("What right does the Data Protection Act give you?",
          ["To see the personal data an organisation holds about you",
           "To access any computer system you like",
           "To copy any software you have bought",
           "To free internet access"], 0,
          "This is called a subject access request, and organisations must respond within one month."),
        Q("Why are many online services free to use?",
          ["Your data and attention are sold to advertisers",
           "Governments pay for them",
           "They are run as charities",
           "They make money from selling hardware"], 0,
          "Targeted advertising based on collected data is the business model behind most free services."),
        Q("Which is the strongest structure for an answer about the impact of a new technology?",
          ["Both sides, a named affected group, and a conclusion",
           "A list of as many disadvantages as possible",
           "Only the advantages, since progress is good",
           "A definition of the technology and nothing else"], 0,
          "Balance, specificity and a judgement are what mark schemes reward at the top level."),
    ],
    exam=[
        EQ("Name the law that would be broken by a student who guesses another student's password and reads their files.", 1, [
            MP("Computer Misuse Act 1990", ["computer misuse", "misuse act", "1990"]),
        ], "The Computer Misuse Act 1990, which makes unauthorised access to computer material a criminal offence even when nothing is changed or taken.",
           command="Name"),
        EQ("State three principles that organisations must follow under the Data Protection Act 2018.", 3, [
            MP("Data must be used fairly and lawfully", ["fairly", "lawfully", "legally", "fair"]),
            MP("Data must be adequate and not excessive, collected for a specified purpose", ["adequate", "not excessive", "only what is needed", "specified purpose", "relevant"]),
            MP("Data must be kept secure, accurate, and not kept longer than necessary", ["secure", "accurate", "up to date", "not kept longer", "necessary", "deleted"]),
        ], "Organisations must use personal data fairly and lawfully, and only for the specific purpose they stated when they collected it. They must collect only data that is adequate and relevant for that purpose and not excessive, so they cannot gather extra information just in case it might be useful. They must also keep the data accurate and up to date, store it securely so it cannot be stolen or lost, and delete it once it is no longer needed for the purpose it was collected for.",
           command="State"),
        EQ("Explain what is meant by the digital divide and describe one group it affects.", 3, [
            MP("The gap between those with reliable access to technology and those without", ["gap", "access", "without", "some people have", "divide"]),
            MP("Names a specific affected group", ["elderly", "older", "low income", "poorer", "rural", "disabled", "homeless"]),
            MP("Explains a consequence for that group", ["excluded", "cannot apply", "cannot access services", "disadvantaged", "left behind", "schoolwork"]),
        ], "The digital divide is the gap between people who have reliable access to technology and the internet, along with the skills and confidence to use them, and people who do not. It matters because more and more essential services assume that everyone is online. One group strongly affected is students in low income households, who may share a single device between several family members or have no home broadband at all. When homework is set online and lessons rely on digital resources, those students fall behind not because of ability but because of access, and the gap widens over time.",
           command="Explain"),
        EQ("A council is planning to move all its services online so that residents must use a website. Discuss the advantages and disadvantages of this decision.", 8, [
            MP("Advantage: cheaper to run than staffed offices", ["cheaper", "cost", "saves money", "less expensive"]),
            MP("Advantage: available at any time rather than only office hours", ["any time", "24 hours", "convenient", "evenings", "weekends"]),
            MP("Advantage: faster processing and easier tracking of requests", ["faster", "quicker", "track", "efficient", "automatic"]),
            MP("Disadvantage: excludes residents without internet access or devices", ["excluded", "no internet", "no device", "cannot access", "digital divide"]),
            MP("Names a specific affected group such as elderly or low income residents", ["elderly", "older", "low income", "poorer", "rural", "disabled"]),
            MP("Raises data protection responsibilities for personal data collected", ["data protection", "personal data", "secure", "gdpr", "privacy"]),
            MP("Gives both sides rather than only one", ["however", "on the other hand", "although", "but", "against this"]),
            MP("Reaches a clear conclusion with a recommendation", ["conclusion", "overall", "therefore", "should", "recommend"]),
        ], "Moving council services online brings real advantages. Running a website costs far less than staffing offices across the borough, and those savings can be spent on other services. The site is available at any hour, so a resident working shifts can report a problem at eleven at night rather than taking time off work, and requests submitted online can be logged, tracked and processed automatically, which is quicker and less error prone than paper forms. However, the decision has serious disadvantages. Not every resident has a reliable internet connection, a suitable device, or the confidence to use one, and the people most likely to be excluded are elderly residents, people on low incomes and those in rural areas with poor broadband. These are frequently the same residents who most need council support, so a digital only service risks becoming hardest to reach for the people who depend on it most. There is also a legal dimension: the council will be collecting large amounts of personal data including addresses, financial details and information about vulnerable people, so under the Data Protection Act 2018 it must keep that data secure, use it only for the stated purpose and not retain it longer than necessary, and a breach would be both damaging and expensive. Overall the council is right to develop online services, because the cost savings and the convenience for the majority are substantial, but it would be wrong to make them the only option. The best approach is to build the website properly while keeping a telephone line and a staffed counter available, and to fund support that helps residents get online, so that nobody loses access to services they are entitled to.",
           command="Discuss"),
        EQ("Explain why using an image from a search engine in a website you publish may be illegal.", 3, [
            MP("Images are protected by copyright", ["copyright", "protected", "intellectual property"]),
            MP("The creator owns the work and permission is needed to use it", ["creator", "owner", "permission", "licence", "consent"]),
            MP("Names the Copyright, Designs and Patents Act 1988 or suggests using Creative Commons images instead", ["copyright designs and patents", "1988", "creative commons", "royalty free", "own photo"]),
        ], "Images found through a search engine are almost always protected by copyright, which belongs to whoever created them. The Copyright, Designs and Patents Act 1988 makes it illegal to copy, publish or distribute someone else's work without their permission, and publishing an image on a public website counts as exactly that. Using the image without a licence could result in the site being taken down or a demand for payment. The safe alternatives are to take or create the image yourself, to use images released under a Creative Commons licence while following whatever conditions the creator set, usually crediting them, or to use a stock library that explicitly permits the use.",
           command="Explain"),
    ],
)

Y9_DATAREP = Topic(
    slug="data-representation",
    title="Data Representation",
    spec="Y9.2",
    icon="i-binary",
    minutes=32,
    blurb="Binary, hexadecimal, binary addition, and exactly how text, images and sound become numbers. This is the foundation of the whole GCSE course.",
    fact="Hexadecimal exists only for people. The computer never uses it. The colour white in 24 bit binary is twenty four ones in a row, and in hexadecimal it is just FFFFFF, which is why every web developer is grateful for base 16.",
    sections=[
        Section("Binary and hexadecimal", """
### Binary to denary

Write the place values above the digits and add where there is a 1.

| 128 | 64 | 32 | 16 | 8 | 4 | 2 | 1 |
| 1 | 1 | 0 | 1 | 0 | 0 | 1 | 0 |

128 + 64 + 16 + 2 = **210**

### Denary to binary

Work from the left, asking whether each place value fits. Convert 156:

- 128 fits, leaving 28. Write 1.
- 64 does not fit. Write 0.
- 32 does not fit. Write 0.
- 16 fits, leaving 12. Write 1.
- 8 fits, leaving 4. Write 1.
- 4 fits, leaving 0. Write 1.
- 2 no, 1 no. Write 0, 0.

Result `10011100`. Check: 128 + 16 + 8 + 4 = 156.

### Hexadecimal

Base 16, using 0 to 9 then A to F.

| Denary | 10 | 11 | 12 | 13 | 14 | 15 |
| Hex | A | B | C | D | E | F |

**Why it is used**: one hex digit replaces four binary digits, so values are a quarter of the length and far easier for a person to read, write and remember without mistakes. You see it in colour codes, MAC addresses and error codes.

### Converting

**Binary to hex**: split into nibbles of four bits from the right, convert each.

`11010110` becomes `1101` and `0110`, which is 13 and 6, so **D6**.

**Hex to binary**: expand each digit to four bits.

`2F` becomes `0010` and `1111`, so `00101111`.

**Hex to denary**: multiply the first digit by 16 and add the second.

`3A` = (3 x 16) + 10 = **58**
"""),
        Section("Binary addition and units", """
### The four rules

    0 + 0 = 0
    0 + 1 = 1
    1 + 1 = 0 carry 1
    1 + 1 + 1 = 1 carry 1

Work from right to left, exactly like column addition.

      01101010   (106)
    + 00110101   (53)
    ----------
      10011111   (159)

### Overflow

An **overflow error** happens when the answer needs more bits than are available. With 8 bits the largest value is 255, so any total above that overflows, the carry out of the leftmost column is lost, and the stored answer is wrong.

### Units

| Unit | Size |
| Bit | One 1 or 0 |
| Nibble | 4 bits |
| Byte | 8 bits |
| Kilobyte | 1000 bytes |
| Megabyte | 1000 KB |
| Gigabyte | 1000 MB |
| Terabyte | 1000 GB |
"""),
        Section("Representing text, images and sound", """
### Text

Every character is given a number, and that number is stored in binary. The agreed list is the **character set**.

- **ASCII** uses 7 bits, giving 128 characters. Enough for English.
- **Unicode** uses 16 bits or more, giving over a million characters, covering every major writing system and emoji.

Unicode's advantage is language coverage. Its cost is file size, because each character takes more bits.

Characters are in order, so if A is 65 then D is 68. The character '5' is not the number 5: its ASCII code is 53.

### Images

An image is a grid of **pixels**, each storing a colour as a binary number.

- **Resolution** is the number of pixels, written width by height
- **Colour depth** is the number of **bits per pixel**, and n bits gives 2^n^ colours
- **Metadata** is data about the image such as its dimensions, needed so the computer knows how to arrange the pixels

    file size in bits = colour depth x width x height

A 500 by 400 image at 8 bit colour depth:

    8 x 500 x 400 = 1,600,000 bits = 200,000 bytes = 200 KB

### Sound

Sound is a continuous wave, so it must be **sampled**: measured at regular intervals with each measurement stored as a binary number.

- **Sample rate** is how many measurements per second, in hertz
- **Bit depth** is how many bits store each measurement

    file size in bits = sample rate x duration in seconds x bit depth

A 60 second clip at 44,100 Hz with 16 bit depth:

    44100 x 60 x 16 = 42,336,000 bits = 5,292,000 bytes = about 5.3 MB

!key The pattern across all three :: Better quality always means more numbers, and more numbers always means a bigger file. There is no way around that trade off.
"""),
    ],
    keyterms=[
        ("Binary", "Base 2, using only the digits 0 and 1."),
        ("Denary", "Base 10, the everyday number system. Also called decimal."),
        ("Hexadecimal", "Base 16, using 0 to 9 and A to F, where one digit represents four bits."),
        ("Overflow", "An error where a result needs more bits than are available, so the stored answer is wrong."),
        ("Character set", "The agreed list of characters and the binary code used for each."),
        ("ASCII", "A 7 bit character set representing 128 characters."),
        ("Unicode", "A character set using 16 or more bits, representing over a million characters."),
        ("Resolution", "The number of pixels in an image, given as width by height."),
        ("Colour depth", "The number of bits used to store the colour of each pixel."),
        ("Sampling", "Measuring a sound wave at regular intervals and storing each measurement in binary."),
        ("Sample rate", "The number of sound samples taken each second, measured in hertz."),
    ],
    grade="""
This topic is where careful students collect free marks and careless ones give them away.

**Write the place values down every time.** 128 64 32 16 8 4 2 1. Every single time, even when you are sure.

**Check by converting back.** It takes ten seconds and catches almost every error.

**Show every line of working in calculations, with units.** Method marks are real marks, and an answer left in bits when the question asked for kilobytes loses the final mark even when everything else was perfect.

**Explain rather than assert.** Higher sample rate improves quality *because* measurements are taken closer together, so the stored data follows the original wave more closely.

+ Convert 8 bit binary to denary and back in under 30 seconds
+ Convert between binary, hex and denary in both directions
+ Add two 8 bit numbers and identify overflow
+ Calculate an image or sound file size in the unit requested
""",
    mistakes=[
        "Writing the place values in the wrong direction. The 1 is on the right.",
        "Splitting binary into nibbles from the left instead of the right.",
        "Treating hexadecimal A as 1 rather than 10.",
        "Saying a colour depth of 4 means four colours. It means four bits, so sixteen colours.",
        "Forgetting to divide by 8 when the answer must be in bytes.",
        "Forgetting to convert minutes into seconds before a sound calculation.",
    ],
    quiz=[
        Q("What is 11001010 in denary?", ["202", "198", "206", "210"], 0,
          "128 + 64 + 8 + 2 = 202."),
        Q("What is 45 in 8 bit binary?", ["00101101", "00101110", "00110101", "01001101"], 0,
          "32 + 8 + 4 + 1 = 45, so the bits at those place values are set."),
        Q("What is 10110110 in hexadecimal?", ["B6", "6B", "A6", "B8"], 0,
          "Split into 1011 and 0110, which are 11 and 6, so B6."),
        Q("Why is hexadecimal used by programmers?",
          ["It is much shorter than binary and easier for people to read without errors",
           "Computers process it faster", "It uses less storage", "It is the only base that stores colours"], 0,
          "One hex digit replaces four bits, so values are a quarter the length. The computer still stores binary."),
        Q("What is the denary value of hexadecimal 5C?", ["92", "512", "88", "76"], 0,
          "C is 12, so (5 x 16) + 12 = 80 + 12 = 92."),
        Q("An overflow error happens when:",
          ["The result of a calculation needs more bits than are available",
           "Two numbers are divided", "A file is too large for the disk", "Binary is converted to hex"], 0,
          "The carry out of the leftmost column has nowhere to go, so it is lost and the answer is wrong."),
        Q("An image is 400 by 300 with a colour depth of 8 bits. What is the file size in bits?",
          ["960,000", "120,000", "9,600,000", "1,200"], 0,
          "8 x 400 x 300 = 960,000 bits, which is 120,000 bytes or 120 KB."),
        Q("What does a colour depth of 6 bits allow?",
          ["64 different colours", "6 different colours", "36 colours", "12 colours"], 0,
          "Two to the power 6 is 64. Each extra bit doubles the number of available colours."),
        Q("What is sample rate?",
          ["How many measurements of the sound wave are taken each second",
           "How many bits store each measurement",
           "How loud the recording is",
           "How long the recording lasts"], 0,
          "Sample rate is along the time axis. Bit depth is how precisely each measurement is stored."),
        Q("What is the main disadvantage of Unicode compared with ASCII?",
          ["It uses more bits per character, so files are larger",
           "It cannot store English", "It is no longer supported", "It cannot store numbers"], 0,
          "At 16 or more bits per character rather than 7, the same text takes roughly twice the storage."),
    ],
    exam=[
        EQ("Convert the denary number 187 into 8 bit binary. Show your working.", 3, [
            MP("Uses place values from 128 downwards", ["128", "64", "place value", "32"]),
            MP("Shows the subtraction working", ["187 - 128", "59", "subtract", "leaves"]),
            MP("Correct answer 10111011", ["10111011"]),
        ], "Working from the largest place value: 128 fits into 187 leaving 59, so write 1. 64 does not fit into 59, write 0. 32 fits leaving 27, write 1. 16 fits leaving 11, write 1. 8 fits leaving 3, write 0 for 8 being used, so write 1. 4 does not fit into 3, write 0. 2 fits leaving 1, write 1. 1 fits leaving 0, write 1. This gives 10111011, and checking: 128 + 32 + 16 + 8 + 2 + 1 = 187.",
           command="Convert"),
        EQ("Explain why hexadecimal is often used instead of binary.", 3, [
            MP("One hexadecimal digit represents four binary digits", ["four bits", "one digit", "nibble", "quarter"]),
            MP("Values are much shorter to write and read", ["shorter", "fewer characters", "compact", "less to write"]),
            MP("Shorter values are easier for people to remember and less prone to error", ["easier", "remember", "fewer mistakes", "less error", "spot"]),
        ], "Hexadecimal is used because each hexadecimal digit represents exactly four binary digits, so an eight bit value that needs eight characters in binary needs only two in hexadecimal. Values written in hexadecimal are therefore around a quarter of the length, which makes them far quicker for a person to write down and read back. Because the values are short, people make fewer transcription mistakes and any error that is made is much easier to spot, which is why colour codes, MAC addresses and memory addresses are all normally written in hexadecimal. The computer itself still works entirely in binary.",
           command="Explain"),
        EQ("Add the binary numbers 01011010 and 00110110, showing your working, and state the denary value of the answer.", 4, [
            MP("Adds column by column from the right with carries", ["carry", "right to left", "column"]),
            MP("Correct binary answer 10010000", ["10010000"]),
            MP("Converts the answer to denary", ["144", "denary", "128 + 16"]),
            MP("States that no overflow occurs as the answer fits in 8 bits", ["no overflow", "fits", "8 bits", "within range"]),
        ], "Adding column by column from the right and carrying wherever two or three ones meet gives 10010000. Checking in denary, 01011010 is 90 and 00110110 is 54, and 90 plus 54 is 144, which is 10010000 in binary since 128 + 16 = 144. No overflow error occurs, because 144 is within the range 0 to 255 that eight bits can represent, so nothing is carried out of the most significant column and no data is lost.",
           command="Add"),
        EQ("A photograph is 1200 pixels wide and 800 pixels high with a colour depth of 24 bits. Calculate the file size in megabytes.", 4, [
            MP("Multiplies colour depth by width by height", ["24 x 1200", "1200 x 800", "colour depth x width x height"]),
            MP("Obtains 23,040,000 bits", ["23040000", "23,040,000"]),
            MP("Divides by 8 to obtain 2,880,000 bytes", ["2880000", "2,880,000", "divide by 8"]),
            MP("States 2.88 MB", ["2.88", "2880 kb", "2.88 mb"]),
        ], "File size in bits is colour depth multiplied by width multiplied by height, so 24 x 1200 x 800 = 23,040,000 bits. Dividing by 8 gives 2,880,000 bytes. Dividing by 1000 gives 2880 kilobytes, and dividing by 1000 again gives a file size of 2.88 megabytes.",
           command="Calculate"),
        EQ("Explain how sound is stored digitally, and describe the effect of increasing the sample rate.", 4, [
            MP("The amplitude of the sound wave is measured at regular intervals", ["amplitude", "measured", "regular intervals", "height"]),
            MP("Each measurement is stored as a binary number", ["binary", "number", "stored", "digital"]),
            MP("A higher sample rate means measurements are taken closer together in time", ["closer together", "more often", "more samples", "more measurements"]),
            MP("So the recording is a more accurate copy of the original wave, but the file is larger", ["more accurate", "closer to the original", "better quality", "larger file", "bigger"]),
        ], "Sound in the real world is a continuously varying wave, which cannot be stored directly because a computer can only store numbers. Instead the amplitude of the wave is measured at regular fixed intervals, a process called sampling, and each measurement is rounded to the nearest available level and stored as a binary number. Increasing the sample rate means those measurements are taken more often and therefore closer together in time, so less of the wave's shape is missed between samples and the stored data follows the original much more closely, producing a more accurate and better sounding recording. The cost is file size, which is directly proportional to sample rate, so doubling the sample rate doubles the amount of storage the recording needs.",
           command="Explain"),
    ],
)

Y9_PYTHON = Topic(
    slug="python-programming",
    title="Python Programming",
    spec="Y9.3",
    icon="i-python",
    minutes=32,
    blurb="Subroutines, 2D lists, file handling, dictionaries and structured programs. Everything you need so that GCSE programming feels like continuing rather than starting.",
    fact="Reading someone else's code is a genuine skill and it is harder than writing your own. Professional programmers spend far more time reading than writing, which is exactly why clear names and comments matter so much.",
    sections=[
        Section("Structuring a program", """
### Subroutines

A **subroutine** is a named block of code you can call whenever you need it.

```python
def get_valid_mark(prompt):
    # Keep asking until the user enters a mark between 0 and 100
    while True:
        entry = input(prompt)
        if entry.isdigit() and 0 <= int(entry) <= 100:
            return int(entry)
        print("Please enter a whole number between 0 and 100.")

def grade_for(mark):
    if mark >= 70:
        return "Distinction"
    elif mark >= 50:
        return "Pass"
    else:
        return "Fail"

mark = get_valid_mark("Enter the mark: ")
print("Grade:", grade_for(mark))
```

Notice how the main program at the bottom reads almost like English. That is what good structure buys you.

- A **function** returns a value using `return`
- A **procedure** just does something and returns nothing

### Local and global variables

A **local** variable exists only inside the subroutine that created it. A **global** variable exists everywhere.

Local is almost always better, because nothing else in the program can change it by accident.

```python
def add_tax(amount):
    tax = amount * 0.2      # local, disappears when the function ends
    return amount + tax
```
"""),
        Section("Lists, 2D lists and dictionaries", """
### Working with lists

```python
scores = [45, 78, 12, 90, 33]

print(sum(scores), max(scores), min(scores), len(scores))
print(sorted(scores))          # a sorted copy
scores.sort()                  # sorts in place
scores.append(60)
scores.insert(0, 5)            # insert at the start
scores.remove(12)              # remove the value 12
print(scores.index(90))        # position of 90
print(90 in scores)            # True or False
```

### 2D lists

A **2D list** is a list of lists, forming a grid.

```python
board = [["X", "O", "X"],
         ["O", "X", "O"],
         ["X", "O", "X"]]

print(board[1][2])       # row 1, column 2, which is "O"

for row in board:
    for cell in row:
        print(cell, end=" ")
    print()
```

!key Row first, then column :: `board[1][2]` means row 1, column 2. Getting these round the wrong way is one of the most common errors, and on a non square grid it causes a crash.

### Dictionaries

A **dictionary** stores pairs of keys and values, which is far more readable than remembering that index 3 was the score.

```python
student = {"name": "Aisha", "year": 9, "score": 82}

print(student["name"])          # Aisha
student["score"] = 90           # change a value
student["house"] = "Blue"       # add a new pair

for key in student:
    print(key, "=", student[key])
```
"""),
        Section("Files and building a real program", """
### Reading and writing files

```python
# Write, which erases anything already in the file
with open("scores.txt", "w") as file:
    file.write("Aisha,82\n")
    file.write("Ben,64\n")

# Append, which adds without deleting
with open("scores.txt", "a") as file:
    file.write("Chloe,91\n")

# Read
with open("scores.txt", "r") as file:
    for line in file:
        name, score = line.strip().split(",")
        print(name, "scored", score)
```

Using `with open(...)` closes the file automatically, even if something goes wrong.

!warn Write mode erases the file :: If you need to add a record without losing what is there, use `"a"` for append.

### Putting it together

```python
def load_scores(filename):
    scores = {}
    try:
        with open(filename, "r") as file:
            for line in file:
                name, value = line.strip().split(",")
                scores[name] = int(value)
    except FileNotFoundError:
        print("No score file yet, starting fresh.")
    return scores

def save_scores(filename, scores):
    with open(filename, "w") as file:
        for name in scores:
            file.write(name + "," + str(scores[name]) + "\n")

def show_top(scores):
    if len(scores) == 0:
        print("No scores recorded.")
        return
    best = max(scores, key=scores.get)
    print("Top score:", best, "with", scores[best])

scores = load_scores("scores.txt")
scores["Dev"] = 77
show_top(scores)
save_scores("scores.txt", scores)
```

This program has four clear jobs, each in its own subroutine, and it handles the case where the file does not exist yet. That is the difference between code that works on your machine and code that works.
"""),
    ],
    keyterms=[
        ("Subroutine", "A named block of code that performs a task and can be called from anywhere in a program."),
        ("Function", "A subroutine that returns a value."),
        ("Procedure", "A subroutine that performs a task without returning a value."),
        ("Parameter", "A value passed into a subroutine so it can do its work."),
        ("Local variable", "A variable that exists only inside the subroutine where it was created."),
        ("Global variable", "A variable available throughout the whole program."),
        ("2D list", "A list of lists, forming a grid accessed by row and column."),
        ("Dictionary", "A data structure storing pairs of keys and values."),
        ("Append mode", "Opening a file so new data is added to the end without erasing existing content."),
    ],
    grade="""
The top level in Year 9 Python is about **writing programs that survive contact with a real user**.

**Break the program into subroutines before you start typing.** If you can name four jobs the program has to do, you have four subroutines and the code almost writes itself.

**Handle the awkward cases.** What if the file does not exist? What if the list is empty? What if the user types letters? A program that only works when everything goes right is not finished.

**Comment why, not what.** `count = count + 1  # add one to count` is useless. `# skip the header row` is worth having.

+ Write a program using at least three subroutines with parameters and return values
+ Read from and write to a file, choosing the correct mode
+ Use a 2D list to represent a grid and loop through it correctly
+ Validate every piece of input before the program uses it
""",
    mistakes=[
        "Opening a file in write mode when the existing data needs keeping.",
        "Getting row and column the wrong way round in a 2D list.",
        "Forgetting to use return, so the function calculates an answer and throws it away.",
        "Assuming a file exists, so the program crashes the first time it is run.",
        "Writing one long program with no subroutines, which becomes impossible to debug.",
    ],
    quiz=[
        Q("What is the difference between a function and a procedure?",
          ["A function returns a value, a procedure does not",
           "A procedure returns a value, a function does not",
           "Functions can only be called once", "There is no difference"], 0,
          "The return value is the defining difference, and it comes up in exams every year."),
        Q("In `grid = [[1,2,3],[4,5,6]]`, what does `grid[1][0]` give?",
          ["4", "2", "1", "6"], 0,
          "Row 1 is the second row, [4,5,6], and column 0 is its first item, which is 4."),
        Q("Which file mode adds to a file without erasing what is already there?",
          ["\"a\"", "\"w\"", "\"r\"", "\"x\""], 0,
          "Append mode preserves existing content. Write mode erases the file first."),
        Q("What does a dictionary store?",
          ["Pairs of keys and values", "Only numbers", "Only text", "A grid of values"], 0,
          "Dictionaries let you look a value up by a meaningful name rather than by a numeric index."),
        Q("Why are local variables usually preferred to global ones?",
          ["Other parts of the program cannot change them by accident",
           "They are faster to access", "They can store more data", "They are saved automatically"], 0,
          "Limited scope removes a very common and hard to trace source of bugs."),
        Q("What does `scores.append(50)` do?",
          ["Adds 50 to the end of the list", "Replaces the list with 50",
           "Removes 50", "Sorts the list"], 0,
          "append always adds to the end, making the list one item longer."),
        Q("What does `student[\"name\"]` do if student is a dictionary?",
          ["Returns the value stored under the key name",
           "Returns the first item in the dictionary",
           "Adds a new key called name",
           "Deletes the key name"], 0,
          "Square brackets with a key look up the value associated with that key."),
        Q("Why should a program be split into subroutines?",
          ["Each part can be tested separately and code is not repeated",
           "It makes the program run at a higher clock speed",
           "It removes the need for validation",
           "Python requires it"], 0,
          "Testable, reusable pieces are far easier to debug than one long block of code."),
        Q("What does `line.strip().split(\",\")` do?",
          ["Removes the newline then splits the line into parts at each comma",
           "Deletes every comma", "Joins the line to another", "Converts the line to a number"], 0,
          "strip removes whitespace including the newline, and split breaks the text into a list of fields."),
        Q("What happens if a program opens a file that does not exist in read mode?",
          ["It raises an error unless the program handles it",
           "It creates an empty file", "It returns an empty string", "Nothing happens"], 0,
          "A robust program uses try and except, or checks first, so it does not crash on the first run."),
    ],
    exam=[
        EQ("State two reasons why a programmer would use subroutines.", 2, [
            MP("Code can be reused rather than written out several times", ["reuse", "once", "not repeated", "many times", "call"]),
            MP("Each subroutine can be tested separately, making errors easier to find", ["test", "separately", "debug", "find errors", "easier"]),
        ], "Subroutines let the same code be written once and then called wherever it is needed, so it does not have to be repeated and any change only has to be made in one place. They also make a program much easier to develop and test, because each subroutine does one clearly defined job and can be tested on its own until it is known to work.",
           command="State"),
        EQ("Write a Python function that takes a list of numbers as a parameter and returns the average.", 4, [
            MP("Defines a function with a parameter", ["def", "parameter", "(numbers)", "(values)"]),
            MP("Calculates the total of the list", ["sum", "total", "add"]),
            MP("Divides by the number of items", ["len", "divide", "/ len", "count"]),
            MP("Uses return to send the answer back", ["return"]),
        ], "def average(numbers):\n    total = sum(numbers)\n    return total / len(numbers)\n\nThe function takes the list as a parameter called numbers. The built in sum function adds every value in the list, and dividing that total by len(numbers), which gives how many items there are, produces the mean. The return statement sends the answer back to the code that called the function, so it can be printed or stored.",
           command="Write"),
        EQ("Explain the difference between opening a file in write mode and in append mode, and state when each should be used.", 3, [
            MP("Write mode erases the existing contents of the file", ["erase", "delete", "overwrite", "removes", "clears"]),
            MP("Append mode adds to the end without deleting existing data", ["end", "adds", "keeps", "preserves", "existing"]),
            MP("Use write to start a new file and append to add a record to existing data", ["new file", "start again", "add a record", "keep previous", "high scores"]),
        ], "Opening a file in write mode erases everything already in it before anything new is written, so all previous content is lost. Opening in append mode leaves the existing content untouched and adds anything written to the end of the file. Write mode should be used when the file is being created from scratch or when the whole contents are being replaced, for example saving a complete set of records back to disk. Append mode should be used when a single new record is being added to data that must be kept, such as adding one new high score to an existing list.",
           command="Explain"),
        EQ("A program uses `board = [[\"X\",\"O\"],[\"O\",\"X\"],[\"X\",\"X\"]]`. State what `board[2][0]` contains and explain how a 2D list is accessed.", 3, [
            MP("board[2][0] contains X", ["x"]),
            MP("The first index gives the row", ["row", "first index", "outer list"]),
            MP("The second index gives the column or position within that row", ["column", "second index", "position", "within"]),
        ], "board[2][0] contains \"X\". A 2D list is a list whose items are themselves lists, so it behaves like a grid. The first index selects which inner list, which corresponds to the row, and the second index selects a position within that inner list, which corresponds to the column. Here index 2 selects the third row, which is [\"X\",\"X\"], and index 0 selects the first item in it, which is \"X\". Because both indexes start at 0, care is needed not to swap them round.",
           command="State"),
        EQ("Write a program that asks the user for a name and a score, then adds them to a file called scores.txt without deleting the existing contents.", 5, [
            MP("Asks for the name", ["input", "name"]),
            MP("Asks for the score", ["input", "score"]),
            MP("Opens the file in append mode", ["\"a\"", "append", "open"]),
            MP("Writes the name and score to the file", ["write", "file.write"]),
            MP("Closes the file, or uses with open", ["close", "with open"]),
        ], "name = input(\"Enter the name: \")\nscore = input(\"Enter the score: \")\n\nwith open(\"scores.txt\", \"a\") as file:\n    file.write(name + \",\" + score + \"\\n\")\n\nprint(\"Score saved.\")\n\nThe file is opened in append mode, which is essential here because write mode would delete every score already stored. The name and score are written on one line separated by a comma so they can be split apart when the file is read back, and the newline character puts each record on its own line. Using with open means the file is closed automatically once the block finishes, even if an error occurs.",
           command="Write"),
    ],
)

Y9_APP = Topic(
    slug="app-development",
    title="App Development",
    spec="Y9.4",
    icon="i-web",
    minutes=24,
    blurb="How an app is designed before it is built: user interface, wireframes, the development cycle, and testing with real people.",
    fact="The average app is deleted within three days of being installed. Almost always the reason is not a bug, it is that the user could not work out what to do in the first thirty seconds.",
    sections=[
        Section("Designing before building", """
The temptation is to start building immediately. Almost every failed project starts that way.

### The development cycle

1. **Analysis.** Who is this for, what problem does it solve, what must it do?
2. **Design.** Plan the screens, the flow between them and the data it needs.
3. **Implementation.** Build it.
4. **Testing.** Check it works, including when things go wrong.
5. **Evaluation.** Does it actually solve the original problem?
6. **Maintenance.** Fix problems and add features.

This cycle repeats. Real apps go round it many times, which is why apps update constantly.

### Requirements

Write down what the app must do, as specific testable statements:

- The user can add a task with a title and a due date
- The user can mark a task as complete
- Completed tasks move to a separate list
- Data is saved so it is still there when the app reopens

"Make it good" is not a requirement. "The user can add a task in two taps" is.

### Wireframes

A **wireframe** is a rough sketch of a screen showing where things go, without colours or fonts. It is deliberately ugly, so that discussion stays on layout and flow rather than on whether the blue is right.

A **navigation diagram** shows how screens connect: which buttons lead where.
"""),
        Section("User interface design", """
An interface succeeds when the user does not have to think about it.

### Principles

- **Consistency.** The same action looks and behaves the same everywhere. The back button is always in the same place.
- **Feedback.** Every action produces a visible response, so the user knows it worked.
- **Clarity.** Buttons say what they do. "Save changes" beats "OK".
- **Forgiveness.** Mistakes can be undone. Destructive actions ask for confirmation.
- **Simplicity.** Fewer options is usually better. Every extra button is another decision for the user.

### Accessibility

- Large enough tap targets for people with limited dexterity
- Strong colour contrast, and never colour alone to convey meaning
- Text that works with the phone's larger font settings
- Labels on every control so a screen reader can describe it
- Works with the device turned either way

### Knowing your audience

An app for young children needs large simple controls, few words and instant feedback. An app for professionals can assume expertise and prioritise speed and density of information. Designing one as if it were the other fails both.

!key The test of an interface :: Give it to someone who has never seen it, say nothing, and watch. Wherever they hesitate is a design problem, not a user problem.
"""),
        Section("Testing and evaluation", """
### What to test

- **Functionality.** Does every feature do what the requirement said?
- **Usability.** Can a real person complete the task without help?
- **Compatibility.** Does it work on different screen sizes and devices?
- **Robustness.** What happens with no internet, an empty list, or silly input?

### Test data

- **Normal**, a typical value that should be accepted
- **Boundary**, right at the edge of what is allowed
- **Erroneous**, the wrong type entirely, which should be rejected politely

### A test plan

| Test | Data | Type | Expected result | Actual result |
| 1 | Task title "Maths" | Normal | Task added | Task added |
| 2 | Empty title | Erroneous | Message asking for a title | App crashed |
| 3 | 200 character title | Boundary | Accepted or truncated cleanly | Text overflowed the box |

Tests 2 and 3 are the useful ones. A test plan that only contains things you know will work is a waste of time.

### Evaluating

Go back to your original requirements and check them one at a time. Then be honest:

- Which requirements are fully met, partly met or not met?
- What did users struggle with?
- What would you do differently?
- What would you add next?

!warn Do not evaluate your own app by using it :: You built it, so you know where everything is. Watch someone else use it and count the number of times they hesitate.
"""),
    ],
    keyterms=[
        ("Requirement", "A specific, testable statement of something the app must do."),
        ("Wireframe", "A rough sketch of a screen layout without colours or styling."),
        ("Navigation diagram", "A diagram showing how the screens of an app connect to each other."),
        ("User interface", "The part of the app the user sees and interacts with."),
        ("Usability", "How easily a real user can achieve what they came to do."),
        ("Accessibility", "Designing so the app can be used by everyone, including people with disabilities."),
        ("Iterative development", "Repeatedly designing, building, testing and improving."),
        ("Test plan", "A table of planned tests with test data, its type, and the expected result."),
        ("Evaluation", "Judging honestly whether the finished product meets its original requirements."),
    ],
    grade="""
The top level here is about **evidence and honesty**.

**Write testable requirements.** A requirement you cannot tick off is not a requirement. "The user can add a task in two taps" can be tested. "It is easy to use" cannot.

**Test the failure cases.** A test plan full of things that work proves nothing. The value is in the tests that break it.

**Evaluate honestly.** An evaluation that says everything went perfectly scores badly, because it shows you have not looked hard. Saying "three of my five testers could not find the delete button, so I would move it into the task itself" shows real understanding.

**Justify design choices against the audience.** Large buttons because the users are young children, not because you like large buttons.

+ Write five specific testable requirements for an app
+ Draw wireframes for three screens and a navigation diagram linking them
+ Produce a test plan including boundary and erroneous data with expected results
+ Write an honest evaluation against your original requirements
""",
    mistakes=[
        "Starting to build before writing down what the app has to do.",
        "Writing requirements that cannot be tested.",
        "Only testing things that work.",
        "Evaluating by saying everything went well.",
        "Designing the interface for yourself rather than for the actual audience.",
    ],
    quiz=[
        Q("What is a wireframe?",
          ["A rough sketch of a screen layout without colours or styling",
           "The final polished design", "The code behind a screen", "A test plan"], 0,
          "It is deliberately plain so discussion stays on layout and flow rather than on visual details."),
        Q("Which is a good requirement?",
          ["The user can add a task with a title and a due date",
           "The app should be good", "It should look nice", "Users will enjoy it"], 0,
          "A requirement must be specific and testable so you can prove whether it has been met."),
        Q("What does a navigation diagram show?",
          ["How the screens of an app connect to each other",
           "The colours used in the app", "The code structure", "The test results"], 0,
          "It maps which buttons lead to which screens, so gaps and dead ends show up before building starts."),
        Q("Which test data would be most useful for a task title field with a 100 character limit?",
          ["A 101 character title", "A 20 character title",
           "A 5 character title", "A normal title"], 0,
          "Boundary data just outside the limit is exactly where errors hide."),
        Q("Why should you watch someone else use your app?",
          ["You know where everything is, so you cannot judge how obvious it is",
           "They will find bugs faster than you",
           "It is required by law",
           "It makes the app run faster"], 0,
          "Familiarity blinds you. Wherever a new user hesitates is a design problem you cannot see yourself."),
        Q("What is meant by consistency in interface design?",
          ["The same action looks and behaves the same way throughout the app",
           "Every screen uses the same colour",
           "The app never changes after release",
           "All text is the same size"], 0,
          "Consistency means the user learns the app once rather than relearning it on every screen."),
        Q("Which is an accessibility consideration?",
          ["Never using colour alone to convey meaning",
           "Using as many features as possible",
           "Making the app as small as possible",
           "Adding background music"], 0,
          "Someone who is colour blind cannot see a red field as an error, so there must be text or an icon too."),
        Q("What happens after evaluation in the development cycle?",
          ["Maintenance, and the cycle repeats with improvements",
           "The project ends permanently",
           "Analysis is skipped",
           "The app is deleted"], 0,
          "Real development is iterative, which is why apps receive updates for years after release."),
        Q("What is erroneous test data?",
          ["Data of the wrong type entirely, which should be rejected",
           "Data at the edge of the allowed range",
           "Typical data that should be accepted",
           "Data copied from another app"], 0,
          "It checks the app rejects nonsense politely rather than crashing."),
        Q("Why should destructive actions ask for confirmation?",
          ["So a mistake can be prevented rather than having to be undone",
           "To slow the user down", "To increase app size", "Because the law requires it"], 0,
          "Forgiveness is a core interface principle: make errors hard to make and easy to recover from."),
    ],
    exam=[
        EQ("State what a wireframe is and explain why one is produced before building an app.", 3, [
            MP("A rough sketch of a screen layout without styling", ["sketch", "rough", "layout", "without colours", "plain", "outline"]),
            MP("It allows the layout and flow to be planned and discussed early", ["plan", "discuss", "layout", "flow", "before building"]),
            MP("Changes are far quicker and cheaper to make on a sketch than in finished code", ["quicker", "cheaper", "easier to change", "less work", "save time"]),
        ], "A wireframe is a rough sketch of a screen showing where each element will go, drawn deliberately without colours, fonts or images. It is produced before building so that the layout and the flow between screens can be planned and discussed while everything is still easy to change. Redrawing a sketch takes a minute, whereas rebuilding a finished screen can take hours, so problems with the design are far cheaper to find at this stage. Keeping wireframes plain also helps discussion stay on whether the screen works, rather than on whether the colours are right.",
           command="State"),
        EQ("Write three testable requirements for an app that helps students keep track of homework.", 3, [
            MP("First requirement about adding homework with details", ["add", "enter", "title", "subject", "due date"]),
            MP("Second requirement about viewing or sorting tasks", ["view", "list", "sort", "order", "due", "display"]),
            MP("Third requirement about marking complete or saving data", ["complete", "tick", "done", "save", "stored", "reopen"]),
        ], "First, the user can add a homework task by entering a subject, a description and a due date. Second, the app displays all outstanding homework sorted by due date, with the nearest deadline first. Third, the user can mark a task as complete, after which it is removed from the main list, and all data is saved so that it is still present when the app is closed and reopened. Each of these is specific enough that you can test it and say clearly whether it has been achieved.",
           command="Write"),
        EQ("Explain two principles of good user interface design.", 4, [
            MP("Consistency, so the same action works the same way throughout", ["consistency", "consistent", "same way", "same place", "predictable"]),
            MP("Which means the user only has to learn the app once", ["learn once", "predictable", "know what to expect", "not relearn", "familiar"]),
            MP("Feedback, so every action produces a visible response", ["feedback", "response", "confirms", "shows", "message"]),
            MP("So the user knows their action worked and does not repeat it", ["knows it worked", "confirms", "not repeat", "reassures", "certain"]),
        ], "The first principle is consistency. The same action should look and behave the same way everywhere in the app, so a back button always appears in the same position and a save button always looks the same. This means the user only has to learn the interface once rather than working out each screen from scratch, and they can predict what will happen before they tap. The second principle is feedback. Every action the user takes should produce a visible response, whether that is a button changing appearance when pressed, a confirmation message after saving, or a loading indicator during a delay. Without feedback the user cannot tell whether their tap registered, so they tap again, which often causes duplicate entries or leaves them stuck and frustrated.",
           command="Explain"),
        EQ("Describe how you would test an app that stores a list of tasks, including the types of test data you would use.", 6, [
            MP("Test with normal data such as a typical task title", ["normal", "typical", "ordinary", "usual"]),
            MP("Test with boundary data at the limits of what is allowed", ["boundary", "edge", "limit", "maximum", "longest"]),
            MP("Test with erroneous data such as an empty entry or wrong type", ["erroneous", "empty", "blank", "letters", "invalid", "wrong type"]),
            MP("State an expected result for each test", ["expected", "should", "predicted"]),
            MP("Test usability by watching a real user complete a task", ["usability", "real user", "watch", "someone else", "observe"]),
            MP("Test robustness, such as behaviour with an empty list or no internet", ["empty list", "no internet", "robust", "crash", "unexpected"]),
        ], "I would begin with functional testing against each requirement, using three kinds of test data. Normal data would be a typical task such as the title Maths homework with a due date next week, and the expected result is that it is added and appears in the list. Boundary data would test the edges of what is allowed, for example a title of exactly the maximum length and one character longer, where the expected result is that the first is accepted cleanly and the second is either rejected with a message or truncated without breaking the layout. Erroneous data would be an empty title or letters typed into the date field, where the expected result is a clear message asking the user to correct it rather than the app crashing. Every test needs its expected result recorded in advance, because without that there is nothing to compare the actual behaviour against. Beyond functionality, I would test robustness by trying the app with an empty task list, with a very large number of tasks and with no internet connection, since these are situations that break real apps. Finally I would test usability by giving the app to someone who has never seen it, asking them to add and complete a task, and watching without helping. Every point where they hesitate is a design fault, and this is something the developer can never find on their own because they already know where everything is.",
           command="Describe"),
        EQ("Explain why an app aimed at young children should be designed differently from one aimed at adult professionals.", 4, [
            MP("Young children need large, simple controls", ["large", "big buttons", "simple", "few controls"]),
            MP("Because they have less developed reading and fine motor skills", ["reading", "motor skills", "dexterity", "cannot read", "young"]),
            MP("Professionals can be given denser information and more options", ["dense", "more options", "advanced", "information", "features", "shortcuts"]),
            MP("Because they are experienced and value speed and efficiency", ["experienced", "speed", "efficient", "quickly", "expert", "familiar"]),
        ], "An app for young children needs large tap targets, very few controls on each screen and instant obvious feedback, because young children have less developed fine motor control and may struggle to hit small buttons accurately. They may also read slowly or not at all, so meaning has to be carried by pictures, colour and sound rather than by text, and there should be very little that can go wrong because they will not read an error message. An app for adult professionals is the opposite. Those users will use it every day, so they value speed and efficiency far more than simplicity, and they can be given dense information, many options at once, keyboard shortcuts and advanced settings that would overwhelm a child. Designing either one as if it were the other fails both audiences: children get lost in an interface built for experts, and professionals get frustrated by an interface that takes five taps to do something that should take one.",
           command="Explain"),
    ],
)

Y9_AI = Topic(
    slug="artificial-intelligence",
    title="Artificial Intelligence and the Impact of Computing",
    spec="Y9.5",
    icon="i-brain",
    minutes=28,
    blurb="What machine learning actually is, why AI systems become biased, and how to think clearly about technology that is changing faster than the rules around it.",
    fact="An AI system trained to spot skin cancer became extremely good at it, until researchers discovered it had partly learned that photographs containing a ruler were more likely to be cancerous, because doctors put a ruler in the picture when they suspected something serious.",
    sections=[
        Section("What AI actually is", """
**Artificial intelligence** means computer systems performing tasks that would normally require human intelligence, such as recognising objects, understanding language or making decisions.

### Machine learning

Most modern AI uses **machine learning**. Instead of a programmer writing rules, the system is shown a very large number of examples and finds patterns in them itself.

To build a system that recognises cats:

1. Collect hundreds of thousands of images, each labelled cat or not cat, which is the **training data**
2. The system adjusts its internal values, trying to get more labels right
3. It is then tested on images it has never seen, to check it has learned something general rather than memorising
4. It can then classify new images

!key This is the crucial point :: The system has no idea what a cat is. It has found statistical patterns that correlate with the label cat. That is why it can be confidently and bizarrely wrong.

### Where you already meet it

- Recommendations on streaming services and social media
- Voice assistants and speech to text
- Face unlock on a phone
- Spam filters
- Sat nav route prediction
- Translation
- Text and image generation
"""),
        Section("Bias, error and responsibility", """
### Why AI systems become biased

An AI system learns from data, and data comes from the world, which contains bias. If a hiring system is trained on twenty years of a company's decisions, it learns the patterns in those decisions, including any discrimination in them.

Real examples include facial recognition working significantly less accurately on darker skin because the training data contained mostly light skinned faces, and recruitment tools downgrading applications that mentioned women's sports clubs.

The system is not prejudiced. It is doing exactly what it was built to do: reproduce the patterns in its training data. That is what makes it dangerous, because the output looks neutral and mathematical.

### Correlation is not understanding

The skin cancer example above is the classic case. The system found something that correlated with the answer without having any understanding of the actual problem, and it would fail completely on photographs taken a different way.

### Who is responsible

If a self driving car causes a crash, who is at fault? The owner, the manufacturer, the programmer, the company that supplied the training data, or the regulator who approved it? There is no settled answer, and the law is well behind the technology.

The same question applies when an AI system refuses someone a loan, flags a student for cheating, or recommends a longer prison sentence.

!warn AI outputs are confident, not correct :: A generated answer is produced because it is statistically likely, not because it is true. Systems that generate text will state false things with complete confidence, which is why anything important must be checked against a real source.
"""),
        Section("The wider impact of computing", """
### Employment

Technology removes some jobs and creates others. Automated checkouts, warehouse robots and translation software have all replaced human roles.

The genuine problem is not the total number of jobs. It is that the jobs created often need different skills and appear in different places from the jobs lost, so the specific people affected are not the people who benefit.

### Privacy

More of life is recorded than ever before: location, purchases, searches, messages, movement through streets covered by cameras. Individually each piece seems harmless. Combined, they describe a person in extraordinary detail.

### Environment

- Training a single large AI model can use as much electricity as several households use in a year
- Data centres run continuously and need enormous cooling
- Device manufacturing consumes rare earth metals, and mining damages habitats
- E-waste contains toxic materials and is often exported to countries with weaker protections

Against this: video calls replace flights, digital documents replace paper, smart heating cuts energy use, and AI is being used to design more efficient materials and predict extreme weather.

### How to think about it

The useful question is never "is this technology good or bad". It is:

- **Who benefits?**
- **Who bears the cost?**
- **Who decided, and were the people affected consulted?**
- **What would need to be true for this to be acceptable?**

Answer those four and you have a genuinely thoughtful argument rather than an opinion.
"""),
    ],
    keyterms=[
        ("Artificial intelligence", "Computer systems performing tasks that would normally require human intelligence."),
        ("Machine learning", "An approach where a system finds patterns in large amounts of example data rather than following written rules."),
        ("Training data", "The labelled examples a machine learning system learns patterns from."),
        ("Bias", "Systematic unfairness in an AI system's output, usually caused by unrepresentative training data."),
        ("Algorithm", "A set of step by step rules for solving a problem or making a decision."),
        ("Automation", "Using machines or software to perform work previously done by people."),
        ("E-waste", "Discarded electronic equipment, often containing toxic materials."),
        ("Accountability", "Being answerable for a decision, which becomes difficult when a machine made it."),
    ],
    grade="""
The top level here is about **thinking clearly, not having strong opinions**.

**Explain the mechanism of bias.** Not "AI can be racist", but "the system reproduces the patterns in its training data, so if that data reflects past discrimination the system will reproduce it while appearing neutral and objective".

**Give both sides.** AI both consumes enormous energy and helps design more efficient systems. Both are true and a good answer says so.

**Name who is affected.** Not "some people lose their jobs", but "checkout staff, who are often in low income areas with few alternative employers".

**Reach a judgement.** After both sides, say what you think should happen and why.

+ Explain how machine learning works in four steps
+ Explain why an AI system can be biased without anyone intending it
+ Discuss the impact of automation on employment, giving both sides
+ Explain why an AI generated answer should be checked against a real source
""",
    mistakes=[
        "Saying AI 'understands' or 'thinks'. It finds statistical patterns.",
        "Saying AI is biased because the programmers were prejudiced. The usual cause is unrepresentative training data.",
        "Giving only negative environmental impacts.",
        "Treating an AI generated answer as a source. It is confident, not verified.",
        "Writing a one sided answer on impact, which cannot reach the top level.",
    ],
    quiz=[
        Q("What is machine learning?",
          ["A system finding patterns in large amounts of example data rather than following written rules",
           "A computer that thinks like a human",
           "Software that writes itself with no data",
           "A type of computer hardware"], 0,
          "The programmer supplies data and a method for learning, not the rules themselves."),
        Q("Why might a facial recognition system work less accurately on some groups?",
          ["The training data contained far fewer examples of those faces",
           "The camera cannot detect certain colours",
           "The algorithm was written to discriminate",
           "Those faces are harder to photograph"], 0,
          "The system reproduces what is in its training data, so gaps in that data become gaps in accuracy."),
        Q("What is training data?",
          ["The labelled examples a system learns patterns from",
           "The code that runs the AI",
           "The results the AI produces",
           "The hardware the AI runs on"], 0,
          "Its quality and representativeness determine almost everything about how the system behaves."),
        Q("Why should an AI generated answer be checked against another source?",
          ["It is produced because it is statistically likely, not because it is true",
           "AI systems are always wrong",
           "It is illegal to use AI answers",
           "AI answers are always too long"], 0,
          "These systems will state false things with complete confidence, because confidence and accuracy are not linked."),
        Q("A system that recommends videos is an example of:",
          ["Machine learning finding patterns in what you have watched",
           "A human choosing videos for you",
           "Random selection",
           "A rule written by a programmer for each user"], 0,
          "Recommendation systems learn patterns from the behaviour of millions of users."),
        Q("Which is a genuine problem with automation and employment?",
          ["The jobs created often need different skills and are in different places from those lost",
           "There will be no jobs left at all",
           "Machines cannot do any human job",
           "Automation always creates more jobs than it removes in the same town"], 0,
          "The total number of jobs is not the real issue. The mismatch for the specific people affected is."),
        Q("Which is a positive environmental impact of computing?",
          ["Video calls reducing the need for business flights",
           "Data centres consuming electricity",
           "E-waste being exported",
           "Mining rare earth metals"], 0,
          "The others are all costs. A good answer includes both sides."),
        Q("Who is responsible when a self driving car causes a crash?",
          ["It is genuinely unsettled and involves the owner, manufacturer and regulator",
           "Always the owner", "Always the programmer", "Nobody, it is an accident"], 0,
          "This is exactly the kind of question where the law is well behind the technology."),
        Q("An AI trained on a hospital's past decisions may reproduce past unfairness because:",
          ["It learns the patterns in the data, including any discrimination",
           "It was programmed to be unfair",
           "Hospitals always make unfair decisions",
           "AI systems prefer certain groups"], 0,
          "The system has no concept of fairness. It reproduces whatever patterns exist in what it was shown."),
        Q("Which question is most useful when judging a new technology?",
          ["Who benefits and who bears the cost", "Is it new",
           "Is it expensive", "Do most people like it"], 0,
          "Asking who gains and who loses produces a far more thoughtful argument than asking whether it is good or bad."),
    ],
    exam=[
        EQ("Explain what is meant by machine learning.", 3, [
            MP("The system is given a large amount of example data", ["data", "examples", "training data", "lots of"]),
            MP("It finds patterns in that data rather than following rules written by a programmer", ["patterns", "itself", "not programmed", "no rules written", "learns"]),
            MP("It can then apply what it has learned to new data it has not seen before", ["new data", "unseen", "apply", "predict", "classify"]),
        ], "Machine learning is an approach to artificial intelligence in which a system is given a very large amount of example data rather than being given rules by a programmer. The system adjusts its internal values so that it becomes better at producing the correct answer for those examples, effectively finding statistical patterns in the data by itself. Once trained, it can apply those patterns to new data it has never seen before, for example classifying a photograph it was not trained on. Importantly, it has no understanding of what it is looking at, only patterns that correlate with the right answer.",
           command="Explain"),
        EQ("Explain why an artificial intelligence system might produce biased results.", 4, [
            MP("The system learns from training data", ["training data", "learns from", "data it was given", "examples"]),
            MP("If that data is unrepresentative or reflects past unfairness, the system learns that", ["unrepresentative", "reflects", "past decisions", "unfair", "skewed", "not enough examples"]),
            MP("The system reproduces those patterns in its output", ["reproduces", "repeats", "same pattern", "outputs", "continues"]),
            MP("This happens without anyone intending it, and the output looks objective", ["not intended", "no one meant", "appears objective", "looks neutral", "mathematical"]),
        ], "An AI system does not have rules written for it. Instead it learns patterns from its training data, so whatever is in that data shapes how it behaves. If the training data is unrepresentative, for example a facial recognition system trained mostly on light skinned faces, the system will simply be less accurate on the groups that were underrepresented. If the training data reflects past human decisions that were unfair, such as years of recruitment decisions at a company, the system learns those patterns too and continues to apply them. What makes this particularly dangerous is that nobody has to intend it: the bias arrives through the data rather than through anyone's prejudice, and because the output comes from a computer it can appear objective and mathematical, so it is trusted more than a human decision would be.",
           command="Explain"),
        EQ("Give one advantage and one disadvantage of using AI to mark student work.", 4, [
            MP("Advantage: marking is much faster", ["faster", "quicker", "instant", "speed", "immediately"]),
            MP("Advantage explained, such as students getting feedback sooner or teachers having more time", ["feedback", "sooner", "teacher time", "workload", "more time"]),
            MP("Disadvantage: it may not understand an unusual but correct answer", ["unusual", "correct but different", "does not understand", "creative", "unexpected"]),
            MP("Disadvantage explained, such as unfair marks or students learning to write for the machine", ["unfair", "wrong mark", "write for the machine", "penalised", "narrow"]),
        ], "An advantage is speed. An AI system can mark thousands of pieces of work in the time it takes a teacher to mark a handful, which means students receive feedback while the work is still fresh in their minds rather than a fortnight later, and it frees a great deal of teacher time for actual teaching. A disadvantage is that the system does not understand the subject, it recognises patterns, so an answer that is correct but phrased in an unusual or original way may be marked down simply because it does not match what the system learned to expect. Over time this risks teaching students to write for the marking system rather than to think clearly, which is the opposite of what education is for.",
           command="Give"),
        EQ("Discuss the impact of increased automation on employment.", 8, [
            MP("Automation removes some existing jobs", ["removes", "replaces", "lost", "redundant", "fewer jobs"]),
            MP("Gives a specific example such as checkout staff or warehouse workers", ["checkout", "warehouse", "factory", "driver", "call centre", "cashier"]),
            MP("Automation also creates new jobs", ["creates", "new jobs", "new roles", "different jobs"]),
            MP("Gives examples such as maintenance, programming or data roles", ["maintenance", "programming", "engineers", "technicians", "data"]),
            MP("The new jobs often need different skills from the jobs lost", ["different skills", "retraining", "qualifications", "skills gap"]),
            MP("The people who lose out are often not the people who benefit", ["not the same people", "different people", "affected", "benefit", "unequal"]),
            MP("Considers benefits such as lower prices, safer work or higher productivity", ["cheaper", "prices", "safer", "productivity", "efficient", "dangerous jobs"]),
            MP("Reaches a supported conclusion with a suggestion such as retraining or support", ["conclusion", "overall", "retraining", "support", "government", "therefore", "should"]),
        ], "Increased automation clearly removes some existing jobs. Self service checkouts have reduced the number of cashiers needed in supermarkets, warehouse robots have replaced pickers, and automated systems have taken over much routine work in factories and call centres. At the same time automation creates new roles, including engineers who design and build the systems, technicians who maintain them, programmers who develop the software and analysts who work with the data they produce. The overall number of jobs in an economy has historically not collapsed because of automation. The real difficulty is that the jobs created are not the same jobs, do not need the same skills and are frequently not in the same places. A supermarket cashier made redundant in a small town does not simply become a robotics technician, because that requires qualifications, training and often relocation, and the areas that lose the most routine work are often those with fewest alternative employers. So the costs fall on specific people who did nothing wrong, while the benefits go to shareholders and to consumers generally. Those benefits are genuine: automation lowers prices, increases productivity and removes people from work that is dangerous, repetitive or damaging to health, and few would argue for putting humans back into the most hazardous factory roles. Overall, automation should not be resisted, because the productivity and safety gains are real and the alternative is simply falling behind. However, it cannot be treated as automatically fine either. Governments and employers have a responsibility to fund retraining, to give reasonable notice, and to support the regions most affected, because otherwise the pattern is that society as a whole gains while a specific and largely powerless group pays for it.",
           command="Discuss"),
        EQ("Explain why an AI system that generates written answers should not be relied on as a source of factual information.", 3, [
            MP("It produces text that is statistically likely rather than verified as true", ["likely", "statistical", "pattern", "not verified", "probable"]),
            MP("It can therefore state incorrect information confidently", ["incorrect", "wrong", "false", "confidently", "made up", "invented"]),
            MP("Answers should be checked against a reliable source", ["check", "verify", "reliable source", "another source", "confirm"]),
        ], "A text generating AI produces each part of its answer because it is statistically likely to follow what came before, based on patterns learned from enormous amounts of text. It has no mechanism for checking whether what it is producing is actually true, and it does not know what it does or does not know. As a result it can state completely incorrect information, including invented statistics, references and quotations, in exactly the same fluent and confident tone it uses for correct information, which makes errors very hard to spot. Anything important that comes from such a system therefore has to be checked against a reliable independent source before it is used or repeated.",
           command="Explain"),
    ],
)

Y9_3D = Topic(
    slug="3d-modelling-and-animation",
    title="3D Modelling and Animation",
    spec="Y9.6",
    icon="i-cube",
    minutes=22,
    blurb="How 3D objects are built from vertices, edges and faces, how animation works with keyframes, and what actually happens when a scene is rendered.",
    fact="Every 3D model in every film and game is made entirely of flat triangles. Curved surfaces do not exist. They are thousands of tiny triangles arranged so the edges become invisible.",
    sections=[
        Section("How 3D models are built", """
### The building blocks

| Term | Meaning |
| **Vertex** | A single point in 3D space, with x, y and z coordinates |
| **Edge** | A straight line joining two vertices |
| **Face** | A flat surface enclosed by edges, usually a triangle or a square |
| **Mesh** | The complete set of vertices, edges and faces making up an object |

A cube has 8 vertices, 12 edges and 6 faces. A detailed character model may have hundreds of thousands.

### Polygon count

More polygons means more detail and smoother curves, and also more processing power and memory needed.

This is the central trade off in 3D work:

- A film can afford millions of polygons per character, because each frame is rendered once over hours
- A game must render 60 frames every second, so models are far simpler and use clever texturing to fake detail

### Modelling techniques

- **Primitives**: start from a basic shape such as a cube, sphere or cylinder
- **Extrude**: pull a face outwards to create new geometry
- **Subdivide**: split faces into smaller ones to add detail
- **Loop cut**: add a ring of new edges around a model
- **Modifiers**: non destructive effects such as mirror, which builds one half and reflects it automatically

### Coordinates

3D space uses three axes: **x** across, **y** depth and **z** height, though which is which varies between programs. Every vertex has a position, and every object can be moved, rotated and scaled along each axis.
"""),
        Section("Materials, lighting and cameras", """
### Materials and textures

A **material** describes how a surface behaves with light: its colour, how shiny it is, how rough, whether it is transparent or metallic.

A **texture** is an image wrapped onto the surface to give detail without adding geometry. **UV mapping** is the process of unwrapping a 3D surface flat so a 2D image can be applied to it accurately.

Textures are how a simple model gains detail cheaply. A brick wall can be a single flat face with a brick texture rather than thousands of individually modelled bricks.

### Lighting

Lighting does more than make a scene visible. It creates mood and makes shapes readable.

- **Point light**, radiating in all directions from one spot, like a bulb
- **Sun or directional light**, parallel rays from far away, like sunlight
- **Spot light**, a cone, like a stage light
- **Area light**, a soft light from a surface, like a window

The classic setup is **three point lighting**: a bright **key light** as the main source, a softer **fill light** to lift the shadows on the other side, and a **back light** to separate the subject from the background.

### Cameras

The camera decides what the viewer sees. Changing its position, angle and focal length completely changes how a scene feels. A low angle makes a subject look powerful, a high angle makes it look small.
"""),
        Section("Animation and rendering", """
### Keyframes

An animator does not draw every frame. They set **keyframes** at important moments, and the software calculates the frames in between, which is called **interpolation** or tweening.

To move a ball from left to right over two seconds at 24 frames per second:

1. Set a keyframe at frame 1 with the ball on the left
2. Set a keyframe at frame 48 with the ball on the right
3. The software generates the 46 frames between

### Making it look right

- **Easing** means starting and stopping gradually rather than at constant speed, because real objects accelerate and decelerate
- **Squash and stretch** makes objects feel like they have weight
- **Anticipation** is a small movement in the opposite direction before the main action
- **Follow through** means parts keep moving after the main body stops

### Rendering

**Rendering** is calculating the final image from the scene: working out how light bounces, what each surface looks like from the camera and what is in front of what.

It is extremely demanding. A single frame of a modern animated film can take hours on a powerful machine, which is why studios use **render farms** of hundreds of computers.

    24 frames per second x 60 seconds = 1440 frames for one minute

At 30 minutes per frame that is 720 hours, which is 30 days on one computer.

!key Why games and films look different :: A film renders each frame once, slowly, so it can afford perfect lighting and millions of polygons. A game must render every frame in under a sixtieth of a second while responding to the player, so it uses simpler models and approximations. The constraint is time, not talent.
"""),
    ],
    keyterms=[
        ("Vertex", "A single point in 3D space defined by x, y and z coordinates."),
        ("Edge", "A straight line connecting two vertices."),
        ("Face", "A flat surface enclosed by edges, forming part of a model's surface."),
        ("Mesh", "The complete set of vertices, edges and faces that make up a 3D object."),
        ("Polygon count", "The number of faces in a model, affecting both detail and performance."),
        ("Texture", "An image applied to a surface to add detail without adding geometry."),
        ("UV mapping", "Unwrapping a 3D surface flat so a 2D texture can be applied accurately."),
        ("Keyframe", "A frame where the animator sets a value, with the software calculating the frames between."),
        ("Interpolation", "The software generating the in between frames from the keyframes."),
        ("Rendering", "Calculating the final image from the 3D scene, including light, materials and perspective."),
    ],
    grade="""
The top level here is about **explaining trade offs**.

**Polygon count is always a trade off.** More polygons means more detail and more processing. Say both halves.

**Explain why textures matter.** A texture adds visible detail at almost no performance cost, which is why a brick wall is one flat face with an image on it rather than thousands of modelled bricks.

**Explain rendering time with a calculation.** Frames per second multiplied by duration gives the number of frames, and multiplying by time per frame shows why render farms exist.

**Justify lighting choices.** Three point lighting is not a rule to memorise. The key light provides the main illumination, the fill lifts the shadows so detail is not lost, and the back light separates the subject from the background.

+ Define vertex, edge, face and mesh and give the counts for a cube
+ Explain the trade off in polygon count for a game against a film
+ Explain how keyframes and interpolation produce animation
+ Calculate the total render time for a given length of animation
""",
    mistakes=[
        "Saying more polygons is simply better. It costs performance, which matters enormously in games.",
        "Confusing a material with a texture. A material describes how the surface behaves with light, a texture is an image applied to it.",
        "Thinking every frame is animated by hand. Keyframes are set and the software interpolates.",
        "Saying rendering is 'saving the file'. It is calculating the image, which is why it takes so long.",
    ],
    quiz=[
        Q("What is a vertex?", ["A single point in 3D space", "A flat surface",
                                "A line between two points", "The whole model"], 0,
          "Vertices are the points. Edges join them and faces fill the gaps between edges."),
        Q("How many faces does a cube have?", ["6", "8", "12", "4"], 0,
          "A cube has 8 vertices, 12 edges and 6 faces."),
        Q("Why do games use models with fewer polygons than films?",
          ["Games must render every frame in a fraction of a second while responding to the player",
           "Game artists are less skilled",
           "Game engines cannot display curves",
           "Films use only two dimensions"], 0,
          "A film renders each frame once over hours. A game has under a sixtieth of a second per frame."),
        Q("What is a texture?",
          ["An image applied to a surface to add detail without adding geometry",
           "The number of polygons in a model",
           "A type of light",
           "The camera position"], 0,
          "Textures are how simple models gain rich visual detail cheaply."),
        Q("What is a keyframe?",
          ["A frame where the animator sets a value, with the frames between calculated automatically",
           "The first frame of an animation",
           "The most detailed frame",
           "A frame that has been rendered"], 0,
          "Setting the important moments and letting the software interpolate is what makes animation practical."),
        Q("What is rendering?",
          ["Calculating the final image from the 3D scene",
           "Saving the project file",
           "Adding textures to a model",
           "Moving the camera"], 0,
          "Rendering works out light, shadow, materials and perspective, which is why it is so computationally expensive."),
        Q("In three point lighting, what does the back light do?",
          ["Separates the subject from the background",
           "Provides the main illumination",
           "Softens the shadows on the dark side",
           "Colours the whole scene"], 0,
          "The key light is the main source and the fill lifts shadows. The back light creates a rim that lifts the subject away from the background."),
        Q("A one minute animation at 24 frames per second needs how many frames?",
          ["1440", "24", "60", "144"], 0,
          "24 multiplied by 60 gives 1440 frames for a single minute."),
        Q("What does UV mapping do?",
          ["Unwraps a 3D surface flat so a 2D image can be applied accurately",
           "Adds ultraviolet lighting to a scene",
           "Reduces the polygon count",
           "Sets the camera angle"], 0,
          "Without it, a flat image applied to a curved surface stretches and distorts."),
        Q("What does easing add to an animation?",
          ["Gradual acceleration and deceleration, so movement looks natural",
           "More polygons", "Better lighting", "Faster rendering"], 0,
          "Real objects do not start and stop instantly, so constant speed movement looks mechanical."),
    ],
    exam=[
        EQ("State what is meant by a vertex, an edge and a face in a 3D model.", 3, [
            MP("A vertex is a point in 3D space", ["vertex", "point", "coordinate"]),
            MP("An edge is a line connecting two vertices", ["edge", "line", "joins", "connects"]),
            MP("A face is a flat surface enclosed by edges", ["face", "surface", "flat", "enclosed"]),
        ], "A vertex is a single point in three dimensional space, defined by its x, y and z coordinates. An edge is a straight line connecting two vertices. A face is a flat surface enclosed by edges, usually a triangle or a four sided shape, and together the vertices, edges and faces form the mesh that makes up the object.",
           command="State"),
        EQ("Explain why a model used in a video game usually has fewer polygons than the same character in an animated film.", 4, [
            MP("A game must render frames in real time as the player plays", ["real time", "as the player", "instantly", "live", "interactive"]),
            MP("Around 60 frames must be produced every second", ["60", "frames per second", "fps", "every second", "fraction of a second"]),
            MP("A film renders each frame once in advance, taking as long as needed", ["in advance", "once", "hours", "not live", "pre rendered"]),
            MP("Fewer polygons means the game runs smoothly, with textures used to suggest detail", ["smooth", "performance", "runs well", "textures", "fake detail", "frame rate"]),
        ], "A video game has to produce each frame in real time while the player is controlling the character, which means the computer typically has less than a sixtieth of a second to work out lighting, positions and surfaces for the entire scene. If a model contains too many polygons the machine cannot keep up and the frame rate drops, which makes the game feel unresponsive and unplayable. An animated film has no such constraint, because each frame is rendered once in advance and can take minutes or even hours on a render farm, so millions of polygons per character are affordable. Game artists therefore use much simpler meshes and rely on detailed textures and lighting tricks to suggest detail that is not actually modelled, which costs almost no performance while looking convincing on screen.",
           command="Explain"),
        EQ("Describe how keyframes are used to create an animation.", 3, [
            MP("The animator sets values at particular frames", ["sets", "particular frames", "important moments", "positions"]),
            MP("These are the keyframes marking the start and end of a movement", ["keyframes", "start", "end", "key positions"]),
            MP("The software calculates the frames in between by interpolation", ["in between", "interpolation", "calculates", "generates", "tween"]),
        ], "Rather than creating every single frame by hand, the animator sets the position, rotation or other property of an object at a small number of important moments, and each of these is recorded as a keyframe. For example, a keyframe at frame 1 might place a ball on the left of the screen and a keyframe at frame 48 might place it on the right. The software then calculates all the frames in between automatically, a process called interpolation, gradually changing the value from one keyframe to the next. The animator can adjust how that change happens, for example using easing so the movement accelerates and slows rather than travelling at a constant speed, which looks far more natural.",
           command="Describe"),
        EQ("An animation lasts 90 seconds and runs at 25 frames per second. Each frame takes 4 minutes to render. Calculate the total render time in hours.", 4, [
            MP("Calculates the number of frames as 25 x 90", ["25 x 90", "2250", "frames"]),
            MP("Obtains 2250 frames", ["2250"]),
            MP("Multiplies by 4 minutes to get 9000 minutes", ["9000", "x 4", "minutes"]),
            MP("Converts to 150 hours", ["150", "hours", "divide by 60"]),
        ], "The total number of frames is the frame rate multiplied by the duration, so 25 x 90 = 2250 frames. Each frame takes 4 minutes, so the total render time is 2250 x 4 = 9000 minutes. Dividing by 60 converts this to 150 hours, which is over six days of continuous rendering on a single machine, and this is exactly why studios use render farms of hundreds of computers working on different frames at the same time.",
           command="Calculate"),
        EQ("Explain the purpose of a texture in 3D modelling.", 3, [
            MP("A texture is an image applied to the surface of a model", ["image", "applied", "surface", "wrapped"]),
            MP("It adds visual detail without adding polygons", ["without", "no extra polygons", "detail", "geometry"]),
            MP("This keeps the model efficient while still looking detailed", ["efficient", "performance", "faster", "looks detailed", "saves"]),
        ], "A texture is a two dimensional image that is wrapped onto the surface of a 3D model, using UV mapping to ensure it lines up correctly on a curved or complex shape. Its purpose is to add visual detail such as wood grain, brickwork, rust or fabric weave without adding any extra geometry to the model. This matters enormously for performance: modelling every individual brick in a wall would require an enormous number of polygons and slow the scene down, whereas a single flat face with a brick texture looks convincing and costs almost nothing to render.",
           command="Explain"),
    ],
)

# ================================================================== COURSE

COURSE = Course(
    slug="ks3",
    title="Key Stage 3 Computing",
    short="Key Stage 3",
    stage="KS3",
    board="National Curriculum",
    code="",
    goal="Top band",
    icon="i-layers",
    accent="var(--lilac-deep)",
    blurb="Years 7, 8 and 9 in the order they are taught. Computer science, information technology and digital literacy, explained properly so that starting GCSE feels like carrying on rather than starting again.",
    intro="",
    journey=[
        ("Understand it, do not just do it",
         "It is possible to finish every task in a lesson without understanding any of it. Read the explanation on each topic and check you could explain it to somebody else.", ""),
        ("Get full marks on the knowledge checks",
         "Ten questions per unit. If you get eight, go back to the two sections you missed. Nobody ever improved by moving on from the bits they found hard.", ""),
        ("Write the longer answers out",
         "Five written questions per unit, marked against a real mark scheme. Writing an answer is a completely different skill from recognising one, and it is the one that gets tested.", ""),
        ("Build the habit early",
         "Twenty minutes a week from Year 7 puts you two years ahead by GCSE. Nobody who gets a grade 9 started revising in Year 11.", ""),
        ("Keep coding outside lessons",
         "One small Python project a term will do more for you than any amount of note reading. Build something you actually want to exist.", ""),
    ],
    units=[
        Unit("year-7", "Year 7", "Your first year of computing: using computers properly, your first programs in Scratch and Python, what is inside the machine, and vector graphics.",
             [Y7_USING, Y7_SCRATCH, Y7_PYTHON, Y7_UNDERSTAND, Y7_VECTOR], icon="i-play", term="Year 7"),
        Unit("year-8", "Year 8", "Staying safe online, thinking like a computer scientist, real Python programs, spreadsheets, networks and building web pages.",
             [Y8_DIGLIT, Y8_COMPTHINK, Y8_PYTHON, Y8_SPREAD, Y8_NETWORKS, Y8_WEB], icon="i-network", term="Year 8"),
        Unit("year-9", "Year 9", "The bridge into GCSE: the law, data representation in full, structured Python, app development, artificial intelligence and 3D animation.",
             [Y9_DIGLIT, Y9_DATAREP, Y9_PYTHON, Y9_APP, Y9_AI, Y9_3D], icon="i-brain", term="Year 9"),
    ],
)
