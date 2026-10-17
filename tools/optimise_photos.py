#!/usr/bin/env python3
"""Turn original photographs into the files the site serves.

Run it after dropping originals into photos-incoming/, named for their slug in
mskbuild/photos.py, in any format Pillow reads:

    python3 tools/optimise_photos.py

For each original it writes static/img/photos/<slug>.webp at a sensible width
and records the dimensions in index.json, which the build reads so every
<img> carries width and height and the page never jumps while loading.

This is deliberately a separate script rather than part of build.py: the
outputs are committed, so a normal build needs no image library at all.
"""
import json
import os
import sys

try:
    from PIL import Image
except ImportError:
    sys.exit("This script needs Pillow:  pip install Pillow")

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "photos-incoming")
OUT = os.path.join(ROOT, "static", "img", "photos")
INDEX = os.path.join(OUT, "index.json")

# Wide enough to stay sharp on a high density screen at the width the figure
# is actually displayed, and no wider. Photographs are the heaviest thing on
# a page and this site is read on phones.
MAX_W = 1200
QUALITY = 80


def main():
    os.makedirs(OUT, exist_ok=True)
    if not os.path.isdir(SRC):
        sys.exit("No photos-incoming/ directory. Put the originals there, one "
                 "per slug, e.g. photos-incoming/cpu-chip.jpg")

    sys.path.insert(0, ROOT)
    from mskbuild.photos import PHOTOS

    try:
        with open(INDEX, encoding="utf-8") as fh:
            index = json.load(fh)
    except (OSError, ValueError):
        index = {}

    done, unknown = 0, []
    for name in sorted(os.listdir(SRC)):
        slug, ext = os.path.splitext(name)
        if ext.lower() not in (".jpg", ".jpeg", ".png", ".webp", ".tif", ".tiff"):
            continue
        if slug not in PHOTOS:
            unknown.append(name)
            continue
        im = Image.open(os.path.join(SRC, name))
        im = im.convert("RGB")
        if im.width > MAX_W:
            im = im.resize((MAX_W, round(im.height * MAX_W / im.width)),
                           Image.LANCZOS)
        dest = os.path.join(OUT, slug + ".webp")
        im.save(dest, "WEBP", quality=QUALITY, method=6)
        index[slug] = {"w": im.width, "h": im.height}
        print("  %-18s %4d x %-4d  %5.0f KB" %
              (slug, im.width, im.height, os.path.getsize(dest) / 1024))
        done += 1

    with open(INDEX, "w", encoding="utf-8") as fh:
        json.dump(dict(sorted(index.items())), fh, indent=1)
        fh.write("\n")

    print("\n%d written into static/img/photos/" % done)
    if unknown:
        print("Ignored, no matching slug in mskbuild/photos.py: %s"
              % ", ".join(unknown))
    missing = sorted(s for s in PHOTOS if s not in index)
    if missing:
        print("Still needed (%d): %s" % (len(missing), ", ".join(missing)))


if __name__ == "__main__":
    main()
