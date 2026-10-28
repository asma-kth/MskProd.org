/* Engine: select. Keep or remove each detail for the job in hand.
 *
 * data: { details: [{id, text, icon}], picture: name,          (shared by every round)
 *         rounds: [{purpose, icon, keep: [ids], missing, extra,
 *                   scene, look: "map"|"icon", layers: [{id, text, icon, keep, why}]}],
 *         followup: {q, options, answer, why} }                   (all optional but rounds)
 * A round either lists its own layers, each saying whether it stays and why,
 * or uses the shared details with a keep list. Pictures lose every detail the
 * student removes; an icon shows live previews at app-icon sizes, and a map
 * turns into a clean drawn map once it is right.
 * answer: { rounds: [{detailId: "keep"|"bin"} per round], follow: option index }
 */
(function (root) {
  "use strict";
  var CT = root.CT = root.CT || {};

  function items(d, rd) { return rd.layers || d.details; }
  function keeps(d, rd) {
    return rd.layers ? rd.layers.filter(function (l) { return l.keep; }).map(function (l) { return l.id; }) : rd.keep;
  }

  function checkRound(d, rd, ans) {
    ans = ans || {};
    var list = items(d, rd), keep = keeps(d, rd);
    var left = list.filter(function (x) { return !ans[x.id]; });
    if (left.length) return { ok: false, incomplete: true, msg: "Sort every detail first: " + left.length + " still to go." };
    var missing = list.filter(function (x) { return keep.indexOf(x.id) >= 0 && ans[x.id] !== "keep"; });
    var extra = list.filter(function (x) { return keep.indexOf(x.id) < 0 && ans[x.id] === "keep"; });
    if (!missing.length && !extra.length) return { ok: true };
    var first = extra[0] || missing[0];
    var why = first.why || (extra.length ? rd.extra : rd.missing);
    var n = missing.length + extra.length;
    return { ok: false, wrong: extra.concat(missing).map(function (x) { return x.id; }),
             msg: (n > 1 ? n + " details are in the wrong box. " : "One detail is in the wrong box. ") + why };
  }

  CT.check.select = function (d, a) {
    a = a || {};
    for (var i = 0; i < d.rounds.length; i++) {
      var r = checkRound(d, d.rounds[i], (a.rounds || [])[i]);
      if (!r.ok) return Object.assign(r, { round: i });
    }
    if (d.followup && a.follow !== d.followup.answer) {
      if (a.follow === undefined || a.follow === null) return { ok: false, incomplete: true, needFollow: true, msg: "Now answer Pixel's question." };
      return { ok: false, msg: d.followup.why };
    }
    return { ok: true };
  };
  CT.solve.select = function (d) {
    var out = { rounds: d.rounds.map(function (rd) {
      var a = {}, keep = keeps(d, rd);
      items(d, rd).forEach(function (x) { a[x.id] = keep.indexOf(x.id) >= 0 ? "keep" : "bin"; });
      return a;
    }) };
    if (d.followup) out.follow = d.followup.answer;
    return out;
  };

  CT.engines.select = {
    mount: function (host, level, api) {
      var d = level.data, ri = 0, rd, ans = {}, wrong = {}, follow = null, showFollow = false, solved = false;
      var board = CT.el("div", { class: "csel" });
      var top = CT.el("div"), picBox = CT.el("div", { class: "csel-pic" }), cards = CT.el("div"), after = CT.el("div");
      CT.append(board, [top, picBox, cards, after]);
      host.appendChild(board);
      var order;

      function start(i) {
        ri = i; rd = d.rounds[ri]; ans = {}; wrong = {}; solved = false;
        order = CT.shuffle(items(d, rd).map(function (x) { return x.id; }), CT.rng(level.id + ":" + ri));
        CT.clear(top);
        CT.append(top, [CT.roundChip(ri, d.rounds.length),
          CT.el("div", { class: "ct-problem csel-job" }, [CT.el("span", { class: "ct-problem-k" }, "The job"),
            CT.el("span", { class: "csel-job-i", "aria-hidden": "true" }, CT.ico(rd.icon || "target")), rd.purpose])]);
        drawPicture();
        render();
        if (i > 0) api.say("New job: " + rd.purpose, "think", 2600);
      }

      function drawPicture() {
        CT.clear(picBox);
        var name = rd.scene || d.picture;
        picBox.className = "csel-pic" + (rd.look ? " is-" + rd.look : "");
        if (!name || !CT.pics[name]) { picBox.hidden = true; return; }
        picBox.hidden = false;
        var big = CT.el("div", { class: "csel-big" });
        big.innerHTML = CT.pics[name]();
        picBox.appendChild(big);
        if (rd.look === "icon") {
          var row = CT.el("div", { class: "csel-sizes", "aria-label": "Previews at app-icon sizes" });
          [64, 32, 16].forEach(function (px) {
            var f = CT.el("figure", { class: "csel-size" });
            var tile = CT.el("div", { class: "csel-tile", style: { width: px + "px", height: px + "px" } });
            tile.innerHTML = CT.pics[name]();
            var svg = tile.querySelector("svg");
            if (svg) { svg.setAttribute("aria-hidden", "true"); svg.removeAttribute("role"); }
            CT.append(f, [tile, CT.el("figcaption", null, px + " px")]);
            row.appendChild(f);
          });
          picBox.appendChild(row);
        }
        if (rd.look === "map") picBox.appendChild(CT.el("p", { class: "csel-note" }, "Removed layers fade out. Get it right and the picture becomes a map."));
      }

      function paintPicture() {
        Array.prototype.forEach.call(picBox.querySelectorAll("[data-d]"), function (g) {
          var id = g.getAttribute("data-d");
          g.classList.toggle("is-gone", ans[id] === "bin");
          g.classList.toggle("is-kept", ans[id] === "keep");
        });
        picBox.classList.toggle("is-done", solved);
      }

      function render() {
        CT.clear(cards);
        var tray = CT.el("div", { class: "ct-tray", "data-zone": "tray", "data-zone-label": "the details still to sort" }, [CT.el("p", { class: "ct-tray-h" }, "Details to sort")]);
        var waiting = order.filter(function (id) { return !ans[id]; });
        waiting.forEach(function (id) { tray.appendChild(CT.card(CT.byId(items(d, rd), id))); });
        if (!waiting.length) tray.appendChild(CT.el("p", { class: "ct-tray-empty" }, "All sorted! Press Check."));
        cards.appendChild(tray);
        var zones = CT.el("div", { class: "cg-zones cg-n2" });
        [["keep", "tick", "Keep: the job needs it"], ["bin", "bin", "Remove: not needed"]].forEach(function (z) {
          var inZone = order.filter(function (id) { return ans[id] === z[0]; });
          var box = CT.el("div", { class: "cg-zone csel-" + z[0], "data-zone": z[0], "data-zone-label": z[2] }, [
            CT.el("div", { class: "cg-zone-h" }, [CT.el("span", { class: "cg-zone-i", "aria-hidden": "true" }, CT.ico(z[1])), CT.el("b", null, z[2]),
              CT.el("span", { class: "cg-count" }, String(inZone.length))]),
            CT.el("button", { type: "button", class: "ct-drop", "aria-label": "Put the picked card in " + z[2] }, "Put here")
          ]);
          inZone.forEach(function (id) {
            var c = CT.card(CT.byId(items(d, rd), id));
            if (wrong[id]) c.classList.add("is-wrong");
            box.appendChild(c);
          });
          zones.appendChild(box);
        });
        cards.appendChild(zones);
        CT.clear(after);
        if (showFollow && d.followup) after.appendChild(CT.followBox(d.followup, follow, level.id + ":f", function (i) {
          follow = i; render();
          api.result(i === d.followup.answer ? { ok: true } : { ok: false, msg: d.followup.why });
        }));
        paintPicture();
      }

      var dd = CT.dnd(board, {
        onMove: function (id, zone) {
          if (solved) return;
          if (zone === "tray") delete ans[id]; else ans[id] = zone;
          delete wrong[id];
          render();
        }
      });
      start(0);

      function place(moves, done, k) {
        k = k || 0;
        if (k >= moves.length) { if (done) done(); return; }
        var m = moves[k], from = board.querySelector('.ct-tray [data-item="' + m[0] + '"]'), to = board.querySelector('[data-zone="' + m[1] + '"]');
        CT.ghost(from, to, function () { ans[m[0]] = m[1]; render(); setTimeout(function () { place(moves, done, k + 1); }, 120); });
      }

      return {
        check: function () {
          if (solved && showFollow) {
            if (follow === d.followup.answer) return { ok: true };
            return follow === null ? { ok: false, incomplete: true, msg: "Now answer Pixel's question." } : { ok: false, msg: d.followup.why };
          }
          var r = checkRound(d, rd, ans);
          if (!r.ok) return r;
          solved = true;
          paintPicture();
          if (ri < d.rounds.length - 1) return CT.nextRound(api, ri, d.rounds.length, start);
          if (d.followup) {
            showFollow = true; render();
            return { ok: false, incomplete: true, msg: "Spot on! Now answer Pixel's question." };
          }
          return r;
        },
        mark: function (r) { wrong = {}; (r.wrong || []).forEach(function (id) { wrong[id] = true; }); render(); },
        reset: function () { follow = null; showFollow = false; start(ri); },
        showMe: function () {
          ans = CT.solve.select(d).rounds[ri]; wrong = {};
          if (showFollow) follow = d.followup.answer;
          render();
        },
        scaffold: function () {
          var keep = keeps(d, rd);
          var it = items(d, rd).filter(function (x) { return ans[x.id] !== (keep.indexOf(x.id) >= 0 ? "keep" : "bin"); })[0];
          if (it) place([[it.id, keep.indexOf(it.id) >= 0 ? "keep" : "bin"]]);
        },
        demo: function (done) { place((level.watch && level.watch.moves) || [], done); },
        destroy: function () { dd.destroy(); }
      };
    }
  };
})(typeof window !== "undefined" ? window : globalThis);
