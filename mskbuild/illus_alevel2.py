"""A Level illustrations, set two: paradigms, the Little Man Computer, addressing modes, hashing,
hash tables and client side against server side."""
import hashlib
import math

from .illus import Canvas, PAL, INK, ARROW, figure, illustration, _n
from . import illus_props as P
from . import illus_glyphs as G


def wrap(text, n):
    out, cur = [], ""
    for w in text.split():
        if len(cur) + len(w) + 1 > n and cur:
            out.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    out.append(cur)
    return out


def chip(cv, x, y, w, h, text, fill="#FFFFFF", tc=INK, size=13, stroke="#9FB3BE", mono=True, weight=800):
    return cv.rect(x, y, w, h, min(8, h / 2.4), fill, stroke=stroke, sw=1.5) + cv.text(x + w / 2, y + h / 2 + size * .36, text, size, weight, fill=tc, mono=mono)


# ------------------------------------------------------------------ paradigms

@illustration("paradigms")
def _paradigms():
    cv = Canvas(800, 500).backdrop()
    spec = [("Procedural", "sky", "good for: tasks that are a series of steps"), ("Object oriented", "mint", "good for: large systems and teams"),
            ("Declarative", "coral", "good for: queries and safe concurrency"), ("Assembly", "sun", "good for: drivers and tight hardware limits")]
    for n, (title, col, good) in enumerate(spec):
        x, y = (14, 406)[n % 2], (30, 258)[n // 2]
        cv.add(P.card(cv, x, y, 380, 214, 20, title, col), P.badge(cv, x + 22, y + 24, n + 1))
        cv.add(cv.text(x + 190, y + 204, good, 13, 700, cls="il-ink"))
        if n == 0:
            cv.add(P.lift(cv, x + 140, y + 44, 100, 30, "teal", 8, 4, hl=False), cv.text(x + 190, y + 64, "main", 13, 800, fill=INK, mono=True))
            for k, t in enumerate(("get_scores()", "average()", "show()")):
                bx = x + 30 + k * 112
                cv.add(P.lift(cv, bx, y + 120, 104, 30, "sky", 8, 4, hl=False), cv.text(bx + 52, y + 140, t, 12.5, 800, fill=INK, mono=True))
                cv.add(P.arrow(cv, [(x + 190, y + 82), (bx + 52, y + 116)], ARROW, 2.5, 8))
            cv.add(cv.text(x + 190, y + 176, "procedures called in order, data passed between them", 12, 650, cls="il-ink2"))
        elif n == 1:
            cv.add(P.lift(cv, x + 110, y + 42, 160, 54, "mint", 10, 4, hl=False), cv.text(x + 190, y + 62, "Pet  (class)", 13.5, 800, fill=INK, mono=True), cv.text(x + 190, y + 82, "name  age  speak()", 12, 700, fill=INK, mono=True))
            for k, (nm, ag) in enumerate((("rex", "3"), ("mia", "5"))):
                bx = x + 42 + k * 178
                cv.add(P.arrow(cv, [(x + 190, y + 104), (bx + 70, y + 122)], ARROW, 2.5, 8, dash="4 4"))
                cv.add(P.lift(cv, bx, y + 126, 140, 52, "paper", 10, 4, hl=False), cv.text(bx + 70, y + 146, "%s: Pet" % nm, 13, 800, fill=INK, mono=True), cv.text(bx + 70, y + 166, "age %s  speak()" % ag, 11.5, 700, fill=INK, mono=True))
        elif n == 2:
            cv.add(G.code(cv, x + 24, y + 44, 332, ["SELECT name FROM pupils", "WHERE year = 12"], title=None, size=12.5, numbers=False))
            cv.add(P.arrow(cv, [(x + 190, y + 122), (x + 190, y + 138)], ARROW, 3, 9))
            for k, nm in enumerate(("Aisha", "Ben", "Chloe")):
                cv.add(chip(cv, x + 70 + k * 84, y + 144, 76, 24, nm, "#FFFFFF", INK, 12, mono=False, weight=750))
            cv.add(cv.text(x + 190, y + 182, "say what you want, not how to get it", 12, 650, cls="il-ink2"))
        else:
            for k, (a_, b_) in enumerate((("LDA 5", "505"), ("ADD 6", "106"), ("STA 7", "307"))):
                yy = y + 50 + k * 40
                cv.add(chip(cv, x + 40, yy, 120, 28, a_, "#1C2831", "#8CE3EA", 14), P.arrow(cv, [(x + 168, yy + 14), (x + 214, yy + 14)], ARROW, 2.5, 8))
                cv.add(chip(cv, x + 222, yy, 120, 28, b_, "#FFFFFF", INK, 14))
            cv.add(cv.text(x + 100, y + 44, "assembly", 11.5, 700, cls="il-ink2"), cv.text(x + 282, y + 44, "machine code", 11.5, 700, cls="il-ink2"))
            cv.add(cv.text(x + 190, y + 176, "one assembly instruction, one machine instruction", 12, 650, cls="il-ink2"))
    return figure(
        "paradigms", cv, "Four programming paradigms: procedural, object oriented, declarative and assembly",
        "Four paradigms, one card each. Procedural: a main program calls procedures in order, get scores, average and show, passing data between "
        "them. It is good for tasks that are a series of steps. Object oriented: a class, here Pet with a name, an age and a speak method, is "
        "used to create objects such as rex and mia. It is good for large systems and teams. Declarative: an SQL query, select name from pupils "
        "where year equals 12, says what you want and not how to get it, and returns Aisha, Ben and Chloe. It is good for queries and for safe "
        "concurrency. Assembly: each line, such as LDA 5, ADD 6 and STA 7, matches one machine instruction, 505, 106 and 307. It is good for "
        "device drivers and tight hardware limits.",
        ["Procedural: steps grouped into procedures that call each other.", "Object oriented: data and methods bundled into objects made from classes.",
         "Declarative: say what is wanted, not how to compute it.", "Assembly: one instruction for each machine instruction, with direct control of the hardware."],
        "Justify the paradigm from the scenario: size of the team, how the system will grow, and how close to the hardware it must be.")


# ------------------------------------------------------------------ the Little Man Computer

@illustration("lmc-machine")
def _lmc():
    cv = Canvas(800, 500).backdrop()
    cv.add(P.card(cv, 14, 30, 474, 452, 20, "Mailboxes: the memory", "teal"), P.badge(cv, 36, 56, 1))
    prog = {0: "901", 1: "107", 2: "902", 3: "000", 7: "005"}
    notes = {0: "INP", 1: "ADD 07", 2: "OUT", 3: "HLT", 7: "DAT 5"}
    for a in range(10):
        c, r = a % 5, a // 5
        x, y = 32 + c * 88, 86 + r * 98
        filled = a in prog
        cv.add(cv.rect(x, y, 80, 76, 10, "#FFFFFF" if filled else "var(--il-band)", stroke="#9FB3BE", sw=1.6))
        cv.add(cv.text(x + 8, y + 18, "%02d" % a, 12, 750, anchor="start", fill="#4A6470", mono=True) if filled else cv.text(x + 8, y + 18, "%02d" % a, 12, 750, anchor="start", cls="il-ink2", mono=True))
        if filled:
            cv.add(cv.text(x + 40, y + 46, prog[a], 20, 800, fill=INK, mono=True), cv.text(x + 40, y + 66, notes[a], 11.5, 700, fill="#4A6470", mono=True))
    cv.add(cv.text(120, 286, "program", 13, 750, cls="il-ink2"), cv.text(384, 286, "data", 13, 750, cls="il-ink2"))
    cv.add(cv.text(251, 322, "A mailbox holds a three digit number: an instruction or data.", 13.5, 700, cls="il-ink"))
    cv.add(P.badge(cv, 36, 344, 2))
    cv.add(cv.text(60, 350, "Reading an instruction", 14.5, 800, anchor="start", cls="il-ink"))
    cv.add(chip(cv, 70, 372, 60, 56, "107", "#FFFFFF", INK, 24), cv.text(100, 450, "the number", 12, 650, cls="il-ink2"))
    cv.add(P.arrow(cv, [(140, 400), (178, 400)], ARROW, 3, 9))
    cv.add(P.lift(cv, 188, 372, 42, 56, "coral", 8, 4, hl=False), cv.text(209, 408, "1", 24, 800, fill=INK, mono=True), cv.text(209, 450, "opcode", 12, 650, cls="il-ink2"))
    cv.add(P.lift(cv, 240, 372, 76, 56, "sky", 8, 4, hl=False), cv.text(278, 408, "07", 24, 800, fill=INK, mono=True), cv.text(278, 450, "operand", 12, 650, cls="il-ink2"))
    cv.add(cv.text(396, 394, "1 = ADD", 14, 800, cls="il-ink", mono=True), cv.text(396, 416, "07 = mailbox 07", 12.5, 700, cls="il-ink", mono=True))
    # the processor
    cv.add(P.card(cv, 504, 30, 282, 452, 20, "Registers and trays", "coral"), P.badge(cv, 526, 56, 3))
    regs = [("Program counter", "01", "sun"), ("Instruction register", "107", "sky"), ("Accumulator", "12", "mint")]
    for i, (name, val, col) in enumerate(regs):
        y = 80 + i * 92
        cv.add(cv.text(528, y + 12, name, 14, 750, anchor="start", cls="il-ink"))
        cv.add(P.lift(cv, 528, y + 22, 126, 42, col, 9, 4, hl=False), cv.text(591, y + 52, val, 22, 800, fill=INK, mono=True))
        cv.add(cv.text(672, y + 48, ("next address", "what it is doing", "the working number")[i], 12, 650, anchor="start", cls="il-ink2"))
    for i, (name, val, dx) in enumerate((("Input", "7", 0), ("Output", "12", 118))):
        x = 528 + dx
        cv.add(cv.text(x, 372, name, 14, 750, anchor="start", cls="il-ink"))
        cv.add(P.lift(cv, x, 384, 100, 50, "slate", 10, 4, hl=False), cv.text(x + 50, 418, val, 22, 800, fill=INK, mono=True))
    return figure(
        "lmc-machine", cv, "The Little Man Computer: mailboxes, the instruction format, the registers and the input and output trays",
        "The Little Man Computer is a simple model of a processor and memory. The memory is a set of numbered mailboxes, each holding a three "
        "digit number that is either an instruction or data. In this program mailbox 00 holds 901, which is INP, mailbox 01 holds 107, which is "
        "ADD 07, mailbox 02 holds 902, which is OUT, mailbox 03 holds 000, which is HLT, and mailbox 07 holds the data 5. An instruction is a "
        "number split in two: the first digit is the opcode, which says what to do, and the last two digits are the operand, which says which "
        "mailbox, so 107 is 1, ADD, with mailbox 07. The processor has a program counter, here 01, which holds the next address, an "
        "instruction register, here 107, holding the instruction being carried out, and an accumulator, here 12, which holds the working "
        "number. There is an input tray, here 7, and an output tray, here 12.",
        ["Memory is a row of numbered mailboxes. Each holds a three digit number, an instruction or data.",
         "An instruction is an opcode, the first digit, and an operand, the last two digits. 107 means ADD with mailbox 07.",
         "The program counter, instruction register and accumulator do the work, and the input and output trays connect to the outside."],
        "The little man does fetch, decode, execute: read the program counter, fetch that mailbox, then carry out the instruction.")


# ------------------------------------------------------------------ addressing modes

@illustration("addressing-modes")
def _modes():
    cv = Canvas(800, 500).backdrop()
    spec = [("Immediate", "sky", "LDA #5", "the operand is the data", None), ("Direct", "mint", "LDA 5", "the operand is the address of the data", {5: ("42", "sun")}),
            ("Indirect", "coral", "LDA (5)", "the operand is the address of the address", {5: ("8", "coral"), 8: ("42", "sun")}),
            ("Indexed", "plum", "LDA 5,X", "address = operand + index register (X = 3)", {8: ("42", "sun")})]
    for n, (title, col, instr, rule, cells) in enumerate(spec):
        x, y = (14, 406)[n % 2], (30, 258)[n // 2]
        cv.add(P.card(cv, x, y, 380, 214, 20, title, col), P.badge(cv, x + 22, y + 24, n + 1))
        cv.add(P.lift(cv, x + 24, y + 52, 130, 38, "dark", 10, 4, hl=False), cv.text(x + 89, y + 77, instr, 16, 800, fill="#8CE3EA", mono=True))
        for i, ln in enumerate(wrap(rule, 24)):
            cv.add(cv.text(x + 24, y + 112 + i * 16, ln, 12.5, 700, anchor="start", cls="il-ink"))
        if cells is None:
            cv.add(P.arrow(cv, [(x + 160, y + 71), (x + 232, y + 71)], PAL["teal"][2], 3.5, 10))
            cv.add(P.lift(cv, x + 242, y + 52, 100, 38, "sun", 10, 4, hl=False), cv.text(x + 292, y + 77, "5", 18, 800, fill=INK, mono=True), cv.text(x + 292, y + 108, "ACC = 5", 12.5, 750, cls="il-ink", mono=True))
        else:
            for k, a in enumerate(range(4, 10)):
                cy_ = y + 40 + k * 26
                val, hl = cells.get(a, ("", None))
                cv.add(cv.rect(x + 262, cy_, 80, 24, 5, cv.g(hl) if hl else "#FFFFFF", stroke="#9FB3BE", sw=1.2))
                cv.add(cv.text(x + 270, cy_ + 16.5, "%d" % a, 11.5, 700, anchor="start", fill=INK if hl else "#4A6470", mono=True), cv.text(x + 316, cy_ + 17, val, 13, 800, fill=INK, mono=True))
            if n == 1:
                cv.add(P.arrow(cv, [(x + 160, y + 71), (x + 258, y + 40 + 1 * 26 + 12)], PAL["teal"][2], 3, 9))
            elif n == 2:
                cv.add(P.arrow(cv, [(x + 160, y + 71), (x + 258, y + 40 + 1 * 26 + 12)], PAL["teal"][2], 3, 9))
                cv.add(P.curve_arrow(cv, (x + 346, y + 40 + 26 + 12), (x + 374, y + 90), (x + 374, y + 130), (x + 346, y + 40 + 4 * 26 + 12), PAL["coral"][2], 3, 9))
            else:
                cv.add(P.pill(cv, x + 89, y + 150, "X = 3", "plum", 13, 12, 24, 800))
                cv.add(cv.text(x + 89, y + 184, "5 + 3 = 8", 13, 800, cls="il-ink", mono=True))
                cv.add(P.arrow(cv, [(x + 160, y + 71), (x + 258, y + 40 + 4 * 26 + 12)], PAL["teal"][2], 3, 9))
            if n < 3:
                cv.add(cv.text(x + 24, y + 184, "ACC = 42", 13, 800, anchor="start", cls="il-ink", mono=True))
    return figure(
        "addressing-modes", cv, "Four addressing modes loading from memory: immediate, direct, indirect and indexed",
        "Four ways an instruction can find its data. In immediate addressing, LDA hash 5, the operand is the data itself, so the accumulator gets 5. "
        "In direct addressing, LDA 5, the operand is the address of the data: memory address 5 holds 42, so the accumulator gets 42. In indirect "
        "addressing, LDA in brackets 5, the operand is the address of the address: memory address 5 holds 8, which is the address of the data, "
        "and memory address 8 holds 42. In indexed addressing, LDA 5 comma X, the address is the operand plus the index register: with X equal to 3 "
        "the address is 8, which holds 42.",
        ["Immediate: the operand is the data.", "Direct: the operand is the address of the data.", "Indirect: the operand is the address of the address of the data.",
         "Indexed: add the index register to the operand to get the address, which is useful for arrays."],
        "Say what the operand means in each mode: the value, an address, an address of an address, or a base address plus an index.")


# ------------------------------------------------------------------ hashing

def digest(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


@illustration("hashing")
def _hashing():
    cv = Canvas(800, 500).backdrop()
    cv.add(P.card(cv, 14, 30, 520, 324, 20, "A hash function", "teal"), P.badge(cv, 36, 56, 1))
    rows = [("hello", "hello"), ("Hello", "Hello"), ("a whole book", "a" * 4000)]
    for i, (label, text) in enumerate(rows):
        y = 82 + i * 86
        if i == 2:
            cv.add(P.doc(cv, 40, y - 4, .6, 62, 80, 5, "paper"))
            cv.add(cv.text(78, y + 62, label, 12, 650, cls="il-ink2"))
        else:
            cv.add(chip(cv, 34, y + 6, 90, 36, label, "#FFFFFF", INK, 16))
        cv.add(P.arrow(cv, [(132, y + 24), (170, y + 24)], ARROW, 3.5, 10))
        cv.add(P.lift(cv, 178, y, 94, 48, "dark", 10, 4, hl=False), cv.text(225, y + 24, "hash", 14, 800, fill="#FFFFFF", mono=True), cv.text(225, y + 40, "function", 11, 650, fill="#E6EEF2"))
        cv.add(P.arrow(cv, [(280, y + 24), (318, y + 24)], ARROW, 3.5, 10))
        cv.add(chip(cv, 326, y + 6, 196, 36, digest(text)[:14] + "...", "#FFFFFF", INK, 15))
    cv.add(cv.text(274, 336, "SHA-256 shown, cut short: the real hash is 64 hex digits", 12, 650, cls="il-ink2"))
    # properties
    cv.add(P.card(cv, 550, 30, 236, 324, 20, "Four properties", "coral"), P.badge(cv, 572, 56, 2))
    for i, (a_, b_) in enumerate((("Same input, same hash", "every time"), ("One way", "it cannot be reversed"), ("A tiny change", "gives a very different hash"), ("Fixed length", "however big the input"))):
        y = 90 + i * 64
        cv.add(P.tick(cv, 576, y + 6, 10), cv.text(598, y + 4, a_, 14, 750, anchor="start", cls="il-ink"), cv.text(598, y + 24, b_, 12.5, 650, anchor="start", cls="il-ink2"))
    # the use
    cv.add(P.card(cv, 14, 374, 772, 108, 20, "Checking a password without storing it", "sun"), P.badge(cv, 36, 400, 3))
    cv.add(chip(cv, 40, 420, 90, 38, "hello", "#FFFFFF", INK, 16), P.arrow(cv, [(138, 439), (176, 439)], ARROW, 3.5, 10))
    cv.add(P.lift(cv, 184, 418, 84, 40, "dark", 10, 4, hl=False), cv.text(226, 443, "hash", 14, 800, fill="#FFFFFF", mono=True))
    cv.add(P.arrow(cv, [(276, 439), (314, 439)], ARROW, 3.5, 10), P.pill(cv, 380, 439, "match?", "paper", 15, 14, 30, 800))
    cv.add(cv.text(380, 474, "typed password, hashed", 11.5, 650, cls="il-ink2"))
    cv.add(chip(cv, 452, 420, 196, 38, digest("hello")[:14] + "...", "#FFFFFF", INK, 15))
    cv.add(cv.text(550, 474, "the hash that was stored", 11.5, 650, cls="il-ink2"))
    cv.add(P.tick(cv, 690, 439, 14), cv.text(712, 444, "let in", 15, 800, anchor="start", cls="il-ink"))
    return figure(
        "hashing", cv, "A hash function turns any input into a fixed length hash, and how that is used to check a password",
        "A hash function turns any input into a fixed length value called a hash. The input hello gives one hash, the input Hello with a capital "
        "H gives a completely different one, and a whole book gives a hash of exactly the same length. The hashes shown are real SHA-256 "
        "values, cut short. A hash function has four properties: the same input always gives the same hash, it is one way so it cannot be "
        "reversed, a tiny change in the input gives a very different hash, and the hash is a fixed length however big the input is. A system "
        "can check a password without storing it: it stores only the hash, hashes what the user types, and lets them in if the two hashes match.",
        ["The same hash function turns hello, Hello and a whole book into hashes of the same length. A tiny change gives a completely different hash.",
         "A hash is the same every time for the same input, cannot be reversed, and is a fixed length.",
         "Store only the hash of a password. When someone logs in, hash what they typed and compare it with the stored hash."],
        "Hashing is not encryption: there is no key and no way back. That is why it suits passwords and checking that a file has not changed.")


# ------------------------------------------------------------------ hash tables

def simple_hash(s, n=8):
    return sum(ord(c) for c in s) % n


@illustration("hash-table")
def _hashtable():
    cv = Canvas(800, 500).backdrop()
    keys = ["Ada", "Bob", "Zed", "Eve"]
    cv.add(P.card(cv, 14, 30, 220, 452, 20, "Keys", "sky"), P.badge(cv, 36, 56, 1))
    cv.add(P.card(cv, 250, 30, 224, 452, 20, "Hash function", "teal"), P.badge(cv, 272, 56, 2))
    cv.add(P.card(cv, 490, 30, 296, 452, 20, "Array of 8 buckets", "coral"), P.badge(cv, 512, 56, 3))
    cv.add(cv.text(362, 96, "add the character codes,", 13, 700, cls="il-ink"), cv.text(362, 114, "then divide by 8 and", 13, 700, cls="il-ink"), cv.text(362, 132, "keep the remainder", 13, 700, cls="il-ink"))
    cv.add(G.code(cv, 266, 152, 192, ["Ada: 65+100+97", "     = 262", "262 mod 8 = 6"], title=None, size=12, numbers=False))
    ky = {}
    for i, k in enumerate(keys):
        y = 92 + i * 90
        ky[k] = y + 20
        cv.add(chip(cv, 40, y, 100, 40, k, "#FFFFFF", INK, 17))
    bx = 520
    for b in range(8):
        y = 78 + b * 49
        cv.add(cv.rect(bx, y + 4, 164, 38, 7, "var(--il-band)", stroke="#9FB3BE", sw=1.4))
        cv.add(cv.text(bx + 10, y + 28, str(b), 14, 800, anchor="start", cls="il-ink", mono=True))
    cols = {"Ada": "sun", "Bob": "mint", "Zed": "coral", "Eve": "sky"}
    placed = {}
    for k in keys:
        b = simple_hash(k)
        slot = placed.get(b, 0)
        placed[b] = slot + 1
        y = 78 + b * 49
        cv.add(P.lift(cv, bx + 30 + slot * 66, y + 8, 52, 30, cols[k], 8, 3, hl=False), cv.text(bx + 56 + slot * 66, y + 28, k, 14, 800, fill=INK, mono=True))
        if slot:
            cv.add(P.arrow(cv, [(bx + 84, y + 23), (bx + 96, y + 23)], ARROW, 2.5, 6))
    # lines from keys through the function to the buckets
    for k in keys:
        b = simple_hash(k)
        by = 78 + b * 49 + 23
        cv.add(P.arrow(cv, [(146, ky[k]), (250, ky[k])], PAL[cols[k]][2], 3.5, 10))
        cv.add(cv.path("M474 %s C492 %s 496 %s 514 %s" % (_n(ky[k]), _n(ky[k]), _n(by), _n(by)), stroke=PAL[cols[k]][2], sw=3.5))
    cv.add(cv.text(262, 330, "Bob and Zed both give 3.", 13, 800, anchor="start", cls="il-bad"), cv.text(262, 349, "That is a collision, so they", 12.5, 700, anchor="start", cls="il-ink"), cv.text(262, 366, "are chained in bucket 3.", 12.5, 700, anchor="start", cls="il-ink"))
    return figure(
        "hash-table", cv, "Keys hashed into the buckets of a hash table, with a collision",
        "A hash table stores each key in a bucket chosen by a hash function. Here the hash function adds up the character codes of the key, divides "
        "by 8 and keeps the remainder. For Ada that is 65 plus 100 plus 97, which is 262, and 262 mod 8 is 6, so Ada goes in bucket 6. Bob goes "
        "in bucket 3, Eve in bucket 0, and Zed also gives 3. Bob and Zed hash to the same bucket, which is a collision, and here it is "
        "handled by chaining: both are kept in a list in bucket 3.",
        ["Four keys to store: Ada, Bob, Zed and Eve.", "The hash function turns each key into a bucket number, for Ada 65 + 100 + 97 = 262, and 262 mod 8 = 6.",
         "Each key is stored in its bucket. Bob and Zed both give 3, which is a collision, so they are chained in the same bucket."],
        "Lookup is fast because the hash goes straight to the bucket, instead of searching. A good hash function spreads keys evenly.")
