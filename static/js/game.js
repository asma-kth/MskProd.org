/* Pixel Run: a platformer where every obstacle is a Python function to write.

   The page ships the levels, the challenges and the tests as JSON. Python runs
   in the student's own browser (Pyodide), so nothing they type is ever sent
   anywhere. The drawing lives in game-art.js. */
(function () {
  "use strict";

  var root = document.getElementById("pixelrun");
  var dataEl = document.getElementById("pr-data");
  if (!root || !dataEl || !window.PixelArt) return;

  var DATA;
  try { DATA = JSON.parse(dataEl.textContent); } catch (e) { return; }

  var A = window.PixelArt;
  var LV = DATA.levels, CH = DATA.challenges;
  var TOP = LV.length;
  var pool = {};
  CH.forEach(function (c) { (pool[c.level] = pool[c.level] || []).push(c); });

  var SPEED = 250;           // world pixels per second while running
  var SCREEN_X = 170;        // where Pixel stands on screen
  var STAND = 112;           // how far short of an obstacle she waits
  var ATTEMPTS = 3, QUIZ_ATTEMPTS = 2;

  /* --------------------------------------------------------------- helpers */
  function h(tag, attrs, kids) {
    var n = document.createElement(tag);
    var k;
    if (attrs) {
      for (k in attrs) {
        if (!Object.prototype.hasOwnProperty.call(attrs, k)) continue;
        var v = attrs[k];
        if (v === false || v === null || v === undefined) continue;
        if (k === "class") n.className = v;
        else if (k === "html") n.innerHTML = v;       // only ever build-time text
        else if (k.slice(0, 2) === "on") n.addEventListener(k.slice(2), v);
        else n.setAttribute(k, v === true ? "" : v);
      }
    }
    (function add(list) {
      if (list === undefined || list === null || list === false) return;
      if (Array.isArray(list)) { list.forEach(add); return; }
      n.appendChild(typeof list === "object" ? list : document.createTextNode(String(list)));
    })(kids);
    return n;
  }
  function $(sel) { return root.querySelector(sel); }
  function clamp(v, a, b) { return Math.max(a, Math.min(b, v)); }
  function stars(n, of) {
    var s = "";
    for (var i = 0; i < (of || 3); i++) s += i < n ? "★" : "☆";
    return h("span", { class: "pr-starline", "aria-label": n + " out of " + (of || 3) + " stars" }, s);
  }

  var mqReduce = window.matchMedia ? window.matchMedia("(prefers-reduced-motion: reduce)") : null;

  /* --------------------------------------------------------------- storage */
  var store = window.MskStore || { get: function (k, d) { return d; }, set: function () {}, del: function () {} };
  var P;
  function freshProgress() {
    return { best: 1, resume: 0, stars: {}, seen: {}, last: {}, solved: {}, tick: 0, runs: 0, wins: 0, quiz: false, calm: null };
  }
  (function () {
    var s = store.get("pixelrun", null);
    P = freshProgress();
    if (s && typeof s === "object") {
      ["stars", "seen", "last", "solved"].forEach(function (k) { if (s[k] && typeof s[k] === "object") P[k] = s[k]; });
      ["best", "resume", "tick", "runs", "wins"].forEach(function (k) { if (typeof s[k] === "number") P[k] = s[k]; });
      P.quiz = !!s.quiz;
      P.calm = typeof s.calm === "boolean" ? s.calm : null;
    }
  })();
  function save() { store.set("pixelrun", P); }
  function calm() { return P.calm === null ? !!(mqReduce && mqReduce.matches) : P.calm; }
  function totalStars() { var n = 0; for (var k in P.stars) n += P.stars[k]; return n; }
  function solvedCount() { return Object.keys(P.solved).length; }

  /* ----------------------------------------------------------------- state */
  var S = {
    phase: "title",           // title intro run wait jump bonk flag over
    level: 1, picks: [], idx: 0,
    wx: 60, t: 0, fade: 0,
    obstacles: [], pits: [], coins: [], flagX: 0, coinCount: 0,
    particles: [], anim: null, bubble: false,
    pix: { h: 0, rot: 0, sx: 1, sy: 1, run: false, idle: true, dizzy: false },
    att: ATTEMPTS, wrong: 0, hints: 0, busy: false,
    levelStars: {}, fails: {}, runCoins: 0,
    ch: null
  };
  var dirty = true, last = 0, idleAcc = 0;

  /* ---------------------------------------------------------- the console */
  var con = $("#pr-console");
  var liveEl = $("#pr-live");
  var canvas = $("#pr-canvas");
  var spriteImg = new Image();
  spriteImg.src = "data:image/svg+xml;charset=utf-8," + encodeURIComponent(DATA.sprite);
  spriteImg.onload = function () { dirty = true; };
  var art = A.make(canvas, spriteImg);

  function say(msg) {
    liveEl.textContent = "";
    setTimeout(function () { liveEl.textContent = msg; }, 60);
  }

  function show(card, focusSel, quiet) {
    while (con.firstChild) con.removeChild(con.firstChild);
    con.appendChild(card);
    if (quiet) return;
    var f = focusSel ? card.querySelector(focusSel) : null;
    var touch = window.matchMedia && window.matchMedia("(pointer: coarse)").matches;
    if (f && !(touch && f.tagName === "TEXTAREA")) {
      try { f.focus({ preventScroll: true }); } catch (e) { f.focus(); }
    }
    var r = con.getBoundingClientRect();
    if (r.top > window.innerHeight - 140 || r.top < -20) {
      try { con.scrollIntoView({ block: "nearest", behavior: calm() ? "auto" : "smooth" }); } catch (e) { con.scrollIntoView(); }
    }
  }

  /* ----------------------------------------------------------------- hud */
  function hud() {
    var lv = LV[S.level - 1];
    $("#pr-level").textContent = "Level " + S.level + " of " + TOP;
    $("#pr-name").textContent = lv.name;
    var pips = $("#pr-pips").children, done = 0;
    for (var i = 0; i < 3; i++) {
      var st = S.obstacles[i] ? S.obstacles[i].state : "open";
      if (st === "ok") done++;
      pips[i].className = st === "ok" ? "on" : st === "bad" ? "bad" : (i === S.idx && (S.phase === "wait" || S.phase === "run" || S.phase === "jump") ? "now" : "");
    }
    $("#pr-pips").setAttribute("aria-label", "Obstacles cleared: " + done + " of 3");
    $("#pr-stars b").textContent = String(runStarTotal());
    $("#pr-coins b").textContent = String(S.runCoins);
    var calmBtn = $("#pr-calm");
    calmBtn.setAttribute("aria-pressed", calm() ? "true" : "false");
    calmBtn.textContent = "Calm mode";
    calmBtn.appendChild(h("span", { "aria-hidden": "true" }, calm() ? ": on" : ": off"));
    setPyChip();
  }
  function runStarTotal() { var n = 0; for (var k in S.levelStars) n += S.levelStars[k]; return n; }

  function setPyChip() {
    var chip = $("#pr-py");
    var txt = P.quiz ? "Quiz mode" : PY.state === "ready" ? "Python: ready" : PY.state === "loading" ? "Python: loading" : PY.state === "failed" ? "Python: unavailable" : "Python: not loaded";
    chip.textContent = txt;
    chip.setAttribute("data-state", P.quiz ? "quiz" : PY.state);
  }

  /* ---------------------------------------------------------------- python */
  var SOURCES = [
    "https://cdn.jsdelivr.net/pyodide/v314.0.6/full/pyodide.js",
    "https://cdn.jsdelivr.net/pyodide/v0.28.3/full/pyodide.js",
    "https://cdn.jsdelivr.net/npm/pyodide/pyodide.js"
  ];
  var PY = { state: "idle", py: null, p: null };

  function loadScript(src) {
    return new Promise(function (resolve, reject) {
      var s = document.createElement("script");
      var timer = setTimeout(function () { s.remove(); reject(new Error("timed out: " + src)); }, 25000);
      s.src = src;
      s.onload = function () { clearTimeout(timer); resolve(); };
      s.onerror = function () { clearTimeout(timer); reject(new Error("could not load " + src)); };
      document.head.appendChild(s);
    });
  }

  function bootPython() {
    if (PY.state === "ready") return Promise.resolve(PY.py);
    if (PY.p) return PY.p;
    PY.state = "loading";
    setPyChip();
    var first = window.loadPyodide ? Promise.resolve() : SOURCES.reduce(function (chain, url) {
      return chain.catch(function () { return loadScript(url); });
    }, Promise.reject());
    PY.p = first.then(function () {
      return Promise.race([
        window.loadPyodide(),
        new Promise(function (_, rej) { setTimeout(function () { rej(new Error("python start timed out")); }, 90000); })
      ]);
    }).then(function (py) {
      py.runPython(DATA.harness);
      PY.py = py; PY.state = "ready"; setPyChip();
      if (S.ch && S.phase === "wait") refreshRunButton();
      return py;
    }).catch(function (err) {
      PY.state = "failed"; PY.p = null; setPyChip();
      if (S.ch && S.phase === "wait") offerQuiz();
      throw err;
    });
    PY.p.catch(function () {});
    return PY.p;
  }

  function mark(ch, code) {
    var py = PY.py;
    py.setStdout({ batched: function () {} });
    py.setStderr({ batched: function () {} });
    py.globals.set("__pr_src", code);
    py.globals.set("__pr_fn", ch.fn);
    py.globals.set("__pr_tests", JSON.stringify(ch.tests));
    py.globals.set("__pr_rules", JSON.stringify(ch.rules));
    var out;
    try { out = py.runPython("__game_check(__pr_src, __pr_fn, __pr_tests, __pr_rules)"); }
    finally { py.setStdout({}); py.setStderr({}); }
    return JSON.parse(out);
  }

  /* ------------------------------------------------------------ animation */
  function startAnim(dur, fn, done) {
    S.anim = { t: 0, dur: Math.max(0.001, dur), fn: fn, done: done };
    dirty = true;
  }
  function cut(apply, done) {
    var applied = false;
    startAnim(0.34, function (u) {
      S.fade = u < 0.5 ? u * 2 : 2 - u * 2;
      if (u >= 0.5 && !applied) { applied = true; apply(); }
    }, function () { S.fade = 0; if (!applied) apply(); done(); });
  }
  function emit(kind, x, y, n, o) {
    if (calm()) return;
    o = o || {};
    for (var i = 0; i < n; i++) {
      var a = Math.random() * 6.2832, sp = (o.speed || 60) * (0.4 + Math.random());
      S.particles.push({
        kind: kind, x: x + (Math.random() - 0.5) * (o.spread || 0), y: y,
        vx: o.dir !== undefined ? o.dir * sp : Math.cos(a) * sp, vy: o.up ? -Math.abs(Math.sin(a)) * sp - 20 : Math.sin(a) * sp,
        age: 0, life: o.life || 0.6, size: o.size || 4,
        color: o.colors ? o.colors[i % o.colors.length] : "#ffd23d", g: o.g === undefined ? 0 : o.g
      });
    }
  }
  function squash() { S.pix.sx = 1.22; S.pix.sy = 0.78; }

  function playSegs(segs, done) {
    var i = 0;
    (function next() {
      if (i >= segs.length) { done(); return; }
      var g = segs[i++];
      startAnim(g.dur, function (u) {
        S.wx = g.x0 + (g.x1 - g.x0) * u;
        S.pix.h = g.h0 + (g.h1 - g.h0) * u + 4 * (g.peak || 0) * u * (1 - u);
        S.pix.rot = g.peak ? (u - 0.5) * 0.5 * (g.x1 >= g.x0 ? 1 : -1) : 0;
      }, function () {
        S.pix.rot = 0; S.pix.h = g.h1;
        if (g.land) { squash(); emit("dust", S.wx, A.GROUND - S.pix.h, 6, { speed: 40, up: true, life: 0.5, size: 3 }); }
        next();
      });
    })();
  }

  function collect(x0, x1) {
    var lo = Math.min(x0, x1), hi = Math.max(x0, x1);
    S.coins.forEach(function (c) {
      if (!c.got && c.x >= lo && c.x <= hi) { c.got = true; S.runCoins++; }
    });
    $("#pr-coins b").textContent = String(S.runCoins);
  }

  function runTo(x, done) {
    var from = S.wx;
    if (calm()) { cut(function () { collect(from, x); S.wx = x; }, done); return; }
    var dur = Math.abs(x - from) / SPEED;
    S.pix.run = true; S.pix.idle = false;
    startAnim(dur, function (u) { S.wx = from + (x - from) * u; }, function () {
      S.pix.run = false; S.pix.idle = true; done();
    });
  }

  function jumpOver(ob, done) {
    var def = A.OB[ob.kind], x0 = S.wx, landX = ob.x + ob.w + 96;
    S.pix.run = false; S.pix.idle = false;
    if (calm()) { cut(function () { collect(x0, landX); S.wx = landX; }, done); return; }
    var segs;
    if (def.hop) {
      var topX = ob.x + ob.w / 2;
      segs = [
        { dur: 0.52, x0: x0, x1: topX, h0: 0, h1: def.h, peak: 50, land: true },
        { dur: 0.14, x0: topX, x1: topX, h0: def.h, h1: def.h, peak: 0 },
        { dur: 0.5, x0: topX, x1: landX, h0: def.h, h1: 0, peak: 36, land: true }
      ];
    } else {
      segs = [{ dur: 0.95, x0: x0, x1: landX, h0: 0, h1: 0, peak: Math.max(def.h + 56, 100), land: true }];
    }
    playSegs(segs, function () { S.pix.idle = true; done(); });
  }

  function bonkAt(ob, done) {
    var def = A.OB[ob.kind], pit = ob.kind === "gap" || ob.kind === "lava";
    S.pix.idle = false;
    if (calm()) { cut(function () { S.wx = ob.x - STAND; S.pix.dizzy = true; }, done); return; }
    S.pix.run = true;
    var x0 = S.wx, hit = pit ? ob.x - 6 : ob.x - 30;
    startAnim(Math.abs(hit - x0) / SPEED, function (u) { S.wx = x0 + (hit - x0) * u; }, function () {
      S.pix.run = false;
      if (pit) {
        startAnim(0.9, function (u) {
          S.wx = hit + 26 * u; S.pix.h = -170 * u * u; S.pix.rot = u * 3.4; S.pix.alpha = 1 - u;
        }, function () { S.pix.alpha = 1; S.pix.rot = 0; S.pix.h = 0; S.wx = ob.x - STAND; S.pix.dizzy = true; done(); });
      } else {
        emit("star", S.wx + 18, A.GROUND - 40, 6, { speed: 90, up: true, life: 0.7, size: 5, g: 160 });
        playSegs([{ dur: 0.55, x0: hit, x1: ob.x - STAND, h0: 0, h1: 0, peak: 64, land: true }], function () {
          S.pix.dizzy = true; done();
        });
      }
    });
  }

  function celebrate(done) {
    S.pix.run = false; S.pix.idle = false;
    emit("conf", S.wx, A.GROUND - 120, 46, { speed: 150, up: true, life: 1.6, size: 6, g: 260, spread: 40, colors: ["#ff6b8b", "#ffd23d", "#46b873", "#4fb3ff", "#c79bff"] });
    if (calm()) { done(); return; }
    var x = S.wx;
    playSegs([
      { dur: 0.34, x0: x, x1: x, h0: 0, h1: 0, peak: 44, land: true },
      { dur: 0.34, x0: x, x1: x, h0: 0, h1: 0, peak: 44, land: true },
      { dur: 0.4, x0: x, x1: x, h0: 0, h1: 0, peak: 58, land: true }
    ], function () { S.pix.idle = true; done(); });
  }

  /* --------------------------------------------------------------- update */
  function update(dt) {
    if (S.anim) {
      var a = S.anim;
      a.t += dt;
      var u = clamp(a.t / a.dur, 0, 1);
      a.fn(u);
      if (u >= 1) { S.anim = null; a.done(); }
    }
    var p = S.pix;
    var k = Math.min(1, dt * 12);
    p.sx += (1 - p.sx) * k; p.sy += (1 - p.sy) * k;
    if (p.alpha === undefined) p.alpha = 1;

    if (!calm()) {
      if (p.run && Math.random() < dt * 14) {
        S.particles.push({ kind: "dust", x: S.wx - 14, y: A.GROUND - 3, vx: -30, vy: -14, age: 0, life: 0.45, size: 3, color: "#fff", g: 0 });
      }
      for (var i = 0; i < S.coins.length; i++) {
        var c = S.coins[i];
        if (!c.got && Math.abs(c.x - S.wx) < 26 && p.h < c.y + 26) {
          c.got = true; S.runCoins++; S.coinCount++;
          emit("star", c.x, A.GROUND - c.y, 4, { speed: 70, up: true, life: 0.45, size: 3 });
          $("#pr-coins b").textContent = String(S.runCoins);
        }
      }
      for (var j = 0; j < S.particles.length; j++) {
        var q = S.particles[j];
        q.age += dt; q.x += q.vx * dt; q.y += q.vy * dt; q.vy += q.g * dt;
      }
      S.particles = S.particles.filter(function (q) { return q.age < q.life; });
    } else if (S.particles.length) {
      S.particles = [];
    }
    for (var m = 0; m < S.pits.length; m++) S.pits[m].t = S.t;
  }

  function render() {
    var cam = Math.max(0, S.wx - SCREEN_X);
    art.draw({
      t: S.t, cam: cam, palette: LV[S.level - 1].palette, calm: calm(),
      obstacles: S.obstacles, pits: S.pits, coins: S.coins, flagX: S.flagX,
      particles: S.particles, fade: S.fade, bubble: S.bubble && S.phase === "wait",
      pixel: { x: S.wx, h: S.pix.h, rot: S.pix.rot, sx: S.pix.sx, sy: S.pix.sy, run: S.pix.run, idle: S.pix.idle && !calm(), dizzy: S.pix.dizzy, alpha: S.pix.alpha }
    });
  }

  function frame(now) {
    requestAnimationFrame(frame);
    var dt = last ? Math.min(0.05, (now - last) / 1000) : 0.016;
    last = now;
    if (document.hidden) return;
    var live = !calm() || S.anim;
    if (!live && !dirty) return;
    if (S.phase === "wait" && !S.anim && !calm()) {
      idleAcc += dt;
      if (idleAcc < 0.066 && !dirty) return;
      dt = idleAcc; idleAcc = 0;
    }
    S.t += dt;
    update(dt);
    render();
    dirty = false;
  }

  /* ---------------------------------------------------------------- levels */
  function deal(level) {
    var list = pool[level].map(function (c, i) { return { c: c, i: i }; });
    list.sort(function (a, b) {
      var sa = P.seen[a.c.id] || 0, sb = P.seen[b.c.id] || 0;
      if (sa !== sb) return sa - sb;
      var va = P.solved[a.c.id] ? 1 : 0, vb = P.solved[b.c.id] ? 1 : 0;
      if (va !== vb) return va - vb;
      var la = P.last[a.c.id] || 0, lb = P.last[b.c.id] || 0;
      if (la !== lb) return la - lb;
      return a.i - b.i;
    });
    return list.slice(0, 3).sort(function (a, b) { return a.i - b.i; }).map(function (x) { return x.c; });
  }

  function buildWorld(n) {
    var lv = LV[n - 1];
    S.obstacles = []; S.pits = []; S.coins = [];
    for (var i = 0; i < 3; i++) {
      var kind = lv.obstacles[i], def = A.OB[kind], x = 660 + i * 650;
      S.obstacles.push({ x: x, kind: kind, w: def.w, h: def.h, state: "open" });
      if (kind === "gap" || kind === "lava") S.pits.push({ x: x, w: def.w, lava: kind === "lava", t: 0 });
      var start = i === 0 ? 250 : S.obstacles[i - 1].x + S.obstacles[i - 1].w + 190;
      var count = i === 0 ? 3 : 5;
      for (var k = 0; k < count; k++) S.coins.push({ x: start + k * 36, y: 34 + (k === 2 ? 12 : 0), got: false });
    }
    var lastOb = S.obstacles[2];
    S.flagX = lastOb.x + lastOb.w + 560;
    S.wx = 60; S.particles = []; S.fade = 0; S.anim = null;
    S.pix = { h: 0, rot: 0, sx: 1, sy: 1, run: false, idle: true, dizzy: false, alpha: 1 };
  }

  function startLevel(n) {
    S.level = n; S.picks = deal(n); S.idx = 0; S.phase = "intro"; S.ch = null; S.bubble = false;
    S.levelStars[n] = 0;
    buildWorld(n);
    P.best = Math.max(P.best, n); P.resume = n; save();
    hud(); dirty = true;
    var lv = LV[n - 1];
    say("Level " + n + ", " + lv.name + ". " + lv.concept + ".");
    var revise = lv.revise.map(function (r) {
      return h("a", { href: r[1], target: "_blank", rel: "noopener" }, [r[0], h("span", { class: "sr-only" }, " (opens in a new tab)")]);
    });
    var links = [];
    revise.forEach(function (a, i) { if (i) links.push(", "); links.push(a); });
    show(h("div", { class: "pr-card pr-levelcard" }, [
      h("p", { class: "pr-kicker" }, "Level " + n + " of " + TOP + " · " + lv.stage),
      h("h3", null, lv.name),
      h("p", { class: "pr-concept" }, lv.concept),
      h("p", null, lv.blurb),
      h("p", { class: "pr-revise" }, ["Revise first: "].concat(links)),
      h("div", { class: "pr-actions" }, [
        h("button", { class: "btn btn-primary", type: "button", "data-act": "go" }, "Run!")
      ])
    ]), "[data-act=go]");
    bootIfWanted();
  }

  function bootIfWanted() {
    if (!P.quiz && PY.state === "idle") bootPython();
  }

  function go() {
    S.phase = "run";
    runTo(S.obstacles[S.idx].x - STAND, arrive);
    hud();
  }

  function arrive() {
    S.phase = "wait"; S.bubble = true; S.pix.dizzy = false;
    openChallenge();
    hud(); dirty = true;
  }

  /* ------------------------------------------------------------- challenge */
  var editor = null;

  function exampleLine(t) {
    return h("li", null, [h("code", null, t.c), " returns ", h("code", null, t.e)]);
  }

  function openChallenge() {
    var ch = S.picks[S.idx];
    S.ch = ch; S.wrong = 0; S.hints = 0; S.busy = false;
    S.att = P.quiz ? QUIZ_ATTEMPTS : ATTEMPTS;
    P.seen[ch.id] = (P.seen[ch.id] || 0) + 1;
    P.tick += 1; P.last[ch.id] = P.tick; save();
    say("Obstacle " + (S.idx + 1) + " of 3: " + ch.title + ". " + ch.tasktext);
    if (P.quiz) openQuiz(ch); else openCode(ch);
  }

  function attemptsView() {
    var dots = [], total = P.quiz || PY.state === "failed" ? QUIZ_ATTEMPTS : ATTEMPTS;
    for (var i = 0; i < total; i++) dots.push(h("i", { class: i < S.att ? "on" : "" }));
    return h("p", { class: "pr-attempts", id: "pr-attempts" }, [
      "Attempts left: ", h("span", { class: "pr-dots", "aria-hidden": "true" }, dots), " " + S.att
    ]);
  }

  function head(ch) {
    var lv = LV[S.level - 1];
    return [
      h("p", { class: "pr-kicker" }, "Level " + S.level + " · " + lv.name + " · obstacle " + (S.idx + 1) + " of 3"),
      h("h3", null, ch.title)
    ];
  }

  function openCode(ch) {
    var examples = ch.tests.slice(0, 2).map(exampleLine);
    editor = h("textarea", {
      class: "pr-editor", id: "pr-editor", rows: String(Math.min(16, ch.starter.split("\n").length + 4)),
      spellcheck: "false", autocapitalize: "off", autocorrect: "off", autocomplete: "off", wrap: "off",
      "aria-describedby": "pr-edtip"
    });
    editor.value = ch.starter;
    wireEditor(editor);
    var card = h("div", { class: "pr-card pr-challenge", "data-challenge": ch.id }, [
      head(ch),
      h("div", { class: "pr-grid" }, [
        h("div", { class: "pr-brief" }, [
          h("p", { class: "pr-story", html: ch.story }),
          h("p", { class: "pr-task", html: ch.task }),
          h("h4", null, "Examples"),
          h("ul", { class: "pr-examples" }, examples),
          h("div", { class: "pr-hints", id: "pr-hints", "aria-live": "polite" })
        ]),
        h("div", { class: "pr-codepane" }, [
          h("label", { class: "tool-label", for: "pr-editor" }, "Your code"),
          editor,
          h("p", { class: "pr-edtip", id: "pr-edtip" }, "Tab indents. To leave the box with the keyboard, press Esc and then Tab. Ctrl+Enter runs the tests."),
          h("button", { class: "tool-btn pr-tabbtn", type: "button", "data-act": "tab", onpointerdown: function (e) { e.preventDefault(); } }, "Indent"),
          h("div", { class: "pr-actions", id: "pr-actions" }, [
            h("button", { class: "btn btn-primary", type: "button", id: "pr-run", "data-act": "run" }, "Run tests"),
            h("button", { class: "tool-btn", type: "button", id: "pr-hint", "data-act": "hint" }, "Hint (" + ch.hints.length + " left, costs a star)"),
            h("button", { class: "tool-btn", type: "button", "data-act": "reset-code" }, "Reset code"),
            h("button", { class: "tool-btn", type: "button", "data-act": "giveup" }, "Give up")
          ]),
          attemptsView(),
          h("div", { class: "pr-results", id: "pr-results", role: "status", "aria-live": "polite" })
        ])
      ])
    ]);
    show(card, "#pr-editor");
    refreshRunButton();
    if (PY.state === "idle") bootPython().catch(function () {});
    if (PY.state === "failed") offerQuiz();
  }

  function refreshRunButton() {
    var b = $("#pr-run");
    if (!b) return;
    if (PY.state === "ready") {
      b.disabled = false; b.textContent = "Run tests";
      var offer = $("#pr-results[data-kind=py]");
      if (offer) { clear(offer); offer.className = "pr-results"; offer.removeAttribute("data-kind"); }
    }
    else if (PY.state === "failed") { b.disabled = true; b.textContent = "Python unavailable"; }
    else { b.disabled = true; b.textContent = "Loading Python..."; }
  }

  function offerQuiz() {
    var box = $("#pr-results");
    if (!box) return;
    clear(box);
    box.className = "pr-results is-warn";
    box.setAttribute("data-kind", "py");
    box.appendChild(h("p", null, "Python could not be loaded. That usually means a school network or an ad blocker is stopping the download. You can keep playing in quiz mode: read the code and choose what it returns."));
    box.appendChild(h("div", { class: "pr-actions" }, [
      h("button", { class: "btn btn-primary", type: "button", "data-act": "to-quiz" }, "Switch to quiz mode"),
      h("button", { class: "tool-btn", type: "button", "data-act": "retry-py" }, "Try loading Python again")
    ]));
    refreshRunButton();
  }

  function clear(n) { while (n.firstChild) n.removeChild(n.firstChild); }

  function wireEditor(ta) {
    var trap = true;
    ta.addEventListener("keydown", function (e) {
      if (e.key === "Escape") { trap = false; return; }
      if ((e.ctrlKey || e.metaKey) && e.key === "Enter") { e.preventDefault(); runTests(); return; }
      if (e.key === "Tab" && trap && !e.ctrlKey && !e.metaKey && !e.altKey) {
        e.preventDefault();
        indent(ta, e.shiftKey);
        return;
      }
      if (e.key === "Enter" && !e.shiftKey && !e.ctrlKey && !e.metaKey && !e.altKey) {
        var v = ta.value, s = ta.selectionStart;
        var lineStart = v.lastIndexOf("\n", s - 1) + 1;
        var line = v.slice(lineStart, s);
        var ind = /^[ \t]*/.exec(line)[0];
        if (/:\s*$/.test(line)) ind += "    ";
        e.preventDefault();
        insert(ta, "\n" + ind);
        return;
      }
      if (e.key === "Backspace" && ta.selectionStart === ta.selectionEnd) {
        var p = ta.selectionStart, ls = ta.value.lastIndexOf("\n", p - 1) + 1;
        var before = ta.value.slice(ls, p);
        if (before.length >= 4 && /^ +$/.test(before) && before.length % 4 === 0) {
          e.preventDefault();
          ta.setSelectionRange(p - 4, p);
          insert(ta, "");
        }
        return;
      }
      trap = true;
    });
    ta.addEventListener("blur", function () { trap = true; });
  }

  function insert(ta, text) {
    var ok = false;
    try { ok = document.execCommand("insertText", false, text); } catch (e) { ok = false; }
    if (!ok) {
      ta.setRangeText(text, ta.selectionStart, ta.selectionEnd, "end");
      ta.dispatchEvent(new Event("input", { bubbles: true }));
    }
  }

  function indent(ta, back) {
    var v = ta.value, s = ta.selectionStart, e = ta.selectionEnd;
    if (s === e && !back) { insert(ta, "    "); return; }
    var ls = v.lastIndexOf("\n", s - 1) + 1;
    var block = v.slice(ls, e);
    var out = back
      ? block.replace(/^( {1,4}|\t)/gm, "")
      : block.replace(/^/gm, "    ");
    ta.setSelectionRange(ls, e);
    insert(ta, out);
    ta.setSelectionRange(ls, ls + out.length);
  }

  /* ---------------------------------------------------------- run the tests */
  function runTests() {
    if (S.phase !== "wait" || S.busy || !S.ch || !editor) return;
    if (PY.state !== "ready") return;
    var ch = S.ch;
    // phone keyboards sometimes swap in curly quotes and hard spaces, which Python cannot read
    var code = editor.value.replace(/[\u201c\u201d]/g, '"').replace(/[\u2018\u2019]/g, "'").replace(/\u00a0/g, " ");
    S.busy = true;
    var run = $("#pr-run");
    if (run) { run.disabled = true; run.textContent = "Running..."; }
    setTimeout(function () {
      var res;
      try { res = mark(ch, code); } catch (err) { res = { phase: "crash", message: String(err && err.message || err) }; }
      S.busy = false;
      if (run) { run.disabled = false; run.textContent = "Run tests"; }
      afterMark(ch, res);
    }, 40);
  }

  function resultRow(r, detail) {
    var ok = r.ok;
    var kids = [h("span", { class: "pr-tick" }, ok ? "Pass" : "Fail"), " ", h("code", null, r.call)];
    if (!ok && detail) {
      kids.push(h("span", { class: "pr-detail" }, [
        "expected ", h("code", null, r.expected), ", got ", h("code", null, r.got)
      ]));
    }
    return h("li", { class: ok ? "is-pass" : "is-fail" }, kids);
  }

  function afterMark(ch, res) {
    var box = $("#pr-results");
    if (!box) return;
    clear(box);
    box.removeAttribute("data-kind");
    if (res.phase !== "tests") {
      box.className = "pr-results is-warn";
      box.appendChild(h("p", { class: "pr-msg" }, [h("strong", null, "Your code did not run. "), res.message || "Something went wrong."]));
      box.appendChild(h("p", { class: "pr-sub" }, "That did not use up an attempt."));
      return;
    }
    var rows = res.results, passed = rows.filter(function (r) { return r.ok; }).length;
    var allOk = passed === rows.length;
    if (allOk && !res.rule) { solved(ch, rows); return; }

    S.wrong++; S.att--;
    box.className = "pr-results is-bad";
    var summary = allOk
      ? "All " + rows.length + " answers are right, but a rule was broken."
      : passed + " of " + rows.length + " tests passed.";
    box.appendChild(h("p", { class: "pr-msg" }, [h("strong", null, summary)]));
    if (res.rule) box.appendChild(h("p", { class: "pr-msg" }, res.rule));
    var shown = 0, list = h("ul", { class: "pr-tests" });
    rows.forEach(function (r) {
      var detail = !r.ok && shown < 2;
      if (!r.ok) shown++;
      list.appendChild(resultRow(r, detail));
    });
    box.appendChild(list);
    var att = $("#pr-attempts");
    if (att) att.parentNode.replaceChild(attemptsView(), att);
    if (S.att <= 0) {
      box.appendChild(h("p", { class: "pr-msg" }, h("strong", null, "That was your last attempt.")));
      box.appendChild(h("div", { class: "pr-actions" }, [
        h("button", { class: "btn btn-primary", type: "button", "data-act": "lose" }, "See the solution")
      ]));
      lockEditor();
      var b = box.querySelector("[data-act=lose]");
      if (b) b.focus();
    }
  }

  function lockEditor() {
    if (editor) editor.readOnly = true;
    ["run", "hint", "reset-code", "giveup"].forEach(function (a) {
      var b = con.querySelector("[data-act=" + a + "]");
      if (b) b.disabled = true;
    });
  }

  function giveHint() {
    var ch = S.ch, box = $("#pr-hints");
    if (!ch || !box || S.hints >= ch.hints.length) return;
    box.appendChild(h("p", { class: "pr-hint" }, [h("strong", null, "Hint " + (S.hints + 1) + ": "), h("span", { html: ch.hints[S.hints] })]));
    S.hints++;
    var b = $("#pr-hint");
    if (S.hints >= ch.hints.length) { b.disabled = true; b.textContent = "No more hints"; }
    else b.textContent = "Hint (" + (ch.hints.length - S.hints) + " left, costs a star)";
  }

  function confirmGiveUp() {
    var acts = $("#pr-actions");
    if (!acts) return;
    var prev = Math.max(1, S.level - 1);
    clear(acts);
    acts.appendChild(h("p", { class: "pr-msg" }, "Give up? You will see the solution, then go back to " + (S.level > 1 ? "level " + prev : "the start of level 1") + "."));
    acts.appendChild(h("button", { class: "btn btn-primary", type: "button", "data-act": "lose" }, "Yes, show me the solution"));
    acts.appendChild(h("button", { class: "tool-btn", type: "button", "data-act": "keep-going" }, "No, keep trying"));
    var no = acts.querySelector("[data-act=keep-going]");
    if (no) no.focus();
  }

  /* ----------------------------------------------------------------- quiz */
  function openQuiz(ch) {
    var fb = ch.fb;
    var opts = fb.options.map(function (o, i) {
      return h("button", { class: "pr-opt", type: "button", "data-act": "pick", "data-i": String(i) }, [
        h("span", { class: "pr-optkey" }, "ABCD".charAt(i)), h("code", null, o)
      ]);
    });
    var card = h("div", { class: "pr-card pr-challenge pr-quiz", "data-challenge": ch.id }, [
      head(ch),
      h("div", { class: "pr-grid" }, [
        h("div", { class: "pr-brief" }, [
          h("p", { class: "pr-story", html: ch.story }),
          h("p", { class: "pr-task", html: ch.task })
        ]),
        h("div", { class: "pr-codepane" }, [
          h("p", { class: "tool-label" }, "Read this function"),
          h("pre", { class: "pr-solution" }, h("code", null, ch.solution)),
          h("p", { class: "pr-q" }, ["What does ", h("code", null, fb.call), " return?"]),
          h("div", { class: "pr-opts", role: "group", "aria-label": "Choose the answer" }, opts),
          attemptsView(),
          h("div", { class: "pr-results", id: "pr-results", role: "status", "aria-live": "polite" }),
          h("div", { class: "pr-actions", id: "pr-actions" }, [
            h("button", { class: "tool-btn", type: "button", "data-act": "giveup" }, "Give up")
          ])
        ])
      ])
    ]);
    show(card, ".pr-opt");
  }

  function pick(i) {
    var ch = S.ch, fb = ch.fb, box = $("#pr-results");
    if (S.att <= 0) return;
    clear(box);
    if (i === fb.answer) { solved(ch, null); return; }
    S.wrong++; S.att--;
    box.className = "pr-results is-bad";
    box.appendChild(h("p", { class: "pr-msg" }, [h("strong", null, "Not quite. "), "Trace the code again with that input, line by line."]));
    var att = $("#pr-attempts");
    if (att) att.parentNode.replaceChild(attemptsView(), att);
    var b = con.querySelector("[data-i='" + i + "']");
    if (b) { b.disabled = true; b.classList.add("is-wrong"); }
    if (S.att <= 0) {
      Array.prototype.forEach.call(con.querySelectorAll(".pr-opt"), function (o) { o.disabled = true; });
      box.appendChild(h("div", { class: "pr-actions" }, [
        h("button", { class: "btn btn-primary", type: "button", "data-act": "lose" }, "See the answer")
      ]));
      var l = box.querySelector("[data-act=lose]");
      if (l) l.focus();
    }
  }

  /* ----------------------------------------------------------- solve / lose */
  function solved(ch, rows) {
    var earned = Math.max(1, 3 - S.wrong - S.hints);
    P.solved[ch.id] = 1;
    P.stars[ch.id] = Math.max(P.stars[ch.id] || 0, earned);
    S.levelStars[S.level] = (S.levelStars[S.level] || 0) + earned;
    S.obstacles[S.idx].state = "ok"; S.bubble = false;
    save(); hud(); dirty = true;
    say("Correct. " + earned + (earned === 1 ? " star." : " stars.") + " Pixel is ready to jump.");
    emit("star", S.wx + 10, A.GROUND - 60, 10, { speed: 110, up: true, life: 0.8, size: 5, g: 140 });
    var kids = [
      h("p", { class: "pr-kicker pr-good" }, "Obstacle " + (S.idx + 1) + " of 3 cleared"),
      h("h3", null, rows ? "All " + rows.length + " tests passed" : "Right answer"),
      h("p", { class: "pr-stars-big" }, [stars(earned), " ", earned + (earned === 1 ? " star" : " stars")]),
      h("details", { class: "pr-model" }, [
        h("summary", null, "Compare with the model solution"),
        h("pre", { class: "pr-solution" }, h("code", null, ch.solution))
      ]),
      h("div", { class: "pr-actions" }, [
        h("button", { class: "btn btn-primary", type: "button", "data-act": "jump" }, "Jump!")
      ])
    ];
    show(h("div", { class: "pr-card pr-passcard" }, kids), "[data-act=jump]");
  }

  function jump() {
    var ob = S.obstacles[S.idx];
    S.phase = "jump"; S.ch = null; editor = null;
    show(h("div", { class: "pr-card pr-status" }, [h("p", null, "Pixel jumps the obstacle...")]));
    jumpOver(ob, function () {
      if (S.idx < 2) {
        S.idx++; S.phase = "run"; hud();
        runTo(S.obstacles[S.idx].x - STAND, arrive);
      } else {
        S.phase = "flag"; hud();
        runTo(S.flagX - 30, function () { celebrate(levelDone); });
      }
    });
  }

  function lose() {
    var ch = S.ch, ob = S.obstacles[S.idx];
    if (!ch) return;
    S.phase = "bonk"; S.bubble = false; ob.state = "bad";
    S.fails[S.level] = (S.fails[S.level] || 0) + 1;
    S.levelStars[S.level] = 0;
    P.resume = Math.max(1, S.level - 1); save();
    hud();
    var back = Math.max(1, S.level - 1), lv = LV[S.level - 1];
    say("The obstacle wins. Here is a working solution. You go back to level " + back + ".");
    var links = [];
    lv.revise.forEach(function (r, i) {
      if (i) links.push(", ");
      links.push(h("a", { href: r[1], target: "_blank", rel: "noopener" }, [r[0], h("span", { class: "sr-only" }, " (opens in a new tab)")]));
    });
    var card = h("div", { class: "pr-card pr-failcard" }, [
      h("p", { class: "pr-kicker pr-bad" }, "The obstacle wins"),
      h("h3", null, S.level > 1 ? "Back to level " + back : "Back to the start of level 1"),
      h("p", null, ["You did not clear ", h("strong", null, ch.title), ". Here is one working solution. Read it, work out why it passes, and you will meet this idea again."]),
      h("pre", { class: "pr-solution" }, h("code", null, ch.solution)),
      h("p", { class: "pr-key" }, [h("strong", null, "The key idea: "), h("span", { html: ch.hints[ch.hints.length - 1] })]),
      h("p", { class: "pr-revise" }, ["Revise: "].concat(links)),
      h("div", { class: "pr-actions" }, [
        h("button", { class: "btn btn-primary", type: "button", "data-act": "restart" }, S.level > 1 ? "Go back to level " + back : "Try level 1 again")
      ])
    ]);
    show(card, "[data-act=restart]");
    bonkAt(ob, function () { S.phase = "over"; dirty = true; });
  }

  function restart() {
    var back = Math.max(1, S.level - 1);
    S.anim = null; S.fade = 0;
    startLevel(back);
  }

  function levelDone() {
    var n = S.level, lv = LV[n - 1], got = S.levelStars[n] || 0;
    S.phase = "over";
    if (n >= TOP) { win(); return; }
    var next = LV[n];
    say("Level " + n + " clear. " + got + " of 9 stars.");
    show(h("div", { class: "pr-card pr-upcard" }, [
      h("p", { class: "pr-kicker pr-good" }, "Level " + n + " clear"),
      h("h3", null, lv.name + " complete"),
      h("p", { class: "pr-stars-big" }, [stars(got, 9), " ", got + " of 9 stars"]),
      h("p", null, ["Next: ", h("strong", null, next.name), ". ", next.concept + "."]),
      h("div", { class: "pr-actions" }, [
        h("button", { class: "btn btn-primary", type: "button", "data-act": "next" }, "On to level " + (n + 1))
      ])
    ]), "[data-act=next]");
  }

  function win() {
    P.wins++; P.resume = 0; save();
    var total = runStarTotal();
    var weak = [];
    for (var n = 1; n <= TOP; n++) {
      var f = S.fails[n] || 0, st = S.levelStars[n] || 0;
      if (f > 0 || st <= 4) weak.push({ n: n, f: f, st: st });
    }
    weak.sort(function (a, b) { return (b.f * 10 - b.st) - (a.f * 10 - a.st); });
    var items = weak.slice(0, 3).map(function (w) {
      var lv = LV[w.n - 1], r = lv.revise[0];
      return h("li", null, [h("strong", null, "Level " + w.n + ", " + lv.name), ": ",
        w.f ? "the obstacle won " + w.f + (w.f === 1 ? " time" : " times") : "only " + w.st + " of 9 stars", ". Revise ",
        h("a", { href: r[1], target: "_blank", rel: "noopener" }, [r[0], h("span", { class: "sr-only" }, " (opens in a new tab)")]), "."]);
    });
    say("You cleared all ten levels with " + total + " of 90 stars.");
    show(h("div", { class: "pr-card pr-wincard" }, [
      h("p", { class: "pr-kicker pr-good" }, "All ten levels clear"),
      h("h3", null, "You ran the whole game"),
      h("p", { class: "pr-stars-big" }, [stars(Math.round(total / 30), 3), " ", total + " of 90 stars · " + S.runCoins + " coins"]),
      items.length
        ? h("div", null, [h("p", null, "Where a little more practice would help:"), h("ul", { class: "pr-weak" }, items)])
        : h("p", null, "No weak spots to report. That was a clean run."),
      h("div", { class: "pr-actions" }, [
        h("button", { class: "btn btn-primary", type: "button", "data-act": "again" }, "Play again from level 1"),
        h("a", { class: "btn btn-secondary", href: "/python/" }, "Back to the Python course")
      ])
    ]), "[data-act=again]");
  }

  /* ----------------------------------------------------------------- title */
  function showTitle() {
    S.phase = "title"; S.level = Math.max(1, Math.min(TOP, P.resume || 1)); buildWorld(S.level); S.ch = null; S.bubble = false;
    S.levelStars = {}; S.fails = {}; S.runCoins = 0;
    hud(); dirty = true;
    var resume = P.resume > 0;
    var summary = P.best > 1 || solvedCount() > 0
      ? h("p", { class: "pr-note" }, "Your best so far: level " + P.best + " of " + TOP + ", " + totalStars() + " stars, " + solvedCount() + " of " + CH.length + " challenges solved.")
      : null;
    var card = h("div", { class: "pr-card pr-titlecard" }, [
      h("h3", null, resume ? "Welcome back" : "Ready to run?"),
      h("p", null, "Pixel runs by herself. At every obstacle you write a short Python function, and if it passes the tests she jumps on. Fail three times and you go back a level."),
      h("div", { class: "pr-actions" }, [
        resume ? h("button", { class: "btn btn-primary", type: "button", "data-act": "continue" }, "Continue at level " + P.resume) : null,
        h("button", { class: resume ? "btn btn-secondary" : "btn btn-primary", type: "button", "data-act": "start" }, resume ? "Start again at level 1" : "Start at level 1")
      ]),
      h("label", { class: "pr-check" }, [
        h("input", { type: "checkbox", id: "pr-quizmode", "data-act": "quizmode", checked: P.quiz }),
        " Quiz mode: no typing, read the code and choose what it returns"
      ]),
      summary,
      (P.best > 1 || solvedCount() > 0) ? h("p", { class: "pr-note" }, h("button", { class: "linklike", type: "button", "data-act": "reset" }, "Reset my progress")) : null
    ]);
    show(card, null, true);
  }

  function newRun(level) {
    P.runs++; save();
    S.levelStars = {}; S.fails = {}; S.runCoins = 0;
    startLevel(level);
  }

  /* ---------------------------------------------------------------- events */
  root.addEventListener("click", function (e) {
    var t = e.target;
    while (t && t !== root && !(t.getAttribute && t.getAttribute("data-act"))) t = t.parentNode;
    if (!t || t === root) return;
    var act = t.getAttribute("data-act");
    switch (act) {
      case "start": newRun(1); break;
      case "continue": newRun(Math.max(1, P.resume)); break;
      case "go": go(); break;
      case "run": runTests(); break;
      case "hint": giveHint(); break;
      case "tab": if (editor) { editor.focus(); indent(editor, false); } break;
      case "reset-code": if (editor && S.ch) { editor.value = S.ch.starter; editor.focus(); } break;
      case "giveup": confirmGiveUp(); break;
      case "keep-going": openChallengeAgain(); break;
      case "lose": lose(); break;
      case "restart": restart(); break;
      case "jump": jump(); break;
      case "next": startLevel(S.level + 1); break;
      case "again": newRun(1); break;
      case "pick": pick(parseInt(t.getAttribute("data-i"), 10)); break;
      case "to-quiz": P.quiz = true; save(); S.att = Math.min(S.att, QUIZ_ATTEMPTS); hud(); openQuiz(S.ch); break;
      case "retry-py": PY.state = "idle"; PY.p = null; bootPython().catch(function () { offerQuiz(); }); refreshRunButton(); break;
      case "reset": confirmReset(t); break;
      case "reset-yes": store.del("pixelrun"); P = freshProgress(); showTitle(); break;
      case "reset-no": showTitle(); break;
      case "quizmode": P.quiz = t.checked; save(); hud(); break;
    }
  });

  function openChallengeAgain() {
    // "No, keep trying": rebuild the actions row without losing the student's code
    var acts = $("#pr-actions");
    if (!acts) return;
    clear(acts);
    if (P.quiz) {
      acts.appendChild(h("button", { class: "tool-btn", type: "button", "data-act": "giveup" }, "Give up"));
      return;
    }
    [["btn btn-primary", "run", "Run tests", "pr-run"], ["tool-btn", "hint", S.ch.hints.length - S.hints > 0 ? "Hint (" + (S.ch.hints.length - S.hints) + " left, costs a star)" : "No more hints", "pr-hint"],
     ["tool-btn", "reset-code", "Reset code"], ["tool-btn", "giveup", "Give up"]].forEach(function (b) {
      acts.appendChild(h("button", { class: b[0], type: "button", "data-act": b[1], id: b[3] }, b[2]));
    });
    if (S.hints >= S.ch.hints.length) $("#pr-hint").disabled = true;
    refreshRunButton();
    if (editor) editor.focus();
  }

  function confirmReset(btn) {
    var p = btn.parentNode;
    clear(p);
    p.appendChild(document.createTextNode("Delete your level, stars and solved challenges on this device? "));
    p.appendChild(h("button", { class: "tool-btn", type: "button", "data-act": "reset-yes" }, "Yes, reset"));
    p.appendChild(document.createTextNode(" "));
    p.appendChild(h("button", { class: "tool-btn", type: "button", "data-act": "reset-no" }, "Cancel"));
  }

  $("#pr-calm").addEventListener("click", function () {
    P.calm = !calm(); save(); hud(); dirty = true;
  });
  if (mqReduce && mqReduce.addEventListener) mqReduce.addEventListener("change", function () { hud(); dirty = true; });
  window.addEventListener("resize", function () { dirty = true; });

  /* ------------------------------------------------------------------ boot */
  CH.forEach(function (c) {
    // the task as plain words for the screen reader announcement
    c.tasktext = h("div", { html: c.task }).textContent;
  });
  root.setAttribute("data-ready", "yes");
  showTitle();
  requestAnimationFrame(frame);
})();
