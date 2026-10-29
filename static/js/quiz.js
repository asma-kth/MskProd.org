/* MskProd Computing - knowledge quiz engine and exam-style auto marker. */
(function () {
  "use strict";
  var store = window.MskStore || { get: function (k, f) { return f; }, set: function () {} };

  /* =====================================================================
     PART 1 - multiple choice knowledge check
     ===================================================================== */
  function updateScore(quiz) {
    var qs = quiz.querySelectorAll(".q");
    var answered = 0, right = 0;
    qs.forEach(function (q) {
      if (q.getAttribute("data-answered") === "1") {
        answered++;
        if (q.getAttribute("data-correct") === "1") right++;
      }
    });
    var total = qs.length;
    var pct = total ? Math.round((right / total) * 100) : 0;
    var scoreEl = quiz.querySelector("[data-score]");
    var barEl = quiz.querySelector(".scorebar i");
    var counter = quiz.querySelector("[data-counter]");
    if (counter) counter.textContent = answered + " of " + total + " answered";
    if (scoreEl) scoreEl.innerHTML = 'Score <span class="pct">' + right + " / " + total + "</span>";
    if (barEl) barEl.style.width = (total ? (right / total) * 100 : 0) + "%";

    if (answered === total && total > 0) {
      var done = quiz.querySelector("[data-quiz-done]");
      if (done && !done.getAttribute("data-shown")) {
        done.setAttribute("data-shown", "1");
        done.classList.add("show");
        done.className = "q-feedback show " + (pct >= 80 ? "good" : pct >= 50 ? "" : "bad");
        var msg;
        if (pct === 100) msg = "Full marks. Every one correct. That is exactly the level you need for the top grade. Move on to the exam-style questions below.";
        else if (pct >= 80) msg = "Strong work. Read the explanations for the ones you missed, then attempt the exam-style questions below.";
        else if (pct >= 50) msg = "A solid start. Go back over the explanation for the parts you got wrong, wait a day, then retake this quiz before moving on.";
        else msg = "This topic needs another pass. Re-read the explanation section by section, use the key terms table, then come back to this quiz tomorrow. Struggling first time is normal and it is how the knowledge sticks.";
        done.innerHTML = "<b>" + right + " out of " + total + " (" + pct + " per cent)</b>" + msg;
        var key = quiz.getAttribute("data-quiz-id");
        if (key) {
          var rec = store.get("quiz", {});
          // b keeps the best percentage ever scored, so retaking a quiz for
          // practice can never take back a pass (the AI certificate reads it).
          var prev = rec[key], prevBest = prev ? (prev.b != null ? prev.b : (prev.t ? Math.round(100 * prev.s / prev.t) : 0)) : 0;
          rec[key] = { s: right, t: total, d: Date.now(), b: Math.max(pct, prevBest) };
          store.set("quiz", rec);
        }
        if (window.MskCat) {
          if (pct === 100) window.MskCat.say("Full marks on that check. Nothing left to fix here, so go and try the exam-style questions.", "Pixel says");
          else if (pct >= 80) window.MskCat.say("Nice, " + right + " out of " + total + ". Read the two you missed carefully, that is where the grade lives.", "Pixel says");
          else window.MskCat.say("Do not worry about the score. Getting it wrong now, on your own, is much better than getting it wrong in the exam. Re-read and come back.", "Pixel says");
        }
      }
    }
  }

  function handleOption(opt) {
    var q = opt.closest(".q");
    if (!q || q.getAttribute("data-answered") === "1") return;
    var quiz = q.closest(".quiz");
    q.setAttribute("data-answered", "1");
    var correct = opt.getAttribute("data-correct") === "1";
    q.setAttribute("data-correct", correct ? "1" : "0");

    q.querySelectorAll(".opt").forEach(function (o) {
      o.classList.add("is-locked");
      o.querySelector("input").disabled = true;
      if (o.getAttribute("data-correct") === "1") o.classList.add("is-right");
      else if (o === opt) o.classList.add("is-wrong");
    });

    var fb = q.querySelector(".q-feedback");
    if (fb) {
      fb.className = "q-feedback show " + (correct ? "good" : "bad");
      fb.innerHTML = "<b>" + (correct ? "Correct" : "Not quite") + "</b>" + (fb.getAttribute("data-explain") || "");
    }
    updateScore(quiz);
  }

  document.addEventListener("click", function (e) {
    var opt = e.target.closest && e.target.closest(".opt");
    if (opt) handleOption(opt);
  });
  document.addEventListener("keydown", function (e) {
    if (e.key !== "Enter" && e.key !== " ") return;
    var opt = document.activeElement && document.activeElement.closest && document.activeElement.closest(".opt");
    if (opt) { e.preventDefault(); handleOption(opt); }
  });

  document.querySelectorAll("[data-quiz-reset]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var quiz = btn.closest(".quiz");
      quiz.querySelectorAll(".q").forEach(function (q) {
        q.removeAttribute("data-answered"); q.removeAttribute("data-correct");
        q.querySelectorAll(".opt").forEach(function (o) {
          o.classList.remove("is-right", "is-wrong", "is-picked", "is-locked");
          o.querySelector("input").disabled = false; o.querySelector("input").checked = false;
        });
        var fb = q.querySelector(".q-feedback"); if (fb) fb.className = "q-feedback";
      });
      var done = quiz.querySelector("[data-quiz-done]");
      if (done) { done.className = "q-feedback"; done.removeAttribute("data-shown"); done.innerHTML = ""; }
      updateScore(quiz);
      quiz.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  });

  document.querySelectorAll("[data-quiz-shuffle]").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var quiz = btn.closest(".quiz");
      quiz.querySelectorAll(".q-opts").forEach(function (list) {
        var kids = Array.prototype.slice.call(list.children);
        for (var i = kids.length - 1; i > 0; i--) {
          var j = Math.floor(Math.random() * (i + 1));
          list.appendChild(kids[j]); kids.splice(j, 1);
        }
        Array.prototype.slice.call(list.children).forEach(function (o, i) {
          var m = o.querySelector(".mark"); if (m) m.textContent = "ABCDEFGH"[i];
        });
      });
      if (btn.getAttribute("data-quiz-shuffle") !== "quiet") {
        var r = quiz.querySelector("[data-quiz-reset]"); if (r) r.click();
      }
    });
  });

  document.querySelectorAll(".quiz").forEach(updateScore);

  /* =====================================================================
     PART 2 - exam-style auto marker

     Written answers are marked against the mark scheme attached to each
     question. Every mark point carries a list of acceptable phrasings, and a
     point is awarded when the answer contains any one of them, allowing for
     plurals and common verb endings. The full mark scheme and a model answer
     are always revealed afterwards, and the student can override the machine
     mark, because a real examiner rewards correct wording the list has not
     anticipated.

     Closed questions are marked exactly: tick boxes, a tick per row of a
     table, answer boxes, and programs, which are run against the mark scheme
     by mskbuild/codemark.py under Pyodide.
     ===================================================================== */

  var SYNONYMS = {
    "cpu": ["processor", "central processing unit"],
    "processor": ["cpu", "central processing unit"],
    "ram": ["main memory", "primary memory", "random access memory"],
    "rom": ["read only memory"],
    "hdd": ["hard disk", "hard disk drive", "magnetic hard drive"],
    "ssd": ["solid state drive", "solid state"],
    "os": ["operating system"],
    "gui": ["graphical user interface"],
    "url": ["web address"],
    "ip": ["internet protocol"],
    "lan": ["local area network"],
    "wan": ["wide area network"],
    "isp": ["internet service provider"],
    "alu": ["arithmetic logic unit"],
    "cu": ["control unit"],
    "mar": ["memory address register"],
    "mdr": ["memory data register"],
    "pc": ["program counter"],
    "dbms": ["database management system"],
    "sql": ["structured query language"],
    "ide": ["integrated development environment"],
    "nea": ["non exam assessment", "coursework"],
    "loop": ["iteration", "repeat", "repetition"],
    "iteration": ["loop", "repeat", "repetition"],
    "selection": ["if statement", "condition", "conditional"],
    "quicker": ["faster", "quick", "fast", "speed"],
    "faster": ["quicker", "quick", "fast", "speed"]
  };

  function normalise(s) {
    return (" " + String(s || "").toLowerCase()
      .replace(/[‘’“”]/g, "'")
      .replace(/[^a-z0-9'+\-<>=\s]/g, " ")
      .replace(/\s+/g, " ") + " ");
  }
  function stem(w) {
    if (w.length > 5 && /(ies)$/.test(w)) return w.slice(0, -3) + "y";
    if (w.length > 4 && /(ing|ed)$/.test(w)) return w.replace(/(ing|ed)$/, "");
    if (w.length > 3 && /(es)$/.test(w) && !/(ss|us)$/.test(w)) return w.slice(0, -2);
    if (w.length > 3 && /s$/.test(w) && !/(ss|us)$/.test(w)) return w.slice(0, -1);
    return w;
  }
  function stemSet(text) {
    var set = {};
    normalise(text).trim().split(" ").forEach(function (w) { if (w) { set[w] = 1; set[stem(w)] = 1; } });
    return set;
  }
  /* Synonyms are followed one step only. loop and iteration list each other,
     so following them further went round in a circle until the stack ran out,
     and the question could never be marked. */
  function containsPhrase(answerNorm, answerStems, phrase, viaSynonym) {
    var p = normalise(phrase).trim();
    if (!p) return false;
    if (answerNorm.indexOf(" " + p + " ") > -1) return true;
    var words = p.split(" ");
    if (words.length === 1) {
      var w = words[0];
      if (answerStems[w] || answerStems[stem(w)]) return true;
      var syn = viaSynonym ? null : SYNONYMS[w];
      if (syn) { for (var i = 0; i < syn.length; i++) { if (containsPhrase(answerNorm, answerStems, syn[i], true)) return true; } }
      return false;
    }
    /* multi word: every word (stemmed) must be present somewhere in the answer */
    for (var j = 0; j < words.length; j++) {
      if (!answerStems[words[j]] && !answerStems[stem(words[j])]) return false;
    }
    return true;
  }
  function pointHit(answer, answerStems, phrases) {
    for (var i = 0; i < phrases.length; i++) {
      if (containsPhrase(answer, answerStems, phrases[i])) return true;
    }
    return false;
  }
  function parse(json, fallback) {
    try { return JSON.parse(json); } catch (e) { return fallback; }
  }

  /* ------------------------------------------------ written answers */
  function markText(examq) {
    // The answer box is the one directly inside the question. A figure or a model
    // answer can hold Python blocks, and each of those has an editor textarea of
    // its own that comes earlier in the page and must not be marked instead.
    var ta = examq.querySelector(":scope > textarea");
    var answer = normalise(ta.value);
    var stems = stemSet(ta.value);
    var words = ta.value.trim() ? ta.value.trim().split(/\s+/).length : 0;
    var awarded = 0;
    examq.querySelectorAll(".ms li").forEach(function (li) {
      var hit = words > 0 && pointHit(answer, stems, parse(li.getAttribute("data-any") || "[]", []));
      li.classList.toggle("hit", hit);
      if (hit) awarded++;
    });
    return { awarded: awarded, answered: words > 0 };
  }

  /* ------------------------------------------------ tick boxes */
  function markChoice(examq) {
    var inputs = examq.querySelectorAll(".xq-opts input");
    var keys = examq.querySelectorAll('.xq-opts input[data-c="1"]');
    var ticked = 0, right = 0;
    inputs.forEach(function (inp) {
      if (inp.checked) { ticked++; if (inp.getAttribute("data-c") === "1") right++; }
    });
    var tooMany = ticked > keys.length;
    examq.querySelectorAll(".ms li:not(.xq-rule)").forEach(function (li, k) {
      li.classList.toggle("hit", !tooMany && !!(keys[k] && keys[k].checked));
    });
    var rule = examq.querySelector(".ms li.xq-rule");
    if (rule) rule.classList.toggle("broken", tooMany);
    inputs.forEach(function (inp) {
      var lab = inp.closest(".xq-opt");
      lab.classList.toggle("is-right", inp.getAttribute("data-c") === "1");
      lab.classList.toggle("is-wrong", inp.checked && inp.getAttribute("data-c") !== "1");
    });
    return { awarded: tooMany ? 0 : right, answered: ticked > 0 };
  }

  /* ------------------------------------------------ one tick per row */
  function markMatrix(examq) {
    var ok = [], answered = false;
    examq.querySelectorAll(".xq-matrix tbody tr").forEach(function (tr) {
      var picked = tr.querySelector("input:checked");
      if (picked) answered = true;
      ok.push(!!(picked && picked.getAttribute("data-c") === "1"));
      tr.querySelectorAll("input").forEach(function (inp) {
        var cell = inp.closest("td");
        cell.classList.toggle("is-right", inp.getAttribute("data-c") === "1");
        cell.classList.toggle("is-wrong", inp.checked && inp.getAttribute("data-c") !== "1");
      });
    });
    var awarded = 0;
    examq.querySelectorAll(".ms li[data-rows]").forEach(function (li) {
      var hit = parse(li.getAttribute("data-rows"), []).every(function (r) { return ok[r]; });
      li.classList.toggle("hit", hit);
      if (hit) awarded++;
    });
    return { awarded: awarded, answered: answered };
  }

  /* ------------------------------------------------ answer boxes */
  function plainAnswer(s) {
    return String(s || "").toLowerCase()
      .replace(/[‘’]/g, "'").replace(/[“”]/g, '"')
      .replace(/\s+/g, " ").trim()
      .replace(/^["']+|["']+$/g, "").replace(/\.$/, "").trim()
      .replace(/^(the|a|an) /, "");
  }
  function blankRight(inp) {
    var raw = inp.value;
    if (!raw.trim()) return false;
    var accept = parse(inp.getAttribute("data-accept") || "[]", []);
    if (inp.getAttribute("data-numeric") === "1") {
      var m = String(raw).replace(/(\d),(?=\d{3}(\D|$))/g, "$1").match(/-?\d*\.?\d+(?:e[-+]?\d+)?/i);
      if (!m) return false;
      var x = parseFloat(m[0]);
      var tol = parseFloat(inp.getAttribute("data-tol") || "0");
      return accept.some(function (a) { return Math.abs(x - parseFloat(a)) <= tol + 1e-9; });
    }
    var given = plainAnswer(raw), squeezed = given.replace(/ /g, "");
    return accept.some(function (a) {
      var want = plainAnswer(a);
      return want === given || want.replace(/ /g, "") === squeezed;
    });
  }
  function markBlanks(examq) {
    var max = parseInt(examq.getAttribute("data-marks"), 10) || 1;
    var ok = [], answered = false;
    examq.querySelectorAll(".xq-blank").forEach(function (inp) {
      var right = blankRight(inp);
      if (inp.value.trim()) answered = true;
      ok[parseInt(inp.getAttribute("data-b"), 10)] = right;
      inp.classList.toggle("is-right", right);
      inp.classList.toggle("is-wrong", !right);
    });
    var finals = examq.querySelectorAll(".ms li[data-blanks]");
    var awarded = 0;
    finals.forEach(function (li) {
      var hit = parse(li.getAttribute("data-blanks"), []).every(function (b) { return ok[b]; });
      li.classList.toggle("hit", hit);
      if (hit) awarded++;
    });
    var working = examq.querySelector(".xq-working");
    if (working) {
      var methods = examq.querySelectorAll(".ms li[data-any]");
      if (finals.length && awarded === finals.length) {
        // a correct final answer earns full marks, as on the real mark scheme
        methods.forEach(function (li) { li.classList.add("hit"); });
        awarded = max;
      } else {
        var text = working.value, ans = normalise(text), stems = stemSet(text), found = 0;
        if (text.trim()) answered = true;
        methods.forEach(function (li) {
          var hit = !!text.trim() && pointHit(ans, stems, parse(li.getAttribute("data-any") || "[]", []));
          li.classList.toggle("hit", hit);
          if (hit) found++;
        });
        awarded = Math.min(max - 1, awarded + found);
      }
    }
    return { awarded: awarded, answered: answered };
  }

  /* ------------------------------------------------ programs */
  var cmReady = null;
  function codemark() {
    if (cmReady) return cmReady;
    if (!window.MskPython) return Promise.reject(new Error("no python"));
    var srcEl = document.getElementById("msk-codemark");
    cmReady = window.MskPython.boot(function () {}).then(function (py) {
      py.globals.set("__msk_cm_src", srcEl ? parse(srcEl.textContent, "") : "");
      /* SQL answers need sqlite3, built in to some Pyodide releases and a package in others. */
      var sqlite = document.querySelector('.xq-code[data-lang="sql"]') ?
        py.loadPackage("sqlite3").catch(function () {}) : Promise.resolve();
      py.runPython([
        "import sys, types",
        "__msk_codemark = types.ModuleType('mskcodemark')",
        "exec(__msk_cm_src, __msk_codemark.__dict__)",
        "sys.modules['mskcodemark'] = __msk_codemark"
      ].join("\n"));
      return sqlite.then(function () { return py; });
    });
    cmReady.catch(function () { cmReady = null; });
    return cmReady;
  }
  function markCode(examq) {
    var box = examq.querySelector(".xq-code");
    var src = box.querySelector(".xq-code-area").value;
    var starter = box.querySelector(".xq-starter").content.textContent;
    var checks = box.getAttribute("data-checks") || "[]";
    var files = box.getAttribute("data-files") || "{}";
    var lang = box.getAttribute("data-lang") || "python";
    var lis = examq.querySelectorAll(".ms li");
    var verdict = examq.querySelector("[data-verdict]");
    if (verdict) verdict.textContent = lang === "sql" ? "Running your SQL against the database." : "Running your program against the mark scheme.";
    return codemark().then(function (py) {
      py.globals.set("__msk_src", src);
      py.globals.set("__msk_checks", checks);
      py.globals.set("__msk_files", files);
      py.globals.set("__msk_lang", lang);
      py.globals.set("__msk_setup", box.getAttribute("data-setup") || "");
      var res = parse(py.runPython("__msk_codemark.mark_json(__msk_src, __msk_checks, __msk_files, __msk_lang, __msk_setup)"), []);
      var awarded = 0;
      lis.forEach(function (li, k) {
        var r = res[k] || [false, ""];
        li.classList.toggle("hit", !!r[0]);
        var why = li.querySelector(".xq-why");
        if (why) why.remove();
        if (!r[0] && r[1]) {
          why = document.createElement("span");
          why.className = "xq-why";
          why.textContent = "Not awarded: " + r[1] + ".";
          li.appendChild(why);
        }
        if (r[0]) awarded++;
      });
      return { awarded: awarded, answered: src.trim() !== starter.trim() };
    }, function () {
      lis.forEach(function (li) { li.classList.remove("hit"); });
      return { awarded: 0, answered: src.trim() !== starter.trim(), offline: true };
    });
  }

  var MARKERS = { text: markText, choice: markChoice, matrix: markMatrix, blanks: markBlanks, code: markCode };

  function verdictFor(kind, res, max) {
    if (res.offline) return "Python could not be loaded, so this program cannot be run and marked here. Compare it with the program in the mark scheme and give yourself the marks it earns.";
    if (!res.answered) return "You have not answered this yet. In the real exam a blank is a guaranteed zero, so always write something.";
    if (res.awarded >= max) return kind === "text" ? "That covers every mark point. Check the model answer as well, because how you order and link the points is what separates a top answer from an average one." : "Full marks.";
    if (kind === "code") return "Your program earned " + res.awarded + " of " + max + ". The unticked lines say what it does not do yet. Fix it and mark it again.";
    if (kind !== "text") return res.awarded ? "Part marks: " + res.awarded + " of " + max + ". The mark scheme below shows the answers that earn the rest." : "No marks this time. The mark scheme below shows the answer.";
    if (res.awarded >= Math.ceil(max / 2)) return "Part marks. You have the right idea but the answer is missing " + (max - res.awarded) + " mark point" + (max - res.awarded === 1 ? "" : "s") + ". The unticked lines below show exactly what to add.";
    return "The marker found " + res.awarded + " of " + max + ". Read the unticked mark points below, then close this and write the answer again from memory. Rewriting is what makes it stick.";
  }

  function record(examq, awarded, max, self) {
    var key = examq.getAttribute("data-exam-id");
    if (!key) return;
    var rec = store.get("exam", {});
    rec[key] = { s: awarded, t: max, d: Date.now() };
    if (self) rec[key].self = 1;
    store.set("exam", rec);
  }

  /* Marks one question and shows its mark scheme. Always returns a promise,
     because a program has to be run before it can be marked. */
  function markOne(examq) {
    var kind = examq.getAttribute("data-kind") || "text";
    var max = parseInt(examq.getAttribute("data-marks"), 10) || 1;
    var result = examq.querySelector(".examq-result");
    result.classList.add("show");
    return Promise.resolve((MARKERS[kind] || markText)(examq)).then(function (res) {
      var awarded = Math.min(res.awarded, max);
      examq.setAttribute("data-awarded", String(awarded));
      var award = result.querySelector(".award");
      if (award) award.textContent = awarded + " / " + max;
      var verdict = result.querySelector("[data-verdict]");
      if (verdict) verdict.textContent = verdictFor(kind, res, max);
      var sel = result.querySelector("[data-self]");
      if (sel) {
        sel.innerHTML = "";
        for (var i = 0; i <= max; i++) {
          var o = document.createElement("option");
          o.value = String(i); o.textContent = i + " / " + max;
          if (i === awarded) o.selected = true;
          sel.appendChild(o);
        }
      }
      record(examq, awarded, max, false);
      return { awarded: awarded, max: max };
    });
  }

  function clearOne(examq) {
    examq.querySelectorAll(":scope > textarea, .xq-working, .xq-blank").forEach(function (t) {
      t.value = ""; t.classList.remove("is-right", "is-wrong");
    });
    examq.querySelectorAll(".xq-opts input, .xq-matrix input").forEach(function (inp) { inp.checked = false; });
    examq.querySelectorAll(".is-right, .is-wrong").forEach(function (n) { n.classList.remove("is-right", "is-wrong"); });
    var box = examq.querySelector(".xq-code");
    if (box) {
      box.querySelector(".xq-code-area").value = box.querySelector(".xq-starter").content.textContent;
      var out = box.querySelector(".xq-code-out"); out.hidden = true; out.querySelector("code").textContent = "";
    }
    examq.removeAttribute("data-awarded");
    examq.querySelector(".examq-result").classList.remove("show");
  }

  function totalOf(wrap) {
    var got = 0, tot = 0;
    wrap.querySelectorAll(".examq").forEach(function (q) {
      var max = parseInt(q.getAttribute("data-marks"), 10) || 1;
      tot += max;
      var sel = q.querySelector("[data-self]");
      var a = q.getAttribute("data-awarded");
      if (a !== null) got += sel && sel.value !== "" ? parseInt(sel.value, 10) : parseInt(a, 10);
    });
    return { got: got, tot: tot };
  }

  function showTotal(wrap) {
    var t = totalOf(wrap);
    var sum = wrap.querySelector("[data-exam-total]");
    var pc = t.tot ? Math.round((t.got / t.tot) * 100) : 0;
    if (sum) sum.innerHTML = 'Machine mark <span class="pct">' + t.got + " / " + t.tot + "</span> (" + pc + " per cent)";
    var bar = wrap.querySelector("[data-exam-bar]");
    if (bar) bar.style.width = pc + "%";
    document.dispatchEvent(new CustomEvent("msk:exam-total", { detail: t }));
    return t;
  }

  function markAll(wrap) {
    var qs = Array.prototype.slice.call(wrap.querySelectorAll(".examq"));
    // One at a time, so that programs are run in order and the page stays responsive.
    return qs.reduce(function (chain, q) {
      return chain.then(function () { return markOne(q); });
    }, Promise.resolve()).then(function () {
      var t = showTotal(wrap);
      if (window.MskCat && t.tot) {
        var p = Math.round((t.got / t.tot) * 100);
        if (p >= 80) window.MskCat.say("That is top grade territory. Keep checking your answers against the model answers, they show you how to link points together.", "Pixel says");
        else if (p >= 45) window.MskCat.say("Middle of the range. The quickest gain is writing one extra sentence per question that says why, not just what.", "Pixel says");
        else window.MskCat.say("Exam answers are a skill you build, not a talent you have. Read every mark scheme line you missed, then try the paper again in a week.", "Pixel says");
      }
      return t;
    });
  }
  window.MskExam = { markAll: markAll, markOne: markOne, clearOne: clearOne };
  /* The same keyword marker for the stretch tasks' written rounds:
     which of a list of mark points (each a list of phrasings) an answer earns.
     mskbuild/stretchcheck.py is this marker in Python, used at build time. */
  window.MskMarker = {
    hits: function (text, points) {
      var has = !!String(text || "").trim(), a = normalise(text), s = stemSet(text);
      return points.map(function (p) { return has && pointHit(a, s, p); });
    }
  };

  document.addEventListener("click", function (e) {
    var b = e.target.closest && e.target.closest("[data-mark]");
    if (b) {
      var q = b.closest(".examq");
      markOne(q).then(function () { showTotal(q.closest("[data-exam-set]") || document); });
      return;
    }
    var r = e.target.closest && e.target.closest("[data-exam-reset]");
    if (r) {
      var eq = r.closest(".examq");
      clearOne(eq);
      var first = eq.querySelector(":scope > textarea, .xq-code-area, .xq-blank, input");
      if (first) first.focus();
      document.dispatchEvent(new CustomEvent("msk:exam-change"));
      return;
    }
    var all = e.target.closest && e.target.closest("[data-mark-all]");
    if (all) { markAll(all.closest("[data-exam-set]") || document); return; }

    var run = e.target.closest && e.target.closest("[data-code-run]");
    if (run) { runCode(run.closest(".xq-code"), run); return; }
    var back = e.target.closest && e.target.closest("[data-code-reset]");
    if (back) {
      var box = back.closest(".xq-code");
      box.querySelector(".xq-code-area").value = box.querySelector(".xq-starter").content.textContent;
      document.dispatchEvent(new CustomEvent("msk:exam-change"));
    }
  });

  /* A report link carries the page it came from, so the report names the
     exact paper or topic as well as the question. */
  document.addEventListener("click", function (e) {
    var a = e.target.closest && e.target.closest("[data-report]");
    if (a && a.href.indexOf("page=") < 0) a.href += "&page=" + encodeURIComponent(location.pathname);
  });

  function runCode(box, btn) {
    var out = box.querySelector(".xq-code-out"), code = out.querySelector("code");
    if (!window.MskPython) {
      out.hidden = false; code.textContent = "Python could not be loaded on this page.";
      return;
    }
    btn.disabled = true;
    out.hidden = false;
    out.classList.remove("is-error");
    code.textContent = "Starting Python.";
    var running;
    if (box.getAttribute("data-lang") === "sql") {
      running = codemark().then(function (py) {
        py.globals.set("__msk_src", box.querySelector(".xq-code-area").value);
        py.globals.set("__msk_setup", box.getAttribute("data-setup") || "");
        return parse(py.runPython("__msk_codemark.preview_json(__msk_src, __msk_setup)"), {});
      });
    } else {
      var feed = box.querySelector(".xq-code-in textarea").value.split("\n").filter(function (s, i, a) {
        return !(s === "" && i === a.length - 1);
      });
      running = window.MskPython.run(box.querySelector(".xq-code-area").value, feed,
                                     parse(box.getAttribute("data-files") || "{}", {}));
    }
    running.then(function (r) {
      code.textContent = r.output || (r.error ? "" : "The program ran without errors and printed nothing.");
      if (r.error) { code.textContent += (code.textContent ? "\n" : "") + r.error; out.classList.add("is-error"); }
      btn.disabled = false;
    }, function () {
      code.textContent = "Python could not be loaded, so the program cannot be run here.";
      btn.disabled = false;
    });
  }

  document.addEventListener("change", function (e) {
    var s = e.target.closest && e.target.closest("[data-self]");
    if (!s) return;
    var eq = s.closest(".examq");
    var award = eq.querySelector(".award");
    var max = parseInt(eq.getAttribute("data-marks"), 10) || 1;
    if (award) award.textContent = s.value + " / " + max;
    record(eq, parseInt(s.value, 10), max, true);
    showTotal(eq.closest("[data-exam-set]") || document);
  });

  /* keyboard shortcut: ctrl+enter marks the answer you are typing */
  document.addEventListener("keydown", function (e) {
    if (!(e.key === "Enter" && (e.ctrlKey || e.metaKey))) return;
    var eq = e.target.closest && e.target.closest(".examq");
    if (eq) { e.preventDefault(); markOne(eq).then(function () { showTotal(eq.closest("[data-exam-set]") || document); }); }
  });

  /* Tab in a code box indents instead of leaving the box, as an editor would. */
  document.addEventListener("keydown", function (e) {
    if (e.key !== "Tab" || e.shiftKey || !e.target.classList || !e.target.classList.contains("xq-code-area")) return;
    e.preventDefault();
    var t = e.target, a = t.selectionStart, b = t.selectionEnd;
    t.value = t.value.slice(0, a) + "    " + t.value.slice(b);
    t.selectionStart = t.selectionEnd = a + 4;
  });

  /* =====================================================================
     PART 3 - sitting a paper

     The bar at the top of a paper counts down from the real time allowed.
     Answers are saved on this device as they are typed, so a reload loses
     nothing, and the clock keeps running across reloads too. When the time
     is up, or the student finishes early, every answer is locked and the
     whole paper is marked.
     ===================================================================== */
  var bar = document.querySelector("[data-paper-bar]");
  if (bar) sitPaper(bar);

  function sitPaper(bar) {
    var slug = bar.getAttribute("data-paper");
    var mins = parseInt(bar.getAttribute("data-minutes"), 10) || 60;
    var wrap = document.querySelector("[data-exam-set]");
    if (!wrap) return;
    var clock = bar.querySelector("[data-pb-clock]");
    var bStart = bar.querySelector("[data-pb-start]");
    var bPause = bar.querySelector("[data-pb-pause]");
    var bFinish = bar.querySelector("[data-pb-finish]");
    var bAgain = bar.querySelector("[data-pb-again]");
    var done = bar.querySelector("[data-pb-done]");
    var score = bar.querySelector("[data-pb-score]");
    var questions = Array.prototype.slice.call(wrap.querySelectorAll(".examq"));
    var tick = null;

    function all() { return store.get("papers", {}); }
    function mine() { return all()[slug] || { a: {}, t: { used: 0, from: 0 }, done: 0 }; }
    function save(rec) { var p = all(); p[slug] = rec; store.set("papers", p); }

    function stateOf(q) {
      var kind = q.getAttribute("data-kind");
      if (kind === "choice" || kind === "matrix") {
        return Array.prototype.map.call(q.querySelectorAll("input"), function (i) { return i.checked ? 1 : 0; }).join("");
      }
      if (kind === "blanks") {
        var v = Array.prototype.map.call(q.querySelectorAll(".xq-blank"), function (i) { return i.value; });
        var w = q.querySelector(".xq-working");
        return JSON.stringify({ b: v, w: w ? w.value : "" });
      }
      if (kind === "code") return q.querySelector(".xq-code-area").value;
      return q.querySelector(":scope > textarea").value;
    }
    function restore(q, v) {
      var kind = q.getAttribute("data-kind");
      if (v === undefined || v === null) return;
      if (kind === "choice" || kind === "matrix") {
        q.querySelectorAll("input").forEach(function (i, k) { i.checked = v.charAt(k) === "1"; });
      } else if (kind === "blanks") {
        var o = parse(v, { b: [], w: "" });
        q.querySelectorAll(".xq-blank").forEach(function (i, k) { i.value = o.b[k] || ""; });
        var w = q.querySelector(".xq-working"); if (w) w.value = o.w || "";
      } else if (kind === "code") {
        q.querySelector(".xq-code-area").value = v;
      } else {
        q.querySelector(":scope > textarea").value = v;
      }
    }
    function answered(q) {
      var kind = q.getAttribute("data-kind");
      if (kind === "choice" || kind === "matrix") return !!q.querySelector("input:checked");
      if (kind === "blanks") return Array.prototype.some.call(q.querySelectorAll(".xq-blank"), function (i) { return i.value.trim(); });
      if (kind === "code") return q.querySelector(".xq-code-area").value.trim() !== q.querySelector(".xq-starter").content.textContent.trim();
      return !!q.querySelector(":scope > textarea").value.trim();
    }

    var rec = mine();
    questions.forEach(function (q) { restore(q, rec.a[q.getAttribute("data-exam-id")]); });

    function countAnswered() {
      var n = questions.filter(answered).length;
      done.textContent = n + " of " + questions.length;
    }
    var saveTimer = null;
    function persist() {
      clearTimeout(saveTimer);
      saveTimer = setTimeout(function () {
        var r = mine();
        r.a = {};
        questions.forEach(function (q) { r.a[q.getAttribute("data-exam-id")] = stateOf(q); });
        save(r);
      }, 400);
      countAnswered();
    }
    wrap.addEventListener("input", persist);
    wrap.addEventListener("change", persist);
    document.addEventListener("msk:exam-change", persist);

    function left() {
      var r = mine(), used = r.t.used + (r.t.from ? (Date.now() - r.t.from) / 1000 : 0);
      return Math.max(0, mins * 60 - used);
    }
    function fmt(s) {
      s = Math.ceil(s);
      var h = Math.floor(s / 3600), m = Math.floor((s % 3600) / 60), x = s % 60;
      return (h ? h + ":" + (m < 10 ? "0" : "") : "") + m + ":" + (x < 10 ? "0" : "") + x;
    }
    function paint() {
      var l = left();
      clock.textContent = fmt(l);
      bar.classList.toggle("is-low", l > 0 && l <= 300);
      var r = mine();
      bStart.hidden = !!r.t.from || !!r.done;
      bStart.textContent = r.t.used ? "Resume" : "Start the exam";
      bPause.hidden = !r.t.from || !!r.done;
      bFinish.hidden = !!r.done;
      bAgain.hidden = !r.done;
      if (r.t.from && l <= 0) finish(true);
    }
    function run() {
      clearInterval(tick);
      tick = setInterval(paint, 500);
      paint();
    }
    function lock(on) {
      wrap.classList.toggle("is-locked", on);
      wrap.querySelectorAll("textarea, input, [data-mark], [data-exam-reset], [data-code-run], [data-code-reset]").forEach(function (n) {
        if (n.closest(".self-mark")) return;
        if (n.tagName === "TEXTAREA" && !n.closest(".xq-code-in")) n.readOnly = on;
        else n.disabled = on;
      });
    }
    function finish(timeUp) {
      var r = mine();
      if (r.done) return;
      if (r.t.from) { r.t.used += (Date.now() - r.t.from) / 1000; r.t.from = 0; }
      r.done = Date.now();
      save(r);
      clearInterval(tick);
      lock(true);
      bar.classList.add("is-done");
      score.textContent = "Marking";
      if (timeUp && window.MskCat) window.MskCat.say("Time is up. Pens down: the paper is locked and being marked, exactly as it would be collected in the exam hall.", "Pixel says");
      markAll(wrap).then(function (t) { showScore(t); });
      paint();
    }
    function showScore(t) {
      var pc = t.tot ? Math.round((t.got / t.tot) * 100) : 0;
      score.textContent = t.got + " / " + t.tot + " (" + pc + "%)";
    }
    document.addEventListener("msk:exam-total", function (e) {
      if (mine().done) showScore(e.detail);
    });

    bStart.addEventListener("click", function () {
      var r = mine();
      r.t.from = Date.now();
      save(r);
      run();
      var first = wrap.querySelector(".examq");
      if (first && !r.t.used) first.scrollIntoView({ behavior: "smooth", block: "start" });
    });
    bPause.addEventListener("click", function () {
      var r = mine();
      if (r.t.from) { r.t.used += (Date.now() - r.t.from) / 1000; r.t.from = 0; save(r); }
      clearInterval(tick);
      paint();
    });
    bFinish.addEventListener("click", function () {
      var unanswered = questions.length - questions.filter(answered).length;
      var msg = "Finish now and mark the whole paper?" + (unanswered ? " " + unanswered + " question" + (unanswered === 1 ? " is" : "s are") + " still unanswered." : "") + " Your answers will be locked.";
      if (window.confirm(msg)) finish(false);
    });
    bAgain.addEventListener("click", function () {
      if (!window.confirm("Clear every answer and the clock, and sit this paper again?")) return;
      var p = all(); delete p[slug]; store.set("papers", p);
      questions.forEach(clearOne);
      lock(false);
      bar.classList.remove("is-done", "is-low");
      score.textContent = "";
      showTotal(wrap);
      countAnswered();
      paint();
      window.scrollTo({ top: 0, behavior: "smooth" });
    });

    countAnswered();
    if (rec.done) {
      lock(true);
      bar.classList.add("is-done");
      markAll(wrap).then(function (t) { showScore(t); });
    }
    if (rec.t.from) run(); else paint();
  }
})();
