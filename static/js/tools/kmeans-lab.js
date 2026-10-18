/* k-means lab: place points, drop in centroids, and run k-means one half step
 * at a time.
 *
 * The algorithm is two sentences long, and students still misremember which
 * half moves what. Here every press of Assign recolours the points and every
 * press of Update slides the crosses, with the regions each centroid owns
 * shaded behind them. The elbow chart answers the question every k-means
 * lesson ends on: how do you choose k?
 */
(function () {
  "use strict";

  var W = 420, H = 300, PAD = 12;
  var COLS = ["#6D28D9", "#C2410C", "#0F766E", "#BE185D", "#1D4ED8", "#15803D"];
  var NS = "http://www.w3.org/2000/svg";

  function el(tag, cls, txt) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (txt !== undefined && txt !== null) n.textContent = txt;
    return n;
  }
  function sv(tag, attrs) {
    var n = document.createElementNS(NS, tag), k;
    for (k in attrs) n.setAttribute(k, attrs[k]);
    return n;
  }
  function rng(seed) {
    var s = seed % 2147483647;
    if (s <= 0) s += 2147483646;
    return function () { s = s * 16807 % 2147483647; return (s - 1) / 2147483646; };
  }
  function d2(a, b) { var dx = a.x - b.x, dy = a.y - b.y; return dx * dx + dy * dy; }

  function blobs(seed, centres, n, spread) {
    var r = rng(seed), out = [], i, c, a, rad;
    for (i = 0; i < n; i++) {
      c = centres[i % centres.length];
      a = r() * Math.PI * 2;
      rad = spread * Math.sqrt(-2 * Math.log(1 - r() * 0.98)) * 0.6;
      out.push({ x: clamp(c[0] + Math.cos(a) * rad), y: clamp(c[1] + Math.sin(a) * rad) });
    }
    return out;
  }
  function clamp(v) { return Math.min(0.97, Math.max(0.03, v)); }

  var PRESETS = {
    three: { label: "Three groups", k: 3, make: function () {
      return blobs(11, [[0.22, 0.28], [0.75, 0.3], [0.5, 0.76]], 45, 0.09); },
      note: "Three clear groups. Try a bad start (Shuffle start) and watch k-means still find them." },
    four: { label: "Four groups", k: 4, make: function () {
      return blobs(23, [[0.2, 0.22], [0.8, 0.2], [0.22, 0.8], [0.78, 0.78]], 56, 0.08); },
      note: "Four groups. Set k to 3 and two groups must share a centroid; set k to 6 and a group gets split." },
    uneven: { label: "Uneven sizes", k: 2, make: function () {
      return blobs(5, [[0.3, 0.5]], 40, 0.17).concat(blobs(9, [[0.82, 0.5]], 8, 0.04)); },
      note: "One big spread-out group and one small tight one. k-means prefers equal-sized round clusters, so the boundary lands in the wrong place." },
    rings: { label: "Ring", k: 2, make: function () {
      var r = rng(3), out = [], i, a, rad;
      for (i = 0; i < 18; i++) { a = r() * 6.283; rad = r() * 0.07;
        out.push({ x: 0.5 + Math.cos(a) * rad, y: 0.5 + Math.sin(a) * rad }); }
      for (i = 0; i < 40; i++) { a = r() * 6.283; rad = 0.3 + r() * 0.06;
        out.push({ x: clamp(0.5 + Math.cos(a) * rad), y: clamp(0.5 + Math.sin(a) * rad * 0.9) }); }
      return out; },
      note: "A dot inside a ring. People see two groups. k-means cannot, because it cuts space into straight-edged regions around centres." },
    random: { label: "No groups", k: 3, make: function () {
      var r = rng(41), out = [], i;
      for (i = 0; i < 50; i++) out.push({ x: clamp(r()), y: clamp(r()) });
      return out; },
      note: "Pure noise. k-means will still report k neat clusters. Clustering always finds clusters, so a person must judge whether they mean anything." }
  };

  function inertia(pts, cents, assign) {
    var s = 0, i;
    for (i = 0; i < pts.length; i++) s += d2(pts[i], cents[assign[i]]);
    return s;
  }
  function nearest(p, cents) {
    var best = 0, bd = Infinity, i, d;
    for (i = 0; i < cents.length; i++) { d = d2(p, cents[i]); if (d < bd) { bd = d; best = i; } }
    return best;
  }
  function runKmeans(pts, k, seed) {
    var r = rng(seed), cents = [], used = {}, i, j, assign, guard, changed, sx, sy, n;
    if (pts.length < k) return Infinity;
    while (cents.length < k) {
      j = Math.floor(r() * pts.length);
      if (!used[j]) { used[j] = 1; cents.push({ x: pts[j].x, y: pts[j].y }); }
    }
    for (guard = 0; guard < 60; guard++) {
      assign = pts.map(function (p) { return nearest(p, cents); });
      changed = false;
      for (i = 0; i < k; i++) {
        sx = 0; sy = 0; n = 0;
        for (j = 0; j < pts.length; j++) if (assign[j] === i) { sx += pts[j].x; sy += pts[j].y; n++; }
        if (n && (Math.abs(sx / n - cents[i].x) > 1e-9 || Math.abs(sy / n - cents[i].y) > 1e-9)) {
          cents[i] = { x: sx / n, y: sy / n }; changed = true;
        }
      }
      if (!changed) break;
    }
    return inertia(pts, cents, assign);
  }

  function build(body) {
    body.textContent = "";
    var st = { pts: PRESETS.three.make(), k: 3, cents: [], assign: null, round: 0,
               phase: "none", seed: 7, timer: null, preset: "three" };

    var row = el("div", "tool-row");
    var fk = el("div", "tool-field");
    var kid = "km-k-" + Math.random().toString(36).slice(2, 7);
    var lk = el("label", null, "Clusters, k"); lk.setAttribute("for", kid);
    var sk = el("select"); sk.id = kid;
    [2, 3, 4, 5, 6].forEach(function (v) {
      var o = el("option", null, String(v)); o.value = String(v); sk.appendChild(o);
    });
    sk.value = "3";
    fk.appendChild(lk); fk.appendChild(sk);
    var fp = el("div", "tool-field");
    var pid = "km-p-" + Math.random().toString(36).slice(2, 7);
    var lp = el("label", null, "Data"); lp.setAttribute("for", pid);
    var sp = el("select"); sp.id = pid;
    Object.keys(PRESETS).forEach(function (key) {
      var o = el("option", null, PRESETS[key].label); o.value = key; sp.appendChild(o);
    });
    var oc = el("option", null, "Empty: click to add"); oc.value = "empty"; sp.appendChild(oc);
    fp.appendChild(lp); fp.appendChild(sp);
    row.appendChild(fp); row.appendChild(fk);

    var btns = el("div", "tool-btns");
    function button(label, primary) {
      var b = el("button", "tool-btn" + (primary ? " is-primary" : ""), label);
      b.type = "button"; btns.appendChild(b); return b;
    }
    var bPlace = button("1. Place centroids", true);
    var bAssign = button("2. Assign");
    var bUpdate = button("3. Update");
    var bRun = button("Run to the end");
    var bShuffle = button("Shuffle start");

    var wrap = el("div", "km-wrap");
    var svg = sv("svg", { viewBox: "0 0 " + W + " " + H, "class": "km-plot", role: "img",
                          "aria-label": "Scatter plot of points coloured by cluster" });
    var side = el("div", "km-side");
    var stats = el("div", "km-stats");
    var sRound = el("div", "km-stat"); var sIn = el("div", "km-stat");
    stats.appendChild(sRound); stats.appendChild(sIn);
    var elbowBtn = el("button", "tool-btn", "Elbow chart: try k = 1 to 6");
    elbowBtn.type = "button";
    var elbow = el("div", "km-elbow");
    side.appendChild(stats); side.appendChild(elbowBtn); side.appendChild(elbow);
    wrap.appendChild(svg); wrap.appendChild(side);

    var status = el("p", "tool-status"); status.setAttribute("role", "status");
    status.setAttribute("aria-live", "polite");
    var note = el("p", "tool-note");
    var hint = el("p", "tool-note km-hint",
      "Click the plot to add a point, Shift and click to remove one. Assign colours every point by its nearest centroid; Update moves each centroid to the middle of its colour.");

    function setStatus(t) { status.textContent = t; }
    function stop() { if (st.timer) { clearInterval(st.timer); st.timer = null; bRun.textContent = "Run to the end"; } }

    function place() {
      stop();
      var r = rng(st.seed), used = {}, j, guard = 0;
      st.cents = [];
      if (st.pts.length < st.k) { setStatus("Add at least " + st.k + " points first."); render(); return; }
      while (st.cents.length < st.k && guard++ < 500) {
        j = Math.floor(r() * st.pts.length);
        if (!used[j]) { used[j] = 1; st.cents.push({ x: st.pts[j].x, y: st.pts[j].y }); }
      }
      st.assign = null; st.round = 0; st.phase = "placed";
      setStatus("Centroids placed on " + st.k + " random points. Now assign.");
      render();
    }
    function assign() {
      if (!st.cents.length) { place(); return false; }
      var before = st.assign ? st.assign.join(",") : "";
      st.assign = st.pts.map(function (p) { return nearest(p, st.cents); });
      st.round += 1; st.phase = "assigned";
      var same = before === st.assign.join(",");
      setStatus("Round " + st.round + ", assign: every point joins its nearest centroid." +
                (same && st.round > 1 ? " No point changed colour." : ""));
      render();
      return !same;
    }
    function update() {
      if (st.phase !== "assigned") { return assign(); }
      var moved = 0, i, j, sx, sy, n;
      for (i = 0; i < st.cents.length; i++) {
        sx = 0; sy = 0; n = 0;
        for (j = 0; j < st.pts.length; j++) if (st.assign[j] === i) { sx += st.pts[j].x; sy += st.pts[j].y; n++; }
        if (n) {
          var nx = sx / n, ny = sy / n;
          if (Math.abs(nx - st.cents[i].x) > 1e-9 || Math.abs(ny - st.cents[i].y) > 1e-9) moved++;
          st.cents[i] = { x: nx, y: ny };
        }
      }
      st.phase = "updated";
      setStatus(moved ? "Round " + st.round + ", update: " + moved + " centroid" + (moved === 1 ? "" : "s") +
                " moved to the mean of " + (moved === 1 ? "its" : "their") + " points."
                : "Converged after " + st.round + " rounds: no centroid moved, so k-means stops.");
      render();
      return moved > 0;
    }
    function stepOnce() {
      if (!st.cents.length) { place(); return true; }
      if (st.phase === "assigned") return update();
      assign(); return true;
    }

    function render() {
      while (svg.firstChild) svg.removeChild(svg.firstChild);
      svg.appendChild(sv("rect", { x: 0, y: 0, width: W, height: H, rx: 10, "class": "km-bg" }));
      var sx = function (v) { return PAD + v * (W - 2 * PAD); };
      var sy = function (v) { return PAD + v * (H - 2 * PAD); };
      if (st.cents.length) {
        // each centroid's region is the rectangle cut down by the half-planes
        // nearer to it than to every other centroid: an exact Voronoi cell
        st.cents.forEach(function (c, i) {
          var poly = [[0, 0], [1, 0], [1, 1], [0, 1]];
          st.cents.forEach(function (o, j) {
            if (i === j || !poly.length) return;
            var nx = o.x - c.x, ny = o.y - c.y, mx = (o.x + c.x) / 2, my = (o.y + c.y) / 2;
            var inside = function (p) { return (p[0] - mx) * nx + (p[1] - my) * ny <= 0; };
            var out = [], k, a2, b2, ia, ib, t;
            for (k = 0; k < poly.length; k++) {
              a2 = poly[k]; b2 = poly[(k + 1) % poly.length]; ia = inside(a2); ib = inside(b2);
              if (ia) out.push(a2);
              if (ia !== ib) {
                t = ((mx - a2[0]) * nx + (my - a2[1]) * ny) / ((b2[0] - a2[0]) * nx + (b2[1] - a2[1]) * ny);
                out.push([a2[0] + t * (b2[0] - a2[0]), a2[1] + t * (b2[1] - a2[1])]);
              }
            }
            poly = out;
          });
          if (poly.length > 2) {
            svg.appendChild(sv("polygon", { points: poly.map(function (p) { return sx(p[0]) + "," + sy(p[1]); }).join(" "),
                                             fill: COLS[i], "fill-opacity": 0.1 }));
          }
        });
      }
      st.pts.forEach(function (p, i) {
        var col = st.assign && st.phase !== "placed" ? COLS[st.assign[i]] : "#64748B";
        svg.appendChild(sv("circle", { cx: sx(p.x), cy: sy(p.y), r: 5, fill: col, "class": "km-pt" }));
      });
      st.cents.forEach(function (c, i) {
        var gg = sv("g", { transform: "translate(" + sx(c.x) + " " + sy(c.y) + ")" });
        gg.appendChild(sv("circle", { r: 10, fill: COLS[i], "class": "km-cent" }));
        gg.appendChild(sv("path", { d: "M-4.5 -4.5 L4.5 4.5 M4.5 -4.5 L-4.5 4.5", stroke: "#fff",
                                    "stroke-width": 2.4, "stroke-linecap": "round" }));
        svg.appendChild(gg);
      });
      sRound.innerHTML = "<span>Round</span><b>" + st.round + "</b>";
      var inn = st.assign && st.cents.length ? inertia(st.pts, st.cents, st.assign) : null;
      sIn.innerHTML = "<span>Total squared distance</span><b>" + (inn === null ? "&ndash;" : inn.toFixed(3)) + "</b>";
      bAssign.disabled = !st.cents.length;
      bUpdate.disabled = st.phase !== "assigned";
    }

    function drawElbow() {
      elbow.textContent = "";
      if (st.pts.length < 6) { elbow.textContent = "Add a few more points first."; return; }
      var vals = [], k, s, best;
      for (k = 1; k <= 6; k++) {
        best = Infinity;
        for (s = 1; s <= 6; s++) best = Math.min(best, runKmeans(st.pts, k, s * 101 + k));
        vals.push(best);
      }
      var cw = 220, ch = 120, top = Math.max.apply(null, vals) || 1;
      var g = sv("svg", { viewBox: "0 0 " + cw + " " + (ch + 28), "class": "km-elbow-svg", role: "img",
                          "aria-label": "Elbow chart of total squared distance for k from 1 to 6" });
      var pts = [];
      vals.forEach(function (v, i) {
        var x = 20 + i * 36, y = 8 + (1 - v / top) * (ch - 16);
        pts.push(x + "," + y);
      });
      g.appendChild(sv("polyline", { points: pts.join(" "), "class": "km-elbow-line" }));
      vals.forEach(function (v, i) {
        var x = 20 + i * 36, y = 8 + (1 - v / top) * (ch - 16);
        g.appendChild(sv("circle", { cx: x, cy: y, r: i + 1 === st.k ? 6 : 4.2,
                                     fill: i + 1 === st.k ? COLS[0] : "#64748B" }));
        var t = sv("text", { x: x, y: ch + 18, "text-anchor": "middle", "class": "km-elbow-lab" });
        t.textContent = "k=" + (i + 1); g.appendChild(t);
      });
      elbow.appendChild(g);
      var drops = [];
      for (k = 1; k < vals.length; k++) drops.push(vals[k - 1] - vals[k]);
      var elbowK = 2, i2;
      for (i2 = 1; i2 < drops.length; i2++) {
        if (drops[i2] < drops[i2 - 1] * 0.35) { elbowK = i2 + 1; break; }
      }
      elbow.appendChild(el("p", "km-elbow-note",
        "The bend, where adding clusters stops helping much, suggests k = " + elbowK + "."));
    }

    function loadPreset(key) {
      stop();
      st.preset = key;
      st.pts = key === "empty" ? [] : PRESETS[key].make();
      if (key !== "empty") { st.k = PRESETS[key].k; sk.value = String(st.k); }
      st.cents = []; st.assign = null; st.round = 0; st.phase = "none";
      note.textContent = key === "empty" ? "Click to place points, then press Place centroids." : PRESETS[key].note;
      elbow.textContent = "";
      setStatus("Press Place centroids to start.");
      render();
    }

    bPlace.addEventListener("click", place);
    bAssign.addEventListener("click", function () { stop(); assign(); });
    bUpdate.addEventListener("click", function () { stop(); update(); });
    bShuffle.addEventListener("click", function () { st.seed = st.seed * 7 + 3; place(); });
    bRun.addEventListener("click", function () {
      if (st.timer) { stop(); return; }
      if (!st.cents.length) place();
      var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      var count = 0;
      if (reduce) {
        while (count++ < 80) { if (!stepOnce() && st.phase === "updated") break; }
        return;
      }
      bRun.textContent = "Pause";
      st.timer = setInterval(function () {
        if ((!stepOnce() && st.phase === "updated") || ++count > 80) stop();
      }, 650);
    });
    sk.addEventListener("change", function () { st.k = +sk.value; st.cents = []; st.assign = null; st.round = 0; st.phase = "none"; stop(); setStatus("k is now " + st.k + ". Press Place centroids."); render(); });
    sp.addEventListener("change", function () { loadPreset(sp.value); });
    elbowBtn.addEventListener("click", drawElbow);

    function local(ev) {
      var r = svg.getBoundingClientRect();
      return { x: ((ev.clientX - r.left) / r.width * W - PAD) / (W - 2 * PAD),
               y: ((ev.clientY - r.top) / r.height * H - PAD) / (H - 2 * PAD) };
    }
    svg.addEventListener("pointerdown", function (ev) {
      var p = local(ev);
      if (p.x < 0 || p.x > 1 || p.y < 0 || p.y > 1) return;
      if (ev.shiftKey) {
        var best = -1, bd = 0.0016;
        st.pts.forEach(function (q, i) { var d = d2(p, q); if (d < bd) { bd = d; best = i; } });
        if (best >= 0) st.pts.splice(best, 1);
      } else {
        st.pts.push({ x: p.x, y: p.y });
      }
      if (st.assign) { st.assign = st.pts.map(function (q) { return nearest(q, st.cents); }); st.phase = "assigned"; }
      render();
    });

    body.appendChild(row);
    body.appendChild(btns);
    body.appendChild(wrap);
    body.appendChild(status);
    body.appendChild(note);
    body.appendChild(hint);
    loadPreset("three");
  }

  function init() {
    var mounts = document.querySelectorAll('.tool[data-tool="kmeans-lab"]');
    Array.prototype.forEach.call(mounts, function (m) {
      var b = m.querySelector(".tool-body");
      if (b) build(b);
    });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
