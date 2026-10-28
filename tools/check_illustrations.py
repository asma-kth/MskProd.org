#!/usr/bin/env python3
"""Audit every drawn illustration in a real browser.

For each picture, this checks that

  * no text runs off the picture or onto other text,
  * no text spills out of the pill, tile or cell it is drawn in,
  * every piece of text has enough contrast against what is actually behind it
    (WCAG AA: 4.5 to 1, or 3 to 1 for large text), measured on a rendering of
    the picture with its text taken out.

It needs the built site (python3 build.py) for the stylesheet and fonts, plus
Playwright and Pillow:

    pip install playwright pillow && playwright install chromium
    python3 tools/check_illustrations.py                 # all pictures
    python3 tools/check_illustrations.py cpu-board mesh  # just these
    python3 tools/check_illustrations.py --no-contrast

Exits with status 1 if anything is found, so it can gate a build.
"""
import argparse
import http.server
import importlib
import io
import os
import re
import sys
import threading

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, "dist")
sys.path.insert(0, ROOT)

JS_BOXES = r"""
() => [...document.querySelectorAll('figure.illus')].map(fig => {
  const svg = fig.querySelector(':scope > .illus-art > svg');
  const sr = svg.getBoundingClientRect();
  const name = svg.getAttribute('aria-labelledby').replace(/^il-/, '').replace(/-t$/, '');
  // A line of code is one <text> made of coloured <tspan>s, so measure the pieces, not the line.
  const texts = [];
  const push = (el, owner) => {
    const r = el.getBoundingClientRect();
    const cs = getComputedStyle(el);
    let op = parseFloat(cs.opacity); let n = el.parentElement;
    while (n && n !== svg) { op *= parseFloat(getComputedStyle(n).opacity); n = n.parentElement; }
    texts.push({s: el.textContent.trim(), x: r.left - sr.left, y: r.top - sr.top, w: r.width, h: r.height,
                fill: cs.fill, op: op * parseFloat(cs.fillOpacity || 1),
                size: parseFloat(owner.getAttribute('font-size') || '0'), weight: parseInt(cs.fontWeight)});
  };
  svg.querySelectorAll('text').forEach(t => {
    const spans = [...t.querySelectorAll('tspan')];
    if (spans.length) spans.forEach(sp => { if (sp.textContent.trim()) push(sp, t); });
    else if (t.textContent.trim()) push(t, t);
  });
  const rects = [...svg.querySelectorAll('rect')].map(t => {
    const r = t.getBoundingClientRect();
    return {x: r.left - sr.left, y: r.top - sr.top, w: r.width, h: r.height, rx: parseFloat(t.getAttribute('rx') || '0')};
  }).filter(r => r.w < sr.width * .9 && r.w > 8 && r.h > 8 && r.h < sr.height * .6);
  return {name, W: sr.width, H: sr.height, texts, rects};
});
"""


def load_registry():
    from mskbuild import illus
    for f in sorted(os.listdir(os.path.join(ROOT, "mskbuild"))):
        if f.startswith("illus_") and f.endswith(".py"):
            importlib.import_module("mskbuild." + f[:-3])
    return illus.REGISTRY


class Handler(http.server.SimpleHTTPRequestHandler):
    page = b""

    def __init__(self, *a, **kw):
        super().__init__(*a, directory=DIST, **kw)

    def do_GET(self):
        if self.path.startswith("/_illus_check"):
            self.send_response(200)
            self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(Handler.page)
            return
        super().do_GET()

    def log_message(self, *a):
        pass


def serve():
    srv = http.server.ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    threading.Thread(target=srv.serve_forever, daemon=True).start()
    return srv


def lin(c):
    v = c / 255.0
    return v / 12.92 if v <= .03928 else ((v + .055) / 1.055) ** 2.4


LIN = [lin(i) for i in range(256)]


def lum(rgb):
    r, g, b = (min(255, max(0, int(round(c)))) for c in rgb)
    return .2126 * LIN[r] + .7152 * LIN[g] + .0722 * LIN[b]


def ratio(a, b):
    hi, lo = (a, b) if a >= b else (b, a)
    return (hi + .05) / (lo + .05)


def inter(a, b):
    return (min(a["x"] + a["w"], b["x"] + b["w"]) - max(a["x"], b["x"]),
            min(a["y"] + a["h"], b["y"] + b["h"]) - max(a["y"], b["y"]))


def layout_issues(fig):
    issues = []
    T, R, W, H = fig["texts"], fig["rects"], fig["W"], fig["H"]
    for t in T:
        if t["x"] < 2 or t["y"] < 0 or t["x"] + t["w"] > W - 2 or t["y"] + t["h"] > H - 1:
            issues.append("OUT      %r at (%d,%d) w=%d" % (t["s"], t["x"], t["y"], t["w"]))
    for i in range(len(T)):
        for j in range(i + 1, len(T)):
            w, h = inter(T[i], T[j])
            if w > 3 and h > .45 * min(T[i]["h"], T[j]["h"]):
                issues.append("OVERLAP  %r x %r (%.0fx%.0f)" % (T[i]["s"], T[j]["s"], w, h))
    for t in T:
        if len(t["s"]) < 2:
            continue                      # one character is a badge number
        cx, cy = t["x"] + t["w"] / 2, t["y"] + t["h"] / 2
        best = None
        for r in R:
            if r["x"] <= cx <= r["x"] + r["w"] and r["y"] <= cy <= r["y"] + r["h"] and (r["rx"] >= r["h"] / 2 - 1 or r["rx"] >= 6):
                if best is None or r["w"] * r["h"] < best["w"] * best["h"]:
                    best = r
        if best is not None and t["h"] < best["h"] * 1.6:
            over_l, over_r = best["x"] - t["x"], (t["x"] + t["w"]) - (best["x"] + best["w"])
            if over_l > 1.5 or over_r > 1.5:
                issues.append("SPILL    %r out of its %dpx box by %.1f/%.1f" % (t["s"], best["w"], over_l, over_r))
    return issues


def contrast_issues(fig, png):
    from PIL import Image
    im = Image.open(io.BytesIO(png)).convert("RGB")
    sc = im.size[0] / fig["W"]
    out = []
    for t in fig["texts"]:
        x0, x1 = int((t["x"] + t["w"] * .06) * sc), int((t["x"] + t["w"] * .94) * sc)
        y0, y1 = int((t["y"] + t["h"] * .22) * sc), int((t["y"] + t["h"] * .78) * sc)
        if x1 <= x0 or y1 <= y0:
            continue
        raw = im.crop((max(0, x0), max(0, y0), x1, y1)).tobytes()
        reg = [(raw[i], raw[i + 1], raw[i + 2]) for i in range(0, len(raw) - 2, 9)]
        if not reg:
            continue
        nums = [float(v) for v in re.findall(r"[\d.]+", t["fill"])[:3]]
        a = t["op"]
        rs = sorted(ratio(lum([nums[k] * a + p[k] * (1 - a) for k in range(3)]), lum(p)) for p in reg)
        low = rs[int(len(rs) * .12)]
        px = t["size"] * (fig["W"] / 800)
        need = 3.0 if (px >= 24 or (px >= 18.66 and t["weight"] >= 700)) else 4.5
        if low < need:
            out.append("CONTRAST %.2f < %.1f  %r  size %s fill %s" % (low, need, t["s"][:34], t["size"], t["fill"]))
    return out


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("names", nargs="*", help="illustrations to check (default: all)")
    ap.add_argument("--no-contrast", action="store_true", help="skip the contrast measurement")
    args = ap.parse_args()
    if not os.path.isdir(os.path.join(DIST, "assets")):
        sys.exit("dist/ is missing: run python3 build.py first")
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit("needs Playwright: pip install playwright pillow && playwright install chromium")

    reg = load_registry()
    names = args.names or sorted(k for k in reg if not k.startswith("_"))
    unknown = [n for n in names if n not in reg]
    if unknown:
        sys.exit("unknown illustration(s): %s" % ", ".join(unknown))
    body = "\n".join(reg[n]() for n in names)
    srv = serve()
    port = srv.server_address[1]
    total = 0
    chrome = "/opt/pw-browsers/chromium"
    with sync_playwright() as p:
        kw = {"executable_path": chrome} if os.path.exists(chrome) else {}
        b = p.chromium.launch(**kw)
        Handler.page = (
            '<!doctype html><html lang="en-GB"><head><meta charset="utf-8">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<link rel="stylesheet" href="/assets/css/site.css"></head>'
            '<body style="padding:20px"><div style="width:880px;margin:0 auto">%s</div></body></html>'
            % body).encode("utf-8")
        pg = b.new_page(viewport={"width": 960, "height": 900}, device_scale_factor=2)
        pg.goto("http://127.0.0.1:%d/_illus_check" % port, wait_until="load")
        pg.wait_for_timeout(500)
        data = pg.evaluate(JS_BOXES)
        found = {f["name"]: layout_issues(f) for f in data}
        if not args.no_contrast:
            pg.add_style_tag(content=".illus text{visibility:hidden !important}")
            pg.wait_for_timeout(150)
            svgs = pg.locator("figure.illus > .illus-art > svg")
            for i, f in enumerate(data):
                found[f["name"]] += contrast_issues(f, svgs.nth(i).screenshot())
        pg.close()
        n = sum(len(v) for v in found.values())
        total += n
        for name, issues in found.items():
            if issues:
                print("== %s" % name)
                for s in issues:
                    print("     " + s)
        print("%d pictures, %d issues" % (len(data), n))
        b.close()
    srv.shutdown()
    sys.exit(1 if total else 0)


if __name__ == "__main__":
    main()
