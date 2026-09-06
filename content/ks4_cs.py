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

# ==================================================== 1.1.2 CPU performance

T_PERF = Topic(
    slug="cpu-performance",
    title="CPU Performance",
    spec="1.1.2",
    icon="i-gauge",
    minutes=22,
    blurb="The three factors that decide how fast a processor is, why doubling the cores does not double the speed, and how to compare two CPUs in an exam answer.",
    fact="Clock speeds stopped climbing around 2005. Chips hit roughly 4 GHz and further increases produced so much heat they became impractical. That physical wall is exactly why manufacturers switched to adding cores instead.",
    sections=[
        Section("The three factors", """
Three characteristics affect CPU performance. You must be able to explain all three and, more importantly, explain the limits of each.

### 1. Clock speed

The **clock** produces a regular electrical pulse. One pulse is one clock cycle, and roughly speaking one instruction is processed per cycle. Clock speed is measured in **hertz**.

- 1 Hz = one cycle per second
- 1 MHz = one million cycles per second
- 1 GHz = one billion cycles per second

A 3.2 GHz processor completes 3.2 billion cycles every second. Higher clock speed means more instructions executed per second, so the computer is faster.

!warn The limit :: Raising clock speed raises heat and power consumption sharply. Beyond a certain point the chip cannot be cooled reliably, which is why clock speeds have barely moved in twenty years. This is the point that earns you the higher marks.

### 2. Number of cores

A **core** is effectively a complete processing unit: it has its own ALU, control unit and registers. A dual core CPU has two, a quad core has four.

Each core can fetch, decode and execute instructions **independently and at the same time**, so in theory four cores complete four times as much work per second.

In practice they do not, for two reasons:

- **Not all software is written to use multiple cores.** A program that runs as a single sequence of instructions can only use one core, no matter how many are available.
- **Cores must communicate and share resources.** Coordinating work between cores, and sharing cache and memory, adds overhead.

!key The exam sentence :: A quad core processor can process four instructions simultaneously, but only if the software has been written to divide the work between cores. Otherwise the extra cores sit idle.

### 3. Cache size

Cache is fast memory close to the CPU holding recently and frequently used instructions and data. Larger cache means a greater proportion of requests are found there rather than in the far slower RAM, so the CPU spends less time waiting.

Beyond a point, extra cache gives smaller and smaller gains, because the most useful data is already in there, and larger cache is slower to search as well as more expensive.
"""),
        Section("Comparing two processors", """
Exam questions often give you two specifications and ask which is better, or ask you to justify a choice for a particular use.

| | Processor A | Processor B |
| Clock speed | 3.8 GHz | 2.9 GHz |
| Cores | 2 | 8 |
| Cache | 4 MB | 16 MB |

There is no single right answer here, and the marks are for the **reasoning**.

- For software that runs as a single thread, such as many older games or a simple script, **Processor A** may well feel faster, because each individual instruction stream is processed more quickly.
- For video rendering, compiling code or running many programs at once, **Processor B** wins comfortably, because the work can be divided across eight cores and it also has four times the cache.

!exam How to answer 'which is better' :: Never just pick one. Say what each is better at, name the factor that causes it, and then commit to an answer for the specific use in the question. A justified answer with a clear conclusion scores highest.

### A note on multi core versus multi threading

You are not required to go deep on threading at GCSE, but you should know that a **thread** is a sequence of instructions. Software that is *multi threaded* can split its work into several threads, which the operating system can then place on different cores. Software that is single threaded cannot, which is the real reason extra cores sometimes make no difference at all.
"""),
    ],
    keyterms=[
        ("Clock speed", "The number of fetch decode execute cycles a processor can perform each second, measured in hertz."),
        ("Hertz (Hz)", "One cycle per second. A gigahertz is one billion cycles per second."),
        ("Core", "A complete processing unit within a CPU with its own ALU, control unit and registers, able to execute instructions independently."),
        ("Multi core processor", "A CPU containing two or more cores, allowing several instructions to be processed at the same time."),
        ("Cache", "Small, fast memory close to the CPU that holds recently or frequently used data and instructions."),
        ("Thread", "A single sequence of instructions that can be scheduled onto a core."),
    ],
    grade="""
The difference between a level 5 and a level 9 answer on this topic is almost entirely about **stating the limitation**.

Anyone can write "more cores means faster". The mark for AO2 comes from writing "more cores means faster *only if the software is written to use them*, because a single threaded program will run on one core and leave the others idle".

Do the same for each factor:

| Factor | The basic point | The point that gets the extra mark |
| Clock speed | More cycles per second, so more instructions per second | Heat and power rise sharply, so clock speed cannot be raised indefinitely |
| Cores | Several instructions processed simultaneously | Only if software is multi threaded, and coordination between cores adds overhead |
| Cache | Fewer slow trips out to RAM | Diminishing returns, and larger cache is more expensive and slower to search |

+ Practise writing a three sentence justification comparing two named processors for a stated purpose
+ Always finish a compare question with a clear decision, not a shrug
""",
    mistakes=[
        "Writing that a quad core processor is always four times faster than a single core one. It is not, because most tasks cannot be perfectly divided.",
        "Confusing clock speed with the number of instructions. One cycle is roughly one instruction, but they are not the same thing.",
        "Saying cache 'stores more programs'. Cache stores small amounts of frequently or recently used data and instructions, not whole programs.",
        "Giving a comparison answer with no conclusion. If the question says justify, you must commit to a choice.",
        "Using the word 'faster' with no explanation of what is actually happening.",
    ],
    quiz=[
        Q("A processor has a clock speed of 2.5 GHz. Approximately how many cycles does it complete each second?",
          ["2.5 billion", "2.5 million", "2500", "2.5 trillion"], 0,
          "Giga means billion, so 2.5 GHz is 2.5 billion cycles per second."),
        Q("Why might a quad core processor not run a program four times faster than a single core processor?",
          ["The program may be single threaded and unable to use more than one core",
           "Cores can only run at a quarter of the clock speed",
           "Extra cores are only used for graphics",
           "The operating system limits programs to one core"], 0,
          "If software has not been written to divide its work into threads, only one core does the work and the rest stay idle."),
        Q("What is the main practical limit on raising clock speed?",
          ["Heat and power consumption rise sharply", "Cache becomes too small",
           "The address bus becomes too narrow", "Programs stop being compatible"], 0,
          "Higher clock speeds generate substantially more heat and draw more power, and beyond about 4 GHz this becomes very difficult to cool reliably."),
        Q("Which component would most improve performance for a computer that constantly re-uses the same small set of instructions?",
          ["A larger cache", "A larger hard disk", "More USB ports", "A higher resolution monitor"], 0,
          "Repeatedly used instructions are exactly what cache is for. A larger cache raises the hit rate so the CPU waits on RAM less often."),
        Q("A core contains its own:",
          ["ALU, control unit and registers", "Hard disk and RAM",
           "Operating system", "Power supply"], 0,
          "A core is a full processing unit, which is why it can fetch, decode and execute independently of the other cores."),
        Q("Processor A is 4 GHz dual core. Processor B is 3 GHz octa core. Which is likely better for rendering a video?",
          ["Processor B, because rendering can be split across many cores",
           "Processor A, because clock speed is all that matters",
           "They will perform identically",
           "Neither, rendering only uses the GPU"], 0,
          "Video rendering divides naturally into independent chunks, so it scales well across cores. Eight slower cores beat two faster ones here."),
        Q("What does a cache hit rate of 95 per cent mean?",
          ["95 per cent of the CPU's requests were satisfied by cache rather than RAM",
           "The cache is 95 per cent full",
           "95 per cent of the cache is L1",
           "The CPU is running at 95 per cent capacity"], 0,
          "Hit rate is the proportion of requests found in cache. A high hit rate means few slow trips out to RAM."),
        Q("Which statement about clock speed is correct?",
          ["It measures how many cycles the CPU performs per second",
           "It measures how much data the CPU can store",
           "It measures how many cores the CPU has",
           "It measures the width of the data bus"], 0,
          "Clock speed is a frequency: cycles per second, measured in hertz. It says nothing about storage or core count."),
        Q("Why does adding a fourth level of cache give little benefit on most systems?",
          ["The most useful data is already cached, so returns diminish and larger cache is slower to search",
           "Processors can only physically hold three caches",
           "Cache above L3 is not supported by any operating system",
           "It would make the clock speed drop to zero"], 0,
          "Cache benefits follow diminishing returns. Once the frequently used data is in cache, extra capacity adds cost and search time for little gain."),
        Q("A user runs many applications at once and complains of slowdown. Which upgrade most directly addresses this?",
          ["A processor with more cores", "A faster monitor",
           "A larger secondary storage device", "A longer network cable"], 0,
          "Running many applications simultaneously is exactly the workload multiple cores are designed for, since each core can handle different processes at the same time."),
    ],
    exam=[
        EQ("State what is meant by the clock speed of a processor.", 2, [
            MP("The number of cycles or instructions performed each second", ["cycles per second", "instructions per second", "number of cycles", "how many cycles"]),
            MP("Measured in hertz, commonly gigahertz", ["hertz", "hz", "gigahertz", "ghz"]),
        ], "Clock speed is the number of fetch decode execute cycles a processor completes each second. It is measured in hertz, and modern processors are usually quoted in gigahertz, where one gigahertz is one billion cycles per second.",
           command="State"),
        EQ("Explain why a computer with a quad core processor may not run a particular program four times faster than a computer with a single core processor of the same clock speed.", 4, [
            MP("The program must be written to divide work across multiple cores", ["written", "multi threaded", "threads", "designed to use", "programmed to use", "software support"]),
            MP("A single threaded program can only run on one core, leaving the others idle", ["single threaded", "one core", "idle", "unused", "only one"]),
            MP("Some tasks are sequential and cannot be split because later steps depend on earlier results", ["sequential", "depend", "cannot be split", "in order", "one after another"]),
            MP("Coordinating cores and sharing cache or memory adds overhead", ["overhead", "coordinate", "communicate", "share", "sharing resources", "manage"]),
        ], "A quad core processor can only deliver four times the throughput if the work can actually be divided between the four cores. This requires the program to be written as multiple threads. If the program is single threaded then it runs on one core and the other three sit idle, so there is no gain at all. Even in multi threaded programs, some parts of a task are inherently sequential because later steps depend on results produced earlier, and those parts cannot be run in parallel. In addition, the cores must communicate with each other and share cache and memory bandwidth, and this coordination adds overhead that reduces the theoretical speed increase.",
           command="Explain"),
        EQ("A video editing company must choose between Processor X at 4.1 GHz with two cores and 4 MB cache, and Processor Y at 3.0 GHz with eight cores and 16 MB cache. Recommend a processor and justify your choice.", 6, [
            MP("Recommends Processor Y", ["processor y", "y", "eight core", "octa"]),
            MP("Video editing and rendering can be divided into independent tasks across cores", ["divided", "split", "parallel", "simultaneously", "at the same time", "independent"]),
            MP("Eight cores process far more instructions simultaneously than two", ["eight cores", "more cores", "four times", "simultaneously"]),
            MP("The larger 16 MB cache raises the hit rate so the CPU waits on RAM less often", ["cache", "16 mb", "hit rate", "less waiting", "larger cache"]),
            MP("Acknowledges that Processor X has the higher clock speed and would be better for single threaded work", ["clock speed", "4.1", "single threaded", "processor x", "higher clock"]),
            MP("Concludes that the parallel nature of video work outweighs the clock speed advantage", ["outweigh", "overall", "therefore", "more important", "conclusion", "better choice"]),
        ], "Processor Y is the better choice for this company. Video editing and rendering split naturally into independent tasks, such as processing separate frames or segments, so the work can be shared across all eight cores and run simultaneously. Eight cores at 3.0 GHz will therefore complete far more instructions per second on this workload than two cores at 4.1 GHz. Processor Y also has 16 MB of cache rather than 4 MB, which raises the cache hit rate and means the CPU spends less time waiting for data from RAM, and video work moves large amounts of data. Processor X does have the higher clock speed, and it would be the better choice for single threaded software where only one core can be used. However, because video rendering parallelises well, the four times increase in core count and the four times increase in cache outweigh the roughly 37 per cent clock speed advantage, so Processor Y should be chosen.",
           command="Justify"),
        EQ("Explain how increasing cache size can improve processor performance, and give one reason why simply making the cache as large as possible is not the best solution.", 4, [
            MP("More frequently or recently used data and instructions can be stored close to the CPU", ["more data", "frequently used", "recently used", "store more", "close to"]),
            MP("More requests are satisfied by cache rather than the slower RAM", ["cache hit", "fewer misses", "instead of ram", "not go to ram", "hit rate"]),
            MP("The CPU spends less time waiting so completes more instructions per second", ["less waiting", "idle", "more instructions", "faster", "not wait"]),
            MP("Cache is expensive per byte, takes physical space on the chip, and larger caches take longer to search, so returns diminish", ["expensive", "cost", "space", "slower to search", "diminishing", "physical"]),
        ], "Increasing cache size means more of the instructions and data the processor uses frequently can be held in memory that sits inside or very close to the CPU. This raises the cache hit rate, so a greater proportion of requests are satisfied without going out to the much slower RAM, and the CPU therefore spends less time idle and completes more instructions per second. However, making the cache as large as possible is not the best solution because very fast memory is expensive per byte and takes up physical space on the processor die, and a larger cache also takes longer to search, so the performance gains get smaller and smaller as size increases.",
           command="Explain"),
        EQ("Describe one similarity and one difference between a dual core processor and two separate single core processors installed in the same computer.", 3, [
            MP("Both allow two instructions to be processed at the same time", ["two instructions", "simultaneously", "at the same time", "parallel", "both can process"]),
            MP("A dual core processor has both cores on a single chip", ["same chip", "one chip", "single chip", "same die", "integrated"]),
            MP("Cores on one chip communicate faster and can share cache, reducing latency", ["share cache", "communicate", "faster", "latency", "closer", "shared"]),
        ], "A similarity is that both arrangements allow two instructions to be fetched, decoded and executed at the same time, so both can genuinely process work in parallel. A key difference is that a dual core processor has both cores built onto a single chip, which means they are physically much closer together and can share cache and communicate over very short internal connections. Two separate processors must communicate across the motherboard, which is slower, so the dual core arrangement generally has lower latency when cores need to work together.",
           command="Describe"),
    ],
)

# ================================================== 1.1.3 Embedded systems

T_EMBED = Topic(
    slug="embedded-systems",
    title="Embedded Systems",
    spec="1.1.3",
    icon="i-timer",
    minutes=18,
    blurb="What an embedded system is, how it differs from a general purpose computer, and why your washing machine does exactly one job extremely reliably.",
    fact="A modern car contains somewhere between 50 and 150 embedded systems. The engine management unit alone runs continuously and makes thousands of adjustments per second, and it has to be right every time, because there is no restart button at 70 mph.",
    sections=[
        Section("What an embedded system is", """
An **embedded system** is a computer built into a larger device to perform a **single specific task**, or a small set of dedicated tasks.

The computer is not the product. The washing machine is the product, and the computer inside it exists only to run the wash cycles.

### Everyday examples

- Washing machine, dishwasher and microwave controllers
- Traffic light controllers
- Central heating thermostats
- Engine management systems in cars
- Digital cameras
- Fitness trackers
- Pacemakers
- Vending machines
- Domestic burglar alarms

!warn A laptop is not an embedded system :: Neither is a smartphone. They run many different programs chosen by the user, which makes them **general purpose** computers. The test is: can the user install whatever software they like?
"""),
        Section("Embedded versus general purpose", """
| | Embedded system | General purpose computer |
| Purpose | One dedicated task | Many different tasks |
| Software | Fixed, usually stored in ROM, rarely changed by the user | Installed and removed freely by the user |
| Hardware | Minimal, only what the task requires | Full range: keyboard, screen, expansion slots |
| Processing power | Low, matched exactly to the job | High, must cope with unpredictable demands |
| Power consumption | Very low | Comparatively high |
| Cost | Cheap to manufacture in volume | Expensive |
| Physical size | Small, often a single chip | Large |
| Operating system | Often none, or a small real time OS | Full operating system such as Windows or macOS |
| Reliability | Very high, the task is fixed and well tested | Lower, more can go wrong |
| User interface | Very limited: a few buttons and lights | Rich: keyboard, mouse, touchscreen, monitor |

### Why the differences exist

Because the task never changes, the designer knows exactly what the system needs. That makes it possible to strip out everything else. The result is cheaper, smaller, uses less power, generates less heat, and is far less likely to fail, because there is far less to fail.

!key The advantage sentence examiners want :: Because an embedded system performs only one dedicated task, its hardware and software can be designed and optimised specifically for that task, which makes it cheaper, smaller, more power efficient and more reliable than a general purpose computer doing the same job.

### The trade off

The flexibility is gone. You cannot make your washing machine play music, and updating the software may be difficult or impossible without replacing the chip. For the manufacturer that is a feature, not a bug: fewer possibilities means fewer things that can go wrong.
"""),
    ],
    keyterms=[
        ("Embedded system", "A computer built into a larger device to perform one dedicated task or a small set of dedicated tasks."),
        ("General purpose computer", "A computer designed to run many different programs chosen by the user, such as a laptop or desktop."),
        ("ROM", "Read only memory. Non volatile memory holding the fixed program an embedded system runs."),
        ("Real time system", "A system that must respond to inputs within a guaranteed time limit, such as an anti lock braking system."),
        ("Dedicated function", "The single specific job an embedded system is built to carry out."),
    ],
    grade="""
This topic is short, so the marks are won on precision.

**Choose your examples carefully.** A smartphone is a trap: it looks like a small device but it is general purpose. Safe examples are a washing machine controller, a traffic light system, a microwave and a central heating thermostat.

**Give reasons that follow from the single task.** Everything good about an embedded system, low cost, small size, low power, high reliability, follows from the same root cause: the task is fixed, so the design can be stripped back to exactly what is needed. Say that link explicitly.

**Know the disadvantage.** Higher mark questions often ask for a drawback. The answer is loss of flexibility: the system cannot be repurposed and the software is usually difficult or impossible for the user to update.

+ Be able to give three correct examples instantly
+ Be able to state four differences from a general purpose computer in a table format
+ Be able to explain one advantage and one disadvantage with reasons
""",
    mistakes=[
        "Giving a smartphone or tablet as an example. They run user chosen software, so they are general purpose.",
        "Saying an embedded system 'has no operating system'. Many have a small real time operating system. Say it is often minimal or absent rather than never present.",
        "Writing that embedded systems are 'less powerful' as if it is a flaw. It is a deliberate design choice, because the task does not need more power.",
        "Forgetting the disadvantage. Loss of flexibility and difficulty of updating is worth a mark in a two sided question.",
    ],
    quiz=[
        Q("Which of these is an embedded system?",
          ["A washing machine controller", "A laptop", "A desktop PC", "A games console"], 0,
          "The washing machine controller does one fixed job. The others run whatever software the user chooses, which makes them general purpose."),
        Q("Embedded systems are usually cheaper to produce than general purpose computers because:",
          ["They only need the hardware required for one specific task",
           "They are always made from recycled parts",
           "They have no processor",
           "They are sold in smaller quantities"], 0,
          "Knowing the task in advance lets the designer remove everything unnecessary, which cuts component cost and manufacturing complexity."),
        Q("Where is the program of an embedded system typically stored?",
          ["ROM", "A removable USB stick", "Cache", "The cloud"], 0,
          "The program is fixed and must survive a power cut, so it is held in non volatile ROM rather than in volatile memory."),
        Q("Which is a disadvantage of an embedded system?",
          ["It cannot easily be updated or repurposed for a different task",
           "It uses too much electricity",
           "It is physically very large",
           "It requires a full operating system"], 0,
          "Fixed function is the whole point, and the price of that is flexibility. Updating often means replacing hardware."),
        Q("Why is an embedded system generally more reliable than a general purpose computer doing the same job?",
          ["It runs a single, fixed, thoroughly tested program with far fewer things that can go wrong",
           "It has more RAM", "It uses a faster processor", "It is connected to the internet"], 0,
          "Fewer components and one fixed program means a far smaller number of possible failure points, and that program can be tested exhaustively."),
        Q("A traffic light system must change lights within a guaranteed time. This makes it an example of:",
          ["A real time system", "A distributed system", "A general purpose computer", "A virtual machine"], 0,
          "Real time means the response must happen within a guaranteed time limit, which is exactly the requirement for safety critical control systems."),
        Q("Which feature would you NOT expect to find in a typical embedded system?",
          ["A slot for the user to install additional software",
           "A microcontroller", "Sensors", "ROM"], 0,
          "User installable software is a defining feature of general purpose computers. Embedded systems run fixed firmware."),
        Q("An embedded system usually consumes less power than a general purpose computer because:",
          ["Its processor and hardware are matched to a single low demand task",
           "It only runs at night", "It has no power supply", "It is smaller in colour depth"], 0,
          "The processor can be chosen to be exactly powerful enough for the task and no more, which keeps power draw and heat very low."),
        Q("Which pair are both embedded systems?",
          ["A microwave oven controller and a central heating thermostat",
           "A tablet and a smartwatch app store",
           "A desktop PC and a games console",
           "A web server and a laptop"], 0,
          "Both the microwave controller and the thermostat perform one dedicated task with fixed software."),
        Q("What is the best description of the user interface on a typical embedded system?",
          ["Very limited, often just a few buttons and indicator lights",
           "A full graphical desktop", "A command line with full shell access", "There is never any interface"], 0,
          "Interfaces are cut back to what the single task needs, which is usually a small set of physical controls and simple feedback."),
    ],
    exam=[
        EQ("Define the term embedded system.", 2, [
            MP("A computer system built into a larger device", ["built into", "part of", "inside", "within a device", "larger device"]),
            MP("Designed to perform one specific or dedicated task", ["one task", "specific task", "dedicated", "single function", "particular purpose"]),
        ], "An embedded system is a computer system that is built into a larger device or machine, and it is designed to carry out one specific dedicated task rather than a range of different tasks chosen by the user.",
           command="Define"),
        EQ("Give two examples of embedded systems and, for each, state the task it performs.", 4, [
            MP("First valid example named, such as a washing machine controller", ["washing machine", "microwave", "traffic light", "thermostat", "dishwasher", "pacemaker", "camera", "vending machine", "engine management", "alarm"]),
            MP("Task of the first example stated", ["controls", "manages", "monitors", "runs the cycle", "regulates", "adjusts"]),
            MP("Second valid example named", ["washing machine", "microwave", "traffic light", "thermostat", "dishwasher", "pacemaker", "camera", "vending machine", "engine management", "alarm"]),
            MP("Task of the second example stated", ["controls", "manages", "monitors", "sequence", "temperature", "timing", "regulates"]),
        ], "One example is the controller inside a washing machine, which manages the wash cycle by controlling the water inlet valve, the drum motor speed and the heating element according to the programme the user has selected. A second example is a central heating thermostat, which monitors the temperature reported by a sensor and switches the boiler on or off to keep the room at the target temperature.",
           command="Give"),
        EQ("Explain two advantages of using an embedded system rather than a general purpose computer to control a microwave oven.", 4, [
            MP("Cheaper to produce because only the hardware needed for the task is included", ["cheaper", "cost", "less expensive", "low cost", "inexpensive"]),
            MP("Reason linked to the fixed task, such as no need for a screen, keyboard or expansion", ["only what is needed", "no keyboard", "no monitor", "minimal hardware", "one task", "specific task"]),
            MP("More reliable because the single fixed program can be tested thoroughly and there is less to go wrong", ["reliable", "reliability", "less to go wrong", "fewer faults", "tested", "stable"]),
            MP("Smaller and lower power, so it fits inside the appliance and generates little heat", ["smaller", "compact", "less power", "low power", "energy", "fits inside", "less heat"]),
        ], "The first advantage is cost. Because the system only ever has to run the microwave, the manufacturer can include just the processing power, memory and inputs the task requires, with no monitor, keyboard or expansion slots, so the unit is far cheaper to produce in volume. The second advantage is reliability. The embedded system runs a single fixed program stored in ROM, which can be tested exhaustively before release, and there are far fewer hardware and software components that could fail than in a general purpose computer, so the microwave is much less likely to crash or need maintenance.",
           command="Explain"),
        EQ("Describe two differences between an embedded system and a general purpose computer.", 4, [
            MP("Embedded systems perform one dedicated task, general purpose computers run many different programs", ["one task", "dedicated", "many programs", "range of tasks", "different tasks"]),
            MP("Embedded software is fixed and usually stored in ROM, general purpose software is installed by the user", ["rom", "fixed", "cannot be changed", "installed by the user", "user chooses", "install software"]),
            MP("Embedded systems use minimal hardware and have limited interfaces, general purpose computers have full input and output devices", ["minimal hardware", "few buttons", "limited interface", "keyboard", "monitor", "full", "peripherals"]),
            MP("Embedded systems use less power and are physically smaller", ["less power", "smaller", "compact", "low power", "energy efficient"]),
        ], "The first difference is purpose. An embedded system is built to carry out one dedicated task, such as controlling a set of traffic lights, whereas a general purpose computer such as a laptop is designed to run many different programs chosen by the user. The second difference is how the software is handled. In an embedded system the program is fixed and usually stored in ROM, so it is not intended to be changed by the user, while on a general purpose computer the user installs, updates and removes applications freely. This also means embedded systems need only minimal hardware and a very limited interface, often just a few buttons and lights, whereas a general purpose computer needs a keyboard, a monitor and support for a wide range of peripherals.",
           command="Describe"),
        EQ("A manufacturer is deciding whether to control a new coffee machine using an embedded system or a small general purpose computer. Evaluate the use of an embedded system for this purpose.", 6, [
            MP("Embedded system is cheaper to produce per unit", ["cheaper", "cost", "less expensive", "cheap to manufacture"]),
            MP("Smaller physical size fits inside the machine and uses less power", ["smaller", "size", "fits", "less power", "low power"]),
            MP("More reliable because a single tested program runs on minimal hardware", ["reliable", "reliability", "less to go wrong", "tested", "stable", "fewer failures"]),
            MP("Disadvantage: difficult or impossible for the user to update the software", ["update", "cannot be changed", "difficult to update", "fixed", "no updates", "replace the chip"]),
            MP("Disadvantage: no flexibility, the system cannot be repurposed or given new features later", ["flexibility", "cannot be repurposed", "new features", "limited", "inflexible"]),
            MP("Reaches a supported conclusion for this specific product", ["therefore", "overall", "conclusion", "best choice", "should use", "recommend"]),
        ], "An embedded system is a strong choice here. Because a coffee machine only ever needs to run a fixed set of brewing programmes, the manufacturer can specify exactly the processing power, memory and inputs required, which makes each unit significantly cheaper to produce than fitting a general purpose computer. The reduced hardware is also physically smaller, so it fits easily inside the casing, and it draws far less power and generates less heat, which matters in an appliance that already produces heat. Reliability is the strongest argument: a single fixed program running on minimal hardware can be tested exhaustively, and there are far fewer components that could fail, so warranty returns should be low. There are drawbacks. The software is normally stored in ROM, so fixing a bug or adding a new drink option after release may require physically replacing a chip or recalling units, and the system cannot be repurposed for anything else. On balance, because the function of a coffee machine is stable and well defined, and cost and reliability matter far more to the manufacturer than future flexibility, the embedded system is the better choice, provided the design allows firmware to be updated during servicing.",
           command="Evaluate"),
    ],
)

# ==================================================== 1.2.1 Primary storage

T_PRIMARY = Topic(
    slug="primary-storage",
    title="Primary Storage: RAM, ROM and Virtual Memory",
    spec="1.2.1",
    icon="i-memory",
    minutes=28,
    blurb="Why the computer needs memory at all, the real difference between RAM and ROM, and what virtual memory is actually doing when your machine slows to a crawl.",
    fact="The word RAM stands for random access memory, and the random part means any location can be read in the same amount of time. Old magnetic tape was the opposite: to reach the end you had to wind through everything before it.",
    sections=[
        Section("Why primary memory exists", """
The CPU can only fetch instructions and data from **primary memory**. It cannot read directly from a hard disk or an SSD.

So when you open a program, the operating system copies it from secondary storage into RAM, and the CPU works from there.

Why not just run it from the hard drive? Because secondary storage is thousands of times slower. If the CPU had to wait for a disk on every instruction, a 3 GHz processor would perform like a machine from the 1970s.

!key The definition to memorise :: Primary storage is memory that the CPU can access directly. It holds the data and instructions that are currently in use.

### The memory hierarchy

Speed and cost pull in opposite directions, which produces a hierarchy:

| Level | Speed | Capacity | Cost per byte | Volatile |
| Registers | Fastest | A few bytes | Highest | Yes |
| Cache | Very fast | KB to MB | Very high | Yes |
| RAM | Fast | GB | Moderate | Yes |
| Secondary storage | Slow | GB to TB | Low | No |

The pattern is consistent: the closer to the CPU, the faster, the smaller and the more expensive.
"""),
        Section("RAM", """
**RAM**, random access memory, is the computer's main memory.

- It holds the **operating system**, the **applications currently running** and the **data those applications are using**.
- It is **volatile**: its contents are lost the moment power is removed.
- It can be **read from and written to**.
- It is much faster than secondary storage but slower than cache.

!warn Volatile means power, not speed :: Volatile does not mean unstable or unreliable. It means the contents disappear when the power goes. This is why unsaved work is lost in a power cut.

### What happens when RAM fills up

RAM is finite. Open enough programs and it runs out. The computer does not simply stop, it starts using **virtual memory**, and that is when things get slow.
"""),
        Section("ROM", """
**ROM**, read only memory, holds instructions that must be available the instant the machine is switched on.

- It is **non volatile**: contents are kept when the power is off.
- It is **read only** in normal use, so the contents cannot be accidentally overwritten.
- It is small, typically a few megabytes at most.
- It contains the **bootstrap** or **BIOS**: the start up instructions.

### The boot process

1. The computer is switched on.
2. The CPU fetches the boot program from ROM, because RAM is empty at this point.
3. The boot program checks the hardware is working, a power on self test.
4. It then locates the operating system on secondary storage and **copies it into RAM**.
5. Control is handed to the operating system, which is now running from RAM.

!exam The classic question :: "Explain why a computer needs both RAM and ROM." The answer hinges on volatility. RAM is volatile, so at switch on it is empty and cannot hold the start up instructions. ROM is non volatile, so it still holds the boot program. ROM alone is not enough because it cannot be written to, and running programs constantly need to write data.

| | RAM | ROM |
| Full name | Random access memory | Read only memory |
| Volatile | Yes | No |
| Read and write | Both | Read only in normal use |
| Typical size | 8 GB to 32 GB | A few MB |
| Contents | Operating system, open programs, data in use | Boot program, BIOS |
| Speed | Fast | Fast |
"""),
        Section("Virtual memory", """
**Virtual memory** is a section of secondary storage used as if it were RAM, when RAM is full.

### How it works

1. RAM becomes full but another program needs to be loaded.
2. The operating system identifies data in RAM that has not been used recently.
3. That data is **moved out to a dedicated area of secondary storage**, called the swap file or page file.
4. The freed RAM is used for the new program.
5. If the moved out data is needed again, it is **swapped back into RAM**, which may require moving something else out.

### Why it makes the computer slow

Secondary storage is far slower than RAM. Every swap means writing data out and reading data in. If the machine is very short on RAM this can happen constantly, a condition called **disk thrashing**, where the computer spends more time moving data than doing useful work.

!key The trade off in one sentence :: Virtual memory lets a computer run more programs than its RAM can physically hold, at the cost of a large drop in speed, because secondary storage is much slower than RAM.

### The fix

Adding more RAM. With enough RAM, virtual memory is rarely needed, so the swapping stops.
"""),
    ],
    keyterms=[
        ("Primary storage", "Memory the CPU can access directly, holding data and instructions currently in use."),
        ("RAM", "Random access memory. Volatile main memory holding the operating system, running programs and data in use."),
        ("ROM", "Read only memory. Non volatile memory holding the boot program the computer needs at switch on."),
        ("Volatile", "Loses its contents when power is removed."),
        ("Non volatile", "Keeps its contents when power is removed."),
        ("Virtual memory", "An area of secondary storage used as extra RAM when RAM is full."),
        ("Swap file", "The area of secondary storage where data moved out of RAM is held."),
        ("Bootstrap", "The small start up program held in ROM that loads the operating system into RAM."),
        ("Disk thrashing", "Excessive swapping between RAM and virtual memory, which makes a computer extremely slow."),
    ],
    grade="""
The high marks on this topic come from **causal chains**. A grade 9 answer explains virtual memory as a sequence of events with a consequence, not as a definition.

**Weak**: "Virtual memory is part of the hard drive used as RAM. It makes the computer slow."

**Strong**: "When RAM becomes full, the operating system moves data that has not been used recently out to the swap file on secondary storage, freeing RAM for the new program. Because secondary storage is far slower than RAM, every subsequent access to that data requires it to be swapped back in, and if this happens continuously the computer spends most of its time transferring data rather than executing instructions."

Notice the second version names the trigger, the mechanism, the location and the consequence.

+ Be able to explain why ROM is needed given that RAM exists, using volatility
+ Be able to describe the boot sequence in four steps
+ Be able to explain the cause of slowdown when virtual memory is heavily used
+ Be able to recommend adding RAM and justify why it solves the problem
""",
    mistakes=[
        "Saying ROM is 'where the operating system is stored'. The OS lives in secondary storage and is copied into RAM at boot. ROM holds only the small boot program.",
        "Describing volatile as 'temporary' without mentioning power. The examiner wants the link to power being removed.",
        "Saying virtual memory 'adds more RAM'. It does not. It uses slower secondary storage as a substitute for RAM.",
        "Claiming ROM can never be changed. It can be reflashed during a firmware update, it just is not written to during normal operation.",
        "Confusing cache with RAM. Cache is inside or beside the CPU and is much smaller and faster than RAM.",
    ],
    quiz=[
        Q("Which statement about RAM is correct?",
          ["It is volatile and holds programs and data currently in use",
           "It is non volatile and holds the boot program",
           "It is read only",
           "It is a type of secondary storage"], 0,
          "RAM is volatile main memory. It holds the operating system, the applications you have open and the data they are working with."),
        Q("Why does a computer need ROM as well as RAM?",
          ["RAM is volatile, so at switch on it is empty and cannot hold the start up instructions",
           "ROM is faster than RAM",
           "ROM has a larger capacity than RAM",
           "RAM cannot be written to"], 0,
          "At power on RAM contains nothing at all. ROM is non volatile, so the boot instructions survive being switched off and are there to run."),
        Q("What happens immediately after the boot program in ROM completes its hardware checks?",
          ["The operating system is copied from secondary storage into RAM",
           "The operating system is copied into ROM",
           "The CPU shuts down",
           "Virtual memory is disabled"], 0,
          "The bootstrap locates the operating system on secondary storage and loads it into RAM, then hands control over to it."),
        Q("Virtual memory is best described as:",
          ["An area of secondary storage used as if it were RAM when RAM is full",
           "Extra RAM chips added to the motherboard",
           "Memory built into the CPU",
           "A faster form of cache"], 0,
          "It is not real memory. It is disk space the operating system uses as an overflow when RAM runs out."),
        Q("Why does heavy use of virtual memory slow a computer down?",
          ["Secondary storage is much slower than RAM, so constant swapping wastes time",
           "The CPU clock speed is reduced",
           "The RAM is physically removed",
           "The operating system stops multitasking"], 0,
          "Every swap means writing to and reading from a device thousands of times slower than RAM. Done constantly, this is called disk thrashing."),
        Q("A user complains that their computer becomes very slow when many applications are open. What is the most effective upgrade?",
          ["Install more RAM", "Install a larger monitor",
           "Install a faster network card", "Install more ROM"], 0,
          "The slowdown is caused by running out of RAM and falling back on virtual memory. More RAM means the swapping stops."),
        Q("Which of these is non volatile?",
          ["ROM", "RAM", "Cache", "Registers"], 0,
          "ROM keeps its contents without power. RAM, cache and registers all lose theirs the instant power is removed."),
        Q("Where must a program be before the CPU can execute it?",
          ["In RAM", "On the hard disk", "In ROM", "In the swap file"], 0,
          "The CPU can only fetch from primary memory, so the program must be copied from secondary storage into RAM first."),
        Q("Which is the correct ordering from fastest to slowest?",
          ["Registers, cache, RAM, secondary storage",
           "Cache, registers, secondary storage, RAM",
           "RAM, registers, cache, secondary storage",
           "Secondary storage, RAM, cache, registers"], 0,
          "Speed decreases with distance from the CPU. Registers are inside it, then cache, then RAM, then secondary storage."),
        Q("Disk thrashing occurs when:",
          ["The system spends more time swapping data between RAM and disk than doing useful work",
           "A hard disk is physically damaged",
           "Too many files are deleted at once",
           "The CPU overheats"], 0,
          "It is the extreme case of virtual memory use: swapping happens so often that almost no real processing gets done."),
    ],
    exam=[
        EQ("State two differences between RAM and ROM.", 2, [
            MP("RAM is volatile while ROM is non volatile", ["volatile", "non volatile", "loses contents", "keeps contents", "power"]),
            MP("RAM can be read from and written to, ROM is read only in normal use", ["read only", "written to", "write", "read and write", "cannot be written"]),
        ], "RAM is volatile, meaning its contents are lost when the power is switched off, whereas ROM is non volatile and keeps its contents. RAM can also be both read from and written to during normal operation, while ROM is read only in normal use.",
           command="State"),
        EQ("Explain the purpose of ROM in a computer system.", 3, [
            MP("Holds the boot program or BIOS", ["boot", "bootstrap", "bios", "start up", "startup"]),
            MP("It is non volatile so the instructions are still present when the computer is switched on", ["non volatile", "not lost", "kept", "power off", "still there", "retains"]),
            MP("The boot program checks hardware and loads the operating system from secondary storage into RAM", ["operating system", "loads", "into ram", "secondary storage", "hardware check", "self test"]),
        ], "ROM holds the bootstrap program, sometimes called the BIOS, which is the set of instructions the computer runs the moment it is switched on. ROM is used because it is non volatile, so unlike RAM its contents survive the computer being powered down and the instructions are guaranteed to be present at start up. The boot program checks that the hardware is working, then locates the operating system in secondary storage and copies it into RAM so that the CPU can run it.",
           command="Explain"),
        EQ("Explain what virtual memory is and describe how it is used when a computer runs out of RAM.", 4, [
            MP("Virtual memory is an area of secondary storage used as if it were RAM", ["secondary storage", "hard disk", "ssd", "used as ram", "disk space", "swap file", "page file"]),
            MP("Used when RAM is full and more space is needed", ["ram is full", "runs out", "not enough ram", "insufficient"]),
            MP("Data not being used recently is moved from RAM out to the swap file", ["moved", "transferred", "swapped out", "least recently used", "not being used"]),
            MP("It is swapped back into RAM when needed again", ["swapped back", "moved back", "returned", "read back", "brought back"]),
        ], "Virtual memory is an area of secondary storage, such as a region of the hard disk or SSD known as the swap file, that the operating system uses as though it were additional RAM. It is used when RAM becomes full but another program or piece of data needs to be loaded. The operating system identifies data in RAM that has not been accessed recently and moves it out to the swap file, freeing physical RAM for the new data. If the data that was moved out is needed again later, it is swapped back into RAM, which may require moving something else out to make room.",
           command="Explain"),
        EQ("A laptop with 4 GB of RAM becomes very slow when the user has several applications open at once. Explain why this happens and recommend a solution.", 6, [
            MP("4 GB of RAM fills up when several applications are open", ["ram fills", "runs out", "full", "not enough ram", "insufficient memory"]),
            MP("The operating system starts using virtual memory on secondary storage", ["virtual memory", "swap file", "page file", "hard disk", "secondary storage"]),
            MP("Data is repeatedly swapped between RAM and secondary storage", ["swap", "swapping", "moved back and forth", "transferred", "paging"]),
            MP("Secondary storage is far slower to access than RAM", ["slower", "much slower", "slow access", "not as fast"]),
            MP("The CPU spends time waiting rather than executing instructions, which the user experiences as slowdown", ["waiting", "idle", "delay", "slow", "less work", "thrashing"]),
            MP("Recommends installing more RAM, so fewer programs need to be swapped out", ["more ram", "upgrade ram", "additional ram", "increase ram", "8 gb", "16 gb"]),
        ], "With only 4 GB of RAM, opening several applications at once quickly fills the available physical memory. Once RAM is full the operating system falls back on virtual memory, which is an area of the laptop's secondary storage used as if it were RAM. Data belonging to programs that have not been used recently is written out to the swap file, and when the user switches back to those programs that data has to be read back into RAM again, usually forcing something else out. Because secondary storage is thousands of times slower to access than RAM, each of these swaps takes a substantial amount of time, and the CPU sits waiting for data instead of executing instructions. When it happens continuously it is known as disk thrashing, and the user experiences it as severe slowdown. The most effective solution is to install more RAM, for example upgrading to 16 GB, because all the open applications can then be held in physical memory at once and swapping is largely eliminated. Replacing a mechanical hard disk with an SSD would reduce the penalty of each swap, but it treats the symptom rather than the cause.",
           command="Explain"),
        EQ("Describe the role of primary storage in a computer system.", 3, [
            MP("Primary storage is directly accessible by the CPU", ["cpu", "directly", "accessed by the processor", "direct access"]),
            MP("It holds the data and instructions currently in use", ["currently", "in use", "running", "open programs", "being used"]),
            MP("Programs are copied from secondary storage into primary storage before they can be executed", ["copied", "loaded", "transferred", "from secondary storage", "before"]),
        ], "Primary storage is the memory that the CPU is able to access directly, and it holds the data and instructions that are currently being used, including the operating system and any programs the user has open. The CPU cannot execute a program directly from secondary storage, so when a program is opened it is first copied from secondary storage into primary storage, and the CPU then fetches its instructions from there during the fetch decode execute cycle.",
           command="Describe"),
    ],
)

# ================================================== 1.2.2 Secondary storage

T_SECONDARY = Topic(
    slug="secondary-storage",
    title="Secondary Storage",
    spec="1.2.2",
    icon="i-database",
    minutes=26,
    blurb="Why every computer needs secondary storage, the three technology types, and how to choose the right device using the six characteristics examiners expect.",
    fact="Magnetic hard disks have platters spinning at 7200 revolutions per minute with a read write head hovering roughly 3 nanometres above the surface. Scaled up, that is a jumbo jet flying at full speed a few millimetres above the ground.",
    sections=[
        Section("Why secondary storage is needed", """
RAM is volatile. When the power goes, everything in it is gone. So a computer needs somewhere to keep data **permanently**, and that is **secondary storage**.

Three reasons a computer needs it:

1. **Persistence.** Files, programs and the operating system must survive being switched off.
2. **Capacity.** RAM is expensive per gigabyte. Secondary storage gives far more space for the money.
3. **Portability and backup.** Data can be moved between machines or kept as a safe copy.

!key The one line answer :: Secondary storage is non volatile, so it retains data when the computer is switched off, which primary storage cannot do.
"""),
        Section("The three types", """
### Magnetic

A **hard disk drive (HDD)** contains rigid platters coated in magnetic material, spinning at high speed. A read write head on an arm moves across the surface, magnetising tiny regions to represent 1s and 0s.

- High capacity for low cost per gigabyte
- Slower than solid state, because parts must physically move
- Contains moving parts, so it is vulnerable to being knocked or dropped
- Makes noise and generates heat
- Very long lasting if left undisturbed

Magnetic tape is also magnetic. It is extremely cheap per terabyte and still used for large scale archive backups, but access is **serial**, so reaching data at the end means winding through everything before it.

### Solid state

A **solid state drive (SSD)** stores data in flash memory using transistors that hold a charge. There are **no moving parts** at all.

- Much faster read and write speeds than magnetic
- Silent, and produces less heat
- Uses less power, which matters for battery life
- More resistant to being dropped
- More expensive per gigabyte
- Has a **finite number of write cycles**, though modern drives outlast typical use

USB flash drives and memory cards use the same flash technology.

### Optical

**CDs, DVDs and Blu-ray discs** store data as physical pits and lands burned into a reflective layer, read by a laser.

| Format | Typical capacity |
| CD | 700 MB |
| DVD | 4.7 GB single layer |
| Blu-ray | 25 GB single layer |

- Very cheap per disc and extremely portable
- Low capacity by modern standards
- Slow compared with SSD and HDD
- Easily scratched
- Read only versions cannot be altered, which is useful for distributing software

!warn Optical is not obsolete in the exam :: Even though few laptops now have a disc drive, optical storage still appears in questions about distributing software to many people cheaply, or supplying a copy that cannot be modified.
"""),
        Section("Choosing the right device", """
Six characteristics decide which device suits a situation. Learn all six, because questions often ask for three with justification.

| Characteristic | What it means | Typical winner |
| Capacity | How much data it holds | HDD, or tape for archives |
| Speed | How quickly data is read and written | SSD |
| Portability | How easily it is carried | Flash drive, optical |
| Durability | How well it survives knocks, drops and moisture | SSD, no moving parts |
| Reliability | How likely it is to fail over time | SSD for shock, HDD for long term archive |
| Cost | Price per gigabyte | HDD, or tape, cheapest per TB |

### Working through an example

*A photographer needs storage for a laptop used outdoors on location.*

- **Durability** matters most, the laptop is being carried and knocked, so an SSD with no moving parts is far less likely to be damaged.
- **Speed** matters, large image files must be written quickly.
- **Capacity** is a concern, but a 2 TB SSD is now realistic.
- **Cost** is the trade off: an SSD costs more per gigabyte than an HDD.

Conclusion: SSD, justified by durability and speed, accepting the higher cost.

!exam Always name the characteristic :: Do not write "an SSD is better because it is good". Write "an SSD is more suitable because it has no moving parts, so it is more durable when the laptop is carried between locations".
"""),
    ],
    keyterms=[
        ("Secondary storage", "Non volatile storage used to keep programs and data permanently, even when the computer is switched off."),
        ("Magnetic storage", "Storage that represents data by magnetising regions of a surface, such as a hard disk drive or tape."),
        ("Solid state storage", "Storage using flash memory with no moving parts, such as an SSD or USB flash drive."),
        ("Optical storage", "Storage read by a laser from pits and lands on a disc, such as a CD, DVD or Blu-ray."),
        ("Durability", "How well a storage device withstands physical damage such as being dropped."),
        ("Portability", "How easily a storage device can be carried and moved between computers."),
        ("Capacity", "The total amount of data a device can hold."),
        ("Write cycle", "One operation writing data to a flash memory cell. Flash memory supports a large but finite number."),
    ],
    grade="""
Nearly all the marks here are for **matching a characteristic to a scenario**. The knowledge is easy, the application is where students lose marks.

The technique is a three part sentence, repeated:

1. Name the device.
2. Name the characteristic.
3. Link it explicitly to something in the question.

"An SSD is most suitable **because it has no moving parts**, so it is **more durable** when the laptop is carried between filming locations."

Watch for the trade off. Almost every scenario has one, and stating it earns the higher mark:

+ SSD gives speed and durability but costs more per gigabyte
+ HDD gives capacity cheaply but is fragile and slower
+ Optical is cheap and portable but low capacity and easily scratched
+ Tape is cheapest per terabyte for archives but is serial access, so retrieval is slow

Also know the reason each device is fast or slow. SSD is fast because there is nothing to move. HDD is slower because the platter must rotate and the head must seek to the right track.
""",
    mistakes=[
        "Recommending a device without naming which characteristic makes it suitable.",
        "Saying an SSD 'never fails'. Flash memory has a finite number of write cycles, and any drive can fail.",
        "Calling RAM a type of secondary storage. RAM is primary storage and it is volatile.",
        "Writing 'a hard drive' when the question is about a laptop being carried around, and ignoring the durability issue.",
        "Forgetting that the operating system itself is stored in secondary storage, not in ROM.",
    ],
    quiz=[
        Q("Why does a computer need secondary storage?",
          ["It is non volatile, so data is retained when the computer is switched off",
           "It is faster than RAM",
           "The CPU reads instructions directly from it",
           "It replaces the need for ROM"], 0,
          "RAM loses everything when power is removed, so permanent storage requires a non volatile device."),
        Q("Which type of secondary storage has no moving parts?",
          ["Solid state", "Magnetic hard disk", "Optical disc", "Magnetic tape"], 0,
          "SSDs store data in flash memory using transistors. Nothing spins or moves, which is why they are fast and shock resistant."),
        Q("A charity needs to archive 200 TB of records cheaply, with retrieval expected only rarely. Which is most suitable?",
          ["Magnetic tape", "Solid state drive", "Blu-ray disc", "USB flash drive"], 0,
          "Tape has by far the lowest cost per terabyte. Its slow serial access does not matter when data is almost never retrieved."),
        Q("Which characteristic makes an SSD more suitable than an HDD for a laptop used on building sites?",
          ["Durability, because it has no moving parts to be damaged by knocks",
           "Capacity, because SSDs always hold more data",
           "Cost, because SSDs are cheaper per gigabyte",
           "Portability, because HDDs cannot be moved"], 0,
          "The key risk is physical shock. A spinning platter with a head hovering above it is vulnerable, flash memory is not."),
        Q("Approximately how much data does a single layer DVD hold?",
          ["4.7 GB", "700 MB", "25 GB", "1 TB"], 0,
          "A single layer DVD holds about 4.7 GB, roughly seven times a CD, and a single layer Blu-ray holds about 25 GB."),
        Q("How does a magnetic hard disk represent binary data?",
          ["By magnetising tiny regions of a spinning platter",
           "By burning pits into a reflective surface",
           "By trapping charge in transistors",
           "By storing it as sound waves"], 0,
          "Regions of the magnetic coating are magnetised in one direction or the other to represent 1 and 0."),
        Q("What is a disadvantage of solid state storage compared with magnetic storage?",
          ["It costs more per gigabyte", "It is much slower",
           "It uses more power", "It is noisier"], 0,
          "Flash memory is more expensive per gigabyte. On every other measure listed here the SSD wins."),
        Q("Which storage medium is most appropriate for distributing a game to shops that must not be modified by the buyer?",
          ["A read only optical disc", "A rewritable USB flash drive",
           "An external hard disk", "A cloud folder with edit access"], 0,
          "Read only optical media is cheap to produce in bulk and cannot be altered by the user, which is exactly the requirement."),
        Q("Optical storage reads data using:",
          ["A laser detecting pits and lands", "A magnetic read write head",
           "Electric charge in flash cells", "Radio waves"], 0,
          "A laser is shone at the disc surface, and pits and lands reflect the light differently, which is decoded as binary."),
        Q("Which statement about flash memory is correct?",
          ["It supports a large but finite number of write cycles",
           "It can be written to an unlimited number of times",
           "It is volatile",
           "It requires a spinning disc"], 0,
          "Each flash cell wears slightly with every write. Modern drives spread writes out, so they still last well beyond typical use."),
    ],
    exam=[
        EQ("State why a computer system requires secondary storage.", 2, [
            MP("Secondary storage is non volatile", ["non volatile", "not lost", "retained", "keeps data", "permanent"]),
            MP("So data and programs are kept when the computer is switched off, which RAM cannot do", ["switched off", "power off", "ram is volatile", "permanently", "saved"]),
        ], "Secondary storage is required because it is non volatile, which means it retains its contents when the power is removed. RAM is volatile and loses everything when the computer is switched off, so files, applications and the operating system itself must be stored in secondary storage in order to survive between sessions.",
           command="State"),
        EQ("Describe two differences between solid state and magnetic secondary storage.", 4, [
            MP("Solid state has no moving parts, magnetic uses spinning platters and a moving read write head", ["moving parts", "no moving", "spinning", "platter", "read write head"]),
            MP("Solid state is faster to read and write", ["faster", "quicker", "speed", "faster access"]),
            MP("Solid state is more durable and resistant to physical shock", ["durable", "shock", "dropped", "robust", "damage"]),
            MP("Magnetic is cheaper per gigabyte and often available in larger capacities", ["cheaper", "cost", "price per gigabyte", "larger capacity", "more storage for the money"]),
        ], "The first difference is construction. Solid state storage uses flash memory with no moving parts, whereas magnetic storage uses rigid platters that spin at high speed with a read write head that moves across the surface. This leads directly to the second difference: because nothing has to move mechanically, a solid state drive reads and writes data significantly faster and is far more resistant to damage from being knocked or dropped. In exchange, magnetic storage is considerably cheaper per gigabyte and is typically available in larger capacities for the same price.",
           command="Describe"),
        EQ("A film crew records video on location in remote areas. They need portable storage for the raw footage. Discuss which type of secondary storage they should use.", 6, [
            MP("Recommends solid state storage", ["solid state", "ssd", "flash"]),
            MP("Durability: no moving parts so it survives transport and rough handling", ["durable", "no moving parts", "shock", "dropped", "rough", "transport"]),
            MP("Speed: video files are very large so fast write speed matters", ["fast", "speed", "write quickly", "large files", "transfer"]),
            MP("Portability: physically small and light to carry", ["portable", "small", "light", "carry", "compact"]),
            MP("Power consumption is lower, useful when mains power is unavailable", ["power", "battery", "energy", "less power"]),
            MP("Acknowledges the higher cost per gigabyte as the trade off", ["expensive", "cost", "price", "more per gigabyte", "trade off"]),
        ], "The crew should use solid state storage such as portable SSDs or high capacity memory cards. The most important factor is durability: they are working in remote areas and equipment will be carried, jolted in vehicles and used in poor conditions, and because solid state storage has no moving parts it is far less likely to be damaged by physical shock than a magnetic hard disk with spinning platters and a floating read write head. Speed is the second consideration, because raw video files are extremely large and a slow write speed would either drop frames during recording or leave the crew waiting a long time to transfer footage at the end of a shoot. Solid state devices are also physically small and light, which matters when everything has to be carried, and they draw less power, which is a genuine benefit when mains electricity is not available and everything is running from batteries. The clear trade off is cost, since solid state storage is significantly more expensive per gigabyte than magnetic storage, so the crew will pay considerably more for the same capacity. Given that losing footage would mean losing an entire shoot that cannot easily be repeated, the extra cost is justified.",
           command="Discuss"),
        EQ("Explain why optical storage might still be chosen for distributing software to customers.", 3, [
            MP("Very cheap to produce in large quantities", ["cheap", "low cost", "inexpensive", "mass produce", "bulk"]),
            MP("Read only versions cannot be modified or overwritten by the customer", ["read only", "cannot be changed", "cannot be modified", "cannot be overwritten", "protected"]),
            MP("Discs are lightweight and easy to post or stock in shops", ["portable", "post", "light", "easy to transport", "shops", "shipping"]),
        ], "Optical discs remain a reasonable choice for software distribution because they are extremely cheap to manufacture in large quantities, so the cost of producing many thousands of copies is very low. Read only formats also cannot be altered or overwritten by the customer, which protects the integrity of the software and prevents accidental modification. Finally, discs are thin, light and robust enough to be posted or stocked on shop shelves easily, which makes physical distribution straightforward.",
           command="Explain"),
        EQ("A school has 500 desktop computers and needs to choose secondary storage for them. Students store documents and presentations only. Recommend a storage type and justify your recommendation.", 5, [
            MP("Recommends magnetic hard disk drives", ["hard disk", "hdd", "magnetic"]),
            MP("Cheapest cost per gigabyte, important when buying 500 units", ["cheap", "cost", "500", "budget", "price per gigabyte", "value"]),
            MP("Large capacity available for documents and presentations", ["capacity", "large", "plenty of space", "enough storage"]),
            MP("Desktop machines are not moved, so the durability weakness of magnetic storage does not matter", ["not moved", "stationary", "fixed", "desks", "durability not an issue", "do not get dropped"]),
            MP("Notes that documents are small files, so the speed advantage of SSD is not worth the extra cost here", ["small files", "speed not important", "not needed", "documents are small", "no benefit"]),
        ], "The school should choose magnetic hard disk drives. The dominant factor is cost, because buying storage for 500 machines multiplies any price difference five hundred times, and magnetic storage has by far the lowest cost per gigabyte. Hard disks also offer large capacities as standard, which comfortably exceeds what is needed for documents and presentations. The usual weakness of magnetic storage, its vulnerability to physical shock because of the spinning platters and moving head, is not relevant here because desktop computers sit permanently on desks and are not carried around. Solid state drives would boot and load faster, but student work consists of small documents and presentation files rather than large media, so the speed advantage would be barely noticeable in daily use and would not justify the substantially higher cost across the whole school.",
           command="Justify"),
    ],
)

# ============================================================= 1.2.3 Units

T_UNITS = Topic(
    slug="units-of-data",
    title="Units of Data",
    spec="1.2.3",
    icon="i-binary",
    minutes=18,
    blurb="Bits, nibbles and bytes through to petabytes, why computers use binary at all, and how to answer file size calculation questions without losing marks on the units.",
    fact="A nibble is half a byte, and yes, it is genuinely spelled that way in textbooks because it is half a byte. Computing has a long history of engineers naming things at the end of a very long day.",
    sections=[
        Section("Why binary", """
Computers use **binary**, base 2, because the components they are built from have exactly two reliable states.

A transistor is either conducting or not. A capacitor is charged or not. A region of a disk is magnetised one way or the other. Two states can be distinguished quickly and reliably even when voltages fluctuate slightly.

Ten distinguishable voltage levels for denary would be far harder to build, far more error prone, and far more expensive. So everything, numbers, text, images, sound, instructions, is stored as patterns of 1s and 0s.

!key The exam answer :: Computers use binary because their electronic components have two states, on and off, which can represent 1 and 0 reliably.
"""),
        Section("The units", """
| Unit | Symbol | Size |
| Bit | b | A single 1 or 0, the smallest unit of data |
| Nibble | | 4 bits |
| Byte | B | 8 bits |
| Kilobyte | KB | 1000 bytes |
| Megabyte | MB | 1000 kilobytes |
| Gigabyte | GB | 1000 megabytes |
| Terabyte | TB | 1000 gigabytes |
| Petabyte | PB | 1000 terabytes |

!warn 1000 or 1024 :: OCR J277 uses **1000**, not 1024. Historically 1 KB meant 2^10^ = 1024 bytes, and some software still reports sizes that way, but for this specification use powers of 1000. If a question uses 1024 it will say so.

### Converting between units

To go **up** a unit, divide by 1000. To go **down** a unit, multiply by 1000.

- 6000 bytes = 6 KB
- 3.5 MB = 3500 KB = 3,500,000 bytes
- 12,000,000,000 bytes = 12 GB

Bits to bytes: divide by 8. Bytes to bits: multiply by 8.

- 2 KB = 2000 bytes = 16,000 bits
"""),
        Section("Calculating file sizes", """
Three formulas cover almost every calculation question at GCSE.

### Text

    file size (bits) = number of characters x bits per character

A 500 character message in ASCII, which uses 7 bits per character:

    500 x 7 = 3500 bits = 437.5 bytes

### Images

    file size (bits) = colour depth x image height in pixels x image width in pixels

A 400 by 300 image with a colour depth of 8 bits:

    8 x 400 x 300 = 960,000 bits = 120,000 bytes = 120 KB

### Sound

    file size (bits) = sample rate x duration in seconds x bit depth

A 30 second clip at 44,100 Hz with a bit depth of 16:

    44100 x 30 x 16 = 21,168,000 bits = 2,646,000 bytes = 2.646 MB

!exam Marks are lost on units, not maths :: Read the question. If it asks for the answer in kilobytes and you leave it in bits, you lose the mark even though your arithmetic was perfect. Write the unit after every line of working.

### A worked full mark answer

*An image is 1000 pixels wide, 800 pixels high, with a colour depth of 24 bits. Calculate the file size in megabytes.*

    24 x 1000 x 800 = 19,200,000 bits
    19,200,000 / 8   = 2,400,000 bytes
    2,400,000 / 1000 = 2400 KB
    2400 / 1000      = 2.4 MB

Every line shows a unit. Even if the final division went wrong, the working earns method marks.
"""),
    ],
    keyterms=[
        ("Bit", "A binary digit, either 1 or 0. The smallest unit of data a computer can store."),
        ("Nibble", "Four bits, half a byte."),
        ("Byte", "Eight bits. The standard unit for measuring file sizes."),
        ("Kilobyte", "1000 bytes in the OCR specification."),
        ("Colour depth", "The number of bits used to store the colour of each pixel in an image."),
        ("Sample rate", "The number of audio samples recorded each second, measured in hertz."),
        ("Bit depth", "The number of bits used to store each individual audio sample."),
    ],
    grade="""
This topic is pure technique, and technique is the easiest place to guarantee marks.

**Always show working line by line, with units.** Examiners award method marks. A single number with no working scores nothing if it is wrong, while correct working with an arithmetic slip at the end usually still scores most of the marks.

**Convert at the end, not in the middle.** Do the multiplication in bits, then convert down step by step: bits to bytes, bytes to KB, KB to MB. Converting halfway through is where errors creep in.

**Watch the wording.** "How many bits" and "how many bytes" differ by a factor of 8. "Colour depth of 3 bits" means 2^3^ = 8 possible colours, not 3 colours.

+ Learn the three formulas by heart: text, image, sound
+ Practise converting bits to megabytes in four clean steps
+ Always finish with the unit the question asked for
""",
    mistakes=[
        "Using 1024 instead of 1000. OCR J277 uses 1000.",
        "Forgetting to divide by 8 when the answer must be in bytes rather than bits.",
        "Confusing colour depth with number of colours. A colour depth of n bits gives 2 to the power n colours.",
        "Giving an answer with no unit, or with the wrong unit.",
        "Doing all the conversions in one step in your head and getting the power of ten wrong.",
    ],
    quiz=[
        Q("How many bits are in a byte?", ["8", "4", "16", "1000"], 0,
          "Eight bits make one byte. Four bits is a nibble."),
        Q("According to the OCR specification, how many bytes are in a kilobyte?",
          ["1000", "1024", "8", "100"], 0,
          "J277 uses powers of 1000. The 1024 figure comes from the binary definition and is not used here unless a question states otherwise."),
        Q("An image is 200 by 100 pixels with a colour depth of 4 bits. What is its file size in bits?",
          ["80,000", "20,000", "800,000", "10,000"], 0,
          "4 x 200 x 100 = 80,000 bits. Multiply colour depth by width by height."),
        Q("Convert 24,000,000 bits into megabytes.",
          ["3 MB", "24 MB", "192 MB", "0.3 MB"], 0,
          "24,000,000 divided by 8 is 3,000,000 bytes, divided by 1000 is 3000 KB, divided by 1000 again is 3 MB."),
        Q("A colour depth of 8 bits allows how many different colours?",
          ["256", "8", "64", "1024"], 0,
          "Each bit doubles the possibilities, so n bits gives 2 to the power n. Two to the power 8 is 256."),
        Q("Why do computers use binary rather than denary?",
          ["Electronic components have two reliable states, on and off",
           "Binary numbers are shorter than denary numbers",
           "Denary was invented after computers",
           "Binary uses less electricity per digit"], 0,
          "Two states can be distinguished reliably even with small voltage variations, whereas ten distinct levels would be far harder to build."),
        Q("A 20 second sound clip is sampled at 8000 Hz with a bit depth of 8. What is the file size in bits?",
          ["1,280,000", "160,000", "12,800", "640,000"], 0,
          "Sample rate x duration x bit depth = 8000 x 20 x 8 = 1,280,000 bits."),
        Q("What is a nibble?", ["4 bits", "8 bits", "2 bits", "16 bits"], 0,
          "A nibble is half a byte, so four bits. One hexadecimal digit represents exactly one nibble."),
        Q("Which is the largest of these?",
          ["1 terabyte", "900 gigabytes", "5000 megabytes", "1,000,000 kilobytes"], 0,
          "1 TB is 1000 GB. The other options work out to 900 GB, 5 GB and 1 GB respectively."),
        Q("A text file contains 2000 characters stored in ASCII using 7 bits each. What is the size in bytes?",
          ["1750", "14,000", "2000", "875"], 0,
          "2000 x 7 = 14,000 bits, and 14,000 divided by 8 is 1750 bytes."),
    ],
    exam=[
        EQ("Explain why data is stored in binary in a computer system.", 2, [
            MP("Electronic components have two states, such as on and off or high and low voltage", ["two states", "on and off", "voltage", "current", "switch", "transistor"]),
            MP("These two states directly represent 1 and 0, and are reliable to distinguish", ["represent", "1 and 0", "reliable", "easily distinguished", "no confusion"]),
        ], "Data is stored in binary because the electronic components inside a computer, such as transistors, have two reliable states: they are either conducting or not conducting, which corresponds to a high or low voltage. These two states map directly onto the digits 1 and 0, and because there are only two of them they can be distinguished reliably even if the voltage varies slightly, which would not be true if ten separate levels had to be recognised for denary.",
           command="Explain"),
        EQ("An image is 800 pixels wide and 600 pixels high, with a colour depth of 16 bits. Calculate the file size of the image in megabytes. Show your working.", 4, [
            MP("Multiplies colour depth by width by height: 16 x 800 x 600", ["16 x 800", "800 x 600", "multiply", "colour depth x width x height"]),
            MP("Obtains 7,680,000 bits", ["7680000", "7,680,000", "7.68 million bits"]),
            MP("Divides by 8 to obtain 960,000 bytes", ["divide by 8", "960000", "960,000 bytes"]),
            MP("Divides by 1000 twice to obtain 0.96 MB", ["0.96", "960 kb", "divide by 1000", "0.96 mb"]),
        ], "File size in bits is colour depth multiplied by width multiplied by height, so 16 x 800 x 600 = 7,680,000 bits. Dividing by 8 converts this to 960,000 bytes. Dividing by 1000 gives 960 kilobytes, and dividing by 1000 again gives a final file size of 0.96 megabytes.",
           command="Calculate"),
        EQ("A sound file is recorded for 4 minutes at a sample rate of 44,100 Hz with a bit depth of 16 bits. Calculate the file size in megabytes, showing your working.", 4, [
            MP("Converts 4 minutes to 240 seconds", ["240", "4 x 60", "240 seconds"]),
            MP("Multiplies sample rate by duration by bit depth", ["44100 x 240", "sample rate x duration", "x 16"]),
            MP("Obtains 169,344,000 bits", ["169344000", "169,344,000"]),
            MP("Converts to approximately 21.17 MB", ["21.17", "21168000", "21,168,000 bytes", "21 mb", "21168 kb"]),
        ], "First convert the duration: 4 minutes is 4 x 60 = 240 seconds. File size in bits is sample rate x duration x bit depth, so 44,100 x 240 x 16 = 169,344,000 bits. Dividing by 8 gives 21,168,000 bytes, dividing by 1000 gives 21,168 kilobytes, and dividing by 1000 again gives a file size of approximately 21.17 megabytes.",
           command="Calculate"),
        EQ("State the number of bits in a nibble and the number of bits in a byte.", 2, [
            MP("A nibble is 4 bits", ["nibble", "4 bits", "four bits"]),
            MP("A byte is 8 bits", ["byte", "8 bits", "eight bits"]),
        ], "A nibble contains 4 bits and a byte contains 8 bits, so a nibble is exactly half a byte.",
           command="State"),
        EQ("A school stores 3000 photographs. Each photograph is 2000 by 1500 pixels with a colour depth of 24 bits. Calculate the total storage required in gigabytes.", 5, [
            MP("Calculates bits per image as 24 x 2000 x 1500", ["24 x 2000", "2000 x 1500", "colour depth x width x height"]),
            MP("Obtains 72,000,000 bits per image", ["72000000", "72,000,000", "72 million"]),
            MP("Converts to 9,000,000 bytes or 9 MB per image", ["9000000", "9,000,000", "9 mb"]),
            MP("Multiplies by 3000 photographs", ["3000", "x 3000", "multiply by the number of photos"]),
            MP("Obtains 27,000 MB which is 27 GB", ["27 gb", "27000 mb", "27,000"]),
        ], "For one photograph the file size in bits is 24 x 2000 x 1500 = 72,000,000 bits. Dividing by 8 gives 9,000,000 bytes, which is 9000 kilobytes or 9 megabytes per photograph. Multiplying by 3000 photographs gives 27,000 megabytes in total, and dividing by 1000 converts this to 27 gigabytes of storage required.",
           command="Calculate"),
    ],
)

# ================================================ 1.2.4 Numbers and binary

T_NUMBERS = Topic(
    slug="binary-and-hexadecimal",
    title="Binary, Denary and Hexadecimal",
    spec="1.2.4",
    icon="i-binary",
    minutes=35,
    blurb="Converting between all three number bases with a method that does not fail under pressure, binary addition including overflow, and binary shifts with their effect on the value.",
    fact="Hexadecimal exists purely for humans. The computer does not use it at all. The colour white as a 24 bit binary value is 111111111111111111111111, and as hex it is FFFFFF, which is why every web developer on Earth is grateful for base 16.",
    sections=[
        Section("Binary to denary", """
Each binary digit has a **place value**, doubling from right to left.

| 128 | 64 | 32 | 16 | 8 | 4 | 2 | 1 |
| 1 | 0 | 1 | 1 | 0 | 0 | 1 | 0 |

Add the place values wherever there is a 1:

    128 + 32 + 16 + 2 = 178

So `10110010` is 178 in denary.

!key Method that never fails :: Write the place value headings above the digits before you start. Every mark lost on this question type comes from doing it in your head.

### Denary to binary

Work from the **largest place value downwards**. For each, ask: does it fit?

Convert 200:

- 128 fits. Write 1. Remaining: 200 - 128 = 72
- 64 fits. Write 1. Remaining: 72 - 64 = 8
- 32 does not fit. Write 0.
- 16 does not fit. Write 0.
- 8 fits. Write 1. Remaining: 0
- 4, 2, 1 do not fit. Write 0, 0, 0.

Result: `11001000`

Always check by adding back: 128 + 64 + 8 = 200. Correct.
"""),
        Section("Hexadecimal", """
**Hexadecimal** is base 16. It uses sixteen digits: 0 to 9, then A to F.

| Denary | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 | 14 | 15 |
| Hex | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | A | B | C | D | E | F |

### Why hexadecimal is used

- **It is shorter.** One hex digit replaces four binary digits, so a value is a quarter of the length.
- **It is easier for humans to read, write and remember**, which means fewer mistakes.
- **Errors are easier to spot**, because a wrong digit stands out in a short string.
- It converts to and from binary very easily, because 16 is a power of 2.

Common uses: colour codes in HTML and CSS, MAC addresses, memory addresses, and error codes.

!warn Hex is for humans, not computers :: The computer still stores everything in binary. Hexadecimal is only a shorthand used when people need to read or write binary values. Say this and you get the mark.

### Binary to hex

Split the binary into **nibbles of four bits**, starting from the right, then convert each nibble.

`11010110`

- Split: `1101` `0110`
- `1101` = 8 + 4 + 1 = 13 = **D**
- `0110` = 4 + 2 = 6 = **6**
- Answer: **D6**

### Hex to binary

Convert each hex digit into its own four bit group.

`2F`

- `2` = `0010`
- `F` = 15 = `1111`
- Answer: `00101111`

### Hex to denary

Multiply the first digit by 16 and add the second.

`3A` = (3 x 16) + 10 = 48 + 10 = **58**

### Denary to hex

Divide by 16. The quotient is the first digit, the remainder is the second.

93 divided by 16 = 5 remainder 13, so `5D`.
"""),
        Section("Binary addition", """
There are only four rules:

    0 + 0 = 0
    0 + 1 = 1
    1 + 1 = 0 carry 1
    1 + 1 + 1 = 1 carry 1

Work from **right to left**, exactly like column addition in denary.

### Worked example

    00110101   (53)
  + 00011011   (27)
  ----------
    01010000   (80)

Check: 64 + 16 = 80. Correct.

### Overflow

An **overflow error** occurs when the result of a calculation needs more bits than are available.

    11010110   (214)
  + 01001010   (74)
  ----------
   100100000

The answer needs nine bits, but only eight are available. The leading 1 is lost, so the stored answer is wrong.

!key The definition :: Overflow occurs when the result of a calculation is too large to be represented in the number of bits available, so the carry out of the most significant bit is lost and the stored result is incorrect.

With 8 bits the largest unsigned value is 255. Any total above that overflows.
"""),
        Section("Binary shifts", """
A **logical binary shift** moves every bit left or right by a given number of places, filling the vacated positions with 0.

### Left shift multiplies

Shifting **left** by n places multiplies the value by 2^n^.

    00001101  (13)
    shift left 2
    00110100  (52)

13 x 4 = 52. Correct, because shifting left 2 multiplies by 2^2^ = 4.

### Right shift divides

Shifting **right** by n places divides the value by 2^n^.

    00110100  (52)
    shift right 2
    00001101  (13)

### Loss of data

Bits shifted off the end are **lost**, and this can cause a loss of precision.

    00001101  (13)
    shift right 2
    00000011  (3)

13 divided by 4 is 3.25, but there is no way to store the fraction, so the result is rounded down to 3. The lost bits cannot be recovered.

!exam The mark scheme wording :: When asked for the effect of a shift, say both things: the multiplication or division by a power of two, **and** what happens to bits that fall off the end.
"""),
    ],
    keyterms=[
        ("Binary", "Base 2. A number system using only the digits 0 and 1."),
        ("Denary", "Base 10. The everyday number system using digits 0 to 9. Also called decimal."),
        ("Hexadecimal", "Base 16. Uses digits 0 to 9 and letters A to F, where one hex digit represents four bits."),
        ("Most significant bit", "The leftmost bit in a binary number, with the largest place value."),
        ("Least significant bit", "The rightmost bit in a binary number, with a place value of 1."),
        ("Overflow", "An error that occurs when a result requires more bits than are available, so the answer stored is incorrect."),
        ("Logical shift", "Moving all bits left or right by a set number of places, filling the gaps with zeros."),
        ("Nibble", "A group of four bits, represented by exactly one hexadecimal digit."),
    ],
    grade="""
This is the topic where careful students collect free marks and careless ones throw them away. Almost nothing here is difficult, but everything here is easy to get slightly wrong.

**Write the place values down every single time.** 128 64 32 16 8 4 2 1. Every time, even when you are certain.

**Check by converting back.** A denary to binary conversion takes ten seconds to verify. Do it.

**For hex, always go through binary if you are unsure.** Denary to hex directly is fast when it works, but denary to binary to hex is almost impossible to get wrong.

**Learn the shift wording precisely.** "A left shift of 3 multiplies the number by 8, because 2 to the power 3 is 8. Any bits shifted beyond the most significant bit are lost."

**Overflow needs the reason, not the label.** Say the result requires more bits than are available, so the most significant bit is lost and the stored value is wrong.

+ Convert 8 bit binary to denary in under 20 seconds, reliably
+ Convert any two digit hex value to binary and denary
+ Add two 8 bit numbers and correctly identify overflow
+ State the effect of any shift, including the loss of bits
""",
    mistakes=[
        "Writing place values in the wrong direction. The 1 is on the right, the 128 is on the left.",
        "Forgetting that hexadecimal A to F represent 10 to 15, and treating A as 1.",
        "Splitting binary into nibbles from the left rather than the right when the number of bits is not a multiple of four.",
        "Saying a right shift 'divides by 2 always'. It divides by 2 to the power of the number of places shifted.",
        "Describing overflow as 'the number is too big' without explaining that the result needs more bits than are available.",
        "Losing the carry in binary addition, particularly when three 1s are added in one column.",
    ],
    quiz=[
        Q("What is the denary value of the binary number 10011010?",
          ["154", "146", "158", "150"], 0,
          "128 + 16 + 8 + 2 = 154. Write the place values above the digits and add wherever there is a 1."),
        Q("Convert the denary number 172 to 8 bit binary.",
          ["10101100", "10101010", "11001100", "10110100"], 0,
          "128 fits leaving 44, 32 fits leaving 12, 8 fits leaving 4, 4 fits leaving 0. That gives 10101100."),
        Q("What is 11101001 in hexadecimal?",
          ["E9", "9E", "D9", "EA"], 0,
          "Split into nibbles: 1110 is 14 which is E, and 1001 is 9. So the answer is E9."),
        Q("What is the denary value of hexadecimal 4C?",
          ["76", "412", "68", "196"], 0,
          "C is 12, so the calculation is (4 x 16) + 12 = 64 + 12 = 76."),
        Q("Why is hexadecimal used by programmers?",
          ["It is shorter than binary and easier for humans to read without error",
           "Computers process hexadecimal faster than binary",
           "Hexadecimal uses less storage space",
           "It is the only base that can represent colours"], 0,
          "Hex is purely a human convenience. The computer still stores binary, but one hex digit replaces four bits so values are far shorter to read and write."),
        Q("00110101 shifted left by 2 places gives which result, and what has happened to the value?",
          ["11010100, the value has been multiplied by 4",
           "00001101, the value has been divided by 4",
           "11010100, the value has been divided by 4",
           "01101010, the value has been multiplied by 2"], 0,
          "A left shift of 2 multiplies by 2 to the power 2, which is 4. Zeros fill the vacated positions on the right."),
        Q("An overflow error occurs when:",
          ["The result of a calculation requires more bits than are available",
           "A number is divided by zero",
           "Binary is converted to hexadecimal incorrectly",
           "Two negative numbers are added"], 0,
          "The carry out of the most significant bit has nowhere to go, so it is lost and the stored result is wrong."),
        Q("What is 01010110 + 00101101 in binary?",
          ["10000011", "01111011", "10000111", "01110011"], 0,
          "86 + 45 = 131, and 131 in binary is 10000011. Working column by column from the right gives the same result."),
        Q("How many bits does one hexadecimal digit represent?",
          ["4", "8", "2", "16"], 0,
          "One hex digit covers the values 0 to 15, which needs exactly four bits, so one hex digit is one nibble."),
        Q("00011000 is shifted right by 3 places. What is the result in denary and what has happened?",
          ["3, the value has been divided by 8",
           "3, the value has been multiplied by 8",
           "192, the value has been multiplied by 8",
           "6, the value has been divided by 4"], 0,
          "00011000 is 24. A right shift of 3 divides by 2 to the power 3, which is 8, so 24 becomes 3, which is 00000011."),
    ],
    exam=[
        EQ("Convert the denary number 217 into 8 bit binary. Show your working.", 2, [
            MP("Correct method shown, subtracting place values from 128 downwards", ["128", "place value", "64", "subtract", "fits"]),
            MP("Correct answer 11011001", ["11011001"]),
        ], "Working from the largest place value: 128 fits into 217 leaving 89, 64 fits into 89 leaving 25, 32 does not fit, 16 fits leaving 9, 8 fits leaving 1, 4 does not fit, 2 does not fit, and 1 fits leaving 0. This gives 11011001. Checking: 128 + 64 + 16 + 8 + 1 = 217.",
           command="Convert"),
        EQ("Explain why hexadecimal is often used by programmers instead of binary.", 3, [
            MP("Hexadecimal is much shorter, one hex digit replaces four binary digits", ["shorter", "four bits", "one digit", "fewer characters", "quarter"]),
            MP("It is easier for humans to read, write and remember, so fewer mistakes are made", ["easier", "read", "remember", "fewer mistakes", "less error", "human"]),
            MP("It converts easily to and from binary because 16 is a power of 2", ["easy to convert", "power of 2", "nibble", "straightforward", "directly"]),
        ], "Hexadecimal is used because it is far more compact than binary: each hexadecimal digit represents exactly four binary digits, so an eight bit value that takes eight characters in binary takes only two in hexadecimal. Shorter values are much easier for a person to read, write down and remember accurately, so programmers make fewer transcription errors and mistakes are easier to spot. Hexadecimal is also convenient because 16 is a power of 2, which means converting between hexadecimal and binary is a simple matter of expanding each digit into its own group of four bits, with no arithmetic required.",
           command="Explain"),
        EQ("Add the binary numbers 01101110 and 00110101. Show your working and state whether an overflow error occurs.", 4, [
            MP("Correct addition performed column by column from the right", ["carry", "right to left", "column", "working"]),
            MP("Correct answer 10100011", ["10100011"]),
            MP("States that no overflow error occurs", ["no overflow", "does not overflow", "no error", "fits"]),
            MP("Justifies this because the result fits within 8 bits", ["8 bits", "eight bits", "fits", "within", "no carry out", "less than 256"]),
        ], "Adding column by column from the right and carrying where two or three ones meet gives 10100011. Checking in denary, 01101110 is 110 and 00110101 is 53, and 110 + 53 = 163, which is 10100011 in binary. No overflow error occurs, because the result 163 is still within the range 0 to 255 that eight bits can represent, so there is no carry out of the most significant bit and no data is lost.",
           command="Add"),
        EQ("Explain what is meant by an overflow error, using an example.", 4, [
            MP("Occurs when the result of a calculation needs more bits than are available", ["more bits", "too many bits", "not enough bits", "exceeds", "too large"]),
            MP("The carry out of the most significant bit is lost", ["carry", "most significant bit", "lost", "dropped", "discarded"]),
            MP("The stored result is therefore incorrect", ["incorrect", "wrong", "inaccurate", "error", "not correct"]),
            MP("Gives a valid example with 8 bit numbers exceeding 255", ["255", "256", "example", "8 bit", "exceeds"]),
        ], "An overflow error occurs when the result of a calculation requires more bits than the system has available to store it. When this happens the carry generated out of the most significant bit has nowhere to be stored, so it is lost, and the value that ends up being stored is therefore incorrect. For example, using eight bits the largest value that can be represented is 255. Adding 11010110, which is 214, to 01001010, which is 74, produces 288, and in binary this is 100100000, a nine bit number. Since only eight bits are available, the leading 1 is discarded and the stored result becomes 00100000, which is 32 rather than 288.",
           command="Explain"),
        EQ("The binary number 00101100 is shifted left by 2 places. State the result and explain the effect this has on the value represented.", 3, [
            MP("Correct result 10110000", ["10110000"]),
            MP("The value has been multiplied by 4", ["multiplied by 4", "times 4", "x 4", "four times"]),
            MP("Because a left shift of n places multiplies by 2 to the power n", ["2 to the power", "power of two", "2^2", "doubles twice", "each shift doubles"]),
        ], "Shifting 00101100 left by two places gives 10110000, with zeros filling the two vacated positions on the right. The original value was 44 and the new value is 176, so the number has been multiplied by 4. This is because a logical left shift of n places multiplies the value by 2 to the power n, and here n is 2, so the multiplier is 4. No bits were shifted beyond the most significant bit in this case, so no data was lost.",
           command="State"),
    ],
)

# ========================================================= 1.2.4 Characters

T_CHARS = Topic(
    slug="character-encoding",
    title="Storing Characters: ASCII and Unicode",
    spec="1.2.4",
    icon="i-language",
    minutes=18,
    blurb="How text becomes binary, why ASCII was not enough, and the exact trade off between ASCII and Unicode that examiners ask about every year.",
    fact="In ASCII, the code for uppercase A is 65 and lowercase a is 97, a difference of exactly 32. That is not a coincidence: 32 is a single bit, so changing letter case is one bit flip. Early programmers designed it that way deliberately.",
    sections=[
        Section("Character sets", """
A computer cannot store the letter A. It can only store binary. So every character is given a **number**, and that number is stored in binary.

A **character set** is the agreed list of characters a computer can use, together with the binary code that represents each one.

The agreement matters enormously. If the sending computer used one mapping and the receiving computer used a different one, every message would arrive as gibberish. A shared character set is what makes text portable between machines.

!key Definition :: A character set is a defined list of characters recognised by a computer system, where each character is represented by a unique binary code.
"""),
        Section("ASCII", """
**ASCII** stands for American Standard Code for Information Interchange.

- Uses **7 bits** per character
- 2^7^ = **128 different characters**
- Covers the English alphabet in upper and lower case, digits 0 to 9, punctuation, and control characters such as carriage return
- **Extended ASCII** uses 8 bits, giving 256 characters, which adds some accented characters and symbols

### Useful ASCII values

| Character | Denary code |
| A | 65 |
| Z | 90 |
| a | 97 |
| z | 122 |
| 0 | 48 |
| 9 | 57 |
| space | 32 |

You do not have to memorise the table, but you should know two patterns:

- Characters are stored in a **logical order**, so B is one more than A. If A is 65 then F is 70.
- The **digit character '5' is not the number 5**. The character '5' has the ASCII code 53. This is why `"5" + "3"` gives `"53"` in a program while `5 + 3` gives `8`.

!warn The classic trap :: A question gives you A = 65 and asks for the code for E. Count carefully: A 65, B 66, C 67, D 68, E 69. Off by one errors here are extremely common.
"""),
        Section("Unicode", """
ASCII has 128 characters. There are thousands of writing systems in the world. Chinese alone uses tens of thousands of characters, and none of them fit.

**Unicode** was created to solve this.

- Uses **16 bits or more** per character, depending on the encoding
- Can represent **over a million characters**
- Covers every major writing system: Latin, Cyrillic, Arabic, Greek, Hebrew, Chinese, Japanese, Korean, Devanagari, and also emoji and mathematical symbols
- The first 128 Unicode codes are **identical to ASCII**, which means old ASCII text is still valid Unicode

### The trade off

| | ASCII | Unicode |
| Bits per character | 7, or 8 for extended | 16 or more |
| Number of characters | 128, or 256 extended | Over a million |
| File size | Smaller | Larger for the same text |
| Language support | English and basic symbols only | Almost every written language |

!key The exam answer for the disadvantage :: Unicode uses more bits per character than ASCII, so text files are larger and take up more storage and more bandwidth to transmit.

### Which to use

- A system handling only English text where storage is very tight, such as a small embedded device, may still use ASCII.
- Anything on the modern web uses Unicode, because websites must handle names, addresses and content in any language.
"""),
    ],
    keyterms=[
        ("Character set", "A defined list of characters recognised by a computer, each with a unique binary code."),
        ("ASCII", "American Standard Code for Information Interchange. A 7 bit character set representing 128 characters."),
        ("Extended ASCII", "An 8 bit version of ASCII representing 256 characters."),
        ("Unicode", "A character set using 16 or more bits per character, able to represent over a million characters from all major writing systems."),
        ("Character code", "The unique number assigned to a particular character within a character set."),
    ],
    grade="""
There are only two hard marks on this topic, and they are both about **why**.

**Why a character set is needed at all.** Not "so computers can store text", which is circular. The real reason: computers can only store binary, so each character must be assigned a numeric code, and the code must be agreed between systems so that text transfers correctly.

**Why Unicode costs more.** Not "Unicode is bigger". The reason: Unicode uses at least 16 bits per character compared with 7 or 8 for ASCII, so the same message takes roughly double the storage and double the transmission time.

The application marks come from choosing correctly for a scenario. A global social network needs Unicode because users write in many languages. A tiny sensor logging English status codes into 2 KB of memory may sensibly use ASCII.

+ Be able to calculate the size of a text file given the character set
+ Be able to work out any character code from a given starting value without off by one errors
+ Be able to give one advantage and one disadvantage of Unicode over ASCII
""",
    mistakes=[
        "Saying Unicode 'replaced' ASCII entirely. The first 128 Unicode codes are the same as ASCII, so ASCII text is a subset of Unicode.",
        "Miscounting character codes. If A is 65, then E is 69, not 70.",
        "Treating the character '7' as the number 7. Its ASCII code is 55.",
        "Saying ASCII has 256 characters. Standard ASCII is 7 bit and has 128. Extended ASCII is 8 bit with 256.",
        "Giving 'it supports more languages' as the only advantage, without mentioning the file size cost as the trade off.",
    ],
    quiz=[
        Q("How many bits does standard ASCII use per character?",
          ["7", "8", "16", "32"], 0,
          "Standard ASCII is 7 bit, giving 2 to the power 7 which is 128 characters. Extended ASCII adds an eighth bit for 256."),
        Q("If the ASCII code for A is 65, what is the code for G?",
          ["71", "70", "72", "66"], 0,
          "Characters run in order: A 65, B 66, C 67, D 68, E 69, F 70, G 71."),
        Q("What is the main advantage of Unicode over ASCII?",
          ["It can represent characters from almost every written language",
           "It uses fewer bits per character",
           "It is faster to process",
           "It does not need a character set"], 0,
          "Unicode was created specifically so that scripts such as Chinese, Arabic and Cyrillic could be represented, which ASCII cannot do."),
        Q("What is the main disadvantage of Unicode compared with ASCII?",
          ["It uses more bits per character, so files are larger",
           "It cannot store English text",
           "It is no longer supported by modern systems",
           "It cannot represent numbers"], 0,
          "At 16 or more bits per character rather than 7 or 8, the same text takes roughly twice the storage and bandwidth."),
        Q("A file contains 1000 characters stored using 8 bit extended ASCII. What is its size in bytes?",
          ["1000", "8000", "125", "2000"], 0,
          "8 bits is one byte per character, so 1000 characters is 1000 bytes."),
        Q("Why must computers agree on a common character set?",
          ["So that text sent between systems is interpreted the same way",
           "So that files compress more efficiently",
           "So that the CPU can run faster",
           "So that images can be stored"], 0,
          "Without a shared mapping between characters and binary codes, the receiving computer would decode the message into different characters."),
        Q("The ASCII code for lowercase a is 97. What is the code for lowercase d?",
          ["100", "99", "101", "104"], 0,
          "a is 97, b is 98, c is 99, d is 100."),
        Q("Which statement about the character '9' is correct?",
          ["It has its own character code, which is different from the number 9",
           "It is stored as the binary value 1001",
           "It cannot be stored in ASCII",
           "It has the same code as the letter I"], 0,
          "The digit character '9' has ASCII code 57. The numeric value 9 is stored differently, which is why adding two digit characters concatenates rather than sums."),
        Q("Extended ASCII can represent how many characters?",
          ["256", "128", "1024", "65,536"], 0,
          "Extended ASCII uses 8 bits, and 2 to the power 8 is 256."),
        Q("A messaging app must support users writing in Arabic, Japanese and English. Which character set should it use?",
          ["Unicode", "Standard ASCII", "Extended ASCII", "Binary coded decimal"], 0,
          "Only Unicode covers all three writing systems. ASCII in either form is limited to Latin characters and symbols."),
    ],
    exam=[
        EQ("Explain what is meant by a character set.", 2, [
            MP("A list of characters that a computer system recognises", ["list", "set of characters", "recognises", "collection"]),
            MP("Each character is represented by a unique binary code or number", ["unique", "binary", "code", "number", "value"]),
        ], "A character set is the defined list of characters that a computer system is able to recognise and use, such as letters, digits, punctuation and control characters. Each character in the set is assigned its own unique binary code, so that the computer can store and transmit text as binary values.",
           command="Explain"),
        EQ("Describe one advantage and one disadvantage of using Unicode rather than ASCII.", 4, [
            MP("Advantage: Unicode represents far more characters", ["more characters", "over a million", "65536", "larger set", "many more"]),
            MP("Advantage explained: it supports the writing systems of most world languages", ["languages", "chinese", "arabic", "worldwide", "international", "scripts", "emoji"]),
            MP("Disadvantage: Unicode uses more bits per character", ["more bits", "16 bits", "larger", "more storage per character"]),
            MP("Disadvantage explained: files are larger, using more storage and bandwidth", ["file size", "storage", "bandwidth", "slower to transmit", "takes up more space"]),
        ], "An advantage of Unicode is that it can represent over a million different characters rather than the 128 available in standard ASCII, which means it supports the writing systems of virtually every language including Chinese, Arabic and Cyrillic, as well as symbols and emoji. This makes it essential for any system used internationally. The disadvantage is that Unicode uses at least 16 bits per character compared with 7 or 8 bits in ASCII, so the same piece of text takes up roughly twice as much storage space and takes longer to transmit over a network.",
           command="Describe"),
        EQ("The ASCII code for the character 'M' is 77. State the ASCII code for the character 'Q' and explain how you worked it out.", 2, [
            MP("Correct answer 81", ["81"]),
            MP("Explains that characters are stored in sequential order, so counting forward from M gives Q", ["sequential", "order", "consecutive", "counting", "next", "one more", "n o p q"]),
        ], "The ASCII code for 'Q' is 81. Characters in ASCII are stored in sequential order, so counting forward from M at 77 gives N as 78, O as 79, P as 80 and Q as 81.",
           command="State"),
        EQ("A text file contains 4000 characters. Calculate the difference in file size, in bytes, between storing it in 8 bit extended ASCII and storing it in 16 bit Unicode.", 3, [
            MP("ASCII size calculated as 4000 bytes", ["4000 bytes", "4000 x 8", "32000 bits"]),
            MP("Unicode size calculated as 8000 bytes", ["8000 bytes", "4000 x 16", "64000 bits"]),
            MP("Difference stated as 4000 bytes", ["4000", "difference", "double", "twice"]),
        ], "In 8 bit extended ASCII each character takes one byte, so 4000 characters take 4000 bytes. In 16 bit Unicode each character takes two bytes, so the same 4000 characters take 8000 bytes. The difference in file size is therefore 8000 minus 4000, which is 4000 bytes, meaning the Unicode version is twice the size.",
           command="Calculate"),
        EQ("A company is developing a website that will be used by customers all over the world. Explain why the company should use Unicode rather than ASCII, and identify one drawback of this decision.", 4, [
            MP("Customers will write in many different languages", ["many languages", "worldwide", "international", "different countries", "global"]),
            MP("ASCII only covers English letters, digits and basic symbols", ["ascii", "english only", "128", "limited", "latin"]),
            MP("Unicode can represent the characters of virtually all writing systems", ["unicode", "all languages", "over a million", "any script", "worldwide"]),
            MP("Drawback: larger files, so more storage and bandwidth is used", ["larger", "storage", "bandwidth", "slower", "more space", "file size"]),
        ], "The company should use Unicode because its customers are spread across the world and will enter names, addresses and messages in many different writing systems. Standard ASCII can only represent 128 characters, which covers English letters, digits and basic punctuation, so any customer writing in Arabic, Chinese, Greek or Russian would find their text could not be stored or displayed correctly. Unicode can represent over a million characters and covers essentially every major script, so all customers are supported equally. The drawback is that Unicode uses at least 16 bits per character rather than 7 or 8, which roughly doubles the size of stored text and increases the bandwidth needed to send pages, adding to hosting costs and slightly slowing page loads.",
           command="Explain"),
    ],
)

# ============================================================ 1.2.4 Images

T_IMAGES = Topic(
    slug="storing-images",
    title="Storing Images",
    spec="1.2.4",
    icon="i-image",
    minutes=24,
    blurb="How a picture becomes binary, what resolution and colour depth actually control, and the file size calculation with metadata included.",
    fact="The very first digital image was made in 1957 by Russell Kirsch, who scanned a photograph of his baby son at 176 by 176 pixels. He said decades later that he regretted choosing square pixels, because he had inflicted them on the whole world.",
    sections=[
        Section("Bitmap images", """
A **bitmap** image is made of a grid of tiny squares called **pixels**, short for picture elements.

Each pixel is a single colour, and each colour is stored as a binary number. Put enough small pixels together and the eye stops seeing squares and starts seeing a photograph.

!key The definition :: A bitmap image is stored as a grid of pixels, where the colour of each pixel is represented by a binary value.

### Resolution

**Resolution** is the number of pixels in the image, usually written as width by height, for example 1920 x 1080.

Higher resolution means:

- More detail, because there are more pixels to describe the picture
- A larger file size, because there is more data to store

Below a certain resolution the individual squares become visible, which is why an image looks blocky or **pixelated** when enlarged too far.

### Colour depth

**Colour depth** is the number of **bits used to store the colour of each pixel**.

| Colour depth | Number of colours | Where you see it |
| 1 bit | 2 (black and white) | Fax, simple line art |
| 4 bit | 16 | Very old graphics |
| 8 bit | 256 | GIF images, older games |
| 24 bit | 16,777,216 | Standard photographs, called true colour |

The rule is simple: **n bits gives 2^n^ colours.**

24 bit colour uses 8 bits for red, 8 for green and 8 for blue, which is why colours are written as three values, and why hexadecimal colour codes like `#FF8800` have six digits, two per channel.

!warn Colour depth is bits, not colours :: A colour depth of 4 does not mean four colours. It means four bits, which is sixteen colours.
"""),
        Section("Metadata", """
**Metadata** is data about the data. In an image file it is the information stored alongside the pixels that tells software how to interpret and display them.

Typical image metadata includes:

- Width and height in pixels
- Colour depth
- File format
- Date and time created
- Camera make, model and settings
- Sometimes GPS location

### Why metadata is essential

Without the width, the computer would have a long list of colour values and no idea how to arrange them. Is it 200 pixels wide by 300 tall, or 300 by 200? The picture would be scrambled.

!exam The mark scheme point :: Metadata is needed so the image can be displayed correctly, because the software needs the dimensions and colour depth in order to reconstruct the grid of pixels from the stored data.

Metadata also increases the file size slightly, and this appears in calculation questions.
"""),
        Section("Calculating image file size", """
    file size (bits) = colour depth x image width x image height

Add metadata afterwards if the question gives you a value for it.

### Worked example

*An image is 500 pixels wide and 400 pixels high with a colour depth of 8 bits. The metadata is 1 KB. Calculate the total file size in kilobytes.*

    Pixel data: 8 x 500 x 400 = 1,600,000 bits
    1,600,000 / 8    = 200,000 bytes
    200,000 / 1000   = 200 KB
    Plus metadata    = 200 + 1 = 201 KB

### Effect of changing settings

| Change | Effect on quality | Effect on file size |
| Double the resolution | More detail | Roughly four times larger, since both width and height double |
| Halve the colour depth | Fewer available colours, possible banding | Half the size |
| Increase colour depth from 8 to 24 | Far more colours, smoother gradients | Three times larger |

!warn Doubling resolution quadruples the file :: If both width and height double, the number of pixels goes up by a factor of four, not two. This catches students out constantly.
"""),
    ],
    keyterms=[
        ("Pixel", "Picture element. The smallest single point in a bitmap image, holding one colour value."),
        ("Bitmap", "An image stored as a grid of pixels, each with a binary colour value."),
        ("Resolution", "The number of pixels in an image, usually given as width by height."),
        ("Colour depth", "The number of bits used to store the colour of each pixel."),
        ("Metadata", "Data stored with a file describing it, such as dimensions, colour depth and date created."),
        ("Pixelated", "The blocky appearance produced when an image with too few pixels is displayed at a large size."),
    ],
    grade="""
The knowledge here is straightforward. The marks come from **explaining consequences precisely**.

**Do not say 'better quality'.** Say what improves and why. Higher resolution means more pixels are used to represent the same area, so finer detail is captured and the image looks sharper when enlarged.

**Always mention the cost.** Every quality increase costs file size. Every file size reduction costs quality. Examiners are looking for you to state both sides.

**Get the arithmetic relationship right.** Doubling colour depth doubles file size. Doubling *both* dimensions quadruples it. Students routinely lose a mark by saying doubling resolution doubles the file.

**Metadata is worth a mark on its own.** Learn one clear reason it is necessary: without dimensions the software cannot rebuild the grid of pixels.

+ Calculate an image file size including metadata, in the unit requested
+ Explain the effect on quality and size of changing resolution or colour depth
+ Give three examples of image metadata and say why one of them is essential
""",
    mistakes=[
        "Saying colour depth is the number of colours. It is the number of bits, and n bits gives 2 to the power n colours.",
        "Forgetting to add metadata when the question supplies it.",
        "Saying doubling the resolution doubles the file size, when both dimensions doubling means four times as many pixels.",
        "Describing resolution as 'how good the image looks'. Resolution is a count of pixels.",
        "Leaving the final answer in bits when the question asked for kilobytes.",
    ],
    quiz=[
        Q("What is a pixel?",
          ["The smallest single point of colour in a bitmap image",
           "A unit of file size", "A type of image file format", "A measure of colour depth"], 0,
          "Pixel is short for picture element. Each one holds a single colour value stored in binary."),
        Q("An image has a colour depth of 5 bits. How many different colours can it use?",
          ["32", "5", "25", "10"], 0,
          "2 to the power 5 is 32. Each additional bit doubles the number of available colours."),
        Q("An image is 300 by 200 pixels with a colour depth of 24 bits. What is the pixel data size in bits?",
          ["1,440,000", "60,000", "144,000", "14,400,000"], 0,
          "24 x 300 x 200 = 1,440,000 bits, which is 180,000 bytes or 180 KB."),
        Q("What is metadata in an image file?",
          ["Data describing the image, such as its dimensions and colour depth",
           "The colour value of each pixel",
           "The compression algorithm used",
           "A thumbnail preview"], 0,
          "Metadata is data about the file. Without the dimensions, software could not arrange the pixel values into the correct grid."),
        Q("If both the width and the height of an image are doubled, the file size becomes approximately:",
          ["Four times larger", "Twice as large", "The same", "Eight times larger"], 0,
          "Doubling both dimensions gives 2 x 2 = 4 times as many pixels, so roughly four times the data."),
        Q("Why does an image look pixelated when enlarged too much?",
          ["The individual pixels become large enough to see as squares",
           "The colour depth is automatically reduced",
           "Metadata is lost during resizing",
           "The compression algorithm fails"], 0,
          "There is no extra detail to reveal, so the existing pixels simply get bigger until the grid itself becomes visible."),
        Q("How many bits per pixel does true colour use?",
          ["24", "8", "16", "32"], 0,
          "True colour is 24 bit, using 8 bits each for red, green and blue, giving over 16 million colours."),
        Q("An image file is 400 KB. If the colour depth is halved and nothing else changes, what is the new approximate size?",
          ["200 KB", "800 KB", "400 KB", "100 KB"], 0,
          "File size is directly proportional to colour depth, so halving the bits per pixel halves the pixel data."),
        Q("Which is the best reason for metadata being stored with an image?",
          ["The software needs the width, height and colour depth to reconstruct the image correctly",
           "It makes the image file smaller",
           "It improves the resolution",
           "It converts the image to vector format"], 0,
          "The pixel values alone are just a long list. The dimensions tell the software how to lay them out."),
        Q("A photographer increases the resolution of a photo from 1000 x 800 to 2000 x 1600 at the same colour depth. What happens?",
          ["More detail is captured and the file becomes about four times larger",
           "More detail is captured and the file stays the same size",
           "Detail is unchanged but the file is four times larger",
           "The file becomes four times smaller"], 0,
          "Both dimensions have doubled, so there are four times as many pixels holding four times as much detail and data."),
    ],
    exam=[
        EQ("Explain how a bitmap image is represented in binary.", 3, [
            MP("The image is made up of a grid of pixels", ["grid", "pixels", "picture elements", "squares"]),
            MP("Each pixel is assigned a colour, stored as a binary value", ["binary", "colour value", "each pixel", "binary number"]),
            MP("The number of bits used for each pixel is the colour depth, and n bits gives 2 to the power n colours", ["colour depth", "bits per pixel", "2 to the power", "number of colours"]),
        ], "A bitmap image is made up of a grid of very small squares called pixels. Each pixel holds a single colour, and that colour is stored as a binary number. The number of bits used to store each pixel's colour is called the colour depth, and a colour depth of n bits allows 2 to the power n different colours, so 8 bits gives 256 colours and 24 bits gives over 16 million.",
           command="Explain"),
        EQ("An image is 640 pixels wide and 480 pixels high with a colour depth of 8 bits. The metadata is 2 KB. Calculate the total file size in kilobytes.", 4, [
            MP("Multiplies 8 x 640 x 480", ["8 x 640", "640 x 480", "colour depth x width x height"]),
            MP("Obtains 2,457,600 bits", ["2457600", "2,457,600"]),
            MP("Converts to 307,200 bytes which is 307.2 KB", ["307200", "307.2", "divide by 8"]),
            MP("Adds metadata to give 309.2 KB", ["309.2", "add 2", "plus metadata"]),
        ], "The pixel data is colour depth multiplied by width multiplied by height, which is 8 x 640 x 480 = 2,457,600 bits. Dividing by 8 gives 307,200 bytes, and dividing by 1000 gives 307.2 kilobytes. Adding the 2 KB of metadata gives a total file size of 309.2 kilobytes.",
           command="Calculate"),
        EQ("Explain what is meant by metadata and give two examples of metadata stored in an image file.", 3, [
            MP("Metadata is data about the file, stored alongside the image data", ["data about", "describes", "information about the file", "alongside"]),
            MP("First valid example such as width, height, resolution or colour depth", ["width", "height", "resolution", "colour depth", "dimensions"]),
            MP("Second valid example such as date created, file format, camera model or GPS location", ["date", "format", "camera", "gps", "location", "time", "author"]),
        ], "Metadata is data about the data, meaning information stored alongside the actual image content that describes the file and tells software how to interpret it. Two examples of image metadata are the width and height of the image in pixels, which the software needs in order to arrange the stored pixel values into the correct grid, and the date and time the photograph was taken, which is recorded automatically by most cameras.",
           command="Explain"),
        EQ("Describe the effect of increasing the colour depth of an image from 8 bits to 24 bits.", 4, [
            MP("The number of available colours rises from 256 to over 16 million", ["256", "16 million", "16777216", "more colours", "2 to the power 24"]),
            MP("Image quality improves with smoother colour gradients and more realistic images", ["quality", "smoother", "gradients", "realistic", "detail", "accurate colours", "banding"]),
            MP("The file size triples because three times as many bits are used per pixel", ["three times", "triples", "3x", "larger", "x3"]),
            MP("This requires more storage space and more bandwidth to transmit", ["storage", "bandwidth", "slower to transmit", "more space", "longer to download"]),
        ], "Increasing colour depth from 8 bits to 24 bits raises the number of colours available for each pixel from 256 to over 16 million. This significantly improves quality, because gradual changes in colour such as a sky or a skin tone can be reproduced smoothly instead of showing visible banding where the limited palette has to jump between shades. The cost is file size: three times as many bits are now stored for every pixel, so the image file becomes three times larger. That means it takes up three times the storage space and takes about three times as long to transmit over a network.",
           command="Describe"),
        EQ("A website designer needs to reduce the file size of a large photograph before uploading it. Describe two changes that could be made and explain the effect of each on the image.", 4, [
            MP("Reduce the resolution by decreasing the number of pixels", ["resolution", "fewer pixels", "smaller dimensions", "reduce size", "scale down"]),
            MP("Effect: less detail and the image may look pixelated if enlarged", ["less detail", "pixelated", "blocky", "loss of detail", "sharpness"]),
            MP("Reduce the colour depth so fewer bits are used per pixel", ["colour depth", "fewer bits", "fewer colours", "reduce colours"]),
            MP("Effect: fewer colours available which may cause visible banding in gradients", ["fewer colours", "banding", "less realistic", "quality", "posterised"]),
        ], "The first change is to reduce the resolution, lowering the number of pixels in the width and the height. Because file size is directly proportional to the number of pixels, halving both dimensions cuts the file to roughly a quarter of its original size, but less detail is captured so the photograph will look softer and will appear pixelated if a viewer enlarges it. The second change is to reduce the colour depth, for example from 24 bits to 8 bits per pixel, which cuts the pixel data to a third of its size. The drawback is that only 256 colours are then available, so smooth gradients such as a sky may show visible banding where the image has to jump between the nearest available shades.",
           command="Describe"),
    ],
)

# ============================================================= 1.2.4 Sound

T_SOUND = Topic(
    slug="storing-sound",
    title="Storing Sound",
    spec="1.2.4",
    icon="i-sound",
    minutes=22,
    blurb="How a continuous analogue wave becomes a list of binary numbers, what sample rate and bit depth each control, and the sound file size calculation.",
    fact="CD audio uses 44,100 samples per second. That specific number exists because early digital recorders stored audio on video tape, and 44,100 fit neatly into the line and frame structure of both PAL and NTSC television.",
    sections=[
        Section("Analogue to digital", """
Sound in the real world is an **analogue** wave: a continuously varying change in air pressure. It has infinitely many values at infinitely many moments.

A computer cannot store infinity. So sound must be **sampled**.

### Sampling

**Sampling** means measuring the amplitude of the sound wave at regular intervals and recording each measurement as a binary number.

1. A microphone converts the sound wave into a varying electrical signal.
2. An analogue to digital converter measures the amplitude of that signal at fixed intervals.
3. Each measurement is rounded to the nearest available level and stored in binary.

The result is a long list of numbers that approximates the original wave.

!key Definition :: Sampling is the process of measuring the amplitude of an analogue sound wave at regular intervals and storing each measurement as a binary value.

!warn Digital sound is always an approximation :: Because samples are taken at intervals and rounded to fixed levels, the stored version can never be a perfect copy. It can only be a closer or a rougher approximation.
"""),
        Section("Sample rate and bit depth", """
### Sample rate

**Sample rate** is the number of samples taken per second, measured in **hertz**.

- CD quality is 44,100 Hz, so 44,100 measurements every second
- Telephone quality is about 8000 Hz

A higher sample rate means:

- The samples are closer together, so the digital version follows the shape of the original wave more closely
- Higher frequencies can be captured accurately
- The file is larger

### Bit depth

**Bit depth** is the number of bits used to store **each individual sample**.

- 8 bit depth gives 2^8^ = 256 possible amplitude levels
- 16 bit depth gives 2^16^ = 65,536 levels

A higher bit depth means:

- Each measurement can be recorded more precisely, because there are more levels to round to
- Quieter details survive rather than being rounded away
- The file is larger

!exam Do not mix them up :: Sample rate is about **how often** you measure, along the time axis. Bit depth is about **how precisely** you record each measurement, along the amplitude axis. Questions frequently test whether you know which is which.

| | Sample rate | Bit depth |
| Measures | How many samples per second | How many bits per sample |
| Axis | Time | Amplitude |
| Unit | Hertz | Bits |
| Increasing it | Captures the wave shape more accurately over time | Records each amplitude more precisely |
"""),
        Section("Calculating sound file size", """
    file size (bits) = sample rate x duration in seconds x bit depth

If the recording is in stereo, multiply by 2, because there are two channels.

### Worked example

*A 3 minute song is recorded at 44,100 Hz with a bit depth of 16, in mono. Calculate the file size in megabytes.*

    Duration: 3 x 60 = 180 seconds
    44,100 x 180 x 16 = 127,008,000 bits
    127,008,000 / 8   = 15,876,000 bytes
    / 1000            = 15,876 KB
    / 1000            = 15.876 MB

In stereo that would be 31.752 MB.

### The quality against size trade off

| Setting | Quality effect | Size effect |
| Double the sample rate | Better representation of the wave, higher frequencies captured | Doubles the file |
| Double the bit depth | More precise amplitudes, wider dynamic range | Doubles the file |
| Halve the sample rate | Wave shape reproduced more roughly, sounds duller | Halves the file |

!key The answer examiners want :: Increasing the sample rate or the bit depth improves the accuracy with which the original analogue wave is reproduced, and therefore the sound quality, but it increases the file size proportionally.
"""),
    ],
    keyterms=[
        ("Analogue", "A continuously varying signal, such as a real sound wave, with infinitely many possible values."),
        ("Sampling", "Measuring the amplitude of an analogue signal at regular intervals and storing each value in binary."),
        ("Sample rate", "The number of samples taken per second, measured in hertz."),
        ("Bit depth", "The number of bits used to store each individual sample."),
        ("Amplitude", "The height of the sound wave at a given moment, which corresponds to loudness."),
        ("Analogue to digital converter", "The hardware that measures an analogue signal and outputs binary sample values."),
    ],
    grade="""
The single biggest discriminator on this topic is whether you can explain **why** a higher sample rate improves quality, rather than just asserting that it does.

**Weak**: "A higher sample rate means better quality."

**Strong**: "A higher sample rate means samples are taken closer together in time, so the sequence of stored values follows the shape of the original analogue wave more closely and less detail is lost between samples, which produces a more accurate reproduction."

Do the same for bit depth: more bits means more possible amplitude levels, so each sample is rounded by a smaller amount, which means quieter detail is preserved.

**Always state the file size consequence.** Every quality improvement on this topic costs storage in direct proportion.

+ Explain sampling as a three step process from microphone to binary
+ Distinguish sample rate and bit depth in one sentence each
+ Calculate a sound file size in the unit asked for, including stereo
+ Give a reasoned recommendation for a scenario, such as a podcast versus a music studio
""",
    mistakes=[
        "Swapping sample rate and bit depth. Rate is per second, depth is per sample.",
        "Forgetting to convert minutes into seconds before calculating.",
        "Forgetting to double the file size for stereo when the question says stereo.",
        "Saying digital sound is 'exactly the same' as the original. It is always an approximation.",
        "Saying a higher sample rate 'makes the sound louder'. It affects accuracy, not volume.",
    ],
    quiz=[
        Q("What does sample rate measure?",
          ["The number of samples taken per second",
           "The number of bits used per sample",
           "The loudness of the recording",
           "The length of the recording"], 0,
          "Sample rate is a frequency, measured in hertz. Bit depth is the number of bits per sample."),
        Q("A sound is recorded with a bit depth of 8. How many different amplitude levels can be stored?",
          ["256", "8", "64", "1024"], 0,
          "2 to the power 8 is 256. Each extra bit doubles the number of levels available."),
        Q("Why can a digital recording never be a perfect copy of the original sound?",
          ["Samples are taken at intervals and rounded to fixed levels, so some detail is lost",
           "Microphones always add noise",
           "Binary cannot store decimal numbers",
           "Speakers reduce the quality on playback"], 0,
          "Between two samples the wave is not recorded at all, and each sample is rounded to the nearest available level."),
        Q("A 10 second clip is sampled at 16,000 Hz with a bit depth of 8, in mono. What is the file size in bits?",
          ["1,280,000", "160,000", "128,000", "12,800,000"], 0,
          "16,000 x 10 x 8 = 1,280,000 bits, which is 160,000 bytes or 160 KB."),
        Q("What is the effect of doubling the sample rate while keeping everything else the same?",
          ["The wave is reproduced more accurately and the file size doubles",
           "The sound becomes twice as loud and the file size stays the same",
           "The file size halves and quality improves",
           "Nothing changes audibly"], 0,
          "Twice as many measurements per second gives a closer approximation of the wave, and twice as much data to store."),
        Q("Bit depth affects:",
          ["How precisely the amplitude of each sample is recorded",
           "How many samples are taken each second",
           "The length of the recording",
           "Whether the recording is mono or stereo"], 0,
          "More bits means more possible levels, so each measurement is rounded by a smaller amount."),
        Q("A recording in stereo compared with the same recording in mono will be:",
          ["Twice the file size, because two channels are stored",
           "The same file size", "Half the file size", "Four times the file size"], 0,
          "Stereo stores separate data for the left and right channels, so the total is doubled."),
        Q("Which device converts the analogue signal from a microphone into binary samples?",
          ["An analogue to digital converter", "A digital to analogue converter",
           "The graphics processor", "The sound speaker"], 0,
          "The ADC measures the incoming electrical signal at regular intervals and outputs binary values."),
        Q("A 2 minute recording at 44,100 Hz with 16 bit depth in mono is approximately:",
          ["10.6 MB", "1.4 MB", "84.7 MB", "5.3 MB"], 0,
          "120 seconds x 44,100 x 16 = 84,672,000 bits, which is 10,584,000 bytes, about 10.6 MB."),
        Q("Which change would reduce a sound file's size while having the smallest impact on speech clarity?",
          ["Reducing the sample rate, since speech occupies a limited frequency range",
           "Removing the metadata",
           "Converting to stereo",
           "Increasing the bit depth"], 0,
          "Speech sits in a fairly narrow frequency band, which is why telephone systems have used low sample rates for decades and remain intelligible."),
    ],
    exam=[
        EQ("Explain what is meant by sampling when recording sound digitally.", 3, [
            MP("The amplitude of the analogue sound wave is measured", ["amplitude", "height", "measure", "measured", "level"]),
            MP("Measurements are taken at regular intervals", ["regular intervals", "fixed intervals", "at intervals", "periodically", "each time"]),
            MP("Each measurement is stored as a binary value", ["binary", "stored as a number", "digital value", "converted"]),
        ], "Sampling is the process by which a continuously varying analogue sound wave is converted into digital data. The amplitude of the wave is measured at regular fixed intervals, and each of those measurements is rounded to the nearest available level and stored as a binary number. The complete recording is therefore a long sequence of binary values that approximates the shape of the original wave.",
           command="Explain"),
        EQ("Explain the difference between sample rate and bit depth.", 4, [
            MP("Sample rate is the number of samples taken per second", ["per second", "samples per second", "how often", "frequency", "hertz"]),
            MP("Bit depth is the number of bits used to store each sample", ["bits per sample", "each sample", "number of bits", "size of each"]),
            MP("Higher sample rate captures the shape of the wave over time more accurately", ["shape", "over time", "closer together", "more accurate", "follows the wave"]),
            MP("Higher bit depth records each amplitude more precisely because there are more levels", ["more levels", "precisely", "amplitude", "rounded less", "accuracy of each"]),
        ], "Sample rate is the number of samples taken every second, measured in hertz, so it describes how often the sound wave is measured along the time axis. Bit depth is the number of bits used to store each individual sample, so it describes how precisely each measurement is recorded along the amplitude axis. Increasing the sample rate means the measurements are closer together in time, so the stored data follows the shape of the original wave more closely and less detail is lost between samples. Increasing the bit depth means there are more possible amplitude levels available, so each measurement is rounded by a smaller amount and quieter detail is preserved.",
           command="Explain"),
        EQ("A 90 second sound clip is recorded in mono at a sample rate of 22,050 Hz with a bit depth of 16. Calculate the file size in megabytes.", 4, [
            MP("Multiplies sample rate by duration by bit depth", ["22050 x 90", "x 16", "sample rate x duration"]),
            MP("Obtains 31,752,000 bits", ["31752000", "31,752,000"]),
            MP("Divides by 8 to obtain 3,969,000 bytes", ["3969000", "3,969,000", "divide by 8"]),
            MP("States approximately 3.97 MB", ["3.97", "3.969", "3969 kb", "4 mb"]),
        ], "File size in bits is sample rate multiplied by duration multiplied by bit depth, which is 22,050 x 90 x 16 = 31,752,000 bits. Dividing by 8 gives 3,969,000 bytes, dividing by 1000 gives 3969 kilobytes, and dividing by 1000 again gives approximately 3.97 megabytes.",
           command="Calculate"),
        EQ("A student is recording a spoken podcast that will be downloaded by listeners on mobile data. Recommend suitable settings for sample rate and bit depth, and justify your recommendation.", 6, [
            MP("Recommends a relatively low sample rate such as 22,050 Hz or lower", ["22050", "22.05", "low sample rate", "8000", "16000", "lower rate"]),
            MP("Speech occupies a narrower frequency range than music so a high rate is unnecessary", ["speech", "voice", "narrow", "frequency range", "not music", "limited range"]),
            MP("Recommends a bit depth of 16, or justifies 8, for adequate clarity", ["16 bit", "bit depth of 16", "8 bit"]),
            MP("Explains that this keeps the file size small for downloading over mobile data", ["file size", "smaller", "download", "mobile data", "bandwidth", "quicker"]),
            MP("Recommends mono rather than stereo, halving the size", ["mono", "one channel", "not stereo", "halves"]),
            MP("Acknowledges the trade off that quality is reduced compared with music standard settings", ["trade off", "quality", "not as good", "lower quality", "compromise", "acceptable"]),
        ], "A sample rate of around 22,050 Hz with a bit depth of 16, recorded in mono, would be a sensible choice. Speech occupies a much narrower frequency range than music, so the very high frequencies that a 44,100 Hz rate is designed to capture are simply not present in a spoken voice, and halving the sample rate therefore halves the file size with almost no audible loss of clarity. A bit depth of 16 keeps the dynamic range wide enough that quiet speech does not become distorted, and dropping to 8 bits would introduce noticeable background hiss on quiet passages. Recording in mono rather than stereo halves the size again, and since a single speaker has no meaningful stereo image there is nothing lost. Together these settings might produce a file around a quarter the size of a CD quality stereo recording, which matters a great deal to listeners downloading episodes over mobile data where both speed and data allowances are limited. The trade off is that the recording would not be suitable if music were included, and a studio producing music would need the full 44,100 Hz stereo settings.",
           command="Justify"),
        EQ("Describe the effect on both quality and file size of halving the sample rate of a recording.", 3, [
            MP("Fewer samples are taken each second", ["fewer samples", "half as many", "less often", "fewer measurements"]),
            MP("The reproduction of the original wave is less accurate, so quality falls", ["less accurate", "quality", "worse", "detail lost", "rougher", "duller"]),
            MP("The file size is halved", ["halved", "half", "50 per cent", "smaller by half"]),
        ], "Halving the sample rate means only half as many measurements of the sound wave are taken each second. Because the samples are further apart in time, more of the detail between them is lost and the stored data follows the shape of the original wave less closely, so the playback quality is noticeably lower and the recording tends to sound duller. Since file size is directly proportional to sample rate, the file will be half its original size, which is the benefit being traded for that loss of quality.",
           command="Describe"),
    ],
)

# ======================================================== 1.2.5 Compression

T_COMPRESS = Topic(
    slug="compression",
    title="Compression",
    spec="1.2.5",
    icon="i-compress",
    minutes=20,
    blurb="Why files are compressed at all, exactly how lossy and lossless differ, and how to choose correctly between them in any scenario the exam gives you.",
    fact="Lossless compression works by finding repetition. This is why a text file can shrink to a fifth of its size while a file of truly random numbers barely shrinks at all: there is no pattern to exploit.",
    sections=[
        Section("Why compress", """
**Compression** means reducing the size of a file.

Three reasons it matters:

1. **Less storage space** is used, so more files fit on a device.
2. **Faster transmission** over a network, because there is less data to send.
3. **Less bandwidth** is consumed, which reduces cost and eases congestion.

Streaming video, sending email attachments, loading web pages and backing up a phone all depend on compression working well.

!key The exam sentence :: Compressed files take up less storage space and can be transmitted more quickly, because there is less data to send.
"""),
        Section("Lossy compression", """
**Lossy** compression permanently removes some of the data from the file.

The data chosen for removal is data the human eye or ear is least likely to notice:

- In audio, frequencies too high or too quiet for most people to hear
- In images, subtle colour differences the eye cannot easily distinguish

### Characteristics

- **Much greater size reduction**, often to a small fraction of the original
- Some **quality is lost**, and it is lost permanently
- The original file **cannot be recovered**
- Repeatedly saving in a lossy format degrades the file further each time

### Where it is used

- MP3 and AAC audio
- JPEG images
- MP4 video and most streaming

!warn Lossy is irreversible :: Once compressed, the removed data is gone. Saving a JPEG back as a PNG does not restore anything, it just stops further loss. This point is worth a mark.
"""),
        Section("Lossless compression", """
**Lossless** compression reduces file size **without removing any data**. It works by recording the data more efficiently, usually by identifying and encoding repetition.

### A simple illustration

Instead of storing:

    AAAAAAAABBBBCCCCCCCC

it stores:

    8A 4B 8C

Every character can be reconstructed exactly. Nothing has been thrown away, the information has simply been described more compactly.

### Characteristics

- The original file is **restored perfectly** when decompressed
- **Less size reduction** than lossy
- No loss of quality at all

### Where it is used

- ZIP archives
- PNG and GIF images
- FLAC audio
- Any file where every byte matters: program files, spreadsheets, documents, databases

!key Why a program must use lossless :: If lossy compression removed part of a program file, the instructions would be corrupted and the program would fail to run. Text documents are the same, a missing word changes the meaning.
"""),
        Section("Choosing between them", """
| | Lossy | Lossless |
| Data removed | Yes, permanently | No |
| Original recoverable | No | Yes |
| Size reduction | Large | Smaller |
| Quality | Reduced | Unchanged |
| Typical uses | MP3, JPEG, streaming video | ZIP, PNG, FLAC, program files |

### Choosing correctly

Ask one question: **would losing some data matter?**

- Streaming a film to a phone: no, the viewer will not notice, and small files matter enormously. Use **lossy**.
- Archiving a legal document: yes, absolutely. Use **lossless**.
- A photographer's master copies: yes, they need to edit them later without accumulated degradation. Use **lossless**.
- A photograph on a web page: no, small size and fast loading matter more. Use **lossy**.

!exam How to phrase the justification :: Name the type, then say what would happen if you chose the other one. "Lossless must be used because compressing a spreadsheet with lossy compression would permanently remove values, corrupting the data."
"""),
    ],
    keyterms=[
        ("Compression", "Reducing the size of a file so it uses less storage and transmits more quickly."),
        ("Lossy compression", "Compression that permanently removes some data, giving a large size reduction but reduced quality."),
        ("Lossless compression", "Compression that reduces size without losing any data, so the original file can be perfectly restored."),
        ("Bandwidth", "The amount of data that can be transmitted over a network connection in a given time."),
        ("Decompression", "Restoring a compressed file so it can be used."),
    ],
    grade="""
This topic is generous with marks provided you write with precision.

**Say permanently.** Lossy compression does not just reduce quality, it removes data permanently and the original cannot be recovered. That word is often the difference between one mark and two.

**Explain the mechanism of lossless.** Do not just say "no data is lost". Say that repeated patterns are identified and stored more efficiently, for example by recording a value once with a count, so the original can be reconstructed exactly.

**Justify with consequences.** The strongest scenario answers say what would go wrong with the wrong choice, not just what is good about the right one.

**Know that lossy is not always worse.** For a video streaming service, lossy is not a compromise, it is the only workable option. Answers that treat lossy as simply inferior miss the point.

+ Define both types in one sentence each, including the word permanently
+ Explain the mechanism of lossless with a short example
+ Recommend a type for any scenario and justify by naming what would go wrong otherwise
+ Give two correct real file formats for each type
""",
    mistakes=[
        "Saying lossy compression 'compresses more of the file'. It removes data, which is why it achieves greater reduction.",
        "Claiming a lossy file can be restored to its original quality later. It cannot.",
        "Saying lossless compression 'does not reduce the file size much so it is not useful'. It is essential wherever accuracy matters.",
        "Giving JPEG as an example of lossless. JPEG is lossy. PNG and GIF are lossless.",
        "Recommending lossy for a text document or a program file, which would corrupt it.",
    ],
    quiz=[
        Q("What is the main purpose of compression?",
          ["To reduce file size so less storage is used and transmission is faster",
           "To improve the quality of a file",
           "To protect a file with a password",
           "To convert a file into binary"], 0,
          "Compression is about size. Smaller files take less space and travel across a network faster."),
        Q("Which statement about lossy compression is correct?",
          ["Some data is permanently removed and cannot be recovered",
           "All data is retained and the original can be restored",
           "It only works on text files",
           "It increases the file size"], 0,
          "Lossy compression discards data the human eye or ear is unlikely to notice, and that data is gone for good."),
        Q("Which of these uses lossless compression?",
          ["A ZIP archive", "An MP3 file", "A JPEG image", "A streamed video"], 0,
          "ZIP must restore files exactly, so it is lossless. MP3, JPEG and streaming video all use lossy compression."),
        Q("Why must a program file be compressed using a lossless method?",
          ["Removing any data would corrupt the instructions and the program would not run",
           "Program files are too small for lossy compression",
           "Lossy compression only works on images",
           "Lossless compression is always faster"], 0,
          "Every byte of a program is a meaningful instruction. Discarding some would break it."),
        Q("How does lossless compression reduce file size?",
          ["By recording repeated data more efficiently so it can be perfectly reconstructed",
           "By deleting the least important pixels",
           "By reducing the sample rate",
           "By converting the file to a lower resolution"], 0,
          "It finds patterns and repetition and encodes them compactly, for example storing a value once with a count of how many times it repeats."),
        Q("A user saves a photograph as a JPEG, opens it, and saves it as a JPEG again several times. What happens?",
          ["Quality degrades further with each save",
           "The image is restored to its original quality",
           "The file size grows each time",
           "Nothing changes after the first save"], 0,
          "Each lossy save discards more data, and because the loss is permanent it accumulates."),
        Q("Which is the strongest reason a music streaming service uses lossy compression?",
          ["Much smaller files mean faster streaming and far less bandwidth used",
           "Lossy files sound better than the original",
           "Lossy compression is free and lossless is not",
           "Lossless cannot be used for audio"], 0,
          "Bandwidth is the constraint. Lossy files can be a tenth of the size, which is what makes streaming to millions of users practical."),
        Q("What happens to a lossless compressed file when it is decompressed?",
          ["It is restored exactly to the original", "It loses a small amount of quality",
           "It stays compressed", "It becomes a lossy file"], 0,
          "That is the defining property of lossless: perfect reconstruction, byte for byte."),
        Q("A hospital must store patient scan images for legal review. Which compression should be used?",
          ["Lossless, because losing any detail could affect a diagnosis",
           "Lossy, because the files would be smaller",
           "No compression is possible on images",
           "Lossy, because scans are not important"], 0,
          "Any removed detail could be the detail that mattered clinically or legally, so nothing may be discarded."),
        Q("Which pair of formats are both lossy?",
          ["MP3 and JPEG", "PNG and FLAC", "ZIP and GIF", "PNG and MP3"], 0,
          "MP3 for audio and JPEG for images both discard data permanently. PNG, FLAC, ZIP and GIF are lossless."),
    ],
    exam=[
        EQ("State two reasons why files are compressed.", 2, [
            MP("Uses less storage space", ["storage", "space", "less room", "smaller"]),
            MP("Faster to transmit or download because less data is sent", ["faster", "transmit", "download", "bandwidth", "quicker", "less data"]),
        ], "Files are compressed so that they take up less storage space on a device, allowing more files to be stored. They are also compressed so that they can be transmitted more quickly across a network, because there is less data to send, which reduces both the download time and the bandwidth used.",
           command="State"),
        EQ("Explain the difference between lossy and lossless compression.", 4, [
            MP("Lossy permanently removes some of the data from the file", ["removes", "permanently", "deleted", "discarded", "lost"]),
            MP("The original file cannot be recovered after lossy compression", ["cannot be recovered", "not restored", "irreversible", "gone", "cannot get back"]),
            MP("Lossless reduces size without removing any data", ["no data", "nothing removed", "all data kept", "retained"]),
            MP("The original file can be perfectly restored when decompressed", ["perfectly", "exactly", "restored", "reconstructed", "original back"]),
        ], "Lossy compression reduces file size by permanently removing some of the data, typically detail that the human eye or ear is unlikely to notice, such as very high frequencies in audio or subtle colour differences in an image. Because the data has been deleted, the original file cannot be recovered from the compressed version. Lossless compression reduces file size without removing any data at all, instead recording the information more efficiently by identifying repetition and encoding it compactly. When a losslessly compressed file is decompressed, the original is restored exactly, byte for byte.",
           command="Explain"),
        EQ("A company needs to email a large spreadsheet containing financial records to its accountant. Explain which type of compression should be used and why.", 4, [
            MP("Lossless compression should be used", ["lossless"]),
            MP("Every value in a financial spreadsheet is significant", ["every value", "all data", "important", "accurate", "figures", "numbers matter"]),
            MP("Lossy compression would permanently remove data, corrupting the records", ["lossy would remove", "corrupt", "lose data", "wrong figures", "inaccurate", "permanently"]),
            MP("Lossless still reduces the size so it is quicker to email, and the file opens exactly as it was", ["smaller", "quicker to send", "email", "restored exactly", "identical"]),
        ], "The company should use lossless compression, for example by placing the spreadsheet in a ZIP archive. In a financial spreadsheet every single figure is significant, and the accountant needs the file to be exactly as it was created. Lossy compression works by permanently discarding data that is judged unimportant, and applied to a spreadsheet this would destroy or alter values, producing records that are inaccurate and legally worthless. Lossless compression still makes the file meaningfully smaller, so it attaches and sends more quickly and is less likely to hit an email size limit, but when the accountant decompresses it the spreadsheet is restored exactly as it was, with every value intact.",
           command="Explain"),
        EQ("Describe how lossless compression is able to reduce the size of a file without losing any data.", 3, [
            MP("It identifies repeated data or patterns within the file", ["repeated", "patterns", "repetition", "same data", "duplicates"]),
            MP("The repetition is recorded more efficiently, for example storing a value once with a count", ["count", "once", "index", "shorter code", "efficiently", "reference"]),
            MP("The original can be reconstructed exactly from this record", ["reconstructed", "restored", "exactly", "rebuilt", "decompressed"]),
        ], "Lossless compression works by finding repetition within the data rather than throwing anything away. The algorithm identifies patterns and sequences that occur more than once, and records them more efficiently, for example by storing a repeated value a single time together with a count of how many times it should appear, or by building an index of common sequences and replacing each occurrence with a short reference to that index. Because the record contains everything needed to rebuild the original, decompression reconstructs the file exactly as it was, so no data is lost.",
           command="Describe"),
        EQ("A video streaming service compresses all of its films using lossy compression. Evaluate this decision.", 6, [
            MP("Lossy gives a much greater reduction in file size than lossless", ["much smaller", "greater reduction", "far smaller", "significant reduction"]),
            MP("Smaller files use less bandwidth, allowing streaming without buffering", ["bandwidth", "buffering", "streaming", "faster", "less data"]),
            MP("Less storage is needed on the servers, reducing cost", ["storage", "servers", "cost", "cheaper", "space"]),
            MP("Some quality is permanently lost", ["quality", "lost", "permanently", "reduced", "detail removed"]),
            MP("The removed data is chosen to be least noticeable to viewers, so the impact is limited", ["not noticeable", "eye cannot", "barely", "hardly notice", "least noticeable"]),
            MP("Concludes that lossy is appropriate here, with a caveat such as keeping lossless masters", ["appropriate", "correct decision", "justified", "master copy", "original", "conclusion", "sensible"]),
        ], "Using lossy compression is the right decision for a streaming service. Lossy compression achieves a far greater reduction in file size than lossless could, often reducing a film to a small fraction of its original size, and this directly determines whether streaming is viable at all. Smaller files require far less bandwidth per viewer, which means films start quickly and play without buffering even on slower home connections, and it also means the service can serve many more simultaneous viewers from the same infrastructure. Storage costs fall too, since a library of thousands of films takes up a fraction of the space it otherwise would. The cost is that quality is permanently reduced and the original cannot be recovered from the compressed copy. However, lossy video compression is designed to discard the information the human visual system is least sensitive to, so on a typical television or phone screen most viewers notice little or no difference. On balance the decision is correct, because without lossy compression streaming at scale would be impossible. The service should, however, retain uncompressed or losslessly compressed master copies of each film, so that higher quality versions can be produced in future as bandwidth improves, rather than being permanently limited by today's compressed files.",
           command="Evaluate"),
    ],
)

# ================================================== 1.3.1 Networks and topologies

T_NETWORKS = Topic(
    slug="networks-and-topologies",
    title="Networks and Topologies",
    spec="1.3.1",
    icon="i-network",
    minutes=30,
    blurb="LANs and WANs, the hardware that makes a network work, client server against peer to peer, star against mesh, and the factors that decide how fast it all runs.",
    fact="The first message ever sent over ARPANET, the ancestor of the internet, was meant to be the word LOGIN. The system crashed after two letters, so the first thing ever transmitted across the internet was LO.",
    sections=[
        Section("LAN and WAN", """
A **network** is two or more computers connected together so they can share data and resources.

### LAN, local area network

- Covers a **small geographical area**, such as one building or one site
- The **hardware is owned by the organisation** that uses it
- Examples: a school, an office, a home

### WAN, local area network becomes wide area network

- Covers a **large geographical area**, potentially the whole world
- The organisation **does not own all the infrastructure**, it leases connections from telecommunications companies
- Examples: the internet, a bank connecting branches in different cities

!key The distinguishing point :: The real difference is ownership as well as size. In a LAN the organisation owns the cabling and hardware. In a WAN it uses third party infrastructure that it does not own.

### Advantages and disadvantages of networking

**Advantages**

- Share files and data easily
- Share hardware such as printers, saving money
- Share an internet connection
- Central backup of all data
- Central management of user accounts and software updates

**Disadvantages**

- Expensive to set up: cabling, servers and hardware
- Malware can spread quickly across the network
- If the server fails, everyone is affected
- Requires a network manager, which is a staffing cost
- Increased security risk, since data is accessible from many machines
"""),
        Section("Network hardware", """
| Device | What it does |
| **NIC** | Network Interface Card. Allows a device to connect to a network, wired or wireless. Each has a unique MAC address. |
| **Switch** | Connects devices on a LAN. It reads the destination MAC address of each frame and sends it **only to the correct device**, which reduces unnecessary traffic. |
| **Router** | Connects **different networks** together and directs data between them using IP addresses. Your home router joins your LAN to the internet. |
| **WAP** | Wireless Access Point. Allows devices to connect to the network wirelessly using radio waves. |
| **Transmission media** | The cabling or radio waves that carry the data: copper twisted pair, fibre optic, or wireless. |

!warn Switch versus router :: A switch works **inside** one network using MAC addresses. A router works **between** networks using IP addresses. Confusing these two is one of the most common lost marks in this topic.

### Servers and clients

A **server** is a computer that provides services or resources to other computers. Common types include file servers, print servers, web servers and mail servers.
"""),
        Section("Client server and peer to peer", """
### Client server

One or more powerful central **servers** provide resources, and **clients** request them.

**Advantages**

- Central backup, so data is protected in one place
- Central management of security, updates and user accounts
- Easier to add new clients
- Files are stored centrally, so any user can access their work from any machine

**Disadvantages**

- Expensive: servers and specialist staff cost money
- If the server fails, the whole network loses access
- The server can become a bottleneck if demand is high

### Peer to peer

Every computer is equal. Each acts as both client and server, sharing files directly with the others.

**Advantages**

- Cheap, no server to buy
- Easy to set up, needs no specialist knowledge
- No single point of failure, if one machine goes down the rest continue

**Disadvantages**

- No central backup, so files must be backed up individually
- Files are spread across machines, so a computer must be switched on for its files to be available
- Difficult to manage security and updates across many machines
- Performance drops as more peers join

!exam Choosing between them :: A home with three computers sharing a printer suits peer to peer, because it is cheap and simple. A school with 500 machines needs client server, because central backup, central account management and central security are essential at that scale.
"""),
        Section("Star and mesh topologies", """
A **topology** is the layout of a network: how the devices are physically or logically arranged.

### Star topology

Every device connects to a **central switch or hub**.

**Advantages**

- If one cable fails, only that one device is affected
- Easy to add or remove devices without disrupting anyone else
- Very few data collisions, because the switch directs traffic
- Good performance, since each device has its own dedicated connection

**Disadvantages**

- Requires a lot of cable, so it is expensive to install
- If the **central switch fails, the entire network fails**

### Mesh topology

Every device connects to **many other devices**, so there are multiple routes for data.

In a **full mesh** every device connects to every other. In a **partial mesh** only some connections exist.

**Advantages**

- Extremely reliable: if one connection fails, data is rerouted another way
- No single point of failure
- Data can take the fastest available route
- Adding devices does not slow the network as much as other topologies

**Disadvantages**

- Very expensive in cabling for a wired mesh
- Complex to set up and maintain

Wireless mesh networks avoid the cabling cost, which is why mesh is now common in smart home and large scale Wi-Fi systems.

!key The comparison sentence :: A star topology fails completely if the central switch fails, whereas a mesh has no single point of failure because data can be rerouted through alternative paths.
"""),
        Section("Factors affecting network performance", """
Five factors, and you need to be able to explain each.

1. **Bandwidth.** The amount of data that can be carried per second. Higher bandwidth means more data flows at once. Bandwidth on a network is **shared**, so more users each get less.

2. **Number of users.** More devices using the network at once means the available bandwidth is divided further, so each device gets less and everything slows.

3. **Transmission media.** Fibre optic carries far more data over far greater distances than copper, and is immune to electrical interference. Copper is cheaper but slower and degrades over distance.

4. **Error rate and interference.** Wireless signals weaken with distance and are blocked by walls, and can be interfered with by other devices. Errors mean data has to be resent, which reduces effective speed.

5. **Latency.** The delay between sending data and it arriving. Even on a fast connection, high latency makes interactive applications such as video calls and online gaming feel unresponsive.

!warn Bandwidth is not speed :: Bandwidth is capacity, like the number of lanes on a motorway. Latency is delay, like how long the journey takes. A satellite link can have huge bandwidth and terrible latency.
"""),
    ],
    keyterms=[
        ("LAN", "Local area network. Covers a small geographical area with hardware owned by the organisation."),
        ("WAN", "Wide area network. Covers a large geographical area using infrastructure the organisation does not own."),
        ("NIC", "Network interface card. The hardware that allows a device to connect to a network."),
        ("Switch", "A device that connects computers on a LAN and sends data only to the intended recipient using MAC addresses."),
        ("Router", "A device that connects different networks together and directs data between them using IP addresses."),
        ("WAP", "Wireless access point. Allows devices to join a network wirelessly."),
        ("Client server", "A network model where central servers provide resources to client computers."),
        ("Peer to peer", "A network model where all computers are equal and share resources directly with each other."),
        ("Topology", "The layout or arrangement of devices in a network, such as star or mesh."),
        ("Bandwidth", "The amount of data that can be transmitted over a connection in a given time."),
        ("Latency", "The delay between data being sent and it arriving at its destination."),
    ],
    grade="""
Three habits separate top answers here.

**Say what fails and what still works.** Reliability questions want specifics. "In a star topology, if one cable fails only the device on that cable is affected, but if the central switch fails the entire network goes down."

**Attach the reason to the recommendation.** Choosing client server for a school is not enough. Say that central backup protects student work, central account management lets any student log in at any machine, and central updates keep 500 machines secure without visiting each one.

**Separate bandwidth from latency and from number of users.** Many students blur all three into "the internet is slow". Bandwidth is capacity, latency is delay, and number of users is what divides the capacity up.

+ Explain the difference between a switch and a router without hesitating
+ Give three advantages and three disadvantages each for client server and peer to peer
+ Compare star and mesh on reliability, cost and expandability
+ Explain all five performance factors with a cause and an effect
""",
    mistakes=[
        "Saying a WAN is 'just a bigger LAN'. The ownership of the infrastructure is the key distinction.",
        "Confusing switches and routers. Switches work within a network using MAC addresses, routers work between networks using IP addresses.",
        "Saying peer to peer has 'no server'. Every peer acts as both client and server, which is the point.",
        "Claiming a star topology is more reliable than mesh. Mesh has no single point of failure, a star has one at the central switch.",
        "Using bandwidth and speed interchangeably. Bandwidth is capacity, latency is delay.",
    ],
    quiz=[
        Q("Which statement best describes a LAN?",
          ["A network covering a small area where the organisation owns the hardware",
           "A network covering a large geographical area",
           "A network that only uses wireless connections",
           "A network with fewer than ten computers"], 0,
          "Size and ownership together define a LAN. The organisation owns the cabling and hardware on a single site."),
        Q("What does a switch use to decide where to send data?",
          ["The MAC address of the destination device", "The IP address of the destination network",
           "The name of the file being sent", "The port number only"], 0,
          "A switch operates within a LAN and reads MAC addresses so that data goes only to the intended recipient."),
        Q("Which device connects two different networks together?",
          ["A router", "A switch", "A network interface card", "A wireless access point"], 0,
          "Routers join networks and direct traffic between them using IP addresses. A switch works within one network."),
        Q("What is the main disadvantage of a star topology?",
          ["If the central switch fails, the whole network fails",
           "A single cable failure brings down all devices",
           "Data collisions happen constantly",
           "Devices cannot be added once it is set up"], 0,
          "The central switch is a single point of failure. Individual cable failures only affect one device, which is a strength."),
        Q("Which network model is best for a school with 600 computers?",
          ["Client server, because it provides central backup, security and account management",
           "Peer to peer, because it is cheaper to set up",
           "Peer to peer, because there is no single point of failure",
           "Neither, a school should not use a network"], 0,
          "At that scale, central management is essential. Managing security and backups across 600 independent peers would be unworkable."),
        Q("Why is a mesh topology very reliable?",
          ["If one connection fails, data can be rerouted along an alternative path",
           "It uses less cable than other topologies",
           "It requires no switches",
           "It only allows one device to transmit at a time"], 0,
          "Multiple routes between devices mean there is no single point of failure."),
        Q("Which factor describes the delay between sending data and it arriving?",
          ["Latency", "Bandwidth", "Colour depth", "Topology"], 0,
          "Latency is delay. Bandwidth is capacity. A link can have high bandwidth and high latency at the same time."),
        Q("Why does network performance drop when more users connect?",
          ["The available bandwidth is shared between more devices",
           "The latency of each cable increases",
           "The router changes its IP address",
           "MAC addresses become duplicated"], 0,
          "Bandwidth is a shared resource. Splitting the same capacity between more devices means less for each."),
        Q("What is one advantage of fibre optic cable over copper?",
          ["It carries more data over longer distances without interference",
           "It is much cheaper to install",
           "It works without any hardware",
           "It can only be used indoors"], 0,
          "Fibre uses light rather than electricity, so it is immune to electromagnetic interference and signals degrade far less over distance."),
        Q("In a peer to peer network, what happens if one computer is switched off?",
          ["The files stored on that computer become unavailable to others",
           "The whole network stops working",
           "All files are automatically transferred to another peer",
           "The router shuts down"], 0,
          "Files live on individual machines, so a peer must be powered on and connected for its files to be reachable."),
    ],
    exam=[
        EQ("State two differences between a LAN and a WAN.", 2, [
            MP("A LAN covers a small geographical area, a WAN covers a large one", ["small area", "large area", "geographical", "one site", "wide area", "distance"]),
            MP("LAN hardware is owned by the organisation, WAN infrastructure is often leased from third parties", ["owned", "leased", "rented", "third party", "telecommunications", "does not own"]),
        ], "A LAN covers a small geographical area such as a single building or site, whereas a WAN covers a large geographical area and may span cities or countries. In addition, the organisation using a LAN owns all of the hardware and cabling itself, whereas a WAN relies on infrastructure leased from telecommunications companies that the organisation does not own.",
           command="State"),
        EQ("Explain the difference between the role of a switch and the role of a router.", 4, [
            MP("A switch connects devices within a single network or LAN", ["within", "same network", "lan", "connects devices", "inside"]),
            MP("A switch uses MAC addresses to send data only to the intended device", ["mac address", "intended", "correct device", "only to"]),
            MP("A router connects different networks together", ["different networks", "between networks", "join networks", "connects networks"]),
            MP("A router uses IP addresses to direct data between networks", ["ip address", "routes", "directs", "between"]),
        ], "A switch operates inside a single network such as a LAN, connecting the devices on that network to one another. It reads the MAC address in each frame and forwards it only to the port where the intended recipient is connected, which avoids sending unnecessary traffic to every device. A router works at a higher level, connecting entirely different networks together, such as joining a home LAN to the internet. It uses IP addresses to decide which network a packet must be sent towards, and selects the appropriate route to get it there.",
           command="Explain"),
        EQ("A small business with six computers is deciding between a peer to peer network and a client server network. Recommend which they should use and justify your answer.", 6, [
            MP("Recommends peer to peer", ["peer to peer", "p2p"]),
            MP("Cheaper because no dedicated server hardware needs to be bought", ["cheaper", "cost", "no server", "less expensive", "budget"]),
            MP("Simple to set up without specialist network staff", ["easy", "simple", "no specialist", "no technician", "straightforward"]),
            MP("With only six computers the management overhead of client server is not justified", ["six", "small", "few computers", "not needed", "overkill"]),
            MP("Notes the drawback that there is no central backup", ["backup", "no central", "individually", "back up separately"]),
            MP("Notes that files are unavailable if a computer is switched off, and suggests a mitigation", ["switched off", "unavailable", "turned off", "must be on", "cloud", "external drive"]),
        ], "The business should use a peer to peer network. With only six computers, the main advantage is cost: a peer to peer network needs no dedicated server hardware and no server software licences, so the setup cost is far lower than a client server arrangement. It is also simple enough to configure and maintain without employing a network technician, which matters for a business of this size where there is unlikely to be dedicated IT staff. A client server network would bring central backup, central security and central account management, but with six machines the administrative burden those features remove is small, so the extra expense is difficult to justify. The business should be aware of the drawbacks. There is no central backup, so each computer's files must be backed up separately and it would be easy for this to be neglected until data is lost. Files are also only available while the computer holding them is switched on, which can be inconvenient. Both problems can be reduced cheaply by adding a shared network attached storage drive or a cloud storage subscription for important files, which keeps the simplicity of peer to peer while covering its weakest point.",
           command="Justify"),
        EQ("Compare a star topology and a mesh topology in terms of reliability and cost.", 4, [
            MP("Star has a single point of failure at the central switch", ["single point of failure", "central switch", "switch fails", "whole network fails"]),
            MP("Mesh has multiple paths so data can be rerouted if a connection fails", ["multiple paths", "reroute", "alternative route", "no single point of failure", "redundancy"]),
            MP("Star uses less cable and is cheaper to install than a full mesh", ["less cable", "cheaper", "cost", "less expensive"]),
            MP("A wired mesh requires many connections making it expensive and complex", ["expensive", "many cables", "complex", "costly", "lots of connections"]),
        ], "In terms of reliability, a mesh topology is stronger. Every device in a mesh is connected to several others, so if one link fails the data is simply rerouted along an alternative path and the network continues to function, meaning there is no single point of failure. A star topology is reliable against individual cable faults, because a broken cable only disconnects the one device attached to it, but it depends entirely on the central switch, and if that switch fails then every device loses connectivity. In terms of cost, the star topology wins clearly. It needs only one cable per device running back to the switch, whereas a full wired mesh requires a connection between every pair of devices, so the amount of cabling and the complexity of installation rise very steeply as more devices are added.",
           command="Compare"),
        EQ("Explain three factors that can affect the performance of a network.", 6, [
            MP("Bandwidth is the amount of data that can be carried per second", ["bandwidth", "capacity", "data per second"]),
            MP("Higher bandwidth allows more data to be transferred, but it is shared between users", ["shared", "more data", "divided", "split between"]),
            MP("The number of users affects performance because bandwidth is divided between them", ["number of users", "more users", "more devices", "each gets less"]),
            MP("Transmission media matters, with fibre optic faster and less prone to interference than copper", ["fibre", "copper", "cable", "wireless", "interference", "medium"]),
            MP("Interference and errors cause data to be resent, reducing effective speed", ["interference", "errors", "resent", "retransmit", "signal strength", "walls", "distance"]),
            MP("Latency is the delay before data arrives and affects interactive applications", ["latency", "delay", "lag", "response time"]),
        ], "The first factor is bandwidth, which is the amount of data the connection can carry each second. A higher bandwidth connection can move more data in the same time, but bandwidth is a shared resource, so the capacity available to any one device depends on what everyone else is doing. That leads directly to the second factor, the number of users. As more devices connect and transmit at the same time, the same total bandwidth is divided between more of them, so each device receives a smaller share and everything slows down, which is why school networks feel slowest at the start of a lesson when every student logs on at once. The third factor is the transmission media. Fibre optic cable carries far more data over much greater distances than copper and is immune to electromagnetic interference because it transmits light rather than electricity, whereas copper signals degrade over distance and can be disrupted by nearby electrical equipment. Wireless is more convenient but weakens with distance and is blocked by walls, and when signal quality is poor data has to be retransmitted, which reduces the effective throughput even though the nominal bandwidth has not changed.",
           command="Explain"),
    ],
)

# ============================== 1.3.2 Wired and wireless, protocols and layers

T_PROTOCOLS = Topic(
    slug="protocols-and-layers",
    title="Wired and Wireless Networks, Protocols and Layers",
    spec="1.3.2",
    icon="i-layers",
    minutes=30,
    blurb="Wi-Fi against Ethernet, IP and MAC addressing, every protocol on the specification with what it actually does, and why layering makes the internet possible.",
    fact="Your MAC address is burned into the network card at the factory and the first half identifies the manufacturer. Given only a MAC address, you can look up who made the device, which is why some phones now randomise it for privacy.",
    sections=[
        Section("Wired and wireless", """
### Wired, usually Ethernet

- **Faster** and more consistent speeds
- **More secure**, since an attacker needs physical access to the cable
- **More reliable**, no interference from walls or other devices
- **Lower latency**, important for gaming and video calls
- But: devices cannot move, and installing cabling is expensive and disruptive

### Wireless, Wi-Fi or Bluetooth

- **Convenient**, devices can move freely
- **Cheaper and quicker to install**, no cabling needed
- **Many devices** can connect easily
- But: **slower and less reliable**, signal weakens with distance and is blocked by walls
- **Less secure**, since the signal travels through the air and can be intercepted, so encryption is essential

!key The trade off in one line :: Wired networks offer speed, reliability and security. Wireless offers convenience, mobility and lower installation cost.

**Bluetooth** is short range wireless, typically under 10 metres, designed for connecting a small number of devices directly, such as headphones to a phone. Wi-Fi is longer range and higher bandwidth, designed to connect devices to a network.
"""),
        Section("IP addresses and MAC addresses", """
### IP address

An **IP address** identifies a device **on a network** and is used to route data between networks.

- **IPv4** uses 32 bits, written as four denary numbers 0 to 255, for example `192.168.1.24`
- **IPv6** uses 128 bits, written as eight groups of hexadecimal, because IPv4 addresses have run out
- IP addresses are **assigned by the network** and can change, for example each time you join a different Wi-Fi network

### MAC address

A **MAC address**, media access control, identifies a **specific piece of hardware**.

- 48 bits, written as six pairs of hexadecimal digits, for example `00:1B:44:11:3A:B7`
- **Assigned by the manufacturer** and does not change
- Used by switches to deliver data **within** a local network

| | IP address | MAC address |
| Identifies | A device on a network | A specific piece of hardware |
| Assigned by | The network | The manufacturer |
| Changes | Yes, can change | No, it is fixed |
| Used for | Routing between networks | Delivery within a local network |
| Format | 192.168.1.24 or IPv6 hex | 00:1B:44:11:3A:B7 |

!warn Both are needed :: A common misconception is that one replaces the other. The IP address gets the data to the right network, and the MAC address then gets it to the right device on that network.
"""),
        Section("Standards and protocols", """
A **standard** is an agreed way of doing something, so that hardware and software from different manufacturers can work together.

A **protocol** is a set of rules governing how data is transmitted between devices. Without shared protocols, two computers would be talking different languages.

| Protocol | Full name | What it does |
| **TCP** | Transmission Control Protocol | Splits data into packets, checks they all arrive, requests any that are missing, and reassembles them in the right order |
| **IP** | Internet Protocol | Addresses and routes packets across networks so they reach the right destination |
| **HTTP** | Hypertext Transfer Protocol | Requests and transfers web pages between a browser and a web server |
| **HTTPS** | HTTP Secure | The same as HTTP but the data is encrypted, protecting it from being read if intercepted |
| **FTP** | File Transfer Protocol | Sends and receives files between computers, typically uploading to a server |
| **POP** | Post Office Protocol | Retrieves email from a server and normally **deletes it from the server** |
| **IMAP** | Internet Message Access Protocol | Retrieves email but **keeps it on the server**, so it syncs across multiple devices |
| **SMTP** | Simple Mail Transfer Protocol | **Sends** email from a client to a server, and between mail servers |

!exam The email trio :: SMTP sends. POP downloads and removes. IMAP downloads and keeps synced. If a question mentions reading the same emails on a phone and a laptop, the answer is IMAP.

### TCP/IP working together

TCP and IP are almost always used as a pair.

- **TCP** handles the reliability: breaking data into packets, numbering them, checking they arrive and reassembling them.
- **IP** handles the addressing: making sure each packet is routed to the correct destination.
"""),
        Section("Layers", """
Network protocols are organised into **layers**. Each layer has a specific job and only interacts with the layers directly above and below it.

The four layer TCP/IP model:

| Layer | Job | Example protocols |
| Application | Provides services to the user's software | HTTP, HTTPS, FTP, SMTP, IMAP |
| Transport | Splits data into packets and ensures reliable delivery | TCP, UDP |
| Internet | Adds addresses and routes packets across networks | IP |
| Link | Handles the physical transmission over the medium | Ethernet, Wi-Fi |

### Why layering is used

- **It breaks a complex problem into manageable parts**, so each layer can be designed and understood separately.
- **Layers can be changed independently.** Switching from copper to fibre changes only the link layer, and everything above it carries on unchanged.
- **It allows interoperability**, because manufacturers only need to follow the rules of the layer they are working in.
- **It makes fault finding easier**, since a problem can be isolated to one layer.
- **Different protocols can be used at the same layer** without affecting the rest, for example choosing IMAP instead of POP.

!key The exam answer :: Layers divide the complexity of network communication into self contained parts, so each layer can be developed, changed or replaced without affecting the others.
"""),
    ],
    keyterms=[
        ("Protocol", "A set of rules governing how data is transmitted between devices."),
        ("Standard", "An agreed specification that allows equipment from different manufacturers to work together."),
        ("IP address", "An address identifying a device on a network, used to route data between networks."),
        ("MAC address", "A unique address assigned to network hardware by its manufacturer, used within a local network."),
        ("TCP", "Transmission Control Protocol. Splits data into packets and guarantees they arrive and are reassembled correctly."),
        ("IP", "Internet Protocol. Addresses and routes packets across networks."),
        ("HTTPS", "The encrypted version of HTTP, protecting web traffic from being read if intercepted."),
        ("SMTP", "The protocol used to send email."),
        ("POP", "A protocol that retrieves email and normally deletes it from the server."),
        ("IMAP", "A protocol that retrieves email while keeping it on the server so it syncs across devices."),
        ("Layer", "A distinct level of network functionality with a defined job, interacting only with adjacent layers."),
    ],
    grade="""
Two things earn the top marks here.

**Never define a protocol as 'a set of rules' and stop.** Every protocol is a set of rules. Say what the rules are for. TCP is the set of rules for splitting data into packets and ensuring they arrive complete and in order.

**On layering, give a consequence not just a description.** The strongest phrasing names a change and says what is unaffected: "Because Wi-Fi and Ethernet both sit at the link layer, a network can switch from cable to wireless without any change to HTTP, TCP or IP above it."

The email protocols come up almost every year, and the discriminator is IMAP against POP. Learn the scenario: multiple devices means IMAP.

+ Match all eight protocols to their function without hesitation
+ Explain the IP against MAC distinction using assignment and purpose, not just format
+ Give three benefits of layering, each with a consequence
+ Choose wired or wireless for a scenario and justify with the specific constraint in the question
""",
    mistakes=[
        "Saying HTTPS 'is more secure' with no mechanism. It encrypts the data so that intercepted traffic cannot be read.",
        "Saying POP and IMAP send email. They retrieve it. SMTP sends.",
        "Saying a MAC address can be assigned by the network. It is set by the manufacturer.",
        "Describing layers as 'to make it faster'. Layering is about manageability and interoperability, not speed.",
        "Giving TCP the job of addressing. TCP handles packets and reliability, IP handles addressing and routing.",
    ],
    quiz=[
        Q("Which protocol is responsible for splitting data into packets and ensuring they all arrive?",
          ["TCP", "IP", "HTTP", "SMTP"], 0,
          "TCP handles reliability: numbering packets, checking for missing ones and reassembling them in order. IP handles addressing."),
        Q("Which protocol is used to send an email?",
          ["SMTP", "POP", "IMAP", "FTP"], 0,
          "SMTP sends. POP and IMAP both retrieve mail from a server."),
        Q("A user reads the same emails on their phone and laptop and wants them to stay in sync. Which protocol should be used?",
          ["IMAP", "POP", "SMTP", "HTTP"], 0,
          "IMAP keeps messages on the server, so any device sees the same mailbox state. POP typically downloads and deletes."),
        Q("Which statement about MAC addresses is correct?",
          ["They are assigned by the manufacturer and identify specific hardware",
           "They are assigned by the network and change when you move",
           "They are used to route data between different networks",
           "They are 32 bits long"], 0,
          "A MAC address is burned into the network interface card and is used for delivery within a local network."),
        Q("What is the main advantage of HTTPS over HTTP?",
          ["Data is encrypted so it cannot be read if intercepted",
           "Web pages load faster", "It uses less bandwidth", "It works without an IP address"], 0,
          "The S is for secure. Encryption means that even if traffic is captured it cannot be understood."),
        Q("Why are network protocols organised into layers?",
          ["To break a complex system into parts that can be developed and changed independently",
           "To make the network transmit data faster",
           "To reduce the number of protocols needed to one",
           "To remove the need for IP addresses"], 0,
          "Layering is about managing complexity and enabling interoperability. Changing one layer does not disturb the others."),
        Q("Which is an advantage of a wired connection over wireless?",
          ["Faster and more consistent speeds with lower latency",
           "Devices can move around freely",
           "It is cheaper to install in an existing building",
           "It supports more devices without any hardware"], 0,
          "Cable gives higher and steadier throughput with less interference. Convenience and mobility are the wireless advantages."),
        Q("Which protocol is used to transfer files to a web server?",
          ["FTP", "SMTP", "IMAP", "TCP"], 0,
          "File Transfer Protocol is designed for uploading and downloading files between computers."),
        Q("An IPv4 address is how many bits long?",
          ["32", "48", "128", "16"], 0,
          "IPv4 is 32 bits, written as four numbers from 0 to 255. IPv6 is 128 bits and MAC addresses are 48 bits."),
        Q("At which layer would you find HTTP and SMTP?",
          ["The application layer", "The transport layer", "The internet layer", "The link layer"], 0,
          "Application layer protocols provide services directly to user software such as browsers and mail clients."),
    ],
    exam=[
        EQ("State what is meant by a protocol.", 2, [
            MP("A set of rules", ["set of rules", "rules", "agreed standard"]),
            MP("Governing how data is transmitted or communicated between devices", ["transmitted", "communication", "between devices", "sending data", "format"]),
        ], "A protocol is an agreed set of rules that governs how data is transmitted and communicated between devices on a network, covering things such as how the data is formatted, how it is addressed and how errors are handled, so that different systems can understand each other.",
           command="State"),
        EQ("Explain two differences between an IP address and a MAC address.", 4, [
            MP("An IP address identifies a device on a network, a MAC address identifies a specific piece of hardware", ["identifies", "device on a network", "hardware", "physical device", "network card"]),
            MP("IP addresses are assigned by the network, MAC addresses by the manufacturer", ["assigned", "network", "manufacturer", "factory", "built in"]),
            MP("An IP address can change, a MAC address is fixed", ["change", "changes", "fixed", "permanent", "does not change", "static"]),
            MP("IP addresses route data between networks, MAC addresses deliver data within a local network", ["between networks", "routing", "within", "local network", "same network", "switch"]),
        ], "The first difference is what they identify and who assigns them. An IP address identifies a device's position on a network and is assigned by the network itself, which means it can change, for example when a laptop joins a different Wi-Fi network. A MAC address identifies one specific piece of network hardware, is assigned by the manufacturer when the network interface card is made, and does not change. The second difference is their purpose. IP addresses are used to route data between different networks across the internet, whereas MAC addresses are used by switches to deliver data to the correct device within a single local network once it has arrived.",
           command="Explain"),
        EQ("Explain why network protocols are organised into layers.", 4, [
            MP("It breaks a complex process into smaller self contained parts", ["complex", "smaller parts", "manageable", "self contained", "divided", "simpler"]),
            MP("Each layer has a specific role and only interacts with adjacent layers", ["specific role", "own job", "adjacent", "above and below", "defined"]),
            MP("A layer can be changed or replaced without affecting the others", ["changed", "replaced", "independently", "without affecting", "swap"]),
            MP("It allows equipment and software from different manufacturers to work together", ["different manufacturers", "interoperability", "compatible", "work together", "standards"]),
        ], "Network communication is a very complex process, and layering divides it into smaller self contained parts so that each part can be designed, understood and maintained separately. Each layer is given one specific responsibility and only interacts with the layers immediately above and below it, which means a layer can be changed or replaced entirely without the rest of the stack being affected. For example, a network can switch from Ethernet cabling to Wi-Fi at the link layer while HTTP, TCP and IP continue to work exactly as before. Layering also allows manufacturers to build hardware and software that only has to comply with the rules of one layer, which means equipment from different companies can interoperate, and it makes fault finding easier because a problem can be isolated to a single layer.",
           command="Explain"),
        EQ("A hotel is installing a network for its guests. Discuss whether it should use a wired or a wireless network.", 6, [
            MP("Recommends wireless", ["wireless", "wifi", "wi-fi"]),
            MP("Guests need mobility and use their own devices in rooms and public areas", ["mobility", "move", "own devices", "phones", "laptops", "anywhere", "rooms"]),
            MP("Cheaper and less disruptive than running cable to every room", ["cheaper", "cost", "cabling", "disruptive", "no cables", "installation"]),
            MP("Wireless is slower and less reliable, with signal weakened by walls and distance", ["slower", "less reliable", "walls", "distance", "signal", "interference"]),
            MP("Wireless is less secure as the signal can be intercepted, so encryption is essential", ["less secure", "intercepted", "encryption", "security", "wpa"]),
            MP("Reaches a justified conclusion, possibly a hybrid with wired backbone", ["conclusion", "therefore", "overall", "hybrid", "combination", "backbone", "recommend"]),
        ], "The hotel should provide a wireless network for guests. Guests arrive with their own phones, tablets and laptops and expect to use them in their rooms, in the lobby and in the restaurant, so mobility is essential and a wired connection that ties a device to one socket would not meet that need. Installing wireless access points is also considerably cheaper and far less disruptive than running Ethernet cable to every guest room in an existing building, where floors and walls would have to be opened up. There are real disadvantages. Wireless is slower and less consistent than cable, and the signal is weakened by the thick walls and long corridors typical of hotels, so careful placement of multiple access points is needed to avoid dead spots. It is also less secure, because the signal travels through the air and can be intercepted by anyone in range, so strong encryption such as WPA3 and an isolated guest network are necessary to stop guests seeing each other's traffic or reaching the hotel's own systems. The sensible solution is a hybrid: a wired backbone connecting the access points, the reception computers and the booking system, since those machines never move and benefit from the speed and security of cable, with wireless provided throughout the building for guests. This gives guests the mobility they expect while keeping the hotel's own critical systems on the faster and more secure wired network.",
           command="Discuss"),
        EQ("Describe the roles of the TCP and IP protocols and explain why they are used together.", 4, [
            MP("TCP splits data into packets and numbers them", ["splits", "packets", "divides", "breaks", "numbers"]),
            MP("TCP checks all packets arrive and reassembles them in the correct order", ["checks", "arrive", "reassemble", "correct order", "missing", "resend"]),
            MP("IP addresses each packet and routes it to the correct destination", ["address", "routes", "routing", "destination", "directs"]),
            MP("Together they provide addressing and reliable delivery, which are both needed", ["together", "both", "addressing and reliability", "complete", "combined"]),
        ], "TCP, the Transmission Control Protocol, takes the data being sent and splits it into numbered packets. At the receiving end it checks that every packet has arrived, requests the retransmission of any that are missing or corrupted, and then reassembles the packets back into the original data in the correct order. IP, the Internet Protocol, is responsible for addressing: it attaches the source and destination IP addresses to each packet and determines the route the packet should take across the networks between them. They are used together because each solves only half the problem. IP can get a packet to the right destination but offers no guarantee that it arrives or that packets arrive in order, while TCP can guarantee complete, correctly ordered delivery but has no mechanism for finding the destination in the first place. Combined as TCP/IP they provide both reliable delivery and correct routing.",
           command="Describe"),
    ],
)

# ========================================================= 1.4 Network security

T_SECURITY = Topic(
    slug="network-security",
    title="Network Security: Threats and Prevention",
    spec="1.4",
    icon="i-shield",
    minutes=32,
    blurb="Every threat on the specification explained by how it actually works, every prevention method, and the reason the biggest weakness in any network is a person.",
    fact="The most successful phishing emails are not the badly spelled ones. They are the ones that create urgency: a fake message saying your account will be closed in 24 hours defeats careful thinking, because panicking people stop checking details.",
    sections=[
        Section("Forms of attack", """
### Malware

**Malware** is any software written to cause harm. The main types:

- **Virus.** Attaches itself to a file or program and spreads when that file is opened or shared. It needs a host file and a user action.
- **Worm.** Spreads by itself across a network without any user action, which makes it spread very fast.
- **Trojan.** Disguises itself as legitimate software. The user installs it willingly, and it then does something harmful.
- **Ransomware.** Encrypts the victim's files and demands payment for the key.
- **Spyware.** Secretly records activity, such as keystrokes, and sends it to an attacker.

!warn Virus and worm are not the same :: A virus needs a host file and someone to open it. A worm spreads on its own. Getting this distinction right is worth a mark.

### Social engineering

**Social engineering** is manipulating people rather than attacking technology. The target is human trust, not a software flaw.

- **Phishing.** Fraudulent emails or messages pretending to be from a legitimate organisation, designed to trick the victim into revealing passwords or bank details, or into clicking a malicious link.
- **Shouldering** or shoulder surfing. Watching someone enter a PIN or password.
- **Blagging** or pretexting. Inventing a scenario to gain trust, such as phoning an employee while pretending to be from IT support and asking for their password.
- **Name generator attacks.** Quizzes asking for your first pet and street name, which are common security question answers.

!key Why people are the weak point :: Technical defences can be very strong, but a person can be persuaded to hand over a password, and no firewall can stop an attacker who has been given valid credentials.

### Brute force attack

Trying every possible combination of characters until the correct password is found, usually automated so millions of attempts are made per second.

Defences: strong long passwords, limiting the number of login attempts, and two factor authentication.

### Denial of service attack

A **DoS attack** floods a server with so many requests that it cannot respond to genuine users, so the service becomes unavailable.

A **DDoS**, distributed denial of service, uses many compromised machines at once, which makes it far harder to block because the traffic comes from thousands of different addresses.

### Data interception and theft

Data is captured while travelling across a network, for example by **packet sniffing** on an unencrypted public Wi-Fi network. The attacker reads the traffic and extracts passwords or personal information.

Defence: encryption. Intercepted data is then unreadable.

### SQL injection

A website that builds a database query directly from user input can be attacked by typing SQL code into an input box. If the input is not checked, the database executes the attacker's code, which can reveal, alter or delete data.

Example: entering `' OR '1'='1` into a login box may make the condition always true, granting access without a password.

Defence: **validation** of all input, and parameterised queries that keep data separate from code.
"""),
        Section("Preventing attacks", """
### Penetration testing

Deliberately attacking your own system, with permission, to find weaknesses before a real attacker does. The report identifies vulnerabilities so they can be fixed.

### Anti malware software

Scans files against a database of known malware signatures and monitors behaviour for suspicious activity. It quarantines or removes anything it finds. It must be **kept up to date**, because new malware appears constantly.

### Firewalls

A firewall sits between a network and the outside world and **inspects incoming and outgoing traffic**, blocking anything that does not meet its rules. It can block specific ports, addresses or applications.

### User access levels

Different users are given different permissions, so each person can access only what their role requires. A student cannot see staff files, and a teacher cannot change system settings.

This limits the damage a compromised account can do, and reduces accidental damage too.

### Passwords

Strong passwords are long, mix character types and avoid dictionary words and personal information. Combined with a limit on login attempts, they defeat brute force attacks. Two factor authentication adds a second requirement, so a stolen password alone is not enough.

### Encryption

Data is scrambled using a key so that it is meaningless to anyone without the key.

Encryption does **not** stop data being intercepted. It makes intercepted data useless. That distinction is frequently tested.

### Physical security

Locked server rooms, keycard access, CCTV and alarms. No amount of software security helps if someone can walk out with the server.

!exam Matching defence to threat :: Questions often give a threat and ask for a suitable prevention. Learn the pairs: brute force pairs with strong passwords and attempt limits, interception pairs with encryption, SQL injection pairs with input validation, malware pairs with anti malware and firewalls, social engineering pairs with staff training.
"""),
    ],
    keyterms=[
        ("Malware", "Software written with the intention of causing harm to a computer system or its data."),
        ("Virus", "Malware that attaches to a host file and spreads when that file is opened or shared."),
        ("Worm", "Malware that spreads itself across a network without needing any user action."),
        ("Trojan", "Malware disguised as legitimate software that the user installs voluntarily."),
        ("Ransomware", "Malware that encrypts files and demands payment for the decryption key."),
        ("Social engineering", "Manipulating people into revealing information or performing actions that compromise security."),
        ("Phishing", "Fraudulent messages imitating a legitimate organisation in order to obtain personal information."),
        ("Brute force attack", "Systematically trying every possible password combination until the correct one is found."),
        ("Denial of service", "Flooding a server with requests so that it cannot respond to legitimate users."),
        ("SQL injection", "Entering SQL code into an input field so that an unprotected database executes it."),
        ("Penetration testing", "Authorised simulated attacks on a system to identify weaknesses before criminals find them."),
        ("Firewall", "Hardware or software that inspects network traffic and blocks anything not meeting its rules."),
        ("Encryption", "Scrambling data using a key so it cannot be understood by anyone who intercepts it."),
        ("User access level", "A permission setting that controls which files and features a particular user can reach."),
    ],
    grade="""
The marks on this topic are almost entirely about **mechanism** and **matching**.

**Explain how, not what.** A grade 5 answer says "a firewall protects the network". A grade 9 answer says "a firewall examines every packet entering and leaving the network and blocks any that do not match its rule set, for example traffic to a port that should not be in use".

**Match the defence exactly to the threat in the question.** If the scenario is staff being tricked by fake emails, the answer is training and awareness, not a firewall. A firewall does nothing against an employee who types their password into a convincing fake login page.

**Be precise about encryption.** Encryption does not prevent interception. It prevents intercepted data from being understood. Examiners specifically look for this.

**Give the strongest answer on human factors.** Every technical control can be undone by a person, which is why staff training is a genuine security control and not an afterthought.

+ Define every threat with its mechanism in one sentence
+ Pair each threat with the most appropriate prevention and say why
+ Explain why a network needs several layers of defence rather than one
+ Explain user access levels in terms of limiting damage, not just restricting access
""",
    mistakes=[
        "Saying encryption stops data being intercepted. It stops it being understood.",
        "Describing a firewall as 'antivirus'. A firewall filters network traffic, anti malware scans files.",
        "Saying a virus and a worm are the same. A worm needs no user action and no host file.",
        "Recommending a technical control against a social engineering attack. Training is the answer there.",
        "Saying penetration testing 'stops attacks'. It finds weaknesses so they can be fixed before attackers exploit them.",
        "Giving 'use a strong password' as the answer to everything. Match the control to the specific threat.",
    ],
    quiz=[
        Q("What is the key difference between a virus and a worm?",
          ["A worm spreads by itself across a network, a virus needs a host file and user action",
           "A virus spreads by itself, a worm needs a host file",
           "A worm only affects servers", "There is no difference"], 0,
          "Self replication without user involvement is what makes worms spread so quickly."),
        Q("A user receives an email claiming to be from their bank asking them to confirm their password. This is an example of:",
          ["Phishing", "A denial of service attack", "SQL injection", "A brute force attack"], 0,
          "Phishing imitates a trusted organisation to trick the victim into handing over information voluntarily."),
        Q("Which prevention method is most effective against a brute force attack?",
          ["Limiting the number of login attempts and using long strong passwords",
           "Installing a firewall", "Encrypting the hard disk", "Using a wired connection"], 0,
          "Brute force relies on making huge numbers of guesses. Locking the account after a few failures makes that impossible."),
        Q("What does encryption achieve?",
          ["Intercepted data cannot be understood without the key",
           "Data cannot be intercepted at all",
           "Malware cannot be installed",
           "Passwords can never be guessed"], 0,
          "Encryption does not prevent interception. It makes intercepted data meaningless to anyone without the decryption key."),
        Q("A website allows users to type into a search box which is passed straight into a database query. Which attack does this enable?",
          ["SQL injection", "Denial of service", "Shouldering", "A worm"], 0,
          "Unvalidated input passed into a query lets an attacker submit SQL code that the database will execute."),
        Q("What is the purpose of penetration testing?",
          ["To find weaknesses in a system before real attackers do",
           "To remove all malware from a network",
           "To encrypt data in transit",
           "To restrict which files a user can open"], 0,
          "It is a controlled simulated attack carried out with permission, producing a report of vulnerabilities to fix."),
        Q("How do user access levels improve security?",
          ["Users can only access what their role requires, limiting the damage from a compromised account",
           "They encrypt every file on the network",
           "They block all incoming network traffic",
           "They prevent phishing emails from arriving"], 0,
          "If an account is compromised, the attacker only inherits that account's limited permissions rather than full access."),
        Q("A DDoS attack differs from a DoS attack because:",
          ["It uses many compromised machines at once, making it harder to block",
           "It encrypts the victim's files",
           "It only targets wireless networks",
           "It requires physical access to the server"], 0,
          "Distributed attacks come from thousands of addresses simultaneously, so blocking a single source achieves nothing."),
        Q("Which measure best protects against staff being tricked into revealing passwords?",
          ["Regular staff training and awareness of social engineering",
           "A more powerful firewall",
           "Increasing the server's bandwidth",
           "Switching to fibre optic cable"], 0,
          "Social engineering attacks the person, not the technology, so the defence must also address the person."),
        Q("What does a firewall do?",
          ["Inspects incoming and outgoing traffic and blocks anything not meeting its rules",
           "Scans files for known malware signatures",
           "Encrypts data before transmission",
           "Backs up files automatically"], 0,
          "A firewall is a traffic filter. Scanning files is the job of anti malware software."),
    ],
    exam=[
        EQ("Describe what is meant by social engineering and give one example.", 3, [
            MP("Manipulating or tricking people rather than attacking the technology", ["people", "tricking", "manipulating", "human", "deceiving", "persuading"]),
            MP("The aim is to obtain confidential information or access", ["information", "passwords", "access", "details", "credentials"]),
            MP("Gives a valid example such as phishing, blagging or shouldering", ["phishing", "blagging", "shouldering", "pretexting", "shoulder surfing", "fake email", "phone call"]),
        ], "Social engineering is the practice of manipulating people rather than attacking a system's technology, in order to obtain confidential information such as passwords or to persuade someone to grant access they should not. It works because human trust and helpfulness can be exploited in ways that technical defences cannot prevent. One example is phishing, in which an attacker sends an email that appears to come from a legitimate organisation such as a bank, containing a link to a convincing fake login page, so that the victim enters their username and password and hands them directly to the attacker.",
           command="Describe"),
        EQ("Explain the difference between a computer virus and a worm.", 3, [
            MP("A virus attaches itself to a host file or program", ["attaches", "host file", "program", "file", "embeds"]),
            MP("A virus requires a user action such as opening the file in order to spread", ["user", "opening", "action", "run", "executed", "shared"]),
            MP("A worm replicates and spreads across a network on its own without user action", ["on its own", "no user", "automatically", "self replicating", "by itself", "network"]),
        ], "A virus is malware that attaches itself to a host file or program, and it only spreads when a user carries out an action such as opening that file, running the program or sharing it with somebody else. A worm, by contrast, is self replicating and spreads itself across a network without needing any user action or host file at all, which means it can move between machines far faster and infect a whole network in a very short time.",
           command="Explain"),
        EQ("A company's website has a login form. Explain how an SQL injection attack could be carried out against it and describe how the company could prevent this.", 4, [
            MP("The attacker enters SQL code into an input field instead of normal data", ["sql", "code", "input field", "text box", "types", "enters"]),
            MP("If the input is not checked it is passed into the database query and executed", ["not checked", "unvalidated", "passed into", "executed", "runs", "query"]),
            MP("This could allow the attacker to bypass the login or read, change or delete data", ["bypass", "access", "read", "delete", "change", "steal", "log in without"]),
            MP("Prevention: validate and sanitise all user input, or use parameterised queries", ["validation", "validate", "sanitise", "parameterised", "prepared statement", "check input", "whitelist"]),
        ], "An SQL injection attack is carried out by typing SQL code into an input field on the login form rather than a normal username or password. If the website builds its database query by inserting that text directly and does not check what has been entered, the attacker's code becomes part of the query and is executed by the database. For example, entering a fragment that makes the condition always evaluate to true could allow the attacker to log in as any user without knowing a password, and further injected statements could read, modify or delete the contents of the customer table. The company can prevent this by validating and sanitising all user input so that characters and keywords used in SQL are rejected or escaped, and more reliably by using parameterised queries, which keep the user's data strictly separate from the SQL code so that it can never be executed as an instruction.",
           command="Explain"),
        EQ("A school network has been affected by malware. Describe three measures the school could take to reduce the risk of this happening again.", 6, [
            MP("Install anti malware software", ["anti malware", "antivirus", "anti virus", "malware scanner"]),
            MP("Keep it updated so new threats are recognised", ["updated", "up to date", "new threats", "signatures", "latest"]),
            MP("Use a firewall to filter network traffic", ["firewall", "filter traffic", "block traffic"]),
            MP("Apply user access levels so students cannot install software", ["access levels", "permissions", "restrict", "cannot install", "rights"]),
            MP("Train staff and students to recognise suspicious emails and attachments", ["training", "educate", "awareness", "recognise", "suspicious", "not open"]),
            MP("Keep operating systems and applications patched", ["updates", "patches", "patched", "up to date", "security updates"]),
        ], "First, the school should install anti malware software on every machine and configure it to update automatically. Anti malware compares files against a database of known malware signatures and monitors for suspicious behaviour, quarantining anything it detects, but new malware appears constantly so the signature database must be kept current or recent threats will pass straight through. Second, the school should use a firewall between its network and the internet. A firewall inspects all incoming and outgoing traffic and blocks anything that does not meet its rules, which prevents malware from communicating with external servers and stops many infections reaching the network in the first place. Third, the school should set user access levels so that students and most staff cannot install software or alter system files. This means that even if a user is tricked into running something malicious, the malware inherits only that account's restricted permissions and cannot spread across the whole system. Alongside these, training staff and students to recognise suspicious emails and attachments addresses the human route that most infections actually take, and keeping operating systems and applications patched closes the software vulnerabilities that malware exploits.",
           command="Describe"),
        EQ("Explain why encryption is used when data is transmitted over a public wireless network.", 3, [
            MP("Data on a wireless network travels through the air and can be intercepted", ["intercepted", "through the air", "captured", "sniffed", "read", "eavesdrop"]),
            MP("Encryption scrambles the data using a key so it is unreadable", ["scrambles", "unreadable", "key", "cipher", "meaningless", "cannot be understood"]),
            MP("Without the key an attacker who intercepts the data cannot understand it", ["without the key", "cannot read", "useless", "cannot understand", "decrypt"]),
        ], "On a public wireless network the data travels through the air as radio waves, and anyone within range with the right software can capture that traffic without the sender being aware, which is known as packet sniffing. Encryption protects against this by scrambling the data using a key before it is transmitted, so that what is actually broadcast is meaningless. Encryption does not prevent the data from being intercepted, but an attacker who captures it has only unreadable ciphertext, and without the decryption key they cannot recover the original information such as passwords or bank details.",
           command="Explain"),
    ],
)

# ======================================================== 1.5 Systems software

T_SYSSOFT = Topic(
    slug="systems-software",
    title="Systems Software",
    spec="1.5",
    icon="i-software",
    minutes=28,
    blurb="What the operating system is really doing while you use a computer, all five of its management jobs, and every utility program on the specification.",
    fact="When a computer looks like it is running twenty programs at once, it usually is not. A single core switches between them thousands of times per second, giving each a tiny slice of time. The illusion is so convincing that we had to invent a word for it, multitasking.",
    sections=[
        Section("What system software is", """
Software divides into two categories.

- **System software** runs the computer itself: the operating system and utility programs.
- **Application software** lets the user do a task: a browser, a word processor, a game.

!key The distinguishing question :: Does the user run this to get a job done, or does the computer need it to function? Word processor is application. Disk defragmenter is system.
"""),
        Section("The operating system", """
The **operating system** manages the hardware and software of a computer and provides an environment in which applications can run. Without it, nothing else works.

It has five main jobs on this specification.

### 1. User interface

The operating system provides the way the user interacts with the machine.

- **Graphical user interface (GUI).** Windows, icons, menus and a pointer. Easy for beginners, and it requires more processing power and memory.
- **Command line interface (CLI).** The user types text commands. Uses very few resources and is far more powerful for experienced users, and it has a steep learning curve because commands must be memorised.

### 2. Memory management and multitasking

The operating system decides which programs and data are held in RAM and where.

- It allocates memory to each program and keeps them separate, so one program cannot overwrite another's data and crash it.
- It frees memory when a program closes.
- It manages **virtual memory** when RAM is full.

**Multitasking** is the appearance of several programs running at once. The operating system gives each process a small slice of CPU time and switches between them very rapidly, so quickly that the user perceives them as simultaneous.

### 3. Peripheral management and drivers

The operating system controls communication with input and output devices.

A **device driver** is software that translates operating system instructions into commands a specific piece of hardware understands. Each type of device needs its own driver, which is why plugging in a new printer often installs software.

### 4. User management

The operating system manages accounts.

- Creating and deleting user accounts
- Authenticating users with usernames and passwords
- Setting **access rights**, so each user reaches only what their role allows
- Keeping each user's files and settings separate

### 5. File management

The operating system organises files on secondary storage.

- Naming, saving, opening, moving, copying, renaming and deleting files
- Maintaining the folder structure
- Recording where each file is physically stored
- Managing access permissions on files

!exam A very common question :: "State three tasks of an operating system." Learn the five headings and you can always name three with confidence: user interface, memory management, peripheral management, user management, file management.
"""),
        Section("Utility software", """
**Utility software** performs maintenance tasks that keep a computer running well. It is system software, but it is separate from the operating system itself.

### Encryption software

Scrambles data using a key so it is unreadable without that key. Used for full disk encryption, protecting files and securing communication. If a laptop is stolen, encrypted data is useless to the thief.

### Defragmentation

Over time, files on a **magnetic hard disk** become **fragmented**: parts of the same file end up scattered across the disk because they were saved into whatever gaps were available.

The read write head then has to move to several different places to read one file, which is slow.

**Defragmentation** rearranges the data so that the parts of each file are stored together in contiguous blocks, and gathers the free space into one area. This reduces head movement and speeds up access.

!warn Do not defragment an SSD :: SSDs have no moving parts, so there is no head movement to save and no speed benefit. Worse, defragmentation writes data unnecessarily, and flash memory has a finite number of write cycles, so it shortens the drive's life. This point earns marks in comparison questions.

### Data compression

Reduces file sizes so that more can be stored and files transfer more quickly. Covered in detail in the compression topic.

### Backup

Creates copies of data so it can be restored after loss, corruption, hardware failure, ransomware or accidental deletion.

- **Full backup.** Copies every file. Slow to create and uses a lot of storage, but restoring is quick and simple because everything is in one place.
- **Incremental backup.** Copies only the files that have changed since the last backup of any type. Very fast to create and uses little storage, but restoring is slower because the last full backup and every incremental backup since must be applied in order.

!key Choosing a backup strategy :: A typical strategy is a full backup weekly with incremental backups daily, which balances the speed of creating backups against the time it takes to restore.
"""),
    ],
    keyterms=[
        ("System software", "Software that runs and maintains the computer itself, such as the operating system and utilities."),
        ("Operating system", "System software that manages hardware and software and provides an environment for applications to run."),
        ("GUI", "Graphical user interface. Interaction through windows, icons, menus and a pointer."),
        ("CLI", "Command line interface. Interaction by typing text commands."),
        ("Multitasking", "Rapidly switching the CPU between processes so several programs appear to run at once."),
        ("Device driver", "Software that translates operating system instructions into commands a specific hardware device understands."),
        ("Utility software", "Software that performs maintenance tasks such as backup, compression, encryption and defragmentation."),
        ("Fragmentation", "When parts of the same file are stored in separate locations on a disk, slowing access."),
        ("Defragmentation", "Reorganising data on a magnetic disk so files are stored in contiguous blocks."),
        ("Full backup", "A copy of every file, slow to create but quick to restore."),
        ("Incremental backup", "A copy of only the files changed since the last backup, quick to create but slower to restore."),
    ],
    grade="""
The examiner is looking for **the reason behind the task**, not just the task.

**Memory management** is not "it manages memory". It allocates memory to each program, keeps programs separate so one cannot overwrite another and cause a crash, and frees memory when programs close.

**Multitasking** is not "running several programs at once". The CPU switches between processes extremely rapidly, giving each a slice of time, so they appear to run simultaneously.

**Defragmentation** questions almost always include an SSD trap. Know that defragmenting an SSD gives no benefit and actively wastes write cycles.

**Backup comparison** is a favourite. The trade off is always the same shape: incremental is fast to create and slow to restore, full is slow to create and fast to restore.

+ Name all five operating system management jobs from memory
+ Explain multitasking in terms of time slicing, not just simultaneity
+ Explain fragmentation and defragmentation with reference to head movement
+ Compare full and incremental backup on both creation time and restore time
""",
    mistakes=[
        "Listing 'runs programs' as an operating system task without saying it manages memory and CPU time to do so.",
        "Saying a GUI is 'better' than a CLI. A CLI uses fewer resources and is more powerful for expert users.",
        "Recommending defragmentation for an SSD. It provides no benefit and consumes write cycles.",
        "Saying incremental backups are 'better' outright. They are faster to create but slower to restore.",
        "Confusing utility software with application software. A word processor is an application, a backup tool is a utility.",
    ],
    quiz=[
        Q("Which of these is an example of utility software?",
          ["A disk defragmenter", "A web browser", "A spreadsheet program", "A video game"], 0,
          "Utilities maintain the computer. The other three are applications the user runs to do a task."),
        Q("What does the operating system do during memory management?",
          ["Allocates memory to programs and keeps them separate so they cannot overwrite each other",
           "Increases the total amount of RAM installed",
           "Stores files permanently on the hard disk",
           "Converts programs into machine code"], 0,
          "Isolation is the key point. If one program could write into another's memory, it would crash it."),
        Q("How does an operating system make several programs appear to run at once on a single core?",
          ["It switches between processes very rapidly, giving each a small slice of CPU time",
           "It runs each program at a lower clock speed",
           "It runs them on the graphics card instead",
           "It compresses each program so they fit together"], 0,
          "This is time slicing. The switching is far faster than human perception, so it feels simultaneous."),
        Q("What is a device driver?",
          ["Software that translates operating system instructions into commands a hardware device understands",
           "A cable connecting a peripheral to the computer",
           "The person who installs new hardware",
           "A utility that defragments a disk"], 0,
          "Each type of hardware speaks its own language, and the driver is the translator between it and the operating system."),
        Q("Why does fragmentation slow down a magnetic hard disk?",
          ["The read write head must move to several locations to read one file",
           "The disk spins more slowly when fragmented",
           "Fragmented files take up more space",
           "The operating system has to decompress each fragment"], 0,
          "Physical head movement is the slow part of a hard disk. Scattered file parts multiply that movement."),
        Q("Why should an SSD not be defragmented?",
          ["There are no moving parts to benefit, and it wastes limited write cycles",
           "SSDs cannot store fragmented files",
           "It would delete the data",
           "SSDs defragment themselves every hour"], 0,
          "Access time is the same wherever data sits on an SSD, so there is no gain, and unnecessary writes shorten the drive's life."),
        Q("Which backup type is quickest to create but slowest to restore?",
          ["Incremental", "Full", "Differential to disk", "Mirror"], 0,
          "Incremental copies only what changed, so it is fast. Restoring needs the last full backup plus every incremental since, in order."),
        Q("What is one advantage of a command line interface over a graphical user interface?",
          ["It uses far fewer system resources", "It is easier for beginners to learn",
           "It shows previews of files", "It requires no typing"], 0,
          "A CLI needs very little memory and processing power, which is why servers and embedded systems often use one."),
        Q("Which is NOT a function of an operating system?",
          ["Editing a photograph", "Managing files and folders",
           "Managing user accounts", "Controlling peripherals"], 0,
          "Editing a photograph is what application software does. The other three are core operating system responsibilities."),
        Q("User access levels set by the operating system are used to:",
          ["Control which files and features each user can reach",
           "Speed up the processor for administrators",
           "Increase the amount of available RAM",
           "Encrypt every file automatically"], 0,
          "Access levels enforce that each account can only reach what its role requires, which limits both accidents and attacks."),
    ],
    exam=[
        EQ("State three tasks carried out by an operating system.", 3, [
            MP("Manages memory or provides multitasking", ["memory", "multitasking", "ram", "allocates memory", "processor management"]),
            MP("Manages peripherals and device drivers", ["peripheral", "drivers", "input", "output", "hardware", "devices"]),
            MP("Manages files, users or provides the user interface", ["file", "user management", "accounts", "user interface", "gui", "permissions"]),
        ], "An operating system manages memory, allocating it to programs and freeing it when they close as well as handling multitasking. It manages peripherals, using device drivers to communicate with input and output hardware. It also manages files and folders on secondary storage, and provides the user interface through which the user interacts with the computer.",
           command="State"),
        EQ("Explain how an operating system uses multitasking to allow several programs to run at the same time.", 3, [
            MP("Each program or process is given a small slice of CPU time", ["slice", "time", "share", "allocated", "turn"]),
            MP("The operating system switches rapidly between processes", ["switches", "rapidly", "quickly", "alternates", "scheduler"]),
            MP("The switching is so fast that the programs appear to run simultaneously", ["appear", "seems", "illusion", "simultaneously", "at the same time", "user does not notice"]),
        ], "The operating system allocates each running process a very small slice of processor time, and then switches the CPU rapidly from one process to the next according to a scheduling algorithm. Because each switch happens in a fraction of a second, far faster than a person can perceive, every program appears to be making continuous progress, giving the impression that they are all running at the same time even on a single core processor.",
           command="Explain"),
        EQ("Explain how defragmentation software improves the performance of a magnetic hard disk drive.", 4, [
            MP("Over time files become fragmented and stored in separate parts of the disk", ["fragmented", "split", "scattered", "different parts", "not together"]),
            MP("The read write head must move to several locations to read one file", ["read write head", "head", "move", "several locations", "seek"]),
            MP("Defragmentation rearranges the data so file parts are stored together", ["together", "contiguous", "next to", "rearranges", "one place", "adjacent"]),
            MP("Less head movement is required so files are accessed more quickly", ["less movement", "faster", "quicker access", "reduces", "speeds up"]),
        ], "As files are created, edited and deleted, gaps appear on the disk and new data is written wherever space is available, so parts of the same file end up stored in several separate locations, which is known as fragmentation. Because a magnetic hard disk reads data using a physical head on a moving arm, opening a fragmented file requires the head to move to each of those locations in turn, and this mechanical movement is by far the slowest part of the operation. Defragmentation software reorganises the contents of the disk so that all the parts of each file are placed together in contiguous blocks and the free space is gathered into one area. The head then only needs to move a short distance to read a whole file, so access times fall and the drive performs noticeably better.",
           command="Explain"),
        EQ("Compare a full backup and an incremental backup.", 4, [
            MP("A full backup copies every file", ["every file", "all files", "everything", "complete copy"]),
            MP("An incremental backup copies only files changed since the last backup", ["changed", "modified", "since the last", "only new"]),
            MP("Full backups take longer to create and use more storage", ["longer", "slower to create", "more storage", "more space", "time consuming"]),
            MP("Incremental backups are faster to create but slower to restore because multiple backups must be applied", ["faster to create", "quicker", "slower to restore", "multiple", "each one", "in order", "restore takes longer"]),
        ], "A full backup makes a complete copy of every file in the selected data, whereas an incremental backup copies only those files that have been created or changed since the previous backup of any kind. This produces opposite strengths. A full backup takes considerably longer to create and requires much more storage space, because the same unchanged files are copied every time, but restoring is fast and simple because everything needed is contained in a single backup set. An incremental backup is very quick to create and uses very little storage, but restoring is slower and more complex, because the most recent full backup must be restored first and then every incremental backup since must be applied in the correct order, and if any one of them is missing or corrupted the restore may fail.",
           command="Compare"),
        EQ("A company issues laptops to employees who work while travelling. Explain why encryption software should be installed on these laptops.", 3, [
            MP("Laptops carried outside the office are at higher risk of loss or theft", ["lost", "stolen", "theft", "travelling", "risk", "left behind"]),
            MP("Encryption scrambles the data using a key so it cannot be read without that key", ["scrambles", "key", "unreadable", "cannot be read", "cipher", "meaningless"]),
            MP("If the device is stolen, confidential company or customer data remains protected", ["confidential", "protected", "customer data", "cannot access", "useless", "gdpr", "data protection"]),
        ], "Laptops that leave the office are at a much higher risk of being lost or stolen, whether left on a train, taken from a hotel room or snatched in a public place. Encryption software protects against this by scrambling all the data on the drive using a key, so that the contents are meaningless to anyone who does not have that key, even if they remove the drive and connect it to another computer. This means that if a laptop is stolen the company loses the hardware but not the confidential business information or the personal data of its customers, which also helps the company meet its legal obligations under data protection law and avoid the penalties and reputational damage that follow a data breach.",
           command="Explain"),
    ],
)

# ================================================== 1.6 Ethical, legal, cultural

T_IMPACTS = Topic(
    slug="ethical-legal-cultural-environmental",
    title="Ethical, Legal, Cultural and Environmental Impacts",
    spec="1.6",
    icon="i-scales",
    minutes=32,
    blurb="The four impact categories, all four pieces of legislation you must name, open source against proprietary software, and how to structure the eight mark essay so it actually scores.",
    fact="A single large data centre can use as much electricity as a small town. This is why the biggest technology companies now build them next to hydroelectric dams or in the Arctic circle, where the outside air does the cooling for free.",
    sections=[
        Section("The four categories", """
Every impact question fits into one of four categories, and knowing which is which stops you writing the same point twice.

### Ethical

Questions of **right and wrong**, where there is no law forcing an answer.

- Should an employer read employees' emails?
- Is it acceptable for an algorithm to decide who gets a loan?
- Should facial recognition be used in public spaces?
- Is it right that technology jobs replace human ones?

### Legal

What the **law** requires or forbids. This is where the four named acts belong.

### Cultural

How technology changes **how groups of people live, work and interact**.

- The digital divide: those without reliable internet or devices are excluded from services that assume everyone has both
- Changes to how people socialise, shop, work and access news
- Online communities forming across national borders
- Concerns about screen time, misinformation and the effect on young people

### Environmental

The effect on the **planet**.

- Manufacturing devices consumes rare earth metals, and mining causes habitat destruction and pollution
- Data centres and devices consume enormous amounts of electricity
- **E-waste**: discarded electronics contain toxic substances such as lead and mercury, and much of it is shipped to countries with weak environmental controls
- Short replacement cycles worsen all of the above
- Positives: video conferencing reduces travel, smart systems cut energy use, digital documents reduce paper
"""),
        Section("Legislation", """
Four acts. You must know the name, the year and what it protects.

### Data Protection Act 2018

Controls how organisations use **personal data**. It incorporates GDPR into UK law.

Key principles: data must be used fairly and lawfully, collected for a specified purpose, adequate and not excessive, accurate and up to date, kept no longer than necessary, and kept secure.

Individuals have rights: to see the data held about them, to have errors corrected, and to have data erased in certain circumstances.

### Computer Misuse Act 1990

Created three offences, in increasing seriousness:

1. **Unauthorised access** to computer material, for example guessing a password to read someone's files
2. **Unauthorised access with intent to commit a further offence**, such as breaking in to commit fraud
3. **Unauthorised modification** of computer material, such as deleting files or spreading a virus

!warn This act covers hacking, not piracy :: Downloading a film illegally is copyright, not Computer Misuse. Guessing your friend's password is Computer Misuse even if you change nothing.

### Copyright, Designs and Patents Act 1988

Protects the **intellectual property** of creators: software, music, films, books, images and designs. It makes copying, distributing or using work without permission illegal.

This is the act that covers software piracy and illegal downloads.

### Software licences

**Open source software** is distributed with its source code, which anyone may view, modify and redistribute.

- Free to use in most cases
- Can be adapted to exact needs
- A large community may fix bugs and add features quickly
- Weaknesses are visible to everyone, including attackers
- Support is community based rather than guaranteed
- Examples: Linux, LibreOffice, Firefox, VLC

**Proprietary software** is distributed as a compiled program only. The source code is kept secret and the licence restricts what users may do.

- Usually paid for, sometimes by subscription
- Professional support and regular tested updates
- Cannot be modified or adapted by the user
- Users depend entirely on the vendor continuing to support it
- Examples: Microsoft Windows, Adobe Photoshop, Microsoft Office
"""),
        Section("Writing the eight mark answer", """
The impacts question is usually the longest on Paper 1 and it is marked by **levels**, not by counting points. That changes how you should write.

### What the levels reward

| Level | What it looks like |
| Level 1 | A few relevant points, mostly listed, little development |
| Level 2 | Several points developed with reasons, some balance |
| Level 3 | A balanced discussion of several impacts, developed with reasons, reaching a supported conclusion |

### A structure that reaches level 3

1. **Open with the context.** One sentence naming what is being introduced and who it affects.
2. **Two or three paragraphs, each on a different impact category.** Name the category, make the point, explain the consequence, and identify who is affected.
3. **Give both sides.** Every paragraph should acknowledge a counterpoint. A one sided answer is capped in the mark scheme.
4. **Conclude with a judgement.** Say what should happen and why, based on what you have argued.

!exam The single biggest mistake :: Writing eight separate points and stopping. Level 3 requires **development** and a **conclusion**. Four well developed points with a conclusion will beat eight bare assertions every time.

### Worked opening

*A supermarket replaces all its staffed checkouts with self service tills.*

"This change has significant ethical and cultural implications. Ethically, the supermarket has a responsibility towards the staff whose roles are removed, and while the company is not legally obliged to retain them, replacing long serving employees with machines purely to reduce costs raises questions of fairness, particularly where those employees have few alternative opportunities in the local area. Culturally, self service tills also disadvantage certain groups: elderly customers and those with visual impairments may find touchscreens difficult, and for some isolated customers the brief interaction at a checkout is genuine social contact. Against this, self service reduces queueing for the majority and lowers costs, which may keep prices down for all customers..."

Notice: category named, point made, consequence explained, group affected identified, counterpoint given.
"""),
    ],
    keyterms=[
        ("Ethical issue", "A question of right and wrong where no law dictates the answer."),
        ("Legal issue", "Something governed by law, such as the use of personal data or unauthorised access."),
        ("Cultural issue", "The effect of technology on how groups of people live, work and interact."),
        ("Environmental issue", "The effect of technology on the natural world, including energy use and e-waste."),
        ("Data Protection Act 2018", "Legislation controlling how organisations collect, store and use personal data."),
        ("Computer Misuse Act 1990", "Legislation making unauthorised access to and modification of computer material a criminal offence."),
        ("Copyright, Designs and Patents Act 1988", "Legislation protecting the intellectual property of creators, including software."),
        ("Open source software", "Software distributed with its source code, which anyone may view, modify and redistribute."),
        ("Proprietary software", "Software distributed without source code, under a licence restricting how it may be used."),
        ("Digital divide", "The gap between those with reliable access to technology and the internet and those without."),
        ("E-waste", "Discarded electronic equipment, often containing toxic materials, much of it exported to developing countries."),
    ],
    grade="""
This topic separates students more than any other on Paper 1, because it is marked by levels.

**Never write a list.** Lists reach level 1. Each point needs: the claim, the reason, the consequence and who is affected.

**Always give both sides.** A one sided answer cannot reach the top level even if every point is correct. Use phrases like "however", "on the other hand" and "against this".

**Name the specific group affected.** Not "people" but "elderly customers", "employees in low skilled roles", "students in households without broadband", "communities near mining sites". Specificity is what makes an answer feel expert.

**Always conclude.** One or two sentences giving your judgement and the reason for it. Answers without a conclusion routinely lose the top mark even when the discussion was strong.

**Learn the four acts precisely.** The name and year are worth a mark on their own, and using the wrong act for a scenario loses marks that are otherwise free.

+ Write an eight mark answer in 12 minutes with four developed points and a conclusion
+ Match any given scenario to the correct legislation instantly
+ Give three advantages and three disadvantages of open source
+ Name a specific affected group in every paragraph you write
""",
    mistakes=[
        "Writing a list of impacts with no development or conclusion, which caps the answer at level 1.",
        "Confusing the Computer Misuse Act with the Copyright Act. Hacking is Misuse, piracy is Copyright.",
        "Saying open source is 'free' as if that is the only difference. The defining feature is that the source code is available to view and modify.",
        "Giving only negative environmental impacts. Video conferencing, digital documents and smart energy systems are genuine positives.",
        "Writing only about one category when the question says impacts, plural.",
        "Saying 'it affects people' rather than naming the specific group affected.",
    ],
    quiz=[
        Q("Which act makes it illegal to access a computer system without permission?",
          ["Computer Misuse Act 1990", "Data Protection Act 2018",
           "Copyright, Designs and Patents Act 1988", "Freedom of Information Act 2000"], 0,
          "The Computer Misuse Act created the offence of unauthorised access, even where nothing is changed or stolen."),
        Q("A student illegally downloads a film. Which law has been broken?",
          ["Copyright, Designs and Patents Act 1988", "Computer Misuse Act 1990",
           "Data Protection Act 2018", "No law has been broken"], 0,
          "Copyright protects the creator's intellectual property, and copying or distributing without permission infringes it."),
        Q("Which is a defining feature of open source software?",
          ["The source code is available for anyone to view and modify",
           "It can never be sold", "It has no bugs", "It only runs on Linux"], 0,
          "Availability of source code is the definition. Many open source projects are commercially supported."),
        Q("The digital divide refers to:",
          ["The gap between those with reliable access to technology and those without",
           "The difference between analogue and digital signals",
           "The split between hardware and software companies",
           "The gap between open source and proprietary software"], 0,
          "It matters because services increasingly assume everyone has a device and a connection, which excludes those who do not."),
        Q("Which is an environmental impact of computing?",
          ["E-waste containing toxic materials being exported to developing countries",
           "Employees having their emails monitored",
           "Software being copied without permission",
           "Users being unable to modify proprietary software"], 0,
          "The others are ethical, legal and licensing issues respectively."),
        Q("Under the Data Protection Act 2018, an individual has the right to:",
          ["See the personal data an organisation holds about them",
           "Copy any software they have purchased",
           "Access any computer system they choose",
           "Demand free internet access"], 0,
          "Subject access is a core right, alongside the right to correction and, in some circumstances, erasure."),
        Q("Which is a disadvantage of proprietary software?",
          ["It cannot be modified because the source code is not available",
           "It never receives updates",
           "It always contains malware",
           "It cannot be used commercially"], 0,
          "Users depend entirely on the vendor for changes, fixes and continued support."),
        Q("An employer secretly reads staff private messages. This is primarily:",
          ["An ethical issue about privacy and trust",
           "An environmental issue",
           "A cultural issue about the digital divide",
           "Not an issue of any kind"], 0,
          "It is a question of what is right rather than only what is legal, which places it in the ethical category."),
        Q("Which is an advantage of open source software for a school with a limited budget?",
          ["It is usually free to use and can be installed on any number of machines",
           "It comes with a guaranteed support contract",
           "It is always easier to use than proprietary software",
           "It automatically updates all hardware drivers"], 0,
          "No per machine licence cost is a substantial saving when deploying to hundreds of computers."),
        Q("Which statement about e-waste is correct?",
          ["It often contains toxic substances and is frequently exported to countries with weaker regulations",
           "It is always safely recycled in the country where it is used",
           "It contains no valuable materials",
           "It is not considered an environmental problem"], 0,
          "Lead, mercury and cadmium are common in electronics, and informal recycling exposes workers and contaminates land and water."),
    ],
    exam=[
        EQ("State the name of the legislation that protects the personal data an organisation holds about individuals.", 1, [
            MP("Data Protection Act 2018", ["data protection act", "data protection", "gdpr"]),
        ], "The Data Protection Act 2018, which brings the General Data Protection Regulation into UK law.",
           command="State"),
        EQ("Describe two offences created by the Computer Misuse Act 1990.", 4, [
            MP("Unauthorised access to computer material", ["unauthorised access", "without permission", "gaining access", "hacking"]),
            MP("Example or explanation of unauthorised access, such as using someone else's password", ["password", "someone else", "log in", "account", "files"]),
            MP("Unauthorised modification of computer material", ["modification", "modify", "change", "delete", "altering", "virus"]),
            MP("Unauthorised access with intent to commit a further offence such as fraud", ["intent", "further offence", "fraud", "commit a crime", "in order to"]),
        ], "The first offence is unauthorised access to computer material, which means gaining access to a computer system or the data on it without permission, for example by guessing or stealing another person's password in order to read their files. This is an offence even if nothing is altered or taken. The second offence is unauthorised modification of computer material, which covers changing or deleting data without permission, including deliberately spreading a virus or ransomware that alters files. The Act also creates the more serious offence of unauthorised access with intent to commit a further offence, such as breaking into a system in order to commit fraud.",
           command="Describe"),
        EQ("Explain two advantages of using open source software rather than proprietary software.", 4, [
            MP("It is usually free of charge, reducing costs", ["free", "no cost", "cheaper", "no licence fee", "saves money"]),
            MP("The source code can be viewed and modified to suit specific needs", ["source code", "modify", "adapt", "customise", "change it", "tailor"]),
            MP("A community of developers can fix bugs and add features", ["community", "developers", "bugs fixed", "improvements", "anyone can contribute"]),
            MP("There is no dependence on a single vendor continuing to support the software", ["vendor", "not dependent", "company", "discontinued", "lock in", "supported"]),
        ], "The first advantage is cost. Open source software is normally free to download and use with no per machine licence fee, which for an organisation deploying software to hundreds of computers represents a very large saving compared with proprietary licences that must be bought and often renewed annually. The second advantage is that the source code is made available, so the software can be examined and modified. This means an organisation can adapt the program to its own specific requirements rather than working around limitations, and a global community of developers can inspect the code, identify security weaknesses and contribute fixes and new features, often far more quickly than a single company could.",
           command="Explain"),
        EQ("A local council is planning to move all of its services online, so that residents must use a website to report problems, pay bills and apply for support. Discuss the impacts of this decision.", 8, [
            MP("Identifies a cultural impact such as the digital divide", ["digital divide", "access", "internet", "cultural", "excluded"]),
            MP("Names a specific affected group such as elderly residents or low income households", ["elderly", "older", "low income", "poorer", "disabled", "rural", "no internet"]),
            MP("Identifies an ethical impact, such as fairness of removing non digital options", ["ethical", "fair", "unfair", "right", "responsibility", "obligation"]),
            MP("Identifies a legal impact, such as Data Protection Act obligations for personal data", ["data protection", "legal", "gdpr", "personal data", "law", "secure"]),
            MP("Identifies an environmental impact such as reduced paper and travel, or increased server energy use", ["environmental", "paper", "travel", "energy", "carbon", "servers", "emissions"]),
            MP("Gives benefits such as lower costs, 24 hour availability and faster service", ["cheaper", "cost", "24 hours", "any time", "faster", "convenient", "efficient"]),
            MP("Presents both sides rather than only advantages or only disadvantages", ["however", "on the other hand", "although", "but", "balance", "against this"]),
            MP("Reaches a supported conclusion with a recommendation", ["conclusion", "overall", "therefore", "should", "recommend", "in my opinion"]),
        ], "Moving all council services online has substantial impacts across several areas. Culturally, the most serious is the digital divide. Not every resident has a reliable internet connection, a suitable device or the confidence to use one, and the groups most likely to be excluded are elderly residents, people on low incomes and those in rural areas with poor broadband. These are also, in many cases, precisely the residents who most need council support, so a digital only service risks making it hardest to reach for the people who depend on it most. Ethically, this raises a genuine question of fairness. The council has a duty to serve all of its residents equally, and while moving online is not unlawful, removing every alternative route to a service effectively withdraws it from a minority of the population who have done nothing wrong. Legally, the council will be handling large volumes of personal data including addresses, financial details and information about vulnerable people, so it is bound by the Data Protection Act 2018 to collect only what is necessary, keep it accurate, store it securely and retain it no longer than needed. A breach would expose residents to fraud and expose the council to significant fines. Environmentally the picture is mixed. Online services remove a great deal of printing, postage and travel to council offices, which reduces paper use and vehicle emissions, but the servers hosting the service consume electricity continuously and the devices residents need in order to use it carry their own manufacturing and disposal costs. There are clear benefits driving the decision. Online services are far cheaper to run than staffed offices, they are available at any hour rather than only during working hours, and requests can be tracked and processed more quickly, which improves the experience for the majority of residents and frees money for other services. Overall, the council is right to move services online, but wrong to make it the only option. The most defensible approach is to develop the digital service fully while retaining a telephone line and a staffed counter for those who cannot use it, and to fund community support to help residents get online. This captures most of the cost savings and convenience without excluding the residents least able to adapt.",
           command="Discuss"),
        EQ("Explain one environmental benefit and one environmental drawback of increased use of video conferencing by businesses.", 4, [
            MP("Benefit: less travel to meetings", ["travel", "flights", "driving", "commute", "journeys"]),
            MP("Which reduces fuel use and carbon emissions", ["emissions", "carbon", "fuel", "pollution", "co2", "greenhouse"]),
            MP("Drawback: servers and networks consume electricity continuously", ["servers", "electricity", "energy", "data centres", "power"]),
            MP("Devices must be manufactured and eventually disposed of, using resources and creating e-waste", ["manufacture", "e-waste", "disposal", "resources", "rare earth", "mining", "devices"]),
        ], "The environmental benefit is a reduction in travel. Meetings that previously required employees to drive across the country or fly abroad can be held from a desk, which cuts fuel consumption and the carbon emissions associated with road and air travel, and also reduces the demand for large office buildings that must be heated and lit. The drawback is that video conferencing is not free of environmental cost. The data centres that host the service run continuously and consume very large amounts of electricity, both for the servers themselves and for the cooling systems that keep them at a safe temperature, and video is one of the most data intensive services on the internet. In addition, every participant needs a device with a camera and a reliable connection, and manufacturing those devices consumes rare earth metals extracted through environmentally damaging mining, while their eventual disposal adds to the growing volume of electronic waste.",
           command="Explain"),
    ],
)
