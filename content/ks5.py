"""OCR A Level Computer Science H446 revision content.

Covers Component 01 (Computer Systems), Component 02 (Algorithms and
Programming) and guidance for Component 03/04, the programming project.
"""
from mskbuild.models import Topic, Section, Unit, Course, Q, EQ, MP

# ============================================== 1.1.1 Structure of the processor

A_PROCESSOR = Topic(
    slug="structure-and-function-of-the-processor",
    title="Structure and Function of the Processor",
    spec="1.1.1",
    icon="i-cpu",
    minutes=40,
    blurb="The full fetch decode execute cycle with every register and bus, pipelining, and the architectures you must be able to compare at A Level depth.",
    fact="Pipelining is why a modern processor completes roughly one instruction per cycle despite each instruction taking several cycles to finish. It is the same idea as a production line: nobody waits for the first car to be finished before starting the second.",
    sections=[
        Section("Components and registers", """
### The core components

| Component | Function |
| **ALU** | Performs all arithmetic and logical operations, and the shifts used in multiplication and division |
| **Control Unit** | Decodes instructions, generates control signals, synchronises components to the clock and directs data flow |
| **Registers** | Extremely fast storage inside the processor holding values currently in use |
| **Cache** | Small, very fast memory holding recently and frequently accessed instructions and data |
| **Clock** | Generates the regular pulse that synchronises all operations |

### The registers you must know

| Register | Contents |
| **PC** Program Counter | Address of the next instruction to be fetched |
| **MAR** Memory Address Register | The address currently being read from or written to |
| **MDR** Memory Data Register | The data or instruction transferred to or from memory |
| **CIR** Current Instruction Register | The instruction currently being decoded and executed |
| **ACC** Accumulator | The result of ALU operations |
| **Status register** | Flags such as zero, negative, carry and overflow set by the last operation |

!key A Level goes beyond GCSE by adding the CIR :: At GCSE the instruction sits in the MDR. At A Level it is copied from the MDR into the CIR so that the MDR is free for the data the instruction needs.

### Buses

- **Address bus.** Unidirectional, carrying memory addresses from the processor. Its **width determines the maximum addressable memory**: an n bit address bus can address 2^n^ locations.
- **Data bus.** Bidirectional, carrying data and instructions. Its **width determines how much data moves per transfer**, so a wider data bus increases throughput.
- **Control bus.** Bidirectional, carrying control signals such as read, write, clock, interrupt request and bus request.

A 32 bit address bus can address 2^32^ locations, which is about 4 GB. This is precisely why 32 bit systems could not use more than 4 GB of RAM.
"""),
        Section("The fetch decode execute cycle in full", """
### Fetch

1. The address in the **PC** is copied into the **MAR**.
2. The **PC is incremented**.
3. The address in the MAR is placed on the **address bus** and a read signal is sent on the **control bus**.
4. The instruction at that address is returned on the **data bus** into the **MDR**.
5. The instruction is copied from the **MDR into the CIR**.

### Decode

6. The **Control Unit** splits the instruction in the CIR into its **opcode** and **operand**.
7. The opcode identifies the operation. The operand is the data or the address of the data.
8. Control signals are generated for the units that will carry it out.

### Execute

9. The instruction is carried out: an ALU operation with the result in the **accumulator**, a transfer to or from memory, or a change to the PC in the case of a jump.
10. The **status register flags** are updated.

The cycle then repeats.

### Interrupts

An **interrupt** is a signal from a device or program requesting the processor's attention.

At the **end of each cycle** the processor checks the interrupt register. If an interrupt of higher priority than the current task is present:

1. The contents of the registers are copied to a **stack**, saving the current state
2. The relevant **interrupt service routine** is loaded and executed
3. When it completes, the previous state is **popped from the stack** back into the registers
4. Execution resumes exactly where it left off

Because a stack is used, interrupts can nest, so a higher priority interrupt can interrupt an interrupt service routine.

!exam Interrupts are examined every year :: Learn the sequence, including that the check happens at the end of a cycle and that the stack is what makes nesting possible.
"""),
        Section("Performance and architectures", """
### Factors affecting performance

| Factor | Effect |
| **Clock speed** | More cycles per second means more instructions per second, but heat and power rise sharply |
| **Number of cores** | Genuine parallel execution, limited by whether software is multi threaded and by Amdahl's law |
| **Cache size and levels** | Higher hit rate means fewer slow accesses to main memory |
| **Word length** | Longer words mean more data processed per operation |
| **Bus width** | A wider data bus increases throughput, a wider address bus increases addressable memory |

### Pipelining

Instructions are broken into stages, and while one instruction is being executed the next is being decoded and a third is being fetched.

    Cycle 1:  Fetch A
    Cycle 2:  Fetch B   Decode A
    Cycle 3:  Fetch C   Decode B   Execute A
    Cycle 4:  Fetch D   Decode C   Execute B

Throughput rises to roughly one instruction per cycle even though each instruction still takes three cycles.

**The problem is branching.** When a conditional jump is taken, the instructions already in the pipeline are wrong and must be discarded, which is a **pipeline flush**. Processors use **branch prediction** to guess which way a branch will go and reduce this cost.

### Von Neumann against Harvard

| | Von Neumann | Harvard |
| Memory | One shared memory for instructions and data | Separate memories, and separate buses |
| Buses | One set, shared | Two sets, one for each memory |
| Speed | Slower, because instructions and data compete for the same bus, the von Neumann bottleneck | Faster, since an instruction and data can be fetched simultaneously |
| Cost and complexity | Cheaper and simpler | More expensive and more complex |
| Typical use | General purpose computers | Embedded systems and digital signal processors |

Many real processors are **hybrid**: von Neumann in main memory, Harvard at the cache level with separate instruction and data caches.

### RISC against CISC

| | RISC | CISC |
| Instruction set | Small, simple instructions | Large, complex instructions |
| Instruction length | Fixed | Variable |
| Cycles per instruction | Usually one | Several |
| Instructions per task | More | Fewer |
| Pipelining | Straightforward, because instructions are uniform | Difficult, because instruction lengths vary |
| Complexity | In the compiler and the software | In the hardware |
| Power use | Lower | Higher |
| Examples | ARM | x86 |

The trade off is where the complexity sits. RISC pushes it into the compiler, CISC builds it into the hardware. RISC dominates mobile devices because of its power efficiency and its suitability for pipelining.

### Co-processors and parallel systems

- A **GPU** has thousands of simple cores optimised for performing the same operation on large amounts of data at once, which suits graphics, machine learning and scientific simulation.
- **Multicore** systems run genuinely parallel threads.
- **Parallel processing** speeds up work only to the extent that the task can be divided. **Amdahl's law** states that the maximum speedup is limited by the fraction of the task that must remain sequential.
"""),
    ],
    keyterms=[
        ("ALU", "Arithmetic Logic Unit, performing all arithmetic and logical operations."),
        ("Control Unit", "The component that decodes instructions and generates control signals to coordinate the processor."),
        ("CIR", "Current Instruction Register, holding the instruction currently being decoded and executed."),
        ("Status register", "A register holding flags such as zero, carry, negative and overflow set by the last operation."),
        ("Opcode", "The part of an instruction identifying which operation to perform."),
        ("Operand", "The part of an instruction giving the data or the address of the data to operate on."),
        ("Interrupt", "A signal requesting the processor's attention, checked at the end of each cycle."),
        ("Interrupt service routine", "The code executed in response to a particular interrupt."),
        ("Pipelining", "Overlapping the fetch, decode and execute stages of consecutive instructions to increase throughput."),
        ("Pipeline flush", "Discarding instructions already in the pipeline after a branch is taken."),
        ("Von Neumann bottleneck", "The limit imposed by instructions and data sharing a single bus and memory."),
        ("Harvard architecture", "An architecture with separate memories and buses for instructions and data."),
        ("RISC", "Reduced Instruction Set Computer, using a small set of simple, uniform instructions."),
        ("CISC", "Complex Instruction Set Computer, using a large set of powerful, variable length instructions."),
        ("Amdahl's law", "The principle that speedup from parallelism is limited by the sequential fraction of a task."),
    ],
    grade="""
A Level answers on this topic must go beyond the GCSE version in three specific ways.

**Include the CIR and the status register.** A cycle description that stops at MDR is a GCSE answer. The instruction moves MDR to CIR, and the flags update on execute.

**Explain the mechanism of the interrupt, including the stack.** Registers are pushed to a stack, the ISR runs, the registers are popped back. The stack is what permits nesting, and saying so shows genuine understanding.

**Quantify where you can.** An n bit address bus addresses 2^n^ locations. A 32 bit bus therefore reaches 4 GB, which explains a real historical limitation.

**On comparisons, give the underlying cause.** RISC pipelines well *because* its instructions are fixed length and take a uniform number of cycles. Harvard is faster *because* an instruction and its data can be fetched simultaneously rather than competing for one bus.

+ Write the full ten step cycle from memory, naming every register and bus
+ Describe the interrupt sequence including the stack and nesting
+ Explain pipelining, the branching problem and branch prediction
+ Compare RISC and CISC and Harvard and von Neumann with causes, not just properties
""",
    mistakes=[
        "Giving the GCSE five step cycle at A Level, with no CIR and no status register.",
        "Saying interrupts are checked continuously. They are checked at the end of each cycle.",
        "Omitting the stack from an interrupt answer, which loses the explanation of nesting.",
        "Saying RISC is 'simpler so faster'. It executes more instructions per task but pipelines far better.",
        "Confusing the address bus and data bus roles when explaining addressable memory.",
    ],
    quiz=[
        Q("Which register holds the instruction currently being decoded?",
          ["CIR", "MDR", "MAR", "PC"], 0,
          "The instruction is copied from the MDR into the CIR so the MDR is free for the data the instruction needs."),
        Q("A processor has a 36 bit address bus. How many memory locations can it address?",
          ["2 to the power 36", "36", "36 squared", "2 times 36"], 0,
          "Each additional address line doubles the addressable space, so n lines give 2 to the power n locations."),
        Q("When are interrupts checked?",
          ["At the end of each fetch decode execute cycle", "Continuously in hardware",
           "Only when the processor is idle", "At the start of the fetch stage"], 0,
          "Checking at a cycle boundary means the processor is always in a consistent state when it switches."),
        Q("What is stored on the stack when an interrupt occurs?",
          ["The contents of the registers, saving the current state",
           "The interrupt service routine", "The next instruction only", "The contents of cache"], 0,
          "Using a stack is what allows interrupts to nest, since each saved state is restored in reverse order."),
        Q("What is a pipeline flush?",
          ["Discarding partly processed instructions after a branch is taken",
           "Clearing the cache", "Resetting the program counter", "Emptying the interrupt queue"], 0,
          "The instructions already fetched follow the wrong path, so they must be thrown away."),
        Q("What is the von Neumann bottleneck?",
          ["Instructions and data compete for the same bus and memory",
           "The processor cannot address enough memory",
           "Cache is too small", "Too many cores share one clock"], 0,
          "Harvard architecture removes it by giving instructions and data separate memories and buses."),
        Q("Which is characteristic of RISC?",
          ["Fixed length instructions that usually execute in one cycle",
           "A large set of complex variable length instructions",
           "Complexity built into the hardware",
           "Fewer instructions needed per task"], 0,
          "Uniform instructions are what make RISC so well suited to pipelining."),
        Q("Why is a GPU well suited to machine learning?",
          ["It has many simple cores performing the same operation on large amounts of data",
           "It has a much higher clock speed than a CPU",
           "It has a larger instruction set",
           "It requires no memory"], 0,
          "Training involves the same arithmetic applied across huge matrices, which parallelises almost perfectly."),
        Q("What does Amdahl's law state?",
          ["Speedup from parallelism is limited by the sequential fraction of the task",
           "Transistor counts double every two years",
           "Cache hit rate determines performance",
           "Clock speed doubles with each generation"], 0,
          "If ten per cent of a task must be sequential, no amount of parallelism can exceed a tenfold speedup."),
        Q("Which flag in the status register indicates a result of zero?",
          ["The zero flag", "The carry flag", "The negative flag", "The overflow flag"], 0,
          "Flags are set by the last ALU operation and are used by conditional branch instructions."),
    ],
    exam=[
        EQ("Describe the fetch stage of the fetch decode execute cycle, referring to the registers and buses involved.", 5, [
            MP("The address in the Program Counter is copied to the MAR", ["program counter", "pc", "mar", "copied"]),
            MP("The Program Counter is incremented", ["incremented", "increased", "plus one", "next instruction"]),
            MP("The address is placed on the address bus", ["address bus", "placed on", "sent"]),
            MP("A read signal is sent on the control bus", ["control bus", "read signal", "read"]),
            MP("The instruction returns on the data bus into the MDR and is then copied to the CIR", ["data bus", "mdr", "cir", "copied to"]),
        ], "The address of the next instruction, held in the Program Counter, is copied into the Memory Address Register, and the Program Counter is then incremented so that it points at the following instruction. The address held in the MAR is placed on the address bus and a read signal is asserted on the control bus. Main memory responds by placing the contents of that location onto the data bus, from where it is loaded into the Memory Data Register. The instruction is then copied from the MDR into the Current Instruction Register, leaving the MDR free for any data the instruction subsequently requires.",
           command="Describe"),
        EQ("Explain how a processor handles an interrupt.", 5, [
            MP("Interrupts are checked at the end of each fetch decode execute cycle", ["end of", "each cycle", "after", "checked"]),
            MP("The priority of the interrupt is compared with that of the current task", ["priority", "higher", "compared", "more important"]),
            MP("The contents of the registers are pushed onto a stack to save the current state", ["stack", "pushed", "saved", "registers", "state"]),
            MP("The relevant interrupt service routine is loaded and executed", ["interrupt service routine", "isr", "loaded", "executed"]),
            MP("Afterwards the saved state is popped back and execution resumes where it left off", ["popped", "restored", "resumes", "returns", "continues"]),
        ], "At the end of each fetch decode execute cycle the processor checks the interrupt register to see whether any interrupt has been raised. If one has, its priority is compared with that of the task currently executing, and if it is lower the interrupt is left pending. If it is higher, the processor saves its current state by pushing the contents of all its registers, including the Program Counter, onto a stack. The address of the appropriate interrupt service routine is then loaded into the Program Counter and that routine is executed. When it finishes, the saved register contents are popped from the stack and restored, so the interrupted program continues from exactly the point where it was suspended. Because a stack is used, an interrupt service routine can itself be interrupted by a higher priority interrupt and each state is restored in the correct reverse order.",
           command="Explain"),
        EQ("Explain how pipelining improves processor performance and describe one situation in which its benefit is reduced.", 5, [
            MP("Instructions are divided into stages such as fetch, decode and execute", ["stages", "fetch decode execute", "divided", "split"]),
            MP("Different instructions occupy different stages at the same time", ["at the same time", "simultaneously", "overlap", "while", "concurrent"]),
            MP("Throughput approaches one instruction completed per cycle", ["one per cycle", "throughput", "more instructions", "each cycle"]),
            MP("A conditional branch may mean the instructions already fetched are the wrong ones", ["branch", "jump", "wrong instructions", "conditional"]),
            MP("The pipeline must then be flushed, wasting the work already done", ["flush", "flushed", "discarded", "wasted", "cleared"]),
        ], "Pipelining divides instruction processing into separate stages, typically fetch, decode and execute, and allows different instructions to occupy different stages at the same time. While one instruction is being executed, the next is being decoded and a third is being fetched, so although each individual instruction still takes three cycles to complete, one instruction finishes on every cycle once the pipeline is full, which raises throughput substantially without any increase in clock speed. The benefit is reduced when a conditional branch is encountered. The processor has already fetched and begun decoding the instructions that follow sequentially, but if the branch is taken those are not the instructions that should execute next. The pipeline must therefore be flushed and refilled from the branch target, discarding several cycles of completed work. Processors mitigate this using branch prediction, which guesses the likely outcome based on previous behaviour and speculatively fills the pipeline accordingly.",
           command="Explain"),
        EQ("Compare the von Neumann and Harvard architectures.", 6, [
            MP("Von Neumann uses a single memory for both instructions and data", ["single memory", "shared", "same memory", "one memory"]),
            MP("Harvard uses separate memories for instructions and data", ["separate", "two memories", "different memories"]),
            MP("Von Neumann uses one set of buses, Harvard uses separate buses for each memory", ["one set", "shared bus", "separate buses", "two sets"]),
            MP("Harvard can fetch an instruction and data simultaneously, so it is faster", ["simultaneously", "at the same time", "faster", "parallel"]),
            MP("Von Neumann suffers from the bottleneck of instructions and data competing for one bus", ["bottleneck", "compete", "contention", "shared"]),
            MP("Von Neumann is cheaper and simpler, Harvard is used in embedded and DSP systems", ["cheaper", "simpler", "embedded", "dsp", "specialised", "more expensive"]),
        ], "The von Neumann architecture stores both instructions and data in a single shared memory, accessed through one set of address, data and control buses. The Harvard architecture uses physically separate memories for instructions and for data, each with its own set of buses. This leads directly to the key performance difference: in a Harvard system an instruction can be fetched at the same time as data is read or written, whereas in a von Neumann system both must use the same bus and therefore compete, producing what is known as the von Neumann bottleneck. The compensating advantages of von Neumann are cost and flexibility. Only one memory and one bus set are needed, which makes the hardware cheaper and simpler, and because instructions and data occupy the same memory the division between them can be varied freely, which suits general purpose computers running unpredictable workloads. Harvard architecture is more expensive and less flexible, since the split between instruction and data memory is fixed by the hardware, so it is used chiefly in embedded systems and digital signal processors where the program is fixed and predictable performance matters more. Many modern processors are hybrid, presenting a von Neumann model at the level of main memory while using separate instruction and data caches internally to gain the Harvard speed advantage.",
           command="Compare"),
        EQ("Explain how the width of the address bus and the width of the data bus each affect the performance and capability of a processor.", 4, [
            MP("The address bus width determines how many memory locations can be addressed", ["address bus", "locations", "addressable", "how much memory"]),
            MP("An n bit address bus can address 2 to the power n locations", ["2 to the power", "2^n", "doubles", "32 bit gives 4gb"]),
            MP("The data bus width determines how much data is transferred in one operation", ["data bus", "how much data", "per transfer", "at once"]),
            MP("A wider data bus increases throughput, so fewer transfers are needed for the same data", ["throughput", "fewer transfers", "faster", "more data at once"]),
        ], "The width of the address bus determines the size of the address space, because each line carries one bit of the address. An n bit address bus can therefore specify 2 to the power n distinct locations, which is why a 32 bit address bus limits a system to approximately 4 GB of addressable memory and why moving to 64 bit addressing was necessary. The width of the data bus determines how many bits are transferred between the processor and memory in a single operation. A 64 bit data bus moves eight bytes per transfer where a 32 bit bus moves four, so for the same volume of data half as many transfers are required, which directly increases throughput and reduces the time the processor spends waiting for memory.",
           command="Explain"),
    ],
)

# ================================================= 1.1.2 Types of processor

A_PROCTYPES = Topic(
    slug="types-of-processor",
    title="Types of Processor",
    spec="1.1.2",
    icon="i-gauge",
    minutes=20,
    blurb="RISC against CISC in the depth the specification demands, GPUs, multicore and parallel systems, and how to compare them in an exam.",
    fact="The ARM architecture that powers almost every phone was designed by a small team in Cambridge in the 1980s. Its low power consumption was originally an accident of the design, not a goal, and it turned out to be the single most valuable property a processor could have.",
    sections=[
        Section("RISC and CISC", """
The central question is **where the complexity sits**: in the hardware, or in the compiler.

### CISC, Complex Instruction Set Computer

- A **large instruction set** with powerful, specialised instructions
- Instructions are of **variable length** and take **varying numbers of cycles**
- One instruction may perform what would otherwise take several
- Complexity is built into the **hardware**, often using **microcode** to break complex instructions into internal steps
- Fewer instructions are needed per task, so programs are shorter, which mattered enormously when memory was scarce
- Harder to pipeline, since instruction lengths and durations vary
- Example: the x86 family in desktop and laptop computers

### RISC, Reduced Instruction Set Computer

- A **small instruction set** of simple operations
- Instructions are of **fixed length** and typically execute in **one cycle**
- More instructions are needed per task, so programs are longer
- Complexity is moved into the **compiler**, which must build complex operations from simple ones
- Pipelines extremely well, because every instruction takes the same shape and duration
- **Lower power consumption** and simpler hardware
- Example: ARM, used in virtually all mobile devices

| | RISC | CISC |
| Instruction set size | Small | Large |
| Instruction length | Fixed | Variable |
| Cycles per instruction | Usually one | Several |
| Instructions per program | More | Fewer |
| Complexity is in | The compiler | The hardware |
| Pipelining | Straightforward | Difficult |
| Power consumption | Lower | Higher |
| Registers | Many | Fewer |

!key Why RISC won mobile :: Fixed length instructions pipeline cleanly, and simpler hardware draws less power. On a device running from a battery, power efficiency outweighs everything else.
"""),
        Section("GPUs and parallel systems", """
### Graphics Processing Units

A GPU contains **thousands of relatively simple cores** designed to perform the **same operation on many data items simultaneously**. This is single instruction, multiple data, or SIMD.

**Well suited to:**

- Graphics rendering, where the same lighting calculation applies to millions of pixels
- Machine learning, which is dominated by matrix multiplication
- Scientific simulation, image and video processing
- Cryptographic work and password cracking

**Poorly suited to:**

- Tasks with complex branching, where different data items need different code paths
- Sequential tasks where each step depends on the previous result
- General purpose operating system work

A CPU has few powerful cores optimised for complex sequential work with sophisticated branch prediction. A GPU has many simple cores optimised for throughput on uniform work. They are complementary, not competing.

### Multicore and parallel systems

- **Multicore.** Several complete processing units on one chip, each able to execute a separate thread.
- **Parallel processing.** Dividing a task so that parts run simultaneously on different processors.

**Limits on parallel speedup:**

1. **Amdahl's law.** If a fraction of the task must remain sequential, that fraction sets a ceiling on the possible speedup no matter how many processors are added.
2. **Data dependencies.** A step that needs the result of a previous step cannot start early.
3. **Communication overhead.** Coordinating processors and sharing data costs time that grows with the number of processors.
4. **Software support.** Code that is not written to be multi threaded uses one core.

!exam A frequent question :: "Explain why doubling the number of cores does not halve the execution time." The answer needs Amdahl's law, data dependencies, coordination overhead and software support, not just one of them.
"""),
    ],
    keyterms=[
        ("RISC", "Reduced Instruction Set Computer, using few simple fixed length instructions."),
        ("CISC", "Complex Instruction Set Computer, using many complex variable length instructions."),
        ("Microcode", "Low level instructions inside a CISC processor that implement its complex instructions."),
        ("GPU", "Graphics Processing Unit, with many simple cores optimised for the same operation on much data."),
        ("SIMD", "Single Instruction Multiple Data, applying one operation across many data items simultaneously."),
        ("Multicore", "A processor containing several complete cores capable of independent execution."),
        ("Parallel processing", "Dividing a task so that parts execute simultaneously on different processors."),
        ("Amdahl's law", "The principle that speedup is limited by the fraction of a task that must be sequential."),
        ("Co-processor", "A secondary processor handling specific tasks to relieve the main processor."),
    ],
    grade="""
+ Explain RISC and CISC as a trade off about where complexity sits, not as good against bad
+ Link RISC's fixed length instructions directly to its suitability for pipelining
+ Explain GPU suitability in terms of the same operation applied to many data items
+ Give at least three separate reasons why parallel speedup is less than linear
+ Name a real example of each architecture: ARM for RISC, x86 for CISC
""",
    mistakes=[
        "Saying RISC is faster than CISC. It uses more instructions per task but pipelines far better.",
        "Saying a GPU is simply a faster processor. It is optimised for throughput on uniform work, not for sequential complexity.",
        "Giving only Amdahl's law when asked why parallelism does not scale linearly.",
        "Forgetting that most CISC processors now translate instructions into RISC style operations internally.",
    ],
    quiz=[
        Q("Which is a characteristic of RISC?",
          ["Fixed length instructions that mostly execute in one cycle",
           "Variable length complex instructions", "Complexity in the hardware", "Fewer instructions per program"], 0,
          "Uniformity is exactly what makes RISC so straightforward to pipeline."),
        Q("Where does complexity sit in a RISC system?",
          ["In the compiler", "In the hardware", "In the operating system", "In cache"], 0,
          "The compiler must build complex operations from simple instructions, which is why RISC compilers are sophisticated."),
        Q("Why are GPUs well suited to machine learning?",
          ["The same operation is applied across huge amounts of data simultaneously",
           "They have higher clock speeds than CPUs",
           "They have larger instruction sets",
           "They require no memory"], 0,
          "Matrix multiplication is the same arithmetic repeated across millions of values, which is the SIMD model exactly."),
        Q("What does SIMD stand for?",
          ["Single Instruction Multiple Data", "Sequential Instruction Modular Design",
           "Shared Interrupt Memory Device", "Simple Integrated Microprocessor Design"], 0,
          "One instruction is applied to many data items at once, which is the core of GPU design."),
        Q("Why does doubling the number of cores not halve execution time?",
          ["Part of the task is sequential and coordination adds overhead",
           "Cores run at half speed when doubled", "The clock speed drops",
           "Operating systems only use one core"], 0,
          "Amdahl's law, data dependencies, communication overhead and software support all limit the gain."),
        Q("Which architecture is used in almost all mobile phones?",
          ["RISC, specifically ARM", "CISC, specifically x86", "Harvard only", "Neither"], 0,
          "Low power consumption and clean pipelining make RISC the right choice for battery powered devices."),
        Q("What is microcode?",
          ["Low level instructions inside a CISC processor implementing its complex instructions",
           "The source code of an operating system", "A type of cache", "Assembly language"], 0,
          "It is how a single complex CISC instruction is broken into internal hardware steps."),
        Q("A task is 20 per cent sequential. What is the maximum possible speedup with unlimited processors?",
          ["5 times", "20 times", "80 times", "Unlimited"], 0,
          "Amdahl's law gives 1 divided by 0.2, which is 5. The sequential fifth cannot be sped up at all."),
        Q("Which task is LEAST suited to a GPU?",
          ["Running an operating system with complex branching",
           "Rendering graphics", "Training a neural network", "Processing a large image"], 0,
          "GPU cores are poor at divergent branching, where different data items need different code paths."),
        Q("Compared with CISC, a RISC program for the same task typically:",
          ["Contains more instructions", "Contains fewer instructions",
           "Contains the same number", "Cannot be written"], 0,
          "Simple instructions mean more of them are needed, which was a real disadvantage when memory was expensive."),
    ],
    exam=[
        EQ("State two differences between RISC and CISC processors.", 2, [
            MP("RISC has a small instruction set with fixed length instructions, CISC has a large set with variable length", ["small", "large", "fixed", "variable", "instruction set"]),
            MP("RISC instructions usually take one cycle, CISC instructions take several", ["one cycle", "several cycles", "multiple cycles", "single cycle"]),
        ], "A RISC processor has a small instruction set consisting of simple, fixed length instructions, whereas a CISC processor has a large instruction set containing complex instructions of variable length. As a consequence, RISC instructions typically complete in a single clock cycle while CISC instructions may take several, which means a RISC program needs more instructions to accomplish the same task but is far easier to pipeline.",
           command="State"),
        EQ("Explain why RISC processors are commonly used in mobile devices.", 4, [
            MP("Simpler hardware consumes less power", ["less power", "power consumption", "energy", "efficient"]),
            MP("Battery life is a critical constraint on a mobile device", ["battery", "mobile", "portable", "charge"]),
            MP("Fixed length uniform instructions pipeline effectively, giving good throughput", ["pipeline", "fixed length", "uniform", "throughput"]),
            MP("Less complex hardware also generates less heat, which matters in a sealed device", ["heat", "cooling", "thermal", "no fan", "sealed"]),
        ], "RISC processors use a small set of simple instructions implemented in comparatively simple hardware, and that simplicity translates directly into lower power consumption per instruction. On a mobile device, where everything runs from a battery of fixed capacity, power efficiency is the dominant design constraint and outweighs raw peak performance. The uniform, fixed length instructions also pipeline extremely effectively, so despite each instruction doing less work the processor achieves high throughput, closing much of the performance gap. Finally, simpler hardware drawing less power generates less heat, which is essential in a thin sealed device with no fan and no room for a heatsink.",
           command="Explain"),
        EQ("Explain why a GPU is more suitable than a CPU for training a machine learning model.", 4, [
            MP("Training is dominated by the same arithmetic applied to very large amounts of data", ["same operation", "matrix", "repeated", "large amounts", "many values"]),
            MP("A GPU has thousands of simple cores that operate in parallel", ["thousands", "many cores", "parallel", "simple cores"]),
            MP("This matches the SIMD model of one instruction applied to many data items", ["simd", "single instruction", "multiple data", "same instruction"]),
            MP("A CPU has few cores optimised for complex sequential work, so it processes far fewer values per cycle", ["few cores", "sequential", "complex", "fewer", "cpu is optimised"]),
        ], "Training a machine learning model consists overwhelmingly of matrix multiplication, which means the same arithmetic operation applied independently to enormous numbers of values. A GPU is built for exactly this: it contains thousands of relatively simple cores that all execute the same instruction on different data at the same time, which is the single instruction multiple data model. Because the calculations for different elements do not depend on one another, they can all proceed in parallel with almost no coordination cost, so a GPU can complete in one pass what would take a CPU many thousands. A CPU has only a handful of cores, each of which is optimised for complex sequential work with sophisticated branch prediction and large caches, so although each core is individually far more capable, the total number of arithmetic operations completed per cycle is orders of magnitude lower for this kind of workload.",
           command="Explain"),
        EQ("A program is run on a system with four cores rather than one, but the execution time is only reduced by 40 per cent rather than 75 per cent. Explain why.", 5, [
            MP("Part of the task must be executed sequentially and cannot be divided", ["sequential", "cannot be divided", "must be in order", "serial"]),
            MP("Amdahl's law limits the speedup to the fraction that can be parallelised", ["amdahl", "limits", "fraction", "ceiling", "maximum"]),
            MP("Data dependencies mean some steps must wait for earlier results", ["dependencies", "wait", "depends on", "previous result"]),
            MP("Coordinating the cores and sharing data adds overhead", ["overhead", "coordinate", "communication", "synchronisation", "sharing"]),
            MP("The software may not divide the work evenly, leaving some cores idle", ["evenly", "unbalanced", "idle", "load", "not written", "single threaded parts"]),
        ], "Only part of a program can usually be parallelised. Any section that must execute sequentially, such as reading the input, setting up data structures or producing the final output, takes exactly the same time regardless of how many cores are available, and Amdahl's law states that this sequential fraction places a hard ceiling on the achievable speedup. Within the parallel section, data dependencies further limit what can genuinely run at once, because a calculation that requires the result of an earlier step cannot begin until that step has completed. On top of this, running work across four cores introduces overhead that did not exist with one: threads must be created and scheduled, access to shared data must be synchronised to prevent corruption, and results must be gathered and combined at the end, all of which consumes time that grows as more cores are added. Finally, the work may not divide into four equal parts, so some cores finish early and sit idle while the slowest thread completes, and the overall time is determined by that slowest thread rather than by the average.",
           command="Explain"),
        EQ("Explain what is meant by a co-processor and give an example of its use.", 3, [
            MP("A secondary processor that handles specific tasks", ["secondary", "additional", "specific tasks", "specialised"]),
            MP("It relieves the main processor of that work", ["relieves", "frees", "offload", "main processor", "cpu"]),
            MP("Gives a valid example such as a GPU or a maths co-processor", ["gpu", "graphics", "maths", "floating point", "sound", "ai accelerator"]),
        ], "A co-processor is an additional processor that works alongside the main CPU and is specialised for a particular class of task, taking that work off the CPU so it is free to do other things. Because it is designed for one kind of computation it can perform that work far more efficiently than a general purpose processor would. The most familiar example is a GPU, which handles the rendering calculations for graphics and, increasingly, the matrix arithmetic for machine learning, allowing the CPU to run the operating system and application logic without being blocked by that work.",
           command="Explain"),
    ],
)

A_IOSTORAGE = Topic(
    slug="input-output-and-storage",
    title="Input, Output and Storage",
    spec="1.1.3",
    icon="i-database",
    minutes=22,
    blurb="Devices and their uses, magnetic, flash and optical storage, RAM and ROM, virtual storage and how to justify a choice.",
    fact="Solid state drives write data in pages but can only erase in much larger blocks. This mismatch is why an SSD slows down as it fills up, and why wear levelling exists to spread writes across the whole drive.",
    sections=[
        Section("Devices and how they work", """
### Input devices

Convert a real world signal into data the computer can process.

- **Keyboard**: each key closes a circuit, producing a scan code translated by the driver
- **Optical mouse**: an LED and a small camera photograph the surface many times a second and compare successive images to detect movement
- **Barcode scanner**: a laser sweeps across the code and a sensor measures reflected light, since black absorbs and white reflects
- **Microphone**: a diaphragm vibrates, producing a varying voltage sampled by an analogue to digital converter
- **Sensors**: temperature, pressure, light, motion, converting a physical quantity into a measurable electrical value

### Output devices

- **LCD and OLED displays**: an LCD uses a backlight with liquid crystals controlling how much light passes each subpixel, while OLED pixels emit their own light, so black pixels are simply off and contrast is far higher
- **Laser printer**: a laser draws the page as a static charge on a drum, toner sticks to the charged areas and is fused by heat
- **Inkjet printer**: droplets are fired from nozzles onto the paper
- **3D printer**: builds an object layer by layer, usually by extruding molten material

!key Justifying a device choice :: Name the property that matters for the scenario. A laser printer suits an office because its cost per page is low over high volumes and it is fast, whereas an inkjet suits occasional photo printing because the initial cost is low and the colour quality is good.
"""),
        Section("Storage", """
### Magnetic

Rigid platters coated in magnetic material spin at high speed while a read write head on an actuator arm magnetises regions to represent bits.

- Very high capacity at low cost per byte
- Slow relative to solid state, because access requires physical seek and rotation
- Vulnerable to shock, since the head hovers nanometres above the surface
- Magnetic tape is serial access, very cheap per terabyte, still standard for archives

### Flash, solid state

Data is stored as charge trapped in floating gate transistors, arranged in NAND cells.

- No moving parts, so access time is uniform and shock resistance is excellent
- Far faster and lower power than magnetic
- More expensive per byte
- A **finite number of program and erase cycles** per cell, managed by **wear levelling**, which distributes writes across the drive rather than repeatedly hitting the same cells

### Optical

A laser reads pits and lands burned into a reflective layer. Cheap, portable, low capacity, easily scratched, and read only formats cannot be altered.

### RAM and ROM

- **RAM** is volatile and holds the operating system, running programs and their data. **DRAM** must be refreshed constantly and is used for main memory. **SRAM** is faster, needs no refresh, and is used for cache.
- **ROM** is non volatile and holds firmware such as the bootstrap. **EEPROM** and flash allow it to be rewritten for firmware updates.

### Virtual storage

**Virtual memory** is secondary storage used as an extension of RAM. Pages not recently used are written to the page file, freeing physical memory. Excessive paging causes **disk thrashing**, where the system spends more time moving pages than executing instructions.

**Cloud storage** is a form of virtual storage: files appear local but are held on remote servers, giving access from any device and offsite backup, at the cost of requiring a connection and placing data under someone else's control.
"""),
    ],
    keyterms=[
        ("Analogue to digital converter", "Hardware that samples a continuous signal and outputs binary values."),
        ("Magnetic storage", "Storage representing data by magnetising regions of a rotating platter or a tape."),
        ("Solid state storage", "Storage using charge trapped in transistors, with no moving parts."),
        ("Wear levelling", "Distributing writes across a flash device so no cells wear out prematurely."),
        ("DRAM", "Dynamic RAM, which must be refreshed continuously and is used for main memory."),
        ("SRAM", "Static RAM, faster and requiring no refresh, used for cache."),
        ("EEPROM", "Electrically erasable programmable ROM, allowing firmware to be updated."),
        ("Virtual memory", "Secondary storage used as an extension of RAM when physical memory is full."),
        ("Disk thrashing", "Excessive paging between RAM and secondary storage, severely degrading performance."),
    ],
    grade="""
+ Explain how a device works mechanically, not just what it is for
+ Justify a storage choice by naming the property that matters in that scenario
+ Distinguish DRAM from SRAM by refresh requirement and where each is used
+ Explain wear levelling as the response to a finite number of write cycles
+ Explain virtual memory as a paging mechanism with a performance cost, not as extra RAM
""",
    mistakes=[
        "Saying virtual memory 'adds RAM'. It substitutes far slower secondary storage for it.",
        "Saying SSDs never fail. Flash cells have a finite number of program and erase cycles.",
        "Confusing DRAM and SRAM. SRAM is the faster one used for cache.",
        "Describing an OLED as a backlit display. OLED pixels emit their own light, which is why black is truly black.",
    ],
    quiz=[
        Q("How does an optical mouse detect movement?",
          ["It photographs the surface repeatedly and compares successive images",
           "A ball rotates two sensors", "It measures magnetic field changes", "It uses GPS"], 0,
          "An LED illuminates the surface and a tiny camera compares frames thousands of times a second."),
        Q("Which type of RAM requires constant refreshing?",
          ["DRAM", "SRAM", "ROM", "EEPROM"], 0,
          "DRAM stores each bit as charge in a capacitor which leaks, so it must be refreshed. SRAM does not."),
        Q("What is wear levelling?",
          ["Distributing writes across a flash device so no cells wear out early",
           "Defragmenting a hard disk", "Balancing load between processors", "Compressing files"], 0,
          "Each flash cell tolerates only a finite number of program and erase cycles, so writes are spread out."),
        Q("Why does an OLED display achieve better contrast than an LCD?",
          ["OLED pixels emit their own light, so a black pixel is simply switched off",
           "OLED uses a brighter backlight", "OLED has more pixels", "OLED refreshes faster"], 0,
          "An LCD must block light from an always on backlight, so its blacks are never fully black."),
        Q("Which storage is most appropriate for archiving 500 TB retrieved once a year?",
          ["Magnetic tape", "Solid state drives", "Optical discs", "RAM"], 0,
          "Tape has the lowest cost per terabyte and its slow serial access does not matter for a yearly retrieval."),
        Q("What causes disk thrashing?",
          ["Excessive paging between RAM and secondary storage",
           "A damaged hard disk platter", "Too many files on a disk", "An overheating processor"], 0,
          "When physical memory is far too small, the system spends most of its time swapping pages."),
        Q("Where is SRAM typically used?",
          ["Cache", "Main memory", "Secondary storage", "The page file"], 0,
          "SRAM is faster and needs no refresh, but it is more expensive and less dense, so it is used in small quantities."),
        Q("How does a laser printer place toner on the page?",
          ["A laser creates a static charge pattern on a drum that attracts toner",
           "Nozzles spray liquid ink", "A ribbon is struck by pins", "Heat activates the paper"], 0,
          "The toner is then transferred to the paper and fused permanently by heat and pressure."),
        Q("Which is a disadvantage of cloud storage?",
          ["It requires an internet connection and places data under a third party's control",
           "It cannot be accessed from more than one device",
           "It provides no backup", "It has very limited capacity"], 0,
          "Availability and control are the real trade offs against convenience and offsite redundancy."),
        Q("Why is a hard disk drive vulnerable to physical shock?",
          ["The read write head hovers nanometres above a fast spinning platter",
           "The magnetic coating is fragile in air", "It contains glass optics", "It uses flash memory"], 0,
          "Any impact can cause the head to touch the surface, which physically destroys the data stored there."),
    ],
    exam=[
        EQ("Describe how data is stored on a magnetic hard disk drive.", 3, [
            MP("Rigid platters coated with magnetic material rotate at high speed", ["platter", "rotate", "spin", "magnetic material", "disk"]),
            MP("A read write head on a moving arm passes over the surface", ["read write head", "head", "arm", "actuator"]),
            MP("Regions of the surface are magnetised in one direction or another to represent 1 and 0", ["magnetised", "direction", "polarity", "1 and 0", "represent"]),
        ], "A magnetic hard disk drive contains one or more rigid platters coated with a magnetic material, which rotate at high speed, typically between five and fifteen thousand revolutions per minute. A read write head mounted on a moving actuator arm is positioned nanometres above the surface and can be moved radially to reach any track. To write data, the head produces a magnetic field that magnetises a tiny region of the coating in one of two directions, representing a 1 or a 0, and to read it the head detects the direction of magnetisation as the surface passes beneath it.",
           command="Describe"),
        EQ("Explain the difference between DRAM and SRAM and state where each is typically used.", 4, [
            MP("DRAM stores each bit as charge in a capacitor which must be refreshed", ["capacitor", "refresh", "leaks", "recharged"]),
            MP("SRAM uses flip flops and needs no refresh, so it is faster", ["flip flop", "no refresh", "faster", "transistors"]),
            MP("DRAM is denser and cheaper, so it is used for main memory", ["denser", "cheaper", "main memory", "ram", "larger capacity"]),
            MP("SRAM is more expensive and less dense, so it is used for cache", ["expensive", "cache", "less dense", "smaller"]),
        ], "DRAM stores each bit as an electrical charge in a tiny capacitor. Because that charge leaks away, every cell has to be refreshed thousands of times per second, and this refresh cycle both consumes power and makes access slower. SRAM stores each bit using a small arrangement of transistors forming a flip flop, which holds its value as long as power is supplied and therefore needs no refreshing, making it considerably faster to access. The trade off is density and cost: a DRAM cell needs roughly one transistor and one capacitor while an SRAM cell needs about six transistors, so DRAM packs far more capacity into the same area at a much lower price. DRAM is therefore used for main memory where large capacity is essential, while SRAM is used for the small quantities of cache inside and beside the processor where speed matters far more than cost.",
           command="Explain"),
        EQ("Explain what wear levelling is and why it is necessary in solid state storage.", 3, [
            MP("Flash memory cells tolerate only a finite number of program and erase cycles", ["finite", "limited", "number of writes", "wear out", "cycles"]),
            MP("Without intervention frequently written areas would fail long before the rest", ["frequently", "same cells", "fail early", "worn out", "repeatedly"]),
            MP("Wear levelling distributes writes evenly across all cells to extend the drive's life", ["distributes", "spreads", "evenly", "across", "extends life"]),
        ], "Each cell in flash memory can only be programmed and erased a finite number of times before it becomes unreliable, typically in the order of thousands of cycles for consumer drives. Without intervention this would be a serious problem, because file systems repeatedly rewrite certain areas such as directory structures and log files, so those particular cells would wear out and fail while the vast majority of the drive remained almost unused. Wear levelling is a technique implemented by the drive's controller that tracks how many times each block has been written and deliberately redistributes data so that writes are spread evenly across every cell in the device. This means the whole drive ages at approximately the same rate, which extends its usable life very substantially.",
           command="Explain"),
        EQ("A company must choose storage for a database that is accessed thousands of times per second. Justify a suitable choice.", 4, [
            MP("Recommends solid state storage", ["solid state", "ssd", "flash", "nvme"]),
            MP("Access time is uniform because there is no seek or rotational delay", ["no seek", "no moving parts", "uniform", "rotational", "latency"]),
            MP("Random access performance matters most for a database with many small reads", ["random access", "small reads", "database", "many requests", "iops"]),
            MP("Acknowledges the higher cost per byte as the accepted trade off", ["cost", "expensive", "per byte", "trade off", "price"]),
        ], "The company should use solid state storage, ideally NVMe drives. A database serving thousands of requests per second performs a very large number of small random reads scattered across the data, and this is precisely the workload magnetic storage handles worst, because every request requires the actuator arm to seek to the correct track and then wait for the platter to rotate the sector under the head, adding several milliseconds of latency to each access. Solid state storage has no moving parts, so access time is essentially uniform regardless of where the data sits and random reads are served hundreds of times faster, which translates directly into the number of queries the system can serve. The trade off is cost per byte, which is significantly higher than magnetic storage, but for a workload where response time determines whether the service is usable, that cost is easily justified, and the capacity required for a transactional database is generally modest compared with archival data.",
           command="Justify"),
        EQ("Explain what virtual memory is and why heavy use of it degrades performance.", 4, [
            MP("Virtual memory is an area of secondary storage used as an extension of RAM", ["secondary storage", "page file", "swap", "extension", "as if it were ram"]),
            MP("Pages not recently used are written out to free physical memory", ["pages", "written out", "swapped", "not recently used", "freed"]),
            MP("They must be read back when needed, which requires further paging", ["read back", "swapped back", "retrieved", "paging"]),
            MP("Secondary storage is orders of magnitude slower than RAM, so the processor waits", ["much slower", "orders of magnitude", "waits", "idle", "thrashing"]),
        ], "Virtual memory is a region of secondary storage, known as the page file or swap space, which the operating system uses as an extension of physical RAM so that the total memory available to running processes can exceed the RAM actually installed. When physical memory is exhausted, the operating system selects pages that have not been accessed recently and writes them out to the page file, freeing those physical frames for other use. Performance suffers because those pages will usually be needed again, and retrieving them requires reading from secondary storage and typically evicting something else to make room. Secondary storage is orders of magnitude slower than RAM even when it is solid state, so every page fault stalls the process for a period during which the processor has nothing useful to do. When physical memory is very badly oversubscribed the system reaches a state called thrashing, in which almost all processor time is spent moving pages back and forth and almost none is spent executing the programs themselves.",
           command="Explain"),
    ],
)

A_SYSSOFT = Topic(
    slug="systems-software",
    title="Systems Software",
    spec="1.2.1",
    icon="i-software",
    minutes=32,
    blurb="Operating system functions, memory management and paging, every scheduling algorithm, interrupts, and the four types of operating system.",
    fact="Round robin scheduling was designed to be fair, not fast. Every process gets an equal slice whether it needs a microsecond or an hour, which is exactly what makes an interactive system feel responsive.",
    sections=[
        Section("Memory management and scheduling", """
### Memory management

The operating system must decide what occupies physical memory and where.

**Paging** divides memory into fixed size **pages** and physical memory into equally sized **frames**. Any page can go in any frame, so pages of a process need not be contiguous. A **page table** maps logical page numbers to physical frame numbers.

**Segmentation** divides memory into variable sized **segments** that reflect the logical structure of the program, such as a function, an array or a module.

| | Paging | Segmentation |
| Size | Fixed | Variable |
| Divided by | The operating system | The logical structure of the program |
| Fragmentation | Internal, since the last page is rarely full | External, as gaps appear between segments |
| Address | Page number plus offset | Segment number plus offset |

**Virtual memory** uses secondary storage to hold pages that do not fit in RAM. When a required page is absent a **page fault** occurs, the operating system loads it, evicting another page if necessary. Excessive page faults cause **disk thrashing**.

### Scheduling

The scheduler decides which process gets the processor and for how long, aiming to maximise throughput, keep the processor busy, be fair and stay responsive.

| Algorithm | How it works | Strengths and weaknesses |
| **Round robin** | Each process gets a fixed time slice in turn | Fair and responsive, but ignores priority and urgency |
| **First come first served** | Processes run in arrival order until they finish or block | Simple, but one long job blocks everything behind it, the convoy effect |
| **Shortest job first** | The process with the shortest total time runs next | Best average waiting time, but requires knowing run times in advance and can starve long jobs |
| **Shortest remaining time** | Pre-emptive version of shortest job first | Very responsive, but high overhead and worse starvation |
| **Multi level feedback queues** | Several queues of differing priority, with processes moved between them based on behaviour | Flexible and adaptive, but complex to tune |

!key Pre-emptive against non pre-emptive :: A pre-emptive scheduler can interrupt a running process to give the processor to another. Round robin, shortest remaining time and multi level feedback queues are pre-emptive. First come first served and shortest job first are not.
"""),
        Section("Types of operating system and other functions", """
### Types

- **Distributed.** One system spread across multiple networked machines, sharing work and appearing to the user as a single system.
- **Embedded.** Built for one dedicated task, minimal, stored in ROM, highly reliable and low power.
- **Multi tasking.** Several processes appear to run at once through rapid context switching between them.
- **Multi user.** Several users share one system simultaneously, requiring scheduling and access control to keep them separated fairly.
- **Real time.** A guaranteed maximum response time, essential where a late answer is a wrong answer, as in an anti lock braking system or a pacemaker.

### Other operating system functions

- **Interrupt handling.** The end of cycle check, saving state to a stack, running the interrupt service routine, restoring state.
- **Device drivers.** Translating generic operating system instructions into commands a specific hardware device understands, which is why the same operating system supports thousands of printers.
- **File management.** Directory structure, permissions, allocation of blocks, and tracking free space.
- **Security.** Authentication, access rights, encryption support and auditing.

### The BIOS and the boot process

1. Power on. The processor begins executing at a fixed address in ROM.
2. The **BIOS** or UEFI firmware runs a **power on self test**, checking that essential hardware responds.
3. It identifies the boot device and loads the **bootstrap loader** from it.
4. The bootstrap loads the operating system kernel into RAM.
5. Control passes to the kernel, which initialises drivers, memory management and the user interface.

### Virtual machines

A **virtual machine** is a software implementation of a computer.

- **Intermediate code**, such as Java bytecode, is executed by a virtual machine, so the same compiled code runs on any platform with a suitable VM. The cost is slower execution than native code.
- **System virtual machines** run a complete guest operating system in software, allowing several operating systems on one physical machine, sandboxed testing of untrusted software, and consolidation of servers.
"""),
    ],
    keyterms=[
        ("Paging", "Dividing memory into fixed size pages mapped to equally sized physical frames."),
        ("Segmentation", "Dividing memory into variable sized segments reflecting the logical structure of a program."),
        ("Page fault", "An event raised when a required page is not present in physical memory."),
        ("Scheduler", "The operating system component deciding which process runs and for how long."),
        ("Pre-emptive", "A scheduling approach that can interrupt a running process to give the processor to another."),
        ("Round robin", "Scheduling giving each process an equal time slice in turn."),
        ("Starvation", "A process never receiving processor time because others are continually prioritised."),
        ("Device driver", "Software translating operating system instructions into commands for specific hardware."),
        ("Real time operating system", "An operating system guaranteeing a maximum response time."),
        ("Virtual machine", "A software implementation of a computer, used to run intermediate code or a guest operating system."),
        ("BIOS", "Firmware that performs the power on self test and loads the bootstrap loader."),
    ],
    grade="""
+ Compare paging and segmentation on size, who decides the division, and the kind of fragmentation each causes
+ Name each scheduling algorithm with both a strength and a weakness, including starvation and the convoy effect
+ Identify which algorithms are pre-emptive and explain what that means
+ Explain intermediate code and virtual machines in terms of portability against execution speed
+ Explain a real time operating system as one where a late answer is a wrong answer
""",
    mistakes=[
        "Saying paging and segmentation are the same. Pages are fixed size and decided by the OS, segments are variable and follow program structure.",
        "Describing round robin as efficient. It is fair and responsive, which is a different property.",
        "Forgetting starvation as the weakness of shortest job first.",
        "Saying a real time OS is simply fast. It guarantees a maximum response time.",
        "Saying intermediate code runs everywhere with no cost. It executes more slowly than native code.",
    ],
    quiz=[
        Q("What is the key difference between paging and segmentation?",
          ["Pages are fixed size, segments are variable and follow logical program structure",
           "Segments are fixed size and pages vary", "Paging only applies to ROM",
           "Segmentation is used only in embedded systems"], 0,
          "Paging is decided by the operating system, segmentation reflects the structure of the program itself."),
        Q("What is a page fault?",
          ["A required page is not currently in physical memory",
           "A page table has been corrupted", "A page is written to twice", "Memory has run out entirely"], 0,
          "The operating system must fetch the page from secondary storage, evicting another if necessary."),
        Q("Which scheduling algorithm can cause starvation of long processes?",
          ["Shortest job first", "Round robin", "First come first served", "None of them"], 0,
          "If short jobs keep arriving, a long job may never reach the front of the queue."),
        Q("What is the convoy effect?",
          ["One long process blocks all the shorter ones queued behind it",
           "Processes migrate between priority queues",
           "Several processes share a time slice",
           "Pages are swapped repeatedly"], 0,
          "It is the classic weakness of first come first served scheduling."),
        Q("Which scheduling algorithm is NOT pre-emptive?",
          ["First come first served", "Round robin", "Shortest remaining time", "Multi level feedback queues"], 0,
          "First come first served runs each process until it finishes or blocks, with no interruption."),
        Q("What defines a real time operating system?",
          ["It guarantees a maximum response time", "It has the fastest processor",
           "It shows the current time", "It runs only one program"], 0,
          "In a braking system or a pacemaker, a correct answer delivered late is a failure."),
        Q("What is the purpose of a device driver?",
          ["To translate operating system instructions into commands for specific hardware",
           "To defragment a disk", "To schedule processes", "To manage virtual memory"], 0,
          "Drivers are why one operating system can support thousands of different printers."),
        Q("What is the main advantage of intermediate code such as Java bytecode?",
          ["The same compiled code runs on any platform with a suitable virtual machine",
           "It executes faster than native machine code",
           "It requires no compiler", "It cannot contain errors"], 0,
          "Portability is the benefit. Slower execution than native code is the cost."),
        Q("During booting, what does the BIOS do first?",
          ["Runs a power on self test to check essential hardware",
           "Loads the operating system kernel", "Initialises device drivers", "Starts the user interface"], 0,
          "Only once the hardware is confirmed working does it locate a boot device and load the bootstrap."),
        Q("Round robin scheduling is best described as:",
          ["Fair and responsive, giving each process an equal time slice",
           "The most efficient possible algorithm",
           "Prioritising the shortest job", "Non pre-emptive"], 0,
          "Its strength is fairness and responsiveness rather than throughput, and it ignores priority entirely."),
    ],
    exam=[
        EQ("Explain the difference between paging and segmentation.", 4, [
            MP("Pages are fixed size divisions of memory", ["fixed", "same size", "equal", "pages"]),
            MP("Segments are variable in size", ["variable", "different sizes", "vary", "segments"]),
            MP("Paging is decided by the operating system regardless of program structure", ["operating system", "physical", "regardless", "no relation"]),
            MP("Segmentation follows the logical structure of the program such as functions or arrays", ["logical", "structure", "function", "module", "array", "program"]),
        ], "Paging divides memory into fixed size blocks called pages, with physical memory divided into frames of exactly the same size, so any page can be placed in any free frame. The division is made by the operating system purely on the basis of size and takes no account of what the memory contains, which means a single function might be split across two pages. Segmentation instead divides memory into variable sized segments that correspond to the logical structure of the program, so one segment might hold a particular function, another an array and another the stack. Because segments vary in size, allocating and freeing them leaves gaps between them, producing external fragmentation, whereas paging produces internal fragmentation because the final page of an allocation is rarely completely full.",
           command="Explain"),
        EQ("Describe how round robin scheduling works and state one advantage and one disadvantage.", 4, [
            MP("Each process is given a fixed time slice or quantum", ["time slice", "quantum", "fixed", "equal"]),
            MP("When the slice expires the process is pre-empted and moved to the back of the queue", ["pre-empted", "back of the queue", "next process", "interrupted"]),
            MP("Advantage: it is fair and gives good responsiveness for interactive processes", ["fair", "responsive", "equal", "no starvation"]),
            MP("Disadvantage: it ignores priority and urgency, and context switching adds overhead", ["priority", "ignores", "urgency", "overhead", "context switch"]),
        ], "In round robin scheduling every ready process is placed in a queue and each is given the processor for a fixed period known as a time slice or quantum. When that slice expires the process is pre-empted, its state is saved, and it is moved to the back of the queue while the next process runs. The cycle continues so that every process receives processor time regularly. Its main advantage is fairness and responsiveness: no process can monopolise the processor and none can be starved, which makes an interactive system feel consistently responsive to user input. Its main disadvantage is that it takes no account of priority or urgency, so a critical process waits exactly as long as a trivial one, and the frequent context switching consumes processor time that does no useful work, which becomes significant if the quantum is set too short.",
           command="Describe"),
        EQ("Explain what is meant by a real time operating system and give an example of where one would be used.", 3, [
            MP("It guarantees a response within a defined maximum time", ["guarantee", "maximum time", "deadline", "within", "deterministic"]),
            MP("A late response is treated as a failure even if it is correct", ["late", "failure", "too late", "no use", "deadline missed"]),
            MP("Gives a valid example such as anti lock brakes, a pacemaker or industrial control", ["brakes", "pacemaker", "aircraft", "industrial", "medical", "control system"]),
        ], "A real time operating system is one that guarantees a response to an event within a defined maximum time, rather than merely aiming to be fast on average. The essential property is determinism: the worst case response time is known and bounded. In such a system a correct result delivered after the deadline counts as a failure, because the moment for acting has already passed. An anti lock braking system is a clear example: when a wheel locks, the controller must reduce brake pressure within milliseconds, and a decision arriving even slightly late is worthless because the vehicle has already skidded. Other examples include pacemakers, aircraft flight control systems and industrial machinery controllers.",
           command="Explain"),
        EQ("Explain the advantages and disadvantages of using intermediate code executed by a virtual machine.", 5, [
            MP("The source is compiled once into platform independent intermediate code", ["intermediate", "bytecode", "compiled once", "platform independent"]),
            MP("The same code runs on any platform that has a suitable virtual machine", ["any platform", "portable", "different systems", "same code"]),
            MP("This removes the need to compile separately for every target platform", ["no need", "one version", "separately", "recompile"]),
            MP("Execution is slower than native machine code because of the translation layer", ["slower", "translation", "overhead", "not native", "interpreted"]),
            MP("A virtual machine must be installed on the target system", ["must be installed", "requires", "vm installed", "runtime"]),
        ], "With intermediate code, the source is compiled once into a platform independent form such as Java bytecode rather than into the machine code of a particular processor. The main advantage is portability: the same compiled file will run on Windows, macOS, Linux or a mobile platform provided a suitable virtual machine is present, so the developer maintains and distributes one version rather than building and testing a separate binary for every target. This substantially reduces development and distribution effort, and it also allows the virtual machine to provide a controlled sandbox, which improves security. The principal disadvantage is performance. The virtual machine must translate the intermediate code to native instructions as the program runs, and this additional layer means execution is slower than equivalent natively compiled code, even with just in time compilation reducing the gap. There is also a dependency cost, since the appropriate virtual machine must be installed on the target system before the program will run at all, and the program cannot access platform specific hardware features directly.",
           command="Explain"),
        EQ("Describe the sequence of events that occurs when a computer is switched on.", 5, [
            MP("The processor begins executing firmware from a fixed address in ROM", ["rom", "firmware", "fixed address", "bios", "start"]),
            MP("A power on self test checks that essential hardware is present and working", ["post", "self test", "checks hardware", "tests"]),
            MP("The firmware identifies the boot device", ["boot device", "identifies", "locates", "which drive"]),
            MP("The bootstrap loader is loaded and run", ["bootstrap", "loader", "boot loader"]),
            MP("The operating system kernel is loaded into RAM and takes control", ["kernel", "into ram", "operating system", "control", "loaded"]),
        ], "When power is applied, the processor begins executing instructions from a fixed address which points into ROM, so the first code to run is firmware rather than anything on the disk. That firmware, the BIOS or UEFI, performs a power on self test which verifies that essential hardware such as memory, the processor and the display adapter are present and responding, halting with an error if anything critical fails. It then consults its configuration to determine the boot order and identifies the device to boot from. The bootstrap loader is read from that device into memory and executed, and its job is to locate and load the operating system kernel into RAM. Control is then transferred to the kernel, which initialises memory management, loads device drivers, starts system services and finally presents the user interface.",
           command="Describe"),
    ],
)

A_APPGEN = Topic(
    slug="applications-generation",
    title="Applications Generation and Software Development",
    spec="1.2.2 and 1.2.3",
    icon="i-code",
    minutes=34,
    blurb="Translators, the stages of compilation, linkers and loaders, libraries, and every software development methodology with its strengths and weaknesses.",
    fact="A compiler makes several complete passes over your source code before producing anything. Lexical analysis, syntax analysis, semantic analysis, optimisation and code generation each look at the whole program in a different way.",
    sections=[
        Section("Translators and the stages of compilation", """
### The three translators

- **Assembler.** Translates assembly language to machine code, essentially one to one.
- **Compiler.** Translates the entire source into machine code before execution, producing an executable. All errors are reported after the attempt. The executable runs fast and the source stays private, but a separate build is needed for each platform.
- **Interpreter.** Translates and executes one statement at a time, every time the program runs. It stops at the first error, which makes development much easier, but execution is slower and both the source and the interpreter are needed to run.

### The stages of compilation

**1. Lexical analysis.** The source is read character by character and grouped into **tokens**. Whitespace and comments are removed. Identifiers and constants are entered into the **symbol table**.

**2. Syntax analysis.** The token stream is parsed against the grammar of the language to build an **abstract syntax tree**. Anything that does not fit produces a **syntax error**. Semantic checks such as type compatibility and use of undeclared variables also happen here.

**3. Code generation.** The abstract syntax tree is converted into machine code or object code.

**4. Optimisation.** The code is improved to run faster or use less memory: removing redundant instructions, moving invariant calculations out of loops, reusing registers efficiently. Optimisation takes compilation time and can make debugging harder because the generated code no longer maps neatly onto the source.

### Linkers, loaders and libraries

- A **library** is a collection of pre-compiled, pre-tested subroutines that can be reused. It saves development time and the code is generally more reliable than a fresh implementation.
- A **linker** combines the compiled object code with the library code the program uses.
  - **Static linking** copies the library code into the executable. The file is larger but self contained, and it is unaffected by later library changes.
  - **Dynamic linking** stores only a reference, and the library is loaded at run time. The executable is smaller and a library update benefits every program using it, but a missing or incompatible library breaks the program.
- A **loader** copies the executable into memory and prepares it to run, resolving addresses.

!key Static against dynamic linking :: Static gives reliability and independence at the cost of size and duplication. Dynamic gives smaller files and shared updates at the cost of a run time dependency.
"""),
        Section("Development methodologies", """
### Waterfall

Sequential stages: analysis, design, implementation, testing, evaluation, maintenance. Each is completed before the next begins.

- Clear structure with well defined documentation at every stage, so progress is easy to manage
- Suits projects where the requirements are fully known and stable, such as safety critical systems
- Very inflexible: changing a requirement late means revisiting earlier stages at great expense
- The client sees nothing working until very late

### Agile

An umbrella term for iterative approaches delivering working software in short cycles, with continuous customer involvement.

- Responds well to changing requirements
- The customer sees working software early and often, so misunderstandings surface quickly
- Requires close, continuous customer availability
- Documentation is lighter, which can cause problems for long term maintenance
- Harder to predict a final cost and completion date

### Extreme programming, a form of agile

- **Pair programming**: two developers at one machine, one writing and one reviewing continuously
- **Test driven development**: tests written before the code
- Very frequent small releases and constant refactoring
- Produces high quality code, but is expensive in developer time and demands high discipline

### Spiral

Repeated cycles, each containing determining objectives, **risk analysis**, development and planning the next cycle. Risk is assessed explicitly at every turn.

- Excellent for large, high risk projects
- Expensive, and requires genuine risk assessment expertise

### Rapid application development

Prototypes are built quickly and refined through user feedback.

- Very fast, with strong user involvement, so usability is usually good
- Risk of a poorly structured final system if prototypes are patched rather than rebuilt
- Not suitable for large systems with complex integration

### Choosing one

| Situation | Methodology |
| Requirements fixed and safety critical | Waterfall |
| Requirements likely to change, customer available | Agile |
| Large project with significant risk | Spiral |
| Interface heavy with uncertain user needs | Rapid application development |
| Code quality is paramount and budget allows | Extreme programming |

!exam Always justify against the scenario :: The marks are for linking the choice to something specific in the question, such as an unavailable client, a regulatory requirement or requirements that are certain to change.
"""),
    ],
    keyterms=[
        ("Lexical analysis", "The first stage of compilation, converting source characters into tokens and building the symbol table."),
        ("Token", "A categorised unit of source code such as a keyword, identifier or operator."),
        ("Symbol table", "A structure holding identifiers and their attributes, built during compilation."),
        ("Syntax analysis", "Parsing tokens against the grammar of the language to build an abstract syntax tree."),
        ("Abstract syntax tree", "A tree representing the structure of a program, produced by syntax analysis."),
        ("Code generation", "Converting the abstract syntax tree into machine or object code."),
        ("Optimisation", "Improving generated code so it runs faster or uses less memory."),
        ("Linker", "Software combining compiled object code with the library code the program requires."),
        ("Static linking", "Copying library code into the executable at compile time."),
        ("Dynamic linking", "Storing a reference so the library is loaded at run time."),
        ("Loader", "Software that copies an executable into memory and prepares it for execution."),
        ("Waterfall", "A sequential development methodology completing each stage before the next begins."),
        ("Agile", "Iterative development delivering working software in short cycles with continuous customer involvement."),
        ("Spiral", "An iterative methodology with explicit risk analysis in every cycle."),
    ],
    grade="""
+ Name all four stages of compilation in order and say what each produces
+ Explain the symbol table as built during lexical analysis and used throughout
+ Compare static and dynamic linking on file size, updates and dependency
+ Justify a methodology against something specific in the scenario, not in general
+ Give both a strength and a weakness for every methodology you name
""",
    mistakes=[
        "Giving compilation stages out of order, or omitting optimisation.",
        "Saying agile has no documentation. It has less, which is a genuine maintenance trade off.",
        "Saying waterfall is simply outdated. It remains correct where requirements are fixed and must be documented, as in regulated industries.",
        "Confusing the linker with the loader. The linker combines code, the loader puts it into memory.",
        "Recommending a methodology without referring to anything in the scenario.",
    ],
    quiz=[
        Q("What happens during lexical analysis?",
          ["Source characters are grouped into tokens and the symbol table is built",
           "The abstract syntax tree is built", "Machine code is generated", "Code is optimised"], 0,
          "Comments and whitespace are also removed at this stage, since they carry no meaning for the compiler."),
        Q("At which stage are syntax errors detected?",
          ["Syntax analysis", "Lexical analysis", "Code generation", "Optimisation"], 0,
          "The parser attempts to fit the token stream to the grammar, and anything that does not fit is a syntax error."),
        Q("What is the main advantage of dynamic linking?",
          ["The executable is smaller and a library update benefits every program using it",
           "The program has no external dependencies",
           "It always runs faster", "The library cannot be changed"], 0,
          "The cost is that a missing or incompatible library at run time breaks the program."),
        Q("What does a loader do?",
          ["Copies an executable into memory and prepares it to run",
           "Combines object code with libraries", "Translates source to machine code", "Optimises the code"], 0,
          "The linker combines code, the loader places the result into memory and resolves addresses."),
        Q("Which methodology is most suitable when requirements are fixed and full documentation is legally required?",
          ["Waterfall", "Agile", "Rapid application development", "Extreme programming"], 0,
          "Its sequential stages and heavy documentation are exactly what regulated safety critical work demands."),
        Q("What is a key requirement for agile development to work well?",
          ["Continuous availability of the customer", "A fully fixed specification at the start",
           "A very large development team", "No testing until the end"], 0,
          "Agile depends on frequent feedback, so an unavailable client removes its central advantage."),
        Q("What distinguishes the spiral model?",
          ["Explicit risk analysis in every cycle", "It has only one pass",
           "It never involves the customer", "It produces no documentation"], 0,
          "That is why it suits large, expensive projects where the cost of an unmanaged risk is severe."),
        Q("What is pair programming?",
          ["Two developers working at one machine, one writing and one reviewing",
           "Two teams building the same feature", "Writing two versions of every function",
           "Testing in pairs"], 0,
          "It is a practice of extreme programming, improving quality at the cost of developer time."),
        Q("What is stored in the symbol table?",
          ["Identifiers and their attributes such as type and scope",
           "The machine code produced", "The optimisation settings", "The error messages"], 0,
          "It is built during lexical analysis and consulted throughout the remaining stages."),
        Q("Which is a disadvantage of using a compiler rather than an interpreter during development?",
          ["Errors are reported all together after translating the whole program",
           "The resulting program runs slowly",
           "The source code must be distributed", "It cannot optimise"], 0,
          "An interpreter stops at the first error, which makes locating and fixing problems much easier."),
    ],
    exam=[
        EQ("Describe the stages of compilation.", 6, [
            MP("Lexical analysis groups characters into tokens", ["lexical", "tokens", "characters"]),
            MP("Whitespace and comments are removed and the symbol table is created", ["whitespace", "comments removed", "symbol table"]),
            MP("Syntax analysis parses tokens against the grammar of the language", ["syntax analysis", "parse", "grammar", "rules"]),
            MP("An abstract syntax tree is produced and syntax errors are reported", ["abstract syntax tree", "tree", "syntax error", "reported"]),
            MP("Code generation converts the tree into machine or object code", ["code generation", "machine code", "object code", "converts"]),
            MP("Optimisation improves the code so it runs faster or uses less memory", ["optimisation", "faster", "less memory", "improves", "efficient"]),
        ], "Compilation begins with lexical analysis, in which the source is read character by character and grouped into tokens representing keywords, identifiers, operators and constants. Whitespace and comments are discarded because they have no meaning to the compiler, and identifiers and constants are recorded in the symbol table along with attributes such as type and scope. Syntax analysis then parses the stream of tokens against the formal grammar of the language, building an abstract syntax tree that represents the structure of the program, and reporting a syntax error for anything that cannot be fitted to the grammar. Semantic checks such as type compatibility and the use of undeclared identifiers are also carried out at this point. Code generation then walks the abstract syntax tree and produces the equivalent machine code or object code. Finally the optimisation stage improves that code, for example by removing instructions whose results are never used, moving calculations that do not change out of loops, and allocating registers more efficiently, so that the finished program runs faster or occupies less memory.",
           command="Describe"),
        EQ("Explain the difference between static and dynamic linking.", 4, [
            MP("Static linking copies the library code into the executable at compile time", ["copies", "into the executable", "compile time", "included"]),
            MP("The executable is larger but self contained", ["larger", "bigger", "self contained", "no dependency"]),
            MP("Dynamic linking stores only a reference and loads the library at run time", ["reference", "run time", "loaded when", "not included"]),
            MP("The executable is smaller and library updates apply automatically, but a missing library breaks it", ["smaller", "updates", "shared", "missing", "breaks", "dependency"]),
        ], "Static linking copies the machine code of every library subroutine the program uses directly into the executable file at compile time. The result is a larger file, and identical library code is duplicated across every program that uses it, but the executable is entirely self contained: it will run wherever it is placed and cannot be broken by a later change to the library. Dynamic linking instead stores only a reference to the library, which is located and loaded into memory when the program runs. Executables are therefore much smaller, one copy of the library serves every program on the system, and a security fix or improvement to that library benefits all of them without any of them being rebuilt. The trade off is a run time dependency: if the library is missing, or has been replaced by an incompatible version, the program will fail to start or behave unpredictably.",
           command="Explain"),
        EQ("A company is developing a control system for a medical device. The requirements are fixed by regulation and full documentation must be produced. Recommend a development methodology and justify your choice.", 6, [
            MP("Recommends the waterfall methodology", ["waterfall"]),
            MP("The requirements are fixed and fully known in advance", ["fixed", "known", "will not change", "stable", "defined"]),
            MP("Waterfall completes each stage fully before the next begins", ["each stage", "sequential", "completed before", "in order"]),
            MP("It produces thorough documentation at every stage, which regulation demands", ["documentation", "records", "regulation", "audit", "evidence"]),
            MP("Its inflexibility is not a problem because the requirements cannot change", ["inflexible", "not a problem", "no change", "does not matter"]),
            MP("Notes that a methodology such as agile would produce insufficient documentation for approval", ["agile", "insufficient documentation", "not suitable", "would not meet", "lighter documentation"]),
        ], "The company should use the waterfall methodology. Its central weakness, inflexibility in the face of changing requirements, does not apply here because the requirements are fixed by regulation and cannot change during development, so the risk of an expensive late revision is minimal. Waterfall's sequential structure, completing analysis, design, implementation, testing and evaluation fully in turn, produces a formal signed off deliverable at the end of each stage, and this is precisely what a regulator needs: a complete audit trail demonstrating that every requirement was specified, designed for, implemented and tested. In a medical device context this documentation is not overhead, it is a legal necessity, and its absence would prevent approval regardless of how good the software actually was. An agile approach would be a poor fit here even though it is often preferable elsewhere. Agile deliberately produces lighter documentation and expects requirements to evolve through customer feedback, neither of which is appropriate when the specification is externally imposed and immutable. Its strength, responding rapidly to change, has no value in this project. The one adjustment worth making is to include rigorous verification within each waterfall stage rather than leaving all testing to the end, since defects found late in a safety critical system are extremely expensive to correct.",
           command="Justify"),
        EQ("Explain two advantages of using a library of pre-written subroutines.", 4, [
            MP("Development time is reduced because the code does not have to be written", ["time", "faster", "not written", "already exists", "quicker"]),
            MP("The developer can concentrate on the parts specific to their application", ["concentrate", "focus", "specific", "own problem"]),
            MP("Library code is widely used and tested, so it is more reliable", ["tested", "reliable", "proven", "widely used", "fewer bugs"]),
            MP("Specialist areas such as cryptography are extremely difficult to implement correctly", ["specialist", "cryptography", "difficult", "expertise", "correctly", "security"]),
        ], "The first advantage is development speed. A library provides subroutines for common tasks such as sorting, mathematical functions, file compression or network communication, so the developer does not have to write, debug and document that functionality themselves and can concentrate on the parts of the system that are specific to their own application. The second advantage is reliability. Library code has typically been used by very large numbers of developers over a long period, so defects have been found and corrected in a way that newly written code cannot match. This matters most in specialist areas such as cryptography, where a subtly incorrect implementation may appear to work perfectly while being completely insecure, and where writing it yourself is almost always the wrong decision.",
           command="Explain"),
        EQ("Compare the waterfall and agile approaches to software development.", 6, [
            MP("Waterfall is sequential with each stage completed before the next", ["sequential", "each stage", "one after", "completed before"]),
            MP("Agile is iterative, delivering working software in short repeated cycles", ["iterative", "cycles", "sprints", "repeated", "increments"]),
            MP("Waterfall produces extensive documentation at every stage", ["documentation", "documented", "records"]),
            MP("Agile involves the customer continuously and adapts to changing requirements", ["customer", "continuous", "changing requirements", "feedback", "adapt"]),
            MP("Waterfall handles change poorly and shows the client nothing working until late", ["change", "inflexible", "late", "nothing to see", "expensive to change"]),
            MP("Agile can be harder to cost and schedule and produces lighter documentation", ["cost", "schedule", "predict", "less documentation", "maintenance"]),
        ], "Waterfall is a sequential methodology in which analysis, design, implementation, testing and evaluation are each completed and signed off before the next begins, producing a full set of documentation at every stage. Agile is iterative: the project is divided into short cycles, each of which delivers a working increment of the software, and the customer reviews that increment and influences what is built next. This produces two very different profiles. Waterfall gives strong control and a complete audit trail, which suits projects where the requirements are fixed and where regulators or contracts demand documented evidence, but it handles change extremely badly, because altering a requirement after design is complete means revisiting earlier stages at considerable cost, and the client sees nothing that actually runs until very late in the project. Agile handles change as a normal part of the process rather than an exception, and because working software is delivered early and frequently, misunderstandings about requirements surface within weeks rather than months. Its costs are that it demands continuous customer availability, which many organisations cannot provide, that the final cost and delivery date are much harder to predict at the outset, and that its lighter documentation can make the system more difficult to maintain years later when the original developers have moved on.",
           command="Compare"),
    ],
)

A_LANGUAGES = Topic(
    slug="programming-paradigms",
    title="Types of Programming Language and Assembly",
    spec="1.2.4",
    icon="i-language",
    minutes=30,
    blurb="The paradigms you must compare, Little Man Computer, addressing modes, and how to answer a question that asks you to justify a paradigm.",
    fact="Assembly language has a near one to one relationship with machine code, but that one instruction can still be modified by the addressing mode, which changes whether the operand is a value, an address, or an address of an address.",
    sections=[
        Section("Paradigms", """
### Procedural

Programs are sequences of instructions grouped into procedures and functions, operating on data passed between them. Control is expressed with sequence, selection and iteration.

- Straightforward to learn and to follow
- Well suited to problems that are naturally a series of steps
- Becomes difficult to manage as programs grow, because data and the code acting on it are separate
- Examples: C, Pascal, and Python used procedurally

### Object oriented

Data and the methods that operate on it are bundled into objects created from classes.

- **Encapsulation** means an object controls its own state and can guarantee it stays valid
- **Inheritance** removes duplication by placing shared behaviour in a superclass
- **Polymorphism** lets code work with many types through one interface, so new types need no changes to existing code
- Scales well to large systems and large teams
- Adds overhead and complexity that is not worth it for a small script
- Examples: Java, C#, Python, C++

### Assembly and low level

- One assembly instruction generally corresponds to one machine instruction
- Direct control over registers and memory addresses
- Highly efficient in both speed and memory
- Difficult to write, read and maintain, and specific to one processor architecture
- Used for device drivers, embedded systems with severe constraints, and performance critical routines

### Declarative and functional

The programmer specifies **what** is wanted rather than **how** to compute it. Functional languages avoid changing state, which makes concurrency safer and behaviour more predictable. SQL is the declarative language you will meet most often.

!exam Justifying a paradigm :: Link it to the scenario. A large system built by a team, with many similar entities and likely future extension, points to object oriented. A short data processing script points to procedural. A device driver with tight timing points to assembly.
"""),
        Section("Little Man Computer and addressing modes", """
### The LMC instruction set

| Mnemonic | Code | Meaning |
| `INP` | 901 | Input to the accumulator |
| `OUT` | 902 | Output from the accumulator |
| `LDA` | 5xx | Load the contents of address xx into the accumulator |
| `STA` | 3xx | Store the accumulator at address xx |
| `ADD` | 1xx | Add the contents of address xx to the accumulator |
| `SUB` | 2xx | Subtract the contents of address xx from the accumulator |
| `BRA` | 6xx | Branch always to xx |
| `BRZ` | 7xx | Branch to xx if the accumulator is zero |
| `BRP` | 8xx | Branch to xx if the accumulator is zero or positive |
| `HLT` | 000 | Halt |
| `DAT` | | Declare a data location |

### Reading two numbers and outputting the larger

```assembly
        INP
        STA first
        INP
        STA second
        SUB first        // second minus first
        BRP secondbig    // if zero or positive, second is larger or equal
        LDA first
        OUT
        HLT
secondbig LDA second
        OUT
        HLT
first   DAT
second  DAT
```

### Counting down from a number

```assembly
loop    LDA count
        BRZ done
        OUT
        SUB one
        STA count
        BRA loop
done    HLT
count   DAT 5
one     DAT 1
```

!key Tracing LMC :: Keep a table with the accumulator, each data location and the output. Work one instruction at a time and never skip a pass of a loop.

### Addressing modes

The addressing mode determines how the operand should be interpreted.

| Mode | Meaning | Example |
| **Immediate** | The operand **is** the value | `ADD #5` adds the literal 5 |
| **Direct** | The operand is the **address** of the value | `ADD 60` adds the contents of address 60 |
| **Indirect** | The operand is the address of a location **holding the address** of the value | `ADD (60)` follows the pointer stored at 60 |
| **Indexed** | The value's address is the operand **plus** the contents of an index register | Used for stepping through arrays |

Immediate is fastest since no memory access is needed, but the value is fixed at compile time. Indirect allows pointers and dynamic data structures. Indexed makes array traversal efficient, because only the index register changes between elements.
"""),
    ],
    keyterms=[
        ("Paradigm", "An approach to structuring and thinking about a program, such as procedural or object oriented."),
        ("Procedural", "A paradigm structuring programs as sequences of instructions grouped into procedures."),
        ("Object oriented", "A paradigm bundling data with the methods that operate on it, into objects created from classes."),
        ("Declarative", "A paradigm specifying what is required rather than how to compute it."),
        ("Assembly language", "A low level language with a near one to one correspondence to machine code."),
        ("Little Man Computer", "A simplified model processor and instruction set used to teach assembly programming."),
        ("Immediate addressing", "The operand is the value itself."),
        ("Direct addressing", "The operand is the address of the value."),
        ("Indirect addressing", "The operand is the address of a location holding the address of the value."),
        ("Indexed addressing", "The address is the operand plus the contents of an index register."),
    ],
    grade="""
+ Justify a paradigm against the scenario, naming a specific feature such as inheritance removing duplication
+ Trace LMC code with a full table showing the accumulator, memory and output
+ Distinguish all four addressing modes and give a use for each
+ Explain indexed addressing in terms of array traversal, which is what it exists for
+ Say why assembly is used despite being hard, rather than treating it as obsolete
""",
    mistakes=[
        "Saying object oriented is always better. For a fifty line data script it is unnecessary overhead.",
        "Confusing direct and indirect addressing. Indirect follows a pointer to a second address.",
        "Tracing LMC in your head instead of keeping a table.",
        "Forgetting that BRP branches when the accumulator is zero or positive, not strictly positive.",
        "Saying assembly is obsolete. It remains essential for drivers and tightly constrained embedded work.",
    ],
    quiz=[
        Q("What does immediate addressing mean?",
          ["The operand is the value itself", "The operand is the address of the value",
           "The operand points to an address holding the address", "The operand is added to an index register"], 0,
          "No memory access is needed, so it is the fastest, but the value is fixed when the program is written."),
        Q("Which addressing mode is most useful for stepping through an array?",
          ["Indexed", "Immediate", "Direct", "Absolute"], 0,
          "The base address stays fixed in the instruction while only the index register changes between elements."),
        Q("In LMC, what does BRP do?",
          ["Branches if the accumulator is zero or positive", "Branches if the accumulator is zero",
           "Branches always", "Prints the accumulator"], 0,
          "It is branch if positive, and zero counts as positive, which is a common source of tracing errors."),
        Q("Which paradigm bundles data with the methods that operate on it?",
          ["Object oriented", "Procedural", "Declarative", "Assembly"], 0,
          "That bundling is encapsulation, which lets an object guarantee its own state remains valid."),
        Q("Which is an advantage of the procedural paradigm for a short data processing script?",
          ["It is simple and direct, with none of the overhead of defining classes",
           "It provides inheritance", "It guarantees data validity", "It supports polymorphism"], 0,
          "For a task that is genuinely a sequence of steps, adding a class hierarchy is unnecessary complexity."),
        Q("What does indirect addressing allow?",
          ["The use of pointers and dynamic data structures",
           "Faster access than immediate addressing", "Values fixed at compile time", "Array traversal only"], 0,
          "Following a stored address is what makes linked structures possible at machine level."),
        Q("Why is assembly language still used for device drivers?",
          ["It gives direct control over hardware registers with predictable timing",
           "It is easier to write than a high level language",
           "It is portable across all processors", "It requires no translator"], 0,
          "Precise control and known instruction timing are exactly what a driver needs."),
        Q("In LMC, what does `STA 42` do?",
          ["Stores the accumulator into address 42", "Loads address 42 into the accumulator",
           "Adds 42 to the accumulator", "Branches to address 42"], 0,
          "STA stores, LDA loads. Getting them the wrong way round is a very common tracing error."),
        Q("Which is a disadvantage of the object oriented paradigm?",
          ["It adds complexity and overhead that is unnecessary for small programs",
           "Code cannot be reused", "Data cannot be protected", "It cannot model real world entities"], 0,
          "The benefits of OOP scale with project size, and below a certain size they do not repay the cost."),
        Q("SQL is an example of which paradigm?",
          ["Declarative", "Procedural", "Object oriented", "Assembly"], 0,
          "You specify what data you want, and the database engine decides how to obtain it."),
    ],
    exam=[
        EQ("Explain the difference between immediate and direct addressing.", 3, [
            MP("In immediate addressing the operand is the value to be used", ["value itself", "actual value", "operand is the value", "literal"]),
            MP("In direct addressing the operand is the address where the value is stored", ["address", "location", "where it is stored", "points to"]),
            MP("Immediate needs no memory access so is faster, but the value is fixed", ["faster", "no memory access", "fixed", "cannot change", "compile time"]),
        ], "In immediate addressing the operand contained in the instruction is the actual value to be operated on, so an instruction to add five carries the number five within it. In direct addressing the operand is instead a memory address, and the value to be used is whatever is currently stored at that address, so the processor must perform a memory read before it can carry out the operation. Immediate addressing is therefore faster, since no memory access is required, but the value is fixed at the moment the program is written and cannot change while it runs, whereas direct addressing works with data that varies during execution.",
           command="Explain"),
        EQ("Explain why indexed addressing is useful when working with arrays.", 3, [
            MP("The address used is the operand plus the contents of an index register", ["index register", "plus", "added", "base plus"]),
            MP("The base address of the array stays fixed within the instruction", ["base address", "fixed", "same instruction", "unchanged"]),
            MP("Only the index register needs to change to move to the next element", ["index changes", "increment", "next element", "one register", "loop"]),
        ], "In indexed addressing the effective address is calculated by adding the operand in the instruction to the contents of a dedicated index register. This maps directly onto how an array works: the operand holds the base address of the array and the index register holds the position within it. To move from one element to the next, only the index register has to be incremented, and the same instruction can then be executed repeatedly inside a loop without any modification. This is far more efficient than the alternative of generating a different instruction for every element or performing separate arithmetic to calculate each address.",
           command="Explain"),
        EQ("A company is developing a large system that will be maintained by a team over many years and will need new types of user account added regularly. Justify the use of the object oriented paradigm.", 6, [
            MP("Recommends object oriented", ["object oriented", "oop"]),
            MP("Encapsulation keeps data with the methods that act on it and protects its validity", ["encapsulation", "together", "protects", "valid", "controlled access"]),
            MP("Inheritance places shared behaviour in a superclass so it is written once", ["inheritance", "shared", "superclass", "once", "avoids duplication"]),
            MP("A new account type is added as a subclass without changing existing code", ["subclass", "new type", "without changing", "extend", "add a class"]),
            MP("Polymorphism lets existing code work with new types through the same interface", ["polymorphism", "same interface", "existing code", "same method"]),
            MP("These properties make a large system maintainable by a team over time", ["maintainable", "team", "long term", "large system", "scales"]),
        ], "The object oriented paradigm is the right choice here, principally because of how the system will change over its lifetime. Encapsulation bundles each account's data together with the methods that operate on it and restricts direct access from outside, which means the rules governing what a valid account looks like live in one place and are enforced automatically, rather than being scattered through the codebase where a single developer forgetting a check could corrupt the data. Inheritance addresses the requirement for regularly added account types directly: everything common to all accounts is written once in a base Account class, and each specific type becomes a subclass that inherits that behaviour and overrides only what differs. This eliminates duplication, so a correction to shared logic is made in one place and applies everywhere. Polymorphism then means that existing code which processes accounts continues to work unchanged when a new subclass appears, because it calls the same methods and each object supplies its own implementation. Adding a new account type therefore involves writing one new class rather than finding and editing every conditional statement in the system, which is exactly what a procedural design would require. Over a system maintained by a team for many years, these properties are what keep the cost of change roughly constant instead of rising steeply as the codebase grows.",
           command="Justify"),
        EQ("The following Little Man Computer program is executed with inputs 7 and 3. State the output and explain how it is produced.\n\nINP, STA 90, INP, STA 91, LDA 90, SUB 91, OUT, HLT", 4, [
            MP("The first input 7 is stored at address 90", ["7", "stored", "address 90", "first"]),
            MP("The second input 3 is stored at address 91", ["3", "address 91", "second"]),
            MP("The accumulator is loaded with 7 and 3 is subtracted", ["loaded", "subtract", "7 - 3", "accumulator"]),
            MP("The output is 4", ["4"]),
        ], "The first INP instruction places the value 7 into the accumulator, and STA 90 stores it at address 90. The second INP replaces the accumulator contents with 3, and STA 91 stores that at address 91. LDA 90 then loads the contents of address 90, which is 7, back into the accumulator, and SUB 91 subtracts the contents of address 91, which is 3, leaving 4 in the accumulator. OUT displays the accumulator, so the output is 4, and HLT stops the program.",
           command="State"),
        EQ("Explain one situation in which assembly language would be preferred over a high level language, and one disadvantage of that choice.", 4, [
            MP("Gives a valid situation such as a device driver or a tightly constrained embedded system", ["device driver", "embedded", "real time", "firmware", "critical"]),
            MP("Assembly gives direct control over registers, memory and timing", ["direct control", "registers", "memory", "timing", "hardware"]),
            MP("Disadvantage: it is far harder to write, read and maintain", ["harder", "difficult", "maintain", "read", "error prone"]),
            MP("Disadvantage: it is specific to one processor architecture so it is not portable", ["not portable", "one processor", "architecture", "specific", "rewrite"]),
        ], "Assembly language would be preferred when writing a device driver or the control software for an embedded system with severe constraints. In those situations the programmer needs direct control over specific hardware registers and memory locations, and needs to know exactly how many cycles a sequence of instructions will take, neither of which a high level language and its compiler can guarantee. Assembly also allows the code to be made extremely compact, which matters when the whole program must fit into a few kilobytes of ROM. The disadvantages are substantial. Assembly is far harder to write, read and maintain than a high level language, because a single statement in a high level language may correspond to a dozen assembly instructions with no self documenting structure, so development takes much longer and errors are both more likely and harder to find. It is also written against one specific processor's instruction set, so the code is not portable and moving to different hardware means rewriting it entirely rather than recompiling.",
           command="Explain"),
    ],
)

A_COMPRESSION = Topic(
    slug="compression-encryption-and-hashing",
    title="Compression, Encryption and Hashing",
    spec="1.3.1",
    icon="i-lock",
    minutes=28,
    blurb="Run length and dictionary encoding, symmetric and asymmetric encryption, and what a hash is actually for.",
    fact="In asymmetric encryption you can publish your public key to the entire world and it still cannot be used to read messages sent to you. Only the matching private key can decrypt them, and deriving one from the other is computationally infeasible.",
    sections=[
        Section("Compression", """
### Lossy and lossless

**Lossy** permanently discards data judged least perceptible, giving very large reductions but no way back to the original. Used for images, audio and video.

**Lossless** reduces size by encoding the data more efficiently, and the original is restored exactly. Essential for text, program files, spreadsheets and anything where every byte matters.

### Run length encoding

Consecutive identical values are replaced by the value and a count.

    AAAAABBBCCCCCCCC   becomes   5A 3B 8C

- Extremely effective on data with long runs, such as simple graphics with large blocks of one colour
- Can make a file **larger** if there are few runs, because each single value now needs a count as well
- Lossless

### Dictionary encoding

Repeated sequences are replaced with references to an index, and the dictionary is stored with the compressed data so it can be reversed.

    the cat sat on the mat, the cat sat
    Dictionary: 1=the 2=cat 3=sat
    1 2 3 on 1 mat, 1 2 3

- Very effective on text, which is full of repeated words
- The dictionary itself takes space, so short files may not benefit
- Lossless, and the basis of ZIP and PNG

!key Choosing between them :: Run length encoding suits data with long runs of identical values. Dictionary encoding suits data with repeated sequences that are not adjacent, such as natural language.
"""),
        Section("Encryption and hashing", """
### Symmetric encryption

The **same key** encrypts and decrypts.

- Fast, so suitable for large volumes of data
- The problem is **key distribution**: the key must reach the recipient securely, and if it is intercepted the encryption is worthless
- With n people all communicating, the number of keys required grows as n(n-1)/2

### Asymmetric encryption, public key

Two mathematically related keys. The **public key** may be distributed freely. The **private key** is never shared.

- Anything encrypted with the public key can only be decrypted with the private key, so anyone can send you a secure message
- Anything encrypted with the **private** key can be decrypted with the public key, which proves it came from the holder of the private key. This is a **digital signature**
- Solves key distribution completely
- Considerably slower than symmetric encryption

### How they are used together

In practice HTTPS uses both. Asymmetric encryption is used at the start of the connection to exchange a **symmetric session key** securely, and all the actual data is then encrypted symmetrically because it is far faster. This takes the security of asymmetric key exchange and the speed of symmetric encryption.

### Digital signatures and certificates

1. The sender produces a **hash** of the message.
2. The hash is encrypted with the sender's **private key**, producing the signature.
3. The recipient decrypts it with the sender's public key and independently hashes the message.
4. If the two hashes match, the message is unaltered and came from the holder of that private key.

A **digital certificate** issued by a certificate authority binds a public key to an identity, which is what stops an attacker simply publishing a public key claiming to be your bank.

### Hashing

A **hash function** takes an input of any size and produces a fixed size output.

Properties of a good hash function:

- **Deterministic.** The same input always gives the same output.
- **Fast to compute.**
- **One way.** It must be computationally infeasible to recover the input from the hash.
- **Avalanche effect.** A tiny change to the input produces a completely different hash.
- **Collision resistant.** It should be extremely difficult to find two inputs with the same hash.

### Uses

- **Password storage.** Store the hash rather than the password. A stolen database does not reveal the passwords. A **salt**, a random value added before hashing, ensures two identical passwords produce different hashes and defeats precomputed rainbow tables.
- **Hash tables.** The hash of a key determines the storage index, giving average constant time lookup.
- **Integrity checking.** Rehash a downloaded file and compare with the published hash to confirm nothing changed.
- **Digital signatures**, as above.

!warn Hashing is not encryption :: Encryption is two way and reversible with a key. Hashing is one way by design. You never decrypt a hash, you hash the new input and compare.
"""),
    ],
    keyterms=[
        ("Lossy compression", "Compression that permanently discards data, giving large reductions but no exact recovery."),
        ("Lossless compression", "Compression that allows the original data to be restored exactly."),
        ("Run length encoding", "Replacing runs of identical consecutive values with the value and a count."),
        ("Dictionary encoding", "Replacing repeated sequences with references to an index stored with the data."),
        ("Symmetric encryption", "Encryption using the same key to encrypt and decrypt."),
        ("Asymmetric encryption", "Encryption using a public key to encrypt and a matching private key to decrypt."),
        ("Key distribution problem", "The difficulty of getting a symmetric key to the recipient securely."),
        ("Digital signature", "A hash encrypted with a private key, proving authorship and that the message is unaltered."),
        ("Digital certificate", "A document from a certificate authority binding a public key to a verified identity."),
        ("Hash function", "A function producing a fixed size output from an input of any size, designed to be one way."),
        ("Salt", "A random value added to a password before hashing so identical passwords hash differently."),
        ("Collision", "Two different inputs producing the same hash value."),
    ],
    grade="""
+ Explain why run length encoding can increase file size, and on what data it works well
+ State the key distribution problem as the reason asymmetric encryption exists
+ Explain how HTTPS uses both types together, and why
+ Describe the digital signature process in four ordered steps
+ Never describe hashing as reversible, and explain salting as defeating rainbow tables
""",
    mistakes=[
        "Saying hashing is a form of encryption. It is one way and cannot be reversed.",
        "Claiming run length encoding always reduces size. On data with few runs it makes files larger.",
        "Saying asymmetric encryption is better than symmetric. It is much slower, which is why both are used together.",
        "Forgetting the salt when discussing password storage.",
        "Confusing which key does what. Encrypt with the public key for secrecy, with the private key for a signature.",
    ],
    quiz=[
        Q("When can run length encoding increase the size of a file?",
          ["When there are very few runs of identical consecutive values",
           "When the file is very large", "When the file is text", "It never increases size"], 0,
          "Each single value then needs a count of one stored alongside it, doubling the data."),
        Q("What problem does asymmetric encryption solve?",
          ["Key distribution, since the public key can be shared openly",
           "Slow encryption of large files", "Data compression", "Password storage"], 0,
          "There is no need to transmit a secret key, which removes the risk of it being intercepted."),
        Q("Why does HTTPS use both symmetric and asymmetric encryption?",
          ["Asymmetric securely exchanges a session key, then fast symmetric encryption carries the data",
           "Asymmetric is used for images and symmetric for text",
           "For legal reasons", "To make the connection slower and safer"], 0,
          "It combines the secure key exchange of asymmetric with the speed of symmetric encryption."),
        Q("What is the avalanche effect?",
          ["A tiny change to the input produces a completely different hash",
           "Hash values gradually become longer", "Collisions increase with file size", "Encryption keys expire"], 0,
          "It means you cannot tell from two hashes whether the inputs were nearly identical."),
        Q("Why are passwords stored as salted hashes?",
          ["A stolen database does not reveal passwords, and identical passwords hash differently",
           "It makes login faster", "It compresses the database", "It encrypts the whole database"], 0,
          "The salt defeats precomputed rainbow tables, because each password must be attacked individually."),
        Q("A digital signature is created by:",
          ["Encrypting a hash of the message with the sender's private key",
           "Encrypting the message with the recipient's public key",
           "Hashing the recipient's public key", "Compressing the message"], 0,
          "Anyone can then decrypt it with the sender's public key, which proves who sent it."),
        Q("Which compression method replaces repeated sequences with index references?",
          ["Dictionary encoding", "Run length encoding", "Lossy compression", "Hashing"], 0,
          "It suits natural language, where the same words recur throughout but not adjacently."),
        Q("What is a hash collision?",
          ["Two different inputs producing the same hash value",
           "A hash that cannot be computed", "A hash longer than its input", "Two identical inputs"], 0,
          "A good hash function makes finding one computationally infeasible."),
        Q("Which key encrypts a message so that only the intended recipient can read it?",
          ["The recipient's public key", "The recipient's private key",
           "The sender's public key", "The sender's private key"], 0,
          "Only the matching private key, which only the recipient holds, can decrypt it."),
        Q("What is the main disadvantage of symmetric encryption?",
          ["The key must be transmitted securely to the recipient",
           "It is very slow", "It cannot handle large files", "It requires a certificate authority"], 0,
          "If the key is intercepted in transit, the encryption provides no protection at all."),
    ],
    exam=[
        EQ("Explain how run length encoding compresses data and state one type of data for which it is unsuitable.", 4, [
            MP("Runs of identical consecutive values are replaced by the value and a count", ["consecutive", "identical", "count", "replaced", "run"]),
            MP("Gives a valid example of the encoding", ["5a", "example", "aaaaa", "3b"]),
            MP("It is lossless, so the original is restored exactly", ["lossless", "exactly", "restored", "no data lost"]),
            MP("It is unsuitable for data with few runs, such as a photograph, where it may increase size", ["photograph", "few runs", "increase size", "larger", "no repetition", "random"]),
        ], "Run length encoding works by scanning the data for runs of identical consecutive values and replacing each run with a single copy of the value together with a count of how many times it repeated, so a sequence of five As followed by three Bs is stored as 5A3B. It is lossless, because the count contains everything needed to reconstruct the original sequence exactly. It is unsuitable for data that contains few runs of identical adjacent values, such as a photograph, where neighbouring pixels almost always differ slightly. In that case almost every value would be stored with a count of one, so the encoded file would actually be larger than the original.",
           command="Explain"),
        EQ("Explain the difference between symmetric and asymmetric encryption.", 4, [
            MP("Symmetric uses the same key to encrypt and decrypt", ["same key", "one key", "shared key"]),
            MP("Asymmetric uses a public key to encrypt and a matching private key to decrypt", ["public key", "private key", "pair", "two keys"]),
            MP("Symmetric is faster but the key must be distributed securely", ["faster", "key distribution", "must be sent", "intercepted"]),
            MP("Asymmetric solves key distribution because the public key can be shared openly, but it is slower", ["shared openly", "no need to send", "slower", "solves distribution"]),
        ], "Symmetric encryption uses a single shared key for both encryption and decryption, so both parties must possess the same secret. Asymmetric encryption uses a mathematically related pair of keys: a public key that may be distributed openly and a private key that is never shared, where data encrypted with the public key can only be decrypted with the private one. The practical difference is a trade off between speed and key distribution. Symmetric encryption is considerably faster and therefore suited to encrypting large volumes of data, but it requires the key itself to be transmitted to the recipient by some secure means, and if that transmission is intercepted the encryption is worthless. Asymmetric encryption removes that problem entirely, since the public key can be published without compromising anything, but it is significantly slower, which is why real systems use asymmetric encryption to exchange a symmetric session key and then use that faster symmetric key for the actual data.",
           command="Explain"),
        EQ("Describe how a digital signature is created and used to verify a message.", 5, [
            MP("A hash of the message is calculated", ["hash", "digest", "hashed"]),
            MP("The hash is encrypted with the sender's private key to form the signature", ["private key", "encrypted", "signature", "sender's"]),
            MP("The recipient decrypts the signature using the sender's public key", ["public key", "decrypts", "recipient"]),
            MP("The recipient independently hashes the received message", ["independently", "hashes the message", "own hash", "recalculates"]),
            MP("If the two hashes match, the message is unaltered and came from the private key holder", ["match", "unaltered", "authentic", "not changed", "proves"]),
        ], "To create a digital signature, the sender first passes the message through a hash function to produce a fixed size digest. That digest is then encrypted using the sender's private key, and the result is attached to the message as the signature. To verify it, the recipient decrypts the signature using the sender's public key, which recovers the original hash value, and separately calculates the hash of the message they actually received using the same hash function. If the two hashes are identical then two things are proven at once: the message has not been altered in transit, since any change would produce a completely different hash because of the avalanche effect, and it genuinely came from the holder of the private key, since no one else could have produced a signature that decrypts correctly with that public key.",
           command="Describe"),
        EQ("Explain why passwords should be stored as salted hashes rather than as encrypted values.", 5, [
            MP("Hashing is a one way function that cannot be reversed", ["one way", "cannot be reversed", "irreversible", "not decrypted"]),
            MP("Encryption is reversible, so an attacker who obtains the key recovers every password", ["reversible", "key", "decrypt", "recover", "all passwords"]),
            MP("Login works by hashing the entered password and comparing the hashes", ["compare", "hash the entered", "same hash", "matches"]),
            MP("A salt is a random value added before hashing", ["salt", "random", "added", "unique value"]),
            MP("The salt ensures identical passwords hash differently and defeats precomputed rainbow tables", ["identical passwords", "different hashes", "rainbow table", "precomputed", "each user"]),
        ], "Hashing is a one way function: it is computationally infeasible to recover the original input from the hash, so an attacker who steals the database obtains only hashes and not the passwords themselves. Encryption, by contrast, is reversible by design, which means the system must hold a decryption key somewhere, and an attacker who obtains both the database and that key recovers every password in plain text at once. Authentication does not require the original password to be recoverable: when a user logs in, the system hashes what they typed and compares the result with the stored hash, and a match proves they supplied the right password. Salting adds a random value, unique to each user, to the password before it is hashed, and that salt is stored alongside the hash. This matters because without it two users who chose the same password would produce identical hashes, which is visible information, and an attacker could use a precomputed rainbow table mapping common passwords to their hashes to crack thousands of accounts instantly. With a unique salt per user, every hash is different even for identical passwords, precomputed tables are useless, and the attacker must mount a separate brute force attack against each account individually.",
           command="Explain"),
        EQ("Explain why lossless compression must be used for a program file.", 3, [
            MP("Every byte of a program file is a meaningful instruction or data value", ["every byte", "instruction", "meaningful", "all data needed"]),
            MP("Lossy compression permanently discards data", ["lossy", "discards", "removes", "permanently"]),
            MP("Removing any part would corrupt the program so it would not run correctly", ["corrupt", "would not run", "crash", "broken", "fail"]),
        ], "A program file consists entirely of machine instructions and the data they operate on, and every single byte is significant, since there is no redundant detail that a human observer would fail to notice. Lossy compression achieves its size reduction precisely by permanently discarding information judged to be imperceptible, which is a reasonable trade for an image or a piece of audio but is meaningless for executable code. Discarding any portion of a program would corrupt the instruction stream, so the program would either fail to start, crash during execution or, worse, run while behaving incorrectly. Lossless compression must therefore be used, since it reduces the file size by encoding the same information more efficiently and restores it byte for byte on decompression.",
           command="Explain"),
    ],
)

A_DATABASES = Topic(
    slug="databases",
    title="Databases",
    spec="1.3.2",
    icon="i-database",
    minutes=32,
    blurb="Normalisation to third normal form, entity relationship modelling, SQL, indexing, transactions and the ACID properties.",
    fact="The ACID properties exist because of one question: what happens if the power fails halfway through moving money between two accounts? Every serious database is built around making that question answerable.",
    sections=[
        Section("Structure and normalisation", """
### Key terms

- **Entity**: something data is stored about, becoming a table
- **Attribute**: a property of an entity, becoming a field
- **Record** or tuple: one row
- **Primary key**: an attribute uniquely identifying each record
- **Composite key**: a primary key made of two or more attributes together
- **Foreign key**: an attribute in one table that is the primary key of another, creating the link
- **Secondary key**: an additional indexed field used for searching

### Relationships

- **One to one**: rare, and usually a sign the tables should be merged
- **One to many**: the most common. The foreign key goes on the many side
- **Many to many**: cannot be implemented directly and must be resolved with a **linking table** holding foreign keys to both

### Normalisation

**First normal form (1NF).** No repeating groups, and every field holds a single atomic value. Each record is uniquely identifiable.

**Second normal form (2NF).** In 1NF, and every non key attribute depends on the **whole** primary key, not just part of a composite key.

**Third normal form (3NF).** In 2NF, and no non key attribute depends on another non key attribute. There are no transitive dependencies.

The usual summary: every non key attribute depends on **the key, the whole key, and nothing but the key**.

### Why normalise

- Removes **redundancy**, so the same fact is stored once
- Removes **update anomalies**, where changing a fact in one place leaves other copies wrong
- Removes **insertion anomalies**, where a record cannot be added without unrelated data
- Removes **deletion anomalies**, where deleting a record destroys unrelated information
- Reduces storage and improves data consistency

The cost is more tables and therefore more joins, which can slow complex queries. This is why some analytical systems deliberately **denormalise** for read performance.
"""),
        Section("SQL, indexing and transactions", """
### Querying

```sql
SELECT Name, Grade
FROM Students
WHERE Year = 11 AND Grade >= 7
ORDER BY Grade DESC;

SELECT Students.Name, Courses.Title
FROM Students
INNER JOIN Enrolments ON Students.ID = Enrolments.StudentID
INNER JOIN Courses ON Enrolments.CourseID = Courses.ID
WHERE Courses.Title LIKE 'Comp%';

SELECT Year, COUNT(*) AS Total, AVG(Grade) AS MeanGrade
FROM Students
GROUP BY Year
HAVING COUNT(*) > 5;
```

### Modifying

```sql
INSERT INTO Students (Name, Year, Grade) VALUES ('Aisha', 11, 8);

UPDATE Students SET Grade = 9 WHERE Name = 'Aisha';

DELETE FROM Students WHERE Year = 13;

CREATE TABLE Courses (
    ID      INTEGER PRIMARY KEY,
    Title   VARCHAR(60) NOT NULL,
    Credits INTEGER
);

ALTER TABLE Courses ADD Department VARCHAR(40);
```

!warn UPDATE and DELETE without WHERE affect every row :: This is one of the most damaging mistakes in professional practice, and it is entirely preventable.

### Indexing

An **index** is a separate structure mapping the values of a field to the locations of matching records.

- Searches and sorts on that field become far faster, since the whole table need not be scanned
- Every insert, update and delete becomes slower, because the index must also be maintained
- The index consumes additional storage

Index fields that are searched frequently. Do not index fields that are written far more often than they are read.

### Transactions and ACID

A **transaction** is a group of operations treated as a single indivisible unit.

- **Atomicity.** All operations succeed or none do. A transfer that debits one account must not fail after the debit but before the credit.
- **Consistency.** The database moves from one valid state to another, with all rules and constraints satisfied.
- **Isolation.** Concurrent transactions do not interfere. The result matches some sequential ordering of them.
- **Durability.** Once committed, changes survive a crash or power failure, guaranteed by writing to non volatile storage.

### Concurrency control

- **Record locking** prevents two users modifying the same record simultaneously, but can produce **deadlock** where each transaction waits for a record the other holds
- **Timestamp ordering** gives each transaction a timestamp and resolves conflicts by ordering, avoiding deadlock at the cost of restarting some transactions
- **Serialisation** ensures the outcome of concurrent transactions matches some sequential execution of them
"""),
    ],
    keyterms=[
        ("Entity", "Something that data is stored about, implemented as a table."),
        ("Primary key", "An attribute or set of attributes uniquely identifying each record in a table."),
        ("Foreign key", "An attribute in one table that is the primary key of another, forming the link between them."),
        ("Composite key", "A primary key made up of two or more attributes together."),
        ("Normalisation", "Organising data to remove redundancy and eliminate update, insertion and deletion anomalies."),
        ("Third normal form", "A table in second normal form with no non key attribute depending on another non key attribute."),
        ("Transitive dependency", "A non key attribute depending on another non key attribute rather than directly on the key."),
        ("Linking table", "A table resolving a many to many relationship by holding foreign keys to both entities."),
        ("Index", "A structure mapping field values to record locations, speeding searches at the cost of slower writes."),
        ("Transaction", "A group of database operations treated as a single indivisible unit."),
        ("ACID", "Atomicity, Consistency, Isolation and Durability, the guarantees a reliable transaction system provides."),
        ("Deadlock", "A state where two transactions each hold a lock the other needs, so neither can proceed."),
    ],
    grade="""
+ Apply 1NF, 2NF and 3NF to an actual table rather than reciting the definitions
+ Name the anomalies removed by normalisation: update, insertion and deletion
+ Resolve a many to many relationship with a correctly described linking table
+ Write SQL with joins, aggregate functions and GROUP BY, not just SELECT and WHERE
+ Explain each ACID property with a concrete failure it prevents
+ State the cost of indexing as well as the benefit
""",
    mistakes=[
        "Reciting normal form definitions without applying them to the table in the question.",
        "Putting the foreign key on the wrong side of a one to many relationship. It belongs on the many side.",
        "Implementing a many to many relationship directly rather than with a linking table.",
        "Forgetting the WHERE clause on UPDATE or DELETE.",
        "Describing indexing as purely beneficial, with no mention of slower writes or extra storage.",
        "Confusing atomicity with consistency. Atomicity is all or nothing, consistency is about valid states.",
    ],
    quiz=[
        Q("Which normal form removes transitive dependencies?",
          ["Third normal form", "First normal form", "Second normal form", "Fourth normal form"], 0,
          "3NF requires that no non key attribute depends on another non key attribute."),
        Q("How is a many to many relationship implemented?",
          ["With a linking table holding foreign keys to both entities",
           "By duplicating records in both tables", "With a composite primary key in one table",
           "It cannot be implemented"], 0,
          "The linking table turns one many to many into two one to many relationships."),
        Q("Where does the foreign key go in a one to many relationship?",
          ["On the many side", "On the one side", "In a separate table", "It is not needed"], 0,
          "Each record on the many side refers to exactly one record on the one side."),
        Q("What is an update anomaly?",
          ["Changing a fact in one place leaves other copies of it inconsistent",
           "A record cannot be added", "Deleting a record loses unrelated data", "An index becomes out of date"], 0,
          "It is one of three anomalies normalisation removes by ensuring each fact is stored once."),
        Q("What does the atomicity property guarantee?",
          ["All operations in a transaction succeed or none do",
           "Data is stored in the smallest possible form",
           "Transactions run one at a time", "Committed data survives a crash"], 0,
          "This is what prevents money being debited from one account without being credited to the other."),
        Q("What is one disadvantage of adding an index to a field?",
          ["Inserts, updates and deletes become slower and more storage is used",
           "Searches on that field become slower", "The table can no longer be joined",
           "The primary key is lost"], 0,
          "The index must be maintained on every write, so heavily written fields are poor candidates."),
        Q("Which SQL clause filters groups after aggregation?",
          ["HAVING", "WHERE", "ORDER BY", "GROUP BY"], 0,
          "WHERE filters individual rows before grouping, HAVING filters the resulting groups."),
        Q("What is deadlock?",
          ["Two transactions each hold a lock the other needs, so neither can continue",
           "A database that has run out of storage", "A query that returns no rows",
           "An index that has become corrupted"], 0,
          "Timestamp ordering is one approach that avoids it entirely, at the cost of restarting transactions."),
        Q("A table has a composite key and an attribute depending on only part of it. Which normal form is violated?",
          ["Second normal form", "First normal form", "Third normal form", "None"], 0,
          "2NF requires every non key attribute to depend on the whole primary key."),
        Q("Why might a data warehouse be deliberately denormalised?",
          ["To reduce the number of joins and speed up complex read queries",
           "To save storage space", "To remove update anomalies", "To add more foreign keys"], 0,
          "Analytical systems are read heavy and rarely updated, so the usual arguments for normalisation weigh less."),
    ],
    exam=[
        EQ("Explain what is meant by a foreign key.", 2, [
            MP("An attribute in one table that is the primary key of another table", ["primary key", "another table", "other table", "attribute in one"]),
            MP("It creates the link between the two tables", ["link", "relationship", "connects", "joins", "relates"]),
        ], "A foreign key is an attribute in one table which holds values drawn from the primary key of another table. It is the mechanism that creates a relationship between the two, allowing each record in the first table to be associated with exactly one record in the second, and it is what makes joins possible when querying data spread across several tables.",
           command="Explain"),
        EQ("Explain why a database should be normalised to third normal form.", 5, [
            MP("Normalisation removes redundant duplicated data", ["redundancy", "duplicated", "stored once", "repeated data"]),
            MP("Update anomalies are avoided, since a fact is changed in only one place", ["update anomaly", "one place", "inconsistent", "change once"]),
            MP("Insertion anomalies are avoided, so records can be added independently", ["insertion", "add a record", "without", "independently"]),
            MP("Deletion anomalies are avoided, so removing a record does not destroy unrelated data", ["deletion", "lose", "destroy", "unrelated"]),
            MP("Less storage is used and data consistency is improved", ["storage", "less space", "consistency", "accurate", "integrity"]),
        ], "Normalising to third normal form ensures that every non key attribute depends on the key, the whole key and nothing but the key, which means each individual fact is stored in exactly one place. The most important consequence is the elimination of anomalies. Without normalisation, an update anomaly occurs when a fact stored in several rows is changed in one of them and not the others, leaving the database internally inconsistent with no indication of which copy is right. An insertion anomaly occurs when a new record cannot be added because unrelated information is missing, for example being unable to record a new course until a student has enrolled on it. A deletion anomaly occurs when removing a record destroys information that was only stored there, such as losing all record of a department because its last employee left. Normalisation also reduces the total storage required, since data is not duplicated across many rows, and it improves overall data integrity because there is only ever one authoritative copy of each fact to keep correct.",
           command="Explain"),
        EQ("Write an SQL query that returns the name and course title of every student enrolled on a course, given tables Students(ID, Name), Courses(ID, Title) and Enrolments(StudentID, CourseID).", 4, [
            MP("Selects the required columns from the correct tables", ["select", "name", "title"]),
            MP("Joins Students to Enrolments on the student ID", ["join", "students.id", "studentid", "enrolments"]),
            MP("Joins Enrolments to Courses on the course ID", ["courses.id", "courseid", "join courses"]),
            MP("Uses correct SQL syntax throughout", ["from", "on", "inner join", "="]),
        ], "SELECT Students.Name, Courses.Title\nFROM Students\nINNER JOIN Enrolments ON Students.ID = Enrolments.StudentID\nINNER JOIN Courses ON Enrolments.CourseID = Courses.ID;\n\nThe Enrolments table is the linking table resolving the many to many relationship between students and courses, so two joins are needed. The first connects each student to their enrolment records by matching the student ID, and the second connects each enrolment to the course it refers to by matching the course ID. Because the columns Name and Title come from different tables, they are qualified with their table names to avoid ambiguity.",
           command="Write"),
        EQ("Explain what is meant by the ACID properties of a transaction.", 6, [
            MP("Atomicity means all operations in the transaction succeed or none do", ["atomicity", "all or nothing", "none", "complete"]),
            MP("Gives an example such as a bank transfer not leaving money missing", ["transfer", "bank", "debit", "credit", "example"]),
            MP("Consistency means the database moves from one valid state to another", ["consistency", "valid state", "rules", "constraints"]),
            MP("Isolation means concurrent transactions do not interfere with one another", ["isolation", "concurrent", "interfere", "at the same time"]),
            MP("Durability means committed changes survive a system failure", ["durability", "survive", "crash", "power failure", "permanent"]),
            MP("Together they guarantee the database remains reliable despite failures and concurrency", ["reliable", "guarantee", "together", "integrity", "correct"]),
        ], "Atomicity means that a transaction is indivisible: either every operation within it completes or none of them does. The standard example is transferring money between accounts, where debiting one account and crediting the other must happen together, since a failure between the two would make money simply disappear. Consistency means that a transaction takes the database from one valid state to another, with every rule, constraint and relationship still satisfied when it completes, so a transaction that would violate a foreign key constraint is rejected rather than applied. Isolation means that transactions running at the same time do not interfere with each other, and the result is as though they had run one after another in some order, which prevents one transaction reading data another has partially modified. Durability means that once a transaction has been committed, its changes are permanent and will survive a crash or power failure, which is achieved by writing to non volatile storage and maintaining a transaction log that can be replayed after a restart. Together these four properties are what allow a database to be trusted with financial and other critical data despite hardware failures and thousands of simultaneous users.",
           command="Explain"),
        EQ("A table stores StudentID, StudentName, CourseID, CourseTitle and TutorName. Explain why this table is not in third normal form and describe how it should be restructured.", 6, [
            MP("A student can take several courses, so there is a many to many relationship", ["many to many", "several courses", "multiple", "more than one"]),
            MP("CourseTitle depends on CourseID rather than on the whole key", ["coursetitle", "depends on courseid", "part of the key", "partial dependency"]),
            MP("This is a partial dependency violating second normal form", ["partial", "second normal form", "2nf"]),
            MP("TutorName depends on CourseID, which is a transitive dependency violating third normal form", ["transitive", "tutorname", "third normal form", "non key attribute"]),
            MP("Create a Students table and a Courses table", ["students table", "courses table", "separate tables"]),
            MP("Create a linking table holding StudentID and CourseID as foreign keys", ["linking table", "enrolments", "foreign keys", "both"]),
        ], "The table is not in third normal form for several reasons. Because a student can take more than one course and a course has many students, the relationship is many to many, so identifying a row requires a composite key of StudentID and CourseID. Once that is recognised, StudentName depends only on StudentID and CourseTitle depends only on CourseID, so both are partially dependent on part of the composite key rather than on the whole of it, which breaks second normal form and causes the student's name and the course title to be repeated in every row. TutorName is worse still: it depends on CourseID, which is not itself the whole key, so it is a transitive dependency and breaks third normal form. The consequences are redundancy and anomalies, since changing a course title requires updating many rows and deleting the last enrolment on a course loses all record of that course and its tutor. The correct structure is three tables. A Students table holds StudentID as its primary key with StudentName. A Courses table holds CourseID as its primary key with CourseTitle and TutorName, or with a TutorID foreign key if tutors need their own table. An Enrolments linking table holds StudentID and CourseID as foreign keys, together forming its composite primary key, which resolves the many to many relationship into two one to many relationships and stores each fact exactly once.",
           command="Explain"),
    ],
)

A_NETWORKS = Topic(
    slug="networks-and-web-technologies",
    title="Networks and Web Technologies",
    spec="1.3.3 and 1.3.4",
    icon="i-network",
    minutes=36,
    blurb="The TCP/IP stack, packet switching, DNS, client server and peer to peer, HTML, CSS and JavaScript, search indexing and PageRank.",
    fact="PageRank works by treating a link as a vote, but weights each vote by the importance of the page casting it. The mathematics is an eigenvector calculation on a matrix with billions of rows, and it made Google.",
    sections=[
        Section("Networks and protocols", """
### The TCP/IP stack

| Layer | Responsibility | Protocols |
| **Application** | Provides services to user software and formats data | HTTP, HTTPS, FTP, SMTP, IMAP, POP3, DNS |
| **Transport** | Splits data into segments, adds port numbers, ensures reliable delivery | TCP, UDP |
| **Network** or Internet | Adds source and destination IP addresses, routes packets across networks | IP, ICMP |
| **Link** or Data link | Handles physical transmission on the local medium, adds MAC addresses | Ethernet, Wi-Fi |

Data passes **down** the stack at the sender, gaining a header at each layer, and **up** the stack at the receiver, with each header removed by the corresponding layer. This is **encapsulation**.

**Why layering:** each layer can be developed, replaced or upgraded independently; hardware and software from different manufacturers interoperate provided they follow the rules of their layer; faults can be isolated to a single layer.

**TCP against UDP.** TCP is connection oriented, guaranteeing delivery, ordering and error checking, at the cost of overhead. UDP is connectionless with no guarantee of delivery or order, which makes it faster and therefore preferred for live video, voice and gaming, where a late packet is worse than a missing one.

### Packet switching and circuit switching

**Packet switching** divides data into packets, each carrying source and destination addresses and a sequence number, routed independently and reassembled at the destination.

- Efficient use of the network, since capacity is shared
- Resilient, because packets route around failures
- Variable delay, and packets may arrive out of order

**Circuit switching** establishes a dedicated path for the duration of the communication.

- Consistent quality and guaranteed bandwidth
- Wasteful, since the circuit is reserved even when nothing is being sent

### DNS

The Domain Name System resolves human readable names to IP addresses through a hierarchy of servers: root servers, then top level domain servers such as .uk, then authoritative name servers for the specific domain. Results are cached at every level, which is why a repeated lookup is almost instant.

### Network security and hardware

- **Firewalls** filter traffic against rules. **Packet filtering** examines headers, while **stateful inspection** tracks whole connections and is more effective.
- A **proxy server** sits between clients and the internet, hiding client addresses, caching frequently requested content, and filtering requests.
- **Network address translation** allows many devices to share one public IP address.
- **Client server** centralises resources, backup and control but creates a single point of failure and a potential bottleneck. **Peer to peer** distributes load with no single point of failure but has no central management or backup, and performance depends on which peers are online.
"""),
        Section("Web technologies", """
### HTML, CSS and JavaScript

**HTML** defines structure and content. **CSS** defines presentation. **JavaScript** provides behaviour and runs in the browser.

```html
<div id="quiz" class="panel">
  <h2>Question 1</h2>
  <button onclick="check()">Submit</button>
</div>
```

```css
.panel { border: 1px solid #ccc; padding: 1rem; }
#quiz  { background: #f4f4f4; }
```

```javascript
function check() {
  const panel = document.getElementById("quiz");
  panel.classList.add("answered");
}
```

### Client side and server side processing

| | Client side | Server side |
| Runs on | The user's browser | The web server |
| Speed | Immediate, no round trip needed | Requires a request and response |
| Server load | Reduced | Increased |
| Security | Can be viewed and altered by the user, so never trust it alone | Code and data are hidden from the user |
| Typical use | Form validation for usability, interface effects, animation | Authentication, database access, payment, authoritative validation |

!key The rule that matters :: Client side validation improves the experience by giving immediate feedback. Server side validation provides the security, because a user can disable JavaScript or send a crafted request directly. Validate on both, and trust only the server.

### Search engine indexing

A **web crawler** follows links from page to page, retrieving content. Each page is analysed and added to an **index** mapping words to the pages containing them, along with position and prominence information. When a query arrives, the index is consulted rather than the web itself, which is what makes results appear instantly rather than after a search of billions of pages.

`robots.txt` lets a site request that crawlers avoid particular paths.

### PageRank

PageRank orders results by importance, estimated from the link structure of the web.

- A link to a page counts as a vote for it
- Votes from pages that are themselves important count for more
- A page's outgoing votes are divided among the pages it links to, so a page linking to a thousand others confers little on each
- A **damping factor**, typically 0.85, models a user eventually stopping following links, and keeps the calculation convergent

    PR(A) = (1 - d) + d ( PR(T1)/C(T1) + ... + PR(Tn)/C(Tn) )

where d is the damping factor, T1 to Tn are pages linking to A, and C(T) is the number of outgoing links from T.

The calculation is iterative: every page starts with an equal rank and the formula is applied repeatedly until the values converge.
"""),
    ],
    keyterms=[
        ("TCP/IP stack", "A four layer model organising network protocols into application, transport, network and link layers."),
        ("Encapsulation", "Adding a header at each layer as data passes down the stack, removed at the corresponding layer on receipt."),
        ("TCP", "A connection oriented transport protocol guaranteeing delivery, ordering and error checking."),
        ("UDP", "A connectionless transport protocol with no delivery guarantee, used where speed matters more than reliability."),
        ("Packet switching", "Dividing data into independently routed packets reassembled at the destination."),
        ("Circuit switching", "Establishing a dedicated path for the duration of a communication."),
        ("DNS", "The hierarchical system resolving domain names into IP addresses."),
        ("Proxy server", "A server sitting between clients and the internet, hiding addresses, caching and filtering."),
        ("Client side processing", "Code executed in the user's browser, giving immediate response but no security."),
        ("Server side processing", "Code executed on the web server, hidden from the user and therefore trustworthy."),
        ("Web crawler", "A program following links to retrieve pages for indexing by a search engine."),
        ("PageRank", "An algorithm ranking pages by importance derived from the link structure of the web."),
        ("Damping factor", "A constant in PageRank modelling the probability that a user stops following links."),
    ],
    grade="""
+ Name all four TCP/IP layers with their protocols and describe encapsulation in both directions
+ Compare TCP and UDP and give a scenario where UDP is genuinely preferable
+ Explain why client side validation is never sufficient on its own
+ Explain PageRank as weighted votes divided by outgoing link count, not simply counting links
+ Explain the role of the damping factor rather than treating it as an arbitrary constant
""",
    mistakes=[
        "Placing protocols at the wrong layer. HTTP is application, TCP is transport, IP is network.",
        "Saying UDP is simply worse than TCP. For live video, a late packet is more damaging than a missing one.",
        "Saying client side validation makes a form secure. It can be bypassed entirely.",
        "Describing PageRank as counting inbound links. Votes are weighted and divided among outgoing links.",
        "Confusing packet switching with circuit switching in a comparison question.",
    ],
    quiz=[
        Q("At which layer of the TCP/IP stack does IP operate?",
          ["Network", "Transport", "Application", "Link"], 0,
          "IP handles addressing and routing between networks, which is the network layer's responsibility."),
        Q("What is encapsulation in networking?",
          ["Each layer adds a header as data passes down the stack",
           "Data is compressed before transmission", "Packets are encrypted",
           "Several packets are merged into one"], 0,
          "The corresponding layer at the receiver removes its own header as the data passes back up."),
        Q("When is UDP preferable to TCP?",
          ["Live video and voice, where a late packet is worse than a missing one",
           "Transferring a file that must arrive intact",
           "Sending an email", "Loading a web page"], 0,
          "Retransmitting a lost frame in a live call would arrive after it was needed, so it is better simply dropped."),
        Q("What is the main advantage of packet switching over circuit switching?",
          ["Network capacity is shared efficiently and packets route around failures",
           "It guarantees constant bandwidth", "It has no delay",
           "Packets always arrive in order"], 0,
          "Circuit switching reserves capacity even when idle, which wastes it."),
        Q("Why is client side validation not sufficient for security?",
          ["The user can disable JavaScript or send a crafted request directly to the server",
           "It runs too slowly", "It cannot check numbers", "Browsers do not support it"], 0,
          "Anything running on the user's machine is under their control, so the server must revalidate."),
        Q("In PageRank, why does a page linking to a thousand others confer little rank on each?",
          ["A page's outgoing vote is divided among all the pages it links to",
           "Only the first link counts", "Links beyond ten are ignored",
           "The damping factor removes them"], 0,
          "This is what stops a page boosting others simply by linking to everything."),
        Q("What does the damping factor model in PageRank?",
          ["The probability that a user eventually stops following links",
           "The speed of the web crawler", "The number of pages in the index",
           "The rate at which pages change"], 0,
          "It also keeps the iterative calculation mathematically well behaved and convergent."),
        Q("What does a proxy server do?",
          ["Sits between clients and the internet, hiding addresses, caching and filtering",
           "Assigns IP addresses to devices", "Resolves domain names",
           "Encrypts all network traffic"], 0,
          "Caching frequently requested content also reduces external bandwidth use significantly."),
        Q("What does a web crawler do?",
          ["Follows links between pages to retrieve content for indexing",
           "Ranks pages by importance", "Encrypts web traffic", "Stores user search history"], 0,
          "The index it builds is what the search engine actually queries, not the live web."),
        Q("Which is a disadvantage of the client server model?",
          ["The server is a single point of failure and can become a bottleneck",
           "There is no central backup", "Security cannot be managed centrally",
           "Performance depends on which peers are online"], 0,
          "The last two are weaknesses of peer to peer, not client server."),
    ],
    exam=[
        EQ("Describe the function of each layer of the TCP/IP stack.", 4, [
            MP("The application layer provides services to user software and formats data", ["application", "services", "user software", "http", "formats"]),
            MP("The transport layer splits data into segments and ensures reliable delivery", ["transport", "segments", "packets", "tcp", "reliable", "ports"]),
            MP("The network layer adds IP addresses and routes packets between networks", ["network", "internet layer", "ip address", "routes", "routing"]),
            MP("The link layer handles physical transmission and uses MAC addresses", ["link", "physical", "mac", "ethernet", "wifi", "transmission"]),
        ], "The application layer is where the protocols used directly by software operate, such as HTTP for web pages and SMTP for sending mail, and it is responsible for formatting the data appropriately for the service being used. The transport layer takes that data and divides it into segments, adding port numbers so the receiving machine knows which application the data belongs to, and where TCP is used it also numbers the segments and manages acknowledgements and retransmission to guarantee complete, correctly ordered delivery. The network layer, sometimes called the internet layer, attaches the source and destination IP addresses and is responsible for routing each packet across the intervening networks towards its destination. The link layer handles the actual transmission over the physical medium, adding MAC addresses so that frames reach the correct device on the local network, and it is where Ethernet and Wi-Fi operate.",
           command="Describe"),
        EQ("Explain why a live video call would use UDP rather than TCP.", 4, [
            MP("UDP is connectionless and does not guarantee delivery or ordering", ["connectionless", "no guarantee", "does not retransmit", "no acknowledgement"]),
            MP("This reduces overhead so data arrives with lower latency", ["overhead", "latency", "faster", "less delay"]),
            MP("In a live call a retransmitted packet would arrive too late to be useful", ["too late", "already passed", "no use", "moment has gone"]),
            MP("A small amount of lost data causes a brief glitch, which is preferable to delay", ["glitch", "small loss", "acceptable", "better than", "preferable"]),
        ], "UDP is connectionless: it sends datagrams without establishing a connection, without acknowledgements and without retransmitting anything that is lost, so it carries far less overhead than TCP and delivers data with noticeably lower latency. That matters enormously in a live call, where the total delay between speaking and being heard determines whether a conversation is usable at all. The decisive point is what would happen if TCP were used instead. If a packet carrying a fiftieth of a second of audio were lost, TCP would detect the gap and retransmit it, but by the time the replacement arrived that moment in the conversation would already have passed, so the retransmitted data is worthless while the stall waiting for it is very noticeable. With UDP the missing fragment simply produces a momentary glitch that the human ear largely ignores, and the call continues smoothly. In short, for live media a small amount of loss is far preferable to delay, which is precisely the trade UDP makes.",
           command="Explain"),
        EQ("Explain the difference between client side and server side processing, and state why validation should be performed on both.", 5, [
            MP("Client side code runs in the user's browser", ["browser", "user's machine", "client", "locally"]),
            MP("Server side code runs on the web server", ["server", "web server", "remote", "host"]),
            MP("Client side gives immediate feedback without a round trip to the server", ["immediate", "instant", "no round trip", "quick", "responsive"]),
            MP("Client side code can be viewed, disabled or altered by the user", ["viewed", "disabled", "altered", "modified", "under their control"]),
            MP("Server side validation is authoritative because the user cannot bypass it", ["cannot bypass", "authoritative", "trusted", "secure", "must be checked"]),
        ], "Client side processing is code, usually JavaScript, that is downloaded and executed by the user's own browser, whereas server side processing runs on the web server and only the results are sent to the client. The advantage of client side processing is responsiveness: a form field can be checked the moment the user leaves it, with no request to the server and no waiting, which makes the interface feel immediate and reduces load on the server. The critical weakness is that anything running on the user's machine is entirely under their control. They can read the source, disable JavaScript altogether, modify the code with browser developer tools, or bypass the page completely and send a crafted request directly to the server. Client side validation therefore provides usability but no security whatsoever. Server side validation is authoritative because the user cannot alter or bypass it, and it is the only check that can be trusted to protect the database from invalid or malicious data. Both are used together: client side for a good experience, server side because it is the only one that actually enforces anything.",
           command="Explain"),
        EQ("Explain how the PageRank algorithm determines the importance of a web page.", 5, [
            MP("A link from one page to another is treated as a vote for the target page", ["link", "vote", "counts as", "recommendation"]),
            MP("Votes from pages that are themselves important carry more weight", ["important", "weighted", "more weight", "high ranking"]),
            MP("A page's vote is divided among all the pages it links to", ["divided", "shared", "split", "number of outgoing", "between"]),
            MP("A damping factor models the probability that a user stops following links", ["damping", "0.85", "stops following", "probability"]),
            MP("The calculation is iterative, repeated until the values converge", ["iterative", "repeated", "converge", "until stable", "several passes"]),
        ], "PageRank estimates the importance of a page from the structure of links pointing at it, treating each incoming link as a vote of confidence. Crucially the votes are not counted equally: a link from a page that is itself highly ranked contributes far more than a link from an obscure one, so the rank of a page depends recursively on the ranks of the pages linking to it. Each page's voting power is also divided among all the pages it links out to, so a page with a thousand outgoing links passes only a thousandth of its rank to each, which prevents importance being manufactured simply by linking to everything. A damping factor, conventionally 0.85, is applied to model the probability that a person following links eventually stops and starts somewhere new, and it also guarantees that the mathematics converges rather than concentrating all rank in a small group of pages. Because each page's rank depends on others which are themselves being calculated, the algorithm is iterative: every page begins with an equal rank, the formula is applied to every page, and this repeats until the values stop changing significantly.",
           command="Explain"),
        EQ("Compare the client server and peer to peer network models.", 6, [
            MP("Client server has dedicated servers providing resources to clients", ["server", "dedicated", "provides", "clients request"]),
            MP("Peer to peer has all machines acting as both client and server", ["peer", "equal", "both client and server", "all machines"]),
            MP("Client server allows central backup, security and account management", ["central backup", "security", "accounts", "management", "centralised"]),
            MP("Client server has a single point of failure and can become a bottleneck", ["single point of failure", "bottleneck", "server fails", "overloaded"]),
            MP("Peer to peer is cheaper with no dedicated server and distributes load", ["cheaper", "no server", "distributes", "shares load"]),
            MP("Peer to peer has no central backup or management and depends on which peers are online", ["no central backup", "no management", "online", "switched on", "availability"]),
        ], "In a client server network, dedicated server machines provide resources and services which client machines request, so files, authentication and applications are centralised. In a peer to peer network every machine is an equal that acts as both client and server, sharing its own resources directly with the others. The client server model's strength is control: data can be backed up centrally in one place, user accounts and permissions are administered from a single point, and software updates and security policies are applied consistently across the whole network, which is essential once an organisation grows beyond a handful of machines. Its weaknesses are cost and dependency, since server hardware and specialist staff are expensive, the server represents a single point of failure whose loss affects every user, and it can become a bottleneck if demand exceeds what it can serve. Peer to peer inverts this. It is cheap to set up because there is no server to buy, load is naturally distributed across the participants so it scales well as more peers join, and there is no single point of failure. In exchange it offers no central backup, so data protection depends on each user individually, no central management of security or updates, and availability depends entirely on which peers happen to be switched on, so a file may simply be unreachable. In practice client server suits organisations needing control and reliability, while peer to peer suits small informal networks and distributed content sharing.",
           command="Compare"),
    ],
)

A_DATATYPES = Topic(
    slug="data-types-and-boolean-algebra",
    title="Data Types, Number Systems and Boolean Algebra",
    spec="1.4.1 and 1.4.3",
    icon="i-binary",
    minutes=38,
    blurb="Two's complement, floating point, bitwise operations, character sets, and Boolean algebra including De Morgan's laws and Karnaugh maps.",
    fact="Floating point cannot represent 0.1 exactly, for the same reason denary cannot represent one third exactly. This is why financial systems store money as an integer number of pence rather than as a floating point value.",
    sections=[
        Section("Number representation", """
### Two's complement

The standard representation for signed integers. The most significant bit has a **negative** place value.

For 8 bits: -128, 64, 32, 16, 8, 4, 2, 1

    11101100  =  -128 + 64 + 32 + 8 + 4  =  -20

**To negate a number:** invert every bit, then add one.

    20  = 00010100
    invert 11101011
    add 1  11101100  = -20

Range for n bits: -2^(n-1)^ to 2^(n-1)^ - 1. For 8 bits that is -128 to 127.

Subtraction becomes addition of the negative, which is why hardware needs only an adder.

### Floating point

A number is stored as a **mantissa** and an **exponent**, both in two's complement.

    value = mantissa x 2^exponent

**Normalisation** maximises precision by ensuring the mantissa begins with `01` for a positive number or `10` for a negative one, so no significant bits are wasted on leading duplicates.

Example with a 6 bit mantissa and a 4 bit exponent:

    0.1101 0 0011   ->   mantissa 0.1101, exponent 3   ->   110.1  =  6.5

**The trade off.** For a fixed total number of bits, more mantissa bits give greater **precision** and more exponent bits give greater **range**. You cannot increase both.

**Fixed point** places the binary point at a set position. It is faster and always has the same absolute accuracy, but a far smaller range.

### Bitwise operations

| Operation | Effect |
| `AND` | Masking: `x AND 00001111` keeps only the low nibble |
| `OR` | Setting bits: `x OR 10000000` forces the top bit on |
| `XOR` | Toggling, and a simple reversible cipher, since `(x XOR k) XOR k = x` |
| Left shift | Multiplies by 2 per place |
| Right shift | Divides by 2 per place, losing the bits shifted out |

### Character sets

**ASCII** uses 7 bits for 128 characters. **Unicode** uses 16 or more bits for over a million, covering all major writing systems, at the cost of larger files.
"""),
        Section("Boolean algebra", """
### The operations

| Notation | Meaning |
| `A.B` or `A AND B` | Conjunction |
| `A+B` or `A OR B` | Disjunction |
| `A'` or `NOT A` | Negation |
| `A XOR B` | Exclusive or, true when exactly one input is true |

### The laws you must know

| Law | Form |
| Identity | `A + 0 = A`, `A . 1 = A` |
| Null | `A + 1 = 1`, `A . 0 = 0` |
| Idempotent | `A + A = A`, `A . A = A` |
| Inverse | `A + A' = 1`, `A . A' = 0` |
| Commutative | `A + B = B + A` |
| Associative | `A + (B + C) = (A + B) + C` |
| Distributive | `A . (B + C) = A.B + A.C` |
| Absorption | `A + A.B = A`, `A . (A + B) = A` |
| **De Morgan's** | `(A.B)' = A' + B'` and `(A+B)' = A' . B'` |

**De Morgan's laws in words:** break the bar and change the operator. The negation of an AND is the OR of the negations, and vice versa. This is examined almost every year.

### Simplifying an expression

Simplify `A.B + A.B'`

    A.B + A.B'
    = A.(B + B')      distributive
    = A.1             inverse law
    = A               identity law

Simplify `(A + B).(A + B')`

    = A.A + A.B' + B.A + B.B'    distributive
    = A + A.B' + A.B + 0         idempotent and inverse
    = A(1 + B' + B)              factorise
    = A

### Karnaugh maps

A visual method of simplification. Adjacent cells differ by exactly one variable, so grouping them eliminates that variable.

For two variables:

| | B'=0 | B=1 |
| A'=0 | 1 | 0 |
| A=1 | 1 | 1 |

**Rules:**

1. Group only 1s, in rectangular groups of 1, 2, 4, 8 and so on
2. Make groups as **large** as possible, since a larger group eliminates more variables
3. Groups may **overlap**
4. Groups **wrap around** the edges of the map
5. Every 1 must be covered by at least one group

Here the left column groups vertically to give `B'`, and the bottom row groups horizontally to give `A`, so the expression simplifies to `A + B'`.

### Why simplify

Fewer terms means fewer logic gates, which means lower cost to manufacture, less power consumed, less heat produced, less physical space used and a shorter propagation delay through the circuit.
"""),
    ],
    keyterms=[
        ("Two's complement", "A signed integer representation where the most significant bit carries a negative place value."),
        ("Mantissa", "The significant digits of a floating point number."),
        ("Exponent", "The power of two by which the mantissa is multiplied in floating point representation."),
        ("Normalisation", "Adjusting a floating point number so the mantissa begins 01 or 10, maximising precision."),
        ("Precision", "How finely a value can be represented, determined by the number of mantissa bits."),
        ("Range", "The span of values representable, determined by the number of exponent bits."),
        ("Bit mask", "A pattern combined with a value using AND or OR to isolate or set particular bits."),
        ("De Morgan's laws", "The rules that the negation of an AND is the OR of the negations, and vice versa."),
        ("Karnaugh map", "A grid method for simplifying Boolean expressions by grouping adjacent ones."),
        ("Propagation delay", "The time taken for a signal to pass through the gates of a circuit."),
    ],
    grade="""
+ Convert to and from two's complement in both directions, and state the range for n bits
+ Explain normalisation as maximising precision by removing wasted leading bits
+ State the precision against range trade off explicitly whenever floating point is discussed
+ Apply De Morgan's laws confidently in both directions
+ Show every step of a Boolean simplification, naming the law used
+ Justify simplification by cost, power, heat, space and propagation delay
""",
    mistakes=[
        "Forgetting that the most significant bit in two's complement has a negative place value.",
        "Forgetting the add one step when negating a two's complement number.",
        "Saying more bits give both greater precision and greater range for a fixed total.",
        "Applying De Morgan's law without changing the operator.",
        "Making Karnaugh map groups that are not a power of two in size.",
        "Simplifying without stating which law justified each step.",
    ],
    quiz=[
        Q("What is 11101100 in denary as an 8 bit two's complement number?",
          ["-20", "236", "-108", "20"], 0,
          "The most significant bit is negative: -128 + 64 + 32 + 8 + 4 = -20."),
        Q("How do you negate a two's complement number?",
          ["Invert every bit then add one", "Invert every bit", "Add one then invert", "Shift left by one"], 0,
          "Inverting alone gives ones complement, and the add one step produces two's complement."),
        Q("What is the range of an 8 bit two's complement number?",
          ["-128 to 127", "-127 to 128", "0 to 255", "-128 to 128"], 0,
          "There is one more negative value than positive because zero occupies a positive pattern."),
        Q("In floating point, what does increasing the number of exponent bits do?",
          ["Increases the range but reduces precision for a fixed total",
           "Increases both range and precision", "Increases precision only", "Has no effect"], 0,
          "The total is fixed, so any bit given to the exponent is taken from the mantissa."),
        Q("What is the purpose of normalisation in floating point?",
          ["To maximise precision by removing wasted leading duplicate bits",
           "To make the number positive", "To reduce the exponent to zero", "To convert to fixed point"], 0,
          "A mantissa starting 01 or 10 wastes no significant bits on repeated leading digits."),
        Q("Which is a correct statement of De Morgan's law?",
          ["(A.B)' = A' + B'", "(A.B)' = A' . B'", "(A+B)' = A' + B'", "(A.B)' = A + B"], 0,
          "Break the bar and change the operator. AND becomes OR when negated."),
        Q("Simplify A.B + A.B'",
          ["A", "B", "A.B", "A + B"], 0,
          "Factorising gives A.(B + B'), and B + B' is 1, so the expression reduces to A."),
        Q("In a Karnaugh map, why should groups be as large as possible?",
          ["A larger group eliminates more variables, giving a simpler expression",
           "It makes the map easier to draw", "Small groups are not allowed", "It reduces the number of maps needed"], 0,
          "Each doubling of a group size removes one more variable from the resulting term."),
        Q("What does `x AND 00001111` achieve?",
          ["It masks off the upper four bits, keeping only the lower nibble",
           "It sets the upper four bits to 1", "It toggles all the bits", "It shifts x right by four"], 0,
          "ANDing with a mask of zeros clears those positions while ones preserve the original bits."),
        Q("Why is simplifying a Boolean expression worthwhile?",
          ["Fewer gates means lower cost, less power, less heat and shorter propagation delay",
           "It makes the truth table smaller", "It removes the need for a circuit diagram",
           "It increases the number of inputs"], 0,
          "Every gate removed is a real saving in manufacturing cost and running power."),
    ],
    exam=[
        EQ("Convert the denary number -45 into 8 bit two's complement, showing your working.", 3, [
            MP("Converts 45 to binary as 00101101", ["00101101", "45 is"]),
            MP("Inverts all the bits to give 11010010", ["11010010", "invert", "flip"]),
            MP("Adds one to give 11010011", ["11010011", "add 1", "plus one"]),
        ], "First convert 45 into 8 bit binary: 32 + 8 + 4 + 1 = 45, giving 00101101. Then invert every bit, which produces 11010010. Finally add one, giving 11010011. Checking the result confirms it: -128 + 64 + 16 + 2 + 1 = -45.",
           command="Convert"),
        EQ("Explain why a floating point number is normalised.", 3, [
            MP("Normalisation adjusts the mantissa so it begins 01 for positive or 10 for negative", ["01", "10", "begins", "starts with", "first two bits"]),
            MP("This removes leading duplicate bits that carry no information", ["leading", "wasted", "no information", "duplicate", "redundant"]),
            MP("The greatest possible precision is obtained from the available mantissa bits", ["precision", "accuracy", "most significant", "maximum", "best use"]),
        ], "A floating point value can be written in many equivalent ways by shifting the mantissa and adjusting the exponent to compensate, and most of those forms waste bits. Normalisation adjusts the number so that the mantissa begins with 01 for a positive value or 10 for a negative one, which guarantees that the leading bits actually carry information rather than simply repeating the sign. Because no mantissa bits are wasted on redundant leading zeros or ones, the maximum possible precision is obtained from the fixed number of bits available. Normalisation also gives every value a single unique representation, which makes comparison and arithmetic in hardware much simpler.",
           command="Explain"),
        EQ("Explain the trade off between range and precision in floating point representation.", 4, [
            MP("The mantissa determines precision", ["mantissa", "precision", "accuracy", "significant digits"]),
            MP("The exponent determines range", ["exponent", "range", "magnitude", "how large"]),
            MP("The total number of bits is fixed", ["fixed", "total", "same number", "limited"]),
            MP("Increasing one necessarily reduces the other", ["reduces", "at the expense", "decreases", "cannot increase both", "trade off"]),
        ], "In a floating point representation the mantissa holds the significant digits of the value and therefore determines how precisely a number can be represented, while the exponent determines how far the binary point can be shifted and therefore how large or small a magnitude can be expressed, which is the range. Because the total number of bits available for a value is fixed, every bit allocated to the exponent is a bit taken from the mantissa and vice versa. Increasing the exponent field allows very large and very small numbers to be represented but leaves fewer mantissa bits, so values are stored to fewer significant figures and rounding errors become larger. Increasing the mantissa gives greater accuracy for each stored value but restricts the magnitudes that can be represented at all. A designer must therefore choose the split according to whether the application needs to handle extreme magnitudes or to represent moderate values very accurately.",
           command="Explain"),
        EQ("Simplify the Boolean expression A.B + A.B' + A'.B, showing each step and naming the law used.", 5, [
            MP("Factorises A from the first two terms", ["factorise", "a.(b", "common", "a("]),
            MP("Applies the inverse law that B + B' equals 1", ["b + b'", "inverse", "equals 1", "complement"]),
            MP("Simplifies A.1 to A using the identity law", ["a.1", "identity", "gives a"]),
            MP("Reaches A + A'.B", ["a + a'.b"]),
            MP("Simplifies to A + B using the absorption or distributive law", ["a + b", "absorption", "distributive"]),
        ], "Starting with A.B + A.B' + A'.B, factorise A out of the first two terms to give A.(B + B') + A'.B. By the inverse law B + B' equals 1, so this becomes A.1 + A'.B, and by the identity law A.1 is simply A, leaving A + A'.B. Applying the distributive law gives (A + A').(A + B), and since A + A' equals 1 by the inverse law this becomes 1.(A + B), which by the identity law simplifies to A + B. The final simplified expression is therefore A + B, reduced from three AND terms and two OR operations to a single OR gate.",
           command="Simplify"),
        EQ("State De Morgan's laws and explain why simplifying a Boolean expression is useful in circuit design.", 5, [
            MP("States that the negation of an AND is the OR of the negations", ["(a.b)'", "a' + b'", "not and", "or of the negations"]),
            MP("States that the negation of an OR is the AND of the negations", ["(a+b)'", "a' . b'", "not or", "and of the negations"]),
            MP("Simplification reduces the number of logic gates required", ["fewer gates", "reduces gates", "less hardware", "fewer components"]),
            MP("This lowers manufacturing cost and reduces power consumption and heat", ["cost", "cheaper", "power", "heat", "energy"]),
            MP("It also reduces propagation delay so the circuit operates faster", ["propagation delay", "faster", "quicker", "speed", "delay"]),
        ], "De Morgan's laws state that the complement of a conjunction equals the disjunction of the complements, written (A.B)' = A' + B', and that the complement of a disjunction equals the conjunction of the complements, written (A+B)' = A'.B'. In words, breaking the negation bar over an expression requires changing AND to OR or OR to AND. Simplification matters in circuit design because every term and every operator in a Boolean expression corresponds to physical logic gates on a chip. Reducing an expression from six gates to two directly reduces the number of transistors required, which lowers the manufacturing cost of every unit produced and reduces the physical area occupied on the die, allowing more circuitry in the same space. Fewer gates also draw less current, so the circuit consumes less power and generates less heat, which matters greatly in battery powered and densely packed devices. Finally, each gate a signal passes through introduces a small propagation delay, so a shallower simplified circuit produces its output sooner and can therefore be clocked at a higher frequency.",
           command="State"),
    ],
)

A_STRUCTURES = Topic(
    slug="data-structures",
    title="Data Structures",
    spec="1.4.2",
    icon="i-layers",
    minutes=38,
    blurb="Arrays, records, lists, tuples, stacks, queues, linked lists, graphs, trees and hash tables, with the operations and when to choose each.",
    fact="A hash table gives average constant time lookup regardless of size, which is why a dictionary with ten items and one with ten million behave almost identically. Everything depends on the hash function distributing keys evenly.",
    sections=[
        Section("Linear structures", """
### Arrays, records, lists and tuples

| Structure | Properties |
| **Array** | Fixed size, same data type, contiguous memory, direct access by index in constant time |
| **Record** | Fixed set of named fields of possibly different types, a row in a file |
| **List** | Ordered, may hold mixed types, dynamic size, may not be contiguous |
| **Tuple** | Ordered and **immutable** once created |

An array's index calculation is `base address + index x element size`, which is why access is constant time and why elements must all be the same size.

### Stacks

**Last in, first out.** Operations: `push`, `pop`, `peek`, `isEmpty`, `isFull`.

```pseudo
procedure push(item)
    if top == maxSize - 1 then
        return "Stack overflow"
    endif
    top = top + 1
    stack[top] = item
endprocedure

function pop()
    if top == -1 then
        return "Stack underflow"
    endif
    item = stack[top]
    top = top - 1
    return item
endfunction
```

**Uses:** the call stack holding return addresses and local variables, undo functionality, evaluating reverse Polish notation, backtracking, and depth first search.

### Queues

**First in, first out.** Operations: `enqueue`, `dequeue`, `isEmpty`, `isFull`.

A **linear queue** wastes space as the front pointer advances. A **circular queue** solves this by wrapping the pointers using modulo arithmetic:

    rear = (rear + 1) MOD maxSize

A **priority queue** dequeues the highest priority item rather than the oldest.

**Uses:** print spoolers, keyboard buffers, process scheduling, breadth first search.

### Linked lists

Each **node** holds data and a **pointer** to the next node. A separate pointer marks the start, and a null pointer marks the end.

| | Array | Linked list |
| Memory | Contiguous | Anywhere, connected by pointers |
| Size | Fixed at creation | Grows and shrinks dynamically |
| Access | Direct by index, constant time | Must traverse from the start, linear time |
| Insertion in the middle | Requires shifting every later element | Change two pointers |
| Overhead | None | A pointer stored per node |

Insertion is the key difference. Inserting into the middle of an array of a million elements means moving up to a million items. In a linked list it means changing two pointers.
"""),
        Section("Trees, graphs and hash tables", """
### Graphs

A set of **vertices** connected by **edges**. Edges may be **directed** or undirected, and **weighted** or unweighted.

**Adjacency matrix.** A two dimensional array where entry (i, j) records an edge from i to j.

- Constant time to check whether an edge exists
- Uses n^2^ space regardless of how few edges there are, so it wastes memory on **sparse** graphs
- Better for **dense** graphs

**Adjacency list.** Each vertex stores a list of its neighbours.

- Space proportional to the number of edges, so far more efficient for sparse graphs
- Checking a specific edge requires searching a list
- Better for **sparse** graphs

Uses: road and rail networks, social networks, the web, dependency graphs, state machines.

### Trees

A connected acyclic graph with a **root**, **parent** and **child** nodes, and **leaves** with no children.

A **binary search tree** keeps values ordered: everything in the left subtree is smaller than the node, everything in the right subtree is larger.

- Search, insert and delete average O(log n)
- Degenerates to O(n) if items are inserted in sorted order, producing a linked list
- **Self balancing** trees avoid this

### Traversals

```pseudo
procedure preOrder(node)      // node, left, right - copying a tree
procedure inOrder(node)       // left, node, right - visits in sorted order
procedure postOrder(node)     // left, right, node - deleting, or postfix expressions
```

**In order traversal of a binary search tree outputs the values in ascending order.** This is examined frequently.

### Hash tables

A **hash function** maps a key to an index in an array, giving average constant time insertion and lookup.

A **collision** occurs when two keys hash to the same index.

- **Separate chaining.** Each slot holds a list of all items hashing there. Simple, and degrades gracefully.
- **Open addressing** or linear probing. On collision, try the next free slot. No extra structures, but causes **clustering** which degrades performance.

The **load factor** is the number of items divided by the number of slots. As it rises, collisions become frequent and performance falls, so the table is **rehashed** into a larger array when it passes a threshold, typically around 0.7.

!key Choosing a structure :: Frequent lookup by key means a hash table. Ordered data needing range queries means a binary search tree. Frequent insertion in the middle means a linked list. Fixed size with index access means an array.
"""),
    ],
    keyterms=[
        ("Array", "A fixed size collection of items of the same type in contiguous memory, accessed by index."),
        ("Record", "A structure holding a fixed set of named fields, which may be of different types."),
        ("Tuple", "An ordered collection that cannot be changed after creation."),
        ("Stack", "A last in first out structure supporting push and pop."),
        ("Queue", "A first in first out structure supporting enqueue and dequeue."),
        ("Circular queue", "A queue whose pointers wrap around using modulo arithmetic to avoid wasting space."),
        ("Linked list", "A structure of nodes each holding data and a pointer to the next node."),
        ("Graph", "A set of vertices connected by edges, which may be directed or weighted."),
        ("Adjacency matrix", "A two dimensional array recording which vertices are connected."),
        ("Adjacency list", "A representation where each vertex stores a list of its neighbours."),
        ("Binary search tree", "A tree where the left subtree holds smaller values and the right subtree larger ones."),
        ("In order traversal", "Visiting left subtree, node, then right subtree, which outputs a BST in ascending order."),
        ("Hash table", "A structure using a hash function to map keys to array indexes for constant time access."),
        ("Collision", "Two keys hashing to the same index in a hash table."),
        ("Load factor", "The ratio of stored items to available slots in a hash table."),
    ],
    grade="""
+ Justify a data structure choice by the operations the scenario performs most
+ Compare arrays and linked lists on access time and insertion cost, with the reason for each
+ Explain adjacency matrix against adjacency list in terms of sparse and dense graphs
+ Know that in order traversal of a BST yields sorted output, and that a sorted insertion order degenerates it
+ Explain collision resolution and why the load factor triggers rehashing
""",
    mistakes=[
        "Saying a linked list is faster than an array. Access is slower, insertion in the middle is faster.",
        "Forgetting that a binary search tree degenerates to a linked list if data is inserted in sorted order.",
        "Confusing the traversal orders. In order gives sorted output from a BST.",
        "Using an adjacency matrix for a sparse graph, which wastes enormous amounts of memory.",
        "Saying hash tables are always constant time. That is the average case, and it depends on the load factor and the hash function.",
    ],
    quiz=[
        Q("Which structure operates on a last in first out basis?",
          ["Stack", "Queue", "Linked list", "Binary search tree"], 0,
          "The most recently pushed item is the first popped, which is why stacks suit undo and call handling."),
        Q("What is the main advantage of a circular queue over a linear queue?",
          ["It reuses space at the front rather than wasting it",
           "It can hold more data types", "It is faster to search", "It never becomes full"], 0,
          "Modulo arithmetic wraps the pointers so freed slots at the front are reused."),
        Q("What is the key advantage of a linked list over an array?",
          ["Insertion and deletion in the middle require only pointer changes",
           "Access by index is faster", "It uses less memory per item", "It is stored contiguously"], 0,
          "An array insertion in the middle requires shifting every subsequent element."),
        Q("Which traversal of a binary search tree outputs values in ascending order?",
          ["In order", "Pre order", "Post order", "Level order"], 0,
          "Visiting the left subtree, then the node, then the right subtree follows the ordering property exactly."),
        Q("When does a binary search tree degenerate to linear performance?",
          ["When items are inserted in sorted order", "When it contains duplicates",
           "When it is traversed in order", "When it holds more than 1000 items"], 0,
          "Every new item goes down the same side, producing what is effectively a linked list."),
        Q("Which graph representation is better for a sparse graph?",
          ["Adjacency list", "Adjacency matrix", "Both are identical", "Neither can represent it"], 0,
          "A matrix uses n squared space regardless of how few edges exist, which is very wasteful when edges are rare."),
        Q("What is a hash collision?",
          ["Two different keys hashing to the same index", "A hash table becoming full",
           "A key that cannot be hashed", "Two identical keys being inserted"], 0,
          "It is resolved by separate chaining or by probing for the next free slot."),
        Q("What does the load factor of a hash table measure?",
          ["The ratio of stored items to available slots", "The time taken to hash a key",
           "The number of collisions so far", "The size of each stored item"], 0,
          "As it rises collisions become frequent, so the table is rehashed into a larger array."),
        Q("Which structure is most appropriate for a print spooler?",
          ["A queue, since jobs are printed in the order they arrive",
           "A stack", "A binary search tree", "A hash table"], 0,
          "First in first out is exactly the fairness property a print queue needs."),
        Q("What is stored in each node of a linked list?",
          ["The data and a pointer to the next node", "Only the data",
           "The data and its index", "A pointer to the start of the list"], 0,
          "The final node's pointer is null, which is how traversal knows to stop."),
    ],
    exam=[
        EQ("Explain the difference between a stack and a queue, giving one use for each.", 4, [
            MP("A stack is last in first out", ["last in", "lifo", "most recent"]),
            MP("A queue is first in first out", ["first in", "fifo", "oldest"]),
            MP("Gives a valid stack use such as the call stack or undo", ["call stack", "undo", "backtracking", "return address", "depth first"]),
            MP("Gives a valid queue use such as a print spooler or scheduling", ["print", "spooler", "buffer", "scheduling", "breadth first"]),
        ], "A stack operates on a last in first out basis, so the most recently pushed item is the first one removed by a pop, and only the top of the stack is directly accessible. A queue operates on a first in first out basis, so items are dequeued in the order they were added and access is at both ends, adding at the rear and removing from the front. A stack is used for the call stack in a running program, where each function call pushes a return address and local variables that must be restored in exactly the reverse order as calls return, and it is equally the natural structure for undo functionality. A queue is used for a print spooler, where jobs must be printed in the order they were submitted so that no user is unfairly delayed by someone who submitted later.",
           command="Explain"),
        EQ("Compare an array and a linked list.", 6, [
            MP("An array occupies contiguous memory, a linked list does not", ["contiguous", "adjacent", "anywhere", "scattered"]),
            MP("An array has a fixed size, a linked list can grow and shrink dynamically", ["fixed size", "dynamic", "grow", "shrink"]),
            MP("Array elements are accessed directly by index in constant time", ["direct", "index", "constant time", "immediately", "calculated"]),
            MP("A linked list must be traversed from the start, so access is slower", ["traverse", "from the start", "sequential", "slower", "follow pointers"]),
            MP("Inserting into the middle of an array requires shifting subsequent elements", ["shift", "move", "subsequent", "every element after"]),
            MP("Inserting into a linked list only requires changing pointers", ["pointers", "change two", "reassign", "no shifting"]),
        ], "An array stores its elements in a contiguous block of memory, all of the same type and size, which allows the address of any element to be calculated directly from the base address and the index, giving constant time access to any position. Its size is fixed when it is created, so it cannot grow, and inserting an element into the middle requires every subsequent element to be shifted one position along, which on a large array is extremely expensive. A linked list stores each element in a node that may be located anywhere in memory, together with a pointer to the next node, so the list can grow and shrink at run time as nodes are created and destroyed. The cost of that flexibility is access time: there is no way to calculate the address of the nth item, so the list must be traversed from the head following pointers, which takes time proportional to the position. In exchange, inserting or deleting in the middle requires only that two pointers be reassigned, with no data movement at all. Each node also carries the memory overhead of its pointer, which an array does not. The choice therefore depends on the workload: arrays suit data that is read by index and rarely restructured, while linked lists suit data that is frequently inserted into and removed from.",
           command="Compare"),
        EQ("Explain how a hash table achieves constant time lookup and describe one method of resolving collisions.", 5, [
            MP("A hash function converts the key into an array index", ["hash function", "index", "converts", "maps"]),
            MP("The item is stored at and retrieved from that index directly", ["directly", "that index", "no searching", "immediately"]),
            MP("No search of the structure is required, so lookup time does not depend on the number of items", ["no search", "does not depend", "regardless of size", "constant"]),
            MP("A collision occurs when two keys hash to the same index", ["collision", "same index", "two keys"]),
            MP("Describes chaining or linear probing as a resolution method", ["chaining", "linked list", "probing", "next free slot", "open addressing"]),
        ], "A hash table achieves fast lookup by applying a hash function to the key, which deterministically converts it into an index within the underlying array. The item is stored at that index when inserted, and on retrieval the same hash function is applied to the search key to produce the same index, so the item is found by a single direct array access without searching any part of the structure. Because the position is calculated rather than searched for, the time taken does not grow as the number of stored items increases, giving average constant time performance. A collision occurs when two different keys produce the same index. One resolution method is separate chaining, in which each slot in the array holds a linked list rather than a single item, and any keys hashing to that slot are appended to its list. Lookup then hashes to the slot and searches only that short list, and performance degrades gracefully as the table fills. The alternative, linear probing, stores the colliding item in the next free slot instead, which avoids extra structures but tends to produce clusters of occupied slots that lengthen future searches.",
           command="Explain"),
        EQ("A program must repeatedly find a customer record by their unique customer ID from several million records. Recommend a data structure and justify your choice.", 5, [
            MP("Recommends a hash table", ["hash table", "hash", "dictionary"]),
            MP("The customer ID is a unique key suited to hashing", ["unique", "key", "id", "suited"]),
            MP("The hash function calculates the position so no search is needed", ["calculates", "no search", "direct", "index"]),
            MP("Lookup is average constant time regardless of the number of records", ["constant", "regardless", "does not grow", "same speed", "millions"]),
            MP("Compares favourably with alternatives such as a linear search or a tree", ["linear search", "binary search", "tree", "slower", "log n", "compared"]),
        ], "A hash table is the right structure here. Each customer has a unique ID, which is precisely the kind of key a hash table is designed around, and the required operation is repeated lookup by that key rather than ordered traversal or range queries. The hash function converts the customer ID directly into an array index, so the record is retrieved by a single array access with no searching whatsoever, and crucially the time taken does not grow as the number of records increases, so retrieval from ten million records is essentially as fast as from ten. The alternatives are markedly worse for this workload. A linear search through an unsorted array would examine on average half of the several million records for every lookup, which is completely impractical at any volume of queries. A binary search tree would give logarithmic performance, requiring around twenty three comparisons for eight million records, which is far better than linear but still substantially slower than a single calculated access, and it would degrade badly if the IDs happened to be inserted in sorted order. The hash table's costs are that it does not maintain any useful ordering and that performance depends on a good hash function and on rehashing when the load factor rises, but since the requirement is purely lookup by unique key, neither of those is a meaningful drawback.",
           command="Justify"),
        EQ("Explain the difference between an adjacency matrix and an adjacency list, and state when each is preferable.", 4, [
            MP("An adjacency matrix is a two dimensional array recording whether each pair of vertices is connected", ["two dimensional", "matrix", "array", "each pair", "grid"]),
            MP("An adjacency list stores for each vertex a list of the vertices it connects to", ["list", "each vertex", "neighbours", "connected to"]),
            MP("A matrix uses space proportional to the square of the number of vertices regardless of edges", ["n squared", "square", "regardless", "wastes", "even with few edges"]),
            MP("A list is preferable for sparse graphs and a matrix for dense graphs or frequent edge checks", ["sparse", "dense", "few edges", "many edges", "checking an edge"]),
        ], "An adjacency matrix represents a graph as a two dimensional array in which the entry at row i and column j records whether an edge exists from vertex i to vertex j, and in a weighted graph holds the weight of that edge. An adjacency list instead stores, for each vertex, a list of the vertices it is directly connected to. The essential difference is space. A matrix requires storage proportional to the square of the number of vertices whether or not the edges exist, so a graph of ten thousand vertices needs a hundred million entries even if only a few thousand edges are present. An adjacency list uses space proportional to the number of edges actually present. A matrix is therefore preferable for dense graphs, where most possible edges exist so little space is wasted, and where the ability to check whether a specific edge exists in constant time matters. An adjacency list is preferable for sparse graphs, which is the far more common case in practice, since real road networks, social networks and dependency graphs all have far fewer edges than the theoretical maximum.",
           command="Explain"),
    ],
)

A_LEGAL = Topic(
    slug="legal-moral-and-ethical-issues",
    title="Legal, Moral, Cultural and Ethical Issues",
    spec="1.5",
    icon="i-scales",
    minutes=30,
    blurb="The five acts you must name, the ethical frameworks that make an argument rigorous, and how to structure the extended response so it reaches the top level.",
    fact="The Computer Misuse Act was passed in 1990 after two hackers who broke into Prestel, including the Duke of Edinburgh's mailbox, were acquitted because no existing law actually covered what they had done.",
    sections=[
        Section("Legislation", """
### Data Protection Act 2018

Implements GDPR in UK law. Personal data must be processed lawfully, fairly and transparently, collected for specified purposes, adequate and limited to what is necessary, accurate, kept no longer than necessary, and kept secure.

Individual rights include access, rectification, erasure, restriction of processing, portability and objection. Organisations must report serious breaches to the Information Commissioner within 72 hours.

### Computer Misuse Act 1990

1. Unauthorised access to computer material
2. Unauthorised access with intent to commit or facilitate further offences
3. Unauthorised acts with intent to impair, or recklessness as to impairing, the operation of a computer

The third offence covers denial of service attacks and the deliberate spreading of malware.

### Copyright, Designs and Patents Act 1988

Protects intellectual property including software, music, film, images and writing. Note the distinction: **copyright** protects the expression of an idea and arises automatically, while a **patent** protects an invention and must be applied for.

**Open source** licensing gives users the right to view, modify and redistribute the source, sometimes with a copyleft requirement that derived works remain open. **Proprietary** licensing restricts users to running the compiled program.

### Regulation of Investigatory Powers Act 2000

Governs the interception of communications and surveillance by public bodies. It permits monitoring under specified conditions and requires authorisation, and it is significant to computing because it defines when providers can be compelled to assist.

### Wireless Telegraphy Act 2006 and Freedom of Information Act 2000

The former regulates the radio spectrum and makes unauthorised use of a wireless network an offence. The latter gives a right to request information held by public authorities.
"""),
        Section("Ethics and writing the extended answer", """
### Frameworks that make an argument rigorous

- **Consequentialism.** Judge an action by its outcomes. A system is justified if the total benefit exceeds the total harm. The difficulty is that outcomes are uncertain and it can justify harming a minority for the majority.
- **Deontology.** Judge an action against duties and rights, regardless of outcome. Some things are wrong even if they produce good results, such as reading private messages without consent.
- **Virtue ethics.** Ask what a person of good character would do, focusing on honesty, responsibility and care.

Naming a framework and applying it turns an opinion into an argument, which is what the top mark band requires.

### The recurring themes

- **Automation and employment.** Jobs are removed and created, but rarely in the same places or requiring the same skills, so the costs and benefits fall on different people.
- **Algorithmic decision making.** Systems trained on historical data reproduce historical bias while appearing objective. Accountability is unclear when nobody can explain a decision.
- **Privacy and surveillance.** Individually harmless data points combine into a detailed picture of a person's life.
- **The digital divide.** Moving services online excludes those without access, who are frequently those most dependent on the services.
- **Environmental cost.** Manufacturing, energy consumption and e-waste, weighed against reduced travel and more efficient systems.
- **Censorship and free expression.** Who decides what is removed, and by what process.
- **Intellectual property in the age of AI.** Whether training a model on copyrighted work is fair use, and who owns what a model generates.

### Structuring the extended response

The high mark questions are levels marked, so the structure matters as much as the content.

1. **One sentence of context.** Identify what is at stake and who is affected.
2. **Three developed paragraphs.** Each takes one issue, states the point, explains the mechanism, names the specific group affected and acknowledges the counterargument.
3. **A conclusion that decides.** Give a judgement with a reason, and where appropriate a condition under which your view would change.

!key What separates the top band :: Development, balance and a supported conclusion. Eight separate assertions score in the bottom band. Three fully developed arguments with a genuine counterpoint and a reasoned conclusion score in the top one.

### A worked opening

*An employer introduces software that monitors every keystroke made by employees working from home.*

"The central tension here is between an employer's legitimate interest in verifying that work is being done and an employee's reasonable expectation of privacy in their own home. Legally the employer is not necessarily prohibited from monitoring, but under the Data Protection Act 2018 any such processing must be lawful, proportionate and transparent, which means covert keystroke logging would almost certainly be unlawful and even disclosed monitoring must be limited to what is genuinely necessary rather than gathering everything possible. Ethically, a deontological analysis is unfavourable to the employer: keystroke logging captures private messages, medical searches and banking activity conducted on the same device, and the fact that some of this is incidental does not remove the intrusion, because employees have a right to privacy that does not depend on whether the employer intends to exercise it. A consequentialist analysis is more finely balanced, since productivity gains are real, but the evidence suggests surveillance corrodes trust..."

Notice that each sentence does work: it names the framework, applies it to this scenario, identifies the specific harm, and anticipates the counterargument.
"""),
    ],
    keyterms=[
        ("Data Protection Act 2018", "UK legislation implementing GDPR and governing the processing of personal data."),
        ("Computer Misuse Act 1990", "Legislation creating offences of unauthorised access to and impairment of computer systems."),
        ("Copyright, Designs and Patents Act 1988", "Legislation protecting intellectual property including software."),
        ("Regulation of Investigatory Powers Act 2000", "Legislation governing interception of communications and surveillance by public bodies."),
        ("Patent", "Legal protection for an invention, which must be applied for, unlike copyright."),
        ("Open source licence", "A licence granting the right to view, modify and redistribute source code."),
        ("Consequentialism", "Judging an action by whether its outcomes produce more benefit than harm."),
        ("Deontology", "Judging an action against duties and rights rather than by its outcomes."),
        ("Algorithmic bias", "Systematic unfairness in automated decisions, usually inherited from the training data."),
        ("Digital divide", "The gap between those with reliable access to technology and those without."),
    ],
    grade="""
+ Name the correct act with its year for any scenario, without hesitation
+ Distinguish copyright, which is automatic, from a patent, which must be applied for
+ Name and apply at least one ethical framework rather than simply asserting a view
+ Identify the specific group affected in every paragraph, never just people in general
+ Always acknowledge the strongest counterargument, then say why you still hold your position
+ End with a judgement and, where you can, the condition that would change it
""",
    mistakes=[
        "Listing impacts without developing any of them, which caps the answer in the bottom band.",
        "Writing a one sided answer, which cannot reach the top band however correct it is.",
        "Confusing the Computer Misuse Act with the Copyright Act.",
        "Saying copyright must be registered. It arises automatically. Patents must be applied for.",
        "Omitting a conclusion, which loses marks even after a strong discussion.",
        "Asserting an opinion with no framework or reasoning behind it.",
    ],
    quiz=[
        Q("Which act makes a denial of service attack an offence?",
          ["Computer Misuse Act 1990", "Data Protection Act 2018",
           "Copyright, Designs and Patents Act 1988", "Regulation of Investigatory Powers Act 2000"], 0,
          "The third offence covers unauthorised acts intended to impair the operation of a computer."),
        Q("What is the difference between copyright and a patent?",
          ["Copyright arises automatically and protects expression, a patent must be applied for and protects an invention",
           "A patent is automatic and copyright must be registered",
           "They are the same thing", "Copyright applies only to music"], 0,
          "This distinction is worth a mark on its own and is frequently confused."),
        Q("Under the Data Protection Act 2018, how quickly must a serious breach be reported?",
          ["Within 72 hours", "Within 24 hours", "Within one month", "There is no requirement"], 0,
          "Reporting to the Information Commissioner within 72 hours is a specific statutory obligation."),
        Q("What does consequentialism judge an action by?",
          ["Its outcomes and whether benefit exceeds harm", "Whether it respects rights and duties",
           "What a person of good character would do", "Whether it is legal"], 0,
          "Its weakness is that it can justify harming a minority when the aggregate benefit is large."),
        Q("Why can an algorithm trained on historical data produce biased decisions?",
          ["It reproduces the patterns in that data, including past discrimination",
           "The programmers introduced bias deliberately",
           "Algorithms cannot process certain data types",
           "Bias is added during compilation"], 0,
          "The output appears objective precisely because it is mathematical, which makes it more likely to be trusted."),
        Q("Which act would be relevant to an employer intercepting employee communications?",
          ["Regulation of Investigatory Powers Act 2000", "Copyright, Designs and Patents Act 1988",
           "Wireless Telegraphy Act 2006", "Freedom of Information Act 2000"], 0,
          "It governs interception and surveillance, alongside data protection obligations."),
        Q("What is a copyleft licence?",
          ["An open source licence requiring derived works to remain open",
           "A licence prohibiting all modification", "A licence for images only",
           "A licence granted by a patent office"], 0,
          "It uses copyright law itself to guarantee that freedoms are preserved downstream."),
        Q("Which is the strongest structure for an eight mark discussion question?",
          ["Three developed arguments with counterpoints and a reasoned conclusion",
           "Eight separate points listed briefly",
           "Only the advantages, argued forcefully",
           "A definition followed by a list of laws"], 0,
          "Levels marking rewards development, balance and a supported judgement, not the number of points."),
        Q("A deontological objection to workplace surveillance would argue that:",
          ["Employees have a right to privacy regardless of any productivity benefit",
           "The productivity gain outweighs the intrusion",
           "It depends entirely on the outcome",
           "Surveillance is efficient"], 0,
          "Deontology judges the action against rights and duties rather than by its consequences."),
        Q("The digital divide is a concern when services move online because:",
          ["Those without reliable access are excluded, and they are often those most in need",
           "Websites are expensive to build", "Online services are always slower",
           "It breaches the Computer Misuse Act"], 0,
          "The groups least likely to have access frequently overlap with those most dependent on public services."),
    ],
    exam=[
        EQ("State two rights that the Data Protection Act 2018 gives to individuals.", 2, [
            MP("The right to access the personal data held about them", ["access", "see", "obtain a copy", "subject access"]),
            MP("The right to have inaccurate data corrected, or erased in certain circumstances", ["rectification", "corrected", "erasure", "deleted", "removed"]),
        ], "Individuals have the right of access, meaning they can request and receive a copy of the personal data an organisation holds about them, together with information about how and why it is being processed. They also have the right to rectification, requiring inaccurate data to be corrected, and in certain circumstances the right to erasure, requiring their data to be deleted.",
           command="State"),
        EQ("Explain the difference between copyright and a patent.", 3, [
            MP("Copyright protects the expression of an idea such as code, text or music", ["expression", "code", "text", "music", "creative work"]),
            MP("Copyright arises automatically as soon as the work is created", ["automatic", "as soon as", "no registration", "immediately"]),
            MP("A patent protects an invention or process and must be formally applied for", ["invention", "process", "applied for", "registered", "granted"]),
        ], "Copyright protects the particular expression of an idea, such as the source code a programmer writes, a piece of music or a photograph, and it arises automatically the moment the work is created in a fixed form, with no need to register or apply for anything. A patent protects an invention or a novel technical process rather than an expression of it, and it does not arise automatically: an application must be made, examined and granted, and the invention must be genuinely new and non obvious. The distinction matters in software because the code itself is protected by copyright as soon as it is written, whereas an underlying algorithm or technique may in some jurisdictions be patentable, which is a separate and far more contested question.",
           command="Explain"),
        EQ("An insurance company uses a machine learning system trained on twenty years of its own decisions to determine premiums. Discuss the ethical issues raised.", 8, [
            MP("The system learns patterns from historical data", ["historical", "past data", "learns", "trained on"]),
            MP("Past decisions may contain discrimination which the system reproduces", ["discrimination", "bias", "reproduces", "repeats", "unfair"]),
            MP("The output appears objective because it comes from a computer, so it is trusted more", ["objective", "appears", "trusted", "neutral", "mathematical"]),
            MP("Names a group likely to be disadvantaged", ["postcode", "ethnicity", "disability", "age", "low income", "gender", "area"]),
            MP("Accountability is unclear when no one can explain an individual decision", ["accountability", "explain", "who is responsible", "opaque", "black box"]),
            MP("Recognises legitimate benefits such as consistency, speed and better risk pricing", ["consistent", "faster", "accurate", "efficient", "cheaper", "benefit"]),
            MP("Applies an ethical framework or gives a genuine counterargument", ["deontological", "consequentialist", "however", "on the other hand", "against this", "rights"]),
            MP("Reaches a supported conclusion with a safeguard or recommendation", ["conclusion", "should", "recommend", "audit", "human review", "transparency", "overall"]),
        ], "The central issue is that a system trained on twenty years of the company's own decisions learns the patterns present in those decisions, and it cannot distinguish patterns that reflect genuine risk from patterns that reflect historical unfairness. If past underwriters systematically quoted higher premiums to applicants from particular postcodes, and those postcodes correlate strongly with ethnicity or income, the system will reproduce that behaviour faithfully while never being told to consider ethnicity at all, because a proxy variable carries the information. The harm is compounded by how the output is perceived: a decision produced by an algorithm appears objective and mathematical, so it is scrutinised far less than an equivalent human judgement would be, and an applicant who suspects unfairness has no visible decision to challenge. This connects directly to accountability. If nobody at the company can explain why a particular applicant was quoted a particular premium, then in practice no one is answerable for it, and both regulators and the applicant are left unable to test whether the decision was lawful. A deontological analysis is unfavourable here: applicants have a right to be assessed on their own circumstances rather than on statistical associations with people who share an incidental characteristic, and that right does not depend on whether the aggregate outcome is efficient. The benefits are nonetheless real and should not be dismissed. An automated system applies the same criteria to every applicant, removing the inconsistency and individual prejudice of human underwriters having a bad day, it produces decisions in seconds rather than days, and more accurate risk pricing genuinely can reduce premiums for lower risk customers who were previously overcharged by cruder models. A consequentialist would weigh these gains seriously. On balance the company should not deploy the system in the form described. The defensible position is to use it, but with specific safeguards: auditing outputs for disparate impact across protected characteristics rather than only checking that such characteristics are absent from the inputs, requiring that every decision can be explained in terms an applicant would understand, retaining human review for any decision the model is uncertain about or that falls outside normal ranges, and retraining on data that has itself been examined for historical bias. Without those, the system does not remove human prejudice, it automates it and removes the ability to see it.",
           command="Discuss"),
        EQ("Explain why the Computer Misuse Act 1990 was necessary.", 3, [
            MP("Before it, unauthorised access to a computer was not clearly a criminal offence", ["not an offence", "no law", "not covered", "not illegal"]),
            MP("Existing laws such as those on theft and criminal damage did not apply to data", ["theft", "criminal damage", "did not apply", "physical", "existing law"]),
            MP("Prosecutions failed, so specific legislation was introduced", ["prosecution failed", "acquitted", "could not convict", "needed a new law"]),
        ], "Before 1990 there was no offence in UK law that clearly covered gaining access to a computer system without permission. The existing legislation had been written for a physical world: theft required an intention to permanently deprive someone of property, and criminal damage required damage to tangible property, neither of which fitted a situation where data had been read or copied but nothing physical had been taken or broken. This became untenable when prosecutions of individuals who had demonstrably broken into systems collapsed because no applicable offence could be identified. The Computer Misuse Act was passed to close that gap, creating specific offences of unauthorised access, unauthorised access with intent to commit a further offence, and unauthorised acts intended to impair the operation of a computer, the last of which now covers denial of service attacks and the deliberate distribution of malware.",
           command="Explain"),
        EQ("Explain what is meant by algorithmic bias and describe one way an organisation could reduce it.", 4, [
            MP("Systematic unfairness in the decisions an automated system produces", ["systematic", "unfair", "biased outcomes", "disadvantages"]),
            MP("It usually arises from the training data rather than from deliberate intent", ["training data", "not deliberate", "unintentional", "data", "not intended"]),
            MP("Because the system learns and reproduces patterns present in that data", ["reproduces", "learns", "patterns", "repeats"]),
            MP("Describes a mitigation such as auditing outputs, diversifying training data or requiring explainability", ["audit", "diverse data", "representative", "explainable", "human review", "testing"]),
        ], "Algorithmic bias is systematic unfairness in the decisions produced by an automated system, where particular groups are consistently disadvantaged relative to others. It normally arises not from any deliberate intent by the developers but from the training data, because a machine learning system finds and reproduces whatever patterns exist in the examples it is shown. If that data is unrepresentative, or if it records past decisions that were themselves discriminatory, the system learns those patterns and applies them to new cases while appearing entirely neutral. One effective mitigation is regular auditing of outputs for disparate impact: rather than only checking that protected characteristics are absent from the inputs, which is inadequate because proxy variables carry the same information, the organisation measures whether outcomes differ significantly across groups and investigates any disparity it finds. This should be combined with requiring that decisions be explainable, so that an individual affected can be told why a decision was reached and can challenge it.",
           command="Explain"),
    ],
)

A_THINKING = Topic(
    slug="elements-of-computational-thinking",
    title="Elements of Computational Thinking",
    spec="2.1",
    icon="i-brain",
    minutes=26,
    blurb="Thinking abstractly, ahead, procedurally, logically and concurrently, applied to real problems rather than defined in isolation.",
    fact="Caching, precomputation and lookup tables are all the same idea: thinking ahead. Work out in advance what you will need, so that at the moment you need it the answer is already there.",
    sections=[
        Section("Abstractly, ahead and procedurally", """
### 2.1.1 Thinking abstractly

**Abstraction** is removing detail that is not relevant to the problem.

- **Representational abstraction.** Remove detail until only what is needed remains, as a Tube map removes real distances and everything above ground.
- **Abstraction by generalisation.** Group things by shared characteristics so one solution serves many cases, as a Vehicle class serves cars, lorries and vans.

Distinguish the **reality** from the **model**. A model is always simpler than what it represents, which is exactly why it is useful and exactly why it can mislead. A traffic simulation that assumes every driver behaves rationally will not predict real congestion.

### 2.1.2 Thinking ahead

Identifying in advance what will be needed.

- **Inputs and outputs** determined before design begins
- **Preconditions**: what must be true before a subroutine may be called, such as an array being sorted before a binary search
- **Caching**: storing results likely to be needed again, trading memory for speed
- **Reusable components**: designing so that parts serve future needs as well as present ones

### 2.1.3 Thinking procedurally

**Decomposition** into sub problems, deciding the order in which they must be solved, and identifying which can become reusable subroutines.

A **top down** approach starts with the whole problem and repeatedly divides it. A **bottom up** approach builds small reliable components and assembles them. Real projects use both.
"""),
        Section("Logically and concurrently", """
### 2.1.4 Thinking logically

Identifying the points where a decision is made, the conditions that determine each outcome, and every path through the program.

The discipline is completeness: for every decision, ask what happens in each case, including the boundary and the case nobody expected. Most defects live in the path that was never considered.

Nested conditions, compound conditions using AND and OR, and the correct ordering of conditions all belong here. Boolean algebra and truth tables are the formal tools.

### 2.1.5 Thinking concurrently

Identifying which parts of a problem can be carried out **at the same time**, and which cannot because they depend on earlier results.

**Genuine concurrency** requires multiple processors executing simultaneously. **Apparent concurrency** is a single processor switching between tasks so rapidly that they appear simultaneous.

**Benefits:** the total time falls when independent parts run in parallel, the processor is used more fully, and a system stays responsive while long work continues in the background.

**Costs:**

- Only the parallelisable portion benefits, and **Amdahl's law** caps the gain
- **Data dependencies** force some steps to wait
- **Race conditions** occur when the result depends on the order in which threads happen to access shared data
- **Deadlock** occurs when threads each hold a resource the other needs
- Synchronisation and coordination add overhead, and concurrent code is substantially harder to write, test and debug, because faults may appear only under particular timings

!key When concurrency is worth it :: When the work divides into genuinely independent parts, when the sequential fraction is small, and when the complexity cost is repaid by the time saved. Rendering separate video frames qualifies. Applying a running total does not.
"""),
    ],
    keyterms=[
        ("Abstraction", "Removing detail not relevant to the problem being solved."),
        ("Representational abstraction", "Reducing detail until only what is needed to solve the problem remains."),
        ("Abstraction by generalisation", "Grouping things by shared characteristics so one solution serves many cases."),
        ("Precondition", "A condition that must hold before a subroutine may correctly be called."),
        ("Caching", "Storing results likely to be needed again, trading memory for speed."),
        ("Decomposition", "Breaking a problem into smaller sub problems that can be solved separately."),
        ("Concurrency", "Carrying out parts of a problem at the same time, or appearing to."),
        ("Race condition", "A fault where the outcome depends on the unpredictable order in which threads access shared data."),
        ("Deadlock", "A state where threads each hold a resource another needs, so none can proceed."),
    ],
    grade="""
+ Apply each element to the scenario in the question rather than defining it
+ Distinguish representational abstraction from abstraction by generalisation with an example of each
+ State a precondition precisely, such as the array must be sorted in ascending order
+ Identify both what can be done concurrently and what cannot, with the dependency that prevents it
+ Give at least three costs of concurrency, including race conditions
""",
    mistakes=[
        "Defining the terms rather than applying them to the scenario.",
        "Confusing abstraction with decomposition. Abstraction removes detail, decomposition splits the problem.",
        "Saying concurrency always makes a program faster.",
        "Omitting race conditions and deadlock when asked for the difficulties of concurrency.",
        "Failing to identify the dependency that prevents two tasks running in parallel.",
    ],
    quiz=[
        Q("What is abstraction by generalisation?",
          ["Grouping things by shared characteristics so one solution serves many cases",
           "Removing all detail from a problem", "Splitting a problem into parts",
           "Storing results for later reuse"], 0,
          "A Vehicle class serving cars, vans and lorries is generalisation. A Tube map is representational abstraction."),
        Q("What is a precondition?",
          ["Something that must be true before a subroutine can correctly be called",
           "The first line of a program", "A condition inside a loop",
           "The result a subroutine returns"], 0,
          "A binary search has the precondition that the array is already sorted."),
        Q("Caching is an example of which element of computational thinking?",
          ["Thinking ahead", "Thinking logically", "Thinking concurrently", "Thinking abstractly"], 0,
          "Results likely to be needed again are stored in advance, trading memory for speed."),
        Q("What is a race condition?",
          ["The outcome depends on the unpredictable order in which threads access shared data",
           "Two programs competing for processor time",
           "A loop that runs too quickly", "A deadlock between two threads"], 0,
          "It is particularly difficult to debug because the fault may appear only under specific timings."),
        Q("Why can a model mislead?",
          ["It is necessarily simpler than the reality it represents",
           "Models are always mathematically wrong", "Models cannot be tested",
           "Models require too much processing"], 0,
          "The simplification that makes a model useful is the same thing that limits what it can predict."),
        Q("Which task is genuinely suitable for concurrent execution?",
          ["Rendering separate frames of a video", "Calculating a running total",
           "Following a linked list", "Applying a series of dependent transformations"], 0,
          "Independent frames have no data dependency, so each can be computed without waiting for the others."),
        Q("What distinguishes genuine concurrency from apparent concurrency?",
          ["Genuine concurrency requires multiple processors executing at the same time",
           "Apparent concurrency is faster", "Genuine concurrency uses less memory",
           "There is no difference"], 0,
          "Apparent concurrency is one processor switching between tasks fast enough to look simultaneous."),
        Q("What is deadlock?",
          ["Threads each hold a resource another needs, so none can proceed",
           "A thread that never starts", "A loop with no exit condition",
           "Two threads reading the same value"], 0,
          "It is a classic hazard of lock based concurrency control."),
        Q("Thinking logically primarily involves:",
          ["Identifying decision points and the conditions determining each outcome",
           "Removing unnecessary detail", "Running tasks in parallel",
           "Storing results for reuse"], 0,
          "Completeness matters: every path, including the boundary case, must be considered."),
        Q("A top down approach to a problem means:",
          ["Starting with the whole problem and repeatedly dividing it",
           "Building small components first and assembling them",
           "Writing the user interface first", "Testing before designing"], 0,
          "Bottom up is the opposite, and real projects usually combine the two."),
    ],
    exam=[
        EQ("Explain the difference between representational abstraction and abstraction by generalisation.", 4, [
            MP("Representational abstraction removes detail until only what is needed remains", ["removes detail", "only what is needed", "simplify", "reduce"]),
            MP("Gives an example such as a map or a model", ["map", "underground", "tube", "model", "diagram"]),
            MP("Abstraction by generalisation groups things by shared characteristics", ["group", "shared", "common", "categorise", "similar"]),
            MP("Gives an example such as a superclass serving several subclasses", ["superclass", "class", "vehicle", "inheritance", "general"]),
        ], "Representational abstraction is the process of removing detail from a situation until only the information needed to solve the problem remains. A map of the London Underground is the classic example: it discards real distances, geographic direction and everything above ground, keeping only the order of stations and where lines interchange, which is precisely what a passenger needs and nothing more. Abstraction by generalisation instead groups different things together according to characteristics they share, so that one solution can serve all of them. Defining a Vehicle class with attributes and methods common to cars, vans and lorries is an example, since code written to work with Vehicle then works for every kind of vehicle without being rewritten for each.",
           command="Explain"),
        EQ("Explain what is meant by a precondition and give an example.", 3, [
            MP("A condition that must be true before a subroutine is called for it to work correctly", ["must be true", "before", "called", "correctly", "assumption"]),
            MP("Gives a valid example such as a sorted array for binary search", ["sorted", "binary search", "not empty", "positive", "example"]),
            MP("Explains that if it is not met the result is incorrect or the program fails", ["incorrect", "fails", "wrong result", "crash", "undefined"]),
        ], "A precondition is a statement that must be true before a subroutine is called if that subroutine is to work correctly. It documents an assumption the subroutine makes rather than checks. For example, a binary search has the precondition that the array passed to it is already sorted in ascending order, because the algorithm decides which half to discard on the assumption that everything to the left of the midpoint is smaller. If that precondition is not met the search will still run and return a result, but the result will simply be wrong, and no error will be raised to indicate that anything went astray, which is why preconditions must be stated explicitly and guaranteed by the calling code.",
           command="Explain"),
        EQ("Explain the benefits and difficulties of concurrent processing.", 6, [
            MP("Independent parts of a task can be executed at the same time", ["at the same time", "simultaneously", "parallel", "independent"]),
            MP("The total execution time is reduced and processor resources are used more fully", ["reduced", "faster", "less time", "fully used", "utilisation"]),
            MP("A system can remain responsive while long work continues in the background", ["responsive", "background", "interface", "while", "user"]),
            MP("Only the parallelisable portion benefits, and Amdahl's law limits the gain", ["amdahl", "sequential portion", "limits", "ceiling", "fraction"]),
            MP("Race conditions can occur where the result depends on the timing of access to shared data", ["race condition", "timing", "shared data", "order", "unpredictable"]),
            MP("Deadlock and synchronisation overhead make concurrent code harder to write and debug", ["deadlock", "synchronisation", "overhead", "harder", "debug", "test"]),
        ], "The benefit of concurrent processing is that parts of a task which do not depend on one another can be executed at the same time rather than one after another, so the total elapsed time falls and the available processing resources are used far more fully. Rendering the separate frames of an animation is a clear case, since each frame can be computed entirely independently. Concurrency also allows a system to stay responsive, running a long calculation on one thread while the user interface continues to react on another. The difficulties are substantial. Only the portion of the work that can genuinely be divided benefits, and Amdahl's law states that whatever fraction must remain sequential sets a hard ceiling on the achievable speedup regardless of how many processors are added. Data dependencies limit division further, since a step requiring the result of an earlier one cannot begin until that step has finished. Where threads share data, race conditions become possible: if two threads read, modify and write the same value without proper synchronisation, the final result depends on the order in which their operations happen to interleave, and the fault may appear only occasionally and only under particular timings, which makes it exceptionally difficult to reproduce and diagnose. Preventing this with locks introduces the risk of deadlock, where two threads each hold a resource the other is waiting for so neither can continue. Finally, the synchronisation itself consumes time, and concurrent code is significantly harder to write, test and reason about than sequential code, so the complexity cost must be genuinely repaid by the time saved.",
           command="Explain"),
        EQ("A program processes a large set of images, applying the same filter to each one, and then produces a single report summarising all of them. Explain which parts of this could be executed concurrently and which could not.", 4, [
            MP("Applying the filter to each image is independent so images can be processed concurrently", ["independent", "each image", "concurrently", "in parallel", "at the same time"]),
            MP("No image's result depends on any other image", ["does not depend", "no dependency", "separate", "unrelated"]),
            MP("Producing the summary report cannot begin until all images are processed", ["cannot begin", "after", "all images", "waits", "depends on"]),
            MP("The report is a data dependency, forcing that part to be sequential", ["dependency", "sequential", "must wait", "combine", "aggregate"]),
        ], "Applying the filter to the images is an ideal candidate for concurrent execution, because each image is processed entirely independently of every other one. Nothing about filtering image five depends on the outcome of filtering image four, so the set can be divided between as many threads or processors as are available, and the total time for that stage falls roughly in proportion to the number of workers used. Producing the summary report is different. It aggregates information drawn from every image, so it cannot begin until every image has been processed, which makes it a data dependency that forces the program back into sequential execution at that point. In practice the report generation itself is also likely to be a single sequential operation, and it is precisely this kind of unavoidable sequential section that Amdahl's law identifies as the limit on the overall speedup achievable.",
           command="Explain"),
        EQ("Explain why a computational model of a real world system may produce inaccurate predictions.", 3, [
            MP("A model is necessarily a simplification of the reality", ["simplification", "simpler", "not complete", "abstraction"]),
            MP("Detail judged irrelevant is removed, but it may turn out to matter", ["removed", "omitted", "left out", "may matter", "irrelevant"]),
            MP("Assumptions made in the model may not hold in reality", ["assumptions", "may not hold", "unrealistic", "does not behave"]),
        ], "A computational model is by definition a simplification of the system it represents, since a model containing every detail of reality would be as complex as reality itself and therefore useless. Building it requires choosing which details are relevant and discarding the rest, and the accuracy of the model depends entirely on whether those choices were right. Detail that was judged irrelevant may in fact influence the outcome, and factors omitted altogether cannot be predicted at all. Beyond omission, models rest on assumptions about how the system behaves, and those assumptions may simply not hold: a traffic model assuming every driver chooses the objectively fastest route will underestimate congestion, because real drivers act on habit and incomplete information. The model can therefore be internally correct and still produce predictions that do not match what actually happens.",
           command="Explain"),
    ],
)

A_PROGTECH = Topic(
    slug="programming-techniques-and-methods",
    title="Programming Techniques and Computational Methods",
    spec="2.2",
    icon="i-code",
    minutes=34,
    blurb="Recursion, parameter passing, scope, IDE features, and every computational method on the specification with when each applies.",
    fact="Every recursive algorithm can be written iteratively and every iterative one recursively. The choice is about which one expresses the problem more clearly, and about whether you can afford the stack.",
    sections=[
        Section("Programming techniques", """
### Recursion

A subroutine that calls itself. Every recursive solution needs:

1. A **base case** that returns without recursing, stopping the process
2. A **general case** that calls itself with input moving towards the base case

```python
def factorial(n):
    if n <= 1:          # base case
        return 1
    return n * factorial(n - 1)      # general case
```

Each call adds a **stack frame** holding parameters, local variables and the return address. Too many nested calls exhaust the stack, producing a **stack overflow**.

| | Recursion | Iteration |
| Expressiveness | Very natural for tree and graph problems, and divide and conquer | Natural for repeated sequential work |
| Memory | A stack frame per call, so memory grows with depth | Constant |
| Speed | Slower, because of call overhead | Faster |
| Risk | Stack overflow if the depth is large or the base case is wrong | Infinite loop if the condition is never met |

Use recursion where the problem is genuinely recursive: tree traversal, merge sort, quicksort, depth first search, and the Tower of Hanoi.

### Parameter passing

- **By value.** A copy is passed. Changes inside the subroutine do not affect the original. Safer, but copying a large structure costs memory and time.
- **By reference.** The memory address is passed. Changes inside the subroutine do affect the original. Efficient for large structures, and it allows several values to be returned, but it makes side effects possible.

### Scope and lifetime

**Scope** is where an identifier can be accessed. **Lifetime** is how long it exists in memory. A local variable is scoped to its subroutine and lives only while that subroutine runs. A global is accessible everywhere and persists for the whole program.

Prefer local. Global variables can be changed from anywhere, which makes a fault extremely hard to trace, and they prevent a subroutine from being reasoned about in isolation.

### IDE features

Editor with syntax highlighting and auto complete, error diagnostics identifying the line and type, a run time environment, a translator, debugging tools including **breakpoints**, **stepping** and **variable watches**, refactoring tools, version control integration and automated test running.
"""),
        Section("Computational methods", """
### Problem recognition

Some problems are amenable to computational solution and some are not. The question is whether the problem can be defined precisely, whether the necessary data is available, whether the rules can be stated explicitly, and whether the solution can be computed within acceptable time and resources.

### Divide and conquer

Repeatedly split the problem into smaller instances of the same problem, solve those, and combine the results. Merge sort, quicksort and binary search all work this way. It reduces complexity substantially, typically from O(n^2^) to O(n log n).

### Abstraction by generalisation

Grouping problems that share a structure so one solution serves all of them.

### Backtracking

Explore a path, and when it proves not to lead to a solution, return to the last decision point and try a different option. Used for maze solving, constraint problems such as sudoku, and the eight queens problem.

### Data mining

Searching very large datasets for patterns and relationships not previously known, such as products frequently bought together or early indicators of equipment failure.

### Heuristics

A rule of thumb that produces a good enough solution quickly, where finding the optimal one would take unacceptably long. A satnav uses heuristics to avoid evaluating every possible route. A* uses a heuristic estimate of remaining distance to guide its search. The trade off is that the answer is not guaranteed to be optimal.

### Performance modelling

Simulating a system mathematically to predict how it will behave under load, rather than building it and finding out. Far cheaper than testing the real system, and safe where the real system cannot be experimented on.

### Pipelining

Dividing a process into stages so that different items occupy different stages simultaneously, as in a processor's instruction pipeline or a data processing pipeline.

### Visualisation

Presenting data graphically so patterns invisible in raw figures become apparent. Human pattern recognition on a chart is far faster than reading a table of ten thousand rows.
"""),
    ],
    keyterms=[
        ("Recursion", "A subroutine that calls itself, with a base case that stops the process."),
        ("Base case", "The condition under which a recursive subroutine returns without calling itself again."),
        ("Stack frame", "The record of parameters, local variables and return address created by each subroutine call."),
        ("Stack overflow", "The error occurring when recursion becomes too deep for the available stack space."),
        ("Pass by value", "Passing a copy, so changes inside the subroutine do not affect the original."),
        ("Pass by reference", "Passing the address, so changes inside the subroutine do affect the original."),
        ("Scope", "The region of a program in which an identifier can be accessed."),
        ("Divide and conquer", "Repeatedly splitting a problem into smaller instances of itself and combining the results."),
        ("Backtracking", "Returning to the last decision point when a path fails, and trying an alternative."),
        ("Heuristic", "A rule of thumb producing a good enough solution quickly, without guaranteeing optimality."),
        ("Performance modelling", "Simulating a system to predict its behaviour under load rather than building it."),
        ("Visualisation", "Presenting data graphically so patterns become apparent to a human observer."),
    ],
    grade="""
+ Always identify the base case explicitly when writing or explaining recursion
+ Compare recursion and iteration on memory as well as clarity, naming the stack frame
+ Distinguish pass by value and pass by reference by effect on the original, not just mechanism
+ Give a scenario for every computational method rather than a definition
+ Explain a heuristic as trading optimality for speed, and say when that trade is acceptable
""",
    mistakes=[
        "Writing recursion with no base case, or with one the input never reaches.",
        "Saying recursion is more efficient. It is often clearer but uses more memory and is slower.",
        "Saying pass by reference passes the variable. It passes the address, which is why changes propagate.",
        "Defining a computational method without giving a scenario in which it applies.",
        "Saying a heuristic gives the best answer. It gives a good enough answer quickly.",
    ],
    quiz=[
        Q("What must every recursive subroutine have?",
          ["A base case that returns without recursing", "At least two parameters",
           "A loop inside it", "A global variable"], 0,
          "Without a base case the recursion never terminates and the stack is exhausted."),
        Q("What causes a stack overflow in recursion?",
          ["The recursion goes too deep, exhausting the available stack space",
           "The base case returns too early", "Too many parameters are passed",
           "The subroutine returns the wrong type"], 0,
          "Every call adds a stack frame, so depth is limited by available stack memory."),
        Q("What is the effect of passing a parameter by reference?",
          ["Changes made inside the subroutine affect the original variable",
           "A copy is made so the original is protected",
           "The parameter becomes global", "The subroutine cannot modify it"], 0,
          "The address is passed, so the subroutine operates on the original data."),
        Q("Which algorithm is an example of divide and conquer?",
          ["Merge sort", "Bubble sort", "Linear search", "Insertion sort"], 0,
          "It repeatedly halves the list, sorts the halves and merges them, which is the pattern exactly."),
        Q("What is backtracking used for?",
          ["Returning to the last decision point when a path fails and trying another option",
           "Undoing a user action", "Reversing a linked list", "Restoring from a backup"], 0,
          "Maze solving, sudoku and the eight queens problem all rely on it."),
        Q("What is a heuristic?",
          ["A rule of thumb producing a good enough answer quickly",
           "An algorithm guaranteed to find the optimal answer",
           "A method of encrypting data", "A type of data structure"], 0,
          "The trade is optimality for speed, which is worthwhile when an exhaustive search is impractical."),
        Q("Why is performance modelling useful?",
          ["It predicts behaviour under load without building or risking the real system",
           "It removes the need for testing", "It compresses data",
           "It guarantees the system will work"], 0,
          "It is far cheaper than construction and safe where experimenting on the real system is impossible."),
        Q("When is recursion generally preferable to iteration?",
          ["When the problem is naturally recursive, such as traversing a tree",
           "When memory is very limited", "When maximum speed is required",
           "When the number of repetitions is known"], 0,
          "Tree and graph problems express far more clearly as recursion despite the extra memory cost."),
        Q("What is the main risk of using global variables?",
          ["Any part of the program can change them, making faults very hard to trace",
           "They use more memory than locals", "They cannot hold objects",
           "They are slower to access"], 0,
          "It also prevents a subroutine from being understood or tested in isolation."),
        Q("Data mining is best described as:",
          ["Searching large datasets for previously unknown patterns and relationships",
           "Deleting unnecessary data", "Compressing a database",
           "Encrypting stored records"], 0,
          "Discovering associations nobody looked for is what distinguishes it from ordinary querying."),
    ],
    exam=[
        EQ("Explain what is meant by recursion and state what every recursive subroutine must include.", 3, [
            MP("A subroutine that calls itself", ["calls itself", "own", "itself"]),
            MP("It must include a base case that returns without recursing", ["base case", "stopping condition", "terminating", "without calling"]),
            MP("And a general case moving towards the base case", ["general case", "towards", "moves closer", "smaller", "recursive case"]),
        ], "Recursion is a technique in which a subroutine calls itself in order to solve a smaller instance of the same problem. Every recursive subroutine must contain a base case, which is a condition under which it returns a value directly without calling itself again, since this is what stops the process. It must also contain a general case in which it calls itself with an argument that has moved closer to the base case, guaranteeing that the base case is eventually reached. Without a correct base case, or with a general case that never approaches it, the recursion continues indefinitely until the available stack space is exhausted and a stack overflow occurs.",
           command="Explain"),
        EQ("Compare recursion and iteration as ways of solving a repeated problem.", 5, [
            MP("Recursion is a subroutine calling itself, iteration uses a loop", ["calls itself", "loop", "repeats"]),
            MP("Recursion often expresses tree and divide and conquer problems more naturally", ["natural", "clearer", "tree", "divide and conquer", "elegant"]),
            MP("Each recursive call creates a stack frame, so memory use grows with depth", ["stack frame", "memory", "grows", "each call", "stack"]),
            MP("Iteration uses constant memory and is generally faster", ["constant", "less memory", "faster", "no overhead"]),
            MP("Recursion risks stack overflow where iteration risks an infinite loop", ["stack overflow", "infinite loop", "risk", "crash"]),
        ], "Recursion solves a problem by having a subroutine call itself with a smaller version of the same problem, while iteration solves it by repeating a block of code within a loop. The main advantage of recursion is expressiveness: problems that are themselves recursive in structure, such as traversing a binary tree, sorting by divide and conquer or exploring a graph depth first, translate into remarkably short and clear recursive code, whereas the iterative equivalents require an explicit stack and are considerably harder to follow. The cost is memory and speed. Every recursive call creates a new stack frame holding its parameters, local variables and return address, so memory consumption grows in proportion to the depth of recursion, and if that depth is large the stack is exhausted and the program crashes with a stack overflow. Iteration uses a constant amount of memory regardless of how many times it repeats and avoids the overhead of function calls, so it is generally faster. The failure modes differ correspondingly: badly written recursion overflows the stack, while a badly written loop runs forever. In practice recursion is chosen when it makes the solution genuinely clearer and the depth is bounded, and iteration when performance or memory matters or the depth could be large.",
           command="Compare"),
        EQ("Explain the difference between passing a parameter by value and passing it by reference.", 4, [
            MP("By value a copy of the data is passed to the subroutine", ["copy", "duplicate", "value is copied"]),
            MP("Changes made inside the subroutine do not affect the original", ["do not affect", "original unchanged", "protected", "no effect"]),
            MP("By reference the memory address of the data is passed", ["address", "memory location", "pointer", "reference"]),
            MP("Changes made inside the subroutine do affect the original, and no copy is made so it is efficient for large data", ["affect the original", "changes", "efficient", "no copy", "large"]),
        ], "When a parameter is passed by value, a copy of the data is created and given to the subroutine, so the subroutine works on that copy and any changes it makes are discarded when it returns, leaving the caller's variable untouched. This is safer, because the subroutine cannot produce unexpected side effects, but copying a large data structure such as an array of a million elements costs both time and memory. When a parameter is passed by reference, the memory address of the original data is passed instead, so the subroutine operates directly on the caller's variable and any modification it makes persists after the subroutine returns. This is efficient for large structures, since nothing is copied, and it allows a subroutine to return several results by modifying the variables it was given. The corresponding risk is that changes propagate outwards, so a subroutine can alter data the caller did not expect it to touch, which makes reasoning about the program harder.",
           command="Explain"),
        EQ("Explain what a heuristic is and give an example of a situation where one would be used.", 4, [
            MP("A rule of thumb that produces an acceptable solution quickly", ["rule of thumb", "good enough", "acceptable", "approximation"]),
            MP("It does not guarantee the optimal solution", ["not guaranteed", "not optimal", "may not be best", "approximate"]),
            MP("It is used where finding the optimal solution would take unacceptably long", ["too long", "impractical", "unacceptable", "exhaustive", "computationally"]),
            MP("Gives a valid example such as route finding or the travelling salesman problem", ["satnav", "route", "a star", "travelling salesman", "chess", "pathfinding"]),
        ], "A heuristic is a rule of thumb that guides a search towards a good solution quickly, without guaranteeing that the solution found is the best one available. It is used where finding the genuinely optimal answer would require exploring so many possibilities that the computation would take an unacceptable amount of time, or would be entirely infeasible. Route finding is a clear example. A satnav could in principle evaluate every possible sequence of roads between two points and pick the shortest, but the number of possibilities in a real road network is astronomically large. Instead the A star algorithm uses a heuristic, typically the straight line distance from a node to the destination, to decide which routes look most promising and explore those first, discarding directions that lead away from the target. The result is found in a fraction of a second and is almost always optimal or very close to it, and a driver waiting at a junction is far better served by a good answer immediately than a perfect one in an hour.",
           command="Explain"),
        EQ("A student writes a recursive function that calculates the sum of the numbers from 1 to n, but it causes a stack overflow when n is 100000. Explain why and suggest a solution.", 4, [
            MP("Each recursive call adds a stack frame to the call stack", ["stack frame", "each call", "stack grows", "added"]),
            MP("With 100000 calls the stack space available is exhausted", ["exhausted", "runs out", "too many", "limit", "100000"]),
            MP("Suggests rewriting the function iteratively using a loop", ["iterative", "loop", "rewrite", "for loop", "while"]),
            MP("An iterative version uses constant memory regardless of n", ["constant", "no stack", "same memory", "does not grow"]),
        ], "Every time the function calls itself, a new stack frame is pushed onto the call stack containing that call's parameters, its local variables and the address to return to when it finishes. None of these frames can be removed until the recursion reaches its base case and the calls begin returning, so at the deepest point there are one hundred thousand frames on the stack simultaneously. The stack is allocated a fixed and comparatively modest amount of memory, typically a few megabytes, so it is exhausted long before that depth is reached and the program crashes with a stack overflow. The solution is to rewrite the function iteratively, using a loop that maintains a running total from 1 to n. This uses a constant amount of memory no matter how large n becomes, because there is only ever one stack frame, and it is also faster because it avoids the overhead of a hundred thousand function calls. For this particular problem there is an even better answer, since the sum of the first n integers is given directly by the formula n multiplied by n plus one, divided by two, which computes the result in a single operation.",
           command="Explain"),
    ],
)

A_ALGORITHMS = Topic(
    slug="algorithms-and-complexity",
    title="Algorithms and Big O Complexity",
    spec="2.3.1",
    icon="i-shuffle",
    minutes=40,
    blurb="Searching, sorting, traversals, Dijkstra and A star, and Big O analysis with the reasoning behind each complexity class.",
    fact="Dijkstra devised his shortest path algorithm in about twenty minutes in 1956 while sitting in a cafe with his fiancee, without pencil or paper. He said the absence of paper forced him to avoid all avoidable complexity.",
    sections=[
        Section("Big O and searching", """
### Big O notation

Big O describes how the resources an algorithm requires grow as the input size n grows. It describes the **worst case** unless stated otherwise, and it discards constants and lower order terms because only the dominant behaviour matters at scale.

| Complexity | Name | Example | n = 1,000,000 |
| O(1) | Constant | Array access by index, hash table lookup | 1 operation |
| O(log n) | Logarithmic | Binary search, balanced BST | about 20 |
| O(n) | Linear | Linear search, one pass over a list | 1,000,000 |
| O(n log n) | Linearithmic | Merge sort, quicksort average case | about 20,000,000 |
| O(n^2^) | Polynomial | Bubble sort, insertion sort, nested loops | 1,000,000,000,000 |
| O(2^n^) | Exponential | Brute force subset problems | Infeasible |
| O(n!) | Factorial | Brute force travelling salesman | Utterly infeasible |

**Space complexity** describes memory growth in the same way. Merge sort is O(n log n) in time but O(n) in space, which is exactly the trade off against bubble sort's O(1) space.

### Linear search

Check each element in turn. **O(n)** worst case. Works on unsorted data, requires no preparation.

### Binary search

Requires **sorted** data. Compare with the middle element and discard half the remaining range each time.

```pseudo
function binarySearch(list, target)
    low = 0
    high = list.length - 1
    while low <= high
        mid = (low + high) DIV 2
        if list[mid] == target then
            return mid
        elseif list[mid] < target then
            low = mid + 1
        else
            high = mid - 1
        endif
    endwhile
    return -1
endfunction
```

**O(log n)**, because each comparison halves the search space. On a million items that is about twenty comparisons rather than a million.

!key Why sorting first can still be worth it :: Sorting costs O(n log n), which is more than a single linear search. But if the data will be searched many times, that cost is paid once and every subsequent search drops from O(n) to O(log n).
"""),
        Section("Sorting algorithms", """
### Bubble sort, O(n^2^)

Repeatedly compare adjacent pairs and swap if out of order. After each pass the largest remaining value is in place. With a swap flag it terminates early on sorted data, giving O(n) best case.

Space O(1). Simple, and unusable at scale.

### Insertion sort, O(n^2^)

Build a sorted section at the front, inserting each next item into its correct place. Space O(1). Best case O(n) on nearly sorted data, and it can sort a stream as items arrive.

### Merge sort, O(n log n)

Divide and conquer. Split the list until each part holds one item, then repeatedly merge sorted sub lists.

```pseudo
function mergeSort(list)
    if list.length <= 1 then
        return list
    endif
    mid = list.length DIV 2
    left = mergeSort(list[0 to mid-1])
    right = mergeSort(list[mid to end])
    return merge(left, right)
endfunction
```

Consistently O(n log n) in every case, which is its great strength. Space O(n), because the sub lists must be stored, and that is its cost.

### Quicksort, O(n log n) average

Choose a **pivot**, partition so smaller values are on the left and larger on the right, then recursively sort each partition. Average O(n log n) with better constants than merge sort, so it is usually faster in practice, and space O(log n) for the recursion stack. Worst case O(n^2^) when the pivot is consistently the smallest or largest element, which is why practical implementations choose the pivot carefully.

### Choosing

| Situation | Algorithm |
| Small or nearly sorted list | Insertion sort |
| Guaranteed performance required | Merge sort |
| Best average speed, memory limited | Quicksort |
| Very limited memory | Insertion or bubble sort |
| Teaching the concept | Bubble sort |
"""),
        Section("Graph and tree algorithms", """
### Traversals

**Depth first search** goes as deep as possible before backtracking, using a **stack** or recursion. Suits maze solving, topological sorting and finding any path.

**Breadth first search** explores all neighbours at the current depth before going deeper, using a **queue**. Finds the shortest path in an **unweighted** graph, and suits finding the nearest node.

**Tree traversals:** pre order visits node, left, right and is used for copying a tree. In order visits left, node, right and outputs a binary search tree in ascending order. Post order visits left, right, node and is used for deletion and postfix expressions.

### Dijkstra's shortest path

Finds the shortest path from one source to all other nodes in a **weighted graph with non negative weights**.

1. Set the source distance to 0 and every other to infinity, and mark all nodes unvisited.
2. From the unvisited nodes, select the one with the smallest known distance, the current node.
3. For each unvisited neighbour, calculate the distance through the current node. If it is smaller than the recorded distance, replace it and record the current node as its predecessor.
4. Mark the current node visited.
5. Repeat from step 2 until the destination is visited or no reachable unvisited node remains.

The predecessor records allow the actual path to be reconstructed by working backwards from the destination.

Complexity O(n^2^) with a simple implementation, improving to O(E + V log V) with a priority queue.

!warn Dijkstra cannot handle negative weights :: Once a node is marked visited its distance is assumed final, and a negative edge could later produce a shorter route, invalidating that assumption.

### A star

An extension of Dijkstra using a **heuristic** to guide the search towards the goal.

At each step it selects the node with the lowest value of:

    f(n) = g(n) + h(n)

where g(n) is the actual cost from the start to n, and h(n) is a heuristic **estimate** of the cost from n to the goal, commonly the straight line distance.

Because it prefers nodes that appear to lead towards the goal, A star explores far fewer nodes than Dijkstra and reaches the answer much faster. It is guaranteed to find the optimal path provided the heuristic is **admissible**, meaning it never overestimates the true remaining cost.

Dijkstra is A star with h(n) set to zero for every node.
"""),
    ],
    keyterms=[
        ("Big O notation", "A description of how an algorithm's resource use grows with input size, in the worst case."),
        ("Time complexity", "How the number of operations grows as the input size increases."),
        ("Space complexity", "How the memory required grows as the input size increases."),
        ("Linear search", "Checking each element in turn, O(n), requiring no ordering."),
        ("Binary search", "Halving a sorted range at each comparison, O(log n)."),
        ("Merge sort", "A divide and conquer sort with consistent O(n log n) time and O(n) space."),
        ("Quicksort", "A partitioning sort averaging O(n log n) with O(n squared) worst case."),
        ("Pivot", "The element around which quicksort partitions the data."),
        ("Depth first search", "A traversal exploring as deep as possible before backtracking, using a stack."),
        ("Breadth first search", "A traversal exploring all nodes at one depth before going deeper, using a queue."),
        ("Dijkstra's algorithm", "An algorithm finding the shortest path in a weighted graph with non negative weights."),
        ("A star", "A pathfinding algorithm using a heuristic estimate to guide the search towards the goal."),
        ("Admissible heuristic", "A heuristic that never overestimates the remaining cost, guaranteeing an optimal result."),
    ],
    grade="""
+ State a complexity and justify it, for example that binary search is O(log n) because each comparison halves the range
+ Give the space complexity as well as the time complexity when comparing sorts
+ Know that DFS uses a stack and BFS uses a queue, and what each is therefore good at
+ Trace Dijkstra with a full table of distances, predecessors and visited nodes
+ Explain A star's f = g + h and why an admissible heuristic guarantees optimality
+ Justify a choice of algorithm against the properties of the data in the question
""",
    mistakes=[
        "Quoting a complexity with no justification for why it is that class.",
        "Comparing sorts on time only, ignoring merge sort's O(n) space cost.",
        "Applying binary search to unsorted data.",
        "Using Dijkstra on a graph with negative weights.",
        "Saying A star is always faster with no mention of the heuristic having to be admissible.",
        "Confusing depth first and breadth first, and which structure each uses.",
    ],
    quiz=[
        Q("What is the time complexity of binary search?",
          ["O(log n)", "O(n)", "O(n log n)", "O(1)"], 0,
          "Each comparison halves the remaining range, so the number of steps grows logarithmically."),
        Q("Which sorting algorithm has consistent O(n log n) performance in all cases?",
          ["Merge sort", "Quicksort", "Bubble sort", "Insertion sort"], 0,
          "Quicksort averages O(n log n) but degrades to O(n squared) with poor pivot choices."),
        Q("What is the space complexity of merge sort?",
          ["O(n)", "O(1)", "O(log n)", "O(n log n)"], 0,
          "The sub lists must be stored during merging, which is the price of its consistent speed."),
        Q("Which data structure does breadth first search use?",
          ["A queue", "A stack", "A binary tree", "A hash table"], 0,
          "A queue processes nodes in the order discovered, which is what explores level by level."),
        Q("Why can Dijkstra's algorithm not handle negative edge weights?",
          ["A visited node's distance is assumed final, which a negative edge could invalidate",
           "It cannot store negative numbers", "The queue would overflow",
           "Negative weights are impossible in a graph"], 0,
          "The algorithm's correctness depends on never finding a shorter route to an already visited node."),
        Q("In A star, what does f(n) = g(n) + h(n) represent?",
          ["The actual cost so far plus the estimated cost remaining",
           "The number of nodes visited", "The total number of edges",
           "The heuristic alone"], 0,
          "Selecting the lowest f value focuses the search on nodes that appear to lead towards the goal."),
        Q("What makes a heuristic admissible?",
          ["It never overestimates the true remaining cost",
           "It always finds the answer quickly", "It is calculated in constant time",
           "It uses straight line distance only"], 0,
          "Admissibility is what guarantees A star returns an optimal path rather than merely a good one."),
        Q("Which traversal of a binary search tree produces sorted output?",
          ["In order", "Pre order", "Post order", "Breadth first"], 0,
          "Visiting left subtree, node, then right subtree follows the ordering property exactly."),
        Q("Why is bubble sort O(n squared)?",
          ["It makes up to n passes, each comparing up to n elements",
           "It stores n copies of the list", "It calls itself n times",
           "It halves the list n times"], 0,
          "Nested repetition over the data is the signature of quadratic complexity."),
        Q("An algorithm takes 1 second on 1000 items and 100 seconds on 10000 items. What is its likely complexity?",
          ["O(n squared)", "O(n)", "O(log n)", "O(n log n)"], 0,
          "Ten times the data taking a hundred times the time is exactly quadratic growth."),
    ],
    exam=[
        EQ("Explain what Big O notation describes and why constants are ignored.", 3, [
            MP("It describes how resource use grows as the input size increases", ["grows", "input size", "scales", "resource", "as n increases"]),
            MP("It describes the worst case unless otherwise stated", ["worst case", "upper bound", "maximum"]),
            MP("Constants and lower order terms are ignored because only dominant growth matters at scale", ["constants", "dominant", "large n", "lower order", "scale"]),
        ], "Big O notation describes how the resources an algorithm requires, usually time but also memory, grow as the size of the input increases, and unless stated otherwise it describes the worst case, giving an upper bound on the behaviour. Constants and lower order terms are discarded because they become insignificant as the input grows. An algorithm taking 3n squared plus 100n plus 5000 operations is written as O(n squared), because once n is large the squared term dominates completely and the difference between 3n squared and n squared is a fixed multiple that does not change the fundamental scaling behaviour. This matters because the purpose of Big O is to compare how algorithms behave as data grows, not to predict exact runtimes on a particular machine.",
           command="Explain"),
        EQ("Compare merge sort and quicksort in terms of time complexity and space complexity.", 5, [
            MP("Merge sort is O(n log n) in all cases including the worst", ["n log n", "all cases", "consistent", "worst case", "guaranteed"]),
            MP("Quicksort averages O(n log n) but degrades to O(n squared) in the worst case", ["average", "n squared", "worst case", "degrades", "poor pivot"]),
            MP("The quicksort worst case occurs when the pivot is consistently the smallest or largest element", ["pivot", "smallest", "largest", "already sorted", "bad pivot"]),
            MP("Merge sort requires O(n) additional space for the sub lists", ["o(n) space", "extra memory", "sub lists", "additional"]),
            MP("Quicksort sorts largely in place using only O(log n) stack space", ["in place", "log n space", "less memory", "stack"]),
        ], "Merge sort has time complexity O(n log n) in the best, average and worst cases alike, because it always divides the list exactly in half regardless of the data and always performs the same merging work. Quicksort has average time complexity O(n log n) and in practice usually outperforms merge sort because its constant factors are smaller, but its worst case is O(n squared). That worst case occurs when the chosen pivot is consistently the smallest or largest remaining element, so each partition removes only one item rather than roughly half, and it arises naturally if the first element is chosen as the pivot on data that is already sorted. Practical implementations avoid it by choosing the pivot as the median of three candidates or at random. Space is where the comparison reverses. Merge sort requires O(n) additional memory because the sub lists produced by the divide phase must be stored while merging, whereas quicksort partitions the array in place and needs only O(log n) stack space for its recursive calls. The choice therefore depends on priorities: merge sort when guaranteed performance is essential or when sorting data that does not fit in memory, quicksort when average speed matters most and memory is constrained.",
           command="Compare"),
        EQ("Describe how Dijkstra's algorithm finds the shortest path between two nodes in a weighted graph.", 6, [
            MP("The source node distance is set to zero and all others to infinity", ["zero", "infinity", "source", "initialise"]),
            MP("The unvisited node with the smallest known distance is selected as the current node", ["smallest", "lowest", "current node", "select", "unvisited"]),
            MP("For each unvisited neighbour the distance through the current node is calculated", ["neighbour", "calculate", "distance through", "via"]),
            MP("If that distance is smaller than the recorded distance it replaces it", ["smaller", "replace", "update", "shorter", "if less"]),
            MP("The predecessor is recorded so the path can be reconstructed", ["predecessor", "previous", "record", "reconstruct", "trace back"]),
            MP("The current node is marked visited and the process repeats until the destination is reached", ["marked visited", "repeats", "until", "destination"]),
        ], "Dijkstra's algorithm begins by setting the distance to the source node as zero and the distance to every other node as infinity, with all nodes marked unvisited. It then repeatedly selects, from among the unvisited nodes, the one with the smallest recorded distance, and treats this as the current node. For each unvisited neighbour of the current node, it calculates the distance to that neighbour by travelling through the current node, which is the current node's distance plus the weight of the connecting edge. If this calculated distance is less than the distance already recorded for that neighbour, the recorded distance is replaced with the new smaller value and the current node is stored as that neighbour's predecessor. Once all neighbours have been considered, the current node is marked as visited and will not be examined again, because its distance is now known to be final. The process repeats, always choosing the unvisited node with the smallest distance, until the destination has been visited or no reachable unvisited node remains. The shortest path itself is then recovered by starting at the destination and following the chain of recorded predecessors back to the source, which yields the route in reverse.",
           command="Describe"),
        EQ("Explain how the A star algorithm differs from Dijkstra's algorithm and why it is usually faster.", 5, [
            MP("A star adds a heuristic estimate of the remaining cost to the goal", ["heuristic", "estimate", "remaining", "to the goal"]),
            MP("Nodes are selected by the lowest value of f equals g plus h", ["f = g + h", "g plus h", "cost so far plus estimate"]),
            MP("Dijkstra explores outwards in all directions equally", ["all directions", "outwards", "equally", "no direction", "everywhere"]),
            MP("A star prioritises nodes appearing to lead towards the goal, so it examines fewer nodes", ["towards the goal", "fewer nodes", "focused", "directed"]),
            MP("It still finds the optimal path provided the heuristic never overestimates", ["never overestimates", "admissible", "optimal", "guaranteed"]),
        ], "Dijkstra's algorithm always expands the unvisited node with the smallest distance from the source, which means it explores outwards from the start in every direction equally, discovering shortest paths to nodes that lie entirely away from the destination before it happens to reach the destination itself. A star modifies the selection rule by adding a heuristic estimate of the remaining cost from each node to the goal, so it chooses the node with the lowest value of f, where f equals g plus h, g being the actual cost accumulated from the start and h being the estimated cost still to travel. Because a node lying in the direction of the goal receives a low h value, it is selected in preference to a node that is equally close to the start but heading away, so the search is directed rather than uniform and typically examines a small fraction of the nodes that Dijkstra would. Crucially, A star still guarantees the optimal path provided the heuristic is admissible, meaning it never overestimates the true remaining cost, since underestimating simply means the algorithm may explore a few extra nodes rather than committing to a suboptimal route. Straight line distance is the standard admissible heuristic for geographic pathfinding, since no actual route can be shorter than a straight line. Dijkstra can be seen as the special case of A star where h is zero everywhere.",
           command="Explain"),
        EQ("A system stores 10 million records and must be searched frequently by a unique key. Compare linear search, binary search and a hash table for this purpose.", 6, [
            MP("Linear search is O(n) and would examine up to 10 million records per search", ["o(n)", "linear", "10 million", "every record", "one at a time"]),
            MP("Linear search requires no ordering but is far too slow at this scale", ["no ordering", "unsorted", "too slow", "impractical"]),
            MP("Binary search is O(log n), needing about 24 comparisons", ["log n", "24", "23", "about 20", "halves"]),
            MP("Binary search requires the data to be kept sorted, which costs time on insertion", ["sorted", "must be sorted", "insertion cost", "maintaining order"]),
            MP("A hash table gives average O(1) lookup by calculating the position from the key", ["o(1)", "constant", "calculates", "hash function", "index"]),
            MP("Recommends the hash table, noting it does not support ordered or range queries", ["recommend", "hash table", "no ordering", "range queries", "not sorted", "best"]),
        ], "Linear search has time complexity O(n), so on 10 million records it would examine on average five million and at worst all ten million entries for every single query. It has the advantage of requiring no ordering or preparation at all, but at this scale and with frequent searching it is completely impractical. Binary search has complexity O(log n), which reduces the work to about 24 comparisons for ten million records, an improvement of roughly six orders of magnitude. Its precondition is that the data must be kept in sorted order, which means either sorting once at O(n log n) if the data is static, or paying an insertion cost to maintain the ordering as records are added, and inserting into a sorted array requires shifting subsequent elements. A hash table offers average O(1) lookup, because the hash function calculates the storage index directly from the key so no searching of any kind is performed, and the time taken does not increase as the number of records grows. Given that the search is by a unique key and is performed frequently, the hash table is the strongest choice, and it should be sized so the load factor stays low enough that collisions remain rare. The one caveat is that a hash table imposes no useful ordering on the data, so if the system also needs to retrieve records in key order or answer range queries such as all keys between two values, a balanced binary search tree giving O(log n) for both lookup and ordered traversal would be the better overall structure.",
           command="Compare"),
    ],
)

A_NEA = Topic(
    slug="nea-programming-project",
    title="The Programming Project (NEA)",
    spec="Component 3 and 4",
    icon="i-flag",
    minutes=30,
    blurb="How the 70 mark project is actually marked, what separates a high band analysis from an average one, and the mistakes that cost the most marks.",
    fact="The single most common reason for losing marks on the project is not weak code. It is evidence: excellent work that was never documented as it happened, and cannot be reconstructed afterwards.",
    sections=[
        Section("Analysis and design", """
The project is worth 70 marks and around 20 per cent of the A Level. It is marked in four sections.

### Analysis, 10 marks

**Problem identification.** Describe a problem that is genuinely suitable for a computational solution, explaining why it is solvable computationally and why it is worth solving.

**Stakeholders.** Identify who will use the solution and who else is affected, describing each specifically and explaining how the solution addresses their particular needs. Generic stakeholders lose marks.

**Research.** Examine existing similar solutions, identifying what each does well and where it falls short, and interview or survey your stakeholders. Evidence the research: include the questions asked and the answers received.

**Requirements.** Produce specific, measurable, testable requirements, covering hardware and software requirements too.

**Success criteria.** Each must be independently testable, because you will evaluate against them at the end. "The system will be easy to use" is not testable. "A new user can add a booking in under 60 seconds without assistance" is.

### Design, 15 marks

**Decomposition.** Break the problem down and show the structure, typically as a structure diagram or a hierarchy chart.

**Algorithms.** Present the key algorithms as pseudocode or flowcharts, with enough detail that a competent third party could implement them.

**Usability.** Show interface designs and explain how they address the needs of specific stakeholders, referring to usability principles rather than simply presenting screens.

**Data structures.** Justify each choice against the operations required, not merely state it.

**Validation.** Specify validation for every input.

**Test data.** Plan tests using normal, boundary and erroneous data, with the expected result stated for each before development begins.

!key What separates the top band :: Justification. Every design decision must be explained in terms of the requirements it serves, and every algorithm must be detailed enough to implement without further invention.
"""),
        Section("Development, testing and evaluation", """
### Development, 25 marks

The largest section, and it rewards **evidence of an iterative process**, not merely a finished program.

Work in **cycles**, and for each one:

1. State what you are building and why it comes next
2. Show annotated code, explaining the technique used and why it was chosen
3. Show it working, with screenshots including the input used
4. Test it, including the cases where it should fail
5. Review it, describing what worked, what did not, and what you changed as a result
6. Show any refinement made in response

Technical skill is assessed on the difficulty of what you attempt as well as its correctness. Complex data structures, recursion, file or database handling, OOP where appropriate, and effective algorithms all count. A perfectly working but trivial program cannot reach the top band.

Code quality is assessed too: meaningful identifiers, sensible modular structure, comments explaining why, consistent style, and no unnecessary duplication.

!warn Evidence must be captured as you go :: Screenshots taken during development, dated review notes, and version history. Reconstructing this at the end is obvious to a moderator and takes far longer than doing it properly.

### Testing, 10 marks

**Testing during development** shows each component working as it was built, and is evidenced within the development cycles.

**Post development testing** tests the complete system against the test plan written during design, with evidence for every test, and follow up evidence showing that any failure was corrected.

**Usability testing** involves real stakeholders using the system while you observe, recording what they struggled with and what you changed as a result.

Cover normal, boundary and erroneous data for every input, and test the requirements, not just the code you happen to have written.

### Evaluation, 10 marks

**Against success criteria.** Take each criterion in turn, present the evidence, and state honestly whether it was fully met, partly met or not met.

**Usability.** Report what stakeholders said and did, including the negative feedback, and describe what you changed.

**Maintenance and development.** Describe specific limitations of the finished system and realistic further developments, explaining how each would be implemented.

An honest evaluation identifying real weaknesses scores far more highly than one claiming everything worked perfectly. Moderators read hundreds of these, and an evaluation with no criticism reads as an evaluation that was never actually done.

### The five most costly mistakes

1. **Choosing a problem that is too simple.** The band is capped by the difficulty attempted.
2. **No real stakeholder.** Without one, the analysis, usability and evaluation sections all lose marks.
3. **Evidence gathered at the end.** It is always visible, and it is worth many marks.
4. **Success criteria that cannot be tested.** These make the evaluation impossible to write well.
5. **A dishonest evaluation.** Claiming everything worked perfectly is the surest way to lose evaluation marks.
"""),
    ],
    keyterms=[
        ("Stakeholder", "A person who will use or be affected by the solution, identified specifically."),
        ("Success criterion", "A specific, independently testable statement of what the finished system must achieve."),
        ("Decomposition", "Breaking the problem into sub problems, evidenced with a structure diagram."),
        ("Iterative development", "Building in cycles of implement, test and review, with evidence at each cycle."),
        ("Post development testing", "Testing the complete system against the plan written during the design stage."),
        ("Usability testing", "Observing real stakeholders using the system and recording what they struggle with."),
        ("Boundary data", "Test data at the very edge of the acceptable range, where errors are most likely."),
        ("Erroneous data", "Test data of the wrong type entirely, which the system should reject."),
    ],
    grade="""
+ Choose a problem with genuine technical depth: real data structures, algorithms, persistence
+ Secure a real stakeholder early and keep documented contact throughout
+ Write success criteria that can each be objectively tested with a yes or no
+ Capture evidence at the moment it happens, never afterwards
+ Justify every design decision against a specific requirement
+ Evaluate honestly, and describe what you would change and why
""",
    mistakes=[
        "Choosing a problem too simple to demonstrate technical skill, capping the mark band.",
        "Inventing a stakeholder rather than working with a real one.",
        "Writing success criteria such as 'the system will be user friendly', which cannot be tested.",
        "Producing a finished program with no evidence of the iterative process behind it.",
        "Testing only the paths that work.",
        "Writing an evaluation claiming everything succeeded perfectly.",
    ],
    quiz=[
        Q("How many marks is the OCR A Level programming project worth?",
          ["70", "50", "100", "40"], 0,
          "It is worth 70 marks and around 20 per cent of the overall A Level."),
        Q("Which is a well written success criterion?",
          ["A new user can add a booking in under 60 seconds without assistance",
           "The system will be easy to use", "The program will work well",
           "Users will like the interface"], 0,
          "It must be objectively testable, so that the evaluation can state clearly whether it was met."),
        Q("Why must evidence be captured during development rather than afterwards?",
          ["It shows the genuine iterative process, and reconstruction is obvious to a moderator",
           "Screenshots expire", "It is required by law", "The code changes automatically"], 0,
          "The development section rewards evidence of the process, not simply the finished program."),
        Q("What should usability testing involve?",
          ["Observing real stakeholders using the system and recording their difficulties",
           "Checking the code compiles", "Running the unit tests",
           "Asking a friend if it looks good"], 0,
          "Watching a genuine user reveals problems the developer cannot see, because they already know the system."),
        Q("Which section of the project carries the most marks?",
          ["Development", "Analysis", "Testing", "Evaluation"], 0,
          "Development is worth 25 of the 70 marks, more than any other section."),
        Q("What makes an evaluation score highly?",
          ["Honest assessment against each success criterion, including what was not met",
           "Stating that every criterion was fully met",
           "A long description of the code", "Screenshots of the final program"], 0,
          "An evaluation with no identified weaknesses reads as one that was never genuinely carried out."),
        Q("Why should the chosen problem have technical depth?",
          ["The mark band is capped by the difficulty of what is attempted",
           "Simple problems take longer", "Moderators prefer complex code",
           "Simple problems cannot be tested"], 0,
          "A flawless but trivial program cannot reach the top band, however well written it is."),
        Q("What should a test plan include for every test?",
          ["The test data, its type and the expected result stated in advance",
           "Only the actual result", "A screenshot only", "The line of code being tested"], 0,
          "Without an expected result there is nothing to compare the actual behaviour against."),
        Q("What is the purpose of identifying stakeholders specifically?",
          ["Requirements, usability and evaluation all depend on real user needs",
           "It fills space in the analysis", "It is required by the exam board only",
           "It makes the project longer"], 0,
          "Without real stakeholders, three separate sections of the project lose marks."),
        Q("What should each development cycle include?",
          ["What was built, annotated code, evidence of it working, testing and a review",
           "Only the final code", "A screenshot of the interface",
           "A list of variables used"], 0,
          "The review, describing what changed and why, is what evidences a genuinely iterative process."),
    ],
    exam=[
        EQ("Explain why success criteria must be measurable.", 3, [
            MP("The evaluation assesses the finished system against them", ["evaluation", "assessed against", "compared", "judged"]),
            MP("A vague criterion cannot be shown to have been met or not met", ["vague", "cannot be shown", "subjective", "no evidence", "unclear"]),
            MP("A measurable criterion allows objective evidence to be presented", ["objective", "evidence", "test", "demonstrate", "prove"]),
        ], "The success criteria written during the analysis stage are what the finished system is evaluated against, so they determine whether the evaluation can be written convincingly at all. A criterion such as the system will be easy to use is subjective, and there is no evidence that could settle whether it was achieved, so the evaluation of it becomes an unsupported opinion. A measurable criterion such as a new user can complete a booking in under sixty seconds without assistance can be tested directly by observing a real user with a stopwatch, which produces objective evidence that can be presented and judged. Writing testable criteria at the start therefore makes both the testing and the evaluation possible, and it also clarifies during design exactly what the system has to achieve.",
           command="Explain"),
        EQ("Describe what should be included in each development cycle of the project.", 5, [
            MP("A statement of what is being built and why it comes next", ["what", "why", "next", "aim", "objective"]),
            MP("Annotated code explaining the techniques used", ["annotated", "code", "explains", "commented", "justify"]),
            MP("Evidence of it working, such as screenshots with the input used", ["screenshot", "evidence", "working", "output", "input used"]),
            MP("Testing of that component including cases that should fail", ["test", "testing", "should fail", "erroneous", "boundary"]),
            MP("A review describing what worked, what did not and what was changed", ["review", "what worked", "changed", "refinement", "improved"]),
        ], "Each development cycle should begin with a clear statement of what is being built in that iteration and why it is the sensible next step, which demonstrates that the development was planned rather than arbitrary. The code produced should then be presented with annotation explaining the techniques used and why they were chosen over alternatives, rather than simply pasted in. Evidence that it works must follow, in the form of screenshots that show both the input given and the output produced, since a screenshot of output alone proves nothing. That component should then be tested, including deliberately with data that should be rejected, and the results shown. Finally the cycle should close with a review that honestly describes what worked, what did not, and what was consequently changed, with evidence of the refinement. It is this review and refinement, repeated across cycles, that evidences a genuinely iterative process rather than a single linear attempt.",
           command="Describe"),
        EQ("Explain why identifying real stakeholders is important for the project.", 4, [
            MP("Stakeholders provide the requirements the system must meet", ["requirements", "needs", "what is needed", "specification"]),
            MP("Their needs justify design decisions during the design stage", ["justify", "design decisions", "based on", "informed"]),
            MP("They can be observed using the system during usability testing", ["usability testing", "observe", "real user", "feedback"]),
            MP("The evaluation depends on their feedback and on the criteria derived from them", ["evaluation", "feedback", "criteria", "judged"]),
        ], "Real stakeholders matter because three separate sections of the project depend on them. In analysis, they are the source of the requirements: interviewing them establishes what the system actually needs to do rather than what the developer imagines, and the success criteria are derived from those needs. In design, their particular characteristics justify decisions, so choosing large controls and minimal text can be defended by reference to the specific users rather than being asserted as good practice in general. In testing and evaluation, they are the people who use the system while the developer observes, which reveals usability problems the developer cannot possibly see because they already know where everything is, and their feedback is the evidence against which the finished system is judged. A project with an invented stakeholder has nothing genuine to test against and loses marks in all of these areas.",
           command="Explain"),
        EQ("Explain what should be included in the evaluation section and why an honest evaluation scores more highly.", 5, [
            MP("Each success criterion is addressed in turn with evidence", ["each criterion", "in turn", "evidence", "one by one"]),
            MP("It states whether each was fully met, partly met or not met", ["fully met", "partly", "not met", "extent"]),
            MP("Usability feedback from stakeholders is reported, including negative feedback", ["usability", "feedback", "stakeholders", "negative", "criticism"]),
            MP("Limitations and possible further developments are described", ["limitations", "further development", "improvements", "future"]),
            MP("An evaluation with no identified weaknesses appears not to have been genuinely carried out", ["no weaknesses", "not genuine", "unrealistic", "not credible", "everything worked"]),
        ], "The evaluation should work through each success criterion established during analysis in turn, presenting the evidence relating to it and stating clearly whether it was fully met, partly met or not met, with an explanation where it fell short. It should then report the usability feedback obtained from stakeholders who actually used the system, including the criticism they gave and what was changed in response to it. Finally it should describe the limitations of the finished system honestly, and set out realistic further developments with an explanation of how each would be implemented. Honesty scores more highly because the marks are awarded for the quality of the judgement rather than for the quality of the outcome being described. An evaluation claiming that every criterion was fully met and every user was entirely satisfied is not credible, since no software project achieves that, and it demonstrates either that the evaluation was not genuinely carried out or that the student cannot identify weaknesses in their own work. Identifying a specific shortcoming, explaining why it occurred and describing precisely how it would be addressed shows exactly the critical understanding the mark scheme rewards.",
           command="Explain"),
        EQ("A student is choosing a problem for their programming project. Explain what makes a problem suitable.", 5, [
            MP("It must be genuinely solvable by a computational approach", ["computational", "solvable", "suitable for a computer", "definable"]),
            MP("It must have sufficient technical depth to demonstrate skill", ["depth", "complex", "technical", "demonstrate skill", "not trivial"]),
            MP("It should involve data structures, algorithms and persistence rather than trivial operations", ["data structures", "algorithms", "file", "database", "persistence"]),
            MP("It must have real stakeholders whose needs can be researched", ["stakeholders", "real users", "researched", "interview"]),
            MP("It must be achievable within the available time", ["achievable", "time", "realistic", "scope", "manageable"]),
        ], "A suitable problem must first be genuinely amenable to a computational solution, meaning it can be defined precisely, the necessary data is obtainable and the rules governing it can be stated explicitly. It must then have enough technical depth to allow the student to demonstrate real skill, because the mark band is capped by the difficulty of what is attempted, so a flawlessly implemented but trivial program cannot reach the highest marks. In practice this means the problem should naturally require non trivial data structures, meaningful algorithms, validated input and some form of persistent storage, rather than being a sequence of simple calculations. There must be real stakeholders who can be interviewed at the analysis stage and observed at the testing stage, since the requirements, usability testing and evaluation all depend on them. Finally the problem must be achievable within the time available, because an over ambitious project that is left incomplete loses marks across development, testing and evaluation, and a well executed project of moderate ambition scores far better than an unfinished one of great ambition.",
           command="Explain"),
    ],
)

# ================================================================== COURSE

COURSE = Course(
    slug="ks5",
    title="A Level Computer Science",
    short="A Level",
    stage="KS5",
    board="OCR",
    code="H446",
    goal="Grade A star",
    icon="i-brain",
    accent="var(--deep)",
    blurb="The full OCR H446 specification at A Level depth. Component 01 computer systems, Component 02 algorithms and programming, and guidance on the programming project, each with quizzes and auto marked extended answers.",
    intro="",
    journey=[
        ("Depth, not coverage",
         "At A Level the marks are in the mechanism. Knowing that pipelining improves throughput is a GCSE answer. Explaining what happens to the pipeline when a branch is taken is an A Level one.", ""),
        ("Program every single week",
         "Paper 2 is a programming paper. You cannot revise your way to fluency in it, and the project makes up a fifth of the qualification. Write code weekly from Year 12, not from January of Year 13.", ""),
        ("Learn the mark scheme language",
         "Examiners reward specific vocabulary: encapsulation, admissible heuristic, transitive dependency, load factor. Using the precise term signals understanding far more efficiently than a paragraph of description.", ""),
        ("Start the project early and evidence it as you go",
         "The project is 70 marks. The evidence that earns them has to be captured while the work is happening. It cannot be reconstructed afterwards, and moderators always notice when it has been.", ""),
        ("Practise extended responses under time",
         "The long answers carry a large proportion of the marks and are levels marked. Structure, balance and a conclusion matter as much as the content, and that is a skill you build only by writing them.", ""),
        ("Fill your gaps with question level analysis",
         "After every mock, list every mark you dropped and why. Revise that list, not the whole specification. A star students are not the ones who know everything, they are the ones who found their gaps and closed them.", ""),
    ],
    units=[
        Unit("processors", "1.1 Characteristics of Contemporary Processors",
             "The processor in full, the fetch decode execute cycle with all registers, pipelining, architectures and input, output and storage.",
             [A_PROCESSOR, A_PROCTYPES, A_IOSTORAGE], icon="i-cpu", term="Component 01"),
        Unit("software", "1.2 Software and Software Development",
             "Operating systems, memory management and scheduling, translators and the stages of compilation, methodologies and programming paradigms.",
             [A_SYSSOFT, A_APPGEN, A_LANGUAGES], icon="i-software", term="Component 01"),
        Unit("exchanging-data", "1.3 Exchanging Data",
             "Compression, encryption and hashing, databases and normalisation, networks, the TCP/IP stack and web technologies.",
             [A_COMPRESSION, A_DATABASES, A_NETWORKS], icon="i-network", term="Component 01"),
        Unit("data-and-logic", "1.4 Data Types, Data Structures and Boolean Algebra",
             "Two's complement, floating point, bitwise operations, Boolean algebra with De Morgan's laws, and every data structure on the specification.",
             [A_DATATYPES, A_STRUCTURES], icon="i-binary", term="Component 01"),
        Unit("issues", "1.5 Legal, Moral, Cultural and Ethical Issues",
             "The five acts, ethical frameworks, and how to structure the extended response so it reaches the top level.",
             [A_LEGAL], icon="i-scales", term="Component 01"),
        Unit("computational-thinking", "2.1 and 2.2 Computational Thinking and Problem Solving",
             "Thinking abstractly, ahead, procedurally, logically and concurrently, plus recursion, parameter passing and every computational method.",
             [A_THINKING, A_PROGTECH], icon="i-brain", term="Component 02"),
        Unit("algorithms", "2.3 Algorithms",
             "Searching, sorting, traversals, Dijkstra, A star and Big O complexity with the reasoning behind each class.",
             [A_ALGORITHMS], icon="i-shuffle", term="Component 02"),
        Unit("nea", "Component 03 and 04: The Programming Project",
             "How the 70 mark project is marked, what reaches the top band in each section, and the mistakes that cost the most.",
             [A_NEA], icon="i-flag", term="NEA"),
    ],
)
