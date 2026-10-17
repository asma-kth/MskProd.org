"""Illustrations for data representation: hexadecimal, character codes, shifts, overflow,
run length encoding, Huffman coding and image metadata."""
import math

from .illus import Canvas, PAL, INK, ARROW, figure, illustration, _n
from . import illus_props as P
from . import illus_glyphs as G


def bit_row(cv, x, y, s, cw=33, ch=36, gap=4, nib=9, size=18, ones="sky", zeros="slate", op=None, override=None):
    """A row of bit cells, 1s coloured and 0s pale. s is a string such as "0000 1100".

    A space in s starts a new nibble, with a wider gap. ones may be a list with one colour
    per nibble, and override maps a bit's index to its own colour. Returns (markup, x of every
    cell, width of the row).
    """
    out, xs, cx, k, idx = "", [], x, 0, 0
    for c in s:
        if c == " ":
            cx += nib - gap
            k += 1
            continue
        col = (ones[min(k, len(ones) - 1)] if isinstance(ones, (list, tuple)) else ones) if c == "1" else zeros
        if override and idx in override and c == "1":
            col = override[idx]
        idx += 1
        cell = P.lift(cv, cx, y, cw, ch, col, 8, 4, hl=False)
        cell += cv.text(cx + cw / 2, y + ch / 2 + size * .36, c, size, 800, fill=INK if col in ("sky", "slate", "sun", "mint", "teal", "coral") else P._on(col), mono=True)
        out += '<g opacity="%s">%s</g>' % (op, cell) if op is not None else cell
        xs.append(cx)
        cx += cw + gap
    return out, xs, cx - gap - x


def outline(cv, x, y, w, h, color, r=9, sw=3, dash=None):
    """A ring just outside a cell, to call it out."""
    return cv.rect(x - 4, y - 4, w + 8, h + 8, r, "none", stroke=color, sw=sw, dash=dash)


def bracket(cv, x0, x1, y, color, up=8):
    """A square bracket under a run of cells, opening upwards."""
    return cv.path("M%s %s L%s %s L%s %s L%s %s" % (_n(x0), _n(y - up), _n(x0), _n(y), _n(x1), _n(y), _n(x1), _n(y - up)), stroke=color, sw=3)


# ------------------------------------------------------------------ hexadecimal

@illustration("hex-nibbles")
def _hex():
    cv = Canvas(800, 500).backdrop()
    cv.add(P.card(cv, 14, 34, 772, 262, 20, "Binary to hex, one nibble at a time", "teal"))
    row, xs, wd = bit_row(cv, 60, 76, "1010 1111", cw=44, ch=46, gap=6, nib=34, size=22, ones=["sky", "coral"])
    cv.add(row)
    cols = [("sky", 0, "8 + 2 = 10", "A"), ("coral", 4, "8 + 4 + 2 + 1 = 15", "F")]
    centres = []
    for col, i0, calc, digit in cols:
        x0, x1 = xs[i0], xs[i0 + 3] + 44
        mid = (x0 + x1) / 2
        centres.append(mid)
        cv.add(bracket(cv, x0, x1, 142, PAL[col][2]))
        cv.add(P.pill(cv, mid, 170, calc, "paper", 14.5, 12, 28, 700))
        cv.add(P.arrow(cv, [(mid, 190), (mid, 212)], PAL[col][2], 4, 11))
        cv.add(P.lift(cv, mid - 30, 220, 60, 56, col, 12, 6), cv.text(mid, 220 + 28 + 11, digit, 30, 800, fill=INK, mono=True))
    # the join
    cv.add(P.arrow(cv, [(centres[1] + 40, 250), (556, 250)], PAL["deep"][1], 4, 11))
    cv.add(P.lift(cv, 566, 214, 190, 64, "deep", 14, 6, hl=False), cv.text(661, 214 + 32 + 12, "AF", 36, 800, fill="#FFFFFF", mono=True))
    cv.add(cv.text(661, 206, "side by side", 13.5, 700, cls="il-ink2"))
    # the table of sixteen digits
    cv.add(P.card(cv, 14, 322, 772, 168, 20, "The sixteen hex digits", "coral"))
    for r, (lab, y) in enumerate((("hex", 368), ("denary", 410), ("binary", 436))):
        cv.add(cv.text(34, y, lab, 13, 700, anchor="start", cls="il-ink2"))
    for d in range(16):
        x = 112 + d * 41
        col = "sky" if d < 10 else "coral"
        cv.add(P.lift(cv, x, 346, 36, 36, col, 9, 5, hl=False), cv.text(x + 18, 346 + 18 + 7, "%X" % d, 19, 800, fill=INK, mono=True))
        cv.add(cv.text(x + 18, 410, str(d), 14, 700, cls="il-ink", mono=True), cv.text(x + 18, 436, format(d, "04b"), 11.5, 600, cls="il-ink2", mono=True))
    cv.add(cv.text(400, 470, "One hex digit is always exactly four bits.", 14.5, 700, cls="il-ink"))
    cv.add(P.badge(cv, 36, 56, 1), P.badge(cv, 86, 170, 2), P.badge(cv, 580, 208, 3), P.badge(cv, 32, 324, 4))
    return figure(
        "hex-nibbles", cv, "Converting 1010 1111 to hexadecimal one nibble at a time, and the sixteen hex digits",
        "How to convert a byte to hexadecimal. The byte 1010 1111 is split into two nibbles of four bits each: 1010 on the left and 1111 on the "
        "right. Each nibble is converted on its own using the place values 8, 4, 2 and 1. The left nibble is 8 plus 2, which is 10, and 10 is the "
        "hex digit A. The right nibble is 8 plus 4 plus 2 plus 1, which is 15, and 15 is the hex digit F. Written side by side the byte is AF in "
        "hex. Underneath is a table of all sixteen hex digits with their denary and four bit binary values: 0 to 9 are written as themselves and "
        "10 to 15 are written A, B, C, D, E and F.",
        ["Split the byte into two nibbles of four bits. Colours keep each nibble with its digit.",
         "Convert each nibble on its own with 8, 4, 2 and 1: 1010 is 10 and 1111 is 15.",
         "Write each value as one hex digit, 10 as A and 15 as F, and put them side by side.",
         "Learn the table: 0 to 9 look the same in hex, then A is 10 up to F which is 15."],
        "Split into nibbles, convert each, join them up. Going the other way, turn each hex digit back into four bits.")


# ------------------------------------------------------------------ character codes

def smiley(cv, cx, cy, r=15):
    out = cv.circle(cx, cy, r, "#FFD24A", stroke="#B98A12", sw=1.6)
    out += cv.circle(cx - r * .34, cy - r * .2, r * .11, INK) + cv.circle(cx + r * .34, cy - r * .2, r * .11, INK)
    out += cv.path("M%s %s Q%s %s %s %s" % (_n(cx - r * .5), _n(cy + r * .28), _n(cx), _n(cy + r * .86), _n(cx + r * .5), _n(cy + r * .28)), stroke=INK, sw=max(1.6, r * .12))
    return out


@illustration("char-codes")
def _chars():
    cv = Canvas(800, 500).backdrop()
    cv.add(P.card(cv, 14, 34, 772, 262, 20, "Every character is stored as a number", "teal"))
    rows = [("A", 65, "sky"), ("B", 66, "sky"), ("a", 97, "mint"), ("7", 55, "sun")]
    for i, (ch_, code, col) in enumerate(rows):
        y = 70 + i * 54
        cv.add(P.lift(cv, 40, y, 48, 42, col, 10, 5, hl=False), cv.text(64, y + 21 + 9, ch_, 26, 800, fill=INK, mono=True))
        cv.add(P.arrow(cv, [(96, y + 21), (124, y + 21)], ARROW, 3.5, 10))
        cv.add(cv.rect(132, y, 66, 42, 10, "#FFFFFF", stroke="#B9C6CE", sw=2), cv.text(165, y + 21 + 8, str(code), 22, 800, fill=INK, mono=True))
        cv.add(P.arrow(cv, [(206, y + 21), (234, y + 21)], ARROW, 3.5, 10))
        row, _, _ = bit_row(cv, 242, y + 3, format(code, "08b")[:4] + " " + format(code, "08b")[4:], cw=26, ch=30, gap=3, nib=9, size=15, ones="teal")
        cv.add(row)
    # what to notice
    cv.add(P.card(cv, 520, 62, 252, 216, 16))
    notes = [("Codes run in order:", "A 65, B 66, C 67 ..."), ("Lower case is 32 higher:", "a is 97, A is 65"), ("The character 7 is code 55,", "not the number 7")]
    for i, (a_, b_) in enumerate(notes):
        y = 96 + i * 62
        cv.add(P.tick(cv, 546, y + 4, 10))
        cv.add(cv.text(566, y, a_, 13.5, 750, anchor="start", cls="il-ink"), cv.text(566, y + 20, b_, 13.5, 650, anchor="start", cls="il-ink2", mono=True))
    # the three sets
    cv.add(P.card(cv, 14, 322, 772, 168, 20, "Three character sets", "plum"))
    sets = [("ASCII", "7 bits each", "128 characters", "sky", ["A", "z", "5", "?"]),
            ("Extended ASCII", "8 bits each", "256 characters", "mint", ["é", "ñ", "£", "©"]),
            ("Unicode", "up to 32 bits each", "over a million", "plum", ["Ω", "Ж", None])]
    for i, (name, bits_, count, col, sample) in enumerate(sets):
        x = 34 + i * 246
        if col == "plum":       # white text needs the darker face
            cv.add(cv.rect(x, 352, 232, 128, 14, PAL[col][2]), cv.rect(x, 346, 232, 128, 14, cv.g(col, "deep")))
        else:
            cv.add(P.lift(cv, x, 346, 232, 128, col, 14, 6, hl=False))
        tc = "#FFFFFF" if col == "plum" else INK
        cv.add(cv.text(x + 116, 374, name, 17, 750, fill=tc), cv.text(x + 116, 394, bits_, 13, 600, fill=tc))
        cv.add(cv.text(x + 116, 420, count, 19, 800, fill=tc, mono=True))
        n = len(sample)
        x0 = x + 116 - (n * 36 - 6) / 2
        for j, g_ in enumerate(sample):
            gx = x0 + j * 36
            cv.add(cv.rect(gx, 434, 30, 28, 7, "#FFFFFF"))
            cv.add(smiley(cv, gx + 15, 448, 11) if g_ is None else cv.text(gx + 15, 453, g_, 16, 750, fill=INK))
    cv.add(P.badge(cv, 36, 56, 1), P.badge(cv, 536, 64, 2), P.badge(cv, 36, 326, 3))
    return figure(
        "char-codes", cv, "Characters stored as numbers, and the three character sets ASCII, extended ASCII and Unicode",
        "Computers store text as numbers. A character set is the agreed list that says which number means which character. In ASCII the capital "
        "letter A is 65, which is 0100 0001 in binary, B is 66, a lower case a is 97 and the character 7 is 55. The codes run in order, so B is "
        "always one more than A, and a lower case letter is 32 higher than its capital. The character 7 is text with code 55, which is different "
        "from the number 7. Below are three character sets. ASCII uses 7 bits per character and so holds 128 characters. Extended ASCII uses 8 "
        "bits and holds 256, adding accents and symbols such as é, ñ and £. Unicode uses up to 32 bits and holds over a million characters, "
        "covering every writing system and emoji, with the first 128 codes kept the same as ASCII.",
        ["Each character has a code number, and the computer stores that number in binary.",
         "The codes run in order, so you can work out C from A. The character 7 is not the number 7.",
         "More bits per character means more characters: 128, then 256, then over a million."],
        "A character set is just an agreed table of numbers. Unicode is needed because 256 characters cannot cover the world's languages.")


# ------------------------------------------------------------------ binary shifts

@illustration("binary-shifts")
def _shifts():
    cv = Canvas(800, 500).backdrop()
    cw, ch, gap, nib = 33, 36, 4, 9
    bx, ax = 56, 470
    specs = [
        (34, "Shift left by 1 place: × 2", "teal", "0000 0110", "0000 1100", "= 6", "= 12", "<< 1", "× 2", "new0r", None),
        (180, "Shift right by 2 places: ÷ 4", "coral", "0001 1000", "0000 0110", "= 24", "= 6", ">> 2", "÷ 4", "new0l2", None),
        (326, "Careful: a 1 can fall off the end", "plum", "1100 0000", "1000 0000", "= 192", "= 128, not 384", "<< 1", "bit lost", "new0r", "lost"),
    ]
    for n, (y, title, col, before, after, lb, la, op_, res, new, lost) in enumerate(specs):
        cv.add(P.card(cv, 14, y, 772, 130, 18, title, col, tx=.3))
        r1, xs1, _ = bit_row(cv, bx, y + 36, before, cw=cw, ch=ch, gap=gap, nib=nib, ones="sky")
        r2, xs2, _ = bit_row(cv, ax, y + 36, after, cw=cw, ch=ch, gap=gap, nib=nib, ones="sky")
        cv.add(r1, r2)
        if new == "new0r":
            cv.add(outline(cv, xs2[7], y + 36, cw, ch, "#C84B43", dash="5 4"))
        else:
            for k in (0, 1):
                cv.add(outline(cv, xs2[k], y + 36, cw, ch, "#C84B43", dash="5 4"))
        if lost:
            cv.add(outline(cv, xs1[0], y + 36, cw, ch, "#BA352D", sw=3.4))
            cv.add(cv.rect(ax - 46, y + 38, 32, 32, 8, "none", stroke="#BA352D", sw=2.4, dash="4 4"), cv.text(ax - 30, y + 61, "1", 17, 800, cls="il-bad", mono=True))
        # the middle: the rule and what it does
        cv.add(P.pill(cv, 392, y + 40, op_, "paper", 14.5, 11, 26, 800))
        cv.add(P.arrow(cv, [(362, y + 58), (418, y + 58)], PAL[col][2], 4.5, 12))
        cv.add(cv.text(392, y + 84, res, 14.5, 800, cls="il-ink"))
        cv.add(cv.text(bx + 148, y + 98, lb, 15, 750, cls="il-ink", mono=True), cv.text(ax + 148, y + 98, la, 15, 750, cls="il-ink", mono=True))
    cv.add(cv.rect(60, 474, 20, 14, 4, "none", stroke="#C84B43", sw=2.4, dash="4 3"), cv.text(88, 486, "a 0 is shifted in", 13, 650, anchor="start", cls="il-ink2"))
    cv.add(cv.rect(250, 474, 20, 14, 4, "none", stroke="#BA352D", sw=2.4, dash="4 3"), cv.text(278, 486, "a bit is lost off the end", 13, 650, anchor="start", cls="il-ink2"))
    cv.add(P.badge(cv, 36, 56, 1), P.badge(cv, 36, 202, 2), P.badge(cv, 36, 348, 3))
    return figure(
        "binary-shifts", cv, "Binary shifts: left multiplies by two, right divides, and a bit can be lost",
        "Three worked binary shifts on an eight bit number. First, shifting 0000 0110, which is 6, left by one place gives 0000 1100, which is "
        "12: every bit moves one column left, which doubles its value, and a new 0 fills the gap on the right. Second, shifting 0001 1000, which "
        "is 24, right by two places gives 0000 0110, which is 6: every bit moves two columns right, which divides the value by four, and two new "
        "0s fill the gaps on the left. Third, a warning: shifting 1100 0000, which is 192, left by one place pushes the leading 1 off the end of "
        "the register, so the result is 1000 0000, which is 128, not 384. A bit that is shifted off the end is lost.",
        ["A left shift moves every bit one column to the left, which doubles it. A 0 fills the gap on the right.",
         "A right shift moves bits to the right, which halves them each place. Shifting by 2 divides by 4.",
         "In a fixed number of bits a 1 can be pushed off the end and lost, which makes the answer wrong."],
        "Left shift by n multiplies by 2 to the power n; right shift divides. It only works while no 1 falls off the end.")


# ------------------------------------------------------------------ overflow

def wheel(cv, x, y, d, w=44, h=64):
    """One digit wheel of an odometer."""
    out = cv.rect(x, y, w, h, 8, cv.lin("whl", [(0, "#2A3E49"), (.5, "#46606D"), (1, "#2A3E49")]))
    out += cv.rect(x + 4, y + 4, w - 8, h - 8, 5, "#FBF8F0")
    out += cv.text(x + w / 2, y + h / 2 + 11, str(d), 32, 800, fill=INK, mono=True)
    return out


@illustration("binary-overflow")
def _overflow():
    cv = Canvas(800, 500).backdrop()
    cv.add(P.card(cv, 14, 34, 500, 290, 20, "255 + 1 in an 8 bit register", "teal"))
    cw, ch, pitch = 40, 38, 44
    cx0 = 84
    colx = lambda k: cx0 + pitch * k
    a, _, _ = bit_row(cv, colx(1), 84, "11111111", cw=cw, ch=ch, gap=4, nib=4, ones="sky")
    b, _, _ = bit_row(cv, colx(1), 134, "00000001", cw=cw, ch=ch, gap=4, nib=4, ones="sky")
    cv.add(a, b)
    cv.add(cv.text(48, 168, "+", 34, 800, cls="il-ink"))
    cv.add(cv.line(40, 190, 480, 190, ARROW, 3.5, op=.8))
    res, xs, _ = bit_row(cv, colx(1), 202, "00000000", cw=cw, ch=ch, gap=4, nib=4, ones="sky")
    cv.add(res)
    # the ninth bit
    cv.add(cv.rect(colx(0), 202, cw, ch, 8, "#FDE7E4", stroke="#BA352D", sw=2.6, dash="5 4"), cv.text(colx(0) + cw / 2, 202 + ch / 2 + 7, "1", 20, 800, fill="#8F2923", mono=True))
    cv.add(bracket(cv, colx(1) - 2, colx(8) + cw + 2, 262, PAL["teal"][2]))
    cv.add(cv.text((colx(1) + colx(8) + cw) / 2, 284, "what the register keeps: 0", 14.5, 750, cls="il-ink"))
    cv.add(P.arrow(cv, [(colx(0) + cw / 2, 246), (colx(0) + cw / 2, 276)], "#BA352D", 3.5, 10))
    cv.add(cv.text(colx(0) - 4, 304, "9th bit: no room", 13, 750, anchor="start", cls="il-bad"))
    # an odometer, the same thing in denary
    cv.add(P.card(cv, 14, 348, 500, 140, 20, "The same thing on an odometer", "sun"))
    for i in range(3):
        cv.add(wheel(cv, 44 + i * 50, 392, 9))
    cv.add(P.pill(cv, 234, 424, "+ 1", "paper", 18, 14, 34, 800))
    cv.add(P.arrow(cv, [(276, 424), (298, 424)], ARROW, 3.5, 10))
    for i in range(3):
        cv.add(wheel(cv, 308 + i * 50, 392, 0))
    cv.add(cv.text(484, 412, "1000", 15, 750, cls="il-bad", mono=True), cv.text(484, 434, "does", 13, 650, cls="il-ink2"), cv.text(484, 452, "not fit", 13, 650, cls="il-ink2"))
    # what goes wrong
    cv.add(P.card(cv, 530, 34, 256, 454, 20, "What goes wrong", "coral"))
    items = [("warn", "The answer is wrong", "255 + 1 shows as 0, not 256."),
             ("flag", "A flag is set", "The carry flag in the status register records it."),
             ("fix", "How to avoid it", "Use more bits, or check the flag.")]
    for i, (kind, head, body) in enumerate(items):
        y = 96 + i * 136
        if kind == "warn":
            cv.add(G.warning(cv, 566, y + 20, .95))
        elif kind == "flag":
            cv.add(G.flag(cv, 554, y, .9, "coral"))
        else:
            cv.add(P.tick(cv, 566, y + 20, 15))
        cv.add(cv.text(594, y + 14, head, 15.5, 750, anchor="start", cls="il-ink"))
        words = body.split(" ")
        lines, cur = [], ""
        for w_ in words:
            if len(cur) + len(w_) + 1 > 22 and cur:
                lines.append(cur)
                cur = w_
            else:
                cur = (cur + " " + w_).strip()
        lines.append(cur)
        for j, ln in enumerate(lines):
            cv.add(cv.text(594, y + 38 + j * 19, ln, 13.5, 650, anchor="start", cls="il-ink2"))
    cv.add(P.badge(cv, 36, 58, 1), P.badge(cv, 36, 372, 2), P.badge(cv, 546, 58, 3))
    return figure(
        "binary-overflow", cv, "Overflow: 255 plus 1 does not fit in eight bits",
        "What overflow is. Adding 1111 1111, which is 255, and 0000 0001 in an eight bit register gives 1 0000 0000, which is 256 and needs nine "
        "bits. The register only holds eight, so the ninth bit, the leading 1, has nowhere to go and is lost, and the register keeps 0000 0000, "
        "which is 0. The answer is wrong. An odometer does the same thing: 999 plus 1 turns all three wheels to 0 and the 1000 does not fit. "
        "When this happens the processor sets the carry flag in the status register. It can be avoided by using more bits, or by checking the flag.",
        ["Adding 1111 1111 and 0000 0001 produces a ninth bit. The register only keeps eight, so the answer shown is 0000 0000.",
         "An odometer is the same: 999 plus 1 gives 000 because the 1000 does not fit in three wheels.",
         "The answer is wrong, the carry flag is set to record it, and it is avoided with more bits or a check."],
        "Overflow happens when a result needs more bits than the register has. The largest 8 bit number is 255.")


# ------------------------------------------------------------------ run length encoding

BITMAP = ["............",
          ".....BB.....",
          "....BBBB....",
          "...BBBBBB...",
          "..BBBBBBBB..",
          "............"]


def runs(row):
    out, i = [], 0
    while i < len(row):
        j = i
        while j < len(row) and row[j] == row[i]:
            j += 1
        out.append((j - i, "B" if row[i] == "B" else "W"))
        i = j
    return out


def run_chip(cv, x, y, n, c, w=48, h=24):
    dark = c == "B"
    out = cv.rect(x, y, w, h, 7, INK if dark else "#FFFFFF", stroke="#9FB3BE", sw=1.8)
    out += cv.text(x + w / 2, y + h / 2 + 5, "%d%s" % (n, c), 14, 800, fill="#FFFFFF" if dark else INK, mono=True)
    return out


@illustration("rle-encoding")
def _rle():
    cv = Canvas(800, 500).backdrop()
    cv.add(P.card(cv, 14, 34, 772, 288, 20, "Run length encoding: store a run once, with its length", "teal"))
    cs, gx, gy = 26, 44, 78
    cv.add(cv.rect(gx - 5, gy - 5, 12 * cs + 10, 6 * cs + 10, 6, "#FFFFFF", stroke="#9FB3BE", sw=1.5))
    total_runs = 0
    for r, row in enumerate(BITMAP):
        for c, ch_ in enumerate(row):
            cv.add(cv.rect(gx + c * cs, gy + r * cs, cs, cs, 0, INK if ch_ == "B" else "#FFFFFF", stroke="#C9D5DC", sw=.8))
        rr = runs(row)
        total_runs += len(rr)
        for k, (n, c) in enumerate(rr):
            cv.add(run_chip(cv, 388 + k * 54, gy + r * cs + 1, n, c))
        cv.add(cv.text(372, gy + r * cs + 18, "›", 18, 800, cls="il-ink2"))
    cv.add(cv.text(gx + 6 * cs, gy + 6 * cs + 36, "the image: 12 × 6 = 72 pixels", 13.5, 700, cls="il-ink"))
    cv.add(cv.text(470, gy + 6 * cs + 36, "each row as runs", 13.5, 700, cls="il-ink"))
    # the saving
    cv.add(P.lift(cv, 600, 84, 160, 54, "sky", 12, 5, hl=False), cv.text(680, 84 + 27 + 9, "72 pixels", 22, 800, fill=INK, mono=True))
    cv.add(P.arrow(cv, [(680, 152), (680, 178)], ARROW, 4, 11))
    cv.add(P.lift(cv, 600, 186, 160, 54, "mint", 12, 5, hl=False), cv.text(680, 186 + 27 + 9, "%d runs" % total_runs, 22, 800, fill=INK, mono=True))
    cv.add(cv.text(680, 268, "much less to store", 13.5, 700, cls="il-ink"))
    # when it fails
    cv.add(P.card(cv, 14, 346, 772, 142, 20, "It fails when nothing repeats", "coral"))
    alt = "WBWBWBWB"
    cv.add(cv.rect(39, 387, 8 * 26 + 10, 36, 6, "#FFFFFF", stroke="#9FB3BE", sw=1.5))
    for i, c in enumerate(alt):
        cv.add(cv.rect(44 + i * 26, 392, 26, 26, 0, INK if c == "B" else "#FFFFFF", stroke="#C9D5DC", sw=.8))
    cv.add(cv.text(44 + 4 * 26, 444, "8 pixels", 13.5, 700, cls="il-ink"))
    cv.add(P.arrow(cv, [(270, 405), (306, 405)], ARROW, 4, 11))
    for k, c in enumerate(alt):
        cv.add(run_chip(cv, 318 + (k % 8) * 56, 392, 1, c, 50, 26))
    cv.add(cv.text(318 + 4 * 56 - 3, 444, "8 runs: no saving, and it can even grow", 13.5, 700, cls="il-bad"))
    cv.add(P.badge(cv, 36, 56, 1), P.badge(cv, 590, 82, 2), P.badge(cv, 36, 348, 3))
    return figure(
        "rle-encoding", cv, "Run length encoding a small black and white image, and when it does not help",
        "Run length encoding, RLE, stores a run of identical values once, with a count, instead of storing every value. A small black and white "
        "image, twelve pixels wide and six tall, is stored row by row. The first and last rows are all white, so each is just 12W. The middle "
        "rows are runs of white, then black, then white: 5W 2B 5W, then 4W 4B 4W, then 3W 6B 3W, then 2W 8B 2W. The 72 pixels become 14 runs, "
        "so there is much less to store. RLE is lossless, because the original can be rebuilt exactly. It only helps when values repeat. A row "
        "that alternates white, black, white, black becomes eight runs of 1, one for every pixel, so nothing is saved and the file can grow.",
        ["Count runs of the same colour along each row, and write the count then the colour.",
         "72 pixels become 14 runs. The saving is big because long runs repeat.",
         "If the values keep changing, every run is 1 long and RLE saves nothing, and may be larger."],
        "RLE is lossless and works best on images with large blocks of one colour, such as logos, icons and diagrams.")


# ------------------------------------------------------------------ Huffman coding

@illustration("huffman-tree")
def _huffman():
    cv = Canvas(800, 520).backdrop()
    letters = {"A": "sky", "B": "sun", "C": "mint", "D": "coral"}
    msg = "AAAAABBBCCD"
    cv.add(P.band(cv, 14, 24, 772, 72, 18))
    cv.add(cv.text(34, 66, "message", 13.5, 700, anchor="start", cls="il-ink2"))
    for i, c in enumerate(msg):
        cv.add(P.lift(cv, 110 + i * 44, 40, 38, 38, letters[c], 8, 4, hl=False), cv.text(110 + i * 44 + 19, 40 + 19 + 7, c, 20, 800, fill=INK, mono=True))
    cv.add(cv.text(612, 62, "11 characters", 15, 750, anchor="start", cls="il-ink"), cv.text(612, 82, "in ASCII: 88 bits", 14, 650, anchor="start", cls="il-ink2"))
    # counts
    cv.add(P.card(cv, 14, 118, 214, 226, 18, "1  Count", "teal"))
    for i, (c, n) in enumerate((("A", 5), ("B", 3), ("C", 2), ("D", 1))):
        y = 156 + i * 40
        cv.add(P.lift(cv, 34, y, 34, 32, letters[c], 8, 4, hl=False), cv.text(51, y + 16 + 7, c, 18, 800, fill=INK, mono=True))
        cv.add(cv.rect(78, y + 6, n * 22, 20, 6, cv.g(letters[c], "deep")))
        cv.add(cv.text(78 + n * 22 + 10, y + 22, str(n), 16, 800, anchor="start", cls="il-ink", mono=True))
    cv.add(cv.text(121, 336, "least common is joined first", 12.5, 650, cls="il-ink2"))
    # the tree
    cv.add(P.card(cv, 244, 118, 370, 330, 18, "2  Build the tree", "plum", tx=.4))
    nodes = {"R": (380, 176), "A": (306, 250), "N6": (452, 250), "B": (394, 322), "N3": (510, 322), "D": (470, 394), "C": (552, 394)}
    edges = [("R", "A", "0"), ("R", "N6", "1"), ("N6", "B", "0"), ("N6", "N3", "1"), ("N3", "D", "0"), ("N3", "C", "1")]
    for p, c, bit in edges:
        (x0, y0), (x1, y1) = nodes[p], nodes[c]
        cv.add(cv.line(x0, y0, x1, y1, ARROW, 3, op=.8))
        mx, my = (x0 + x1) / 2, (y0 + y1) / 2
        cv.add(cv.circle(mx, my, 11, "#FFFFFF", stroke=ARROW, sw=1.6), cv.text(mx, my + 5, bit, 14, 800, fill=INK, mono=True))
    for key, val in (("R", "11"), ("N6", "6"), ("N3", "3")):
        x, y = nodes[key]
        cv.add(cv.circle(x, y, 23, cv.g("deep", "deep"), stroke="#FFFFFF", sw=2.4), cv.text(x, y + 7, val, 20, 800, fill="#FFFFFF", mono=True))
    for key, c, n in (("A", "A", 5), ("B", "B", 3), ("D", "D", 1), ("C", "C", 2)):
        x, y = nodes[key]
        cv.add(P.lift(cv, x - 29, y - 20, 58, 40, letters[c], 10, 4, hl=False), cv.text(x, y + 6, "%s:%d" % (c, n), 17, 800, fill=INK, mono=True))
    # the codes
    cv.add(P.card(cv, 630, 118, 156, 330, 18, "3  Codes", "coral", tx=.5))
    codes = (("A", "0"), ("B", "10"), ("D", "110"), ("C", "111"))
    for i, (c, code) in enumerate(codes):
        y = 168 + i * 66
        cv.add(P.lift(cv, 646, y, 34, 32, letters[c], 8, 4, hl=False), cv.text(663, y + 16 + 7, c, 18, 800, fill=INK, mono=True))
        r, _, _ = bit_row(cv, 690, y + 1, code, cw=22, ch=30, gap=3, size=15, ones="teal")
        cv.add(r)
    cv.add(cv.text(708, 416, "common letters", 12.5, 650, cls="il-ink2"), cv.text(708, 433, "get short codes", 12.5, 650, cls="il-ink2"))
    # the saving
    cv.add(cv.text(34, 478, "ASCII", 14, 750, anchor="start", cls="il-ink"))
    cv.add(cv.rect(110, 462, 440, 22, 8, cv.g("slate")), cv.text(330, 478, "11 × 8 = 88 bits", 14.5, 800, fill=INK, mono=True))
    cv.add(cv.text(34, 506, "Huffman", 14, 750, anchor="start", cls="il-ink"))
    cv.add(cv.rect(110, 490, 100, 22, 8, cv.g("teal")), cv.text(160, 506, "20 bits", 14.5, 800, fill=INK, mono=True))
    cv.add(cv.text(224, 506, "5×1 + 3×2 + 2×3 + 1×3 = 20, about 77% smaller", 13, 700, anchor="start", cls="il-ink"))
    cv.add(P.badge(cv, 36, 140, 1), P.badge(cv, 266, 140, 2), P.badge(cv, 652, 140, 3))
    return figure(
        "huffman-tree", cv, "Huffman coding of the message AAAAABBBCCD: count, build the tree, read the codes",
        "Huffman coding compresses text by giving common characters short codes. The message AAAAABBBCCD has 11 characters, which would take 88 "
        "bits in ASCII. Count them first: A appears 5 times, B 3 times, C twice and D once. Build the tree by repeatedly joining the two "
        "smallest counts. D 1 and C 2 join to make a node worth 3. That node and B, 3, are now the two smallest, and join to make 6. Then 6 and A, "
        "5, join to make the root, 11. Label every left branch 0 and every right branch 1, and read the code for each letter from the root down. "
        "A is 0, B is 10, D is 110 and C is 111. The most common letter has the shortest code. The message now needs 5 times 1, plus 3 times 2, "
        "plus 2 times 3, plus 1 times 3, which is 20 bits, about 77 percent smaller than 88. Huffman coding is lossless.",
        ["Count how often each character appears.",
         "Join the two smallest counts into a new node, and repeat until one node, the root, is left. Label branches 0 and 1.",
         "Read each code from the root down to its letter. Frequent letters get the shortest codes.",
         ],
        "Common characters get short codes and rare ones get long codes, so the total is smaller. No code is the start of another.")


# ------------------------------------------------------------------ image metadata

@illustration("image-metadata")
def _meta():
    cv = Canvas(800, 500).backdrop()
    # the picture
    cv.add(cv.shadow(200, 300, 150, 9, .2))
    cv.add(P.photo(cv, 54, 70, 292, 220, 10))
    cv.add(cv.text(200, 326, "IMG_0412.jpg", 15, 750, cls="il-ink", mono=True))
    cv.add(cv.text(200, 352, "the pixels you see", 13.5, 650, cls="il-ink2"))
    # the tag
    cv.add(P.arrow(cv, [(352, 190), (412, 190)], PAL["deep"][1], 5, 14))
    cv.add(P.card(cv, 420, 40, 366, 372, 20, "Metadata: data about the data", "teal", tx=.5))
    needed = [("Width", "4032 px"), ("Height", "3024 px"), ("Colour depth", "24 bits"), ("File type", "JPEG")]
    extra = [("Date taken", "14 Jun 2026 09:41"), ("Device", "smartphone"), ("Location", "51.50 N, 0.12 W"), ("Resolution", "300 ppi")]
    cv.add(cv.rect(436, 74, 334, 26, 8, "var(--il-band)"), cv.text(452, 92, "needed to show the picture", 13.5, 750, anchor="start", cls="il-ink"))
    for i, (k, v) in enumerate(needed):
        y = 118 + i * 36
        cv.add(P.tick(cv, 452, y + 8, 9), cv.text(474, y + 13, k, 14.5, 650, anchor="start", cls="il-ink2"), cv.text(762, y + 13, v, 14.5, 800, anchor="end", cls="il-ink", mono=True))
    cv.add(cv.rect(436, 268 - 8, 334, 26, 8, "var(--il-band)"), cv.text(452, 270 + 10, "extra information", 13.5, 750, anchor="start", cls="il-ink"))
    for i, (k, v) in enumerate(extra):
        y = 288 + i * 30
        cv.add(cv.circle(452, y + 8, 6, cv.g("sun", "deep")), cv.text(474, y + 13, k, 14.5, 650, anchor="start", cls="il-ink2"), cv.text(762, y + 13, v, 14.5, 800, anchor="end", cls="il-ink", mono=True))
    # the formula and the warning
    cv.add(P.card(cv, 14, 436, 772, 54, 16))
    cv.add(cv.text(34, 469, "File size = width × height × colour depth, plus a little for the metadata.", 14.5, 700, anchor="start", cls="il-ink"))
    cv.add(P.badge(cv, 36, 74, 1), P.badge(cv, 438, 42, 2), P.badge(cv, 424, 270, 3))
    return figure(
        "image-metadata", cv, "A photograph and the metadata stored with it",
        "An image file holds more than the pixels. Metadata is data about the data: it is stored in the file but it is not part of the picture. "
        "Some metadata is needed to rebuild and show the image: the width and height in pixels, here 4032 by 3024, the colour depth, here 24 "
        "bits, and the file type, here JPEG. Other metadata is extra information: the date and time the photo was taken, the device, the "
        "resolution in pixels per inch, and the GPS location, here 51.50 north, 0.12 west. Without the width, height and colour depth the "
        "computer would not know how to turn the stream of bits back into a grid of pixels. The extra information can be a privacy risk, "
        "because a photo shared online can reveal where it was taken.",
        ["The picture is a grid of pixels, stored as one long stream of bits.",
         "Metadata that must be stored: width, height and colour depth. Without them the bits cannot be turned back into the picture.",
         "Extra metadata such as date, device and GPS location is useful, but sharing it can be a privacy risk."],
        "Metadata is data about the data. It is not part of the picture, but the file would not open properly without the key parts.")
