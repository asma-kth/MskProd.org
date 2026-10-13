"""A Level Python: Dijkstra's shortest path algorithm and A* search."""
from mskbuild.models import Topic, Section, Q, EQ, MP

INPUTS = {}
EXPECT = {}

TOPIC = Topic(
    slug="dijkstra-and-a-star",
    title="Dijkstra's Algorithm and A* Search",
    spec="A Level 7",
    icon="i-map",
    minutes=55,
    blurb="The two shortest path algorithms in the specification: Dijkstra's, built on a priority queue and traced in a table, and A*, which adds a heuristic and visibly explores a fraction of the graph, both running on real data.",
    fact="Edsger Dijkstra designed his shortest path algorithm in about twenty minutes in 1956, without pencil and paper, while shopping with his fiancée in Amsterdam. He later said that the lack of pencil and paper had forced him to avoid unnecessary complication.",
    sections=[
        Section("Dijkstra's shortest path algorithm", r"""
In a **weighted graph** every edge has a cost, such as a distance, a time or a price. The **shortest path** between two vertices is the one with the lowest **total** weight, which is not necessarily the one with the fewest edges. Breadth first search counts edges. Dijkstra's algorithm counts weights.

It finds the shortest distance from one **start** vertex to **every other** vertex, as long as no weight is negative. It works by always **fixing** the nearest vertex that is not yet fixed, and then seeing whether that vertex gives a shorter way to any of its neighbours.

!diagram py-dijkstra

The method, which the exam expects you to be able to carry out by hand:

1. Give the start vertex a distance of 0 and every other vertex a distance of **infinity**.
2. Choose the unfixed vertex with the **smallest** distance and fix it. That distance is now final.
3. For each neighbour of that vertex, work out *distance of the vertex plus the edge weight*. If that is **smaller** than the neighbour's recorded distance, replace the distance, and record that the neighbour was reached from this vertex.
4. Repeat from step 2 until every vertex is fixed, or until the goal is fixed.

Step 2 is "find the smallest of the waiting vertices", and a **priority queue** does exactly that. Python's `heapq` is one.

```python
import heapq

graph = {
    "A": {"B": 7, "C": 9, "F": 14},
    "B": {"A": 7, "C": 10, "D": 15},
    "C": {"A": 9, "B": 10, "D": 11, "F": 2},
    "D": {"B": 15, "C": 11, "E": 6},
    "E": {"D": 6, "F": 9},
    "F": {"A": 14, "C": 2, "E": 9},
}

def dijkstra(graph, start):
    distance = {v: float("inf") for v in graph}
    previous = {v: None for v in graph}
    distance[start] = 0
    queue = [(0, start)]
    fixed = []
    while queue:
        dist, vertex = heapq.heappop(queue)
        if vertex in fixed:
            continue                                  # an out of date entry
        fixed.append(vertex)
        for neighbour, weight in graph[vertex].items():
            new = dist + weight
            if new < distance[neighbour]:
                distance[neighbour] = new
                previous[neighbour] = vertex
                heapq.heappush(queue, (new, neighbour))
        row = [distance[v] for v in graph]
        print("fixed", vertex, row)
    return distance, previous

def path_to(previous, goal):
    path = []
    while goal is not None:
        path.append(goal)
        goal = previous[goal]
    return path[::-1]

distance, previous = dijkstra(graph, "A")
print(path_to(previous, "E"), distance["E"])
```

The lines printed are the rows of the working table the exam asks for, with the columns in the order A, B, C, D, E, F:

| Step | Fixed | A | B | C | D | E | F |
| 1 | A | 0 | 7 | 9 | ∞ | ∞ | 14 |
| 2 | B | 0 | 7 | 9 | 22 | ∞ | 14 |
| 3 | C | 0 | 7 | 9 | **20** | ∞ | **11** |
| 4 | F | 0 | 7 | 9 | 20 | **20** | 11 |
| 5 | D | 0 | 7 | 9 | 20 | 20 | 11 |
| 6 | E | 0 | 7 | 9 | 20 | 20 | 11 |

Step 3 is the one that shows the method working. When C is fixed at 9, the route to D through C costs 9 + 11 = 20, which beats the 22 found through B. The route to F through C costs 9 + 2 = 11, which beats the direct edge of 14. The bold values are distances that were **improved**.

!key Read the shortest path backwards :: Each vertex remembers the vertex it was reached from. To find the route to E, start at E and follow `previous` back to A, then reverse it. E was reached from F, F from C, and C from A, so the route is A, C, F, E, with a total of 20.

### Why a negative weight breaks it

Dijkstra's algorithm is **greedy**. When it fixes a vertex, it assumes no later route can be shorter, because every later route has to go through vertices that are further away and can only add. A negative edge could subtract, making an apparently longer route into a shorter one after the vertex was already declared final.

### How much work

With a heap, each edge causes at most one push, and each push or pop costs the logarithm of the heap's size. The total is about (V + E) log V steps, where V is the number of vertices and E the number of edges. That is fast enough for a road network of millions of junctions.
"""),
        Section("A* search", r"""
Dijkstra's algorithm spreads out from the start in every direction, like a ripple, and fixes every vertex nearer than the goal. If you are navigating from Manchester to Leeds, that includes vertices in Wales. **`A*`** (say "A star") avoids this by being **guided**: it prefers vertices that look as if they are heading **towards the goal**.

For each vertex *n* it uses two numbers:

- **g(n)**: the real cost of the best route found **so far** from the start to *n*
- **h(n)**: a **heuristic**, an **estimate** of the cost still to go from *n* to the goal

and it always expands the vertex with the smallest **f(n) = g(n) + h(n)**, the estimated cost of the whole journey through *n*. Dijkstra's algorithm is exactly `A*` with **h = 0** for every vertex.

### The heuristic

A heuristic is a rule of thumb: a quick estimate that need not be exact. For finding a route across a map, the straight line distance to the goal is a natural one. On a grid where you can move up, down, left and right, it is the **Manhattan distance**, the number of rows plus the number of columns still to travel.

For `A*` to be certain to find the **shortest** path, the heuristic must be **admissible**: it must **never overestimate** the true remaining cost. The Manhattan distance is admissible on this grid, because you can never get there in fewer moves than the rows plus columns, and walls can only make it longer. A heuristic that overestimated could make the best route look too expensive, and `A*` would pass it over.

### Dijkstra and A* on the same grid

Both programs below are the same code. The only difference is whether `h` is 0 or the Manhattan distance. `o` marks every cell that was expanded, and `*` is the path found. Ties in f are broken in favour of the smaller h, which keeps `A*` heading for the goal.

```python
import heapq

GRID = [
    "S.........",
    "..........",
    "..........",
    "......#...",
    "......#...",
    "......#...",
    "......#...",
    "..........",
    "..........",
    ".........G",
]

def search(grid, start, goal, use_heuristic):
    rows, cols = len(grid), len(grid[0])

    def h(cell):
        if not use_heuristic:
            return 0
        return abs(cell[0] - goal[0]) + abs(cell[1] - goal[1])

    best = {start: 0}
    previous = {start: None}
    queue = [(h(start), h(start), 0, start)]
    expanded = []
    while queue:
        f, estimate, g, cell = heapq.heappop(queue)
        if cell in expanded:
            continue
        expanded.append(cell)
        if cell == goal:
            break
        row, col = cell
        for step_row, step_col in ((0, 1), (1, 0), (0, -1), (-1, 0)):
            r, c = row + step_row, col + step_col
            if 0 <= r < rows and 0 <= c < cols and grid[r][c] != "#":
                new_g = g + 1
                if new_g < best.get((r, c), 10 ** 9):
                    best[(r, c)] = new_g
                    previous[(r, c)] = cell
                    heapq.heappush(queue, (new_g + h((r, c)), h((r, c)), new_g, (r, c)))
    path = []
    cell = goal
    while cell is not None:
        path.append(cell)
        cell = previous[cell]
    return expanded, path[::-1]

for name, use_h in (("Dijkstra", False), ("A*", True)):
    expanded, path = search(GRID, (0, 0), (9, 9), use_h)
    canvas = [list(line) for line in GRID]
    for row, col in expanded:
        if canvas[row][col] == ".":
            canvas[row][col] = "o"
    for row, col in path[1:-1]:
        canvas[row][col] = "*"
    print(name, "expanded", len(expanded), "cells; path of", len(path) - 1, "steps")
    for line in canvas:
        print("".join(line))
```

Both find a path of 18 steps, which is the shortest possible. Dijkstra's algorithm had to look at 96 cells to prove it, and `A*` looked at 19.

### Choosing between the three

| | Breadth first | Dijkstra | A* |
| Edge weights | All equal | Any, not negative | Any, not negative |
| Finds the shortest path | Yes, in edges | Yes | Yes, if the heuristic is admissible |
| Explores | Evenly in all directions | Evenly in all directions | Mostly towards the goal |
| Needs | A queue | A priority queue | A priority queue and a heuristic |
| Used for | Fewest hops | Network routing protocols, shortest path to many destinations | Satnav, game characters finding their way |

Dijkstra's algorithm answers "how far is it to everywhere?" `A*` answers "what is the best route to **this** place?", and gets there faster by using what it knows about where the goal is.

!exam Always write f = g + h, and say which is which :: A frequent question gives a table of g and h values for the vertices waiting in the open list, and asks which A* expands next. Work out f for each one, write it down, and choose the smallest. Say that h must never overestimate, or the shortest path is not guaranteed.
"""),
    ],
    keyterms=[
        ("Shortest path", "The route between two vertices of a weighted graph with the lowest total weight."),
        ("Dijkstra's algorithm", "An algorithm that finds the shortest distance from a start vertex to every other vertex in a graph with non-negative weights."),
        ("Priority queue", "A queue from which the item with the highest priority, here the smallest distance, is always removed first."),
        ("Greedy algorithm", "An algorithm that makes the best looking choice at each step, without reconsidering it."),
        ("A* search", "A shortest path algorithm that uses a heuristic to prefer vertices that appear to lead towards the goal."),
        ("Heuristic", "An estimate or rule of thumb that is quick to calculate and need not be exact."),
        ("Admissible heuristic", "A heuristic that never overestimates the true cost of reaching the goal."),
        ("g(n)", "In A*, the cost of the best known route from the start to vertex n."),
        ("h(n)", "In A*, the heuristic estimate of the cost from vertex n to the goal."),
        ("Manhattan distance", "The distance between two points on a grid measured as rows plus columns, as when moving only up, down, left and right."),
    ],
    grade="""
Shortest path questions are marked on method shown in a table, and on being exact about the difference between the two algorithms.

+ Set up the working table with infinity for every vertex but the start, and update a row per fixed vertex
+ Only replace a distance when the new total is strictly smaller, and record where it came from
+ Write the path backwards from the goal using the recorded previous vertices, then reverse it
+ State A* as f = g + h and name g as cost so far and h as the estimate still to go
+ Say that an admissible heuristic never overestimates, and that this is what guarantees the shortest path
""",
    mistakes=[
        "Fixing a vertex that does not have the smallest distance among those not yet fixed.",
        "Adding the edge weight to the start distance instead of to the distance of the vertex just fixed.",
        "Describing A* as always faster, without saying that it depends on a good heuristic.",
        "Using a heuristic that overestimates the cost and so losing the guarantee of the shortest path.",
        "Applying Dijkstra's algorithm to a graph with negative weights.",
    ],
    quiz=[
        Q("What does Dijkstra's algorithm find?",
          ["The shortest distance from a start vertex to every other vertex in a weighted graph",
           "The vertex with the most edges in an unweighted graph",
           "The shortest path through a graph that has negative weights",
           "The order in which the vertices were added to the graph"], 0,
          "It works on weighted graphs where no weight is negative, and gives a distance to every vertex."),
        Q("Which data structure is used to choose the next vertex in Dijkstra's algorithm?",
          ["A priority queue", "A stack", "An adjacency matrix", "A binary tree that is sorted by name"], 0,
          "The unfixed vertex with the smallest recorded distance is needed each time, which is the front of a priority queue."),
        Q("What distance does Dijkstra's algorithm give every vertex except the start at the beginning?",
          ["Infinity", "Zero", "One", "The weight of its nearest edge"], 0,
          "Nothing is known about those vertices yet, so every route found will be shorter than infinity."),
        Q("Why can Dijkstra's algorithm not be used on a graph with negative weights?",
          ["A vertex that has been fixed could later be reached by a shorter route",
           "A negative weight cannot be stored in a priority queue", "The graph would no longer be connected",
           "The algorithm would not be able to find the start vertex"], 0,
          "The algorithm assumes that further routes can only add to a distance, which a negative weight breaks."),
        Q("In A* search, what does f(n) = g(n) + h(n) represent?",
          ["The estimated total cost of a route that goes through vertex n", "The number of edges leaving vertex n",
           "The real distance from vertex n to the goal", "The difference between the start and the goal"], 0,
          "g is what it has cost to get to n, and h is the estimate of what is left."),
        Q("What does g(n) represent in A* search?",
          ["The cost of the best route found so far from the start to n", "The estimated cost from n to the goal",
           "The number of vertices adjacent to n", "The greatest edge weight in the graph"], 0,
          "g is a real cost, already incurred, while h is a guess about the future."),
        Q("What is an admissible heuristic?",
          ["One that never overestimates the true cost to reach the goal", "One that is always exactly equal to the true cost",
           "One that has been approved by the user of the program", "One that gives the same estimate for every vertex"], 0,
          "If the estimate is never too high, the best route is never ruled out by being made to look too expensive."),
        Q("Which heuristic suits a grid where movement is up, down, left or right only?",
          ["The Manhattan distance to the goal", "The number of walls on the grid", "The number of cells already expanded",
           "The cost of the cell nearest the start"], 0,
          "The rows plus columns remaining is the fewest moves possible, so it never overestimates."),
        Q("What is A* search when the heuristic is zero for every vertex?",
          ["The same as Dijkstra's algorithm", "The same as a depth first search", "The same as a linear search",
           "It does not work at all"], 0,
          "With h = 0 the priority is simply g, the distance so far, which is exactly Dijkstra's rule."),
        Q("Why is A* often faster than Dijkstra's algorithm for finding a route to one particular place?",
          ["The heuristic makes it explore mainly in the direction of the goal",
           "It stops checking the edge weights, so each step takes much less time",
           "It stores the whole graph as an adjacency matrix, which is faster to search",
           "It avoids using a priority queue, which is the slowest part of Dijkstra's algorithm"], 0,
          "Dijkstra's spreads in every direction, while A* leans towards the goal and so expands fewer vertices."),
    ],
    exam=[
        EQ("State the purpose of Dijkstra's shortest path algorithm, and state one restriction on the graph it is used on.", 2, [
            MP("It finds the shortest path, or the shortest distance, from a start vertex to the other vertices of a weighted graph", ["shortest path", "shortest distance", "lowest total", "start vertex", "weighted"]),
            MP("The weights must not be negative", ["negative", "non-negative", "not be negative", "positive"]),
        ], "Dijkstra's algorithm finds the shortest path, meaning the one with the lowest total weight, from a start vertex to the other vertices of a weighted graph. It can only be used if none of the edge weights is negative.",
           command="State"),
        EQ("Use Dijkstra's algorithm to find the shortest path from A to E in the graph shown. Show your working, and state the path and its total weight.", 6, [
            MP("A is given 0, and B and C are updated to 4 and 2 after A is fixed", ["a = 0", "b = 4", "c = 2", "4", "2"]),
            MP("C is fixed next, being the smallest, and B is improved to 3", ["c is fixed", "b = 3", "3", "improved", "via c"]),
            MP("B is fixed and D is updated to 8", ["d = 8", "8"]),
            MP("D is fixed and E is updated to 10", ["e = 10", "10"]),
            MP("The shortest path is A, C, B, D, E", ["a, c, b, d, e", "a c b d e", "acbde"]),
            MP("The total weight is 10", ["10"]),
        ], "A is fixed at 0, which sets B to 4 and C to 2. C has the smallest distance so it is fixed next. The route to B through C is 2 + 1 = 3, which is less than 4, so B becomes 3. C also sets D to 10 and E to 12. B is fixed next at 3, and D becomes 3 + 5 = 8, which is less than 10. D is fixed at 8, and E becomes 8 + 2 = 10, which is less than 12. E is fixed at 10. Reading back from E, it was reached from D, D from B, B from C and C from A. The shortest path is A, C, B, D, E and its total weight is 10.",
           command="Show",
           figure="""| Edge | Weight |
| A to B | 4 |
| A to C | 2 |
| B to C | 1 |
| B to D | 5 |
| C to D | 8 |
| C to E | 10 |
| D to E | 2 |"""),
        EQ("In an A* search, four vertices are waiting to be expanded. Their values of g and h are shown. Calculate f for each vertex and state which vertex is expanded next.", 3, [
            MP("f is calculated as g + h", ["g + h", "g+h", "add"]),
            MP("The values are P = 10, Q = 9, R = 12 and S = 10", ["10", "9", "12", "p = 10", "q = 9"]),
            MP("Q is expanded next, as it has the lowest f", ["q", "lowest f", "smallest f", "lowest"]),
        ], "f is g plus h, so P is 4 + 6 = 10, Q is 7 + 2 = 9, R is 3 + 9 = 12 and S is 5 + 5 = 10. The vertex with the lowest value of f is expanded next, which is Q.",
           command="Calculate",
           figure="""| Vertex | g | h |
| P | 4 | 6 |
| Q | 7 | 2 |
| R | 3 | 9 |
| S | 5 | 5 |"""),
        EQ("Explain the role of the heuristic in the A* algorithm, and why it must not overestimate the cost.", 4, [
            MP("The heuristic is an estimate of the cost from a vertex to the goal", ["estimate", "estimated", "guess", "cost to the goal", "remaining"]),
            MP("It is used to choose the vertex to expand next, so the search is guided towards the goal", ["guided", "towards the goal", "direction", "choose", "next vertex", "prioritise"]),
            MP("This means fewer vertices are explored than in Dijkstra's algorithm", ["fewer", "less", "faster", "quicker", "fewer vertices", "more efficient"]),
            MP("If it overestimated, a vertex on the shortest path could be made to look too costly and be ignored, so the path found might not be the shortest", ["ignored", "too costly", "not be the shortest", "miss", "overlook", "not shortest", "not optimal"]),
        ], "The heuristic is an estimate of the cost of getting from a vertex to the goal. A* adds it to the cost so far and expands the vertex with the lowest total, which guides the search towards the goal, so it explores fewer vertices than Dijkstra's algorithm, which spreads out in every direction. It must not overestimate because a vertex on the shortest path could then look more expensive than it really is, and be passed over, so the path found might not be the shortest.",
           command="Explain"),
        EQ("A satellite navigation system must find a route between two towns on a road network. Compare using Dijkstra's algorithm with using A* for this task.", 4, [
            MP("Both find the shortest route if the weights are not negative and the heuristic is admissible", ["both find", "both give", "shortest", "optimal", "same route"]),
            MP("Dijkstra's explores in every direction from the start, including roads that lead away from the destination", ["every direction", "all directions", "away from", "spreads", "ripple"]),
            MP("A* uses an estimate, such as the straight line distance to the destination, to explore mainly towards it", ["straight line", "estimate", "heuristic", "towards", "destination"]),
            MP("So A* usually finds the route more quickly, and is better for this task, though it needs a suitable heuristic", ["quicker", "faster", "fewer", "better", "more efficient", "suitable heuristic", "needs"]),
        ], "Both algorithms find the shortest route, provided the road lengths are not negative and the heuristic used by A* never overestimates. Dijkstra's algorithm explores outwards in every direction from the start, including roads leading away from the destination. A* uses an estimate, such as the straight line distance to the destination, to explore mainly towards it. A* is therefore usually quicker for finding a route between two particular towns, and the better choice here, although it needs a suitable heuristic to be available.",
           command="Compare"),
    ],
)
