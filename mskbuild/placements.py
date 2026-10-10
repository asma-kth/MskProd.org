"""Where each diagram and tool is embedded.

Placement lives here rather than inside the content modules for one reason: the
content files are long prose and threading directives through them by hand is
how you end up with a diagram in the wrong section. Here the whole map is on
one screen and can be checked against the specification at a glance.

Each key is (course slug, topic slug) and each value maps a section title to
the markup directives appended to the end of that section.
"""

PLACEMENTS = {
    # -------------------------------------------------- GCSE Computer Science
    ("ks4/computer-science", "architecture-of-the-cpu"): {
        "Components of the CPU": ["!diagram cpu-components"],
        "The fetch decode execute cycle": ["!diagram fetch-decode-execute"],
    },
    ("ks4/computer-science", "primary-storage"): {
        "Why primary memory exists": ["!diagram memory-hierarchy"],
    },
    ("ks4/computer-science", "units-of-data"): {
        "Calculating file sizes": ["!tool file-size"],
    },
    ("ks4/computer-science", "binary-and-hexadecimal"): {
        "Binary to denary": ["!diagram binary-place-values", "!tool base-converter"],
        "Binary addition": ["!diagram binary-addition"],
    },
    ("ks4/computer-science", "storing-images"): {
        "Bitmap images": ["!diagram image-representation"],
        "Calculating image file size": ["!tool file-size"],
    },
    ("ks4/computer-science", "storing-sound"): {
        "Analogue to digital": ["!diagram sound-sampling"],
        "Calculating sound file size": ["!tool file-size"],
    },
    ("ks4/computer-science", "networks-and-topologies"): {
        "Client server and peer to peer": ["!diagram client-server-p2p"],
        "Star and mesh topologies": ["!diagram network-topologies"],
    },
    ("ks4/computer-science", "protocols-and-layers"): {
        "Standards and protocols": ["!diagram packet-switching"],
        "Layers": ["!diagram tcp-ip-stack", "!scene tcp-ip-stack-3d"],
    },
    ("ks4/computer-science", "boolean-logic"): {
        "The three gates": ["!diagram logic-gates"],
        "Truth tables for combined circuits": ["!diagram logic-circuit",
                                               "!tool logic-simulator"],
    },
    ("ks4/computer-science", "searching-and-sorting"): {
        "Binary search": ["!diagram binary-search"],
        "Bubble sort": ["!diagram bubble-sort"],
        "Merge sort": ["!diagram merge-sort"],
        "Choosing an algorithm": ["!tool sort-visualiser"],
    },
    ("ks4/computer-science", "designing-algorithms"): {
        "Trace tables": ["!tool trace-table"],
    },

    # ------------------------------------------------------- AQA GCSE 8525
    ("ks4/aqa-computer-science", "searching-algorithms"): {
        "Binary search": ["!diagram binary-search"],
    },
    ("ks4/aqa-computer-science", "sorting-algorithms"): {
        "Bubble sort": ["!diagram bubble-sort"],
        "Merge sort": ["!diagram merge-sort", "!tool sort-visualiser"],
    },
    ("ks4/aqa-computer-science", "number-bases-and-units"): {
        "Converting between the bases": ["!diagram binary-place-values",
                                         "!tool base-converter"],
        "Units of information": ["!tool file-size"],
    },
    ("ks4/aqa-computer-science", "binary-arithmetic-and-shifts"): {
        "Binary addition": ["!diagram binary-addition"],
    },
    ("ks4/aqa-computer-science", "representing-images"): {
        "Bitmap images": ["!diagram image-representation"],
        "Calculating image file size": ["!tool file-size"],
    },
    ("ks4/aqa-computer-science", "representing-sound"): {
        "From analogue to digital": ["!diagram sound-sampling"],
        "Calculating sound file size": ["!tool file-size"],
    },
    ("ks4/aqa-computer-science", "boolean-logic"): {
        "The four gates": ["!diagram logic-gates"],
        "Truth tables for combined circuits": ["!diagram logic-circuit",
                                               "!tool logic-simulator"],
    },
    ("ks4/aqa-computer-science", "systems-architecture"): {
        "Registers and the fetch execute cycle": ["!diagram fetch-decode-execute"],
        "CPU performance and embedded systems": ["!diagram cpu-components"],
    },
    ("ks4/aqa-computer-science", "computer-networks"): {
        "Star and bus topologies": ["!diagram network-topologies"],
    },
    ("ks4/aqa-computer-science", "protocols-and-layers"): {
        "Layers": ["!diagram tcp-ip-stack"],
    },
    ("ks4/aqa-computer-science", "representing-algorithms"): {
        "Trace tables": ["!tool trace-table"],
    },

    # --------------------------------------------------- Edexcel GCSE 1CP2
    ("ks4/edexcel-computer-science", "searching-and-sorting-algorithms"): {
        "Linear search and binary search": ["!diagram binary-search"],
        "Bubble sort": ["!diagram bubble-sort"],
        "Merge sort": ["!diagram merge-sort"],
        "Choosing and comparing": ["!tool sort-visualiser"],
    },
    ("ks4/edexcel-computer-science", "binary-and-hexadecimal"): {
        "Converting between denary and binary": ["!diagram binary-place-values",
                                                 "!tool base-converter"],
    },
    ("ks4/edexcel-computer-science", "truth-tables-and-logic"): {
        "The three logical operators": ["!diagram logic-gates"],
        "Building a truth table that is right": ["!diagram logic-circuit",
                                                 "!tool logic-simulator"],
    },
    ("ks4/edexcel-computer-science", "algorithms-flowcharts-and-pseudocode"): {
        "Trace tables": ["!tool trace-table"],
    },
    ("ks4/edexcel-computer-science", "representing-text-images-and-sound"): {
        "Representing images": ["!diagram image-representation"],
        "Representing sound": ["!diagram sound-sampling", "!tool file-size"],
    },
    ("ks4/edexcel-computer-science", "data-storage-and-compression"): {
        "Units of storage": ["!tool base-converter"],
        "Secondary storage": ["!diagram memory-hierarchy"],
    },
    ("ks4/edexcel-computer-science", "hardware-and-the-processor"): {
        "Inside the CPU": ["!diagram cpu-components", "!diagram fetch-decode-execute"],
    },
    ("ks4/edexcel-computer-science", "networks-and-network-security"): {
        "Networks and topologies": ["!diagram network-topologies"],
        "Protocols and layers": ["!diagram tcp-ip-stack"],
    },
    ("ks4/edexcel-computer-science", "lists-strings-and-files-in-python"): {
        "Lists": ["!diagram linked-list-vs-array"],
    },
    ("ks4/edexcel-computer-science", "developing-and-testing-programs"): {
        "Validation, authentication and testing": ["!tool trace-table"],
    },

    # ------------------------------------------------------------- A Level
    ("ks5", "structure-and-function-of-the-processor"): {
        "Components and registers": ["!diagram cpu-components"],
        "The fetch decode execute cycle in full": ["!diagram fetch-decode-execute"],
        "Performance and architectures": ["!diagram von-neumann-harvard"],
    },
    ("ks5", "input-output-and-storage"): {
        "Storage": ["!diagram memory-hierarchy"],
    },
    ("ks5", "programming-paradigms"): {
        "Little Man Computer and addressing modes": ["!tool lmc"],
    },
    ("ks5", "data-types-and-boolean-algebra"): {
        "Number representation": ["!diagram binary-place-values", "!tool base-converter"],
        "Boolean algebra": ["!diagram karnaugh-map", "!tool logic-simulator"],
    },
    ("ks5", "data-structures"): {
        "Linear structures": ["!diagram linked-list-vs-array", "!diagram stack-queue"],
        "Trees, graphs and hash tables": ["!diagram binary-tree"],
    },
    ("ks5", "algorithms-and-complexity"): {
        "Big O and searching": ["!diagram binary-search"],
        "Sorting algorithms": ["!diagram merge-sort", "!tool sort-visualiser"],
    },
    ("ks5", "networks-and-web-technologies"): {
        "Networks and protocols": ["!diagram tcp-ip-stack"],
    },
    ("ks5", "programming-techniques-and-methods"): {
        "Programming techniques": ["!tool trace-table"],
    },

    # ----------------------------------------------------------- Key Stage 3
    ("ks3", "understanding-computers"): {
        "Binary": ["!diagram binary-place-values", "!tool base-converter"],
        "Units and how everything is stored": ["!tool file-size"],
    },
    ("ks3", "data-representation"): {
        "Binary and hexadecimal": ["!tool base-converter"],
        "Binary addition and units": ["!diagram binary-addition", "!tool file-size"],
        "Representing text, images and sound": ["!diagram image-representation"],
    },
    ("ks3", "networks-and-cyber-security"): {
        "Networks": ["!diagram network-topologies"],
    },
    # ------------------------------- computational thinking, law, character sets
    # Every course that teaches these now has a worked picture rather than three
    # abstract nouns. Section titles below are the real ones; apply() raises at
    # build time if any of them stops existing.
    ("ks4/computer-science", "computational-thinking"): {
        "Algorithmic thinking": ["!diagram computational-thinking"],
    },
    ("ks4/computer-science", "character-encoding"): {
        "ASCII": ["!diagram character-encoding"],
    },
    ("ks4/computer-science", "ethical-legal-cultural-environmental"): {
        "Legislation": ["!diagram uk-computing-law"],
    },
    ("ks4/aqa-computer-science", "computational-thinking"): {
        "Abstraction": ["!diagram computational-thinking"],
    },
    ("ks4/aqa-computer-science", "character-encoding"): {
        "ASCII": ["!diagram character-encoding"],
    },
    ("ks4/aqa-computer-science", "ethical-legal-and-environmental-impacts"): {
        "The four Acts": ["!diagram uk-computing-law"],
    },
    ("ks4/edexcel-computer-science", "decomposition-and-abstraction"): {
        "Using both in an exam answer": ["!diagram computational-thinking"],
    },
    ("ks4/edexcel-computer-science", "legislation-and-privacy"): {
        "The Acts": ["!diagram uk-computing-law"],
    },
    ("ks3", "computational-thinking"): {
        "The four techniques": ["!diagram computational-thinking"],
        "Pseudocode and testing": ["!tool trace-table"],
    },
    ("ks3", "digital-literacy-and-the-law"): {
        "The four laws": ["!diagram uk-computing-law"],
    },
    ("ks5", "elements-of-computational-thinking"): {
        "Abstractly, ahead and procedurally": ["!diagram computational-thinking"],
    },
    ("ks5", "legal-moral-and-ethical-issues"): {
        "Legislation": ["!diagram uk-computing-law"],
    },
    # ------------------------------------------- Key Stage 3 unit diagrams
    # Every KS3 topic now carries a figure. The three programming topics get the
    # idea drawn before the syntax, which is the order Year 7 to 9 need it in.
    ("ks3", "using-computers"): {
        "Hardware and software": ["!diagram ks3-input-process-output"],
    },
    ("ks3", "programming-in-scratch"): {
        "Iteration and events": ["!diagram ks3-scratch-constructs"],
    },
    ("ks3", "introduction-to-python"): {
        "Input and data types": ["!diagram ks3-python-variables"],
    },
    ("ks3", "vector-graphics"): {
        "Bitmap against vector": ["!diagram ks3-bitmap-vector"],
    },
    ("ks3", "digital-literacy"): {
        "Your digital footprint": ["!diagram ks3-digital-footprint"],
    },
    ("ks3", "python-loops-and-lists"): {
        "Loops": ["!diagram ks3-python-loop-trace"],
    },
    ("ks3", "spreadsheets"): {
        "Absolute and relative references": ["!diagram ks3-cell-references"],
    },
    ("ks3", "web-development"): {
        "CSS: style": ["!diagram ks3-html-css-render"],
    },
    ("ks3", "python-programming"): {
        "Lists, 2D lists and dictionaries": ["!diagram ks3-list-vs-dict"],
    },
    ("ks3", "app-development"): {
        "Designing before building": ["!diagram ks3-design-cycle"],
    },
    ("ks3", "artificial-intelligence"): {
        "What AI actually is": ["!diagram ks3-how-ai-learns"],
    },
    ("ks3", "3d-modelling-and-animation"): {
        "How 3D models are built": ["!diagram ks3-3d-pipeline"],
    },

    # ------------------------------------------------------- Creative iMedia
    # Every R093, R094 and R097 topic now carries a worked figure. The
    # pre-production one is deliberately on three topics: the visualisation
    # diagram, storyboard and wireframe are the most frequently swapped answers
    # in the course, and all three units examine them.
    ("ks4/imedia", "the-media-industry"): {
        "Job roles": ["!diagram imedia-production-pipeline"],
    },
    ("ks4/imedia", "factors-influencing-product-design"): {
        "Style, content, layout and media codes": ["!diagram imedia-visual-identity"],
    },
    ("ks4/imedia", "pre-production-planning"): {
        "Pre-production documents": ["!diagram imedia-pre-production"],
        "Work planning, legislation and file management": ["!diagram imedia-file-formats"],
    },
    ("ks4/imedia", "distribution-considerations"): {
        "File properties and compression": ["!diagram imedia-file-formats"],
    },
    ("ks4/imedia", "visual-identity-and-digital-graphics"): {
        "Developing visual identity": ["!diagram imedia-visual-identity"],
        "Planning and creating digital graphics": ["!diagram imedia-pre-production"],
    },
    ("ks4/imedia", "interactive-digital-media"): {
        "Planning an interactive product": ["!diagram imedia-navigation-structures"],
        "Creating and reviewing": ["!diagram imedia-pre-production"],
    },
}


def apply(course):
    """Append the mapped directives to the right sections of a course, in place.

    Raises if a mapping names a topic or a section that does not exist, because a
    silently dropped diagram is worse than a failed build.
    """
    used = set()
    for unit in course.units:
        for topic in unit.topics:
            key = (course.slug, topic.slug)
            if key not in PLACEMENTS:
                continue
            plan = PLACEMENTS[key]
            used.add(key)
            titles = {s.title: s for s in topic.sections}
            for title, directives in plan.items():
                if title not in titles:
                    raise KeyError(
                        "placement for %s/%s names section %r, which does not exist. "
                        "Sections are: %s"
                        % (course.slug, topic.slug, title, ", ".join(titles)))
                sec = titles[title]
                sec.body = sec.body.rstrip() + "\n\n" + "\n\n".join(directives) + "\n"
    return used


def check(all_used):
    """Every mapping must have matched a real topic."""
    missing = set(PLACEMENTS) - all_used
    if missing:
        raise KeyError("placements that matched no topic: %s" % sorted(missing))
