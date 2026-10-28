/* Engine: identify. Choose the details that tell things apart.
 *
 * Poster mode: pick a few facts for a lost-property poster so that exactly one
 * of the look-alikes on the table matches it.
 *   data: { mode: "poster", noun, things: [{id, ...attributes}],
 *           rounds: [{target, name, slots, cards: [{id, text, icon, test: {attr: value} | null, why}]}] }
 *   A card with no test is true of every thing on the table, so it never helps.
 *   answer: [[cardId...] per round]
 * Sensors mode: fit a robot with the sensors whose readings separate every
 * kind of item, run it, then sort mystery items from their readings alone.
 *   data: { mode: "sensors", budget, classes: [{id, text, icon}], sensors: [{id, text, icon, why}],
 *           items: [{id, text, icon, cls, r: {sensorId: reading}}],
 *           mystery: [{id, label, reveal, cls, r, why}] }
 *   answer: { sensors: [sensorId...], sort: {mysteryId: classId} }
 */
(function (root) {
  "use strict";
  var CT = root.CT = root.CT || {};

  // ------------------------------------------------------------ poster logic
  function fits(card, t) {
    return !card.test || Object.keys(card.test).every(function (k) { return t[k] === card.test[k]; });
  }
  function matchesOf(d, rd, picks) {
    return d.things.filter(function (t) { return picks.every(function (id) { return fits(CT.byId(rd.cards, id), t); }); });
  }
  function posterRound(d, rd, picks) {
    picks = (picks || []).filter(Boolean);
    if (!picks.length) return { ok: false, incomplete: true, msg: "Put at least one detail on the poster." };
    if (picks.length > rd.slots) return { ok: false, msg: "The poster only has room for " + rd.slots + " details." };
    var useless = picks.map(function (id) { return CT.byId(rd.cards, id); }).filter(function (c) { return !c.test; });
    if (useless.length) return { ok: false, wrong: useless.map(function (c) { return c.id; }), msg: useless[0].why };
    var m = matchesOf(d, rd, picks).map(function (t) { return t.id; });
    if (m.length === 1 && m[0] === rd.target) return { ok: true, matches: m };
    return { ok: false, matches: m, msg: "The helper found " + m.length + " " + (d.noun || "things") +
      " that match your poster. Use a detail that tells them apart." };
  }

  // ----------------------------------------------------------- sensor logic
  function confusedPair(d, chosen) {
    for (var i = 0; i < d.items.length; i++) for (var j = i + 1; j < d.items.length; j++) {
      var a = d.items[i], b = d.items[j];
      if (a.cls !== b.cls && chosen.every(function (s) { return a.r[s] === b.r[s]; })) return [a, b];
    }
    return null;
  }
  function sensorRound(d, chosen) {
    chosen = (chosen || []).filter(Boolean);
    if (!chosen.length) return { ok: false, incomplete: true, msg: "Fit at least one sensor to the robot." };
    if (chosen.length > d.budget) return { ok: false, msg: "The robot only has power for " + d.budget + " sensors." };
    var p = confusedPair(d, chosen);
    if (p) return { ok: false, pair: [p[0].id, p[1].id],
      msg: "The robot cannot tell the " + p[0].text.toLowerCase() + " from the " + p[1].text.toLowerCase() +
           ": your sensors give them the same readings, but they belong in different bins." };
    return { ok: true };
  }
  function mysteryRound(d, sort) {
    sort = sort || {};
    var left = d.mystery.filter(function (m) { return !sort[m.id]; });
    if (left.length) return { ok: false, incomplete: true, msg: "Put every mystery item in a bin: " + left.length + " still to go." };
    var bad = d.mystery.filter(function (m) { return sort[m.id] !== m.cls; });
    if (bad.length) return { ok: false, wrong: bad.map(function (m) { return m.id; }), msg: bad[0].why };
    return { ok: true };
  }

  CT.check.identify = function (d, a) {
    if (d.mode === "sensors") {
      a = a || {};
      var r = sensorRound(d, a.sensors);
      return r.ok ? mysteryRound(d, a.sort) : r;
    }
    a = a || [];
    for (var i = 0; i < d.rounds.length; i++) {
      var p = posterRound(d, d.rounds[i], a[i]);
      if (!p.ok) return Object.assign(p, { round: i });
    }
    return { ok: true };
  };

  // The smallest set that works, found by trying every set in size order.
  function smallest(ids, max, works) {
    for (var size = 1; size <= max; size++) {
      var found = null;
      (function pick(startAt, chosen) {
        if (found) return;
        if (chosen.length === size) { if (works(chosen)) found = chosen.slice(); return; }
        for (var i = startAt; i < ids.length; i++) { chosen.push(ids[i]); pick(i + 1, chosen); chosen.pop(); }
      })(0, []);
      if (found) return found;
    }
    return null;
  }
  CT.solve.identify = function (d) {
    if (d.mode === "sensors") {
      var s = smallest(d.sensors.map(function (x) { return x.id; }), d.budget, function (c) { return sensorRound(d, c).ok; });
      var sort = {};
      d.mystery.forEach(function (m) { sort[m.id] = m.cls; });
      return { sensors: s, sort: sort };
    }
    return d.rounds.map(function (rd) {
      return smallest(rd.cards.filter(function (c) { return c.test; }).map(function (c) { return c.id; }), rd.slots,
        function (c) { return posterRound(d, rd, c).ok; });
    });
  };

  // --------------------------------------------------------------- drawing
  CT.teddy = function (t) {
    var fur = { brown: "#B7791F", white: "#F5F5F4", grey: "#9CA3AF" }[t.fur] || "#B7791F";
    var dark = { brown: "#713F12", white: "#A8A29E", grey: "#4B5563" }[t.fur] || "#713F12";
    var st = ' fill="' + fur + '" stroke="' + dark + '" stroke-width="2"';
    return '<svg viewBox="0 0 80 92" class="cid-teddy" aria-hidden="true">' +
      '<circle cx="19" cy="17" r="10"' + st + '/><circle cx="61" cy="17" r="10"' + st + '/>' +
      '<ellipse cx="40" cy="70" rx="24" ry="20"' + st + '/>' +
      '<circle cx="17" cy="78" r="7"' + st + '/><circle cx="63" cy="78" r="7"' + st + '/>' +
      '<circle cx="40" cy="34" r="22"' + st + '/>' +
      '<ellipse cx="40" cy="43" rx="10" ry="7" fill="#FEF3C7" opacity=".85"/><circle cx="40" cy="40" r="3" fill="#1F2937"/>' +
      '<circle cx="31" cy="30" r="3" fill="#1F2937"/><circle cx="49" cy="30" r="3" fill="#1F2937"/>' +
      (t.patch === "yes" ? '<path d="M19 22 L61 19" stroke="#111827" stroke-width="2"/><circle cx="31" cy="30" r="7" fill="#111827"/>' : "") +
      (t.neck === "bow" ? '<path d="M40 57 l-12 -7 v14 z M40 57 l12 -7 v14 z" fill="#DC2626"/><circle cx="40" cy="57" r="3.5" fill="#991B1B"/>' : "") +
      (t.neck === "scarf" ? '<path d="M19 54 q21 9 42 0 v8 q-21 9 -42 0 z" fill="#2563EB"/><path d="M50 61 l4 17 l7 -2 l-4 -16 z" fill="#1D4ED8"/>' : "") +
      "</svg>";
  };

  function scanner() {
    return '<svg viewBox="0 0 120 90" class="cid-robot" aria-hidden="true"><rect x="30" y="18" width="60" height="44" rx="12" fill="#64748B" stroke="#1E293B" stroke-width="3"/>' +
      '<circle cx="48" cy="38" r="7" fill="#E0F2FE" stroke="#1E293B" stroke-width="2"/><circle cx="72" cy="38" r="7" fill="#E0F2FE" stroke="#1E293B" stroke-width="2"/>' +
      '<circle cx="48" cy="38" r="3" fill="#0EA5E9"/><circle cx="72" cy="38" r="3" fill="#0EA5E9"/><rect x="50" y="50" width="20" height="4" rx="2" fill="#1E293B"/>' +
      '<path d="M60 18 V6" stroke="#1E293B" stroke-width="3"/><circle cx="60" cy="5" r="4" fill="#F59E0B"/>' +
      '<path class="cid-beam" d="M46 62 L20 90 H100 L74 62 Z" fill="#FDE68A" opacity=".5"/></svg>';
  }

  CT.engines.identify = {
    mount: function (host, level, api) {
      return level.data.mode === "sensors" ? sensorsGame(host, level, api) : posterGame(host, level, api);
    }
  };

  // ------------------------------------------------------------ poster game
  function posterGame(host, level, api) {
    var d = level.data, ri = 0, rd, picks, wrong = {}, marks = {}, cardOrder, scanning = false;
    var lineup = CT.shuffle(d.things.map(function (t) { return t.id; }), CT.rng(level.id + ":line"));
    var board = CT.el("div", { class: "cid" });
    host.appendChild(board);

    function start(i) {
      ri = i; rd = d.rounds[ri]; picks = rd.cards.map(function () { return null; }).slice(0, rd.slots);
      wrong = {}; marks = {};
      cardOrder = CT.shuffle(rd.cards.map(function (c) { return c.id; }), CT.rng(level.id + ":c" + ri));
      render();
      if (i > 0) api.say("Oh no, " + rd.name + " is lost too! This poster has room for only " + rd.slots + " details.", "think", 3200);
    }
    function render() {
      CT.clear(board);
      var target = CT.byId(d.things, rd.target);
      var mine = CT.el("figure", { class: "cid-mine" });
      mine.innerHTML = CT.teddy(target);
      mine.appendChild(CT.el("figcaption", null, [CT.el("b", null, rd.name), " is lost!"]));
      var poster = CT.el("div", { class: "cid-poster" }, [CT.el("p", { class: "cid-poster-h" }, "LOST: " + rd.name.toUpperCase()),
        CT.el("p", { class: "cid-poster-s" }, "Room for " + rd.slots + " details")]);
      picks.forEach(function (id, i) {
        var slot = CT.el("div", { class: "cid-slot ct-zone" + (id ? " is-full" : ""), "data-zone": "slot-" + i, "data-zone-label": "poster line " + (i + 1) });
        if (id) { var c = CT.card(CT.byId(rd.cards, id)); if (wrong[id]) c.classList.add("is-wrong"); slot.appendChild(c); }
        else slot.appendChild(CT.el("span", { class: "ctr-empty" }, "Detail " + (i + 1)));
        slot.appendChild(CT.el("button", { type: "button", class: "ct-drop", "aria-label": "Put the picked card on poster line " + (i + 1) }, "Put here"));
        poster.appendChild(slot);
      });
      var table = CT.el("div", { class: "cid-table", role: "list", "aria-label": "The lost-property table" });
      lineup.forEach(function (tid, k) {
        var f = CT.el("figure", { class: "cid-t" + (marks[tid] ? " is-" + marks[tid] : ""), role: "listitem",
          "aria-label": "Teddy " + (k + 1) + (marks[tid] === "match" ? ", matches the poster" : marks[tid] === "out" ? ", ruled out" : "") });
        f.innerHTML = CT.teddy(CT.byId(d.things, tid));
        f.appendChild(CT.el("figcaption", null, String(k + 1)));
        table.appendChild(f);
      });
      var tray = CT.el("div", { class: "ct-tray", "data-zone": "tray", "data-zone-label": "the details" }, [CT.el("p", { class: "ct-tray-h" }, "Details about " + rd.name)]);
      cardOrder.filter(function (id) { return picks.indexOf(id) < 0; }).forEach(function (id) {
        var c = CT.card(CT.byId(rd.cards, id)); if (wrong[id]) c.classList.add("is-wrong"); tray.appendChild(c);
      });
      CT.append(board, [CT.roundChip(ri, d.rounds.length, "Poster"),
        CT.el("div", { class: "cid-top" }, [mine, poster]),
        CT.el("div", { class: "cid-tablewrap" }, [CT.el("p", { class: "ct-tray-h" }, "The lost-property table"), table]),
        tray]);
    }
    var dd = CT.dnd(board, {
      canDrop: function () { return !scanning; },
      onMove: function (id, zone) {
        var from = picks.indexOf(id);
        if (zone === "tray") { if (from >= 0) picks[from] = null; }
        else { var to = Number(zone.slice(5)), there = picks[to]; if (from >= 0) picks[from] = there; picks[to] = id; }
        wrong = {}; marks = {};
        render();
      }
    });
    start(0);

    function finish(r, done) {
      if (r.ok && ri < d.rounds.length - 1) done(CT.nextRound(api, ri, d.rounds.length, start, "Poster"));
      else done(r);
    }
    return {
      checkLabel: "Send the poster",
      run: function (done) {
        var r = posterRound(d, rd, picks);
        if (!r.matches) { done(r); return; }
        scanning = true; api.busy(true); marks = {};
        var k = 0;
        (function step() {
          if (!api.alive()) return;
          if (k >= lineup.length) {
            scanning = false; api.busy(false);
            if (r.ok) api.say("The helper found " + rd.name + "!", "happy", 2000);
            finish(r, done);
            return;
          }
          var tid = lineup[k++];
          marks[tid] = r.matches.indexOf(tid) >= 0 ? "match" : "out";
          render();
          CT.sound.play(marks[tid] === "match" ? "pick" : "step");
          CT.wait(240, step);
        })();
      },
      mark: function (r) { wrong = {}; (r.wrong || []).forEach(function (id) { wrong[id] = true; }); render(); },
      reset: function () { start(ri); },
      showMe: function () { var sol = CT.solve.identify(d)[ri]; picks = picks.map(function (x, i) { return sol[i] || null; }); wrong = {}; marks = {}; render(); },
      scaffold: function () {
        var sol = CT.solve.identify(d)[ri], need = sol.filter(function (id) { return picks.indexOf(id) < 0; })[0];
        if (!need) return;
        var at = picks.indexOf(null);
        if (at < 0) at = picks.findIndex(function (id) { return sol.indexOf(id) < 0; });
        if (at < 0) return;
        picks[at] = need; marks = {}; render();
        CT.announce("Pixel added " + CT.byId(rd.cards, need).text + " to the poster.");
      },
      demo: function (done) {
        var mv = (level.watch && level.watch.moves) || [];
        if (!mv.length) { done(); return; }
        var from = board.querySelector('.ct-tray [data-item="' + mv[0][0] + '"]'), to = board.querySelector('[data-zone="' + mv[0][1] + '"]');
        CT.ghost(from, to, function () { picks[Number(mv[0][1].slice(5))] = mv[0][0]; render(); done(); });
      },
      destroy: function () { dd.destroy(); }
    };
  }

  // ----------------------------------------------------------- sensor game
  function sensorsGame(host, level, api) {
    var d = level.data, phase = "fit", fitted, sort = {}, wrong = {}, scan = {}, bad = {}, running = false, revealed = false;
    var sensorOrder = CT.shuffle(d.sensors.map(function (s) { return s.id; }), CT.rng(level.id + ":s"));
    var mysteryOrder = CT.shuffle(d.mystery.map(function (m) { return m.id; }), CT.rng(level.id + ":m"));
    var board = CT.el("div", { class: "cid cid-sensors" });
    host.appendChild(board);
    function fresh() { fitted = []; for (var i = 0; i < d.budget; i++) fitted.push(null); scan = {}; bad = {}; wrong = {}; }
    function sensor(id) { return CT.byId(d.sensors, id); }
    function cls(id) { return CT.byId(d.classes, id); }
    function chosen() { return fitted.filter(Boolean); }

    function render() {
      CT.clear(board);
      if (phase === "fit") renderFit(); else renderMystery();
    }
    function renderFit() {
      var bot = CT.el("div", { class: "cid-bot" });
      bot.insertAdjacentHTML("beforeend", scanner());
      var sockets = CT.el("div", { class: "cid-sockets" }, [CT.el("p", { class: "ct-tray-h" }, "Sensor sockets (" + d.budget + ")")]);
      fitted.forEach(function (id, i) {
        var z = CT.el("div", { class: "cid-slot ct-zone" + (id ? " is-full" : ""), "data-zone": "slot-" + i, "data-zone-label": "sensor socket " + (i + 1) });
        if (id) { var c = CT.card(sensor(id)); if (wrong[id]) c.classList.add("is-wrong"); z.appendChild(c); }
        else z.appendChild(CT.el("span", { class: "ctr-empty" }, "Socket " + (i + 1)));
        z.appendChild(CT.el("button", { type: "button", class: "ct-drop", "aria-label": "Fit the picked sensor in socket " + (i + 1) }, "Put here"));
        sockets.appendChild(z);
      });
      bot.appendChild(sockets);
      var tray = CT.el("div", { class: "ct-tray", "data-zone": "tray", "data-zone-label": "the sensor box" }, [CT.el("p", { class: "ct-tray-h" }, "Sensor box")]);
      sensorOrder.filter(function (id) { return fitted.indexOf(id) < 0; }).forEach(function (id) { tray.appendChild(CT.card(sensor(id))); });
      var belt = CT.el("div", { class: "cid-belt", role: "list", "aria-label": "Items on the belt" });
      d.items.forEach(function (it) {
        var c = cls(it.cls);
        var li = CT.el("div", { class: "cid-item" + (scan[it.id] ? " is-" + scan[it.id] : "") + (bad[it.id] ? " is-bad" : ""), role: "listitem" }, [
          CT.el("span", { class: "cid-item-i", "aria-hidden": "true" }, CT.ico(it.icon)),
          CT.el("b", null, it.text),
          CT.el("span", { class: "cid-bin cid-bin-" + it.cls }, c.text)
        ]);
        if (scan[it.id]) li.appendChild(CT.readings(chosen().map(function (s) { return [sensor(s).icon, sensor(s).text, it.r[s]]; })));
        belt.appendChild(li);
      });
      CT.append(board, [CT.el("div", { class: "cid-top" }, [bot, tray]),
        CT.el("p", { class: "ct-tray-h cid-belt-h" }, "The robot must put each item in the right bin"), belt]);
    }
    function renderMystery() {
      var tray = CT.el("div", { class: "ct-tray", "data-zone": "tray", "data-zone-label": "the mystery items" }, [CT.el("p", { class: "ct-tray-h" }, "Mystery items: only the readings are known")]);
      function mcard(m) {
        var c = CT.card({ id: m.id, icon: revealed ? "tick" : "question", text: m.label + (revealed ? ": " + m.reveal : "") });
        c.classList.add("cid-mcard");
        c.appendChild(CT.readings(chosen().map(function (s) { return [sensor(s).icon, sensor(s).text, m.r[s]]; })));
        if (wrong[m.id]) c.classList.add("is-wrong");
        return c;
      }
      mysteryOrder.filter(function (id) { return !sort[id]; }).forEach(function (id) { tray.appendChild(mcard(CT.byId(d.mystery, id))); });
      var bins = CT.el("div", { class: "cg-zones cid-bins" });
      d.classes.forEach(function (c) {
        var inBin = mysteryOrder.filter(function (id) { return sort[id] === c.id; });
        var box = CT.el("div", { class: "cg-zone", "data-zone": "bin-" + c.id, "data-zone-label": "the " + c.text + " bin" }, [
          CT.el("div", { class: "cg-zone-h" }, [CT.el("span", { class: "cg-zone-i", "aria-hidden": "true" }, CT.ico(c.icon)), CT.el("b", null, c.text),
            CT.el("span", { class: "cg-count" }, String(inBin.length))]),
          CT.el("button", { type: "button", class: "ct-drop", "aria-label": "Put the picked item in the " + c.text + " bin" }, "Put here")]);
        inBin.forEach(function (id) { box.appendChild(mcard(CT.byId(d.mystery, id))); });
        bins.appendChild(box);
      });
      CT.append(board, [CT.el("p", { class: "ct-round" }, "Round 2 of 2: be the detective"), tray, bins]);
    }

    var dd = CT.dnd(board, {
      canDrop: function () { return !running; },
      onMove: function (id, zone) {
        wrong = {};
        if (phase === "fit") {
          var from = fitted.indexOf(id);
          if (zone === "tray") { if (from >= 0) fitted[from] = null; }
          else { var to = Number(zone.slice(5)), there = fitted[to]; if (from >= 0) fitted[from] = there; fitted[to] = id; }
          scan = {}; bad = {};
        } else {
          if (zone === "tray") delete sort[id]; else sort[id] = zone.slice(4);
        }
        render();
      }
    });
    fresh(); render();

    function startMystery() { phase = "mystery"; wrong = {}; api.label("Check the bins"); render(); api.say("Now you are the detective. Use the readings to sort the mystery items.", "think", 3200); }

    return {
      checkLabel: "Run the robot",
      run: function (done) {
        if (phase === "mystery") {
          var m = mysteryRound(d, sort);
          if (m.ok) { revealed = true; render(); }
          done(m);
          return;
        }
        var r = sensorRound(d, fitted);
        if (r.incomplete || (!r.ok && !r.pair)) { done(r); return; }
        running = true; api.busy(true); scan = {}; bad = {};
        var k = 0;
        (function step() {
          if (!api.alive()) return;
          var it = d.items[k];
          if (!it || (r.pair && bad[r.pair[1]])) {
            running = false; api.busy(false);
            if (r.ok) { CT.sound.play("good"); done(CT.nextRound(api, 0, 2, startMystery)); }
            else done(r);
            return;
          }
          scan[it.id] = "done";
          if (r.pair && it.id === r.pair[1]) { bad[r.pair[0]] = true; bad[r.pair[1]] = true; CT.sound.play("bad"); }
          else CT.sound.play("step");
          render();
          k++;
          CT.wait(420, step);
        })();
      },
      mark: function (r) { wrong = {}; (r.wrong || []).forEach(function (id) { wrong[id] = true; }); render(); },
      reset: function () { if (phase === "fit") fresh(); else { sort = {}; wrong = {}; } render(); },
      showMe: function () {
        var sol = CT.solve.identify(d);
        if (phase === "fit") { fitted = sol.sensors.slice(); scan = {}; bad = {}; }
        else sort = Object.assign({}, sol.sort);
        wrong = {}; render();
      },
      scaffold: function () {
        var sol = CT.solve.identify(d);
        if (phase === "fit") {
          var need = sol.sensors.filter(function (s) { return fitted.indexOf(s) < 0; })[0];
          if (!need) return;
          var at = fitted.indexOf(null);
          if (at < 0) at = fitted.findIndex(function (s) { return sol.sensors.indexOf(s) < 0; });
          fitted[at] = need; scan = {}; bad = {}; render();
          CT.announce("Pixel fitted the " + sensor(need).text + ".");
        } else {
          var m = d.mystery.filter(function (x) { return sort[x.id] !== x.cls; })[0];
          if (m) { sort[m.id] = m.cls; render(); CT.announce("Pixel sorted " + m.label + "."); }
        }
      },
      destroy: function () { dd.destroy(); }
    };
  }
})(typeof window !== "undefined" ? window : globalThis);
