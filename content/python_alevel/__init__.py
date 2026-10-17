"""A Level Computer Science, taught through Python.

One module per topic, grouped into units in content/python_course.py.
INPUTS is only read by tools/check_python_examples.py.
"""
from . import recursion, functional, oop_design, stacks_queues, linked_hash, trees_graphs, pathfinding, big_o, sorting_alevel, binary_bitwise, databases_alevel, testing_tdd, nea_project, heaps_sets, dynamic_greedy, fsm_regex, parsing_bnf, turing_halting, little_man, scheduling_concurrency, crypto_compress, networks_web

MODULES = [
    recursion,
    functional,
    oop_design,
    stacks_queues,
    linked_hash,
    trees_graphs,
    pathfinding,
    big_o,
    sorting_alevel,
    binary_bitwise,
    databases_alevel,
    testing_tdd,
    nea_project,
    heaps_sets,
    dynamic_greedy,
    fsm_regex,
    parsing_bnf,
    turing_halting,
    little_man,
    scheduling_concurrency,
    crypto_compress,
    networks_web,
]
TOPICS = [m.TOPIC for m in MODULES]
INPUTS = {m.TOPIC.slug: getattr(m, "INPUTS", {}) for m in MODULES}
EXPECT = {m.TOPIC.slug: getattr(m, "EXPECT", {}) for m in MODULES}
