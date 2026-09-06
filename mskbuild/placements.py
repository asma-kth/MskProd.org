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
            plan = PLACEMENTS.get((course.slug, topic.slug))
            if not plan:
                continue
            used.add((course.slug, topic.slug))
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
