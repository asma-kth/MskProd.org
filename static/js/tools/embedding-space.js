/* Embedding space lab: words as points in a rotating 3D space.
 *
 * The words are the same hand-placed toy vectors as the lesson's figure, so
 * the picture and the lab agree. Choosing a word draws lines to its nearest
 * neighbours by cosine similarity; the analogy row computes a − b + c and
 * draws the parallelogram, so "king − man + woman" is something the student
 * can watch land on "queen" from any angle.
 */
(function () {
  "use strict";

  var WORDS = {
    man: [-0.7, 0.3, 0.1], woman: [-0.7, 0.3, 0.5], boy: [-0.8, 0.15, 0.05], girl: [-0.8, 0.15, 0.45],
    king: [-0.4, 0.65, 0.1], queen: [-0.4, 0.65, 0.5], prince: [-0.5, 0.5, 0.05], princess: [-0.5, 0.5, 0.45],
    cat: [0.55, 0.45, -0.35], kitten: [0.5, 0.33, -0.3], dog: [0.66, 0.5, -0.45], puppy: [0.6, 0.38, -0.42],
    lion: [0.72, 0.72, -0.3], tiger: [0.78, 0.66, -0.36], horse: [0.82, 0.4, -0.62], cow: [0.88, 0.28, -0.55],
    apple: [0.45, -0.55, 0.5], banana: [0.52, -0.48, 0.58], bread: [0.6, -0.72, 0.3], cheese: [0.68, -0.64, 0.36],
    pizza: [0.74, -0.58, 0.24], cake: [0.56, -0.78, 0.46],
    car: [-0.5, -0.55, -0.35], bus: [-0.56, -0.66, -0.28], train: [-0.66, -0.72, -0.42], bike: [-0.4, -0.48, -0.52],
    plane: [-0.6, -0.38, -0.66], boat: [-0.72, -0.56, -0.6],
    France: [0.05, 0.0, 0.75], Paris: [0.25, 0.2, 0.8], Italy: [-0.1, -0.05, 0.85], Rome: [0.1, 0.15, 0.9],
    Germany: [0.15, -0.15, 0.7], Berlin: [0.35, 0.05, 0.75]
  };
  var GROUPS = [["#6D28D9", ["man", "woman", "boy", "girl", "king", "queen", "prince", "princess"], "people"],
                ["#BE185D", ["cat", "kitten", "dog", "puppy", "lion", "tiger", "horse", "cow"], "animals"],
                ["#C2410C", ["apple", "banana", "bread", "cheese", "pizza", "cake"], "food"],
                ["#1D4ED8", ["car", "bus", "train", "bike", "plane", "boat"], "vehicles"],
                ["#0F766E", ["France", "Paris", "Italy", "Rome", "Germany", "Berlin"], "places"]];
  var COLOUR = {};
  GROUPS.forEach(function (g) { g[1].forEach(function (w) { COLOUR[w] = g[0]; }); });
  var NAMES = Object.keys(WORDS);
  var PRESETS = [["king", "man", "woman"], ["Paris", "France", "Italy"], ["kitten", "cat", "dog"],
                 ["princess", "girl", "boy"], ["Berlin", "Germany", "France"]];

  function el(tag, cls, txt) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (txt !== undefined && txt !== null) n.textContent = txt;
    return n;
  }
  function dot(a, b) { return a[0] * b[0] + a[1] * b[1] + a[2] * b[2]; }
  function len(a) { return Math.sqrt(dot(a, a)); }
  function cosine(a, b) { return dot(a, b) / (len(a) * len(b)); }
  function nearest(v, exclude, n) {
    return NAMES.filter(function (w) { return exclude.indexOf(w) < 0; })
      .map(function (w) { return [cosine(v, WORDS[w]), w]; })
      .sort(function (a, b) { return b[0] - a[0]; }).slice(0, n);
  }

  function build(body) {
    body.textContent = "";
    var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var st = { yaw: -1.31, pitch: 0.3, spin: !reduce, focus: "cat", analogy: null, raf: 0, last: 0 };

    var row = el("div", "tool-row");
    function field(label, ctrl) {
      var f = el("div", "tool-field"), id = "es-" + Math.random().toString(36).slice(2, 8);
      var l = el("label", null, label); l.setAttribute("for", id); ctrl.id = id;
      f.appendChild(l); f.appendChild(ctrl); row.appendChild(f); return f;
    }
    function wordSelect(val) {
      var s = el("select");
      NAMES.forEach(function (w) { var o = el("option", null, w); o.value = w; s.appendChild(o); });
      s.value = val; return s;
    }
    var sFocus = wordSelect("cat");
    field("Neighbours of", sFocus);

    var arow = el("div", "tool-row es-analogy");
    var sA = wordSelect("king"), sB = wordSelect("man"), sC = wordSelect("woman");
    function afield(label, ctrl) {
      var f = el("div", "tool-field"), id = "es-" + Math.random().toString(36).slice(2, 8);
      var l = el("label", null, label); l.setAttribute("for", id); ctrl.id = id;
      f.appendChild(l); f.appendChild(ctrl); arow.appendChild(f);
    }
    afield("Start from", sA); afield("minus", sB); afield("plus", sC);
    var bGo = el("button", "tool-btn is-primary", "Find a − b + c"); bGo.type = "button";
    var bTry = el("button", "tool-btn", "Another example"); bTry.type = "button";
    var bSpin = el("button", "tool-btn", st.spin ? "Stop spinning" : "Spin"); bSpin.type = "button";
    var btns = el("div", "tool-btns"); btns.appendChild(bGo); btns.appendChild(bTry); btns.appendChild(bSpin);

    var wrap = el("div", "es-wrap");
    var canvas = el("canvas", "es-plot"); canvas.setAttribute("tabindex", "0"); canvas.setAttribute("role", "img");
    canvas.setAttribute("aria-label", "A 3D space of word vectors. Drag, or use the arrow keys, to turn it.");
    var side = el("div", "es-side"), sNear = el("div"), sKey = el("div");
    var list = el("ol", "es-list");
    sNear.appendChild(el("p", "es-cap", "Nearest by cosine similarity"));
    sNear.appendChild(list);
    var legend = el("ul", "es-legend");
    GROUPS.forEach(function (g) {
      var li = el("li"), dotEl = el("span", "es-dot"); dotEl.style.background = g[0];
      li.appendChild(dotEl); li.appendChild(document.createTextNode(g[2])); legend.appendChild(li);
    });
    sKey.appendChild(el("p", "es-cap", "Colour key"));
    sKey.appendChild(legend);
    side.appendChild(sNear); side.appendChild(sKey);
    wrap.appendChild(canvas); wrap.appendChild(side);
    var status = el("p", "tool-status"); status.setAttribute("role", "status"); status.setAttribute("aria-live", "polite");
    var note = el("p", "tool-note", "These 34 words were placed by hand in 3 dimensions so you can see the idea. Real embeddings are learned, with hundreds of dimensions.");

    function proj(v, S) {
      var cy = Math.cos(st.yaw), sy = Math.sin(st.yaw), cp = Math.cos(st.pitch), sp = Math.sin(st.pitch);
      var x1 = v[0] * cy - v[1] * sy, y1 = v[0] * sy + v[1] * cy;
      var y2 = y1 * cp - v[2] * sp, z2 = y1 * sp + v[2] * cp;
      var persp = 1 / (1 + y2 * 0.18);
      return [S.w / 2 + x1 * S.k * persp, S.cy - z2 * S.k * persp, y2, persp];
    }
    function fit() {
      var w = canvas.clientWidth || 320, dpr = Math.min(2, window.devicePixelRatio || 1), h = Math.round(w * (w < 480 ? 0.95 : 0.7));
      if (canvas.width !== Math.round(w * dpr)) { canvas.width = Math.round(w * dpr); canvas.height = Math.round(h * dpr); canvas.style.height = h + "px"; }
      // Over every yaw, and pitch kept between 0.1 and 1, the words and the
      // floor project to between 1.03 units above the centre and 1.58 below,
      // so this scale and centre keep the scene inside the canvas as it turns.
      var k = Math.min(canvas.height * 0.36, canvas.width * 0.3);
      return { w: canvas.width, h: canvas.height, k: k, cy: canvas.height / 2 - 0.275 * k, dpr: dpr };
    }
    function draw() {
      var S = fit(), g = canvas.getContext("2d");
      g.clearRect(0, 0, S.w, S.h);
      var ink = "#111827", faint = "rgba(17,24,39,0.14)";
      // a floor grid under the words, for orientation
      var F = 0.9, Z = -0.85, corners = [[-F, -F, Z], [F, -F, Z], [F, F, Z], [-F, F, Z]];
      g.strokeStyle = faint; g.lineWidth = S.dpr;
      g.beginPath();
      corners.forEach(function (c, i) { var p = proj(c, S); if (i) g.lineTo(p[0], p[1]); else g.moveTo(p[0], p[1]); });
      g.closePath(); g.stroke();
      for (var t = -F / 2; t <= F / 2 + 0.01; t += F / 2) {
        var a = proj([t, -F, Z], S), b = proj([t, F, Z], S), c = proj([-F, t, Z], S), d = proj([F, t, Z], S);
        g.beginPath(); g.moveTo(a[0], a[1]); g.lineTo(b[0], b[1]); g.moveTo(c[0], c[1]); g.lineTo(d[0], d[1]); g.stroke();
      }
      var focusV = WORDS[st.focus], near = nearest(focusV, [st.focus], 4).map(function (p) { return p[1]; });
      // lines from the focus word to its neighbours
      var fp = proj(focusV, S);
      g.lineWidth = 2 * S.dpr; g.strokeStyle = "#F59E0B";
      near.forEach(function (w) { var p = proj(WORDS[w], S); g.beginPath(); g.moveTo(fp[0], fp[1]); g.lineTo(p[0], p[1]); g.stroke(); });
      // the analogy parallelogram
      if (st.analogy) {
        var A = WORDS[st.analogy[0]], B = WORDS[st.analogy[1]], C = WORDS[st.analogy[2]];
        var R = [A[0] - B[0] + C[0], A[1] - B[1] + C[1], A[2] - B[2] + C[2]];
        var pa = proj(A, S), pb = proj(B, S), pc = proj(C, S), pr = proj(R, S);
        g.setLineDash([6 * S.dpr, 5 * S.dpr]); g.lineWidth = 2 * S.dpr; g.strokeStyle = "#06B6D4";
        g.beginPath(); g.moveTo(pb[0], pb[1]); g.lineTo(pa[0], pa[1]); g.moveTo(pb[0], pb[1]); g.lineTo(pc[0], pc[1]); g.stroke();
        g.setLineDash([]); g.strokeStyle = "#F43F5E"; g.lineWidth = 2.6 * S.dpr;
        g.beginPath(); g.moveTo(pa[0], pa[1]); g.lineTo(pr[0], pr[1]); g.moveTo(pc[0], pc[1]); g.lineTo(pr[0], pr[1]); g.stroke();
        g.beginPath(); g.arc(pr[0], pr[1], 7 * S.dpr, 0, Math.PI * 2); g.strokeStyle = "#F43F5E"; g.stroke();
      }
      // points, back to front
      var pts = NAMES.map(function (w) { return { w: w, p: proj(WORDS[w], S) }; });
      pts.sort(function (a, b) { return b.p[2] - a.p[2]; });
      pts.forEach(function (it) {
        var w = it.w, p = it.p;
        it.hot = w === st.focus || near.indexOf(w) >= 0 || (st.analogy && st.analogy.indexOf(w) >= 0);
        it.r = (w === st.focus ? 7.5 : 5.2) * S.dpr * p[3];
        g.beginPath(); g.arc(p[0], p[1], it.r, 0, Math.PI * 2);
        g.fillStyle = COLOUR[w]; g.globalAlpha = it.hot ? 1 : 0.75; g.fill(); g.globalAlpha = 1;
        g.lineWidth = 1.5 * S.dpr; g.strokeStyle = "#FFFFFF"; g.stroke();
      });
      // Labels go on last: the focus word always, then the other highlighted
      // words, then the rest from front to back, skipping any label that would
      // overlap one already placed, so the picture stays readable at every
      // angle and on a small screen.
      var placed = [], pad = 2 * S.dpr;
      function rank(it) { return it.w === st.focus ? 2 : it.hot ? 1 : 0; }
      pts.slice().sort(function (a, b) { return (rank(b) - rank(a)) || (a.p[2] - b.p[2]); }).forEach(function (it) {
        var font = (it.hot ? "700 " : "600 ") + Math.round((it.hot ? 12.5 : 10.5) * S.dpr) + "px system-ui, sans-serif";
        g.font = font;
        var x = it.p[0] + it.r + 3 * S.dpr, y = it.p[1] - 3 * S.dpr, wd = g.measureText(it.w).width, ht = (it.hot ? 12.5 : 10.5) * S.dpr;
        var box = [x - pad, y - ht - pad, x + wd + pad, y + 0.3 * ht + pad];
        var clash = placed.some(function (q) { return box[0] < q[2] && q[0] < box[2] && box[1] < q[3] && q[1] < box[3]; });
        if (clash && it.w !== st.focus) return;
        placed.push(box);
        g.lineWidth = 3 * S.dpr; g.strokeStyle = "rgba(255,255,255,0.9)";
        g.strokeText(it.w, x, y);
        g.fillStyle = ink; g.globalAlpha = it.hot ? 1 : 0.8;
        g.fillText(it.w, x, y); g.globalAlpha = 1;
      });
    }
    function describe() {
      list.textContent = "";
      nearest(WORDS[st.focus], [st.focus], 5).forEach(function (p) {
        var li = el("li"); var d = el("span", "es-dot"); d.style.background = COLOUR[p[1]];
        li.appendChild(d); li.appendChild(document.createTextNode(p[1] + "  " + p[0].toFixed(3))); list.appendChild(li);
      });
    }
    function runAnalogy() {
      var a = sA.value, b = sB.value, c = sC.value;
      var v = [WORDS[a][0] - WORDS[b][0] + WORDS[c][0], WORDS[a][1] - WORDS[b][1] + WORDS[c][1], WORDS[a][2] - WORDS[b][2] + WORDS[c][2]];
      var best = nearest(v, [a, b, c], 2);
      st.analogy = [a, b, c];
      status.textContent = a + " − " + b + " + " + c + " lands nearest to “" + best[0][1] + "” (cosine " +
        best[0][0].toFixed(3) + "), then “" + best[1][1] + "” (" + best[1][0].toFixed(3) + ").";
      st.focus = best[0][1]; sFocus.value = st.focus; describe(); draw();
    }

    function frame(ts) {
      st.raf = 0;
      var dt = st.last ? Math.min(80, ts - st.last) : 16; st.last = ts;
      if (st.spin) { st.yaw += dt * 0.00025; draw(); st.raf = requestAnimationFrame(frame); }
    }
    function kick() { if (st.spin && !st.raf) { st.last = 0; st.raf = requestAnimationFrame(frame); } }

    sFocus.addEventListener("change", function () { st.focus = sFocus.value; describe(); draw(); status.textContent = "Nearest neighbours of “" + st.focus + "” are joined by amber lines."; });
    bGo.addEventListener("click", runAnalogy);
    var pi = 0;
    bTry.addEventListener("click", function () { pi = (pi + 1) % PRESETS.length; sA.value = PRESETS[pi][0]; sB.value = PRESETS[pi][1]; sC.value = PRESETS[pi][2]; runAnalogy(); });
    bSpin.addEventListener("click", function () { st.spin = !st.spin; bSpin.textContent = st.spin ? "Stop spinning" : "Spin"; kick(); });
    var drag = null;
    canvas.addEventListener("pointerdown", function (ev) { drag = [ev.clientX, ev.clientY, st.yaw, st.pitch]; canvas.setPointerCapture(ev.pointerId); });
    canvas.addEventListener("pointermove", function (ev) {
      if (!drag) return;
      st.yaw = drag[2] + (ev.clientX - drag[0]) * 0.008;
      st.pitch = Math.max(0.1, Math.min(1, drag[3] + (ev.clientY - drag[1]) * 0.006));
      if (!st.spin) draw();
    });
    canvas.addEventListener("pointerup", function () { drag = null; });
    canvas.addEventListener("pointercancel", function () { drag = null; });
    canvas.addEventListener("keydown", function (ev) {
      var used = true;
      if (ev.key === "ArrowLeft") st.yaw -= 0.12; else if (ev.key === "ArrowRight") st.yaw += 0.12;
      else if (ev.key === "ArrowUp") st.pitch = Math.min(1, st.pitch + 0.08);
      else if (ev.key === "ArrowDown") st.pitch = Math.max(0.1, st.pitch - 0.08);
      else used = false;
      if (used) { ev.preventDefault(); draw(); }
    });
    window.addEventListener("resize", draw);

    body.appendChild(row); body.appendChild(arow); body.appendChild(btns); body.appendChild(wrap);
    body.appendChild(status); body.appendChild(note);
    describe(); draw(); kick();
    status.textContent = "Pick a word to see its nearest neighbours, or try an analogy.";
  }

  function init() {
    var mounts = document.querySelectorAll('.tool[data-tool="embedding-space"]');
    Array.prototype.forEach.call(mounts, function (m) {
      var b = m.querySelector(".tool-body");
      if (b) build(b);
    });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
