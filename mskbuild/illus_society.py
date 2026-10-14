"""Illustrations for computing in society: software licences, your data trail and the four
kinds of impact technology has."""
import math

from .illus import Canvas, PAL, INK, ARROW, figure, illustration, _n
from . import illus_props as P
from . import illus_glyphs as G


# ------------------------------------------------------------------ open source against proprietary

@illustration("licences")
def _licences():
    cv = Canvas(800, 500).backdrop()
    rows = [("Source code", ("hidden", False), ("provided", True)), ("Modify it", ("not allowed", False), ("allowed", True)),
            ("Share copies", ("not allowed", False), ("allowed", True)), ("Cost", ("usually paid", None), ("often free", None)),
            ("Support", ("from the company", None), ("from the community", None))]
    for k, (x, title, col) in enumerate(((14, "Proprietary", "coral"), (406, "Open source", "mint"))):
        cv.add(P.card(cv, x, 26, 380, 388, 20, title, col))
        cv.add(P.badge(cv, x + 22, 52, k + 1))
        if k == 0:
            cv.add(P.lift(cv, x + 110, 62, 160, 88, "dark", 16, 6, hl=False))
            cv.add(cv.text(x + 190, 98, "app.exe", 16, 800, fill="#FFFFFF", mono=True))
            cv.add(P.padlock(cv, x + 172, 106, .62, "sun"))
            cv.add(cv.text(x + 190, 178, "you get the finished program only", 13.5, 700, cls="il-ink2"))
        else:
            cv.add(G.code(cv, x + 60, 62, 260, ["def greet(name):", "    return 'Hi ' + name"], title="app.py", size=12.5, numbers=False))
            cv.add(cv.text(x + 190, 178, "you get the source code as well", 13.5, 700, cls="il-ink2"))
        for i, (lab, left, right) in enumerate(rows):
            y = 200 + i * 40
            val, mark = left if k == 0 else right
            if i % 2 == 0:
                cv.add(cv.rect(x + 12, y, 356, 34, 8, "var(--il-band)"))
            cv.add(cv.text(x + 26, y + 23, lab, 14, 750, anchor="start", cls="il-ink"))
            if mark is True:
                cv.add(P.tick(cv, x + 206, y + 17, 10))
            elif mark is False:
                cv.add(P.cross(cv, x + 206, y + 17, 10))
            else:
                cv.add(cv.circle(x + 206, y + 17, 5, cv.g("teal", "deep")))
            cv.add(cv.text(x + 226, y + 23, val, 14, 650, anchor="start", cls="il-ink"))
    cv.add(P.card(cv, 14, 432, 772, 54, 16))
    cv.add(P.badge(cv, 36, 459, 3), G.warning(cv, 82, 459, .8), cv.text(110, 465, "Open source does not mean free of charge. It means the source code is open.", 15, 750, anchor="start", cls="il-ink"))
    return figure(
        "licences", cv, "Proprietary against open source software",
        "Two kinds of software licence compared. Proprietary software is sold as a finished program, shown as a locked box called app dot exe. "
        "The source code is hidden, you may not modify it, you may not share copies, it is usually paid for, and support comes from the company. "
        "Open source software comes with its source code, shown as a window of readable code. The source is provided, you may modify it, you may "
        "share copies, it is often free, and support comes from the community. A reminder at the bottom says that open source does not mean free "
        "of charge: it means the source code is open.",
        ["Proprietary software is a finished program. The source code is hidden and the licence limits what you may do.",
         "Open source software comes with its source code, and the licence lets you modify it and share copies.",
         "Open source does not mean free of charge. It means the source code is open."],
        "For a school with little money open source is attractive, but proprietary software comes with a company that must fix problems.")


# ------------------------------------------------------------------ your data trail

def bag(cv, x, y):
    out = cv.path("M%s %s q0 -14 10 -14 q10 0 10 14" % (x + 6, y + 8), stroke="#8A5A2B", sw=3)
    return out + cv.rect(x, y + 6, 32, 28, 5, cv.g("coral")) + cv.rect(x + 3, y + 8, 26, 5, 2, "#FFFFFF", op=.3)


def pin(cv, x, y):
    d = "M%s %s C%s %s %s %s %s %s A16 16 0 0 1 %s %s C%s %s %s %s %s %s Z" % (x + 16, y + 38, x + 8, y + 30, x, y + 22, x, y + 16, x + 32, y + 16, x + 32, y + 22, x + 24, y + 30, x + 16, y + 38)
    return cv.path(d, fill=cv.g("red"), stroke=PAL["red"][2], sw=1.4) + cv.circle(x + 16, y + 15, 6, "#FFFFFF")


def star(cv, cx, cy, r=18):
    pts = []
    for k in range(10):
        a = -math.pi / 2 + k * math.pi / 5
        rr = r if k % 2 == 0 else r * .45
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    return cv.poly(pts, cv.g("sun"), stroke=PAL["sun"][2], sw=1.4)


@illustration("data-trail")
def _trail():
    cv = Canvas(800, 500).backdrop()
    # 1 what you leave behind
    cv.add(P.card(cv, 14, 34, 230, 372, 20, "Your data trail", "teal"))
    rows = [("Posts and photos", "what you share"), ("Searches", "what you look for"), ("Purchases", "what you buy"), ("Location", "where you go"), ("Cookies", "sites remember you")]
    for i, (a_, b_) in enumerate(rows):
        y = 88 + i * 62
        if i == 0:
            cv.add(P.photo(cv, 34, y - 6, 46, 34, 4))
        elif i == 1:
            cv.add(P.magnifier(cv, 52, y + 8, 1.0, 12))
        elif i == 2:
            cv.add(bag(cv, 38, y - 4))
        elif i == 3:
            cv.add(pin(cv, 38, y - 8))
        else:
            cv.add(G.cookie(cv, 57, y + 12, 15))
        cv.add(cv.text(100, y + 8, a_, 14.5, 750, anchor="start", cls="il-ink"), cv.text(100, y + 28, b_, 12.5, 650, anchor="start", cls="il-ink2"))
    cv.add(P.arrow(cv, [(250, 220), (280, 220)], PAL["teal"][2], 5, 13))
    # 2 the profile it builds
    cv.add(P.card(cv, 284, 34, 232, 372, 20, "Your profile", "coral"))
    cv.add(cv.circle(400, 112, 30, cv.g("slate", "deep")), cv.circle(400, 104, 11, "#FFFFFF"), cv.path("M378 132 Q400 108 422 132 Z", fill="#FFFFFF"))
    cv.add(cv.text(400, 168, "built from the trail", 13, 650, cls="il-ink2"))
    for i, t in enumerate(("likes football", "age 13 to 15", "lives near London", "buys trainers", "watches gaming")):
        cv.add(P.pill(cv, 400, 202 + i * 38, t, "paper", 13.5, 12, 28, 700))
    cv.add(P.arrow(cv, [(522, 220), (552, 220)], PAL["teal"][2], 5, 13))
    # 3 who uses it
    cv.add(P.card(cv, 556, 34, 230, 372, 20, "Who uses it", "sun"))
    users = [("Advertisers", "show you targeted ads"), ("Websites and apps", "recommend things"), ("Data brokers", "sell your profile on")]
    for i, (a_, b_) in enumerate(users):
        y = 96 + i * 100
        if i == 1:
            cv.add(star(cv, 592, y + 16, 25))
        else:
            cv.add(cv.circle(592, y + 16, 22, cv.g("sun"), stroke=PAL["sun"][2], sw=1.4), cv.text(592, y + 24, "£", 22, 800, fill=INK))
        cv.add(cv.text(626, y + 12, a_, 14.5, 750, anchor="start", cls="il-ink"), cv.text(626, y + 32, b_, 12.5, 650, anchor="start", cls="il-ink2"))
        if i < 2:
            cv.add(cv.line(576, y + 66, 766, y + 66, "var(--il-line)", 1.4))
    # you stay in control
    cv.add(P.card(cv, 14, 424, 772, 64, 16))
    cv.add(P.padlock(cv, 30, 436, .5, "sun"), cv.text(70, 462, "You stay in control:", 15, 800, anchor="start", cls="il-ink"))
    for t, x in (("privacy settings", 250), ("limit cookies", 420), ("think before you post", 566)):
        cv.add(P.pill(cv, x, 456, t, "mint", 13.5, 12, 28, 750, anchor="start"))
    cv.add(P.badge(cv, 36, 56, 1), P.badge(cv, 306, 56, 2), P.badge(cv, 578, 56, 3))
    return figure(
        "data-trail", cv, "Your data trail, the profile it builds, and who uses it",
        "How your data is collected and used. Everything you do online leaves a trail: the posts and photos you share, your searches, your "
        "purchases, your location and the cookies that websites store. That trail is put together into a profile, for example likes football, "
        "age 13 to 15, lives near London, buys trainers, watches gaming. The profile is used by advertisers to show you targeted ads, by websites "
        "and apps to recommend things, and by data brokers who sell it on. You stay in control through privacy settings, by limiting cookies and "
        "by thinking before you post.",
        ["Everything you do online leaves data behind: posts, searches, purchases, location and cookies.",
         "Companies join the pieces into a profile of you.",
         "Advertisers, websites and data brokers use the profile, to sell to you or to sell it on."],
        "Your data trail is permanent and valuable. Privacy settings and care about what you share are how you control it.")


# ------------------------------------------------------------------ the four kinds of impact

def scales(cv, cx, cy):
    out = cv.rect(cx - 18, cy + 32, 36, 7, 3, cv.g("dark", "deep")) + cv.line(cx, cy - 30, cx, cy + 34, "#5B6D79", 5)
    out += cv.line(cx - 34, cy - 24, cx + 34, cy - 18, "#36464F", 4)
    for (bx, by, sx) in ((cx - 34, cy - 24, -1), (cx + 34, cy - 18, 1)):
        py = by + 28
        out += cv.line(bx, by, bx - 13, py, "#8799A7", 1.6) + cv.line(bx, by, bx + 13, py, "#8799A7", 1.6)
        out += cv.path("M%s %s Q%s %s %s %s Z" % (bx - 15, py, bx, py + 15, bx + 15, py), fill=cv.g("coral"), stroke=PAL["coral"][2], sw=1.2)
    return out + cv.circle(cx, cy - 31, 4, cv.g("sun"))


def gavel(cv, cx, cy):
    out = cv.rect(cx - 30, cy + 30, 60, 10, 4, PAL["wood"][2]) + cv.rect(cx - 22, cy + 22, 44, 9, 4, cv.g("wood"))
    head = cv.rect(-20, -11, 40, 22, 5, cv.g("wood", "deep")) + cv.rect(-3, 10, 6, 46, 3, cv.g("wood")) + cv.rect(-20, -11, 6, 22, 3, PAL["wood"][2])
    return out + cv.group(head, cx - 4, cy - 18, 1, -32)


def globe(cv, cx, cy):
    out = cv.circle(cx, cy, 33, cv.rad("globe", [(0, "#8EE1E5"), (1, "#14707A")], .38, .3, .85))
    out += cv.path("M%s %s q10 -16 20 -6 q6 10 -6 16 q-12 4 -14 -10 Z" % (cx - 22, cy - 6), fill="#62CFA3", op=.9)
    out += cv.path("M%s %s q12 -6 16 8 q-2 14 -12 10 q-8 -6 -4 -18 Z" % (cx + 8, cy + 4), fill="#62CFA3", op=.9)
    out += cv.ellipse(cx, cy, 14, 33, "none", stroke="#FFFFFF", sw=1.3, op=.55) + cv.line(cx - 33, cy, cx + 33, cy, "#FFFFFF", 1.3, op=.55)
    return out + cv.circle(cx, cy, 33, "none", stroke="#0F7C84", sw=1.6)


def leaf(cv, cx, cy):
    out = cv.path("M%s %s C%s %s %s %s %s %s C%s %s %s %s %s %s Z" % (cx - 28, cy + 26, cx - 34, cy - 16, cx + 6, cy - 36, cx + 32, cy - 32,
                                                                      cx + 36, cy - 4, cx + 6, cy + 30, cx - 28, cy + 26), fill=cv.g("green"), stroke=PAL["green"][2], sw=1.6)
    return out + cv.path("M%s %s Q%s %s %s %s" % (cx - 28, cy + 26, cx - 4, cy + 4, cx + 22, cy - 24), stroke="#FFFFFF", sw=2.4, op=.8) + cv.path("M%s %s L%s %s" % (cx - 28, cy + 26, cx - 36, cy + 36), stroke=PAL["green"][2], sw=3)


@illustration("tech-impact")
def _impact():
    cv = Canvas(800, 500).backdrop()
    spec = [("Ethical", "plum", scales, ("AI bias and fairness", "privacy and surveillance", "who is responsible for harm")),
            ("Legal", "sky", gavel, ("Data Protection Act and GDPR", "Computer Misuse Act", "Copyright, Designs & Patents Act")),
            ("Cultural", "sun", globe, ("the digital divide", "how social media changes us", "jobs changed by automation")),
            ("Environmental", "green", leaf, ("e-waste and rare materials", "energy used by data centres", "remote work saves travel"))]
    for n, (title, col, icon, bullets) in enumerate(spec):
        x, y = (14, 406)[n % 2], (34, 262)[n // 2]
        cv.add(P.card(cv, x, y, 380, 212, 20, title, col))
        cv.add(P.badge(cv, x + 22, y + 24, n + 1))
        cv.add(cv.circle(x + 66, y + 112, 52, "var(--il-band)"))
        cv.add(icon(cv, x + 66, y + 112))
        for i, t in enumerate(bullets):
            yy = y + 66 + i * 46
            cv.add(P.tick(cv, x + 136, yy + 6, 9), cv.text(x + 154, yy + 11, t, 13, 700, anchor="start", cls="il-ink"))
    return figure(
        "tech-impact", cv, "The four kinds of impact of technology: ethical, legal, cultural and environmental",
        "The four categories of impact that technology has, one card each. Ethical, shown as a set of scales: AI bias and fairness, privacy "
        "and surveillance, and who is responsible for harm. Legal, shown as a gavel: the Data Protection Act and GDPR, the Computer Misuse Act, "
        "and the Copyright, Designs and Patents Act. Cultural, shown as a globe: the digital divide, how social media changes us, and jobs "
        "changed by automation. Environmental, shown as a leaf: e-waste and rare materials, the energy used by data centres, and the fact "
        "that remote work saves travel.",
        ["Ethical: questions of right and wrong, such as fairness, privacy and responsibility.", "Legal: the laws that apply, which you must be able to name.",
         "Cultural: how technology changes the way people live, communicate and work.", "Environmental: the materials and energy technology uses, and the savings it can make."],
        "A strong answer names the category, gives a specific example, and says who is affected and how.")
