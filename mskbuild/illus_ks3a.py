"""Key Stage 3 illustrations: block coding, files and folders, spreadsheets and charts."""
import math

from .illus import Canvas, PAL, INK, ARROW, figure, illustration, _n
from . import illus_props as P
from . import illus_glyphs as G


# ------------------------------------------------------------------ block coding

# fill, text colour, the darker edge under it
BLK = {"event": ("#FFC93C", INK, "#D9A000"), "motion": ("#2F6FD6", "#FFFFFF", "#1F4FA0"), "looks": ("#7B4FD0", "#FFFFFF", "#5A36A0"),
       "control": ("#F29B1D", INK, "#C47800"), "sensing": ("#78D4E8", INK, "#3FA9C4")}
ARM = 18


def parts_markup(cv, x, y, h, parts, tc):
    out, tx = "", x + 12
    for part in parts:
        if isinstance(part, tuple):
            t = part[1]
            pw = len(t) * 8.4 + 14
            out += cv.rect(tx, y + h / 2 - 11, pw, 22, 11, "#FFFFFF") + cv.text(tx + pw / 2, y + h / 2 + 5, t, 13, 800, fill=INK)
            tx += pw + 6
        else:
            out += cv.text(tx, y + h / 2 + 5, part, 13.5, 750, anchor="start", fill=tc)
            tx += len(part) * 7.4 + 9
    return out


def block(cv, x, y, w, kind, parts, h=30):
    fill, tc, edge = BLK[kind]
    out = cv.rect(x, y + 3, w, h, 7, edge) + cv.rect(x, y, w, h, 7, fill)
    out += cv.rect(x + 14, y + h - 2, 30, 7, 3, fill) + cv.rect(x + 4, y + 3, w - 8, 5, 2.5, "#FFFFFF", op=.22)
    return out + parts_markup(cv, x, y, h, parts, tc)


def hat(cv, x, y, w, parts):
    fill, tc, edge = BLK["event"]
    d = "M%s %s L%s %s C%s %s %s %s %s %s L%s %s Q%s %s %s %s L%s %s Z"
    shape = lambda dy: d % (x, y + 34 + dy, x, y + 18 + dy, x + 16, y - 6 + dy, x + 70, y - 6 + dy, x + 88, y + 12 + dy, x + w - 7, y + 12 + dy, x + w, y + 12 + dy, x + w, y + 19 + dy, x + w, y + 34 + dy)
    out = cv.path(shape(3), fill=edge) + cv.path(shape(0), fill=fill) + cv.rect(x + 14, y + 32, 30, 7, 3, fill)
    return out + parts_markup(cv, x, y + 10, 30, parts, tc)


def cstack(cv, x, y, w, kind, segs):
    """A block with a mouth, such as if or repeat. segs: ("bar", parts, h) or ("arm", h). Returns (markup, height)."""
    fill, tc, edge = BLK[kind]
    under, face, text, cy = "", "", "", y
    for seg in segs:
        if seg[0] == "bar":
            _, parts, h = seg
            under += cv.rect(x, cy + 3, w, h, 7, edge)
            face += cv.rect(x, cy, w, h, 7, fill)
            text += parts_markup(cv, x, cy, h, parts, tc)
            cy += h - 4
        else:
            h = seg[1]
            under += cv.rect(x, cy + 3, ARM, h + 8, 0, edge)
            face += cv.rect(x, cy, ARM, h + 8, 0, fill)
            cy += h
    return under + face + text, cy - y + 4


def stage(cv, x, y, w, h):
    return cv.rect(x, y, w, h, 10, "#FFFFFF", stroke="#B9C6CE", sw=1.6)


@illustration("scratch-blocks")
def _scratch():
    cv = Canvas(800, 500).backdrop()
    titles = (("Sequence", "sky"), ("Selection", "coral"), ("Iteration", "mint"))
    for n, (title, col) in enumerate(titles):
        x = (14, 277, 540)[n]
        cv.add(P.card(cv, x, 28, 246, 448, 20, title, col))
        cv.add(P.badge(cv, x + 22, 56, n + 1))
        bx, bw = x + 20, 206
        if n == 0:
            cv.add(hat(cv, bx, 66, bw, ["when flag clicked"]))
            cv.add(block(cv, bx, 100, bw, "motion", ["move", ("in", "80"), "steps"]))
            cv.add(block(cv, bx, 130, bw, "motion", ["turn right", ("in", "90"), "degrees"]))
            cv.add(block(cv, bx, 160, bw, "motion", ["move", ("in", "80"), "steps"]))
            cv.add(block(cv, bx, 190, bw, "looks", ["say", ("in", "Hello!")]))
            sx, sy = x + 16, 250
            cv.add(stage(cv, sx, sy, 214, 132))
            cv.add(cv.path("M%s %s L%s %s L%s %s" % (sx + 36, sy + 38, sx + 120, sy + 38, sx + 120, sy + 100), stroke="#2F6FD6", sw=3, dash="2 7"))
            cv.add(cv.circle(sx + 36, sy + 38, 5, "#2F6FD6"))
            cv.add(P.pixel_cat(cv, sx + 100, sy + 84, 40))
            cv.add(G.bubble(cv, sx + 140, sy + 64, 62, 28, ["Hello!"], tail=(-20, 20), size=13))
            cv.add(cv.text(x + 123, 410, "one block after another,", 13.5, 700, cls="il-ink"), cv.text(x + 123, 430, "in the order they are stacked", 13.5, 700, cls="il-ink"))
        elif n == 1:
            cv.add(hat(cv, bx, 66, bw, ["when flag clicked"]))
            mk, hh = cstack(cv, bx, 100, bw, "control", [("bar", ["if", ("in", "touching edge?"), "then"], 34), ("arm", 30), ("bar", ["else"], 26), ("arm", 30), ("bar", [""], 20)])
            cv.add(mk)
            cv.add(block(cv, bx + ARM, 130, bw - ARM, "motion", ["turn", ("in", "180"), "degrees"], 28))
            cv.add(block(cv, bx + ARM, 184, bw - ARM, "motion", ["move", ("in", "10"), "steps"], 28))
            sx, sy = x + 16, 250
            cv.add(stage(cv, sx, sy, 214, 132))
            cv.add(cv.rect(sx + 200, sy + 8, 8, 116, 3, "#BA352D"))
            cv.add(P.pixel_cat(cv, sx + 142, sy + 46, 40))
            cv.add(P.arrow(cv, [(sx + 24, sy + 100), (sx + 130, sy + 100)], "#2F6FD6", 3.5, 10, dash="2 7"))
            cv.add(cv.text(x + 123, 410, "the condition picks one path.", 13.5, 700, cls="il-ink"), cv.text(x + 123, 430, "only one of them runs", 13.5, 700, cls="il-ink"))
        else:
            cv.add(hat(cv, bx, 66, bw, ["when flag clicked"]))
            mk, hh = cstack(cv, bx, 100, bw, "control", [("bar", ["repeat", ("in", "4")], 34), ("arm", 56), ("bar", [""], 20)])
            cv.add(mk)
            cv.add(block(cv, bx + ARM, 130, bw - ARM, "motion", ["move", ("in", "80"), "steps"], 28))
            cv.add(block(cv, bx + ARM, 158, bw - ARM, "motion", ["turn right", ("in", "90")], 28))
            sx, sy = x + 16, 250
            cv.add(stage(cv, sx, sy, 214, 132))
            cv.add(cv.path("M%s %s L%s %s L%s %s L%s %s Z" % (sx + 60, sy + 30, sx + 150, sy + 30, sx + 150, sy + 108, sx + 60, sy + 108), stroke="#2F6FD6", sw=3.5))
            for k, (px, py) in enumerate(((105, 30), (150, 69), (105, 108), (60, 69))):
                cv.add(cv.circle(sx + px, sy + py, 9, "#FFFFFF", stroke="#2F6FD6", sw=2), cv.text(sx + px, sy + py + 4.5, str(k + 1), 12.5, 800, fill=INK))
            cv.add(P.pixel_cat(cv, sx + 38, sy + 8, 36))
            cv.add(cv.text(x + 123, 410, "repeat does the same steps", 13.5, 700, cls="il-ink"), cv.text(x + 123, 430, "again: four sides, four times", 13.5, 700, cls="il-ink"))
    cv.add(P.pill(cv, 400, 484, "An event, such as the green flag being clicked, starts every script.", "paper", 13.5, 14, 24, 700))
    return figure(
        "scratch-blocks", cv, "Three block scripts: a sequence, a selection and a repeat loop, each with what it does on the stage",
        "Three scripts built from coloured blocks, each starting with a yellow when flag clicked block, which is an event. Sequence: the blocks "
        "run from top to bottom, move 80 steps, turn right 90 degrees, move 80 steps, say Hello, and the sprite walks right, turns and "
        "walks down. Selection: an if else block chooses one path from a condition. If touching edge then turn 180 degrees, else move 10 "
        "steps, and only one of the two paths runs. Iteration: a repeat 4 block runs the blocks inside it four times, move 80 steps and turn "
        "right 90 degrees, which draws a square with four equal sides.",
        ["Sequence: the blocks run one after another from the top, in the order they are stacked.",
         "Selection: the if block asks a question and picks one of two paths. Only one path runs.",
         "Iteration: repeat runs the blocks inside it again and again. Four sides, four identical steps, so repeat 4."],
        "Every program is built from these three ideas: sequence, selection and iteration.")


# ------------------------------------------------------------------ files and folders

EXT = {"docx": ("sky", "document"), "xlsx": ("mint", "spreadsheet"), "jpg": ("sun", "image"), "mp3": ("coral", "sound"),
       "mp4": ("plum", "video"), "py": ("teal", "Python program"), "txt": ("slate", "plain text"), "pdf": ("red", "portable doc")}


def ext_tag(cv, x, y, ext, w=54, h=22):
    col = EXT[ext][0]
    tc = "#FFFFFF" if col in ("red", "plum") else INK
    return P.lift(cv, x, y, w, h, col, 6, 3, hl=False) + cv.text(x + w / 2, y + h / 2 + 4.5, "." + ext, 12.5, 800, fill=tc, mono=True)


@illustration("files-folders")
def _files():
    cv = Canvas(800, 500).backdrop()
    cv.add(P.card(cv, 14, 34, 420, 448, 20, "Folders keep files in order", "teal"))
    cv.add(cv.rect(30, 62, 388, 30, 15, "var(--il-band)"))
    for i, t in enumerate(("School", "Year 7", "Computing")):
        cv.add(cv.text(46 + i * 96, 82, t, 13.5, 750, anchor="start", cls="il-ink"))
        if i < 2:
            cv.add(cv.text(124 + i * 96, 82, "›", 16, 800, cls="il-ink2"))
    tree = [(0, "folder", "School"), (1, "folder", "Year 7"), (2, "folder", "Computing"), (3, "file", "networks-homework", "docx"), (3, "file", "python-lesson-3", "py"),
            (2, "folder", "Maths"), (3, "file", "fractions-quiz", "xlsx"), (1, "folder", "Photos"), (2, "file", "museum-trip", "jpg")]
    for i, row in enumerate(tree):
        lvl, kind, name = row[0], row[1], row[2]
        y = 112 + i * 40
        x = 40 + lvl * 28
        if lvl:
            cv.add(cv.path("M%s %s L%s %s L%s %s" % (x - 14, y - 10, x - 14, y + 12, x - 2, y + 12), stroke="#8AA0AC", sw=1.6))
        if kind == "folder":
            cv.add(P.folder(cv, x, y - 2, .36, "sun"))
            cv.add(cv.text(x + 40, y + 16, name, 14.5, 750, anchor="start", cls="il-ink"))
        else:
            cv.add(P.doc(cv, x + 4, y - 4, .3, 62, 80, 0, "paper"))
            cv.add(cv.text(x + 30, y + 16, name, 13.5, 650, anchor="start", cls="il-ink", mono=True))
            cv.add(ext_tag(cv, x + 30 + len(name) * 8.1 + 6, y + 0, row[3], 54, 22))
    # names
    cv.add(P.card(cv, 450, 34, 336, 214, 20, "Good and bad file names", "coral"))
    bad, good = ["doc1.docx", "final_FINAL2 (copy).docx", "new picture.jpg"], ["year7-homework-networks.docx", "2026-10-museum-trip.jpg"]
    for i, t in enumerate(bad):
        cv.add(P.cross(cv, 478, 80 + i * 28, 10), cv.text(498, 85 + i * 28, t, 13.5, 650, anchor="start", cls="il-ink", mono=True))
    cv.add(cv.line(466, 154, 770, 154, "var(--il-line)", 1.4, dash="4 5"))
    cv.add(cv.text(468, 174, "say what it is:", 12.5, 700, anchor="start", cls="il-ink2"))
    for i, t in enumerate(good):
        cv.add(P.tick(cv, 478, 194 + i * 28, 10), cv.text(498, 199 + i * 28, t, 12.5, 700, anchor="start", cls="il-ink", mono=True))
    # extensions
    cv.add(P.card(cv, 450, 270, 336, 212, 20, "File extensions", "sun"))
    for i, ext in enumerate(EXT):
        col, row = i % 2, i // 2
        x, y = 470 + col * 152, 312 + row * 42
        cv.add(ext_tag(cv, x, y, ext, 50, 24), cv.text(x + 58, y + 17, EXT[ext][1], 12.5, 700, anchor="start", cls="il-ink"))
    cv.add(P.badge(cv, 36, 60, 1), P.badge(cv, 472, 58, 2), P.badge(cv, 468, 276, 3))
    return figure(
        "files-folders", cv, "A folder tree, good and bad file names, and what the file extensions mean",
        "How to keep files in order. Folders are nested inside folders, for example School, then Year 7, then Computing, which holds the files "
        "networks-homework.docx and python-lesson-3.py, with Maths holding fractions-quiz.xlsx and Photos holding museum-trip.jpg. File names "
        "should say what the file is. Doc1.docx, final_FINAL2 copy.docx and new picture.jpg are bad names. Year7-homework-networks.docx and "
        "2026-10-museum-trip.jpg are good ones. The extension after the dot tells the computer which program opens the file: .docx is a "
        "document, .xlsx a spreadsheet, .jpg an image, .mp3 sound, .mp4 video, .py a Python program, .txt plain text and .pdf a portable document.",
        ["Folders inside folders make a tree. The path shows where a file lives.",
         "A good file name says what the file is, so it can be found later.", "The extension tells the computer which program to open the file with, so keep it."],
        "A good system takes seconds to set up and saves hours later.")


# ------------------------------------------------------------------ spreadsheets

@illustration("spreadsheet-anatomy")
def _sheet():
    cv = Canvas(800, 500).backdrop()
    gx, gy, cw, rh = 56, 138, 108, 40
    cv.add(cv.shadow(250, 442, 220, 8, .18))
    cv.add(cv.rect(14, 28, 500, 410, 14, "#FFFFFF", stroke="#B9C6CE", sw=1.6))
    cv.add(cv.rect(14, 28, 500, 34, 14, cv.g("mint")), cv.rect(14, 46, 500, 16, 0, cv.g("mint")))
    cv.add(cv.text(30, 51, "budget.xlsx", 13.5, 750, anchor="start", fill=INK, mono=True))
    # the formula bar
    cv.add(cv.rect(26, 72, 62, 30, 6, "#F1F5F8", stroke="#B9C6CE", sw=1.2), cv.text(57, 92, "B6", 14, 800, fill=INK, mono=True))
    cv.add(cv.text(104, 93, "fx", 15, 800, anchor="start", fill="#1F5F9A"))
    cv.add(cv.rect(130, 72, 372, 30, 6, "#FFFFFF", stroke="#B9C6CE", sw=1.2), cv.text(142, 92, "=SUM(B2:B5)", 15, 800, anchor="start", fill=INK, mono=True))
    # the grid
    cols = "ABC"
    for c in range(3):
        cv.add(cv.rect(gx + c * cw, gy - 26, cw, 26, 0, "#DDE6EC", stroke="#B9C6CE", sw=1), cv.text(gx + c * cw + cw / 2, gy - 8, cols[c], 14, 800, fill=INK))
    data = [("Pens", "12"), ("Books", "45"), ("Bag", "38"), ("Lunch", "45"), ("Total", "140")]
    for r in range(6):
        cv.add(cv.rect(gx - 30, gy + r * rh, 30, rh, 0, "#DDE6EC", stroke="#B9C6CE", sw=1), cv.text(gx - 15, gy + r * rh + 25, str(r + 1), 13.5, 800, fill=INK, mono=True))
        for c in range(3):
            cv.add(cv.rect(gx + c * cw, gy + r * rh, cw, rh, 0, "#FFFFFF", stroke="#D5DEE4", sw=1))
    cv.add(cv.text(gx + 14, gy + 26, "Item", 14, 800, anchor="start", fill=INK), cv.text(gx + cw + cw - 14, gy + 26, "Cost", 14, 800, anchor="end", fill=INK))
    for i, (a_, b_) in enumerate(data):
        yy = gy + (i + 1) * rh + 26
        cv.add(cv.text(gx + 14, yy, a_, 14, 700 if a_ == "Total" else 600, anchor="start", fill=INK), cv.text(gx + cw + cw - 14, yy, b_, 14, 800 if a_ == "Total" else 600, anchor="end", fill=INK, mono=True))
    cv.add(cv.rect(gx + cw, gy + rh, cw, 4 * rh, 0, "#25B3BB", op=.14), cv.rect(gx + cw, gy + rh, cw, 4 * rh, 0, "none", stroke="#0F7C84", sw=2.4, dash="6 4"))
    cv.add(cv.rect(gx + cw, gy + 5 * rh, cw, rh, 0, "none", stroke="#1F5F9A", sw=3.2))
    cv.add(P.badge(cv, 22, 86, 1), P.badge(cv, gx + 2 * cw + 20, gy + 5 * rh + 20, 2), P.badge(cv, gx + 2 * cw + 20, gy + 2 * rh + 20, 3))
    # reading the formula
    cv.add(P.card(cv, 534, 28, 252, 410, 20, "Reading a formula", "teal"))
    bits = [("=", "starts every formula", "sun", "="), ("SUM", "the function: add up", "coral", "SUM"), ("B2:B5", "the range: B2 down to B5", "mint", "B2:B5")]
    for i, (code, what, col, _) in enumerate(bits):
        y = 82 + i * 82
        w = 24 + len(code) * 15
        cv.add(P.lift(cv, 556, y, w, 38, col, 9, 5, hl=False), cv.text(556 + w / 2, y + 26, code, 20, 800, fill=INK, mono=True))
        cv.add(cv.text(556, y + 66, what, 13.5, 700, anchor="start", cls="il-ink"))
    cv.add(cv.line(552, 326, 770, 326, "var(--il-line)", 1.4, dash="4 5"))
    cv.add(cv.text(556, 354, "Use cell references, not numbers:", 13, 700, anchor="start", cls="il-ink2"))
    cv.add(P.cross(cv, 566, 378, 9), cv.text(584, 383, "=45*0.2", 14.5, 800, anchor="start", cls="il-ink", mono=True), P.tick(cv, 566, 408, 9), cv.text(584, 413, "=B3*0.2", 14.5, 800, anchor="start", cls="il-ink", mono=True))
    cv.add(P.pill(cv, 400, 466, "Change a number and every formula that uses it updates by itself.", "paper", 14, 16, 28, 700))
    return figure(
        "spreadsheet-anatomy", cv, "A spreadsheet with a SUM formula, and how to read the formula",
        "A small spreadsheet called budget.xlsx. Columns are lettered A, B and C and rows are numbered. Column A holds items, Pens, Books, Bag and "
        "Lunch, and column B holds their costs, 12, 45, 38 and 45. The selected cell is B6, shown in the cell box, and its formula appears in the "
        "formula bar: equals SUM of B2 to B5, which gives 140. The range B2 to B5, outlined with dashes, is what is added up. On the right the "
        "formula is read in three parts: the equals sign starts every formula, SUM is the function that adds up, and B2:B5 is the range, from B2 "
        "down to B5. A formula should use cell references, such as equals B3 times 0.2, instead of typing the number, such as equals 45 times "
        "0.2, so that it updates when the data changes.",
        ["The formula bar shows what is in the selected cell. Every formula starts with an equals sign.",
         "A cell is named by its column letter and row number, so this is cell B6.", "The range B2:B5 is a block of cells, from B2 down to B5. SUM adds them up."],
        "Refer to cells, not to numbers, so the answer changes when the data does. That is the whole point of a spreadsheet.")


# ------------------------------------------------------------------ choosing a chart

@illustration("chart-choice")
def _charts():
    cv = Canvas(800, 500).backdrop()
    spec = [("Bar chart", "teal", "compare categories"), ("Line chart", "coral", "show change over time"), ("Pie chart", "sun", "parts of one whole"), ("Scatter graph", "plum", "do two things relate?")]
    for n, (title, col, use) in enumerate(spec):
        x, y = (14, 406)[n % 2], (34, 238)[n // 2]
        cv.add(P.card(cv, x, y, 380, 190, 20, title, col))
        cv.add(P.badge(cv, x + 22, y + 24, n + 1))
        ox, oy = x + 130, y + 136
        if n == 0:
            cv.add(cv.line(ox - 10, y + 36, ox - 10, oy, ARROW, 2), cv.line(ox - 10, oy, ox + 220, oy, ARROW, 2))
            for i, (h_, c) in enumerate(((60, "teal"), (96, "teal"), (44, "teal"), (80, "teal"))):
                cv.add(cv.rect(ox + 8 + i * 54, oy - h_, 38, h_, 5, cv.g(c)))
                cv.add(cv.text(ox + 27 + i * 54, oy + 18, "Mon Tue Wed Thu".split()[i], 11.5, 650, cls="il-ink2"))
        elif n == 1:
            cv.add(cv.line(ox - 10, y + 36, ox - 10, oy, ARROW, 2), cv.line(ox - 10, oy, ox + 220, oy, ARROW, 2))
            pts = [(ox + 8, oy - 30), (ox + 62, oy - 52), (ox + 116, oy - 44), (ox + 170, oy - 86), (ox + 216, oy - 98)]
            cv.add(cv.path("M" + " L".join("%s %s" % p for p in pts), stroke="#C84B43", sw=4))
            for px, py in pts:
                cv.add(cv.circle(px, py, 5.5, "#FFFFFF", stroke="#C84B43", sw=3))
            for i, t in enumerate(("Jan", "Mar", "May", "Jul", "Sep")):
                cv.add(cv.text(pts[i][0], oy + 18, t, 11.5, 650, cls="il-ink2"))
        elif n == 2:
            pcx, pcy, pr = ox + 100, y + 96, 56
            ang = -90
            for frac, c in ((.5, "sun"), (.3, "coral"), (.2, "teal")):
                a0, a1 = math.radians(ang), math.radians(ang + frac * 360)
                x0_, y0_, x1_, y1_ = pcx + pr * math.cos(a0), pcy + pr * math.sin(a0), pcx + pr * math.cos(a1), pcy + pr * math.sin(a1)
                big = 1 if frac > .5 else 0
                cv.add(cv.path("M%s %s L%s %s A%s %s 0 %d 1 %s %s Z" % (pcx, pcy, _n(x0_), _n(y0_), pr, pr, big, _n(x1_), _n(y1_)), fill=cv.g(c, "deep"), stroke="#FFFFFF", sw=2.5))
                ang += frac * 360
        else:
            cv.add(cv.line(ox - 10, y + 36, ox - 10, oy, ARROW, 2), cv.line(ox - 10, oy, ox + 220, oy, ARROW, 2))
            dots = [(10, 20), (30, 34), (48, 30), (66, 52), (88, 50), (110, 70), (130, 66), (152, 92), (170, 88), (196, 108), (60, 26), (140, 80)]
            cv.add(cv.line(ox + 2, oy - 14, ox + 210, oy - 112, "#8061A9", 2.4, dash="6 5"))
            for dx, dy in dots:
                cv.add(cv.circle(ox + dx + 8, oy - dy - 6, 5.5, cv.g("plum", "deep")))
        cv.add(cv.text(x + 190, y + 176, "best for: " + use, 13.5, 700, cls="il-ink"))
    cv.add(P.pill(cv, 400, 462, "Every chart needs a title, labelled axes and, with more than one series, a legend.", "sun", 14, 16, 30, 750))
    return figure(
        "chart-choice", cv, "Four chart types and what each is best for: bar, line, pie and scatter",
        "Four chart types, each drawn with example data. A bar chart compares separate categories, here four days of the week. A line chart "
        "shows change over time, here a value rising across five months. A pie chart shows parts of one whole, with only a few slices, here three "
        "slices of 50, 30 and 20 percent. A scatter graph shows whether two things are related, here dots that rise from left to right "
        "around a dashed trend line. A note at the bottom says every chart needs a title, labelled axes and, when it has more than one series, a legend.",
        ["Bar chart: compare separate categories.", "Line chart: show how something changes over time.", "Pie chart: show parts of one whole, with only a few categories.",
         "Scatter graph: show whether two things are related."],
        "Pick the chart for the question you are asking. A pie chart with ten slices cannot be read.")
