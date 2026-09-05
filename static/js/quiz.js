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
          rec[key] = { s: right, t: total, d: Date.now() };
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

     The marker reads the mark scheme attached to each question. Every mark
     point carries a list of acceptable phrasings. A point is awarded when the
     student's answer contains any one of them, allowing for plurals and common
     verb endings. The full mark scheme and a model answer are always revealed
     afterwards, and the student can override the machine mark, because a real
     examiner rewards correct wording the keyword list has not anticipated.
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
  function containsPhrase(answerNorm, answerStems, phrase) {
    var p = normalise(phrase).trim();
    if (!p) return false;
    if (answerNorm.indexOf(" " + p + " ") > -1) return true;
    var words = p.split(" ");
    if (words.length === 1) {
      var w = words[0];
      if (answerStems[w] || answerStems[stem(w)]) return true;
      var syn = SYNONYMS[w];
      if (syn) { for (var i = 0; i < syn.length; i++) { if (containsPhrase(answerNorm, answerStems, syn[i])) return true; } }
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

  function markOne(examq) {
    var ta = examq.querySelector("textarea");
    var result = examq.querySelector(".examq-result");
    var answer = normalise(ta.value);
    var stems = stemSet(ta.value);
    var words = ta.value.trim() ? ta.value.trim().split(/\s+/).length : 0;
    var max = parseInt(examq.getAttribute("data-marks"), 10) || 1;
    var awarded = 0;

    result.querySelectorAll(".ms li").forEach(function (li) {
      var phrases = [];
      try { phrases = JSON.parse(li.getAttribute("data-any") || "[]"); } catch (e) { phrases = []; }
      var hit = words > 0 && pointHit(answer, stems, phrases);
      li.classList.toggle("hit", hit);
      if (hit) awarded++;
    });
    awarded = Math.min(awarded, max);

    var award = result.querySelector(".award");
    if (award) award.textContent = awarded + " / " + max;

    var verdict = result.querySelector("[data-verdict]");
    if (verdict) {
      var msg;
      if (words === 0) msg = "You have not written anything yet. Even a rough attempt is worth more than a blank, and in the real exam a blank is a guaranteed zero. Write what you can, then compare it with the mark scheme below.";
      else if (awarded >= max) msg = "That covers every mark point. Check the model answer as well, because how you order and link the points is what separates a top answer from an average one.";
      else if (awarded >= Math.ceil(max / 2)) msg = "Part marks. You have the right idea but the answer is missing " + (max - awarded) + " mark point" + (max - awarded === 1 ? "" : "s") + ". The unticked lines below show exactly what to add.";
      else msg = "The marker found " + awarded + " of " + max + ". Read the unticked mark points below, then close this and write the answer again from memory. Rewriting is what makes it stick.";
      verdict.textContent = msg;
    }

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
    result.classList.add("show");
    var key = examq.getAttribute("data-exam-id");
    if (key) {
      var rec = store.get("exam", {});
      rec[key] = { s: awarded, t: max, d: Date.now() };
      store.set("exam", rec);
    }
    return { awarded: awarded, max: max };
  }

  document.addEventListener("click", function (e) {
    var b = e.target.closest && e.target.closest("[data-mark]");
    if (b) { markOne(b.closest(".examq")); return; }

    var r = e.target.closest && e.target.closest("[data-exam-reset]");
    if (r) {
      var eq = r.closest(".examq");
      eq.querySelector("textarea").value = "";
      eq.querySelector(".examq-result").classList.remove("show");
      eq.querySelector("textarea").focus();
      return;
    }

    var all = e.target.closest && e.target.closest("[data-mark-all]");
    if (all) {
      var wrap = all.closest("[data-exam-set]") || document;
      var got = 0, tot = 0;
      wrap.querySelectorAll(".examq").forEach(function (q) { var res = markOne(q); got += res.awarded; tot += res.max; });
      var sum = wrap.querySelector("[data-exam-total]");
      if (sum) {
        var pc = tot ? Math.round((got / tot) * 100) : 0;
        sum.innerHTML = 'Machine mark <span class="pct">' + got + " / " + tot + "</span> (" + pc + " per cent)";
        var b2 = wrap.querySelector("[data-exam-bar]"); if (b2) b2.style.width = pc + "%";
      }
      if (window.MskCat && tot) {
        var p = Math.round((got / tot) * 100);
        if (p >= 80) window.MskCat.say("That is grade 8 to 9 territory on written answers. Keep checking your work against the model answers, they show you how to link points together.", "Pixel says");
        else if (p >= 45) window.MskCat.say("Middle of the range. The quickest gain is writing one extra sentence per question that says why, not just what.", "Pixel says");
        else window.MskCat.say("Written answers are a skill you build, not a talent you have. Copy the model answers out by hand once, then try again from memory tomorrow.", "Pixel says");
      }
    }
  });

  document.addEventListener("change", function (e) {
    var s = e.target.closest && e.target.closest("[data-self]");
    if (!s) return;
    var eq = s.closest(".examq");
    var award = eq.querySelector(".award");
    var max = parseInt(eq.getAttribute("data-marks"), 10) || 1;
    if (award) award.textContent = s.value + " / " + max;
    var key = eq.getAttribute("data-exam-id");
    if (key) {
      var rec = store.get("exam", {});
      rec[key] = { s: parseInt(s.value, 10), t: max, d: Date.now(), self: 1 };
      store.set("exam", rec);
    }
  });

  /* keyboard shortcut: ctrl+enter marks the answer you are typing */
  document.addEventListener("keydown", function (e) {
    if (!(e.key === "Enter" && (e.ctrlKey || e.metaKey))) return;
    var eq = e.target.closest && e.target.closest(".examq");
    if (eq) { e.preventDefault(); markOne(eq); }
  });

  /* ------------------------------------------------------ exam timer */
  document.querySelectorAll("[data-timer]").forEach(function (el) {
    var mins = parseInt(el.getAttribute("data-timer"), 10) || 90;
    var left = mins * 60, id = null;
    var face = el.querySelector("[data-timer-face]");
    var btn = el.querySelector("[data-timer-btn]");
    function paint() {
      var m = Math.floor(left / 60), s = left % 60;
      face.textContent = (m < 10 ? "0" : "") + m + ":" + (s < 10 ? "0" : "") + s;
    }
    paint();
    btn.addEventListener("click", function () {
      if (id) { clearInterval(id); id = null; btn.textContent = "Resume"; return; }
      btn.textContent = "Pause";
      id = setInterval(function () {
        left--; paint();
        if (left <= 0) {
          clearInterval(id); id = null; btn.textContent = "Start";
          face.textContent = "00:00";
          if (window.MskCat) window.MskCat.say("Time is up. Stop writing, then mark what you have. Working to the clock is half of exam technique.", "Pixel says");
        }
      }, 1000);
    });
    var reset = el.querySelector("[data-timer-reset]");
    if (reset) reset.addEventListener("click", function () {
      if (id) { clearInterval(id); id = null; }
      left = mins * 60; paint(); btn.textContent = "Start";
    });
  });
})();
