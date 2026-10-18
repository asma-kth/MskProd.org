/* Convolution lab: draw a picture, choose or edit a 3 × 3 kernel, and see the
 * feature map it produces.
 *
 * Hovering over (or focusing) a cell of the feature map outlines the patch of
 * the picture it came from and writes out the nine products, so the sliding
 * dot product of the lesson becomes something the student can check by hand.
 */
(function () {
  "use strict";

  var N = 12, NS = "http://www.w3.org/2000/svg";
  var KERNELS = {
    vertical: { label: "Vertical edges", k: [[-1, 0, 1], [-2, 0, 2], [-1, 0, 1]] },
    horizontal: { label: "Horizontal edges", k: [[-1, -2, -1], [0, 0, 0], [1, 2, 1]] },
    diagonal: { label: "Diagonal", k: [[2, -1, -1], [-1, 2, -1], [-1, -1, 2]] },
    blur: { label: "Blur", k: [[1 / 9, 1 / 9, 1 / 9], [1 / 9, 1 / 9, 1 / 9], [1 / 9, 1 / 9, 1 / 9]] },
    sharpen: { label: "Sharpen", k: [[0, -1, 0], [-1, 5, -1], [0, -1, 0]] },
    identity: { label: "Identity", k: [[0, 0, 0], [0, 1, 0], [0, 0, 0]] }
  };
  function blank() { var g = [], i; for (i = 0; i < N; i++) g.push(new Array(N).fill(0)); return g; }
  var PICTURES = {
    house: function () {
      var g = blank(), r, c;
      for (r = 6; r < 11; r++) for (c = 3; c < 9; c++) g[r][c] = 1;
      for (r = 2; r < 6; r++) for (c = 6 - (r - 1); c < 6 + (r - 1); c++) g[r][c] = 1;
      g[8][5] = g[8][6] = g[9][5] = g[9][6] = g[10][5] = g[10][6] = 0;
      return g; },
    letterT: function () {
      var g = blank(), i;
      for (i = 2; i < 10; i++) g[2][i] = g[3][i] = 1;
      for (i = 4; i < 11; i++) g[i][5] = g[i][6] = 1;
      return g; },
    diagonal: function () {
      var g = blank(), i;
      for (i = 1; i < 11; i++) { g[i][i] = 1; if (i + 1 < N) g[i][i + 1] = 1; }
      return g; },
    smile: function () {
      var g = blank(), i;
      g[3][3] = g[3][4] = g[4][3] = g[4][4] = 1; g[3][7] = g[3][8] = g[4][7] = g[4][8] = 1;
      for (i = 3; i < 9; i++) g[8][i] = 1;
      g[7][2] = g[7][9] = 1;
      return g; },
    empty: blank
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
  function fmt(v) {
    var r = Math.round(v * 100) / 100;
    return (r < 0 ? "−" : "") + Math.abs(r).toString();
  }
  function diverging(t) {
    t = Math.max(-1, Math.min(1, t));
    var a = [29, 78, 216], m = [243, 244, 246], b = [190, 24, 93], c, u;
    if (t < 0) { u = t + 1; c = [a[0] + (m[0] - a[0]) * u, a[1] + (m[1] - a[1]) * u, a[2] + (m[2] - a[2]) * u]; }
    else { u = t; c = [m[0] + (b[0] - m[0]) * u, m[1] + (b[1] - m[1]) * u, m[2] + (b[2] - m[2]) * u]; }
    return "rgb(" + Math.round(c[0]) + "," + Math.round(c[1]) + "," + Math.round(c[2]) + ")";
  }

  function build(body) {
    body.textContent = "";
    var st = { img: PICTURES.house(), k: KERNELS.vertical.k.map(function (r) { return r.slice(); }),
               relu: false, pad: 0, stride: 1, paint: null, hover: null };

    var row = el("div", "tool-row");
    function field(label, ctrl) {
      var f = el("div", "tool-field"), id = "cv-" + Math.random().toString(36).slice(2, 8);
      var l = el("label", null, label); l.setAttribute("for", id); ctrl.id = id;
      f.appendChild(l); f.appendChild(ctrl); row.appendChild(f); return f;
    }
    var sPic = el("select");
    [["house", "House"], ["letterT", "Letter T"], ["diagonal", "Diagonal line"], ["smile", "Smile"], ["empty", "Empty: draw your own"]]
      .forEach(function (p) { var o = el("option", null, p[1]); o.value = p[0]; sPic.appendChild(o); });
    field("Picture", sPic);
    var sKer = el("select");
    Object.keys(KERNELS).forEach(function (k) { var o = el("option", null, KERNELS[k].label); o.value = k; sKer.appendChild(o); });
    var oc = el("option", null, "Custom"); oc.value = "custom"; sKer.appendChild(oc);
    field("Kernel", sKer);
    var sPad = el("select");
    [["0", "0 (valid)"], ["1", "1 (same size)"]].forEach(function (p) { var o = el("option", null, p[1]); o.value = p[0]; sPad.appendChild(o); });
    field("Padding", sPad);
    var sStr = el("select");
    [["1", "1"], ["2", "2"]].forEach(function (p) { var o = el("option", null, p[1]); o.value = p[0]; sStr.appendChild(o); });
    field("Stride", sStr);
    var relu = el("input"); relu.type = "checkbox";
    var rf = el("div", "tool-field cv-check"), rl = el("label", null, " Apply ReLU");
    var rid = "cv-relu-" + Math.random().toString(36).slice(2, 8); relu.id = rid; rl.setAttribute("for", rid);
    rl.insertBefore(relu, rl.firstChild); rf.appendChild(rl); row.appendChild(rf);

    var wrap = el("div", "cv-wrap");
    var left = el("div", "cv-col"), mid = el("div", "cv-col cv-kcol"), right = el("div", "cv-col");
    left.appendChild(el("p", "cv-cap", "Picture: click or drag to draw"));
    var inSvg = sv("svg", { viewBox: "0 0 " + N * 20 + " " + N * 20, "class": "cv-grid", role: "img",
                             "aria-label": "Drawable picture, 12 by 12 pixels" });
    left.appendChild(inSvg);
    mid.appendChild(el("p", "cv-cap", "Kernel"));
    var kGrid = el("div", "cv-kernel");
    var kInputs = [];
    for (var i = 0; i < 3; i++) for (var j = 0; j < 3; j++) {
      var inp = el("input"); inp.type = "number"; inp.step = "0.5"; inp.setAttribute("aria-label", "Kernel weight row " + (i + 1) + " column " + (j + 1));
      kGrid.appendChild(inp); kInputs.push(inp);
    }
    mid.appendChild(kGrid);
    right.appendChild(el("p", "cv-cap", "Feature map: hover a cell"));
    var outSvg = sv("svg", { "class": "cv-grid", role: "img", "aria-label": "Feature map" });
    right.appendChild(outSvg);
    wrap.appendChild(left); wrap.appendChild(mid); wrap.appendChild(right);
    var work = el("p", "tool-working cv-work");
    var status = el("p", "tool-status"); status.setAttribute("role", "status"); status.setAttribute("aria-live", "polite");

    function syncInputs() { kInputs.forEach(function (inp, n) { inp.value = fmt(st.k[Math.floor(n / 3)][n % 3]).replace("−", "-"); }); }
    function conv() {
      var pad = st.pad, s = st.stride, size = Math.floor((N + 2 * pad - 3) / s) + 1, out = [], r, c, i2, j2;
      function px(rr, cc) { rr -= pad; cc -= pad; return rr < 0 || cc < 0 || rr >= N || cc >= N ? 0 : st.img[rr][cc]; }
      for (r = 0; r < size; r++) {
        var line = [];
        for (c = 0; c < size; c++) {
          var sum = 0;
          for (i2 = 0; i2 < 3; i2++) for (j2 = 0; j2 < 3; j2++) sum += px(r * s + i2, c * s + j2) * st.k[i2][j2];
          line.push(st.relu ? Math.max(0, sum) : sum);
        }
        out.push(line);
      }
      return out;
    }
    function render() {
      while (inSvg.firstChild) inSvg.removeChild(inSvg.firstChild);
      var r, c;
      for (r = 0; r < N; r++) for (c = 0; c < N; c++) {
        inSvg.appendChild(sv("rect", { x: c * 20 + 1, y: r * 20 + 1, width: 18, height: 18, rx: 3,
          "class": st.img[r][c] ? "cv-on" : "cv-off", "data-r": r, "data-c": c }));
      }
      var out = conv(), size = out.length, hi = 0;
      out.forEach(function (rw) { rw.forEach(function (v) { hi = Math.max(hi, Math.abs(v)); }); });
      while (outSvg.firstChild) outSvg.removeChild(outSvg.firstChild);
      outSvg.setAttribute("viewBox", "0 0 " + size * 20 + " " + size * 20);
      for (r = 0; r < size; r++) for (c = 0; c < size; c++) {
        var v = out[r][c], cell = sv("rect", { x: c * 20 + 1, y: r * 20 + 1, width: 18, height: 18, rx: 3,
          fill: diverging(hi ? v / hi : 0), "data-r": r, "data-c": c, tabindex: (r === 0 && c === 0) ? "0" : "-1",
          "class": "cv-out" });
        outSvg.appendChild(cell);
      }
      status.textContent = "Feature map " + size + " × " + size + ". Strongest response " + fmt(hi) + ".";
      st.size = size;
      paintHover();
    }
    // Only the outlines and the working change on hover, so the cells under
    // the pointer are never rebuilt while it moves.
    function paintHover() {
      Array.prototype.forEach.call(wrap.querySelectorAll(".cv-hl"), function (n) { n.parentNode.removeChild(n); });
      var size = st.size;
      if (st.hover && st.hover[0] < size && st.hover[1] < size) {
        var hr = st.hover[0], hc = st.hover[1];
        outSvg.appendChild(sv("rect", { x: hc * 20, y: hr * 20, width: 20, height: 20, rx: 3, "class": "cv-hl" }));
        var top = hr * st.stride - st.pad, lft = hc * st.stride - st.pad;
        inSvg.appendChild(sv("rect", { x: lft * 20, y: top * 20, width: 60, height: 60, rx: 4, "class": "cv-hl" }));
        var terms = [], i3, j3, sum = 0;
        for (i3 = 0; i3 < 3; i3++) for (j3 = 0; j3 < 3; j3++) {
          var rr = top + i3, cc = lft + j3, p = (rr < 0 || cc < 0 || rr >= N || cc >= N) ? 0 : st.img[rr][cc];
          if (st.k[i3][j3] !== 0 && p !== 0) terms.push(p + "×" + fmt(st.k[i3][j3]));
          sum += p * st.k[i3][j3];
        }
        work.textContent = "Cell (" + (hr + 1) + ", " + (hc + 1) + "): " + (terms.length ? terms.join(" + ") : "every product is 0") +
          " = " + fmt(sum) + (st.relu ? ", after ReLU " + fmt(Math.max(0, sum)) : "");
      } else {
        work.textContent = "Hover over, or tab to, a cell of the feature map to see its sum worked out. Pixels are 1 where drawn and 0 elsewhere.";
      }
    }

    function cellAt(svgEl, ev) {
      var t = ev.target;
      if (t && t.getAttribute && t.getAttribute("data-r") !== null) return [+t.getAttribute("data-r"), +t.getAttribute("data-c")];
      return null;
    }
    inSvg.addEventListener("pointerdown", function (ev) {
      var c = cellAt(inSvg, ev); if (!c) return;
      st.paint = ev.shiftKey || ev.button === 2 ? 0 : (st.img[c[0]][c[1]] ? 0 : 1);
      st.img[c[0]][c[1]] = st.paint; inSvg.setPointerCapture(ev.pointerId); sPic.value = "empty"; render();
    });
    inSvg.addEventListener("pointermove", function (ev) {
      if (st.paint === null) return;
      var r = inSvg.getBoundingClientRect(), x = Math.floor((ev.clientX - r.left) / r.width * N), y = Math.floor((ev.clientY - r.top) / r.height * N);
      if (x >= 0 && y >= 0 && x < N && y < N && st.img[y][x] !== st.paint) { st.img[y][x] = st.paint; render(); }
    });
    inSvg.addEventListener("pointerup", function () { st.paint = null; });
    inSvg.addEventListener("contextmenu", function (ev) { ev.preventDefault(); });
    function hoverFrom(ev) {
      var c = cellAt(outSvg, ev);
      if (c && !(st.hover && st.hover[0] === c[0] && st.hover[1] === c[1])) { st.hover = c; paintHover(); }
    }
    outSvg.addEventListener("pointermove", hoverFrom);
    outSvg.addEventListener("focusin", hoverFrom);
    outSvg.addEventListener("keydown", function (ev) {
      if (!st.hover) st.hover = [0, 0];
      var size = st.size, r = st.hover[0], c = st.hover[1], used = true;
      if (ev.key === "ArrowRight") c = Math.min(size - 1, c + 1); else if (ev.key === "ArrowLeft") c = Math.max(0, c - 1);
      else if (ev.key === "ArrowDown") r = Math.min(size - 1, r + 1); else if (ev.key === "ArrowUp") r = Math.max(0, r - 1);
      else used = false;
      if (used) { ev.preventDefault(); st.hover = [r, c]; paintHover(); var t = outSvg.querySelector('[data-r="' + r + '"][data-c="' + c + '"]'); if (t) t.focus(); }
    });
    kInputs.forEach(function (inp, n) {
      inp.addEventListener("input", function () {
        var v = parseFloat(inp.value); if (isNaN(v)) return;
        st.k[Math.floor(n / 3)][n % 3] = v; sKer.value = "custom"; render();
      });
    });
    sPic.addEventListener("change", function () { st.img = PICTURES[sPic.value](); render(); });
    sKer.addEventListener("change", function () {
      if (sKer.value === "custom") return;
      st.k = KERNELS[sKer.value].k.map(function (r) { return r.slice(); }); syncInputs(); render();
    });
    sPad.addEventListener("change", function () { st.pad = +sPad.value; st.hover = null; render(); });
    sStr.addEventListener("change", function () { st.stride = +sStr.value; st.hover = null; render(); });
    relu.addEventListener("change", function () { st.relu = relu.checked; render(); });

    body.appendChild(row); body.appendChild(wrap); body.appendChild(work); body.appendChild(status);
    syncInputs(); render();
  }

  function init() {
    var mounts = document.querySelectorAll('.tool[data-tool="convolution-lab"]');
    Array.prototype.forEach.call(mounts, function (m) {
      var b = m.querySelector(".tool-body");
      if (b) build(b);
    });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
