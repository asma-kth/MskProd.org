/* Diffusion lab: noise flowing into a shape, one denoising step at a time.
 *
 * With a small dataset of points the best possible denoiser can be computed
 * exactly: a softmax-weighted average of the data points, weighted by how
 * well each one explains the noisy point. The sampler is the deterministic
 * DDIM update from the lesson's Python, on a cosine noise schedule. "Add
 * noise" runs the forward process instead, which needs no learning at all.
 */
(function () {
  "use strict";

  function shape(name) {
    var pts = [], i, t;
    if (name === "spiral") {
      for (i = 0; i < 160; i++) { t = i / 159; var r = 0.15 + 0.95 * t, a = 4.2 * Math.PI * t; pts.push([r * Math.cos(a), r * Math.sin(a)]); }
    } else if (name === "heart") {
      for (i = 0; i < 140; i++) {
        t = 2 * Math.PI * i / 140;
        pts.push([16 * Math.pow(Math.sin(t), 3) / 15, (13 * Math.cos(t) - 5 * Math.cos(2 * t) - 2 * Math.cos(3 * t) - Math.cos(4 * t)) / 15 + 0.1]);
      }
    } else if (name === "moons") {
      for (i = 0; i < 80; i++) { t = Math.PI * i / 79; pts.push([Math.cos(t) - 0.5, Math.sin(t) - 0.25]); pts.push([0.5 - Math.cos(t), 0.25 - Math.sin(t)]); }
    } else if (name === "smile") {
      for (i = 0; i < 100; i++) { t = 2 * Math.PI * i / 100; pts.push([1.1 * Math.cos(t), 1.1 * Math.sin(t)]); }
      for (i = 0; i < 40; i++) { t = Math.PI * (1.15 + 0.7 * i / 39); pts.push([0.6 * Math.cos(t), 0.6 * Math.sin(t) + 0.05]); }
      for (i = 0; i < 14; i++) { t = 2 * Math.PI * i / 14; pts.push([-0.38 + 0.1 * Math.cos(t), 0.4 + 0.1 * Math.sin(t)]); pts.push([0.38 + 0.1 * Math.cos(t), 0.4 + 0.1 * Math.sin(t)]); }
    } else {
      // the letters A and I
      var segs = [[-1.0, -0.9, -0.55, 0.9], [-0.55, 0.9, -0.1, -0.9], [-0.8, -0.1, -0.3, -0.1],
                  [0.5, 0.9, 1.0, 0.9], [0.75, 0.9, 0.75, -0.9], [0.5, -0.9, 1.0, -0.9]];
      segs.forEach(function (s) {
        var n = Math.round(Math.sqrt(Math.pow(s[2] - s[0], 2) + Math.pow(s[3] - s[1], 2)) * 30);
        for (var k = 0; k <= n; k++) pts.push([s[0] + (s[2] - s[0]) * k / n, s[1] + (s[3] - s[1]) * k / n]);
      });
    }
    return pts;
  }
  var SHAPES = [["spiral", "A spiral"], ["heart", "A heart"], ["moons", "Two moons"], ["smile", "A smiley face"], ["ai", "The letters AI"]];

  function gauss(rnd) {
    var u = 0, v = 0;
    while (u === 0) u = rnd();
    v = rnd();
    return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v);
  }
  function el(tag, cls, txt) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (txt !== undefined && txt !== null) n.textContent = txt;
    return n;
  }

  function build(body) {
    body.textContent = "";
    var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
    var st = { data: shape("spiral"), T: 40, n: 260, pts: [], trails: [], noise: [], t: 0, mode: "idle", raf: 0, last: 0, seed: 1 };

    var row = el("div", "tool-row");
    function field(label, ctrl, out) {
      var f = el("div", "tool-field"), id = "dl-" + Math.random().toString(36).slice(2, 8);
      var l = el("label", null, label); l.setAttribute("for", id); ctrl.id = id;
      f.appendChild(l); f.appendChild(ctrl); if (out) f.appendChild(out); row.appendChild(f); return f;
    }
    var sShape = el("select");
    SHAPES.forEach(function (s) { var o = el("option", null, s[1]); o.value = s[0]; sShape.appendChild(o); });
    field("Training data", sShape);
    var sSteps = el("input"); sSteps.type = "range"; sSteps.min = "2"; sSteps.max = "100"; sSteps.step = "1"; sSteps.value = "40";
    var stepOut = el("span", "dl-num", "40");
    field("Denoising steps", sSteps, stepOut);
    var chk = el("div", "tool-field dl-checks");
    function check(label, on) {
      var l = el("label"), c = el("input"); c.type = "checkbox"; c.checked = on;
      l.appendChild(c); l.appendChild(document.createTextNode(" " + label)); chk.appendChild(l); return c;
    }
    var cData = check("Show the training data", true), cTrail = check("Show each point's path", true);
    row.appendChild(chk);

    var btns = el("div", "tool-btns");
    var bGen = el("button", "tool-btn is-primary", "Generate from noise"); bGen.type = "button";
    var bNoise = el("button", "tool-btn", "Add noise to the data"); bNoise.type = "button";
    var bNew = el("button", "tool-btn", "New random noise"); bNew.type = "button";
    btns.appendChild(bGen); btns.appendChild(bNoise); btns.appendChild(bNew);

    var canvas = el("canvas", "dl-plot"); canvas.setAttribute("role", "img");
    canvas.setAttribute("aria-label", "Points on a plane moving between random noise and the shape of the training data.");
    var meterRow = el("div", "dl-meter-row"), meter = el("div", "dl-meter"), meterFill = el("span", "dl-meter-fill");
    meter.appendChild(meterFill); meterRow.appendChild(el("span", "dl-meter-label", "noise level")); meterRow.appendChild(meter);
    meter.setAttribute("aria-hidden", "true");
    var status = el("p", "tool-status"); status.setAttribute("role", "status"); status.setAttribute("aria-live", "polite");
    var note = el("p", "tool-note", "With only a few hundred training points the perfect denoiser can be written down exactly, so every generated point lands on the shape. A real model has to learn its denoiser from millions of images.");

    // cosine schedule: how much of the clean point survives after t of T steps
    function abar(t) { var v = Math.cos((t / st.T + 0.008) / 1.008 * Math.PI / 2); return v * v; }
    function denoise(x, t) {
      var a = Math.sqrt(abar(t)), s2 = 2 * (1 - abar(t)), m = -Infinity, i, d, sc = new Array(st.data.length);
      for (i = 0; i < st.data.length; i++) {
        d = st.data[i];
        var dx = x[0] - a * d[0], dy = x[1] - a * d[1];
        sc[i] = -(dx * dx + dy * dy) / s2;
        if (sc[i] > m) m = sc[i];
      }
      var tot = 0, ox = 0, oy = 0;
      for (i = 0; i < st.data.length; i++) { var w = Math.exp(sc[i] - m); tot += w; ox += w * st.data[i][0]; oy += w * st.data[i][1]; }
      return [ox / tot, oy / tot];
    }
    function reverseStep() {
      var t = st.t, a = Math.sqrt(abar(t)), s = Math.sqrt(1 - abar(t)), a2 = Math.sqrt(abar(t - 1)), s2 = Math.sqrt(1 - abar(t - 1));
      st.pts = st.pts.map(function (x, i) {
        var x0 = denoise(x, t), e = [(x[0] - a * x0[0]) / s, (x[1] - a * x0[1]) / s];
        var nx = [a2 * x0[0] + s2 * e[0], a2 * x0[1] + s2 * e[1]];
        st.trails[i].push(nx);
        return nx;
      });
      st.t -= 1;
    }
    function forwardAt(t) {
      // the forward process jumps straight to step t: no learning involved
      var a = Math.sqrt(abar(t)), s = Math.sqrt(1 - abar(t));
      st.pts = st.noise.map(function (e, i) {
        var d = st.data[i % st.data.length];
        return [a * d[0] + s * e[0], a * d[1] + s * e[1]];
      });
    }
    function freshNoise() {
      var seed = st.seed++, rnd = (function (s) { return function () { s = (s * 16807) % 2147483647; return (s - 1) / 2147483646; }; })(seed * 7919 + 13);
      st.noise = [];
      for (var i = 0; i < st.n; i++) st.noise.push([gauss(rnd), gauss(rnd)]);
    }

    function fit() {
      var w = canvas.clientWidth || 320, dpr = Math.min(2, window.devicePixelRatio || 1), h = Math.round(w * 0.72);
      if (canvas.width !== Math.round(w * dpr)) { canvas.width = Math.round(w * dpr); canvas.height = Math.round(h * dpr); canvas.style.height = h + "px"; }
      return { w: canvas.width, h: canvas.height, k: Math.min(canvas.width, canvas.height) / 5.2, dpr: dpr };
    }
    function hue(i) {
      var e = st.noise[i] || [0, 0];
      return "hsl(" + Math.round((Math.atan2(e[1], e[0]) / Math.PI * 180 + 360) % 360) + ",85%,55%)";
    }
    function draw() {
      var S = fit(), g = canvas.getContext("2d"), cx = S.w / 2, cy = S.h / 2;
      g.clearRect(0, 0, S.w, S.h);
      g.strokeStyle = "rgba(17,24,39,0.1)"; g.lineWidth = S.dpr;
      for (var v = -2; v <= 2; v++) {
        g.beginPath(); g.moveTo(cx + v * S.k, 0); g.lineTo(cx + v * S.k, S.h); g.stroke();
        g.beginPath(); g.moveTo(0, cy - v * S.k); g.lineTo(S.w, cy - v * S.k); g.stroke();
      }
      if (cData.checked) {
        g.fillStyle = "rgba(17,24,39,0.25)";
        st.data.forEach(function (d) { g.beginPath(); g.arc(cx + d[0] * S.k, cy - d[1] * S.k, 2.2 * S.dpr, 0, Math.PI * 2); g.fill(); });
      }
      if (cTrail.checked && st.mode !== "noising") {
        g.lineWidth = 1 * S.dpr; g.globalAlpha = 0.35;
        st.trails.forEach(function (tr, i) {
          if (tr.length < 2) return;
          g.strokeStyle = hue(i); g.beginPath();
          tr.forEach(function (p, k) { var x = cx + p[0] * S.k, y = cy - p[1] * S.k; if (k) g.lineTo(x, y); else g.moveTo(x, y); });
          g.stroke();
        });
        g.globalAlpha = 1;
      }
      st.pts.forEach(function (p, i) {
        g.beginPath(); g.arc(cx + p[0] * S.k, cy - p[1] * S.k, 2.8 * S.dpr, 0, Math.PI * 2);
        g.fillStyle = hue(i); g.fill();
      });
      meterFill.style.width = (100 * Math.sqrt(1 - abar(Math.max(0, Math.min(st.T, st.t))))).toFixed(1) + "%";
    }

    function stop() { if (st.raf) { cancelAnimationFrame(st.raf); st.raf = 0; } st.mode = "idle"; }
    function startReverse() {
      stop();
      st.T = parseInt(sSteps.value, 10);
      st.t = st.T;
      st.pts = st.noise.map(function (e) { return [e[0], e[1]]; });
      st.trails = st.pts.map(function (p) { return [p]; });
      st.mode = "generating";
      status.textContent = "Starting from pure noise: " + st.n + " random points.";
      if (reduce) { while (st.t > 0) reverseStep(); finishReverse(); return; }
      st.last = 0;
      st.raf = requestAnimationFrame(tick);
    }
    function finishReverse() {
      st.mode = "idle"; draw();
      var sum = 0;
      st.pts.forEach(function (p) {
        var best = Infinity;
        st.data.forEach(function (d) { best = Math.min(best, Math.hypot(p[0] - d[0], p[1] - d[1])); });
        sum += best;
      });
      status.textContent = "Done after " + st.T + " steps. Average distance from a point to the shape: " + (sum / st.pts.length).toFixed(3) + ".";
    }
    function tick(ts) {
      st.raf = 0;
      if (st.mode === "generating") {
        if (!st.last || ts - st.last > Math.max(16, 900 / st.T)) {
          st.last = ts;
          reverseStep();
          status.textContent = "Step " + (st.T - st.t) + " of " + st.T + ": each point moves towards the denoiser's guess.";
        }
        draw();
        if (st.t > 0) st.raf = requestAnimationFrame(tick); else finishReverse();
      } else if (st.mode === "noising") {
        if (!st.last || ts - st.last > Math.max(16, 900 / st.T)) {
          st.last = ts;
          st.t += 1;
          forwardAt(st.t);
          status.textContent = "Forward step " + st.t + " of " + st.T + ": " + Math.round(100 * Math.sqrt(abar(st.t))) + "% of the shape is left.";
        }
        draw();
        if (st.t < st.T) st.raf = requestAnimationFrame(tick); else { st.mode = "idle"; status.textContent = "Pure noise: the shape is gone. Now generate it back."; }
      }
    }
    function startForward() {
      stop();
      st.T = parseInt(sSteps.value, 10);
      st.t = 0; st.trails = [];
      forwardAt(0);
      st.mode = "noising";
      if (reduce) { st.t = st.T; forwardAt(st.T); st.mode = "idle"; draw(); status.textContent = "Pure noise: the shape is gone. Now generate it back."; return; }
      st.last = 0;
      st.raf = requestAnimationFrame(tick);
    }

    sShape.addEventListener("change", function () { st.data = shape(sShape.value); startReverse(); });
    sSteps.addEventListener("input", function () { stepOut.textContent = sSteps.value; });
    sSteps.addEventListener("change", function () { startReverse(); });
    cData.addEventListener("change", draw);
    cTrail.addEventListener("change", draw);
    bGen.addEventListener("click", startReverse);
    bNoise.addEventListener("click", startForward);
    bNew.addEventListener("click", function () { freshNoise(); startReverse(); });
    window.addEventListener("resize", draw);

    body.appendChild(row); body.appendChild(btns); body.appendChild(canvas); body.appendChild(meterRow);
    body.appendChild(status); body.appendChild(note);
    freshNoise();
    st.pts = st.noise.map(function (e) { return [e[0], e[1]]; });
    st.trails = st.pts.map(function (p) { return [p]; });
    st.t = st.T;
    draw();
    status.textContent = "These " + st.n + " points are pure random noise. Press Generate to denoise them, step by step.";
  }

  function init() {
    var mounts = document.querySelectorAll('.tool[data-tool="diffusion-lab"]');
    Array.prototype.forEach.call(mounts, function (m) {
      var b = m.querySelector(".tool-body");
      if (b) build(b);
    });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
