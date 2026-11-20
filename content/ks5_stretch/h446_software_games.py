"""OCR H446 1.2 Software and software development: Code Word, Link Up and Bug Hunt."""
from mskbuild.models import Games, Word, Group, Bug

GAMES = [
    Games(
        lesson="systems-software",
        words=[
            Word("FRAME", "A fixed size slot in physical memory that holds one page."),
            Word("KERNEL", "The core of the operating system, loaded into RAM by the bootstrap."),
            Word("DRIVER", "Software that turns operating system commands into ones a particular device understands."),
        ],
        groups=[
            Group("Types of operating system", ["Distributed", "Embedded", "Multi user", "Real time"]),
            Group("Scheduling algorithms", ["Round robin", "First come first served", "Shortest job first",
                                            "Feedback queues"]),
            Group("Memory management", ["Paging", "Segmentation", "Page table", "Page fault"]),
        ],
        bugs=[
            Bug(["Pages are a fixed size and fit any frame in physical memory.",
                 "Segments vary in size and follow the structure of the program."],
                "Paging causes external fragmentation between pages.",
                "Paging causes internal fragmentation, because the last page is rarely full. Segmentation causes "
                "external fragmentation."),
            Bug(["Round robin gives each process an equal time slice in turn.",
                 "First come first served runs processes in order of arrival."],
                "Round robin always runs the most urgent process first.",
                "Round robin ignores priority and urgency. Every process simply gets its turn."),
            Bug(["Shortest job first gives the lowest average waiting time.",
                 "Shortest job first needs run times to be known in advance."],
                "Shortest job first makes sure that long processes are never starved.",
                "If short jobs keep arriving, a long job may wait forever. That is starvation."),
            Bug(["A device driver translates operating system commands for one device.",
                 "The BIOS runs a power on self test before loading the bootstrap."],
                "The operating system kernel is loaded before the power on self test runs.",
                "The power on self test runs first to check the hardware. Only then is the bootstrap loaded, and it "
                "loads the kernel."),
            Bug(["A real time operating system guarantees a maximum response time.",
                 "An embedded operating system is built for one dedicated task."],
                "A distributed operating system runs on a single machine.",
                "A distributed operating system spreads one system across several networked machines, while appearing "
                "to the user as one system."),
        ],
    ),
    Games(
        lesson="applications-generation",
        words=[
            Word("TOKEN", "A keyword, identifier or operator produced by lexical analysis."),
            Word("LINKER", "Combines compiled object code with the library code a program uses."),
            Word("SPIRAL", "A methodology that analyses risk in every cycle."),
        ],
        groups=[
            Group("Stages of compilation", ["Lexical analysis", "Syntax analysis", "Code generation", "Optimisation"]),
            Group("Made by a compiler", ["Tokens", "Symbol table", "Syntax tree", "Object code"]),
            Group("Methodologies", ["Waterfall", "Spiral", "Agile", "Extreme programming"]),
        ],
        bugs=[
            Bug(["Lexical analysis turns the source into tokens.",
                 "Syntax analysis builds an abstract syntax tree."],
                "Optimisation is the first stage of compilation.",
                "Optimisation comes last, after code generation. Lexical analysis is first."),
            Bug(["A compiler reports its errors after translating the whole program.",
                 "An interpreter stops at the first error it meets."],
                "An interpreted program runs faster than the same program compiled.",
                "Interpreting translates every statement each time it runs, so it is slower. Compiled code runs at full "
                "speed."),
            Bug(["Static linking copies library code into the executable.",
                 "Dynamic linking loads the library while the program runs."],
                "Dynamic linking makes the executable larger than static linking.",
                "Dynamic linking stores only a reference, so the file is smaller. Static linking copies the code in, "
                "making it larger."),
            Bug(["The loader copies an executable into memory.",
                 "A library holds subroutines that are already tested."],
                "The linker copies the finished program into memory to run it.",
                "That is the loader's job. The linker combines object code with library code."),
            Bug(["Waterfall completes each stage fully before the next stage begins.",
                 "Spiral analyses risk in every cycle."],
                "Agile suits projects where the client cannot be contacted.",
                "Agile needs the customer involved throughout. Waterfall suits a client who is not available."),
        ],
    ),
    Games(
        lesson="programming-paradigms",
        words=[
            Word("MNEMONIC", "A short code such as LDA or STA that stands for a machine instruction."),
            Word("CLASS", "A template from which objects are created."),
            Word("PARADIGM", "An approach to structuring a program, such as procedural or object oriented."),
        ],
        groups=[
            Group("Addressing modes", ["Immediate", "Direct", "Indirect", "Indexed"]),
            Group("LMC mnemonics", ["LDA", "STA", "BRZ", "HLT"]),
            Group("Object oriented ideas", ["Inheritance", "Encapsulation", "Polymorphism", "Classes"]),
        ],
        bugs=[
            Bug(["In immediate addressing the operand is the value itself.",
                 "In direct addressing the operand is the address of the value."],
                "In indexed addressing the operand is the address of an address.",
                "That is indirect addressing. Indexed addressing adds the operand to the contents of an index "
                "register."),
            Bug(["BRZ branches only when the value in the accumulator is zero.",
                 "STA copies the value in the accumulator to a memory address."],
                "BRP branches only when the accumulator is more than zero.",
                "BRP also branches when the accumulator is zero, because LMC treats zero as positive."),
            Bug(["Inheritance puts shared code in a superclass.",
                 "Encapsulation lets an object protect its own state."],
                "Polymorphism means a class can only have one method.",
                "Polymorphism lets the same method call work on objects of different classes, each responding in its "
                "own way."),
            Bug(["SQL is a declarative language.",
                 "Procedural programs group instructions into procedures and functions."],
                "Declarative code spells out every step the computer must take.",
                "That is procedural. Declarative code says what result is wanted and leaves the how to the system."),
            Bug(["Assembly gives direct control over registers and memory.",
                 "One assembly instruction usually matches one machine instruction."],
                "Assembly language programs run on any processor without changes.",
                "Assembly is tied to one processor's instruction set, so it must be rewritten for a different "
                "architecture."),
        ],
    ),
]
