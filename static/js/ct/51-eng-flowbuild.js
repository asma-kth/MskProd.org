/* Engine: flowbuild. Complete a flowchart by dragging steps, with the right
 * symbol, into its numbered boxes; then run it.
 *
 * data: { rounds: [{problem, flow, cards: [{id, t, text, code, slot, why}], tests, sim}] }
 * A node in the flow with a slot is an empty box. Plain boxes take an input,
 * output or process card; decision and loop boxes take a decision card. Some
 * cards are decoys: the right words in the wrong symbol, or a plausible wrong
 * step. Running uses test data, or, for sim "pelican", a crossing simulation
 * with a safety check: the green man must never show unless the lights are red.
 * answer: [{slotId: cardId} per round]
 */
(function (root) {
  "use strict";
  var CT = root.CT = root.CT || {};

  function slotsOf(flow) {
    return CT.flow.nodes(flow).filter(function (n) { return n.slot; }).map(function (n) { return { slot: n.slot, label: n.label, kind: n.t }; });
  }
  function cardOf(rd, id) { return CT.byId(rd.cards, id); }
  function fillMap(rd, ans) {
    var fill = {};
    Object.keys(ans || {}).forEach(function (s) { var c = cardOf(rd, ans[s]); if (c) fill[s] = { t: c.t, text: c.text, code: c.code || c.text }; });
    return fill;
  }
  // The flow with its boxes filled: structure from the template, words from the cards.
  function build(rd, ans) {
    var fill = fillMap(rd, ans);
    return (function walk(list) {
      return (list || []).map(function (n) {
        var c = Object.assign({}, n);
        if (n.slot && fill[n.slot]) {
          c.text = fill[n.slot].text; c.code = fill[n.slot].code;
          if (n.t === "slot") c.t = fill[n.slot].t;
        } else if (n.slot) c.empty = true;
        if (n.yes) c.yes = walk(n.yes);
        if (n.no) c.no = walk(n.no);
        if (n.body) c.body = walk(n.body);
        return c;
      });
    })(rd.flow);
  }
  CT.flowBuild = build;

  // The crossing simulation: a log of what the lights did, and the first problem.
  CT.pelican = function (flow) {
    var st = { lights: "green", man: "red", clock: 0, pressedAt: 4 }, log = [], problem = null;
    var r = CT.flow.run(flow, { maxSteps: 3000, builtins: {
      lights: function (c) { st.lights = c; log.push({ k: "lights", v: c, t: st.clock }); },
      man: function (c) {
        st.man = c; log.push({ k: "man", v: c, t: st.clock });
        if (c === "green" && st.lights !== "red") { problem = "Danger! The green man came on while the traffic lights were " + st.lights + "."; return { ctError: problem }; }
      },
      wait: function (n) { st.clock += n; log.push({ k: "wait", v: n, t: st.clock }); },
      pressed: function () { var p = st.clock >= st.pressedAt; if (p) log.push({ k: "press", t: st.clock }); return p; }
    } });
    if (!problem && r.error) problem = /too long/.test(r.error.msg) ? "The crossing got stuck in a loop and never let anyone cross." : r.error.msg;
    if (!problem) {
      var seq = log.filter(function (e) { return e.k === "lights" || e.k === "man"; }).map(function (e) { return e.k + " " + e.v; });
      var firstChange = log.filter(function (e) { return e.k === "lights" && e.v !== "green"; })[0];
      if (firstChange && firstChange.t < st.pressedAt) problem = "The lights changed before anyone pressed the button.";
      else if (seq.indexOf("lights amber") < 0) problem = "The cars never got an amber warning before the red light.";
      else if (seq.indexOf("lights red") < 0) problem = "The traffic lights never turned red, so nobody could cross safely.";
      else if (seq.indexOf("lights red") < seq.indexOf("lights amber")) problem = "Cars need an amber warning before the red light.";
      else if (seq.indexOf("man green") < 0) problem = "The green man never came on, so nobody could cross.";
      else if (seq[seq.length - 1] !== "man red") problem = "The man must go back to red when the crossing time is over.";
    }
    return { ok: !problem, log: log, problem: problem, output: r.output };
  };

  function checkRound(rd, ans) {
    ans = ans || {};
    var slots = slotsOf(rd.flow);
    var left = slots.filter(function (s) { return !ans[s.slot]; }).length;
    if (left) return { ok: false, incomplete: true, msg: "Fill every numbered box first: " + left + " still empty." };
    var wrong = slots.filter(function (s) { var c = cardOf(rd, ans[s.slot]); return !c || c.slot !== s.slot; });
    if (wrong.length) {
      var c = cardOf(rd, ans[wrong[0].slot]), msg = (c && c.why) || "That card belongs in a different box.";
      if (rd.sim === "pelican") { var sim = CT.pelican(build(rd, ans)); if (sim.problem) msg = sim.problem; }
      return { ok: false, wrong: wrong.map(function (s) { return ans[s.slot]; }), msg: (wrong.length > 1 ? wrong.length + " boxes are not right yet. " : "Box " + wrong[0].label + " is not right yet. ") + msg };
    }
    return { ok: true };
  }
  CT.check.flowbuild = function (d, a) {
    a = a || [];
    for (var i = 0; i < d.rounds.length; i++) {
      var r = checkRound(d.rounds[i], a[i]);
      if (!r.ok) return Object.assign(r, { round: i });
    }
    return { ok: true };
  };
  CT.solve.flowbuild = function (d) {
    return d.rounds.map(function (rd) {
      var a = {};
      rd.cards.forEach(function (c) { if (c.slot) a[c.slot] = c.id; });
      return a;
    });
  };

  // A small drawing of a card's symbol.
  CT.shapeIcon = function (t) {
    var d = { io: "M6 2 H34 L28 18 H0 Z", process: "M1 2 H33 V18 H1 Z", decision: "M17 0 L34 10 L17 20 L0 10 Z", start: "M9 2 H25 A8 8 0 0 1 25 18 H9 A8 8 0 0 1 9 2 Z" }[t] || "M1 2 H33 V18 H1 Z";
    return CT.svg("svg", { class: "fcs fcs-" + t, viewBox: "0 0 34 20", "aria-hidden": "true" }, [CT.svg("path", { d: d })]);
  };
  var SHAPE_NAME = { io: "parallelogram", process: "rectangle", decision: "diamond" };

  CT.engines.flowbuild = {
    mount: function (host, level, api) {
      var d = level.data, ri = 0, rd, ans = {}, wrong = {}, on = null, results = null, simState = null;
      var board = CT.el("div", { class: "cfb" });
      host.appendChild(board);
      var order;

      function start(i) {
        ri = i; rd = d.rounds[ri]; ans = {}; wrong = {}; on = null; results = null;
        simState = rd.sim === "pelican" ? { lights: "green", man: "red", clock: 0, pressed: false } : null;
        order = CT.shuffle(rd.cards.map(function (c) { return c.id; }), CT.rng(level.id + ":c" + ri));
        render();
        if (i > 0) api.say("Next flowchart: " + rd.problem, "think", 3000);
      }
      function kindOf(slot) { return slotsOf(rd.flow).filter(function (s) { return s.slot === slot; })[0].kind; }

      function cardEl(c) {
        var el = CT.card({ id: c.id, text: c.text }, { "aria-label": c.text + ", in a " + (SHAPE_NAME[c.t] || "box") });
        el.insertBefore(CT.shapeIcon(c.t), el.firstChild);
        el.classList.add("cfb-card", "cfb-" + c.t);
        if (wrong[c.id]) el.classList.add("is-wrong");
        return el;
      }
      function render() {
        CT.clear(board);
        var chart = CT.el("div", { class: "cfb-chart" });
        chart.innerHTML = CT.flow.svg(build(rd, ans), { on: on, label: "Your flowchart for: " + rd.problem });
        var slotsBox = CT.el("ol", { class: "cfb-slots", "aria-label": "Numbered boxes" });
        slotsOf(rd.flow).forEach(function (s) {
          var id = ans[s.slot];
          var z = CT.el("li", { class: "cid-slot ct-zone cfb-slot" + (id ? " is-full" : ""), "data-zone": "slot-" + s.slot,
            "data-zone-label": "box " + s.label + (s.kind === "slot" ? "" : " (a decision)") }, [CT.el("span", { class: "cfb-num" }, s.label)]);
          if (id) z.appendChild(cardEl(cardOf(rd, id)));
          else z.appendChild(CT.el("span", { class: "ctr-empty" }, s.kind === "slot" ? "Box " + s.label : "Box " + s.label + ": a question"));
          z.appendChild(CT.el("button", { type: "button", class: "ct-drop", "aria-label": "Put the picked card in box " + s.label }, "Put here"));
          slotsBox.appendChild(z);
        });
        var tray = CT.el("div", { class: "ct-tray", "data-zone": "tray", "data-zone-label": "the step cards" }, [CT.el("p", { class: "ct-tray-h" }, "Step cards")]);
        var used = Object.keys(ans).map(function (k) { return ans[k]; });
        order.filter(function (id) { return used.indexOf(id) < 0; }).forEach(function (id) { tray.appendChild(cardEl(cardOf(rd, id))); });
        var right = CT.el("div", { class: "cfb-right" }, [slotsBox, tray]);
        if (simState) right.insertBefore(simPanel(), right.firstChild);
        if (results) right.appendChild(testTable(results));
        CT.append(board, [CT.roundChip(ri, d.rounds.length), CT.el("div", { class: "ct-problem" }, [CT.el("span", { class: "ct-problem-k" }, "Problem"), rd.problem]),
          CT.el("div", { class: "cfb-wrap" }, [chart, right])]);
      }
      function simPanel() {
        var L = simState.lights, M = simState.man;
        var lamp = function (c, onIf) { return CT.el("i", { class: "cfb-lamp cfb-" + c + (onIf ? " is-on" : "") }); };
        return CT.el("div", { class: "cfb-sim", role: "img", "aria-label": "Traffic lights: " + L + ". Pedestrian signal: " + M + " man." + (simState.pressed ? " The button has been pressed." : "") }, [
          CT.el("div", { class: "cfb-tl" }, [lamp("red", L === "red"), lamp("amber", L === "amber"), lamp("green", L === "green")]),
          CT.el("div", { class: "cfb-ped" }, [CT.el("span", { class: "cfb-man" + (M === "red" ? " is-red" : "") }, CT.ico("person-red")), CT.el("span", { class: "cfb-man" + (M === "green" ? " is-green" : "") }, CT.ico("person-green"))]),
          CT.el("div", { class: "cfb-info" }, [CT.el("p", null, [CT.ico("stopwatch"), " ", CT.el("b", null, simState.clock + " s")]), CT.el("p", { class: "cfb-btn" + (simState.pressed ? " is-on" : "") }, simState.pressed ? "Button pressed" : "Button not pressed")])
        ]);
      }
      function testTable(res) {
        return CT.el("table", { class: "cfl-table cfb-tests" }, [
          CT.el("caption", null, "Test results"),
          CT.el("thead", null, CT.el("tr", null, ["Input", "Expected output", "Actual output", ""].map(function (h) { return CT.el("th", { scope: "col" }, h); }))),
          CT.el("tbody", null, res.map(function (t) {
            return CT.el("tr", { class: t.pass ? "is-pass" : "is-fail" }, [CT.el("td", null, t.inputs.join(", ") || "none"), CT.el("td", null, t.expect.join(", ")),
              CT.el("td", null, t.got ? t.got.join(", ") || "nothing" : "Error: " + t.error.msg), CT.el("td", null, [CT.ico(t.pass ? "tick" : "no"), t.pass ? " Pass" : " Fail"])]);
          }))]);
      }

      var dd = CT.dnd(board, {
        canDrop: function (id, zone) {
          if (zone === "tray") return true;
          if (zone.indexOf("slot-") !== 0) return false;
          var c = cardOf(rd, id), k = kindOf(zone.slice(5));
          return k === "slot" ? c.t !== "decision" : c.t === "decision";
        },
        onMove: function (id, zone) {
          Object.keys(ans).forEach(function (s) { if (ans[s] === id) delete ans[s]; });
          if (zone !== "tray") ans[zone.slice(5)] = id;
          wrong = {}; results = null; render();
        }
      });
      start(0);

      // Light up each symbol in turn as the flowchart runs.
      function animateRun(done) {
        var flow = build(rd, ans), code = CT.flow.code(flow);
        api.busy(true);
        if (rd.sim === "pelican") {
          var st = simState = { lights: "green", man: "red", clock: 0, pressed: false };
          var stepper = CT.pseudo.steps(code.text, { maxSteps: 3000, builtins: {
            lights: function (c) { st.lights = c; }, man: function (c) { st.man = c; }, wait: function (n) { st.clock += n; },
            pressed: function () { if (st.clock >= 4) st.pressed = true; return st.clock >= 4; } } });
          (function tick() {
            if (!api.alive()) return;
            var r = stepper.next();
            if (r.done) { on = null; api.busy(false); render(); done(); return; }
            on = code.map[r.line - 1]; render();
            CT.sound.play("step");
            CT.wait(st.clock < 4 ? 260 : 420, tick);
          })();
          return;
        }
        var all = [], k = 0;
        (function nextTest() {
          if (!api.alive()) return;
          if (k >= rd.tests.length) { on = null; results = CT.flow.test(flow, rd.tests); api.busy(false); render(); done(); return; }
          var t = rd.tests[k++], stepper = CT.pseudo.steps(code.text, { inputs: t.inputs, quiet: true, maxSteps: 3000 });
          (function tick() {
            if (!api.alive()) return;
            var r = stepper.next();
            if (r.done) { all.push(r); CT.wait(250, nextTest); return; }
            on = code.map[r.line - 1]; render();
            CT.wait(230, tick);
          })();
        })();
      }

      return {
        checkLabel: "Run the flowchart",
        run: function (done) {
          var r = checkRound(rd, ans);
          if (!r.ok) { done(r); return; }
          animateRun(function () {
            done(ri < d.rounds.length - 1 ? CT.nextRound(api, ri, d.rounds.length, start) : r);
          });
        },
        mark: function (r) { wrong = {}; (r.wrong || []).forEach(function (id) { wrong[id] = true; }); render(); },
        reset: function () { start(ri); },
        showMe: function () { ans = CT.solve.flowbuild({ rounds: [rd] })[0]; wrong = {}; render(); },
        scaffold: function () {
          var sol = CT.solve.flowbuild({ rounds: [rd] })[0];
          var s = slotsOf(rd.flow).filter(function (x) { return ans[x.slot] !== sol[x.slot]; })[0];
          if (!s) return;
          Object.keys(ans).forEach(function (k) { if (ans[k] === sol[s.slot]) delete ans[k]; });
          ans[s.slot] = sol[s.slot]; wrong = {}; render();
          CT.announce("Pixel placed a card in box " + s.label + ".");
        },
        destroy: function () { dd.destroy(); }
      };
    }
  };
})(typeof window !== "undefined" ? window : globalThis);
