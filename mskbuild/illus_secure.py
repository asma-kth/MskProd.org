"""Illustrations for cyber security: the threats, a phishing email, the layers of defence
and what makes a password strong."""
import math

from .illus import Canvas, PAL, INK, ARROW, figure, illustration, _n
from . import illus_props as P
from . import illus_glyphs as G

GRID_X = (14, 277, 540)
GRID_Y = (36, 266)


# ------------------------------------------------------------------ the threats

def icon_virus(cv, x, y):
    return P.doc(cv, x + 1, y - 2, .36, 62, 80, 0, "paper") + G.bug(cv, x + 17, y + 17, .55)


def icon_worm(cv, x, y):
    out = cv.path("M%s %s L%s %s L%s %s" % (x + 3, y + 21, x + 13, y + 6, x + 24, y + 18), stroke="#BA352D", sw=2.2)
    for px, py in ((x + 3, y + 21), (x + 13, y + 6), (x + 24, y + 18)):
        out += cv.circle(px, py, 4.4, "#F0584B", stroke="#8F2923", sw=1.2)
    return out


def icon_gift(cv, x, y):
    out = cv.rect(x + 2, y + 11, 22, 15, 3, cv.g("sun"), stroke=PAL["sun"][2], sw=1.2)
    out += cv.rect(x, y + 6, 26, 7, 3, cv.g("sun"), stroke=PAL["sun"][2], sw=1.2) + cv.rect(x + 11, y + 6, 4, 20, 0, "#F0584B")
    out += cv.path("M%s %s q-7 -9 -1 -9 q5 0 1 9 q6 -9 9 -4 q1 5 -9 4" % (x + 13, y + 6), stroke="#F0584B", sw=1.8)
    return out


def icon_eye(cv, x, y):
    out = cv.path("M%s %s Q%s %s %s %s Q%s %s %s %s Z" % (x, y + 14, x + 13, y, x + 26, y + 14, x + 13, y + 28, x, y + 14), fill="#FFFFFF", stroke=INK, sw=1.6)
    return out + cv.circle(x + 13, y + 14, 6.2, cv.g("plum", "deep")) + cv.circle(x + 13, y + 14, 2.6, "#10151A")


@illustration("cyber-threats")
def _threats():
    cv = Canvas(800, 500).backdrop()
    spec = [("Malware", "coral"), ("Social engineering", "plum"), ("Brute force", "sun"), ("Denial of service", "teal"), ("SQL injection", "sky"), ("Data interception", "mint")]
    for n, (title, col) in enumerate(spec):
        x, y = GRID_X[n % 3], GRID_Y[n // 3]
        cv.add(P.card(cv, x, y, 246, 200, 18, title, col))
        cv.add(P.badge(cv, x + 16, y + 24, n + 1))
        cx = x + 123
        if n == 0:
            rows = [(icon_virus, "virus: needs a host file"), (icon_worm, "worm: spreads by itself"), (icon_gift, "trojan: looks harmless"),
                    (lambda c, a, b: P.padlock(c, a + 3, b - 1, .36), "ransomware: locks your files"), (icon_eye, "spyware: watches you")]
            for i, (icon, label) in enumerate(rows):
                yy = y + 46 + i * 28
                cv.add(icon(cv, x + 16, yy), cv.text(x + 52, yy + 16, label, 13, 700, anchor="start", cls="il-ink"))
        elif n == 1:
            cv.add(G.bubble(cv, x + 16, y + 38, 214, 46, ["\"I'm from IT. What's", "your password?\""], tail=(36, 52), size=13.5))
            cv.add(P.person(cv, x + 126, y + 86, .5, "tan", "brown", "plum", "short"))
            for i, t in enumerate(("phishing", "blagging", "shouldering")):
                cv.add(P.pill(cv, x + 16, y + 112 + i * 25, t, "lilac", 12.5, 10, 22, 750, anchor="start"))
            cv.add(cv.text(cx, y + 186, "tricks people, not computers", 13.5, 700, cls="il-ink"))
        elif n == 2:
            for i, (code, ok) in enumerate((("0000", False), ("0001", False), ("....", None), ("7316", True))):
                yy = y + 46 + i * 31
                cv.add(cv.rect(x + 16, yy, 84, 25, 6, "#FFFFFF", stroke="#9FB3BE", sw=1.4), cv.text(x + 58, yy + 18, code, 14, 800, fill=INK, mono=True))
                if ok is True:
                    cv.add(P.tick(cv, x + 118, yy + 12, 9))
                elif ok is False:
                    cv.add(P.cross(cv, x + 118, yy + 12, 9))
            cv.add(P.padlock(cv, x + 156, y + 56, 1.3, "sun"))
            cv.add(cv.text(cx, y + 186, "tries every combination", 13.5, 700, cls="il-ink"))
        elif n == 3:
            for i in range(6):
                bx, by = x + 16 + (i % 2) * 38, y + 46 + (i // 2) * 34
                cv.add(cv.rect(bx, by, 24, 17, 3, cv.g("red")), cv.rect(bx + 5, by + 19, 14, 3, 1.5, PAL["red"][2]))
                cv.add(cv.line(bx + 24, by + 9, x + 150, y + 90, "#BA352D", 1.8, op=.55))
            cv.add(P.server_rack(cv, x + 150, y + 74, 1, .62))
            cv.add(P.pill(cv, x + 190, y + 62, "BUSY", "red", 12, 8, 20, 800))
            cv.add(P.pill(cv, x + 16, y + 160, "you", "green", 12.5, 10, 24, 750, anchor="start"), P.arrow(cv, [(x + 62, y + 160), (x + 118, y + 160)], "#248049", 3.5, 10), P.cross(cv, x + 132, y + 160, 10))
            cv.add(cv.text(cx + 40, y + 186, "floods it with requests", 13.5, 700, cls="il-ink"))
        elif n == 4:
            cv.add(cv.text(x + 16, y + 50, "username", 12, 650, anchor="start", cls="il-ink2"))
            cv.add(cv.rect(x + 16, y + 56, 174, 28, 7, "#FFFFFF", stroke="#9FB3BE", sw=1.5), cv.text(x + 26, y + 75, "' OR '1'='1", 13.5, 800, anchor="start", fill=INK, mono=True))
            cv.add(P.arrow(cv, [(x + 70, y + 88), (x + 70, y + 108)], ARROW, 3.5, 10))
            cv.add(G.cylinder(cv, x + 70, y + 136, 56, 52, "sky", 3))
            cv.add(P.arrow(cv, [(x + 108, y + 134), (x + 126, y + 134)], "#BA352D", 3.5, 10))
            for i, t in enumerate(("names", "passwords", "cards")):
                cv.add(cv.rect(x + 134, y + 106 + i * 21, 92, 18, 5, "#FDE7E4", stroke="#BA352D", sw=1), cv.text(x + 180, y + 119 + i * 21, t, 11.5, 750, fill="#8F2923"))
            cv.add(cv.text(cx, y + 186, "code typed into a form", 13.5, 700, cls="il-ink"))
        else:
            cv.add(P.laptop(cv, x + 8, y + 108, .46))
            cv.add(P.router(cv, x + 172, y + 116, .46))
            cv.add(cv.path("M%s %s L%s %s" % (x + 108, y + 140, x + 170, y + 140), stroke=ARROW, sw=2.2, dash="4 5"))
            cv.add(P.envelope(cv, x + 102, y + 126, .5, 70, 48))
            cv.add(P.person(cv, x + 92, y + 40, .38, "light", "black", "slate", "short", False, "smile", True))
            cv.add(P.magnifier(cv, x + 136, y + 108, .62, 16))
            cv.add(cv.text(cx, y + 186, "reads data in transit", 13.5, 700, cls="il-ink"))
    return figure(
        "cyber-threats", cv, "Six cyber security threats: malware, social engineering, brute force, denial of service, SQL injection and interception",
        "Six common cyber security threats, one card each. Malware is software written to cause harm: a virus needs a host file, a worm spreads by "
        "itself, a trojan looks harmless, ransomware locks your files and spyware watches you. Social engineering tricks people instead of "
        "computers, for example a caller who says they are from IT and asks for a password; phishing, blagging and shouldering are all social "
        "engineering. A brute force attack tries every possible combination, for example every code from 0000 upwards, until one works. A "
        "denial of service attack floods a server with requests from many machines so that a real user cannot get through. SQL injection types "
        "database code such as ' OR '1'='1 into a form so that the database hands over names, passwords and card numbers. Data interception "
        "reads data while it travels, for example from an unencrypted wireless connection.",
        ["Malware: virus, worm, trojan, ransomware and spyware.", "Social engineering: phishing, blagging and shouldering trick people instead of computers.",
         "Brute force: try every combination until one works.", "Denial of service: flood a server so real users cannot get in.",
         "SQL injection: database code typed into an input box.", "Interception: reading data as it travels, for example on public Wi-Fi."],
        "Every threat has a matching defence. Learn them as pairs: the picture on the next page of defences shows which goes with which.")


# ------------------------------------------------------------------ a phishing email

def flag(cv, x, y, n):
    out = cv.circle(x, y + 1.5, 13.5, "#10303A", op=.2) + cv.circle(x, y, 13.5, "#FFFFFF") + cv.circle(x, y, 11.2, cv.g("red", "deep"))
    return out + cv.text(x, y + 5, str(n), 14, 800, fill="#FFFFFF")


@illustration("phishing-email")
def _phish():
    cv = Canvas(800, 500).backdrop()
    ex, ey, ew, eh = 14, 22, 504, 456
    cv.add(cv.shadow(ex + ew / 2, ey + eh + 6, 230, 8, .18))
    cv.add(cv.rect(ex, ey, ew, eh, 14, "#FFFFFF", stroke="#B9C6CE", sw=1.6))
    cv.add(cv.rect(ex, ey, ew, 34, 14, cv.g("teal")), cv.rect(ex, ey + 18, ew, 16, 0, cv.g("teal")))
    for i, c in enumerate(("#FF7B72", "#FFCB47", "#5BD58B")):
        cv.add(cv.circle(ex + 18 + i * 16, ey + 17, 4.6, c))
    cv.add(cv.text(ex + 80, ey + 22, "Inbox", 13.5, 750, anchor="start", fill=INK))
    # header
    grey = "#4A6470"
    cv.add(cv.text(ex + 20, ey + 62, "From:", 13.5, 700, anchor="start", fill=grey), cv.text(ex + 82, ey + 62, "Bank Support <support@bank-secure-login.example>", 13.5, 650, anchor="start", fill=INK))
    cv.add(cv.text(ex + 20, ey + 88, "Subject:", 13.5, 700, anchor="start", fill=grey), cv.text(ex + 82, ey + 88, "URGENT: your account will be closed", 13.5, 650, anchor="start", fill=INK))
    cv.add(cv.line(ex + 14, ey + 102, ex + ew - 14, ey + 102, "#D5DEE4", 1.6))
    # body
    for (yy, t) in ((ey + 136, "Dear Customer,"), (ey + 190, "You must verify your details within 24 hours"), (ey + 214, "or your account will be closed.")):
        cv.add(cv.text(ex + 24, yy, t, 14, 600, anchor="start", fill=INK))
    bad = ' fill="#BA352D" font-weight="800"'
    cv.add('<text x="%s" y="%s" font-size="14" font-weight="600" fill="%s">We have noticed <tspan%s>unusal</tspan> activity on your <tspan%s>acount</tspan>.</text>'
           % (ex + 24, ey + 166, INK, bad, bad))
    cv.add(cv.rect(ex + 22, ey + 236, 196, 40, 9, "#1F5F9A"), cv.text(ex + 120, ey + 262, "Verify my account now", 14.5, 750, fill="#FFFFFF"))
    cv.add(cv.rect(ex + 22, ey + 284, 306, 26, 6, INK), cv.text(ex + 32, ey + 302, "http://bank-secure-login.example/verify", 12, 700, anchor="start", fill="#FFFFFF", mono=True))
    cv.add(cv.rect(ex + 22, ey + 326, 168, 36, 9, "#F1F5F8", stroke="#B9C6CE", sw=1.4))
    cv.add(cv.path("M%s %s l0 -14 a5 5 0 0 1 10 0 l0 18 a8 8 0 0 1 -16 0 l0 -16" % (ex + 40, ey + 349), stroke="#6F8794", sw=1.8))
    cv.add(cv.text(ex + 62, ey + 349, "invoice.exe", 13.5, 750, anchor="start", fill=INK, mono=True))
    cv.add(cv.text(ex + 24, ey + 404, "The Security Team", 14, 600, anchor="start", fill=INK))
    # what is wrong, marked on the email
    marks = [(ey + 55, "From"), (ey + 83, "Subject"), (ey + 130, "Greeting"), (ey + 160, "Spelling"), (ey + 297, "Link"), (ey + 346, "Attachment")]
    for i, (yy, _) in enumerate(marks):
        cv.add(flag(cv, ex + ew - 26, yy, i + 1))
    # the list of flags
    cv.add(P.card(cv, 540, 22, 246, 456, 18, "Six red flags", "coral"))
    items = [("Strange sender address", "does not match the real bank"), ("Urgent threat", "pressure to act without thinking"), ("Generic greeting", "\"Dear Customer\", not your name"),
             ("Spelling mistakes", "unusal, acount"), ("Link does not match", "hover to see where it goes"), ("Unexpected attachment", ".exe files can run malware")]
    for i, (a_, b_) in enumerate(items):
        yy = 74 + i * 66
        cv.add(flag(cv, 566, yy + 2, i + 1))
        cv.add(cv.text(590, yy, a_, 14.5, 750, anchor="start", cls="il-ink"), cv.text(590, yy + 21, b_, 12.5, 650, anchor="start", cls="il-ink2"))
    return figure(
        "phishing-email", cv, "A phishing email with its six warning signs marked",
        "A fake email pretending to be from a bank, with its six warning signs numbered. One: the sender address, support at bank secure login "
        "dot example, does not match the real bank. Two: the subject is urgent, saying your account will be closed, which pressures you to act "
        "without thinking. Three: the greeting is generic, Dear Customer, instead of your name. Four: there are spelling mistakes, unusal and "
        "acount. Five: the button says Verify my account now but when you hover over it the address it really goes to is a different website. "
        "Six: there is an unexpected attachment called invoice dot exe, and a file ending in dot exe can run malware.",
        ["The sender's address does not match the real organisation.", "The message is urgent and threatens you, to stop you thinking.",
         "It says Dear Customer instead of using your name.", "Spelling and grammar mistakes.",
         "The link goes somewhere different to what it says, which you can see by hovering over it.", "An attachment you were not expecting, here a program file."],
        "Phishing works on trust and panic. Stop, check the sender and the link, and never open an unexpected attachment.")


# ------------------------------------------------------------------ the layers of defence

@illustration("cyber-defences")
def _defences():
    cv = Canvas(800, 500).backdrop()
    cx, cy = 240, 258
    layers = [(222, "Physical security", "slate"), (188, "Firewall", "coral"), (154, "Anti-malware", "sun"), (120, "Access levels", "mint"), (86, "Passwords and 2FA", "sky")]
    for r, name, col in layers:
        cv.add(cv.circle(cx, cy, r + 2, "#10303A", op=.07), cv.circle(cx, cy, r, "var(--il-card)", stroke=PAL[col][2], sw=3.2))
        cv.add(cv.rect(cx - len(name) * 4.1 - 10, cy - r + 8, len(name) * 8.2 + 20, 22, 11, "var(--il-bg1)", op=.9))
        cv.add(cv.text(cx, cy - r + 24, name, 13.5, 750, cls="il-ink"))
    cv.add(cv.circle(cx, cy, 52, cv.g("deep", "deep"), stroke="#FFFFFF", sw=3))
    cv.add(G.cylinder(cv, cx, cy - 4, 44, 44, "sky", 2), P.padlock(cv, cx + 4, cy + 4, .5, "sun"))
    cv.add(cv.text(cx, cy + 74, "encrypted data", 12.5, 750, cls="il-ink"))
    # which defence answers which threat
    cv.add(P.card(cv, 500, 24, 286, 458, 18, "Defence for each threat", "teal"))
    pairs = [("Brute force", "long password, 2FA, limit tries"), ("Phishing", "staff training, spam filters"), ("Malware", "anti-malware, keep it updated"),
             ("SQL injection", "validate every input"), ("Interception", "encrypt the data"), ("Unauthorised access", "firewall, access levels")]
    for i, (threat, fix) in enumerate(pairs):
        yy = 74 + i * 66
        cv.add(P.pill(cv, 522, yy, threat, "coral", 12.5, 10, 24, 750, anchor="start"))
        cv.add(P.arrow(cv, [(536, yy + 14), (536, yy + 26)], ARROW, 2.5, 7))
        cv.add(P.tick(cv, 524, yy + 38, 8), cv.text(540, yy + 43, fix, 13.5, 700, anchor="start", cls="il-ink"))
    cv.add(P.badge(cv, 40, 70, 1), P.badge(cv, 518, 28, 2))
    return figure(
        "cyber-defences", cv, "Layers of defence around encrypted data, and the defence that answers each threat",
        "Defence in depth drawn as rings around the data. From the outside in the rings are physical security, a firewall, anti-malware "
        "software, user access levels, and passwords with two factor authentication, and at the centre the data itself is encrypted. An attacker "
        "has to get through every layer. On the right each threat is matched with its defence: brute force is stopped by a long password, "
        "two factor authentication and a limit on login attempts; phishing by staff training and spam filters; malware by anti-malware "
        "software that is kept up to date; SQL injection by validating every input; interception by encrypting the data; and unauthorised "
        "access by a firewall and user access levels.",
        ["No single defence is enough, so several layers are used. An attacker has to get past all of them.",
         "Match each threat to the defence that answers it. This pairing is asked in the exam."],
        "Encryption does not stop data being intercepted. It makes intercepted data useless.")


# ------------------------------------------------------------------ password strength

@illustration("password-strength")
def _passwords():
    cv = Canvas(800, 500).backdrop()
    rows = [("sunny", "a common word", "26 letters, 5 places", "12 million", 7, "under a second", "red"),
            ("k7$Rm2!x", "8 random characters", "95 symbols, 8 places", "6.6 quadrillion", 15.8, "about 77 days", "sun"),
            ("river-dust-lamp-oak-fern", "5 random words", "a 7776 word list, 5 words", "2.8 × 10^19", 19.4, "about 900 years", "green")]
    cv.add(cv.text(400, 30, "At a billion guesses a second", 15, 750, cls="il-ink2"))
    for i, (pw, kind, space, count, expo, time_, col) in enumerate(rows):
        y = 52 + i * 118
        cv.add(P.card(cv, 14, y, 772, 104, 18))
        cv.add(P.badge(cv, 32, y + 20, i + 1))
        cv.add(cv.rect(54, y + 34, 238, 36, 9, "#FFFFFF", stroke="#9FB3BE", sw=1.6), cv.text(173, y + 58, pw, 15 if len(pw) > 12 else 19, 800, fill=INK, mono=True))
        cv.add(cv.text(173, y + 90, kind, 13, 650, cls="il-ink2"))
        # the number of possibilities, drawn as a bar on a log scale
        cv.add(cv.text(318, y + 46, "%s possibilities" % count, 14.5, 750, anchor="start", cls="il-ink"))
        cv.add(cv.rect(318, y + 58, 260, 16, 8, "var(--il-band)", stroke="var(--il-line)", sw=1))
        cv.add(cv.rect(318, y + 58, 260 * expo / 20.0, 16, 8, cv.g("teal" if col != "red" else "coral")))
        cv.add(cv.text(318, y + 92, space, 12.5, 650, anchor="start", cls="il-ink2"))
        # the time
        cv.add(P.lift(cv, 606, y + 22, 160, 60, col, 12, 5, hl=False))
        cv.add(cv.text(686, y + 46, "cracked in", 12.5, 650, fill=INK if col != "red" else "#FFFFFF"), cv.text(686, y + 68, time_, 15, 800, fill=INK if col != "red" else "#FFFFFF"))
    cv.add(cv.text(400, 420, "Longer beats clever: every extra character multiplies the work.", 16, 750, cls="il-ink"))
    cv.add(cv.text(400, 446, "Never reuse a password, and add two factor authentication so that a stolen password is not enough.", 13.5, 650, cls="il-ink2"))
    cv.add(cv.text(400, 470, "Bar length shows how many digits the number of possibilities has.", 12.5, 650, cls="il-ink2"))
    return figure(
        "password-strength", cv, "Three passwords compared by how many guesses an attacker needs",
        "Three passwords, each with the number of possibilities an attacker must search and how long that takes at a billion guesses a second. "
        "The first, sunny, is a common word, so it is found from a word list in under a second. The second, k7$Rm2!x, is eight random "
        "characters chosen from 95 symbols, which is about 6.6 quadrillion possibilities and takes about 77 days. The third, river-dust-lamp-oak-fern, "
        "is five random words from a list of 7776 words, which is about 2.8 times 10 to the 19, and takes about 900 years. Length matters "
        "more than cleverness, because every extra character multiplies the number of possibilities, and a password should never be reused.",
        ["A common word is cracked at once, however long it feels to type.", "Eight random characters from 95 symbols: about 6.6 quadrillion possibilities.",
         "Five random words from a list: far more possibilities, and easier to remember."],
        "A strong password is long, random and used once. Add two factor authentication for anything that matters.")
