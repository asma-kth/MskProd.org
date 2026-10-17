"""Illustrations for building applications and games in Python: a tkinter window, the game loop and
rectangle collisions."""
import math

from .illus import Canvas, PAL, INK, ARROW, figure, illustration, _n
from . import illus_props as P
from . import illus_glyphs as G


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


# ------------------------------------------------------------------ a tkinter window

@illustration("tk-widgets")
def _tk():
    cv = Canvas(800, 500).backdrop()
    cv.add(cv.shadow(220, 322, 190, 8, .2))
    cv.add(cv.rect(14, 30, 416, 290, 12, "#FFFFFF", stroke="#9FB3BE", sw=1.6), cv.rect(14, 30, 416, 30, 12, "#DCE8EE"), cv.rect(14, 46, 416, 14, 0, "#DCE8EE"))
    cv.add(cv.text(30, 51, "Mark book", 13.5, 750, anchor="start", fill=INK))
    for i, c in enumerate(("#5BD58B", "#FFCB47", "#FF7B72")):
        cv.add(cv.circle(344 + i * 24, 45, 6, c))
    # the widgets, in a grid
    def widget(x, y, w, h, kind, text, col):
        out = cv.rect(x, y, w, h, 6, col[0], stroke=col[1], sw=2.2)
        return out + cv.text(x + (10 if kind == "entry" else w / 2), y + h / 2 + 5, text, 14, 750, anchor="start" if kind == "entry" else "middle", fill=INK, mono=kind != "button")
    cv.add(widget(34, 82, 100, 36, "label", "Name:", ("#DDF3FA", "#2F82C0")), widget(150, 82, 250, 36, "entry", "Aisha", ("#FFFFFF", "#0F7C84")))
    cv.add(widget(34, 132, 100, 36, "label", "Mark:", ("#DDF3FA", "#2F82C0")), widget(150, 132, 120, 36, "entry", "72", ("#FFFFFF", "#0F7C84")))
    cv.add(widget(150, 184, 120, 38, "button", "Add", ("#FFE9A8", "#B98A12")))
    cv.add(cv.rect(34, 238, 366, 66, 6, "#FFFFFF", stroke="#C84B43", sw=2.2))
    for i, t in enumerate(("Aisha   72", "Ben     55")):
        cv.add(cv.text(46, 258 + i * 22, t, 13, 650, anchor="start", fill=INK, mono=True))
    for (x, y, n) in ((34, 80, 1), (150, 80, 2), (150, 182, 3), (34, 236, 4)):
        cv.add(P.badge(cv, x + 4, y + 2, n, "deep", 13))
    # the same thing in code
    cv.add(G.code(cv, 442, 30, 344, ["root = tk.Tk()", "tk.Label(root, text='Name:').grid(row=0, column=0)", "entry = tk.Entry(root)", "entry.grid(row=0, column=1)", "tk.Button(root, text='Add',", "          command=add).grid(row=2, column=1)", "root.mainloop()"], title="app.py", size=10.5, numbers=False))
    for i, (col, t) in enumerate((("#2F82C0", "Label: text to read"), ("#0F7C84", "Entry: text to type"), ("#B98A12", "Button: runs a function"), ("#C84B43", "Listbox: a list to show"))):
        cv.add(cv.rect(446, 232 + i * 22, 14, 14, 3, col), cv.text(468, 244 + i * 22, t, 13, 700, anchor="start", cls="il-ink"))
    # the event loop
    cv.add(P.card(cv, 14, 346, 772, 138, 20, "mainloop() waits for events", "teal"), P.badge(cv, 36, 372, 5))
    steps = [("wait", "sky"), ("click", "sun"), ("call add()", "coral"), ("redraw", "mint")]
    for i, (t, col) in enumerate(steps):
        x = 50 + i * 178
        cv.add(P.lift(cv, x, 398, 130, 42, col, 10, 4, hl=False), cv.text(x + 65, 424, t, 15, 800, fill=INK, mono=True))
        if i < 3:
            cv.add(P.arrow(cv, [(x + 134, 419), (x + 172, 419)], ARROW, 3.5, 10))
    cv.add(P.curve_arrow(cv, (690, 446), (640, 478), (180, 478), (115, 446), ARROW, 3, 10, dash="5 5"))
    return figure(
        "tk-widgets", cv, "A tkinter window with its widgets, the code that makes it, and the event loop",
        "A small tkinter window called Mark book, built from widgets laid out in a grid. One, a Label reading Name next to two, an Entry that "
        "holds the name Aisha; the same again for the mark; three, a Button labelled Add; and four, a Listbox showing the marks added so far. "
        "Beside it is the code: tk.Tk creates the window, tk.Label creates a label and grid places it in a row and column, tk.Entry creates "
        "an entry, tk.Button creates a button whose command is a function, and root.mainloop starts the event loop. Five: mainloop waits. When "
        "the user clicks, the button's function, here add, is called, the screen is redrawn, and the program goes back to waiting.",
        ["A Label shows text.", "An Entry lets the user type.", "A Button runs a function when clicked.", "A Listbox shows a list.",
         "mainloop() waits for events. A click calls your function, the screen is redrawn, then it waits again."],
        "Widgets are created, then placed with grid(). Nothing happens until mainloop() starts waiting for the user.")


# ------------------------------------------------------------------ the game loop

@illustration("game-loop")
def _loop():
    cv = Canvas(800, 500).backdrop()
    cv.add(P.card(cv, 14, 30, 460, 452, 20, "Every frame, 60 times a second", "teal"))
    nodes = [("Events", "sky", (118, 120), "keys, mouse, quit"), ("Update", "coral", (370, 120), "move things, check hits"), ("Draw", "mint", (370, 330), "clear, draw, flip"), ("Tick", "sun", (118, 330), "clock.tick(60)")]
    for i, (name, col, (cx, cy), sub) in enumerate(nodes):
        cv.add(P.lift(cv, cx - 82, cy - 40, 164, 80, col, 14, 6, hl=False), cv.text(cx, cy - 6, name, 18, 800, fill=INK, mono=True), cv.text(cx, cy + 20, sub, 12.5, 700, fill=INK))
        cv.add(P.badge(cv, cx - 82, cy - 40, i + 1))
    cv.add(P.arrow(cv, [(204, 120), (282, 120)], ARROW, 4.5, 13), P.arrow(cv, [(370, 168), (370, 282)], ARROW, 4.5, 13), P.arrow(cv, [(284, 330), (206, 330)], ARROW, 4.5, 13), P.arrow(cv, [(118, 282), (118, 168)], ARROW, 4.5, 13))
    cv.add(G.arrow_ring(cv, 244, 225, 34, -60, 240, "#25B3BB", 5, 12))
    cv.add(cv.text(244, 230, "60", 20, 800, cls="il-ink", mono=True))
    cv.add(cv.text(244, 424, "Each pass is one frame. Games feel smooth", 13, 650, cls="il-ink2"), cv.text(244, 444, "because the frames come so fast.", 13, 650, cls="il-ink2"))
    cv.add(G.code(cv, 494, 30, 292, ["running = True", "while running:", "    for event in pygame.event.get():", "        if event.type == pygame.QUIT:", "            running = False", "    update()", "    draw()", "    clock.tick(60)"], title="game.py", size=11.5, numbers=False, hl=(2, 5, 6, 7)))
    for i, (t, col) in enumerate((("lines 3 to 5: events", "#66B8EC"), ("line 6: update", "#F77F72"), ("line 7: draw", "#62CFA3"), ("line 8: tick", "#FFCC4A"))):
        cv.add(cv.rect(494, 262 + i * 28, 14, 14, 3, col), cv.text(516, 274 + i * 28, t, 13, 700, anchor="start", cls="il-ink"))
    cv.add(cv.text(640, 400, "clock.tick(60) pauses just long enough", 12.5, 650, cls="il-ink2"), cv.text(640, 418, "to hold the game at 60 frames a second", 12.5, 650, cls="il-ink2"))
    return figure(
        "game-loop", cv, "The game loop: handle events, update, draw and tick, 60 times a second, with the code that does it",
        "Every game runs a loop, one pass of which is a frame. One, handle events: read the keys, the mouse and the quit button. Two, update: move "
        "things and check for hits. Three, draw: clear the screen, draw everything and flip the display. Four, tick: clock dot tick 60 "
        "pauses just long enough to hold the game at 60 frames a second. The code is a while loop with a for loop over pygame.event.get, an "
        "update call, a draw call and clock.tick 60. Because the frames come so fast the game feels smooth.",
        ["Handle events: keys, mouse and quit.", "Update: move things and check for collisions.", "Draw: clear the screen, draw everything, flip the display.",
         "Tick: hold the game at 60 frames a second."],
        "Input, update, draw, repeat. Moving things in update and drawing them in draw keeps the code easy to follow.")


# ------------------------------------------------------------------ collisions between rectangles

@illustration("collision-rects")
def _collide():
    cv = Canvas(800, 500).backdrop()
    cv.add(P.card(cv, 14, 30, 420, 300, 20, "A Rect: x, y, width, height", "sky"), P.badge(cv, 36, 56, 1))
    ox, oy = 52, 76
    cv.add(P.arrow(cv, [(ox, oy), (ox + 360, oy)], ARROW, 2.6, 9), P.arrow(cv, [(ox, oy), (ox, oy + 230)], ARROW, 2.6, 9))
    cv.add(cv.text(ox + 372, oy + 5, "x", 14, 800, anchor="start", cls="il-ink", mono=True), cv.text(ox - 4, oy + 246, "y", 14, 800, anchor="end", cls="il-ink", mono=True))
    cv.add(cv.text(ox + 6, oy + 18, "(0, 0) top left", 12, 650, anchor="start", cls="il-ink2"))
    ax, ay, aw, ah = ox + 40, oy + 50, 150, 100
    bx, by, bw, bh = ox + 128, oy + 110, 100, 90
    cv.add(cv.rect(ax, ay, aw, ah, 6, "#66B8EC", stroke="#1F5F9A", sw=2.6), cv.rect(bx, by, bw, bh, 6, "#FFCC4A", stroke="#B98A12", sw=2.6))
    cv.add(cv.rect(bx, by, ax + aw - bx, ay + ah - by, 2, "#BA352D", op=.5))
    cv.add(cv.text(ax + 8, ay + 22, "player", 13, 800, anchor="start", fill=INK), cv.text(ax + 8, ay + 40, "Rect(40,50,150,100)", 11.5, 700, anchor="start", fill=INK, mono=True))
    cv.add(cv.text(bx + bw + 12, by + 28, "coin", 13, 800, anchor="start", cls="il-ink"), cv.text(bx + bw + 12, by + 46, "Rect(128,110,", 11, 700, anchor="start", cls="il-ink2", mono=True), cv.text(bx + bw + 12, by + 61, "100,90)", 11, 700, anchor="start", cls="il-ink2", mono=True))
    cv.add(cv.text(ox + 20, oy + 222, "the overlap", 13, 800, anchor="start", cls="il-bad"), P.arrow(cv, [(ox + 96, oy + 214), (bx + 20, by + 24)], "#BA352D", 2.6, 8))
    # the four tests
    cv.add(P.card(cv, 450, 30, 336, 300, 20, "player.colliderect(coin)", "coral"), P.badge(cv, 472, 56, 2))
    tests = ["player.left   < coin.right", "player.right  > coin.left", "player.top    < coin.bottom", "player.bottom > coin.top"]
    for i, t in enumerate(tests):
        y = 96 + i * 40
        cv.add(P.tick(cv, 480, y + 8, 10), cv.text(500, y + 13, t, 12.5, 750, anchor="start", cls="il-ink", mono=True))
    cv.add(cv.line(468, 262, 768, 262, "var(--il-line)", 1.4, dash="4 5"))
    cv.add(P.pill(cv, 618, 292, "all four true: they overlap", "sun", 14, 14, 30, 800))
    # a miss
    cv.add(P.card(cv, 14, 350, 772, 132, 20, "One false test is enough for a miss", "mint"), P.badge(cv, 36, 376, 3))
    cv.add(cv.rect(44, 396, 110, 66, 6, "#66B8EC", stroke="#1F5F9A", sw=2.6), cv.rect(200, 410, 80, 52, 6, "#FFCC4A", stroke="#B98A12", sw=2.6))
    cv.add(cv.line(154, 440, 200, 440, "#BA352D", 2.6), cv.text(177, 428, "gap", 12, 800, cls="il-bad"))
    cv.add(P.cross(cv, 332, 428, 12), cv.text(354, 433, "player.right > coin.left", 14, 750, anchor="start", cls="il-ink", mono=True))
    cv.add(cv.text(354, 454, "is False, so colliderect() is False", 13, 650, anchor="start", cls="il-ink2"))
    return figure(
        "collision-rects", cv, "A Rect with its corner at the top left, and the four tests that make colliderect true",
        "A pygame Rect is a rectangle given by its x, y, width and height, and the screen's origin, 0 0, is at the top left, with x going right and "
        "y going down. The player is Rect 40, 50, 150, 100 and the coin is Rect 128, 110, 100, 90, and the two overlap in a shaded region. "
        "player dot colliderect coin is true when four tests are all true: the player's left is less than the coin's right, the player's "
        "right is greater than the coin's left, the player's top is less than the coin's bottom, and the player's bottom is greater than the "
        "coin's top. If any one test is false, for example when there is a gap between the player's right edge and the coin's left edge, the "
        "rectangles do not overlap.",
        ["A Rect has x, y, width and height. The origin is the top left, and y increases downwards.",
         "colliderect is true only if all four tests are true: the rectangles overlap on both the x axis and the y axis.",
         "If any one test is false there is a gap, so there is no collision."],
        "Two rectangles overlap only when they overlap in both directions. Check each axis separately.")
