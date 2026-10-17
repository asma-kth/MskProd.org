"""Key Stage 3 illustrations: how a web page is built, app interface design, bias in AI,
two factor authentication and what to do about cyberbullying."""
import math

from .illus import Canvas, PAL, INK, ARROW, figure, illustration, _n
from . import illus_props as P
from . import illus_glyphs as G


def mono(cv, x, y, s, size, fill, anchor="start", weight=700):
    return cv.text(x, y, s, size, weight, anchor=anchor, fill=fill, mono=True)


def under(cv, x0, x1, y, color, label, size=12.5):
    """A bracket under a stretch of code with its name below it."""
    out = cv.path("M%s %s L%s %s L%s %s L%s %s" % (_n(x0), _n(y - 7), _n(x0), _n(y), _n(x1), _n(y), _n(x1), _n(y - 7)), stroke=color, sw=2.6)
    return out + cv.text((x0 + x1) / 2, y + 18, label, size, 750, cls="il-ink")


# ------------------------------------------------------------------ HTML and CSS

@illustration("html-css-anatomy")
def _html():
    cv = Canvas(800, 500).backdrop()
    CW = 0.6
    # an HTML element
    cv.add(P.card(cv, 14, 28, 380, 262, 20, "An HTML element", "coral"))
    cv.add(P.badge(cv, 36, 54, 1))
    cv.add(cv.rect(30, 70, 348, 66, 12, "#1C2831"))
    size = 30
    x0 = 44
    segs = [("<h1>", "#8CE3EA"), ("Welcome", "#EEF4F6"), ("</h1>", "#8CE3EA")]
    xs = []
    cx = x0
    for t, c in segs:
        cv.add(mono(cv, cx, 114, t, size, c))
        xs.append((cx, cx + len(t) * size * CW))
        cx += len(t) * size * CW
    cv.add(under(cv, xs[0][0], xs[0][1], 152, "#25B3BB", "opening tag"), under(cv, xs[1][0], xs[1][1], 152, "#FFC93C", "content"), under(cv, xs[2][0], xs[2][1], 152, "#25B3BB", "closing tag"))
    cv.add(cv.rect(30, 196, 348, 52, 12, "#1C2831"))
    size = 17
    x0 = 42
    segs = [("<a ", "#8CE3EA"), ("href", "#FFB3A8"), ("=", "#EEF4F6"), ('"page2.html"', "#9AF0B5"), (">", "#8CE3EA"), ("Next", "#EEF4F6"), ("</a>", "#8CE3EA")]
    cx = x0
    pos = []
    for t, c in segs:
        cv.add(mono(cv, cx, 228, t, size, c))
        pos.append((cx, cx + len(t) * size * CW))
        cx += len(t) * size * CW
    cv.add(cv.text(pos[1][0], 266, "attribute name", 12.5, 750, anchor="start", cls="il-ink"), cv.text(pos[3][1], 266, "its value", 12.5, 750, anchor="end", cls="il-ink"))
    cv.add(cv.line((pos[1][0] + pos[1][1]) / 2, 236, (pos[1][0] + pos[1][1]) / 2, 252, "#F77F72", 2.4), cv.line((pos[3][0] + pos[3][1]) / 2, 236, (pos[3][0] + pos[3][1]) / 2, 252, "#66B8EC", 2.4))
    # a CSS rule
    cv.add(P.card(cv, 406, 28, 380, 262, 20, "A CSS rule", "teal"))
    cv.add(P.badge(cv, 428, 54, 2))
    cv.add(cv.rect(422, 70, 348, 150, 12, "#1C2831"))
    size = 26
    cv.add(mono(cv, 440, 108, "h1", size, "#D9BEFF"), mono(cv, 440 + 3 * size * CW, 108, "{", size, "#EEF4F6"))
    cv.add(mono(cv, 470, 148, "color", size, "#8CE3EA"), mono(cv, 470 + 5 * size * CW, 148, ":", size, "#EEF4F6"), mono(cv, 470 + 7 * size * CW, 148, "teal", size, "#FFDA8A"), mono(cv, 470 + 11 * size * CW, 148, ";", size, "#EEF4F6"))
    cv.add(mono(cv, 440, 190, "}", size, "#EEF4F6"))
    cv.add(cv.text(432, 244, "selector", 12.5, 750, anchor="start", cls="il-ink"), cv.text(470 + 2.5 * size * CW + 8, 244, "property", 12.5, 750, cls="il-ink"), cv.text(470 + 9 * size * CW, 244, "value", 12.5, 750, cls="il-ink"))
    for xx, col in ((440 + 1 * size * CW, "#D9BEFF"), (470 + 2.5 * size * CW, "#8CE3EA"), (470 + 9 * size * CW, "#FFDA8A")):
        cv.add(cv.line(xx, 226, xx, 232, col, 2.6))
    cv.add(cv.text(596, 264, "the selector says what to style,", 12.5, 650, cls="il-ink2"), cv.text(596, 281, "each declaration is property: value;", 12.5, 650, cls="il-ink2"))
    # the page they make
    for k, (x, title, col, styled) in enumerate(((14, "HTML only: the structure", "sky", False), (416, "HTML and CSS: the style", "mint", True))):
        cv.add(P.card(cv, x, 316, 370, 168, 20, title, col))
        cv.add(cv.rect(x + 20, 340, 330, 130, 8, "#FFFFFF" if not styled else "#F4F4F4", stroke="#B9C6CE", sw=1.4))
        cv.add(cv.rect(x + 20, 340, 330, 20, 8, "#DCE8EE"), cv.rect(x + 20, 350, 330, 10, 0, "#DCE8EE"))
        for i, c in enumerate(("#FF7B72", "#FFCB47", "#5BD58B")):
            cv.add(cv.circle(x + 34 + i * 12, 350, 3.4, c))
        if not styled:
            cv.add('<text x="%s" y="%s" font-size="26" font-weight="700" font-family="Georgia, serif" fill="#111111">Welcome</text>' % (x + 34, 396))
            cv.add('<text x="%s" y="%s" font-size="13.5" font-family="Georgia, serif" fill="#111111">This is a paragraph of text.</text>' % (x + 34, 424))
            cv.add('<text x="%s" y="%s" font-size="13.5" font-family="Georgia, serif" fill="#0000CC" text-decoration="underline">Go to page two</text>' % (x + 34, 448))
        else:
            cv.add(cv.text(x + 185, 396, "Welcome", 26, 800, fill="#03747B"))
            cv.add(cv.text(x + 185, 424, "This is a paragraph of text.", 13.5, 500, fill="#222222"))
            cv.add(cv.rect(x + 122, 436, 126, 24, 12, "#03747B"), cv.text(x + 185, 452, "Go to page two", 13, 750, fill="#FFFFFF"))
    cv.add(P.arrow(cv, [(392, 400), (414, 400)], PAL["teal"][2], 4, 11))
    cv.add(P.badge(cv, 36, 318, 3))
    return figure(
        "html-css-anatomy", cv, "The parts of an HTML element and a CSS rule, and the page with and without style",
        "How a web page is described. An HTML element is made of an opening tag, the content and a closing tag: h1, Welcome, slash h1. A tag can "
        "have an attribute, such as href equals page2.html on a link, which has a name and a value. A CSS rule has a selector, which says what to "
        "style, here h1, and declarations in curly brackets, each a property and a value ending in a semicolon, here color colon teal. Below, "
        "the same page is shown with HTML only, which gives the structure with the browser's plain default look, and with HTML and CSS, "
        "where the heading is centred and teal and the link is a button.",
        ["HTML marks up the structure. An element has an opening tag, content and a closing tag, and a tag can carry attributes.",
         "CSS describes the style. A rule has a selector, and declarations that are each a property and a value.",
         "The same HTML looks plain on its own and is transformed by a stylesheet."],
        "HTML says what things are. CSS says what they look like.")


# ------------------------------------------------------------------ interface design

def callout(cv, x, y, w, n, title, sub, to, side):
    """A numbered note with a leader line to the thing it is about."""
    out = P.card(cv, x, y, w, 62, 14)
    out += P.badge(cv, x + 24, y + 31, n, "deep", 14)
    out += cv.text(x + 48, y + 28, title, 14.5, 750, anchor="start", cls="il-ink") + cv.text(x + 48, y + 47, sub, 12.5, 650, anchor="start", cls="il-ink2")
    sx = x + w if side == "L" else x
    mx = (sx + to[0]) / 2
    out = cv.path("M%s %s L%s %s L%s %s" % (sx, y + 31, _n(mx), y + 31, to[0], to[1]), stroke="#0F7C84", sw=2, dash="3 5") + out + cv.circle(to[0], to[1], 4.5, "#0F7C84")
    return out


@illustration("app-ui-design")
def _ui():
    cv = Canvas(800, 500).backdrop()
    px, py, pw, ph = 306, 16, 188, 470
    cv.add(cv.shadow(px + pw / 2, py + ph + 6, 100, 8, .25))
    cv.add(cv.rect(px, py, pw, ph, 30, cv.g("dark", "deep")), cv.rect(px + 8, py + 14, pw - 16, ph - 28, 20, "#FFFFFF"))
    sx, sy, sw_ = px + 8, py + 14, pw - 16
    cv.add(cv.rect(sx, sy, sw_, 44, 20, cv.g("teal")), cv.rect(sx, sy + 22, sw_, 22, 0, cv.g("teal")))
    cv.add(cv.path("M%s %s L%s %s L%s %s" % (sx + 24, sy + 14, sx + 14, sy + 22, sx + 24, sy + 30), stroke=INK, sw=3.2), cv.text(sx + sw_ / 2 + 8, sy + 28, "Quiz", 16, 800, fill=INK))
    cv.add(cv.text(sx + sw_ / 2, sy + 90, "What is 7 × 8?", 17, 800, fill=INK))
    for i, (t, sel) in enumerate((("54", False), ("56", True), ("58", False))):
        yy = sy + 112 + i * 54
        cv.add(cv.rect(sx + 14, yy, sw_ - 28, 44, 12, "#1E7344" if sel else "#FFFFFF", stroke="#1F5F9A" if not sel else "#14532D", sw=2.4))
        cv.add(cv.text(sx + sw_ / 2 - (8 if sel else 0), yy + 29, t, 18, 800, fill="#FFFFFF" if sel else INK, mono=True))
        if sel:
            cv.add(cv.circle(sx + sw_ / 2 + 22, yy + 22, 10, "#FFFFFF"), cv.path("M%s %s L%s %s L%s %s" % (sx + sw_ / 2 + 17, yy + 22, sx + sw_ / 2 + 21, yy + 26, sx + sw_ / 2 + 28, yy + 17), stroke="#1E6B42", sw=2.6))
    cv.add(cv.rect(sx + 14, sy + 280, sw_ - 28, 30, 10, "#E1F5EA", stroke="#2E8B57", sw=1.6), cv.text(sx + sw_ / 2, sy + 300, "Correct! +10 points", 13.5, 800, fill="#14532D"))
    cv.add(cv.text(sx + sw_ / 2, sy + 336, "Undo last answer", 13.5, 700, fill="#1F5F9A"), cv.line(sx + 44, sy + 340, sx + sw_ - 44, sy + 340, "#1F5F9A", 1.4))
    cv.add(cv.rect(sx + 14, sy + 360, sw_ - 28, 46, 14, "#1F5F9A"), cv.text(sx + sw_ / 2, sy + 389, "Next question", 16, 800, fill="#FFFFFF"))
    # notes
    L, R = 14, 520
    cv.add(callout(cv, L, 60, 270, 1, "Consistency", "back is always top left", (sx + 20, sy + 22), "L"))
    cv.add(callout(cv, L, 190, 270, 2, "Accessibility", "big targets, strong contrast", (sx + 14, sy + 166), "L"))
    cv.add(callout(cv, L, 340, 270, 3, "Clarity", "buttons say what they do", (sx + 14, sy + 383), "L"))
    cv.add(callout(cv, R, 60, 266, 4, "Simplicity", "one question at a time", (sx + sw_ - 14, sy + 90), "R"))
    cv.add(callout(cv, R, 190, 266, 5, "Feedback", "every tap gets a response", (sx + sw_ - 14, sy + 295), "R"))
    cv.add(callout(cv, R, 340, 266, 6, "Forgiveness", "mistakes can be undone", (sx + sw_ - 44, sy + 336), "R"))
    return figure(
        "app-ui-design", cv, "A quiz app screen with six interface design principles marked on it",
        "A phone showing a quiz app, with six design principles pointing at parts of the screen. Consistency: the back button is always in the "
        "top left. Accessibility: the answer buttons are big targets with strong contrast. Clarity: the button says Next question, which "
        "says what it does. Simplicity: there is one question at a time. Feedback: after the answer is tapped the screen says Correct, plus 10 "
        "points. Forgiveness: an Undo last answer link means mistakes can be undone.",
        ["Consistency: the same action looks and behaves the same everywhere.", "Accessibility: large tap targets and strong colour contrast.",
         "Clarity: buttons say what they do, so Next question beats OK.", "Simplicity: fewer options, one thing at a time.",
         "Feedback: every action gets a visible response.", "Forgiveness: mistakes can be undone."],
        "An interface succeeds when the user does not have to think about it.")


# ------------------------------------------------------------------ bias in AI

def apple(cv, cx, cy, r=13):
    out = cv.circle(cx, cy, r, cv.g("red", "deep")) + cv.circle(cx - r * .3, cy - r * .3, r * .28, "#FFFFFF", op=.35)
    return out + cv.path("M%s %s q1 -5 4 -7" % (cx, cy - r + 1), stroke="#5B3A1B", sw=2) + cv.path("M%s %s q7 -7 11 -1 q-6 5 -11 1" % (cx + 1, cy - r - 3), fill="#41B56D")


def pear(cv, cx, cy, r=13):
    cmds = [("M", (0, -1.15)), ("C", (.5, -1.1), (.6, -.3), (.9, .1)), ("C", (1.3, .8), (.6, 1.3), (0, 1.3)),
            ("C", (-.6, 1.3), (-1.3, .8), (-.9, .1)), ("C", (-.6, -.3), (-.5, -1.1), (0, -1.15)), ("Z",)]
    d = " ".join(c[0] + " ".join("%s %s" % (_n(cx + px * r), _n(cy + py * r)) for px, py in c[1:]) for c in cmds)
    return cv.path(d, fill=cv.g("green", "deep"), stroke=PAL["green"][2], sw=1) + cv.circle(cx - r * .3, cy + r * .2, r * .22, "#FFFFFF", op=.3) + cv.path("M%s %s l2 -6" % (_n(cx), _n(cy - r * 1.15)), stroke="#5B3A1B", sw=2)


@illustration("ai-bias")
def _bias():
    cv = Canvas(800, 500).backdrop()
    cv.add(P.card(cv, 14, 30, 250, 290, 20, "1  Training data", "sky"))
    spots = [(i % 5, i // 5) for i in range(20)]
    pears = {7, 18}
    for i, (c, r) in enumerate(spots):
        x, y = 50 + c * 42, 80 + r * 50
        cv.add(pear(cv, x, y + 2, 12) if i in pears else apple(cv, x, y + 2, 13))
    cv.add(cv.text(139, 296, "18 apples, only 2 pears", 14, 750, cls="il-ink"))
    cv.add(P.arrow(cv, [(268, 175), (296, 175)], PAL["teal"][2], 5, 13))
    cv.add(P.card(cv, 300, 30, 200, 290, 20, "2  The model", "teal"))
    cv.add(G.machine(cv, 330, 120, 140, 110, "Sorter", "teal", "learns patterns"))
    cv.add(cv.text(400, 296, "it copies its data", 14, 750, cls="il-ink"))
    cv.add(P.arrow(cv, [(504, 175), (532, 175)], PAL["teal"][2], 5, 13))
    cv.add(P.card(cv, 536, 30, 250, 290, 20, "3  How often it is right", "coral"))
    for i, (name, pct, col, fn) in enumerate((("apples", 98, "green", apple), ("pears", 40, "red", pear))):
        y = 110 + i * 92
        cv.add(fn(cv, 576, y + 8, 14))
        cv.add(cv.text(604, y - 6, name, 14, 750, anchor="start", cls="il-ink"))
        cv.add(cv.rect(604, y + 4, 160, 18, 9, "var(--il-band)", stroke="var(--il-line)", sw=1), cv.rect(604, y + 4, 160 * pct / 100.0, 18, 9, cv.g(col)))
        cv.add(cv.text(604, y + 42, "%d%% right" % pct, 15, 800, anchor="start", cls="il-ink", mono=True))
    # the fix
    cv.add(P.card(cv, 14, 342, 772, 140, 20))
    cv.add(G.warning(cv, 54, 388, 1.1))
    cv.add(cv.text(90, 380, "The system is not prejudiced. It copies the patterns in its data.", 16, 800, anchor="start", cls="il-ink"))
    cv.add(cv.text(90, 406, "If the data under-represents a group, the system works worse for that group,", 13.5, 650, anchor="start", cls="il-ink2"))
    cv.add(cv.text(90, 426, "and the answers still look neutral and mathematical.", 13.5, 650, anchor="start", cls="il-ink2"))
    cv.add(P.tick(cv, 54, 456, 11), cv.text(76, 461, "The fix: more varied training data, and testing every group.", 14.5, 750, anchor="start", cls="il-ink"))
    cv.add(P.badge(cv, 36, 54, 1), P.badge(cv, 322, 54, 2), P.badge(cv, 558, 54, 3))
    return figure(
        "ai-bias", cv, "A sorting model trained mostly on apples is much worse at pears",
        "How bias gets into an AI system. The training data has twenty pieces of fruit but only two of them are pears: eighteen apples and two "
        "pears. The model learns the patterns in that data. When tested it is right 98 percent of the time for apples but only 40 percent of the "
        "time for pears. The system is not prejudiced, it copies the patterns in its data. If the data under-represents a group, the system "
        "works worse for that group while its answers still look neutral. The fix is more varied training data and testing every group.",
        ["The training data is unbalanced: 18 apples and only 2 pears.", "The model copies the patterns it finds in its data.",
         "So it is right 98% of the time for apples but only 40% for pears."],
        "Real examples include face recognition that is less accurate for groups missing from its training photos.")


# ------------------------------------------------------------------ two factor authentication

@illustration("two-factor")
def _twofa():
    cv = Canvas(800, 500).backdrop()
    # step 1: something you know
    cv.add(P.card(cv, 14, 30, 244, 270, 20, "Something you know", "sun", .5))
    cv.add(cv.rect(34, 78, 204, 150, 12, "#FFFFFF", stroke="#B9C6CE", sw=1.6))
    cv.add(cv.text(50, 104, "Username", 12, 700, anchor="start", fill="#4A6470"), cv.rect(50, 110, 172, 26, 6, "#F1F5F8", stroke="#B9C6CE", sw=1.2), cv.text(58, 128, "sam_k", 13.5, 700, anchor="start", fill=INK, mono=True))
    cv.add(cv.text(50, 156, "Password", 12, 700, anchor="start", fill="#4A6470"), cv.rect(50, 162, 172, 26, 6, "#F1F5F8", stroke="#B9C6CE", sw=1.2))
    for i in range(10):
        cv.add(cv.circle(64 + i * 14, 175, 4, INK))
    cv.add(cv.rect(50, 196, 172, 24, 12, "#1F5F9A"), cv.text(136, 213, "Log in", 13.5, 800, fill="#FFFFFF"))
    cv.add(cv.text(136, 266, "a password can be stolen", 13.5, 700, cls="il-ink"))
    cv.add(P.arrow(cv, [(262, 165), (292, 165)], PAL["teal"][2], 5, 13))
    # step 2: something you have
    cv.add(P.card(cv, 296, 30, 218, 270, 20, "Something you have", "coral", .5))
    cv.add(P.phone(cv, 372, 70, 1.5, "", 64, 120))
    cv.add(cv.text(420, 132, "Your code", 11.5, 700, fill=INK))
    cv.add(cv.text(420, 164, "482 913", 17, 800, fill=INK, mono=True))
    cv.add(cv.circle(420, 194, 8, "none", stroke="#2F82C0", sw=3), cv.path("M420 186 A8 8 0 0 1 428 194", stroke="#F0584B", sw=3))
    cv.add(cv.text(405, 266, "a code only your phone has", 13.5, 700, cls="il-ink"))
    cv.add(P.arrow(cv, [(518, 165), (548, 165)], PAL["teal"][2], 5, 13))
    # step 3: you are in
    cv.add(P.card(cv, 552, 30, 234, 270, 20, "You are in", "mint", .5))
    cv.add(cv.circle(669, 140, 54, cv.g("green", "deep")), cv.path("M644 142 L663 161 L696 120", stroke="#FFFFFF", sw=11))
    cv.add(cv.text(669, 232, "Welcome back, Sam", 15, 800, cls="il-ink"))
    cv.add(cv.text(669, 266, "both checks passed", 13.5, 700, cls="il-ink2"))
    # the thief
    cv.add(P.card(cv, 14, 326, 772, 156, 20, "What a thief with only the password gets", "red", .5))
    cv.add(P.person(cv, 44, 346, .72, "light", "black", "slate", "short", False, "smile", True))
    cv.add(cv.rect(130, 388, 88, 46, 8, "#FFF4C2", stroke="#DFA000", sw=1.4), cv.text(174, 407, "stolen", 11.5, 700, fill=INK), cv.text(174, 424, "pass1234", 13.5, 800, fill=INK, mono=True))
    cv.add(P.arrow(cv, [(224, 411), (330, 411)], ARROW, 4.5, 12))
    cv.add(cv.rect(340, 376, 140, 70, 12, "#FFFFFF", stroke="#B9C6CE", sw=1.6), cv.text(410, 400, "Enter the code", 13, 750, fill=INK), cv.rect(360, 410, 100, 24, 6, "#F1F5F8", stroke="#B9C6CE", sw=1.2), cv.text(410, 427, "? ? ? ? ? ?", 13.5, 800, fill=INK, mono=True))
    cv.add(P.cross(cv, 500, 411, 15), cv.text(528, 406, "Blocked.", 17, 800, anchor="start", cls="il-bad"), cv.text(528, 428, "A stolen password alone is not enough.", 13.5, 700, anchor="start", cls="il-ink"))
    cv.add(P.badge(cv, 36, 52, 1), P.badge(cv, 318, 52, 2), P.badge(cv, 574, 52, 3))
    return figure(
        "two-factor", cv, "Two factor authentication: a password and a code from your phone",
        "How two factor authentication works. Step one is something you know: you type your username and password. Step two is something you "
        "have: a code, here 482 913, appears on your phone and you type it in. Step three is you are in. Underneath, a thief wearing a hood "
        "has a stolen password, pass1234. They get past step one but are blocked at the screen that asks for the code, because the code is "
        "only on your phone. A stolen password alone is not enough.",
        ["Something you know: your username and password.", "Something you have: a code sent to, or made by, your phone.",
         "Only when both are right are you let in. A thief with just the password is stopped at step 2."],
        "Turn on two factor authentication wherever it is offered, and never share the code.")


# ------------------------------------------------------------------ cyberbullying

@illustration("report-it")
def _report():
    cv = Canvas(800, 500).backdrop()
    cols = [("1", "Do not reply", "A reply is what the bully wants.", "coral"), ("2", "Screenshot it", "Evidence matters. Deleted posts cannot be reported.", "sky"),
            ("3", "Block and report", "Use the block and report buttons on the platform.", "plum"), ("4", "Tell an adult", "A teacher, parent or carer you trust.", "mint")]
    for i, (n, title, sub, col) in enumerate(cols):
        x = 14 + i * 195
        cv.add(P.card(cv, x, 30, 183, 344, 20, title, col))
        cv.add(P.badge(cv, x + 24, 54, int(n)))
        cx = x + 91
        cv.add(cv.circle(cx, 150, 62, "var(--il-band)"))
        if i == 0:
            cv.add(G.bubble(cv, cx - 38, 118, 76, 48, ["..."], tail=(-14, 34), size=22))
            cv.add(P.cross(cv, cx + 30, 116, 17))
        elif i == 1:
            cv.add(P.phone(cv, cx - 32, 96, .9))
            cv.add(cv.path("M%s %s l0 -10 l10 0 M%s %s l0 -10 l-10 0 M%s %s l0 10 l10 0 M%s %s l0 10 l-10 0" % (cx - 40, 110, cx + 40, 110, cx - 40, 190, cx + 40, 190), stroke="#2F82C0", sw=3))
        elif i == 2:
            cv.add(cv.circle(cx, 150, 36, "none", stroke="#BA352D", sw=9), cv.line(cx - 25, 125, cx + 25, 175, "#BA352D", 9))
            cv.add(G.flag(cv, cx + 30, 100, 1.0, "coral"))
        else:
            cv.add(P.person(cv, cx - 44, 118, .42, "tan", "brown", "plum", "short"), P.person(cv, cx + 4, 130, .34, "light", "black", "coral", "short"))
            cv.add(cv.path("M%s %s c-8 -8 -18 4 0 14 c18 -10 8 -22 0 -14" % (cx, 112), fill="#F0584B"))
        for j, ln in enumerate(wrap(sub, 22)):
            cv.add(cv.text(cx, 266 + j * 20, ln, 13.5, 650, cls="il-ink"))
    cv.add(P.card(cv, 14, 396, 772, 80, 18))
    cv.add(cv.circle(60, 436, 22, cv.g("green", "deep")), cv.path("M49 436 L57 444 L72 427", stroke="#FFFFFF", sw=5))
    cv.add(cv.text(96, 430, "You are not in trouble for reporting something.", 17, 800, anchor="start", cls="il-ink"))
    cv.add(cv.text(96, 456, "The person doing it is the one with the problem.", 14, 650, anchor="start", cls="il-ink2"))
    return figure(
        "report-it", cv, "Four steps when you see or get cyberbullying: do not reply, screenshot, block and report, tell an adult",
        "Four steps to take if cyberbullying is happening to you or you see it happening. One: do not reply, because a reply is what the bully "
        "wants. Two: screenshot everything, because evidence matters and deleted posts cannot be reported. Three: block the person and report "
        "them using the platform's buttons. Four: tell an adult you trust, such as a teacher, a parent or a carer. A reminder says you are not "
        "in trouble for reporting something, and the person doing it is the one with the problem.",
        ["Do not reply. A response is what the bully wants.", "Screenshot everything as evidence, before anything is deleted.",
         "Block the person and report them on the platform.", "Tell an adult you trust."],
        "You are never in trouble for reporting.")


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
