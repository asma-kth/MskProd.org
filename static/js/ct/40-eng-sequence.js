/* Engine: sequence. Patterns in a row: fill the gaps, answer a question about
 * the rule, find the item that breaks the pattern, or find and fix the line of
 * code whose output breaks it.
 *
 * data: { look: "emoji"|"colour"|"number"|"lights", palette, rounds: [...] }
 * Round types (each may override look and palette):
 *   fill  { seq: [value|null], answers: [value], why }
 *   ask   { seq, q, options, answer: index, tiles, hint, why }  or  { input: true, answer: number }
 *   odd   { seq, wrong: index, fix: value, why }
 *   code  { code, expect: [lines], bug: line number, fixes: [line text], answer: index, why }
 * The first wrong try in a round gets a nudge; later ones get the full reason.
 * answer: one entry per round: fill [values], ask index or number, odd {pick, fix}, code {line, fix}
 */
(function (root) {
  "use strict";
  var CT = root.CT = root.CT || {};

  function empty(v) { return v === undefined || v === null || v === ""; }
  function same(a, b) { return String(a).trim() === String(b); }

  // The program with line n swapped for the chosen fix.
  CT.patchCode = function (code, line, text) {
    var lines = code.split("\n");
    lines[line - 1] = text;
    return lines.join("\n");
  };

  function checkRound(rd, a) {
    switch (rd.type) {
      case "fill": {
        a = a || [];
        var left = rd.answers.filter(function (x, i) { return empty(a[i]); }).length;
        if (left) return { ok: false, incomplete: true, msg: "Fill every gap first: " + left + " still empty." };
        var bad = [];
        rd.answers.forEach(function (x, i) { if (!same(a[i], x)) bad.push(i); });
        if (!bad.length) return { ok: true };
        return { ok: false, wrong: bad, msg: (bad.length > 1 ? bad.length + " gaps don't fit the pattern yet. " : "One gap doesn't fit the pattern yet. ") + rd.why };
      }
      case "ask": {
        if (empty(a)) return { ok: false, incomplete: true, msg: rd.input ? "Type your answer first." : "Choose an answer first." };
        if (rd.input ? same(a, rd.answer) : a === rd.answer) return { ok: true };
        return { ok: false, msg: rd.why, nudge: "Not quite. Use the pattern's rule to work it out, then try again." };
      }
      case "odd": {
        a = a || {};
        if (empty(a.pick)) return { ok: false, incomplete: true, msg: "Click the item that breaks the pattern." };
        if (a.pick !== rd.wrong) return { ok: false, wrong: [a.pick], msg: "That one fits the pattern. Look for the item that breaks it." };
        if (empty(a.fix)) return { ok: false, incomplete: true, msg: "Well spotted! Now choose what it should be." };
        if (!same(a.fix, rd.fix)) return { ok: false, wrong: [a.pick], msg: rd.why, nudge: "That still breaks the pattern. What should go there?" };
        return { ok: true };
      }
      case "code": {
        a = a || {};
        if (!a.line) return { ok: false, incomplete: true, msg: "Click the line with the bug." };
        if (a.line !== rd.bug) return { ok: false, msg: "Line " + a.line + " does its job. Which line makes or controls the numbers?" };
        if (empty(a.fix)) return { ok: false, incomplete: true, msg: "Now choose the fix for line " + a.line + "." };
        if (a.fix === rd.answer) return { ok: true };
        var out = CT.pseudo.run(CT.patchCode(rd.code, rd.bug, rd.fixes[a.fix]), { maxSteps: 2000 });
        var shows = out.ok ? (out.output.join(", ") || "nothing") : "an error";
        return { ok: false, msg: "With that fix the program prints " + shows + ". " + rd.why,
                 nudge: "With that fix the program prints " + shows + ", not " + rd.expect.join(", ") + "." };
      }
    }
    return { ok: false, msg: "Unknown round." };
  }
  CT.check.sequence = function (d, a) {
    a = a || [];
    for (var i = 0; i < d.rounds.length; i++) {
      var r = checkRound(d.rounds[i], a[i]);
      if (!r.ok) return Object.assign(r, { round: i });
    }
    return { ok: true };
  };
  function solveRound(rd) {
    if (rd.type === "fill") return rd.answers.slice();
    if (rd.type === "ask") return rd.answer;
    if (rd.type === "odd") return { pick: rd.wrong, fix: rd.fix };
    return { line: rd.bug, fix: rd.answer };
  }
  CT.solve.sequence = function (d) { return d.rounds.map(solveRound); };

  // ---------------------------------------------------------------- tiles
  function entry(pal, v) {
    for (var i = 0; i < (pal || []).length; i++) { var p = pal[i]; if ((p && p.id !== undefined ? p.id : p) === v) return p; }
    return null;
  }
  CT.seqTile = function (v, look, pal) {
    var p = entry(pal, v), label = p && p.label ? p.label : String(v);
    // A letter as well as a colour, so the pattern does not depend on seeing colour.
    if (look === "colour") return CT.el("span", { class: "cseq-bead", style: { background: p ? p.c : "#94A3B8" }, role: "img", "aria-label": label }, label.charAt(0));
    if (look === "lights") {
      var on = { R: [1, 0, 0], RA: [1, 1, 0], G: [0, 0, 1], A: [0, 1, 0] }[v] || [0, 0, 0];
      return CT.el("span", { class: "cseq-light", role: "img", "aria-label": label }, ["r", "a", "g"].map(function (c, i) {
        return CT.el("i", { class: "cseq-l cseq-l-" + c + (on[i] ? " is-on" : "") });
      }));
    }
    if (look === "number") return CT.el("span", { class: "cseq-num" }, String(v));
    return CT.el("span", { class: "cseq-emo", role: "img", "aria-label": label }, String(v));
  };
  function valueOf(p) { return p && p.id !== undefined ? p.id : p; }
  function labelOf(p) { return p && p.label ? p.label : String(p); }

  // Code with line numbers; each line can be a button.
  CT.codeView = function (code, opts) {
    opts = opts || {};
    var box = CT.el("ol", { class: "ct-code" + (opts.pick ? " is-pick" : "") });
    code.split("\n").forEach(function (text, i) {
      var n = i + 1, inner = CT.el("code", { html: CT.hilite(text) });
      var li = CT.el("li", { class: (opts.picked === n ? "is-picked" : "") + (opts.mark === n ? " is-mark" : "") });
      if (opts.pick) li.appendChild(CT.el("button", { type: "button", class: "ct-code-line", "aria-pressed": opts.picked === n ? "true" : "false",
        "aria-label": "Line " + n + ": " + text.trim(), onclick: function () { opts.pick(n); } }, [CT.el("span", { class: "ct-ln", "aria-hidden": "true" }, String(n)), inner]));
      else CT.append(li, [CT.el("span", { class: "ct-ln", "aria-hidden": "true" }, String(n)), inner]);
      box.appendChild(li);
    });
    return box;
  };
  // A light touch of colour for keywords, text and numbers.
  CT.hilite = function (text) {
    var esc = function (s) { return s.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); };
    var out = "", re = /("[^"]*"?|'[^']*'?)|(\/\/.*$)|\b(if|then|elseif|else|endif|for|to|step|next|while|endwhile|do|until|repeat|print|input|and|or|not|mod|div|true|false|array|AND|OR|NOT|MOD|DIV)\b|(\b\d+(?:\.\d+)?\b)/g;
    var last = 0, m;
    while ((m = re.exec(text))) {
      out += esc(text.slice(last, m.index));
      if (m[1]) out += '<span class="hl-s">' + esc(m[1]) + "</span>";
      else if (m[2]) out += '<span class="hl-c">' + esc(m[2]) + "</span>";
      else if (m[3]) out += '<span class="hl-k">' + esc(m[3]) + "</span>";
      else out += '<span class="hl-n">' + esc(m[4]) + "</span>";
      last = re.lastIndex;
    }
    return out + esc(text.slice(last)) || " ";
  };

  CT.engines.sequence = {
    mount: function (host, level, api) {
      var d = level.data, ri = 0, rd, ans, active = 0, wrong = {}, tries = 0, struck = {}, preview = null;
      var board = CT.el("div", { class: "cseq" });
      host.appendChild(board);
      function look() { return rd.look || d.look || "emoji"; }
      function pal() { return rd.palette || d.palette || []; }

      function start(i) {
        ri = i; rd = d.rounds[ri]; wrong = {}; tries = 0; struck = {}; preview = null;
        ans = rd.type === "fill" ? rd.answers.map(function () { return null; }) : rd.type === "odd" || rd.type === "code" ? {} : null;
        active = 0;
        render();
        if (i > 0) api.say(rd.type === "odd" ? "Something here breaks the pattern. Can you find it?" : rd.type === "code" ? "Time to debug some code!" : "Next pattern!", "think", 2400);
      }
      function gapIndexes() { var g = []; rd.seq.forEach(function (v, i) { if (v === null) g.push(i); }); return g; }

      function render(focus) {
        CT.clear(board);
        CT.append(board, [CT.roundChip(ri, d.rounds.length), rd.text ? CT.el("p", { class: "cseq-text" }, rd.text) : null]);
        if (rd.type === "code") { renderCode(); return; }
        var row = CT.el("div", { class: "cseq-row cseq-" + look(), role: "list", "aria-label": "The pattern" });
        var g = 0;
        rd.seq.forEach(function (v, i) {
          var cell;
          if (rd.type === "fill" && v === null) {
            var k = g++, val = ans[k];
            if (look() === "number") {
              cell = CT.el("input", { type: "text", inputmode: "numeric", class: "cseq-in" + (wrong[k] ? " is-wrong" : ""), value: val === null ? "" : String(val),
                "aria-label": "Gap " + (k + 1), "data-gap": String(k), oninput: (function (kk) { return function () { ans[kk] = this.value.replace(/[^0-9.-]/g, ""); this.value = ans[kk]; }; })(k),
                onkeydown: function (e) { if (e.key === "Enter") { e.preventDefault(); api.submit(); } } });
            } else {
              cell = CT.el("button", { type: "button", class: "cseq-gap" + (k === active ? " is-active" : "") + (wrong[k] ? " is-wrong" : "") + (val !== null ? " is-full" : ""),
                "data-gap": String(k),
                "aria-label": "Gap " + (k + 1) + (val !== null ? ": " + labelOf(entry(pal(), val) || val) : ", empty") + (k === active ? ", selected" : ""),
                onclick: (function (kk) { return function () { active = kk; render("[data-gap='" + kk + "']"); }; })(k) },
                val !== null ? CT.seqTile(val, look(), pal()) : CT.el("span", { class: "cseq-q", "aria-hidden": "true" }, "?"));
            }
          } else if (rd.type === "odd") {
            var picked = ans.pick === i, shown = picked && !empty(ans.fix) ? ans.fix : v;
            cell = CT.el("button", { type: "button", class: "cseq-cell cseq-pickable" + (picked ? " is-picked" : "") + (wrong[i] ? " is-wrong" : ""),
              "aria-pressed": picked ? "true" : "false", "aria-label": "Item " + (i + 1) + ": " + labelOf(entry(pal(), shown) || shown), "data-cell": String(i),
              onclick: (function (ii) { return function () { if (ans.pick !== ii) { ans.pick = ii; ans.fix = null; } wrong = {}; render("[data-cell='" + ii + "']"); CT.sound.play("pick"); }; })(i) },
              CT.seqTile(shown, look(), pal()));
          } else cell = CT.el("span", { class: "cseq-cell" }, CT.seqTile(v, look(), pal()));
          row.appendChild(CT.el("span", { class: "cseq-slot", role: "listitem" }, [cell, CT.el("small", { class: "cseq-pos", "aria-hidden": "true" }, String(i + 1))]));
        });
        if (rd.type === "ask") row.appendChild(CT.el("span", { class: "cseq-more", "aria-hidden": "true" }, "…"));
        board.appendChild(row);
        if (rd.type === "odd" && empty(ans.pick)) board.appendChild(CT.el("p", { class: "cseq-hint" }, "👆 Click the item that breaks the pattern."));
        if (rd.type === "fill" && look() !== "number") board.appendChild(CT.el("p", { class: "cseq-hint" }, "👆 Pick a gap, then choose what goes in it."));

        if (rd.type === "fill" && look() !== "number") board.appendChild(palette(function (v) {
          ans[active] = v;
          delete wrong[active];
          var next = gapIndexes().map(function (x, k) { return k; }).filter(function (k) { return ans[k] === null; })[0];
          if (next !== undefined) active = next;
          render();
          CT.sound.play("drop");
        }, "Fill the selected gap with"));
        if (rd.type === "odd" && !empty(ans.pick)) {
          var fixBox = CT.el("div", { class: "cseq-fix" }, [CT.el("p", { class: "ct-tray-h" }, "What should item " + (ans.pick + 1) + " be?")]);
          if (look() === "number") {
            fixBox.appendChild(CT.el("input", { type: "text", inputmode: "numeric", class: "cseq-in", value: empty(ans.fix) ? "" : String(ans.fix), "aria-label": "Correct value for item " + (ans.pick + 1),
              oninput: function () { ans.fix = this.value.replace(/[^0-9.-]/g, ""); this.value = ans.fix; },
              onkeydown: function (e) { if (e.key === "Enter") { e.preventDefault(); api.submit(); } } }));
          } else fixBox.appendChild(palette(function (v) { ans.fix = v; wrong = {}; render(); CT.sound.play("drop"); }, "Change it to"));
          board.appendChild(fixBox);
        }
        if (rd.type === "ask") renderAsk();
        if (focus) { var f = board.querySelector(focus); if (f) f.focus(); }
      }

      function palette(onPick, label) {
        var box = CT.el("div", { class: "cseq-pal", role: "group", "aria-label": label });
        pal().forEach(function (p) {
          var v = valueOf(p);
          box.appendChild(CT.el("button", { type: "button", class: "cseq-pbtn", "data-pal": String(v), "aria-label": label + " " + labelOf(p),
            onclick: function () { onPick(v); } }, [CT.seqTile(v, look(), pal()), look() === "colour" || look() === "lights" ? CT.el("small", { "aria-hidden": "true" }, labelOf(p)) : null]));
        });
        return box;
      }

      function renderAsk() {
        var box = CT.el("div", { class: "cg-follow cseq-ask" }, [CT.el("p", { class: "ct-kicker" }, "🔎 Pattern question"), CT.el("h3", null, rd.q)]);
        if (rd.input) {
          box.appendChild(CT.el("input", { type: "text", inputmode: "numeric", class: "cseq-in cseq-in-big", value: empty(ans) ? "" : String(ans), "aria-label": "Your answer",
            oninput: function () { ans = this.value.replace(/[^0-9.-]/g, ""); this.value = ans; },
            onkeydown: function (e) { if (e.key === "Enter") { e.preventDefault(); api.submit(); } } }));
        } else {
          var opts = CT.el("div", { class: rd.tiles ? "cseq-pal" : "ct-mcq" });
          CT.shuffle(rd.options.map(function (o, i) { return i; }), CT.rng(level.id + ":q" + ri)).forEach(function (i) {
            var o = rd.options[i];
            opts.appendChild(CT.el("button", { type: "button", class: (rd.tiles ? "cseq-pbtn" : "ct-mcq-opt") + (ans === i ? " is-chosen" : "") + (struck[i] ? " is-struck" : ""),
              disabled: struck[i] ? true : null, "aria-pressed": ans === i ? "true" : "false", "data-opt": String(i),
              "aria-label": rd.tiles ? labelOf(entry(pal(), o) || o) : null,
              onclick: function () { ans = i; render("[data-opt='" + i + "']"); CT.sound.play("tap"); } },
              rd.tiles ? CT.seqTile(o, look(), pal()) : o));
          });
          box.appendChild(opts);
        }
        board.appendChild(box);
      }

      function renderCode() {
        var expect = CT.el("div", { class: "cseq-out" }, [CT.el("p", { class: "ct-tray-h" }, "It should print"), CT.el("pre", null, rd.expect.join("\n"))]);
        var now = CT.pseudo.run(rd.code, { maxSteps: 2000 });
        var actual = CT.el("div", { class: "cseq-out is-bad" }, [CT.el("p", { class: "ct-tray-h" }, "It actually prints"), CT.el("pre", null, now.output.join("\n"))]);
        var outs = [expect, actual];
        if (preview) outs.push(CT.el("div", { class: "cseq-out" + (preview.good ? " is-good" : " is-bad") }, [CT.el("p", { class: "ct-tray-h" }, "With your fix"), CT.el("pre", null, preview.text)]));
        board.appendChild(CT.el("div", { class: "cseq-code" }, [
          CT.el("div", null, [CT.el("p", { class: "ct-tray-h" }, "The program: click the line with the bug"),
            CT.codeView(rd.code, { pick: function (n) { if (ans.line !== n) { ans.line = n; ans.fix = null; preview = null; } render("[aria-label^='Line " + n + ":']"); CT.sound.play("pick"); }, picked: ans.line })]),
          CT.el("div", { class: "cseq-outs" }, outs)]));
        if (ans.line) {
          var fx = CT.el("div", { class: "cseq-fix" }, [CT.el("p", { class: "ct-tray-h" }, "Replace line " + ans.line + " with")]);
          var opts = CT.el("div", { class: "ct-mcq" });
          CT.shuffle(rd.fixes.map(function (o, i) { return i; }), CT.rng(level.id + ":fx" + ri)).forEach(function (i) {
            opts.appendChild(CT.el("button", { type: "button", class: "ct-mcq-opt cseq-fixopt" + (ans.fix === i ? " is-chosen" : ""), "aria-pressed": ans.fix === i ? "true" : "false", "data-fix": String(i),
              onclick: function () { ans.fix = i; preview = null; render("[data-fix='" + i + "']"); CT.sound.play("tap"); } }, CT.el("code", { html: CT.hilite(rd.fixes[i].trim()) })));
          });
          fx.appendChild(opts);
          if (!empty(ans.fix)) fx.appendChild(CT.el("button", { type: "button", class: "ct-btn ct-btn-mini", onclick: function () {
            var r = CT.pseudo.run(CT.patchCode(rd.code, ans.line, rd.fixes[ans.fix]), { maxSteps: 2000 });
            preview = { text: r.ok ? r.output.join("\n") : "Error: " + r.error.msg, good: r.ok && r.output.join("\n") === rd.expect.join("\n") };
            render(); CT.sound.play("step");
          } }, "▶ Try my fix"));
          board.appendChild(fx);
        }
      }

      start(0);

      return {
        check: function () {
          var r = checkRound(rd, ans);
          if (r.ok) {
            if (ri < d.rounds.length - 1) return CT.nextRound(api, ri, d.rounds.length, start);
            return r;
          }
          if (!r.incomplete) {
            tries++;
            if (r.nudge && tries < 2) r = Object.assign({}, r, { msg: r.nudge });
          }
          return r;
        },
        mark: function (r) {
          wrong = {};
          (r.wrong || []).forEach(function (i) { wrong[i] = true; });
          if (rd.type === "odd" && r.wrong && r.wrong[0] !== rd.wrong) { ans = {}; }
          render();
        },
        reset: function () { start(ri); },
        showMe: function () { ans = solveRound(rd); if (rd.type === "fill") ans = ans.slice(); wrong = {}; render(); },
        scaffold: function () {
          if (rd.type === "fill") {
            var k = rd.answers.map(function (x, i) { return i; }).filter(function (i) { return !same(ans[i] === null ? "" : ans[i], rd.answers[i]); })[0];
            if (k !== undefined) { ans[k] = rd.answers[k]; active = k; }
          } else if (rd.type === "ask") {
            if (rd.hint) api.say(rd.hint, "think", 5000);
            if (!rd.input) {
              var wrongOnes = rd.options.map(function (o, i) { return i; }).filter(function (i) { return i !== rd.answer && !struck[i]; });
              wrongOnes.slice(0, 2).forEach(function (i) { struck[i] = true; });
              if (struck[ans]) ans = null;
            }
          } else if (rd.type === "odd") { ans = { pick: rd.wrong, fix: null }; }
          else { ans = { line: rd.bug, fix: null }; }
          render();
          CT.announce("Pixel did one step for you.");
        },
        demo: function (done) {
          var mv = (level.watch && level.watch.moves) || [];
          if (!mv.length || rd.type !== "fill") { done(); return; }
          var k = mv[0][0], v = mv[0][1];
          if (look() === "number") {
            CT.wait(500, function () { ans[k] = v; render(); CT.sound.play("drop"); CT.wait(400, done); });
            return;
          }
          var from = board.querySelector('[data-pal="' + v + '"]'), to = board.querySelector('[data-gap="' + k + '"]');
          CT.ghost(from, to, function () { ans[k] = v; active = k + 1; render(); done(); });
        },
        destroy: function () { }
      };
    }
  };
})(typeof window !== "undefined" ? window : globalThis);
