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
        "Why primary memory exists": ["!diagram memory-hierarchy", "!illus memory-hierarchy"],
    },
    ("ks4/computer-science", "units-of-data"): {
        "Calculating file sizes": ["!tool file-size"],
    },
    ("ks4/computer-science", "binary-and-hexadecimal"): {
        "Binary to denary": ["!diagram binary-place-values", "!illus binary-place-value",
                             "!tool base-converter"],
        "Binary addition": ["!diagram binary-addition"],
    },
    ("ks4/computer-science", "storing-images"): {
        "Bitmap images": ["!diagram image-representation", "!illus image-layers"],
        "Calculating image file size": ["!tool file-size"],
    },
    ("ks4/computer-science", "storing-sound"): {
        "Analogue to digital": ["!diagram sound-sampling", "!illus sound-sampling"],
        "Calculating sound file size": ["!tool file-size"],
    },
    ("ks4/computer-science", "networks-and-topologies"): {
        "Client server and peer to peer": ["!diagram client-server-p2p", "!illus client-server"],
        "Star and mesh topologies": ["!diagram network-topologies", "!illus network-topologies"],
    },
    ("ks4/computer-science", "protocols-and-layers"): {
        "Standards and protocols": ["!diagram packet-switching", "!illus packet-journey"],
        "Layers": ["!diagram tcp-ip-stack", "!illus tcp-ip-stack"],
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
        "Representing text, images and sound": ["!diagram image-representation",
                                                "!illus image-layers"],
    },
    ("ks3", "networks-and-cyber-security"): {
        "Networks": ["!diagram network-topologies", "!illus network-topologies"],
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

    # ------------------------------------------------- OCR Data Analytics
    # This course earns the most figures on the site, and the reason is in the
    # subject: a distribution, a correlation, an overfitted curve and a
    # confusion matrix are objects you have to see to reason about. Three of
    # these are real plotted graphs and two are live tools, because the
    # argument they make, that accuracy is misleading and that one outlier can
    # carry a whole correlation, lands when the reader moves the slider.
    ("data-analytics", "understanding-data"): {
        "Data, information, knowledge and wisdom": ["!diagram data-dikw"],
        "Types and classifications of data": ["!diagram data-types-tree"],
        "Data file formats": ["!diagram data-file-formats"],
    },
    ("data-analytics", "managing-data"): {
        "The data lifecycle and the analytics pipeline": ["!diagram data-pipeline"],
        "Gathering and storing data": ["!diagram data-store-choice",
                                       "!illus data-stack"],
        "Transformation, data quality and assurance": ["!diagram data-etl-elt",
                                                       "!diagram data-cleaning"],
    },
    ("data-analytics", "data-across-platforms"): {
        "APIs and moving data between systems": ["!diagram data-api-request"],
        "Interoperability and integration patterns": ["!diagram data-interoperability"],
        "Access control, security and the cloud": ["!diagram data-access-control"],
    },
    ("data-analytics", "legal-considerations"): {
        "The UK GDPR and the Data Protection Act 2018": ["!diagram data-gdpr"],
        "The other legislation by name": ["!diagram uk-computing-law"],
        "Ethics, retention and destruction": ["!diagram data-retention",
                                              "!diagram data-anonymisation"],
    },
    ("data-analytics", "roles-skills-and-attributes"): {
        "Technical skills": ["!diagram data-distribution",
                             "!diagram data-correlation",
                             "!tool correlation-lab"],
        "Personal attributes and communicating results": ["!diagram data-chart-choice"],
    },
    ("data-analytics", "the-scope-of-big-data"): {
        "What makes data big": ["!diagram data-five-vs",
                                "!diagram data-units-scale"],
        "Where big data comes from": ["!diagram data-big-data-sources",
                                      "!illus data-stack"],
    },
    ("data-analytics", "big-data-infrastructure"): {
        "Storage at scale": ["!diagram data-store-choice"],
        "Network and movement": ["!diagram data-scaling"],
        "Processing and computing power": ["!diagram data-processing-models",
                                           "!illus parallel-cores",
                                           "!photo server-rack"],
    },
    ("data-analytics", "machine-learning-and-ai"): {
        "The three kinds of learning, and the tasks": ["!diagram data-ml-types",
                                                       "!illus neural-network"],
        "AI, machine learning and deep learning": ["!diagram data-ml-applications"],
        "Measuring whether a model works": ["!diagram data-ml-workflow",
                                            "!diagram data-confusion-matrix",
                                            "!tool confusion-matrix",
                                            "!diagram data-overfitting"],
    },
    ("data-analytics", "legal-and-ethical-issues"): {
        "Data protection at big data scale": ["!diagram data-gdpr"],
        "Bias, fairness and transparency": ["!diagram data-bias-sources"],
        "Ownership, security and accountability": ["!diagram data-anonymisation"],
    },
    ("data-analytics", "environment-and-society"): {
        "The environmental cost": ["!diagram data-energy"],
        "Green computing": ["!diagram data-green-computing"],
        "Society, work and culture": ["!diagram data-society-impacts"],
    },

    # ------------------------------------------------------- Creative iMedia
    # iMedia earns more figures per topic than any other course, because the
    # specification is almost entirely about recognising and comparing things
    # you can see: a storyboard against a visualisation diagram, a low angle
    # against a high angle, CMYK against RGB. Describing any of those in prose
    # is strictly harder than drawing it.
    ("ks4/imedia", "the-media-industry"): {
        "The sectors": ["!diagram imedia-sectors-products"],
        "Purpose": ["!diagram imedia-purpose-wheel"],
    },
    ("ks4/imedia", "job-roles-in-media"): {
        "Pre-production roles": ["!diagram imedia-production-pipeline"],
        "Production and post-production roles": ["!illus imedia-phases"],
    },
    ("ks4/imedia", "client-requirements-and-the-brief"): {
        "What a client brief contains": ["!diagram imedia-brief-anatomy"],
        "Constraints and limitations": ["!diagram imedia-constraints"],
    },
    ("ks4/imedia", "target-audience-and-segmentation"): {
        "Describing an audience": ["!diagram imedia-audience-segments"],
        "How the audience changes the product": ["!diagram imedia-accessibility"],
    },
    ("ks4/imedia", "research-methods-and-sources"): {
        "Quantitative and qualitative data": ["!diagram imedia-research-matrix"],
        "Judging a source": ["!diagram imedia-source-check"],
    },
    ("ks4/imedia", "style-content-and-layout"): {
        "Style: colour and typography": ["!diagram imedia-visual-identity"],
        "Layout and composition": ["!diagram imedia-layout-conventions"],
        "Media codes and conventions": ["!diagram imedia-camera-codes"],
    },
    ("ks4/imedia", "pre-production-documents"): {
        "Documents for generating ideas": ["!diagram imedia-mindmap-example",
                                           "!diagram imedia-moodboard-example",
                                           "!photo moodboard-bakery"],
        "Documents for designing and planning": ["!diagram imedia-pre-production",
                                                 "!diagram imedia-visualisation-anatomy",
                                                 "!photo storyboard-sketch",
                                                 "!diagram imedia-storyboard-example",
                                                 "!illus imedia-storyboard",
                                                 "!diagram imedia-script-example"],
        "Wireframes, navigation diagrams and asset tables": [
            "!diagram imedia-navigation-structures",
            "!illus imedia-navigation-depth",
            "!diagram imedia-asset-table-example"],
        "What every pre-production document must carry": [
            "!diagram imedia-doc-essentials"],
    },
    ("ks4/imedia", "work-planning-and-workflow"): {
        "What a work plan contains": ["!diagram imedia-work-plan"],
        "Workflow and the production phases": ["!illus imedia-phases"],
    },
    ("ks4/imedia", "legislation-and-permissions"): {
        "Copyright and intellectual property": ["!diagram imedia-licence-check"],
        "Regulation and certification": ["!diagram uk-computing-law"],
    },
    ("ks4/imedia", "file-formats-and-properties"): {
        "Image formats": ["!diagram imedia-raster-vector",
                          "!diagram imedia-file-formats"],
        "Properties, compression and fitness for purpose": [
            "!diagram imedia-compression-types", "!diagram imedia-colour-modes"],
    },
    ("ks4/imedia", "distribution-platforms"): {
        "Physical and online distribution": ["!diagram imedia-distribution-routes"],
        "Platforms and what they demand": ["!diagram imedia-streaming-download"],
    },
    ("ks4/imedia", "visual-identity-and-digital-graphics"): {
        "What visual identity is": ["!diagram imedia-visual-identity",
                                    "!diagram imedia-logo-types"],
        "Interpreting the brief and researching": ["!diagram imedia-moodboard-example",
                                                   "!photo moodboard-bakery"],
    },
    ("ks4/imedia", "planning-digital-graphics"): {
        "Visualisation diagrams and asset tables": [
            "!diagram imedia-visualisation-anatomy",
            "!diagram imedia-asset-table-example"],
    },
    ("ks4/imedia", "creating-digital-graphics"): {
        "Raster techniques": ["!illus graphics-layers"],
    },
    ("ks4/imedia", "interactive-digital-media"): {
        "Types of interactive product and their structures": [
            "!diagram imedia-navigation-structures"],
        "Navigation diagrams and wireframes": ["!diagram imedia-wireframe-example",
                                               "!illus imedia-navigation-depth"],
        "Interface design and accessibility": ["!diagram imedia-accessibility"],
    },
    ("ks4/imedia", "creating-and-testing-interactive-media"): {
        "Building in the right order": ["!illus graphics-layers"],
    },
    ("ks4/imedia", "reviewing-interactive-media"): {
        "Testing": ["!diagram imedia-test-record"],
        "Reviewing and improving": ["!diagram imedia-review-quality"],
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



# Illustration placements are kept apart from the table above and merged into
# it, rather than written as more entries in the same literal. A dict literal
# keeps only the last of a repeated key, and almost every topic that wants an
# illustration already has a line above for its diagrams: written inline,
# fifteen of them quietly replaced the diagram placements they were meant to join.
ILLUSTRATIONS = {
    ("ks5", "types-of-processor"): {
        "GPUs and parallel systems": ["!illus parallel-cores"],
    },
    ("ks3", "networks-and-cyber-security"): {
        "The internet and the web": ["!illus web-request"],
    },
    ("ks4/aqa-computer-science", "data-structures-and-file-handling"): {
        "Arrays and records": ["!illus array-2d"],
    },
    ("ks4/computer-science", "networks-and-topologies"): {
        "LAN and WAN": ["!illus lan-wan"],
    },
    ("ks4/computer-science", "embedded-systems"): {
        "Embedded versus general purpose": ["!illus embedded-systems"],
    },
    ("ks3", "3d-modelling-and-animation"): {
        "How 3D models are built": ["!illus mesh"],
    },
    ("ks3", "vector-graphics"): {
        "Working with vector shapes": ["!illus graphics-layers"],
    },
    ("ks4/computer-science", "compression"): {
        "Why compress": ["!illus compression"],
    },
    ("ks4/aqa-computer-science", "data-compression"): {
        "Why compress at all": ["!illus compression"],
    },
    ("ks5", "compression-encryption-and-hashing"): {
        "Compression": ["!illus compression"],
        "Encryption and hashing": ["!illus encryption"],
    },
    ("ks4/computer-science", "network-security"): {
        "Preventing attacks": ["!illus encryption"],
    },
    ("ks4/computer-science", "units-of-data"): {
        "The units": ["!illus units-of-data"],
    },
    ("ks4/computer-science", "cpu-performance"): {
        "The three factors": ["!illus cpu-performance"],
    },
    ("ks4/computer-science", "boolean-logic"): {
        "Truth tables for combined circuits": ["!illus logic-circuit"],
    },
    ("ks4/aqa-computer-science", "boolean-logic"): {
        "Reading and drawing circuit diagrams": ["!illus logic-circuit"],
    },
    ("ks4/edexcel-computer-science", "truth-tables-and-logic"): {
        "Logic in real systems and real programs": ["!illus logic-circuit"],
    },
    ("ks5", "data-types-and-boolean-algebra"): {
        "Boolean algebra": ["!illus logic-circuit"],
    },
    ("ks5", "data-structures"): {
        "Linear structures": ["!illus stack-queue"],
        "Trees, graphs and hash tables": ["!illus binary-tree"],
    },
    ("ks4/aqa-computer-science", "relational-databases-and-sql"): {
        "Relational database structure": ["!illus database-tables"],
    },
    ("ks5", "databases"): {
        "Structure and normalisation": ["!illus database-tables"],
    },
    ("ks4/computer-science", "systems-software"): {
        "What system software is": ["!illus abstraction-layers"],
    },
    ("ks4/aqa-computer-science", "hardware-software-and-the-operating-system"): {
        "System software and the operating system": ["!illus abstraction-layers"],
    },
    ("ks4/edexcel-computer-science", "software-and-programming-languages"): {
        "System and application software": ["!illus abstraction-layers"],
    },
    ("ks4/computer-science", "primary-storage"): {
        "Virtual memory": ["!illus virtual-memory"],
    },
    ("ks5", "systems-software"): {
        "Memory management and scheduling": ["!illus virtual-memory"],
    },
    # ------------------------------------------------------- illustrations
    # Only on topics whose subject is easier to see than to read: layers,
    # stacks, hardware, movement through a network. Everything else keeps its
    # flat stepped diagram.
    ("ks4/computer-science", "architecture-of-the-cpu"): {
        "Components of the CPU": ["!illus cpu-board"],
    },
    ("ks4/aqa-computer-science", "systems-architecture"): {
        "The von Neumann architecture": ["!illus cpu-board"],
        "CPU performance and embedded systems": ["!illus cpu-performance"],
    },
    ("ks4/edexcel-computer-science", "hardware-and-the-processor"): {
        "Inside the CPU": ["!illus cpu-board"],
        "What makes a processor faster": ["!illus cpu-performance"],
    },
    ("ks5", "structure-and-function-of-the-processor"): {
        "Components and registers": ["!illus cpu-board"],
    },
    ("ks4/aqa-computer-science", "computer-networks"): {
        "Star and bus topologies": ["!illus network-topologies"],
        "Networks": ["!illus lan-wan"],
    },
    ("ks4/edexcel-computer-science", "networks-and-network-security"): {
        "Networks and topologies": ["!illus network-topologies"],
        "Protocols and layers": ["!illus tcp-ip-stack"],
    },
    ("ks4/aqa-computer-science", "number-bases-and-units"): {
        "Converting between the bases": ["!illus binary-place-value"],
        "Units of information": ["!illus units-of-data"],
    },
    ("ks4/edexcel-computer-science", "binary-and-hexadecimal"): {
        "Converting between denary and binary": ["!illus binary-place-value"],
    },
    ("ks4/computer-science", "secondary-storage"): {
        "The three types": ["!illus secondary-storage"],
    },
    ("ks4/aqa-computer-science", "representing-images"): {
        "Bitmap images": ["!illus image-layers"],
    },
    ("ks4/aqa-computer-science", "representing-sound"): {
        "From analogue to digital": ["!illus sound-sampling"],
    },
    ("ks4/aqa-computer-science", "protocols-and-layers"): {
        "Layers": ["!illus tcp-ip-stack"],
    },
    ("ks4/edexcel-computer-science", "representing-text-images-and-sound"): {
        "Representing images": ["!illus image-layers"],
        "Representing sound": ["!illus sound-sampling"],
    },
    ("ks4/edexcel-computer-science", "data-storage-and-compression"): {
        "Secondary storage": ["!illus secondary-storage"],
        "Compression": ["!illus compression"],
        "Units of storage": ["!illus units-of-data"],
    },
    ("ks5", "networks-and-web-technologies"): {
        "Networks and protocols": ["!illus tcp-ip-stack"],
        "Web technologies": ["!illus web-request"],
    },
    ("ks5", "input-output-and-storage"): {
        "Storage": ["!illus secondary-storage"],
    },
}

for _key, _mapping in ILLUSTRATIONS.items():
    _target = PLACEMENTS.setdefault(_key, {})
    for _section, _items in _mapping.items():
        # Only illustrations belong here. Restating a diagram would add a second
        # copy of it to a page that already has one, which is how this table
        # went wrong the first time.
        assert all(i.startswith("!illus ") for i in _items), (_key, _section)
        _target.setdefault(_section, []).extend(_items)


# Photographs, merged in the same way and for the same reason as the illustrations.
# A topic that already has a diagram or an illustration above keeps it: the picture of
# the object and the picture of the mechanism do different jobs. Entries whose
# image file is not in the repository yet render as nothing, so this table can
# be written before the photographs are sourced.
PHOTO_PLACEMENTS = {
    ("ks3", "using-computers"): {
        "Hardware and software": ["!photo peripherals"],
    },
    ("ks3", "understanding-computers"): {
        "Inside the computer": ["!photo motherboard", "!photo cpu-chip"],
    },
    ("ks4/computer-science", "architecture-of-the-cpu"): {
        "What the CPU is for": ["!photo cpu-chip"],
    },
    ("ks4/computer-science", "cpu-performance"): {
        "The three factors": ["!photo heatsink-fan"],
    },
    ("ks4/computer-science", "primary-storage"): {
        "RAM": ["!photo ram-stick"],
        "ROM": ["!photo rom-chip"],
    },
    ("ks4/computer-science", "secondary-storage"): {
        "The three types": ["!photo hdd-open", "!photo ssd-open"],
        "Choosing the right device": ["!photo usb-and-disc"],
    },
    ("ks4/computer-science", "embedded-systems"): {
        "What an embedded system is": ["!photo embedded-board"],
    },
    ("ks4/computer-science", "networks-and-topologies"): {
        "Network hardware": ["!photo network-switch", "!photo home-router"],
        "Client server and peer to peer": ["!photo server-rack"],
    },
    ("ks4/computer-science", "protocols-and-layers"): {
        "Wired and wireless": ["!photo ethernet-cable", "!photo fibre-optic"],
        "IP addresses and MAC addresses": ["!photo nic-card"],
    },
    ("ks4/aqa-computer-science", "systems-architecture"): {
        "The von Neumann architecture": ["!photo cpu-chip"],
    },
    ("ks4/aqa-computer-science", "hardware-software-and-the-operating-system"): {
        "Hardware and software": ["!photo ram-stick"],
    },
    ("ks4/aqa-computer-science", "computer-networks"): {
        "Networks": ["!photo network-switch"],
        "Wired and wireless": ["!photo ethernet-cable"],
    },
    ("ks4/edexcel-computer-science", "hardware-and-the-processor"): {
        "Components of a computer system": ["!photo motherboard"],
        "Inside the CPU": ["!photo cpu-chip"],
    },
    ("ks4/edexcel-computer-science", "data-storage-and-compression"): {
        "Secondary storage": ["!photo hdd-open", "!photo ssd-open"],
    },
    ("ks5", "structure-and-function-of-the-processor"): {
        "Components and registers": ["!photo cpu-chip"],
    },
    ("ks5", "types-of-processor"): {
        "GPUs and parallel systems": ["!photo gpu-card"],
    },
    ("ks5", "input-output-and-storage"): {
        "Devices and how they work": ["!photo peripherals"],
        "Storage": ["!photo hdd-open", "!photo ssd-open"],
    },
}

for _key, _mapping in PHOTO_PLACEMENTS.items():
    _target = PLACEMENTS.setdefault(_key, {})
    for _section, _items in _mapping.items():
        assert all(i.startswith("!photo ") for i in _items), (_key, _section)
        _target.setdefault(_section, []).extend(_items)

# The concept illustrations shared across boards are written as calls in their
# own module, and folded in last so they land after what a section already has.
from . import placements_visuals as _visuals
_visuals.merge(PLACEMENTS)

def _duplicate_keys():
    """Find keys written twice in the literal above.

    A dict literal keeps the last of any repeated key and says nothing, so
    writing the same (course, topic) pair twice silently throws the earlier
    one away. That has now happened twice here, once losing a tool from a
    page for several deploys, so the source is parsed and checked rather than
    trusted. Nothing else can catch it: by the time the module has imported,
    the evidence is gone.
    """
    import ast
    with open(__file__, encoding="utf-8") as fh:
        tree = ast.parse(fh.read())
    seen, dupes = set(), []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Assign):
            continue
        name = next((getattr(t, "id", "") for t in node.targets), "")
        if name not in ("PLACEMENTS", "ILLUSTRATIONS", "PHOTO_PLACEMENTS"):
            continue
        for key in node.value.keys:
            try:
                k = ast.literal_eval(key)
            except ValueError:
                continue
            if (name, k) in seen:
                dupes.append("%s%r" % (name, (k,)))
            seen.add((name, k))
    return dupes


def check(all_used):
    """Every mapping must have matched a real topic, and be written once."""
    dupes = _duplicate_keys()
    if dupes:
        raise KeyError("placement keys written more than once, so the earlier "
                       "one is being discarded: %s" % sorted(dupes))
    missing = set(PLACEMENTS) - all_used
    if missing:
        raise KeyError("placements that matched no topic: %s" % sorted(missing))
