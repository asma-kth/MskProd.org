"""Hardware illustrations: the processor, memory, storage and the units that measure them."""
import math

from .illus import Canvas, PAL, INK, ARROW, figure, illustration, _n
from . import illus_props as P


def pins(cv, x, y, w, h, n=12, side=8, color="gold"):
    """Gold pins along all four edges of a package. (x, y, w, h) is the package body."""
    out = ""
    for i in range(n):
        px = x + 14 + i * (w - 28) / (n - 1) - 3
        out += cv.rect(px, y - side, 6, side + 3, 1.5, cv.g(color)) + cv.rect(px, y + h - 3, 6, side + 3, 1.5, cv.g(color))
    m = max(3, int(h / (w / n)))
    for i in range(m):
        py = y + 14 + i * (h - 28) / (m - 1) - 3
        out += cv.rect(x - side, py, side + 3, 6, 1.5, cv.g(color)) + cv.rect(x + w - 3, py, side + 3, 6, 1.5, cv.g(color))
    return out


def reg(cv, x, y, w, h, name, sub, color, value=None):
    """A register or unit inside the die."""
    out = P.lift(cv, x, y, w, h, color, 10, 4)
    tc = P._on(color)
    out += cv.text(x + w / 2, y + 20, name, 17, 800, fill=tc)
    out += cv.text(x + w / 2, y + 36, sub, 11.5, 600, fill=tc, op=.9)
    if value:
        out += cv.rect(x + w / 2 - 34, y + h - 21, 68, 17, 8.5, "#FFFFFF", op=.92)
        out += cv.text(x + w / 2, y + h - 8.2, value, 12, 800, fill=INK, mono=True)
    return out


@illustration("cpu-board")
def _cpu_board():
    cv = Canvas(800, 500).backdrop()
    bx, by, bw, bh = 34, 34, 396, 432
    cv.add(cv.shadow(bx + bw / 2, by + bh + 14, 200, 10, .25))
    cv.add(pins(cv, bx, by, bw, bh, 13))
    cv.add(cv.rect(bx, by, bw, bh, 22, cv.g("dark", "deep")), cv.rect(bx + 3, by + 3, bw - 6, 40, 20, "#fff", op=.08))
    cv.add(cv.rect(bx + 18, by + 18, bw - 36, bh - 36, 14, cv.lin("die", [(0, "#2C4350"), (1, "#1D303B")])))
    cv.add(cv.poly([(bx + 6, by + 6), (bx + 24, by + 6), (bx + 6, by + 24)], "#FFCC4A"))
    cv.add(cv.text(bx + bw / 2, by + 44, "CENTRAL PROCESSING UNIT", 12.5, 800, fill="#8FB1BF", spacing=2))
    # the units on the die
    L, R, M = bx + 36, bx + bw - 36 - 104, bx + 36 + 108
    pc = (L, 96, 108, 62)
    mar = (R, 96, 104, 62)
    cir = (L, 186, 108, 62)
    mdr = (R, 186, 104, 62)
    cu = (L, 278, 108, 92)
    alu = (L + 126, 278, bw - 72 - 126, 92)
    cv.add(reg(cv, *pc, "PC", "program counter", "sun", "0x04A"))
    cv.add(reg(cv, *mar, "MAR", "memory address", "sky", "0x04A"))
    cv.add(reg(cv, *cir, "CIR", "current instruction", "lilac", "LDA 7"))
    cv.add(reg(cv, *mdr, "MDR", "memory data", "mint", "LDA 7"))
    cv.add(reg(cv, *cu, "CU", "control unit", "coral"))
    cv.add(cv.text(cu[0] + 54, cu[1] + 64, "decodes", 12.5, 700, fill=P._on("coral")))
    cv.add(reg(cv, *alu, "ALU", "arithmetic logic unit", "teal"))
    cv.add(cv.text(alu[0] + alu[2] / 2, alu[1] + 66, "adds, compares, ANDs", 12.5, 700, fill=P._on("teal")))
    w = "#FFFFFF"
    cv.add(P.arrow(cv, [(pc[0] + pc[2] + 6, 127), (mar[0] - 8, 127)], "#FFCC4A", 5, 13))
    cv.add(P.arrow(cv, [(mdr[0] - 6, 217), (cir[0] + cir[2] + 8, 217)], "#7ED6B0", 5, 13))
    cv.add(P.arrow(cv, [(cir[0] + 54, cir[1] + 66), (cir[0] + 54, cu[1] - 4)], "#C9A9E6", 5, 13))
    cv.add(P.arrow(cv, [(cu[0] + cu[2] + 6, 324), (alu[0] - 8, 324)], "#FF9C90", 5, 13))
    # the buses out to memory
    ex = bx + bw + 8
    rx = 566
    cv.add(P.cable(cv, "M%d 127 L%d 127" % (mar[0] + mar[2], rx), "sky", 8))
    cv.add(P.arrow(cv, [(ex + 40, 127), (rx - 4, 127)], PAL["sky"][1], 6, 14))
    cv.add(P.cable(cv, "M%d 217 L%d 217" % (mdr[0] + mdr[2], rx), "mint", 8))
    cv.add(P.arrow(cv, [(ex + 40, 217), (rx - 4, 217)], PAL["mint"][1], 6, 14))
    cv.add(P.arrow(cv, [(rx - 40, 217), (ex + 4, 217)], PAL["mint"][1], 6, 14))
    cv.add(P.cable(cv, "M%d 370 L%d 400 L%d 400 L%d 400" % (cu[0] + 54, cu[0] + 54, bx + bw, rx), "coral", 8))
    cv.add(P.arrow(cv, [(ex + 40, 400), (rx - 4, 400)], PAL["coral"][1], 6, 14))
    for yy, t, col in ((100, "address bus", "sky"), (192, "data bus", "mint"), (374, "control bus", "coral")):
        cv.add(P.pill(cv, (bx + bw + rx) / 2 + 6, yy - 8 if yy != 374 else yy, t, col, 13.5, 8, 24, 700))
    # main memory
    cv.add(P.card(cv, rx, 56, 218, 256, 16))
    cv.add(cv.text(rx + 109, 86, "Main memory (RAM)", 15, 750, cls="il-ink il-h"))
    for i, (addr, val) in enumerate((("0x049", "ADD 3"), ("0x04A", "LDA 7"), ("0x04B", "STA 9"), ("0x04C", "JMP 2"))):
        yy = 100 + i * 50
        hot = addr == "0x04A"
        cv.add(cv.rect(rx + 12, yy, 64, 40, 8, cv.g("sky") if hot else "#E6EEF2"), cv.text(rx + 44, yy + 25, addr, 12.5, 800, fill=INK, mono=True))
        cv.add(cv.rect(rx + 80, yy, 126, 40, 8, cv.g("mint") if hot else "#FFFFFF", stroke="var(--il-line)", sw=1), cv.text(rx + 143, yy + 25.5, val, 14, 800, fill=INK, mono=True))
    cv.add(P.ram_stick(cv, rx + 4, 340, 210, 56, 1, 5))
    cv.add(cv.text(rx + 109, 432, "a real memory module", 12.5, 600, cls="il-ink2"))
    cv.add(P.badge(cv, 70, 76, 1), P.badge(cv, 500, 150, 2), P.badge(cv, 500, 246, 3), P.badge(cv, 70, 372, 4), P.badge(cv, 250, 376, 5))
    return figure(
        "cpu-board", cv, "The fetch decode execute cycle inside the processor",
        "The processor on the left, with main memory on the right, joined by three buses. Inside the processor are the program counter, "
        "the memory address register, the memory data register, the current instruction register, the control unit and the arithmetic logic "
        "unit. The cycle runs like this. The program counter holds the address of the next instruction, here 0x04A. That address is copied "
        "into the memory address register and sent to memory along the address bus, which is one way. Memory sends the contents of that "
        "address, here the instruction LDA 7, back along the data bus into the memory data register, and it is copied to the current "
        "instruction register. The control unit decodes the instruction and works out what has to happen, sending signals along the control "
        "bus when memory is involved. The arithmetic logic unit carries it out, and the program counter moves on by one.",
        ["The program counter holds the address of the next instruction.",
         "That address goes to memory along the address bus.",
         "The instruction comes back along the data bus and lands in the MDR.",
         "The control unit decodes it and works out what has to happen.",
         "The ALU executes it, and the program counter moves on by one."],
        "Address out, data back, control alongside. The address bus is one way: memory never sends an address to the CPU.")


def gauge(cv, cx, cy, r=88, value=.72):
    """A speedometer dial. (cx, cy) is the hub; the dial is a half circle above it."""
    out = cv.path("M%s %s A%s %s 0 0 1 %s %s" % (_n(cx - r), _n(cy), _n(r), _n(r), _n(cx + r), _n(cy)), stroke="#DDE6EC", sw=22, cap="butt")
    segs = [("teal", 0, .34), ("sun", .34, .67), ("coral", .67, 1)]
    for col, a, b in segs:
        a0, a1 = math.pi * (1 - a), math.pi * (1 - b)
        x0, y0 = cx + r * math.cos(a0), cy - r * math.sin(a0)
        x1, y1 = cx + r * math.cos(a1), cy - r * math.sin(a1)
        out += cv.path("M%s %s A%s %s 0 0 1 %s %s" % (_n(x0), _n(y0), _n(r), _n(r), _n(x1), _n(y1)), stroke=PAL[col][1], sw=22, cap="butt")
    for k in range(0, 11):
        a = math.pi * (1 - k / 10)
        out += cv.line(cx + (r - 17) * math.cos(a), cy - (r - 17) * math.sin(a), cx + (r - 26) * math.cos(a), cy - (r - 26) * math.sin(a), INK, 2.4, op=.55)
    a = math.pi * (1 - value)
    nx, ny = cx + (r - 14) * math.cos(a), cy - (r - 14) * math.sin(a)
    out += cv.path("M%s %s L%s %s" % (_n(cx), _n(cy), _n(nx), _n(ny)), stroke="#26363F", sw=7)
    out += cv.circle(cx, cy, 13, cv.g("dark", "deep")) + cv.circle(cx, cy, 5, "#9FB2BD")
    return out


@illustration("cpu-performance")
def _cpu_performance():
    cv = Canvas(800, 500).backdrop()
    heads = [("Clock speed", "teal"), ("Cores", "plum"), ("Cache", "coral")]
    for i, (t, c) in enumerate(heads):
        cv.add(P.card(cv, 14 + i * 262, 34, 250, 330, 20, t, c))
    # clock
    cv.add(gauge(cv, 139, 200, 84, .74))
    cv.add(cv.text(139, 254, "3.6 GHz", 28, 800, cls="il-ink il-h"))
    cv.add(cv.text(139, 280, "3,600,000,000 cycles", 14, 600, cls="il-ink2"))
    cv.add(cv.text(139, 298, "every second", 14, 600, cls="il-ink2"))
    cv.add(P.pill(cv, 139, 336, "more cycles = more done", "paper", 13.5))
    # cores
    cx = 401
    cv.add(P.cpu_chip(cv, cx - 62, 98, 124, "", 1, "dark", 8))
    for k, col in enumerate(("sky", "mint", "sun", "coral")):
        gx, gy = cx - 40 + (k % 2) * 42, 118 + (k // 2) * 42
        cv.add(P.lift(cv, gx, gy, 38, 38, col, 7, 3, hl=False), cv.text(gx + 19, gy + 25, str(k + 1), 17, 800, fill=P._on(col)))
    cv.add(cv.text(cx, 270, "4 cores", 26, 800, cls="il-ink il-h"))
    cv.add(cv.text(cx, 296, "4 jobs at the same moment", 14, 600, cls="il-ink2"))
    cv.add(P.pill(cv, cx, 336, "if the work can be split", "paper", 13.5))
    # cache
    cx = 663
    cv.add(P.cpu_chip(cv, 548, 106, 66, "", 1, "dark", 6))
    cv.add(P.lift(cv, 560, 118, 42, 42, "coral", 8, 3, hl=False), cv.text(581, 146, "L1", 15, 800, fill=P._on("coral")))
    cv.add(P.arrow(cv, [(626, 140), (652, 140)], PAL["green"][1], 6, 12))
    cv.add(P.ram_stick(cv, 656, 118, 100, 46, 1, 3))
    cv.add(P.pill(cv, 581, 196, "cache: ~1 ns", "green", 13.5, 10, 26, 750))
    cv.add(P.pill(cv, 706, 196, "RAM: ~100 ns", "coral", 13.5, 10, 26, 750))
    cv.add(cv.text(cx, 270, "Cache", 26, 800, cls="il-ink il-h"))
    cv.add(cv.text(cx, 296, "memory on the chip itself", 14, 600, cls="il-ink2"))
    cv.add(P.pill(cv, cx, 336, "waits for RAM less often", "paper", 13.5))
    # the warning
    cv.add(cv.rect(14, 388, 772, 92, 20, "var(--il-card)", stroke="var(--il-line)", sw=1.5))
    cv.add(cv.poly([(56, 410), (86, 462), (26, 462)], cv.g("sun")), cv.text(56, 454, "!", 28, 900, fill=INK))
    cv.add(cv.text(112, 428, "A bigger number is not automatically a faster computer.", 17.5, 750, anchor="start", cls="il-ink il-h"))
    cv.add(cv.text(112, 454, "Cores that cannot be kept busy, or a slow memory, hold the whole machine back.", 14.5, 500, anchor="start", cls="il-ink2"))
    cv.add(P.badge(cv, 60, 34, 1), P.badge(cv, 322, 34, 2), P.badge(cv, 584, 34, 3), P.badge(cv, 770, 392, 4))
    return figure(
        "cpu-performance", cv, "What decides how fast a processor is: clock speed, cores and cache",
        "The three things that decide how fast a processor is. Clock speed is how many cycles it runs each second, measured in gigahertz, and "
        "3.6 GHz means three thousand six hundred million cycles a second; each cycle can carry out part of an instruction, so more cycles "
        "means more work done, as long as nothing else is holding it up. The number of cores is how many instructions it can genuinely "
        "process at the same time, since each core is a complete processor; four cores can work on four jobs at once, but only if the work "
        "can be split up. Cache is a small amount of very fast memory on the processor chip, about a nanosecond away, where the processor "
        "keeps what it is likely to need next, so it waits for main memory, about a hundred nanoseconds away, less often. A bigger number "
        "on one of these is not automatically a faster computer, because the other two, and the software, can hold it back.",
        ["Clock speed: how many cycles the processor runs each second.",
         "Cores: how many instructions it can genuinely work on at once.",
         "Cache: fast memory on the chip, so it waits for RAM less often.",
         "A bigger number is not automatically a faster computer."],
        "Exam answers that just say ‘higher clock speed is faster’ get one mark. Saying what it does, and what limits it, gets the rest.")


@illustration("memory-hierarchy")
def _memory_hierarchy():
    cv = Canvas(800, 500).backdrop()
    apex, base_y, top_y = (230, 40), 430, 40
    half = 200

    def xl(y):
        return apex[0] - (y - top_y) / (base_y - top_y) * half

    def xr(y):
        return apex[0] + (y - top_y) / (base_y - top_y) * half
    tiers = [
        (40, 126, "sun", "Registers", "inside the CPU", "a few hundred bytes", "fastest of all"),
        (132, 220, "coral", "Cache", "on the CPU chip", "a few megabytes", "nanoseconds"),
        (226, 322, "sky", "Main memory", "RAM", "8 to 32 gigabytes", "fast, but volatile"),
        (328, 430, "plum", "Secondary storage", "SSD or hard disk", "terabytes", "slow, but permanent"),
    ]
    cv.add(cv.shadow(apex[0], 442, 210, 10, .22))
    for i, (y0, y1, col, name, where, size, speed) in enumerate(tiers):
        pts = [(xl(y0), y0), (xr(y0), y0), (xr(y1), y1), (xl(y1), y1)]
        cv.add(cv.poly([(x, y + 6) for x, y in pts], PAL[col][2]))
        cv.add(cv.poly(pts, cv.g(col)))
        cv.add(cv.poly([(xl(y0) + 4, y0 + 3), (xr(y0) - 4, y0 + 3), (xr(y0 + (y1 - y0) * .35) - 3, y0 + (y1 - y0) * .35), (xl(y0 + (y1 - y0) * .35) + 3, y0 + (y1 - y0) * .35)], "#fff", op=.2))
        mid = (y0 + y1) / 2
        # the part of the machine this tier is
        if i == 0:
            for a in range(3):
                for b in range(2):
                    cv.add(cv.rect(apex[0] - 22 + a * 15, y0 + 44 + b * 14, 12, 10, 2.5, "#fff", op=.85))
        elif i == 1:
            cv.add(P.chip_small(cv, apex[0] - 28, y0 + 38, 56, "dark", "L1"))
        elif i == 2:
            cv.add(P.ram_stick(cv, apex[0] - 70, y0 + 46, 140, 36, 1, 4))
        else:
            cv.add(P.ssd(cv, apex[0] - 56, y0 + 40, 230, .49, label=False), P.hdd(cv, apex[0] + 58, y0 + 38, 70, 1))
        # the card to the right
        cy = mid + 6
        cv.add(cv.line(xr(mid) + 4, mid + 4, 470, cy, ARROW, 2, op=.35, dash="3 5"))
        cv.add(P.lift(cv, 476, cy - 36, 312, 74, col, 14, 5, hl=False))
        cv.add(cv.rect(484, cy - 28, 8, 58, 4, "#fff", op=.55))
        tc = P._on(col)
        cv.add(cv.text(504, cy - 8, name, 19, 800, fill=tc, anchor="start"))
        cv.add(cv.text(504, cy + 12, where + "  ·  " + size, 13.5, 600, fill=tc, anchor="start"))
        cv.add(cv.text(504, cy + 29, speed, 13.5, 700, fill=tc, anchor="start"))
    cv.add(P.pill(cv, 120, 32, "smaller, faster, dearer", "paper", 13.5, 10, 26, 700))
    cv.add(P.pill(cv, 150, 470, "bigger, slower, cheaper per byte", "paper", 13.5, 10, 26, 700))
    cv.add(P.badge(cv, 330, 70, 1), P.badge(cv, 330, 160, 2), P.badge(cv, 330, 258, 3), P.badge(cv, 330, 356, 4), P.badge(cv, 28, 32, 5))
    return figure(
        "memory-hierarchy", cv, "The memory hierarchy: small and fast at the top, huge and slow at the bottom",
        "The memory hierarchy drawn as a pyramid of four tiers, narrow at the top and wide at the bottom. Registers sit inside the processor "
        "itself, hold a few hundred bytes and are the fastest storage in the machine. Cache sits on the processor chip, holds a few "
        "megabytes and answers in nanoseconds, which is why a cache hit saves so much time. Main memory, the RAM, holds eight to thirty two "
        "gigabytes, is fast but volatile, so everything in it is lost when the power goes off. Secondary storage, an SSD or a hard disk, holds "
        "terabytes and keeps your files permanently, but is far slower. Every step down is bigger, slower and cheaper per byte. If one kind "
        "of memory were fast, huge and cheap there would only be one kind.",
        ["Registers: inside the CPU, a few hundred bytes, fastest of all.",
         "Cache: still on the chip, a few megabytes, and very fast.",
         "Main memory: gigabytes, fast, and it empties when the power goes.",
         "Secondary storage: terabytes, slow, and it keeps your files forever.",
         "The whole point: small and fast at the top, huge and slow at the bottom."],
        "Every level down is bigger, slower and cheaper per byte. If one kind of memory were fast, huge and cheap, there would only be one kind.")


@illustration("secondary-storage")
def _secondary_storage():
    cv = Canvas(800, 500).backdrop()
    heads = [("Magnetic", "teal"), ("Solid state", "plum"), ("Optical", "coral")]
    for i, (t, c) in enumerate(heads):
        cv.add(P.card(cv, 14 + i * 262, 34, 250, 372, 20, t, c))
    # the three devices
    cv.add(P.hdd(cv, 34, 86, 210))
    cv.add(P.pill(cv, 62, 100, "platters", "paper", 12.5, 8, 22, 700), P.pill(cv, 212, 214, "read-write head", "paper", 12.5, 8, 22, 700))
    cv.add(P.ssd(cv, 304, 96, 214))
    cv.add(P.pill(cv, 410, 78 + 38, "flash memory chips", "paper", 12.5, 8, 22, 700))
    cv.add(P.disc(cv, 663, 160, 72))
    cv.add(P.pill(cv, 663, 252, "a laser reads the pits", "paper", 12.5, 8, 22, 700))
    notes = [
        [("ok", "Cheapest per gigabyte"), ("ok", "Huge capacity"), ("bad", "Moving parts, slow")],
        [("ok", "No moving parts"), ("ok", "Fast, quiet, tough"), ("bad", "Dearer per gigabyte")],
        [("ok", "Cheap and portable"), ("bad", "Small capacity"), ("bad", "Scratches easily")],
    ]
    for i, lst in enumerate(notes):
        for j, (kind, txt) in enumerate(lst):
            x0, y0 = 38 + i * 262, 298 + j * 34
            cv.add(P.tick(cv, x0 + 11, y0 + 10, 11) if kind == "ok" else P.cross(cv, x0 + 11, y0 + 10, 11))
            cv.add(cv.text(x0 + 30, y0 + 16, txt, 15, 600, anchor="start"))
    cv.add(cv.rect(14, 424, 772, 58, 18, "var(--il-card)", stroke="var(--il-line)", sw=1.5))
    cv.add(cv.text(46, 459, "Choose by:", 16, 800, anchor="start", cls="il-ink il-h"))
    x = 150
    for (t, c) in (("capacity", "sky"), ("speed", "sun"), ("durability", "mint"), ("cost per gigabyte", "coral")):
        w = len(t) * 14.5 * .58 + 24
        cv.add(P.pill(cv, x + w / 2, 453, t, c, 14.5, 12, 30, 700))
        x += w + 14
    cv.add(P.badge(cv, 54, 34, 1), P.badge(cv, 316, 34, 2), P.badge(cv, 578, 34, 3), P.badge(cv, 770, 428, 4))
    return figure(
        "secondary-storage", cv, "Three kinds of secondary storage: magnetic, solid state and optical",
        "The three kinds of secondary storage, as the three different physical things they are. A magnetic hard disk drive is a stack of "
        "spinning platters coated in magnetic material, with a read write head floating just above the surface and moving in and out to "
        "reach different tracks. It is the cheapest per gigabyte and comes in the largest capacities, but it is slow, noisy, uses more power, "
        "and because it has moving parts it is damaged by knocks. A solid state drive is a circuit board of flash memory chips with no "
        "moving parts, so it is fast, silent and tough, but costs more per gigabyte. An optical disc has one spiral track of tiny pits and "
        "flat lands that a laser reads: it is cheap and portable but holds little and scratches easily. Which one to choose depends on "
        "capacity, speed, durability and cost per gigabyte.",
        ["Magnetic: spinning platters with a head floating over the surface.",
         "Solid state: a grid of cells holding charge, with no moving parts.",
         "Optical: one spiral track of pits and lands, read by a laser.",
         "Which one depends on capacity, speed, durability and cost per gigabyte."],
        "Exam answers need the reason, not the name: no moving parts is why an SSD survives being dropped and starts up faster.")


def app_icon(cv, x, y, color, kind, s=44):
    """A small app tile: a rounded square with a simple symbol on it."""
    out = P.lift(cv, x, y, s, s, color, 11, 4)
    cx, cy = x + s / 2, y + s / 2 - 1
    if kind == "web":
        out += cv.circle(cx, cy, s * .27, "none", stroke="#fff", sw=2.6) + cv.ellipse(cx, cy, s * .11, s * .27, "none", stroke="#fff", sw=2) + cv.line(cx - s * .27, cy, cx + s * .27, cy, "#fff", 2)
    elif kind == "play":
        out += cv.poly([(cx - s * .12, cy - s * .2), (cx - s * .12, cy + s * .2), (cx + s * .22, cy)], "#fff")
    elif kind == "sheet":
        out += cv.rect(cx - s * .26, cy - s * .24, s * .52, s * .48, 3, "none", stroke="#fff", sw=2.4)
        out += cv.line(cx - s * .26, cy, cx + s * .26, cy, "#fff", 2.2) + cv.line(cx, cy - s * .24, cx, cy + s * .24, "#fff", 2.2)
    else:
        out += cv.line(cx - s * .22, cy - s * .12, cx + s * .22, cy - s * .12, "#fff", 3) + cv.line(cx - s * .22, cy + s * .02, cx + s * .22, cy + s * .02, "#fff", 3) + cv.line(cx - s * .22, cy + s * .16, cx + s * .06, cy + s * .16, "#fff", 3)
    return out


def microwave(cv, x, y, s=1.0):
    """A microwave oven, seen from the front. Canonical 270 x 170."""
    body = cv.shadow(135, 176, 140, 8)
    body += cv.rect(0, 0, 270, 168, 16, cv.g("metal")) + cv.rect(0, 0, 270, 168, 16, "none", stroke=PAL["metal"][2], sw=2, op=.6)
    body += cv.rect(14, 14, 172, 136, 10, cv.g("dark", "deep"))
    body += cv.rect(22, 22, 156, 120, 6, cv.lin("mwglass", [(0, "#35505E"), (1, "#1B2C36")]))
    body += cv.circle(100, 118, 30, "#E9F2F6", op=.9) + cv.ellipse(100, 112, 30, 8, "#fff", op=.8)
    body += cv.circle(100, 44, 38, cv.rad("mwlight", [(0, "#FFE27A", .55), (1, "#FFE27A", 0)]))
    body += cv.rect(26, 26, 40, 10, 5, "#fff", op=.18)
    body += cv.rect(198, 18, 58, 26, 5, "#10202A") + cv.text(227, 38, "0:30", 17, 800, fill="#7CF0B0", mono=True)
    for i in range(3):
        for j in range(3):
            body += cv.rect(200 + j * 20, 56 + i * 20, 16, 14, 4, cv.g("slate", "deep"))
    body += cv.circle(228, 138, 11, cv.g("slate", "deep")) + cv.line(228, 138, 234, 131, INK, 2.5)
    return cv.group(body, x, y, s)


@illustration("embedded-systems")
def _embedded():
    cv = Canvas(800, 500).backdrop()
    cv.add(P.card(cv, 14, 40, 380, 440, 20, "General purpose", "teal"))
    cv.add(P.card(cv, 406, 40, 380, 440, 20, "Embedded", "plum"))
    # a laptop with everything it has
    cv.add(P.laptop(cv, 76, 118, 1.16, P.browser_screen(cv, 31, 9, 158, 102, "any.app", True)))
    for (x, y, t, c) in ((40, 92, "CPU", "dark"), (302, 92, "RAM", "pcb"), (30, 212, "GPU", "plum"), (310, 212, "SSD", "sky"), (170, 304, "full operating system", "coral")):
        cv.add(P.pill(cv, x + 34, y + 12, t, c, 14.5, 10, 28, 750) if t != "full operating system" else P.pill(cv, 204, 306, t, c, 14.5, 12, 28, 750))
    for i, (c, k) in enumerate((("coral", "web"), ("teal", "play"), ("plum", "sheet"), ("sun", "doc"))):
        cv.add(app_icon(cv, 60 + i * 76, 346, c, k, 48))
    cv.add(P.tick(cv, 316, 372, 14))
    cv.add(cv.text(204, 434, "runs whatever you install", 16, 700, cls="il-ink"))
    # the embedded one
    cv.add(microwave(cv, 436, 110, 1.0))
    cv.add(cv.circle(706, 240, 70, "#FFFFFF", op=.9), cv.circle(706, 240, 70, "none", stroke=PAL["plum"][1], sw=3, dash="7 6"))
    cv.add(cv.line(657, 191, 560, 140, PAL["plum"][1], 3, op=.9, dash="6 6"))
    cv.add(cv.rect(656, 198, 100, 86, 10, cv.g("pcb")))
    for yy in (210, 228, 246, 264):
        cv.add(cv.line(660, yy, 672, yy, "#E9F7EF", 2, op=.55), cv.line(740, yy, 752, yy, "#E9F7EF", 2, op=.55))
    cv.add(P.chip_small(cv, 676, 204, 58, "dark", "MCU"), P.chip_small(cv, 704, 252, 44, "navy", "ROM"))
    cv.add(P.pill(cv, 706, 328, "one small board", "paper", 13, 10, 26, 700))
    dim = "".join(app_icon(cv, 452 + i * 76, 346, c, k, 48) for i, (c, k) in enumerate((("coral", "web"), ("teal", "play"), ("plum", "sheet"), ("sun", "doc"))))
    cv.add(cv.group(dim, 0, 0, 1, extra=' opacity=".32"'))
    cv.add(P.cross(cv, 722, 372, 14))
    cv.add(cv.text(596, 434, "one program, fixed in ROM", 16, 700, cls="il-ink"))
    cv.add(cv.text(204, 458, "flexible, but dear and complicated", 13.5, 600, cls="il-ink2"))
    cv.add(cv.text(596, 458, "pennies, instant start, rarely crashes", 13.5, 600, cls="il-ink2"))
    cv.add(P.badge(cv, 60, 40, 1), P.badge(cv, 450, 40, 2), P.badge(cv, 650, 168, 3), P.badge(cv, 770, 458, 4))
    return figure(
        "embedded-systems", cv, "A general purpose computer compared with an embedded system",
        "A general purpose computer against an embedded system. The general purpose machine, drawn as a laptop, has a processor, main memory, "
        "a graphics processor and secondary storage, runs a full operating system, and will run whatever software you choose to install on "
        "it, which is exactly what makes it flexible, expensive and complicated. An embedded system, drawn as a microwave oven with a small "
        "board inside it, is a single small circuit board built into the device it controls, often one chip carrying the processor, memory "
        "and inputs and outputs together. It runs one program, written once and stored in ROM, and it is never replaced or added to, which is "
        "why it starts instantly, costs pennies and almost never crashes. You cannot install new software on it.",
        ["A general purpose computer: many parts, and it runs whatever you install.",
         "An embedded system: one small board, built into the device it controls.",
         "It runs one program, written once, stored in ROM, never replaced.",
         "That is why it boots instantly, costs pennies and almost never crashes."],
        "Ask whether the user can install new software on it. If not, it is almost certainly embedded.")


def hourglass(cv, cx, cy, s=1.0):
    out = cv.path("M-9 -13 L9 -13 L9 -10 Q9 -3 2 0 Q9 3 9 10 L9 13 L-9 13 L-9 10 Q-9 3 -2 0 Q-9 -3 -9 -10 Z", fill="#F4F8FA", stroke=PAL["dark"][1], sw=2)
    out += cv.path("M-5 11 L5 11 L2 5 L-2 5 Z", fill="#FFCC4A") + cv.path("M-6 -11 L6 -11 L3 -6 L-3 -6 Z", fill="#FFCC4A")
    return cv.group(out, cx, cy, s)


@illustration("parallel-cores")
def _parallel():
    cv = Canvas(800, 500).backdrop()
    cols = ["sky", "mint", "sun", "coral"]
    X0, W, JW = 104, 436, 100

    def lane(y, n, h=34):
        o = cv.rect(X0, y, W, h, 9, "var(--il-card)", stroke="var(--il-line)", sw=1.2)
        o += P.lift(cv, 20, y, 76, h, "dark", 9, 3, hl=False) + cv.text(58, y + h / 2 + 5, "Core %d" % n, 14, 800, fill="#fff")
        return o

    def job(x, y, n, h=34, dim=False):
        o = P.lift(cv, x, y, JW, h, cols[(n - 1) % 4], 9, 3, hl=False)
        return o + cv.text(x + JW / 2, y + h / 2 + 5, "Job %d" % n, 14.5, 800, fill=P._on(cols[(n - 1) % 4]))
    # one core
    cv.add(cv.text(50, 26, "One core: the jobs queue up", 16, 800, anchor="start", cls="il-ink il-h"))
    cv.add(lane(36, 1))
    for k in range(4):
        cv.add(job(X0 + 4 + k * 108, 36, k + 1))
    cv.add(P.arrow(cv, [(X0, 84), (X0 + W - 6, 84)], ARROW, 3, 10, op=.6))
    cv.add(cv.text(X0 + W - 6, 99, "time", 12.5, 600, anchor="end", cls="il-ink2"))
    # four cores
    cv.add(cv.text(50, 126, "Four cores: four jobs at once", 16, 800, anchor="start", cls="il-ink il-h"))
    for i in range(4):
        y = 138 + i * 40
        cv.add(lane(y, i + 1), job(X0 + 4, y, i + 1))
    cv.add(cv.line(X0 + 112, 132, X0 + 112, 298, PAL["green"][1], 2.5, dash="5 5"))
    cv.add(P.pill(cv, X0 + 276, 214, "done in a quarter of the time", "green", 14, 12, 28, 750))
    # a chain
    cv.add(cv.text(50, 326, "...but only if the work can be split", 16, 800, anchor="start", cls="il-ink il-h"))
    for i in range(3):
        y = 338 + i * 40
        cv.add(lane(y, i + 1), job(X0 + 4 + i * 108, y, i + 1))
        if i:
            cv.add(hourglass(cv, X0 + 30 + (i - 1) * 54 + 20, y + 17, .9))
            cv.add(P.arrow(cv, [(X0 + 4 + i * 108 - 4, y - 5), (X0 + 4 + i * 108 + 8, y + 4)], ARROW, 2.5, 8))
    cv.add(P.pill(cv, X0 + 360, 380, "Job 3 needs Job 2", "paper", 14, 12, 28, 700))
    cv.add(P.cross(cv, X0 + W - 10, 468, 11), cv.text(X0 + W - 28, 473, "the other cores sit idle", 14.5, 650, anchor="end"))
    # the GPU
    cv.add(P.card(cv, 566, 26, 222, 270, 18, "GPU", "plum"))
    for r in range(9):
        for c in range(11):
            col = ("sky", "mint", "sun", "coral", "lilac")[(r + c) % 5]
            cv.add(cv.rect(580 + c * 18.6, 70 + r * 19.5, 14.5, 15, 3, cv.g(col)))
    cv.add(cv.text(677, 262, "thousands of tiny cores", 14.5, 700, cls="il-ink"))
    cv.add(cv.text(677, 282, "all doing the same kind of job", 12.5, 600, cls="il-ink2"))
    cv.add(P.card(cv, 566, 318, 222, 162, 18))
    for j, (kind, t) in enumerate((("ok", "Pixels in a picture"), ("ok", "Frames of a film"), ("bad", "Steps that need the last"))):
        cv.add(P.tick(cv, 590, 352 + j * 38, 11) if kind == "ok" else P.cross(cv, 590, 352 + j * 38, 11))
        cv.add(cv.text(610, 358 + j * 38, t, 14.5, 650, anchor="start"))
    cv.add(cv.text(677, 462, "split well, or not at all", 12.5, 600, cls="il-ink2"))
    cv.add(P.badge(cv, 26, 20, 1), P.badge(cv, 26, 120, 2), P.badge(cv, 26, 320, 3), P.badge(cv, 580, 30, 4))
    return figure(
        "parallel-cores", cv, "Why more cores is not simply more speed",
        "Why more cores is not simply more speed. A single core takes jobs from the queue one after another, so four jobs take four times as "
        "long as one. Four cores can take one job each at the same moment, and the queue clears in roughly a quarter of the time. That only "
        "works if the work can genuinely be split: when job three needs the result of job two it has to wait however many cores are sitting "
        "idle, which is why doubling the cores rarely doubles the speed. A graphics processor takes the idea much further, with thousands of "
        "tiny cores that all do the same kind of job at once, which suits work that splits perfectly, such as the pixels in a picture.",
        ["One core takes the jobs one after another, in order.",
         "Four cores take four jobs at once, so the queue clears sooner.",
         "Only if the work can be split. Some jobs must wait for the one before.",
         "A GPU takes this much further: thousands of tiny cores, one kind of job."],
        "The exam answer is the condition, not the claim: more cores help when the task can be divided.")


@illustration("virtual-memory")
def _virtual_memory():
    cv = Canvas(800, 500).backdrop()
    cv.add(P.card(cv, 14, 34, 590, 214, 20, "RAM: fast, and small", "teal", .22))
    cv.add(P.card(cv, 14, 290, 590, 190, 20, "Disk: slow, and huge", "plum", .22))
    slots = [("A1", "sky"), ("A2", "sky"), ("B1", "mint"), ("B2", "mint"), ("C1", "plum"), ("C2", "plum"), ("A3", "sky"), ("C3", "plum")]
    pos = {}
    for i, (name, col) in enumerate(slots):
        x, y = 38 + (i % 4) * 140, 76 + (i // 4) * 80
        pos[name] = (x, y)
        cv.add(P.lift(cv, x, y, 124, 64, col, 12, 5, hl=False), cv.text(x + 62, y + 40, name, 20, 800, fill=P._on(col)))
    ox, oy = pos["C3"]
    cv.add(cv.rect(ox - 4, oy - 4, 132, 72, 15, "none", stroke="#E6574D", sw=3.5, dash="7 6"))
    cv.add(P.pill(cv, ox + 62, oy - 6, "not used lately", "coral", 12.5, 8, 22, 750))
    # the disk
    cv.add(cv.rect(40, 332, 548, 130, 14, "var(--il-band)", stroke="var(--il-line)", sw=1.5, dash="7 6"))
    cv.add(P.hdd(cv, 52, 346, 112))
    cv.add(cv.text(218, 453, "swap space (the page file)", 14.5, 750, anchor="start", cls="il-ink"))
    for i, (name, col) in enumerate((("B4", "mint"), ("A7", "sky"), ("C3", "plum"))):
        x = 218 + i * 124
        cv.add(P.lift(cv, x, 376, 108, 56, col, 11, 4, hl=False), cv.text(x + 54, 411, name, 18, 800, fill=P._on(col)))
    # a new program that does not fit
    cv.add(cv.rect(634, 60, 152, 116, 14, cv.lin("winD", [(0, "#FFFFFF"), (1, "#EEF3F6")]), stroke="var(--il-line)", sw=1.5))
    cv.add(cv.rect(634, 60, 152, 26, 14, cv.g("coral")) + cv.rect(634, 74, 152, 12, 0, PAL["coral"][1]))
    for i, c in enumerate(("#fff", "#fff", "#fff")):
        cv.add(cv.circle(650 + i * 12, 73, 3.4, c, op=.85))
    cv.add(cv.text(710, 128, "Program D", 17, 800, fill=INK))
    cv.add(cv.text(710, 152, "opening now", 13, 600, fill="#4A6470"))
    cv.add(P.pill(cv, 710, 206, "no room left!", "red", 14, 10, 28, 750))
    cv.add(P.arrow(cv, [(630, 142), (590, 142), (ox + 134, oy + 36)], ARROW, 4, 12, op=.7, dash="6 6"))
    # swapping
    cv.add(P.curve_arrow(cv, (ox + 62, oy + 70), (ox + 80, 280), (ox + 80, 330), (ox + 62, 372), PAL["coral"][1], 5.5, 14))
    cv.add(P.curve_arrow(cv, (282, 372), (282, 320), (330, 290), (352, 232), PAL["teal"][1], 5.5, 14, dash="2 9"))
    cv.add(P.pill(cv, 440, 270, "needed again", "teal", 13.5, 10, 26, 750))
    # slow
    cv.add(P.pill(cv, 700, 330, "disk is slow", "paper", 14, 10, 28, 700), hourglass(cv, 700, 372, 1.8))
    cv.add(cv.text(700, 424, "so the computer", 13.5, 600, cls="il-ink2"), cv.text(700, 442, "feels sluggish", 13.5, 600, cls="il-ink2"))
    cv.add(P.badge(cv, 40, 34, 1), P.badge(cv, 626, 60, 2), P.badge(cv, ox + 98, 296, 3), P.badge(cv, ox + 130, oy + 28, 4), P.badge(cv, 338, 262, 5))
    return figure(
        "virtual-memory", cv, "Virtual memory: pages moved between RAM and disk",
        "Virtual memory, drawn as pages moving between two levels. RAM holds the parts of the running programs that are needed now: it is "
        "fast, volatile and small. The disk below is slow, permanent and enormous. When another program is started and there is no space "
        "left in RAM, the operating system picks a page that has not been used recently and writes it out to a reserved area of the disk, "
        "which is the swap space or page file. That frees real memory so the new program can start. If the page that was swapped out is "
        "needed again, it has to be fetched back from the disk, which is thousands of times slower than RAM, and that is why a computer that "
        "is short of memory and swapping constantly feels so slow.",
        ["RAM holds the programs that are running. It is fast, and it is small.",
         "Open one program too many and there is no room left.",
         "A page that has not been used lately is written out to the disk.",
         "That frees real memory, so the new program can start.",
         "Needed again, the page is fetched back, which is why it goes slow."],
        "Virtual memory does not make a machine faster. It lets it run more than will fit, and pays for that in disk time.")


@illustration("units-of-data")
def _units():
    cv = Canvas(800, 500).backdrop()
    steps = [
        ("bit", "1 bit", "0 or 1", "sky"), ("byte", "8 bits", "1 character", "teal"), ("KB", "1,000 bytes", "a page of text", "mint"),
        ("MB", "1,000 KB", "a photograph", "sun"), ("GB", "1,000 MB", "a film", "coral"), ("TB", "1,000 GB", "a hard disk", "plum"),
    ]
    base = 452
    cv.add(cv.rect(0, base, 800, 48, 0, "var(--il-band)"))
    for i, (name, size, eg, col) in enumerate(steps):
        x = 28 + i * 124
        h = 64 + i * 40
        y = base - h
        cv.add(cv.shadow(x + 56, base + 4, 62, 5, .2))
        cv.add(P.lift(cv, x, y, 116, h, col, 12, 6, hl=False))
        cv.add(cv.rect(x + 6, y + 5, 104, 18, 8, "#fff", op=.2))
        tc = P._on(col)
        cv.add(cv.text(x + 58, y + 44, name, 30 if i else 26, 800, fill=tc, cls="il-h"))
        if h > 108:
            cv.add(cv.text(x + 58, y + 68, size, 13.5, 700, fill=tc))
            cv.add(cv.text(x + 58, y + 86, eg, 12.5, 600, fill=tc))
        else:
            cv.add(cv.text(x + 58, y + 62, size if i else "", 13, 700, fill=tc))
        # the thing it holds, on top of the step
        cx, ty = x + 58, y - 8
        if i == 0:
            cv.add(P.toggle(cv, cx - 28, ty - 34, True), cv.text(cx, ty - 44, "1", 16, 800, mono=True, cls="il-ink"))
        elif i == 1:
            cv.add(P.lift(cv, cx - 24, ty - 50, 48, 46, "paper", 10, 4, hl=False), cv.text(cx, ty - 18, "A", 30, 800, fill=INK))
            for b in range(8):
                cv.add(cv.rect(cx - 24 + b * 6, ty - 62, 4.5, 8, 1.5, PAL["teal"][1] if b in (1, 7) else "#C3CFD8"))
        elif i == 2:
            cv.add(P.doc(cv, cx - 25, ty - 80, 1, 50, 70, 4, "paper", "teal"))
        elif i == 3:
            cv.add(P.photo(cv, cx - 34, ty - 66, 68, 48))
        elif i == 4:
            cv.add(P.lift(cv, cx - 40, ty - 62, 80, 52, "dark", 8, 4, hl=False))
            cv.add(cv.poly([(cx - 8, ty - 48), (cx - 8, ty - 24), (cx + 14, ty - 36)], "#fff"))
        else:
            cv.add(P.hdd(cv, cx - 44, ty - 74, 88, 1))
    cv.add(P.pixel_cat(cv, 40, 56, 74))
    cv.add(P.pill(cv, 214, 86, "each step up is × 1000", "paper", 15, 14, 32, 750))
    cv.add(P.badge(cv, 34, 398, 1), P.badge(cv, 160, 372, 2), P.badge(cv, 300, 330, 3), P.badge(cv, 424, 288, 4), P.badge(cv, 750, 196, 5))
    return figure(
        "units-of-data", cv, "The units of data storage, each step a thousand times the last",
        "The units of data storage drawn as a staircase, each step sitting on the one below it. A bit is a single binary digit, one 0 or one "
        "1, and it is the smallest thing a computer can store. A nibble is four bits. Eight bits make a byte, which is enough to hold one "
        "character of text. A thousand bytes make a kilobyte, roughly a page of plain text. A thousand kilobytes make a megabyte, about the "
        "size of a photograph or a minute of music. A thousand megabytes make a gigabyte, about a film, and a thousand gigabytes make a "
        "terabyte, about the capacity of a hard disk. Each step up from the byte is a thousand times the last.",
        ["A bit is one binary digit: a single 0 or a single 1.",
         "Eight bits make a byte, which is enough for one character.",
         "A thousand bytes make a kilobyte. A page of plain text.",
         "A thousand kilobytes make a megabyte. A photograph, or a minute of music.",
         "A thousand megabytes make a gigabyte, and a thousand of those a terabyte."],
        "Each step up is a thousand times the last. That is why a film does not fit on a floppy disk and a text file always will.")
