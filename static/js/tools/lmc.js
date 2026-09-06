/* Little Man Computer: assemble, run and step through LMC programs. */
(function () {
  "use strict";

  var OPS = { ADD: 100, SUB: 200, STA: 300, LDA: 500, BRA: 600, BRZ: 700, BRP: 800 };
  var NOARG = { INP: 901, OUT: 902, OTP: 902, HLT: 0, COB: 0 };

  function el(tag, cls, txt) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (txt !== undefined && txt !== null) n.textContent = txt;
    return n;
  }

  var SAMPLES = [
    {
      name: "Add two numbers",
      code: [
        "// Reads two numbers and prints their total",
        "        INP",
        "        STA FIRST",
        "        INP",
        "        ADD FIRST",
        "        OUT",
        "        HLT",
        "FIRST   DAT"
      ].join("\n"),
      inputs: "7, 5"
    },
    {
      name: "Count down to zero",
      code: [
        "// Reads a number and prints it counting down to zero",
        "        INP",
        "        STA N",
        "LOOP    LDA N",
        "        OUT",
        "        SUB ONE",
        "        STA N",
        "        BRP LOOP",
        "        HLT",
        "N       DAT",
        "ONE     DAT 1"
      ].join("\n"),
      inputs: "5"
    },
    {
      name: "Larger of two numbers",
      code: [
        "// Reads two numbers and prints the larger one",
        "        INP",
        "        STA A",
        "        INP",
        "        STA B",
        "        SUB A",
        "        BRP BBIG",
        "        LDA A",
        "        OUT",
        "        HLT",
        "BBIG    LDA B",
        "        OUT",
        "        HLT",
        "A       DAT",
        "B       DAT"
      ].join("\n"),
      inputs: "12, 30"
    },
    {
      name: "Times table",
      code: [
        "// Reads a number and prints the first five multiples of it",
        "        INP",
        "        STA STEP",
        "LOOP    LDA TOTAL",
        "        ADD STEP",
        "        STA TOTAL",
        "        OUT",
        "        LDA COUNT",
        "        SUB ONE",
        "        STA COUNT",
        "        BRZ END",
        "        BRA LOOP",
        "END     HLT",
        "STEP    DAT",
        "TOTAL   DAT 0",
        "COUNT   DAT 5",
        "ONE     DAT 1"
      ].join("\n"),
      inputs: "3"
    }
  ];

  function assemble(src) {
    var lines = src.split("\n");
    var parsed = [], labels = {}, errors = [], addr = 0;

    lines.forEach(function (raw, i) {
      var line = raw.replace(/(\/\/|#|;).*$/, "").trim();
      if (!line) return;
      var parts = line.split(/\s+/);
      var label = null, mnem, operand = null;
      var head = parts[0].toUpperCase();
      if (!OPS[head] && !NOARG.hasOwnProperty(head) && head !== "DAT") {
        label = parts[0].toUpperCase();
        parts.shift();
      }
      if (!parts.length) {
        errors.push("Line " + (i + 1) + ": a label needs an instruction after it.");
        return;
      }
      mnem = parts[0].toUpperCase();
      operand = parts.length > 1 ? parts[1].toUpperCase().replace(/,$/, "") : null;
      if (!OPS[mnem] && !NOARG.hasOwnProperty(mnem) && mnem !== "DAT") {
        errors.push("Line " + (i + 1) + ": " + parts[0] + " is not an LMC instruction.");
        return;
      }
      if (addr > 99) {
        errors.push("Line " + (i + 1) + ": the program is longer than the 100 mailboxes.");
        return;
      }
      if (label) {
        if (labels.hasOwnProperty(label)) {
          errors.push("Line " + (i + 1) + ": the label " + label + " is used twice.");
        }
        labels[label] = addr;
      }
      parsed.push({ addr: addr, mnem: mnem, operand: operand, line: i + 1 });
      addr++;
    });

    var mem = [];
    for (var m = 0; m < 100; m++) mem.push(0);

    parsed.forEach(function (p) {
      if (p.mnem === "DAT") {
        mem[p.addr] = p.operand === null ? 0 : (parseInt(p.operand, 10) || 0);
        return;
      }
      if (NOARG.hasOwnProperty(p.mnem)) {
        if (p.operand !== null && p.mnem !== "HLT" && p.mnem !== "COB") {
          errors.push("Line " + p.line + ": " + p.mnem + " does not take an operand.");
        }
        mem[p.addr] = NOARG[p.mnem];
        return;
      }
      if (p.operand === null) {
        errors.push("Line " + p.line + ": " + p.mnem + " needs a mailbox or a label.");
        return;
      }
      var target;
      if (/^\d+$/.test(p.operand)) target = parseInt(p.operand, 10);
      else if (labels.hasOwnProperty(p.operand)) target = labels[p.operand];
      else {
        errors.push("Line " + p.line + ": there is no label called " + p.operand + ".");
        return;
      }
      if (target > 99) {
        errors.push("Line " + p.line + ": mailbox " + target + " does not exist.");
        return;
      }
      mem[p.addr] = OPS[p.mnem] + target;
    });

    return { mem: mem, errors: errors, labels: labels, used: parsed.length };
  }

  function build(body) {
    body.textContent = "";

    var top = el("div", "tool-row");
    var codeField = el("div", "tool-field");
    codeField.style.flex = "1 1 20rem";
    var codeLab = el("label", null, "LMC assembly");
    var code = document.createElement("textarea");
    code.rows = 14;
    code.spellcheck = false;
    code.id = "lmc-code-" + Math.random().toString(36).slice(2, 7);
    codeLab.setAttribute("for", code.id);
    codeField.appendChild(codeLab);
    codeField.appendChild(code);
    top.appendChild(codeField);

    var side = el("div", "lmc-side");
    var inField = el("div", "tool-field");
    var inLab = el("label", null, "Input queue, separated by commas");
    var inInp = document.createElement("input");
    inInp.type = "text";
    inInp.className = "tool-mono";
    inInp.id = "lmc-in-" + Math.random().toString(36).slice(2, 7);
    inLab.setAttribute("for", inInp.id);
    inField.appendChild(inLab);
    inField.appendChild(inInp);
    side.appendChild(inField);

    var regWrap = el("div", "lmc-regs");
    var regs = {};
    [["pc", "Program counter"], ["acc", "Accumulator"], ["mar", "MAR"],
     ["mdr", "MDR"], ["cir", "CIR"]].forEach(function (r) {
      var b = el("div", "lmc-reg");
      b.appendChild(el("span", "lmc-reg-name", r[1]));
      var v = el("b", "lmc-reg-val", "0");
      b.appendChild(v);
      regWrap.appendChild(b);
      regs[r[0]] = v;
    });
    side.appendChild(regWrap);

    var outLab = el("p", "tool-label", "Output");
    var outBox = el("div", "lmc-out", "");
    side.appendChild(outLab);
    side.appendChild(outBox);
    top.appendChild(side);
    body.appendChild(top);

    var btns = el("div", "tool-btns");
    btns.style.marginTop = ".8rem";
    var bAsm = el("button", "tool-btn is-primary", "Assemble");
    var bRun = el("button", "tool-btn", "Run");
    var bStep = el("button", "tool-btn", "Step");
    var bReset = el("button", "tool-btn", "Reset");
    [bAsm, bRun, bStep, bReset].forEach(function (b) { b.type = "button"; btns.appendChild(b); });
    var sampleSel = document.createElement("select");
    SAMPLES.forEach(function (s, i) {
      var o = document.createElement("option");
      o.value = String(i);
      o.textContent = s.name;
      sampleSel.appendChild(o);
    });
    sampleSel.setAttribute("aria-label", "Example program");
    btns.appendChild(sampleSel);
    body.appendChild(btns);

    var status = el("p", "tool-status");
    body.appendChild(status);

    var boxWrap = el("div", "tool-scroll");
    var boxes = el("div", "lmc-boxes");
    var cells = [];
    for (var i = 0; i < 100; i++) {
      var c = el("div", "lmc-box");
      c.appendChild(el("span", "lmc-addr", String(i).padStart(2, "0")));
      var v = el("b", "lmc-val", "000");
      c.appendChild(v);
      boxes.appendChild(c);
      cells.push({ wrap: c, val: v });
    }
    boxWrap.appendChild(boxes);
    body.appendChild(boxWrap);

    var mem = [], pc = 0, acc = 0, neg = false, halted = true, queue = [], out = [];
    var timer = null;

    function paint() {
      regs.pc.textContent = String(pc).padStart(2, "0");
      regs.acc.textContent = String(acc).padStart(3, "0");
      for (var k = 0; k < 100; k++) {
        var v = String(mem[k] === undefined ? 0 : mem[k]).padStart(3, "0");
        if (cells[k].val.textContent !== v) cells[k].val.textContent = v;
        cells[k].wrap.classList.toggle("is-pc", k === pc && !halted);
        cells[k].wrap.classList.toggle("is-used", (mem[k] || 0) !== 0);
      }
      outBox.textContent = out.length ? out.join("   ") : "nothing yet";
    }

    function say(msg, kind) {
      status.className = "tool-status" + (kind ? " " + kind : "");
      status.textContent = msg;
    }

    function doAssemble() {
      stop();
      var r = assemble(code.value);
      if (r.errors.length) {
        mem = r.mem;
        say(r.errors[0], "is-bad");
        halted = true;
        paint();
        return false;
      }
      mem = r.mem;
      pc = 0;
      acc = 0;
      neg = false;
      halted = false;
      out = [];
      queue = inInp.value.split(/[,\s]+/).filter(function (s) { return s !== ""; })
        .map(function (s) { return parseInt(s, 10) || 0; });
      say("Assembled into " + r.used + " mailboxes. Press run, or step to watch the "
        + "fetch decode execute cycle one instruction at a time.", "is-good");
      paint();
      return true;
    }

    function step() {
      if (halted) { say("The program has halted. Assemble it again to run it.", ""); return; }
      /* fetch */
      var instr = mem[pc] || 0;
      regs.mar.textContent = String(pc).padStart(2, "0");
      regs.mdr.textContent = String(instr).padStart(3, "0");
      regs.cir.textContent = String(instr).padStart(3, "0");
      pc = (pc + 1) % 100;
      /* decode */
      var op = Math.floor(instr / 100), arg = instr % 100;
      /* execute */
      if (instr === 0) {
        halted = true;
        say("HLT reached. The program has finished.", "is-good");
      } else if (op === 1) {
        acc = acc + (mem[arg] || 0);
        neg = false;
        if (acc > 999) acc = acc % 1000;
      } else if (op === 2) {
        acc = acc - (mem[arg] || 0);
        neg = acc < 0;
        if (acc < 0) acc = acc + 1000;
      } else if (op === 3) {
        mem[arg] = acc;
      } else if (op === 5) {
        acc = mem[arg] || 0;
        neg = false;
      } else if (op === 6) {
        pc = arg;
      } else if (op === 7) {
        if (acc === 0 && !neg) pc = arg;
      } else if (op === 8) {
        if (!neg) pc = arg;
      } else if (instr === 901) {
        if (!queue.length) {
          halted = true;
          say("The program asked for input but the queue is empty. Add more numbers "
            + "to the input queue and assemble again.", "is-bad");
        } else {
          acc = queue.shift();
          neg = false;
        }
      } else if (instr === 902) {
        out.push(acc);
      } else {
        halted = true;
        say("Mailbox " + String(pc - 1) + " holds " + String(instr).padStart(3, "0")
          + ", which is not an instruction.", "is-bad");
      }
      paint();
      if (halted) stop();
    }

    function stop() {
      if (timer) { clearInterval(timer); timer = null; }
      bRun.textContent = "Run";
    }

    bAsm.addEventListener("click", doAssemble);
    bStep.addEventListener("click", function () {
      if (halted && !mem.length) doAssemble();
      step();
    });
    bRun.addEventListener("click", function () {
      if (timer) { stop(); return; }
      if (halted) { if (!doAssemble()) return; }
      bRun.textContent = "Pause";
      var guard = 0;
      timer = setInterval(function () {
        step();
        guard++;
        if (guard > 5000) { stop(); say("Stopped after 5000 instructions. That "
          + "usually means the program is stuck in a loop with no way out.", "is-bad"); }
      }, 90);
    });
    bReset.addEventListener("click", function () { doAssemble(); });
    sampleSel.addEventListener("change", function () {
      var s = SAMPLES[parseInt(sampleSel.value, 10)];
      code.value = s.code;
      inInp.value = s.inputs;
      doAssemble();
    });

    code.value = SAMPLES[0].code;
    inInp.value = SAMPLES[0].inputs;
    for (var z = 0; z < 100; z++) mem.push(0);
    doAssemble();
  }

  var mounts = document.querySelectorAll('.tool[data-tool="lmc"] .tool-body');
  for (var i = 0; i < mounts.length; i++) build(mounts[i]);
})();
