/* The labs: free play with no levels and no marks.
 *
 *   #/lab/pseudocode   write OCR-style pseudocode, run it, step through it and
 *                      see a trace table build itself
 *   #/lab/flowchart    build a flowchart from blocks, watch it drawn with the
 *                      standard symbols, see its pseudocode and run it step by step
 * Everything runs in CT.pseudo inside the page; nothing typed is sent anywhere.
 */
(function (root) {
  "use strict";
  var CT = root.CT = root.CT || {};
  var V = CT.views = CT.views || {};

  var EXAMPLES = [
    { name: "Hello, world", code: 'print("Hello, world!")' },
    { name: "Input and output", inputs: "Ada", code: 'name = input("What is your name? ")\nprint("Hello, " + name)' },
    { name: "If, elseif, else", inputs: "14", code: 'age = int(input("How old are you? "))\nif age >= 18 then\n    print("Adult ticket")\nelseif age >= 5 then\n    print("Child ticket")\nelse\n    print("Free entry")\nendif' },
    { name: "For loop", code: "for i = 1 to 5\n    print(i * i)\nnext i" },
    { name: "Times table", code: 'for i = 1 to 12\n    print(str(i) + " x 7 = " + str(i * 7))\nnext i' },
    { name: "While loop", code: "n = 10\nwhile n > 0\n    print(n)\n    n = n - 3\nendwhile\nprint(\"Lift off!\")" },
    { name: "Guess the number (do until)", inputs: "3\n9\n7", code: 'secret = 7\ndo\n    guess = int(input("Guess: "))\n    if guess < secret then\n        print("Too low")\n    elseif guess > secret then\n        print("Too high")\n    endif\nuntil guess == secret\nprint("Got it!")' },
    { name: "Running total", inputs: "4\n10\n6", code: 'total = 0\nfor i = 1 to 3\n    n = int(input("Number: "))\n    total = total + n\nnext i\nprint("Total: " + str(total))' },
    { name: "Arrays", code: "array scores[4]\nscores[0] = 12\nscores[1] = 7\nscores[2] = 15\nscores[3] = 9\nbest = scores[0]\nfor i = 1 to 3\n    if scores[i] > best then\n        best = scores[i]\n    endif\nnext i\nprint(best)" },
    { name: "Strings", code: 'word = "pixel"\nprint(word.upper)\nprint(word.length)\nprint(word.substring(1, 3))\nprint(word.left(2) + word.right(2))' },
    { name: "MOD and DIV", code: "for n = 1 to 6\n    if n MOD 2 == 0 then\n        print(str(n) + \" is even\")\n    else\n        print(str(n) + \" is odd\")\n    endif\nnext n\nprint(17 DIV 5)\nprint(17 MOD 5)" },
  ];

  // The OCR-style reference card, shared by the playground and the levels.
  CT.guide = function () {
    var rows = [
      ["Store a value", "score = 0"], ["Output", 'print("Hello")'], ["Input", 'name = input("Name? ")'],
      ["Text to number", 'age = int(input("Age? "))'], ["Number to text", 'print("You are " + str(age))'],
      ["Selection", "if x > 5 then\n    print(\"big\")\nelseif x == 5 then\n    print(\"five\")\nelse\n    print(\"small\")\nendif"],
      ["Count-controlled loop", "for i = 1 to 10 step 2\n    print(i)\nnext i"],
      ["Condition-controlled loop", "while x < 100\n    x = x * 2\nendwhile"],
      ["Loop at least once", "do\n    x = x - 1\nuntil x == 0"],
      ["Comparison", "==  !=  <  <=  >  >="], ["Maths", "+  -  *  /  ^  MOD (remainder)  DIV (whole number division)"],
      ["Boolean", "AND  OR  NOT"], ["Arrays", "array names[3]\nnames[0] = \"Ada\""],
      ["Strings", "s.length  s.upper  s.lower  s.substring(start, length)  s.left(n)  s.right(n)"],
      ["Comments", "// this line is a note for humans"]
    ];
    return CT.el("details", { class: "clab-guide" }, [CT.el("summary", null, "📘 OCR-style pseudocode guide"),
      CT.el("p", null, "This adventure writes pseudocode in the style of the OCR Exam Reference Language used in GCSE Computer Science (J277). = stores a value; == compares two values."),
      CT.el("table", { class: "cfl-table clab-ref" }, [CT.el("tbody", null, rows.map(function (r) {
        return CT.el("tr", null, [CT.el("th", { scope: "row" }, r[0]), CT.el("td", null, CT.el("pre", null, r[1]))]);
      }))])]);
  };

  // Run a program step by step and keep a trace: one row each time a line changes a variable or prints.
  // The stepper reports a line just before running it, so changes seen now belong to the line before.
  function trace(code, inputs) {
    var st = CT.pseudo.steps(code, { inputs: inputs, maxSteps: 20000 }), rows = [], names = [], prev = {}, outLen = 0, r, lastLine = null, guard = 0;
    function note(now, line) {
      var changed = {}, any = false;
      Object.keys(now.vars || {}).forEach(function (k) {
        if (Array.isArray(now.vars[k])) return;
        if (names.indexOf(k) < 0) names.push(k);
        if (prev[k] !== now.vars[k]) { changed[k] = now.vars[k]; any = true; }
      });
      var out = (now.output || []).length > outLen ? now.output.slice(outLen).join(" / ") : "";
      if ((any || out) && line !== null) rows.push({ line: line, vals: changed, out: out });
      prev = now.vars || {}; outLen = (now.output || []).length;
    }
    while (!(r = st.next()).done && guard++ < 20000) { note(r, lastLine); lastLine = r.line; }
    note(r, lastLine);
    return { rows: rows, names: names, error: r.error, output: r.output || [] };
  }
  function traceTable(t) {
    return CT.el("table", { class: "cfl-table clab-trace" }, [
      CT.el("caption", null, "Trace table"),
      CT.el("thead", null, CT.el("tr", null, [CT.el("th", { scope: "col" }, "Line")].concat(t.names.map(function (n) { return CT.el("th", { scope: "col" }, n); }), [CT.el("th", { scope: "col" }, "Output")]))),
      CT.el("tbody", null, t.rows.slice(0, 200).map(function (row) {
        return CT.el("tr", null, [CT.el("td", null, String(row.line))].concat(t.names.map(function (n) {
          return CT.el("td", null, row.vals.hasOwnProperty(n) ? CT.pseudo.show(row.vals[n]) : "");
        }), [CT.el("td", null, row.out)]));
      }))]);
  }
  function inputsOf(text) { return String(text || "").split("\n").map(function (s) { return s.trim(); }).filter(function (s) { return s !== ""; }); }
  function countRun() { CT.store.state.stat.playground = (CT.store.state.stat.playground || 0) + 1; CT.store.save(); CT.emit("hud"); }

  // ------------------------------------------------------- the playground
  function playground(host) {
    var code = EXAMPLES[2].code, inputs = EXAMPLES[2].inputs || "", stepper = null, stepLine = null, vars = {}, output = [], error = null, showTrace = null, timer = null;
    var h1 = CT.el("h1", { tabindex: "-1" }, "⌨️ Pseudocode Playground");
    var page = CT.el("div", { class: "clab" });
    CT.append(host, [CT.el("header", { class: "ct-me-head" }, [CT.el("a", { class: "ct-back", href: "#/" }, "← Adventure map"), h1,
      CT.el("p", { class: "ct-lead" }, "Write pseudocode in the OCR style, run it, and step through it line by line. It runs safely inside this page and nothing you type is sent anywhere.")]), page]);

    function stop() { if (timer) clearTimeout(timer); timer = null; stepper = null; stepLine = null; }
    function render(focusSel) {
      CT.clear(page);
      var pick = CT.el("select", { "aria-label": "Load an example", onchange: function () {
        var ex = EXAMPLES[Number(this.value)]; if (!ex) return;
        stop(); code = ex.code; inputs = ex.inputs || ""; output = []; error = null; vars = {}; showTrace = null; render();
      } }, [CT.el("option", { value: "" }, "📂 Load an example…")].concat(EXAMPLES.map(function (e, i) { return CT.el("option", { value: String(i) }, e.name); })));
      var bar = CT.el("div", { class: "clab-bar" }, [pick,
        CT.el("button", { type: "button", class: "ct-btn ct-btn-go", onclick: runAll }, "▶ Run"),
        CT.el("button", { type: "button", class: "ct-btn ct-btn-soft", onclick: step }, stepper ? "⏭ Next line" : "⏭ Step through"),
        stepper ? CT.el("button", { type: "button", class: "ct-btn ct-btn-soft", onclick: function () { stop(); render(); } }, "⏹ Stop") : null,
        CT.el("button", { type: "button", class: "ct-btn ct-btn-soft", onclick: function () { showTrace = trace(code, inputsOf(inputs)); render(); } }, "📋 Trace table")]);
      var editor;
      if (stepper) editor = CT.el("div", { class: "clab-view" }, [CT.codeView(code, { mark: stepLine }), CT.el("p", { class: "clab-note" }, "Stepping: the highlighted line runs next. Stop to edit.")]);
      else {
        var nums = CT.el("pre", { class: "clab-nums", "aria-hidden": "true" }, code.split("\n").map(function (x, i) { return i + 1; }).join("\n"));
        var ta = CT.el("textarea", { class: "clab-ta", spellcheck: "false", autocapitalize: "off", "aria-label": "Your pseudocode", rows: String(Math.max(10, code.split("\n").length + 1)),
          oninput: function () { code = this.value; nums.textContent = code.split("\n").map(function (x, i) { return i + 1; }).join("\n"); },
          onscroll: function () { nums.scrollTop = this.scrollTop; },
          onkeydown: function (e) {
            if (e.key === "Tab" && !e.shiftKey) { e.preventDefault(); var s = this.selectionStart; this.setRangeText("    ", s, this.selectionEnd, "end"); code = this.value; }
          } }, code);
        editor = CT.el("div", { class: "clab-edit" }, [nums, ta]);
      }
      var inBox = CT.el("label", { class: "clab-inputs" }, [CT.el("span", null, "Test inputs, one per line"),
        CT.el("textarea", { rows: "3", spellcheck: "false", oninput: function () { inputs = this.value; } }, inputs)]);
      var outBox = CT.el("div", { class: "clab-out" }, [CT.el("p", { class: "ct-tray-h" }, "Output"),
        CT.el("pre", { "aria-live": "polite" }, output.join("\n") || " "),
        error ? CT.el("p", { class: "clab-err", role: "alert" }, "⚠ Line " + error.line + ": " + error.msg) : null]);
      var varBox = Object.keys(vars).length ? CT.el("div", { class: "clab-vars" }, [CT.el("p", { class: "ct-tray-h" }, "Variables now"),
        CT.el("table", { class: "cfl-table" }, CT.el("tbody", null, Object.keys(vars).map(function (k) {
          return CT.el("tr", null, [CT.el("th", { scope: "row" }, k), CT.el("td", null, CT.pseudo.show(vars[k]))]);
        })))]) : null;
      CT.append(page, [bar, CT.el("div", { class: "clab-grid" }, [CT.el("div", null, [editor, inBox]), CT.el("div", null, [outBox, varBox])]),
        showTrace ? CT.el("div", { class: "cfl-wrap clab-tracewrap" }, traceTable(showTrace)) : null, CT.guide()]);
      if (focusSel) { var f = page.querySelector(focusSel); if (f) f.focus(); }
    }
    function runAll() {
      stop();
      var r = CT.pseudo.run(code, { inputs: inputsOf(inputs), maxSteps: 20000 });
      output = r.output; error = r.error; vars = r.vars; showTrace = null;
      if (r.ok) { countRun(); CT.sound.play("good"); } else CT.sound.play("bad");
      render();
    }
    function step() {
      if (!stepper) { stepper = CT.pseudo.steps(code, { inputs: inputsOf(inputs), maxSteps: 20000 }); output = []; error = null; vars = {}; showTrace = null; }
      var r = stepper.next();
      output = r.output.slice(); vars = r.vars; error = r.error || null;
      if (r.done) { if (!r.error) countRun(); stepper = null; stepLine = null; CT.sound.play(r.error ? "bad" : "good"); }
      else { stepLine = r.line; CT.sound.play("step"); }
      render(stepper ? ".clab-bar .ct-btn-soft" : null);
    }
    render();
    setTimeout(function () { h1.focus({ preventScroll: true }); }, 30);
    return { destroy: stop };
  }

  // ------------------------------------------------------ the flowchart lab
  var seq = 0;
  function blk(kind, value, extra) { return Object.assign({ id: "b" + (++seq), kind: kind, value: value }, extra || {}); }
  var FLOW_EXAMPLES = [
    { name: "Adult or child ticket", inputs: "15", blocks: function () {
      return [blk("input", "age", { num: true }), blk("if", "age >= 18", { yes: [blk("output", '"Adult"')], no: [blk("output", '"Child"')] })];
    } },
    { name: "Count to 10", blocks: function () {
      return [blk("process", "count = 1"), blk("while", "count <= 10", { body: [blk("output", "count"), blk("process", "count = count + 1")] })];
    } },
    { name: "Times table", inputs: "7", blocks: function () {
      return [blk("input", "n", { num: true }), blk("process", "i = 1"), blk("while", "i <= 10", { body: [blk("output", "i * n"), blk("process", "i = i + 1")] })];
    } },
    { name: "Keep adding until over 20", inputs: "8\n5\n9\n4", blocks: function () {
      return [blk("process", "total = 0"), blk("until", "total > 20", { body: [blk("input", "x", { num: true }), blk("process", "total = total + x")] }), blk("output", "total")];
    } },
  ];
  var KIND = { input: ["▱", "Input"], output: ["▱", "Output"], process: ["▭", "Process"], if: ["◇", "If (decision)"], while: ["◇", "While loop"], until: ["◇", "Repeat until"] };
  function toFlow(blocks) {
    function conv(list) {
      return list.map(function (b) {
        var v = String(b.value || "").trim();
        if (b.kind === "input") return { id: b.id, t: "io", text: "Input " + (v || "?"), code: (v || "x") + " = " + (b.num ? "int(input())" : "input()") };
        if (b.kind === "output") return { id: b.id, t: "io", text: "Output " + (v || "?"), code: "print(" + (v || '""') + ")" };
        if (b.kind === "process") return { id: b.id, t: "process", text: v || "?", code: v || "// empty" };
        if (b.kind === "if") return { id: b.id, t: "decision", text: (v || "?") + "?", code: v || "true", yes: conv(b.yes), no: conv(b.no) };
        return { id: b.id, t: b.kind, text: (v || "?") + "?", code: v || "true", body: conv(b.body) };
      });
    }
    return [{ id: "start", t: "start", text: "Start" }].concat(conv(blocks), [{ id: "end", t: "end", text: "End" }]);
  }

  function flowLab(host) {
    var ex = FLOW_EXAMPLES[0], blocks = ex.blocks(), inputs = ex.inputs || "", into = null, on = null, output = [], error = null, timer = null, running = false;
    var h1 = CT.el("h1", { tabindex: "-1" }, "🔀 Flowchart Lab");
    var page = CT.el("div", { class: "clab" });
    CT.append(host, [CT.el("header", { class: "ct-me-head" }, [CT.el("a", { class: "ct-back", href: "#/" }, "← Adventure map"), h1,
      CT.el("p", { class: "ct-lead" }, "Build a flowchart from blocks and watch it drawn with the standard symbols. See the matching pseudocode, then run it step by step.")]), page]);

    function find(list, id, parent) {
      for (var i = 0; i < list.length; i++) {
        if (list[i].id === id) return { list: list, i: i, block: list[i] };
        var sub = ["yes", "no", "body"];
        for (var k = 0; k < sub.length; k++) if (list[i][sub[k]]) { var f = find(list[i][sub[k]], id); if (f) return f; }
      }
      return null;
    }
    function targetList() {
      if (!into) return blocks;
      var f = find(blocks, into.id);
      return f ? f.block[into.part] : blocks;
    }
    function add(kind) {
      var b = blk(kind, kind === "input" ? "x" : kind === "output" ? "x" : kind === "process" ? "x = x + 1" : "x < 10", kind === "input" ? { num: true } : null);
      if (kind === "if") { b.yes = []; b.no = []; }
      if (kind === "while" || kind === "until") b.body = [];
      targetList().push(b);
      stopRun(); render('[data-val="' + b.id + '"]');
    }
    function stopRun() { if (timer) clearTimeout(timer); timer = null; running = false; on = null; }

    function rowFor(b) {
      var f = function () { return find(blocks, b.id); };
      var li = CT.el("li", { class: "clab-blk clab-" + b.kind + (on === b.id ? " is-on" : "") }, [
        CT.el("span", { class: "clab-kind", title: KIND[b.kind][1] }, [CT.el("span", { "aria-hidden": "true" }, KIND[b.kind][0] + " "), KIND[b.kind][1]]),
        CT.el("input", { type: "text", class: "clab-val", value: b.value, "data-val": b.id, spellcheck: "false", "aria-label": KIND[b.kind][1] + (b.kind === "if" || b.kind === "while" || b.kind === "until" ? " condition" : ""),
          oninput: function () { b.value = this.value; stopRun(); draw(); } }),
        b.kind === "input" ? CT.el("label", { class: "clab-num" }, [CT.el("input", { type: "checkbox", checked: b.num ? true : null, onchange: function () { b.num = this.checked; draw(); } }), " number"]) : null,
        CT.el("span", { class: "clab-ops" }, [
          CT.el("button", { type: "button", "aria-label": "Move up", onclick: function () { var x = f(); if (x && x.i > 0) { x.list.splice(x.i - 1, 0, x.list.splice(x.i, 1)[0]); render(); } } }, "↑"),
          CT.el("button", { type: "button", "aria-label": "Move down", onclick: function () { var x = f(); if (x && x.i < x.list.length - 1) { x.list.splice(x.i + 1, 0, x.list.splice(x.i, 1)[0]); render(); } } }, "↓"),
          CT.el("button", { type: "button", "aria-label": "Delete", onclick: function () { var x = f(); if (x) { x.list.splice(x.i, 1); if (into && into.id === b.id) into = null; stopRun(); render(); } } }, "✕")])
      ]);
      ["yes", "no", "body"].forEach(function (part) {
        if (!b[part]) return;
        var name = part === "yes" ? "Yes branch" : part === "no" ? "No branch" : "Loop body";
        var active = into && into.id === b.id && into.part === part;
        li.appendChild(CT.el("div", { class: "clab-sub" + (active ? " is-into" : "") }, [
          CT.el("button", { type: "button", class: "clab-subh", "aria-pressed": active ? "true" : "false", onclick: function () { into = active ? null : { id: b.id, part: part }; render(); } },
            name + (active ? " (adding here)" : ": add here")),
          CT.el("ol", { class: "clab-list" }, b[part].map(rowFor))]));
      });
      return li;
    }
    var chartBox, codeBox;
    function draw() {
      var flow = toFlow(blocks), c = CT.flow.code(flow);
      chartBox.innerHTML = CT.flow.svg(flow, { on: on, label: "Your flowchart" });
      CT.clear(codeBox).appendChild(CT.codeView(c.text || "// add some blocks"));
    }
    function render(focusSel) {
      CT.clear(page);
      var pick = CT.el("select", { "aria-label": "Load an example", onchange: function () {
        var e = FLOW_EXAMPLES[Number(this.value)]; if (!e) return;
        stopRun(); blocks = e.blocks(); inputs = e.inputs || ""; into = null; output = []; error = null; render();
      } }, [CT.el("option", { value: "" }, "📂 Load an example…")].concat(FLOW_EXAMPLES.map(function (e, i) { return CT.el("option", { value: String(i) }, e.name); })));
      var addBar = CT.el("div", { class: "clab-add", role: "group", "aria-label": "Add a block" }, [CT.el("p", { class: "ct-tray-h" }, into ? "Add inside the chosen branch" : "Add a block")]
        .concat(["input", "output", "process", "if", "while", "until"].map(function (k) {
          return CT.el("button", { type: "button", class: "cdz-move", onclick: function () { add(k); } }, [CT.el("span", { "aria-hidden": "true" }, KIND[k][0]), KIND[k][1]]);
        })));
      var list = CT.el("ol", { class: "clab-list clab-main" }, blocks.length ? blocks.map(rowFor) : [CT.el("li", { class: "cpg-empty" }, "No blocks yet. Add one above.")]);
      chartBox = CT.el("div", { class: "cfb-chart" });
      codeBox = CT.el("div");
      var run = CT.el("div", { class: "clab-bar" }, [
        CT.el("button", { type: "button", class: "ct-btn ct-btn-go", disabled: running ? true : null, onclick: function () { play(false); } }, "▶ Run"),
        CT.el("button", { type: "button", class: "ct-btn ct-btn-soft", onclick: function () { play(true); } }, running ? "⏸ Pause" : "⏭ Step"),
        CT.el("button", { type: "button", class: "ct-btn ct-btn-soft", onclick: function () { stopRun(); stepper = null; output = []; error = null; render(); } }, "⏹ Reset")]);
      var inBox = CT.el("label", { class: "clab-inputs" }, [CT.el("span", null, "Test inputs, one per line"),
        CT.el("textarea", { rows: "3", spellcheck: "false", oninput: function () { inputs = this.value; } }, inputs)]);
      var outBox = CT.el("div", { class: "clab-out" }, [CT.el("p", { class: "ct-tray-h" }, "Output"), CT.el("pre", { "aria-live": "polite" }, output.join("\n") || " "),
        error ? CT.el("p", { class: "clab-err", role: "alert" }, "⚠ " + error.msg) : null]);
      CT.append(page, [CT.el("div", { class: "clab-bar" }, [pick]), CT.el("div", { class: "clab-grid" }, [
        CT.el("div", null, [CT.el("p", { class: "ct-tray-h" }, "Your blocks"), addBar, list]),
        CT.el("div", null, [chartBox, run, inBox, outBox, CT.el("p", { class: "ct-tray-h" }, "The same algorithm in pseudocode"), codeBox])])]);
      draw();
      if (focusSel) { var f = page.querySelector(focusSel); if (f) { f.focus(); if (f.select) f.select(); } }
    }
    var stepper = null, map = null;
    function play(single) {
      if (running && single) { stopRun(); render(); return; }
      if (!stepper) {
        var c = CT.flow.code(toFlow(blocks));
        var p = CT.pseudo.parse(c.text);
        if (!p.ok) { error = { msg: "The pseudocode does not work yet: " + p.error.msg }; render(); return; }
        stepper = CT.pseudo.steps(c.text, { inputs: inputsOf(inputs), maxSteps: 5000 }); map = c.map; output = []; error = null;
      }
      var tick = function () {
        var r = stepper.next();
        output = r.output.slice(); error = r.error || null;
        if (r.done) { stepper = null; on = null; running = false; render(); CT.sound.play(r.error ? "bad" : "good"); return; }
        on = map[r.line - 1];
        CT.sound.play("step");
        if (running) { draw(); refreshOut(); timer = CT.wait(450, tick); }
        else render();
      };
      if (single) tick();
      else { running = true; render(); tick(); }
    }
    function refreshOut() {
      var pre = page.querySelector(".clab-out pre");
      if (pre) pre.textContent = output.join("\n") || " ";
    }
    render();
    setTimeout(function () { h1.focus({ preventScroll: true }); }, 30);
    return { destroy: stopRun };
  }

  V.lab = function (host, name) {
    return name === "flowchart" ? flowLab(host) : playground(host);
  };
})(typeof window !== "undefined" ? window : globalThis);
