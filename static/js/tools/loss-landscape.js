/* Loss landscape lab: a rotating 3D loss surface with balls that descend it.
 *
 * Gradient descent is usually taught with one picture of one bowl. Here the
 * student picks the landscape, drops balls by clicking the map, and chooses
 * the optimiser and learning rate, then watches each ball roll in 3D and on
 * the contour map at the same time. Ravines make plain descent zigzag, saddles
 * stall it, two valleys show where the starting point decides the ending
 * point, and a bumpy landscape shows momentum rolling through dips that trap
 * plain descent.
 */
(function () {
  "use strict";

  var BALLS = ["#06B6D4", "#F43F5E", "#84CC16", "#F59E0B", "#A855F7", "#38BDF8"];
  var STOPS = [[0, [13, 8, 135]], [0.25, [126, 3, 168]], [0.5, [204, 71, 120]],
               [0.75, [248, 149, 64]], [1, [240, 249, 33]]];

  function plasma(t, light) {
    t = Math.min(1, Math.max(0, t));
    var i, a, b, u, c = [0, 0, 0];
    for (i = 0; i < STOPS.length - 1; i++) {
      a = STOPS[i]; b = STOPS[i + 1];
      if (t <= b[0]) {
        u = (t - a[0]) / (b[0] - a[0]);
        c = [a[1][0] + (b[1][0] - a[1][0]) * u, a[1][1] + (b[1][1] - a[1][1]) * u,
             a[1][2] + (b[1][2] - a[1][2]) * u];
        break;
      }
    }
    var k = light === undefined ? 1 : light;
    return "rgb(" + Math.round(c[0] * k) + "," + Math.round(c[1] * k) + "," + Math.round(c[2] * k) + ")";
  }

  var LANDS = {
    bowl: { label: "Bowl", lr: 0.3,
      f: function (x, y) { return 0.25 * (x * x + y * y); },
      note: "One smooth bowl, like linear regression. Every ball reaches the same bottom. Push the learning rate up until the balls start to overshoot." },
    ravine: { label: "Ravine", lr: 1.6,
      f: function (x, y) { return 0.05 * x * x + 0.5 * y * y; },
      note: "A long narrow valley. Plain descent zigzags from wall to wall and crawls along the floor. Switch to momentum or Adam and compare." },
    valleys: { label: "Two valleys", lr: 0.25,
      f: function (x, y) {
        return 1.55 - 1.25 * Math.exp(-((x - 1) * (x - 1) + (y - 0.7) * (y - 0.7)) / 0.55)
          - 0.75 * Math.exp(-((x + 1.05) * (x + 1.05) + (y + 0.85) * (y + 0.85)) / 0.42)
          + 0.38 * Math.exp(-((x + 0.9) * (x + 0.9) + (y - 1.15) * (y - 1.15)) / 0.3)
          + 0.06 * (x * x + y * y); },
      note: "A deep valley and a shallow one. Drop balls in different places: where a ball starts decides which valley it ends in." },
    saddle: { label: "Saddle", lr: 0.2,
      f: function (x, y) { return 1 + 0.3 * x * x - 0.3 * y * y + 0.06 * y * y * y * y; },
      note: "A pass between two valleys. A ball dropped exactly on the middle line stalls at the saddle, where the slope is zero; a tiny nudge sends it down one side." },
    bumpy: { label: "Bumpy", lr: 0.05,
      f: function (x, y) { return 0.12 * (x * x + y * y) + 0.22 * (2 - Math.cos(4.7 * x) - Math.cos(4.7 * y)); },
      note: "Dozens of small dips. Plain descent gets stuck in whichever dip is nearest. Momentum can carry a ball through the small dips towards the middle." }
  };

  function el(tag, cls, txt) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (txt !== undefined && txt !== null) n.textContent = txt;
    return n;
  }

  function build(body) {
    body.textContent = "";
    var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var st = { land: "valleys", opt: "gd", lr: LANDS.valleys.lr, yaw: 0.7, pitch: 0.62,
               balls: [], running: false, spin: !reduce, raf: 0, last: 0, acc: 0, zlo: 0, zhi: 1 };

    // ----- controls
    var row = el("div", "tool-row");
    function field(label, ctrl) {
      var f = el("div", "tool-field"), id = "ll-" + Math.random().toString(36).slice(2, 8);
      var l = el("label", null, label); l.setAttribute("for", id); ctrl.id = id;
      f.appendChild(l); f.appendChild(ctrl); row.appendChild(f); return f;
    }
    var sLand = el("select");
    Object.keys(LANDS).forEach(function (k) { var o = el("option", null, LANDS[k].label); o.value = k; sLand.appendChild(o); });
    sLand.value = st.land;
    field("Landscape", sLand);
    var sOpt = el("select");
    [["gd", "Gradient descent"], ["momentum", "Momentum (0.9)"], ["adam", "Adam"]].forEach(function (p) {
      var o = el("option", null, p[1]); o.value = p[0]; sOpt.appendChild(o);
    });
    field("Optimiser", sOpt);
    var rLr = el("input"); rLr.type = "range"; rLr.min = "-3"; rLr.max = "0.4"; rLr.step = "0.01";
    var lrField = field("Learning rate", rLr);
    var lrOut = el("output", "ll-lr"); lrField.appendChild(lrOut);

    var btns = el("div", "tool-btns");
    function button(label, primary) {
      var b = el("button", "tool-btn" + (primary ? " is-primary" : ""), label);
      b.type = "button"; btns.appendChild(b); return b;
    }
    var bPlay = button("Play", true), bStep = button("Step"), bDrop = button("Drop 4 balls"),
        bReset = button("Back to start"), bClear = button("Clear"), bSpin = button(st.spin ? "Stop spinning" : "Spin");

    var wrap = el("div", "ll-wrap");
    var c3 = el("canvas", "ll-3d"); c3.setAttribute("tabindex", "0");
    c3.setAttribute("role", "img");
    c3.setAttribute("aria-label", "3D loss surface. Drag, or use the arrow keys, to rotate it.");
    var side = el("div", "ll-side");
    var cm = el("canvas", "ll-map"); cm.setAttribute("role", "img");
    cm.setAttribute("aria-label", "Contour map of the loss. Click to drop a ball.");
    var mapCap = el("p", "ll-cap", "Contour map: click to drop a ball");
    var list = el("ol", "ll-list");
    side.appendChild(cm); side.appendChild(mapCap); side.appendChild(list);
    wrap.appendChild(c3); wrap.appendChild(side);
    var status = el("p", "tool-status"); status.setAttribute("role", "status"); status.setAttribute("aria-live", "polite");
    var note = el("p", "tool-note");
    var hint = el("p", "tool-note ll-hint", "Drag the 3D view to turn it. Each step moves every ball against the gradient of the loss.");

    // ----- maths
    function F(x, y) { return LANDS[st.land].f(x, y); }
    function grad(x, y) {
      var h = 1e-4;
      return [(F(x + h, y) - F(x - h, y)) / (2 * h), (F(x, y + h) - F(x, y - h)) / (2 * h)];
    }
    function zRange() {
      var lo = Infinity, hi = -Infinity, i, j, z;
      for (i = 0; i <= 40; i++) for (j = 0; j <= 40; j++) {
        z = F(-2 + 4 * i / 40, -2 + 4 * j / 40); if (z < lo) lo = z; if (z > hi) hi = z;
      }
      st.zlo = lo; st.zhi = hi;
    }
    function lrFromSlider() { return Math.pow(10, +rLr.value); }
    function setLr(v) { st.lr = v; rLr.value = String(Math.log(v) / Math.LN10); lrOut.textContent = v < 0.01 ? v.toFixed(4) : v < 1 ? v.toFixed(3) : v.toFixed(2); }

    function addBall(x, y) {
      if (st.balls.length >= BALLS.length) st.balls.shift();
      st.balls.push({ x: x, y: y, x0: x, y0: y, vx: 0, vy: 0, mx: 0, my: 0, sx: 0, sy: 0, t: 0,
                      trail: [[x, y]], out: false, colour: BALLS[(st.dropCount = (st.dropCount || 0) + 1) % BALLS.length] });
    }
    function stepBall(b) {
      if (b.out) return;
      var g = grad(b.x, b.y), lr = st.lr;
      b.t += 1;
      if (st.opt === "gd") { b.x -= lr * g[0]; b.y -= lr * g[1]; }
      else if (st.opt === "momentum") {
        b.vx = 0.9 * b.vx + g[0]; b.vy = 0.9 * b.vy + g[1];
        b.x -= lr * b.vx; b.y -= lr * b.vy;
      } else {
        b.mx = 0.9 * b.mx + 0.1 * g[0]; b.my = 0.9 * b.my + 0.1 * g[1];
        b.sx = 0.999 * b.sx + 0.001 * g[0] * g[0]; b.sy = 0.999 * b.sy + 0.001 * g[1] * g[1];
        var c1 = 1 - Math.pow(0.9, b.t), c2 = 1 - Math.pow(0.999, b.t);
        b.x -= lr * (b.mx / c1) / (Math.sqrt(b.sx / c2) + 1e-8);
        b.y -= lr * (b.my / c1) / (Math.sqrt(b.sy / c2) + 1e-8);
      }
      if (!isFinite(b.x) || !isFinite(b.y) || Math.abs(b.x) > 2.2 || Math.abs(b.y) > 2.2) {
        b.out = true; b.x = Math.max(-2.2, Math.min(2.2, b.x || 0)); b.y = Math.max(-2.2, Math.min(2.2, b.y || 0));
      }
      b.trail.push([b.x, b.y]);
      if (b.trail.length > 400) b.trail.shift();
    }
    function stepAll() { st.balls.forEach(stepBall); describe(); }

    function describe() {
      list.textContent = "";
      st.balls.forEach(function (b, i) {
        var li = el("li");
        var dot = el("span", "ll-dot"); dot.style.background = b.colour;
        li.appendChild(dot);
        li.appendChild(document.createTextNode(b.out ? "left the map: the steps were too big" :
          "loss " + F(b.x, b.y).toFixed(3) + " after " + b.t + " step" + (b.t === 1 ? "" : "s")));
        list.appendChild(li);
      });
      if (!st.balls.length) { var li = el("li", "ll-empty", "No balls yet: click the map or press Drop 4 balls."); list.appendChild(li); }
    }

    // ----- drawing
    function fit(canvas, ratio) {
      var w = canvas.clientWidth || 300, dpr = Math.min(2, window.devicePixelRatio || 1);
      var h = Math.round(w * ratio);
      if (canvas.width !== Math.round(w * dpr) || canvas.height !== Math.round(h * dpr)) {
        canvas.width = Math.round(w * dpr); canvas.height = Math.round(h * dpr);
        canvas.style.height = h + "px";
      }
      return { w: canvas.width, h: canvas.height, dpr: dpr };
    }
    function proj(x, y, z, S) {
      var cy = Math.cos(st.yaw), sy = Math.sin(st.yaw), cp = Math.cos(st.pitch), sp = Math.sin(st.pitch);
      var zn = (z - st.zlo) / ((st.zhi - st.zlo) || 1) * 1.1 - 0.4;
      var x1 = x * cy - y * sy, y1 = x * sy + y * cy;
      var y2 = y1 * cp - zn * sp * 1.6, z2 = y1 * sp + zn * cp * 1.6;
      return [S.w / 2 + x1 * S.k, S.h * 0.56 - z2 * S.k, y2];
    }
    function draw3d() {
      var S = fit(c3, 0.72), g = c3.getContext("2d"), N = 34, i, j;
      S.k = Math.min(S.w, S.h * 1.4) * 0.19;
      g.clearRect(0, 0, S.w, S.h);
      var quads = [];
      for (i = 0; i < N; i++) for (j = 0; j < N; j++) {
        var xa = -2 + 4 * i / N, xb = -2 + 4 * (i + 1) / N, ya = -2 + 4 * j / N, yb = -2 + 4 * (j + 1) / N;
        var za = F(xa, ya), zb = F(xb, ya), zc = F(xb, yb), zd = F(xa, yb);
        var pa = proj(xa, ya, za, S), pb = proj(xb, ya, zb, S), pc = proj(xb, yb, zc, S), pd = proj(xa, yb, zd, S);
        var t = ((za + zb + zc + zd) / 4 - st.zlo) / ((st.zhi - st.zlo) || 1);
        // simple lighting from the surface normal
        var nx = (zb - za) / (4 / N), ny = (zd - za) / (4 / N);
        var light = 0.78 + 0.22 * (1 / Math.sqrt(1 + nx * nx * 0.4 + ny * ny * 0.4));
        quads.push([pa[2] + pb[2] + pc[2] + pd[2], pa, pb, pc, pd, plasma(t, light)]);
      }
      quads.sort(function (a, b) { return b[0] - a[0]; });
      g.lineWidth = Math.max(0.5, S.dpr * 0.4);
      g.strokeStyle = "rgba(255,255,255,0.18)";
      quads.forEach(function (q) {
        g.beginPath(); g.moveTo(q[1][0], q[1][1]); g.lineTo(q[2][0], q[2][1]);
        g.lineTo(q[3][0], q[3][1]); g.lineTo(q[4][0], q[4][1]); g.closePath();
        g.fillStyle = q[5]; g.fill(); g.stroke();
      });
      st.balls.forEach(function (b) {
        g.lineWidth = 2.4 * S.dpr; g.strokeStyle = "rgba(255,255,255,0.9)"; g.beginPath();
        b.trail.forEach(function (p, k) { var q = proj(p[0], p[1], F(p[0], p[1]) + 0.02, S); if (k) g.lineTo(q[0], q[1]); else g.moveTo(q[0], q[1]); });
        g.stroke();
        g.lineWidth = 1.4 * S.dpr; g.strokeStyle = b.colour; g.stroke();
        var p = proj(b.x, b.y, F(b.x, b.y) + 0.02, S), r = 6.5 * S.dpr;
        var rg = g.createRadialGradient(p[0] - r * 0.35, p[1] - r * 0.35 - r, r * 0.15, p[0], p[1] - r, r);
        rg.addColorStop(0, "#ffffff"); rg.addColorStop(0.35, b.colour); rg.addColorStop(1, "#111827");
        g.beginPath(); g.arc(p[0], p[1] - r, r, 0, Math.PI * 2); g.fillStyle = rg; g.fill();
      });
    }
    var mapCache = null;
    function drawMap() {
      var S = fit(cm, 1), g = cm.getContext("2d"), key = st.land + "|" + S.w;
      if (!mapCache || mapCache.key !== key) {
        var img = g.createImageData(S.w, S.h), d = img.data, x, y, k = 0;
        for (y = 0; y < S.h; y++) for (x = 0; x < S.w; x++) {
          var fx = -2 + 4 * x / (S.w - 1), fy = 2 - 4 * y / (S.h - 1);
          var t = (F(fx, fy) - st.zlo) / ((st.zhi - st.zlo) || 1);
          var band = Math.floor(t * 14) / 14;
          var edge = Math.abs(t * 14 - Math.round(t * 14)) < 0.06;
          var rgb = plasma(band + 0.035, edge ? 0.72 : 1).match(/\d+/g);
          d[k++] = +rgb[0]; d[k++] = +rgb[1]; d[k++] = +rgb[2]; d[k++] = 255;
        }
        mapCache = { key: key, img: img };
      }
      g.putImageData(mapCache.img, 0, 0);
      st.balls.forEach(function (b) {
        g.lineWidth = 2 * S.dpr; g.strokeStyle = "#ffffff"; g.beginPath();
        b.trail.forEach(function (p, k) {
          var px = (p[0] + 2) / 4 * S.w, py = (2 - p[1]) / 4 * S.h;
          if (k) g.lineTo(px, py); else g.moveTo(px, py);
        });
        g.stroke(); g.lineWidth = 1.2 * S.dpr; g.strokeStyle = b.colour; g.stroke();
        var px = (b.x + 2) / 4 * S.w, py = (2 - b.y) / 4 * S.h;
        g.beginPath(); g.arc(px, py, 5 * S.dpr, 0, Math.PI * 2); g.fillStyle = b.colour; g.fill();
        g.lineWidth = 1.5 * S.dpr; g.strokeStyle = "#111827"; g.stroke();
      });
    }
    function draw() { draw3d(); drawMap(); }

    // ----- animation loop
    function frame(ts) {
      st.raf = 0;
      var dt = st.last ? Math.min(100, ts - st.last) : 16; st.last = ts;
      if (st.spin) st.yaw += dt * 0.00018;
      if (st.running) {
        st.acc += dt;
        while (st.acc > 70) { st.acc -= 70; stepAll(); }
      }
      draw();
      if (st.spin || st.running) st.raf = requestAnimationFrame(frame);
    }
    function kick() { if (!st.raf) { st.last = 0; st.raf = requestAnimationFrame(frame); } }

    function loadLand(k) {
      st.land = k; mapCache = null; zRange(); st.balls = [];
      setLr(st.opt === "gd" ? LANDS[k].lr : st.opt === "momentum" ? LANDS[k].lr * 0.12 : 0.04);
      note.textContent = LANDS[k].note;
      if (k === "saddle") { addBall(-1.6, 0); addBall(-1.6, 0.04); }
      else if (k === "valleys") { addBall(-1.9, 0.1); addBall(1.9, -1.5); }
      else if (k === "ravine") { addBall(-1.9, 1.6); }
      else if (k === "bumpy") { addBall(-1.75, 1.6); addBall(1.7, -1.5); }
      else { addBall(-1.8, 1.4); addBall(1.6, 1.7); }
      status.textContent = "Press Play to let the balls roll.";
      describe(); draw();
    }

    sLand.addEventListener("change", function () { loadLand(sLand.value); });
    sOpt.addEventListener("change", function () {
      st.opt = sOpt.value;
      // each optimiser has its own sensible range: momentum's velocity adds up
      // about ten gradients, and Adam's steps are about the learning rate long
      setLr(st.opt === "gd" ? LANDS[st.land].lr : st.opt === "momentum"
            ? LANDS[st.land].lr * 0.12 : 0.04);
      st.balls.forEach(function (b) { b.vx = b.vy = b.mx = b.my = b.sx = b.sy = 0; b.t = 0; });
      status.textContent = "Optimiser: " + sOpt.options[sOpt.selectedIndex].text + ".";
    });
    rLr.addEventListener("input", function () { setLr(lrFromSlider()); });
    bPlay.addEventListener("click", function () {
      st.running = !st.running; bPlay.textContent = st.running ? "Pause" : "Play";
      status.textContent = st.running ? "Rolling downhill..." : "Paused.";
      if (st.running && !st.balls.length) dropFour();
      kick(); if (!st.running) draw();
    });
    bStep.addEventListener("click", function () { stepAll(); draw(); });
    function dropFour() {
      var r = Math.random, i;
      for (i = 0; i < 4; i++) addBall(-1.9 + 3.8 * r(), -1.9 + 3.8 * r());
      describe(); draw();
    }
    bDrop.addEventListener("click", dropFour);
    bReset.addEventListener("click", function () {
      st.balls.forEach(function (b) { b.x = b.x0; b.y = b.y0; b.vx = b.vy = b.mx = b.my = b.sx = b.sy = 0; b.t = 0; b.out = false; b.trail = [[b.x0, b.y0]]; });
      describe(); draw();
    });
    bClear.addEventListener("click", function () { st.balls = []; describe(); draw(); });
    bSpin.addEventListener("click", function () { st.spin = !st.spin; bSpin.textContent = st.spin ? "Stop spinning" : "Spin"; kick(); });

    // drag to rotate
    var drag = null;
    c3.addEventListener("pointerdown", function (ev) { drag = [ev.clientX, ev.clientY, st.yaw, st.pitch]; c3.setPointerCapture(ev.pointerId); });
    c3.addEventListener("pointermove", function (ev) {
      if (!drag) return;
      st.yaw = drag[2] + (ev.clientX - drag[0]) * 0.008;
      st.pitch = Math.max(0.12, Math.min(1.35, drag[3] + (ev.clientY - drag[1]) * 0.006));
      if (!st.raf) draw();
    });
    c3.addEventListener("pointerup", function () { drag = null; });
    c3.addEventListener("pointercancel", function () { drag = null; });
    c3.addEventListener("keydown", function (ev) {
      var k = ev.key, used = true;
      if (k === "ArrowLeft") st.yaw -= 0.12; else if (k === "ArrowRight") st.yaw += 0.12;
      else if (k === "ArrowUp") st.pitch = Math.min(1.35, st.pitch + 0.08);
      else if (k === "ArrowDown") st.pitch = Math.max(0.12, st.pitch - 0.08);
      else used = false;
      if (used) { ev.preventDefault(); if (!st.raf) draw(); }
    });
    cm.addEventListener("pointerdown", function (ev) {
      var r = cm.getBoundingClientRect();
      var x = -2 + 4 * (ev.clientX - r.left) / r.width, y = 2 - 4 * (ev.clientY - r.top) / r.height;
      addBall(x, y); describe(); draw();
      status.textContent = "Ball dropped at loss " + F(x, y).toFixed(3) + ".";
    });
    window.addEventListener("resize", function () { mapCache = null; draw(); });

    body.appendChild(row); body.appendChild(btns); body.appendChild(wrap);
    body.appendChild(status); body.appendChild(note); body.appendChild(hint);
    loadLand(st.land);
    kick();
  }

  function init() {
    var mounts = document.querySelectorAll('.tool[data-tool="loss-landscape"]');
    Array.prototype.forEach.call(mounts, function (m) {
      var b = m.querySelector(".tool-body");
      if (b) build(b);
    });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
