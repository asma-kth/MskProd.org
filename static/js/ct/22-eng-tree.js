/* Engine: tree. Build a structure diagram: the problem at the top, its
 * sub-problems below it, and the small tasks under each sub-problem.
 *
 * data: { root, heads: [{id, text, icon, given}], ordered, orderWhy,
 *         pool: [{id, text, icon, kind: "head"|"leaf", parent: headId|null, why}],
 *         roles: {prompt, cards: [{id, text, icon}], answer: {headId: roleId}} (optional),
 *         mission: {stages...} (optional: the plan is tested by flying it) }
 * Given heads are already in their boxes; the rest come from the pool, which
 * also holds decoys that belong nowhere. Every non-decoy leaf must be placed.
 * answer: { slots: [headId|null], place: {leafId: headId}, roles: {headId: roleId} }
 */
(function (root) {
  "use strict";
  var CT = root.CT = root.CT || {};

  function headIds(d) { return d.heads.map(function (h) { return h.id; }); }
  function find(d, id) { return CT.byId(d.heads, id) || CT.byId(d.pool, id) || (d.roles ? CT.byId(d.roles.cards, id) : null); }

  CT.check.tree = function (d, a) {
    a = a || {};
    var slots = a.slots || [], place = a.place || {};
    var empty = slots.filter(function (s) { return !s; }).length + Math.max(0, d.heads.length - slots.length);
    var wrongHead = slots.filter(function (s) { return s && headIds(d).indexOf(s) < 0; });
    if (wrongHead.length) {
      var h = find(d, wrongHead[0]);
      return { ok: false, wrong: wrongHead, stage: slots.indexOf(wrongHead[0]), msg: (h && h.why) || "That is not one of the sub-problems." };
    }
    if (empty) return { ok: false, incomplete: true, msg: "Fill every sub-problem box first." };
    if (d.ordered) {
      for (var i = 0; i < d.heads.length; i++) {
        if (slots[i] !== d.heads[i].id) return { ok: false, wrong: [slots[i]], stage: i, msg: d.orderWhy || "The sub-problems are in the wrong order." };
      }
    }
    var wrong = [], missing = 0, firstWhy = "", stage = -1;
    d.pool.forEach(function (it) {
      if (it.kind !== "leaf") return;
      var at = place[it.id];
      if (it.parent === null) {
        if (at) { wrong.push(it.id); if (!firstWhy) { firstWhy = it.why; stage = slots.indexOf(at); } }
      } else if (!at) missing++;
      else if (at !== it.parent) { wrong.push(it.id); if (!firstWhy) { firstWhy = it.why; stage = slots.indexOf(it.parent); } }
    });
    if (wrong.length) return { ok: false, wrong: wrong, stage: stage, msg: (wrong.length > 1 ? wrong.length + " task cards are in the wrong place. " : "") + firstWhy };
    if (missing) {
      var miss = d.pool.filter(function (it) { return it.kind === "leaf" && it.parent && !place[it.id]; })[0];
      return { ok: false, incomplete: true, stage: slots.indexOf(miss.parent), msg: missing + " task card" + (missing > 1 ? "s" : "") + " still to place." };
    }
    if (d.roles) {
      var roles = a.roles || {};
      var unassigned = d.heads.filter(function (h) { return !roles[h.id]; });
      if (unassigned.length) return { ok: false, incomplete: true, needRoles: true, msg: d.roles.prompt };
      var bad = d.heads.filter(function (h) { return roles[h.id] !== d.roles.answer[h.id]; });
      if (bad.length) {
        var role = CT.byId(d.roles.cards, roles[bad[0].id]);
        return { ok: false, wrong: bad.map(function (h) { return roles[h.id]; }), msg: (role && role.why) || "One person is matched to the wrong part." };
      }
    }
    return { ok: true };
  };
  CT.solve.tree = function (d) {
    var place = {}, roles = {};
    d.pool.forEach(function (it) { if (it.kind === "leaf" && it.parent) place[it.id] = it.parent; });
    if (d.roles) Object.keys(d.roles.answer).forEach(function (h) { roles[h] = d.roles.answer[h]; });
    return { slots: headIds(d), place: place, roles: roles };
  };

  CT.engines.tree = {
    mount: function (host, level, api) {
      var d = level.data, st, wrong = {}, showRoles = false;
      var order = CT.shuffle(d.pool.map(function (x) { return x.id; }), api.rng);
      var roleOrder = d.roles ? CT.shuffle(d.roles.cards.map(function (x) { return x.id; }), CT.rng(level.id + ":r")) : [];
      var board = CT.el("div", { class: "ctr" });
      host.appendChild(board);

      function fresh() {
        st = { slots: d.heads.map(function (h) { return h.given ? h.id : null; }), place: {}, roles: {} };
        wrong = {}; showRoles = false;
      }
      function given(id) { var h = CT.byId(d.heads, id); return !!(h && h.given); }

      function render() {
        CT.clear(board);
        if (d.mission) board.appendChild(missionStrip());
        var tray = CT.el("div", { class: "ct-tray", "data-zone": "tray", "data-zone-label": "the card pile" }, [CT.el("p", { class: "ct-tray-h" }, "Cards")]);
        var unused = order.filter(function (id) { return st.slots.indexOf(id) < 0 && !st.place[id]; });
        unused.forEach(function (id) {
          var it = CT.byId(d.pool, id);
          var c = CT.card(it);
          c.classList.add(it.kind === "head" ? "is-head" : "is-leaf");
          if (wrong[id]) c.classList.add("is-wrong");
          tray.appendChild(c);
        });
        if (!unused.length) tray.appendChild(CT.el("p", { class: "ct-tray-empty" }, "No cards left."));
        board.appendChild(tray);

        var dia = CT.el("div", { class: "ctr-dia" }, [CT.el("div", { class: "ctr-root" }, [CT.el("span", { class: "ctr-k" }, "Problem"), d.root])]);
        var cols = CT.el("div", { class: "ctr-cols ctr-n" + st.slots.length });
        st.slots.forEach(function (hid, i) {
          var col = CT.el("div", { class: "ctr-col" });
          var head = CT.el("div", { class: "ctr-head" + (hid ? " is-full" : "") + (hid && given(hid) ? " is-given" : ""),
            "data-zone": given(hid) ? null : "slot-" + i, "data-zone-label": "sub-problem box " + (i + 1) });
          if (hid) {
            var hd = find(d, hid);
            if (given(hid)) head.appendChild(CT.el("div", { class: "ctr-headtxt" }, [hd.icon ? CT.ico(hd.icon) : null, " ", hd.text]));
            else { var hc = CT.card(hd); hc.classList.add("is-head"); if (wrong[hid]) hc.classList.add("is-wrong"); head.appendChild(hc); }
          } else {
            head.appendChild(CT.el("span", { class: "ctr-empty" }, "Sub-problem " + (i + 1)));
            head.appendChild(CT.el("button", { type: "button", class: "ct-drop", "aria-label": "Put the picked card in sub-problem box " + (i + 1) }, "Put here"));
          }
          col.appendChild(head);
          var under = CT.el("div", { class: "ctr-under ct-zone" + (hid ? "" : " is-off"), "data-zone": hid ? "under-" + i : null,
            "data-zone-label": hid ? "tasks under " + find(d, hid).text : null });
          if (hid) {
            Object.keys(st.place).filter(function (k) { return st.place[k] === hid; }).sort(function (a, b) { return order.indexOf(a) - order.indexOf(b); }).forEach(function (lid) {
              var lc = CT.card(CT.byId(d.pool, lid)); lc.classList.add("is-leaf");
              if (wrong[lid]) lc.classList.add("is-wrong");
              under.appendChild(lc);
            });
            under.appendChild(CT.el("button", { type: "button", class: "ct-drop", "aria-label": "Put the picked card under " + find(d, hid).text }, "Put here"));
          } else under.appendChild(CT.el("span", { class: "ctr-wait" }, "Tasks go here once the box above is filled."));
          col.appendChild(under);
          if (showRoles && hid) {
            var rz = CT.el("div", { class: "ctr-role ct-zone", "data-zone": "role-" + i, "data-zone-label": "who builds " + find(d, hid).text });
            var rid = st.roles[hid];
            if (rid) { var rc = CT.card(CT.byId(d.roles.cards, rid)); rc.classList.add("is-role"); if (wrong[rid]) rc.classList.add("is-wrong"); rz.appendChild(rc); }
            else rz.appendChild(CT.el("span", { class: "ctr-wait" }, "Who builds this?"));
            rz.appendChild(CT.el("button", { type: "button", class: "ct-drop", "aria-label": "Put the picked person on " + find(d, hid).text }, "Put here"));
            col.appendChild(rz);
          }
          cols.appendChild(col);
        });
        dia.appendChild(cols);
        board.appendChild(dia);
        if (showRoles) {
          var rt = CT.el("div", { class: "ct-tray ctr-roles", "data-zone": "rtray", "data-zone-label": "the team" }, [CT.el("p", { class: "ct-tray-h" }, d.roles.prompt)]);
          roleOrder.filter(function (id) { return !Object.keys(st.roles).some(function (h) { return st.roles[h] === id; }); }).forEach(function (id) {
            var c = CT.card(CT.byId(d.roles.cards, id)); c.classList.add("is-role"); rt.appendChild(c);
          });
          board.appendChild(rt);
        }
      }

      function kindOf(id) {
        if (d.roles && CT.byId(d.roles.cards, id)) return "role";
        var it = CT.byId(d.pool, id);
        return it ? it.kind : "head";
      }
      var dd = CT.dnd(board, {
        canDrop: function (id, zone) {
          var k = kindOf(id);
          if (zone === "tray") return k !== "role";
          if (zone === "rtray") return k === "role";
          if (zone.indexOf("slot-") === 0) return k === "head";
          if (zone.indexOf("under-") === 0) return k === "leaf";
          if (zone.indexOf("role-") === 0) return k === "role";
          return false;
        },
        onMove: function (id, zone) {
          var k = kindOf(id);
          wrong = {};
          if (k === "role") {
            Object.keys(st.roles).forEach(function (h) { if (st.roles[h] === id) delete st.roles[h]; });
            if (zone.indexOf("role-") === 0) { var hh = st.slots[Number(zone.slice(5))]; st.roles[hh] = id; }
          } else if (k === "head") {
            var from = st.slots.indexOf(id);
            if (zone === "tray") {
              if (from >= 0) {
                st.slots[from] = null;
                Object.keys(st.place).forEach(function (l) { if (st.place[l] === id) delete st.place[l]; });
                delete st.roles[id];
              }
            } else {
              var to = Number(zone.slice(5)), there = st.slots[to];
              if (there && given(there)) return;
              if (from >= 0) st.slots[from] = there;  // swap boxes, tasks travel with their heads
              else if (there) Object.keys(st.place).forEach(function (l) { if (st.place[l] === there) delete st.place[l]; });
              st.slots[to] = id;
            }
          } else {
            if (zone === "tray") delete st.place[id];
            else st.place[id] = st.slots[Number(zone.slice(6))];
          }
          render();
        }
      });

      // ------------------------------------------------------- mission
      var strip = null;
      function missionStrip() {
        strip = CT.el("div", { class: "ctr-mission", "aria-hidden": "true" });
        var lane = CT.el("div", { class: "ctr-lane" });
        st.slots.forEach(function (hid, i) {
          var hd = hid ? find(d, hid) : null;
          lane.appendChild(CT.el("div", { class: "ctr-stage" }, [CT.el("span", { class: "ctr-stage-i" }, CT.ico(hd && hd.icon ? hd.icon : "question")),
            CT.el("small", null, hd ? hd.text : "Stage " + (i + 1))]));
        });
        lane.appendChild(CT.el("div", { class: "ctr-rocket" }, CT.ico("rocket")));
        strip.appendChild(lane);
        return strip;
      }
      function fly(res, done) {
        var rocket = strip && strip.querySelector(".ctr-rocket");
        var stages = strip ? strip.querySelectorAll(".ctr-stage") : [];
        var stop = res.ok ? stages.length : Math.max(0, res.stage === undefined || res.stage < 0 ? 0 : res.stage);
        var i = 0;
        api.busy(true);
        function step() {
          if (!api.alive()) return;
          if (i >= stages.length || i > stop || !rocket) {
            api.busy(false);
            if (!res.ok && stages[stop]) stages[stop].classList.add("is-fail");
            done(res.ok ? res : Object.assign({}, res, { msg: "Mission failed at stage " + (stop + 1) + ". " + res.msg }));
            return;
          }
          var s = stages[i];
          rocket.style.left = (s.offsetLeft + s.offsetWidth / 2 - 18) + "px";
          if (i < stop || res.ok) s.classList.add("is-ok");
          CT.sound.play("step");
          i++;
          CT.wait(650, step);
        }
        step();
      }

      fresh();
      render();
      var ctl = {
        answer: function () { return st; },
        check: d.mission ? null : function () {
          var r = CT.check.tree(d, st);
          if (r.needRoles && !showRoles) { showRoles = true; render(); r.msg = "Your diagram is right! " + d.roles.prompt; }
          return r;
        },
        mark: function (r) { wrong = {}; (r.wrong || []).forEach(function (id) { wrong[id] = true; }); render(); },
        reset: function () { fresh(); render(); },
        showMe: function () { st = CT.solve.tree(d); if (d.roles) showRoles = true; wrong = {}; render(); },
        scaffold: function () {
          var sol = CT.solve.tree(d);
          for (var i = 0; i < sol.slots.length; i++) {
            if (st.slots[i] !== sol.slots[i]) {
              var prev = st.slots.indexOf(sol.slots[i]);
              if (prev >= 0) st.slots[prev] = null;
              st.slots[i] = sol.slots[i]; render();
              CT.announce("Pixel placed " + find(d, sol.slots[i]).text + "."); return;
            }
          }
          var leaf = d.pool.filter(function (it) { return it.kind === "leaf" && it.parent && st.place[it.id] !== it.parent; })[0];
          if (leaf) { st.place[leaf.id] = leaf.parent; render(); CT.announce("Pixel placed " + leaf.text + "."); }
        },
        demo: function (done) {
          var mv = (level.watch && level.watch.moves) || [];
          var k = 0;
          (function next() {
            if (k >= mv.length) { done(); return; }
            var m = mv[k++], from = board.querySelector('.ct-tray [data-item="' + m[0] + '"]');
            var to = board.querySelector('[data-zone="' + m[1] + '"]');
            CT.ghost(from, to, function () {
              if (m[1].indexOf("slot-") === 0) st.slots[Number(m[1].slice(5))] = m[0];
              else st.place[m[0]] = st.slots[Number(m[1].slice(6))];
              render(); setTimeout(next, 150);
            });
          })();
        },
        destroy: function () { dd.destroy(); }
      };
      if (d.mission) {
        ctl.checkLabel = "Launch mission";
        ctl.run = function (done) {
          var r = CT.check.tree(d, st);
          if (r.incomplete) { done(r); return; }
          render();
          fly(r, done);
        };
      }
      return ctl;
    }
  };
})(typeof window !== "undefined" ? window : globalThis);
