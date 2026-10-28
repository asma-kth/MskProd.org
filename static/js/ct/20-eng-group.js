/* Engine: group. Cards go into the boxes they belong to.
 *
 * data: { problem, zones: [{id, label, icon, pin}], items: [{id, text, icon, zone, why}],
 *         picture: "robot" (optional), followup: {q, options, answer, why} (optional) }
 * A follow-up question appears once the groups are right, so the student has
 * to say why the split helps, not only make it.
 * answer: { itemId: zoneId } for every placed card, plus follow: option index
 */
(function (root) {
  "use strict";
  var CT = root.CT = root.CT || {};

  CT.check.group = function (data, answer) {
    answer = answer || {};
    var left = data.items.filter(function (it) { return !answer[it.id]; });
    if (left.length) return { ok: false, incomplete: true, msg: "Place every card first: " + left.length + " still to go." };
    var wrong = data.items.filter(function (it) { return answer[it.id] !== it.zone; });
    if (!wrong.length) {
      if (data.followup && answer.follow !== data.followup.answer) {
        if (answer.follow === undefined || answer.follow === null) return { ok: false, incomplete: true, needFollow: true, msg: "Your groups are right! Now answer Pixel's question." };
        return { ok: false, msg: data.followup.why };
      }
      return { ok: true };
    }
    return { ok: false, wrong: wrong.map(function (w) { return w.id; }),
             msg: (wrong.length === 1 ? "One card is in the wrong box. " : wrong.length + " cards are in the wrong box. ") + wrong[0].why };
  };
  CT.solve.group = function (data) {
    var a = {};
    data.items.forEach(function (it) { a[it.id] = it.zone; });
    if (data.followup) a.follow = data.followup.answer;
    return a;
  };

  // Pictures a group board can show, with numbered pins matching its boxes.
  CT.pics = CT.pics || {};
  CT.pics.robot = function () {
    return '<svg viewBox="0 0 220 230" class="cg-pic" role="img" aria-label="A broken robot: 1 sensors in its head, 2 power in its body, 3 movement in its wheels">' +
      '<line x1="110" y1="14" x2="110" y2="38" stroke="#475569" stroke-width="5"/><circle cx="110" cy="12" r="8" fill="#F59E0B"/>' +
      '<rect x="62" y="36" width="96" height="66" rx="18" fill="#94A3B8" stroke="#334155" stroke-width="4"/>' +
      '<circle cx="92" cy="66" r="14" fill="#E2E8F0" stroke="#334155" stroke-width="3"/><circle cx="92" cy="66" r="6" fill="#0EA5E9"/>' +
      '<rect x="114" y="56" width="30" height="20" rx="5" fill="#1F2937"/><path d="M118 66 h8 l3 -5 l4 10 l3 -5 h5" stroke="#22C55E" stroke-width="2" fill="none"/>' +
      '<rect x="50" y="108" width="120" height="74" rx="14" fill="#CBD5E1" stroke="#334155" stroke-width="4"/>' +
      '<rect x="92" y="122" width="36" height="46" rx="5" fill="#fff" stroke="#334155" stroke-width="3"/><rect x="104" y="117" width="12" height="6" fill="#334155"/>' +
      '<rect x="96" y="150" width="28" height="14" fill="#EF4444"/><path d="M28 120 h22 M170 120 h22" stroke="#475569" stroke-width="8" stroke-linecap="round"/>' +
      '<circle cx="80" cy="196" r="22" fill="#1F2937"/><circle cx="80" cy="196" r="8" fill="#94A3B8"/><circle cx="140" cy="196" r="22" fill="#1F2937"/><circle cx="140" cy="196" r="8" fill="#94A3B8"/>' +
      '<path d="M150 40 l10 -10 M156 50 l12 -4" stroke="#F59E0B" stroke-width="3" stroke-linecap="round"/>' +
      pin(186, 60, 1) + pin(196, 146, 2) + pin(186, 206, 3) +
      '<path d="M174 60 h-14 M184 146 h-22 M174 206 h-12" stroke="#0F2026" stroke-width="2" stroke-dasharray="3 3"/></svg>';
    function pin(x, y, n) { return '<circle cx="' + x + '" cy="' + y + '" r="12" fill="#EA580C" stroke="#fff" stroke-width="3"/><text x="' + x + '" y="' + (y + 5) + '" text-anchor="middle" font-size="14" font-weight="800" fill="#fff" font-family="Inter, sans-serif">' + n + '</text>'; }
  };

  CT.card = function (item, extra) {
    return CT.el("button", Object.assign({ type: "button", class: "ct-card", "data-item": item.id, "aria-pressed": "false" }, extra || {}), [
      item.icon ? CT.el("span", { class: "ct-card-i", "aria-hidden": "true" }, CT.ico(item.icon)) : null,
      CT.el("span", { class: "ct-card-t" }, item.text)
    ]);
  };

  CT.engines.group = {
    mount: function (host, level, api) {
      var data = level.data, ans = {}, order = CT.shuffle(data.items.map(function (i) { return i.id; }), api.rng);
      var wrongSet = {};
      var board = CT.el("div", { class: "cg" });
      host.appendChild(board);

      function render() {
        CT.clear(board);
        if (data.problem) board.appendChild(CT.el("div", { class: "ct-problem" }, [CT.el("span", { class: "ct-problem-k" }, data.kicker || "Big problem"), data.problem]));
        if (data.picture && CT.pics[data.picture]) {
          var pic = CT.el("div", { class: "cg-picwrap" });
          pic.innerHTML = CT.pics[data.picture]();
          board.appendChild(pic);
        }
        var tray = CT.el("div", { class: "ct-tray", "data-zone": "tray", "data-zone-label": "the card tray" }, [
          CT.el("p", { class: "ct-tray-h" }, "Cards to sort")]);
        var waiting = order.filter(function (id) { return !ans[id]; });
        waiting.forEach(function (id) { tray.appendChild(CT.card(CT.byId(data.items, id))); });
        if (!waiting.length) tray.appendChild(CT.el("p", { class: "ct-tray-empty" }, "All sorted! Press Check."));
        board.appendChild(tray);
        var zones = CT.el("div", { class: "cg-zones cg-n" + data.zones.length });
        data.zones.forEach(function (z) {
          var inZone = order.filter(function (id) { return ans[id] === z.id; });
          var box = CT.el("div", { class: "cg-zone", "data-zone": z.id, "data-zone-label": z.label }, [
            CT.el("div", { class: "cg-zone-h" }, [z.pin ? CT.el("span", { class: "cg-pin", "aria-label": "Part " + z.pin }, String(z.pin)) : null,
              CT.el("span", { class: "cg-zone-i", "aria-hidden": "true" }, CT.ico(z.icon || "box")),
              CT.el("b", null, z.label), CT.el("span", { class: "cg-count" }, String(inZone.length))]),
            CT.el("button", { type: "button", class: "ct-drop", "aria-label": "Put the picked card in " + z.label }, "Put here")
          ]);
          inZone.forEach(function (id) {
            var c = CT.card(CT.byId(data.items, id));
            if (wrongSet[id]) c.classList.add("is-wrong");
            box.appendChild(c);
          });
          zones.appendChild(box);
        });
        board.appendChild(zones);
        if (showFollow) board.appendChild(followBox());
      }

      // The question that comes once the groups are right.
      var showFollow = false;
      function followBox() {
        var f = data.followup;
        var box = CT.el("div", { class: "cg-follow" }, [CT.el("p", { class: "ct-kicker" }, "Question"), CT.el("h3", null, f.q)]);
        var opts = CT.el("div", { class: "ct-mcq" });
        CT.shuffle(f.options.map(function (o, i) { return i; }), CT.rng(level.id + ":f")).forEach(function (i) {
          opts.appendChild(CT.el("button", { type: "button", class: "ct-mcq-opt" + (ans.follow === i ? (i === f.answer ? " is-right" : " is-wrong") : ""), onclick: function () {
            ans.follow = i;
            render();
            api.result(i === f.answer ? { ok: true } : { ok: false, msg: f.why });
          } }, f.options[i]));
        });
        box.appendChild(opts);
        setTimeout(function () { box.scrollIntoView({ block: "nearest", behavior: CT.calm() ? "auto" : "smooth" }); }, 50);
        return box;
      }

      var dd = CT.dnd(board, {
        onMove: function (id, zone) {
          if (zone === "tray") delete ans[id]; else ans[id] = zone;
          delete wrongSet[id];
          render();
        }
      });
      render();

      function place(moves, done, i) {
        i = i || 0;
        if (i >= moves.length) { done && done(); return; }
        var m = moves[i];
        var from = board.querySelector('[data-item="' + m[0] + '"]'), to = board.querySelector('[data-zone="' + m[1] + '"]');
        CT.ghost(from, to, function () { ans[m[0]] = m[1]; render(); setTimeout(function () { place(moves, done, i + 1); }, 120); });
      }

      return {
        answer: function () { return ans; },
        check: function () {
          var r = CT.check.group(data, ans);
          if (r.needFollow && !showFollow) { showFollow = true; render(); }
          return r;
        },
        mark: function (r) { wrongSet = {}; (r.wrong || []).forEach(function (id) { wrongSet[id] = true; }); render(); },
        reset: function () { ans = {}; wrongSet = {}; showFollow = false; dd.cancel(); render(); },
        showMe: function () { ans = CT.solve.group(data); wrongSet = {}; showFollow = !!data.followup; render(); },
        scaffold: function () {
          var it = data.items.filter(function (x) { return ans[x.id] !== x.zone; })[0];
          if (it) place([[it.id, it.zone]]);
        },
        demo: function (done) { place((level.watch && level.watch.moves) || [], done); },
        destroy: function () { dd.destroy(); }
      };
    }
  };
})(typeof window !== "undefined" ? window : globalThis);
