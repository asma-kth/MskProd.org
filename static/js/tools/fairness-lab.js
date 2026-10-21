/* Fairness lab: one model, two groups, and the thresholds that decide.
 *
 * 200 simulated applicants per group, each with a score and whether they
 * would really repay. Group B has a lower base rate, so no single setting
 * can make every fairness measure equal at once: the lab lets the student
 * find that out by moving the thresholds or pressing the "equalise" buttons.
 * An optional measurement bias makes the model under-score group B.
 */
(function () {
  "use strict";

  var NS = "http://www.w3.org/2000/svg";

  function rng(seed) {
    return function () {
      seed |= 0; seed = seed + 0x6D2B79F5 | 0;
      var t = Math.imul(seed ^ seed >>> 15, 1 | seed);
      t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
    };
  }
  function gauss(r) { return Math.sqrt(-2 * Math.log(r() || 1e-9)) * Math.cos(2 * Math.PI * r()); }
  function makeGroup(seed, base) {
    var r = rng(seed), people = [];
    for (var i = 0; i < 200; i++) {
      var good = r() < base;
      var s = (good ? 0.62 : 0.40) + 0.14 * gauss(r);
      people.push({ s: Math.max(0.01, Math.min(0.99, s)), good: good, jitter: r() });
    }
    return people;
  }
  var GROUPS = [{ name: "group A", base: 0.5, people: makeGroup(11, 0.5), cls: "fl-a" },
                { name: "group B", base: 0.3, people: makeGroup(29, 0.3), cls: "fl-b" }];

  function el(tag, cls, txt) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (txt !== undefined && txt !== null) n.textContent = txt;
    return n;
  }
  function sv(tag, attrs) {
    var n = document.createElementNS(NS, tag);
    for (var k in attrs) if (Object.prototype.hasOwnProperty.call(attrs, k)) n.setAttribute(k, attrs[k]);
    return n;
  }
  function pct(v) { return isFinite(v) ? Math.round(100 * v) + "%" : "–"; }
  function textWidth(s) { return s.length * 6.6; }

  function build(body) {
    body.textContent = "";
    var st = { t: [0.5, 0.5], bias: false };

    function score(g, p) { return g === 1 && st.bias ? Math.max(0.01, p.s - 0.07) : p.s; }
    function metrics(g) {
      var tp = 0, fp = 0, fn = 0, tn = 0;
      GROUPS[g].people.forEach(function (p) {
        var yes = score(g, p) >= st.t[g];
        if (yes && p.good) tp++; else if (yes) fp++; else if (p.good) fn++; else tn++;
      });
      var n = tp + fp + fn + tn;
      return { sel: (tp + fp) / n, tpr: tp / (tp + fn), fpr: fp / (fp + tn), prec: tp / (tp + fp), acc: (tp + tn) / n };
    }

    var row = el("div", "tool-row");
    function field(label, ctrl, out) {
      var f = el("div", "tool-field"), id = "fl-" + Math.random().toString(36).slice(2, 8);
      var l = el("label", null, label); l.setAttribute("for", id); ctrl.id = id;
      f.appendChild(l); f.appendChild(ctrl); if (out) f.appendChild(out); row.appendChild(f); return f;
    }
    function slider() { var s = el("input"); s.type = "range"; s.min = "0.05"; s.max = "0.95"; s.step = "0.01"; s.value = "0.5"; return s; }
    var sA = slider(), oA = el("span", "fl-num", "0.50"); field("Group A threshold", sA, oA);
    var sB = slider(), oB = el("span", "fl-num", "0.50"); field("Group B threshold", sB, oB);
    var checks = el("div", "tool-field fl-checks");
    var lab = el("label"), cBias = el("input"); cBias.type = "checkbox";
    lab.appendChild(cBias); lab.appendChild(document.createTextNode(" The model under-scores group B"));
    checks.appendChild(lab); row.appendChild(checks);

    var btns = el("div", "tool-btns");
    var bSame = el("button", "tool-btn", "Same threshold for both"); bSame.type = "button";
    var bDP = el("button", "tool-btn", "Equalise approval rates"); bDP.type = "button";
    var bEO = el("button", "tool-btn", "Equalise true positive rates"); bEO.type = "button";
    var bPP = el("button", "tool-btn", "Equalise precision"); bPP.type = "button";
    [bSame, bDP, bEO, bPP].forEach(function (b) { btns.appendChild(b); });

    // a phone gets a narrower drawing, so the dots and labels stay a readable size
    var W = 640, H = 236, X0 = 70, X1 = 620, narrow = false;
    function isNarrow() { return (body.clientWidth || 640) < 520; }
    var svg = sv("svg", { viewBox: "0 0 " + W + " " + H, "class": "fl-plot", role: "img",
                          "aria-label": "Applicants in two groups placed by their score, with each group's threshold." });
    var table = el("table", "fl-table"), wrap = el("div", "fl-scroll");
    wrap.appendChild(table);
    var status = el("p", "tool-status"); status.setAttribute("role", "status"); status.setAttribute("aria-live", "polite");
    var note = el("p", "tool-note", "Each dot is an applicant: filled dots would repay, hollow dots would not, and everyone right of their group's line is approved. Group B has fewer applicants who would repay, so try to make every measure equal at once.");

    function x(s) { return X0 + s * (X1 - X0); }
    function draw() {
      narrow = isNarrow();
      W = narrow ? 340 : 640; X0 = narrow ? 30 : 70; X1 = W - 20;
      svg.setAttribute("viewBox", "0 0 " + W + " " + H);
      while (svg.firstChild) svg.removeChild(svg.firstChild);
      for (var v = 0; v <= 1.001; v += 0.25) {
        svg.appendChild(sv("line", { x1: x(v), y1: 10, x2: x(v), y2: 210, "class": "fl-grid" }));
        var tl = sv("text", { x: x(v), y: 226, "text-anchor": "middle", "class": "fl-axis" }); tl.textContent = v.toFixed(2); svg.appendChild(tl);
      }
      GROUPS.forEach(function (G, g) {
        var y0 = 24 + g * 100;
        var name = sv("text", { x: 8, y: y0 + 42, "class": "fl-name " + G.cls });
        name.textContent = narrow ? G.name.slice(-1) : G.name; svg.appendChild(name);
        G.people.forEach(function (p) {
          var s = score(g, p), yes = s >= st.t[g];
          svg.appendChild(sv("circle", { cx: x(s).toFixed(1), cy: (y0 + 6 + p.jitter * 70).toFixed(1), r: 3.6,
                                         "class": "fl-dot " + G.cls + (p.good ? " is-good" : "") + (yes ? "" : " is-out") }));
        });
        var tx = x(st.t[g]), label = "approved →";
        svg.appendChild(sv("line", { x1: tx, y1: y0 - 4, x2: tx, y2: y0 + 82, "class": "fl-thresh " + G.cls }));
        // near the right edge the label goes on the left of the line, still pointing right
        var right = tx + 5 + textWidth(label) <= W - 4;
        var ap = sv("text", { x: right ? tx + 5 : tx - 5, y: y0 - 8, "text-anchor": right ? "start" : "end", "class": "fl-approve" });
        ap.textContent = label; svg.appendChild(ap);
      });
    }
    function render() {
      oA.textContent = st.t[0].toFixed(2); oB.textContent = st.t[1].toFixed(2);
      sA.value = st.t[0]; sB.value = st.t[1];
      draw();
      var m = [metrics(0), metrics(1)];
      table.textContent = "";
      var thead = el("thead"), hr = el("tr");
      hr.appendChild(el("th", null, "measure"));
      GROUPS.forEach(function (G) { hr.appendChild(el("th", G.cls, G.name)); });
      hr.appendChild(el("th", null, "gap"));
      thead.appendChild(hr); table.appendChild(thead);
      var tb = el("tbody"), ok = {};
      [["sel", "approved"], ["tpr", "true positive rate"], ["fpr", "false positive rate"],
       ["prec", "precision"], ["acc", "accuracy"]].forEach(function (r) {
        var k = r[0], tr = el("tr"), d = Math.abs(m[0][k] - m[1][k]);
        ok[k] = d <= 0.03;
        tr.appendChild(el("th", null, r[1]));
        tr.appendChild(el("td", null, pct(m[0][k])));
        tr.appendChild(el("td", null, pct(m[1][k])));
        tr.appendChild(isFinite(d) ? el("td", "fl-gap " + (ok[k] ? "is-ok" : "is-bad"), Math.round(100 * d) + " pts")
                                   : el("td", "fl-gap", "–"));
        tb.appendChild(tr);
      });
      table.appendChild(tb);
      // equalised odds needs both error rates to match, not just one
      var met = [];
      if (ok.sel) met.push("demographic parity");
      if (ok.tpr) met.push("equal opportunity");
      if (ok.tpr && ok.fpr) met.push("equalised odds");
      if (ok.prec) met.push("predictive parity");
      status.textContent = met.length ? "Met, to within 3 points: " + met.join(", ") + "." : "No fairness definition is met at these thresholds.";
    }
    function search(target) {
      // Keep group A's threshold and give group B the lowest threshold that
      // matches A to within a point of the best match. With only a few people
      // approved, precision jumps about, so "the exact best" can be far too strict.
      var want = target(metrics(0)), keep = st.t[1], tried = [], bestD = Infinity;
      for (var i = 0; i <= 180; i++) {
        st.t[1] = 0.05 + i * 0.005;
        var d = Math.abs(target(metrics(1)) - want);
        tried.push([st.t[1], d]);
        if (d < bestD) bestD = d;
      }
      st.t[1] = keep;
      for (var j = 0; j < tried.length; j++) {
        if (tried[j][1] <= bestD + 0.01) { st.t[1] = Math.round(tried[j][0] * 1000) / 1000; break; }
      }
      render();
    }

    sA.addEventListener("input", function () { st.t[0] = parseFloat(sA.value); render(); });
    sB.addEventListener("input", function () { st.t[1] = parseFloat(sB.value); render(); });
    cBias.addEventListener("change", function () { st.bias = cBias.checked; render(); });
    bSame.addEventListener("click", function () { st.t[1] = st.t[0]; render(); });
    bDP.addEventListener("click", function () { search(function (m) { return m.sel; }); });
    bEO.addEventListener("click", function () { search(function (m) { return m.tpr; }); });
    bPP.addEventListener("click", function () { search(function (m) { return isFinite(m.prec) ? m.prec : 0; }); });
    window.addEventListener("resize", function () { if (isNarrow() !== narrow) draw(); });

    body.appendChild(row); body.appendChild(btns); body.appendChild(svg); body.appendChild(wrap);
    body.appendChild(status); body.appendChild(note);
    render();
  }

  function init() {
    var mounts = document.querySelectorAll('.tool[data-tool="fairness-lab"]');
    Array.prototype.forEach.call(mounts, function (m) {
      var b = m.querySelector(".tool-body");
      if (b) build(b);
    });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
