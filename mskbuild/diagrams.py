"""Inline SVG diagrams for the revision site.

Each entry in REGISTRY is a callable returning a complete <figure>. Diagrams are
embedded in topic content with the `!diagram <name>` markup directive. Every one
carries a <title> and a full <desc>, so a screen reader user receives the same
information the picture conveys rather than being told an image exists.
"""
from .svg import (figure, box, text, line, path, circle, chip, esc)

REGISTRY = {}


def diagram(name):
    def wrap(fn):
        REGISTRY[name] = fn
        return fn
    return wrap


TEAL = "var(--dg-accent)"
TEAL_SOFT = "var(--dg-accent-soft)"
LILAC = "var(--dg-alt)"
LILAC_SOFT = "var(--dg-alt-soft)"
WARN = "var(--dg-warn)"
WARN_SOFT = "var(--dg-warn-soft)"
FILL = "var(--dg-fill)"
LINE = "var(--dg-line)"
MUTED = "var(--dg-muted)"


def _lines(x, y, items, size=11, gap=21, fill="var(--dg-text)"):
    """A left aligned block of small text lines."""
    return "".join(text(x, y + i * gap, s, size, 450, anchor="start", fill=fill)
                   for i, s in enumerate(items))


# ============================================================ 1. FDE cycle

@diagram("fetch-decode-execute")
def _fde():
    b = []
    cols = [
        (11, "FETCH", TEAL, TEAL_SOFT, [
            "1. Address in the PC is",
            "    copied into the MAR",
            "2. The PC is incremented",
            "3. Address goes out on",
            "    the address bus",
            "4. Instruction returns on",
            "    the data bus into the MDR",
            "5. MDR is copied to the CIR",
        ]),
        (267, "DECODE", LILAC, LILAC_SOFT, [
            "6. The Control Unit splits",
            "    the instruction in the CIR",
            "7. The opcode says which",
            "    operation to perform",
            "8. The operand gives the data,",
            "    or the address of the data",
            "9. Control signals are sent",
            "    to the units that will act",
        ]),
        (523, "EXECUTE", TEAL, TEAL_SOFT, [
            "10. The instruction is",
            "      carried out",
            "11. An ALU result is placed",
            "      in the accumulator",
            "12. Status register flags",
            "      are updated",
            "13. A jump writes a new",
            "      address into the PC",
        ]),
    ]
    for x, title, accent, soft, steps in cols:
        b.append(box(x, 52, 226, 236, None, fill=FILL, stroke=accent))
        b.append(box(x, 52, 226, 34, None, fill=soft, stroke=accent, r=8))
        b.append(text(x + 113, 74, title, 13, 700, fill=accent))
        b.append(_lines(x + 13, 108, steps))

    b.append(line(240, 170, 264, 170, stroke=LINE, arrow=True))
    b.append(line(496, 170, 520, 170, stroke=LINE, arrow=True))

    b.append(path("M636 288 L636 330 L124 330 L124 292", stroke=TEAL, w=1.8,
                  dash="5 4", arrow=True, marker="ah-accent"))
    b.append(text(380, 322, "and repeat, billions of times each second", 11, 500,
                  fill=MUTED))

    desc = ("A three stage cycle. In fetch, the address in the program counter is copied "
            "into the memory address register, the program counter is incremented, the "
            "address travels out on the address bus, the instruction returns on the data "
            "bus into the memory data register and is then copied into the current "
            "instruction register. In decode, the control unit splits that instruction "
            "into an opcode saying which operation to perform and an operand giving the "
            "data or the address of the data, then sends control signals to the units that "
            "will act. In execute, the instruction is carried out, any result from the "
            "arithmetic logic unit is placed in the accumulator, the status register flags "
            "are updated, and a jump instruction writes a new address into the program "
            "counter. Control then returns to fetch and the cycle repeats.")
    return figure("fde", 760, 348, "".join(b),
                  "The fetch decode execute cycle", desc,
                  "The fetch decode execute cycle. Naming the registers and buses in this "
                  "order is what turns a one mark answer into a full mark one.")


# ======================================================== 2. CPU components

@diagram("cpu-components")
def _cpu():
    b = []
    b.append(box(20, 40, 420, 250, None, fill="var(--dg-fill-2)", stroke=TEAL, r=14))
    b.append(text(230, 64, "CENTRAL PROCESSING UNIT", 12, 700, fill=TEAL))

    b.append(box(40, 82, 180, 62, "Control Unit",
                 "decodes and coordinates", fill=FILL, stroke=LINE))
    b.append(box(240, 82, 180, 62, "Arithmetic Logic Unit",
                 "calculates and compares", fill=FILL, stroke=LINE))

    b.append(box(40, 158, 380, 76, None, fill=LILAC_SOFT, stroke=LILAC, r=10))
    b.append(text(230, 178, "REGISTERS", 11, 700, fill=LILAC))
    regs = [("PC", 60), ("MAR", 132), ("MDR", 204), ("CIR", 276), ("ACC", 348)]
    for lbl, x in regs:
        b.append(box(x - 30, 190, 60, 32, lbl, fill=FILL, stroke=LILAC, r=6,
                     label_size=11))

    b.append(box(40, 246, 380, 30, "Cache", fill=TEAL_SOFT, stroke=TEAL, r=8,
                 label_size=12, text_fill=TEAL))

    b.append(box(560, 90, 170, 60, "Main memory", "RAM", fill=FILL, stroke=LINE))
    b.append(box(560, 200, 170, 60, "Input and output", "devices", fill=FILL, stroke=LINE))

    buses = [(120, "Address bus", "one way, out of the CPU", TEAL),
             (170, "Data bus", "two way", LILAC),
             (220, "Control bus", "two way", MUTED)]
    for y, name, note, col in buses:
        b.append(line(444, y, 556, y, stroke=col, w=2, arrow=True,
                      marker="ah-accent" if col == TEAL else "ah"))
        b.append(text(500, y - 8, name, 10, 620, fill=col))
        b.append(text(500, y + 16, note, 9, 450, fill=MUTED))

    desc = ("The central processing unit contains a control unit which decodes instructions "
            "and coordinates the other components, an arithmetic logic unit which performs "
            "calculations and comparisons, a set of registers holding the program counter, "
            "memory address register, memory data register, current instruction register and "
            "accumulator, and cache holding recently used data and instructions. The CPU "
            "connects to main memory and to input and output devices through three buses. "
            "The address bus carries addresses one way out of the processor, the data bus "
            "carries data and instructions in both directions, and the control bus carries "
            "control signals in both directions.")
    return figure("cpu", 760, 310, "".join(b),
                  "Components of the CPU and the three buses", desc,
                  "The address bus is one way because addresses only ever travel out of the "
                  "processor. The data bus is two way because data travels in both.")


# ====================================================== 3. Memory hierarchy

@diagram("memory-hierarchy")
def _hier():
    b = []
    rows = [
        ("Registers", "a few bytes", "fastest, most expensive", 150, 46, TEAL),
        ("Cache", "KB to MB", "very fast", 240, 96, TEAL),
        ("RAM", "GB", "fast, volatile", 330, 146, LILAC),
        ("Secondary storage", "GB to TB", "slow, non volatile", 420, 196, MUTED),
    ]
    cx = 290
    for label, size, note, w, y, col in rows:
        x = cx - w / 2
        b.append(box(x, y, w, 42, None, fill=FILL, stroke=col, r=6))
        b.append(text(cx, y + 20, label, 12, 620))
        b.append(text(cx, y + 34, size, 10, 450, fill=MUTED))
        b.append(text(548, y + 26, note, 10, 500, anchor="start", fill=col))

    b.append(path("M28 250 L28 44", stroke=TEAL, w=2, arrow=True, marker="ah-accent"))
    b.append(text(20, 150, "faster", 10, 620, anchor="middle", fill=TEAL))
    b.append(path("M28 44 L28 250", stroke=MUTED, w=0, arrow=False))
    b.append(text(20, 262, "bigger and cheaper", 10, 500, anchor="start", fill=MUTED))

    desc = ("A four level pyramid. Registers sit at the top holding a few bytes and are the "
            "fastest and most expensive storage. Below them cache holds kilobytes to "
            "megabytes and is very fast. Below that RAM holds gigabytes, is fast and is "
            "volatile. At the base secondary storage holds gigabytes to terabytes, is slow "
            "and is non volatile. Moving up the pyramid storage gets faster, smaller and "
            "more expensive per byte. Moving down it gets larger and cheaper.")
    return figure("hier", 760, 290, "".join(b),
                  "The memory hierarchy", desc,
                  "The pattern is consistent: the closer to the processor, the faster, the "
                  "smaller and the more expensive per byte.", max_w=620)


# ================================================ 4. Von Neumann vs Harvard

@diagram("von-neumann-harvard")
def _vnh():
    b = []
    for ox, title, col in ((10, "Von Neumann", TEAL), (400, "Harvard", LILAC)):
        b.append(box(ox, 34, 350, 236, None, fill="var(--dg-fill-2)", stroke=col, r=12))
        b.append(text(ox + 175, 56, title, 13, 700, fill=col))
        b.append(box(ox + 125, 74, 100, 44, "CPU", fill=FILL, stroke=LINE))

    b.append(box(135, 200, 100, 48, "Memory", "code + data", fill=FILL, stroke=LINE))
    b.append(line(185, 120, 185, 196, stroke=TEAL, w=2.5, arrow=True, marker="ah-accent"))
    b.append(chip(185, 160, "one shared bus", TEAL_SOFT, TEAL, TEAL))
    b.append(text(185, 264, "instructions and data compete for the bus", 10, 500, fill=MUTED))

    b.append(box(430, 200, 110, 48, "Instruction", "memory", fill=FILL, stroke=LINE))
    b.append(box(620, 200, 110, 48, "Data", "memory", fill=FILL, stroke=LINE))
    b.append(path("M555 120 L485 196", stroke=LILAC, w=2.5, arrow=True, marker="ah-alt"))
    b.append(path("M605 120 L675 196", stroke=LILAC, w=2.5, arrow=True, marker="ah-alt"))
    b.append(chip(580, 160, "two buses", LILAC_SOFT, LILAC, LILAC))
    b.append(text(580, 264, "an instruction and data can be fetched at once", 10, 500,
                  fill=MUTED))

    desc = ("Two architectures side by side. In von Neumann, one CPU connects through a "
            "single shared bus to one memory holding both instructions and data, so "
            "instructions and data compete for that bus, which is the von Neumann "
            "bottleneck. In Harvard, one CPU connects through two separate buses to two "
            "separate memories, one holding instructions and one holding data, so an "
            "instruction and its data can be fetched at the same time.")
    return figure("vnh", 760, 288, "".join(b),
                  "Von Neumann architecture compared with Harvard architecture", desc,
                  "Harvard is faster because an instruction and data can be fetched "
                  "simultaneously. Von Neumann is cheaper and more flexible.")


# ---------------------------------------------------------- shared builders

def _ttable(x, y, headers, rows, cw=30, rh=19, accent=LINE, rule_before=1):
    """A compact truth table. `rule_before` is how many columns from the right
    the dividing rule sits, separating inputs from outputs."""
    n = len(headers)
    w = n * cw
    h = (len(rows) + 1) * rh
    out_from = n - rule_before
    b = [box(x, y, w, h, None, fill="var(--dg-fill-2)", stroke=accent, r=6)]
    b.append(line(x, y + rh, x + w, y + rh, stroke=accent, w=1))
    b.append(line(x + out_from * cw, y, x + out_from * cw, y + h, stroke=accent, w=1))
    for i, hd in enumerate(headers):
        b.append(text(x + i * cw + cw / 2.0, y + rh - 6, hd, 10, 700,
                      fill=TEAL if i >= out_from else MUTED))
    for r, row in enumerate(rows):
        for i, cell in enumerate(row):
            b.append(text(x + i * cw + cw / 2.0, y + (r + 2) * rh - 6, cell, 10, 500,
                          mono=True,
                          fill=TEAL if i >= out_from else "var(--dg-text)"))
    return "".join(b)


def _gate(kind, x, y, w=46, h=36, stroke=None):
    """A logic gate symbol whose body starts at x and whose output tip is
    returned alongside the drawing, so wires can be attached exactly."""
    stroke = stroke or LINE
    b = []
    my = y + h / 2.0
    bubble = kind in ("NAND", "NOR", "NOT", "XNOR")
    bw = w - (10 if bubble else 0)
    if kind in ("AND", "NAND"):
        r = h / 2.0
        b.append(path("M%s %s L%s %s A%s %s 0 0 1 %s %s L%s %s Z"
                      % (x, y, x + bw - r, y, r, r, x + bw - r, y + h, x, y + h),
                      stroke=stroke, w=1.6, fill=FILL))
    elif kind in ("OR", "NOR", "XOR", "XNOR"):
        b.append(path("M%s %s Q%s %s %s %s Q%s %s %s %s Q%s %s %s %s Z"
                      % (x, y, x + bw * 0.55, y, x + bw, my,
                         x + bw * 0.55, y + h, x, y + h,
                         x + bw * 0.22, my, x, y),
                      stroke=stroke, w=1.6, fill=FILL))
        if kind in ("XOR", "XNOR"):
            b.append(path("M%s %s Q%s %s %s %s"
                          % (x - 7, y, x + bw * 0.22 - 7, my, x - 7, y + h),
                          stroke=stroke, w=1.6))
    else:  # NOT
        b.append(path("M%s %s L%s %s L%s %s Z" % (x, y, x, y + h, x + bw, my),
                      stroke=stroke, w=1.6, fill=FILL))
    if bubble:
        b.append(circle(x + bw + 5, my, 5, fill=FILL, stroke=stroke, w=1.6))
    return "".join(b), (x + w if bubble else x + bw), my


# ==================================================== 5. Network topologies

@diagram("network-topologies")
def _topo():
    b = []
    for ox, title, col in ((10, "STAR", TEAL), (390, "MESH", LILAC)):
        b.append(box(ox, 34, 360, 260, None, fill="var(--dg-fill-2)", stroke=col, r=12))
        b.append(text(ox + 180, 56, title, 12, 700, fill=col))

    hub = (155, 150, 70, 40)
    nodes = [(38, 82), (252, 82), (38, 226), (252, 226)]
    for nx, ny in nodes:
        b.append(line(nx + 36, ny + 16, 190, 170, stroke=TEAL, w=1.6))
    b.append(box(hub[0], hub[1], hub[2], hub[3], "Switch", fill=TEAL_SOFT,
                 stroke=TEAL, label_size=11, text_fill=TEAL))
    for i, (nx, ny) in enumerate(nodes):
        b.append(box(nx, ny, 72, 32, "Device %d" % (i + 1), fill=FILL, stroke=LINE,
                     label_size=10))
    b.append(text(190, 268, "every device has one link to the switch", 10, 500, fill=MUTED))
    b.append(text(190, 284, "one cable fails, one device is cut off", 10, 500, fill=MUTED))

    pent = [(570, 88), (648, 145), (618, 236), (522, 236), (492, 145)]
    for i in range(5):
        for j in range(i + 1, 5):
            b.append(line(pent[i][0], pent[i][1], pent[j][0], pent[j][1],
                          stroke=LILAC, w=1.3))
    for i, (px, py) in enumerate(pent):
        b.append(circle(px, py, 19, fill=LILAC_SOFT, stroke=LILAC, w=1.6))
        b.append(text(px, py + 4, chr(65 + i), 11, 700, fill=LILAC))
    b.append(text(570, 268, "every device links to every other device", 10, 500, fill=MUTED))
    b.append(text(570, 284, "many routes, so one broken link is survivable", 10, 500,
                  fill=MUTED))

    desc = ("Two topologies side by side. In a star, four devices each have a single "
            "cable running to a central switch, and no device connects directly to "
            "another, so traffic always passes through the switch. If one cable fails "
            "only that one device is cut off, but if the switch fails the whole network "
            "stops. In a full mesh, five devices labelled A to E are each joined "
            "directly to all four of the others, giving ten links in total. Because "
            "there are many possible routes between any two devices, a broken link "
            "does not stop traffic, but the amount of cable needed grows very quickly.")
    return figure("topo", 760, 300, "".join(b),
                  "Star topology compared with mesh topology", desc,
                  "In a full mesh of n devices there are n times n minus one, all divided "
                  "by two links. Five devices need ten. Ten devices would need forty five.")


# ======================================================== 6. TCP/IP stack

@diagram("tcp-ip-stack")
def _stack():
    b = []
    layers = [
        (56, "Application", "HTTP, HTTPS, FTP, SMTP, IMAP", TEAL),
        (126, "Transport", "TCP splits data into packets, adds port numbers", LILAC),
        (196, "Internet", "IP adds source and destination IP addresses", TEAL),
        (266, "Link", "Ethernet or Wi-Fi, adds MAC addresses", MUTED),
    ]
    for y, name, note, col in layers:
        b.append(box(30, y, 280, 58, None, fill=FILL, stroke=col, r=8))
        b.append(text(46, y + 24, name, 12, 700, anchor="start", fill=col))
        b.append(text(46, y + 42, note, 9, 450, anchor="start", fill=MUTED))

    b.append(path("M20 62 L20 330", stroke=TEAL, w=2, arrow=True, marker="ah-accent"))
    b.append(text(22, 48, "sending", 9, 700, anchor="middle", fill=TEAL))

    seg_h = 30
    rows = [
        [(530, 190, "Data", TEAL_SOFT, TEAL)],
        [(470, 60, "TCP", LILAC_SOFT, LILAC), (530, 190, "Data", TEAL_SOFT, TEAL)],
        [(410, 60, "IP", TEAL_SOFT, TEAL), (470, 60, "TCP", LILAC_SOFT, LILAC),
         (530, 190, "Data", TEAL_SOFT, TEAL)],
        [(350, 60, "Frame", WARN_SOFT, WARN), (410, 60, "IP", TEAL_SOFT, TEAL),
         (470, 60, "TCP", LILAC_SOFT, LILAC), (530, 190, "Data", TEAL_SOFT, TEAL),
         (720, 28, "End", WARN_SOFT, WARN)],
    ]
    for (y, _n, _t, _c), segs in zip(layers, rows):
        for sx, sw, lbl, fl, st in segs:
            b.append(box(sx, y + 14, sw, seg_h, lbl, fill=fl, stroke=st, r=5,
                         label_size=10, text_fill=st))
    b.append(text(550, 340, "each layer wraps the layer above in its own header",
                  10, 500, fill=MUTED))
    b.append(text(550, 356, "the receiver unwraps them in the reverse order",
                  10, 500, fill=MUTED))

    desc = ("The four layer TCP/IP model, drawn top to bottom with the growing packet "
            "beside it. The application layer handles protocols such as HTTP, HTTPS, "
            "FTP, SMTP and IMAP, and produces the raw data. The transport layer, using "
            "TCP, splits that data into packets and adds a header carrying port numbers, "
            "so the packet is now a TCP header followed by data. The internet layer adds "
            "an IP header carrying the source and destination IP addresses, so the packet "
            "is an IP header, a TCP header and the data. The link layer, Ethernet or "
            "Wi-Fi, adds a frame header carrying MAC addresses and a frame end, giving "
            "frame header, IP header, TCP header, data, frame end. Each layer wraps the "
            "one above it in its own header, and the receiving computer unwraps the "
            "layers in reverse order.")
    return figure("stack", 760, 370, "".join(b),
                  "The four layer TCP/IP model and packet encapsulation", desc,
                  "Layers are independent. Changing from Wi-Fi to Ethernet swaps the link "
                  "layer only, and nothing above it has to change.")


# =========================================================== 7. Logic gates

@diagram("logic-gates")
def _gates():
    b = []
    cells = [
        (8, 40, "AND", "Q = A . B", ["A", "B"],
         [["0", "0", "0"], ["0", "1", "0"], ["1", "0", "0"], ["1", "1", "1"]]),
        (258, 40, "OR", "Q = A + B", ["A", "B"],
         [["0", "0", "0"], ["0", "1", "1"], ["1", "0", "1"], ["1", "1", "1"]]),
        (508, 40, "NOT", "Q = NOT A", ["A"],
         [["0", "1"], ["1", "0"]]),
        (8, 218, "XOR", "Q = A xor B", ["A", "B"],
         [["0", "0", "0"], ["0", "1", "1"], ["1", "0", "1"], ["1", "1", "0"]]),
        (258, 218, "NAND", "Q = NOT (A . B)", ["A", "B"],
         [["0", "0", "1"], ["0", "1", "1"], ["1", "0", "1"], ["1", "1", "0"]]),
        (508, 218, "NOR", "Q = NOT (A + B)", ["A", "B"],
         [["0", "0", "1"], ["0", "1", "0"], ["1", "0", "0"], ["1", "1", "0"]]),
    ]
    for cx, cy, name, expr, ins, rows in cells:
        b.append(box(cx, cy, 244, 162, None, fill="var(--dg-fill-2)", stroke=LINE, r=10))
        b.append(text(cx + 14, cy + 22, name, 13, 700, anchor="start", fill=TEAL))
        b.append(text(cx + 14, cy + 39, expr, 10, 500, anchor="start", fill=MUTED))
        gx, gy = cx + 36, cy + 58
        svg, tip, my = _gate(name, gx, gy, 48, 40)
        if len(ins) == 2:
            ys = [gy + 10, gy + 30]
        else:
            ys = [my]
        for lbl, yy in zip(ins, ys):
            b.append(line(gx - 20, yy, gx + 2, yy, stroke=LINE, w=1.4))
            b.append(text(gx - 26, yy + 4, lbl, 10, 700, fill=MUTED))
        b.append(svg)
        b.append(line(tip, my, tip + 22, my, stroke=LINE, w=1.4))
        b.append(text(tip + 30, my + 4, "Q", 10, 700, fill=TEAL))
        b.append(_ttable(cx + 148, cy + 46, ins + ["Q"], rows, cw=30))

    desc = ("Six logic gates, each with its British Standard symbol, its Boolean "
            "expression and its truth table. AND, written Q equals A dot B, gives 1 only "
            "when both inputs are 1. OR, written Q equals A plus B, gives 1 when at least "
            "one input is 1. NOT, a triangle with a small circle, inverts its single "
            "input, so 0 becomes 1 and 1 becomes 0. XOR, exclusive or, gives 1 when the "
            "inputs are different and 0 when they are the same. NAND is AND followed by "
            "an inverting circle, so it gives 0 only when both inputs are 1 and 1 "
            "otherwise. NOR is OR followed by an inverting circle, so it gives 1 only "
            "when both inputs are 0.")
    return figure("gates", 760, 396, "".join(b),
                  "The six logic gates with symbols, expressions and truth tables", desc,
                  "The small circle on a symbol always means invert. Learn AND, OR and NOT, "
                  "then NAND, NOR and XNOR are just those with a circle added.")


# ========================================================= 8. Logic circuit

@diagram("logic-circuit")
def _circuit():
    b = []
    b.append(text(20, 30, "Q = (A . B) + (NOT C)", 13, 700, anchor="start", fill=TEAL))

    for lbl, yy in (("A", 70), ("B", 100), ("C", 190)):
        b.append(text(34, yy + 4, lbl, 12, 700, fill=MUTED))
        b.append(circle(52, yy, 4, fill=LINE, stroke=LINE))

    and_svg, and_tip, and_my = _gate("AND", 150, 65, 52, 40)
    b.append(line(52, 70, 152, 75, stroke=LINE, w=1.4))
    b.append(line(52, 100, 152, 95, stroke=LINE, w=1.4))
    b.append(and_svg)
    b.append(text(176, 58, "AND", 9, 700, fill=MUTED))

    not_svg, not_tip, not_my = _gate("NOT", 150, 172, 46, 36)
    b.append(line(52, 190, 152, 190, stroke=LINE, w=1.4))
    b.append(not_svg)
    b.append(text(172, 165, "NOT", 9, 700, fill=MUTED))

    or_svg, or_tip, or_my = _gate("OR", 300, 108, 54, 44)
    b.append(path("M%s %s L262 %s L262 120 L302 120" % (and_tip, and_my, and_my),
                  stroke=LINE, w=1.4))
    b.append(path("M%s %s L262 %s L262 140 L302 140" % (not_tip, not_my, not_my),
                  stroke=LINE, w=1.4))
    b.append(or_svg)
    b.append(text(326, 100, "OR", 9, 700, fill=MUTED))
    b.append(line(or_tip, or_my, or_tip + 40, or_my, stroke=TEAL, w=1.8))
    b.append(text(or_tip + 54, or_my + 5, "Q", 13, 700, fill=TEAL))

    b.append(_ttable(508, 52, ["A", "B", "C", "A.B", "C'", "Q"], [
        ["0", "0", "0", "0", "1", "1"],
        ["0", "0", "1", "0", "0", "0"],
        ["0", "1", "0", "0", "1", "1"],
        ["0", "1", "1", "0", "0", "0"],
        ["1", "0", "0", "0", "1", "1"],
        ["1", "0", "1", "0", "0", "0"],
        ["1", "1", "0", "1", "1", "1"],
        ["1", "1", "1", "1", "0", "1"],
    ], cw=36, rh=20, rule_before=3))
    b.append(text(616, 254, "work out the middle columns first", 10, 500, fill=MUTED))

    desc = ("A circuit for Q equals A AND B, OR NOT C. Inputs A and B feed an AND gate. "
            "Input C feeds a NOT gate. The outputs of the AND gate and the NOT gate feed "
            "an OR gate, whose output is Q. The truth table has eight rows and shows the "
            "intermediate columns. With A, B and C as 0, 0, 0: A AND B is 0, NOT C is 1, "
            "Q is 1. With 0, 0, 1: 0 and 0, Q is 0. With 0, 1, 0: 0 and 1, Q is 1. With "
            "0, 1, 1: 0 and 0, Q is 0. With 1, 0, 0: 0 and 1, Q is 1. With 1, 0, 1: 0 and "
            "0, Q is 0. With 1, 1, 0: 1 and 1, Q is 1. With 1, 1, 1: 1 and 0, Q is 1. So "
            "Q is 1 in five of the eight rows.")
    return figure("circuit", 760, 280, "".join(b),
                  "A worked logic circuit and its full truth table", desc,
                  "Add a column for every gate output, not just the final one. The marks "
                  "for method are in those middle columns.")


# ===================================================== 9. Binary place value

@diagram("binary-place-values")
def _places():
    b = []
    vals = [128, 64, 32, 16, 8, 4, 2, 1]
    bits = [0, 1, 0, 1, 1, 0, 1, 0]
    x0, w, gap = 63, 74, 6
    for i, (v, bit) in enumerate(zip(vals, bits)):
        x = x0 + i * (w + gap)
        on = bit == 1
        b.append(box(x, 44, w, 32, str(v), fill=FILL, stroke=LINE, r=6, label_size=12,
                     text_fill=MUTED))
        b.append(box(x, 84, w, 44, str(bit),
                     fill=TEAL_SOFT if on else "var(--dg-fill-2)",
                     stroke=TEAL if on else LINE, r=6, label_size=20,
                     text_fill=TEAL if on else MUTED))
        b.append(text(x + w / 2.0, 152, str(v) if on else "0", 13, 700 if on else 450,
                      fill=TEAL if on else MUTED))
    b.append(text(x0 - 12, 64, "place", 10, 620, anchor="end", fill=MUTED))
    b.append(text(x0 - 12, 110, "bit", 10, 620, anchor="end", fill=MUTED))
    b.append(text(x0 - 12, 152, "worth", 10, 620, anchor="end", fill=MUTED))

    b.append(line(x0, 168, x0 + 8 * w + 7 * gap, 168, stroke=LINE, w=1))
    b.append(text(380, 194, "64 + 16 + 8 + 2 = 90", 16, 700, fill=TEAL))
    b.append(text(380, 216, "so 01011010 in binary is 90 in denary", 11, 500, fill=MUTED))

    desc = ("An eight bit binary number laid out under its place values. The place "
            "values from left to right are 128, 64, 32, 16, 8, 4, 2 and 1, each half "
            "the one to its left. The bits are 0, 1, 0, 1, 1, 0, 1, 0. Where a bit is "
            "1 the column contributes its place value, so the contributions are 0, 64, "
            "0, 16, 8, 0, 2 and 0. Adding the contributions gives 64 plus 16 plus 8 plus "
            "2, which is 90. So binary 01011010 is 90 in denary.")
    return figure("places", 760, 236, "".join(b),
                  "Converting binary 01011010 to denary using place values", desc,
                  "Write the place values above the bits every single time. It costs five "
                  "seconds and removes almost every conversion error.", max_w=700)


# =========================================================== 10. Bubble sort

@diagram("bubble-sort")
def _bubble():
    b = []
    b.append(text(380, 28, "Bubble sort on 5, 1, 4, 2, 8", 13, 700, fill=TEAL))
    rows = [
        ("start", [5, 1, 4, 2, 8], None, "", None),
        ("pass 1", [5, 1, 4, 2, 8], (0, 1), "5 is bigger than 1, so swap", None),
        ("", [1, 5, 4, 2, 8], (1, 2), "5 is bigger than 4, so swap", None),
        ("", [1, 4, 5, 2, 8], (2, 3), "5 is bigger than 2, so swap", None),
        ("", [1, 4, 2, 5, 8], (3, 4), "5 is smaller than 8, leave it", 4),
        ("pass 2", [1, 2, 4, 5, 8], None, "one swap this pass, 5 is now in place", 3),
        ("pass 3", [1, 2, 4, 5, 8], None, "no swaps at all, so the list is sorted", None),
    ]
    x0, w, gap = 236, 52, 6
    for r, (lbl, arr, hi, note, locked) in enumerate(rows):
        y = 52 + r * 44
        if lbl:
            b.append(text(228, y + 24, lbl, 11, 700, anchor="end", fill=MUTED))
        for i, v in enumerate(arr):
            x = x0 + i * (w + gap)
            on = hi is not None and i in hi
            done = locked is not None and i >= locked
            fill = TEAL_SOFT if on else (LILAC_SOFT if done else FILL)
            stroke = TEAL if on else (LILAC if done else LINE)
            b.append(box(x, y, w, 36, str(v), fill=fill, stroke=stroke, r=6,
                         label_size=15, text_fill=TEAL if on else (LILAC if done else "var(--dg-text)")))
        if note:
            b.append(text(x0 + 5 * (w + gap) + 6, y + 22, note, 10, 500,
                          anchor="start", fill=MUTED))
    desc = ("Bubble sort applied to the list 5, 1, 4, 2, 8. In pass one the algorithm "
            "compares each neighbouring pair from the left. It compares 5 and 1, 5 is "
            "bigger so they swap, giving 1, 5, 4, 2, 8. It compares 5 and 4 and swaps, "
            "giving 1, 4, 5, 2, 8. It compares 5 and 2 and swaps, giving 1, 4, 2, 5, 8. "
            "It compares 5 and 8, 5 is smaller so nothing moves, and the largest value 8 "
            "has bubbled to the end and is now in its final place. Pass two makes one "
            "swap, of 4 and 2, giving 1, 2, 4, 5, 8, and 5 is now also in place. Pass "
            "three makes no swaps at all, which tells the algorithm the list is sorted "
            "and it can stop.")
    return figure("bubble", 760, 372, "".join(b),
                  "Bubble sort worked through pass by pass", desc,
                  "After pass one the largest value is definitely at the end. After pass "
                  "two the two largest are. A pass with no swaps means the list is sorted.")


# ============================================================ 11. Merge sort

@diagram("merge-sort")
def _merge():
    b = []
    b.append(text(380, 22, "DIVIDE: split in half until every list holds one item",
                  11, 700, fill=TEAL))


    def rowdraw(y, groups, col, soft):
        k = len(groups)
        cents = []
        for i, g in enumerate(groups):
            cx = 760.0 * (i + 0.5) / k
            cents.append(cx)
            w = len(g) * 22 + 16
            b.append(box(cx - w / 2.0, y, w, 30, None, fill=soft, stroke=col, r=6))
            for j, v in enumerate(g):
                b.append(text(cx - w / 2.0 + 8 + j * 22 + 11, y + 20, str(v), 11, 620,
                              mono=True, fill=col))
        return cents

    d0 = [[38, 27, 43, 3, 9, 82, 10, 1]]
    d1 = [[38, 27, 43, 3], [9, 82, 10, 1]]
    d2 = [[38, 27], [43, 3], [9, 82], [10, 1]]
    d3 = [[38], [27], [43], [3], [9], [82], [10], [1]]
    m2 = [[27, 38], [3, 43], [9, 82], [1, 10]]
    m1 = [[3, 27, 38, 43], [1, 9, 10, 82]]
    m0 = [[1, 3, 9, 10, 27, 38, 43, 82]]

    ys = [34, 78, 122, 166]
    cents = []
    for y, g in zip(ys, (d0, d1, d2, d3)):
        cents.append(rowdraw(y, g, TEAL, "var(--dg-fill-2)"))
    for lvl in range(3):
        for i, cx in enumerate(cents[lvl + 1]):
            b.append(line(cents[lvl][i // 2], ys[lvl] + 30, cx, ys[lvl + 1],
                          stroke=LINE, w=1.2))

    ys2 = [232, 276, 320]
    c2 = []
    for y, g in zip(ys2, (m2, m1, m0)):
        c2.append(rowdraw(y, g, LILAC, LILAC_SOFT))
    for i, cx in enumerate(c2[0]):
        b.append(line(cents[3][i * 2] / 1.0, ys[3] + 30, cx, ys2[0], stroke=LILAC, w=1.2))
        b.append(line(cents[3][i * 2 + 1], ys[3] + 30, cx, ys2[0], stroke=LILAC, w=1.2))
    for lvl in range(2):
        for i, cx in enumerate(c2[lvl]):
            b.append(line(cx, ys2[lvl] + 30, c2[lvl + 1][i // 2], ys2[lvl + 1],
                          stroke=LILAC, w=1.2))

    desc = ("Merge sort on the list 38, 27, 43, 3, 9, 82, 10, 1. The divide phase splits "
            "the list in half repeatedly: first into 38, 27, 43, 3 and 9, 82, 10, 1; then "
            "into 38, 27 and 43, 3 and 9, 82 and 10, 1; then into eight single item lists. "
            "A list of one item is already sorted. The merge phase then combines pairs, "
            "each time comparing the front items of the two lists and taking the smaller. "
            "The pairs become 27, 38 and 3, 43 and 9, 82 and 1, 10. Those merge into 3, "
            "27, 38, 43 and 1, 9, 10, 82. Those merge into the final sorted list 1, 3, 9, "
            "10, 27, 38, 43, 82.")
    b.append(text(380, 362, "MERGE: rebuild in pairs, always taking the smaller "
                  "front item", 11, 700, fill=LILAC))
    return figure("merge", 760, 380, "".join(b),
                  "Merge sort: the divide phase and the merge phase", desc,
                  "Merge sort always takes about n log n comparisons, whatever order the "
                  "list starts in, but it needs extra memory to hold the part lists.")


# ========================================================= 12. Binary search

@diagram("binary-search")
def _bsearch():
    b = []
    vals = [2, 5, 8, 12, 16, 23, 38, 56, 72, 91, 100]
    b.append(text(380, 28, "Binary search for 12 in a sorted list of 11 items",
                  12, 700, fill=TEAL))
    steps = [
        (0, 10, 5, "midpoint is 23. 12 is smaller, so throw away 23 and everything right"),
        (0, 4, 2, "midpoint is 8. 12 is bigger, so throw away 8 and everything left"),
        (3, 4, 3, "midpoint is 12. Found it, after only three comparisons"),
    ]
    x0, w, gap = 41, 58, 4
    for r, (lo, hi, mid, note) in enumerate(steps):
        y = 66 + r * 94
        for i, v in enumerate(vals):
            x = x0 + i * (w + gap)
            inside = lo <= i <= hi
            if i == mid:
                fl, st, tf = TEAL_SOFT, TEAL, TEAL
            elif inside:
                fl, st, tf = FILL, LINE, "var(--dg-text)"
            else:
                fl, st, tf = "var(--dg-fill-2)", "var(--dg-line-soft)", "var(--dg-muted)"
            b.append(box(x, y, w, 34, str(v), fill=fl, stroke=st, r=6, label_size=13,
                         text_fill=tf))
            if i == lo:
                b.append(text(x + w / 2.0, y - 6, "low", 9, 700, fill=LILAC))
            if i == hi and hi != lo:
                b.append(text(x + w / 2.0, y - 6, "high", 9, 700, fill=LILAC))
            if i == mid:
                b.append(text(x + w / 2.0, y + 48, "mid", 9, 700, fill=TEAL))
        b.append(text(41, y + 70, note, 10, 500, anchor="start", fill=MUTED))
    desc = ("Binary search looking for 12 in the sorted list 2, 5, 8, 12, 16, 23, 38, 56, "
            "72, 91, 100. Step one sets low to the first item and high to the last, giving "
            "a midpoint of 23. The target 12 is smaller than 23, so the whole right half "
            "including 23 is discarded. Step two searches 2, 5, 8, 12, 16 with a midpoint "
            "of 8. The target 12 is bigger than 8, so 8 and everything to its left is "
            "discarded. Step three searches 12 and 16 with a midpoint of 12, which is the "
            "target, so the search succeeds after three comparisons rather than the four "
            "a linear search would need.")
    return figure("bsearch", 760, 344, "".join(b),
                  "Binary search halving the list three times", desc,
                  "Binary search only works on a sorted list. Doubling the list length "
                  "adds just one extra comparison, which is why it scales so well.")


# =========================================================== 13. Binary tree

@diagram("binary-tree")
def _tree():
    b = []
    nodes = {8: (215, 52), 3: (110, 116), 10: (320, 116), 1: (56, 180),
             6: (168, 180), 14: (382, 180), 4: (132, 244), 7: (206, 244),
             13: (348, 244)}
    edges = [(8, 3), (8, 10), (3, 1), (3, 6), (10, 14), (6, 4), (6, 7), (14, 13)]
    for a, c in edges:
        b.append(line(nodes[a][0], nodes[a][1], nodes[c][0], nodes[c][1],
                      stroke=LINE, w=1.4))
    for v, (x, y) in nodes.items():
        b.append(circle(x, y, 21, fill=TEAL_SOFT if v == 8 else FILL, stroke=TEAL, w=1.6))
        b.append(text(x, y + 5, str(v), 13, 700, fill=TEAL if v == 8 else "var(--dg-text)"))
    b.append(text(215, 24, "A binary search tree", 12, 700, fill=TEAL))
    b.append(text(215, 288, "smaller values go left, larger values go right",
                  10, 500, fill=MUTED))

    orders = [
        (60, "Pre-order", "root, left, right", "8  3  1  6  4  7  10  14  13", TEAL),
        (140, "In-order", "left, root, right", "1  3  4  6  7  8  10  13  14", LILAC),
        (220, "Post-order", "left, right, root", "1  4  7  6  3  13  14  10  8", MUTED),
    ]
    for y, name, rule, seq, col in orders:
        b.append(box(452, y, 292, 62, None, fill="var(--dg-fill-2)", stroke=col, r=8))
        b.append(text(468, y + 20, name, 12, 700, anchor="start", fill=col))
        b.append(text(468, y + 36, rule, 9, 450, anchor="start", fill=MUTED))
        b.append(text(468, y + 54, seq, 11, 620, anchor="start", mono=True))
    b.append(text(598, 300, "in-order always comes out in ascending order",
                  10, 500, fill=LILAC))

    desc = ("A binary search tree with root 8. The root's left child is 3 and its right "
            "child is 10. Node 3 has children 1 and 6. Node 6 has children 4 and 7. Node "
            "10 has a right child 14, and 14 has a left child 13. Every value in a left "
            "subtree is smaller than its parent and every value in a right subtree is "
            "larger. Traversing pre-order, which visits root then left then right, gives "
            "8, 3, 1, 6, 4, 7, 10, 14, 13. Traversing in-order, which visits left then "
            "root then right, gives 1, 3, 4, 6, 7, 8, 10, 13, 14, which is ascending "
            "order. Traversing post-order, which visits left then right then root, gives "
            "1, 4, 7, 6, 3, 13, 14, 10, 8.")
    return figure("tree", 760, 314, "".join(b),
                  "A binary search tree and its three traversal orders", desc,
                  "The name of each traversal tells you when the root is visited: pre "
                  "means before the subtrees, in means between them, post means after.")


# ================================================== 14. Linked list vs array

@diagram("linked-list-vs-array")
def _lla():
    b = []
    b.append(text(20, 26, "ARRAY", 12, 700, anchor="start", fill=TEAL))
    b.append(text(78, 26, "one block of memory, fixed size", 10, 450, anchor="start",
                 fill=MUTED))
    vals = ["Ada", "Bob", "Cai", "Dee", "Eve"]
    x0, w = 40, 128
    for i, v in enumerate(vals):
        x = x0 + i * (w + 6)
        b.append(box(x, 42, w, 44, v, fill=FILL, stroke=TEAL, r=6, label_size=12))
        b.append(text(x + w / 2.0, 100, "index %d" % i, 9, 620, fill=MUTED))
        b.append(text(x + w / 2.0, 114, "address %d" % (400 + i * 4), 9, 450, fill=MUTED))
    b.append(_lines(20, 140, [
        "To reach index 3 the computer works out 400 + 3 x 4 and jumps straight there.",
        "Inserting in the middle means shifting every item after it along by one.",
    ], size=10, gap=16, fill=MUTED))

    b.append(text(20, 186, "LINKED LIST", 12, 700, anchor="start", fill=LILAC))
    b.append(text(112, 186, "scattered nodes, each holding a pointer to the next",
                  10, 450, anchor="start", fill=MUTED))
    order = [("Ada", 512, 730), ("Bob", 730, 604), ("Cai", 604, 918), ("Dee", 918, None)]
    nx = 40
    for i, (v, addr, nxt) in enumerate(order):
        x = nx + i * 178
        b.append(box(x, 204, 96, 48, None, fill=FILL, stroke=LILAC, r=6))
        b.append(text(x + 48, 224, v, 12, 620))
        b.append(text(x + 48, 240, "at %d" % addr, 9, 450, fill=MUTED))
        b.append(box(x + 96, 204, 52, 48, None, fill=LILAC_SOFT, stroke=LILAC, r=6))
        b.append(text(x + 122, 222, "next", 8, 620, fill=LILAC))
        b.append(text(x + 122, 238, str(nxt) if nxt else "null", 10, 700, fill=LILAC,
                      mono=True))
        if nxt:
            b.append(line(x + 148, 228, x + 174, 228, stroke=LILAC, w=1.6, arrow=True,
                          marker="ah-alt"))
    b.append(_lines(20, 288, [
        "To reach the fourth item you must start at the head and follow three pointers.",
        "Inserting in the middle changes two pointers, and the list can grow at any time.",
    ], size=10, gap=16, fill=MUTED))

    desc = ("Two data structures compared. An array holds Ada, Bob, Cai, Dee and Eve in "
            "one continuous block of memory at addresses 400, 404, 408, 412 and 416, "
            "indexed 0 to 4. Because the items are evenly spaced the computer can jump "
            "straight to any index by calculating start address plus index times item "
            "size, but inserting an item in the middle means shifting every item after it, "
            "and the array cannot grow beyond its declared size. A linked list holds the "
            "same names in nodes scattered anywhere in memory. Ada sits at address 512 "
            "and its next pointer holds 730, where Bob sits. Bob's pointer holds 604 for "
            "Cai. Cai's pointer holds 918 for Dee. Dee's pointer holds null, marking the "
            "end. Reaching the fourth item means following three pointers from the head, "
            "but inserting in the middle only changes two pointers and the list can grow "
            "as long as there is free memory.")
    return figure("lla", 760, 322, "".join(b),
                  "An array compared with a linked list", desc,
                  "Arrays win on reading a known position. Linked lists win on inserting "
                  "and deleting, and on not needing to know the size in advance.")


# ====================================================== 15. Packet switching

@diagram("packet-switching")
def _packets():
    b = []
    b.append(box(18, 118, 110, 74, "Sender", "splits the message", fill=TEAL_SOFT,
                 stroke=TEAL, r=10, text_fill=TEAL))
    b.append(box(632, 118, 110, 74, "Receiver", "reassembles it", fill=TEAL_SOFT,
                 stroke=TEAL, r=10, text_fill=TEAL))
    routers = {"R1": (232, 62), "R2": (232, 236), "R3": (380, 150),
               "R4": (528, 62), "R5": (528, 236)}
    links = [("R1", "R3"), ("R2", "R3"), ("R3", "R4"), ("R3", "R5"),
             ("R1", "R4"), ("R2", "R5"), ("R1", "R2")]
    for a, c in links:
        b.append(line(routers[a][0], routers[a][1], routers[c][0], routers[c][1],
                      stroke="var(--dg-line-soft)", w=1.3, dash="4 4"))
    b.append(line(128, 155, 214, 74, stroke="var(--dg-line-soft)", w=1.3, dash="4 4"))
    b.append(line(128, 155, 214, 226, stroke="var(--dg-line-soft)", w=1.3, dash="4 4"))
    b.append(line(546, 74, 630, 155, stroke="var(--dg-line-soft)", w=1.3, dash="4 4"))
    b.append(line(546, 226, 630, 155, stroke="var(--dg-line-soft)", w=1.3, dash="4 4"))

    b.append(path("M130 142 L232 62 L528 62 L634 140", stroke=TEAL, w=2.2, arrow=True,
                  marker="ah-accent"))
    b.append(path("M130 168 L232 236 L528 236 L634 172", stroke=LILAC, w=2.2, arrow=True,
                  marker="ah-alt"))
    b.append(path("M132 155 L232 236 L380 150 L528 62 L632 152", stroke=WARN, w=2.2,
                  dash="7 4"))

    for name, (x, y) in routers.items():
        b.append(circle(x, y, 22, fill=FILL, stroke=LINE, w=1.6))
        b.append(text(x, y + 5, name, 11, 700, fill=MUTED))

    b.append(chip(300, 40, "packet 1", TEAL_SOFT, TEAL, TEAL))
    b.append(chip(300, 262, "packet 2", LILAC_SOFT, LILAC, LILAC))
    b.append(chip(430, 200, "packet 3", WARN_SOFT, WARN, WARN))
    b.append(text(380, 296, "Packets take whatever route is free, so they can arrive "
                  "out of order.", 10, 500, fill=MUTED))
    b.append(text(380, 312, "Each one carries a sequence number, so the receiver can "
                  "rebuild the message in order.", 10, 500, fill=MUTED))
    desc = ("A message travelling across a packet switched network. The sender on the left "
            "splits the message into numbered packets. Five routers, R1 to R5, sit between "
            "the sender and the receiver, joined by several possible links. Packet 1 "
            "travels the northern route through R1 and R4. Packet 2 travels the southern "
            "route through R2 and R5. Packet 3 takes a third route through R2, R3 and R4. "
            "Because each packet is routed independently according to which links are free "
            "at that moment, packets can arrive in a different order from the one they "
            "were sent in. Every packet carries a sequence number, so the receiver on the "
            "right can put them back into the right order and rebuild the message, and can "
            "request any packet that never arrived.")
    return figure("packets", 760, 328, "".join(b),
                  "Packet switching across a network", desc,
                  "The exam answer is: split into packets, each routed independently by "
                  "the fastest free path, reassembled in sequence number order at the end.")


# ======================================================== 16. Stack vs queue

@diagram("stack-queue")
def _sq():
    b = []
    b.append(box(14, 34, 356, 258, None, fill="var(--dg-fill-2)", stroke=TEAL, r=12))
    b.append(text(192, 58, "STACK", 12, 700, fill=TEAL))
    b.append(text(192, 76, "last in, first out", 10, 450, fill=MUTED))
    items = ["D", "C", "B", "A"]
    for i, v in enumerate(items):
        y = 100 + i * 44
        top = i == 0
        b.append(box(120, y, 144, 38, v, fill=TEAL_SOFT if top else FILL,
                     stroke=TEAL if top else LINE, r=6, label_size=14,
                     text_fill=TEAL if top else "var(--dg-text)"))
    b.append(line(288, 96, 288, 130, stroke=TEAL, w=1.8, arrow=True, marker="ah-accent"))
    b.append(text(316, 106, "push", 10, 700, fill=TEAL))
    b.append(line(96, 130, 96, 96, stroke=TEAL, w=1.8, arrow=True, marker="ah-accent"))
    b.append(text(70, 106, "pop", 10, 700, fill=TEAL))
    b.append(text(192, 284, "both happen at the same end, the top", 10, 500, fill=MUTED))

    b.append(box(390, 34, 356, 258, None, fill="var(--dg-fill-2)", stroke=LILAC, r=12))
    b.append(text(568, 58, "QUEUE", 12, 700, fill=LILAC))
    b.append(text(568, 76, "first in, first out", 10, 450, fill=MUTED))
    for i, v in enumerate(["A", "B", "C", "D"]):
        x = 424 + i * 74
        edge = i in (0, 3)
        b.append(box(x, 150, 66, 60, v, fill=LILAC_SOFT if edge else FILL,
                     stroke=LILAC if edge else LINE, r=6, label_size=14,
                     text_fill=LILAC if edge else "var(--dg-text)"))
    b.append(text(457, 130, "front", 9, 700, fill=LILAC))
    b.append(text(679, 130, "back", 9, 700, fill=LILAC))
    b.append(line(457, 236, 457, 216, stroke=LILAC, w=1.8, arrow=True, marker="ah-alt"))
    b.append(text(457, 252, "dequeue", 10, 700, fill=LILAC))
    b.append(line(679, 236, 679, 216, stroke=LILAC, w=1.8, arrow=True, marker="ah-alt"))
    b.append(text(679, 252, "enqueue at the back", 10, 700, fill=LILAC))
    b.append(text(568, 284, "items leave in the order they arrived", 10, 500, fill=MUTED))

    desc = ("Two abstract data structures compared. A stack holds A at the bottom, then B, "
            "then C, with D on top. Both operations act on the top: push adds a new item "
            "onto the top and pop removes the top item, so the last item pushed is the "
            "first one popped. That is why a stack is called last in, first out, and why "
            "it suits undo history and the call stack. A queue holds A at the front, then "
            "B, C and D at the back. Enqueue adds a new item at the back and dequeue "
            "removes the item at the front, so items leave in the order they arrived. That "
            "is why a queue is called first in, first out, and why it suits print jobs and "
            "keyboard buffers.")
    return figure("sq", 760, 302, "".join(b),
                  "A stack compared with a queue", desc,
                  "A stack needs one pointer, to the top. A queue needs two, to the front "
                  "and to the back.")


# ========================================================= 17. Karnaugh map

@diagram("karnaugh-map")
def _kmap():
    b = []
    b.append(text(380, 26, "Q = A'B'C'D' + A'BC'D' + ABC'D' + ABC'D + ABCD + AB'C'D'",
                  11, 620, fill=MUTED))
    cw, ch = 74, 52
    ox, oy = 250, 78
    cols = ["00", "01", "11", "10"]
    rows = ["00", "01", "11", "10"]
    grid = [
        [1, 0, 0, 0],
        [1, 0, 0, 0],
        [1, 1, 1, 0],
        [1, 0, 0, 0],
    ]
    b.append(text(ox - 14, oy - 26, "CD", 11, 700, anchor="end", fill=MUTED))
    b.append(text(ox - 14, oy - 10, "AB", 11, 700, anchor="end", fill=MUTED))
    b.append(line(ox - 62, oy - 34, ox - 6, oy - 2, stroke=LINE, w=1))
    for c, lbl in enumerate(cols):
        b.append(text(ox + c * cw + cw / 2.0, oy - 12, lbl, 11, 700, mono=True, fill=MUTED))
    for r, lbl in enumerate(rows):
        b.append(text(ox - 16, oy + r * ch + ch / 2.0 + 4, lbl, 11, 700, mono=True,
                      anchor="end", fill=MUTED))
    for r in range(4):
        for c in range(4):
            v = grid[r][c]
            b.append(box(ox + c * cw, oy + r * ch, cw, ch, str(v),
                         fill=TEAL_SOFT if v else FILL, stroke=LINE, r=0,
                         label_size=16, text_fill=TEAL if v else MUTED))

    b.append(box(ox - 7, oy - 7, cw + 14, 4 * ch + 14, None, fill="none", stroke=TEAL,
                 r=12))
    b.append(box(ox + cw - 5, oy + 2 * ch - 5, 2 * cw + 10, ch + 10, None, fill="none",
                 stroke=LILAC, r=12))

    b.append(chip(140, 130, "group of 4", TEAL_SOFT, TEAL, TEAL))
    b.append(text(140, 154, "C and D are both 0", 10, 500, fill=MUTED))
    b.append(text(140, 170, "in all four cells,", 10, 500, fill=MUTED))
    b.append(text(140, 186, "and A and B change,", 10, 500, fill=MUTED))
    b.append(text(140, 202, "so the term is C'D'", 10, 700, fill=TEAL))

    b.append(chip(640, 200, "group of 2", LILAC_SOFT, LILAC, LILAC))
    b.append(text(640, 224, "A, B and D are all 1", 10, 500, fill=MUTED))
    b.append(text(640, 240, "in both cells, and C", 10, 500, fill=MUTED))
    b.append(text(640, 256, "changes, so the term", 10, 500, fill=MUTED))
    b.append(text(640, 272, "is A.B.D", 10, 700, fill=LILAC))

    b.append(text(380, 316, "Q = C'D' + A.B.D", 16, 700, fill=TEAL))
    desc = ("A four variable Karnaugh map with AB down the side and CD across the top, "
            "both labelled in Gray code order 00, 01, 11, 10 so that neighbouring cells "
            "differ in only one variable. The map holds a 1 in the whole of the CD equals "
            "00 column, that is at AB 00, 01, 11 and 10, and also at AB equals 11 with CD "
            "equals 01 and CD equals 11. All other cells hold 0. The first group is the "
            "column of four cells: C and D are 0 in every one of them while A and B change, "
            "so that group simplifies to C NOT AND D NOT, written C'D'. The second group is "
            "the pair of cells in the AB equals 11 row at CD 01 and 11: A, B and D are 1 in "
            "both while C changes, so that group simplifies to A AND B AND D. The simplified "
            "expression is therefore Q equals C'D' plus A B D.")
    return figure("kmap", 760, 340, "".join(b),
                  "Simplifying a Boolean expression with a Karnaugh map", desc,
                  "Groups must be rectangles of 1, 2, 4, 8 or 16 cells, may wrap around the "
                  "edges, and may overlap. Bigger groups give shorter terms.")


# =================================================== 18. Client server vs P2P

@diagram("client-server-p2p")
def _csp2p():
    b = []
    for ox, title, col in ((14, "CLIENT SERVER", TEAL), (390, "PEER TO PEER", LILAC)):
        b.append(box(ox, 34, 356, 250, None, fill="var(--dg-fill-2)", stroke=col, r=12))
        b.append(text(ox + 178, 58, title, 12, 700, fill=col))

    clients = [(60, 200), (152, 200), (244, 200)]
    for cx, cy in clients:
        b.append(line(cx + 28, cy, 192, 132, stroke=TEAL, w=1.6))
    b.append(box(132, 96, 120, 52, "Server", "holds the files", fill=TEAL_SOFT,
                 stroke=TEAL, r=8, text_fill=TEAL))
    for i, (cx, cy) in enumerate(clients):
        b.append(box(cx, cy, 56, 44, "Client", fill=FILL, stroke=LINE, r=6,
                     label_size=10))
        b.append(text(cx + 28, cy + 58, str(i + 1), 10, 700, fill=MUTED))
    b.append(text(192, 274, "one machine serves them all, and is a single point of failure",
                  10, 500, fill=MUTED))

    peers = [(490, 110), (646, 110), (490, 214), (646, 214)]
    for i in range(4):
        for j in range(i + 1, 4):
            b.append(line(peers[i][0] + 28, peers[i][1] + 22,
                          peers[j][0] + 28, peers[j][1] + 22, stroke=LILAC, w=1.4))
    for px, py in peers:
        b.append(box(px, py, 56, 44, "Peer", fill=LILAC_SOFT, stroke=LILAC, r=6,
                     label_size=10, text_fill=LILAC))
    b.append(text(568, 274, "every machine is both client and server, so nothing is central",
                  10, 500, fill=MUTED))

    desc = ("Two network models side by side. In a client server network three client "
            "machines each connect to one central server which holds the files, runs the "
            "backups and controls the accounts. Management and security are centralised, "
            "which is easier to administer, but the server is a single point of failure "
            "and can become a bottleneck when many clients ask for data at once. In a peer "
            "to peer network four machines are joined directly to one another and every "
            "machine acts as both a client and a server, sharing its own files. There is "
            "no central point to fail and it is cheap to set up, but backups, security and "
            "finding files are all harder because nothing is centralised.")
    return figure("csp2p", 760, 294, "".join(b),
                  "Client server networks compared with peer to peer networks", desc,
                  "Schools and businesses use client server for control. File sharing and "
                  "blockchain use peer to peer because there is no central point to attack.")


# ======================================================== 19. Sound sampling

@diagram("sound-sampling")
def _sound():
    import math
    b = []
    ox, oy, w, h = 70, 50, 620, 190
    mid = oy + h / 2.0
    b.append(line(ox, mid, ox + w, mid, stroke="var(--dg-line-soft)", w=1))
    b.append(line(ox, oy, ox, oy + h, stroke=LINE, w=1.4))
    b.append(text(ox - 12, oy + 10, "loud", 9, 620, anchor="end", fill=MUTED))
    b.append(text(ox - 12, oy + h, "quiet", 9, 620, anchor="end", fill=MUTED))
    b.append(text(ox + w / 2.0, oy + h + 22, "time", 9, 620, fill=MUTED))

    def wave(t):
        return mid - (math.sin(t * 2 * math.pi * 1.6) * 0.36
                      + math.sin(t * 2 * math.pi * 3.4) * 0.13) * h

    pts = ["%.1f %.1f" % (ox + w * (i / 240.0), wave(i / 240.0)) for i in range(241)]
    b.append(path("M" + " L".join(pts), stroke=LILAC, w=2))

    n = 16
    levels = 8
    step = h / float(levels)
    prev = None
    for i in range(n + 1):
        t = i / float(n)
        x = ox + w * t
        yv = wave(t)
        q = oy + round((yv - oy) / step) * step
        b.append(line(x, mid, x, yv, stroke="var(--dg-line-soft)", w=1, dash="3 3"))
        b.append(circle(x, yv, 3.5, fill=TEAL, stroke=TEAL, w=1))
        if prev is not None:
            b.append(line(prev[0], prev[1], x, prev[1], stroke=TEAL, w=1.6))
            b.append(line(x, prev[1], x, q, stroke=TEAL, w=1.6))
        prev = (x, q)
    b.append(line(prev[0], prev[1], ox + w, prev[1], stroke=TEAL, w=1.6))

    b.append(box(70, 276, 300, 62, None, fill=TEAL_SOFT, stroke=TEAL, r=8))
    b.append(text(86, 296, "Sample rate", 11, 700, anchor="start", fill=TEAL))
    b.append(text(86, 314, "how many samples per second, in hertz.", 10, 450,
                  anchor="start", fill=MUTED))
    b.append(text(86, 330, "More samples means more detail across time.", 10, 450,
                  anchor="start", fill=MUTED))
    b.append(box(390, 276, 300, 62, None, fill=LILAC_SOFT, stroke=LILAC, r=8))
    b.append(text(406, 296, "Bit depth", 11, 700, anchor="start", fill=LILAC))
    b.append(text(406, 314, "bits stored per sample, so 8 bits gives 256 levels.",
                  10, 450, anchor="start", fill=MUTED))
    b.append(text(406, 330, "More bits means each height is recorded more exactly.",
                  10, 450, anchor="start", fill=MUTED))
    b.append(text(380, 360, "file size in bits = sample rate x bit depth x seconds x channels",
                  11, 700, fill=TEAL))

    desc = ("A smooth analogue sound wave drawn as a continuous curve, with sampling shown "
            "on top of it. At sixteen evenly spaced moments the height of the wave is "
            "measured, marked by dots on the curve, and each measured height is rounded to "
            "the nearest of the available levels. Joining those rounded values produces a "
            "staircase that follows the curve but is not identical to it, and the "
            "difference between the staircase and the curve is the loss caused by "
            "digitising. Taking samples more often, a higher sample rate measured in hertz, "
            "makes the staircase steps narrower. Storing more bits per sample, a higher bit "
            "depth, gives more possible levels, so eight bits gives 256 levels and each "
            "step lands closer to the true height. Both improvements make the recording "
            "closer to the original and both make the file bigger. File size in bits equals "
            "sample rate times bit depth times length in seconds times number of channels.")
    return figure("sound", 760, 376, "".join(b),
                  "Sampling an analogue sound wave into digital data", desc,
                  "Sample rate is how often you measure. Bit depth is how precisely you "
                  "record each measurement. Examiners want both named, not just one.")


# ================================================= 20. Image representation

@diagram("image-representation")
def _image():
    b = []
    b.append(text(20, 28, "An 8 by 8 image, one bit per pixel", 12, 700, anchor="start",
                  fill=TEAL))
    grid = [
        "00111100",
        "01000010",
        "10100101",
        "10000001",
        "10100101",
        "10011001",
        "01000010",
        "00111100",
    ]
    cs = 26
    ox, oy = 30, 44
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            on = ch == "1"
            b.append(box(ox + c * cs, oy + r * cs, cs, cs, None,
                         fill="var(--dg-ink)" if on else "var(--dg-paper)",
                         stroke="var(--dg-line-soft)", r=0))
    b.append(text(ox + 4 * cs, oy + 8 * cs + 20, "the picture", 10, 500, fill=MUTED))

    ox2 = 268
    for r, row in enumerate(grid):
        b.append(text(ox2, oy + r * cs + cs / 2.0 + 4, "  ".join(row), 12, 620,
                      anchor="start", mono=True, fill=LILAC))
    b.append(text(ox2 + 92, oy + 8 * cs + 20, "the same thing, stored as bits", 10, 500,
                  fill=MUTED))

    px, py = 470, 44
    b.append(box(px, py, 274, 78, None, fill=TEAL_SOFT, stroke=TEAL, r=8))
    b.append(text(px + 16, py + 22, "Resolution", 11, 700, anchor="start", fill=TEAL))
    b.append(text(px + 16, py + 40, "how many pixels across by how many", 10, 450,
                  anchor="start", fill=MUTED))
    b.append(text(px + 16, py + 56, "down. Here 8 x 8, so 64 pixels.", 10, 450,
                  anchor="start", fill=MUTED))

    b.append(box(px, py + 92, 274, 78, None, fill=LILAC_SOFT, stroke=LILAC, r=8))
    b.append(text(px + 16, py + 114, "Colour depth", 11, 700, anchor="start", fill=LILAC))
    b.append(text(px + 16, py + 132, "bits per pixel. 1 bit gives 2 colours,", 10, 450,
                  anchor="start", fill=MUTED))
    b.append(text(px + 16, py + 148, "8 gives 256, 24 gives 16.7 million.", 10, 450,
                  anchor="start", fill=MUTED))

    b.append(box(px, py + 184, 274, 62, None, fill="var(--dg-fill-2)", stroke=LINE, r=8))
    b.append(text(px + 16, py + 206, "Metadata", 11, 700, anchor="start", fill=MUTED))
    b.append(text(px + 16, py + 224, "width, height, colour depth, date,", 10, 450,
                  anchor="start", fill=MUTED))
    b.append(text(px + 16, py + 240, "so the file can be opened correctly.", 10, 450,
                  anchor="start", fill=MUTED))

    b.append(text(380, 300, "file size in bits = width x height x colour depth, "
                  "then add the metadata", 11, 700, fill=TEAL))
    desc = ("An eight by eight bitmap image of a simple face shown next to the binary that "
            "stores it. Each square of the picture is one pixel, and because this image "
            "uses one bit per pixel each pixel is either 0 for the background or 1 for the "
            "ink. The eight rows of bits are 00111100, 01000010, 10100101, 10000001, "
            "10100101, 10011001, 01000010 and 00111100. Three properties decide the file. "
            "Resolution is how many pixels across by how many down, here eight by eight, "
            "giving 64 pixels in total. Colour depth is how many bits are stored per "
            "pixel: one bit gives two colours, eight bits gives 256 colours and 24 bits "
            "gives about 16.7 million. Metadata is the extra information stored with the "
            "image, such as width, height, colour depth and date, so that software can "
            "open it correctly. File size in bits equals width times height times colour "
            "depth, plus the metadata.")
    return figure("image", 760, 322, "".join(b),
                  "How a bitmap image is stored, and what decides its size", desc,
                  "Increasing colour depth by one bit doubles the number of available "
                  "colours and adds one bit to every single pixel.")


# ====================================================== 21. Binary addition

@diagram("binary-addition")
def _addition():
    b = []
    b.append(text(380, 26, "Adding two 8 bit numbers, and what overflow means",
                  12, 700, fill=TEAL))
    cw = 42
    ox = 232
    rows = [
        ("carry", "1 1 1 1 1       ", MUTED, None),
        ("", "0 1 1 0 1 1 0 1", "var(--dg-text)", "109"),
        ("+", "0 0 1 1 0 1 1 0", "var(--dg-text)", "54"),
        ("=", "1 0 1 0 0 0 1 1", TEAL, "163"),
    ]
    for r, (lbl, bits, col, dec) in enumerate(rows):
        y = 62 + r * 44
        if lbl:
            b.append(text(ox - 24, y + 20, lbl, 11, 700, anchor="end", fill=MUTED))
        parts = bits.split(" ")
        for i, ch in enumerate(parts):
            if ch.strip() == "":
                continue
            b.append(text(ox + i * cw + cw / 2.0, y + 24, ch, 18, 700, mono=True, fill=col))
        if dec:
            b.append(text(ox + 8 * cw + 26, y + 22, "= %s" % dec, 12, 620, anchor="start",
                          fill=MUTED))
    b.append(line(ox, 190, ox + 8 * cw, 190, stroke=LINE, w=1.4))

    b.append(box(60, 250, 320, 92, None, fill=TEAL_SOFT, stroke=TEAL, r=8))
    b.append(text(78, 274, "The four rules", 11, 700, anchor="start", fill=TEAL))
    b.append(text(78, 294, "0 + 0 = 0        1 + 0 = 1", 11, 620, anchor="start", mono=True))
    b.append(text(78, 312, "1 + 1 = 0 carry 1", 11, 620, anchor="start", mono=True))
    b.append(text(78, 330, "1 + 1 + 1 = 1 carry 1", 11, 620, anchor="start", mono=True))

    b.append(box(400, 250, 300, 92, None, fill=WARN_SOFT, stroke=WARN, r=8))
    b.append(text(418, 274, "Overflow", 11, 700, anchor="start", fill=WARN))
    b.append(text(418, 294, "If a carry comes out of the leftmost", 10, 450,
                  anchor="start", fill=MUTED))
    b.append(text(418, 310, "column there is no ninth bit to hold it,", 10, 450,
                  anchor="start", fill=MUTED))
    b.append(text(418, 326, "so the answer stored is wrong.", 10, 450,
                  anchor="start", fill=MUTED))

    desc = ("A worked binary addition set out in columns. The first number is 01101101, "
            "which is 109 in denary. The second is 00110110, which is 54. Working from the "
            "right, the four rules are that 0 plus 0 is 0, 1 plus 0 is 1, 1 plus 1 is 0 "
            "carry 1, and 1 plus 1 plus 1 is 1 carry 1. Carries of 1 are generated in four "
            "of the columns. The result is 10100011, which is 163 in denary, and 109 plus "
            "54 does equal 163. Overflow happens when a carry comes out of the leftmost "
            "column: with only eight bits available there is no ninth bit to hold it, so "
            "the carry is lost and the stored answer is wrong.")
    return figure("addition", 760, 358, "".join(b),
                  "Binary addition with carries, and overflow", desc,
                  "Always write the carry row above the columns. Losing a carry off the "
                  "left hand end is overflow, and it is a favourite exam question.")
