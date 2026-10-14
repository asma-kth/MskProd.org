"""Illustrations for programming: the ideas every board teaches, drawn once and shared.

Most of these are placed on several topics at once, because OCR, AQA, Edexcel,
Key Stage 3 and the Python course all teach the same variable, the same loop
and the same function in nearly the same words.
"""
from .illus import Canvas, PAL, INK, figure, illustration, _n
from . import illus_props as P
from . import illus_glyphs as G


def cw(size):
    return size * .6


# ------------------------------------------------------------ first program

@illustration("hello-world")
def _hello():
    cv = Canvas(800, 500).backdrop()
    size = 17
    lines = ['name = "Asha"', 'print("Hi", name)', 'print("Hello, world!")   # a greeting']
    x0, y0, W = 24, 40, 500
    cv.add(G.code(cv, x0, y0, W, lines, "hello.py", size, hl=(2,)))
    tx = G.code_x(x0, size)
    c = cw(size)
    # underline the three ideas on the line they live on
    by = G.code_y(y0, 2, size) + 6
    cv.add(cv.rect(tx, by, 5 * c, 4, 2, "#66B8EC"), cv.rect(tx + 6 * c, by, 15 * c, 4, 2, "#62CFA3"),
           cv.rect(tx + 25 * c, by, 12 * c, 4, 2, "#FFCC4A"))
    bottom = y0 + G.code_h(3, size)
    cards = [(24, "sky", "print()", ["a function that", "shows what is", "in the brackets"], tx + 2.5 * c),
             (192, "mint", "\"text\"", ["text goes inside", "quote marks: it", "is called a string"], tx + 13.5 * c),
             (360, "sun", "# comment", ["Python ignores it:", "a note for people", "reading the code"], tx + 31 * c)]
    for i, (x, col, head, body, ax) in enumerate(cards):
        yy = 226
        cv.add(cv.line(ax, by + 5, ax, yy - 2, PAL[col][2], 2.4, dash="3 5"))
        cv.add(P.lift(cv, x, yy, 156, 108, col, 14, 6, hl=False))
        cv.add(cv.text(x + 78, yy + 28, head, 17, 800, fill=P._on(col), mono=True))
        for k, t in enumerate(body):
            cv.add(cv.text(x + 78, yy + 52 + k * 17, t, 12.5, 650, fill=P._on(col)))
    # run it
    cv.add(P.lift(cv, 560, 52, 116, 46, "green", 14, 6))
    cv.add(cv.poly([(583, 64), (583, 86), (603, 75)], P._on("green")), cv.text(642, 82, "Run", 17, 800, fill=P._on("green")))
    cv.add(P.curve_arrow(cv, (524, 120), (548, 150), (560, 154), (578, 162), PAL["teal"][2], 5, 13))
    cv.add(G.terminal(cv, 540, 128, 236, ["Hi Asha", "Hello, world!"], "output", 16))
    # Pixel explains the order
    cv.add(P.pixel_cat(cv, 30, 366, 96))
    cv.add(G.bubble(cv, 146, 372, 380, 70, ["Python reads your program from the top,", "one line at a time."], (-180, 30), 15))
    cv.add(P.badge(cv, W + x0 - 18, y0 + 14, 1), P.badge(cv, 210, 226, 2), P.badge(cv, 378, 226, 3), P.badge(cv, 762, 130, 4))
    return figure(
        "hello-world", cv, "Your first program: print, a string and a comment",
        "A small Python program in a code editor, with its output beside it. The line print, bracket, quote Hello comma world quote, bracket "
        "is a function call: print is the function, the brackets hold what it is given, and the text inside the quote marks is a string. "
        "After it, a hash starts a comment, which Python ignores and which is there for the people reading the code. Pressing Run "
        "makes the program execute from the top, one line at a time, and the output appears in the console: Hi Asha and then Hello, world! "
        "The first print shows two things at once, a string and the variable name, separated by a space.",
        ["print() is a function: it displays whatever is inside the brackets.",
         "Text goes inside quote marks. Text in quotes is called a string.",
         "Anything after a # is a comment. Python ignores it: it is a note for people.",
         "Run it and the output appears. Python works from the top, one line at a time."],
        "Every program starts like this: a command, brackets, and what to show.")


# ---------------------------------------------------------------- variables

@illustration("variables-boxes")
def _variables():
    cv = Canvas(800, 500).backdrop()
    size = 15
    lines = ['name = "Asha"', 'age = 15', 'price = 2.50', 'passed = True', 'age = age + 1', 'PI = 3.14159']
    cols = {0: "#F77F72", 1: "#66B8EC", 2: "#62CFA3", 3: "#FFCC4A", 4: "#66B8EC", 5: "#8B6BB8"}
    cv.add(G.code(cv, 24, 40, 330, lines, "variables.py", size, bars=cols))
    # good and bad names
    cv.add(P.card(cv, 24, 262, 330, 216, 18, "Naming a variable", "teal"))
    names = [(True, "total_score", "words joined by _"), (True, "age2", "digits are fine inside"), (False, "2nd_place", "cannot start with a digit"), (False, "my score", "no spaces")]
    for i, (ok, n, why) in enumerate(names):
        yy = 306 + i * 42
        cv.add(P.tick(cv, 52, yy, 11) if ok else P.cross(cv, 52, yy, 11))
        cv.add(cv.text(76, yy - 2, n, 15, 800, anchor="start", cls="il-ink", mono=True), cv.text(76, yy + 15, why, 12, 600, anchor="start", cls="il-ink2"))
    # the boxes the code builds
    cv.add(P.card(cv, 380, 34, 396, 444, 20, "What the computer keeps", "plum"))
    cv.add(G.var_box(cv, 404, 84, 160, 112, "name", '"Asha"', "str", "wood", "coral", 22))
    cv.add(G.var_box(cv, 596, 84, 160, 112, "age", "16", "int", "wood", "sky", 28))
    cv.add(cv.text(676, 76, "replaces 15", 12.5, 700, cls="il-ink2", mono=True))
    cv.add(G.var_box(cv, 404, 244, 160, 112, "price", "2.5", "float", "wood", "mint", 28))
    cv.add(G.var_box(cv, 596, 244, 160, 112, "passed", "True", "bool", "wood", "sun", 24))
    cv.add(G.var_box(cv, 500, 376, 160, 74, "PI", "3.14159", None, "metal", "plum", 18))
    cv.add(P.padlock(cv, 654, 372, .62, "sun"))
    cv.add(cv.text(580, 472, "a constant: never changes", 12.5, 700, cls="il-ink2"))
    cv.add(P.badge(cv, 40, 44, 1), P.badge(cv, 560, 84, 2), P.badge(cv, 752, 84, 3), P.badge(cv, 502, 388, 4), P.badge(cv, 40, 262, 5))
    return figure(
        "variables-boxes", cv, "Variables as labelled boxes, with the code that makes them",
        "Six lines of code on the left and the boxes they create on the right. The equals sign is assignment: it stores the value on its right "
        "in the variable named on its left. Every variable is like a labelled box with a name, a value and a data type. name holds the string "
        "Asha, age holds the whole number 15, price holds the decimal 2.5 and passed holds True. The fifth line, age equals age plus one, takes "
        "the 15 out and puts 16 in, which shows that the value of a variable can change while its name stays the same. PI is a constant: a value "
        "that must never change, written in capitals by convention and shown with a padlock. A card at the bottom left gives the naming rules: "
        "use letters, digits and underscores, do not start with a digit and never use a space.",
        ["= stores a value in a variable: the name on the left, the value on the right.",
         "A variable is a labelled box with a name, a value and a data type.",
         "The value can change. age = age + 1 takes the 15 out and puts 16 in.",
         "A constant holds a value that must never change. By convention it is written in capitals.",
         "Names use letters, digits and underscores. No spaces, and no digit first."],
        "The name stays. The value is what you can swap.")


# -------------------------------------------------------------- data types

@illustration("data-types")
def _types():
    cv = Canvas(800, 500).backdrop()
    kinds = [("Integer", "sky", "42", "-7  0  2025", "int", "whole numbers"),
             ("Real", "teal", "3.14", "0.5  -2.75", "float", "with a decimal point"),
             ("Boolean", "sun", None, "True  False", "bool", "only two values"),
             ("Character", "coral", "A", "z  7  ?", "str", "one single symbol"),
             ("String", "plum", '"Hi"', '"07700 900123"', "str", "text in quotes")]
    for i, (name, col, big, small, py, desc) in enumerate(kinds):
        x = 24 + i * 153.5
        cv.add(P.card(cv, x, 40, 146, 196, 18, name, col))
        if big is None:
            cv.add(P.toggle(cv, x + 45, 84, True, 56, 30), P.toggle(cv, x + 45, 126, False, 56, 30))
        else:
            cv.add(P.lift(cv, x + 24, 78, 98, 64, "paper", 14, 6, hl=False), cv.text(x + 73, 121, big, 28 if len(big) < 5 else 22, 800, fill=INK, mono=True))
        cv.add(cv.text(x + 73, 172, small, 12.5 if len(small) < 12 else 11.5, 700, cls="il-ink", mono=True))
        cv.add(cv.text(x + 73, 192, desc, 12, 600, cls="il-ink2"))
        cv.add(P.pill(cv, x + 73, 216, py, "paper", 13, 10, 22, 800))
    cv.add(P.badge(cv, 36, 42, 1))
    # why a phone number is a string
    cv.add(P.card(cv, 24, 268, 372, 212, 18, "A phone number is a string", "coral"))
    cv.add(P.phone(cv, 50, 312, .86, cv.text(32, 46, "07700", 15, 800, fill=INK, mono=True) + cv.text(32, 66, "900123", 15, 800, fill=INK, mono=True)))
    cv.add(P.pill(cv, 250, 330, "you never add phone numbers", "paper", 13, 12, 26, 700))
    cv.add(P.pill(cv, 250, 372, "a number would lose the 0", "paper", 13, 12, 26, 700))
    cv.add(cv.text(250, 416, "07700  as a number  =  7700", 14, 800, cls="il-ink", mono=True), cv.text(250, 440, "so it is stored as text", 13, 650, cls="il-ink2"))
    cv.add(P.badge(cv, 40, 270, 2))
    # casting
    cv.add(P.card(cv, 420, 268, 356, 212, 18, "Casting: changing type", "teal"))
    rows = [('"42"', 'int()', "42", "to a whole number"), ("42", 'str()', '"42"', "to text"), ("3.9", 'int()', "3", "cuts off the .9")]
    for i, (a_, f, b_, note) in enumerate(rows):
        yy = 322 + i * 52
        cv.add(P.lift(cv, 438, yy - 15, 62, 30, "paper", 9, 4, hl=False), cv.text(469, yy + 6, a_, 15, 800, fill=INK, mono=True))
        cv.add(P.arrow(cv, [(506, yy), (556, yy)], PAL["teal"][2], 4, 11))
        cv.add(P.pill(cv, 531, yy - 20, f, "teal", 12, 8, 20, 800))
        cv.add(P.lift(cv, 562, yy - 15, 62, 30, "sun", 9, 4, hl=False), cv.text(593, yy + 6, b_, 15, 800, fill=INK, mono=True))
        cv.add(cv.text(636, yy + 5, note, 11.5, 650, anchor="start", cls="il-ink2"))
    cv.add(P.badge(cv, 436, 270, 3))
    return figure(
        "data-types", cv, "The data types, and changing one into another",
        "The five basic data types, one card each. An integer is a whole number such as 42, written int in Python. A real number has a decimal "
        "point such as 3.14, written float. A Boolean has only two values, True and False, shown as a switch that is on and a switch that is off. "
        "A character is a single symbol such as the letter A, and a string is text inside quote marks. A phone number is stored as a string, "
        "because you never do arithmetic on it and because storing it as a number would drop the leading zero, turning 07700 into 7700. Casting "
        "changes a value from one type to another: int of the text 42 gives the number 42, str of the number 42 gives the text 42, and int of "
        "3.9 gives 3 because the decimal part is cut off rather than rounded.",
        ["Five data types: integer, real, Boolean, character and string.",
         "A phone number is a string: you never add them, and a number would lose the leading 0.",
         "Casting changes a value from one type to another: int(), str(), float().",
         ],
        "Choose the type from what you will do with the value, not from how it looks.")


# ---------------------------------------------------------- input and types

@illustration("input-types")
def _input():
    cv = Canvas(800, 500).backdrop()
    # the journey of one typed answer
    cv.add(P.band(cv, 24, 34, 752, 206, 20))
    cv.add(G.terminal(cv, 40, 54, 190, [("How old are you?", "#CFE8DC"), ("15", "#FFD479")], "console", 14))
    cv.add(cv.text(135, 160, "the user types 15", 12.5, 700, cls="il-ink2"))
    cv.add(P.arrow(cv, [(236, 98), (276, 98)], PAL["teal"][2], 5, 13))
    cv.add(G.var_box(cv, 282, 56, 118, 100, "age", '"15"', "str", "wood", "coral", 20))
    cv.add(cv.text(341, 178, "input() always gives text", 12.5, 700, cls="il-ink2"))
    cv.add(P.arrow(cv, [(406, 98), (440, 98)], PAL["teal"][2], 5, 13))
    cv.add(G.machine(cv, 446, 72, 100, 82, "int()", "teal"))
    cv.add(P.arrow(cv, [(574, 112), (606, 112)], PAL["teal"][2], 5, 13))
    cv.add(G.var_box(cv, 612, 56, 128, 100, "age", "15", "int", "wood", "sky", 30))
    cv.add(cv.text(676, 178, "now it can be added up", 12.5, 700, cls="il-ink2"))
    cv.add(P.pill(cv, 400, 214, "age + 1  gives  16", "sun", 15, 14, 28, 800))
    # the code and the trap
    cv.add(G.code(cv, 24, 262, 400, ['age = input("How old are you? ")', 'age = int(age)', 'print("Next year you will be", age + 1)'], "age.py", 13.5, hl=(1,)))
    cv.add(P.card(cv, 448, 262, 328, 218, 18, "The trap", "coral"))
    cv.add(G.code(cv, 464, 300, 296, ['"15" + "1"', '15 + 1'], None, 17, numbers=False, h=70))
    cv.add(cv.text(466, 387, "= \"151\"", 17, 800, anchor="start", cls="il-bad", mono=True), cv.text(466, 415, "= 16", 17, 800, anchor="start", cls="il-ink", mono=True))
    cv.add(cv.text(560, 387, "joined, not added", 13, 650, anchor="start", cls="il-ink2"), cv.text(560, 415, "arithmetic", 13, 650, anchor="start", cls="il-ink2"))
    cv.add(cv.text(612, 450, "forget int() and + joins text", 13, 750, cls="il-ink"))
    cv.add(P.badge(cv, 40, 54, 1), P.badge(cv, 290, 56, 2), P.badge(cv, 452, 72, 3), P.badge(cv, 466, 262, 4))
    return figure(
        "input-types", cv, "input() gives text, so convert it before doing sums",
        "The journey of one typed answer. The program asks How old are you, and the user types 15. The input function always gives back text, "
        "so the variable age holds the string 15 in quote marks, not the number. Passing it through int turns the text into the whole number 15, "
        "which can now be added to, so age plus one gives 16. The code on the bottom left does exactly that in three lines. The trap on the right "
        "shows what happens if the conversion is forgotten: adding the text 15 and the text 1 with a plus sign joins them into 151, whereas adding "
        "the numbers 15 and 1 gives 16.",
        ["The user types an answer at the console.",
         "input() always hands it back as text, a string, even when it looks like a number.",
         "int() turns the text into a whole number, so it can be used in sums.",
         "Skip the conversion and + joins text instead of adding: \"15\" + \"1\" is \"151\"."],
        "If the answer is going into a calculation, convert it as you take it in.")


# ---------------------------------------------------------- the constructs

@illustration("three-constructs")
def _constructs():
    cv = Canvas(800, 500).backdrop()
    cards = [("Sequence", "teal", 14), ("Selection", "coral", 277), ("Iteration", "plum", 540)]
    for t, col, x in cards:
        cv.add(P.card(cv, x, 40, 246, 440, 20, t, col))
    # sequence: steps in order
    for i, t in enumerate(("wake up", "brush teeth", "have breakfast")):
        yy = 84 + i * 62
        cv.add(P.lift(cv, 38, yy, 198, 40, "sky", 12, 5, hl=False))
        cv.add(cv.circle(58, yy + 20, 12, "#FFFFFF"), cv.text(58, yy + 25, str(i + 1), 14, 800, fill=INK))
        cv.add(cv.text(78, yy + 26, t, 15, 750, anchor="start", fill=INK))
        if i < 2:
            cv.add(P.arrow(cv, [(137, yy + 44), (137, yy + 66)], PAL["teal"][2], 4, 10))
    cv.add(G.code(cv, 28, 282, 218, ['print("Wake up")', 'print("Brush teeth")', 'print("Have breakfast")'], None, 12.5, numbers=False, h=96))
    cv.add(cv.text(137, 410, "every line runs once,", 13, 700, cls="il-ink"), cv.text(137, 429, "from the top down", 13, 700, cls="il-ink"))
    # selection: a fork
    cv.add(cv.poly([(400, 76), (456, 104), (400, 132), (344, 104)], cv.g("sun"), stroke=PAL["sun"][2], sw=2.4))
    cv.add(cv.text(400, 109, "raining?", 14, 800, fill=INK))
    cv.add(P.arrow(cv, [(352, 112), (322, 160)], PAL["ink"][1], 3.4, 10), P.arrow(cv, [(448, 112), (478, 160)], PAL["ink"][1], 3.4, 10))
    cv.add(cv.text(318, 140, "yes", 13, 800, cls="il-ink"), cv.text(486, 140, "no", 13, 800, cls="il-ink"))
    cv.add(P.lift(cv, 292, 164, 84, 76, "sky", 12, 5, hl=False), G.umbrella(cv, 334, 202, .9))
    cv.add(P.lift(cv, 424, 164, 84, 76, "paper", 12, 5, hl=False), G.sun(cv, 466, 202, 14))
    cv.add(cv.text(334, 262, "umbrella", 13, 700, cls="il-ink"), cv.text(466, 262, "sunglasses", 13, 700, cls="il-ink"))
    cv.add(G.code(cv, 291, 282, 218, ['if raining:', '    print("Umbrella")', 'else:', '    print("Sunglasses")'], None, 12.5, numbers=False, h=96 + 20))
    cv.add(cv.text(400, 430, "only one branch runs", 13, 700, cls="il-ink"), cv.text(400, 449, "depending on the answer", 13, 700, cls="il-ink"))
    # iteration: go round again
    cv.add(G.arrow_ring(cv, 663, 160, 58, -50, 270, PAL["plum"][1], 8, 18))
    cv.add(P.pixel_cat(cv, 633, 128, 60))
    cv.add(P.pill(cv, 663, 232, "5 times", "plum", 14, 12, 26, 800))
    cv.add(G.code(cv, 554, 282, 218, ['for i in range(5):', '    print("Star jump")'], None, 12.5, numbers=False, h=96 - 24))
    cv.add(cv.text(663, 388, "the block repeats,", 13, 700, cls="il-ink"), cv.text(663, 407, "then the program moves on", 13, 700, cls="il-ink"))
    cv.add(P.badge(cv, 30, 42, 1), P.badge(cv, 293, 42, 2), P.badge(cv, 556, 42, 3))
    return figure(
        "three-constructs", cv, "The three constructs: sequence, selection and iteration",
        "Every program is built from three constructs, one card each. Sequence is steps taken one after another in order: wake up, brush teeth, "
        "have breakfast, and in code the lines run once each from the top down. Selection is a choice: a decision diamond asks whether it is raining, "
        "and only one of the two branches is taken, an umbrella if yes and sunglasses if no, written in code as if and else. Iteration is repetition: "
        "a loop arrow carries Pixel round again, here five times, written as a for loop over range of five, and when the loop has finished the program "
        "carries on with the next line.",
        ["Sequence: instructions run in order, each one once, from the top down.",
         "Selection: a condition is tested and only one branch of the program runs.",
         "Iteration: a block is repeated, a set number of times or until a condition changes."],
        "Any algorithm, however big, is these three arranged in different ways.")


@illustration("selection-fork")
def _selection():
    cv = Canvas(800, 500).backdrop()
    lines = ['score = 65', 'if score >= 70:', '    print("A")', 'elif score >= 60:', '    print("B")', 'else:', '    print("C")']
    cv.add(G.code(cv, 24, 40, 360, lines, "grade.py", 15, hl=(3, 4)))
    # the ball falls through the tests, top to bottom
    cv.add(P.card(cv, 410, 34, 366, 446, 20, "Where does 65 go?", "teal"))
    cv.add(P.lift(cv, 456, 76, 58, 34, "sun", 17, 5, hl=False), cv.text(485, 100, "65", 18, 800, fill=INK, mono=True))
    gates = [("score >= 70", False, "A", 150), ("score >= 60", True, "B", 244), ("else", None, "C", 338)]
    cv.add(cv.line(485, 116, 485, 380, PAL["ink"][1], 3, op=.35, dash="2 6"))
    for cond, state, res, y in gates:
        dim = state is None
        cv.add(P.lift(cv, 430, y, 110, 48, "paper" if not dim else "slate", 12, 5, hl=False))
        cv.add(cv.text(485, y + 30, cond, 14, 800, fill=INK, mono=True))
        if state is True:
            cv.add(P.tick(cv, 556, y + 24, 12), cv.text(574, y + 29, "True", 13, 800, anchor="start", cls="il-ink"))
            cv.add(P.arrow(cv, [(610, y + 24), (644, y + 24)], PAL["green"][2], 5, 12))
            cv.add(P.lift(cv, 652, y + 6, 100, 44, "green", 12, 5), cv.text(702, y + 36, 'prints "B"', 14, 800, fill=P._on("green"), mono=True))
        elif state is False:
            cv.add(P.cross(cv, 556, y + 24, 12), cv.text(574, y + 29, "False", 13, 800, anchor="start", cls="il-ink"))
            cv.add(cv.text(660, y + 29, 'skip "A"', 13, 700, anchor="start", cls="il-ink2", mono=True))
        else:
            cv.add(cv.text(560, y + 29, "never reached", 13, 700, anchor="start", cls="il-ink2"))
    cv.add(P.arrow(cv, [(485, 116), (485, 144)], PAL["ink"][1], 4, 11), P.arrow(cv, [(485, 202), (485, 238)], PAL["ink"][1], 4, 11))
    cv.add(P.pill(cv, 593, 417, "first True branch wins", "sun", 14, 14, 28, 800))
    cv.add(P.card(cv, 24, 276, 360, 204, 18))
    cv.add(G.warning(cv, 58, 318, .8))
    cv.add(cv.text(88, 314, "Order matters", 16, 800, anchor="start", cls="il-ink"))
    cv.add(cv.text(88, 336, "Test the strictest condition first.", 13, 650, anchor="start", cls="il-ink2"))
    cv.add(G.code(cv, 40, 356, 328, ['if score >= 50:   # catches 90 too!', '    print("C")'], None, 12.5, numbers=False, h=64))
    cv.add(cv.text(204, 446, "a 90 would get the C: the first test is True", 12.5, 700, cls="il-ink"))
    cv.add(P.badge(cv, 40, 44, 1), P.badge(cv, 432, 34, 2), P.badge(cv, 428, 250, 3), P.badge(cv, 40, 278, 4))
    return figure(
        "selection-fork", cv, "if, elif and else: the first true branch wins",
        "A grading program with the score 65, and the route that 65 takes. The first test, score greater than or equal to 70, is False, so the "
        "block that prints A is skipped. The second test, score greater than or equal to 60, is True, so its block runs and prints B. Because "
        "a branch has been chosen, the else is never reached. Only one branch of an if, elif and else ever runs, and it is the first one whose "
        "condition is True. That is why the order of the tests matters: if a test for 50 or more had been written first, a score of 90 would "
        "satisfy it and receive the lowest grade, so the strictest condition must come first.",
        ["The code: if, elif and else test one condition after another.",
         "Follow the value 65 down: each test is True or False, in order.",
         "The first True test runs its block, and the rest are skipped.",
         "So test the strictest condition first, or an easy one will catch everything."],
        "Conditions are checked in order, and checking stops at the first one that is True.")


@illustration("loops-track")
def _loops():
    cv = Canvas(800, 500).backdrop()
    # for: count the laps
    cv.add(P.card(cv, 14, 34, 772, 226, 20, "for: repeat a set number of times", "teal"))
    cv.add(G.code(cv, 30, 64, 300, ['for lap in range(5):', '    print("Lap", lap)'], "for.py", 15, hl=(0,)))
    cv.add(G.terminal(cv, 30, 176, 300, ["Lap 0 Lap 1 Lap 2 Lap 3 Lap 4"], "output", 13))
    cv.add(cv.rect(356, 176, 408, 12, 6, "#B9C6CE"), cv.rect(356, 176, 408, 5, 2.5, "#fff", op=.5))
    for i in range(5):
        x = 392 + i * 84
        cv.add(G.flag(cv, x, 134, 1, "coral"), cv.text(x + 4, 212, str(i), 17, 800, cls="il-ink", mono=True))
    cv.add(P.pixel_cat(cv, 358, 104, 56))
    cv.add(cv.text(566, 244, "range(5) counts 0, 1, 2, 3, 4: five laps, never 5", 13, 700, cls="il-ink"))
    cv.add(P.pill(cv, 566, 82, "lap starts at 0, finishes at 4", "paper", 13, 12, 26, 700))
    # while: until the condition fails
    cv.add(P.card(cv, 14, 280, 772, 202, 20, "while: repeat until a condition is False", "coral"))
    cv.add(G.code(cv, 30, 318, 300, ['battery = 3', 'while battery > 0:', '    battery = battery - 1'], "while.py", 15, hl=(1,)))
    for i, lvl in enumerate((3, 2, 1, 0)):
        x = 372 + i * 96
        cv.add(P.lift(cv, x, 322, 70, 34, "paper", 8, 4, hl=False), cv.rect(x + 70, 332, 6, 14, 2, PAL["slate"][2]))
        for k in range(3):
            filled = k < lvl
            cv.add(cv.rect(x + 6 + k * 21, 328, 17, 22, 3, cv.g("green") if filled else "#DDE6EC"))
        cv.add(cv.text(x + 35, 380, "battery = %d" % lvl, 13, 800, cls="il-ink", mono=True))
        cv.add(cv.text(x + 35, 400, "%d > 0  %s" % (lvl, "True" if lvl else "False"), 12.5, 700, cls="il-ok" if lvl else "il-bad", mono=True))
        if i < 3:
            cv.add(P.arrow(cv, [(x + 82, 339), (x + 94, 339)], PAL["ink"][1], 3, 8))
    cv.add(P.cross(cv, 756, 340, 11), cv.text(756, 372, "stops", 13, 800, cls="il-ink"))
    cv.add(G.warning(cv, 388, 448, .62), cv.text(414, 453, "if battery never changed, the loop would never stop", 12.5, 700, anchor="start", cls="il-ink"))
    cv.add(P.badge(cv, 30, 36, 1), P.badge(cv, 30, 282, 2))
    return figure(
        "loops-track", cv, "for loops count; while loops wait for a condition",
        "Two kinds of loop. A for loop repeats a set number of times. The code for lap in range of five prints Lap and the lap number, and the "
        "picture shows it as a running track with five flags numbered 0 to 4: range of five counts from 0 up to 4, so there are five laps and "
        "the value 5 is never reached. A while loop repeats until a condition becomes False. Starting with battery equal to 3, the loop checks "
        "battery greater than 0, which is True, so it takes one off the battery and goes round again, checking before every go. At battery 0 "
        "the condition is False and the loop stops. If nothing inside the loop ever changes the battery, the condition would stay True for "
        "ever, which is an infinite loop.",
        ["for repeats a set number of times. range(5) gives 0, 1, 2, 3, 4: five laps.",
         "while repeats until its condition is False, checked before every go round.",
         ],
        "Use for when you know how many times. Use while when you only know when to stop.")


@illustration("operators")
def _operators():
    cv = Canvas(800, 500).backdrop()
    ops = [("+", "add", "7 + 2", "9", "sky"), ("-", "subtract", "7 - 2", "5", "teal"), ("*", "multiply", "7 * 2", "14", "mint"),
           ("/", "divide", "7 / 2", "3.5", "sun"), ("//", "DIV", "7 // 2", "3", "coral"), ("%", "MOD", "7 % 2", "1", "plum"), ("**", "power", "2 ** 3", "8", "lilac")]
    for i, (sym, name, ex, res, col) in enumerate(ops):
        x = 24 + i * 108
        cv.add(P.lift(cv, x, 40, 100, 140, col, 16, 6))
        tc = P._on(col)
        cv.add(cv.text(x + 50, 92, sym, 34, 800, fill=tc, mono=True), cv.text(x + 50, 118, name, 14, 800, fill=tc))
        cv.add(cv.rect(x + 10, 130, 80, 40, 9, "#FFFFFF"), cv.text(x + 50, 146, ex, 12.5, 700, fill=INK, mono=True), cv.text(x + 50, 163, "= " + res, 14, 800, fill=INK, mono=True))
    cv.add(P.badge(cv, 36, 42, 1))
    # DIV and MOD: sharing seven cookies between two people
    cv.add(P.card(cv, 24, 206, 420, 274, 18, "DIV and MOD: 7 cookies, 2 people", "coral"))
    cv.add(P.person(cv, 52, 250, .5, "tan", "black", "teal", "bun"), P.person(cv, 250, 250, .5, "light", "brown", "sun", "short"))
    for px in (108, 306):
        cv.add(G.plate_flat(cv, px, 322, 42))
        for k in range(3):
            cv.add(G.cookie(cv, px - 18 + k * 18, 318 + (k % 2) * 3, 8))
    cv.add(G.plate_flat(cv, 207, 392, 24), G.cookie(cv, 207, 389, 8))
    cv.add(cv.text(108, 358, "3 each", 14, 800, cls="il-ink"), cv.text(306, 358, "3 each", 14, 800, cls="il-ink"))
    cv.add(cv.text(207, 424, "1 left over", 13, 800, cls="il-ink"))
    cv.add(P.pill(cv, 130, 454, "7 // 2 = 3  (DIV)", "coral", 13, 12, 26, 800), P.pill(cv, 322, 454, "7 % 2 = 1  (MOD)", "plum", 13, 12, 26, 800))
    cv.add(P.badge(cv, 40, 208, 2))
    # comparing, and the = trap
    cv.add(P.card(cv, 468, 206, 308, 274, 18, "Comparing: True or False", "teal"))
    cmp_ = [("5 == 5", "True"), ("5 != 5", "False"), ("5 >= 6", "False"), ("5 < 6", "True")]
    for i, (e, r) in enumerate(cmp_):
        y = 252 + i * 38
        cv.add(cv.text(500, y + 6, e, 16, 800, anchor="start", cls="il-ink", mono=True))
        cv.add(P.tick(cv, 624, y, 11) if r == "True" else P.cross(cv, 624, y, 11), cv.text(644, y + 5, r, 14, 800, anchor="start", cls="il-ink"))
    cv.add(P.lift(cv, 486, 410, 272, 52, "sun", 12, 5, hl=False))
    cv.add(cv.text(622, 432, "=  stores a value", 14, 800, fill=INK, mono=True), cv.text(622, 452, "== asks \"are they equal?\"", 13, 800, fill=INK, mono=True))
    cv.add(P.badge(cv, 484, 208, 3), P.badge(cv, 490, 410, 4))
    return figure(
        "operators", cv, "Arithmetic and comparison operators",
        "The arithmetic operators as seven cards: plus, minus, multiply, divide, DIV, MOD and power, each with a worked example. Seven divided "
        "by two is 3.5. DIV gives the whole number of times it goes in, so 7 DIV 2 is 3, written with a double slash in Python, and MOD gives "
        "what is left over, so 7 MOD 2 is 1, written with a percent sign. A picture shows it as seven cookies shared between two people: "
        "three each, and one left over. Below, the comparison operators give True or False: 5 equals 5 is True, 5 is not equal to 5 is False, "
        "5 greater than or equal to 6 is False and 5 less than 6 is True. A warning shows the commonest slip: a single equals sign stores a "
        "value, while a double equals sign asks whether two values are equal.",
        ["Arithmetic: + - * / then DIV, MOD and power.",
         "DIV is how many whole times it goes in. MOD is what is left over.",
         "Comparisons ask a question, and the answer is always True or False.",
         "= stores a value. == asks whether two values are equal."],
        "MOD is the clock operator: it is what is left when you have gone round as many times as you can.")


# ---------------------------------------------------------- strings, lists

@illustration("strings-tiles")
def _strings():
    cv = Canvas(800, 500).backdrop()
    word = "Computer"
    x0, pitch, tw_ = 110, 80, 70
    cv.add(P.band(cv, 24, 34, 752, 218, 20))
    cv.add(cv.text(100, 70, "index", 13, 700, anchor="end", cls="il-ink2"), cv.text(100, 188, "from the end", 13, 700, anchor="end", cls="il-ink2"))
    for i, ch in enumerate(word):
        x = x0 + i * pitch
        col = "sun" if i == 7 else "sky"
        cv.add(P.lift(cv, x, 84, tw_, 72, col, 12, 6, hl=False), cv.text(x + tw_ / 2, 131, ch, 36, 800, fill=INK, mono=True))
        cv.add(cv.text(x + tw_ / 2, 74, str(i), 16, 800, cls="il-ink", mono=True), cv.text(x + tw_ / 2, 188, str(i - 8), 16, 800, cls="il-ink2", mono=True))
    # slices
    def brace(a, b, col, label, res, cx):
        xa, xb = x0 + a * pitch, x0 + b * pitch - 10
        cv.add(cv.path("M%d 202 v8 H%d v-8" % (xa, xb), stroke=PAL[col][1], sw=3.5))
        cv.add(P.pill(cv, cx, 232, "%s  =  %s" % (label, res), col, 13.5, 12, 26, 800))
    brace(0, 3, "teal", "word[0:3]", '"Com"', 225)
    brace(3, 8, "coral", "word[3:]", '"puter"', 480)
    cv.add(P.pill(cv, 705, 232, "word[-1] = \"r\"", "sun", 13.5, 12, 26, 800))
    cv.add(P.badge(cv, 40, 86, 1), P.badge(cv, 40, 214, 2), P.badge(cv, 770, 214, 3))
    # what you can do with a string
    cards = [('len(word)', '8', "how many characters"), ('word.upper()', '"COMPUTER"', "a new string in capitals"),
             ('word.find("p")', '3', "index of the first match"), ('word + "s"', '"Computers"', "+ joins two strings")]
    for i, (expr, res, why) in enumerate(cards):
        x = 24 + i * 190
        cv.add(P.card(cv, x, 280, 178, 200, 18))
        cv.add(cv.text(x + 89, 320, expr, 14, 800, cls="il-ink", mono=True))
        cv.add(P.arrow(cv, [(x + 89, 332), (x + 89, 358)], PAL["teal"][2], 4, 10))
        cv.add(P.lift(cv, x + 14, 364, 150, 44, "paper", 10, 5, hl=False), cv.text(x + 89, 393, res, 17 if len(res) < 10 else 14.5, 800, fill=INK, mono=True))
        cv.add(cv.text(x + 89, 440, why, 12.5, 650, cls="il-ink2"))
    cv.add(P.badge(cv, 40, 282, 4))
    return figure(
        "strings-tiles", cv, "A string is a row of characters, each with an index",
        "The word Computer drawn as eight letter tiles. Above each tile is its index, counting from 0 at the first letter to 7 at the last, and "
        "below it is the negative index, counting back from the end, from minus 8 to minus 1. A slice takes part of the string: word, bracket, 0, "
        "colon, 3 gives Com, which runs from index 0 up to but not including index 3, and word, bracket, 3, colon gives puter, from index 3 to the "
        "end. word minus one is the last character, r. Below, four things you can do with a string: len gives the number of characters, which is 8; "
        "upper gives a new string in capitals; find gives the index of the first match, here 3 for the letter p; and a plus sign joins two strings "
        "together. A string is never changed in place: each of these gives back a new string.",
        ["Every character has an index. The first is 0, and negative indexes count back from the end.",
         "A slice [a:b] runs from index a up to, but not including, b. Leave b out to go to the end.",
         "[-1] is the last character.",
         "Functions and methods build and search strings, and each one gives back a new string."],
        "In exam pseudocode the same idea is written as substring: check your board's command set for the exact form.")


@illustration("lists-lockers")
def _lists():
    cv = Canvas(800, 500).backdrop()
    cv.add(G.code(cv, 24, 40, 420, ['scores = [72, 85, 90, 64, 78]', 'scores.append(88)', 'scores[1] = 99', 'print(scores[2], len(scores))'], "lists.py", 15, bars={1: "#62CFA3", 2: "#FFCC4A", 3: "#66B8EC"}))
    cv.add(G.terminal(cv, 470, 40, 306, ["90 6"], "output", 15))
    cv.add(cv.text(623, 130, "the item at index 2, then the length", 12.5, 700, cls="il-ink2"))
    cv.add(P.band(cv, 24, 200, 752, 270, 20))
    vals = [72, 99, 90, 64, 78, 88]
    out, xs = G.lockers(cv, 53, 262, 6, 104, 108, 14, vals, 0, "sky", None, {1: "sun", 5: "mint"})
    cv.add(out)
    cv.add(P.pill(cv, xs[5], 238, "append", "mint", 13, 10, 24, 800), P.pill(cv, xs[1], 238, "changed", "sun", 13, 10, 24, 800))
    cv.add(P.arrow(cv, [(xs[2], 236), (xs[2], 258)], PAL["ink"][1], 4, 10))
    cv.add(P.pill(cv, xs[2], 222, "scores[2]", "paper", 13.5, 12, 26, 800))
    cv.add(cv.path("M%d 416 v8 H%d v-8" % (xs[0] - 40, xs[5] + 40), stroke=PAL["ink"][1], sw=3, op=.6))
    cv.add(P.pill(cv, 400, 446, "len(scores) is 6, so the last index is 5", "paper", 14, 14, 28, 750))
    cv.add(P.badge(cv, 40, 44, 1), P.badge(cv, xs[5] + 44, 262, 2), P.badge(cv, xs[1] - 44, 262, 3), P.badge(cv, xs[2] + 54, 226, 4))
    return figure(
        "lists-lockers", cv, "A list is a row of numbered lockers",
        "A list drawn as a row of numbered lockers, with the code that changes it. The list scores starts with five values, 72, 85, 90, 64 and 78, "
        "in lockers numbered from 0. The call append of 88 adds a new locker on the end, so the list now has six items. The assignment scores, "
        "bracket, 1, bracket, equals 99 replaces what was in locker 1, the 85, with 99. Reading scores bracket 2 opens locker 2 and finds 90, and "
        "len of scores is 6, so the last index is 5, one less than the length. The program prints 90 and 6.",
        ["The list holds its items in order, and the first locker is number 0.",
         "append() puts a new item on the end, so the list grows.",
         "Assign to an index to replace what is there. The old value is gone.",
         "scores[2] opens locker 2. len(scores) counts the lockers, so the last index is one less."],
        "Index from 0, and remember the last index is len minus 1.")


@illustration("dictionary-drawers")
def _dict():
    cv = Canvas(800, 500).backdrop()
    code = ['student = {"name": "Asha", "age": 15}', 'student["form"] = "10B"', 'print(student["age"])', 'print("form" in student)']
    cv.add(G.code(cv, 24, 40, 420, code, "dict.py", 14, bars={1: "#62CFA3", 2: "#66B8EC"}))
    cv.add(G.terminal(cv, 24, 196, 420, ["15", "True"], "output", 14))
    cv.add(P.card(cv, 24, 304, 420, 176, 18, "List or dictionary?", "teal"))
    cv.add(cv.text(124, 356, "list", 17, 800, cls="il-ink", mono=True), cv.text(124, 380, "find by position", 13, 700, cls="il-ink2"), cv.text(124, 404, "scores[2]", 15, 800, cls="il-ink", mono=True))
    cv.add(cv.text(344, 356, "dictionary", 17, 800, cls="il-ink", mono=True), cv.text(344, 380, "find by key", 13, 700, cls="il-ink2"), cv.text(344, 404, 'student["age"]', 15, 800, cls="il-ink", mono=True))
    cv.add(cv.line(234, 340, 234, 420, "var(--il-line)", 2))
    cv.add(cv.text(234, 450, "a key is a label you choose, so the order does not matter", 12.5, 700, cls="il-ink"))
    # the cabinet
    cv.add(cv.shadow(610, 466, 150, 9, .25))
    cv.add(P.lift(cv, 470, 40, 300, 416, "metal", 18, 10, hl=False))
    rows = [("name", '"Asha"', "coral"), ("age", "15", "sky"), ("form", '"10B"', "mint")]
    for i, (k, v, col) in enumerate(rows):
        y = 62 + i * 96
        cv.add(P.lift(cv, 488, y, 264, 84, "slate", 12, 5, hl=False))
        cv.add(cv.rect(502, y + 14, 90, 28, 6, "#FFFFFF"), cv.rect(502, y + 14, 90, 28, 6, "none", stroke=PAL[col][2], sw=2))
        cv.add(cv.text(547, y + 34, k, 15, 800, fill=INK, mono=True))
        cv.add(cv.rect(618, y + 52, 52, 8, 4, PAL["slate"][2]))
        cv.add(P.lift(cv, 614, y + 14, 122, 36, "paper", 9, 4, hl=False), cv.text(675, y + 38, v, 16, 800, fill=INK, mono=True))
    y = 62 + 3 * 96
    cv.add(P.lift(cv, 488, y, 264, 84, "slate", 12, 5, hl=False))
    cv.add(cv.rect(502, y + 14, 90, 28, 6, "#FFFFFF", op=.8), cv.rect(502, y + 14, 90, 28, 6, "none", stroke=PAL["sun"][2], sw=2, dash="4 4"))
    cv.add(cv.text(547, y + 34, "club", 15, 800, fill="#455C69", mono=True), cv.text(675, y + 38, "not here", 14, 700, fill="#455C69", mono=True))
    cv.add(P.badge(cv, 486, 62, 1), P.badge(cv, 486, 158, 2), P.badge(cv, 486, 254, 3))
    return figure(
        "dictionary-drawers", cv, "A dictionary is a cabinet of labelled drawers",
        "A Python dictionary drawn as a filing cabinet. Each drawer has a label, which is the key, and holds one value: the drawer labelled name "
        "holds Asha, the drawer labelled age holds 15, and the drawer labelled form, added by the second line of code, holds 10B. To find a value "
        "you ask for it by key, so student with the key age gives 15, and the test form in student is True because a drawer with that label exists. "
        "A fourth drawer labelled club is shown dashed because it has not been added: asking for a key that is not there is an error. A list is "
        "found by position, scores at index 2, but a dictionary is found by key, student at key age, and the order of the drawers does not matter.",
        ["Each drawer has a key for a label and one value inside it.",
         "Assigning to a new key adds a drawer, here form: \"10B\".",
         "Ask for a value by its key, and in tests whether a key exists.",
         ],
        "Use a list when position matters and a dictionary when a name does.")


@illustration("function-machine")
def _function():
    cv = Canvas(800, 500).backdrop()
    cv.add(G.code(cv, 24, 40, 330, ['def area(w, h):', '    return w * h', '', 'x = area(3, 4)', 'print(x)'], "area.py", 15, hl=(3,)))
    cv.add(G.terminal(cv, 24, 234, 330, ["12"], "output", 15))
    # the machine
    cv.add(P.card(cv, 380, 34, 396, 262, 20, "A function is a machine", "teal"))
    cv.add(G.machine(cv, 470, 182, 170, 96, "area(w, h)", "teal"))
    cv.add(P.lift(cv, 462, 90, 44, 36, "sky", 10, 4, hl=False), cv.text(484, 115, "3", 20, 800, fill=INK, mono=True))
    cv.add(P.lift(cv, 560, 90, 44, 36, "sun", 10, 4, hl=False), cv.text(582, 115, "4", 20, 800, fill=INK, mono=True))
    cv.add(P.arrow(cv, [(484, 134), (508, 156)], PAL["ink"][1], 3.4, 10), P.arrow(cv, [(582, 134), (572, 156)], PAL["ink"][1], 3.4, 10))
    cv.add(P.pill(cv, 533, 76, "arguments in", "paper", 12.5, 10, 22, 750))
    cv.add(P.lift(cv, 700, 238, 56, 38, "green", 10, 4, hl=False), cv.text(728, 264, "12", 20, 800, fill=P._on("green"), mono=True))
    cv.add(P.pill(cv, 700, 286, "returned", "paper", 12.5, 10, 22, 750))
    cv.add(cv.text(396, 196, "w and h:", 12.5, 700, anchor="start", cls="il-ink2"), cv.text(396, 212, "parameters", 12.5, 700, anchor="start", cls="il-ink2"))
    # procedure or function
    cv.add(P.card(cv, 380, 318, 188, 162, 18, "Procedure", "plum"))
    cv.add(G.code(cv, 392, 352, 164, ['def hello():', '    print("Hi")'], None, 12.5, numbers=False, h=70))
    cv.add(cv.text(474, 446, "does a job, gives", 12.5, 700, cls="il-ink"), cv.text(474, 464, "nothing back", 12.5, 700, cls="il-ink"))
    cv.add(P.card(cv, 588, 318, 188, 162, 18, "Function", "coral"))
    cv.add(G.code(cv, 600, 352, 164, ['def double(n):', '    return n * 2'], None, 12.5, numbers=False, h=70))
    cv.add(cv.text(682, 446, "hands a value back", 12.5, 700, cls="il-ink"), cv.text(682, 464, "with return", 12.5, 700, cls="il-ink"))
    cv.add(P.badge(cv, 40, 42, 1), P.badge(cv, 396, 88, 2), P.badge(cv, 684, 250, 3), P.badge(cv, 396, 320, 4))
    return figure(
        "function-machine", cv, "A function takes values in and hands a value back",
        "A function drawn as a machine. The code defines area with two parameters, w and h, and returns w times h. The line x equals area of 3, 4 "
        "calls it: the two arguments, 3 and 4, drop into the machine through the hopper, and the result, 12, comes out of the chute and is stored in "
        "x, so print of x shows 12. Parameters are the names the function uses for what it is given, and arguments are the actual values supplied "
        "when it is called. Below, a procedure and a function are compared: a procedure does a job, such as printing a greeting, and gives nothing "
        "back, while a function hands a value back to the caller with return.",
        ["Define it once with def, naming the parameters it will be given.",
         "Call it with arguments. They fill the parameters, w = 3 and h = 4.",
         "return hands the result back to the line that called it.",
         "A procedure does a job. A function also gives a value back."],
        "Parameters are the names in the definition. Arguments are the values in the call.")


# ------------------------------------------------- scope, files and errors

@illustration("scope-rooms")
def _scope():
    cv = Canvas(800, 500).backdrop()
    cv.add(P.card(cv, 24, 34, 406, 446, 20, "The program: global scope", "teal"))
    # the hallway: a variable everyone can see
    cv.add(cv.rect(44, 78, 366, 92, 14, "var(--il-band)"))
    cv.add(cv.rect(222, 96, 4, 20, 2, PAL["wood"][2]))
    cv.add(P.lift(cv, 142, 86, 160, 44, "sun", 10, 5, hl=False), cv.text(222, 116, "score = 10", 19, 800, fill=INK, mono=True))
    cv.add(cv.text(222, 154, "global: every function can read it", 12.5, 700, cls="il-ink2"))
    # two rooms
    for x, name, loc, col in ((44, "bonus()", "extra = 5", "coral"), (238, "reset()", "temp = 0", "sky")):
        cv.add(P.lift(cv, x, 206, 172, 168, col, 16, 8, hl=False))
        cv.add(cv.rect(x + 12, 222, 148, 140, 10, "#FFFFFF", op=.9))
        cv.add(P.pill(cv, x + 86, 206, name, col, 14, 12, 26, 800))
        cv.add(P.lift(cv, x + 26, 262, 120, 44, "paper", 9, 4, hl=False), cv.text(x + 86, 291, loc, 16, 800, fill=INK, mono=True))
        cv.add(cv.text(x + 86, 334, "local: only in", 12.5, 700, fill="#4A6470"), cv.text(x + 86, 350, "this room", 12.5, 700, fill="#4A6470"))
    cv.add(P.curve_arrow(cv, (130, 204), (130, 186), (160, 176), (170, 168), PAL["teal"][2], 4, 11))
    cv.add(P.curve_arrow(cv, (324, 204), (324, 186), (290, 176), (278, 168), PAL["teal"][2], 4, 11))
    # outside the house
    cv.add(P.person(cv, 52, 392, .5, "brown", "black", "plum", "short", mood="worry"))
    cv.add(G.bubble(cv, 126, 398, 180, 40, ["print(extra)"], (-40, 24), 15))
    cv.add(P.cross(cv, 330, 420, 14), cv.text(350, 425, "NameError", 14, 800, anchor="start", cls="il-bad", mono=True))
    cv.add(cv.text(132, 466, "the room's variables are not visible from outside", 12.5, 700, anchor="start", cls="il-ink2"))
    # the code
    code = ['score = 10          # global', '', 'def bonus():', '    extra = 5       # local', '    print(score + extra)', '', 'bonus()             # 15', 'print(extra)        # error']
    cv.add(G.code(cv, 452, 40, 324, code, "scope.py", 12.5, hl=(3,)))
    cv.add(G.terminal(cv, 452, 290, 324, ["15", ("NameError: name 'extra' is not defined", "#FF9A91")], "output", 12))
    cv.add(P.card(cv, 452, 388, 324, 92, 16))
    for i, t in enumerate(("a function can read a global variable", "a local variable dies when the function ends")):
        cv.add(P.tick(cv, 474, 414 + i * 30, 9), cv.text(492, 419 + i * 30, t, 12.5, 700, anchor="start", cls="il-ink"))
    cv.add(P.badge(cv, 44, 36, 1), P.badge(cv, 60, 206, 2), P.badge(cv, 126, 398, 3))
    return figure(
        "scope-rooms", cv, "Local and global variables as the rooms of a house",
        "Scope shown as a house. The whole program is the house, and the variable score equals 10, declared in the hallway, is global: every room, "
        "which is to say every function, can read it. Each function is a room with its own local variables on the wall: bonus has extra equals 5 and "
        "reset has temp equals 0. A local variable exists only inside its own room and is gone when the function ends. The code on the right "
        "defines bonus, which prints score plus extra, giving 15, and then tries to print extra from outside, which fails with a NameError because "
        "extra is not visible out there. In the picture a person standing outside the house asks for extra and is refused.",
        ["The program is the house. A variable made in the hallway is global, and any function can read it.",
         "Each function is a room. Variables made inside it are local and live only in that room.",
         "Outside code cannot see a room's local variables: asking for one gives a NameError.",
         ],
        "Make variables local by default. Reach for a global only when many functions truly share it.")


@illustration("files-flow")
def _files():
    cv = Canvas(800, 500).backdrop()
    modes = [('"r"', "read", "teal", 14), ('"w"', "write", "coral", 277), ('"a"', "append", "mint", 540)]
    def sheet(x, y, rows, new=None, w=112):
        out = cv.rect(x, y + 3, w, 14 + 20 * max(1, len(rows)) + 8, 6, "#10303A", op=.12) + cv.rect(x, y, w, 14 + 20 * max(1, len(rows)) + 8, 6, "#FFFFFF")
        out += cv.poly([(x + w - 14, y), (x + w, y + 14), (x + w - 14, y + 14)], PAL["paper"][2])
        for i, r in enumerate(rows):
            hot = (new is not None and i == new)
            if hot:
                out += cv.rect(x + 4, y + 17 + i * 20, w - 8, 19, 4, "#C8F0DA")
            out += cv.text(x + 10, y + 31 + i * 20, r, 13, 800 if hot else 600, anchor="start", fill=INK, mono=True)
        return out
    for t, name, col, x in modes:
        cv.add(P.card(cv, x, 34, 246, 272, 20, "%s  %s" % (t, name), col))
        cv.add(cv.text(x + 123, 82, "before", 12, 700, cls="il-ink2"))
        cv.add(sheet(x + 67, 90, ["Asha,42", "Tom,37"]))
        cv.add(P.arrow(cv, [(x + 123, 152), (x + 123, 172)], PAL[col][2], 4, 10))
    # read: the file is only looked at
    cv.add(P.lift(cv, 34 + 56, 178, 134, 52, "dark", 10, 4, hl=False), cv.text(34 + 123, 200, "program", 13, 800, fill="#EEF4F6"), cv.text(34 + 123, 218, "reads each line", 11.5, 650, fill="#EEF4F6"))
    cv.add(cv.text(137, 276, "the file is not changed", 13, 700, cls="il-ink"), cv.text(137, 295, "error if it does not exist", 12.5, 650, cls="il-ink2"))
    # write: starts again
    cv.add(sheet(277 + 67, 178, ["Tia,51"], 0))
    cv.add(G.warning(cv, 277 + 200, 206, .6))
    cv.add(cv.text(400, 276, "erases what was there", 13, 800, cls="il-bad"), cv.text(400, 295, "creates the file if missing", 12.5, 650, cls="il-ink2"))
    # append: adds to the end
    cv.add(sheet(540 + 67, 178, ["Asha,42", "Tom,37", "Tia,51"], 2))
    cv.add(cv.text(663, 276, "adds to the end", 13, 800, cls="il-ink"), cv.text(663, 295, "keeps what was there", 12.5, 650, cls="il-ink2"))
    # the safe way to write the code
    cv.add(G.code(cv, 24, 330, 440, ['with open("scores.txt", "a") as f:', '    f.write("Tia,51\\n")'], "save.py", 14, hl=(0,)))
    cv.add(P.card(cv, 488, 330, 288, 150, 16))
    notes = [("with closes the file for you", "teal"), ("\\n starts a new line", "sun"), ("a is safer than w for adding", "mint")]
    for i, (t, col) in enumerate(notes):
        cv.add(P.tick(cv, 512, 366 + i * 38, 10), cv.text(530, 371 + i * 38, t, 12.5, 700, anchor="start", cls="il-ink"))
    cv.add(cv.text(244, 470, "always close a file, or the last lines may never reach the disk", 12.5, 700, cls="il-ink2"))
    cv.add(P.badge(cv, 30, 36, 1), P.badge(cv, 293, 36, 2), P.badge(cv, 556, 36, 3), P.badge(cv, 40, 332, 4))
    return figure(
        "files-flow", cv, "Reading, writing and appending to a text file",
        "Three ways to open a text file, one card each. Opening with mode r reads the file: the program looks at the lines, nothing in the file "
        "changes, and it is an error if the file does not exist. Opening with mode w writes: it creates the file if it is missing, but if it exists "
        "everything in it is erased first, so a file that held two lines ends up holding only the new line. Opening with mode a appends: the new line "
        "is added to the end and the old lines are kept. The code below uses the with statement, which closes the file automatically, and writes "
        "the line Tia comma 51 followed by a newline character. Always close a file, because unwritten data may stay in a buffer and never reach the disk.",
        ["r reads. The file is only looked at, and it must already exist.",
         "w writes. Everything already in the file is erased first.",
         "a appends. New lines go on the end and the old ones are kept.",
         "with closes the file for you, and \\n ends a line."],
        "If you mean to add to a file, open it with a. Opening it with w by mistake wipes it.")


@illustration("error-types")
def _errors():
    cv = Canvas(800, 500).backdrop()
    kinds = [("Syntax error", "coral", 14, ['print("Hello"'], ["SyntaxError:", "'(' was never closed"], "a typo in the rules of the language", ["found before it runs,", "by the translator"]),
             ("Runtime error", "sun", 277, ['x = 10 / 0'], ["ZeroDivisionError:", "division by zero"], "the program starts, then crashes", ["found while it runs:", "it stops on that line"]),
             ("Logic error", "plum", 540, ['a, b = 4, 8', 'average = a + b / 2', 'print(average)'], ["8.0", "(should be 6.0)"], "runs fine, gives a wrong answer", ["found only by testing against", "the answer you expected"])]
    for title, col, x, snippet, out, what, found in kinds:
        cv.add(P.card(cv, x, 34, 246, 446, 20, title, col))
        cv.add(G.bug(cv, x + 123, 106, 1.7, "red" if col != "plum" else "plum"))
        cv.add(cv.text(x + 123, 166, what, 13, 700, cls="il-ink"))
        h = G.code_h(len(snippet), 13.5, None) + 6
        cv.add(G.code(cv, x + 14, 186, 218, snippet, None, 13.5, numbers=False, h=h))
        ty = 186 + h + 14
        cv.add(G.terminal(cv, x + 14, ty, 218, [(t, "#FF9A91" if col != "plum" else "#FFDA8A") for t in out], "result", 12.5))
        cv.add(P.pill(cv, x + 123, 408, "found how?", col, 12.5, 10, 24, 800))
        for k, t in enumerate(found):
            cv.add(cv.text(x + 123, 438 + k * 18, t, 12.5, 700 if k == 0 else 650, cls="il-ink" if k == 0 else "il-ink2"))
    cv.add(P.badge(cv, 30, 36, 1), P.badge(cv, 293, 36, 2), P.badge(cv, 556, 36, 3))
    return figure(
        "error-types", cv, "The three kinds of error: syntax, runtime and logic",
        "The three kinds of programming error, one card each, each with its own bug. A syntax error breaks the rules of the language, like print "
        "with an opening bracket that is never closed. The translator cannot understand the line, reports a SyntaxError and the program will not "
        "start. A runtime error happens while the program is running: dividing 10 by 0 makes the program start and then crash on that line with a "
        "ZeroDivisionError. A logic error is the hardest to find because nothing crashes: the program average equals a plus b divided by 2 runs "
        "happily and prints 8.0, when the average of 4 and 8 is 6.0, because division is done before addition. Only testing against the answer "
        "you expected finds it.",
        ["Syntax error: the code breaks the rules of the language, so it will not run at all.",
         "Runtime error: the program starts, then crashes when it meets something it cannot do.",
         "Logic error: it runs without complaint but gives the wrong answer, so only testing finds it."],
        "A program that runs is not a program that is right. Test the answers, not only the absence of crashes.")


@illustration("try-except")
def _tryexcept():
    cv = Canvas(800, 500).backdrop()
    code = ['try:', '    n = int(input("Number: "))', '    print(100 / n)', 'except ValueError:', '    print("Numbers only")', 'except ZeroDivisionError:', '    print("Cannot divide by zero")']
    cv.add(G.code(cv, 24, 40, 430, code, "safe.py", 13.5, bars={0: "#66B8EC", 3: "#FFCC4A", 5: "#F77F72"}))
    # a safety net under the tightrope
    cv.add(P.band(cv, 24, 280, 430, 200, 18))
    cv.add(cv.rect(60, 330, 8, 100, 3, cv.g("wood", "deep")), cv.rect(410, 330, 8, 100, 3, cv.g("wood", "deep")))
    cv.add(cv.line(64, 334, 414, 334, "#4A5A64", 4))
    cv.add(cv.path("M64 392 Q239 470 414 392", stroke="#8FA3AE", sw=2.5))
    for k in range(0, 8):
        xx = 64 + k * 50
        cv.add(cv.line(xx, 392, xx, 392 + 38 * (1 - ((xx - 239) / 175) ** 2), "#8FA3AE", 1.6, op=.55))
    cv.add(P.pixel_cat(cv, 190, 276, 76))
    cv.add(P.pill(cv, 118, 306, "the try block", "sky", 13, 12, 24, 800))
    cv.add(P.pill(cv, 239, 452, "except catches the fall", "sun", 13, 12, 26, 800))
    # three runs
    cv.add(P.card(cv, 480, 40, 296, 440, 20, "Three runs", "teal"))
    runs = [('"abc"', "ValueError", "Numbers only", "yellow"), ('0', "ZeroDivisionError", "Cannot divide by zero", "coral"), ('4', "no error", "25.0", "green")]
    for i, (inp, err, outp, col) in enumerate(runs):
        y = 86 + i * 128
        cv.add(P.lift(cv, 498, y, 70, 38, "paper", 10, 4, hl=False), cv.text(533, y + 26, inp, 16, 800, fill=INK, mono=True))
        cv.add(P.arrow(cv, [(574, y + 19), (606, y + 19)], PAL["ink"][1], 3.4, 10))
        c2 = {"yellow": "sun", "coral": "coral", "green": "green"}[col]
        cv.add(P.pill(cv, 690, y + 19, err, c2, 12, 10, 26, 800))
        cv.add(P.arrow(cv, [(690, y + 36), (690, y + 60)], PAL["ink"][1], 3.4, 10))
        cv.add(P.lift(cv, 560, y + 64, 200, 36, "dark", 9, 4, hl=False), cv.text(660, y + 88, outp, 14, 800, fill="#E8F0F3", mono=True))
    cv.add(P.badge(cv, 434, 62, 1), P.badge(cv, 434, 154, 2), P.badge(cv, 434, 197, 3), P.badge(cv, 496, 42, 4))
    return figure(
        "try-except", cv, "try and except: catching an error instead of crashing",
        "Error handling drawn as a safety net under a tightrope. The risky code goes in a try block, shown as Pixel on the rope: it asks for a number "
        "and then divides 100 by it. If something goes wrong, the program does not crash: it falls into the net, which is the matching except block. "
        "There are three runs. If the user types the letters abc, int fails with a ValueError, the except ValueError block runs and prints Numbers "
        "only. If the user types 0, the division fails with a ZeroDivisionError and the program prints Cannot divide by zero. If the user types 4 "
        "nothing goes wrong, the except blocks are skipped and the program prints 25.0.",
        ["try holds the code that might fail.",
         "except ValueError catches a bad conversion, such as int(\"abc\").",
         "except ZeroDivisionError catches a division by zero.",
         "With no error, the except blocks are skipped and the program carries on."],
        "Catch the specific error you expect, and say what went wrong in plain words.")


# ----------------------------------------------- robust programs and testing

@illustration("validation-checks")
def _validation():
    cv = Canvas(800, 500).backdrop()
    checks = [("Presence", "something must be entered", ('""', "Asha"), "sky"), ("Type", "the right kind of data", ('"abc"', "15"), "teal"),
              ("Range", "between two limits (0 to 120)", ("200", "15"), "mint"), ("Length", "enough characters (8 or more)", ('"pass"', '"pass1234"'), "sun"),
              ("Format", "matches a pattern", ('"asha.com"', '"asha@mail.com"'), "coral"), ("Lookup", "one of an allowed list", ('"Funday"', '"Friday"'), "plum")]
    for i, (name, rule, (bad, good), col) in enumerate(checks):
        x, y = 24 + (i % 3) * 252, 34 + (i // 3) * 136
        cv.add(P.card(cv, x, y, 236, 122, 18, name, col))
        cv.add(cv.text(x + 118, y + 36, rule, 12.5, 700, cls="il-ink2"))
        cv.add(P.cross(cv, x + 22, y + 68, 10), cv.text(x + 40, y + 73, bad, 14.5, 800, anchor="start", cls="il-bad", mono=True))
        cv.add(P.tick(cv, x + 22, y + 98, 10), cv.text(x + 40, y + 103, good, 14.5, 800, anchor="start", cls="il-ok", mono=True))
    cv.add(P.badge(cv, 36, 36, 1))
    # what validation cannot do
    cv.add(P.card(cv, 24, 316, 372, 164, 18, "Valid is not the same as true", "coral"))
    cv.add(P.person(cv, 40, 354, .5, "brown", "black", "teal", "bun", mood="worry"))
    cv.add(cv.text(106, 372, "Age 15 mistyped as 51 is in range,", 12.5, 700, anchor="start", cls="il-ink"), cv.text(106, 390, "so every check passes and the", 12.5, 700, anchor="start", cls="il-ink"), cv.text(106, 408, "data is still wrong.", 12.5, 700, anchor="start", cls="il-ink"))
    cv.add(cv.text(210, 456, "validation checks it is sensible, not that it is true", 12.5, 700, cls="il-ink2"))
    cv.add(P.card(cv, 412, 316, 364, 164, 18, "Verification: typed twice", "teal"))
    cv.add(P.lift(cv, 430, 360, 150, 34, "paper", 9, 4, hl=False), cv.text(505, 383, "password", 13, 700, fill="#4A6470", mono=True), cv.text(440, 352, "enter it", 12.5, 700, anchor="start", cls="il-ink2"))
    cv.add(P.lift(cv, 430, 418, 150, 34, "paper", 9, 4, hl=False), cv.text(505, 441, "confirm", 13, 700, fill="#4A6470", mono=True), cv.text(440, 410, "and enter it again", 12.5, 700, anchor="start", cls="il-ink2"))
    cv.add(P.arrow(cv, [(590, 390), (620, 420)], PAL["teal"][2], 4, 10), P.arrow(cv, [(590, 440), (620, 428)], PAL["teal"][2], 4, 10))
    cv.add(P.lift(cv, 624, 400, 138, 44, "sun", 10, 5, hl=False), cv.text(693, 428, "do they match?", 13, 800, fill=INK))
    cv.add(P.badge(cv, 40, 318, 2), P.badge(cv, 428, 318, 3))
    return figure(
        "validation-checks", cv, "Validation checks, and what they cannot do",
        "Six validation checks, one card each, with a value that is rejected and a value that is accepted. A presence check makes sure something is "
        "entered, so an empty entry is rejected. A type check makes sure the data is the right kind, so the letters abc are rejected for an age. A "
        "range check keeps a number between limits, so an age of 200 is rejected. A length check makes sure there are enough characters, so pass is "
        "too short for a password of eight or more. A format check makes sure the data matches a pattern, so asha dot com is not an email address "
        "without an at sign. A lookup check makes sure the value is one of an allowed list, so Funday is not a day of the week. Two cards underneath "
        "separate validation from correctness: validation checks data is sensible, not that it is true, so an age of 15 mistyped as 51 passes a range "
        "check and is still wrong. Verification checks that data was entered as intended, for example by typing a password twice and comparing.",
        ["Validation checks: presence, type, range, length, format and lookup.",
         "Validation checks that data is sensible. It cannot know whether it is true.",
         "Verification asks the user again, for example with a confirm password box, to catch typing slips."],
        "Validate on the way in, and tell the user what is wrong, not just that something is.")


@illustration("authentication")
def _authentication():
    cv = Canvas(800, 500).backdrop()
    factors = [("Something you know", "sky", "password, PIN"), ("Something you have", "mint", "phone, bank card, key fob"), ("Something you are", "coral", "fingerprint, face")]
    for i, (t, col, ex) in enumerate(factors):
        x = 24 + i * 252
        cv.add(P.card(cv, x, 40, 236, 176, 18, t, col))
        if i == 0:
            cv.add(P.lift(cv, x + 38, 84, 160, 44, "paper", 12, 5, hl=False), cv.text(x + 118, 114, "• • • • • • • •", 18, 800, fill=INK))
        elif i == 1:
            cv.add(P.phone(cv, x + 90, 66, .86, cv.text(32, 52, "482 913", 10.5, 800, fill=INK, mono=True) + cv.text(32, 70, "code", 9, 700, fill="#4A6470")))
        else:
            cv.add(cv.circle(x + 118, 106, 34, "#FFFFFF"), G.fingerprint(cv, x + 118, 96, .9))
        cv.add(cv.text(x + 118, 198, ex, 13, 700, cls="il-ink"))
    cv.add(P.badge(cv, 36, 42, 1))
    # two factor login
    cv.add(P.card(cv, 24, 244, 456, 236, 18, "Two-factor login", "teal"))
    steps = [("username +", "password", "sky", 44), ("code sent to", "your phone", "mint", 190), ("access", "granted", "green", 336)]
    for i, (a_, b_, col, x) in enumerate(steps):
        cv.add(P.lift(cv, x, 296, 110, 74, col, 14, 6, hl=False))
        tc = P._on(col)
        cv.add(cv.text(x + 55, 326, a_, 13.5, 800, fill=tc), cv.text(x + 55, 346, b_, 13.5, 800, fill=tc))
        if i < 2:
            cv.add(P.arrow(cv, [(x + 118, 333), (x + 146, 333)], PAL["ink"][1], 4, 11))
    cv.add(P.pill(cv, 252, 410, "a stolen password alone is not enough", "sun", 13.5, 14, 28, 800))
    cv.add(cv.text(252, 456, "the second factor is something an attacker does not have", 12.5, 700, cls="il-ink2"))
    cv.add(P.badge(cv, 40, 246, 2))
    # stored as a hash
    cv.add(P.card(cv, 500, 244, 276, 236, 18, "Stored as a hash", "plum"))
    cv.add(P.lift(cv, 518, 290, 240, 36, "paper", 10, 4, hl=False), cv.text(638, 314, "password123", 15, 800, fill=INK, mono=True))
    cv.add(P.arrow(cv, [(638, 336), (638, 362)], PAL["plum"][2], 4, 10), P.gear(cv, 704, 350, 14, "slate"), cv.text(598, 352, "hash function", 12, 700, anchor="start", cls="il-ink2"))
    cv.add(G.code(cv, 518, 368, 240, ["5f4dcc3b5aa765d6..."], None, 12.5, numbers=False, h=42))
    cv.add(cv.text(638, 438, "the real password is never kept,", 12.5, 700, cls="il-ink"), cv.text(638, 456, "so a leak does not reveal it", 12.5, 700, cls="il-ink"))
    cv.add(P.badge(cv, 516, 246, 3))
    return figure(
        "authentication", cv, "Authentication: what you know, have and are, and how passwords are kept",
        "Authentication proves who someone is, using three kinds of evidence, one card each: something you know, such as a password or PIN; "
        "something you have, such as a phone showing a one time code, a bank card or a key fob; and something you are, such as a fingerprint or a "
        "face. Using two of them together, two factor authentication, is far stronger than one. The login flow shows it: the user enters a username "
        "and password, a code is sent to their phone, and only then is access granted, so a stolen password alone is not enough. Underneath, a "
        "password should never be stored as typed. The system keeps only a hash, the output of a one way function, so password123 is stored as a "
        "string of characters such as 5f4dcc3b and the real password is never kept. If the file is stolen, it does not reveal the passwords.",
        ["Three kinds of evidence: something you know, have or are.",
         "Two factors together are far stronger than one: a stolen password alone is not enough.",
         "Passwords should be stored as hashes, never as typed, so a leak does not reveal them."],
        "Strong authentication is layers. No single one of them is enough alone.")


@illustration("test-data")
def _testdata():
    cv = Canvas(800, 500).backdrop()
    cv.add(P.card(cv, 24, 34, 752, 200, 20, "Test data for: enter an age from 13 to 19", "teal"))
    x0, k = 64, 27.5
    X = lambda v: x0 + v * k
    cv.add(cv.rect(X(0), 120, X(12.5) - X(0), 22, 4, "#F6C7C2"), cv.rect(X(12.5), 120, X(19.5) - X(12.5), 22, 4, "#BDEBCF"), cv.rect(X(19.5), 120, X(26) - X(19.5), 22, 4, "#F6C7C2"))
    cv.add(cv.line(X(0), 131, X(26), 131, "#4A6470", 2.5))
    for v in range(0, 26, 1):
        if v % 13 in (0,) or v in (12, 13, 16, 19, 20):
            cv.add(cv.line(X(v), 126, X(v), 136, "#4A6470", 2), cv.text(X(v), 160, str(v), 13, 800, cls="il-ink", mono=True))
    cv.add(cv.text(X(6), 112, "invalid", 13, 800, cls="il-bad"), cv.text(X(16), 112, "valid", 13, 800, cls="il-ok"), cv.text(X(23), 112, "invalid", 13, 800, cls="il-bad"))
    # normal, boundary, erroneous
    cv.add(cv.circle(X(16), 131, 9, "#41B56D", stroke="#fff", sw=3))
    for v, ok in ((13, True), (19, True), (12, False), (20, False)):
        cv.add(cv.circle(X(v), 131, 9, "#FFCC4A", stroke="#fff", sw=3))
    cv.add(P.pill(cv, X(16), 80, "normal: 16", "green", 13, 12, 26, 800))
    cv.add(P.pill(cv, X(10), 80, "boundary: 12, 13", "sun", 13, 12, 26, 800), P.pill(cv, X(23), 80, "boundary: 19, 20", "sun", 13, 12, 26, 800))
    cv.add(cv.text(X(0) + 4, 190, "erroneous:", 13, 800, anchor="start", cls="il-ink"))
    for i, v in enumerate(('"abc"', "-5", "empty")):
        cv.add(P.pill(cv, 190 + i * 96, 186, v, "coral", 13, 12, 26, 800))
    cv.add(cv.text(560, 191, "the wrong type, or not a sensible value", 12.5, 650, anchor="start", cls="il-ink2"))
    cv.add(P.badge(cv, 40, 36, 1), P.badge(cv, X(16) + 56, 80, 2), P.badge(cv, 40, 186, 3))
    # a test plan, as the exam asks for it
    cv.add(P.card(cv, 24, 258, 752, 222, 20, "A test plan, with the result of each test", "coral"))
    heads = [("Test", 52), ("Data", 130), ("Type", 262), ("Expected", 392), ("Actual", 548), ("Pass?", 704)]
    cv.add(cv.rect(40, 292, 720, 28, 8, cv.g("coral")))
    for h_, xx in heads:
        cv.add(cv.text(xx, 311, h_, 13.5, 800, anchor="start", fill=P._on("coral")))
    rows = [("1", "16", "normal", "accepted", "accepted", True), ("2", "13", "boundary", "accepted", "accepted", True), ("3", "12", "boundary", "rejected", "rejected", True),
            ("4", '"abc"', "erroneous", "asks again", "crashes", False)]
    for i, r in enumerate(rows):
        y = 328 + i * 36
        cv.add(cv.rect(40, y, 720, 32, 7, "#FFFFFF" if r[5] else "#FFE3DD", stroke="#DCE6EC", sw=1))
        for (t, xx) in zip(r[:5], [52, 130, 262, 392, 548]):
            cv.add(cv.text(xx, y + 21, t, 13.5, 700, anchor="start", fill=INK, mono=(xx == 130)))
        cv.add(P.tick(cv, 716, y + 16, 10) if r[5] else P.cross(cv, 716, y + 16, 10))
    cv.add(P.badge(cv, 40, 260, 4))
    return figure(
        "test-data", cv, "Normal, boundary and erroneous test data",
        "Test data for a program that asks for an age from 13 to 19. A number line shows the valid range in green, from 13 to 19, and the invalid "
        "values in red either side. Normal data is a typical value inside the range, such as 16. Boundary data sits on the edge of what is allowed "
        "and just outside it: 13 and 19 are the two valid boundaries and 12 and 20 are the first invalid values either side. Erroneous data is the "
        "wrong type or not sensible at all, such as the text abc, a negative number or an empty entry. Beneath, a test plan lists each test with "
        "its data, type, expected result and actual result. The first three pass. The fourth, the text abc, was expected to make the program ask "
        "again but the program crashed, so it fails, and that points to a missing validation check.",
        ["Test data for an age from 13 to 19, on a number line.",
         "Normal data is typical and should be accepted.",
         "Boundary data sits on and just outside each edge, because that is where mistakes hide.",
         "A test plan records expected against actual. A failed test shows what to fix."],
        "Always test at the boundaries, on both sides of each one.")


@illustration("language-levels")
def _levels():
    cv = Canvas(800, 500).backdrop()
    rungs = [("High-level", "Python, Java, C#", ["English-like.", "One line, many instructions.", "Runs on any machine."], "sky"),
             ("Assembly language", "LDA 7, ADD 3, STA 9", ["Short codes, one per", "instruction: one line,", "one instruction. One CPU."], "mint"),
             ("Machine code", "10110001 00000111", ["Binary: the only thing", "a processor can run.", "Hard for people to read."], "plum")]
    for i, (t, ex, d, col) in enumerate(rungs):
        y = 50 + i * 142
        cv.add(P.lift(cv, 96, y, 416, 118, col, 18, 8))
        tc = P._on(col)
        cv.add(cv.text(120, y + 36, t, 22, 800, anchor="start", fill=tc))
        cv.add(cv.rect(120, y + 50, 146, 26, 7, "#FFFFFF", op=.92), cv.text(193, y + 69, ex, 11.5, 800, fill=INK, mono=True))
        for k, w_ in enumerate(d):
            cv.add(cv.text(282, y + 62 + k * 18, w_, 12.5, 650, anchor="start", fill=tc))
    cv.add(P.arrow(cv, [(44, 290), (44, 96)], PAL["teal"][2], 6, 15))
    cv.add(cv.text(44, 56, "easier", 13, 800, cls="il-ink"), cv.text(44, 74, "to write", 13, 800, cls="il-ink"))
    cv.add(P.arrow(cv, [(44, 326), (44, 420)], PAL["coral"][2], 6, 15))
    cv.add(cv.text(44, 446, "closer to", 13, 800, cls="il-ink"), cv.text(44, 464, "hardware", 13, 800, cls="il-ink"))
    # the same sum in all three
    cv.add(P.card(cv, 540, 40, 236, 440, 20, "The same sum", "teal"))
    cv.add(cv.text(658, 92, "total = a + b", 15, 800, cls="il-ink", mono=True))
    cv.add(cv.text(658, 112, "1 line of Python", 12.5, 650, cls="il-ink2"))
    cv.add(cv.line(560, 130, 756, 130, "var(--il-line)", 2))
    for i, t in enumerate(("LDA a", "ADD b", "STA total")):
        cv.add(cv.text(658, 168 + i * 24, t, 15, 800, cls="il-ink", mono=True))
    cv.add(cv.text(658, 252, "3 lines of assembly", 12.5, 650, cls="il-ink2"))
    cv.add(cv.line(560, 270, 756, 270, "var(--il-line)", 2))
    for i, t in enumerate(("1010 0001 0000 0101", "0001 1000 0000 0110", "1011 0001 0000 0111")):
        cv.add(cv.text(658, 306 + i * 24, t, 13, 800, cls="il-ink", mono=True))
    cv.add(cv.text(658, 392, "3 machine instructions", 12.5, 650, cls="il-ink2"))
    cv.add(P.pill(cv, 658, 436, "a translator turns the top", "sun", 12, 12, 24, 800), cv.text(658, 464, "one into the bottom one", 12.5, 700, cls="il-ink"))
    cv.add(P.badge(cv, 96, 50, 1), P.badge(cv, 96, 192, 2), P.badge(cv, 96, 334, 3), P.badge(cv, 556, 42, 4))
    return figure(
        "language-levels", cv, "High-level, assembly and machine code",
        "Three levels of programming language drawn as a ladder. At the top is high-level language, such as Python, Java or C sharp: it is "
        "English-like, one line becomes many machine instructions and it runs on any machine. Below it is assembly language, with short codes such "
        "as LDA, ADD and STA: one line is one instruction and it is tied to one type of processor. At the bottom is machine code, binary such as "
        "1011 0001, the only thing a processor can run, and very hard for people to read. A green arrow up the left side points towards easier to "
        "write, and a coral arrow down points towards closer to the hardware. The panel on the right shows the same sum, total equals a plus b: "
        "one line of Python, three lines of assembly, load a, add b, store total, and three binary machine instructions. A translator turns the "
        "top form into the bottom one.",
        ["High-level: English-like, portable, one line becomes many instructions.",
         "Assembly: one short code per instruction, tied to one processor.",
         "Machine code: binary, the only thing the processor runs.",
         "The same sum at each level. A translator turns the top into the bottom."],
        "High-level is for people to write. Machine code is for the processor to run. Translators connect them.")


@illustration("translators")
def _translators():
    cv = Canvas(800, 500).backdrop()
    cols = [("Compiler", "teal", 14), ("Interpreter", "coral", 277), ("Assembler", "plum", 540)]
    for t, col, x in cols:
        cv.add(P.card(cv, x, 34, 246, 446, 20, t, col))
    srcs = ["source code", "source code", "assembly code"]
    machines = [("compile", "all of it, once"), ("interpret", "one line at a time"), ("assemble", "one to one")]
    for i, (t, col, x) in enumerate(cols):
        cv.add(P.doc(cv, x + 95, 62, .9, lines=4, head=["teal", "coral", "plum"][i]))
        cv.add(cv.text(x + 123, 150, srcs[i], 12.5, 700, cls="il-ink2"))
        cv.add(P.arrow(cv, [(x + 123, 158), (x + 123, 182)], PAL[col][2], 4, 11))
        cv.add(P.lift(cv, x + 34, 186, 178, 62, col, 14, 6, hl=False))
        cv.add(P.gear(cv, x + 58, 217, 14, "metal"))
        tc = P._on(col)
        cv.add(cv.text(x + 134, 211, machines[i][0], 16, 800, fill=tc), cv.text(x + 134, 230, machines[i][1], 11.5, 650, fill=tc))
        cv.add(P.arrow(cv, [(x + 123, 256), (x + 123, 280)], PAL[col][2], 4, 11))
    # outputs
    cv.add(P.lift(cv, 14 + 70, 284, 106, 54, "paper", 12, 5, hl=False), cv.text(14 + 123, 308, "program.exe", 13, 800, fill=INK, mono=True), cv.text(14 + 123, 326, "machine code", 11.5, 650, fill="#4A6470"))
    for k in range(3):
        cv.add(P.lift(cv, 277 + 44, 284 + k * 26, 78, 22, "paper", 7, 3, hl=False), cv.text(277 + 83, 300 + k * 26, "line %d" % (k + 1), 11.5, 700, fill=INK, mono=True))
        cv.add(P.arrow(cv, [(277 + 126, 295 + k * 26), (277 + 152, 295 + k * 26)], PAL["coral"][2], 3, 8))
        cv.add(cv.rect(277 + 156, 284 + k * 26, 38, 22, 5, cv.g("dark", "deep")), cv.text(277 + 175, 299 + k * 26, "run", 11, 800, fill="#E8F0F3"))
    cv.add(P.lift(cv, 540 + 40, 284, 166, 54, "paper", 12, 5, hl=False), cv.text(540 + 123, 308, "10110001 00000111", 11.5, 800, fill=INK, mono=True), cv.text(540 + 123, 326, "machine code, one to one", 11.5, 650, fill="#4A6470"))
    facts = [["translates it all first", "then it runs fast, again and again", "source code stays private"],
             ["translates as it goes", "runs straight away, so easy to test", "stops at the first error"],
             ["one line is one instruction", "for low-level control of hardware", "output only fits one processor"]]
    for i, (t, col, x) in enumerate(cols):
        for k, f in enumerate(facts[i]):
            cv.add(P.tick(cv, x + 24, 382 + k * 34, 8), cv.text(x + 42, 387 + k * 34, f, 12, 650, anchor="start", cls="il-ink"))
    cv.add(P.badge(cv, 30, 36, 1), P.badge(cv, 293, 36, 2), P.badge(cv, 556, 36, 3))
    return figure(
        "translators", cv, "Compiler, interpreter and assembler",
        "Three translators, one card each. A compiler takes the source code and translates all of it at once into a separate executable file of "
        "machine code. The file can then be run again and again without the compiler, and it runs fast and keeps the source code private. An "
        "interpreter translates and runs the source code one line at a time, line 1 then line 2 then line 3, so it runs straight away, which makes "
        "it easy to test, but it stops at the first error and is slower because the translation happens every time. An assembler translates "
        "assembly language into machine code, with one line of assembly becoming one machine instruction, which gives low-level control of the "
        "hardware but produces code that only fits one type of processor.",
        ["Compiler: translates everything first, then the program runs fast and the source stays private.",
         "Interpreter: translates and runs one line at a time, so it is easy to test and stops at the first error.",
         "Assembler: turns assembly into machine code, one line for one instruction."],
        "Compiled code runs faster. Interpreted code is quicker to try out. Learn one point for each.")


@illustration("ide-tour")
def _ide():
    cv = Canvas(800, 500).backdrop()
    # the window
    cv.add(cv.rect(24, 38, 548, 446, 16, "#10303A", op=.18), cv.rect(24, 34, 548, 446, 16, "#EEF3F6"))
    cv.add(cv.rect(24, 34, 548, 34, 16, "#3C505B"), cv.rect(24, 52, 548, 16, 0, "#3C505B"))
    for i, c in enumerate(("#FF7B72", "#FFCB47", "#5BD58B")):
        cv.add(cv.circle(44 + i * 16, 51, 4.5, c))
    cv.add(cv.text(298, 56, "my_project — IDE", 12, 700, fill="#D7E3E8", mono=True))
    # toolbar
    cv.add(P.lift(cv, 36, 78, 68, 26, "green", 8, 4, hl=False), cv.poly([(48, 85), (48, 97), (58, 91)], P._on("green")), cv.text(82, 96, "Run", 13, 800, fill=P._on("green")))
    cv.add(P.lift(cv, 114, 78, 82, 26, "sun", 8, 4, hl=False), G.bug(cv, 131, 91, .42), cv.text(166, 96, "Debug", 13, 800, fill=INK))
    cv.add(P.lift(cv, 206, 78, 58, 26, "red", 8, 4, hl=False), cv.rect(218, 85, 11, 11, 2, "#fff"), cv.text(246, 96, "Stop", 13, 800, fill=P._on("red")))
    # file explorer
    cv.add(cv.rect(34, 116, 104, 176, 8, "#DCE6EC"))
    cv.add(cv.text(44, 136, "FILES", 11, 800, anchor="start", fill="#4A6470"))
    for i, (n, sel) in enumerate((("main.py", True), ("utils.py", False), ("data.txt", False))):
        y = 150 + i * 28
        if sel:
            cv.add(cv.rect(40, y - 2, 92, 24, 6, "#FFFFFF"), cv.rect(40, y - 2, 3, 24, 1.5, "#25B3BB"))
        cv.add(cv.rect(48, y + 2, 11, 14, 2, "#8AA0AC"), cv.text(66, y + 14, n, 12, 700, anchor="start", fill=INK, mono=True))
    # editor with a breakpoint, an error and a suggestion
    lines = ['def total(prices):', '    t = 0', '    for p in prices:', '        t = t + p', '    return t', '', 'print(totl([2, 3]))']
    cv.add(G.code(cv, 146, 112, 418, lines, None, 13, hl=(3,)))
    tx = G.code_x(146, 13)
    cv.add(cv.circle(152, G.code_y(112, 3, 13, None) - 4, 4.4, "#FF5A4F", stroke="#fff", sw=1.2))
    ey = G.code_y(112, 6, 13, None) + 4
    cv.add(cv.path("M%s %s q3 -4 6 0 t6 0 t6 0 t6 0 t6 0 t6 0 t6 0" % (_n(tx + 6 * 7.8), _n(ey)), stroke="#FF6B6B", sw=2))
    cv.add(P.lift(cv, tx + 6 * 7.8 - 6, ey + 8, 156, 24, "red", 8, 3, hl=False), cv.text(tx + 6 * 7.8 + 72, ey + 25, "totl is not defined", 11.5, 800, fill=P._on("red")))
    pop_x, pop_y = tx + 22 * 7.8, G.code_y(112, 2, 13, None) + 4
    cv.add(cv.rect(pop_x, pop_y, 110, 52, 7, "#FFFFFF", stroke="#C5D1D9", sw=1.2))
    cv.add(cv.rect(pop_x + 3, pop_y + 3, 104, 22, 5, "#D5F2F3"), cv.text(pop_x + 10, pop_y + 18, "prices", 12.5, 800, anchor="start", fill=INK, mono=True), cv.text(pop_x + 10, pop_y + 42, "print", 12.5, 600, anchor="start", fill="#4A6470", mono=True))
    # watch window and console
    cv.add(cv.rect(146, 310, 196, 162, 10, "#FFFFFF", stroke="#DCE6EC", sw=1.2), cv.text(160, 332, "WATCH", 11, 800, anchor="start", fill="#4A6470"))
    for i, (n, v) in enumerate((("t", "2"), ("p", "3"), ("prices", "[2, 3]"))):
        cv.add(cv.text(160, 360 + i * 30, n, 14, 800, anchor="start", fill=INK, mono=True), cv.text(330, 360 + i * 30, v, 14, 800, anchor="end", fill="#1B6F3E", mono=True))
    cv.add(G.terminal(cv, 352, 310, 212, [("paused at line 4", "#FFDA8A"), ("NameError: name", "#FF9A91"), ("'totl' is not defined", "#FF9A91")], "console", 12))
    # the list beside it
    items = [("Editor", "colour and line numbers"), ("Auto-complete", "suggests as you type"), ("Error check", "red line before you run"),
             ("Debugger", "breakpoint, step, watch"), ("Console", "output and error messages"), ("Project files", "all in one place")]
    for i, (t, d) in enumerate(items):
        y = 44 + i * 74
        cv.add(P.card(cv, 596, y, 180, 62, 14))
        cv.add(cv.text(612, y + 26, t, 14.5, 800, anchor="start", cls="il-ink"), cv.text(612, y + 46, d, 12, 650, anchor="start", cls="il-ink2"))
    # badges on the picture, matched to the list
    pts = [(420, 130), (pop_x + 124, pop_y + 14), (tx + 6 * 7.8 + 176, ey + 20), (190, G.code_y(112, 3, 13, None) - 28), (556, 330), (122, 124)]
    for i, (bx, by) in enumerate(pts):
        cv.add(P.badge(cv, bx, by, i + 1))
    for i in range(6):
        cv.add(P.badge(cv, 596, 44 + i * 74, i + 1))
    return figure(
        "ide-tour", cv, "What an integrated development environment gives you",
        "A mock up of an integrated development environment, an IDE, with six features picked out. The editor colours the code and numbers the lines. "
        "Auto-complete offers names as you type, here suggesting prices and print. The error check underlines a mistake in red before the program is "
        "run: in the picture totl is underlined with the message totl is not defined, because the function is called total. The debugger lets you set "
        "a breakpoint, shown as a red dot beside line 4, run to it, step through the code and watch the values of the variables, here t equal to 2, "
        "p equal to 3 and prices equal to the list 2, 3. The console shows output and error messages. A file explorer keeps all the project files in "
        "one place. A Run button runs the program, a Debug button runs it under the debugger, and Stop ends it.",
        ["Editor: colours the code and numbers the lines.",
         "Auto-complete: suggests names as you type, which saves typing and typos.",
         "Error check: underlines mistakes in red before you run the program.",
         "Debugger: breakpoints, stepping and a watch window to see what the variables hold.",
         "Console: where output and error messages appear.",
         "Project files: everything in one place."],
        "An IDE is an editor, a translator and a debugger in one window. Learn the features it gives you.")
