"""Where the concept illustrations go, topic by topic and board by board.

OCR, AQA, Edexcel, Key Stage 3 and the Python course teach the same variable,
the same loop and the same translator, so one drawing is placed on every topic
that teaches it. Each call below adds one or more illustrations to the end of a
named section.

This is written as calls rather than as a big dictionary on purpose. A dict
literal silently keeps only the last of a repeated key, which already lost
diagrams from pages twice; a call that adds to what is there cannot.
placements.apply() still raises if a topic or a section named here does not
exist, so a typo fails the build instead of dropping a picture.
"""

OCR = "ks4/computer-science"
AQA = "ks4/aqa-computer-science"
EDX = "ks4/edexcel-computer-science"
KS3 = "ks3"
IMEDIA = "ks4/imedia"
ALEVEL = "ks5"
DATA = "data-analytics"
PY = "python"

PLAN = {}
_SEEN = set()


def put(course, topic, section, *names):
    """Add illustrations to the end of a section."""
    for name in names:
        key = (course, topic, name)
        if key in _SEEN:
            raise ValueError("illustration %r is placed twice on %s/%s" % (name, course, topic))
        _SEEN.add(key)
        PLAN.setdefault((course, topic), {}).setdefault(section, []).append("!illus " + name)


def merge(into):
    """Fold the plan into the main placement table without replacing anything."""
    for key, sections in PLAN.items():
        target = into.setdefault(key, {})
        for title, items in sections.items():
            target.setdefault(title, []).extend(items)


# ================================================================ programming
# ---- OCR GCSE
put(OCR, "programming-fundamentals", "Variables and constants", "variables-boxes")
put(OCR, "programming-fundamentals", "The three constructs", "three-constructs")
put(OCR, "programming-fundamentals", "Operators", "operators")
put(OCR, "data-types-and-casting", "The five data types", "data-types")
put(OCR, "additional-programming-techniques", "String manipulation", "strings-tiles")
put(OCR, "additional-programming-techniques", "Arrays and lists", "lists-lockers")
put(OCR, "additional-programming-techniques", "File handling", "files-flow")
put(OCR, "additional-programming-techniques", "Subroutines and random numbers", "function-machine")
put(OCR, "producing-robust-programs", "Defensive design", "validation-checks", "authentication")
put(OCR, "producing-robust-programs", "Testing", "error-types", "test-data")
put(OCR, "languages-and-ides", "High and low level languages", "language-levels")
put(OCR, "languages-and-ides", "Translators", "translators")
put(OCR, "languages-and-ides", "Integrated development environments", "ide-tour")

# ---- AQA GCSE
put(AQA, "programming-fundamentals", "Data types", "data-types")
put(AQA, "programming-fundamentals", "Variables and constants", "variables-boxes")
put(AQA, "programming-fundamentals", "Operators", "operators")
put(AQA, "programming-fundamentals", "The three constructs", "three-constructs")
put(AQA, "data-structures-and-file-handling", "String handling", "strings-tiles")
put(AQA, "data-structures-and-file-handling", "Files and random numbers", "files-flow")
put(AQA, "subroutines-and-structured-programming", "Procedures and functions", "function-machine")
put(AQA, "subroutines-and-structured-programming", "Scope", "scope-rooms")
put(AQA, "robust-and-secure-programming", "Validation and authentication", "validation-checks", "authentication")
put(AQA, "robust-and-secure-programming", "Testing and the three kinds of error", "error-types", "test-data")
put(AQA, "classification-of-programming-languages", "High and low level languages", "language-levels")
put(AQA, "classification-of-programming-languages", "Translators", "translators")

# ---- Edexcel GCSE
put(EDX, "programming-fundamentals-in-python", "Variables, constants and data types", "variables-boxes", "data-types")
put(EDX, "programming-fundamentals-in-python", "Operators", "operators")
put(EDX, "programming-fundamentals-in-python", "Sequence, selection and iteration", "three-constructs", "selection-fork", "loops-track")
put(EDX, "lists-strings-and-files-in-python", "Lists", "lists-lockers")
put(EDX, "lists-strings-and-files-in-python", "Strings", "strings-tiles")
put(EDX, "lists-strings-and-files-in-python", "Files", "files-flow")
put(EDX, "developing-and-testing-programs", "Subprograms", "function-machine")
put(EDX, "developing-and-testing-programs", "Validation, authentication and testing", "validation-checks", "authentication", "test-data")
put(EDX, "software-and-programming-languages", "Programming languages and translators", "language-levels", "translators")

# ---- Key Stage 3
put(KS3, "introduction-to-python", "Output and variables", "hello-world", "variables-boxes")
put(KS3, "introduction-to-python", "Input and data types", "input-types")
put(KS3, "introduction-to-python", "Making decisions", "selection-fork")
put(KS3, "python-loops-and-lists", "Loops", "loops-track")
put(KS3, "python-loops-and-lists", "Lists", "lists-lockers")
put(KS3, "python-loops-and-lists", "Functions and validation", "function-machine", "validation-checks")
put(KS3, "python-programming", "Structuring a program", "scope-rooms")
put(KS3, "python-programming", "Lists, 2D lists and dictionaries", "dictionary-drawers")
put(KS3, "python-programming", "Files and building a real program", "files-flow")

# ---- A Level
put(ALEVEL, "applications-generation", "Translators and the stages of compilation", "translators")

# ---- the Python course
put(PY, "first-steps", "Your first program", "hello-world")
put(PY, "first-steps", "Reading error messages", "error-types")
put(PY, "variables-and-data-types", "Variables", "variables-boxes")
put(PY, "variables-and-data-types", "Data types", "data-types")
put(PY, "input-and-operators", "Input", "input-types")
put(PY, "input-and-operators", "Operators", "operators")
put(PY, "selection", "Making a decision", "selection-fork")
put(PY, "loops", "for loops", "loops-track")
put(PY, "string-manipulation", "Indexing and slicing", "strings-tiles")
put(PY, "lists", "Lists", "lists-lockers")
put(PY, "functions", "Defining and calling", "function-machine")
put(PY, "functions", "Scope", "scope-rooms")
put(PY, "dictionaries-files-and-errors", "Dictionaries", "dictionary-drawers")
put(PY, "dictionaries-files-and-errors", "Files", "files-flow")
put(PY, "dictionaries-files-and-errors", "Error handling", "try-except")
put(PY, "validation-authentication-and-testing", "Validation and sanitisation", "validation-checks")
put(PY, "validation-authentication-and-testing", "Authentication", "authentication")
put(PY, "tracing-and-debugging", "Finding and fixing errors", "error-types")
put(PY, "tracing-and-debugging", "Debugging tools and techniques", "ide-tour")
put(PY, "subprograms-and-parameters", "Procedures and functions", "function-machine")
put(PY, "arrays-records-and-files", "One dimensional arrays", "lists-lockers")
put(PY, "arrays-records-and-files", "Text files", "files-flow")
put(PY, "pseudocode-to-python", "Data types, casting and operators", "data-types", "operators")


# ============================================ algorithms and computational thinking
# ---- OCR GCSE
put(OCR, "computational-thinking", "Abstraction", "abstraction-map")
put(OCR, "computational-thinking", "Decomposition", "decomposition-tree")
put(OCR, "computational-thinking", "Algorithmic thinking", "ct-four")
put(OCR, "designing-algorithms", "Flowcharts", "flowchart-symbols")
put(OCR, "searching-and-sorting", "Linear search", "search-compare")
put(OCR, "searching-and-sorting", "Bubble sort", "bubble-sort-cards")
put(OCR, "searching-and-sorting", "Merge sort", "merge-sort-cards")
put(OCR, "searching-and-sorting", "Insertion sort", "insertion-sort-cards")

# ---- AQA GCSE
put(AQA, "computational-thinking", "Algorithms and programs", "ct-four")
put(AQA, "computational-thinking", "Decomposition", "decomposition-tree")
put(AQA, "computational-thinking", "Abstraction", "abstraction-map")
put(AQA, "representing-algorithms", "Flowcharts", "flowchart-symbols")
put(AQA, "searching-algorithms", "Linear search", "search-compare")
put(AQA, "sorting-algorithms", "Bubble sort", "bubble-sort-cards")
put(AQA, "sorting-algorithms", "Merge sort", "merge-sort-cards")

# ---- Edexcel GCSE
put(EDX, "decomposition-and-abstraction", "Decomposition: breaking the problem up", "decomposition-tree")
put(EDX, "decomposition-and-abstraction", "Abstraction: deciding what to ignore", "abstraction-map")
put(EDX, "algorithms-flowcharts-and-pseudocode", "Flowcharts", "flowchart-symbols")
put(EDX, "searching-and-sorting-algorithms", "Linear search and binary search", "search-compare")
put(EDX, "searching-and-sorting-algorithms", "Bubble sort", "bubble-sort-cards")
put(EDX, "searching-and-sorting-algorithms", "Merge sort", "merge-sort-cards")

# ---- Key Stage 3
put(KS3, "computational-thinking", "The four techniques", "ct-four")
put(KS3, "computational-thinking", "Flowcharts", "flowchart-symbols")

# ---- A Level
put(ALEVEL, "elements-of-computational-thinking", "Abstractly, ahead and procedurally", "abstraction-map", "decomposition-tree")
put(ALEVEL, "algorithms-and-complexity", "Big O and searching", "big-o-growth", "search-compare")
put(ALEVEL, "algorithms-and-complexity", "Sorting algorithms", "merge-sort-cards")
put(ALEVEL, "algorithms-and-complexity", "Graph and tree algorithms", "shortest-path", "graph-traversal")

# ---- the Python course
put(PY, "searching-and-sorting", "Linear and binary search", "search-compare")
put(PY, "searching-and-sorting", "Bubble sort and insertion sort", "bubble-sort-cards", "insertion-sort-cards")
put(PY, "searching-and-sorting", "Merge sort", "merge-sort-cards")


# ================================================== data representation
# ---- OCR GCSE
put(OCR, "binary-and-hexadecimal", "Hexadecimal", "hex-nibbles")
put(OCR, "binary-and-hexadecimal", "Binary addition", "binary-overflow")
put(OCR, "binary-and-hexadecimal", "Binary shifts", "binary-shifts")
put(OCR, "character-encoding", "ASCII", "char-codes")
put(OCR, "storing-images", "Metadata", "image-metadata")

# ---- AQA GCSE
put(AQA, "number-bases-and-units", "Converting between the bases", "hex-nibbles")
put(AQA, "binary-arithmetic-and-shifts", "Overflow", "binary-overflow")
put(AQA, "binary-arithmetic-and-shifts", "Binary shifts", "binary-shifts")
put(AQA, "character-encoding", "ASCII", "char-codes")
put(AQA, "representing-images", "Metadata", "image-metadata")
put(AQA, "data-compression", "Run length encoding", "rle-encoding")
put(AQA, "data-compression", "Huffman coding", "huffman-tree")

# ---- Edexcel GCSE
put(EDX, "binary-and-hexadecimal", "Hexadecimal", "hex-nibbles")
put(EDX, "representing-text-images-and-sound", "Representing text", "char-codes")
put(EDX, "representing-text-images-and-sound", "Representing images", "image-metadata")

# ---- Key Stage 3
put(KS3, "data-representation", "Binary and hexadecimal", "hex-nibbles")
put(KS3, "data-representation", "Binary addition and units", "binary-overflow")
put(KS3, "data-representation", "Representing text, images and sound", "char-codes", "image-metadata")

# ---- the Python course
put(PY, "binary-and-bitwise-operations", "Bitwise operations", "binary-shifts")
put(PY, "binary-and-bitwise-operations", "Floating point and characters", "char-codes")


# ================================================== how the computer system works
# ---- OCR GCSE
put(OCR, "systems-software", "The operating system", "os-jobs")
put(OCR, "systems-software", "Utility software", "utilities")

# ---- AQA GCSE
put(AQA, "hardware-software-and-the-operating-system", "Hardware and software", "hardware-software")
put(AQA, "hardware-software-and-the-operating-system", "System software and the operating system", "os-jobs")
put(AQA, "hardware-software-and-the-operating-system", "Utility software", "utilities")

# ---- Edexcel GCSE
put(EDX, "software-and-programming-languages", "System and application software", "os-jobs")
put(EDX, "software-and-programming-languages", "Utility software", "utilities")

# ---- Key Stage 3
put(KS3, "using-computers", "Hardware and software", "hardware-software")

# ---- A Level
put(ALEVEL, "structure-and-function-of-the-processor", "Performance and architectures", "pipelining")
put(ALEVEL, "types-of-processor", "RISC and CISC", "risc-cisc")
put(ALEVEL, "systems-software", "Memory management and scheduling", "scheduling")
put(ALEVEL, "systems-software", "Types of operating system and other functions", "os-jobs")
put(ALEVEL, "input-output-and-storage", "Devices and how they work", "input-devices-how", "output-devices-how")


# ================================================== networks, security, law and impact
# ---- OCR GCSE
put(OCR, "networks-and-topologies", "Factors affecting network performance", "network-factors")
put(OCR, "protocols-and-layers", "IP addresses and MAC addresses", "ip-mac")
put(OCR, "protocols-and-layers", "Standards and protocols", "email-protocols")
put(OCR, "network-security", "Forms of attack", "cyber-threats", "phishing-email")
put(OCR, "network-security", "Preventing attacks", "cyber-defences", "password-strength")
put(OCR, "ethical-legal-cultural-environmental", "The four categories", "tech-impact")
put(OCR, "ethical-legal-cultural-environmental", "Legislation", "licences")

# ---- AQA GCSE
put(AQA, "protocols-and-layers", "What a protocol is", "email-protocols")
put(AQA, "cyber-security", "What cyber security is, and social engineering", "phishing-email")
put(AQA, "cyber-security", "Malicious code and other threats", "cyber-threats")
put(AQA, "cyber-security", "Detecting and preventing attacks", "cyber-defences", "password-strength")
put(AQA, "ethical-legal-and-environmental-impacts", "The four Acts", "licences")
put(AQA, "ethical-legal-and-environmental-impacts", "Ethical and environmental issues", "tech-impact")

# ---- Edexcel GCSE
put(EDX, "networks-and-network-security", "Protocols and layers", "ip-mac", "email-protocols")
put(EDX, "networks-and-network-security", "Threats and protection", "cyber-threats", "cyber-defences", "password-strength")
put(EDX, "legislation-and-privacy", "Software licensing", "licences")
put(EDX, "legislation-and-privacy", "Privacy in practice", "data-trail")
put(EDX, "issues-and-impact-of-technology", "Ethical, cultural and privacy issues", "tech-impact")

# ---- Key Stage 3
put(KS3, "digital-literacy", "Your digital footprint", "data-trail")
put(KS3, "digital-literacy", "Scams, phishing and misinformation", "phishing-email")
put(KS3, "digital-literacy", "Protecting yourself", "password-strength")
put(KS3, "networks-and-cyber-security", "The internet and the web", "email-protocols")
put(KS3, "networks-and-cyber-security", "Cyber security", "cyber-threats", "cyber-defences")
put(KS3, "digital-literacy-and-the-law", "Ethics and the impact of technology", "tech-impact")

# ---- A Level
put(ALEVEL, "legal-moral-and-ethical-issues", "Legislation", "licences")


# ================================================== Key Stage 3
put(KS3, "using-computers", "Files and folders", "files-folders")
put(KS3, "using-computers", "Staying safe and being organised", "password-strength")
put(KS3, "programming-in-scratch", "Sequence", "scratch-blocks")
put(KS3, "vector-graphics", "Working with vector shapes", "vector-nodes")
put(KS3, "vector-graphics", "Designing a good logo", "logo-design")
put(KS3, "digital-literacy", "Protecting yourself", "two-factor", "report-it")
put(KS3, "spreadsheets", "Formulas and functions", "spreadsheet-anatomy")
put(KS3, "spreadsheets", "Modelling, charts and good design", "chart-choice")
put(KS3, "web-development", "HTML: structure", "html-css-anatomy")
put(KS3, "app-development", "User interface design", "app-ui-design")
put(KS3, "app-development", "Testing and evaluation", "test-data")
put(KS3, "artificial-intelligence", "Bias, error and responsibility", "ai-bias")
put(KS3, "3d-modelling-and-animation", "Materials, lighting and cameras", "lights-camera")
put(KS3, "3d-modelling-and-animation", "Animation and rendering", "keyframes")


# ================================================== A Level
put(ALEVEL, "applications-generation", "Translators and the stages of compilation", "compilation-stages")
put(ALEVEL, "applications-generation", "Development methodologies", "methodologies")
put(ALEVEL, "programming-paradigms", "Paradigms", "paradigms")
put(ALEVEL, "programming-paradigms", "Little Man Computer and addressing modes", "lmc-machine", "addressing-modes")
put(ALEVEL, "compression-encryption-and-hashing", "Encryption and hashing", "hashing")
put(ALEVEL, "data-structures", "Trees, graphs and hash tables", "hash-table")
put(ALEVEL, "networks-and-web-technologies", "Web technologies", "web-tech-split")
put(ALEVEL, "data-types-and-boolean-algebra", "Number representation", "twos-complement", "floating-point")
put(ALEVEL, "elements-of-computational-thinking", "Logically and concurrently", "concurrency")
put(ALEVEL, "databases", "SQL, indexing and transactions", "sql-anatomy", "acid")
put(ALEVEL, "nea-programming-project", "Analysis and design", "nea-lifecycle")
put(ALEVEL, "nea-programming-project", "Development, testing and evaluation", "test-levels")

# ================================================== the Python course, object oriented and advanced
put(PY, "classes-and-objects", "The idea", "class-object")
put(PY, "classes-and-objects", "Encapsulation", "encapsulation")
put(PY, "inheritance-and-polymorphism", "Inheritance", "inheritance-tree")
put(PY, "inheritance-and-polymorphism", "Polymorphism", "polymorphism")
put(PY, "oop-design", "Inheritance, overriding and abstract classes", "inheritance-tree")
put(PY, "oop-design", "Composition, aggregation and association", "oop-relationships")
put(PY, "recursion", "Problems that recurse: Hanoi, nesting and backtracking", "hanoi")
put(PY, "linked-lists-and-hash-tables", "Hash tables", "hash-table")
put(PY, "binary-and-bitwise-operations", "Two's complement", "twos-complement")
put(PY, "binary-and-bitwise-operations", "Floating point and characters", "floating-point")
put(PY, "databases-and-sql", "Searching with SELECT", "sql-anatomy")
put(PY, "relational-databases-and-sql", "Transactions and ACID", "acid")
put(PY, "testing-and-tdd", "Levels and kinds of testing", "test-levels")
put(PY, "testing-and-tdd", "Test-driven development", "tdd-cycle")
put(PY, "programming-project", "What the project rewards", "nea-lifecycle")
put(PY, "tkinter-gui-programming", "Widgets and layout", "tk-widgets")
put(PY, "pygame-game-programming", "The game loop", "game-loop")
put(PY, "pygame-game-programming", "Rects, collisions and sprites", "collision-rects")


# ================================================== Creative iMedia and OCR Data Analytics
put(IMEDIA, "the-media-industry", "Types of product", "media-products")
put(IMEDIA, "target-audience-and-segmentation", "Describing an audience", "persona-card")
put(IMEDIA, "research-methods-and-sources", "Primary and secondary research", "research-methods")
put(IMEDIA, "file-formats-and-properties", "Audio, video and document formats", "media-file-types")
put(IMEDIA, "legislation-and-permissions", "People, data and privacy", "permissions-chain")
put(IMEDIA, "work-planning-and-workflow", "Risk, contingency and resources", "risk-matrix")
put(IMEDIA, "distribution-platforms", "Choosing and comparing platforms", "platform-compare")
put(IMEDIA, "creating-digital-graphics", "Vector techniques", "vector-nodes")
put(IMEDIA, "interactive-digital-media", "Interface design and accessibility", "app-ui-design")

put(DATA, "roles-skills-and-attributes", "The roles", "data-roles")
put(DATA, "the-scope-of-big-data", "The impacts of big data", "big-data-impacts")
put(DATA, "legal-and-ethical-issues", "Bias, fairness and transparency", "ai-bias")


# ================================================== the thinnest topics
# ---- tracing
put(OCR, "designing-algorithms", "Trace tables", "trace-table-walk")
put(AQA, "representing-algorithms", "Trace tables", "trace-table-walk")
put(EDX, "algorithms-flowcharts-and-pseudocode", "Trace tables", "trace-table-walk")
put(KS3, "computational-thinking", "Pseudocode and testing", "trace-table-walk")
put(PY, "tracing-and-debugging", "Trace tables", "trace-table-walk")

# ---- casting
put(OCR, "data-types-and-casting", "Casting", "casting")
put(AQA, "programming-fundamentals", "Data types", "casting")
put(EDX, "programming-fundamentals-in-python", "Variables, constants and data types", "casting")
put(KS3, "introduction-to-python", "Input and data types", "casting")
put(PY, "variables-and-data-types", "Data types", "casting")
put(PY, "input-and-operators", "Input", "casting")

# ---- compression
put(OCR, "compression", "Choosing between them", "lossy-lossless")
put(AQA, "data-compression", "Why compress at all", "lossy-lossless")
put(EDX, "data-storage-and-compression", "Compression", "lossy-lossless")
put(ALEVEL, "compression-encryption-and-hashing", "Compression", "lossy-lossless")
put(KS3, "understanding-computers", "Units and how everything is stored", "lossy-lossless")

# ---- the environment
put(OCR, "ethical-legal-cultural-environmental", "The four categories", "tech-lifecycle")
put(AQA, "ethical-legal-and-environmental-impacts", "Ethical and environmental issues", "tech-lifecycle")
put(EDX, "issues-and-impact-of-technology", "Environmental impact", "tech-lifecycle")
put(KS3, "artificial-intelligence", "The wider impact of computing", "tech-lifecycle")

# ---- sorting in depth, A Level
put(PY, "sorting-algorithms", "Quick sort", "quick-sort-cards")
put(PY, "sorting-algorithms", "Stability, and the sort you will actually use", "sort-stability")
put(ALEVEL, "algorithms-and-complexity", "Sorting algorithms", "quick-sort-cards", "sort-stability")
put(PY, "stacks-and-queues", "Stacks", "stack-queue")
put(PY, "dijkstra-and-a-star", "Dijkstra's shortest path algorithm", "shortest-path")
put(PY, "trees-and-graphs", "Breadth first and depth first traversal", "graph-traversal")
put(PY, "big-o-and-complexity", "Counting steps, not seconds", "big-o-growth")

# ---- computational methods
put(ALEVEL, "programming-techniques-and-methods", "Computational methods", "computational-methods")
put(ALEVEL, "programming-techniques-and-methods", "Programming techniques", "hanoi")

# ---- Python: loops, strings, lists, selection
put(PY, "loops", "while loops", "while-loops")
put(PY, "string-manipulation", "String methods", "string-methods")
put(PY, "lists", "Lists", "list-methods")
put(PY, "selection", "Patterns that keep selection readable", "selection-flatten")
put(KS3, "python-loops-and-lists", "Loops", "while-loops")
put(KS3, "python-loops-and-lists", "Lists", "list-methods")
put(OCR, "additional-programming-techniques", "String manipulation", "string-methods")
put(EDX, "lists-strings-and-files-in-python", "Strings", "string-methods")
put(AQA, "data-structures-and-file-handling", "String handling", "string-methods")


# ================================================== the last gaps
# ---- file sizes
put(OCR, "units-of-data", "Calculating file sizes", "file-size-formulas")
put(OCR, "storing-images", "Calculating image file size", "file-size-formulas")
put(AQA, "number-bases-and-units", "Units of information", "file-size-formulas")
put(AQA, "representing-sound", "Calculating sound file size", "file-size-formulas")
put(EDX, "data-storage-and-compression", "Units of storage", "file-size-formulas")
put(KS3, "understanding-computers", "Units and how everything is stored", "file-size-formulas")

# ---- algorithms
put(OCR, "designing-algorithms", "Flowcharts", "flowchart-to-code")
put(AQA, "representing-algorithms", "Flowcharts", "flowchart-to-code")
put(EDX, "algorithms-flowcharts-and-pseudocode", "Flowcharts", "flowchart-to-code")
put(KS3, "computational-thinking", "Flowcharts", "flowchart-to-code")
put(PY, "pseudocode-to-python", "Translating whole algorithms", "flowchart-to-code")
put(PY, "stacks-and-queues", "Expressions: infix, postfix and the shunting yard", "postfix-stack")
put(ALEVEL, "data-structures", "Linear structures", "postfix-stack")
put(PY, "sorting-algorithms", "Counting the work", "sort-compare")
put(ALEVEL, "algorithms-and-complexity", "Sorting algorithms", "sort-compare")
put(PY, "dijkstra-and-a-star", "A* search", "a-star-heuristic")
put(ALEVEL, "algorithms-and-complexity", "Graph and tree algorithms", "a-star-heuristic")

# ---- testing and applications in Python, and SQL at GCSE
put(PY, "testing-and-tdd", "Unit tests with unittest", "unittest-run")
put(PY, "tkinter-gui-programming", "Widgets and layout", "tk-grid")
put(AQA, "relational-databases-and-sql", "SQL: retrieving data", "sql-anatomy")
put(OCR, "additional-programming-techniques", "SQL", "sql-anatomy")

# ---- Python: A Level structures, algorithms, theory of computation, machines and systems
put(PY, "heaps-tries-and-disjoint-sets", "The binary heap", "heap-array")
put(PY, "heaps-tries-and-disjoint-sets", "Tries: searching by prefix", "trie-tree")
put(PY, "heaps-tries-and-disjoint-sets", "Disjoint sets and union-find", "union-find")
put(PY, "heaps-tries-and-disjoint-sets", "Minimum spanning trees", "mst-kruskal")
put(PY, "dynamic-programming-and-greedy", "Greedy algorithms", "greedy-vs-optimal")
put(PY, "dynamic-programming-and-greedy", "Dynamic programming", "dp-coin-table")
put(PY, "finite-state-machines-and-regex", "Finite state machines", "fsm-states")
put(PY, "grammars-parsing-and-compilers", "Lexical analysis: from text to tokens", "compilation-stages")
put(PY, "grammars-parsing-and-compilers", "Syntax analysis: a recursive descent parser", "ast-precedence")
put(PY, "grammars-parsing-and-compilers", "Code generation, a stack machine and optimisation", "postfix-stack")
put(PY, "turing-machines-and-halting", "The Turing machine", "turing-tape")
put(PY, "turing-machines-and-halting", "The halting problem", "halting-paradox")
put(PY, "turing-machines-and-halting", "Tractable and intractable problems", "big-o-growth")
put(PY, "turing-machines-and-halting", "Abstraction and automation", "abstraction-map")
put(PY, "little-man-computer", "Inside the processor: fetch, decode, execute", "fde-registers")
put(PY, "little-man-computer", "The Little Man Computer", "lmc-machine")
put(PY, "little-man-computer", "Addressing modes and the pipeline", "addressing-modes", "pipelining")
put(PY, "scheduling-and-concurrency", "Sharing one processor: scheduling", "scheduling")
put(PY, "scheduling-and-concurrency", "Race conditions and locks", "race-lost-update")
put(PY, "scheduling-and-concurrency", "Deadlock", "deadlock-cycle")
put(PY, "scheduling-and-concurrency", "Threads, processes and parallel speed-up", "parallel-cores", "concurrency")
put(PY, "compression-encryption-hashing", "Compression: run length and dictionary coding", "rle-encoding")
put(PY, "compression-encryption-hashing", "Huffman coding", "huffman-tree")
put(PY, "compression-encryption-hashing", "Encryption: ciphers old and new", "encryption")
put(PY, "compression-encryption-hashing", "Public key cryptography", "rsa-keys")
put(PY, "compression-encryption-hashing", "Hashing and storing passwords", "hashing")
put(PY, "networks-and-the-web", "Protocols, layers and packets", "tcp-ip-stack", "packet-journey")
put(PY, "networks-and-the-web", "IP addresses and subnets", "subnet-mask", "ip-mac")
put(PY, "networks-and-the-web", "Reliable delivery over an unreliable network", "tcp-ack-retransmit")
put(PY, "networks-and-the-web", "The web: URLs, HTTP and JSON", "web-request", "web-tech-split")
put(PY, "networks-and-the-web", "Sockets and servers on your own computer", "client-server")

# ---- Python: advanced Python
put(PY, "names-objects-and-memory", "Variables are names, not boxes", "names-objects")
put(PY, "names-objects-and-memory", "Copying: aliases, shallow and deep", "copy-depth")
put(PY, "iterators-and-generators", "Generators: functions that pause", "generator-pause")
put(PY, "iterators-and-generators", "Pipelines: processing data of any size", "pipeline-stages")
put(PY, "closures-decorators-and-context-managers", "Decorators", "decorator-wrap")
put(PY, "closures-decorators-and-context-managers", "Context managers and the with statement", "with-block")
put(PY, "special-methods-dataclasses-and-typing", "The data model: special methods", "dunder-map")
put(PY, "exceptions-logging-and-defensive-code", "The try statement in full", "exception-flow")
put(PY, "the-standard-library-toolbox", "collections: the right container for the job", "stdlib-toolbox")
put(PY, "working-like-a-professional", "Version control with Git", "git-branches")

# ---- Python: simulation and machine learning
put(PY, "simulation-and-modelling", "Monte Carlo: answering questions by sampling", "monte-carlo-pi")
put(PY, "simulation-and-modelling", "Random walks, growth and spreading models", "epidemic-curves")
put(PY, "simulation-and-modelling", "Cellular automata: the Game of Life", "life-glider")
put(PY, "machine-learning-from-scratch", "k-nearest neighbours", "knn-vote")
put(PY, "machine-learning-from-scratch", "Fitting a line by gradient descent", "gradient-descent")
put(PY, "machine-learning-from-scratch", "The perceptron and a small neural network", "neural-network")
put(PY, "machine-learning-from-scratch", "Measuring a model, and being fair", "confusion-matrix", "ai-bias")
put(PY, "finite-state-machines-and-regex", "Regular expressions", "regex-anatomy")
put(PY, "exceptions-logging-and-defensive-code", "Logging", "log-levels")
