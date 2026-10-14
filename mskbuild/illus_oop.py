"""Illustrations for object oriented programming and recursion: class and object, encapsulation,
inheritance, polymorphism, relationships between classes and the Towers of Hanoi."""
import math

from .illus import Canvas, PAL, INK, ARROW, figure, illustration, _n
from . import illus_props as P
from . import illus_glyphs as G

KIND = {"": ("#FFFFFF", INK), "inh": ("#E6EEF2", "#4A6470"), "over": ("#FFC6BB", INK), "new": ("#C9F3E0", INK)}


def uml(cv, x, y, w, name, attrs, methods, col="sky", size=12.5):
    """A UML class box. attrs and methods are (text, kind) pairs; kind colours a line as inherited, overridden or new."""
    lh = size * 1.7
    h_attr = max(1, len(attrs)) * lh + 10
    h_meth = max(1, len(methods)) * lh + 10
    total = 32 + h_attr + h_meth
    out = cv.rect(x, y + 3, w, total, 9, "#10303A", op=.14) + cv.rect(x, y, w, total, 9, "#FFFFFF", stroke="#8AA0AC", sw=1.8)
    out += cv.rect(x + .9, y + .9, w - 1.8, 32, 8, cv.g(col)) + cv.rect(x + .9, y + 16, w - 1.8, 17, 0, cv.g(col))
    out += cv.text(x + w / 2, y + 22, name, 14.5, 800, fill=INK, mono=True)
    cy = y + 32
    for block in (attrs, methods):
        out += cv.line(x, cy, x + w, cy, "#8AA0AC", 1.4)
        for i, (t, kind) in enumerate(block):
            bg, tc = KIND[kind]
            if kind:
                out += cv.rect(x + 5, cy + 4 + i * lh, w - 10, lh - 2, 4, bg)
            out += cv.text(x + 12, cy + 4 + i * lh + size * 1.05, t, size, 700, anchor="start", fill=tc, mono=True)
        cy += (max(1, len(block)) * lh + 10)
    return out, total


def triangle(cv, x, y, up=True, s=12):
    pts = [(x, y), (x - s, y + s * 1.5), (x + s, y + s * 1.5)] if up else [(x, y), (x - s, y - s * 1.5), (x + s, y - s * 1.5)]
    return cv.poly(pts, "#FFFFFF", stroke="#2A3E49", sw=2.2)


def diamond(cv, x, y, filled, horizontal=True, s=11):
    pts = [(x - s * 1.4, y), (x, y - s * .8), (x + s * 1.4, y), (x, y + s * .8)] if horizontal else [(x, y - s * 1.4), (x + s * .8, y), (x, y + s * 1.4), (x - s * .8, y)]
    return cv.poly(pts, "#2A3E49" if filled else "#FFFFFF", stroke="#2A3E49", sw=2)


# ------------------------------------------------------------------ class and object

@illustration("class-object")
def _class_object():
    cv = Canvas(800, 500).backdrop()
    cv.add(G.code(cv, 14, 30, 350, ["class Dog:", "    def __init__(self, name, breed):", "        self.name = name", "        self.breed = breed", "    def bark(self):", "        print(self.name, 'says woof!')"], title="dog.py", size=12, numbers=False))
    cv.add(G.code(cv, 14, 222, 350, ["rex = Dog('Rex', 'Labrador')", "bella = Dog('Bella', 'Collie')", "rex.bark()"], title="main.py", size=12, numbers=False))
    cv.add(cv.text(189, 366, "Output:  Rex says woof!", 13, 750, cls="il-ink", mono=True))
    # the blueprint
    cv.add(P.card(cv, 392, 30, 394, 130, 18, "class Dog: the blueprint", "teal"), P.badge(cv, 414, 54, 1))
    cv.add(cv.rect(412, 70, 354, 76, 10, "none", stroke="#0F7C84", sw=2.4, dash="7 5"))
    cv.add(cv.text(430, 96, "attributes:  name  breed", 14, 750, anchor="start", cls="il-ink", mono=True), cv.text(430, 124, "method:      bark()", 14, 750, anchor="start", cls="il-ink", mono=True))
    # the objects
    for k, (nm, br, col) in enumerate((("rex", "Labrador", "sky"), ("bella", "Collie", "mint"))):
        x = 392 + k * 200
        cv.add(P.arrow(cv, [(x + 100 if k == 0 else x + 96, 164), (x + 98, 214)], ARROW, 3, 9, dash="5 4"))
        cv.add(P.card(cv, x, 222, 194, 130, 16, "%s: Dog" % nm, col))
        if k == 0:
            cv.add(P.badge(cv, x + 16, 240, 2))
        cv.add(cv.text(x + 18, 270, "self.name", 12, 650, anchor="start", cls="il-ink2", mono=True), cv.text(x + 18, 290, '"%s"' % nm.capitalize(), 15, 800, anchor="start", cls="il-ink", mono=True))
        cv.add(cv.text(x + 18, 316, "self.breed", 12, 650, anchor="start", cls="il-ink2", mono=True), cv.text(x + 18, 336, '"%s"' % br, 15, 800, anchor="start", cls="il-ink", mono=True))
    cv.add(cv.text(589, 376, "the same methods, but each object keeps its own data", 13, 700, cls="il-ink"))
    # vocabulary
    for i, (t, sub, col) in enumerate((("class", "the blueprint", "teal"), ("object", "one thing built from it", "sky"), ("self", "this particular object", "sun"))):
        x = 14 + i * 262
        cv.add(P.lift(cv, x, 412, 250, 62, col, 12, 5, hl=False), cv.text(x + 125, 438, t, 17, 800, fill=INK, mono=True), cv.text(x + 125, 460, sub, 13, 650, fill=INK))
    cv.add(P.badge(cv, 30, 412, 3))
    return figure(
        "class-object", cv, "A Dog class as a blueprint, and two objects made from it with their own data",
        "A class is a blueprint and an object is a thing built from it. The class Dog has the attributes name and breed and the method bark. Two "
        "objects are created from it: rex, with the name Rex and the breed Labrador, and bella, with the name Bella and the breed Collie. They share "
        "the same methods but each object keeps its own data. Calling rex dot bark prints Rex says woof. In the code, self means this "
        "particular object, so self dot name is Rex when rex calls bark.",
        ["The class Dog is the blueprint: it says which attributes and methods every dog has.", "Each object made from it has its own attribute values. They share the methods.",
         "A class is a blueprint, an object is one thing built from it, and self means this particular object."],
        "One plan, many houses: each house has its own address, but they are all built to the same plan.")


# ------------------------------------------------------------------ encapsulation

@illustration("encapsulation")
def _encap():
    cv = Canvas(800, 500).backdrop()
    # the object
    cv.add(cv.shadow(400, 440, 150, 10, .2))
    cv.add(cv.rect(290, 60, 240, 372, 30, cv.g("sky", "deep")), cv.rect(298, 68, 224, 356, 24, "var(--il-bg1)"))
    cv.add(cv.text(410, 98, "BankAccount", 17, 800, cls="il-ink", mono=True))
    cv.add(P.lift(cv, 330, 164, 160, 96, "dark", 14, 6, hl=False), cv.text(410, 192, "private", 12.5, 700, fill="#FFFFFF", mono=True), cv.text(410, 222, "__balance", 17, 800, fill="#FFFFFF", mono=True), cv.text(410, 246, "= 120", 15, 800, fill="#FFDA8A", mono=True))
    cv.add(P.padlock(cv, 397, 130, .5, "sun"))
    for i, t in enumerate(("deposit(amount)", "withdraw(amount)", "get_balance()")):
        y = 296 + i * 42
        cv.add(P.lift(cv, 322, y, 176, 32, "mint", 9, 4, hl=False), cv.text(410, y + 21, t, 13, 800, fill=INK, mono=True))
    # the outside
    cv.add(P.card(cv, 14, 130, 230, 232, 18, "Other code", "coral"))
    cv.add(G.code(cv, 28, 168, 202, ["acc.__balance = -1000"], title=None, size=11.5, numbers=False))
    cv.add(P.arrow(cv, [(236, 190), (326, 212)], "#BA352D", 4.5, 12), P.cross(cv, 300, 204, 14))
    cv.add(cv.text(129, 250, "cannot reach the data", 13, 750, cls="il-bad"))
    cv.add(G.code(cv, 28, 276, 202, ["acc.withdraw(50)"], title=None, size=11.5, numbers=False))
    cv.add(P.arrow(cv, [(236, 296), (318, 312)], "#248049", 4.5, 12), P.tick(cv, 288, 306, 13))
    cv.add(cv.text(129, 354, "asks the object", 13, 750, cls="il-ok"))
    # the reasons
    cv.add(P.card(cv, 556, 30, 230, 402, 18, "Why it helps", "teal"))
    for i, (a_, b_) in enumerate((("The data is private", "only the object's own methods change it"), ("Methods can check", "withdraw refuses if there is not enough money"), ("It stays valid", "the balance can never be set to nonsense"), ("Easy to change", "the inside can change without breaking other code"))):
        y = 82 + i * 86
        cv.add(P.tick(cv, 582, y + 6, 10), cv.text(604, y + 4, a_, 14.5, 800, anchor="start", cls="il-ink"))
        for j, ln in enumerate(_wrap(b_, 22)):
            cv.add(cv.text(604, y + 24 + j * 16, ln, 12.5, 650, anchor="start", cls="il-ink2"))
    cv.add(P.badge(cv, 310, 84, 1), P.badge(cv, 36, 152, 2), P.badge(cv, 578, 54, 3))
    return figure(
        "encapsulation", cv, "Encapsulation: a BankAccount keeps its balance private and offers methods to use it",
        "Encapsulation means an object controls its own data. A BankAccount object holds a private balance, here 120, inside a vault. Around "
        "the outside are three methods you can use: deposit, withdraw and get balance. Other code that tries to set the balance directly, "
        "acc dot underscore underscore balance equals minus 1000, is blocked. Other code that calls acc dot withdraw 50 gets through, because "
        "it asks the object to do it. The benefits are that only the object's own methods change the data, the methods can check, for "
        "example refusing to withdraw more than there is, so the object always stays valid, and the inside can change without breaking other code.",
        ["The data is private, inside the object.", "Other code cannot change it directly, but it can ask through a method.",
         "That keeps the object valid, and lets the inside change without breaking anything that uses it."],
        "Make attributes private, and give the outside world methods that check before they change anything.")


def _wrap(text, n):
    out, cur = [], ""
    for w in text.split():
        if len(cur) + len(w) + 1 > n and cur:
            out.append(cur)
            cur = w
        else:
            cur = (cur + " " + w).strip()
    out.append(cur)
    return out


# ------------------------------------------------------------------ inheritance

@illustration("inheritance-tree")
def _inherit():
    cv = Canvas(800, 500).backdrop()
    top, w1 = uml(cv, 250, 30, 300, "Animal", [("name", ""), ("age", "")], [("speak()", ""), ("describe()", "")], "sun")
    cv.add(top)
    dog, hd = uml(cv, 40, 270, 290, "Dog", [("name", "inh"), ("age", "inh")], [("describe()", "inh"), ("speak()  -> 'Woof'", "over")], "sky")
    cat, hc = uml(cv, 470, 270, 290, "Cat", [("name", "inh"), ("age", "inh"), ("indoor", "new")], [("speak()  -> 'Meow'", "over"), ("describe()  + super()", "over")], "mint")
    cv.add(dog, cat)
    cv.add(cv.path("M185 270 L185 246 L615 246", stroke="#2A3E49", sw=2.4), cv.path("M615 246 L615 270", stroke="#2A3E49", sw=2.4), cv.line(400, 246, 400, 30 + w1 + 14, "#2A3E49", 2.4))
    cv.add(triangle(cv, 400, 30 + w1 + 14 - 1, True, 11))
    cv.add(cv.text(412, 232, "inherits from", 13, 750, anchor="start", cls="il-ink"))
    # the key
    for i, (kind, t) in enumerate((("inh", "inherited: used as it is"), ("over", "overridden: its own version"), ("new", "new: only in this subclass"))):
        x = 40 + i * 252
        bg, tc = KIND[kind]
        cv.add(cv.rect(x, 440, 230, 30, 8, bg, stroke="#9FB3BE", sw=1.2), cv.text(x + 115, 460, t, 13, 750, fill=tc))
    cv.add(P.badge(cv, 266, 40, 1), P.badge(cv, 56, 284, 2), P.badge(cv, 486, 284, 3), P.badge(cv, 22, 440, 4))
    return figure(
        "inheritance-tree", cv, "Dog and Cat inheriting from Animal, showing what is inherited, overridden and new",
        "A UML diagram of inheritance. The parent class Animal has the attributes name and age and the methods speak and describe. Two child "
        "classes, Dog and Cat, inherit from it, shown by lines ending in a hollow triangle pointing at Animal. Dog inherits name, age and "
        "describe unchanged, and overrides speak to return Woof. Cat inherits name and age, adds a new attribute, indoor, overrides speak to "
        "return Meow, and overrides describe while still calling the parent's version with super. A key says grey lines are inherited, "
        "coral lines are overridden and green lines are new in the subclass.",
        ["The parent class holds what all animals share.", "Dog inherits everything and overrides speak.", "Cat adds an attribute of its own and overrides speak and describe.",
         "Inherited lines are used as they are, overridden lines replace the parent's version, and new lines exist only in the subclass."],
        "Inheritance removes duplication: put shared behaviour in the parent, and only what differs in the children.")


# ------------------------------------------------------------------ polymorphism

@illustration("polymorphism")
def _poly():
    cv = Canvas(800, 500).backdrop()
    cv.add(G.code(cv, 14, 34, 372, ["class Shape(ABC):", "    @abstractmethod", "    def area(self): ...", "", "for shape in [Circle(3), Square(4)]:", "    print(shape.describe())"], title="shapes.py", size=12, numbers=False))
    cv.add(P.badge(cv, 34, 28, 1))
    cv.add(P.card(cv, 404, 34, 382, 186, 18, "One call, many forms", "teal"), P.badge(cv, 426, 58, 2))
    cv.add(cv.text(595, 98, "shape.area()", 18, 800, cls="il-ink", mono=True))
    cv.add(P.arrow(cv, [(560, 110), (500, 150)], ARROW, 3, 9), P.arrow(cv, [(630, 110), (690, 150)], ARROW, 3, 9))
    cv.add(cv.text(489, 180, "Circle's own", 12.5, 700, cls="il-ink2"), cv.text(489, 197, "area()", 12.5, 700, cls="il-ink2", mono=True))
    cv.add(cv.text(701, 180, "Square's own", 12.5, 700, cls="il-ink2"), cv.text(701, 197, "area()", 12.5, 700, cls="il-ink2", mono=True))
    # the two shapes
    cv.add(P.card(cv, 14, 238, 372, 244, 18, "Circle(3)", "sky"), P.card(cv, 414, 238, 372, 244, 18, "Square(4)", "mint"))
    cv.add(cv.circle(120, 350, 52, cv.g("sky", "deep")), cv.line(120, 350, 172, 350, "#FFFFFF", 3), cv.rect(126, 322, 44, 20, 6, "#FFFFFF"), cv.text(148, 337, "r = 3", 13, 800, fill=INK, mono=True))
    cv.add(cv.rect(474, 300, 100, 100, 6, cv.g("mint", "deep")))
    cv.add(cv.text(524, 424, "side = 4", 13, 800, cls="il-ink", mono=True))
    cv.add(cv.text(290, 330, "3.14159 x r x r", 14, 700, cls="il-ink", mono=True), cv.text(290, 372, "= 28.27", 22, 800, cls="il-ink", mono=True))
    cv.add(cv.text(664, 330, "side x side", 14, 700, cls="il-ink", mono=True), cv.text(664, 372, "= 16.00", 22, 800, cls="il-ink", mono=True))
    cv.add(P.badge(cv, 36, 262, 3), P.badge(cv, 436, 262, 4))
    return figure(
        "polymorphism", cv, "Polymorphism: one call to area works on a circle and a square, each using its own method",
        "Polymorphism means one interface with many forms. The code loops over a list holding a Circle and a Square, and calls the same "
        "method on each one. The abstract class Shape guarantees that every subclass provides an area method. Calling shape dot area on the "
        "Circle with radius 3 uses the Circle's own version, 3.14159 times r times r, which gives 28.27. Calling it on the Square with side 4 "
        "uses the Square's own version, side times side, which gives 16.00. The loop does not need to know which kind of shape it has.",
        ["The abstract class says every shape has an area method, and the loop calls it on each shape.", "One call, shape.area(), is made, and each object answers with its own version.",
         "A Circle works out its area with its own method.", "A Square uses its own method. The loop never checks the type, so new shapes can be added without changing it."],
        "Polymorphism lets code work with many types through one interface, so new types need no changes to existing code.")


# ------------------------------------------------------------------ relationships between classes

@illustration("oop-relationships")
def _relations():
    cv = Canvas(800, 500).backdrop()
    spec = [("Inheritance: is a", "sun", "Dog is an Animal"), ("Composition: owns", "coral", "a Car has an Engine, and it goes when the car goes"),
            ("Aggregation: has", "sky", "a Team has Players, who exist without it"), ("Association: uses", "mint", "a Teacher knows about a Class")]
    for n, (title, col, rule) in enumerate(spec):
        x, y = (14, 406)[n % 2], (30, 258)[n // 2]
        cv.add(P.card(cv, x, y, 380, 214, 20, title, col), P.badge(cv, x + 22, y + 24, n + 1))
        names = (("Animal", "Dog"), ("Car", "Engine"), ("Team", "Player"), ("Teacher", "Class"))[n]
        bx1, bx2 = x + 28, x + 232
        if n == 0:
            cv.add(cv.rect(x + 140, y + 54, 100, 40, 8, "#FFFFFF", stroke="#8AA0AC", sw=1.8), cv.text(x + 190, y + 80, names[0], 14, 800, fill=INK, mono=True))
            cv.add(cv.rect(x + 140, y + 130, 100, 40, 8, "#FFFFFF", stroke="#8AA0AC", sw=1.8), cv.text(x + 190, y + 156, names[1], 14, 800, fill=INK, mono=True))
            cv.add(cv.line(x + 190, y + 130, x + 190, y + 112, "#2A3E49", 2.4), triangle(cv, x + 190, y + 94, True, 9))
        else:
            for bx, nm in ((bx1, names[0]), (bx2, names[1])):
                cv.add(cv.rect(bx, y + 74, 120, 44, 8, "#FFFFFF", stroke="#8AA0AC", sw=1.8), cv.text(bx + 60, y + 102, nm, 14, 800, fill=INK, mono=True))
            cv.add(cv.line(bx1 + 120, y + 96, bx2, y + 96, "#2A3E49", 2.4))
            if n == 1:
                cv.add(diamond(cv, bx1 + 134, y + 96, True))
            elif n == 2:
                cv.add(diamond(cv, bx1 + 134, y + 96, False))
            else:
                cv.add(P.arrow(cv, [(bx2 - 30, y + 96), (bx2, y + 96)], "#2A3E49", 2.4, 9))
            cv.add(cv.text(bx1 + 124, y + 82, "1", 12.5, 800, cls="il-ink", mono=True), cv.text(bx2 - 8, y + 82, "1" if n == 1 else "*", 12.5, 800, anchor="end", cls="il-ink", mono=True))
        for j, ln in enumerate(_wrap(rule, 40)):
            cv.add(cv.text(x + 190, y + 192 + (j - (len(_wrap(rule, 40)) - 1)) * 17 + 4, ln, 13, 700, cls="il-ink"))
    return figure(
        "oop-relationships", cv, "Four relationships between classes: inheritance, composition, aggregation and association",
        "Four ways classes relate, drawn as UML. Inheritance means is a: Dog is an Animal, drawn with a hollow triangle pointing at the parent. "
        "Composition means owns: a Car has an Engine and the engine goes when the car goes, drawn with a filled diamond on the owner. "
        "Aggregation means has: a Team has Players, who exist without the team, drawn with a hollow diamond. Association means uses: a Teacher "
        "knows about a Class, drawn as a plain line or arrow.",
        ["Inheritance: a subclass is a kind of its parent.", "Composition: the whole owns its parts. If the whole goes, the parts go too.",
         "Aggregation: the whole has parts that can exist on their own.", "Association: one class knows about, or uses, another."],
        "Ask two questions: is it a kind of that thing (inheritance), or does it have one (composition, aggregation)? If it has one, would the part survive without it?")


# ------------------------------------------------------------------ the Towers of Hanoi

def pegs(cv, x, y, state, w=170):
    """Three pegs with discs. state is three lists of disc sizes, biggest first."""
    out = cv.rect(x, y + 112, w, 9, 4.5, cv.g("wood", "deep"))
    cols = {1: "coral", 2: "sun", 3: "sky"}
    for p in range(3):
        px = x + w / 6 + p * w / 3
        out += cv.rect(px - 2.5, y + 14, 5, 98, 2.5, "#8AA0AC")
        for k, d in enumerate(state[p]):
            dw = 18 + d * 12
            out += P.lift(cv, px - dw / 2, y + 92 - k * 20, dw, 17, cols[d], 6, 3, hl=False)
    return out


@illustration("hanoi")
def _hanoi():
    cv = Canvas(800, 500).backdrop()
    steps = [([[3, 2, 1], [], []], "Start", "all three discs on peg A"), ([[3], [2, 1], []], "Step 1", "top 2 discs to peg B"),
             ([[], [2, 1], [3]], "Step 2", "biggest disc to peg C"), ([[], [], [3, 2, 1]], "Step 3", "2 discs back on top")]
    for i, (state, head, sub) in enumerate(steps):
        x = 14 + i * 196
        cv.add(P.card(cv, x, 30, 186, 236, 18), P.badge(cv, x + 18, 52, i + 1))
        cv.add(cv.text(x + 100, 58, head, 14, 800, cls="il-ink"))
        cv.add(pegs(cv, x + 8, 70, state))
        for p_, lab in enumerate("ABC"):
            cv.add(cv.text(x + 8 + 170 / 6 + p_ * 170 / 3, 208, lab, 12.5, 800, cls="il-ink2", mono=True))
        cv.add(cv.text(x + 93, 238, sub, 12.5, 700, cls="il-ink"))
        if i < 3:
            cv.add(P.arrow(cv, [(x + 187, 150), (x + 195, 150)], PAL["teal"][2], 3, 7))
    cv.add(P.card(cv, 14, 286, 506, 196, 18, "The recursive idea", "teal"))
    rows = [("Move the top n - 1 discs to the spare peg.", "a smaller version of the same problem"), ("Move the biggest disc to the target peg.", "one move"),
            ("Move the n - 1 discs on top of it.", "the same method again")]
    for i, (a_, b_) in enumerate(rows):
        y = 322 + i * 44
        cv.add(cv.circle(44, y + 4, 12, cv.g("deep", "deep")), cv.text(44, y + 9, str(i + 1), 14, 800, fill="#FFFFFF"))
        cv.add(cv.text(66, y, a_, 14.5, 750, anchor="start", cls="il-ink"), cv.text(66, y + 18, b_, 12.5, 650, anchor="start", cls="il-ink2"))
    cv.add(P.pill(cv, 267, 456, "Base case: with 1 disc, just move it. That stops the recursion.", "sun", 13, 14, 26, 750))
    cv.add(P.card(cv, 536, 286, 250, 196, 18, "Moves for n discs", "coral"))
    moves = [1, 3, 7, 15, 31, 63]
    for i, m in enumerate(moves):
        bx = 556 + i * 36
        h = 10 + m * 1.1
        cv.add(cv.rect(bx, 452 - h, 26, h, 5, cv.g("coral", "deep")))
        cv.add(cv.text(bx + 13, 448 - h, str(m), 11.5, 800, cls="il-ink", mono=True), cv.text(bx + 13, 468, str(i + 1), 12, 700, cls="il-ink2", mono=True))
    cv.add(cv.text(661, 326, "moves = 2^n - 1", 15, 800, cls="il-ink", mono=True))
    cv.add(cv.text(661, 344, "each extra disc doubles the work", 12, 650, cls="il-ink2"))
    return figure(
        "hanoi", cv, "Solving the Towers of Hanoi with three discs by recursion, and how the number of moves grows",
        "The Towers of Hanoi puzzle with three pegs, A, B and C, and three discs, solved by recursion. At the start all three discs are on peg A. "
        "Step one moves the top two discs to peg B, which is a smaller version of the same problem. Step two moves the biggest disc to peg C. Step "
        "three moves the two discs from B onto it. To move n discs you move n minus 1 discs out of the way, move the biggest disc, then move "
        "the n minus 1 discs back on top, and the base case is that one disc is simply moved. The number of moves is 2 to the power n minus 1: 1, "
        "3, 7, 15, 31 and 63 moves for 1 to 6 discs, so each extra disc doubles the work.",
        ["Start: all the discs are on the first peg.", "Move the top n - 1 discs to the spare peg. That is the same problem, but smaller.",
         "Move the biggest disc to the target peg.", "Move the n - 1 discs on top of it, using the same method again."],
        "A recursive solution needs a base case that stops it, and a step that makes the problem smaller.")
