"""OCR H446 2.1 and 2.2 Computational thinking and problem solving: Code Word, Link Up and Bug Hunt."""
from mskbuild.models import Games, Word, Group, Bug

GAMES = [
    Games(
        lesson="elements-of-computational-thinking",
        words=[
            Word("CACHE", "Fast storage for results that are likely to be needed again."),
            Word("RACE", "This kind of condition means the result depends on which thread reaches shared data first."),
            Word("MODEL", "A simplified version of reality, useful precisely because it leaves things out."),
        ],
        groups=[
            Group("Costs of concurrency", ["Race conditions", "Deadlock", "Harder debugging", "Coordination"]),
            Group("Thinking ahead", ["Caching", "Preconditions", "Inputs and outputs", "Reusable parts"]),
            Group("Models of reality", ["Tube map", "Flight simulator", "Floor plan", "Traffic simulation"]),
        ],
        bugs=[
            Bug(["Abstraction removes detail that is not needed.",
                 "Decomposition splits a problem into sub problems."],
                "Abstraction means splitting a problem into smaller parts.",
                "That is decomposition. Abstraction removes detail that does not matter to the problem."),
            Bug(["Caching trades memory for speed.",
                 "A precondition must be true before a subroutine is called."],
                "A cache keeps results that will never be used again.",
                "A cache stores results likely to be needed again, so they need not be worked out a second time."),
            Bug(["Genuine concurrency needs more than one processor.",
                 "Apparent concurrency switches quickly between tasks."],
                "Apparent concurrency needs several processors running at once.",
                "Apparent concurrency is one processor switching tasks so quickly they seem simultaneous. Genuine "
                "concurrency needs several."),
            Bug(["A race condition depends on the order threads access shared data.",
                 "Deadlock leaves threads each waiting for the other."],
                "Race conditions always show up the first time a program is tested.",
                "They depend on timing, so they may only appear occasionally, which makes them hard to find."),
            Bug(["Top down design starts with the whole problem.",
                 "Bottom up design builds small components first."],
                "Real projects only ever use top down design.",
                "Real projects use both: dividing the whole problem and assembling small, reliable components."),
        ],
    ),
    Games(
        lesson="programming-techniques-and-methods",
        words=[
            Word("RECURSION", "A subroutine calling itself, stopped by a base case."),
            Word("SCOPE", "Where in a program an identifier can be accessed."),
            Word("HEURISTIC", "A rule of thumb that gives a good enough answer quickly."),
        ],
        groups=[
            Group("Computational methods", ["Backtracking", "Data mining", "Heuristics", "Visualisation"]),
            Group("IDE features", ["Breakpoints", "Stepping", "Variable watch", "Auto complete"]),
            Group("Recursion needs", ["Base case", "General case", "Stack frames", "Calls to itself"]),
        ],
        bugs=[
            Bug(["A recursive subroutine needs a base case.",
                 "Each recursive call adds a stack frame."],
                "Recursion uses less memory than the same loop.",
                "Every call adds a stack frame, so recursion uses more memory than a loop."),
            Bug(["Passing by value gives the subroutine a copy.",
                 "Passing by reference passes the address of the variable."],
                "A value parameter changes the original variable.",
                "A value parameter is a copy, so the original is untouched. Only passing by reference changes the "
                "original."),
            Bug(["A local variable exists only while its subroutine runs.",
                 "A global variable can be changed from anywhere."],
                "Global variables make faults easier to trace.",
                "A global can be changed from anywhere, so a fault could come from any part of the program."),
            Bug(["Merge sort uses divide and conquer.",
                 "Backtracking returns to the last decision point when a path fails."],
                "Data mining finds the best route between two places.",
                "That is a job for a heuristic search such as A star. Data mining finds unknown patterns in large "
                "datasets."),
            Bug(["A breakpoint pauses a program at a chosen line.",
                 "Stepping runs a program one line at a time."],
                "Performance modelling means building the real system and timing it.",
                "Performance modelling simulates the system mathematically, which is cheaper and safer than building it "
                "first."),
        ],
    ),
]
