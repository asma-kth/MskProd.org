/* Correlation lab: add points, move them, and watch r and the line respond.
 *
 * Correlation is taught as a number and understood as a shape. Here the
 * student builds the shape: click to add a point, drag to move one, and the
 * coefficient, the fitted line and the strength description update as they go.
 * The outlier preset exists because a single point moving r from 0.1 to 0.8 is
 * the most convincing argument there is for plotting your data first.
 */
(function () {
  "use strict";

  var W = 420, H = 300, PAD = 34;

  function el(tag, cls, txt) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (txt !== undefined && txt !== null) n.textContent = txt;
    return n;
  }

  function uid() { return Math.random().toString(36).slice(2, 8); }

  function rng(seed) {
    var s = seed;
    return function () {
      s = (s * 1103515245 + 12345) % 2147483648;
      return s / 2147483648;
    };
  }

  function gen(kind) {
    var r = rng(kind.seed), pts = [], i, x, y, n = kind.n;
    for (i = 0; i < n; i++) {
      x = 0.06 + 0.88 * r();
      y = kind.fn(x, r() - 0.5);
      pts.push({ x: x, y: Math.min(0.97, Math.max(0.03, y)) });
    }
    if (kind.outlier) pts.push({ x: kind.outlier[0], y: kind.outlier[1] });
    return pts;
  }

  var PRESETS = {
    positive: {
      label: "Strong positive", seed: 7, n: 26,
      fn: function (x, e) { return 0.12 + 0.78 * x + e * 0.22; },
      note: "Spend against sales. As one rises so does the other, which is "
          + "what a strong positive correlation looks like."
    },
    weak: {
      label: "Weak", seed: 15, n: 26,
      fn: function (x, e) { return 0.28 + 0.46 * x + e * 0.5; },
      note: "There is a relationship, and it is far too loose to predict a "
          + "single case from. A weak correlation is not a licence to forecast."
    },
    none: {
      label: "None", seed: 29, n: 26,
      fn: function (x, e) { return 0.5 + e * 0.84; },
      note: "No direction at all. Knowing one variable tells you nothing "
          + "about the other, so r sits near zero."
    },
    negative: {
      label: "Strong negative", seed: 37, n: 26,
      fn: function (x, e) { return 0.88 - 0.78 * x + e * 0.22; },
      note: "Price against units sold. A negative correlation is just as "
          + "strong and just as useful as a positive one."
    },
    outlier: {
      label: "One outlier", seed: 51, n: 18,
      fn: function (x, e) { return 0.26 + 0.05 * x + e * 0.18; },
      outlier: [0.96, 0.95],
      note: "The cloud on the left has almost no relationship. The single "
          + "point in the top right is doing nearly all of the work. Delete "
          + "it and watch r collapse."
    },
    spurious: {
      label: "Spurious", seed: 61, n: 26,
      fn: function (x, e) { return 0.1 + 0.8 * x + e * 0.18; },
      note: "Ice cream sales against drowning deaths. The correlation is as "
          + "strong as the first preset and there is no causal link at all: "
          + "hot weather causes both."
    }
  };

  function stats(pts) {
    var n = pts.length, i, mx = 0, my = 0, sxy = 0, sxx = 0, syy = 0;
    if (n < 2) return null;
    for (i = 0; i < n; i++) { mx += pts[i].x; my += pts[i].y; }
    mx /= n; my /= n;
    for (i = 0; i < n; i++) {
      sxy += (pts[i].x - mx) * (pts[i].y - my);
      sxx += (pts[i].x - mx) * (pts[i].x - mx);
      syy += (pts[i].y - my) * (pts[i].y - my);
    }
    if (sxx === 0 || syy === 0) return null;
    var r = sxy / Math.sqrt(sxx * syy);
    var m = sxy / sxx;
    return { r: r, m: m, c: my - m * mx, n: n };
  }

  function strength(r) {
    var a = Math.abs(r);
    var dir = r > 0 ? "positive" : "negative";
    if (a < 0.1) return "no correlation";
    if (a < 0.3) return "a very weak " + dir + " correlation";
    if (a < 0.5) return "a weak " + dir + " correlation";
    if (a < 0.7) return "a moderate " + dir + " correlation";
    if (a < 0.9) return "a strong " + dir + " correlation";
    return "a very strong " + dir + " correlation";
  }

  function build(body) {
    body.textContent = "";
    var pts = gen(PRESETS.positive);
    var presetKey = "positive";
    var dragging = -1;

    var btns = el("div", "tool-btns");
    Object.keys(PRESETS).forEach(function (k) {
      var b = el("button", "tool-btn", PRESETS[k].label);
      b.type = "button";
      b.addEventListener("click", function () {
        presetKey = k;
        pts = gen(PRESETS[k]);
        render();
      });
      btns.appendChild(b);
    });
    var clear = el("button", "tool-btn", "Clear");
    clear.type = "button";
    clear.addEventListener("click", function () {
      pts = []; presetKey = null; render();
    });
    btns.appendChild(clear);

    var wrap = el("div", "cl-wrap");
    var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("viewBox", "0 0 " + W + " " + H);
    svg.setAttribute("class", "cl-plot");
    svg.setAttribute("role", "img");
    wrap.appendChild(svg);

    var side = el("div", "cl-side");
    var rBig = el("div", "cl-r");
    var rVal = el("strong", "cl-r-val", "–");
    var rWord = el("span", "cl-r-word", "");
    rBig.appendChild(el("span", "cl-r-name", "r"));
    rBig.appendChild(rVal);
    rBig.appendChild(rWord);
    var eqn = el("p", "cl-eqn");
    var count = el("p", "cl-count");
    side.appendChild(rBig);
    side.appendChild(eqn);
    side.appendChild(count);
    wrap.appendChild(side);

    var note = el("p", "tool-note");
    var warn = el("p", "cl-warn");
    warn.textContent = "r measures how closely the points follow a straight "
      + "line. It says nothing about which variable causes the other, or "
      + "whether either does.";
    var live = el("p", "tool-status");
    live.setAttribute("role", "status");
    live.setAttribute("aria-live", "polite");

    var hint = el("p", "tool-note cl-hint");
    hint.textContent = "Click the grid to add a point. Drag a point to move "
      + "it. Shift-click a point to delete it.";

    function sx(x) { return PAD + x * (W - PAD - 14); }
    function sy(y) { return (H - PAD) - y * (H - PAD - 14); }
    function ux(px) { return (px - PAD) / (W - PAD - 14); }
    function uy(py) { return ((H - PAD) - py) / (H - PAD - 14); }

    function render() {
      var s = stats(pts), i, parts = [];
      parts.push('<rect class="cl-bg" x="' + PAD + '" y="14" width="'
                 + (W - PAD - 14) + '" height="' + (H - PAD - 14) + '"/>');
      for (i = 1; i < 4; i++) {
        parts.push('<line class="cl-grid" x1="' + sx(i / 4) + '" y1="14" x2="'
                   + sx(i / 4) + '" y2="' + (H - PAD) + '"/>');
        parts.push('<line class="cl-grid" x1="' + PAD + '" y1="' + sy(i / 4)
                   + '" x2="' + (W - 14) + '" y2="' + sy(i / 4) + '"/>');
      }
      parts.push('<line class="cl-axis" x1="' + PAD + '" y1="' + (H - PAD)
                 + '" x2="' + (W - 14) + '" y2="' + (H - PAD) + '"/>');
      parts.push('<line class="cl-axis" x1="' + PAD + '" y1="14" x2="' + PAD
                 + '" y2="' + (H - PAD) + '"/>');
      if (s) {
        var y0 = s.c, y1 = s.m + s.c;
        /* Clip the fitted line to the plot rather than letting it run out. */
        parts.push('<line class="cl-fit" x1="' + sx(0) + '" y1="' + sy(y0)
                   + '" x2="' + sx(1) + '" y2="' + sy(y1) + '"/>');
      }
      for (i = 0; i < pts.length; i++) {
        parts.push('<circle class="cl-pt" data-i="' + i + '" cx="'
                   + sx(pts[i].x).toFixed(1) + '" cy="' + sy(pts[i].y).toFixed(1)
                   + '" r="6"/>');
      }
      parts.push('<text class="cl-lab" x="' + ((W + PAD) / 2) + '" y="'
                 + (H - 6) + '" text-anchor="middle">variable x</text>');
      parts.push('<text class="cl-lab" x="12" y="' + ((H - PAD) / 2)
                 + '" text-anchor="middle" transform="rotate(-90 12 '
                 + ((H - PAD) / 2) + ')">variable y</text>');
      svg.innerHTML = parts.join("");

      if (s) {
        rVal.textContent = (s.r < 0 ? "−" : "+")
          + Math.abs(s.r).toFixed(2);
        rWord.textContent = strength(s.r);
        eqn.innerHTML = "line of best fit: <code>y = "
          + s.m.toFixed(2) + "x " + (s.c < 0 ? "− " : "+ ")
          + Math.abs(s.c).toFixed(2) + "</code>";
        live.textContent = "r is " + s.r.toFixed(2) + ", which is "
          + strength(s.r) + ", from " + s.n + " points.";
      } else {
        rVal.textContent = "–";
        rWord.textContent = pts.length < 2 ? "add at least two points"
                                           : "no variation to measure";
        eqn.textContent = "";
        live.textContent = "Not enough points to calculate r.";
      }
      count.textContent = pts.length + (pts.length === 1 ? " point" : " points");
      svg.setAttribute("aria-label", "Scatter plot of " + pts.length
        + " points with a line of best fit. "
        + (s ? "r is " + s.r.toFixed(2) + ", " + strength(s.r) + "."
             : "Not enough points to calculate r."));
      note.textContent = presetKey ? PRESETS[presetKey].note
        : "Your own points. Watch what happens to r when you drag one a long "
        + "way from the rest.";
    }

    function local(ev) {
      var box = svg.getBoundingClientRect();
      var t = ev.touches && ev.touches[0] ? ev.touches[0] : ev;
      return {
        x: (t.clientX - box.left) / box.width * W,
        y: (t.clientY - box.top) / box.height * H
      };
    }

    function nearest(p) {
      var best = -1, bd = 14 * 14, i, dx, dy, d;
      for (i = 0; i < pts.length; i++) {
        dx = sx(pts[i].x) - p.x; dy = sy(pts[i].y) - p.y;
        d = dx * dx + dy * dy;
        if (d < bd) { bd = d; best = i; }
      }
      return best;
    }

    svg.addEventListener("pointerdown", function (ev) {
      var p = local(ev), i = nearest(p);
      if (i >= 0 && ev.shiftKey) {
        pts.splice(i, 1); presetKey = null; render(); return;
      }
      if (i >= 0) {
        dragging = i;
        svg.setPointerCapture(ev.pointerId);
        return;
      }
      var ux_ = ux(p.x), uy_ = uy(p.y);
      if (ux_ < 0 || ux_ > 1 || uy_ < 0 || uy_ > 1) return;
      pts.push({ x: ux_, y: uy_ });
      presetKey = null;
      render();
    });

    svg.addEventListener("pointermove", function (ev) {
      if (dragging < 0) return;
      var p = local(ev);
      pts[dragging] = {
        x: Math.min(1, Math.max(0, ux(p.x))),
        y: Math.min(1, Math.max(0, uy(p.y)))
      };
      presetKey = null;
      render();
    });

    svg.addEventListener("pointerup", function () { dragging = -1; });
    svg.addEventListener("pointercancel", function () { dragging = -1; });

    body.appendChild(btns);
    body.appendChild(wrap);
    body.appendChild(note);
    body.appendChild(hint);
    body.appendChild(warn);
    body.appendChild(live);
    render();
  }

  function init() {
    var mounts = document.querySelectorAll('.tool[data-tool="correlation-lab"]');
    Array.prototype.forEach.call(mounts, function (m) {
      var b = m.querySelector(".tool-body");
      if (b) build(b);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else { init(); }
})();
