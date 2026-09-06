/* Trace table trainer: fill the table in, every cell is marked as you go. */
(function () {
  "use strict";

  function el(tag, cls, txt) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (txt !== undefined && txt !== null) n.textContent = txt;
    return n;
  }

  var EXERCISES = [
    {
      name: "Counting loop",
      code: [
        "total = 0",
        "for i = 1 to 4",
        "    total = total + i",
        "next i",
        "print total"
      ],
      prompt: "One row for each pass of the for loop.",
      cols: ["i", "total"],
      given: [],
      rows: [["1", "1"], ["2", "3"], ["3", "6"], ["4", "10"]],
      output: "10"
    },
    {
      name: "While loop halving",
      code: [
        "n = 40",
        "count = 0",
        "while n > 1",
        "    n = n DIV 2",
        "    count = count + 1",
        "endwhile",
        "print count"
      ],
      prompt: "The first row is the starting values. Add one row for each pass.",
      cols: ["n", "count"],
      given: [["40", "0"]],
      rows: [["20", "1"], ["10", "2"], ["5", "3"], ["2", "4"], ["1", "5"]],
      output: "5"
    },
    {
      name: "One pass of bubble sort",
      code: [
        "a = [5, 3, 8, 1]",
        "for i = 0 to 2",
        "    if a[i] > a[i + 1] then",
        "        temp = a[i]",
        "        a[i] = a[i + 1]",
        "        a[i + 1] = temp",
        "    endif",
        "next i"
      ],
      prompt: "Write the whole array as it stands at the end of each pass.",
      cols: ["i", "a[0]", "a[1]", "a[2]", "a[3]"],
      given: [["start", "5", "3", "8", "1"]],
      rows: [["0", "3", "5", "8", "1"], ["1", "3", "5", "8", "1"],
             ["2", "3", "5", "1", "8"]],
      output: ""
    },
    {
      name: "Binary to denary",
      code: [
        "num = 1101",
        "answer = 0",
        "power = 1",
        "while num > 0",
        "    digit = num MOD 10",
        "    answer = answer + digit * power",
        "    power = power * 2",
        "    num = num DIV 10",
        "endwhile",
        "print answer"
      ],
      prompt: "One row for each pass. MOD gives the remainder, DIV gives the whole "
        + "number part of a division.",
      cols: ["digit", "answer", "power", "num"],
      given: [["", "0", "1", "1101"]],
      rows: [["1", "1", "2", "110"], ["0", "1", "4", "11"],
             ["1", "5", "8", "1"], ["1", "13", "16", "0"]],
      output: "13"
    }
  ];

  function build(body) {
    body.textContent = "";

    var pick = el("div", "tool-btns");
    var buttons = [];
    EXERCISES.forEach(function (ex, i) {
      var b = el("button", "tool-btn" + (i === 0 ? " is-primary" : ""), ex.name);
      b.type = "button";
      b.setAttribute("aria-pressed", i === 0 ? "true" : "false");
      b.addEventListener("click", function () { load(i); });
      pick.appendChild(b);
      buttons.push(b);
    });
    body.appendChild(pick);

    var split = el("div", "tt-split");
    var left = el("div", "tt-left");
    var right = el("div", "tt-right");
    split.appendChild(left);
    split.appendChild(right);
    body.appendChild(split);

    var actions = el("div", "tool-btns");
    actions.style.marginTop = ".9rem";
    var bMark = el("button", "tool-btn is-primary", "Mark my table");
    var bShow = el("button", "tool-btn", "Show the answer");
    var bClear = el("button", "tool-btn", "Clear");
    [bMark, bShow, bClear].forEach(function (b) { b.type = "button"; });
    actions.appendChild(bMark);
    actions.appendChild(bShow);
    actions.appendChild(bClear);
    body.appendChild(actions);

    var status = el("p", "tool-status");
    body.appendChild(status);

    var cells = [], outInput = null, current = null;

    function norm(s) {
      return String(s === undefined || s === null ? "" : s)
        .trim().toLowerCase().replace(/\s+/g, "").replace(/,$/, "");
    }

    function markCell(inp) {
      var want = norm(inp.dataset.answer);
      var got = norm(inp.value);
      inp.classList.remove("is-good", "is-bad");
      if (got === "") return null;
      var ok = got === want;
      inp.classList.add(ok ? "is-good" : "is-bad");
      return ok;
    }

    function load(index) {
      current = EXERCISES[index];
      buttons.forEach(function (b, i) {
        b.classList.toggle("is-primary", i === index);
        b.setAttribute("aria-pressed", String(i === index));
      });

      left.textContent = "";
      var codeWrap = el("div", "tt-code");
      var pre = document.createElement("pre");
      var code = document.createElement("code");
      current.code.forEach(function (l, i) {
        var line = el("span", "tt-line");
        line.appendChild(el("span", "tt-num", String(i + 1).padStart(2, "0")));
        line.appendChild(document.createTextNode(l));
        code.appendChild(line);
        code.appendChild(document.createTextNode("\n"));
      });
      pre.appendChild(code);
      codeWrap.appendChild(pre);
      left.appendChild(codeWrap);
      left.appendChild(el("p", "tool-note", current.prompt));

      right.textContent = "";
      cells = [];
      var scroll = el("div", "tool-scroll");
      var table = document.createElement("table");
      var thead = document.createElement("thead");
      var hr = document.createElement("tr");
      current.cols.forEach(function (c) {
        var th = document.createElement("th");
        th.textContent = c;
        hr.appendChild(th);
      });
      thead.appendChild(hr);
      table.appendChild(thead);
      var tbody = document.createElement("tbody");

      current.given.forEach(function (row) {
        var tr = document.createElement("tr");
        tr.className = "tt-given";
        row.forEach(function (v) {
          var td = document.createElement("td");
          td.textContent = v;
          tr.appendChild(td);
        });
        tbody.appendChild(tr);
      });

      current.rows.forEach(function (row) {
        var tr = document.createElement("tr");
        row.forEach(function (v) {
          var td = document.createElement("td");
          var inp = document.createElement("input");
          inp.type = "text";
          inp.className = "tt-cell tool-mono";
          inp.autocomplete = "off";
          inp.spellcheck = false;
          inp.setAttribute("aria-label", "value");
          inp.dataset.answer = v;
          inp.addEventListener("blur", function () { markCell(inp); });
          td.appendChild(inp);
          tr.appendChild(td);
          cells.push(inp);
        });
        tbody.appendChild(tr);
      });
      table.appendChild(tbody);
      scroll.appendChild(table);
      right.appendChild(scroll);

      outInput = null;
      if (current.output) {
        var f = el("div", "tool-field");
        f.style.marginTop = ".8rem";
        var lab = el("label", null, "What does the algorithm print");
        var oi = document.createElement("input");
        oi.type = "text";
        oi.className = "tool-mono";
        oi.autocomplete = "off";
        oi.id = "tt-out-" + Math.random().toString(36).slice(2, 7);
        oi.dataset.answer = current.output;
        oi.addEventListener("blur", function () { markCell(oi); });
        lab.setAttribute("for", oi.id);
        f.appendChild(lab);
        f.appendChild(oi);
        right.appendChild(f);
        outInput = oi;
      }

      status.textContent = "";
      status.className = "tool-status";
    }

    bMark.addEventListener("click", function () {
      var all = cells.concat(outInput ? [outInput] : []);
      var right_ = 0, blank = 0;
      all.forEach(function (inp) {
        if (norm(inp.value) === "") { blank++; inp.classList.remove("is-good", "is-bad"); return; }
        if (markCell(inp)) right_++;
      });
      if (blank === all.length) {
        status.className = "tool-status";
        status.textContent = "Fill in at least one cell and then press mark.";
        return;
      }
      status.className = "tool-status " + (right_ === all.length ? "is-good" : "is-bad");
      status.textContent = right_ + " of " + all.length + " cells correct"
        + (blank ? ", and " + blank + " still blank." : ".")
        + (right_ === all.length
          ? " That is a full mark trace table."
          : " Red cells are wrong. Work down the algorithm one line at a time and write "
            + "the value the moment it changes.");
    });

    bShow.addEventListener("click", function () {
      cells.concat(outInput ? [outInput] : []).forEach(function (inp) {
        inp.value = inp.dataset.answer;
        inp.classList.remove("is-bad");
        inp.classList.add("is-good");
      });
      status.className = "tool-status";
      status.textContent = "That is the completed trace. Now try the next one with the "
        + "answer covered.";
    });

    bClear.addEventListener("click", function () {
      cells.concat(outInput ? [outInput] : []).forEach(function (inp) {
        inp.value = "";
        inp.classList.remove("is-good", "is-bad");
      });
      status.textContent = "";
      status.className = "tool-status";
    });

    load(0);
  }

  var mounts = document.querySelectorAll('.tool[data-tool="trace-table"] .tool-body');
  for (var i = 0; i < mounts.length; i++) build(mounts[i]);
})();
