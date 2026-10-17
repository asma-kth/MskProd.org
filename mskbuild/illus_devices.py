"""Illustrations of how input and output devices work: the optical mouse, the barcode scanner,
the capacitive touchscreen, the laser printer, LCD against OLED, and the 3D printer."""
import math

from .illus import Canvas, PAL, INK, ARROW, figure, illustration, _n
from . import illus_props as P
from . import illus_glyphs as G

CARD_X = (14, 277, 540)
TOP = 34


def glow(cv, cx, cy, r, color, o=.8):
    return cv.circle(cx, cy, r, cv.rad("glow%s" % color.lstrip("#"), [(0, color, o), (1, color, 0)]))


def three_cards(cv, titles, steps):
    """Three tall cards side by side, each with a drawing area on top and three numbered steps below."""
    for i, ((title, col), st) in enumerate(zip(titles, steps)):
        x = CARD_X[i]
        cv.add(P.card(cv, x, TOP, 246, 456, 20, title, col))
        cv.add(cv.line(x + 16, TOP + 290, x + 230, TOP + 290, "var(--il-line)", 1.5))
        for k, lines in enumerate(st):
            y = TOP + 316 + k * 52
            cv.add(cv.circle(x + 28, y + 2, 12, cv.g("deep", "deep")), cv.text(x + 28, y + 7.5, str(k + 1), 14, 800, fill="#FFFFFF"))
            for j, ln in enumerate(lines):
                cv.add(cv.text(x + 50, y + j * 17, ln, 13, 650, anchor="start", cls="il-ink"))


# ------------------------------------------------------------------ input devices

def cursor(cv, x, y, s=1.0):
    pts = [(0, 0), (0, 21), (5.5, 16), (9.5, 25), (13, 23.5), (9, 15), (16, 15)]
    return cv.poly([(x + px * s, y + py * s) for px, py in pts], "#FFFFFF", stroke=INK, sw=1.8)


@illustration("input-devices-how")
def _inputs():
    cv = Canvas(800, 500).backdrop()
    three_cards(cv, (("Optical mouse", "sky"), ("Barcode scanner", "coral"), ("Touchscreen", "mint")),
                ((("An LED lights the", "desk surface"), ("A tiny camera takes", "1000s of photos a second"), ("Comparing the photos shows", "which way it moved")),
                 (("A laser sweeps across", "the bars"), ("White reflects light,", "black absorbs it"), ("The sensor turns the light", "pattern into 1s and 0s")),
                 (("A grid of wires under the", "glass holds a small charge"), ("A finger conducts, so the", "charge changes at that spot"), ("The controller finds the", "row and column that changed"))))
    # ---- the optical mouse, cut open
    x0, ly = CARD_X[0], TOP
    cv.add(cv.rect(x0 + 14, ly + 246, 218, 24, 8, cv.g("wood")), cv.rect(x0 + 18, ly + 247, 210, 5, 2.5, "#FFFFFF", op=.35))
    body = ("M%s %s L%s %s Q%s %s %s %s L%s %s Q%s %s %s %s L%s %s Z"
            % (x0 + 50, ly + 218, x0 + 50, ly + 196, x0 + 54, ly + 158, x0 + 100, ly + 156, x0 + 148, ly + 156, x0 + 192, ly + 158, x0 + 196, ly + 196, x0 + 196, ly + 218))
    cv.add(cv.shadow(x0 + 123, ly + 224, 80, 5, .2))
    cv.add(cv.path(body, fill=cv.g("slate"), stroke=PAL["slate"][2], sw=2.4))
    cv.add(cv.path("M%s %s L%s %s" % (x0 + 123, ly + 157, x0 + 123, ly + 178), stroke=PAL["slate"][2], sw=2))
    cv.add(cv.rect(x0 + 80, ly + 196, 86, 22, 4, "#DDE6EC"))
    cv.add(cv.poly([(x0 + 91, ly + 210), (x0 + 101, ly + 210), (x0 + 137, ly + 246), (x0 + 117, ly + 246)], "#F0584B", op=.38))
    cv.add(cv.line(x0 + 127, ly + 246, x0 + 156, ly + 214, "#F0584B", 2.6, op=.85))
    cv.add(cv.ellipse(x0 + 127, ly + 247, 15, 3.4, "#F0584B", op=.55))
    cv.add(glow(cv, x0 + 96, ly + 207, 14, "#F0584B", .7), cv.circle(x0 + 96, ly + 207, 5, "#F0584B"))
    cv.add(cv.rect(x0 + 147, ly + 203, 20, 11, 2.5, "#36464F"), cv.circle(x0 + 157, ly + 208.5, 3, "#9FD3F0"))
    cv.add(cv.text(x0 + 96, ly + 192, "LED", 12, 750, fill=INK), cv.text(x0 + 157, ly + 192, "sensor", 12, 750, fill=INK))
    # two photos of the desk, and what they say
    dots = [(9, 11), (24, 27), (15, 38), (31, 15), (27, 36), (38, 24)]
    for k, (fx, shift) in enumerate(((x0 + 16, 0), (x0 + 88, 6))):
        cv.add(cv.rect(fx, ly + 52, 52, 52, 6, "#FFFFFF", stroke="#9FB3BE", sw=1.6))
        for (dx, dy) in dots:
            cv.add(cv.circle(fx + 4 + dx + shift, ly + 56 + dy, 3.2, "#8B5A2B"))
        cv.add(cv.text(fx + 26, ly + 122, "photo %d" % (k + 1), 12, 650, cls="il-ink2"))
    cv.add(P.arrow(cv, [(x0 + 72, ly + 78), (x0 + 84, ly + 78)], ARROW, 3, 8))
    cv.add(P.arrow(cv, [(x0 + 146, ly + 78), (x0 + 168, ly + 78)], ARROW, 3, 8))
    cv.add(cursor(cv, x0 + 180, ly + 62, 1.0), cv.path("M%s %s L%s %s" % (x0 + 214, ly + 96, x0 + 196, ly + 80), stroke=ARROW, sw=2, dash="3 5"))
    cv.add(cv.text(x0 + 192, ly + 122, "pointer moves", 12, 650, cls="il-ink2"))
    # ---- the barcode scanner
    x1 = CARD_X[1]
    cv.add(cv.poly([(x1 + 123, ly + 78), (x1 + 34, ly + 150), (x1 + 212, ly + 150)], "#F0584B", op=.2))
    cv.add(P.lift(cv, x1 + 66, ly + 42, 114, 36, "dark", 10, 5, hl=False), cv.rect(x1 + 96, ly + 68, 54, 7, 3, "#F0584B"))
    cv.add(cv.text(x1 + 123, ly + 64, "scanner", 12, 750, fill="#FFFFFF"))
    widths = [6, 4, 4, 8, 4, 4, 4, 8, 4, 6, 4, 4, 8, 4, 6, 4, 4, 6, 4, 8, 4]
    k = 172.0 / sum(widths)
    bx, bt, bh = x1 + 37, ly + 124, 56
    cv.add(cv.rect(bx - 8, bt - 6, 172 + 16, bh + 12, 8, "#FFFFFF", stroke="#B9C6CE", sw=1.4))
    pos, edges = bx, []
    for i, w_ in enumerate(widths):
        black = i % 2 == 0
        if black:
            cv.add(cv.rect(pos, bt, w_ * k, bh, 0, INK))
        edges.append((pos, pos + w_ * k, black))
        pos += w_ * k
    cv.add(cv.line(bx - 12, ly + 152, bx + 184, ly + 152, "#F0584B", 3.2), cv.circle(bx - 12, ly + 152, 4, "#F0584B"), cv.circle(bx + 184, ly + 152, 4, "#F0584B"))
    hi, lo = ly + 212, ly + 240
    d = "M%s %s" % (_n(bx), _n(lo if edges[0][2] else hi))
    for (a_, b_, black) in edges:
        yy = lo if black else hi
        d += " L%s %s L%s %s" % (_n(a_), _n(yy), _n(b_), _n(yy))
        if (a_, b_, black) != edges[-1]:
            nxt = edges[edges.index((a_, b_, black)) + 1]
            d += " L%s %s" % (_n(b_), _n(lo if nxt[2] else hi))
    cv.add(cv.path(d, stroke=PAL["teal"][2], sw=2.8, cap="butt"))
    cv.add(cv.text(x1 + 123, ly + 268, "reflected light, high then low", 12, 650, cls="il-ink2"))
    # ---- the capacitive touchscreen
    x2 = CARD_X[2]
    gx, gy, cs = x2 + 34, ly + 118, 30
    cv.add(cv.rect(gx - 8, gy - 8, 6 * cs + 16, 4 * cs + 16, 12, "#CFEAF6", op=.85, stroke="#9FB3BE", sw=1.6))
    cv.add(cv.rect(gx - 4, gy - 4, 6 * cs + 8, 7, 3, "#FFFFFF", op=.5))
    for i in range(7):
        cv.add(cv.line(gx + i * cs, gy, gx + i * cs, gy + 4 * cs, "#6F8794", 1.4, op=.7))
    for j in range(5):
        cv.add(cv.line(gx, gy + j * cs, gx + 6 * cs, gy + j * cs, "#6F8794", 1.4, op=.7))
    hc, hr = 3, 1
    for i in range(6):
        cv.add(cv.rect(gx + i * cs + 3, gy - 20, cs - 6, 8, 3, cv.g("teal") if i == hc else "#B9C6CE"))
    for j in range(4):
        cv.add(cv.rect(gx - 22, gy + j * cs + 3, 8, cs - 6, 3, cv.g("teal") if j == hr else "#B9C6CE"))
    tx, ty = gx + hc * cs + cs / 2, gy + hr * cs + cs / 2
    cv.add(cv.rect(gx + hc * cs, gy, cs, 4 * cs, 0, "#25B3BB", op=.14), cv.rect(gx, gy + hr * cs, 6 * cs, cs, 0, "#25B3BB", op=.14))
    cv.add(cv.circle(tx, ty, 11, "#FF8A3D", op=.45), cv.circle(tx, ty, 19, "none", stroke="#FF8A3D", sw=2.4, op=.75), cv.circle(tx, ty, 27, "none", stroke="#FF8A3D", sw=2, op=.4))
    fade = cv.lin("ffade", [(0, "#000000"), (.45, "#FFFFFF"), (1, "#FFFFFF")], 0, 0, 0, 1)
    fmask = cv._def("fmask", '<mask id="{id}"><rect x="-24" y="-120" width="48" height="126" fill="%s"/></mask>' % fade)
    finger = "M-15 -120 L-15 -14 Q-15 2 0 2 Q15 2 15 -14 L15 -120 Z"
    fb = cv.path(finger, fill=cv.lin("skin", [(0, "#F9D7B5"), (1, "#E9B58B")], 0, 0, 1, 0), stroke="#C99A74", sw=2, extra=' mask="%s"' % fmask)
    fb += cv.path("M-8 -78 L-8 -20", stroke="#FFFFFF", sw=3, op=.45) + cv.path("M-7 -12 Q0 -6 7 -12", stroke="#D9A57C", sw=1.6, op=.8)
    cv.add(cv.group(fb, tx, ty, 1, 22))
    cv.add(cv.text(x2 + 123, ly + 268, "column 4, row 2", 12, 650, cls="il-ink2"))
    return figure(
        "input-devices-how", cv, "How an optical mouse, a barcode scanner and a capacitive touchscreen work",
        "Three input devices, each drawn working. An optical mouse is cut open to show an LED that lights the desk and a tiny camera, the "
        "sensor, that photographs it thousands of times a second. Two photos of the same desk are shown with the pattern slightly shifted, "
        "and comparing them tells the processor which way the mouse moved, so the pointer moves. A barcode scanner shines a laser line "
        "sweeping across the black and white bars. White bars reflect the light and black bars absorb it, so the sensor sees a pattern of high "
        "and low light, drawn as a square wave under the barcode, which becomes a pattern of 1s and 0s. A capacitive touchscreen has a grid of "
        "wires under the glass holding a small electric charge. A finger conducts, so the charge changes where it touches, and the "
        "controller finds the row and the column that changed, here column 4 and row 2, which gives the position of the touch.",
        ["Optical mouse: an LED lights the surface, a tiny camera takes thousands of photos a second, and comparing them shows the movement.",
         "Barcode scanner: a laser sweeps across the bars, white reflects and black absorbs, and the sensor turns the pattern of light into 1s and 0s.",
         "Capacitive touchscreen: a finger changes the charge in the grid of wires, and the controller finds the row and column that changed."],
        "An input device turns something real, such as movement, light or touch, into a signal the computer can process.")


# ------------------------------------------------------------------ output devices

@illustration("output-devices-how")
def _outputs():
    cv = Canvas(800, 500).backdrop()
    three_cards(cv, (("Laser printer", "teal"), ("LCD against OLED", "plum"), ("3D printer", "sun")),
                ((("A laser draws the page as", "a charge on the drum"), ("Toner sticks to the", "charged parts of the drum"), ("Paper picks up the toner,", "a hot fuser melts it in")),
                 (("LCD: a backlight shines", "through liquid crystals"), ("OLED: each pixel makes", "its own light"), ("OLED black is simply off,", "so contrast is higher")),
                 (("Plastic filament is fed", "to a heated nozzle"), ("The nozzle moves, laying", "down one thin layer"), ("Layer on layer builds", "the whole object"))))
    ly = TOP
    # ---- the laser printer, in section
    x0 = CARD_X[0]
    dcx, dcy, dr = x0 + 84, ly + 130, 34
    cv.add(cv.circle(dcx, dcy, dr + 3, "#10303A", op=.18), cv.circle(dcx, dcy, dr, cv.rad("drum", [(0, "#F7FAFB"), (.7, "#CDD8DF"), (1, "#94A6B3")], .4, .35, .8)))
    for a in range(-110, 40, 25):
        px, py = dcx + (dr - 9) * math.cos(math.radians(a)), dcy + (dr - 9) * math.sin(math.radians(a))
        cv.add(cv.path("M%s %s L%s %s M%s %s L%s %s" % (_n(px - 3.5), _n(py), _n(px + 3.5), _n(py), _n(px), _n(py - 3.5), _n(px), _n(py + 3.5)), stroke="#C84B43", sw=1.8))
    cv.add(cv.text(dcx, dcy + 22, "drum", 12.5, 750, fill=INK))
    cv.add(P.lift(cv, x0 + 12, ly + 62, 40, 20, "dark", 5, 3, hl=False), cv.circle(x0 + 52, ly + 72, 3, "#F0584B"))
    cv.add(cv.line(x0 + 52, ly + 72, dcx - 24, dcy - 24, "#F0584B", 2.6), glow(cv, dcx - 24, dcy - 24, 10, "#F0584B", .8))
    cv.add(cv.text(x0 + 32, ly + 50, "laser", 12, 650, cls="il-ink2"))
    rcx, rcy = x0 + 148, ly + 126
    cv.add(cv.circle(rcx, rcy, 17, cv.g("dark", "deep")), cv.circle(rcx, rcy, 6, "#B9C6CE"))
    for (tx_, ty_) in ((dcx + 33, dcy - 10), (dcx + 38, dcy - 2), (dcx + 38, dcy + 8), (dcx + 34, dcy + 17), (rcx - 22, rcy - 4), (rcx - 24, rcy + 6)):
        cv.add(cv.circle(tx_, ty_, 2.6, "#2A3E49"))
    cv.add(cv.text(rcx, ly + 96, "toner", 12, 650, cls="il-ink2"))
    py_ = ly + 178
    cv.add(cv.rect(x0 + 14, py_, 224, 5, 2, "#FFFFFF", stroke="#9FB3BE", sw=1))
    for k in range(7):
        cv.add(cv.rect(x0 + 74 + k * 12, py_ - 3.6, 6, 3.6, 1, "#2A3E49", op=.85))
    cv.add(cv.circle(dcx, py_ + 17, 12, cv.g("dark", "deep")))
    fx = x0 + 188
    cv.add(cv.circle(fx, py_ - 12, 13, cv.g("coral", "deep")), cv.circle(fx, py_ + 17, 13, cv.g("coral", "deep")))
    for dx in (-7, 0, 7):
        cv.add(cv.path("M%s %s q-4 -6 0 -12 q4 -6 0 -12" % (fx + dx, ly + 140), stroke="#F77F72", sw=2.2, op=.9))
    cv.add(cv.rect(x0 + 206, py_ - 4.4, 26, 4.4, 1.4, "#2A3E49"))
    cv.add(cv.text(x0 + 46, py_ + 38, "paper", 12, 650, cls="il-ink2"), cv.text(fx, py_ + 48, "fuser", 12, 650, cls="il-ink2"))
    # ---- LCD against OLED
    x1 = CARD_X[1]
    lx, ox, sw_ = x1 + 22, x1 + 128, 96
    cv.add(cv.text(lx + sw_ / 2, ly + 40, "LCD", 15, 800, cls="il-ink"), cv.text(ox + sw_ / 2, ly + 40, "OLED", 15, 800, cls="il-ink"))
    # the pixel that is meant to be black
    cv.add(cv.rect(lx + 33, ly + 54, 30, 24, 5, "#4A5560", stroke="#9FB3BE", sw=1.4), glow(cv, lx + 48, ly + 66, 28, "#FFE680", .22))
    cv.add(cv.rect(ox + 33, ly + 54, 30, 24, 5, "#05080A", stroke="#9FB3BE", sw=1.4))
    cv.add(cv.text(lx + sw_ / 2, ly + 100, "dark grey", 12, 650, cls="il-ink2"), cv.text(ox + sw_ / 2, ly + 100, "black: off", 12, 650, cls="il-ink2"))
    # LCD layers: colour filter, liquid crystal, backlight
    fy = ly + 122
    cv.add(cv.rect(lx, fy, sw_, 28, 5, "#FFFFFF"))
    for i, c in enumerate(("#FFC6BB", "#A5E6B8", "#C9EAFB") * 4):
        cv.add(cv.rect(lx + 2 + i * 7.9, fy + 2, 7.5, 24, 1.5, c))
    cv.add(cv.text(lx + sw_ / 2, fy + 18, "filters", 12, 750, fill=INK))
    cv.add(cv.rect(lx, fy + 34, sw_, 28, 5, cv.g("sky")), cv.text(lx + sw_ / 2, fy + 52, "crystals", 12, 750, fill=INK))
    cv.add(cv.rect(lx, fy + 68, sw_, 28, 5, cv.g("sun")), cv.text(lx + sw_ / 2, fy + 86, "backlight", 12, 750, fill=INK))
    # OLED layers: pixels that light themselves, and the circuits behind them
    cv.add(cv.rect(ox, fy, sw_, 28, 5, "#1B2830"))
    for i, c in enumerate(("#FF7B72", "#5BD58B", "#66B8EC", "#05080A")):
        if i < 3:
            cv.add(glow(cv, ox + 13 + i * 24, fy + 14, 13, c, .55))
        cv.add(cv.rect(ox + 3 + i * 24, fy + 4, 20, 20, 4, c, stroke="#9FB3BE" if i == 3 else None, sw=1.2))
    cv.add(cv.text(ox + sw_ / 2, fy + 46, "pixels", 12, 750, cls="il-ink"))
    cv.add(cv.rect(ox, fy + 68, sw_, 28, 5, cv.g("slate")), cv.text(ox + sw_ / 2, fy + 86, "circuits", 12, 750, fill=INK))
    cv.add(cv.text(lx + sw_ / 2, fy + 124, "one light for all", 12, 650, cls="il-ink2"), cv.text(ox + sw_ / 2, fy + 124, "each lights itself", 12, 650, cls="il-ink2"))
    # ---- the 3D printer
    x2 = CARD_X[2]
    cv.add(cv.rect(x2 + 26, ly + 52, 12, 200, 4, cv.g("metal", "side")), cv.rect(x2 + 208, ly + 52, 12, 200, 4, cv.g("metal", "side")), cv.rect(x2 + 26, ly + 52, 194, 12, 4, cv.g("metal")))
    cv.add(cv.rect(x2 + 20, ly + 250, 206, 16, 6, cv.g("dark", "deep")), cv.rect(x2 + 44, ly + 238, 158, 12, 3, cv.g("metal", "deep")))
    cv.add(P.lift(cv, x2 + 100, ly + 66, 54, 22, "sky", 5, 3, hl=False), P.lift(cv, x2 + 106, ly + 90, 42, 38, "plum", 8, 4, hl=False))
    cv.add(cv.poly([(x2 + 116, ly + 132), (x2 + 138, ly + 132), (x2 + 130, ly + 152), (x2 + 124, ly + 152)], "#8799A7"), glow(cv, x2 + 127, ly + 153, 12, "#FF8A3D", .9))
    cv.add(cv.circle(x2 + 62, ly + 100, 24, cv.g("coral", "deep")), cv.circle(x2 + 62, ly + 100, 9, "var(--il-hole)"), cv.circle(x2 + 62, ly + 100, 14, "none", stroke="#FFFFFF", sw=1.6, op=.5))
    cv.add(cv.path("M%s %s Q%s %s %s %s" % (x2 + 82, ly + 90, x2 + 96, ly + 96, x2 + 108, ly + 106), stroke="#F77F72", sw=3))
    cv.add(cv.path("M%s %s L%s %s" % (x2 + 127, ly + 128, x2 + 127, ly + 138), stroke="#F77F72", sw=3))
    widths = [70, 74, 78, 80, 78, 72, 66, 70, 74]
    for i, w_ in enumerate(widths):
        yy = ly + 230 - i * 8
        cv.add(cv.rect(x2 + 127 - w_ / 2, yy, w_, 8, 3, "#F77F72" if i % 2 else "#FFC6BB", stroke="#C84B43", sw=.8))
    cv.add(cv.rect(x2 + 127 - widths[-1] / 2, ly + 230 - 8 * 8 - .5, widths[-1], 3, 1.5, "#FF8A3D"))
    cv.add(P.arrow(cv, [(x2 + 160, ly + 78), (x2 + 196, ly + 78)], ARROW, 3, 9), P.arrow(cv, [(x2 + 196, ly + 78), (x2 + 160, ly + 78)], ARROW, 3, 9))
    cv.add(cv.text(x2 + 62, ly + 138, "filament", 12, 650, cls="il-ink2"), cv.text(x2 + 188, ly + 152, "nozzle", 12, 650, cls="il-ink2"), cv.text(x2 + 190, ly + 208, "layers", 12, 650, cls="il-ink2"))
    return figure(
        "output-devices-how", cv, "How a laser printer, LCD and OLED screens, and a 3D printer work",
        "Three output devices, each drawn working. In a laser printer a laser draws the page as an electric charge on a rotating drum. Toner "
        "powder sticks only to the charged parts of the drum. The paper passes under the drum and picks up the toner, and then a hot fuser "
        "melts the toner into the paper. A liquid crystal display has a backlight behind a layer of liquid crystals and colour filters, so "
        "the light is always on and the crystals block it, which means a black pixel is only dark grey. An OLED display has pixels that make "
        "their own light, so a black pixel is simply switched off and the contrast is higher. A 3D printer feeds plastic filament from a "
        "spool to a heated nozzle that moves across the build plate laying down one thin layer, then another on top, until the whole object is "
        "built.",
        ["Laser printer: a laser draws the page on a drum as a charge, toner sticks to it, the paper picks the toner up and a fuser melts it in.",
         "LCD has a backlight that is always on, so black is dark grey. OLED pixels make their own light, so black is off and the contrast is higher.",
         "A 3D printer melts plastic filament and lays it down one layer at a time until the object is built."],
        "An output device turns data back into something a person can see or hold.")
