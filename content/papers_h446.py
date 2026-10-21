"""OCR A Level Computer Science H446: a second full length Paper 1 and Paper 2.

Modelled on the H446 past papers: 140 marks in 2 hours 30 minutes each.
Paper 1, Computer systems, mixes short answers, tables, binary and floating
point working, Boolean algebra and SQL with a 9 mark and a 12 mark extended
response. Paper 2, Algorithms and programming, has a Section A of traditional
questions and a Section B built on one scenario, a word game, in which the
programs are written in Python so they can be run and marked.
"""
from mskbuild.examkit import tick, rows, ans, boxes, table, calc, write, prog, db, sql
from mskbuild.models import Paper

ACC = "var(--deep)"


def T(code, expected):
    """A check that runs test code after the program and compares its result."""
    return "test(%r) == %r" % (code, expected)


# ===================================================================== H446/01

VET = db(
    ("Owner", ["OwnerID INTEGER", "Surname TEXT", "Phone TEXT"],
     [(10, "Patel", "01632 960101"), (11, "Okafor", "01632 960245"), (12, "Byrne", "01632 960377"), (13, "Novak", "01632 960412")]),
    ("Pet", ["PetID INTEGER", "Name TEXT", "Species TEXT", "OwnerID INTEGER"],
     [(1, "Biscuit", "Dog", 12), (2, "Luna", "Cat", 10), (3, "Thumper", "Rabbit", 11), (4, "Ziggy", "Dog", 12),
      (5, "Clover", "Rabbit", 13), (6, "Mochi", "Cat", 12), (7, "Pepper", "Rabbit", 10)]),
    ("Visit", ["VisitID INTEGER", "PetID INTEGER", "Cost REAL"],
     [(101, 1, 45.0), (102, 2, 18.5), (103, 4, 120.0), (104, 3, 15.0), (105, 6, 32.0), (106, 1, 19.99),
      (107, 7, 60.0), (108, 5, 20.0)]),
)

KMAP4 = """**Figure 2**: a Karnaugh map. AB labels the rows and CD the columns.

| AB \\\\ CD | 00 | 01 | 11 | 10 |
|---|---|---|---|---|
| **00** | 0 | 1 | 0 | 0 |
| **01** | 0 | 1 | 0 | 0 |
| **11** | 1 | 1 | 1 | 1 |
| **10** | 0 | 1 | 0 | 0 |"""

LINKED = """**Figure 1**: a linked list held in an array. The start pointer is 1, the next free position is 5, and -1 marks the end of the list.

| Index | Data | Next |
|---|---|---|
| 0 | Kiwi | 4 |
| 1 | Apple | 3 |
| 2 | Fig | 0 |
| 3 | Banana | 2 |
| 4 | Mango | -1 |
| 5 | | |"""

H446_1B = Paper(
    slug="h446-paper-1-b",
    title="A Level Computer Science Paper 1 B: Computer Systems",
    course="A Level Computer Science", board="OCR", code="H446/01",
    minutes=150, marks=140, accent=ACC, spec="H446", full=True,
    blurb="A full length H446/01 paper: registers, pipelining and GPUs; scheduling, paging and interrupts; compilation, linking and development methodologies with a 9 mark evaluation; two's complement and floating point; stacks, trees, hash tables and linked lists; Karnaugh maps and adders; SQL run against a vet's database; networks and the web; and a 12 mark discussion of live facial recognition.",
    calculator="You must not use a calculator.",
    instructions=["The 9 and 12 mark questions earn a mark for each relevant point here; the real exam marks them in levels.",
                  "SQL answers are run against the tables printed in question 7, so they must be valid SQL."],
    questions=[
        # ---------------------------------------------------- 1 processors
        rows("Tick (✓) one box in each row to identify the register described.", ["PC", "MAR", "MDR", "CIR"],
             [("Holds the address of the next instruction to be fetched", "PC"),
              ("Holds the address of the memory location about to be read from or written to", "MAR"),
              ("Holds the data or instruction just fetched from memory, or about to be written to it", "MDR"),
              ("Holds the instruction that is currently being decoded and executed", "CIR")],
             model="The program counter points to the next instruction, the MAR holds an address, the MDR holds what travels on the data bus, and the CIR holds the instruction being worked on.",
             label="1(a)"),
        write("Describe how pipelining improves the performance of a processor, and explain why a conditional branch instruction can reduce the benefit.", 4, [
            ("The fetch, decode and execute stages of different instructions overlap", ["overlap", "at the same time", "simultaneous", "while one", "different stages"]),
            ("So the parts of the processor are not left idle and more instructions are completed each second", ["idle", "throughput", "more instructions", "per second", "every clock cycle", "faster"]),
            ("After a branch, the instructions already fetched and decoded may not be the ones that run next", ["wrong instruction", "already fetched", "not needed", "not the next", "jump", "branch"]),
            ("So the pipeline has to be flushed and refilled, wasting clock cycles", ["flush", "emptied", "refill", "wasted", "cleared", "stall"]),
        ], "Pipelining overlaps the stages of the fetch-decode-execute cycle: while one instruction executes, the next is being decoded and the one after that fetched. No part of the processor sits idle, so more instructions complete per second. A conditional branch is not resolved until it executes, by which time the instructions after it have already been fetched and decoded. If the branch is taken those instructions are the wrong ones, so the pipeline must be flushed and refilled, wasting the cycles spent on them.",
              command="Describe", label="1(b)"),
        rows("Tick (✓) one box in each row to show whether each statement describes a CISC or a RISC processor.", ["CISC", "RISC"],
             [("Has a large set of complex instructions, some taking many clock cycles", "CISC"),
              ("Has a small set of simple instructions, each completing in one clock cycle", "RISC"),
              ("A program compiles to fewer machine code instructions, so it takes up less memory", "CISC"),
              ("Pipelining is easier, because every instruction takes the same time", "RISC")],
             marks=2, model="CISC does more per instruction with more complex hardware; RISC keeps instructions simple and uniform, which suits pipelining.",
             label="1(c)"),
        write("Explain why a graphics processing unit (GPU) can carry out some tasks much faster than a CPU.", 3, [
            ("A GPU has a very large number of simple cores", ["many cores", "thousands", "hundreds", "large number of cores", "lots of cores", "many processing units"]),
            ("They carry out the same instruction on many pieces of data at the same time (SIMD)", ["same instruction", "simd", "parallel", "at the same time", "simultaneous", "many pieces of data"]),
            ("So tasks made of many independent calculations, such as rendering images or training machine learning models, are much faster",
             ["image", "graphic", "pixel", "render", "machine learning", "video", "matrix", "independent"]),
        ], "A GPU contains thousands of simple cores designed to carry out the same instruction on many items of data at once. Tasks made of large numbers of independent, identical calculations, such as working out the colour of every pixel in an image or the matrix arithmetic in machine learning, can be split across all of those cores, so they complete far faster than on a CPU's few powerful cores.",
              command="Explain", label="1(d)"),

        # ---------------------------------------------------- 2 systems software
        boxes("Three processes arrive in the ready queue at the same time, in the order A, B, C. Process A needs 5 ms of processor time, B needs 3 ms and C needs 4 ms. The operating system uses round robin scheduling with a time slice of 2 ms. State the time at which each process finishes.",
              [("A", "12", "ms"), ("B", "9", "ms"), ("C", "11", "ms")], numeric=True,
              model="A runs 0-2, B 2-4, C 4-6, A 6-8, B 8-9 and finishes, C 9-11 and finishes, then A 11-12 and finishes.",
              label="2(a)"),
        tick("Which **one** of these scheduling algorithms can leave a long process waiting indefinitely (starvation)?",
             ["*Shortest job first", "Round robin", "First come first served"],
             "Shortest job first always picks the shortest process, so if short ones keep arriving a long one may never run.",
             label="2(b)"),
        write("Describe the differences between paging and segmentation.", 4, [
            ("Paging splits memory into blocks of a fixed size, called pages", ["fixed size", "fixed-size", "same size", "equal size", "equally sized"]),
            ("Segmentation splits memory into blocks of variable size, called segments", ["variable size", "variable-size", "different sizes", "varying size", "different size"]),
            ("Pages are physical divisions, made without regard to the program's structure", ["physical", "regardless", "without regard", "not logical", "arbitrary", "may split"]),
            ("Segments are logical divisions, matching parts of the program such as a subroutine or a data structure", ["logical", "subroutine", "module", "function", "structure of the program", "meaningful"]),
        ], "Paging divides memory into equal, fixed-size pages. The divisions are physical: a page boundary can fall in the middle of a subroutine. Segmentation divides memory into segments of different sizes, and the divisions are logical, so each segment holds a complete part of the program, such as a subroutine or a data structure.",
              command="Describe", label="2(c)"),
        write("Explain how a processor deals with an interrupt.", 5, [
            ("At the end of each fetch-decode-execute cycle the processor checks the interrupt register", ["end of", "each cycle", "interrupt register", "checks", "every cycle"]),
            ("If the interrupt has a higher priority than the current task it is serviced; otherwise it waits", ["priority", "higher", "lower", "wait", "queue"]),
            ("The contents of the registers, including the program counter, are saved onto a stack", ["stack", "push", "saved", "registers", "program counter"]),
            ("The address of the interrupt service routine is loaded into the program counter and the ISR runs", ["isr", "interrupt service routine", "service routine", "handler", "loaded into the"]),
            ("When it finishes, the saved values are popped from the stack and the original task resumes", ["pop", "restored", "resume", "continues", "carry on", "returns"]),
        ], "At the end of every fetch-decode-execute cycle the processor checks the interrupt register. If an interrupt is waiting and its priority is higher than the current task, the processor saves the contents of its registers, including the program counter, onto a stack. The address of the matching interrupt service routine is loaded into the program counter, so the ISR runs. When it finishes, the saved values are popped back off the stack and the interrupted task carries on exactly where it stopped. An interrupt of lower priority waits until the current task allows it.",
              command="Explain", label="2(d)"),
        rows("Tick (✓) one box in each row to show the type of operating system described.",
             ["Real-time", "Distributed", "Multi-user", "Embedded"],
             [("Must respond to inputs within a guaranteed time, such as a car's anti-lock brakes", "Real-time"),
              ("Shares the processing of one task across several networked computers", "Distributed"),
              ("Lets several people use the resources of one computer at the same time", "Multi-user"),
              ("Built into a device with limited resources to control one function", "Embedded")],
             marks=2, model="Guaranteed response times are real-time, work spread over networked computers is distributed, many users of one machine is multi-user, and an OS built into a device is embedded.",
             label="2(e)"),

        # ---------------------------------------------------- 3 software and its development
        rows("Tick (✓) one box in each row to show the stage of compilation described.",
             ["Lexical analysis", "Syntax analysis", "Code generation", "Optimisation"],
             [("Whitespace and comments are removed and the code is split into tokens", "Lexical analysis"),
              ("The tokens are checked against the rules of the language and an abstract syntax tree is built", "Syntax analysis"),
              ("Object code is produced from the abstract syntax tree", "Code generation"),
              ("Code is removed or changed so the program runs faster or uses less memory", "Optimisation")],
             model="Lexical analysis tokenises, syntax analysis checks the grammar and builds the tree, code generation produces object code and optimisation improves it.",
             label="3(a)"),
        write("Explain the difference between static and dynamic linking of libraries.", 4, [
            ("Static linking copies the library code into the executable file when it is built", ["copied into", "included in the executable", "compile time", "part of the executable", "built in", "copies"]),
            ("So the executable is larger, but self-contained: it runs without the library being present", ["larger", "bigger", "self-contained", "self contained", "does not depend", "standalone"]),
            ("Dynamic linking loads the library from a separate file when the program runs, and it can be shared by several programs", ["run time", "runtime", "when it runs", "dll", "separate file", "shared", "loaded"]),
            ("So executables are smaller and library updates apply to them automatically, but the program fails if the library is missing or the wrong version",
             ["smaller", "update", "missing", "wrong version", "incompatib", "dependency"]),
        ], "With static linking the linker copies the library code the program uses into the executable. The file is larger, but it is self-contained and always has the version of the library it was built with. With dynamic linking the executable only holds a reference, and the library, a separate file such as a DLL, is loaded when the program runs and can be shared by many programs. Executables are smaller and pick up library updates automatically, but the program will not run if the library is missing or an incompatible version is installed.",
              command="Explain", label="3(b)"),
        rows("Tick (✓) one box in each row to show the development methodology described.",
             ["Waterfall", "Rapid application development", "Spiral model", "Extreme programming"],
             [("Each stage is completed and signed off before the next one begins", "Waterfall"),
              ("Prototypes are built quickly and refined with constant feedback from users", "Rapid application development"),
              ("Each cycle of development starts by identifying and resolving the biggest risks", "Spiral model"),
              ("Programmers work in pairs, and the code is tested continually and refactored", "Extreme programming")],
             model="Sequential sign-off is waterfall, repeated prototypes are RAD, risk-driven cycles are the spiral model, and pair programming with continual testing is extreme programming.",
             label="3(c)"),
        write("A start-up company is developing a mobile banking app. The client's requirements are expected to change as the app is tried out with customers, and the app must be secure and reliable.\n\nEvaluate the suitability of the waterfall model and of an agile methodology, such as extreme programming, for this project.", 9, [
            ("Waterfall has clear stages, documentation and sign-off, so it is easy to plan and manage", ["documentation", "clear stages", "sign off", "signed off", "easy to manage", "plan", "deadline"]),
            ("But waterfall fixes the requirements at the start, so changing them later is difficult and expensive", ["fixed", "at the start", "difficult to change", "expensive to change", "go back", "changing requirements"]),
            ("In waterfall the client sees the product only near the end, so problems are found late", ["only at the end", "late", "little user", "until the end", "not see", "end of the project"]),
            ("Agile works in short iterations, each producing a working version", ["iteration", "sprint", "increment", "working version", "short cycles", "prototype"]),
            ("Agile welcomes changing requirements, with regular feedback from the client and customers", ["feedback", "changing requirements", "adapt", "flexible", "respond to change", "client involvement", "customer"]),
            ("Extreme programming's pair programming and continual testing give high quality code", ["pair programming", "pairs", "unit test", "test-driven", "continual testing", "quality", "refactor"]),
            ("A banking app must be secure and reliable: frequent, rigorous testing supports this, and documentation helps to show it meets regulations",
             ["security", "secure", "reliab", "regulat", "compliance", "testing", "audit"]),
            ("Agile's drawbacks: less documentation, the client must stay closely involved, and the final cost and time are harder to estimate",
             ["less documentation", "documentation", "client must", "available", "harder to estimate", "cost", "scope creep"]),
            ("A justified conclusion: an agile methodology suits this project better because its requirements will change", ["conclusion", "overall", "more suitable", "therefore", "recommend", "best"]),
        ], "The waterfall model completes each stage, from analysis to maintenance, before the next begins, with documentation signed off at each step. That makes the project easy to plan and manage, and the thorough documentation helps a bank show regulators how the app was designed and tested. Its weakness here is that the requirements are fixed at the start: the client expects them to change as customers try the app, and in waterfall going back to change the design is slow and expensive. The client also sees a working product only near the end, so a misunderstanding may be discovered when it is most costly to fix.\n\nAn agile methodology such as extreme programming builds the app in short iterations, each producing a working version that the client and real customers can try. Their feedback shapes the next iteration, so changing requirements are expected rather than a problem. Extreme programming also suits the need for security and reliability: programmers work in pairs, so every line is reviewed as it is written, and tests are written first and run continually, so faults are caught early and the code is refactored to stay clean. The drawbacks are that agile projects produce less documentation, which a bank may need for compliance, the client must stay closely involved throughout, and the final cost and delivery date are harder to predict.\n\nOverall an agile methodology is more suitable, because the requirements will certainly change, but the team should keep enough documentation of its security design and testing to satisfy the regulators.",
              command="Evaluate", label="3(d)"),

        # ---------------------------------------------------- 4 data types
        boxes("Give the denary number -73 as an 8-bit binary integer in each representation.",
              [("Two's complement", ["10110111"]), ("Sign and magnitude", ["11001001"])],
              model="73 is 0100 1001. In two's complement, invert to 1011 0110 and add 1: 1011 0111. In sign and magnitude, set the sign bit: 1100 1001.",
              label="4(a)"),
        calc("A floating point number uses an 8-bit mantissa and a 4-bit exponent, both in two's complement. Convert the floating point number 0.1011000 0011 into denary. Show your working.",
             ["5.5"], 2, [("The exponent is 3, so the binary point moves 3 places right: 0101.1000",
                           ["0101.1", "101.1", "3 places", "exponent is 3", "exponent 3", "2^3", "x 8", "× 8", "0.6875"])],
             model="The exponent 0011 is 3, so the binary point moves 3 places right: 0101.1000, which is 4 + 1 + 0.5 = 5.5.",
             label="4(b)"),
        boxes("Normalise the floating point number 0.0011010 0010, which uses an 8-bit mantissa and a 4-bit exponent, both in two's complement.",
              [("Mantissa", ["0.1101000", "01101000"]), ("Exponent", ["0000"])],
              model="The mantissa must start 0.1, so shift it 2 places left to 0.1101000 and reduce the exponent by 2, from 2 to 0: 0000. Both represent 0.8125.",
              label="4(c)"),
        calc("Convert the floating point number 1.0110000 0010, which uses an 8-bit mantissa and a 4-bit exponent, both in two's complement, into denary. Show your working.",
             ["-2.5"], 2, [("The exponent is 2, giving 101.10000, or the mantissa is found to be -0.625",
                            ["101.1", "-0.625", "−0.625", "2 places", "exponent is 2", "exponent 2", "x 4", "× 4", "-4 + 1 + 0.5"])],
             model="The exponent 0010 is 2, so the binary point moves 2 places right: 101.10000. In two's complement that is -4 + 1 + 0.5 = -2.5.",
             label="4(d)"),
        boxes("Give the result of each bitwise operation.",
              [("1011 0110 AND 0000 1111", ["00000110"]), ("0011 0101 OR 1000 0000", ["10110101"]), ("1010 1010 XOR 1111 1111", ["01010101"])],
              model="AND with 0000 1111 keeps only the low four bits: 0000 0110. OR with 1000 0000 sets the top bit: 1011 0101. XOR with 1111 1111 flips every bit: 0101 0101.",
              label="4(e)"),
        write("Explain why floating point numbers are normalised.", 2, [
            ("To give the greatest precision possible for the number of bits in the mantissa", ["precision", "accura", "most significant", "maximum", "no wasted", "leading zero"]),
            ("So that each number has only one representation", ["unique", "one way", "only one", "single representation"]),
        ], "A normalised mantissa has no wasted leading bits, so every bit of the mantissa adds precision. It also means each number can be written in only one way, which makes numbers easy to compare.",
              command="Explain", label="4(f)"),
        boxes("State the smallest and largest denary values that can be represented in 8-bit two's complement.",
              [("Smallest", ["-128", "−128"]), ("Largest", "127")],
              model="1000 0000 is -128 and 0111 1111 is 127.", label="4(g)"),

        # ---------------------------------------------------- 5 data structures
        table("A stack is empty. These operations are carried out in order: push(5), push(9), pop(), push(3), push(7), pop(), push(1). Complete the table to show the contents of the stack.",
              ["Position", "Value"], [["Top", "=1"], ["Middle", "=3"], ["Bottom", "=5"]],
              groups=[("Top", [0]), ("Middle and bottom", [1, 2])], numeric=True,
              model="After push(5), push(9) and pop() the stack holds 5. push(3) and push(7) give 5, 3, 7, and pop() removes 7. push(1) gives 5, 3, 1 from bottom to top.",
              label="5(a)"),
        ans("A circular queue is held in an array with positions 0 to 5. The front pointer points to the first item and the rear pointer to the last item. The front pointer is 4 and the rear pointer is 1. State how many items are in the queue.",
            "4", numeric=True, model="The items are in positions 4, 5, 0 and 1, wrapping round: 4 items.", width=4, label="5(b)"),
        table("The values 50, 30, 70, 20, 40, 60, 80, 35 are inserted, in that order, into an empty binary search tree. Complete the table to show the order in which the nodes are visited by each traversal.",
              ["Traversal", "1st", "2nd", "3rd", "4th", "5th", "6th", "7th", "8th"],
              [["Pre-order", "=50", "=30", "=20", "=40", "=35", "=70", "=60", "=80"],
               ["In-order", "=20", "=30", "=35", "=40", "=50", "=60", "=70", "=80"],
               ["Post-order", "=20", "=35", "=40", "=30", "=60", "=80", "=70", "=50"]],
              per_row=True, numeric=True, width=4,
              model="50 is the root, with 30 and 70 as its children, 20 and 40 under 30, 60 and 80 under 70, and 35 as the left child of 40. Pre-order visits the root first, in-order visits it between its subtrees, giving the values in order, and post-order visits it last.",
              label="5(c)"),
        ans("State how many nodes are compared with 35 when the tree in 5(c) is searched for 35.", "4", numeric=True,
            model="50, then 30, then 40, then 35: four comparisons.", width=4, label="5(d)"),
        write("Describe how a hash table stores a record and finds it again, and how a collision can be dealt with.", 4, [
            ("A hashing function is applied to the record's key to give its position (index) in the table", ["hash function", "hashing function", "hashing algorithm", "key", "index", "address"]),
            ("To find it, the same function is applied to the key, and that position is read directly", ["same function", "same hash", "directly", "straight to", "without searching", "look up"]),
            ("A collision is when two keys hash to the same position", ["collision", "same position", "same index", "same address", "already occupied"]),
            ("Dealt with by storing the record in the next free position (linear probing), or by chaining in a linked list at that position",
             ["next free", "next available", "linear probing", "probing", "chaining", "linked list", "overflow"]),
        ], "A hashing function is applied to the record's key to calculate its position in the table, and the record is stored there. To find it again, the same function is applied to the key, which leads straight to the right position without searching. If two keys hash to the same position, a collision, the second record can be put in the next free position, which is then searched in order, or each position can hold a linked list of every record that hashes to it.",
              command="Describe", label="5(e)"),
        boxes("Cherry is to be added to the linked list in Figure 1, in alphabetical order, using position 5. State the new value of each pointer.",
              [("Next pointer of Cherry, at index 5", "2"), ("Next pointer of Banana, at index 3", "5")], numeric=True,
              figure=LINKED,
              model="Cherry belongs between Banana and Fig. Cherry takes Banana's old pointer, 2, so it points to Fig, and Banana's pointer changes to 5, Cherry's position.",
              label="5(f)"),
        tick("Which **one** data structure is used to hold the return addresses when subroutines are called?",
             ["*Stack", "Queue", "Hash table", "Binary tree"],
             "The most recent call must return first, which is last in, first out: a stack.", label="5(g)"),

        # ---------------------------------------------------- 6 Boolean algebra
        ans("Simplify the Boolean expression (A ∧ B) ∨ (A ∧ ¬B).", ["A"],
            model="A ∧ (B ∨ ¬B) = A ∧ 1 = A.", width=6, label="6(a)"),
        tick("Which **one** expression is equivalent to ¬(A ∨ B)?", ["*¬A ∧ ¬B", "¬A ∨ ¬B", "A ∧ B", "¬A ∧ B"],
             "De Morgan's law: negate each term and change OR to AND.", label="6(b)"),
        table("Complete the Karnaugh map for Q = (A ∧ ¬B) ∨ C.", ["AB", "C = 0", "C = 1"],
              [["00", "=0", "=1"], ["01", "=0", "=1"], ["11", "=0", "=1"], ["10", "=1", "=1"]],
              groups=[("Rows 00 and 01", [0, 1, 2, 3]), ("Rows 11 and 10", [4, 5, 6, 7])], numeric=True,
              model="Every cell where C is 1 is 1. A ∧ ¬B adds the cell where AB is 10 and C is 0.",
              label="6(c)"),
        tick("Which **one** expression is represented by the Karnaugh map in Figure 2?",
             ["*(A ∧ B) ∨ (¬C ∧ D)", "(A ∧ B) ∨ D", "(A ∨ B) ∧ (¬C ∧ D)", "A ∨ (¬C ∧ D)"],
             "The row AB = 11 is all 1s, giving A ∧ B, and the column CD = 01 is all 1s, giving ¬C ∧ D.",
             figure=KMAP4, label="6(d)"),
        table("Complete the truth table for a half adder.", ["A", "B", "Sum", "Carry"],
              [["0", "0", "=0", "=0"], ["0", "1", "=1", "=0"], ["1", "0", "=1", "=0"], ["1", "1", "=0", "=1"]],
              groups=[("Sum column", [0, 2, 4, 6]), ("Carry column", [1, 3, 5, 7])], numeric=True,
              model="Sum is 1 when exactly one input is 1. Carry is 1 only when both are 1.", label="6(e)"),
        rows("Tick (✓) one box in each row to show the logic gate that produces each output of a half adder.", ["AND", "OR", "XOR", "NOT"],
             [("Sum", "XOR"), ("Carry", "AND")],
             model="Sum = A XOR B and Carry = A AND B.", label="6(f)"),
        write("Describe the purpose and operation of a D-type flip-flop.", 3, [
            ("It stores a single bit, so it is used as memory, for example in registers", ["store", "one bit", "single bit", "memory", "register", "remember"]),
            ("The output Q takes the value of the data input D when the clock pulse rises (on the rising edge)", ["rising edge", "clock", "on the edge", "pulse", "takes the value", "copies"]),
            ("The output then stays the same, whatever D does, until the next rising edge", ["until the next", "holds", "stays", "unchanged", "retains", "keeps"]),
        ], "A D-type flip-flop stores one bit, so it is a building block of registers and memory. On each rising edge of the clock, the output Q takes the value of the data input D. Between rising edges Q holds that value, however D changes.",
              command="Describe", label="6(g)"),

        # ---------------------------------------------------- 7 databases and SQL
        rows("A vet stores data in the three tables shown in Figure 3. Tick (✓) one box in each row to show the type of key.",
             ["Primary key", "Foreign key"],
             [("PetID in the Pet table", "Primary key"), ("OwnerID in the Pet table", "Foreign key"),
              ("PetID in the Visit table", "Foreign key"), ("VisitID in the Visit table", "Primary key")],
             marks=2, model="Each table's own ID is its primary key. OwnerID in Pet and PetID in Visit link to other tables, so they are foreign keys.",
             figure="**Figure 3**\n\n" + VET[1], label="7(a)"),
        sql("Write an SQL query to return the Name and Species of every pet belonging to the owner with OwnerID 12, in alphabetical order of Name.",
            VET, "SELECT Name, Species\nFROM Pet\nWHERE OwnerID = 12\nORDER BY Name",
            [("SELECT Name, Species", "sorted(fields()) == ['name', 'species']"),
             ("FROM Pet", "tables() == ['pet']"),
             ("WHERE OwnerID = 12", "same_where('Pet', 'OwnerID = 12')"),
             ("ORDER BY Name (ASC)", "same_order('Pet', 'Name', 'OwnerID = 12')")],
            model="ORDER BY sorts in ascending order unless DESC is given.",
            wrong=["SELECT Name, Species FROM Pet WHERE OwnerID = 12 ORDER BY PetID", "SELECT Name, Species FROM Pet ORDER BY Name"],
            figure="", label="7(b)"),
        sql("Write an SQL query to return the Surname of the owner and the Name of the pet for every pet whose Species is Rabbit.",
            VET, "SELECT Surname, Name\nFROM Owner, Pet\nWHERE Owner.OwnerID = Pet.OwnerID\nAND Species = 'Rabbit'",
            [("SELECT Surname, Name", "sorted(fields()) == ['name', 'surname']"),
             ("FROM Owner, Pet, or an INNER JOIN of the two tables", "sorted(tables()) == ['owner', 'pet']"),
             ("Joins the tables: Owner.OwnerID = Pet.OwnerID", "uses(r'owner\\.ownerid\\s*=\\s*pet\\.ownerid', r'pet\\.ownerid\\s*=\\s*owner\\.ownerid')"),
             ("Only the rabbits: Species = 'Rabbit'", "set(r[0] for r in q('SELECT Pet.PetID FROM Owner, Pet WHERE ' + where())) == {3, 5, 7}")],
            model="The join condition pairs each pet with its own owner. An INNER JOIN ... ON Owner.OwnerID = Pet.OwnerID with WHERE Species = 'Rabbit' is equally correct.",
            wrong=["SELECT Surname, Name FROM Owner, Pet WHERE Species = 'Rabbit'"],
            figure="", label="7(c)"),
        sql("Write an SQL statement to delete every visit that cost less than £20.00.",
            VET, "DELETE FROM Visit\nWHERE Cost < 20",
            [("DELETE FROM Visit", "uses(r'^\\s*delete\\s+from\\s+visit\\b')"),
             ("WHERE Cost < 20: every visit costing less than £20.00 is removed", "qa('SELECT VisitID FROM Visit WHERE Cost < 20') == []"),
             ("Every visit costing £20.00 or more is kept, including the one costing exactly £20.00",
              "qa('SELECT VisitID FROM Visit ORDER BY VisitID') == [(101,), (103,), (105,), (107,), (108,)]")],
            model="Visit 108 cost exactly £20.00, so it must stay: the condition is < 20, not <= 20.",
            wrong=["DELETE FROM Visit", "DELETE FROM Visit WHERE Cost <= 20"],
            figure="", label="7(d)"),
        write("Explain how record locking prevents an update being lost when two users edit the same record at the same time.", 3, [
            ("When one user starts to edit a record, the record is locked", ["locked", "lock"]),
            ("No other user can change it until the first user's transaction is complete and the lock is released", ["cannot", "no other", "until", "released", "unlock", "complete", "finished"]),
            ("So the second change is made to the up-to-date record, instead of overwriting the first user's change", ["overwrit", "lost", "up to date", "up-to-date", "latest", "both changes"]),
        ], "When the first user opens the record to edit it, the record is locked. A second user cannot change it until the first user's transaction has been completed and the lock released. The second user then works on the updated record, so their change is added to the first rather than overwriting it.",
              command="Explain", label="7(e)"),

        # ---------------------------------------------------- 8 networks and the web
        rows("Tick (✓) one box in each row to show the layer of the TCP/IP stack that carries out each task.",
             ["Application", "Transport", "Internet", "Link"],
             [("Splits the data into numbered packets and adds the port number", "Transport"),
              ("Adds the source and destination IP addresses, which routers use to forward each packet", "Internet"),
              ("Adds MAC addresses and sends the data as signals over the physical connection", "Link"),
              ("Uses the protocol for the program in use, such as HTTP or SMTP, to format the data", "Application")],
             model="Application formats, transport packetises and numbers, internet addresses and routes, link transmits.",
             label="8(a)"),
        write("Describe how the domain name in a URL is resolved into an IP address.", 4, [
            ("The computer first checks its own cache for the IP address", ["cache", "cached", "stored locally", "already knows"]),
            ("Otherwise the request is sent to a DNS server", ["dns server", "domain name server", "resolver", "dns"]),
            ("If that server does not know it, the request passes to other DNS servers in the hierarchy: the root, then the top level domain, then the authoritative server",
             ["root", "top level", "top-level", "tld", "authoritative", "hierarchy", "another dns", "higher"]),
            ("The IP address is returned, and the browser uses it to connect to the web server", ["returned", "sent back", "connect", "web server"]),
        ], "The browser first checks its local cache in case the address was looked up recently. If not, it asks a DNS server. If that server does not hold the record, the query is passed up the hierarchy: a root server points to the server for the top level domain, such as .uk, which points to the domain's authoritative server, which holds the IP address. The address is returned to the browser, cached, and used to connect to the web server.",
              command="Describe", label="8(b)"),
        write("Compare packet switching with circuit switching.", 4, [
            ("Circuit switching sets up a dedicated path for the whole communication", ["dedicated", "reserved", "single path", "fixed path", "whole communication", "set up"]),
            ("Packet switching splits the data into packets that can take different routes", ["packets", "different routes", "different paths", "independently", "own route"]),
            ("Packets may arrive out of order and are reassembled using their sequence numbers", ["out of order", "reassembl", "sequence number", "reordered", "put back"]),
            ("Packet switching shares the network efficiently and routes round failures; circuit switching suits real-time data because the path and order are guaranteed",
             ["efficient", "shared", "avoid", "reroute", "real time", "real-time", "guaranteed", "phone call"]),
        ], "Circuit switching sets up a dedicated path between the two ends for the whole communication, so data arrives in order with a constant delay, which suits real-time voice, but the path is reserved even when nothing is being sent. Packet switching splits data into numbered packets that each take the best route available, so the links are shared efficiently and packets can be rerouted around a failure. The packets may arrive out of order, and are reassembled using their sequence numbers.",
              command="Compare", label="8(c)"),
        calc("PageRank uses the formula PR(A) = (1 - d) + d × (PR(T1) / C(T1) + ... + PR(Tn) / C(Tn)), where T1 to Tn are the pages that link to page A, and C(T) is the number of links out of page T.\n\nPages B and C are the only pages that link to page A. PR(B) = 2 and B links to 4 pages. PR(C) = 1 and C links only to A. Using d = 0.85, calculate PR(A). Show your working.",
             ["1.425"], 2, [("Works out 2 / 4 + 1 / 1 = 1.5", ["2/4", "2 / 4", "0.5", "1.5", "1/1"])],
             model="2 / 4 + 1 / 1 = 1.5. 0.85 x 1.5 = 1.275. 0.15 + 1.275 = 1.425.", tol=0.001, label="8(d)"),

        # ---------------------------------------------------- 9 exchanging data
        write("Explain how dictionary coding compresses a text file.", 3, [
            ("Words or patterns that occur often are stored once in a dictionary", ["dictionary", "stored once", "frequently", "repeated", "common words", "patterns"]),
            ("Each occurrence in the file is replaced by a short reference to its dictionary entry", ["replaced", "reference", "index", "code", "number", "token", "pointer"]),
            ("The references take fewer bits than the words, and the file is rebuilt exactly from the dictionary, so it is lossless",
             ["fewer bits", "less space", "smaller", "lossless", "rebuilt", "reconstruct", "exactly"]),
        ], "Dictionary coding builds a dictionary of the words and patterns that appear in the file. Each occurrence is replaced by its short index in the dictionary, which takes far fewer bits than the word itself. The dictionary is stored with the file, so the original can be rebuilt exactly: the compression is lossless.",
              command="Explain", label="9(a)"),
        write("Describe how asymmetric encryption allows a customer to send their card details securely to an online shop.", 3, [
            ("The shop has a key pair: a public key it shares and a private key it keeps secret", ["public key", "private key", "pair", "secret"]),
            ("The customer's browser encrypts the card details with the shop's public key", ["encrypt", "public key", "with the public", "using the public"]),
            ("Only the shop's private key can decrypt them, so anyone who intercepts the data cannot read it", ["only the", "private key can", "decrypt", "intercept", "cannot read", "cannot be read"]),
        ], "The shop publishes its public key and keeps the matching private key secret. The customer's browser encrypts the card details with the shop's public key. Data encrypted with that key can only be decrypted with the private key, which only the shop holds, so anyone intercepting the data in transit cannot read it.",
              command="Describe", label="9(b)"),
        write("Explain why a website stores the hashes of its users' passwords rather than the passwords themselves.", 2, [
            ("A hash cannot be reversed, so if the database is stolen the passwords are not revealed", ["cannot be reversed", "one way", "one-way", "irreversible", "stolen", "breach", "not revealed"]),
            ("When a user logs in, the password they enter is hashed and compared with the stored hash", ["compared", "compare", "hashed and", "matches", "same hash"]),
        ], "Hashing is one-way, so even if attackers steal the database they cannot turn the hashes back into passwords. The site never needs the password itself: it hashes whatever is typed at login and checks that it matches the stored hash.",
              command="Explain", label="9(c)"),

        # ---------------------------------------------------- 10 legal, moral, cultural and ethical issues
        write("A police force plans to use live facial recognition cameras in a city centre, comparing the face of everyone who walks past with a database of wanted people.\n\nDiscuss the legal, moral and ethical issues raised by this plan.", 12, [
            ("It can help catch wanted criminals and find missing people, improving public safety", ["catch", "wanted", "criminal", "missing", "safety", "crime", "deter"]),
            ("Everyone's face is scanned without their consent, including innocent people, which affects their privacy", ["privacy", "consent", "innocent", "everyone", "without their"]),
            ("Faces are biometric data, special category personal data under the Data Protection Act 2018 and UK GDPR", ["biometric", "special category", "data protection", "gdpr", "personal data"]),
            ("The data must be processed lawfully, kept only as long as necessary and kept secure", ["lawful", "necessary", "minimis", "deleted", "retention", "only as long", "secure", "proportion"]),
            ("Surveillance by public bodies is governed by the Regulation of Investigatory Powers Act 2000", ["regulation of investigatory powers", "ripa", "investigatory"]),
            ("False matches mean innocent people may be stopped or wrongly accused", ["false", "wrongly", "mistaken", "misidentif", "accuracy", "error"]),
            ("Systems trained on unrepresentative data can be less accurate for some ethnic groups, which is discriminatory", ["bias", "ethnic", "skin", "discriminat", "less accurate for", "unrepresentative", "women"]),
            ("People may feel watched and avoid protests or public places, a chilling effect on freedom", ["protest", "freedom", "chilling", "behave", "assembly", "expression", "trust"]),
            ("Function creep: the system could be extended to track ordinary people's movements", ["function creep", "track", "movements", "extended", "misuse", "mass surveillance"]),
            ("The database could be hacked or leaked, an offence under the Computer Misuse Act 1990", ["hack", "breach", "computer misuse", "stolen", "leak", "security"]),
            ("Safeguards: a human checks every match, signs warn the public, and there is independent oversight", ["human", "review", "sign", "oversight", "transparen", "audit", "safeguard"]),
            ("Reaches a balanced, justified conclusion", ["conclusion", "overall", "on balance", "therefore", "justified", "proportionate"]),
        ], "Supporters argue that live facial recognition helps the police find wanted criminals and missing people quickly, and that its presence may deter crime, making the city centre safer.\n\nLegally, a face is biometric data, which the Data Protection Act 2018 and UK GDPR treat as special category personal data. The police need a clear lawful basis, must show the use is necessary and proportionate, must delete the images of people who do not match straight away and must keep the data secure. Covert surveillance by public bodies is also governed by the Regulation of Investigatory Powers Act 2000, and anyone who hacked the system or leaked the watch list would commit an offence under the Computer Misuse Act 1990.\n\nMorally, everyone who walks past is scanned without their consent, though nearly all of them are innocent, which is a serious intrusion on privacy. No system is perfectly accurate: a false match can lead to an innocent person being stopped and searched in public. Systems trained on unrepresentative data have been shown to be less accurate for some ethnic groups and for women, so the harm of false matches falls unequally, which is discriminatory. Culturally, people who know they are being watched may change their behaviour, for example avoiding a lawful protest, which has a chilling effect on freedom of expression and assembly and can damage trust between the public and the police. There is also the risk of function creep, in which a system introduced to find wanted criminals is gradually extended to track the movements of ordinary people.\n\nOn balance the technology can be justified only with strong safeguards: a narrow watch list, a trained officer checking every match before anyone is stopped, clear signs telling the public it is in use, independent oversight and published accuracy figures. Without those, the harm to privacy and fairness outweighs the benefit.",
              command="Discuss", label="10"),
    ],
)


# ===================================================================== H446/02

MYSTERY = '''def mystery(n):
    if n == 0:
        return 0
    else:
        return n % 10 + mystery(n // 10)
'''

MYSTERY_ITER = '''def mystery(n):
    total = 0
    while n > 0:
        total = total + n % 10
        n = n // 10
    return total
'''

ANIMAL = '''class Animal:
    def __init__(self, name):
        self.__name = name

    def getName(self):
        return self.__name

    def speak(self):
        return "..."


class Dog(Animal):
    def speak(self):
        return "Woof"
'''

TREE = ((None, 2, None), 4, ((None, 5, None), 7, (None, 9, None)))

COUNT_NODES = '''def countNodes(tree):
    if tree is None:
        return 0
    left, value, right = tree
    return 1 + countNodes(left) + countNodes(right)
'''

BALANCED = '''def isBalanced(text):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for character in text:
        if character in "([{":
            stack.append(character)
        elif character in ")]}":
            if len(stack) == 0 or stack.pop() != pairs[character]:
                return False
    return len(stack) == 0
'''

SEARCH = '''def binarySearch(items, target, low, high):
    if low > high:
        return -1
    mid = (low + high) // 2
    if items[mid] == target:
        return mid
    elif items[mid] < target:
        return binarySearch(items, target, mid + 1, high)
    else:
        return binarySearch(items, target, low, mid - 1)
'''
SORTED = [3, 8, 12, 19, 25, 31, 40, 52, 66]

INSERTION_START = '''def insertionSort(items):
    for i in range(1, len(items)):
        current = items[i]
        # Complete the procedure: move each item before position i that is
        # larger than current one place to the right, then put current
        # into the gap that is left
        pass
'''

INSERTION = '''def insertionSort(items):
    for i in range(1, len(items)):
        current = items[i]
        position = i
        while position > 0 and items[position - 1] > current:
            items[position] = items[position - 1]
            position = position - 1
        items[position] = current
'''

QUEUE_HEAD = '''class Queue:
    def __init__(self, size):
        self.items = [None] * size
        self.size = size
        self.front = 0
        self.rear = -1
        self.count = 0

    def isEmpty(self):
        return self.count == 0

    def isFull(self):
        return self.count == self.size
'''

QUEUE_START = QUEUE_HEAD + '''
    def enqueue(self, item):
        # Add item at the rear, wrapping round to position 0.
        # Return False if the queue is full, otherwise True.
        pass

    def dequeue(self):
        # Remove and return the item at the front, wrapping round.
        # Return None if the queue is empty.
        pass
'''

QUEUE = QUEUE_HEAD + '''
    def enqueue(self, item):
        if self.isFull():
            return False
        self.rear = (self.rear + 1) % self.size
        self.items[self.rear] = item
        self.count = self.count + 1
        return True

    def dequeue(self):
        if self.isEmpty():
            return None
        item = self.items[self.front]
        self.front = (self.front + 1) % self.size
        self.count = self.count - 1
        return item
'''

VALUES = '''VALUES = {"A": 1, "B": 3, "C": 3, "D": 2, "E": 1, "F": 4, "G": 2, "H": 4, "I": 1,
          "J": 8, "K": 5, "L": 1, "M": 3, "N": 1, "O": 1, "P": 3, "Q": 10, "R": 1,
          "S": 1, "T": 1, "U": 1, "V": 4, "W": 4, "X": 8, "Y": 4, "Z": 10}
'''

WORD_SCORE = '''def wordScore(word):
    total = 0
    for letter in word.upper():
        total = total + VALUES[letter]
    if len(word) >= 7:
        total = total * 2
    return total
'''

CAN_MAKE = '''def canMake(word, rack):
    tiles = list(rack)
    for letter in word.upper():
        if letter in tiles:
            tiles.remove(letter)
        else:
            return False
    return True
'''

BEST_WORD = '''def bestWord(words, rack):
    best = ""
    bestScore = 0
    for word in words:
        if canMake(word, rack) and wordScore(word) > bestScore:
            best = word
            bestScore = wordScore(word)
    return best
'''

PLAYER = '''class Player:
    def __init__(self, name):
        self.__name = name
        self.__score = 0

    def getName(self):
        return self.__name

    def getScore(self):
        return self.__score

    def addWord(self, word):
        points = wordScore(word)
        self.__score = self.__score + points
        return points
'''

GAME_START = '''class Game:
    def __init__(self, players):
        # players is a list of Player objects, in the order they take turns
        pass

    def nextPlayer(self):
        # Return the player whose turn it is, and move them to the back of the queue
        pass

    def winner(self):
        # Return the name of the player with the highest score
        pass
'''

GAME = '''class Game:
    def __init__(self, players):
        self.__queue = list(players)

    def nextPlayer(self):
        player = self.__queue.pop(0)
        self.__queue.append(player)
        return player

    def winner(self):
        best = self.__queue[0]
        for player in self.__queue:
            if player.getScore() > best.getScore():
                best = player
        return best.getName()
'''

SCENARIO = """A company is writing a word game for two or more players. Each player has a rack of seven letter tiles. On their turn, a player makes a word from the tiles on their rack and scores the total of the letter values in the word. A word of seven or more letters scores double.

The letter values are stored in a dictionary called VALUES:

```pycode
""" + VALUES + """```"""

H446_2B = Paper(
    slug="h446-paper-2-b",
    title="A Level Computer Science Paper 2 B: Algorithms and Programming",
    course="A Level Computer Science", board="OCR", code="H446/02",
    minutes=150, marks=140, accent=ACC, spec="H446", full=True,
    blurb="A full length H446/02 paper. Section A: computational thinking, recursion, parameter passing, OOP, Big O, insertion sort, Dijkstra's algorithm and A*, tree traversals, and programs for bracket matching, a recursive binary search and a circular queue. Section B: a word game to program in Python, with a 9 mark evaluation of object-oriented design.",
    calculator="You must not use a calculator.",
    instructions=["Write program code in Python, so it can be run and marked here.",
                  "The 9 mark question earns a mark for each relevant point here; the real exam marks it in levels."],
    questions=[
        # ---------------------------------------------------- Section A: 1 computational thinking
        write("A satnav app shows a map of the roads to help a driver plan a route. Explain how abstraction has been used to produce the map.", 2, [
            ("Details that are not needed, such as buildings, trees or the exact shape of the land, are removed", ["removed", "left out", "hidden", "unnecessary", "buildings", "not shown", "ignore", "irrelevant"]),
            ("Only what the driver needs, such as the roads, junctions and distances, is kept, so the problem is simpler to solve",
             ["roads", "junction", "distance", "only what", "relevant", "needed", "simpler", "graph"]),
        ], "Everything that does not help plan a route, such as buildings, trees and the shape of the land, has been removed. Only the roads, the junctions and the distances between them are kept, which turns the real world into a much simpler problem the app can solve.",
              command="Explain", label="1(a)", section="Section A", section_note="Answer all the questions in this section."),
        write("A function binarySearch(items, target) is to be written. Identify **two** preconditions for the function.", 2, [
            ("The list items must be sorted", ["sorted", "in order", "ordered"]),
            ("The target and the items must be of the same type, so they can be compared (or the list must not be empty)", ["same type", "comparable", "not empty", "same data type", "compared"]),
        ], "The list must already be sorted, and the target must be the same type as the items in the list, so that they can be compared.",
              command="Identify", label="1(b)"),
        write("A web browser caches the pages it has recently loaded. Explain **one** benefit and **one** drawback of caching.", 3, [
            ("A cached page is loaded from local storage instead of being downloaded again", ["local", "stored", "rather than download", "not downloaded again", "already stored", "memory", "instead of"]),
            ("So it loads faster and uses less bandwidth", ["faster", "quicker", "bandwidth", "less data", "reduced load"]),
            ("Drawback: the cached copy may be out of date, or the cache uses storage space", ["out of date", "stale", "old version", "not the latest", "storage space", "takes up space"]),
        ], "A page in the cache is loaded from the computer's own storage rather than downloaded again, so it appears faster and less bandwidth is used. But if the page has changed since it was cached, the browser may show an out of date version.",
              command="Explain", label="1(c)"),
        write("Explain how thinking concurrently could reduce the time taken to display a web page that contains many images.", 3, [
            ("Identify the parts of the task that can be carried out at the same time", ["at the same time", "simultaneous", "parallel", "concurren"]),
            ("The images can be downloaded at the same time as each other, while the text is laid out", ["images", "download", "while", "at once", "each image", "text"]),
            ("Because these tasks do not depend on each other, the total time is reduced", ["independent", "do not depend", "don't depend", "less time", "reduced", "sooner", "faster"]),
        ], "Thinking concurrently means identifying the parts of the task that can happen at the same time. Each image can be requested and downloaded at the same time as the others, while the text of the page is being laid out. None of these tasks depends on the others, so overlapping them makes the page appear much sooner than doing them one after another.",
              command="Explain", label="1(d)"),
        write("Explain **two** reasons why programmers use reusable components, such as subroutines from a library.", 2, [
            ("They save development time, because the code does not need to be written again", ["time", "saves", "quicker", "not written again", "already written"]),
            ("They have already been tested, so they are reliable", ["tested", "reliable", "debugged", "fewer errors", "proven"]),
        ], "Using a library subroutine saves the time it would take to write and test the code again, and because it has already been tested and used by many programmers it is likely to be reliable.",
              command="Explain", label="1(e)"),
        rows("Tick (✓) one box in each row to show the aspect of computational thinking described.",
             ["Thinking ahead", "Thinking procedurally", "Thinking logically", "Thinking concurrently"],
             [("Identifying the inputs and outputs a program needs before writing it", "Thinking ahead"),
              ("Breaking a problem into sub-procedures that can each be solved separately", "Thinking procedurally"),
              ("Identifying the decision points in an algorithm and the conditions that decide them", "Thinking logically"),
              ("Identifying the parts of a problem that can be tackled at the same time", "Thinking concurrently")],
             marks=2, model="Inputs and outputs are thinking ahead, sub-procedures are thinking procedurally, decisions are thinking logically and simultaneous parts are thinking concurrently.",
             label="1(f)"),

        # ---------------------------------------------------- 2 programming techniques
        ans("State the value returned by mystery(472), for the function in Figure 1.", "13", numeric=True,
            figure="**Figure 1**\n\n```pycode\n" + MYSTERY + "```",
            model="2 + mystery(47) = 2 + 7 + mystery(4) = 2 + 7 + 4 + mystery(0) = 13. The function adds up the digits.", width=6, label="2(a)(i)"),
        ans("State how many times mystery is called, in total, when mystery(472) is called.", "4", numeric=True,
            model="mystery(472), mystery(47), mystery(4) and mystery(0): four calls.", width=4, label="2(a)(ii)"),
        prog("Rewrite the function mystery so that it uses iteration instead of recursion. It must return the same values.",
             MYSTERY, MYSTERY_ITER,
             [("Returns 13 for 472", "call('mystery', 472) == 13"),
              ("Returns 0 for 0", "call('mystery', 0) == 0"),
              ("Works for other numbers: 36 for 9999 and 1 for 1000000", "call('mystery', 9999) == 36 and call('mystery', 1000000) == 1"),
              ("Uses iteration, and the function no longer calls itself",
               "count('While') + count('For') + count('comprehension') >= 1 and src.count('mystery(') == 1")],
             model="Take the last digit with % 10, add it to a running total, and remove it with // 10, until no digits are left.",
             wrong=[MYSTERY_ITER.replace("while n > 0:", "while n > 9:")],
             label="2(a)(iii)", filename="mystery.py"),
        write("Explain **one** advantage and **one** disadvantage of using recursion rather than iteration.", 4, [
            ("Advantage: recursive code is often shorter and more natural for problems defined in terms of themselves, such as traversing a tree",
             ["shorter", "fewer lines", "natural", "elegant", "easier to write", "tree", "defined in terms"]),
            ("Because the code mirrors the structure of the problem, it is easier to follow", ["mirror", "structure", "easier to understand", "easier to follow", "readable", "clear"]),
            ("Disadvantage: every call adds a stack frame, using more memory", ["stack", "memory", "frame"]),
            ("So deep recursion can cause a stack overflow, and the extra calls make it slower", ["stack overflow", "overflow", "runs out", "slower", "overhead"]),
        ], "For a problem that is defined in terms of smaller versions of itself, such as visiting every node of a tree, a recursive solution is short and mirrors the structure of the data, so it is easier to write and follow. But every recursive call puts a new frame on the call stack, holding its parameters, local variables and return address, so recursion uses more memory and time than a loop, and very deep recursion can overflow the stack.",
              command="Explain", label="2(b)"),
        boxes("State the two values printed when this program is run.",
              [("First value printed", "5"), ("Second value printed", "6")], numeric=True,
              figure="```pseudo\nprocedure change(byVal a, byRef b)\n    a = a + 1\n    b = b + 1\nendprocedure\n\nx = 5\ny = 5\nchange(x, y)\nprint(x)\nprint(y)\n```",
              model="x is passed by value, so the procedure changes only its own copy and x stays 5. y is passed by reference, so the change to b changes y, which becomes 6.",
              label="2(c)"),
        rows("Tick (✓) one box in each row to show the feature of an IDE described.",
             ["Breakpoint", "Watch window", "Stepping", "Syntax highlighting"],
             [("Pauses the program when it reaches a chosen line", "Breakpoint"),
              ("Displays the values of chosen variables as the program runs", "Watch window"),
              ("Runs the program one line at a time", "Stepping"),
              ("Shows keywords, strings and comments in different colours", "Syntax highlighting")],
             marks=2, model="Breakpoints pause, watches show values, stepping runs line by line, and highlighting colours the code.",
             label="2(d)"),
        tick("Which **one** object-oriented concept is shown by the method speak in the class Dog, in Figure 2?",
             ["*Polymorphism", "Encapsulation", "Instantiation", "Abstraction"],
             "Dog overrides the speak method it inherits, so the same call gives different behaviour depending on the object's class: polymorphism.",
             figure="**Figure 2**\n\n```pycode\n" + ANIMAL + "```", label="2(e)(i)"),
        write("Explain how the class Animal in Figure 2 uses encapsulation.", 2, [
            ("The attribute name is private (__name), so it cannot be accessed directly from outside the class", ["private", "__name", "cannot be accessed", "directly", "outside the class", "hidden"]),
            ("It can only be read through the public method getName", ["getname", "method", "getter", "public method", "through"]),
        ], "The attribute __name is private, so code outside the class cannot read or change it directly. The only way to get the name is through the public method getName, so the class controls how its data is used.",
              command="Explain", label="2(e)(ii)"),
        rows("Tick (✓) one box in each row to show the object-oriented term described.", ["Class", "Object", "Method", "Inheritance"],
             [("A template that defines the attributes and methods of a type of object", "Class"),
              ("An instance of a class", "Object"),
              ("A subroutine that belongs to a class", "Method"),
              ("Creating a new class from an existing one, so it gains its attributes and methods", "Inheritance")],
             marks=2, model="A class is the template, an object an instance of it, a method a subroutine in it, and inheritance builds a class on another.",
             label="2(e)(iii)"),
        write("Explain why programmers avoid using global variables where possible.", 2, [
            ("A global variable can be changed by any part of the program, so errors caused by unexpected changes are hard to trace", ["any part", "anywhere", "hard to trace", "unexpected", "side effect", "accidentally", "difficult to debug"]),
            ("Subroutines that use globals are harder to reuse and test separately, and the variable uses memory for the whole run", ["reuse", "test", "independent", "memory", "whole program", "self-contained"]),
        ], "Because any subroutine can change a global variable, an unexpected change is hard to trace back to its cause. Subroutines that depend on globals are also harder to test separately and reuse in other programs.",
              command="Explain", label="2(f)"),
        prog("A binary tree is stored either as None, if it is empty, or as a tuple (left, value, right), where left and right are themselves trees. For example, the tree in Figure 3 is stored as\n\n((None, 2, None), 4, ((None, 5, None), 7, (None, 9, None)))\n\nWrite a recursive function countNodes(tree) that returns the number of nodes in a tree.",
             "def countNodes(tree):\n    # Return the number of nodes in tree\n    pass\n", COUNT_NODES,
             [("Returns 0 for an empty tree, None", "call('countNodes', None) == 0"),
              ("Returns 1 for a tree of one node", "call('countNodes', (None, 5, None)) == 1"),
              ("Counts the nodes in both subtrees: 5 for the tree in Figure 3", "call('countNodes', %r) == 5" % (TREE,)),
              ("Is recursive: countNodes calls itself", "src.count('countNodes(') >= 2")],
             model="The base case is the empty tree, with 0 nodes. Any other tree has 1 node, its root, plus the nodes in its left and right subtrees.",
             wrong=[COUNT_NODES.replace("1 + countNodes(left) + countNodes(right)", "1 + countNodes(left)")],
             figure="**Figure 3**\n\n```text\n    4\n   / \\\n  2   7\n     / \\\n    5   9\n```",
             label="2(g)", filename="tree.py"),

        # ---------------------------------------------------- 3 algorithms
        rows("Tick (✓) one box in each row to show the time complexity.", ["O(1)", "O(log n)", "O(n)", "O(n log n)", "O(n²)"],
             [("A binary search", "O(log n)"), ("A bubble sort, in the worst case", "O(n²)"),
              ("A merge sort", "O(n log n)"), ("Reading an item from an array by its index", "O(1)")],
             model="Binary search halves the list each time, bubble sort compares every pair, merge sort does n work on each of log n levels, and indexing is a single step.",
             label="3(a)"),
        write("Explain why an O(n log n) sorting algorithm is preferred to an O(n²) one for a large data set.", 2, [
            ("The time an O(n²) algorithm takes grows with the square of the number of items, much faster than n log n", ["square", "grows", "much faster", "quadratic", "increases"]),
            ("So for large n the O(n log n) algorithm needs far fewer steps: for a million items, about 20 million against a million million",
             ["fewer", "far less", "million", "less time", "quicker", "steps", "operations"]),
        ], "The time taken by an O(n²) algorithm grows with the square of the number of items, so doubling the data quadruples the time. For a million items, n² is a million million steps while n log n is about 20 million, so the O(n log n) algorithm is many thousands of times faster.",
              command="Explain", label="3(b)"),
        table("An insertion sort is used to sort the list 7, 3, 9, 1, 5 into ascending order. Complete the table to show the list after each pass of the outer loop.",
              ["", "Position 0", "Position 1", "Position 2", "Position 3", "Position 4"],
              [["After pass 1", "=3", "=7", "=9", "=1", "=5"], ["After pass 2", "=3", "=7", "=9", "=1", "=5"],
               ["After pass 3", "=1", "=3", "=7", "=9", "=5"], ["After pass 4", "=1", "=3", "=5", "=7", "=9"]],
              per_row=True, numeric=True, width=4,
              model="Pass 1 inserts 3 before 7. Pass 2 leaves 9 where it is. Pass 3 moves 1 to the front. Pass 4 inserts 5 between 3 and 7.",
              label="3(c)"),
        tick("Which **one** is the worst case time complexity of a quick sort?", ["O(log n)", "O(n)", "O(n log n)", "*O(n²)"],
             "If every pivot is the largest or smallest item, each partition removes only one item, giving O(n²).", label="3(d)"),
        boxes("Figure 4 shows the weights of the edges of an undirected graph. Use Dijkstra's algorithm to find the length of the shortest path from A to each node.",
              [("B", "3"), ("C", "2"), ("D", "8"), ("E", "10"), ("F", "12")], numeric=True,
              groups=[("B and C", [0, 1]), ("D and E", [2, 3]), ("F", [4])],
              figure="**Figure 4**\n\n| Edge | A-B | A-C | B-C | B-D | C-D | C-E | D-E | D-F | E-F |\n|---|---|---|---|---|---|---|---|---|---|\n| Weight | 4 | 2 | 1 | 5 | 8 | 10 | 2 | 6 | 2 |",
              model="C is 2. B is 3, through C (2 + 1), which beats the direct 4. D is 8, through B (3 + 5). E is 10, through D (8 + 2), which beats 12 through C. F is 12, through E (10 + 2), which beats 14 through D.",
              label="3(e)(i)"),
        ans("State the shortest path from A to F, as the list of nodes visited.",
            [sep.join("ACBDEF") for sep in (", ", ",", " ", "", "-", "->", "→", ">")],
            model="A, C, B, D, E, F, with a length of 12.", width=18, label="3(e)(ii)"),
        write("Explain how the A* algorithm differs from Dijkstra's algorithm.", 3, [
            ("A* uses a heuristic: an estimate of the distance from each node to the goal", ["heuristic", "estimate", "to the goal", "to the destination", "straight line"]),
            ("It visits next the node with the lowest f = g + h: the distance so far plus the estimate", ["f = g + h", "g + h", "plus the heuristic", "distance so far", "total estimated", "g(n)"]),
            ("So it heads towards the goal and usually visits fewer nodes, finding one route faster; Dijkstra finds the shortest path to every node",
             ["fewer nodes", "faster", "towards the goal", "every node", "all nodes", "one destination", "single destination"]),
        ], "Dijkstra's algorithm always visits the unvisited node with the smallest distance from the start, so it spreads out in every direction and finds the shortest path to every node. A* adds a heuristic, an estimate of the remaining distance to the goal, and visits the node with the smallest total of distance so far plus estimate. That steers the search towards the goal, so it usually visits far fewer nodes to find a route to one destination.",
              command="Explain", label="3(f)"),
        table("Complete the table to show the order in which the nodes of the tree in Figure 5 are visited by a breadth-first traversal and by a depth-first (pre-order) traversal, starting at A and visiting left children first.",
              ["Traversal", "1st", "2nd", "3rd", "4th", "5th", "6th"],
              [["Breadth-first", "=A", "=B", "=C", "=D", "=E", "=F"], ["Depth-first", "=A", "=B", "=D", "=E", "=C", "=F"]],
              per_row=True, width=3,
              figure="**Figure 5**\n\n```text\n        A\n       / \\\n      B   C\n     / \\   \\\n    D   E   F\n```",
              model="Breadth-first visits each level in turn: A, then B and C, then D, E and F. Depth-first goes as deep as it can down the left first: A, B, D, E, then C and F.",
              label="3(g)"),
        write("Explain why a binary search cannot be carried out efficiently on a linked list.", 2, [
            ("A binary search must go straight to the middle item, which needs direct access by index", ["middle", "direct access", "random access", "index", "jump"]),
            ("In a linked list an item can only be reached by following the pointers from the start, so finding the middle takes linear time", ["pointer", "from the start", "follow", "traverse", "one by one", "sequential", "linear"]),
        ], "A binary search works by jumping straight to the middle item, which needs direct access by position, as an array gives. A linked list can only be followed node by node from its start, so just reaching the middle takes as long as a linear search.",
              command="Explain", label="3(h)"),
        prog("Write a function isBalanced(text) that uses a stack to check whether the brackets ( ), [ ] and { } in a string are balanced. It returns True if every opening bracket is closed by the matching bracket, in the right order, and False otherwise. Other characters are ignored.",
             "def isBalanced(text):\n    # Use a list as a stack\n    pass\n", BALANCED,
             [("Returns True for balanced brackets: (a[b]{c})", "call('isBalanced', '(a[b]{c})') == True"),
              ("Returns True for a string with no brackets, and for an empty string", "call('isBalanced', 'abc') == True and call('isBalanced', '') == True"),
              ("Returns False when a bracket is closed by the wrong type: (]", "call('isBalanced', '(]') == False"),
              ("Returns False when brackets close in the wrong order: ([)]", "call('isBalanced', '([)]') == False"),
              ("Returns False when a bracket is never closed: ((x)", "call('isBalanced', '((x)') == False"),
              ("Returns False when a closing bracket has nothing to match: x)(", "call('isBalanced', 'x)(') == False")],
             model="Push each opening bracket. For each closing bracket, the stack must not be empty and the bracket popped must be its partner. At the end, the stack must be empty.",
             wrong=["def isBalanced(text):\n    depth = 0\n    for c in text:\n        if c in '([{':\n            depth += 1\n        elif c in ')]}':\n            depth -= 1\n            if depth < 0:\n                return False\n    return depth == 0\n",
                    BALANCED.replace("return len(stack) == 0", "return True")],
             label="3(i)", filename="brackets.py"),
        prog("Write a recursive function binarySearch(items, target, low, high) that returns the index of target in the sorted list items, searching only between the indexes low and high inclusive, or -1 if target is not there. It is first called as binarySearch(items, target, 0, len(items) - 1).",
             "def binarySearch(items, target, low, high):\n    # Return the index of target, or -1\n    pass\n", SEARCH,
             [("Finds an item in the middle: 25 is at index 4", "call('binarySearch', %r, 25, 0, 8) == 4" % (SORTED,)),
              ("Finds the first and the last items", "call('binarySearch', %r, 3, 0, 8) == 0 and call('binarySearch', %r, 66, 0, 8) == 8" % (SORTED, SORTED)),
              ("Finds items in either half", "call('binarySearch', %r, 12, 0, 8) == 2 and call('binarySearch', %r, 52, 0, 8) == 7" % (SORTED, SORTED)),
              ("Returns -1 when the item is not there, including for an empty list",
               "call('binarySearch', %r, 20, 0, 8) == -1 and call('binarySearch', %r, 99, 0, 8) == -1 and call('binarySearch', [], 5, 0, -1) == -1" % (SORTED, SORTED)),
              ("Is recursive, and searches only between low and high", "src.count('binarySearch(') >= 2 and call('binarySearch', [1, 2, 3, 4, 5], 1, 2, 4) == -1")],
             model="The base case is low > high: nothing is left to search. Otherwise compare the middle item and recurse on the half that could hold the target, moving low or high past the middle.",
             wrong=["def binarySearch(items, target, low, high):\n    while low <= high:\n        mid = (low + high) // 2\n        if items[mid] == target:\n            return mid\n        elif items[mid] < target:\n            low = mid + 1\n        else:\n            high = mid - 1\n    return -1\n",
                    "def binarySearch(items, target, low, high):\n    if target in items:\n        return items.index(target)\n    return -1\n"],
             label="3(j)", filename="search.py"),
        prog("Complete the procedure insertionSort(items), which sorts the list items into ascending order, in place, using an insertion sort.",
             INSERTION_START, INSERTION,
             [("Sorts the list in place: 7, 3, 9, 1, 5", "after('insertionSort', [7, 3, 9, 1, 5])[0] == [1, 3, 5, 7, 9]"),
              ("Sorts a list in reverse order, and one with repeated values",
               "after('insertionSort', [9, 7, 5, 3, 1])[0] == [1, 3, 5, 7, 9] and after('insertionSort', [4, 2, 4, 1, 2])[0] == [1, 2, 2, 4, 4]"),
              ("Copes with an empty list and a list of one item", "after('insertionSort', [])[0] == [] and after('insertionSort', [6])[0] == [6]"),
              ("Keeps the outer loop of the insertion sort, and uses no built-in sort",
               "uses(r'for\\s+i\\s+in\\s+range\\(\\s*1\\s*,\\s*len\\(\\s*items\\s*\\)\\s*\\)') and not uses(r'\\.sort\\s*\\(', r'\\bsorted\\s*\\(')")],
             model="Shift each larger item one place right, working back from position i - 1, then drop current into the gap.",
             wrong=[INSERTION.replace("items[position - 1] > current", "items[position - 1] < current"),
                    INSERTION_START.replace("        pass\n", "        pass\n    items.sort()\n")],
             label="3(k)", filename="sort.py"),
        write("Explain why a merge sort needs more memory than an insertion sort.", 2, [
            ("Merge sort creates new lists as it splits the list and merges the parts", ["new list", "sublists", "temporary", "copies", "extra lists", "additional lists"]),
            ("So it needs extra memory in proportion to the size of the list, while insertion sort only moves items within the original list",
             ["proportional", "o(n)", "in place", "within the original", "same list", "extra memory", "additional memory"]),
        ], "Merge sort builds new lists as it splits the data and merges the sorted halves, so it needs extra memory in proportion to the number of items. Insertion sort works in place, moving items within the original list, so it needs only one extra variable.",
              command="Explain", label="3(l)"),
        tick("Which **one** is the time complexity of this code, in terms of n?", ["O(n)", "*O(n²)", "O(log n)", "O(n log n)"],
             "The inner loop runs n times for each of the n passes of the outer loop: n x n steps.",
             figure="```pycode\ntotal = 0\nfor i in range(n):\n    for j in range(n):\n        total = total + i * j\n```", label="3(m)(i)"),
        tick("Which **one** is the time complexity of this code, in terms of n?", ["*O(log n)", "O(n)", "O(n²)", "O(1)"],
             "n is halved each time round the loop, so it repeats about log2 n times.",
             figure="```pycode\nwhile n > 1:\n    n = n // 2\n```", label="3(m)(ii)"),
        write("Explain why A* may not find the shortest path if its heuristic overestimates the distance to the goal.", 2, [
            ("An overestimate can make a node on the true shortest path look worse than it is", ["look worse", "worse than", "overestimat", "higher than", "too high", "not explored", "ignored"]),
            ("So the algorithm may reach the goal by another route first, and stop before exploring the shortest path", ["another route", "longer route", "stop", "reaches the goal", "first", "before"]),
        ], "A* explores the nodes with the smallest estimated total first. If the heuristic overestimates, a node on the genuinely shortest path can look more expensive than it is and be left unexplored, so the algorithm may reach the goal along a longer route first and stop there.",
              command="Explain", label="3(n)"),

        # ---------------------------------------------------- 4 a circular queue
        prog("The class Queue holds a circular queue in a list of fixed size. Complete the methods enqueue and dequeue, following the comments in the code.",
             QUEUE_START, QUEUE,
             [("enqueue and dequeue give items back in first in, first out order",
               T("q = Queue(3)\nq.enqueue(1)\nq.enqueue(2)\nresult = [q.dequeue(), q.dequeue()]", [1, 2])),
              ("enqueue returns True when the item is added", T("q = Queue(2)\nresult = q.enqueue(5)", True)),
              ("enqueue returns False when the queue is full, and does not add the item",
               T("q = Queue(2)\nq.enqueue(1)\nq.enqueue(2)\nresult = [q.enqueue(3), q.dequeue(), q.dequeue(), q.dequeue()]", [False, 1, 2, None])),
              ("dequeue returns None when the queue is empty", T("q = Queue(2)\nresult = q.dequeue()", None)),
              ("Wraps round: when the end of the list is reached, the next item goes in position 0",
               T("q = Queue(3)\nfor x in (1, 2, 3):\n    q.enqueue(x)\nq.dequeue()\nq.enqueue(4)\nresult = q.items[0]", 4)),
              ("The front pointer wraps round, so items keep coming out in order",
               T("q = Queue(3)\nout = []\nfor x in range(1, 8):\n    q.enqueue(x)\n    out.append(q.dequeue())\nresult = out", [1, 2, 3, 4, 5, 6, 7]))],
             model="Check for a full or empty queue first. Move the pointer on with (pointer + 1) % size, which wraps from the last position back to 0, and keep count up to date.",
             wrong=[QUEUE.replace("self.rear = (self.rear + 1) % self.size", "self.rear = self.rear + 1"),
                    QUEUE.replace("        if self.isFull():\n            return False\n", "")],
             label="4(a)", filename="queue.py"),
        write("Explain why a circular queue is used, rather than a linear queue, when a queue is stored in an array of fixed size.", 2, [
            ("In a linear queue, positions freed at the front by dequeuing cannot be used again", ["cannot be reused", "cannot be used again", "wasted", "freed", "empty spaces", "not reused"]),
            ("A circular queue wraps its pointers round to the start of the array, so every position is reused", ["wrap", "reuse", "start", "beginning", "every position", "position 0"]),
        ], "In a linear queue the front pointer moves along the array as items are removed, so the positions behind it are never used again and the queue soon reports itself full. A circular queue wraps both pointers back to position 0, so the freed positions are reused.",
              command="Explain", label="4(b)"),

        # ---------------------------------------------------- Section B: a word game
        write("Identify **two** items of data that the game must store about each player.", 2, [
            ("The player's name", ["name"]),
            ("The player's score", ["score", "points"]),
            ("The tiles on the player's rack", ["rack", "tiles", "letters"]),
        ], "Each player's name, their score and the tiles on their rack.",
              command="Identify", label="5(a)", section="Section B",
              section_note="Answer all the questions in this section. They are about a word game.", lead=SCENARIO),
        prog("Write a function wordScore(word) that returns the score for a word: the total of its letter values, doubled if the word has 7 or more letters. Lower case letters are worth the same as upper case letters.",
             VALUES + "\n\ndef wordScore(word):\n    # Return the score for word\n    pass\n", VALUES + "\n\n" + WORD_SCORE,
             [("Returns the total of the letter values: CAT scores 5", "call('wordScore', 'CAT') == 5"),
              ("Counts every letter, including repeats: QUIZ scores 22 and BOOK 10", "call('wordScore', 'QUIZ') == 22 and call('wordScore', 'BOOK') == 10"),
              ("Scores lower case letters as upper case: cat scores 5", "call('wordScore', 'cat') == 5"),
              ("Doubles a word of 7 or more letters: EXAMPLE scores 36 and QUESTION 34", "call('wordScore', 'EXAMPLE') == 36 and call('wordScore', 'QUESTION') == 34"),
              ("Does not double a word of 6 letters: PUZZLE scores 26", "call('wordScore', 'PUZZLE') == 26")],
             model="Convert the word to upper case, add up VALUES[letter] for each letter, then double the total if len(word) >= 7.",
             wrong=[VALUES + "\n\n" + WORD_SCORE.replace("len(word) >= 7", "len(word) > 7"),
                    VALUES + "\n\n" + WORD_SCORE.replace("word.upper()", "word")],
             label="5(b)", filename="game.py"),
        prog("Write a function canMake(word, rack) that returns True if word can be made from the tiles in rack, a string of seven upper case letters, using each tile at most once, and False otherwise. The word may be in upper or lower case.",
             VALUES + "\n\ndef canMake(word, rack):\n    # Return True if word can be made from the tiles in rack\n    pass\n", VALUES + "\n\n" + CAN_MAKE,
             [("Returns True when every letter is on the rack: CAT from TACKLES", "call('canMake', 'CAT', 'TACKLES') == True"),
              ("Returns False when a letter is not on the rack: DOG from TACKLES", "call('canMake', 'DOG', 'TACKLES') == False"),
              ("Uses each tile only once: BOOK cannot be made from BOKERST", "call('canMake', 'BOOK', 'BOKERST') == False"),
              ("Allows a repeated letter when there are enough tiles: BOOK from BOOKEND", "call('canMake', 'BOOK', 'BOOKEND') == True"),
              ("Can use every tile on the rack: TACKLES from SLACKET", "call('canMake', 'TACKLES', 'SLACKET') == True"),
              ("Accepts a word in lower case: cat from TACKLES", "call('canMake', 'cat', 'TACKLES') == True")],
             model="Copy the rack into a list of tiles and remove each letter of the word as it is used, so that a tile cannot be used twice. If a letter is not there, the word cannot be made.",
             wrong=[VALUES + "\n\ndef canMake(word, rack):\n    for letter in word.upper():\n        if letter not in rack:\n            return False\n    return True\n",
                    VALUES + "\n\n" + CAN_MAKE.replace("word.upper()", "word")],
             label="5(c)", filename="game.py"),
        prog("Write a function bestWord(words, rack) that returns the highest scoring word in the list words that can be made from the tiles in rack. It returns an empty string if no word can be made. If two words have the same score, it returns the one that comes first in the list. Use the functions wordScore and canMake, which are given.",
             VALUES + "\n\n" + WORD_SCORE + "\n\n" + CAN_MAKE + "\n\ndef bestWord(words, rack):\n    # Return the best word that can be made\n    pass\n",
             VALUES + "\n\n" + WORD_SCORE + "\n\n" + CAN_MAKE + "\n\n" + BEST_WORD,
             [("Returns the highest scoring word that can be made", "call('bestWord', ['CAT', 'TACK', 'LAST'], 'TACKLES') == 'TACK'"),
              ("Ignores a higher scoring word that cannot be made", "call('bestWord', ['QUIZ', 'CAT'], 'TACKLES') == 'CAT'"),
              ("Returns an empty string when no word can be made", "call('bestWord', ['DOG', 'QUIZ'], 'TACKLES') == ''"),
              ("Returns the first of two words with the same score", "call('bestWord', ['SALT', 'LAST'], 'TACKLES') == 'SALT'"),
              ("Returns an empty string for an empty list of words", "call('bestWord', [], 'TACKLES') == ''"),
              ("Uses the functions canMake and wordScore", "src.count('canMake') >= 2 and src.count('wordScore') >= 2")],
             model="Keep the best word so far and its score, starting from an empty string and 0. Replace them only when a word can be made and scores strictly more, so the first of two equal words is kept.",
             wrong=[VALUES + "\n\n" + WORD_SCORE + "\n\n" + CAN_MAKE + "\n\n" + BEST_WORD.replace("wordScore(word) > bestScore", "wordScore(word) >= bestScore"),
                    VALUES + "\n\n" + WORD_SCORE + "\n\n" + CAN_MAKE + "\n\n" + BEST_WORD.replace("canMake(word, rack) and ", "")],
             label="5(d)", filename="game.py"),
        write("The game checks that every word played is in a dictionary of 270,000 valid words. Explain why the words should be stored in a hash table rather than in a list that is searched with a linear search.", 3, [
            ("A hash table finds a word in constant time, O(1), by calculating its position from the word", ["o(1)", "constant", "calculat", "hash", "directly", "straight to", "position"]),
            ("A linear search is O(n): it may compare the word with all 270,000 words", ["o(n)", "every word", "270", "each word", "one by one", "linear", "all the words"]),
            ("So checking a word is much faster, which matters because a check is made on every turn", ["faster", "quicker", "every turn", "many times", "efficient", "less time"]),
        ], "A hash table calculates where a word would be stored from the word itself, so a lookup takes constant time, O(1), however many words there are. A linear search is O(n): a word near the end, or one that is not valid, means comparing it with all 270,000 words. Words are checked on every turn, so the hash table keeps the game responsive.",
              command="Explain", label="5(e)"),
        prog("Write a class Player. It must have:\n\n- private attributes for the player's name and score, with the score starting at 0\n- a constructor that takes the player's name\n- methods getName() and getScore()\n- a method addWord(word) that adds the score for the word to the player's score, and returns the score for that word, using wordScore.",
             VALUES + "\n\n" + WORD_SCORE + "\n\nclass Player:\n    # Write the class here\n    pass\n",
             VALUES + "\n\n" + WORD_SCORE + "\n\n" + PLAYER,
             [("A new player's score is 0", T("result = Player('Ana').getScore()", 0)),
              ("getName returns the name given to the constructor", T("result = Player('Ana').getName()", "Ana")),
              ("addWord returns the score for the word: 5 for CAT", T("result = Player('Ana').addWord('CAT')", 5)),
              ("addWord adds the word's score to the player's score", T("p = Player('Ana')\np.addWord('CAT')\nresult = p.getScore()", 5)),
              ("The score is a running total over several words", T("p = Player('Ana')\np.addWord('CAT')\np.addWord('QUIZ')\nresult = p.getScore()", 27)),
              ("Each player has a score of their own", T("a = Player('Ana')\nb = Player('Ben')\na.addWord('QUIZ')\nresult = [a.getScore(), b.getScore()]", [22, 0])),
              ("The name and the score are private attributes", T("p = Player('Ana')\nresult = [k for k in vars(p) if not k.startswith('_')]", [])),
              ("addWord uses the function wordScore", "src.count('wordScore') >= 2")],
             model="Two underscores make an attribute private in Python. addWord works out the word's score once, adds it to the running total and returns it.",
             wrong=[VALUES + "\n\n" + WORD_SCORE + "\n\n" + PLAYER.replace("self.__", "self."),
                    VALUES + "\n\n" + WORD_SCORE + "\n\n" + PLAYER.replace("self.__score = self.__score + points", "self.__score = points")],
             label="5(f)", filename="game.py"),
        prog("Write a class Game that keeps the players in a queue, in the order they take turns. Complete the constructor and the methods nextPlayer and winner, following the comments. The function wordScore and the class Player are given.",
             VALUES + "\n\n" + WORD_SCORE + "\n\n" + PLAYER + "\n\n" + GAME_START,
             VALUES + "\n\n" + WORD_SCORE + "\n\n" + PLAYER + "\n\n" + GAME,
             [("nextPlayer returns the first player in the list first", T("g = Game([Player('Ana'), Player('Ben')])\nresult = g.nextPlayer().getName()", "Ana")),
              ("The players then take turns in order", T("g = Game([Player('Ana'), Player('Ben'), Player('Cy')])\nresult = [g.nextPlayer().getName() for turn in range(3)]", ["Ana", "Ben", "Cy"])),
              ("After the last player, the first player has a turn again",
               T("g = Game([Player('Ana'), Player('Ben'), Player('Cy')])\nresult = [g.nextPlayer().getName() for turn in range(5)]", ["Ana", "Ben", "Cy", "Ana", "Ben"])),
              ("Works with two players", T("g = Game([Player('Ana'), Player('Ben')])\nresult = [g.nextPlayer().getName() for turn in range(4)]", ["Ana", "Ben", "Ana", "Ben"])),
              ("winner returns the name of the player with the highest score",
               T("a, b = Player('Ana'), Player('Ben')\na.addWord('CAT')\nb.addWord('QUIZ')\nresult = Game([a, b]).winner()", "Ben")),
              ("winner works when the first player has the highest score",
               T("a, b, c = Player('Ana'), Player('Ben'), Player('Cy')\na.addWord('QUIZ')\nb.addWord('CAT')\nresult = Game([a, b, c]).winner()", "Ana")),
              ("winner is still right after turns have moved the queue round",
               T("a, b, c = Player('Ana'), Player('Ben'), Player('Cy')\ng = Game([a, b, c])\nfor word in ('CAT', 'QUIZ', 'TACK'):\n    g.nextPlayer().addWord(word)\ng.nextPlayer()\nresult = g.winner()", "Ben"))],
             model="A list used as a queue: nextPlayer removes the player at the front and appends them to the back, so the order cycles. winner looks at every player in the queue, whatever order it is in.",
             wrong=[VALUES + "\n\n" + WORD_SCORE + "\n\n" + PLAYER + "\n\n" + GAME.replace("        player = self.__queue.pop(0)\n        self.__queue.append(player)\n        return player",
                                                                                   "        return self.__queue[0]"),
                    VALUES + "\n\n" + WORD_SCORE + "\n\n" + PLAYER + "\n\n" + GAME.replace("return best.getName()", "return best")],
             label="5(g)", filename="game.py"),
        write("Describe how the game could use a stack to let a player undo the words they have played.", 4, [
            ("Each word played, with its score, is pushed onto a stack", ["push", "stack"]),
            ("To undo, the top item is popped: the most recent word", ["pop", "top", "last word", "most recent"]),
            ("Its score is taken off the player's score, and its tiles are returned to the rack", ["subtract", "take off", "taken off", "deduct", "tiles", "rack", "return"]),
            ("Because a stack is last in, first out, repeated undos remove the words in the reverse of the order they were played", ["last in", "lifo", "reverse order", "first out", "in reverse"]),
        ], "Every time a word is played it is pushed onto a stack along with its score. Undo pops the top item, which is always the most recent word, subtracts its score from the player's total and puts its tiles back on the rack. Because a stack is last in, first out, pressing undo again removes the word before that, so the words are undone in the reverse order to the one they were played in.",
              command="Describe", label="5(h)"),
        write("Evaluate the use of object-oriented programming, compared with a procedural approach, for developing the word game.", 9, [
            ("Classes such as Player and Game model the things in the game, so the design matches the problem", ["model", "real", "player", "objects", "represent", "natural", "matches"]),
            ("Encapsulation protects data such as a player's score from being changed incorrectly", ["encapsulat", "private", "protect", "cannot be changed", "getter", "setter"]),
            ("Any number of players can be created as instances of one class, each holding its own data", ["instance", "many players", "each player", "own score", "instantiat", "multiple"]),
            ("Inheritance would let a ComputerPlayer class reuse Player's code", ["inherit", "subclass", "computer player", "reuse", "extend"]),
            ("Polymorphism: a computer player could override a method, such as choosing its word, and be used in the same way", ["polymorphism", "overrid", "override", "different behaviour"]),
            ("Classes can be written and tested separately, by different programmers, which helps maintenance", ["separately", "team", "maintain", "test", "modular", "independent"]),
            ("But object-oriented design needs more planning, and adds code and complexity", ["more complex", "complexity", "planning", "design", "overhead", "more code", "longer"]),
            ("A procedural approach is simpler for small parts, such as wordScore, which need no class", ["procedural", "simpler", "functions", "small", "straightforward"]),
            ("A justified conclusion: object-oriented programming suits this game", ["conclusion", "overall", "therefore", "suitable", "on balance", "recommend"]),
        ], "Object-oriented programming suits the game because its design can mirror the problem: there are players, a game and a queue of turns, and each becomes a class. Encapsulation keeps each player's score private, so it can only change through addWord, which stops other parts of the program corrupting it. Any number of players can be created as instances of Player, each with its own name and score, without any extra code.\n\nThe design is also easy to extend. A ComputerPlayer class could inherit everything from Player and override a method to choose its own word, and through polymorphism the Game class would treat it exactly like a human player. Because each class is self-contained it can be written and tested separately, so a team can share the work and later changes are less likely to break other parts.\n\nThere are costs. The classes and their relationships need careful design before coding starts, and for a small program the classes add code and complexity. Parts of the game, such as wordScore and canMake, are simple calculations that are clearer as ordinary functions, as a procedural approach would write them.\n\nOverall an object-oriented approach is the better choice for the game as a whole, because it has several kinds of object with their own data and behaviour and is likely to grow, while small stateless calculations can stay as plain functions.",
              command="Evaluate", label="5(i)"),
    ],
)

PAPERS = [H446_1B, H446_2B]
