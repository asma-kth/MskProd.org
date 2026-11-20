"""OCR H446 2.3 Algorithms: stretch tasks."""
from mskbuild.models import Blitz, Written, Stretch, MP, Pick, Pair, Sort, SortItem

COURSE = "ks5"

LESSONS = [
    Stretch(
        lesson="algorithms-and-complexity",
        blitz=[
            Blitz("What is the time complexity of binary search?",
                  options=["O(log n)", "O(n)", "O(n log n)", "O(1)"],
                  explain="Each comparison halves the range, so a million items need only about twenty comparisons."),
            Blitz("What must be true of data before a binary search?",
                  options=["It must be sorted", "It must contain no duplicates", "It must be stored in a linked list",
                           "It must have an even number of items"],
                  explain="Comparing with the middle item only tells you which half to discard if the data is in order."),
            Blitz("Merge sort takes O(n log n) time in every case.", kind="tf", answer=True,
                  explain="Its splitting and combining do the same work whatever the order of the data, which is its "
                          "great strength."),
            Blitz("Which data structure does depth first search use?",
                  options=["Stack", "Queue", "Hash table", "Two dimensional array"],
                  explain="Depth first search backtracks to the most recent branch, last in, first out, so it uses a "
                          "stack or recursion."),
            Blitz("Which TWO sorts use only a fixed amount of extra memory?", kind="multi", n=2,
                  options=["Bubble sort", "Insertion sort", "Merge sort", "Quicksort"],
                  explain="Bubble and insertion sort work in place. Merge sort stores its sub lists, and quicksort needs "
                          "a stack for its recursion."),
            Blitz("Order these complexities from the slowest growing to the fastest growing.", kind="order",
                  options=["O(1)", "O(log n)", "O(n)", "O(n log n)"],
                  explain="Constant, then logarithmic, then linear, then linearithmic."),
            Blitz("When does quicksort hit its worst case of O(n squared)?",
                  options=["When the pivot is always the smallest or largest item", "When the list is very short",
                           "When every item is different", "When it uses a stack"],
                  explain="A bad pivot leaves one side empty every time, so the list shrinks by only one item per pass."),
            Blitz("Dijkstra's algorithm works correctly with negative edge weights.", kind="tf", answer=False,
                  explain="Once a node is visited its distance is treated as final, so a negative edge found later "
                          "could break that."),
            Blitz("Which algorithm finds shortest paths by choosing the node with the lowest f(n) = g(n) + h(n)?",
                  kind="type",
                  accept=["a star", "a*", "astar", "a star search", "a* search", "the a star algorithm",
                          "a star algorithm"],
                  explain="g is the cost so far and h is a heuristic estimate of the cost still to go."),
            Blitz("What makes an A star heuristic admissible?",
                  options=["It never overestimates the remaining cost", "It always overestimates the cost",
                           "It ignores the edge weights", "It visits every node"],
                  explain="An admissible heuristic guarantees that A star finds the optimal path."),
            Blitz("Which search finds the shortest path in an unweighted graph?",
                  options=["Breadth first search", "Depth first search", "Linear search", "Binary search"],
                  explain="It explores every node one step away, then two, so it first reaches each node by the fewest "
                          "edges."),
            Blitz("Why might you sort data before searching it, even though sorting costs O(n log n)?",
                  options=["Many later searches each drop from O(n) to O(log n)", "Sorting makes the data smaller",
                           "Unsorted data cannot be searched at all", "Sorting removes duplicates"],
                  explain="The sorting cost is paid once, and every search after that is far faster."),
        ],
        short=[
            Written("Explain why binary search is O(log n).", 2, [
                MP("Each comparison halves the remaining range",
                   ["halves", "half", "halving", "discard half", "cuts in half"]),
                MP("So doubling the number of items adds only one more comparison",
                   ["one more comparison", "one extra", "doubling", "twenty", "logarithm"]),
            ], "Each comparison halves the remaining range, so doubling the number of items adds only one more "
               "comparison. A million items need only about twenty comparisons.",
               command="Explain"),
            Written("Explain why Dijkstra's algorithm cannot handle negative edge weights.", 2, [
                MP("Once a node is visited its distance is treated as final",
                   ["final", "visited", "fixed", "permanent", "settled"]),
                MP("A negative edge found later could give a shorter route",
                   ["shorter", "later", "smaller distance", "reduce", "lower"]),
            ], "Once a node is marked visited its distance is treated as final, but a negative edge found later could "
               "give a shorter route to it, so the answer could be wrong.",
               command="Explain"),
            Written("Give one advantage of merge sort over quicksort, and one of quicksort over merge sort.", 2, [
                MP("Merge sort is O(n log n) in every case, quicksort is not",
                   ["every case", "worst case", "guaranteed", "always", "consistent", "consistently"]),
                MP("Quicksort needs less memory and is usually faster in practice",
                   ["less memory", "less space", "memory", "space", "faster in practice", "usually faster",
                    "better constants"]),
            ], "Merge sort is O(n log n) in every case, while quicksort can fall to n squared in its worst case. "
               "Quicksort needs less memory, because merge sort has to store the sub lists, and it is usually faster in "
               "practice.",
               command="Give"),
            Written("Explain why depth first search uses a stack and breadth first search uses a queue.", 2, [
                MP("Depth first goes as deep as possible, then backtracks to the most recent branch",
                   ["most recent", "last in first out", "lifo", "backtrack", "backtracks", "as deep as possible",
                    "deepest"]),
                MP("Breadth first visits nodes in the order they were found, level by level",
                   ["order they were found", "order found", "first in first out", "fifo", "level by level",
                    "all neighbours", "neighbours first"]),
            ], "Depth first search goes as deep as possible, then backtracks to the most recent branch, which is last "
               "in, first out, like a stack. Breadth first search visits nodes in the order they were found, level by "
               "level, which is first in, first out, like a queue.",
               command="Explain"),
        ],
        long=[
            Written("Describe how Dijkstra's algorithm finds the shortest path from a start node.", 6, [
                MP("The start node gets distance 0 and every other node infinity",
                   ["infinity", "infinite", "distance 0", "distance of 0", "zero"]),
                MP("Every node starts unvisited", ["unvisited"]),
                MP("The unvisited node with the smallest known distance becomes the current node",
                   ["smallest", "shortest known", "lowest"]),
                MP("The distance to each unvisited neighbour through the current node is worked out",
                   ["neighbour", "neighbours", "through the current"]),
                MP("A shorter distance replaces the old one, with the current node as predecessor",
                   ["update", "updated", "replace", "replaced", "previous", "predecessor"]),
                MP("The current node is marked visited and the steps repeat",
                   ["mark", "marked", "repeat", "repeats", "until"]),
                MP("The path is rebuilt by working back through the predecessors",
                   ["work back", "working back", "backwards", "back from"]),
                MP("The weights must not be negative", ["negative"]),
            ], "The start node is given a distance of 0 and every other node a distance of infinity, and all nodes are "
               "marked unvisited. The unvisited node with the smallest known distance becomes the current node. For "
               "each unvisited neighbour, the distance through the current node is calculated, and if it is shorter "
               "than the recorded distance it is updated and the current node is recorded as its predecessor. The "
               "current node is then marked visited, and this repeats until the destination is visited. The path is "
               "rebuilt by working back from the destination through the predecessors. The edge weights must not be "
               "negative.",
               command="Describe",
               frame=["The start node", "Each time", "For every neighbour", "Finally"]),
            Written("Explain how A star improves on Dijkstra's algorithm, and when it is guaranteed to find the best "
                    "path.", 4, [
                MP("It adds a heuristic estimate of the distance still to go",
                   ["heuristic", "estimate", "straight line"]),
                MP("It chooses the node with the lowest f = g + h",
                   ["g + h", "g plus h", "lowest f", "actual cost"]),
                MP("It explores far fewer nodes, so it is faster",
                   ["fewer nodes", "fewer", "faster", "less work", "towards the goal"]),
                MP("It is optimal when the heuristic is admissible, never overestimating",
                   ["admissible", "never overestimates", "overestimate", "overestimates"]),
                MP("Dijkstra is A star with h set to zero", ["h = 0", "h is 0", "h is zero", "zero heuristic"]),
            ], "A star adds a heuristic, an estimate of the remaining distance to the goal such as the straight line "
               "distance. At each step it chooses the node with the lowest f = g + h, where g is the actual cost so "
               "far. Because it prefers nodes that lead towards the goal, it explores far fewer nodes and is faster. It "
               "is guaranteed to find the best path as long as the heuristic is admissible, meaning it never "
               "overestimates the remaining cost.",
               command="Explain",
               frame=["A star adds", "At each step it chooses", "This means it",
                      "It is guaranteed to find the best path when"]),
        ],
        picks=[
            Pick("Which search works on unsorted data?",
                 "Linear search", "Binary search",
                 "Linear search simply checks each item. Binary search needs sorted data to discard half each time."),
            Pick("Which is O(n log n) even in its worst case?",
                 "Merge sort", "Quicksort",
                 "Quicksort can fall to n squared with bad pivots. Merge sort does the same work every time."),
            Pick("Which sort suits a small list that is nearly sorted?",
                 "Insertion sort", "Merge sort",
                 "Insertion sort is close to O(n) on nearly sorted data and needs no extra memory."),
            Pick("Which grows faster as n increases?",
                 "O(n squared)", "O(n log n)",
                 "For a million items, n squared is a million million, but n log n is about twenty million."),
            Pick("Which finds the nearest node to a start point in an unweighted graph?",
                 "Breadth first search", "Depth first search",
                 "Breadth first explores level by level, so the first time it meets a node is by the fewest edges."),
            Pick("Dijkstra's algorithm is the same as A star with what?",
                 "h set to zero", "g set to zero",
                 "With no heuristic, A star chooses purely by the cost so far, which is exactly what Dijkstra does."),
            Pick("Which statement is about space rather than time?",
                 "Merge sort needs O(n) memory", "Merge sort takes O(n log n) steps",
                 "Space complexity is about memory. Merge sort's O(n) space is the price it pays for its speed."),
            Pick("What is the average complexity of a hash table lookup?",
                 "O(1)", "O(n)",
                 "The hash function goes straight to the index, however many items there are."),
        ],
        pairs=[
            Pair("Linear search", "Checks each item in turn"),
            Pair("Binary search", "Halves a sorted range each comparison"),
            Pair("Bubble sort", "Swaps adjacent pairs that are out of order"),
            Pair("Merge sort", "Splits to single items, then merges back"),
            Pair("Quicksort", "Partitions the items around a pivot"),
            Pair("Dijkstra", "Shortest paths with non negative weights"),
        ],
        pair_names=("Algorithm", "How it works"),
        sort=Sort(
            prompt="What is the time complexity of each?",
            bins=["O(1)", "O(log n)", "O(n)", "O(n squared)"],
            items=[
                SortItem("Reading an array element by its index", 0,
                         "The address is worked out directly, however long the array."),
                SortItem("A hash table lookup on average", 0,
                         "The hash function goes straight to the right slot."),
                SortItem("Pushing an item onto a stack", 0,
                         "Adding to the top takes the same time however full the stack is."),
                SortItem("Binary search", 1, "Each comparison halves the range."),
                SortItem("Searching a balanced binary search tree", 1,
                         "Each step down a balanced tree halves what is left."),
                SortItem("Finding a word by halving a dictionary", 1, "Halving the pages each time is logarithmic."),
                SortItem("Linear search", 2, "In the worst case every item is checked once."),
                SortItem("Finding the largest value in an unsorted list", 2, "Every item must be looked at once."),
                SortItem("Printing every item of a list", 2, "One step for each item is linear."),
                SortItem("Bubble sort", 3, "Up to n passes of up to n comparisons."),
                SortItem("Insertion sort on a reversed list", 3,
                         "Each item has to move past every item before it."),
                SortItem("Comparing every item with every other item", 3,
                         "n items each compared with n others gives n squared."),
            ]),
    ),
]
