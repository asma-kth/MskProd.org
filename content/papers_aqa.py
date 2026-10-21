"""AQA GCSE Computer Science 8525: a full length Paper 1 (Python) and Paper 2.

Modelled on the 8525 past papers. Paper 1, Computational thinking and
programming skills, is 90 marks in 2 hours: algorithms in AQA pseudo-code to
trace and explain, Python to read, and programs to write, building to a long
programming task. Paper 2, Computing concepts, is 90 marks in 1 hour 45 minutes
across data representation, computer systems, networks, cyber security,
relational databases and SQL, and the impacts of technology. The SQL questions
run the student's statement against the database printed in the paper.
"""
from mskbuild.examkit import tick, rows, ans, boxes, table, calc, write, prog, db, sql
from mskbuild.models import Paper

ACC = "var(--purple)"


def last(inputs):
    """The numbers on the last line a program prints, for checks on a final answer."""
    return "nums(lines(run(%r))[-1])" % (inputs,)


PASSWORD = '''password = input("Enter a password: ")
hasDigit = False
for character in password:
    if character.isdigit():
        hasDigit = True
if len(password) >= 8 and hasDigit:
    print("Strong")
else:
    print("Weak")
'''

VOWELS = '''word = input("Enter a word: ")
count = 0
for letter in word.lower():
    if letter in "aeiou":
        count = count + 1
print("Number of vowels:", count)
'''

TOTAL = '''def playerTotal(scores, player):
    total = 0
    for score in scores[player]:
        total = total + score
    return total
'''

BEST = TOTAL + '''

def bestPlayer(scores):
    best = 0
    for player in range(1, len(scores)):
        if playerTotal(scores, player) > playerTotal(scores, best):
            best = player
    return best
'''

LOGIN_START = '''USERNAME = "admin"
PASSWORD = "Secret99"

# Write the rest of your program below
'''

LOGIN = '''USERNAME = "admin"
PASSWORD = "Secret99"

attempts = 0
granted = False
while attempts < 3 and not granted:
    username = input("Username: ")
    password = input("Password: ")
    if username == USERNAME and password == PASSWORD:
        granted = True
    else:
        attempts = attempts + 1
if granted:
    print("Access granted")
else:
    print("Account locked")
'''

PARKING = '''hours = int(input("Number of hours parked: "))
while hours < 1 or hours > 24:
    hours = int(input("Enter a whole number of hours from 1 to 24: "))
badge = input("Blue badge (Y/N)? ")
if hours <= 3:
    charge = hours * 2.00
else:
    charge = 3 * 2.00 + (hours - 3) * 1.50
if charge > 15:
    charge = 15.00
if badge == "Y":
    charge = 0
print("Charge: £" + format(charge, ".2f"))
'''

SCORES = "```pycode\nscores = [[12, 15, 9],\n          [20, 18, 22],\n          [7, 11, 14]]\n```"
FIG11 = [[12, 15, 9], [20, 18, 22], [7, 11, 14]]


# ===================================================================== 8525/1B (Python)

AQA_1 = Paper(
    slug="aqa-8525-paper-1",
    title="GCSE Computer Science Paper 1: Computational Thinking and Programming Skills (Python)",
    course="GCSE Computer Science", board="AQA", code="8525/1B",
    minutes=120, marks=90, accent=ACC, spec="8525", full=True,
    blurb="A full length 8525/1B paper: algorithms in AQA pseudo-code, data types, Boolean expressions, trace tables, searching and sorting, subroutines, testing, string handling, records, 2D lists, an authentication routine and a 9 mark car park program.",
    calculator="You must not use a calculator.",
    instructions=["Answer the questions that ask for program code in Python, using meaningful variable names and indentation.",
                  "Algorithms in the figures are written in AQA pseudo-code or Python, as labelled."],
    questions=[
        # ---------------------------------------------------- 01 algorithms
        tick("Shade **one** lozenge to show the best definition of an algorithm.",
             ["*A sequence of steps that can be followed to complete a task", "A program written in a high-level language",
              "A diagram that shows how the parts of a system are connected", "A set of data used to test a program"],
             "An algorithm is a sequence of steps that solves a problem or completes a task. It is not tied to any language.",
             label="01.1"),
        tick("Shade **one** lozenge to show which computational thinking technique involves removing unnecessary detail from a problem.",
             ["*Abstraction", "Decomposition", "Iteration", "Selection"],
             "Abstraction keeps only the details that matter. Decomposition breaks a problem into smaller problems.",
             label="01.2"),
        table("Figure 1 shows an algorithm. The user enters two whole numbers. Complete the table to show the output for each pair of inputs.",
              ["a", "b", "Output"], [["4", "9", "=5"], ["12", "7", "=5"], ["6", "6", "=0"]], numeric=True,
              figure="**Figure 1**\n\n```aqa\na ← USERINPUT\nb ← USERINPUT\nIF a > b THEN\n    c ← a - b\nELSE\n    c ← b - a\nENDIF\nOUTPUT c\n```",
              model="4 is not greater than 9, so c = 9 - 4 = 5. 12 is greater than 7, so c = 12 - 7 = 5. 6 is not greater than 6, so c = 6 - 6 = 0.",
              label="01.3"),
        tick("Shade **one** lozenge to show the purpose of the algorithm in Figure 1.",
             ["*It outputs the difference between the two numbers", "It outputs the larger of the two numbers",
              "It outputs the smaller of the two numbers", "It outputs the sum of the two numbers"],
             "Whichever number is larger, the smaller is subtracted from it, so the output is always the difference.",
             label="01.4"),

        # ---------------------------------------------------- 02 data types and Python expressions
        rows("A football club stores data about its matches. Shade one lozenge in each row to show the most suitable data type for each item.",
             ["Integer", "Real", "Boolean", "Character", "String"],
             [("The number of goals scored in a match", "Integer"), ("The average number of goals scored per match", "Real"),
              ("Whether the match has been played yet", "Boolean"), ("The name of the opposing team", "String")],
             model="Goals are whole numbers, an average can have a fractional part, played or not is true or false, and a team name is a string of characters.",
             label="02.1"),
        boxes("Figure 2 shows one line of a Python program. State the value of each Python expression.",
              [("len(word)", "8"), ("word[2]", ["M"]), ("word[1:4]", ["OMP"]), ("17 // 5", "3"), ("17 % 5", "2")],
              figure="**Figure 2**\n\n```pycode\nword = \"COMPUTER\"\n```",
              model="COMPUTER has 8 characters. Indexes start at 0, so word[2] is M, and word[1:4] is the characters at indexes 1, 2 and 3: OMP. 17 // 5 is integer division, 3, and 17 % 5 is the remainder, 2.",
              label="02.2"),

        # ---------------------------------------------------- 03 iteration, constants and Boolean expressions
        tick("Shade **two** lozenges to show which are examples of indefinite iteration.",
             ["*A WHILE loop that repeats until the user enters 0", "*A REPEAT ... UNTIL loop that repeats until a password is correct",
              "A FOR loop that repeats 10 times", "An IF statement with an ELSE"],
             "Indefinite iteration repeats until a condition is met, so the number of repeats is not known in advance. A FOR loop that runs 10 times is definite iteration, and IF is selection.",
             label="03.1"),
        write("Explain **one** reason why a programmer might use a named constant, such as VAT_RATE, instead of writing the value 0.2 each time it is needed.", 2, [
            ("If the value changes it only needs to be updated in one place", ["one place", "only once", "changed once", "update", "only change", "single place"]),
            ("The name makes the program easier to read and understand, and the value cannot be changed by mistake while the program runs",
             ["easier to read", "readab", "understand", "meaningful", "cannot be changed", "accidental", "by mistake"]),
        ], "If the VAT rate changes, the programmer only has to update the constant in one place, rather than finding every 0.2 in the program and risking missing one.",
              command="Explain", label="03.2"),
        boxes("Figure 3 shows the values of three Boolean variables in a Python program. State the value of each Python expression.",
              [("(a and not b) or (b and c)", ["True"]), ("not a or b", ["False"]), ("a and b or c", ["True"])],
              figure="**Figure 3**\n\n```pycode\na = True\nb = False\nc = True\n```",
              model="a and not b is True, so the whole OR is True. not a is False and b is False, so not a or b is False. and is worked out before or: a and b is False, and False or c is True.",
              label="03.3"),

        # ---------------------------------------------------- 04 trace table
        table("Complete the trace table for the algorithm in Figure 4. The first row has been completed for you.",
              ["i", "largest", "total"], [["", "3", "0"], ["1", "=8", "=8"], ["2", "=8", "=10"], ["3", "=8", "=17"]],
              per_row=True, numeric=True,
              figure="**Figure 4**\n\n```aqa\nnums ← [3, 8, 2, 7]\nlargest ← nums[0]\ntotal ← 0\nFOR i ← 1 TO 3\n    IF nums[i] > largest THEN\n        largest ← nums[i]\n    ENDIF\n    total ← total + nums[i]\nENDFOR\nOUTPUT largest\nOUTPUT total\n```",
              model="i = 1: 8 > 3, so largest becomes 8 and total becomes 8. i = 2: 2 is not larger, total becomes 10. i = 3: 7 is not larger than 8, total becomes 17.",
              label="04.1"),
        write("The algorithm in Figure 4 should output the total of all four numbers in nums. Explain why it does not, and how the algorithm could be corrected.", 2, [
            ("The first number, nums[0] (3), is never added to total because the loop starts at 1",
             ["nums[0]", "first number", "first item", "index 0", "never added", "not added", "missed", "skipped", "starts at 1"]),
            ("Set total to nums[0] at the start, or make the loop run from 0 to 3",
             ["total ← nums[0]", "total = nums[0]", "total to nums[0]", "from 0", "0 to 3", "i ← 0", "start at 0", "starts at 0", "begin at 0"]),
        ], "The loop starts at index 1, so nums[0], the 3, is never added: the algorithm outputs 17 instead of 20. Setting total to nums[0] instead of 0 at the start fixes it.",
              command="Explain", label="04.2"),

        # ---------------------------------------------------- 05 searching and sorting
        tick("Shade **one** lozenge to show which statement must be true for a binary search to be used on a list.",
             ["*The list must be in order", "The list must only contain numbers",
              "The list must contain an even number of items", "The item being searched for must be in the list"],
             "A binary search discards half of the list at each step, which only works if the list is sorted.",
             label="05.1"),
        table("A binary search is used to find Lemon in the list in Figure 5. The middle item is found with (first + last) DIV 2, where first and last are the positions of the first and last items still being searched. Complete the table to show the item checked at each comparison.",
              ["Comparison", "Item checked"], [["1", "=Fig"], ["2", "=Kiwi"], ["3", "=Lemon"]],
              figure="**Figure 5**\n\n| Position | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |\n|---|---|---|---|---|---|---|---|---|---|\n| Item | Apple | Banana | Cherry | Date | Fig | Grape | Kiwi | Lemon | Mango |",
              model="(0 + 8) DIV 2 = 4: Fig. Lemon comes after Fig, so first becomes 5. (5 + 8) DIV 2 = 6: Kiwi. Lemon comes after Kiwi, so first becomes 7. (7 + 8) DIV 2 = 7: Lemon, found.",
              label="05.2"),
        write("Explain why a binary search is usually more efficient than a linear search for a large list.", 2, [
            ("Each comparison halves the number of items still to be searched", ["half", "halves", "halving", "discard", "eliminat"]),
            ("so far fewer comparisons are needed, whereas a linear search may have to check every item", ["fewer comparisons", "every item", "each item", "one by one", "one at a time", "fewer"]),
        ], "Every comparison in a binary search discards half of the items that are left, so even a list of a million items needs only about 20 comparisons. A linear search checks the items one at a time and may have to look at all of them.",
              command="Explain", label="05.3"),
        table("A bubble sort is used to put the list 5, 1, 4, 2 into ascending order. Complete the table to show the list after each of the first two passes.",
              ["", "Position 0", "Position 1", "Position 2", "Position 3"],
              [["After pass 1", "=1", "=4", "=2", "=5"], ["After pass 2", "=1", "=2", "=4", "=5"]], per_row=True, numeric=True,
              model="Pass 1: 5 and 1 swap, 5 and 4 swap, 5 and 2 swap, giving 1, 4, 2, 5. Pass 2: 1 and 4 stay, 4 and 2 swap, 4 and 5 stay, giving 1, 2, 4, 5.",
              label="05.4"),
        tick("Shade **one** lozenge to show an advantage of merge sort compared with bubble sort.",
             ["*It is usually much faster for large lists", "It uses less memory", "It is easier to write",
              "It can only be used on lists that are nearly sorted"],
             "Merge sort is far more time efficient on large lists. It needs extra memory for the lists it merges, and it is harder to write.",
             label="05.5"),

        # ---------------------------------------------------- 06 subroutines
        ans("State the output when the program in Figure 6 is run.", "10", numeric=True,
            figure="**Figure 6**\n\n```pycode\ndef calculate(a, b):\n    result = a * 2 + b\n    return result\n\nx = calculate(3, 4)\nprint(x)\n```",
            model="calculate(3, 4) works out 3 * 2 + 4 = 10, which is returned, stored in x and printed.", width=6, label="06.1"),
        rows("Shade one lozenge in each row to show how each identifier is used in Figure 6.",
             ["Parameter", "Local variable", "Global variable"],
             [("a", "Parameter"), ("result", "Local variable"), ("x", "Global variable")],
             model="a and b receive the values passed in, so they are parameters. result is created inside the subroutine, so it is local. x is assigned in the main program, so it is global.",
             label="06.2"),
        write("Explain **two** advantages of using subroutines when writing a large program.", 2, [
            ("A subroutine can be called many times, so code is reused rather than written again", ["reuse", "re-use", "called", "again", "many times", "rewrit", "repeat"]),
            ("Each subroutine can be written and tested on its own, or by different programmers, which makes the program easier to debug and maintain",
             ["test", "separately", "on its own", "independent", "different programmers", "team", "debug", "maintain", "decompos"]),
        ], "A subroutine can be called whenever it is needed, so the code is written once and reused. Each subroutine is a small, self-contained part that can be tested on its own, or written by a different member of a team, so errors are easier to find and the program is easier to maintain.",
              command="Explain", label="06.3"),

        # ---------------------------------------------------- 07 errors and testing
        rows("Shade one lozenge in each row to show whether each is an example of a syntax error or a logic error.",
             ["Syntax error", "Logic error"],
             [("Leaving out the closing bracket of print(", "Syntax error"), ("Using < instead of <= in a condition", "Logic error"),
              ("Spelling the keyword while as whlie", "Syntax error"), ("Adding two numbers that should have been multiplied", "Logic error")],
             marks=2, model="Breaking the rules of the language is a syntax error, so the program will not run. A program that runs but gives the wrong result has a logic error.",
             label="07.1"),
        rows("A program accepts a test mark, which must be a whole number from 0 to 50. Shade one lozenge in each row to show the type of each piece of test data.",
             ["Normal", "Boundary", "Erroneous"], [("27", "Normal"), ("50", "Boundary"), ("fifty", "Erroneous")],
             model="27 is a typical valid mark, 50 is at the edge of the allowed range, and fifty is the wrong type of data, so it should be rejected.",
             label="07.2"),
        tick("The program in Figure 7 should output the total of the whole numbers from 1 to 10, but it outputs 45. Shade **one** lozenge to show the line that contains the error.",
             ["01", "*02", "03", "04"],
             "range(1, 10) stops before 10, so 10 is never added and the total is 45 instead of 55.",
             figure="**Figure 7**\n\n```pycode\n01 total = 0\n02 for i in range(1, 10):\n03     total = total + i\n04 print(total)\n```",
             label="07.3"),
        ans("Write the corrected version of the line you identified in 07.3.",
            ["for i in range(1, 11):", "for i in range(1, 11)", "for i in range(11):", "for i in range(11)",
             "for i in range(0, 11):", "for i in range(0, 11)"],
            model="for i in range(1, 11):", width=22, label="07.4"),

        # ---------------------------------------------------- 08 password strength
        prog("A website checks how strong a new password is. A password is **strong** if it has at least 8 characters and contains at least one digit.\n\nWrite a Python program that:\n\n- gets the user to enter a password\n- outputs Strong if the password is strong\n- otherwise outputs Weak.",
             "# Write your program here\n", PASSWORD,
             [("Gets a password from the user", "uses(r'input\\s*\\(')"),
              ("Outputs Strong for a long password that contains a digit, such as secure123",
               "has(run(['secure123']), 'strong') and not has(run(['secure123']), 'weak')"),
              ("Outputs Weak for a password with a digit that is too short, such as abc1",
               "has(run(['abc1']), 'weak') and not has(run(['abc1']), 'strong')"),
              ("Outputs Weak for a long password with no digit, such as abcdefghij",
               "has(run(['abcdefghij']), 'weak') and not has(run(['abcdefghij']), 'strong')"),
              ("Treats exactly 8 characters as long enough: abcdefg1 is Strong",
               "has(run(['abcdefg1']), 'strong') and not has(run(['abcdefg1']), 'weak')")],
             model="Check every character for a digit, then test both rules together with and, using >= 8 so that a password of exactly 8 characters counts.",
             wrong=[PASSWORD.replace(">= 8", "> 8"),
                    'password = input()\nif len(password) >= 8:\n    print("Strong")\nelse:\n    print("Weak")\n'],
             label="08", filename="password.py"),

        # ---------------------------------------------------- 09 string handling
        boxes("State the four values output by the algorithm in Figure 9. The character code for 'A' is 65.",
              [("First output", "9"), ("Second output", ["alg"]), ("Third output", "4"), ("Fourth output", "66")],
              figure="**Figure 9**\n\n```aqa\nword ← 'algorithm'\nOUTPUT LEN(word)\nOUTPUT SUBSTRING(0, 2, word)\nOUTPUT POSITION(word, 'r')\nOUTPUT CHAR_TO_CODE('B')\n```",
              model="algorithm has 9 characters. SUBSTRING(0, 2, word) gives the characters at positions 0 to 2 inclusive: alg. r is at position 4, counting from 0. B comes one after A, so its code is 66.",
              label="09.1"),
        prog("Write a Python program that gets the user to enter a word and outputs how many vowels (a, e, i, o and u) the word contains. Vowels in upper case and in lower case must both be counted.",
             "# Write your program here\n", VOWELS,
             [("Gets a word from the user", "uses(r'input\\s*\\(')"),
              ("Outputs 3 for banana", "nums(run(['banana']))[-1] == 3"),
              ("Counts upper case vowels too: 5 for EDUCATION", "nums(run(['EDUCATION']))[-1] == 5"),
              ("Outputs 0 for a word with no vowels, such as rhythm", "nums(run(['rhythm']))[-1] == 0")],
             model="Loop through the word one letter at a time, converting each to lower case, and add one to a count whenever the letter is in \"aeiou\".",
             wrong=[VOWELS.replace("word.lower()", "word")],
             label="09.2", filename="vowels.py"),

        # ---------------------------------------------------- 10 random numbers and records
        tick("The random module has been imported. Shade **one** lozenge to show which Python expression gives a random whole number from 1 to 6 inclusive.",
             ["*random.randint(1, 6)", "random.randint(0, 6)", "random.randint(1, 7)", "random.random() * 6"],
             "randint includes both of its end values, so randint(1, 6) gives 1, 2, 3, 4, 5 or 6.", label="10.1"),
        write("Figure 10 shows a record used by a library program. Explain **one** advantage of storing the details of each book as a record rather than in four separate variables.", 2, [
            ("All the data about one book is kept together under one name", ["together", "one name", "single", "grouped", "one variable", "one structure", "related"]),
            ("so it is easier to manage: a whole book can be passed to a subroutine, or many books stored in an array of records",
             ["array", "list", "pass", "subroutine", "many books", "easier", "manage", "each book"]),
        ], "A record keeps all the related data about one book together under a single name. That makes the program easier to manage: a whole book can be passed to a subroutine in one go, and the library's books can be stored in a single array of Book records.",
              command="Explain", label="10.2",
              figure="**Figure 10**\n\n```aqa\nRECORD Book\n    title : String\n    author : String\n    pages : Integer\n    onLoan : Boolean\nENDRECORD\n```"),

        # ---------------------------------------------------- 11 2D lists
        boxes("Three players take part in a quiz. Each row of the list in Figure 11 holds one player's scores in three rounds, so scores[1][0] is player 1's score in round 0. State the value of each.",
              [("scores[1][2]", "22"), ("scores[2][0]", "7")], numeric=True, figure="**Figure 11**\n\n" + SCORES,
              model="scores[1] is the row [20, 18, 22], and item 2 of it is 22. scores[2] is [7, 11, 14], and item 0 of it is 7.",
              label="11.1"),
        prog("Write a Python subroutine called playerTotal that takes the 2D list of scores and a player number as parameters, and returns the total of that player's scores.",
             "def playerTotal(scores, player):\n    # Write the subroutine here\n    pass\n", TOTAL,
             [("Defines playerTotal with two parameters", "defines('playerTotal') and len(params('playerTotal')) == 2"),
              ("Returns 36 for player 0 in Figure 11", "call('playerTotal', %r, 0) == 36" % FIG11),
              ("Works for any player and any number of rounds", "call('playerTotal', %r, 2) == 32 and call('playerTotal', [[1, 2], [3, 4, 5]], 1) == 12" % FIG11)],
             model="Loop through the player's row, scores[player], adding each score to a running total, then return the total.",
             wrong=["def playerTotal(scores, player):\n    total = 0\n    for row in scores:\n        total = total + row[player]\n    return total\n"],
             label="11.2", filename="quiz.py"),
        prog("Write a Python subroutine called bestPlayer that takes the 2D list of scores as a parameter and returns the number of the player with the highest total. The subroutine playerTotal is given for you to use. You can assume no two players have the same total.",
             TOTAL + "\n\ndef bestPlayer(scores):\n    # Write the subroutine here\n    pass\n", BEST,
             [("Defines bestPlayer with one parameter", "defines('bestPlayer') and len(params('bestPlayer')) == 1"),
              ("Returns 1 for the scores in Figure 11", "call('bestPlayer', %r) == 1" % FIG11),
              ("Works when the best player is the first or the last", "call('bestPlayer', [[9, 9], [1, 1], [2, 2]]) == 0 and call('bestPlayer', [[1], [2], [3]]) == 2"),
              ("Compares each player's total over every round, for any number of players", "call('bestPlayer', [[3, 4], [10, 1], [6, 6], [2, 9]]) == 2")],
             model="Keep the number of the best player so far, starting with player 0. Loop through the other players and, whenever one has a higher total, remember that player instead. Return the player number, not the total.",
             wrong=[TOTAL + "\n\ndef bestPlayer(scores):\n    best = 0\n    for player in range(1, len(scores)):\n        if scores[player][0] > scores[best][0]:\n            best = player\n    return best\n",
                    TOTAL + "\n\ndef bestPlayer(scores):\n    best = 0\n    for player in range(1, len(scores)):\n        if playerTotal(scores, player) > playerTotal(scores, best):\n            best = player\n    return playerTotal(scores, best)\n"],
             label="11.3", filename="quiz.py"),

        # ---------------------------------------------------- 12 authentication
        prog("A program must check a user's login details. The correct username and password are stored in the constants USERNAME and PASSWORD.\n\nWrite a Python program that:\n\n- gets the user to enter a username and a password\n- outputs Access granted if both are correct\n- gives the user up to three attempts\n- outputs Account locked if all three attempts are wrong.",
             LOGIN_START, LOGIN,
             [("Outputs Access granted when both are correct", "has(run(['admin', 'Secret99']), 'access granted')"),
              ("Checks both the username and the password", "not has(run(['admin', 'wrong', 'bob', 'Secret99', 'x', 'y']), 'granted')"),
              ("Allows a second attempt", "has(run(['a', 'b', 'admin', 'Secret99']), 'access granted')"),
              ("Allows a third attempt", "has(run(['a', 'b', 'c', 'd', 'admin', 'Secret99']), 'access granted')"),
              ("Outputs Account locked after three wrong attempts, without asking again", "has(run(['a', 'b', 'c', 'd', 'e', 'f']), 'locked')"),
              ("Ends with Access granted, not Account locked, when the third attempt is right",
               "'granted' in norm(lines(run(['a', 'b', 'c', 'd', 'admin', 'Secret99']))[-1])"),
              ("Uses iteration to repeat the attempts", "count('While') + count('For') >= 1")],
             model="Count the failed attempts in a loop that stops when the details are right or after three attempts, checking the username and the password together with and. After the loop, output one message or the other.",
             wrong=[LOGIN.replace("attempts < 3", "attempts < 4"),
                    LOGIN.replace("username == USERNAME and password == PASSWORD", "username == USERNAME or password == PASSWORD"),
                    LOGIN.replace('if granted:\n    print("Access granted")\nelse:\n    print("Account locked")',
                                  'if granted:\n    print("Access granted")\nprint("Account locked")')],
             label="12", filename="login.py"),

        # ---------------------------------------------------- 13 car park
        prog("A car park charges £2.00 an hour for each of the first 3 hours, and £1.50 for each hour after that. The most anyone pays is £15.00. Blue badge holders park for free.\n\nWrite a Python program that:\n\n- gets the user to enter the number of hours parked, as a whole number\n- keeps asking until the number of hours is from 1 to 24\n- gets the user to enter Y or N to say whether they have a blue badge\n- calculates the charge\n- outputs the charge.",
             "# Write your program here\n", PARKING,
             [("Charges £2.00 an hour up to 3 hours: 2 hours costs £4.00", "4 in " + last(['2', 'N'])),
              ("Rejects fewer than 1 hour and asks again", "4 in " + last(['0', '2', 'N'])),
              ("Rejects more than 24 hours and asks again", "6 in " + last(['25', '3', 'N'])),
              ("Charges £1.50 for each hour after the first 3: 5 hours costs £9.00", "9 in " + last(['5', 'N'])),
              ("Gets the charge right below the maximum: 8 hours costs £13.50", "13.5 in " + last(['8', 'N'])),
              ("Charges no more than £15.00: 20 hours costs £15.00", "15 in %s and 31.5 not in %s" % (last(['20', 'N']), last(['20', 'N']))),
              ("Blue badge holders pay nothing", "0 in %s and 9 not in %s" % (last(['5', 'Y']), last(['5', 'Y']))),
              ("Accepts the boundary values 1 and 24", "2 in %s and 15 in %s" % (last(['1', 'N']), last(['24', 'N']))),
              ("Uses a loop to repeat the validation", "count('While') >= 1")],
             model="Validate the hours with a while loop. Work out the charge for the first 3 hours and the hours after that separately, cap it at 15, and set it to 0 for a blue badge holder before outputting it.",
             wrong=[PARKING.replace("if charge > 15:\n    charge = 15.00\n", ""),
                    PARKING.replace("hours < 1 or hours > 24", "hours <= 1 or hours > 24"),
                    PARKING.replace("3 * 2.00 + (hours - 3) * 1.50", "hours * 1.50")],
             label="13", filename="parking.py"),
    ],
)


# ===================================================================== 8525/2

FILMS = db(
    ("Film", ["FilmID INTEGER", "Title TEXT", "Genre TEXT", "Year INTEGER", "Minutes INTEGER"],
     [(1, "Star Quest", "Sci-fi", 2019, 128), (2, "The Last Laugh", "Comedy", 2021, 95),
      (3, "Deep Water", "Thriller", 2018, 110), (4, "Robot Rising", "Sci-fi", 2022, 141),
      (5, "Holiday Mix-up", "Comedy", 2017, 88), (6, "Night Train", "Thriller", 2023, 102),
      (7, "Moon Base", "Sci-fi", 2015, 150)]),
    ("Showing", ["ShowID INTEGER", "FilmID INTEGER", "Screen INTEGER", "StartTime TEXT"],
     [(101, 4, 1, "18:00"), (102, 2, 2, "18:30"), (103, 4, 2, "20:45"), (104, 6, 1, "21:00"), (105, 1, 3, "17:15")]),
)

HUFFMAN = """**Figure 3**

```text
            (7)
          0 / \\ 1
         A:3   (4)
             0 / \\ 1
            N:2   (2)
                0 / \\ 1
               B:1   S:1
```"""


def _heater():
    base = ["S AND NOT W", "NOT W AND S", "S AND (NOT W)", "(NOT W) AND S", "S . NOT W", "S.¬W", "S AND ¬W"]
    return base + ["H = " + b for b in base]


AQA_2 = Paper(
    slug="aqa-8525-paper-2",
    title="GCSE Computer Science Paper 2: Computing Concepts",
    course="GCSE Computer Science", board="AQA", code="8525/2",
    minutes=105, marks=90, accent=ACC, spec="8525", full=True,
    blurb="A full length 8525/2 paper: number bases, binary arithmetic and shifts, characters, images and sound, run length encoding and Huffman coding, Boolean logic, systems architecture, networks, cyber security, SQL queries run against a cinema database, and a discussion of smart speakers.",
    calculator="You must not use a calculator.",
    instructions=["In this paper 1 kilobyte (kB) = 1000 bytes, 1 megabyte (MB) = 1000 kilobytes, and so on, as in the specification.",
                  "SQL answers are run against the tables printed in question 08, so they must be valid SQL."],
    questions=[
        # ---------------------------------------------------- 01 number bases and binary arithmetic
        boxes("Complete each conversion.",
              [("1011 0101 in denary", "181"), ("200 as an 8-bit binary number", ["11001000"]),
               ("hexadecimal B7 in binary", ["10110111"]), ("0110 1110 in hexadecimal", ["6E"])],
              model="1011 0101 = 128 + 32 + 16 + 4 + 1 = 181. 200 = 128 + 64 + 8 = 1100 1000. B is 1011 and 7 is 0111. 0110 is 6 and 1110 is E: 6E.",
              label="01.1"),
        write("Explain why computer scientists often use hexadecimal instead of binary.", 2, [
            ("Hexadecimal is shorter: one hex digit represents four bits", ["four bits", "4 bits", "nibble", "shorter", "fewer digits", "compact"]),
            ("so it is easier for people to read and remember, and fewer mistakes are made copying it", ["easier", "read", "remember", "fewer mistakes", "fewer errors", "less likely"]),
        ], "Each hexadecimal digit stands for exactly four bits, so a byte is two hex digits instead of eight binary digits. That makes values much easier for people to read and remember, and fewer mistakes are made when copying them.",
              command="Explain", label="01.2"),
        boxes("Add together the three binary numbers 0010 1101, 0100 0110 and 0001 0011. Give your answer as an 8-bit binary number, in two halves.",
              [("Most significant four bits", ["1000"]), ("Least significant four bits", ["0110"])],
              model="Adding column by column, carrying where needed, gives 1000 0110. Check in denary: 45 + 70 + 19 = 134, and 134 = 128 + 4 + 2.",
              label="01.3"),
        ans("Apply a logical left shift of three places to the binary number 0001 0110. Give the 8-bit result.", ["10110000"],
            model="Every bit moves three places left and zeros fill the gap on the right: 1011 0000.", width=10, label="01.4"),
        tick("Shade **one** lozenge to show the effect of the shift in 01.4 on the value of the number.",
             ["*It multiplies it by 8", "It multiplies it by 3", "It divides it by 8", "It adds 3 to it"],
             "Each place shifted left doubles the number, so three places multiply it by 2 x 2 x 2 = 8: 22 becomes 176.",
             label="01.5"),

        # ---------------------------------------------------- 02 units, characters, images and sound
        tick("Shade **one** lozenge to show which of these is the largest amount of storage.",
             ["2,500 gigabytes", "40,000 megabytes", "*3 terabytes", "900,000 kilobytes"],
             "3 terabytes is 3,000 gigabytes. 40,000 megabytes is 40 gigabytes and 900,000 kilobytes is 0.9 gigabytes.",
             label="02.1"),
        boxes("In ASCII, the character code for 'A' is 65. State:",
              [("the character code for 'E'", "69"), ("the character whose code is 72", ["H"])],
              model="The letters have consecutive codes: A 65, B 66, C 67, D 68, E 69, F 70, G 71, H 72.",
              label="02.2"),
        write("Explain **one** advantage of using Unicode instead of ASCII.", 2, [
            ("Unicode uses more bits per character, so it can represent far more characters", ["more bits", "16", "32", "more characters", "millions", "larger", "over a million"]),
            ("so it can represent the characters of every language, and symbols such as emoji", ["language", "alphabet", "emoji", "symbols", "chinese", "arabic", "world"]),
        ], "ASCII uses 7 bits, so it has only 128 codes, enough for English. Unicode uses more bits for each character, so it can represent over a million characters, including every writing system in the world and emoji.",
              command="Explain", label="02.3"),
        calc("An image is 400 pixels wide and 300 pixels high, and has a colour depth of 8 bits. Calculate the file size of the image in kilobytes. Show your working.",
             ["120", "117.19"], 3, [
                 ("Multiplies width by height by colour depth: 960,000 bits", ["400 x 300 x 8", "400*300*8", "400 × 300 × 8", "960000", "960,000", "960 000"]),
                 ("Divides by 8 and then by 1000 to reach kilobytes", ["/ 8", "/8", "÷ 8", "÷8", "/ 1000", "/1000", "÷ 1000", "÷1000", "/1024", "/ 1024"])],
             model="400 x 300 x 8 = 960,000 bits. 960,000 / 8 = 120,000 bytes. 120,000 / 1000 = 120 kB.",
             unit="kB", tol=0.01, label="02.4"),
        calc("A sound is sampled at 20,000 Hz with a sample resolution of 8 bits. Calculate the file size, in bytes, of a 5 second recording. Show your working.",
             ["100000"], 2, [
                 ("Multiplies sample rate by resolution by time: 800,000 bits", ["20000 x 8 x 5", "20,000 x 8 x 5", "20000*8*5", "800000", "800,000", "800 000"])],
             model="20,000 x 8 x 5 = 800,000 bits. 800,000 / 8 = 100,000 bytes.",
             unit="bytes", label="02.5"),

        # ---------------------------------------------------- 03 compression
        boxes("Run length encoding (RLE) is used to compress the bit pattern 0000011100000011. Complete the frequency and data pairs that represent it.",
              [("Pair 1", ["5 0", "5,0", "(5,0)"]), ("Pair 2", ["3 1", "3,1", "(3,1)"]),
               ("Pair 3", ["6 0", "6,0", "(6,0)"]), ("Pair 4", ["2 1", "2,1", "(2,1)"])],
              groups=[("Pairs 1 and 2", [0, 1]), ("Pairs 3 and 4", [2, 3])],
              model="The pattern is five 0s, three 1s, six 0s and two 1s: 5 0, 3 1, 6 0, 2 1.",
              label="03.1"),
        boxes("Figure 3 shows a Huffman tree for the characters in the word BANANAS. A left branch is 0 and a right branch is 1. State the Huffman code for each character.",
              [("N", "10"), ("S", "111")], figure=HUFFMAN,
              model="Reading from the root: N is right then left, 10. S is right, right, right, 111.",
              label="03.2"),
        calc("Calculate the number of bits needed to store the word BANANAS using the Huffman codes in Figure 3. Show your working.",
             ["13"], 2, [("Multiplies each character's frequency by the length of its code", ["3 x 1", "3x1", "2 x 2", "2x2", "1 x 3", "1x3", "3 + 3 + 4 + 3", "3+3+4+3"])],
             model="A: 3 x 1 bit = 3. N: 2 x 2 bits = 4. B: 1 x 3 bits = 3. S: 1 x 3 bits = 3. 3 + 4 + 3 + 3 = 13 bits.",
             unit="bits", label="03.3"),
        calc("Calculate how many bits are saved by storing BANANAS using Huffman coding instead of 7-bit ASCII. Show your working.",
             ["36"], 2, [("Works out that 7-bit ASCII needs 49 bits", ["49", "7 x 7", "7x7", "7 × 7"])],
             model="BANANAS has 7 characters, so 7-bit ASCII needs 7 x 7 = 49 bits. 49 - 13 = 36 bits saved.",
             unit="bits", label="03.4"),

        # ---------------------------------------------------- 04 Boolean logic
        table("Complete the truth table for the expression Q = (A OR B) AND (NOT C), written Q = (A + B) · C̄ in Boolean notation.",
              ["A", "B", "C", "Q"],
              [["0", "0", "0", "=0"], ["0", "0", "1", "=0"], ["0", "1", "0", "=1"], ["0", "1", "1", "=0"],
               ["1", "0", "0", "=1"], ["1", "0", "1", "=0"], ["1", "1", "0", "=1"], ["1", "1", "1", "=0"]],
              groups=[("Rows 1 and 2", [0, 1]), ("Rows 3 and 4", [2, 3]), ("Rows 5 and 6", [4, 5]), ("Rows 7 and 8", [6, 7])], numeric=True,
              model="Q is 1 only when C is 0 and at least one of A and B is 1.", label="04.1"),
        tick("Shade **one** lozenge to show the logic gate whose output is 1 only when its two inputs are different.",
             ["AND", "OR", "*XOR", "NOT"], "XOR, exclusive OR, outputs 1 when exactly one input is 1.", label="04.2"),
        ans("A heater (H) is on when the system is switched on (S) and the room is not warm (W). Write a Boolean expression for H.",
            _heater(), model="H = S AND NOT W, written H = S · W̄ in Boolean notation.", width=18, label="04.3"),

        # ---------------------------------------------------- 05 computer systems
        rows("Shade one lozenge in each row to show the component of the CPU that is described.",
             ["ALU", "Control unit", "Clock", "Register"],
             [("Carries out arithmetic and logical operations", "ALU"),
              ("Coordinates the actions of the CPU by sending out control signals", "Control unit"),
              ("Sends out regular pulses that keep the CPU's actions in step", "Clock"),
              ("A tiny, very fast storage location inside the CPU", "Register")],
             model="The ALU calculates and compares, the control unit coordinates, the clock keeps time, and registers hold the values being worked on.",
             label="05.1"),
        write("Describe the fetch-execute cycle.", 3, [
            ("The next instruction is fetched from main memory, using its address", ["fetch", "main memory", "ram", "address"]),
            ("The instruction is decoded by the control unit", ["decode"]),
            ("The instruction is executed, and the cycle repeats for the next instruction", ["execute", "carried out", "repeat", "next instruction"]),
        ], "The CPU fetches the next instruction from main memory, using the address held in the program counter. The control unit decodes the instruction to work out what it means. The instruction is then executed, and the cycle repeats with the next instruction.",
              command="Describe", label="05.2"),
        write("Explain why a solid state drive is often used in a laptop instead of a magnetic hard disk drive.", 2, [
            ("An SSD has no moving parts, so it is more durable if the laptop is knocked or dropped", ["no moving parts", "durable", "robust", "dropped", "knocked", "shock"]),
            ("It is faster, lighter and uses less power, so the laptop starts quickly and its battery lasts longer",
             ["faster", "quicker", "lighter", "less power", "battery", "silent", "smaller", "thinner"]),
        ], "A laptop gets carried around and knocked, and an SSD has no moving parts to damage. It is also faster, lighter and uses less power than a hard disk, so the laptop starts and loads quickly and its battery lasts longer.",
              command="Explain", label="05.3"),
        rows("Shade one lozenge in each row to show the type of translator described.", ["Compiler", "Interpreter", "Assembler"],
             [("Translates a whole high-level program into machine code before it is run", "Compiler"),
              ("Translates and executes a high-level program one line at a time", "Interpreter"),
              ("Translates assembly language into machine code", "Assembler")],
             model="A compiler translates everything first, an interpreter translates and runs line by line, and an assembler translates assembly language.",
             label="05.4"),
        write("Explain why most programs are written in high-level languages rather than low-level languages.", 2, [
            ("High-level code uses English-like statements, so it is easier to read, write, understand and debug", ["english", "easier", "understand", "read", "debug", "quicker to write"]),
            ("It is portable: it is not tied to one type of processor, and one statement can do the work of many machine code instructions",
             ["portable", "any processor", "different processors", "machine independent", "not specific", "many instructions", "different computers"]),
        ], "High-level languages use English-like keywords, so programs are quicker to write and much easier to read and debug. They are also portable: the same program can be translated for different types of processor, whereas low-level code is written for one processor.",
              command="Explain", label="05.5"),
        tick("Shade **two** lozenges to show which statements about embedded systems are true.",
             ["*They are built into a larger device", "*They usually carry out one dedicated task",
              "They always have a keyboard and a monitor", "They are general purpose computers"],
             "An embedded system, such as the controller in a washing machine, is part of a larger device and does one job.",
             label="05.6"),

        # ---------------------------------------------------- 06 networks
        tick("Shade **one** lozenge to show which describes a personal area network (PAN).",
             ["*A network of devices used by one person, connected over a short distance",
              "A network that covers a large geographical area, such as a country",
              "A network of computers on a single site, such as a school",
              "A network in which every device is connected to every other device"],
             "A PAN connects one person's devices, such as a phone and headphones over Bluetooth.", label="06.1"),
        rows("Shade one lozenge in each row to show the layer of the TCP/IP model at which each protocol operates.",
             ["Application", "Transport", "Internet", "Link"],
             [("HTTPS", "Application"), ("TCP", "Transport"), ("IP", "Internet"), ("Ethernet", "Link")],
             marks=2, model="HTTPS is an application protocol, TCP works at the transport layer, IP at the internet layer and Ethernet at the link layer.",
             label="06.2"),
        write("Explain the purpose of the protocols SMTP and IMAP.", 2, [
            ("SMTP is used to send emails, to a mail server and between servers", ["send"]),
            ("IMAP is used to retrieve or access emails from the mail server, keeping them on the server", ["retriev", "access", "download", "read", "collect", "fetch"]),
        ], "SMTP is used to send email: it transfers a message from the sender's device to their mail server and on to the recipient's server. IMAP is used to retrieve email: it lets a device read the messages that are kept on the server, so they stay in step across devices.",
              command="Explain", label="06.3"),
        write("Explain how MAC address filtering helps to keep a wireless network secure.", 2, [
            ("Only devices whose MAC addresses are on an approved list can connect", ["approved", "allowed", "whitelist", "list", "permitted", "only devices"]),
            ("Every device has a unique MAC address, so any unknown device is blocked", ["unique", "unknown", "blocked", "rejected", "not on the list", "denied", "refused"]),
        ], "Every network interface has a unique MAC address. The router keeps a list of the MAC addresses that are allowed, and refuses to connect any device whose address is not on the list.",
              command="Explain", label="06.4"),
        tick("Shade **one** lozenge to show an advantage of a wireless network compared with a wired network.",
             ["*Users can connect from anywhere within range, so they can move around", "Data is always transmitted faster",
              "It is more secure", "It is less affected by interference"],
             "Wireless gives freedom to move. Wired connections are usually faster, more secure and less affected by interference.",
             label="06.5"),

        # ---------------------------------------------------- 07 cyber security
        rows("Shade one lozenge in each row to show the form of social engineering described.", ["Blagging", "Phishing", "Shouldering"],
             [("Phoning an employee, pretending to be from IT support, to get their password", "Blagging"),
              ("Watching someone enter their PIN at a cash machine", "Shouldering"),
              ("Sending emails that link to a fake bank website", "Phishing")],
             model="Inventing a scenario to get information is blagging, watching someone is shouldering, and fake emails are phishing.",
             label="07.1"),
        rows("Shade one lozenge in each row to show the type of malware described.", ["Virus", "Trojan", "Spyware"],
             [("Attaches itself to a file and spreads when the file is run", "Virus"),
              ("Pretends to be useful software but secretly does harm", "Trojan"),
              ("Secretly records what a user does, such as the keys they press", "Spyware")],
             model="A virus copies itself into other files, a trojan is disguised as something useful, and spyware secretly gathers information.",
             label="07.2"),
        write("Describe the difference between black-box and white-box penetration testing.", 2, [
            ("Black-box testing simulates an external attack by someone with no knowledge of the system and no login details",
             ["no knowledge", "external", "outside", "no information", "no credentials", "no login", "outsider"]),
            ("White-box testing simulates an attack by a malicious insider who knows about the system and has some login details",
             ["insider", "employee", "inside", "knowledge of the system", "credentials", "knows", "login details", "staff"]),
        ], "Black-box testing simulates an attack from outside: the testers are given no knowledge of the system and no login details. White-box testing simulates a malicious insider, such as an employee, who knows how the system works and has basic login details.",
              command="Describe", label="07.3"),
        write("Explain why automatic software updates help to protect a computer.", 2, [
            ("Updates contain patches that fix security vulnerabilities", ["patch", "fix", "vulnerab", "security hole", "weakness", "bug", "loophole"]),
            ("Being automatic, they are installed as soon as they are released, before attackers can exploit the weakness and without relying on the user",
             ["automatic", "straight away", "as soon as", "forget", "before", "exploit", "up to date", "immediately"]),
        ], "Software updates include patches that close security weaknesses that have been discovered. Installing them automatically means the computer is protected as soon as the fix is released, before attackers can exploit the weakness, and does not depend on the user remembering to update.",
              command="Explain", label="07.4"),
        tick("Shade **one** lozenge to show the purpose of a CAPTCHA.",
             ["*To check that the user is a person, not an automated program", "To encrypt data sent over a network",
              "To scan downloaded files for viruses", "To back up data automatically"],
             "A CAPTCHA asks for something that people find easy and automated programs find hard, which stops bots.", label="07.5"),

        # ---------------------------------------------------- 08 databases and SQL
        boxes("A cinema stores data about its films and showings in a relational database. Figure 8 shows the two tables. State:",
              [("the primary key of the Film table", ["FilmID"]), ("the foreign key in the Showing table", ["FilmID"])],
              figure="**Figure 8**\n\n" + FILMS[1],
              model="FilmID uniquely identifies each film, so it is the primary key of Film. Showing uses FilmID to link each showing to a film, so in Showing it is a foreign key.",
              label="08.1"),
        sql("Write an SQL query to find the Title and Year of every film in the Sci-fi genre. The newest film must be shown first.",
            FILMS, "SELECT Title, Year\nFROM Film\nWHERE Genre = 'Sci-fi'\nORDER BY Year DESC",
            [("SELECT Title, Year", "sorted(fields()) == ['title', 'year']"),
             ("FROM Film", "tables() == ['film']"),
             ("WHERE Genre = 'Sci-fi'", "same_where('Film', \"Genre = 'Sci-fi'\")"),
             ("ORDER BY Year DESC", "same_order('Film', 'Year DESC', \"Genre = 'Sci-fi'\")")],
            model="Each clause earns its own mark. DESC puts the largest year, the newest film, first.",
            wrong=["SELECT Title, Year FROM Film WHERE Genre = 'Sci-fi' ORDER BY Year",
                   "SELECT * FROM Film WHERE Genre = 'Sci-fi' ORDER BY Year DESC"],
            figure="", label="08.2"),
        sql("Write an SQL query to find the Title of the film and the StartTime of every showing on Screen 2.",
            FILMS, "SELECT Title, StartTime\nFROM Film, Showing\nWHERE Film.FilmID = Showing.FilmID\nAND Screen = 2",
            [("SELECT Title, StartTime", "sorted(fields()) == ['starttime', 'title']"),
             ("FROM Film, Showing (or a join of the two tables)", "sorted(tables()) == ['film', 'showing']"),
             ("Links the tables: Film.FilmID = Showing.FilmID", "uses(r'film\\.filmid\\s*=\\s*showing\\.filmid', r'showing\\.filmid\\s*=\\s*film\\.filmid')"),
             ("Only the showings on Screen 2", "set(r[0] for r in q('SELECT Showing.ShowID FROM Film, Showing WHERE ' + where())) == {102, 103}")],
            model="The two tables are linked by matching FilmID in each, so every showing is paired with its own film. Without that condition every showing would be paired with every film.",
            wrong=["SELECT Title, StartTime FROM Film, Showing WHERE Screen = 2",
                   "SELECT Title, StartTime FROM Film, Showing WHERE Film.FilmID = Showing.FilmID"],
            figure="", label="08.3"),
        sql("The running time of Deep Water has been corrected to 112 minutes. Write an SQL statement to update the Film table.",
            FILMS, "UPDATE Film\nSET Minutes = 112\nWHERE FilmID = 3",
            [("UPDATE Film", "uses(r'^\\s*update\\s+film\\b')"),
             ("SET Minutes = 112", "qa('SELECT Minutes FROM Film WHERE FilmID = 3') == [(112,)]"),
             ("WHERE FilmID = 3 (or Title = 'Deep Water'), so no other film changes",
              "uses(r'\\bwhere\\b') and qa('SELECT * FROM Film WHERE FilmID <> 3') == q('SELECT * FROM Film WHERE FilmID <> 3')")],
            model="Without the WHERE clause, every film's running time would be set to 112.",
            wrong=["UPDATE Film SET Minutes = 112"],
            figure="", label="08.4"),
        sql("A new showing has ShowID 106. It is a showing of Deep Water (FilmID 3) on Screen 1, starting at 19:30. Write an SQL statement to add it to the Showing table.",
            FILMS, "INSERT INTO Showing\nVALUES (106, 3, 1, '19:30')",
            [("INSERT INTO Showing", "uses(r'^\\s*insert\\s+into\\s+showing\\b')"),
             ("VALUES (106, 3, 1, '19:30'), in the order of the fields", "qa('SELECT * FROM Showing WHERE ShowID = 106') == [(106, 3, 1, '19:30')]")],
            model="The values go in the same order as the fields, ShowID, FilmID, Screen, StartTime, with the time in quotes because it is text.",
            wrong=["INSERT INTO Showing VALUES (106, 1, 3, '19:30')"],
            figure="", label="08.5"),

        # ---------------------------------------------------- 09 impacts
        write("Many people now have smart speakers with voice assistants in their homes.\n\nDiscuss the ethical, legal and environmental issues of using smart speakers.", 6, [
            ("Privacy: the speaker is always listening, and may record private conversations", ["privacy", "listening", "record", "conversation", "private", "eavesdrop"]),
            ("The company collects data about users, which may be used for targeted advertising or shared", ["advert", "target", "sold", "shared", "profile", "collect", "company"]),
            ("Legal: under the Data Protection Act 2018 personal data must be processed lawfully, kept secure and not kept too long, and users can ask to see it",
             ["data protection", "gdpr", "consent", "lawful", "secure", "request", "subject access"]),
            ("Devices could be hacked to listen in or reach the home network, an offence under the Computer Misuse Act", ["hack", "computer misuse", "unauthorised", "security", "breach"]),
            ("Benefits: they help disabled, blind or elderly people, and are convenient", ["disab", "elderly", "older", "blind", "accessib", "convenien", "independen"]),
            ("Environmental: always-on devices and the data centres behind them use energy", ["energy", "electricity", "data centre", "always on", "power", "carbon"]),
            ("Manufacturing uses mined materials, and replaced devices become e-waste", ["e-waste", "waste", "landfill", "recycl", "materials", "manufactur", "mining", "rare"]),
            ("Reaches a balanced conclusion", ["overall", "conclusion", "on balance", "however", "therefore"]),
        ], "Smart speakers are always listening for their wake word, which raises obvious privacy concerns: recordings of private conversations can be stored on the company's servers, and the data gathered about a household can be used to target advertising. Legally, the company must follow the Data Protection Act 2018, processing personal data lawfully, keeping it secure, not keeping it for longer than needed and letting users see what is held about them. Poorly secured devices could also be hacked to listen in or to reach the rest of the home network, which is an offence under the Computer Misuse Act 1990. On the other hand, voice control is a real benefit for people who are blind, disabled or elderly, helping them live independently. Environmentally, the devices are always on, and every request is processed in energy-hungry data centres; making them uses mined materials, and old devices add to e-waste. On balance smart speakers are useful, especially for accessibility, but users should review privacy settings and companies must handle the data responsibly.",
              command="Discuss", label="09"),
    ],
)

PAPERS = [AQA_1, AQA_2]
