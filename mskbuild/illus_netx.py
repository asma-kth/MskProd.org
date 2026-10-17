"""More network illustrations: what limits performance, IP against MAC addresses, and how email travels."""
import math

from .illus import Canvas, PAL, INK, ARROW, figure, illustration, _n
from . import illus_props as P
from . import illus_glyphs as G

GRID_X = (14, 277, 540)
GRID_Y = (36, 266)


# ------------------------------------------------------------------ what limits performance

def pipe(cv, x, y, w, h, color="sky"):
    out = cv.rect(x, y + 4, w, h, h / 2.4, PAL[color][2]) + cv.rect(x, y, w, h, h / 2.4, cv.g(color))
    return out + cv.rect(x + 8, y + 3, w - 16, max(3, h * .16), 2, "#FFFFFF", op=.35)


def packet(cv, x, y, s=9):
    return cv.rect(x, y, s, s, 2.4, cv.g("sun"), stroke=PAL["sun"][2], sw=.9)


@illustration("network-factors")
def _factors():
    cv = Canvas(800, 500).backdrop()
    spec = [("Bandwidth", "teal"), ("Number of users", "coral"), ("Transmission media", "sun"), ("Interference", "plum"), ("Latency", "mint"), ("Not the same thing", "sky")]
    for n, (title, col) in enumerate(spec):
        x, y = GRID_X[n % 3], GRID_Y[n // 3]
        cv.add(P.card(cv, x, y, 246, 200, 18, title, col))
        cv.add(P.badge(cv, x + 16, y + 24, n + 1))
        cx = x + 123
        if n == 0:
            cv.add(cv.text(x + 18, y + 48, "high bandwidth", 12.5, 700, anchor="start", cls="il-ink2"))
            cv.add(pipe(cv, x + 16, y + 54, 214, 48, "sky"))
            for r in range(3):
                for k in range(8):
                    cv.add(packet(cv, x + 26 + k * 25, y + 61 + r * 13))
            cv.add(cv.text(x + 18, y + 128, "low bandwidth", 12.5, 700, anchor="start", cls="il-ink2"))
            cv.add(pipe(cv, x + 16, y + 134, 214, 22, "sky"))
            for k in range(3):
                cv.add(packet(cv, x + 30 + k * 66, y + 140))
            cv.add(cv.text(cx, y + 186, "capacity: data per second", 13.5, 700, cls="il-ink"))
        elif n == 1:
            for i, (lab, parts) in enumerate((("1 user", 1), ("3 users", 3), ("6 users", 6))):
                yy = y + 50 + i * 42
                cv.add(cv.text(x + 18, yy, lab, 12.5, 700, anchor="start", cls="il-ink2"))
                gap = 4
                bw = (214 - gap * (parts - 1)) / parts
                for k in range(parts):
                    cv.add(cv.rect(x + 16 + k * (bw + gap), yy + 7, bw, 14, 5, cv.g("teal")))
            cv.add(cv.text(cx, y + 186, "the connection is shared", 13.5, 700, cls="il-ink"))
        elif n == 2:
            fade = cv.lin("copper", [(0, "#D9762B"), (1, "#D9762B", .12)], 0, 0, 1, 0)
            cv.add(cv.text(x + 18, y + 50, "copper: fades over distance", 12.5, 700, anchor="start", cls="il-ink2"))
            cv.add(cv.rect(x + 16, y + 58, 214, 12, 6, fade))
            cv.add(cv.text(x + 18, y + 108, "fibre: light stays strong", 12.5, 700, anchor="start", cls="il-ink2"))
            cv.add(cv.rect(x + 16, y + 116, 214, 12, 6, cv.g("teal", "deep")))
            for k in range(5):
                cv.add(glow(cv, x + 36 + k * 44, y + 122, 9, "#FFFFFF", .95))
            cv.add(cv.text(cx, y + 186, "fibre carries more, further", 13.5, 700, cls="il-ink"))
        elif n == 3:
            cv.add(P.router(cv, x + 6, y + 70, .4))
            for k, r in enumerate((16, 28, 40)):
                cv.add(cv.path("M%s %s A%s %s 0 0 1 %s %s" % (x + 64 + r * .55, y + 78 - r * .8, r, r, x + 64 + r * .55, y + 78 + r * .8), stroke="#25B3BB", sw=3, op=[.9, .6, .3][k]))
            for i in range(3):
                cv.add(cv.rect(x + 112 + (i % 2) * 6, y + 56 + i * 20, 32, 17, 3, cv.g("coral"), stroke=PAL["coral"][2], sw=1))
            cv.add(P.laptop(cv, x + 168, y + 72, .28))
            for i, ok in enumerate((True, False, True)):
                bx = x + 30 + i * 70
                cv.add(cv.rect(bx, y + 138, 50, 24, 7, "#FFFFFF", stroke="#9FB3BE", sw=1.4), cv.text(bx + 25, y + 155, str(i + 1), 13, 800, fill=INK, mono=True))
                cv.add(P.tick(cv, bx + 40, y + 168, 7) if ok else P.cross(cv, bx + 40, y + 168, 7))
            cv.add(cv.text(cx, y + 190, "lost packets are sent again", 13.5, 700, cls="il-ink"))
        elif n == 4:
            cv.add(G.stopwatch(cv, x + 62, y + 98, 38, -35))
            cv.add(cv.text(x + 118, y + 70, "cable: 20 ms", 13, 750, anchor="start", cls="il-ink"))
            cv.add(cv.rect(x + 118, y + 77, 22, 14, 5, cv.g("teal")))
            cv.add(cv.text(x + 118, y + 122, "satellite: 600 ms", 13, 750, anchor="start", cls="il-ink"))
            cv.add(cv.rect(x + 118, y + 129, 106, 14, 5, cv.g("coral")))
            cv.add(cv.text(x + 118, y + 158, "(not to scale)", 11.5, 650, anchor="start", cls="il-ink2"))
            cv.add(cv.text(cx, y + 190, "the delay before data arrives", 13.5, 700, cls="il-ink"))
        else:
            cv.add(cv.text(x + 18, y + 50, "lanes = bandwidth", 12.5, 750, anchor="start", cls="il-ink"))
            cv.add(cv.rect(x + 16, y + 56, 214, 78, 8, "#4A5A64"))
            for k in (1, 2):
                cv.add(cv.line(x + 22, y + 56 + k * 26, x + 224, y + 56 + k * 26, "#FFFFFF", 2, dash="10 9", op=.75))
            for lane, cx_, col in ((0, 40, "coral"), (1, 120, "sky"), (2, 70, "sun"), (0, 160, "mint"), (2, 170, "plum")):
                cv.add(cv.rect(x + cx_, y + 62 + lane * 26, 30, 15, 5, cv.g(col)))
            cv.add(P.arrow(cv, [(x + 18, y + 150), (x + 226, y + 150)], ARROW, 3, 9))
            cv.add(cv.text(x + 18, y + 172, "long road = latency", 12.5, 750, anchor="start", cls="il-ink"))
    return figure(
        "network-factors", cv, "Six ideas about network performance: bandwidth, users, media, interference, latency and why bandwidth is not speed",
        "Six cards about what affects network performance. Bandwidth is the capacity of a connection, how much data it can carry each second, "
        "drawn as a wide pipe carrying many packets and a narrow pipe carrying few. The connection is shared, so with one user the whole bar is "
        "theirs, with three users each gets a third and with six users each gets a sixth. Fibre optic cable carries more data further than "
        "copper, whose signal fades over distance. Wireless signals are weakened by walls and distance, and a lost packet must be sent again. "
        "Latency is the delay before data arrives, around 20 milliseconds on a cable but around 600 on a satellite link. Bandwidth is like the "
        "number of lanes on a road and latency is like the length of the road, so a connection can have a lot of one and little of the other.",
        ["Bandwidth is the capacity of a connection: how much data it can carry each second.",
         "Bandwidth is shared, so the more users there are, the less each one gets.",
         "Fibre carries more data further than copper, and copper fades over distance.",
         "Walls, distance and other devices weaken wireless signals, and lost packets are sent again.",
         "Latency is the delay before data arrives. A satellite link has a long delay even if its bandwidth is large.",
         "Bandwidth is like the number of lanes. Latency is like the length of the journey."],
        "Bandwidth is capacity and latency is delay. A fast connection needs both to be good.")


def glow(cv, cx, cy, r, color, o=.8):
    return cv.circle(cx, cy, r, cv.rad("glow%s" % color.lstrip("#"), [(0, color, o), (1, color, 0)]))


# ------------------------------------------------------------------ IP against MAC

def house(cv, x, y):
    out = cv.rect(x + 8, y + 26, 56, 38, 4, cv.g("wood"), stroke=PAL["wood"][2], sw=1.2)
    out += cv.poly([(x, y + 30), (x + 36, y), (x + 72, y + 30)], cv.g("coral", "deep"))
    out += cv.rect(x + 30, y + 40, 14, 24, 3, PAL["wood"][2]) + cv.rect(x + 14, y + 36, 11, 11, 2, "#DDF3FA") + cv.rect(x + 47, y + 36, 11, 11, 2, "#DDF3FA")
    return out


def school(cv, x, y):
    out = cv.rect(x, y + 14, 80, 50, 4, cv.g("sky"), stroke=PAL["sky"][2], sw=1.2)
    out += cv.rect(x + 30, y, 20, 20, 3, cv.g("sky", "deep")) + cv.rect(x + 36, y + 40, 8, 24, 2, PAL["sky"][2])
    for k in (0, 1, 2, 3):
        out += cv.rect(x + 8 + (k % 2) * 52 + (k // 2) * 0, y + 24 + (k // 2) * 18, 12, 10, 2, "#DDF3FA")
    return out + G.flag(cv, x + 40, y - 26, .8, "coral")


@illustration("ip-mac")
def _ipmac():
    cv = Canvas(800, 500).backdrop()
    # the laptop, with its fixed MAC address
    cv.add(P.laptop(cv, 290, 54, 1.0))
    cv.add(P.pill(cv, 400, 236, "MAC 3C:22:FB:9A:41:7E", "green", 14, 12, 28, 800))
    cv.add(cv.text(400, 266, "burned in by the manufacturer", 12.5, 650, cls="il-ink2"))
    # the two networks it moves between
    for x, title, col, icon, ip in ((14, "At home", "teal", house, "192.168.1.23"), (546, "At school", "sky", school, "10.4.7.52")):
        cv.add(P.card(cv, x, 24, 240, 250, 18, title, col))
        cv.add(icon(cv, x + 84, 80))
        cv.add(cv.text(x + 120, 190, "the network gives it", 13, 650, cls="il-ink2"))
        cv.add(P.pill(cv, x + 120, 224, "IP " + ip, "sun", 15, 14, 30, 800))
    cv.add(P.arrow(cv, [(284, 140), (262, 140)], ARROW, 4, 11), P.arrow(cv, [(516, 140), (538, 140)], ARROW, 4, 11))
    cv.add(cv.text(400, 24, "same laptop, two networks", 13.5, 700, cls="il-ink2"))
    # the comparison
    cv.add(P.card(cv, 14, 298, 772, 192, 18))
    cv.add(P.pill(cv, 450, 320, "MAC address", "green", 15, 16, 28, 800), P.pill(cv, 660, 320, "IP address", "sun", 15, 16, 28, 800))
    rows = [("Assigned by", "the manufacturer", "the network"), ("Changes?", "never", "when you change network"),
            ("Looks like", "6 hex pairs, 48 bits", "4 numbers, 32 bits (IPv4)"), ("Used for", "delivery inside one network", "routing between networks")]
    for i, (lab, a_, b_) in enumerate(rows):
        y = 344 + i * 33
        if i % 2 == 0:
            cv.add(cv.rect(26, y, 748, 31, 8, "var(--il-band)"))
        cv.add(cv.text(42, y + 21, lab, 14, 750, anchor="start", cls="il-ink"))
        cv.add(cv.text(450, y + 21, a_, 14, 650, cls="il-ink"), cv.text(660, y + 21, b_, 14, 650, cls="il-ink"))
    cv.add(P.badge(cv, 330, 60, 1), P.badge(cv, 36, 46, 2), P.badge(cv, 36, 300, 3))
    return figure(
        "ip-mac", cv, "The same laptop on two networks: its MAC address stays, its IP address changes",
        "A laptop with a MAC address, 3C:22:FB:9A:41:7E, burned in by the manufacturer. At home the network gives it the IP address 192.168.1.23. "
        "At school the network gives it a different IP address, 10.4.7.52. The MAC address stays the same on both networks, but the IP address "
        "changes whenever it joins a different network. A table compares them. A MAC address is assigned by the manufacturer, never changes, "
        "looks like six pairs of hex digits and is 48 bits long, and is used for delivery inside one network. An IP address is assigned by "
        "the network, changes when you change network, is four numbers or 32 bits in IPv4, and is used for routing between networks.",
        ["The MAC address belongs to the hardware, so it stays the same wherever the laptop goes.",
         "The IP address is given by the network, so the same laptop has a different one at home and at school.",
         "MAC: manufacturer, never changes, local delivery. IP: network, changes, routing between networks."],
        "Think of the MAC address as a serial number and the IP address as a postal address.")


# ------------------------------------------------------------------ how an email travels

def mailbox(cv, x, y, n=3, ghost=False, w=84):
    out = cv.rect(x, y, w, 54, 8, "var(--il-band)", stroke="var(--il-line)", sw=1.4, dash="5 4" if ghost else None)
    for i in range(n):
        env = P.envelope(cv, x + 7 + i * 25, y + 12, .3, 70, 48)
        out += '<g opacity="%s">%s</g>' % (.3 if ghost else 1, env)
    return out


@illustration("email-protocols")
def _email():
    cv = Canvas(800, 500).backdrop()
    # the journey
    nodes = [(76, "sender", "laptop"), (276, "sender's mail server", "server"), (500, "recipient's mail server", "server"), (716, "recipient", "phone")]
    for cx, lab, kind in nodes:
        if kind == "laptop":
            cv.add(P.laptop(cv, cx - 55, 70, .5))
        elif kind == "server":
            cv.add(P.server_rack(cv, cx - 42, 60, 1, .65))
        else:
            cv.add(P.phone(cv, cx - 18, 52, .62))
            cv.add(P.laptop(cv, cx + 8, 82, .3))
        cv.add(cv.text(cx, 168, lab, 13.5, 750, cls="il-ink"))
    for (a_, b_, label, col) in ((136, 216, "SMTP", "sky"), (336, 440, "SMTP", "sky"), (560, 660, "POP or IMAP", "mint")):
        cv.add(P.arrow(cv, [(a_, 104), (b_, 104)], PAL[col][2], 5, 13))
        cv.add(P.pill(cv, (a_ + b_) / 2, 80, label, col, 13.5, 12, 26, 800))
    cv.add(P.envelope(cv, 150, 126, .5, 70, 48))
    cv.add(P.badge(cv, 30, 40, 1))
    # POP
    cv.add(P.card(cv, 14, 214, 380, 274, 20, "POP: download, then delete", "coral"))
    cv.add(cv.text(60, 262, "mail server", 13, 700, cls="il-ink2"), cv.text(330, 262, "one laptop", 13, 700, cls="il-ink2"))
    cv.add(mailbox(cv, 30, 272, 3, True), P.arrow(cv, [(122, 296), (262, 296)], PAL["coral"][2], 5, 13))
    cv.add(cv.text(192, 286, "download", 12.5, 750, cls="il-ink"))
    cv.add(P.laptop(cv, 270, 270, .26), mailbox(cv, 276, 336, 3, False, 84))
    cv.add(P.cross(cv, 74, 346, 11), cv.text(92, 351, "removed from the server", 13, 700, anchor="start", cls="il-bad"))
    cv.add(cv.text(204, 432, "mail is only on the device that downloaded it", 13.5, 700, cls="il-ink"))
    cv.add(cv.text(204, 454, "good for: one device, little storage", 12.5, 650, cls="il-ink2"))
    cv.add(P.badge(cv, 36, 216, 2))
    # IMAP
    cv.add(P.card(cv, 406, 214, 380, 274, 20, "IMAP: keep it on the server", "mint"))
    cv.add(cv.text(452, 262, "mail server", 13, 700, cls="il-ink2"), cv.text(730, 262, "every device", 13, 700, cls="il-ink2"))
    cv.add(mailbox(cv, 422, 272, 3, False), P.arrow(cv, [(512, 292), (592, 292)], "#248049", 4, 11), P.arrow(cv, [(592, 312), (512, 312)], "#248049", 4, 11))
    cv.add(P.laptop(cv, 606, 270, .26), mailbox(cv, 612, 336, 3, False, 84))
    cv.add(P.phone(cv, 716, 270, .42), cv.text(742, 346, "same mail", 11.5, 650, cls="il-ink2"))
    cv.add(P.tick(cv, 466, 346, 11), cv.text(484, 351, "kept on the server", 13, 700, anchor="start", cls="il-ok"))
    cv.add(cv.text(596, 432, "every device shows the same mailbox", 13.5, 700, cls="il-ink"))
    cv.add(cv.text(596, 454, "good for: phone and laptop together", 12.5, 650, cls="il-ink2"))
    cv.add(P.badge(cv, 428, 216, 3))
    return figure(
        "email-protocols", cv, "How an email travels, and the difference between POP and IMAP",
        "The journey of an email. The sender's laptop uses SMTP to send the message to the sender's mail server. SMTP is used again to pass it "
        "to the recipient's mail server. The recipient then collects it with POP or IMAP. Below, the two ways of collecting mail are compared. "
        "With POP the mail is downloaded to one device and then removed from the server, so it only exists on the device that downloaded it. With "
        "IMAP the mail stays on the server and every device, such as a phone and a laptop, shows the same mailbox, so they stay in sync.",
        ["SMTP sends email, from the sender to their server and between mail servers.",
         "POP downloads mail and normally deletes it from the server, so it lives on one device.",
         "IMAP keeps mail on the server, so a phone and a laptop both show the same mailbox."],
        "SMTP sends. POP downloads and removes. IMAP keeps it on the server and in sync. Two devices means IMAP.")
