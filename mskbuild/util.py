"""Helpers shared by modules that cannot import each other.

render.py imports markup.py, so anything both of them need has to live
somewhere neither one owns.
"""
import re


def slugify(s: str) -> str:
    s = re.sub(r"[^a-z0-9]+", "-", str(s).lower()).strip("-")
    return s or "section"
