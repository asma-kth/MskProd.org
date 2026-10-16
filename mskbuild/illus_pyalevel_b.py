"""Illustrations for the A Level Python topics, set two: the Turing machine, the halting problem, the
fetch-decode-execute cycle, race conditions, deadlock, public key cryptography, subnet masks and
reliable delivery."""
from .illus import Canvas, PAL, INK, ARROW, figure, illustration, _n
from . import illus_props as P
from . import illus_glyphs as G


def chip(cv, x, y, w, h, text, fill="#FFFFFF", tc=INK, size=14, stroke="#9FB3BE", mono=True, weight=800, r=None):
    return cv.rect(x, y, w, h, r if r is not None else min(9, h / 2.4), fill, stroke=stroke, sw=1.5) + cv.text(x + w / 2, y + h / 2 + size * .36, text, size, weight, fill=tc, mono=mono)


def reg(cv, x, y, w, h, name, value, color="sky", hot=False):
    """A register: a lifted box with its name on the left and its contents on the right."""
    out = P.lift(cv, x, y, w, h, color, 10, 4, hl=False)
    if hot:
        out += cv.rect(x - 3, y - 3, w + 6, h + 6, 12, "none", stroke="#C84B43", sw=2.8)
    out += cv.text(x + 14, y + h / 2 + 6, name, 17, 800, anchor="start", fill=INK, mono=True)
    out += cv.text(x + w - 14, y + h / 2 + 6, value, 17, 800, anchor="end", fill=INK, mono=True)
    return out


# ------------------------------------------------------------------ the Turing machine

@illustration("turing-tape")
def _turing():
    cv = Canvas(800, 500).backdrop()
    cv.add(P.card(cv, 14, 24, 772, 214, 20, "the tape, the head and the state", "teal"))
    symbols = ["_", "1", "0", "1", "1", "_", "_", "_"]
    cx0, cw = 50, 84
    head = 2
    for i, sym in enumerate(symbols):
        x = cx0 + i * cw
        hot = i == head
        cv.add(P.lift(cv, x, 130, cw - 8, 62, "sun" if hot else ("paper" if sym == "_" else "sky"), 8, 4, hl=False))
        cv.add(cv.text(x + (cw - 8) / 2, 170, "blank" if sym == "_" else sym, 13 if sym == "_" else 28, 800, fill=INK if sym != "_" else "#4A6470", mono=True))
    cv.add(cv.text(20, 226, "the tape goes on in both directions, so it never runs out", 13, 650, anchor="start", cls="il-ink2"))
    hx = cx0 + head * cw + (cw - 8) / 2
    cv.add(cv.poly([(hx - 20, 94), (hx + 20, 94), (hx, 126)], cv.g("coral"), stroke=PAL["coral"][2], sw=2))
    cv.add(P.pill(cv, hx, 76, "head", "coral", 15, 14, 26, 800))
    cv.add(P.pill(cv, hx + 150, 76, "state: start", "mint", 15, 14, 26, 800))
    cv.add(P.badge(cv, 40, 68, 1))
    # rules
    cv.add(P.card(cv, 14, 262, 470, 224, 20, "the rules are the program", "sun"))
    cv.add(cv.text(40, 322, "state", 13, 750, anchor="start", cls="il-ink2"), cv.text(130, 322, "reads", 13, 750, anchor="start", cls="il-ink2"),
           cv.text(226, 322, "writes", 13, 750, anchor="start", cls="il-ink2"), cv.text(310, 322, "moves", 13, 750, anchor="start", cls="il-ink2"),
           cv.text(392, 322, "next", 13, 750, anchor="start", cls="il-ink2"))
    rules = [("start", "0", "1", "right", "start"), ("start", "1", "0", "right", "start"), ("start", "blank", "blank", "stay", "halt")]
    for i, r_ in enumerate(rules):
        y = 328 + i * 44
        cv.add(P.lift(cv, 28, y, 440, 34, "sun" if i == 0 else "paper", 9, 3, hl=False))
        for text, x in zip(r_, (40, 130, 226, 310, 392)):
            cv.add(cv.text(x, y + 23, text, 15, 800, anchor="start", fill=INK, mono=True))
    cv.add(P.badge(cv, 436, 296, 2))
    # one step
    cv.add(P.card(cv, 500, 262, 286, 224, 20, "one step of the machine", "coral"))
    steps = [("read", "the head is on a 0"), ("write", "it writes a 1"), ("move", "one cell to the right"), ("change state", "stays in start")]
    for i, (a, b) in enumerate(steps):
        y = 296 + i * 44
        cv.add(P.pill(cv, 580, y + 14, a, "sky", 14, 10, 26, 800), cv.text(648, y + 20, b, 13.5, 650, anchor="start", cls="il-ink"))
    cv.add(P.badge(cv, 526, 300, 3))
    return figure(
        "turing-tape", cv, "A Turing machine: a tape, a head, a state and a table of rules",
        "A Turing machine has a tape of cells, endless in both directions, holding the symbols 1, 0, 1, 1 with blanks on either side. A head sits "
        "over one cell, here the 0, and the machine is in the state called start. The rules are a table: in the state start, reading 0 writes 1, "
        "moves right and stays in start. Reading 1 writes 0, moves right and stays in start. Reading a blank writes a blank, stays put and halts. "
        "One step has four parts: read the symbol under the head, write a symbol, move one cell left or right, and change state. The machine "
        "inverts every bit of the number.",
        ["The tape holds the data, the head reads and writes one cell at a time, and the machine is always in exactly one state.",
         "The rules are the program: for each state and symbol read, they say what to write, which way to move and which state comes next.",
         "A step is always read, write, move, change state. The machine stops when it enters a halting state."],
        "Everything a computer does can, in principle, be done by this machine. It is a model for reasoning, not a design to build.")


# ------------------------------------------------------------------ the halting problem

@illustration("halting-paradox")
def _halting():
    cv = Canvas(800, 470).backdrop()
    # suppose a checker exists
    cv.add(P.card(cv, 14, 24, 250, 340, 20, "suppose it exists", "teal"))
    cv.add(chip(cv, 40, 96, 198, 40, "a program p", "#FFFFFF", INK, 16))
    cv.add(P.arrow(cv, [(139, 140), (139, 176)], ARROW, 3.4, 11))
    cv.add(P.lift(cv, 40, 180, 198, 64, "sky", 12, 5, hl=False), cv.text(139, 220, "halts(p)", 22, 800, fill=INK, mono=True))
    cv.add(P.arrow(cv, [(100, 258), (100, 286)], ARROW, 3, 10), P.arrow(cv, [(178, 258), (178, 286)], ARROW, 3, 10))
    cv.add(P.pill(cv, 100, 306, "YES", "mint", 17, 14, 30, 800), P.pill(cv, 178, 306, "NO", "coral", 17, 14, 30, 800))
    cv.add(cv.text(139, 346, "it halts   |   it runs forever", 12, 650, cls="il-ink2"))
    cv.add(P.badge(cv, 40, 66, 1))
    # build paradox
    cv.add(P.card(cv, 276, 24, 250, 340, 20, "build paradox", "plum"))
    cv.add(G.code(cv, 292, 92, 218, ["def paradox():", "    if halts(paradox):", "        while True:", "            pass", "    # otherwise stop"], title=None, size=12.5, numbers=False, h=140))
    for i, t in enumerate(("it does the opposite of", "whatever the checker says", "about paradox itself")):
        cv.add(cv.text(401, 268 + i * 22, t, 13.5, 700, cls="il-ink"))
    cv.add(P.badge(cv, 302, 66, 2))
    # contradiction
    cv.add(P.card(cv, 538, 24, 248, 340, 20, "does paradox halt?", "coral"))
    cv.add(P.badge(cv, 564, 66, 3))
    for k, (says, does, col) in enumerate((("checker says YES", "so paradox loops forever", "coral"), ("checker says NO", "so paradox stops at once", "coral"))):
        y = 94 + k * 128
        cv.add(P.lift(cv, 556, y, 212, 38, "mint" if k == 0 else "coral", 10, 4, hl=False), cv.text(662, y + 25, says, 15, 800, fill=INK))
        cv.add(P.arrow(cv, [(662, y + 46), (662, y + 66)], ARROW, 3, 9))
        cv.add(P.lift(cv, 556, y + 70, 212, 34, "paper", 10, 4, hl=False), cv.text(662, y + 92, does, 13.5, 750, fill=INK))
    cv.add(P.cross(cv, 750, 140, 13), P.cross(cv, 750, 268, 13))
    cv.add(P.pill(cv, 400, 410, "the checker is wrong either way, so it cannot exist", "plum", 19, 22, 40, 800))
    return figure(
        "halting-paradox", cv, "The proof that no program can solve the halting problem",
        "A proof by contradiction. First, suppose someone had written halts of p, a function that is given any program p and always answers YES if "
        "p halts and NO if it runs forever. Second, use it to build a troublemaker called paradox, which asks the checker about itself and does the "
        "opposite: if halts of paradox says yes, it loops forever, otherwise it stops at once. Third, ask whether paradox halts. If the checker "
        "says yes, then paradox loops forever, so the checker was wrong. If the checker says no, then paradox stops at once, so the checker was "
        "wrong again. The checker is wrong whichever answer it gives, so no such checker can exist.",
        ["Suppose a perfect checker halts(p) existed: it answers YES if p halts and NO if p runs forever.",
         "Build paradox, which asks the checker about itself and then does the opposite of the answer.",
         "Either answer makes the checker wrong, which is a contradiction, so the checker cannot exist."],
        "This is Turing's 1936 argument. It shows that some well defined questions about programs cannot be answered by any program.")


# ------------------------------------------------------------------ fetch, decode, execute

@illustration("fde-registers")
def _fde():
    cv = Canvas(800, 520).backdrop()
    cv.add(P.card(cv, 14, 24, 500, 470, 20, "the processor", "teal"))
    cv.add(P.card(cv, 546, 24, 240, 470, 20, "main memory", "sun"))
    # registers
    cv.add(reg(cv, 44, 96, 190, 46, "PC", "0", "mint", True))
    cv.add(reg(cv, 44, 184, 190, 46, "MAR", "0", "sky", True))
    cv.add(reg(cv, 44, 272, 190, 46, "MDR", "505", "sky", True))
    cv.add(reg(cv, 44, 360, 190, 46, "CIR", "505", "sky", True))
    cv.add(P.arrow(cv, [(139, 150), (139, 178)], "#C84B43", 3.4, 10))
    cv.add(P.badge(cv, 70, 164, 1))
    cv.add(P.arrow(cv, [(139, 326), (139, 354)], "#C84B43", 3.4, 10))
    cv.add(P.badge(cv, 70, 340, 4))
    # the PC increment
    cv.add(cv.path("M236 112 C268 100 268 130 238 128", stroke="#C84B43", sw=3.2), cv.poly([(236, 123), (248, 132), (232, 135)], "#C84B43"))
    cv.add(cv.text(268, 126, "+ 1", 15, 800, anchor="start", cls="il-bad", mono=True))
    cv.add(P.badge(cv, 280, 162, 3))
    # the ALU and accumulator above the buses, the control unit below them
    cv.add(P.lift(cv, 336, 74, 154, 48, "coral", 12, 5, hl=False), cv.text(413, 97, "ALU", 17, 800, fill=INK), cv.text(413, 115, "adds, compares", 12, 650, fill=INK))
    cv.add(reg(cv, 336, 128, 154, 38, "ACC", "0", "sun"))
    cv.add(P.lift(cv, 310, 336, 180, 70, "plum", 12, 5, hl=False), cv.text(400, 366, "control unit", 17, 800, fill="#FFFFFF"), cv.text(400, 390, "decodes the CIR", 13, 650, fill="#FFFFFF"))
    cv.add(P.arrow(cv, [(240, 383), (304, 372)], ARROW, 2.8, 10))
    cv.add(cv.text(272, 424, "decode, then execute", 13, 700, cls="il-ink2"))
    # the buses run straight from MAR and to MDR
    cv.add(P.arrow(cv, [(240, 207), (574, 207)], "#2F82C0", 5, 14))
    cv.add(cv.text(400, 196, "address bus", 13, 800, cls="il-ink"))
    cv.add(P.arrow(cv, [(574, 296), (240, 296)], "#2F9F77", 5, 14))
    cv.add(cv.text(400, 286, "data bus", 13, 800, cls="il-ink"))
    # memory
    cells = [("0", "505", "LDA 5"), ("1", "106", "ADD 6"), ("2", "307", "STA 7"), ("3", "000", "HLT"), ("5", "042", "data")]
    for i, (a, v, m) in enumerate(cells):
        y = 96 + i * 62
        hot = i == 0
        cv.add(P.lift(cv, 568, y, 196, 50, "coral" if hot else "paper", 10, 4, hl=False))
        cv.add(cv.text(584, y + 31, a, 17, 800, anchor="start", fill=INK, mono=True), cv.text(646, y + 31, v, 17, 800, fill=INK, mono=True), cv.text(752, y + 31, m, 13, 650, anchor="end", fill=INK, mono=True))
    cv.add(cv.text(666, 450, "address, contents, meaning", 12.5, 650, cls="il-ink2"))
    cv.add(P.badge(cv, 592, 66, 2))
    return figure(
        "fde-registers", cv, "The fetch stage in the processor: PC, MAR, MDR and CIR, with the buses to memory",
        "A processor and main memory. The processor holds four registers and some units. The program counter, PC, holds 0, the address of the next "
        "instruction. Step 1: the address in the PC is copied to the memory address register, MAR. The address travels along the address bus to "
        "memory, and step 2: the contents of address 0, the number 505, which means load the number in mailbox 5, comes back along the data bus to "
        "the memory data register, MDR. Step 3: the PC is increased by 1 so that it points to the next instruction. Step 4: the instruction is "
        "copied from the MDR to the current instruction register, CIR. The control unit then decodes the instruction in the CIR, and it is "
        "executed, using the ALU and the accumulator, ACC.",
        ["PC to MAR: the address of the next instruction is copied into the memory address register.",
         "Memory at that address is read along the data bus into the MDR.",
         "The PC is incremented so that it already points to the next instruction.",
         "MDR to CIR: the instruction is copied into the current instruction register, ready to be decoded and executed."],
        "Fetch is the same for every instruction. What differs is what the control unit does after it has decoded the CIR.")


# ------------------------------------------------------------------ race condition

@illustration("race-lost-update")
def _race():
    cv = Canvas(800, 600).backdrop()
    for k, (title, color, rows, final, ok) in enumerate((
        ("no lock: the two tasks overlap", "coral",
         [("A", "reads", "100", 0), ("B", "reads", "100", 0), ("A", "writes 150", "150", 1), ("B", "writes 125", "125", 1)], "125", False),
        ("with a lock: B waits until A has finished", "mint",
         [("A", "reads", "100", 0), ("A", "writes 150", "150", 1), ("B", "reads", "150", 0), ("B", "writes 175", "175", 1)], "175", True))):
        y0 = 24 + k * 290
        cv.add(P.card(cv, 14, y0, 772, 270, 20, title, color))
        cv.add(P.badge(cv, 42, y0 + 42, k + 1))
        # lanes
        cv.add(cv.text(160, y0 + 70, "task A", 16, 800, cls="il-ink", mono=True), cv.text(360, y0 + 70, "task B", 16, 800, cls="il-ink", mono=True), cv.text(640, y0 + 70, "balance", 16, 800, cls="il-ink", mono=True))
        for x in (160, 360, 640):
            cv.add(cv.line(x, y0 + 82, x, y0 + 250, "#9FB3BE", 2, dash="4 5"))
        for i, (who, what, val, writes) in enumerate(rows):
            y = y0 + 106 + i * 40
            x = 160 if who == "A" else 360
            cv.add(P.lift(cv, x - 54, y - 14, 108, 28, "sky" if who == "A" else "plum", 9, 3, hl=False))
            cv.add(cv.text(x, y + 6, what, 13.5, 800, fill=INK if who == "A" else "#FFFFFF"))
            if writes:
                cv.add(P.arrow(cv, [(x + 56, y), (590, y)], ARROW, 2.6, 9))
            else:
                cv.add(P.arrow(cv, [(590, y), (x + 56, y)], ARROW, 2.6, 9, dash="5 4"))
            last = i == 3
            col = ("coral" if not ok else "mint") if last else ("sun" if writes else "paper")
            cv.add(P.lift(cv, 598, y - 14, 84, 28, col, 9, 3, hl=False), cv.text(640, y + 6, val, 15, 800, fill=INK, mono=True))
        cv.add(cv.text(640, y0 + 262, ("correct: 175" if ok else "wrong: A's deposit is lost"), 14, 800, cls="il-ok" if ok else "il-bad"))
    return figure(
        "race-lost-update", cv, "A race condition: two deposits to the same balance, with and without a lock",
        "Two tasks, A and B, each deposit money into one account whose balance starts at 100. A deposits 50 and B deposits 25, so the right answer "
        "is 175. Without a lock the tasks overlap: A reads 100, then B reads 100, then A writes 150, then B writes 125. B has overwritten A's "
        "deposit and the balance is 125, so a deposit has been lost. With a lock, B waits until A has finished: A reads 100 and writes 150, then B "
        "reads 150 and writes 175. The balance is correct.",
        ["Without a lock A and B both read 100 before either has written, so each works from the same old value.",
         "With a lock only one task is inside the critical section at a time, so B reads the balance after A has written it."],
        "The result depends on the timing, which is why the fault appears only sometimes. A lock makes the read and the write one indivisible step.")


# ------------------------------------------------------------------ deadlock

@illustration("deadlock-cycle")
def _deadlock():
    cv = Canvas(800, 470).backdrop()
    cv.add(P.card(cv, 14, 24, 500, 424, 20, "two tasks, two locks, and a circle of waiting", "coral"))
    t1, b, t2, a = (130, 140), (400, 140), (400, 340), (130, 340)
    # edges
    cv.add(P.arrow(cv, [(t1[0] + 36, t1[1]), (b[0] - 40, b[1])], "#C84B43", 3.6, 12, dash="8 6"))
    cv.add(cv.text(265, t1[1] - 14, "T1 wants B", 14, 800, cls="il-bad"))
    cv.add(P.arrow(cv, [(b[0], b[1] + 38), (t2[0] - 0, t2[1] - 40)], "#2F82C0", 3.6, 12))
    cv.add(cv.text(b[0] - 14, 226, "B is held", 13.5, 800, anchor="end", cls="il-ink"), cv.text(b[0] - 14, 246, "by T2", 13.5, 800, anchor="end", cls="il-ink"))
    cv.add(P.arrow(cv, [(t2[0] - 36, t2[1]), (a[0] + 40, a[1])], "#C84B43", 3.6, 12, dash="8 6"))
    cv.add(cv.text(265, t2[1] + 30, "T2 wants A", 14, 800, cls="il-bad"))
    cv.add(P.arrow(cv, [(a[0], a[1] - 38), (t1[0], t1[1] + 40)], "#2F82C0", 3.6, 12))
    cv.add(cv.text(a[0] + 14, 226, "A is held", 13.5, 800, anchor="start", cls="il-ink"), cv.text(a[0] + 14, 246, "by T1", 13.5, 800, anchor="start", cls="il-ink"))
    # nodes
    for (x, y), nm in ((t1, "T1"), (t2, "T2")):
        cv.add(node_circle(cv, x, y, nm, "plum"))
    for (x, y), nm in ((b, "lock B"), (a, "lock A")):
        cv.add(P.lift(cv, x - 40, y - 24, 80, 48, "sun", 10, 4, hl=False), cv.text(x, y + 6, nm, 15, 800, fill=INK, mono=True))
    cv.add(P.badge(cv, 42, 66, 1))
    cv.add(cv.text(264, 296, "no task can move", 15, 800, cls="il-bad"))
    # conditions
    cv.add(P.card(cv, 534, 24, 252, 424, 20, "all four must be true", "plum"))
    conds = [("mutual exclusion", "one holder at a time"), ("hold and wait", "keeps one lock while waiting"), ("no pre-emption", "a lock cannot be taken away"), ("circular wait", "a ring of tasks waiting")]
    for i, (c, d) in enumerate(conds):
        y = 70 + i * 74
        hot = i == 3
        cv.add(P.lift(cv, 552, y, 216, 60, "coral" if hot else "paper", 10, 4, hl=False), cv.text(660, y + 25, c, 14.5, 800, fill=INK), cv.text(660, y + 45, d, 12, 650, fill=INK))
    cv.add(P.badge(cv, 566, 412, 2))
    cv.add(P.pill(cv, 676, 392, "prevent it: lock A", "mint", 13.5, 10, 28, 800), P.pill(cv, 676, 426, "always before lock B", "mint", 13.5, 10, 28, 800))
    return figure(
        "deadlock-cycle", cv, "Deadlock: each task holds one lock and waits for the other",
        "Two tasks, T1 and T2, and two locks, A and B. T1 holds lock A and wants lock B. T2 holds lock B and wants lock A. Drawn as a graph, the "
        "arrows form a circle: T1 wants B, B is held by T2, T2 wants A, and A is held by T1. Neither task can go on, and neither will ever let go. "
        "Deadlock needs four things to be true at once: mutual exclusion, hold and wait, no pre-emption, and circular wait. It can be prevented by "
        "breaking one of them, most simply by making every task acquire the locks in the same order, so that a circle cannot form.",
        ["The wait for graph has a cycle: T1 wants B, T2 holds B and wants A, and T1 holds A. Nobody can move.",
         "Deadlock needs all four conditions. Break any one, for example circular wait by always locking A before B, and it cannot happen."],
        "Databases detect deadlocks by looking for exactly this kind of cycle, then end one of the tasks to break it.")


def node_circle(cv, x, y, label, color):
    out = cv.circle(x, y + 3, 38, "#10303A", op=.16) + cv.circle(x, y, 38, cv.g(color, "deep"), stroke=PAL[color][2], sw=1.6)
    return out + cv.text(x, y + 7, label, 20, 800, fill="#FFFFFF", mono=True)


# ------------------------------------------------------------------ public key cryptography

@illustration("rsa-keys")
def _rsa():
    cv = Canvas(800, 520).backdrop()
    cv.add(P.card(cv, 14, 24, 772, 230, 20, "keeping a message secret: lock with the receiver's public key", "teal"))
    cv.add(P.badge(cv, 42, 70, 1))
    cv.add(P.person(cv, 34, 92, .5, "light", "black", "coral", "short"))
    cv.add(cv.text(64, 214, "Ali", 15, 800, cls="il-ink"))
    cv.add(chip(cv, 110, 112, 90, 40, "hello", "#FFFFFF", INK, 17))
    cv.add(P.arrow(cv, [(204, 132), (254, 132)], ARROW, 3, 10))
    cv.add(P.padlock(cv, 262, 100, .7, "sun"))
    cv.add(cv.text(292, 190, "Bea's public key", 12.5, 750, cls="il-ink"), cv.text(292, 207, "(everyone has it)", 12, 650, cls="il-ink2"))
    cv.add(P.arrow(cv, [(334, 132), (394, 132)], ARROW, 3, 10))
    cv.add(chip(cv, 400, 112, 130, 40, "xK9#qL2", "#1C2831", "#8CE3EA", 16))
    cv.add(cv.text(465, 176, "ciphertext, safe to send", 12.5, 700, cls="il-ink2"))
    cv.add(P.arrow(cv, [(534, 132), (584, 132)], ARROW, 3, 10))
    cv.add(P.key(cv, 590, 106, .8, "coral"))
    cv.add(cv.text(626, 190, "Bea's private key", 12.5, 750, cls="il-ink"), cv.text(626, 207, "(only Bea has it)", 12, 650, cls="il-ink2"))
    cv.add(P.arrow(cv, [(660, 132), (692, 132)], ARROW, 3, 10))
    cv.add(chip(cv, 696, 112, 76, 40, "hello", "#FFFFFF", INK, 17))
    cv.add(cv.text(734, 176, "Bea", 15, 800, cls="il-ink"))
    # signature
    cv.add(P.card(cv, 14, 280, 772, 230, 20, "proving who sent it: sign with your own private key", "plum"))
    cv.add(P.badge(cv, 42, 326, 2))
    cv.add(chip(cv, 70, 360, 118, 40, "pay Sam 10", "#FFFFFF", INK, 15))
    cv.add(P.arrow(cv, [(192, 380), (228, 380)], ARROW, 3, 10))
    cv.add(chip(cv, 232, 360, 66, 40, "hash", "#FFFFFF", INK, 15))
    cv.add(P.arrow(cv, [(302, 380), (336, 380)], ARROW, 3, 10))
    cv.add(P.key(cv, 340, 354, .8, "coral"))
    cv.add(cv.text(376, 428, "Ali's private key", 12.5, 750, cls="il-ink"))
    cv.add(P.arrow(cv, [(396, 380), (436, 380)], ARROW, 3, 10))
    cv.add(chip(cv, 440, 360, 108, 40, "signature", "#FFF0AD", INK, 15, mono=False))
    cv.add(P.arrow(cv, [(552, 380), (590, 380)], ARROW, 3, 10))
    cv.add(P.padlock(cv, 594, 348, .7, "sun", True))
    cv.add(cv.text(624, 428, "Ali's public key", 12.5, 750, cls="il-ink"))
    cv.add(P.arrow(cv, [(656, 380), (688, 380)], ARROW, 3, 10))
    cv.add(chip(cv, 692, 360, 82, 40, "same hash", "#C9F3E0", INK, 13.5, mono=False))
    cv.add(cv.text(400, 480, "if the hashes match the message is genuine and has not been changed", 14, 750, cls="il-ink"))
    return figure(
        "rsa-keys", cv, "Public key cryptography: encrypting for one person and signing as another",
        "Top: keeping a message secret. Ali writes hello, and locks it with Bea's public key, which everyone can have. The result, the ciphertext, "
        "is safe to send. Only Bea's private key, which only she has, can unlock it, and she reads hello. Bottom: proving who sent a message. Ali "
        "makes a hash of the message, pay Sam 10, and encrypts the hash with his own private key to make a signature. Anyone can decrypt the "
        "signature with Ali's public key and compare the result with their own hash of the message. If the hashes match, the message is genuine "
        "and has not been changed.",
        ["Confidentiality: encrypt with the receiver's public key. Only the matching private key can decrypt it.",
         "Authenticity: sign a hash of the message with your own private key. Anyone can check it with your public key."],
        "The two keys are a pair: what one locks, only the other unlocks. That removes the need to send a secret key in advance.")


# ------------------------------------------------------------------ subnet masks

@illustration("subnet-mask")
def _subnet():
    cv = Canvas(800, 470).backdrop()
    cv.add(P.card(cv, 14, 24, 772, 424, 20, "an address ANDed with its subnet mask gives the network address", "teal"))
    rows = [("address", "192.168.5.130", "11000000101010000000010110000010"),
            ("mask", "255.255.255.192", "11111111111111111111111111000000"),
            ("AND", "192.168.5.128", "11000000101010000000010110000000")]
    cw, gx = 17.2, 10
    x0 = 152
    for r, (name, dotted, bits) in enumerate(rows):
        y = 84 + r * 86
        cv.add(cv.text(26, y + 18, name, 16, 800, anchor="start", cls="il-ink", mono=True), cv.text(26, y + 38, dotted, 12, 650, anchor="start", cls="il-ink2", mono=True))
        for i, ch in enumerate(bits):
            x = x0 + i * cw + (i // 8) * gx
            host = i >= 26
            fill = "#FFE9A8" if host else "#CFEFF2"
            if r == 1 and not host and ch == "1":
                fill = "#9BDDE2"
            cv.add(cv.rect(x, y, cw - 1.5, 34, 3, fill, stroke="#B5C4CC", sw=.8))
            cv.add(cv.text(x + (cw - 1.5) / 2, y + 23, ch, 14, 800, fill=INK, mono=True))
    cv.add(P.badge(cv, 42, 62, 1))
    # braces under the last row
    nx0 = x0
    nx1 = x0 + 26 * cw + 3 * gx
    cv.add(cv.path("M%s 310 L%s 320 L%s 320 L%s 310" % (_n(nx0), _n(nx0), _n(nx1 - 4), _n(nx1 - 4)), stroke="#0F7C84", sw=3))
    cv.add(cv.text((nx0 + nx1) / 2, 346, "network part: 26 bits (the 1s in the mask)", 14.5, 800, cls="il-ink"))
    hx0 = nx1
    hx1 = x0 + 32 * cw + 3 * gx
    cv.add(cv.path("M%s 310 L%s 320 L%s 320 L%s 310" % (_n(hx0 + 2), _n(hx0 + 2), _n(hx1 - 2), _n(hx1 - 2)), stroke="#DFA000", sw=3))
    cv.add(cv.text(hx1 - 30, 346, "host: 6 bits", 14.5, 800, cls="il-ink"))
    cv.add(P.badge(cv, 44, 332, 2))
    cv.add(cv.text(400, 388, "2 to the power 6 = 64 addresses, minus the network and broadcast addresses", 14.5, 700, cls="il-ink"))
    cv.add(P.pill(cv, 400, 420, "62 usable hosts   |   written 192.168.5.128/26", "mint", 17, 20, 34, 800))
    return figure(
        "subnet-mask", cv, "Finding the network address of 192.168.5.130 with the subnet mask 255.255.255.192",
        "The address 192.168.5.130 written in 32 bits is 11000000 10101000 00000101 10000010. The subnet mask 255.255.255.192 is 26 ones followed by "
        "6 zeros: 11111111 11111111 11111111 11000000. ANDing the two, bit by bit, keeps only the bits where the mask has a 1 and gives 11000000 "
        "10101000 00000101 10000000, which is 192.168.5.128, the network address. The 26 ones are the network part, and the 6 zeros are the host "
        "part. Six host bits give 64 addresses, and two of them, the network address and the broadcast address, cannot be given to devices, so "
        "there are 62 usable hosts. The mask can also be written as a slash 26.",
        ["Write the address and the mask in binary and AND them: the result keeps the network part and zeroes the host part.",
         "The 1s in the mask are the network part and the 0s are the host part. Six host bits give 64 addresses, and 62 can be used by devices."],
        "Two devices are on the same subnet if their addresses give the same network address when ANDed with the mask.")


# ------------------------------------------------------------------ reliable delivery

@illustration("tcp-ack-retransmit")
def _tcp():
    cv = Canvas(800, 560).backdrop()
    cv.add(P.card(cv, 14, 24, 772, 520, 20, "stop and wait: how a lost or damaged packet is delivered in the end", "teal"))
    sx, rx = 150, 650
    cv.add(P.lift(cv, sx - 50, 64, 100, 34, "sky", 10, 4, hl=False), cv.text(sx, 87, "sender", 16, 800, fill=INK))
    cv.add(P.lift(cv, rx - 50, 64, 100, 34, "mint", 10, 4, hl=False), cv.text(rx, 87, "receiver", 16, 800, fill=INK))
    cv.add(cv.line(sx, 106, sx, 538, "#9FB3BE", 2, dash="4 5"), cv.line(rx, 106, rx, 538, "#9FB3BE", 2, dash="4 5"))
    events = [
        (120, "send", 1, "ok", "packet 1"), (160, "ack", 1, "ok", "ACK 1"),
        (214, "send", 2, "lost", "packet 2"), (268, "timeout", 2, "", "no ACK before the timeout"),
        (304, "send", 2, "ok", "packet 2 again"), (344, "ack", 2, "ok", "ACK 2"),
        (392, "send", 3, "bad", "packet 3"), (442, "timeout", 3, "", "damaged: checksum fails, no ACK"),
        (478, "send", 3, "ok", "packet 3 again"), (518, "ack", 3, "ok", "ACK 3"),
    ]
    for y, kind, n, fate, label in events:
        if kind == "send":
            col = "#2F82C0" if fate != "lost" else "#8799A7"
            end = rx - 8 if fate == "ok" or fate == "bad" else 400
            cv.add(P.arrow(cv, [(sx + 6, y), (end, y + 22)], col, 3.2, 11, dash="7 5" if fate == "lost" else None))
            cv.add(cv.text((sx + end) / 2, y - 6, label, 13.5, 800, cls="il-ink", mono=True))
            if fate == "lost":
                cv.add(P.cross(cv, 410, y + 24, 13))
            if fate == "bad":
                cv.add(P.cross(cv, rx + 28, y + 24, 12))
        elif kind == "ack":
            cv.add(P.arrow(cv, [(rx - 6, y), (sx + 8, y + 18)], "#2F9F77", 3.2, 11))
            cv.add(cv.text((sx + rx) / 2, y - 4, label, 13.5, 800, cls="il-ink", mono=True))
        else:
            cv.add(cv.circle(sx, y, 9, "#FFCC4A", stroke="#B98A12", sw=1.8))
            cv.add(cv.text(sx + 18, y + 5, label, 13, 700, anchor="start", cls="il-bad"))
    cv.add(P.badge(cv, 44, 142, 1), P.badge(cv, 44, 250, 2), P.badge(cv, 44, 428, 3))
    return figure(
        "tcp-ack-retransmit", cv, "Stop and wait: a lost packet and a damaged packet are both sent again",
        "A sequence diagram between a sender on the left and a receiver on the right, with time running down the page. Packet 1 is sent, and an "
        "acknowledgement, ACK 1, comes back. Packet 2 is sent and is lost on the way, so no acknowledgement arrives. The sender's timer runs out, so "
        "it sends packet 2 again, and this time ACK 2 comes back. Packet 3 arrives damaged: its checksum does not match, so the receiver throws it "
        "away and sends no acknowledgement. The sender's timer runs out again and packet 3 is sent again.",
        ["Every packet that arrives intact is acknowledged, and the sender moves on to the next.",
         "A lost packet gets no acknowledgement, so when the timer runs out the sender sends it again.",
         "A damaged packet fails its checksum and is discarded, which has the same result: no ACK, and a resend."],
        "TCP adds sequence numbers, so packets can be put in order, and a window, so many packets are in flight at once and the sender is not idle.")
