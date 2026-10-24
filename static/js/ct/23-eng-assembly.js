/* Engine: assembly. A production line: put the stations in order, give each
 * station its jobs, then run the line and watch the car being built.
 *
 * data: { stations: [{id, name, icon}], order: [ids], orderWhy,
 *         tasks: [{id, text, icon, station, why}] }
 * answer: { line: [stationId|null], tasks: {taskId: stationId} }
 */
(function (root) {
  "use strict";
  var CT = root.CT = root.CT || {};

  CT.check.assembly = function (d, a) {
    a = a || {};
    var line = a.line || [], tasks = a.tasks || {};
    if (line.filter(Boolean).length < d.order.length) return { ok: false, incomplete: true, msg: "Put a station in every place on the line first." };
    for (var i = 0; i < d.order.length; i++) {
      if (line[i] !== d.order[i]) return { ok: false, wrong: [line[i]], stage: i, msg: d.orderWhy };
    }
    var left = d.tasks.filter(function (t) { return !tasks[t.id]; });
    if (left.length) return { ok: false, incomplete: true, msg: "Give every job to a station: " + left.length + " still to place." };
    for (var j = 0; j < d.order.length; j++) {
      var bad = d.tasks.filter(function (t) { return (t.station === d.order[j]) !== (tasks[t.id] === d.order[j]); });
      if (bad.length) {
        var wrongOnes = d.tasks.filter(function (t) { return tasks[t.id] !== t.station; });
        var first = wrongOnes.filter(function (t) { return tasks[t.id] === d.order[j] || t.station === d.order[j]; })[0] || wrongOnes[0];
        return { ok: false, wrong: wrongOnes.map(function (t) { return t.id; }), stage: j, msg: first.why };
      }
    }
    return { ok: true };
  };
  CT.solve.assembly = function (d) {
    var t = {};
    d.tasks.forEach(function (x) { t[x.id] = x.station; });
    return { line: d.order.slice(), tasks: t };
  };

  // The car, drawn in stages: chassis, body, paint, wheels, checked.
  function carSvg(stage, ok) {
    var paint = stage >= 2 ? "#DC2626" : "#94A3B8";
    var s = '<svg viewBox="0 0 120 64" class="cas-car' + (ok === false ? " is-broken" : "") + '" aria-hidden="true">';
    s += '<rect x="10" y="38" width="100" height="8" rx="3" fill="#334155"/>';
    if (stage >= 1) s += '<path d="M14 40 q2 -16 22 -18 l12 -12 h30 l14 12 q16 2 18 18 z" fill="' + paint + '" stroke="#1F2937" stroke-width="2"/>' +
      '<path d="M50 14 h26 l10 10 h-40 z" fill="#BFDBFE" stroke="#1F2937" stroke-width="1.5"/>';
    if (stage >= 3) s += '<circle cx="34" cy="48" r="10" fill="#111827"/><circle cx="34" cy="48" r="4" fill="#CBD5E1"/>' +
      '<circle cx="88" cy="48" r="10" fill="#111827"/><circle cx="88" cy="48" r="4" fill="#CBD5E1"/>';
    if (stage >= 4) s += '<path d="M98 6 l4 8 l9 1 l-7 6 l2 9 l-8 -5 l-8 5 l2 -9 l-7 -6 l9 -1 z" fill="#F5B700"/>';
    if (ok === false) s += '<path d="M50 20 l20 20 M70 20 l-20 20" stroke="#DC2626" stroke-width="6" stroke-linecap="round"/>';
    return s + '</svg>';
  }

  CT.engines.assembly = {
    mount: function (host, level, api) {
      var d = level.data, st, wrong = {};
      var sOrder = CT.scramble(d.stations.map(function (s) { return s.id; }), CT.rng(level.id + ":s"));
      var tOrder = CT.shuffle(d.tasks.map(function (t) { return t.id; }), api.rng);
      var board = CT.el("div", { class: "cas" });
      host.appendChild(board);
      function fresh() { st = { line: d.order.map(function () { return null; }), tasks: {} }; wrong = {}; }
      function isStation(id) { return !!CT.byId(d.stations, id); }

      function render(carAt, carStage, broken) {
        CT.clear(board);
        var tray = CT.el("div", { class: "ct-tray", "data-zone": "tray", "data-zone-label": "the parts tray" }, [CT.el("p", { class: "ct-tray-h" }, "Stations and jobs")]);
        sOrder.filter(function (id) { return st.line.indexOf(id) < 0; }).forEach(function (id) {
          var c = CT.card({ id: id, text: CT.byId(d.stations, id).name, icon: CT.byId(d.stations, id).icon }); c.classList.add("is-head"); tray.appendChild(c);
        });
        tOrder.filter(function (id) { return !st.tasks[id]; }).forEach(function (id) {
          var c = CT.card(CT.byId(d.tasks, id)); c.classList.add("is-leaf"); if (wrong[id]) c.classList.add("is-wrong"); tray.appendChild(c);
        });
        board.appendChild(tray);
        var line = CT.el("div", { class: "cas-line" });
        st.line.forEach(function (sid, i) {
          var slot = CT.el("div", { class: "cas-st" + (sid ? " is-full" : "") });
          var head = CT.el("div", { class: "cas-head", "data-zone": "line-" + i, "data-zone-label": "place " + (i + 1) + " on the line" }, [CT.el("span", { class: "cas-num" }, String(i + 1))]);
          if (sid) { var sc = CT.card({ id: sid, text: CT.byId(d.stations, sid).name, icon: CT.byId(d.stations, sid).icon }); sc.classList.add("is-head"); if (wrong[sid]) sc.classList.add("is-wrong"); head.appendChild(sc); }
          else head.appendChild(CT.el("span", { class: "ctr-empty" }, "Station " + (i + 1)));
          head.appendChild(CT.el("button", { type: "button", class: "ct-drop", "aria-label": "Put the picked card at place " + (i + 1) }, "Put here"));
          slot.appendChild(head);
          var jobs = CT.el("div", { class: "cas-jobs ct-zone" + (sid ? "" : " is-off"), "data-zone": sid ? "jobs-" + i : null, "data-zone-label": sid ? "jobs at " + CT.byId(d.stations, sid).name : null });
          if (sid) {
            tOrder.filter(function (t) { return st.tasks[t] === sid; }).forEach(function (t) {
              var tc = CT.card(CT.byId(d.tasks, t)); tc.classList.add("is-leaf"); if (wrong[t]) tc.classList.add("is-wrong"); jobs.appendChild(tc);
            });
            jobs.appendChild(CT.el("button", { type: "button", class: "ct-drop", "aria-label": "Give the picked job to " + CT.byId(d.stations, sid).name }, "Put here"));
          } else jobs.appendChild(CT.el("span", { class: "ctr-wait" }, "Jobs go here"));
          slot.appendChild(jobs);
          if (carAt === i) { var cw = CT.el("div", { class: "cas-carpos" }); cw.innerHTML = carSvg(carStage, broken ? false : null); slot.appendChild(cw); }
          line.appendChild(slot);
        });
        board.appendChild(CT.el("div", { class: "cas-belt" }, [line]));
        if (carAt === "out") {
          var out = CT.el("div", { class: "cas-out" }); out.innerHTML = carSvg(4, null);
          out.appendChild(CT.el("p", null, "🎉 A finished car rolls off the line!"));
          board.appendChild(out);
        }
      }

      var dd = CT.dnd(board, {
        canDrop: function (id, zone) {
          if (zone === "tray") return true;
          if (zone.indexOf("line-") === 0) return isStation(id);
          return zone.indexOf("jobs-") === 0 && !isStation(id);
        },
        onMove: function (id, zone) {
          wrong = {};
          if (isStation(id)) {
            var from = st.line.indexOf(id);
            if (zone === "tray") {
              if (from >= 0) { st.line[from] = null; Object.keys(st.tasks).forEach(function (t) { if (st.tasks[t] === id) delete st.tasks[t]; }); }
            } else {
              var to = Number(zone.slice(5)), there = st.line[to];
              if (from >= 0) st.line[from] = there;
              else if (there) Object.keys(st.tasks).forEach(function (t) { if (st.tasks[t] === there) delete st.tasks[t]; });
              st.line[to] = id;
            }
          } else {
            if (zone === "tray") delete st.tasks[id];
            else st.tasks[id] = st.line[Number(zone.slice(5))];
          }
          render();
        }
      });

      fresh(); render();
      return {
        checkLabel: "▶ Run the line",
        run: function (done) {
          var r = CT.check.assembly(d, st);
          if (r.incomplete) { done(r); return; }
          var stop = r.ok ? d.order.length : r.stage;
          var i = 0;
          api.busy(true);
          (function step() {
            if (!api.alive()) return;
            if (i > stop || i >= d.order.length) {
              api.busy(false);
              if (r.ok) { render("out"); CT.sound.play("good"); }
              else { render(stop, stop, true); }
              done(r.ok ? r : Object.assign({}, r, { msg: "The car broke down at station " + (stop + 1) + ". " + r.msg }));
              return;
            }
            render(i, i + 1, false);
            CT.sound.play("step");
            i++;
            CT.wait(700, step);
          })();
        },
        mark: function (r) { wrong = {}; (r.wrong || []).forEach(function (id) { wrong[id] = true; }); render(); },
        reset: function () { fresh(); render(); },
        showMe: function () { st = CT.solve.assembly(d); wrong = {}; render(); },
        scaffold: function () {
          for (var i = 0; i < d.order.length; i++) {
            if (st.line[i] !== d.order[i]) {
              var prev = st.line.indexOf(d.order[i]); if (prev >= 0) st.line[prev] = null;
              st.line[i] = d.order[i]; render(); CT.announce("Pixel placed " + CT.byId(d.stations, d.order[i]).name + "."); return;
            }
          }
          var t = d.tasks.filter(function (x) { return st.tasks[x.id] !== x.station; })[0];
          if (t) { st.tasks[t.id] = t.station; render(); CT.announce("Pixel placed " + t.text + "."); }
        },
        demo: function (done) {
          var id = d.order[0], from = board.querySelector('.ct-tray [data-item="' + id + '"]'), to = board.querySelector('[data-zone="line-0"]');
          CT.ghost(from, to, function () { st.line[0] = id; render(); done(); });
        },
        destroy: function () { dd.destroy(); }
      };
    }
  };
})(typeof window !== "undefined" ? window : globalThis);
