/* Assignment links. A teacher picks topics, the page encodes that choice into
   the URL, and anybody opening the link sees the list. Nothing is stored on a
   server: the whole assignment travels inside the link itself. */
(function () {
  "use strict";

  var root = document.getElementById("assign");
  if (!root) return;

  var store = {
    get: function (k, fb) {
      try {
        var v = localStorage.getItem("mskprod:" + k);
        return v === null ? fb : JSON.parse(v);
      } catch (e) { return fb; }
    }
  };

  function el(tag, cls, txt) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (txt !== undefined && txt !== null) n.textContent = txt;
    return n;
  }

  function encode(obj) {
    var json = JSON.stringify(obj);
    var b64 = btoa(String.fromCharCode.apply(null,
      new TextEncoder().encode(json)));
    return b64.replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
  }

  function decode(str) {
    try {
      var b64 = str.replace(/-/g, "+").replace(/_/g, "/");
      while (b64.length % 4) b64 += "=";
      var bin = atob(b64);
      var bytes = new Uint8Array(bin.length);
      for (var i = 0; i < bin.length; i++) bytes[i] = bin.charCodeAt(i);
      return JSON.parse(new TextDecoder().decode(bytes));
    } catch (e) { return null; }
  }

  function topicIndex(manifest) {
    var map = {};
    manifest.courses.forEach(function (c) {
      c.topics.forEach(function (t) { map[t.id] = { course: c, topic: t }; });
    });
    return map;
  }

  /* --------------------------------------------------------------- viewer */

  function renderView(manifest, data) {
    var map = topicIndex(manifest);
    var quiz = store.get("quiz", {}) || {};
    root.textContent = "";

    var head = el("header", "assign-head");
    head.appendChild(el("h2", null, data.n || "Revision assignment"));
    var meta = [];
    meta.push(data.t.length + (data.t.length === 1 ? " topic" : " topics"));
    var totalQ = 0, totalM = 0, minutes = 0;
    data.t.forEach(function (id) {
      var r = map[id];
      if (!r) return;
      totalQ += r.topic.q;
      totalM += r.topic.e;
      minutes += r.topic.m;
    });
    meta.push(totalQ + " quiz questions");
    meta.push(totalM + " marks of written practice");
    meta.push("about " + Math.round(minutes / 5) * 5 + " minutes of reading");
    if (data.d) meta.push("due " + data.d);
    head.appendChild(el("p", "muted", meta.join("  |  ")));
    if (data.m) head.appendChild(el("p", "assign-message", data.m));
    root.appendChild(head);

    var list = el("ol", "dash-list");
    var done = 0;
    data.t.forEach(function (id) {
      var r = map[id];
      var li = el("li");
      if (!r) {
        li.appendChild(el("p", "muted",
          "One topic in this link is not on the site any more."));
        list.appendChild(li);
        return;
      }
      var q = quiz[id];
      var pct = q && q.t ? Math.round((q.s / q.t) * 100) : null;
      if (pct !== null && pct >= 80) done++;
      var a = el("a", "dash-item", null);
      a.href = r.topic.u;
      var main = el("span", "dash-item-main");
      main.appendChild(el("b", null, r.topic.t));
      main.appendChild(el("small", null, r.course.title + "  |  " + r.topic.unit));
      a.appendChild(main);
      var m2 = el("span", "dash-item-meta");
      m2.appendChild(el("span", "dash-pill", r.topic.q + " questions"));
      if (pct === null) {
        m2.appendChild(el("span", "dash-pill", "not done"));
      } else {
        m2.appendChild(el("span", "dash-pill " + (pct >= 80 ? "is-good"
          : pct >= 50 ? "is-mid" : "is-bad"), pct + " per cent"));
      }
      a.appendChild(m2);
      li.appendChild(a);
      list.appendChild(li);
    });
    root.appendChild(list);

    var bar = el("div", "assign-progress");
    bar.appendChild(el("p", null, done + " of " + data.t.length
      + " done to 80 per cent or better in this browser."));
    var track = el("div", "dash-bar");
    var fill = el("span", "dash-bar-fill");
    fill.style.width = Math.round((done / Math.max(1, data.t.length)) * 100) + "%";
    track.appendChild(fill);
    bar.appendChild(track);
    bar.appendChild(el("p", "muted",
      "A topic counts as done once its knowledge check is at 80 per cent or better. "
      + "That tick lives in this browser only. Nobody, including whoever set this "
      + "work, can see it, so screenshot the page if you have been asked to prove "
      + "you did it."));
    root.appendChild(bar);

    var again = el("p");
    var link = el("a", "btn btn-secondary", "Build a different assignment");
    link.href = window.location.pathname;
    again.appendChild(link);
    root.appendChild(again);
  }

  /* -------------------------------------------------------------- builder */

  function renderBuilder(manifest) {
    root.textContent = "";
    var chosen = {};

    var form = el("div", "assign-form");
    var nameField = el("div", "tool-field");
    var nameLab = el("label", null, "Assignment title");
    var nameInp = document.createElement("input");
    nameInp.type = "text";
    nameInp.placeholder = "For example: Half term revision, paper 1";
    nameInp.id = "assign-name";
    nameLab.setAttribute("for", nameInp.id);
    nameField.appendChild(nameLab);
    nameField.appendChild(nameInp);

    var dueField = el("div", "tool-field");
    dueField.style.flex = "0 1 12rem";
    var dueLab = el("label", null, "Due date, optional");
    var dueInp = document.createElement("input");
    dueInp.type = "date";
    dueInp.id = "assign-due";
    dueLab.setAttribute("for", dueInp.id);
    dueField.appendChild(dueLab);
    dueField.appendChild(dueInp);

    var msgField = el("div", "tool-field");
    var msgLab = el("label", null, "A note for whoever opens the link, optional");
    var msgInp = document.createElement("input");
    msgInp.type = "text";
    msgInp.placeholder = "For example: do the quizzes first, then the written questions";
    msgInp.id = "assign-msg";
    msgLab.setAttribute("for", msgInp.id);
    msgField.appendChild(msgLab);
    msgField.appendChild(msgInp);

    var row = el("div", "tool-row");
    row.appendChild(nameField);
    row.appendChild(dueField);
    form.appendChild(row);
    form.appendChild(msgField);
    root.appendChild(form);

    var count = el("p", "assign-count", "No topics chosen yet.");
    root.appendChild(count);

    manifest.courses.forEach(function (c) {
      var details = document.createElement("details");
      details.className = "assign-course";
      var sum = document.createElement("summary");
      sum.textContent = c.title + "  (" + c.topics.length + " topics)";
      details.appendChild(sum);
      var grid = el("div", "assign-grid");
      c.topics.forEach(function (t) {
        var lab = el("label", "assign-check");
        var cb = document.createElement("input");
        cb.type = "checkbox";
        cb.value = t.id;
        cb.addEventListener("change", function () {
          if (cb.checked) chosen[t.id] = true; else delete chosen[t.id];
          update();
        });
        lab.appendChild(cb);
        var sp = el("span");
        sp.appendChild(el("b", null, t.t));
        sp.appendChild(el("small", null, t.unit + "  |  " + t.q + " questions"));
        lab.appendChild(sp);
        grid.appendChild(lab);
      });
      details.appendChild(grid);
      root.appendChild(details);
    });

    var outWrap = el("div", "assign-out");
    var outLab = el("p", "tool-label", "Your link");
    var outInp = document.createElement("input");
    outInp.type = "text";
    outInp.readOnly = true;
    outInp.className = "tool-mono";
    outInp.setAttribute("aria-label", "The assignment link");
    var btns = el("div", "tool-btns");
    var bCopy = el("button", "tool-btn is-primary", "Copy link");
    var bOpen = el("button", "tool-btn", "Open it");
    bCopy.type = bOpen.type = "button";
    btns.appendChild(bCopy);
    btns.appendChild(bOpen);
    var copied = el("span", "assign-copied", "");
    btns.appendChild(copied);
    outWrap.appendChild(outLab);
    outWrap.appendChild(outInp);
    outWrap.appendChild(btns);
    root.appendChild(outWrap);

    function link() {
      var ids = Object.keys(chosen);
      var payload = { t: ids };
      if (nameInp.value.trim()) payload.n = nameInp.value.trim();
      if (dueInp.value) payload.d = dueInp.value;
      if (msgInp.value.trim()) payload.m = msgInp.value.trim();
      return window.location.origin + window.location.pathname + "#" + encode(payload);
    }

    function update() {
      var n = Object.keys(chosen).length;
      count.textContent = n === 0 ? "No topics chosen yet."
        : n + (n === 1 ? " topic chosen." : " topics chosen.");
      outInp.value = n ? link() : "";
      bCopy.disabled = bOpen.disabled = !n;
    }

    [nameInp, dueInp, msgInp].forEach(function (i) {
      i.addEventListener("input", update);
      i.addEventListener("change", update);
    });

    bCopy.addEventListener("click", function () {
      if (!outInp.value) return;
      outInp.select();
      var ok = false;
      try { ok = document.execCommand("copy"); } catch (e) { ok = false; }
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(outInp.value).then(function () {
          copied.textContent = "Copied.";
        }, function () { copied.textContent = ok ? "Copied." : "Press ctrl and c to copy."; });
      } else {
        copied.textContent = ok ? "Copied." : "Press ctrl and c to copy.";
      }
      setTimeout(function () { copied.textContent = ""; }, 2600);
    });

    bOpen.addEventListener("click", function () {
      if (outInp.value) window.location.href = outInp.value;
      window.location.reload();
    });

    update();
  }

  fetch("/assets/data/progress.json", { cache: "no-cache" })
    .then(function (r) { return r.json(); })
    .then(function (manifest) {
      var hash = window.location.hash.replace(/^#/, "");
      var data = hash ? decode(hash) : null;
      if (data && data.t && data.t.length) renderView(manifest, data);
      else renderBuilder(manifest);
    })
    .catch(function () {
      root.textContent = "";
      root.appendChild(el("p", "muted",
        "The topic list could not be loaded. Refresh the page to try again."));
    });

  window.addEventListener("hashchange", function () { window.location.reload(); });
})();
