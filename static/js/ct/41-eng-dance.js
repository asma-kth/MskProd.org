/* Engine: dance. Pixel dances a pattern; the student programs what comes next,
 * fills the missing moves, then writes the whole dance as a loop.
 *
 * data: { moves: [{id, text, icon}],
 *         rounds: [{type: "next", shown: [ids], answer: [ids]},
 *                  {type: "gap", shown: [id|null], answer: [ids]},
 *                  {type: "loop", target: [ids], units, answer: {times, unit: [ids]}}] }
 * answer: per round, the moves chosen ([ids]), or {times, unit} for a loop.
 */
(function (root) {
  "use strict";
  var CT = root.CT = root.CT || {};

  CT.expandLoop = function (times, unit) {
    var out = [], u = (unit || []).filter(Boolean);
    for (var i = 0; i < (times || 0); i++) out = out.concat(u);
    return out;
  };
  function eq(a, b) { return a.length === b.length && a.every(function (x, i) { return x === b[i]; }); }

  function checkRound(d, rd, a) {
    if (rd.type === "loop") {
      a = a || {};
      var unit = (a.unit || []).filter(Boolean);
      if (!unit.length || !a.times) return { ok: false, incomplete: true, msg: "Put at least one move inside the loop and choose how many times it repeats." };
      var made = CT.expandLoop(a.times, unit);
      if (eq(made, rd.target)) return { ok: true };
      return { ok: false, msg: "Your loop makes a dance of " + made.length + " moves, but it does not match the robot's dance of " + rd.target.length +
        " moves. Find the moves that repeat, then count how many times they repeat." };
    }
    a = a || [];
    var left = rd.answer.filter(function (x, i) { return !a[i]; }).length;
    if (left) return { ok: false, incomplete: true, msg: "Program every missing move first: " + left + " still empty." };
    var bad = [];
    rd.answer.forEach(function (x, i) { if (a[i] !== x) bad.push(i); });
    if (!bad.length) return { ok: true };
    return { ok: false, wrong: bad, msg: (bad.length > 1 ? bad.length + " moves break the pattern." : "One move breaks the pattern.") +
      " Watch the dance again and find the moves that repeat." };
  }
  CT.check.dance = function (d, a) {
    a = a || [];
    for (var i = 0; i < d.rounds.length; i++) {
      var r = checkRound(d, d.rounds[i], a[i]);
      if (!r.ok) return Object.assign(r, { round: i });
    }
    return { ok: true };
  };
  CT.solve.dance = function (d) {
    return d.rounds.map(function (rd) { return rd.type === "loop" ? { times: rd.answer.times, unit: rd.answer.unit.slice() } : rd.answer.slice(); });
  };

  var POSE = { left: "dz-left", right: "dz-right", up: "dz-up", jump: "dz-jump", spin: "dz-spin", wave: "dz-wave" };
  var MOOD = { up: "cheer", jump: "happy", wave: "wave" };

  CT.engines.dance = {
    mount: function (host, level, api) {
      var d = level.data, ri = 0, rd, slots, times, active = 0, wrong = {}, playing = false, hi = -1;
      var board = CT.el("div", { class: "cdz" });
      host.appendChild(board);
      var px = new CT.Pixel({ mood: "idle" });
      var dancer = CT.el("div", { class: "cdz-dancer" }, [px.svg]);
      var caption = CT.el("p", { class: "cdz-cap", "aria-live": "polite" }, "Ready to dance!");
      var stage = CT.el("div", { class: "cdz-stage" }, [CT.el("div", { class: "cdz-floor", "aria-hidden": "true" }), dancer, caption]);
      var area = CT.el("div");
      CT.append(board, [stage, area]);
      function move(id) { return CT.byId(d.moves, id); }

      function start(i) {
        ri = i; rd = d.rounds[ri]; wrong = {}; hi = -1; active = 0;
        if (rd.type === "loop") { slots = []; for (var k = 0; k < rd.units; k++) slots.push(null); times = 1; }
        else slots = rd.answer.map(function () { return null; });
        pose(null);
        render();
        api.say(rd.say, "think", 3000);
      }
      function pose(id) {
        dancer.className = "cdz-dancer" + (id ? " " + POSE[id] : "");
        px.mood(id && MOOD[id] ? MOOD[id] : "idle");
        caption.textContent = id ? move(id).icon + " " + move(id).text : "Ready to dance!";
      }
      // The full dance the student has programmed, gaps still empty.
      function programmed() {
        if (rd.type === "next") return rd.shown.concat(slots);
        if (rd.type === "gap") { var g = 0; return rd.shown.map(function (m) { return m === null ? slots[g++] : m; }); }
        return CT.expandLoop(times, slots);
      }

      function chip(id, extra) {
        var m = id ? move(id) : null;
        return CT.el("span", Object.assign({ class: "cdz-chip" + (m ? "" : " is-empty") }, extra || {}), m ? [CT.el("span", { "aria-hidden": "true" }, m.icon), CT.el("small", null, m.text)] : "?");
      }
      function slotBtn(k) {
        var id = slots[k];
        return CT.el("button", { type: "button", class: "cdz-slot" + (k === active ? " is-active" : "") + (wrong[k] ? " is-wrong" : "") + (id ? " is-full" : ""), "data-slot": String(k),
          "aria-label": "Move " + (k + 1) + (id ? ": " + move(id).text : ", empty") + (k === active ? ", selected" : ""),
          onclick: function () { if (k === active && slots[k]) slots[k] = null; active = k; wrong = {}; render("[data-slot='" + k + "']"); } }, chip(id));
      }

      function render(focus) {
        CT.clear(area);
        area.appendChild(CT.roundChip(ri, d.rounds.length));
        var strip = CT.el("ol", { class: "cdz-strip", "aria-label": rd.type === "loop" ? "The robot's dance" : "The dance so far" });
        if (rd.type === "loop") rd.target.forEach(function (m, i) { strip.appendChild(CT.el("li", { class: i === hi ? "is-now" : "" }, chip(m))); });
        else {
          var g = 0;
          rd.shown.forEach(function (m, i) {
            if (m === null) { var k = g++; strip.appendChild(CT.el("li", { class: "is-gap" + (i === hi ? " is-now" : "") }, slotBtn(k))); }
            else strip.appendChild(CT.el("li", { class: i === hi ? "is-now" : "" }, chip(m)));
          });
          if (rd.type === "next") slots.forEach(function (x, k) { strip.appendChild(CT.el("li", { class: "is-gap" + (rd.shown.length + k === hi ? " is-now" : "") }, slotBtn(k))); });
        }
        area.appendChild(CT.el("div", { class: "cdz-row" }, [strip,
          CT.el("button", { type: "button", class: "ct-btn ct-btn-mini", disabled: playing ? true : null, onclick: function () { watch(); } }, rd.type === "loop" ? "▶ Watch the dance" : "▶ Watch it again")]));
        if (rd.type === "loop") {
          var loop = CT.el("div", { class: "cdz-loop" }, [
            CT.el("p", { class: "cdz-kw" }, [
              CT.el("b", null, "repeat "),
              CT.el("button", { type: "button", class: "cdz-step", "aria-label": "Fewer times", onclick: function () { times = Math.max(1, times - 1); render(); } }, "−"),
              CT.el("output", { class: "cdz-times", "aria-live": "polite", "aria-label": times + " times" }, String(times)),
              CT.el("button", { type: "button", class: "cdz-step", "aria-label": "More times", onclick: function () { times = Math.min(9, times + 1); render(); } }, "+"),
              CT.el("b", null, " times:")]),
            CT.el("div", { class: "cdz-body" }, slots.map(function (x, k) { return slotBtn(k); })),
            CT.el("p", { class: "cdz-kw" }, CT.el("b", null, "end repeat")),
            CT.el("p", { class: "cdz-count" }, "Your loop makes " + CT.expandLoop(times, slots).length + " moves. The robot's dance has " + rd.target.length + ".")
          ]);
          area.appendChild(loop);
        }
        var palEl = CT.el("div", { class: "cdz-pal", role: "group", "aria-label": "Moves" }, [CT.el("p", { class: "ct-tray-h" }, "Moves: pick a box, then a move")]);
        d.moves.forEach(function (m) {
          palEl.appendChild(CT.el("button", { type: "button", class: "cdz-move", "data-move": m.id, "aria-label": "Put " + m.text + " in the selected box", onclick: function () {
            slots[active] = m.id; wrong = {};
            var next = slots.map(function (x, k) { return k; }).filter(function (k) { return !slots[k]; })[0];
            if (next !== undefined) active = next;
            pose(m.id);
            CT.sound.play("drop");
            render();
          } }, [CT.el("span", { "aria-hidden": "true" }, m.icon), m.text]));
        });
        area.appendChild(palEl);
        if (focus) { var f = area.querySelector(focus); if (f) f.focus(); }
      }

      function play(list, done) {
        playing = true; api.busy(true);
        var i = 0;
        (function step() {
          if (!api.alive()) return;
          if (i >= list.length) { playing = false; api.busy(false); hi = -1; pose(null); render(); if (done) done(); return; }
          hi = i;
          pose(list[i]);
          if (list[i]) CT.sound.play("step");
          else caption.textContent = "❓ ...";
          render();
          i++;
          CT.wait(650, step);
        })();
      }
      function watch() {
        if (playing) return;
        play(rd.type === "loop" ? rd.target : rd.type === "gap" ? rd.shown : rd.shown);
      }

      start(0);
      CT.wait(500, function () { if (api.alive() && !playing) watch(); });
      return {
        checkLabel: "▶ Dance!",
        run: function (done) {
          var a = rd.type === "loop" ? { times: times, unit: slots } : slots;
          var r = checkRound(d, rd, a);
          if (r.incomplete) { done(r); return; }
          play(programmed(), function () {
            if (r.ok) {
              px.mood("cheer", 1500);
              done(ri < d.rounds.length - 1 ? CT.nextRound(api, ri, d.rounds.length, start) : r);
            } else done(r);
          });
        },
        mark: function (r) { wrong = {}; (r.wrong || []).forEach(function (k) { wrong[k] = true; }); render(); },
        reset: function () { start(ri); },
        showMe: function () {
          if (rd.type === "loop") { times = rd.answer.times; slots = rd.answer.unit.slice(); while (slots.length < rd.units) slots.push(null); }
          else slots = rd.answer.slice();
          wrong = {}; render();
        },
        scaffold: function () {
          if (rd.type === "loop") {
            if (times !== rd.answer.times) times = rd.answer.times;
            else { var k = rd.answer.unit.findIndex(function (m, i) { return slots[i] !== m; }); if (k >= 0) slots[k] = rd.answer.unit[k]; }
          } else {
            var j = rd.answer.findIndex(function (m, i) { return slots[i] !== m; });
            if (j >= 0) slots[j] = rd.answer[j];
          }
          wrong = {}; render();
          CT.announce("Pixel programmed one step for you.");
        },
        destroy: function () { }
      };
    }
  };
})(typeof window !== "undefined" ? window : globalThis);
