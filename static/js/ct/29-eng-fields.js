/* Engine: fields. Hide the data a decision does not need, then use the rest.
 *
 * data: { key, columns: [{id, text}], rows: [{...}],
 *         rounds: [{question, icon, rule, need: [colIds], colWhy: {colId: why},
 *                   labels: [text], answers: {keyValue: labelIndex}, rowWhy: {keyValue: why}}] }
 * Each round has two steps: tap the headings of the columns the rule needs,
 * then, with every other column hidden, decide each row.
 * answer: [{cols: [colIds], labels: {keyValue: labelIndex}} per round]
 */
(function (root) {
  "use strict";
  var CT = root.CT = root.CT || {};

  function colText(d, id) { var c = CT.byId(d.columns, id); return c ? c.text : id; }
  function colsCheck(d, rd, cols) {
    cols = (cols || []).filter(function (c) { return c !== d.key; });
    if (!cols.length) return { ok: false, incomplete: true, msg: "Choose the columns the rule needs: tap their headings." };
    var extra = cols.filter(function (c) { return rd.need.indexOf(c) < 0; });
    if (extra.length) return { ok: false, wrong: extra, msg: (rd.colWhy && rd.colWhy[extra[0]]) || "The rule does not use the " + colText(d, extra[0]) + " column." };
    var missing = rd.need.filter(function (c) { return cols.indexOf(c) < 0; });
    if (missing.length) return { ok: false, wrong: [], msg: "The rule needs " + (missing.length === 1 ? "one more column" : missing.length + " more columns") + ". Read the rule again, word by word." };
    return { ok: true };
  }
  function labelsCheck(d, rd, labels) {
    labels = labels || {};
    var keys = d.rows.map(function (r) { return String(r[d.key]); });
    var left = keys.filter(function (k) { return labels[k] === undefined || labels[k] === null; });
    if (left.length) return { ok: false, incomplete: true, msg: "Make a decision for every row: " + left.length + " still to go." };
    var bad = keys.filter(function (k) { return labels[k] !== rd.answers[k]; });
    if (bad.length) return { ok: false, wrong: bad, msg: (bad.length > 1 ? bad.length + " decisions need another look. " : "") + rd.rowWhy[bad[0]] };
    return { ok: true };
  }
  CT.check.fields = function (d, a) {
    a = a || [];
    for (var i = 0; i < d.rounds.length; i++) {
      var x = a[i] || {}, r = colsCheck(d, d.rounds[i], x.cols);
      if (r.ok) r = labelsCheck(d, d.rounds[i], x.labels);
      if (!r.ok) return Object.assign(r, { round: i });
    }
    return { ok: true };
  };
  CT.solve.fields = function (d) {
    return d.rounds.map(function (rd) { return { cols: rd.need.slice(), labels: Object.assign({}, rd.answers) }; });
  };

  CT.engines.fields = {
    mount: function (host, level, api) {
      var d = level.data, ri = 0, rd, step, cols, labels, wrong = {};
      var board = CT.el("div", { class: "cfl" });
      host.appendChild(board);

      function start(i) {
        ri = i; rd = d.rounds[ri]; step = "cols"; cols = []; labels = {}; wrong = {};
        render();
        if (i > 0) api.say("New question: " + rd.question, "think", 2600);
      }
      function render() {
        CT.clear(board);
        var rule = CT.el("div", { class: "ct-problem cfl-rule" }, [CT.el("span", { class: "ct-problem-k" }, "The rule"),
          CT.el("span", null, [CT.el("b", null, [rd.icon ? rd.icon + " " : "", rd.question]), " ", rd.rule])]);
        var stepNote = CT.el("p", { class: "cfl-step" }, step === "cols"
          ? ["Step 1: choose each column the rule needs. ", CT.el("b", null, cols.length + " chosen")]
          : ["Step 2: every other column is hidden. Decide each row."]);
        var shown = step === "cols" ? d.columns : d.columns.filter(function (c) { return c.id === d.key || cols.indexOf(c.id) >= 0; });
        function toggle(id) {
          var i = cols.indexOf(id);
          if (i >= 0) cols.splice(i, 1); else cols.push(id);
          wrong = {}; render(); CT.sound.play("tap");
        }
        // The same choices as chips above the table, so nothing needs a sideways scroll.
        var chips = step === "cols" ? CT.el("div", { class: "cfl-chips", role: "group", "aria-label": "Columns" }, d.columns.filter(function (c) { return c.id !== d.key; }).map(function (c) {
          var on = cols.indexOf(c.id) >= 0;
          return CT.el("button", { type: "button", class: "cfl-col" + (wrong[c.id] ? " is-wrong" : ""), "aria-pressed": on ? "true" : "false", "data-chip": c.id,
            onclick: function () { toggle(c.id); var b = board.querySelector('[data-chip="' + c.id + '"]'); if (b) b.focus(); } }, [on ? "📌 " : "", c.text]);
        })) : null;
        var table = CT.el("table", { class: "cfl-table" + (step === "label" ? " is-label" : "") });
        var hr = CT.el("tr");
        shown.forEach(function (c) {
          if (c.id === d.key || step === "label") { hr.appendChild(CT.el("th", { scope: "col" }, c.text)); return; }
          var on = cols.indexOf(c.id) >= 0;
          hr.appendChild(CT.el("th", { scope: "col", class: (on ? "is-on" : "") + (wrong[c.id] ? " is-wrong" : "") }, [
            CT.el("button", { type: "button", class: "cfl-col", "aria-pressed": on ? "true" : "false", tabindex: "-1", "aria-hidden": "true", onclick: function () {
              toggle(c.id);
            } }, [on ? "📌 " : "", c.text])]));
        });
        if (step === "label") hr.appendChild(CT.el("th", { scope: "col", class: "cfl-dec" }, "Your decision"));
        table.appendChild(CT.el("thead", null, hr));
        var body = CT.el("tbody");
        d.rows.forEach(function (row) {
          var k = String(row[d.key]), tr = CT.el("tr", { class: wrong[k] ? "is-wrong" : "" });
          shown.forEach(function (c) {
            var on = cols.indexOf(c.id) >= 0;
            tr.appendChild(CT.el(c.id === d.key ? "th" : "td", { scope: c.id === d.key ? "row" : null, class: step === "cols" && on ? "is-on" : null }, String(row[c.id])));
          });
          if (step === "label") {
            var seg = CT.el("div", { class: "cfl-seg", role: "group", "aria-label": "Decision for " + k });
            rd.labels.forEach(function (t, li) {
              seg.appendChild(CT.el("button", { type: "button", class: "cfl-opt" + (labels[k] === li ? " is-on" : ""), "aria-pressed": labels[k] === li ? "true" : "false",
                onclick: function () { labels[k] = li; delete wrong[k]; render(); CT.sound.play("tap"); var b = board.querySelector('[data-row="' + k + '"][data-li="' + li + '"]'); if (b) b.focus(); },
                "data-row": k, "data-li": String(li) }, t));
            });
            tr.appendChild(CT.el("td", { class: "cfl-dec" }, seg));
          }
          body.appendChild(tr);
        });
        table.appendChild(body);
        CT.append(board, [CT.roundChip(ri, d.rounds.length, "Question"), rule, stepNote, chips, CT.el("div", { class: "cfl-wrap", tabindex: "0", "aria-label": "Data table" }, table)]);
      }

      start(0);
      return {
        check: function () {
          if (step === "cols") {
            var r = colsCheck(d, rd, cols);
            if (!r.ok) return r;
            CT.wait(700, function () { if (api.alive()) { step = "label"; wrong = {}; render(); } });
            return { ok: true, more: true, msg: "Exactly the right columns! Now use them to decide each row.", toast: "⭐ Columns spot on!" };
          }
          var l = labelsCheck(d, rd, labels);
          if (l.ok && ri < d.rounds.length - 1) return CT.nextRound(api, ri, d.rounds.length, start, "Question");
          return l;
        },
        mark: function (r) { wrong = {}; (r.wrong || []).forEach(function (id) { wrong[id] = true; }); render(); },
        reset: function () { if (step === "cols") cols = []; else labels = {}; wrong = {}; render(); },
        showMe: function () { if (step === "cols") cols = rd.need.slice(); else labels = Object.assign({}, rd.answers); wrong = {}; render(); },
        scaffold: function () {
          if (step === "cols") {
            var extra = cols.filter(function (c) { return rd.need.indexOf(c) < 0; })[0];
            if (extra) cols.splice(cols.indexOf(extra), 1);
            else { var need = rd.need.filter(function (c) { return cols.indexOf(c) < 0; })[0]; if (need) cols.push(need); }
          } else {
            var k = d.rows.map(function (r) { return String(r[d.key]); }).filter(function (x) { return labels[x] !== rd.answers[x]; })[0];
            if (k !== undefined) labels[k] = rd.answers[k];
          }
          wrong = {}; render();
          CT.announce("Pixel did one step for you.");
        },
        destroy: function () { }
      };
    }
  };
})(typeof window !== "undefined" ? window : globalThis);
