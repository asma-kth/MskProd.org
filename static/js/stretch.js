/* MskProd Computing - stretch tasks, Key Stage 3 and Key Stage 4.
 *
 * The tasks for one lesson. The Quiz Challenge has three rounds. Quiz Blitz
 * is a quiz show: a clock, four coloured tiles that each carry a shape, points
 * for speed, an answer streak and four computer players to race to the
 * podium. Quick Fire and Big Think are written answers, marked by the keyword
 * marker in quiz.js (window.MskMarker); the mark scheme and a model answer are
 * shown afterwards and the student can change the mark, as on the exam pages.
 * In This or That, Pixel the cat asks questions with two answers and reacts
 * to each choice. Memory Match is a card game: flip two cards at a time to
 * pair each word with its meaning. Key Stage 4 lessons add Sort It: drag each
 * statement into the right box, tap a box, or press its number. Every lesson
 * adds three games. Code Word: guess a secret word from its clue, and
 * every guess shows which letters are right. Link Up: twelve tiles hide three
 * groups of four. Bug Hunt: two statements are true and one has a mistake to
 * catch. Then three brain games replay the lesson as brain training: Odd One
 * Out (logic), Memory Flash (memory) and Fact or Fib (speed). Every lesson
 * ends with City Run: a robot cat races through a neon cyber city and every
 * lane is an answer; static/js/cityrun.js draws the street. Every result is rated
 * out of three diamonds. Best scores are kept on this device only.
 *
 * The hub page uses only the diamond painting near the top of this file.
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
  /* A cut diamond: the rating on every result, out of three. Its facets take
     their colours from custom properties, so the stylesheet lights it. */
  var GEM_FACETS = '<path d="M2 7.5 6.5 2h3L8 7.5Z" style="fill:var(--g2,#7DD3FC)"/><path d="M9.5 2h5L16 7.5H8Z" style="fill:var(--g1,#E0F2FE)"/>' +
    '<path d="M14.5 2h3L22 7.5h-6Z" style="fill:var(--g3,#38BDF8)"/><path d="M2 7.5h6l4 13Z" style="fill:var(--g3,#38BDF8)"/>' +
    '<path d="M8 7.5h8l-4 13Z" style="fill:var(--g2,#7DD3FC)"/><path d="M16 7.5h6l-10 13Z" style="fill:var(--g4,#0284C7)"/>' +
    '<path d="M6.5 2h11L22 7.5 12 20.5 2 7.5Z" fill="none" style="stroke:var(--g5,#075985)" stroke-width="1.3" stroke-linejoin="round"/>';
  var GEM = '<svg class="st-gem is-on" viewBox="0 0 24 22" aria-hidden="true" focusable="false">' + GEM_FACETS + "</svg>";
  function gemIcon(on) {
    return '<svg class="st-gem' + (on ? " is-on" : "") + '" viewBox="0 0 24 22" aria-hidden="true" focusable="false"><use href="#st-gem"></use></svg>';
  }
  function bigGem(on) {
    return '<svg class="st-biggem' + (on ? " is-on" : " is-off") + '" viewBox="0 0 64 56" aria-hidden="true" focusable="false">' +
      '<path d="M4 19 17 5h8l-4 14Z" style="fill:var(--g2)"/><path d="M25 5h14l4 14H21Z" style="fill:var(--g1)"/>' +
      '<path d="M39 5h8l13 14H43Z" style="fill:var(--g3)"/><path d="M4 19h17l11 34Z" style="fill:var(--g3)"/>' +
      '<path d="M21 19h22L32 53Z" style="fill:var(--g2)"/><path d="M43 19h17L32 53Z" style="fill:var(--g4)"/>' +
      '<path d="M17 5h30l13 14-28 34L4 19Z" fill="none" style="stroke:var(--g5)" stroke-width="3" stroke-linejoin="round"/>' +
      (on ? '<path d="M27 8.5h6l-3.5 7Z" fill="#fff" opacity=".85"/><path class="st-gem-spark" d="M53 1.5l1.6 3.4 3.4 1.6-3.4 1.6-1.6 3.4-1.6-3.4-3.4-1.6 3.4-1.6Z" fill="#fff"/>' : "") +
      "</svg>";
  }
  var MEDAL_ART = {
    gem: '<path d="M24 22h16l7 8-15 17-15-17Z" fill="#BAE6FD" stroke="#075985" stroke-width="2" stroke-linejoin="round"/><path d="M17 30h30M27 22l5 25 5-25" fill="none" stroke="#0284C7" stroke-width="1.6"/>',
    shield: '<path d="M32 17l12 4v9c0 8-5 13-12 16-7-3-12-8-12-16v-9Z" fill="#fff" stroke="#1E293B" stroke-width="2" stroke-linejoin="round"/><path d="M26.5 31l4 4 7-8" fill="none" stroke="#16A34A" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>',
    paw: '<ellipse cx="32" cy="36" rx="7.5" ry="6.5" fill="#fff" stroke="#1E293B" stroke-width="2"/><circle cx="23.5" cy="27" r="3.4" fill="#fff" stroke="#1E293B" stroke-width="2"/><circle cx="29" cy="22.5" r="3.4" fill="#fff" stroke="#1E293B" stroke-width="2"/><circle cx="35" cy="22.5" r="3.4" fill="#fff" stroke="#1E293B" stroke-width="2"/><circle cx="40.5" cy="27" r="3.4" fill="#fff" stroke="#1E293B" stroke-width="2"/>',
    crown: '<path d="M18 36 20 22l7 7 5-10 5 10 7-7 2 14Z" fill="#FDE047" stroke="#92400E" stroke-width="2" stroke-linejoin="round"/>',
    podium: '<path d="M20 40V31h8v-7h8v11h8v5Z" fill="#fff" stroke="#1E293B" stroke-width="2" stroke-linejoin="round"/>',
    sweep: '<path d="M21 31l7 7 15-15" fill="none" stroke="#fff" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>',
    fire: '<path d="M32 18c2 6 9 9 9 16a9 9 0 0 1-18 0c0-5 3-7 4-10 1.6 2.3 2 4 1.6 6.2C31 28 32.6 24 32 18Z" fill="#FDE047" stroke="#9A3412" stroke-width="2"/>',
    bolt: '<path d="M35 17 23 33h8l-3 13 13-17h-8Z" fill="#FDE047" stroke="#713F12" stroke-width="2" stroke-linejoin="round"/>',
    pen: '<path d="M22 41l3-9 14-14 6 6-14 14Z" fill="#fff" stroke="#1E293B" stroke-width="2" stroke-linejoin="round"/><path d="M22 41l9-3" stroke="#1E293B" stroke-width="2"/>',
    bulb: '<path d="M32 17a9 9 0 0 0-5 16.5V37h10v-3.5A9 9 0 0 0 32 17Z" fill="#FDE047" stroke="#713F12" stroke-width="2"/><path d="M28 41h8" stroke="#fff" stroke-width="2.4" stroke-linecap="round"/>',
    fish: '<path d="M19 29c4.5-6.5 13-7 18.5-2.2L43 22.5v13L37.5 31.2C32 36 23.5 35.5 19 29Z" fill="#FDBA74" stroke="#9A3412" stroke-width="2" stroke-linejoin="round"/><circle cx="25" cy="28" r="1.8" fill="#1E293B"/>',
    cards: '<rect x="19" y="18" width="14" height="19" rx="3" fill="#fff" stroke="#1E293B" stroke-width="2" transform="rotate(-10 26 27.5)"/><rect x="31" y="18" width="14" height="19" rx="3" fill="#FDE047" stroke="#1E293B" stroke-width="2" transform="rotate(9 38 27.5)"/>',
    box: '<path d="M20.5 26.5h23l-2.4 13h-18.2Z" fill="#fff" stroke="#1E293B" stroke-width="2" stroke-linejoin="round"/><path d="M25.5 21.5l5 5 9.5-9.5" fill="none" stroke="#FDE047" stroke-width="3.6" stroke-linecap="round" stroke-linejoin="round"/>'
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
    win: function () { [523, 659, 784, 1046, 784, 1046, 1318].forEach(function (f, i) { tone(f, i * 0.11, 0.26, "triangle", 0.1); }); },
    gem: function () { tone(1568, 0, 0.09, "triangle", 0.06); tone(2093, 0.06, 0.12, "triangle", 0.05); tone(2637, 0.12, 0.2, "sine", 0.045); },
    flip: function () { tone(740, 0, 0.05, "square", 0.025); tone(980, 0.04, 0.05, "square", 0.02); },
    level: function () { [659, 784, 988, 1318, 1568].forEach(function (f, i) { tone(f, i * 0.08, 0.22, "triangle", 0.08); }); },
    stamp: function () { tone(160, 0, 0.14, "square", 0.05); tone(90, 0.03, 0.16, "sine", 0.08); },
    coin: function () { tone(1760, 0, 0.05, "triangle", 0.035); tone(2350, 0.04, 0.07, "triangle", 0.03); },
    jump: function () { tone(440, 0, 0.1, "triangle", 0.05); tone(660, 0.05, 0.12, "triangle", 0.045); },
    hit: function () { tone(150, 0, 0.18, "square", 0.05); tone(95, 0.05, 0.22, "sine", 0.08); },
    splash: function () { tone(1200, 0, 0.05, "sine", 0.03); tone(800, 0.04, 0.08, "sine", 0.03); },
    whoosh: function () { tone(320, 0, 0.3, "sawtooth", 0.018); tone(170, 0.1, 0.35, "sawtooth", 0.018); }
  };
  var opts = store.get(OPTS, null) || {};
  if (typeof opts.timer !== "boolean") opts.timer = true;
  if (typeof opts.sound !== "boolean") opts.sound = false;
  function sfx(name) { if (opts.sound && SOUNDS[name]) { try { SOUNDS[name](); } catch (e) { /* sound is a nicety */ } } }

  /* ------------------------------------------------------------ confetti */
  function confetti(canvas, ms, gems) {
    if (calm() || !canvas || !canvas.getContext) return;
    var ctx = canvas.getContext("2d"), W, H, t0 = performance.now(), parts = [];
    var colours = gems ? ["#E0F2FE", "#7DD3FC", "#38BDF8", "#0EA5E9", "#A5F3FC", "#F0ABFC", "#FFFFFF"] :
      ["#D7263D", "#1F5FD1", "#F2B705", "#1E7B34", "#FDE047", "#F472B6", "#FFFFFF"];
    var dpr = Math.min(2, window.devicePixelRatio || 1);
    W = canvas.clientWidth; H = canvas.clientHeight;
    canvas.width = W * dpr; canvas.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    for (var i = 0; i < 160; i++) {
      var left = i % 2 === 0;
      parts.push({ x: left ? -10 : W + 10, y: H * (0.25 + Math.random() * 0.35), vx: (left ? 1 : -1) * (Math.random() * 9 + 4),
                   vy: -Math.random() * 12 - 3, r: Math.random() * 7 + 5, a: Math.random() * 6, va: (Math.random() - 0.5) * 0.3,
                   c: colours[i % colours.length], s: gems ? (i % 3 ? 3 : 1) : i % 4 });
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
      // a frame can be stamped a moment before t0, so k is kept at zero or more
      var k = Math.max(0, Math.min(1, (t - t0) / ms)), e = 1 - Math.pow(1 - k, 3);
      node.textContent = prefix + fmt(from + (to - from) * e);
      if (k < 1) requestAnimationFrame(step); else node.textContent = prefix + fmt(to);
    })(t0);
  }
  function escHtml(s) { return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;"); }
  /* A program printed with a question. On a phone it can be wider than the
     screen and scroll sideways, so it takes keyboard focus to be scrolled. */
  function codeBox(html) {
    return el("pre", { class: "st-code", tabindex: "0", role: "region", "aria-label": "Code" }, [el("code", { html: html })]);
  }

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
  var TASKS = ["quiz", "cat", "match", "sort", "word", "link", "bug", "odd", "flash", "fib", "run"];
  var TASK_NAMES = { quiz: "Quiz Challenge", cat: "This or That", match: "Memory Match", sort: "Sort It",
                     word: "Code Word", link: "Link Up", bug: "Bug Hunt",
                     odd: "Odd One Out", flash: "Memory Flash", fib: "Fact or Fib", run: "City Run" };
  var BRAIN = { odd: "Logic", flash: "Memory", fib: "Speed" };
  /* The Quiz Challenge keeps the lesson's own key, so results saved before
     the other tasks existed still count. */
  function recKey(base, task) { return task === "quiz" ? base : base + "/" + task; }
  var records = store.get(RECORDS, {}) || {};
  Array.prototype.forEach.call(document.querySelectorAll("[data-st-key]"), function (card) {
    var base = card.getAttribute("data-st-key");
    Array.prototype.forEach.call(card.querySelectorAll("[data-st-task]"), function (b) {
      var task = b.getAttribute("data-st-task"), r = records[recKey(base, task)], n = r ? r.s : 0;
      Array.prototype.forEach.call(b.querySelectorAll("[data-st-gems] .st-gem"), function (s, i) { s.classList.toggle("is-on", i < n); });
      var sr = b.querySelector("[data-st-sr]");
      if (sr) sr.textContent = TASK_NAMES[task] + ": " + (r ? n + " of 3 diamonds." : "not played yet.");
      b.classList.toggle("is-played", !!r);
    });
  });

  /* Hooks for tools/check_stretch.mjs and the browser tests. typedRight and
     wordMarks are hoisted, so they are ready here even on a page with no game. */
  var hooks = window.MskStretch = { typedRight: typedRight, wordMarks: wordMarks };

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
      best.innerHTML = '<span class="st-gems" aria-hidden="true">' + [0, 1, 2].map(function (i) { return gemIcon(i < r.s); }).join("") + "</span>";
      best.appendChild(document.createTextNode("Your best: " + plural(r.s, "diamond") + ", " + fmt(r.b) + " points"));
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
      Array.prototype.forEach.call(copy.querySelectorAll(".st-res-go, .px, .rc, canvas"), function (n) { n.remove(); });
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
    } else if (task === "word") {
      ui.wordN = el("span", { text: "0 / " + D.words.length });
      ui.ptsN = el("span", { text: "0" });
      ui.wordChip = el("span", { class: "st-chip" }, [el("small", { text: "Unlocked" }), ui.wordN]);
      ui.ptsChip = el("span", { class: "st-chip st-chip-score" }, [el("small", { text: "Points" }), ui.ptsN]);
      chips = [ui.wordChip, ui.ptsChip];
    } else if (task === "link") {
      ui.groupsN = el("span", { text: "0 / " + D.link.length });
      ui.timeN = el("span", { text: "0:00" });
      ui.groupsChip = el("span", { class: "st-chip" }, [el("small", { text: "Groups" }), ui.groupsN]);
      ui.timeChip = el("span", { class: "st-chip st-chip-time", hidden: !opts.timer }, [el("span", { html: ico("i-timer") }).firstChild, ui.timeN]);
      chips = [ui.groupsChip, ui.timeChip];
    } else if (BRAIN[task] || task === "run") {
      ui.progN = el("span", { text: "" });
      ui.progChip = el("span", { class: "st-chip" }, [el("small", { text: task === "flash" ? "Level" : task === "fib" ? "Card" : task === "run" ? "Question" : "Round" }), ui.progN]);
      ui.ptsN = el("span", { text: "0" });
      ui.ptsChip = el("span", { class: "st-chip st-chip-gem" }, [el("span", { class: "st-chip-gemico", html: GEM }), el("small", { text: "Points" }), ui.ptsN]);
      ui.multi = el("b", { class: "st-multi", hidden: true });
      ui.streak.appendChild(ui.multi);
      chips = [ui.progChip, ui.ptsChip, ui.streak];
    } else if (task === "bug") {
      ui.caughtN = el("span", { text: "0 / " + D.bugs.length });
      ui.caughtChip = el("span", { class: "st-chip" }, [el("small", { text: "Caught" }), ui.caughtN]);
      chips = [ui.caughtChip, ui.streak];
    } else if (task === "sort") {
      ui.sortN = el("span", { text: "0 / " + D.sort.i.length });
      ui.missN = el("span", { text: "0" });
      ui.timeN = el("span", { text: "0:00" });
      ui.sortChip = el("span", { class: "st-chip" }, [el("small", { text: "Sorted" }), ui.sortN]);
      ui.missChip = el("span", { class: "st-chip" }, [el("small", { text: "Misses" }), ui.missN]);
      ui.timeChip = el("span", { class: "st-chip st-chip-time", hidden: !opts.timer }, [el("span", { html: ico("i-timer") }).firstChild, ui.timeN]);
      chips = [ui.sortChip, ui.missChip, ui.timeChip];
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

  /* While a game is open it is the whole screen, so the page behind it is
     hidden from screen readers and from the keyboard, as behind any modal. */
  var behind = [];
  function lockScroll(on) {
    document.documentElement.classList.toggle("st-locked", on);
    behind.forEach(function (n) { n.removeAttribute("aria-hidden"); n.inert = false; });
    behind = [];
    if (!on) return;
    for (var n = stage; n && n.parentElement && n !== document.body; n = n.parentElement) {
      Array.prototype.forEach.call(n.parentElement.children, function (sib) {
        if (sib === n || /^(SCRIPT|TEMPLATE|STYLE|LINK)$/.test(sib.tagName) || sib.getAttribute("aria-hidden") === "true") return;
        sib.setAttribute("aria-hidden", "true");
        sib.inert = true;
        behind.push(sib);
      });
    }
  }
  /* Whether this lesson has a task: Sort It is a Key Stage 4 task, and Code
     Word, Link Up and Bug Hunt are Key Stage 3 games. */
  function has(task) {
    return task === "sort" ? !!D.sort : task === "word" ? !!D.words : task === "link" ? !!D.link :
      task === "bug" ? !!D.bugs : BRAIN[task] ? !!(D.odd && D.fib && D.flash && D.link) :
      task === "run" ? !!(D.run && D.fib && D.flash && window.MskCityRun) : !!TASK_NAMES[task];
  }
  function begin(task) {
    task = has(task) ? task : "quiz";
    if (task === "quiz") {
      G = { round: "blitz", qi: 0, streak: 0, bestStreak: 0, right: 0, blitzPts: 0, writtenPts: 0, times: [], marks: [],
            rivals: RIVALS.map(function (r) { return { id: r.id, name: r.name, av: r.av, face: r.face, skill: r.skill, pace: r.pace, pts: 0, streak: 0 }; }),
            order: ["you", "ada", "alan", "grace", "tim"], written: { short: [], long: [] }, done: false };
    } else {
      G = { round: task, qi: 0, streak: 0, bestStreak: 0, right: 0, pts: 0, answers: [], done: false, locked: false,
            shown: 0, hints: 0, fast: 0, misses: 0, firsts: 0, caught: 0 };
    }
    G.task = task;
    buildStage(task);
    stage.hidden = false;
    stage.setAttribute("data-round", task === "quiz" ? "blitz" : task);
    lockScroll(true);
    if (task === "quiz") splash("blitz");
    else if (task === "cat") catSplash();
    else if (task === "sort") sortSplash();
    else if (task === "word") wordSplash();
    else if (task === "link") linkSplash();
    else if (task === "bug") bugSplash();
    else if (task === "odd") oddSplash();
    else if (task === "flash") flashSplash();
    else if (task === "fib") fibSplash();
    else if (task === "run") runSplash();
    else matchSplash();
  }
  function leave(ask) {
    if (ask && G && !G.done && !window.confirm("Leave the game? This game's score will not be saved.")) return;
    var task = G ? G.task : "quiz";
    stopClock();
    if (G && G.tick) clearInterval(G.tick);
    if (G && G.busy) clearTimeout(G.busy);
    if (G && G.world) { G.world.destroy(); G.world = null; }
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
    if (G.task === "word" && G.word && !G.locked && !G.done) {
      /* Code Word is typed straight onto its tiles. Enter sends the guess
         from anywhere except a button that has a job of its own; a letter key
         of the drawn keyboard does not count as one. */
      var letterKey = tag === "button" && e.target.classList.contains("st-kb") && (e.target.getAttribute("data-k") || "").length === 1;
      if (/^[a-zA-Z]$/.test(e.key)) { e.preventDefault(); wordType(e.key.toUpperCase()); return; }
      if (e.key === "Backspace") { e.preventDefault(); wordDelete(); return; }
      if (e.key === "Enter" && ((tag !== "button" && tag !== "a") || letterKey)) { e.preventDefault(); wordSubmit(); return; }
    }
    if (G.task === "fib" && G.deck && !G.locked && !G.done && (e.key === "ArrowLeft" || e.key === "ArrowRight")) {
      e.preventDefault(); fibAnswer(e.key === "ArrowRight", false); return;
    }
    if (G.task === "run" && G.world && !G.done && runKey(e, tag)) { e.preventDefault(); return; }
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
    if (q.c) card.appendChild(codeBox(q.c));
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
    if (w.c) card.appendChild(codeBox(w.c));

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
    s.appendChild(el("div", { class: "st-res-stars", role: "img", "aria-label": stars + " of 3 diamonds", html: bigGem(stars >= 1) + bigGem(stars >= 2) + bigGem(stars >= 3) }));
    var totalN = el("span", { text: "0" });
    s.appendChild(el("div", { class: "st-res-total" }, [totalN, el("small", { text: "points" })]));
    if (newBest) s.appendChild(el("span", { class: "st-res-best", text: "New personal best!" }));

    var card = el("div", { class: "st-res-card" });
    var who = (opts.name || "").trim();
    card.appendChild(el("p", { class: "st-res-name", text: (who ? who + " \u00b7 " : "") + D.where + " \u00b7 " +
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
    say("Finished. " + stars + " of 3 diamonds and " + fmt(total) + " points." + (newBest ? " New personal best." : ""));
    focusFirst(s.querySelector("h2"));
  }

  /* ------------------------------------------------- shared result screen */
  /* The task after this one, of the tasks this lesson has. */
  function nextTask(task) {
    var mine = TASKS.filter(has), i = mine.indexOf(task);
    return i > -1 && i < mine.length - 1 ? mine[i + 1] : null;
  }
  function resultButtons(task) {
    var go = el("div", { class: "st-res-go" });
    go.appendChild(el("button", { class: "st-go", type: "button", html: ico("i-repeat") + " Play again", onclick: function () { leave(false); begin(task); } }));
    var nt = nextTask(task);
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
    var cat = o.hero || pixel(o.mood);
    if (o.wear && !o.hero) wear(cat, o.wear);
    s.appendChild(el("div", { class: "st-res-top" }, [cat, el("p", { class: "st-res-title", text: o.title })]));
    s.appendChild(el("h2", { tabindex: "-1", text: D.lesson }));
    s.appendChild(el("div", { class: "st-res-stars", role: "img", "aria-label": o.stars + " of 3 diamonds", html: bigGem(o.stars >= 1) + bigGem(o.stars >= 2) + bigGem(o.stars >= 3) }));
    var totalN = el("span", { text: "0" });
    s.appendChild(el("div", { class: "st-res-total" }, [totalN, el("small", { text: "points" })]));
    if (newBest) s.appendChild(el("span", { class: "st-res-best", text: "New personal best!" }));

    var card = el("div", { class: "st-res-card" });
    var who = (opts.name || "").trim();
    card.appendChild(el("p", { class: "st-res-name", text: (who ? who + " · " : "") + TASK_NAMES[G.task] + " · " + D.where +
      " · " + new Date().toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" }) }));
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
    if (o.stars >= 2) setTimeout(function () { confetti(ui.confetti, 4200, true); }, calm() ? 0 : 900);
    sfx("win");
    say("Finished. " + o.summary + " " + o.stars + " of 3 diamonds and " + fmt(o.pts) + " points." + (newBest ? " New personal best." : ""));
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
    if (q.c) bubble.appendChild(codeBox(q.c));
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
  /* A card label inside a sentence: "Tag" reads as tag, but CSS stays CSS. */
  function pn(side) { var t = D.pn[side]; return /^[A-Z0-9]+$/.test(t) ? t : t.toLowerCase(); }
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
    var sub = D.pairs.length * 2 + " cards lie face down. Flip two at a time to match each " + pn(0) + " card to its " +
      pn(1) + " card. You can peek once.";
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
    return c.up ? n + ": " + c.text + ", " + pn(c.side) : n + ", face down";
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
      el("p", { class: "st-match-hint", text: "Match each " + pn(0) + " card to its " + pn(1) + " card." }), ui.peek]));
    s.appendChild(grid);
    fitSoon();
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

  // A long word shrinks until it fits on its card whole, instead of breaking
  // in the middle. Code still too wide at 62% of the size breaks where it must.
  function brokenWord(t) {
    var walk = document.createTreeWalker(t, NodeFilter.SHOW_TEXT), r = document.createRange(), node, m, i;
    while ((node = walk.nextNode())) {
      var re = /\S+/g;
      while ((m = re.exec(node.data))) {
        r.setStart(node, m.index);
        r.setEnd(node, m.index + m[0].length);
        var rects = r.getClientRects(), top = null;
        for (i = 0; i < rects.length; i++) {
          if (rects[i].width < 0.5) continue;
          if (top === null) top = rects[i].top;
          else if (Math.abs(rects[i].top - top) > 2) return true;
        }
      }
    }
    return false;
  }
  function fitWords(root, sel, least) {
    Array.prototype.forEach.call(root.querySelectorAll(sel), function (t) {
      t.style.fontSize = "";
      var size = parseFloat(getComputedStyle(t).fontSize), min = size * least;
      for (var n = 0; n < 12 && size > min && brokenWord(t); n++) {
        size = Math.max(min, size * 0.93);
        t.style.fontSize = size + "px";
      }
    });
  }
  // Memory Match cards, Link Up tiles and Bug Hunt statements, with how far each may shrink.
  var FIT = [[".st-card-t", 0.62], [".st-lt-t", 0.7], [".st-bug-t", 0.85], [".st-odd-t", 0.7], [".st-fcard-t", 0.62], [".st-fib-t", 0.8]];
  function fitScreen() {
    if (!ui.screen) return;
    FIT.forEach(function (f) { fitWords(ui.screen, f[0], f[1]); });
  }
  function fitSoon() {
    fitScreen();
    if (document.fonts && document.fonts.ready) document.fonts.ready.then(fitScreen);
  }
  var fitTimer = 0;
  window.addEventListener("resize", function () { clearTimeout(fitTimer); fitTimer = setTimeout(fitScreen, 120); });

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
    if (G.open.length < 2) { say(c.text + ", " + pn(c.side) + ". Now find its partner."); return; }
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
    if (G.peeks === 1 && stars === 3) medals.push(["cards", "#0F766E", "No peeking", "Three diamonds without a peek"]);
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

  /* ============================================================= SORT IT */
  /* One card at a time: drag it into a box, tap a box, or press the box's
     number. A wrong box shows where the card belongs and why before the next
     card is dealt. */
  var BIN_SHAPES = [0, 2, 3, 1];
  var GRIP = '<svg viewBox="0 0 24 10" aria-hidden="true" focusable="false"><circle cx="6" cy="3" r="1.6"/><circle cx="12" cy="3" r="1.6"/><circle cx="18" cy="3" r="1.6"/><circle cx="6" cy="8" r="1.6"/><circle cx="12" cy="8" r="1.6"/><circle cx="18" cy="8" r="1.6"/></svg>';
  function binName(k) { return stripTags(D.sort.b[k]); }
  function binsSpoken() { return D.sort.b.map(function (b, k) { return (k + 1) + ", " + stripTags(b); }).join("; "); }
  function sortChips(bump) {
    ui.sortN.textContent = G.deck.filter(function (c) { return c.ok !== undefined; }).length + " / " + G.deck.length;
    ui.missN.textContent = String(G.misses);
    if (bump) { ui.sortChip.classList.remove("is-bump"); void ui.sortChip.offsetWidth; ui.sortChip.classList.add("is-bump"); }
    paintDots(G.deck.map(function (c) { return c.ok === true ? 1 : c.ok === false ? 0 : -1; }), G.si);
  }
  function binLabel(k) {
    var n = G.inBin[k];
    return binName(k) + ", box " + (k + 1) + (n ? ", " + plural(n, "card") + " so far" : "");
  }

  function sortSplash() {
    var n = D.sort.i.length;
    label("Sort It", plural(n, "card"));
    ui.dots.innerHTML = "";
    var s = screen("st-splash");
    s.appendChild(el("span", { class: "st-splash-tag", text: "Sort It" }));
    s.appendChild(el("div", { class: "st-splash-ico", "aria-hidden": "true", html: art("sort") }));
    s.appendChild(el("h2", { tabindex: "-1", text: "Sort It" }));
    s.appendChild(el("p", { class: "st-sort-prompt", html: D.sort.p }));
    var how = "Drag each of the " + n + " cards into the right box, tap a box, or press its number. Cards sorted in a row win combo points.";
    s.appendChild(el("p", { text: how }));
    var row = el("div", { class: "st-sort-preview", "aria-hidden": "true" });
    D.sort.b.forEach(function (b, k) {
      row.appendChild(el("span", { class: "st-bin-chip st-bin-" + k, html: '<span class="st-bin-key">' + (k + 1) + "</span>" + b }));
    });
    s.appendChild(row);
    var go = el("button", { class: "st-go", type: "button", html: ico("i-play") + " Deal the cards" });
    go.addEventListener("click", sortDeal);
    s.appendChild(go);
    sfx("board");
    say("Sort It. " + stripTags(D.sort.p) + " " + how + " The boxes are " + binsSpoken() + ".");
    focusFirst(go);
  }

  function sortDeal() {
    if (!G) return;
    G.deck = shuffle(D.sort.i.map(function (c, k) { return { k: k, t: c.t, b: c.b, x: c.x, text: stripTags(c.t) }; }));
    G.si = 0; G.right = 0; G.misses = 0; G.combo = 0; G.bestCombo = 0; G.pts = 0; G.t0 = 0; G.tEnd = 0;
    G.locked = false; G.drag = null; G.lastBin = 0;
    G.inBin = D.sort.b.map(function () { return 0; });
    var s = screen("st-sort");
    ui.sortLeft = el("span", { class: "st-sort-left" });
    s.appendChild(el("div", { class: "st-sort-head" }, [el("p", { class: "st-sort-q", html: D.sort.p }), ui.sortLeft]));
    ui.pile = el("div", { class: "st-sort-pile", "aria-hidden": "true" });
    ui.slot = el("div", { class: "st-sort-slot" });
    s.appendChild(el("div", { class: "st-sort-deck" }, [ui.pile, ui.slot]));
    ui.hint = el("p", { class: "st-sort-hint", text: "Drag the card into a box, tap a box, or press 1 to " + D.sort.b.length + "." });
    s.appendChild(ui.hint);
    ui.bins = D.sort.b.map(function (b, k) {
      var bin = el("button", { class: "st-bin st-bin-" + k, type: "button", "data-bin": k }, [
        el("span", { class: "st-bin-top", "aria-hidden": "true" }, [
          el("span", { class: "st-bin-key", text: String(k + 1) }),
          el("span", { class: "st-bin-shape", html: '<svg viewBox="0 0 24 24">' + SHAPES[BIN_SHAPES[k]] + "</svg>" }),
          el("span", { class: "st-bin-n", text: "0" })]),
        el("span", { class: "st-bin-label", html: b }),
        el("span", { class: "st-bin-tray", "aria-hidden": "true" })]);
      bin.addEventListener("click", function () { G.lastBin = k; sortDrop(k); });
      return bin;
    });
    ui.binRow = el("div", { class: "st-bins", role: "group", "aria-label": "Boxes", "data-n": D.sort.b.length }, ui.bins);
    s.appendChild(ui.binRow);
    ui.bins.forEach(function (b, k) { b.setAttribute("aria-label", binLabel(k)); });
    ui.tiles = ui.bins;
    sfx("board");
    sortCard();
    focusFirst(ui.bins[0]);
  }

  function paintPile() {
    var left = G.deck.length - G.si - 1;
    ui.pile.innerHTML = "";
    for (var i = Math.min(3, left); i > 0; i--) ui.pile.appendChild(el("i", { style: "--n:" + i }));
    ui.sortLeft.textContent = left > 0 ? plural(left, "card") + " to come" : "Last card";
  }

  function sortCard() {
    var c = G.deck[G.si];
    label("Sort It", "Card " + (G.si + 1) + " of " + G.deck.length);
    paintPile();
    var card = el("div", { class: "st-sort-card" }, [
      el("span", { class: "st-sort-grip", html: GRIP }),
      el("p", { class: "st-sort-t", html: c.t })]);
    card.addEventListener("pointerdown", dragStart);
    card.addEventListener("pointermove", dragMove);
    card.addEventListener("pointerup", dragEnd);
    card.addEventListener("pointercancel", dragEnd);
    ui.slot.innerHTML = "";
    ui.slot.appendChild(card);
    ui.card = card;
    G.locked = false;
    sortChips(false);
    say("Card " + (G.si + 1) + " of " + G.deck.length + ": " + c.text + ". Which box? " + binsSpoken() + ".");
  }

  /* ----- dragging */
  function binAt(x, y) {
    for (var k = 0; k < ui.bins.length; k++) {
      var r = ui.bins[k].getBoundingClientRect();
      if (x >= r.left - 6 && x <= r.right + 6 && y >= r.top - 6 && y <= r.bottom + 6) return k;
    }
    return -1;
  }
  function overBin(k) {
    var d = G.drag;
    if (k === d.over) return;
    if (d.over >= 0) ui.bins[d.over].classList.remove("is-over");
    if (k >= 0) { ui.bins[k].classList.add("is-over"); sfx("tick"); }
    d.over = k;
  }
  function dragStart(e) {
    if (!G || G.done || G.locked || G.drag || (e.button !== undefined && e.button > 0)) return;
    if (e.target.closest && e.target.closest("button")) return;
    e.preventDefault();
    startWatch();
    try { ui.card.setPointerCapture(e.pointerId); } catch (err) { /* capture is a nicety */ }
    G.drag = { id: e.pointerId, x0: e.clientX, y0: e.clientY, moved: false, over: -1 };
    ui.card.classList.add("is-drag");
  }
  function dragMove(e) {
    var d = G && G.drag;
    if (!d || e.pointerId !== d.id) return;
    var dx = e.clientX - d.x0, dy = e.clientY - d.y0;
    if (!d.moved && Math.abs(dx) + Math.abs(dy) < 6) return;
    d.moved = true;
    ui.card._at = { x: dx, y: dy };
    ui.card.style.translate = dx + "px " + dy + "px";
    ui.card.style.rotate = Math.max(-9, Math.min(9, dx / 22)) + "deg";
    overBin(binAt(e.clientX, e.clientY));
  }
  function dragEnd(e) {
    var d = G && G.drag;
    if (!d || e.pointerId !== d.id) return;
    var k = e.type === "pointerup" ? binAt(e.clientX, e.clientY) : -1;
    overBin(-1);
    G.drag = null;
    ui.card.classList.remove("is-drag");
    if (!d.moved) { sortNudge(); return; }
    if (k >= 0) { G.lastBin = k; sortDrop(k); } else springBack(ui.card);
  }
  function springBack(card) {
    card._at = { x: 0, y: 0 };
    card.style.translate = "";
    card.style.rotate = "";
  }
  function sortNudge() {
    ui.card.classList.remove("is-nudge"); void ui.card.offsetWidth; ui.card.classList.add("is-nudge");
    ui.hint.classList.remove("is-flash"); void ui.hint.offsetWidth; ui.hint.classList.add("is-flash");
    say(ui.hint.textContent);
  }
  /* The card flies into a box: from wherever it is, dragged or not, to the
     middle of the box, shrinking as it goes. */
  function flyTo(card, k, done) {
    var game = G;
    var finish = function () { if (G === game && !G.done) done(); };
    if (calm()) { finish(); return; }
    var a = card.getBoundingClientRect(), b = ui.bins[k].getBoundingClientRect(), at = card._at || { x: 0, y: 0 };
    var dx = at.x + (b.left + b.width / 2) - (a.left + a.width / 2), dy = at.y + (b.top + b.height / 2) - (a.top + a.height / 2);
    card.classList.add("is-flying");
    void card.offsetWidth;
    card.style.translate = dx + "px " + dy + "px";
    card.style.rotate = (dx > 0 ? 8 : -8) + "deg";
    card.style.scale = "0.18";
    card.style.opacity = "0";
    setTimeout(finish, 430);
  }
  function landIn(k, ok) {
    var bin = ui.bins[k];
    G.inBin[k] += 1;
    bin.querySelector(".st-bin-n").textContent = String(G.inBin[k]);
    bin.querySelector(".st-bin-tray").appendChild(el("i", { class: ok ? "" : "is-miss" }));
    bin.setAttribute("aria-label", binLabel(k));
    bin.classList.remove("is-hit"); void bin.offsetWidth; bin.classList.add("is-hit");
  }
  function popIn(node, text, cls) {
    if (!cls) Array.prototype.forEach.call(ui.binRow.querySelectorAll(".st-pop"), function (o) { o.remove(); });
    var p = el("span", { class: "st-pop" + (cls ? " " + cls : ""), "aria-hidden": "true", text: text });
    node.appendChild(p);
    setTimeout(function () { if (p.parentNode) p.parentNode.removeChild(p); }, 1300);
  }

  /* ----- sorting */
  function sortDrop(k) {
    if (!G || G.done || G.locked || !ui.card || G.drag) return;
    startWatch();
    G.locked = true;
    var c = G.deck[G.si];
    if (c.b === k) sortRight(c, k); else sortWrong(c, k);
  }
  function sortRight(c, k) {
    c.ok = true;
    G.right += 1; G.combo += 1;
    G.bestCombo = Math.max(G.bestCombo, G.combo);
    var gain = 100 + 50 * Math.min(G.combo - 1, 4);
    G.pts += gain;
    sortChips(true);
    sfx("good");
    say("Right: " + binName(k) + "." + (G.combo >= 3 ? " A combo of " + G.combo + "." : ""));
    flyTo(ui.card, k, function () {
      landIn(k, true);
      popIn(ui.bins[k], "+" + gain);
      if (G.combo >= 3) popIn(ui.bins[k], "Combo x" + G.combo + "!", "is-combo");
      sortNext();
    });
  }
  function sortWrong(c, k) {
    c.ok = false;
    G.misses += 1; G.combo = 0;
    var card = ui.card, last = G.si === G.deck.length - 1;
    springBack(card);
    card.classList.add("is-wrong");
    ui.bins[k].classList.add("is-no");
    ui.bins[c.b].classList.add("is-answer");
    var next = el("button", { class: "st-go st-sort-next", type: "button", html: (last ? "See my results " : "Next card ") + ico("i-arrow-right") });
    card.appendChild(el("div", { class: "st-sort-fb" }, [
      el("p", { class: "st-sort-fb-h", html: '<span class="st-nw">' + ico("i-cross") + " Not " + D.sort.b[k] + ".</span> It goes in <b>" + D.sort.b[c.b] + "</b>." }),
      el("p", { class: "st-sort-fb-x", html: c.x }), next]));
    next.addEventListener("click", function () {
      if (!G || G.done || next.disabled) return;
      next.disabled = true;
      ui.bins[k].classList.remove("is-no");
      ui.bins[c.b].classList.remove("is-answer");
      card.classList.remove("is-wrong");
      flyTo(card, c.b, function () { landIn(c.b, false); sortNext(); });
    });
    sortChips(false);
    sfx("bad");
    say("Not quite. It goes in " + binName(c.b) + ". " + stripTags(c.x));
    focusFirst(next);
  }
  function sortNext() {
    G.si += 1;
    if (G.si >= G.deck.length) {
      G.tEnd = performance.now();
      clearInterval(G.tick); G.tick = 0;
      if (ui.timeN) ui.timeN.textContent = mmss(watch());
      ui.slot.innerHTML = "";
      ui.pile.innerHTML = "";
      ui.sortLeft.textContent = "All sorted";
      sortChips(false);
      var game = G;
      setTimeout(function () { if (G === game) sortResults(); }, calm() ? 300 : 800);
      return;
    }
    sortCard();
    if (!stage.contains(document.activeElement) || document.activeElement === document.body) focusFirst(ui.bins[G.lastBin] || ui.bins[0]);
  }

  function sortResults() {
    if (!G || G.done) return;
    var n = G.deck.length, secs = Math.floor(watch() / 1000);
    var bonus = opts.timer ? Math.max(0, 500 - 5 * secs) : 0;
    var sortPts = G.pts;
    G.pts += bonus;
    var pct = G.right / n;
    var stars = G.right === n ? 3 : pct >= 0.75 ? 2 : 1;
    var medals = [];
    if (G.right === n) medals.push(["box", "#16A34A", "Perfect sort", "Every card in the right box"]);
    if (G.bestCombo >= 6) medals.push(["fire", "#EA580C", "Combo king", plural(G.bestCombo, "card") + " in a row"]);
    if (opts.timer && secs <= 50 && pct >= 0.75) medals.push(["bolt", "#7C3AED", "Speed sorter", "Done in " + mmss(secs * 1000)]);
    var rows = [[art("sort"), "Cards sorted", G.right + " of " + n + " right first time", fmt(sortPts)]];
    if (opts.timer) rows.push([ico("i-timer"), "Time", mmss(secs * 1000) + (bonus ? ", with a time bonus" : ""), "+" + fmt(bonus)]);
    rows.push([FLAME, "Best combo", plural(G.bestCombo, "card") + " in a row", ""]);
    var extra = el("div", { class: "st-res-extra" });
    var missed = G.deck.filter(function (c) { return !c.ok; });
    if (missed.length) {
      extra.appendChild(reviewList("Look again at these", missed.map(function (c) {
        return c.t + ' <span class="st-res-ans">' + D.sort.b[c.b] + ": " + c.x + "</span>";
      })));
    }
    extra.appendChild(reviewList("The boxes", D.sort.b.map(function (b, k) {
      return '<span class="st-res-a">' + b + "</span> " + D.sort.i.filter(function (c) { return c.b === k; }).map(function (c) { return c.t; }).join("; ");
    })));
    taskResults({
      stars: stars, pts: G.pts, pct: pct,
      title: stars === 3 ? "Sorting champion" : stars === 2 ? "Sharp sorting" : "All sorted: play again to get more right first time",
      mood: stars === 3 ? "proud" : stars === 2 ? "cheer" : "happy", wear: stars === 3 ? ["crown"] : null,
      rows: rows, medals: medals, extra: extra,
      summary: G.right + " of " + n + " cards right first time."
    });
  }

  /* ------------------------------------------- shared by the three games */
  /* Later, unless the game has been left or replaced in the meantime. */
  function after(ms, fn) {
    var game = G;
    return setTimeout(function () { if (G === game && !stage.hidden) fn(); }, ms);
  }
  /* The panel under a round once it is over: what happened, why, and the way on. */
  function roundPanel(ok, head, gain, extra, html, nextText, onNext) {
    var next = el("button", { class: "st-go", type: "button", html: nextText + " " + ico("i-arrow-right") });
    next.addEventListener("click", function () { if (!next.disabled) { next.disabled = true; onNext(); } });
    var fb = el("div", { class: "st-catfb is-plain " + (ok ? "is-ok" : "is-bad"), role: "status" }, [
      el("div", { class: "st-catfb-head" }, [
        el("span", { class: "st-catfb-badge", "aria-hidden": "true", html: ico(ok ? "i-check" : "i-cross") }),
        el("b", { text: head }),
        gain ? el("span", { class: "st-catfb-pts", text: "+" + gain }) : null]),
      extra ? el("p", { class: "st-catfb-streak", html: FLAME + "<span>" + extra + "</span>" }) : null,
      el("p", { class: "st-catfb-x", html: html }),
      el("div", { class: "st-fb-go" }, [next])
    ]);
    ui.fb.appendChild(fb);
    setTimeout(function () {
      try { fb.scrollIntoView({ behavior: calm() ? "auto" : "smooth", block: "nearest" }); } catch (e) { fb.scrollIntoView(false); }
      next.focus({ preventScroll: true });
    }, calm() ? 0 : 350);
    return fb;
  }
  function bump(chip) { chip.classList.remove("is-bump"); void chip.offsetWidth; chip.classList.add("is-bump"); }
  function gridKeys(e, grid, sel) {
    if (["ArrowLeft", "ArrowRight", "ArrowUp", "ArrowDown", "Home", "End"].indexOf(e.key) < 0) return;
    var cells = Array.prototype.slice.call(grid.querySelectorAll(sel));
    var i = cells.indexOf(document.activeElement);
    if (i < 0) return;
    var cols = getComputedStyle(grid).gridTemplateColumns.split(" ").length || 1;
    var j = e.key === "ArrowLeft" ? i - 1 : e.key === "ArrowRight" ? i + 1 : e.key === "ArrowUp" ? i - cols :
      e.key === "ArrowDown" ? i + cols : e.key === "Home" ? 0 : cells.length - 1;
    if (j < 0 || j >= cells.length) return;
    e.preventDefault();
    cells[j].focus();
  }

  /* ============================================================ CODE WORD */
  /* A clue, a row of empty tiles and five guesses. After each guess every
     letter is marked: right place, in the word but somewhere else, or not in
     the word. Each mark is a shape as well as a colour. */
  var WORD_TRIES = 5;
  var KEY_ROWS = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"];
  var MARK_CLS = ["is-no", "is-near", "is-yes"];
  var MARK_SAY = ["not in the word", "in the word but in the wrong place", "in the right place"];
  var MARK_ART = ["",
    '<svg viewBox="0 0 12 12"><circle cx="6" cy="6" r="3.7" fill="none" stroke="currentColor" stroke-width="2.3"/></svg>',
    '<svg viewBox="0 0 12 12"><path d="M1.8 6.5l2.7 2.7L10.2 3.3" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/></svg>'];
  var BACKSPACE = '<svg viewBox="0 0 30 20" aria-hidden="true" focusable="false"><path d="M10 2h16a2 2 0 0 1 2 2v12a2 2 0 0 1-2 2H10L2 10Z" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linejoin="round"/>' +
    '<path d="M14 6.5l7 7M21 6.5l-7 7" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg>';

  /* One guess marked against the word, a mark for each letter: 2 in the right
     place, 1 in the word but somewhere else, 0 not in the word. A letter is
     only marked as many times as the word has it. word_marks in
     mskbuild/stretchcheck.py is the same marking in Python. */
  function wordMarks(guess, answer) {
    guess = String(guess).toUpperCase();
    answer = String(answer).toUpperCase();
    var marks = [], spare = {}, i, ch;
    for (i = 0; i < guess.length; i++) marks.push(0);
    for (i = 0; i < answer.length; i++) {
      ch = answer.charAt(i);
      if (i < guess.length && guess.charAt(i) === ch) marks[i] = 2;
      else spare[ch] = (spare[ch] || 0) + 1;
    }
    for (i = 0; i < guess.length; i++) {
      ch = guess.charAt(i);
      if (marks[i] === 0 && spare[ch] > 0) { marks[i] = 1; spare[ch] -= 1; }
    }
    return marks;
  }
  function guesses(n) { return n === 1 ? "1 guess" : n + " guesses"; }
  /* A padlock: shut, open or lost. `dark` draws its shackle for a pale background. */
  function lockArt(state, dark) {
    var open = state === "open", lost = state === "lost";
    return '<svg viewBox="0 0 40 46" aria-hidden="true" focusable="false">' +
      '<path d="' + (open ? "M12.5 21v-8a7.5 7.5 0 0 1 15 0v1.5" : "M12.5 22v-7.5a7.5 7.5 0 0 1 15 0V22") + '" fill="none" stroke="' + (dark ? "#64748B" : "#E2E8F0") + '" stroke-width="4.6" stroke-linecap="round"/>' +
      '<rect x="5.5" y="20.5" width="29" height="23" rx="6" fill="' + (open ? "#4ADE80" : lost ? "#FCA5A5" : "#FBBF24") + '" stroke="#1E293B" stroke-width="2.4"/>' +
      (open ? '<path d="M13.5 32l4.4 4.4 8.6-9.2" fill="none" stroke="#14532D" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>' :
       lost ? '<path d="M15 27l10 10M25 27 15 37" stroke="#7F1D1D" stroke-width="3.2" stroke-linecap="round"/>' :
       '<circle cx="20" cy="29.5" r="3.2" fill="#1E293B"/><path d="M20 31v6" stroke="#1E293B" stroke-width="3.2" stroke-linecap="round"/>') + "</svg>";
  }
  function wordTile(letter, mark) {
    return el("span", { class: "st-wt" + (mark === undefined ? "" : " is-filled " + MARK_CLS[mark]) }, [
      el("b", { text: letter || "" }),
      el("i", { "aria-hidden": "true", html: mark === undefined ? "" : MARK_ART[mark] })]);
  }
  function wordDots() { return D.words.map(function (w, i) { return i < G.answers.length ? (G.answers[i] ? 1 : 0) : -1; }); }
  function wordChips(up) {
    ui.wordN.textContent = G.right + " / " + D.words.length;
    ui.wordChip.setAttribute("aria-label", G.right + " of " + D.words.length + " code words found");
    ui.ptsN.textContent = fmt(G.pts);
    if (up) bump(ui.ptsChip);
  }
  function locksLabel() {
    var open = G.answers.filter(Boolean).length;
    return "Locks: " + open + " of " + D.words.length + " open";
  }

  function wordSplash() {
    var n = D.words.length;
    G.tries = []; G.firsts = 0;
    label("Code Word", plural(n, "word"));
    ui.dots.innerHTML = "";
    var s = screen("st-splash st-word-splash");
    s.appendChild(el("span", { class: "st-splash-tag", text: "Code Word" }));
    s.appendChild(el("div", { class: "st-splash-ico", "aria-hidden": "true", html: art("word") }));
    s.appendChild(el("h2", { tabindex: "-1", text: "Code Word" }));
    var sub = plural(n, "code word") + " lock Pixel's treat tin. Read each clue and guess the word. You get " +
      WORD_TRIES + " guesses, and after each one the tiles show how close you are.";
    s.appendChild(el("p", { text: sub }));
    var key = el("ul", { class: "st-word-key" });
    [[2, "G", "Right letter, right place"], [1, "A", "In the word, wrong place"], [0, "X", "Not in the word"]].forEach(function (k) {
      key.appendChild(el("li", {}, [wordTile(k[1], k[0]), el("span", { text: k[2] })]));
    });
    s.appendChild(key);
    var go = el("button", { class: "st-go", type: "button", html: ico("i-play") + " Start" });
    go.addEventListener("click", function () { wordRound(0); });
    s.appendChild(go);
    sfx("board");
    say("Code Word. " + sub + " A tick means the right letter in the right place. A ring means the letter is in the word but in the wrong place.");
    focusFirst(go);
  }

  function keyBtn(html, name, cls, fn) {
    var b = el("button", { class: "st-kb" + (cls ? " " + cls : ""), type: "button", "aria-label": name, "data-k": name, html: html });
    /* A click or tap presses the key without moving the focus onto it. */
    b.addEventListener("mousedown", function (e) { e.preventDefault(); });
    b.addEventListener("click", fn);
    return b;
  }

  function wordRound(i) {
    if (!G) return;
    G.qi = i; G.locked = false;
    var w = D.words[i], n = w.w.length;
    var W = G.word = { answer: w.w, n: n, row: 0, cur: "", rows: [], best: {} };
    label("Code Word", "Word " + (i + 1) + " of " + D.words.length);
    paintDots(wordDots(), i);
    wordChips(false);
    var s = screen("st-word");
    ui.locks = el("div", { class: "st-locks", role: "img", "aria-label": locksLabel() });
    D.words.forEach(function (x, k) {
      var state = k < G.answers.length ? (G.answers[k] ? "open" : "lost") : "shut";
      ui.locks.appendChild(el("span", { class: "st-lock is-" + state + (k === i ? " is-now" : ""), html: lockArt(state) }));
    });
    G.cat = pixel("think");
    var h = el("h2", { class: "st-word-q", tabindex: "-1", html: w.c });
    s.appendChild(el("div", { class: "st-word-top" }, [
      G.cat ? el("div", { class: "st-word-host", "aria-hidden": "true" }, [G.cat]) : null,
      el("div", { class: "st-word-clue" }, [
        el("p", { class: "st-qmeta" }, [el("span", { text: "Clue " + (i + 1) + " of " + D.words.length }), el("span", { class: "st-kind", text: n + " letters" })]),
        h]),
      ui.locks]));
    var board = el("div", { class: "st-word-board", style: "--n:" + n });
    for (var r = 0; r < WORD_TRIES; r++) {
      var row = el("div", { class: "st-word-row", role: "img", "aria-label": "Guess " + (r + 1) + ": not used yet" });
      for (var c = 0; c < n; c++) row.appendChild(wordTile("", undefined));
      board.appendChild(row);
      W.rows.push(row);
    }
    s.appendChild(board);
    ui.wordMsg = el("p", { class: "st-word-msg", "aria-hidden": "true" });
    s.appendChild(ui.wordMsg);
    ui.keys = el("div", { class: "st-kbd", role: "group", "aria-label": "Letter keys" });
    KEY_ROWS.forEach(function (letters, k) {
      var line = el("div", { class: "st-kbd-row" });
      if (k === 2) line.appendChild(keyBtn("Enter", "Enter", "is-wide", wordSubmit));
      letters.split("").forEach(function (ch) { line.appendChild(keyBtn(ch, ch, "", function () { wordType(ch); })); });
      if (k === 2) line.appendChild(keyBtn(BACKSPACE, "Delete", "is-wide", wordDelete));
      ui.keys.appendChild(line);
    });
    s.appendChild(ui.keys);
    ui.fb = el("div", { class: "st-fbslot" });
    s.appendChild(ui.fb);
    wordPaintRow(false);
    say("Word " + (i + 1) + " of " + D.words.length + ": " + n + " letters. Clue: " + stripTags(w.c) + " Type your guess, then press Enter.");
    focusFirst(h);
  }

  function wordPaintRow(pop) {
    var W = G.word, row = W.rows[W.row];
    if (!row) return;
    row.classList.add("is-now");
    Array.prototype.forEach.call(row.children, function (t, i) {
      var ch = W.cur.charAt(i);
      t.firstChild.textContent = ch;
      t.classList.toggle("is-filled", !!ch);
      t.classList.toggle("is-next", i === W.cur.length);
      if (pop && i === W.cur.length - 1) { t.classList.remove("is-pop"); void t.offsetWidth; t.classList.add("is-pop"); }
    });
  }
  function wordNudge(msg) {
    var W = G.word, row = W.rows[W.row];
    if (row) { row.classList.remove("is-shake"); void row.offsetWidth; row.classList.add("is-shake"); }
    ui.wordMsg.textContent = msg;
    ui.wordMsg.classList.remove("is-on"); void ui.wordMsg.offsetWidth; ui.wordMsg.classList.add("is-on");
    say(msg);
  }
  function wordType(ch) {
    var W = G && G.word;
    if (!W || G.locked || G.done) return;
    if (W.cur.length >= W.n) { say("That is all " + W.n + " letters. Press Enter to guess."); return; }
    W.cur += ch;
    ui.wordMsg.classList.remove("is-on");
    sfx("pop");
    wordPaintRow(true);
    say(ch);
  }
  function wordDelete() {
    var W = G && G.word;
    if (!W || G.locked || G.done || !W.cur) return;
    var gone = W.cur.slice(-1);
    W.cur = W.cur.slice(0, -1);
    wordPaintRow(false);
    say(gone + " deleted");
  }
  function wordSubmit() {
    var W = G && G.word;
    if (!W || G.locked || G.done) return;
    if (W.cur.length < W.n) { wordNudge("Not enough letters: this word has " + W.n + "."); return; }
    G.locked = true;
    var guess = W.cur, marks = wordMarks(guess, W.answer), row = W.rows[W.row], step = calm() ? 0 : 170;
    var spoken = guess.split("").map(function (ch, i) { return ch + " " + MARK_SAY[marks[i]]; }).join(", ");
    row.classList.remove("is-now");
    row.setAttribute("aria-label", "Guess " + (W.row + 1) + ": " + spoken);
    Array.prototype.forEach.call(row.children, function (t, i) {
      t.classList.remove("is-next");
      var show = function () { t.classList.add(MARK_CLS[marks[i]]); t.lastChild.innerHTML = MARK_ART[marks[i]]; };
      if (!step) { show(); return; }
      setTimeout(function () { t.classList.add("is-flip"); }, i * step);
      setTimeout(show, i * step + 160);
    });
    after(step ? W.n * step + 380 : 0, function () {
      if (G.word !== W) return;
      guess.split("").forEach(function (ch, i) { if (W.best[ch] === undefined || marks[i] > W.best[ch]) W.best[ch] = marks[i]; });
      Array.prototype.forEach.call(ui.keys.querySelectorAll(".st-kb"), function (b) {
        var k = b.getAttribute("data-k"), m = W.best[k];
        if (k.length !== 1 || m === undefined) return;
        b.classList.remove("is-no", "is-near", "is-yes");
        b.classList.add(MARK_CLS[m]);
        b.setAttribute("aria-label", k + ", " + MARK_SAY[m]);
      });
      var solved = marks.every(function (m) { return m === 2; });
      W.row += 1; W.cur = "";
      if (solved) wordEnd(true);
      else if (W.row >= WORD_TRIES) wordEnd(false);
      else {
        G.locked = false;
        wordPaintRow(false);
        sfx("tick");
        say("Guess " + W.row + ": " + spoken + ". " + guesses(WORD_TRIES - W.row) + " left.");
      }
    });
  }
  function wordEnd(solved) {
    var W = G.word, i = G.qi, tries = W.row, last = i === D.words.length - 1;
    G.answers.push(solved);
    G.tries.push(tries);
    var gain = solved ? 100 * (WORD_TRIES + 1 - tries) : 0;
    if (solved) { G.right += 1; G.pts += gain; if (tries === 1) G.firsts += 1; }
    paintDots(wordDots(), -1);
    wordChips(solved);
    var lock = ui.locks.children[i];
    lock.className = "st-lock is-" + (solved ? "open" : "lost") + " is-pop";
    lock.innerHTML = lockArt(solved ? "open" : "lost");
    ui.locks.setAttribute("aria-label", locksLabel());
    ui.keys.hidden = true;
    ui.wordMsg.hidden = true;
    if (solved) W.rows[tries - 1].classList.add("is-win");
    setMood(G.cat, solved ? (tries <= 2 ? "cheer" : "happy") : "oops");
    sfx(solved ? "good" : "bad");
    var head = solved ? (tries === 1 ? "First guess!" : pick(["Unlocked!", "Cracked it!", "Code word found!"])) : "Locked out";
    roundPanel(solved, head, gain, "",
      '<span class="st-fb-ans"><b>' + (solved ? "The code word:" : "The code word was:") + "</b> " + W.answer + "</span>" + D.words[i].c,
      last ? "See my result" : "Next word",
      function () { if (last) wordResults(); else wordRound(i + 1); });
    say((solved ? head + " " + W.answer + ", in " + guesses(tries) + "." : "Out of guesses. The code word was " + W.answer + ".") + " " + stripTags(D.words[i].c));
  }
  function wordResults() {
    var n = D.words.length, used = 0;
    G.tries.forEach(function (t) { used += t; });
    var stars = G.right === n && used <= n + 4 ? 3 : G.right >= n - 1 ? 2 : 1;
    var medals = [];
    if (G.right === n) medals.push(["sweep", "#16A34A", "Tin unlocked", "Every code word found"]);
    if (G.firsts === n) medals.push(["crown", "#D97706", "Word wizard", "Every word at the first guess"]);
    else if (G.firsts) medals.push(["bolt", "#7C3AED", "Mind reader", plural(G.firsts, "word") + " at the first guess"]);
    taskResults({
      stars: stars, pts: G.pts, pct: G.pts / (n * 100 * WORD_TRIES),
      title: stars === 3 ? "Word wizard: the tin is open" : stars === 2 ? "Sharp guessing" : "A good start: play again to open every lock",
      mood: stars === 3 ? "proud" : stars === 2 ? "cheer" : "happy", wear: stars === 3 ? ["crown"] : null,
      rows: [[art("word"), "Code words found", G.right + " of " + n, fmt(G.pts)],
             [lockArt("open", true), "Guesses used", guesses(used) + " in all", ""]],
      medals: medals,
      extra: reviewList("The code words", D.words.map(function (w) { return '<span class="st-res-a">' + w.w + "</span> " + w.c; })),
      summary: G.right + " of " + n + " code words found."
    });
  }

  /* ============================================================== LINK UP */
  /* Twelve tiles hide three groups of four. Pick four tiles and submit them:
     either they are a group, which is banked with its name, or it is a slip.
     Four slips end the round. The last group banks itself. */
  var LINK_SLIPS = 4;
  function linkSize() { return D.link[0].t.length; }
  function linkPicked() { return G.pool.filter(function (t) { return t.on; }); }
  function slips(n) { return n === 0 ? "no slips" : n === 1 ? "1 slip" : n + " slips"; }
  function linkChips(up) {
    ui.groupsN.textContent = G.found.length + " / " + D.link.length;
    ui.groupsChip.setAttribute("aria-label", G.found.length + " of " + D.link.length + " groups found");
    if (up) bump(ui.groupsChip);
  }
  function linkLives(pop) {
    var left = LINK_SLIPS - G.slips;
    ui.lives.innerHTML = "";
    for (var i = 0; i < LINK_SLIPS; i++) {
      ui.lives.appendChild(el("i", { class: i < left ? "" : "is-gone" + (pop && i === left ? " is-pop" : ""), html: HEART }));
    }
    ui.lives.setAttribute("aria-label", left === 1 ? "1 slip left" : left + " slips left");
  }
  function linkSay(text, flash) {
    ui.linkMsg.textContent = text;
    ui.linkMsg.classList.toggle("is-flash", !!flash);
    if (flash) { void ui.linkMsg.offsetWidth; say(text); }
  }
  function linkCount() {
    var n = linkPicked().length, size = linkSize();
    ui.linkGo.disabled = n !== size;
    if (G.over || !G.pool.length) return;
    linkSay(n === 0 ? "Pick " + size + " tiles that belong together." : n === size ? "That is " + size + ". Press Submit." : n + " of " + size + " picked.", false);
  }

  function linkSplash() {
    var n = D.link.length, size = linkSize();
    label("Link Up", plural(n, "group"));
    ui.dots.innerHTML = "";
    var s = screen("st-splash");
    s.appendChild(el("span", { class: "st-splash-tag", text: "Link Up" }));
    s.appendChild(el("div", { class: "st-splash-ico", "aria-hidden": "true", html: art("link") }));
    s.appendChild(el("h2", { tabindex: "-1", text: "Link Up" }));
    var sub = n * size + " tiles hide " + n + " groups of " + size + ". Pick " + size + " tiles that belong together, then press Submit. " +
      "You can slip up " + LINK_SLIPS + " times.";
    s.appendChild(el("p", { text: sub }));
    var go = el("button", { class: "st-go", type: "button", html: ico("i-play") + " Deal the tiles" });
    go.addEventListener("click", linkDeal);
    s.appendChild(go);
    sfx("board");
    say("Link Up. " + sub);
    focusFirst(go);
  }

  function linkDeal() {
    if (!G) return;
    var id = 0, size = linkSize();
    G.pool = [];
    D.link.forEach(function (g, k) {
      g.t.forEach(function (h) { G.pool.push({ id: id++, g: k, html: h, text: stripTags(h), on: false }); });
    });
    G.pool = shuffle(G.pool);
    G.found = []; G.mine = 0; G.slips = 0; G.tried = {}; G.pts = 0; G.t0 = 0; G.tEnd = 0; G.locked = false; G.over = false;
    label("Link Up", "Find the " + D.link.length + " groups");
    var s = screen("st-linkup");
    ui.lives = el("span", { class: "st-link-lives", role: "img" });
    var h = el("h2", { class: "st-link-q", tabindex: "-1", text: "Find " + D.link.length + " groups of " + size });
    s.appendChild(el("div", { class: "st-link-head" }, [h, el("span", { class: "st-link-slips" }, [el("small", { text: "Slips left" }), ui.lives])]));
    ui.bands = el("div", { class: "st-bands" });
    s.appendChild(ui.bands);
    ui.linkGrid = el("div", { class: "st-link-grid", role: "group", "aria-label": "Tiles" });
    ui.linkGrid.addEventListener("keydown", function (e) { gridKeys(e, ui.linkGrid, ".st-lt"); });
    s.appendChild(ui.linkGrid);
    ui.linkMsg = el("p", { class: "st-link-msg" });
    s.appendChild(ui.linkMsg);
    ui.linkGo = el("button", { class: "st-go", type: "button", disabled: true, html: ico("i-check") + " Submit" });
    ui.linkGo.addEventListener("click", linkSubmit);
    var mix = el("button", { class: "st-ghost", type: "button", html: ico("i-repeat") + " Shuffle" });
    mix.addEventListener("click", function () {
      if (!G || G.locked || G.done) return;
      G.pool = shuffle(G.pool);
      linkPaint(true);
      say("The tiles have been shuffled.");
    });
    var clear = el("button", { class: "st-ghost", type: "button", text: "Clear" });
    clear.addEventListener("click", function () {
      if (!G || G.locked || G.done) return;
      G.pool.forEach(function (t) { t.on = false; });
      linkPaint(false);
    });
    ui.linkActions = el("div", { class: "st-actions" }, [mix, clear, ui.linkGo]);
    s.appendChild(ui.linkActions);
    linkPaint(true);
    linkLives(false);
    linkChips(false);
    sfx("board");
    say("The tiles are dealt: " + G.pool.length + " tiles. Pick " + size + " that belong together, then press Submit. Move with Tab or the arrow keys.");
    focusFirst(h);
  }

  /* Draws the tiles still in play. The tile that had the focus keeps it. */
  function linkPaint(deal) {
    var at = document.activeElement && document.activeElement._tile ? document.activeElement._tile.id : -1;
    ui.linkGrid.innerHTML = "";
    ui.linkGrid.setAttribute("data-left", String(G.pool.length));
    G.pool.forEach(function (t, i) {
      var b = el("button", { class: "st-lt" + (t.on ? " is-on" : "") + (deal ? " is-deal" : ""), type: "button", style: "--i:" + i, "aria-pressed": String(t.on) }, [
        el("span", { class: "st-lt-t", html: t.html }),
        el("span", { class: "st-lt-m", "aria-hidden": "true", html: ico("i-check") })]);
      b._tile = t;
      t.el = b;
      b.addEventListener("click", function () { linkTap(t); });
      ui.linkGrid.appendChild(b);
      if (t.id === at) b.focus();
    });
    fitSoon();
    linkCount();
  }
  function linkTap(t) {
    if (!G || G.locked || G.done) return;
    var size = linkSize();
    if (!t.on && linkPicked().length >= size) { linkSay("You have " + size + " already. Press Submit, or tap a tile to drop it.", true); return; }
    startWatch();
    t.on = !t.on;
    t.el.classList.toggle("is-on", t.on);
    t.el.setAttribute("aria-pressed", String(t.on));
    sfx("pop");
    linkCount();
  }
  function linkShake(tiles) {
    tiles.forEach(function (t) { t.el.classList.remove("is-no"); void t.el.offsetWidth; t.el.classList.add("is-no"); });
  }
  function linkSubmit() {
    if (!G || G.locked || G.done) return;
    var picked = linkPicked(), size = linkSize();
    if (picked.length !== size) return;
    startWatch();
    var count = {}, best = 0;
    picked.forEach(function (t) { count[t.g] = (count[t.g] || 0) + 1; best = Math.max(best, count[t.g]); });
    if (best === size) { linkBank(picked[0].g, true); return; }
    var key = picked.map(function (t) { return t.id; }).sort(function (a, b) { return a - b; }).join(",");
    linkShake(picked);
    if (G.tried[key]) { linkSay("You have already tried those " + size + ". Change at least one tile.", true); return; }
    G.tried[key] = true;
    G.slips += 1;
    linkLives(true);
    sfx("bad");
    var left = LINK_SLIPS - G.slips;
    if (left <= 0) { linkSay("Out of slips. Here are the groups.", true); linkOver(); return; }
    linkSay((best === size - 1 ? "One away! " : "Not a group. ") + (left === 1 ? "1 slip left." : left + " slips left."), true);
  }
  function linkBand(g, order, cls) {
    var grp = D.link[g];
    return el("div", { class: "st-band st-band-" + (order % 4) + (cls ? " " + cls : "") }, [
      el("b", { html: grp.n }), el("span", { html: grp.t.join(", ") })]);
  }
  /* A whole group leaves the grid and becomes a named band above it. `mine`
     is false when the round is over and the group is only being shown. */
  function linkBank(g, mine) {
    G.locked = true;
    var tiles = G.pool.filter(function (t) { return t.g === g; });
    if (mine) { G.mine += 1; G.pts += 300; sfx("good"); }
    tiles.forEach(function (t, k) { t.el.disabled = true; t.el.style.setProperty("--k", k); t.el.classList.add(mine ? "is-win" : "is-shown"); });
    after(calm() ? 0 : 720, function () {
      var order = G.found.length;
      G.pool = G.pool.filter(function (t) { return t.g !== g; });
      G.found.push(g);
      ui.bands.appendChild(linkBand(g, order, mine ? "" : "is-missed"));
      linkPaint(false);
      linkChips(mine);
      var name = stripTags(D.link[g].n), list = D.link[g].t.map(stripTags).join(", ");
      var left = D.link.length - G.found.length;
      if (!mine) {
        say("A group you did not find: " + name + ": " + list + ".");
        if (left > 0) after(calm() ? 200 : 700, function () { linkBank(G.pool[0].g, false); }); else linkEnd();
        return;
      }
      if (left === 1) {
        say("Group found: " + name + ": " + list + ". That leaves the last group.");
        linkSay("That leaves the last group.", false);
        after(calm() ? 200 : 900, function () { linkBank(G.pool[0].g, true); });
      } else if (left === 0) {
        say("Group found: " + name + ": " + list + ". Every group found.");
        linkEnd();
      } else {
        G.locked = false;
        say("Group found: " + name + ": " + list + ". " + plural(left, "group") + " to go.");
        if (!stage.contains(document.activeElement) || document.activeElement === document.body) focusFirst(G.pool[0].el);
      }
    });
  }
  function linkStop() {
    G.tEnd = performance.now();
    clearInterval(G.tick); G.tick = 0;
    if (ui.timeN) ui.timeN.textContent = mmss(watch());
  }
  function linkOver() {
    G.locked = true; G.over = true;
    linkStop();
    ui.linkActions.hidden = true;
    after(calm() ? 200 : 900, function () { linkBank(G.pool[0].g, false); });
  }
  function linkEnd() {
    if (!G.tEnd) linkStop();
    ui.linkActions.hidden = true;
    ui.linkGrid.hidden = true;
    linkSay(G.over ? "Out of slips: these are the groups." : "Every group found!", false);
    after(calm() ? 500 : 1500, linkResults);
  }
  function linkResults() {
    if (!G || G.done) return;
    var n = D.link.length, done = !G.over, secs = Math.floor(watch() / 1000);
    var found = done ? n : G.mine;
    var keep = done ? 100 * (LINK_SLIPS - G.slips) : 0;
    var bonus = done && opts.timer ? Math.max(0, 300 - 4 * secs) : 0;
    var base = G.pts;
    G.pts += keep + bonus;
    var stars = done ? (G.slips <= 1 ? 3 : 2) : 1;
    var medals = [];
    if (done && G.slips === 0) medals.push(["sweep", "#16A34A", "No slips", "Every group at the first try"]);
    if (done && opts.timer && secs <= 45) medals.push(["bolt", "#7C3AED", "Quick links", "Done in " + mmss(secs * 1000)]);
    var rows = [[art("link"), "Groups found", found + " of " + n + ", with " + slips(G.slips), fmt(base)]];
    if (done) rows.push([HEART, "Slips left", (LINK_SLIPS - G.slips) + " of " + LINK_SLIPS, "+" + fmt(keep)]);
    if (done && opts.timer) rows.push([ico("i-timer"), "Time", mmss(secs * 1000) + (bonus ? ", with a time bonus" : ""), "+" + fmt(bonus)]);
    taskResults({
      stars: stars, pts: G.pts, pct: done ? 1 - G.slips / (2 * LINK_SLIPS) : 0.5 * G.mine / n,
      title: stars === 3 ? "Link master" : stars === 2 ? "Well linked" : "Out of slips: play again to find every group",
      mood: stars === 3 ? "proud" : stars === 2 ? "cheer" : "happy", wear: stars === 3 ? ["crown"] : null,
      rows: rows, medals: medals,
      extra: reviewList("The groups", D.link.map(function (g) { return '<span class="st-res-a">' + g.n + "</span> " + g.t.join(", "); })),
      summary: found + " of " + n + " groups found, with " + slips(G.slips) + "."
    });
  }

  /* ============================================================= BUG HUNT */
  /* Each round shows three statements: two are true and one has a mistake in
     it, the bug. The student catches the bug by choosing that statement. With
     the timer on, a bug crawls toward the way out, and the round is lost if it
     gets there first. */
  var BUG_MS = 40000;
  var BUG_RIGHT = ["Caught it!", "Bug squashed!", "Got it!", "Nice catch!"];
  var BUG_WRONG = ["Not that one", "That one is true", "The bug got away"];
  function bugDots() { return D.bugs.map(function (q, i) { return i < G.answers.length ? (G.answers[i] ? 1 : 0) : -1; }); }
  function bugChips(up) {
    ui.caughtN.textContent = G.right + " / " + D.bugs.length;
    ui.caughtChip.setAttribute("aria-label", G.right + " of " + D.bugs.length + " bugs caught");
    if (up) bump(ui.caughtChip);
    ui.streak.hidden = G.streak < 2;
    ui.streakN.textContent = String(G.streak);
    ui.streak.classList.toggle("is-hot", G.streak >= 3);
    ui.streak.setAttribute("aria-label", "Catching streak " + G.streak);
  }
  function bugSplash() {
    var n = D.bugs.length;
    label("Bug Hunt", plural(n, "round"));
    ui.dots.innerHTML = "";
    var s = screen("st-splash st-bug-splash");
    s.appendChild(el("span", { class: "st-splash-tag", text: "Bug Hunt" }));
    s.appendChild(el("div", { class: "st-splash-ico", "aria-hidden": "true", html: art("bug") }));
    s.appendChild(el("h2", { tabindex: "-1", text: "Bug Hunt" }));
    var sub = "A bug is a mistake. In each of the " + plural(n, "round") + ", two statements are true and one has a bug. Pick the one with the bug to catch it." +
      (opts.timer ? " Be quick: the bug is crawling to the way out." : "");
    s.appendChild(el("p", { text: sub }));
    var go = el("button", { class: "st-go", type: "button", html: ico("i-play") + " Start the hunt" });
    go.addEventListener("click", function () { bugRound(0); });
    s.appendChild(go);
    sfx("board");
    say("Bug Hunt. " + sub);
    focusFirst(go);
  }
  /* The round's clock is a bug crawling along a lane. In calm mode it stays
     still and only the seconds count down. */
  function bugClock(limit, onEnd) {
    var t0 = performance.now(), raf = 0, stopped = false, lastWhole = -1, track = ui.bugTrack, secs = ui.bugSecs;
    var api = {
      elapsed: function () { return performance.now() - t0; },
      stop: function () { stopped = true; cancelAnimationFrame(raf); }
    };
    if (!opts.timer) { secs.textContent = "No clock"; return api; }
    (function frame(now) {
      if (stopped) return;
      var left = Math.max(0, limit - (now - t0));
      if (!calm()) track.style.setProperty("--p", (1 - left / limit).toFixed(4));
      var whole = Math.ceil(left / 1000);
      if (whole !== lastWhole) {
        lastWhole = whole;
        secs.textContent = whole + "s";
        track.classList.toggle("is-low", left <= 10000);
        if (left <= 5000 && left > 0) sfx("tick");
        if (whole === 10) say("10 seconds left");
      }
      if (left <= 0) { stopped = true; onEnd(); return; }
      raf = requestAnimationFrame(frame);
    })(t0);
    return api;
  }
  function bugRound(i) {
    if (!G) return;
    G.qi = i; G.locked = false;
    var q = D.bugs[i];
    label("Bug Hunt", "Round " + (i + 1) + " of " + D.bugs.length);
    paintDots(bugDots(), i);
    bugChips(false);
    var s = screen("st-bug");
    G.cat = pixel("think");
    var h = el("h2", { class: "st-bug-q", tabindex: "-1", text: "Two are true. Which one has the bug?" });
    s.appendChild(el("div", { class: "st-bug-head" }, [
      G.cat ? el("div", { class: "st-bug-host", "aria-hidden": "true" }, [G.cat]) : null,
      el("div", { class: "st-bug-ask" }, [el("p", { class: "st-bug-round", text: "Round " + (i + 1) + " of " + D.bugs.length }), h])]));
    ui.bugSecs = el("span", { class: "st-bug-secs" });
    ui.bugTrack = el("div", { class: "st-bug-track" + (opts.timer ? "" : " is-off"), role: "timer",
                              "aria-label": opts.timer ? (BUG_MS / 1000) + " seconds to catch the bug" : "No clock" }, [
      el("span", { class: "st-bug-lane", "aria-hidden": "true" }, [
        el("span", { class: "st-bug-crawler", html: art("bug") }), el("span", { class: "st-bug-exit" })]),
      ui.bugSecs]);
    s.appendChild(ui.bugTrack);
    var three = shuffle(q.t.map(function (t) { return { h: t, bug: false }; }).concat([{ h: q.b, bug: true }]));
    var list = el("div", { class: "st-bug-list" });
    var cards = [];
    three.forEach(function (o, k) {
      var b = el("button", { class: "st-bug-card", type: "button", style: "--i:" + k, "aria-label": "Statement " + (k + 1) + ": " + stripTags(o.h) }, [
        el("span", { class: "st-bug-k", "aria-hidden": "true", text: String(k + 1) }),
        el("span", { class: "st-bug-t", html: o.h }),
        el("span", { class: "st-bug-tag", "aria-hidden": "true" }),
        el("span", { class: "st-mark", "aria-hidden": "true" })]);
      b._bug = o.bug;
      b._text = stripTags(o.h);
      b.addEventListener("click", function () { bugAnswer(b); });
      cards.push(b);
      list.appendChild(b);
    });
    ui.tiles = cards;
    s.appendChild(list);
    fitSoon();
    ui.fb = el("div", { class: "st-fbslot" });
    s.appendChild(ui.fb);
    say("Round " + (i + 1) + " of " + D.bugs.length + ". Three statements: two are true and one has a bug. Choose the one with the bug, or press 1, 2 or 3.");
    focusFirst(h);
    T = bugClock(BUG_MS, function () { bugAnswer(null); });
  }
  function bugAnswer(btn) {
    if (!G || G.locked || G.done) return;
    G.locked = true;
    var q = D.bugs[G.qi], late = !btn, ok = !!btn && btn._bug;
    var ms = T ? T.elapsed() : 0;
    stopClock();
    ui.tiles.forEach(function (t, k) {
      t.disabled = true;
      var tag = t.querySelector(".st-bug-tag");
      if (t._bug) {
        t.classList.add("is-bug");
        tag.textContent = "Bug";
        if (ok) markTile(t, true);
      } else {
        t.classList.add("is-true");
        tag.textContent = "True";
        if (t === btn) markTile(t, false);
      }
      t.setAttribute("aria-label", "Statement " + (k + 1) + ": " + t._text + " " + (t._bug ? "This one has the bug." : "True."));
    });
    G.answers.push(ok);
    var gain = 0;
    if (ok) {
      G.right += 1; G.streak += 1;
      G.bestStreak = Math.max(G.bestStreak, G.streak);
      gain = 100 + 25 * Math.min(G.streak - 1, 5) + (opts.timer ? Math.round(50 * Math.max(0, 1 - ms / BUG_MS)) : 0);
      G.pts += gain;
    } else G.streak = 0;
    ui.bugTrack.classList.add(ok ? "is-caught" : "is-escaped");
    setMood(G.cat, ok ? (G.streak >= 3 ? "cheer" : "happy") : "oops");
    paintDots(bugDots(), -1);
    bugChips(ok);
    sfx(ok ? "good" : "bad");
    var last = G.qi === D.bugs.length - 1;
    var head = ok ? pick(BUG_RIGHT) : late ? "Too slow: it got away!" : pick(BUG_WRONG);
    roundPanel(ok, head, gain, ok && G.streak >= 3 ? G.streak + " bugs in a row!" : "",
      (ok ? "" : '<span class="st-fb-ans"><b>The bug:</b> ' + q.b + "</span>") + "<b>The fix:</b> " + q.x,
      last ? "See my result" : "Next round",
      function () { if (last) bugResults(); else bugRound(G.qi + 1); });
    say((ok ? "Caught it! " : late ? "Time is up. The bug was: " + stripTags(q.b) + " " : "Not that one: it is true. The bug was: " + stripTags(q.b) + " ") +
        "The fix: " + stripTags(q.x));
  }
  function bugResults() {
    var n = D.bugs.length, pct = G.right / n;
    var stars = G.right === n ? 3 : pct >= 0.75 ? 2 : 1;
    var medals = [];
    if (G.right === n) medals.push(["sweep", "#16A34A", "Bug free", "Every bug caught"]);
    if (G.bestStreak >= 4) medals.push(["fire", "#EA580C", "Hot streak", plural(G.bestStreak, "bug") + " in a row"]);
    var missed = [];
    D.bugs.forEach(function (q, i) { if (!G.answers[i]) missed.push(q.b + ' <span class="st-res-ans">' + q.x + "</span>"); });
    taskResults({
      stars: stars, pts: G.pts, pct: pct,
      title: stars === 3 ? "Bug free: every bug caught" : stars === 2 ? "Sharp eyes" : "A good start: play again to catch them all",
      mood: stars === 3 ? "proud" : stars === 2 ? "cheer" : "happy", wear: stars === 3 ? ["crown"] : null,
      rows: [[art("bug"), "Bugs caught", G.right + " of " + n, fmt(G.pts)],
             [FLAME, "Best streak", plural(G.bestStreak, "bug") + " in a row", ""]],
      medals: medals,
      extra: missed.length ? reviewList("The bugs that got away", missed) : null,
      summary: G.right + " of " + n + " bugs caught."
    });
  }

  /* ========================================================== BRAIN GAMES */
  /* Three quick games that replay the lesson as brain training. Odd One Out
     (logic) mixes three tiles of one Link Up group with one tile of another;
     the build has checked every mix it may make. Memory Flash (memory) shows
     the Memory Match words, turns them over, then asks for the word that goes
     with each meaning. Fact or Fib (speed) deals Bug Hunt's statements and the
     quiz's true or false questions one at a time. Right answers throw
     diamonds into the points chip, and a streak multiplies the points. */
  var BULB = '<svg viewBox="0 0 20 24" aria-hidden="true" focusable="false"><path d="M10 1.8a7 7 0 0 0-4 12.8c.9.7 1.4 1.5 1.4 2.5v1h5.2v-1c0-1 .5-1.8 1.4-2.5A7 7 0 0 0 10 1.8Z" fill="#FDE047" stroke="currentColor" stroke-width="1.6"/>' +
    '<path d="M7.6 21h4.8M8.4 23h3.2" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>';
  var LINKED = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M10 14a4.5 4.5 0 0 0 6.4 0l3.2-3.2a4.5 4.5 0 0 0-6.4-6.4L11.6 6" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/>' +
    '<path d="M14 10a4.5 4.5 0 0 0-6.4 0l-3.2 3.2a4.5 4.5 0 0 0 6.4 6.4l1.6-1.6" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/></svg>';
  var BOLT = '<svg viewBox="0 0 80 56" aria-hidden="true" focusable="false"><rect x="5" y="5" width="70" height="46" rx="8" fill="none" stroke="#fff" stroke-opacity=".45" stroke-width="2" stroke-dasharray="4 3"/>' +
    '<circle cx="40" cy="28" r="15" fill="#fff" fill-opacity=".16"/><path d="M43.5 13.5 32 30h8l-3.6 13 12-17.5h-8Z" fill="#FDE047" stroke="#0B3B4A" stroke-width="2" stroke-linejoin="round"/>' +
    '<circle cx="15" cy="16" r="2.4" fill="#A5F3FC"/><circle cx="66" cy="41" r="2.4" fill="#A5F3FC"/><path d="M63 13l2.5 2.5M17 41l-2.5 2.5" stroke="#A5F3FC" stroke-width="2.2" stroke-linecap="round"/></svg>';
  var CROSS = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M6 6l12 12M18 6 6 18" stroke="currentColor" stroke-width="3.2" stroke-linecap="round"/></svg>';
  var TICK = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M4.5 12.5l5 5 10-11" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></svg>';

  /* The multiplier a streak earns: three in a row doubles the points, six trebles them. */
  function multi() { return G.streak >= 6 ? 3 : G.streak >= 3 ? 2 : 1; }
  /* The chips. Points count up when the diamonds land, not before. */
  function brainChips(landed) {
    if (landed) {
      countUp(ui.ptsN, G.shown, G.pts, calm() ? 0 : 500);
      G.shown = G.pts;
      bump(ui.ptsChip);
    } else ui.ptsN.textContent = fmt(G.shown);
    ui.ptsChip.setAttribute("aria-label", fmt(G.pts) + " points");
    var m = multi();
    ui.streak.hidden = G.streak < 2;
    ui.streakN.textContent = String(G.streak);
    ui.streak.classList.toggle("is-hot", G.streak >= 3);
    ui.multi.hidden = m < 2;
    ui.multi.textContent = "x" + m;
    ui.streak.setAttribute("aria-label", "Streak " + G.streak + (m > 1 ? ", points times " + m : ""));
  }
  /* Diamonds burst out of a tile and fly into the points chip. */
  function gemFly(from, n, done) {
    var to = ui.ptsChip;
    if (!from || !to || calm() || !from.getBoundingClientRect || !Element.prototype.animate) { done(); return; }
    var a = from.getBoundingClientRect(), b = to.getBoundingClientRect();
    var x0 = a.left + a.width / 2, y0 = a.top + a.height / 2, x1 = b.left + 20, y1 = b.top + b.height / 2;
    var landed = false, game = G;
    for (var i = 0; i < n; i++) {
      (function (i) {
        var g = el("span", { class: "st-gem-fly", "aria-hidden": "true", html: GEM });
        g.style.left = x0 + "px";
        g.style.top = y0 + "px";
        stage.appendChild(g);
        var ang = (Math.PI * 2 * i) / n + Math.random() * 0.7, r = 46 + Math.random() * 54;
        var bx = Math.cos(ang) * r, by = Math.sin(ang) * r - 26, spin = (Math.random() < 0.5 ? -1 : 1) * (180 + Math.random() * 260);
        var anim = g.animate([
          { transform: "translate(0px, 0px) scale(.2) rotate(0deg)", opacity: 0 },
          { transform: "translate(" + bx + "px, " + by + "px) scale(1.2) rotate(" + (spin / 3) + "deg)", opacity: 1, offset: 0.32 },
          { transform: "translate(" + (bx * 0.6) + "px, " + (by * 0.6 - 10) + "px) scale(1) rotate(" + (spin / 2) + "deg)", opacity: 1, offset: 0.48 },
          { transform: "translate(" + (x1 - x0) + "px, " + (y1 - y0) + "px) scale(.45) rotate(" + spin + "deg)", opacity: 0.85 }
        ], { duration: 760 + i * 70, easing: "cubic-bezier(.35, .05, .35, 1)", fill: "forwards" });
        anim.onfinish = function () {
          if (g.parentNode) g.parentNode.removeChild(g);
          if (!landed && G === game) { landed = true; done(); }
        };
      })(i);
    }
  }
  function floatText(node, text, cls) {
    if (!node || calm()) return;
    var r = node.getBoundingClientRect();
    var p = el("span", { class: "st-float" + (cls ? " " + cls : ""), "aria-hidden": "true", text: text });
    p.style.left = (r.left + r.width / 2) + "px";
    p.style.top = (r.top + Math.min(40, r.height / 3)) + "px";
    stage.appendChild(p);
    setTimeout(function () { if (p.parentNode) p.parentNode.removeChild(p); }, 1300);
  }
  function quake() {
    if (calm()) return;
    ui.screen.classList.remove("is-quake");
    void ui.screen.offsetWidth;
    ui.screen.classList.add("is-quake");
  }
  /* A right answer: the points, the diamonds and the chips. */
  function brainWin(from, gain, gems) {
    G.pts += gain;
    floatText(from, "+" + fmt(gain), multi() > 1 ? "is-multi" : "");
    gemFly(from, gems, function () { brainChips(true); sfx("gem"); });
    brainChips(false);
  }
  function endStop(t) { return /[.?!]$/.test(stripTags(t)) ? "" : "."; }

  /* The splash every brain game opens with, then a three, two, one. */
  function brainSplash(task, sub, onGo) {
    label(TASK_NAMES[task], "Brain game: " + BRAIN[task]);
    ui.dots.innerHTML = "";
    ui.progChip.hidden = true;
    brainChips(false);
    var s = screen("st-splash st-brain-splash");
    s.appendChild(el("span", { class: "st-splash-tag st-brain-badge", text: "Brain game: " + BRAIN[task] }));
    s.appendChild(el("div", { class: "st-splash-ico", "aria-hidden": "true", html: art(task) }));
    s.appendChild(el("h2", { tabindex: "-1", text: TASK_NAMES[task] }));
    s.appendChild(el("p", { text: sub }));
    s.appendChild(el("p", { class: "st-brain-prize", html: '<span class="st-brain-prize-g" aria-hidden="true">' + GEM + GEM + GEM + "</span>Win up to three diamonds" }));
    var go = el("button", { class: "st-go", type: "button", html: ico("i-play") + " Start" });
    go.addEventListener("click", function () { brainCount(s, go, onGo); });
    s.appendChild(go);
    sfx("board");
    say(TASK_NAMES[task] + ", a brain game for " + BRAIN[task].toLowerCase() + ". " + sub);
    focusFirst(go);
  }
  function brainCount(s, go, then) {
    go.remove();
    if (calm()) { then(); return; }
    var c = el("div", { class: "st-count st-brain-count", "aria-hidden": "true" });
    s.appendChild(c);
    var n = 3, game = G;
    (function tick() {
      if (G !== game) return;
      if (n === 0) { sfx("go"); then(); return; }
      c.textContent = String(n);
      c.classList.remove("is-pop"); void c.offsetWidth; c.classList.add("is-pop");
      sfx("count");
      n -= 1;
      setTimeout(tick, 700);
    })();
  }
  /* The fuse: a bar that burns down while a round is on. */
  function fuseBar(limit, what) {
    ui.fuseSecs = el("span", { class: "st-fuse-secs" });
    ui.fuse = el("div", { class: "st-fuse" + (opts.timer ? "" : " is-off"), role: "timer",
                          "aria-label": opts.timer ? Math.round(limit / 1000) + " seconds " + what : "No clock" }, [
      el("span", { class: "st-fuse-track", "aria-hidden": "true" }, [el("span", { class: "st-fuse-fill" }, [el("i", { class: "st-fuse-spark" })])]),
      ui.fuseSecs]);
    return ui.fuse;
  }
  function fuseClock(limit, onEnd) {
    var t0 = performance.now(), raf = 0, stopped = false, lastWhole = -1, fuse = ui.fuse, secs = ui.fuseSecs;
    var api = {
      elapsed: function () { return performance.now() - t0; },
      stop: function () { stopped = true; cancelAnimationFrame(raf); }
    };
    if (!opts.timer) { secs.textContent = "No clock"; return api; }
    (function frame(now) {
      if (stopped) return;
      var left = Math.max(0, limit - (now - t0)), whole = Math.ceil(left / 1000);
      if (!calm() || whole !== lastWhole) fuse.style.setProperty("--p", (left / limit).toFixed(4));
      if (whole !== lastWhole) {
        lastWhole = whole;
        secs.textContent = whole + "s";
        fuse.classList.toggle("is-low", left <= 5000);
        if (left <= 5000 && left > 0) sfx("tick");
        if (whole === 5) say("5 seconds left");
      }
      if (left <= 0) { stopped = true; onEnd(); return; }
      raf = requestAnimationFrame(frame);
    })(t0);
    return api;
  }
  function brainResults(o) {
    o.rows.push([FLAME, "Best streak", plural(G.bestStreak, "right answer") + " in a row", ""]);
    ui.progChip.hidden = true;
    ui.streak.hidden = true;
    taskResults(o);
  }

  /* ========================================================= ODD ONE OUT */
  var ODD_N = 8, ODD_MS = 25000;
  var ODD_RIGHT = ["Spotted it!", "Sharp thinking!", "Odd one found!", "Big brain move!", "Nailed it!"];
  var ODD_WRONG = ["Not that one", "That one belongs", "So close"];
  /* Eight rounds: the groups take turns to supply the three, and each odd one
     out comes from the mixes the build allows, new ones first. */
  function oddDeal() {
    var usable = [];
    D.odd.forEach(function (ok, b) { if (ok.length) usable.push(b); });
    var order = [];
    while (order.length < ODD_N) order = order.concat(shuffle(usable));
    order = order.slice(0, ODD_N);
    for (var i = 1; i < order.length; i++) {
      if (order[i] !== order[i - 1]) continue;
      for (var j = i + 1; j < order.length; j++) if (order[j] !== order[i - 1]) { var t = order[i]; order[i] = order[j]; order[j] = t; break; }
    }
    var used = {}, seen = {}, out = [];
    order.forEach(function (b) {
      var n = D.link[b].t.length, pickd = null;
      for (var k = 0; k < 40 && !pickd; k++) {
        var trio = shuffle(D.link[b].t.map(function (x, i) { return i; })).slice(0, 3);
        var fresh = D.odd[b].filter(function (x) { return !used[x[0] + "," + x[1]]; });
        var x = pick(fresh.length ? fresh : D.odd[b]);
        var key = b + "|" + trio.slice().sort().join("") + "|" + x[0] + "," + x[1];
        if (seen[key] && k < 39) continue;
        pickd = { trio: trio, x: x, key: key };
      }
      seen[pickd.key] = 1;
      used[pickd.x[0] + "," + pickd.x[1]] = 1;
      var tiles = pickd.trio.map(function (i) { return { h: D.link[b].t[i], odd: false }; });
      tiles.push({ h: D.link[pickd.x[0]].t[pickd.x[1]], odd: true });
      out.push({ b: b, g: pickd.x[0], tiles: shuffle(tiles), n: n });
    });
    return out;
  }
  function oddSplash() {
    brainSplash("odd", "Four tiles, and three of them share a link. Tap the odd one out. " + ODD_N + " rounds" +
      (opts.timer ? ", each against a burning fuse." : ".") + " Stuck? A hint shows the link, for half the points.",
      function () { G.rounds = oddDeal(); oddRound(0); });
  }
  function oddDots() { return G.rounds.map(function (q, i) { return i < G.answers.length ? (G.answers[i] ? 1 : 0) : -1; }); }
  function oddRound(i) {
    if (!G) return;
    G.qi = i; G.locked = false; G.hinted = false;
    var q = G.rounds[i], n = G.rounds.length;
    label("Odd One Out", "Round " + (i + 1) + " of " + n);
    ui.progN.textContent = (i + 1) + " / " + n;
    ui.progChip.hidden = false;
    paintDots(oddDots(), i);
    brainChips(false);
    var s = screen("st-odd");
    var h = el("h2", { class: "st-brain-q", tabindex: "-1", text: "Three belong together. Which is the odd one out?" });
    s.appendChild(el("div", { class: "st-brain-ask" }, [el("p", { class: "st-brain-round", text: "Round " + (i + 1) + " of " + n }), h]));
    s.appendChild(fuseBar(ODD_MS, "to spot the odd one out"));
    ui.link = el("p", { class: "st-odd-link", hidden: true });
    s.appendChild(ui.link);
    var grid = el("div", { class: "st-odd-grid", role: "group", "aria-label": "Four tiles" });
    ui.tiles = [];
    q.tiles.forEach(function (o, k) {
      var b = el("button", { class: "st-odd-tile", type: "button", style: "--i:" + k, "aria-label": "Tile " + (k + 1) + ": " + stripTags(o.h) }, [
        el("span", { class: "st-odd-k", "aria-hidden": "true", text: String(k + 1) }),
        el("span", { class: "st-odd-t", html: o.h }),
        el("span", { class: "st-odd-tag", "aria-hidden": "true" }),
        el("span", { class: "st-mark", "aria-hidden": "true" })]);
      b._odd = o.odd;
      b._text = stripTags(o.h);
      b.addEventListener("click", function () { oddAnswer(b); });
      ui.tiles.push(b);
      grid.appendChild(b);
    });
    grid.addEventListener("keydown", function (e) { gridKeys(e, grid, ".st-odd-tile"); });
    s.appendChild(grid);
    ui.hint = el("button", { class: "st-ghost st-hint", type: "button", html: BULB + " Show the link <small>half points</small>" });
    ui.hint.addEventListener("click", oddHint);
    s.appendChild(el("div", { class: "st-brain-tools" }, [ui.hint]));
    ui.fb = el("div", { class: "st-fbslot" });
    s.appendChild(ui.fb);
    fitSoon();
    say("Round " + (i + 1) + " of " + n + ". Three tiles belong together and one does not: " +
        ui.tiles.map(function (t, k) { return (k + 1) + ", " + t._text; }).join("; ") + ". Choose the odd one out, or press its number.");
    focusFirst(h);
    T = fuseClock(ODD_MS, function () { oddAnswer(null); });
  }
  function oddHint() {
    if (!G || G.locked || G.hinted || G.done) return;
    G.hinted = true; G.hints += 1;
    ui.hint.disabled = true;
    var q = G.rounds[G.qi];
    ui.link.hidden = false;
    ui.link.className = "st-odd-link is-hint";
    ui.link.innerHTML = BULB + '<span>Three of them: <b>' + D.link[q.b].n + "</b></span>";
    sfx("pop");
    say("Hint: three of them are " + stripTags(D.link[q.b].n) + ".");
  }
  function oddAnswer(btn) {
    if (!G || G.locked || G.done) return;
    G.locked = true;
    var q = G.rounds[G.qi], ok = !!btn && btn._odd, late = !btn;
    var ms = T ? T.elapsed() : 0;
    stopClock();
    var oddEl = null;
    ui.tiles.forEach(function (t, k) {
      t.disabled = true;
      if (t._odd) {
        oddEl = t;
        t.classList.add("is-odd");
        t.querySelector(".st-odd-tag").textContent = "Odd one out";
      } else t.classList.add("is-link");
      t.setAttribute("aria-label", "Tile " + (k + 1) + ": " + t._text + (t._odd ? ". The odd one out." : "."));
    });
    if (btn) markTile(btn, ok);
    if (ui.hint) ui.hint.disabled = true;
    ui.link.hidden = false;
    ui.link.className = "st-odd-link is-shown";
    ui.link.innerHTML = LINKED + '<span>What links the three: <b>' + D.link[q.b].n + "</b></span>";
    G.answers.push(ok);
    var gain = 0;
    if (ok) {
      G.right += 1; G.streak += 1;
      G.bestStreak = Math.max(G.bestStreak, G.streak);
      var quick = opts.timer && !G.hinted && ms <= ODD_MS / 3;
      if (quick) G.fast += 1;
      gain = ((G.hinted ? 50 : 100) + (opts.timer && !G.hinted ? Math.round(50 * Math.max(0, 1 - ms / ODD_MS)) : 0)) * multi();
      brainWin(oddEl, gain, G.hinted ? 3 : quick ? 8 : 6);
    } else {
      G.streak = 0;
      quake();
      brainChips(false);
    }
    paintDots(oddDots(), -1);
    sfx(ok ? "good" : "bad");
    var last = G.qi === G.rounds.length - 1;
    var odd = oddEl.querySelector(".st-odd-t").innerHTML, A = D.link[q.b].n, B = D.link[q.g].n;
    var head = ok ? pick(ODD_RIGHT) : late ? "Out of time!" : pick(ODD_WRONG);
    roundPanel(ok, head, gain, ok && G.streak >= 3 ? G.streak + " in a row! Points x" + multi() + "." : "",
      '<span class="st-fb-ans"><b>What links the other three:</b> ' + A + "</span><b>" + odd + "</b> goes with a different group: " + B + endStop(B),
      last ? "See my result" : "Next round",
      function () { if (last) oddResults(); else oddRound(G.qi + 1); });
    say((ok ? "Right! " : late ? "Time is up. " : "Not that one. ") + stripTags(odd) + " is the odd one out. The other three: " +
        stripTags(A) + ". " + stripTags(odd) + " goes with: " + stripTags(B) + ".");
  }
  function oddResults() {
    var n = G.rounds.length, pct = G.right / n;
    var stars = G.right === n && G.hints <= 1 ? 3 : G.right >= n - 2 ? 2 : 1;
    var medals = [];
    if (G.right === n && !G.hints) medals.push(["sweep", "#16A34A", "Logic legend", "Every odd one out, no hints"]);
    if (G.bestStreak >= 5) medals.push(["fire", "#EA580C", "Hot streak", plural(G.bestStreak, "round") + " in a row"]);
    if (G.fast >= 4) medals.push(["bolt", "#7C3AED", "Quick thinker", plural(G.fast, "fast answer")]);
    var missed = [];
    G.rounds.forEach(function (q, i) {
      if (G.answers[i]) return;
      var t = q.tiles.filter(function (x) { return x.odd; })[0];
      missed.push(t.h + ' <span class="st-res-ans">goes with ' + D.link[q.g].n + ", not " + D.link[q.b].n + "</span>");
    });
    brainResults({
      stars: stars, pts: G.pts, pct: pct,
      title: stars === 3 ? "Logic legend" : stars === 2 ? "Sharp thinking" : "A good start: play again to spot them all",
      mood: stars === 3 ? "proud" : stars === 2 ? "cheer" : "happy", wear: stars === 3 ? ["crown"] : null,
      rows: [[art("odd"), "Odd ones out found", G.right + " of " + n + (G.hints ? ", " + plural(G.hints, "hint") : ""), fmt(G.pts)]],
      medals: medals,
      extra: missed.length ? reviewList("The odd ones that got past you", missed) : null,
      summary: G.right + " of " + n + " odd ones out found."
    });
  }

  /* ======================================================== MEMORY FLASH */
  var FLASH_LEVELS = D.flash ? D.flash.l : [3, 4, 6];
  function flashStudy(n) { return 3000 + n * 1200; }
  function flashTotal() { return FLASH_LEVELS.reduce(function (a, b) { return a + b; }, 0); }
  function flashSplash() {
    brainSplash("flash", "Study the " + pn(0) + " cards. When they flip over, find the card that goes with each clue, from memory. " +
      "Three levels: " + FLASH_LEVELS.join(", then ") + " cards. " +
      (opts.timer ? "The cards turn over when the fuse burns out." : "Take as long as you need to study them."),
      function () { flashLevel(0); });
  }
  function flashDots(now) {
    var list = [];
    for (var i = 0; i < flashTotal(); i++) list.push(i < G.answers.length ? (G.answers[i] ? 1 : 0) : -1);
    paintDots(list, now);
  }
  function fcardLabel(c) {
    var n = "Card " + (c.i + 1);
    if (c.done) return n + ": " + c.text + ", found";
    return c.up ? n + ": " + c.text : n + ", face down";
  }
  function fcardUp(c, up) {
    c.up = up;
    c.el.classList.toggle("is-up", up);
    c.el.setAttribute("aria-label", fcardLabel(c));
  }
  function flashLevel(L) {
    if (!G) return;
    G.level = L; G.locked = true; G.phase = "study";
    var n = FLASH_LEVELS[L], ms = flashStudy(n);
    var FP = D.flash.p, ks = shuffle(FP.map(function (p, k) { return k; })).slice(0, n);
    label("Memory Flash", "Level " + (L + 1) + " of " + FLASH_LEVELS.length);
    ui.progN.textContent = (L + 1) + " / " + FLASH_LEVELS.length;
    ui.progChip.hidden = false;
    flashDots(G.answers.length);
    brainChips(false);
    var s = screen("st-flash");
    s.appendChild(el("div", { class: "st-flash-banner", "aria-hidden": "true" }, [
      el("span", { class: "st-flash-lv", text: "Level " + (L + 1) }), el("b", { text: n + " cards" })]));
    ui.ask = el("div", { class: "st-flash-ask" }, [
      el("h2", { class: "st-brain-q", tabindex: "-1", text: "Remember where each card is" }),
      el("p", { class: "st-flash-sub", text: opts.timer ? "They turn over when the fuse burns out." : "Press Hide the cards when you are ready." })]);
    s.appendChild(ui.ask);
    s.appendChild(fuseBar(ms, "to study the cards"));
    var grid = el("div", { class: "st-flash-grid", "data-n": String(n), role: "group", "aria-label": "Cards" });
    G.cards = ks.map(function (k, i) {
      var c = { k: k, i: i, up: true, done: false, text: stripTags(FP[k].a) };
      c.el = el("button", { class: "st-fcard is-up", type: "button", style: "--i:" + i, "aria-label": fcardLabel(c) }, [
        el("span", { class: "st-fcard-in" }, [
          el("span", { class: "st-fcard-back", "aria-hidden": "true", html: BOLT }),
          el("span", { class: "st-fcard-front", "aria-hidden": "true" }, [el("span", { class: "st-fcard-t", html: FP[k].a })])]),
        el("span", { class: "st-fcard-k", "aria-hidden": "true", text: String(i + 1) }),
        el("span", { class: "st-mark", "aria-hidden": "true" })]);
      c.el.addEventListener("click", function () { flashTap(c); });
      grid.appendChild(c.el);
      return c;
    });
    grid.addEventListener("keydown", function (e) { gridKeys(e, grid, ".st-fcard"); });
    s.appendChild(grid);
    ui.ready = el("button", { class: "st-go st-flash-ready", type: "button", html: ico("i-eye") + (opts.timer ? " I'm ready" : " Hide the cards") });
    ui.ready.addEventListener("click", flashHide);
    s.appendChild(el("div", { class: "st-brain-tools" }, [ui.ready]));
    ui.fb = el("div", { class: "st-fbslot" });
    s.appendChild(ui.fb);
    fitSoon();
    sfx("board");
    say("Level " + (L + 1) + " of " + FLASH_LEVELS.length + ". Remember these " + n + " cards: " +
        G.cards.map(function (c) { return (c.i + 1) + ", " + c.text; }).join("; ") + ".");
    focusFirst(ui.ask.querySelector("h2"));
    T = fuseClock(ms, flashHide);
  }
  function flashHide() {
    if (!G || G.phase !== "study") return;
    stopClock();
    G.phase = "turning";
    if (ui.ready && ui.ready.parentNode) ui.ready.parentNode.removeChild(ui.ready);
    if (ui.fuse) ui.fuse.hidden = true;
    if (!calm()) {
      var veil = el("span", { class: "st-flash-veil", "aria-hidden": "true" });
      ui.screen.appendChild(veil);
      setTimeout(function () { if (veil.parentNode) veil.parentNode.removeChild(veil); }, 700);
    }
    sfx("flip");
    G.cards.forEach(function (c, i) {
      after(calm() ? 0 : i * 90, function () { fcardUp(c, false); });
    });
    ui.tiles = G.cards.map(function (c) { return c.el; });
    after(calm() ? 50 : 520 + G.cards.length * 90, function () { G.phase = "recall"; G.ai = 0; G.ask = shuffle(G.cards.map(function (c) { return c.k; })); flashAsk(); });
  }
  function flashAsk() {
    if (!G) return;
    var k = G.ask[G.ai];
    G.tries = 0; G.locked = false;
    ui.ask.className = "st-flash-ask is-asking";
    ui.ask.innerHTML = "";
    var clue = D.flash.p[k].b;
    var h = el("h2", { class: "st-brain-q", tabindex: "-1", text: D.flash.q });
    ui.ask.appendChild(el("p", { class: "st-flash-count", text: "Clue " + (G.ai + 1) + " of " + G.ask.length }));
    ui.ask.appendChild(h);
    ui.ask.appendChild(el("p", { class: "st-flash-meaning" }, [el("span", { class: "st-flash-tag", text: D.pn[1] }), el("span", { html: clue })]));
    flashDots(G.answers.length);
    say(D.flash.q + " " + D.pn[1] + ": " + stripTags(clue) + ". Choose a card, or press its number.");
    focusFirst(h);
  }
  function flashTap(c) {
    if (!G || G.phase !== "recall" || G.locked || c.done || G.done) return;
    var k = G.ask[G.ai];
    G.locked = true;
    if (c.k === k) {
      var first = G.tries === 0;
      c.done = true;
      c.el.disabled = true;
      fcardUp(c, true);
      c.el.classList.add("is-found");
      markTile(c.el, true);
      G.answers.push(first);
      var gain;
      if (first) {
        G.right += 1; G.firsts += 1; G.streak += 1;
        G.bestStreak = Math.max(G.bestStreak, G.streak);
        gain = 100 * multi();
      } else gain = 50;
      brainWin(c.el, gain, first ? 6 : 2);
      sfx("good");
      say("Right! Card " + (c.i + 1) + " is " + c.text + ". Plus " + gain + " points.");
      after(calm() ? 700 : 1000, flashNext);
      return;
    }
    G.misses += 1; G.tries += 1; G.streak = 0;
    brainChips(false);
    fcardUp(c, true);
    c.el.classList.add("is-miss");
    sfx("bad");
    quake();
    if (G.tries < 2) {
      say("Not that one: card " + (c.i + 1) + " is " + c.text + ". Try once more.");
      after(1100, function () { c.el.classList.remove("is-miss"); fcardUp(c, false); G.locked = false; });
      return;
    }
    G.answers.push(false);
    var right = G.cards.filter(function (x) { return x.k === k; })[0];
    say("Not that one: card " + (c.i + 1) + " is " + c.text + ". The answer was card " + (right.i + 1) + ": " + right.text + ".");
    after(900, function () {
      c.el.classList.remove("is-miss");
      fcardUp(c, false);
      right.done = true;
      right.el.disabled = true;
      fcardUp(right, true);
      right.el.classList.add("is-shown");
      after(calm() ? 900 : 1500, flashNext);
    });
  }
  function flashNext() {
    if (!G) return;
    G.ai += 1;
    if (G.ai < G.ask.length) { flashAsk(); return; }
    G.locked = true; G.phase = "done";
    flashDots(-1);
    var last = G.level === FLASH_LEVELS.length - 1;
    var got = G.answers.slice(G.answers.length - G.ask.length).filter(Boolean).length;
    var bonus = got === G.ask.length ? 50 * G.ask.length : 0;
    sfx("level");
    if (bonus) brainWin(ui.ask, bonus, 8);
    ui.ask.className = "st-flash-ask is-clear";
    ui.ask.innerHTML = "";
    ui.ask.appendChild(el("h2", { class: "st-brain-q", tabindex: "-1", text: "Level " + (G.level + 1) + " cleared!" }));
    ui.ask.appendChild(el("p", { class: "st-flash-sub", text: got + " of " + G.ask.length + " found first time" + (bonus ? ": a perfect level, plus " + bonus + " points." : ".") }));
    var next = el("button", { class: "st-go", type: "button", html: (last ? "See my result" : "Level " + (G.level + 2) + ": " + FLASH_LEVELS[G.level + 1] + " cards") + " " + ico("i-arrow-right") });
    next.addEventListener("click", function () { if (!next.disabled) { next.disabled = true; if (last) flashResults(); else flashLevel(G.level + 1); } });
    ui.ask.appendChild(next);
    say("Level " + (G.level + 1) + " cleared. " + got + " of " + G.ask.length + " found first time.");
    setTimeout(function () { next.focus({ preventScroll: false }); }, calm() ? 0 : 350);
  }
  function flashResults() {
    var n = flashTotal(), pct = G.firsts / n;
    var stars = G.misses <= 1 ? 3 : G.misses <= 4 ? 2 : 1;
    var medals = [];
    if (!G.misses) medals.push(["cards", "#0891B2", "Photographic memory", "Every card first time"]);
    if (G.bestStreak >= 6) medals.push(["fire", "#EA580C", "Hot streak", plural(G.bestStreak, "card") + " in a row"]);
    brainResults({
      stars: stars, pts: G.pts, pct: pct,
      title: stars === 3 ? "Memory master" : stars === 2 ? "Sharp memory" : "A good start: play again to remember more",
      mood: stars === 3 ? "proud" : stars === 2 ? "cheer" : "happy", wear: stars === 3 ? ["crown"] : null,
      rows: [[art("flash"), "Found first time", G.firsts + " of " + n + ", " + misses(G.misses), fmt(G.pts)]],
      medals: medals,
      extra: reviewList("The cards and their clues", D.flash.p.map(function (p) { return '<span class="st-res-a">' + p.a + "</span> " + p.b; })),
      summary: G.firsts + " of " + n + " cards found first time, with " + misses(G.misses) + "."
    });
  }

  /* ========================================================= FACT OR FIB */
  var FIB_N = 12, FIB_MAX = 6, FIB_MS = 15000;
  var FIB_RIGHT = ["Fib spotted!", "Busted!", "Not fooled!", "Lie detector!"];
  function fibRuns(deck) {
    var most = 1, run = 1;
    for (var i = 1; i < deck.length; i++) { run = deck[i].t === deck[i - 1].t ? run + 1 : 1; most = Math.max(most, run); }
    return most;
  }
  function fibDeal() {
    var fibs = shuffle(D.fib.filter(function (f) { return !f.t; })).slice(0, FIB_MAX);
    var facts = shuffle(D.fib.filter(function (f) { return f.t; })).slice(0, FIB_N - fibs.length);
    var deck = shuffle(fibs.concat(facts));
    for (var k = 0; k < 60 && fibRuns(deck) > 3; k++) deck = shuffle(deck);
    return deck;
  }
  function fibSplash() {
    brainSplash("fib", "Statements fly in one at a time. Is each one a fact or a fib? Swipe right for fact and left for fib, tap the buttons, or use the arrow keys. " +
      FIB_N + " statements" + (opts.timer ? ", each with a fuse." : "."),
      function () { G.deck = fibDeal(); fibCard(0); });
  }
  function fibDots(now) { paintDots(G.deck.map(function (f, i) { return i < G.answers.length ? (G.answers[i] ? 1 : 0) : -1; }), now); }
  function fibCard(i) {
    if (!G) return;
    G.qi = i; G.locked = false;
    var f = G.deck[i], n = G.deck.length;
    label("Fact or Fib", "Statement " + (i + 1) + " of " + n);
    ui.progN.textContent = (i + 1) + " / " + n;
    ui.progChip.hidden = false;
    fibDots(i);
    brainChips(false);
    var s = screen("st-fib");
    s.appendChild(el("p", { class: "st-brain-round", text: "Statement " + (i + 1) + " of " + n }));
    s.appendChild(fuseBar(FIB_MS, "to decide"));
    var card = el("div", { class: "st-fib-card", tabindex: "-1", role: "group", "aria-label": "Statement " + (i + 1) + " of " + n }, [
      el("span", { class: "st-fib-stamp is-fact", "aria-hidden": "true", text: "Fact" }),
      el("span", { class: "st-fib-stamp is-fib", "aria-hidden": "true", text: "Fib" }),
      el("p", { class: "st-fib-t", html: f.s })]);
    ui.card = card;
    s.appendChild(el("div", { class: "st-fib-deck" }, [el("span", { class: "st-fib-under", "aria-hidden": "true" }), card]));
    ui.fibNo = el("button", { class: "st-fib-btn is-fib", type: "button", "aria-label": "Fib: it is not true. Left arrow key" }, [
      el("span", { class: "st-fib-ico", html: CROSS }), el("b", { text: "Fib" }), el("span", { class: "st-mark", "aria-hidden": "true" })]);
    ui.fibYes = el("button", { class: "st-fib-btn is-fact", type: "button", "aria-label": "Fact: it is true. Right arrow key" }, [
      el("b", { text: "Fact" }), el("span", { class: "st-fib-ico", html: TICK }), el("span", { class: "st-mark", "aria-hidden": "true" })]);
    ui.fibNo.addEventListener("click", function () { fibAnswer(false, false); });
    ui.fibYes.addEventListener("click", function () { fibAnswer(true, false); });
    s.appendChild(el("div", { class: "st-fib-btns" }, [ui.fibNo, el("span", { class: "st-fib-keys", "aria-hidden": "true", text: "or swipe the card" }), ui.fibYes]));
    ui.fb = el("div", { class: "st-fbslot" });
    s.appendChild(ui.fb);
    fibDrag(card);
    fitSoon();
    say("Statement " + (i + 1) + " of " + n + ": " + stripTags(f.s) + " Fact or fib?");
    focusFirst(card);
    T = fuseClock(FIB_MS, function () { fibAnswer(null, false); });
  }
  /* Drag the card: right for fact, left for fib. Short drags spring back. */
  function fibDrag(card) {
    var id = null, x0 = 0, dx = 0, w = 1;
    card.addEventListener("pointerdown", function (e) {
      if (!G || G.locked || (e.pointerType === "mouse" && e.button !== 0)) return;
      id = e.pointerId; x0 = e.clientX; dx = 0; w = card.offsetWidth || 1;
      try { card.setPointerCapture(id); } catch (err) { /* not every pointer can be captured */ }
      card.classList.add("is-drag");
    });
    card.addEventListener("pointermove", function (e) {
      if (e.pointerId !== id) return;
      dx = e.clientX - x0;
      card.style.setProperty("--dx", dx + "px");
      card.style.setProperty("--r", Math.max(-1, Math.min(1, dx / (w * 0.4))).toFixed(3));
    });
    function end(e) {
      if (e.pointerId !== id) return;
      id = null;
      card.classList.remove("is-drag");
      card.style.setProperty("--dx", "0px");
      card.style.setProperty("--r", "0");
      if (Math.abs(dx) > Math.min(110, w * 0.28) && G && !G.locked) fibAnswer(dx > 0, true);
    }
    card.addEventListener("pointerup", end);
    card.addEventListener("pointercancel", end);
  }
  function fibAnswer(says, swiped) {
    if (!G || G.locked || G.done || !G.deck) return;
    G.locked = true;
    var f = G.deck[G.qi], late = says === null, truth = !!f.t, ok = !late && says === truth;
    var ms = T ? T.elapsed() : 0;
    stopClock();
    ui.fibNo.disabled = true; ui.fibYes.disabled = true;
    ui.card.classList.add(truth ? "show-fact" : "show-fib", ok ? "is-ok" : "is-bad");
    if (!late && !swiped) markTile(says ? ui.fibYes : ui.fibNo, ok);
    sfx("stamp");
    G.answers.push(ok);
    var gain = 0;
    if (ok) {
      G.right += 1; G.streak += 1;
      G.bestStreak = Math.max(G.bestStreak, G.streak);
      if (!truth) G.caught += 1;
      var quick = opts.timer && ms <= FIB_MS / 3;
      if (quick) G.fast += 1;
      gain = (100 + (opts.timer ? Math.round(50 * Math.max(0, 1 - ms / FIB_MS)) : 0)) * multi();
      brainWin(ui.card, gain, quick ? 7 : 5);
    } else {
      G.streak = 0;
      quake();
      brainChips(false);
    }
    fibDots(-1);
    setTimeout(function () { sfx(ok ? "good" : "bad"); }, 120);
    var last = G.qi === G.deck.length - 1;
    var go = function () { if (last) fibResults(); else fibCard(G.qi + 1); };
    if (ok && truth) {
      say("Right, it is a fact. Plus " + gain + " points.");
      after(calm() ? 900 : 1150, function () {
        if (!calm()) ui.card.classList.add("is-gone");
        after(calm() ? 0 : 260, go);
      });
      return;
    }
    var head = ok ? pick(FIB_RIGHT) : late ? "Out of time!" : truth ? "That one is a fact" : "That one is a fib";
    var html = truth ? "<b>It is true:</b> " + f.s :
      '<span class="st-fb-ans"><b>The fib:</b> ' + f.s + "</span>" + (f.x ? "<b>The truth:</b> " + f.x : "");
    roundPanel(ok, head, gain, ok && G.streak >= 3 ? G.streak + " in a row! Points x" + multi() + "." : "", html,
      last ? "See my result" : "Next statement", go);
    say((ok ? "Right, it is a fib. " : late ? "Time is up. " : "Not quite. ") + (truth ? "It is a fact: " + stripTags(f.s) :
        "It is a fib. " + (f.x ? "The truth: " + stripTags(f.x) : "")));
  }
  function fibResults() {
    var n = G.deck.length, pct = G.right / n;
    var fibs = G.deck.filter(function (f) { return !f.t; }).length;
    var stars = G.right === n ? 3 : G.right >= n - 3 ? 2 : 1;
    var medals = [];
    if (G.caught === fibs) medals.push(["sweep", "#16A34A", "Lie detector", "Every fib caught"]);
    if (G.bestStreak >= 6) medals.push(["fire", "#EA580C", "Hot streak", plural(G.bestStreak, "answer") + " in a row"]);
    if (G.fast >= 6) medals.push(["bolt", "#7C3AED", "Speed reader", plural(G.fast, "fast answer")]);
    var missed = [];
    G.deck.forEach(function (f, i) {
      if (G.answers[i]) return;
      missed.push(f.s + ' <span class="st-res-ans">' + (f.t ? "This is a fact." : "A fib. " + (f.x ? "The truth: " + f.x : "")) + "</span>");
    });
    brainResults({
      stars: stars, pts: G.pts, pct: pct,
      title: stars === 3 ? "Fact checker supreme" : stars === 2 ? "Sharp judge" : "A good start: play again to catch every fib",
      mood: stars === 3 ? "proud" : stars === 2 ? "cheer" : "happy", wear: stars === 3 ? ["crown"] : null,
      rows: [[art("fib"), "Right calls", G.right + " of " + n + ", " + G.caught + " of " + fibs + " fibs caught", fmt(G.pts)]],
      medals: medals,
      extra: missed.length ? reviewList("The ones to look at again", missed) : null,
      summary: G.right + " of " + n + " right, with " + G.caught + " of " + fibs + " fibs caught."
    });
  }
  /* ============================================================ CITY RUN */
  /* A robot cat skates along the tracks of a neon cyber city: Neon Station,
     Ramen Row, Arcade Alley and the Hyper Tunnel, five questions in each.
     Each question is a row of neon gates across the tracks with an answer
     over each one: steer onto the right track, or tap an answer to sprint
     to it for bonus points. Between questions the cat dodges metro cars,
     holograms, crates and cones and picks up diamonds. static/js/cityrun.js
     draws the city; what is right is decided here. */
  var RUN_HIT = { puddle: 10, cone: 30, barrier: 30, crate: 30, holo: 30, metro: 30, works: 0 };
  // each track's neon, and the dark ink that sits on it
  var RUN_COL = [["#22D3EE", "#083344"], ["#FBBF24", "#422006"], ["#F472B6", "#500724"]];
  var RUN_RIGHT = ["Correct!", "Spot on!", "Brilliant!", "Nailed it!", "Top speed!", "Yes!"];
  var RUN_WRONG = ["Not quite", "Wrong lane", "Not this time"];
  var RUN_TIPS = ["Swipe up, or press the up arrow or space, to jump cones, crates and barriers.",
                  "Metro cars and holograms are too tall to jump. Change tracks!",
                  "Tap an answer to sprint to its gate and win bonus points.",
                  "Every diamond you pick up is worth 10 points.",
                  "Three right in a row doubles your points. Six in a row trebles them.",
                  "Bumping into anything costs you 30 points. Watch the tracks!"];
  var RUN_ARROW = [
    '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M14.5 5.5 8 12l6.5 6.5" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M5.5 14.5 12 8l6.5 6.5" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M9.5 5.5 16 12l-6.5 6.5" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></svg>'];
  var RUN_PAUSE = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><rect x="6" y="5" width="4" height="14" rx="1.4" fill="currentColor"/><rect x="14" y="5" width="4" height="14" rx="1.4" fill="currentColor"/></svg>';
  var RUN_PLAY = '<svg viewBox="0 0 24 24" aria-hidden="true" focusable="false"><path d="M8 5.5v13l11-6.5Z" fill="currentColor"/></svg>';

  /* The robot cat, from the page's template, with ids of its own. */
  function robocat(mood) {
    var tpl = document.getElementById("st-robocat");
    if (!tpl) return null;
    var svg = (tpl.content ? tpl.content.firstElementChild : tpl.firstElementChild).cloneNode(true);
    pxSeq += 1;
    var map = {};
    Array.prototype.forEach.call(svg.querySelectorAll("[id]"), function (n) { map[n.id] = n.id + "-k" + pxSeq; n.id = map[n.id]; });
    Array.prototype.forEach.call(svg.querySelectorAll("[fill^='url(#']"), function (n) {
      var m = /^url\(#([^)]+)\)$/.exec(n.getAttribute("fill"));
      if (m && map[m[1]]) n.setAttribute("fill", "url(#" + map[m[1]] + ")");
    });
    svg.setAttribute("class", "rc is-" + (mood || "idle"));
    svg.setAttribute("aria-hidden", "true");
    return svg;
  }

  /* Twenty questions from the lesson: the quiz's, This or That's, Memory
     Flash's pairs and Fact or Fib's statements, with no three of a kind in
     a row. Each gets its lanes: three answers fill the road; with two, the
     middle lane is closed for road works. Fib is always on the left and
     fact on the right, as in Fact or Fib. */
  function runDeal() {
    var R = D.run, most = {}, out = [];
    R.mix.forEach(function (m) { most[m[0]] = m[1]; });
    shuffle(R.c.slice()).slice(0, most.c).forEach(function (q) {
      out.push({ k: "c", q: q.q, code: q.c, x: q.x, o: [q.o[0]].concat(shuffle(q.o.slice(1)).slice(0, 2)) });
    });
    shuffle(R.p.slice()).slice(0, most.p).forEach(function (q) {
      out.push({ k: "p", q: q.q, code: q.c, x: q.x, o: [q.o[0], q.o[1]] });
    });
    var pairs = D.flash.p, idx = pairs.map(function (p, i) { return i; });
    shuffle(idx.slice()).slice(0, Math.min(most.m, pairs.length)).forEach(function (i) {
      var other = shuffle(idx.filter(function (j) { return j !== i; })).slice(0, 2);
      out.push({ k: "m", q: pairs[i].b, o: [pairs[i].a, pairs[other[0]].a, pairs[other[1]].a] });
    });
    var need = R.n - out.length;
    var fibs = shuffle(D.fib.filter(function (f) { return !f.t; })), facts = shuffle(D.fib.filter(function (f) { return f.t; }));
    var nf = Math.min(fibs.length, Math.ceil(need / 2)), nt = Math.min(facts.length, need - nf);
    nf = Math.min(fibs.length, need - nt);
    fibs.slice(0, nf).concat(facts.slice(0, nt)).forEach(function (f) { out.push({ k: "f", q: f.s, truth: !!f.t, x: f.x }); });
    for (var k = 0; k < 120; k++) {
      out = shuffle(out);
      var three = false;
      for (var i = 2; i < out.length; i++) if (out[i].k === out[i - 1].k && out[i].k === out[i - 2].k) three = true;
      if (!three && !(out[0].code)) break;
    }
    out.forEach(function (q) {
      if (q.k === "f") { q.lanes = [{ i: "fib" }, null, { i: "fact" }]; q.right = q.truth ? 2 : 0; return; }
      var order = shuffle(q.o.map(function (o, j) { return j; }));
      if (order.length === 2) { q.lanes = [{ i: order[0] }, null, { i: order[1] }]; q.right = order[0] === 0 ? 0 : 2; }
      else { q.lanes = order.map(function (j) { return { i: j }; }); q.right = order.indexOf(0); }
    });
    return out;
  }
  function runLetter(q, l) { return q.k === "f" ? (l === 0 ? "Fib" : "Fact") : !q.lanes[1] ? (l === 0 ? "A" : "B") : "ABC".charAt(l); }
  function runColour(q, l) {
    if (q.k === "f") return l === 0 ? ["#F87171", "#450A0A"] : ["#4ADE80", "#052E16"];
    return RUN_COL[q.lanes[1] ? l : l === 0 ? 0 : 2];
  }
  /* What the gates' banners say, for cityrun.js. */
  function runLanes(q) {
    return [0, 1, 2].map(function (l) {
      if (!q.lanes[l]) return null;
      var c = runColour(q, l);
      if (q.k === "f") return { t: "", icon: l === 0 ? "cross" : "tick", s: l === 0 ? "Fib" : "Fact", c: c[0], ink: c[1] };
      return { t: runLetter(q, l), s: stripTags(q.o[q.lanes[l].i]), c: c[0], ink: c[1] };
    });
  }
  /* Seconds to read a question before its gate: more for longer text and for code. */
  function runRead(q) {
    var chars = stripTags(q.q).length + (q.k === "f" ? 12 : q.o.reduce(function (n, o) { return n + stripTags(o).length; }, 0));
    var lines = q.code ? q.code.split("\n").length : 0;
    return Math.max(8, Math.min(20, 5.5 + 0.055 * chars + 1.5 * lines));
  }

  function runSplash() {
    label("City Run", "Cyber City Dash");
    ui.dots.innerHTML = "";
    ui.progChip.hidden = true;
    runChips();
    var s = screen("st-splash st-run-splash");
    s.appendChild(el("span", { class: "st-splash-tag st-run-badge", text: "Cyber City Dash" }));
    // the run's picture from the lobby, or the cat on its own
    var shot = lobby.querySelector(".st-run-shot"), hero = el("div", { class: "st-run-hero", "aria-hidden": "true" });
    if (shot) { var pic = shot.cloneNode(true); pic.setAttribute("loading", "eager"); hero.appendChild(pic); }
    else { var cat = robocat("idle"); if (cat) hero.appendChild(cat); }
    s.appendChild(hero);
    s.appendChild(el("h2", { tabindex: "-1", text: "City Run" }));
    var sub = "Race a robot cat on inline skates through a neon cyber city, from Neon Station to the Hyper Tunnel. " + D.run.n + " questions from this lesson stand across the tracks as gates: skate through the one with the right answer." +
      (opts.timer ? "" : " The clock is off, so the cat waits at each gate for you.");
    s.appendChild(el("p", { text: sub }));
    var how = el("ul", { class: "st-run-how" });
    [[RUN_ARROW[0] + RUN_ARROW[2], "Steer", "swipe, or the left and right arrow keys"],
     [RUN_ARROW[1], "Jump", "swipe up, or the up arrow or space"],
     ['<b class="st-run-k">1</b><b class="st-run-k">2</b><b class="st-run-k">3</b>', "Answer", "tap an answer, or press its number, to sprint to its gate"]].forEach(function (r) {
      how.appendChild(el("li", {}, [el("span", { class: "st-run-how-ico", "aria-hidden": "true", html: r[0] }), el("b", { text: r[1] + ": " }), document.createTextNode(r[2])]));
    });
    s.appendChild(how);
    if (calm()) s.appendChild(el("p", { class: "st-run-calm", text: "Your device asks for less motion, so the cat skates more gently and nothing shakes." }));
    s.appendChild(el("p", { class: "st-brain-prize", html: '<span class="st-brain-prize-g" aria-hidden="true">' + GEM + GEM + GEM + "</span>Win up to three diamonds" }));
    var go = el("button", { class: "st-go", type: "button", html: ico("i-play") + " Start running" });
    go.addEventListener("click", runStart);
    s.appendChild(go);
    sfx("board");
    say("City Run. " + sub);
    focusFirst(go);
  }

  function runStart() {
    if (!window.MskCityRun) return;
    G.qs = runDeal();
    G.qi = -1; G.cur = null; G.lost = 0; G.hits = 0; G.picked = 0; G.pts = 0; G.lastCoin = 0;
    var s = screen("st-run");
    stage.classList.add("is-running");
    ui.runKick = el("p", { class: "st-run-kick" });
    ui.runSecs = el("span", { class: "st-run-secs", "aria-hidden": "true" });
    ui.runQ = el("div", { class: "st-run-q" });
    ui.runFuse = el("div", { class: "st-run-fuse", "aria-hidden": "true" }, [el("span", { class: "st-run-fuse-fill" })]);
    ui.runCard = el("div", { class: "st-run-card" }, [el("div", { class: "st-run-cardtop" }, [ui.runKick, ui.runSecs]), ui.runQ, ui.runFuse]);
    ui.runCanvas = el("canvas", { class: "st-run-canvas", "aria-hidden": "true" });
    ui.runRoute = runRoute();
    ui.runPause = el("button", { class: "st-run-pause", type: "button", "aria-label": "Pause the run. Key P", html: RUN_PAUSE });
    ui.runPause.addEventListener("click", function () { runPause(!G.world.paused()); });
    ui.runLayer = el("div", { class: "st-run-layer", "aria-hidden": "true" });
    ui.runFb = el("div", { class: "st-run-fb" });
    ui.runView = el("div", { class: "st-run-view" }, [ui.runCanvas, ui.runRoute, ui.runPause, ui.runLayer, ui.runFb]);
    ui.runOpts = el("div", { class: "st-run-opts" });
    s.appendChild(ui.runCard);
    s.appendChild(ui.runView);
    s.appendChild(ui.runOpts);
    runSwipe(ui.runView);
    G.world = window.MskCityRun.world(ui.runCanvas, {
      gates: G.qs.map(function (q) { return { lanes: runLanes(q), read: runRead(q) }; }),
      timer: opts.timer, calm: calm(),
      onRead: function (i) { if (G && G.world) runQuestion(i); },
      onGate: function (i, lane) { return runGate(i, lane); },
      onHit: function (kind) { return runHit(kind); },
      onGem: function () { runGem(); },
      onDistrict: function (k) { runDistrict(k); },
      onFinish: function () { runFinish(); },
      onAutoPause: function () { if (G && G.world && !G.done) runPause(true); },
      sound: function (name) { sfx(name); }
    });
    runIdle(0, true);
    runTick(G);
    // three, two, one, go
    var c = el("div", { class: "st-count st-run-count" });
    ui.runLayer.appendChild(c);
    var n = 3, game = G;
    (function tick() {
      if (G !== game) return;
      if (n === 0) {
        c.textContent = "Go!";
        c.classList.remove("is-pop"); void c.offsetWidth; c.classList.add("is-pop");
        sfx("go");
        G.world.start();
        setTimeout(function () { if (c.parentNode) c.parentNode.removeChild(c); }, 600);
        return;
      }
      c.textContent = String(n);
      c.classList.remove("is-pop"); void c.offsetWidth; c.classList.add("is-pop");
      sfx("count");
      n -= 1;
      setTimeout(tick, 700);
    })();
    say("Get ready. 3, 2, 1, go!");
    focusFirst(ui.runView);
    ui.runView.setAttribute("tabindex", "-1");
  }

  /* The four districts along a line, with the cat's progress. */
  function runRoute() {
    var box = el("div", { class: "st-run-route", "aria-hidden": "true" });
    ui.runFill = el("b", { class: "st-run-route-fill" });
    box.appendChild(el("i", { class: "st-run-route-line" }, [ui.runFill]));
    D.run.d.forEach(function (name, k) { box.appendChild(el("span", { class: "st-run-stop", style: "left:" + (k * 25 + 12.5) + "%", text: name })); });
    ui.runMark = el("span", { class: "st-run-mark", html: GEM });
    box.appendChild(ui.runMark);
    return box;
  }
  function runRoutePaint() {
    var p = Math.min(1, G.answers.length / G.qs.length);
    ui.runFill.style.width = (p * 100) + "%";
    ui.runMark.style.left = (p * 100) + "%";
  }

  /* The chips: points straight away, since diamonds land all the time. */
  function runChips() {
    ui.ptsN.textContent = fmt(G.pts);
    ui.ptsChip.setAttribute("aria-label", fmt(G.pts) + " points");
    var m = multi();
    ui.streak.hidden = G.streak < 2;
    ui.streakN.textContent = String(G.streak);
    ui.streak.classList.toggle("is-hot", G.streak >= 3);
    ui.multi.hidden = m < 2;
    ui.multi.textContent = "x" + m;
    ui.streak.setAttribute("aria-label", "Streak " + G.streak + (m > 1 ? ", points times " + m : ""));
  }

  /* Between questions: what is coming, a tip, and the steering buttons. */
  function runIdle(next, first) {
    if (!G || G.done) return;
    G.cur = null;
    var n = G.qs.length, k = Math.min(3, Math.floor(next / 5));
    ui.runCard.classList.remove("is-q");
    ui.runKick.textContent = first ? "Get ready" : next < n ? D.run.d[k] : D.run.d[3];
    ui.runSecs.textContent = "";
    ui.runQ.innerHTML = "";
    ui.runQ.appendChild(el("p", { class: "st-run-idle", text: next < n ? "Question " + (next + 1) + " of " + n + " is coming up." : "Last stretch: race to the finish line!" }));
    ui.runQ.appendChild(el("p", { class: "st-run-tip", text: RUN_TIPS[next % RUN_TIPS.length] }));
    ui.runFuse.style.setProperty("--p", "0");
    ui.runFuse.classList.remove("is-low");
    runControls();
  }
  function runControls() {
    ui.runBtns = null;
    ui.runOpts.innerHTML = "";
    ui.runOpts.className = "st-run-opts is-pad";
    [[RUN_ARROW[0], "Left", "Move left. Left arrow key", -1], [RUN_ARROW[1], "Jump", "Jump. Up arrow or space", 0], [RUN_ARROW[2], "Right", "Move right. Right arrow key", 1]].forEach(function (c) {
      var b = el("button", { class: "st-run-padbtn", type: "button", "aria-label": c[2] }, [el("span", { html: c[0] }), el("b", { text: c[1] })]);
      b.addEventListener("click", function () { if (!G || !G.world) return; if (c[3]) G.world.steer(c[3]); else G.world.jump(); });
      ui.runOpts.appendChild(b);
    });
  }

  /* A question: its text in the card and its answers in the lanes' colours. */
  function runQuestion(i) {
    if (!G || G.done) return;
    var q = G.qs[i], n = G.qs.length;
    G.qi = i; G.cur = q; G.locked = false; G.quick = false; G.here = -1; G.lastSecs = -1;
    label("City Run", D.run.d[Math.min(3, Math.floor(i / 5))] + ": question " + (i + 1) + " of " + n);
    ui.progN.textContent = (i + 1) + " / " + n;
    ui.progChip.hidden = false;
    ui.runCard.classList.add("is-q");
    var kind = q.k === "f" ? "Fact or fib?" : q.k === "m" ? stripTags(D.flash.q) : q.k === "p" ? "This or That" : "Pick a lane";
    ui.runKick.textContent = "Question " + (i + 1) + " · " + kind;
    ui.runQ.innerHTML = "";
    if (q.k === "m") ui.runQ.appendChild(el("span", { class: "st-run-cluetag", text: D.pn[1] }));
    ui.runQ.appendChild(el("p", { class: "st-run-qt", html: q.q }));
    if (q.code) ui.runQ.appendChild(codeBox(q.code));
    runOptions(q);
    fitWords(ui.runQ, ".st-run-qt", 0.8);
    var spoken = [0, 1, 2].filter(function (l) { return q.lanes[l]; }).map(function (l) {
      return (q.k === "f" ? runLetter(q, l) : "Answer " + runLetter(q, l)) + ", " + (l === 0 ? "left" : l === 1 ? "middle" : "right") + " lane" +
        (q.k === "f" ? "" : ": " + stripTags(q.o[q.lanes[l].i]));
    }).join(". ");
    say("Question " + (i + 1) + " of " + n + ". " + (q.k === "m" ? stripTags(D.flash.q) + " " : "") + stripTags(q.q) + (q.k === "f" ? " Fact or fib?" : "") + " " + spoken + ".");
  }
  function runOptions(q) {
    ui.runOpts.innerHTML = "";
    ui.runOpts.className = "st-run-opts is-" + (q.lanes[1] ? "three" : "two") + (q.k === "f" ? " is-fib" : "");
    ui.runBtns = [null, null, null];
    var key = 0;
    [0, 1, 2].forEach(function (l) {
      if (!q.lanes[l]) return;
      key += 1;
      var c = runColour(q, l), where = l === 0 ? "left" : l === 1 ? "middle" : "right";
      var text = q.k === "f" ? (l === 0 ? "Fib: it is not true" : "Fact: it is true") : q.o[q.lanes[l].i];
      var b = el("button", { class: "st-run-opt", type: "button", "data-lane": String(l), style: "--oc:" + c[0] + ";--od:" + c[1],
                             "aria-label": (q.k === "f" ? runLetter(q, l) : "Answer " + runLetter(q, l)) + ", " + where + " lane: " + stripTags(text) + ". Key " + key }, [
        el("span", { class: "st-run-arrow", "aria-hidden": "true", html: RUN_ARROW[l] }),
        el("span", { class: "st-run-letter", "aria-hidden": "true", html: q.k === "f" ? (l === 0 ? CROSS : TICK) : runLetter(q, l) }),
        el("span", { class: "st-run-txt", html: q.k === "f" ? "<b>" + runLetter(q, l) + "</b>" : text }),
        el("span", { class: "st-run-key", "aria-hidden": "true", text: String(key) })]);
      b.addEventListener("click", function () { runCommit(l); });
      ui.runBtns[l] = b;
      ui.runOpts.appendChild(b);
    });
  }
  /* Lock in an answer: the cat moves over and sprints to its gate. */
  function runCommit(lane) {
    if (!G || !G.cur || G.locked || !G.world || G.world.paused()) return;
    var quick = opts.timer && G.world.progress(G.qi) < 0.5;
    if (!G.world.commit(lane)) return;
    G.locked = true;
    G.quick = quick;
    ui.runBtns.forEach(function (b, l) { if (b) { b.disabled = true; b.classList.toggle("is-picked", l === lane); } });
    sfx("go");
  }
  /* Every frame: the fuse, the seconds left, and which answer the cat is under. */
  function runTick(game) {
    if (G !== game || !G.world) return;
    var q = G.cur;
    if (q) {
      var p = G.world.progress(G.qi);
      ui.runFuse.style.setProperty("--p", (1 - p).toFixed(4));
      if (opts.timer) {
        var secs = Math.ceil(G.world.secondsLeft(G.qi));
        if (secs !== G.lastSecs) {
          G.lastSecs = secs;
          ui.runSecs.textContent = secs + "s";
          ui.runFuse.classList.toggle("is-low", secs <= 3);
          if (secs === 3) say("3 seconds");
        }
      } else ui.runSecs.textContent = G.world.waiting() ? "Your move" : "No clock";
      var here = G.world.lane();
      if (here !== G.here && ui.runBtns) {
        G.here = here;
        ui.runBtns.forEach(function (b, l) { if (b) b.classList.toggle("is-here", l === here); });
      }
    }
    requestAnimationFrame(function () { runTick(game); });
  }
  /* Where a gate is on the page, for diamonds to fly from. */
  function runPoint(lane) {
    var r = ui.runCanvas.getBoundingClientRect(), p = G.world.point(lane);
    return { getBoundingClientRect: function () { return { left: r.left + p.x - 30, top: r.top + p.y - 30, width: 60, height: 60 }; } };
  }

  /* The cat reaches a gate: is it the right lane? */
  function runGate(i, lane) {
    var q = G.qs[i];
    var blocked = !q.lanes[lane], ok = !blocked && lane === q.right;
    G.answers.push(ok);
    G.cur = null;
    G.locked = true;
    if (ui.runBtns) ui.runBtns.forEach(function (b, l) {
      if (!b) return;
      b.disabled = true;
      if (l === q.right) b.classList.add("is-right");
      else if (l === lane) b.classList.add("is-wrong");
    });
    ui.runSecs.textContent = "";
    runRoutePaint();
    if (ok) {
      G.right += 1; G.streak += 1;
      G.bestStreak = Math.max(G.bestStreak, G.streak);
      if (G.quick) G.fast += 1;
      var gain = 100 * multi() + (G.quick ? 50 : 0);
      G.pts += gain;
      var from = runPoint(lane);
      floatText(from, "+" + fmt(gain), multi() > 1 ? "is-multi" : "");
      gemFly(from, G.quick ? 7 : 5, function () { bump(ui.ptsChip); sfx("gem"); });
      runChips();
      runToast(pick(RUN_RIGHT) + (G.streak >= 3 ? " " + G.streak + " in a row!" : ""), "is-ok");
      setTimeout(function () { sfx("good"); }, 100);
      say("Right! Plus " + gain + " points." + (G.streak >= 3 ? " " + G.streak + " in a row." : ""));
      var game = G;
      // unless the next question has already reached the card
      setTimeout(function () { if (G === game && !G.done && G.qi === i && !G.cur) runIdle(i + 1); }, calm() ? 600 : 1000);
    } else {
      G.streak = 0;
      runChips();
      G.world.hold();
      quake();
      setTimeout(function () { sfx("bad"); }, 100);
      runFeedback(q, lane, blocked, i);
    }
    return { ok: ok, right: q.right };
  }
  function runAnswerHtml(q) {
    if (q.k === "f") {
      return q.truth ? "<b>It is a fact:</b> " + q.q :
        '<span class="st-fb-ans"><b>It is a fib:</b> ' + q.q + "</span>" + (q.x ? " <b>The truth:</b> " + q.x : "");
    }
    return "<b>The answer was " + runLetter(q, q.right) + ":</b> " + q.o[0] + endStop(q.o[0]) + (q.x ? " " + q.x : "");
  }
  /* After a wrong lane the cat stops, and the panel shows the right answer. */
  function runFeedback(q, lane, blocked, i) {
    var head = blocked ? "Track closed!" : pick(RUN_WRONG);
    var html = (blocked ? "The middle track was closed, so pick a side next time. " : "") + runAnswerHtml(q);
    var next = el("button", { class: "st-go", type: "button", html: (i === G.qs.length - 1 ? "Run to the finish" : "Keep running") + " " + ico("i-arrow-right") });
    var panel = el("div", { class: "st-catfb is-plain is-bad st-run-panel", role: "status" }, [
      el("div", { class: "st-catfb-head" }, [el("span", { class: "st-catfb-badge", "aria-hidden": "true", html: ico("i-cross") }), el("b", { text: head })]),
      el("p", { class: "st-catfb-x", html: html }),
      el("div", { class: "st-fb-go" }, [next])]);
    next.addEventListener("click", function () {
      if (next.disabled) return;
      next.disabled = true;
      if (panel.parentNode) panel.parentNode.removeChild(panel);
      G.world.resume();
      runIdle(i + 1);
      focusFirst(ui.runView);
    });
    ui.runFb.appendChild(panel);
    say(head + ". " + stripTags(html));
    try { next.focus({ preventScroll: true }); } catch (e) { next.focus(); }
  }
  function runToast(text, cls) {
    if (!ui.runLayer) return;
    var t = el("div", { class: "st-run-toast " + (cls || ""), text: text });
    ui.runLayer.appendChild(t);
    setTimeout(function () { if (t.parentNode) t.parentNode.removeChild(t); }, 1500);
  }
  function runHit(kind) {
    if (!G || G.done) return 0;
    var lose = Math.min(G.pts, RUN_HIT[kind] || 0);
    G.pts -= lose;
    G.lost += lose;
    if (kind !== "puddle" && kind !== "works") G.hits += 1;
    runChips();
    if (kind === "works") return 0;
    sfx(kind === "puddle" ? "splash" : "hit");
    if (lose) {
      runToast((kind === "puddle" ? "Splash! " : "Bump! ") + lose + " points lost", "is-bad");
      bump(ui.ptsChip);
    }
    return Math.round(lose / 10);
  }
  function runGem() {
    if (!G || G.done) return;
    G.pts += 10;
    G.picked += 1;
    runChips();
    var now = performance.now();
    if (now - G.lastCoin > 90) { G.lastCoin = now; sfx("coin"); bump(ui.ptsChip); }
  }
  function runDistrict(k) {
    if (!G || G.done || !ui.runLayer) return;
    var b = el("div", { class: "st-run-banner" }, [el("small", { text: "Welcome to" }), el("b", { text: D.run.d[k] })]);
    ui.runLayer.appendChild(b);
    setTimeout(function () { if (b.parentNode) b.parentNode.removeChild(b); }, 2600);
    sfx("level");
    say("Welcome to " + D.run.d[k] + ".");
  }
  function runFinish() {
    if (!G || G.done) return;
    G.cur = null;
    runToast("Finish!", "is-finish");
    sfx("level");
    var game = G;
    setTimeout(function () { if (G === game && !G.done) runResults(); }, calm() ? 700 : 1700);
  }
  function runPause(on) {
    if (!G || !G.world || G.done) return;
    G.world.pause(on);
    ui.runPause.innerHTML = on ? RUN_PLAY : RUN_PAUSE;
    ui.runPause.setAttribute("aria-label", on ? "Carry on running. Key P" : "Pause the run. Key P");
    var old = ui.runView.querySelector(".st-run-paused");
    if (old) old.parentNode.removeChild(old);
    if (on) {
      var go = el("button", { class: "st-go", type: "button", html: RUN_PLAY + " Carry on" });
      go.addEventListener("click", function () { runPause(false); focusFirst(ui.runView); });
      ui.runView.appendChild(el("div", { class: "st-run-paused" }, [el("b", { text: "Paused" }), go]));
      say("Paused.");
      focusFirst(go);
    }
  }
  /* Swipes on the street: left, right and up. A tap on either side of the
     street steers that way. */
  function runSwipe(view) {
    var id = null, x0 = 0, y0 = 0;
    view.addEventListener("pointerdown", function (e) {
      if (e.target.closest("button") || !G || !G.world) return;
      id = e.pointerId; x0 = e.clientX; y0 = e.clientY;
    });
    function end(e) {
      if (e.pointerId !== id) return;
      id = null;
      if (!G || !G.world || G.world.paused()) return;
      var dx = e.clientX - x0, dy = e.clientY - y0;
      if (Math.abs(dx) < 24 && Math.abs(dy) < 24) {
        var r = view.getBoundingClientRect(), fx = (e.clientX - r.left) / r.width;
        if (fx < 0.33) G.world.steer(-1); else if (fx > 0.67) G.world.steer(1); else G.world.jump();
      } else if (Math.abs(dx) > Math.abs(dy)) G.world.steer(dx > 0 ? 1 : -1);
      else if (dy < 0) G.world.jump();
    }
    view.addEventListener("pointerup", end);
    view.addEventListener("pointercancel", function () { id = null; });
  }
  /* Keys: arrows or A and D steer, up, W or space jump, 1 to 3 answer,
     Enter runs on with the clock off, and P pauses. */
  function runKey(e, tag) {
    var w = G.world, k = e.key;
    if (k === "p" || k === "P") { runPause(!w.paused()); return true; }
    if (w.paused()) return false;
    var onButton = tag === "button" || tag === "a";
    var carryOn = ui.runFb && ui.runFb.querySelector(".st-go");
    if (carryOn && (k === "Enter" || k === " ")) { if (!onButton) carryOn.click(); return !onButton; }
    if (k === "ArrowLeft" || k === "a" || k === "A") { w.steer(-1); return true; }
    if (k === "ArrowRight" || k === "d" || k === "D") { w.steer(1); return true; }
    if (k === "ArrowUp" || k === "w" || k === "W" || (k === " " && !onButton)) { w.jump(); return true; }
    if (/^[1-3]$/.test(k) && G.cur && ui.runBtns) {
      var live = ui.runBtns.map(function (b, l) { return b ? l : -1; }).filter(function (l) { return l > -1; });
      var lane = live[parseInt(k, 10) - 1];
      if (lane !== undefined) { runCommit(lane); return true; }
    }
    if (k === "Enter" && !onButton && G.cur && !G.locked) {
      if (ui.runBtns && ui.runBtns[w.lane()]) runCommit(w.lane());
      return true;
    }
    return false;
  }

  function runResults() {
    var n = G.qs.length, pct = G.right / n;
    var stars = G.right >= n - 2 ? 3 : G.right >= n - 6 ? 2 : 1;
    var medals = [];
    if (G.right === n) medals.push(["sweep", "#16A34A", "Perfect run", "Every gate right"]);
    if (G.hits === 0) medals.push(["shield", "#0284C7", "Untouchable", "Not one bump"]);
    if (G.picked >= 50) medals.push(["gem", "#7C3AED", "Diamond magnet", plural(G.picked, "diamond") + " picked up"]);
    if (G.bestStreak >= 8) medals.push(["fire", "#EA580C", "Hot streak", plural(G.bestStreak, "answer") + " in a row"]);
    if (G.fast >= 8) medals.push(["paw", "#DB2777", "Quick paws", plural(G.fast, "fast answer")]);
    var missed = [];
    G.qs.forEach(function (q, i) {
      if (G.answers[i]) return;
      var ask = q.k === "m" ? stripTags(D.flash.q) + " " : "";
      missed.push(ask + q.q + ' <span class="st-res-ans">' + (q.k === "f" ? (q.truth ? "A fact." : "A fib." + (q.x ? " The truth: " + q.x : "")) :
        "Answer: " + q.o[0]) + "</span>");
    });
    var hero = robocat(stars === 3 ? "happy" : "idle");
    G.world.destroy();
    G.world = null;
    ui.progChip.hidden = true;
    ui.streak.hidden = true;
    taskResults({
      stars: stars, pts: G.pts, pct: pct, hero: hero,
      title: stars === 3 ? "Cyber City champion" : stars === 2 ? "Speedy runner" : "A good first run: try again to win more diamonds",
      rows: [[art("run"), "Right answers", G.right + " of " + n + " gates", ""],
             [GEM, "Diamonds picked up", plural(G.picked, "diamond") + (G.lost ? ", " + fmt(G.lost) + " points lost to bumps" : ""), ""],
             [FLAME, "Best streak", plural(G.bestStreak, "right answer") + " in a row", ""]],
      medals: medals,
      extra: missed.length ? reviewList("The ones to look at again", missed) : null,
      summary: G.right + " of " + n + " gates right, with " + plural(G.picked, "diamond") + " picked up."
    });
    stage.classList.remove("is-running");
  }
  hooks.runDeal = function () { return runDeal(); };
  hooks.runWorld = function () { return G && G.world; };
  hooks.runRead = function (q) { return runRead(q); };

  hooks.oddDeal = function () { return oddDeal(); };
  hooks.fibDeal = function () { return fibDeal(); };

  hooks.data = D;
  hooks.state = function () { return G; };
})();
