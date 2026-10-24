"""The interactive tools hub and one page per tool."""
from mskbuild import markup
from mskbuild.tools import TOOLS, ORDER, AI_ORDER
from mskbuild.render import (layout, crumbs, crumbs_ld, ico, esc, write)

INTRO = ("Tools that let you do the thing itself, get it wrong, and see immediately why. "
         "Everything runs in your browser, and none of it needs an account.")

# Extra teaching that sits above each tool on its own page.
NOTES = {
    "base-converter": """
!tool base-converter

!key The one method worth learning :: Go through binary: denary to hex is denary to binary to hex, and hex to denary is hex to binary to denary. You only ever need two conversions, not six.

!exam Show the working :: In an exam a wrong final answer with correct place values written above the columns often still earns a method mark. A bare wrong number earns nothing.
""",
    "file-size": """
!tool file-size

### The three formulas

| What | Formula | Watch out for |
| Image | width x height x colour depth | The answer is in **bits**, and metadata is extra |
| Sound | sample rate x bit depth x seconds x channels | Stereo doubles it, and minutes must become seconds |
| Text | number of characters x bits per character | Spaces and punctuation are characters too |

!warn Bits and bytes :: A lower case b means bits and an upper case B means bytes. Every one of these formulas gives you bits, so dividing by eight is always the first conversion.
""",
    "logic-simulator": """
!tool logic-simulator

### Try these

1. Build **Q = A AND B**, then change the AND to a NAND and watch every output flip
2. Build **Q = (A AND B) OR C** using three inputs
3. Build **Q = NOT (A OR B)** with an OR and a NOT, then check it matches a single NOR gate
4. Build an XOR from AND, OR and NOT gates only, and prove the truth tables match

!grade Prove it, do not assert it :: An A star answer to "show that these two circuits are equivalent" is a full truth table for each, side by side, with a sentence saying the output columns are identical.
""",
    "sort-visualiser": """
!tool sort-visualiser

### What to look for

+ Bubble sort compares the same neighbours over and over, and the largest value walks to the end on every pass
+ Insertion sort grows a sorted section on the left and pushes each new value back into place
+ Merge sort barely compares at all until it starts merging, and the number of comparisons hardly changes when you shuffle the list
+ Quick sort is usually the fastest here, but its comparison count swings the most between shuffles, which is exactly why its worst case is so much worse than its average case

!exam Best, average and worst :: Bubble and insertion sort are n squared in the worst case. Merge sort is n log n in every case. Quick sort is n log n on average but n squared in the worst case.
""",
    "trace-table": """
!tool trace-table

!warn The most common mistake :: Updating two variables in the same row when the algorithm changes them on different lines. If line 4 changes total and line 5 changes count, they belong in different steps of your working even if the exam table gives you one row per loop.
""",
    "lmc": """
!tool lmc

### The instruction set

| Code | Mnemonic | What it does |
| 1xx | ADD | Add the contents of mailbox xx to the accumulator |
| 2xx | SUB | Subtract the contents of mailbox xx from the accumulator |
| 3xx | STA | Store the accumulator into mailbox xx |
| 5xx | LDA | Load mailbox xx into the accumulator |
| 6xx | BRA | Branch to mailbox xx, always |
| 7xx | BRZ | Branch to mailbox xx if the accumulator is zero |
| 8xx | BRP | Branch to mailbox xx if the accumulator is zero or positive |
| 901 | INP | Take the next number from the input queue into the accumulator |
| 902 | OUT | Copy the accumulator to the output |
| 000 | HLT | Stop |
| | DAT | Not an instruction. Reserves a mailbox, optionally with a starting value |

!key Instructions and data share the same memory :: The mailboxes hold both. That is the von Neumann idea, and it is why a program can accidentally treat its own instructions as data if a branch goes to the wrong place. Step through a program and watch the program counter to see it happen.

!fact One accumulator :: The LMC has exactly one general purpose register. Everything has to pass through it, which is why so many LMC programs are a run of load, do something, store. Real processors have dozens of registers precisely to avoid that traffic.
""",
}


def _page(path, title, description, trail, body_md):
    body = """<div class="wrap">
  %s
  <div class="wrap-narrow" style="width:100%%;margin-inline:auto">
    <article class="prose" style="padding-bottom:var(--sp-8)">
      <header class="topic-header"><h1>%s</h1><p class="lead">%s</p></header>
      %s
    </article>
  </div>
</div>""" % (crumbs(trail), esc(title), esc(description), markup.render(body_md))
    return path, layout(title=title, description=description, path=path, body=body,
                        active="/tools/",
                        jsonld=[crumbs_ld(trail)])


def build(register, add_search):
    # ------------------------------------------------------------ the hub
    def tiles(names):
        return "".join(
            '<a class="tile" href="/tools/%s/">'
            '<span class="tile-icon">%s</span><h3>%s</h3><p>%s</p></a>'
            % (name, ico(TOOLS[name]["icon"], "icon"), esc(TOOLS[name]["title"]),
               esc(TOOLS[name]["blurb"])) for name in names)
    cards = [tiles(ORDER)]
    trail = [("Home", "/"), ("Tools", None)]
    body = """<div class="wrap">
  %s
  <header class="section-head"><h1>Interactive tools</h1><p class="lead">%s</p></header>
  <div class="grid grid-3">%s</div>
  <header class="section-head" style="margin-top:var(--sp-7)"><h2>AI labs</h2>
    <p class="lead">From the <a href="/ai/">Artificial Intelligence course</a>: watch models learn, in colour and in 3D.</p></header>
  <div class="grid grid-3">%s</div>
  <header class="section-head" style="margin-top:var(--sp-7)"><h2>Games</h2>
    <p class="lead">Practice that does not feel like practice.</p></header>
  <div class="grid" style="grid-template-columns:repeat(auto-fill,minmax(min(265px,100%%),1fr))">
    <a class="tile" href="/computational-thinking/"><span class="tile-icon">%s</span><h3>Computational Thinking Adventure</h3>
      <p>Forty levels across four worlds: decomposition, abstraction, pattern recognition and algorithms.</p></a>
    <a class="tile" href="/computational-thinking/#/lab/pseudocode"><span class="tile-icon">%s</span><h3>Pseudocode Playground</h3>
      <p>Write OCR-style pseudocode, run it, step through it and watch a trace table build itself.</p></a>
    <a class="tile" href="/computational-thinking/#/lab/flowchart"><span class="tile-icon">%s</span><h3>Flowchart Lab</h3>
      <p>Build a flowchart from blocks, see it drawn with the standard symbols, then run it step by step.</p></a>
    <a class="tile" href="/pixel-run/"><span class="tile-icon">%s</span><h3>Pixel Run</h3>
      <p>A platformer where every obstacle is a Python function to write. Ten levels, from print to Dijkstra's algorithm.</p></a>
  </div>
</div>""" % (crumbs(trail), esc(INTRO), "".join(cards), tiles(AI_ORDER), ico("i-map", "icon"), ico("i-code", "icon"), ico("i-flow", "icon"), ico("i-flag", "icon"))
    path = "/tools/"
    write(path, layout(title="Interactive Computing Tools",
                       description=INTRO, path=path, body=body, active="/tools/",
                       jsonld=[crumbs_ld(trail)]))
    register(path, 0.8, "monthly")
    add_search("Interactive tools", path, "%d tools and AI labs you can actually use"
               % (len(ORDER) + len(AI_ORDER)),
               "tools converter binary hex logic gates simulator sorting trace table "
               "little man computer file size calculator interactive ai labs neural "
               "network k-means gradient descent attention embeddings")

    # ------------------------------------------------------ one per tool
    for name in ORDER + AI_ORDER:
        meta = TOOLS[name]
        tpath = "/tools/%s/" % name
        ttrail = [("Home", "/"), ("Tools", "/tools/"), (meta["title"], None)]
        md = NOTES.get(name) or ("!tool %s\n" % name)
        _p, html = _page(tpath, meta["title"], meta["long"], ttrail, md)
        write(tpath, html)
        register(tpath, 0.75, "monthly")
        add_search(meta["title"], tpath, "Interactive tool",
                   (meta["title"] + " " + meta["blurb"] + " " + meta["long"]).lower())
