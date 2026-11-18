/* City Run: the street, the robot cat and everything on the road.

   A silver robot cat runs up a London street, seen from just behind and
   above: Westminster in the morning, the South Bank at noon, the City at
   sunset and Tower Bridge at night. The street is a small world projected
   onto a canvas: x across the road, y up and s along it, with three lanes
   up the middle.

   This file knows nothing about questions. stretch.js hands it a plan, the
   answer gates and what each lane's banner says, and hears back when the
   cat reaches a gate, picks up a diamond or bumps into something. Which
   lane is right is decided there, never here.

   window.MskCityRun.world(canvas, cfg) starts a street; see the API at the
   end of world(). */
(function () {
  "use strict";

  /* --------------------------------------------------------- the street */
  var LANE = 1.25;           // from one lane's middle to the next
  var ROAD = 1.95;           // half the road's width
  var WALK = 3.75;           // where the buildings start, either side
  var Z_CAT = 3.4;           // how far in front of the camera the cat runs
  var Z_NEAR = 0.6, Z_FAR = 118, Z_FADE = 82;
  var GRAV = 26, JUMP_V = 7.9;
  var SPEEDS = [13.5, 14.5, 15.5, 16.5], CALM_SPEED = 11, DASH = 2.5;
  var INTRO = 64;            // the stretch of road before the first question
  var GAP = 62;              // the road between one gate and the next question
  var FINISH = 52;           // from the last gate to the finish line
  var WAIT_BACK = 5.5;       // with the clock off, the cat waits this far short of a gate

  /* One palette per district, from morning to night. */
  var DIST = [
    { name: "Westminster",
      sky: ["#4F9FEA", "#A5D8F7", "#FCE1CB"], sun: [0.18, 0.5, "#FFF3D1", 0.07], night: 0,
      road: "#58626F", road2: "#4F5966", walk: "#D3CEC3", walk2: "#C2BCB0", line: "#F8FAFC", far: "#A4B6C8",
      build: [["#E9DFC8", "#D2C3A1"], ["#DCC79A", "#C2AC7B"], ["#EEE7D7", "#D8CBB0"], ["#C9A170", "#AD8556"], ["#E3D6BC", "#C9B994"]],
      win: "#41536A", glass: "#7FA6C4", lit: 0, roof: "#59626F", trim: "#F7F2E6", water: "#4B83A8", lamp: 0, cloud: "rgba(255,255,255,.85)" },
    { name: "South Bank",
      sky: ["#2E86DE", "#8ECFF7", "#E2F3FC"], sun: [0.72, 0.28, "#FFFCEB", 0.06], night: 0,
      road: "#5A6470", road2: "#525C68", walk: "#D6D2C8", walk2: "#C5C0B4", line: "#F8FAFC", far: "#9FB8CC",
      build: [["#A9533B", "#8E432F"], ["#BFB7AA", "#A59D8F"], ["#9C4A36", "#7F3B2A"], ["#D8D1C3", "#BDB4A3"], ["#B5644A", "#97503A"]],
      win: "#3D4D60", glass: "#8DC2DB", lit: 0, roof: "#5D5A57", trim: "#EFE8DA", water: "#3F87B5", lamp: 0, cloud: "rgba(255,255,255,.9)" },
    { name: "The City",
      sky: ["#4C2C8F", "#E2669C", "#FDBA74"], sun: [0.3, 0.9, "#FFE1A6", 0.09], night: 0.2,
      road: "#544E5E", road2: "#4C4656", walk: "#CDB9AE", walk2: "#BCA79C", line: "#FFF7ED", far: "#B98AA8",
      build: [["#4E7FA6", "#3D6688"], ["#D9C9B5", "#BFAD97"], ["#5C8CB0", "#476F8F"], ["#3F6A8A", "#30536D"], ["#E0CDB2", "#C5B094"]],
      win: "#2C3E57", glass: "#F8B88B", lit: 0.25, roof: "#3F3A4A", trim: "#F3E3D3", water: "#8C5B8F", lamp: 0.5, cloud: "rgba(255,214,190,.75)" },
    { name: "Tower Bridge",
      sky: ["#060A1F", "#1B2563", "#4B3A8A"], sun: [0.8, 0.22, "#F1F5F9", 0.05], night: 1,
      road: "#2A2F45", road2: "#252A3E", walk: "#4E5370", walk2: "#454A65", line: "#E2E8F0", far: "#3A3F6E",
      build: [["#6B3A31", "#552E27"], ["#7A4536", "#60362A"], ["#5D3A35", "#4A2E2A"], ["#4B4A60", "#3B3A4E"], ["#7D4B3A", "#62392C"]],
      win: "#1E2238", glass: "#FCD34D", lit: 0.62, roof: "#23263A", trim: "#9A8F86", water: "#1E3A6E", lamp: 1, cloud: "rgba(148,163,214,.35)" }
  ];
  var GEMC = ["#E0F2FE", "#7DD3FC", "#38BDF8", "#0284C7", "#075985"];

  /* ------------------------------------------------------------ helpers */
  function rng(seed) {
    var a = seed >>> 0;
    return function () {
      a = (a + 0x6D2B79F5) >>> 0;
      var t = a;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  function hex(c) {
    var n = parseInt(c.slice(1), 16);
    return [(n >> 16) & 255, (n >> 8) & 255, n & 255];
  }
  function mix(a, b, t) {
    var x = hex(a), y = hex(b);
    return "rgb(" + Math.round(x[0] + (y[0] - x[0]) * t) + "," + Math.round(x[1] + (y[1] - x[1]) * t) + "," + Math.round(x[2] + (y[2] - x[2]) * t) + ")";
  }
  function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
  function ease(t) { return t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2; }

  function world(canvas, cfg) {
    var ctx = canvas.getContext("2d");
    var calm = !!cfg.calm;
    var rnd = rng(cfg.seed || (Date.now() & 0x7fffffff));
    var W = 0, H = 0, dpr = 1, F = 300, hy = 100, cx = 0, camH = 1.9, camX = 0;
    var T = 0, last = 0, raf = 0, dead = false, paused = false;
    var dist = 0, v = 0, started = false, held = false, finished = false, finishFired = false;
    var cat = { lane: 1, x: 0, y: 0, vy: 0, phase: 0, lean: 0, squash: 0, hurt: 0, safe: 0, cheer: 0, splash: 0 };
    var objs = [];           // things on the road: obstacles, diamonds, gates, pigeons, beacons
    var scen = [];           // buildings, props and bridge parts at the sides
    var parts = [];          // particles, in screen space
    var nextB = [0, 0], nextP = [6, 10];
    var dash = false, gi = 0, waiting = false, shake = 0, skyK = 0, skyT = 0;

    /* ---------------------------------------------------------- the plan
       Every gate's place on the road, worked out up front from how long its
       question takes to read. The road between gates is filled as the cat
       gets near it. */
    var gates = [];
    var s = INTRO;
    cfg.gates.forEach(function (g, i) {
      var k = Math.min(3, Math.floor(i / 5));
      var speed = calm ? CALM_SPEED : SPEEDS[k];
      var read = cfg.timer ? Math.max(70, speed * g.read) : 58;
      gates.push({ i: i, lanes: g.lanes, readS: s, s: s + read, read: false, passed: false, res: null, burst: 0, k: k });
      s += read + (calm ? GAP - 10 : GAP);
    });
    var finishS = gates.length ? gates[gates.length - 1].s + FINISH : s;
    // A district starts just after the gate that ends the one before it.
    var districtS = [0];
    for (var d = 1; d < 4; d++) districtS.push(gates[d * 5 - 1] ? gates[d * 5 - 1].s + 3 : 1e9);
    var districtFired = [true, false, false, false];
    // Two bridges: Westminster Bridge into the South Bank, and Tower Bridge at the end.
    var bridges = [];
    if (gates[4] && gates[5]) bridges.push({ s0: gates[4].s + 10, s1: gates[5].readS - 4, kind: "west" });
    if (gates.length) bridges.push({ s0: gates[gates.length - 1].s + 8, s1: finishS + 60, kind: "tower" });
    function districtAt(pos) { var k = 0; for (var j = 1; j < 4; j++) if (pos >= districtS[j]) k = j; return k; }
    function onBridge(pos) { for (var j = 0; j < bridges.length; j++) if (pos >= bridges[j].s0 && pos <= bridges[j].s1) return bridges[j]; return null; }
    var filled = 0;          // the road is planned up to here
    var sections = [];       // [from, to, district] stretches to fill with traffic and diamonds
    sections.push([18, INTRO - 10, 0]);
    gates.forEach(function (g, i) {
      var next = gates[i + 1] ? gates[i + 1].readS : finishS - 6;
      sections.push([g.s + 16, next - 8, Math.min(3, Math.floor((i + 1) / 5)), g.i]);
    });

    /* ---------------------------------------------------------- layout */
    function layout() {
      var r = canvas.getBoundingClientRect();
      W = Math.max(1, r.width); H = Math.max(1, r.height);
      dpr = Math.min(2, window.devicePixelRatio || 1);
      canvas.width = Math.round(W * dpr); canvas.height = Math.round(H * dpr);
      hy = H * 0.33;
      F = Math.min(1.02 * H, 0.84 * W);
      camH = (H * 0.9 - hy) * Z_CAT / F;
      cx = W / 2;
      cache = {};
      if (!started || paused) draw();
    }
    var cache = {};
    var ro = null;
    if (window.ResizeObserver) { ro = new ResizeObserver(function () { layout(); }); ro.observe(canvas); }
    else window.addEventListener("resize", layout);

    /* ------------------------------------------------------- projection */
    function zOf(pos) { return pos - dist + Z_CAT; }
    function PX(x, z) { return cx + (x - camX) * F / z; }
    function PY(y, z) { return hy + (camH - y) * F / z; }
    function laneX(l) { return (l - 1) * LANE; }

    /* ------------------------------------------------------- the road ahead */
    function spawn() {
      var ahead = dist + Z_FAR + 4;
      // buildings, both sides
      for (var side = 0; side < 2; side++) {
        while (nextB[side] < ahead) {
          var br = onBridge(nextB[side]) || onBridge(nextB[side] + 3);
          if (br) { nextB[side] = br.s1 + 0.5; continue; }
          var k = districtAt(nextB[side]);
          var P = DIST[k];
          var len = 3.3 + rnd() * 4.4;
          var tower = k === 2 && rnd() < 0.55;
          var h = tower ? 7 + rnd() * 8 : 3.2 + rnd() * (k === 0 ? 2.6 : 3.4);
          var col = P.build[Math.floor(rnd() * P.build.length)];
          var floors = Math.max(2, Math.round(h / (tower ? 0.95 : 1.2)));
          var cols = Math.max(2, Math.round(len / (tower ? 0.7 : 1.05)));
          var lit = [];
          for (var q = 0; q < floors * cols; q++) lit.push(rnd() < P.lit);
          scen.push({ t: "build", side: side ? 1 : -1, s0: nextB[side], s1: nextB[side] + len, h: h, col: col, k: k,
                      floors: floors, cols: cols, tower: tower, shop: !tower && rnd() < 0.45,
                      awn: ["#B91C1C", "#1D4ED8", "#047857", "#7C2D12", "#6D28D9", "#0F766E"][Math.floor(rnd() * 6)],
                      gothic: k === 0 && rnd() < 0.5, lit: lit });
          nextB[side] += len + (rnd() < 0.1 ? 2.2 : 0);
        }
      }
      // street furniture
      for (side = 0; side < 2; side++) {
        while (nextP[side] < ahead) {
          var pos = nextP[side], sd = side ? 1 : -1;
          var b2 = onBridge(pos);
          if (b2) {
            scen.push({ t: b2.kind === "west" ? "blamp" : "tlamp", side: sd, s0: pos });
            nextP[side] += 7;
            continue;
          }
          var kk = districtAt(pos), roll = rnd();
          var kind = roll < 0.38 ? "lamp" : roll < 0.6 ? "tree" : roll < 0.72 ? "phone" : roll < 0.84 ? "post" : roll < 0.93 ? "bench" : "stop";
          if (kk === 2 && kind === "tree" && rnd() < 0.5) kind = "lamp";
          scen.push({ t: kind, side: sd, s0: pos, k: kk, sway: rnd() * 6 });
          nextP[side] += 6.5 + rnd() * 5;
        }
      }
      // the river under the bridges
      bridges.forEach(function (b) {
        if (!b.made && b.s0 < ahead) { b.made = true; scen.push({ t: "water", s0: b.s0, s1: b.s1, kind: b.kind }); }
      });
      // traffic and diamonds, a section at a time
      while (sections.length && sections[0][0] < ahead + 40) fill(sections.shift());
      // each gate, when it comes into range
      gates.forEach(function (g) {
        if (!g.made && g.s < ahead + 20) { g.made = true; makeGate(g); }
      });
      if (!finishMade && finishS < ahead + 30) { finishMade = true; objs.push({ t: "finish", s: finishS }); objs.push({ t: "tower", s: finishS - 1.5 }); objs.push({ t: "tower", s: finishS + 20 }); }
      if (!startMade) { startMade = true; objs.push({ t: "startarch", s: 7 }); }
    }
    var finishMade = false, startMade = false;

    /* The traffic between two questions. Every row leaves at least one lane
       open, and a bus or a cab blocks its lane for its whole length. */
    function fill(sec) {
      var from = sec[0], to = sec[1], k = sec[2];
      var busy = [-1e9, -1e9, -1e9];
      var pos = from + 4;
      var rows = 0;
      while (pos < to - 4) {
        var free = [0, 1, 2].filter(function (l) { return busy[l] < pos - 1.5; });
        if (free.length < 2) { pos += 3; continue; }
        var hard = !calm && k >= 1 && rnd() < 0.18 + k * 0.08;
        var roll = rnd();
        var lanes = shuffleArr([0, 1, 2].filter(function (l) { return free.indexOf(l) > -1; }));
        var a = lanes[0], b = lanes[1];
        if (roll < 0.22) {
          addVehicle("bus", a, pos); busy[a] = pos + 4.6;
          if (hard && lanes.length > 2) { objs.push({ t: "cone", lane: b, s: pos + 1 }); }
          gemLine(lanes[lanes.length - 1], pos - 1, 4);
        } else if (roll < 0.38) {
          addVehicle("cab", a, pos); busy[a] = pos + 3;
          gemLine(b, pos - 2, 4);
          if (hard && lanes.length > 2) objs.push({ t: "barrier", lane: lanes[2], s: pos + 0.5 });
        } else if (roll < 0.55) {
          objs.push({ t: "cone", lane: a, s: pos });
          if (hard) objs.push({ t: "cone", lane: b, s: pos });
          gemArc(a, pos);
        } else if (roll < 0.68) {
          objs.push({ t: "barrier", lane: a, s: pos });
          gemArc(a, pos);
          if (hard) addVehicle("cab", b, pos + 2), busy[b] = pos + 5;
        } else if (roll < 0.8) {
          objs.push({ t: "puddle", lane: a, s: pos });
          gemLine(b, pos - 2, 5);
        } else {
          objs.push({ t: "pigeons", lane: a, s: pos, birds: [0, 1, 2].map(function () { return { dx: (rnd() - 0.5) * 0.7, ds: (rnd() - 0.5) * 1.2, ph: rnd() * 6, fly: 0, vx: 0, vy: 0, vz: 0 }; }) });
          gemLine(a, pos + 2, 5);
        }
        rows += 1;
        pos += (calm ? 17 : 13) + rnd() * 5 - k;
      }
    }
    function shuffleArr(a) {
      for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(rnd() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t; }
      return a;
    }
    function addVehicle(kind, lane, pos) {
      objs.push({ t: kind, lane: lane, s: pos, len: kind === "bus" ? 4.4 : 2.7,
                  col: kind === "cab" && rnd() < 0.25 ? "#7F1D1D" : null, n: Math.floor(rnd() * 90) + 10 });
    }
    function gemLine(lane, pos, n) {
      for (var i = 0; i < n; i++) objs.push({ t: "gem", lane: lane, s: pos + i * 1.7, y: 0.42 });
    }
    function gemArc(lane, pos) {
      for (var i = 0; i < 5; i++) {
        var u = (i - 2) / 2;
        objs.push({ t: "gem", lane: lane, s: pos + u * 2.6, y: 0.5 + 0.75 * (1 - u * u) });
      }
    }
    /* A gate: a banner across each answer lane, a zebra crossing just before
       it and road works in the middle lane when there are only two answers.
       While a question is being read, a diamond in every lane now and then,
       so no lane is a better place to wait than another. */
    function makeGate(g) {
      objs.push({ t: "zebra", s: g.s - 3.6 });
      objs.push({ t: "beacon", side: -1, s: g.s - 3.6 });
      objs.push({ t: "beacon", side: 1, s: g.s - 3.6 });
      objs.push({ t: "gate", s: g.s, g: g });
      if (!g.lanes[1]) objs.push({ t: "works", lane: 1, s: g.s - 0.6, g: g });
      for (var p = g.readS + 14; p < g.s - 12; p += 15) {
        for (var l = 0; l < 3; l++) if (g.lanes[l] || l !== 1) objs.push({ t: "gem", lane: l, s: p, y: 0.42, rowGem: true });
      }
    }

    /* ---------------------------------------------------------- update */
    function speedNow() {
      var k = Math.min(3, Math.floor(gi / 5));
      return calm ? CALM_SPEED : SPEEDS[k];
    }
    function update(dt) {
      T += dt;
      if (shake > 0) shake = Math.max(0, shake - dt * 3);
      var g = gates[gi];
      // how fast the cat should be going
      var target = 0;
      if (started && !held && !finished) {
        target = speedNow() * (dash ? DASH : 1);
        waiting = false;
        if (g && !cfg.timer && !g.go && dist > g.readS) {
          var stopAt = g.s - WAIT_BACK;
          var room = stopAt - dist;
          target = room <= 0.05 ? 0 : Math.min(target, Math.sqrt(2 * 22 * room) + 0.4);
          if (room <= 0.3) waiting = true;
        }
      }
      if (finished) target = Math.max(0, v - 0); // coast to a stop below
      var acc = target > v ? (dash ? 40 : 14) : (held ? 90 : finished ? 7 : 45);
      v += clamp(target - v, -acc * dt, acc * dt);
      if (finished) v = Math.max(0, v - 7 * dt);
      dist += v * dt;
      if (!cfg.timer && g && !g.go && dist > g.s - WAIT_BACK) dist = Math.max(dist - v * dt, Math.min(dist, g.s - WAIT_BACK));

      // the cat
      var tx = laneX(cat.lane);
      var dx = tx - cat.x;
      cat.x += clamp(dx, -10 * dt, 10 * dt);
      cat.lean += ((clamp(dx * 0.55, -0.32, 0.32)) - cat.lean) * Math.min(1, dt * 14);
      if (cat.y > 0 || cat.vy > 0) {
        cat.vy -= GRAV * dt;
        cat.y += cat.vy * dt;
        if (cat.y <= 0) { cat.y = 0; cat.vy = 0; cat.squash = calm ? 0 : 0.16; }
      }
      cat.squash *= Math.pow(0.0008, dt);
      cat.phase += dt * (v > 0.5 ? 7 + v * 0.62 : 0);
      if (cat.hurt > 0) cat.hurt = Math.max(0, cat.hurt - dt);
      if (cat.safe > 0) cat.safe = Math.max(0, cat.safe - dt);
      if (cat.cheer > 0) cat.cheer = Math.max(0, cat.cheer - dt);
      camX += (cat.x * 0.55 - camX) * Math.min(1, dt * 6);

      spawn();
      collide();

      // questions: time to read, then the gate
      if (g && !g.read && dist >= g.readS) { g.read = true; if (cfg.onRead) cfg.onRead(g.i); }
      if (g && !g.passed && dist >= g.s) passGate(g);
      for (var k2 = 1; k2 < 4; k2++) {
        if (!districtFired[k2] && dist >= districtS[k2]) { districtFired[k2] = true; if (cfg.onDistrict) cfg.onDistrict(k2); }
      }
      if (!finishFired && dist >= finishS) {
        finishFired = true; finished = true;
        burst(PX(laneX(cat.lane), Z_CAT + 1), PY(1.4, Z_CAT + 1), 40, "confetti");
        if (cfg.onFinish) cfg.onFinish();
      }
      // the sky turns with the district the cat is in
      var want = districtAt(dist);
      if (want !== skyK) { skyT += dt / 3.2; if (skyT >= 1) { skyK = want; skyT = 0; } }

      // tidy up what is behind the camera
      objs = objs.filter(function (o) { return zOf(o.s + (o.len || 0)) > Z_NEAR - 0.4 || o.t === "pigeons" && o.birds.some(function (b) { return b.fly > 0 && b.fly < 2.5; }); });
      scen = scen.filter(function (o) { return zOf(o.s1 || o.s0) > Z_NEAR - 1; });
      parts = parts.filter(function (p) { p.life -= dt; return p.life > 0; });
      parts.forEach(function (p) { p.vy += (p.g || 0) * dt; p.x += p.vx * dt; p.y += p.vy * dt; p.a += (p.va || 0) * dt; });
    }

    function catBox() { return { x: cat.x, s: dist }; }
    function collide() {
      var cs = dist;
      for (var i = 0; i < objs.length; i++) {
        var o = objs[i];
        if (o.done) continue;
        var lx = laneX(o.lane);
        if (o.t === "gem") {
          if (Math.abs(o.s - cs) < 0.75 && Math.abs(lx - cat.x) < 0.62 && Math.abs(cat.y + 0.4 - o.y) < 0.85) {
            o.done = true;
            var z = zOf(o.s);
            burst(PX(lx, Math.max(z, 1)), PY(o.y, Math.max(z, 1)), calm ? 0 : 6, "sparkle");
            if (cfg.onGem) cfg.onGem(1);
          }
          continue;
        }
        if (o.t === "pigeons") {
          if (o.s - cs < 6) o.birds.forEach(function (b) {
            if (!b.fly) { b.fly = 0.01; b.vx = (b.dx < 0 ? -1 : 1) * (1.5 + rnd() * 2); b.vy = 2.5 + rnd() * 2; b.vz = 2 + rnd() * 3; if (cfg.sound) cfg.sound("flap"); }
          });
          continue;
        }
        var solid = { cone: [0.36, 0.55], barrier: [0.56, 0.62], puddle: [0.5, 0], bus: [0.62, 3], cab: [0.55, 1.5], works: [0.6, 0.7] }[o.t];
        if (!solid || cat.safe > 0 || held) continue;
        var len = o.len || (o.t === "puddle" ? 1.2 : 0.4);
        if (cs < o.s - 0.35 || cs > o.s + len + 0.2) continue;
        if (Math.abs(lx - cat.x) > solid[0] + 0.22) continue;
        if (o.t === "works") continue;    // the gate decides what happens in the middle lane
        if (cat.y > solid[1]) continue;
        o.done = true;
        if (o.t === "puddle") {
          var zp = zOf(o.s);
          burst(PX(lx, Math.max(zp, 1.2)), PY(0.1, Math.max(zp, 1.2)), calm ? 0 : 16, "splash");
          cat.splash = 0.5;
          if (cfg.onHit) cfg.onHit("puddle");
          continue;
        }
        hurt(o.t);
      }
    }
    function hurt(kind) {
      cat.hurt = 0.55; cat.safe = 1.3;
      shake = calm ? 0 : 1;
      v *= 0.45;
      var lost = cfg.onHit ? cfg.onHit(kind) || 0 : 0;
      var gx = PX(cat.x, Z_CAT), gy = PY(0.6, Z_CAT);
      burst(gx, gy, calm ? 0 : 14, "spark");
      for (var i = 0; i < lost && !calm; i++) {
        parts.push({ kind: "gemlost", x: gx, y: gy, vx: (rnd() - 0.5) * 420, vy: -260 - rnd() * 200, g: 900, a: 0, va: (rnd() - 0.5) * 12, life: 1, max: 1, r: 9 });
      }
    }
    function passGate(g) {
      g.passed = true;
      var lane = cat.lane;
      dash = false;
      var res = cfg.onGate ? cfg.onGate(g.i, lane) : null;
      g.res = res || { ok: false, right: -1 };
      g.chosen = lane;
      g.burst = T;
      gi += 1;
      var z = Z_CAT + 0.2;
      var gx = PX(laneX(lane), z), gy = PY(1.0, z);
      if (!g.lanes[lane]) {                 // ran into the road works
        hurt("works");
        return;
      }
      if (g.res.ok) {
        burst(gx, gy, calm ? 0 : 26, "paper", g.lanes[lane].c);
        burst(gx, gy, calm ? 0 : 14, "gem");
        cat.cheer = 0.7;
        if (!calm && cat.y <= 0) cat.vy = 4.2;
      } else {
        burst(gx, gy, calm ? 0 : 18, "paper", g.lanes[lane].c);
        shake = calm ? 0 : 0.6;
        cat.hurt = 0.4;
      }
    }

    /* --------------------------------------------------------- particles */
    function burst(x, y, n, kind, colour) {
      for (var i = 0; i < n; i++) {
        var a = rnd() * Math.PI * 2, sp = 120 + rnd() * 320;
        var p = { kind: kind, x: x, y: y, vx: Math.cos(a) * sp, vy: Math.sin(a) * sp - 120, g: 700, a: rnd() * 6, va: (rnd() - 0.5) * 14, life: 0.9 + rnd() * 0.5, r: 4 + rnd() * 5, c: colour };
        if (kind === "sparkle") { p.vx *= 0.35; p.vy = -60 - rnd() * 120; p.g = 0; p.life = 0.45; p.r = 2 + rnd() * 3; }
        if (kind === "spark") { p.c = rnd() < 0.5 ? "#FDE047" : "#FB923C"; p.r = 2 + rnd() * 2.5; p.life = 0.5; }
        if (kind === "splash") { p.c = rnd() < 0.5 ? "#BAE6FD" : "#7DD3FC"; p.vy = -180 - rnd() * 260; p.vx *= 0.6; p.g = 1100; p.life = 0.7; p.r = 2.5 + rnd() * 3; }
        if (kind === "gem") { p.vy = -280 - rnd() * 300; p.vx *= 0.7; p.g = 820; p.r = 8 + rnd() * 5; p.life = 1.1; }
        if (kind === "confetti") { p.c = ["#F43F5E", "#FDE047", "#38BDF8", "#4ADE80", "#E879F9", "#FFFFFF"][i % 6]; p.vy = -380 - rnd() * 380; p.vx *= 1.4; p.g = 520; p.life = 2.2; }
        p.max = p.life;
        parts.push(p);
      }
    }

    /* ============================================================= DRAW */
    function draw() {
      if (!W) return;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
      var P = DIST[skyK], Q = DIST[Math.min(3, skyK + 1)];
      var t = skyT > 0 ? ease(skyT) : 0;
      ctx.save();
      if (shake > 0) ctx.translate((rnd() - 0.5) * 9 * shake, (rnd() - 0.5) * 7 * shake);
      drawSky(P, Q, t);
      drawSkyline(P, Q, t);
      drawGround(P, Q, t);
      var list = [];
      scen.forEach(function (o) { if (o.t === "water") return; var z = zOf(o.s1 !== undefined ? o.s1 : o.s0); list.push([Math.min(z, Z_FAR), o, 1]); });
      objs.forEach(function (o) { if (o.t === "zebra" || o.t === "puddle") return; list.push([zOf(o.s), o, 0]); });
      list.push([Z_CAT - 0.05, null, 2]);
      list.sort(function (a, b) { return b[0] - a[0]; });
      for (var i = 0; i < list.length; i++) {
        var it = list[i];
        if (it[2] === 2) { drawCat(); continue; }
        if (it[2] === 1) drawScen(it[1]); else drawObj(it[1]);
      }
      drawParts();
      if (dash && !calm) speedLines();
      ctx.restore();
    }

    /* ------------------------------------------------------------- sky */
    function drawSky(P, Q, t) {
      var g = ctx.createLinearGradient(0, 0, 0, hy + 2);
      g.addColorStop(0, mix(P.sky[0], Q.sky[0], t));
      g.addColorStop(0.62, mix(P.sky[1], Q.sky[1], t));
      g.addColorStop(1, mix(P.sky[2], Q.sky[2], t));
      ctx.fillStyle = g;
      ctx.fillRect(-20, -20, W + 40, hy + 22);
      var night = P.night + (Q.night - P.night) * t;
      // stars of the night district are tiny city sparks, not stars: a few twinkles
      if (night > 0.6) {
        ctx.fillStyle = "rgba(255,255,255," + (0.5 * night) + ")";
        for (var i = 0; i < 26; i++) {
          var sx = (i * 97.3) % W, sy = (i * 41.7) % (hy * 0.7);
          var tw = calm ? 1 : 0.5 + 0.5 * Math.sin(T * 2 + i);
          ctx.globalAlpha = 0.35 + 0.5 * tw * night;
          ctx.fillRect(sx, sy, 1.6, 1.6);
        }
        ctx.globalAlpha = 1;
      }
      // the sun, or the moon at night
      var sp = t < 0.5 ? P.sun : Q.sun, fade = t < 0.5 ? 1 - t * 2 : (t - 0.5) * 2;
      var sxp = W * sp[0], syp = hy * sp[1], r = H * sp[3] + 6;
      ctx.globalAlpha = fade;
      var gl = ctx.createRadialGradient(sxp, syp, r * 0.4, sxp, syp, r * 4);
      gl.addColorStop(0, "rgba(255,250,230,.55)"); gl.addColorStop(1, "rgba(255,250,230,0)");
      ctx.fillStyle = gl;
      ctx.fillRect(sxp - r * 4, syp - r * 4, r * 8, r * 8);
      ctx.fillStyle = sp[2];
      ctx.beginPath(); ctx.arc(sxp, syp, r, 0, 6.3); ctx.fill();
      if ((t < 0.5 ? P : Q).night > 0.6) {          // the moon's shadow side
        ctx.fillStyle = mix(P.sky[0], Q.sky[0], t);
        ctx.beginPath(); ctx.arc(sxp + r * 0.42, syp - r * 0.2, r * 0.9, 0, 6.3); ctx.fill();
      }
      ctx.globalAlpha = 1;
      // clouds drift slowly by
      ctx.fillStyle = t < 0.5 ? P.cloud : Q.cloud;
      for (var c = 0; c < 5; c++) {
        var w = W * (0.12 + (c % 3) * 0.05), cxp = ((c * 0.27 * W + (calm ? 0 : T * (6 + c * 2))) % (W + w * 2)) - w;
        var cy = hy * (0.18 + (c * 0.13) % 0.5);
        cloud(cxp, cy, w);
      }
    }
    function cloud(x, y, w) {
      ctx.beginPath();
      ctx.ellipse(x, y, w * 0.5, w * 0.13, 0, 0, 6.3);
      ctx.ellipse(x - w * 0.18, y - w * 0.08, w * 0.2, w * 0.13, 0, 0, 6.3);
      ctx.ellipse(x + w * 0.1, y - w * 0.12, w * 0.24, w * 0.17, 0, 0, 6.3);
      ctx.fill();
    }

    /* -------------------------------------------------------- skyline
       Far away, along the horizon: a band of low roofs, then each district's
       landmarks. They grow a little as the cat runs towards them. */
    function drawSkyline(P, Q, t) {
      var k = districtAt(dist);
      var a = gates[k * 5] ? gates[k * 5].readS : 0, b = districtS[k + 1] < 1e8 ? districtS[k + 1] : finishS;
      var prog = clamp((dist - (k ? districtS[k] : 0)) / Math.max(1, b - (k ? districtS[k] : 0)), 0, 1);
      var u = H * 0.055 * (0.86 + prog * 0.42);
      var base = hy + 1;
      var far = mix(P.far, Q.far, t);
      // a band of distant roofs
      ctx.fillStyle = far;
      ctx.beginPath();
      ctx.moveTo(-10, base);
      for (var x = -10, j = 0; x < W + 10; j++) {
        var bw = 8 + ((j * 37) % 23), bh = H * (0.012 + ((j * 53) % 17) / 600);
        ctx.lineTo(x, base - bh); ctx.lineTo(x + bw, base - bh);
        x += bw;
      }
      ctx.lineTo(W + 10, base); ctx.closePath(); ctx.fill();
      var night = k === 3;
      var drift = (camX * -6);
      if (k === 0) {
        parliament(cx - u * 2.2 + drift, base, u, night);
        bigBen(cx + u * 1.6 + drift, base, u, night);
      } else if (k === 1) {
        eye(cx - u * 1.1 + drift, base, u, night);
        shard(cx + u * 3.6 + drift, base, u * 0.8, night);
      } else if (k === 2) {
        stPauls(cx - u * 2.6 + drift, base, u, night);
        gherkin(cx + u * 1.2 + drift, base, u, night);
        shard(cx + u * 3.4 + drift, base, u * 1.05, night);
      } else {
        towerBridge(cx + drift, base, u * 1.05, night);
      }
      // a haze over the far distance
      var hz = ctx.createLinearGradient(0, base - H * 0.08, 0, base + 2);
      hz.addColorStop(0, "rgba(255,255,255,0)");
      hz.addColorStop(1, night ? "rgba(76,58,138,.35)" : "rgba(255,240,225,.32)");
      ctx.fillStyle = hz;
      ctx.fillRect(0, base - H * 0.08, W, H * 0.08 + 2);
    }
    function rect(x, y, w, h, c) { ctx.fillStyle = c; ctx.fillRect(x, y, w, h); }
    function tri(x1, y1, x2, y2, x3, y3, c) { ctx.fillStyle = c; ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.lineTo(x3, y3); ctx.closePath(); ctx.fill(); }
    function bigBen(x, y, u, night) {
      var stone = night ? "#8C7A55" : "#D8BF85", deep = night ? "#6E5F42" : "#B79C62", roof = night ? "#2E3550" : "#4B5568", gold = "#E9C46A";
      rect(x - u * 0.5, y - u * 3.8, u, u * 3.8, stone);
      for (var i = 1; i < 4; i++) rect(x - u * 0.5 + i * u * 0.25 - u * 0.02, y - u * 3.6, u * 0.04, u * 3.3, deep);
      rect(x - u * 0.62, y - u * 4.85, u * 1.24, u * 1.08, stone);
      rect(x - u * 0.62, y - u * 3.86, u * 1.24, u * 0.1, deep);
      ctx.fillStyle = night ? "#FDE68A" : "#FFF8E7";
      ctx.beginPath(); ctx.arc(x, y - u * 4.3, u * 0.4, 0, 6.3); ctx.fill();
      ctx.strokeStyle = gold; ctx.lineWidth = Math.max(1, u * 0.07); ctx.stroke();
      var now = new Date(), hr = (now.getHours() % 12 + now.getMinutes() / 60) / 12 * Math.PI * 2, mn = now.getMinutes() / 60 * Math.PI * 2;
      ctx.strokeStyle = "#1F2937"; ctx.lineWidth = Math.max(1, u * 0.06); ctx.lineCap = "round";
      ctx.beginPath(); ctx.moveTo(x, y - u * 4.3); ctx.lineTo(x + Math.sin(hr) * u * 0.2, y - u * 4.3 - Math.cos(hr) * u * 0.2);
      ctx.moveTo(x, y - u * 4.3); ctx.lineTo(x + Math.sin(mn) * u * 0.32, y - u * 4.3 - Math.cos(mn) * u * 0.32); ctx.stroke();
      rect(x - u * 0.52, y - u * 5.45, u * 1.04, u * 0.6, deep);
      for (var j = 0; j < 3; j++) rect(x - u * 0.38 + j * u * 0.3, y - u * 5.35, u * 0.16, u * 0.42, night ? "#1E1B2E" : "#5B4A2E");
      tri(x - u * 0.6, y - u * 5.45, x, y - u * 7.3, x + u * 0.6, y - u * 5.45, roof);
      tri(x - u * 0.62, y - u * 5.45, x - u * 0.5, y - u * 6.1, x - u * 0.38, y - u * 5.45, gold);
      tri(x + u * 0.38, y - u * 5.45, x + u * 0.5, y - u * 6.1, x + u * 0.62, y - u * 5.45, gold);
      rect(x - u * 0.03, y - u * 7.7, u * 0.06, u * 0.45, gold);
    }
    function parliament(x, y, u, night) {
      var stone = night ? "#7E6E50" : "#CFB77F", deep = night ? "#655840" : "#B09A66";
      rect(x - u * 3.4, y - u * 1.4, u * 3.6, u * 1.4, stone);
      for (var i = 0; i < 12; i++) {
        var px = x - u * 3.3 + i * u * 0.3;
        tri(px, y - u * 1.4, px + u * 0.08, y - u * 1.85, px + u * 0.16, y - u * 1.4, deep);
        rect(px + u * 0.03, y - u * 1.15, u * 0.1, u * 0.5, night ? "#FCD34D" : "#8A7650");
      }
      rect(x - u * 4.2, y - u * 3.2, u * 0.95, u * 3.2, stone);
      for (var j = 0; j < 4; j++) tri(x - u * 4.2 + j * u * 0.24, y - u * 3.2, x - u * 4.08 + j * u * 0.24, y - u * 3.6, x - u * 3.96 + j * u * 0.24, y - u * 3.2, deep);
      rect(x - u * 4.05, y - u * 2.7, u * 0.65, u * 0.12, deep);
    }
    function eye(x, y, u, night) {
      var R = u * 2.6, hx = x, hyy = y - R - u * 0.35;
      ctx.strokeStyle = night ? "#C7D2FE" : "#F1F5F9"; ctx.lineWidth = Math.max(1.2, u * 0.12);
      ctx.beginPath(); ctx.moveTo(hx, hyy); ctx.lineTo(hx + R * 0.55, y); ctx.moveTo(hx, hyy); ctx.lineTo(hx + R * 0.2, y); ctx.stroke();
      ctx.lineWidth = Math.max(1, u * 0.09);
      ctx.beginPath(); ctx.arc(hx, hyy, R, 0, 6.3); ctx.stroke();
      ctx.lineWidth = Math.max(0.6, u * 0.035);
      ctx.beginPath(); ctx.arc(hx, hyy, R * 0.93, 0, 6.3); ctx.stroke();
      var rot = calm ? 0 : T * 0.06;
      for (var i = 0; i < 16; i++) { var a = rot + i * Math.PI / 8; ctx.moveTo(hx, hyy); ctx.lineTo(hx + Math.cos(a) * R, hyy + Math.sin(a) * R); }
      ctx.stroke();
      ctx.fillStyle = night ? "#A5B4FC" : "#7DD3FC";
      for (var c = 0; c < 32; c++) {
        var b = rot + c * Math.PI / 16;
        ctx.beginPath(); ctx.ellipse(hx + Math.cos(b) * R, hyy + Math.sin(b) * R + u * 0.1, u * 0.13, u * 0.09, 0, 0, 6.3); ctx.fill();
      }
      ctx.fillStyle = "#E2E8F0"; ctx.beginPath(); ctx.arc(hx, hyy, u * 0.2, 0, 6.3); ctx.fill();
    }
    function stPauls(x, y, u, night) {
      var stone = night ? "#8D8778" : "#E7E0CF", lead = night ? "#5D6B78" : "#9DAAB4", deep = night ? "#6E695C" : "#C9C0AA";
      rect(x - u * 1.6, y - u * 1.3, u * 3.2, u * 1.3, stone);
      rect(x - u * 1.5, y - u * 2.1, u * 0.5, u * 0.8, stone); rect(x + u * 1.0, y - u * 2.1, u * 0.5, u * 0.8, stone);
      tri(x - u * 1.55, y - u * 2.1, x - u * 1.25, y - u * 2.6, x - u * 0.95, y - u * 2.1, lead);
      tri(x + u * 0.95, y - u * 2.1, x + u * 1.25, y - u * 2.6, x + u * 1.55, y - u * 2.1, lead);
      rect(x - u * 0.85, y - u * 2.2, u * 1.7, u * 0.9, stone);
      for (var i = 0; i < 8; i++) rect(x - u * 0.78 + i * u * 0.21, y - u * 2.15, u * 0.07, u * 0.8, deep);
      ctx.fillStyle = lead;
      ctx.beginPath(); ctx.ellipse(x, y - u * 2.2, u * 0.95, u * 1.15, 0, Math.PI, 0); ctx.fill();
      ctx.fillStyle = "rgba(255,255,255,.25)"; ctx.beginPath(); ctx.ellipse(x - u * 0.35, y - u * 2.7, u * 0.18, u * 0.5, 0.3, 0, 6.3); ctx.fill();
      rect(x - u * 0.16, y - u * 3.75, u * 0.32, u * 0.45, stone);
      ctx.fillStyle = "#E9C46A"; ctx.beginPath(); ctx.arc(x, y - u * 3.85, u * 0.12, 0, 6.3); ctx.fill();
      rect(x - u * 0.025, y - u * 4.2, u * 0.05, u * 0.3, "#E9C46A");
    }
    function gherkin(x, y, u, night) {
      ctx.save();
      ctx.beginPath();
      ctx.moveTo(x - u * 0.62, y);
      ctx.bezierCurveTo(x - u * 1.05, y - u * 2.0, x - u * 0.75, y - u * 4.0, x, y - u * 4.6);
      ctx.bezierCurveTo(x + u * 0.75, y - u * 4.0, x + u * 1.05, y - u * 2.0, x + u * 0.62, y);
      ctx.closePath();
      ctx.fillStyle = night ? "#1F3B4D" : "#2F6170"; ctx.fill();
      ctx.clip();
      ctx.strokeStyle = night ? "rgba(253,224,71,.45)" : "rgba(180,226,230,.55)"; ctx.lineWidth = Math.max(0.8, u * 0.07);
      for (var i = -8; i < 8; i++) {
        ctx.beginPath(); ctx.moveTo(x + i * u * 0.32, y); ctx.lineTo(x + i * u * 0.32 + u * 2.2, y - u * 4.6); ctx.stroke();
        ctx.beginPath(); ctx.moveTo(x + i * u * 0.32, y); ctx.lineTo(x + i * u * 0.32 - u * 2.2, y - u * 4.6); ctx.stroke();
      }
      ctx.restore();
    }
    function shard(x, y, u, night) {
      var g = ctx.createLinearGradient(x - u, 0, x + u, 0);
      g.addColorStop(0, night ? "#36406B" : "#B9CCDC"); g.addColorStop(0.55, night ? "#4C5A8A" : "#DCE8F1"); g.addColorStop(1, night ? "#2B3358" : "#9FB6C9");
      ctx.fillStyle = g;
      ctx.beginPath(); ctx.moveTo(x - u * 0.9, y); ctx.lineTo(x - u * 0.12, y - u * 7.4); ctx.lineTo(x + u * 0.05, y - u * 7.0); ctx.lineTo(x + u * 0.14, y - u * 7.6); ctx.lineTo(x + u * 0.9, y); ctx.closePath(); ctx.fill();
      ctx.strokeStyle = night ? "rgba(253,224,71,.3)" : "rgba(255,255,255,.5)"; ctx.lineWidth = Math.max(0.6, u * 0.04);
      ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x, y - u * 7.2); ctx.stroke();
    }
    function towerBridge(x, y, u, night) {
      var stone = night ? "#8E8476" : "#DCCFB5", blue = night ? "#60A5FA" : "#3B82F6", lt = night ? "#FDE68A" : "#F8FAFC";
      [-1, 1].forEach(function (sd) {
        var tx = x + sd * u * 2.3;
        rect(tx - u * 0.6, y - u * 4.5, u * 1.2, u * 4.5, stone);
        for (var i = 0; i < 4; i++) {
          var px = tx - u * 0.6 + i * u * 0.4;
          tri(px - u * 0.05, y - u * 4.5, px + u * 0.08, y - u * 5.2, px + u * 0.21, y - u * 4.5, night ? "#3F4566" : "#64748B");
        }
        tri(tx - u * 0.3, y - u * 4.5, tx, y - u * 5.6, tx + u * 0.3, y - u * 4.5, night ? "#3F4566" : "#64748B");
        ctx.strokeStyle = blue; ctx.lineWidth = Math.max(1, u * 0.12);
        ctx.beginPath(); ctx.moveTo(tx + sd * u * 0.6, y - u * 3.4); ctx.quadraticCurveTo(tx + sd * u * 2.2, y - u * 1.4, tx + sd * u * 3.4, y - u * 0.4); ctx.stroke();
        rect(tx - u * 0.28, y - u * 2.2, u * 0.56, u * 1.1, night ? "#1E1B2E" : "#8A7F69");
        if (night) { rect(tx - u * 0.18, y - u * 3.6, u * 0.12, u * 0.25, lt); rect(tx + u * 0.06, y - u * 3.6, u * 0.12, u * 0.25, lt); }
      });
      rect(x - u * 1.7, y - u * 4.0, u * 3.4, u * 0.22, blue);
      rect(x - u * 1.7, y - u * 3.6, u * 3.4, u * 0.18, blue);
      rect(x - u * 1.7, y - u * 1.0, u * 3.4, u * 0.2, night ? "#94A3B8" : "#CBD5E1");
    }

    /* ---------------------------------------------------------- ground */
    function quad(x1, y1, x2, y2, x3, y3, x4, y4) {
      ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.lineTo(x3, y3); ctx.lineTo(x4, y4); ctx.closePath(); ctx.fill();
    }
    function groundQuad(xa, xb, s0, s1) {
      var z0 = Math.max(Z_NEAR, zOf(s0)), z1 = Math.min(Z_FAR, zOf(s1));
      if (z1 <= z0) return;
      quad(PX(xa, z0), PY(0, z0), PX(xb, z0), PY(0, z0), PX(xb, z1), PY(0, z1), PX(xa, z1), PY(0, z1));
    }
    function drawGround(P, Q, t) {
      var dk = districtAt(dist + 30), DK = DIST[dk];
      // pavements fill everything below the horizon, then the road on top
      ctx.fillStyle = DK.walk;
      ctx.fillRect(-20, hy, W + 40, H - hy + 20);
      // the river under any bridge in view
      scen.forEach(function (o) {
        if (o.t !== "water") return;
        ctx.fillStyle = DIST[o.kind === "west" ? 1 : 3].water;
        groundQuad(-60, -ROAD - 0.66, o.s0, o.s1); groundQuad(ROAD + 0.66, 60, o.s0, o.s1);
        ctx.fillStyle = "rgba(255,255,255,.35)";
        for (var p = Math.ceil(dist / 3) * 3; p < o.s1; p += 3) {
          if (p < o.s0) continue;
          var off = ((p * 7.3) % 9) + 4.5;
          groundQuad(-off - 0.6, -off, p, p + 0.25); groundQuad(off, off + 0.6, p + 1.4, p + 1.65);
        }
      });
      var z0 = Z_NEAR, z1 = Z_FAR;
      ctx.fillStyle = DK.road;
      quad(PX(-ROAD, z0), PY(0, z0), PX(ROAD, z0), PY(0, z0), PX(ROAD, z1), PY(0, z1), PX(-ROAD, z1), PY(0, z1));
      // paving slabs: bands across the pavement
      ctx.fillStyle = DK.walk2;
      var first = Math.floor((dist - Z_CAT) / 2) * 2;
      for (var p = first; p < dist + Z_FAR - Z_CAT; p += 2) {
        groundQuad(-WALK, -ROAD - 0.16, p, p + 0.08);
        groundQuad(ROAD + 0.16, WALK, p, p + 0.08);
      }
      // kerbs
      ctx.fillStyle = "#E5E1D8";
      groundQuad(-ROAD - 0.16, -ROAD, dist - Z_CAT + Z_NEAR, dist + Z_FAR);
      groundQuad(ROAD, ROAD + 0.16, dist - Z_CAT + Z_NEAR, dist + Z_FAR);
      // London's double yellow lines
      ctx.fillStyle = "#FACC15";
      [-ROAD + 0.12, -ROAD + 0.25, ROAD - 0.18, ROAD - 0.31].forEach(function (x) { groundQuad(x, x + 0.06, dist - Z_CAT + Z_NEAR, dist + Z_FAR); });
      // lane markings
      ctx.fillStyle = DK.line;
      var dfirst = Math.floor((dist - Z_CAT) / 5) * 5;
      for (var q = dfirst; q < dist + Z_FAR; q += 5) {
        groundQuad(-LANE / 2 - 0.05, -LANE / 2 + 0.05, q, q + 2.2);
        groundQuad(LANE / 2 - 0.05, LANE / 2 + 0.05, q, q + 2.2);
      }
      // things painted on the road, and puddles
      objs.forEach(function (o) {
        var z = zOf(o.s);
        if (z < Z_NEAR || z > Z_FAR) return;
        if (o.t === "zebra") {
          ctx.fillStyle = "#F8FAFC";
          for (var x = -ROAD + 0.1; x < ROAD - 0.2; x += 0.5) groundQuad(x, x + 0.26, o.s, o.s + 2.2);
          ctx.fillStyle = "#F8FAFC";
          groundQuad(-ROAD, ROAD, o.s - 0.9, o.s - 0.8);
        } else if (o.t === "puddle" && !o.gone) {
          var lx = laneX(o.lane), k = F / z;
          ctx.globalAlpha = fade(z);
          ctx.fillStyle = "#3B5268";
          ctx.beginPath(); ctx.ellipse(PX(lx, z), PY(0, z + 0.6), 0.55 * k, Math.max(1, 0.3 * k * (camH / (z + 0.6))), 0, 0, 6.3); ctx.fill();
          ctx.fillStyle = "rgba(186,230,253,.55)";
          ctx.beginPath(); ctx.ellipse(PX(lx - 0.15, z), PY(0, z + 0.6), 0.25 * k, Math.max(0.6, 0.08 * k * (camH / (z + 0.6))), 0, 0, 6.3); ctx.fill();
          ctx.globalAlpha = 1;
        }
      });
    }
    function fade(z) { return z < Z_FADE ? 1 : clamp(1 - (z - Z_FADE) / (Z_FAR - Z_FADE), 0, 1); }

    /* --------------------------------------------------- the buildings */
    function drawScen(o) {
      if (o.t === "build") return building(o);
      var z = zOf(o.s0);
      if (z < Z_NEAR || z > Z_FAR) return;
      var k = F / z, x = o.side * (o.t === "blamp" || o.t === "tlamp" ? ROAD + 0.55 : ROAD + 0.75);
      var X = PX(x, z), Y = PY(0, z);
      ctx.globalAlpha = fade(z);
      var night = DIST[o.k || districtAt(o.s0)].lamp;
      if (o.t === "lamp") lamp(X, Y, k, night);
      else if (o.t === "tree") tree(X + o.side * 0.25 * k, Y, k, o);
      else if (o.t === "phone") phoneBox(X, Y, k, night);
      else if (o.t === "post") postBox(X, Y, k);
      else if (o.t === "bench") bench(X, Y, k, o.side);
      else if (o.t === "stop") busStop(X, Y, k);
      else if (o.t === "blamp") bridgeLamp(X, Y, k, "#166534", night);
      else if (o.t === "tlamp") bridgeLamp(X, Y, k, "#1D4ED8", 1);
      ctx.globalAlpha = 1;
      if (o.t === "blamp" || o.t === "tlamp") parapet(o);
    }
    function building(b) {
      var z0 = Math.max(Z_NEAR, zOf(b.s0)), z1 = Math.min(Z_FAR, zOf(b.s1));
      if (z1 <= z0 + 0.01) return;
      var x = b.side * WALK;
      ctx.globalAlpha = fade(z0);
      // the end wall, where it faces the camera
      if (zOf(b.s0) >= Z_NEAR) {
        ctx.fillStyle = b.col[1];
        var xe = b.side * (WALK + 8);
        quad(PX(x, z0), PY(0, z0), PX(x, z0), PY(b.h, z0), PX(xe, z0), PY(b.h, z0), PX(xe, z0), PY(0, z0));
      }
      ctx.fillStyle = b.col[0];
      quad(PX(x, z0), PY(0, z0), PX(x, z0), PY(b.h, z0), PX(x, z1), PY(b.h, z1), PX(x, z1), PY(0, z1));
      // a cornice along the top
      ctx.fillStyle = b.tower ? "rgba(255,255,255,.18)" : DIST[b.k].trim;
      var top = b.h, cz = 0.22;
      quad(PX(x, z0), PY(top - cz, z0), PX(x, z0), PY(top, z0), PX(x, z1), PY(top, z1), PX(x, z1), PY(top - cz, z1));
      // windows
      var P = DIST[b.k], len = b.s1 - b.s0, fh = (b.h - (b.shop ? 1.25 : 0.6)) / b.floors;
      var near = zOf(b.s0), far = zOf(b.s1);
      var big = F / Math.max(near, Z_NEAR) > 3;      // close enough for windows to show
      if (big) {
        for (var c = 0; c < b.cols; c++) {
          var sa = b.s0 + (c + 0.22) * len / b.cols, sb = b.s0 + (c + 0.78) * len / b.cols;
          var za = zOf(sa), zb = zOf(sb);
          if (zb < Z_NEAR || za > Z_FAR) continue;
          za = Math.max(Z_NEAR, za);
          for (var f = 0; f < b.floors; f++) {
            var y0 = (b.shop ? 1.25 : 0.6) + f * fh + fh * 0.2, y1 = y0 + fh * (b.tower ? 0.66 : 0.56);
            if (y1 > b.h - 0.25) continue;
            var lit = b.lit[f * b.cols + c];
            ctx.fillStyle = lit ? P.glass : b.tower ? (f % 2 ? P.win : "#5E86A8") : P.win;
            if (b.gothic && !b.tower) {
              var mx = PX(x, (za + zb) / 2);
              ctx.beginPath(); ctx.moveTo(PX(x, za), PY(y0, za)); ctx.lineTo(PX(x, za), PY(y1 - fh * 0.12, za));
              ctx.lineTo(mx, PY(y1 + fh * 0.08, (za + zb) / 2)); ctx.lineTo(PX(x, zb), PY(y1 - fh * 0.12, zb)); ctx.lineTo(PX(x, zb), PY(y0, zb)); ctx.closePath(); ctx.fill();
            } else quad(PX(x, za), PY(y0, za), PX(x, za), PY(y1, za), PX(x, zb), PY(y1, zb), PX(x, zb), PY(y0, zb));
          }
        }
        if (b.shop) {
          // a shop front with an awning
          ctx.fillStyle = b.awn;
          quad(PX(x, z0), PY(1.12, z0), PX(x, z0), PY(1.42, z0), PX(x, z1), PY(1.42, z1), PX(x, z1), PY(1.12, z1));
          ctx.fillStyle = "rgba(255,255,255,.55)";
          for (var st = 0; st < len; st += 0.5) {
            var q0 = zOf(b.s0 + st), q1 = zOf(b.s0 + st + 0.25);
            if (q1 < Z_NEAR || q0 > Z_FAR) continue;
            q0 = Math.max(Z_NEAR, q0);
            quad(PX(x, q0), PY(1.12, q0), PX(x, q0), PY(1.42, q0), PX(x, q1), PY(1.42, q1), PX(x, q1), PY(1.12, q1));
          }
          ctx.fillStyle = P.lit > 0.5 ? "#FDE68A" : "#5B7895";
          var g0 = zOf(b.s0 + 0.4), g1 = zOf(b.s1 - 0.4);
          if (g1 > Z_NEAR && g0 < Z_FAR) { g0 = Math.max(Z_NEAR, g0); quad(PX(x, g0), PY(0.15, g0), PX(x, g0), PY(1.0, g0), PX(x, g1), PY(1.0, g1), PX(x, g1), PY(0.15, g1)); }
        }
      }
      ctx.globalAlpha = 1;
    }
    function lamp(X, Y, k, night) {
      var w = Math.max(1, 0.06 * k);
      rect(X - w / 2, Y - 2.3 * k, w, 2.3 * k, "#1F2937");
      rect(X - w * 1.6, Y - 0.12 * k, w * 3.2, 0.12 * k, "#1F2937");
      var lx = X, ly = Y - 2.45 * k;
      if (night) {
        var g = ctx.createRadialGradient(lx, ly, 0, lx, ly, 0.9 * k);
        g.addColorStop(0, "rgba(253,230,138,.65)"); g.addColorStop(1, "rgba(253,230,138,0)");
        ctx.fillStyle = g; ctx.fillRect(lx - k, ly - k, 2 * k, 2 * k);
      }
      rect(lx - 0.11 * k, ly - 0.14 * k, 0.22 * k, 0.26 * k, night ? "#FDE68A" : "#E2E8F0");
      tri(lx - 0.15 * k, ly - 0.14 * k, lx, ly - 0.32 * k, lx + 0.15 * k, ly - 0.14 * k, "#1F2937");
    }
    function tree(X, Y, k, o) {
      rect(X - 0.07 * k, Y - 1.5 * k, 0.14 * k, 1.5 * k, "#6B4F3A");
      var sw = calm ? 0 : Math.sin(T * 1.3 + o.sway) * 0.04 * k;
      ctx.fillStyle = o.k === 3 ? "#1F4D3A" : o.k === 2 ? "#6E7F3A" : "#3F8F4B";
      ctx.beginPath();
      ctx.arc(X + sw, Y - 2.1 * k, 0.62 * k, 0, 6.3);
      ctx.arc(X - 0.42 * k + sw, Y - 1.8 * k, 0.45 * k, 0, 6.3);
      ctx.arc(X + 0.42 * k + sw, Y - 1.85 * k, 0.48 * k, 0, 6.3);
      ctx.fill();
      ctx.fillStyle = "rgba(255,255,255,.14)";
      ctx.beginPath(); ctx.arc(X - 0.18 * k + sw, Y - 2.3 * k, 0.28 * k, 0, 6.3); ctx.fill();
    }
    function phoneBox(X, Y, k, night) {
      var w = 0.5 * k, h = 1.55 * k;
      rect(X - w / 2, Y - h, w, h, "#C8102E");
      rect(X - w / 2 - 0.03 * k, Y - h - 0.08 * k, w + 0.06 * k, 0.12 * k, "#A50D26");
      ctx.fillStyle = "#A50D26"; ctx.beginPath(); ctx.ellipse(X, Y - h - 0.08 * k, w / 2, 0.08 * k, 0, Math.PI, 0); ctx.fill();
      rect(X - w * 0.36, Y - h + 0.08 * k, w * 0.72, 0.1 * k, "#1F2937");
      ctx.fillStyle = night ? "#FEF3C7" : "#BFD7EA";
      for (var r = 0; r < 4; r++) for (var c = 0; c < 2; c++) ctx.fillRect(X - w * 0.36 + c * w * 0.38, Y - h + 0.26 * k + r * 0.2 * k, w * 0.32, 0.15 * k);
      rect(X - w / 2, Y - 0.12 * k, w, 0.12 * k, "#7F0A1E");
    }
    function postBox(X, Y, k) {
      var w = 0.3 * k, h = 0.85 * k;
      rect(X - w / 2, Y - h, w, h, "#C8102E");
      ctx.fillStyle = "#1F2937"; ctx.beginPath(); ctx.ellipse(X, Y - h, w * 0.58, 0.07 * k, 0, 0, 6.3); ctx.fill();
      ctx.beginPath(); ctx.ellipse(X, Y - h - 0.02 * k, w * 0.5, 0.11 * k, 0, Math.PI, 0); ctx.fill();
      rect(X - w * 0.3, Y - h * 0.72, w * 0.6, 0.05 * k, "#1F2937");
      rect(X - w * 0.6, Y - 0.06 * k, w * 1.2, 0.06 * k, "#1F2937");
    }
    function bench(X, Y, k, side) {
      var w = 0.75 * k;
      rect(X - w / 2, Y - 0.42 * k, w, 0.07 * k, "#7C4A2B");
      rect(X - w / 2, Y - 0.62 * k, w, 0.06 * k, "#7C4A2B");
      rect(X - w * 0.42, Y - 0.42 * k, 0.04 * k, 0.42 * k, "#1F2937");
      rect(X + w * 0.38, Y - 0.42 * k, 0.04 * k, 0.42 * k, "#1F2937");
    }
    function busStop(X, Y, k) {
      rect(X - 0.03 * k, Y - 2.0 * k, 0.06 * k, 2.0 * k, "#334155");
      rect(X - 0.22 * k, Y - 2.15 * k, 0.44 * k, 0.32 * k, "#C8102E");
      rect(X - 0.17 * k, Y - 2.04 * k, 0.34 * k, 0.1 * k, "#FFFFFF");
    }
    function bridgeLamp(X, Y, k, colour, night) {
      rect(X - 0.04 * k, Y - 2.0 * k, 0.08 * k, 2.0 * k, colour);
      ctx.fillStyle = night ? "#FDE68A" : "#F8FAFC";
      ctx.beginPath(); ctx.arc(X, Y - 2.1 * k, 0.13 * k, 0, 6.3); ctx.fill();
      if (night) {
        var g = ctx.createRadialGradient(X, Y - 2.1 * k, 0, X, Y - 2.1 * k, 0.8 * k);
        g.addColorStop(0, "rgba(253,230,138,.6)"); g.addColorStop(1, "rgba(253,230,138,0)");
        ctx.fillStyle = g; ctx.fillRect(X - 0.8 * k, Y - 2.9 * k, 1.6 * k, 1.6 * k);
      }
    }
    function parapet(o) {
      // a low railing from this lamp to the next, along the bridge's edge
      var z0 = Math.max(Z_NEAR, zOf(o.s0)), z1 = Math.min(Z_FAR, zOf(o.s0 + 7));
      if (z1 <= z0) return;
      var x = o.side * (ROAD + 0.62);
      ctx.fillStyle = o.t === "blamp" ? "#15803D" : "#3B82F6";
      quad(PX(x, z0), PY(0.62, z0), PX(x, z0), PY(0.72, z0), PX(x, z1), PY(0.72, z1), PX(x, z1), PY(0.62, z1));
      quad(PX(x, z0), PY(0.05, z0), PX(x, z0), PY(0.14, z0), PX(x, z1), PY(0.14, z1), PX(x, z1), PY(0.05, z1));
      ctx.fillStyle = o.t === "blamp" ? "#166534" : "#1E40AF";
      for (var p = 0.5; p < 7; p += 0.5) {
        var z = zOf(o.s0 + p);
        if (z < Z_NEAR || z > Z_FAR) continue;
        var X = PX(x, z), k = F / z;
        ctx.fillRect(X - Math.max(0.5, 0.025 * k), PY(0.72, z), Math.max(1, 0.05 * k), 0.6 * k);
      }
    }

    /* ----------------------------------------------- things on the road */
    function drawObj(o) {
      var z = zOf(o.s);
      if (z > Z_FAR) return;
      if (o.t === "gate") return gate(o, z);
      if (o.t === "tower") return bigTower(o, z);
      if (z < Z_NEAR) return;
      var k = F / z, alpha = fade(z);
      ctx.globalAlpha = alpha;
      if (o.t === "beacon") beacon(PX(o.side * (ROAD + 0.35), z), PY(0, z), k);
      else if (o.t === "startarch" || o.t === "finish") arch(o, z, k);
      else if (!o.done || o.t === "bus" || o.t === "cab" || o.t === "pigeons") {
        var X = PX(laneX(o.lane), z), Y = PY(0, z);
        if (o.t === "gem") gem(X, PY(o.y + (calm ? 0 : Math.sin(T * 3 + o.s) * 0.06), z), k);
        else if (o.t === "cone") cone(X, Y, k, o.done);
        else if (o.t === "barrier" || o.t === "works") barrier(X, Y, k, o.t === "works");
        else if (o.t === "bus" || o.t === "cab") vehicle(o, z);
        else if (o.t === "pigeons") pigeons(o, z);
      }
      ctx.globalAlpha = 1;
    }
    function shadow(X, Y, w, k) {
      ctx.fillStyle = "rgba(15,23,42,.28)";
      ctx.beginPath(); ctx.ellipse(X, Y, w, Math.max(1, w * 0.22), 0, 0, 6.3); ctx.fill();
    }
    function gem(X, Y, k) {
      var w = 0.2 * k, h = 0.26 * k, spin = calm ? 1 : Math.cos(T * 4 + X * 0.01);
      var sx = Math.max(0.25, Math.abs(spin)) * w;
      ctx.fillStyle = "rgba(56,189,248,.25)";
      ctx.beginPath(); ctx.arc(X, Y - h * 0.1, w * 1.5, 0, 6.3); ctx.fill();
      ctx.fillStyle = GEMC[1]; quadP(X - sx, Y - h * 0.3, X - sx * 0.55, Y - h * 0.62, X + sx * 0.55, Y - h * 0.62, X + sx, Y - h * 0.3);
      ctx.fillStyle = GEMC[0]; quadP(X - sx * 0.55, Y - h * 0.62, X - sx * 0.1, Y - h * 0.3, X + sx * 0.1, Y - h * 0.3, X + sx * 0.55, Y - h * 0.62);
      ctx.fillStyle = spin > 0 ? GEMC[2] : GEMC[3];
      ctx.beginPath(); ctx.moveTo(X - sx, Y - h * 0.3); ctx.lineTo(X, Y + h * 0.5); ctx.lineTo(X + sx * 0.1, Y - h * 0.3); ctx.closePath(); ctx.fill();
      ctx.fillStyle = spin > 0 ? GEMC[3] : GEMC[2];
      ctx.beginPath(); ctx.moveTo(X + sx, Y - h * 0.3); ctx.lineTo(X, Y + h * 0.5); ctx.lineTo(X + sx * 0.1, Y - h * 0.3); ctx.closePath(); ctx.fill();
      ctx.strokeStyle = GEMC[4]; ctx.lineWidth = Math.max(0.6, 0.02 * k);
      ctx.beginPath(); ctx.moveTo(X - sx, Y - h * 0.3); ctx.lineTo(X - sx * 0.55, Y - h * 0.62); ctx.lineTo(X + sx * 0.55, Y - h * 0.62); ctx.lineTo(X + sx, Y - h * 0.3); ctx.lineTo(X, Y + h * 0.5); ctx.closePath(); ctx.stroke();
      if (!calm && Math.sin(T * 5 + X) > 0.92) { ctx.fillStyle = "#fff"; star4(X - sx * 0.4, Y - h * 0.5, w * 0.5); }
    }
    function quadP(a, b, c, d, e, f, g, h) { ctx.beginPath(); ctx.moveTo(a, b); ctx.lineTo(c, d); ctx.lineTo(e, f); ctx.lineTo(g, h); ctx.closePath(); ctx.fill(); }
    function star4(x, y, r) {
      ctx.beginPath(); ctx.moveTo(x, y - r); ctx.lineTo(x + r * 0.25, y - r * 0.25); ctx.lineTo(x + r, y); ctx.lineTo(x + r * 0.25, y + r * 0.25);
      ctx.lineTo(x, y + r); ctx.lineTo(x - r * 0.25, y + r * 0.25); ctx.lineTo(x - r, y); ctx.lineTo(x - r * 0.25, y - r * 0.25); ctx.closePath(); ctx.fill();
    }
    function cone(X, Y, k, knocked) {
      shadow(X, Y, 0.24 * k, k);
      rect(X - 0.22 * k, Y - 0.06 * k, 0.44 * k, 0.06 * k, "#1F2937");
      tri(X - 0.17 * k, Y - 0.06 * k, X, Y - 0.6 * k, X + 0.17 * k, Y - 0.06 * k, "#F97316");
      ctx.fillStyle = "#F8FAFC";
      quadP(X - 0.115 * k, Y - 0.24 * k, X - 0.08 * k, Y - 0.36 * k, X + 0.08 * k, Y - 0.36 * k, X + 0.115 * k, Y - 0.24 * k);
      ctx.fillStyle = "rgba(255,255,255,.3)";
      tri(X - 0.05 * k, Y - 0.1 * k, X - 0.01 * k, Y - 0.55 * k, X + 0.02 * k, Y - 0.1 * k, "rgba(255,255,255,.3)");
    }
    function barrier(X, Y, k, works) {
      var w = (works ? 1.05 : 0.95) * k, h = (works ? 0.7 : 0.62) * k;
      shadow(X, Y, w * 0.55, k);
      rect(X - w * 0.42, Y - h, 0.06 * k, h, "#334155"); rect(X + w * 0.42 - 0.06 * k, Y - h, 0.06 * k, h, "#334155");
      ctx.save();
      ctx.beginPath(); ctx.rect(X - w / 2, Y - h, w, 0.24 * k); ctx.clip();
      rect(X - w / 2, Y - h, w, 0.24 * k, "#F8FAFC");
      ctx.fillStyle = "#DC2626";
      for (var i = -2; i < 8; i++) { var x0 = X - w / 2 + i * 0.2 * k; quadP(x0, Y - h + 0.24 * k, x0 + 0.1 * k, Y - h + 0.24 * k, x0 + 0.2 * k, Y - h, x0 + 0.1 * k, Y - h); }
      ctx.restore();
      ctx.strokeStyle = "#7F1D1D"; ctx.lineWidth = Math.max(0.6, 0.02 * k); ctx.strokeRect(X - w / 2, Y - h, w, 0.24 * k);
      var on = calm || Math.sin(T * 8) > 0;
      ctx.fillStyle = on ? "#FBBF24" : "#B45309";
      ctx.beginPath(); ctx.arc(X, Y - h - 0.08 * k, 0.07 * k, 0, 6.3); ctx.fill();
      if (works) {
        rect(X - 0.32 * k, Y - h - 0.62 * k, 0.64 * k, 0.4 * k, "#FDE047");
        ctx.strokeStyle = "#1F2937"; ctx.lineWidth = Math.max(0.6, 0.025 * k); ctx.strokeRect(X - 0.32 * k, Y - h - 0.62 * k, 0.64 * k, 0.4 * k);
        rect(X - 0.02 * k, Y - h - 0.22 * k, 0.04 * k, 0.16 * k, "#334155");
        if (k > 14) {
          ctx.fillStyle = "#1F2937"; ctx.font = "800 " + Math.round(0.13 * k) + "px Poppins, sans-serif"; ctx.textAlign = "center"; ctx.textBaseline = "middle";
          ctx.fillText("ROAD", X, Y - h - 0.5 * k); ctx.fillText("CLOSED", X, Y - h - 0.34 * k);
        }
      }
    }
    function vehicle(o, z) {
      var bus = o.t === "bus", w = bus ? 1.12 : 0.98, h = bus ? 2.75 : 1.42, x = laneX(o.lane);
      var zr = Math.max(Z_NEAR + 0.01, z), zf = Math.min(Z_FAR, zOf(o.s + o.len));
      var body = bus ? "#DA1F26" : o.col || "#111827", dark = bus ? "#A3161C" : "#030712";
      var side = x - camX > 0 ? -1 : 1;     // the side that faces the middle of the view
      var xs = x + side * w / 2;
      if (zf > zr && Math.abs(x - camX) > 0.12) {
        ctx.fillStyle = dark;
        quad(PX(xs, zr), PY(0.12, zr), PX(xs, zr), PY(h, zr), PX(xs, zf), PY(h, zf), PX(xs, zf), PY(0.12, zf));
        ctx.fillStyle = bus ? "#1E293B" : "#1F2937";
        if (bus) {
          for (var d = 0; d < 2; d++) {
            var y0 = d ? 1.75 : 0.85, y1 = d ? 2.4 : 1.45;
            for (var p = 0.3; p < o.len - 0.3; p += 0.75) {
              var za = zOf(o.s + p), zb = zOf(o.s + p + 0.6);
              if (zb < Z_NEAR) continue;
              za = Math.max(Z_NEAR, za);
              quad(PX(xs, za), PY(y0, za), PX(xs, za), PY(y1, za), PX(xs, zb), PY(y1, zb), PX(xs, zb), PY(y0, zb));
            }
          }
        } else {
          var w0 = zOf(o.s + 0.5), w1 = zOf(o.s + o.len - 0.4);
          w0 = Math.max(Z_NEAR, w0);
          if (w1 > w0) quad(PX(xs, w0), PY(0.85, w0), PX(xs, w0), PY(1.3, w0), PX(xs, w1), PY(1.3, w1), PX(xs, w1), PY(0.85, w1));
        }
      }
      if (camH > h && zf > zr) {            // the roof, from above
        ctx.fillStyle = bus ? "#B91C1C" : "#1F2937";
        quad(PX(x - w / 2, zr), PY(h, zr), PX(x + w / 2, zr), PY(h, zr), PX(x + w / 2, zf), PY(h, zf), PX(x - w / 2, zf), PY(h, zf));
      }
      var k = F / zr, X = PX(x, zr), Y = PY(0, zr);
      ctx.globalAlpha = fade(zr);
      // the back of the vehicle
      rect(X - w / 2 * k, Y - h * k, w * k, (h - 0.12) * k, body);
      rect(X - w * 0.42 * k, Y - 0.12 * k, 0.2 * k, 0.12 * k, "#0F172A"); rect(X + w * 0.42 * k - 0.2 * k, Y - 0.12 * k, 0.2 * k, 0.12 * k, "#0F172A");
      if (bus) {
        rect(X - w * 0.4 * k, Y - 2.55 * k, w * 0.8 * k, 0.6 * k, "#1E293B");
        rect(X - w * 0.36 * k, Y - 2.5 * k, w * 0.72 * k, 0.12 * k, "rgba(255,255,255,.18)");
        rect(X - w * 0.4 * k, Y - 1.62 * k, w * 0.8 * k, 0.5 * k, "#1E293B");
        rect(X - w * 0.5 * k, Y - 1.86 * k, w * k, 0.08 * k, "#F8FAFC");
        rect(X - w * 0.2 * k, Y - 0.82 * k, w * 0.4 * k, 0.36 * k, "#0F172A");
        rect(X - w * 0.15 * k, Y - 0.75 * k, w * 0.3 * k, 0.16 * k, "#64748B");
      } else {
        rect(X - w * 0.36 * k, Y - 1.3 * k, w * 0.72 * k, 0.38 * k, "#1E293B");
        rect(X - w * 0.3 * k, Y - 1.27 * k, w * 0.6 * k, 0.08 * k, "rgba(255,255,255,.2)");
        rect(X - 0.18 * k, Y - h * k - 0.14 * k, 0.36 * k, 0.15 * k, DIST[districtAt(o.s)].lamp ? "#FDE047" : "#FCD34D");
        if (k > 18) { ctx.fillStyle = "#111827"; ctx.font = "800 " + Math.round(0.1 * k) + "px Poppins, sans-serif"; ctx.textAlign = "center"; ctx.textBaseline = "middle"; ctx.fillText("TAXI", X, Y - h * k - 0.065 * k); }
      }
      // yellow number plate and red lights
      rect(X - 0.2 * k, Y - (bus ? 0.4 : 0.42) * k, 0.4 * k, 0.11 * k, "#FACC15");
      var glow = DIST[districtAt(o.s)].lamp;
      [-1, 1].forEach(function (sd) {
        ctx.fillStyle = "#EF4444";
        ctx.fillRect(X + sd * w * 0.4 * k - 0.07 * k, Y - (bus ? 0.62 : 0.66) * k, 0.14 * k, 0.16 * k);
        if (glow) {
          var g = ctx.createRadialGradient(X + sd * w * 0.4 * k, Y - 0.55 * k, 0, X + sd * w * 0.4 * k, Y - 0.55 * k, 0.4 * k);
          g.addColorStop(0, "rgba(239,68,68,.55)"); g.addColorStop(1, "rgba(239,68,68,0)");
          ctx.fillStyle = g; ctx.fillRect(X + sd * w * 0.4 * k - 0.4 * k, Y - 0.95 * k, 0.8 * k, 0.8 * k);
        }
      });
      if (bus && k > 16) {
        ctx.fillStyle = "#FDE047"; ctx.font = "800 " + Math.round(0.16 * k) + "px Poppins, sans-serif"; ctx.textAlign = "center"; ctx.textBaseline = "middle";
        ctx.fillText(String(o.n), X, Y - 2.3 * k);
      }
      ctx.globalAlpha = 1;
    }
    function pigeons(o, z) {
      o.birds.forEach(function (b) {
        var bz = z + b.ds, X, Y, k;
        if (b.fly) {
          b.fly += 1 / 60;
          var fz = Math.max(Z_NEAR + 0.2, bz + b.vz * b.fly);
          k = F / fz;
          X = PX(laneX(o.lane) + b.dx + b.vx * b.fly, fz);
          Y = PY(0.15 + b.vy * b.fly * 1.1, fz);
        } else {
          if (bz < Z_NEAR) return;
          k = F / bz; X = PX(laneX(o.lane) + b.dx, bz); Y = PY(0, bz);
        }
        if (b.fly > 2.5) return;
        var s = 0.16 * k;
        if (!b.fly) shadow(X, Y, s * 0.8, k);
        ctx.fillStyle = "#7C8796";
        ctx.beginPath(); ctx.ellipse(X, Y - s * 0.6, s * 0.9, s * 0.55, 0, 0, 6.3); ctx.fill();
        var peck = b.fly || calm ? 0 : Math.max(0, Math.sin(T * 6 + b.ph)) * s * 0.35;
        ctx.fillStyle = "#5B6573";
        ctx.beginPath(); ctx.arc(X + s * 0.7, Y - s * 1.0 + peck, s * 0.38, 0, 6.3); ctx.fill();
        ctx.fillStyle = "#F59E0B"; tri(X + s * 1.0, Y - s * 1.02 + peck, X + s * 1.28, Y - s * 0.92 + peck, X + s * 1.0, Y - s * 0.86 + peck, "#F59E0B");
        ctx.fillStyle = "#4ADE80"; ctx.beginPath(); ctx.arc(X + s * 0.45, Y - s * 0.72, s * 0.16, 0, 6.3); ctx.fill();
        if (b.fly) {
          var flap = Math.sin(T * 30 + b.ph) * s * 0.9;
          tri(X - s * 0.2, Y - s * 0.7, X - s * 1.3, Y - s * 0.7 - flap, X + s * 0.2, Y - s * 0.55, "#94A3B8");
          tri(X + s * 0.2, Y - s * 0.7, X + s * 1.3, Y - s * 0.7 - flap, X - s * 0.2, Y - s * 0.55, "#94A3B8");
        }
      });
    }
    function beacon(X, Y, k) {
      var w = Math.max(1, 0.07 * k);
      for (var i = 0; i < 8; i++) rect(X - w / 2, Y - (i + 1) * 0.2 * k, w, 0.2 * k, i % 2 ? "#F8FAFC" : "#111827");
      var on = calm || Math.sin(T * 5) > -0.2;
      if (on) {
        var g = ctx.createRadialGradient(X, Y - 1.75 * k, 0, X, Y - 1.75 * k, 0.5 * k);
        g.addColorStop(0, "rgba(251,146,60,.6)"); g.addColorStop(1, "rgba(251,146,60,0)");
        ctx.fillStyle = g; ctx.fillRect(X - 0.5 * k, Y - 2.25 * k, k, k);
      }
      ctx.fillStyle = on ? "#FB923C" : "#C2410C";
      ctx.beginPath(); ctx.arc(X, Y - 1.75 * k, 0.15 * k, 0, 6.3); ctx.fill();
    }
    function arch(o, z, k) {
      var finish = o.t === "finish";
      var X0 = PX(-ROAD - 0.1, z), X1 = PX(ROAD + 0.1, z), Y = PY(0, z), top = PY(2.7, z);
      rect(X0 - 0.08 * k, top, 0.16 * k, Y - top, "#F8FAFC");
      rect(X1 - 0.08 * k, top, 0.16 * k, Y - top, "#F8FAFC");
      var bh = 0.5 * k;
      ctx.save(); ctx.beginPath(); ctx.rect(X0, top - bh * 0.2, X1 - X0, bh); ctx.clip();
      for (var i = 0; i * bh * 0.25 < X1 - X0; i++) for (var j = 0; j < 4; j++) {
        ctx.fillStyle = (i + j) % 2 ? "#111827" : "#F8FAFC";
        ctx.fillRect(X0 + i * bh * 0.25, top - bh * 0.2 + j * bh * 0.25, bh * 0.25, bh * 0.25);
      }
      ctx.restore();
      if (k > 10) {
        var label = finish ? "FINISH" : "CITY RUN";
        ctx.font = "800 " + Math.round(0.36 * k) + "px Poppins, sans-serif"; ctx.textAlign = "center"; ctx.textBaseline = "middle";
        var tw = ctx.measureText(label).width + 0.4 * k;
        rect((X0 + X1) / 2 - tw / 2, top - bh * 0.95, tw, bh * 0.75, finish ? "#DC2626" : "#1D4ED8");
        ctx.fillStyle = "#fff"; ctx.fillText(label, (X0 + X1) / 2, top - bh * 0.57);
      }
    }
    /* Tower Bridge at the finish: each tower stands across the road, which
       runs through an arch in its middle. */
    function bigTower(o, z) {
      if (z < Z_NEAR + 0.2) return;
      var k = F / z, Y = PY(0, z), Xc = PX(0, z), half = (ROAD + 1.7) * k, hgt = 9 * k, arch = 3.9 * k, road = (ROAD + 0.15) * k;
      var stone = "#A89F8E", dark = "#6E6758", lit = "#FDE68A";
      ctx.globalAlpha = fade(z);
      ctx.fillStyle = stone;
      ctx.beginPath();
      ctx.moveTo(Xc - half, Y); ctx.lineTo(Xc - half, Y - hgt); ctx.lineTo(Xc + half, Y - hgt); ctx.lineTo(Xc + half, Y);
      ctx.lineTo(Xc + road, Y); ctx.lineTo(Xc + road, Y - arch * 0.75); ctx.quadraticCurveTo(Xc, Y - arch * 1.2, Xc - road, Y - arch * 0.75); ctx.lineTo(Xc - road, Y);
      ctx.closePath(); ctx.fill();
      rect(Xc - half, Y - hgt, half * 2, 0.25 * k, dark);
      for (var i = 0; i < 4; i++) {
        var tx = Xc - half + (i + 0.5) * half / 2;
        tri(tx - 0.42 * k, Y - hgt, tx, Y - hgt - 1.6 * k, tx + 0.42 * k, Y - hgt, "#334155");
        rect(tx - 0.08 * k, Y - hgt - 2.0 * k, 0.16 * k, 0.45 * k, "#E9C46A");
      }
      for (var r = 0; r < 3; r++) for (var c = -2; c <= 2; c++) {
        var wx = Xc + c * half * 0.32, wy = Y - hgt + (1.2 + r * 1.3) * k;
        rect(wx - 0.18 * k, wy, 0.36 * k, 0.75 * k, r === 2 && Math.abs(c) < 2 ? dark : lit);
      }
      // the high walkways, in blue and white
      rect(Xc - half, Y - hgt + 0.6 * k, half * 2, 0.35 * k, "#2563EB");
      rect(Xc - half, Y - hgt + 0.95 * k, half * 2, 0.12 * k, "#F8FAFC");
      ctx.strokeStyle = "#2563EB"; ctx.lineWidth = Math.max(1, 0.16 * k);
      ctx.beginPath(); ctx.moveTo(Xc - half, Y - hgt * 0.7); ctx.quadraticCurveTo(Xc - half - 3 * k, Y - hgt * 0.3, Xc - half - 6 * k, Y - 0.6 * k);
      ctx.moveTo(Xc + half, Y - hgt * 0.7); ctx.quadraticCurveTo(Xc + half + 3 * k, Y - hgt * 0.3, Xc + half + 6 * k, Y - 0.6 * k); ctx.stroke();
      ctx.globalAlpha = 1;
    }

    /* The answer gates. Each answer lane gets a banner in its colour with
       its letter, and the cat bursts through the one it is in. */
    function gate(o, z) {
      var g = o.g;
      if (z < Z_NEAR + 0.05) return;
      var k = F / z, Y = PY(0, z), age = g.passed ? T - g.burst : -1;
      ctx.globalAlpha = fade(z);
      for (var l = 0; l < 3; l++) {
        var L = g.lanes[l];
        if (!L) continue;
        var x = laneX(l), X0 = PX(x - 0.56, z), X1 = PX(x + 0.56, z), top = PY(2.05, z), w = X1 - X0;
        var chosen = g.passed && g.chosen === l, right = g.passed && g.res && g.res.right === l;
        rect(X0 - 0.05 * k, top, 0.1 * k, Y - top, "#E2E8F0");
        rect(X1 - 0.05 * k, top, 0.1 * k, Y - top, "#E2E8F0");
        rect(X0 - 0.08 * k, top - 0.08 * k, w + 0.16 * k, 0.3 * k, L.c);
        if (!chosen) {
          // the paper banner, with the letter and the answer's first words
          ctx.globalAlpha = fade(z) * (g.passed && !right ? 0.55 : 0.92);
          rect(X0 + 0.04 * k, top + 0.22 * k, w - 0.08 * k, Y - top - 0.32 * k, L.c);
          ctx.globalAlpha = fade(z);
          ctx.fillStyle = "rgba(255,255,255,.16)";
          for (var st = 0; st < 3; st++) ctx.fillRect(X0 + 0.04 * k, top + (0.5 + st * 0.5) * k, w - 0.08 * k, 0.05 * k);
          var cy = PY(1.32, z);
          ctx.fillStyle = "#fff";
          ctx.beginPath(); ctx.arc((X0 + X1) / 2, cy, 0.27 * k, 0, 6.3); ctx.fill();
          if (L.icon) {
            var mx = (X0 + X1) / 2, r = 0.12 * k;
            ctx.strokeStyle = L.ink || L.c; ctx.lineWidth = Math.max(1.5, 0.07 * k); ctx.lineCap = "round"; ctx.lineJoin = "round";
            ctx.beginPath();
            if (L.icon === "tick") { ctx.moveTo(mx - r, cy + 0.01 * k); ctx.lineTo(mx - r * 0.25, cy + r * 0.75); ctx.lineTo(mx + r * 1.05, cy - r * 0.8); }
            else { ctx.moveTo(mx - r * 0.8, cy - r * 0.8); ctx.lineTo(mx + r * 0.8, cy + r * 0.8); ctx.moveTo(mx + r * 0.8, cy - r * 0.8); ctx.lineTo(mx - r * 0.8, cy + r * 0.8); }
            ctx.stroke();
          } else if (k > 7) {
            ctx.fillStyle = L.ink || L.c; ctx.textAlign = "center"; ctx.textBaseline = "middle";
            ctx.font = "800 " + Math.round(0.34 * k) + "px Poppins, sans-serif";
            ctx.fillText(L.t, (X0 + X1) / 2, cy + 0.02 * k);
          }
          if (k > 26 && L.s) {
            ctx.fillStyle = "#fff"; ctx.font = "700 " + Math.round(0.135 * k) + "px Inter, sans-serif";
            wrapText(L.s, (X0 + X1) / 2, PY(0.78, z), w - 0.2 * k, 0.16 * k, 3);
          }
          if (right && g.res && !g.res.ok) {
            ctx.strokeStyle = "#4ADE80"; ctx.lineWidth = Math.max(2, 0.08 * k);
            ctx.strokeRect(X0 + 0.04 * k, top + 0.22 * k, w - 0.08 * k, Y - top - 0.32 * k);
          }
        } else if (age < 0.25) {
          ctx.globalAlpha = fade(z) * (1 - age / 0.25);
          rect(X0, top + 0.22 * k, w, Y - top - 0.32 * k, "#fff");
          ctx.globalAlpha = fade(z);
        }
      }
      ctx.globalAlpha = 1;
    }
    function wrapText(text, x, y, maxW, lh, maxLines) {
      var words = String(text).split(/\s+/), lines = [], line = "";
      for (var i = 0; i < words.length; i++) {
        var test = line ? line + " " + words[i] : words[i];
        if (ctx.measureText(test).width > maxW && line) { lines.push(line); line = words[i]; } else line = test;
        if (lines.length === maxLines) break;
      }
      if (lines.length < maxLines && line) lines.push(line);
      if (lines.length === maxLines && (i < words.length)) {
        var lastL = lines[maxLines - 1];
        while (lastL.length > 1 && ctx.measureText(lastL + "…").width > maxW) lastL = lastL.slice(0, -1);
        lines[maxLines - 1] = lastL + "…";
      }
      lines.forEach(function (l, n) { ctx.fillText(l, x, y + n * lh); });
    }

    /* ----------------------------------------------------------- the cat
       Seen from behind: its head and ears, a silver body, the two hind legs
       that show their pink paw pads as they kick up, and a jointed tail with
       red and blue wires. */
    function drawCat() {
      var k = F / Z_CAT, gx = PX(cat.x, Z_CAT), gy = PY(0, Z_CAT);
      var blink = cat.safe > 0 && !calm && cat.hurt <= 0 && Math.floor(T * 12) % 2 === 0;
      var run = v > 0.6 && started;
      var bob = run && !calm ? Math.abs(Math.sin(cat.phase)) * 0.045 * k : Math.sin(T * 2.4) * 0.01 * k;
      ctx.save();
      ctx.globalAlpha = 0.3 * Math.max(0.25, 1 - cat.y / 1.4);
      ctx.fillStyle = "#020617";
      ctx.beginPath(); ctx.ellipse(gx, gy, 0.34 * k * (1 - cat.y * 0.18), 0.08 * k, 0, 0, 6.3); ctx.fill();
      ctx.restore();
      ctx.save();
      if (blink) ctx.globalAlpha = 0.4;
      ctx.translate(gx, gy - cat.y * k - bob);
      var wob = cat.hurt > 0 && !calm ? Math.sin(T * 40) * 0.18 * cat.hurt : 0;
      ctx.rotate(cat.lean * 0.6 + wob);
      var sq = cat.squash;
      ctx.scale(1 + sq * 0.5, 1 - sq);
      ctx.scale(k * 0.9, k * 0.9);
      ctx.lineJoin = "round"; ctx.lineCap = "round";
      var lw = Math.max(1.2, 0.022 * k) / (k * 0.9);
      var ph = cat.phase, air = cat.y > 0.05;
      var lift = function (i) { return air ? 0.06 : run ? Math.max(0, Math.sin(ph + i * Math.PI)) * 0.13 : 0; };
      var metal = ctx.createLinearGradient(-0.3, -1.1, 0.3, 0);
      metal.addColorStop(0, "#FFFFFF"); metal.addColorStop(0.4, "#E2E8F0"); metal.addColorStop(0.8, "#B8C4D3"); metal.addColorStop(1, "#8D9AAB");
      var ink = "#334155";
      // head, further away than the body, so drawn first
      var hb = run && !calm ? Math.sin(ph * 2 + 0.6) * 0.012 : 0;
      ctx.save(); ctx.translate(0, hb);
      [-1, 1].forEach(function (sd) {
        ctx.fillStyle = metal; ctx.strokeStyle = ink; ctx.lineWidth = lw;
        ctx.beginPath(); ctx.moveTo(sd * 0.235, -0.86); ctx.lineTo(sd * 0.21, -1.19); ctx.lineTo(sd * 0.065, -1.0); ctx.closePath(); ctx.fill(); ctx.stroke();
        ctx.fillStyle = "#94A3B8";
        ctx.beginPath(); ctx.moveTo(sd * 0.2, -0.9); ctx.lineTo(sd * 0.195, -1.1); ctx.lineTo(sd * 0.1, -0.99); ctx.closePath(); ctx.fill();
      });
      ctx.fillStyle = metal; ctx.strokeStyle = ink; ctx.lineWidth = lw;
      ctx.beginPath(); ctx.ellipse(0, -0.8, 0.27, 0.245, 0, 0, 6.3); ctx.fill(); ctx.stroke();
      ctx.strokeStyle = "#94A3B8"; ctx.lineWidth = lw * 0.8;
      ctx.beginPath(); ctx.moveTo(0, -1.04); ctx.lineTo(0, -0.6); ctx.moveTo(-0.24, -0.76); ctx.quadraticCurveTo(0, -0.66, 0.24, -0.76); ctx.stroke();
      ctx.fillStyle = "#1E293B"; ctx.beginPath(); ctx.ellipse(0, -0.93, 0.075, 0.045, 0, 0, 6.3); ctx.fill();
      ctx.fillStyle = "#64748B"; ctx.beginPath(); ctx.arc(0, -0.93, 0.03, 0, 6.3); ctx.fill();
      ctx.strokeStyle = "#DC2626"; ctx.lineWidth = lw * 1.2; ctx.beginPath(); ctx.moveTo(-0.06, -0.92); ctx.quadraticCurveTo(-0.02, -0.96, 0.0, -0.92); ctx.stroke();
      ctx.strokeStyle = "#2563EB"; ctx.beginPath(); ctx.moveTo(0.0, -0.92); ctx.quadraticCurveTo(0.03, -0.88, 0.06, -0.93); ctx.stroke();
      [[-0.17, -0.97], [0.17, -0.97], [-0.23, -0.72], [0.23, -0.72]].forEach(function (p) { ctx.fillStyle = "#64748B"; ctx.beginPath(); ctx.arc(p[0], p[1], 0.014, 0, 6.3); ctx.fill(); });
      ctx.restore();
      // the neck: dark, with a wire showing
      ctx.fillStyle = "#1E293B"; ctx.beginPath(); ctx.ellipse(0, -0.58, 0.15, 0.05, 0, 0, 6.3); ctx.fill();
      // front paws, peeking out either side
      [-1, 1].forEach(function (sd, i) {
        var up = lift(i + 1) * 0.7;
        ctx.fillStyle = "#CBD5E1"; ctx.strokeStyle = ink; ctx.lineWidth = lw;
        ctx.beginPath(); ctx.ellipse(sd * 0.215, -0.06 - up, 0.07, 0.05, 0, 0, 6.3); ctx.fill(); ctx.stroke();
      });
      // body
      ctx.fillStyle = metal; ctx.strokeStyle = ink; ctx.lineWidth = lw;
      ctx.beginPath(); ctx.ellipse(0, -0.38, 0.27, 0.235, 0, 0, 6.3); ctx.fill(); ctx.stroke();
      ctx.strokeStyle = "#94A3B8"; ctx.lineWidth = lw * 0.8;
      ctx.beginPath(); ctx.moveTo(0, -0.6); ctx.lineTo(0, -0.24); ctx.stroke();
      [[-0.05, -0.55], [0.05, -0.55], [-0.05, -0.42], [0.05, -0.42]].forEach(function (p) { ctx.fillStyle = "#64748B"; ctx.beginPath(); ctx.arc(p[0], p[1], 0.012, 0, 6.3); ctx.fill(); });
      ctx.fillStyle = "rgba(255,255,255,.55)"; ctx.beginPath(); ctx.ellipse(-0.12, -0.5, 0.06, 0.1, -0.5, 0, 6.3); ctx.fill();
      // hind legs: a paw that kicks up shows its pads
      [-1, 1].forEach(function (sd, i) {
        var up = lift(i), x = sd * 0.125;
        ctx.fillStyle = metal; ctx.strokeStyle = ink; ctx.lineWidth = lw;
        roundRect(x - 0.07, -0.27, 0.14, 0.27 - up, 0.06); ctx.fill(); ctx.stroke();
        ctx.fillStyle = "#475569"; ctx.beginPath(); ctx.arc(x, -0.2, 0.028, 0, 6.3); ctx.fill();
        ctx.fillStyle = "#334155"; ctx.beginPath(); ctx.ellipse(x, -up - 0.005, 0.072, 0.04, 0, 0, 6.3); ctx.fill();
        if (up > 0.05) {
          ctx.fillStyle = "#F9A8D4";
          ctx.beginPath(); ctx.ellipse(x, -up + 0.005, 0.03, 0.02, 0, 0, 6.3); ctx.fill();
          [-0.04, 0, 0.04].forEach(function (t2) { ctx.beginPath(); ctx.arc(x + t2, -up - 0.03, 0.012, 0, 6.3); ctx.fill(); });
        }
      });
      // the tail curls up and to one side, swishing as the cat runs
      var sw = calm ? 0.2 : Math.sin(T * (run ? 7 : 2.5)) * (run ? 0.35 : 0.2);
      var px0 = 0.02, py0 = -0.26, ang = -1.25 + sw * 0.3, seg = 0.085;
      var pts = [[px0, py0]];
      for (var j = 0; j < 8; j++) {
        ang += 0.14 + sw * 0.05 - (j > 5 ? 0.35 : 0);
        px0 += Math.cos(ang) * seg; py0 += Math.sin(ang) * seg;
        pts.push([px0, py0]);
      }
      ctx.beginPath(); ctx.moveTo(pts[0][0], pts[0][1]);
      for (var n = 1; n < pts.length; n++) ctx.lineTo(pts[n][0], pts[n][1]);
      ctx.strokeStyle = ink; ctx.lineWidth = 0.112; ctx.stroke();
      ctx.strokeStyle = "#D5DDE7"; ctx.lineWidth = 0.112 - lw * 2; ctx.stroke();
      ctx.strokeStyle = "rgba(255,255,255,.75)"; ctx.lineWidth = 0.025;
      ctx.beginPath(); ctx.moveTo(pts[0][0] - 0.02, pts[0][1]);
      for (n = 1; n < pts.length; n++) ctx.lineTo(pts[n][0] - 0.02, pts[n][1] - 0.012);
      ctx.stroke();
      for (n = 1; n < pts.length - 1; n++) {
        var ax = pts[n + 1][0] - pts[n - 1][0], ay = pts[n + 1][1] - pts[n - 1][1], al = Math.sqrt(ax * ax + ay * ay) || 1;
        var nx = -ay / al * 0.056, ny = ax / al * 0.056;
        ctx.strokeStyle = "#475569"; ctx.lineWidth = lw * 1.6;
        ctx.beginPath(); ctx.moveTo(pts[n][0] - nx, pts[n][1] - ny); ctx.lineTo(pts[n][0] + nx, pts[n][1] + ny); ctx.stroke();
        if (n % 2) { ctx.fillStyle = n % 4 === 1 ? "#DC2626" : "#2563EB"; ctx.beginPath(); ctx.arc(pts[n][0] + nx * 0.55, pts[n][1] + ny * 0.55, 0.014, 0, 6.3); ctx.fill(); }
      }
      ctx.fillStyle = "#F1F5F9"; ctx.strokeStyle = ink;
      var tip = pts[pts.length - 1];
      ctx.beginPath(); ctx.arc(tip[0], tip[1], 0.06, 0, 6.3); ctx.fill(); ctx.stroke();
      if (cat.cheer > 0 && !calm) {
        ctx.fillStyle = "#FDE047";
        for (var c = 0; c < 4; c++) { var a = T * 6 + c * 1.57; ctx.save(); ctx.translate(Math.cos(a) * 0.42, -0.85 + Math.sin(a) * 0.18); star4(0, 0, 0.06); ctx.restore(); }
      }
      if (cat.hurt > 0) {
        for (var h2 = 0; h2 < 3; h2++) {
          var b2 = T * 7 + h2 * 2.09;
          ctx.fillStyle = h2 === 1 ? "#FB923C" : "#FDE047";
          ctx.save(); ctx.translate(Math.cos(b2) * 0.3, -1.12 + Math.sin(b2) * 0.07); star4(0, 0, 0.055); ctx.restore();
        }
      }
      ctx.restore();
    }
    function roundRect(x, y, w, h, r) {
      ctx.beginPath(); ctx.moveTo(x + r, y); ctx.lineTo(x + w - r, y); ctx.quadraticCurveTo(x + w, y, x + w, y + r);
      ctx.lineTo(x + w, y + h - r); ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h); ctx.lineTo(x + r, y + h);
      ctx.quadraticCurveTo(x, y + h, x, y + h - r); ctx.lineTo(x, y + r); ctx.quadraticCurveTo(x, y, x + r, y); ctx.closePath();
    }

    function drawParts() {
      parts.forEach(function (p) {
        var a = clamp(p.life / p.max, 0, 1);
        ctx.globalAlpha = a;
        if (p.kind === "gem" || p.kind === "gemlost") {
          ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.a * 0.2);
          var r = p.r;
          ctx.fillStyle = GEMC[1]; quadP(-r, -r * 0.2, -r * 0.55, -r * 0.6, r * 0.55, -r * 0.6, r, -r * 0.2);
          ctx.fillStyle = GEMC[2]; ctx.beginPath(); ctx.moveTo(-r, -r * 0.2); ctx.lineTo(0, r * 0.8); ctx.lineTo(r, -r * 0.2); ctx.closePath(); ctx.fill();
          ctx.fillStyle = GEMC[0]; quadP(-r * 0.55, -r * 0.6, -r * 0.1, -r * 0.2, r * 0.1, -r * 0.2, r * 0.55, -r * 0.6);
          ctx.restore();
        } else if (p.kind === "paper" || p.kind === "confetti") {
          ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.a);
          ctx.fillStyle = p.c || "#fff"; ctx.fillRect(-p.r, -p.r * 0.45, p.r * 2, p.r * 0.9);
          ctx.restore();
        } else if (p.kind === "sparkle") {
          ctx.fillStyle = "#fff"; star4(p.x, p.y, p.r * 1.6);
        } else {
          ctx.fillStyle = p.c || "#fff"; ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, 6.3); ctx.fill();
        }
      });
      ctx.globalAlpha = 1;
    }
    function speedLines() {
      ctx.strokeStyle = "rgba(255,255,255,.5)"; ctx.lineWidth = 2;
      for (var i = 0; i < 16; i++) {
        var a = (i / 16) * Math.PI * 2 + (Math.floor(T * 20) % 7) * 0.13;
        var r0 = Math.max(W, H) * (0.42 + ((i * 37) % 10) / 40), r1 = r0 + 60 + ((i * 53) % 40);
        ctx.beginPath(); ctx.moveTo(cx + Math.cos(a) * r0, hy + Math.sin(a) * r0 * 0.7); ctx.lineTo(cx + Math.cos(a) * r1, hy + Math.sin(a) * r1 * 0.7); ctx.stroke();
      }
    }

    /* ------------------------------------------------------------- loop */
    function frame(now) {
      if (dead) return;
      raf = requestAnimationFrame(frame);
      var dt = last ? Math.min(0.05, (now - last) / 1000) : 0;
      last = now;
      if (paused) return;
      update(dt);
      draw();
    }
    function onVis() { if (document.hidden && !paused && cfg.onAutoPause) cfg.onAutoPause(); }
    document.addEventListener("visibilitychange", onVis);

    layout();
    spawn();
    draw();
    raf = requestAnimationFrame(frame);

    /* -------------------------------------------------------------- API */
    function steer(d) {
      if (!started || finished || held) return;
      var g = gates[gi];
      if (g && g.go && dist < g.s) return;      // locked in on an answer
      cat.lane = clamp(cat.lane + d, 0, 2);
      if (cfg.sound) cfg.sound("swish");
    }
    function jump() {
      if (!started || finished || held || cat.y > 0.02) return;
      cat.vy = JUMP_V; cat.y = 0.001; cat.squash = calm ? 0 : -0.12;
      if (cfg.sound) cfg.sound("jump");
    }
    return {
      start: function () { started = true; last = 0; },
      steer: steer,
      jump: jump,
      /* Lock in an answer: the cat moves into the lane and sprints to the gate. */
      commit: function (lane) {
        var g = gates[gi];
        if (!g || !g.read || g.passed || g.go || held) return false;
        g.go = true;
        cat.lane = lane;
        dash = true;
        return true;
      },
      /* With the clock off, run on through the lane the cat is in. */
      go: function () {
        var g = gates[gi];
        if (!g || !g.read || g.passed || g.go || held) return false;
        g.go = true; dash = true;
        return true;
      },
      hold: function () { held = true; },
      resume: function () { held = false; },
      pause: function (on) { paused = !!on; last = 0; if (!paused) draw(); },
      paused: function () { return paused; },
      lane: function () { return cat.lane; },
      /* How far the cat is through reading question i: 0 at the start, 1 at its gate. */
      progress: function (i) {
        var g = gates[i];
        if (!g) return 1;
        var end = cfg.timer ? g.s : g.s - WAIT_BACK;
        return clamp((dist - g.readS) / Math.max(1, end - g.readS), 0, 1);
      },
      secondsLeft: function (i) {
        var g = gates[i];
        if (!g || !cfg.timer) return 0;
        return Math.max(0, (g.s - dist) / Math.max(1, speedNow()));
      },
      waiting: function () { return waiting; },
      /* Where on the canvas a gate's lane is, for diamonds to fly from. */
      point: function (lane) { return { x: PX(laneX(lane), Z_CAT + 0.4), y: PY(1.1, Z_CAT + 0.4) }; },
      state: function () {
        return { dist: dist, v: v, lane: cat.lane, x: cat.x, y: cat.y, gi: gi, waiting: waiting, held: held, paused: paused,
                 finished: finished, gates: gates, objs: objs, finishS: finishS, started: started };
      },
      /* For the browser tests: move the cat along instantly. */
      skipTo: function (pos) { dist = pos; },
      destroy: function () {
        dead = true;
        cancelAnimationFrame(raf);
        if (ro) ro.disconnect(); else window.removeEventListener("resize", layout);
        document.removeEventListener("visibilitychange", onVis);
      }
    };
  }

  window.MskCityRun = { world: world, LANES: 3 };
})();
