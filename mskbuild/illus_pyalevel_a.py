"""Illustrations for the A Level Python topics, set one: heaps, tries, union-find, spanning trees,
greedy and dynamic programming, finite state machines and the syntax tree."""
from .illus import Canvas, PAL, INK, ARROW, figure, illustration, _n
from . import illus_props as P


def node(cv, x, y, label, color="sky", r=19, size=17, ring=None, double=False, mono=True):
    """A circle with a label, lifted off the page."""
    out = cv.circle(x, y + 3, r, "#10303A", op=.16)
    if double:
        out += cv.circle(x, y, r + 5, "#FFFFFF", stroke=PAL[color][2], sw=2.2)
    out += cv.circle(x, y, r, cv.g(color, "deep") if color in ("plum", "deep", "navy", "dark") else cv.g(color), stroke=ring or PAL[color][2], sw=2.6 if ring else 1.6)
    tc = "#FFFFFF" if color in ("plum", "deep", "navy", "dark") else INK
    out += cv.text(x, y + size * .36, label, size, 800, fill=tc, mono=mono)
    return out


def edge(cv, x1, y1, x2, y2, color="#8AA0AC", w=2.6, dash=None, op=None):
    return cv.line(x1, y1, x2, y2, color, w, dash=dash, op=op)


# ------------------------------------------------------------------ the binary heap

@illustration("heap-array")
def _heap_array():
    cv = Canvas(800, 470).backdrop()
    items = [1, 3, 2, 5, 9, 8]
    level_color = ["sun", "sky", "sky", "mint", "mint", "mint"]
    pos = [(215, 88), (125, 180), (305, 180), (65, 272), (185, 272), (305, 272)]
    cv.add(P.card(cv, 14, 24, 410, 372, 20, "a heap drawn as a tree", "teal"))
    for i in range(1, 6):
        px, py = pos[(i - 1) // 2]
        cx, cy = pos[i]
        cv.add(edge(cv, px, py, cx, cy, "#8AA0AC", 2.6))
    for i, v in enumerate(items):
        ring = "#C84B43" if i in (1, 3, 4) else None
        cv.add(node(cv, pos[i][0], pos[i][1], str(v), level_color[i], 21, 19, ring=ring))
        side = (1, -1, 1, -1, 1, 1)[i]              # which side of the node the index is written on
        cv.add(cv.text(pos[i][0] + side * 30, pos[i][1] - 20, "i=%d" % i, 12.5, 700, cls="il-ink2", mono=True, anchor="end" if side < 0 else "start"))
    cv.add(P.badge(cv, 40, 72, 1))
    cv.add(cv.text(219, 352, "every parent is no bigger than its children", 13.5, 700, cls="il-ink"))
    cv.add(cv.text(219, 376, "so the smallest is always at the top", 13.5, 700, cls="il-ink"))

    cv.add(P.card(cv, 440, 24, 346, 372, 20, "the same heap in a list", "sun"))
    ax, ay, bw, gap = 454, 128, 48, 5
    for i, v in enumerate(items):
        x = ax + i * (bw + gap)
        ring = "#C84B43" if i in (1, 3, 4) else None
        cv.add(P.lift(cv, x, ay, bw, 52, level_color[i], 9, 5, hl=False))
        if ring:
            cv.add(cv.rect(x - 2, ay - 2, bw + 4, 56, 10, "none", stroke=ring, sw=2.6))
        cv.add(cv.text(x + bw / 2, ay + 33, str(v), 21, 800, fill=INK, mono=True))
        cv.add(cv.text(x + bw / 2, ay + 82, str(i), 14, 700, cls="il-ink2", mono=True))
    cv.add(cv.text(612, ay + 106, "index", 12.5, 650, cls="il-ink2"))
    cv.add(P.badge(cv, 468, 62, 2))
    # arcs from index 1 to its children at 3 and 4
    x1 = ax + 1 * (bw + gap) + bw / 2
    for child, height in ((3, 40), (4, 62)):
        x2 = ax + child * (bw + gap) + bw / 2
        cv.add(P.curve_arrow(cv, (x1, ay - 6), (x1, ay - height - 24), (x2, ay - height - 24), (x2, ay - 8), "#C84B43", 2.6, 9, dash="5 4"))
    cv.add(cv.text(680, ay - 52, "children of index 1", 12.5, 700, cls="il-ink2"))
    cv.add(P.badge(cv, 468, 232, 3))
    for k, (what, rule) in enumerate((("left child of i", "2 * i + 1"), ("right child of i", "2 * i + 2"), ("parent of i", "(i - 1) // 2"))):
        y = 252 + k * 40
        cv.add(P.lift(cv, 462, y, 312, 32, "paper", 9, 3, hl=False))
        cv.add(cv.text(476, y + 22, what, 14.5, 700, anchor="start", fill=INK), cv.text(760, y + 22, rule, 15.5, 800, anchor="end", fill=INK, mono=True))
    cv.add(cv.text(400, 438, "highlighted: the item at index 1 and its two children, found by arithmetic alone, with no pointers", 13.5, 650, cls="il-ink2"))
    return figure(
        "heap-array", cv, "A binary heap drawn as a tree and stored in a list",
        "A min-heap holding 1, 3, 2, 5, 9 and 8. Drawn as a tree, 1 is at the top with 3 and 2 below it, and 5, 9 and 8 below those. Every parent is "
        "no bigger than its children, so the smallest item is always at the top. The same heap is stored in a list, level by level, as 1, 3, 2, 5, "
        "9, 8 at indexes 0 to 5, so a heap needs no pointers. The position of an item gives the position of its relatives: the left child of index "
        "i is at 2 times i plus 1, the right child at 2 times i plus 2, and the parent at i minus 1, divided by 2 and rounded down. For the item 3 "
        "at index 1 the children are at indexes 3 and 4, holding 5 and 9.",
        ["The heap property: every parent is smaller than or equal to its children, so the smallest item is at the root.",
         "The tree is complete, so it is stored in a list level by level, and no pointers are needed.",
         "Index arithmetic finds the family of any item: children at 2i + 1 and 2i + 2, parent at (i - 1) // 2."],
        "Adding or removing an item moves it along one branch of the tree, at most the height of the tree, which is why both cost O(log n).")


# ------------------------------------------------------------------ the trie

@illustration("trie-tree")
def _trie():
    cv = Canvas(800, 470).backdrop()
    cv.add(P.card(cv, 14, 24, 520, 424, 20, "a trie holding seven words", "teal"))
    pts = {"": (270, 80), "c": (170, 150), "d": (400, 150), "ca": (170, 220), "do": (400, 220),
           "car": (110, 290), "cat": (230, 290), "dog": (400, 290),
           "card": (50, 360), "care": (115, 360), "cart": (180, 360)}
    ends = {"car", "card", "care", "cart", "cat", "do", "dog"}
    on_path = {"", "c", "ca", "car"}
    sub = {"card", "care", "cart"}
    for key, (x, y) in pts.items():
        if key:
            px, py = pts[key[:-1]]
            hot = key in on_path or key in sub
            cv.add(edge(cv, px, py, x, y, "#C84B43" if key in on_path else ("#25B3BB" if key in sub else "#8AA0AC"), 3.6 if hot else 2.4))
    for key, (x, y) in pts.items():
        label = key[-1] if key else ""
        color = "paper" if not key else ("coral" if key in on_path else ("teal" if key in sub else "sky"))
        cv.add(node(cv, x, y, label if key else "root", color if key else "slate", 19 if key else 22, 17 if key else 12.5, double=key in ends, mono=bool(key)))
    cv.add(P.badge(cv, 42, 60, 1))
    cv.add(P.badge(cv, 456, 222, 2))
    # the words, listed
    cv.add(P.card(cv, 556, 24, 230, 424, 20, "typed so far: car", "coral"))
    cv.add(cv.text(671, 86, "suggest('car')", 15, 800, cls="il-ink", mono=True))
    for i, w in enumerate(("car", "card", "care", "cart")):
        y = 108 + i * 46
        cv.add(P.lift(cv, 586, y, 170, 36, "teal", 10, 4, hl=False), cv.text(671, y + 24, w, 17, 800, fill=INK, mono=True))
    cv.add(P.badge(cv, 580, 308, 3))
    cv.add(cv.text(671, 322, "not suggested:", 13.5, 700, cls="il-ink2"))
    for i, w in enumerate(("cat", "do", "dog")):
        cv.add(P.lift(cv, 586 + i * 58, 336, 52, 32, "slate", 9, 3, hl=False), cv.text(612 + i * 58, 358, w, 14.5, 800, fill=INK, mono=True))
    cv.add(cv.text(671, 400, "double ring = a word", 13, 650, cls="il-ink2"))
    cv.add(cv.text(671, 420, "ends here", 13, 650, cls="il-ink2"))
    return figure(
        "trie-tree", cv, "A trie of seven words, and the suggestions after typing car",
        "A trie is a tree in which each node is a letter and each path from the root spells a prefix. This one holds car, card, care, cart, cat, do "
        "and dog. Words that share a beginning share nodes: c, a and r are used by car, card, care and cart. A double ring marks a node where a word "
        "ends. Typing the letters c, a, r follows the highlighted path, and every word in the sub-tree below that node is a suggestion: car, card, "
        "care and cart. The words cat, do and dog are not below that node and are not suggested.",
        ["Each path from the root spells a prefix, and words that begin the same way share their first nodes.",
         "A double ring marks the end of a word, so car is a word and ca is not.",
         "Following the typed prefix leads to one node, and everything below it is a suggestion."],
        "Finding a word takes one step per letter, so the cost depends on the length of the word, not on how many words are stored.")


# ------------------------------------------------------------------ union-find

@illustration("union-find")
def _union_find():
    cv = Canvas(800, 570).backdrop()
    # before: a chain
    cv.add(P.card(cv, 14, 24, 772, 150, 20, "before: a chain, so find(0) takes four steps", "coral"))
    xs = [90 + i * 150 for i in range(5)]
    for i in range(4):
        cv.add(P.arrow(cv, [(xs[i] + 24, 96), (xs[i + 1] - 26, 96)], ARROW, 3, 10))
    for i, x in enumerate(xs):
        cv.add(node(cv, x, 96, str(i), "sun" if i == 4 else "sky", 22, 19, double=(i == 4)))
    cv.add(cv.text(xs[4], 144, "the root", 13, 750, cls="il-ink2"))
    cv.add(cv.text(xs[0], 144, "start here", 13, 750, cls="il-ink2"))
    cv.add(P.badge(cv, 42, 60, 1))
    # after: flattened
    cv.add(P.card(cv, 14, 196, 772, 170, 20, "after: every item points straight at the root", "mint"))
    root = (400, 250)
    for x, off in ((130, -26), (265, -10), (535, 10), (670, 26)):
        cv.add(P.arrow(cv, [(x, 322 - 24), (root[0] + off, root[1] + 20)], ARROW, 2.6, 9))
    cv.add(node(cv, root[0], root[1], "4", "sun", 22, 19, double=True))
    for x, t in ((130, "0"), (265, "1"), (535, "2"), (670, "3")):
        cv.add(node(cv, x, 322, t, "sky", 22, 19))
    cv.add(P.badge(cv, 42, 232, 2))
    cv.add(cv.text(400, 336, "find(0) is now one step", 13, 750, cls="il-ink2"))
    # union by size
    cv.add(P.card(cv, 14, 388, 772, 168, 20, "union by size: the smaller tree hangs under the bigger", "plum"))
    cv.add(P.badge(cv, 42, 424, 3))
    # the two trees before the union
    big = (120, 450)
    cv.add(edge(cv, big[0], big[1], 80, 506, "#8AA0AC", 2.6), edge(cv, big[0], big[1], 160, 506, "#8AA0AC", 2.6))
    cv.add(node(cv, big[0], big[1], "4", "sun", 20, 18, double=True), node(cv, 80, 506, "0", "sky", 18, 16), node(cv, 160, 506, "1", "sky", 18, 16))
    cv.add(cv.text(120, 540, "size 3", 12.5, 700, cls="il-ink2"))
    small = (260, 450)
    cv.add(edge(cv, small[0], small[1], 260, 506, "#8AA0AC", 2.6))
    cv.add(node(cv, small[0], small[1], "8", "mint", 20, 18, double=True), node(cv, 260, 506, "7", "sky", 18, 16))
    cv.add(cv.text(260, 540, "size 2", 12.5, 700, cls="il-ink2"))
    cv.add(P.arrow(cv, [(320, 480), (400, 480)], ARROW, 3.4, 11))
    cv.add(cv.text(360, 462, "union", 13.5, 800, cls="il-ink", mono=True))
    # after the union
    top = (580, 450)
    cv.add(edge(cv, top[0], top[1], 520, 506, "#8AA0AC", 2.6), edge(cv, top[0], top[1], 580, 506, "#8AA0AC", 2.6), edge(cv, top[0], top[1], 660, 500, "#8AA0AC", 2.6))
    cv.add(edge(cv, 660, 500, 660, 536, "#8AA0AC", 2.6))
    cv.add(node(cv, top[0], top[1], "4", "sun", 20, 18, double=True), node(cv, 520, 506, "0", "sky", 18, 16), node(cv, 580, 506, "1", "sky", 18, 16))
    cv.add(node(cv, 660, 500, "8", "mint", 18, 16), node(cv, 660, 538, "7", "sky", 16, 14))
    cv.add(cv.text(720, 454, "one group,", 13, 700, cls="il-ink2", anchor="middle"), cv.text(720, 472, "still shallow", 13, 700, cls="il-ink2", anchor="middle"))
    return figure(
        "union-find", cv, "Union-find: a chain of four links, the same group after path compression, and joining two groups by size",
        "Five items, 0 to 4, in one group. Before: the items form a chain, 0 points to 1, 1 to 2, 2 to 3 and 3 to 4, and 4 is the root of the group, "
        "so find of 0 has to follow four links. After the search, path compression has made every item on the way point straight at the root: 0, 1, 2 "
        "and 3 all point at 4, so the next find from any of them takes a single step. At the bottom, two groups are joined. A group of three items "
        "with root 4 and a group of two items with root 8 are merged by hanging the smaller group under the root of the bigger one, so the "
        "combined tree stays shallow.",
        ["A group is a tree stored in a list. Each item points at its parent, and a root points at itself.",
         "Path compression: while find walks up to the root it re-points every item it passes straight at the root.",
         "Union by size: the smaller tree is hung under the bigger one, so trees stay shallow."],
        "Together these make find and union take almost constant time, however large the groups become.")


# ------------------------------------------------------------------ minimum spanning tree

@illustration("mst-kruskal")
def _mst():
    cv = Canvas(800, 480).backdrop()
    pts = {"A": (70, 132), "B": (210, 78), "C": (390, 86), "D": (130, 258), "E": (310, 220), "F": (210, 384), "G": (430, 334)}
    edges = [("A", "B", 7), ("A", "D", 5), ("B", "C", 8), ("B", "D", 9), ("B", "E", 7), ("C", "E", 5), ("D", "E", 15),
             ("D", "F", 6), ("E", "F", 8), ("E", "G", 9), ("F", "G", 11)]
    chosen = {("A", "D"), ("C", "E"), ("D", "F"), ("A", "B"), ("B", "E"), ("E", "G")}
    cv.add(P.card(cv, 14, 24, 500, 432, 20, "a weighted graph and its minimum spanning tree", "teal"))
    for a, b, w in edges:
        (x1, y1), (x2, y2) = pts[a], pts[b]
        hot = (a, b) in chosen
        cv.add(edge(cv, x1, y1, x2, y2, "#0F7C84" if hot else "#9FB3BE", 5.2 if hot else 2.2, None if hot else "6 5"))
    for a, b, w in edges:
        (x1, y1), (x2, y2) = pts[a], pts[b]
        mx, my = (x1 + x2) / 2, (y1 + y2) / 2
        cv.add(cv.rect(mx - 14, my - 11, 28, 22, 8, "#FFFFFF", stroke="#C9D5DC", sw=1), cv.text(mx, my + 5.5, str(w), 14, 800, fill=INK, mono=True))
    for k, (x, y) in pts.items():
        cv.add(node(cv, x, y, k, "sun", 20, 18))
    cv.add(P.badge(cv, 44, 62, 1))
    cv.add(cv.text(264, 436, "six edges join seven towns, total weight 39", 14, 750, cls="il-ink"))
    # kruskal's order
    cv.add(P.card(cv, 534, 24, 252, 432, 20, "Kruskal's order", "coral"))
    order = [("AD", 5, True), ("CE", 5, True), ("DF", 6, True), ("AB", 7, True), ("BE", 7, True), ("BC", 8, False), ("EF", 8, False), ("BD", 9, False), ("EG", 9, True)]
    for i, (e, w, ok) in enumerate(order):
        y = 64 + i * 36
        cv.add(P.lift(cv, 552, y, 216, 28, "mint" if ok else "slate", 9, 3, hl=False))
        cv.add(cv.text(570, y + 20, e, 16, 800, anchor="start", fill=INK, mono=True), cv.text(630, y + 20, str(w), 16, 800, anchor="start", fill=INK, mono=True))
        cv.add(cv.text(752, y + 20, "keep" if ok else "cycle", 13.5, 800, anchor="end", fill=INK))
    cv.add(P.badge(cv, 566, 416, 2))
    cv.add(cv.text(590, 412, "cheapest edge first,", 12.5, 650, anchor="start", cls="il-ink2"), cv.text(590, 430, "skipping any that make a loop", 12.5, 650, anchor="start", cls="il-ink2"))
    return figure(
        "mst-kruskal", cv, "Kruskal's algorithm choosing a minimum spanning tree of seven towns",
        "A weighted graph of seven towns, A to G, with eleven possible links whose weights are the costs. The minimum spanning tree connects every "
        "town as cheaply as possible and is drawn with thick lines: A to D at 5, C to E at 5, D to F at 6, A to B at 7, B to E at 7 and E to G at "
        "9, six edges in all with a total weight of 39. The rest are drawn dashed and are not used. Kruskal's algorithm sorts the edges by weight "
        "and takes them in order: A D, C E, D F, A B and B E are kept. B C, E F and B D are rejected because each would join two towns that are "
        "already connected, making a cycle. E G is kept.",
        ["The thick edges are the minimum spanning tree: every vertex joined, no cycles, the smallest total weight.",
         "Kruskal sorts the edges, then takes each in turn unless it would make a cycle. Union-find answers that question."],
        "A spanning tree of seven vertices always has six edges. It is not the same as a shortest path: it connects everything cheaply, not one place to another.")


# ------------------------------------------------------------------ greedy against optimal

@illustration("greedy-vs-optimal")
def _greedy():
    cv = Canvas(800, 440).backdrop()
    for k, (title, color, coins, count, note) in enumerate((
            ("greedy: biggest coin first", "coral", (4, 1, 1), "3 coins", "stuck with two 1p coins"),
            ("the best answer", "mint", (3, 3), "2 coins", "found by working from smaller amounts"))):
        x = 14 + k * 396
        cv.add(P.card(cv, x, 78, 376, 280, 20, title, color))
        cv.add(P.badge(cv, x + 26, 118, k + 1))
        for i, c in enumerate(coins):
            cx = x + 188 + (i - (len(coins) - 1) / 2) * 92
            cv.add(cv.circle(cx, 196 + 4, 36, "#10303A", op=.16))
            cv.add(cv.circle(cx, 196, 36, cv.g("sun" if c != 1 else "slate"), stroke=PAL["sun" if c != 1 else "slate"][2], sw=3))
            cv.add(cv.circle(cx, 196, 28, "none", stroke=PAL["sun" if c != 1 else "slate"][2], sw=1.4, op=.6))
            cv.add(cv.text(cx, 208, "%dp" % c, 26, 800, fill=INK, mono=True))
        cv.add(cv.text(x + 188, 284, " + ".join(str(c) for c in coins) + " = 6p", 20, 800, cls="il-ink", mono=True))
        cv.add(P.pill(cv, x + 188, 322, count, color, 20, 20, 36, 800))
    cv.add(cv.text(400, 38, "make 6p from coins worth 1p, 3p and 4p", 19, 800, cls="il-ink"))
    cv.add(cv.text(412, 396, "greedy never goes back to reconsider the 4p, so it is fast and sometimes wrong", 15, 750, cls="il-ink"))
    cv.add(P.badge(cv, 30, 390, 3))
    return figure(
        "greedy-vs-optimal", cv, "Making 6p from 1p, 3p and 4p coins: the greedy answer and the best answer",
        "Coins of 1p, 3p and 4p have to make 6p. A greedy algorithm takes the biggest coin that fits each time: a 4p coin, then two 1p coins, "
        "which is three coins. It never goes back to reconsider the 4p. The best answer is two 3p coins, which is only two coins. Greedy is fast and "
        "simple, but it only gives the best answer for problems where taking the best local choice is provably safe.",
        ["Greedy takes the best looking choice at each step and never reconsiders: 4p first leaves 2p to make from 1p coins.",
         "A different first choice does better: two 3p coins make 6p. Dynamic programming finds it by working up from smaller amounts.",
         "A greedy algorithm is only guaranteed to be best when the greedy choice is proved to be safe."],
        "For British coins greedy happens to be optimal, which is why it seems so natural. Change the coins and it can fail.")


# ------------------------------------------------------------------ dynamic programming table

@illustration("dp-coin-table")
def _dp_table():
    cv = Canvas(800, 470).backdrop()
    best = [0, 1, 2, 1, 1, 2, 2, 2]
    cv.add(P.card(cv, 14, 24, 772, 422, 20, "fewest coins to make each amount, with coins of 1p, 3p and 4p", "teal"))
    bx, by, bw, gap = 46, 232, 76, 8
    for a in range(8):
        x = bx + a * (bw + gap)
        color = "coral" if a == 6 else ("mint" if a < 6 else "slate")
        cv.add(P.lift(cv, x, by, bw, 62, color, 10, 5, hl=False))
        cv.add(cv.text(x + bw / 2, by + 41, str(best[a]) if a < 7 else "?", 26, 800, fill=INK, mono=True))
        cv.add(cv.text(x + bw / 2, by + 96, "%dp" % a, 15, 700, cls="il-ink2", mono=True))
    cv.add(cv.text(400, 80, "to make 6p, try each coin as the LAST coin and look up what is left", 16, 800, cls="il-ink"))
    cv.add(P.badge(cv, 46, 74, 1))
    # three tracks into the box for 6p, one per coin, at different heights
    tx = bx + 6 * (bw + gap) + bw / 2
    for src, coin, cand, track, hot in ((5, 1, 3, 30, False), (3, 3, 2, 62, True), (2, 4, 3, 94, False)):
        sx = bx + src * (bw + gap) + bw / 2
        ty = by - track
        col = "#C84B43" if hot else "#8799A7"
        cv.add(cv.path("M%s %s L%s %s L%s %s" % (_n(sx), _n(by - 4), _n(sx), _n(ty), _n(tx - (6 if hot else 0)), _n(ty)), stroke=col, sw=3.4 if hot else 2.4, dash=None if hot else "6 5"))
        cv.add(P.arrow(cv, [(tx - (6 if hot else 0), ty), (tx - (6 if hot else 0), by - 6)], col, 3.4 if hot else 2.4, 9, dash=None if hot else "6 5"))
        label = "%dp, then a %dp coin: %d" % (src, coin, cand)
        lw = 8.4 * len(label) + 14
        lx = tx - 16 - lw / 2
        cv.add(cv.rect(lx - lw / 2, ty - 25, lw, 22, 11, "#FFFFFF", stroke=col, sw=1.6))
        cv.add(cv.text(lx, ty - 9.5, label, 12.5, 800, fill=INK, mono=True))
    cv.add(P.badge(cv, 66, 352, 2))
    cv.add(cv.text(420, 364, "best[a] = 1 + the smallest best[a - coin]", 18, 800, cls="il-ink", mono=True))
    cv.add(cv.text(400, 396, "for 6p the three choices give 3, 2 and 3, and the smallest is 2", 14.5, 700, cls="il-ink2"))
    cv.add(cv.text(400, 426, "each box is worked out once from boxes already filled in", 15, 700, cls="il-ink"))
    return figure(
        "dp-coin-table", cv, "A dynamic programming table: the fewest coins for each amount",
        "A row of boxes for the amounts 0p to 7p, holding the fewest coins needed with coins of 1p, 3p and 4p: 0, 1, 2, 1, 1, 2, then 2 for 6p and 2 "
        "for 7p. To fill the box for 6p, try each coin as the last coin and look up what is left, which is already in the table. A 1p coin leaves "
        "5p, which needs 2 coins, making 3. A 3p coin leaves 3p, which needs 1 coin, making 2. A 4p coin leaves 2p, which needs 2 coins, making 3. "
        "The smallest is 2. The rule is best of a equals 1 plus the smallest best of a minus coin. Every box is worked out once from boxes that "
        "are already filled in.",
        ["Try each coin as the last coin used. Each leaves a smaller amount whose answer is already in the table.",
         "Take 1 plus the smallest of those answers. Every box is worked out once, from the boxes before it."],
        "Storing sub-answers instead of recalculating them turns an exponential search into a table with one box per amount.")


# ------------------------------------------------------------------ finite state machines

def loop_arrow(cv, x, y, r, up=True, color=ARROW):
    """A small loop on top of (or below) a state, with a head."""
    s = -1 if up else 1
    d = "M%s %s C%s %s %s %s %s %s" % (_n(x - 12), _n(y + s * (r - 1)), _n(x - 36), _n(y + s * (r + 46)), _n(x + 36), _n(y + s * (r + 46)), _n(x + 12), _n(y + s * (r + 3)))
    out = cv.path(d, stroke=color, sw=2.8)
    out += cv.poly([(x + 12, y + s * (r - 1)), (x + 20, y + s * (r + 14)), (x + 4, y + s * (r + 12))], color)
    return out


@illustration("fsm-states")
def _fsm():
    cv = Canvas(800, 470).backdrop()
    # even number of 1s
    cv.add(P.card(cv, 14, 24, 384, 424, 20, "accepts an even number of 1s", "teal"))
    ex, ox, cy = 110, 300, 250
    cv.add(P.arrow(cv, [(40, cy), (ex - 36, cy)], ARROW, 3, 10))
    cv.add(cv.text(46, cy - 14, "start", 12.5, 700, anchor="start", cls="il-ink2"))
    cv.add(node(cv, ex, cy, "even", "mint", 30, 15, double=True, mono=False))
    cv.add(node(cv, ox, cy, "odd", "coral", 30, 15, mono=False))
    cv.add(P.curve_arrow(cv, (ex + 26, cy - 22), (ex + 70, cy - 78), (ox - 70, cy - 78), (ox - 26, cy - 22), ARROW, 3, 11))
    cv.add(cv.text((ex + ox) / 2, cy - 72, "1", 18, 800, cls="il-ink", mono=True))
    cv.add(P.curve_arrow(cv, (ox - 26, cy + 22), (ox - 70, cy + 78), (ex + 70, cy + 78), (ex + 26, cy + 22), ARROW, 3, 11))
    cv.add(cv.text((ex + ox) / 2, cy + 86, "1", 18, 800, cls="il-ink", mono=True))
    cv.add(loop_arrow(cv, ex, cy, 30, True), cv.text(ex, cy - 98, "0", 18, 800, cls="il-ink", mono=True))
    cv.add(loop_arrow(cv, ox, cy, 30, True), cv.text(ox, cy - 98, "0", 18, 800, cls="il-ink", mono=True))
    cv.add(P.badge(cv, 42, 66, 1))
    cv.add(cv.text(206, 408, "1011  ends in odd: rejected", 13.5, 700, cls="il-ink2", mono=True))
    # turnstile
    cv.add(P.card(cv, 414, 24, 372, 424, 20, "a turnstile: locked or unlocked", "sun"))
    lx, ux = 500, 700
    cv.add(P.arrow(cv, [(436, cy), (lx - 36, cy)], ARROW, 3, 10))
    cv.add(node(cv, lx, cy, "locked", "coral", 34, 14.5, mono=False))
    cv.add(node(cv, ux, cy, "unlocked", "mint", 34, 13, mono=False))
    cv.add(P.curve_arrow(cv, (lx + 28, cy - 24), (lx + 70, cy - 80), (ux - 70, cy - 80), (ux - 30, cy - 26), ARROW, 3, 11))
    cv.add(cv.text((lx + ux) / 2, cy - 72, "coin", 15, 800, cls="il-ink", mono=True))
    cv.add(P.curve_arrow(cv, (ux - 30, cy + 26), (ux - 70, cy + 80), (lx + 70, cy + 80), (lx + 28, cy + 24), ARROW, 3, 11))
    cv.add(cv.text((lx + ux) / 2, cy + 90, "push", 15, 800, cls="il-ink", mono=True))
    cv.add(loop_arrow(cv, lx, cy, 34, True), cv.text(lx, cy - 104, "push", 14, 800, cls="il-ink", mono=True))
    cv.add(loop_arrow(cv, ux, cy, 34, True), cv.text(ux, cy - 104, "coin", 14, 800, cls="il-ink", mono=True))
    cv.add(P.badge(cv, 442, 66, 2))
    cv.add(cv.text(600, 408, "state table: (state, input) gives the next state", 13.5, 700, cls="il-ink2"))
    return figure(
        "fsm-states", cv, "Two finite state machines drawn as state transition diagrams",
        "Left: a machine that accepts binary strings with an even number of 1s. It has two states, even, drawn with a double ring because it is the "
        "accepting state and marked as the start, and odd. Reading a 0 keeps the machine where it is, and reading a 1 moves it to the other state. "
        "The string 1011 has three 1s and ends in odd, so it is rejected. Right: a turnstile with two states, locked and unlocked. A coin moves it "
        "from locked to unlocked, and a push moves it from unlocked back to locked. A push while locked, or a coin while unlocked, leaves it as it is.",
        ["States are circles, transitions are labelled arrows, and a double ring marks an accepting state. The only memory is which state it is in.",
         "A turnstile is a machine too: every input in every state has exactly one next state, which is what a state transition table lists."],
        "A machine is data: the whole behaviour is in the table, and one short loop can run any machine.")


# ------------------------------------------------------------------ syntax trees

def op_node(cv, x, y, label, color):
    return node(cv, x, y, label, color, 22, 20)


@illustration("ast-precedence")
def _ast():
    cv = Canvas(800, 480).backdrop()
    for k, (src, value) in enumerate((("2 + 3 * 4", 14), ("(2 + 3) * 4", 20))):
        x0 = 14 + k * 396
        cv.add(P.card(cv, x0, 24, 376, 432, 20, src, "teal" if k == 0 else "plum"))
        cx = x0 + 188
        if k == 0:
            nodes = {"root": (cx, 100), "l": (cx - 90, 190), "r": (cx + 70, 190), "rl": (cx, 280), "rr": (cx + 140, 280)}
            lab = {"root": ("+", "coral"), "l": ("2", "sky"), "r": ("*", "sun"), "rl": ("3", "sky"), "rr": ("4", "sky")}
            links = (("root", "l"), ("root", "r"), ("r", "rl"), ("r", "rr"))
            code = ["PUSH 2", "PUSH 3", "PUSH 4", "MUL", "ADD"]
        else:
            nodes = {"root": (cx, 100), "l": (cx - 70, 190), "r": (cx + 90, 190), "ll": (cx - 140, 280), "lr": (cx, 280)}
            lab = {"root": ("*", "sun"), "l": ("+", "coral"), "r": ("4", "sky"), "ll": ("2", "sky"), "lr": ("3", "sky")}
            links = (("root", "l"), ("root", "r"), ("l", "ll"), ("l", "lr"))
            code = ["PUSH 2", "PUSH 3", "ADD", "PUSH 4", "MUL"]
        for a, b in links:
            cv.add(edge(cv, nodes[a][0], nodes[a][1], nodes[b][0], nodes[b][1], "#8AA0AC", 2.8))
        for key, (nx, ny) in nodes.items():
            t, c = lab[key]
            cv.add(node(cv, nx, ny, t, c, 22, 20))
        cv.add(P.badge(cv, x0 + 28, 66, k + 1))
        cv.add(cv.text(cx, 338, "evaluate the lower nodes first", 13, 700, cls="il-ink2"))
        for i, c in enumerate(code):
            cv.add(P.lift(cv, x0 + 22 + i * 68, 358, 62, 32, "paper", 8, 3, hl=False), cv.text(x0 + 22 + i * 68 + 31, 379, c, 11.5, 800, fill=INK, mono=True))
        cv.add(P.pill(cv, cx, 428, "result: %d" % value, "mint", 17, 16, 32, 800))
    return figure(
        "ast-precedence", cv, "Two syntax trees: brackets change the shape of the tree, not the rules",
        "Two abstract syntax trees. On the left is 2 plus 3 times 4. The plus is at the top, with 2 on the left and a times node on the right, whose "
        "children are 3 and 4. The times is lower in the tree, so it is worked out first, and the answer is 14. The instructions for a stack machine "
        "come from visiting the tree left, right, then the operator: push 2, push 3, push 4, multiply, add. On the right is the expression with "
        "brackets, 2 plus 3 in brackets, times 4. Now the plus is lower, and the times is at the top, so the answer is 20. The instructions are "
        "push 2, push 3, add, push 4, multiply.",
        ["Operators lower in the tree are worked out first, so precedence is built into the shape of the tree.",
         "Brackets change the shape of the tree, not the rules. The brackets themselves are gone from the tree."],
        "Visiting the tree left, then right, then the operator, gives the postfix order a stack machine runs.")


# ------------------------------------------------------------------ a regular expression taken apart

@illustration("regex-anatomy")
def _regex():
    cv = Canvas(800, 450).backdrop()
    cv.add(P.card(cv, 14, 24, 772, 232, 20, "a UK number plate pattern, one piece at a time", "teal"))
    parts = [("[A-Z]{2}", "two capital", "letters", "sky", "AB"), ("[0-9]{2}", "two", "digits", "mint", "12"),
             ("' '", "one", "space", "sun", None), ("[A-Z]{3}", "three capital", "letters", "coral", "CDE")]
    for i, (code, l1, l2, color, got) in enumerate(parts):
        x = 64 + i * 174
        cx = x + 75
        cv.add(P.lift(cv, x, 84, 150, 54, color, 12, 5, hl=False), cv.text(cx, 118, code, 21, 800, fill=INK, mono=True))
        cv.add(cv.text(cx, 168, l1, 13.5, 750, cls="il-ink"), cv.text(cx, 186, l2, 13.5, 750, cls="il-ink"))
        cv.add(P.arrow(cv, [(cx, 198), (cx, 214)], ARROW, 2.4, 8))
        cv.add(cv.rect(cx - 50, 218, 100, 28, 9, "#FFFFFF", stroke=PAL[color][2], sw=2.4))
        if got:
            cv.add(cv.text(cx, 239, got, 18, 800, fill=INK, mono=True))
        else:
            cv.add(cv.path("M%s 226 L%s 236 L%s 236 L%s 226" % (_n(cx - 10), _n(cx - 10), _n(cx + 10), _n(cx + 10)), stroke=INK, sw=2.6))
    cv.add(P.badge(cv, 42, 64, 1))
    cv.add(P.card(cv, 14, 286, 772, 150, 20, "three strings tried against it with re.fullmatch", "sun"))
    tries = [("AB12 CDE", True, "every piece matches"), ("ab12 cde", False, "lower case: [A-Z] fails"), ("AB12CDE", False, "no space: ' ' fails")]
    for i, (text, ok, why) in enumerate(tries):
        x = 36 + i * 250
        col = "#2F9F77" if ok else "#C84B43"
        cv.add(cv.rect(x, 330, 232, 88, 14, "#FFFFFF", stroke=col, sw=2.6))
        cv.add(cv.text(x + 116, 364, text, 22, 800, fill=INK, mono=True))
        cv.add((P.tick if ok else P.cross)(cv, x + 24, 396, 11), cv.text(x + 44, 401, why, 13, 750, anchor="start", fill=INK))
    cv.add(P.badge(cv, 42, 308, 2))
    return figure(
        "regex-anatomy", cv, "A regular expression for a UK number plate, taken apart and tried on three strings",
        "The pattern is made of four pieces in a row. The first piece, a capital letter from A to Z repeated twice, matches two capital letters. "
        "The second, a digit from 0 to 9 repeated twice, matches two digits. The third is a single space. The fourth, a capital letter repeated "
        "three times, matches three capital letters. Under each piece sits the part of the text it matched in AB12 CDE: AB, then 12, then the "
        "space, then CDE. Below, three strings are tried with re dot fullmatch. AB12 CDE matches because every piece matches. ab12 cde fails "
        "because the letters are lower case. AB12CDE fails because there is no space.",
        ["A pattern is a row of small pieces. Each piece describes the kind of characters that may come next, and how many.",
         "fullmatch asks for the whole string to fit. One piece that fails, whether letters in the wrong case or a missing space, rejects the string."],
        "A regular expression is a compact way of writing a set of strings, and it describes exactly the languages a finite state machine can accept.")
