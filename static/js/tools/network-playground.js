/* Network playground: train a small neural network in the browser and watch
 * its decision boundary form.
 *
 * Everything the lessons describe happens here for real: a forward pass over
 * the data, cross-entropy loss, backpropagation through each layer and a
 * gradient descent step with momentum, many times a second. The shading is
 * the network's output probability at every point of the plane, and the
 * diagram on the right shows every weight, coloured by sign and thickened by
 * size, changing as it learns.
 */
(function () {
  "use strict";

  var PINK = [190, 24, 93], BLUE = [29, 78, 216], MID = [243, 244, 246];

  function rng(seed) {
    var s = seed % 2147483647; if (s <= 0) s += 2147483646;
    return function () { s = s * 16807 % 2147483647; return (s - 1) / 2147483646; };
  }
  function gauss(r) { var u = 1 - r(), v = r(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v); }

  var DATA = {
    blobs: { label: "Two clouds", make: function (r) {
      var out = [], i;
      for (i = 0; i < 100; i++) out.push([-1.6 + gauss(r) * 0.75, -1.4 + gauss(r) * 0.75, 0]);
      for (i = 0; i < 100; i++) out.push([1.5 + gauss(r) * 0.75, 1.5 + gauss(r) * 0.75, 1]);
      return out; }, note: "A straight line is enough. Even a network with one hidden neuron learns this." },
    circle: { label: "Circle", make: function (r) {
      var out = [], i, a, d;
      for (i = 0; i < 200; i++) {
        a = r() * Math.PI * 2;
        if (i % 2) { d = r() * 1.6; out.push([Math.cos(a) * d, Math.sin(a) * d, 1]); }
        else { d = 2.4 + r() * 1.2; out.push([Math.cos(a) * d, Math.sin(a) * d, 0]); }
      }
      return out; }, note: "No straight line separates a disc from a ring. With 3 or more hidden neurons, the network builds a closed boundary from several straight pieces." },
    xor: { label: "XOR quadrants", make: function (r) {
      var out = [], i, x, y;
      for (i = 0; i < 200; i++) {
        x = r() * 7 - 3.5; y = r() * 7 - 3.5;
        if (Math.abs(x) < 0.3 || Math.abs(y) < 0.3) { i--; continue; }
        out.push([x, y, x * y > 0 ? 1 : 0]);
      }
      return out; }, note: "The XOR problem with many points. One hidden layer of 2 to 4 neurons is enough, as Level 7 showed by hand." },
    spiral: { label: "Two spirals", make: function (r) {
      var out = [], i, t, k;
      for (k = 0; k < 2; k++) for (i = 0; i < 100; i++) {
        t = i / 100 * 3.2 * Math.PI;
        var rad = 0.35 + t * 0.32;
        out.push([rad * Math.cos(t + k * Math.PI) + gauss(r) * 0.12, rad * Math.sin(t + k * Math.PI) + gauss(r) * 0.12, k]);
      }
      return out; }, note: "The hard one. Try 2 hidden layers of 8 tanh neurons and give it a few thousand epochs. With 1 layer of 2 neurons it never gets there." }
  };

  function el(tag, cls, txt) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (txt !== undefined && txt !== null) n.textContent = txt;
    return n;
  }

  var ACT = {
    tanh: { f: function (z) { return Math.tanh(z); }, d: function (a) { return 1 - a * a; } },
    relu: { f: function (z) { return z > 0 ? z : 0; }, d: function (a) { return a > 0 ? 1 : 0; } },
    sigmoid: { f: function (z) { return 1 / (1 + Math.exp(-z)); }, d: function (a) { return a * (1 - a); } }
  };

  function Net(sizes, act, seed) {
    var r = rng(seed), l, i, j;
    this.sizes = sizes; this.act = act; this.W = []; this.b = []; this.vW = []; this.vb = [];
    for (l = 0; l < sizes.length - 1; l++) {
      var n = sizes[l], m = sizes[l + 1], scale = Math.sqrt((act === "relu" ? 2 : 1) / n);
      var Wl = [], vWl = [];
      for (j = 0; j < m; j++) {
        var row = [], vrow = [];
        for (i = 0; i < n; i++) { row.push(gauss(r) * scale); vrow.push(0); }
        Wl.push(row); vWl.push(vrow);
      }
      this.W.push(Wl); this.vW.push(vWl);
      this.b.push(new Array(m).fill(act === "relu" && l < sizes.length - 2 ? 0.05 : 0));
      this.vb.push(new Array(m).fill(0));
    }
  }
  Net.prototype.forward = function (x) {
    var acts = [x], l, j, i, L = this.W.length, a = x;
    for (l = 0; l < L; l++) {
      var out = new Array(this.W[l].length);
      for (j = 0; j < out.length; j++) {
        var z = this.b[l][j], row = this.W[l][j];
        for (i = 0; i < a.length; i++) z += row[i] * a[i];
        out[j] = l === L - 1 ? 1 / (1 + Math.exp(-z)) : ACT[this.act].f(z);
      }
      acts.push(out); a = out;
    }
    return acts;
  };
  Net.prototype.train = function (data, lr) {
    var L = this.W.length, gW = [], gb = [], l, j, i, loss = 0, right = 0, self = this;
    for (l = 0; l < L; l++) {
      gW.push(this.W[l].map(function (row) { return row.map(function () { return 0; }); }));
      gb.push(this.b[l].map(function () { return 0; }));
    }
    data.forEach(function (p) {
      var acts = self.forward([p[0], p[1]]), out = acts[L][0], y = p[2];
      var pc = Math.min(1 - 1e-7, Math.max(1e-7, out));
      loss -= y * Math.log(pc) + (1 - y) * Math.log(1 - pc);
      if ((out > 0.5 ? 1 : 0) === y) right++;
      var delta = [out - y];                       // dLoss/dz at the sigmoid output
      for (l = L - 1; l >= 0; l--) {
        var prev = acts[l], nd = l > 0 ? new Array(prev.length).fill(0) : null;
        for (j = 0; j < delta.length; j++) {
          gb[l][j] += delta[j];
          for (i = 0; i < prev.length; i++) {
            gW[l][j][i] += delta[j] * prev[i];
            if (nd) nd[i] += delta[j] * self.W[l][j][i];
          }
        }
        if (nd) { for (i = 0; i < nd.length; i++) nd[i] *= ACT[self.act].d(prev[i]); delta = nd; }
      }
    });
    var n = data.length;
    for (l = 0; l < L; l++) for (j = 0; j < this.W[l].length; j++) {
      for (i = 0; i < this.W[l][j].length; i++) {
        this.vW[l][j][i] = 0.9 * this.vW[l][j][i] + gW[l][j][i] / n;
        this.W[l][j][i] -= lr * this.vW[l][j][i];
      }
      this.vb[l][j] = 0.9 * this.vb[l][j] + gb[l][j] / n;
      this.b[l][j] -= lr * this.vb[l][j];
    }
    return { loss: loss / n, acc: right / n };
  };

  function build(body) {
    body.textContent = "";
    var st = { data: "circle", layers: 1, width: 4, act: "tanh", lr: 0.1, epoch: 0, running: false,
               raf: 0, seed: 1, last: { loss: NaN, acc: NaN } };

    var row = el("div", "tool-row");
    function field(label, ctrl) {
      var f = el("div", "tool-field"), id = "np-" + Math.random().toString(36).slice(2, 8);
      var l = el("label", null, label); l.setAttribute("for", id); ctrl.id = id;
      f.appendChild(l); f.appendChild(ctrl); row.appendChild(f); return f;
    }
    function select(opts, val) {
      var s = el("select");
      opts.forEach(function (o) { var e = el("option", null, o[1]); e.value = String(o[0]); s.appendChild(e); });
      s.value = String(val); return s;
    }
    var sData = select(Object.keys(DATA).map(function (k) { return [k, DATA[k].label]; }), st.data);
    var sLayers = select([[1, "1"], [2, "2"], [3, "3"]], st.layers);
    var sWidth = select([[1, "1"], [2, "2"], [3, "3"], [4, "4"], [6, "6"], [8, "8"]], st.width);
    var sAct = select([["tanh", "tanh"], ["relu", "ReLU"], ["sigmoid", "sigmoid"]], st.act);
    var rLr = el("input"); rLr.type = "range"; rLr.min = "-2.5"; rLr.max = "0.3"; rLr.step = "0.05";
    field("Data", sData); field("Hidden layers", sLayers); field("Neurons per layer", sWidth);
    field("Activation", sAct);
    var lrF = field("Learning rate", rLr), lrOut = el("output", "np-lr"); lrF.appendChild(lrOut);

    var btns = el("div", "tool-btns");
    function button(label, primary) {
      var b = el("button", "tool-btn" + (primary ? " is-primary" : ""), label);
      b.type = "button"; btns.appendChild(b); return b;
    }
    var bPlay = button("Train", true), bStep = button("One step"), bReset = button("New random weights");

    var wrap = el("div", "np-wrap");
    var canvas = el("canvas", "np-plot"); canvas.width = 300; canvas.height = 300;
    canvas.setAttribute("role", "img"); canvas.setAttribute("aria-label", "The data and the network's decision regions");
    var side = el("div", "np-side");
    var stats = el("div", "np-stats");
    var sE = el("div", "np-stat"), sL = el("div", "np-stat"), sA = el("div", "np-stat");
    stats.appendChild(sE); stats.appendChild(sL); stats.appendChild(sA);
    var netSvg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    netSvg.setAttribute("viewBox", "0 0 320 190"); netSvg.setAttribute("class", "np-net");
    netSvg.setAttribute("role", "img"); netSvg.setAttribute("aria-label", "The network's layers and weights");
    side.appendChild(stats); side.appendChild(netSvg);
    wrap.appendChild(canvas); wrap.appendChild(side);
    var status = el("p", "tool-status"); status.setAttribute("role", "status"); status.setAttribute("aria-live", "polite");
    var note = el("p", "tool-note");

    var data = [], net = null, R = 4.2;
    function setLr(v) { st.lr = v; rLr.value = String(Math.log(v) / Math.LN10); lrOut.textContent = v < 0.1 ? v.toFixed(3) : v.toFixed(2); }
    function reset() {
      var sizes = [2]; for (var l = 0; l < st.layers; l++) sizes.push(st.width); sizes.push(1);
      net = new Net(sizes, st.act, st.seed * 7919 + st.layers * 31 + st.width);
      st.epoch = 0; st.last = { loss: NaN, acc: NaN }; draw(); drawNet(); stats_();
    }
    function load() { data = DATA[st.data].make(rng(17)); note.textContent = DATA[st.data].note; reset(); }
    function stats_() {
      sE.innerHTML = "<span>Epoch</span><b>" + st.epoch + "</b>";
      sL.innerHTML = "<span>Training loss</span><b>" + (isNaN(st.last.loss) ? "&ndash;" : st.last.loss.toFixed(3)) + "</b>";
      sA.innerHTML = "<span>Accuracy</span><b>" + (isNaN(st.last.acc) ? "&ndash;" : Math.round(st.last.acc * 100) + "%") + "</b>";
    }

    var G = 60, img = null, ictx = null, off = document.createElement("canvas");
    off.width = G; off.height = G;
    function draw() {
      var ctx = canvas.getContext("2d"), W = canvas.width, i, j;
      ictx = off.getContext("2d"); img = img || ictx.createImageData(G, G);
      var d = img.data, k = 0;
      for (j = 0; j < G; j++) for (i = 0; i < G; i++) {
        var x = -R + 2 * R * (i + 0.5) / G, y = R - 2 * R * (j + 0.5) / G;
        var p = net.forward([x, y])[net.W.length][0], c, u;
        if (p < 0.5) { u = p / 0.5; c = [BLUE[0] + (MID[0] - BLUE[0]) * u, BLUE[1] + (MID[1] - BLUE[1]) * u, BLUE[2] + (MID[2] - BLUE[2]) * u]; }
        else { u = (p - 0.5) / 0.5; c = [MID[0] + (PINK[0] - MID[0]) * u, MID[1] + (PINK[1] - MID[1]) * u, MID[2] + (PINK[2] - MID[2]) * u]; }
        d[k++] = c[0]; d[k++] = c[1]; d[k++] = c[2]; d[k++] = 150;
      }
      ictx.putImageData(img, 0, 0);
      ctx.clearRect(0, 0, W, W);
      ctx.imageSmoothingEnabled = true;
      ctx.drawImage(off, 0, 0, W, W);
      data.forEach(function (p) {
        var x = (p[0] + R) / (2 * R) * W, y = (R - p[1]) / (2 * R) * W;
        ctx.beginPath(); ctx.arc(x, y, 3.4, 0, Math.PI * 2);
        ctx.fillStyle = p[2] ? "rgb(190,24,93)" : "rgb(29,78,216)"; ctx.fill();
        ctx.lineWidth = 1.2; ctx.strokeStyle = "#ffffff"; ctx.stroke();
      });
    }
    function drawNet() {
      while (netSvg.firstChild) netSvg.removeChild(netSvg.firstChild);
      var sizes = net.sizes, NSs = "http://www.w3.org/2000/svg", pos = [], l, j, i;
      for (l = 0; l < sizes.length; l++) {
        var x = 24 + l * (272 / (sizes.length - 1)), col = [];
        for (j = 0; j < sizes[l]; j++) col.push([x, 95 + (j - (sizes[l] - 1) / 2) * Math.min(22, 170 / sizes[l])]);
        pos.push(col);
      }
      for (l = 0; l < net.W.length; l++) for (j = 0; j < net.W[l].length; j++) for (i = 0; i < net.W[l][j].length; i++) {
        var w = net.W[l][j][i], ln = document.createElementNS(NSs, "line");
        ln.setAttribute("x1", pos[l][i][0]); ln.setAttribute("y1", pos[l][i][1]);
        ln.setAttribute("x2", pos[l + 1][j][0]); ln.setAttribute("y2", pos[l + 1][j][1]);
        ln.setAttribute("stroke", w >= 0 ? "#BE185D" : "#1D4ED8");
        ln.setAttribute("stroke-width", Math.min(6, 0.4 + Math.abs(w) * 1.4).toFixed(2));
        ln.setAttribute("stroke-opacity", "0.7");
        netSvg.appendChild(ln);
      }
      pos.forEach(function (col, l2) {
        col.forEach(function (p) {
          var c = document.createElementNS(NSs, "circle");
          c.setAttribute("cx", p[0]); c.setAttribute("cy", p[1]); c.setAttribute("r", "7");
          c.setAttribute("fill", l2 === 0 ? "#1D4ED8" : l2 === pos.length - 1 ? "#C2410C" : "#6D28D9");
          c.setAttribute("stroke", "#ffffff"); c.setAttribute("stroke-width", "1.5");
          netSvg.appendChild(c);
        });
      });
      var t1 = document.createElementNS(NSs, "text"); t1.setAttribute("x", "24"); t1.setAttribute("y", "186");
      t1.setAttribute("class", "np-lab"); t1.setAttribute("text-anchor", "middle"); t1.textContent = "x, y";
      netSvg.appendChild(t1);
      var t2 = document.createElementNS(NSs, "text"); t2.setAttribute("x", "296"); t2.setAttribute("y", "186");
      t2.setAttribute("class", "np-lab"); t2.setAttribute("text-anchor", "middle"); t2.textContent = "output";
      netSvg.appendChild(t2);
    }

    function stepN(n) {
      for (var k = 0; k < n; k++) { st.last = net.train(data, st.lr); st.epoch++; }
      if (!isFinite(st.last.loss)) { st.running = false; bPlay.textContent = "Train"; status.textContent = "The loss blew up: the learning rate is too high. Lower it and press New random weights."; }
    }
    var frame = 0;
    function loop() {
      st.raf = 0;
      if (!st.running) return;
      stepN(4); frame++;
      draw(); stats_(); if (frame % 6 === 0) drawNet();
      if (st.epoch >= 5000) { st.running = false; bPlay.textContent = "Train"; status.textContent = "Stopped after 5,000 epochs."; drawNet(); return; }
      st.raf = requestAnimationFrame(loop);
    }

    bPlay.addEventListener("click", function () {
      st.running = !st.running; bPlay.textContent = st.running ? "Pause" : "Train";
      status.textContent = st.running ? "Training: forward pass, loss, backpropagation, update, over and over." :
        "Paused at epoch " + st.epoch + ".";
      if (st.running && !st.raf) st.raf = requestAnimationFrame(loop);
      if (!st.running) drawNet();
    });
    bStep.addEventListener("click", function () { stepN(1); draw(); drawNet(); stats_(); });
    bReset.addEventListener("click", function () { st.seed += 1; reset(); status.textContent = "New random weights. Press Train."; });
    sData.addEventListener("change", function () { st.data = sData.value; load(); });
    sLayers.addEventListener("change", function () { st.layers = +sLayers.value; reset(); });
    sWidth.addEventListener("change", function () { st.width = +sWidth.value; reset(); });
    sAct.addEventListener("change", function () { st.act = sAct.value; reset(); });
    rLr.addEventListener("input", function () { setLr(Math.pow(10, +rLr.value)); });

    body.appendChild(row); body.appendChild(btns); body.appendChild(wrap);
    body.appendChild(status); body.appendChild(note);
    setLr(st.lr); load();
    status.textContent = "Press Train and watch the boundary form.";
  }

  function init() {
    var mounts = document.querySelectorAll('.tool[data-tool="network-playground"]');
    Array.prototype.forEach.call(mounts, function (m) {
      var b = m.querySelector(".tool-body");
      if (b) build(b);
    });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
