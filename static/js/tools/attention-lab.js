/* Attention lab: one query, a handful of keys, and the softmax between them.
 *
 * Keys and the query are 2D arrows the student drags. Every change re-runs
 * scaled dot-product attention: the dot products, the sharpness multiplier,
 * the softmax and the blend of the values. Each token's value is a colour, so
 * the output is a colour too, mixed in proportion to the weights. A causal
 * mask can hide the tokens after a chosen position.
 */
(function () {
  "use strict";

  var NS = "http://www.w3.org/2000/svg";
  var PRESETS = {
    pronoun: {
      label: "A pronoun finds its noun",
      query: [0.55, 1.15],
      tokens: [["The", [-0.55, -0.75], "#64748B"], ["animal", [1.0, 0.6], "#DB2777"],
               ["crossed", [-0.9, 0.3], "#F59E0B"], ["the", [0.15, -1.05], "#94A3B8"],
               ["street", [0.9, -0.55], "#2563EB"], ["it", [0.25, 0.25], "#7C3AED"]]
    },
    split: {
      label: "Two good matches",
      query: [0.2, 1.2],
      tokens: [["red", [-0.6, 1.0], "#DC2626"], ["blue", [0.8, 0.9], "#2563EB"],
               ["green", [0.9, -0.8], "#16A34A"], ["gold", [-0.9, -0.7], "#F59E0B"]]
    },
    spread: {
      label: "Nothing stands out",
      query: [0.25, 0.1],
      tokens: [["one", [1, 0], "#DB2777"], ["two", [0.5, 0.87], "#F59E0B"],
               ["three", [-0.5, 0.87], "#16A34A"], ["four", [-1, 0], "#0D9488"],
               ["five", [-0.5, -0.87], "#2563EB"], ["six", [0.5, -0.87], "#7C3AED"]]
    }
  };

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
  function fmt(v, d) { return v.toFixed(d === undefined ? 2 : d).replace("-", "−"); }
  function rgb(hex) { return [1, 3, 5].map(function (i) { return parseInt(hex.slice(i, i + 2), 16); }); }
  function inkOn(hex) {
    var l = rgb(hex).map(function (v) { v /= 255; return v <= 0.03928 ? v / 12.92 : Math.pow((v + 0.055) / 1.055, 2.4); });
    return 1.05 / (0.2126 * l[0] + 0.7152 * l[1] + 0.0722 * l[2] + 0.05) >= 4.5 ? "#FFFFFF" : "#111827";
  }
  function toHex(c) { return "#" + c.map(function (v) { var s = Math.round(v).toString(16); return s.length < 2 ? "0" + s : s; }).join(""); }

  function build(body) {
    body.textContent = "";
    var st = { preset: "pronoun", q: null, toks: null, sharp: 1, maskAt: -1, drag: null };

    var row = el("div", "tool-row");
    function field(label, ctrl) {
      var f = el("div", "tool-field"), id = "al-" + Math.random().toString(36).slice(2, 8);
      var l = el("label", null, label); l.setAttribute("for", id); ctrl.id = id;
      f.appendChild(l); f.appendChild(ctrl); row.appendChild(f); return f;
    }
    var sPreset = el("select");
    Object.keys(PRESETS).forEach(function (k) { var o = el("option", null, PRESETS[k].label); o.value = k; sPreset.appendChild(o); });
    field("Example", sPreset);
    var sharp = el("input"); sharp.type = "range"; sharp.min = "0.2"; sharp.max = "4"; sharp.step = "0.05"; sharp.value = "1";
    var fSharp = field("Sharpness", sharp);
    var sharpOut = el("span", "al-num", "× 1.00"); fSharp.appendChild(sharpOut);
    var sMask = el("select");
    field("Causal mask", sMask);

    var wrap = el("div", "al-wrap");
    var plane = sv("svg", { viewBox: "0 0 320 320", "class": "al-plane", role: "group",
                            "aria-label": "The query and key vectors. Drag the round handles, or focus one and use the arrow keys." });
    var side = el("div", "al-side");
    var table = el("table", "al-table");
    var thead = el("thead"), hr = el("tr");
    ["token", "q · k", "× sharp", "weight"].forEach(function (h) { hr.appendChild(el("th", null, h)); });
    thead.appendChild(hr); table.appendChild(thead);
    var tbody = el("tbody"); table.appendChild(tbody);
    side.appendChild(table);
    var outBox = el("div", "al-out");
    var swatch = el("span", "al-swatch");
    var outText = el("p", "al-outtext");
    outBox.appendChild(swatch); outBox.appendChild(outText);
    side.appendChild(outBox);
    wrap.appendChild(plane); wrap.appendChild(side);

    var status = el("p", "tool-status"); status.setAttribute("role", "status"); status.setAttribute("aria-live", "polite");
    var note = el("p", "tool-note", "Each token's value is a colour, so the output is the colours mixed by the weights. " +
      "Sharpness multiplies every score before the softmax: dividing by √dₖ is a sharpness below 1, and turning it up makes the biggest score take everything.");

    var S = 100, O = 160;
    function toPx(v) { return [O + v[0] * S, O - v[1] * S]; }
    function fromEvent(ev) {
      var m = plane.getScreenCTM();
      if (!m) return null;
      var p = plane.createSVGPoint(); p.x = ev.clientX; p.y = ev.clientY;
      var r = p.matrixTransform(m.inverse());
      return [Math.max(-1.5, Math.min(1.5, (r.x - O) / S)), Math.max(-1.5, Math.min(1.5, (O - r.y) / S))];
    }

    function load(name) {
      var p = PRESETS[name];
      st.preset = name;
      st.q = p.query.slice();
      st.toks = p.tokens.map(function (t) { return { w: t[0], k: t[1].slice(), c: t[2] }; });
      st.maskAt = -1;
      sMask.textContent = "";
      var off = el("option", null, "Off: every token visible"); off.value = "-1"; sMask.appendChild(off);
      st.toks.forEach(function (t, i) {
        var o = el("option", null, "Query at position " + (i + 1) + " (" + t.w + ")"); o.value = String(i); sMask.appendChild(o);
      });
      sMask.value = "-1";
      drawStatic();
      update();
    }

    var handles = [];
    function arrowHead(x1, y1, x2, y2, size) {
      var a = Math.atan2(y2 - y1, x2 - x1), hx = x2 - size * Math.cos(a), hy = y2 - size * Math.sin(a);
      return [x2, y2, hx + size * 0.5 * Math.sin(a), hy - size * 0.5 * Math.cos(a), hx - size * 0.5 * Math.sin(a), hy + size * 0.5 * Math.cos(a)]
        .map(function (v) { return v.toFixed(1); }).join(" ").replace(/(\S+) (\S+)/g, "$1,$2");
    }
    function drawStatic() {
      while (plane.firstChild) plane.removeChild(plane.firstChild);
      var g = sv("g", { "class": "al-grid" });
      [-1, 0, 1].forEach(function (t) {
        g.appendChild(sv("line", { x1: O + t * S, y1: 10, x2: O + t * S, y2: 310 }));
        g.appendChild(sv("line", { x1: 10, y1: O + t * S, x2: 310, y2: O + t * S }));
      });
      g.appendChild(sv("circle", { cx: O, cy: O, r: S, "class": "al-unit" }));
      plane.appendChild(g);
      handles = [];
      st.toks.forEach(function (t, i) { plane.appendChild(makeArrow(t.c, "key of " + t.w, i)); });
      plane.appendChild(makeArrow(null, "query", -1));
    }
    function makeArrow(colour, name, idx) {
      var g = sv("g", { "class": idx < 0 ? "al-q" : "al-k" });
      var ln = sv("line", { x1: O, y1: O, "stroke-width": idx < 0 ? 4 : 3, "stroke-linecap": "round" });
      var head = sv("polygon", {});
      var lab = sv("text", { "class": "al-lab", "text-anchor": "middle" });
      lab.textContent = idx < 0 ? "query" : st.toks[idx].w;
      var h = sv("circle", { r: idx < 0 ? 9 : 7, tabindex: "0", role: "slider", "class": "al-handle",
                             "aria-label": name + ": drag, or use the arrow keys" });
      if (colour) { ln.setAttribute("stroke", colour); head.setAttribute("fill", colour); h.setAttribute("fill", colour); }
      g.appendChild(ln); g.appendChild(head); g.appendChild(lab); g.appendChild(h);
      handles.push({ idx: idx, g: g, ln: ln, head: head, lab: lab, h: h });
      h.addEventListener("pointerdown", function (ev) { ev.preventDefault(); st.drag = idx; h.setPointerCapture(ev.pointerId); });
      h.addEventListener("pointermove", function (ev) {
        if (st.drag !== idx) return;
        var v = fromEvent(ev); if (!v) return;
        if (idx < 0) st.q = v; else st.toks[idx].k = v;
        update();
      });
      h.addEventListener("pointerup", function () { st.drag = null; });
      h.addEventListener("pointercancel", function () { st.drag = null; });
      h.addEventListener("keydown", function (ev) {
        var v = idx < 0 ? st.q : st.toks[idx].k, d = ev.shiftKey ? 0.2 : 0.05, used = true;
        if (ev.key === "ArrowLeft") v[0] -= d; else if (ev.key === "ArrowRight") v[0] += d;
        else if (ev.key === "ArrowUp") v[1] += d; else if (ev.key === "ArrowDown") v[1] -= d;
        else used = false;
        if (!used) return;
        ev.preventDefault();
        v[0] = Math.max(-1.5, Math.min(1.5, v[0])); v[1] = Math.max(-1.5, Math.min(1.5, v[1]));
        update();
      });
      return g;
    }

    function compute() {
      var dots = st.toks.map(function (t) { return st.q[0] * t.k[0] + st.q[1] * t.k[1]; });
      var scaled = dots.map(function (d) { return d * st.sharp; });
      var live = st.toks.map(function (t, i) { return st.maskAt < 0 || i <= st.maskAt; });
      var m = -Infinity;
      scaled.forEach(function (v, i) { if (live[i]) m = Math.max(m, v); });
      var ex = scaled.map(function (v, i) { return live[i] ? Math.exp(v - m) : 0; });
      var tot = ex.reduce(function (a, b) { return a + b; }, 0);
      var wts = ex.map(function (e) { return e / tot; });
      var mix = [0, 0, 0];
      st.toks.forEach(function (t, i) { var c = rgb(t.c); for (var j = 0; j < 3; j++) mix[j] += wts[i] * c[j]; });
      return { dots: dots, scaled: scaled, live: live, wts: wts, mix: mix };
    }

    function update() {
      var r = compute();
      handles.forEach(function (H) {
        var v = H.idx < 0 ? st.q : st.toks[H.idx].k, p = toPx(v);
        var col = H.idx < 0 ? null : st.toks[H.idx].c;
        H.ln.setAttribute("x2", p[0]); H.ln.setAttribute("y2", p[1]);
        var len = Math.sqrt(Math.pow(p[0] - O, 2) + Math.pow(p[1] - O, 2));
        H.head.setAttribute("points", len > 14 ? arrowHead(O, O, p[0], p[1], 12) : "");
        H.h.setAttribute("cx", p[0]); H.h.setAttribute("cy", p[1]);
        var a = Math.atan2(p[1] - O, p[0] - O), ca = Math.cos(a);
        // labels sit beyond the tip, anchored so they run away from the arrow
        H.lab.setAttribute("text-anchor", ca > 0.35 ? "start" : ca < -0.35 ? "end" : "middle");
        H.lab.setAttribute("x", (p[0] + ca * 14).toFixed(1));
        H.lab.setAttribute("y", (p[1] + Math.sin(a) * 16 + 4).toFixed(1));
        H.h.setAttribute("aria-valuetext", "x " + fmt(v[0]) + ", y " + fmt(v[1]));
        if (H.idx >= 0) {
          var w = r.wts[H.idx];
          H.g.setAttribute("opacity", r.live[H.idx] ? String(0.35 + 0.65 * Math.min(1, w * 2.2)) : "0.15");
          H.ln.setAttribute("stroke-width", (2 + 6 * w).toFixed(1));
          if (col) H.ln.setAttribute("stroke", col);
        }
      });
      tbody.textContent = "";
      var best = 0;
      st.toks.forEach(function (t, i) {
        if (r.wts[i] > r.wts[best]) best = i;
        var tr = el("tr", r.live[i] ? null : "is-masked");
        var td0 = el("td"), chip = el("span", "al-chip", t.w); chip.style.background = t.c; chip.style.color = inkOn(t.c); td0.appendChild(chip);
        tr.appendChild(td0);
        tr.appendChild(el("td", "al-num", fmt(r.dots[i])));
        tr.appendChild(el("td", "al-num", r.live[i] ? fmt(r.scaled[i]) : "−∞"));
        var td3 = el("td", "al-wcell"), bar = el("span", "al-bar"), fill = el("span", "al-fill");
        fill.style.width = (100 * r.wts[i]).toFixed(1) + "%";
        bar.appendChild(fill); td3.appendChild(bar); td3.appendChild(el("span", "al-num", r.live[i] ? fmt(r.wts[i], 3) : "0"));
        tr.appendChild(td3);
        tbody.appendChild(tr);
      });
      var hex = toHex(r.mix);
      swatch.style.background = hex;
      var top = st.toks.map(function (t, i) { return [r.wts[i], t.w]; }).filter(function (p) { return p[0] >= 0.005; })
        .sort(function (a, b) { return b[0] - a[0]; }).slice(0, 3);
      var parts = top.map(function (p) { return Math.round(p[0] * 100) + "% " + p[1]; });
      var rest = 1 - top.reduce(function (a, p) { return a + p[0]; }, 0);
      if (rest >= 0.005) parts.push(Math.round(rest * 100) + "% the rest");
      var said = parts.length > 1 ? parts.slice(0, -1).join(", ") + " and " + parts[parts.length - 1] : parts[0];
      outText.textContent = "Output: the values mixed as " + said + ".";
      status.textContent = "Most attention goes to “" + st.toks[best].w + "”, weight " + fmt(r.wts[best], 3) +
        ". The weights add up to " + fmt(r.wts.reduce(function (a, b) { return a + b; }, 0), 2) + ".";
    }

    sPreset.addEventListener("change", function () { load(sPreset.value); });
    sharp.addEventListener("input", function () { st.sharp = parseFloat(sharp.value); sharpOut.textContent = "× " + fmt(st.sharp); update(); });
    sMask.addEventListener("change", function () { st.maskAt = parseInt(sMask.value, 10); update(); });

    body.appendChild(row); body.appendChild(wrap); body.appendChild(status); body.appendChild(note);
    load("pronoun");
  }

  function init() {
    var mounts = document.querySelectorAll('.tool[data-tool="attention-lab"]');
    Array.prototype.forEach.call(mounts, function (m) {
      var b = m.querySelector(".tool-body");
      if (b) build(b);
    });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
