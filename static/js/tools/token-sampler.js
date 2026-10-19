/* Token sampler: temperature, top-k and top-p on a toy language model.
 *
 * The model is a hand-written bigram table, the same idea as Level 9's
 * bigram model: the next word depends only on the last one. That keeps every
 * probability small enough to show, while the sampling settings work exactly
 * as they do on a real model. Each generated word is shaded by how likely it
 * was when it was picked, so high temperatures show up as surprising words.
 */
(function () {
  "use strict";

  var MODEL = {
    "the": { cat: 2.2, dog: 2.0, robot: 1.6, mat: 1.4, park: 1.2, sofa: 1.0, garden: 0.8, moon: -0.5 },
    "a": { cat: 1.5, dog: 1.5, robot: 1.2, time: 0.8, mat: 0.3 },
    "cat": { sat: 2.0, slept: 1.6, purred: 1.4, ran: 1.0, and: 0.3, ".": 0.2 },
    "dog": { ran: 2.0, barked: 1.8, sat: 1.0, slept: 1.0, ".": 0.2 },
    "robot": { beeped: 2.0, ran: 0.8, sat: 0.4, ".": 0.3, slept: -0.5 },
    "sat": { on: 2.5, "in": 0.8, under: 0.6, quietly: 0.4, ".": 0.0 },
    "ran": { to: 1.8, quickly: 1.2, away: 1.0, ".": 0.5, "in": 0.5 },
    "slept": { on: 1.6, "in": 1.2, ".": 1.0, under: 0.9, happily: 0.3 },
    "purred": { ".": 1.8, happily: 1.0, and: 0.8 },
    "barked": { ".": 1.6, loudly: 1.4, and: 0.8 },
    "beeped": { ".": 1.6, loudly: 1.0, and: 0.9, happily: 0.3 },
    "on": { the: 3.0, a: 1.0 },
    "in": { the: 2.6, a: 1.0 },
    "under": { the: 2.6, a: 0.8 },
    "to": { the: 2.5, a: 0.6 },
    "mat": { ".": 2.0, and: 0.6 },
    "sofa": { ".": 1.8, and: 0.6 },
    "park": { ".": 1.8, and: 0.7 },
    "garden": { ".": 1.8, and: 0.6 },
    "moon": { ".": 1.5, and: 0.5 },
    "quickly": { ".": 1.2, to: 1.0, and: 0.8 },
    "happily": { ".": 1.6, and: 0.6 },
    "loudly": { ".": 1.6, and: 0.7 },
    "quietly": { ".": 1.6, on: 0.6 },
    "away": { ".": 1.6, and: 0.6 },
    "and": { the: 2.0, it: 1.2, then: 1.0, a: 0.6 },
    "then": { the: 1.6, it: 1.6, a: 0.5 },
    "it": { slept: 1.2, sat: 1.0, ran: 1.0, purred: 0.5, barked: 0.5, beeped: 0.5 },
    ".": { the: 2.0, it: 1.2, then: 0.8, once: 0.3 },
    "once": { upon: 3.0, the: -1.0 },
    "upon": { a: 3.0 },
    "time": { there: 2.0, the: 1.0 },
    "there": { was: 3.0 },
    "was": { a: 2.4, the: 1.0 }
  };
  var PROMPTS = { cat: "the cat sat on the", once: "once upon a time", robot: "the robot" };

  function el(tag, cls, txt) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (txt !== undefined && txt !== null) n.textContent = txt;
    return n;
  }
  function plasma(t) {
    var stops = [[0, [13, 8, 135]], [0.25, [126, 3, 168]], [0.5, [204, 71, 120]], [0.75, [248, 149, 64]], [1, [240, 249, 33]]];
    t = Math.max(0, Math.min(1, t));
    for (var i = 1; i < stops.length; i++) {
      if (t <= stops[i][0]) {
        var a = stops[i - 1], b = stops[i], u = (t - a[0]) / (b[0] - a[0]);
        return "rgb(" + [0, 1, 2].map(function (k) { return Math.round(a[1][k] + (b[1][k] - a[1][k]) * u); }).join(",") + ")";
      }
    }
    return "rgb(240,249,33)";
  }

  // The full decoding pipeline: temperature, softmax, top-k, top-p, rescale.
  function distribution(last, T, k, p) {
    var logits = MODEL[last] || MODEL["."];
    var toks = Object.keys(logits);
    function soft(scale) {
      var m = -Infinity;
      toks.forEach(function (t) { m = Math.max(m, logits[t] / scale); });
      var ex = toks.map(function (t) { return Math.exp(logits[t] / scale - m); });
      var s = ex.reduce(function (a, b) { return a + b; }, 0);
      return ex.map(function (e) { return e / s; });
    }
    var raw = soft(1), hot = soft(T);
    var rows = toks.map(function (t, i) { return { tok: t, raw: raw[i], temp: hot[i], p: 0, cut: null }; });
    rows.sort(function (a, b) { return b.temp - a.temp; });
    var run = 0;
    rows.forEach(function (r, i) {
      if (k && i >= k) r.cut = "top-k";
      else if (p < 1 && run >= p - 1e-9) r.cut = "top-p";
      if (!r.cut) run += r.temp;
    });
    rows.forEach(function (r) { r.p = r.cut ? 0 : r.temp / run; });
    return rows;
  }

  function build(body) {
    body.textContent = "";
    var st = { words: [], gen: [], timer: 0 };
    var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    var row = el("div", "tool-row");
    function field(label, ctrl, out) {
      var f = el("div", "tool-field"), id = "ts-" + Math.random().toString(36).slice(2, 8);
      var l = el("label", null, label); l.setAttribute("for", id); ctrl.id = id;
      f.appendChild(l); f.appendChild(ctrl); if (out) f.appendChild(out); row.appendChild(f); return f;
    }
    var sPrompt = el("select");
    Object.keys(PROMPTS).forEach(function (k) { var o = el("option", null, "“" + PROMPTS[k] + "…”"); o.value = k; sPrompt.appendChild(o); });
    field("Start from", sPrompt);
    var temp = el("input"); temp.type = "range"; temp.min = "0.05"; temp.max = "2.5"; temp.step = "0.05"; temp.value = "1";
    var tOut = el("span", "ts-num", "1.00");
    field("Temperature", temp, tOut);
    var sK = el("select");
    [["0", "off"], ["1", "1 (greedy)"], ["2", "2"], ["3", "3"], ["5", "5"]].forEach(function (o) { var n = el("option", null, o[1]); n.value = o[0]; sK.appendChild(n); });
    field("Top-k", sK);
    var topp = el("input"); topp.type = "range"; topp.min = "0.1"; topp.max = "1"; topp.step = "0.05"; topp.value = "1";
    var pOut = el("span", "ts-num", "1.00 (off)");
    field("Top-p", topp, pOut);

    var btns = el("div", "tool-btns");
    var bOne = el("button", "tool-btn is-primary", "Pick the next word"); bOne.type = "button";
    var bTen = el("button", "tool-btn", "Write 10 more"); bTen.type = "button";
    var bReset = el("button", "tool-btn", "Start again"); bReset.type = "button";
    btns.appendChild(bOne); btns.appendChild(bTen); btns.appendChild(bReset);

    var textBox = el("p", "ts-text"); textBox.setAttribute("aria-live", "off");
    var cap = el("p", "ts-cap");
    var table = el("table", "ts-dist");
    var thead = el("thead"), hr = el("tr");
    ["next word", "trained", "after your settings"].forEach(function (h) { hr.appendChild(el("th", null, h)); });
    thead.appendChild(hr); table.appendChild(thead);
    var tbody = el("tbody"); table.appendChild(tbody);
    var legend = el("p", "ts-legend");
    legend.appendChild(document.createTextNode("Each written word is shaded by how likely it was when picked: "));
    var lo = el("span", "ts-swatch"); lo.style.background = plasma(0.05); legend.appendChild(lo);
    legend.appendChild(document.createTextNode(" unlikely to "));
    var hi = el("span", "ts-swatch"); hi.style.background = plasma(0.95); legend.appendChild(hi);
    legend.appendChild(document.createTextNode(" very likely."));
    var status = el("p", "tool-status"); status.setAttribute("role", "status"); status.setAttribute("aria-live", "polite");
    var note = el("p", "tool-note", "This toy model looks only at the last word, like the bigram model in Level 9. A real language model uses the whole context and a vocabulary of 100,000 tokens, but temperature, top-k and top-p work exactly the same way.");

    function settings() { return { T: parseFloat(temp.value), k: parseInt(sK.value, 10), p: parseFloat(topp.value) }; }
    function last() { return st.words.length ? st.words[st.words.length - 1].w : "."; }

    function renderText() {
      textBox.textContent = "";
      st.words.forEach(function (it, i) {
        var s = el("span", it.gen ? "ts-tok is-gen" : "ts-tok", it.w);
        if (it.gen) {
          s.style.background = plasma(0.1 + 0.85 * it.p);
          s.style.color = it.p > 0.45 ? "#111827" : "#FFFFFF";
          s.title = "probability " + it.p.toFixed(2) + " when picked";
        }
        textBox.appendChild(s);
        if (i < st.words.length - 1) textBox.appendChild(document.createTextNode(" "));
      });
    }
    function renderDist() {
      var o = settings(), rows = distribution(last(), o.T, o.k, o.p);
      cap.textContent = "What could come after “" + last() + "”:";
      tbody.textContent = "";
      rows.forEach(function (r) {
        var tr = el("tr", r.cut ? "is-cut" : null);
        tr.appendChild(el("td", "ts-word", r.tok === "." ? "full stop" : r.tok));
        tr.appendChild(el("td", "ts-num", r.raw.toFixed(3)));
        var td = el("td", "ts-cell"), bar = el("span", "ts-bar"), fill = el("span", "ts-fill");
        fill.style.width = (100 * r.p).toFixed(1) + "%";
        bar.appendChild(fill); td.appendChild(bar);
        td.appendChild(el("span", "ts-num", r.cut ? "cut by " + r.cut : r.p.toFixed(3)));
        tr.appendChild(td);
        tbody.appendChild(tr);
      });
    }
    function pick() {
      var o = settings(), rows = distribution(last(), o.T, o.k, o.p);
      var r = Math.random(), acc = 0, chosen = rows[0];
      for (var i = 0; i < rows.length; i++) {
        if (rows[i].cut) continue;
        acc += rows[i].p;
        if (r <= acc) { chosen = rows[i]; break; }
      }
      st.words.push({ w: chosen.tok, gen: true, p: chosen.p });
      renderText(); renderDist();
      status.textContent = "Picked “" + (chosen.tok === "." ? "." : chosen.tok) + "”, which had probability " + chosen.p.toFixed(2) + " after your settings.";
    }
    function stop() { if (st.timer) { clearTimeout(st.timer); st.timer = 0; } }
    function reset() {
      stop();
      st.words = PROMPTS[sPrompt.value].split(" ").map(function (w) { return { w: w, gen: false, p: 1 }; });
      renderText(); renderDist();
      status.textContent = "Ready. Pick one word at a time, or write ten.";
    }

    bOne.addEventListener("click", function () { stop(); pick(); });
    bTen.addEventListener("click", function () {
      stop();
      if (reduce) { for (var i = 0; i < 10; i++) pick(); return; }
      var n = 0;
      (function next() { pick(); n += 1; if (n < 10) st.timer = setTimeout(next, 180); else st.timer = 0; })();
    });
    bReset.addEventListener("click", reset);
    sPrompt.addEventListener("change", reset);
    temp.addEventListener("input", function () { tOut.textContent = parseFloat(temp.value).toFixed(2); renderDist(); });
    sK.addEventListener("change", renderDist);
    topp.addEventListener("input", function () {
      var v = parseFloat(topp.value); pOut.textContent = v.toFixed(2) + (v >= 1 ? " (off)" : ""); renderDist();
    });

    body.appendChild(row); body.appendChild(btns); body.appendChild(textBox); body.appendChild(legend);
    body.appendChild(cap); body.appendChild(table); body.appendChild(status); body.appendChild(note);
    reset();
  }

  function init() {
    var mounts = document.querySelectorAll('.tool[data-tool="token-sampler"]');
    Array.prototype.forEach.call(mounts, function (m) {
      var b = m.querySelector(".tool-body");
      if (b) build(b);
    });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
