/* What-if model: a small spreadsheet model you can push around.
 *
 * F202 asks students to build models that answer "what if" questions, and the
 * idea only lands once you have changed an input and watched every output
 * move. This is the festival ticket model from the F202 pages: change the
 * price or any assumption and the outputs, the break-even prices and the
 * graph recalculate. Scenario buttons do what Scenario Manager does, the
 * Goal Seek button works backwards from a target profit exactly as the
 * spreadsheet tool does (including finding a different answer from a
 * different starting price), and the data table and formula view show the
 * same model the way a spreadsheet would.
 */
(function () {
  "use strict";

  var PMAX = 60, W = 400, H = 280, L = 62, R = 14, T = 16, B = 42;

  var FIELDS = [
    { k: "price", label: "Ticket price", unit: "£", min: 5, max: 60, step: 0.5,
      name: "TicketPrice", note: "the input variable" },
    { k: "demand", label: "Demand at £0", unit: "people", min: 300, max: 900,
      step: 10, name: "DemandAtZero", note: "assumption: survey" },
    { k: "lost", label: "Tickets lost per £1", unit: "people", min: 4, max: 24,
      step: 1, name: "LostPerPound", note: "assumption: survey" },
    { k: "cap", label: "Venue capacity", unit: "people", min: 100, max: 800,
      step: 10, name: "Capacity", note: "constant: licence" },
    { k: "head", label: "Cost per attendee", unit: "£", min: 0, max: 15,
      step: 0.5, name: "CostPerHead", note: "assumption: quotes" },
    { k: "fixed", label: "Fixed costs", unit: "£", min: 1000, max: 10000,
      step: 100, name: "FixedCosts", note: "assumption: quotes" }
  ];

  var SCENARIOS = {
    pessimistic: { label: "Pessimistic", demand: 500, lost: 12, cap: 400,
                   head: 6, fixed: 4500 },
    expected: { label: "Expected", demand: 600, lost: 12, cap: 400,
                head: 5, fixed: 4000 },
    optimistic: { label: "Optimistic", demand: 700, lost: 12, cap: 400,
                  head: 4.5, fixed: 3800 }
  };

  function el(tag, cls, txt) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (txt !== undefined && txt !== null) n.textContent = txt;
    return n;
  }

  function uid() { return "wim-" + Math.random().toString(36).slice(2, 8); }

  function money(v, pence) {
    var a = Math.abs(v);
    var s = a.toLocaleString("en-GB", {
      minimumFractionDigits: pence ? 2 : 0,
      maximumFractionDigits: pence ? 2 : 0
    });
    return (v < -0.004 ? "−£" : "£") + s;
  }

  function tickets(m, p) {
    return Math.min(m.cap, Math.max(0, m.demand - m.lost * p));
  }

  function calc(m, p) {
    var t = tickets(m, p);
    var rev = t * p, vc = t * m.head, tc = m.fixed + vc;
    return { t: t, rev: rev, vc: vc, tc: tc, profit: rev - tc };
  }

  function profit(m, p) { return calc(m, p).profit; }

  /* Every price in [0, 100] where profit crosses the target, refined by
     bisection. A fine scan is plenty for a function this smooth. */
  function crossings(m, target) {
    var out = [], step = 0.05, p, a, b, fa, fb, i, mid, fm;
    for (p = 0; p < 100; p += step) {
      a = p; b = p + step;
      fa = profit(m, a) - target; fb = profit(m, b) - target;
      if (fa === 0) { out.push(a); continue; }
      if (fa * fb < 0) {
        for (i = 0; i < 50; i++) {
          mid = (a + b) / 2; fm = profit(m, mid) - target;
          if (fa * fm <= 0) { b = mid; fb = fm; } else { a = mid; fa = fm; }
        }
        out.push((a + b) / 2);
      }
    }
    return out;
  }

  /* The best price inside the validated range of the price input. */
  function best(m) {
    var bp = 5, bv = -Infinity, p, v;
    for (p = 5; p <= PMAX + 1e-9; p += 0.01) {
      v = profit(m, p);
      if (v > bv + 1e-9) { bv = v; bp = p; }
    }
    return { p: Math.round(bp * 100) / 100, v: bv };
  }

  function niceStep(span) {
    var raw = span / 4, mag = Math.pow(10, Math.floor(Math.log(raw) / Math.LN10));
    var n = raw / mag;
    return (n < 1.5 ? 1 : n < 3 ? 2 : n < 7 ? 5 : 10) * mag;
  }

  function build(body) {
    body.textContent = "";
    var m = { price: 27.5, demand: 600, lost: 12, cap: 400, head: 5,
              fixed: 4000 };
    var scenario = "expected";
    var lastSeek = "";
    var inputs = {};

    /* ---- scenario buttons */
    var scen = el("div", "tool-btns wim-scen");
    scen.setAttribute("role", "group");
    scen.setAttribute("aria-label", "Scenarios");
    var scenBtns = {};
    Object.keys(SCENARIOS).forEach(function (k) {
      var b = el("button", "tool-btn", SCENARIOS[k].label);
      b.type = "button";
      b.addEventListener("click", function () {
        var s = SCENARIOS[k];
        ["demand", "lost", "cap", "head", "fixed"].forEach(function (f) {
          m[f] = s[f];
        });
        scenario = k;
        lastSeek = "";
        sync();
        render();
      });
      scenBtns[k] = b;
      scen.appendChild(b);
    });

    /* ---- the input sheet */
    var grid = el("div", "wim-inputs");
    FIELDS.forEach(function (f) {
      var id = uid();
      var row = el("div", "wim-field" + (f.k === "price" ? " is-key" : ""));
      var lab = el("label", null, f.label + (f.unit === "£" ? " (£)" : ""));
      lab.setAttribute("for", id);
      var range = document.createElement("input");
      range.type = "range"; range.min = f.min; range.max = f.max;
      range.step = f.step; range.id = id;
      range.setAttribute("aria-describedby", id + "-n");
      var num = document.createElement("input");
      num.type = "number"; num.min = f.min; num.max = f.max; num.step = f.step;
      num.setAttribute("aria-label", f.label + " value");
      num.className = "wim-num";
      var note = el("span", "wim-note", f.name + " · " + f.note);
      note.id = id + "-n";
      range.addEventListener("input", function () {
        m[f.k] = parseFloat(range.value);
        if (f.k !== "price") scenario = null;
        lastSeek = "";
        sync(); render();
      });
      num.addEventListener("change", function () {
        var v = parseFloat(num.value);
        /* Validation, exactly as the input sheet would apply it. */
        if (isNaN(v) || v < f.min || v > f.max) {
          status.textContent = f.label + " must be a number from "
            + f.min + " to " + f.max + ". The value was rejected, which "
            + "is what data validation is for.";
          status.className = "tool-status is-bad";
          sync();
          return;
        }
        m[f.k] = v;
        if (f.k !== "price") scenario = null;
        lastSeek = "";
        sync(); render();
      });
      var ctl = el("div", "wim-ctl");
      ctl.appendChild(range);
      ctl.appendChild(num);
      row.appendChild(lab);
      row.appendChild(ctl);
      row.appendChild(note);
      grid.appendChild(row);
      inputs[f.k] = { range: range, num: num };
    });

    /* ---- outputs */
    var outWrap = el("div", "wim-out");
    var table = el("table", "wim-table");
    var tbody = el("tbody");
    table.appendChild(tbody);
    var big = el("div", "wim-big");
    var bigLab = el("span", "wim-big-lab", "Profit");
    var bigVal = el("strong", "wim-big-val", "");
    var bigNote = el("span", "wim-big-note", "");
    big.appendChild(bigLab); big.appendChild(bigVal); big.appendChild(bigNote);
    outWrap.appendChild(big);
    outWrap.appendChild(table);

    /* ---- chart */
    var svg = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    svg.setAttribute("viewBox", "0 0 " + W + " " + H);
    svg.setAttribute("class", "wim-plot");
    svg.setAttribute("role", "img");

    var top = el("div", "wim-top");
    top.appendChild(grid);
    top.appendChild(outWrap);

    /* ---- goal seek */
    var seek = el("div", "tool-row wim-seek");
    var sid = uid();
    var sf = el("div", "tool-field");
    var sl = el("label", null, "Goal Seek: target profit (£)");
    sl.setAttribute("for", sid);
    var target = document.createElement("input");
    target.type = "number"; target.id = sid; target.value = "1000";
    target.step = "100";
    sf.appendChild(sl); sf.appendChild(target);
    var go = el("button", "tool-btn is-primary", "Find the price");
    go.type = "button";
    seek.appendChild(sf);
    seek.appendChild(go);

    /* ---- data table and formulas */
    var extras = el("div", "tool-btns");
    var dtBtn = el("button", "tool-btn", "Show data table");
    dtBtn.type = "button";
    dtBtn.setAttribute("aria-expanded", "false");
    var fxBtn = el("button", "tool-btn", "Show formulas");
    fxBtn.type = "button";
    fxBtn.setAttribute("aria-expanded", "false");
    extras.appendChild(dtBtn);
    extras.appendChild(fxBtn);
    var dt = el("div", "wim-dt");
    dt.hidden = true;
    var fx = el("div", "wim-fx");
    fx.hidden = true;

    var status = el("p", "tool-status");
    status.setAttribute("role", "status");
    status.setAttribute("aria-live", "polite");
    var note = el("p", "tool-note", "This is an invented example, not an OCR "
      + "brief. Build your own model in a real spreadsheet: this only shows "
      + "how one behaves.");

    function sync() {
      FIELDS.forEach(function (f) {
        /* Goal Seek leaves the price unrounded, as the spreadsheet does; the
           box shows it to the penny. */
        var v = f.k === "price" ? Math.round(m[f.k] * 100) / 100 : m[f.k];
        inputs[f.k].range.value = v;
        inputs[f.k].num.value = v;
      });
      Object.keys(scenBtns).forEach(function (k) {
        scenBtns[k].classList.toggle("is-on", k === scenario);
        scenBtns[k].setAttribute("aria-pressed", k === scenario ? "true" : "false");
      });
    }

    function row(label, value, cls) {
      var tr = el("tr", cls || null);
      tr.appendChild(el("th", null, label));
      var td = el("td", null, value);
      tr.appendChild(td);
      tbody.appendChild(tr);
    }

    function render() {
      var c = calc(m, m.price);
      var be = crossings(m, 0);
      var bst = best(m);
      tbody.textContent = "";
      row("Tickets sold", Math.round(c.t) + " of " + m.cap
          + (c.t >= m.cap ? " (sold out)" : ""));
      row("Revenue", money(c.rev, true));
      row("Variable costs", money(c.vc, true));
      row("Total costs", money(c.tc, true));
      row("Break-even price" + (be.length === 1 ? "" : "s"),
          be.length ? be.map(function (p) { return money(p, true); }).join(" and ")
                    : "none: it never breaks even");
      row("Best price", money(bst.p, true) + " → " + money(bst.v)
          + " profit", "wim-best");
      bigVal.textContent = money(c.profit);
      big.classList.toggle("is-loss", c.profit < 0);
      bigNote.textContent = c.profit < 0 ? "LOSS" : "PROFIT";
      draw(be, bst);
      if (!dt.hidden) fillTable();
      if (!fx.hidden) fillFormulas(c);
      status.className = "tool-status";
      status.textContent = lastSeek || ("At " + money(m.price, true) + " the model sells "
        + Math.round(c.t) + " tickets for a " + (c.profit < 0 ? "loss" : "profit")
        + " of " + money(Math.abs(c.profit)) + ".");
    }

    function draw(be, bst) {
      var lo = Infinity, hi = -Infinity, p, v, pts = [];
      for (p = 0; p <= PMAX + 1e-9; p += 0.25) {
        v = profit(m, p);
        pts.push([p, v]);
        if (v < lo) lo = v;
        if (v > hi) hi = v;
      }
      lo = Math.min(lo, 0); hi = Math.max(hi, 0);
      var st = niceStep(hi - lo || 1);
      lo = Math.floor(lo / st) * st; hi = Math.ceil(hi / st) * st;
      function sx(p) { return L + (W - L - R) * p / PMAX; }
      function sy(v) { return T + (H - T - B) * (hi - v) / (hi - lo); }
      var parts = [], i, y;
      parts.push('<rect class="wim-bg" x="' + L + '" y="' + T + '" width="'
                 + (W - L - R) + '" height="' + (H - T - B) + '"/>');
      for (v = lo; v <= hi + 1e-9; v += st) {
        y = sy(v).toFixed(1);
        parts.push('<line class="wim-grid" x1="' + L + '" y1="' + y + '" x2="'
                   + (W - R) + '" y2="' + y + '"/>');
        parts.push('<text class="wim-tick" x="' + (L - 6) + '" y="' + (+y + 3.5)
                   + '" text-anchor="end">' + money(v) + '</text>');
      }
      for (p = 0; p <= PMAX; p += 10) {
        parts.push('<text class="wim-tick" x="' + sx(p) + '" y="' + (H - B + 16)
                   + '" text-anchor="middle">£' + p + '</text>');
      }
      parts.push('<text class="wim-lab" x="' + ((W + L) / 2) + '" y="' + (H - 6)
                 + '" text-anchor="middle">ticket price</text>');
      parts.push('<line class="wim-zero" x1="' + L + '" y1="' + sy(0) + '" x2="'
                 + (W - R) + '" y2="' + sy(0) + '"/>');
      var d = "";
      for (i = 0; i < pts.length; i++) {
        d += (i ? " L" : "M") + sx(pts[i][0]).toFixed(1) + " "
          + sy(pts[i][1]).toFixed(1);
      }
      parts.push('<path class="wim-curve" d="' + d + '"/>');
      be.forEach(function (bp) {
        if (bp <= PMAX) {
          parts.push('<circle class="wim-be" cx="' + sx(bp).toFixed(1) + '" cy="'
                     + sy(0).toFixed(1) + '" r="4.5"/>');
        }
      });
      if (bst.p <= PMAX) {
        parts.push('<circle class="wim-max" cx="' + sx(bst.p).toFixed(1)
                   + '" cy="' + sy(bst.v).toFixed(1) + '" r="4.5"/>');
      }
      var cur = profit(m, m.price);
      parts.push('<line class="wim-cur-line" x1="' + sx(m.price).toFixed(1)
                 + '" y1="' + T + '" x2="' + sx(m.price).toFixed(1) + '" y2="'
                 + (H - B) + '"/>');
      parts.push('<circle class="wim-cur" cx="' + sx(m.price).toFixed(1)
                 + '" cy="' + sy(cur).toFixed(1) + '" r="6"/>');
      svg.innerHTML = parts.join("");
      svg.setAttribute("aria-label", "Graph of profit against ticket price from "
        + "£0 to £" + PMAX + ". The current price of " + money(m.price, true)
        + " gives " + money(cur) + ". The best price is " + money(bst.p, true)
        + " for " + money(bst.v) + ". "
        + (be.length ? "It breaks even at " + be.map(function (b) {
            return money(b, true); }).join(" and ") + "." : "It never breaks even."));
    }

    function fillTable() {
      dt.textContent = "";
      var t = el("table", "wim-dt-table");
      var cap = el("caption", null, "One-variable data table: profit at each "
        + "price, with every other input held as it is now");
      t.appendChild(cap);
      var head = el("tr");
      ["Ticket price", "Tickets sold", "Revenue", "Profit"].forEach(function (h) {
        var th = el("th", null, h);
        th.setAttribute("scope", "col");
        head.appendChild(th);
      });
      var thead = el("thead"); thead.appendChild(head); t.appendChild(thead);
      var tb = el("tbody"), bp = best(m).p, p, c, tr;
      for (p = 10; p <= 50; p += 5) {
        c = calc(m, p);
        tr = el("tr", c.profit < 0 ? "is-loss" : null);
        tr.appendChild(el("td", null, money(p, true)));
        tr.appendChild(el("td", null, String(Math.round(c.t))));
        tr.appendChild(el("td", null, money(c.rev)));
        tr.appendChild(el("td", null, money(c.profit)));
        if (Math.abs(p - bp) < 2.5) tr.classList.add("is-near");
        tb.appendChild(tr);
      }
      t.appendChild(tb);
      dt.appendChild(t);
    }

    function fillFormulas(c) {
      fx.textContent = "";
      var rows = [
        ["TicketsSold", "=MIN(Capacity, MAX(0, DemandAtZero - LostPerPound * TicketPrice))",
         String(Math.round(c.t))],
        ["Revenue", "=TicketsSold * TicketPrice", money(c.rev, true)],
        ["VariableCosts", "=TicketsSold * CostPerHead", money(c.vc, true)],
        ["TotalCosts", "=FixedCosts + VariableCosts", money(c.tc, true)],
        ["Profit", "=Revenue - TotalCosts", money(c.profit, true)],
        ["Status", "=IF(Profit >= 0, \"PROFIT\", \"LOSS\")",
         c.profit >= 0 ? "PROFIT" : "LOSS"]
      ];
      var t = el("table", "wim-fx-table");
      var head = el("tr");
      ["Named cell", "Formula", "Value now"].forEach(function (h) {
        var th = el("th", null, h); th.setAttribute("scope", "col");
        head.appendChild(th);
      });
      var thead = el("thead"); thead.appendChild(head); t.appendChild(thead);
      var tb = el("tbody");
      rows.forEach(function (r) {
        var tr = el("tr");
        tr.appendChild(el("td", null, r[0]));
        var f = el("td"); f.appendChild(el("code", null, r[1])); tr.appendChild(f);
        tr.appendChild(el("td", null, r[2]));
        tb.appendChild(tr);
      });
      t.appendChild(tb);
      fx.appendChild(t);
    }

    dtBtn.addEventListener("click", function () {
      dt.hidden = !dt.hidden;
      dtBtn.textContent = dt.hidden ? "Show data table" : "Hide data table";
      dtBtn.setAttribute("aria-expanded", dt.hidden ? "false" : "true");
      if (!dt.hidden) fillTable();
    });
    fxBtn.addEventListener("click", function () {
      fx.hidden = !fx.hidden;
      fxBtn.textContent = fx.hidden ? "Show formulas" : "Hide formulas";
      fxBtn.setAttribute("aria-expanded", fx.hidden ? "false" : "true");
      if (!fx.hidden) fillFormulas(calc(m, m.price));
    });

    go.addEventListener("click", function () {
      var tv = parseFloat(target.value);
      if (isNaN(tv)) {
        lastSeek = "Type a target profit first.";
        render();
        return;
      }
      var all = crossings(m, tv), start = m.price;
      var xs = all.filter(function (p) { return p >= 5 && p <= PMAX; });
      if (!xs.length) {
        lastSeek = all.length
          ? "Goal Seek would need a price of " + money(all[0], true) + ", outside "
            + "the validated range of £5 to £" + PMAX + "."
          : "Goal Seek may not have found a solution: no price reaches "
            + money(tv) + ". The most this model can make is " + money(best(m).v)
            + ".";
        render();
        return;
      }
      /* Like the real tool, start from the current price and settle on the
         nearest answer, so a different start can give a different answer. */
      xs.sort(function (a, b) { return Math.abs(a - start) - Math.abs(b - start); });
      var ans = xs[0];
      m.price = ans;
      sync();
      lastSeek = "Goal Seek started at " + money(start, true) + " and found "
        + money(ans, true) + ", which gives " + money(profit(m, ans)) + "."
        + (xs.length > 1 ? " There is another answer at " + money(xs[1], true)
          + ": start nearer to it and Goal Seek finds that one instead." : "");
      render();
    });

    body.appendChild(scen);
    body.appendChild(top);
    body.appendChild(svg);
    body.appendChild(seek);
    body.appendChild(extras);
    body.appendChild(dt);
    body.appendChild(fx);
    body.appendChild(status);
    body.appendChild(note);
    sync();
    render();
  }

  function init() {
    var mounts = document.querySelectorAll('.tool[data-tool="what-if-model"]');
    Array.prototype.forEach.call(mounts, function (m) {
      var b = m.querySelector(".tool-body");
      if (b) build(b);
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else { init(); }
})();
