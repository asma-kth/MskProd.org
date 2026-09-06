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
        "Layers": ["!diagram tcp-ip-stack"],
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
    ("ks3", "computational-thinking"): {
        "Pseudocode and testing": ["!tool trace-table"],
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
