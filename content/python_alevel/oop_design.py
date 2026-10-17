"""A Level Python: object oriented design beyond the first classes."""
from mskbuild.models import Topic, Section, Q, EQ, MP

INPUTS = {}
EXPECT = {}

TOPIC = Topic(
    slug="oop-design",
    title="Object-Oriented Design",
    spec="A Level 3",
    icon="i-cube",
    minutes=50,
    blurb="Class and instance attributes, access levels, abstract classes and overriding, then the A Level design questions: composition against inheritance, association and aggregation, and reading and drawing UML class diagrams.",
    fact="Alan Kay, who coined the term object-oriented in the 1960s, later said he had in mind something closer to cells that send each other messages than to the class hierarchies most people now call OOP. The big idea, he said, was messaging.",
    sections=[
        Section("Class members and access levels", r"""
You have already built classes with a constructor, methods and properties. The A Level specification asks for the vocabulary and the precision on top of that.

### Instance and class attributes

An **instance attribute** belongs to one object, and every object has its own copy. A **class attribute** belongs to the class itself and is **shared** by all its objects.

```python
class Student:
    school = "MskProd Academy"         # class attribute: one copy, shared
    count = 0

    def __init__(self, name):
        self.name = name               # instance attribute: one per object
        Student.count += 1

    @classmethod
    def from_text(cls, text):          # an alternative way to construct an object
        name, year = text.split(",")
        student = cls(name)
        student.year = int(year)
        return student

    @staticmethod
    def valid_year(year):              # belongs with the class but needs no object
        return 7 <= year <= 13

a = Student("Asha")
b = Student.from_text("Ben,11")
print(Student.count, a.school, b.year, Student.valid_year(14))
```

| Kind of method | First parameter | Can use |
| Instance method | `self`, the object | the object's attributes and the class's |
| Class method, `@classmethod` | `cls`, the class | class attributes, and can build new objects |
| Static method, `@staticmethod` | none | nothing of the object or class: a plain function filed with the class |

### Access levels

Some languages enforce who can see an attribute. Python trusts the programmer and relies on **naming conventions**:

| Level | Python | Meaning |
| Public | `name` | Part of the class's interface. Use it freely |
| Protected | `_name` | For the class and its subclasses. Please leave it alone |
| Private | `__name` | Python renames it to `_Class__name` to avoid accidents |

```python
class Account:
    def __init__(self, owner):
        self.owner = owner
        self._balance = 0
        self.__pin = "4821"

acct = Account("Asha")
print(acct.owner, acct._balance)
print(hasattr(acct, "__pin"), hasattr(acct, "_Account__pin"))     # False True
```

The private attribute is not hidden, only renamed. It stops accidental access, not a determined programmer, and that is why exam answers should say the **intent** of encapsulation, not claim Python makes the data unreachable.

### Making objects behave like built in types

Special methods let your own class work with `len`, `for` loops, indexing and sorting.

```python
class Playlist:
    def __init__(self, name):
        self.name = name
        self._songs = []

    def add(self, song):
        self._songs.append(song)

    def __len__(self):
        return len(self._songs)

    def __iter__(self):
        return iter(self._songs)

    def __getitem__(self, index):
        return self._songs[index]

    def __repr__(self):
        return "Playlist(" + repr(self.name) + ", " + str(len(self)) + " songs)"

p = Playlist("Revision")
p.add("Lofi 1")
p.add("Lofi 2")
print(len(p), p[0], list(p))
print(p)

class Card:
    def __init__(self, rank):
        self.rank = rank
    def __lt__(self, other):
        return self.rank < other.rank
    def __repr__(self):
        return "Card(" + str(self.rank) + ")"

print(sorted([Card(9), Card(2), Card(5)]))
```

`__lt__` is all `sorted` needs to put your own objects in order. That is **polymorphism** at its most practical: `sorted` does not know what a `Card` is, and does not need to.
"""),
        Section("Inheritance, overriding and abstract classes", r"""
**Inheritance** lets a class take on the attributes and methods of another. The new class is the **subclass** (or child, or derived class) and the one it inherits from is the **superclass** (parent, or base class). It models an **is-a** relationship: a `Circle` *is a* `Shape`.

A subclass can **override** a method, supplying its own version, and it can call the original with `super()`.

```python
class Employee:
    def __init__(self, name, base):
        self.name = name
        self.base = base

    def pay(self):
        return self.base

class Manager(Employee):
    def __init__(self, name, base, bonus):
        super().__init__(name, base)       # let the superclass set up its part
        self.bonus = bonus

    def pay(self):                         # overrides Employee.pay
        return super().pay() + self.bonus

staff = [Employee("Asha", 2000), Manager("Ben", 3000, 500)]
for person in staff:
    print(person.name, person.pay())
```

The loop calls `pay()` on each object and each gives its own answer. The caller does not check which kind of employee it has. That is **polymorphism**: the same message, different behaviour, decided by the class of the object.

### Abstract classes

Sometimes a superclass exists only to say what every subclass **must** be able to do. An **abstract class** has at least one **abstract method**, with no body, which every concrete subclass has to supply. You cannot create an object from the abstract class itself.

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    def __init__(self, name):
        self.name = name

    @abstractmethod
    def area(self):
        pass

    def describe(self):
        return self.name + " with area " + str(round(self.area(), 2))

class Rectangle(Shape):
    def __init__(self, w, h):
        super().__init__("Rectangle")
        self.w = w
        self.h = h

    def area(self):
        return self.w * self.h

class Circle(Shape):
    def __init__(self, r):
        super().__init__("Circle")
        self.r = r

    def area(self):
        return 3.14159 * self.r ** 2

for shape in [Rectangle(3, 4), Circle(2)]:
    print(shape.describe())
```

`describe` is written once, in `Shape`, and calls `self.area()`. It works for any shape, including ones that do not exist yet. Trying to build the abstract class itself fails:

```python
# raises: TypeError
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

shape = Shape()
```

!key An abstract class is a contract :: It does not say how each shape calculates its area, only that every shape must. Code that is written against `Shape` never needs to change when a `Triangle` is added.
"""),
        Section("Composition, aggregation and association", r"""
Inheritance is the relationship people reach for first and the one they most often misuse. There are three others, and all of them are **has-a** or **uses-a** relationships rather than is-a.

| Relationship | Meaning | Test | Example |
| **Association** | One object uses another | Can the two exist with no lasting link? | A `Teacher` marks a `Student`'s work |
| **Aggregation** | The whole *has* parts that can exist without it | If the whole is deleted, do the parts live on? | A `Team` has `Player`s |
| **Composition** | The whole *owns* parts that cannot exist without it | If the whole is deleted, do the parts go too? | A `Car` has an `Engine` |

```python
class Engine:
    def __init__(self, horsepower):
        self.horsepower = horsepower

class Car:
    def __init__(self, horsepower):
        self.engine = Engine(horsepower)      # composition: the car creates and owns it

class Team:
    def __init__(self, players):
        self.players = players                # aggregation: they were created elsewhere

class Teacher:
    def mark(self, student):                  # association: uses the student for a moment
        return student + " marked"

car = Car(150)
players = ["Asha", "Ben"]
team = Team(players)
del team
print(car.engine.horsepower, players)         # the players outlive the team
print(Teacher().mark("Asha"))
```

### Favour composition over inheritance

Inheritance locks the relationship in at the moment the class is written. Here is the standard trap:

```python
class Bird:
    def fly(self):
        return "flap flap"

class Penguin(Bird):
    pass

print(Penguin().fly())     # flap flap, but penguins cannot fly
```

A `Penguin` *is a* `Bird`, so it inherits `fly`. The model has gone wrong, and every new kind of bird that cannot fly makes it worse. **Composition** fixes it by treating the behaviour as a part, which the bird *has*:

```python
class Flies:
    def move(self):
        return "flaps"

class Walks:
    def move(self):
        return "waddles"

class Bird:
    def __init__(self, name, movement):
        self.name = name
        self.movement = movement          # has-a: how it moves is a part

    def move(self):
        return self.name + " " + self.movement.move()

for bird in [Bird("Sparrow", Flies()), Bird("Penguin", Walks())]:
    print(bird.move())
```

A new way of moving, swimming perhaps, is one new small class, and no existing class changes. The bird's behaviour could even be swapped while the program runs.

### Design principles to quote

| Principle | In practice |
| Encapsulate what varies | Put the part that changes, such as how a bird moves, in its own class |
| Program to an interface | Write code against the abstract class, not against one concrete subclass |
| Favour composition over inheritance | Use is-a only where it is really true for the whole life of the object |
| Single responsibility | A class should have one reason to change |
"""),
        Section("UML class diagrams", r"""
The **Unified Modelling Language** draws a design before any code is written. A class is a box with three compartments: the **name**, the **attributes** and the **methods**. A symbol in front of each says who can use it.

!diagram py-uml-class

| Symbol | Means |
| `+` | public |
| `-` | private |
| `#` | protected |

The lines between classes carry the meaning:

| Line | Relationship |
| Solid line with a hollow triangle at the parent end | Inheritance: is-a |
| Solid line with a filled diamond at the whole | Composition: owns, and the parts die with it |
| Solid line with a hollow diamond at the whole | Aggregation: has, and the parts live on |
| Plain solid line, often with an arrow | Association: uses |

Translating the diagram into code is mechanical. Each box is a class, each `-` attribute becomes `self.__name` or `self._name`, each arrow of inheritance becomes a class that names its parent in brackets, and each diamond becomes an attribute that holds another object.

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    def __init__(self, name):
        self._name = name                  # protected: subclasses use it

    @abstractmethod
    def area(self):                        # + area(): float
        pass

    def get_name(self):
        return self._name

class Circle(Shape):
    def __init__(self, radius):
        super().__init__("Circle")
        self.__radius = radius             # private: only Circle touches it

    def area(self):
        return round(3.14159 * self.__radius ** 2, 2)

c = Circle(2)
print(c.get_name(), c.area())              # Circle 12.57
```

!exam Read the arrow before the box :: Questions give a UML diagram and ask for code, or give code and ask for the diagram. Mark each line as inheritance, composition, aggregation or association before you write anything, then write the classes. Most lost marks are an arrow pointing the wrong way or a private attribute written as public.
"""),
    ],
    keyterms=[
        ("Class attribute", "An attribute that belongs to the class itself and is shared by every object of that class."),
        ("Instance attribute", "An attribute that belongs to one object, so each object has its own copy."),
        ("Encapsulation", "Bundling data with the methods that act on it, and restricting direct access to the data from outside the class."),
        ("Inheritance", "A mechanism by which a subclass acquires the attributes and methods of a superclass."),
        ("Overriding", "Providing a new version of an inherited method in a subclass."),
        ("Polymorphism", "The ability for the same method call to behave differently depending on the class of the object it is called on."),
        ("Abstract class", "A class that cannot be instantiated, which declares methods that its subclasses must implement."),
        ("Composition", "A relationship in which one object is made of other objects that it owns, and which cannot exist without it."),
        ("Aggregation", "A relationship in which one object holds other objects that can exist independently of it."),
        ("Association", "A relationship in which one object uses another."),
        ("UML class diagram", "A diagram that shows classes, their attributes and methods, and the relationships between them."),
    ],
    grade="""
Object oriented answers reward exact vocabulary tied to the code in front of you.

+ Define encapsulation, inheritance and polymorphism separately, then show each in the given code
+ Say whether a relationship is is-a, or has-a, and name it: inheritance, composition or aggregation
+ Use the correct UML symbols for public, private and protected, and draw the arrow for inheritance towards the parent
+ In a design question, justify a choice: composition because behaviour might change, inheritance because it is truly is-a
+ Write super().__init__ in a subclass constructor, and mark abstract methods as abstract
""",
    mistakes=[
        "Using inheritance for a has-a relationship, such as making Car a subclass of Engine.",
        "Saying a private attribute in Python cannot be accessed at all, when it is only renamed.",
        "Drawing the inheritance arrow towards the subclass instead of the superclass.",
        "Forgetting to call super().__init__ in the subclass, so the inherited attributes are never set.",
        "Mixing up class attributes, shared by all, and instance attributes, one per object.",
    ],
    quiz=[
        Q("What is the difference between a class attribute and an instance attribute?",
          ["A class attribute is shared by all objects, an instance attribute belongs to one",
           "A class attribute can only be a number, an instance attribute can be anything",
           "A class attribute is private, an instance attribute is public",
           "A class attribute is created each time an object is made"], 0,
          "A class attribute has one copy on the class. Each object has its own copy of every instance attribute."),
        Q("What does `super().__init__(name, base)` do in a subclass constructor?",
          ["Runs the superclass constructor so the inherited attributes are set",
           "Creates a second copy of the subclass object and links the two together",
           "Deletes the superclass so that the subclass can stand on its own",
           "Overrides every inherited method with an empty version of it"], 0,
          "Without it the inherited part of the object is never initialised."),
        Q("What happens when you try to create an object from an abstract class?",
          ["A TypeError is raised", "The object is created with empty attributes",
           "The first subclass is created instead", "Nothing, because abstract classes are ignored"], 0,
          "An abstract class has methods with no implementation, so Python refuses to create an object from it."),
        Q("Which relationship does `class Car` having an `Engine` object that it creates and owns describe?",
          ["Composition", "Inheritance", "Association", "Polymorphism"], 0,
          "A car has an engine, and the engine is created and owned by the car, which is composition."),
        Q("What is polymorphism?",
          ["The same method call behaving differently depending on the class of the object",
           "A class that has more than one constructor with different parameters",
           "A subclass that inherits from more than one superclass at the same time",
           "Hiding the attributes of an object so they cannot be read from outside"], 0,
          "Calling shape.area() runs a different method for a Circle and a Rectangle, and the caller does not need to know which."),
        Q("In a UML class diagram, what does a `-` in front of an attribute mean?",
          ["Private", "Public", "Protected", "Static"], 0,
          "A minus means private, a plus public and a hash protected."),
        Q("Which line in a UML diagram means inheritance?",
          ["A solid line with a hollow triangle at the parent class", "A dashed line with an open arrowhead",
           "A line with a filled diamond at the whole", "A plain line with no end markers"], 0,
          "The hollow triangle points at the superclass, the more general class."),
        Q("What does `_balance` with one leading underscore indicate in Python?",
          ["It is protected by convention and should not be used from outside the class",
           "It is a constant that cannot be changed", "It is a class attribute",
           "It will be deleted when the object is destroyed"], 0,
          "Python does not enforce it. The single underscore is a signal to other programmers."),
        Q("Why is it often better to favour composition over inheritance?",
          ["Behaviour can be changed or added without altering existing classes",
           "Composition always runs faster", "Inheritance cannot be used with abstract classes",
           "Composition removes the need for constructors"], 0,
          "Inheritance fixes the relationship when the class is written. Composition lets parts be swapped."),
        Q("What does a `@staticmethod` have access to?",
          ["Neither the object nor the class, unless they are passed in as arguments",
           "The attributes of the object, through the self parameter that is passed in",
           "The attributes of the class, through the cls parameter that is passed in",
           "Only the private attributes of the object, and none of the public ones"], 0,
          "A static method is an ordinary function that happens to be stored in the class's namespace."),
    ],
    exam=[
        EQ("Explain what is meant by encapsulation, and give one benefit of using it.", 3, [
            MP("Data and the methods that work on it are combined in one class", ["combined", "bundled", "together", "one class", "grouped"]),
            MP("Access to the data from outside the class is restricted, for example by making attributes private", ["private", "restrict", "hidden", "hide", "access", "protected", "control"]),
            MP("Benefit: the data can only be changed through methods that check it is valid, so it stays consistent", ["valid", "consistent", "checks", "protect", "cannot be changed", "accidentally", "integrity", "security"]),
        ], "Encapsulation means that the data of an object and the methods that operate on it are combined in a single class, and access to the data from outside is restricted, usually by making the attributes private and providing methods to read or change them. The benefit is that the data can only be changed through methods that can check it is valid, so an object cannot be put into an inconsistent state by other parts of the program.",
           command="Explain"),
        EQ("Explain the difference between a class and an object, using an example.", 3, [
            MP("A class is a template or blueprint that defines attributes and methods", ["template", "blueprint", "definition", "defines", "design"]),
            MP("An object is an instance of a class, created from it", ["instance", "created from", "made from", "instantiated"]),
            MP("An example, such as Dog as a class and rex as an object, where each object has its own attribute values", ["example", "rex", "each object", "own values", "own data", "for example"]),
        ], "A class is a template that defines the attributes and methods that its objects will have. An object is an instance of a class, created from that template, and it has its own values for the attributes. For example, a Dog class defines a name and a bark method, and rex and bella are two separate Dog objects, each with their own name.",
           command="Explain"),
        EQ("A Vehicle class has a private attribute registration, a protected attribute speed that starts at 0, a method accelerate(amount) that increases the speed, and a method get_speed(). A subclass Lorry has an extra attribute load, and overrides accelerate so that the speed can never go above 60. Write Python class definitions for Vehicle and Lorry.", 6, [
            MP("Vehicle class with a constructor that sets registration as private and speed as 0", ["class vehicle", "__registration", "__init__", "self.__registration", "_speed = 0", "speed = 0"]),
            MP("accelerate adds amount to speed", ["speed += amount", "self._speed + amount", "speed + amount", "+= amount"]),
            MP("get_speed returns the speed", ["return self._speed", "def get_speed", "return"]),
            MP("Lorry inherits from Vehicle", ["class lorry(vehicle)", "(vehicle)", "inherits"]),
            MP("Lorry constructor calls super().__init__ and sets load", ["super().__init__", "super", "self.load", "load"]),
            MP("Lorry accelerate overrides, restricting the speed to a maximum of 60", ["60", "min(", "if", "override", "maximum", "cap"]),
        ], r"""```python
class Vehicle:
    def __init__(self, registration):
        self.__registration = registration
        self._speed = 0

    def accelerate(self, amount):
        self._speed += amount

    def get_speed(self):
        return self._speed

class Lorry(Vehicle):
    def __init__(self, registration, load):
        super().__init__(registration)
        self.load = load

    def accelerate(self, amount):
        self._speed = min(self._speed + amount, 60)

truck = Lorry("AB12 CDE", 8000)
truck.accelerate(45)
truck.accelerate(45)
print(truck.get_speed())
```

Vehicle keeps registration private and speed protected, so the subclass can use it. Lorry inherits from Vehicle, calls the superclass constructor to set up the inherited attributes, and overrides accelerate so that the speed is capped at 60. The calls shown print 60.""",
           command="Write"),
        EQ("Explain what is meant by polymorphism, using the shape classes in your answer as an example.", 3, [
            MP("The same method name can be called on objects of different classes", ["same method", "same name", "same call", "different classes", "different objects"]),
            MP("Each class provides its own version of the method, which overrides the one in the superclass", ["override", "own version", "own implementation", "each class", "different implementation"]),
            MP("The version that runs depends on the class of the object, so area() gives a different calculation for a circle and a rectangle", ["depends on", "circle", "rectangle", "area", "decided", "which class"]),
        ], "Polymorphism means that the same method can be called on objects of different classes and each responds in its own way. Each subclass provides its own version of the method, overriding the one in the superclass. For shapes, calling area() on a Circle object calculates pi times the radius squared and calling it on a Rectangle calculates width times height, and the program does not need to know which class it has because the object's class decides which version runs.",
           command="Explain"),
        EQ("A game has a Character class. Some characters can fly, some can swim and some can do both. Discuss whether inheritance or composition is the better way to model how a character moves.", 4, [
            MP("Inheritance gives a fixed is-a hierarchy, and a character that can do both cannot easily inherit from two separate parents", ["fixed", "hierarchy", "both", "multiple", "is-a", "difficult", "cannot"]),
            MP("Composition lets each ability be a separate class held as a part", ["separate class", "ability", "has-a", "part", "attribute", "held"]),
            MP("New abilities can be added or swapped without changing existing classes", ["add", "swap", "change", "without changing", "new ability", "flexible", "at run time"]),
            MP("Reasoned conclusion: composition is better because the abilities vary and combine", ["better", "conclusion", "composition because", "therefore", "overall", "i would"]),
        ], "Composition is the better choice. With inheritance, flying and swimming would each be a subclass, and a character that can do both would need to inherit from two parents or have a third class made for the combination, and every new ability would multiply the hierarchy. With composition each ability, such as Flying or Swimming, is its own class and a character holds the ones it has as attributes, so any combination is possible. A new ability can be added, or one swapped at run time, without changing any existing class, so composition suits behaviour that varies and combines.",
           command="Discuss"),
    ],
)
