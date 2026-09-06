/* File size calculator: image, sound and text, with every step shown. */
(function () {
  "use strict";

  function el(tag, cls, txt) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (txt !== undefined && txt !== null) n.textContent = txt;
    return n;
  }

  function uid() { return Math.random().toString(36).slice(2, 8); }

  function field(parent, label, value, min, step) {
    var f = el("div", "tool-field");
    var l = el("label", null, label);
    var i = document.createElement("input");
    i.type = "number";
    i.value = String(value);
    if (min !== undefined) i.min = String(min);
    if (step !== undefined) i.step = String(step);
    i.id = "fs-" + uid();
    l.setAttribute("for", i.id);
    f.appendChild(l);
    f.appendChild(i);
    parent.appendChild(f);
    return i;
  }

  function select(parent, label, options, value) {
    var f = el("div", "tool-field");
    var l = el("label", null, label);
    var s = document.createElement("select");
    options.forEach(function (o) {
      var opt = document.createElement("option");
      opt.value = String(o[0]);
      opt.textContent = o[1];
      s.appendChild(opt);
    });
    s.value = String(value);
    s.id = "fs-" + uid();
    l.setAttribute("for", s.id);
    f.appendChild(l);
    f.appendChild(s);
    parent.appendChild(f);
    return s;
  }

  function group(n) {
    /* thousands separators, so a seven digit bit count stays readable */
    var s = String(Math.round(n * 100) / 100).split(".");
    s[0] = s[0].replace(/\B(?=(\d{3})+(?!\d))/g, ",");
    return s.join(".");
  }

  function build(body) {
    body.textContent = "";

    var tabs = el("div", "tool-btns");
    var kinds = [["image", "Image"], ["sound", "Sound"], ["text", "Text"]];
    var buttons = {};
    kinds.forEach(function (k, idx) {
      var b = el("button", "tool-btn" + (idx === 0 ? " is-primary" : ""), k[1]);
      b.type = "button";
      b.setAttribute("aria-pressed", idx === 0 ? "true" : "false");
      tabs.appendChild(b);
      buttons[k[0]] = b;
    });
    body.appendChild(tabs);

    var panels = {};

    /* image */
    var pImg = el("div");
    pImg.style.marginTop = ".9rem";
    var iRow = el("div", "tool-row");
    var iW = field(iRow, "Width in pixels", 1920, 1, 1);
    var iH = field(iRow, "Height in pixels", 1080, 1, 1);
    var iD = select(iRow, "Colour depth", [
      [1, "1 bit, 2 colours"], [2, "2 bit, 4 colours"], [4, "4 bit, 16 colours"],
      [8, "8 bit, 256 colours"], [16, "16 bit, 65536 colours"],
      [24, "24 bit, 16.7 million colours"], [32, "32 bit, with transparency"]], 24);
    var iM = field(iRow, "Metadata in bytes", 0, 0, 1);
    pImg.appendChild(iRow);
    panels.image = pImg;

    /* sound */
    var pSnd = el("div");
    pSnd.style.marginTop = ".9rem";
    pSnd.hidden = true;
    var sRow = el("div", "tool-row");
    var sR = select(sRow, "Sample rate", [
      [8000, "8 kHz, telephone"], [22050, "22.05 kHz, speech"],
      [44100, "44.1 kHz, CD quality"], [48000, "48 kHz, video"],
      [96000, "96 kHz, studio"]], 44100);
    var sB = select(sRow, "Bit depth", [
      [8, "8 bit"], [16, "16 bit"], [24, "24 bit"], [32, "32 bit"]], 16);
    var sS = field(sRow, "Length in seconds", 180, 0, 1);
    var sC = select(sRow, "Channels", [[1, "1, mono"], [2, "2, stereo"]], 2);
    pSnd.appendChild(sRow);
    panels.sound = pSnd;

    /* text */
    var pTxt = el("div");
    pTxt.style.marginTop = ".9rem";
    pTxt.hidden = true;
    var tRow = el("div", "tool-row");
    var tN = field(tRow, "Number of characters", 5000, 0, 1);
    var tB = select(tRow, "Character set", [
      [7, "ASCII, 7 bits"], [8, "Extended ASCII, 8 bits"],
      [16, "Unicode UTF-16, 16 bits"]], 8);
    pTxt.appendChild(tRow);
    panels.text = pTxt;

    body.appendChild(pImg);
    body.appendChild(pSnd);
    body.appendChild(pTxt);

    var answer = el("p", "tool-status is-good");
    answer.style.fontSize = "1.05rem";
    body.appendChild(answer);
    var working = el("div", "tool-working");
    body.appendChild(working);
    var note = el("p", "tool-note",
      "Exam boards accept 1 kilobyte as 1000 bytes or as 1024 bytes. This calculator "
      + "divides by 1000, which is what OCR and AQA use in their mark schemes. Say "
      + "which one you have used and you will not lose the mark.");
    body.appendChild(note);

    var mode = "image";

    function line(label, value) {
      var d = el("div");
      d.appendChild(el("span", "step-op", label + " "));
      d.appendChild(el("b", null, value));
      return d;
    }

    function render(steps, finalText) {
      working.textContent = "";
      steps.forEach(function (s) { working.appendChild(s); });
      answer.textContent = finalText;
    }

    function unitChain(bits, steps) {
      var bytes = bits / 8;
      var kb = bytes / 1000;
      var mb = kb / 1000;
      var gb = mb / 1000;
      steps.push(line("Bits to bytes, divide by 8:",
        group(bits) + " / 8 = " + group(bytes) + " bytes"));
      steps.push(line("Bytes to kilobytes, divide by 1000:",
        group(bytes) + " / 1000 = " + group(kb) + " KB"));
      if (kb >= 1000) {
        steps.push(line("Kilobytes to megabytes, divide by 1000:",
          group(kb) + " / 1000 = " + group(mb) + " MB"));
      }
      if (mb >= 1000) {
        steps.push(line("Megabytes to gigabytes, divide by 1000:",
          group(mb) + " / 1000 = " + group(gb) + " GB"));
      }
      if (gb >= 1) return group(gb) + " GB";
      if (mb >= 1) return group(mb) + " MB";
      if (kb >= 1) return group(kb) + " KB";
      return group(bytes) + " bytes";
    }

    function calc() {
      var steps = [], bits = 0, best;
      if (mode === "image") {
        var w = Math.max(0, +iW.value || 0), h = Math.max(0, +iH.value || 0);
        var d = +iD.value, meta = Math.max(0, +iM.value || 0);
        steps.push(line("Formula:", "width x height x colour depth"));
        steps.push(line("Substitute:", w + " x " + h + " x " + d + " bits"));
        steps.push(line("Pixels:", group(w * h)));
        bits = w * h * d;
        steps.push(line("Image data:", group(bits) + " bits"));
        if (meta > 0) {
          steps.push(line("Metadata:", group(meta) + " bytes, which is "
            + group(meta * 8) + " bits"));
          bits += meta * 8;
          steps.push(line("Total:", group(bits) + " bits"));
        }
        best = unitChain(bits, steps);
        answer.textContent = "That image is " + best + ".";
      } else if (mode === "sound") {
        var r = +sR.value, bd = +sB.value, sec = Math.max(0, +sS.value || 0), ch = +sC.value;
        steps.push(line("Formula:", "sample rate x bit depth x seconds x channels"));
        steps.push(line("Substitute:", group(r) + " x " + bd + " x " + sec + " x " + ch));
        steps.push(line("One second of one channel:", group(r * bd) + " bits"));
        bits = r * bd * sec * ch;
        steps.push(line("All channels, whole length:", group(bits) + " bits"));
        best = unitChain(bits, steps);
        answer.textContent = "That recording is " + best + ".";
      } else {
        var n = Math.max(0, +tN.value || 0), cb = +tB.value;
        steps.push(line("Formula:", "characters x bits per character"));
        steps.push(line("Substitute:", group(n) + " x " + cb));
        bits = n * cb;
        steps.push(line("Text data:", group(bits) + " bits"));
        best = unitChain(bits, steps);
        answer.textContent = "That text is " + best + ".";
      }
      render(steps, answer.textContent);
    }

    [iW, iH, iD, iM, sR, sB, sS, sC, tN, tB].forEach(function (c) {
      c.addEventListener("input", calc);
      c.addEventListener("change", calc);
    });

    kinds.forEach(function (k) {
      buttons[k[0]].addEventListener("click", function () {
        mode = k[0];
        kinds.forEach(function (o) {
          var on = o[0] === mode;
          panels[o[0]].hidden = !on;
          buttons[o[0]].setAttribute("aria-pressed", String(on));
          buttons[o[0]].classList.toggle("is-primary", on);
        });
        calc();
      });
    });

    calc();
  }

  var mounts = document.querySelectorAll('.tool[data-tool="file-size"] .tool-body');
  for (var i = 0; i < mounts.length; i++) build(mounts[i]);
})();
