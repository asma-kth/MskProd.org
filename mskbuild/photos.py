"""Photographs of real hardware, for the topics that describe real objects.

A diagram shows how a thing works; a photograph shows what it looks like when
you are holding it. For hardware topics the exam genuinely asks students to
recognise and compare physical devices, so both earn their place: the 3D scene
for the mechanism, the photograph for the object.

Every entry here records where the picture came from and under what licence,
because the site carries advertising and so counts as commercial use. Only
licences that permit that are allowed, the credit is printed under the
picture, and /attributions/ lists the lot in one place.

The image files themselves are not in the repository yet. An entry whose file
is missing is skipped at build time and reported, so the placements below can
be written in advance and a photograph starts appearing on every one of its
topics the moment the file lands. tools/optimise_photos.py turns an original
into the sizes the site serves and writes the dimensions this module reads.
"""
import json
import os

from .svg import esc

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Where optimised photographs live, relative to the built site.
DIR = "/assets/img/photos"

# Written by tools/optimise_photos.py: {slug: {"w": int, "h": int}}.
_INDEX = None


def _index():
    global _INDEX
    if _INDEX is None:
        path = os.path.join(ROOT, "static", "img", "photos", "index.json")
        try:
            with open(path, encoding="utf-8") as fh:
                _INDEX = json.load(fh)
        except (OSError, ValueError):
            _INDEX = {}
    return _INDEX


class Photo:
    """One photograph, with everything needed to publish it lawfully."""

    def __init__(self, slug, alt, caption, credit, licence, source):
        self.slug = slug
        self.alt = alt              # what the picture shows, for a screen reader
        self.caption = caption      # what the reader should notice in it
        self.credit = credit        # photographer or institution
        self.licence = licence      # must permit commercial use
        self.source = source        # where it came from, so it can be checked


def P(slug, alt, caption, credit="", licence="", source=""):
    return Photo(slug, alt, caption, credit, licence, source)


# --------------------------------------------------------------- the shot list
#
# Each of these is a photograph the hardware topics need. Alt text and caption
# are written now because they are teaching, not decoration: the caption says
# what to look at, and the alt text describes the object for somebody who
# cannot see it. Credit and licence are filled in when the file is sourced.

PHOTOS = {p.slug: p for p in [
    P("cpu-chip",
      "A processor chip lying face up out of its socket, with the heat spreader "
      "on top and hundreds of gold contact pads covering the underside.",
      "The metal lid is a heat spreader, not the processor. The silicon doing the "
      "work is a square a few millimetres across underneath it."),
    P("motherboard",
      "A desktop motherboard seen from above, showing the square processor socket, "
      "four long memory slots beside it, expansion slots along the bottom edge and "
      "the chipset heatsinks.",
      "Every component plugs into this one board, and the tracks between them are "
      "the buses."),
    P("ram-stick",
      "A stick of DDR memory: a long green circuit board with eight black memory "
      "chips in a row and a gold edge connector with a notch off centre.",
      "The notch is in a different place on each generation of memory, so a DDR4 "
      "stick physically will not fit a DDR5 slot."),
    P("rom-chip",
      "A small rectangular flash memory chip soldered to a motherboard, holding "
      "the firmware the computer runs before the operating system loads.",
      "This chip holds the firmware. It keeps its contents with the power off, "
      "which is what makes it read only memory rather than RAM."),
    P("hdd-open",
      "A hard disk drive with the lid removed, showing the mirrored circular "
      "platter, the pivoting actuator arm reaching across it and the read write "
      "head at the tip of the arm.",
      "The head never touches the platter. It floats a few nanometres above a "
      "surface spinning at 7,200 revolutions a minute, which is why a knock while "
      "it is running destroys the drive."),
    P("ssd-open",
      "A solid state drive with its case opened, showing a circuit board carrying "
      "several flash memory chips and a controller chip, with no moving parts.",
      "Nothing in here moves. That single fact explains the speed, the silence, "
      "the power saving and the durability all at once."),
    P("usb-and-disc",
      "A USB flash drive beside an optical disc, showing the two portable storage "
      "formats side by side.",
      "Both are secondary storage, and both are chosen for being portable rather "
      "than for being fast."),
    P("gpu-card",
      "A graphics card removed from a computer, showing the large cooling fans, "
      "the heatsink underneath them and the display connectors along the bracket.",
      "Most of the card is cooling. The processor underneath has thousands of "
      "small cores all doing the same kind of calculation."),
    P("heatsink-fan",
      "A processor cooler: a block of metal fins with a fan mounted on top, sitting "
      "on a motherboard above the processor socket.",
      "A faster clock speed makes more heat, and heat is the limit. This is why "
      "processors gained cores instead of gigahertz."),
    P("network-switch",
      "A rack mounted network switch, a flat metal box with two rows of numbered "
      "Ethernet ports along the front, each with a small status light.",
      "One port per device. That is a star topology, and this is the thing in the "
      "middle of it."),
    P("home-router",
      "A domestic broadband router with external aerials, Ethernet ports on the "
      "back and status lights on the front.",
      "A home router is several devices in one box: a router, a switch, a wireless "
      "access point and usually a modem and firewall."),
    P("ethernet-cable",
      "The end of an Ethernet cable, showing the transparent RJ45 plug with eight "
      "coloured copper wires visible inside it, twisted into four pairs.",
      "The pairs are twisted to cancel out interference. That is the whole reason "
      "for the name twisted pair."),
    P("fibre-optic",
      "Fibre optic cable with the jacket cut back, showing hair thin glass strands "
      "carrying points of light at their ends.",
      "Light down glass, not electricity down copper. It goes further and faster "
      "and nothing electrical nearby can interfere with it."),
    P("nic-card",
      "A network interface card: a small circuit board with an Ethernet socket on "
      "its metal bracket and a controller chip on the board.",
      "Every device on a network needs one of these, and the MAC address is burned "
      "into it at the factory."),
    P("embedded-board",
      "A small single board computer the size of a bank card, with the processor, "
      "memory and connectors all on one board.",
      "One board, one job, no hard disk and no operating system to load. That is "
      "why it boots instantly and costs very little."),
    P("server-rack",
      "A rack of servers in a data centre, with rows of identical units stacked in "
      "a cabinet and cabling running down the side.",
      "When a website is described as being in the cloud, this is the cloud."),
    P("peripherals",
      "A desk with a keyboard, mouse, microphone and printer, the everyday input "
      "and output devices of a computer system.",
      "Input brings data in, output sends results back out. Classify by the job it "
      "does, not by what it looks like."),
]}


def available():
    """The photographs whose files are actually present."""
    idx = _index()
    return {s: p for s, p in PHOTOS.items() if s in idx}


def pending():
    idx = _index()
    return sorted(s for s in PHOTOS if s not in idx)


def render(slug):
    """One photograph as a figure, or nothing if the file is not here yet."""
    if slug not in PHOTOS:
        raise KeyError("unknown photo %r (have: %s)"
                       % (slug, ", ".join(sorted(PHOTOS))))
    meta = _index().get(slug)
    if not meta:
        return ""
    p = PHOTOS[slug]
    credit = ""
    if p.credit or p.licence:
        credit = ('<span class="photo-credit">%s</span>'
                  % esc(" · ".join(x for x in (p.credit, p.licence) if x)))
    return (
        '<figure class="photo">'
        '<img src="%s/%s.webp" width="%d" height="%d" loading="lazy" '
        'decoding="async" alt="%s">'
        '<figcaption>%s%s</figcaption></figure>'
        % (DIR, esc(slug), meta["w"], meta["h"], esc(p.alt),
           esc(p.caption), credit))
