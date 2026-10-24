/* Engine: flowfix. Test a flowchart, find the step that makes a test fail, fix it.
 *
 * data: { rounds: [{title, flow, tests: [{inputs, expect}], bug: nodeId,
 *                   fixes: [{text, code}], answer: index, why}] }
 * The student runs the tests (free, as often as they like), follows the
 * failing test's path through the chart, clicks the broken step and checks
 * it. Once the right step is found they choose a fix, and the tests must pass.
 * answer: [{node, fix} per round]
 */
(function (root) {
  "use strict";
  var CT = root.CT = root.CT || {};

  function fixed(rd, fixIndex) {
    var f = rd.fixes[fixIndex];
    return CT.flow.replace(rd.flow, rd.bug, { text: f.text, code: f.code });
  }
  function checkRound(rd, a) {
    a = a || {};
    if (!a.node) return { ok: false, incomplete: true, msg: "Click the step you think is broken, then press Check." };
    if (a.node !== rd.bug) return { ok: false, wrong: [a.node], msg: "That step works for every test. Follow the failing test's path to find where it goes wrong." };
    if (a.fix === undefined || a.fix === null) return { ok: false, incomplete: true, found: true, msg: "Yes, that's the broken step! Now choose the fix." };
    var res = CT.flow.test(fixed(rd, a.fix), rd.tests), fails = res.filter(function (t) { return !t.pass; }).length;
    if (!fails) return { ok: true };
    return { ok: false, msg: "With that fix, " + fails + " test" + (fails > 1 ? "s still fail. " : " still fails. ") + rd.why,
             nudge: "With that fix, " + fails + " test" + (fails > 1 ? "s still fail." : " still fails.") + " Run the tests to see what it does." };
  }
  CT.check.flowfix = function (d, a) {
    a = a || [];
    for (var i = 0; i < d.rounds.length; i++) {
      var r = checkRound(d.rounds[i], a[i]);
      if (!r.ok) return Object.assign(r, { round: i });
    }
    return { ok: true };
  };
  CT.solve.flowfix = function (d) { return d.rounds.map(function (rd) { return { node: rd.bug, fix: rd.answer }; }); };
  CT.flowFixed = fixed;

  // The symbols a test passes through, in order.
  function pathOf(flow, t) {
    var code = CT.flow.code(flow), st = CT.pseudo.steps(code.text, { inputs: t.inputs || [], quiet: true, maxSteps: 3000 }), seen = {}, r;
    while (!(r = st.next()).done) seen[code.map[r.line - 1]] = true;
    return seen;
  }

  CT.engines.flowfix = {
    mount: function (host, level, api) {
      var d = level.data, ri = 0, rd, pick = null, fix = null, found = false, results = null, path = null, tries = 0;
      var board = CT.el("div", { class: "cff" });
      host.appendChild(board);

      function start(i) {
        ri = i; rd = d.rounds[ri]; pick = null; fix = null; found = false; results = null; path = null; tries = 0;
        render();
        if (i > 0) api.say("Next broken flowchart: " + rd.title + ". Run the tests first!", "think", 3000);
      }
      function current() { return found && fix !== null ? fixed(rd, fix) : rd.flow; }

      function render(focus) {
        CT.clear(board);
        var chart = CT.el("div", { class: "cfb-chart" });
        chart.innerHTML = CT.flow.svg(current(), { picked: pick, path: path, clickable: true, label: "Flowchart: " + rd.title + ". Click a step to choose it." });
        Array.prototype.forEach.call(chart.querySelectorAll("[data-node]"), function (g) {
          var id = g.getAttribute("data-node"), n = CT.byId(CT.flow.nodes(rd.flow), id);
          if (!n || n.t === "start" || n.t === "end") { g.removeAttribute("tabindex"); g.removeAttribute("role"); return; }
          var choose = function () { if (pick !== id) { pick = id; found = false; fix = null; } render('[data-node="' + id + '"]'); CT.sound.play("pick"); };
          g.addEventListener("click", choose);
          g.addEventListener("keydown", function (e) { if (e.key === "Enter" || e.key === " ") { e.preventDefault(); choose(); } });
        });
        var right = CT.el("div", { class: "cfb-right" });
        right.appendChild(CT.el("button", { type: "button", class: "ct-btn ct-btn-soft", onclick: runTests }, "🧪 Run the tests"));
        right.appendChild(CT.el("p", { class: "cff-note" }, pick ? "Chosen step: " + label(pick) + ". Press Check when you are sure." : "Click a step in the flowchart to choose it."));
        if (results) right.appendChild(table(results));
        if (found) {
          var opts = CT.el("div", { class: "ct-mcq" });
          CT.shuffle(rd.fixes.map(function (f, i) { return i; }), CT.rng(level.id + ":f" + ri)).forEach(function (i) {
            opts.appendChild(CT.el("button", { type: "button", class: "ct-mcq-opt" + (fix === i ? " is-chosen" : ""), "aria-pressed": fix === i ? "true" : "false", "data-fix": String(i),
              onclick: function () { fix = i; results = null; path = null; render("[data-fix='" + i + "']"); CT.sound.play("tap"); } }, rd.fixes[i].text));
          });
          right.appendChild(CT.el("div", { class: "cseq-fix" }, [CT.el("p", { class: "ct-tray-h" }, "Change this step to"), opts]));
        }
        CT.append(board, [CT.roundChip(ri, d.rounds.length), CT.el("h3", { class: "cff-title" }, "🔧 " + rd.title), CT.el("div", { class: "cfb-wrap" }, [chart, right])]);
        if (focus) { var f = board.querySelector(focus); if (f) f.focus(); }
      }
      function label(id) { var n = CT.byId(CT.flow.nodes(rd.flow), id); return n ? n.text : id; }
      function table(res) {
        return CT.el("table", { class: "cfl-table cfb-tests" }, [
          CT.el("caption", null, "Tests"),
          CT.el("thead", null, CT.el("tr", null, ["Input", "Expected", "Actual", ""].map(function (h) { return CT.el("th", { scope: "col" }, h); }))),
          CT.el("tbody", null, res.map(function (t, i) {
            return CT.el("tr", { class: t.pass ? "is-pass" : "is-fail" }, [CT.el("td", null, t.inputs.join(", ") || "none"), CT.el("td", null, t.expect.join(", ")),
              CT.el("td", null, t.got ? t.got.join(", ") || "nothing" : "Error"), CT.el("td", null, [t.pass ? "✅" : "❌",
                !t.pass ? CT.el("button", { type: "button", class: "ct-btn ct-btn-mini", onclick: function () { path = pathOf(current(), rd.tests[i]); render(); } }, "Show its path") : null])]);
          }))]);
      }
      function runTests() {
        results = CT.flow.test(current(), rd.tests);
        var firstFail = results.findIndex(function (t) { return !t.pass; });
        path = firstFail >= 0 ? pathOf(current(), rd.tests[firstFail]) : null;
        CT.sound.play(firstFail >= 0 ? "bad" : "good");
        render();
        api.say(firstFail >= 0 ? "The blue path shows where the failing test went. Where did it go wrong?" : "Every test passes! Press Check.", "think", 3000);
      }

      start(0);
      return {
        check: function () {
          var r = checkRound(rd, { node: pick, fix: fix });
          if (r.found) { found = true; render(); return r; }
          if (r.ok) return ri < d.rounds.length - 1 ? CT.nextRound(api, ri, d.rounds.length, start) : r;
          if (!r.incomplete) { tries++; if (r.nudge && tries < 2) r = Object.assign({}, r, { msg: r.nudge }); }
          return r;
        },
        mark: function () { render(); },
        reset: function () { start(ri); },
        showMe: function () { pick = rd.bug; found = true; fix = rd.answer; results = null; path = null; render(); },
        scaffold: function () { pick = rd.bug; found = true; render(); CT.announce("Pixel pointed to the broken step."); },
        destroy: function () { }
      };
    }
  };
})(typeof window !== "undefined" ? window : globalThis);
