"""Drawn pictures of the hardware the topics talk about.

Each one stands in for a photograph (see photos.py): until the photograph's file
exists, photos.render() draws one of these instead, credited as a drawing. They
are not diagrams. They try to look like the object, with the few parts worth
naming labelled in plain words, so that a student who has only ever seen the
outside of a computer can recognise the real thing when they meet it.
"""
import math

from .illus import REGISTRY, Canvas, PAL, INK, ARROW, figure, _n
from . import illus_props as P
from . import illus_glyphs as G

PICS = {}


def picture(slug, title, max_w=700):
    """Register a drawing as the stand in for the photograph called slug."""
    def wrap(fn):
        def render():
            from .photos import PHOTOS
            cv = Canvas(800, 500).backdrop()
            fn(cv)
            ph = PHOTOS[slug]
            return figure("pic-" + slug, cv, title, ph.alt, [], ph.caption, max_w=max_w, credit="Drawn illustration")
        REGISTRY["pic-" + slug] = render
        PICS[slug] = render
        return fn
    return wrap


def note(cv, px, py, tx, ty, text, anchor="start", sub=None):
    """A label with a thin leader to the part it names, and a dot on the part.

    The leader stops at the nearest edge of the label's box, so that it never crosses the words.
    (tx, ty) is the label's anchor point and ty its first baseline.
    """
    w = max(len(text) * 14.5 * .6, len(sub) * 12.5 * .56 if sub else 0)
    x0 = tx if anchor == "start" else tx - w if anchor == "end" else tx - w / 2
    x1 = x0 + w
    y0, y1 = ty - 15, ty + (23 if sub else 6)
    cxm, cym = (x0 + x1) / 2, (y0 + y1) / 2
    if abs(px - cxm) / (w / 2 + 1) > abs(py - cym) / ((y1 - y0) / 2 + 1):
        ex, ey = (x0 - 7 if px < cxm else x1 + 7), cym
    else:
        ex, ey = min(max(px, x0 + 8), x1 - 8), (y0 - 6 if py < cym else y1 + 6)
    out = cv.line(px, py, ex, ey, ARROW, 2, op=.9) + cv.circle(px, py, 4.6, "#FFFFFF", stroke="#0F7C84", sw=2.4)
    out += cv.text(tx, ty, text, 14.5, 800, anchor=anchor, cls="il-ink")
    if sub:
        out += cv.text(tx, ty + 18, sub, 12.5, 650, anchor=anchor, cls="il-ink2")
    return out


# ------------------------------------------------------------------ the processor

@picture("cpu-chip", "A processor, from above and from below")
def _cpu(cv):
    S = 230
    for (x0, y0, kind) in ((90, 150, "top"), (480, 150, "under")):
        cv.add(cv.shadow(x0 + S / 2, y0 + S + 14, S * .52, 8, .25))
        if kind == "top":
            cv.add(cv.rect(x0, y0, S, S, 22, cv.g("metal"), stroke="#8799A7", sw=2.4))
            cv.add(cv.rect(x0 + 20, y0 + 20, S - 40, S - 40, 14, cv.lin("lid", [(0, "#FFFFFF"), (1, "#C7D3DA")]), stroke="#A9B8C2", sw=1.6))
            for k, w in enumerate((110, 90, 70)):
                cv.add(cv.rect(x0 + 62, y0 + 84 + k * 24, w, 9, 4.5, "#AFC0CB"))
            cv.add(cv.rect(x0 + 62, y0 + 160, 50, 9, 4.5, "#AFC0CB"))
        else:
            cv.add(cv.rect(x0, y0, S, S, 20, cv.g("pcb", "deep"), stroke="#17754E", sw=2.4))
            n = 15
            step = (S - 36) / (n - 1)
            for i in range(n):
                for j in range(n):
                    if 4 <= i <= 10 and 4 <= j <= 10:
                        continue
                    cv.add(cv.circle(x0 + 18 + i * step, y0 + 18 + j * step, 4.4, cv.g("gold")))
            for (dx, dy, w, h) in ((84, 92, 12, 7), (134, 92, 12, 7), (84, 133, 12, 7), (134, 133, 12, 7), (108, 84, 14, 7), (108, 141, 14, 7)):
                cv.add(cv.rect(x0 + dx, y0 + dy, w, h, 2, "#2A3E49"))
        cv.add(cv.poly([(x0 + 8, y0 + S - 8), (x0 + 8, y0 + S - 34), (x0 + 34, y0 + S - 8)], "#FFCC4A", stroke="#B98A12", sw=1.4))
    cv.add(P.pill(cv, 205, 118, "top", "paper", 15, 16, 28, 800), P.pill(cv, 595, 118, "underneath", "paper", 15, 16, 28, 800))
    cv.add(cv.text(205, 446, "the metal lid is a heat spreader", 14.5, 800, cls="il-ink"), cv.text(205, 466, "the silicon is a few millimetres wide, beneath it", 12.5, 650, cls="il-ink2"))
    cv.add(cv.text(595, 446, "hundreds of gold contact pads", 14.5, 800, cls="il-ink"), cv.text(595, 466, "they press onto the socket's pins", 12.5, 650, cls="il-ink2"))
    cv.add(note(cv, 108, 372, 96, 410, "pin 1 marker", "start"))


# ------------------------------------------------------------------ the motherboard

@picture("motherboard", "A motherboard with its main parts labelled")
def _board(cv):
    bx, by, bw, bh = 230, 30, 380, 440
    cv.add(cv.shadow(bx + bw / 2, by + bh + 12, 200, 9, .25))
    cv.add(cv.rect(bx, by, bw, bh, 14, cv.g("pcb", "deep"), stroke="#17754E", sw=3))
    for k in range(7):
        cv.add(cv.path("M%s %s L%s %s L%s %s" % (bx + 30, by + 60 + k * 54, bx + 70, by + 60 + k * 54, bx + 90, by + 40 + k * 54), stroke="#8FE3BC", sw=1.6, op=.35))
    # the processor socket
    cv.add(cv.rect(bx + 70, by + 70, 120, 120, 6, "#2A3E49"), cv.rect(bx + 82, by + 82, 96, 96, 4, cv.g("metal")), cv.rect(bx + 94, by + 94, 72, 72, 3, "#DCE6EC"), cv.rect(bx + 56, by + 150, 8, 56, 3, "#8799A7"))
    # memory slots
    for k in range(4):
        cv.add(cv.rect(bx + 220 + k * 22, by + 50, 14, 190, 3, "#1C2831"), cv.rect(bx + 218 + k * 22, by + 48, 18, 8, 2, "#8799A7"))
    # the chipset heatsink
    cv.add(cv.rect(bx + 190, by + 290, 80, 80, 6, cv.g("metal", "deep")))
    for k in range(6):
        cv.add(cv.line(bx + 198, by + 298 + k * 12, bx + 262, by + 298 + k * 12, "#8799A7", 2))
    # expansion slots
    cv.add(cv.rect(bx + 30, by + 390, 300, 14, 3, "#1C2831"), cv.rect(bx + 30, by + 350, 150, 12, 3, "#1C2831"), cv.rect(bx + 30, by + 318, 130, 12, 3, "#2A3E49"))
    # power connectors, battery and ports
    cv.add(cv.rect(bx + 348, by + 70, 22, 110, 3, "#F1F5F8", stroke="#9FB3BE", sw=1.4), cv.rect(bx + 80, by + 28, 70, 14, 3, "#F1F5F8", stroke="#9FB3BE", sw=1.4))
    cv.add(cv.circle(bx + 300, by + 330, 22, cv.g("metal")), cv.circle(bx + 300, by + 330, 15, "none", stroke="#8799A7", sw=1.6))
    cv.add(cv.rect(bx - 56, by + 230, 70, 150, 6, cv.g("metal")), cv.rect(bx - 44, by + 242, 26, 18, 2, "#2F82C0"), cv.rect(bx - 44, by + 270, 26, 18, 2, "#2F82C0"), cv.rect(bx - 44, by + 302, 36, 30, 3, "#2A3E49"), cv.rect(bx - 44, by + 342, 26, 14, 2, "#E6574D"))
    for k in range(4):
        cv.add(cv.rect(bx + 340, by + 220 + k * 18, 22, 11, 2, "#1C2831"))
    # the labels, away from the board
    cv.add(note(cv, bx + 130, by + 130, 40, 120, "processor socket", "start", "the chip plugs in here"))
    cv.add(note(cv, bx + 275, by + 120, 650, 120, "memory slots", "start", "one stick per slot"))
    cv.add(note(cv, bx + 230, by + 330, 650, 300, "chipset heatsink", "start", "links the parts together"))
    cv.add(note(cv, bx + 130, by + 397, 24, 448, "expansion slots", "start", "graphics and network cards"))
    cv.add(note(cv, bx + 359, by + 125, 650, 200, "power connector", "start", "feeds every part"))
    cv.add(note(cv, bx - 18, by + 290, 24, 252, "ports", "start", "USB, network, audio"))
    cv.add(note(cv, bx + 300, by + 330, 650, 390, "battery", "start", "keeps the clock running"))


# ------------------------------------------------------------------ memory

def dimm(cv, x, y, w, h, notch):
    out = cv.shadow(x + w / 2, y + h + 12, w * .46, 6, .22)
    out += cv.rect(x, y, w, h, 6, cv.g("pcb", "deep"), stroke="#17754E", sw=2)
    cw = (w - 70) / 8
    for i in range(8):
        out += cv.rect(x + 28 + i * cw, y + 14, cw - 8, h - 46, 4, "#1A242B") + cv.rect(x + 31 + i * cw, y + 17, cw - 14, 6, 2, "#FFFFFF", op=.16)
    for i in range(int((w - 16) / 8)):
        px = x + 8 + i * 8
        if abs(px - (x + w * notch)) < 6:
            continue
        out += cv.rect(px, y + h - 15, 5, 15, 1, cv.g("gold"))
    out += cv.rect(x + w * notch - 5, y + h - 16, 10, 16, 0, "var(--il-bg1)")
    return out + cv.circle(x + 10, y + h / 2 - 8, 3.4, "#E9F7EF", op=.8) + cv.circle(x + w - 10, y + h / 2 - 8, 3.4, "#E9F7EF", op=.8)


@picture("ram-stick", "Two memory sticks with the notch in a different place")
def _ram(cv):
    cv.add(dimm(cv, 120, 90, 560, 110, .4), dimm(cv, 120, 280, 560, 110, .58))
    cv.add(cv.text(100, 150, "DDR4", 16, 800, anchor="end", cls="il-ink", mono=True), cv.text(100, 340, "DDR5", 16, 800, anchor="end", cls="il-ink", mono=True))
    cv.add(note(cv, 120 + 560 * .4, 193, 120 + 560 * .4, 236, "notch", "middle"))
    cv.add(note(cv, 120 + 560 * .58, 383, 120 + 560 * .58, 426, "notch, somewhere else", "middle", "so it will not fit the wrong slot"))
    cv.add(note(cv, 260, 130, 260, 70, "memory chips", "middle"))
    cv.add(note(cv, 540, 196, 640, 236, "gold contacts", "start"))


# ------------------------------------------------------------------ the firmware chip

@picture("rom-chip", "A flash memory chip soldered to a board")
def _rom(cv):
    cv.add(cv.rect(210, 90, 420, 330, 20, cv.g("pcb", "deep"), stroke="#17754E", sw=3))
    for k in range(5):
        cv.add(cv.path("M%s %s L%s %s L%s %s" % (240, 140 + k * 56, 290, 140 + k * 56, 316, 160 + k * 56 if k < 3 else 140 + k * 56), stroke="#8FE3BC", sw=2.4, op=.5))
    cx, cy = 400, 255
    for k in range(4):
        yy = cy - 46 + k * 28
        cv.add(cv.rect(cx - 98, yy, 34, 12, 2, cv.g("metal", "deep")), cv.rect(cx + 64, yy, 34, 12, 2, cv.g("metal", "deep")))
        cv.add(cv.path("M%s %s L%s %s" % (cx - 98, yy + 6, cx - 150 - k * 6, yy + 6), stroke="#8FE3BC", sw=3, op=.8), cv.path("M%s %s L%s %s" % (cx + 98, yy + 6, cx + 150 + k * 6, yy + 6), stroke="#8FE3BC", sw=3, op=.8))
    cv.add(cv.rect(cx - 70, cy - 62, 140, 124, 8, cv.g("dark", "deep"), stroke="#0E171C", sw=2))
    cv.add(cv.circle(cx - 50, cy + 42, 6, "#0E171C"))
    cv.add(cv.text(cx, cy - 20, "FLASH", 17, 800, fill="#E6EEF2", mono=True), cv.text(cx, cy + 6, "64M", 17, 800, fill="#E6EEF2", mono=True), cv.text(cx, cy + 32, "firmware", 12.5, 700, fill="#AFC0CB", mono=True))
    cv.add(note(cv, cx - 50, cy + 42, 24, 380, "pin 1 dot", "start", "marks the first leg"))
    cv.add(note(cv, cx - 82, cy - 32, 24, 150, "legs", "start", "soldered to the board"))
    cv.add(note(cv, cx + 50, cy - 40, 650, 150, "flash memory chip", "start", "keeps its contents"))


# ------------------------------------------------------------------ storage

@picture("hdd-open", "A hard disk drive with the lid removed")
def _hdd(cv):
    x0, y0, w = 200, 96, 400
    cv.add(P.hdd(cv, x0, y0, w))
    h = w * .76
    cx, cy, r = x0 + w * .42, y0 + h * .5, h * .4
    cv.add(note(cv, cx - r * .6, cy - r * .5, 24, 52, "platter", "start", "a mirror disc that stores the data"))
    cv.add(note(cv, cx + r * .06, cy + r * .28, 776, 52, "read-write head", "end", "floats above the platter"))
    cv.add(note(cv, cx, cy, 24, 452, "spindle motor", "start", "spins the platter at 7,200 rpm"))
    cv.add(note(cv, x0 + w * .87, y0 + h * .84, 776, 452, "actuator arm", "end", "swings the head across"))


@picture("ssd-open", "A solid state drive with its case open")
def _ssd(cv):
    cv.add(P.ssd(cv, 140, 120, 520, label=False))
    w = 520
    h = w * .52
    cv.add(note(cv, 140 + 54 + 20, 120 + 12 + 14, 140 + 80, 70, "flash memory chips", "middle", "this is where the data is"))
    cv.add(note(cv, 140 + w - 24, 120 + h * .38 + 12, 140 + w + 80, 90, "controller", "end", "manages the chips"))
    cv.add(note(cv, 140 + 30, 120 + h - 6, 140 + 30, 120 + h + 70, "connector", "start", "plugs into the computer"))
    cv.add(cv.text(680, 440, "no moving parts", 16, 800, anchor="middle", cls="il-ink"))


@picture("usb-and-disc", "A USB flash drive and an optical disc")
def _usb(cv):
    cv.add(cv.shadow(210, 330, 140, 8, .22))
    cv.add(cv.rect(70, 232, 90, 70, 6, cv.g("metal", "deep")), cv.rect(84, 248, 14, 12, 2, "#2A3E49"), cv.rect(84, 274, 14, 12, 2, "#2A3E49"), cv.rect(110, 242, 40, 50, 4, "none", stroke="#8799A7", sw=1.4))
    cv.add(cv.rect(160, 218, 190, 98, 20, cv.g("coral", "deep")), cv.rect(172, 228, 166, 22, 10, "#FFFFFF", op=.22), cv.circle(325, 267, 10, "var(--il-bg1)"))
    cv.add(P.disc(cv, 580, 260, 130))
    cv.add(note(cv, 114, 245, 60, 170, "USB connector", "start"))
    cv.add(note(cv, 255, 316, 255, 390, "USB flash drive", "middle", "flash memory, no moving parts"))
    cv.add(note(cv, 640, 330, 640, 450, "optical disc", "middle", "read by a laser"))


# ------------------------------------------------------------------ graphics card and cooling

def fan(cv, cx, cy, r, blades=9):
    out = cv.circle(cx, cy, r + 8, "#0E171C") + cv.circle(cx, cy, r, "#1C2831")
    for k in range(blades):
        a = k * 360 / blades
        ra, rb = math.radians(a), math.radians(a + 34)
        out += cv.path("M%s %s Q%s %s %s %s Q%s %s %s %s Z" % (_n(cx + 12 * math.cos(ra)), _n(cy + 12 * math.sin(ra)), _n(cx + r * .75 * math.cos(ra - .25)), _n(cy + r * .75 * math.sin(ra - .25)), _n(cx + r * .94 * math.cos(rb)), _n(cy + r * .94 * math.sin(rb)),
                                                      _n(cx + r * .5 * math.cos(rb + .3)), _n(cy + r * .5 * math.sin(rb + .3)), _n(cx + 12 * math.cos(ra)), _n(cy + 12 * math.sin(ra))), fill="#5B6D79", stroke="#36464F", sw=1)
    return out + cv.circle(cx, cy, 22, cv.g("dark", "deep")) + cv.circle(cx, cy, 8, "#8799A7")


@picture("gpu-card", "A graphics card with two fans")
def _gpu(cv):
    cv.add(cv.shadow(400, 400, 300, 10, .25))
    cv.add(cv.rect(110, 150, 600, 190, 20, cv.g("dark", "deep"), stroke="#0E171C", sw=2))
    cv.add(cv.rect(120, 160, 580, 10, 5, "#FFFFFF", op=.12))
    cv.add(fan(cv, 270, 245, 72), fan(cv, 520, 245, 72))
    cv.add(cv.rect(120, 340, 560, 22, 4, cv.g("pcb", "deep")), cv.rect(150, 346, 300, 16, 0, cv.g("gold")))
    for i in range(30):
        cv.add(cv.rect(152 + i * 10, 346, 6, 16, 1, cv.g("gold")))
    cv.add(cv.rect(60, 130, 40, 240, 6, cv.g("metal", "deep")), cv.rect(66, 160, 28, 16, 3, "#2A3E49"), cv.rect(66, 190, 28, 16, 3, "#2A3E49"), cv.rect(66, 220, 28, 16, 3, "#2A3E49"))
    cv.add(cv.rect(520, 134, 120, 16, 4, "#0E171C"), cv.rect(530, 138, 100, 8, 2, "#36464F"))
    cv.add(note(cv, 270, 245, 150, 80, "cooling fans", "middle", "most of the card is cooling"))
    cv.add(note(cv, 80, 175, 60, 430, "display ports", "start"))
    cv.add(note(cv, 300, 355, 300, 430, "connector to the motherboard", "middle"))
    cv.add(note(cv, 590, 142, 700, 90, "extra power", "end"))
    cv.add(note(cv, 640, 300, 700, 430, "heatsink under the shroud", "end"))


@picture("heatsink-fan", "A processor cooler: fan, fins and heat pipes")
def _cooler(cv):
    cv.add(cv.shadow(210, 410, 160, 8, .22))
    cv.add(cv.rect(80, 150, 260, 260, 18, cv.g("dark", "deep"), stroke="#0E171C", sw=2))
    cv.add(fan(cv, 210, 280, 105, 7))
    for (x, y) in ((92, 162), (328, 162), (92, 398), (328, 398)):
        cv.add(cv.circle(x, y, 6, "#8799A7"))
    # the same cooler from the side
    cv.add(cv.rect(440, 120, 280, 24, 6, cv.g("dark", "deep")))
    for k in range(18):
        cv.add(cv.rect(446 + k * 15, 150, 7, 190, 2, cv.g("metal", "side")))
    for k in range(3):
        cv.add(cv.path("M%s 340 L%s 380" % (470 + k * 100, 470 + k * 100), stroke="#C97A3A", sw=11), cv.path("M%s 340 L%s 380" % (470 + k * 100, 470 + k * 100), stroke="#F1B374", sw=4, op=.7))
    cv.add(cv.rect(440, 380, 280, 22, 5, cv.g("coral", "deep")))
    cv.add(cv.rect(560, 410, 40, 6, 2, "#5B6D79"))
    cv.add(note(cv, 210, 200, 210, 90, "fan", "middle", "pushes air through the fins"))
    cv.add(note(cv, 600, 240, 700, 90, "metal fins", "end", "spread the heat into the air"))
    cv.add(note(cv, 570, 360, 470, 450, "heat pipes", "end", "carry heat up from the base"))
    cv.add(note(cv, 700, 392, 776, 450, "base plate", "end", "sits on the processor"))


# ------------------------------------------------------------------ small computers and network hardware

@picture("embedded-board", "A single board computer, about the size of a bank card")
def _embedded(cv):
    x, y, w, h = 120, 110, 560, 330
    cv.add(cv.shadow(400, y + h + 16, 250, 9, .25))
    cv.add(cv.rect(x, y, w, h, 16, cv.g("pcb", "deep"), stroke="#17754E", sw=3))
    for (hx, hy) in ((x + 16, y + 16), (x + w - 16, y + 16), (x + 16, y + h - 16), (x + w - 16, y + h - 16)):
        cv.add(cv.circle(hx, hy, 8, "var(--il-bg1)"), cv.circle(hx, hy, 8, "none", stroke="#D9A441", sw=3))
    cv.add(cv.rect(x + 200, y + 100, 110, 110, 8, cv.g("metal", "deep"), stroke="#8799A7", sw=1.6), cv.text(x + 255, y + 162, "CPU", 17, 800, fill=INK))
    cv.add(cv.rect(x + 330, y + 110, 90, 70, 6, "#1C2831"), cv.text(x + 375, y + 150, "RAM", 14, 800, fill="#C9D8E0", mono=True))
    cv.add(cv.rect(x + 56, y + 24, 140, 70, 4, cv.g("metal", "deep")), cv.rect(x + 66, y + 34, 56, 50, 2, "#0F1A20"), cv.rect(x + 128, y + 34, 56, 50, 2, "#0F1A20"))
    cv.add(cv.rect(x + 440, y + 40, 100, 90, 4, cv.g("metal", "deep")), cv.rect(x + 450, y + 52, 38, 28, 2, "#2F82C0"), cv.rect(x + 494, y + 52, 38, 28, 2, "#2F82C0"), cv.rect(x + 450, y + 88, 82, 32, 2, "#0F1A20"))
    for k in range(20):
        cv.add(cv.rect(x + 40 + k * 12, y + 276, 7, 20, 2, "#1C2831"), cv.rect(x + 40 + k * 12, y + 300, 7, 20, 2, "#1C2831"))
    cv.add(cv.rect(x + 40, y + 260, 244, 70, 4, "none", stroke="#2A3E49", sw=1.6, op=.5))
    cv.add(cv.rect(x + 330, y + 250, 120, 70, 4, cv.g("sun", "deep")), cv.text(x + 390, y + 292, "microSD slot", 11.5, 800, fill=INK))
    cv.add(cv.circle(x + 500, y + 290, 14, cv.g("slate", "deep")))
    cv.add(note(cv, x + 100, y + 60, 24, 56, "display connector", "start"))
    cv.add(note(cv, x + 255, y + 100, 330, 56, "processor", "middle", "runs the program"))
    cv.add(note(cv, x + 375, y + 112, 500, 56, "memory", "middle"))
    cv.add(note(cv, x + 490, y + 130, 776, 56, "USB and network ports", "end"))
    cv.add(note(cv, x + 140, y + 280, 24, 472, "input and output pins", "start", "connect sensors and lights"))
    cv.add(note(cv, x + 390, y + 300, 520, 472, "storage card", "start", "no hard disk"))


def rj45(cv, cx, cy, s=1.0):
    out = cv.rect(cx - 70 * s, cy - 56 * s, 140 * s, 112 * s, 10 * s, "#E3F1F6", stroke="#9FB3BE", sw=2, op=.95)
    cols = ["#FFFFFF", "#E8913C", "#FFFFFF", "#2F82C0", "#FFFFFF", "#41B56D", "#FFFFFF", "#8A5A2B"]
    for k in range(8):
        px = cx - 56 * s + k * 16 * s
        out += cv.rect(px - 4.4 * s, cy - 40 * s, 8.8 * s, 84 * s, 4 * s, cols[k], stroke="#8799A7", sw=.8)
    for k in range(8):
        out += cv.rect(cx - 62 * s + k * 16 * s, cy + 44 * s, 9 * s, 12 * s, 1.5, cv.g("gold"))
    out += cv.rect(cx - 26 * s, cy - 76 * s, 52 * s, 22 * s, 4 * s, "#E3F1F6", stroke="#9FB3BE", sw=2)
    return out


@picture("ethernet-cable", "An Ethernet cable and its RJ45 plug")
def _eth(cv):
    cv.add(cv.shadow(400, 400, 260, 8, .22))
    cv.add(cv.path("M20 330 Q200 310 330 300", stroke="#1F6FAE", sw=26), cv.path("M20 330 Q200 310 330 300", stroke="#66B8EC", sw=18), cv.path("M20 322 Q200 302 330 292", stroke="#FFFFFF", sw=4, op=.5))
    cv.add(cv.rect(318, 270, 70, 60, 8, cv.g("slate", "deep")))
    cv.add(rj45(cv, 520, 290, 1.5))
    # twisted pairs
    cols = [("#E8913C", "#FFFFFF"), ("#2F82C0", "#FFFFFF"), ("#41B56D", "#FFFFFF"), ("#8A5A2B", "#FFFFFF")]
    for k, (a_, b_) in enumerate(cols):
        y = 108 + k * 24
        cv.add(cv.path("M90 %s q16 -9 32 0 t32 0 t32 0 t32 0 t32 0 t32 0" % y, stroke=a_, sw=6), cv.path("M90 %s q16 9 32 0 t32 0 t32 0 t32 0 t32 0 t32 0" % y, stroke=b_, sw=6, op=.95))
    cv.add(cv.text(185, 82, "four twisted pairs", 14.5, 800, cls="il-ink"), cv.text(185, 224, "each pair twists around its partner", 12.5, 650, cls="il-ink2"))
    cv.add(note(cv, 520, 236, 520, 150, "RJ45 plug", "middle", "clear plastic: eight wires inside"))
    cv.add(note(cv, 80, 322, 80, 410, "cable jacket", "middle"))
    cv.add(note(cv, 520, 336, 520, 440, "gold contacts", "middle", "touch the pins in the socket"))


@picture("fibre-optic", "Fibre optic cable with the jacket cut back")
def _fibre(cv):
    cv.add(cv.shadow(400, 420, 280, 8, .22))
    cv.add(cv.path("M30 300 L330 300", stroke="#C7A31A", sw=70), cv.path("M30 300 L330 300", stroke="#F2CF3E", sw=60), cv.path("M30 282 L330 282", stroke="#FFFFFF", sw=5, op=.4))
    cv.add(cv.rect(300, 262, 44, 76, 6, cv.g("sun", "deep")))
    cv.add(cv.path("M344 300 L480 300", stroke="#9FB3BE", sw=40), cv.path("M344 300 L480 300", stroke="#E6EEF2", sw=32))
    for k, dy in enumerate((-10, -3, 4, 11)):
        cv.add(cv.path("M344 %s L700 %s" % (300 + dy, 270 + dy * 3 + (k - 2) * 10), stroke="#CFE9F4", sw=3.6, op=.9))
    for k, dy in enumerate((-10, -3, 4, 11)):
        yy = 270 + dy * 3 + (k - 2) * 10
        cv.add(glow(cv, 700, yy, 20, "#FFFFFF" if k % 2 else "#9CD3F0", .95), cv.circle(700, yy, 4, "#FFFFFF"))
    cv.add(note(cv, 160, 262, 120, 150, "outer jacket", "middle", "protects the glass inside"))
    cv.add(note(cv, 412, 288, 440, 190, "strengthening layer", "middle"))
    cv.add(note(cv, 600, 272, 640, 150, "glass strands", "middle", "as thin as a hair"))
    cv.add(note(cv, 700, 270, 700, 380, "light pulses", "middle", "the data travels as light"))


def glow(cv, cx, cy, r, color, o=.8):
    return cv.circle(cx, cy, r, cv.rad("g%s" % color.lstrip("#"), [(0, color, o), (1, color, 0)]))


@picture("network-switch", "A rack mounted network switch")
def _switch(cv):
    cv.add(cv.shadow(400, 330, 330, 10, .25))
    cv.add(cv.rect(40, 170, 720, 130, 10, cv.g("dark", "deep"), stroke="#0E171C", sw=2))
    cv.add(cv.rect(40, 170, 720, 10, 8, "#FFFFFF", op=.14))
    for r in range(2):
        for c in range(12):
            x, y = 118 + c * 52, 196 + r * 52
            cv.add(cv.rect(x, y, 40, 34, 3, "#0E171C"), cv.rect(x + 5, y + 5, 30, 18, 2, "#1F2C34"), cv.rect(x + 8, y + 26, 10, 4, 1, "#5BE08A" if (c + r) % 3 else "#FFC84A"), cv.rect(x + 22, y + 26, 10, 4, 1, "#5BE08A"))
    cv.add(cv.rect(54, 200, 46, 80, 6, "#1C2831"), cv.text(77, 222, "PWR", 11, 800, fill="#B8F7CE", mono=True), cv.circle(77, 244, 5, "#5BE08A"), cv.text(77, 268, "SYS", 10.5, 800, fill="#C9D8E0", mono=True))
    for (x, y) in ((52, 180), (748, 180), (52, 290), (748, 290)):
        cv.add(cv.circle(x, y, 5, "#8799A7"))
    cv.add(cv.rect(700, 202, 50, 70, 6, "#1C2831"), cv.text(725, 240, "24", 18, 800, fill="#C9D8E0", mono=True))
    cv.add(note(cv, 170, 213, 120, 100, "Ethernet ports", "middle", "one cable, one device"))
    cv.add(note(cv, 188, 243, 330, 100, "port lights", "middle", "green means linked"))
    cv.add(note(cv, 93, 236, 60, 380, "power and status", "start"))
    cv.add(note(cv, 748, 188, 740, 120, "mounting holes", "end", "it bolts into a rack"))
    cv.add(cv.text(400, 400, "in a star network, every device has its own port", 14.5, 800, cls="il-ink"))


@picture("home-router", "A home broadband router")
def _router(cv):
    cv.add(cv.shadow(400, 400, 260, 10, .25))
    for x in (220, 560):
        cv.add(cv.rect(x - 6, 70, 12, 200, 6, cv.g("dark", "deep")), cv.circle(x, 70, 11, "#2A3E49"), cv.rect(x - 14, 262, 28, 22, 5, "#2A3E49"))
    cv.add(cv.rect(120, 270, 560, 130, 22, cv.g("coral", "deep"), stroke="#C84B43", sw=2))
    cv.add(cv.rect(120, 270, 560, 40, 22, "#FFFFFF", op=.18))
    for i, c in enumerate(("#5BE08A", "#5BE08A", "#FFD24A", "#FFFFFF", "#5BE08A")):
        cv.add(cv.circle(172 + i * 36, 346, 8, c, stroke="#0E171C", sw=1.4))
    for k in range(4):
        cv.add(cv.rect(430 + k * 46, 326, 38, 34, 4, "#0F1A20"), cv.rect(436 + k * 46, 332, 26, 16, 2, "#FFD24A"))
    cv.add(cv.rect(618, 326, 38, 34, 4, "#0F1A20"), cv.rect(624, 332, 26, 16, 2, "#66B8EC"))
    cv.add(note(cv, 220, 80, 400, 40, "aerials", "middle", "send and receive wireless signals"))
    cv.add(note(cv, 208, 346, 24, 452, "status lights", "start", "power, internet, wireless"))
    cv.add(note(cv, 510, 360, 520, 452, "Ethernet ports", "middle", "plug in wired devices"))
    cv.add(note(cv, 637, 360, 776, 452, "internet port", "end", "to the broadband line"))


@picture("nic-card", "A network interface card")
def _nic(cv):
    cv.add(cv.shadow(400, 400, 260, 8, .22))
    cv.add(cv.rect(110, 150, 560, 210, 8, cv.g("pcb", "deep"), stroke="#17754E", sw=2.4))
    cv.add(cv.rect(60, 120, 40, 270, 5, cv.g("metal", "deep")), cv.rect(66, 190, 28, 22, 3, "#1C2831"), cv.rect(66, 226, 28, 22, 3, "#1C2831"))
    cv.add(cv.rect(56, 160, 48, 100, 6, "none"))
    cv.add(cv.rect(104, 175, 90, 100, 6, cv.g("metal", "deep"), stroke="#8799A7", sw=1.6), cv.rect(112, 190, 74, 70, 3, "#1C2831"))
    cv.add(cv.rect(250, 200, 100, 60, 5, "#1C2831"), cv.text(300, 236, "CONTROLLER", 11.5, 800, fill="#C9D8E0", mono=True))
    for k in range(5):
        cv.add(cv.rect(390 + k * 22, 200, 14, 22, 2, "#2A3E49"))
    cv.add(cv.rect(250, 290, 190, 10, 2, "#F1F5F8"), cv.text(345, 299, "3C:22:FB:9A:41:7E", 10, 800, fill="#2A3E49", mono=True))
    for k in range(34):
        cv.add(cv.rect(250 + k * 12, 346, 7, 14, 1, cv.g("gold")))
    cv.add(note(cv, 80, 202, 24, 90, "Ethernet socket", "start", "the cable plugs in here"))
    cv.add(note(cv, 300, 220, 300, 100, "controller chip", "middle", "turns data into signals"))
    cv.add(note(cv, 345, 295, 250, 410, "MAC address", "middle", "burned in at the factory"))
    cv.add(note(cv, 560, 353, 640, 410, "gold edge connector", "middle", "plugs into the motherboard"))


@picture("server-rack", "A rack of servers in a data centre")
def _server(cv):
    ox = 90
    cv.add(cv.shadow(400 + ox, 450, 260, 10, .25))
    cv.add(cv.rect(180 + ox, 30, 440, 420, 10, cv.g("dark", "deep"), stroke="#0E171C", sw=2.4))
    cv.add(cv.rect(194 + ox, 44, 412, 392, 6, "#0F1A20", op=.7))
    for r in range(8):
        y = 54 + r * 48
        cv.add(cv.rect(204 + ox, y, 392, 40, 5, cv.g("dark")), cv.rect(204 + ox, y, 392, 40, 5, "none", stroke="#0E171C", sw=1.2))
        for k in range(8):
            cv.add(cv.rect(214 + ox + k * 24, y + 9, 14, 22, 2, "#0F1A20", op=.75))
        cv.add(cv.circle(520 + ox, y + 14, 3.6, "#5BE08A" if r % 3 else "#FFC84A"), cv.circle(534 + ox, y + 14, 3.6, "#5C6F7B"), cv.rect(504 + ox, y + 26, 70, 4, 2, "#6F8794"))
    cv.add(cv.path("M%s 90 C%s 100 %s 200 %s 240 C%s 280 %s 360 %s 420" % (620 + ox, 700 + ox, 690 + ox, 640 + ox, 600 + ox, 680 + ox, 628 + ox), stroke="#2F82C0", sw=7))
    cv.add(cv.path("M%s 100 C%s 110 %s 210 %s 250 C%s 290 %s 370 %s 430" % (620 + ox, 690 + ox, 680 + ox, 630 + ox, 590 + ox, 670 + ox, 620 + ox), stroke="#F0584B", sw=7))
    cv.add(note(cv, 330 + ox, 74, 24, 110, "one server", "start", "a flat computer"))
    cv.add(note(cv, 520 + ox, 68, 400 + ox, 20, "status lights", "middle"))
    cv.add(note(cv, 300 + ox, 300, 24, 330, "the rack", "start", "many servers, one cabinet"))
    cv.add(note(cv, 668 + ox, 330, 776, 482, "cables carry network and power", "end"))


@picture("peripherals", "A desk with a keyboard, mouse, microphone and printer")
def _periph(cv):
    cv.add(cv.rect(30, 380, 740, 30, 8, cv.g("wood", "deep")), cv.rect(60, 410, 20, 70, 3, PAL["wood"][2]), cv.rect(720, 410, 20, 70, 3, PAL["wood"][2]))
    cv.add(cv.shadow(400, 382, 330, 8, .2))
    # keyboard
    cv.add(cv.rect(250, 330, 280, 50, 8, cv.g("metal", "deep")))
    for r in range(3):
        for c in range(14):
            cv.add(cv.rect(258 + c * 19.4, 336 + r * 12, 16, 9, 2, "#FFFFFF", stroke="#B9C6CE", sw=.8))
    cv.add(cv.rect(300, 372, 160, 5, 2, "#FFFFFF", stroke="#B9C6CE", sw=.8))
    # mouse
    cv.add(cv.path("M580 380 Q570 340 600 332 Q630 326 640 350 Q648 376 640 380 Z", fill=cv.g("slate", "deep"), stroke="#8799A7", sw=1.6), cv.line(612, 332, 612, 352, "#8799A7", 1.6))
    # microphone
    cv.add(cv.rect(114, 300, 36, 6, 3, "#5B6D79"), cv.rect(129, 250, 6, 56, 2, "#5B6D79"), cv.rect(116, 196, 32, 58, 16, cv.g("metal", "round"), stroke="#8799A7", sw=1.6))
    for k in range(4):
        cv.add(cv.line(122, 208 + k * 10, 142, 208 + k * 10, "#8799A7", 1.6))
    cv.add(cv.rect(100, 372, 64, 8, 4, "#5B6D79"))
    # printer
    cv.add(cv.rect(650, 190, 100, 38, 4, "#FFFFFF", stroke="#9FB3BE", sw=1.4))
    cv.add(P.lift(cv, 630, 220, 140, 70, "slate", 12, 6, hl=False), cv.rect(646, 236, 90, 8, 3, "#0F1A20", op=.5), cv.circle(750, 240, 4, "#5BE08A"))
    cv.add(cv.rect(660, 296, 80, 40, 3, "#FFFFFF", stroke="#9FB3BE", sw=1.4), cv.rect(668, 306, 56, 4, 2, "#C5D1D9"))
    # a monitor, so the system makes sense
    cv.add(cv.rect(300, 120, 200, 130, 10, cv.g("dark", "deep")), cv.rect(308, 128, 184, 114, 5, "#EAF6F8"), cv.rect(390, 250, 20, 62, 3, cv.g("metal", "side")), cv.rect(350, 304, 100, 12, 6, cv.g("metal", "deep")))
    cv.add(cv.rect(318, 140, 90, 12, 4, cv.g("teal")), cv.rect(318, 162, 160, 8, 3, "#C5D1D9"), cv.rect(318, 178, 130, 8, 3, "#C5D1D9"))
    cv.add(note(cv, 400, 126, 400, 62, "monitor: output", "middle", "shows the result"))
    cv.add(note(cv, 132, 210, 60, 160, "microphone: input", "start"))
    cv.add(note(cv, 330, 355, 230, 440, "keyboard: input", "start"))
    cv.add(note(cv, 612, 356, 560, 440, "mouse: input", "start"))
    cv.add(note(cv, 700, 262, 776, 170, "printer: output", "end"))
