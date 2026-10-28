/* Engine: order. Put steps in a sequence that works.
 *
 * data: { problem, items: [{id, text, icon}], order: [ids],
 *         rules: [[before, after, why]] (optional), flow: true (optional), rounds: [...] (optional) }
 * With rules, any order that keeps every rule is right, because real tasks
 * often have more than one correct order. Without them, data.order is the answer.
 * With flow, a live flowchart (Start, one box per step, End) is drawn beside the list.
 * With code, the steps are lines of pseudocode, shown in a code font with their indents.
 * answer: [ids in order], or with rounds { round: i, order: [...] }.
 */
(function (root) {
  "use strict";
  var CT = root.CT = root.CT || {};

  function checkOne(d, order) {
    if (!order || order.length !== d.items.length) return { ok: false, incomplete: true, msg: "Every step needs a place in the list." };
    if (d.rules && d.rules.length) {
      for (var i = 0; i < d.rules.length; i++) {
        var r = d.rules[i], a = order.indexOf(r[0]), b = order.indexOf(r[1]);
        if (a > b) return { ok: false, wrong: [r[0], r[1]], msg: r[2] };
      }
      return { ok: true };
    }
    var bad = [];
    order.forEach(function (id, i) { if (d.order[i] !== id) bad.push(id); });
    if (!bad.length) return { ok: true };
    var first = CT.byId(d.items, bad[0]);
    return { ok: false, wrong: bad, msg: bad.length + " step" + (bad.length > 1 ? "s are" : " is") + " out of place. " + (first && first.why ? first.why : "Check what has to happen first.") };
  }
  CT.check.order = function (data, answer) {
    if (data.rounds) {
      for (var i = 0; i < data.rounds.length; i++) {
        var r = checkOne(data.rounds[i], answer && answer[i]);
        if (!r.ok) return r;
      }
      return { ok: true };
    }
    return checkOne(data, answer);
  };
  CT.solve.order = function (data) {
    return data.rounds ? data.rounds.map(function (r) { return r.order.slice(); }) : data.order.slice();
  };

  // A flowchart of a plain sequence: Start, the steps, End.
  CT.seqFlow = function (steps) {
    var W = 260, boxH = 40, gap = 22, y = 10, parts = [];
    var H = 10 + (steps.length + 2) * (boxH + gap);
    function arrow(y1, y2) { return '<path d="M130 ' + y1 + ' V' + (y2 - 2) + '" class="fl-arrow" marker-end="url(#ct-arrow)"/>'; }
    parts.push('<rect x="80" y="' + y + '" width="100" height="' + boxH + '" rx="20" class="fl-term"/><text x="130" y="' + (y + 25) + '" class="fl-t">Start</text>');
    steps.forEach(function (s) {
      parts.push(arrow(y + boxH, y + boxH + gap));
      y += boxH + gap;
      parts.push('<rect x="20" y="' + y + '" width="220" height="' + boxH + '" rx="4" class="fl-proc"/><text x="130" y="' + (y + 25) + '" class="fl-t fl-t-s">' + esc(s) + '</text>');
    });
    parts.push(arrow(y + boxH, y + boxH + gap));
    y += boxH + gap;
    parts.push('<rect x="80" y="' + y + '" width="100" height="' + boxH + '" rx="20" class="fl-term"/><text x="130" y="' + (y + 25) + '" class="fl-t">End</text>');
    return '<svg viewBox="0 0 ' + W + ' ' + H + '" class="ct-flow-mini" role="img" aria-label="Flowchart: Start, ' + steps.map(esc).join(", ") + ', End">' +
      '<defs><marker id="ct-arrow" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" class="fl-head"/></marker></defs>' + parts.join("") + '</svg>';
  };
  function esc(s) { return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }
  function short(t) { return t.length > 30 ? t.slice(0, 28) + "…" : t; }

  CT.engines.order = {
    mount: function (host, level, api) {
      var rounds = level.data.rounds || [level.data], ri = 0, d, order, wrong = {};
      var board = CT.el("div", { class: "co" });
      host.appendChild(board);

      function start(i) {
        ri = i; d = rounds[ri]; wrong = {};
        order = CT.scramble(d.items.map(function (x) { return x.id; }), CT.rng(level.id + ":" + ri));
        render();
      }
      function moveTo(id, idx) {
        var from = order.indexOf(id);
        order.splice(from, 1);
        if (idx > from) idx -= 1;
        order.splice(Math.max(0, Math.min(order.length, idx)), 0, id);
      }
      function render() {
        CT.clear(board);
        if (rounds.length > 1) board.appendChild(CT.el("p", { class: "ct-round" }, "Round " + (ri + 1) + " of " + rounds.length));
        if (d.problem) board.appendChild(CT.el("div", { class: "ct-problem" }, [CT.el("span", { class: "ct-problem-k" }, d.kicker || "Task"), d.problem]));
        var list = CT.el("ol", { class: "co-list ct-zone", "data-zone": "list", "data-zone-label": "the sequence" });
        order.forEach(function (id, i) {
          var it = CT.byId(d.items, id);
          var li = CT.el("li", { class: "co-row" }, [
            CT.el("span", { class: "co-n", "aria-hidden": "true" }, String(i + 1)),
            CT.card(it, { "aria-label": "Step " + (i + 1) + ": " + it.text + (wrong[id] ? ". Out of place." : "") }),
            CT.el("span", { class: "co-moves" }, [
              CT.el("button", { type: "button", class: "co-mv", "aria-label": "Move " + it.text + " up", disabled: i === 0 ? true : null,
                onclick: function () { moveTo(id, i - 1); wrong = {}; render(); CT.sound.play("drop"); focusMv(id, "up"); } }, CT.ico("arrow-up")),
              CT.el("button", { type: "button", class: "co-mv", "aria-label": "Move " + it.text + " down", disabled: i === order.length - 1 ? true : null,
                onclick: function () { moveTo(id, i + 2); wrong = {}; render(); CT.sound.play("drop"); focusMv(id, "down"); } }, CT.ico("arrow-down"))
            ])
          ]);
          if (wrong[id]) li.querySelector(".ct-card").classList.add("is-wrong");
          if (d.code) li.querySelector(".ct-card").classList.add("is-code");
          list.appendChild(li);
        });
        var wrap = CT.el("div", { class: "co-wrap" + (d.flow ? " has-flow" : "") }, [list]);
        if (d.flow) {
          var fl = CT.el("div", { class: "co-flow" }, [CT.el("p", { class: "ct-tray-h" }, "Your algorithm as a flowchart")]);
          fl.insertAdjacentHTML("beforeend", CT.seqFlow(order.map(function (id) { return short(CT.byId(d.items, id).text); })));
          wrap.appendChild(fl);
        }
        board.appendChild(wrap);
      }
      function focusMv(id, dir) {
        setTimeout(function () {
          var idx = order.indexOf(id), rows = board.querySelectorAll(".co-row");
          var b = rows[idx] && rows[idx].querySelectorAll(".co-mv")[dir === "up" ? 0 : 1];
          if (b && !b.disabled) b.focus(); else if (rows[idx]) rows[idx].querySelector(".ct-card").focus();
        }, 0);
      }
      var dd = CT.dnd(board, { sortable: true, onMove: function (id, zone, idx) { moveTo(id, idx); wrong = {}; render(); } });
      start(0);

      function correctOrder() { return d.order; }
      return {
        answer: function () { return rounds.length > 1 ? null : order; },
        check: function () {
          var r = checkOne(d, order);
          if (r.ok && ri < rounds.length - 1) {
            setTimeout(function () { start(ri + 1); }, CT.calm() ? 50 : 900);
            return { ok: true, more: true, msg: "Round " + (ri + 1) + " done! Here comes the next task.", toast: "Round " + (ri + 1) + " of " + rounds.length + " complete!" };
          }
          return r;
        },
        mark: function (r) { wrong = {}; (r.wrong || []).forEach(function (id) { wrong[id] = true; }); render(); },
        reset: function () { start(ri); },
        showMe: function () { order = correctOrder().slice(); wrong = {}; render(); },
        scaffold: function () {
          var target = correctOrder();
          for (var i = 0; i < target.length; i++) {
            if (order[i] !== target[i]) { moveTo(target[i], i); render(); CT.announce("Pixel moved " + CT.byId(d.items, target[i]).text + " to step " + (i + 1) + "."); return; }
          }
        },
        demo: function (done) {
          var target = correctOrder(), id = target[0];
          var from = board.querySelector('[data-item="' + id + '"]'), to = board.querySelector(".co-row");
          CT.ghost(from, to, function () { moveTo(id, 0); render(); done(); });
        },
        destroy: function () { dd.destroy(); }
      };
    }
  };
})(typeof window !== "undefined" ? window : globalThis);
