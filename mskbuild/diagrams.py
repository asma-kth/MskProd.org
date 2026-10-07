"""Inline SVG diagrams for the revision site.

Each entry in REGISTRY is a callable returning a complete <figure>. Diagrams are
embedded in topic content with the `!diagram <name>` markup directive. Every one
carries a <title> and a full <desc>, so a screen reader user receives the same
information the picture conveys rather than being told an image exists.
"""
from .svg import (figure, figure_steps, step, box, text, line, path, circle, chip, esc)

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
    """The cycle, one stage at a time.

    A static picture of three boxes does not show the one thing that matters,
    which is that control returns to fetch and goes round again. Stepping
    through it makes the loop the point rather than a footnote.
    """
    # Drawn on every stage: the CPU, memory, and the buses between them.
    base = [
        box(28, 54, 300, 180, None, fill="var(--dg-fill-2)", stroke=LINE, r=12),
        text(178, 76, "CENTRAL PROCESSING UNIT", 11, 700, fill=MUTED),
        box(46, 92, 128, 30, "PC", fill=FILL, stroke=LINE, label_size=12),
        box(186, 92, 128, 30, "MAR", fill=FILL, stroke=LINE, label_size=12),
        box(46, 132, 128, 30, "MDR", fill=FILL, stroke=LINE, label_size=12),
        box(186, 132, 128, 30, "CIR", fill=FILL, stroke=LINE, label_size=12),
        box(46, 180, 268, 36, "Control Unit  +  ALU", fill=FILL, stroke=LINE, label_size=12),
        box(470, 92, 240, 124, None, fill="var(--dg-fill-2)", stroke=LINE, r=12),
        text(590, 114, "MAIN MEMORY", 11, 700, fill=MUTED),
        box(488, 128, 204, 30, "0x04A  ADD 12", fill=FILL, stroke=LINE, label_size=11),
        box(488, 166, 204, 30, "0x04B  STA 20", fill=FILL, stroke=LINE, label_size=11),
        # Faint rails so the bus labels have something to sit against on every
        # stage; the live arrows are drawn over them when that stage runs.
        line(328, 128, 470, 128, stroke="var(--dg-line-soft)", w=2),
        line(328, 180, 470, 180, stroke="var(--dg-line-soft)", w=2),
        text(399, 120, "address bus", 10, 500, fill=MUTED),
        text(399, 204, "data bus", 10, 500, fill=MUTED),
    ]
    L = [
        "Fetch: the address in the program counter is copied into the MAR.",
        "Fetch: the program counter is incremented, ready for the next instruction.",
        "Fetch: the address travels out on the address bus to main memory.",
        "Fetch: the instruction returns on the data bus into the MDR, then the CIR.",
        "Decode: the control unit splits the instruction into an opcode and an operand.",
        "Execute: the instruction is carried out and any result lands in the accumulator.",
        "And back to fetch. A 3 GHz processor does this about three billion times a second.",
    ]
    def hl(x, y, w, h, c=TEAL):
        return box(x, y, w, h, None, fill="none", stroke=c, r=8)
    steps = [
        step(1, hl(46, 92, 128, 30) + hl(186, 92, 128, 30)
             + line(174, 107, 186, 107, stroke=TEAL, w=2.4, arrow=True, marker="ah-accent")
             + text(178, 300, "PC  \u2192  MAR", 13, 700, fill=TEAL), L[0]),
        step(2, hl(46, 92, 128, 30)
             + text(110, 300, "PC = PC + 1", 13, 700, fill=TEAL), L[1]),
        step(3, hl(186, 92, 128, 30)
             + '<line x1="328" y1="128" x2="470" y2="128" stroke="%s" stroke-width="2.4" '
               'marker-end="url(#ah-accent)" class="dg-flow"/>' % TEAL
             + text(399, 300, "address out on the address bus", 12, 650, fill=TEAL), L[2]),
        step(4, hl(46, 132, 128, 30) + hl(186, 132, 128, 30) + hl(488, 128, 204, 30)
             + '<line x1="470" y1="180" x2="328" y2="180" stroke="%s" stroke-width="2.4" '
               'marker-end="url(#ah-accent)" class="dg-flow"/>' % TEAL
             + text(399, 300, "instruction back on the data bus  \u2192  MDR  \u2192  CIR",
                    12, 650, fill=TEAL), L[3]),
        step(5, hl(186, 132, 128, 30, LILAC) + hl(46, 180, 268, 36, LILAC)
             + text(178, 300, "opcode  +  operand", 13, 700, fill=LILAC), L[4]),
        step(6, hl(46, 180, 268, 36)
             + text(178, 300, "carry it out, update the flags", 12, 650, fill=TEAL), L[5]),
        step(7, path("M60 232 L60 282 L300 282", stroke=TEAL, w=2.2, dash="5 4",
                     arrow=True, marker="ah-accent")
             + text(420, 300, "repeat", 13, 700, fill=TEAL), L[6]),
    ]
    desc = ("A seven stage walk through the fetch decode execute cycle. In fetch, the "
            "address in the program counter is copied into the memory address register, "
            "the program counter is incremented, the address travels out on the address "
            "bus to main memory, and the instruction returns on the data bus into the "
            "memory data register and then the current instruction register. In decode, "
            "the control unit splits that instruction into an opcode saying which "
            "operation to perform and an operand giving the data or its address. In "
            "execute, the instruction is carried out and any result from the arithmetic "
            "logic unit is placed in the accumulator with the status flags updated. "
            "Control then returns to fetch and the whole cycle repeats, around three "
            "billion times a second on a 3 gigahertz processor.")
    return figure_steps("fde", 760, 320, "".join(base), steps,
                        "The fetch decode execute cycle", desc,
                        "Step through the cycle. Naming the registers and buses in this "
                        "order is what turns a one mark answer into a full mark one.",
                        labels=L)


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


# ================================================= 22. Computational thinking

@diagram("computational-thinking")
def _ct():
    """The three pillars applied to one concrete problem.

    Taught abstractly these three words are indistinguishable to most students.
    Walking one real problem through each pillar is what separates them.
    """
    base = [
        box(24, 48, 712, 44, None, fill="var(--dg-fill-2)", stroke=LINE, r=10),
        text(380, 76, "Problem: write a program that marks a class set of quizzes",
             13, 650, fill="var(--dg-text)"),
    ]
    L = [
        "Decomposition: break the problem into parts small enough to solve one at a time.",
        "Abstraction: strip out the detail that does not affect the result.",
        "Algorithmic thinking: write the steps down in an order a computer can follow.",
    ]
    cols = [
        ("DECOMPOSITION", TEAL, TEAL_SOFT,
         ["Read the answers from a file", "Compare each one to the key",
          "Count the marks", "Work out a grade", "Write a report"]),
        ("ABSTRACTION", LILAC, LILAC_SOFT,
         ["Keep: the answer given", "Keep: the correct answer",
          "Ignore: the pupil's handwriting", "Ignore: how long they took",
          "Ignore: the paper colour"]),
        ("ALGORITHM", TEAL, TEAL_SOFT,
         ["FOR each pupil", "  score = 0", "  FOR each question",
          "    IF answer = key THEN", "      score = score + 1"]),
    ]
    steps = []
    for n, (title, accent, soft, items) in enumerate(cols, start=1):
        x = 24 + (n - 1) * 244
        body = [
            box(x, 116, 228, 186, None, fill=FILL, stroke=accent, r=10),
            box(x, 116, 228, 32, None, fill=soft, stroke=accent, r=10),
            text(x + 114, 137, title, 11, 700, fill=accent),
            _lines(x + 14, 172, items, size=11, gap=24,
                   fill="var(--dg-text)" if n != 3 else "var(--dg-text)"),
        ]
        if n > 1:
            body.append(line(x - 14, 209, x - 2, 209, stroke=LINE, arrow=True))
        steps.append(step(n, "".join(body), L[n - 1]))
    desc = ("Computational thinking applied to one problem, marking a class set of "
            "quizzes. Decomposition breaks it into parts: read the answers from a file, "
            "compare each one to the key, count the marks, work out a grade and write a "
            "report. Abstraction decides what matters and what does not: keep the answer "
            "given and the correct answer, ignore the pupil's handwriting, how long they "
            "took and the colour of the paper. Algorithmic thinking then writes the steps "
            "in an order a computer can follow, looping over each pupil and each question "
            "and adding one to the score whenever the answer matches the key.")
    return figure_steps("ct", 760, 320, "".join(base), steps,
                        "Computational thinking applied to one problem", desc,
                        "The three pillars on a single problem. In an exam, name the "
                        "pillar and then show it doing something to the problem in front "
                        "of you; naming it alone rarely scores.",
                        labels=L)


# ============================================= 23. UK computing law

@diagram("uk-computing-law")
def _law():
    """The four Acts, each with the thing it actually prohibits.

    Students lose marks by naming the right Act for the wrong offence, so each
    card leads with the offence rather than the title.
    """
    base = [text(380, 36, "Which Act covers which offence", 12, 650, fill=MUTED)]
    acts = [
        ("Computer Misuse Act 1990", TEAL, TEAL_SOFT,
         ["Unauthorised access to a computer", "Access with intent to commit a crime",
          "Unauthorised changes to data", "Making or supplying hacking tools"],
         "Hacking, planting malware, using\\nsomebody else's login"),
        ("Data Protection Act 2018 / UK GDPR", LILAC, LILAC_SOFT,
         ["Data used fairly and lawfully", "Collected for a stated purpose",
          "Kept accurate and no longer than needed", "Kept secure, and the right to see it"],
         "How an organisation must handle\\npersonal data about living people"),
        ("Copyright, Designs and Patents Act 1988", TEAL, TEAL_SOFT,
         ["Protects original work automatically", "Covers code, music, images, text",
          "Lasts the author's life plus 70 years", "Breached by copying or sharing it"],
         "Piracy, using an image without\\na licence, copying source code"),
        ("Freedom of Information Act 2000", LILAC, LILAC_SOFT,
         ["A right to ask public bodies for data", "Councils, schools, the NHS, police",
          "They must reply within 20 working days", "Personal data is exempt"],
         "Asking a public body what it holds,\\nnot a private company"),
    ]
    L = [a[0] for a in acts]
    steps = []
    for n, (title, accent, soft, points, when) in enumerate(acts, start=1):
        body = [
            box(60, 56, 640, 226, None, fill=FILL, stroke=accent, r=12),
            box(60, 56, 640, 40, None, fill=soft, stroke=accent, r=12),
            text(380, 82, title, 13, 700, fill=accent),
            _lines(96, 132, points, size=12, gap=26),
            line(96, 232, 664, 232, stroke="var(--dg-line-soft)", w=1),
        ]
        # Two lines of context sit inside the card, so they must clear its
        # lower border at y = 282 rather than straddle it.
        for i, ln in enumerate(when.split("\\n")):
            body.append(text(380, 252 + i * 16, ln, 11, 500, fill=MUTED))
        steps.append(step(n, "".join(body), title))
    desc = ("Four Acts of UK law that apply to computing. The Computer Misuse Act 1990 "
            "covers unauthorised access to a computer, access with intent to commit a "
            "further offence, unauthorised changes to data, and making or supplying "
            "hacking tools; it is the Act for hacking, malware and using somebody else's "
            "login. The Data Protection Act 2018 and UK GDPR govern how organisations "
            "handle personal data about living people, requiring it to be used fairly and "
            "lawfully, collected for a stated purpose, kept accurate and no longer than "
            "needed, kept secure, and made available to the person it is about. The "
            "Copyright, Designs and Patents Act 1988 protects original work automatically, "
            "including code, music, images and text, for the author's life plus seventy "
            "years, and is breached by copying or sharing without permission. The Freedom "
            "of Information Act 2000 gives a right to ask public bodies such as councils, "
            "schools, the NHS and the police for the information they hold, with a reply "
            "due within twenty working days, though personal data is exempt.")
    return figure_steps("law", 760, 300, "".join(base), steps,
                        "The four Acts that cover computing in the UK", desc,
                        "Step through the four Acts. Most marks are lost by naming the "
                        "right Act for the wrong offence, so learn these by the offence "
                        "rather than by the title.",
                        labels=L)


# ============================================ 24. Character encoding

@diagram("character-encoding")
def _charset():
    """From a keypress to the bits actually stored."""
    base = [
        text(380, 34, 'Storing the text  "Hi"', 12, 650, fill=MUTED),
    ]
    L = [
        "Every character has a number. In ASCII, capital H is 72 and lower case i is 105.",
        "That number is written in binary. ASCII uses 7 bits, usually stored in one byte.",
        "So two characters take two bytes. Text size is simply characters times bytes each.",
        "ASCII has only 128 codes, so Unicode extends the same idea to every writing system.",
    ]
    def cell(x, y, w, h, v, accent=TEAL, soft=TEAL_SOFT, sub=None, mono=True):
        o = [box(x, y, w, h, None, fill=soft, stroke=accent, r=6),
             '<text x="%s" y="%s" text-anchor="middle" font-size="14" font-weight="650" '
             'fill="%s" class="dg-mono">%s</text>' % (x + w / 2, y + h / 2 + 5, accent, esc(v))]
        if sub: o.append(text(x + w / 2, y + h + 16, sub, 10, 500, fill=MUTED))
        return "".join(o)
    steps = [
        step(1, cell(250, 70, 110, 56, "H", TEAL, TEAL_SOFT, "character")
             + cell(400, 70, 110, 56, "i", LILAC, LILAC_SOFT, "character")
             + line(305, 140, 305, 176, stroke=LINE, arrow=True)
             + line(455, 140, 455, 176, stroke=LINE, arrow=True)
             + cell(250, 182, 110, 50, "72", TEAL, FILL, "ASCII code")
             + cell(400, 182, 110, 50, "105", LILAC, FILL, "ASCII code"), L[0]),
        step(2, cell(250, 70, 110, 50, "72", TEAL, FILL)
             + cell(400, 70, 110, 50, "105", LILAC, FILL)
             + line(305, 134, 305, 170, stroke=LINE, arrow=True)
             + line(455, 134, 455, 170, stroke=LINE, arrow=True)
             + cell(214, 176, 182, 50, "01001000", TEAL, TEAL_SOFT, "8 bits")
             + cell(410, 176, 182, 50, "01101001", LILAC, LILAC_SOFT, "8 bits"), L[1]),
        step(3, cell(214, 100, 182, 54, "01001000", TEAL, TEAL_SOFT, "1 byte")
             + cell(410, 100, 182, 54, "01101001", LILAC, LILAC_SOFT, "1 byte")
             + box(214, 196, 378, 46, None, fill=FILL, stroke=LINE, r=8)
             + text(403, 224, "2 characters  x  1 byte  =  2 bytes", 13, 650, fill="var(--dg-text)"), L[2]),
        step(4, box(120, 86, 240, 150, None, fill=FILL, stroke=TEAL, r=10)
             + text(240, 112, "ASCII", 13, 700, fill=TEAL)
             + _lines(142, 142, ["7 bits, 128 codes", "English letters,", "digits, punctuation"], 11, 24)
             + box(400, 86, 240, 150, None, fill=FILL, stroke=LILAC, r=10)
             + text(520, 112, "UNICODE", 13, 700, fill=LILAC)
             + _lines(422, 142, ["Up to 32 bits", "Over 140,000 codes", "Every writing system,"
                                 ], 11, 24)
             + text(422, 214, "plus emoji", 11, 450, anchor="start", fill="var(--dg-text)")
             + line(366, 160, 394, 160, stroke=LINE, arrow=True), L[3]),
    ]
    desc = ("How text is stored. Each character is given a number by a character set: in "
            "ASCII, capital H is 72 and lower case i is 105. That number is then written "
            "in binary, so H becomes 01001000 and i becomes 01101001. ASCII uses seven "
            "bits and is normally stored in one byte per character, so the two character "
            "string Hi takes two bytes, and the size of any text is simply the number of "
            "characters multiplied by the bytes used for each. ASCII has only 128 codes, "
            "enough for English letters, digits and punctuation, so Unicode extends the "
            "same idea with up to 32 bits and over 140,000 codes, covering every writing "
            "system in use as well as emoji.")
    return figure_steps("charset", 760, 266, "".join(base), steps,
                        "From a character to the bits stored", desc,
                        "A character set is only a lookup table from characters to "
                        "numbers. Everything else follows from that one idea.",
                        labels=L)


# ================================================ 25. Pre-production documents

@diagram("imedia-pre-production")
def _imedia_preprod():
    """The four documents students most often confuse, actually drawn.

    Describing a wireframe in words sounds exactly like describing a
    visualisation diagram. Seeing one of each, side by side, is the only
    reliable way to stop the two being swapped in an exam.
    """
    base = [text(380, 30, "The four planning documents, and what each one looks like",
                 12, 650, fill=MUTED)]

    def frame(x, y, w, h, label, accent=TEAL):
        return (box(x, y, w, h, None, fill=FILL, stroke=accent, r=6)
                + text(x + w / 2, y + h + 16, label, 10, 550, fill=MUTED))

    # 1. Visualisation diagram: one static page, annotated.
    vis = [box(250, 60, 190, 170, None, fill=FILL, stroke=TEAL, r=8),
           box(268, 76, 154, 54, None, fill=TEAL_SOFT, stroke=TEAL, r=4),
           text(345, 107, "MASTHEAD", 11, 650, fill=TEAL),
           box(268, 140, 70, 54, None, fill="var(--dg-fill-2)", stroke=LINE, r=4),
           text(303, 171, "image", 10, 500, fill=MUTED)]
    for i in range(4):
        vis.append(line(350, 148 + i * 13, 420, 148 + i * 13, stroke=LINE, w=2))
    vis += [line(440, 103, 492, 103, stroke=LILAC, w=1.2, dash="3 3"),
            text(498, 107, "colour, font, size", 10, 500, anchor="start", fill=LILAC),
            line(250, 167, 198, 167, stroke=LILAC, w=1.2, dash="3 3"),
            text(192, 171, "image source", 10, 500, anchor="end", fill=LILAC),
            text(345, 248, "ONE static page, annotated", 11, 650, fill=TEAL)]

    # 2. Storyboard: a sequence of frames, in time order.
    sb = []
    shots = [("WS", "pan left"), ("MS", "cut"), ("CU", "2 sec"), ("WS", "fade out")]
    for i, (shot, note) in enumerate(shots):
        x = 60 + i * 168
        sb.append(box(x, 70, 140, 92, None, fill=FILL, stroke=LILAC, r=6))
        sb.append(text(x + 70, 108, shot, 15, 700, fill=LILAC))
        sb.append(text(x + 70, 128, note, 10, 500, fill=MUTED))
        sb.append(text(x + 70, 180, "frame %d" % (i + 1), 10, 550, fill=MUTED))
        if i < 3:
            sb.append(line(x + 146, 116, x + 162, 116, stroke=LINE, arrow=True))
    sb.append(text(380, 232, "A SEQUENCE of shots in time order", 11, 650, fill=LILAC))
    sb.append(text(380, 250, "each frame annotated with shot type, movement and duration",
                   10, 500, fill=MUTED))

    # 3. Wireframe: screen layout, no styling at all.
    wf = [box(232, 60, 226, 170, None, fill=FILL, stroke=TEAL, r=8),
          box(244, 72, 202, 26, None, fill="var(--dg-fill-2)", stroke=LINE, r=3),
          text(345, 89, "nav", 10, 550, fill=MUTED),
          box(244, 106, 128, 70, None, fill="var(--dg-fill-2)", stroke=LINE, r=3),
          text(308, 145, "hero image", 10, 550, fill=MUTED),
          box(380, 106, 66, 70, None, fill="var(--dg-fill-2)", stroke=LINE, r=3),
          text(413, 145, "text", 10, 550, fill=MUTED),
          box(244, 184, 202, 34, None, fill="var(--dg-fill-2)", stroke=LINE, r=3),
          text(345, 205, "footer", 10, 550, fill=MUTED),
          text(345, 248, "ONE screen's layout, with NO styling", 11, 650, fill=TEAL),
          text(345, 266, "grey boxes on purpose: colour and font come later", 10, 500, fill=MUTED)]

    # 4. Navigation diagram: how the screens connect.
    nav = [box(320, 62, 120, 38, "Home", fill=TEAL_SOFT, stroke=TEAL, r=6, label_size=12)]
    kids = [("Gallery", 150), ("About", 320), ("Contact", 490)]
    for label, x in kids:
        nav.append(box(x, 142, 120, 38, label, fill=FILL, stroke=LILAC, r=6, label_size=12))
        nav.append(path("M380 100 L380 122 L%d 122 L%d 140" % (x + 60, x + 60),
                        stroke=LINE, arrow=True))
    nav += [box(150, 212, 120, 36, "Image page", fill=FILL, stroke=LINE, r=6, label_size=11),
            line(210, 180, 210, 210, stroke=LINE, arrow=True),
            text(380, 272, "EVERY screen and how they connect", 11, 650, fill=TEAL)]

    L = [
        "Visualisation diagram: one static product, sketched and annotated.",
        "Storyboard: a sequence of shots in time order, for anything that moves.",
        "Wireframe: the layout of a single screen, deliberately with no styling.",
        "Navigation diagram: every screen in the product and the routes between them.",
    ]
    steps = [step(1, "".join(vis), L[0]), step(2, "".join(sb), L[1]),
             step(3, "".join(wf), L[2]), step(4, "".join(nav), L[3])]
    desc = ("Four pre-production documents compared. A visualisation diagram is a sketch "
            "of one static product such as a poster or magazine page, annotated with "
            "colours, fonts, sizes and image sources. A storyboard is a sequence of "
            "frames showing shots in time order, each annotated with the shot type, "
            "camera movement and duration, and is used for anything that moves. A "
            "wireframe shows the layout of a single screen with no styling at all, which "
            "is why its boxes are plain grey: the colour and typography are decided "
            "later. A navigation diagram shows every screen in the product and the routes "
            "between them, so a home screen might lead to a gallery, an about page and a "
            "contact page, with the gallery leading on to individual image pages.")
    return figure_steps("imedia-pre", 760, 290, "".join(base), steps,
                        "Visualisation diagram, storyboard, wireframe and navigation diagram", desc,
                        "The three most swapped answers in the whole course. A "
                        "visualisation diagram is one static page, a storyboard is a "
                        "sequence over time, and a wireframe is one screen's layout with "
                        "the styling deliberately left out.",
                        labels=L)


# =================================================== 26. Production pipeline

@diagram("imedia-production-pipeline")
def _imedia_pipeline():
    """Who does what, and in which phase."""
    base = [
        text(380, 28, "One product, three phases, and the roles in each", 12, 650, fill=MUTED),
        box(40, 48, 220, 34, "PRE-PRODUCTION", fill="var(--dg-fill-2)", stroke=LINE, r=8, label_size=11),
        box(270, 48, 220, 34, "PRODUCTION", fill="var(--dg-fill-2)", stroke=LINE, r=8, label_size=11),
        box(500, 48, 220, 34, "POST-PRODUCTION", fill="var(--dg-fill-2)", stroke=LINE, r=8, label_size=11),
        line(262, 65, 268, 65, stroke=LINE, arrow=True),
        line(492, 65, 498, 65, stroke=LINE, arrow=True),
    ]
    phases = [
        (40, TEAL, TEAL_SOFT, "Plan it",
         ["Client sets the brief", "Producer plans budget", "Scriptwriter writes", "Storyboard artist draws"]),
        (270, LILAC, LILAC_SOFT, "Make it",
         ["Director decides", "Camera operator shoots", "Sound engineer records", "Designer builds assets"]),
        (500, TEAL, TEAL_SOFT, "Finish it",
         ["Video editor assembles", "Sound editor mixes", "VFX artist composites", "QA tester finds faults"]),
    ]
    L = ["Pre-production: everything decided before anything is made.",
         "Production: the assets are actually captured or built.",
         "Post-production: the pieces are assembled, polished and tested."]
    steps = []
    for n, (x, accent, soft, head, roles) in enumerate(phases, start=1):
        body = [box(x, 96, 220, 164, None, fill=FILL, stroke=accent, r=10),
                box(x, 96, 220, 30, None, fill=soft, stroke=accent, r=10),
                text(x + 110, 116, head, 12, 700, fill=accent),
                _lines(x + 14, 150, roles, size=11, gap=26)]
        steps.append(step(n, "".join(body), L[n - 1]))
    desc = ("A media product moves through three phases. In pre-production everything is "
            "decided before anything is made: the client sets the brief, the producer "
            "plans the budget and schedule, the scriptwriter writes and the storyboard "
            "artist draws the planned shots. In production the assets are actually "
            "captured or built: the director makes the creative decisions, the camera "
            "operator shoots, the sound engineer records and the graphic designer builds "
            "the visual assets. In post-production the pieces are brought together: the "
            "video editor assembles the footage, the sound editor mixes the audio, the "
            "visual effects artist composites, and the quality assurance tester finds "
            "faults before release.")
    return figure_steps("imedia-pipe", 760, 278, "".join(base), steps,
                        "The three phases of production and the roles in each", desc,
                        "Questions on job roles almost always ask which phase a role "
                        "belongs to. Learn the roles by phase rather than as one list.",
                        labels=L)


# ======================================================= 27. Choosing a format

@diagram("imedia-file-formats")
def _imedia_formats():
    """Lossy, lossless and vector, then the format the question actually wants."""
    base = [text(380, 28, "Which format, and why", 12, 650, fill=MUTED)]
    L = [
        "Lossy throws data away permanently to make the file small.",
        "Lossless keeps every bit, so the file is larger but nothing is lost.",
        "Vector stores shapes as maths, so it scales to any size with no loss.",
        "Pick the format from the purpose, and keep the master lossless until export.",
    ]
    def card(x, title, accent, soft, lines, formats):
        o = [box(x, 60, 226, 150, None, fill=FILL, stroke=accent, r=10),
             box(x, 60, 226, 32, None, fill=soft, stroke=accent, r=10),
             text(x + 113, 81, title, 12, 700, fill=accent),
             _lines(x + 14, 114, lines, size=11, gap=22)]
        o.append(text(x + 113, 196, formats, 11, 650, fill=accent))
        return "".join(o)
    steps = [
        step(1, card(24, "LOSSY", TEAL, TEAL_SOFT,
                     ["Data is permanently removed", "Much smaller files",
                      "Quality drops each re-save"], "JPG   MP3   MP4")
             + text(380, 240, "Use for the final export, never for the master",
                    11, 600, fill=MUTED), L[0]),
        step(2, card(267, "LOSSLESS", LILAC, LILAC_SOFT,
                     ["Every bit is kept", "Larger files",
                      "Re-saving costs nothing"], "PNG   WAV   TIFF")
             + text(380, 240, "Use while you are still working on it", 11, 600, fill=MUTED), L[1]),
        step(3, card(510, "VECTOR", TEAL, TEAL_SOFT,
                     ["Shapes stored as maths", "Scales to any size",
                      "Tiny files for flat graphics"], "SVG   AI   EPS")
             + text(380, 240, "Use for logos and anything that must resize",
                    11, 600, fill=MUTED), L[2]),
        step(4, _ttable(96, 56, ["Purpose", "Format", "Why"], [
                 ["Photo on a web page", "JPG", "Small, no transparency needed"],
                 ["Logo on a colour", "PNG or SVG", "Transparency, scales cleanly"],
                 ["Print poster", "PDF, CMYK, 300dpi", "Layout and fonts preserved"],
                 ["Social media video", "MP4 H.264", "Supported everywhere"],
                 ["Master recording", "WAV", "Lossless until the final export"],
             ], cw=190, rh=26), L[3]),
    ]
    desc = ("Three kinds of file format and how to choose between them. Lossy formats "
            "such as JPG, MP3 and MP4 permanently discard data to make files much "
            "smaller, and quality drops a little more every time the file is re-saved, "
            "so they belong at the final export and never as the working master. "
            "Lossless formats such as PNG, WAV and TIFF keep every bit, so files are "
            "larger but re-saving costs nothing, which is what you want while still "
            "working. Vector formats such as SVG store shapes as mathematics rather "
            "than pixels, so they scale to any size with no loss and stay tiny for flat "
            "graphics, which is why logos are vector. Choosing in an exam means reading "
            "the purpose: a photograph on a web page is JPG, a logo over a colour is PNG "
            "or SVG for the transparency, a print poster is a PDF in CMYK at 300 dots "
            "per inch, a social media video is MP4 using H.264, and a master audio "
            "recording is WAV.")
    return figure_steps("imedia-fmt", 760, 258, "".join(base), steps,
                        "Lossy, lossless and vector, and choosing a format by purpose", desc,
                        "Format questions are really purpose questions. Say what the "
                        "product has to do, then name the format that does it.",
                        labels=L)


# ===================================================== 28. Visual identity

@diagram("imedia-visual-identity")
def _imedia_identity():
    """The components of an identity, and the justification that earns the marks."""
    base = [text(380, 28, "What a visual identity is made of", 12, 650, fill=MUTED)]
    L = [
        "A logo: the single mark that has to work everywhere, at any size.",
        "A colour palette: chosen for what the colours mean to the audience.",
        "Typography: a type pairing that carries the same tone as the brand.",
        "Tone and consistency: the same rules applied across every product.",
        "The marks come from justifying each choice against the client brief.",
    ]
    def panel(title, accent, soft, body_items, art):
        o = [box(70, 56, 620, 164, None, fill=FILL, stroke=accent, r=12),
             box(70, 56, 620, 34, None, fill=soft, stroke=accent, r=12),
             text(380, 79, title, 12, 700, fill=accent),
             _lines(104, 124, body_items, size=12, gap=26)]
        return "".join(o) + art
    swatches = "".join(
        box(400 + i * 54, 112, 44, 44, None, fill=c, stroke=LINE, r=6)
        for i, c in enumerate([TEAL, LILAC, "var(--dg-fill-2)", "var(--dg-warn)"]))
    steps = [
        step(1, panel("LOGO", TEAL, TEAL_SOFT,
                      ["Works at any size", "Works in one colour", "Recognisable in a second"],
                      circle(500, 134, 30, fill=TEAL_SOFT, stroke=TEAL)
                      + text(500, 140, "M", 24, 700, fill=TEAL)
                      + box(556, 118, 32, 32, None, fill=TEAL_SOFT, stroke=TEAL, r=6)
                      + text(572, 140, "M", 15, 700, fill=TEAL)
                      + text(536, 190, "same mark, any size", 10, 500, fill=MUTED)), L[0]),
        step(2, panel("COLOUR PALETTE", LILAC, LILAC_SOFT,
                      ["Chosen for association", "Blue reads as trust",
                       "Checked for contrast"], swatches), L[1]),
        step(3, panel("TYPOGRAPHY", TEAL, TEAL_SOFT,
                      ["One display face", "One readable body face",
                       "Tone must match the brand"],
                      text(500, 128, "Headline", 22, 700, fill=TEAL)
                      + text(500, 156, "and the body text beneath it", 12, 400,
                             fill="var(--dg-text)")), L[2]),
        step(4, panel("TONE AND CONSISTENCY", LILAC, LILAC_SOFT,
                      ["The same rules everywhere", "Poster, web, social, print",
                       "One identity, many products"],
                      "".join(box(430 + i * 62, 112, 52, 44, None, fill="var(--dg-fill-2)",
                                  stroke=LILAC, r=5) for i in range(4))
                      + text(524, 190, "one identity across every product", 10, 500, fill=MUTED)), L[3]),
        step(5, box(70, 56, 620, 164, None, fill=FILL, stroke=WARN, r=12)
             + box(70, 56, 620, 34, None, fill=WARN_SOFT, stroke=WARN, r=12)
             + text(380, 79, "WHERE THE MARKS ARE", 12, 700, fill=WARN)
             + text(380, 124, '"I chose blue because I like it"', 13, 500, fill=MUTED)
             + text(380, 148, "scores nothing", 11, 600, fill=MUTED)
             + line(140, 164, 620, 164, stroke="var(--dg-line-soft)", w=1)
             + text(380, 188, '"Blue because the brief asks for a trustworthy, professional feel"',
                    12, 650, fill=WARN)
             + text(380, 208, "justification against the brief is the whole difference",
                    10, 500, fill=MUTED), L[4]),
    ]
    desc = ("A visual identity has four components and one thing that earns the marks. "
            "The logo is the single mark that must work at any size, in one colour, and "
            "be recognisable in a second. The colour palette is chosen for what the "
            "colours mean to the audience, so blue reads as trust and stability, and it "
            "must be checked for contrast. Typography is usually one display face and one "
            "readable body face, chosen so the tone matches the brand. Tone and "
            "consistency mean the same rules are applied across every product, from "
            "poster to website to social media. What separates a high band answer is "
            "justification against the brief: saying a colour was chosen because you like "
            "it scores nothing, while saying blue was chosen because the brief asks for a "
            "trustworthy and professional feel is the whole difference.")
    return figure_steps("imedia-vi", 760, 236, "".join(base), steps,
                        "The components of a visual identity", desc,
                        "R094 is marked on justification. Every choice you make needs a "
                        "sentence tying it back to the client brief.",
                        labels=L)


# ============================================== 29. Navigation structures

@diagram("imedia-navigation-structures")
def _imedia_nav():
    """The shapes a navigation diagram can take, and when each fits."""
    base = [text(380, 28, "How the screens of an interactive product connect",
                 12, 650, fill=MUTED)]
    L = [
        "Linear: one route, start to finish. A guided tour or a quiz.",
        "Hierarchical: a home screen branching into sections. Most websites and apps.",
        "Non-linear: any screen reaches any other. A reference product or a menu hub.",
    ]
    def node(x, y, label, accent=TEAL, soft=None, w=104, h=34):
        return box(x, y, w, h, label, fill=soft or FILL, stroke=accent, r=6, label_size=11)
    lin = []
    for i, nm in enumerate(["Start", "Step 1", "Step 2", "End"]):
        x = 60 + i * 168
        lin.append(node(x, 110, nm, TEAL, TEAL_SOFT if i in (0, 3) else None))
        if i < 3:
            lin.append(line(x + 110, 127, x + 162, 127, stroke=LINE, arrow=True))
    lin.append(text(380, 196, "one route, no way to skip ahead", 11, 600, fill=MUTED))

    hier = [node(328, 66, "Home", TEAL, TEAL_SOFT)]
    for i, nm in enumerate(["Section A", "Section B", "Section C"]):
        x = 150 + i * 178
        hier.append(node(x, 142, nm, LILAC))
        hier.append(path("M380 100 L380 122 L%d 122 L%d 140" % (x + 52, x + 52),
                         stroke=LINE, arrow=True))
    for i, x in enumerate([116, 222]):
        hier.append(node(x, 206, "Page %d" % (i + 1), LINE, w=92, h=30))
        hier.append(path("M202 176 L202 192 L%d 192 L%d 204" % (x + 46, x + 46),
                         stroke=LINE, arrow=True))
    hier.append(text(380, 254, "a clear top level, then depth below it", 11, 600, fill=MUTED))

    pts = [(380, 70), (240, 150), (520, 150), (380, 212)]
    nonlin = []
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            nonlin.append(line(pts[i][0], pts[i][1] + 17, pts[j][0], pts[j][1] + 17,
                               stroke="var(--dg-line-soft)", w=1.2))
    for i, (x, y) in enumerate(pts):
        nonlin.append(node(x - 52, y, "Screen %d" % (i + 1), TEAL if i == 0 else LILAC,
                           TEAL_SOFT if i == 0 else None))
    nonlin.append(text(380, 266, "every screen reaches every other", 11, 600, fill=MUTED))

    steps = [step(1, "".join(lin), L[0]), step(2, "".join(hier), L[1]),
             step(3, "".join(nonlin), L[2])]
    desc = ("Three shapes a navigation diagram can take. A linear structure gives one "
            "route from start to finish with no way to skip ahead, which suits a guided "
            "tour, a tutorial or a quiz. A hierarchical structure has a home screen "
            "branching into sections, with further pages below each section, and is what "
            "most websites and apps use because it gives a clear top level and depth "
            "underneath. A non-linear structure lets any screen reach any other, which "
            "suits a reference product or a menu hub where the user decides the order. "
            "The navigation diagram is the single most important planning document for "
            "an interactive product, because it is what proves every screen is reachable "
            "and every route returns.")
    return figure_steps("imedia-nav", 760, 286, "".join(base), steps,
                        "Linear, hierarchical and non-linear navigation", desc,
                        "Name the structure and say why it suits the product. "
                        "A quiz is linear, an app is hierarchical, a reference "
                        "product is non-linear.",
                        labels=L)


# ================================================= 30. Input, process, output

@diagram("ks3-input-process-output")
def _ks3_ipo():
    """Hardware by the job it does, and where software sits."""
    base = [text(380, 28, "Every computer does the same four jobs", 12, 650, fill=MUTED)]
    L = ["Input: hardware that gets data into the computer.",
         "Process: the CPU does the actual work.",
         "Output: hardware that gets the results back out to you.",
         "Storage: keeps your files when the power is off.",
         "Software is the instructions. Hardware is the parts you could drop on your foot."]
    def stage(x, title, accent, soft, items, on):
        o = [box(x, 76, 160, 118, None, fill=soft if on else FILL,
                 stroke=accent if on else "var(--dg-line-soft)", r=10),
             text(x + 80, 102, title, 12, 700, fill=accent if on else MUTED)]
        o.append(_lines(x + 16, 130, items, size=11, gap=22,
                        fill="var(--dg-text)" if on else MUTED))
        return "".join(o)
    cfg = [(26, "INPUT", TEAL, TEAL_SOFT, ["Keyboard", "Mouse", "Microphone"]),
           (212, "PROCESS", LILAC, LILAC_SOFT, ["CPU", "RAM", "the thinking"]),
           (398, "OUTPUT", TEAL, TEAL_SOFT, ["Screen", "Speakers", "Printer"]),
           (584, "STORAGE", LILAC, LILAC_SOFT, ["Hard drive", "SSD", "USB stick"])]
    arrows = (line(190, 135, 208, 135, stroke=LINE, arrow=True)
              + line(376, 135, 394, 135, stroke=LINE, arrow=True)
              + path("M292 194 L292 216 L664 216 L664 198", stroke=LINE, dash="4 4", arrow=True))
    steps = []
    for n in range(4):
        body = arrows + "".join(stage(x, t, a, s, i, on=(k == n))
                                for k, (x, t, a, s, i) in enumerate(cfg))
        steps.append(step(n + 1, body, L[n]))
    # Final stage: hardware vs software.
    sw = [box(60, 72, 290, 128, None, fill=FILL, stroke=TEAL, r=10),
          text(205, 98, "HARDWARE", 12, 700, fill=TEAL),
          _lines(90, 128, ["The physical parts", "You can touch them",
                           "Keyboard, CPU, screen"], size=11, gap=22),
          box(410, 72, 290, 128, None, fill=FILL, stroke=LILAC, r=10),
          text(555, 98, "SOFTWARE", 12, 700, fill=LILAC),
          _lines(440, 128, ["The instructions", "You cannot touch them",
                            "Games, browser, Windows"], size=11, gap=22),
          text(380, 228, "Software tells the hardware what to do", 11, 600, fill=MUTED)]
    steps.append(step(5, "".join(sw), L[4]))
    desc = ("Every computer does four jobs. Input hardware gets data in, such as a "
            "keyboard, mouse or microphone. The processor does the actual work, helped by "
            "RAM. Output hardware gets results back to you through a screen, speakers or "
            "a printer. Storage such as a hard drive, solid state drive or USB stick "
            "keeps your files when the power is off, which is the difference between it "
            "and RAM. Hardware means the physical parts you can touch, while software "
            "means the instructions that tell that hardware what to do.")
    return figure_steps("ks3-ipo", 760, 246, "".join(base), steps,
                        "Input, process, output and storage", desc,
                        "If you are asked to classify a device, ask what job it does: "
                        "does it bring data in, work on it, send it out, or keep it?",
                        labels=L)


# ===================================================== 31. Scratch constructs

@diagram("ks3-scratch-constructs")
def _ks3_scratch():
    """The three programming constructs, drawn as blocks."""
    base = [text(380, 28, "The three things every program is built from", 12, 650, fill=MUTED)]
    L = ["Sequence: instructions run in order, top to bottom.",
         "Selection: the program chooses a path using IF.",
         "Iteration: a block of instructions repeats."]

    def blk(x, y, label, accent=TEAL, soft=TEAL_SOFT, w=250, h=34, notch=True):
        o = [box(x, y, w, h, None, fill=soft, stroke=accent, r=6),
             text(x + 14, y + h / 2 + 4.5, label, 12, 600, anchor="start", fill="var(--dg-text)")]
        if notch:
            o.append(box(x + 18, y + h - 3, 22, 7, None, fill=soft, stroke=accent, r=3))
        return "".join(o)

    seq = [blk(255, 66, "when green flag clicked", LILAC, LILAC_SOFT),
           blk(255, 108, "say  Hello!"), blk(255, 150, "move 10 steps"),
           blk(255, 192, "turn 15 degrees"),
           path("M240 83 L240 226", stroke=LINE, w=2, dash="4 4", arrow=True),
           text(190, 160, "runs in", 11, 600, anchor="end", fill=MUTED),
           text(190, 178, "this order", 11, 600, anchor="end", fill=MUTED)]

    sel = [blk(230, 62, "if  touching edge?  then", LILAC, LILAC_SOFT, w=300),
           box(230, 96, 300, 86, None, fill="none", stroke=LILAC, r=6, dash="4 3"),
           blk(254, 108, "turn 180 degrees", TEAL, TEAL_SOFT, w=252),
           blk(254, 146, "say  Ouch!", TEAL, TEAL_SOFT, w=252),
           blk(230, 190, "else", LILAC, LILAC_SOFT, w=300, notch=False),
           blk(254, 226, "move 10 steps", TEAL, TEAL_SOFT, w=252, notch=False),
           text(560, 140, "only one", 11, 600, anchor="start", fill=MUTED),
           text(560, 158, "branch runs", 11, 600, anchor="start", fill=MUTED)]

    it = [blk(230, 70, "repeat  10", WARN, WARN_SOFT, w=300),
          box(230, 104, 300, 92, None, fill="none", stroke=WARN, r=6, dash="4 3"),
          blk(254, 116, "move 10 steps", TEAL, TEAL_SOFT, w=252),
          blk(254, 154, "turn 36 degrees", TEAL, TEAL_SOFT, w=252),
          path("M224 196 L196 196 L196 88 L224 88", stroke=WARN, w=2.2, arrow=True,
               marker="ah"),
          text(560, 146, "these two run", 11, 600, anchor="start", fill=MUTED),
          text(560, 164, "ten times", 11, 600, anchor="start", fill=MUTED),
          text(380, 232, "ten moves and ten turns of 36 degrees draws a circle",
               11, 500, fill=MUTED)]

    steps = [step(1, "".join(seq), L[0]), step(2, "".join(sel), L[1]),
             step(3, "".join(it), L[2])]
    desc = ("Every program is built from three constructs. Sequence means the "
            "instructions run in order from top to bottom, so a script might say hello, "
            "move ten steps and then turn fifteen degrees. Selection means the program "
            "chooses between paths using if and else, so if the sprite is touching the "
            "edge it turns around and says ouch, and otherwise it keeps moving, with "
            "only one branch ever running. Iteration means a block of instructions "
            "repeats, so repeat ten times around a move of ten steps and a turn of "
            "thirty six degrees draws a complete circle.")
    return figure_steps("ks3-scratch", 760, 270, "".join(base), steps,
                        "Sequence, selection and iteration as Scratch blocks", desc,
                        "These three ideas are the whole of programming. Everything you "
                        "write later in Python is still only these, in different words.",
                        labels=L)


# ================================================== 32. Bitmap against vector

@diagram("ks3-bitmap-vector")
def _ks3_bitmap_vector():
    """Why one goes blocky and the other does not, by zooming in on both."""
    base = [text(380, 26, "What happens when you make an image bigger", 12, 650, fill=MUTED)]
    L = ["A bitmap is a grid of coloured pixels. The file stores every single one.",
         "Enlarge a bitmap and the pixels get bigger, so the edges turn into steps.",
         "A vector stores instructions, not pixels: a circle, this big, this colour.",
         "Enlarge a vector and it is simply redrawn, so the edge stays perfectly smooth.",
    ]
    def grid(ox, oy, cell, n, filled):
        o = []
        for r in range(n):
            for c in range(n):
                on = (r, c) in filled
                o.append(box(ox + c * cell, oy + r * cell, cell, cell, None,
                             fill=TEAL if on else FILL,
                             stroke="var(--dg-line-soft)", r=0))
        return "".join(o)
    # A crude circle on an 8x8 grid.
    disc = {(r, c) for r in range(8) for c in range(8)
            if (r - 3.5) ** 2 + (c - 3.5) ** 2 <= 11}
    steps = [
        step(1, grid(290, 56, 22, 8, disc)
             + text(380, 254, "8 x 8 = 64 pixels, each one stored in the file",
                    11, 600, fill=MUTED), L[0]),
        step(2, grid(120, 54, 22, 8, disc)
             + text(208, 250, "normal size", 11, 600, fill=MUTED)
             + line(300, 142, 340, 142, stroke=LINE, arrow=True)
             + text(320, 130, "zoom", 10, 600, fill=MUTED)
             + grid(372, 54, 48, 4, {(r, c) for r in range(4) for c in range(4)
                                     if (r - 1.5) ** 2 + (c - 1.5) ** 2 <= 3.2})
             + text(468, 250, "enlarged: blocky steps", 11, 650, fill=WARN), L[1]),
        step(3, circle(380, 150, 86, fill=TEAL_SOFT, stroke=TEAL, w=2)
             + text(380, 156, "circle", 13, 650, fill=TEAL)
             + _lines(120, 118, ["The file says:", "  a circle", "  centre here",
                                 "  radius 86", "  filled teal"], size=11, gap=22)
             + text(380, 262, "five instructions, not sixty four pixels", 11, 600, fill=MUTED), L[2]),
        step(4, circle(190, 150, 56, fill=TEAL_SOFT, stroke=TEAL, w=2)
             + text(190, 234, "normal size", 11, 600, fill=MUTED)
             + line(260, 150, 300, 150, stroke=LINE, arrow=True)
             + text(280, 138, "zoom", 10, 600, fill=MUTED)
             + circle(470, 150, 94, fill=TEAL_SOFT, stroke=TEAL, w=2)
             + text(470, 262, "enlarged: still perfectly smooth", 11, 650, fill=TEAL), L[3]),
    ]
    desc = ("Why a bitmap goes blocky and a vector does not. A bitmap, also called a "
            "raster image, is a grid of coloured pixels, and the file stores every single "
            "one, so an eight by eight image is sixty four stored values. Enlarging it "
            "cannot invent detail that was never recorded, so each pixel simply becomes "
            "bigger and curved edges turn into visible steps. A vector file stores "
            "instructions rather than pixels: it says there is a circle, with this centre, "
            "this radius and this fill colour. Enlarging it just means redrawing those "
            "instructions at the new size, so the edge stays perfectly smooth however big "
            "it gets. That is why photographs are bitmaps and logos are vectors.")
    return figure_steps("ks3-bv", 760, 282, "".join(base), steps,
                        "Why a bitmap goes blocky and a vector stays sharp", desc,
                        "A vector file does not store a picture. It stores the "
                        "instructions for drawing one, and instructions work at any size.",
                        labels=L)


# ==================================================== 33. Digital footprint

@diagram("ks3-digital-footprint")
def _ks3_footprint():
    """What you post, what is taken, and where both end up."""
    base = [text(380, 26, "The trail you leave behind online", 12, 650, fill=MUTED)]
    L = ["Active footprint: everything you deliberately post.",
         "Passive footprint: data collected while you did nothing at all.",
         "Both end up in the same place, and the copies outlive the original.",
         "You can shrink a footprint. You cannot delete one."]

    def source(title, accent, soft, items, dash, note):
        return "".join([
            circle(100, 148, 44, fill=soft, stroke=accent, w=2),
            text(100, 154, "YOU", 13, 700, fill=accent),
            line(148, 148, 204, 148, stroke=accent, arrow=True,
                 marker="ah-accent" if accent == TEAL else "ah-alt", dash=dash),
            box(212, 68, 268, 160, None, fill=soft, stroke=accent, r=10),
            text(346, 94, title, 12, 700, fill=accent),
            _lines(234, 124, items, size=11, gap=24),
            line(488, 148, 544, 148, stroke=accent, arrow=True,
                 marker="ah-accent" if accent == TEAL else "ah-alt", dash=dash),
            box(550, 68, 186, 160, None, fill=FILL, stroke=LINE, r=10),
            text(643, 94, "YOUR FOOTPRINT", 11, 700, fill=MUTED),
            text(643, 134, "stored", 12, 600),
            text(643, 160, "copied", 12, 600),
            text(643, 186, "searchable", 12, 600),
            text(380, 262, note, 11, 650, fill=MUTED)])

    s1 = source("ACTIVE", TEAL, TEAL_SOFT,
                ["Photos and videos you post", "Comments and messages",
                 "Your profile and your bio", "Likes, follows, reviews"], None,
                "You chose to put all of this online")
    s2 = source("PASSIVE", LILAC, LILAC_SOFT,
                ["Pages you visit, and for how long", "Every search you type",
                 "Your location and your device", "Who you are connected to"], "5 4",
                "Nobody asked you. It was collected anyway.")

    s3 = "".join([
        box(286, 56, 188, 64, None, fill=FILL, stroke=LINE, r=10),
        text(380, 80, "YOUR FOOTPRINT", 11, 700, fill=MUTED),
        text(380, 102, "active and passive together", 10, 450, fill=MUTED),
        path("M380 120 L380 142 L142 142 L142 166", stroke=LINE, arrow=True),
        path("M380 120 L380 166", stroke=LINE, arrow=True),
        path("M380 120 L380 142 L618 142 L618 166", stroke=LINE, arrow=True),
        box(34, 168, 216, 66, "ADVERTISERS", "profiled and targeted",
            fill=FILL, stroke=LINE, label_size=11),
        box(272, 168, 216, 66, "EMPLOYERS AND UNIS", "they really do look",
            fill=FILL, stroke=LINE, label_size=11),
        box(510, 168, 216, 66, "DATA BROKERS", "collected, bundled, sold on",
            fill=FILL, stroke=LINE, label_size=11),
        text(380, 262, "Deleting your post does not delete anyone's screenshot of it",
             11, 650, fill=WARN)])

    tips = [("Check your privacy settings", "and again after every app update"),
            ("Think before you post", "teacher, parent, future employer"),
            ("Turn off location tagging", "a photo records where you were"),
            ("Skip the fun quizzes", "your first pet is a security answer")]
    s4 = "".join(
        [box(36 + (i % 2) * 350, 60 + (i // 2) * 72, 338, 62, t, s,
             fill=TEAL_SOFT, stroke=TEAL, label_size=12) for i, (t, s) in enumerate(tips)]
        + [box(36, 204, 688, 36, "Log out of your accounts on any shared device",
               fill=FILL, stroke=LINE, label_size=12),
           text(380, 262, "Assume anything you put online is permanent and public",
                11, 650, fill=TEAL)])

    steps = [step(1, s1, L[0]), step(2, s2, L[1]), step(3, s3, L[2]), step(4, s4, L[3])]
    desc = ("Your digital footprint has two halves. The active half is everything you "
            "deliberately post: photos, videos, comments, messages, your profile, your "
            "likes and follows. The passive half is collected without you doing anything: "
            "which pages you visit and for how long, every search you type, your location, "
            "your device and who you are connected to. Both halves end up in the same "
            "store, where they are copied and searchable, and from there they reach "
            "advertisers who profile you, employers and universities who really do look, "
            "and data brokers who bundle and sell them on. Deleting a post does not delete "
            "anybody's screenshot of it. You can shrink a footprint by checking privacy "
            "settings after every update, thinking before posting, turning off location "
            "tagging, refusing quizzes that ask for security question answers and logging "
            "out on shared devices, but you cannot delete one.")
    return figure_steps("ks3-fp", 760, 276, "".join(base), steps,
                        "Active and passive digital footprints", desc,
                        "The passive half is the bigger half, and it is the half most "
                        "people have never thought about.", labels=L)


# ============================================ 34. Relative and absolute cells

@diagram("ks3-cell-references")
def _ks3_cells():
    """Why a formula that works in row 2 breaks in row 3."""
    base = [text(380, 24, "What the dollar signs actually do", 12, 650, fill=MUTED)]
    L = ["One cell holds the VAT multiplier. The formula points at a price and at that cell.",
         "Copy it down with no dollar signs and BOTH references move. E2 is empty.",
         "Lock it with $E$1 and the price still moves while the rate stays put.",
         "Mixed references lock one half: the column, or the row."]

    COLS = [("A", 60, 92), ("B", 152, 92), ("C", 244, 150), ("D", 394, 86), ("E", 480, 70)]
    RH, R0 = 30, 92

    def cellbox(x, w, r, s, fill=FILL, stroke="var(--dg-line-soft)", mono=False,
                col="var(--dg-text)"):
        y = R0 + r * RH
        o = [box(x, y, w, RH, None, fill=fill, stroke=stroke, r=0)]
        if s:
            o.append(text(x + w / 2, y + RH / 2 + 4, s, 11, 600, fill=col, mono=mono))
        return "".join(o)

    def sheet(formulas, hl=()):
        o = [box(26, 66, 34, 26, None, fill="var(--dg-fill-2)", stroke="var(--dg-line-soft)", r=0)]
        for letter, x, w in COLS:
            o.append(box(x, 66, w, 26, None, fill="var(--dg-fill-2)",
                         stroke="var(--dg-line-soft)", r=0))
            o.append(text(x + w / 2, 84, letter, 11, 700, fill=MUTED))
        rows = [["Item", "Price", "With VAT", "VAT x", "1.2"],
                ["Pen", "2.00", formulas[0], "", ""],
                ["Pad", "5.00", formulas[1], "", ""],
                ["Bag", "9.00", formulas[2], "", ""]]
        for r in range(4):
            o.append(box(26, R0 + r * RH, 34, RH, None, fill="var(--dg-fill-2)",
                         stroke="var(--dg-line-soft)", r=0))
            o.append(text(43, R0 + r * RH + RH / 2 + 4, str(r + 1), 11, 700, fill=MUTED))
            for (letter, x, w), s in zip(COLS, rows[r]):
                ref = "%s%d" % (letter, r + 1)
                mono = letter == "C" and r > 0
                acc = hl.get(ref) if isinstance(hl, dict) else None
                o.append(cellbox(x, w, r, s, mono=mono,
                                 fill=acc[1] if acc else FILL,
                                 stroke=acc[0] if acc else "var(--dg-line-soft)",
                                 col=acc[0] if acc and not mono else "var(--dg-text)"))
        return "".join(o)

    def notes(items, fill=MUTED):
        return _lines(574, 108, items, size=11, gap=24, fill=fill)

    s1 = sheet(["=B2*$E$1", "", ""], {"B2": (TEAL, TEAL_SOFT), "E1": (LILAC, LILAC_SOFT)})
    s1 += notes(["B2 is the price", "on this row.", "", "E1 is the rate,", "stored once."])
    s2 = sheet(["=B2*E1", "=B3*E2", "=B4*E3"],
               {"E2": (WARN, WARN_SOFT), "E3": (WARN, WARN_SOFT)})
    s2 += notes(["Both halves moved.", "E2 and E3 are", "empty cells, so", "both answers", "come out as 0."], WARN)
    s3 = sheet(["=B2*$E$1", "=B3*$E$1", "=B4*$E$1"], {"E1": (TEAL, TEAL_SOFT)})
    s3 += notes(["B moved: correct.", "$E$1 did not:", "also correct.", "", "2.40  6.00  10.80"], TEAL)

    mixed = [("B2", "Nothing locked. Copy it anywhere and both parts move."),
             ("$B$2", "Both locked. It always means B2, wherever you copy it."),
             ("$B2", "Column locked, row free. Copy right and it stays in B."),
             ("B$2", "Row locked, column free. Copy down and it stays in row 2.")]
    s4 = "".join([box(40, 60 + i * 44, 672, 38, None, fill=FILL, stroke=LINE, r=8)
                  + box(52, 68 + i * 44, 86, 22, None, fill=TEAL_SOFT, stroke=TEAL, r=6)
                  + text(95, 84 + i * 44, ref, 12, 700, fill=TEAL, mono=True)
                  + text(154, 84 + i * 44, meaning, 11, 500, anchor="start")
                  for i, (ref, meaning) in enumerate(mixed)])

    steps = [step(1, s1, L[0]), step(2, s2, L[1]), step(3, s3, L[2]), step(4, s4, L[3])]
    desc = ("A sheet with items in column A, prices in column B and a VAT multiplier of "
            "1.2 stored once in cell E1. The formula in C2 is B2 multiplied by E1. Written "
            "with no dollar signs and copied down, both references move, so row 3 becomes "
            "B3 times E2 and row 4 becomes B4 times E3. E2 and E3 are empty, so every "
            "answer below the first row is zero. Written as B2 times dollar E dollar 1 and "
            "copied down, the price reference still moves to B3 and B4, which is what you "
            "want, while the locked rate reference stays on E1, giving 2.40, 6.00 and "
            "10.80. A reference with no dollar signs is relative and moves. Dollar B "
            "dollar 2 locks both parts. Dollar B 2 locks the column only. B dollar 2 locks "
            "the row only.")
    return figure_steps("ks3-cells", 760, 262, "".join(base), steps,
                        "Relative and absolute cell references", desc,
                        "If a formula works in the first row and gives nonsense when "
                        "copied down, you needed a dollar sign on something that moved.",
                        labels=L)


# ============================================== 35. HTML, CSS and the browser

@diagram("ks3-html-css-render")
def _ks3_html_css():
    """Two files, two jobs, one page."""
    base = [text(380, 24, "HTML says what it is. CSS says what it looks like.",
                 12, 650, fill=MUTED)]
    L = ["HTML marks up the structure: a heading, a paragraph, a link.",
         "CSS holds the styling rules, in a separate file.",
         "The browser takes both and draws the page.",
         "A selector decides which parts of the page a rule reaches."]

    def code(x, y, title, lines, accent, soft):
        o = [box(x, y, 336, 196, None, fill=soft, stroke=accent, r=10),
             text(x + 14, y + 22, title, 11, 700, anchor="start", fill=accent)]
        for i, s in enumerate(lines):
            o.append(text(x + 14, y + 46 + i * 20, s, 10.5, 500, anchor="start", mono=True))
        return "".join(o)

    HTML = ['<body>', '  <h1>Welcome</h1>', '  <p>A paragraph of text.</p>',
            '  <p class="highlight">Read me.</p>', '  <a href="page2.html">Next</a>',
            '</body>']
    CSS = ['h1 { color: #03969d;', '     text-align: center; }',
           'p  { font-size: 16px; }', '.highlight {',
           '  background-color: yellow; }', '#header { border-bottom: 2px; }']

    def page(x, y, styled, selectors=False):
        o = [box(x, y, 300, 196, None, fill="var(--dg-paper)", stroke=LINE, r=10)]
        if styled:
            o += [box(x + 1, y + 1, 298, 54, None, fill="var(--dg-fill-2)",
                      stroke="none", r=10),
                  line(x + 1, y + 55, x + 299, y + 55, stroke=LILAC, w=2),
                  text(x + 150, y + 36, "Welcome", 17, 700, fill=TEAL)]
        else:
            o.append(text(x + 18, y + 36, "Welcome", 17, 700, anchor="start",
                          fill="var(--dg-ink)"))
        ty = y + (76 if styled else 66)
        o.append(text(x + 18, ty, "A paragraph of text.", 11, 450, anchor="start",
                      fill="var(--dg-ink)"))
        if styled:
            o.append(box(x + 16, ty + 16, 140, 24, None, fill="var(--dg-mark)",
                         stroke="none", r=3))
        o.append(text(x + 18, ty + 33, "Read me.", 11, 450, anchor="start",
                      fill="var(--dg-mark-ink)" if styled else "var(--dg-ink)"))
        o.append(text(x + 18, ty + 66, "Next", 11, 500, anchor="start",
                      fill="var(--dg-link)"))
        o.append(line(x + 18, ty + 70, x + 44, ty + 70, stroke="var(--dg-link)", w=1))
        o.append(text(x + 150, y + 214, "the page as you see it", 11, 600, fill=MUTED))
        if selectors:
            o += [line(x - 86, y + 30, x + 140, y + 30, stroke=TEAL, dash="4 3",
                       arrow=True, marker="ah-accent"),
                  line(x - 86, ty + 28, x + 12, ty + 28, stroke=TEAL, dash="4 3",
                       arrow=True, marker="ah-accent"),
                  line(x - 86, y + 56, x + 1, y + 56, stroke=LILAC, dash="4 3",
                       arrow=True, marker="ah-alt")]
        return "".join(o)

    s1 = code(26, 50, "index.html", HTML, TEAL, TEAL_SOFT) + page(410, 50, False) \
        + text(380, 266, "With no CSS the browser uses its own plain defaults",
               11, 600, fill=MUTED)
    s2 = code(26, 50, "style.css", CSS, LILAC, LILAC_SOFT) + page(410, 50, False) \
        + text(380, 266, "The rules exist, but nothing has been joined up yet",
               11, 600, fill=MUTED)
    s3 = "".join([
        box(26, 50, 150, 72, "index.html", "structure", fill=TEAL_SOFT, stroke=TEAL,
            label_size=12),
        box(26, 142, 150, 72, "style.css", "style", fill=LILAC_SOFT, stroke=LILAC,
            label_size=12),
        path("M176 86 L226 86 L226 124", stroke=TEAL, arrow=True, marker="ah-accent"),
        path("M176 178 L226 178 L226 140", stroke=LILAC, arrow=True, marker="ah-alt"),
        box(196, 112, 180, 40, "THE BROWSER", fill=FILL, stroke=LINE, label_size=12),
        line(376, 132, 404, 132, stroke=LINE, arrow=True),
        page(410, 50, True),
        text(30, 266, "one CSS file can style every page on the site", 11, 600,
             anchor="start", fill=MUTED)])
    s4 = "".join([
        box(26, 62, 300, 40, None, fill=TEAL_SOFT, stroke=TEAL, r=8),
        text(44, 86, "h1 { ... }", 12, 650, anchor="start", mono=True, fill=TEAL),
        text(150, 86, "every h1 on the page", 11, 500, anchor="start"),
        box(26, 112, 300, 40, None, fill=LILAC_SOFT, stroke=LILAC, r=8),
        text(44, 136, "#header { ... }", 12, 650, anchor="start", mono=True, fill=LILAC),
        text(166, 136, "the one id", 11, 500, anchor="start"),
        box(26, 162, 300, 40, None, fill=TEAL_SOFT, stroke=TEAL, r=8),
        text(44, 186, ".highlight { ... }", 12, 650, anchor="start", mono=True, fill=TEAL),
        text(186, 186, "every class", 11, 500, anchor="start"),
        page(410, 50, True, selectors=True),
        text(176, 266, "a class for many, an id for exactly one", 11, 600, fill=MUTED)])

    steps = [step(1, s1, L[0]), step(2, s2, L[1]), step(3, s3, L[2]), step(4, s4, L[3])]
    desc = ("A web page is built from two files doing two different jobs. The HTML file "
            "marks up structure: a body containing an h1 heading, two paragraphs, one of "
            "them given class highlight, and a link. On its own the browser draws it with "
            "plain default styling, left aligned in black. The CSS file holds rules: h1 "
            "coloured teal and centred, paragraphs at sixteen pixels, the highlight class "
            "given a yellow background, the header id given a bottom border. On its own it "
            "draws nothing. The browser reads both and produces the finished page, which "
            "is why one CSS file can restyle an entire site. A selector decides which "
            "elements a rule reaches: a tag name such as h1 reaches every h1, a class "
            "beginning with a dot reaches every element carrying that class, and an id "
            "beginning with a hash reaches the single element with that id.")
    return figure_steps("ks3-webdev", 760, 282, "".join(base), steps,
                        "How HTML and CSS become a page", desc,
                        "Keeping structure and style in separate files is the reason a "
                        "whole site can be redesigned by editing one file.", labels=L)


# =================================================== 36. How an AI is trained

@diagram("ks3-how-ai-learns")
def _ks3_ai():
    """Rules against examples, and what that costs."""
    base = [text(380, 24, "Nobody wrote the rules for recognising a cat",
                 12, 650, fill=MUTED)]
    L = ["A normal program follows rules a human wrote down.",
         "Machine learning is shown labelled examples and finds the patterns itself.",
         "It is then tested on images it has never seen before.",
         "Whatever the training data contains, the system reproduces.",
         "It has no idea what a cat is, which is why it can be confidently wrong."]

    s1 = "".join([
        box(30, 66, 190, 54, "THE RULES", "written by a programmer",
            fill=LILAC_SOFT, stroke=LILAC, label_size=12),
        box(30, 150, 190, 54, "THE DATA", "one photo", fill=FILL, stroke=LINE,
            label_size=12),
        path("M220 93 L272 93 L272 125", stroke=LILAC, arrow=True, marker="ah-alt"),
        path("M220 177 L272 177 L272 145", stroke=LINE, arrow=True),
        box(272, 112, 196, 46, "THE PROGRAM", fill=FILL, stroke=LINE, label_size=12),
        line(468, 135, 508, 135, stroke=LINE, arrow=True),
        box(514, 108, 216, 54, "THE ANSWER", "if whiskers and fur then cat",
            fill=FILL, stroke=LINE, label_size=12),
        text(380, 232, "This works for tax and for traffic lights. It does not work for "
             "cats:", 11, 600, fill=MUTED),
        text(380, 252, "nobody can write down the rule that makes a cat a cat",
             11, 600, fill=MUTED)])

    s2 = "".join([
        box(30, 62, 204, 150, None, fill=TEAL_SOFT, stroke=TEAL, r=10),
        text(132, 86, "TRAINING DATA", 11, 700, fill=TEAL),
        _lines(48, 116, ["500,000 photographs,", "each one already", "labelled by a human:",
                         "cat, or not cat"], size=11, gap=22),
        line(234, 137, 274, 137, stroke=TEAL, arrow=True, marker="ah-accent"),
        box(280, 62, 200, 150, None, fill=FILL, stroke=LINE, r=10),
        text(380, 86, "THE MODEL", 11, 700, fill=MUTED),
        _lines(296, 116, ["Adjusts millions of", "internal numbers,", "guesses a label,",
                          "checks, adjusts again"], size=11, gap=22),
        path("M300 212 L300 234 L460 234 L460 212", stroke=TEAL, dash="4 4", arrow=True,
             marker="ah-accent"),
        text(380, 252, "every wrong guess nudges the numbers", 10.5, 600, fill=MUTED),
        line(480, 137, 520, 137, stroke=LINE, arrow=True),
        box(526, 92, 204, 90, "A TRAINED MODEL", "no rules anywhere in it",
            fill=LILAC_SOFT, stroke=LILAC, label_size=12)])

    s3 = "".join([
        box(30, 76, 214, 110, None, fill=FILL, stroke=LINE, r=10),
        text(137, 102, "UNSEEN PHOTOS", 11, 700, fill=MUTED),
        _lines(48, 132, ["10,000 images held", "back from training"], size=11, gap=22),
        line(244, 131, 284, 131, stroke=LINE, arrow=True),
        box(290, 92, 180, 78, "THE MODEL", fill=LILAC_SOFT, stroke=LILAC, label_size=12),
        line(470, 131, 510, 131, stroke=LINE, arrow=True),
        box(516, 76, 214, 110, None, fill=TEAL_SOFT, stroke=TEAL, r=10),
        text(623, 102, "92% CORRECT", 12, 700, fill=TEAL),
        _lines(534, 132, ["so it learned something", "general, not the answers"],
               size=11, gap=22),
        text(380, 228, "Testing on the training images would prove nothing at all:",
             11, 600, fill=MUTED),
        text(380, 248, "a system can score 100% by memorising and still be useless",
             11, 600, fill=MUTED)])

    def bar(x, y, w, pct, label, accent, soft):
        return "".join([box(x, y, w, 26, None, fill=soft, stroke=accent, r=6),
                        box(x, y, w * pct / 100.0, 26, None, fill=accent, stroke=accent, r=6),
                        text(x + w + 12, y + 18, "%d%%" % pct, 12, 700, anchor="start",
                             fill=accent),
                        text(x, y - 10, label, 11, 600, anchor="start", fill=MUTED)])
    s4 = "".join([
        box(30, 62, 250, 150, None, fill=FILL, stroke=LINE, r=10),
        text(155, 86, "THE TRAINING DATA", 11, 700, fill=MUTED),
        box(48, 104, 214, 26, None, fill=TEAL, stroke=TEAL, r=6),
        text(155, 122, "mostly light skinned faces", 10.5, 650, fill="var(--dg-fill)"),
        box(48, 138, 56, 26, None, fill=LILAC, stroke=LILAC, r=6),
        text(76, 156, "others", 10.5, 650, fill="var(--dg-fill)"),
        text(155, 192, "nobody chose this on purpose", 10.5, 500, fill=MUTED),
        line(280, 137, 320, 137, stroke=LINE, arrow=True),
        text(300, 124, "learns", 10, 600, fill=MUTED),
        bar(336, 104, 250, 98, "accuracy on light skinned faces", TEAL, TEAL_SOFT),
        bar(336, 162, 250, 71, "accuracy on dark skinned faces", WARN, WARN_SOFT),
        text(380, 242, "The system is not prejudiced. It is reproducing its data, "
             "exactly as built.", 11, 650, fill=WARN)])

    s5 = "".join([
        box(30, 64, 330, 150, None, fill=WARN_SOFT, stroke=WARN, r=10),
        text(195, 90, "WHAT IT ACTUALLY LEARNED", 11, 700, fill=WARN),
        _lines(50, 120, ["\"Photos labelled wolf usually", "have snow in them.\"",
                         "", "So a husky on a snowy path"], size=11, gap=22),
        text(50, 208, "is labelled wolf, with 97% confidence.", 11, 600, anchor="start"),
        box(400, 64, 330, 150, None, fill=FILL, stroke=LINE, r=10),
        text(565, 90, "WHY THAT MATTERS", 11, 700, fill=MUTED),
        _lines(420, 120, ["It found something that", "correlates with the answer.",
                          "It understands nothing.", "Confident is not correct."],
               size=11, gap=22),
        text(380, 244, "Anything that matters has to be checked against a real source",
             11, 650, fill=MUTED)])

    steps = [step(1, s1, L[0]), step(2, s2, L[1]), step(3, s3, L[2]),
             step(4, s4, L[3]), step(5, s5, L[4])]
    desc = ("How a machine learning system is built, and what that costs. A normal program "
            "takes rules a programmer wrote and some data, and produces an answer, which "
            "works for tax but not for recognising a cat, because nobody can write down the "
            "rule that makes a cat a cat. Machine learning instead starts from training "
            "data: five hundred thousand photographs already labelled cat or not cat by "
            "humans. The model guesses a label, checks it, and nudges millions of internal "
            "numbers every time it is wrong, until it is usually right. It is then tested on "
            "ten thousand images held back from training, and scoring well on those shows it "
            "learned something general rather than memorising answers. Because it only ever "
            "reproduces patterns in its data, data that is mostly light skinned faces "
            "produces a system markedly less accurate on darker skin, without anyone "
            "choosing that. And because it understands nothing, a system that learned only "
            "that wolf photographs usually contain snow will label a husky on a snowy path "
            "a wolf with ninety seven per cent confidence. Confident is not correct.")
    return figure_steps("ks3-ai", 760, 268, "".join(base), steps,
                        "How a machine learning system is trained, and how it goes wrong",
                        desc,
                        "The exam answer is the same every time: the system found "
                        "patterns in its training data. It did not understand anything.",
                        labels=L)


# ================================================= 37. The 3D pipeline

@diagram("ks3-3d-pipeline")
def _ks3_3d():
    """From eight points to a finished frame."""
    base = [text(380, 24, "From eight points to a finished frame", 12, 650, fill=MUTED)]
    L = ["A vertex is one point in 3D space, with an x, a y and a z.",
         "An edge is a straight line joining two vertices. A cube needs twelve.",
         "A face is a flat surface enclosed by edges. Together they make the mesh.",
         "More polygons means more detail, and more work for the computer.",
         "Materials say what it is made of, lights and a camera say how you see it.",
         "Animation sets keyframes, then every frame in between is rendered."]

    # An isometric cube. Front face, back face, and the edges joining them.
    F = [(284, 128), (404, 128), (404, 248), (284, 248)]
    B = [(340, 84), (460, 84), (460, 204), (340, 204)]
    def poly(pts, fill, stroke, w=1.8, dash=None):
        d = "M%d %d " % pts[0] + " ".join("L%d %d" % p for p in pts[1:]) + " Z"
        return path(d, stroke=stroke, w=w, fill=fill, dash=dash)

    verts = "".join(circle(x, y, 5, fill=TEAL, stroke=TEAL) for x, y in F + B)
    edges = "".join([poly(F, "none", LINE), poly(B, "none", LINE)] +
                    [line(F[i][0], F[i][1], B[i][0], B[i][1], stroke=LINE) for i in range(4)])

    s1 = verts + text(380, 282, "8 vertices. A detailed character has hundreds of "
                      "thousands.", 11, 600, fill=MUTED) \
        + _lines(40, 120, ["VERTEX", "", "one point", "x across", "y depth",
                           "z height"], size=11, gap=22, fill=MUTED)
    s2 = edges + verts + text(380, 282, "12 edges. Still see through: there are no "
                              "surfaces yet.", 11, 600, fill=MUTED) \
        + _lines(40, 120, ["EDGE", "", "a straight line", "joining two",
                           "vertices"], size=11, gap=22, fill=MUTED)
    s3 = "".join([
        poly([F[3], F[2], B[2], B[3]], TEAL_SOFT, TEAL),
        poly([B[0], B[1], B[2], B[3]], "var(--dg-fill-2)", LINE),
        poly([F[1], B[1], B[2], F[2]], LILAC_SOFT, LILAC),
        poly(F, TEAL_SOFT, TEAL),
        edges,
        text(380, 282, "6 faces. Vertices plus edges plus faces is the mesh.",
             11, 600, fill=MUTED),
        _lines(40, 120, ["FACE", "", "a flat surface", "enclosed by", "edges, usually",
                         "a triangle"], size=11, gap=22, fill=MUTED)])

    def sphere(cx, cy, r, bands, accent, soft):
        o = [circle(cx, cy, r, fill=soft, stroke=accent, w=1.8)]
        for i in range(1, bands):
            t = -r + 2.0 * r * i / bands
            half = (r * r - t * t) ** 0.5
            o.append(line(cx - half, cy + t, cx + half, cy + t,
                          stroke=accent, w=1))
            o.append(line(cx + t, cy - half, cx + t, cy + half, stroke=accent, w=1))
        return "".join(o)
    s4 = "".join([
        sphere(180, 140, 62, 4, TEAL, TEAL_SOFT),
        text(180, 230, "LOW POLYGON", 11, 700, fill=TEAL),
        text(180, 250, "blocky, but fast", 11, 500, fill=MUTED),
        sphere(400, 140, 62, 14, LILAC, LILAC_SOFT),
        text(400, 230, "HIGH POLYGON", 11, 700, fill=LILAC),
        text(400, 250, "smooth, but heavy", 11, 500, fill=MUTED),
        box(540, 76, 200, 128, None, fill=FILL, stroke=LINE, r=10),
        text(640, 100, "THE TRADE OFF", 11, 700, fill=MUTED),
        _lines(556, 128, ["A film renders each", "frame once, over hours.",
                          "A game renders 60", "frames every second."], size=10.5, gap=20),
        text(380, 284, "Games fake the missing detail with clever textures instead",
             11, 600, fill=MUTED)])

    s5 = "".join([
        poly([F[3], F[2], B[2], B[3]], TEAL_SOFT, TEAL),
        poly([F[1], B[1], B[2], F[2]], LILAC_SOFT, LILAC),
        poly(F, TEAL_SOFT, TEAL),
        edges,
        circle(170, 92, 20, fill=WARN_SOFT, stroke=WARN, w=2),
        path("M186 104 L270 136", stroke=WARN, w=1.6, dash="5 4", arrow=True),
        path("M186 96 L268 112", stroke=WARN, w=1.6, dash="5 4", arrow=True),
        text(170, 64, "LIGHT", 11, 700, fill=WARN),
        box(540, 212, 132, 48, "CAMERA", "the only view that exists",
            fill=FILL, stroke=LINE, label_size=11),
        path("M540 232 L478 206", stroke=LINE, dash="5 4", arrow=True),
        _lines(40, 170, ["MATERIAL", "colour, shine,", "roughness,", "transparency"],
               size=11, gap=20, fill=MUTED),
        text(380, 284, "A model with no material, light or camera renders as nothing",
             11, 600, fill=MUTED)])

    s6 = "".join([
        box(30, 70, 700, 96, None, fill=FILL, stroke=LINE, r=10),
        text(60, 94, "TIMELINE", 11, 700, anchor="start", fill=MUTED),
        line(60, 136, 700, 136, stroke="var(--dg-line-soft)", w=2),
        chip(90, 136, "frame 1"), chip(380, 136, "frame 24"), chip(670, 136, "frame 48"),
        text(90, 170, "keyframe", 10.5, 650, fill=TEAL),
        text(380, 170, "keyframe", 10.5, 650, fill=TEAL),
        text(670, 170, "keyframe", 10.5, 650, fill=TEAL),
        text(235, 118, "the computer fills these in", 10.5, 500, fill=MUTED),
        text(525, 118, "and these", 10.5, 500, fill=MUTED),
        box(30, 190, 340, 60, "RENDERING", "every frame calculated: lights, materials, "
            "shadows", fill=LILAC_SOFT, stroke=LILAC, label_size=12, sub_size=10),
        box(390, 190, 340, 60, "WHY IT TAKES SO LONG", "a 2 minute film at 24fps is "
            "2,880 frames", fill=WARN_SOFT, stroke=WARN, label_size=12, sub_size=10),
        text(380, 284, "You set the important poses. The computer does the in between.",
             11, 600, fill=MUTED)])

    steps = [step(i + 1, b, L[i]) for i, b in enumerate([s1, s2, s3, s4, s5, s6])]
    desc = ("How a 3D model is built and turned into a picture. A vertex is a single point "
            "in 3D space with an x coordinate across, a y for depth and a z for height; a "
            "cube has eight. An edge is a straight line joining two vertices, and a cube "
            "needs twelve. A face is a flat surface enclosed by edges, usually a triangle "
            "or a square, and a cube has six; vertices, edges and faces together are the "
            "mesh. More polygons give more detail and smoother curves but need more "
            "processing power and memory, which is the central trade off: a film renders "
            "each frame once over hours and can afford millions of polygons, while a game "
            "must render sixty frames every second and fakes missing detail with textures. "
            "A material gives the surface colour, shine, roughness and transparency, and "
            "lights and a camera decide how it is seen, since a model with none of those "
            "renders as nothing. Animation sets keyframes at the important poses and the "
            "computer calculates every frame in between, then renders each one, which is "
            "why a two minute film at twenty four frames a second means two thousand eight "
            "hundred and eighty rendered frames.")
    return figure_steps("ks3-3d", 760, 300, "".join(base), steps,
                        "The 3D pipeline, from vertices to a rendered frame", desc,
                        "Vertex, edge, face, mesh. Learn those four in that order and "
                        "the rest of the unit has somewhere to attach.", labels=L)


# ================================================== 38. The development cycle

@diagram("ks3-design-cycle")
def _ks3_cycle():
    """Six phases, and the fact that it goes round again."""
    base = [text(380, 24, "Why nobody starts by building", 12, 650, fill=MUTED)]
    PHASES = [
        ("1. ANALYSIS", "who is it for, what must it do",
         "Write requirements as testable statements. \"Make it good\" is not one."),
        ("2. DESIGN", "screens, flow and data",
         "Wireframes are deliberately ugly, so discussion stays on layout, not colour."),
        ("3. IMPLEMENTATION", "build it",
         "The shortest phase in this list, and the only one most people plan for."),
        ("4. TESTING", "including when things go wrong",
         "Normal, boundary and erroneous data. What happens when the field is empty?"),
        ("5. EVALUATION", "does it solve the problem",
         "Checked against the requirements you wrote in analysis, not against a hunch."),
        ("6. MAINTENANCE", "fix problems, add features",
         "And then straight back to analysis, which is why your apps update every week."),
    ]
    POS = [(40, 62), (280, 62), (520, 62), (520, 164), (280, 164), (40, 164)]

    arrows = "".join([
        line(240, 93, 276, 93, stroke=LINE, arrow=True),
        line(480, 93, 516, 93, stroke=LINE, arrow=True),
        path("M620 124 L620 160", stroke=LINE, arrow=True),
        line(516, 195, 480, 195, stroke=LINE, arrow=True),
        line(276, 195, 240, 195, stroke=LINE, arrow=True),
        path("M140 226 L140 248 L380 248", stroke=LINE, w=1.5, dash="5 4"),
        path("M380 248 L620 248 L620 230", stroke=LINE, dash="5 4", arrow=True),
    ])
    steps = []
    for n, (title, sub, detail) in enumerate(PHASES):
        body = [arrows]
        for k, ((x, y), (t, s, _)) in enumerate(zip(POS, PHASES)):
            on = k == n
            body.append(box(x, y, 200, 62, t, s,
                            fill=TEAL_SOFT if on else FILL,
                            stroke=TEAL if on else "var(--dg-line-soft)",
                            label_size=11, sub_size=10,
                            text_fill=TEAL if on else MUTED))
        body.append(text(380, 288, detail, 11, 600, fill=MUTED))
        steps.append(step(n + 1, "".join(body), title[3:].capitalize() + ": " + sub))
    base.append(text(380, 266, "and then round again, which is the whole point",
                     10.5, 600, fill=MUTED))
    desc = ("The development cycle has six phases and it repeats. Analysis asks who the "
            "app is for and what it must do, written down as specific testable "
            "requirements, so \"the user can add a task in two taps\" rather than \"make it "
            "good\". Design plans the screens, the flow between them and the data needed, "
            "using wireframes that are deliberately ugly so discussion stays on layout "
            "rather than colour, and a navigation diagram showing which button leads where. "
            "Implementation is the actual building. Testing checks it works, including with "
            "boundary and erroneous data and when a field is left empty. Evaluation asks "
            "whether it solves the original problem, measured against the requirements "
            "written during analysis. Maintenance fixes problems and adds features, and "
            "then the cycle returns to analysis, which is why real apps update constantly.")
    return figure_steps("ks3-cycle", 760, 304, "".join(base), steps,
                        "The six phase development cycle", desc,
                        "Almost every failed project is one that started at phase three.",
                        labels=[p[0][3:].capitalize() + ": " + p[1] for p in PHASES])


# ============================================= 39. Variables and data types

@diagram("ks3-python-variables")
def _ks3_py_vars():
    """Why input() plus 1 is an error, and what int() fixes."""
    base = [text(380, 24, "The single most common beginner bug", 12, 650, fill=MUTED)]
    L = ["input() always hands back text, even when the user typed a number.",
         "So adding 1 to it is asking Python to add a number to a word.",
         "int() converts the text into a number, and then it works.",
         "The four types you need, and how to tell them apart.",
         "Printing a number next to text needs str(), or a comma."]

    def codebox(x, y, w, lines, accent, soft, h=None):
        h = h or 30 + len(lines) * 22
        o = [box(x, y, w, h, None, fill=soft, stroke=accent, r=10)]
        for i, (s, col) in enumerate(lines):
            o.append(text(x + 16, y + 30 + i * 22, s, 11.5, 500, anchor="start",
                          mono=True, fill=col))
        return "".join(o)

    def memory(x, y, name, value, typ, accent, soft):
        return "".join([
            box(x, y, 230, 92, None, fill=FILL, stroke=LINE, r=10),
            text(x + 115, y + 24, "IN MEMORY", 10.5, 700, fill=MUTED),
            box(x + 24, y + 38, 80, 34, None, fill="var(--dg-fill-2)", stroke=LINE, r=6),
            text(x + 64, y + 60, name, 12, 650, mono=True),
            line(x + 104, y + 55, x + 124, y + 55, stroke=LINE, arrow=True),
            box(x + 128, y + 38, 78, 34, None, fill=soft, stroke=accent, r=6),
            text(x + 167, y + 60, value, 12, 650, mono=True, fill=accent),
            text(x + 115, y + 86, "type: " + typ, 10.5, 600, fill=accent)])

    T = "var(--dg-text)"
    s1 = codebox(30, 62, 380, [('age = input("How old are you? ")', T),
                               ('# the user types 14', MUTED)], TEAL, TEAL_SOFT) \
        + memory(450, 62, "age", '"14"', "str", LILAC, LILAC_SOFT) \
        + text(380, 200, "Those quote marks are the whole problem. 14 went in, "
               '"14" came out.', 11, 650, fill=MUTED)
    s2 = codebox(30, 62, 380, [('age = input("How old are you? ")', T),
                               ('print(age + 1)', WARN)], WARN, WARN_SOFT) \
        + box(450, 62, 230, 92, None, fill=WARN_SOFT, stroke=WARN, r=10) \
        + text(565, 86, "TypeError", 12, 700, fill=WARN) \
        + text(565, 112, "can only concatenate", 10, 500, fill=WARN) \
        + text(565, 130, 'str to str, not int', 10, 500, fill=WARN) \
        + text(380, 200, 'Python will not guess. "14" is a word and 1 is a number.',
               11, 650, fill=MUTED)
    s3 = codebox(30, 62, 380, [('age = int(input("How old are you? "))', T),
                               ('print(age + 1)        # 15', TEAL)], TEAL, TEAL_SOFT) \
        + memory(450, 62, "age", "14", "int", TEAL, TEAL_SOFT) \
        + text(380, 200, "int() around the input. Three characters, and most of your "
               "bugs go away.", 11, 650, fill=MUTED)

    TYPES = [("int", "whole numbers", "7   -3   0"),
             ("float", "numbers with a decimal point", "3.14   1.5"),
             ("str", "text, called a string", '"hello"   "7"'),
             ("bool", "True or False, nothing else", "True   False")]
    s4 = "".join([box(40, 54 + i * 42, 672, 36, None, fill=FILL, stroke=LINE, r=8)
                  + box(54, 61 + i * 42, 68, 22, None, fill=TEAL_SOFT, stroke=TEAL, r=6)
                  + text(88, 77 + i * 42, t, 11.5, 700, fill=TEAL, mono=True)
                  + text(140, 77 + i * 42, meaning, 11, 500, anchor="start")
                  + text(700, 77 + i * 42, ex, 11, 500, anchor="end", mono=True, fill=MUTED)
                  for i, (t, meaning, ex) in enumerate(TYPES)]) \
        + text(380, 236, 'Note the fourth row: "7" is a str and 7 is an int. '
               "They are not the same thing.", 11, 650, fill=MUTED)
    s5 = codebox(30, 56, 672, [
        ('score = 15', T),
        ('print("You scored " + score)       # TypeError', WARN),
        ('print("You scored " + str(score))  # converts it first', TEAL),
        ('print("You scored", score)         # or let the comma do it', TEAL),
    ], LILAC, LILAC_SOFT) \
        + text(380, 214, "A plus sign joins two strings. A comma prints two things "
               "with a space between.", 11, 650, fill=MUTED)

    steps = [step(i + 1, b, L[i]) for i, b in enumerate([s1, s2, s3, s4, s5])]
    desc = ("Why input plus one is an error. The input function always returns text, so "
            "after age equals input, a user who typed fourteen leaves the string quote "
            "fourteen quote in memory, with type str, not the number fourteen. Printing age "
            "plus one then raises a TypeError, because Python will not guess: it cannot add "
            "the number one to a word. Wrapping the input in int converts the text to a "
            "whole number, so age holds fourteen as an int and age plus one gives fifteen. "
            "The four main types are int for whole numbers such as seven or minus three, "
            "float for numbers with a decimal point such as three point one four, str for "
            "text including the digits quote seven quote, and bool for True or False. The "
            "same conversion applies when printing: joining a number onto text with a plus "
            "sign needs str around the number, or you can pass both to print separated by a "
            "comma and Python handles it.")
    return figure_steps("ks3-pyvars", 760, 248, "".join(base), steps,
                        "Input, variables and data types", desc,
                        "If an error message mentions str and int in the same sentence, "
                        "you have forgotten a conversion.", labels=L)


# ===================================================== 40. Loops, traced

@diagram("ks3-python-loop-trace")
def _ks3_loops():
    """What the loop variable actually holds, line by line."""
    base = [text(380, 24, "What the loop variable is doing on each pass",
                 12, 650, fill=MUTED)]
    L = ["A for loop repeats a known number of times, and i changes every pass.",
         "range() decides exactly which numbers i takes.",
         "A while loop repeats until its condition stops being true.",
         "If nothing inside the loop can change the condition, it never stops."]

    def codebox(x, y, w, lines, accent, soft):
        h = 30 + len(lines) * 22
        o = [box(x, y, w, h, None, fill=soft, stroke=accent, r=10)]
        for i, (s, col) in enumerate(lines):
            o.append(text(x + 16, y + 30 + i * 22, s, 11.5, 500, anchor="start",
                          mono=True, fill=col))
        return "".join(o)

    T = "var(--dg-text)"

    def tracetable(x, y, headers, rows, w=(60, 110), accent=TEAL):
        o, cw = [], list(w)
        tw = sum(cw)
        for c, head in enumerate(headers):
            cx = x + sum(cw[:c])
            o.append(box(cx, y, cw[c], 26, None, fill="var(--dg-fill-2)",
                         stroke="var(--dg-line-soft)", r=0))
            o.append(text(cx + cw[c] / 2, y + 18, head, 10.5, 700, fill=MUTED, mono=True))
        for r, row in enumerate(rows):
            for c, cell in enumerate(row):
                cx = x + sum(cw[:c])
                o.append(box(cx, y + 26 + r * 26, cw[c], 26, None, fill=FILL,
                             stroke="var(--dg-line-soft)", r=0))
                o.append(text(cx + cw[c] / 2, y + 44 + r * 26, cell, 10.5, 600, mono=True))
        o.append(text(x + tw / 2, y - 10, "TRACE", 10.5, 700, fill=accent))
        return "".join(o)

    s1 = codebox(30, 60, 330, [('for i in range(5):', T),
                               ('    print("Hello", i)', T)], TEAL, TEAL_SOFT) \
        + tracetable(410, 70, ["i", "printed"],
                     [("0", "Hello 0"), ("1", "Hello 1"), ("2", "Hello 2"),
                      ("3", "Hello 3"), ("4", "Hello 4")]) \
        + text(195, 160, "five passes", 11, 650, fill=TEAL) \
        + text(195, 182, "i starts at 0", 11, 500, fill=MUTED) \
        + text(195, 204, "and never reaches 5", 11, 500, fill=MUTED) \
        + text(380, 256, "range(5) gives five numbers starting at zero, which is why the "
               "last one is 4", 11, 650, fill=MUTED)

    def numline(y, label, nums, accent, soft):
        o = [text(40, y + 6, label, 11.5, 650, anchor="start", mono=True, fill=accent)]
        for k, n in enumerate(nums):
            o.append(box(206 + k * 54, y - 14, 44, 28, None, fill=soft, stroke=accent, r=6))
            o.append(text(228 + k * 54, y + 6, str(n), 11.5, 650, mono=True, fill=accent))
        return "".join(o)
    s2 = numline(80, "range(5)", [0, 1, 2, 3, 4], TEAL, TEAL_SOFT) \
        + numline(136, "range(1, 6)", [1, 2, 3, 4, 5], LILAC, LILAC_SOFT) \
        + numline(192, "range(0, 10, 2)", [0, 2, 4, 6, 8], WARN, WARN_SOFT) \
        + text(380, 240, "start, stop, step. The stop value is never included.",
               11, 650, fill=MUTED) \
        + text(380, 262, "range(1, 6) is the one to use when counting 1 to 5",
               11, 500, fill=MUTED)

    s3 = codebox(30, 56, 350, [('password = ""', T),
                               ('while password != "letmein":', T),
                               ('    password = input("Password: ")', T),
                               ('print("Welcome")', TEAL)], LILAC, LILAC_SOFT) \
        + tracetable(410, 70, ["password", "!= letmein?"],
                     [('""', "True"), ('"cat"', "True"), ('"dog"', "True"),
                      ('"letmein"', "False")], w=(110, 110), accent=LILAC) \
        + text(380, 244, "The condition is checked before every pass, so a wrong "
               "guess simply asks again", 11, 650, fill=MUTED) \
        + text(380, 266, "Use while when you do not know how many repeats you need",
               11, 500, fill=MUTED)

    s4 = codebox(30, 62, 330, [('total = 0', T),
                               ('while total < 10:', WARN),
                               ('    print(total)', T),
                               ('# total never changes', WARN)], WARN, WARN_SOFT) \
        + box(410, 62, 300, 118, None, fill=FILL, stroke=LINE, r=10) \
        + text(560, 86, "INFINITE LOOP", 11, 700, fill=WARN) \
        + _lines(430, 114, ["total is 0 forever, so", "0 < 10 is true forever.",
                            "The program never ends."], size=11, gap=22) \
        + text(380, 216, "Before you run a while loop, find the line inside it that "
               "changes the value being tested.", 11, 650, fill=MUTED) \
        + text(380, 240, "If there isn't one, you have written an infinite loop.",
               11, 500, fill=MUTED)

    steps = [step(i + 1, b, L[i]) for i, b in enumerate([s1, s2, s3, s4])]
    desc = ("What a loop variable holds on each pass. For i in range five, printing Hello "
            "and i, runs five times with i taking the values zero, one, two, three and "
            "four, printing Hello 0 through to Hello 4, so it never reaches five. The range "
            "function takes a start, a stop and a step, and the stop value is never "
            "included: range five gives zero to four, range one to six gives one to five, "
            "and range zero to ten step two gives zero, two, four, six and eight. A while "
            "loop instead repeats as long as its condition is true, so a password loop that "
            "starts with an empty string keeps asking while the entered password does not "
            "equal letmein, and the trace shows the condition true for the empty string, "
            "for cat and for dog, and false once letmein is typed, at which point Welcome "
            "is printed. Use while when you do not know how many repeats are needed. If "
            "nothing inside the loop changes the value being tested, such as a total that "
            "stays at zero while the condition checks total less than ten, the loop runs "
            "forever.")
    return figure_steps("ks3-loops", 760, 280, "".join(base), steps,
                        "for loops, while loops and what the loop variable holds", desc,
                        "In an exam, trace the loop on paper with a two column table. It "
                        "turns a guess into a method.", labels=L)


# ========================================== 41. Lists, 2D lists and dictionaries

@diagram("ks3-list-vs-dict")
def _ks3_collections():
    """Three ways to store more than one thing."""
    base = [text(380, 24, "Three ways to hold more than one value", 12, 650, fill=MUTED)]
    L = ["A list is values in order, reached by their position number.",
         "Counting starts at zero, which is where off by one errors come from.",
         "A 2D list is a list of lists: a grid, reached by row then column.",
         "A dictionary uses a name instead of a position.",
         "Which one to reach for."]

    def cells(x, y, vals, accent, soft, idx=True, w=92, label=None):
        o = []
        for i, v in enumerate(vals):
            cx = x + i * w
            o.append(box(cx, y, w, 42, None, fill=soft, stroke=accent, r=8))
            o.append(text(cx + w / 2, y + 27, str(v), 13, 650, mono=True))
            if idx:
                o.append(text(cx + w / 2, y + 62, "[%d]" % i, 11, 700, fill=accent,
                              mono=True))
        if label:
            o.append(text(x, y - 14, label, 11.5, 650, anchor="start", mono=True,
                          fill=accent))
        return "".join(o)

    s1 = cells(70, 90, [45, 78, 12, 90, 33], TEAL, TEAL_SOFT,
               label="scores = [45, 78, 12, 90, 33]") \
        + text(380, 182, "scores[0] is 45    scores[3] is 90    len(scores) is 5",
               12, 650, fill=TEAL, mono=True) \
        + text(380, 214, "Order is kept, duplicates are allowed, and you can add to or "
               "remove from either end.", 11, 600, fill=MUTED) \
        + text(380, 240, "sum, max, min, len, sorted, append, insert, remove, index",
               11, 500, fill=MUTED, mono=True)
    s2 = cells(70, 90, [45, 78, 12, 90, 33], TEAL, TEAL_SOFT,
               label="scores = [45, 78, 12, 90, 33]") \
        + box(438, 84, 100, 54, None, fill="none", stroke=WARN, r=10, dash="5 4") \
        + text(488, 158, "[3]", 11, 700, fill=WARN, mono=True) \
        + text(380, 190, "The fourth value lives at index 3", 12, 650, fill=WARN) \
        + text(380, 222, "scores[5] does not exist: five values occupy indexes 0 to 4.",
               11, 600, fill=MUTED) \
        + text(380, 246, "IndexError means you asked for a position that is not there.",
               11, 500, fill=MUTED)

    board = [["X", "O", "X"], ["O", "X", "O"], ["X", "O", "X"]]
    g = [text(60, 76, 'board = [["X","O","X"],', 11.5, 650, anchor="start", mono=True,
              fill=LILAC),
         text(60, 98, '         ["O","X","O"],', 11.5, 650, anchor="start", mono=True,
              fill=LILAC),
         text(60, 120, '         ["X","O","X"]]', 11.5, 650, anchor="start", mono=True,
              fill=LILAC)]
    for r in range(3):
        g.append(text(404, 100 + r * 56, "row %d" % r, 10.5, 700, anchor="end", fill=MUTED,
                      mono=True))
        for c in range(3):
            on = (r, c) == (1, 2)
            g.append(box(418 + c * 56, 78 + r * 56, 50, 50, None,
                         fill=WARN_SOFT if on else FILL,
                         stroke=WARN if on else LINE, r=8))
            g.append(text(443 + c * 56, 110 + r * 56, board[r][c], 14, 650, mono=True,
                          fill=WARN if on else "var(--dg-text)"))
    for c in range(3):
        g.append(text(443 + c * 56, 68, "col %d" % c, 10.5, 700, fill=MUTED, mono=True))
    g.append(text(380, 266, 'board[1][2] is "O": row first, then column',
                  12, 650, fill=WARN, mono=True))
    g.append(text(380, 290, "Swapping them round is the most common error in the whole "
                  "topic.", 11, 600, fill=MUTED))
    s3 = "".join(g)

    pairs = [("name", '"Aisha"'), ("year", "9"), ("score", "82")]
    s4 = "".join(
        [text(60, 76, 'student = {"name": "Aisha", "year": 9, "score": 82}', 11.5, 650,
              anchor="start", mono=True, fill=TEAL)]
        + ["".join([box(120, 100 + i * 50, 170, 40, None, fill="var(--dg-fill-2)",
                        stroke=LINE, r=8),
                    text(205, 126 + i * 50, k, 12, 650, mono=True),
                    line(292, 120 + i * 50, 326, 120 + i * 50, stroke=LINE, arrow=True),
                    text(309, 110 + i * 50, "", 10, 500),
                    box(332, 100 + i * 50, 170, 40, None, fill=TEAL_SOFT, stroke=TEAL, r=8),
                    text(417, 126 + i * 50, v, 12, 650, mono=True, fill=TEAL)])
           for i, (k, v) in enumerate(pairs)]
        + [text(205, 92, "KEY", 10.5, 700, fill=MUTED),
           text(417, 92, "VALUE", 10.5, 700, fill=TEAL),
           _lines(530, 118, ['student["name"]', '  gives "Aisha"', "",
                             'student["house"] = "Blue"', "  adds a new pair"],
                  size=10.5, gap=20),
           text(380, 266, 'student["score"] says what it means. scores[2] does not.',
                11, 650, fill=MUTED)])

    rows = [("A set of scores you will sort and total", "list", TEAL, TEAL_SOFT),
            ("A noughts and crosses board, or a seating plan", "2D list", LILAC, LILAC_SOFT),
            ("One person's name, year and score together", "dictionary", TEAL, TEAL_SOFT),
            ("Anything where you would otherwise write a comment", "dictionary",
             TEAL, TEAL_SOFT)]
    s5 = "".join([box(40, 60 + i * 50, 672, 42, None, fill=FILL, stroke=LINE, r=8)
                  + text(60, 86 + i * 50, what, 11.5, 500, anchor="start")
                  + box(566, 68 + i * 50, 130, 26, None, fill=soft, stroke=acc, r=8)
                  + text(631, 86 + i * 50, use, 11.5, 700, fill=acc, mono=True)
                  for i, (what, use, acc, soft) in enumerate(rows)]) \
        + text(380, 282, "A dictionary costs you nothing and makes the code readable six "
               "months later.", 11, 650, fill=MUTED)

    steps = [step(i + 1, b, L[i]) for i, b in enumerate([s1, s2, s3, s4, s5])]
    desc = ("Three ways to store more than one value. A list holds values in order, reached "
            "by position, so for scores equals forty five, seventy eight, twelve, ninety "
            "and thirty three, scores index zero is forty five, scores index three is "
            "ninety, and len of scores is five. Because counting starts at zero, five values "
            "occupy indexes zero to four and asking for index five raises an IndexError. A "
            "2D list is a list of lists forming a grid, so a noughts and crosses board is "
            "three rows of three, and board index one index two means row one then column "
            "two, which is O; getting row and column the wrong way round is the most common "
            "error in the topic. A dictionary stores pairs of keys and values, so student "
            "holds name Aisha, year nine and score eighty two, reached by name rather than "
            "by position, and a new pair such as house Blue can simply be added. Use a list "
            "for a set of values you will sort or total, a 2D list for a grid, and a "
            "dictionary whenever a position number would otherwise need a comment "
            "explaining it.")
    return figure_steps("ks3-coll", 760, 300, "".join(base), steps,
                        "Lists, 2D lists and dictionaries", desc,
                        "If you find yourself writing a comment to remember what index 3 "
                        "was, you wanted a dictionary.", labels=L)
