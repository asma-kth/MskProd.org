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


def box3d(x, y, z, w, h, label, sub="", tone="teal", tall=0, round=False):
    """A labelled block standing on the board at (x, y), lifted to z.

    `tall` draws a side wall under it so the block reads as having height
    rather than floating, which is what sells the depth on a flat board.
    """
    wall = ('<span class="sc-leg" style="--sc-leg:%dpx"></span>' % tall) if tall else ""
    return ('<div class="sc-box sc-%s%s" style="--sc-x:%dpx;--sc-y:%dpx;--sc-z:%dpx;'
            '--sc-w:%dpx;--sc-hh:%dpx">%s'
            '<span class="sc-box-label"><b>%s</b>%s</span></div>'
            % (tone, " is-round" if round else "", x, y, z, w, h, wall, esc(label),
               '<i>%s</i>' % esc(sub) if sub else ""))


def cube3d(size, cx=0, cy=0, cz=0, verts=False, edges=False, faces=False,
           tone="teal"):
    """A real cube: six faces, twelve edges, eight vertices, in actual 3D.

    This is the one topic where the medium is the subject. A 3D model is built
    from vertices joined by edges enclosing faces, and here those are the
    literal parts of the drawing rather than a picture of them.
    """
    h = size / 2.0
    out = []
    if faces:
        spec = [("", 0, 0), ("rotateY(180deg)", 0, 0), ("rotateY(90deg)", 0, 0),
                ("rotateY(-90deg)", 0, 0), ("rotateX(90deg)", 0, 0),
                ("rotateX(-90deg)", 0, 0)]
        for rot, _, _ in spec:
            out.append('<div class="sc-face sc-%s" style="--sc-x:%dpx;--sc-y:%dpx;'
                       '--sc-z:%dpx;--sc-s:%dpx;--sc-rot3:%s translateZ(%dpx)"></div>'
                       % (tone, cx, cy, cz, size, rot or "rotateX(0deg)", h))
    if edges:
        for axis in ("x", "y", "z"):
            for a in (-h, h):
                for b in (-h, h):
                    if axis == "x":
                        p, rot = (cx, cy + a, cz + b), "rotateX(0deg)"
                    elif axis == "y":
                        p, rot = (cx + a, cy, cz + b), "rotateZ(90deg)"
                    else:
                        p, rot = (cx + a, cy + b, cz), "rotateY(90deg)"
                    out.append('<div class="sc-edge sc-edge-%s" style="--sc-x:%dpx;'
                               '--sc-y:%dpx;--sc-z:%dpx;--sc-len:%dpx;--sc-rot3:%s"></div>'
                               % (tone, p[0], p[1], p[2], size, rot))
    if verts:
        for dx in (-h, h):
            for dy in (-h, h):
                for dz in (-h, h):
                    out.append(dot3d(int(cx + dx), int(cy + dy), int(cz + dz),
                                     "", tone, 13))
    return "".join(out)


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


@scene("client-server-3d")
def _client_server():
    """Clients round a server, then the same machines with no server at all."""
    import math
    L = ["Client server: every device asks one central machine for what it needs.",
         "The server holds the files, does the work and checks who you are.",
         "Peer to peer: no server, and every machine is both client and server.",
         "Lose the server and a client server network stops. A peer network does not."]
    pts = [(round(150 * math.cos(math.radians(a))), round(150 * math.sin(math.radians(a))))
           for a in (90, 162, 234, 306, 18)]

    def clients(tone="floor"):
        return "".join(box3d(x, y, 16, 80, 44, "Client %d" % (i + 1), "", tone)
                       for i, (x, y) in enumerate(pts))

    cs = (board(460, 360) + clients()
          + "".join(link3d(0, 0, x, y, 12, "teal") for x, y in pts)
          + box3d(0, 0, 26, 120, 60, "SERVER", "", "teal"))
    cs2 = (cs + billboard(0, 235, 30, "files · printing · logins · backups", "teal"))
    p2p = (board(460, 360)
           + "".join(box3d(x, y, 16, 80, 44, "Peer %d" % (i + 1), "", "lilac")
                     for i, (x, y) in enumerate(pts))
           + "".join(link3d(pts[i][0], pts[i][1], pts[j][0], pts[j][1], 12, "lilac")
                     for i in range(5) for j in range(i + 1, 5))
           + billboard(0, 235, 30, "every machine shares with every other", "lilac"))
    gone = (board(460, 360) + clients()
            + billboard(0, 0, 60, "server down: nobody can work", "teal")
            + billboard(0, 235, 30, "a peer network would carry on", "lilac"))

    steps = [stage(1, cs, L[0]), stage(2, cs2, L[1]), stage(3, p2p, L[2]), stage(4, gone, L[3])]
    desc = ("Two ways of organising a network. In a client server network, five client "
            "machines all connect to one central server, which stores the files, does the "
            "heavy processing, handles printing, checks logins and runs the backups. That "
            "makes everything central: one place to back up, one place to set security, "
            "one place to update. It also makes the server a single point of failure, so "
            "when it goes down nobody can work, and it is expensive and needs managing. "
            "In a peer to peer network there is no server at all. Every machine is both "
            "client and server, sharing its own files directly with the others, which is "
            "cheap, needs no specialist to run and keeps working when any one machine is "
            "switched off. The cost is that files are scattered across machines, backups "
            "are nobody's job in particular, and performance drops as machines get busy.")
    return figure_scene("client-server-3d", world="", steps=steps,
                        title="Client server and peer to peer", desc=desc,
                        height=380, depth=0, labels=L, scale=0.88,
                        caption="A school uses client server because somebody has to "
                                "control logins and back work up. Sharing music between "
                                "phones is peer to peer.")


@scene("packet-journey-3d")
def _packet_journey():
    """One message, split into packets, each taking its own way across a mesh."""
    L = ["Your message is too big to send in one go, so it is split into packets.",
         "Every packet carries the destination address and its own number.",
         "Each router picks the next hop, so packets can take different routes.",
         "They arrive out of order, and the numbers put them back together."]
    R = [(-190, 60), (-70, -80), (60, 70), (190, -60), (0, -10), (120, -120)]

    def mesh():
        out = [board(520, 330)]
        for i, (x, y) in enumerate(R):
            out.append(box3d(x, y, 16, 72, 40, "R%d" % (i + 1), "", "floor"))
        pairs = [(0, 1), (0, 4), (1, 4), (1, 5), (4, 2), (4, 3), (2, 3), (3, 5), (1, 2)]
        for i, j in pairs:
            out.append(link3d(R[i][0], R[i][1], R[j][0], R[j][1], 12, "floorwire"))
        return "".join(out)

    base = mesh() + box3d(-215, 125, 20, 94, 48, "YOU", "", "teal") \
                  + box3d(215, -125, 20, 94, 48, "SERVER", "", "lilac")
    s1 = base + billboard(0, 225, 40, "one 3 MB photo → about 2,000 packets", "teal")
    s2 = (base + dot3d(-190, 60, 30, "1 of 3", 16)
          + dot3d(-150, 20, 30, "2 of 3", 16) + dot3d(-110, -20, 30, "3 of 3", 16)
          + billboard(0, 225, 40, "each packet: address, number, and a slice of the data", "teal"))
    s3 = (base
          + link3d(R[0][0], R[0][1], R[4][0], R[4][1], 22, "teal")
          + link3d(R[4][0], R[4][1], R[3][0], R[3][1], 22, "teal")
          + link3d(R[0][0], R[0][1], R[1][0], R[1][1], 22, "lilac")
          + link3d(R[1][0], R[1][1], R[5][0], R[5][1], 22, "lilac")
          + link3d(R[5][0], R[5][1], R[3][0], R[3][1], 22, "lilac")
          + billboard(0, 225, 40, "two packets, two routes, same destination"))
    s4 = (base + dot3d(230, -105, 30, "3", 16) + dot3d(255, -70, 30, "1", 16)
          + dot3d(205, -70, 30, "2", 16)
          + billboard(0, 225, 40, "out of order on arrival, reassembled by number", "lilac"))
    steps = [stage(1, s1, L[0]), stage(2, s2, L[1]), stage(3, s3, L[2]), stage(4, s4, L[3])]
    desc = ("How packet switching moves a message across a network. The message is far "
            "too big to send as one lump, so it is split into packets: a three megabyte "
            "photograph becomes roughly two thousand of them. Each packet carries the "
            "destination address, the address it came from, its own sequence number and a "
            "slice of the data, plus a checksum used to spot corruption. Each router it "
            "reaches reads the destination and chooses the next hop based on how busy the "
            "links are at that moment, so two packets from the same message can take "
            "completely different routes through the network. That is the strength of the "
            "method: there is no fixed line to tie up and no single route to break. The "
            "packets therefore arrive out of order, and the receiving computer uses the "
            "sequence numbers to put them back in order, asking for any that never "
            "arrived to be sent again.")
    return figure_scene("packet-journey-3d", world="", steps=steps,
                        title="A packet's journey across a network", desc=desc,
                        height=400, depth=30, labels=L, scale=0.85,
                        caption="Nothing reserves a line for you. Every packet is handled "
                                "on its own, and that is why the internet copes when part "
                                "of it fails.")


@scene("image-layers-3d")
def _image_layers():
    """A bitmap taken apart: pixels, then channels, then bits."""
    L = ["A bitmap is a grid of pixels. This one is 8 by 8, so 64 of them.",
         "Pick one pixel. Its colour is three numbers: red, green and blue.",
         "Each number is 8 bits, so one pixel costs 24 bits, which is 3 bytes.",
         "File size = width × height × colour depth. That is the whole formula."]

    import math
    def grid(z=0, tone_of=None):
        out = []
        for r in range(8):
            for c in range(8):
                on = ((r - 3.5) ** 2 + (c - 3.5) ** 2) <= 10
                out.append(box3d(-140 + c * 40, -140 + r * 40, z, 34, 34, "", "",
                                 (tone_of(r, c) if tone_of else ("teal" if on else "floor"))))
        return "".join(out)

    s1 = board(380, 380) + grid() + billboard(0, 240, 30, "8 × 8 = 64 pixels")
    one = (board(380, 380)
           + grid(tone_of=lambda r, c: "teal" if (r, c) == (2, 5) else "floor")
           + box3d(60, -60, 70, 44, 44, "", "", "teal")
           + billboard(60, -60, 130, "one pixel", "teal"))
    s2 = one
    s3 = (board(380, 380)
          + box3d(0, 0, 40, 220, 160, "RED", "1 0 1 1 0 0 1 0", "lilac")
          + box3d(0, 0, 130, 220, 160, "GREEN", "0 1 1 0 1 1 0 1", "teal")
          + box3d(0, 0, 220, 220, 160, "BLUE", "0 0 1 1 1 0 1 0", "lilac")
          + billboard(0, 255, 30, "8 + 8 + 8 = 24 bits for one pixel", "teal"))
    s4 = (board(380, 380)
          + billboard(0, -60, 150, "64 pixels × 24 bits = 1,536 bits")
          + billboard(0, 0, 100, "1,536 ÷ 8 = 192 bytes", "teal")
          + billboard(0, 60, 50, "add a few bytes of metadata on top", "lilac"))
    steps = [stage(1, s1, L[0]), stage(2, s2, L[1]), stage(3, s3, L[2]), stage(4, s4, L[3])]
    desc = ("How a bitmap image is stored. The image is a grid of pixels, and this one is "
            "eight by eight, so sixty four pixels in total. Every pixel holds one colour, "
            "and that colour is stored as three numbers: how much red, how much green and "
            "how much blue. In 24 bit colour each of those three numbers gets eight bits, "
            "so one pixel costs 8 plus 8 plus 8, which is 24 bits or 3 bytes. The colour "
            "depth is simply how many bits each pixel gets: more bits means more possible "
            "colours, and 24 bits gives about 16.7 million of them. File size is therefore "
            "width times height times colour depth: 64 pixels times 24 bits is 1,536 bits, "
            "which divided by 8 is 192 bytes, plus a small amount of metadata recording "
            "the dimensions, the colour depth and when the picture was taken. Doubling "
            "both the width and the height multiplies the file size by four, because it "
            "is four times as many pixels.")
    return figure_scene("image-layers-3d", world="", steps=steps,
                        title="How a bitmap image is stored", desc=desc,
                        height=420, depth=220, labels=L, scale=0.8,
                        caption="Width times height times colour depth gives bits. Divide "
                                "by 8 for bytes. Every image file size question is that "
                                "line and nothing more.")


@scene("sound-sampling-3d")
def _sound_3d():
    """Sampling drawn as bars standing on a timeline."""
    import math
    L = ["Sound is a wave: a smooth, continuous change in air pressure.",
         "A computer cannot store smooth. It measures the height at intervals.",
         "Sample more often and the shape you recorded is closer to the original.",
         "Bit depth is how finely each measurement is rounded."]

    def wave(n, tone="teal", z0=0, show_steps=False, levels=0):
        out = []
        span = 460.0
        for i in range(n):
            t = i / float(n - 1)
            x = int(-span / 2 + t * span)
            v = math.sin(t * math.pi * 1.6) * 0.5 + 0.5
            if levels:
                v = round(v * (levels - 1)) / float(levels - 1)
            h = int(16 + v * 150)
            out.append(box3d(x, 0, h, max(8, int(span / n) - 6), 30, "", "", tone, tall=h))
        return "".join(out)

    base = board(540, 150)
    s1 = base + wave(44, "lilac") + billboard(0, 110, 200, "the original wave, smooth", "lilac")
    s2 = (base + wave(11, "teal")
          + billboard(0, 110, 200, "11 samples: the shape is rough", "teal"))
    s3 = (base + wave(30, "teal")
          + billboard(0, 110, 200, "30 samples: closer, and a bigger file", "teal"))
    s4 = (base + wave(30, "teal", levels=4)
          + billboard(0, 110, 200, "only 4 levels to round to: 2 bit depth", "lilac"))
    steps = [stage(1, s1, L[0]), stage(2, s2, L[1]), stage(3, s3, L[2]), stage(4, s4, L[3])]
    desc = ("How a sound is turned into numbers. Sound is a wave, a smooth and continuous "
            "change in air pressure, and a computer cannot store smooth because it can "
            "only store numbers. So it measures the height of the wave at regular "
            "intervals, and each measurement is a sample. The sample rate is how many "
            "measurements are taken each second, in hertz: with only eleven samples the "
            "recorded shape is a rough approximation of the original, and with thirty it "
            "is much closer, at the cost of a bigger file. CD audio uses 44,100 samples a "
            "second. The bit depth, sometimes called the sample resolution, is how many "
            "bits each measurement gets, which decides how finely it can be rounded: with "
            "only two bits there are four levels to round to and the result is coarse and "
            "distorted, while sixteen bits gives 65,536 levels and sounds accurate. File "
            "size is sample rate times bit depth times the number of seconds, times two "
            "for stereo.")
    return figure_scene("sound-sampling-3d", world="", steps=steps,
                        title="Sampling a sound wave", desc=desc,
                        height=390, depth=170, labels=L, scale=0.85,
                        caption="Higher sample rate and higher bit depth both mean a "
                                "closer recording and a bigger file. That trade is the "
                                "whole topic.")


@scene("secondary-storage-3d")
def _secondary():
    """The three technologies, as the three different physical things they are."""
    L = ["Magnetic: spinning platters with a head floating over the surface.",
         "Solid state: a grid of cells holding charge, with no moving parts.",
         "Optical: one spiral track of pits and lands, read by a laser.",
         "Which one depends on capacity, speed, durability and cost per gigabyte."]

    hdd = (board(420, 330)
           + "".join(box3d(0, 0, 20 + i * 36, 190, 190, "", "", "floor", round=True)
                     for i in range(3))
           + box3d(0, 0, 128, 190, 190, "", "", "teal", round=True)
           + box3d(120, -10, 140, 110, 22, "read/write head", "", "lilac")
           + billboard(0, 215, 40, "platters spin, the head moves in and out", "teal"))
    ssd = (board(420, 330)
           + "".join(box3d(-150 + c * 60, -90 + r * 60, 24, 50, 50, "", "",
                           "teal" if (r * 6 + c) % 3 else "floor")
                     for r in range(4) for c in range(6))
           + billboard(0, 215, 40, "no moving parts, so nothing to wear out", "teal"))
    opt = (board(420, 330)
           + box3d(0, 0, 20, 230, 230, "", "", "floor", round=True)
           + box3d(0, 0, 26, 70, 70, "", "", "floor", round=True)
           + "".join(box3d(-90 + i * 26, 0, 32, 14, 14, "", "", "lilac") for i in range(8))
           + billboard(0, 215, 40, "pits and lands in one long spiral", "lilac"))
    cmp_ = (board(420, 330)
            + box3d(-130, 0, 30, 150, 90, "MAGNETIC", "cheapest per GB", "floor", tall=30)
            + box3d(30, 0, 70, 150, 90, "SOLID STATE", "fastest, no moving parts", "teal", tall=70)
            + box3d(190, 0, 20, 150, 90, "OPTICAL", "cheap to post", "lilac", tall=20)
            + billboard(0, 215, 40, "height here is speed, not capacity"))
    steps = [stage(1, hdd, L[0]), stage(2, ssd, L[1]), stage(3, opt, L[2]), stage(4, cmp_, L[3])]
    desc = ("The three kinds of secondary storage, as the three different physical things "
            "they actually are. A magnetic hard disk drive is a stack of spinning platters "
            "coated in magnetic material, with a read write head floating just above the "
            "surface and moving in and out to reach different tracks. It is the cheapest "
            "per gigabyte and comes in the largest capacities, but it is slow, it is noisy, "
            "it uses more power, and because it has moving parts a knock while it is "
            "running can destroy it. A solid state drive is a grid of flash memory cells "
            "that hold an electrical charge, with no moving parts at all, which makes it "
            "far faster to start up and to find data, silent, more durable and more power "
            "efficient, at a higher price per gigabyte and with a limit on how many times "
            "each cell can be rewritten. Optical media such as a CD, DVD or Blu-ray stores "
            "data as pits and lands along one long spiral track, read by a laser. It is "
            "very cheap, light and easy to post, but it is slow, holds little, and "
            "scratches easily.")
    return figure_scene("secondary-storage-3d", world="", steps=steps,
                        title="Magnetic, solid state and optical storage", desc=desc,
                        height=400, depth=130, labels=L, scale=0.82,
                        caption="Exam answers need the reason, not the name: no moving "
                                "parts is why an SSD survives being dropped and starts up "
                                "faster.")


# ============================================================ logic and data

@scene("logic-circuit-3d")
def _logic_circuit():
    """A two gate circuit with the signal actually travelling through it."""
    L = ["Two inputs, one AND gate, one NOT gate, one output.",
         "A = 1 and B = 0. AND needs both, so it gives 0.",
         "NOT flips it, so Q becomes 1.",
         "A = 1 and B = 1. AND gives 1, NOT flips it, Q is 0.",
         "Q = NOT (A AND B). That is a NAND gate, written out."]

    def circuit(a, b, mid, q, lit=()):
        def tone(n):
            return "teal" if n in lit else "floor"
        return (board(620, 240)
                + box3d(-230, -50, 20, 70, 44, "A", str(a), tone("A"))
                + box3d(-230, 50, 20, 70, 44, "B", str(b), tone("B"))
                + link3d(-195, -50, -70, -25, 16, "teal" if a else "floorwire")
                + link3d(-195, 50, -70, 25, 16, "teal" if b else "floorwire")
                + box3d(-20, 0, 24, 100, 70, "AND", str(mid) if mid is not None else "",
                        tone("AND"))
                + link3d(30, 0, 110, 0, 16, "teal" if mid else "floorwire")
                + box3d(150, 0, 24, 90, 60, "NOT", "", tone("NOT"))
                + link3d(195, 0, 250, 0, 16, "teal" if q else "floorwire")
                + box3d(262, 0, 20, 70, 44, "Q", str(q) if q is not None else "", tone("Q")))

    steps = [
        stage(1, circuit("", "", None, None), L[0]),
        stage(2, circuit(1, 0, 0, None, lit=("A", "AND"))
              + billboard(0, 170, 40, "AND needs both inputs to be 1"), L[1]),
        stage(3, circuit(1, 0, 0, 1, lit=("A", "AND", "NOT", "Q"))
              + billboard(0, 170, 40, "NOT turns the 0 into a 1", "teal"), L[2]),
        stage(4, circuit(1, 1, 1, 0, lit=("A", "B", "AND", "NOT"))
              + billboard(0, 170, 40, "both inputs 1, so Q is 0", "lilac"), L[3]),
        stage(5, circuit("A", "B", "A AND B", "Q")
              + billboard(0, 170, 40, "Q = NOT (A AND B)", "teal"), L[4]),
    ]
    desc = ("A circuit with two inputs, A and B, feeding an AND gate whose output feeds a "
            "NOT gate, which produces the output Q. The AND gate outputs 1 only when both "
            "its inputs are 1, so with A set to 1 and B set to 0 it outputs 0. The NOT "
            "gate inverts whatever it is given, so that 0 becomes a 1 and Q is 1. Setting "
            "both A and B to 1 makes the AND gate output 1, the NOT gate inverts it, and Q "
            "becomes 0. The whole circuit is therefore Q equals NOT, bracket, A AND B, "
            "bracket, and it gives 1 in every case except when both inputs are 1. That "
            "combination is common enough to have its own name and its own symbol: it is "
            "a NAND gate. When reading a circuit in an exam, work left to right and write "
            "the value on every wire as you go, because the marks are for the "
            "intermediate columns as much as the answer.")
    return figure_scene("logic-circuit-3d", world="", steps=steps,
                        title="Tracing a signal through a logic circuit", desc=desc,
                        height=350, depth=30, labels=L, scale=0.86,
                        caption="Label every wire as you go. An intermediate column in a "
                                "truth table is a mark, and it is also how you catch your "
                                "own mistake.")


@scene("stack-queue-3d")
def _stack_queue():
    """A stack is a pile. A queue is a line. Drawn as a pile and a line."""
    L = ["A stack is a pile. New items go on the top.",
         "Push another one and it goes on top again.",
         "Pop takes the top one off, so the last in is the first out.",
         "A queue is a line. New items join the back.",
         "Dequeue takes from the front, so the first in is the first out."]

    def stack(items, tag=None, tagz=0):
        out = [board(300, 200)]
        for i, v in enumerate(items):
            out.append(box3d(0, 0, 14 + i * 46, 150, 80, v, "", "teal" if i == len(items) - 1 else "floor"))
        if tag:
            out.append(billboard(0, 150, tagz, tag, "teal"))
        return "".join(out)

    def queue(items, front=0, tag=None):
        out = [board(560, 190)]
        for i, v in enumerate(items):
            x = -210 + i * 105
            out.append(box3d(x, 0, 18, 92, 78, v, "", "teal" if i == front else "floor"))
        out.append(billboard(-270, 0, 90, "front"))
        out.append(billboard(270, 0, 90, "back"))
        if tag:
            out.append(billboard(0, 150, 40, tag, "teal"))
        return "".join(out)

    steps = [
        stage(1, stack(["first", "second"], "push adds to the top", 40), L[0]),
        stage(2, stack(["first", "second", "third"], "push: third goes on top", 40), L[1]),
        stage(3, stack(["first", "second"], "pop returned third: last in, first out", 40), L[2]),
        stage(4, queue(["A", "B", "C", "D"], 0, "enqueue adds to the back"), L[3]),
        stage(5, queue(["B", "C", "D"], 0, "dequeue returned A: first in, first out"), L[4]),
    ]
    desc = ("Two linear data structures, drawn as the two physical things they are named "
            "after. A stack is a pile: items are pushed onto the top and popped off the "
            "top, so the last item in is the first one out, which is called LIFO. Pushing "
            "first, then second, then third gives a pile with third on top, and popping "
            "returns third. Only the top item can be reached, and a pointer records where "
            "the top is. Stacks are what a computer uses to remember where to return to "
            "after a subroutine call, and what an undo feature is built on. A queue is a "
            "line: items are enqueued at the back and dequeued from the front, so the "
            "first item in is the first one out, which is called FIFO. With A, B, C and D "
            "in the queue, dequeuing returns A. Two pointers are needed, one for the front "
            "and one for the back. Queues are used for print jobs, for keyboard input and "
            "for scheduling processes, anywhere that fairness matters.")
    return figure_scene("stack-queue-3d", world="", steps=steps,
                        title="Stacks and queues", desc=desc,
                        height=390, depth=120, labels=L, scale=0.9,
                        caption="LIFO and FIFO are not jargon to memorise. A stack of "
                                "plates and a queue at a shop behave exactly like this.")


@scene("binary-tree-3d")
def _tree_3d():
    """A binary search tree, and the path a search takes through it."""
    L = ["A binary tree: every node has at most two children.",
         "In a binary search tree, smaller goes left and larger goes right.",
         "Searching for 37: start at the root and compare.",
         "37 is less than 50, so go left. More than 30, so go right. Found.",
         "Three comparisons for seven items. That is why trees are fast."]

    N = {50: (0, -110), 30: (-150, 10), 70: (150, 10),
         20: (-230, 130), 37: (-70, 130), 60: (70, 130), 90: (230, 130)}
    EDGES = [(50, 30), (50, 70), (30, 20), (30, 37), (70, 60), (70, 90)]

    def tree(lit=(), path=()):
        out = [board(600, 330)]
        for a, b in EDGES:
            tone = "teal" if (a, b) in path else "floorwire"
            out.append(link3d(N[a][0], N[a][1], N[b][0], N[b][1], 12, tone))
        for v, (x, y) in N.items():
            out.append(box3d(x, y, 20, 66, 46, str(v), "", "teal" if v in lit else "floor"))
        return "".join(out)

    steps = [
        stage(1, tree() + billboard(0, 215, 40, "root at the top, leaves at the bottom"), L[0]),
        stage(2, tree() + billboard(-230, -110, 60, "smaller", "lilac")
              + billboard(230, -110, 60, "larger", "teal"), L[1]),
        stage(3, tree(lit=(50,)) + billboard(0, 215, 40, "37 < 50", "teal"), L[2]),
        stage(4, tree(lit=(50, 30, 37), path=((50, 30), (30, 37)))
              + billboard(0, 240, 20, "37 > 30, so right. Found.", "teal"), L[3]),
        stage(5, tree(lit=(50, 30, 37), path=((50, 30), (30, 37)))
              + billboard(0, 240, 20, "7 items, at most 3 comparisons", "lilac"), L[4]),
    ]
    desc = ("A binary search tree holding the values 50, 30, 70, 20, 37, 60 and 90. Every "
            "node has at most two children, the node at the top is the root, and the nodes "
            "with no children at the bottom are the leaves. What makes it a search tree "
            "rather than just a binary tree is the rule about where things go: anything "
            "smaller than a node is placed in its left subtree and anything larger in its "
            "right subtree. Searching is then a matter of comparing and moving. To find "
            "37, start at the root, 50. 37 is smaller, so go left to 30. 37 is larger than "
            "30, so go right, and there it is. Three comparisons for seven items, because "
            "each comparison throws away half of what is left, in the same way a binary "
            "search does on a sorted list. That is why a balanced tree of a million items "
            "needs about twenty comparisons rather than a million.")
    return figure_scene("binary-tree-3d", world="", steps=steps,
                        title="A binary search tree", desc=desc,
                        height=380, depth=20, labels=L, scale=0.82,
                        caption="Every comparison halves what is left. A tree is binary "
                                "search, built into the shape of the data.")


@scene("database-tables-3d")
def _db_tables():
    """Two tables as two sheets, with the foreign key joining them."""
    L = ["One table for students. Each row is a student, each column a field.",
         "A primary key: one field whose value is different in every row.",
         "A second table for courses, with its own primary key.",
         "A foreign key in one table holds the primary key of the other.",
         "That link is why the data is stored once and not repeated."]

    def rows(z, tone, key, data):
        """A sheet with real rows on it, because a table without rows is a box."""
        out = []
        for i, (k, rest) in enumerate(data):
            y = -46 + i * 46
            out.append(box3d(-130, y, z + 6, 96, 26, k, "", tone))
            out.append(box3d(40, y, z + 6, 180, 26, rest, "", "floor"))
        out.append(billboard(-130, -72, z + 20, key, tone))
        return "".join(out)

    students = (plane(0, "STUDENTS", "", "teal", width=400, height=190)
                + rows(0, "teal", "StudentID (primary key)",
                       [("S01", "Aisha Khan · Y10"),
                        ("S02", "Tom Reilly · Y11"),
                        ("S03", "Mia Okafor · Y10")]))
    courses = (plane(230, "COURSES", "", "lilac", width=400, height=190)
               + rows(230, "lilac", "CourseID (primary key)",
                      [("C01", "Computing · Mr Ali"),
                       ("C02", "Physics · Ms Dale"),
                       ("C03", "Art · Mr Boyd")]))
    steps = [
        stage(1, students + billboard(0, 150, 40, "one row per student, one column per field"), L[0]),
        stage(2, students + billboard(0, 150, 40, "unique, never reused, never a name", "teal"), L[1]),
        stage(3, students + courses + billboard(0, 150, 40, "two tables, two primary keys", "lilac"), L[2]),
        stage(4, students + courses
              + billboard(0, 20, 118, "ENROLMENTS  \u2022  S01 + C01  \u2022  S01 + C03", "teal")
              + billboard(0, 150, 40, "in that table both fields are foreign keys", "teal"), L[3]),
        stage(5, students + courses
              + billboard(0, 150, 40, "change a teacher once, not on 300 rows", "lilac"), L[4]),
    ]
    desc = ("A relational database drawn as separate sheets. One table holds students, "
            "with a row for each student and a column for each field: StudentID, Name and "
            "Year. One field is chosen as the primary key, here StudentID, and its value "
            "must be different in every row and must never be reused, which is why a name "
            "makes a poor key and an ID number makes a good one. A second table holds "
            "courses, with CourseID as its own primary key. The two are joined by a third "
            "table of enrolments holding pairs of StudentID and CourseID, and in that "
            "table each of those fields is a foreign key, meaning a field that holds the "
            "primary key of another table. Splitting the data this way is normalisation, "
            "and the reason for it is that every fact is then stored exactly once: when a "
            "course changes teacher you change one row in the courses table rather than "
            "three hundred rows in one enormous table, and there is no way for two of "
            "those rows to end up disagreeing.")
    return figure_scene("database-tables-3d", world="", steps=steps,
                        title="Tables, keys and the link between them", desc=desc,
                        height=420, depth=230, labels=L, scale=0.74,
                        caption="Store every fact once. Almost every database exam answer "
                                "comes back to that sentence.")


@scene("abstraction-layers-3d")
def _abstraction():
    """What sits on what, from the metal up to the thing you clicked."""
    L = ["The hardware at the bottom: the parts you could drop on your foot.",
         "The operating system sits on it and manages all of it for you.",
         "Utility software does the housekeeping jobs around the system.",
         "Your applications sit on top and never touch the hardware directly.",
         "That is why a program written once runs on very different machines."]
    TIERS = [
        (0, "HARDWARE", "CPU · memory · disks · screen", "floor"),
        (95, "OPERATING SYSTEM", "memory, files, processes, devices, users", "teal"),
        (190, "UTILITY SOFTWARE", "backup · defrag · compression · antivirus", "lilac"),
        (285, "APPLICATIONS", "browser · word processor · game", "teal"),
    ]
    world = "".join(plane(z, t, s, tone, width=400, height=120) for z, t, s, tone in TIERS)
    steps = []
    for i, (z, t, s_, tone) in enumerate(TIERS):
        steps.append(stage(i + 1,
                           '<div class="sc-glow sc-glow-at sc-%s" style="--sc-x:0px;--sc-y:0px;'
                           '--sc-z:%dpx;--sc-w:400px;--sc-hh:120px"></div>' % (tone, z + 2),
                           L[i]))
    steps.append(stage(5, billboard(0, 170, 150,
                                    "each layer only talks to the one below it", "teal"), L[4]))
    desc = ("The layers of a computer system, from the metal upwards. At the bottom is the "
            "hardware: the processor, the memory, the disks, the screen. On top of it sits "
            "the operating system, which manages all of that on everyone's behalf, "
            "handling memory allocation, the file system, processes and scheduling, device "
            "drivers and user accounts. Beside it sits utility software, the housekeeping "
            "programs that keep the system in order: backup, defragmentation, compression "
            "and antivirus. On top sit the applications, the browser, the word processor, "
            "the game, which is what the person actually wanted to use. The rule that "
            "makes this worth drawing is that each layer talks only to the layer below it. "
            "An application never addresses the disk directly; it asks the operating "
            "system, which asks the driver, which talks to the hardware. That is exactly "
            "why the same program can run on two machines with completely different "
            "hardware inside them.")
    return figure_scene("abstraction-layers-3d", world=world, steps=steps,
                        title="Hardware, operating system, utilities, applications", desc=desc,
                        height=400, depth=285, labels=L, scale=0.82,
                        caption="An application that wants a file asks the operating "
                                "system. It has no idea whether the file is on a hard disk "
                                "or an SSD, and it does not need to.")


@scene("virtual-memory-3d")
def _virtual_memory():
    """Pages moving between RAM and the disk, which is the whole mechanism."""
    L = ["RAM holds the programs that are running. It is fast, and it is small.",
         "Open one program too many and there is no room left.",
         "A page that has not been used lately is written out to the disk.",
         "That frees real memory, so the new program can start.",
         "Needed again, the page is fetched back, which is why it goes slow."]

    def ram(pages, tone_of=None):
        out = [plane(230, "RAM", "fast · small · volatile", "teal", width=330, height=120)]
        for i in range(4):
            v = pages[i] if i < len(pages) else None
            out.append(box3d(-120 + i * 80, 26, 248, 66, 58, v or "", "",
                             (tone_of(i) if tone_of else ("lilac" if v else "floor"))))
        return "".join(out)

    def disk(pages):
        out = [plane(0, "DISK", "slow · huge · permanent", "lilac", width=430, height=150)]
        for i, v in enumerate(pages):
            out.append(box3d(-150 + i * 80, 32, 18, 66, 58, v, "", "floor"))
        return "".join(out)

    s1 = ram(["A1", "A2", "B1", "B2"]) + disk([])
    s2 = (ram(["A1", "A2", "B1", "B2"]) + disk([])
          + billboard(0, 205, 120, "program C needs a page, and RAM is full", "lilac"))
    s3 = (ram(["A1", "A2", "B1", "B2"], tone_of=lambda i: "teal" if i == 0 else "lilac")
          + disk(["A1"]) + billboard(0, 205, 120, "A1 is least recently used: page it out", "teal"))
    s4 = (ram(["C1", "A2", "B1", "B2"], tone_of=lambda i: "teal" if i == 0 else "lilac")
          + disk(["A1"]) + billboard(0, 205, 120, "C1 takes its place in real memory", "teal"))
    s5 = (ram(["A1", "A2", "B1", "B2"], tone_of=lambda i: "teal" if i == 0 else "lilac")
          + disk(["C1"]) + billboard(0, 205, 120, "swapping back and forth is thrashing", "lilac"))
    steps = [stage(1, s1, L[0]), stage(2, s2, L[1]), stage(3, s3, L[2]),
             stage(4, s4, L[3]), stage(5, s5, L[4])]
    desc = ("Virtual memory, drawn as pages moving between two levels. RAM holds the parts "
            "of the running programs that are needed now: it is fast, volatile and small. "
            "The disk below is slow, permanent and enormous. When another program is "
            "started and there is no space left in RAM, the operating system picks a page "
            "that has not been used recently and writes it out to a reserved area of the "
            "disk, which is the swap space or page file. That frees a frame of real memory "
            "for the new page, so the program can start even though the machine has run "
            "out of actual RAM. The cost arrives when the page that was written out is "
            "needed again, because fetching it back from disk is thousands of times slower "
            "than reading RAM. If memory is badly oversubscribed the machine spends most "
            "of its time moving pages in and out rather than doing any work, which is "
            "called thrashing and is what a computer that has gone treacly is usually "
            "doing. Adding more RAM fixes it; a faster processor does not.")
    return figure_scene("virtual-memory-3d", world="", steps=steps,
                        title="Virtual memory: paging to disk", desc=desc,
                        height=420, depth=260, labels=L, scale=0.78,
                        caption="Virtual memory does not make a machine faster. It lets it "
                                "run more than will fit, and pays for that in disk time.")


# ================================================== 3D modelling and graphics

@scene("mesh-3d")
def _mesh_3d():
    """Vertex, edge, face, mesh, built as an actual cube you can turn."""
    L = ["A vertex is one point in space, with an x, a y and a z. A cube has 8.",
         "An edge is a straight line joining two vertices. A cube needs 12.",
         "A face is a flat surface enclosed by edges. A cube has 6.",
         "All of them together are the mesh, and that is the model.",
         "More polygons means more detail, and more work for the computer."]

    s1 = cube3d(190, cz=110, verts=True) + billboard(0, 190, 20, "8 vertices")
    s2 = cube3d(190, cz=110, verts=True, edges=True) + billboard(0, 190, 20, "12 edges")
    s3 = (cube3d(190, cz=110, edges=True, faces=True)
          + billboard(0, 190, 20, "6 faces, each one flat"))
    s4 = (cube3d(190, cz=110, verts=True, edges=True, faces=True)
          + billboard(0, 190, 20, "vertices + edges + faces = the mesh", "teal"))
    s5 = (cube3d(120, cx=-150, cz=90, edges=True, faces=True)
          + cube3d(120, cx=150, cz=90, edges=True, faces=True, tone="lilac")
          + "".join(cube3d(40, cx=150 - 40 + (i % 3) * 40, cy=-40 + (i // 3) * 40,
                           cz=50 + 40 * ((i % 2)), edges=True, tone="lilac")
                    for i in range(6))
          + billboard(-150, 110, 20, "low poly: fast")
          + billboard(150, 110, 20, "high poly: heavy", "lilac"))
    steps = [stage(i + 1, b, L[i]) for i, b in enumerate([s1, s2, s3, s4, s5])]
    desc = ("A cube, built from the parts a 3D model is actually made of. A vertex is a "
            "single point in three dimensional space, given by an x coordinate across, a "
            "y for depth and a z for height, and a cube has eight of them, one at each "
            "corner. An edge is a straight line joining two vertices, and a cube needs "
            "twelve. A face is a flat surface enclosed by edges, usually a triangle or a "
            "square, and a cube has six. Those three things together, every vertex, every "
            "edge and every face, are the mesh, and the mesh is the model. The number of "
            "faces is the polygon count, and it is the central trade off in all 3D work: "
            "more polygons give finer detail and smoother curves, and also demand more "
            "processing power and more memory. A film can afford millions per character "
            "because each frame is rendered once over hours, while a game has to draw "
            "sixty frames every second and uses far simpler meshes with clever texturing "
            "to fake the detail that is missing.")
    return figure_scene("mesh-3d", world="", steps=steps,
                        title="Vertices, edges, faces and the mesh", desc=desc,
                        height=400, depth=210, labels=L, scale=0.9,
                        hint="Drag it. This one is a real cube, so turning it shows you "
                             "the faces you could not see before.",
                        caption="Learn vertex, edge, face, mesh in that order and the "
                                "rest of the unit has somewhere to attach.")


@scene("graphics-layers-3d")
def _graphics_layers():
    """Why designers work in layers: each part stays editable on its own."""
    L = ["The background sits at the bottom of the stack.",
         "The photograph goes on a layer of its own, above it.",
         "The logo goes above that, so it is never painted into the photo.",
         "The text sits on top, and can be restyled without touching anything else.",
         "Flatten it and they merge into one image, and that is no longer editable."]
    LAYERS = [(0, "BACKGROUND", "the base colour or texture", "floor"),
              (80, "PHOTOGRAPH", "placed, masked, not painted in", "teal"),
              (160, "LOGO", "vector, so it scales cleanly", "lilac"),
              (240, "TEXT", "still editable text, not pixels", "teal")]
    world = "".join(plane(z, t, s, tone, width=340, height=130)
                    for z, t, s, tone in LAYERS)
    steps = []
    for i, (z, t, s_, tone) in enumerate(LAYERS):
        steps.append(stage(i + 1,
                           '<div class="sc-glow sc-glow-at sc-%s" style="--sc-x:0px;'
                           '--sc-y:0px;--sc-z:%dpx;--sc-w:340px;--sc-hh:130px"></div>'
                           % (tone, z + 2), L[i]))
    steps.append(stage(5, billboard(0, 160, 40,
                                    "keep the layered master file, export the flat one",
                                    "lilac"), L[4]))
    desc = ("Why graphics software works in layers. Each part of the design sits on its "
            "own layer, stacked above the others: the background colour or texture at the "
            "bottom, then the photograph, then the logo, then the text on top. Nothing is "
            "painted into anything else, so any one layer can be moved, recoloured, "
            "hidden or deleted without disturbing the rest. The logo stays a vector, so "
            "it scales to any size cleanly, and the text stays real text, so the wording "
            "and the typeface can still be changed. Flattening merges every layer into a "
            "single image, which is what an exported JPEG or PNG is, and at that point "
            "none of it can be separated again. That is why the working practice is "
            "always to keep the layered master file and export a flat copy for use.")
    return figure_scene("graphics-layers-3d", world=world, steps=steps,
                        title="Working in layers", desc=desc,
                        height=380, depth=240, labels=L, scale=0.88,
                        caption="A flattened file is a finished file. The master stays "
                                "layered, because the client always wants one change.")


# ==================================================== compression and security

@scene("compression-3d")
def _compression():
    """The same data, three heights: original, lossless, lossy."""
    L = ["The original file: every byte of the data, nothing thrown away.",
         "Lossless finds repetition and records it more briefly.",
         "Unpack it and you get back exactly what you started with.",
         "Lossy throws data away permanently, and gets much smaller.",
         "Text and code must be lossless. Photos and music can be lossy."]

    def bar(x, h, label, sub, tone):
        return box3d(x, 0, h, 120, 120, label, sub, tone, tall=h)

    base = board(520, 220)
    s1 = base + bar(-160, 180, "ORIGINAL", "100%", "floor") + billboard(0, 205, 30, "say 10 MB")
    s2 = (base + bar(-160, 180, "ORIGINAL", "100%", "floor")
          + bar(20, 110, "LOSSLESS", "about 60%", "teal")
          + billboard(0, 205, 30, "RLE, Huffman: patterns written once", "teal"))
    s3 = (base + bar(-160, 180, "ORIGINAL", "100%", "floor")
          + bar(20, 110, "LOSSLESS", "about 60%", "teal")
          + billboard(0, 205, 30, "every bit recoverable, exactly", "teal"))
    s4 = (base + bar(-160, 180, "ORIGINAL", "100%", "floor")
          + bar(20, 110, "LOSSLESS", "about 60%", "teal")
          + bar(190, 40, "LOSSY", "about 10%", "lilac")
          + billboard(0, 205, 30, "the discarded detail is gone for good", "lilac"))
    s5 = (base + bar(-160, 180, "ORIGINAL", "100%", "floor")
          + bar(20, 110, "LOSSLESS", "text, code, spreadsheets", "teal")
          + bar(190, 40, "LOSSY", "photos, music, video", "lilac")
          + billboard(0, 205, 30, "one missing letter ruins a program", "teal"))
    steps = [stage(i + 1, b, L[i]) for i, b in enumerate([s1, s2, s3, s4, s5])]
    desc = ("Compression, with the height of each block standing for the size of the "
            "file. The original holds every byte of the data. Lossless compression finds "
            "repetition and records it more briefly: run length encoding replaces a run "
            "of identical values with the value and a count, and Huffman coding gives the "
            "most common symbols the shortest codes. Nothing is discarded, so unpacking "
            "returns exactly the original file, bit for bit, and the saving is modest, "
            "often around forty per cent. Lossy compression instead permanently throws "
            "away detail the eye or the ear is unlikely to notice, such as colours in a "
            "photograph or frequencies in a recording. It achieves far smaller files, "
            "often a tenth of the original, and what it removed cannot be recovered. "
            "Which to use follows from that: text, program code, spreadsheets and "
            "databases must be lossless, because a single changed character breaks them, "
            "while photographs, music and video are normally lossy, because nobody can "
            "tell and the saving is enormous.")
    return figure_scene("compression-3d", world="", steps=steps,
                        title="Lossless and lossy compression", desc=desc,
                        height=370, depth=190, labels=L, scale=0.86,
                        caption="Ask what happens if one byte changes. If the answer is "
                                "that it breaks, the compression has to be lossless.")


@scene("encryption-3d")
def _encryption():
    """Plaintext in, ciphertext across, plaintext out."""
    L = ["You start with plaintext: the message as anyone could read it.",
         "A key and an algorithm turn it into ciphertext.",
         "The ciphertext is what travels, and it is what an attacker sees.",
         "The right key reverses it. The wrong key gives nothing useful.",
         "Hashing is different: it is one way, and there is no way back."]

    base = board(600, 200)
    sender = box3d(-220, 0, 20, 130, 90, "PLAINTEXT", "MEET AT SIX", "teal")
    attacker = box3d(0, 130, 20, 150, 70, "ATTACKER", "sees only this", "lilac")
    receiver = box3d(220, 0, 20, 130, 90, "PLAINTEXT", "MEET AT SIX", "teal")
    cipher = box3d(0, -60, 70, 160, 80, "CIPHERTEXT", "Xq7#tLp2@v", "lilac")

    s1 = base + sender + billboard(0, 150, 30, "readable by anyone who intercepts it")
    s2 = (base + sender + cipher
          + box3d(-110, -60, 120, 90, 50, "KEY", "", "teal")
          + billboard(0, 150, 30, "same algorithm, different key, different output", "teal"))
    s3 = (base + sender + cipher + attacker
          + billboard(0, 215, 30, "without the key it is noise", "lilac"))
    s4 = (base + sender + cipher + receiver
          + box3d(110, -60, 120, 90, 50, "KEY", "", "teal")
          + billboard(0, 150, 30, "decryption is the same process in reverse", "teal"))
    s5 = (base + sender
          + box3d(60, -60, 70, 190, 80, "HASH", "a3f91c7e04", "lilac")
          + billboard(0, 150, 30, "stored instead of the password, and never reversed", "lilac"))
    steps = [stage(i + 1, b, L[i]) for i, b in enumerate([s1, s2, s3, s4, s5])]
    desc = ("Encryption, drawn as a journey. You begin with plaintext, the message as "
            "anybody could read it. An encryption algorithm combined with a key turns it "
            "into ciphertext, which looks like nonsense. The algorithm is usually public "
            "and well known; the secrecy lives entirely in the key, and the same algorithm "
            "with a different key produces completely different ciphertext. The ciphertext "
            "is what actually travels across the network, so an attacker who intercepts it "
            "sees only that, and without the key it is noise. At the far end the right key "
            "reverses the process and the original plaintext comes back. Hashing is a "
            "different thing that is often confused with it: a hash function turns an "
            "input into a fixed length value and is deliberately one way, with no key and "
            "no way back. That is why a sensible system stores the hash of a password "
            "rather than the password: it can check a login by hashing what was typed and "
            "comparing, while a stolen database gives the thief nothing to read.")
    return figure_scene("encryption-3d", world="", steps=steps,
                        title="Encryption, and why hashing is not the same", desc=desc,
                        height=370, depth=130, labels=L, scale=0.84,
                        caption="The algorithm is public. The key is the secret. That one "
                                "sentence answers most encryption questions.")


# =============================================================== units and speed

@scene("units-of-data-3d")
def _units():
    """Each unit sitting on the one below it, a thousand times bigger each time."""
    L = ["A bit is one binary digit: a single 0 or a single 1.",
         "Eight bits make a byte, which is enough for one character.",
         "A thousand bytes make a kilobyte. A page of plain text.",
         "A thousand kilobytes make a megabyte. A photograph, or a minute of music.",
         "A thousand megabytes make a gigabyte, and a thousand of those a terabyte."]
    TIERS = [(0, 110, "BIT", "one 0 or one 1", "teal"),
             (85, 170, "BYTE", "8 bits · one character", "lilac"),
             (170, 240, "KILOBYTE", "1,000 bytes · a page of text", "teal"),
             (255, 320, "MEGABYTE", "1,000 KB · a photo", "lilac"),
             (340, 400, "GIGABYTE", "1,000 MB · a film", "teal")]
    world = "".join(plane(z, t, s, tone, width=w, height=100)
                    for z, w, t, s, tone in TIERS)
    steps = []
    for i, (z, w, t, s_, tone) in enumerate(TIERS):
        steps.append(stage(i + 1,
                           '<div class="sc-glow sc-glow-at sc-%s" style="--sc-x:0px;'
                           '--sc-y:0px;--sc-z:%dpx;--sc-w:%dpx;--sc-hh:100px"></div>'
                           % (tone, z + 2, w), L[i]))
    desc = ("The units of data storage, each sitting on the one below it. A bit is a "
            "single binary digit, one 0 or one 1, and it is the smallest thing a computer "
            "can store. A nibble is four bits. Eight bits make a byte, which is enough to "
            "hold one character of text. A thousand bytes make a kilobyte, roughly a page "
            "of plain text. A thousand kilobytes make a megabyte, about the size of a "
            "photograph or a minute of music. A thousand megabytes make a gigabyte, enough "
            "for a film, and a thousand gigabytes make a terabyte, which is a typical hard "
            "disk. Each step is a thousand times the one before it, so the jumps are far "
            "larger than they look written down. Exam boards accept either a thousand or "
            "1,024 bytes to the kilobyte; OCR and AQA mark schemes use a thousand, and as "
            "long as you say which one you used you will not lose the mark.")
    return figure_scene("units-of-data-3d", world=world, steps=steps,
                        title="Bits, bytes and the units above them", desc=desc,
                        height=400, depth=340, labels=L, scale=0.8,
                        caption="Each step up is a thousand times the last. That is why a "
                                "film does not fit on a floppy disk and a text file "
                                "always will.")


@scene("cpu-performance-3d")
def _cpu_performance():
    """The three factors as three towers, so the trade offs are visible."""
    L = ["Clock speed: how many cycles the processor runs each second.",
         "Cores: how many instructions it can genuinely work on at once.",
         "Cache: fast memory on the chip, so it waits for RAM less often.",
         "A bigger number is not automatically a faster computer."]

    def towers(lit=None):
        def t(name):
            return "teal" if lit == name else "floor"
        return (board(480, 200)
                + box3d(-150, 0, 170, 120, 110, "CLOCK SPEED", "3.6 GHz", t("clock"), tall=170)
                + box3d(0, 0, 110, 120, 110, "CORES", "8 cores", t("cores"), tall=110)
                + box3d(150, 0, 140, 120, 110, "CACHE", "16 MB", t("cache"), tall=140))

    steps = [
        stage(1, towers("clock") + billboard(0, 165, 40,
                                             "3.6 GHz is 3,600,000,000 cycles a second"), L[0]),
        stage(2, towers("cores") + billboard(0, 165, 40,
                                             "only helps if the software is written to use them", "teal"), L[1]),
        stage(3, towers("cache") + billboard(0, 165, 40,
                                             "a cache miss costs hundreds of wasted cycles", "teal"), L[2]),
        stage(4, towers() + billboard(0, 165, 40,
                                      "four slow cores can lose to two fast ones", "lilac"), L[3]),
    ]
    desc = ("The three things that decide how fast a processor is. Clock speed is how many "
            "cycles it runs each second, measured in gigahertz, and 3.6 GHz means three "
            "thousand six hundred million cycles a second; each cycle can carry out part "
            "of an instruction, so more cycles means more work done, as long as nothing "
            "else is holding it up. The number of cores is how many instructions it can "
            "genuinely process at the same time, since each core is effectively a separate "
            "processor, but that only helps if the software has been written to split its "
            "work across them, which is why doubling the cores rarely doubles the speed. "
            "Cache is a small amount of very fast memory on the processor chip holding "
            "data it is likely to need next: a cache hit is answered in a few cycles while "
            "a miss means waiting hundreds of cycles for main memory, so more cache means "
            "less waiting. None of the three works alone, which is why four slow cores can "
            "be beaten by two fast ones, and why a bigger number on the box does not by "
            "itself mean a faster computer.")
    return figure_scene("cpu-performance-3d", world="", steps=steps,
                        title="Clock speed, cores and cache", desc=desc,
                        height=370, depth=180, labels=L, scale=0.88,
                        caption="Exam answers that just say ‘higher clock speed is "
                                "faster’ get one mark. Saying what it does, and what "
                                "limits it, gets the rest.")


# ==================================================== processors and networks

@scene("parallel-cores-3d")
def _parallel():
    """One core working through a queue, then four sharing it out."""
    L = ["One core takes the jobs one after another, in order.",
         "Four cores take four jobs at once, so the queue clears sooner.",
         "Only if the work can be split. Some jobs must wait for the one before.",
         "A GPU takes this much further: thousands of tiny cores, one kind of job."]

    def core(x, y, label, jobs, tone="teal"):
        out = [box3d(x, y, 24, 110, 70, label, "", tone)]
        for i, j in enumerate(jobs):
            out.append(box3d(x, y - 90 - i * 46, 20, 90, 38, j, "", "floor"))
        return "".join(out)

    s1 = (board(520, 330) + core(-120, 60, "CORE 1", ["job 1", "job 2", "job 3", "job 4"])
          + billboard(130, 60, 60, "4 jobs, one at a time", "teal"))
    s2 = (board(520, 330)
          + "".join(core(-180 + i * 120, 60, "CORE %d" % (i + 1), ["job %d" % (i + 1)])
                    for i in range(4))
          + billboard(0, 190, 40, "4 jobs, all at once", "teal"))
    s3 = (board(520, 330)
          + "".join(core(-180 + i * 120, 60, "CORE %d" % (i + 1),
                         ["job %d" % (i + 1)] if i < 2 else [])
                    for i in range(4))
          + billboard(0, 190, 40, "jobs 3 and 4 need the result of job 2", "lilac"))
    s4 = (board(520, 330)
          + "".join(box3d(-200 + (i % 10) * 45, -70 + (i // 10) * 45, 20, 36, 36, "", "",
                          "lilac")
                    for i in range(40))
          + billboard(0, 190, 40, "a GPU: thousands of simple cores, same job each", "lilac"))
    steps = [stage(i + 1, b, L[i]) for i, b in enumerate([s1, s2, s3, s4])]
    desc = ("Why more cores is not simply more speed. A single core takes jobs from the "
            "queue one after another, so four jobs take four times as long as one. Four "
            "cores can take one job each at the same moment, and the queue clears in "
            "roughly a quarter of the time. That only works if the work can genuinely be "
            "split: when job three needs the result of job two it has to wait however "
            "many cores are sitting idle, which is why doubling the cores rarely doubles "
            "real performance and why software has to be deliberately written to use "
            "them. A graphics processor takes the idea to its limit with thousands of very "
            "simple cores, each doing the same kind of small calculation on different "
            "data, which suits shading millions of pixels or training a neural network "
            "and is poor at general purpose work.")
    return figure_scene("parallel-cores-3d", world="", steps=steps,
                        title="One core, four cores, and a GPU", desc=desc,
                        height=390, depth=40, labels=L, scale=0.82,
                        caption="The exam answer is the condition, not the claim: more "
                                "cores help when the task can be divided.")


@scene("web-request-3d")
def _web_request():
    """What actually happens between typing an address and seeing a page."""
    L = ["You type an address. The browser needs the IP address behind the name.",
         "A DNS server looks up the name and returns the IP address.",
         "The browser sends an HTTP request to that address.",
         "The server sends back HTML, CSS, images and scripts.",
         "The browser renders them into the page you see."]

    base = (board(620, 300)
            + box3d(-230, 60, 20, 130, 80, "YOUR BROWSER", "", "teal")
            + box3d(0, -110, 20, 130, 70, "DNS SERVER", "the phone book", "lilac")
            + box3d(230, 60, 20, 130, 80, "WEB SERVER", "", "teal"))
    s1 = base + billboard(-230, 170, 40, "mskprod.org", "teal")
    s2 = (base + link3d(-230, 60, 0, -110, 16, "lilac")
          + dot3d(-115, -25, 26, "mskprod.org?", "lilac")
          + billboard(0, 170, 40, "names are for people, addresses are for routers", "lilac"))
    s3 = (base + link3d(0, -110, -230, 60, 16, "lilac")
          + dot3d(-115, -25, 26, "185.199.108.153", "lilac")
          + billboard(0, 170, 40, "now the browser knows where to go"))
    s4 = (base + link3d(-230, 60, 230, 60, 16, "teal")
          + dot3d(0, 60, 26, "GET /", "teal")
          + billboard(0, 170, 40, "an HTTP request for one page", "teal"))
    s5 = (base + link3d(230, 60, -230, 60, 16, "teal")
          + dot3d(0, 60, 26, "HTML + CSS + images", "teal")
          + billboard(0, 170, 40, "the browser builds the page from the files", "teal"))
    steps = [stage(i + 1, b, L[i]) for i, b in enumerate([s1, s2, s3, s4, s5])]
    desc = ("What happens between typing a web address and seeing the page. You type a "
            "domain name, which is written for people to remember, but routers only "
            "understand IP addresses, so the browser first has to translate it. It asks a "
            "DNS server, which works like a phone book for the internet, and the DNS "
            "server returns the IP address that the name belongs to. The browser then "
            "sends an HTTP request to that address asking for the page. The web server "
            "responds with the files that make it up: the HTML holding the structure, the "
            "CSS holding the styling, and the images and scripts. The browser puts those "
            "together and renders the finished page. If the address begins with HTTPS the "
            "whole exchange is encrypted first, so anybody intercepting it sees nothing "
            "useful.")
    return figure_scene("web-request-3d", world="", steps=steps,
                        title="From typing an address to seeing a page", desc=desc,
                        height=380, depth=30, labels=L, scale=0.84,
                        caption="DNS is a lookup, not a delivery. It tells the browser "
                                "where to go, and the browser goes there itself.")


@scene("array-2d-3d")
def _array_2d():
    """One row, then a grid, then a record. The indexes are the point."""
    L = ["A one dimensional array: values in a row, reached by one index.",
         "A two dimensional array: rows and columns, reached by two.",
         "grid[1][2] means row 1, then column 2. Row always comes first.",
         "A record holds fields of different types, reached by name."]

    def row(vals, lit=None, y=0, z=20):
        out = []
        for i, v in enumerate(vals):
            out.append(box3d(-160 + i * 80, y, z, 66, 52, str(v), "[%d]" % i,
                             "teal" if i == lit else "floor"))
        return "".join(out)

    def grid(lit=None):
        out = []
        data = [[4, 9, 2], [7, 1, 8], [3, 6, 5]]
        for r in range(3):
            for c in range(3):
                out.append(box3d(-110 + c * 110, -90 + r * 90, 20, 84, 64,
                                 str(data[r][c]), "[%d][%d]" % (r, c),
                                 "teal" if (r, c) == lit else "floor"))
        return "".join(out)

    s1 = board(480, 180) + row([4, 9, 2, 7, 1]) + billboard(0, 130, 40, "scores[3] is 7")
    s2 = board(480, 340) + grid() + billboard(0, 215, 40, "three rows, three columns")
    s3 = (board(480, 340) + grid(lit=(1, 2))
          + billboard(0, 215, 40, "grid[1][2] is 8, not 6", "teal"))
    s4 = (board(480, 200)
          + box3d(-170, 0, 24, 140, 80, "name", "\"Aisha\"", "teal")
          + box3d(0, 0, 24, 140, 80, "year", "10", "lilac")
          + box3d(170, 0, 24, 140, 80, "present", "True", "teal")
          + billboard(0, 150, 40, "one record, three fields, three types", "teal"))
    steps = [stage(i + 1, b, L[i]) for i, b in enumerate([s1, s2, s3, s4])]
    desc = ("Arrays and records. A one dimensional array is a row of values of the same "
            "type, reached by a single index, and the indexes start at zero, so in the "
            "row 4, 9, 2, 7, 1 the value at index 3 is 7. A two dimensional array is a "
            "grid of rows and columns, reached by two indexes, and the order is always "
            "row first and column second: in a three by three grid, grid index one index "
            "two means the second row and the third column. Getting those two the wrong "
            "way round is the single most common mistake in the topic, and on a grid that "
            "is not square it crashes rather than quietly giving the wrong answer. A "
            "record is different again: it holds several fields which may be of different "
            "types, a string for the name, an integer for the year, a Boolean for whether "
            "they are present, and the fields are reached by name rather than by position, "
            "which is what makes a record readable where an index is not.")
    return figure_scene("array-2d-3d", world="", steps=steps,
                        title="Arrays, two dimensional arrays and records", desc=desc,
                        height=380, depth=40, labels=L, scale=0.84,
                        caption="Row first, then column. Say it out loud every time you "
                                "write a 2D index and you will stop getting it backwards.")


@scene("lan-wan-3d")
def _lan_wan():
    """Two sites, each a LAN, joined into a WAN by infrastructure you rent."""
    L = ["A LAN covers one site: one building, one campus, cabling you own.",
         "A second site has its own LAN, with its own switch and its own cabling.",
         "Joining them makes a WAN, over lines nobody at either end owns.",
         "That is the real difference: not size, but who owns the connection."]

    def site(cx, label, tone):
        pts = [(cx - 80, -70), (cx + 80, -70), (cx - 80, 70), (cx + 80, 70)]
        out = [box3d(cx, 0, 26, 100, 54, "SWITCH", "", tone)]
        for i, (x, y) in enumerate(pts):
            out.append(box3d(x, y, 18, 70, 40, "PC", "", "floor"))
            out.append(link3d(cx, 0, x, y, 12, tone))
        out.append(billboard(cx, 150, 40, label, tone))
        return "".join(out)

    left = site(-200, "SITE A · LAN", "teal")
    right = site(200, "SITE B · LAN", "lilac")
    base = board(700, 330)
    s1 = base + left + billboard(0, -170, 60, "cabling and switches you own and maintain")
    s2 = base + left + right + billboard(0, -170, 60, "two separate local networks")
    s3 = (base + left + right
          + link3d(-200, 0, 200, 0, 50, "teal", "leased line · rented")
          + billboard(0, -170, 60, "a WAN: the link between them is somebody else's", "teal"))
    s4 = (base + left + right
          + link3d(-200, 0, 200, 0, 50, "teal", "the internet is the largest WAN")
          + billboard(0, -170, 60, "size is a symptom. Ownership is the definition.", "lilac"))
    steps = [stage(i + 1, b, L[i]) for i, b in enumerate([s1, s2, s3, s4])]
    desc = ("The difference between a local area network and a wide area network. A LAN "
            "covers a single geographical site, one building or one campus, and the "
            "organisation owns and maintains all of it: the switches, the cabling, the "
            "wireless access points. That is why a LAN is fast and cheap to run once it is "
            "installed. A second site has its own LAN, its own switch and its own cabling. "
            "Joining the two sites makes a wide area network, and the link between them "
            "runs over infrastructure that neither site owns, whether a leased line, a "
            "fibre connection from a telecoms provider or the internet itself. That is the "
            "real distinction and the one exam answers miss: not that a WAN is bigger, but "
            "that a WAN depends on connections somebody else owns, which is why it is "
            "slower, costs a rental, and brings security questions a LAN does not have. "
            "The internet is simply the largest WAN there is.")
    return figure_scene("lan-wan-3d", world="", steps=steps,
                        title="LAN, WAN and who owns the wire", desc=desc,
                        height=380, depth=60, labels=L, scale=0.76,
                        caption="‘A WAN is bigger’ gets you nothing. ‘A WAN "
                                "uses infrastructure the organisation does not own’ "
                                "is the mark.")


@scene("embedded-systems-3d")
def _embedded():
    """A general purpose machine beside a chip that does exactly one job."""
    L = ["A general purpose computer: many parts, and it runs whatever you install.",
         "An embedded system: one small board, built into the device it controls.",
         "It runs one program, written once, stored in ROM, never replaced.",
         "That is why it boots instantly, costs pennies and almost never crashes."]

    general = (box3d(-180, 0, 14, 300, 230, "", "", "floor")
               + box3d(-250, -60, 26, 110, 60, "CPU", "", "teal")
               + box3d(-110, -60, 26, 110, 60, "RAM", "", "lilac")
               + box3d(-250, 50, 26, 110, 60, "DISK", "", "floor")
               + box3d(-110, 50, 26, 110, 60, "GPU", "", "floor")
               + billboard(-180, 170, 40, "general purpose computer"))
    embedded = (box3d(190, 0, 14, 200, 150, "", "", "teal")
                + box3d(190, 0, 26, 120, 70, "ONE CHIP", "CPU + ROM + I/O", "teal")
                + billboard(190, 150, 40, "embedded system", "teal"))
    base = board(640, 320)
    s1 = base + general
    s2 = base + general + embedded
    s3 = (base + general + embedded
          + billboard(0, -190, 70, "washing machine · microwave · traffic light · pacemaker"))
    s4 = (base + general + embedded
          + billboard(0, -190, 70, "one job, so nothing else can slow it down or break it",
                      "teal"))
    steps = [stage(i + 1, b, L[i]) for i, b in enumerate([s1, s2, s3, s4])]
    desc = ("A general purpose computer against an embedded system. The general purpose "
            "machine has a processor, main memory, a graphics processor and secondary "
            "storage, runs a full operating system, and will run whatever software you "
            "choose to install on it, which is exactly what makes it flexible, expensive "
            "and complicated. An embedded system is a single small board built into the "
            "device it controls, often one chip carrying the processor, the memory and the "
            "input and output together. It runs one program, written for that device, "
            "stored in ROM and normally never changed for the life of the product. "
            "Washing machines, microwaves, traffic lights, car engine management and "
            "pacemakers are all embedded systems. Because it does one job it can be made "
            "tiny and cheap, it starts instantly with no operating system to load, it uses "
            "very little power, and there is very little in it to go wrong, which matters "
            "a great deal when the device is keeping somebody's heart beating.")
    return figure_scene("embedded-systems-3d", world="", steps=steps,
                        title="General purpose against embedded", desc=desc,
                        height=380, depth=40, labels=L, scale=0.8,
                        caption="Ask whether the user can install new software on it. If "
                                "not, it is almost certainly embedded.")
