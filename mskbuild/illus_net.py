"""Networking illustrations."""
import math

from .illus import Canvas, PAL, INK, ARROW, figure, illustration, _n
from . import illus_props as P


# ------------------------------------------------------------ small glyphs

def g_browser(cv, cx, cy, c="#fff"):
    out = cv.rect(cx - 12, cy - 9, 24, 18, 3.5, "none", stroke=c, sw=2.2)
    out += cv.line(cx - 12, cy - 3, cx + 12, cy - 3, c, 2.2)
    out += cv.circle(cx - 7.5, cy - 6, 1.2, c) + cv.circle(cx - 3.5, cy - 6, 1.2, c)
    return out


def g_port(cv, cx, cy, c="#fff"):
    out = cv.rect(cx - 12, cy - 8, 24, 16, 3.5, "none", stroke=c, sw=2.2)
    out += cv.text(cx, cy + 4.6, "80", 12.5, 800, fill=c, mono=True)
    return out


def g_globe(cv, cx, cy, c="#fff"):
    out = cv.circle(cx, cy, 11, "none", stroke=c, sw=2.2)
    out += cv.ellipse(cx, cy, 4.6, 11, "none", stroke=c, sw=1.8)
    out += cv.line(cx - 11, cy, cx + 11, cy, c, 1.8)
    return out


def g_plug(cv, cx, cy, c="#fff"):
    out = cv.rect(cx - 10, cy - 8, 20, 15, 3, "none", stroke=c, sw=2.2)
    for k in (-5, 0, 5):
        out += cv.line(cx + k, cy - 3, cx + k, cy + 3, c, 1.8)
    out += cv.line(cx, cy + 7, cx, cy + 12, c, 2.2)
    return out


GLYPHS = [g_browser, g_port, g_globe, g_plug]


@illustration("tcp-ip-stack")
def _tcpip():
    cv = Canvas(800, 500).backdrop()
    layers = [
        ("Application", "HTTP · SMTP · DNS", "shows the page", "sky"),
        ("Transport", "TCP · UDP · ports", "puts the pieces in order", "teal"),
        ("Internet", "IP · addresses", "checks it is for me", "plum"),
        ("Link", "Wi-Fi · Ethernet · MAC", "reads the frame", "coral"),
    ]
    y0, step, th = 104, 76, 60
    # the two ends
    cv.add(P.laptop(cv, 36, 12, .4, P.browser_screen(cv, 31, 9, 158, 102, "chat", False) + cv.rect(44, 40, 70, 24, 10, "#25B3BB") + cv.rect(80, 76, 90, 24, 10, "#DCE8EE")),
           cv.text(142, 52, "Sender", 21, 700, anchor="start", cls="il-ink il-h"))
    cv.add(P.laptop(cv, 676, 12, .4, P.browser_screen(cv, 31, 9, 158, 102, "chat", False) + cv.rect(44, 40, 70, 24, 10, "#DCE8EE") + cv.rect(80, 76, 90, 24, 10, "#25B3BB")),
           cv.text(668, 52, "Receiver", 21, 700, anchor="end", cls="il-ink il-h"))
    cv.add(cv.text(400, 48, "What is on the wire", 15, 650, cls="il-ink2"))
    for i, (name, sub, sub2, col) in enumerate(layers):
        y = y0 + i * step
        # the band that ties a row together
        cv.add(P.band(cv, 14, y - 8, 772, th + 22, 18))
        for side in (0, 1):
            x = 26 if side == 0 else 550
            cv.add(P.lift(cv, x, y, 224, th, col, 14, 6))
            cv.add(cv.circle(x + 32, y + th / 2, 19, "#1F6FA8" if col == "sky" else PAL[col][2]))
            cv.add(GLYPHS[i](cv, x + 32, y + th / 2, "#FFFFFF"))
            tc = P._on(col)
            cv.add(cv.text(x + 60, y + 26, name, 19, 750, fill=tc, anchor="start"))
            cv.add(cv.text(x + 60, y + 46, sub if side == 0 else sub2, 13.5, 500, fill=tc, anchor="start"))
        # the data unit as it stands at this layer
        chips = [("DATA", "sky", 70)]
        if i >= 1: chips.insert(0, ("TCP", "teal", 46))
        if i >= 2: chips.insert(0, ("IP", "plum", 36))
        if i >= 3:
            chips.insert(0, ("MAC", "coral", 48))
            chips.append(("FCS", "coral", 42))
        total = sum(w for _, _, w in chips) + 4 * (len(chips) - 1)
        x = 400 - total / 2
        for label, col2, w in chips:
            cv.add(P.lift(cv, x, y + 6, w, 30, col2, 8, 4, hl=False))
            cv.add(cv.text(x + w / 2, y + 27, label, 14.5, 800, fill=P._on(col2)))
            x += w + 4
        cv.add(cv.text(400, y + 56, ["message", "segment", "packet", "frame"][i], 14, 600, cls="il-ink2"))
        # which way things move through the stack
        if i < 3:
            cv.add(cv.poly([(138 - 9, y + th + 4), (138 + 9, y + th + 4), (138, y + th + 14)], ARROW, op=.85))
            cv.add(cv.poly([(662 - 9, y + th + 14), (662 + 9, y + th + 14), (662, y + th + 4)], ARROW, op=.85))
    # the wire between the two link layers
    yb = y0 + 3 * step + th + 6
    wire = "M138 %d L138 %d Q138 %d 152 %d L648 %d Q662 %d 662 %d L662 %d" % (yb, yb + 38, yb + 52, yb + 52, yb + 52, yb + 52, yb + 38, yb)
    cv.add(P.cable(cv, wire, "slate", 9))
    cv.add(P.envelope(cv, 366, yb + 22, 1, 68, 44, "paper", "coral"))
    cv.add(P.pill(cv, 400, yb + 83, "cable or Wi-Fi: bits on the wire", "paper", 14.5))
    for (bx, by, n) in ((22, y0 - 8, 1), (260, y0 + step - 8, 2), (260, y0 + 2 * step - 8, 3), (260, y0 + 3 * step - 8, 4), (780, y0 - 8, 5)):
        pass
    cv.add(P.badge(cv, 30, y0 - 4, 1), P.badge(cv, 250, y0 + step - 4, 2), P.badge(cv, 250, y0 + 2 * step - 4, 3),
           P.badge(cv, 250, y0 + 3 * step - 4, 4), P.badge(cv, 770, y0 - 4, 5))
    return figure(
        "tcp-ip-stack", cv, "The TCP/IP model: a message wrapped on the way down and unwrapped on the way up",
        "Two stacks of four layers, the sender's on the left and the receiver's on the right, with the data between them. "
        "At the application layer, where HTTP, HTTPS, SMTP, IMAP and FTP live, the data is just the message. The transport layer splits it "
        "into segments and adds a TCP or UDP header carrying the port number. The internet layer wraps each segment in a packet and adds the "
        "source and destination IP addresses used for routing. The link layer wraps the packet in a frame carrying MAC addresses and a check "
        "value, and puts it on the cable or the wireless link. At the receiving computer the same four layers run in reverse: each strips off "
        "the wrapper it recognises and hands the rest up, so the application receives exactly the message that was sent. No layer needs to know "
        "how another layer does its job, which is the whole reason the model is split up this way.",
        ["Your message starts at the top, in the application.",
         "Transport splits it into segments and adds a port number.",
         "Internet wraps each segment in a packet and adds IP addresses.",
         "Link turns the packet into a frame with MAC addresses, and it goes out.",
         "At the other end the same four layers run in reverse, unwrapping it."],
        "Each layer wraps what the layer above handed it, and knows nothing about what is inside. That is why you can change the wifi for a cable without rewriting the web browser.")


# ---------------------------------------------------------- small helpers

def node(cv, cx, cy, r=24, color="sky", glyph=True):
    """A router drawn as a round button with four arrows on it."""
    out = cv.shadow(cx, cy + r + 4, r * .9, 4, .22)
    out += cv.circle(cx, cy + 5, r, PAL[color][2]) + cv.circle(cx, cy, r, cv.g(color))
    out += cv.circle(cx, cy - r * .35, r * .62, "#fff", op=.18)
    if glyph:
        k = r * .52
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            tx, ty = cx + dx * k, cy + dy * k
            out += cv.line(cx + dx * k * .25, cy + dy * k * .25, tx, ty, "#fff", 3)
            px, py = -dy, dx
            out += cv.poly([(tx + dx * 5, ty + dy * 5), (tx + px * 4.2, ty + py * 4.2), (tx - px * 4.2, ty - py * 4.2)], "#fff")
    return out


def mini_pc(cv, x, y, s=.3, dim=False):
    """A small laptop used as one device among several. (x, y) is its top left."""
    out = P.laptop(cv, x, y, s, cv.rect(31, 9, 158, 102, 5, cv.g("teal")) + cv.rect(44, 24, 70, 14, 4, "#fff", op=.55) + cv.rect(44, 46, 100, 10, 4, "#fff", op=.4))
    return cv.group(out, 0, 0, 1, extra=' opacity=".38"') if dim else out


@illustration("packet-journey")
def _packet_journey():
    cv = Canvas(800, 500).backdrop()
    R = {1: (306, 282), 2: (414, 138), 3: (414, 426), 4: (422, 282), 5: (540, 282)}
    edges = [(1, 2), (1, 4), (1, 3), (2, 5), (4, 5), (3, 5), (2, 4), (3, 4)]
    for a, b in edges:
        cv.add(P.cable(cv, "M%d %d L%d %d" % (R[a] + R[b]), "slate", 6))
    cv.add(P.cable(cv, "M%d %d L%d %d" % (R[5][0], R[5][1], 592, 282), "slate", 6))
    # routes
    routes = [("teal", [1, 2, 5], None), ("coral", [1, 4, 5], None), ("plum", [1, 3, 4, 5], "7 6"), ("sun", [1, 2, 4, 5], "2 9")]
    for col, path, dash in routes[:3]:
        d = "M" + " L".join("%d %d" % R[k] for k in path)
        cv.add(cv.path(d, stroke=PAL[col][1], sw=5, dash=dash, op=.95))
    # the link that failed
    mx, my = (R[3][0] + R[5][0]) / 2, (R[3][1] + R[5][1]) / 2
    cv.add(P.cross(cv, mx, my, 13))
    for k, (x, y) in R.items():
        cv.add(node(cv, x, y, 25, "sky" if k not in (1, 5) else "navy"))
    cv.add(cv.text(R[1][0], R[1][1] + 52, "router", 14, 600, cls="il-ink2"))
    cv.add(cv.text(R[5][0], R[5][1] + 52, "router", 14, 600, cls="il-ink2"))
    # envelopes in flight
    for n, col, (x, y) in ((4, "sun", (356, 190)), (1, "teal", (466, 190)), (2, "coral", (360, 268)), (3, "plum", (396, 346))):
        cv.add(P.envelope(cv, x - 24, y - 17, 1, 48, 34, "paper", col, n=n))
    # the sender
    cv.add(P.laptop(cv, 34, 54, .55, P.photo(cv, 58, 24, 104, 70)))
    cv.add(P.pill(cv, 94, 166, "Sender", "paper", 15))
    for i, col in enumerate(("teal", "coral", "plum", "sun")):
        cv.add(P.envelope(cv, 40 + i * 56, 196, 1, 48, 34, "paper", col, n=[1, 2, 3, 4][i]))
    cv.add(P.arrow(cv, [(252, 226), (280, 258)], ARROW, 4, 11))
    # one packet, opened up
    cv.add(P.card(cv, 14, 262, 218, 216, 16))
    cv.add(cv.text(123, 290, "Inside one packet", 16, 750, cls="il-ink il-h"))
    rows = [("To", "93.184.216.34", "sky"), ("From", "81.2.69.160", "mint"), ("Number", "2 of 4", "sun"), ("Check", "checksum", "lilac")]
    for i, (k, v, col) in enumerate(rows):
        yy = 304 + i * 32
        cv.add(cv.rect(26, yy, 70, 26, 8, cv.g(col)), cv.text(61, yy + 18, k, 14, 700, fill=P._on(col)))
        cv.add(cv.rect(100, yy, 120, 26, 8, "#FFFFFF", stroke="var(--il-line)", sw=1), cv.text(160, yy + 18, v, 13, 650, fill=INK, mono=True))
    cv.add(cv.rect(26, 436, 194, 30, 9, cv.lin("slicebg", [(0, "#8ED5F5"), (1, "#DDF3FB")])))
    cv.add(cv.path("M26 466 L26 454 Q50 438 78 452 L98 466 Z", fill="#5FC38C"), cv.text(88, 456, "a slice of the photo", 12.5, 650, fill=INK, anchor="start"))
    # the receiver
    cv.add(P.laptop(cv, 640, 54, .55, P.photo(cv, 58, 24, 104, 70)))
    cv.add(P.pill(cv, 700, 166, "Receiver", "paper", 15))
    cv.add(P.card(cv, 592, 192, 196, 286, 16))
    cv.add(cv.text(696, 220, "Arrive in any order", 14.5, 750, cls="il-ink il-h"))
    for i, (n, col) in enumerate(((2, "coral"), (1, "teal"), (4, "sun"), (3, "plum"))):
        cv.add(P.envelope(cv, 604 + i * 44, 236, 1, 40, 28, "paper", col, n=n))
    cv.add(P.arrow(cv, [(690, 276), (690, 316)], ARROW, 4, 11))
    cv.add(P.pill(cv, 690, 344, "numbers put them back", "paper", 13.5))
    for i, (n, col) in enumerate(((1, "teal"), (2, "coral"), (3, "plum"), (4, "sun"))):
        cv.add(P.envelope(cv, 604 + i * 44, 372, 1, 40, 28, "paper", col, n=n))
    cv.add(P.photo(cv, 640, 414, 100, 52))
    cv.add(P.pill(cv, 420, 482, "each router chooses the next hop for itself", "paper", 14))
    cv.add(P.badge(cv, 28, 190, 1), P.badge(cv, 26, 276, 2), P.badge(cv, 356, 120, 3), P.badge(cv, 602, 206, 4))
    return figure(
        "packet-journey", cv, "Packet switching: a photo split into numbered packets that take different routes",
        "A message is far too big to send as one lump, so the sender splits it into packets: a three megabyte photograph becomes roughly two "
        "thousand of them. The picture shows four. Each packet carries the destination address, the address it came from, its own sequence "
        "number and a slice of the data, plus a checksum used to spot corruption. Each router it reaches reads the destination and chooses the "
        "next hop for itself, so packets from the same message can take different routes: in the picture a failed link is crossed out and one "
        "packet has gone around it. The packets arrive out of order, and the sequence numbers let the receiving computer put them back "
        "together into the complete photo. Nothing reserves a line for the whole message.",
        ["Your message is too big to send in one go, so it is split into packets.",
         "Every packet carries the destination address and its own number.",
         "Each router picks the next hop, so packets can take different routes, even around a broken link.",
         "They arrive out of order, and the numbers put them back together."],
        "Nothing reserves a line for you. Every packet is handled on its own, and that is why the internet copes when part of it fails.")


@illustration("network-topologies")
def _topologies():
    cv = Canvas(800, 500).backdrop()
    panels = [("Star", "teal"), ("Mesh", "plum"), ("Bus", "coral")]
    for i, (name, col) in enumerate(panels):
        cv.add(P.card(cv, 14 + i * 262, 40, 250, 440, 20, name, col))
    pc = lambda cx, cy, dim=False: mini_pc(cv, cx - 33, cy - 24, .3, dim)
    # ---- star
    cx, cy, r = 139, 196, 88
    pts = [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)) * .92) for a in (-90, -18, 54, 126, 198)]
    for k, (x, y) in enumerate(pts):
        cv.add(P.cable(cv, "M%s %s L%s %s" % (_n(x), _n(y), cx, cy), "slate", 5))
    cv.add(P.net_switch(cv, cx - 46, cy - 14, .5, 6, "sky", 180))
    for k, (x, y) in enumerate(pts):
        cv.add(pc(x, y, k == 2))
    cv.add(P.cross(cv, (pts[2][0] + cx) / 2 - 2, (pts[2][1] + cy) / 2, 12))
    # ---- mesh
    cx2 = 139 + 262
    pts2 = [(cx2 + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)) * .92) for a in (-90, -18, 54, 126, 198)]
    for a in range(5):
        for b in range(a + 1, 5):
            if (a, b) == (0, 2):
                continue
            cv.add(P.cable(cv, "M%s %s L%s %s" % (_n(pts2[a][0]), _n(pts2[a][1]), _n(pts2[b][0]), _n(pts2[b][1])), "slate", 3.5))
    cv.add(cv.path("M%s %s L%s %s L%s %s" % (_n(pts2[0][0]), _n(pts2[0][1]), _n(pts2[1][0]), _n(pts2[1][1]), _n(pts2[2][0]), _n(pts2[2][1])), stroke=PAL["teal"][1], sw=5.5, dash="2 9"))
    cv.add(P.cross(cv, (pts2[0][0] + pts2[2][0]) / 2, (pts2[0][1] + pts2[2][1]) / 2, 12))
    for (x, y) in pts2:
        cv.add(pc(x, y))
    # ---- bus
    bx = 14 + 2 * 262
    by = 196
    cv.add(P.cable(cv, "M%d %d L%d %d" % (bx + 22, by, bx + 228, by), "dark", 10))
    cv.add(cv.rect(bx + 14, by - 14, 10, 28, 3, PAL["coral"][1]), cv.rect(bx + 226, by - 14, 10, 28, 3, PAL["coral"][1]))
    for k, (x, y) in enumerate(((bx + 56, 110), (bx + 126, 110), (bx + 196, 110), (bx + 90, 284), (bx + 162, 284))):
        cv.add(P.cable(cv, "M%d %d L%d %d" % (x, (y + 20) if y < by else (y - 10), x, by), "slate", 4))
        cv.add(pc(x, y))
    # ---- what each is good and bad at
    notes = [
        [("ok", "Its own cable each"), ("ok", "One failure drops one PC"), ("bad", "Switch is a weak point")],
        [("ok", "Many routes to take"), ("ok", "Survives failures"), ("bad", "Needs lots of cable")],
        [("ok", "Cheap, little cable"), ("bad", "One break stops all"), ("bad", "Everyone shares it")],
    ]
    for i, lst in enumerate(notes):
        for j, (kind, txt) in enumerate(lst):
            x0, y0 = 34 + i * 262, 338 + j * 44
            cv.add(P.tick(cv, x0 + 12, y0 + 12, 12) if kind == "ok" else P.cross(cv, x0 + 12, y0 + 12, 12))
            cv.add(cv.text(x0 + 32, y0 + 18, txt, 15.5, 600, anchor="start"))
    cv.add(P.badge(cv, 60, 40, 1), P.badge(cv, 218, 262, 2), P.badge(cv, 322, 40, 3), P.badge(cv, 470, 120, 4), P.badge(cv, 584, 40, 5))
    return figure(
        "network-topologies", cv, "Three network topologies: star, mesh and bus",
        "Three network topologies side by side. In a star, every device has its own cable running to a central switch, so performance stays "
        "high because no device shares its cable, and a single cable failure takes out only the one device attached to it; the costs are "
        "that it needs a lot of cable and that the switch is a single point of failure for the whole network. In a mesh, every device is "
        "connected directly to every other, so any one link can fail and the data simply goes a different way, which is why the internet is "
        "built as a mesh; the cost is a great deal of cable. In a bus, every device taps into one shared backbone cable with a terminator at "
        "each end: it is cheap and needs little cable, but a break in the backbone stops everyone and all the devices share its capacity.",
        ["Star: every device has its own cable to a central switch.",
         "If one cable fails, only that one device drops off.",
         "Mesh: every device connects to every other, with no centre at all.",
         "Any one link can fail and the data simply goes a different way.",
         "Bus: one shared backbone, and every device taps into it."],
        "Star for a school or an office, mesh for anything that has to survive a failure. The internet is a mesh.")


@illustration("lan-wan")
def _lan_wan():
    cv = Canvas(800, 500).backdrop()
    cv.add(cv.path("M0 414 Q200 386 400 404 T800 396 L800 500 L0 500 Z", fill=cv.lin("grass", [(0, "#C4EBD3"), (1, "#8FD4AF")])))
    cv.add(cv.path("M0 450 Q200 434 400 448 T800 444", stroke="#fff", sw=3, op=.5))

    def site(x0, name, tint):
        out = cv.shadow(x0 + 115, 412, 132, 9)
        out += cv.rect(x0, 176, 230, 236, 14, cv.lin("wall" + name, [(0, "#FFFFFF"), (1, "#E6EEF2")]))
        out += cv.rect(x0 - 8, 148, 246, 36, 10, cv.g(tint, "deep")) + cv.rect(x0 - 8, 148, 246, 13, 8, "#fff", op=.22)
        out += cv.text(x0 + 115, 173, name, 17, 800, fill="#fff", cls="")
        out += cv.rect(x0 + 14, 196, 202, 158, 10, cv.lin("room" + name, [(0, "#E4F6F8"), (1, "#D3EDF1")]), stroke=PAL[tint][1], sw=2)
        pcs = [(x0 + 22, 284), (x0 + 86, 302), (x0 + 150, 284)]
        for (px, py) in pcs:
            out += P.cable(cv, "M%d 234 L%d %d" % (x0 + 115, px + 33, py + 4), "slate", 4)
        out += P.net_switch(cv, x0 + 66, 208, .55, 6, "sky", 180)
        for (px, py) in pcs:
            out += mini_pc(cv, px, py, .3)
        out += cv.rect(x0 + 96, 358, 38, 54, 6, PAL["wood"][1]) + cv.circle(x0 + 126, 388, 3, "#fff")
        return out
    cv.add(site(34, "SCHOOL", "deep"), site(536, "OFFICE", "plum"))
    # the wide area network: cables run into the cloud and disappear behind it
    cv.add(P.cable(cv, "M272 164 Q296 164 338 118", "dark", 6), P.cable(cv, "M528 164 Q504 164 462 118", "dark", 6))
    cv.add(P.cloud(cv, 300, 30, 200, "paper", 1, "#BFDDEE"))
    cv.add(cv.text(400, 98, "WAN", 26, 800, fill="#2A5B6B", cls="il-h"))
    cv.add(cv.text(400, 118, "wide area network", 12.5, 600, fill="#4A6470"))
    cv.add(P.pill(cv, 400, 196, "telephone lines and fibre", "paper", 14.5))
    cv.add(P.pill(cv, 400, 236, "not owned by either site", "sun", 14.5, 12, 28, 700))
    cv.add(P.pixel_cat(cv, 372, 322, 58))
    cv.add(P.pill(cv, 400, 300, "not my cables!", "paper", 13.5))
    cv.add(P.pill(cv, 149, 442, "a LAN: one site, your own cables", "paper", 14.5))
    cv.add(P.pill(cv, 651, 442, "another LAN, its own cables", "paper", 14.5))
    cv.add(P.badge(cv, 34, 168, 1), P.badge(cv, 768, 168, 2), P.badge(cv, 300, 150, 3), P.badge(cv, 276, 236, 4))
    return figure(
        "lan-wan", cv, "A LAN in each building, joined across a WAN",
        "The difference between a local area network and a wide area network. A LAN covers a single geographical site, one building or one "
        "campus, and the organisation owns and maintains all of it: the switches, the cabling and the wireless access points. That is why a "
        "LAN is fast and cheap to run once it is installed. The picture shows a school with its own LAN and an office with its own LAN, each a "
        "switch with computers cabled to it. Joining the two sites makes a wide area network, drawn as a cloud between them, which runs over "
        "telephone lines, fibre or satellite that belong to a telecoms provider rather than to either site. The real difference is not size but "
        "who owns the connection.",
        ["A LAN covers one site: one building, one campus, cabling you own.",
         "A second site has its own LAN, with its own switch and its own cabling.",
         "Joining them makes a WAN, over lines nobody at either end owns.",
         "That is the real difference: not size, but who owns the connection."],
        "‘A WAN is bigger’ gets you nothing. ‘A WAN uses infrastructure the organisation does not own’ is the mark.")


def feature(cv, x, y, label, color, icon):
    """A labelled chip with a round icon on its left. (x, y) is the chip's left edge and centre."""
    w = 44 + len(label) * 8.6
    out = P.lift(cv, x, y - 18, w, 36, color, 18, 4, hl=False)
    out += cv.circle(x + 18, y, 15, "#FFFFFF")
    out += icon(x + 18, y)
    out += cv.text(x + 40, y + 5.5, label, 14.5, 700, fill=P._on(color), anchor="start")
    return out


@illustration("client-server")
def _client_server():
    cv = Canvas(800, 500).backdrop()
    cv.add(P.card(cv, 14, 40, 380, 440, 20, "Client–server", "teal"))
    cv.add(P.card(cv, 406, 40, 380, 440, 20, "Peer to peer", "plum"))
    # ---- client server
    clients = [(36, 326), (124, 342), (212, 342), (300, 326)]
    for (x, y) in clients:
        cv.add(P.cable(cv, "M%d %d Q%d %d %d %d" % (x + 39, y + 4, x + 39, 300, 121, 268), "slate", 4))
    cv.add(P.server_rack(cv, 56, 92, 3, .95))
    for (x, y) in clients:
        cv.add(mini_pc(cv, x, y, .36))
    ico_folder = lambda cx, cy: P.folder(cv, cx - 9, cy - 7, .22, "sun", 84, 62)
    ico_lock = lambda cx, cy: P.padlock(cv, cx - 7, cy - 9, .26, "mint")
    ico_disc = lambda cx, cy: P.disc(cv, cx, cy, 10)
    for i, (label, col, ic) in enumerate((("stores the files", "sun", ico_folder), ("checks logins", "mint", ico_lock), ("runs the backups", "sky", ico_disc))):
        yy = 126 + i * 58
        cv.add(cv.line(186, yy, 222, yy, ARROW, 2.5, op=.45, dash="3 5"))
        cv.add(feature(cv, 224, yy, label, col, ic))
    cv.add(P.pill(cv, 204, 304, "every client asks the server", "paper", 14))
    # ---- peer to peer
    cx, cy, r = 596, 236, 120
    pts = [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a)) * .88) for a in (-90, -18, 54, 126, 198)]
    for a in range(5):
        for b in range(a + 1, 5):
            cv.add(P.cable(cv, "M%s %s L%s %s" % (_n(pts[a][0]), _n(pts[a][1]), _n(pts[b][0]), _n(pts[b][1])), "slate", 3.5))
    for (x, y) in pts:
        cv.add(mini_pc(cv, x - 33, y - 24, .3))
    cv.add(P.pill(cv, cx, cy + 6, "each is client and server", "paper", 14))
    # ---- when something breaks
    cv.add(P.cross(cv, 62, 428, 14), cv.text(86, 434, "Server down: nobody can work", 15.5, 650, anchor="start"))
    cv.add(P.tick(cv, 454, 428, 14), cv.text(478, 434, "One down: the rest carry on", 15.5, 650, anchor="start"))
    cv.add(P.badge(cv, 60, 40, 1), P.badge(cv, 206, 96, 2), P.badge(cv, 450, 40, 3), P.badge(cv, 34, 406, 4))
    return figure(
        "client-server", cv, "Client–server compared with peer to peer",
        "Two ways of organising a network. In a client server network, four client machines all connect to one central server, which stores "
        "the files, checks logins and runs the backups. That makes everything central: one place to back up, one place to set security, one "
        "place to update. It also makes the server a single point of failure, so when it goes down nobody can work. In a peer to peer "
        "network there is no server: every machine is both a client and a server and is joined directly to the others, so it is simple and "
        "cheap, there is no central security or backup, and losing one machine leaves the rest working.",
        ["Client server: every device asks one central machine for what it needs.",
         "The server holds the files, does the work and checks who you are.",
         "Peer to peer: no server, and every machine is both client and server.",
         "Lose the server and a client server network stops. A peer network does not."],
        "A school uses client server because somebody has to control logins and back work up. Sharing music between phones is peer to peer.")


@illustration("web-request")
def _web_request():
    cv = Canvas(800, 500).backdrop()
    cv.add(P.person(cv, 14, 236, .72, "tan", "black", "teal", "short"))
    cv.add(P.laptop(cv, 112, 232, .98, P.browser_screen(cv, 31, 9, 158, 102, "www.example.com", True)))
    # the DNS book
    cv.add(P.book(cv, 378, 26, .95, "coral", "DNS"))
    cv.add(P.pill(cv, 494, 70, "the internet's phone book", "paper", 14, 12, 28, 650, anchor="start"))
    # the web server
    cv.add(P.server_rack(cv, 640, 186, 3, 1.0))
    cv.add(P.pill(cv, 705, 384, "web server", "paper", 15))
    cv.add(P.pill(cv, 705, 416, "93.184.216.34", "sun", 14, 12, 28, 700))
    # 1 ask, 2 answer
    cv.add(P.curve_arrow(cv, (232, 226), (236, 138), (300, 96), (372, 92), PAL["teal"][1], 5.5, 14))
    cv.add(P.curve_arrow(cv, (376, 146), (372, 190), (346, 208), (318, 232), PAL["coral"][1], 5.5, 14))
    cv.add(P.pill(cv, 178, 80, "Where is example.com?", "teal", 14.5))
    cv.add(P.pill(cv, 496, 184, "It is 93.184.216.34", "coral", 14.5, 12, 28, 700))
    # 3 request, 4 files back
    cv.add(P.arrow(cv, [(342, 298), (628, 298)], PAL["teal"][1], 6, 16))
    cv.add(P.pill(cv, 486, 272, "GET /index.html", "teal", 14.5, 12, 28, 700))
    cv.add(P.arrow(cv, [(628, 356), (342, 356)], PAL["plum"][1], 6, 16))
    for i, (lab, col) in enumerate((("HTML", "coral"), ("CSS", "sky"), ("JS", "sun"), ("IMG", "mint"))):
        xx = 372 + i * 62
        cv.add(P.doc(cv, xx, 306, .46, 62, 80, 0, "paper", col))
        cv.add(cv.text(xx + 14.2, 354, lab, 11.5, 800, cls="il-ink"))
    cv.add(P.pill(cv, 486, 398, "the files the page is made of", "paper", 14.5))
    cv.add(P.badge(cv, 252, 150, 1), P.badge(cv, 352, 200, 2), P.badge(cv, 360, 298, 3), P.badge(cv, 612, 356, 4), P.badge(cv, 150, 256, 5))
    return figure(
        "web-request", cv, "What happens between typing a web address and seeing the page",
        "You type a domain name, which is written for people to remember, but routers only understand IP addresses, so the browser first has "
        "to translate it. It asks a DNS server, which works like a phone book for the internet, and the DNS server returns the IP address that "
        "the name belongs to. The browser then sends an HTTP request to that address asking for the page. The web server answers with the "
        "files the page is made of: HTML, CSS, images and scripts. The browser puts them together and draws the page on the screen. DNS only "
        "tells the browser where to go; the browser makes the journey itself.",
        ["You type an address. The browser needs the IP address behind the name.",
         "A DNS server looks up the name and returns the IP address.",
         "The browser sends an HTTP request to that address.",
         "The server sends back HTML, CSS, images and scripts.",
         "The browser renders them into the page you see."],
        "DNS is a lookup, not a delivery. It tells the browser where to go, and the browser goes there itself.")


