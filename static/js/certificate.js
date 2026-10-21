/* MskProd Computing - the AI course certificate.
 *
 * Reads the quiz scores saved on this device, unlocks the certificate once
 * every lesson quiz has been passed, and fills in the student's own details.
 * The details are kept on this device too, under mskprod:aicert.
 */
(function () {
  "use strict";
  var store = window.MskStore || {
    get: function (k, f) { try { var v = localStorage.getItem("mskprod:" + k); return v === null ? f : JSON.parse(v); } catch (e) { return f; } },
    set: function (k, v) { try { localStorage.setItem("mskprod:" + k, JSON.stringify(v)); } catch (e) { /* private mode */ } }
  };
  var app = document.getElementById("cert");
  var dataEl = document.getElementById("cert-data");
  if (!app || !dataEl) return;
  var data = JSON.parse(dataEl.textContent);
  document.body.classList.add("cert-page");

  function $(id) { return document.getElementById(id); }
  function el(tag, cls, txt) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (txt !== undefined && txt !== null) n.textContent = txt;
    return n;
  }
  function pad(n) { return (n < 10 ? "0" : "") + n; }
  function iso(ts) { var d = new Date(ts); return d.getFullYear() + "-" + pad(d.getMonth() + 1) + "-" + pad(d.getDate()); }
  function longDate(s) {
    var m = /^(\d{4})-(\d{2})-(\d{2})$/.exec(s || "");
    if (!m) return "";
    var d = new Date(+m[1], +m[2] - 1, +m[3]);
    return d.toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" });
  }

  /* ------------------------------------------------------------ scores */
  var quiz = store.get("quiz", {}) || {};
  function best(id) {
    var r = quiz[id];
    if (!r) return null;
    if (r.b != null) return r.b;
    return r.t ? Math.round(100 * r.s / r.t) : 0;
  }
  var total = 0, passed = 0, sum = 0, last = 0;
  data.levels.forEach(function (L) {
    L.lessons.forEach(function (l) {
      total++;
      l.best = best(l.id);
      if (l.best !== null) sum += l.best;
      if (l.best !== null && l.best >= data.pass) passed++;
      var r = quiz[l.id];
      if (r && r.d > last) last = r.d;
    });
  });
  var unlocked = total > 0 && passed === total;
  var average = total ? Math.round(sum / total) : 0;

  var saved = store.get("aicert", {}) || {};
  if (unlocked && !saved.done) { saved.done = last || Date.now(); store.set("aicert", saved); }

  /* ------------------------------------------------------------ status */
  var status = $("cert-status");
  status.textContent = "";
  status.classList.add(unlocked ? "is-unlocked" : "is-locked");
  if (unlocked) {
    status.appendChild(el("p", "cert-kicker", "Unlocked"));
    status.appendChild(el("h2", null, "Congratulations, you are an AI hero"));
    status.appendChild(el("p", null, "You passed all " + total + " lesson quizzes, with an average of " + average +
      "%. Add your name below, then print your certificate or save it as a PDF."));
  } else {
    status.appendChild(el("p", "cert-kicker", passed + " of " + total + " lessons passed"));
    status.appendChild(el("h2", null, passed === 0 ? "Your certificate is waiting" : "Keep going, you are on your way"));
    status.appendChild(el("p", null, "Score at least " + data.pass + "% on every lesson quiz to unlock your certificate. " +
      "You can set it up now: it prints once the last quiz is passed."));
    var bar = el("div", "cert-bar"), fill = el("i");
    fill.style.width = (total ? 100 * passed / total : 0).toFixed(1) + "%";
    bar.appendChild(fill);
    bar.setAttribute("role", "progressbar");
    bar.setAttribute("aria-valuemin", "0"); bar.setAttribute("aria-valuemax", String(total));
    bar.setAttribute("aria-valuenow", String(passed));
    bar.setAttribute("aria-label", "Lessons passed");
    status.appendChild(bar);
    var next = null;
    data.levels.some(function (L) {
      return L.lessons.some(function (l) { if (l.best === null || l.best < data.pass) { next = l; return true; } return false; });
    });
    if (next) {
      var p = el("p", "cert-next");
      p.appendChild(document.createTextNode("Next up: "));
      var a = el("a", null, next.t); a.href = next.u;
      p.appendChild(a);
      status.appendChild(p);
    }
  }

  /* ------------------------------------------------------------ lessons */
  var list = $("cert-levels");
  data.levels.forEach(function (L, i) {
    var done = L.lessons.every(function (l) { return l.best !== null && l.best >= data.pass; });
    var card = el("div", "cert-level" + (done ? " is-done" : ""));
    var head = el("p", "cert-level-title");
    head.appendChild(el("span", "cert-level-num", String(i + 1)));
    head.appendChild(document.createTextNode(L.title.replace(/^Level \d+: /, "")));
    card.appendChild(head);
    var ul = el("ul");
    L.lessons.forEach(function (l) {
      var li = el("li"), a = el("a", null, l.t);
      a.href = l.u;
      li.appendChild(a);
      var pill;
      if (l.best === null) pill = el("span", "cert-pill", "not started");
      else if (l.best >= data.pass) pill = el("span", "cert-pill is-pass", "passed " + l.best + "%");
      else pill = el("span", "cert-pill is-low", l.best + "%, retake");
      li.appendChild(pill);
      ul.appendChild(li);
    });
    card.appendChild(ul);
    list.appendChild(card);
  });

  /* ------------------------------------------------------- certificate */
  var inName = $("cert-in-name"), inOrg = $("cert-in-org"), inDate = $("cert-in-date"), inAvg = $("cert-in-avg");
  var btn = $("cert-print"), hint = $("cert-hint");
  var svg = document.querySelector("#cert-sheet svg");
  var tName = $("cert-name"), tOrg = $("cert-org"), tDate = $("cert-date"), tAvg = $("cert-avg"), tNo = $("cert-no");
  var mark = $("cert-mark");

  inName.value = saved.name || "";
  inOrg.value = saved.org || "";
  inDate.value = saved.date || iso(saved.done || Date.now());
  inAvg.checked = !!saved.avg;
  var theme = data.themes[saved.theme] ? saved.theme : Object.keys(data.themes)[0];
  Array.prototype.forEach.call(document.querySelectorAll('input[name="cert-theme"]'), function (r) {
    r.checked = r.value === theme;
    r.addEventListener("change", function () { if (r.checked) { theme = r.value; update(); } });
  });

  function rgb(h) { return [parseInt(h.slice(1, 3), 16), parseInt(h.slice(3, 5), 16), parseInt(h.slice(5, 7), 16)]; }
  function mix(c, t) {
    var a = t <= 0.5 ? c[0] : c[1], b = t <= 0.5 ? c[1] : c[2], u = t <= 0.5 ? t * 2 : (t - 0.5) * 2;
    var A = rgb(a), B = rgb(b);
    return "#" + [0, 1, 2].map(function (i) {
      var v = Math.round(A[i] + (B[i] - A[i]) * u).toString(16);
      return v.length < 2 ? "0" + v : v;
    }).join("");
  }
  function paint(c) {
    Array.prototype.forEach.call(svg.querySelectorAll("[data-c]"), function (n) { n.setAttribute("stop-color", c[+n.getAttribute("data-c") - 1]); });
    Array.prototype.forEach.call(svg.querySelectorAll("[data-fill]"), function (n) { n.setAttribute("fill", c[+n.getAttribute("data-fill") - 1]); });
    Array.prototype.forEach.call(svg.querySelectorAll("[data-stroke]"), function (n) { n.setAttribute("stroke", c[+n.getAttribute("data-stroke") - 1]); });
    Array.prototype.forEach.call(svg.querySelectorAll("[data-mix]"), function (n) { n.setAttribute("fill", mix(c, +n.getAttribute("data-mix"))); });
  }

  // The number is a hash of the name and the date, so the same details always
  // give the same number. It identifies a printout; it is not a password.
  function certNo(name, date) {
    var s = name.toLowerCase().replace(/\s+/g, " ").trim() + "|" + date;
    var h1 = 0x811c9dc5, h2 = 0x9747b28c;
    for (var i = 0; i < s.length; i++) {
      var ch = s.charCodeAt(i);
      h1 = Math.imul(h1 ^ ch, 16777619);
      h2 = Math.imul(h2 ^ ch, 0x5bd1e995); h2 ^= h2 >>> 15;
    }
    var A = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789", x = h1 >>> 0, y = h2 >>> 0, out = "";
    for (var k = 0; k < 4; k++) { out += A[x % 32]; x = Math.floor(x / 32); }
    out += "-";
    for (k = 0; k < 4; k++) { out += A[y % 32]; y = Math.floor(y / 32); }
    return "AI-" + (date || "").slice(0, 4) + "-" + out;
  }

  // Shrink a long name to fit the line, and squeeze it as a last resort.
  function fitName() {
    var size = 56, len = 0;
    tName.style.fontSize = size + "px";
    tName.removeAttribute("textLength"); tName.removeAttribute("lengthAdjust");
    try { len = tName.getComputedTextLength(); } catch (e) { len = 0; }
    if (len > 700) {
      size = Math.max(20, Math.floor(size * 700 / len));
      tName.style.fontSize = size + "px";
      try { len = tName.getComputedTextLength(); } catch (e) { len = 0; }
      if (len > 700) { tName.setAttribute("textLength", "700"); tName.setAttribute("lengthAdjust", "spacingAndGlyphs"); }
    }
  }

  function update() {
    var name = inName.value.replace(/\s+/g, " ").trim();
    var org = inOrg.value.replace(/\s+/g, " ").trim();
    tName.textContent = name || "Your name";
    tName.classList.toggle("is-empty", !name);
    fitName();
    tOrg.textContent = org ? "of " + org : "";
    tDate.textContent = longDate(inDate.value);
    tAvg.textContent = inAvg.checked ? "Average quiz score across all " + total + " lessons: " + average + "%" : "";
    tNo.textContent = name && inDate.value ? "Certificate no. " + certNo(name, inDate.value) : "";
    paint(data.themes[theme]);
    mark.style.display = unlocked ? "none" : "";

    btn.disabled = !unlocked || !name;
    if (!unlocked) hint.textContent = "Printing unlocks when every lesson quiz is passed. " + (total - passed) + " to go.";
    else if (!name) hint.textContent = "Type your name to print your certificate.";
    else hint.textContent = "Choose A4, landscape, and switch headers and footers off in the print window.";

    saved.name = inName.value; saved.org = inOrg.value; saved.date = inDate.value;
    saved.theme = theme; saved.avg = inAvg.checked;
    store.set("aicert", saved);
  }

  [inName, inOrg, inDate].forEach(function (n) { n.addEventListener("input", update); });
  inAvg.addEventListener("change", update);
  btn.addEventListener("click", function () { if (!btn.disabled) window.print(); });
  // Fonts change the width of the name, so fit it again once they have loaded.
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(fitName);
  update();

  if (unlocked && window.MskCat && !saved.cheered) {
    saved.cheered = true; store.set("aicert", saved);
    window.MskCat.say("Fifteen levels, thirty lessons. You built an AI from scratch. Go and print that certificate!", "Pixel says");
  }
})();
