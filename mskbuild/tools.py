"""Registry of the interactive tools embedded in topic pages.

A tool is two files, both optional to the build only in the sense that a missing
one is an error:

    static/js/tools/<name>.js     an IIFE that self initialises
    static/css/tools/<name>.css   styles, all selectors under .tool[data-tool=...]

Shared chrome (.tool, .tool-btn, .tool-field and the rest) lives in
static/css/tools/_common.css, which is bundled ahead of the per tool files.

Every tool is mounted by the `!tool <name>` markup directive, which writes

    <div class="tool" data-tool="<name>">
      <div class="tool-head">...</div>
      <div class="tool-body"><p class="tool-fallback">...</p></div>
    </div>

The script finds its own mounts with document.querySelectorAll and replaces the
contents of .tool-body. Because the fallback paragraph is rendered server side,
a reader without JavaScript sees an explanation rather than an empty box.

All tool files are concatenated into one bundle at build time, and `layout()`
only links that bundle on pages that actually mount a tool.
"""
import os

TOOLS = {
    "base-converter": {
        "title": "Number base converter",
        "icon": "i-binary",
        "blurb": "Convert between denary, binary and hexadecimal, with every step of "
                 "the working written out.",
        "long": "Type a number in any base and watch the other two update. Switch to "
                "practice mode for endless auto marked conversion questions with the "
                "method shown after each answer.",
    },
    "file-size": {
        "title": "File size calculator",
        "icon": "i-disk",
        "blurb": "Work out the size of an image, a sound file or a block of text, one "
                 "conversion at a time.",
        "long": "Choose image, sound or text, set the properties, and the calculator "
                "shows the formula, the substitution and every division from bits to "
                "bytes to kilobytes to megabytes.",
    },
    "logic-simulator": {
        "title": "Logic gate simulator",
        "icon": "i-gate",
        "blurb": "Build a circuit from gates, wire it up, and see the truth table fill "
                 "in as you go.",
        "long": "Place AND, OR, NOT, XOR, NAND and NOR gates on the canvas, drag from an "
                "output to an input to wire them, flip the inputs, and read the full "
                "truth table and Boolean expression the circuit produces.",
    },
    "sort-visualiser": {
        "title": "Sorting algorithm visualiser",
        "icon": "i-shuffle",
        "blurb": "Run bubble, insertion, merge and quick sort side by side and count "
                 "the comparisons.",
        "long": "Watch four sorting algorithms work on the same list at the same time, "
                "with a live count of comparisons and swaps, so the difference between "
                "them stops being an abstract claim.",
    },
    "trace-table": {
        "title": "Trace table trainer",
        "icon": "i-table",
        "blurb": "Fill in a trace table row by row and have it marked as you type.",
        "long": "Read the algorithm, fill in what each variable holds after each line, "
                "and every cell is checked the moment you leave it. Step through the "
                "answer afterwards to see exactly where a value changed.",
    },
    "confusion-matrix": {
        "title": "Classifier scorer",
        "icon": "i-table",
        "blurb": "Move the threshold and watch precision and recall trade against "
                 "each other.",
        "long": "Pick a scenario, drag the threshold across two overlapping score "
                "distributions, and the confusion matrix, accuracy, precision, "
                "recall and F1 all update as cases move from one cell to another. "
                "The point it makes is the one the exam asks: on an imbalanced "
                "problem, accuracy measures the imbalance.",
    },
    "correlation-lab": {
        "title": "Correlation lab",
        "icon": "i-chart",
        "blurb": "Add and drag points on a scatter plot and watch the coefficient "
                 "respond.",
        "long": "Load a preset or build your own cloud of points, then drag one a "
                "long way from the rest. The correlation coefficient, the strength "
                "description and the line of best fit recalculate live, which is "
                "the quickest way to see how much damage a single outlier does.",
    },
    "what-if-model": {
        "title": "What-if model",
        "icon": "i-chart",
        "blurb": "Change the inputs of a spreadsheet model and watch every output, "
                 "the break-even prices and the graph recalculate.",
        "long": "A ticket price model with its assumptions laid out like an input "
                "sheet. Move the price or any assumption, switch between "
                "pessimistic, expected and optimistic scenarios, run Goal Seek "
                "for a target profit, and open the data table or the formulas "
                "behind every output. It is the spreadsheet modelling unit's "
                "what-if analysis, made something you can push around.",
    },
    "kmeans-lab": {
        "title": "k-means clustering lab",
        "icon": "i-target",
        "blurb": "Drop centroids onto a scatter of points and run k-means one "
                 "assign and update at a time.",
        "long": "Choose a dataset and a number of clusters, place the centroids, "
                "then press Assign to colour every point by its nearest centroid "
                "and Update to move each centroid to the middle of its points. "
                "Shuffle the start to see different results, try the datasets "
                "k-means gets wrong, and draw an elbow chart to choose k.",
    },
    "loss-landscape": {
        "title": "Loss landscape lab",
        "icon": "i-route",
        "blurb": "Roll balls down a rotating 3D loss surface with gradient "
                 "descent, momentum or Adam.",
        "long": "Pick a landscape, a bowl, a ravine, two valleys, a saddle or a "
                "bumpy field, click the contour map to drop balls, then choose "
                "an optimiser and a learning rate and watch every ball descend "
                "in 3D and on the map at once. Drag the surface to turn it.",
    },
    "neuron-lab": {
        "title": "Neuron lab",
        "icon": "i-gate",
        "blurb": "Turn one neuron's weights and bias and watch its decision "
                 "boundary turn and slide; then let the perceptron rule learn.",
        "long": "One artificial neuron with two inputs. Drag w1, w2 and b to move "
                "its decision boundary across the plane, switch between step and "
                "sigmoid activations, and train it with Rosenblatt's perceptron rule "
                "on AND, OR, NAND, two clouds of points, or XOR, which it can never "
                "learn.",
    },
    "network-playground": {
        "title": "Neural network playground",
        "icon": "i-layers",
        "blurb": "Train a small neural network in your browser and watch its "
                 "decision boundary form, weight by weight.",
        "long": "Choose a dataset, from two clouds to two interlocking spirals, "
                "set the number of hidden layers, neurons and the activation, and "
                "press Train. Every frame runs real forward passes, cross-entropy "
                "loss, backpropagation and a gradient step, and the shading shows "
                "the network's output across the whole plane.",
    },
    "convolution-lab": {
        "title": "Convolution lab",
        "icon": "i-image",
        "blurb": "Draw a picture, choose or design a 3 × 3 kernel, and see the "
                 "feature map it produces.",
        "long": "Paint pixels on a 12 × 12 grid or load a picture, then pick an "
                "edge, blur or sharpen kernel or type your own weights. The "
                "feature map updates as you draw, padding and stride change its "
                "size, and hovering over any cell writes out the sum that made it.",
    },
    "embedding-space": {
        "title": "Embedding space lab",
        "icon": "i-language",
        "blurb": "Spin a 3D space of word vectors, find each word's nearest "
                 "neighbours and test analogies like king − man + woman.",
        "long": "Thirty-four words placed as points in three dimensions. Pick a "
                "word and its nearest neighbours by cosine similarity light up; "
                "choose three words and the lab computes a − b + c, draws the "
                "parallelogram and names the word it lands on. Drag the space to "
                "turn it and see that the pattern holds from every angle.",
    },
    "lmc": {
        "title": "Little Man Computer",
        "icon": "i-cpu",
        "blurb": "Assemble and run LMC programs and watch the fetch decode execute cycle "
                 "happen.",
        "long": "Write LMC assembly, assemble it into the mailboxes, then run it or step "
                "one instruction at a time while the program counter, accumulator and "
                "each mailbox update in front of you.",
    },
}

# The order tools appear in on the /tools/ hub page.
ORDER = ["base-converter", "file-size", "logic-simulator", "sort-visualiser",
         "trace-table", "lmc", "confusion-matrix", "correlation-lab",
         "what-if-model"]

# The AI course's labs. They get their own section on the /tools/ hub page,
# and are bundled with the rest.
AI_ORDER = ["kmeans-lab", "loss-landscape", "neuron-lab", "network-playground",
            "convolution-lab", "embedding-space"]


def _read(path):
    with open(path, encoding="utf-8") as fh:
        return fh.read()


def bundle(root, kind):
    """Concatenate every tool's js or css into one file's worth of text."""
    ext = "js" if kind == "js" else "css"
    base = os.path.join(root, "static", ext, "tools")
    parts = ["/* MskProd interactive tools bundle. Generated by build.py. */"]
    # The shared chrome every tool's markup assumes. It has to come first so a
    # tool's own file can override it.
    names = (["_common"] if ext == "css" else []) + ORDER + AI_ORDER
    for name in names:
        p = os.path.join(base, name + "." + ext)
        if not os.path.exists(p):
            raise FileNotFoundError("missing tool asset: %s" % p)
        parts.append("/* ---- %s ---- */" % name)
        parts.append(_read(p).strip())
    return "\n".join(parts) + "\n"
