"""A Level illustrations, set three: browser against server, two's complement, floating point,
concurrency, ACID, SQL, the programming project, levels of testing and test driven development."""
import math

from .illus import Canvas, PAL, INK, ARROW, figure, illustration, _n
from . import illus_props as P
from . import illus_glyphs as G
from .illus_bits import bit_row, outline


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


# ------------------------------------------------------------------ browser against server

@illustration("web-tech-split")
def _webs():
    cv = Canvas(800, 500).backdrop()
    cv.add(P.card(cv, 14, 30, 336, 264, 20, "In the browser: client side", "sky"), P.badge(cv, 36, 56, 1))
    cv.add(cv.rect(34, 70, 296, 150, 10, "#FFFFFF", stroke="#9FB3BE", sw=1.5), cv.rect(34, 70, 296, 22, 10, "#DCE8EE"), cv.rect(34, 82, 296, 10, 0, "#DCE8EE"))
    for i, c in enumerate(("#FF7B72", "#FFCB47", "#5BD58B")):
        cv.add(cv.circle(48 + i * 12, 81, 3.6, c))
    for i, (t, sub, col) in enumerate((("HTML", "structure", "coral"), ("CSS", "style", "sky"), ("JavaScript", "behaviour", "sun"))):
        x = 44 + i * 96
        cv.add(P.lift(cv, x, 108, 88, 62, col, 10, 4, hl=False), cv.text(x + 44, 135, t, 13.5, 800, fill=INK, mono=True), cv.text(x + 44, 155, sub, 12, 650, fill=INK))
    cv.add(cv.rect(44, 184, 276, 24, 8, "#F1F5F8", stroke="#B9C6CE", sw=1.2), cv.text(54, 201, "Email: sam@", 12.5, 700, anchor="start", fill=INK, mono=True), cv.text(300, 201, "typed so far", 11.5, 650, anchor="end", fill="#4A6470"))
    for j, ln in enumerate(("runs on the user's device", "feedback at once: no trip to the server")):
        cv.add(cv.text(182, 242 + j * 20, ln, 13, 700, cls="il-ink"))
    cv.add(P.card(cv, 450, 30, 336, 264, 20, "On the server: server side", "coral"), P.badge(cv, 472, 56, 2))
    cv.add(P.server_rack(cv, 480, 76, 2, .95), G.cylinder(cv, 690, 130, 70, 78, "sky", 3))
    cv.add(cv.text(690, 196, "database", 12.5, 700, cls="il-ink2"))
    cv.add(cv.text(560, 218, "Python or PHP", 12.5, 750, cls="il-ink", mono=True))
    cv.add(P.arrow(cv, [(626, 122), (648, 122)], ARROW, 3, 8), P.arrow(cv, [(648, 140), (626, 140)], ARROW, 3, 8))
    for j, ln in enumerate(("runs on the company's machine", "private code, shared data, secure checks")):
        cv.add(cv.text(618, 242 + j * 20, ln, 13, 700, cls="il-ink"))
    cv.add(P.pill(cv, 400, 120, "request", "paper", 13, 12, 26, 750), P.arrow(cv, [(356, 140), (444, 140)], PAL["teal"][2], 4, 11))
    cv.add(P.arrow(cv, [(444, 182), (356, 182)], PAL["coral"][2], 4, 11), P.pill(cv, 400, 202, "response", "paper", 13, 12, 26, 750))
    # the comparison
    cv.add(P.card(cv, 14, 316, 772, 166, 20), P.pill(cv, 450, 338, "Client side", "sky", 14.5, 16, 28, 800), P.pill(cv, 650, 338, "Server side", "coral", 14.5, 16, 28, 800), P.badge(cv, 36, 322, 3))
    rows = [("The user can", "see and change it", "not see it"), ("Good for", "instant checks and animation", "passwords and shared data"), ("Never trust it for", "security", "speed of feedback")]
    for i, (lab, a_, b_) in enumerate(rows):
        y = 362 + i * 38
        if i % 2 == 0:
            cv.add(cv.rect(26, y, 748, 34, 8, "var(--il-band)"))
        cv.add(cv.text(42, y + 23, lab, 14, 750, anchor="start", cls="il-ink"), cv.text(450, y + 23, a_, 13.5, 650, cls="il-ink"), cv.text(650, y + 23, b_, 13.5, 650, cls="il-ink"))
    return figure(
        "web-tech-split", cv, "Client side processing in the browser against server side processing on the server",
        "Web applications split their work between two places. On the client side, in the browser, HTML gives the structure, CSS the style and "
        "JavaScript the behaviour. It runs on the user's own device, so feedback is at once with no trip to the server, for example checking an "
        "email address as it is typed. On the server side, code in a language such as Python or PHP runs on the company's machine and talks to "
        "the database. Its code stays private, it shares data between users and it does the secure checks. The browser sends a request and the "
        "server sends back a response. Client side code can be seen and changed by the user, so it should never be trusted for security, while "
        "server side code cannot be seen.",
        ["Client side code runs in the browser: HTML for structure, CSS for style, JavaScript for behaviour. It gives instant feedback.",
         "Server side code runs on the server and uses the database. The user cannot see it, so it does the secure checks.",
         "The user can see and change client side code, so never trust it for security."],
        "Validate on the client for a better experience, and validate again on the server for security.")


# ------------------------------------------------------------------ two's complement

@illustration("twos-complement")
def _twos():
    cv = Canvas(800, 500).backdrop()
    cv.add(P.card(cv, 14, 30, 772, 196, 20, "Eight bits, with the left bit worth -128", "teal"), P.badge(cv, 36, 56, 1))
    weights = [-128, 64, 32, 16, 8, 4, 2, 1]
    row, xs, _ = bit_row(cv, 64, 124, "1111 1011", cw=70, ch=50, gap=8, nib=22, size=24, ones="sky", override={0: "coral"})
    cv.add(row)
    for i, wgt in enumerate(weights):
        cv.add(cv.text(xs[i] + 35, 110, str(wgt), 15, 800, cls="il-ink", mono=True))
    cv.add(outline(cv, xs[0], 124, 70, 50, "#BA352D", 9, 3))
    cv.add(cv.text(400, 208, "-128 + 64 + 32 + 16 + 8 + 2 + 1  =  -5", 17, 800, cls="il-ink", mono=True))
    # finding the negative
    cv.add(P.card(cv, 14, 246, 520, 236, 20, "Finding -5 from +5", "coral"), P.badge(cv, 36, 272, 2))
    steps = [("Write +5", "0000 0101", "sky"), ("Flip every bit", "1111 1010", "sun"), ("Add 1", "1111 1011", "mint")]
    for i, (lab, bits, col) in enumerate(steps):
        y = 296 + i * 60
        cv.add(cv.text(36, y + 26, lab, 14.5, 800, anchor="start", cls="il-ink"))
        r, _, _ = bit_row(cv, 196, y + 4, bits, cw=30, ch=34, gap=4, nib=12, size=17, ones=col)
        cv.add(r)
        if i < 2:
            cv.add(P.arrow(cv, [(368, y + 38), (368, y + 56)], ARROW, 3, 8))
    # the range
    cv.add(P.card(cv, 550, 246, 236, 236, 20, "The range", "sun"), P.badge(cv, 572, 272, 3))
    cv.add(cv.line(574, 370, 764, 370, ARROW, 3), cv.circle(574, 370, 5, ARROW), cv.circle(764, 370, 5, ARROW), cv.circle(669, 370, 6, "#BA352D"))
    cv.add(cv.text(574, 396, "-128", 14, 800, anchor="start", cls="il-ink", mono=True), cv.text(669, 396, "0", 14, 800, cls="il-ink", mono=True), cv.text(764, 396, "127", 14, 800, anchor="end", cls="il-ink", mono=True))
    cv.add(cv.text(668, 326, "8 bits give", 14, 750, cls="il-ink"), cv.text(668, 348, "256 values", 17, 800, cls="il-ink"))
    cv.add(cv.text(668, 432, "one more negative than", 12.5, 650, cls="il-ink2"), cv.text(668, 450, "positive: there is no +128", 12.5, 650, cls="il-ink2"))
    return figure(
        "twos-complement", cv, "Two's complement: the left bit is worth minus 128, and how to find -5 from +5",
        "Two's complement stores negative numbers in binary. In eight bits the place values are minus 128, 64, 32, 16, 8, 4, 2 and 1, so the "
        "leftmost bit is worth minus 128 instead of plus 128. The bits 1111 1011 are minus 128 plus 64 plus 32 plus 16 plus 8 plus 2 plus 1, which "
        "is minus 5. To find minus 5 from plus 5, write 5 as 0000 0101, flip every bit to get 1111 1010, then add 1 to get 1111 1011. Eight bits "
        "give 256 values from minus 128 to plus 127, one more negative number than positive because there is no plus 128.",
        ["The leftmost bit has a negative place value, -128. Add up the columns that hold a 1.",
         "To negate a number: write it in binary, flip every bit, then add 1.", "Eight bits hold -128 to 127. There is one more negative number than positive."],
        "The left bit is the sign bit: 1 means negative. Check an answer by adding the column values back up.")


# ------------------------------------------------------------------ floating point

@illustration("floating-point")
def _float():
    cv = Canvas(800, 500).backdrop()
    cv.add(P.card(cv, 14, 30, 772, 214, 20, "A number stored as a mantissa and an exponent", "teal"), P.badge(cv, 36, 56, 1))
    mant, xs, _ = bit_row(cv, 54, 112, "01101000", cw=44, ch=46, gap=6, nib=6, size=22, ones=["sky"])
    cv.add(mant)
    cv.add(cv.line(xs[0] + 44 + 3, 100, xs[0] + 44 + 3, 172, "#BA352D", 3.4, dash="4 4"), cv.text(xs[0] + 47, 92, "binary point", 12.5, 750, anchor="start", cls="il-bad"))
    cv.add(cv.text(54 + 8 * 50 / 2 - 4, 202, "mantissa  0.1101000  =  0.8125", 15, 800, cls="il-ink", mono=True))
    cv.add(cv.text(520, 134, "x", 26, 800, cls="il-ink"))
    cv.add(cv.text(560, 134, "2", 26, 800, cls="il-ink", mono=True))
    ex, _, _ = bit_row(cv, 590, 112, "0011", cw=44, ch=46, gap=6, nib=6, size=22, ones=["sun"])
    cv.add(ex)
    cv.add(cv.text(688, 202, "exponent  0011  =  3", 15, 800, cls="il-ink", mono=True))
    cv.add(cv.text(664, 100, "the power of 2", 12.5, 650, cls="il-ink2"))
    # moving the point
    cv.add(P.card(cv, 14, 264, 772, 140, 20, "The exponent moves the binary point", "coral"), P.badge(cv, 36, 290, 2))
    cv.add(cv.text(46, 336, "0.1101000", 26, 800, anchor="start", cls="il-ink", mono=True))
    cv.add(P.arrow(cv, [(300, 330), (400, 330)], PAL["coral"][2], 5, 13), cv.text(350, 318, "3 places right", 13, 750, cls="il-ink"))
    cv.add(cv.text(420, 336, "110.1000", 26, 800, anchor="start", cls="il-ink", mono=True), cv.text(640, 336, "= 6.5", 26, 800, anchor="start", cls="il-ink", mono=True))
    cv.add(cv.text(46, 376, "110.1000 = 4 + 2 + 0.5 = 6.5, and 0.8125 x 2^3 = 6.5 as well", 14, 700, anchor="start", cls="il-ink2", mono=True))
    # the trade off and normalising
    cv.add(P.card(cv, 14, 424, 772, 62, 16))
    cv.add(P.badge(cv, 36, 455, 3), cv.text(64, 450, "Normalised: the first two mantissa bits differ (01 or 10), so no accuracy is wasted on leading zeros.", 13.5, 750, anchor="start", cls="il-ink"))
    cv.add(cv.text(64, 471, "More mantissa bits give more precision. More exponent bits give a bigger range.", 13, 650, anchor="start", cls="il-ink2"))
    return figure(
        "floating-point", cv, "6.5 stored in floating point as the mantissa 01101000 and the exponent 0011",
        "A floating point number has two parts. The mantissa, here 01101000, is read with the binary point after the first bit, which gives "
        "0.1101000, or 0.8125. The exponent, here 0011, is 3. The value is the mantissa times 2 to the power of the exponent. The exponent moves "
        "the binary point three places to the right, turning 0.1101000 into 110.1000, which is 4 plus 2 plus 0.5, which is 6.5. A mantissa is "
        "normalised when its first two bits differ, 01 for a positive number or 10 for a negative one, so no accuracy is wasted on leading "
        "zeros. More mantissa bits give more precision, and more exponent bits give a bigger range.",
        ["Mantissa times two to the power of the exponent. The binary point sits after the first mantissa bit.",
         "The exponent moves the point: 0.1101000 moved 3 places right is 110.1000, which is 6.5.",
         "Normalise so the first two bits differ. More mantissa bits give precision, more exponent bits give range."],
        "Floating point trades precision against range, and most decimals cannot be stored exactly.")


# ------------------------------------------------------------------ thinking concurrently

JOB = {"A": ("Load", "coral"), "B": ("Clean 1", "sky"), "C": ("Clean 2", "mint"), "D": ("Merge", "sun")}


def tblock(cv, x, y, w, k, h=34):
    size = 12.5 if w >= 60 else 11
    return P.lift(cv, x, y, w, h, JOB[k][1], 8, 4, hl=False) + cv.text(x + w / 2, y + h / 2 + 4.8, JOB[k][0], size, 800, fill=INK)


@illustration("concurrency")
def _conc():
    cv = Canvas(800, 500).backdrop()
    cv.add(P.card(cv, 14, 30, 300, 280, 20, "What depends on what", "sky"), P.badge(cv, 36, 56, 1))
    nodes = {"A": (164, 92), "B": (84, 180), "C": (244, 180), "D": (164, 268)}
    for a_, b_ in (("A", "B"), ("A", "C"), ("B", "D"), ("C", "D")):
        cv.add(P.arrow(cv, [(nodes[a_][0], nodes[a_][1] + 20), (nodes[b_][0], nodes[b_][1] - 22)], ARROW, 2.6, 9))
    for k, (nx, ny) in nodes.items():
        cv.add(tblock(cv, nx - 44, ny - 17, 88, k))
    cv.add(P.card(cv, 330, 30, 456, 280, 20, "Time taken", "coral"), P.badge(cv, 352, 56, 2))
    u, x0 = 36, 394
    for r, (title, segs, total, y) in enumerate((("one at a time", [("A", 0, 3, 0), ("B", 3, 2, 0), ("C", 5, 2, 0), ("D", 7, 1, 0)], 8, 100),
                                                 ("concurrently", [("A", 0, 3, 0), ("B", 3, 2, 0), ("C", 3, 2, 1), ("D", 5, 1, 0)], 6, 200))):
        cv.add(cv.text(x0 - 16, y - 10, title, 14.5, 800, anchor="start", cls="il-ink"))
        lanes = 2 if r else 1
        for k, st, ln, lane in segs:
            cv.add(tblock(cv, x0 + st * u + 1, y + lane * 40, ln * u - 2, k))
        cv.add(cv.line(x0, y + lanes * 40 + 8, x0 + 8 * u, y + lanes * 40 + 8, "#8AA0AC", 2))
        for t in range(0, total + 1):
            cv.add(cv.line(x0 + t * u, y + lanes * 40 + 4, x0 + t * u, y + lanes * 40 + 12, "#8AA0AC", 1.6))
        cv.add(P.pill(cv, x0 + total * u + 56, y + 16 + (20 if r else 0), "%d units" % total, "sun" if r else "paper", 14, 12, 26, 800))
    cv.add(P.card(cv, 14, 332, 772, 150, 20, "Using concurrency", "mint"), P.badge(cv, 36, 358, 3))
    for i, (ok, a_, b_) in enumerate(((True, "Find independent tasks", "they can run side by side, on different cores or machines"),
                                       (False, "The cost", "coordinating the tasks and sharing their data"),
                                       (False, "The limit", "the longest chain of dependent tasks sets the minimum time"))):
        y = 394 + i * 30
        cv.add(P.tick(cv, 44, y, 10) if ok else cv.circle(44, y, 5, cv.g("teal", "deep")))
        cv.add(cv.text(64, y + 5, a_ + ":", 13.5, 800, anchor="start", cls="il-ink"), cv.text(64 + len(a_) * 7.2 + 14, y + 5, b_, 13, 650, anchor="start", cls="il-ink2"))
    return figure(
        "concurrency", cv, "Four tasks with dependencies, taking 8 units one at a time and 6 units concurrently",
        "Thinking concurrently means finding the parts of a problem that can happen at the same time. Four tasks are shown. Load comes first. "
        "Clean 1 and Clean 2 both depend on Load but not on each other. Merge needs both of them. Done one at a time they take 3 plus 2 plus 2 "
        "plus 1, which is 8 units. Done concurrently, Clean 1 and Clean 2 run side by side on two lanes, so the total is 3 plus 2 plus 1, which "
        "is 6 units. Tasks that do not depend on each other can run on different cores or machines, but the cost is coordinating them and "
        "sharing their data, and the longest chain of dependent tasks sets the shortest possible time.",
        ["A dependency graph: Load first, then two cleaning tasks that do not depend on each other, then Merge.",
         "One at a time is 8 units. Running the two cleaning tasks side by side is 6 units.",
         "Concurrency needs independent tasks and brings coordination costs. The longest dependent chain limits the saving."],
        "Concurrency speeds things up only where tasks are independent. The longest chain of dependencies sets the minimum time.")
