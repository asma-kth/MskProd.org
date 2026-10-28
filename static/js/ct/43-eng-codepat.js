/* Engine: codepat. Replace repeated lines of code with a loop.
 *
 * data: { rounds: [{long: code, template: "for i = 1 to {a} ...", blanks: {a: "3"}}] }
 * The student fills the gaps in the loop. Their loop is run by CT.pseudo and
 * passes when it prints exactly what the long program prints, so any correct
 * answer works, such as i * 7 instead of 7 * i.
 * answer: per round, {blankName: text}
 */
(function (root) {
  "use strict";
  var CT = root.CT = root.CT || {};

  CT.fillTemplate = function (template, vals) {
    return template.replace(/\{(\w+)\}/g, function (m, k) { return vals && vals[k] !== undefined && vals[k] !== null ? String(vals[k]) : ""; });
  };
  function checkRound(rd, vals) {
    vals = vals || {};
    var left = Object.keys(rd.blanks).filter(function (k) { return !String(vals[k] === undefined || vals[k] === null ? "" : vals[k]).trim(); });
    if (left.length) return { ok: false, incomplete: true, msg: "Fill every gap in the loop first: " + left.length + " still empty." };
    var want = CT.pseudo.run(rd.long, { maxSteps: 3000 });
    var got = CT.pseudo.run(CT.fillTemplate(rd.template, vals), { maxSteps: 3000 });
    if (!got.ok) return { ok: false, output: got.output, error: got.error, msg: "Your loop stops with an error on line " + got.error.line + ": " + got.error.msg };
    if (got.output.join("\n") === want.output.join("\n")) return { ok: true, output: got.output };
    var n = got.output.length, m = want.output.length;
    return { ok: false, output: got.output, msg: n !== m
      ? "Your loop prints " + n + " line" + (n === 1 ? "" : "s") + ", but the long program prints " + m + ". Check where the loop starts and stops."
      : "Your loop prints the right number of lines, but not the same ones. Check the part that changes each time." };
  }
  CT.check.codepat = function (d, a) {
    a = a || [];
    for (var i = 0; i < d.rounds.length; i++) {
      var r = checkRound(d.rounds[i], a[i]);
      if (!r.ok) return Object.assign(r, { round: i });
    }
    return { ok: true };
  };
  CT.solve.codepat = function (d) { return d.rounds.map(function (rd) { return Object.assign({}, rd.blanks); }); };

  CT.engines.codepat = {
    mount: function (host, level, api) {
      var d = level.data, ri = 0, rd, vals, result = null;
      var board = CT.el("div", { class: "ccp" });
      host.appendChild(board);

      function start(i) {
        ri = i; rd = d.rounds[ri]; vals = {}; result = null;
        render();
        if (i > 0) api.say("Another long program to shrink!", "think", 2200);
      }
      function render(focus) {
        CT.clear(board);
        var want = CT.pseudo.run(rd.long, { maxSteps: 3000 });
        var longBox = CT.el("div", { class: "ccp-pane" }, [
          CT.el("p", { class: "ct-tray-h" }, "The long program (" + rd.long.split("\n").length + " lines)"),
          CT.codeView(rd.long),
          CT.el("p", { class: "ct-tray-h" }, "It prints"),
          CT.el("pre", { class: "ccp-out" }, want.output.join("\n"))]);
        var mine = CT.el("ol", { class: "ct-code ccp-tpl" });
        rd.template.split("\n").forEach(function (line, li) {
          var code = CT.el("code");
          var parts = line.split(/(\{\w+\})/);
          parts.forEach(function (p) {
            var m = /^\{(\w+)\}$/.exec(p);
            if (!m) { if (p) code.appendChild(CT.el("span", { html: CT.hilite(p) })); return; }
            var k = m[1], w = Math.max(3, String(rd.blanks[k]).length + 2);
            code.appendChild(CT.el("input", { type: "text", class: "ccp-in", size: String(w), value: vals[k] || "", "data-blank": k, autocomplete: "off", spellcheck: "false",
              "aria-label": "Gap " + k + " on line " + (li + 1),
              oninput: function () { vals[k] = this.value; result = null; },
              onkeydown: function (e) { if (e.key === "Enter") { e.preventDefault(); api.submit(); } } }));
          });
          mine.appendChild(CT.el("li", null, [CT.el("span", { class: "ct-ln", "aria-hidden": "true" }, String(li + 1)), code]));
        });
        var mineBox = CT.el("div", { class: "ccp-pane" }, [CT.el("p", { class: "ct-tray-h" }, "Your loop (" + rd.template.split("\n").length + " lines): fill the gaps"), mine]);
        if (result) {
          var lines = result.output || [];
          var list = CT.el("ol", { class: "ccp-cmp" });
          var n = Math.max(lines.length, want.output.length);
          for (var j = 0; j < n; j++) {
            var okLine = lines[j] === want.output[j];
            list.appendChild(CT.el("li", { class: okLine ? "is-ok" : "is-bad" }, [CT.ico(okLine ? "tick" : "no"), " ",
              lines[j] === undefined ? CT.el("i", null, "(nothing)") : lines[j]]));
          }
          mineBox.appendChild(CT.el("p", { class: "ct-tray-h" }, "Your loop prints"));
          mineBox.appendChild(list);
          if (result.error) mineBox.appendChild(CT.el("p", { class: "ccp-err" }, "Error on line " + result.error.line + ": " + result.error.msg));
        }
        CT.append(board, [CT.roundChip(ri, d.rounds.length), CT.el("div", { class: "ccp-wrap" }, [longBox, mineBox])]);
        var f = board.querySelector(focus || "[data-blank]");
        if (focus && f) f.focus();
      }

      start(0);
      return {
        checkLabel: "Run my loop",
        check: function () {
          var r = checkRound(rd, vals);
          if (!r.incomplete) { result = r; render(); }
          if (r.ok) {
            CT.sound.play("good");
            return ri < d.rounds.length - 1 ? CT.nextRound(api, ri, d.rounds.length, start) : r;
          }
          return r;
        },
        mark: function () { },
        reset: function () { start(ri); },
        showMe: function () { vals = Object.assign({}, rd.blanks); result = null; render(); },
        scaffold: function () {
          var k = Object.keys(rd.blanks).filter(function (x) { return String(vals[x] || "").trim() !== rd.blanks[x]; })[0];
          if (k) { vals[k] = rd.blanks[k]; result = null; render("[data-blank='" + k + "']"); CT.announce("Pixel filled one gap for you."); }
        },
        destroy: function () { }
      };
    }
  };
})(typeof window !== "undefined" ? window : globalThis);
