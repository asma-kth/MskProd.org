"""Illustrations for how the computer system works: the pipeline, RISC and CISC, the operating
system, scheduling, utility software, and hardware against software."""
import math

from .illus import Canvas, PAL, INK, ARROW, figure, illustration, _n
from . import illus_props as P
from . import illus_glyphs as G


# ------------------------------------------------------------------ pipelining

STAGES = (("Fetch", "sky"), ("Decode", "sun"), ("Execute", "coral"))


def stage_block(cv, x, y, k, w=60, h=32):
    name, col = STAGES[k]
    return P.lift(cv, x, y, w, h, col, 8, 4, hl=False) + cv.text(x + w / 2, y + h / 2 + 4.5, name, 12.5, 750, fill=INK)


@illustration("pipelining")
def _pipe():
    cv = Canvas(800, 500).backdrop()
    x0, pitch = 150, 66

    def panel(top, title, color, starts, total):
        out = P.card(cv, 14, top, 772, 212, 20, title, color, tx=.3)
        out += cv.text(44, top + 46, "cycle", 13, 700, anchor="start", cls="il-ink2")
        for c in range(9):
            out += cv.text(x0 + c * pitch + 30, top + 46, str(c + 1), 13, 700, cls="il-ink2", mono=True)
        for i, st in enumerate(starts):
            y = top + 58 + i * 40
            out += cv.text(44, y + 21, "Instruction %d" % (i + 1), 13.5, 700, anchor="start", cls="il-ink")
            for k in range(3):
                out += stage_block(cv, x0 + (st + k) * pitch, y, k)
        out += P.pill(cv, 690, top + 190, total, "paper", 15, 14, 28, 800)
        return out

    cv.add(panel(34, "No pipeline: one at a time", "coral", (0, 3, 6), "9 cycles in all"))
    cv.add(panel(270, "With a pipeline: stages overlap", "teal", (0, 1, 2), "5 cycles in all"))
    # the time that is saved
    cv.add(cv.rect(x0 + 5 * pitch, 326, 4 * pitch, 118, 12, "var(--il-band)", stroke="var(--il-line)", sw=1.5, dash="6 5"))
    cv.add(cv.text(x0 + 7 * pitch, 372, "4 cycles saved", 17, 800, cls="il-ink"))
    cv.add(cv.text(x0 + 7 * pitch, 398, "a taken branch flushes it,", 12.5, 650, cls="il-ink2"), cv.text(x0 + 7 * pitch, 416, "so branches are predicted", 12.5, 650, cls="il-ink2"))
    cv.add(P.badge(cv, 36, 56, 1), P.badge(cv, 36, 292, 2), P.badge(cv, x0 + 5 * pitch + 6, 332, 3))
    return figure(
        "pipelining", cv, "Three instructions with and without a pipeline: nine cycles against five",
        "Pipelining shown on a grid of clock cycles. Every instruction has three stages: fetch, decode and execute. Without a pipeline, "
        "instruction 1 finishes all three stages before instruction 2 starts, and so on, so three instructions take 9 cycles. With a pipeline the "
        "stages overlap: in cycle 2 instruction 1 is being decoded while instruction 2 is fetched, and in cycle 3 instruction 1 executes while "
        "instruction 2 is decoded and instruction 3 is fetched. All three instructions finish in 5 cycles, which saves 4. One instruction still "
        "takes three cycles, so the gain is in throughput, close to one instruction per cycle. When a conditional jump is taken, the "
        "instructions already in the pipeline are the wrong ones and are discarded, which is a pipeline flush, so processors use branch "
        "prediction.",
        ["Without a pipeline each instruction finishes fetch, decode and execute before the next one starts: 3 instructions take 9 cycles.",
         "With a pipeline the stages overlap, so while one instruction executes the next is decoded and the one after is fetched: 5 cycles.",
         "One instruction still takes 3 cycles. The gain is throughput. A taken branch flushes the pipeline, which is why branches are predicted."],
        "Pipelining does not make one instruction faster. It raises throughput by keeping every stage busy at once.")


# ------------------------------------------------------------------ RISC and CISC

@illustration("risc-cisc")
def _riscc():
    cv = Canvas(800, 500).backdrop()
    cv.add(P.pill(cv, 400, 20, "the same job: c = a × b", "sun", 15.5, 16, 30, 750))
    # RISC: several small steps
    cv.add(P.card(cv, 14, 54, 380, 176, 20, "RISC", "teal"))
    for i, (lab, col) in enumerate((("LOAD a", "sky"), ("LOAD b", "sky"), ("MULT", "coral"), ("STORE c", "mint"))):
        x = 30 + i * 90
        cv.add(P.lift(cv, x, 92, 82, 42, col, 9, 5, hl=False), cv.text(x + 41, 92 + 21 + 5, lab, 13.5, 800, fill=INK, mono=True))
        cv.add(cv.text(x + 41, 160, "cycle %d" % (i + 1), 12.5, 650, cls="il-ink2", mono=True))
    cv.add(cv.text(204, 192, "4 simple instructions", 15, 750, cls="il-ink"), cv.text(204, 212, "one cycle each", 13, 650, cls="il-ink2"))
    # CISC: one big step
    cv.add(P.card(cv, 406, 54, 380, 176, 20, "CISC", "plum"))
    cv.add(P.lift(cv, 426, 92, 340, 42, "coral", 9, 5, hl=False))
    for k in range(1, 5):
        cv.add(cv.line(426 + k * 68, 119, 426 + k * 68, 131, "#FFFFFF", 2.4, op=.85))
    cv.add(cv.text(596, 92 + 21 + 1, "MULT a, b, c", 15, 800, fill=INK, mono=True))
    for k in range(5):
        cv.add(cv.text(426 + k * 68 + 34, 160, "cycle %d" % (k + 1), 12.5, 650, cls="il-ink2", mono=True))
    cv.add(cv.text(596, 192, "1 complex instruction", 15, 750, cls="il-ink"), cv.text(596, 212, "several cycles", 13, 650, cls="il-ink2"))
    # the comparison
    cv.add(P.card(cv, 14, 254, 772, 236, 20))
    cv.add(P.pill(cv, 430, 276, "RISC", "teal", 15.5, 18, 28, 800), P.pill(cv, 660, 276, "CISC", "plum", 15.5, 18, 28, 800))
    rows = [("Instruction set", "small and simple", "large and complex"),
            ("Instruction length", "fixed", "variable"),
            ("Cycles per instruction", "usually one", "several"),
            ("Instructions per task", "more", "fewer"),
            ("Complexity is in", "the compiler", "the hardware"),
            ("Power use", "lower (ARM, phones)", "higher (x86, PCs)")]
    for i, (lab, a_, b_) in enumerate(rows):
        y = 298 + i * 31
        if i % 2 == 0:
            cv.add(cv.rect(26, y, 748, 29, 8, "var(--il-band)"))
        cv.add(cv.text(42, y + 20, lab, 14, 750, anchor="start", cls="il-ink"))
        cv.add(cv.text(430, y + 20, a_, 14, 650, cls="il-ink"), cv.text(660, y + 20, b_, 14, 650, cls="il-ink"))
    cv.add(P.badge(cv, 36, 76, 1), P.badge(cv, 428, 76, 2), P.badge(cv, 36, 256, 3))
    return figure(
        "risc-cisc", cv, "RISC and CISC doing the same job, and how they compare",
        "The same job, c equals a times b, done on a RISC and on a CISC processor. A RISC processor uses four simple instructions of the same "
        "size, LOAD a, LOAD b, MULT and STORE c, and each takes one cycle. A CISC processor has a single complex instruction, MULT a, b, c, "
        "that does the whole job but takes several cycles. A table compares them. RISC has a small, simple instruction set, fixed length "
        "instructions, usually one cycle per instruction, more instructions per task, its complexity in the compiler, and lower power use, as in "
        "ARM processors in phones. CISC has a large, complex instruction set, variable length instructions, several cycles per instruction, "
        "fewer instructions per task, its complexity in the hardware, and higher power use, as in x86 processors in PCs.",
        ["RISC does the job with four simple instructions, one cycle each.",
         "CISC does it with one complex instruction that takes several cycles.",
         "The trade off is where the complexity sits: RISC puts it in the compiler, CISC in the hardware."],
        "Neither is better. RISC suits pipelining and low power, which is why it dominates phones.")


# ------------------------------------------------------------------ the operating system

def mini_window(cv, x, y, w=54, h=40):
    out = cv.rect(x, y, w, h, 6, "#FFFFFF", stroke="#9FB3BE", sw=1.5)
    out += cv.rect(x + .75, y + .75, w - 1.5, 11, 5, cv.g("teal")) + cv.rect(x + .75, y + 7, w - 1.5, 5, 0, cv.g("teal"))
    for i, c in enumerate(("#FF7B72", "#FFCB47", "#5BD58B")):
        out += cv.circle(x + 8 + i * 7, y + 6.2, 2, c)
    out += cv.rect(x + 7, y + 19, w * .5, 5, 2, "#C5D1D9") + cv.rect(x + 7, y + 28, w - 14, 5, 2, "#C5D1D9")
    return out


def mini_printer(cv, x, y):
    out = cv.rect(x + 12, y, 30, 16, 3, "#FFFFFF", stroke="#9FB3BE", sw=1.4)
    out += P.lift(cv, x, y + 12, 54, 24, "slate", 8, 4, hl=False)
    out += cv.circle(x + 44, y + 24, 2.6, "#5BE08A")
    out += cv.rect(x + 10, y + 34, 34, 14, 2, "#FFFFFF", stroke="#9FB3BE", sw=1.4) + cv.rect(x + 15, y + 40, 24, 3, 1.5, "#C5D1D9")
    return out


def mini_memory(cv, x, y):
    out = ""
    for i, c in enumerate(("sky", "sky", "coral", "slate", "mint", "mint", "slate", "sun")):
        out += P.lift(cv, x + (i % 4) * 14, y + (i // 4) * 17, 12, 12, c, 3, 2, hl=False)
    return out


@illustration("os-jobs")
def _os():
    cv = Canvas(800, 500).backdrop()
    hx, hy = 400, 250
    cards = [(14, 76, "Memory", ("decides which program", "gets which part of RAM"), "mem"),
             (14, 202, "Processor time", ("shares the CPU between", "the running programs"), "cpu"),
             (14, 328, "Files", ("folders, names and", "where data is stored"), "file"),
             (546, 76, "Devices", ("drivers let programs use", "printers, screens, disks"), "dev"),
             (546, 202, "Security", ("log-ins, accounts and", "who can open what"), "lock"),
             (546, 328, "User interface", ("windows, icons, menus", "or typed commands"), "ui")]
    # the spokes first, so that everything else sits on top of them
    for x, y, *_ in cards:
        ex = x + 240 if x < 400 else x
        cv.add(cv.line(hx, hy, ex, y + 48, PAL["teal"][1], 5, op=.75))
        cv.add(cv.circle(ex, y + 48, 6, PAL["teal"][2]))
    for x, y, title, subs, icon in cards:
        cv.add(P.card(cv, x, y, 240, 96, 16))
        if icon == "mem":
            cv.add(mini_memory(cv, x + 16, y + 34))
        elif icon == "cpu":
            cv.add(P.cpu_chip(cv, x + 18, y + 26, 42, "CPU"))
        elif icon == "file":
            cv.add(P.folder(cv, x + 14, y + 28, .62))
        elif icon == "dev":
            cv.add(mini_printer(cv, x + 12, y + 24))
        elif icon == "lock":
            cv.add(P.padlock(cv, x + 20, y + 22, .66))
        else:
            cv.add(mini_window(cv, x + 12, y + 28))
        cv.add(cv.text(x + 78, y + 38, title, 16.5, 750, anchor="start", cls="il-ink"))
        cv.add(cv.text(x + 78, y + 59, subs[0], 12.5, 650, anchor="start", cls="il-ink2"), cv.text(x + 78, y + 76, subs[1], 12.5, 650, anchor="start", cls="il-ink2"))
    # the hub, with programs above it and hardware below
    cv.add(P.pill(cv, hx, 40, "Applications", "sky", 16, 18, 32, 750), P.arrow(cv, [(hx, 62), (hx, 176)], ARROW, 4, 12))
    cv.add(P.arrow(cv, [(hx, 324), (hx, 424)], ARROW, 4, 12), P.pill(cv, hx, 450, "Hardware", "sun", 16, 18, 32, 750))
    cv.add(cv.shadow(hx, hy + 76, 70, 8, .22))
    cv.add(cv.circle(hx, hy, 74, "#FFFFFF"), cv.circle(hx, hy, 68, cv.g("deep", "deep")))
    cv.add(cv.text(hx, hy - 4, "Operating", 19, 800, fill="#FFFFFF"), cv.text(hx, hy + 20, "system", 19, 800, fill="#FFFFFF"))
    cv.add(P.badge(cv, 346, 192, 1), P.badge(cv, 30, 78, 2), P.badge(cv, 562, 78, 3))
    return figure(
        "os-jobs", cv, "What the operating system does, between the applications and the hardware",
        "The operating system sits between the applications above it and the hardware below it, with an arrow from the applications down into "
        "the operating system and another from the operating system down to the hardware. Six jobs surround it. Memory management decides "
        "which program gets which part of RAM. Processor scheduling shares the CPU between the running programs. File management looks after "
        "folders, names and where data is stored. Device drivers let programs use printers, screens and disks. Security handles log-ins, "
        "accounts and who can open what. The user interface provides windows, icons and menus, or typed commands.",
        ["The operating system sits between the applications and the hardware, so a program never has to deal with the hardware directly.",
         "It shares out the computer's resources: memory, processor time and storage.",
         "It also talks to devices through drivers, keeps the system secure and provides the user interface."],
        "Most exam answers on the operating system are a list of these jobs with one sentence on what each one does.")


# ------------------------------------------------------------------ scheduling

JOBS = {"A": "coral", "B": "sky", "C": "mint"}


def gantt(cv, x, y, segs, u=54):
    out, marks = "", set()
    for job, st, ln in segs:
        out += P.lift(cv, x + st * u + 1.5, y, ln * u - 3, 36, JOBS[job], 8, 4, hl=False)
        out += cv.text(x + st * u + ln * u / 2, y + 18 + 7, job, 18, 800, fill=INK, mono=True)
        marks.update((st, st + ln))
    out += cv.line(x, y + 46, x + 10 * u, y + 46, "#8AA0AC", 2)
    for m in sorted(marks):
        out += cv.line(x + m * u, y + 42, x + m * u, y + 50, "#8AA0AC", 2)
        out += cv.text(x + m * u, y + 65, str(m), 12.5, 700, cls="il-ink2", mono=True)
    return out


@illustration("scheduling")
def _sched():
    cv = Canvas(800, 500).backdrop()
    cv.add(P.band(cv, 14, 18, 772, 58, 16))
    cv.add(cv.text(34, 53, "Three jobs arrive together:", 14.5, 750, anchor="start", cls="il-ink"))
    for i, (job, need) in enumerate((("A", 5), ("B", 3), ("C", 2))):
        x = 262 + i * 126
        cv.add(P.lift(cv, x, 30, 112, 34, JOBS[job], 10, 4, hl=False), cv.text(x + 56, 30 + 17 + 6, "%s needs %d" % (job, need), 15, 800, fill=INK))
    cv.add(cv.text(650, 53, "time units of CPU", 13, 650, anchor="start", cls="il-ink2"))
    specs = [(96, "First come first served", "coral", [("A", 0, 5), ("B", 5, 3), ("C", 8, 2)], "avg wait 4.3", "all started by 8", "long job blocks others"),
             (220, "Shortest job first", "sky", [("C", 0, 2), ("B", 2, 3), ("A", 5, 5)], "avg wait 2.3", "all started by 5", "must know the lengths"),
             (344, "Round robin, slice of 2", "teal", [("A", 0, 2), ("B", 2, 2), ("C", 4, 2), ("A", 6, 2), ("B", 8, 1), ("A", 9, 1)], "avg wait 5.0", "all started by 4", "fair share of the CPU")]
    for n, (top, title, col, segs, l1, l2, l3) in enumerate(specs):
        cv.add(P.card(cv, 14, top, 772, 112, 18, title, col, tx=.28))
        cv.add(gantt(cv, 56, top + 34, segs))
        cv.add(cv.text(618, top + 50, l1, 15.5, 800, anchor="start", cls="il-ink"), cv.text(618, top + 71, l2, 13, 650, anchor="start", cls="il-ink2"), cv.text(618, top + 90, l3, 13, 650, anchor="start", cls="il-ink2"))
        cv.add(P.badge(cv, 34, top + 6, n + 1))
    cv.add(cv.text(400, 482, "Wait = time spent waiting for the CPU before the job finishes.", 13.5, 650, cls="il-ink2"))
    return figure(
        "scheduling", cv, "Three scheduling algorithms run on the same three jobs",
        "Three jobs arrive together: A needs 5 time units of processor time, B needs 3 and C needs 2. Each scheduling algorithm is drawn as a "
        "chart of who has the processor over time. First come first served runs A for 0 to 5, B for 5 to 8 and C for 8 to 10. The long job A "
        "makes the others wait, the average wait is 4.3 and the last job does not start until time 8. Shortest job first runs C for 0 to 2, B "
        "for 2 to 5 and A for 5 to 10. It has the lowest average wait, 2.3, but it must know how long each job is in advance. Round robin with a "
        "time slice of 2 runs A, B, C, A, B, A for slices of 2, 2, 2, 2, 1 and 1. It is fair, every job has started by time 4, but the "
        "average wait is 5.0.",
        ["First come first served: jobs run in arrival order, so the long job A holds up B and C.",
         "Shortest job first: the lowest average wait, but it needs to know the lengths and can starve long jobs.",
         "Round robin: each job gets a short slice in turn, so everyone starts quickly and shares the CPU fairly."],
        "There is no best algorithm. Each trades fairness, response time and average waiting time.")


# ------------------------------------------------------------------ utility software

def brick(cv, x, y, w=34, h=17):
    return cv.rect(x, y + 2, w, h, 3, PAL["coral"][2]) + cv.rect(x, y, w, h, 3, cv.g("coral"))


@illustration("utilities")
def _utils():
    cv = Canvas(800, 500).backdrop()
    xs, ys = (14, 277, 540), (36, 266)
    spec = [("Antivirus", "coral", "finds and removes malware"), ("Firewall", "sun", "blocks unwanted traffic"), ("Defragmentation", "sky", "joins each file's pieces up"),
            ("Compression", "mint", "makes files smaller"), ("Backup", "teal", "keeps a second copy safe"), ("Encryption", "plum", "scrambles data; a key unlocks it")]
    for n, (title, col, cap) in enumerate(spec):
        x, y = xs[n % 3], ys[n // 3]
        cv.add(P.card(cv, x, y, 246, 200, 18, title, col))
        cv.add(cv.text(x + 123, y + 182, cap, 13.5, 700, cls="il-ink"))
        cv.add(P.badge(cv, x + 16, y + 24, n + 1))
        cx = x + 123
        if n == 0:      # a shield stops a bug
            cv.add(cv.circle(x + 62, y + 106, 44, "#EEF3F6", op=.95))
            cv.add(G.bug(cv, x + 62, y + 106, 1.5))
            cv.add(P.cross(cv, x + 90, y + 74, 13))
            sh = "M%s %s L%s %s L%s %s Q%s %s %s %s Q%s %s %s %s L%s %s Z" % (cx + 62, y + 52, cx + 98, y + 64, cx + 98, y + 106, cx + 98, y + 140, cx + 62, y + 156,
                                                                              cx + 26, y + 140, cx + 26, y + 106, cx + 26, y + 64)
            cv.add(cv.path(sh, fill=cv.g("teal"), stroke=PAL["teal"][2], sw=3))
            cv.add(cv.path("M%s %s L%s %s L%s %s" % (cx + 46, y + 104, cx + 58, y + 118, cx + 80, y + 88), stroke="#FFFFFF", sw=8))
        elif n == 1:    # a wall with a gate, seen from above
            wx = cx - 16
            for i in range(2):
                cv.add(brick(cv, wx + (i % 2) * 8 - 4, y + 44 + i * 19), brick(cv, wx + (i % 2) * 8 - 4, y + 114 + i * 19))
            cv.add(P.arrow(cv, [(x + 24, y + 62), (wx - 8, y + 62)], "#BA352D", 5, 13))
            cv.add(P.arrow(cv, [(x + 24, y + 98), (x + 222, y + 98)], "#248049", 5, 13))
            cv.add(cv.text(x + 62, y + 84, "blocked", 12.5, 750, cls="il-bad"), cv.text(x + 78, y + 122, "allowed", 12.5, 750, cls="il-ok"))
        elif n == 2:    # files in pieces are gathered up
            colors = {"A": "coral", "B": "sky", "C": "mint"}

            def strip(yy, seq):
                out = ""
                for i, c in enumerate(seq):
                    px = x + 12 + i * 18.5
                    out += cv.rect(px, yy, 16.5, 28, 3, "var(--il-band)", stroke="var(--il-line)", sw=1.2, dash="3 3") if c == "_" else cv.rect(px, yy, 16.5, 28, 3, cv.g(colors[c]))
                return out
            cv.add(cv.text(x + 14, y + 48, "before", 12.5, 700, anchor="start", cls="il-ink2"))
            cv.add(strip(y + 54, "AB_ACB_CA_BC"))
            cv.add(P.arrow(cv, [(cx, y + 90), (cx, y + 108)], ARROW, 3.5, 10))
            cv.add(cv.text(x + 14, y + 124, "after", 12.5, 700, anchor="start", cls="il-ink2"))
            cv.add(strip(y + 130, "AAABBBCCC___"))
        elif n == 3:    # a big folder becomes a small one
            cv.add(P.folder(cv, x + 22, y + 62, 1.0))
            cv.add(cv.text(x + 64, y + 150, "10 MB", 14, 800, cls="il-ink", mono=True))
            cv.add(P.arrow(cv, [(x + 114, y + 92), (x + 148, y + 92)], ARROW, 4, 11))
            cv.add(P.folder(cv, x + 160, y + 78, .62, "mint"))
            for k in range(5):
                cv.add(cv.rect(x + 186 + (k % 2) * 3 - 1.5, y + 92 + k * 5, 4, 3.6, 1, "#2F9F77"))
            cv.add(cv.text(x + 186, y + 150, "4 MB", 14, 800, cls="il-ink", mono=True))
        elif n == 4:    # files are copied to the cloud
            cv.add(P.folder(cv, x + 20, y + 66, 1.0))
            cv.add(cv.text(x + 62, y + 150, "your files", 13, 700, cls="il-ink2"))
            cv.add(P.arrow(cv, [(x + 110, y + 98), (x + 142, y + 98)], ARROW, 4, 11))
            cv.add(P.cloud(cv, x + 144, y + 62, 92))
            cv.add(P.folder(cv, x + 172, y + 80, .42))
            cv.add(cv.text(x + 190, y + 150, "a copy", 13, 700, cls="il-ink2"))
        else:           # plain text becomes cipher text, through a lock
            cv.add(cv.rect(x + 12, y + 74, 62, 34, 9, "#FFFFFF", stroke="#9FB3BE", sw=1.6), cv.text(x + 43, y + 97, "Hello", 14, 800, fill=INK, mono=True))
            cv.add(P.arrow(cv, [(x + 78, y + 91), (x + 96, y + 91)], ARROW, 3.5, 9))
            cv.add(P.padlock(cv, x + 100, y + 62, .8))
            cv.add(P.arrow(cv, [(x + 148, y + 91), (x + 166, y + 91)], ARROW, 3.5, 9))
            cv.add(cv.rect(x + 170, y + 74, 62, 34, 9, INK, stroke="#9FB3BE", sw=1.6), cv.text(x + 201, y + 97, "x9#Q!", 14, 800, fill="#FFFFFF", mono=True))
            cv.add(cv.text(x + 43, y + 130, "plain text", 12.5, 650, cls="il-ink2"), cv.text(x + 201, y + 130, "cipher text", 12.5, 650, cls="il-ink2"))
    return figure(
        "utilities", cv, "Six utility programs: antivirus, firewall, defragmentation, compression, backup and encryption",
        "Six kinds of utility software, each drawn as a small scene. Antivirus software is a shield that stops a bug, finding and removing "
        "malware. A firewall is a wall with a gap, seen from above: unwanted traffic is blocked by the wall while allowed traffic passes "
        "through the gate. Defragmentation takes a disk where each file is in separate pieces with gaps between them and gathers every file's "
        "pieces together, leaving the free space at the end. Compression turns a 10 megabyte folder into a 4 megabyte one. Backup copies "
        "your files to a second place, shown as the cloud, so that a copy is safe if the original is lost. Encryption scrambles plain text, "
        "here Hello, into cipher text, here x9#Q!, so that only someone with the key can read it.",
        ["Antivirus finds and removes malware.", "A firewall blocks unwanted traffic and lets allowed traffic through.",
         "Defragmentation puts each file's pieces next to each other, which speeds up a hard disk.",
         "Compression makes files smaller so they use less storage and send faster.",
         "Backup keeps a second copy of your files in case the originals are lost.",
         "Encryption scrambles data so that only someone with the key can read it."],
        "System software has two parts: the operating system, and utilities that look after and protect the computer.")


# ------------------------------------------------------------------ hardware and software

def keyboard(cv, x, y, w=120, h=52):
    out = P.lift(cv, x, y, w, h, "metal", 9, 5, hl=False)
    kw = (w - 16) / 10
    for r in range(3):
        for c in range(10):
            out += cv.rect(x + 8 + c * kw + 1, y + 8 + r * 12, kw - 3, 9, 2, "#FFFFFF", stroke="#B9C6CE", sw=.8)
    out += cv.rect(x + 28, y + 8 + 3 * 12 - 1, w - 56, 8, 2, "#FFFFFF", stroke="#B9C6CE", sw=.8)
    return out


def gamepad(cv, x, y):
    out = P.lift(cv, x, y + 10, 110, 48, "navy", 22, 5, hl=False)
    out += cv.rect(x + 22, y + 28, 24, 7, 3, "#FFFFFF") + cv.rect(x + 30.5, y + 19.5, 7, 24, 3, "#FFFFFF")
    out += cv.circle(x + 78, y + 38, 6, "#FFC93C") + cv.circle(x + 92, y + 28, 6, "#F0584B")
    return out


@illustration("hardware-software")
def _hws():
    cv = Canvas(800, 500).backdrop()
    cv.add(P.card(cv, 14, 34, 372, 286, 20, "Hardware: parts you can touch", "teal"))
    hw = [(34, 66), (206, 66), (34, 196), (206, 196)]
    cv.add(P.monitor(cv, hw[0][0] + 34, hw[0][1] + 2, .5))
    cv.add(cv.text(hw[0][0] + 80, hw[0][1] + 104, "monitor", 15, 700, cls="il-ink"))
    cv.add(keyboard(cv, hw[1][0] + 14, hw[1][1] + 24))
    cv.add(cv.text(hw[1][0] + 74, hw[1][1] + 104, "keyboard", 15, 700, cls="il-ink"))
    cv.add(P.cpu_chip(cv, hw[2][0] + 50, hw[2][1] + 14, 60, "CPU"))
    cv.add(cv.text(hw[2][0] + 80, hw[2][1] + 104, "processor", 15, 700, cls="il-ink"))
    cv.add(P.ram_stick(cv, hw[3][0] + 2, hw[3][1] + 26, 140, 44, 1, 4))
    cv.add(cv.text(hw[3][0] + 72, hw[3][1] + 104, "memory", 15, 700, cls="il-ink"))
    cv.add(P.card(cv, 414, 34, 372, 286, 20, "Software: programs that run", "plum"))
    sw = [(434, 66), (606, 66), (434, 196), (606, 196)]
    cv.add(cv.rect(sw[0][0] + 6, sw[0][1] + 6, 126, 78, 6, "#FFFFFF", stroke="#9FB3BE", sw=1.4), P.browser_screen(cv, sw[0][0] + 12, sw[0][1] + 12, 114, 66, "mskprod.org"))
    cv.add(cv.text(sw[0][0] + 70, sw[0][1] + 104, "web browser", 15, 700, cls="il-ink"))
    cv.add(P.doc(cv, sw[1][0] + 46, sw[1][1] + 2, 1.0, 62, 82, 5, "paper", "sky"))
    cv.add(cv.text(sw[1][0] + 78, sw[1][1] + 104, "word processor", 15, 700, cls="il-ink"))
    cv.add(gamepad(cv, sw[2][0] + 14, sw[2][1] + 14))
    cv.add(cv.text(sw[2][0] + 70, sw[2][1] + 104, "game", 15, 700, cls="il-ink"))
    cv.add(mini_window(cv, sw[3][0] + 36, sw[3][1] + 14, 92, 62))
    cv.add(P.gear(cv, sw[3][0] + 126, sw[3][1] + 62, 18, "slate"))
    cv.add(cv.text(sw[3][0] + 78, sw[3][1] + 104, "operating system", 15, 700, cls="il-ink"))
    # together
    cv.add(P.card(cv, 14, 348, 772, 142, 20, "How they work together", "sun"))
    cv.add(P.lift(cv, 40, 392, 170, 50, "plum", 12, 5, hl=False), cv.text(125, 392 + 25 + 6, "Software", 18, 800, fill="#FFFFFF"))
    cv.add(P.arrow(cv, [(220, 417), (262, 417)], ARROW, 4.5, 13))
    cv.add(P.lift(cv, 272, 392, 170, 50, "teal", 12, 5, hl=False), cv.text(357, 392 + 25 + 6, "Hardware", 18, 800, fill=INK))
    cv.add(cv.text(125, 466, "gives the instructions", 13.5, 650, cls="il-ink2"), cv.text(357, 466, "carries them out", 13.5, 650, cls="il-ink2"))
    for i, (t1, t2) in enumerate((("No software: the hardware has", "nothing to do."), ("No hardware: the software has", "nothing to run on."))):
        cv.add(cv.circle(488, 398 + i * 50, 6, cv.g("teal", "deep")), cv.text(504, 403 + i * 50, t1, 14.5, 700, anchor="start", cls="il-ink"), cv.text(504, 423 + i * 50, t2, 14.5, 700, anchor="start", cls="il-ink"))
    cv.add(P.badge(cv, 36, 56, 1), P.badge(cv, 436, 56, 2), P.badge(cv, 36, 370, 3))
    return figure(
        "hardware-software", cv, "Hardware you can touch, software that runs on it, and how they work together",
        "Hardware is the physical parts of a computer that you can touch: the monitor, the keyboard, the processor and the memory. Software "
        "is the programs, the instructions that tell the hardware what to do: a web browser, a word processor, a game and the operating system. "
        "Software gives the instructions and the hardware carries them out. Without software the hardware has nothing to do, and without "
        "hardware the software has nothing to run on.",
        ["Hardware is the physical parts you can touch, such as the monitor, keyboard, processor and memory.",
         "Software is the programs: the instructions, such as a browser, a word processor, a game or the operating system.",
         "Software gives the instructions and hardware carries them out. A computer needs both."],
        "If you can touch it, it is hardware. If it is a set of instructions, it is software.")
