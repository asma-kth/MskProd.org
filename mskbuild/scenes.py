"""Three dimensional scenes for topics where depth is part of the explanation.

These are plain HTML and CSS 3D transforms. There is no WebGL and no library:
a scene costs a few hundred bytes of markup and reuses the stylesheet the page
already loads, which matters on a revision site that students open on phones.

A scene is used where the thing being taught genuinely has layers, stacking or
position in space. A protocol stack, a memory hierarchy and a polygon mesh are
all easier to hold in your head when you can see them separated and turn them
around. A list of laws is not, and gets a flat diagram instead.

Every scene renders complete and readable with no JavaScript at all: the
stages are all in the markup and only hidden once the controller loads, and
the whole thing is described in full in the text alternative underneath, so a
reader using a screen reader is told what the picture shows rather than that a
picture exists.
"""
from .svg import esc

REGISTRY = {}


def scene(name):
    def wrap(fn):
        REGISTRY[name] = fn
        return fn
    return wrap


def plane(z, title, sub="", tone="teal", extra="", width=None, height=None):
    """One horizontal sheet in the stack, lifted off the floor by z pixels."""
    w = ' style="--sc-z:%dpx%s%s"' % (
        z,
        ";--sc-w:%dpx" % width if width else "",
        ";--sc-hh:%dpx" % height if height else "")
    return ('<div class="sc-plane sc-%s"%s>'
            '<span class="sc-plane-label"><b>%s</b>%s</span>%s</div>'
            % (tone, w, esc(title), '<i>%s</i>' % esc(sub) if sub else "", extra))


def board(w, h, label="", tone="floor"):
    """The flat ground a scene stands on."""
    lab = ('<span class="sc-plane-label"><b>%s</b></span>' % esc(label)) if label else ""
    return ('<div class="sc-plane sc-board sc-%s" style="--sc-z:0px;--sc-w:%dpx;--sc-hh:%dpx">%s</div>'
            % (tone, w, h, lab))


def box3d(x, y, z, w, h, label, sub="", tone="teal", tall=0):
    """A labelled block standing on the board at (x, y), lifted to z.

    `tall` draws a side wall under it so the block reads as having height
    rather than floating, which is what sells the depth on a flat board.
    """
    wall = ('<span class="sc-leg" style="--sc-leg:%dpx"></span>' % tall) if tall else ""
    return ('<div class="sc-box sc-%s" style="--sc-x:%dpx;--sc-y:%dpx;--sc-z:%dpx;'
            '--sc-w:%dpx;--sc-hh:%dpx">%s'
            '<span class="sc-box-label"><b>%s</b>%s</span></div>'
            % (tone, x, y, z, w, h, wall, esc(label),
               '<i>%s</i>' % esc(sub) if sub else ""))


def link3d(x1, y1, x2, y2, z=0, tone="teal", label="", dashed=False):
    """A bus or wire laid on the board between two points.

    The length and angle are worked out here rather than in CSS, because a
    line between two arbitrary points needs real trigonometry and CSS has no
    way to express it.
    """
    import math
    dx, dy = x2 - x1, y2 - y1
    length = math.hypot(dx, dy)
    angle = math.degrees(math.atan2(dy, dx))
    cls = "sc-wire sc-wire-%s%s" % (tone, " is-dashed" if dashed else "")
    tag = ('<span class="sc-wire-tag">%s</span>' % esc(label)) if label else ""
    return ('<div class="%s" style="--sc-x:%dpx;--sc-y:%dpx;--sc-z:%dpx;'
            '--sc-len:%.1fpx;--sc-rot:%.2fdeg">%s</div>'
            % (cls, x1, y1, z, length, angle, tag))


def dot3d(x, y, z, label="", tone="teal", size=14):
    """A travelling marker: a packet, a signal, a value in flight."""
    tag = ('<span class="sc-dot-tag">%s</span>' % esc(label)) if label else ""
    return ('<div class="sc-dot sc-%s" style="--sc-x:%dpx;--sc-y:%dpx;--sc-z:%dpx;'
            '--sc-size:%dpx">%s</div>' % (tone, x, y, z, size, tag))


def billboard(x, y, z, text, tone=""):
    """A caption that always faces the reader, placed in the scene."""
    return ('<div class="sc-note sc-note-at %s" style="--sc-x:%dpx;--sc-y:%dpx;--sc-z:%dpx">%s</div>'
            % (("sc-" + tone) if tone else "", x, y, z, esc(text)))


def stage(n, body, label):
    """One step of the walkthrough."""
    return ('<div class="sc-step" data-step="%d" data-sc-label="%s">%s</div>'
            % (n, esc(label), body))


def figure_scene(name, *, world, steps, title, desc, caption=None,
                 height=340, depth=0, labels=None, hint=None, scale=1.0):
    """Wrap a scene in its figure, controls and text alternative.

    `world` is drawn on every stage, `steps` are the stages. `desc` is the full
    description, which is the picture's content for anyone who cannot see it.
    """
    n = len(steps)
    first = esc(labels[0]) if labels else ""
    controls = ""
    if n > 1:
        controls = (
            '<div class="sc-controls" hidden data-sc-controls>'
            '<button type="button" class="sc-btn" data-sc-prev aria-label="Previous step">Back</button>'
            '<button type="button" class="sc-btn sc-btn-play" data-sc-play '
            'aria-label="Play the animation">Play</button>'
            '<button type="button" class="sc-btn" data-sc-next aria-label="Next step">Next</button>'
            '<p class="sc-status" role="status" aria-live="polite">'
            '<b data-sc-count>Step 1 of %d</b> <span data-sc-text>%s</span></p>'
            '</div>' % (n, first))
    tip = ('<p class="sc-hint" data-sc-hint hidden>%s</p>'
           % esc(hint or "Drag the picture to turn it round. "
                         "With it focused, the arrow keys turn it too.")) if hint is not False else ""
    cap = '<figcaption>%s</figcaption>' % esc(caption) if caption else ""
    return (
        '<figure class="scene" data-scene="%s" style="--sc-h:%dpx;--sc-depth:%dpx;--sc-fit:%s">'
        '<div class="sc-frame"><div class="sc-stage" data-sc-stage>'
        '<div class="sc-world" data-sc-world>%s%s</div>'
        '</div></div>'
        '<p class="sc-alt">%s</p>%s%s%s</figure>'
        % (esc(name), height, depth, ("%.2f" % scale), world, "".join(steps),
           esc(desc), tip, controls, cap))


# ============================================================ the TCP/IP stack

@scene("tcp-ip-stack-3d")
def _tcpip():
    """Four layers, seen as four sheets, with a packet falling through them.

    The whole point of a layered model is that each layer wraps what the one
    above it handed down and knows nothing about the contents. Drawn flat that
    reads as four boxes in a column; drawn as sheets you can see the message
    pass down through them and come back out the other side.
    """
    L = ["Your message starts at the top, in the application.",
         "Transport splits it into segments and adds a port number.",
         "Internet wraps each segment in a packet and adds IP addresses.",
         "Link turns the packet into a frame with MAC addresses, and it goes out.",
         "At the other end the same four layers run in reverse, unwrapping it."]

    LAYERS = [
        (255, "APPLICATION", "HTTP · HTTPS · SMTP", "lilac"),
        (170, "TRANSPORT", "TCP · UDP · ports", "teal"),
        (85, "INTERNET", "IP · routing", "lilac"),
        (0, "LINK", "cables, wifi · MAC", "teal"),
    ]
    world = "".join(plane(z, t, s, tone) for z, t, s, tone in LAYERS)

    # The travelling unit of data. It gains a wrapper at each layer going down.
    WRAPS = [
        (255, "DATA", ["Your message"], "lilac"),
        (170, "SEGMENT", ["TCP", "DATA"], "teal"),
        (85, "PACKET", ["IP", "TCP", "DATA"], "lilac"),
        (0, "FRAME", ["MAC", "IP", "TCP", "DATA"], "teal"),
    ]

    def unit(z, name, parts, tone):
        chips = "".join('<span class="sc-chip sc-chip-%s">%s</span>'
                        % ("head" if i < len(parts) - 1 else "body", esc(p))
                        for i, p in enumerate(parts))
        return ('<div class="sc-unit sc-%s" style="--sc-z:%dpx">'
                '<span class="sc-unit-name">%s</span>'
                '<span class="sc-unit-parts">%s</span></div>' % (tone, z, esc(name), chips))

    steps = []
    for i, (z, nm, parts, tone) in enumerate(WRAPS):
        body = unit(z, nm, parts, tone) + ('<div class="sc-glow" style="--sc-z:%dpx"></div>' % z)
        steps.append(stage(i + 1, body, L[i]))

    # The receiving stack: the same frame climbing back up, shedding wrappers.
    back = (unit(0, "FRAME ARRIVES", ["MAC", "IP", "TCP", "DATA"], "teal")
            + '<div class="sc-arrow sc-arrow-up"></div>'
            + '<div class="sc-note">each layer strips its own wrapper'
              ' and hands the rest up</div>')
    steps.append(stage(5, back, L[4]))

    desc = ("The four layer TCP/IP model drawn as four stacked sheets, with the "
            "application layer on top and the link layer at the bottom. A message "
            "starts at the application layer, where protocols such as HTTP, HTTPS, "
            "SMTP, IMAP and FTP live. It passes down to the transport layer, which "
            "splits it into segments and adds a TCP or UDP header carrying the port "
            "number. Each segment passes down to the internet layer, which wraps it "
            "in a packet and adds the source and destination IP addresses used for "
            "routing. Each packet passes down to the link layer, which wraps it in a "
            "frame carrying MAC addresses and puts it onto the physical network. At "
            "the receiving computer the same four layers run in reverse: each layer "
            "strips off the wrapper it recognises and hands the rest up, so the "
            "application at the top receives exactly the message that was sent. No "
            "layer needs to know how any other layer does its job, which is the "
            "whole reason the model is split up this way.")
    return figure_scene(
        "tcp-ip-stack-3d", world=world, steps=steps,
        title="The TCP/IP stack", desc=desc, height=425, depth=255, labels=L,
        caption="Each layer wraps what the layer above handed it, and knows nothing "
                "about what is inside. That is why you can change the wifi for a "
                "cable without rewriting the web browser.")


# ====================================================== the processor and memory

@scene("cpu-board-3d")
def _cpu_board():
    """The CPU and memory as two chips on a board, with the three buses.

    The buses are the part a flat diagram always fudges. Seen as wires running
    across a board between two chips, it is obvious that an address goes one
    way, data comes back the other, and control runs alongside both.
    """
    L = ["The program counter holds the address of the next instruction.",
         "That address goes to memory along the address bus.",
         "The instruction comes back along the data bus and lands in the MDR.",
         "The control unit decodes it and works out what has to happen.",
         "The ALU executes it, and the program counter moves on by one."]

    base = (board(640, 440)
            + box3d(-150, 30, 10, 280, 250, "", "", "teal")
            + billboard(-150, -110, 30, "CENTRAL PROCESSING UNIT", "teal")
            + box3d(190, -90, 10, 200, 110, "MAIN MEMORY", "RAM", "lilac")
            + box3d(190, 120, 10, 200, 90, "INPUT / OUTPUT", "", "floor")
            + box3d(-230, -40, 26, 100, 48, "PC", "", "floor")
            + box3d(-70, -40, 26, 100, 48, "MAR", "", "floor")
            + box3d(-230, 50, 26, 100, 48, "MDR", "", "floor")
            + box3d(-70, 50, 26, 100, 48, "CIR", "", "floor")
            + box3d(-150, 135, 26, 260, 48, "CU  +  ALU", "", "floor")
            + link3d(-10, -150, 90, -150, 14, "teal", "address")
            + link3d(-10, -100, 90, -100, 14, "lilac", "data")
            + link3d(-10, -50, 90, -50, 14, "teal", "control", dashed=True))

    def hot(x, y, z, w, h, tone="teal"):
        return '<div class="sc-glow sc-glow-at sc-%s" style="--sc-x:%dpx;--sc-y:%dpx;--sc-z:%dpx;--sc-w:%dpx;--sc-hh:%dpx"></div>' % (tone, x, y, z, w, h)

    steps = [
        stage(1, hot(-230, -40, 28, 100, 48) + billboard(-150, 250, 60, "PC holds 0x04A"), L[0]),
        stage(2, hot(-70, -40, 28, 100, 48)
              + dot3d(40, -150, 18, "0x04A")
              + billboard(-150, 250, 60, "address bus: CPU to memory, one way"), L[1]),
        stage(3, hot(-230, 50, 28, 100, 48)
              + dot3d(40, -100, 18, "ADD 12", "lilac")
              + billboard(-150, 250, 60, "data bus: both directions", "lilac"), L[2]),
        stage(4, hot(-70, 50, 28, 100, 48) + hot(-150, 135, 28, 260, 48)
              + billboard(-150, 250, 60, "decode: operation ADD, operand 12"), L[3]),
        stage(5, hot(-150, 135, 28, 260, 48)
              + billboard(-150, 250, 60, "execute, then PC = PC + 1"), L[4]),
    ]
    desc = ("A circuit board carrying the processor on the left and main memory on the "
            "right, joined by three buses. Inside the processor are the program counter, "
            "the memory address register, the memory data register, the current "
            "instruction register and the control unit with the arithmetic logic unit. "
            "The cycle runs like this. The program counter holds the address of the next "
            "instruction, here 0x04A. That address is copied into the memory address "
            "register and travels to memory along the address bus, which carries "
            "addresses in one direction only. Memory sends the instruction back along the "
            "data bus, which carries data in both directions, and it arrives in the memory "
            "data register before being copied to the current instruction register. The "
            "control unit decodes it into an operation and an operand, the arithmetic "
            "logic unit executes it, and the program counter is incremented so the next "
            "pass fetches the following instruction. The control bus runs alongside both, "
            "carrying the signals that say whether this is a read or a write and when each "
            "step may happen.")
    return figure_scene("cpu-board-3d", world=base, steps=steps,
                        title="The CPU, memory and the buses", desc=desc,
                        height=430, depth=30, labels=L, scale=0.78,
                        caption="Address out, data back, control alongside. The address "
                                "bus is one way: memory never sends an address to the CPU.")


@scene("memory-hierarchy-3d")
def _mem_hierarchy():
    """Four tiers as four sheets, widening as they get slower.

    The trade off is the whole idea, and it is a trade between three things at
    once. Stacking the tiers makes the shape of it visible: the useful stuff is
    tiny and fast at the top, enormous and slow at the bottom.
    """
    L = ["Registers: inside the CPU, a few hundred bytes, fastest of all.",
         "Cache: still on the chip, a few megabytes, and very fast.",
         "Main memory: gigabytes, fast, and it empties when the power goes.",
         "Secondary storage: terabytes, slow, and it keeps your files forever.",
         "The whole point: small and fast at the top, huge and slow at the bottom."]

    TIERS = [
        (330, 150, "REGISTERS", "a few hundred bytes · instant", "teal"),
        (220, 250, "CACHE", "a few MB · nanoseconds", "lilac"),
        (110, 350, "MAIN MEMORY (RAM)", "8–32 GB · volatile", "teal"),
        (0, 450, "SECONDARY STORAGE", "1 TB+ · permanent", "lilac"),
    ]
    world = "".join(plane(z, t, s, tone, width=w, height=110)
                    for z, w, t, s, tone in TIERS)
    steps = []
    for i, (z, w, t, s, tone) in enumerate(TIERS):
        steps.append(stage(i + 1,
                           '<div class="sc-glow sc-glow-at sc-%s" style="--sc-x:0px;--sc-y:0px;'
                           '--sc-z:%dpx;--sc-w:%dpx;--sc-hh:110px"></div>' % (tone, z + 2, w),
                           L[i]))
    steps.append(stage(5,
                       billboard(-230, 0, 390, "faster, smaller, dearer per byte", "teal")
                       + billboard(230, 0, -50, "slower, bigger, cheaper per byte", "lilac"),
                       L[4]))
    desc = ("The memory hierarchy drawn as four sheets, narrow at the top and wide at the "
            "bottom. Registers sit inside the processor itself, hold a few hundred bytes "
            "and are the fastest storage in the machine. Cache sits on the processor chip, "
            "holds a few megabytes and answers in nanoseconds, which is why a cache hit "
            "saves so much time. Main memory, the RAM, holds eight to thirty two gigabytes, "
            "is fast but volatile, so everything in it is lost when the power goes off. "
            "Secondary storage, a hard disk or a solid state drive, holds a terabyte or "
            "more, is far slower, and keeps its contents permanently. The pattern running "
            "down the stack is the point: each level down is slower and bigger and cheaper "
            "per byte than the one above it, and that is exactly why a computer has all "
            "four instead of just one.")
    return figure_scene("memory-hierarchy-3d", world=world, steps=steps,
                        title="The memory hierarchy", desc=desc,
                        height=445, depth=330, labels=L, scale=0.74,
                        caption="Every level down is bigger, slower and cheaper per byte. "
                                "If one kind of memory were fast, huge and cheap, there "
                                "would only be one kind.")


# ================================================================== networks

@scene("network-topologies-3d")
def _topologies():
    """Star, mesh and bus, laid out in space rather than on a flat page."""
    L = ["Star: every device has its own cable to a central switch.",
         "If one cable fails, only that one device drops off.",
         "Mesh: every device connects to every other, with no centre at all.",
         "Any one link can fail and the data simply goes a different way.",
         "Bus: one shared backbone, and every device taps into it."]

    import math
    R = 130
    pts = [(round(R * math.cos(math.radians(a))), round(R * math.sin(math.radians(a))))
           for a in (90, 162, 234, 306, 18)]

    def nodes(tone="floor", skip=None):
        return "".join(box3d(x, y, 16, 74, 42, "PC %d" % (i + 1), "", tone)
                       for i, (x, y) in enumerate(pts) if i != skip)

    star = (board(420, 330) + nodes()
            + box3d(0, 0, 22, 96, 50, "SWITCH", "", "teal")
            + "".join(link3d(0, 0, x, y, 14, "teal") for x, y in pts))
    star_fail = (board(420, 330) + nodes()
                 + box3d(0, 0, 22, 96, 50, "SWITCH", "", "teal")
                 + "".join(link3d(0, 0, x, y, 14, "teal")
                           for i, (x, y) in enumerate(pts) if i != 2)
                 + link3d(0, 0, pts[2][0], pts[2][1], 14, "lilac", "broken", dashed=True))

    mesh_links = [(i, j) for i in range(5) for j in range(i + 1, 5)]
    mesh = (board(420, 330) + nodes()
            + "".join(link3d(pts[i][0], pts[i][1], pts[j][0], pts[j][1], 14, "lilac")
                      for i, j in mesh_links))
    mesh_fail = (board(420, 330) + nodes()
                 + "".join(link3d(pts[i][0], pts[i][1], pts[j][0], pts[j][1], 14,
                                  "teal" if (i, j) == (0, 2) else "lilac",
                                  dashed=((i, j) == (0, 3)))
                           for i, j in mesh_links)
                 + billboard(0, 170, 90, "one link down, the data goes round", "teal"))

    bus_pts = [(-150, -60), (-50, -60), (50, -60), (150, -60)]
    bus = (board(420, 330)
           + "".join(box3d(x, y, 16, 74, 42, "PC %d" % (i + 1)) for i, (x, y) in enumerate(bus_pts))
           + link3d(-190, 40, 190, 40, 14, "teal", "the backbone")
           + "".join(link3d(x, y + 24, x, 40, 14, "teal") for x, y in bus_pts)
           + billboard(0, 110, 60, "one break splits the whole network in two", "lilac"))

    steps = [stage(1, star, L[0]), stage(2, star_fail, L[1]),
             stage(3, mesh, L[2]), stage(4, mesh_fail, L[3]), stage(5, bus, L[4])]
    desc = ("Three network topologies laid out in space. In a star, every device has its "
            "own cable running to a central switch, so performance stays high because no "
            "device shares its cable, and a single cable failure takes out only the one "
            "device attached to it. The cost is that it needs a lot of cable and that the "
            "switch is a single point of failure for the whole network. In a mesh, every "
            "device is connected directly to every other device and there is no centre at "
            "all, so any one link can fail and the traffic simply takes another route, "
            "which is why the internet is built this way. The cost is an enormous amount "
            "of cable: five devices already need ten links. In a bus, every device taps "
            "into one shared backbone cable, which is cheap and uses very little cable, "
            "but all devices share the bandwidth, collisions happen as traffic rises, and "
            "one break in the backbone splits the network in two.")
    return figure_scene("network-topologies-3d", world="", steps=steps,
                        title="Star, mesh and bus topologies", desc=desc,
                        height=380, depth=0, labels=L, scale=0.9,
                        caption="Star for a school or an office, mesh for anything that "
                                "has to survive a failure. The internet is a mesh.")


# ====================================================== binary place value

@scene("binary-place-value-3d")
def _place_value():
    """The place value columns as blocks whose height is their value.

    Written flat, 128 64 32 16 8 4 2 1 is just a row of numbers to memorise.
    Given height, the doubling is something you can see, and it becomes obvious
    why the left hand bit is worth more than all the others put together.
    """
    L = ["Eight columns, and each one is worth double the one to its right.",
         "A 1 means take that column's value. A 0 means skip it.",
         "Add up the columns you took: 64 + 16 + 8 + 2 = 90.",
         "The leftmost bit is worth more than every other bit added together."]

    VALUES = [128, 64, 32, 16, 8, 4, 2, 1]
    BITS = [0, 1, 0, 1, 1, 0, 1, 0]          # 0101 1010 = 90

    def columns(show_bits=False, only_on=False, highlight_msb=False):
        out = []
        for i, v in enumerate(VALUES):
            x = -192 + i * 55
            on = BITS[i] == 1
            if only_on and not on:
                out.append(box3d(x, 0, 6, 46, 46, "0", "", "floor"))
                continue
            h = int(14 + v * 0.62)
            tone = "lilac" if (highlight_msb and i == 0) else ("teal" if on or not show_bits else "floor")
            out.append(box3d(x, 0, h, 46, 46, str(v), "", tone, tall=h))
            if show_bits:
                out.append(billboard(x, -46, h + 30, "1" if on else "0",
                                     "teal" if on else ""))
        return board(520, 160) + "".join(out)

    steps = [
        stage(1, columns(), L[0]),
        stage(2, columns(show_bits=True), L[1]),
        stage(3, columns(show_bits=True, only_on=True)
              + billboard(0, 95, 160, "0101 1010 = 90"), L[2]),
        stage(4, columns(highlight_msb=True)
              + billboard(0, 95, 160, "128  >  64+32+16+8+4+2+1  =  127", "lilac"), L[3]),
    ]
    desc = ("The eight place value columns of a byte, drawn as blocks whose height is the "
            "value of the column: 128, 64, 32, 16, 8, 4, 2 and 1 from left to right, each "
            "one worth double the column to its right. To read a binary number, take the "
            "value of every column holding a 1 and ignore every column holding a 0. For "
            "0101 1010 that means taking 64, 16, 8 and 2, which add up to 90. The tallest "
            "block shows something worth remembering: the leftmost bit is worth 128, which "
            "is more than 64 plus 32 plus 16 plus 8 plus 4 plus 2 plus 1, the sum of every "
            "other column, which comes to 127. That is why flipping the leftmost bit "
            "changes the number more than flipping all the others together, and it is also "
            "why eight bits can hold 0 to 255 and no further.")
    return figure_scene("binary-place-value-3d", world="", steps=steps,
                        title="Binary place values", desc=desc,
                        height=370, depth=90, labels=L, scale=0.88,
                        caption="Each column doubles. Learn the row 128 64 32 16 8 4 2 1 "
                                "and every conversion question becomes adding up.")
