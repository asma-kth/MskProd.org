/* Neuron lab: one artificial neuron, its two weights and its bias as sliders.
 *
 * The plane is shaded by the neuron's output, which only changes along the
 * direction of the weight vector, so the shading is one linear gradient laid
 * across that direction: exact, smooth and cheap. Moving w1 and w2 turns the
 * boundary, moving b slides it, and the perceptron buttons run Rosenblatt's
 * rule on the chosen gate until it settles, or, for XOR, until it is clear
 * that it never will.
 */
(function () {
  "use strict";

  var NS = "http://www.w3.org/2000/svg";
  var W = 360, H = 360, PAD = 18, LO = -0.6, HI = 1.6;
  var BLUE = "#1D4ED8", PINK = "#BE185D";

  var SETS = {
    and: { label: "AND", pts: [[0, 0, 0], [0, 1, 0], [1, 0, 0], [1, 1, 1]] },
    or: { label: "OR", pts: [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 1]] },
    nand: { label: "NAND", pts: [[0, 0, 1], [0, 1, 1], [1, 0, 1], [1, 1, 0]] },
    xor: { label: "XOR", pts: [[0, 0, 0], [0, 1, 1], [1, 0, 1], [1, 1, 0]] },
    blobs: { label: "Two clouds", pts: (function () {
      var s = 9, out = [], i;
      function r() { s = s * 16807 % 2147483647; return (s - 1) / 2147483646; }
      for (i = 0; i < 12; i++) out.push([0.05 + r() * 0.55, 0.0 + r() * 0.5, 0]);
      for (i = 0; i < 12; i++) out.push([0.55 + r() * 0.6, 0.65 + r() * 0.6, 1]);
      return out; })() }
  };

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
  function sig(z) { return 1 / (1 + Math.exp(-z)); }
  function mix(t) {
    // blue (0) to near-white (0.5) to pink (1), as in the course's diverging map
    var a = [29, 78, 216], m = [243, 244, 246], b = [190, 24, 93], c, u;
    if (t < 0.5) { u = t / 0.5; c = [a[0] + (m[0] - a[0]) * u, a[1] + (m[1] - a[1]) * u, a[2] + (m[2] - a[2]) * u]; }
    else { u = (t - 0.5) / 0.5; c = [m[0] + (b[0] - m[0]) * u, m[1] + (b[1] - m[1]) * u, m[2] + (b[2] - m[2]) * u]; }
    return "rgb(" + Math.round(c[0]) + "," + Math.round(c[1]) + "," + Math.round(c[2]) + ")";
  }
  var uid = 0;

  function build(body) {
    body.textContent = "";
    uid += 1;
    var gid = "nl-grad-" + uid;
    var st = { set: "and", w1: 0.6, w2: -0.4, b: 0.2, act: "sigmoid", epoch: 0, timer: null, idx: 0 };

    var row = el("div", "tool-row");
    function field(label, ctrl) {
      var f = el("div", "tool-field"), id = "nl-" + uid + "-" + label.replace(/\W/g, "");
      var l = el("label", null, label); l.setAttribute("for", id); ctrl.id = id;
      f.appendChild(l); f.appendChild(ctrl); row.appendChild(f); return f;
    }
    var sSet = el("select");
    Object.keys(SETS).forEach(function (k) { var o = el("option", null, SETS[k].label); o.value = k; sSet.appendChild(o); });
    field("Data", sSet);
    var sAct = el("select");
    [["sigmoid", "Sigmoid"], ["step", "Step"]].forEach(function (p) { var o = el("option", null, p[1]); o.value = p[0]; sAct.appendChild(o); });
    field("Activation", sAct);

    var sliders = el("div", "nl-sliders");
    function slider(name, min, max) {
      var wrap = el("div", "nl-slider");
      var id = "nl-" + uid + "-" + name;
      var lab = el("label", null, name); lab.setAttribute("for", id);
      var r = el("input"); r.type = "range"; r.min = String(min); r.max = String(max); r.step = "0.05"; r.id = id;
      var out = el("output");
      wrap.appendChild(lab); wrap.appendChild(r); wrap.appendChild(out); sliders.appendChild(wrap);
      return { r: r, out: out };
    }
    var s1 = slider("w1", -4, 4), s2 = slider("w2", -4, 4), sb = slider("b", -6, 6);

    var btns = el("div", "tool-btns");
    function button(label, primary) {
      var b = el("button", "tool-btn" + (primary ? " is-primary" : ""), label);
      b.type = "button"; btns.appendChild(b); return b;
    }
    var bTrain = button("Train with the perceptron rule", true);
    var bEpoch = button("One epoch");
    var bRand = button("Random weights");

    var wrap = el("div", "nl-wrap");
    var svg = sv("svg", { viewBox: "0 0 " + W + " " + H, "class": "nl-plot", role: "img",
                          "aria-label": "The input plane shaded by the neuron's output, with its decision boundary" });
    var side = el("div", "nl-side");
    var eq = el("p", "nl-eq");
    var table = el("table", "nl-table");
    side.appendChild(eq); side.appendChild(table);
    wrap.appendChild(svg); wrap.appendChild(side);
    var status = el("p", "tool-status"); status.setAttribute("role", "status"); status.setAttribute("aria-live", "polite");
    var hint = el("p", "tool-note", "Turn w1 and w2 to rotate the boundary; move b to slide it. The arrow is the weight vector, pointing to the side where the neuron says 1.");

    function px(v) { return PAD + (v - LO) / (HI - LO) * (W - 2 * PAD); }
    function py(v) { return H - PAD - (v - LO) / (HI - LO) * (H - 2 * PAD); }
    function z(p) { return st.w1 * p[0] + st.w2 * p[1] + st.b; }
    function out(p) { return st.act === "step" ? (z(p) > 0 ? 1 : 0) : sig(z(p)); }
    function fmt(v) { return (v < 0 ? "−" : "") + Math.abs(v).toFixed(2); }

    function render() {
      while (svg.firstChild) svg.removeChild(svg.firstChild);
      var defs = sv("defs", {}), n = Math.hypot(st.w1, st.w2);
      svg.appendChild(defs);
      var bg = sv("rect", { x: PAD, y: PAD, width: W - 2 * PAD, height: H - 2 * PAD, rx: 8 });
      if (n < 1e-6) {
        bg.setAttribute("fill", mix(st.act === "step" ? (st.b > 0 ? 1 : 0) : sig(st.b)));
      } else {
        // the output only changes along w: one gradient across that direction
        var ux = st.w1 / n, uy = st.w2 / n, cx = -st.b * ux / n, cy = -st.b * uy / n;
        var L = 3.2, g = sv("linearGradient", { id: gid, gradientUnits: "userSpaceOnUse",
          x1: px(cx - ux * L), y1: py(cy - uy * L), x2: px(cx + ux * L), y2: py(cy + uy * L) }), i, d, t;
        for (i = 0; i <= 40; i++) {
          d = -L + 2 * L * i / 40;
          t = st.act === "step" ? (d > 0 ? 1 : 0) : sig(n * d);
          g.appendChild(sv("stop", { offset: i / 40, "stop-color": mix(t), "stop-opacity": 0.7 }));
        }
        defs.appendChild(g);
        bg.setAttribute("fill", "url(#" + gid + ")");
      }
      svg.appendChild(bg);
      svg.appendChild(sv("rect", { x: PAD, y: PAD, width: W - 2 * PAD, height: H - 2 * PAD, rx: 8, "class": "nl-frame" }));
      [0, 1].forEach(function (v) {
        svg.appendChild(sv("line", { x1: px(v), y1: PAD, x2: px(v), y2: H - PAD, "class": "nl-grid" }));
        svg.appendChild(sv("line", { x1: PAD, y1: py(v), x2: W - PAD, y2: py(v), "class": "nl-grid" }));
      });
      if (n > 1e-6) {
        // boundary w1 x + w2 y + b = 0, clipped to the box
        var pts = [], ends = [[LO, null], [HI, null], [null, LO], [null, HI]];
        ends.forEach(function (e) {
          if (e[0] !== null && Math.abs(st.w2) > 1e-9) { var y = -(st.w1 * e[0] + st.b) / st.w2; if (y >= LO - 1e-9 && y <= HI + 1e-9) pts.push([e[0], y]); }
          if (e[1] !== null && Math.abs(st.w1) > 1e-9) { var x = -(st.w2 * e[1] + st.b) / st.w1; if (x >= LO - 1e-9 && x <= HI + 1e-9) pts.push([x, e[1]]); }
        });
        if (pts.length >= 2) {
          svg.appendChild(sv("line", { x1: px(pts[0][0]), y1: py(pts[0][1]), x2: px(pts[1][0]), y2: py(pts[1][1]), "class": "nl-line" }));
          var mx = (pts[0][0] + pts[1][0]) / 2, my = (pts[0][1] + pts[1][1]) / 2, ux2 = st.w1 / n * 0.35, uy2 = st.w2 / n * 0.35;
          var ax = px(mx + ux2), ay = py(my + uy2), sx = px(mx), sy = py(my), ang = Math.atan2(ay - sy, ax - sx);
          svg.appendChild(sv("line", { x1: sx, y1: sy, x2: ax - 8 * Math.cos(ang), y2: ay - 8 * Math.sin(ang), "class": "nl-arrow" }));
          svg.appendChild(sv("polygon", { points: ax + "," + ay + " " + (ax - 11 * Math.cos(ang) + 5.5 * Math.sin(ang)) + "," +
            (ay - 11 * Math.sin(ang) - 5.5 * Math.cos(ang)) + " " + (ax - 11 * Math.cos(ang) - 5.5 * Math.sin(ang)) + "," +
            (ay - 11 * Math.sin(ang) + 5.5 * Math.cos(ang)), "class": "nl-arrowhead" }));
        }
      }
      var right = 0, list = SETS[st.set].pts;
      list.forEach(function (p) {
        var o = out(p), pred = o > 0.5 ? 1 : 0, ok = pred === p[2];
        if (ok) right++;
        if (p[2]) svg.appendChild(sv("circle", { cx: px(p[0]), cy: py(p[1]), r: list.length > 4 ? 6 : 10, fill: PINK, "class": "nl-pt" }));
        else svg.appendChild(sv("circle", { cx: px(p[0]), cy: py(p[1]), r: list.length > 4 ? 5.5 : 9, fill: "#fff", stroke: BLUE, "stroke-width": 3 }));
        if (!ok) svg.appendChild(sv("circle", { cx: px(p[0]), cy: py(p[1]), r: list.length > 4 ? 10 : 15, "class": "nl-wrong" }));
      });
      s1.out.textContent = fmt(st.w1); s2.out.textContent = fmt(st.w2); sb.out.textContent = fmt(st.b);
      s1.r.value = String(st.w1); s2.r.value = String(st.w2); sb.r.value = String(st.b);
      eq.innerHTML = "z = <b>" + fmt(st.w1) + "</b>·x₁ + <b>" + fmt(st.w2) + "</b>·x₂ + <b>" + fmt(st.b) +
        "</b><br>output = " + (st.act === "step" ? "step(z)" : "σ(z)") + " · <b>" + right + " of " + list.length + "</b> right";
      table.textContent = "";
      if (list.length === 4) {
        var head = el("tr"); ["x₁", "x₂", "z", "output", "target"].forEach(function (h) { head.appendChild(el("th", null, h)); });
        table.appendChild(head);
        list.forEach(function (p) {
          var tr = el("tr"), o = out(p), pred = o > 0.5 ? 1 : 0;
          [String(p[0]), String(p[1]), fmt(z(p)), st.act === "step" ? String(o) : o.toFixed(2), String(p[2])].forEach(function (c, k) {
            var td = el("td", null, c); if (k === 3) td.className = pred === p[2] ? "nl-ok" : "nl-bad"; tr.appendChild(td);
          });
          table.appendChild(tr);
        });
      }
      return right === list.length;
    }

    function epoch() {
      var list = SETS[st.set].pts, mistakes = 0, lr = 0.5;
      list.forEach(function (p) {
        var pred = z(p) > 0 ? 1 : 0, err = p[2] - pred;
        if (err) { mistakes++; st.w1 += lr * err * p[0]; st.w2 += lr * err * p[1]; st.b += lr * err; }
      });
      st.epoch += 1;
      return mistakes;
    }
    function stop() { if (st.timer) { clearInterval(st.timer); st.timer = null; bTrain.textContent = "Train with the perceptron rule"; } }

    bEpoch.addEventListener("click", function () {
      stop();
      var m = epoch(); render();
      status.textContent = "Epoch " + st.epoch + ": " + m + " mistake" + (m === 1 ? "" : "s") + " during the pass" + (m ? ", so the weights moved." : ", so the weights stayed put: learned.");
    });
    bTrain.addEventListener("click", function () {
      if (st.timer) { stop(); return; }
      var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      var limit = st.epoch + 40;
      function tick() {
        var m = epoch(); render();
        if (!m) { stop(); status.textContent = "Learned it after " + st.epoch + " epochs: a straight line separates the classes."; return true; }
        if (st.epoch >= limit) {
          stop();
          status.textContent = st.set === "xor" ? "Still making mistakes after " + st.epoch + " epochs. No straight line can separate XOR, so the perceptron never settles." :
            "Still learning after " + st.epoch + " epochs. Press again to continue.";
          return true;
        }
        status.textContent = "Epoch " + st.epoch + ": " + m + " mistake" + (m === 1 ? "" : "s") + ".";
        return false;
      }
      if (reduce) { while (!tick()) { /* run to the end at once */ } return; }
      bTrain.textContent = "Pause";
      st.timer = setInterval(tick, 260);
    });
    bRand.addEventListener("click", function () {
      stop();
      st.w1 = Math.round((Math.random() * 6 - 3) * 20) / 20; st.w2 = Math.round((Math.random() * 6 - 3) * 20) / 20;
      st.b = Math.round((Math.random() * 4 - 2) * 20) / 20; st.epoch = 0; render();
      status.textContent = "Random weights. Press Train to let the perceptron rule fix them.";
    });
    [[s1, "w1"], [s2, "w2"], [sb, "b"]].forEach(function (p) {
      p[0].r.addEventListener("input", function () { stop(); st[p[1]] = +p[0].r.value; var all = render(); status.textContent = all ? "Every point is on the correct side." : ""; });
    });
    sSet.addEventListener("change", function () { stop(); st.set = sSet.value; st.epoch = 0; render(); status.textContent = SETS[st.set].label + " loaded. Can you find weights that get every point right?"; });
    sAct.addEventListener("change", function () { st.act = sAct.value; render(); });

    body.appendChild(row); body.appendChild(sliders); body.appendChild(btns); body.appendChild(wrap);
    body.appendChild(status); body.appendChild(hint);
    render();
    status.textContent = "AND loaded. Can you find weights that get every point right?";
  }

  function init() {
    var mounts = document.querySelectorAll('.tool[data-tool="neuron-lab"]');
    Array.prototype.forEach.call(mounts, function (m) {
      var b = m.querySelector(".tool-body");
      if (b) build(b);
    });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
