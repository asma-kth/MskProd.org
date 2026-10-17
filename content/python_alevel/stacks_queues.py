"""A Level Python: stacks and queues, built from arrays and pointers."""
from mskbuild.models import Topic, Section, Q, EQ, MP

INPUTS = {}
EXPECT = {}

TOPIC = Topic(
    slug="stacks-and-queues",
    title="Stacks and Queues",
    spec="A Level 4",
    icon="i-layers",
    minutes=50,
    blurb="Last in first out and first in first out, built the way the exam asks for them, from a fixed array and pointers, with overflow and underflow, circular and priority queues, bracket matching, Reverse Polish and a round robin scheduler.",
    fact="The 1960s computer scientist Edsger Dijkstra's shunting yard algorithm, which converts everyday arithmetic into the form a stack can evaluate, is named after the railway yard where trains are shunted onto sidings in the order they need to leave.",
    sections=[
        Section("Stacks", r"""
A **stack** is a collection where items are added and removed at **one end only**, the top. The last item in is the first item out, so it is called **LIFO**, last in first out. Think of a pile of plates.

| Operation | Does | Python list |
| `push(item)` | adds an item to the top | `items.append(item)` |
| `pop()` | removes and returns the top item | `items.pop()` |
| `peek()` | returns the top item without removing it | `items[-1]` |
| `is_empty()` | is there nothing in it? | `items == []` |
| `is_full()` | is there no room left? | only for a fixed size stack |

### Built from an array and a pointer

The exam describes a stack as a **fixed size array** with a **pointer** to the top item. The pointer starts at -1, meaning the stack is empty, and moves up by one on a push and down by one on a pop.

```python
class Stack:
    def __init__(self, capacity):
        self.items = [None] * capacity
        self.top = -1

    def is_empty(self):
        return self.top == -1

    def is_full(self):
        return self.top == len(self.items) - 1

    def push(self, item):
        if self.is_full():
            raise OverflowError("stack overflow")
        self.top += 1
        self.items[self.top] = item

    def pop(self):
        if self.is_empty():
            raise IndexError("stack underflow")
        item = self.items[self.top]
        self.top -= 1
        return item

    def peek(self):
        if self.is_empty():
            raise IndexError("stack is empty")
        return self.items[self.top]

s = Stack(3)
s.push(10)
s.push(20)
s.push(30)
print(s.is_full(), s.peek())          # True 30
print(s.pop(), s.pop(), s.top)        # 30 20 0
```

Two errors, and the exam names both:

- **Stack overflow**: pushing onto a stack that is full.
- **Stack underflow**: popping from a stack that is empty.

!key Popping does not erase :: In the array version `pop` only moves the pointer down. The old value is still in the array, but it is outside the stack because it is above `top`, and the next push overwrites it.

### Where stacks are used

| Use | How the stack is involved |
| The call stack | Each call pushes a frame, each return pops one, which is what makes recursion work |
| Undo | Every action is pushed, and undo pops the latest |
| Back button | Each page visited is pushed, and Back pops the latest |
| Expression evaluation | Operands are held until the operator that needs them arrives |
| Bracket checking | An opening bracket is pushed and each closing one must match the top |

### Bracket matching

Every closing bracket must match the most recent opening bracket not yet closed, and that is exactly the top of a stack.

```python
def balanced(text):
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in text:
        if ch in "([{":
            stack.append(ch)
        elif ch in ")]}":
            if not stack or stack.pop() != pairs[ch]:
                return False
    return not stack

print(balanced("{[()]}"), balanced("(]"), balanced("(()"))     # True False False
```

The three results come from three different failures. `(]` closes the wrong kind. `(()` leaves one open, so the stack is not empty at the end.

### Undo and redo with two stacks

```python
document = ""
undo_stack = []
redo_stack = []

def type_text(extra):
    global document
    undo_stack.append(document)
    redo_stack.clear()
    document = document + extra

def undo():
    global document
    if undo_stack:
        redo_stack.append(document)
        document = undo_stack.pop()

def redo():
    global document
    if redo_stack:
        undo_stack.append(document)
        document = redo_stack.pop()

type_text("Hello")
type_text(" world")
print(document)                 # Hello world
undo()
print(document)                 # Hello
undo()
print(repr(document))           # ''
redo()
print(document)                 # Hello
type_text("!")
redo()                          # nothing to redo: typing cleared the redo stack
print(document)                 # Hello!
```
"""),
        Section("Queues", r"""
A **queue** adds items at the **rear** and removes them from the **front**, so the first item in is the first out: **FIFO**. A queue of people is the example.

| Operation | Does |
| `enqueue(item)` | adds an item at the rear |
| `dequeue()` | removes and returns the item at the front |
| `is_empty()` and `is_full()` | the same tests as for a stack |

A Python list can be a queue, but `items.pop(0)` has to shuffle every other item along by one place, which gets slow as the list grows. `collections.deque` is built for it, and adds and removes at both ends in constant time.

```python
from collections import deque

queue = deque()
queue.append("Asha")               # enqueue
queue.append("Ben")
queue.append("Chloe")
print(queue.popleft(), queue)      # Asha deque(['Ben', 'Chloe'])
```

### The linear queue wastes space

If a queue is a fixed array with a front and a rear pointer that only ever move forward, then once the rear reaches the end of the array the queue is "full", even when the front has moved on and the first places are free. Shuffling everything back is slow.

### The circular queue

A **circular queue** treats the array as a ring. When a pointer moves past the last position, it **wraps** round to the first, and the remainder operator does it:

```text
next_position = (position + 1) MOD size
```

!diagram py-circular-queue

```python
class CircularQueue:
    def __init__(self, capacity):
        self.items = [None] * capacity
        self.front = 0
        self.rear = -1
        self.count = 0

    def is_empty(self):
        return self.count == 0

    def is_full(self):
        return self.count == len(self.items)

    def enqueue(self, item):
        if self.is_full():
            raise OverflowError("queue is full")
        self.rear = (self.rear + 1) % len(self.items)
        self.items[self.rear] = item
        self.count += 1

    def dequeue(self):
        if self.is_empty():
            raise IndexError("queue is empty")
        item = self.items[self.front]
        self.items[self.front] = None
        self.front = (self.front + 1) % len(self.items)
        self.count -= 1
        return item

q = CircularQueue(4)
for letter in "ABCD":
    q.enqueue(letter)
print(q.items, q.front, q.rear)            # ['A', 'B', 'C', 'D'] 0 3
print(q.dequeue(), q.dequeue())            # A B
q.enqueue("E")
q.enqueue("F")
print(q.items, q.front, q.rear)            # ['E', 'F', 'C', 'D'] 2 1
```

After `E` and `F` are added the rear pointer has wrapped round to position 1, so the queue spans the end of the array and the start. Without the circular design the array would have been declared full after `D`, with two empty places at the front.

A counter, `count`, is kept as well as the pointers, because when `front` and `rear` are neighbours you cannot tell from the pointers alone whether the queue is completely full or completely empty.

### Priority queues

In a **priority queue** each item has a priority, and the item removed is the one with the highest priority, whatever order they arrived in. `heapq` keeps a list so that the smallest item is always removed first, so a lower number means a higher priority:

```python
import heapq

tasks = []
heapq.heappush(tasks, (2, "print report"))
heapq.heappush(tasks, (1, "fire alarm"))
heapq.heappush(tasks, (3, "update software"))

while tasks:
    print(heapq.heappop(tasks))
```

### A queue at work: round robin scheduling

An operating system shares one processor between many processes. In **round robin** scheduling each process gets a fixed slice of time, the **quantum**. If it has not finished, it goes to the back of the queue.

```python
from collections import deque

processes = deque([("A", 5), ("B", 2), ("C", 4)])
quantum = 2
time = 0

while processes:
    name, remaining = processes.popleft()
    run = min(quantum, remaining)
    time = time + run
    remaining = remaining - run
    if remaining > 0:
        processes.append((name, remaining))
        print(time, name, "paused with", remaining, "left")
    else:
        print(time, name, "finished")
```

| Structure | Order out | Used for |
| Stack | Last in, first out | Undo, the call stack, expression evaluation |
| Queue | First in, first out | Print jobs, keyboard buffer, scheduling, breadth first search |
| Priority queue | Highest priority first | Scheduling urgent jobs, shortest path algorithms |
"""),
        Section("Expressions: infix, postfix and the shunting yard", r"""
We write arithmetic in **infix** notation, with the operator between its operands: `3 + 4 * 2`. It needs brackets and rules about which operator goes first. **Reverse Polish notation**, also called **postfix**, puts the operator **after** its operands: `3 4 2 * +`. It needs neither. The order of the operators is the order of the calculation.

| Infix | Postfix |
| `3 + 4` | `3 4 +` |
| `3 + 4 * 2` | `3 4 2 * +` |
| `( 3 + 4 ) * 2` | `3 4 + 2 *` |

### Evaluating postfix with a stack

Read left to right. A **number** is pushed. An **operator** pops two operands, applies itself and pushes the result. The left operand was pushed first, so it is popped **second**, and the order matters for `-` and `/`.

```python
def evaluate_rpn(expression):
    stack = []
    for token in expression.split():
        if token in ("+", "-", "*", "/"):
            right = stack.pop()
            left = stack.pop()
            if token == "+":
                stack.append(left + right)
            elif token == "-":
                stack.append(left - right)
            elif token == "*":
                stack.append(left * right)
            else:
                stack.append(left / right)
        else:
            stack.append(float(token))
    return stack.pop()

print(evaluate_rpn("3 4 + 2 *"))              # 14.0
print(evaluate_rpn("5 1 2 + 4 * + 3 -"))      # 14.0
```

Tracing `3 4 + 2 *`:

| Token | Action | Stack, top on the right |
| `3` | push | 3 |
| `4` | push | 3 4 |
| `+` | pop 4, pop 3, push 7 | 7 |
| `2` | push | 7 2 |
| `*` | pop 2, pop 7, push 14 | 14 |

### Converting infix to postfix: the shunting yard

Dijkstra's **shunting yard** algorithm uses a stack of **operators**. Numbers go straight to the output. An operator waits on the stack, but first any operator already there with **equal or higher precedence** is moved to the output, because it must be done first. A bracket is a barrier.

```python
def to_postfix(expression):
    precedence = {"+": 1, "-": 1, "*": 2, "/": 2}
    output = []
    operators = []
    for token in expression.split():
        if token in precedence:
            while (operators and operators[-1] in precedence
                   and precedence[operators[-1]] >= precedence[token]):
                output.append(operators.pop())
            operators.append(token)
        elif token == "(":
            operators.append(token)
        elif token == ")":
            while operators[-1] != "(":
                output.append(operators.pop())
            operators.pop()
        else:
            output.append(token)
    while operators:
        output.append(operators.pop())
    return " ".join(output)

print(to_postfix("3 + 4 * 2"))            # 3 4 2 * +
print(to_postfix("( 3 + 4 ) * 2"))        # 3 4 + 2 *
print(to_postfix("5 + 1 * 2 - 3"))        # 5 1 2 * + 3 -
```

!exam Show the stack at every step :: A trace question gives one mark per correct stack state. Write the contents after each token, mark the top, and for postfix evaluation say which operand was popped first. For subtraction and division, getting that the wrong way round is the most common slip.
"""),
    ],
    keyterms=[
        ("Stack", "A last in first out data structure in which items are added and removed at one end, the top."),
        ("Queue", "A first in first out data structure in which items are added at the rear and removed from the front."),
        ("Push", "The operation that adds an item to the top of a stack."),
        ("Pop", "The operation that removes and returns the item at the top of a stack."),
        ("Stack overflow", "An error caused by pushing an item onto a stack that is already full."),
        ("Stack underflow", "An error caused by popping from a stack that is empty."),
        ("Pointer", "A variable that holds the position of an item, such as the top of a stack or the front of a queue."),
        ("Circular queue", "A queue held in a fixed array in which the pointers wrap round to the start, so freed places are reused."),
        ("Priority queue", "A queue in which the item removed is the one with the highest priority, not the one that arrived first."),
        ("Reverse Polish notation", "A notation in which each operator follows its operands, so no brackets or precedence rules are needed."),
    ],
    grade="""
Stack and queue questions are procedural: marks are for exact pointer behaviour and for knowing which error is which.

+ State LIFO or FIFO, and match each to its structure, its operations and its typical use
+ Give the pointer value before and after every operation when you trace one
+ Name stack overflow for a push when full and underflow for a pop when empty, and say what check prevents each
+ In a circular queue, write the wrap round as (pointer + 1) MOD size, and explain why it is used
+ Pop the right operand first when evaluating postfix, so that subtraction and division are not reversed
""",
    mistakes=[
        "Mixing up LIFO and FIFO, or describing a queue as removing from the rear.",
        "Moving the pointer before checking whether the stack is full or empty.",
        "Forgetting that a circular queue wraps with MOD, so the pointer runs off the end of the array.",
        "Evaluating postfix subtraction as right minus left.",
        "Saying a popped value is deleted from the array, when only the pointer moves.",
    ],
    quiz=[
        Q("Which description matches a stack?",
          ["The last item added is the first removed", "The first item added is the first removed",
           "Items are removed in alphabetical order", "Items can be removed from either end"], 0,
          "That is LIFO, last in first out, like a pile of plates."),
        Q("Which description matches a queue?",
          ["The first item added is the first removed", "The last item added is the first removed",
           "Only the highest value is removed first", "Items are removed at random"], 0,
          "That is FIFO, first in first out, like people waiting."),
        Q("What error occurs when you pop from an empty stack?",
          ["Stack underflow", "Stack overflow", "Queue overflow", "Index overflow"], 0,
          "Underflow is removing from an empty structure. Overflow is adding to a full one."),
        Q("A stack is empty. `push(1)`, `push(2)`, `push(3)`, `pop()` are performed. What is now on top?",
          ["2", "3", "1", "The stack is empty"], 0,
          "3 was on top and was removed by pop, so 2 is the top of what is left."),
        Q("Why is a circular queue better than a linear queue in a fixed size array?",
          ["Places freed at the front can be reused without shifting items",
           "It can hold an unlimited number of items", "It does not need a front pointer",
           "It sorts the items as they are added"], 0,
          "When a pointer reaches the end of the array it wraps to the start, so freed places are reused."),
        Q("A circular queue has 6 places and the rear pointer is at position 5. Where is the next item added?",
          ["Position 0", "Position 6", "Position 4", "Position 5"], 0,
          "(5 + 1) MOD 6 is 0, so the pointer wraps round to the start of the array."),
        Q("Which data structure is best for implementing an undo feature?",
          ["A stack", "A queue", "A priority queue", "A circular queue"], 0,
          "The most recent action is the first to be undone, which is last in first out."),
        Q("Which data structure is best for holding print jobs in the order they were sent?",
          ["A queue", "A stack", "A binary tree", "A hash table"], 0,
          "Jobs are printed in the order they arrive, which is first in first out."),
        Q("How does a priority queue differ from an ordinary queue?",
          ["The item removed is the one with the highest priority, not the one that arrived first",
           "Items can only be added at the front and are only ever removed from the rear",
           "It has no maximum size, so it can never become full or cause an overflow",
           "It removes the item that arrived last, so it behaves in the same way as a stack"], 0,
          "Arrival order matters only between items of equal priority."),
        Q("What is the postfix form of the infix expression `3 + 4 * 2`?",
          ["`3 4 2 * +`", "`3 4 + 2 *`", "`+ 3 * 4 2`", "`3 + 4 2 *`"], 0,
          "The multiplication happens first, so 4 2 * comes before the +."),
    ],
    exam=[
        EQ("Describe two differences between a stack and a queue.", 4, [
            MP("A stack is last in first out", ["lifo", "last in first out", "last in, first out"]),
            MP("A queue is first in first out", ["fifo", "first in first out", "first in, first out"]),
            MP("Items are added and removed at the same end of a stack, but at opposite ends of a queue", ["same end", "one end", "opposite", "different end", "top", "front and rear", "rear"]),
            MP("An example use of each, such as undo for a stack and a print queue for a queue", ["undo", "call stack", "back button", "print", "scheduling", "buffer", "example"]),
        ], "A stack is last in first out, so the item removed is the one most recently added, whereas a queue is first in first out, so the item removed is the one that has been waiting longest. Items are added to and removed from the same end of a stack, the top, but a queue adds at the rear and removes from the front. A stack is used for undo or the call stack, and a queue for print jobs or process scheduling.",
           command="Describe"),
        EQ("An empty stack has the following operations performed on it, in order: push(4), push(7), pop(), push(2), push(9), pop(), pop(). State the values returned by each of the three pop operations, and the contents of the stack at the end.", 4, [
            MP("The first pop returns 7", ["7"]),
            MP("The second pop returns 9", ["9"]),
            MP("The third pop returns 2", ["2"]),
            MP("The stack contains only 4 at the end", ["4", "only 4", "just 4", "[4]"]),
        ], "After push(4) and push(7) the stack is 4, 7 with 7 on top, so the first pop returns 7. push(2) and push(9) give 4, 2, 9, so the second pop returns 9 and the third returns 2. The stack then contains only 4.",
           command="State"),
        EQ("A stack is implemented as an array called items, with a pointer called top that is -1 when the stack is empty. The array has a fixed size of 10. Write the subprograms push and pop, including checks for overflow and underflow.", 6, [
            MP("push checks whether the stack is full, when top is 9", ["full", "top == 9", "len(items) - 1", "overflow", "== 9"]),
            MP("push reports an error or returns False if it is full", ["error", "false", "raise", "message", "overflow"]),
            MP("push increases top by 1 and stores the item at items[top]", ["top += 1", "top + 1", "items[top] = ", "increment"]),
            MP("pop checks whether the stack is empty, when top is -1", ["empty", "top == -1", "underflow", "== -1"]),
            MP("pop reads the item at items[top] before changing the pointer", ["items[top]", "item = ", "read", "return"]),
            MP("pop reduces top by 1 and returns the item", ["top -= 1", "top - 1", "decrement", "return item"]),
        ], r"""```python
items = [None] * 10
top = -1

def push(item):
    global top
    if top == 9:
        return False
    top = top + 1
    items[top] = item
    return True

def pop():
    global top
    if top == -1:
        return None
    item = items[top]
    top = top - 1
    return item

push(5)
push(8)
print(pop(), pop(), pop())
```

push first checks whether the pointer is at the last position, and returns False to report the overflow if so. Otherwise it moves the pointer up and stores the item there. pop checks for an empty stack and reports underflow by returning None, otherwise it reads the item at the pointer, moves the pointer down and returns the item. The calls shown print 8 5 None.""",
           command="Write"),
        EQ("A circular queue is held in an array of size 5. The front pointer is 3 and the queue contains 3 items. State the position of the rear pointer, and the position at which the next item will be added. Explain how the remainder operator is used when a pointer is moved.", 4, [
            MP("The rear is at position 0", ["0", "zero", "position 0"]),
            MP("The next item will be added at position 1", ["1", "position 1", "one"]),
            MP("The pointer is increased by 1 and the remainder after division by the size of the array is taken", ["divided by 5", "mod 5", "% 5", "remainder", "size of the array", "divide"]),
            MP("So when the pointer passes the last position it wraps round to 0", ["wraps", "back to 0", "start of the array", "back to the start", "round to"]),
        ], "The items are at positions 3, 4 and 0, so the rear pointer is at position 0, and the next item is added at position (0 + 1) MOD 5, which is 1. When a pointer is moved, 1 is added and the remainder after dividing by the size of the array is taken. Since the remainder can never be 5 or more, a pointer that passes the last position wraps round to position 0 at the start of the array.",
           command="State"),
        EQ("The postfix expression 6 2 3 + * is evaluated using a stack. Show the contents of the stack after each token and state the result.", 4, [
            MP("6 is pushed, then 2, then 3, giving 6 2 3", ["6 2 3", "6, 2, 3", "pushed"]),
            MP("+ pops 3 and 2 and pushes 5, leaving 6 5", ["6 5", "6, 5", "5", "pops 3 and 2"]),
            MP("* pops 5 and 6 and pushes 30", ["30", "pops 5 and 6"]),
            MP("The result is 30", ["result is 30", "30"]),
        ], "Each number is pushed, so after 6, 2 and 3 the stack holds 6, 2, 3 with 3 on top. The + pops 3 and 2 and pushes their sum, 5, leaving 6, 5. The * pops 5 and 6 and pushes their product, 30. The stack holds only 30, which is the result.",
           command="Show"),
    ],
)
