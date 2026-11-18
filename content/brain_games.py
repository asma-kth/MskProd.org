"""The three brain games on every stretch task page: Odd One Out, Memory
Flash and Fact or Fib.

None of them has questions of its own. Each one replays the lesson's checked
material in a new way, so it asks only what the lesson teaches:

  Odd One Out (logic)   Link Up's groups: three tiles from one group and one
                        from another. Tap the tile that does not belong.
  Memory Flash (memory) Memory Match's pairs: study the cards, they flip
                        over, then find the card for each clue from memory.
  Fact or Fib (speed)   Bug Hunt's true statements and its bugs, with the
                        lesson's true or false quiz questions. Decide fast.

Link Up only promises that its twelve tiles split into three groups one way.
Odd One Out asks more: the tile from another group must not belong with the
other three by any fair reading. AVOID lists, lesson by lesson, the mixes that
fail that test, found by reading every group of every lesson. The checks below
prove each rule names real groups and tiles, and that every lesson still has
plenty of rounds to play.
"""
import re

# The lesson's key, as its page and saved results know it, then the mixes to
# avoid:
#   ("pair", A, B)   never put a tile of group A among three of group B, or
#                    the other way round
#   ("into", A, B)   never put a tile of group A among three of group B
#   ("tile", T, B)   never put tile T among three of group B; B "*" means any
AVOID = {
    # Year 7
    "using-computers/3": [("pair", "Too easy to guess", "Risky habits")],
    "programming-in-scratch/2": [("tile", "score > 10", "Variable blocks"),
                                 ("into", "Things a variable can store", "Variable blocks")],
    "vector-graphics/1": [("pair", "Describes a bitmap", "Bitmap file types")],
    "vector-graphics/2": [("tile", "Group", "Combine shapes into a new one"),
                          ("tile", "Ungroup", "Combine shapes into a new one")],
    # Year 8
    "digital-literacy/2": [("pair", "Signs of a phishing email", "Other scams")],
    "computational-thinking/1": [("tile", "One rule for many cases", "Abstraction")],
    "spreadsheets/3": [("tile", "Your height as you grow", "Best as a scatter graph"),
                       ("tile", "Age and reaction time", "Best as a line chart")],
    "networks-and-cyber-security/3": [("into", "Facts about encryption", "Other defences")],
    "web-development/3": [("pair", "Accessibility", "Testing")],
    # Year 9
    "digital-literacy-and-the-law/1": [("tile", "Publishing someone's photo", "Breaks the Data Protection Act")],
    "app-development/2": [("tile", "Are you sure? on Delete", "Feedback")],
    "artificial-intelligence/1": [("tile", "Classify new images", "Everyday uses of AI")],
    "3d-modelling-and-animation/1": [("into", "Primitive shapes", "Building blocks of a model")],
    "3d-modelling-and-animation/2": [("tile", "Metallic look", "True of a texture")],
    "3d-modelling-and-animation/3": [("into", "Follow through", "Easing")],
    # OCR J277
    "ks4/ocr/primary-storage": [("tile", "Slower than RAM", "Non volatile storage"),
                                ("tile", "Swap file", "Non volatile storage"),
                                ("tile", "Hard disk", "Virtual memory"),
                                ("tile", "SSD", "Virtual memory")],
    "ks4/ocr/secondary-storage": [("tile", "Lowest cost per GB", "Optical"),
                                  ("tile", "Moving read head", "Optical")],
    "ks4/ocr/compression": [("tile", "Photo on a web page", "Lossless")],
    "ks4/ocr/networks-and-topologies": [("pair", "Network hardware", "LAN"), ("pair", "Network hardware", "WAN")],
    "ks4/ocr/computational-thinking": [("tile", "Easier to understand", "Qualities of a good algorithm")],
    "ks4/ocr/designing-algorithms": [("tile", "endwhile", "Condition controlled loops")],
    "ks4/ocr/searching-and-sorting": [("pair", "Linear search", "Insertion sort"),
                                      ("tile", "Little extra memory", "*"),
                                      ("tile", "Stops at the first match", "Binary search"),
                                      ("tile", "Up to n checks for n items", "Binary search")],
    # AQA 8525
    "ks4/aqa/computational-thinking": [("pair", "Benefits of decomposition", "Benefits of abstraction")],
    "ks4/aqa/sorting-algorithms": [("into", "Both sorts", "Bubble sort"), ("into", "Both sorts", "Merge sort")],
    "ks4/aqa/robust-and-secure-programming": [("tile", "1", "Normal, for a mark of 1 to 50"),
                                              ("tile", "50", "Normal, for a mark of 1 to 50"),
                                              ("tile", "0", "Erroneous, for a mark of 1 to 50"),
                                              ("tile", "51", "Erroneous, for a mark of 1 to 50")],
    "ks4/aqa/systems-architecture": [("tile", "Next instruction's address", "MAR"),
                                     ("tile", "Gets a copy of the PC", "PC")],
    "ks4/aqa/cyber-security": [("tile", "Pharming", "Malware")],
    "ks4/aqa/ethical-legal-and-environmental-impacts": [("tile", "Vendor support", "Open source")],
    # Edexcel 1CP2
    "ks4/edexcel/networks-and-network-security": [("pair", "Star topology", "Wireless"),
                                                  ("tile", "Scales well for wireless", "*"),
                                                  ("tile", "Easy to extend", "Mesh topology")],
    "ks4/edexcel/issues-and-impact-of-technology": [("tile", "Available anywhere", "Wearables and implants")],
    # Creative iMedia
    "ks4/imedia/the-media-industry": [("into", "Audio", "Digital and interactive")],
    "ks4/imedia/client-requirements-and-the-brief": [("pair", "Deliverables", "Constraints"),
                                                     ("into", "Content", "Constraints"),
                                                     ("tile", "House style fonts", "Content")],
    "ks4/imedia/target-audience-and-segmentation": [("into", "Older audience", "International audience")],
    "ks4/imedia/style-content-and-layout": [("pair", "Magazine", "Poster"), ("into", "Poster", "Web page"),
                                            ("tile", "Masthead", "Web page"), ("tile", "Logo top left", "*")],
    "ks4/imedia/pre-production-documents": [("tile", "Every screen as a box", "Storyboard"),
                                            ("tile", "Transition to next shot", "Navigation diagram")],
    "ks4/imedia/work-planning-and-workflow": [("pair", "Resources", "Contingency for a shoot"),
                                              ("tile", "Backup in a second place", "Contingency for a shoot")],
    "ks4/imedia/legislation-and-permissions": [("into", "Clear before filming", "Data Protection Act")],
    "ks4/imedia/file-formats-and-properties": [("pair", "Print poster", "Logo for any use"),
                                               ("pair", "Website hero image", "Logo for any use"),
                                               ("tile", "JPG or WEBP", "Print poster")],
    "ks4/imedia/distribution-platforms": [("tile", "Alt text", "Social feeds"), ("tile", "Privacy declaration", "Email")],
    "ks4/imedia/visual-identity-and-digital-graphics": [("tile", "Minimum size", "Refining a logo"),
                                                        ("tile", "Legible at smallest size", "Style guide contents"),
                                                        ("tile", "Works in one colour", "Style guide contents")],
    "ks4/imedia/planning-digital-graphics": [("pair", "Asset table columns", "Decide before designing"),
                                             ("pair", "On the visualisation diagram", "Decide before designing"),
                                             ("tile", "Dimensions", "On the visualisation diagram"),
                                             ("tile", "Format", "On the visualisation diagram")],
    "ks4/imedia/interactive-digital-media": [("into", "Interface principles", "Accessibility")],
    "ks4/imedia/reviewing-interactive-media": [("tile", "Reflection on process", "Opinion, not evidence")],
}

# Memory Flash shows a few of Memory Match's cards at a time, so a clue must
# fit only its own card. These cards are left out because their clue fits
# another card of the lesson as well: a general term beside its own examples
# ("Iteration" beside repeat blocks), or a property shared by others ("In
# place" beside sorts that work in place). Found by reading every pair.
FLASH_DROP = {
    "using-computers/1": ["Software"],
    "programming-in-scratch/2": ["if ... else"],
    "programming-in-scratch/3": ["Iteration"],
    "introduction-to-python/1": ["score = score + 10"],
    "introduction-to-python/2": ["input()"],
    "vector-graphics/1": ["Scalable", "SVG"],
    "digital-literacy/1": ["Digital footprint"],
    "spreadsheets/2": ["Absolute reference"],
    "digital-literacy-and-the-law/2": ["Cookie"],
    "python-programming/1": ["Subroutine"],
    "ks4/ocr/primary-storage": ["Volatile", "Swap file"],
    "ks4/ocr/character-encoding": ["Character set"],
    "ks4/ocr/compression": ["Lossy", "Lossless"],
    "ks4/ocr/searching-and-sorting": ["In place"],
    "ks4/aqa/computational-thinking": ["Algorithm"],
    "ks4/aqa/sorting-algorithms": ["In place"],
    "ks4/aqa/hardware-software-and-the-operating-system": ["Software", "Utility"],
    "ks4/edexcel/searching-and-sorting-algorithms": ["Divide and conquer", "In place"],
}

# The question Memory Flash asks, by the lesson's two kinds of card.
FLASH_ASK = {
    ("Term", "Meaning"): "Which term means this?",
    ("Code", "Output"): "Which code gives this output?",
    ("Code", "Meaning"): "Which code does this?",
    ("Binary", "Denary"): "Which binary number equals this?",
    ("Hex", "Denary"): "Which hex number equals this?",
    ("Value", "Denary"): "Which value equals this?",
    ("Stage", "Meaning"): "Which stage is this?",
    ("Unit", "Size"): "Which unit is this size?",
    ("Protocol", "Job"): "Which protocol does this job?",
    ("Component", "Job"): "Which component does this job?",
    ("Expression", "Value"): "Which expression gives this value?",
    ("Operation", "Result"): "Which operation gives this result?",
    ("Python", "Result"): "Which Python code gives this result?",
    ("Extension", "File type"): "Which extension is this type of file?",
    ("Block", "Meaning"): "Which block does this?",
    ("Operator", "Meaning"): "Which operator means this?",
    ("Function", "Meaning"): "Which function does this?",
    ("Tag", "Meaning"): "Which tag is this?",
    ("CSS", "Meaning"): "Which CSS does this?",
    ("Item", "Meaning"): "Which of these is this?",
    ("Algorithm", "How it works"): "Which algorithm works like this?",
    ("AQA", "Meaning"): "Which AQA pseudocode means this?",
    ("Document", "What it is"): "Which document is this?",
}

# The games show no dashes. Words that read as well without one are written
# without; anything else that still has a dash, such as code with a minus
# sign, is left out of the brain games.
DASH = re.compile("[-\u2010-\u2015\u2212]")
FIXES = [("E-waste", "Electronic waste"), ("e-waste", "electronic waste"), ("Self-driving", "Self driving"),
         ("One-way", "One way"), ("Two-way", "Two way"), ("Non-volatile", "Non volatile"),
         ("Real-time", "Real time"), ("real-time", "real time"), ("Blu-ray", "Blu ray"),
         ("Sub-problem", "Sub problem"), ("sub-problems", "sub problems"), ("self-contained", "self contained"),
         ("count-controlled", "count controlled"), ("condition-controlled", "condition controlled"),
         ("High-level", "High level"), ("high-level", "high level"), ("24-bit", "24 bit"), ("f-string", "f string"),
         ("Multi-platform", "Multi platform"), ("sub-lists", "sub lists"), ("five-item", "five item"),
         ("variable-width", "variable width"), ("Wi-Fi", "WiFi"), ("full-size", "full size"), ("LEN - 1", "LEN minus 1"),
         ("Pre-production", "Pre production"), ("pre-production", "pre production")]


def tidy(text):
    for a, b in FIXES:
        text = text.replace(a, b)
    return text


def clean(text):
    """The text with its dashes written out, or None if a dash is left."""
    t = tidy(text or "")
    return None if DASH.search(t) else t


ODD_ROUNDS = 8          # rounds in one game of Odd One Out
ODD_MIN_PUZZLES = 24    # different rounds a lesson must offer, so eight rarely repeat
FIB_DEAL = 12           # statements in one game of Fact or Fib
FIB_MAX_FIBS = 6        # at most this many of them false
FIB_MIN = (5, 6)        # a lesson needs at least this many false, and true, statements
FLASH_LEVELS = (3, 4, 6)  # cards on the table at each level of Memory Flash, with six pairs to play
FLASH_MIN = 4             # pairs Memory Flash needs; with fewer than six the levels shrink to fit
STATEMENT_MAX = 120     # characters on a Fact or Fib card

_MARKS = re.compile(r"[`*_]")


def _plain(s):
    return _MARKS.sub("", s or "").strip()


def odd_intruders(key, st):
    """For each of the lesson's groups, the tiles of other groups that may be
    the odd one out among three of its tiles: [[(group, tile), ...], ...] by
    index. Raises ValueError naming any rule that does not fit the lesson."""
    names = [_plain(g.name) for g in st.groups]
    tiles = [[_plain(t) for t in g.tiles] for g in st.groups]
    where = {}
    for gi, ts in enumerate(tiles):
        for ti, t in enumerate(ts):
            where.setdefault(t, []).append((gi, ti))
    banned = set()           # (intruder group, intruder tile, trio group)

    def group(name):
        if name not in names:
            raise ValueError("%s: Odd One Out rule names a group the lesson does not have: %r" % (key, name))
        return names.index(name)

    for rule in AVOID.get(key, []):
        kind = rule[0]
        if kind in ("pair", "into"):
            a, b = group(rule[1]), group(rule[2])
            if a == b:
                raise ValueError("%s: Odd One Out rule mixes a group with itself: %r" % (key, rule))
            for ti in range(len(tiles[a])):
                banned.add((a, ti, b))
            if kind == "pair":
                for ti in range(len(tiles[b])):
                    banned.add((b, ti, a))
        elif kind == "tile":
            if rule[1] not in where:
                raise ValueError("%s: Odd One Out rule names a tile the lesson does not have: %r" % (key, rule[1]))
            targets = range(len(names)) if rule[2] == "*" else [group(rule[2])]
            for gi, ti in where[rule[1]]:
                for b in targets:
                    if b == gi and rule[2] != "*":
                        raise ValueError("%s: tile %r is already in group %r" % (key, rule[1], rule[2]))
                    banned.add((gi, ti, b))
        else:
            raise ValueError("%s: unknown Odd One Out rule %r" % (key, rule))
    out = []
    for b in range(len(names)):
        ok = [(a, ti) for a in range(len(names)) if a != b for ti in range(len(tiles[a])) if (a, ti, b) not in banned]
        out.append(ok)
    return out


def odd_puzzles(intruders, groups):
    """How many different rounds the lesson offers: three of a group's tiles
    and one allowed intruder."""
    total = 0
    for b, ok in enumerate(intruders):
        n = len(groups[b].tiles)
        trios = n * (n - 1) * (n - 2) // 6
        total += trios * len(ok)
    return total


def fib_deck(st):
    """Every statement Fact or Fib can deal: (text, is it true, why). The
    true ones are Bug Hunt's true statements and the quiz's true or false
    questions that are true; the false ones are Bug Hunt's bugs, with their
    fixes, and the quiz's false ones, with their explanations. A statement
    that cannot be written without a dash is left out."""
    raw = []
    for b in st.bugs:
        for t in b.truths:
            raw.append((t, True, ""))
        raw.append((b.bug, False, b.fix))
    for q in st.blitz:
        if q.kind == "tf" and not q.code:
            raw.append((q.q, bool(q.answer), q.explain))
    deck = []
    for t, ok, why in raw:
        t2, why2 = clean(t), clean(why)
        if t2 is not None and why2 is not None:
            deck.append((t2, ok, why2))
    return deck


def flash_pairs(key, st):
    """The pairs Memory Flash plays: Memory Match's, less any whose clue
    fits another card and any that cannot be written without a dash."""
    drop = set(FLASH_DROP.get(key, []))
    out = []
    for p in st.pairs:
        a, b = clean(p.a), clean(p.b)
        if a is None or b is None or _plain(p.a) in drop:
            continue
        out.append((a, b))
    return out


def flash_levels(n):
    """Cards on the table at each of the three levels, for n pairs."""
    return list(FLASH_LEVELS) if n >= 6 else [3, 4, 5] if n == 5 else [2, 3, 4]


def flash_ask(st):
    return FLASH_ASK.get(tuple(st.pair_names), "Which card goes with this?")


def problems(key, st):
    """Everything that stops this lesson's brain games being played fairly."""
    out = []
    try:
        intruders = odd_intruders(key, st)
    except ValueError as e:
        return [str(e)]
    n = odd_puzzles(intruders, st.groups)
    if n < ODD_MIN_PUZZLES:
        out.append("%s: Odd One Out offers only %d different rounds, at least %d needed" % (key, n, ODD_MIN_PUZZLES))
    if sum(1 for ok in intruders if ok) < 2:
        out.append("%s: Odd One Out needs at least two groups that can hold an odd one out" % key)
    deck = fib_deck(st)
    texts = [_plain(t).lower() for t, _, _ in deck]
    if len(set(texts)) != len(texts):
        out.append("%s: Fact or Fib has the same statement twice" % key)
    fibs = sum(1 for _, ok, _ in deck if not ok)
    facts = len(deck) - fibs
    if fibs < FIB_MIN[0] or facts < FIB_MIN[1]:
        out.append("%s: Fact or Fib needs %d false and %d true statements, has %d and %d" % (key, FIB_MIN[0], FIB_MIN[1], fibs, facts))
    for t, ok, why in deck:
        if len(_plain(t)) > STATEMENT_MAX:
            out.append("%s: a Fact or Fib statement is longer than %d characters: %s" % (key, STATEMENT_MAX, t))
        if not ok and not why.strip():
            out.append("%s: a false Fact or Fib statement has no fix: %s" % (key, t))
    drop = set(FLASH_DROP.get(key, []))
    missing = drop - {_plain(p.a) for p in st.pairs}
    if missing:
        out.append("%s: FLASH_DROP names cards the lesson does not have: %s" % (key, ", ".join(sorted(missing))))
    pairs = flash_pairs(key, st)
    if len(pairs) < FLASH_MIN:
        out.append("%s: Memory Flash has only %d pairs to play, at least %d needed" % (key, len(pairs), FLASH_MIN))
    if tuple(st.pair_names) not in FLASH_ASK:
        out.append("%s: Memory Flash has no question for %s and %s cards: add one to FLASH_ASK" % (key, st.pair_names[0], st.pair_names[1]))
    for gi, g in enumerate(st.groups):
        for t in [g.name] + list(g.tiles):
            if DASH.search(t):
                out.append("%s: an Odd One Out tile or link has a dash: %s" % (key, t))
    return out


def check(records):
    """records: the stretch pages, as stretch_page.records() gives them.
    Returns a list of problems; also proves AVOID names only real lessons."""
    out = []
    keys = {r["key"] for r in records}
    for key in list(AVOID) + list(FLASH_DROP):
        if key not in keys:
            out.append("content/brain_games.py: a rule names a lesson that does not exist: %s" % key)
    for r in records:
        st = r["stretch"]
        if st.groups and st.bugs and st.pairs:
            out += problems(r["key"], st)
    return out
