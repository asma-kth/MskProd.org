/* Progress dashboard. Reads the site manifest and whatever this browser has
   saved locally, works out what is weak and what is due, and shows it. No data
   leaves the machine and there is nothing to sign in to. */
(function () {
  "use strict";

  var store = {
    get: function (k, fb) {
      try {
        var v = localStorage.getItem("mskprod:" + k);
        return v === null ? fb : JSON.parse(v);
      } catch (e) { return fb; }
    }
  };

  var root = document.getElementById("dash");
  if (!root) return;

  var DAY = 86400000;

  /* How long until a topic is worth revisiting. The stronger the last score,
     the longer the gap, which is the whole point of spaced repetition: you
     revisit a thing just as you are starting to forget it. */
  function interval(pct) {
    if (pct >= 90) return 10;
    if (pct >= 80) return 6;
    if (pct >= 65) return 3;
    if (pct >= 50) return 2;
    return 1;
  }

  function el(tag, cls, txt) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (txt !== undefined && txt !== null) n.textContent = txt;
    return n;
  }

  function pill(text, kind) {
    return el("span", "dash-pill" + (kind ? " " + kind : ""), text);
  }

  function daysAgo(ts) {
    var d = Math.floor((Date.now() - ts) / DAY);
    if (d <= 0) return "today";
    if (d === 1) return "yesterday";
    return d + " days ago";
  }

  function render(manifest) {
    var quiz = store.get("quiz", {}) || {};
    var exam = store.get("exam", {}) || {};
    var seen = store.get("seen", {}) || {};
    var streak = store.get("streak", { days: 0, best: 0, hist: [] }) || {};

    var rows = [];
    manifest.courses.forEach(function (c) {
      c.topics.forEach(function (t) {
        var q = quiz[t.id] || null;
        var pct = q && q.t ? Math.round((q.s / q.t) * 100) : null;
        var examMarks = 0, examMax = 0;
        Object.keys(exam).forEach(function (k) {
          if (k.indexOf(t.id + "-e") === 0) {
            examMarks += exam[k].s || 0;
            examMax += exam[k].t || 0;
          }
        });
        var last = q ? q.d : (seen[t.id] || null);
        var due = null, overdue = 0;
        if (q && q.d) {
          due = q.d + interval(pct) * DAY;
          overdue = (Date.now() - due) / DAY;
        }
        rows.push({
          course: c, topic: t, quiz: q, pct: pct, last: last,
          examMarks: examMarks, examMax: examMax,
          seen: !!seen[t.id], due: due, overdue: overdue
        });
      });
    });

    var studied = rows.filter(function (r) { return r.pct !== null; });
    var opened = rows.filter(function (r) { return r.seen; });

    root.textContent = "";

    /* ------------------------------------------------------ empty state */
    if (!opened.length && !studied.length) {
      var empty = el("div", "card dash-empty");
      empty.appendChild(el("h2", null, "Nothing recorded yet"));
      empty.appendChild(el("p", null,
        "This page fills itself in as you work. Open a topic, do the knowledge "
        + "check at the bottom of it, and come back here. Everything is stored in "
        + "this browser only, so there is no account and nothing to sign in to. "
        + "Using a different browser or a private window starts again from empty."));
      var links = el("p");
      manifest.courses.forEach(function (c, i) {
        if (i) links.appendChild(document.createTextNode("  "));
        var a = el("a", "btn btn-secondary", "Start " + c.title);
        a.href = c.url;
        links.appendChild(a);
      });
      empty.appendChild(links);
      root.appendChild(empty);
      return;
    }

    /* ------------------------------------------------------- top figures */
    var stats = el("div", "dash-stats");
    function stat(value, label, note) {
      var s = el("div", "dash-stat");
      s.appendChild(el("b", null, value));
      s.appendChild(el("span", null, label));
      if (note) s.appendChild(el("small", null, note));
      stats.appendChild(s);
    }
    var avg = studied.length
      ? Math.round(studied.reduce(function (a, r) { return a + r.pct; }, 0) / studied.length)
      : 0;
    stat(String(streak.days || 0), (streak.days === 1 ? "day" : "days") + " in a row",
         "best " + (streak.best || 0));
    stat(opened.length + " of " + rows.length, "topics opened",
         Math.round((opened.length / rows.length) * 100) + " per cent of the site");
    stat(String(studied.length), "quizzes completed",
         studied.length ? "average " + avg + " per cent" : "none yet");
    var strong = studied.filter(function (r) { return r.pct >= 80; }).length;
    stat(String(strong), "topics at 80 per cent or better",
         "that is the grade 9 threshold on knowledge");
    root.appendChild(stats);

    /* -------------------------------------------------- revise these five */
    var due = studied.slice().filter(function (r) { return r.overdue > -0.5; });
    due.sort(function (a, b) {
      /* weakest first, then most overdue: a weak topic left for a week is the
         single most valuable thing a student can open today */
      var wa = (100 - a.pct) + Math.min(a.overdue, 21) * 2;
      var wb = (100 - b.pct) + Math.min(b.overdue, 21) * 2;
      return wb - wa;
    });
    var pickSection = el("section", "dash-section");
    pickSection.appendChild(el("h2", null, "Revise these five today"));
    if (!due.length) {
      pickSection.appendChild(el("p", "muted",
        "Nothing is due yet. Every topic you have tested yourself on is still "
        + "inside its spacing window, so the most useful thing you can do is start "
        + "a topic you have not opened."));
    } else {
      pickSection.appendChild(el("p", "muted",
        "Ranked by how weak the last score was and how long it has been. Doing "
        + "these five is worth more than rereading five pages you already know."));
      var list = el("ol", "dash-list");
      due.slice(0, 5).forEach(function (r) {
        var li = el("li");
        var a = el("a", "dash-item", null);
        a.href = r.topic.u;
        var main = el("span", "dash-item-main");
        main.appendChild(el("b", null, r.topic.t));
        main.appendChild(el("small", null, r.course.title + "  |  " + r.topic.unit));
        a.appendChild(main);
        var meta = el("span", "dash-item-meta");
        meta.appendChild(pill(r.pct + " per cent",
          r.pct >= 80 ? "is-good" : r.pct >= 50 ? "is-mid" : "is-bad"));
        meta.appendChild(pill(r.overdue >= 1
          ? Math.floor(r.overdue) + " days overdue"
          : "due now", r.overdue >= 3 ? "is-bad" : ""));
        a.appendChild(meta);
        li.appendChild(a);
        list.appendChild(li);
      });
      pickSection.appendChild(list);
    }
    root.appendChild(pickSection);

    /* ------------------------------------------------------ never opened */
    var fresh = rows.filter(function (r) { return !r.seen && r.pct === null; });
    if (fresh.length) {
      var newSection = el("section", "dash-section");
      newSection.appendChild(el("h2", null, "Not started yet"));
      newSection.appendChild(el("p", "muted",
        fresh.length + " topics on the site are still untouched. Here are the next "
        + "three in specification order."));
      var ul = el("ul", "dash-list");
      fresh.slice(0, 3).forEach(function (r) {
        var li = el("li");
        var a = el("a", "dash-item", null);
        a.href = r.topic.u;
        var main = el("span", "dash-item-main");
        main.appendChild(el("b", null, r.topic.t));
        main.appendChild(el("small", null, r.course.title + "  |  " + r.topic.unit));
        a.appendChild(main);
        var meta = el("span", "dash-item-meta");
        meta.appendChild(pill("about " + r.topic.m + " min"));
        a.appendChild(meta);
        li.appendChild(a);
        ul.appendChild(li);
      });
      newSection.appendChild(ul);
      root.appendChild(newSection);
    }

    /* -------------------------------------------------- per course bars */
    var courseSection = el("section", "dash-section");
    courseSection.appendChild(el("h2", null, "Progress by course"));
    manifest.courses.forEach(function (c) {
      var mine = rows.filter(function (r) { return r.course.slug === c.slug; });
      var done = mine.filter(function (r) { return r.pct !== null && r.pct >= 80; }).length;
      var attempted = mine.filter(function (r) { return r.pct !== null; }).length;
      var openedC = mine.filter(function (r) { return r.seen; }).length;
      var pctDone = Math.round((done / mine.length) * 100);
      var block = el("div", "dash-course");
      var head = el("div", "dash-course-head");
      var link = el("a", null, c.title);
      link.href = c.url;
      head.appendChild(link);
      head.appendChild(el("span", null, pctDone + " per cent"));
      block.appendChild(head);
      var bar = el("div", "dash-bar");
      var fill = el("span", "dash-bar-fill");
      fill.style.width = pctDone + "%";
      var fill2 = el("span", "dash-bar-soft");
      fill2.style.width = Math.round((openedC / mine.length) * 100) + "%";
      bar.appendChild(fill2);
      bar.appendChild(fill);
      block.appendChild(bar);
      block.appendChild(el("p", "dash-course-note",
        done + " of " + mine.length + " topics scored 80 per cent or better, "
        + attempted + " quizzed, " + openedC + " opened."));
      courseSection.appendChild(block);
    });
    root.appendChild(courseSection);

    /* ---------------------------------------------------- weakest topics */
    if (studied.length) {
      var weak = studied.slice().sort(function (a, b) { return a.pct - b.pct; })
        .slice(0, 10);
      var weakSection = el("section", "dash-section");
      weakSection.appendChild(el("h2", null, "Weakest topics"));
      weakSection.appendChild(el("p", "muted",
        "Your lowest knowledge check scores, worst first. A score below 50 per cent "
        + "means read the explanation again before retaking it, not just retake it."));
      var table = document.createElement("table");
      table.className = "dash-table";
      var thead = document.createElement("thead");
      var hr = document.createElement("tr");
      ["Topic", "Course", "Quiz", "Exam marks", "Last done"].forEach(function (h) {
        var th = document.createElement("th");
        th.textContent = h;
        hr.appendChild(th);
      });
      thead.appendChild(hr);
      table.appendChild(thead);
      var tb = document.createElement("tbody");
      weak.forEach(function (r) {
        var tr = document.createElement("tr");
        var td1 = document.createElement("td");
        var a = el("a", null, r.topic.t);
        a.href = r.topic.u;
        td1.appendChild(a);
        tr.appendChild(td1);
        var td2 = document.createElement("td");
        td2.textContent = r.course.title;
        tr.appendChild(td2);
        var td3 = document.createElement("td");
        td3.appendChild(pill(r.quiz.s + " / " + r.quiz.t,
          r.pct >= 80 ? "is-good" : r.pct >= 50 ? "is-mid" : "is-bad"));
        tr.appendChild(td3);
        var td4 = document.createElement("td");
        td4.textContent = r.examMax ? r.examMarks + " / " + r.examMax : "not attempted";
        tr.appendChild(td4);
        var td5 = document.createElement("td");
        td5.textContent = daysAgo(r.quiz.d);
        tr.appendChild(td5);
        tb.appendChild(tr);
      });
      table.appendChild(tb);
      var scroll = el("div", "table-scroll");
      scroll.appendChild(table);
      weakSection.appendChild(scroll);
      root.appendChild(weakSection);
    }

    /* --------------------------------------------------------- the streak */
    var hist = streak.hist || [];
    var streakSection = el("section", "dash-section");
    streakSection.appendChild(el("h2", null, "The last four weeks"));
    var grid = el("div", "dash-days");
    for (var i = 27; i >= 0; i--) {
      var d = new Date(Date.now() - i * DAY);
      var k = d.getFullYear() + "-" + String(d.getMonth() + 1).padStart(2, "0")
        + "-" + String(d.getDate()).padStart(2, "0");
      var cell = el("span", "dash-day" + (hist.indexOf(k) >= 0 ? " is-on" : ""));
      cell.title = k;
      grid.appendChild(cell);
    }
    streakSection.appendChild(grid);
    streakSection.appendChild(el("p", "muted",
      "Twenty minutes a day beats three hours on a Sunday, because the gap between "
      + "sessions is what moves knowledge into long term memory. Filled squares are "
      + "days you opened the site."));
    root.appendChild(streakSection);
  }

  fetch("/assets/data/progress.json", { cache: "no-cache" })
    .then(function (r) { return r.json(); })
    .then(render)
    .catch(function () {
      root.textContent = "";
      var p = document.createElement("p");
      p.className = "muted";
      p.textContent = "The progress data could not be loaded. Refresh the page to try "
        + "again. Your saved scores are untouched.";
      root.appendChild(p);
    });
})();
