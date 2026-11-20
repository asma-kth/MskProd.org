"""OCR H446 1.5 Legal, moral, cultural and ethical issues: Code Word, Link Up and Bug Hunt."""
from mskbuild.models import Games, Word, Group, Bug

GAMES = [
    Games(
        lesson="legal-moral-and-ethical-issues",
        words=[
            Word("PATENT", "Protection for an invention, which must be applied for."),
            Word("PRIVACY", "The right to keep your personal life and data to yourself."),
            Word("VIRTUE", "The ethical approach that asks what a person of good character would do."),
        ],
        groups=[
            Group("Rights under data protection", ["Access", "Rectification", "Erasure", "Portability"]),
            Group("Protected by copyright", ["Software", "Music", "Films", "Photographs"]),
            Group("Recurring ethical themes", ["Automation", "Digital divide", "Surveillance", "Algorithmic bias"]),
        ],
        bugs=[
            Bug(["The Computer Misuse Act 1990 makes unauthorised access an offence.",
                 "A denial of service attack can break the Computer Misuse Act."],
                "The Computer Misuse Act 1990 protects music and films from copying.",
                "Copying music and films is covered by the Copyright, Designs and Patents Act 1988."),
            Bug(["Copyright arises automatically when a work is created.",
                 "A patent protects an invention."],
                "Copyright must be registered before it protects a work.",
                "Copyright needs no registration. It is a patent that must be applied for."),
            Bug(["The Data Protection Act 2018 implements GDPR in UK law.",
                 "Personal data must be kept secure."],
                "Organisations may keep personal data for as long as they like.",
                "Personal data must not be kept for longer than necessary."),
            Bug(["Consequentialism judges an action by its outcomes.",
                 "Deontology judges an action against duties and rights."],
                "Virtue ethics judges an action by its profit.",
                "Virtue ethics asks what a person of good character would do, focusing on honesty, responsibility and "
                "care."),
            Bug(["Algorithms trained on historical data can repeat historical bias.",
                 "The digital divide can exclude people from services moved online."],
                "A decision made by a computer is always free of bias.",
                "A system repeats the bias in its training data, while appearing objective."),
        ],
    ),
]
