"""Content model for the MskProd Computing revision site."""
from dataclasses import dataclass, field
from typing import List, Tuple, Optional


@dataclass
class Q:
    """One multiple choice knowledge-check question."""
    stem: str
    options: List[str]
    answer: int          # index of the correct option
    explain: str         # shown after answering, whatever the student picked


@dataclass
class MP:
    """One mark point in a mark scheme.

    `text` is what the examiner is looking for, written the way a real mark
    scheme writes it. `any` lists acceptable phrasings the auto marker will
    accept for that point.
    """
    text: str
    any: List[str]


@dataclass
class EQ:
    """One exam-style extended answer question."""
    stem: str
    marks: int
    points: List[MP]
    model: str
    command: str = ""     # describe / explain / compare / justify ...


@dataclass
class Section:
    title: str
    body: str            # mini-markup, parsed at build time
    id: str = ""


@dataclass
class Topic:
    slug: str
    title: str
    blurb: str
    sections: List[Section]
    quiz: List[Q] = field(default_factory=list)
    exam: List[EQ] = field(default_factory=list)
    spec: str = ""
    icon: str = "i-book"
    keyterms: List[Tuple[str, str]] = field(default_factory=list)
    grade: str = ""            # how to reach the top grade on this topic
    mistakes: List[str] = field(default_factory=list)
    fact: str = ""             # a Pixel fun fact tied to this topic
    minutes: int = 25


@dataclass
class Unit:
    slug: str
    title: str
    blurb: str
    topics: List[Topic]
    icon: str = "i-book"
    term: str = ""             # eg "Year 7, Autumn 1"


@dataclass
class Course:
    slug: str
    title: str
    short: str
    blurb: str
    intro: str
    units: List[Unit]
    icon: str = "i-book"
    accent: str = "var(--teal)"
    stage: str = ""            # KS3 / KS4 / KS5
    board: str = ""
    code: str = ""
    goal: str = ""             # the top grade for this course
    journey: List[Tuple[str, str, str]] = field(default_factory=list)
