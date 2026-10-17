"""Advanced Python: simulation, modelling, random numbers and cellular automata."""
from mskbuild.models import Topic, Section, Q, EQ, MP

INPUTS = {}
EXPECT = {}

TOPIC = Topic(
    slug="simulation-and-modelling",
    title="Simulation and Modelling",
    spec="Advanced 8",
    icon="i-chart",
    minutes=70,
    blurb="Use a computer to ask what would happen if. Build a random number generator, estimate pi and a probability by Monte Carlo sampling, model a spreading disease and the chaos in a population, grow patterns with Conway's Game of Life, and simulate a shop queue, then check the model against the theory.",
    fact="The Monte Carlo method was invented in the 1940s by the mathematician Stanislaw Ulam, who was recovering from an illness and playing solitaire. He wondered how to work out the chance of winning, and realised that it would be far quicker to play a hundred games and count. The method was named after the casino in Monaco.",
    sections=[
        Section("Models, simulation and random numbers", r"""
A **model** is a simplified version of something real, an abstraction that keeps what matters and drops what does not. A **simulation** runs the model forward in time to see what happens. Simulations are used when trying it for real would be:

- **dangerous**: a nuclear reactor, a plane that loses an engine
- **expensive**: crash tests, wind tunnels, a new factory layout
- **too slow**: the climate over a hundred years
- **impossible**: two galaxies colliding
- **unethical**: testing a harmful dose on people

| Advantages | Disadvantages |
| safe, cheap and repeatable | only as good as the model: an assumption left out can invalidate the result |
| can be run faster or slower than real time | needs data to build and check it |
| any number of "what if" experiments | can give a false sense of certainty |
| can show the effect of one change at a time | may need a lot of computing power |

### Random numbers that are not random

Many simulations need chance: when a customer arrives, whether a virus spreads. A computer is deterministic, so it uses a **pseudo-random number generator**: a formula whose output *looks* random. A simple one is the **linear congruential generator**. Each number is made from the last by multiplying, adding and taking a remainder:

```python
class LCG:
    def __init__(self, seed):
        self.state = seed

    def next(self):
        self.state = (1103515245 * self.state + 12345) % 2 ** 31
        return self.state / 2 ** 31              # a number from 0 up to, but not including, 1

rng = LCG(42)
print([round(rng.next(), 3) for _ in range(5)])

rng = LCG(42)                                    # the same seed
print([round(rng.next(), 3) for _ in range(5)])

rng = LCG(43)                                    # a different seed
print([round(rng.next(), 3) for _ in range(5)])

counts = [0] * 10
rng = LCG(7)
for _ in range(10000):
    counts[int(rng.next() * 10)] += 1
print(counts)
```

The same **seed** gives exactly the same sequence, which is why a simulation can be repeated and a bug reproduced. The last line is a quick check of quality: ten thousand numbers sorted into ten equal bins give about a thousand in each, so the numbers are spread **uniformly**. This simple generator is fine for learning but weak for serious use. Python's own `random` module uses the Mersenne Twister, a far better one, and `random.Random(seed)` makes a generator you can seed.

!key Seeds make science repeatable :: When you report a simulation's results, say the seed. Anyone who runs the same code with the same seed must get the same numbers, which lets them check your work. For security, the opposite is needed: use the `secrets` module, whose numbers cannot be predicted.
"""),
        Section("Monte Carlo: answering questions by sampling", r"""
A **Monte Carlo** method finds an answer by running a random experiment many times and averaging. It suits questions where the exact mathematics is hard.

### Estimating pi

Throw darts at random at a square that has a quarter circle of radius 1 drawn inside it. The area of the quarter circle is pi / 4 and the area of the square is 1, so the fraction of darts landing **inside** the circle should be about pi / 4:

```python
import math
import random

rng = random.Random(2024)

def estimate_pi(darts):
    inside = 0
    for _ in range(darts):
        x, y = rng.random(), rng.random()
        if x * x + y * y <= 1:                  # inside the quarter circle
            inside += 1
    return 4 * inside / darts

for darts in (100, 1000, 10000, 100000):
    estimate = estimate_pi(darts)
    print(str(darts).rjust(6), round(estimate, 4), "error", round(abs(estimate - math.pi), 4))
```

More darts give a better answer, but slowly: to make the error ten times smaller you need about a hundred times as many. The error shrinks with the square root of the number of samples.

### Estimating a probability

How likely is it that in a class of 23 people, two share a birthday? Most people guess it is small. Simulate many classes and count:

```python
import random

def shared_birthday(people, trials, seed):
    rng = random.Random(seed)
    hits = 0
    for _ in range(trials):
        birthdays = [rng.randrange(365) for _ in range(people)]
        if len(set(birthdays)) < people:         # a repeat means fewer different days
            hits += 1
    return hits / trials

exact = 1.0
for i in range(23):
    exact *= (365 - i) / 365                     # the chance that everyone is different

print("simulated:", shared_birthday(23, 3000, 1))
print("exact:    ", round(1 - exact, 4))

rng = random.Random(9)
sevens = sum(1 for _ in range(12000) if rng.randint(1, 6) + rng.randint(1, 6) == 7)
print("two dice add up to 7:", round(sevens / 12000, 4), "against 1/6 =", round(1 / 6, 4))
```

The simulation agrees with the exact answer, about 51%, to within about a percentage point, and it did not need any mathematics at all. This is the strength of the method. When the exact answer cannot be worked out, such as the chance that a complex system fails, sampling still works.

!warn One run is not an answer :: A single simulation is a single random sample. Run it many times, with different seeds, and report the average and how much the results vary.
"""),
        Section("Random walks, growth and spreading models", r"""
### A random walk

A drunk person takes steps left or right at random. How far from the start will they be after n steps? Not n, as the steps cancel out each other. Not zero either. Simulate hundreds of walks and average the distance:

```python
import math
import random

rng = random.Random(7)

def walk(steps):
    position = 0
    for _ in range(steps):
        position += 1 if rng.random() < 0.5 else -1        # one step left or right
    return position

print("steps   average distance   prediction")
for steps in (100, 400, 1600):
    average = sum(abs(walk(steps)) for _ in range(200)) / 200
    print(str(steps).ljust(7), str(round(average, 1)).ljust(18), round(math.sqrt(2 * steps / math.pi), 1))
```

The distance grows with the **square root** of the number of steps: sixteen times as many steps takes you only four times as far. This pattern describes the diffusion of smells and heat, and the movement of share prices.

### Population growth and chaos

A population where each generation depends on the last can be modelled by the **logistic map**: `x = r * x * (1 - x)`. The number x is the population as a fraction of the most the environment could support, and r is the growth rate. Run it for different values of r and look at where it settles:

```python
for r in (2.8, 3.5, 3.9):
    x = 0.5
    last = []
    for generation in range(200):
        x = r * x * (1 - x)
        if generation >= 194:
            last.append(round(x, 3))
    print("r =", r, last)
```

With r = 2.8 the population settles to a single value. At 3.5 it cycles round four values. At 3.9 it never settles at all: this is **chaos**. There is no randomness in the formula, yet the result is unpredictable in practice, because a tiny difference in the starting value grows until it dominates. That is why the weather cannot be forecast for more than a week or two, however good the model.

### A model of an epidemic

The **SIR model** splits a population into the **S**usceptible, the **I**nfected and the **R**ecovered. Each day, some susceptible people meet an infected one and catch it, and some of the infected recover:

- new infections each day = `beta * S * I / population`
- recoveries each day = `gamma * I`

```python
def sir(beta, gamma, days, population=1000, infected=1):
    s, i, r = population - infected, infected, 0
    history = []
    for day in range(days + 1):
        history.append((day, s, i, r))
        new_infections = beta * s * i / population
        recoveries = gamma * i
        s -= new_infections
        i += new_infections - recoveries
        r += recoveries
    return history

for beta in (0.5, 0.35, 0.25):
    history = sir(beta, 0.2, 200)
    peak = max(history, key=lambda row: row[2])
    total = round(1000 - history[-1][1])
    print("spread rate", beta, ": peak on day", peak[0], "with", round(peak[2]), "ill at once;", total, "caught it in all")

print()
for day, s, i, r in sir(0.5, 0.2, 60)[::5]:
    print(str(day).rjust(2), "#" * round(i / 10))
```

Reducing the spread rate (`beta`), by washing hands, wearing masks or staying at home, makes the peak **lower** and **later**. That is "flattening the curve", and it matters because the number ill at once is what overwhelms hospitals. The model also has a famous number, `beta / gamma`, the **basic reproduction number**. When it is below 1 the infection dies out.

The model is a big simplification. It assumes everyone mixes equally, and that recovered people are immune. Real models add age groups, places and vaccination, and they are checked against real data.
"""),
        Section("Cellular automata: the Game of Life", r"""
A **cellular automaton** is a grid of cells. Each cell is on or off, and at every tick all the cells update at once, using a simple rule that looks only at the cell's neighbours. In 1970 the mathematician John Conway invented the best known: the **Game of Life**.

On an endless grid, every cell has eight neighbours. At each generation:

1. A live cell with **2 or 3** live neighbours **survives**. Otherwise it dies, of loneliness or overcrowding.
2. A dead cell with **exactly 3** live neighbours is **born**.

That is the whole game. The program keeps only the set of live cells, so the grid has no edge, and counts the neighbours of every cell next to a live one:

```python
from collections import Counter

def step(live):
    neighbours = Counter((x + dx, y + dy)
                         for x, y in live
                         for dx in (-1, 0, 1)
                         for dy in (-1, 0, 1)
                         if (dx, dy) != (0, 0))
    return {cell for cell, count in neighbours.items() if count == 3 or (count == 2 and cell in live)}

def show(live, size=6):
    for y in range(size):
        print("".join("#" if (x, y) in live else "." for x in range(size)))

glider = {(1, 0), (2, 1), (0, 2), (1, 2), (2, 2)}
for generation in range(5):
    print("generation", generation, "| alive:", len(glider))
    show(glider)
    glider = step(glider)

blinker = {(1, 2), (2, 2), (3, 2)}
print("a blinker repeats after 2 steps:", step(step(blinker)) == blinker, "| after 1:", step(blinker) == blinker)
```

Watch the **glider**. It has five cells and keeps the same shape, but moves one square diagonally every four generations. Nothing in the rules mentions movement. It **emerges** from the rules. Patterns come in families: **still lifes** that never change, **oscillators** like the blinker that repeat, and **spaceships** like the glider that travel. Life is **Turing complete**: with the right patterns it can compute anything a computer can, and people have built working processors inside it.

### One dimensional automata

The simplest automaton is a single row. Each cell's next value depends on itself and its two neighbours, so there are eight possible neighbourhoods, and a rule is a choice of the result for each. That is eight bits, so there are 256 rules, numbered 0 to 255 by the binary number they make. Print each generation under the one before:

```python
def rule(number, width=31, steps=12):
    table = {(a, b, c): (number >> (a * 4 + b * 2 + c)) & 1 for a in (0, 1) for b in (0, 1) for c in (0, 1)}
    cells = [0] * width
    cells[width // 2] = 1
    for _ in range(steps):
        print("".join("#" if cell else "." for cell in cells))
        cells = [table[(cells[i - 1], cells[i], cells[(i + 1) % width])] for i in range(width)]

print("rule 90")
rule(90)
print("rule 30")
rule(30)
```

Rule 90 draws a neat, regular triangle (the Sierpinski triangle). Rule 30, with an equally simple rule, produces a pattern so irregular that its centre column was used as a random number generator. Complicated behaviour does not need complicated rules.
"""),
        Section("Queues, and testing a model", r"""
A supermarket wants to know how many checkouts to open. Customers arrive at random, each takes a random time to serve, and if all the tills are busy they wait. Too few tills and the queues are huge. Too many and staff stand idle. A simulation can try each choice.

The simulation does not step through every second. It jumps from **event to event**, the arrival of a customer and the time a till becomes free. This is a **discrete event simulation**. The program keeps a **heap** of the times at which each till will be free, the data structure from the heaps topic, so the next free till is always at the front.

```python
import heapq
import random

def simulate(tills, customers, seed, mean_gap, mean_service):
    rng = random.Random(seed)
    free_at = [0.0] * tills                       # when each till next becomes free
    clock = 0.0
    waits = []
    for _ in range(customers):
        clock += rng.expovariate(1 / mean_gap)    # the next customer arrives
        soonest = heapq.heappop(free_at)          # the till that frees up first
        start = max(clock, soonest)
        waits.append(start - clock)
        heapq.heappush(free_at, start + rng.expovariate(1 / mean_service))
    return sum(waits) / len(waits), max(waits)

# a customer arrives every 1 minute on average, and each takes 1.5 minutes to serve
for tills in (1, 2, 3):
    average, worst = simulate(tills, 2000, 3, 1.0, 1.5)
    print(tills, "till(s): average wait", round(average, 2), "minutes, worst", round(worst, 1))
```

One till cannot cope, since customers arrive faster than they can be served, so the queue grows without limit: an average wait of **hundreds of minutes**. Two tills cope but with a short wait. A third makes the wait almost vanish. Notice how **non-linear** this is: the step from one till to two changes everything, and the step from two to three still matters. Intuition about queues is often wrong, which is exactly why we simulate them.

The arrival and service times were drawn from an **exponential distribution** (`expovariate`), which is the standard model of "events happening at random at a steady average rate".

### Is the model any good?

Two separate questions must be asked:

- **Verification**: *did we build the model right?* Does the code do what we meant, and is it free of bugs?
- **Validation**: *did we build the right model?* Does it behave like the real thing?

One way to **verify** is to test it on a case where the exact answer is known. For a single till, with customers arriving every minute on average and service taking half a minute, queueing theory says the average wait should be 0.5 minutes:

```python
import heapq
import random

def average_wait(tills, customers, seed, mean_gap, mean_service):
    rng = random.Random(seed)
    free_at = [0.0] * tills
    clock = 0.0
    total = 0.0
    for _ in range(customers):
        clock += rng.expovariate(1 / mean_gap)
        soonest = heapq.heappop(free_at)
        start = max(clock, soonest)
        total += start - clock
        heapq.heappush(free_at, start + rng.expovariate(1 / mean_service))
    return total / customers

print("simulated:", round(average_wait(1, 50000, 3, 1.0, 0.5), 3), "| theory: 0.5")

print("two tills, five different seeds:")
for seed in range(1, 6):
    print("  seed", seed, round(average_wait(2, 2000, seed, 1.0, 1.5), 2))
```

The simulated 0.508 is very close to the theory's 0.5, which is evidence the code is right. **Validation** would compare the average waits with times measured in the real shop, and change the model if they disagree.

The five seeds give different answers, between about 1.4 and 1.8 minutes. Each is a legitimate sample, which shows why you need many runs.

### The limits of any model

- **Garbage in, garbage out.** If the arrival rate is guessed wrongly, the answer is wrong, however good the code.
- **Assumptions.** This model assumes customers arrive at a steady rate. A real shop has a lunchtime rush.
- **Sensitivity.** Change an input a little, such as the service time, and see how much the answer moves. If a small change gives a large one, the conclusion is fragile. This is **sensitivity analysis**.
- **A model answers the question you asked.** It cannot tell you about things you left out, such as the cost of an extra till.

!exam Verify or validate? :: A question about checking a model wants the two terms kept apart. Verification compares the program with the specification of the model, for example against a known answer. Validation compares the model with the real world, for example against measured data.
"""),
    ],
    keyterms=[
        ("Model", "A simplified representation of a real system that includes what matters and leaves out the rest."),
        ("Simulation", "Running a model over time on a computer to see how the system behaves."),
        ("Pseudo-random number generator", "An algorithm that produces a sequence of numbers that appear random but are determined by a starting seed."),
        ("Seed", "The starting value of a pseudo-random number generator. The same seed always gives the same sequence."),
        ("Monte Carlo method", "Estimating an answer by running many random trials and averaging the results."),
        ("Chaos", "Behaviour that follows exact rules but is unpredictable in practice, because tiny differences in the start grow rapidly."),
        ("Cellular automaton", "A grid of cells that all update at once according to a rule based on their neighbours."),
        ("Emergence", "Complex behaviour appearing from the interaction of simple rules, although none of the rules describe it."),
        ("Discrete event simulation", "A simulation that moves from one event to the next, rather than advancing time in equal steps."),
        ("Verification", "Checking that the program correctly implements the model: building the model right."),
        ("Validation", "Checking that the model matches the real system: building the right model."),
        ("Sensitivity analysis", "Changing the inputs of a model by small amounts to see how much the results change."),
    ],
    grade="""
Simulation questions want a reason why, and a limitation.

+ Give a reason for simulating: too dangerous, too expensive, too slow, impossible or unethical to try for real
+ Say that pseudo-random numbers come from a formula and the same seed gives the same sequence
+ For Monte Carlo, say many random trials are averaged, and more trials give a better answer
+ Keep verification (is the program right?) and validation (does the model match reality?) separate
+ Name a limitation: an assumption, the quality of the input data, or the need for repeated runs
""",
    mistakes=[
        "Saying a pseudo-random number generator is truly random. It is a formula, and repeats if the seed repeats.",
        "Treating the result of one run of a random simulation as the answer, instead of averaging many.",
        "Confusing verification with validation.",
        "Assuming a simulation is accurate because it is detailed. It is only as good as its assumptions and data.",
        "Forgetting to say what was left out of the model, and why it was safe to leave out.",
    ],
    quiz=[
        Q("Why are pseudo-random number generators used in simulations, rather than truly random numbers?",
          ["They can be repeated by using the same seed, so results can be checked", "They are more random", "They are cheaper to calculate", "They use less memory"], 0,
          "Repeatability makes it possible to reproduce a result and to find a bug."),
        Q("Which of these is a good reason to use a simulation?",
          ["The real experiment would be too dangerous or expensive", "The real system is already working perfectly", "The model has not been made yet", "The computer is faster than the real system"], 0,
          "Crash tests, nuclear reactors and the climate are all examples."),
        Q("What does a Monte Carlo method do?",
          ["Estimates an answer by averaging many random trials", "Finds the exact answer by algebra", "Sorts data into order", "Generates a password"], 0,
          "It is useful when the exact mathematics is too hard."),
        Q("In the Monte Carlo estimate of pi, what happens to the estimate as more darts are thrown?",
          ["It generally becomes more accurate, though slowly", "It always becomes exactly pi", "It gets worse", "It stays the same"], 0,
          "The error shrinks roughly with the square root of the number of darts."),
        Q("What is the 'glider' in the Game of Life?",
          ["A pattern that moves across the grid, although the rules never mention movement", "A cell with no neighbours", "A rule for births", "A pattern that never changes"], 0,
          "It is an example of emergence: behaviour that arises from simple rules."),
        Q("What is emergence?",
          ["Complex behaviour arising from simple rules that do not describe it", "A bug in a program", "The start of a simulation", "A kind of random number"], 0,
          "The movement of a glider, or the shape of a Sierpinski triangle, is not in the rules."),
        Q("What is a discrete event simulation?",
          ["One that jumps from event to event instead of moving time in fixed steps", "One with only two outcomes", "One that uses a continuous random number", "One that cannot be repeated"], 0,
          "Queue simulations jump to the next arrival or the next time a till becomes free."),
        Q("What is the difference between verification and validation of a model?",
          ["Verification checks the program matches the model; validation checks the model matches reality", "They mean the same", "Verification checks the model matches reality; validation checks the code", "Verification is done by users, validation by programmers"], 0,
          "Building the model right, and building the right model."),
        Q("The results of a simulation change a lot when one input is changed slightly. What does this show?",
          ["The results are sensitive to that input, so it needs to be estimated carefully", "The simulation has a bug", "The simulation is accurate", "The random numbers are not random"], 0,
          "This is what sensitivity analysis looks for."),
        Q("Why should a random simulation be run many times?",
          ["One run is only one random sample, so results vary", "The computer needs to warm up", "To use up the random numbers", "To make the model valid"], 0,
          "Averaging many runs, and seeing the spread, gives a reliable answer."),
    ],
    exam=[
        EQ("Explain two reasons why a company might use a computer simulation to test a new design instead of building and testing the real thing.", 4, [
            MP("It is cheaper, because there is no need to build physical prototypes", ["cheaper", "cost", "expensive", "prototype", "save money"]),
            MP("It is safer, because dangerous situations can be tested without any risk to people", ["safe", "danger", "risk", "harm", "injury"]),
            MP("It is faster, as results can be produced quickly, and many different designs can be tried", ["faster", "quick", "time", "many designs", "different designs", "speed"]),
            MP("Tests can be repeated exactly, and conditions that are hard to create in real life can be modelled", ["repeat", "exactly", "conditions", "hard to create", "impossible", "controlled"]),
        ], "A simulation is cheaper, because it avoids the cost of building physical prototypes which may be destroyed in testing. It is also safer, because dangerous situations, such as a crash, can be tested without any risk to people. A simulation can also be faster, as many different designs can be tried in a short time, and the tests can be repeated exactly or under conditions that would be difficult or impossible to create in real life.",
           command="Explain"),
        EQ("Explain what is meant by a pseudo-random number generator, and why using the same seed twice gives the same sequence of numbers.", 3, [
            MP("It uses a formula (algorithm) to produce a sequence of numbers that appear random", ["formula", "algorithm", "appear random", "looks random", "calculation"]),
            MP("Each number is calculated from the previous number (the state), starting from the seed", ["previous", "starting", "seed", "state", "starting value"]),
            MP("So the whole sequence is determined by the seed, and the same seed gives the same sequence", ["determined", "same seed", "same sequence", "same numbers", "repeat"]),
        ], "A pseudo-random number generator uses a formula to produce a sequence of numbers that appear to be random. Each number is calculated from the previous one, starting from a value called the seed. Because the whole sequence is completely determined by the formula and the seed, using the same seed twice gives exactly the same sequence of numbers.",
           command="Explain"),
        EQ("Describe how a Monte Carlo simulation could be used to estimate the probability of rolling a double six when two dice are thrown.", 4, [
            MP("Simulate the throw of two dice by generating two random numbers between 1 and 6", ["random number", "1 and 6", "two dice", "simulate", "generate"]),
            MP("Check whether both numbers are 6, and count how many times this happens", ["both", "six", "count", "check"]),
            MP("Repeat for a very large number of throws", ["repeat", "many", "large number", "thousands", "loop"]),
            MP("The probability is estimated as the number of double sixes divided by the total number of throws", ["divided", "divide", "proportion", "fraction", "total number of throws"]),
        ], "The program would simulate throwing two dice by generating two random whole numbers between 1 and 6. It would check whether both were 6, and add one to a count if they were. This would be repeated for a very large number of throws, such as a hundred thousand. The probability is estimated as the number of double sixes divided by the total number of throws, which should be close to 1/36 and gets closer the more throws are used.",
           command="Describe"),
        EQ("Explain the difference between verification and validation of a simulation model.", 4, [
            MP("Verification checks that the program correctly implements the model, with no errors", ["program", "correctly", "no errors", "implement", "bugs", "code"]),
            MP("For example by testing it with an input for which the correct answer is known", ["known answer", "known", "test", "example", "theory"]),
            MP("Validation checks that the model is a good representation of the real system", ["real system", "represents", "real world", "reality", "good representation"]),
            MP("For example by comparing its results with measurements taken from the real system", ["compar", "measurements", "real data", "results", "real life"]),
        ], "Verification checks that the program correctly implements the model and that it has no errors, for example by testing it with an input for which the correct answer is already known. Validation checks that the model is a good representation of the real system, for example by comparing the results of the simulation with measurements taken from the real system.",
           command="Explain"),
        EQ("A supermarket uses a simulation to decide how many checkouts to open. Discuss the benefits and limitations of using the simulation to make the decision.", 6, [
            MP("Different numbers of checkouts can be tried quickly, with no disruption to real customers", ["different numbers", "quickly", "no disruption", "try", "what if", "without"]),
            MP("The simulation can show the average and longest waiting times for each choice, helping to balance customer waiting against staff costs", ["waiting", "average", "longest", "cost", "balance", "staff"]),
            MP("It can be run many times with different random numbers to see how much the results vary", ["many times", "vary", "random", "different seeds", "repeated"]),
            MP("The model is only as good as the data and assumptions, such as the rate at which customers arrive and the time each takes to serve", ["data", "assumption", "arrival", "only as good", "rate", "garbage"]),
            MP("It may leave out real factors, such as rush hours, customers choosing the shortest queue, or staff breaks", ["rush", "leave out", "shortest queue", "breaks", "real factors", "simplif"]),
            MP("A reasoned conclusion: useful to guide the decision provided it is validated against real data, but not the only thing to rely on", ["conclusion", "validated", "guide", "overall", "therefore", "alongside", "i would"]),
        ], "The supermarket can try different numbers of checkouts quickly and without disrupting real customers. The simulation can show the average and longest waiting times for each choice, which helps the managers to balance the time customers spend waiting against the cost of staff. It can be run many times with different random numbers to show how much the results vary. However, the model is only as good as the data and the assumptions it is built on, such as how often customers arrive and how long each one takes to serve, and it may leave out real factors such as lunchtime rushes, customers choosing the shortest queue, or staff breaks. The simulation is therefore useful in guiding the decision, provided that it has been validated against measurements from the real shop, but it should not be the only thing the managers rely on.",
           command="Discuss"),
    ],
)
