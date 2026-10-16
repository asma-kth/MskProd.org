"""A Level Python: grammars, BNF, and building a small compiler."""
from mskbuild.models import Topic, Section, Q, EQ, MP

INPUTS = {}
EXPECT = {}

TOPIC = Topic(
    slug="grammars-parsing-and-compilers",
    title="Grammars, Parsing and Compilers",
    spec="A Level 17",
    icon="i-language",
    minutes=65,
    blurb="How a language is defined and how a program is translated. Write grammars in Backus-Naur form, then build every stage of a small compiler in Python: a tokeniser, a recursive descent parser, a syntax tree, a code generator for a stack machine, and an optimiser.",
    fact="Backus-Naur form is named after John Backus, who led the team that built FORTRAN, and Peter Naur, who used the notation to define ALGOL 60 in 1960. Almost every programming language since has had its syntax written down in a version of it.",
    sections=[
        Section("Describing a language with BNF", r"""
Every language has **syntax**, the rules for what is allowed, and **semantics**, what it means. `print("hi"` has a syntax error because a bracket is missing. `1 / 0` is perfectly good syntax and still fails when it runs.

To define syntax precisely, enough that a program can check it, we write a **grammar**. The standard notation is **Backus-Naur form** (BNF). A grammar is a list of **rules**:

```text
<digit>   ::= 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
<integer> ::= <digit> | <digit> <integer>
<sign>    ::= + | -
<number>  ::= <integer> | <sign> <integer>
```

- `<name>` in angle brackets is a **non-terminal**: something defined by another rule.
- Anything else, such as `0` or `+`, is a **terminal**: it appears in the text exactly as written.
- `::=` means *is defined as*
- `|` means *or*

Rule two is the clever one. An `<integer>` is either a single digit, or a digit followed by *another integer*. The rule uses itself, so it can describe numbers of any length with just two lines. **Recursion is how BNF expresses repetition.**

### Deriving a string

To show that `-407` is a `<number>`, start from `<number>` and rewrite one non-terminal at a time using a rule. This is a **derivation**:

```text
<number>
<sign> <integer>
- <integer>
- <digit> <integer>
- 4 <integer>
- 4 <digit> <integer>
- 4 0 <integer>
- 4 0 <digit>
- 4 0 7
```

### From grammar to program

Each rule becomes a function. It takes the text and a position, and returns the position after what it matched, or `None` if it did not match.

```python
def digit(text, i):                        # <digit> ::= 0 | 1 | ... | 9
    if i < len(text) and text[i] in "0123456789":
        return i + 1
    return None

def integer(text, i):                      # <integer> ::= <digit> | <digit> <integer>
    after_digit = digit(text, i)
    if after_digit is None:
        return None
    longer = integer(text, after_digit)
    return longer if longer is not None else after_digit

def number(text, i):                       # <number> ::= <integer> | <sign> <integer>
    if i < len(text) and text[i] in "+-":
        i = i + 1
    return integer(text, i)

def is_number(text):
    return number(text, 0) == len(text)

for text in ["407", "-407", "+5", "4-7", "", "-"]:
    print(repr(text), is_number(text))
```

### What BNF can do that a regular expression cannot

The grammar for balanced brackets uses recursion in the middle of a rule, which an FSM or a regular expression cannot do:

```text
<balanced> ::= "" | "(" <balanced> ")" <balanced>
```

```python
def balanced(text, i):
    if i < len(text) and text[i] == "(":
        j = balanced(text, i + 1)                       # the part inside the brackets
        if j is None or j >= len(text) or text[j] != ")":
            return None
        return balanced(text, j + 1)                    # whatever follows
    return i                                            # the empty alternative

def is_balanced(text):
    return balanced(text, 0) == len(text)

for text in ["(())()", "(()", "())(", "", "((()))"]:
    print(repr(text), is_balanced(text))
```

!key Syntax diagrams :: The same rules can be drawn as **syntax diagrams** (railroad diagrams), with a path to follow through boxes for non-terminals and ovals for terminals. They carry the same information as BNF. Questions on either one are common.

"""),
        Section("Lexical analysis: from text to tokens", r"""
A compiler or interpreter does not work on raw characters. It works in **stages**, and the output of each is the input to the next.

| Stage | Job |
| **Lexical analysis** | Break the source text into **tokens**, discarding spaces and comments |
| **Syntax analysis** | Check the tokens follow the grammar, and build a tree |
| **Semantic analysis** | Check the meaning: names exist, types fit together |
| **Code generation** | Produce machine code or bytecode from the tree |
| **Optimisation** | Make the result smaller or faster without changing what it does |

The first stage is the **lexer** (or tokeniser). A **token** is the smallest meaningful unit: a number, a name, an operator. It becomes a pair of *what kind* and *what text*. The patterns for the kinds are regular expressions, which is why the last topic matters here.

```python
import re

class ParseError(Exception):
    pass

TOKEN = re.compile(r"\s*(?:(?P<NUMBER>\d+(?:\.\d+)?)|(?P<NAME>[A-Za-z_]\w*)|(?P<OP>[-+*/()=]))")

def tokenise(source):
    tokens, pos = [], 0
    source = source.rstrip()
    while pos < len(source):
        found = TOKEN.match(source, pos)
        if not found:
            bad = source[pos:].lstrip()[0]
            raise ParseError("unexpected character " + repr(bad))
        pos = found.end()
        tokens.append((found.lastgroup, found.group(found.lastgroup)))
    return tokens

print(tokenise("total = price * (2 + 3.5)"))
try:
    tokenise("3 $ 4")
except ParseError as problem:
    print(problem)
```

The spaces have vanished, `3.5` is one token not three, and `$` belongs to no kind so the lexer reports it. A lexer finds **lexical errors** (a character that cannot start any token) and the stage after it finds **syntax errors** (tokens in the wrong order).
"""),
        Section("Syntax analysis: a recursive descent parser", r"""
The **parser** takes the tokens and checks them against the grammar. It also builds an **abstract syntax tree** (AST): a tree that shows how the pieces fit together, with brackets and punctuation gone because the shape of the tree says it all.

The grammar for arithmetic builds the rules of precedence into its structure. A **term** is multiplied things and an **expression** is added terms, so `*` binds more tightly than `+` without any extra rule:

```text
<expression> ::= <term> { ( + | - ) <term> }
<term>       ::= <factor> { ( * | / ) <factor> }
<factor>     ::= <number> | <name> | ( <expression> ) | - <factor>
```

Here `{ }` means *zero or more times*, an extension called EBNF. It is written as a loop rather than as recursion, so `10 - 4 - 3` is worked out left to right as `(10 - 4) - 3`.

In a **recursive descent** parser there is one function for each rule. A rule that mentions another rule calls that function, and `<factor>` calls `<expression>` for a bracket, so the parser is recursive in exactly the places the grammar is.

```python
import re

class ParseError(Exception):
    pass

TOKEN = re.compile(r"\s*(?:(?P<NUMBER>\d+(?:\.\d+)?)|(?P<NAME>[A-Za-z_]\w*)|(?P<OP>[-+*/()=]))")

def tokenise(source):
    tokens, pos = [], 0
    source = source.rstrip()
    while pos < len(source):
        found = TOKEN.match(source, pos)
        if not found:
            raise ParseError("unexpected character " + repr(source[pos:].lstrip()[0]))
        pos = found.end()
        tokens.append((found.lastgroup, found.group(found.lastgroup)))
    return tokens

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else ("END", "")

    def take(self, expected=None):
        kind, value = self.peek()
        if expected is not None and value != expected:
            raise ParseError("expected " + repr(expected) + " but found " + repr(value or "end of input"))
        self.pos += 1
        return kind, value

    def expression(self):                       # <term> { ( + | - ) <term> }
        node = self.term()
        while self.peek()[1] in ("+", "-"):
            op = self.take()[1]
            node = (op, node, self.term())
        return node

    def term(self):                             # <factor> { ( * | / ) <factor> }
        node = self.factor()
        while self.peek()[1] in ("*", "/"):
            op = self.take()[1]
            node = (op, node, self.factor())
        return node

    def factor(self):                           # <number> | <name> | ( <expression> ) | - <factor>
        kind, value = self.peek()
        if kind == "NUMBER":
            self.take()
            return ("num", float(value) if "." in value else int(value))
        if kind == "NAME":
            self.take()
            return ("var", value)
        if value == "(":
            self.take()
            node = self.expression()
            self.take(")")
            return node
        if value == "-":
            self.take()
            return ("neg", self.factor())
        raise ParseError("unexpected " + repr(value or "end of input"))

def parse(source):
    parser = Parser(tokenise(source))
    tree = parser.expression()
    if parser.peek()[0] != "END":
        raise ParseError("unexpected " + repr(parser.peek()[1]) + " after the expression")
    return tree

def show(node, depth=0):
    pad = "    " * depth
    if node[0] in ("num", "var"):
        print(pad + str(node[1]))
    elif node[0] == "neg":
        print(pad + "neg")
        show(node[1], depth + 1)
    else:
        print(pad + node[0])
        show(node[1], depth + 1)
        show(node[2], depth + 1)

print(parse("2 + 3 * 4"))
show(parse("2 + 3 * 4"))
print("--- with brackets")
show(parse("(2 + 3) * 4"))
print("--- left to right")
print(parse("10 - 4 - 3"))
for bad in ["2 +", "(2 + 3", "2 3", "* 4"]:
    try:
        parse(bad)
    except ParseError as problem:
        print(repr(bad), "->", problem)
```

In `2 + 3 * 4` the `*` sits lower in the tree than the `+`, so it is worked out first. Adding brackets changes the shape of the tree, not the rules. A tree whose leaves are numbers and whose inner nodes are operators is called an **expression tree**, and it appears in the trees topic too.

!warn Syntax is not meaning :: A parser accepts `x / (y - y)` because it follows the grammar. The mistake only shows when the program runs. The syntax stage cannot catch it, and neither can the lexer.
"""),
        Section("Code generation, a stack machine and optimisation", r"""
A tree can be **evaluated directly** by walking it, which is how an **interpreter** works. Or it can be **translated** into a flat list of instructions to be run later, which is **code generation**.

The simplest target is a **stack machine**. It has a handful of instructions and one stack:

| Instruction | Does |
| `PUSH n` | puts the number n on the stack |
| `LOAD x` | puts the value of the variable x on the stack |
| `ADD` `SUB` `MUL` `DIV` | pops two numbers, pushes the result |
| `NEG` | pops one number, pushes its negative |

Visiting the tree *left, then right, then the operator* (a **post-order traversal**) gives exactly the order a stack machine needs. It is also the **Reverse Polish notation** from the stacks and queues topic: a compiler is a conversion from infix to postfix with a tree in the middle.

```python
import re

class ParseError(Exception):
    pass

TOKEN = re.compile(r"\s*(?:(?P<NUMBER>\d+(?:\.\d+)?)|(?P<NAME>[A-Za-z_]\w*)|(?P<OP>[-+*/()=]))")

def tokenise(source):
    tokens, pos = [], 0
    source = source.rstrip()
    while pos < len(source):
        found = TOKEN.match(source, pos)
        if not found:
            raise ParseError("unexpected character " + repr(source[pos:].lstrip()[0]))
        pos = found.end()
        tokens.append((found.lastgroup, found.group(found.lastgroup)))
    return tokens

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else ("END", "")

    def take(self, expected=None):
        kind, value = self.peek()
        if expected is not None and value != expected:
            raise ParseError("expected " + repr(expected))
        self.pos += 1
        return kind, value

    def expression(self):
        node = self.term()
        while self.peek()[1] in ("+", "-"):
            op = self.take()[1]
            node = (op, node, self.term())
        return node

    def term(self):
        node = self.factor()
        while self.peek()[1] in ("*", "/"):
            op = self.take()[1]
            node = (op, node, self.factor())
        return node

    def factor(self):
        kind, value = self.peek()
        if kind == "NUMBER":
            self.take()
            return ("num", float(value) if "." in value else int(value))
        if kind == "NAME":
            self.take()
            return ("var", value)
        if value == "(":
            self.take()
            node = self.expression()
            self.take(")")
            return node
        if value == "-":
            self.take()
            return ("neg", self.factor())
        raise ParseError("unexpected " + repr(value or "end of input"))

def parse(source):
    return Parser(tokenise(source)).expression()

# ---- new in this section ------------------------------------------------

NAMES = {"+": "ADD", "-": "SUB", "*": "MUL", "/": "DIV"}

def generate(node, code):
    kind = node[0]
    if kind == "num":
        code.append(("PUSH", node[1]))
    elif kind == "var":
        code.append(("LOAD", node[1]))
    elif kind == "neg":
        generate(node[1], code)
        code.append(("NEG", None))
    else:
        generate(node[1], code)              # left
        generate(node[2], code)              # right
        code.append((NAMES[kind], None))     # then the operator
    return code

def run(code, variables):
    stack = []
    for op, arg in code:
        if op == "PUSH":
            stack.append(arg)
        elif op == "LOAD":
            stack.append(variables[arg])
        elif op == "NEG":
            stack.append(-stack.pop())
        else:
            b = stack.pop()
            a = stack.pop()
            if op == "ADD":
                stack.append(a + b)
            elif op == "SUB":
                stack.append(a - b)
            elif op == "MUL":
                stack.append(a * b)
            else:
                stack.append(a / b)
        label = op if arg is None else op + " " + str(arg)
        print("   ", label, "->", stack)
    return stack.pop()

program = generate(parse("(2 + 3) * x"), [])
print(program)
print("result:", run(program, {"x": 4}))
```

### Optimisation

The last stage improves the code without changing what it does. A simple and common one is **constant folding**: if both sides of an operator are already numbers, work it out *once*, while compiling, instead of every time the program runs.

```python
def evaluate(node):
    kind = node[0]
    if kind == "num":
        return node[1]
    a, b = evaluate(node[1]), evaluate(node[2])
    return {"+": a + b, "-": a - b, "*": a * b}[kind]

def fold(node):
    kind = node[0]
    if kind in ("num", "var"):
        return node
    left, right = fold(node[1]), fold(node[2])
    if left[0] == "num" and right[0] == "num":
        return ("num", evaluate((kind, left, right)))
    return (kind, left, right)

def count(node):
    return 1 if node[0] in ("num", "var") else 1 + count(node[1]) + count(node[2])

# the tree for 2 * 3 + x * (4 - 1)
before = ("+", ("*", ("num", 2), ("num", 3)), ("*", ("var", "x"), ("-", ("num", 4), ("num", 1))))
after = fold(before)
print(after)
print("tree nodes:", count(before), "->", count(after))
```

### Compiler, interpreter or both?

| | Compiler | Interpreter |
| Translates | the whole program before it runs | one statement at a time as it runs |
| Output | a separate executable file | none: the source is run directly |
| Speed when running | fast, and optimised | slower, since it translates every time |
| Errors | all syntax errors reported before running | reported only when that line is reached |
| Distribution | the user needs no translator, but a version for each type of machine | the user needs the interpreter, and the same source runs anywhere |

Real systems mix them. Python compiles source into **bytecode**, a stack machine much like the one above, and a **virtual machine** runs it. Java does the same. An **assembler** is the simplest translator of all, turning each assembly instruction into one machine code instruction.

Python lets you look at the tree its own parser builds:

```python
import ast

tree = ast.parse("2 + 3 * 4", mode="eval")
print(ast.dump(tree.body, indent=2))
```
"""),
        Section("A small language, from source to result", r"""
Put the stages together and you have the front end of a language. This one has variables, `print`, and arithmetic. Its programs are checked **completely** before anything runs. That is a **compile time** check, so a syntax error on line 40 stops the program before line 1 does anything. A mistake that is only found *while running*, such as a name with no value, is a **runtime** error.

```python
import re

class ParseError(Exception):
    pass

class RunError(Exception):
    pass

TOKEN = re.compile(r"\s*(?:(?P<NUMBER>\d+(?:\.\d+)?)|(?P<NAME>[A-Za-z_]\w*)|(?P<OP>[-+*/()=]))")

def tokenise(source):
    tokens, pos = [], 0
    source = source.rstrip()
    while pos < len(source):
        found = TOKEN.match(source, pos)
        if not found:
            raise ParseError("unexpected character " + repr(source[pos:].lstrip()[0]))
        pos = found.end()
        tokens.append((found.lastgroup, found.group(found.lastgroup)))
    return tokens

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else ("END", "")

    def take(self, expected=None):
        kind, value = self.peek()
        if expected is not None and value != expected:
            raise ParseError("expected " + repr(expected) + " but found " + repr(value or "end of line"))
        self.pos += 1
        return kind, value

    def expression(self):
        node = self.term()
        while self.peek()[1] in ("+", "-"):
            op = self.take()[1]
            node = (op, node, self.term())
        return node

    def term(self):
        node = self.factor()
        while self.peek()[1] in ("*", "/"):
            op = self.take()[1]
            node = (op, node, self.factor())
        return node

    def factor(self):
        kind, value = self.peek()
        if kind == "NUMBER":
            self.take()
            return ("num", float(value) if "." in value else int(value))
        if kind == "NAME" and value != "print":
            self.take()
            return ("var", value)
        if value == "(":
            self.take()
            node = self.expression()
            self.take(")")
            return node
        if value == "-":
            self.take()
            return ("neg", self.factor())
        raise ParseError("unexpected " + repr(value or "end of line"))

# ---- statements ---------------------------------------------------------

def compile_line(line):
    parser = Parser(tokenise(line))
    kind, value = parser.peek()
    if (kind, value) == ("NAME", "print"):
        parser.take()
        statement = ("print", None, parser.expression())
    elif kind == "NAME":
        name = parser.take()[1]
        parser.take("=")
        statement = ("assign", name, parser.expression())
    else:
        raise ParseError("a line must start with print or a name")
    if parser.peek()[0] != "END":
        raise ParseError("unexpected " + repr(parser.peek()[1]) + " at the end of the line")
    return statement

def evaluate(node, env):
    kind = node[0]
    if kind == "num":
        return node[1]
    if kind == "var":
        if node[1] not in env:
            raise RunError(node[1] + " has no value yet")
        return env[node[1]]
    if kind == "neg":
        return -evaluate(node[1], env)
    a, b = evaluate(node[1], env), evaluate(node[2], env)
    if kind == "+":
        return a + b
    if kind == "-":
        return a - b
    if kind == "*":
        return a * b
    if b == 0:
        raise RunError("division by zero")
    return a / b

def compile_program(source):
    statements = []
    for number, line in enumerate(source.strip().split("\n"), start=1):
        try:
            statements.append((number,) + compile_line(line))
        except ParseError as problem:
            raise ParseError("line " + str(number) + ": " + str(problem))
    return statements

def execute(statements):
    env = {}
    for number, kind, name, tree in statements:
        try:
            value = evaluate(tree, env)
        except RunError as problem:
            raise RunError("line " + str(number) + ": " + str(problem))
        if kind == "print":
            print(value)
        else:
            env[name] = value

def go(title, source):
    print("==", title)
    try:
        execute(compile_program(source))
    except ParseError as problem:
        print("syntax error, nothing ran ->", problem)
    except RunError as problem:
        print("runtime error ->", problem)

go("a good program", '''
print 100
price = 20
quantity = 3
total = price * quantity
print total - 5
print (total + 10) / 2
''')
go("a syntax error on line 3", '''
print 100
total = 4 * (3 +
print total
''')
go("a runtime error on line 3", '''
print 100
x = 5
print x / (x - 5)
print 999
''')
go("a name with no value", '''
print 100
print cost * 2
''')
```

The first line, `print 100`, runs in the good program and the runtime error program, and **does not run at all** in the syntax error one. That is the difference between the two kinds of error.

!exam Name the stage, then say what it does :: Compilation questions give a mark for each stage correctly named in order (lexical analysis, syntax analysis, code generation, optimisation) and a mark for each job: tokens, tree, machine code, faster or smaller code.
"""),
    ],
    keyterms=[
        ("Syntax", "The rules that decide whether a program is correctly formed."),
        ("Semantics", "The meaning of a program, which decides what it does when it runs."),
        ("Backus-Naur form (BNF)", "A notation for writing the syntax rules of a language, using non-terminals, terminals, ::= and |."),
        ("Terminal", "A symbol that appears in the language exactly as written, such as 0 or +."),
        ("Non-terminal", "A symbol, written in angle brackets, that is defined by another rule."),
        ("Lexical analysis", "The first stage of translation, which splits the source text into tokens and removes spaces and comments."),
        ("Token", "The smallest meaningful unit of a program, such as a name, a number or an operator."),
        ("Syntax analysis (parsing)", "Checking that the tokens follow the grammar, usually building a tree."),
        ("Abstract syntax tree", "A tree showing the structure of a program, with punctuation removed."),
        ("Code generation", "Translating the parsed program into machine code or bytecode."),
        ("Optimisation", "Improving the generated code so it is smaller or quicker, without changing what it does."),
        ("Compiler", "A translator that converts the whole of a program to machine code before it is run."),
        ("Interpreter", "A translator that analyses and runs a program one statement at a time."),
        ("Bytecode", "A compact set of instructions for a virtual machine, produced by compilers such as Python's."),
    ],
    grade="""
Translation questions are mostly about getting the stages and their jobs right, and BNF questions are about the structure of a rule.

+ Name the stages in order: lexical analysis, syntax analysis, semantic analysis, code generation, optimisation
+ Give the output of each stage: tokens, a tree, machine code or bytecode
+ In BNF, use recursion for repetition: `<integer> ::= <digit> | <digit> <integer>`
+ Always give a base case alternative in a recursive rule, or the rule can never end
+ Compare compilers and interpreters in both directions: speed against ease of testing, one executable against the same source anywhere
""",
    mistakes=[
        "Writing a BNF rule that is recursive but has no non-recursive alternative, so no string can ever be derived from it.",
        "Putting terminals in angle brackets, or non-terminals without them.",
        "Saying the lexer checks grammar. The lexer only splits the text into tokens.",
        "Confusing a syntax error, found before the program runs, with a runtime error, found while it runs.",
        "Claiming an interpreter produces an executable file. It does not: it runs the source directly.",
    ],
    quiz=[
        Q("In BNF, what does `::=` mean?",
          ["Is defined as", "Is equal to", "Is assigned the value", "Is greater than or equal to"], 0,
          "A rule such as <digit> ::= 0 | 1 reads: a digit is defined as 0 or 1."),
        Q("In the rule `<integer> ::= <digit> | <digit> <integer>`, how is repetition shown?",
          ["By the rule referring to itself", "By a loop symbol", "By the | symbol", "By the angle brackets"], 0,
          "Recursion lets a rule describe a string of any length: an integer is a digit followed by another integer."),
        Q("What is a terminal in a BNF grammar?",
          ["A symbol that appears in the language exactly as written", "The last rule in the grammar", "A symbol defined by another rule", "A rule that can never be used"], 0,
          "Digits and operators are terminals. Non-terminals are written in angle brackets and defined by rules."),
        Q("What is the output of the lexical analysis stage?",
          ["A sequence of tokens", "Machine code", "A syntax tree", "A list of syntax errors only"], 0,
          "The lexer splits the source text into tokens and discards spaces and comments."),
        Q("Which stage checks that the tokens follow the rules of the grammar?",
          ["Syntax analysis", "Lexical analysis", "Optimisation", "Code generation"], 0,
          "The parser checks the order of the tokens against the grammar, and usually builds a tree."),
        Q("Which of these is found by the syntax analysis stage?",
          ["A missing closing bracket", "A division by zero", "A wrong answer from a correct looking formula", "A file that does not exist"], 0,
          "A missing bracket breaks the grammar. The others only show up when the program runs."),
        Q("What is constant folding?",
          ["Working out an expression made only of numbers once, at compile time", "Storing constants in a table", "Removing comments from the code", "Converting text to tokens"], 0,
          "2 * 3 becomes 6 during compilation, so the work is not repeated every time the program runs."),
        Q("What is one advantage of a compiler over an interpreter?",
          ["The compiled program usually runs faster", "It can run on any type of computer without changes", "It reports errors only when each line runs", "It needs no translator at all"], 0,
          "The translation is done once, in advance, and the result can be optimised."),
        Q("What is one advantage of an interpreter?",
          ["It can run and test one line at a time, so errors are easy to find while developing", "It produces faster code", "It checks the whole program before running", "It produces a standalone executable"], 0,
          "An interpreter runs a statement as soon as it is translated, which suits testing and debugging."),
        Q("Python translates source code into bytecode, which a virtual machine then runs. What does that make Python?",
          ["Both compiled and interpreted", "Only interpreted", "Only compiled", "Neither"], 0,
          "It compiles to an intermediate form and then interprets that. Many languages work this way."),
    ],
    exam=[
        EQ("The grammar for a variable name states that it must start with a letter, followed by any number of letters or digits. Write a BNF definition for a variable name, including definitions for a letter and for a digit. You may use ... to shorten a list of alternatives.", 4, [
            MP("A definition of <letter> as a | b | ... | z (and capitals) and <digit> as 0 | ... | 9", ["<letter>", "<digit>", "a | b", "0 | 1"]),
            MP("Uses ::= and | correctly and the angle brackets for non-terminals", ["::=", "|", "<"]),
            MP("A rule where a name can be just a letter (a non-recursive base case)", ["<letter>", "base", "single letter", "just a letter"]),
            MP("A recursive rule that extends a name by a letter or digit", ["<name> <letter>", "<variable> <letter>", "<name> <digit>", "<variable> <digit>", "recursive", "recursion"]),
        ], r"""```text
<letter>   ::= a | b | c | ... | z | A | B | ... | Z
<digit>    ::= 0 | 1 | 2 | ... | 9
<variable> ::= <letter> | <variable> <letter> | <variable> <digit>
```

A variable is either a single letter, or a variable followed by a letter, or a variable followed by a digit. The recursion allows names of any length, and the first alternative gives it a place to start, so the rule can end.""",
           command="Write"),
        EQ("The line of a program shown is passed to the lexical analysis stage of a compiler. State the tokens that are produced, and state what the lexical analyser does with the spaces.", 3, [
            MP("Identifies the names and operators as separate tokens: total, =, price, *, 2, +, 1", ["total", "price", "=", "*", "+"]),
            MP("Identifies the numbers 2 and 1 as number tokens", ["2", "1", "number", "numeric"]),
            MP("White space is removed (ignored) and does not produce a token", ["removed", "ignored", "discarded", "no token", "not tokens"]),
        ], "The tokens are the name total, the operator =, the name price, the operator *, the number 2, the operator + and the number 1. The spaces are removed by the lexical analyser, and do not produce any tokens.",
           command="State",
           figure="""```text
total = price * 2 + 1
```"""),
        EQ("Describe the purpose of two stages in the compilation of a high-level language program.", 4, [
            MP("Lexical analysis: splits the source code into tokens", ["lexical", "tokens", "token"]),
            MP("and removes spaces and comments (or reports invalid symbols)", ["spaces", "comments", "white space", "invalid", "remove"]),
            MP("Syntax analysis: checks the tokens follow the rules (grammar) of the language, reporting syntax errors", ["syntax analysis", "grammar", "rules", "syntax errors", "parser"]),
            MP("Code generation: produces the machine code (or bytecode); optimisation makes it smaller or faster", ["code generation", "machine code", "bytecode", "optimisation", "faster", "smaller"]),
        ], "In lexical analysis the source code is split into tokens such as names, numbers and operators, and spaces and comments are removed. In syntax analysis the tokens are checked against the grammar rules of the language, any syntax errors are reported, and a syntax tree is usually built. In code generation the tree is translated into machine code or bytecode, and optimisation then changes it so that it is smaller or runs faster without changing what it does.",
           command="Describe"),
        EQ("A stack machine evaluates the expression 2 + 3 * 4. Show the instructions that would be generated, using PUSH, ADD and MUL, and state the value left on the stack.", 4, [
            MP("Recognises that 3 * 4 is done first because * has higher precedence", ["precedence", "3 * 4", "multiplication first", "first"]),
            MP("Instructions PUSH 2, PUSH 3, PUSH 4 in that order", ["push 2", "push 3", "push 4"]),
            MP("Followed by MUL and then ADD", ["mul", "add"]),
            MP("The value left on the stack is 14", ["14"]),
        ], "Multiplication has higher precedence, so 3 * 4 is calculated before the addition. The instructions are PUSH 2, PUSH 3, PUSH 4, MUL, ADD. MUL takes 3 and 4 off the stack and pushes 12, then ADD takes 2 and 12 off the stack and pushes 14. The value left on the stack is 14. This order is the Reverse Polish form 2 3 4 * +.",
           command="Show"),
        EQ("A software company is deciding whether to supply a program as compiled code or to supply the source code to be run with an interpreter. Discuss which it should choose.", 6, [
            MP("Compiled code is already translated, so it runs faster", ["faster", "quicker", "already translated", "speed"]),
            MP("The compiled program does not need a translator on the user's computer", ["no translator", "does not need", "standalone", "executable"]),
            MP("Compiled code hides the source code, protecting the company's work", ["hides", "source code", "protect", "intellectual property", "copy"]),
            MP("But the compiled code only runs on one type of processor or operating system, so versions are needed for each", ["one type", "each", "platform", "operating system", "different versions", "versions"]),
            MP("An interpreted program runs on any computer that has the interpreter, but is slower and exposes the source code", ["any computer", "portable", "slower", "interpreter"]),
            MP("A reasoned conclusion", ["conclusion", "therefore", "overall", "i would", "best choice", "should"]),
        ], "Compiled code has already been translated into machine code, so it runs faster and the user does not need a translator installed. It also keeps the company's source code hidden, which protects its work from being copied. However, it will only run on one type of processor and operating system, so the company must produce and support a different version for each. Supplying source code to be interpreted lets the same program run on any computer that has the interpreter, but it will run more slowly and the source code is exposed. For a commercial program that has to be quick and where the source code is valuable, the company should supply compiled code, producing a version for each of the systems it wants to support.",
           command="Discuss"),
    ],
)
