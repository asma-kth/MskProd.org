"""The interactive tools hub and one page per tool."""
from mskbuild import markup
from mskbuild.tools import TOOLS, ORDER
from mskbuild.render import (layout, crumbs, crumbs_ld, ico, esc, write)

INTRO = ("Reading about a truth table is not the same as building one. These tools let "
         "you do the thing itself, get it wrong, and see immediately why. Everything "
         "runs in your browser, nothing is sent anywhere, and none of it needs an "
         "account.")

# Extra teaching that sits above each tool on its own page.
NOTES = {
    "base-converter": """
Converting between denary, binary and hexadecimal comes up on every single GCSE and A Level paper, and it is the easiest set of marks on the whole specification once the method is automatic. The trick is that the method never changes, so what you are really practising is speed and accuracy.

!key The one method worth learning :: Go through binary. Denary to hex is denary to binary to hex. Hex to denary is hex to binary to denary. You only ever need two conversions, not six.

!tool base-converter

### How to use this properly

+ Start in convert mode and type numbers you already know, so you can see the working laid out
+ Move to practice mode and set yourself a target, for example twenty correct in a row
+ Say the place values out loud as you work: 128, 64, 32, 16, 8, 4, 2, 1
+ Check every answer by converting it back the other way

!exam Show the working :: In an exam a wrong final answer with correct place values written above the columns often still earns a method mark. A bare wrong number earns nothing.
""",
    "file-size": """
File size questions are worth between two and five marks and are lost far more often to a missed conversion than to a missed formula. This calculator shows every division separately, so you can see exactly where an answer usually goes wrong.

!tool file-size

### The three formulas

| What | Formula | Watch out for |
| Image | width x height x colour depth | The answer is in **bits**, and metadata is extra |
| Sound | sample rate x bit depth x seconds x channels | Stereo doubles it, and minutes must become seconds |
| Text | number of characters x bits per character | Spaces and punctuation are characters too |

!warn Bits and bytes :: A lower case b means bits and an upper case B means bytes. Every one of these formulas gives you bits, so dividing by eight is always the first conversion.
""",
    "logic-simulator": """
A logic circuit is easier to understand when you can flip an input and watch the answer change. Build the circuit from the question, switch the inputs through every combination, and the truth table fills itself in.

!tool logic-simulator

### Try these

1. Build **Q = A AND B**, then change the AND to a NAND and watch every output flip
2. Build **Q = (A AND B) OR C** using three inputs
3. Build **Q = NOT (A OR B)** with an OR and a NOT, then check it matches a single NOR gate
4. Build an XOR from AND, OR and NOT gates only, and prove the truth tables match

!grade Prove it, do not assert it :: An A star answer to "show that these two circuits are equivalent" is a full truth table for each, side by side, with a sentence saying the output columns are identical.
""",
    "sort-visualiser": """
Everybody can recite that bubble sort is slow and merge sort is fast. Far fewer students can say what the algorithms are actually doing differently, which is the part worth marks. Watch all four run on the same list and the difference stops being an abstract claim.

!tool sort-visualiser

### What to look for

+ Bubble sort compares the same neighbours over and over, and the largest value walks to the end on every pass
+ Insertion sort grows a sorted section on the left and pushes each new value back into place
+ Merge sort barely compares at all until it starts merging, and the number of comparisons hardly changes when you shuffle the list
+ Quick sort is usually the fastest here, but its comparison count swings the most between shuffles, which is exactly why its worst case is so much worse than its average case

!exam Best, average and worst :: Bubble and insertion sort are n squared in the worst case. Merge sort is n log n in every case. Quick sort is n log n on average but n squared in the worst case. Learn those six facts and most sorting questions answer themselves.
""",
    "trace-table": """
Trace tables are pure method. There is nothing to understand once you know the rule, which is: work down the algorithm one line at a time and write a value the moment it changes, never later. Students lose marks by tracing in their head and only writing down the answer.

!tool trace-table

!warn The most common mistake :: Updating two variables in the same row when the algorithm changes them on different lines. If line 4 changes total and line 5 changes count, they belong in different steps of your working even if the exam table gives you one row per loop.
""",
    "lmc": """
The Little Man Computer is a complete processor with one accumulator, one hundred mailboxes and eleven instructions. It is small enough to hold in your head and real enough that every idea in it transfers straight to a real CPU: the program counter, the accumulator, the fetch decode execute cycle and the difference between an instruction and the data it operates on.

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


def _page(path, title, description, trail, body_md, greeting=""):
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
                        active="/tools/", greeting=greeting,
                        jsonld=[crumbs_ld(trail)])


def build(register, add_search):
    # ------------------------------------------------------------ the hub
    cards = []
    for name in ORDER:
        meta = TOOLS[name]
        cards.append(
            '<a class="tile" href="/tools/%s/">'
            '<span class="tile-icon">%s</span><h3>%s</h3><p>%s</p></a>'
            % (name, ico(meta["icon"], "icon"), esc(meta["title"]), esc(meta["blurb"])))
    trail = [("Home", "/"), ("Tools", None)]
    body = """<div class="wrap">
  %s
  <header class="section-head"><h1>Interactive tools</h1><p class="lead">%s</p></header>
  <div class="grid grid-3">%s</div>
</div>""" % (crumbs(trail), esc(INTRO), "".join(cards))
    path = "/tools/"
    write(path, layout(title="Interactive Computing Tools",
                       description=INTRO, path=path, body=body, active="/tools/",
                       greeting="Pick one and break it. You learn far more from a circuit "
                                "that gives the wrong answer than from one that works "
                                "first time.",
                       jsonld=[crumbs_ld(trail)]))
    register(path, 0.8, "monthly")
    add_search("Interactive tools", path, "Six tools you can actually use",
               "tools converter binary hex logic gates simulator sorting trace table "
               "little man computer file size calculator interactive")

    # ------------------------------------------------------ one per tool
    for name in ORDER:
        meta = TOOLS[name]
        tpath = "/tools/%s/" % name
        ttrail = [("Home", "/"), ("Tools", "/tools/"), (meta["title"], None)]
        md = NOTES.get(name) or ("%s\n\n!tool %s\n" % (meta["long"], name))
        _p, html = _page(tpath, meta["title"], meta["long"], ttrail, md)
        write(tpath, html)
        register(tpath, 0.75, "monthly")
        add_search(meta["title"], tpath, "Interactive tool",
                   (meta["title"] + " " + meta["blurb"] + " " + meta["long"]).lower())
