"""OCR H446 1.4 Data types, data structures and Boolean algebra: Code Word, Link Up and Bug Hunt."""
from mskbuild.models import Games, Word, Group, Bug

GAMES = [
    Games(
        lesson="data-types-and-boolean-algebra",
        words=[
            Word("MANTISSA", "The part of a floating point number that holds its significant digits."),
            Word("EXPONENT", "The power of two that sets where the binary point goes."),
            Word("NIBBLE", "Four bits, which is one hexadecimal digit."),
        ],
        groups=[
            Group("Boolean laws", ["Identity", "Absorption", "Distributive", "De Morgan's"]),
            Group("Bitwise operations", ["AND", "OR", "XOR", "Left shift"]),
            Group("Karnaugh map rules", ["Group only 1s", "Powers of two", "Groups may overlap", "Wrap around edges"]),
        ],
        bugs=[
            Bug(["In 8 bit two's complement the most significant bit is worth minus 128.",
                 "To negate a two's complement number, invert the bits and add one."],
                "The range of 8 bit two's complement is minus 127 to 128.",
                "It is minus 128 to 127. There is one more negative value because zero uses a positive pattern."),
            Bug(["A normalised positive mantissa starts with 01.",
                 "More exponent bits give a larger range."],
                "Normalising a mantissa reduces its precision.",
                "Normalising removes wasted leading bits, so it gives the greatest possible precision."),
            Bug(["AND with 00001111 keeps only the low four bits.",
                 "OR with 10000000 forces the top bit on."],
                "Shifting a binary number right by one place doubles it.",
                "A right shift halves the number, losing the bit shifted out. A left shift doubles it."),
            Bug(["A + A' always equals 1.",
                 "A . 0 always equals 0."],
                "A + A always equals 2A.",
                "By the idempotent law A + A = A. In Boolean algebra a value ORed with itself is unchanged."),
            Bug(["Karnaugh map groups must contain 1, 2, 4 or 8 cells.",
                 "Groups in a Karnaugh map may wrap around the edges."],
                "Groups in a Karnaugh map must never overlap.",
                "Groups may overlap. Making each group as large as possible matters more."),
        ],
    ),
    Games(
        lesson="data-structures",
        words=[
            Word("QUEUE", "A first in, first out structure, like a line at a bus stop."),
            Word("VERTEX", "A node in a graph, joined to others by edges."),
            Word("TUPLE", "An ordered collection that cannot be changed once it is made."),
        ],
        groups=[
            Group("Linear structures", ["Array", "Stack", "Queue", "Linked list"]),
            Group("Parts of a tree", ["Root", "Leaf", "Parent node", "Child node"]),
            Group("Hash tables", ["Collision", "Load factor", "Rehashing", "Chaining"]),
        ],
        bugs=[
            Bug(["A stack is last in, first out.",
                 "A queue is first in, first out."],
                "A circular queue wastes the space at the front of the array.",
                "That is the problem with a linear queue. A circular queue wraps its pointers round so the space is "
                "reused."),
            Bug(["An array is stored in contiguous memory.",
                 "A linked list node holds data and a pointer to the next node."],
                "A linked list gives direct access to any item by its index.",
                "A linked list must be traversed from the start. Direct access by index is what an array gives."),
            Bug(["In order traversal of a binary search tree gives ascending order.",
                 "Post order traversal suits deleting a tree."],
                "Pre order traversal visits the left subtree before the node.",
                "Pre order visits the node first, then the left subtree, then the right."),
            Bug(["An adjacency list suits a sparse graph.",
                 "An adjacency matrix makes checking for one edge quick."],
                "An adjacency matrix uses less memory than a list for a sparse graph.",
                "A matrix always uses n squared cells, so on a sparse graph it wastes far more memory than a list."),
            Bug(["Two keys that hash to the same index cause a collision.",
                 "Linear probing can cause clustering."],
                "A hash table gets faster as its load factor rises.",
                "As the load factor rises, collisions become more frequent and performance falls, so the table is "
                "rehashed."),
        ],
    ),
]
