/* Engine: model. Design a product for one person: only the features they need.
 *
 * data: { features: [{id, text, icon}],
 *         rounds: [{name, age, icon, needs: [{text, feature}], extraWhy: {featureId: why}}] }
 * The phone on screen grows each feature as it is fitted. A round is right
 * when every need is met by its feature and nothing else is fitted.
 * answer: [[featureId...] per round]
 */
(function (root) {
  "use strict";
  var CT = root.CT = root.CT || {};

  function checkRound(d, rd, picks) {
    picks = (picks || []).filter(Boolean);
    if (picks.length < rd.needs.length) return { ok: false, incomplete: true, msg: "Fit all " + rd.needs.length + " features first: " + (rd.needs.length - picks.length) + " still empty." };
    var needed = rd.needs.map(function (n) { return n.feature; });
    var extra = picks.filter(function (f) { return needed.indexOf(f) < 0; });
    if (extra.length) {
      var f = CT.byId(d.features, extra[0]);
      return { ok: false, wrong: extra, msg: (rd.extraWhy && rd.extraWhy[extra[0]]) || rd.name + " does not need the " + f.text.toLowerCase() + "." };
    }
    return { ok: true };
  }
  CT.check.model = function (d, a) {
    a = a || [];
    for (var i = 0; i < d.rounds.length; i++) {
      var r = checkRound(d, d.rounds[i], a[i]);
      if (!r.ok) return Object.assign(r, { round: i });
    }
    return { ok: true };
  };
  CT.solve.model = function (d) { return d.rounds.map(function (rd) { return rd.needs.map(function (n) { return n.feature; }); }); };

  // The phone, drawn with whichever features are fitted.
  CT.phone = function (on) {
    var has = function (f) { return on.indexOf(f) >= 0; };
    var body = has("gold") ? "#D4A017" : "#1F2937";
    var s = '<svg viewBox="0 0 200 300" class="cmd-phone" aria-hidden="true">';
    if (has("projector")) s += '<path d="M100 22 L40 0 H160 Z" fill="#FDE68A" opacity=".7"/>';
    if (has("stylus")) s += '<rect x="168" y="70" width="8" height="150" rx="4" fill="#0EA5E9"/><path d="M168 220 l4 14 l4 -14 z" fill="#334155"/>';
    if (has("tough")) s += '<rect x="34" y="16" width="132" height="272" rx="30" fill="#F97316"/>';
    s += '<rect x="42" y="24" width="116" height="256" rx="24" fill="' + body + '"/><rect x="50" y="44" width="100" height="208" rx="8" fill="#E0F2FE"/>';
    if (has("loud")) s += '<rect x="80" y="31" width="40" height="6" rx="3" fill="#94A3B8"/><path d="M164 40 q10 10 0 20 M172 34 q16 16 0 32" stroke="#0EA5E9" stroke-width="3" fill="none"/>';
    else s += '<rect x="88" y="32" width="24" height="4" rx="2" fill="#475569"/>';
    if (has("camera")) s += '<rect x="54" y="48" width="34" height="34" rx="9" fill="#334155"/><circle cx="63" cy="57" r="5" fill="#0EA5E9"/><circle cx="79" cy="57" r="5" fill="#0EA5E9"/><circle cx="63" cy="73" r="5" fill="#0EA5E9"/><circle cx="79" cy="73" r="3" fill="#FDE68A"/>';
    if (has("battery")) s += '<rect x="104" y="50" width="38" height="16" rx="3" fill="#fff" stroke="#15803D" stroke-width="2"/><rect x="107" y="53" width="30" height="10" fill="#22C55E"/><rect x="142" y="54" width="3" height="8" fill="#15803D"/><text x="123" y="78" text-anchor="middle" font-size="9" font-weight="800" fill="#15803D">3 days</text>';
    if (has("bigtext")) s += '<text x="100" y="128" text-anchor="middle" font-size="40" font-weight="800" fill="#0F172A">Aa</text>' +
      '<rect x="58" y="142" width="38" height="30" rx="6" fill="#0EA5E9"/><rect x="104" y="142" width="38" height="30" rx="6" fill="#22C55E"/><rect x="58" y="178" width="38" height="30" rx="6" fill="#F59E0B"/><rect x="104" y="178" width="38" height="30" rx="6" fill="#A855F7"/>';
    else s += '<g fill="#94A3B8">' + [0, 1, 2, 3].map(function (r) { return [0, 1, 2, 3].map(function (c) { return '<rect x="' + (58 + c * 22) + '" y="' + (96 + r * 22) + '" width="16" height="16" rx="4"/>'; }).join(""); }).join("") + "</g>";
    if (has("gaming")) s += '<rect x="64" y="212" width="72" height="30" rx="15" fill="#4C1D95"/><circle cx="80" cy="227" r="5" fill="#C4B5FD"/><circle cx="118" cy="222" r="3" fill="#F472B6"/><circle cx="124" cy="230" r="3" fill="#34D399"/>';
    if (has("fold")) s += '<path d="M100 44 V252" stroke="#64748B" stroke-width="2" stroke-dasharray="6 4"/>';
    if (has("sos")) s += '<rect x="156" y="96" width="14" height="36" rx="5" fill="#DC2626"/><text x="163" y="118" text-anchor="middle" font-size="6" font-weight="800" fill="#fff" transform="rotate(90 163 114)">SOS</text>';
    if (has("fast")) s += '<path d="M96 280 v14 M104 280 v14" stroke="#334155" stroke-width="4"/><path d="M110 256 l-12 14 h8 l-4 12 l14 -16 h-8 l4 -10 z" fill="#FACC15" stroke="#A16207"/>';
    return s + "</svg>";
  };

  CT.engines.model = {
    mount: function (host, level, api) {
      var d = level.data, ri = 0, rd, slots, wrong = {}, met = false;
      var order = CT.shuffle(d.features.map(function (f) { return f.id; }), CT.rng(level.id + ":f"));
      var board = CT.el("div", { class: "cmd" });
      host.appendChild(board);

      function start(i) {
        ri = i; rd = d.rounds[ri]; slots = rd.needs.map(function () { return null; }); wrong = {}; met = false;
        render();
        if (i > 0) api.say("Next customer: " + rd.name + "!", "wave", 2400);
      }
      function render() {
        CT.clear(board);
        var who = CT.el("div", { class: "cmd-who" }, [
          CT.el("div", { class: "cmd-ava", "aria-hidden": "true" }, rd.icon),
          CT.el("div", null, [CT.el("p", { class: "cmd-name" }, rd.name + ", " + rd.age),
            CT.el("ul", { class: "cmd-needs", "aria-label": rd.name + "'s needs" }, rd.needs.map(function (n) {
              return CT.el("li", { class: met ? "is-met" : "" }, [CT.el("span", { "aria-hidden": "true" }, met ? "✅ " : "• "), n.text]);
            }))])
        ]);
        var ph = CT.el("div", { class: "cmd-phonewrap" + (met ? " is-met" : "") });
        ph.innerHTML = CT.phone(slots.filter(Boolean));
        var sl = CT.el("div", { class: "cmd-slots" });
        slots.forEach(function (id, i) {
          var z = CT.el("div", { class: "cid-slot ct-zone" + (id ? " is-full" : ""), "data-zone": "slot-" + i, "data-zone-label": "feature slot " + (i + 1) });
          if (id) { var c = CT.card(CT.byId(d.features, id)); if (wrong[id]) c.classList.add("is-wrong"); z.appendChild(c); }
          else z.appendChild(CT.el("span", { class: "ctr-empty" }, "Feature " + (i + 1)));
          z.appendChild(CT.el("button", { type: "button", class: "ct-drop", "aria-label": "Fit the picked feature in slot " + (i + 1) }, "Put here"));
          sl.appendChild(z);
        });
        var tray = CT.el("div", { class: "ct-tray", "data-zone": "tray", "data-zone-label": "the feature shelf" }, [CT.el("p", { class: "ct-tray-h" }, "Feature shelf")]);
        order.filter(function (id) { return slots.indexOf(id) < 0; }).forEach(function (id) { tray.appendChild(CT.card(CT.byId(d.features, id))); });
        CT.append(board, [CT.roundChip(ri, d.rounds.length, "Customer"),
          CT.el("div", { class: "cmd-top" }, [who, CT.el("div", { class: "cmd-build" }, [ph, sl])]), tray]);
      }
      var dd = CT.dnd(board, {
        canDrop: function () { return !met; },
        onMove: function (id, zone) {
          var from = slots.indexOf(id);
          if (zone === "tray") { if (from >= 0) slots[from] = null; }
          else { var to = Number(zone.slice(5)), there = slots[to]; if (from >= 0) slots[from] = there; slots[to] = id; }
          wrong = {}; render();
        }
      });
      start(0);
      return {
        check: function () {
          var r = checkRound(d, rd, slots);
          if (!r.ok) return r;
          met = true; render();
          if (ri < d.rounds.length - 1) return CT.nextRound(api, ri, d.rounds.length, start, "Customer");
          return r;
        },
        mark: function (r) { wrong = {}; (r.wrong || []).forEach(function (id) { wrong[id] = true; }); render(); },
        reset: function () { start(ri); },
        showMe: function () { slots = rd.needs.map(function (n) { return n.feature; }); wrong = {}; render(); },
        scaffold: function () {
          var needed = rd.needs.map(function (n) { return n.feature; });
          var miss = needed.filter(function (f) { return slots.indexOf(f) < 0; })[0];
          if (!miss) return;
          var at = slots.indexOf(null);
          if (at < 0) at = slots.findIndex(function (f) { return needed.indexOf(f) < 0; });
          slots[at] = miss; wrong = {}; render();
          CT.announce("Pixel fitted the " + CT.byId(d.features, miss).text + ".");
        },
        destroy: function () { dd.destroy(); }
      };
    }
  };
})(typeof window !== "undefined" ? window : globalThis);
