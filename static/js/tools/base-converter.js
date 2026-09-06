/* Number base converter with full working and a practice mode. */
(function () {
  "use strict";

  var HEX = "0123456789ABCDEF";

  function el(tag, cls, txt) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (txt !== undefined && txt !== null) n.textContent = txt;
    return n;
  }

  function toBin(n, pad) {
    var s = n.toString(2);
    while (s.length < pad) s = "0" + s;
    return s;
  }

  function toHex(n, pad) {
    var s = n.toString(16).toUpperCase();
    while (s.length < pad) s = "0" + s;
    return s;
  }

  /* ------------------------------------------------------------ working */

  function denaryToBinaryWorking(n) {
    var out = [];
    out.push("Take away the biggest place value you can, then move right.");
    var left = n, places = [];
    var p = 1;
    while (p * 2 <= Math.max(n, 1)) p *= 2;
    if (p < 128) p = 128;
    while (p >= 1) {
      if (left >= p) {
        out.push(p + " fits into " + left + ", so write 1. " + left + " - " + p +
                 " = " + (left - p));
        left -= p;
        places.push("1");
      } else {
        out.push(p + " does not fit into " + left + ", so write 0.");
        places.push("0");
      }
      p = p / 2;
    }
    out.push("Reading the column answers gives " + places.join("") + ".");
    return out;
  }

  function binaryToDenaryWorking(bits) {
    var out = [], total = 0, terms = [];
    var n = bits.length;
    out.push("Write the place values above the bits, then add up every column "
             + "holding a 1.");
    for (var i = 0; i < n; i++) {
      var place = Math.pow(2, n - 1 - i);
      if (bits.charAt(i) === "1") {
        total += place;
        terms.push(String(place));
      }
    }
    out.push("Place values: " + Array.from({ length: n }, function (_, i) {
      return Math.pow(2, n - 1 - i);
    }).join("  "));
    out.push("Bits:         " + bits.split("").join("  "));
    out.push(terms.length ? terms.join(" + ") + " = " + total
                          : "No column holds a 1, so the total is 0.");
    return out;
  }

  function denaryToHexWorking(n) {
    var out = [];
    var bin = toBin(n, 8);
    var hi = bin.slice(0, bin.length - 4), lo = bin.slice(-4);
    out.push("Split the binary into groups of four bits from the right, then "
             + "convert each group on its own.");
    out.push("Binary: " + bin);
    out.push("Groups: " + hi + " and " + lo);
    out.push(hi + " is " + parseInt(hi, 2) + ", which is " + HEX.charAt(parseInt(hi, 2))
             + " in hex.");
    out.push(lo + " is " + parseInt(lo, 2) + ", which is " + HEX.charAt(parseInt(lo, 2))
             + " in hex.");
    out.push("So the answer is " + toHex(n, 2) + ".");
    out.push("Checking the other way: " + HEX.indexOf(toHex(n, 2).charAt(0)) + " x 16 + "
             + HEX.indexOf(toHex(n, 2).charAt(1)) + " = " + n + ".");
    return out;
  }

  /* --------------------------------------------------------------- build */

  function build(body) {
    body.textContent = "";

    var tabs = el("div", "tool-btns");
    var bConvert = el("button", "tool-btn is-primary", "Convert");
    var bPractice = el("button", "tool-btn", "Practice");
    bConvert.type = bPractice.type = "button";
    bConvert.setAttribute("aria-pressed", "true");
    bPractice.setAttribute("aria-pressed", "false");
    tabs.appendChild(bConvert);
    tabs.appendChild(bPractice);
    body.appendChild(tabs);

    /* ---- convert panel ---- */
    var panel = el("div", "bc-panel");
    panel.style.marginTop = ".9rem";
    var row = el("div", "tool-row");
    var fields = {};
    [["den", "Denary", "text"], ["bin", "Binary", "text"], ["hex", "Hexadecimal", "text"]]
      .forEach(function (spec) {
        var f = el("div", "tool-field");
        var lab = el("label", null, spec[1]);
        var inp = document.createElement("input");
        inp.type = spec[2];
        inp.id = "bc-" + spec[0] + "-" + Math.random().toString(36).slice(2, 7);
        inp.className = "tool-mono";
        inp.autocomplete = "off";
        inp.spellcheck = false;
        lab.setAttribute("for", inp.id);
        f.appendChild(lab);
        f.appendChild(inp);
        row.appendChild(f);
        fields[spec[0]] = inp;
      });
    panel.appendChild(row);

    var bits = el("div", "tool-row");
    bits.style.marginTop = ".7rem";
    var bitsField = el("div", "tool-field");
    var bitsLab = el("label", null, "Number of bits");
    var bitsSel = document.createElement("select");
    [8, 16].forEach(function (n) {
      var o = document.createElement("option");
      o.value = String(n);
      o.textContent = n + " bit";
      bitsSel.appendChild(o);
    });
    bitsSel.id = "bc-bits-" + Math.random().toString(36).slice(2, 7);
    bitsLab.setAttribute("for", bitsSel.id);
    bitsField.appendChild(bitsLab);
    bitsField.appendChild(bitsSel);
    bits.appendChild(bitsField);
    panel.appendChild(bits);

    var status = el("p", "tool-status");
    panel.appendChild(status);
    var working = el("div", "tool-working");
    panel.appendChild(working);
    body.appendChild(panel);

    function showWorking(lines) {
      working.textContent = "";
      lines.forEach(function (l) {
        var d = el("div", null, l);
        working.appendChild(d);
      });
    }

    function width() { return parseInt(bitsSel.value, 10); }
    function maxVal() { return Math.pow(2, width()) - 1; }

    function setAll(n, from) {
      var w = width();
      if (from !== "den") fields.den.value = String(n);
      if (from !== "bin") fields.bin.value = toBin(n, w);
      if (from !== "hex") fields.hex.value = toHex(n, w / 4);
      status.className = "tool-status is-good";
      status.textContent = n + " in denary is " + toBin(n, w) + " in binary and "
        + toHex(n, w / 4) + " in hexadecimal.";
      var lines = denaryToBinaryWorking(n)
        .concat([" "])
        .concat(denaryToHexWorking(n));
      if (n > 255) lines = binaryToDenaryWorking(toBin(n, w));
      showWorking(lines);
    }

    function bad(msg) {
      status.className = "tool-status is-bad";
      status.textContent = msg;
      working.textContent = "";
    }

    fields.den.addEventListener("input", function () {
      var v = fields.den.value.trim();
      if (v === "") { status.textContent = ""; working.textContent = ""; return; }
      if (!/^\d+$/.test(v)) return bad("Denary uses the digits 0 to 9 only.");
      var n = parseInt(v, 10);
      if (n > maxVal()) return bad("That is bigger than " + maxVal()
        + ", which is the largest value " + width() + " bits can hold.");
      setAll(n, "den");
    });

    fields.bin.addEventListener("input", function () {
      var v = fields.bin.value.trim().replace(/\s+/g, "");
      if (v === "") { status.textContent = ""; working.textContent = ""; return; }
      if (!/^[01]+$/.test(v)) return bad("Binary uses the digits 0 and 1 only.");
      if (v.length > width()) return bad("That is more than " + width() + " bits.");
      var n = parseInt(v, 2);
      fields.den.value = String(n);
      fields.hex.value = toHex(n, width() / 4);
      status.className = "tool-status is-good";
      status.textContent = v + " in binary is " + n + " in denary and "
        + toHex(n, width() / 4) + " in hexadecimal.";
      showWorking(binaryToDenaryWorking(toBin(n, width())));
    });

    fields.hex.addEventListener("input", function () {
      var v = fields.hex.value.trim().toUpperCase().replace(/^0X/, "");
      if (v === "") { status.textContent = ""; working.textContent = ""; return; }
      if (!/^[0-9A-F]+$/.test(v)) return bad("Hexadecimal uses 0 to 9 and A to F only.");
      if (v.length > width() / 4) return bad("That is more than " + (width() / 4)
        + " hex digits.");
      var n = parseInt(v, 16);
      fields.den.value = String(n);
      fields.bin.value = toBin(n, width());
      status.className = "tool-status is-good";
      status.textContent = v + " in hexadecimal is " + n + " in denary and "
        + toBin(n, width()) + " in binary.";
      var lines = ["Convert each hex digit into four bits, then join them up."];
      v.split("").forEach(function (c) {
        lines.push(c + " is " + HEX.indexOf(c) + ", which is " + toBin(HEX.indexOf(c), 4)
                   + " in binary.");
      });
      lines.push("Joined together that is " + toBin(n, width()) + ".");
      var terms = [], powr = v.length - 1;
      v.split("").forEach(function (c) {
        terms.push(HEX.indexOf(c) + " x " + Math.pow(16, powr));
        powr--;
      });
      lines.push("In denary: " + terms.join(" + ") + " = " + n + ".");
      showWorking(lines);
    });

    bitsSel.addEventListener("change", function () {
      fields.den.dispatchEvent(new Event("input"));
    });

    /* ---- practice panel ---- */
    var practice = el("div", "bc-practice");
    practice.hidden = true;
    practice.style.marginTop = ".9rem";
    var qLine = el("p", "tool-label", "Question");
    var qText = el("p", null, "");
    qText.style.fontSize = "1.05rem";
    qText.style.fontWeight = "600";
    qText.style.margin = ".2rem 0 .8rem";
    var ansRow = el("div", "tool-row");
    var ansField = el("div", "tool-field");
    var ansLab = el("label", null, "Your answer");
    var ansInp = document.createElement("input");
    ansInp.type = "text";
    ansInp.className = "tool-mono";
    ansInp.autocomplete = "off";
    ansInp.spellcheck = false;
    ansInp.id = "bc-ans-" + Math.random().toString(36).slice(2, 7);
    ansLab.setAttribute("for", ansInp.id);
    ansField.appendChild(ansLab);
    ansField.appendChild(ansInp);
    var checkBtn = el("button", "tool-btn is-primary", "Check");
    checkBtn.type = "button";
    var nextBtn = el("button", "tool-btn", "New question");
    nextBtn.type = "button";
    var btnWrap = el("div", "tool-btns");
    btnWrap.appendChild(checkBtn);
    btnWrap.appendChild(nextBtn);
    ansRow.appendChild(ansField);
    ansRow.appendChild(btnWrap);
    var pStatus = el("p", "tool-status");
    var pWorking = el("div", "tool-working");
    var score = el("p", "tool-note", "Score 0 out of 0");
    practice.appendChild(qLine);
    practice.appendChild(qText);
    practice.appendChild(ansRow);
    practice.appendChild(pStatus);
    practice.appendChild(pWorking);
    practice.appendChild(score);
    body.appendChild(practice);

    var current = null, right = 0, asked = 0;

    function newQuestion() {
      var kinds = ["den2bin", "bin2den", "den2hex", "hex2den", "bin2hex", "hex2bin"];
      var kind = kinds[Math.floor(Math.random() * kinds.length)];
      var n = Math.floor(Math.random() * 256);
      var q, a;
      if (kind === "den2bin") { q = "Convert " + n + " into 8 bit binary."; a = toBin(n, 8); }
      else if (kind === "bin2den") { q = "Convert " + toBin(n, 8) + " into denary."; a = String(n); }
      else if (kind === "den2hex") { q = "Convert " + n + " into hexadecimal."; a = toHex(n, 2); }
      else if (kind === "hex2den") { q = "Convert " + toHex(n, 2) + " into denary."; a = String(n); }
      else if (kind === "bin2hex") { q = "Convert " + toBin(n, 8) + " into hexadecimal."; a = toHex(n, 2); }
      else { q = "Convert " + toHex(n, 2) + " into 8 bit binary."; a = toBin(n, 8); }
      current = { n: n, kind: kind, answer: a };
      qText.textContent = q;
      ansInp.value = "";
      ansInp.className = "tool-mono";
      pStatus.textContent = "";
      pStatus.className = "tool-status";
      pWorking.textContent = "";
      ansInp.focus();
    }

    function check() {
      if (!current) return;
      var given = ansInp.value.trim().toUpperCase().replace(/\s+/g, "").replace(/^0X/, "");
      if (given === "") return;
      asked++;
      var want = current.answer;
      var ok = given === want
        || (/^\d+$/.test(want) && /^\d+$/.test(given) && parseInt(given, 10) === parseInt(want, 10))
        || (current.kind === "den2bin" || current.kind === "hex2bin"
            ? parseInt(given, 2) === current.n && /^[01]+$/.test(given)
            : false)
        || (current.kind === "den2hex" || current.kind === "bin2hex"
            ? /^[0-9A-F]+$/.test(given) && parseInt(given, 16) === current.n
            : false);
      if (ok) {
        right++;
        pStatus.className = "tool-status is-good";
        pStatus.textContent = "Correct. The answer is " + want + ".";
        ansInp.className = "tool-mono is-good";
      } else {
        pStatus.className = "tool-status is-bad";
        pStatus.textContent = "Not quite. The answer is " + want + ".";
        ansInp.className = "tool-mono is-bad";
      }
      var lines;
      if (current.kind === "den2bin") lines = denaryToBinaryWorking(current.n);
      else if (current.kind === "bin2den" || current.kind === "hex2bin")
        lines = binaryToDenaryWorking(toBin(current.n, 8));
      else lines = denaryToHexWorking(current.n);
      pWorking.textContent = "";
      lines.forEach(function (l) { pWorking.appendChild(el("div", null, l)); });
      score.textContent = "Score " + right + " out of " + asked;
    }

    checkBtn.addEventListener("click", check);
    nextBtn.addEventListener("click", newQuestion);
    ansInp.addEventListener("keydown", function (e) {
      if (e.key === "Enter") { e.preventDefault(); check(); }
    });

    function mode(isPractice) {
      panel.hidden = isPractice;
      practice.hidden = !isPractice;
      bConvert.setAttribute("aria-pressed", String(!isPractice));
      bPractice.setAttribute("aria-pressed", String(isPractice));
      bConvert.classList.toggle("is-primary", !isPractice);
      bPractice.classList.toggle("is-primary", isPractice);
      if (isPractice && !current) newQuestion();
    }
    bConvert.addEventListener("click", function () { mode(false); });
    bPractice.addEventListener("click", function () { mode(true); });

    fields.den.value = "90";
    fields.den.dispatchEvent(new Event("input"));
  }

  var mounts = document.querySelectorAll('.tool[data-tool="base-converter"] .tool-body');
  for (var i = 0; i < mounts.length; i++) build(mounts[i]);
})();
