"""Illustrations for data representation, data structures and algorithms."""
import math

from .illus import Canvas, PAL, INK, ARROW, figure, illustration, _n
from . import illus_props as P


@illustration("binary-place-value")
def _binary():
    cv = Canvas(800, 500).backdrop()
    bits = [0, 1, 0, 1, 1, 0, 1, 0]
    vals = [128, 64, 32, 16, 8, 4, 2, 1]
    base = 338
    k = 200 / 128.0
    xs = [46 + i * 86 + (24 if i >= 4 else 0) for i in range(8)]
    cv.add(P.band(cv, 24, 22, 752, 112, 20))
    cv.add(cv.rect(24, base + 10, 752, 3, 1.5, "var(--il-line)"))
    for i in range(8):
        x = xs[i]
        on = bits[i]
        cv.add(P.bulb(cv, x + 8, 34, .78, bool(on)))
        cv.add(cv.text(x + 39 - 0, 124, str(bits[i]), 24, 800, cls="il-ink", mono=True))
        h = vals[i] * k
        col = "teal" if on else "slate"
        cv.add(cv.shadow(x + 39, base + 12, 38, 4, .15))
        cv.add(P.lift(cv, x, base - h, 78, h, col, min(8, h / 2), 5 if h > 12 else 2, hl=h > 20))
        cv.add(cv.text(x + 39, base + 40, str(vals[i]), 22, 800, cls="il-ink il-h"))
        cv.add(P.tick(cv, x + 39, base + 70, 11) if on else cv.text(x + 39, base + 76, "skip", 14, 600, cls="il-ink2"))
    cv.add(P.pill(cv, 400, 156, "a 1 means take the column, a 0 means skip it", "paper", 14.5, 14, 30, 700))
    # the tallest column is worth more than everything else together
    cv.add(P.pill(cv, 168, 218, "128 is worth more than all the rest together (127)", "sun", 14, 12, 28, 750, anchor="start"))
    cv.add(P.arrow(cv, [(104, 240), (88, base - 200 + 20)], PAL["sun"][2], 4, 11))
    cv.add(P.pill(cv, 400, 462, "64 + 16 + 8 + 2 = 90", "deep", 20, 22, 38, 800))
    cv.add(P.badge(cv, 30, 150, 1), P.badge(cv, 30, 292, 2), P.badge(cv, 590, 462, 3), P.badge(cv, 120, 232, 4))
    return figure(
        "binary-place-value", cv, "The eight place value columns of a byte, here holding 0101 1010",
        "The eight place value columns of a byte, drawn as blocks whose height is the value of the column: 128, 64, 32, 16, 8, 4, 2 and 1 "
        "from left to right, each one worth double the column to its right. Above each column is a light that is on for a 1 and off for a 0. "
        "To read a binary number, take the value of every column holding a 1 and ignore every column holding a 0. For 0101 1010 that means "
        "taking 64, 16, 8 and 2, which add up to 90. The tallest block shows something worth remembering: the leftmost column, 128, is worth "
        "more than all of the other seven added together, which come to 127.",
        ["Eight columns, and each one is worth double the one to its right.",
         "A 1 means take that column's value. A 0 means skip it.",
         "Add up the columns you took: 64 + 16 + 8 + 2 = 90.",
         "The leftmost bit is worth more than every other bit added together."],
        "Each column doubles. Learn the row 128 64 32 16 8 4 2 1 and every conversion question becomes adding up.")


@illustration("image-layers")
def _image():
    cv = Canvas(800, 500).backdrop()
    grid = ["..yyyy..", ".yyyyyy.", "yyDyyDyy", "yyyyyyyy", "yDyyyyDy", "yyDRRDyy", ".yyyyyy.", "..yyyy.."]
    colmap = {".": "#7CC3F0", "y": "#FFD24A", "D": "#2A3E49", "R": "#F0675B"}
    cs, gx, gy = 36, 56, 84
    cv.add(cv.rect(gx - 8, gy - 8, cs * 8 + 16, cs * 8 + 16, 14, "#FFFFFF"), cv.shadow(gx + cs * 4, gy + cs * 8 + 20, 150, 8, .2))
    for r, row in enumerate(grid):
        for c, ch in enumerate(row):
            cv.add(cv.rect(gx + c * cs, gy + r * cs, cs, cs, 0, colmap[ch]))
    for i in range(9):
        cv.add(cv.line(gx + i * cs, gy, gx + i * cs, gy + 8 * cs, "#10303A", 1, op=.22), cv.line(gx, gy + i * cs, gx + 8 * cs, gy + i * cs, "#10303A", 1, op=.22))
    # sizes
    cv.add(cv.path("M%d %d L%d %d" % (gx, 66, gx + 8 * cs, 66), stroke=ARROW, sw=2.5, op=.6), cv.line(gx, 60, gx, 72, ARROW, 2.5, op=.6), cv.line(gx + 8 * cs, 60, gx + 8 * cs, 72, ARROW, 2.5, op=.6))
    cv.add(P.pill(cv, gx + 4 * cs, 46, "8 pixels wide", "paper", 14.5, 12, 28, 700))
    cv.add(P.pill(cv, gx + 4 * cs, gy + 8 * cs + 42, "8 tall: 64 pixels in all", "paper", 14.5, 12, 28, 700))
    # the chosen pixel
    pr, pc_ = 5, 3
    px, py = gx + pc_ * cs, gy + pr * cs
    cv.add(cv.rect(px - 3, py - 3, cs + 6, cs + 6, 3, "none", stroke="#FFFFFF", sw=4), cv.rect(px - 3, py - 3, cs + 6, cs + 6, 3, "none", stroke="#1F3A44", sw=2))
    cv.add(cv.path("M%d %d L%d %d" % (px + cs + 4, py + 6, 420, 120), stroke=ARROW, sw=2.5, dash="4 6", op=.7), cv.path("M%d %d L%d %d" % (px + cs + 4, py + cs - 2, 420, 232), stroke=ARROW, sw=2.5, dash="4 6", op=.7))
    # zoomed swatch and its three numbers
    cv.add(P.card(cv, 420, 60, 360, 230, 18))
    cv.add(cv.rect(440, 80, 100, 100, 14, "#F0675B"), cv.rect(440, 80, 100, 100, 14, "none", stroke="#fff", sw=4), cv.text(490, 204, "one pixel", 14, 700, cls="il-ink2"))
    for i, (ch, name, val, col) in enumerate((("R", "red", 240, "red"), ("G", "green", 103, "green"), ("B", "blue", 91, "sky"))):
        y = 84 + i * 62
        cv.add(P.lift(cv, 566, y, 34, 34, col, 9, 3, hl=False), cv.text(583, y + 24, ch, 19, 800, fill=P._on(col)))
        cv.add(cv.rect(608, y + 4, 150, 14, 7, "#DDE6EC"), cv.rect(608, y + 4, 150 * val / 255, 14, 7, cv.g(col)))
        cv.add(cv.text(608, y + 40, "%d" % val, 14, 800, anchor="start", cls="il-ink", mono=True), cv.text(646, y + 40, format(val, "08b"), 14, 700, anchor="start", cls="il-ink2", mono=True))
    cv.add(P.pill(cv, 600, 266, "3 numbers × 8 bits = 24 bits = 3 bytes", "sun", 14, 14, 28, 750))
    # the whole formula
    cv.add(P.card(cv, 420, 316, 360, 164, 18))
    cv.add(cv.text(600, 346, "File size in bits", 15, 750, cls="il-ink il-h"))
    items = [("8", "width", "sky"), ("×", "", None), ("8", "height", "mint"), ("×", "", None), ("24", "colour depth", "coral")]
    x = 452
    for t, lab, col in items:
        if col:
            cv.add(P.lift(cv, x, 366, 66 if len(t) > 1 else 52, 44, col, 10, 4, hl=False), cv.text(x + (33 if len(t) > 1 else 26), 396, t, 24, 800, fill=P._on(col), cls="il-h"))
            cv.add(cv.text(x + (33 if len(t) > 1 else 26), 436, lab, 12.5, 600, cls="il-ink2"))
            x += (66 if len(t) > 1 else 52) + 14
        else:
            cv.add(cv.text(x + 4, 396, t, 24, 800, cls="il-ink")); x += 26
    cv.add(cv.text(600, 466, "= 1,536 bits, and ÷ 8 = 192 bytes", 15, 750, cls="il-ink"))
    cv.add(P.badge(cv, 40, 80, 1), P.badge(cv, px + cs + 14, py + 4, 2), P.badge(cv, 438, 266, 3), P.badge(cv, 436, 342, 4))
    return figure(
        "image-layers", cv, "How a bitmap image is stored: a grid of pixels, each three numbers",
        "How a bitmap image is stored. The image is a grid of pixels, and this one is eight by eight, so sixty four pixels in total. Every "
        "pixel holds one colour, and that colour is stored as three numbers: how much red, how much green and how much blue. In 24 bit colour "
        "each of those three numbers gets eight bits, so one pixel costs 8 plus 8 plus 8, which is 24 bits or 3 bytes. The colour depth is "
        "simply how many bits each pixel gets. The file size in bits is the width times the height times the colour depth: for this image "
        "8 times 8 times 24 is 1,536 bits, and dividing by 8 gives 192 bytes.",
        ["A bitmap is a grid of pixels. This one is 8 by 8, so 64 of them.",
         "Pick one pixel. Its colour is three numbers: red, green and blue.",
         "Each number is 8 bits, so one pixel costs 24 bits, which is 3 bytes.",
         "File size = width × height × colour depth. That is the whole formula."],
        "Width times height times colour depth gives bits. Divide by 8 for bytes. Every image file size question is that line and nothing more.")


def wave_path(f, x0, y0, w, h, n=160):
    pts = []
    for i in range(n + 1):
        t = i / n
        pts.append((x0 + t * w, y0 - f(t) * h))
    return "M" + " L".join("%s %s" % (_n(x), _n(y)) for x, y in pts)


@illustration("sound-sampling")
def _sound():
    cv = Canvas(800, 500).backdrop()
    f = lambda t: .62 * math.sin(2 * math.pi * 1.6 * t) + .26 * math.sin(2 * math.pi * 3.7 * t + .6)
    panels = [(30, "Sound is a smooth wave", 0), (176, "Few samples: a rough copy", 11), (322, "Many samples: a close copy", 34)]
    for y, title, n in panels:
        cv.add(P.card(cv, 20, y, 540, 132, 16))
        cv.add(cv.text(52, y + 24, title, 14.5, 750, anchor="start", cls="il-ink il-h"))
        x0, w, mid, h = 48, 490, y + 80, 36
        cv.add(cv.line(x0, mid, x0 + w, mid, "var(--il-line)", 1.5))
        if n:
            for i in range(n):
                t = (i + .5) / n
                xx, yy = x0 + t * w, mid - f(t) * h
                cv.add(cv.rect(xx - w / n * .42, min(mid, yy), w / n * .84, abs(yy - mid), 1, PAL["coral"][1], op=.28))
                cv.add(cv.line(xx, mid, xx, yy, PAL["coral"][1], 2, op=.85))
                cv.add(cv.circle(xx, yy, 4.2 if n < 20 else 3, PAL["coral"][2]))
        cv.add(cv.path(wave_path(f, x0, mid, w, h), stroke=PAL["teal"][1], sw=4.2 if not n else 3, op=1 if not n else .7))
    cv.add(P.pill(cv, 462, 200, "sample rate: 11 a second", "coral", 13, 10, 24, 750))
    cv.add(P.pill(cv, 462, 346, "sample rate: 34 a second", "coral", 13, 10, 24, 750))
    cv.add(cv.text(532, 150, "time →", 12.5, 650, anchor="end", cls="il-ink2"))
    # a microphone feeding the wave
    # bit depth
    cv.add(P.card(cv, 580, 30, 206, 424, 16))
    cv.add(cv.text(683, 58, "Bit depth", 16, 800, cls="il-ink il-h"))
    cv.add(cv.text(683, 78, "how finely each height is rounded", 12.5, 600, cls="il-ink2"))
    top, lh = 106, 40
    for i in range(8):
        yy = top + i * lh
        cv.add(cv.line(612, yy, 760, yy, "var(--il-line)", 1.5))
        cv.add(cv.text(598, yy + 5, str(7 - i), 12.5, 700, cls="il-ink2", mono=True, anchor="end"))
    cv.add(cv.circle(640, top + 3 * lh + 22, 7, PAL["coral"][1], stroke="#fff", sw=2))
    cv.add(P.arrow(cv, [(652, top + 3 * lh + 22), (708, top + 3 * lh)], ARROW, 3.5, 11))
    cv.add(cv.circle(722, top + 3 * lh, 8, PAL["teal"][1], stroke="#fff", sw=2))
    cv.add(P.pill(cv, 683, 400, "3 bits: 8 levels", "paper", 13.5, 10, 26, 750))
    cv.add(cv.text(683, 438, "more bits: finer steps", 12.5, 600, cls="il-ink2"))
    cv.add(P.badge(cv, 28, 30, 1), P.badge(cv, 28, 176, 2), P.badge(cv, 28, 322, 3), P.badge(cv, 590, 30, 4))
    return figure(
        "sound-sampling", cv, "Turning a sound wave into numbers by sampling it",
        "How a sound is turned into numbers. Sound is a wave, a smooth and continuous change in air pressure, and a computer cannot store "
        "smooth because it can only store numbers. So it measures the height of the wave at regular intervals, and each measurement is a "
        "sample. The sample rate is how many measurements are taken each second, in hertz: with only eleven samples the recorded shape is a "
        "rough approximation of the original, while with more than thirty it follows the wave closely. The bit depth is how many bits each "
        "measurement is stored in, and so how finely the height is rounded: three bits give eight levels, each sample is rounded to the "
        "nearest one, and more bits give finer steps. Higher sample rate and higher bit depth both mean a closer recording and a bigger file.",
        ["Sound is a wave: a smooth, continuous change in air pressure.",
         "A computer cannot store smooth. It measures the height at intervals.",
         "Sample more often and the shape you recorded is closer to the original.",
         "Bit depth is how finely each measurement is rounded."],
        "Higher sample rate and higher bit depth both mean a closer recording and a bigger file. That trade is the whole topic.")


def photo_blocks(cv, x, y, w, h, n=6, jitter=False):
    """The photo again, but built of coarse blocks: what lossy compression leaves."""
    out = ""
    pal = ["#9ED8F2", "#8ED5F5", "#B6E4F7", "#5FC38C", "#37A777", "#7FD3A2", "#FFD75E", "#8ED5F5", "#6FC6EF"]
    bw, bh = w / n, h / (n * .7)
    rows = int(round(h / bh))
    for r in range(rows):
        for c in range(n):
            col = pal[(r * 3 + c * 2) % len(pal)] if r < rows - 2 else ["#5FC38C", "#37A777", "#7FD3A2"][(c + r) % 3]
            out += cv.rect(x + c * bw, y + r * bh, bw + .5, bh + .5, 0, col)
    return out


@illustration("compression")
def _compression():
    cv = Canvas(800, 500).backdrop()
    cols = [("Original", "sky"), ("Lossless", "mint"), ("Lossy", "coral")]
    xs = [14, 280, 546]
    for (t, c), x in zip(cols, xs):
        cv.add(P.card(cv, x, 34, 240, 330, 20, t, c))
    # original
    cv.add(P.photo(cv, 44, 96, 180, 120, 8))
    cv.add(P.pill(cv, 134, 244, "12 MB", "sky", 20, 20, 36, 800))
    cv.add(cv.text(134, 292, "every byte of the data,", 14, 600, cls="il-ink2"))
    cv.add(cv.text(134, 312, "nothing thrown away", 14, 600, cls="il-ink2"))
    # lossless
    cv.add(cv.text(400, 92, "finds repetition and says it shorter", 12.5, 650, cls="il-ink2"))
    letters = "AAAAAABBB"
    for i, ch in enumerate(letters):
        cv.add(P.lift(cv, 308 + i * 22, 104, 20, 26, "sky" if ch == "A" else "sun", 5, 3, hl=False), cv.text(318 + i * 22, 123, ch, 13, 800, fill=INK, mono=True))
    cv.add(P.arrow(cv, [(400, 146), (400, 172)], ARROW, 3.5, 11))
    cv.add(P.lift(cv, 360, 180, 44, 30, "sky", 8, 3, hl=False), cv.text(382, 202, "6A", 15, 800, fill=INK, mono=True))
    cv.add(P.lift(cv, 410, 180, 44, 30, "sun", 8, 3, hl=False), cv.text(432, 202, "3B", 15, 800, fill=INK, mono=True))
    cv.add(P.photo(cv, 330, 236, 78, 52, 6), P.pill(cv, 420, 262, "6 MB", "mint", 16, 12, 28, 800, anchor="start"))
    cv.add(P.tick(cv, 316, 318, 12), cv.text(334, 324, "unpack it: identical", 14, 650, anchor="start"))
    # lossy
    cv.add(photo_blocks(cv, 580, 96, 172, 112, 7))
    cv.add(cv.rect(580, 96, 172, 112, 0, "none", stroke="#fff", sw=3))
    for i, (dx, dy, c) in enumerate(((596, 224, "#8ED5F5"), (640, 236, "#5FC38C"), (688, 222, "#FFD75E"), (728, 240, "#37A777"), (664, 252, "#B6E4F7"))):
        cv.add(cv.rect(dx, dy, 14, 14, 2, c, op=.85), cv.rect(dx + 1, dy + 1, 12, 12, 2, "none", stroke="#fff", sw=1))
    cv.add(P.pill(cv, 666, 282, "1 MB", "coral", 20, 20, 36, 800))
    cv.add(cv.text(666, 328, "detail thrown away", 14, 650, cls="il-ink2"))
    cv.add(cv.text(666, 348, "and never coming back", 14, 650, cls="il-ink2"))
    # sizes
    cv.add(P.card(cv, 14, 386, 772, 96, 18))
    for i, (lab, col, share, size) in enumerate((("Original", "sky", 1.0, "12 MB"), ("Lossless", "mint", .5, "6 MB"), ("Lossy", "coral", .083, "1 MB"))):
        y = 400 + i * 26
        cv.add(cv.text(112, y + 16, lab, 14, 750, anchor="end", cls="il-ink"))
        cv.add(P.lift(cv, 126, y, 560 * share, 18, col, 6, 3, hl=False))
        cv.add(cv.text(126 + 560 * share + 10, y + 15, size, 13.5, 800, anchor="start", cls="il-ink"))
    cv.add(P.badge(cv, 28, 40, 1), P.badge(cv, 294, 40, 2), P.badge(cv, 326, 242, 3), P.badge(cv, 560, 40, 4))
    return figure(
        "compression", cv, "Lossless and lossy compression compared with the original file",
        "Compression, with the length of each bar at the bottom standing for the size of the file. The original holds every byte of the data. "
        "Lossless compression finds repetition and records it more briefly: run length encoding replaces a run of identical values with the "
        "value and a count, so six As followed by three Bs becomes 6A 3B, and Huffman coding gives the most common symbols the shortest "
        "codes. Nothing is discarded, so unpacking returns exactly the original file, bit for bit, though the saving is modest. Lossy "
        "compression throws data away permanently, such as detail the eye is unlikely to miss, and so the file becomes much smaller but the "
        "original can never be recovered. Text and program code must be lossless because one wrong byte breaks them. Photos and music can "
        "usually be lossy.",
        ["The original file: every byte of the data, nothing thrown away.",
         "Lossless finds repetition and records it more briefly.",
         "Unpack it and you get back exactly what you started with.",
         "Lossy throws data away permanently, and gets much smaller."],
        "Ask what happens if one byte changes. If the answer is that it breaks, the compression has to be lossless.")


def hooded(cv, x, y, s=1.0):
    """A shadowy figure in a hood, for the attacker."""
    return P.person(cv, x, y, s, "pale", "black", "ink", "bald", mood="smirk", hood=True)


@illustration("encryption")
def _encryption():
    cv = Canvas(800, 500).backdrop()
    # sender, plaintext
    cv.add(P.person(cv, 20, 110, .85, "tan", "black", "teal", "short"))
    cv.add(P.lift(cv, 132, 128, 112, 46, "paper", 12, 5, hl=False), cv.text(188, 160, "HELLO", 22, 800, fill=INK, mono=True))
    cv.add(P.pill(cv, 188, 204, "plaintext", "paper", 14, 12, 26, 700))
    # the lock and key
    cv.add(P.arrow(cv, [(250, 152), (292, 152)], ARROW, 4, 12))
    cv.add(P.key(cv, 300, 52, 1.0, "sun"))
    cv.add(P.padlock(cv, 306, 106, 1.2, "sun"))
    cv.add(P.pill(cv, 340, 204, "key + algorithm", "sun", 13.5, 12, 26, 750))
    cv.add(P.arrow(cv, [(376, 152), (436, 152)], ARROW, 4, 12))
    # ciphertext on the wire
    cv.add(P.lift(cv, 444, 128, 118, 46, "dark", 12, 5, hl=False), cv.text(503, 159, "X#9@Q", 21, 800, fill="#9FE3FF", mono=True))
    cv.add(P.pill(cv, 503, 204, "ciphertext", "paper", 14, 12, 26, 700))
    cv.add(P.arrow(cv, [(570, 152), (600, 152)], ARROW, 4, 12))
    # the eavesdropper
    cv.add(hooded(cv, 412, 234, .72))
    cv.add(P.magnifier(cv, 520, 262, .85, 20))
    cv.add(P.pill(cv, 560, 318, "just nonsense!", "red", 13.5, 12, 26, 750))
    # the receiver
    cv.add(P.key(cv, 604, 52, 1.0, "sun"))
    cv.add(P.padlock(cv, 612, 106, 1.2, "mint", True))
    cv.add(P.arrow(cv, [(684, 152), (704, 152)], ARROW, 3, 10))
    cv.add(P.lift(cv, 706, 130, 78, 44, "paper", 11, 4, hl=False), cv.text(745, 159, "HELLO", 17, 800, fill=INK, mono=True))
    cv.add(P.pill(cv, 690, 204, "the right key unlocks it", "mint", 13, 12, 26, 750))
    cv.add(P.person(cv, 660, 226, .72, "brown", "brown", "plum", "bun", True))
    # hashing
    cv.add(P.card(cv, 14, 372, 772, 112, 18, "Hashing is different", "plum", .22))
    cv.add(P.lift(cv, 44, 410, 150, 42, "paper", 12, 4, hl=False), cv.text(119, 438, "password123", 16, 800, fill=INK, mono=True))
    cv.add(P.arrow(cv, [(204, 431), (292, 431)], PAL["plum"][1], 5, 13))
    cv.add(P.gear(cv, 336, 431, 32, "plum", 8))
    cv.add(cv.text(336, 482, "hash function", 12.5, 650, cls="il-ink2"))
    cv.add(P.arrow(cv, [(384, 431), (452, 431)], PAL["plum"][1], 5, 13))
    cv.add(P.lift(cv, 462, 410, 200, 42, "dark", 12, 4, hl=False), cv.text(562, 437, "5f4dcc3b5aa7...", 15, 800, fill="#9FE3FF", mono=True))
    cv.add(P.cross(cv, 704, 431, 16), cv.text(728, 428, "no way", 14.5, 700, anchor="start"), cv.text(728, 446, "back", 14.5, 700, anchor="start"))
    cv.add(P.badge(cv, 30, 128, 1), P.badge(cv, 360, 70, 2), P.badge(cv, 576, 122, 3), P.badge(cv, 654, 80, 4), P.badge(cv, 30, 392, 5))
    return figure(
        "encryption", cv, "Encryption: plaintext locked with a key, and hashing, which cannot be undone",
        "Encryption, drawn as a journey. You begin with plaintext, the message as anybody could read it, here the word HELLO. An encryption "
        "algorithm combined with a key turns it into ciphertext, which looks like nonsense. The algorithm is usually public and well known; "
        "the secrecy lives entirely in the key, and the same algorithm with a different key produces completely different ciphertext. The "
        "ciphertext is what actually travels across the network, so an attacker who intercepts it, shown as a hooded figure with a magnifying "
        "glass, sees only nonsense. The right key reverses the process and the receiver gets the plaintext back; the wrong key gives nothing "
        "useful. Hashing is different. A hash function turns any input, such as a password, into a fixed length string, and it is one way: "
        "there is no way back from the hash to the original.",
        ["You start with plaintext: the message as anyone could read it.",
         "A key and an algorithm turn it into ciphertext.",
         "The ciphertext is what travels, and it is what an attacker sees.",
         "The right key reverses it. The wrong key gives nothing useful.",
         "Hashing is different: it is one way, and there is no way back."],
        "The algorithm is public. The key is the secret. That one sentence answers most encryption questions.")


@illustration("array-2d")
def _arrays():
    cv = Canvas(800, 500).backdrop()
    cards = [("One dimension", "teal", 14), ("Two dimensions", "plum", 280), ("A record", "coral", 546)]
    for t, c, x in cards:
        cv.add(P.card(cv, x, 34, 240, 380, 20, t, c))
    # 1D
    vals = [4, 9, 2, 7, 1]
    for i, v in enumerate(vals):
        x = 28 + i * 44
        hot = i == 3
        cv.add(P.lift(cv, x, 150, 40, 56, "sun" if hot else "sky", 9, 4, hl=False), cv.text(x + 20, 188, str(v), 24, 800, fill=INK, mono=True))
        cv.add(cv.text(x + 20, 242, str(i), 16, 800, cls="il-ink2", mono=True))
    cv.add(cv.text(134, 266, "index starts at 0", 13.5, 650, cls="il-ink2"))
    cv.add(P.arrow(cv, [(28 + 3 * 44 + 20, 130), (28 + 3 * 44 + 20, 142)], PAL["sun"][2], 5, 11))
    cv.add(P.pill(cv, 134, 110, "numbers[3]", "sun", 16, 14, 30, 800))
    cv.add(cv.text(134, 306, "= 7", 28, 800, cls="il-ink il-h", mono=True))
    cv.add(P.pill(cv, 134, 346, "one index finds one value", "paper", 13.5, 10, 26, 650))
    # 2D
    gx, gy, cs = 336, 138, 50
    nums = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    cv.add(cv.rect(gx - 2, gy + 1 * cs - 2, 3 * cs + 4, cs + 4, 10, PAL["sun"][1], op=.28), cv.rect(gx + 2 * cs - 2, gy - 2, cs + 4, 3 * cs + 4, 10, PAL["sky"][1], op=.28))
    for r in range(3):
        for c in range(3):
            hot = (r, c) == (1, 2)
            cv.add(P.lift(cv, gx + c * cs + 2, gy + r * cs + 2, cs - 4, cs - 4, "coral" if hot else "paper", 8, 3, hl=False), cv.text(gx + c * cs + cs / 2, gy + r * cs + 32, str(nums[r][c]), 20, 800, fill=INK, mono=True))
    for i in range(3):
        cv.add(cv.text(gx + i * cs + cs / 2, gy - 12, str(i), 15, 800, cls="il-ink2", mono=True), cv.text(gx - 16, gy + i * cs + 31, str(i), 15, 800, cls="il-ink2", mono=True))
    cv.add(cv.text(gx + 1.5 * cs, gy - 36, "column →", 12.5, 650, cls="il-ink2"), cv.text(gx - 30, gy - 14, "row ↓", 12.5, 650, cls="il-ink2"))
    cv.add(P.pill(cv, 400, 330, "grid[1][2]", "coral", 18, 16, 32, 800))
    cv.add(cv.text(400, 372, "= 6", 22, 800, cls="il-ink il-h", mono=True))
    cv.add(P.pill(cv, 400, 396, "row first, then column", "paper", 13, 10, 24, 700))
    # record
    cv.add(P.lift(cv, 566, 100, 200, 250, "paper", 16, 6, hl=False))
    cv.add(cv.rect(566, 100, 200, 44, 16, cv.g("coral")) + cv.rect(566, 126, 200, 18, 0, PAL["coral"][1]))
    cv.add(cv.text(666, 129, "STUDENT", 16, 800, fill=P._on("coral"), spacing=2))
    cv.add(P.person(cv, 580, 150, .5, "tan", "black", "teal", "short"))
    fields = [("name", "\"Asha\"", "text"), ("age", "15", "integer"), ("member", "True", "boolean")]
    for i, (k, v, ty) in enumerate(fields):
        yy = 214 + i * 44
        cv.add(cv.rect(580, yy, 172, 34, 9, "#EEF3F6"), cv.text(590, yy + 22, k, 14, 800, anchor="start", fill=INK, mono=True), cv.text(646, yy + 22, v, 14, 750, anchor="start", fill=INK, mono=True))
        cv.add(cv.text(746, yy + 22, ty, 11, 700, anchor="end", fill="#547080"))
    cv.add(P.pill(cv, 666, 372, "student.name", "coral", 16, 14, 30, 800))
    cv.add(P.pill(cv, 134, 444, "same type, one row", "paper", 14, 12, 26, 700), P.pill(cv, 400, 444, "same type, rows and columns", "paper", 14, 12, 26, 700), P.pill(cv, 666, 444, "different types, by name", "paper", 14, 12, 26, 700))
    cv.add(P.badge(cv, 30, 36, 1), P.badge(cv, 296, 36, 2), P.badge(cv, 336, 330, 3), P.badge(cv, 562, 36, 4))
    return figure(
        "array-2d", cv, "Arrays and records: one index, two indexes, or a name",
        "Arrays and records. A one dimensional array is a row of values of the same type, reached by a single index, and the indexes start "
        "at zero, so in the row 4, 9, 2, 7, 1 the value at index 3 is 7. A two dimensional array is a grid of rows and columns, reached by "
        "two indexes, and the order is always row first and column second: in a three by three grid, grid index one index two means the "
        "second row and the third column, which here holds 6. A record is different: it holds a group of fields that can be of different "
        "types, such as a text name, an integer age and a boolean, and each field is reached by its name rather than by a position.",
        ["A one dimensional array: values in a row, reached by one index.",
         "A two dimensional array: rows and columns, reached by two.",
         "grid[1][2] means row 1, then column 2. Row always comes first.",
         "A record holds fields of different types, reached by name."],
        "Row first, then column. Say it out loud every time you write a 2D index and you will stop getting it backwards.")


def plate(cv, cx, y, color, w=170):
    """A dinner plate seen slightly from above, centred on cx."""
    lo, base, hi = PAL[color]
    out = cv.ellipse(cx, y + 12, w / 2, 17, hi)
    out += cv.ellipse(cx, y + 6, w / 2, 17, cv.g(color))
    out += cv.ellipse(cx, y + 3, w / 2 - 26, 9, hi, op=.35)
    out += cv.ellipse(cx, y + 1, w / 2 - 30, 7, "#fff", op=.25)
    return out


@illustration("stack-queue")
def _stack_queue():
    cv = Canvas(800, 500).backdrop()
    cv.add(P.card(cv, 14, 34, 380, 446, 20, "Stack: last in, first out", "teal"))
    cv.add(P.card(cv, 406, 34, 380, 446, 20, "Queue: first in, first out", "coral"))
    # a stack of plates, drawn from the bottom up
    cv.add(cv.shadow(204, 400, 112, 8, .25))
    for i, (col, lab) in enumerate((("teal", "1st"), ("sun", "2nd"), ("coral", "3rd"))):
        y = 346 - i * 46
        cv.add(plate(cv, 204, y, col))
        cv.add(cv.text(204 + 100, y + 14, lab, 14, 800, anchor="start", cls="il-ink2"))
    cv.add(cv.group(plate(cv, 0, 0, "plum", 170), 204, 150, 1, extra=' opacity=".45"'))
    cv.add(cv.rect(119, 146, 170, 36, 18, "none", stroke=PAL["plum"][2], sw=2.5, dash="6 6", op=.9))
    cv.add(P.arrow(cv, [(86, 128), (86, 236)], PAL["teal"][1], 7, 18))
    cv.add(P.pill(cv, 86, 106, "push", "teal", 16, 14, 30, 800))
    cv.add(P.arrow(cv, [(322, 244), (322, 130)], PAL["coral"][1], 7, 18))
    cv.add(P.pill(cv, 322, 106, "pop", "coral", 16, 14, 30, 800))
    cv.add(cv.text(204, 440, "only the top plate can be reached", 13.5, 650, cls="il-ink2"))
    cv.add(cv.text(204, 462, "the last one on is the first one off", 13.5, 650, cls="il-ink2"))
    # the queue at a till
    ground = 396
    cv.add(cv.rect(420, ground, 352, 10, 5, "var(--il-line)"))
    cv.add(P.lift(cv, 678, 150, 84, 246, "slate", 12, 5, hl=False))
    cv.add(P.lift(cv, 690, 184, 60, 38, "dark", 9, 3, hl=False), cv.text(720, 210, "£", 22, 800, fill="#7CF0B0"))
    cv.add(cv.text(720, 254, "till", 15, 800, fill=INK))
    people = [("light", "black", "teal", "short", False), ("tan", "brown", "plum", "bun", True), ("brown", "black", "sun", "curly", False), ("pale", "ginger", "sky", "long", False)]
    top = ground - 150 * .5 + 2
    for i, (sk, hr, sh, st, gl) in enumerate(people):
        x = 600 - i * 62
        cv.add(P.person(cv, x, top, .5, sk, hr, sh, st, gl))
        cv.add(P.pill(cv, x + 30, top - 16, str(i + 1), "paper", 14, 8, 24, 800))
    # a new arrival joins the back, the front one is served
    cv.add(P.person(cv, 424, 130, .46, "deep", "black", "red", "short"))
    cv.add(P.arrow(cv, [(470, 176), (440, 250), (418, 316)], PAL["coral"][1], 5, 14, dash="7 6"))
    cv.add(P.pill(cv, 548, 150, "enqueue", "coral", 15, 12, 28, 800))
    cv.add(cv.text(548, 176, "joins the back", 12.5, 650, cls="il-ink2"))
    cv.add(P.arrow(cv, [(640, 292), (654, 262), (674, 252)], PAL["teal"][1], 5, 13))
    cv.add(P.pill(cv, 572, 236, "dequeue", "teal", 15, 12, 28, 800))
    cv.add(cv.text(572, 262, "served from the front", 12.5, 650, cls="il-ink2"))
    cv.add(P.arrow(cv, [(536, 438), (640, 438)], ARROW, 4, 12, op=.55))
    cv.add(cv.text(430, 444, "BACK", 13, 800, spacing=2, anchor="start", cls="il-ink2"))
    cv.add(cv.text(656, 444, "FRONT", 13, 800, spacing=2, anchor="start", cls="il-ink2"))
    cv.add(P.badge(cv, 36, 40, 1), P.badge(cv, 120, 170, 2), P.badge(cv, 356, 170, 3), P.badge(cv, 440, 40, 4), P.badge(cv, 512, 236, 5))
    return figure(
        "stack-queue", cv, "A stack of plates and a queue at a till",
        "Two linear data structures, drawn as the two physical things they are named after. A stack is a pile of plates: items are pushed "
        "onto the top and popped off the top, so the last item in is the first one out, which is called LIFO. Pushing first, then second, "
        "then third gives a pile with third on top, and popping returns third. Only the top item can be reached, and a pointer records where "
        "the top is. Stacks are what a computer uses to remember where to return to after a subroutine call, and to undo. A queue is a line "
        "of people at a till: new items join the back and items leave from the front, so the first item in is the first one out, which is "
        "called FIFO. Queues are used where things must be handled in the order they arrived, such as print jobs and keyboard input.",
        ["A stack is a pile. New items go on the top.",
         "Push another one and it goes on top again.",
         "Pop takes the top one off, so the last in is the first out.",
         "A queue is a line. New items join the back.",
         "Dequeue takes from the front, so the first in is the first out."],
        "LIFO and FIFO are not jargon to memorise. A stack of plates and a queue at a shop behave exactly like this.")


def ball(cv, cx, cy, r, color, label, size=24):
    """A glossy round node with a value in it."""
    out = cv.shadow(cx, cy + r + 9, r * .85, 4, .22)
    out += cv.circle(cx, cy + 5, r, PAL[color][2])
    out += cv.circle(cx, cy, r, cv.g(color))
    out += cv.ellipse(cx - r * .2, cy - r * .52, r * .5, r * .2, "#fff", op=.3)
    out += cv.text(cx, cy + size * .35, label, size, 800, fill=P._on(color), mono=True)
    return out


@illustration("binary-tree")
def _tree():
    cv = Canvas(800, 500).backdrop()
    cv.add(P.card(cv, 14, 34, 546, 448, 20, "A binary search tree", "teal"))
    N = {50: (287, 120), 30: (167, 228), 70: (407, 228), 20: (107, 336), 37: (227, 336), 60: (347, 336), 90: (467, 336)}
    EDGES = [(50, 30), (50, 70), (30, 20), (30, 37), (70, 60), (70, 90)]
    on_path = {(50, 30), (30, 37)}
    for a, b in EDGES:
        d = "M%d %d L%d %d" % (N[a] + N[b])
        cv.add(P.cable(cv, d, "sun" if (a, b) in on_path else "slate", 8 if (a, b) in on_path else 5))
    tone = {50: "sun", 30: "sun", 37: "green"}
    for v, (x, y) in N.items():
        cv.add(ball(cv, x, y, 29, tone.get(v, "sky"), str(v)))
    cv.add(P.pill(cv, 206, 120, "root", "plum", 14, 12, 26, 800))
    cv.add(P.pill(cv, 338, 120, "find 37", "sun", 14, 12, 26, 800, anchor="start"))
    cv.add(P.pill(cv, 78, 168, "37 < 50: go left", "paper", 13.5, 12, 28, 750, anchor="start"))
    cv.add(P.pill(cv, 216, 276, "37 > 30: go right", "paper", 13.5, 12, 28, 750, anchor="start"))
    cv.add(P.pill(cv, 227, 394, "found!", "green", 15, 14, 28, 800))
    cv.add(cv.path("M84 416 L84 426 L490 426 L490 416", stroke=ARROW, sw=2.5, op=.5))
    cv.add(P.pill(cv, 287, 452, "leaves: no children", "lilac", 14, 12, 28, 750))
    # the rule, in miniature
    cv.add(P.card(cv, 576, 34, 210, 200, 20, "The rule", "plum"))
    cv.add(P.cable(cv, "M681 98 L621 150", "slate", 4), P.cable(cv, "M681 98 L741 150", "slate", 4))
    cv.add(ball(cv, 681, 98, 24, "sky", "30", 20), ball(cv, 621, 150, 24, "lilac", "20", 20), ball(cv, 741, 150, 24, "mint", "37", 20))
    cv.add(P.pill(cv, 621, 194, "smaller", "lilac", 13, 10, 24, 750), P.pill(cv, 741, 194, "larger", "mint", 13, 10, 24, 750))
    cv.add(cv.text(681, 222, "left < parent < right", 12.5, 700, cls="il-ink2", mono=True))
    # why it is fast: the sorted values left in play after each comparison
    cv.add(P.card(cv, 576, 254, 210, 228, 20, "Why it is fast", "coral"))
    vals = [20, 30, 37, 50, 60, 70, 90]
    rows = [("7 items to search", set(range(7))), ("after 1 comparison: 3 left", {0, 1, 2}), ("after 2 comparisons: 1 left", {2})]
    y = 302
    for label, live in rows:
        cv.add(cv.text(592, y, label, 12.5, 700, anchor="start", cls="il-ink2"))
        for i, v in enumerate(vals):
            x = 592 + i * 26
            if i in live:
                col = "green" if live == {2} else "sky"
                cv.add(P.lift(cv, x, y + 9, 24, 24, col, 6, 3, hl=False), cv.text(x + 12, y + 26, str(v), 11.5, 800, fill=P._on(col), mono=True))
            else:
                cv.add(cv.rect(x, y + 9, 24, 24, 6, "none", stroke="var(--il-line)", sw=1.6, dash="3 3"))
        y += 50
    cv.add(cv.text(681, 460, "a million items needs", 13, 700, cls="il-ink"), cv.text(681, 477, "only about 20 comparisons", 13, 700, cls="il-ink"))
    cv.add(P.badge(cv, 30, 36, 1), P.badge(cv, 590, 36, 2), P.badge(cv, 452, 120, 3), P.badge(cv, 50, 168, 4), P.badge(cv, 590, 256, 5))
    return figure(
        "binary-tree", cv, "A binary search tree",
        "A binary search tree holding the values 50, 30, 70, 20, 37, 60 and 90. Every node has at most two children, the node at the top is "
        "the root, and the nodes with no children at the bottom are the leaves. What makes it a search tree rather than just a binary tree is "
        "the rule about where things go: anything smaller than a node is placed in its left subtree and anything larger in its right subtree. "
        "Searching is then a matter of comparing and moving. To find 37, start at the root, 50. 37 is smaller, so go left to 30. 37 is larger "
        "than 30, so go right, and there it is. Three comparisons for seven items, because each comparison throws away half of what is left, "
        "in the same way a binary search does on a sorted list. That is why a balanced tree of a million items needs about twenty comparisons "
        "rather than a million.",
        ["A binary tree: every node has at most two children.",
         "In a binary search tree, smaller goes left and larger goes right.",
         "Searching for 37: start at the root and compare.",
         "37 is less than 50, so go left. More than 30, so go right. Found.",
         "Three comparisons for seven items. That is why trees are fast."],
        "Every comparison halves what is left. A tree is binary search, built into the shape of the data.")


# ---------------------------------------------------------------- databases

def link_icon(cv, cx, cy, s=1.0, color="#C84B43"):
    """Two chain links, for a foreign key."""
    body = cv.rect(-15, -6.5, 18, 13, 6.5, "none", stroke=color, sw=3.2) + cv.rect(-3, -6.5, 18, 13, 6.5, "none", stroke=color, sw=3.2)
    return cv.group(body, cx, cy, s, rot=-30)


def pencil(cv, cx, cy, s=1.0):
    body = cv.rect(-30, -7, 46, 14, 3, cv.g("sun"))
    body += cv.poly([(16, -7), (33, 0), (16, 7)], "#F4D9B0") + cv.poly([(27, -3), (33, 0), (27, 3)], "#2A3E49")
    body += cv.rect(-40, -7, 11, 14, 3, cv.g("coral")) + cv.rect(-29, -7, 3, 14, 0, PAL["metal"][1])
    return cv.group(body, cx, cy, s, rot=-35)


def db_table(cv, x, y, w, h, color, title, cols, widths, rows, pk=None, fks=(), marks=(), note=None):
    """A table drawn as the grid it is: coloured header, one white cell per value.

    pk and fks are column indexes; marks is a list of (row, col, outline colour).
    """
    cv.add(P.card(cv, x, y, w, h, 18, title, color))
    x0 = x + 8
    cv.add(cv.rect(x0, y + 24, sum(widths), 26, 7, cv.g(color)))
    cx = x0
    for i, (c, cw) in enumerate(zip(cols, widths)):
        cv.add(cv.text(cx + 10, y + 42, c, 13, 800, anchor="start", fill=P._on(color)))
        if i == pk:
            cv.add(P.key(cv, cx + cw - 34, y + 32, .32, "sun"))
        if i in fks:
            cv.add(link_icon(cv, cx + cw - 20, y + 37, .9))
        cx += cw
    for r, row in enumerate(rows):
        ry = y + 56 + r * 32
        cx = x0
        for i, (v, cw) in enumerate(zip(row, widths)):
            fill = "#FFF1BE" if i == pk else "#FFE3DD" if i in fks else "#FFFFFF"
            cv.add(cv.rect(cx + 1, ry, cw - 2, 28, 6, fill, stroke="#DCE6EC", sw=1))
            cv.add(cv.text(cx + 10, ry + 19, v, 13.5, 750 if (i == pk or i in fks) else 600, anchor="start", fill=INK, mono=(i == pk or i in fks)))
            cx += cw
    for r, c, col in marks:
        cx = x0 + sum(widths[:c])
        cv.add(cv.rect(cx + 1, y + 56 + r * 32, widths[c] - 2, 28, 6, "none", stroke=col, sw=3.2))
    if note:
        cv.add(P.key(cv, x + 16, y + h - 26, .42, "sun"), cv.text(x + 58, y + h - 14, note, 12.5, 650, anchor="start", cls="il-ink2"))


@illustration("database-tables")
def _db():
    cv = Canvas(800, 500).backdrop()
    S, C = "#C84B43", "#0F7C84"
    db_table(cv, 24, 46, 352, 194, "teal", "Students", ["StudentID", "Name", "Year"], [114, 150, 72],
             [("S01", "Aisha Khan", "Y10"), ("S02", "Tom Reilly", "Y11"), ("S03", "Mia Okafor", "Y10")],
             pk=0, marks=[(0, 0, S)], note="primary key: different in every row")
    db_table(cv, 424, 46, 352, 194, "plum", "Courses", ["CourseID", "Subject", "Teacher"], [114, 112, 110],
             [("C01", "Computing", "Mr Ali"), ("C02", "Physics", "Ms Dale"), ("C03", "Art", "Mr Boyd")],
             pk=0, marks=[(0, 0, C)], note="its own primary key")
    db_table(cv, 216, 318, 368, 160, "coral", "Enrolments", ["StudentID", "CourseID"], [176, 176],
             [("S01", "C01"), ("S01", "C03"), ("S02", "C02")], fks=(0, 1), marks=[(0, 0, S), (0, 1, C)])
    # each foreign key points back at the primary key it holds
    cv.add(P.curve_arrow(cv, (300, 318), (300, 282), (92, 284), (92, 248), S, 4, 13))
    cv.add(P.curve_arrow(cv, (488, 318), (488, 292), (480, 276), (480, 248), C, 4, 13))
    cv.add(P.pill(cv, 196, 283, "foreign key", "coral", 13, 12, 26, 800), P.pill(cv, 484, 283, "foreign key", "teal", 13, 12, 26, 800))
    # why it matters
    cv.add(P.band(cv, 24, 330, 176, 148, 18), P.band(cv, 600, 330, 176, 148, 18))
    cv.add(P.person(cv, 88, 336, .42, "tan", "black", "teal", "bun"))
    for i, t in enumerate(("Aisha is stored once,", "even though she", "takes two courses.")):
        cv.add(cv.text(112, 420 + i * 19, t, 13, 700, cls="il-ink"))
    cv.add(pencil(cv, 688, 372, 1.05))
    for i, t in enumerate(("Change a teacher", "once, not on", "300 rows.")):
        cv.add(cv.text(688, 420 + i * 19, t, 13, 700, cls="il-ink"))
    cv.add(P.badge(cv, 40, 48, 1), P.badge(cv, 356, 214, 2), P.badge(cv, 440, 48, 3), P.badge(cv, 232, 320, 4), P.badge(cv, 40, 332, 5))
    return figure(
        "database-tables", cv, "Tables, keys and the link between them",
        "A relational database drawn as separate tables. One table holds students, with a row for each student and a column for each field: "
        "StudentID, Name and Year. One field is chosen as the primary key, here StudentID, and its value must be different in every row and "
        "must never be reused, which is why a name makes a poor key and an ID number makes a good one. A second table holds courses, with "
        "CourseID as its own primary key. The two are joined by a third table of enrolments holding pairs of StudentID and CourseID, and in "
        "that table each of those fields is a foreign key, meaning a field that holds the primary key of another table. In the picture the "
        "enrolment row S01 and C01 points back at student S01 and course C01. Splitting the data this way is normalisation, and the reason "
        "for it is that every fact is then stored exactly once: when a course changes teacher you change one row in the courses table rather "
        "than three hundred rows in one enormous table, and there is no way for two of those rows to end up disagreeing.",
        ["One table for students. Each row is a student, each column a field.",
         "A primary key: one field whose value is different in every row.",
         "A second table for courses, with its own primary key.",
         "A foreign key in one table holds the primary key of the other.",
         "That link is why the data is stored once and not repeated."],
        "Store every fact once. Almost every database exam answer comes back to that sentence.")


# ------------------------------------------------------------------- logic

def gate_and(cv, x, y, w=84, h=80, color="teal"):
    """An AND gate: flat on the left, round on the right."""
    r = h / 2
    d = lambda dy: "M%s %s L%s %s A%s %s 0 0 1 %s %s L%s %s Z" % (_n(x), _n(y + dy), _n(x + w - r), _n(y + dy), _n(r), _n(r), _n(x + w - r), _n(y + dy + h), _n(x), _n(y + dy + h))
    out = cv.path(d(5), fill=PAL[color][2]) + cv.path(d(0), fill=cv.g(color))
    out += cv.path("M%s %s L%s %s" % (_n(x + 8), _n(y + 7), _n(x + w - r - 4), _n(y + 7)), stroke="#fff", sw=4, op=.35)
    out += cv.text(x + w * .4, y + h / 2 + 6, "AND", 17, 800, fill=P._on(color))
    return out


def gate_not(cv, x, y, w=60, h=56, color="plum"):
    """A NOT gate: a triangle with a bubble on its point."""
    pts = lambda dy: [(x, y + dy), (x, y + h + dy), (x + w, y + h / 2 + dy)]
    out = cv.poly(pts(5), PAL[color][2], stroke=PAL[color][2], sw=2) + cv.poly(pts(0), cv.g(color), stroke=PAL[color][2], sw=1)
    out += cv.circle(x + w + 7, y + h / 2 + 4, 7, PAL[color][2]) + cv.circle(x + w + 7, y + h / 2, 7, cv.g(color), stroke=PAL[color][2], sw=1.5)
    out += cv.text(x + w * .34, y + h / 2 + 5, "NOT", 14, 800, fill=P._on(color))
    return out


def wire(cv, pts, on):
    d = "M" + " L".join("%s %s" % (_n(a), _n(b)) for a, b in pts)
    if on:
        return cv.path(d, stroke="#E39A00", sw=8) + cv.path(d, stroke="#FFC933", sw=5.5) + cv.path(d, stroke="#FFF0A8", sw=1.8, op=.9)
    return cv.path(d, stroke="#8EA2AE", sw=8) + cv.path(d, stroke="#B7C6CF", sw=5.5)


def sig(cv, x, y, v):
    """The 1 or 0 written on a wire."""
    out = cv.circle(x, y, 15, "#FFFFFF") + cv.circle(x, y, 12, cv.g("sun") if v else cv.g("slate"))
    return out + cv.text(x, y + 5.5, str(v), 16, 800, fill=INK, mono=True)


def circuit(cv, x, y, w, h, title, a, b, color):
    cv.add(P.card(cv, x, y, w, h, 20, title, color))
    mid = y + 112
    ya, yb = mid - 20, mid + 20
    and_out = int(a and b)
    q = int(not and_out)
    cv.add(wire(cv, [(x + 108, ya), (x + 210, ya)], a), wire(cv, [(x + 108, yb), (x + 210, yb)], b))
    cv.add(wire(cv, [(x + 294, mid), (x + 342, mid)], and_out), wire(cv, [(x + 416, mid), (x + 470, mid)], q))
    for lab, yy, v in (("A", ya, a), ("B", yb, b)):
        cv.add(cv.text(x + 36, yy + 7, lab, 20, 800, cls="il-ink"), P.toggle(cv, x + 52, yy - 15, bool(v)))
    cv.add(gate_and(cv, x + 210, mid - 40), gate_not(cv, x + 342, mid - 27))
    cv.add(sig(cv, x + 150, ya, a), sig(cv, x + 150, yb, b), sig(cv, x + 318, mid, and_out), sig(cv, x + 444, mid, q))
    cv.add(P.bulb(cv, x + 466, mid - 40, 1, bool(q)))
    cv.add(cv.text(x + 491, mid + 58, "Q = %d" % q, 17, 800, cls="il-ink", mono=True))
    return mid


@illustration("logic-circuit")
def _logic():
    cv = Canvas(800, 500).backdrop()
    m1 = circuit(cv, 14, 34, 546, 214, "A = 1, B = 0", 1, 0, "teal")
    m2 = circuit(cv, 14, 272, 546, 214, "A = 1, B = 1", 1, 1, "coral")
    # the truth table, with the two cases above picked out
    cv.add(P.card(cv, 576, 34, 210, 330, 20, "Truth table", "plum"))
    xs = (609, 649, 701, 753)
    cv.add(cv.rect(589, 66, 184, 28, 8, cv.g("plum")))
    for xx, t in zip(xs, ("A", "B", "AND", "Q")):
        cv.add(cv.text(xx, 86, t, 14, 800, fill=P._on("plum")))
    rows = [(0, 0, 0, 1), (0, 1, 0, 1), (1, 0, 0, 1), (1, 1, 1, 0)]
    for r, row in enumerate(rows):
        ry = 102 + r * 42
        fill, stroke, sw = "#FFFFFF", "#DCE6EC", 1
        if r == 2:
            fill, stroke, sw = "#D5F2F3", "#0F7C84", 3
        if r == 3:
            fill, stroke, sw = "#FFE1DC", "#C84B43", 3
        cv.add(cv.rect(589, ry, 184, 34, 8, fill, stroke=stroke, sw=sw))
        for xx, v in zip(xs, row):
            cv.add(cv.text(xx, ry + 23, str(v), 17, 800, fill=INK, mono=True))
    cv.add(cv.text(681, 288, "Q is 1 every time", 13, 700, cls="il-ink"), cv.text(681, 307, "except when A and B", 13, 700, cls="il-ink"),
           cv.text(681, 326, "are both 1", 13, 700, cls="il-ink"))
    # the whole circuit as one line
    cv.add(P.card(cv, 576, 390, 210, 96, 20))
    cv.add(cv.text(681, 428, "Q = NOT (A AND B)", 15, 800, cls="il-ink", mono=True))
    cv.add(P.pill(cv, 681, 456, "that is a NAND gate", "sun", 13.5, 14, 28, 800))
    cv.add(P.badge(cv, 30, 36, 1), P.badge(cv, 14 + 318, m1 - 40, 2), P.badge(cv, 14 + 372, m1 - 50, 3), P.badge(cv, 30, 274, 4), P.badge(cv, 592, 392, 5))
    return figure(
        "logic-circuit", cv, "Tracing a signal through a logic circuit",
        "A circuit with two inputs, A and B, feeding an AND gate whose output feeds a NOT gate, which produces the output Q, drawn twice. "
        "Every wire carries a 1 or a 0, written on it, and a wire carrying a 1 is drawn lit. In the first case A is 1 and B is 0. The AND gate "
        "outputs 1 only when both its inputs are 1, so it outputs 0. The NOT gate inverts whatever it is given, so that 0 becomes a 1 and Q is "
        "1, and the bulb is on. In the second case both A and B are 1, so the AND gate outputs 1, the NOT gate inverts it, and Q becomes 0 and "
        "the bulb is off. A truth table beside the circuit lists all four combinations, with Q equal to 1 in every row except the one where "
        "both inputs are 1. The whole circuit is Q equals NOT, bracket, A AND B, bracket, and a combination that common has its own name and "
        "symbol: it is a NAND gate. When reading a circuit in an exam, work left to right and write the value on every wire as you go, because "
        "the marks are for the intermediate columns as much as the answer.",
        ["Two inputs, one AND gate, one NOT gate, one output.",
         "A = 1 and B = 0. AND needs both, so it gives 0.",
         "NOT flips it, so Q becomes 1.",
         "A = 1 and B = 1. AND gives 1, NOT flips it, Q is 0.",
         "Q = NOT (A AND B). That is a NAND gate, written out."],
        "Label every wire as you go. An intermediate column in a truth table is a mark, and it is also how you catch your own mistake.")


# -------------------------------------------------------------------- mesh

def _mix(a, b, t):
    ca = [int(a[i:i + 2], 16) for i in (1, 3, 5)]
    cb = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#%02x%02x%02x" % tuple(int(ca[k] + (cb[k] - ca[k]) * t) for k in range(3))


def facet_ball(cv, cx, cy, r, rings, segs, color="sky"):
    """A ball built from flat facets, lit from the top left, so the polygons show."""
    lo, base, hi = PAL[color]
    L = (-.42, -.58, .7)
    ln = math.sqrt(sum(v * v for v in L))
    L = tuple(v / ln for v in L)
    out = cv.shadow(cx, cy + r + 8, r * .8, 4, .22)
    for k in range(rings):
        r0, r1 = r * k / rings, r * (k + 1) / rings
        for j in range(segs):
            a0, a1 = 2 * math.pi * j / segs, 2 * math.pi * (j + 1) / segs
            pts = [(cx + r0 * math.cos(a0), cy + r0 * math.sin(a0))] if k else [(cx, cy)]
            pts += [(cx + r1 * math.cos(a0), cy + r1 * math.sin(a0)), (cx + r1 * math.cos(a1), cy + r1 * math.sin(a1))]
            if k:
                pts += [(cx + r0 * math.cos(a1), cy + r0 * math.sin(a1))]
            am, rm = (a0 + a1) / 2, (r0 + r1) / 2
            nx, ny = rm * math.cos(am) / r, rm * math.sin(am) / r
            nz = math.sqrt(max(0, 1 - nx * nx - ny * ny))
            br = max(0, min(1, (nx * L[0] + ny * L[1] + nz * L[2]) * 1.05))
            out += cv.poly(pts, _mix(hi, lo, .08 + .92 * br), stroke=hi, sw=.9)
    return out


def smooth_ball(cv, cx, cy, r, color="sky"):
    """The same ball with so many polygons you stop seeing them."""
    lo, base, hi = PAL[color]
    out = cv.shadow(cx, cy + r + 8, r * .8, 4, .22)
    out += cv.circle(cx, cy, r, cv.rad("ball-" + color, [(0, lo), (.55, base), (1, hi)], .5, .5, .6, .36, .3))
    for k in (-.6, -.3, 0, .3, .6):
        rx = r * math.sqrt(1 - k * k)
        out += cv.ellipse(cx, cy + k * r, rx, rx * .16, "none", stroke=hi, sw=.7, op=.3)
    for deg in (0, 30, 60, 90, 120, 150):
        out += cv.ellipse(cx, cy, abs(r * math.cos(math.radians(deg))) + .01, r, "none", stroke=hi, sw=.7, op=.3)
    out += cv.ellipse(cx - r * .3, cy - r * .5, r * .3, r * .14, "#fff", op=.4)
    return out


def count_pill(cv, x, y, label, icon):
    size, pad = 14.5, 22
    w = len(label) * size * .58 + pad * 2 + 14
    out = P.pill(cv, x + 7, y, label, "paper", size, pad, 30, 800)
    ix = x + 7 - w / 2 + 19
    if icon == "dot":
        out += cv.circle(ix, y, 6.5, cv.g("sun"), stroke="#fff", sw=2) 
    elif icon == "line":
        out += cv.line(ix - 8, y + 6, ix + 8, y - 6, PAL["coral"][2], 4)
    else:
        out += cv.poly([(ix - 8, y + 6), (ix + 4, y + 6), (ix + 8, y - 6), (ix - 4, y - 6)], cv.g("teal"), stroke=PAL["teal"][2], sw=1.5)
    return out


@illustration("mesh")
def _mesh():
    cv = Canvas(800, 500).backdrop()
    cv.add(P.card(cv, 14, 34, 416, 448, 20, "A cube is a mesh", "teal"))
    s, ox, oy = 150, 66, 56
    x0, y0 = 96, 210
    F = [(x0, y0 + s), (x0 + s, y0 + s), (x0 + s, y0), (x0, y0)]
    B = [(px + ox, py - oy) for px, py in F]
    edge_c = "#1F3A44"
    cv.add(cv.shadow(x0 + s / 2 + 30, y0 + s + 14, 120, 8, .22))
    top = cv.lin("cube-top", [(0, "#E3F4FD"), (1, "#B5E0F8")], 0, 1, 1, 0)
    right = cv.lin("cube-right", [(0, "#4E9FD8"), (1, "#2F82C0")], 0, 0, 1, 1)
    cv.add(cv.poly([F[3], F[2], B[2], B[3]], top, stroke=edge_c, sw=3), cv.poly([F[1], B[1], B[2], F[2]], right, stroke=edge_c, sw=3),
           cv.poly(F, cv.g("sky"), stroke=edge_c, sw=3))
    cv.add(cv.poly([F[1], B[1], B[2], F[2]], "#25D3C8", op=.5))
    for p, q in ((B[0], B[1]), (B[0], B[3]), (F[0], B[0])):      # the three edges at the back, seen through
        cv.add(cv.line(p[0], p[1], q[0], q[1], edge_c, 2.5, op=.45, dash="6 6"))
    cv.add(cv.rect(F[3][0] + 10, F[3][1] + 10, 38, 14, 7, "#fff", op=.35))
    # the picked out edge, then every vertex
    cv.add(cv.line(F[0][0], F[0][1], F[3][0], F[3][1], "#F0584B", 8))
    for i, p in enumerate(F + B):
        if p == B[0]:
            cv.add(cv.circle(p[0], p[1], 6.5, "none", stroke=edge_c, sw=2, op=.5, dash="3 3"))
        else:
            cv.add(cv.circle(p[0], p[1], 8, "#FFFFFF"), cv.circle(p[0], p[1], 6, cv.g("sun")))
    # callouts
    cv.add(P.pill(cv, 384, 108, "vertex", "sun", 15, 12, 28, 800))
    cv.add(cv.line(364, 122, 320, 148, PAL["sun"][2], 2.5))
    cv.add(cv.text(384, 142, "a point:", 12.5, 650, cls="il-ink2"), cv.text(384, 158, "(x, y, z)", 12.5, 650, cls="il-ink2", mono=True))
    cv.add(P.pill(cv, 54, 285, "edge", "coral", 15, 12, 28, 800))
    cv.add(cv.text(54, 312, "joins two", 12.5, 650, cls="il-ink2"), cv.text(54, 328, "vertices", 12.5, 650, cls="il-ink2"))
    cv.add(P.pill(cv, 372, 262, "face", "teal", 15, 12, 28, 800))
    cv.add(cv.line(344, 262, 290, 260, PAL["teal"][2], 2.5))
    cv.add(cv.text(372, 288, "a flat", 12.5, 650, cls="il-ink2"), cv.text(372, 304, "surface", 12.5, 650, cls="il-ink2"))
    # axes: x across, y deep, z up
    ax, ay = 332, 396
    cv.add(P.arrow(cv, [(ax, ay), (ax + 46, ay)], ARROW, 3, 9), P.arrow(cv, [(ax, ay), (ax, ay - 44)], ARROW, 3, 9),
           P.arrow(cv, [(ax, ay), (ax + 30, ay - 25)], ARROW, 3, 9))
    cv.add(cv.text(ax + 58, ay + 5, "x", 14, 800, cls="il-ink", mono=True), cv.text(ax - 1, ay - 52, "z", 14, 800, cls="il-ink", mono=True),
           cv.text(ax + 42, ay - 28, "y", 14, 800, cls="il-ink", mono=True))
    cv.add(count_pill(cv, 92, 450, "8 vertices", "dot"), count_pill(cv, 225, 450, "12 edges", "line"), count_pill(cv, 347, 450, "6 faces", "face"))
    # polygons: more of them, more detail, more work
    cv.add(P.card(cv, 444, 34, 342, 448, 20, "How many polygons?", "coral"))
    specs = [("Low poly", "about 100 triangles", .2, .1), ("Medium", "about 2,000 triangles", .6, .45), ("High poly", "about 100,000 triangles", 1, 1)]
    for i, (name, sub, dd, ww) in enumerate(specs):
        yy = 128 + i * 124
        if i == 0:
            cv.add(facet_ball(cv, 502, yy, 42, 2, 8))
        elif i == 1:
            cv.add(facet_ball(cv, 502, yy, 42, 4, 14))
        else:
            cv.add(smooth_ball(cv, 502, yy, 42))
        cv.add(cv.text(560, yy - 26, name, 16, 800, anchor="start", cls="il-ink"), cv.text(560, yy - 8, sub, 12.5, 650, anchor="start", cls="il-ink2"))
        for j, (lab, v, col) in enumerate((("detail", dd, "teal"), ("work", ww, "coral"))):
            by = yy + 8 + j * 24
            cv.add(cv.text(560, by + 10, lab, 12, 650, anchor="start", cls="il-ink2"))
            cv.add(cv.rect(612, by, 150, 12, 6, "var(--il-line)"), cv.rect(612, by, 150 * v, 12, 6, cv.g(col)))
    cv.add(cv.text(615, 452, "Film: millions of polygons, hours per frame.", 12, 650, cls="il-ink2"), cv.text(615, 470, "Game: simpler meshes, 60 frames a second.", 12, 650, cls="il-ink2"))
    cv.add(P.badge(cv, 322, 108, 1), P.badge(cv, 54, 248, 2), P.badge(cv, 372, 224, 3), P.badge(cv, 30, 36, 4), P.badge(cv, 460, 36, 5))
    return figure(
        "mesh", cv, "Vertices, edges, faces and the mesh",
        "A cube, built from the parts a 3D model is actually made of. A vertex is a single point in three dimensional space, given by an x "
        "coordinate across, a y for depth and a z for height, and a cube has eight of them, one at each corner. An edge is a straight line "
        "joining two vertices, and a cube needs twelve. A face is a flat surface enclosed by edges, usually a triangle or a square, and a cube "
        "has six. Those three things together, every vertex, every edge and every face, are the mesh, and the mesh is the model. Beside the "
        "cube, three balls are built from more and more polygons: a low poly one of about a hundred triangles, which looks faceted and is "
        "cheap to draw, a medium one of about two thousand, and a high poly one of about a hundred thousand, which looks smooth and costs the "
        "most. The number of faces is the polygon count, and it is the central trade off in all 3D work: more polygons give finer detail and "
        "smoother curves, and also demand more processing power and more memory. A film can afford millions per character because each frame "
        "is rendered once over hours, while a game has to draw sixty frames every second and uses far simpler meshes with clever texturing to "
        "fake the detail that is missing.",
        ["A vertex is one point in space, with an x, a y and a z. A cube has 8.",
         "An edge is a straight line joining two vertices. A cube needs 12.",
         "A face is a flat surface enclosed by edges. A cube has 6.",
         "All of them together are the mesh, and that is the model.",
         "More polygons means more detail, and more work for the computer."],
        "Learn vertex, edge, face, mesh in that order and the rest of the unit has somewhere to attach.")
