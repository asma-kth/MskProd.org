"""A Level Python: the processor, built as a Little Man Computer emulator."""
from mskbuild.models import Topic, Section, Q, EQ, MP

INPUTS = {}
EXPECT = {}

TOPIC = Topic(
    slug="little-man-computer",
    title="Build a Processor: the Little Man Computer",
    spec="A Level 17",
    icon="i-cpu",
    minutes=65,
    blurb="Write a working processor in Python. Build a Little Man Computer emulator with the real registers, run the fetch-decode-execute cycle, write assembly programs with loops and decisions, build the assembler that turns labels into addresses, then add addressing modes and see how pipelining overlaps instructions.",
    fact="The Little Man Computer was invented in 1965 by Stuart Madnick at MIT to teach how a computer works. A little man sits in a room of 100 numbered mailboxes with a calculator, and follows instructions one at a time. It is still used for teaching because every part of a real processor has a matching part in the room.",
    sections=[
        Section("Inside the processor: fetch, decode, execute", r"""
A processor does one thing, over and over, billions of times a second: it **fetches** an instruction from memory, **decodes** it to see what it means, and **executes** it. This is the **fetch-decode-execute cycle**. To follow it you need to know the places where the processor keeps things, called **registers**:

| Register | Name | Holds |
| **PC** | Program counter | the address of the **next** instruction |
| **MAR** | Memory address register | the address in memory about to be read or written |
| **MDR** | Memory data register | the data just read from memory, or about to be written |
| **CIR** | Current instruction register | the instruction being decoded and executed |
| **ACC** | Accumulator | the result of the most recent calculation |

The **control unit** directs the cycle, and the **ALU** (arithmetic logic unit) does the arithmetic and comparisons. Addresses travel on the **address bus**, data on the **data bus**, and the read and write signals on the **control bus**.

The cycle, as register transfers:

1. **Fetch.** The address in the PC is copied to the MAR.
2. The instruction stored at that address in memory is copied to the MDR.
3. The PC is **incremented**, so it already points to the next instruction.
4. The instruction is copied from the MDR to the CIR.
5. **Decode.** The control unit splits the instruction into an **opcode** (what to do) and an **operand** (what to do it to).
6. **Execute.** The instruction is carried out, which may use the ALU, move data, or change the PC.

You can watch each transfer with a few lines of Python. Here the memory holds one instruction, `505`, which means *load the number in mailbox 5 into the accumulator*:

```python
memory = [0] * 100
memory[0] = 505          # opcode 5 (load), operand 5 (the address)
memory[5] = 42           # the data
pc, acc = 0, 0

print("FETCH")
mar = pc
print("PC -> MAR          MAR =", mar)
mdr = memory[mar]
print("memory[MAR] -> MDR MDR =", mdr)
pc = pc + 1
print("PC + 1 -> PC       PC  =", pc)
cir = mdr
print("MDR -> CIR         CIR =", cir)

print("DECODE")
opcode, operand = divmod(cir, 100)
print("opcode", opcode, "operand", operand)

print("EXECUTE")
acc = memory[operand]
print("memory[", operand, "] -> ACC   ACC =", acc)
```

!key Instructions are just numbers :: The processor has no idea which numbers in memory are instructions and which are data. It treats the number the PC points at as an instruction. Hold the program and its data in the same memory, as here, and you have the **von Neumann architecture**.
"""),
        Section("The Little Man Computer", r"""
The **Little Man Computer** (LMC) is a deliberately tiny processor with the same parts as a real one:

- **100 mailboxes**, numbered 0 to 99, each holding a number. This is the memory (RAM).
- an **accumulator** and a **program counter**
- an **input** and an **output**
- a very small instruction set, each instruction a three digit number: the first digit is the opcode and the last two are the operand, an address.

| Mnemonic | Code | What it does |
| `ADD xx` | 1xx | adds the number in mailbox xx to the accumulator |
| `SUB xx` | 2xx | subtracts the number in mailbox xx from the accumulator |
| `STA xx` | 3xx | stores the accumulator in mailbox xx |
| `LDA xx` | 5xx | loads the number in mailbox xx into the accumulator |
| `BRA xx` | 6xx | **branch always**: sets the PC to xx |
| `BRZ xx` | 7xx | branches to xx only if the accumulator is **zero** |
| `BRP xx` | 8xx | branches to xx only if the accumulator is **zero or positive** |
| `INP` | 901 | waits for an input and puts it in the accumulator |
| `OUT` | 902 | outputs the accumulator |
| `HLT` | 000 | stops |
| `DAT` | none | not an instruction: sets aside a mailbox for data |

Programs are written in **assembly language**: one mnemonic per instruction, with **labels** instead of addresses. The **assembler** turns that into numbers. Here is a complete emulator: an assembler and a processor. Read the `run` function with the table above, and the register names in the previous section.

```python
CODES = {"ADD": 100, "SUB": 200, "STA": 300, "LDA": 500, "BRA": 600,
         "BRZ": 700, "BRP": 800, "INP": 901, "OUT": 902, "HLT": 0}

def assemble(source):
    lines, labels = [], {}
    for raw in source.strip().split("\n"):
        words = raw.split("//")[0].split()          # drop comments
        if not words:
            continue
        if words[0] not in CODES and words[0] != "DAT":
            labels[words[0]] = len(lines)           # pass 1: remember the address of each label
            words = words[1:]
        lines.append(words)
    memory = [0] * 100
    for address, words in enumerate(lines):         # pass 2: turn each line into a number
        name = words[0]
        operand = words[1] if len(words) > 1 else None
        if name == "DAT":
            memory[address] = int(operand) if operand else 0
        elif name in ("INP", "OUT", "HLT"):
            memory[address] = CODES[name]
        else:
            if operand in labels:
                operand = labels[operand]
            memory[address] = CODES[name] + int(operand)
    return memory

NAMES = {1: "ADD", 2: "SUB", 3: "STA", 5: "LDA", 6: "BRA", 7: "BRZ", 8: "BRP"}

def describe(cir):
    if cir in (0, 901, 902):
        return {0: "HLT", 901: "INP", 902: "OUT"}[cir]
    opcode, operand = divmod(cir, 100)
    return NAMES[opcode] + " " + str(operand)

def run(memory, inputs, trace=False, limit=2000):
    memory = list(memory)
    pc = acc = cycles = 0
    inputs, outputs = list(inputs), []
    if trace:
        print("cycle  MAR  MDR  instruction  PC  ACC")
    while cycles < limit:
        mar = pc                          # fetch
        mdr = memory[mar]
        pc = pc + 1
        cir = mdr
        opcode, operand = divmod(cir, 100)    # decode
        cycles = cycles + 1
        if cir == 0:                          # execute
            if trace:
                print(str(cycles).ljust(7), str(mar).ljust(4), str(mdr).ljust(4), "HLT")
            break
        elif opcode == 1:
            acc = acc + memory[operand]
        elif opcode == 2:
            acc = acc - memory[operand]
        elif opcode == 3:
            memory[operand] = acc
        elif opcode == 5:
            acc = memory[operand]
        elif opcode == 6:
            pc = operand
        elif opcode == 7:
            if acc == 0:
                pc = operand
        elif opcode == 8:
            if acc >= 0:
                pc = operand
        elif cir == 901:
            acc = inputs.pop(0)
        elif cir == 902:
            outputs.append(acc)
        if trace:
            print(str(cycles).ljust(7), str(mar).ljust(4), str(mdr).ljust(4), describe(cir).ljust(12), str(pc).ljust(3), acc)
    return outputs

adder = '''
      INP
      STA first
      INP
      ADD first
      OUT
      HLT
first DAT
'''

machine_code = assemble(adder)
print(machine_code[:7])
print("output:", run(machine_code, [7, 5], trace=True))
```

The assembled program is just `901 306 901 106 902 0 0`: seven numbers in the first seven mailboxes. The label `first` became address 6, and `STA first` became `306`.
"""),
        Section("Writing assembly programs", r"""
There is no `if` or `while` in assembly. **Selection and iteration are built from the branch instructions.** A `BRA` is a `goto`; a `BRZ` or `BRP` is a conditional one. Subtracting a number and then testing the sign is how every comparison is made.

Here are three classics in one run. The emulator is the same as before, shortened by taking out the trace.

```python
CODES = {"ADD": 100, "SUB": 200, "STA": 300, "LDA": 500, "BRA": 600,
         "BRZ": 700, "BRP": 800, "INP": 901, "OUT": 902, "HLT": 0}

def assemble(source):
    lines, labels = [], {}
    for raw in source.strip().split("\n"):
        words = raw.split("//")[0].split()
        if not words:
            continue
        if words[0] not in CODES and words[0] != "DAT":
            labels[words[0]] = len(lines)
            words = words[1:]
        lines.append(words)
    memory = [0] * 100
    for address, words in enumerate(lines):
        name = words[0]
        operand = words[1] if len(words) > 1 else None
        if name == "DAT":
            memory[address] = int(operand) if operand else 0
        elif name in ("INP", "OUT", "HLT"):
            memory[address] = CODES[name]
        else:
            if operand in labels:
                operand = labels[operand]
            memory[address] = CODES[name] + int(operand)
    return memory

def run(memory, inputs, limit=2000):
    memory = list(memory)
    pc = acc = cycles = 0
    inputs, outputs = list(inputs), []
    while cycles < limit:
        cir = memory[pc]
        pc = pc + 1
        opcode, operand = divmod(cir, 100)
        cycles = cycles + 1
        if cir == 0:
            break
        elif opcode == 1:
            acc = acc + memory[operand]
        elif opcode == 2:
            acc = acc - memory[operand]
        elif opcode == 3:
            memory[operand] = acc
        elif opcode == 5:
            acc = memory[operand]
        elif opcode == 6:
            pc = operand
        elif opcode == 7 and acc == 0:
            pc = operand
        elif opcode == 8 and acc >= 0:
            pc = operand
        elif cir == 901:
            acc = inputs.pop(0)
        elif cir == 902:
            outputs.append(acc)
    return outputs, cycles

# 1. Countdown: a loop built from BRP
countdown = '''
      INP
loop  OUT
      SUB one
      BRP loop        // still zero or positive: go round again
      HLT
one   DAT 1
'''

# 2. Selection: output the larger of two numbers
larger = '''
          INP
          STA first
          INP
          STA second
          SUB first        // second - first
          BRP secondbig    // zero or positive: second is at least as big
          LDA first
          OUT
          HLT
secondbig LDA second
          OUT
          HLT
first     DAT
second    DAT
'''

# 3. Multiplication by repeated addition: a loop with a counter
multiply = '''
        INP
        STA a
        INP
        STA count
        BRZ done          // multiplying by zero
loop    LDA total
        ADD a
        STA total
        LDA count
        SUB one
        STA count
        BRZ done
        BRA loop
done    LDA total
        OUT
        HLT
a       DAT
count   DAT
total   DAT 0
one     DAT 1
'''

print("countdown from 5:", run(assemble(countdown), [5]))
for first, second in [(3, 8), (9, 4)]:
    print("larger of", first, "and", second, ":", run(assemble(larger), [first, second]))
for a, b in [(6, 7), (5, 0), (9, 1)]:
    result, cycles = run(assemble(multiply), [a, b])
    print(a, "x", b, "=", result[0], "in", cycles, "cycles")
```

Look at the cycle counts. Multiplying is slow because the processor can only add: 6 x 7 means seven trips round the loop. Real processors have hardware multipliers for exactly this reason.

### Turning a flowchart into assembly

A decision becomes a conditional branch past the code it guards. A loop becomes a branch back to its start. Always give the branch a **label**: you never work out an address yourself.

| High-level idea | Assembly pattern |
| `if x >= 0:` | load x, then `BRP` to the code for the true case |
| `if x == 0:` | load x, then `BRZ` |
| `while count > 0:` | at the bottom, subtract 1, test, and branch back |
| `else` | `BRA` over the else code at the end of the true case |
| variable | a labelled `DAT` |

!exam Trace with a table :: In an exam, trace LMC with columns for the PC, the accumulator, and any mailbox that changes, one row per instruction. Write the output when `OUT` runs, not at the end.
"""),
        Section("The assembler: from labels to numbers", r"""
Why have an assembler at all? The processor can only run numbers. Writing `306` instead of `STA first` would be painful and fragile: add one instruction near the top and every address after it moves. The **assembler** does the bookkeeping.

An assembler runs in **two passes** over the source:

1. **Pass one.** Read every line, counting instructions. Whenever a line starts with a label, record the address it has reached in a **symbol table**.
2. **Pass two.** Translate each line into a number, replacing every label with the address from the symbol table.

It needs two passes because a branch may refer to a label that appears *later* in the program, which has no address yet when the branch is read.

```python
CODES = {"ADD": 100, "SUB": 200, "STA": 300, "LDA": 500, "BRA": 600,
         "BRZ": 700, "BRP": 800, "INP": 901, "OUT": 902, "HLT": 0}

def first_pass(source):
    lines, symbols = [], {}
    for raw in source.strip().split("\n"):
        words = raw.split("//")[0].split()
        if not words:
            continue
        if words[0] not in CODES and words[0] != "DAT":
            symbols[words[0]] = len(lines)
            words = words[1:]
        lines.append(words)
    return lines, symbols

def second_pass(lines, symbols):
    memory = []
    for address, words in enumerate(lines):
        name = words[0]
        operand = words[1] if len(words) > 1 else None
        if name == "DAT":
            memory.append(int(operand) if operand else 0)
        elif name in ("INP", "OUT", "HLT"):
            memory.append(CODES[name])
        else:
            if operand in symbols:
                operand = symbols[operand]
            elif operand is None or not operand.isdigit():
                raise ValueError("line " + str(address) + ": no label called " + str(operand))
            memory.append(CODES[name] + int(operand))
    return memory

program = '''
      INP
loop  OUT
      SUB one
      BRP loop
      HLT
one   DAT 1
'''

lines, symbols = first_pass(program)
print("symbol table:", symbols)
print("addr  code  source")
for address, (words, code) in enumerate(zip(lines, second_pass(lines, symbols))):
    print(str(address).ljust(5), str(code).rjust(3).ljust(5), " ".join(words))

try:
    second_pass(*first_pass("LDA nowhere\nHLT"))
except ValueError as problem:
    print("error:", problem)
```

The assembler also reports mistakes before anything runs, such as a branch to a label that does not exist.

### Levels of language

| Level | Example | Translator |
| Machine code | `901 306 901 106` | none: the processor runs it directly |
| Assembly language | `STA first` | **assembler**, one assembly instruction for one machine instruction |
| High-level language | `total = first + second` | **compiler** or **interpreter**, one statement for many instructions |

Assembly is **machine specific**: an LMC program will not run on any other processor, and ARM assembly is different from x86. It is used where speed or size is critical, such as embedded systems and device drivers.
"""),
        Section("Addressing modes and the pipeline", r"""
An instruction's operand is not always an address. The **addressing mode** says how to find the data the operand points to. The LMC only has one, but real processors have several:

| Mode | Operand is... | Example | Used for |
| **Immediate** | the data itself | `LDA #10` loads the number 10 | constants |
| **Direct** | the address of the data | `LDA 10` loads the number held in mailbox 10 | variables |
| **Indirect** | the address of the address of the data | `LDA (11)`: mailbox 11 holds 10, so loads from mailbox 10 | pointers |
| **Indexed** | a base address, plus the index register | `LDA 12,X` with X = 2 loads from mailbox 14 | arrays, lists |

```python
memory = [0] * 20
memory[10] = 42                     # a value
memory[11] = 10                     # a pointer: it holds the address 10
memory[12:15] = [100, 200, 300]     # an array

def operand_value(mode, operand, index=0):
    if mode == "immediate":
        return operand
    if mode == "direct":
        return memory[operand]
    if mode == "indirect":
        return memory[memory[operand]]
    if mode == "indexed":
        return memory[operand + index]

print("immediate 10 ->", operand_value("immediate", 10))
print("direct 10    ->", operand_value("direct", 10))
print("indirect 11  ->", operand_value("indirect", 11))
for x in range(3):
    print("indexed 12 with X =", x, "->", operand_value("indexed", 12, x))
```

Indexed addressing is why an array is fast: element `i` is at the start of the array plus `i`, found in one step.

### The pipeline

In the cycle so far, the processor finishes one instruction before starting the next, so the fetch hardware sits idle while the ALU works. A **pipeline** overlaps them: while instruction 1 is being executed, instruction 2 is being decoded and instruction 3 fetched. Each stage always has something to do.

```python
stages = "FDE"                 # fetch, decode, execute
count = 5
width = count + len(stages) - 1

print("without a pipeline:", count * len(stages), "cycles")
print("with a pipeline:   ", width, "cycles")
print()
for i in range(count):
    print("instruction", i + 1, "." * i + stages + "." * (count - 1 - i))
```

Five instructions take 15 cycles one after another and 7 with a pipeline. Over millions of instructions the pipeline completes close to **one instruction every cycle**. A single instruction still takes three cycles. It is the **throughput** that improves, not the time for one instruction.

The pipeline has weaknesses. A **branch** means the instructions already fetched behind it may be the wrong ones, and must be thrown away (the pipeline is **flushed**), wasting cycles. An instruction that needs the result of the one before it may have to wait.

### Other things that affect performance

| Factor | Effect |
| **Clock speed** | more cycles each second, so more instructions each second |
| **Number of cores** | several instructions streams at once, if the software can use them |
| **Cache** | small, fast memory close to the processor holding recently used data, saving slow trips to RAM |

### Von Neumann and Harvard

The LMC and most computers use the **von Neumann architecture**: one memory for instructions and data, so one bus. It is simple, but instruction fetches and data transfers compete for it. A **Harvard architecture** has separate memories and buses for instructions and data, so both can be fetched at once. It is used in many embedded systems and in the caches of modern processors.
"""),
    ],
    keyterms=[
        ("Fetch-decode-execute cycle", "The repeated cycle in which the processor fetches an instruction from memory, decodes it and carries it out."),
        ("Program counter (PC)", "The register holding the address of the next instruction to be fetched."),
        ("Memory address register (MAR)", "The register holding the address of the memory location about to be read or written."),
        ("Memory data register (MDR)", "The register holding the data that has just been read from, or is about to be written to, memory."),
        ("Current instruction register (CIR)", "The register holding the instruction that is being decoded and executed."),
        ("Accumulator (ACC)", "The register that holds the results of calculations made by the ALU."),
        ("Opcode and operand", "The two parts of an instruction: what to do, and the data or address to do it to."),
        ("Assembly language", "A low-level language in which each instruction is a mnemonic that matches one machine code instruction."),
        ("Assembler", "A translator that converts assembly language into machine code."),
        ("Addressing mode", "The way the operand of an instruction is used to find the data: immediate, direct, indirect or indexed."),
        ("Pipelining", "Overlapping the stages of several instructions, so that fetching, decoding and executing happen at the same time."),
        ("Von Neumann architecture", "A design in which instructions and data are stored in the same memory."),
    ],
    grade="""
Fetch-decode-execute is asked every year, and the marks go to the order and to the register names.

+ Describe the cycle as register transfers: PC to MAR, memory to MDR, PC incremented, MDR to CIR
+ Say what happens at decode (the opcode and operand are separated) and at execute (the instruction is carried out)
+ When tracing assembly, keep a column for every register and variable that changes
+ For addressing modes, give a one line example of the operand and what ends up in the accumulator
+ For pipelining, say throughput improves while the time for one instruction does not, and name the branch problem
""",
    mistakes=[
        "Saying the PC holds the current instruction. It holds the address of the next one, and is incremented during the fetch.",
        "Confusing the MAR, which holds an address, with the MDR, which holds data.",
        "Writing the stages in the wrong order, or leaving out that the PC is incremented.",
        "Mixing up BRZ (branch only if zero) and BRP (branch if zero or positive).",
        "Saying a pipeline makes each instruction faster. It lets more instructions complete in the same time.",
    ],
    quiz=[
        Q("What does the program counter hold?",
          ["The address of the next instruction to be fetched", "The instruction currently being executed", "The result of the last calculation", "The number of instructions executed so far"], 0,
          "The PC is incremented during the fetch stage so that it already points to the next instruction."),
        Q("In the fetch stage, what is the first thing that happens?",
          ["The address in the PC is copied to the MAR", "The instruction is decoded", "The result is written to the ACC", "The MDR is copied to the PC"], 0,
          "The processor needs to send the address of the instruction to memory, and the MAR holds that address."),
        Q("Which register holds the data that has just been read from memory?",
          ["MDR", "MAR", "PC", "CIR"], 0,
          "The memory data register holds the data in transit between the processor and memory."),
        Q("What is the job of the ALU?",
          ["To carry out arithmetic and logical operations", "To fetch instructions from memory", "To store the program counter", "To control the buses"], 0,
          "The arithmetic logic unit does the calculations and comparisons. The control unit directs the cycle."),
        Q("In the LMC, what does the instruction 'BRP loop' do?",
          ["Branches to loop if the accumulator is zero or positive", "Branches to loop if the accumulator is negative", "Branches to loop every time", "Branches to loop if the accumulator is exactly zero"], 0,
          "BRP stands for branch if positive, and in the LMC zero counts as positive."),
        Q("What is the machine code for 'LDA 05' in the LMC?",
          ["505", "305", "105", "905"], 0,
          "LDA has the opcode 5, followed by the two digit operand 05."),
        Q("Why does an assembler need two passes?",
          ["A branch can refer to a label that appears later in the program", "The first pass runs the program and the second checks it", "The first pass removes comments and the second compresses it", "It reads each line twice to be sure"], 0,
          "On the first pass the addresses of all the labels are collected, so the second pass can fill them in."),
        Q("Which addressing mode treats the operand as the data itself?",
          ["Immediate", "Direct", "Indirect", "Indexed"], 0,
          "With immediate addressing, LDA #10 loads the number 10, not the contents of address 10."),
        Q("Which addressing mode is most useful for stepping through the items in an array?",
          ["Indexed", "Immediate", "Direct", "Indirect"], 0,
          "The base address of the array plus the index register gives the address of each item in turn."),
        Q("What is the main benefit of pipelining?",
          ["More instructions are completed in a given time", "Each individual instruction is completed faster", "Less memory is needed", "Branch instructions no longer cause delays"], 0,
          "The stages of different instructions overlap, which increases throughput. A single instruction takes just as long."),
    ],
    exam=[
        EQ("Describe the fetch stage of the fetch-decode-execute cycle, naming the registers that are used.", 4, [
            MP("The address in the program counter (PC) is copied to the memory address register (MAR)", ["pc to mar", "program counter", "copied to the mar", "memory address register"]),
            MP("The instruction at that address is fetched from memory (via the data bus) into the memory data register (MDR)", ["mdr", "memory data register", "data bus", "fetched from memory"]),
            MP("The program counter is incremented", ["incremented", "increased", "pc + 1", "plus one", "next instruction"]),
            MP("The instruction is copied from the MDR to the current instruction register (CIR)", ["cir", "current instruction register", "mdr to"]),
        ], "The address held in the program counter is copied to the memory address register. The instruction stored at that address is then fetched from memory, along the data bus, into the memory data register. The program counter is incremented so that it points to the next instruction. Finally the instruction is copied from the memory data register to the current instruction register, ready to be decoded.",
           command="Describe"),
        EQ("The Little Man Computer program shown is run with the input 7. State the values that are output.", 3, [
            MP("Outputs 7 first (the input value)", ["7"]),
            MP("Each time round the loop 2 is subtracted from the value, so 5 and 3 are output", ["5", "3", "minus 2", "subtracts 2"]),
            MP("The loop ends when the value becomes negative, after 1 has been output: 7, 5, 3, 1", ["7, 5, 3, 1", "7 5 3 1", "1"]),
        ], "The outputs are 7, 5, 3 and 1. The input 7 is stored in num and output. Each time round the loop two is subtracted from num and, while the result is zero or positive, the new value is output. After 1 has been output, subtracting 2 gives -1, which is negative, so BRP does not branch and the program halts.",
           command="State",
           figure="""```text
        INP
        STA num
loop    OUT
        LDA num
        SUB two
        STA num
        BRP loop
        HLT
num     DAT
two     DAT 2
```"""),
        EQ("Write a Little Man Computer program that inputs two numbers and outputs the larger of the two. You may assume that the numbers are different. Use labels for the branch targets and the data locations.", 5, [
            MP("Inputs both numbers and stores them (INP, STA) in labelled locations", ["inp", "sta", "dat"]),
            MP("Subtracts one from the other (SUB) to compare them", ["sub"]),
            MP("Uses a conditional branch (BRP) on the result of the subtraction", ["brp", "brz", "branch"]),
            MP("Loads and outputs the correct number in each case (LDA, OUT)", ["lda", "out"]),
            MP("HLT at the end of each path, and DAT used to define the variables", ["hlt", "dat"]),
        ], r"""```text
        INP
        STA first
        INP
        STA second
        SUB first
        BRP secondbig
        LDA first
        OUT
        HLT
secondbig LDA second
        OUT
        HLT
first   DAT
second  DAT
```

Both numbers are input and stored. The first is subtracted from the second. If the result is positive the second is larger, so the program branches to secondbig, which loads and outputs it. Otherwise the first is larger and is output. Each path ends with HLT.""",
           command="Write"),
        EQ("Explain the difference between immediate addressing and direct addressing. Give an example of each.", 4, [
            MP("Immediate: the operand is the data itself", ["operand is the data", "the value itself", "the data itself", "actual value", "constant"]),
            MP("Example of immediate, such as LDA #10 loads the number 10", ["#10", "loads 10", "loads the number 10", "lda #"]),
            MP("Direct: the operand is the address of the data (a memory location)", ["address", "memory location", "location of the data"]),
            MP("Example of direct, such as LDA 10 loads the contents of address 10", ["lda 10", "contents of", "value stored at", "held in"]),
        ], "In immediate addressing the operand is the data itself, so LDA #10 loads the number 10 into the accumulator. In direct addressing the operand is the address of the data, so LDA 10 loads the number that is stored at memory address 10 into the accumulator.",
           command="Explain"),
        EQ("Discuss how pipelining improves the performance of a processor, and the problems it can introduce.", 6, [
            MP("Pipelining overlaps the stages of different instructions, so that one is fetched while another is decoded and another executed", ["overlap", "at the same time", "fetched while", "different stages", "simultaneously"]),
            MP("The processor can complete close to one instruction per cycle, increasing throughput", ["throughput", "one instruction per cycle", "more instructions", "faster overall"]),
            MP("Each stage of the processor is kept busy rather than waiting", ["busy", "idle", "waiting", "used efficiently"]),
            MP("A branch instruction means that the instructions already fetched may be wrong, so the pipeline must be flushed", ["branch", "flushed", "wrong instructions", "jump", "discarded"]),
            MP("An instruction may depend on the result of a previous one, causing delays (stalls)", ["depend", "result of", "stall", "wait", "hazard"]),
            MP("A reasoned conclusion: the benefits outweigh the problems, and so all modern processors use pipelines", ["conclusion", "outweigh", "overall", "therefore", "benefits"]),
        ], "Pipelining overlaps the stages of consecutive instructions, so that while one instruction is being executed the next is being decoded and the one after that is being fetched. Each part of the processor is kept busy instead of waiting, and the processor can complete close to one instruction every clock cycle, so the throughput increases greatly, although an individual instruction takes the same time as before. There are problems. When there is a branch instruction the instructions already fetched behind it may be the wrong ones, so the pipeline has to be flushed and cycles are wasted. An instruction may also need the result of one in front of it, so it has to wait. Overall, however, the improvement in throughput outweighs these problems, and so all modern processors use pipelines.",
           command="Discuss"),
    ],
)
