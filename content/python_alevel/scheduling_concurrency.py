"""A Level Python: scheduling, concurrency, race conditions and deadlock."""
from mskbuild.models import Topic, Section, Q, EQ, MP

INPUTS = {}
EXPECT = {}

TOPIC = Topic(
    slug="scheduling-and-concurrency",
    title="Scheduling, Concurrency and Deadlock",
    spec="A Level 18",
    icon="i-timer",
    minutes=65,
    blurb="How an operating system shares one processor between many programs, and what goes wrong when they share data. Simulate first come first served, shortest job first, shortest remaining time, round robin and multi-level queues, then reproduce a race condition and a deadlock deterministically, and finish with real threads and processes.",
    fact="The first computer to be taken down by a race condition may be the Therac-25, a radiation therapy machine in the 1980s. An operator who typed quickly could change the settings after the software had checked them but before it had acted, and several patients were given doses far larger than intended.",
    sections=[
        Section("Sharing one processor: scheduling", r"""
A processor can run only one thing at a time per core, yet a computer seems to run dozens of programs at once. The operating system's **scheduler** makes that happen. A running program is a **process**. The scheduler keeps the processes that are ready in a **ready queue**, picks one, lets it run for a while, and then picks another. Switching between them is a **context switch**: the state of the old process (its registers and program counter) is saved, and the state of the new one is loaded.

A scheduling algorithm tries to balance several goals, and they pull in different directions:

- **throughput**: finish as many processes as possible
- **fairness**: give every process a share, and let none starve
- **response time**: how soon a process starts running after it is ready
- **turnaround time**: from arrival to completion
- **waiting time**: the time spent in the ready queue, which is *turnaround time minus the time actually running*

A scheduler is **pre-emptive** if it can take the processor away from a running process. A **non-pre-emptive** one lets a process run until it finishes or waits.

### Four algorithms

Take four processes, each with an **arrival time** and a **burst time** (how long it needs the processor):

| Process | Arrives | Burst |
| A | 0 | 8 |
| B | 1 | 4 |
| C | 2 | 9 |
| D | 3 | 5 |

- **First come first served (FCFS).** Run them in order of arrival. Simple and fair in its way, but one long job at the front delays every short one behind it (the *convoy effect*).
- **Shortest job first (SJF).** When the processor is free, run the waiting process with the smallest burst. It gives the best average waiting time for a non-pre-emptive scheduler, but needs to know how long each job will take, and long jobs may be starved.
- **Shortest remaining time (SRT).** A pre-emptive SJF: whenever a process arrives that needs less time than the one running has left, switch to it.

```python
procs = [("A", 0, 8), ("B", 1, 4), ("C", 2, 9), ("D", 3, 5)]      # name, arrival, burst

def fcfs(procs):
    t, timeline = 0, []
    for name, arrival, burst in sorted(procs, key=lambda p: p[1]):
        while t < arrival:
            timeline.append(".")                  # the processor is idle
            t += 1
        timeline.extend([name] * burst)
        t += burst
    return timeline

def sjf(procs):
    todo, t, timeline = list(procs), 0, []
    while todo:
        ready = [p for p in todo if p[1] <= t]
        if not ready:
            timeline.append(".")
            t += 1
            continue
        job = min(ready, key=lambda p: p[2])      # the shortest of those waiting
        todo.remove(job)
        timeline.extend([job[0]] * job[2])
        t += job[2]
    return timeline

def srt(procs):
    left = {name: burst for name, arrival, burst in procs}
    t, timeline = 0, []
    while any(left.values()):
        ready = [(left[n], n) for n, arrival, burst in procs if arrival <= t and left[n] > 0]
        if not ready:
            timeline.append(".")
            t += 1
            continue
        _, name = min(ready)                      # the least time still to go
        left[name] -= 1
        timeline.append(name)
        t += 1
    return timeline

def report(title, timeline, procs):
    waits, turns, responses = [], [], []
    for name, arrival, burst in procs:
        finish = max(i for i, who in enumerate(timeline) if who == name) + 1
        start = timeline.index(name)
        turns.append(finish - arrival)
        waits.append(finish - arrival - burst)
        responses.append(start - arrival)
    count = len(procs)
    print(title.ljust(14), "".join(timeline))
    print(" " * 14, "average wait", round(sum(waits) / count, 2), "| turnaround", round(sum(turns) / count, 2),
          "| response", round(sum(responses) / count, 2))

report("first come", fcfs(procs), procs)
report("shortest job", sjf(procs), procs)
report("shortest left", srt(procs), procs)
```

Each letter in the line is one unit of time, so the line is a **Gantt chart** of who had the processor. Notice that SRT has the lowest waiting time of the three, and that FCFS has the worst: process D waited behind everything.

### Round robin and multi-level queues

**Round robin** is built for sharing. Each process gets a fixed slice of time called the **quantum**. If it is not finished when the quantum ends, it is pre-empted and joins the back of the queue. Nobody waits long to *start*, so it suits interactive systems.

```python
procs = [("A", 0, 8), ("B", 1, 4), ("C", 2, 9), ("D", 3, 5)]

def round_robin(procs, quantum):
    left = {name: burst for name, arrival, burst in procs}
    arrivals = sorted(procs, key=lambda p: p[1])
    queue, t, timeline, i = [], 0, [], 0
    while any(left.values()):
        while i < len(arrivals) and arrivals[i][1] <= t:
            queue.append(arrivals[i][0])
            i += 1
        if not queue:
            timeline.append(".")
            t += 1
            continue
        name = queue.pop(0)
        for _ in range(min(quantum, left[name])):
            timeline.append(name)
            t += 1
            left[name] -= 1
            while i < len(arrivals) and arrivals[i][1] <= t:
                queue.append(arrivals[i][0])
                i += 1
        if left[name] > 0:
            queue.append(name)                  # not finished: back of the queue
    return timeline

def report(title, timeline, procs):
    waits, responses = [], []
    for name, arrival, burst in procs:
        finish = max(i for i, who in enumerate(timeline) if who == name) + 1
        waits.append(finish - arrival - burst)
        responses.append(timeline.index(name) - arrival)
    count = len(procs)
    print(title.ljust(14), "".join(timeline))
    print(" " * 14, "average wait", round(sum(waits) / count, 2), "| response", round(sum(responses) / count, 2))

for quantum in (1, 3, 8):
    report("quantum " + str(quantum), round_robin(procs, quantum), procs)
```

Round robin has a *worse* average waiting time than FCFS here, but a far better **response time**: every process starts within a few units. The quantum is a trade-off. If it is too long, round robin behaves like FCFS (look at the quantum of 8). If it is too short, the processor wastes more and more time on context switches.

A **multi-level feedback queue** (MLFQ) has several queues of different priorities, so it can serve both kinds of job:

1. A new process enters the **top** queue, which has the shortest quantum.
2. The scheduler always runs a process from the highest queue that is not empty.
3. A process that uses its whole quantum is **demoted** to the queue below, which has a longer quantum.
4. A process that gives up the processor early, for example to wait for the keyboard, stays where it is.
5. To stop low-priority processes starving, a process that waits too long is moved **up** again (this is called **aging**).

Short and interactive jobs finish in the top queues, while long calculations sink to the bottom and run in big slices.

!key Which is best? :: None of them. FCFS is simple, SJF and SRT minimise waiting but need to know the future and can starve long jobs, round robin gives fair sharing and good response, and a multi-level queue tries to combine them. Choose by what the system is for.
"""),
        Section("Tasks that take turns", r"""
**Concurrency** means several tasks are *in progress* at the same time, whether or not any two are being executed at the same instant. On one core the processor switches rapidly between them. **Parallelism** means tasks really are executing at the same instant, on separate cores. A concurrent program may run in parallel, but does not need to.

You can model concurrency in Python without any special tools, using **generators**. A function that contains `yield` can *pause* in the middle and be resumed exactly where it left off. A `yield` is a point where the task offers to give up the processor, and a small scheduler decides who runs next.

```python
def task(name, steps):
    for step in range(1, steps + 1):
        print(name, "does step", step)
        yield                          # pause here: someone else can have a turn

def scheduler(tasks):
    queue = list(tasks)
    while queue:
        current = queue.pop(0)
        try:
            next(current)              # run it until its next yield
            queue.append(current)      # not finished: back of the queue
        except StopIteration:
            pass                       # finished: leave the queue

scheduler([task("A", 3), task("B", 2), task("C", 4)])
```

The output interleaves A, B and C. This is exactly **round robin with a quantum of one step**. Real schedulers use a timer interrupt to take the processor away, instead of waiting for a `yield`, but the effect on the programs is the same: the task is paused in the middle, and later carries on.

This model is useful because it is **deterministic**. You can choose exactly which task runs when, and so reproduce a bug that on a real system would appear once in a million runs.
"""),
        Section("Race conditions and locks", r"""
Tasks that share data can interfere. Suppose two tasks each deposit money into one account. Each does three things: **read** the balance, **calculate** the new balance, **write** it back. If task B reads the balance *between* task A's read and write, A's deposit is lost. The result depends on timing, which is a **race condition**.

Model the two steps that matter (read, then write) with a `yield` between them, and try **every possible interleaving** of the two tasks:

```python
from itertools import permutations

def deposit(shared, amount):
    seen = shared["balance"]              # read
    yield                                 # the scheduler may switch tasks here
    shared["balance"] = seen + amount     # write

def run(order):
    shared = {"balance": 100}
    tasks = {"A": deposit(shared, 50), "B": deposit(shared, 25)}
    for who in order:
        try:
            next(tasks[who])
        except StopIteration:
            pass
    return shared["balance"]

outcomes = {}
for order in sorted(set(permutations("AABB"))):
    outcomes["".join(order)] = run(order)

for order, balance in outcomes.items():
    print(order, "->", balance)
print("possible final balances:", sorted(set(outcomes.values())))
```

The right answer is 100 + 50 + 25 = 175. It is only produced when A finishes completely before B starts, or the other way round. In the other four orderings one deposit overwrites the other, giving 125 or 150. The program is *sometimes* right, which is the worst kind of wrong.

The section of code that must not be interleaved is a **critical section**. The solution is **mutual exclusion**: only one task may be inside it at a time. A **lock** (or **mutex**) does this. A task must acquire the lock before entering, and others wait until it is released.

```python
from itertools import permutations

def safe_deposit(shared, amount):
    while shared["locked"]:
        yield                              # wait for the lock to be free
    shared["locked"] = True                # acquire the lock
    seen = shared["balance"]
    yield                                  # even a switch here is now harmless
    shared["balance"] = seen + amount
    shared["locked"] = False               # release the lock

def run(order):
    shared = {"balance": 100, "locked": False}
    tasks = {"A": safe_deposit(shared, 50), "B": safe_deposit(shared, 25)}
    position = 0
    while tasks:
        who = order[position % len(order)]    # follow the plan, skipping tasks that have finished
        position += 1
        if who in tasks:
            try:
                next(tasks[who])
            except StopIteration:
                del tasks[who]
    return shared["balance"]

balances = {run(order) for order in set(permutations("AABB"))}
print("possible final balances:", balances)
```

Every order now gives 175. Locks have a cost: waiting tasks do nothing, and a lock that is never released stops everything behind it. A **semaphore** generalises a lock to a counter, allowing up to n tasks into a section at once, such as n connections to a database.

!warn Always release :: A lock acquired and never released blocks every other task for good. In real code use `with lock:`, which releases it even if an error occurs inside.
"""),
        Section("Deadlock", r"""
Locks fix one problem and can cause another. Suppose task 1 needs lock A and then lock B, and task 2 needs B and then A. If task 1 takes A and task 2 takes B, each is now waiting for a lock the other holds. Neither can go on, and neither will ever let go. This is **deadlock**.

A deadlock needs four conditions at once (the Coffman conditions):

1. **Mutual exclusion.** A resource can be used by only one task at a time.
2. **Hold and wait.** A task holds one resource while waiting for another.
3. **No pre-emption.** A resource cannot be forcibly taken from the task holding it.
4. **Circular wait.** A ring of tasks, each waiting for a resource held by the next.

Here is a tiny simulation. Each task is a generator that yields requests to acquire or release a lock, and the scheduler grants them if it can. If a whole round passes with no progress, the tasks are deadlocked. The scheduler then builds the **wait-for graph** and looks for a cycle.

```python
def worker(first, second):
    yield ("acquire", first)
    yield ("acquire", second)
    yield ("release", second)
    yield ("release", first)

def simulate(tasks):
    held, waiting, requests = {}, {}, {}
    live = dict(tasks)
    for name, gen in live.items():
        requests[name] = next(gen)
    log = []
    while live:
        progress = False
        for name in list(live):
            kind, lock = requests[name]
            if kind == "acquire" and lock in held:
                waiting[name] = lock             # blocked: someone else holds it
                continue
            waiting.pop(name, None)
            if kind == "acquire":
                held[lock] = name
            else:
                del held[lock]
            log.append(name + " " + kind + " " + lock)
            progress = True
            try:
                requests[name] = next(live[name])
            except StopIteration:
                del live[name]
        if not progress:
            return log, waiting, held             # nobody can move
    return log, {}, {}

def find_cycle(waiting, held):
    graph = {task: held[lock] for task, lock in waiting.items()}     # waits for whoever holds its lock
    for start in graph:
        seen, node = [], start
        while node in graph and node not in seen:
            seen.append(node)
            node = graph[node]
        if node in seen:
            return seen[seen.index(node):]
    return None

print("opposite order:")
log, waiting, held = simulate({"T1": worker("A", "B"), "T2": worker("B", "A")})
print("  ", log)
print("   waiting:", waiting, "| held:", held)
print("   cycle:", find_cycle(waiting, held))

print("same order:")
log, waiting, held = simulate({"T1": worker("A", "B"), "T2": worker("A", "B")})
print("  ", log)
print("   waiting:", waiting)
```

In the first run T1 holds A and wants B, while T2 holds B and wants A: a cycle, so deadlock. In the second, both ask for the locks in the same order. T2 simply waits for T1 to finish, so a circular wait is impossible.

### Dealing with deadlock

| Approach | How |
| **Prevention** | Make one of the four conditions impossible. The usual way: every task acquires locks in the **same global order**. |
| **Avoidance** | Only grant a request if the system will still be in a safe state afterwards. |
| **Detection and recovery** | Allow deadlocks, find them (a cycle in the wait-for graph), then end one task or take a resource back. Databases do this. |
| **Ignore it** | Many operating systems leave it to the programmer, on the grounds that it is rare. |

A related problem is **starvation**: a task that never gets a turn, because others keep being chosen first. The ageing in a multi-level queue is there to prevent it.
"""),
        Section("Threads, processes and parallel speed-up", r"""
A **process** is a running program with its own memory. A **thread** is a path of execution *inside* a process. Threads of one process share its memory, which makes them quick to create and easy to share data between, and also the source of every race condition above. Separate processes do not share memory, so they are safer and slower to communicate.

Python's real `threading` module runs in a browser tab only as a simulation, so the examples in this section need your own computer. The first uses a lock to protect a counter shared between four threads:

```pylocal
import threading

total = 0
lock = threading.Lock()

def count(times):
    global total
    for _ in range(times):
        with lock:                    # only one thread at a time in this block
            total += 1

threads = [threading.Thread(target=count, args=(100000,)) for _ in range(4)]
for t in threads:
    t.start()
for t in threads:
    t.join()                          # wait for each thread to finish

print(total)                          # always 400000 with the lock
```

A **queue** is the safe way to hand work from one thread to another. `put` waits if it is full and `get` waits if it is empty, so the **producer** and **consumer** never need a lock of their own:

```pylocal
import queue
import threading

jobs = queue.Queue(maxsize=3)

def producer():
    for n in range(6):
        jobs.put(n)
    jobs.put(None)                    # a marker meaning: no more work

def consumer():
    while True:
        item = jobs.get()
        if item is None:
            break
        print("handled", item)

workers = [threading.Thread(target=producer), threading.Thread(target=consumer)]
for w in workers:
    w.start()
for w in workers:
    w.join()
```

For many similar jobs, a pool is tidier. The next program fetches five things that each take half a second to arrive. One after another they would take two and a half seconds. In a pool of threads, they all wait at once:

```pylocal
import time
from concurrent.futures import ThreadPoolExecutor

def fetch(n):
    time.sleep(0.5)                   # stands for waiting on a network reply
    return n * n

start = time.perf_counter()
with ThreadPoolExecutor(max_workers=5) as pool:
    results = list(pool.map(fetch, range(5)))
print(results, round(time.perf_counter() - start, 1), "seconds")     # about 0.5
```

The same job with `asyncio` uses a single thread, and tasks that hand over control at each `await`. It is the same cooperative idea as the generators earlier, with the language doing the scheduling:

```pylocal
import asyncio

async def fetch(n):
    await asyncio.sleep(0.5)
    return n * n

async def main():
    results = await asyncio.gather(*(fetch(n) for n in range(5)))
    print(results)

asyncio.run(main())
```

### Threads do not speed up heavy calculation

The standard version of Python has a **global interpreter lock** (the GIL): only one thread executes Python code at a time. Threads still help when programs spend their time *waiting* for a network or a disk, because the lock is released while they wait. But for a long calculation, four threads take as long as one. The remedy is separate **processes**, each with its own interpreter:

```pylocal
from multiprocessing import Pool

def count_primes(limit):
    count = 0
    for n in range(2, limit):
        if all(n % d for d in range(2, int(n ** 0.5) + 1)):
            count += 1
    return count

if __name__ == "__main__":
    with Pool(4) as pool:             # four processes, so up to four cores
        print(pool.map(count_primes, [60000] * 4))
```

### How much faster can parallel processing be?

If a program is split between n processors, you might expect n times the speed. **Amdahl's law** says why not: part of any program cannot be split up (reading the input, combining the results). If a fraction `p` of the work can be run in parallel, the best possible speed-up with `n` processors is:

`speed-up = 1 / ((1 - p) + p / n)`

```python
def speedup(p, n):
    return 1 / ((1 - p) + p / n)

print("processors  90% parallel  50% parallel")
for n in (1, 2, 4, 8, 16, 64, 1000):
    print(str(n).ljust(11), str(round(speedup(0.9, n), 2)).ljust(13), round(speedup(0.5, n), 2))
print("the limit when 90% is parallel is", round(1 / (1 - 0.9)), "times, however many processors")
```

A program that is 90% parallel can never go more than ten times faster, even with a thousand processors. The part that cannot be shared sets the limit. That is why parallel hardware pays off only for software designed to use it.
"""),
    ],
    keyterms=[
        ("Scheduler", "The part of the operating system that decides which process uses the processor, and for how long."),
        ("Context switch", "Saving the state of the running process and loading the state of the next one."),
        ("Pre-emption", "The operating system taking the processor away from a running process before it has finished."),
        ("Round robin", "A scheduling algorithm that gives each process in turn a fixed time slice, the quantum."),
        ("Shortest job first", "A scheduling algorithm that runs the waiting process with the shortest burst time."),
        ("Multi-level feedback queue", "A scheduler with several queues of different priorities, in which processes move between queues according to how they behave."),
        ("Turnaround time", "The time from a process arriving to its completion."),
        ("Concurrency", "Having several tasks in progress at once, by taking turns or by running at the same time."),
        ("Parallelism", "Tasks actually executing at the same instant on separate processors or cores."),
        ("Race condition", "A fault where the result depends on the exact timing of tasks that share data."),
        ("Critical section", "A part of a program that accesses shared data and must not be run by two tasks at once."),
        ("Mutual exclusion (lock)", "Allowing only one task at a time into a critical section, usually with a lock."),
        ("Deadlock", "A state in which every task in a group is waiting for a resource held by another, so none can go on."),
        ("Starvation", "A task never getting the processor or resource it needs because others are always chosen first."),
    ],
    grade="""
Scheduling is examined as calculation and as comparison. Concurrency is examined as explanation, with an example.

+ In a calculation, draw the Gantt chart first, then read the waiting times from it
+ Waiting time = completion time - arrival time - burst time
+ Compare algorithms against a criterion: fairness, response, starvation, throughput
+ For a race condition, describe the interleaving that goes wrong, not just the phrase
+ For deadlock, name the circular wait and state one way to prevent it, such as acquiring resources in the same order
""",
    mistakes=[
        "Saying round robin always gives the shortest waiting time. It gives fair sharing and good response time.",
        "Mixing up concurrency (tasks in progress together) with parallelism (tasks executing at the same instant).",
        "Describing deadlock as a loop that never ends. It is tasks each waiting for something another one holds.",
        "Forgetting to release a lock, or releasing it in the wrong place so the critical section is not protected.",
        "Expecting several Python threads to speed up a long calculation. Use processes for that.",
    ],
    quiz=[
        Q("What is a context switch?",
          ["Saving the state of the running process and loading the state of the next", "Changing the screen resolution", "Switching the processor off to save power", "Moving a file from one folder to another"], 0,
          "The scheduler must save the registers and program counter of the old process so that it can carry on later."),
        Q("Which scheduling algorithm gives each process a fixed time slice in turn?",
          ["Round robin", "First come first served", "Shortest job first", "Priority scheduling"], 0,
          "Round robin pre-empts a process when its quantum expires and puts it at the back of the queue."),
        Q("What is a disadvantage of shortest job first scheduling?",
          ["Long processes may be starved, and burst times must be known in advance", "It cannot run more than one process", "It always has the longest average waiting time", "It needs more than one processor"], 0,
          "If short jobs keep arriving, a long job may never be chosen, and the scheduler has to estimate how long each will take."),
        Q("A process arrives at time 2 and needs 5 units. It finishes at time 14. What was its waiting time?",
          ["7", "12", "9", "5"], 0,
          "Turnaround = 14 - 2 = 12. Waiting = turnaround - burst = 12 - 5 = 7."),
        Q("What is the effect of making the quantum in round robin very large?",
          ["It behaves like first come first served", "It gives the best response time", "It increases the number of context switches", "It makes the processor idle"], 0,
          "If the quantum is longer than any burst, each process runs to completion before the next, as in FCFS."),
        Q("What is a race condition?",
          ["A fault where the result depends on the timing of tasks sharing data", "A program that runs faster than expected", "Two programs competing to open the same file name", "A loop that never ends"], 0,
          "Because the tasks interleave differently each time, the outcome can differ between runs."),
        Q("What does a lock provide?",
          ["Mutual exclusion: only one task at a time in a critical section", "A faster way to read data", "A way to run tasks in parallel", "A way to encrypt shared data"], 0,
          "Other tasks must wait until the lock is released before entering the critical section."),
        Q("Which of these is one of the four conditions needed for deadlock?",
          ["Circular wait", "Starvation", "Time slicing", "Thrashing"], 0,
          "The conditions are mutual exclusion, hold and wait, no pre-emption and circular wait."),
        Q("How can deadlock be prevented in a program that needs several locks?",
          ["Make every task acquire the locks in the same order", "Use more locks", "Release every lock after a random delay", "Run every task at the same priority"], 0,
          "A fixed order makes a circular wait impossible."),
        Q("Amdahl's law says that 80% of a program can run in parallel. What is the greatest possible speed-up, however many processors there are?",
          ["5 times", "80 times", "1.25 times", "2 times"], 0,
          "The limit is 1 / (1 - 0.8) = 1 / 0.2 = 5. The part that cannot run in parallel sets the limit."),
    ],
    exam=[
        EQ("Describe how a round robin scheduling algorithm works.", 3, [
            MP("Each process is given a fixed amount of processor time (a time slice or quantum)", ["time slice", "quantum", "fixed", "amount of time"]),
            MP("When the time is used up the process is pre-empted and put at the back of the queue", ["back of the queue", "end of the queue", "pre-empted", "interrupted", "removed"]),
            MP("The next process in the queue then runs, and processes that finish leave the queue", ["next process", "front of the queue", "leave", "next in the queue", "in turn"]),
        ], "Each process in the ready queue is allowed to use the processor for a fixed amount of time called a time slice or quantum. When the time slice is used up, the process is pre-empted and placed at the back of the queue, and the process at the front of the queue is given the processor next. A process that finishes before the end of its time slice leaves the queue.",
           command="Describe"),
        EQ("Three processes, P1, P2 and P3, all arrive at time 0. They need 5, 3 and 1 units of processor time respectively. Calculate the average waiting time when they are scheduled using (a) first come first served, in the order P1, P2, P3 and (b) shortest job first. State which gives the lower average.", 4, [
            MP("FCFS: waiting times of 0, 5 and 8 for P1, P2 and P3", ["0, 5", "5 and 8", "0, 5, 8", "5, 8"]),
            MP("FCFS average = 13 / 3 = 4.33", ["4.33", "4.3", "13 / 3", "13/3"]),
            MP("SJF order P3, P2, P1 gives waiting times of 0, 1 and 4, with an average of 5 / 3 = 1.67", ["1.67", "1.7", "5 / 3", "5/3", "0, 1, 4"]),
            MP("Shortest job first gives the lower average", ["shortest job first", "sjf", "lower", "less"]),
        ], "With first come first served, P1 runs from 0 to 5 so waits 0, P2 runs from 5 to 8 so waits 5, and P3 runs from 8 to 9 so waits 8. The average is (0 + 5 + 8) / 3 = 13 / 3 = 4.33 units. With shortest job first the order is P3, P2, P1. P3 waits 0, P2 waits 1 and P1 waits 4, so the average is (0 + 1 + 4) / 3 = 5 / 3 = 1.67 units. Shortest job first gives the lower average waiting time.",
           command="Calculate"),
        EQ("Explain what is meant by a race condition, and how it can be prevented.", 4, [
            MP("Two (or more) processes or threads access shared data (the same variable)", ["shared", "same variable", "same data", "both access"]),
            MP("The result depends on the order or timing in which they run (they interleave)", ["order", "timing", "interleav", "depends on when", "switch"]),
            MP("For example, one task reads a value, another changes it, then the first writes back, so an update is lost", ["lost", "overwrit", "example", "read", "write back"]),
            MP("It can be prevented by mutual exclusion: a lock (mutex or semaphore) so only one task is in the critical section at a time", ["lock", "mutex", "semaphore", "mutual exclusion", "critical section"]),
        ], "A race condition happens when two or more processes or threads access the same shared data and the result depends on the order or timing in which they run. For example, one thread may read a balance, then another thread updates it, and then the first writes back its result, so that the second update is lost. It can be prevented using mutual exclusion: the code that uses the shared data is made a critical section, protected by a lock (mutex or semaphore), so that only one thread can be in it at any time.",
           command="Explain"),
        EQ("Two processes each need exclusive use of both a printer and a scanner before they can continue. Process 1 has been allocated the printer and Process 2 has been allocated the scanner. Explain why this situation is a deadlock, and describe one way in which deadlock could be prevented.", 5, [
            MP("Process 1 is waiting for the scanner, which is held by Process 2", ["process 1", "waiting for the scanner", "scanner"]),
            MP("Process 2 is waiting for the printer, which is held by Process 1", ["process 2", "waiting for the printer", "printer"]),
            MP("Neither can release what it holds until it has both, so neither can ever continue (circular wait)", ["circular", "neither", "cannot continue", "wait for each other", "both waiting"]),
            MP("Prevention: require resources to be requested in the same fixed order", ["same order", "fixed order", "order", "hierarchy"]),
            MP("Or: a process must request all of its resources at once (or release what it holds), so there is no hold and wait", ["all at once", "all resources", "release", "no hold", "together"]),
        ], "Process 1 holds the printer and is waiting for the scanner, and Process 2 holds the scanner and is waiting for the printer. Each is waiting for a resource that the other holds, and neither can release what it holds until it has both, so neither can ever continue. This circular wait is a deadlock. It could be prevented by making every process request resources in the same fixed order, for example the printer before the scanner, so that a circular wait cannot form. Alternatively a process could be required to request everything that it needs at the same time, so that it never holds one resource while waiting for another.",
           command="Explain"),
        EQ("A photo editing program applies a filter to a very large image. Discuss the use of parallel processing to make it faster.", 6, [
            MP("The image can be divided into sections, each processed on a separate core (or processor) at the same time", ["sections", "divided", "split", "separate core", "at the same time", "simultaneously"]),
            MP("The work on each section is independent, so the speed-up could be close to the number of cores", ["independent", "close to", "number of cores", "faster", "each pixel"]),
            MP("There is overhead in splitting up the image and combining the results", ["overhead", "combining", "combine", "split", "communication"]),
            MP("Some parts cannot be run in parallel, such as loading and saving the file, which limits the speed-up (Amdahl's law)", ["cannot be", "limits", "amdahl", "serial", "sequential", "loading"]),
            MP("The software must be written to use several cores, and the computer must have them", ["written to", "designed to", "multiple cores", "hardware", "software"]),
            MP("A reasoned conclusion: worthwhile for a large image because the filter can be shared out, but gains tail off as more cores are added", ["conclusion", "worthwhile", "overall", "therefore", "diminishing", "tail off"]),
        ], "The image can be divided into sections, with each section processed by a separate core at the same time. Because the filter is applied to each pixel independently, the work can be shared out very evenly and the speed-up could be close to the number of cores. There is some overhead, though, in splitting up the image and combining the results, and some parts of the program, such as loading and saving the file, cannot be done in parallel, which limits the overall speed-up as described by Amdahl's law. The software must be written to use several cores, and the computer must have them. Overall, parallel processing is worthwhile for a very large image because the filter can be shared out easily, but the gains tail off as more cores are added, because the part that cannot be parallelised takes up a bigger share of the total time.",
           command="Discuss"),
    ],
)
