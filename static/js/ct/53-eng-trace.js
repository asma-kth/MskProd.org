/* Engine: trace. Complete a trace table for a short program.
 *
 * data: { rounds: [{code, cols: [names], rows: [[cell text]], given: [[row, col]], note}] }
 * Given cells are filled in already; the student types the rest. An empty
 * expected cell must stay empty, as in a real trace table.
 * answer: [[[cell text]] per round]
 */
(function (root) {
  "use strict";
  var CT = root.CT = root.CT || {};

  function isGiven(rd, r, c) { return (rd.given || []).some(function (g) { return g[0] === r && g[1] === c; }); }
  function checkRound(rd, a) {
    a = a || [];
    var empty = 0, bad = [];
    rd.rows.forEach(function (row, r) {
      row.forEach(function (want, c) {
        if (isGiven(rd, r, c)) return;
        var got = String(((a[r] || [])[c]) || "").trim();
        if (want !== "" && got === "") empty++;
        else if (got !== want) bad.push([r, c]);
      });
    });
    if (empty) return { ok: false, incomplete: true, msg: "Fill every box that changes: " + empty + " still empty. Leave a box blank when nothing changes there." };
    if (bad.length) return { ok: false, wrong: bad, msg: (bad.length > 1 ? bad.length + " boxes are" : "One box is") + " not right yet. Follow the code line by line, changing one value at a time." };
    return { ok: true };
  }
  CT.check.trace = function (d, a) {
    a = a || [];
    for (var i = 0; i < d.rounds.length; i++) {
      var r = checkRound(d.rounds[i], a[i]);
      if (!r.ok) return Object.assign(r, { round: i });
    }
    return { ok: true };
  };
  CT.solve.trace = function (d) { return d.rounds.map(function (rd) { return rd.rows.map(function (row) { return row.slice(); }); }); };

  CT.engines.trace = {
    mount: function (host, level, api) {
      var d = level.data, ri = 0, rd, cells, wrong = {};
      var board = CT.el("div", { class: "ctt" });
      host.appendChild(board);

      function start(i) {
        ri = i; rd = d.rounds[ri]; wrong = {};
        cells = rd.rows.map(function (row, r) { return row.map(function (v, c) { return isGiven(rd, r, c) ? v : ""; }); });
        render();
      }
      function render(focus) {
        CT.clear(board);
        var table = CT.el("table", { class: "cfl-table ctt-table" }, [
          CT.el("caption", null, "Trace table"),
          CT.el("thead", null, CT.el("tr", null, rd.cols.map(function (c) { return CT.el("th", { scope: "col" }, c); })))]);
        var body = CT.el("tbody");
        rd.rows.forEach(function (row, r) {
          var tr = CT.el("tr");
          row.forEach(function (v, c) {
            if (isGiven(rd, r, c)) { tr.appendChild(CT.el("td", { class: "is-given" }, v)); return; }
            var key = r + ":" + c;
            tr.appendChild(CT.el("td", null, CT.el("input", { type: "text", class: "ctt-in" + (wrong[key] ? " is-wrong" : ""), value: cells[r][c], "data-cell": key,
              autocomplete: "off", spellcheck: "false", "aria-label": rd.cols[c] + ", row " + (r + 1),
              oninput: function () { cells[r][c] = this.value; delete wrong[key]; this.classList.remove("is-wrong"); },
              onkeydown: function (e) { if (e.key === "Enter") { e.preventDefault(); api.submit(); } } })));
          });
          body.appendChild(tr);
        });
        table.appendChild(body);
        CT.append(board, [CT.roundChip(ri, d.rounds.length),
          CT.el("div", { class: "ctt-wrap" }, [
            CT.el("div", null, [CT.el("p", { class: "ct-tray-h" }, "The program"), CT.codeView(rd.code)]),
            CT.el("div", null, [rd.note ? CT.el("p", { class: "ctt-note" }, rd.note) : null, CT.el("div", { class: "cfl-wrap" }, table)])])]);
        if (focus) { var f = board.querySelector(focus); if (f) f.focus(); }
      }

      start(0);
      return {
        check: function () {
          var r = checkRound(rd, cells);
          if (r.ok && ri < d.rounds.length - 1) return CT.nextRound(api, ri, d.rounds.length, start);
          return r;
        },
        mark: function (r) { wrong = {}; (r.wrong || []).forEach(function (rc) { wrong[rc[0] + ":" + rc[1]] = true; }); render(); },
        reset: function () { start(ri); },
        showMe: function () { cells = rd.rows.map(function (row) { return row.slice(); }); wrong = {}; render(); },
        scaffold: function () {
          // fill the first row that is not right yet, as if Pixel traced one more pass
          for (var r = 0; r < rd.rows.length; r++) {
            var off = rd.rows[r].some(function (v, c) { return !isGiven(rd, r, c) && String(cells[r][c]).trim() !== v; });
            if (off) { cells[r] = rd.rows[r].slice(); wrong = {}; render(); CT.announce("Pixel traced row " + (r + 1) + " for you."); return; }
          }
        },
        destroy: function () { }
      };
    }
  };
})(typeof window !== "undefined" ? window : globalThis);
