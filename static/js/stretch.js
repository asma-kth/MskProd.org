/* MskProd Computing - Key Stage 3 stretch tasks.
 *
 * Three tasks for one lesson. The Quiz Challenge has three rounds. Quiz Blitz
 * is a quiz show: a clock, four coloured tiles that each carry a shape, points
 * for speed, an answer streak and four computer players to race to the
 * podium. Quick Fire and Big Think are written answers, marked by the keyword
 * marker in quiz.js (window.MskMarker); the mark scheme and a model answer are
 * shown afterwards and the student can change the mark, as on the exam pages.
 * In This or That, Pixel the cat asks questions with two answers and reacts
 * to each choice. Memory Match is a card game: flip two cards at a time to
 * pair each word with its meaning. Best scores are kept on this device only.
 *
 * The hub page uses only the star painting near the top of this file.
 */
(function () {
  "use strict";
  var store = window.MskStore || { get: function (k, f) { return f; }, set: function () {} };
  var RECORDS = "stretch", OPTS = "stretch-opts";

  /* ------------------------------------------------------------ helpers */
  function el(tag, attrs, kids) {
    var n = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (k) {
      var v = attrs[k];
      if (v === null || v === undefined || v === false) return;
      if (k === "html") n.innerHTML = v;
      else if (k === "text") n.textContent = v;
      else if (k.slice(0, 2) === "on") n.addEventListener(k.slice(2), v);
      else n.setAttribute(k, v === true ? "" : v);
    });
    (kids || []).forEach(function (c) {
      if (c !== null && c !== undefined) n.appendChild(typeof c === "string" ? document.createTextNode(c) : c);
    });
    return n;
  }
  function ico(name) { return '<svg class="icon" aria-hidden="true" focusable="false"><use href="#' + name + '"></use></svg>'; }
  var motionQ = window.matchMedia ? window.matchMedia("(prefers-reduced-motion: reduce)") : { matches: false };
  function calm() { return !!motionQ.matches; }
  function fmt(n) { return Math.round(n).toLocaleString("en-GB"); }
  function shuffle(a) {
    a = a.slice();
    for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t; }
    return a;
  }
  function pick(list) { return list[Math.floor(Math.random() * list.length)]; }
  function ordinal(n) { return n + (n === 1 ? "st" : n === 2 ? "nd" : n === 3 ? "rd" : "th"); }
  function plural(n, word) { return n + " " + word + (n === 1 ? "" : "s"); }
  function words(text) { var t = String(text || "").trim(); return t ? t.split(/\s+/).length : 0; }
  function stripTags(html) { var d = document.createElement("div"); d.innerHTML = html; return d.textContent || ""; }

  /* ------------------------------------------------------------ drawings */
  var SHAPES = [
    '<path d="M12 3.5 21.5 20h-19Z"/>',
    '<path d="M12 2.5 21.5 12 12 21.5 2.5 12Z"/>',
    '<circle cx="12" cy="12" r="9.5"/>',
    '<rect x="3.5" y="3.5" width="17" height="17" rx="2.5"/>',
    '<path d="M12 2.6l2.8 5.7 6.2.9-4.5 4.4 1.1 6.2-5.6-2.9-5.6 2.9 1.1-6.2-4.5-4.4 6.2-.9Z"/>',
    '<path d="M7 3.2h10l5 8.8-5 8.8H7l-5-8.8Z"/>'
  ];
  var SHAPE_NAMES = ["triangle", "diamond", "circle", "square", "star", "hexagon"];
  function shape(i) { return '<span class="st-shape" aria-hidden="true"><svg viewBox="0 0 24 24">' + SHAPES[i % SHAPES.length] + "</svg></span>"; }
  var FLAME = '<svg viewBox="0 0 16 20" aria-hidden="true" focusable="false"><path d="M8 .5c1 3.4 5.6 5.8 5.6 10.8A5.6 5.6 0 0 1 2.4 11.3c0-3 2-4.6 2.6-6.6 1 1.4 1.3 2.6 1 4 1.7-1.3 2.4-4.7 2-8.2Z" fill="#FB923C"/>' +
    '<path d="M8 8.6c.6 2 2.9 3 2.9 5.5a2.9 2.9 0 0 1-5.8 0c0-1.6 1-2.4 1.5-3.6.5.7.7 1.3.6 2 .8-.8 1-2.3.8-3.9Z" fill="#FDE047"/></svg>';
  var FACES = [
    '<rect x="7" y="10" width="18" height="15" rx="5" fill="#fff"/><circle cx="12.5" cy="17" r="2.2" fill="#1E293B"/><circle cx="19.5" cy="17" r="2.2" fill="#1E293B"/><path d="M13 21.6h6" stroke="#1E293B" stroke-width="1.6" stroke-linecap="round"/><path d="M16 10V6.5" stroke="#fff" stroke-width="1.8"/><circle cx="16" cy="5.2" r="2.1" fill="#FDE047"/>',
    '<rect x="6" y="9" width="20" height="16" rx="8" fill="#fff"/><rect x="9" y="14" width="14" height="5" rx="2.5" fill="#1E293B"/><circle cx="13" cy="16.5" r="1.2" fill="#5EEAD4"/><circle cx="19" cy="16.5" r="1.2" fill="#5EEAD4"/><path d="M11 9 9 5M21 9l2-4" stroke="#fff" stroke-width="1.8" stroke-linecap="round"/>',
    '<path d="M8 12a8 8 0 0 1 16 0v8a5 5 0 0 1-5 5h-6a5 5 0 0 1-5-5Z" fill="#fff"/><circle cx="12.6" cy="16" r="2" fill="#1E293B"/><circle cx="19.4" cy="16" r="2" fill="#1E293B"/><path d="M13.5 20.5q2.5 2 5 0" fill="none" stroke="#1E293B" stroke-width="1.6" stroke-linecap="round"/><rect x="4" y="13" width="3" height="6" rx="1.5" fill="#fff"/><rect x="25" y="13" width="3" height="6" rx="1.5" fill="#fff"/>',
    '<rect x="7" y="8" width="18" height="17" rx="3" fill="#fff"/><rect x="9.5" y="12.5" width="5" height="4" rx="1" fill="#1E293B"/><rect x="17.5" y="12.5" width="5" height="4" rx="1" fill="#1E293B"/><path d="M11 21h10" stroke="#1E293B" stroke-width="1.6" stroke-dasharray="2 1.6"/><path d="M16 8V4.5M13 4.5h6" stroke="#fff" stroke-width="1.8" stroke-linecap="round"/>'
  ];
  function avatar(p) {
    if (p.you) return el("span", { class: "st-av st-av-you", "aria-hidden": "true", text: (p.name.charAt(0) || "Y").toUpperCase() });
    return el("span", { class: "st-av", style: "--av:" + p.av, "aria-hidden": "true", html: '<svg viewBox="0 0 32 32">' + FACES[p.face] + "</svg>" });
  }
  function bigStar(on) {
    return '<svg class="st-bigstar' + (on ? "" : " is-off") + '" viewBox="0 0 64 62" aria-hidden="true"><path d="M32 3l8.6 17.6 19.4 2.8-14 13.7 3.3 19.3L32 47.3 14.7 56.4 18 37.1 4 23.4l19.4-2.8Z" fill="' +
      (on ? "#FBBF24" : "#C4B5FD") + '" stroke="' + (on ? "#B45309" : "#7C3AED") + '" stroke-width="3" stroke-linejoin="round"/>' +
      (on ? '<path d="M24 22l5-1.5" stroke="#FEF3C7" stroke-width="3" stroke-linecap="round"/>' : "") + "</svg>";
  }
  var MEDAL_ART = {
    crown: '<path d="M18 36 20 22l7 7 5-10 5 10 7-7 2 14Z" fill="#FDE047" stroke="#92400E" stroke-width="2" stroke-linejoin="round"/>',
    podium: '<path d="M20 40V31h8v-7h8v11h8v5Z" fill="#fff" stroke="#1E293B" stroke-width="2" stroke-linejoin="round"/>',
    sweep: '<path d="M21 31l7 7 15-15" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>',
    fire: '<path d="M32 18c2 6 9 9 9 16a9 9 0 0 1-18 0c0-5 3-7 4-10 1.6 2.3 2 4 1.6 6.2C31 28 32.6 24 32 18Z" fill="#FDE047" stroke="#9A3412" stroke-width="2"/>',
    bolt: '<path d="M35 17 23 33h8l-3 13 13-17h-8Z" fill="#FDE047" stroke="#713F12" stroke-width="2" stroke-linejoin="round"/>',
    pen: '<path d="M22 41l3-9 14-14 6 6-14 14Z" fill="#fff" stroke="#1E293B" stroke-width="2" stroke-linejoin="round"/><path d="M22 41l9-3" stroke="#1E293B" stroke-width="2"/>',
    bulb: '<path d="M32 17a9 9 0 0 0-5 16.5V37h10v-3.5A9 9 0 0 0 32 17Z" fill="#FDE047" stroke="#713F12" stroke-width="2"/><path d="M28 41h8" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/>',
    fish: '<path d="M19 29c4.5-6.5 13-7 18.5-2.2L43 22.5v13L37.5 31.2C32 36 23.5 35.5 19 29Z" fill="#FDBA74" stroke="#9A3412" stroke-width="2" stroke-linejoin="round"/><circle cx="25" cy="28" r="1.8" fill="#1E293B"/>',
    cards: '<rect x="19" y="18" width="14" height="19" rx="3" fill="#fff" stroke="#1E293B" stroke-width="2" transform="rotate(-10 26 27.5)"/><rect x="31" y="18" width="14" height="19" rx="3" fill="#FDE047" stroke="#1E293B" stroke-width="2" transform="rotate(9 38 27.5)"/>'
  };
  function medalSvg(art, colour) {
    return '<svg viewBox="0 0 64 74" aria-hidden="true"><path d="M20 2h10l6 20h-10ZM44 2H34l-6 20h10Z" fill="#EF4444"/><path d="M26 2h4l6 20h-4ZM38 2h-4l-6 20h4Z" fill="#fff" opacity=".55"/>' +
      '<circle cx="32" cy="44" r="25" fill="' + colour + '" stroke="#fff" stroke-width="3"/><circle cx="32" cy="44" r="19" fill="none" stroke="#fff" stroke-opacity=".45" stroke-width="2" stroke-dasharray="3 3"/>' +
      '<g transform="translate(0 15)">' + MEDAL_ART[art] + "</g></svg>";
  }

  /* --------------------------------------------------------------- sound */
  var actx = null;
  function audio() {
    if (!actx) { var A = window.AudioContext || window.webkitAudioContext; if (!A) return null; try { actx = new A(); } catch (e) { return null; } }
    if (actx.state === "suspended") actx.resume();
    return actx;
  }
  function tone(f, start, dur, type, vol) {
    var a = audio(); if (!a) return;
    var o = a.createOscillator(), g = a.createGain(), t = a.currentTime + start;
    o.type = type || "triangle"; o.frequency.setValueAtTime(f, t);
    g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(vol || 0.1, t + 0.015);
    g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    o.connect(g); g.connect(a.destination); o.start(t); o.stop(t + dur + 0.05);
  }
  var SOUNDS = {
    tick: function () { tone(1180, 0, 0.05, "square", 0.025); },
    count: function () { tone(660, 0, 0.16, "triangle", 0.09); },
    go: function () { tone(988, 0, 0.12, "triangle", 0.1); tone(1318, 0.1, 0.25, "triangle", 0.1); },
    good: function () { tone(523, 0, 0.12); tone(659, 0.09, 0.12); tone(784, 0.18, 0.22); },
    bad: function () { tone(233, 0, 0.2, "sine", 0.1); tone(196, 0.14, 0.26, "sine", 0.09); },
    pop: function () { tone(880, 0, 0.06, "triangle", 0.05); },
    board: function () { [392, 494, 587].forEach(function (f, i) { tone(f, i * 0.09, 0.18, "triangle", 0.08); }); },
    win: function () { [523, 659, 784, 1046, 784, 1046, 1318].forEach(function (f, i) { tone(f, i * 0.11, 0.26, "triangle", 0.1); }); }
  };
  var opts = store.get(OPTS, null) || {};
  if (typeof opts.timer !== "boolean") opts.timer = true;
  if (typeof opts.sound !== "boolean") opts.sound = false;
  function sfx(name) { if (opts.sound && SOUNDS[name]) { try { SOUNDS[name](); } catch (e) { /* sound is a nicety */ } } }

  /* ------------------------------------------------------------ confetti */
  function confetti(canvas, ms) {
    if (calm() || !canvas || !canvas.getContext) return;
    var ctx = canvas.getContext("2d"), W, H, t0 = performance.now(), parts = [];
    var colours = ["#D7263D", "#1F5FD1", "#F2B705", "#1E7B34", "#FDE047", "#F472B6", "#FFFFFF"];
    var dpr = Math.min(2, window.devicePixelRatio || 1);
    W = canvas.clientWidth; H = canvas.clientHeight;
    canvas.width = W * dpr; canvas.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    for (var i = 0; i < 160; i++) {
      var left = i % 2 === 0;
      parts.push({ x: left ? -10 : W + 10, y: H * (0.25 + Math.random() * 0.35), vx: (left ? 1 : -1) * (Math.random() * 9 + 4),
                   vy: -Math.random() * 12 - 3, r: Math.random() * 7 + 5, a: Math.random() * 6, va: (Math.random() - 0.5) * 0.3,
                   c: colours[i % colours.length], s: i % 4 });
    }
    function frame(t) {
      var age = t - t0;
      ctx.clearRect(0, 0, W, H);
      parts.forEach(function (p) {
        p.vy += 0.28; p.vx *= 0.992; p.x += p.vx; p.y += p.vy; p.a += p.va;
        ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.a); ctx.globalAlpha = Math.max(0, 1 - age / ms); ctx.fillStyle = p.c;
        ctx.beginPath();
        if (p.s === 0) ctx.rect(-p.r / 2, -p.r / 4, p.r, p.r / 2);
        else if (p.s === 1) ctx.arc(0, 0, p.r / 2.4, 0, 6.3);
        else if (p.s === 2) { ctx.moveTo(0, -p.r / 2); ctx.lineTo(p.r / 2, p.r / 2); ctx.lineTo(-p.r / 2, p.r / 2); }
        else { ctx.moveTo(0, -p.r / 2); ctx.lineTo(p.r / 2, 0); ctx.lineTo(0, p.r / 2); ctx.lineTo(-p.r / 2, 0); }
        ctx.fill(); ctx.restore();
      });
      if (age < ms) requestAnimationFrame(frame); else ctx.clearRect(0, 0, W, H);
    }
    requestAnimationFrame(frame);
  }

  function countUp(node, from, to, ms, prefix) {
    prefix = prefix || "";
    if (calm() || !ms) { node.textContent = prefix + fmt(to); return; }
    var t0 = performance.now();
    (function step(t) {
      var k = Math.min(1, (t - t0) / ms), e = 1 - Math.pow(1 - k, 3);
      node.textContent = prefix + fmt(from + (to - from) * e);
      if (k < 1) requestAnimationFrame(step); else node.textContent = prefix + fmt(to);
    })(t0);
  }
  function escHtml(s) { return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }

  /* --------------------------------------------------------------- Pixel */
  var pxSeq = 0;
  function pixel(mood) {
    var tpl = document.getElementById("st-pixel");
    if (!tpl) return null;
    var svg = (tpl.content ? tpl.content.firstElementChild : tpl.firstElementChild).cloneNode(true);
    pxSeq += 1;
    var map = {};
    Array.prototype.forEach.call(svg.querySelectorAll("[id]"), function (n) { map[n.id] = n.id + "-s" + pxSeq; n.id = map[n.id]; });
    Array.prototype.forEach.call(svg.querySelectorAll("[fill^='url(#']"), function (n) {
      var m = /^url\(#([^)]+)\)$/.exec(n.getAttribute("fill"));
      if (m && map[m[1]]) n.setAttribute("fill", "url(#" + map[m[1]] + ")");
    });
    svg.setAttribute("aria-hidden", "true");
    setMood(svg, mood || "idle");
    return svg;
  }
  /* A pose, keeping whatever Pixel is wearing. */
  function setMood(svg, mood) {
    if (!svg) return;
    svg._mood = mood;
    svg.setAttribute("class", "px is-" + mood + (svg._wear ? " " + svg._wear : ""));
  }
  function wear(svg, list) {
    if (!svg) return;
    svg._wear = (list || []).map(function (w) { return "wear-" + w; }).join(" ");
    setMood(svg, svg._mood || "idle");
  }

  /* ================================================================ HUB */
  var TASKS = ["quiz", "cat", "match"];
  var TASK_NAMES = { quiz: "Quiz Challenge", cat: "This or That", match: "Memory Match" };
  /* The Quiz Challenge keeps the lesson's own key, so results saved before
     the other tasks existed still count. */
  function recKey(base, task) { return task === "quiz" ? base : base + "/" + task; }
  var records = store.get(RECORDS, {}) || {};
  Array.prototype.forEach.call(document.querySelectorAll("[data-st-key]"), function (card) {
    var base = card.getAttribute("data-st-key");
    Array.prototype.forEach.call(card.querySelectorAll("[data-st-task]"), function (b) {
      var task = b.getAttribute("data-st-task"), r = records[recKey(base, task)], n = r ? r.s : 0;
      Array.prototype.forEach.call(b.querySelectorAll("[data-st-stars] .icon"), function (s, i) { s.classList.toggle("is-on", i < n); });
      var sr = b.querySelector("[data-st-sr]");
      if (sr) sr.textContent = TASK_NAMES[task] + ": " + (r ? n + " of 3 stars." : "not played yet.");
      b.classList.toggle("is-played", !!r);
    });
  });

  /* Hooks for tools/check_stretch.mjs and the browser tests. typedRight is
     hoisted, so it is ready here even on a page with no game. */
  var hooks = window.MskStretch = { typedRight: typedRight };

  /* =============================================================== GAME */
  var app = document.getElementById("st");
  var dataEl = document.getElementById("st-data");
  if (!app || !dataEl) return;
  var D;
  try { D = JSON.parse(dataEl.textContent); } catch (e) { return; }
  app.setAttribute("data-motion", calm() ? "calm" : "full");

  var RIVALS = [
    { id: "ada", name: "Ada", av: "#DB2777", face: 0, skill: 0.84, pace: 0.2 },
    { id: "alan", name: "Alan", av: "#0284C7", face: 1, skill: 0.78, pace: 0.28 },
    { id: "grace", name: "Grace", av: "#059669", face: 2, skill: 0.71, pace: 0.24 },
    { id: "tim", name: "Tim", av: "#EA580C", face: 3, skill: 0.63, pace: 0.34 }
  ];
  var KIND = {
    choice: { label: "Pick one", odds: 1 },
    tf: { label: "True or false", odds: 1.06 },
    multi: { label: "Pick more than one", odds: 0.8 },
    order: { label: "Put in order", odds: 0.76 },
    type: { label: "Type it", odds: 0.8 }
  };
  var RIGHT = ["Correct!", "Brilliant!", "Spot on!", "Nailed it!", "Superb!", "Yes!"];
  var WRONG = ["Not quite", "So close", "Not this time", "Unlucky"];
  var PER_MARK = { short: 400, long: 500 };

  var lobby = document.getElementById("st-lobby");
  var stage = document.getElementById("st-stage");
  var starts = {};
  Array.prototype.forEach.call(lobby.querySelectorAll("[data-st-start]"), function (b) {
    starts[b.getAttribute("data-st-start")] = b;
  });
  var nameIn = document.getElementById("st-name");
  var lobbyCat = lobby.querySelector(".st-px");
  if (lobbyCat) setMood(lobbyCat, "wave");
  function art(task) {
    var a = lobby.querySelector('[data-st-art="' + task + '"]');
    return a ? a.innerHTML : "";
  }

  /* ------------------------------------------------------------- lobby */
  function paintBest() {
    var all = store.get(RECORDS, {}) || {};
    TASKS.forEach(function (task) {
      var best = lobby.querySelector('[data-st-best="' + task + '"]');
      var r = all[recKey(D.key, task)];
      if (!best) return;
      if (!r) { best.hidden = true; return; }
      best.hidden = false;
      best.innerHTML = '<span class="st-stars" aria-hidden="true">' + [0, 1, 2].map(function (i) {
        return '<svg class="icon' + (i < r.s ? " is-on" : "") + '" aria-hidden="true" focusable="false"><use href="#i-star"></use></svg>';
      }).join("") + "</span>";
      best.appendChild(document.createTextNode("Your best: " + plural(r.s, "star") + ", " + fmt(r.b) + " points"));
    });
  }
  paintBest();
  if (nameIn) {
    nameIn.value = opts.name || "";
    nameIn.addEventListener("input", function () { opts.name = nameIn.value.trim().slice(0, 16); store.set(OPTS, opts); });
  }
  Array.prototype.forEach.call(lobby.querySelectorAll("[data-st-opt]"), function (b) {
    var key = b.getAttribute("data-st-opt");
    b.setAttribute("aria-pressed", String(!!opts[key]));
    b.addEventListener("click", function () {
      opts[key] = !opts[key];
      b.setAttribute("aria-pressed", String(opts[key]));
      store.set(OPTS, opts);
      if (key === "sound" && opts.sound) sfx("pop");
    });
  });
  function printAs(mode) {
    var root = document.documentElement;
    var copy = null;
    if (mode === "result") {
      var res = stage.querySelector(".st-results");
      if (!res) return;
      copy = el("div", { class: "st-printout" });
      copy.appendChild(res.cloneNode(true));
      Array.prototype.forEach.call(copy.querySelectorAll(".st-res-go, .px, canvas"), function (n) { n.remove(); });
      Array.prototype.forEach.call(copy.querySelectorAll("[id]"), function (n) { n.removeAttribute("id"); });
      document.body.appendChild(copy);
    }
    var cls = mode === "result" ? ["st-print-result"] : mode === "answers" ? ["st-print-sheet", "st-print-answers"] : ["st-print-sheet"];
    var key = document.getElementById("st-key");
    var wasOpen = key && key.open;
    if (key && mode === "answers") key.open = true;
    cls.forEach(function (c) { root.classList.add(c); });
    var done = function () {
      cls.forEach(function (c) { root.classList.remove(c); });
      if (copy && copy.parentNode) copy.parentNode.removeChild(copy);
      if (key) key.open = wasOpen;
      window.removeEventListener("afterprint", done);
    };
    window.addEventListener("afterprint", done);
    window.print();
    setTimeout(done, 1500);
  }
  Array.prototype.forEach.call(document.querySelectorAll("[data-st-print]"), function (b) {
    b.addEventListener("click", function () { printAs(b.getAttribute("data-st-print")); });
  });

  /* ------------------------------------------------------------- state */
  var G = null;
  var T = null;           // the running question clock
  var ui = {};

  function you() { return { id: "you", you: true, name: (opts.name || "").trim() || "You", pts: G.blitzPts }; }
  function standings() {
    var all = [you()].concat(G.rivals);
    return all.slice().sort(function (a, b) { return b.pts - a.pts || (a.you ? -1 : b.you ? 1 : 0); });
  }
  function rankOf(list) { for (var i = 0; i < list.length; i++) if (list[i].you) return i + 1; return list.length; }
  function rankLine(list) {
    var r = rankOf(list);
    if (r === 1) {
      var gap = list[0].pts - (list[1] ? list[1].pts : 0);
      return gap > 0 ? "You're in the lead by " + fmt(gap) + " points" : "You're in the lead";
    }
    var ahead = list[r - 2];
    return "You're " + ordinal(r) + ", " + fmt(ahead.pts - list[r - 1].pts) + " points behind " + ahead.name;
  }

  /* ------------------------------------------------------------- stage */
  function buildStage(task) {
    stage.innerHTML = "";
    stage.setAttribute("role", "dialog");
    stage.setAttribute("aria-modal", "true");
    stage.setAttribute("aria-label", TASK_NAMES[task] + ": " + D.lesson);
    stage.setAttribute("data-motion", calm() ? "calm" : "full");
    stage.appendChild(el("div", { class: "st-bg", "aria-hidden": "true", html: lobby.querySelector(".st-bg") ? lobby.querySelector(".st-bg").innerHTML : "" }));
    ui.confetti = el("canvas", { class: "st-confetti", "aria-hidden": "true" });
    ui.l1 = el("b", { text: TASK_NAMES[task] });
    ui.l2 = el("span", { text: "" });
    ui.streakN = el("span", { text: "0" });
    ui.streak = el("span", { class: "st-chip st-chip-streak", hidden: true, title: "Answer streak", html: FLAME }, []);
    ui.streak.appendChild(ui.streakN);
    var chips;
    if (task === "quiz") {
      ui.rank = el("span", { class: "st-chip st-chip-rank", hidden: true });
      ui.score = el("span", { text: "0" });
      ui.scoreChip = el("span", { class: "st-chip st-chip-score" }, [el("small", { text: "Points" }), ui.score]);
      chips = [ui.rank, ui.scoreChip, ui.streak];
    } else if (task === "cat") {
      ui.fishN = el("span", { text: "0" });
      ui.fishChip = el("span", { class: "st-chip st-chip-fish" }, [el("span", { class: "st-fish", html: FISH }), el("small", { text: "Treats" }), ui.fishN]);
      chips = [ui.fishChip, ui.streak];
    } else {
      ui.pairsN = el("span", { text: "0 / " + D.pairs.length });
      ui.missN = el("span", { text: "0" });
      ui.timeN = el("span", { text: "0:00" });
      ui.pairsChip = el("span", { class: "st-chip" }, [el("small", { text: "Pairs" }), ui.pairsN]);
      ui.missChip = el("span", { class: "st-chip" }, [el("small", { text: "Misses" }), ui.missN]);
      ui.timeChip = el("span", { class: "st-chip st-chip-time", hidden: !opts.timer }, [el("span", { html: ico("i-timer") }).firstChild, ui.timeN]);
      chips = [ui.pairsChip, ui.missChip, ui.timeChip];
    }
    ui.dots = el("div", { class: "st-dots", "aria-hidden": "true" });
    var top = el("div", { class: "st-top" }, [
      el("button", { class: "st-x", type: "button", "aria-label": "Leave the game", html: ico("i-cross"), onclick: function () { leave(true); } }),
      el("div", { class: "st-top-label" }, [ui.l1, ui.l2]),
      el("span", { class: "st-top-gap" }),
      el("div", { class: "st-chips" }, chips),
      ui.dots
    ]);
    ui.screen = el("div", { class: "st-screen" });
    ui.body = el("div", { class: "st-body" }, [ui.screen]);
    ui.live = el("p", { class: "st-live", "aria-live": "polite" });
    stage.appendChild(ui.confetti);
    stage.appendChild(top);
    stage.appendChild(ui.body);
    stage.appendChild(ui.live);
  }
  function label(round, sub) { ui.l1.textContent = round; ui.l2.textContent = sub || ""; }
  function say(text) { ui.live.textContent = ""; setTimeout(function () { ui.live.textContent = text; }, 30); }
  function screen(cls) {
    stopClock();
    ui.tiles = null; ui.typed = null; ui.reveal = null;
    ui.screen.className = "st-screen st-screen-in " + (cls || "");
    ui.screen.innerHTML = "";
    void ui.screen.offsetWidth;
    ui.body.scrollTop = 0;
    return ui.screen;
  }
  function focusFirst(node) { if (node) setTimeout(function () { try { node.focus({ preventScroll: false }); } catch (e) { node.focus(); } }, 40); }
  function paintChips(bump) {
    ui.score.textContent = fmt(G.blitzPts + G.writtenPts);
    if (bump) { ui.scoreChip.classList.remove("is-bump"); void ui.scoreChip.offsetWidth; ui.scoreChip.classList.add("is-bump"); }
    var showStreak = G.round === "blitz" && G.streak >= 2;
    ui.streak.hidden = !showStreak;
    ui.streakN.textContent = String(G.streak);
    ui.streak.classList.toggle("is-hot", G.streak >= 3);
    ui.streak.setAttribute("aria-label", "Answer streak " + G.streak);
    if (G.round === "blitz" && G.times.length > 0) {
      ui.rank.hidden = false;
      ui.rank.textContent = ordinal(rankOf(standings()));
      ui.rank.setAttribute("aria-label", "Your place: " + ordinal(rankOf(standings())));
    } else ui.rank.hidden = true;
  }
  function paintDots(list, now) {
    ui.dots.innerHTML = "";
    list.forEach(function (state, i) {
      ui.dots.appendChild(el("i", { class: state === 1 ? "is-ok" : state === 0 ? "is-bad" : i === now ? "is-now" : "" }));
    });
  }

  function lockScroll(on) { document.documentElement.classList.toggle("st-locked", on); }
  function begin(task) {
    task = TASK_NAMES[task] ? task : "quiz";
    if (task === "quiz") {
      G = { round: "blitz", qi: 0, streak: 0, bestStreak: 0, right: 0, blitzPts: 0, writtenPts: 0, times: [], marks: [],
            rivals: RIVALS.map(function (r) { return { id: r.id, name: r.name, av: r.av, face: r.face, skill: r.skill, pace: r.pace, pts: 0, streak: 0 }; }),
            order: ["you", "ada", "alan", "grace", "tim"], written: { short: [], long: [] }, done: false };
    } else {
      G = { round: task, qi: 0, streak: 0, bestStreak: 0, right: 0, pts: 0, answers: [], done: false, locked: false };
    }
    G.task = task;
    buildStage(task);
    stage.hidden = false;
    stage.setAttribute("data-round", task === "quiz" ? "blitz" : task);
    lockScroll(true);
    if (task === "quiz") splash("blitz");
    else if (task === "cat") catSplash();
    else matchSplash();
  }
  function leave(ask) {
    if (ask && G && !G.done && !window.confirm("Leave the game? This game's score will not be saved.")) return;
    var task = G ? G.task : "quiz";
    stopClock();
    if (G && G.tick) clearInterval(G.tick);
    if (G && G.busy) clearTimeout(G.busy);
    stage.hidden = true;
    stage.innerHTML = "";
    lockScroll(false);
    G = null;
    paintBest();
    focusFirst(starts[task]);
  }
  TASKS.forEach(function (task) {
    if (starts[task]) starts[task].addEventListener("click", function () { begin(task); });
  });

  /* Tab stays inside the game, Escape offers to leave, and number keys pick
     tiles. Listened for on the document, not the stage, because focus can land
     on the page itself for a moment when one screen replaces another. */
  document.addEventListener("keydown", function (e) {
    if (!G || stage.hidden) return;
    if (e.key === "Escape") { e.preventDefault(); leave(true); return; }
    if (e.key === "Tab") {
      var f = Array.prototype.filter.call(stage.querySelectorAll("button, input, textarea, select, a[href], [tabindex='0']"), function (n) {
        return !n.disabled && n.offsetParent !== null;
      });
      if (!f.length) return;
      var first = f[0], last = f[f.length - 1];
      if (!stage.contains(document.activeElement)) { e.preventDefault(); (e.shiftKey ? last : first).focus(); }
      else if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
      else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
      return;
    }
    var tag = (e.target.tagName || "").toLowerCase();
    if (tag === "input" || tag === "textarea" || tag === "select" || e.ctrlKey || e.metaKey || e.altKey) return;
    if (/^[1-6]$/.test(e.key) && ui.tiles && !G.locked) {
      var t = ui.tiles[parseInt(e.key, 10) - 1];
      if (t && !t.disabled) { e.preventDefault(); t.click(); }
    }
  });

  /* ------------------------------------------------------------- splash */
  var ROUND = {
    blitz: { n: 1, name: "Quiz Blitz", art: 0 },
    short: { n: 2, name: "Quick Fire", art: 1 },
    long: { n: 3, name: "Big Think", art: 2 }
  };
  function roundArt(kind) {
    var icons = lobby.querySelectorAll(".st-round-ico");
    var i = ROUND[kind].art;
    return icons[i] ? icons[i].innerHTML : "";
  }
  function splash(kind) {
    G.round = kind;
    stage.setAttribute("data-round", kind);
    var R = ROUND[kind];
    label(R.name, "Round " + R.n + " of 3");
    ui.dots.innerHTML = "";
    paintChips(false);
    var s = screen("st-splash");
    s.appendChild(el("span", { class: "st-splash-tag", text: "Round " + R.n }));
    s.appendChild(el("div", { class: "st-splash-ico", "aria-hidden": "true", html: roundArt(kind) }));
    var h = el("h2", { tabindex: "-1", text: R.name });
    s.appendChild(h);
    var sub;
    if (kind === "blitz") sub = plural(D.blitz.length, "question") + (opts.timer ? " against the clock." : ", no clock.") + " Race four computer players to the podium.";
    else if (kind === "short") sub = plural(D.short.length, "short answer") + ". The marker looks for the key points.";
    else sub = plural(D.long.length, "long answer") + ". Explain fully: every mark point counts.";
    s.appendChild(el("p", { text: sub }));
    if (kind === "blitz") {
      var row = el("div", { class: "st-rivals" });
      G.rivals.forEach(function (r) { row.appendChild(el("span", { class: "st-rival" }, [avatar(r), r.name])); });
      s.appendChild(row);
      var go = el("button", { class: "st-go", type: "button", html: ico("i-play") + " Ready" });
      s.appendChild(go);
      go.addEventListener("click", function () { countdown(s, go); });
      focusFirst(go);
    } else {
      var next = el("button", { class: "st-go", type: "button", html: ico("i-play") + " Go" });
      next.addEventListener("click", function () { written(kind, 0); });
      s.appendChild(next);
      sfx("board");
      focusFirst(next);
    }
    say("Round " + R.n + ": " + R.name + ". " + sub);
  }
  function countdown(s, go) {
    go.remove();
    if (calm()) { blitz(0); return; }
    var c = el("div", { class: "st-count", "aria-hidden": "true" });
    s.appendChild(c);
    var n = 3, game = G;
    (function tick() {
      if (G !== game) return;
      if (n === 0) { sfx("go"); blitz(0); return; }
      c.textContent = String(n);
      c.classList.remove("is-pop"); void c.offsetWidth; c.classList.add("is-pop");
      sfx("count");
      n -= 1;
      setTimeout(tick, 800);
    })();
  }

  /* -------------------------------------------------------------- clock */
  function stopClock() { if (T) { T.stop(); T = null; } }
  function clock(limitMs, ring, num, box, onEnd) {
    var C = 2 * Math.PI * 46, t0 = performance.now(), raf = 0, stopped = false, lastWhole = -1;
    ring.style.strokeDasharray = C.toFixed(2);
    var api = {
      elapsed: function () { return performance.now() - t0; },
      stop: function () { stopped = true; cancelAnimationFrame(raf); }
    };
    if (!opts.timer) { box.classList.add("is-off"); num.textContent = "No clock"; return api; }
    (function frame(now) {
      if (stopped) return;
      var left = Math.max(0, limitMs - (now - t0));
      ring.style.strokeDashoffset = (C * (1 - left / limitMs)).toFixed(2);
      var whole = Math.ceil(left / 1000);
      if (whole !== lastWhole) {
        lastWhole = whole;
        num.textContent = String(whole);
        box.classList.toggle("is-mid", left <= limitMs * 0.5 && left > 5000);
        box.classList.toggle("is-low", left <= 5000);
        if (left <= 5000 && left > 0) sfx("tick");
        if (whole === 5) say("5 seconds left");
      }
      if (left <= 0) { stopped = true; onEnd(); return; }
      raf = requestAnimationFrame(frame);
    })(t0);
    return api;
  }

  /* --------------------------------------------------------- quiz blitz */
  function blitzDots() {
    return D.blitz.map(function (q, i) { return i < G.times.length ? (G.times[i].ok ? 1 : 0) : -1; });
  }
  function blitz(i) {
    if (!G) return;
    G.round = "blitz"; G.qi = i; G.locked = false;
    var q = D.blitz[i];
    label("Quiz Blitz", "Question " + (i + 1) + " of " + D.blitz.length);
    paintDots(blitzDots(), i);
    paintChips(false);
    var s = screen("st-blitz st-kind-" + q.k);

    var card = el("div", { class: "st-qcard" });
    card.appendChild(el("p", { class: "st-qmeta", html: "<span>Question " + (i + 1) + '</span><span class="st-kind">' +
      (q.k === "multi" ? "Pick " + q.n : KIND[q.k].label) + "</span>" }));
    var h = el("h2", { class: "st-qtext", tabindex: "-1", html: q.q });
    card.appendChild(h);
    if (q.c) card.appendChild(el("pre", { class: "st-code" }, [el("code", { html: q.c })]));
    var hint = q.k === "multi" ? "Pick " + q.n + " answers, then lock them in." : q.k === "order" ? "Tap them in order, first to last." :
      q.k === "type" ? "Type your answer, then press Enter." : "";
    if (hint) card.appendChild(el("p", { class: "st-qhint", text: hint }));

    var ring = document.createElementNS("http://www.w3.org/2000/svg", "circle");
    var num = el("span", { class: "st-timer-n" });
    var box = el("div", { class: "st-timer", role: "timer", "aria-label": opts.timer ? q.t + " seconds to answer" : "No clock" });
    box.innerHTML = '<svg viewBox="0 0 104 104" aria-hidden="true"><circle class="st-ring-bg" cx="52" cy="52" r="46"/></svg>';
    ring.setAttribute("class", "st-ring"); ring.setAttribute("cx", "52"); ring.setAttribute("cy", "52"); ring.setAttribute("r", "46");
    box.firstChild.appendChild(ring);
    box.appendChild(num);
    G.cat = pixel("think");
    var side = el("div", { class: "st-side" }, [box, G.cat ? el("div", { class: "st-host" }, [G.cat]) : null]);
    s.appendChild(el("div", { class: "st-qrow" }, [card, side]));

    ui.tiles = [];
    var area = el("div", { class: "st-play" });
    s.appendChild(area);
    if (q.k === "choice") playChoice(q, area);
    else if (q.k === "tf") playTf(q, area);
    else if (q.k === "multi") playMulti(q, area);
    else if (q.k === "order") playOrder(q, area);
    else playType(q, area);
    ui.fb = el("div", { class: "st-fbslot" });
    s.appendChild(ui.fb);

    focusFirst(q.k === "type" ? ui.typed : h);
    T = clock(q.t * 1000, ring, num, box, function () { finish({ ok: false, late: true }); });
  }

  function tile(i, html, cls) {
    var b = el("button", { class: "st-tile st-c" + (i % 6) + (cls ? " " + cls : ""), type: "button",
                           "aria-label": SHAPE_NAMES[i % 6] + " " + (i + 1) + ": " + stripTags(html) },
      [el("span", { html: shape(i) }).firstChild, el("span", { class: "st-tile-t", html: html }),
       el("span", { class: "st-k", "aria-hidden": "true", text: String(i + 1) }),
       el("span", { class: "st-mark", "aria-hidden": "true" })]);
    ui.tiles.push(b);
    return b;
  }
  function grid(n, extra) {
    return el("div", { class: "st-answers" + (n === 3 ? " is-three" : n > 4 ? " is-many" : "") + (extra ? " " + extra : "") });
  }
  function markTile(b, right) {
    var m = b.querySelector(".st-mark");
    b.classList.add(right ? "is-right" : "is-wrong");
    m.innerHTML = ico(right ? "i-check" : "i-cross");
  }
  function lockTiles() { ui.tiles.forEach(function (b) { b.disabled = true; }); }

  function playChoice(q, area) {
    var opts2 = shuffle(q.o.map(function (h, k) { return { h: h, k: k }; }));
    var g = grid(opts2.length);
    var picked = null;
    ui.answer = q.o[0];
    ui.reveal = function () {
      lockTiles();
      ui.tiles.forEach(function (t, j) {
        if (opts2[j].k === 0) markTile(t, true);
        else if (t === picked) markTile(t, false);
        else t.classList.add("is-dim");
      });
    };
    opts2.forEach(function (o, i) {
      var b = tile(i, o.h);
      b.addEventListener("click", function () {
        if (G.locked) return;
        picked = b;
        finish({ ok: o.k === 0 });
      });
      g.appendChild(b);
    });
    area.appendChild(g);
  }
  function playTf(q, area) {
    var g = grid(2);
    area.classList.add("st-tf");
    var picked = null;
    ui.answer = q.a ? "True" : "False";
    ui.reveal = function () {
      lockTiles();
      ui.tiles.forEach(function (t, j) {
        if ((j === 0) === q.a) markTile(t, true); else if (t === picked) markTile(t, false); else t.classList.add("is-dim");
      });
    };
    [[true, "True", 1], [false, "False", 0]].forEach(function (v) {
      var b = el("button", { class: "st-tile st-c" + v[2], type: "button", "aria-label": v[1] + ", key " + (v[0] ? 1 : 2) },
        [el("span", { html: shape(v[2] === 1 ? 1 : 0) }).firstChild, el("span", { class: "st-tile-t", text: v[1] }),
         el("span", { class: "st-k", "aria-hidden": "true", text: v[0] ? "1" : "2" }), el("span", { class: "st-mark", "aria-hidden": "true" })]);
      ui.tiles.push(b);
      b.addEventListener("click", function () {
        if (G.locked) return;
        picked = b;
        finish({ ok: v[0] === q.a });
      });
      g.appendChild(b);
    });
    area.appendChild(g);
  }
  function playMulti(q, area) {
    var items = shuffle(q.o.map(function (h, k) { return { h: h, k: k }; }));
    var chosen = [];
    var g = grid(items.length);
    var lock = el("button", { class: "st-go", type: "button", disabled: true, html: ico("i-check") + " Lock in" });
    items.forEach(function (o, i) {
      var b = tile(i, o.h);
      b.setAttribute("aria-pressed", "false");
      b.addEventListener("click", function () {
        if (G.locked) return;
        var at = chosen.indexOf(i);
        if (at > -1) chosen.splice(at, 1); else chosen.push(i);
        b.classList.toggle("is-on", at < 0);
        b.setAttribute("aria-pressed", String(at < 0));
        lock.disabled = chosen.length !== q.n;
        sfx("pop");
      });
      g.appendChild(b);
    });
    ui.answer = q.o.slice(0, q.n).join("; ");
    ui.reveal = function () {
      lockTiles();
      lock.remove();
      ui.tiles.forEach(function (t, j) {
        var right = items[j].k < q.n, picked = chosen.indexOf(j) > -1;
        t.classList.remove("is-on");
        if (right) markTile(t, true); else if (picked) markTile(t, false); else t.classList.add("is-dim");
      });
    };
    lock.addEventListener("click", function () {
      if (G.locked || chosen.length !== q.n) return;
      finish({ ok: chosen.every(function (i) { return items[i].k < q.n; }) });
    });
    area.appendChild(g);
    area.appendChild(el("div", { class: "st-actions" }, [lock]));
  }
  function playOrder(q, area) {
    var items = shuffle(q.o.map(function (h, k) { return { h: h, k: k }; }));
    var placed = [];
    var slots = el("div", { class: "st-slots", style: "--n:" + Math.min(q.o.length, 4) });
    var slotEls = q.o.map(function (h, n) {
      var sl = el("button", { class: "st-slot", type: "button", "aria-label": "Place " + (n + 1) + ": empty" }, [el("b", { text: String(n + 1) }), el("span", { text: "" })]);
      sl.addEventListener("click", function () {
        if (G.locked || n >= placed.length) return;
        placed.splice(n, 1);
        paint();
      });
      slots.appendChild(sl);
      return sl;
    });
    var g = grid(items.length);
    var lock = el("button", { class: "st-go", type: "button", disabled: true, html: ico("i-check") + " Lock in" });
    var clear = el("button", { class: "st-ghost", type: "button", text: "Clear" });
    function paint() {
      slotEls.forEach(function (sl, n) {
        var it = placed[n] !== undefined ? items[placed[n]] : null;
        sl.classList.toggle("is-filled", !!it);
        sl.lastChild.innerHTML = it ? it.h : "";
        sl.setAttribute("aria-label", "Place " + (n + 1) + ": " + (it ? stripTags(it.h) + ". Activate to take it out." : "empty"));
      });
      ui.tiles.forEach(function (t, i) {
        var used = placed.indexOf(i) > -1;
        t.classList.toggle("is-used", used);
        t.disabled = used;
      });
      lock.disabled = placed.length !== items.length;
    }
    items.forEach(function (o, i) {
      var b = tile(i, o.h);
      b.addEventListener("click", function () {
        if (G.locked || placed.indexOf(i) > -1) return;
        placed.push(i);
        sfx("pop");
        paint();
        if (placed.length === items.length) focusFirst(lock);
      });
      g.appendChild(b);
    });
    clear.addEventListener("click", function () { if (!G.locked) { placed = []; paint(); } });
    ui.answer = q.o.join(" &rarr; ");
    ui.reveal = function () {
      lockTiles();
      lock.remove(); clear.remove();
      slotEls.forEach(function (sl, n) {
        var it = placed[n] !== undefined ? items[placed[n]] : null;
        var right = !!it && it.k === n;
        sl.disabled = true;
        sl.classList.add(right ? "is-right" : "is-wrong");
      });
      ui.tiles.forEach(function (t) { t.classList.add("is-dim"); });
    };
    lock.addEventListener("click", function () {
      if (G.locked || placed.length !== items.length) return;
      finish({ ok: placed.every(function (i, n) { return items[i].k === n; }) });
    });
    area.appendChild(slots);
    area.appendChild(g);
    area.appendChild(el("div", { class: "st-actions" }, [clear, lock]));
  }
  function plainAnswer(s) {
    return String(s || "").toLowerCase().replace(/[‘’]/g, "'").replace(/[“”]/g, '"').replace(/\s+/g, " ").trim()
      .replace(/^["']+|["']+$/g, "").replace(/\.$/, "").trim();
  }
  function typedRight(value, accept) {
    var g = plainAnswer(value), sq = g.replace(/ /g, "");
    if (!g) return false;
    return accept.some(function (a) {
      var w = plainAnswer(a), wsq = w.replace(/ /g, "");
      if (w === g || wsq === sq) return true;
      var num = /^-?\d[\d,]*(\.\d+)?$/;
      return num.test(wsq) && num.test(sq) && parseFloat(wsq.replace(/,/g, "")) === parseFloat(sq.replace(/,/g, ""));
    });
  }
  function playType(q, area) {
    var input = el("input", { type: "text", autocomplete: "off", spellcheck: "false", autocapitalize: "off", "aria-label": "Your answer" });
    var lock = el("button", { class: "st-go", type: "button", html: ico("i-check") + " Lock in" });
    ui.typed = input;
    ui.answer = escHtml(q.a[0]);
    ui.reveal = function () {
      input.readOnly = true;
      input.classList.add(typedRight(input.value, q.a) ? "is-right" : "is-wrong");
      lock.remove();
    };
    function go() {
      if (G.locked) return;
      if (!input.value.trim()) { input.focus(); return; }
      finish({ ok: typedRight(input.value, q.a) });
    }
    input.addEventListener("keydown", function (e) { if (e.key === "Enter") { e.preventDefault(); go(); } });
    lock.addEventListener("click", go);
    area.appendChild(el("div", { class: "st-typed" }, [input, lock]));
  }

  function points(ms, limit, streak) {
    var base = opts.timer ? Math.round(1000 * (1 - 0.5 * Math.min(1, ms / limit))) : 800;
    return { base: base, bonus: Math.min(Math.max(streak - 1, 0), 5) * 100 };
  }
  function rivalsPlay(q) {
    var limit = q.t * 1000;
    G.rivals.forEach(function (r) {
      var ok = Math.random() < Math.min(0.97, r.skill * KIND[q.k].odds);
      if (ok) {
        r.streak += 1;
        var p = points(limit * Math.min(0.95, Math.max(0.12, r.pace + Math.random() * 0.42)), limit, r.streak);
        r.pts += p.base + p.bonus;
      } else r.streak = 0;
    });
  }

  function finish(res) {
    if (!G || G.locked) return;
    G.locked = true;
    var q = D.blitz[G.qi];
    var ms = T ? T.elapsed() : 0;
    stopClock();
    var before = rankOf(standings());
    var gain = { base: 0, bonus: 0 };
    if (res.ok) {
      G.streak += 1; G.right += 1;
      G.bestStreak = Math.max(G.bestStreak, G.streak);
      gain = points(ms, q.t * 1000, G.streak);
      G.blitzPts += gain.base + gain.bonus;
    } else G.streak = 0;
    G.times.push({ ok: !!res.ok, ms: ms, limit: q.t * 1000 });
    rivalsPlay(q);
    if (ui.reveal) ui.reveal();
    paintDots(blitzDots(), -1);
    paintChips(res.ok);
    sfx(res.ok ? "good" : "bad");
    setMood(G.cat, res.ok ? (G.streak >= 3 ? "cheer" : "happy") : "think");

    var list = standings(), after = rankOf(list);
    var last = G.qi === D.blitz.length - 1, board = !last && (G.qi + 1) % 4 === 0;
    var head = res.late ? "Time's up!" : res.ok ? pick(RIGHT) : pick(WRONG);
    var cls = res.late ? "is-late" : res.ok ? "is-ok" : "is-bad";
    var rankMsg = rankLine(list) + (after < before ? ". Up " + plural(before - after, "place") + "!" : "");
    var pts = el("span", { class: "st-fb-pts", text: "+0" });
    var next = el("button", { class: "st-go", type: "button", html: (last ? "See the podium" : board ? "See the scoreboard" : "Next question") + " " + ico("i-arrow-right") });
    var expl = (res.ok ? "" : '<span class="st-fb-ans"><b>Answer:</b> ' + ui.answer + "</span>") + q.x;
    var fb = el("div", { class: "st-fb " + cls, role: "status" }, [
      el("span", { class: "st-fb-badge", "aria-hidden": "true", html: ico(res.ok ? "i-check" : res.late ? "i-clock" : "i-cross") }),
      el("div", { class: "st-fb-head" }, [el("b", { text: head }), el("span", { text: rankMsg })]),
      pts,
      G.streak >= 2 ? el("div", { class: "st-fb-streak", html: FLAME + "<span>Answer streak " + G.streak + (gain.bonus ? ": +" + gain.bonus + " bonus" : "") + "</span>" }) : null,
      el("p", { class: "st-fb-x", html: expl }),
      el("div", { class: "st-fb-go" }, [next])
    ]);
    ui.fb.appendChild(fb);
    countUp(pts, 0, gain.base + gain.bonus, 700, "+");
    next.addEventListener("click", function () {
      if (last) podium();
      else if (board) scoreboard(function () { blitz(G.qi + 1); });
      else blitz(G.qi + 1);
    });
    setTimeout(function () {
      try { fb.scrollIntoView({ behavior: calm() ? "auto" : "smooth", block: "nearest" }); } catch (e) { fb.scrollIntoView(false); }
      next.focus({ preventScroll: true });
    }, calm() ? 0 : 350);
  }

  /* ------------------------------------------------- scoreboard, podium */
  function scoreboard(next) {
    label("Quiz Blitz", "Scoreboard after " + plural(G.qi + 1, "question"));
    paintChips(false);
    var s = screen("st-board-wrap");
    var list = standings();
    var top = list[0].pts || 1;
    s.appendChild(el("h2", { tabindex: "-1", text: "Scoreboard" }));
    s.appendChild(el("p", { text: rankLine(list) }));
    var ol = el("ol", { class: "st-board" });
    var prevOrder = G.order || list.map(function (p) { return p.id; });
    var rows = {};
    list.forEach(function (p) {
      var bar = el("i", { style: "--w:0%" });
      var ptsEl = el("span", { class: "st-row-pts", text: fmt(p.pts) });
      rows[p.id] = el("li", { class: "st-row" + (p.you ? " is-you" : "") }, [
        el("span", { class: "st-row-rank", text: "" }), avatar(p),
        el("span", { class: "st-row-name" }, [el("b", { text: p.name + (p.you ? "" : " (computer)") }), el("span", { class: "st-row-bar" }, [bar])]),
        ptsEl]);
      rows[p.id]._bar = bar; rows[p.id]._pts = p.pts;
    });
    prevOrder.forEach(function (id) { if (rows[id]) ol.appendChild(rows[id]); });
    s.appendChild(ol);
    var go = el("button", { class: "st-go", type: "button", html: "Next question " + ico("i-arrow-right") });
    go.addEventListener("click", next);
    s.appendChild(go);
    sfx("board");
    // FLIP: rows start where they stood last time, then slide to their new places.
    var first = {};
    list.forEach(function (p) { first[p.id] = rows[p.id].getBoundingClientRect().top; });
    list.forEach(function (p, i) { ol.appendChild(rows[p.id]); rows[p.id].firstChild.textContent = String(i + 1); });
    if (!calm()) {
      list.forEach(function (p) {
        var dy = first[p.id] - rows[p.id].getBoundingClientRect().top;
        if (dy) {
          rows[p.id].style.transform = "translateY(" + dy + "px)";
          rows[p.id].style.transition = "none";
        }
      });
      requestAnimationFrame(function () {
        requestAnimationFrame(function () {
          list.forEach(function (p, i) {
            rows[p.id].style.transition = "transform .9s cubic-bezier(.2,.8,.3,1) " + (0.1 + i * 0.05) + "s";
            rows[p.id].style.transform = "";
          });
        });
      });
    }
    setTimeout(function () { list.forEach(function (p) { rows[p.id]._bar.style.setProperty("--w", Math.round(100 * p.pts / top) + "%"); }); }, 60);
    G.order = list.map(function (p) { return p.id; });
    say("Scoreboard. " + rankLine(list) + ".");
    focusFirst(go);
  }

  function podium() {
    label("Quiz Blitz", "Final standings");
    ui.dots.innerHTML = "";
    var list = standings(), r = rankOf(list);
    G.place = r;
    paintChips(false);
    var s = screen("st-board-wrap");
    s.appendChild(el("h2", { tabindex: "-1", text: r === 1 ? "You won the Quiz Blitz!" : r <= 3 ? "You made the podium!" : "Quiz Blitz finished" }));
    s.appendChild(el("p", { text: "You got " + G.right + " of " + D.blitz.length + " right" + (G.bestStreak >= 2 ? ", with a best streak of " + G.bestStreak : "") + "." }));
    var pod = el("div", { class: "st-podium" });
    [1, 0, 2].forEach(function (k) {
      var p = list[k];
      if (!p) return;
      pod.appendChild(el("div", { class: "st-pod st-pod-" + (k + 1) + (p.you ? " is-you" : "") }, [
        k === 0 ? el("span", { html: '<svg class="st-crown" viewBox="0 0 40 28" aria-hidden="true"><path d="M3 25 5 6l9 9 6-12 6 12 9-9 2 19Z" fill="#FDE047" stroke="#B45309" stroke-width="2" stroke-linejoin="round"/></svg>' }).firstChild : null,
        avatar(p), el("span", { class: "st-pod-name", text: p.name }), el("span", { class: "st-pod-pts", text: fmt(p.pts) + " points" }),
        el("div", { class: "st-pod-block", text: String(k + 1) })]));
    });
    s.appendChild(pod);
    if (r > 3) {
      var me = list[r - 1];
      var ol = el("ol", { class: "st-board", start: String(r) });
      ol.appendChild(el("li", { class: "st-row is-you" }, [el("span", { class: "st-row-rank", text: String(r) }), avatar(me),
        el("span", { class: "st-row-name" }, [el("b", { text: me.name })]), el("span", { class: "st-row-pts", text: fmt(me.pts) })]));
      s.appendChild(ol);
    }
    var go = el("button", { class: "st-go", type: "button", html: "On to Round 2 " + ico("i-arrow-right") });
    go.addEventListener("click", function () { splash("short"); });
    s.appendChild(go);
    if (r <= 3) { setTimeout(function () { confetti(ui.confetti, 3800); sfx("win"); }, calm() ? 0 : 1100); }
    else sfx("board");
    say("You finished " + ordinal(r) + ". " + G.right + " of " + D.blitz.length + " right.");
    focusFirst(s.querySelector("h2"));
  }

  /* ----------------------------------------------------- written rounds */
  function written(kind, i) {
    if (!G) return;
    var list = D[kind], w = list[i];
    G.round = kind;
    var R = ROUND[kind];
    label(R.name, "Question " + (i + 1) + " of " + list.length);
    paintDots(list.map(function (x, k) { var r = G.written[kind][k]; return r ? (r.got > 0 ? 1 : 0) : -1; }), i);
    paintChips(false);
    var s = screen("st-written");
    var card = el("div", { class: "st-wcard" });
    G.cat = pixel("wave");
    if (G.cat) card.appendChild(el("div", { class: "st-whost", "aria-hidden": "true" }, [G.cat]));
    var head = el("div", { class: "st-whead" });
    if (w.cmd) head.appendChild(el("span", { class: "st-pill is-cmd", text: w.cmd }));
    head.appendChild(el("span", { class: "st-pill is-marks", text: plural(w.m, "mark") }));
    card.appendChild(head);
    var h = el("h2", { class: "st-wq", tabindex: "-1", html: w.q });
    card.appendChild(h);
    if (w.c) card.appendChild(el("pre", { class: "st-code" }, [el("code", { html: w.c })]));

    var target = kind === "long" ? w.m * 15 : Math.max(8, w.m * 10);
    var area = el("textarea", { class: "st-answer" + (kind === "long" ? " is-long" : ""), rows: kind === "long" ? "8" : "3",
                                "aria-label": "Your answer", spellcheck: "true",
                                placeholder: kind === "long" ? "Write your answer in full sentences." : "Type your answer." });
    var count = el("span", { text: "0 words" });
    var meter = el("span", { class: "st-meter", "aria-hidden": "true" }, [el("i", {})]);
    var meta = el("div", { class: "st-wmeta" }, [count, meter, el("span", { text: "Aim for about " + target + " words" })]);
    area.addEventListener("focus", function () { setMood(G.cat, "think"); });
    area.addEventListener("input", function () {
      var n = words(area.value);
      count.textContent = plural(n, "word");
      meter.firstChild.style.setProperty("--w", Math.min(100, Math.round(100 * n / target)) + "%");
    });
    var frame = null;
    var help = null;
    if (w.f && w.f.length) {
      frame = el("div", { class: "st-frame", hidden: true });
      w.f.forEach(function (start) {
        frame.appendChild(el("button", { type: "button", text: start + "...", onclick: function () {
          var v = area.value.replace(/\s+$/, "");
          area.value = (v ? v + (/[.!?]$/.test(v) ? " " : ". ") : "") + start + " ";
          area.dispatchEvent(new Event("input"));
          area.focus();
          area.selectionStart = area.selectionEnd = area.value.length;
        } }));
      });
      help = el("button", { class: "st-help", type: "button", "aria-expanded": "false", text: "Need a start?" });
      help.addEventListener("click", function () {
        frame.hidden = !frame.hidden;
        help.setAttribute("aria-expanded", String(!frame.hidden));
      });
    }
    var nudge = el("p", { class: "st-nudge", hidden: true, text: "Write something first, even one sentence. Then mark it." });
    var mark = el("button", { class: "st-go", type: "button", html: ico("i-check") + " Mark my answer" });
    var skip = el("button", { class: "st-skip", type: "button", text: "Skip and see the answer" });
    var tools = el("div", { class: "st-wtools" }, [mark, help, skip]);
    card.appendChild(area);
    card.appendChild(meta);
    if (frame) card.appendChild(frame);
    card.appendChild(nudge);
    card.appendChild(tools);
    var result = el("div", { class: "st-wres", hidden: true });
    card.appendChild(result);
    s.appendChild(card);

    function doMark(skipped) {
      if (!skipped && !area.value.trim()) { nudge.hidden = false; area.focus(); return; }
      nudge.hidden = true;
      area.readOnly = true;
      tools.remove();
      if (frame) frame.hidden = true;
      var hits = window.MskMarker ? window.MskMarker.hits(skipped ? "" : area.value, w.p.map(function (p) { return p.a; })) :
        w.p.map(function () { return false; });
      var got = Math.min(w.m, hits.filter(Boolean).length);
      var rec = G.written[kind][i] = { got: got, max: w.m, auto: got };
      showResult(result, kind, w, hits, rec, skipped, i, list.length);
    }
    mark.addEventListener("click", function () { doMark(false); });
    skip.addEventListener("click", function () { doMark(true); });
    area.addEventListener("keydown", function (e) { if (e.key === "Enter" && (e.ctrlKey || e.metaKey)) { e.preventDefault(); doMark(false); } });
    say(R.name + ", question " + (i + 1) + " of " + list.length + ". " + w.m + " marks.");
    focusFirst(h);
  }

  function showResult(box, kind, w, hits, rec, skipped, i, n) {
    box.hidden = false;
    box.innerHTML = "";
    var per = PER_MARK[kind];
    var gainEl = el("span", { class: "st-gain" + (rec.got ? "" : " is-zero"), text: "+" + fmt(rec.got * per) });
    var scoreN = el("span", { class: "st-score-n", html: rec.got + " <small>/ " + w.m + "</small>" });
    var msg = skipped ? "Skipped. Read the answer, then try writing it from memory." :
      rec.got >= w.m ? pick(["Full marks!", "Every point covered!", "Top answer!"]) :
      rec.got ? "Part marks. The unticked points show what to add." : "No mark points found yet. Read the model answer.";
    var msgEl = el("span", { class: "st-score-msg", text: msg });
    box.appendChild(el("div", { class: "st-score" }, [scoreN, gainEl, msgEl]));
    box.appendChild(el("p", { class: "st-ms-head", text: "Mark scheme: one mark per point" + (w.p.length > w.m ? ", up to " + w.m : "") }));
    var ul = el("ul", { class: "st-ms" });
    w.p.forEach(function (p, k) {
      ul.appendChild(el("li", { class: hits[k] ? "is-hit" : "", style: "animation-delay:" + (k * 0.12) + "s" }, [
        el("span", { class: "st-tick", "aria-hidden": "true", html: ico(hits[k] ? "i-check" : "i-cross") }),
        el("span", { html: p.t + (hits[k] ? '<span class="sr-only"> (found in your answer)</span>' : '<span class="sr-only"> (not found)</span>') })]));
    });
    box.appendChild(ul);
    box.appendChild(el("div", { class: "st-model", html: "<b>Model answer</b>" + w.model }));
    var sel = el("select", { "aria-label": "Your mark" });
    for (var m = 0; m <= w.m; m++) sel.appendChild(el("option", { value: String(m), text: m + " / " + w.m, selected: m === rec.got }));
    sel.addEventListener("change", function () {
      rec.got = parseInt(sel.value, 10);
      scoreN.innerHTML = rec.got + " <small>/ " + w.m + "</small>";
      gainEl.textContent = "+" + fmt(rec.got * per);
      gainEl.classList.toggle("is-zero", !rec.got);
      recount();
    });
    box.appendChild(el("label", { class: "st-self" }, [el("span", { text: "Said it another way? Change your mark:" }), sel]));
    var last = i === n - 1;
    var go = el("button", { class: "st-go", type: "button", html: (last ? (kind === "short" ? "On to Round 3" : "See my results") : "Next question") + " " + ico("i-arrow-right") });
    go.addEventListener("click", function () {
      if (!last) written(kind, i + 1);
      else if (kind === "short") splash("long");
      else results();
    });
    box.appendChild(go);
    recount();
    paintChips(rec.got > 0);
    sfx(rec.got ? "good" : "pop");
    if (G.cat) setMood(G.cat, rec.got >= w.m ? "cheer" : "happy");
    say(skipped ? "Skipped. The model answer is shown." : "You scored " + rec.got + " of " + w.m + ". " + msg);
    setTimeout(function () {
      try { box.scrollIntoView({ behavior: calm() ? "auto" : "smooth", block: "start" }); } catch (e) { box.scrollIntoView(); }
      go.focus({ preventScroll: true });
    }, 120);
  }
  function recount() {
    var t = 0;
    ["short", "long"].forEach(function (k) { G.written[k].forEach(function (r) { if (r) t += r.got * PER_MARK[k]; }); });
    G.writtenPts = t;
    paintChips(false);
  }
  function sumRound(kind) {
    var got = 0, max = 0;
    D[kind].forEach(function (w, i) { var r = G.written[kind][i]; max += w.m; if (r) got += r.got; });
    return { got: got, max: max };
  }

  /* ------------------------------------------------------------ results */
  function results() {
    G.done = true;
    G.round = "done";
    stage.setAttribute("data-round", "done");
    label("Results", D.lesson);
    ui.dots.innerHTML = "";
    paintChips(false);
    var sh = sumRound("short"), lg = sumRound("long");
    var pct = 0.4 * (G.right / D.blitz.length) + 0.25 * (sh.max ? sh.got / sh.max : 0) + 0.35 * (lg.max ? lg.got / lg.max : 0);
    var stars = pct >= 0.8 ? 3 : pct >= 0.55 ? 2 : 1;
    var total = G.blitzPts + G.writtenPts;
    var all = store.get(RECORDS, {}) || {};
    var old = all[D.key];
    var newBest = !!old && total > old.b;
    all[D.key] = { b: Math.max(total, old ? old.b : 0), s: Math.max(stars, old ? old.s : 0),
                   p: Math.max(Math.round(pct * 100), old ? old.p || 0 : 0), d: Date.now(), n: (old ? old.n || 0 : 0) + 1 };
    store.set(RECORDS, all);

    var medals = [];
    if (G.place === 1) medals.push(["crown", "#D97706", "Champion", "1st in the Quiz Blitz"]);
    else if (G.place <= 3) medals.push(["podium", "#64748B", "Podium", ordinal(G.place) + " in the Quiz Blitz"]);
    if (G.right === D.blitz.length) medals.push(["sweep", "#16A34A", "Clean sweep", "Every question right"]);
    if (G.bestStreak >= 5) medals.push(["fire", "#EA580C", "On fire", "A streak of " + G.bestStreak]);
    var quick = G.times.filter(function (t) { return t.ok && t.ms <= t.limit * 0.4; }).length;
    if (opts.timer && quick >= 8) medals.push(["bolt", "#7C3AED", "Quick thinker", plural(quick, "fast answer")]);
    if (sh.max && sh.got === sh.max) medals.push(["pen", "#0F766E", "Sharp writer", "Full marks in Quick Fire"]);
    if (D.long.some(function (w, i) { var r = G.written.long[i]; return r && r.got === w.m; })) medals.push(["bulb", "#4F46E5", "Deep thinker", "Full marks on a long answer"]);

    var s = screen("st-results");
    var cat = pixel(stars === 3 ? "proud" : stars === 2 ? "cheer" : "happy");
    var title = stars === 3 ? "Stretch champion" : stars === 2 ? "Strong stretch" : "Stretch started: play again to go further";
    s.appendChild(el("div", { class: "st-res-top" }, [cat, el("p", { class: "st-res-title", text: title })]));
    s.appendChild(el("h2", { tabindex: "-1", text: D.lesson }));
    s.appendChild(el("div", { class: "st-res-stars", role: "img", "aria-label": stars + " of 3 stars", html: bigStar(stars >= 1) + bigStar(stars >= 2) + bigStar(stars >= 3) }));
    var totalN = el("span", { text: "0" });
    s.appendChild(el("div", { class: "st-res-total" }, [totalN, el("small", { text: "points" })]));
    if (newBest) s.appendChild(el("span", { class: "st-res-best", text: "New personal best!" }));

    var card = el("div", { class: "st-res-card" });
    var who = (opts.name || "").trim();
    card.appendChild(el("p", { class: "st-res-name", text: (who ? who + " \u00b7 " : "") + D.spec + " " + D.unit + ", lesson " + D.n + " \u00b7 " +
      new Date().toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" }) }));
    var icons = lobby.querySelectorAll(".st-round-ico");
    [[0, "Quiz Blitz", G.right + " of " + D.blitz.length + " right, " + ordinal(G.place || 5) + " place", fmt(G.blitzPts)],
     [1, "Quick Fire", sh.got + " of " + sh.max + " marks", fmt(sh.got * PER_MARK.short)],
     [2, "Big Think", lg.got + " of " + lg.max + " marks", fmt(lg.got * PER_MARK.long)]].forEach(function (r) {
      card.appendChild(el("div", { class: "st-res-row" }, [
        el("span", { class: "st-round-ico", "aria-hidden": "true", html: icons[r[0]] ? icons[r[0]].innerHTML : "" }),
        el("span", {}, [el("b", { text: r[1] }), el("span", { text: r[2] })]),
        el("strong", { text: r[3] })]));
    });
    s.appendChild(card);
    if (medals.length) {
      var row = el("div", { class: "st-medals" });
      medals.forEach(function (m, k) {
        row.appendChild(el("div", { class: "st-medal", style: "animation-delay:" + (1.2 + k * 0.18) + "s" },
          [el("span", { html: medalSvg(m[0], m[1]) }).firstChild, el("b", { text: m[2] }), el("span", { text: m[3] })]));
      });
      s.appendChild(row);
    }
    s.appendChild(resultButtons("quiz"));

    countUp(totalN, 0, total, 1600);
    if (stars >= 2) setTimeout(function () { confetti(ui.confetti, 4200); }, calm() ? 0 : 900);
    sfx("win");
    say("Finished. " + stars + " of 3 stars and " + fmt(total) + " points." + (newBest ? " New personal best." : ""));
    focusFirst(s.querySelector("h2"));
  }

  /* ------------------------------------------------- shared result screen */
  var NEXT_TASK = { quiz: "cat", cat: "match", match: null };
  function resultButtons(task) {
    var go = el("div", { class: "st-res-go" });
    go.appendChild(el("button", { class: "st-go", type: "button", html: ico("i-repeat") + " Play again", onclick: function () { leave(false); begin(task); } }));
    var nt = NEXT_TASK[task];
    if (nt) go.appendChild(el("button", { class: "st-ghost", type: "button", html: "Next task: " + TASK_NAMES[nt] + " " + ico("i-arrow-right"), onclick: function () { leave(false); begin(nt); } }));
    else if (D.next) go.appendChild(el("a", { class: "st-ghost", href: D.next.u, html: "Next lesson: " + escHtml(D.next.t) + " " + ico("i-arrow-right") }));
    go.appendChild(el("a", { class: "st-ghost", href: D.back, html: ico("i-book") + " Back to the lesson" }));
    go.appendChild(el("button", { class: "st-ghost", type: "button", html: ico("i-paper") + " Print my result", onclick: function () { printAs("result"); } }));
    go.appendChild(el("button", { class: "st-ghost", type: "button", html: ico("i-cross") + " Close", onclick: function () { leave(false); } }));
    return go;
  }
  /* A copy of a drawing whose ids, and the fills that point at them, are its
     own, so two copies on one page never share a gradient. */
  function freshIds(html) {
    var box = el("div", { html: html });
    pxSeq += 1;
    var map = {};
    Array.prototype.forEach.call(box.querySelectorAll("[id]"), function (n) { map[n.id] = n.id + "-r" + pxSeq; n.id = map[n.id]; });
    Array.prototype.forEach.call(box.querySelectorAll("[fill^='url(#']"), function (n) {
      var m = /^url\(#([^)]+)\)$/.exec(n.getAttribute("fill"));
      if (m && map[m[1]]) n.setAttribute("fill", "url(#" + map[m[1]] + ")");
    });
    return box.innerHTML;
  }

  function taskResults(o) {
    G.done = true;
    G.round = "done";
    stage.setAttribute("data-round", "done");
    label("Results", TASK_NAMES[G.task]);
    ui.dots.innerHTML = "";
    var key = recKey(D.key, G.task);
    var all = store.get(RECORDS, {}) || {};
    var old = all[key];
    var newBest = !!old && o.pts > old.b;
    all[key] = { b: Math.max(o.pts, old ? old.b : 0), s: Math.max(o.stars, old ? old.s : 0),
                 p: Math.max(Math.round(o.pct * 100), old ? old.p || 0 : 0), d: Date.now(), n: (old ? old.n || 0 : 0) + 1 };
    store.set(RECORDS, all);

    var s = screen("st-results");
    var cat = pixel(o.mood);
    if (o.wear) wear(cat, o.wear);
    s.appendChild(el("div", { class: "st-res-top" }, [cat, el("p", { class: "st-res-title", text: o.title })]));
    s.appendChild(el("h2", { tabindex: "-1", text: D.lesson }));
    s.appendChild(el("div", { class: "st-res-stars", role: "img", "aria-label": o.stars + " of 3 stars", html: bigStar(o.stars >= 1) + bigStar(o.stars >= 2) + bigStar(o.stars >= 3) }));
    var totalN = el("span", { text: "0" });
    s.appendChild(el("div", { class: "st-res-total" }, [totalN, el("small", { text: "points" })]));
    if (newBest) s.appendChild(el("span", { class: "st-res-best", text: "New personal best!" }));

    var card = el("div", { class: "st-res-card" });
    var who = (opts.name || "").trim();
    card.appendChild(el("p", { class: "st-res-name", text: (who ? who + " · " : "") + TASK_NAMES[G.task] + " · " + D.spec + " " + D.unit +
      ", lesson " + D.n + " · " + new Date().toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" }) }));
    o.rows.forEach(function (r) {
      card.appendChild(el("div", { class: "st-res-row" }, [
        el("span", { class: "st-round-ico", "aria-hidden": "true", html: r[0] }),
        el("span", {}, [el("b", { text: r[1] }), el("span", { text: r[2] })]),
        el("strong", { text: r[3] })]));
    });
    if (o.extra) card.appendChild(o.extra);
    s.appendChild(card);
    if (o.medals.length) {
      var row = el("div", { class: "st-medals" });
      o.medals.forEach(function (m, k) {
        row.appendChild(el("div", { class: "st-medal", style: "animation-delay:" + (1.2 + k * 0.18) + "s" },
          [el("span", { html: medalSvg(m[0], m[1]) }).firstChild, el("b", { text: m[2] }), el("span", { text: m[3] })]));
      });
      s.appendChild(row);
    }
    s.appendChild(resultButtons(G.task));
    countUp(totalN, 0, o.pts, 1400);
    if (o.stars >= 2) setTimeout(function () { confetti(ui.confetti, 4200); }, calm() ? 0 : 900);
    sfx("win");
    say("Finished. " + o.summary + " " + o.stars + " of 3 stars and " + fmt(o.pts) + " points." + (newBest ? " New personal best." : ""));
    focusFirst(s.querySelector("h2"));
  }
  function reviewList(head, items) {
    var box = el("div", { class: "st-res-review" }, [el("b", { text: head })]);
    var ul = el("ul", {});
    items.forEach(function (h) { ul.appendChild(el("li", { html: h })); });
    box.appendChild(ul);
    return box;
  }

  /* ======================================================= THIS OR THAT */
  var FISH = '<svg viewBox="0 0 30 18" aria-hidden="true" focusable="false"><path d="M2.5 9C7 2.6 15.5 2.4 21 7.2L27.5 2.5v13L21 10.8C15.5 15.6 7 15.4 2.5 9Z" fill="#FDBA74" stroke="#9A3412" stroke-width="1.6" stroke-linejoin="round"/>' +
    '<path d="M15 5.8c1.3 1.1 1.3 5.3 0 6.4" fill="none" stroke="#9A3412" stroke-width="1.3" stroke-linecap="round"/><circle cx="8" cy="8" r="1.5" fill="#1E293B"/></svg>';
  var HEART = '<svg viewBox="0 0 24 22" aria-hidden="true" focusable="false"><path d="M12 20.5S2 14.4 2 7.7A5.2 5.2 0 0 1 12 5.4a5.2 5.2 0 0 1 10 2.3c0 6.7-10 12.8-10 12.8Z" fill="#F472B6" stroke="#fff" stroke-width="1.6"/></svg>';
  var DROP = '<svg viewBox="0 0 16 22" aria-hidden="true" focusable="false"><path d="M8 1.5C10.5 7 14 10 14 14a6 6 0 0 1-12 0c0-4 3.5-7 6-12.5Z" fill="#7DD3FC" stroke="#fff" stroke-width="1.5"/></svg>';
  var CAT_INTROS = ["Here's one for you.", "Paws for thought...", "Ooh, I like this one.", "Whisker-twister time!",
                    "Think carefully.", "Which one is it?", "Try this one.", "Ready? Here it comes."];
  var CAT_RIGHT = ["Purr-fect!", "Paw-some!", "Meow-velous!", "Clawsome!", "Fur-tastic!", "You're the cat's whiskers!"];
  var CAT_WRONG = ["Oh, whiskers!", "Not that one.", "Hiss... so close.", "Not quite!"];
  var lastIntro = -1;
  function catIntro(i) {
    if (i === 0) return "First question!";
    if (i === D.picks.length - 1) return "Last one!";
    var k;
    do { k = Math.floor(Math.random() * CAT_INTROS.length); } while (k === lastIntro);
    lastIntro = k;
    return CAT_INTROS[k];
  }
  function catDots() { return D.picks.map(function (q, i) { return i < G.answers.length ? (G.answers[i] ? 1 : 0) : -1; }); }
  function catChips(bump) {
    ui.fishN.textContent = String(G.right);
    ui.fishChip.setAttribute("aria-label", plural(G.right, "fish treat"));
    if (bump) { ui.fishChip.classList.remove("is-bump"); void ui.fishChip.offsetWidth; ui.fishChip.classList.add("is-bump"); }
    ui.streak.hidden = G.streak < 2;
    ui.streakN.textContent = String(G.streak);
    ui.streak.classList.toggle("is-hot", G.streak >= 3);
    ui.streak.setAttribute("aria-label", "Answer streak " + G.streak);
  }
  /* What Pixel wears depends on the answer streak. */
  function catWear() { return G.streak >= 5 ? ["shades", "party"] : G.streak >= 3 ? ["shades"] : []; }

  function catSplash() {
    label("This or That", plural(D.picks.length, "question"));
    ui.dots.innerHTML = "";
    var s = screen("st-splash st-cat-splash");
    var px = pixel("wave");
    if (px) s.appendChild(el("div", { class: "st-cat-hero", "aria-hidden": "true" }, [px]));
    s.appendChild(el("span", { class: "st-splash-tag", text: "This or That" }));
    s.appendChild(el("h2", { tabindex: "-1", text: "Hello! I'm Pixel." }));
    var sub = "I have " + plural(D.picks.length, "question") + " about " + D.lesson + ". Each one has two answers. Pick the right one and I get a fish treat!";
    s.appendChild(el("p", { text: sub }));
    var go = el("button", { class: "st-go", type: "button", html: ico("i-play") + " Let's go" });
    go.addEventListener("click", function () { catQ(0); });
    s.appendChild(go);
    sfx("board");
    say("This or That with Pixel the cat. " + sub);
    focusFirst(go);
  }

  /* The question arrives a word at a time while Pixel talks, and the answers
     appear once it has been asked. Returns how long that takes. */
  function sayWords(node) {
    if (calm()) return 0;
    var texts = [], walker = document.createTreeWalker(node, 4, null), count = 0, n = 0;
    while (walker.nextNode()) texts.push(walker.currentNode);
    texts.forEach(function (t) { count += (t.nodeValue.match(/\S+/g) || []).length; });
    var step = Math.min(70, 1100 / Math.max(1, count));
    texts.forEach(function (t) {
      var frag = document.createDocumentFragment();
      t.nodeValue.split(/(\s+)/).forEach(function (part) {
        if (!part) return;
        if (/^\s+$/.test(part)) { frag.appendChild(document.createTextNode(part)); return; }
        var w = document.createElement("span");
        w.className = "st-w";
        w.textContent = part;
        w.style.animationDelay = Math.round(n * step) + "ms";
        n += 1;
        frag.appendChild(w);
      });
      t.parentNode.replaceChild(frag, t);
    });
    return Math.round(n * step) + 250;
  }

  function catQ(i) {
    if (!G) return;
    G.qi = i;
    G.locked = true;
    var q = D.picks[i];
    label("This or That", "Question " + (i + 1) + " of " + D.picks.length);
    paintDots(catDots(), i);
    catChips(false);
    var s = screen("st-cat");
    var px = G.cat = pixel("talk");
    wear(px, catWear());
    var fx = el("span", { class: "st-cat-fx", "aria-hidden": "true",
                          html: '<i class="st-heart">' + HEART + '</i><i class="st-heart">' + HEART + '</i><i class="st-heart">' + HEART + '</i><i class="st-drop">' + DROP + "</i>" });
    ui.catBox = el("div", { class: "st-cat-pixel" }, [px, fx]);
    var bubble = el("div", { class: "st-bubble" });
    bubble.appendChild(el("p", { class: "st-bubble-intro", text: catIntro(i) }));
    var h = el("h2", { class: "st-bubble-q", tabindex: "-1", html: q.q });
    bubble.appendChild(h);
    if (q.c) bubble.appendChild(el("pre", { class: "st-code" }, [el("code", { html: q.c })]));
    s.appendChild(el("div", { class: "st-cat-scene" }, [ui.catBox, bubble]));

    var duo = el("div", { class: "st-duo" });
    ui.tiles = [];
    (Math.random() < 0.5 ? [true, false] : [false, true]).forEach(function (right, k) {
      var html = right ? q.r : q.w;
      var b = el("button", { class: "st-duo-btn st-duo-" + (k ? "b" : "a"), type: "button", "aria-label": "Answer " + (k + 1) + ": " + stripTags(html) },
        [el("span", { class: "st-duo-k", "aria-hidden": "true", text: String(k + 1) }),
         el("span", { class: "st-duo-t", html: html }),
         el("span", { class: "st-mark", "aria-hidden": "true" })]);
      b._right = right;
      b.addEventListener("click", function () { catAnswer(b); });
      ui.tiles.push(b);
      duo.appendChild(b);
      if (!k) duo.appendChild(el("span", { class: "st-duo-or", "aria-hidden": "true", text: "or" }));
    });
    s.appendChild(duo);
    ui.fb = el("div", { class: "st-fbslot" });
    s.appendChild(ui.fb);

    var wait = sayWords(h), game = G;
    setTimeout(function () {
      if (G !== game || G.qi !== i) return;
      setMood(px, "think");
      duo.classList.add("is-ready");
      G.locked = false;
    }, wait);
    say("Question " + (i + 1) + " of " + D.picks.length + ".");
    focusFirst(h);
  }

  function flyFish(from) {
    var land = function () { if (G && G.task === "cat") catChips(true); };
    if (calm() || !ui.fishChip) { land(); return; }
    var a = from.getBoundingClientRect(), b = ui.fishChip.getBoundingClientRect();
    var x0 = a.left + a.width / 2 - 18, y0 = a.top + a.height / 2 - 11;
    var f = el("span", { class: "st-flyfish", "aria-hidden": "true", html: FISH, style: "left:" + Math.round(x0) + "px;top:" + Math.round(y0) + "px" });
    stage.appendChild(f);
    void f.offsetWidth;
    f.style.transform = "translate(" + Math.round(b.left + 6 - x0) + "px," + Math.round(b.top + 4 - y0) + "px) scale(.55) rotate(-25deg)";
    setTimeout(function () { if (f.parentNode) f.parentNode.removeChild(f); land(); }, 720);
  }

  function catAnswer(btn) {
    if (!G || G.locked) return;
    G.locked = true;
    var q = D.picks[G.qi], ok = btn._right, hadWear = catWear().length > 0;
    ui.tiles.forEach(function (t) {
      t.disabled = true;
      if (t._right) markTile(t, true);
      else if (t === btn) markTile(t, false);
      else t.classList.add("is-dim");
    });
    G.answers.push(ok);
    var gain = 0;
    if (ok) {
      G.right += 1; G.streak += 1;
      G.bestStreak = Math.max(G.bestStreak, G.streak);
      gain = 100 + 25 * Math.min(G.streak - 1, 5);
      G.pts += gain;
    } else G.streak = 0;
    wear(G.cat, catWear());
    setMood(G.cat, ok ? (G.streak >= 3 ? "cheer" : "happy") : "oops");
    ui.catBox.classList.remove("is-love", "is-oops");
    void ui.catBox.offsetWidth;
    ui.catBox.classList.add(ok ? "is-love" : "is-oops");
    paintDots(catDots(), -1);
    if (ok) flyFish(btn); else catChips(false);
    sfx(ok ? "good" : "bad");

    var last = G.qi === D.picks.length - 1;
    var extra = ok && G.streak === 3 ? "Three in a row: shades on!" : ok && G.streak === 5 ? "Five in a row: party hat time!" :
      !ok && hadWear ? "The streak is over, so the shades come off." : "";
    var next = el("button", { class: "st-go", type: "button", html: (last ? "See my result" : "Next question") + " " + ico("i-arrow-right") });
    next.addEventListener("click", function () { if (last) catResults(); else catQ(G.qi + 1); });
    var fb = el("div", { class: "st-catfb " + (ok ? "is-ok" : "is-bad"), role: "status" }, [
      el("div", { class: "st-catfb-head" }, [
        el("span", { class: "st-catfb-badge", "aria-hidden": "true", html: ico(ok ? "i-check" : "i-cross") }),
        el("b", { text: ok ? pick(CAT_RIGHT) : pick(CAT_WRONG) }),
        ok ? el("span", { class: "st-catfb-pts", text: "+" + gain }) : null]),
      extra ? el("p", { class: "st-catfb-streak", html: FLAME + "<span>" + extra + "</span>" }) : null,
      el("p", { class: "st-catfb-x", html: (ok ? "" : '<span class="st-fb-ans"><b>Answer:</b> ' + q.r + "</span>") + q.x }),
      el("div", { class: "st-fb-go" }, [next])
    ]);
    ui.fb.appendChild(fb);
    setTimeout(function () {
      try { fb.scrollIntoView({ behavior: calm() ? "auto" : "smooth", block: "nearest" }); } catch (e) { fb.scrollIntoView(false); }
      next.focus({ preventScroll: true });
    }, calm() ? 0 : 350);
  }

  function catResults() {
    var n = D.picks.length, pct = G.right / n;
    var stars = G.right === n ? 3 : pct >= 0.75 ? 2 : 1;
    var medals = [];
    if (G.right === n) medals.push(["crown", "#D97706", "Cat's whiskers", "Every answer right"]);
    if (G.bestStreak >= 5) medals.push(["fish", "#EA580C", "Cool cat", "A streak of " + G.bestStreak]);
    var missed = [];
    D.picks.forEach(function (q, i) { if (!G.answers[i]) missed.push(q.q + ' <span class="st-res-ans">' + q.r + "</span>"); });
    taskResults({
      stars: stars, pts: G.pts, pct: pct,
      title: stars === 3 ? "Top cat! Every answer right" : stars === 2 ? "Purr-fectly good" : "A good start: play again to beat it",
      mood: stars === 3 ? "proud" : stars === 2 ? "cheer" : "happy", wear: stars === 3 ? ["crown"] : null,
      rows: [[freshIds(art("cat")), "Pixel's questions", G.right + " of " + n + " right", fmt(G.pts)],
             [FLAME, "Best streak", plural(G.bestStreak, "answer") + " in a row", ""]],
      medals: medals,
      extra: missed.length ? reviewList("Worth another look", missed) : null,
      summary: G.right + " of " + n + " right."
    });
  }

  /* ======================================================= MEMORY MATCH */
  var CARD_BACK = '<svg viewBox="0 0 80 56" aria-hidden="true" focusable="false"><rect x="5" y="5" width="70" height="46" rx="8" fill="none" stroke="#fff" stroke-opacity=".45" stroke-width="2" stroke-dasharray="4 3"/>' +
    '<circle cx="40" cy="28" r="13" fill="#fff"/><path d="M35.6 24.6a4.6 4.6 0 1 1 6.3 4.2c-1.4.6-1.9 1.4-1.9 2.9" fill="none" stroke="#1F5FD1" stroke-width="3" stroke-linecap="round"/><circle cx="40" cy="35.6" r="1.9" fill="#1F5FD1"/>' +
    '<path d="M13 18l4-7 4 7Z" fill="#FCA5A5"/><path d="M63 10.5l4 4-4 4-4-4Z" fill="#FDE68A"/><circle cx="17" cy="41" r="3.5" fill="#86EFAC"/><rect x="59.5" y="37.5" width="7" height="7" rx="1.5" fill="#C4B5FD"/></svg>';
  function mmss(ms) { var t = Math.floor(ms / 1000); return Math.floor(t / 60) + ":" + ("0" + (t % 60)).slice(-2); }
  function watch() { return G.t0 ? (G.tEnd || performance.now()) - G.t0 : 0; }
  function startWatch() {
    if (G.t0) return;
    G.t0 = performance.now();
    if (opts.timer) G.tick = setInterval(function () { if (G && ui.timeN) ui.timeN.textContent = mmss(watch()); }, 250);
  }
  function misses(n) { return n === 1 ? "1 miss" : n + " misses"; }
  function matchChips(bump) {
    ui.pairsN.textContent = G.found + " / " + D.pairs.length;
    ui.missN.textContent = String(G.misses);
    if (bump) { ui.pairsChip.classList.remove("is-bump"); void ui.pairsChip.offsetWidth; ui.pairsChip.classList.add("is-bump"); }
  }

  function matchSplash() {
    label("Memory Match", plural(D.pairs.length, "pair"));
    ui.dots.innerHTML = "";
    var s = screen("st-splash");
    s.appendChild(el("span", { class: "st-splash-tag", text: "Memory Match" }));
    s.appendChild(el("div", { class: "st-splash-ico", "aria-hidden": "true", html: art("match") }));
    s.appendChild(el("h2", { tabindex: "-1", text: "Memory Match" }));
    var sub = D.pairs.length * 2 + " cards lie face down. Flip two at a time to match each " + D.pn[0].toLowerCase() + " card to its " +
      D.pn[1].toLowerCase() + " card. You can peek once.";
    s.appendChild(el("p", { text: sub }));
    var go = el("button", { class: "st-go", type: "button", html: ico("i-play") + " Deal the cards" });
    go.addEventListener("click", matchDeal);
    s.appendChild(go);
    sfx("board");
    say("Memory Match. " + sub);
    focusFirst(go);
  }

  function cardLabel(c) {
    var n = "Card " + (c.i + 1);
    if (c.done) return n + ": " + c.text + ", matched";
    return c.up ? n + ": " + c.text + ", " + D.pn[c.side].toLowerCase() : n + ", face down";
  }
  function setUp(c, up) {
    c.up = up;
    c.el.classList.toggle("is-up", up);
    c.el.setAttribute("aria-label", cardLabel(c));
  }

  function matchDeal() {
    if (!G) return;
    G.found = 0; G.misses = 0; G.combo = 0; G.bestCombo = 0; G.pts = 0; G.open = []; G.peeks = 1; G.t0 = 0; G.tEnd = 0;
    label("Memory Match", "Find the " + D.pairs.length + " pairs");
    matchChips(false);
    var s = screen("st-match");
    var deck = [];
    D.pairs.forEach(function (p, k) { deck.push({ k: k, side: 0, html: p.a }); deck.push({ k: k, side: 1, html: p.b }); });
    deck = shuffle(deck);
    var grid = el("div", { class: "st-cards", role: "group", "aria-label": "Cards" });
    deck.forEach(function (c, i) {
      c.i = i; c.up = false; c.done = false; c.text = stripTags(c.html);
      c.el = el("button", { class: "st-card st-card-" + (c.side ? "b" : "a"), type: "button", style: "--i:" + i, "aria-label": cardLabel(c) }, [
        el("span", { class: "st-card-in" }, [
          el("span", { class: "st-card-back", "aria-hidden": "true", html: CARD_BACK }),
          el("span", { class: "st-card-front", "aria-hidden": "true" }, [
            el("small", { class: "st-card-tag", text: D.pn[c.side] }), el("span", { class: "st-card-t", html: c.html })])]),
        el("span", { class: "st-card-badge", "aria-hidden": "true" })]);
      c.el.addEventListener("click", function () { flipCard(c); });
      grid.appendChild(c.el);
    });
    G.cards = deck;
    grid.addEventListener("keydown", function (e) { cardKeys(e, grid); });
    ui.peek = el("button", { class: "st-ghost st-peek", type: "button", html: ico("i-eye") + ' Peek <span class="st-peek-n">1 left</span>' });
    ui.peek.addEventListener("click", function () { peek(grid); });
    s.appendChild(el("div", { class: "st-match-bar" }, [
      el("p", { class: "st-match-hint", text: "Match each " + D.pn[0].toLowerCase() + " card to its " + D.pn[1].toLowerCase() + " card." }), ui.peek]));
    s.appendChild(grid);
    sfx("board");
    say("The cards are dealt: " + deck.length + " cards, face down. Move with Tab or the arrow keys and press Enter to flip a card.");
    focusFirst(deck[0].el);
  }

  function cardKeys(e, grid) {
    if (["ArrowLeft", "ArrowRight", "ArrowUp", "ArrowDown", "Home", "End"].indexOf(e.key) < 0 || !G || !G.cards) return;
    var cards = G.cards.map(function (c) { return c.el; });
    var i = cards.indexOf(document.activeElement);
    if (i < 0) return;
    var cols = getComputedStyle(grid).gridTemplateColumns.split(" ").length || 4;
    var j = e.key === "ArrowLeft" ? i - 1 : e.key === "ArrowRight" ? i + 1 : e.key === "ArrowUp" ? i - cols :
      e.key === "ArrowDown" ? i + cols : e.key === "Home" ? 0 : cards.length - 1;
    if (j < 0 || j >= cards.length) return;
    e.preventDefault();
    cards[j].focus();
  }

  function turnBack() {
    G.open.forEach(function (c) { c.el.classList.remove("is-miss"); setUp(c, false); });
    G.open = [];
  }
  function popText(c, text, cls) {
    var p = el("span", { class: "st-pop" + (cls ? " " + cls : ""), "aria-hidden": "true", text: text });
    c.el.appendChild(p);
    setTimeout(function () { if (p.parentNode) p.parentNode.removeChild(p); }, 1300);
  }

  function flipCard(c) {
    if (!G || G.done || c.done || c.up || G.peeking) return;
    if (G.busy) { clearTimeout(G.busy); G.busy = 0; turnBack(); }
    startWatch();
    setUp(c, true);
    sfx("pop");
    G.open.push(c);
    if (G.open.length < 2) { say(c.text + ", " + D.pn[c.side].toLowerCase() + ". Now find its partner."); return; }
    var a = G.open[0];
    if (a.k === c.k) cardsMatch(a, c); else cardsMiss(a, c);
  }
  function cardsMatch(a, b) {
    G.open = [];
    G.found += 1; G.combo += 1;
    G.bestCombo = Math.max(G.bestCombo, G.combo);
    var gain = 100 + 50 * Math.min(G.combo - 1, 4);
    G.pts += gain;
    var colour = (G.found - 1) % 6;
    [a, b].forEach(function (c) {
      c.done = true;
      c.el.classList.add("is-matched", "st-pair-" + colour);
      c.el.setAttribute("aria-disabled", "true");
      c.el.querySelector(".st-card-badge").innerHTML = '<svg viewBox="0 0 24 24">' + SHAPES[colour] + "</svg>";
      c.el.setAttribute("aria-label", cardLabel(c));
    });
    popText(b, "+" + gain);
    if (G.combo >= 2) popText(a, "Combo x" + G.combo + "!", "is-combo");
    matchChips(true);
    sfx("good");
    var w = a.side === 0 ? a : b, m = a.side === 0 ? b : a;
    say("Match! " + w.text + ": " + m.text + "." + (G.combo >= 2 ? " A combo of " + G.combo + "." : "") + " " +
        G.found + " of " + D.pairs.length + " pairs found.");
    if (G.found === D.pairs.length) {
      G.tEnd = performance.now();
      clearInterval(G.tick); G.tick = 0;
      if (ui.timeN) ui.timeN.textContent = mmss(watch());
      setTimeout(matchResults, calm() ? 400 : 1200);
    }
  }
  function cardsMiss(a, b) {
    G.misses += 1; G.combo = 0;
    a.el.classList.add("is-miss");
    b.el.classList.add("is-miss");
    matchChips(false);
    sfx("bad");
    say("Not a pair: " + a.text + " and " + b.text + ". They turn back over.");
    var game = G;
    G.busy = setTimeout(function () { if (G === game && !G.done) { G.busy = 0; turnBack(); } }, 1400);
  }
  function peek(grid) {
    if (!G || G.done || G.peeks < 1 || G.peeking) return;
    if (G.busy) { clearTimeout(G.busy); G.busy = 0; turnBack(); }
    startWatch();
    G.peeks -= 1;
    G.peeking = true;
    ui.peek.setAttribute("aria-disabled", "true");
    ui.peek.querySelector(".st-peek-n").textContent = "used";
    grid.classList.add("is-peek");
    sfx("pop");
    say("Peek! Every card is face up for two seconds.");
    var game = G;
    setTimeout(function () { grid.classList.remove("is-peek"); if (G === game) G.peeking = false; }, 2000);
  }

  function matchResults() {
    if (!G || G.done) return;
    var secs = Math.floor(watch() / 1000);
    var bonus = opts.timer ? Math.max(0, 600 - 5 * secs) : 0;
    var matchPts = G.pts;
    G.pts += bonus;
    var stars = G.misses <= 4 ? 3 : G.misses <= 8 ? 2 : 1;
    var medals = [];
    if (G.misses === 0) medals.push(["sweep", "#16A34A", "Photographic memory", "No misses at all"]);
    if (G.bestCombo >= 3) medals.push(["fire", "#EA580C", "Combo master", plural(G.bestCombo, "pair") + " in a row"]);
    if (opts.timer && secs <= 60) medals.push(["bolt", "#7C3AED", "Speed run", "Done in " + mmss(secs * 1000)]);
    if (G.peeks === 1 && stars === 3) medals.push(["cards", "#0F766E", "No peeking", "Three stars without a peek"]);
    var rows = [[art("match"), "Pairs found", D.pairs.length + " pairs, " + misses(G.misses), fmt(matchPts)]];
    if (opts.timer) rows.push([ico("i-timer"), "Time", mmss(secs * 1000) + (bonus ? ", with a time bonus" : ""), "+" + fmt(bonus)]);
    rows.push([FLAME, "Best combo", plural(G.bestCombo, "pair") + " in a row", ""]);
    taskResults({
      stars: stars, pts: G.pts, pct: Math.max(0, 1 - G.misses / 12),
      title: stars === 3 ? "Memory master" : stars === 2 ? "Sharp memory" : "Every pair found: play again for fewer misses",
      mood: stars === 3 ? "proud" : stars === 2 ? "cheer" : "happy", wear: stars === 3 ? ["crown"] : null,
      rows: rows, medals: medals,
      extra: reviewList("The pairs", D.pairs.map(function (p) { return '<span class="st-res-a">' + p.a + "</span> " + p.b; })),
      summary: "Every pair found, with " + misses(G.misses) + "."
    });
  }

  hooks.data = D;
  hooks.state = function () { return G; };
})();
