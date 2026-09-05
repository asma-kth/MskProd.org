"""OCR GCSE Computer Science J277 revision content.

Written to the J277 specification and sequenced to match the department long
term plan (Year 10 memory and storage first, Year 11 finishing on impacts,
robust programs and trace tables).
"""
from mskbuild.models import Topic, Section, Unit, Course, Q, EQ, MP

# ============================================================ 1.1.1 CPU

T_CPU = Topic(
    slug="architecture-of-the-cpu",
    title="Architecture of the CPU",
    spec="1.1.1",
    icon="i-cpu",
    minutes=32,
    blurb="What the processor is actually for, the job of every component inside it, and the fetch decode execute cycle written the way examiners want to read it.",
    fact="The 'von Neumann' architecture is named after John von Neumann, but the report that described it in 1945 was a draft with only his name on the cover. The ideas came from a whole team at the University of Pennsylvania, and the argument over credit has never fully died down.",
    sections=[
        Section("What the CPU is for", """
The **Central Processing Unit** is the part of a computer that carries out instructions. Everything a computer appears to do, loading a page, playing audio, checking a password, is the CPU executing a very long list of extremely simple instructions, very fast.

That last sentence is worth slowing down on. The CPU cannot do anything clever. It can add two numbers, compare two numbers, copy a number from one place to another, and jump to a different instruction. Complex behaviour comes from doing millions of those simple things per second in the right order.

!key The one sentence definition :: The CPU processes data and instructions, and it does this by continuously fetching, decoding and executing instructions stored in memory.

### The von Neumann architecture

Almost every computer you use follows the **von Neumann architecture**. Its defining feature is the **stored program concept**: instructions and data are held in the *same* memory, and instructions are fetched from memory one at a time to be executed.

Before this idea, a machine had to be physically rewired to do a different job. The stored program concept is why a single laptop can be a word processor one minute and a games console the next.

!warn Do not say the CPU 'stores' data :: The CPU processes data. Storing is what memory and secondary storage do. Registers hold data only for the split second they are being worked on.
"""),
        Section("Components of the CPU", """
You need to know what each part does, and crucially **why** it exists.

### The Arithmetic Logic Unit (ALU)

The ALU carries out all the **arithmetic** and all the **logic** operations.

- Arithmetic means addition, subtraction, and the shifts used for multiplication and division.
- Logic means comparisons and Boolean operations: AND, OR, NOT, and tests such as *is this value greater than that one*.

Every calculation in every program you have ever run happened in an ALU.

### The Control Unit (CU)

The Control Unit is the manager. It:

- decodes the instructions fetched from memory,
- sends control signals to the other components telling them what to do and when,
- controls the flow of data around the CPU and between the CPU and memory,
- keeps everything synchronised to the clock.

### Cache

Cache is a small amount of **very fast memory located inside or extremely close to the CPU**. It holds copies of instructions and data that have been used recently or are likely to be needed next.

Why it exists: RAM is slow compared with the CPU. If the CPU had to wait for RAM every single cycle it would sit idle most of the time. Cache is the buffer that keeps the CPU fed.

| Level | Size | Speed | Position |
| L1 | Smallest, a few KB to a few hundred KB | Fastest | On the CPU core itself |
| L2 | Larger, hundreds of KB to a few MB | Slower than L1 | On the chip, often per core |
| L3 | Largest, several MB or more | Slowest of the three, still far faster than RAM | Shared between all cores |

When the CPU finds what it needs in cache that is a **cache hit**. When it does not, that is a **cache miss** and it has to go out to RAM, which is much slower.

!key Why more cache means better performance :: More cache means more instructions and data can be held close to the CPU, so there are fewer slow trips out to RAM, so the CPU spends more time working and less time waiting.

### Registers

**Registers** are tiny, extremely fast storage locations inside the CPU. Each holds a single value. They are the fastest storage in the entire computer, faster even than cache, because they are part of the CPU itself.

| Register | Full name | What it holds |
| PC | Program Counter | The **memory address** of the *next* instruction to be fetched |
| MAR | Memory Address Register | The **address** currently being read from or written to |
| MDR | Memory Data Register | The **data or instruction** that has just been fetched, or is about to be written |
| ACC | Accumulator | The **result** of calculations carried out by the ALU |

!warn MAR holds an address, MDR holds data :: This is the single most commonly confused pair at GCSE. MAR is the postcode. MDR is the parcel.

### Buses

A **bus** is a set of parallel wires that carries signals between components.

- **Address bus**: carries memory addresses from the CPU to memory. It is *unidirectional*, addresses only travel one way.
- **Data bus**: carries the actual data and instructions. It is *bidirectional*, data travels both ways.
- **Control bus**: carries control signals, such as read, write and clock signals.
"""),
        Section("The fetch decode execute cycle", """
This is the heartbeat of the computer. It repeats billions of times per second, and it never stops while the machine is on.

### Fetch

1. The address of the next instruction is copied from the **Program Counter** into the **MAR**.
2. The **Program Counter is incremented** so it points at the following instruction.
3. The address in the MAR is sent along the **address bus** to main memory.
4. The instruction at that address is sent back along the **data bus** into the **MDR**.

### Decode

5. The instruction in the MDR is passed to the **Control Unit**, which works out what the instruction means: what operation is required and what data it needs.

### Execute

6. The instruction is carried out. This might be an ALU calculation with the result placed in the **Accumulator**, data being written to memory, or a jump that changes the value in the Program Counter.

Then the cycle begins again.

!exam How to earn full marks on a cycle question :: Use the register names, and put them in the right order. A four mark answer that says "it fetches the instruction, decodes it, then executes it" will usually get one mark. An answer that names PC, MAR, MDR, the buses and the CU in sequence gets all four.

!fact Speed check :: A 3 GHz processor completes this cycle around three billion times each second. In the time it takes you to blink, roughly 300 milliseconds, it has run about 900 million cycles.
"""),
    ],
    keyterms=[
        ("CPU", "The component that processes all data and instructions by repeatedly fetching, decoding and executing them."),
        ("Von Neumann architecture", "A design in which instructions and data are stored in the same memory and instructions are fetched one at a time."),
        ("ALU", "Arithmetic Logic Unit. Performs all arithmetic calculations and all logical comparisons."),
        ("Control Unit", "Decodes instructions and sends control signals that coordinate every other component."),
        ("Cache", "Small, very fast memory inside or near the CPU holding recently or frequently used data and instructions."),
        ("Register", "A tiny, extremely fast storage location inside the CPU that holds a single value."),
        ("Program Counter", "The register holding the memory address of the next instruction to be fetched."),
        ("MAR", "Memory Address Register. Holds the address in memory currently being read from or written to."),
        ("MDR", "Memory Data Register. Holds the data or instruction that has just been fetched from, or is about to be written to, memory."),
        ("Accumulator", "The register that stores the result of calculations carried out by the ALU."),
        ("Bus", "A set of parallel wires carrying signals between components. The three buses are address, data and control."),
    ],
    grade="""
Grade 9 answers on this topic do three things that grade 5 answers do not.

**They use register names as verbs, not decoration.** Weak answer: "the CPU gets the instruction from memory". Strong answer: "the address held in the Program Counter is copied to the MAR, and the instruction at that address is returned along the data bus into the MDR".

**They explain the reason, not just the fact.** If a question asks why cache improves performance, the fact is "cache is faster than RAM". The reason is "so the CPU spends fewer cycles waiting for data, which means more instructions completed per second".

**They link components together.** Top answers show that the components form a system: the CU sends the signal, the ALU does the work, the accumulator holds the result, the PC decides what happens next.

+ Be able to write the full fetch decode execute cycle from memory in six numbered steps
+ Be able to state what each register holds in one sentence, without hesitating between MAR and MDR
+ Be able to explain a cache hit and a cache miss and why the difference matters
+ Be able to say why the address bus is unidirectional but the data bus is bidirectional
""",
    mistakes=[
        "Saying the CPU stores data permanently. It does not. Registers hold values only while they are being processed.",
        "Swapping MAR and MDR. The Address Register holds an address, the Data Register holds data.",
        "Forgetting that the Program Counter is incremented during the fetch stage, not at the end of the cycle.",
        "Writing that cache 'makes the CPU faster'. Cache does not change the clock speed. It reduces the time the CPU spends waiting, so more work is completed per second.",
        "Describing the ALU as doing 'everything'. The ALU does arithmetic and logic. Decoding and coordination are the Control Unit's job.",
    ],
    quiz=[
        Q("Which register holds the address of the next instruction to be fetched?",
          ["Program Counter", "Memory Data Register", "Accumulator", "Memory Address Register"], 0,
          "The Program Counter always points at the next instruction. At the start of the fetch stage its value is copied into the MAR and the PC is then incremented."),
        Q("What is the defining feature of the von Neumann architecture?",
          ["Instructions and data are stored in the same memory",
           "The CPU has more than one core",
           "Cache is placed on the processor chip",
           "Data is stored in binary"], 0,
          "The stored program concept means instructions and data share the same memory, so the machine can be reprogrammed by loading different instructions rather than rewiring it."),
        Q("Which component decodes instructions and sends control signals to the rest of the CPU?",
          ["Control Unit", "Arithmetic Logic Unit", "Accumulator", "Cache"], 0,
          "The Control Unit decodes each instruction and coordinates every other component. The ALU only performs arithmetic and logic."),
        Q("A cache miss occurs when:",
          ["The data the CPU needs is not in cache, so it must be fetched from RAM",
           "The cache is full and cannot accept new data",
           "The CPU reads the wrong instruction",
           "Two cores try to use the cache at once"], 0,
          "A miss simply means the required data was not found in cache. The CPU then has to fetch it from the much slower RAM, which costs time."),
        Q("Which bus is unidirectional?",
          ["The address bus", "The data bus", "The control bus", "All three are bidirectional"], 0,
          "Addresses only ever travel from the CPU out to memory, so the address bus carries signals in one direction only. Data travels both ways, so the data bus is bidirectional."),
        Q("Where is the result of an ALU calculation placed?",
          ["The Accumulator", "The MAR", "The Program Counter", "Cache"], 0,
          "The Accumulator is the register that holds results produced by the ALU, ready to be used again or written back to memory."),
        Q("During the fetch stage, when is the Program Counter incremented?",
          ["Straight after its value is copied into the MAR",
           "After the instruction has been executed",
           "Only when a jump instruction runs",
           "It is never incremented, the Control Unit tracks position"], 0,
          "The PC is incremented during fetch, immediately after its value is copied to the MAR, so it is already pointing at the following instruction while the current one is still being processed."),
        Q("Which of these best explains why L1 cache is smaller than L3 cache?",
          ["Very fast memory placed directly on the core is expensive and takes up physical space",
           "L1 only stores instructions, not data",
           "L1 is never used by modern processors",
           "L1 is stored on the hard drive"], 0,
          "Speed, cost and physical area trade off against each other. The closer and faster the memory, the more expensive per byte, so there is less of it."),
        Q("What does the MDR hold immediately after the fetch stage?",
          ["The instruction that has just been retrieved from memory",
           "The address of the next instruction",
           "The result of the last calculation",
           "The control signals for the ALU"], 0,
          "The Memory Data Register holds the actual instruction or data returned along the data bus. The address it came from was in the MAR."),
        Q("A computer executes a jump instruction. Which register is directly changed as a result?",
          ["The Program Counter", "The Accumulator", "The MDR", "The Control Unit"], 0,
          "A jump changes which instruction runs next, and the next instruction is decided by the Program Counter, so the jump writes a new address into the PC."),
    ],
    exam=[
        EQ("Describe the purpose of the Arithmetic Logic Unit within the CPU.", 2, [
            MP("Performs arithmetic operations such as addition and subtraction",
               ["arithmetic", "addition", "add", "subtraction", "calculations", "maths"]),
            MP("Performs logical operations and comparisons such as AND, OR, NOT or greater than",
               ["logic", "logical", "comparison", "compare", "and or not", "boolean"]),
        ], "The ALU carries out all arithmetic operations, such as addition and subtraction, and all logical operations, such as comparing two values or applying AND, OR and NOT. Results produced by the ALU are placed in the accumulator.",
           command="Describe"),
        EQ("Describe the stages of the fetch decode execute cycle. Refer to the registers involved in your answer.", 6, [
            MP("The address of the next instruction is copied from the Program Counter into the MAR",
               ["program counter", "pc to mar", "mar"]),
            MP("The Program Counter is incremented", ["increment", "incremented", "increases by one", "plus one"]),
            MP("The address is sent to memory along the address bus", ["address bus", "sent to memory", "memory address"]),
            MP("The instruction is returned along the data bus into the MDR", ["data bus", "mdr", "memory data register"]),
            MP("The Control Unit decodes the instruction to determine what operation is required",
               ["control unit", "decode", "decoded", "works out"]),
            MP("The instruction is executed, for example the ALU performs a calculation and stores the result in the accumulator",
               ["execute", "executed", "carried out", "alu", "accumulator"]),
        ], "The address of the next instruction is copied from the Program Counter into the Memory Address Register, and the Program Counter is then incremented so that it points at the following instruction. The address in the MAR is sent to main memory along the address bus, and the instruction stored there is returned along the data bus into the Memory Data Register. The Control Unit then decodes that instruction to determine which operation is required and which data it needs. Finally the instruction is executed: if it is a calculation the ALU performs it and the result is placed in the accumulator, and the cycle then repeats.",
           command="Describe"),
        EQ("Explain how increasing the amount of cache memory in a computer can improve its performance.", 4, [
            MP("Cache is much faster to access than RAM", ["faster than ram", "faster access", "fast memory", "quicker than ram"]),
            MP("More cache means more frequently used instructions and data can be stored close to the CPU",
               ["more data", "more instructions", "store more", "frequently used", "recently used"]),
            MP("This increases the cache hit rate, so fewer requests have to go out to RAM",
               ["cache hit", "hit rate", "fewer misses", "less often", "fewer trips"]),
            MP("The CPU therefore spends less time waiting and can execute more instructions per second",
               ["less time waiting", "not idle", "more instructions per second", "spends less time", "faster overall"]),
        ], "Cache is a small amount of memory that is much faster to access than RAM because it sits inside or very close to the CPU. Increasing the amount of cache means more of the instructions and data the CPU uses frequently can be held there, which raises the proportion of requests that are cache hits. Because fewer requests have to travel out to the slower RAM, the CPU spends less time idle waiting for data, so it completes more instructions per second and the computer performs better.",
           command="Explain"),
        EQ("Explain the difference between the Memory Address Register and the Memory Data Register.", 3, [
            MP("The MAR holds a memory address", ["mar holds address", "address register", "holds the address", "location in memory"]),
            MP("The MDR holds the actual data or instruction", ["mdr holds data", "data register", "holds the data", "holds the instruction"]),
            MP("The MAR identifies where in memory to read from or write to, and the MDR carries what is read or written",
               ["where", "what", "read from or write to", "transfers", "contents"]),
        ], "The Memory Address Register holds the address of the memory location that is currently being read from or written to, so it identifies where in memory the CPU is working. The Memory Data Register holds the actual data or instruction that has just been fetched from that location, or that is about to be written to it. In short, the MAR says where and the MDR says what.",
           command="Explain"),
        EQ("A student says: 'The CPU stores all of a computer's data.' Explain why this statement is incorrect.", 3, [
            MP("The CPU processes data rather than storing it long term", ["processes", "process", "not store", "carries out instructions"]),
            MP("Registers and cache inside the CPU hold data only temporarily while it is being worked on",
               ["temporarily", "registers", "cache", "short time", "while being processed", "volatile"]),
            MP("Data is stored in RAM while in use and in secondary storage such as an SSD or hard disk when not in use",
               ["ram", "secondary storage", "ssd", "hard disk", "main memory"]),
        ], "The statement is incorrect because the role of the CPU is to process data and instructions, not to store them. The registers and cache inside the CPU do hold values, but only temporarily while those values are actively being fetched, decoded or executed, and their contents are lost when power is removed. Data that is currently in use is stored in RAM, and data that must be kept when the computer is switched off is stored in secondary storage such as an SSD or a hard disk drive.",
           command="Explain"),
    ],
)
