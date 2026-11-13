"""Prove every stretch task before it is published.

A stretch task is played, not read, so a fault in one is a fault a student
meets with the clock running: a question with two right answers, a puzzle
that cannot be solved, a written answer the marker can never award. This
module stops the build on any of them.

Written answers are marked in the browser by the keyword marker in
static/js/quiz.js. `score()` below is the same marker in Python, kept line for
line in step with it (tools/check_stretch.mjs runs both on every answer and
fails if they ever disagree). Three things are proved for every written
question:

  The model answer earns full marks, so the mark points can be reached.
  Copying the question back as the answer earns nothing on a short answer and
  at most one mark on a long one, so no mark is given for repeating the
  question.
  A blank or "I don't know" answer earns nothing.

The two shorter tasks are checked too. Each This or That question has one
right and one different wrong answer that fit Pixel's speech bubble and the
buttons, and across a lesson the right answer is not usually the longer one,
so length never gives it away. Memory Match has six pairs whose cards fit a
phone, no two cards alike, and no word that appears in its own meaning.

Key Stage 3 lessons have three more games. Code Word has three words, each a
term the lesson itself uses, with a clue that never contains it. Link Up has
three groups of four tiles, no tile repeated and none that carries a word of
its own group's name. Bug Hunt has five rounds of two true statements and one
with a mistake; the mistake is not usually the longest or the shortest of the
three, so length never gives it away. `word_marks()` is Code Word's letter
marking in Python, kept in step with wordMarks in static/js/stretch.js.
"""
import html
import re

from mskbuild.models import Blitz, Written, Stretch

# ------------------------------------------------------------------ marker
# Mirrors SYNONYMS, normalise, stem, stemSet, containsPhrase and pointHit in
# static/js/quiz.js.
SYNONYMS = {
    "cpu": ["processor", "central processing unit"],
    "processor": ["cpu", "central processing unit"],
    "ram": ["main memory", "primary memory", "random access memory"],
    "rom": ["read only memory"],
    "hdd": ["hard disk", "hard disk drive", "magnetic hard drive"],
    "ssd": ["solid state drive", "solid state"],
    "os": ["operating system"],
    "gui": ["graphical user interface"],
    "url": ["web address"],
    "ip": ["internet protocol"],
    "lan": ["local area network"],
    "wan": ["wide area network"],
    "isp": ["internet service provider"],
    "alu": ["arithmetic logic unit"],
    "cu": ["control unit"],
    "mar": ["memory address register"],
    "mdr": ["memory data register"],
    "pc": ["program counter"],
    "dbms": ["database management system"],
    "sql": ["structured query language"],
    "ide": ["integrated development environment"],
    "nea": ["non exam assessment", "coursework"],
    "loop": ["iteration", "repeat", "repetition"],
    "iteration": ["loop", "repeat", "repetition"],
    "selection": ["if statement", "condition", "conditional"],
    "quicker": ["faster", "quick", "fast", "speed"],
    "faster": ["quicker", "quick", "fast", "speed"],
}


def normalise(s):
    s = str(s or "").lower()
    s = re.sub(r"[‘’“”]", "'", s)
    s = re.sub(r"[^a-z0-9'+\-<>=\s]", " ", s)
    s = re.sub(r"\s+", " ", s)
    return " " + s + " "


def stem(w):
    if len(w) > 5 and w.endswith("ies"):
        return w[:-3] + "y"
    if len(w) > 4 and (w.endswith("ing") or w.endswith("ed")):
        return re.sub(r"(ing|ed)$", "", w)
    if len(w) > 3 and w.endswith("es") and not (w.endswith("ss") or w.endswith("us")):
        return w[:-2]
    if len(w) > 3 and w.endswith("s") and not (w.endswith("ss") or w.endswith("us")):
        return w[:-1]
    if len(w) > 3 and w.endswith("e"):
        return w[:-1]
    return w


def stem_set(text):
    out = set()
    for w in normalise(text).strip().split(" "):
        if w:
            out.add(w)
            out.add(stem(w))
    return out


def contains_phrase(answer_norm, answer_stems, phrase, via_synonym=False):
    p = normalise(phrase).strip()
    if not p:
        return False
    if (" " + p + " ") in answer_norm:
        return True
    words = p.split(" ")
    if len(words) == 1:
        w = words[0]
        if w in answer_stems or stem(w) in answer_stems:
            return True
        if via_synonym:
            return False
        return any(contains_phrase(answer_norm, answer_stems, s, True) for s in SYNONYMS.get(w, []))
    return all(w in answer_stems or stem(w) in answer_stems for w in words)


def hits(text, points):
    """Which mark points an answer earns: a list of booleans, one per point."""
    if not str(text or "").strip():
        return [False] * len(points)
    a, s = normalise(text), stem_set(text)
    return [any(contains_phrase(a, s, ph) for ph in p.any) for p in points]


def score(text, q):
    return min(q.marks, sum(hits(text, q.points)))


# -------------------------------------------------------------- validation
KINDS = ("choice", "multi", "tf", "order", "type")
# Options that point at other options. The game shuffles every question's
# options, so "both of these" would end up pointing at nothing in particular.
_POINTING = re.compile(r"^\s*(both|neither)\b|\b(all|none)\s+of\s+(the\s+)?(above|these|them)\b", re.I)
_IDK = ("I don't know", "not sure", "yes")

Q_MAX = 240          # characters in a game question, so it fits above four tiles
OPTION_MAX = 90      # characters on a tile
PICK_Q_MAX = 200     # characters in Pixel's speech bubble
PICK_MAX = 80        # characters on a This or That answer
WHY_MAX = 260        # characters in Pixel's explanation
CARD_A_MAX = 32      # characters on a Memory Match word card
CARD_B_MAX = 64      # characters on a Memory Match meaning card, which a phone shows three across
PICKS = (8, 10)      # This or That questions in a lesson
PAIRS = 6            # Memory Match pairs: twelve cards, four by three or three by four
# The right answer may be the clearly longer one in at most this many of a
# lesson's This or That questions, so length never gives the answer away.
LONGER_RIGHT_MAX = 3
SORT_PROMPT_MAX = 160  # characters in the Sort It instruction
SORT_BINS = (2, 4)     # boxes in Sort It
SORT_BIN_MAX = 26      # characters on a box's label
SORT_ITEMS = (8, 12)   # cards in Sort It
SORT_CARD_MAX = 100    # characters on a Sort It card
WORDS = 3              # words in Code Word
WORD_LEN = (4, 9)      # letters in a Code Word word, so its tiles fit across a phone
CLUE_MAX = 110         # characters in a Code Word clue
GROUPS = 3             # hidden groups in Link Up
GROUP_TILES = 4        # tiles in each group
GROUP_NAME_MAX = 40    # characters in a group's name
TILE_MAX = 26          # characters on a Link Up tile
TILE_WORD_MAX = 13     # letters in one word on a tile, which cannot wrap
BUGS = 5               # rounds of Bug Hunt
BUG_TRUTHS = 2         # true statements beside each bug
BUG_MAX = 110          # characters in a Bug Hunt statement
FIX_MAX = 200          # characters in a Bug Hunt fix
BUG_EXTREME_MAX = 3    # rounds in which the bug may be the longest, or the shortest, statement
# No hyphen or dash of any kind appears in the three games' text.
_DASH = re.compile("[-\u2010-\u2015\u2212]")


class StretchError(Exception):
    pass


def _blitz_problems(where, b):
    out = []
    if b.kind not in KINDS:
        return ["%s: unknown kind %r" % (where, b.kind)]
    if not b.q.strip():
        out.append("%s: no question" % where)
    if len(b.q) > Q_MAX:
        out.append("%s: question is %d characters, the game shows at most %d" % (where, len(b.q), Q_MAX))
    if not b.explain.strip():
        out.append("%s: no explanation" % where)
    if b.time and not 5 <= b.time <= 120:
        out.append("%s: time %d is outside 5 to 120 seconds" % (where, b.time))
    opts = [o.strip() for o in b.options]
    if b.kind in ("choice", "multi", "order"):
        if any(not o for o in opts):
            out.append("%s: an empty option" % where)
        if len(set(o.lower() for o in opts)) != len(opts):
            out.append("%s: two options are the same" % where)
        for o in opts:
            if len(o) > OPTION_MAX:
                out.append("%s: option is %d characters, a tile shows at most %d: %s" % (where, len(o), OPTION_MAX, o))
            if _POINTING.search(o):
                out.append("%s: option points at other options, which shuffling breaks: %s" % (where, o))
    if b.kind == "choice" and not 3 <= len(opts) <= 4:
        out.append("%s: a choice question needs three or four options" % where)
    if b.kind == "multi" and not (2 <= b.n < len(opts) <= 6):
        out.append("%s: a multi question needs at least two right options and at least one wrong one" % where)
    if b.kind == "order" and not 3 <= len(opts) <= 6:
        out.append("%s: an order question needs three to six items" % where)
    if b.kind == "tf" and (opts or not isinstance(b.answer, bool)):
        out.append("%s: a true or false question has no options and a True or False answer" % where)
    if b.kind == "type":
        if not b.accept or any(not a.strip() for a in b.accept):
            out.append("%s: a typed answer needs at least one accepted answer" % where)
        if opts:
            out.append("%s: a typed answer has no options" % where)
    return out


def _written_problems(where, w, long_answer):
    out = []
    if w.marks < 1:
        out.append("%s: no marks" % where)
    if len(w.points) < w.marks:
        out.append("%s: %d marks but only %d mark points" % (where, w.marks, len(w.points)))
    for p in w.points:
        if not p.any or any(not ph.strip() for ph in p.any):
            out.append("%s: mark point with an empty phrasing: %s" % (where, p.text))
    if not w.model.strip():
        out.append("%s: no model answer" % where)
        return out
    got = score(w.model, w)
    if got < w.marks:
        missed = [p.text for p, h in zip(w.points, hits(w.model, w.points)) if not h]
        out.append("%s: the model answer earns %d of %d; it misses: %s" % (where, got, w.marks, "; ".join(missed)))
    echo = score(w.q, w)
    if echo > (1 if long_answer else 0):
        found = [p.text for p, h in zip(w.points, hits(w.q, w.points)) if h]
        out.append("%s: copying the question earns %d mark(s), from: %s" % (where, echo, "; ".join(found)))
    for idk in _IDK:
        if score(idk, w):
            out.append("%s: the answer %r earns a mark" % (where, idk))
    return out


def _plain(text):
    """What a card or answer shows: markup and backticks gone, entities decoded."""
    return html.unescape(re.sub(r"[`*_]", "", str(text or ""))).strip()


def _pick_problems(where, p):
    out = []
    if not p.q.strip():
        out.append("%s: no question" % where)
    if len(_plain(p.q)) > PICK_Q_MAX:
        out.append("%s: question is %d characters, Pixel's bubble holds %d" % (where, len(_plain(p.q)), PICK_Q_MAX))
    for name, ans in (("right", p.right), ("wrong", p.wrong)):
        if not ans.strip():
            out.append("%s: no %s answer" % (where, name))
        if len(_plain(ans)) > PICK_MAX:
            out.append("%s: %s answer is %d characters, at most %d: %s" % (where, name, len(_plain(ans)), PICK_MAX, ans))
        if _POINTING.search(_plain(ans)):
            out.append("%s: %s answer points at the other one, which swapping sides breaks: %s" % (where, name, ans))
    if _plain(p.right).lower() == _plain(p.wrong).lower():
        out.append("%s: the right and wrong answers are the same" % where)
    if not p.why.strip():
        out.append("%s: Pixel gives no reason" % where)
    if len(_plain(p.why)) > WHY_MAX:
        out.append("%s: the reason is %d characters, at most %d" % (where, len(_plain(p.why)), WHY_MAX))
    return out


def _pair_problems(where, pairs):
    out = []
    if len(pairs) != PAIRS:
        return ["%s: %d Memory Match pairs, expected %d" % (where, len(pairs), PAIRS)]
    for side, limit in (("a", CARD_A_MAX), ("b", CARD_B_MAX)):
        texts = [_plain(getattr(p, side)) for p in pairs]
        if any(not t for t in texts):
            out.append("%s: an empty Memory Match card" % where)
        if len(set(t.lower() for t in texts)) != len(texts):
            out.append("%s: two Memory Match cards say the same thing" % where)
        for t in texts:
            if len(t) > limit:
                out.append("%s: Memory Match card is %d characters, at most %d: %s" % (where, len(t), limit, t))
    for p in pairs:
        a, b = _plain(p.a).lower(), _plain(p.b).lower()
        # a word that appears in its own meaning gives the pair away
        if re.match(r"^[a-z][a-z ]*$", a) and re.search(r"\b%s\b" % re.escape(a), b):
            out.append("%s: the card %r gives itself away in its partner: %s" % (where, p.a, p.b))
    return out


def lesson_problems(where, st):
    """Everything wrong with one lesson's tasks, as a list of messages."""
    problems = []
    if not 10 <= len(st.blitz) <= 14:
        problems.append("%s: %d game questions, expected 10 to 14" % (where, len(st.blitz)))
    if not 3 <= len(st.short) <= 5:
        problems.append("%s: %d short answers, expected 3 to 5" % (where, len(st.short)))
    if not 2 <= len(st.long) <= 3:
        problems.append("%s: %d long answers, expected 2 or 3" % (where, len(st.long)))
    seen = set()
    for n, b in enumerate(st.blitz):
        problems += _blitz_problems("%s game question %d" % (where, n + 1), b)
        key = (b.q.strip().lower(), b.code.strip())
        if key in seen:
            problems.append("%s: game question %d repeats an earlier one" % (where, n + 1))
        seen.add(key)
    for n, w in enumerate(st.short):
        problems += _written_problems("%s short answer %d" % (where, n + 1), w, False)
    for n, w in enumerate(st.long):
        problems += _written_problems("%s long answer %d" % (where, n + 1), w, True)
        if w.marks < 3:
            problems.append("%s long answer %d: a long answer is worth at least 3 marks" % (where, n + 1))
    if not PICKS[0] <= len(st.picks) <= PICKS[1]:
        problems.append("%s: %d This or That questions, expected %d to %d" % (where, len(st.picks), PICKS[0], PICKS[1]))
    asked = {b.q.strip().lower() for b in st.blitz}
    seen = set()
    for n, p in enumerate(st.picks):
        problems += _pick_problems("%s This or That %d" % (where, n + 1), p)
        key = (p.q.strip().lower(), p.code.strip())
        if key in seen:
            problems.append("%s: This or That %d repeats an earlier one" % (where, n + 1))
        if p.q.strip().lower() in asked and not p.code:
            problems.append("%s: This or That %d is also a quiz game question" % (where, n + 1))
        seen.add(key)
    longer = sum(1 for p in st.picks if len(_plain(p.right)) > len(_plain(p.wrong)) + 15)
    if longer > LONGER_RIGHT_MAX:
        problems.append("%s: the right answer is the clearly longer one in %d This or That questions, at most %d"
                        % (where, longer, LONGER_RIGHT_MAX))
    problems += _pair_problems(where, st.pairs)
    if len(st.pair_names) != 2 or not all(n.strip() for n in st.pair_names):
        problems.append("%s: pair_names needs two labels" % where)
    if st.sort is not None:
        problems += _sort_problems(where, st.sort)
    return problems


def _sort_problems(where, sort):
    out = []
    where = "%s Sort It" % where
    if not sort.prompt.strip() or len(_plain(sort.prompt)) > SORT_PROMPT_MAX:
        out.append("%s: the prompt is empty or longer than %d characters" % (where, SORT_PROMPT_MAX))
    bins = [_plain(b) for b in sort.bins]
    if not SORT_BINS[0] <= len(bins) <= SORT_BINS[1]:
        out.append("%s: %d boxes, expected %d to %d" % (where, len(bins), SORT_BINS[0], SORT_BINS[1]))
    if len(set(b.lower() for b in bins)) != len(bins) or any(not b for b in bins):
        out.append("%s: two boxes have the same label, or one is empty" % where)
    for b in bins:
        if len(b) > SORT_BIN_MAX:
            out.append("%s: box label is %d characters, at most %d: %s" % (where, len(b), SORT_BIN_MAX, b))
    if not SORT_ITEMS[0] <= len(sort.items) <= SORT_ITEMS[1]:
        out.append("%s: %d cards, expected %d to %d" % (where, len(sort.items), SORT_ITEMS[0], SORT_ITEMS[1]))
    texts = [_plain(i.text) for i in sort.items]
    if len(set(t.lower() for t in texts)) != len(texts):
        out.append("%s: two cards say the same thing" % where)
    for i in sort.items:
        t = _plain(i.text)
        if not t or len(t) > SORT_CARD_MAX:
            out.append("%s: card is empty or longer than %d characters: %s" % (where, SORT_CARD_MAX, t))
        if not 0 <= i.bin < len(bins):
            out.append("%s: card points at box %d, which does not exist: %s" % (where, i.bin, t))
        if not i.why.strip() or len(_plain(i.why)) > WHY_MAX:
            out.append("%s: card has no reason, or one longer than %d characters: %s" % (where, WHY_MAX, t))
    for k, b in enumerate(bins):
        if sum(1 for i in sort.items if i.bin == k) < 2:
            out.append("%s: the box %r gets fewer than two cards" % (where, b))
    return out


def word_marks(guess, answer):
    """Code Word's marking of one guess, a mark for each letter: 2 for the
    right letter in the right place, 1 for a letter that is in the word but
    somewhere else, 0 for one that is not. A letter is only marked as many
    times as the word has it: guess LLAMA against ALLOW and the second L is
    in place, the first L is elsewhere, and only the first A is marked."""
    guess, answer = str(guess).upper(), str(answer).upper()
    marks = [0] * len(guess)
    spare = {}
    for i, a in enumerate(answer):
        if i < len(guess) and guess[i] == a:
            marks[i] = 2
        else:
            spare[a] = spare.get(a, 0) + 1
    for i, g in enumerate(guess):
        if marks[i] == 0 and spare.get(g, 0) > 0:
            marks[i] = 1
            spare[g] -= 1
    return marks


def _forms(word):
    """The spellings that count as a word being used: itself, its plural and its singular."""
    w = word.lower()
    out = {w, w + "s", w + "es"}
    if w.endswith("s"):
        out.add(w[:-1])
    return out


def _sentence_problems(where, what, text, limit):
    """A sentence a game shows: within its length, tidy, and ending in a full stop."""
    out = []
    t = _plain(text)
    if not t:
        return ["%s: %s is empty" % (where, what)]
    if len(t) > limit:
        out.append("%s: %s is %d characters, at most %d: %s" % (where, what, len(t), limit, t))
    if text != text.strip() or "  " in text:
        out.append("%s: %s has stray spaces: %r" % (where, what, text))
    if not t.endswith(".") or t.endswith(".."):
        out.append("%s: %s must end with one full stop: %s" % (where, what, t))
    if not (t[0].isupper() or t[0].isdigit()):
        out.append("%s: %s must start with a capital letter or a number: %s" % (where, what, t))
    if _DASH.search(text):
        out.append("%s: %s has a hyphen or dash in it: %s" % (where, what, t))
    return out


def _stemmed(word):
    w = word.lower()
    return w[:-1] if len(w) > 4 and w.endswith("s") else w


def _games_problems(where, st, lesson_words):
    """Code Word, Link Up and Bug Hunt for one lesson. `lesson_words` is every
    word the lesson and its other tasks use, or None to skip that check."""
    out = []
    if not (st.words and st.groups and st.bugs):
        return ["%s: Code Word, Link Up and Bug Hunt come together, and one of them is missing" % where]

    # ----- Code Word
    cw = "%s Code Word" % where
    if len(st.words) != WORDS:
        out.append("%s: %d words, expected %d" % (cw, len(st.words), WORDS))
    seen = set()
    for w in st.words:
        word = w.word
        if not re.match(r"^[A-Z]+$", word) or not WORD_LEN[0] <= len(word) <= WORD_LEN[1]:
            out.append("%s: %r must be %d to %d capital letters" % (cw, word, WORD_LEN[0], WORD_LEN[1]))
            continue
        if word in seen:
            out.append("%s: %s appears twice" % (cw, word))
        seen.add(word)
        out += _sentence_problems(cw, "the clue for %s" % word, w.clue, CLUE_MAX)
        if word.lower() in _plain(w.clue).lower():
            out.append("%s: the clue for %s contains the word itself: %s" % (cw, word, w.clue))
        if lesson_words is not None and not (_forms(word) & lesson_words):
            out.append("%s: %s is not a word this lesson or its other tasks use" % (cw, word))

    # ----- Link Up
    lu = "%s Link Up" % where
    if len(st.groups) != GROUPS:
        out.append("%s: %d groups, expected %d" % (lu, len(st.groups), GROUPS))
    names = [_plain(g.name) for g in st.groups]
    if len(set(n.lower() for n in names)) != len(names):
        out.append("%s: two groups have the same name" % lu)
    tiles = []
    for g in st.groups:
        name = _plain(g.name)
        if not name or len(name) > GROUP_NAME_MAX:
            out.append("%s: a group's name is empty or longer than %d characters: %s" % (lu, GROUP_NAME_MAX, name))
        if g.name != g.name.strip() or "  " in g.name or name.endswith(".") or _DASH.search(g.name):
            out.append("%s: a group's name has stray spaces, a full stop or a dash: %r" % (lu, g.name))
        if len(g.tiles) != GROUP_TILES:
            out.append("%s: the group %r has %d tiles, expected %d" % (lu, name, len(g.tiles), GROUP_TILES))
        name_words = {_stemmed(x) for x in re.findall(r"[A-Za-z]{4,}", name)}
        for t in g.tiles:
            tile = _plain(t)
            tiles.append(tile.lower())
            if not tile or len(tile) > TILE_MAX:
                out.append("%s: a tile is empty or longer than %d characters: %s" % (lu, TILE_MAX, tile))
            if t != t.strip() or "  " in t or tile.endswith(".") or _DASH.search(t):
                out.append("%s: a tile has stray spaces, a full stop or a dash: %r" % (lu, t))
            if any(len(x) > TILE_WORD_MAX for x in tile.split()):
                out.append("%s: a tile has a word longer than %d letters, which cannot wrap: %s" % (lu, TILE_WORD_MAX, tile))
            shared = name_words & {_stemmed(x) for x in re.findall(r"[A-Za-z]{4,}", tile)}
            if shared:
                out.append("%s: the tile %r gives away its group %r by sharing the word %s"
                           % (lu, tile, name, ", ".join(sorted(shared))))
    if len(set(tiles)) != len(tiles):
        dup = sorted(t for t in set(tiles) if tiles.count(t) > 1)
        out.append("%s: a tile appears twice: %s" % (lu, ", ".join(dup)))
    if set(tiles) & {n.lower() for n in names}:
        out.append("%s: a tile is the same as a group's name" % lu)

    # ----- Bug Hunt
    bh = "%s Bug Hunt" % where
    if len(st.bugs) != BUGS:
        out.append("%s: %d rounds, expected %d" % (bh, len(st.bugs), BUGS))
    said = []
    longest = shortest = 0
    asked = {_plain(b.q).lower() for b in st.blitz if b.kind == "tf"}
    for n, b in enumerate(st.bugs, 1):
        r = "%s round %d" % (bh, n)
        if len(b.truths) != BUG_TRUTHS:
            out.append("%s: %d true statements, expected %d" % (r, len(b.truths), BUG_TRUTHS))
        for t in b.truths:
            out += _sentence_problems(r, "a true statement", t, BUG_MAX)
        out += _sentence_problems(r, "the bug", b.bug, BUG_MAX)
        out += _sentence_problems(r, "the fix", b.fix, FIX_MAX)
        three = [_plain(t) for t in b.truths] + [_plain(b.bug)]
        for t in three:
            if _POINTING.search(t) or re.search(r"\b(above|below|other (two|statements?))\b", t, re.I):
                out.append("%s: a statement points at the others, which shuffling breaks: %s" % (r, t))
            if t.lower() in asked:
                out.append("%s: a statement is also a true or false question in the quiz: %s" % (r, t))
        said += [t.lower() for t in three]
        lengths = [len(t) for t in three]
        if lengths[-1] == max(lengths) and lengths.count(lengths[-1]) == 1:
            longest += 1
        if lengths[-1] == min(lengths) and lengths.count(lengths[-1]) == 1:
            shortest += 1
    if len(set(said)) != len(said):
        out.append("%s: a statement appears twice" % bh)
    if longest > BUG_EXTREME_MAX:
        out.append("%s: the bug is the longest statement in %d rounds, at most %d" % (bh, longest, BUG_EXTREME_MAX))
    if shortest > BUG_EXTREME_MAX:
        out.append("%s: the bug is the shortest statement in %d rounds, at most %d" % (bh, shortest, BUG_EXTREME_MAX))
    return out


def lesson_words(section, st):
    """Every word a Key Stage 3 lesson uses: its section of the topic page and
    the questions, answers and cards of its other stretch tasks."""
    parts = [section.title, section.body]
    for b in st.blitz:
        parts += [b.q, b.explain] + list(b.options) + list(b.accept)
    for w in st.short + st.long:
        parts += [w.q, w.model]
    for p in st.picks:
        parts += [p.q, p.right, p.wrong, p.why]
    for p in st.pairs:
        parts += [p.a, p.b]
    return set(re.findall(r"[a-z]+", " ".join(parts).lower()))


def topic_words(topic, st):
    """Every word a Key Stage 4 lesson uses: its whole topic page and the
    questions, answers and cards of its other stretch tasks."""
    parts = [topic.title, topic.blurb, topic.grade]
    for sec in topic.sections:
        parts += [sec.title, sec.body]
    for term, meaning in topic.keyterms:
        parts += [term, meaning]
    parts += list(topic.mistakes)
    for b in st.blitz:
        parts += [b.q, b.explain] + list(b.options) + list(b.accept)
    for w in st.short + st.long:
        parts += [w.q, w.model]
    for p in st.picks:
        parts += [p.q, p.right, p.wrong, p.why]
    for p in st.pairs:
        parts += [p.a, p.b]
    if st.sort:
        parts += [st.sort.prompt] + list(st.sort.bins) + [i.text for i in st.sort.items] + [i.why for i in st.sort.items]
    return set(re.findall(r"[a-z]+", " ".join(x or "" for x in parts).lower()))


def validate(units, topics):
    """Key Stage 3. units: [(topic slug, [Stretch])]; topics: {slug: Topic}. Raises StretchError."""
    problems = []
    for slug, lessons in units:
        topic = topics.get(slug)
        if topic is None:
            problems.append("%s: no such topic" % slug)
            continue
        titles = [s.title for s in topic.sections]
        for i, st in enumerate(lessons):
            where = "%s lesson %d (%s)" % (slug, i + 1, st.lesson)
            if st.lesson not in titles:
                problems.append("%s: no section of %s is called that" % (where, slug))
            problems += lesson_problems(where, st)
            if st.words or st.groups or st.bugs:
                used = lesson_words(topic.sections[titles.index(st.lesson)], st) if st.lesson in titles else None
                problems += _games_problems(where, st, used)
        order = [titles.index(s.lesson) for s in lessons if s.lesson in titles]
        if order != sorted(order):
            problems.append("%s: lessons are not in the order the topic teaches them" % slug)
    if problems:
        raise StretchError("Stretch tasks failed their checks:\n  " + "\n  ".join(problems))


def validate_ks4(lessons, topics):
    """Key Stage 4, where a lesson is a whole topic and Sort It is required.

    lessons: [(course slug, Stretch)]; topics: {(course slug, topic slug): Topic}."""
    problems = []
    seen = set()
    for course, st in lessons:
        where = "%s %s" % (course, st.lesson)
        if (course, st.lesson) in seen:
            problems.append("%s: this topic has two sets of stretch tasks" % where)
        seen.add((course, st.lesson))
        if (course, st.lesson) not in topics:
            problems.append("%s: no topic of %s has that slug" % (where, course))
        if st.sort is None:
            problems.append("%s: a Key Stage 4 lesson needs a Sort It task" % where)
        problems += lesson_problems(where, st)
        if st.words or st.groups or st.bugs:
            topic = topics.get((course, st.lesson))
            problems += _games_problems(where, st, topic_words(topic, st) if topic else None)
    if problems:
        raise StretchError("Stretch tasks failed their checks:\n  " + "\n  ".join(problems))
