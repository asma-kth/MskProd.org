"""OCR H446 1.1 Characteristics of contemporary processors: Code Word, Link Up and Bug Hunt."""
from mskbuild.models import Games, Word, Group, Bug

GAMES = [
    Games(
        lesson="structure-and-function-of-the-processor",
        words=[
            Word("OPCODE", "The part of an instruction that says which operation to perform."),
            Word("PIPELINE", "Overlapping fetch, decode and execute so several instructions are in progress at once."),
            Word("INTERRUPT", "A signal asking for the processor's attention, checked at the end of each cycle."),
        ],
        groups=[
            Group("Registers", ["Program counter", "CIR", "MAR", "Accumulator"]),
            Group("Status flags", ["Carry", "Zero", "Overflow", "Negative"]),
            Group("Affect performance", ["Clock speed", "Cache size", "Number of cores", "Word length"]),
        ],
        bugs=[
            Bug(["The program counter holds the address of the next instruction to fetch.",
                 "The MAR holds the address being read from or written to."],
                "The CIR holds the address of the instruction being executed.",
                "The CIR holds the instruction itself, copied from the MDR, not its address."),
            Bug(["The registers are pushed onto a stack when an interrupt is serviced.",
                 "A higher priority interrupt can interrupt an interrupt service routine."],
                "Interrupts cannot be nested, because only one state can be saved at a time.",
                "The state is saved on a stack, so several states can be saved in turn and interrupts can nest."),
            Bug(["A 32 bit address bus can address 2 to the power 32 locations.",
                 "The data bus carries data and instructions in both directions."],
                "The address bus carries addresses in both directions.",
                "The address bus is one way, from the processor to memory. The data and control buses are the two way "
                "ones."),
            Bug(["Pipelining lets one instruction be fetched while another is decoded.",
                 "Branch prediction reduces the cost of pipeline flushes."],
                "Pipelining makes each single instruction finish in fewer cycles.",
                "Each instruction still passes through every stage. Pipelining raises throughput by overlapping "
                "instructions."),
            Bug(["Harvard architecture has separate memories for instructions and data.",
                 "Von Neumann architecture stores instructions and data in one memory."],
                "Harvard architecture is cheaper and simpler than von Neumann.",
                "Harvard needs two memories and two sets of buses, so it is more complex and costly. It is faster, which "
                "is why it suits embedded systems."),
        ],
    ),
    Games(
        lesson="types-of-processor",
        words=[
            Word("MICROCODE", "Low level steps inside a CISC processor that carry out its complex instructions."),
            Word("AMDAHL", "His law says the sequential part of a task caps the speedup from more processors."),
            Word("THREAD", "A single sequence of instructions that one core can run."),
        ],
        groups=[
            Group("RISC features", ["Fixed length", "One cycle each", "Simple decoding", "Low power"]),
            Group("CISC features", ["Variable length", "Microcode", "Many cycles each", "Complex hardware"]),
            Group("Limit parallel speedup", ["Sequential parts", "Data dependencies", "Coordination",
                                             "Single threaded code"]),
        ],
        bugs=[
            Bug(["RISC instructions are a fixed length and usually take one cycle.",
                 "CISC instructions vary in length and can take several cycles."],
                "RISC programs need fewer instructions than CISC programs.",
                "Each RISC instruction does less, so a RISC program needs more instructions. CISC packs more work into "
                "each one."),
            Bug(["A GPU has thousands of simple cores.",
                 "SIMD applies one instruction to many data items at once."],
                "A GPU runs code with many unpredictable branches faster than a CPU.",
                "Branches send data items down different paths, so GPU cores sit idle. A CPU, with branch prediction, "
                "handles them better."),
            Bug(["Amdahl's law limits the speedup from adding more processors.",
                 "A step that needs an earlier result cannot start early."],
                "Doubling the number of cores always halves the running time.",
                "Sequential parts, data dependencies and coordination overhead all mean the time falls by less than "
                "half."),
            Bug(["In RISC, the compiler builds complex operations from simple instructions.",
                 "CISC processors often use microcode."],
                "In CISC, the complexity sits in the compiler rather than the hardware.",
                "CISC builds the complexity into the hardware, often with microcode. It is RISC that moves it into the "
                "compiler."),
            Bug(["ARM processors are RISC and run almost every phone.",
                 "Most desktop computers use x86 processors, which are CISC."],
                "RISC processors draw more power because they run more instructions.",
                "RISC hardware is simpler, so it draws less power, which is why it suits devices that run on a "
                "battery."),
        ],
    ),
    Games(
        lesson="input-output-and-storage",
        words=[
            Word("PAGING", "Moving fixed sized blocks of memory between RAM and secondary storage."),
            Word("PLATTER", "A spinning disc coated in magnetic material inside a hard drive."),
            Word("TONER", "The powder a laser printer fuses onto paper with heat."),
        ],
        groups=[
            Group("Input devices", ["Keyboard", "Barcode scanner", "Microphone", "Optical mouse"]),
            Group("Output devices", ["OLED display", "Laser printer", "Inkjet printer", "3D printer"]),
            Group("Keep data without power", ["ROM", "Flash drive", "Magnetic tape", "Hard disk"]),
        ],
        bugs=[
            Bug(["DRAM stores each bit as charge that slowly leaks away.",
                 "SRAM needs no refreshing and is used for cache."],
                "SRAM is slower than DRAM, so it is used for main memory.",
                "SRAM is the faster one, used for cache. DRAM is cheaper and denser, so it is used for main memory."),
            Bug(["Flash cells survive a limited number of program and erase cycles.",
                 "An SSD has no moving parts, so it copes well with knocks."],
                "Wear levelling sends every write to the same block of cells.",
                "Wear levelling spreads writes across the whole drive so that no cells wear out early."),
            Bug(["Virtual memory uses secondary storage as an extension of RAM.",
                 "Disk thrashing happens when pages are swapped too often."],
                "Pages that are used most often are moved out to the page file.",
                "It is the pages that have not been used recently that are moved out, so the busy ones stay in RAM."),
            Bug(["An OLED pixel gives out its own light.",
                 "An LCD controls light from a backlight with liquid crystals."],
                "An OLED screen needs a backlight behind its pixels.",
                "OLED pixels emit their own light, so there is no backlight and a black pixel is simply switched off."),
            Bug(["Magnetic tape is serial access, so it winds to reach a file.",
                 "Tape costs very little per terabyte, so it suits archives."],
                "Tape gives fast access to any single file.",
                "Tape must wind through to reach a file, so access is slow. That is fine for an archive but not for "
                "daily use."),
        ],
    ),
]
