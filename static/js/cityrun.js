/* City Run: the tracks, the robot cat and everything on them.

   A white robot cat races along the tracks of a neon cyber city at night:
   Neon Station, Ramen Row, Arcade Alley and the Hyper Tunnel at the end.
   The city is a small world projected onto a canvas: x across the tracks,
   y up and s along them. Three tracks run up the middle, a fourth on the
   left carries passing trains, and platforms, shops and neon signs line
   both sides.

   This file knows nothing about questions. stretch.js hands it a plan, the
   answer gates and what each lane's banner says, and hears back when the
   cat reaches a gate, picks up a diamond or bumps into something. Which
   lane is right is decided there, never here.

   window.MskCityRun.world(canvas, cfg) starts a run; see the API at the
   end of world(). */
(function () {
  "use strict";

  /* ------------------------------------------------------- the tracks */
  var LANE = 1.25;           // from one track's middle to the next
  var ROAD = 1.95;           // half the width of the three tracks
  var SIDE = 3.5;            // the side track for passing trains, on the left
  var TRAIN_X = -(ROAD + SIDE) / 2;
  var WALK_L = 5.1, WALK_R = 3.75;   // where the buildings start, left and right
  var Z_CAT = 3.4;           // how far in front of the camera the cat runs
  var Z_NEAR = 0.6, Z_FAR = 118, Z_FADE = 80;
  var GRAV = 26, JUMP_V = 7.9;
  var SPEEDS = [13.5, 14.5, 15.5, 16.5], CALM_SPEED = 11, DASH = 2.5;
  var INTRO = 64;            // the stretch of track before the first question
  var GAP = 62;              // the track between one gate and the next question
  var FINISH = 52;           // from the last gate to the finish line
  var WAIT_BACK = 5.5;       // with the clock off, the cat waits this far short of a gate

  /* One palette per district: all night, each with its own neon. */
  var DIST = [
    { name: "Neon Station", sky: ["#060D2E", "#163679", "#4A8DC8"], haze: "rgba(125,211,252,.30)",
      neon: ["#22D3EE", "#F472B6", "#A78BFA", "#FB923C", "#FDE047"],
      signs: ["NEO CITY", "PLATFORM 1", "TRAINS", "CYBERNETICS", "DATA", "TICKETS", "METRO"],
      bed: "#161C3B", sleeper: "#2B345C", rail: "#B4C6DC", plat: "#283057", plat2: "#1F2549",
      far: ["#1A2A5E", "#22356F", "#14204C"], farWin: ["#7DD3FC", "#FDE68A", "#C4B5FD"],
      build: [["#1C2554", "#131A3F"], ["#242B60", "#191F48"], ["#172850", "#0F1C3C"], ["#2B2358", "#1E1942"]],
      win: ["#FCD34D", "#7DD3FC", "#FDBA74", "#C4B5FD"], lit: 0.48 },
    { name: "Ramen Row", sky: ["#0F0A2E", "#43217A", "#D2577F"], haze: "rgba(251,146,60,.26)",
      neon: ["#FB923C", "#F472B6", "#FDE047", "#22D3EE", "#F87171"],
      signs: ["RAMEN", "NOODLES", "SUSHI", "BYTE BAR", "404 CAFE", "TEA", "DUMPLINGS"],
      bed: "#1B1838", sleeper: "#302B55", rail: "#CBBEDD", plat: "#2E2853", plat2: "#241E47",
      far: ["#2A2160", "#34286F", "#211A52"], farWin: ["#FDBA74", "#F9A8D4", "#FDE68A"],
      build: [["#2C2056", "#1F1740"], ["#36214F", "#25163B"], ["#23244F", "#191A3D"], ["#3B2249", "#291836"]],
      win: ["#FDBA74", "#FCD34D", "#F9A8D4", "#7DD3FC"], lit: 0.55 },
    { name: "Arcade Alley", sky: ["#0A0624", "#491A8A", "#E06BD6"], haze: "rgba(232,121,249,.26)",
      neon: ["#E879F9", "#22D3EE", "#A3E635", "#F472B6", "#FDE047"],
      signs: ["ARCADE", "GAMES", "PIXEL", "HIGH SCORE", "PLAYER 1", "LEVEL UP", "BONUS"],
      bed: "#1A1534", sleeper: "#2F2852", rail: "#D3C2E6", plat: "#2D2452", plat2: "#221B45",
      far: ["#2C1A5E", "#381F70", "#21154C"], farWin: ["#F0ABFC", "#67E8F9", "#BEF264"],
      build: [["#2A1A55", "#1D1240"], ["#33195A", "#231044"], ["#1F1F55", "#151542"], ["#3D1A4E", "#2A1238"]],
      win: ["#F0ABFC", "#67E8F9", "#FDE68A", "#BEF264"], lit: 0.58 },
    { name: "Hyper Tunnel", sky: ["#03061A", "#122059", "#0E8FB0"], haze: "rgba(34,211,238,.32)",
      neon: ["#22D3EE", "#818CF8", "#F472B6", "#5EEAD4", "#FDE047"],
      signs: ["CYBERNETICS", "ROBOTICS", "CODE", "LOGIC", "CLOUD", "BINARY", "NEO CITY"],
      bed: "#121A33", sleeper: "#26324F", rail: "#B8D6E6", plat: "#1F2B4C", plat2: "#182340",
      far: ["#122656", "#1A3068", "#0D1C45"], farWin: ["#67E8F9", "#A5B4FC", "#5EEAD4"],
      build: [["#13234D", "#0C183A"], ["#1A2558", "#111A44"], ["#102B4D", "#0A1E3A"], ["#1F2050", "#15163D"]],
      win: ["#67E8F9", "#A5B4FC", "#FDE68A", "#5EEAD4"], lit: 0.6 }
  ];
  var GEMC = ["#E0F2FE", "#7DD3FC", "#38BDF8", "#0284C7", "#075985"];
  var FONT = "Poppins, Inter, sans-serif";

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
  function rgba(c, a) { var x = hex(c); return "rgba(" + x[0] + "," + x[1] + "," + x[2] + "," + a + ")"; }
  function clamp(v, a, b) { return v < a ? a : v > b ? b : v; }
  function ease(t) { return t < 0.5 ? 2 * t * t : 1 - Math.pow(-2 * t + 2, 2) / 2; }

  function world(canvas, cfg) {
    var ctx = canvas.getContext("2d");
    var calm = !!cfg.calm;
    var rnd = rng(cfg.seed || (Date.now() & 0x7fffffff));
    var W = 0, H = 0, dpr = 1, F = 300, hy = 100, cx = 0, camH = 1.9, camX = 0;
    var T = 0, last = 0, raf = 0, dead = false, paused = false;
    var dist = 0, v = 0, started = false, held = false, finished = false, finishFired = false;
    var cat = { lane: 1, x: 0, y: 0, vy: 0, phase: 0, lean: 0, squash: 0, hurt: 0, safe: 0, cheer: 0, dust: 0 };
    var objs = [];           // things on the tracks: obstacles, diamonds, gates, drones, trains
    var scen = [];           // buildings, signs, platform props and tunnel frames
    var parts = [];          // particles, in screen space
    var nextB = [0, 0], nextP = [4, 8], nextTrain = 150;
    var dash = false, gi = 0, waiting = false, shake = 0, skyK = 0, skyT = 0;
    var sky = null, skyFor = "";

    /* ---------------------------------------------------------- the plan
       Every gate's place on the track, worked out up front from how long
       its question takes to read. The track between gates is filled as the
       cat gets near it. */
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
    // Into Ramen Row the tracks cross a canal on a viaduct.
    var bridges = [];
    if (gates[4] && gates[5]) bridges.push({ s0: gates[4].s + 10, s1: gates[5].readS - 4 });
    function districtAt(pos) { var k = 0; for (var j = 1; j < 4; j++) if (pos >= districtS[j]) k = j; return k; }
    function onBridge(pos) { for (var j = 0; j < bridges.length; j++) if (pos >= bridges[j].s0 && pos <= bridges[j].s1) return bridges[j]; return null; }
    var sections = [];       // [from, to, district] stretches to fill with obstacles and diamonds
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
      skyFor = "";
      if (!started || paused) draw();
    }
    var ro = null;
    if (window.ResizeObserver) { ro = new ResizeObserver(function () { layout(); }); ro.observe(canvas); }
    else window.addEventListener("resize", layout);

    /* ------------------------------------------------------- projection */
    function zOf(pos) { return pos - dist + Z_CAT; }
    function PX(x, z) { return cx + (x - camX) * F / z; }
    function PY(y, z) { return hy + (camH - y) * F / z; }
    function laneX(l) { return (l - 1) * LANE; }

    /* ------------------------------------------------------ the city ahead */
    function spawn() {
      var ahead = dist + Z_FAR + 4;
      // buildings, both sides, each with neon and often a sign
      for (var side = 0; side < 2; side++) {
        while (nextB[side] < ahead) {
          var br = onBridge(nextB[side]) || onBridge(nextB[side] + 3);
          if (br) { nextB[side] = br.s1 + 0.5; continue; }
          var k = districtAt(nextB[side]), P = DIST[k], sd = side ? 1 : -1;
          var len = 3.3 + rnd() * 4.4;
          var tall = rnd() < (k === 3 ? 0.6 : 0.35);
          var h = tall ? 7 + rnd() * 9 : 3.4 + rnd() * 3.6;
          var floors = Math.max(2, Math.round(h / (tall ? 0.95 : 1.1)));
          var cols = Math.max(2, Math.round(len / (tall ? 0.7 : 0.95)));
          var lit = [];
          for (var q = 0; q < floors * cols; q++) lit.push(rnd() < P.lit ? P.win[Math.floor(rnd() * P.win.length)] : null);
          var strips = [];
          for (var f = 1; f < floors; f++) if (rnd() < 0.22) strips.push([f, P.neon[Math.floor(rnd() * P.neon.length)]]);
          var b = { t: "build", side: sd, s0: nextB[side], s1: nextB[side] + len, h: h, k: k,
                    col: P.build[Math.floor(rnd() * P.build.length)], floors: floors, cols: cols, tall: tall,
                    shop: rnd() < (k === 1 ? 0.75 : 0.5), awn: P.neon[Math.floor(rnd() * P.neon.length)], lit: lit, strips: strips };
          scen.push(b);
          if (rnd() < 0.68) {
            var vert = rnd() < 0.42, word = P.signs[Math.floor(rnd() * P.signs.length)];
            if (vert && word.length > 7) word = P.signs[0].length <= 7 ? P.signs[0] : "NEON";
            scen.push({ t: "sign", side: sd, s0: b.s0 + 0.5 + rnd() * Math.max(0.2, len - 1.4), vert: vert, text: word,
                        w: vert ? 0.46 : Math.min(1.5, 0.5 + word.length * 0.11), h: vert ? 0.42 + word.length * 0.2 : 0.46,
                        y0: vert ? 1.9 + rnd() * 0.6 : 2.0 + rnd() * Math.min(1.6, h - 2.8), col: P.neon[Math.floor(rnd() * P.neon.length)], k: k,
                        ph: rnd() * 6 });
          }
          nextB[side] += len + (rnd() < 0.08 ? 1.8 : 0);
        }
      }
      // things on the platforms
      for (side = 0; side < 2; side++) {
        while (nextP[side] < ahead) {
          var pos = nextP[side], sdp = side ? 1 : -1;
          if (onBridge(pos)) { scen.push({ t: "rail", side: sdp, s0: pos }); nextP[side] += 6; continue; }
          var kk = districtAt(pos), roll = rnd();
          var kind = roll < 0.34 ? "lamp" : roll < 0.52 ? "vend" : roll < 0.68 ? "hoload" : roll < 0.8 ? "bench" : roll < 0.9 ? "bin" : "kiosk";
          if (kind === "kiosk" && (kk !== 1 || !side)) kind = "lamp";
          scen.push({ t: kind, side: sdp, s0: pos, k: kk, ph: rnd() * 6, col: DIST[kk].neon[Math.floor(rnd() * DIST[kk].neon.length)] });
          nextP[side] += 6.5 + rnd() * 5;
        }
      }
      // the canal under the viaduct
      bridges.forEach(function (b) {
        if (!b.made && b.s0 < ahead) { b.made = true; scen.push({ t: "water", s0: b.s0, s1: b.s1 }); }
      });
      // a train waiting at Neon Station, and later ones racing past on the side track
      if (!trainMade) {
        trainMade = true;
        objs.push({ t: "train", s: -6, len: 58, cars: 6, v: 0 });
      }
      if (!calm && started && dist > nextTrain && districtAt(dist + 60) > 0 && dist < finishS - 160) {
        nextTrain = dist + 170 + rnd() * 90;
        objs.push({ t: "train", s: dist + Z_FAR + 30, len: 38, cars: 4, v: -24, horn: false });
      }
      // obstacles and diamonds, a section at a time
      while (sections.length && sections[0][0] < ahead + 40) fill(sections.shift());
      // each gate, when it comes into range
      gates.forEach(function (g) {
        if (!g.made && g.s < ahead + 20) { g.made = true; makeGate(g); }
      });
      // the frames of the Hyper Tunnel, then the tunnel itself
      if (districtS[3] < 1e8) {
        while (nextFrame < ahead && nextFrame < finishS - 4) {
          if (nextFrame < districtS[3] + 20) { nextFrame = districtS[3] + 20; continue; }
          scen.push({ t: "frame", s0: nextFrame, col: (Math.floor(nextFrame / 12) % 2) ? "#22D3EE" : "#E879F9" });
          nextFrame += 12;
        }
      }
      if (!finishMade && finishS < ahead + 40) { finishMade = true; objs.push({ t: "tunnel", s: finishS - 1 }); objs.push({ t: "finish", s: finishS }); }
      if (!startMade) { startMade = true; objs.push({ t: "startarch", s: 7 }); }
    }
    var finishMade = false, startMade = false, trainMade = false, nextFrame = 0;

    /* The obstacles between two questions. Every row leaves at least one
       track open, and a stopped metro car blocks its track for its length. */
    function fill(sec) {
      var from = sec[0], to = sec[1], k = sec[2];
      var busy = [-1e9, -1e9, -1e9];
      var pos = from + 4;
      while (pos < to - 4) {
        var free = [0, 1, 2].filter(function (l) { return busy[l] < pos - 1.5; });
        if (free.length < 2) { pos += 3; continue; }
        var hard = !calm && k >= 1 && rnd() < 0.18 + k * 0.08;
        var roll = rnd();
        var lanes = shuffleArr(free.slice());
        var a = lanes[0], b = lanes[1];
        if (roll < 0.2) {
          objs.push({ t: "metro", lane: a, s: pos, len: 6, n: Math.floor(rnd() * 9) + 1 }); busy[a] = pos + 6.4;
          if (hard && lanes.length > 2) objs.push({ t: "cone", lane: b, s: pos + 1 });
          gemLine(lanes[lanes.length - 1], pos - 1, 4);
        } else if (roll < 0.35) {
          objs.push({ t: "holo", lane: a, s: pos }); busy[a] = pos + 1;
          gemLine(b, pos - 2, 4);
          if (hard && lanes.length > 2) objs.push({ t: "barrier", lane: lanes[2], s: pos + 0.5 });
        } else if (roll < 0.5) {
          objs.push({ t: "cone", lane: a, s: pos });
          if (hard) objs.push({ t: "cone", lane: b, s: pos });
          gemArc(a, pos);
        } else if (roll < 0.64) {
          objs.push({ t: "barrier", lane: a, s: pos });
          gemArc(a, pos);
          if (hard) { objs.push({ t: "holo", lane: b, s: pos + 2 }); busy[b] = pos + 3; }
        } else if (roll < 0.77) {
          objs.push({ t: "crate", lane: a, s: pos });
          if (hard && rnd() < 0.5) objs.push({ t: "crate", lane: b, s: pos + 0.4 });
          gemArc(a, pos);
        } else if (roll < 0.87) {
          objs.push({ t: "puddle", lane: a, s: pos });
          gemLine(b, pos - 2, 5);
        } else {
          objs.push({ t: "drones", lane: a, s: pos, bots: [0, 1].map(function () { return { dx: (rnd() - 0.5) * 0.6, ds: (rnd() - 0.5) * 1.4, ph: rnd() * 6, fly: 0, vx: 0, vy: 0, vz: 0 }; }) });
          gemLine(a, pos + 2, 5);
        }
        pos += (calm ? 17 : 13) + rnd() * 5 - k;
      }
    }
    function shuffleArr(a) {
      for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(rnd() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t; }
      return a;
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
    /* A gate: a neon arch over each answer track, a scanner line just before
       it, and the middle track closed when there are only two answers.
       While a question is being read, a diamond on every open track now and
       then, so no track is a better place to wait than another. */
    function makeGate(g) {
      objs.push({ t: "scan", s: g.s - 3.6 });
      objs.push({ t: "pylon", side: -1, s: g.s - 3.6 });
      objs.push({ t: "pylon", side: 1, s: g.s - 3.6 });
      objs.push({ t: "gate", s: g.s, g: g });
      if (!g.lanes[1]) objs.push({ t: "works", lane: 1, s: g.s - 0.6, g: g });
      for (var p = g.readS + 14; p < g.s - 12; p += 15) {
        for (var l = 0; l < 3; l++) if (g.lanes[l] || l !== 1) objs.push({ t: "gem", lane: l, s: p, y: 0.42 });
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
      // little puffs of dust from the cat's feet
      if (!calm && v > 4 && cat.y <= 0.02) {
        cat.dust -= dt;
        if (cat.dust <= 0) {
          cat.dust = 0.11;
          var k0 = F / Z_CAT;
          parts.push({ kind: "dust", x: PX(cat.x, Z_CAT) + (rnd() - 0.5) * 0.3 * k0, y: PY(0, Z_CAT) - 2, vx: (rnd() - 0.5) * 30, vy: -12 - rnd() * 12,
                       g: 0, a: 0, life: 0.55, max: 0.55, r: 0.06 * k0 });
        }
      }

      // trains on the side track
      objs.forEach(function (o) {
        if (o.t !== "train" || !o.v) return;
        o.s += o.v * dt;
        if (!o.horn && zOf(o.s) < Z_CAT + 30) { o.horn = true; if (cfg.sound) cfg.sound("whoosh"); }
      });

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
        burst(PX(laneX(cat.lane), Z_CAT + 1), PY(1.4, Z_CAT + 1), calm ? 0 : 40, "confetti");
        if (cfg.onFinish) cfg.onFinish();
      }
      // the sky turns with the district the cat is in
      var want = districtAt(dist);
      if (want !== skyK) { skyT += dt / 3.2; if (skyT >= 1) { skyK = want; skyT = 0; skyFor = ""; } }

      // tidy up what is behind the camera
      objs = objs.filter(function (o) {
        return zOf(o.s + (o.len || 0)) > Z_NEAR - 0.4 || (o.t === "drones" && o.bots.some(function (b) { return b.fly > 0 && b.fly < 2.5; }));
      });
      scen = scen.filter(function (o) { return zOf(o.s1 || o.s0) > Z_NEAR - 1; });
      parts = parts.filter(function (p) { p.life -= dt; return p.life > 0; });
      parts.forEach(function (p) { p.vy += (p.g || 0) * dt; p.x += p.vx * dt; p.y += p.vy * dt; p.a += (p.va || 0) * dt; if (p.kind === "dust") p.r += dt * 18; });
    }

    var SOLID = { cone: [0.36, 0.55], barrier: [0.56, 0.62], crate: [0.42, 0.72], puddle: [0.5, 0],
                  holo: [0.55, 3], metro: [0.62, 3], works: [0.6, 0.7] };
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
        if (o.t === "drones") {
          if (o.s - cs < 6) o.bots.forEach(function (b) {
            if (!b.fly) { b.fly = 0.01; b.vx = (b.dx < 0 ? -1 : 1) * (1.5 + rnd() * 2); b.vy = 3 + rnd() * 2; b.vz = 2 + rnd() * 3; }
          });
          continue;
        }
        var solid = SOLID[o.t];
        if (!solid || cat.safe > 0 || held) continue;
        var len = o.len || (o.t === "puddle" ? 1.2 : o.t === "crate" ? 0.72 : 0.4);
        if (cs < o.s - 0.35 || cs > o.s + len + 0.2) continue;
        if (Math.abs(lx - cat.x) > solid[0] + 0.22) continue;
        if (o.t === "works") continue;    // the gate decides what happens on the closed track
        if (cat.y > solid[1]) continue;
        o.done = true;
        if (o.t === "puddle") {
          var zp = zOf(o.s);
          burst(PX(lx, Math.max(zp, 1.2)), PY(0.1, Math.max(zp, 1.2)), calm ? 0 : 16, "splash");
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
      if (!g.lanes[lane]) {                 // ran into the closed track
        hurt("works");
        return;
      }
      if (g.res.ok) {
        burst(gx, gy, calm ? 0 : 26, "pixel", g.lanes[lane].c);
        burst(gx, gy, calm ? 0 : 14, "gem");
        cat.cheer = 0.8;
        if (!calm && cat.y <= 0) cat.vy = 4.2;
      } else {
        burst(gx, gy, calm ? 0 : 18, "pixel", g.lanes[lane].c);
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
        if (kind === "spark") { p.c = rnd() < 0.5 ? "#67E8F9" : "#F0ABFC"; p.r = 2 + rnd() * 2.5; p.life = 0.5; }
        if (kind === "splash") { p.c = rnd() < 0.5 ? "#F0ABFC" : "#67E8F9"; p.vy = -180 - rnd() * 260; p.vx *= 0.6; p.g = 1100; p.life = 0.7; p.r = 2.5 + rnd() * 3; }
        if (kind === "gem") { p.vy = -280 - rnd() * 300; p.vx *= 0.7; p.g = 820; p.r = 8 + rnd() * 5; p.life = 1.1; }
        if (kind === "pixel") { p.r = 3 + rnd() * 5; p.va = 0; }
        if (kind === "confetti") { p.c = ["#22D3EE", "#F472B6", "#FDE047", "#A78BFA", "#4ADE80", "#FFFFFF"][i % 6]; p.vy = -380 - rnd() * 380; p.vx *= 1.4; p.g = 520; p.life = 2.2; }
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
      drawGround();
      var list = [];
      scen.forEach(function (o) { if (o.t === "water") return; var z = zOf(o.s1 !== undefined ? o.s1 : o.s0); list.push([Math.min(z, Z_FAR), o, 1]); });
      objs.forEach(function (o) {
        if (o.t === "scan" || o.t === "puddle") return;
        list.push([zOf(o.s), o, 0]);
      });
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

    /* ------------------------------------------------------------- sky
       A night sky with a glow over the city, a skyline of towers with lit
       windows, hover cars, and the Hyper Tunnel waiting at the far end. */
    function drawSky(P, Q, t) {
      var g = ctx.createLinearGradient(0, 0, 0, hy + 2);
      g.addColorStop(0, mix(P.sky[0], Q.sky[0], t));
      g.addColorStop(0.6, mix(P.sky[1], Q.sky[1], t));
      g.addColorStop(1, mix(P.sky[2], Q.sky[2], t));
      ctx.fillStyle = g;
      ctx.fillRect(-20, -20, W + 40, hy + 22);
      // a few far lights twinkle in the sky
      ctx.fillStyle = "#E0F2FE";
      for (var i = 0; i < 22; i++) {
        var sx = (i * 97.3 + 13) % W, sy = (i * 41.7) % (hy * 0.55);
        ctx.globalAlpha = 0.25 + 0.4 * (calm ? 0.6 : 0.5 + 0.5 * Math.sin(T * 2 + i));
        ctx.fillRect(sx, sy, 1.5, 1.5);
      }
      ctx.globalAlpha = 1;
      // the skyline, drawn once for each district and size
      var key = skyK + ":" + Math.round(W) + "x" + Math.round(H);
      if (skyFor !== key) { sky = skyline(DIST[skyK]); skyFor = key; }
      var drift = -camX * 8;
      ctx.drawImage(sky, drift - W * 0.1, 0, W * 1.2, hy + 2);
      // hover cars crossing the sky
      for (var c = 0; c < 6; c++) {
        var dir = c % 2 ? -1 : 1, sp = 26 + c * 9;
        var span = W + 160, xx = ((c * 173 + (calm ? 0 : T * sp)) % span) - 80;
        if (dir < 0) xx = W - xx;
        hoverCar(xx, hy * (0.16 + (c * 0.13) % 0.62), Math.max(6, H * 0.018), dir, c);
      }
      // the Hyper Tunnel, far away, until the real one comes into view
      if (!finishMade || zOf(finishS) > Z_FAR) {
        var prog = clamp(dist / Math.max(1, finishS), 0, 1);
        portal(cx, hy, H * (0.07 + prog * 0.06));
      }
      // a haze of light over the far city
      var hz = ctx.createLinearGradient(0, hy - H * 0.12, 0, hy + 2);
      hz.addColorStop(0, "rgba(0,0,0,0)");
      hz.addColorStop(1, t < 0.5 ? P.haze : Q.haze);
      ctx.fillStyle = hz;
      ctx.fillRect(0, hy - H * 0.12, W, H * 0.12 + 2);
    }
    function skyline(P) {
      var c = document.createElement("canvas"), w = Math.max(1, Math.round(W * 1.2 * dpr)), h = Math.max(1, Math.round((hy + 2) * dpr));
      c.width = w; c.height = h;
      var x = c.getContext("2d"), r = rng(7 + skyK * 31);
      x.scale(dpr, dpr);
      var WW = W * 1.2, base = hy + 2;
      [0, 1, 2].forEach(function (layer) {
        var px = -10;
        while (px < WW + 10) {
          var bw = H * (0.04 + r() * 0.07), bh = H * (layer === 0 ? 0.12 + r() * 0.2 : layer === 1 ? 0.06 + r() * 0.16 : 0.03 + r() * 0.08);
          var mid = Math.abs(px + bw / 2 - WW / 2) < W * 0.07;   // keep the middle clear for the tunnel
          if (mid && layer < 2) bh *= 0.35;
          x.fillStyle = P.far[layer];
          x.fillRect(px, base - bh, bw, bh);
          if (layer < 2 && r() < 0.35) {           // a spire with a red light
            x.fillRect(px + bw * 0.45, base - bh - H * 0.03, Math.max(1, bw * 0.08), H * 0.03);
            x.fillStyle = "#F87171"; x.fillRect(px + bw * 0.43, base - bh - H * 0.034, 2.4, 2.4);
          }
          // lit windows
          var cw = Math.max(2, bw / 6), chh = Math.max(2, H * 0.008);
          for (var wy = base - bh + chh * 2; wy < base - chh * 2; wy += chh * 2.6) {
            for (var wx = px + cw * 0.6; wx < px + bw - cw; wx += cw * 1.6) {
              if (r() < (layer === 0 ? 0.32 : 0.22)) {
                x.fillStyle = P.farWin[Math.floor(r() * P.farWin.length)];
                x.globalAlpha = layer === 0 ? 0.75 : 0.5;
                x.fillRect(wx, wy, cw * 0.7, chh);
                x.globalAlpha = 1;
              }
            }
          }
          // a neon band round the top now and then
          if (layer === 0 && r() < 0.3) { x.fillStyle = P.neon[Math.floor(r() * 4)]; x.fillRect(px, base - bh, bw, Math.max(1.5, H * 0.004)); }
          px += bw + (layer === 2 ? 0 : r() * H * 0.02);
        }
      });
      return c;
    }
    function hoverCar(x, y, s, dir, n) {
      ctx.save(); ctx.translate(x, y); ctx.scale(dir, 1);
      ctx.fillStyle = "rgba(34,211,238,.25)";
      ctx.beginPath(); ctx.ellipse(0, s * 0.45, s * 1.6, s * 0.35, 0, 0, 6.3); ctx.fill();
      ctx.fillStyle = n % 3 ? "#1E293B" : "#312E81";
      ctx.beginPath(); ctx.ellipse(0, 0, s * 1.5, s * 0.5, 0, 0, 6.3); ctx.fill();
      ctx.fillStyle = "#93C5FD"; ctx.beginPath(); ctx.ellipse(s * 0.25, -s * 0.28, s * 0.6, s * 0.3, 0, Math.PI, 0); ctx.fill();
      ctx.fillStyle = "#67E8F9"; ctx.fillRect(-s * 1.2, s * 0.3, s * 2.4, Math.max(1, s * 0.12));
      ctx.fillStyle = "#FEF9C3"; ctx.beginPath(); ctx.arc(s * 1.45, 0, s * 0.18, 0, 6.3); ctx.fill();
      ctx.fillStyle = "#F87171"; ctx.beginPath(); ctx.arc(-s * 1.45, 0, s * 0.15, 0, 6.3); ctx.fill();
      ctx.restore();
    }
    /* The glowing mouth of a tunnel: rings of neon round a bright inside. */
    function portal(x, base, r) {
      var cy = base - r * 0.55;
      var g = ctx.createRadialGradient(x, cy, 0, x, cy, r);
      g.addColorStop(0, "rgba(224,250,255,.95)"); g.addColorStop(0.35, "rgba(103,232,249,.75)"); g.addColorStop(1, "rgba(30,64,175,.2)");
      ctx.fillStyle = g;
      ctx.beginPath(); ctx.arc(x, cy, r, Math.PI, 0); ctx.lineTo(x + r, base); ctx.lineTo(x - r, base); ctx.closePath(); ctx.fill();
      [[1.18, "#E879F9", 0.16], [1.0, "#22D3EE", 0.1], [0.78, "#A78BFA", 0.06]].forEach(function (q) {
        ctx.beginPath(); ctx.arc(x, cy, r * q[0], Math.PI, 0); ctx.lineTo(x + r * q[0], base); ctx.moveTo(x - r * q[0], cy); ctx.lineTo(x - r * q[0], base);
        ctx.strokeStyle = rgba(q[1], 0.35); ctx.lineWidth = r * q[2] * 2.4; ctx.stroke();
        ctx.strokeStyle = q[1]; ctx.lineWidth = r * q[2]; ctx.stroke();
      });
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
    function track(xc, near, P) {
      // sleepers close by, then the two rails all the way
      ctx.fillStyle = P.sleeper;
      var first = Math.floor(near / 0.9) * 0.9;
      for (var p = first; p < dist + 46; p += 0.9) groundQuad(xc - 0.52, xc + 0.52, p, p + 0.2);
      ctx.fillStyle = P.rail;
      groundQuad(xc - 0.4, xc - 0.34, near, dist + Z_FAR);
      groundQuad(xc + 0.34, xc + 0.4, near, dist + Z_FAR);
    }
    function drawGround() {
      var P = DIST[districtAt(dist + 30)];
      var near = dist - Z_CAT + Z_NEAR, far = dist + Z_FAR;
      ctx.fillStyle = P.plat2;
      ctx.fillRect(-20, hy, W + 40, H - hy + 20);
      // platforms and track beds
      ctx.fillStyle = P.plat;
      groundQuad(ROAD + 0.12, WALK_R, near, far);
      groundQuad(-WALK_L, -SIDE - 0.12, near, far);
      ctx.fillStyle = P.bed;
      groundQuad(-ROAD - 0.12, ROAD + 0.12, near, far);
      groundQuad(-SIDE - 0.12, -ROAD - 0.12, near, far);
      // the canal under the viaduct, with the city's lights in it, where the platforms stop
      scen.forEach(function (o) {
        if (o.t !== "water") return;
        ctx.fillStyle = "#0B1340";
        groundQuad(-60, -ROAD - 0.3, o.s0, o.s1); groundQuad(ROAD + 0.3, 60, o.s0, o.s1);
        for (var p = Math.ceil(dist / 2.5) * 2.5; p < o.s1; p += 2.5) {
          if (p < o.s0) continue;
          var off = ((p * 7.3) % 9) + 2.6, c = ["#F472B6", "#22D3EE", "#FDE047"][Math.floor(p) % 3];
          ctx.fillStyle = rgba(c, 0.45);
          groundQuad(-off - 0.5, -off, p, p + 0.3); groundQuad(off, off + 0.5, p + 1.2, p + 1.5);
        }
      });
      // tiles on the platforms
      ctx.fillStyle = "rgba(255,255,255,.05)";
      var tfirst = Math.floor(near / 2) * 2;
      for (var q = tfirst; q < dist + 60; q += 2) { groundQuad(ROAD + 0.2, WALK_R, q, q + 0.06); groundQuad(-WALK_L, -SIDE - 0.2, q, q + 0.06); }
      // the three tracks, and the side track for trains
      for (var l = 0; l < 3; l++) track(laneX(l), near, P);
      track(TRAIN_X, near, P);
      // yellow safety lines, and light strips that race along beside the tracks
      ctx.fillStyle = "#FACC15";
      groundQuad(ROAD + 0.14, ROAD + 0.22, near, far); groundQuad(-SIDE - 0.22, -SIDE - 0.14, near, far);
      var flow = dist % 3;
      [[-ROAD - 0.04, "#22D3EE", 0.08, 0.22], [ROAD - 0.04, "#22D3EE", 0.08, 0.22], [-LANE / 2 - 0.025, "#E879F9", 0.05, 0.1], [LANE / 2 - 0.025, "#E879F9", 0.05, 0.1]].forEach(function (st) {
        ctx.fillStyle = rgba(st[1], st[3]);
        groundQuad(st[0] - st[2], st[0] + st[2] * 2, near, far);
        ctx.fillStyle = rgba(st[1], 0.85);
        for (var p2 = Math.floor(near / 3) * 3 - flow; p2 < far; p2 += 3) groundQuad(st[0], st[0] + st[2], p2, p2 + 1.8);
      });
      // scanners before the gates, and puddles of neon light
      objs.forEach(function (o) {
        var z = zOf(o.s);
        if (z < Z_NEAR || z > Z_FAR) return;
        if (o.t === "scan") {
          var pulse = calm ? 1 : 0.6 + 0.4 * Math.sin(T * 6);
          ctx.fillStyle = rgba("#22D3EE", 0.25 * pulse);
          groundQuad(-ROAD, ROAD, o.s - 0.5, o.s + 0.7);
          ctx.fillStyle = "rgba(165,243,252,.9)";
          groundQuad(-ROAD, ROAD, o.s, o.s + 0.14);
        } else if (o.t === "puddle" && !o.done) {
          var lx = laneX(o.lane), k = F / z, sy = Math.max(1, 0.3 * k * (camH / (z + 0.6)));
          ctx.globalAlpha = fade(z);
          ctx.fillStyle = "#170F3A";
          ctx.beginPath(); ctx.ellipse(PX(lx, z), PY(0, z + 0.6), 0.56 * k, sy, 0, 0, 6.3); ctx.fill();
          ctx.fillStyle = "rgba(244,114,182,.6)";
          ctx.beginPath(); ctx.ellipse(PX(lx - 0.18, z), PY(0, z + 0.6), 0.22 * k, sy * 0.3, 0, 0, 6.3); ctx.fill();
          ctx.fillStyle = "rgba(34,211,238,.6)";
          ctx.beginPath(); ctx.ellipse(PX(lx + 0.2, z), PY(0, z + 0.65), 0.16 * k, sy * 0.25, 0, 0, 6.3); ctx.fill();
          ctx.globalAlpha = 1;
        }
      });
    }
    function fade(z) { return z < Z_FADE ? 1 : clamp(1 - (z - Z_FADE) / (Z_FAR - Z_FADE), 0, 1); }

    /* ------------------------------------------- the buildings and signs */
    function drawScen(o) {
      if (o.t === "build") return building(o);
      if (o.t === "frame") return frame(o);
      var z = zOf(o.s0);
      if (z < Z_NEAR || z > Z_FAR) return;
      var k = F / z;
      ctx.globalAlpha = fade(z);
      if (o.t === "sign") sign(o, z, k);
      else if (o.t === "rail") railing(o);
      else {
        var x = o.side > 0 ? ROAD + 0.95 : -SIDE - 0.75;
        var X = PX(x, z), Y = PY(0, z);
        if (o.t === "lamp") lamp(X, Y, k, o);
        else if (o.t === "vend") vend(X, Y, k, o);
        else if (o.t === "hoload") holoAd(X, Y, k, o);
        else if (o.t === "bench") bench(X, Y, k);
        else if (o.t === "bin") bin(X, Y, k, o);
        else if (o.t === "kiosk") kiosk(X, Y, k, o);
      }
      ctx.globalAlpha = 1;
    }
    function building(b) {
      var z0 = Math.max(Z_NEAR, zOf(b.s0)), z1 = Math.min(Z_FAR, zOf(b.s1));
      if (z1 <= z0 + 0.01) return;
      var x = b.side * (b.side > 0 ? WALK_R : WALK_L);
      ctx.globalAlpha = fade(z0);
      // the end wall, where it faces the camera
      if (zOf(b.s0) >= Z_NEAR) {
        ctx.fillStyle = b.col[1];
        var xe = x + b.side * 8;
        quad(PX(x, z0), PY(0, z0), PX(x, z0), PY(b.h, z0), PX(xe, z0), PY(b.h, z0), PX(xe, z0), PY(0, z0));
      }
      ctx.fillStyle = b.col[0];
      quad(PX(x, z0), PY(0, z0), PX(x, z0), PY(b.h, z0), PX(x, z1), PY(b.h, z1), PX(x, z1), PY(0, z1));
      var len = b.s1 - b.s0, base = b.shop ? 1.3 : 0.5, fh = (b.h - base - 0.3) / b.floors;
      // the roofline glows
      ctx.fillStyle = rgba(b.awn, 0.8);
      quad(PX(x, z0), PY(b.h - 0.08, z0), PX(x, z0), PY(b.h, z0), PX(x, z1), PY(b.h, z1), PX(x, z1), PY(b.h - 0.08, z1));
      if (F / Math.max(zOf(b.s0), Z_NEAR) > 3) {
        // lit windows
        for (var c = 0; c < b.cols; c++) {
          var sa = b.s0 + (c + 0.2) * len / b.cols, sb = b.s0 + (c + 0.8) * len / b.cols;
          var za = zOf(sa), zb = zOf(sb);
          if (zb < Z_NEAR || za > Z_FAR) continue;
          za = Math.max(Z_NEAR, za);
          for (var f = 0; f < b.floors; f++) {
            var lit = b.lit[f * b.cols + c];
            var y0 = base + f * fh + fh * 0.22, y1 = y0 + fh * 0.5;
            if (y1 > b.h - 0.2) continue;
            ctx.fillStyle = lit || "#0D1230";
            quad(PX(x, za), PY(y0, za), PX(x, za), PY(y1, za), PX(x, zb), PY(y1, zb), PX(x, zb), PY(y0, zb));
          }
        }
        // neon strips along some floors
        b.strips.forEach(function (st) {
          var yy = base + st[0] * fh - fh * 0.08;
          ctx.fillStyle = st[1];
          quad(PX(x, z0), PY(yy, z0), PX(x, z0), PY(yy + 0.07, z0), PX(x, z1), PY(yy + 0.07, z1), PX(x, z1), PY(yy, z1));
        });
        if (b.shop) {
          // a lit shop front under an awning
          var g0 = Math.max(Z_NEAR, zOf(b.s0 + 0.35)), g1 = zOf(b.s1 - 0.35);
          if (g1 > g0) {
            ctx.fillStyle = "#FCD9A0";
            quad(PX(x, g0), PY(0.12, g0), PX(x, g0), PY(1.0, g0), PX(x, g1), PY(1.0, g1), PX(x, g1), PY(0.12, g1));
            ctx.fillStyle = "rgba(124,45,18,.35)";
            for (var st2 = 0.8; st2 < len - 0.6; st2 += 1.1) {
              var q0 = zOf(b.s0 + st2), q1 = zOf(b.s0 + st2 + 0.08);
              if (q1 < Z_NEAR) continue;
              q0 = Math.max(Z_NEAR, q0);
              quad(PX(x, q0), PY(0.12, q0), PX(x, q0), PY(1.0, q0), PX(x, q1), PY(1.0, q1), PX(x, q1), PY(0.12, q1));
            }
          }
          ctx.fillStyle = b.awn;
          quad(PX(x, z0), PY(1.08, z0), PX(x, z0), PY(1.3, z0), PX(x, z1), PY(1.3, z1), PX(x, z1), PY(1.08, z1));
        }
      }
      ctx.globalAlpha = 1;
    }
    /* A sign standing out from a wall, face on to the tracks. */
    function sign(o, z, k) {
      var x0 = o.side * ((o.side > 0 ? WALK_R : WALK_L) - 0.08), x1 = x0 - o.side * o.w;
      var X0 = Math.min(PX(x0, z), PX(x1, z)), X1 = Math.max(PX(x0, z), PX(x1, z));
      var Y1 = PY(o.y0, z), Y0 = PY(o.y0 + o.h, z), w = X1 - X0, h = Y1 - Y0;
      if (w < 2) return;
      var on = calm || Math.sin(T * 1.7 + o.ph) > -0.97;   // a rare flicker
      ctx.fillStyle = rgba(o.col, 0.22);
      ctx.fillRect(X0 - w * 0.08, Y0 - h * 0.08, w * 1.16, h * 1.16);
      ctx.fillStyle = "#0A0E2A";
      ctx.fillRect(X0, Y0, w, h);
      var lw = Math.max(1, 0.035 * k);
      ctx.strokeStyle = on ? o.col : rgba(o.col, 0.4); ctx.lineWidth = lw;
      ctx.strokeRect(X0 + lw, Y0 + lw, w - lw * 2, h - lw * 2);
      if (w < 9) return;
      ctx.fillStyle = on ? o.col : rgba(o.col, 0.45);
      ctx.textAlign = "center"; ctx.textBaseline = "middle";
      if (on && !calm && k > 16) { ctx.shadowColor = o.col; ctx.shadowBlur = Math.min(14, k * 0.12); }
      if (o.vert) {
        var n = o.text.length, fs = Math.min(w * 0.62, h / (n + 0.6));
        ctx.font = "800 " + Math.max(4, Math.round(fs)) + "px " + FONT;
        for (var i = 0; i < n; i++) ctx.fillText(o.text.charAt(i), X0 + w / 2, Y0 + h * (i + 0.8) / (n + 0.6));
      } else {
        var fs2 = h * 0.56;
        ctx.font = "800 " + Math.max(4, Math.round(fs2)) + "px " + FONT;
        var tw = ctx.measureText(o.text).width;
        if (tw > w * 0.86) { fs2 *= w * 0.86 / tw; ctx.font = "800 " + Math.max(4, Math.round(fs2)) + "px " + FONT; }
        ctx.fillText(o.text, X0 + w / 2, Y0 + h / 2 + 1);
      }
      ctx.shadowBlur = 0;
    }
    function rect(x, y, w, h, c) { ctx.fillStyle = c; ctx.fillRect(x, y, w, h); }
    function tri(x1, y1, x2, y2, x3, y3, c) { ctx.fillStyle = c; ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.lineTo(x3, y3); ctx.closePath(); ctx.fill(); }
    function glowDot(x, y, r, c, a) {
      if (r < 0.5) return;
      var g = ctx.createRadialGradient(x, y, 0, x, y, r);
      g.addColorStop(0, rgba(c, a)); g.addColorStop(1, rgba(c, 0));
      ctx.fillStyle = g; ctx.fillRect(x - r, y - r, r * 2, r * 2);
    }
    function lamp(X, Y, k, o) {
      var w = Math.max(1, 0.06 * k), side = o.side;
      rect(X - w / 2, Y - 2.4 * k, w, 2.4 * k, "#1E2440");
      rect(side > 0 ? X - 0.5 * k : X, Y - 2.42 * k, 0.5 * k, Math.max(1, 0.05 * k), "#1E2440");
      var lx = X - side * 0.48 * k, ly = Y - 2.32 * k;
      glowDot(lx, ly, 0.9 * k, "#A5F3FC", 0.5);
      rect(lx - 0.13 * k, ly - 0.04 * k, 0.26 * k, 0.08 * k, "#E0FBFF");
    }
    function vend(X, Y, k, o) {
      var w = 0.62 * k, h = 1.45 * k;
      glowDot(X, Y - h * 0.5, 1.1 * k, o.col, 0.22);
      rect(X - w / 2, Y - h, w, h, "#1F2547");
      rect(X - w * 0.42, Y - h * 0.94, w * 0.84, h * 0.62, rgba(o.col, 0.85));
      ctx.fillStyle = "rgba(255,255,255,.65)";
      for (var r = 0; r < 4; r++) for (var c = 0; c < 3; c++) ctx.fillRect(X - w * 0.34 + c * w * 0.26, Y - h * 0.88 + r * h * 0.14, w * 0.14, h * 0.08);
      rect(X - w * 0.3, Y - h * 0.24, w * 0.6, h * 0.1, "#0B1028");
    }
    function holoAd(X, Y, k, o) {
      var w = 0.95 * k, h = 1.15 * k, a0 = ctx.globalAlpha, flick = calm ? 0.8 : 0.65 + 0.2 * Math.sin(T * 9 + o.ph);
      rect(X - 0.03 * k, Y - 0.5 * k, 0.06 * k, 0.5 * k, "#334155");
      ctx.globalAlpha = a0 * flick;
      rect(X - w / 2, Y - 0.5 * k - h, w, h, rgba(o.col, 0.28));
      ctx.strokeStyle = o.col; ctx.lineWidth = Math.max(1, 0.03 * k);
      ctx.strokeRect(X - w / 2, Y - 0.5 * k - h, w, h);
      // a cat's head: the run's own advert
      var hx = X, hy2 = Y - 0.5 * k - h * 0.5, r = h * 0.24;
      ctx.fillStyle = o.col;
      ctx.beginPath(); ctx.arc(hx, hy2, r, 0, 6.3); ctx.fill();
      tri(hx - r, hy2 - r * 0.2, hx - r * 0.8, hy2 - r * 1.4, hx - r * 0.2, hy2 - r * 0.9, o.col);
      tri(hx + r, hy2 - r * 0.2, hx + r * 0.8, hy2 - r * 1.4, hx + r * 0.2, hy2 - r * 0.9, o.col);
      ctx.fillStyle = "#0A0E2A";
      ctx.beginPath(); ctx.arc(hx - r * 0.38, hy2, r * 0.2, 0, 6.3); ctx.arc(hx + r * 0.38, hy2, r * 0.2, 0, 6.3); ctx.fill();
      ctx.globalAlpha = a0;
    }
    function bench(X, Y, k) {
      var w = 0.8 * k;
      rect(X - w / 2, Y - 0.42 * k, w, 0.08 * k, "#3B4470");
      rect(X - w / 2, Y - 0.64 * k, w, 0.07 * k, "#3B4470");
      rect(X - w * 0.42, Y - 0.42 * k, 0.05 * k, 0.42 * k, "#151A33");
      rect(X + w * 0.37, Y - 0.42 * k, 0.05 * k, 0.42 * k, "#151A33");
    }
    function bin(X, Y, k, o) {
      var w = 0.34 * k, h = 0.62 * k;
      rect(X - w / 2, Y - h, w, h, "#283055");
      rect(X - w / 2, Y - h * 0.62, w, Math.max(1, 0.05 * k), o.col);
      rect(X - w * 0.6, Y - h - 0.05 * k, w * 1.2, 0.07 * k, "#3B4470");
    }
    function kiosk(X, Y, k, o) {
      var w = 1.1 * k, h = 1.1 * k;
      glowDot(X, Y - h * 0.6, 1.3 * k, "#FDBA74", 0.3);
      rect(X - w / 2, Y - h * 0.55, w, h * 0.55, "#7C2D12");
      rect(X - w / 2, Y - h * 0.62, w, h * 0.08, "#FCD34D");
      rect(X - w * 0.46, Y - h * 1.25, 0.05 * k, h * 0.7, "#451A03"); rect(X + w * 0.41, Y - h * 1.25, 0.05 * k, h * 0.7, "#451A03");
      ctx.fillStyle = "#DC2626";
      ctx.beginPath(); ctx.moveTo(X - w * 0.62, Y - h * 1.15); ctx.lineTo(X + w * 0.62, Y - h * 1.15); ctx.lineTo(X + w * 0.5, Y - h * 1.38); ctx.lineTo(X - w * 0.5, Y - h * 1.38); ctx.closePath(); ctx.fill();
      for (var i = 0; i < 3; i++) {                       // paper lanterns
        var lx = X - w * 0.36 + i * w * 0.36, ly = Y - h * 1.0 + (calm ? 0 : Math.sin(T * 2 + i + o.ph) * 0.02 * k);
        glowDot(lx, ly, 0.22 * k, "#FB923C", 0.6);
        ctx.fillStyle = "#F97316"; ctx.beginPath(); ctx.ellipse(lx, ly, 0.08 * k, 0.11 * k, 0, 0, 6.3); ctx.fill();
      }
      if (k > 20) { ctx.fillStyle = "#FEF3C7"; ctx.font = "800 " + Math.round(0.16 * k) + "px " + FONT; ctx.textAlign = "center"; ctx.textBaseline = "middle"; ctx.fillText("RAMEN", X, Y - h * 1.27); }
    }
    function railing(o) {
      // the viaduct's glowing railing, from this post to the next
      var z0 = Math.max(Z_NEAR, zOf(o.s0)), z1 = Math.min(Z_FAR, zOf(o.s0 + 6));
      if (z1 <= z0) return;
      var x = o.side > 0 ? ROAD + 0.3 : -ROAD - 0.3;
      ctx.fillStyle = "#22D3EE";
      quad(PX(x, z0), PY(0.7, z0), PX(x, z0), PY(0.78, z0), PX(x, z1), PY(0.78, z1), PX(x, z1), PY(0.7, z1));
      ctx.fillStyle = "#334155";
      for (var p = 0; p < 6; p += 1.5) {
        var z = zOf(o.s0 + p);
        if (z < Z_NEAR || z > Z_FAR) continue;
        var X = PX(x, z), k = F / z;
        ctx.fillRect(X - Math.max(0.5, 0.025 * k), PY(0.78, z), Math.max(1, 0.05 * k), 0.78 * k);
      }
    }
    /* A frame of the Hyper Tunnel over everything. */
    function frame(o) {
      var z = zOf(o.s0);
      if (z < Z_NEAR + 0.3 || z > Z_FAR) return;
      var k = F / z, XL = PX(-WALK_L + 0.4, z), XR = PX(WALK_R - 0.4, z), top = PY(5.2, z), Y = PY(0, z), w = 0.35 * k;
      ctx.globalAlpha = fade(z);
      rect(XL, top, w, Y - top, "#141A3A"); rect(XR - w, top, w, Y - top, "#141A3A");
      rect(XL, top, XR - XL, w, "#141A3A");
      ctx.fillStyle = rgba(o.col, 0.3);
      ctx.fillRect(XL + w, top + w, XR - XL - 2 * w, Math.max(2, 0.12 * k));
      ctx.fillStyle = o.col;
      ctx.fillRect(XL + w, top + w, XR - XL - 2 * w, Math.max(1, 0.05 * k));
      ctx.fillRect(XL + w, top + w, Math.max(1, 0.05 * k), Y - top - w);
      ctx.fillRect(XR - w - Math.max(1, 0.05 * k), top + w, Math.max(1, 0.05 * k), Y - top - w);
      ctx.globalAlpha = 1;
    }

    /* ------------------------------------------------ things on the tracks */
    function drawObj(o) {
      var z = zOf(o.s);
      if (z > Z_FAR) return;
      if (o.t === "gate") return gate(o, z);
      if (o.t === "tunnel") return tunnel(o, z);
      if (o.t === "train") return train(o);
      if (z < Z_NEAR) return;
      var k = F / z;
      ctx.globalAlpha = fade(z);
      if (o.t === "pylon") pylon(PX(o.side * (ROAD + 0.4), z), PY(0, z), k);
      else if (o.t === "startarch" || o.t === "finish") arch(o, z, k);
      else if (!o.done || o.t === "metro" || o.t === "drones" || o.t === "holo") {
        var X = PX(laneX(o.lane), z), Y = PY(0, z);
        if (o.t === "gem") gem(X, PY(o.y + (calm ? 0 : Math.sin(T * 3 + o.s) * 0.06), z), k);
        else if (o.t === "cone") cone(X, Y, k);
        else if (o.t === "barrier") barrier(X, Y, k);
        else if (o.t === "works") closed(X, Y, k);
        else if (o.t === "crate") crate(o, z);
        else if (o.t === "holo") holo(X, Y, k, o);
        else if (o.t === "metro") metro(o, z);
        else if (o.t === "drones") drones(o, z);
      }
      ctx.globalAlpha = 1;
    }
    function shadow(X, Y, w) {
      ctx.fillStyle = "rgba(2,6,23,.4)";
      ctx.beginPath(); ctx.ellipse(X, Y, w, Math.max(1, w * 0.22), 0, 0, 6.3); ctx.fill();
    }
    function gem(X, Y, k) {
      var w = 0.2 * k, h = 0.26 * k, spin = calm ? 1 : Math.cos(T * 4 + X * 0.01);
      var sx = Math.max(0.25, Math.abs(spin)) * w;
      glowDot(X, Y - h * 0.1, w * 1.9, "#38BDF8", 0.45);
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
    function cone(X, Y, k) {
      shadow(X, Y, 0.24 * k);
      rect(X - 0.22 * k, Y - 0.06 * k, 0.44 * k, 0.06 * k, "#1F2937");
      tri(X - 0.17 * k, Y - 0.06 * k, X, Y - 0.6 * k, X + 0.17 * k, Y - 0.06 * k, "#F97316");
      ctx.fillStyle = "#F8FAFC";
      quadP(X - 0.115 * k, Y - 0.24 * k, X - 0.08 * k, Y - 0.36 * k, X + 0.08 * k, Y - 0.36 * k, X + 0.115 * k, Y - 0.24 * k);
      tri(X - 0.05 * k, Y - 0.1 * k, X - 0.01 * k, Y - 0.55 * k, X + 0.02 * k, Y - 0.1 * k, "rgba(255,255,255,.3)");
    }
    function barrier(X, Y, k) {
      var w = 0.98 * k, h = 0.62 * k;
      shadow(X, Y, w * 0.55);
      rect(X - w * 0.42, Y - h, 0.07 * k, h, "#1F2937"); rect(X + w * 0.42 - 0.07 * k, Y - h, 0.07 * k, h, "#1F2937");
      ctx.save();
      ctx.beginPath(); ctx.rect(X - w / 2, Y - h, w, 0.26 * k); ctx.clip();
      rect(X - w / 2, Y - h, w, 0.26 * k, "#111827");
      ctx.fillStyle = "#F59E0B";
      for (var i = -2; i < 8; i++) { var x0 = X - w / 2 + i * 0.22 * k; quadP(x0, Y - h + 0.26 * k, x0 + 0.11 * k, Y - h + 0.26 * k, x0 + 0.22 * k, Y - h, x0 + 0.11 * k, Y - h); }
      ctx.restore();
      var on = calm || Math.sin(T * 8) > 0;
      if (on) glowDot(X, Y - h - 0.08 * k, 0.22 * k, "#FBBF24", 0.7);
      ctx.fillStyle = on ? "#FDE047" : "#B45309";
      ctx.beginPath(); ctx.arc(X, Y - h - 0.08 * k, 0.07 * k, 0, 6.3); ctx.fill();
    }
    function closed(X, Y, k) {
      // the closed middle track: a red hologram wall with a sign
      var w = 1.0 * k, h = 1.3 * k, a0 = ctx.globalAlpha, flick = calm ? 0.9 : 0.75 + 0.15 * Math.sin(T * 11);
      ctx.globalAlpha = a0 * flick;
      rect(X - w / 2, Y - h, w, h, "rgba(248,113,113,.3)");
      ctx.strokeStyle = "#F87171"; ctx.lineWidth = Math.max(1, 0.04 * k);
      ctx.strokeRect(X - w / 2, Y - h, w, h);
      ctx.fillStyle = "rgba(255,255,255,.18)";
      for (var y = Y - h + 0.1 * k; y < Y; y += 0.12 * k) ctx.fillRect(X - w / 2, y, w, Math.max(0.5, 0.02 * k));
      ctx.globalAlpha = a0;
      rect(X - 0.4 * k, Y - h * 0.72, 0.8 * k, 0.42 * k, "#7F1D1D");
      if (k > 14) {
        ctx.fillStyle = "#FEE2E2"; ctx.font = "800 " + Math.round(0.13 * k) + "px " + FONT; ctx.textAlign = "center"; ctx.textBaseline = "middle";
        ctx.fillText("TRACK", X, Y - h * 0.72 + 0.12 * k); ctx.fillText("CLOSED", X, Y - h * 0.72 + 0.29 * k);
      }
    }
    function crate(o, z) {
      var x = laneX(o.lane), s = 0.72, zf = zOf(o.s + s), k = F / z;
      var X0 = PX(x - s / 2, z), X1 = PX(x + s / 2, z), Y0 = PY(s, z), Y1 = PY(0, z);
      shadow((X0 + X1) / 2, Y1, (X1 - X0) * 0.6);
      if (camH > s && zf > z) {                      // the lid, from above
        ctx.fillStyle = "#4B5574";
        quad(PX(x - s / 2, z), PY(s, z), PX(x + s / 2, z), PY(s, z), PX(x + s / 2, zf), PY(s, zf), PX(x - s / 2, zf), PY(s, zf));
      }
      var sd = x - camX > 0 ? -1 : 1;
      if (Math.abs(x - camX) > 0.1 && zf > z) {
        ctx.fillStyle = "#262C46";
        var xs = x + sd * s / 2;
        quad(PX(xs, z), PY(0, z), PX(xs, z), PY(s, z), PX(xs, zf), PY(s, zf), PX(xs, zf), PY(0, zf));
      }
      rect(X0, Y0, X1 - X0, Y1 - Y0, "#363E5E");
      var lw = Math.max(1, 0.035 * k);
      ctx.strokeStyle = "#8C9AC0"; ctx.lineWidth = lw;
      ctx.strokeRect(X0 + lw, Y0 + lw, X1 - X0 - lw * 2, Y1 - Y0 - lw * 2);
      ctx.beginPath(); ctx.moveTo(X0 + lw, Y0 + lw); ctx.lineTo(X1 - lw, Y1 - lw);
      ctx.moveTo(X1 - lw, Y0 + lw); ctx.lineTo(X0 + lw, Y1 - lw); ctx.stroke();
      rect(X0, Y0 + (Y1 - Y0) * 0.45, X1 - X0, Math.max(1, 0.03 * k), "#22D3EE");
    }
    function holo(X, Y, k, o) {
      var w = 1.05 * k, h = 1.75 * k, a0 = ctx.globalAlpha, flick = calm ? 0.85 : 0.72 + 0.18 * Math.sin(T * 13 + o.s);
      ctx.globalAlpha = a0 * flick;
      rect(X - w / 2, Y - h, w, h, "rgba(34,211,238,.24)");
      ctx.strokeStyle = "rgba(103,232,249,.4)"; ctx.lineWidth = Math.max(2, 0.12 * k);
      ctx.strokeRect(X - w / 2, Y - h, w, h);
      ctx.strokeStyle = "#A5F3FC"; ctx.lineWidth = Math.max(1, 0.035 * k);
      ctx.strokeRect(X - w / 2, Y - h, w, h);
      ctx.fillStyle = "rgba(255,255,255,.14)";
      var off = calm ? 0 : (T * 0.6 * k) % (0.14 * k);
      for (var y = Y - h + off; y < Y; y += 0.14 * k) ctx.fillRect(X - w / 2, y, w, Math.max(0.5, 0.025 * k));
      ctx.strokeStyle = "#E0FBFF"; ctx.lineWidth = Math.max(1.2, 0.06 * k);
      ctx.beginPath(); ctx.arc(X, Y - h * 0.55, 0.26 * k, 0, 6.3); ctx.moveTo(X - 0.18 * k, Y - h * 0.55); ctx.lineTo(X + 0.18 * k, Y - h * 0.55); ctx.stroke();
      ctx.globalAlpha = a0;
      rect(X - w / 2, Y - 0.06 * k, w, 0.06 * k, "#334155");
    }
    /* A long box on the tracks: its side towards the middle of the view, and its roof if it is low. */
    function boxSides(x, w, h, zr, zf, side, sideCol, top) {
      var xs = x + side * w / 2;
      if (zf > zr && Math.abs(x - camX) > 0.12) {
        ctx.fillStyle = sideCol;
        quad(PX(xs, zr), PY(0.1, zr), PX(xs, zr), PY(h, zr), PX(xs, zf), PY(h, zf), PX(xs, zf), PY(0.1, zf));
      }
      if (camH > h && zf > zr) {
        ctx.fillStyle = top;
        quad(PX(x - w / 2, zr), PY(h, zr), PX(x + w / 2, zr), PY(h, zr), PX(x + w / 2, zf), PY(h, zf), PX(x - w / 2, zf), PY(h, zf));
      }
    }
    function carWindows(x, side, w, s0, len, y0, y1, colour, people) {
      var xs = x + side * w / 2;
      for (var p = 0.4; p < len - 0.4; p += 1.15) {
        var za = zOf(s0 + p), zb = zOf(s0 + p + 0.8);
        if (zb < Z_NEAR || za > Z_FAR) continue;
        za = Math.max(Z_NEAR, za);
        ctx.fillStyle = colour;
        quad(PX(xs, za), PY(y0, za), PX(xs, za), PY(y1, za), PX(xs, zb), PY(y1, zb), PX(xs, zb), PY(y0, zb));
        if (people && F / za > 30 && ((s0 + p) * 3.1) % 2 > 0.8) {
          var zm = (za + zb) / 2, km = F / zm;
          ctx.fillStyle = "#3B2F4A";
          ctx.beginPath(); ctx.arc(PX(xs, zm), PY(y0 + (y1 - y0) * 0.45, zm), (y1 - y0) * 0.18 * km, 0, 6.3); ctx.fill();
          ctx.fillRect(PX(xs, zm) - (y1 - y0) * 0.22 * km, PY(y0 + (y1 - y0) * 0.28, zm), (y1 - y0) * 0.44 * km, (y1 - y0) * 0.28 * km);
        }
      }
    }
    function roundRectPx(x, y, w, h, r) {
      ctx.beginPath(); ctx.moveTo(x + r, y); ctx.lineTo(x + w - r, y); ctx.quadraticCurveTo(x + w, y, x + w, y + r);
      ctx.lineTo(x + w, y + h); ctx.lineTo(x, y + h); ctx.lineTo(x, y + r); ctx.quadraticCurveTo(x, y, x + r, y); ctx.closePath();
    }
    function metro(o, z) {
      var x = laneX(o.lane), w = 1.12, h = 2.3;
      var zr = Math.max(Z_NEAR + 0.01, z), zf = Math.min(Z_FAR, zOf(o.s + o.len));
      var side = x - camX > 0 ? -1 : 1;
      boxSides(x, w, h, zr, zf, side, "#3E4A70", "#5B6688");
      if (zf > zr && Math.abs(x - camX) > 0.12) {
        carWindows(x, side, w, o.s, o.len, 1.05, 1.85, "#FCD9A0", true);
        var xs = x + side * w / 2;
        ctx.fillStyle = "#22D3EE";
        quad(PX(xs, zr), PY(0.55, zr), PX(xs, zr), PY(0.65, zr), PX(xs, zf), PY(0.65, zf), PX(xs, zf), PY(0.55, zf));
      }
      var k = F / zr, X = PX(x, zr), Y = PY(0, zr);
      ctx.globalAlpha = fade(zr);
      // the back of the car: a window, its line number and red lights
      ctx.fillStyle = "#C9D3E6";
      roundRectPx(X - w / 2 * k, Y - h * k, w * k, (h - 0.1) * k, 0.22 * k); ctx.fill();
      rect(X - w * 0.4 * k, Y - 2.05 * k, w * 0.8 * k, 0.7 * k, "#1E2A4A");
      rect(X - w * 0.36 * k, Y - 2.0 * k, w * 0.72 * k, 0.12 * k, "rgba(255,255,255,.18)");
      rect(X - w / 2 * k, Y - 1.05 * k, w * k, 0.12 * k, "#2563EB");
      rect(X - w / 2 * k, Y - 0.92 * k, w * k, 0.06 * k, "#22D3EE");
      rect(X - 0.26 * k, Y - 2.28 * k, 0.52 * k, 0.18 * k, "#0B1028");
      if (k > 16) { ctx.fillStyle = "#FDE047"; ctx.font = "800 " + Math.round(0.12 * k) + "px " + FONT; ctx.textAlign = "center"; ctx.textBaseline = "middle"; ctx.fillText("LINE " + o.n, X, Y - 2.19 * k); }
      [-1, 1].forEach(function (sd) {
        glowDot(X + sd * w * 0.36 * k, Y - 0.55 * k, 0.35 * k, "#EF4444", 0.6);
        rect(X + sd * w * 0.36 * k - 0.08 * k, Y - 0.62 * k, 0.16 * k, 0.14 * k, "#FCA5A5");
      });
      rect(X - w * 0.45 * k, Y - 0.16 * k, w * 0.9 * k, 0.1 * k, "#1E293B");
      ctx.globalAlpha = 1;
    }
    /* A train on the side track: waiting at the station, or rushing past. */
    function train(o) {
      var x = TRAIN_X, w = 1.2, h = 2.35;
      var zr = zOf(o.s), zf = Math.min(Z_FAR, zOf(o.s + o.len));
      if (zf < Z_NEAR || zr > Z_FAR) return;
      var near = Math.max(Z_NEAR + 0.01, zr), xs = x + w / 2;
      boxSides(x, w, h, near, zf, 1, "#9AA7C4", "#5B6688");
      // windows with people, gaps between the cars, and glowing stripes along the side
      for (var c = 0; c < o.cars; c++) {
        var c0 = o.s + c * (o.len / o.cars), cl = o.len / o.cars - 0.5;
        carWindows(x, 1, w, c0, cl, 1.05, 1.9, "#FDE3B3", true);
        var g0 = Math.max(Z_NEAR, zOf(c0 + cl)), g1 = zOf(c0 + cl + 0.5);
        if (g1 > Z_NEAR && g0 < Z_FAR) { ctx.fillStyle = "#1E2440"; quad(PX(xs, g0), PY(0.1, g0), PX(xs, g0), PY(h, g0), PX(xs, g1), PY(h, g1), PX(xs, g1), PY(0.1, g1)); }
      }
      ctx.fillStyle = "#E879F9";
      quad(PX(xs, near), PY(0.62, near), PX(xs, near), PY(0.74, near), PX(xs, zf), PY(0.74, zf), PX(xs, zf), PY(0.62, zf));
      ctx.fillStyle = "#2563EB";
      quad(PX(xs, near), PY(0.74, near), PX(xs, near), PY(0.86, near), PX(xs, zf), PY(0.86, zf), PX(xs, zf), PY(0.74, zf));
      if (zr < Z_NEAR) return;
      // the end facing us: headlights if it is coming, red lights if it is waiting
      var k = F / zr, X = PX(x, zr), Y = PY(0, zr);
      ctx.globalAlpha = fade(zr);
      ctx.fillStyle = "#D5DEEE";
      roundRectPx(X - w / 2 * k, Y - h * k, w * k, (h - 0.1) * k, 0.3 * k); ctx.fill();
      rect(X - w * 0.42 * k, Y - 2.1 * k, w * 0.84 * k, 0.75 * k, "#16203F");
      rect(X - w / 2 * k, Y - 1.1 * k, w * k, 0.1 * k, "#2563EB");
      var lights = o.v < 0 ? "#FEF9C3" : "#F87171";
      [-1, 1].forEach(function (sd) {
        glowDot(X + sd * w * 0.34 * k, Y - 0.6 * k, (o.v < 0 ? 0.9 : 0.35) * k, lights, 0.65);
        rect(X + sd * w * 0.34 * k - 0.09 * k, Y - 0.67 * k, 0.18 * k, 0.14 * k, lights);
      });
      if (k > 14) { ctx.fillStyle = "#67E8F9"; ctx.font = "800 " + Math.round(0.14 * k) + "px " + FONT; ctx.textAlign = "center"; ctx.textBaseline = "middle"; ctx.fillText("NEO CITY", X, Y - 2.25 * k); }
      ctx.globalAlpha = 1;
    }
    function drones(o, z) {
      o.bots.forEach(function (b) {
        var bz = z + b.ds, X, Y, k;
        if (b.fly) {
          b.fly += 1 / 60;
          var fz = Math.max(Z_NEAR + 0.2, bz + b.vz * b.fly);
          k = F / fz;
          X = PX(laneX(o.lane) + b.dx + b.vx * b.fly, fz);
          Y = PY(0.7 + b.vy * b.fly, fz);
        } else {
          if (bz < Z_NEAR) return;
          k = F / bz; X = PX(laneX(o.lane) + b.dx, bz); Y = PY(0.6 + (calm ? 0 : Math.sin(T * 4 + b.ph) * 0.06), bz);
          shadow(X, PY(0, bz), 0.16 * k);
        }
        if (b.fly > 2.5) return;
        var s = 0.16 * k;
        ctx.fillStyle = "#334155";
        ctx.fillRect(X - s * 1.3, Y - s * 0.1, s * 2.6, Math.max(1, s * 0.16));
        ctx.fillStyle = "#CBD5E1";
        ctx.beginPath(); ctx.ellipse(X, Y, s * 0.6, s * 0.38, 0, 0, 6.3); ctx.fill();
        ctx.fillStyle = "#22D3EE"; ctx.beginPath(); ctx.arc(X, Y, s * 0.17, 0, 6.3); ctx.fill();
        var spin = calm ? 0.6 : Math.abs(Math.sin(T * 40 + b.ph));
        ctx.fillStyle = "rgba(226,232,240,.75)";
        [-1, 1].forEach(function (sd) { ctx.fillRect(X + sd * s * 1.3 - s * 0.5 * spin, Y - s * 0.32, s * spin, Math.max(1, s * 0.1)); });
      });
    }
    function pylon(X, Y, k) {
      var w = Math.max(1, 0.1 * k);
      rect(X - w / 2, Y - 1.7 * k, w, 1.7 * k, "#1E2440");
      var on = calm || Math.sin(T * 5) > -0.2;
      if (on) glowDot(X, Y - 1.75 * k, 0.5 * k, "#22D3EE", 0.6);
      ctx.fillStyle = on ? "#A5F3FC" : "#0E7490";
      ctx.beginPath(); ctx.arc(X, Y - 1.75 * k, 0.12 * k, 0, 6.3); ctx.fill();
      ctx.fillStyle = "#22D3EE";
      for (var i = 0; i < 3; i++) ctx.fillRect(X - w / 2, Y - (0.4 + i * 0.4) * k, w, Math.max(1, 0.05 * k));
    }
    function arch(o, z, k) {
      var finish = o.t === "finish";
      var X0 = PX(-ROAD - 0.15, z), X1 = PX(ROAD + 0.15, z), Y = PY(0, z), top = PY(2.75, z);
      var col = finish ? "#FDE047" : "#22D3EE";
      rect(X0 - 0.09 * k, top, 0.18 * k, Y - top, "#1E2440");
      rect(X1 - 0.09 * k, top, 0.18 * k, Y - top, "#1E2440");
      rect(X0 - 0.03 * k, top, 0.06 * k, Y - top, col);
      rect(X1 - 0.03 * k, top, 0.06 * k, Y - top, col);
      if (k > 9) {
        var label = finish ? "FINISH" : "CITY RUN";
        ctx.font = "800 " + Math.round(0.36 * k) + "px " + FONT; ctx.textAlign = "center"; ctx.textBaseline = "middle";
        var tw = ctx.measureText(label).width + 0.5 * k, mx = (X0 + X1) / 2, edge = finish ? "#FDE047" : "#E879F9";
        glowDot(mx, top, tw * 0.7, edge, 0.35);
        rect(mx - tw / 2, top - 0.42 * k, tw, 0.5 * k, "#0A0E2A");
        ctx.strokeStyle = edge; ctx.lineWidth = Math.max(1.5, 0.05 * k);
        ctx.strokeRect(mx - tw / 2, top - 0.42 * k, tw, 0.5 * k);
        ctx.fillStyle = finish ? "#FEF9C3" : "#F5D0FE";
        if (!calm) { ctx.shadowColor = edge; ctx.shadowBlur = Math.min(16, 0.2 * k); }
        ctx.fillText(label, mx, top - 0.17 * k);
        ctx.shadowBlur = 0;
      }
    }
    /* The Hyper Tunnel at the finish: rings of neon over the tracks, one
       behind the other, with a bright light at the far end. */
    function tunnel(o, z) {
      var rings = [0, 6, 12, 18, 24, 30];
      for (var n = rings.length - 1; n >= 0; n--) {
        var zz = z + rings[n];
        if (zz < Z_NEAR + 0.3 || zz > Z_FAR) continue;
        var k = F / zz, cxp = PX(0, zz), base = PY(0, zz), R = 3.3 * k, cy = PY(0.5, zz);
        ctx.globalAlpha = fade(zz);
        if (n === rings.length - 1) {
          var g = ctx.createRadialGradient(cxp, cy, 0, cxp, cy, R);
          g.addColorStop(0, "rgba(240,253,255,1)"); g.addColorStop(0.4, "rgba(103,232,249,.85)"); g.addColorStop(1, "rgba(30,58,138,.35)");
          ctx.fillStyle = g;
          ctx.beginPath(); ctx.arc(cxp, cy, R, Math.PI, 0); ctx.lineTo(cxp + R, base); ctx.lineTo(cxp - R, base); ctx.closePath(); ctx.fill();
        }
        var col = n % 2 ? "#22D3EE" : "#E879F9";
        ctx.beginPath(); ctx.arc(cxp, cy, R, Math.PI, 0); ctx.lineTo(cxp + R, base); ctx.moveTo(cxp - R, cy); ctx.lineTo(cxp - R, base);
        ctx.strokeStyle = n === 0 ? "#1E2440" : rgba(col, 0.3); ctx.lineWidth = (n === 0 ? 0.9 : 0.3) * k; ctx.stroke();
        ctx.strokeStyle = col; ctx.lineWidth = Math.max(1.5, 0.1 * k); ctx.stroke();
        if (n === 0) {
          ctx.strokeStyle = "#E879F9"; ctx.lineWidth = Math.max(1.5, 0.12 * k);
          ctx.beginPath(); ctx.arc(cxp, cy, R * 1.08, Math.PI, 0); ctx.stroke();
          ctx.fillStyle = "#22D3EE";
          for (var i = 0; i < 7; i++) { var a = Math.PI + (i + 0.5) * Math.PI / 7; ctx.fillRect(cxp + Math.cos(a) * R * 1.04 - 0.1 * k, cy + Math.sin(a) * R * 1.04 - 0.04 * k, 0.2 * k, 0.08 * k); }
        }
      }
      ctx.globalAlpha = 1;
    }

    /* The answer gates: a neon arch over each answer track, with its letter,
       and the cat bursts through the one it is on. */
    function gate(o, z) {
      var g = o.g;
      if (z < Z_NEAR + 0.05) return;
      var k = F / z, Y = PY(0, z), age = g.passed ? T - g.burst : -1;
      ctx.globalAlpha = fade(z);
      for (var l = 0; l < 3; l++) {
        var L = g.lanes[l];
        if (!L) continue;
        var x = laneX(l), X0 = PX(x - 0.56, z), X1 = PX(x + 0.56, z), mx = (X0 + X1) / 2, r = (X1 - X0) / 2;
        var top = PY(1.55, z), chosen = g.passed && g.chosen === l, right = g.passed && g.res && g.res.right === l;
        ctx.beginPath();
        ctx.moveTo(X0, Y); ctx.lineTo(X0, top); ctx.arc(mx, top, r, Math.PI, 0); ctx.lineTo(X1, Y);
        if (!chosen || age < 0.25) {
          ctx.fillStyle = rgba(L.c, chosen ? 0.5 * Math.max(0, 1 - age / 0.25) : g.passed && !right ? 0.12 : 0.26);
          ctx.fill();
        }
        ctx.strokeStyle = rgba(L.c, 0.35); ctx.lineWidth = Math.max(3, 0.16 * k); ctx.stroke();
        ctx.strokeStyle = L.c; ctx.lineWidth = Math.max(1.5, 0.06 * k); ctx.stroke();
        if (chosen) continue;
        ctx.fillStyle = "rgba(255,255,255,.1)";
        for (var yy = top - r * 0.6; yy < Y; yy += Math.max(3, 0.14 * k)) ctx.fillRect(X0 + 1, yy, X1 - X0 - 2, Math.max(0.5, 0.025 * k));
        var cy = PY(1.32, z);
        ctx.fillStyle = "#fff";
        ctx.beginPath(); ctx.arc(mx, cy, 0.27 * k, 0, 6.3); ctx.fill();
        if (L.icon) {
          var ir = 0.12 * k;
          ctx.strokeStyle = L.ink || L.c; ctx.lineWidth = Math.max(1.5, 0.07 * k); ctx.lineCap = "round"; ctx.lineJoin = "round";
          ctx.beginPath();
          if (L.icon === "tick") { ctx.moveTo(mx - ir, cy + 0.01 * k); ctx.lineTo(mx - ir * 0.25, cy + ir * 0.75); ctx.lineTo(mx + ir * 1.05, cy - ir * 0.8); }
          else { ctx.moveTo(mx - ir * 0.8, cy - ir * 0.8); ctx.lineTo(mx + ir * 0.8, cy + ir * 0.8); ctx.moveTo(mx + ir * 0.8, cy - ir * 0.8); ctx.lineTo(mx - ir * 0.8, cy + ir * 0.8); }
          ctx.stroke();
        } else if (k > 7) {
          ctx.fillStyle = L.ink || "#0A0E2A"; ctx.textAlign = "center"; ctx.textBaseline = "middle";
          ctx.font = "800 " + Math.round(0.34 * k) + "px " + FONT;
          ctx.fillText(L.t, mx, cy + 0.02 * k);
        }
        if (k > 26 && L.s) {
          ctx.fillStyle = "#fff"; ctx.font = "700 " + Math.round(0.135 * k) + "px Inter, sans-serif";
          ctx.shadowColor = "rgba(2,6,23,.9)"; ctx.shadowBlur = 4;
          wrapText(L.s, mx, PY(0.78, z), X1 - X0 - 0.2 * k, 0.16 * k, 3);
          ctx.shadowBlur = 0;
        }
        if (right && g.res && !g.res.ok) {
          ctx.strokeStyle = "#4ADE80"; ctx.lineWidth = Math.max(2, 0.09 * k);
          ctx.beginPath(); ctx.moveTo(X0, Y); ctx.lineTo(X0, top); ctx.arc(mx, top, r, Math.PI, 0); ctx.lineTo(X1, Y); ctx.stroke();
        }
      }
      ctx.globalAlpha = 1;
    }
    function wrapText(text, x, y, maxW, lh, maxLines) {
      var words = String(text).split(/\s+/), lines = [], line = "", i;
      for (i = 0; i < words.length; i++) {
        var test = line ? line + " " + words[i] : words[i];
        if (ctx.measureText(test).width > maxW && line) { lines.push(line); line = words[i]; } else line = test;
        if (lines.length === maxLines) break;
      }
      if (lines.length < maxLines && line) lines.push(line);
      if (lines.length === maxLines && i < words.length) {
        var lastL = lines[maxLines - 1];
        while (lastL.length > 1 && ctx.measureText(lastL + "…").width > maxW) lastL = lastL.slice(0, -1);
        lines[maxLines - 1] = lastL + "…";
      }
      lines.forEach(function (l, n) { ctx.fillText(l, x, y + n * lh); });
    }

    /* ----------------------------------------------------------- the cat
       Seen from behind as it runs on two legs: a white helmet with pointed
       ears and side lights, a backpack with a glowing panel, arms and legs
       swinging, and a thin tail with a glowing tip. */
    function capsule(x1, y1, x2, y2, r, fill, ink, lw) {
      ctx.lineCap = "round";
      ctx.strokeStyle = ink; ctx.lineWidth = r * 2 + lw * 2;
      ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.stroke();
      ctx.strokeStyle = fill; ctx.lineWidth = r * 2;
      ctx.beginPath(); ctx.moveTo(x1, y1); ctx.lineTo(x2, y2); ctx.stroke();
    }
    function drawCat() {
      var k = F / Z_CAT, gx = PX(cat.x, Z_CAT), gy = PY(0, Z_CAT);
      var blink = cat.safe > 0 && !calm && cat.hurt <= 0 && Math.floor(T * 12) % 2 === 0;
      var run = v > 0.6 && started, air = cat.y > 0.05;
      var stride = run && !air ? Math.sin(cat.phase) : 0;
      var bob = run && !calm && !air ? Math.abs(Math.cos(cat.phase)) * 0.05 * k : Math.sin(T * 2.4) * 0.008 * k;
      ctx.save();
      ctx.globalAlpha = 0.35 * Math.max(0.25, 1 - cat.y / 1.4);
      ctx.fillStyle = "#020617";
      ctx.beginPath(); ctx.ellipse(gx, gy, 0.3 * k * (1 - cat.y * 0.18), 0.075 * k, 0, 0, 6.3); ctx.fill();
      ctx.restore();
      ctx.save();
      if (blink) ctx.globalAlpha = 0.4;
      ctx.translate(gx, gy - cat.y * k - bob);
      var wob = cat.hurt > 0 && !calm ? Math.sin(T * 40) * 0.18 * cat.hurt : 0;
      ctx.rotate(cat.lean * 0.6 + wob);
      var sq = cat.squash;
      ctx.scale(1 + sq * 0.5, 1 - sq);
      var u = k * 0.92;
      ctx.scale(u, u);
      ctx.lineJoin = "round"; ctx.lineCap = "round";
      var lw = Math.max(1.2, 0.022 * k) / u;
      var ink = "#1E2B4F";
      var white = ctx.createLinearGradient(-0.3, -1.2, 0.3, 0);
      white.addColorStop(0, "#FFFFFF"); white.addColorStop(0.45, "#EAF2FB"); white.addColorStop(1, "#AFC3DD");
      var cheer = cat.cheer > 0;
      // legs: the one kicking back towards us shows its glowing sole
      [-1, 1].forEach(function (sd, i) {
        var swing = i ? -stride : stride;             // above zero: this leg reaches forward, away from us
        var hipX = sd * 0.085, hipY = -0.36;
        var lift = air ? 0.12 : Math.max(0, -swing) * 0.17;
        var reach = air ? 0 : Math.max(0, swing) * 0.06;
        var footX = sd * 0.1, footY = -0.035 - lift - reach;
        capsule(hipX, hipY, footX, footY, 0.055, white, ink, lw);
        ctx.fillStyle = "#2D4A86"; ctx.beginPath(); ctx.arc((hipX + footX) / 2, (hipY + footY) / 2, 0.035, 0, 6.3); ctx.fill();
        ctx.fillStyle = "#2B3F75"; ctx.strokeStyle = ink; ctx.lineWidth = lw;
        roundRect(footX - 0.07, footY - 0.03, 0.14, 0.075, 0.03); ctx.fill(); ctx.stroke();
        if (lift > 0.05) {
          ctx.fillStyle = "rgba(34,211,238,.45)"; ctx.beginPath(); ctx.ellipse(footX, footY + 0.05, 0.09, 0.03, 0, 0, 6.3); ctx.fill();
          ctx.fillStyle = "#67E8F9"; ctx.fillRect(footX - 0.05, footY + 0.035, 0.1, 0.014);
        }
      });
      // the tail, curling up to one side
      var sw = calm ? 0.2 : Math.sin(T * (run ? 7 : 2.5)) * (run ? 0.3 : 0.18);
      var px0 = 0.04, py0 = -0.34, ang = -0.3 + sw * 0.3, seg = 0.075, pts = [[px0, py0]];
      for (var j = 0; j < 8; j++) { ang -= 0.2 + sw * 0.04; px0 += Math.cos(ang) * seg; py0 += Math.sin(ang) * seg; pts.push([px0, py0]); }
      ctx.beginPath(); ctx.moveTo(pts[0][0], pts[0][1]);
      for (var n = 1; n < pts.length; n++) ctx.lineTo(pts[n][0], pts[n][1]);
      ctx.strokeStyle = ink; ctx.lineWidth = 0.06 + lw * 2; ctx.stroke();
      ctx.strokeStyle = "#E2EAF5"; ctx.lineWidth = 0.06; ctx.stroke();
      var tip = pts[pts.length - 1];
      glowDotU(tip[0], tip[1], 0.11, "#22D3EE", 0.6);
      ctx.fillStyle = "#67E8F9"; ctx.beginPath(); ctx.arc(tip[0], tip[1], 0.04, 0, 6.3); ctx.fill();
      // the body
      ctx.fillStyle = white; ctx.strokeStyle = ink; ctx.lineWidth = lw;
      roundRect(-0.17, -0.68, 0.34, 0.38, 0.12); ctx.fill(); ctx.stroke();
      ctx.fillStyle = "#2D4A86"; ctx.fillRect(-0.165, -0.37, 0.33, 0.045);
      // arms swing against the legs, or go up for a cheer or a jump
      [-1, 1].forEach(function (sd, i) {
        var swing = i ? stride : -stride;
        var shX = sd * 0.19, shY = -0.62, hx, hyy;
        if (cheer || air) { hx = sd * 0.3; hyy = -0.95 + (cheer && !calm ? Math.sin(T * 12 + i) * 0.03 : 0); }
        else { hx = sd * (0.25 + Math.max(0, -swing) * 0.03); hyy = -0.42 - swing * 0.08 - Math.max(0, swing) * 0.05; }
        capsule(shX, shY, hx, hyy, 0.048, white, ink, lw);
        ctx.fillStyle = "#2D4A86"; ctx.beginPath(); ctx.arc((shX + hx) / 2, (shY + hyy) / 2, 0.03, 0, 6.3); ctx.fill();
        ctx.fillStyle = "#3B5BA5"; ctx.strokeStyle = ink; ctx.lineWidth = lw;
        ctx.beginPath(); ctx.arc(hx, hyy, 0.055, 0, 6.3); ctx.fill(); ctx.stroke();
      });
      // the head: a helmet with ears glowing at the edges and lights at the sides
      var hb = run && !calm ? Math.sin(cat.phase * 2 + 0.6) * 0.01 : 0;
      ctx.save(); ctx.translate(0, hb);
      [-1, 1].forEach(function (sd) {
        ctx.fillStyle = white; ctx.strokeStyle = ink; ctx.lineWidth = lw;
        ctx.beginPath(); ctx.moveTo(sd * 0.215, -0.92); ctx.lineTo(sd * 0.2, -1.24); ctx.lineTo(sd * 0.05, -1.04); ctx.closePath(); ctx.fill(); ctx.stroke();
        ctx.strokeStyle = "#22D3EE"; ctx.lineWidth = lw * 1.6;
        ctx.beginPath(); ctx.moveTo(sd * 0.19, -0.97); ctx.lineTo(sd * 0.19, -1.17); ctx.stroke();
      });
      ctx.fillStyle = white; ctx.strokeStyle = ink; ctx.lineWidth = lw;
      ctx.beginPath(); ctx.ellipse(0, -0.86, 0.255, 0.225, 0, 0, 6.3); ctx.fill(); ctx.stroke();
      [-1, 1].forEach(function (sd) {
        ctx.fillStyle = "#B9C9DE"; ctx.strokeStyle = ink; ctx.lineWidth = lw;
        ctx.beginPath(); ctx.arc(sd * 0.25, -0.84, 0.07, 0, 6.3); ctx.fill(); ctx.stroke();
        ctx.strokeStyle = "#22D3EE"; ctx.lineWidth = lw * 1.4;
        ctx.beginPath(); ctx.arc(sd * 0.25, -0.84, 0.04, 0, 6.3); ctx.stroke();
      });
      ctx.strokeStyle = "#B9C9DE"; ctx.lineWidth = lw * 0.9;
      ctx.beginPath(); ctx.moveTo(0, -1.07); ctx.lineTo(0, -0.66); ctx.stroke();
      ctx.strokeStyle = "#22D3EE"; ctx.lineWidth = lw * 1.8;
      ctx.beginPath(); ctx.moveTo(-0.1, -0.73); ctx.quadraticCurveTo(0, -0.7, 0.1, -0.73); ctx.stroke();
      ctx.restore();
      // the backpack and its glowing panel
      ctx.fillStyle = "#3554A0"; ctx.strokeStyle = ink; ctx.lineWidth = lw;
      roundRect(-0.12, -0.63, 0.24, 0.22, 0.05); ctx.fill(); ctx.stroke();
      glowDotU(0, -0.52, 0.16, "#22D3EE", calm ? 0.45 : 0.4 + 0.15 * Math.sin(T * 4));
      ctx.fillStyle = "#A5F3FC"; roundRect(-0.045, -0.565, 0.09, 0.09, 0.02); ctx.fill();
      if (cheer && !calm) {
        ctx.fillStyle = "#FDE047";
        for (var c = 0; c < 4; c++) { var a2 = T * 6 + c * 1.57; ctx.save(); ctx.translate(Math.cos(a2) * 0.42, -0.9 + Math.sin(a2) * 0.18); star4(0, 0, 0.06); ctx.restore(); }
      }
      if (cat.hurt > 0) {
        for (var h2 = 0; h2 < 3; h2++) {
          var b2 = T * 7 + h2 * 2.09;
          ctx.fillStyle = h2 === 1 ? "#F0ABFC" : "#67E8F9";
          ctx.save(); ctx.translate(Math.cos(b2) * 0.3, -1.2 + Math.sin(b2) * 0.07); star4(0, 0, 0.055); ctx.restore();
        }
      }
      ctx.restore();
    }
    function glowDotU(x, y, r, c, a) {
      var g = ctx.createRadialGradient(x, y, 0, x, y, r);
      g.addColorStop(0, rgba(c, a)); g.addColorStop(1, rgba(c, 0));
      ctx.fillStyle = g; ctx.beginPath(); ctx.arc(x, y, r, 0, 6.3); ctx.fill();
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
        } else if (p.kind === "pixel") {
          ctx.fillStyle = p.c || "#fff"; ctx.fillRect(p.x - p.r / 2, p.y - p.r / 2, p.r, p.r);
        } else if (p.kind === "confetti") {
          ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.a);
          ctx.fillStyle = p.c || "#fff"; ctx.fillRect(-p.r, -p.r * 0.45, p.r * 2, p.r * 0.9);
          ctx.restore();
        } else if (p.kind === "dust") {
          ctx.globalAlpha = a * 0.35; ctx.fillStyle = "#C7D2FE";
          ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, 6.3); ctx.fill();
        } else if (p.kind === "sparkle") {
          ctx.fillStyle = "#fff"; star4(p.x, p.y, p.r * 1.6);
        } else {
          ctx.fillStyle = p.c || "#fff"; ctx.beginPath(); ctx.arc(p.x, p.y, p.r, 0, 6.3); ctx.fill();
        }
      });
      ctx.globalAlpha = 1;
    }
    function speedLines() {
      ctx.strokeStyle = "rgba(165,243,252,.5)"; ctx.lineWidth = 2;
      for (var i = 0; i < 16; i++) {
        var a = (i / 16) * Math.PI * 2 + (Math.floor(T * 20) % 7) * 0.13;
        var r0 = Math.max(W, H) * (0.42 + ((i * 37) % 10) / 40), r1 = r0 + 60 + ((i * 53) % 40);
        ctx.beginPath(); ctx.moveTo(cx + Math.cos(a) * r0, hy + Math.sin(a) * r0 * 0.7); ctx.lineTo(cx + Math.cos(a) * r1, hy + Math.sin(a) * r1 * 0.7); ctx.stroke();
      }
    }

    /* ------------------------------------------------------------- loop */
    function tick(now) {
      if (dead) return;
      raf = requestAnimationFrame(tick);
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
    raf = requestAnimationFrame(tick);

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
      /* Lock in an answer: the cat moves onto that track and sprints to the gate. */
      commit: function (lane) {
        var g = gates[gi];
        if (!g || !g.read || g.passed || g.go || held) return false;
        g.go = true;
        cat.lane = lane;
        dash = true;
        return true;
      },
      /* With the clock off, run on along the track the cat is on. */
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
      /* Where on the canvas a gate's track is, for diamonds to fly from. */
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
