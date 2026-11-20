"""OCR H446 2.3 Algorithms: Code Word, Link Up and Bug Hunt."""
from mskbuild.models import Games, Word, Group, Bug

GAMES = [
    Games(
        lesson="algorithms-and-complexity",
        words=[
            Word("PIVOT", "The item quicksort uses to split the data into smaller and larger values."),
            Word("DIJKSTRA", "His shortest path algorithm cannot handle negative edge weights."),
            Word("BINARY", "This search halves a sorted range with every comparison."),
        ],
        groups=[
            Group("Searches", ["Linear", "Binary", "Depth first", "Breadth first"]),
            Group("Sorting algorithms", ["Bubble", "Insertion", "Merge", "Quick"]),
            Group("Shortest path ideas", ["Dijkstra", "A star", "Heuristic", "Admissible"]),
        ],
        bugs=[
            Bug(["Binary search needs the data to be sorted.",
                 "Linear search works on unsorted data."],
                "Binary search is O(n) because it checks every item.",
                "Binary search halves the range at every comparison, so it is O(log n)."),
            Bug(["Merge sort is O(n log n) whatever the order of the data.",
                 "Merge sort needs O(n) extra memory."],
                "Quicksort is O(n log n) even in its worst case.",
                "Quicksort's worst case is O(n squared), when the pivot is always the smallest or largest item."),
            Bug(["Depth first search uses a stack.",
                 "Breadth first search uses a queue."],
                "Depth first search finds the shortest path in an unweighted graph.",
                "It is breadth first search that finds the shortest path in an unweighted graph, by exploring level by "
                "level."),
            Bug(["Dijkstra's algorithm finds shortest paths from one start node.",
                 "Dijkstra's algorithm needs non negative edge weights."],
                "Dijkstra uses a heuristic estimate.",
                "Dijkstra uses no heuristic. A star adds one, choosing the node with the lowest f = g + h."),
            Bug(["A star chooses the node with the lowest value of g plus h.",
                 "An admissible heuristic never overestimates the remaining cost."],
                "A star is guaranteed the best path whatever heuristic it uses.",
                "Only an admissible heuristic, one that never overestimates, guarantees the best path."),
        ],
    ),
]
