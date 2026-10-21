"""Pearson Edexcel GCSE Computer Science 1CP2: a full length Paper 1 and Paper 2.

Modelled on the 1CP2 past papers. Paper 1, Principles of Computer Science, is
75 marks in 1 hour 30 minutes: five compulsory questions, one for each topic
area (computational thinking, data, computers, networks, issues and impact).
Paper 2, Application of Computational Thinking, is 75 marks in 2 hours on
screen: six Python 3 programs to amend, fix and write, each in its own code
file, the last four worth 15 marks each. Every program is run and marked.
"""
from mskbuild.examkit import tick, rows, ans, boxes, table, calc, write, prog
from mskbuild.models import Paper

ACC = "var(--lilac-deep)"


# ===================================================================== 1CP2/01

EDX_1 = Paper(
    slug="edexcel-1cp2-paper-1",
    title="GCSE Computer Science Paper 1: Principles of Computer Science",
    course="GCSE Computer Science", board="Pearson Edexcel", code="1CP2/01",
    minutes=90, marks=75, accent=ACC, spec="1CP2", full=True,
    blurb="A full length 1CP2/01 paper in five 15 mark questions: merge sort, binary search, truth tables and a trace table; two's complement, shifts, bitmaps and the Caesar cipher; hardware and software; networks and security; and the impacts of technology, ending with a 6 mark discussion of delivery drones.",
    calculator="You must not use a calculator.",
    instructions=["In this paper 1 kibibyte (KiB) = 1024 bytes and 1 mebibyte (MiB) = 1024 KiB, as in the specification.",
                  "There are five questions, each worth 15 marks."],
    questions=[
        # ---------------------------------------------------- 1 computational thinking
        tick("Which **one** of these describes decomposition? Tick (✓) one box.",
             ["*Breaking a problem down into smaller problems that are easier to solve", "Removing details that are not needed",
              "Repeating a set of instructions", "Putting a list of items into order"],
             "Decomposition breaks a problem into sub-problems. Removing unnecessary detail is abstraction.", label="1(a)",
             section="Question 1", section_note="Computational thinking"),
        table("A merge sort is used to put this list into ascending order.\n\n38, 15, 72, 4, 56, 23, 9, 41\n\nThe list has been split into single items. Complete the table to show the list after each stage of merging.",
              ["Stage", "1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th"],
              [["Pairs merged", "=15", "=38", "=4", "=72", "=23", "=56", "=9", "=41"],
               ["Fours merged", "=4", "=15", "=38", "=72", "=9", "=23", "=41", "=56"],
               ["Fully merged", "=4", "=9", "=15", "=23", "=38", "=41", "=56", "=72"]],
              per_row=True, numeric=True, width=4,
              model="Neighbouring single items are merged into ordered pairs: 15 38, 4 72, 23 56, 9 41. Pairs are merged into ordered fours: 4 15 38 72 and 9 23 41 56. Those two lists are merged by repeatedly taking the smaller front item: 4 9 15 23 38 41 56 72.",
              label="1(b)"),
        table("A binary search is used to find 56 in the sorted list below. The middle item is at position (first + last) // 2, where first and last are the positions of the first and last items still being searched. Complete the table to show the item checked at each comparison.",
              ["Comparison", "Item checked"], [["1", "=23"], ["2", "=41"], ["3", "=56"]], numeric=True,
              figure="| Position | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |\n|---|---|---|---|---|---|---|---|---|\n| Item | 4 | 9 | 15 | 23 | 38 | 41 | 56 | 72 |",
              model="(0 + 7) // 2 = 3: item 23. 56 is larger, so first becomes 4. (4 + 7) // 2 = 5: item 41. 56 is larger, so first becomes 6. (6 + 7) // 2 = 6: item 56, found.",
              label="1(c)"),
        table("Complete the truth table for P = (A AND NOT B) OR (B AND C).", ["A", "B", "C", "P"],
              [["0", "0", "0", "=0"], ["0", "0", "1", "=0"], ["0", "1", "0", "=0"], ["0", "1", "1", "=1"],
               ["1", "0", "0", "=1"], ["1", "0", "1", "=1"], ["1", "1", "0", "=0"], ["1", "1", "1", "=1"]],
              groups=[("Rows 1 and 2", [0, 1]), ("Rows 3 and 4", [2, 3]), ("Rows 5 and 6", [4, 5]), ("Rows 7 and 8", [6, 7])], numeric=True,
              model="A AND NOT B is 1 only when A is 1 and B is 0. B AND C is 1 only when both are 1. P is 1 when either is 1.",
              label="1(d)"),
        table("Complete the trace table for this program. The first row has been completed for you.",
              ["number", "result", "Output"], [["6", "1", ""], ["=4", "=6", ""], ["=2", "=24", ""], ["=0", "=48", "=48"]],
              groups=[("Second row", [0, 1]), ("Third row", [2, 3]), ("Fourth row", [4, 5]), ("Output", [6])], numeric=True,
              figure="```pycode\nnumber = 6\nresult = 1\nwhile number > 1:\n    result = result * number\n    number = number - 2\nprint(result)\n```",
              model="Each pass multiplies result by number, then takes 2 off number: 1 x 6 = 6, 6 x 4 = 24, 24 x 2 = 48. number is then 0, so the loop ends and 48 is printed.",
              label="1(e)"),

        # ---------------------------------------------------- 2 data
        boxes("Signed integers are stored in 8-bit two's complement. Give:",
              [("-45 in 8-bit two's complement", ["11010011"]),
               ("the denary value of the two's complement integer 1110 0110", ["-26", "−26"])],
              model="45 is 0010 1101. Inverting gives 1101 0010, and adding 1 gives 1101 0011. 1110 0110 is -128 + 64 + 32 + 4 + 2 = -26.",
              label="2(a)", section="Question 2", section_note="Data"),
        ans("Give the result of an arithmetic shift right of two places on the 8-bit two's complement integer 1011 0100.", ["11101101"],
            model="An arithmetic shift right copies the sign bit into the gap, keeping the number negative: 1110 1101. That is -76 divided by 4, -19.",
            width=10, label="2(b)"),
        write("Explain what is meant by overflow in binary addition.", 2, [
            ("The result needs more bits than are available to store it", ["more bits", "too large", "too big", "does not fit", "exceeds", "cannot be stored"]),
            ("so the extra carry bit is lost and the stored result is wrong", ["lost", "incorrect", "wrong", "discarded", "carry", "9th bit", "ninth"]),
        ], "Overflow happens when the result of an addition is too large to fit in the number of bits available, for example a result needing 9 bits in an 8-bit register. The final carry is lost, so the stored result is wrong.",
              command="Explain", label="2(c)"),
        calc("A bitmap image is 1024 pixels wide and 768 pixels high, with a colour depth of 24 bits. Calculate the file size in mebibytes (MiB). Show your working.",
             ["2.25"], 3, [
                 ("Multiplies width by height by colour depth", ["1024 x 768 x 24", "1024*768*24", "1024 × 768 × 24", "786432", "786,432", "18874368", "18,874,368"]),
                 ("Divides by 8, then by 1024 twice", ["/ 8", "/8", "÷ 8", "÷8", "2359296", "2,359,296", "/ 1024", "/1024", "÷ 1024", "÷1024", "2304"])],
             model="1024 x 768 = 786,432 pixels. 786,432 x 24 = 18,874,368 bits. / 8 = 2,359,296 bytes. / 1024 = 2304 KiB. / 1024 = 2.25 MiB.",
             unit="MiB", label="2(d)"),
        boxes("A Caesar cipher with a shift of 3 moves each letter three places along the alphabet, wrapping round from Z to A. Give:",
              [("CAB encrypted with a shift of 3", ["FDE"]), ("KHOOR decrypted with a shift of 3", ["HELLO"])],
              model="C, A, B each move three letters on: F, D, E. Moving K, H, O, O, R three letters back gives HELLO.",
              label="2(e)"),
        write("Explain the difference between lossless and lossy compression.", 2, [
            ("Lossless compression lets the original data be restored exactly, with nothing lost", ["exactly", "original", "restored", "no data lost", "nothing lost", "reconstruct"]),
            ("Lossy compression permanently removes some data, usually giving a smaller file", ["permanently", "removes", "lost", "discard", "cannot be restored", "smaller"]),
        ], "Lossless compression reduces the file size in a way that can be reversed, so the original data is restored exactly. Lossy compression permanently removes data that is judged less important, so it makes files smaller but the original can never be fully restored.",
              command="Explain", label="2(f)"),
        ans("State how many bits ASCII uses to represent each character.", "7", numeric=True,
            model="ASCII is a 7-bit code, which gives 128 characters.", width=4, label="2(g)"),
        boxes("Complete each conversion.", [("hexadecimal 3F in denary", "63"), ("1010 1100 in hexadecimal", ["AC"])],
              model="3F = 3 x 16 + 15 = 63. 1010 is A and 1100 is C: AC.", label="2(h)"),

        # ---------------------------------------------------- 3 computers
        rows("Tick (✓) one box in each row to show the utility software described.",
             ["Defragmentation", "Backup", "Compression", "Anti-malware"],
             [("Rearranges the parts of files on a hard disk so they are stored together", "Defragmentation"),
              ("Makes copies of files so they can be restored if the originals are lost", "Backup"),
              ("Reduces the size of files", "Compression"),
              ("Detects and removes malicious software", "Anti-malware")],
             model="Defragmentation reorganises, backup copies, compression shrinks and anti-malware protects.",
             label="3(a)", section="Question 3", section_note="Computers"),
        write("Describe the role of the address bus and the data bus in the von Neumann architecture.", 2, [
            ("The address bus carries the address of the memory location to be read or written, from the CPU to memory", ["address bus", "address", "location"]),
            ("The data bus carries data and instructions between the CPU and memory, in both directions", ["data bus", "both directions", "two-way", "two way", "bidirectional", "carries data"]),
        ], "The address bus carries the address of the memory location the CPU wants to use, one way, from the CPU to memory. The data bus carries the data or instruction itself between the CPU and memory, in either direction.",
              command="Describe", label="3(b)"),
        tick("Which **one** of these is an embedded system? Tick (✓) one box.",
             ["*The controller in a microwave oven", "A laptop", "A games console", "A web server"],
             "An embedded system is a computer built into another device to do one dedicated job.", label="3(c)"),
        write("Explain why a computer needs both RAM and ROM.", 2, [
            ("RAM holds the programs and data in use, and can be changed, but it is volatile", ["ram", "in use", "currently", "running", "volatile", "changed"]),
            ("ROM is non-volatile, so it keeps the start-up instructions (the boot program) when the power is off", ["rom", "non-volatile", "start", "boot", "bios", "power is off", "switched off"]),
        ], "RAM is where the programs and data currently in use are held while the computer runs, and its contents change constantly, but it is volatile. ROM is non-volatile, so it keeps the instructions needed to start the computer even when the power is off.",
              command="Explain", label="3(d)"),
        rows("Tick (✓) one box in each row to show the translator described.", ["Compiler", "Interpreter", "Assembler"],
             [("Translates the whole program into an executable file before it is run", "Compiler"),
              ("Translates and runs a high-level program one line at a time", "Interpreter"),
              ("Translates low-level mnemonics into machine code", "Assembler")],
             model="A compiler produces an executable, an interpreter works line by line, and an assembler translates assembly language mnemonics.",
             label="3(e)"),
        write("Explain **one** reason why a programmer might write part of a program in a low-level language.", 2, [
            ("Low-level code gives direct control of the hardware, such as registers and memory locations", ["direct", "hardware", "register", "memory location", "control"]),
            ("so the code can run faster and use less memory, which matters in an embedded system", ["faster", "quicker", "efficient", "less memory", "smaller", "embedded"]),
        ], "A low-level language gives the programmer direct control of the processor's registers and memory, so the code can be made to run very fast and use very little memory, which matters for device drivers and embedded systems.",
              command="Explain", label="3(f)"),
        tick("Which **one** of these is a function of an operating system? Tick (✓) one box.",
             ["*Managing the files stored on secondary storage", "Translating Python into machine code",
              "Checking the spelling in a document", "Editing photographs"],
             "File management is one of the operating system's jobs, along with memory, process, peripheral and user management.",
             label="3(g)"),

        # ---------------------------------------------------- 4 networks
        tick("Which **one** of these is a characteristic of a wide area network (WAN)? Tick (✓) one box.",
             ["*It covers a large geographical area", "It is always owned by one organisation",
              "It connects devices in a single building", "It never uses the internet"],
             "A WAN connects networks over a large area, often using infrastructure owned by other companies.",
             label="4(a)", section="Question 4", section_note="Networks"),
        write("Explain **one** advantage and **one** disadvantage of a star topology.", 2, [
            ("Advantage: if one cable or device fails, the rest of the network keeps working", ["one cable", "one device", "rest of the network", "still work", "keeps working", "unaffected", "easy to add"]),
            ("Disadvantage: if the central switch fails the whole network fails, and it needs a lot of cable", ["switch fails", "central", "whole network", "lot of cable", "more cable", "expensive", "cost"]),
        ], "Each device has its own cable to the central switch, so if one cable fails only that device is affected. But everything depends on the switch: if it fails, the whole network goes down, and all that cable makes it expensive to install.",
              command="Explain", label="4(b)"),
        rows("Tick (✓) one box in each row to show the protocol described.", ["POP3", "SMTP", "HTTPS", "FTP"],
             [("Downloads emails from a server, usually deleting them from it", "POP3"), ("Sends emails", "SMTP"),
              ("Transfers web pages securely", "HTTPS"), ("Transfers files between computers", "FTP")],
             model="POP3 downloads mail, SMTP sends it, HTTPS is secure web traffic and FTP transfers files.",
             label="4(c)"),
        rows("Tick (✓) one box in each row to show the layer of the TCP/IP model at which each protocol works.",
             ["Application", "Transport", "Internet", "Link"],
             [("HTTP", "Application"), ("TCP", "Transport"), ("IP", "Internet"), ("Ethernet", "Link")],
             marks=2, model="HTTP is an application protocol, TCP works at the transport layer, IP at the internet layer and Ethernet at the link layer.",
             label="4(d)"),
        write("Explain how a firewall protects a network.", 2, [
            ("It checks the data (packets) coming into and going out of the network", ["check", "monitor", "incoming", "outgoing", "traffic", "packets", "inspect", "filter"]),
            ("against a set of rules, blocking anything that is not allowed", ["rules", "block", "unauthorised", "not allowed", "prevent", "deny", "reject"]),
        ], "A firewall inspects every packet entering or leaving the network and compares it against a set of rules, blocking any traffic that is not allowed, such as connections from unknown addresses or to unauthorised ports.",
              command="Explain", label="4(e)"),
        write("Describe what is meant by a phishing attack, and give **one** way of protecting against it.", 2, [
            ("Emails or messages that pretend to come from a trusted organisation, to trick people into giving personal details or clicking a malicious link",
             ["pretend", "fake", "trusted", "trick", "personal details", "password", "link", "bank"]),
            ("Protection: training users to spot suspicious messages, email filtering, or checking the sender and links", ["training", "educat", "filter", "spam", "check the sender", "do not click", "hover", "verify"]),
        ], "Phishing is sending emails or texts that pretend to come from a trusted organisation, such as a bank, to trick people into clicking a link or giving away personal details. Staff can be trained to recognise suspicious messages, and email filters can block many of them.",
              command="Describe", label="4(f)"),
        tick("Which **two** of these are advantages of a wired connection compared with a wireless one? Tick (✓) two boxes.",
             ["*It usually transfers data faster", "*It is less affected by interference", "Devices can be moved around freely", "No cables need to be installed"],
             "Cables give faster, more reliable connections. Freedom to move and no cabling are advantages of wireless.", label="4(g)"),

        # ---------------------------------------------------- 5 issues and impact
        rows("Tick (✓) one box in each row to show the law that has most likely been broken.",
             ["Computer Misuse Act 1990", "Data Protection Act 2018", "Copyright, Designs and Patents Act 1988"],
             [("A company sells its customers' email addresses without their consent", "Data Protection Act 2018"),
              ("A student uploads a film to a website without permission", "Copyright, Designs and Patents Act 1988"),
              ("A hacker guesses a teacher's password and changes students' grades", "Computer Misuse Act 1990")],
             model="Misusing personal data breaks data protection law, sharing a film breaks copyright, and unauthorised access to change data breaks the Computer Misuse Act.",
             label="5(a)", section="Question 5", section_note="Issues and impact"),
        write("A small business is choosing an office suite. Explain **one** benefit and **one** drawback of choosing open-source software.", 2, [
            ("Benefit: it is usually free, and the code can be changed to suit the business", ["free", "no cost", "cheaper", "no licence", "modify", "change", "adapt", "customise"]),
            ("Drawback: there may be no official support, or fewer features and less compatibility", ["support", "help", "no one to", "features", "compatib", "bugs", "updates"]),
        ], "Open-source software is usually free, which saves the business money, and its source code can be modified to suit its needs. However, there is often no official support line, so the business may struggle to get help when something goes wrong.",
              command="Explain", label="5(b)"),
        write("Describe what is meant by machine learning.", 2, [
            ("A computer program improves its performance at a task by learning from data", ["learn", "data", "experience", "improve", "training"]),
            ("It finds patterns itself, rather than being explicitly programmed with rules", ["without being", "explicitly", "pattern", "not programmed", "rules", "itself"]),
        ], "Machine learning is a type of artificial intelligence in which a program improves at a task by being trained on data: it finds the patterns itself instead of being explicitly programmed with rules.",
              command="Describe", label="5(c)"),
        write("Explain how algorithmic bias can occur in an artificial intelligence system.", 2, [
            ("The system is trained on data that is unrepresentative or reflects past prejudice", ["training data", "trained on", "unrepresentative", "biased data", "historical", "not representative", "past decisions"]),
            ("so its decisions unfairly favour or disadvantage some groups of people", ["unfair", "discriminat", "disadvantage", "favour", "groups", "certain people"]),
        ], "An AI system learns from the data it is trained on. If that data is unrepresentative, or reflects unfair decisions made in the past, the system learns the same patterns, so its decisions unfairly favour some groups of people over others.",
              command="Explain", label="5(d)"),
        write("An online retailer plans to deliver parcels using drones.\n\nDiscuss the environmental, ethical and legal issues of this plan.", 6, [
            ("Environmental benefit: battery drones use less fuel and produce fewer emissions than vans", ["emission", "fuel", "pollution", "carbon", "electric", "van"]),
            ("Environmental cost: making and charging drones and their batteries uses resources and energy, creating e-waste", ["battery", "batteries", "energy", "e-waste", "manufactur", "materials", "charging"]),
            ("Noise and disturbance to people and wildlife", ["noise", "wildlife", "birds", "disturb", "animals"]),
            ("Delivery drivers may lose their jobs", ["job", "driver", "unemploy", "redundan"]),
            ("Drones with cameras raise privacy concerns as they fly over homes and gardens", ["privacy", "camera", "filming", "surveillance", "spy", "gardens"]),
            ("Legal: personal data such as addresses and camera footage must be handled under the Data Protection Act; flights must follow aviation rules",
             ["data protection", "personal data", "aviation", "regulation", "law", "licence", "airspace", "caa"]),
            ("Safety and liability: who is responsible if a drone crashes or injures someone", ["crash", "injur", "safety", "liab", "responsib", "accident", "fall"]),
            ("Reaches a balanced conclusion", ["overall", "conclusion", "on balance", "however", "therefore"]),
        ], "Drone delivery could cut emissions, because small battery drones use far less energy per parcel than delivery vans, and they keep vans off congested roads. But the drones and their batteries must be manufactured from mined materials, charged and eventually disposed of, and hundreds of drones overhead would add noise that disturbs people and wildlife. Ethically, delivery drivers could lose their jobs, and drones carrying cameras raise privacy concerns as they fly over homes and gardens. Legally, the retailer must handle customers' addresses and any camera footage under the Data Protection Act 2018, and flights must follow aviation regulations about where and how high drones may fly. It must also be clear who is liable if a drone crashes and injures someone. On balance drones may suit light parcels in rural areas, but only with strict rules on safety, noise and privacy.",
              command="Discuss", label="5(e)"),
    ],
)


# ===================================================================== 1CP2/02

Q1_START = '''# Convert a temperature from Celsius to Fahrenheit

# -----------------------------------------------------------------
# Global variables
# -----------------------------------------------------------------
celsius = 0.0
fahrenheit = 0.0

# -----------------------------------------------------------------
# Main program
# -----------------------------------------------------------------

# =====> Take a temperature in Celsius as a real number input from the user


# =====> Convert the temperature to Fahrenheit, using F = C x 9 / 5 + 32


# =====> Display the temperature in Fahrenheit, with a message


# =====> Display Freezing if the temperature is 0 Celsius or below

'''

Q1 = '''# Convert a temperature from Celsius to Fahrenheit

celsius = 0.0
fahrenheit = 0.0

celsius = float(input("Enter a temperature in Celsius: "))
fahrenheit = celsius * 9 / 5 + 32
print("The temperature in Fahrenheit is", fahrenheit)
if celsius <= 0:
    print("Freezing")
'''

Q2_START = '''# Grade the test marks of five students and count how many passed

passed = 0

for student in range(1, 5):
    mark = int(input("Enter a mark out of 50: "))
    if (mark < 0) and (mark > 50):
        print("Invalid mark")
    elif (mark > 40):
        print("Distinction")
        passed = passed + 1
    elif (mark >= 30):
        print("Merit")
        passed = passed + 1
    elif (mark >= 20):
        print("Merit")
        passed = passed + 1
    else:
        print("Fail")

print("Number passed:", passed)
'''

Q2 = (Q2_START.replace("range(1, 5)", "range(5)").replace("(mark < 0) and (mark > 50)", "(mark < 0) or (mark > 50)")
      .replace("(mark > 40)", "(mark >= 40)").replace('''    elif (mark >= 20):
        print("Merit")''', '''    elif (mark >= 20):
        print("Pass")'''))

Q3_START = '''# Weekly rainfall report

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
rainfall = []

# =====> Write your program here
'''

Q3 = '''# Weekly rainfall report

days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
rainfall = []

for day in days:
    reading = float(input("Rainfall on " + day + " in mm: "))
    while reading < 0:
        print("Rainfall cannot be negative")
        reading = float(input("Rainfall on " + day + " in mm: "))
    rainfall.append(reading)

total = 0.0
highest = rainfall[0]
highestDay = days[0]
dryDays = 0
for index in range(len(rainfall)):
    total = total + rainfall[index]
    if rainfall[index] > highest:
        highest = rainfall[index]
        highestDay = days[index]
    if rainfall[index] == 0:
        dryDays = dryDays + 1
average = round(total / len(rainfall), 1)

print("Total:", total, "mm")
print("Average:", average, "mm")
print("Highest:", highest, "mm on", highestDay)
print("Dry days:", dryDays)
if total > 50:
    print("Wet week")
else:
    print("Dry week")
'''

R1 = ['0', '12.5', '3', '0', '20', '8.5', '0']          # total 44.0, average 6.3, highest 20 on Friday, 3 dry days
R2 = ['15', '2', '9.5', '11', '0', '7', '18']           # total 62.5, average 8.9, highest 18 on Sunday, 1 dry day
R3 = ['30', '1', '1', '1', '1', '1', '1']               # highest on Monday, no dry days
R4 = ['-4', '5', '6', '5', '5', '5', '5', '5']          # one rejected reading: total 36
R5 = ['-1', '-2', '5', '6', '5', '5', '5', '5', '5']    # two rejected readings in a row: total 36
R6 = ['10', '10', '10', '10', '10', '0', '0']           # total exactly 50


def labelled(inputs, label, files=None):
    """The numbers on the output lines that contain a label."""
    if files is None:
        return "sum([nums(l) for l in lines(run(%r)) if has(l, %r)], [])" % (inputs, label)
    return "sum([nums(l) for l in lines(run(%r, %r)) if has(l, %r)], [])" % (inputs, files, label)


def says(inputs, label, word, files=None):
    """Some output line containing the label also contains the word."""
    run = "run(%r)" % (inputs,) if files is None else "run(%r, %r)" % (inputs, files)
    return "any(has(l, %r) for l in lines(%s) if has(l, %r))" % (word, run, label)


Q4 = '''# Caesar cipher

choice = input("Encrypt or decrypt (E/D)? ").upper()
while choice != "E" and choice != "D":
    choice = input("Please enter E or D: ").upper()

message = input("Enter the message: ")

shift = int(input("Enter a shift from 1 to 25: "))
while shift < 1 or shift > 25:
    shift = int(input("The shift must be from 1 to 25: "))

if choice == "D":
    shift = -shift

result = ""
for character in message:
    if "A" <= character <= "Z":
        result = result + chr((ord(character) - ord("A") + shift) % 26 + ord("A"))
    elif "a" <= character <= "z":
        result = result + chr((ord(character) - ord("a") + shift) % 26 + ord("a"))
    else:
        result = result + character

print("Result:", result)
'''

MEMBERS = "Asha,34,12\nBen,19,3\nCara,45,20\nDev,27,0\nEmi,52,4\nFinn,38,9\n"
M2 = {"members.txt": "Zak,61,1\nYara,23,15\nXena,30,14\nWill,44,7\n"}
M3 = {"members.txt": "Omar,29,30\nPia,33,6\nQuin,41,5\n"}
M4 = {"members.txt": "Gus,20,9\nHal,21,10\n"}
M1 = {"members.txt": MEMBERS}

Q5_START = '''# Gym members report
# Each line of members.txt holds a member's name, age and number of visits this month

# =====> Write your program here
'''

Q5 = '''# Gym members report

count = 0
totalAge = 0
mostVisits = -1
mostName = ""
written = 0

reminders = open("reminders.txt", "w")
members = open("members.txt", "r")
for line in members:
    parts = line.strip().split(",")
    name = parts[0]
    age = int(parts[1])
    visits = int(parts[2])
    count = count + 1
    totalAge = totalAge + age
    if visits > mostVisits:
        mostVisits = visits
        mostName = name
    if visits < 5:
        reminders.write(name + "\\n")
        written = written + 1
members.close()
reminders.close()

print("Members:", count)
print("Most visits:", mostName)
print("Average age:", round(totalAge / count, 1))
print("Reminders written:", written)
'''

RESULTS = '''results = [
    ["Ava", "Red", 14.2],
    ["Ben", "Blue", 13.8],
    ["Cal", "Green", 15.1],
    ["Dee", "Red", 13.5],
    ["Eli", "Blue", 14.9],
    ["Fay", "Green", 13.9]
]
'''
RES = [["Ava", "Red", 14.2], ["Ben", "Blue", 13.8], ["Cal", "Green", 15.1],
       ["Dee", "Red", 13.5], ["Eli", "Blue", 14.9], ["Fay", "Green", 13.9]]

Q6_START = '''# Sports day results
# Each record holds a runner's name, house and time in seconds

''' + RESULTS + '''
# -----------------------------------------------------------------
# Subprograms
# -----------------------------------------------------------------

def fastest(records):
    # =====> Return the name of the runner with the lowest time
    pass


def houseCount(records, house):
    # =====> Return the number of runners in the given house
    pass


def averageTime(records, house):
    # =====> Return the average time of the runners in the given house,
    # rounded to 2 decimal places. Return 0 if the house has no runners.
    pass


def points(position):
    # =====> Return the points for a finishing position:
    # 1st 10, 2nd 8, 3rd 6, 4th to 6th 3, any other position 0
    pass


# -----------------------------------------------------------------
# Main program
# -----------------------------------------------------------------
# =====> Display the name of the fastest runner, then the average time for each house
'''

Q6 = '''# Sports day results
# Each record holds a runner's name, house and time in seconds

''' + RESULTS + '''

def fastest(records):
    best = records[0]
    for record in records:
        if record[2] < best[2]:
            best = record
    return best[0]


def houseCount(records, house):
    count = 0
    for record in records:
        if record[1] == house:
            count = count + 1
    return count


def averageTime(records, house):
    if houseCount(records, house) == 0:
        return 0
    total = 0
    for record in records:
        if record[1] == house:
            total = total + record[2]
    return round(total / houseCount(records, house), 2)


def points(position):
    if position == 1:
        return 10
    elif position == 2:
        return 8
    elif position == 3:
        return 6
    elif position >= 4 and position <= 6:
        return 3
    else:
        return 0


print("Fastest runner:", fastest(results))
for house in ["Red", "Blue", "Green"]:
    print(house, "average time:", averageTime(results, house))
'''

EDX_2 = Paper(
    slug="edexcel-1cp2-paper-2",
    title="GCSE Computer Science Paper 2: Application of Computational Thinking",
    course="GCSE Computer Science", board="Pearson Edexcel", code="1CP2/02",
    minutes=120, marks=75, accent=ACC, spec="1CP2", full=True,
    blurb="A full length 1CP2/02 onscreen paper in Python 3: complete a temperature converter, fix the logic errors in a grading program, then write a rainfall report, a Caesar cipher, a gym report that reads and writes files, and the subprograms for a sports day.",
    calculator="You do not need a calculator.",
    instructions=["Each question gives you a Python 3 file to amend; use the Run button to test it."],
    questions=[
        prog("Open **Q01.py**. The program converts a temperature from Celsius to Fahrenheit.\n\nAmend the code to:\n\n- take a temperature in Celsius as a real number input\n- convert it to Fahrenheit, using F = C x 9 / 5 + 32\n- display the temperature in Fahrenheit, with a message\n- display Freezing if the temperature is 0 Celsius or below.",
             Q1_START, Q1,
             [("Takes the temperature as an input", "uses(r'input\\s*\\(')"),
              ("Converts the input to a real number, so 21.5 is accepted", "len(run(['21.5'])) > 0"),
              ("Converts correctly: 100 Celsius is 212 Fahrenheit", "212 in nums(run(['100']))"),
              ("Converts correctly with a fraction: 21.5 Celsius is 70.7 Fahrenheit", "any(abs(n - 70.7) < 0.01 for n in nums(run(['21.5'])))"),
              ("Displays the Fahrenheit temperature with a message", "any(c.isalpha() for c in lines(run(['100']))[0])"),
              ("Displays Freezing for 0 Celsius and below", "has(run(['0']), 'freezing') and has(run(['-5']), 'freezing')"),
              ("Does not display Freezing above 0 Celsius", "not has(run(['0.5']), 'freezing') and not has(run(['20']), 'freezing')")],
             model="float() accepts a real number. The condition uses <= so that exactly 0 counts as freezing.",
             wrong=[Q1.replace("celsius <= 0", "celsius < 0"), Q1.replace("float(", "int(")],
             label="1", filename="Q01.py"),
        prog("Open **Q02.py**. The program should grade the test marks of **five** students and then display how many passed. The grades are:\n\n- a mark below 0 or above 50: Invalid mark\n- 40 to 50: Distinction\n- 30 to 39: Merit\n- 20 to 29: Pass\n- below 20: Fail\n\nA student passes with a Pass, Merit or Distinction. The code contains **logic errors**. Amend the code to fix them.",
             Q2_START, Q2,
             [("Grades five students", "len([l for l in lines(run(['45', '35', '25', '15', '5'])) if not has(l, 'passed')]) == 5"),
              ("Displays Invalid mark for a mark below 0", "has(lines(run(['-1', '10', '10', '10', '10']))[0], 'invalid')"),
              ("Displays Invalid mark for a mark above 50", "has(lines(run(['51', '10', '10', '10', '10']))[0], 'invalid')"),
              ("Gives a Distinction for exactly 40", "has(lines(run(['40', '10', '10', '10', '10']))[0], 'distinction')"),
              ("Gives a Pass, not a Merit, for 20 to 29", "has(lines(run(['25', '10', '10', '10', '10']))[0], 'pass') and not has(lines(run(['25', '10', '10', '10', '10']))[0], 'merit')"),
              ("Still gives Merit for 30 to 39 and Fail below 20", "has(lines(run(['30', '19', '10', '10', '10']))[0], 'merit') and has(lines(run(['30', '19', '10', '10', '10']))[1], 'fail')"),
              ("Counts the passes: 3 for 45, 35, 25, 15 and 5", "nums(lines(run(['45', '35', '25', '15', '5']))[-1]) == [3]"),
              ("Does not count an invalid mark as a pass", "nums(lines(run(['60', '-3', '45', '10', '10']))[-1]) == [1]")],
             model="Four fixes: range(5) grades five students, or replaces and because no mark is both below 0 and above 50, >= 40 includes 40, and the third grade is Pass.",
             wrong=[Q2.replace("range(5)", "range(1, 5)"), Q2.replace("(mark >= 40)", "(mark > 40)"),
                    Q2.replace("(mark < 0) or (mark > 50)", "(mark < 0) and (mark > 50)")],
             label="2", filename="Q02.py"),
        prog("Open **Q03.py**. A weather station records the rainfall in millimetres each day for a week.\n\nWrite a program that:\n\n- takes the rainfall for each of the seven days as a real number input\n- rejects a negative reading and keeps asking until the reading is valid\n- stores the readings in the list rainfall\n- displays the total rainfall and the average daily rainfall, rounded to 1 decimal place\n- displays the highest daily rainfall and the day it fell on\n- displays the number of dry days, days with 0 mm of rain\n- displays Wet week if the total is more than 50 mm, otherwise Dry week.\n\nYour output must follow the format of the example below.",
             Q3_START, Q3,
             [("Takes seven readings as real numbers: total 62.5 for the second week", "62.5 in " + labelled(R2, 'total')),
              ("Accepts a reading of 0: total 44.0 for the example", "44 in " + labelled(R1, 'total')),
              ("Rejects a negative reading", "36 in " + labelled(R4, 'total')),
              ("Keeps asking until the reading is valid", "36 in " + labelled(R5, 'total')),
              ("Displays the average rounded to 1 decimal place: 6.3", "6.3 in " + labelled(R1, 'average')),
              ("Displays the correct average for other readings: 8.9", "8.9 in " + labelled(R2, 'average')),
              ("Displays the highest rainfall: 20.0", "20 in " + labelled(R1, 'highest')),
              ("Displays the day of the highest rainfall: Friday", says(R1, 'highest', 'friday')),
              ("Finds the highest when it falls on the last day", "18 in %s and %s" % (labelled(R2, 'highest'), says(R2, 'highest', 'sunday'))),
              ("Finds the highest when it falls on the first day", "30 in %s and %s" % (labelled(R3, 'highest'), says(R3, 'highest', 'monday'))),
              ("Counts the dry days: 3", "3 in " + labelled(R1, 'dry days')),
              ("Counts no dry days when every day had rain", "0 in " + labelled(R3, 'dry days')),
              ("Displays Wet week when the total is more than 50 mm", "has(run(%r), 'wet week')" % (R2,)),
              ("Displays Dry week when the total is exactly 50 mm", "has(run(%r), 'dry week') and not has(run(%r), 'wet week')" % (R6, R6)),
              ("Displays the four results in the order and format shown",
               "[l.split(':')[0].strip().lower() for l in lines(run(%r))[:4]] == ['total', 'average', 'highest', 'dry days']" % (R1,))],
             model="Validate each reading with a while loop before appending it. One pass through the list can then add up the total, track the highest reading and its day, and count the zeros.",
             wrong=[Q3.replace("    while reading < 0:\n        print(\"Rainfall cannot be negative\")\n        reading",
                               "    if reading < 0:\n        print(\"Rainfall cannot be negative\")\n        reading"),
                    Q3.replace("if total > 50:", "if total >= 50:"),
                    Q3.replace("average = round(total / len(rainfall), 1)", "average = total / len(rainfall)")],
             label="3", filename="Q03.py",
             figure="**Example output** for the readings 0, 12.5, 3, 0, 20, 8.5 and 0\n\n```text\nTotal: 44.0 mm\nAverage: 6.3 mm\nHighest: 20.0 mm on Friday\nDry days: 3\nDry week\n```"),
        prog("Open **Q04.py**. A Caesar cipher replaces each letter with the letter a fixed number of places further along the alphabet, wrapping round from Z to A.\n\nWrite a program that:\n\n- asks whether to encrypt or decrypt, and keeps asking until E or D is entered, in either case\n- asks for the message\n- asks for the shift, and keeps asking until it is a whole number from 1 to 25\n- encrypts or decrypts the message: letters keep their case, and every other character, such as a space, a digit or punctuation, is left unchanged\n- displays the result.\n\nFor example, encrypting Hello World with a shift of 3 gives Khoor Zruog.",
             "# Caesar cipher\n\n# =====> Write your program here\n", Q4,
             [("Encrypts a lower case message", "'khoor' in run(['E', 'hello', '3'])"),
              ("Keeps upper case letters in upper case", "'KHOOR' in run(['E', 'HELLO', '3'])"),
              ("Wraps round from z to a", "'abc' in run(['E', 'xyz', '3'])"),
              ("Wraps round from Z to A", "'ABC' in run(['E', 'XYZ', '3'])"),
              ("Keeps the case of each letter in a mixed message", "'Mjqqt Btwqi' in run(['E', 'Hello World', '5'])"),
              ("Leaves spaces unchanged", "'ij uifsf' in run(['E', 'hi there', '1'])"),
              ("Leaves digits and punctuation unchanged", "'Tqqo 101!' in run(['E', 'Room 101!', '2'])"),
              ("Decrypts a message", "'hello' in run(['D', 'khoor', '3'])"),
              ("Decrypts with wrapping round from a to z", "'xyz' in run(['D', 'abc', '3'])"),
              ("Accepts e or d in lower case", "'bcd' in run(['e', 'abc', '1']) and 'abc' in run(['d', 'bcd', '1'])"),
              ("Keeps asking until E or D is entered", "'bcd' in run(['X', 'Q', 'E', 'abc', '1'])"),
              ("Rejects a shift of 0 and asks again", "'bcd' in run(['E', 'abc', '0', '1'])"),
              ("Rejects a shift of 26 and asks again", "'cde' in run(['E', 'abc', '26', '2'])"),
              ("Accepts a shift of 25", "'zab' in run(['E', 'abc', '25'])"),
              ("Keeps asking until the shift is valid, however many times", "'bcd' in run(['E', 'abc', '30', '-1', '0', '1'])")],
             model="ord() and chr() convert between letters and codes. Taking the position in the alphabet, adding the shift and using % 26 wraps round in both directions; decrypting is encrypting with the shift made negative.",
             wrong=[Q4.replace("% 26 + ord(\"A\")", "+ ord(\"A\")").replace("% 26 + ord(\"a\")", "+ ord(\"a\")"),
                    Q4.replace("shift < 1 or shift > 25", "shift < 0 or shift > 26"),
                    Q4.replace('    else:\n        result = result + character\n', ''),
                    Q4.replace('choice = input("Encrypt or decrypt (E/D)? ").upper()', 'choice = input("Encrypt or decrypt (E/D)? ")')],
             label="4", filename="Q04.py"),
        prog("Open **Q05.py**. Each line of the text file **members.txt** holds a gym member's name, age and number of visits this month, separated by commas, as shown below.\n\nWrite a program that reads the file and:\n\n- displays the number of members\n- displays the name of the member with the most visits\n- displays the average age of the members, rounded to 1 decimal place\n- writes the name of every member with fewer than 5 visits to a new file, reminders.txt, one name per line. The file must be created even if no names are written.\n- displays how many names were written.\n\nYour output must follow the format of the example below.",
             Q5_START, Q5,
             [("Reads every line of the file: 6 members", "6 in " + labelled([], 'members', M1)),
              ("Counts the members in a different file: 4", "4 in " + labelled([], 'members', M2)),
              ("Finds the member with the most visits: Cara", says([], 'most', 'cara', M1)),
              ("Finds the most visits when it is a later member: Yara", says([], 'most', 'yara', M2)),
              ("Finds the most visits when it is the first member: Omar", says([], 'most', 'omar', M3)),
              ("Compares visits as numbers, not as text: 10 is more than 9", says([], 'most', 'hal', M4)),
              ("Calculates the average age: 35.8", "35.8 in " + labelled([], 'average', M1)),
              ("Rounds the average age to 1 decimal place: 34.3", "34.3 in " + labelled([], 'average', M3)),
              ("Creates the file reminders.txt", "read('reminders.txt', [], %r) is not None" % (M1,)),
              ("Writes every member with fewer than 5 visits", "set(lines(read('reminders.txt', [], %r))) >= {'Ben', 'Dev', 'Emi'}" % (M1,)),
              ("Writes no member with 5 or more visits, so Quin, with exactly 5, is left out", "lines(read('reminders.txt', [], %r)) == []" % (M3,)),
              ("Writes one name per line, with nothing else", "lines(read('reminders.txt', [], %r)) == ['Ben', 'Dev', 'Emi']" % (M1,)),
              ("Displays how many names were written: 3", "3 in " + labelled([], 'reminders', M1)),
              ("Displays the count for a different file: 1", "1 in " + labelled([], 'reminders', M2)),
              ("Displays the results in the order and format shown",
               "[l.split(':')[0].strip().lower() for l in lines(run([], %r))] == ['members', 'most visits', 'average age', 'reminders written']" % (M1,))],
             model="Read the file a line at a time, strip the newline and split on commas, converting the age and visits to integers so they compare as numbers. Open reminders.txt for writing before the loop, so it is created even when nothing is written.",
             wrong=[Q5.replace("mostVisits = -1", 'mostVisits = ""').replace("visits = int(parts[2])", "visits = parts[2]").replace("visits < 5", "int(visits) < 5"),
                    Q5.replace("visits < 5", "visits <= 5"),
                    Q5.replace('reminders.write(name + "\\n")', 'reminders.write(name)')],
             files=M1, label="5", filename="Q05.py",
             figure="**members.txt**\n\n```text\n" + MEMBERS + "```\n\n**Example output** for this file\n\n```text\nMembers: 6\nMost visits: Cara\nAverage age: 35.8\nReminders written: 3\n```"),
        prog("Open **Q06.py**. The results of a race on sports day are stored in a two-dimensional list. Each record holds a runner's name, house and time in seconds.\n\nComplete the subprograms fastest, houseCount, averageTime and points, following the comments in the code. Then complete the main program so that it displays the name of the fastest runner, then the average time for each of the houses Red, Blue and Green, using the subprograms.",
             Q6_START, Q6,
             [("fastest returns Dee for the results given", "call('fastest', %r) == 'Dee'" % (RES,)),
              ("fastest works when the fastest runner is first", "call('fastest', [['Al', 'Red', 10.0], ['Bo', 'Red', 11.0]]) == 'Al'"),
              ("fastest works when the fastest runner is last", "call('fastest', [['Al', 'Red', 12.5], ['Bo', 'Blue', 12.4]]) == 'Bo'"),
              ("houseCount returns 2 for Red", "call('houseCount', %r, 'Red') == 2" % (RES,)),
              ("houseCount returns 0 for a house with no runners", "call('houseCount', %r, 'Yellow') == 0" % (RES,)),
              ("averageTime returns 13.85 for Red", "abs(call('averageTime', %r, 'Red') - 13.85) < 0.001" % (RES,)),
              ("averageTime returns 14.35 for Blue", "abs(call('averageTime', %r, 'Blue') - 14.35) < 0.001" % (RES,)),
              ("averageTime rounds to 2 decimal places", "call('averageTime', [['Al', 'Red', 10.0], ['Bo', 'Red', 10.0], ['Cy', 'Red', 10.1]], 'Red') == 10.03"),
              ("averageTime returns 0 for a house with no runners", "call('averageTime', %r, 'Yellow') == 0" % (RES,)),
              ("points gives 10, 8 and 6 for the first three places", "[call('points', p) for p in (1, 2, 3)] == [10, 8, 6]"),
              ("points gives 3 for 4th, 5th and 6th place", "[call('points', p) for p in (4, 5, 6)] == [3, 3, 3]"),
              ("points gives 0 for any other position", "call('points', 7) == 0 and call('points', 0) == 0"),
              ("The main program displays the fastest runner", "has(run([]), 'dee')"),
              ("The main program displays the average time for each house", "all(any(abs(n - x) < 0.001 for n in nums(run([]))) for x in (13.85, 14.35, 14.5))"),
              ("The main program uses the subprograms rather than repeating their code", "src.count('fastest(') >= 2 and src.count('averageTime(') >= 2")],
             model="Each subprogram loops through the records once. averageTime checks for an empty house first, so it never divides by zero, and rounds only the final answer.",
             wrong=[Q6.replace("if record[2] < best[2]:", "if record[2] > best[2]:"),
                    Q6.replace("    if houseCount(records, house) == 0:\n        return 0\n", ""),
                    Q6.replace("elif position >= 4 and position <= 6:", "elif position >= 4:")],
             label="6", filename="Q06.py"),
    ],
)

PAPERS = [EDX_1, EDX_2]
