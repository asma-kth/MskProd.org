"""Stretch tasks for every lesson of the Key Stage 3 course, Year 7 to Year 9.

One module per unit, in the order the units are taught. Each defines TOPIC,
the slug of its unit, and LESSONS, one Stretch per lesson of that unit in the
order the unit teaches them. A lesson is a section of the unit's topic page.
"""
import importlib

MODULES = [
    "y7_using_computers", "y7_scratch", "y7_python", "y7_understanding_computers", "y7_vector_graphics",
    "y8_digital_literacy", "y8_computational_thinking", "y8_python", "y8_spreadsheets",
    "y8_networks", "y8_web",
    "y9_law", "y9_data_representation", "y9_python", "y9_apps", "y9_ai", "y9_3d",
]

# Sections that are not lessons. The computational thinking unit ends by
# pointing at the adventure game, which is its own puzzle practice.
NOT_LESSONS = {("computational-thinking", "Practise it as a game")}


def units():
    """[(topic slug, [Stretch])] for every unit module written so far."""
    out = []
    for name in MODULES:
        try:
            mod = importlib.import_module("content.ks3_stretch." + name)
        except ModuleNotFoundError as e:
            if e.name != "content.ks3_stretch." + name:
                raise
            continue
        out.append((mod.TOPIC, mod.LESSONS))
    return out
