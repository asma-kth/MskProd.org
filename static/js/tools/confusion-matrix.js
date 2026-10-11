/* Classifier scorer: move the threshold and watch precision and recall trade.
 *
 * Every student can recite that accuracy is misleading on an imbalanced
 * problem. Far fewer can feel it. Here the threshold is a slider over a fixed
 * population of scored cases, so tightening it visibly converts false
 * positives into false negatives while accuracy barely moves, and the cost
 * line underneath says what that trade means for the scenario chosen.
 */
(function () {
  "use strict";

  function el(tag, cls, txt) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (txt !== undefined && txt !== null) n.textContent = txt;
    return n;
  }

  function uid() { return Math.random().toString(36).slice(2, 8); }

  /* A deterministic generator: the same population every visit, so a student
     comparing two thresholds is comparing thresholds and nothing else. */
  function rng(seed) {
    var s = seed;
    return function () {
      s = (s * 1103515245 + 12345) % 2147483648;
      return s / 2147483648;
    };
  }

  /* Two overlapping score distributions, one per real class.
   *
   * `gap` is the distance between the two class means and is the only thing
   * that makes the problem hard or easy. It has to leave the classes genuinely
   * overlapping: a well separated pair scores 99% on every measure at every
   * threshold, which teaches the opposite of the intended lesson. */
  function population(n, rate, gap, seed) {
    var r = rng(seed), out = [], i, pos, bell, centre, score;
    for (i = 0; i < n; i++) {
      pos = r() < rate;
      /* sum of three uniforms: mean 0.5, standard deviation about 0.167 */
      bell = (r() + r() + r()) / 3;
      centre = pos ? 0.5 + gap / 2 : 0.5 - gap / 2;
      score = centre + (bell - 0.5);
      out.push({ pos: pos, score: Math.min(0.999, Math.max(0.001, score)) });
    }
    return out;
  }

  var SCENARIOS = {
    spam: {
      name: "Spam filter",
      positive: "spam", negative: "real email",
      rate: 0.22, n: 1000, gap: 0.46, seed: 7,
      prefer: "precision",
      why: "A missed spam is an annoyance. A blocked job offer is serious, and "
         + "the user never knows it happened. Favour precision."
    },
    screening: {
      name: "Cancer screening",
      positive: "has the disease", negative: "does not",
      rate: 0.04, n: 1000, gap: 0.34, seed: 23,
      prefer: "recall",
      why: "A missed case can be fatal. A false alarm means another test. "
         + "Favour recall, and accept the extra tests."
    },
    fraud: {
      name: "Card fraud blocking",
      positive: "fraudulent", negative: "genuine",
      rate: 0.012, n: 2000, gap: 0.5, seed: 41,
      prefer: "balance",
      why: "Blocking a real customer loses them; missing a fraud costs money. "
         + "Set the threshold so a human reviews the uncertain middle."
    }
  };

  function score(data, t) {
    var m = { tp: 0, fp: 0, fn: 0, tn: 0 }, i, d;
    for (i = 0; i < data.length; i++) {
      d = data[i];
      if (d.score >= t) { if (d.pos) m.tp++; else m.fp++; }
      else { if (d.pos) m.fn++; else m.tn++; }
    }
    return m;
  }

  function pct(x) {
    if (!isFinite(x)) return "–";
    return (Math.round(x * 1000) / 10).toFixed(1) + "%";
  }

  function histogram(data, t, sc) {
    /* Twenty buckets per class, drawn as two overlapping series, with the
       threshold as a line you can see cases falling either side of. */
    var B = 20, posB = [], negB = [], i, b, peak = 1;
    for (i = 0; i < B; i++) { posB.push(0); negB.push(0); }
    for (i = 0; i < data.length; i++) {
      b = Math.min(B - 1, Math.floor(data[i].score * B));
      if (data[i].pos) posB[b]++; else negB[b]++;
    }
    for (i = 0; i < B; i++) peak = Math.max(peak, posB[i], negB[i]);

    var W = 600, H = 150, PAD = 28, bw = (W - PAD * 2) / B;
    var parts = [];
    parts.push('<rect x="' + PAD + '" y="6" width="' + (W - PAD * 2)
               + '" height="' + H + '" fill="none" stroke="currentColor" '
               + 'stroke-opacity=".18"/>');
    for (i = 0; i < B; i++) {
      var hn = (negB[i] / peak) * H, hp = (posB[i] / peak) * H;
      var x = PAD + i * bw;
      if (hn > 0) {
        parts.push('<rect class="cm-neg" x="' + (x + 1).toFixed(1) + '" y="'
                   + (6 + H - hn).toFixed(1) + '" width="' + (bw - 2).toFixed(1)
                   + '" height="' + hn.toFixed(1) + '"/>');
      }
      if (hp > 0) {
        parts.push('<rect class="cm-pos" x="' + (x + 1).toFixed(1) + '" y="'
                   + (6 + H - hp).toFixed(1) + '" width="' + (bw - 2).toFixed(1)
                   + '" height="' + hp.toFixed(1) + '"/>');
      }
    }
    var tx = PAD + t * (W - PAD * 2);
    parts.push('<line class="cm-thresh" x1="' + tx.toFixed(1) + '" y1="0" x2="'
               + tx.toFixed(1) + '" y2="' + (H + 14) + '"/>');
    parts.push('<text class="cm-axis" x="' + PAD + '" y="' + (H + 26)
               + '" text-anchor="start">score 0</text>');
    parts.push('<text class="cm-axis" x="' + (W - PAD) + '" y="' + (H + 26)
               + '" text-anchor="end">score 1</text>');
    parts.push('<text class="cm-axis cm-axis-t" x="' + tx.toFixed(1) + '" y="'
               + (H + 26) + '" text-anchor="middle">threshold</text>');
    return '<svg viewBox="0 0 ' + W + ' ' + (H + 32) + '" role="img" '
         + 'aria-label="Score distributions for ' + sc.positive + ' and '
         + sc.negative + ', with the current threshold marked">'
         + parts.join("") + '</svg>';
  }

  function build(body) {
    body.textContent = "";
    var key = "spam";
    var data = null;
    var threshold = 0.5;

    var row = el("div", "tool-row");

    var scf = el("div", "tool-field");
    var scl = el("label", null, "Scenario");
    var sel = document.createElement("select");
    Object.keys(SCENARIOS).forEach(function (k) {
      var o = document.createElement("option");
      o.value = k;
      o.textContent = SCENARIOS[k].name;
      sel.appendChild(o);
    });
    sel.id = "cm-s-" + uid();
    scl.setAttribute("for", sel.id);
    scf.appendChild(scl); scf.appendChild(sel); row.appendChild(scf);

    var thf = el("div", "tool-field cm-thf");
    var thl = el("label", null, "Threshold");
    var slider = document.createElement("input");
    slider.type = "range";
    slider.min = "0.02"; slider.max = "0.98"; slider.step = "0.02";
    slider.value = "0.5";
    slider.id = "cm-t-" + uid();
    thl.setAttribute("for", slider.id);
    thf.appendChild(thl); thf.appendChild(slider); row.appendChild(thf);

    var btns = el("div", "tool-btns");
    [["Favour recall", 0.24], ["Balanced", 0.5], ["Favour precision", 0.76]]
      .forEach(function (p) {
        var b = el("button", "tool-btn", p[0]);
        b.type = "button";
        b.addEventListener("click", function () {
          slider.value = String(p[1]);
          threshold = p[1];
          render();
        });
        btns.appendChild(b);
      });

    var chart = el("div", "cm-chart");
    var legend = el("p", "cm-legend");
    var grid = el("div", "cm-grid");
    var measures = el("div", "cm-measures");
    var note = el("p", "tool-note");
    var live = el("p", "tool-status");
    live.setAttribute("role", "status");
    live.setAttribute("aria-live", "polite");

    function cell(title, n, kind, meaning) {
      var c = el("div", "cm-cell is-" + kind);
      c.appendChild(el("span", "cm-cell-name", title));
      c.appendChild(el("strong", "cm-cell-n", String(n)));
      c.appendChild(el("span", "cm-cell-why", meaning));
      return c;
    }

    function measure(name, formula, sub, value, strong) {
      var m = el("div", "cm-measure" + (strong ? " is-key" : ""));
      m.appendChild(el("span", "cm-m-name", name));
      m.appendChild(el("strong", "cm-m-val", value));
      m.appendChild(el("code", "cm-m-sub", formula + " = " + sub));
      return m;
    }

    function render() {
      var sc = SCENARIOS[key];
      var m = score(data, threshold);
      var all = m.tp + m.fp + m.fn + m.tn;
      var acc = (m.tp + m.tn) / all;
      var prec = m.tp + m.fp ? m.tp / (m.tp + m.fp) : NaN;
      var rec = m.tp + m.fn ? m.tp / (m.tp + m.fn) : NaN;
      var f1 = (isFinite(prec) && isFinite(rec) && prec + rec)
        ? 2 * prec * rec / (prec + rec) : NaN;

      chart.innerHTML = histogram(data, threshold, sc);
      legend.innerHTML = '<span class="cm-key cm-key-pos"></span> '
        + sc.positive + ' <span class="cm-key cm-key-neg"></span> '
        + sc.negative
        + ' — anything at or right of the line is flagged as '
        + sc.positive + '.';

      grid.textContent = "";
      grid.appendChild(cell("True positive", m.tp, "good",
                            "correctly flagged"));
      grid.appendChild(cell("False negative", m.fn, "bad",
                            "missed: " + sc.positive + ", not flagged"));
      grid.appendChild(cell("False positive", m.fp, "bad",
                            "false alarm: " + sc.negative + ", flagged"));
      grid.appendChild(cell("True negative", m.tn, "good",
                            "correctly left alone"));

      measures.textContent = "";
      measures.appendChild(measure("Accuracy", "(TP+TN)/all",
                                   (m.tp + m.tn) + "/" + all, pct(acc), false));
      measures.appendChild(measure("Precision", "TP/(TP+FP)",
                                   m.tp + "/" + (m.tp + m.fp), pct(prec),
                                   sc.prefer === "precision"));
      measures.appendChild(measure("Recall", "TP/(TP+FN)",
                                   m.tp + "/" + (m.tp + m.fn), pct(rec),
                                   sc.prefer === "recall"));
      measures.appendChild(measure("F1", "harmonic mean", "of the two",
                                   pct(f1), sc.prefer === "balance"));

      var allNeg = 1 - sc.rate;
      note.textContent = sc.why + " Predicting “" + sc.negative
        + "” every time would score " + pct(allNeg)
        + " accuracy on this population and catch nothing at all, which is why "
        + "accuracy is never reported on its own.";
      live.textContent = "Threshold " + threshold.toFixed(2) + ": precision "
        + pct(prec) + ", recall " + pct(rec) + ", accuracy " + pct(acc) + ".";
    }

    function reload() {
      var sc = SCENARIOS[key];
      data = population(sc.n, sc.rate, sc.gap, sc.seed);
      render();
    }

    sel.addEventListener("change", function () { key = sel.value; reload(); });
    slider.addEventListener("input", function () {
      threshold = parseFloat(slider.value);
      render();
    });

    body.appendChild(row);
    body.appendChild(btns);
    body.appendChild(chart);
    body.appendChild(legend);
    body.appendChild(grid);
    body.appendChild(measures);
    body.appendChild(note);
    body.appendChild(live);
    reload();
  }

  function init() {
    var mounts = document.querySelectorAll('.tool[data-tool="confusion-matrix"]');
    Array.prototype.forEach.call(mounts, function (m) {
      var b = m.querySelector(".tool-body");
      if (b) build(b);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else { init(); }
})();
