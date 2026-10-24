/* Engine: datamaze. Filter a table of records to find each door's code.
 *
 * data: { fields: [{id, text, num, filter}], rows: [{...}],
 *         doors: [{clue, filters: {fieldId: value}, sort, code, near: {wrongCode: why}}] }
 * The student filters on the facts in the clue, hides columns they do not
 * need, sorts when the clue asks for the most or the least, and types the
 * code. Each door opens onto the next; the last one is the way out.
 * answer: [code per door]
 */
(function (root) {
  "use strict";
  var CT = root.CT = root.CT || {};

  function doorCheck(door, code) {
    code = String(code === undefined || code === null ? "" : code).trim();
    if (!code) return { ok: false, incomplete: true, msg: "Type the code you found, then try it." };
    if (code === door.code) return { ok: true };
    return { ok: false, msg: (door.near && door.near[code]) || "That code does not open the door. Check that your filters use every fact in the clue." };
  }
  CT.check.datamaze = function (d, a) {
    a = a || [];
    for (var i = 0; i < d.doors.length; i++) {
      var r = doorCheck(d.doors[i], a[i]);
      if (!r.ok) return Object.assign(r, { round: i });
    }
    return { ok: true };
  };
  CT.solve.datamaze = function (d) { return d.doors.map(function (x) { return x.code; }); };

  // The rows that pass every filter, sorted if asked.
  CT.filterRows = function (rows, filters, sort, dir) {
    var out = rows.filter(function (r) { return Object.keys(filters).every(function (k) { return !filters[k] || String(r[k]) === filters[k]; }); });
    if (sort) out = out.slice().sort(function (a, b) { return dir === "asc" ? a[sort] - b[sort] : b[sort] - a[sort]; });
    return out;
  };

  CT.engines.datamaze = {
    mount: function (host, level, api) {
      var d = level.data, di = 0, door, filters, sortBy, dir, hidden = {}, code = "", opened = [];
      var board = CT.el("div", { class: "cdm" });
      host.appendChild(board);
      var numField = d.fields.filter(function (f) { return f.num; })[0];

      function start(i) {
        di = i; door = d.doors[di]; filters = {}; sortBy = null; dir = "desc"; code = "";
        render();
        if (i > 0) api.say("Door " + (i + 1) + "! Read the new clue carefully.", "think", 2400);
      }
      function values(fid) {
        var seen = [];
        d.rows.forEach(function (r) { var v = String(r[fid]); if (seen.indexOf(v) < 0) seen.push(v); });
        return seen.sort();
      }
      function render(focusSel) {
        CT.clear(board);
        var hall = CT.el("ol", { class: "cdm-hall", "aria-label": "The maze doors" });
        d.doors.forEach(function (x, i) {
          var st = opened[i] ? "open" : i === di ? "now" : "shut";
          hall.appendChild(CT.el("li", { class: "cdm-door is-" + st, "aria-current": i === di ? "step" : null }, [
            CT.el("span", { class: "cdm-door-i", "aria-hidden": "true" }, opened[i] ? "🚪" : "🔒"),
            CT.el("span", null, "Door " + (i + 1) + (opened[i] ? ": open" : "")),
            i === di ? CT.el("span", { class: "cdm-pixel", "aria-hidden": "true" }, "🐱") : null
          ]));
        });
        hall.appendChild(CT.el("li", { class: "cdm-door cdm-exit" + (opened.length === d.doors.length ? " is-open" : "") }, [CT.el("span", { "aria-hidden": "true" }, "🏁"), " Way out"]));
        var clue = CT.el("div", { class: "ct-problem cdm-clue" }, [CT.el("span", { class: "ct-problem-k" }, "Door " + (di + 1) + " clue"), door.clue]);
        var fbar = CT.el("div", { class: "cdm-filters" }, [CT.el("p", { class: "ct-tray-h" }, "Filters")]);
        d.fields.filter(function (f) { return f.filter; }).forEach(function (f) {
          var sel = CT.el("select", { id: "cdm-f-" + f.id, "data-f": f.id, onchange: function () { filters[f.id] = this.value || null; render("#cdm-f-" + f.id); } },
            [CT.el("option", { value: "" }, "Any")].concat(values(f.id).map(function (v) { return CT.el("option", { value: v, selected: filters[f.id] === v ? true : null }, v); })));
          fbar.appendChild(CT.el("label", { class: "cdm-f" + (filters[f.id] ? " is-on" : "") }, [CT.el("span", null, f.text), sel]));
        });
        if (numField) fbar.appendChild(CT.el("button", { type: "button", class: "ct-btn ct-btn-mini cdm-sort", id: "cdm-sort", "aria-pressed": sortBy ? "true" : "false",
          onclick: function () { if (!sortBy) { sortBy = numField.id; dir = "desc"; } else if (dir === "desc") dir = "asc"; else sortBy = null; render("#cdm-sort"); } },
          !sortBy ? "↕ Sort by " + numField.text.toLowerCase() : dir === "desc" ? "⬇ Most " + numField.text.toLowerCase() + " first" : "⬆ Fewest " + numField.text.toLowerCase() + " first"));
        fbar.appendChild(CT.el("button", { type: "button", class: "ct-btn ct-btn-mini", onclick: function () { filters = {}; sortBy = null; render(); } }, "✕ Clear filters"));
        var showCols = CT.el("div", { class: "cdm-cols" }, [CT.el("span", { class: "ct-tray-h" }, "Show columns")]);
        d.fields.forEach(function (f) {
          showCols.appendChild(CT.el("label", { class: "cdm-chip" + (hidden[f.id] ? "" : " is-on") }, [
            CT.el("input", { type: "checkbox", checked: hidden[f.id] ? null : true, id: "cdm-c-" + f.id,
              onchange: function () { hidden[f.id] = !this.checked; render("#cdm-c-" + f.id); } }), f.text]));
        });
        var rows = CT.filterRows(d.rows, filters, sortBy, dir);
        var cols = d.fields.filter(function (f) { return !hidden[f.id]; });
        var table = CT.el("table", { class: "cfl-table cdm-table" }, [
          CT.el("caption", null, rows.length + " of " + d.rows.length + " records match"),
          CT.el("thead", null, CT.el("tr", null, cols.map(function (f) { return CT.el("th", { scope: "col", class: filters[f.id] ? "is-on" : null }, f.text + (sortBy === f.id ? (dir === "desc" ? " ⬇" : " ⬆") : "")); }))),
          CT.el("tbody", null, rows.map(function (r) { return CT.el("tr", null, cols.map(function (f) { return CT.el("td", { class: filters[f.id] ? "is-on" : null }, String(r[f.id])); })); }))
        ]);
        var input = CT.el("input", { type: "text", inputmode: "numeric", maxlength: "4", autocomplete: "off", class: "cdm-code", id: "cdm-code", value: code,
          "aria-label": "Door " + (di + 1) + " code", oninput: function () { code = this.value.replace(/\D/g, ""); if (this.value !== code) this.value = code; },
          onkeydown: function (e) { if (e.key === "Enter") { e.preventDefault(); api.submit(); } } });
        var pad = CT.el("div", { class: "cdm-keypad" }, [CT.el("label", { for: "cdm-code" }, "🔢 Door code"), input]);
        CT.append(board, [hall, clue, fbar, showCols, CT.el("div", { class: "cfl-wrap", tabindex: "0", "aria-label": "Records" }, table), pad]);
        if (focusSel) { var f = board.querySelector(focusSel); if (f) f.focus(); }
      }

      start(0);
      return {
        checkLabel: "🔓 Try the code",
        check: function () {
          var r = doorCheck(door, code);
          if (!r.ok) return r;
          opened[di] = true; render();
          CT.sound.play("chest");
          if (di < d.doors.length - 1) return CT.nextRound(api, di, d.doors.length, start, "Door");
          return r;
        },
        mark: function () { var i = board.querySelector("#cdm-code"); if (i) i.select(); },
        reset: function () { filters = {}; sortBy = null; hidden = {}; code = ""; render(); },
        showMe: function () {
          filters = Object.assign({}, door.filters);
          if (door.sort) { sortBy = door.sort; dir = "desc"; }
          code = door.code; render();
        },
        scaffold: function () {
          var k = Object.keys(door.filters).filter(function (f) { return filters[f] !== door.filters[f]; })[0];
          if (k) filters[k] = door.filters[k];
          else if (door.sort && sortBy !== door.sort) { sortBy = door.sort; dir = "desc"; }
          render();
          CT.announce("Pixel set a filter for you.");
        },
        destroy: function () { }
      };
    }
  };
})(typeof window !== "undefined" ? window : globalThis);
