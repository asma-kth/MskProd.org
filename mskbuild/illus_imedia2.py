"""More Creative iMedia illustrations: product types, an audience persona, research methods, media
file types, permissions, a risk matrix and a comparison of distribution platforms."""
import math

from .illus import Canvas, PAL, INK, ARROW, figure, illustration, _n
from . import illus_props as P
from . import illus_glyphs as G
from .illus_machine import mini_window
from .illus_devices import cursor

GRID_X = (14, 277, 540)
GRID_Y = (30, 262)


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


# ------------------------------------------------------------------ types of media product

def clapper(cv, x, y):
    out = cv.rect(x, y + 20, 84, 52, 6, cv.g("dark", "deep"))
    out += cv.poly([(x - 2, y + 4), (x + 84, y - 6), (x + 86, y + 12), (x, y + 22)], cv.g("metal"), stroke="#8799A7", sw=1.2)
    for k in range(4):
        x0 = x + 4 + k * 20
        out += cv.poly([(x0, y + 5 - k * 2.2), (x0 + 11, y + 3 - k * 2.2), (x0 + 6, y + 18 - k * 2.2 + 3), (x0 - 5, y + 20 - k * 2.2 + 3)], "#1C2831", op=.9)
    return out + cv.rect(x + 10, y + 34, 64, 6, 3, "#FFFFFF", op=.5) + cv.rect(x + 10, y + 48, 44, 6, 3, "#FFFFFF", op=.35)


def microphone(cv, cx, y):
    out = cv.path("M%s %s q0 30 28 30 q28 0 28 -30" % (cx - 28, y + 20), stroke="#5B6D79", sw=5)
    out += cv.rect(cx - 15, y - 10, 30, 52, 15, cv.g("metal", "round")) + cv.rect(cx - 15, y - 10, 30, 52, 15, "none", stroke="#8799A7", sw=1.6)
    for k in range(4):
        out += cv.line(cx - 9, y + 2 + k * 9, cx + 9, y + 2 + k * 9, "#8799A7", 1.6)
    return out + cv.line(cx, y + 50, cx, y + 70, "#5B6D79", 5) + cv.rect(cx - 20, y + 68, 40, 6, 3, "#5B6D79")


@illustration("media-products")
def _products():
    cv = Canvas(800, 500).backdrop()
    spec = [("Print", "coral", "magazines, posters, leaflets", "static"), ("Moving image", "sky", "film, TV, adverts, video", "time-based"), ("Audio", "plum", "podcasts, radio, music", "time-based"),
            ("Interactive", "mint", "websites, apps, games, kiosks", "interactive"), ("Digital graphics", "sun", "logos, social posts, infographics", "static"), ("Animation", "teal", "cartoons, GIFs, motion graphics", "time-based")]
    tags = {"static": "sun", "time-based": "sky", "interactive": "mint"}
    for n, (title, col, ex, tag) in enumerate(spec):
        x, y = GRID_X[n % 3], GRID_Y[n // 3]
        cv.add(P.card(cv, x, y, 246, 200, 18, title, col), P.badge(cv, x + 16, y + 24, n + 1))
        cx = x + 123
        if n == 0:
            cv.add(cv.rect(cx - 36, y + 44, 72, 96, 5, "#FFFFFF", stroke="#9FB3BE", sw=1.4), cv.rect(cx - 36, y + 44, 72, 18, 5, cv.g("coral")), cv.text(cx, y + 57, "MAGAZINE", 9.5, 800, fill=INK))
            cv.add(P.photo(cv, cx - 29, y + 70, 58, 38, 3), cv.rect(cx - 29, y + 116, 58, 5, 2, "#C5D1D9"), cv.rect(cx - 29, y + 126, 40, 5, 2, "#C5D1D9"))
        elif n == 1:
            cv.add(clapper(cv, cx - 42, y + 56))
        elif n == 2:
            cv.add(microphone(cv, cx, y + 56))
        elif n == 3:
            cv.add(mini_window(cv, cx - 50, y + 54, 100, 76))
            cv.add(cursor(cv, cx + 22, y + 96, 1.3))
        elif n == 4:
            cv.add(cv.rect(cx - 52, y + 48, 104, 88, 8, "#FFFFFF", stroke="#9FB3BE", sw=1.4), cv.circle(cx - 22, y + 86, 20, cv.g("coral")), cv.rect(cx + 2, y + 66, 38, 38, 5, cv.g("sky")), cv.poly([(cx - 30, y + 126), (cx + 4, y + 108), (cx + 32, y + 126)], cv.g("mint")))
        else:
            for k in range(3):
                cv.add(cv.circle(cx - 44 + k * 44, y + 112 - math.sin(k * math.pi / 2) * 40, 16, "#F77F72", op=.4 + k * .3))
            cv.add(cv.path("M%s %s Q%s %s %s %s" % (cx - 44, y + 112, cx, y + 40, cx + 44, y + 112), stroke="#8AA0AC", sw=2, dash="3 6"))
        cv.add(P.pill(cv, cx, y + 150, tag, tags[tag], 12, 10, 22, 800))
        for j, ln in enumerate(wrap(ex, 30)):
            cv.add(cv.text(cx, y + 178 + j * 14, ln, 12.5, 650, cls="il-ink2"))
    return figure(
        "media-products", cv, "Six types of media product: print, moving image, audio, interactive, digital graphics and animation",
        "Six types of media product, one card each. Print, such as magazines, posters and leaflets, is static. Moving image, such as film, TV, "
        "adverts and video, is time based. Audio, such as podcasts, radio and music, is time based. Interactive products, such as websites, apps, "
        "games and kiosks, respond to the user. Digital graphics, such as logos, social posts and infographics, are static. Animation, such as "
        "cartoons, GIFs and motion graphics, is time based.",
        ["Print: a static page, such as a magazine, poster or leaflet.", "Moving image: film, TV and video, which play over time.", "Audio: sound that plays over time.",
         "Interactive: the user's actions change what happens.", "Digital graphics: static images such as logos and social posts.", "Animation: drawn or computer made movement."],
        "Most real products combine several types, so a client's brief often asks for more than one.")


# ------------------------------------------------------------------ an audience persona

@illustration("persona-card")
def _persona():
    cv = Canvas(800, 500).backdrop()
    cv.add(P.card(cv, 14, 30, 440, 452, 20, "Persona: Maya", "coral"), P.badge(cv, 36, 56, 1))
    cv.add(cv.circle(100, 140, 62, "var(--il-band)"), P.person(cv, 56, 82, .72, "tan", "black", "teal", "long"))
    cv.add(cv.text(190, 108, "Maya Chen", 20, 800, anchor="start", cls="il-ink"), cv.text(190, 132, "15, Year 10 student", 14, 650, anchor="start", cls="il-ink2"), cv.text(190, 154, "Manchester, lives with family", 13, 650, anchor="start", cls="il-ink2"))
    px = 190
    for i, t in enumerate(("phone first", "short videos", "football")):
        cv.add(P.pill(cv, px, 182, t, ("sky", "mint", "sun")[i], 12.5, 10, 24, 750, anchor="start"))
        px += len(t) * 12.5 * .58 + 20 + 8
    rows = [("Goals", "learn new skills, keep up with friends", "teal"), ("Habits", "watches video on a phone for 3 hours a day", "sky"), ("Frustrations", "adverts she cannot skip, tiny text, slow sites", "coral")]
    for i, (h_, t, col) in enumerate(rows):
        y = 226 + i * 78
        cv.add(P.lift(cv, 34, y, 100, 30, col, 8, 3, hl=False), cv.text(84, y + 20, h_, 13.5, 800, fill=INK))
        for j, ln in enumerate(wrap(t, 38)):
            cv.add(cv.text(148, y + 21 + j * 18, ln, 13.5, 650, anchor="start", cls="il-ink"))
    cv.add(P.card(cv, 472, 30, 314, 452, 20, "What it means for the product", "teal"), P.badge(cv, 494, 56, 2))
    for i, (a_, b_) in enumerate((("phone first", "design for a small screen, thumbs and portrait"), ("short videos", "keep each clip under a minute, captioned"), ("tiny text", "large type and high contrast"), ("slow sites", "small files, quick to load"), ("football", "content she cares about, in her tone"))):
        y = 92 + i * 76
        cv.add(P.pill(cv, 494, y, a_, "paper", 12.5, 10, 24, 750, anchor="start"), P.arrow(cv, [(512, y + 14), (512, y + 26)], ARROW, 2.5, 7))
        for j, ln in enumerate(wrap(b_, 34)):
            cv.add(cv.text(494, y + 44 + j * 17, ln, 13, 700, anchor="start", cls="il-ink"))
    return figure(
        "persona-card", cv, "An audience persona, Maya Chen, and what each trait means for the product",
        "A persona is an invented but realistic member of the target audience. Maya Chen is 15, in Year 10, from Manchester, and lives with her "
        "family. She is phone first, likes short videos and football. Her goals are to learn new skills and keep up with friends. Her habits "
        "include watching video on her phone for about three hours a day. Her frustrations are adverts she cannot skip, tiny text and slow sites. "
        "On the right each trait is linked to a design decision: phone first means design for a small screen, short videos mean clips under a "
        "minute with captions, tiny text means large type and high contrast, slow sites mean small files, and football means content she cares about.",
        ["The persona is a made up person who stands for the audience, built from research.", "Each trait leads to a design decision, so the product fits the audience."],
        "A persona is only useful if it is based on research and if every design choice can be traced back to it.")


# ------------------------------------------------------------------ research methods

@illustration("research-methods")
def _research():
    cv = Canvas(800, 500).backdrop()
    cv.add(P.card(cv, 14, 30, 480, 330, 20, "Primary research", "teal"), P.badge(cv, 36, 56, 1))
    tiles = [("Questionnaire", "many answers, quickly"), ("Interview", "detailed, one to one"), ("Focus group", "ideas from a small group"), ("Observation", "what people actually do")]
    for i, (t, sub) in enumerate(tiles):
        x, y = 30 + (i % 2) * 226, 92 + (i // 2) * 126
        cv.add(P.lift(cv, x, y, 212, 112, "paper", 12, 4, hl=False))
        cx = x + 106
        if i == 0:
            cv.add(cv.rect(cx - 20, y + 12, 40, 52, 5, "#FFFFFF", stroke="#9FB3BE", sw=1.4), cv.rect(cx - 10, y + 6, 20, 10, 4, "#8799A7"))
            for k in range(3):
                cv.add(cv.rect(cx - 13, y + 24 + k * 12, 7, 7, 2, "#66B8EC"), cv.rect(cx - 3, y + 26 + k * 12, 16, 4, 2, "#C5D1D9"))
        elif i == 1:
            cv.add(G.bubble(cv, cx - 40, y + 12, 44, 28, ["?"], tail=(-10, 18), size=15), G.bubble(cv, cx - 2, y + 34, 44, 28, ["!"], tail=(14, 18), size=15, fill="#C9F3E0"))
        elif i == 2:
            for k in range(3):
                cv.add(P.person(cv, cx - 44 + k * 32, y + 10 + (k % 2) * 6, .26, ("tan", "light", "brown")[k], ("black", "brown", "blond")[k], ("coral", "sky", "plum")[k], "short"))
        else:
            cv.add(P.magnifier(cv, cx - 4, y + 34, .9, 14), cv.circle(cx - 30, y + 54, 10, "#F6CDA8"), cv.rect(cx - 38, y + 62, 16, 10, 4, "#F77F72"))
        cv.add(cv.text(cx, y + 86, t, 14.5, 800, fill=INK), cv.text(cx, y + 104, sub, 12, 650, fill="#4A6470"))
    cv.add(cv.text(254, 80, "you collect it yourself", 13.5, 700, cls="il-ink2"))
    cv.add(P.card(cv, 510, 30, 276, 330, 20, "Secondary research", "sky"), P.badge(cv, 532, 56, 2), cv.text(648, 80, "it already exists", 13.5, 700, cls="il-ink2"))
    for i, (t, sub) in enumerate((("Websites and articles", "quick and cheap"), ("Books and reports", "from experts"), ("Competitor products", "what already works"))):
        y = 102 + i * 82
        cv.add(P.lift(cv, 530, y, 236, 68, "paper", 12, 4, hl=False))
        if i == 0:
            cv.add(mini_window(cv, 546, y + 14, 46, 34))
        elif i == 1:
            cv.add(P.book(cv, 548, y + 8, .3, "teal", ""))
        else:
            cv.add(cv.rect(548, y + 14, 18, 18, 4, cv.g("sun")), cv.rect(570, y + 14, 18, 18, 4, cv.g("coral")), cv.rect(548, y + 36, 40, 10, 3, cv.g("sky")))
        cv.add(cv.text(606, y + 30, t, 13.5, 800, anchor="start", fill=INK), cv.text(606, y + 50, sub, 12, 650, anchor="start", fill="#4A6470"))
    cv.add(P.card(cv, 14, 380, 772, 102, 18), P.badge(cv, 36, 406, 3))
    for k, (col, a_, b_, x) in enumerate((("teal", "Primary", "specific to your audience, but slow and costly to collect", 60), ("sky", "Secondary", "quick and cheap, but may be out of date or not about your audience", 420))):
        cv.add(P.pill(cv, x, 418, a_, col, 13.5, 12, 26, 800, anchor="start"))
        for j, ln in enumerate(wrap(b_, 38)):
            cv.add(cv.text(x, 450 + j * 18, ln, 13.5, 650, anchor="start", cls="il-ink"))
    return figure(
        "research-methods", cv, "Primary research methods you collect yourself, and secondary research that already exists",
        "Two kinds of research. Primary research is collected by you: a questionnaire gets many answers quickly, an interview gives detail one to "
        "one, a focus group draws ideas from a small group, and observation shows what people actually do. Secondary research already exists: "
        "websites and articles are quick and cheap, books and reports come from experts, and competitor products show what already works. "
        "Primary research is specific to your audience but slow and costly to collect. Secondary research is quick and cheap but may be out of date "
        "or not about your audience.",
        ["Primary research is collected first hand: questionnaires, interviews, focus groups and observation.", "Secondary research uses what already exists: websites, books, reports and competitor products.",
         "Primary is specific but slow and costly. Secondary is quick and cheap but may not fit."],
        "A good project uses both: secondary research to get started, primary research to check it against your real audience.")


# ------------------------------------------------------------------ media file types

@illustration("media-file-types")
def _filetypes():
    cv = Canvas(800, 500).backdrop()
    spec = [("Audio", "plum", (("MP3", "lossy, small", "sun"), ("WAV", "lossless, large", "sky"), ("AAC", "lossy, efficient", "mint"))),
            ("Video", "coral", (("MP4", "small, widely used", "sun"), ("MOV", "editing, larger", "sky"), ("AVI", "old, large", "slate"))),
            ("Document", "teal", (("PDF", "fixed layout", "red"), ("DOCX", "can be edited", "sky"), ("TXT", "plain text only", "slate")))]
    for n, (title, col, fmts) in enumerate(spec):
        x = GRID_X[n]
        cv.add(P.card(cv, x, 30, 246, 250, 18, title, col), P.badge(cv, x + 16, 54, n + 1))
        for i, (ext, note, c2) in enumerate(fmts):
            y = 84 + i * 62
            tc = "#FFFFFF" if c2 == "red" else INK
            cv.add(P.lift(cv, x + 18, y, 70, 40, c2, 9, 4, hl=False), cv.text(x + 53, y + 26, ext, 15, 800, fill=tc, mono=True), cv.text(x + 98, y + 25, note, 13, 700, anchor="start", cls="il-ink"))
    # size against quality
    cv.add(P.card(cv, 14, 300, 772, 182, 18, "The same 3 minute song in two formats", "sun"), P.badge(cv, 36, 326, 4))
    for i, (ext, mb, col, note) in enumerate((("WAV", 31.8, "sky", "every sample kept: lossless"), ("MP3", 2.9, "sun", "128 kbps: lossy, about a tenth of the size"))):
        y = 350 + i * 66
        cv.add(cv.text(44, y + 21, ext, 16, 800, anchor="start", cls="il-ink", mono=True))
        w = 520 * mb / 31.8
        cv.add(cv.rect(100, y, w, 28, 8, cv.g(col)), cv.text(100 + w + 12, y + 21, "%.1f MB" % mb, 15, 800, anchor="start", cls="il-ink", mono=True))
        cv.add(cv.text(100, y + 46, note, 12.5, 650, anchor="start", cls="il-ink2"))
    return figure(
        "media-file-types", cv, "Common audio, video and document file formats, and the size of a song as WAV and as MP3",
        "Common file formats in three groups. Audio: MP3 is lossy and small, WAV is lossless and large, and AAC is lossy and efficient. Video: MP4 "
        "is small and plays everywhere, MOV is used for editing and is larger, and AVI is old and large. Documents: PDF has a fixed layout, "
        "DOCX can be edited, and TXT is plain text only. A bar chart compares one three minute song: as a WAV, which keeps every sample, it is about "
        "31.8 megabytes, and as a 128 kilobit per second MP3, which is lossy, it is about 2.9 megabytes, roughly a tenth of the size.",
        ["Audio formats trade quality against size: lossless WAV is large, lossy MP3 and AAC are small.", "Video: MP4 is the safe choice for sharing, MOV and AVI suit editing or are old.",
         "Documents: PDF keeps the layout, DOCX can be edited, TXT is plain text.", "The same song is about ten times smaller as an MP3 than as a WAV."],
        "Choose the format for the job: editing wants quality, sharing wants a small file that plays on every device.")


# ------------------------------------------------------------------ permissions

@illustration("permissions-chain")
def _perms():
    cv = Canvas(800, 500).backdrop()
    cv.add(cv.shadow(400, 304, 120, 8, .2))
    cv.add(cv.rect(310, 130, 180, 150, 14, "#FFFFFF", stroke="#9FB3BE", sw=2), P.photo(cv, 322, 142, 156, 100, 8))
    cv.add(P.person(cv, 374, 160, .38, "tan", "black", "coral", "short"), cv.rect(322, 252, 156, 8, 3, "#C5D1D9"), cv.rect(322, 266, 100, 8, 3, "#C5D1D9"))
    cv.add(cv.text(400, 112, "your finished video", 14.5, 800, cls="il-ink"))
    items = [(14, 40, "A person is in it", "Consent: a model release form", "coral"), (546, 40, "It was filmed on someone's land", "Permission from the owner", "sky"),
             (14, 300, "It uses a clip you did not film", "A licence from the creator", "sun"), (546, 300, "It has a music track", "A licence, or royalty free music", "mint")]
    for k, (x, y, a_, b_, col) in enumerate(items):
        cv.add(P.card(cv, x, y, 240, 126, 18), P.badge(cv, x + 22, y + 24, k + 1))
        cv.add(P.lift(cv, x + 20, y + 40, 200, 28, col, 8, 3, hl=False), cv.text(x + 120, y + 59, a_, 12, 800, fill=INK))
        for j, ln in enumerate(wrap(b_, 28)):
            cv.add(cv.text(x + 120, y + 94 + j * 18, ln, 13.5, 750, cls="il-ink"))
    cv.add(P.arrow(cv, [(254, 110), (306, 170)], ARROW, 3.5, 10), P.arrow(cv, [(546, 110), (494, 170)], ARROW, 3.5, 10), P.arrow(cv, [(254, 350), (306, 246)], ARROW, 3.5, 10), P.arrow(cv, [(546, 350), (494, 246)], ARROW, 3.5, 10))
    cv.add(P.pill(cv, 400, 462, "Keep a record of every permission, and credit where asked.", "paper", 14.5, 16, 30, 750))
    return figure(
        "permissions-chain", cv, "Four permissions a finished video may need",
        "A finished video may need several permissions before it can be published. If a person is in it, you need their consent, usually a model "
        "release form. If it was filmed on someone's land or property, you need the owner's permission. If it uses a clip you did not film, you "
        "need a licence from the creator. If it has a music track, you need a licence, or you can use royalty free music. Keep a record of every "
        "permission, and credit where asked.",
        ["A person in the shot: get their consent, in writing for anyone who is recognisable.", "A private location: get the owner's permission.",
         "Someone else's clip or photo: get a licence, or use material that is free to reuse.", "Music: get a licence, or use royalty free music."],
        "Copyright belongs to the creator automatically. If you did not make it, you need permission to use it.")


# ------------------------------------------------------------------ a risk matrix

@illustration("risk-matrix")
def _risk():
    cv = Canvas(800, 500).backdrop()
    cv.add(P.card(cv, 14, 30, 470, 452, 20, "Risk matrix", "coral"), P.badge(cv, 36, 56, 1))
    gx, gy, cs = 112, 92, 112
    shades = [["#FFF3C4", "#FFD9A8", "#FFB3A8"], ["#DDF3C9", "#FFF3C4", "#FFD9A8"], ["#C9F3E0", "#DDF3C9", "#FFF3C4"]]
    for r in range(3):
        for c in range(3):
            cv.add(cv.rect(gx + c * cs, gy + r * cs, cs - 4, cs - 4, 8, shades[r][c], stroke="#FFFFFF", sw=1))
    for r, lab in enumerate(("high", "medium", "low")):
        cv.add(cv.text(gx - 10, gy + r * cs + cs / 2, lab, 13, 700, anchor="end", cls="il-ink2"))
    for c, lab in enumerate(("low", "medium", "high")):
        cv.add(cv.text(gx + c * cs + cs / 2 - 2, gy + 3 * cs + 18, lab, 13, 700, cls="il-ink2"))
    cv.add(cv.text(gx + 1.5 * cs, gy + 3 * cs + 38, "impact if it happens", 13.5, 800, cls="il-ink"), cv.text(gx - 10, gy - 12, "likelihood", 13.5, 800, anchor="end", cls="il-ink"))
    placed = [("Lost files", 2, 2, "sky"), ("Actor ill", 2, 1, "plum"), ("Rain", 1, 1, "mint"), ("Flat battery", 0, 0, "sun")]
    for name, c, r, col in placed:
        cv.add(P.pill(cv, gx + c * cs + cs / 2 - 2, gy + r * cs + cs / 2 - 2, name, col, 12.5, 10, 26, 800))
    cv.add(P.card(cv, 500, 30, 286, 452, 20, "Contingency: the plan B", "teal"), P.badge(cv, 522, 56, 2))
    for i, (a_, b_, col) in enumerate((("Actor ill", "a reserve actor, or a second shooting day", "plum"), ("Flat battery", "spare batteries and a charger", "sun"), ("Rain", "an indoor backup location", "mint"), ("Lost files", "backups on two drives", "sky"))):
        y = 92 + i * 94
        cv.add(P.pill(cv, 520, y, a_, col, 12.5, 10, 24, 800, anchor="start"), P.arrow(cv, [(536, y + 14), (536, y + 28)], ARROW, 2.5, 7))
        for j, ln in enumerate(wrap(b_, 30)):
            cv.add(cv.text(520, y + 48 + j * 17, ln, 13.5, 700, anchor="start", cls="il-ink"))
    return figure(
        "risk-matrix", cv, "A risk matrix of likelihood against impact for a film shoot, with a contingency for each risk",
        "A risk matrix plots how likely a risk is against how bad it would be. Four risks for a film shoot are placed on it. A flat battery is "
        "likely but low impact. Rain is medium on both. An actor being ill is medium likely and high impact. Lost files are less likely but "
        "high impact. For each risk a contingency, a plan B, is listed: a reserve actor or a second shooting day for illness, spare batteries and a "
        "charger, an indoor backup location for rain, and backups on two drives for lost files.",
        ["Plot each risk by how likely it is and how much damage it would do. Plan most carefully for the top right.",
         "Every risk gets a contingency, a plan B, written down before the shoot."],
        "A work plan is only complete if it names the risks and says what you will do when one happens.")


# ------------------------------------------------------------------ comparing platforms

def meter(cv, x, y, n, color="teal"):
    out = ""
    for i in range(3):
        out += cv.circle(x + i * 20, y, 7, cv.g(color, "deep") if i < n else "var(--il-band)", stroke="#8AA0AC" if i >= n else None, sw=1.4)
    return out


@illustration("platform-compare")
def _platforms():
    cv = Canvas(800, 500).backdrop()
    cv.add(P.card(cv, 14, 30, 772, 452, 20, "How the platforms compare", "teal"), P.badge(cv, 36, 56, 1))
    crit = ["Reach", "Cost to you", "Control", "Interaction"]
    for j, t in enumerate(crit):
        cv.add(cv.text(300 + j * 118, 92, t, 14.5, 800, cls="il-ink"))
    plats = [("Social media", (3, 1, 1, 3)), ("Streaming service", (3, 2, 2, 1)), ("Your own website", (2, 2, 3, 3)), ("Print", (1, 3, 3, 1)), ("Broadcast TV", (3, 3, 1, 1))]
    for i, (name, vals) in enumerate(plats):
        y = 128 + i * 66
        if i % 2 == 0:
            cv.add(cv.rect(26, y - 24, 748, 56, 10, "var(--il-band)"))
        cv.add(cv.text(46, y + 6, name, 15, 800, anchor="start", cls="il-ink"))
        for j, v in enumerate(vals):
            cv.add(meter(cv, 300 + j * 118 - 20, y + 2, v, "coral" if j == 1 else "teal"))
    cv.add(cv.text(400, 462, "more filled dots = more of it. For cost, more is dearer.", 13, 650, cls="il-ink2"))
    return figure(
        "platform-compare", cv, "Five distribution platforms compared on reach, cost, control and interaction",
        "Five platforms rated from one to three on four measures. Social media has high reach, low cost to you, low control because the platform sets "
        "the rules, and high interaction. A streaming service has high reach, medium cost, medium control and low interaction. Your own website "
        "has medium reach unless you promote it, medium cost, high control and high interaction. Print has low reach, high cost, high control and low "
        "interaction. Broadcast TV has high reach, high cost, low control because of schedules, and low interaction.",
        ["Compare platforms on the same measures: reach, cost, control and interaction. Choose by matching them to the brief and the audience."],
        "There is no best platform. Pick the one that fits the audience, the budget and how much control the client needs.")
