/* Pixel Run: the drawing. Pure canvas code with no knowledge of the rules, so
   the game logic in game.js only ever hands it a description of what to show. */
(function () {
  "use strict";

  var W = 640, H = 360, GROUND = 292, SPRITE = 76;

  /* ------------------------------------------------------------ palettes */
  var PAL = {
    meadow: { sky: ["#8ed4f2", "#e3f6fb"], sun: "#fff2a8", far: "#a9dfb2", mid: "#79c887", top: "#5cb86a", dirt: "#8a6a47", dirt2: "#7a5b3b", deco: "trees", near: "flowers" },
    sunset: { sky: ["#ff9f80", "#ffe0b0"], sun: "#fff3c4", far: "#d78aa8", mid: "#b5688f", top: "#d29a55", dirt: "#7d4a52", dirt2: "#6c3f47", deco: "hills", near: "grass" },
    stream: { sky: ["#9edbe9", "#e8f7ef"], sun: "#fff4bd", far: "#9ccdb9", mid: "#68ad97", top: "#72bb83", dirt: "#68553f", dirt2: "#5a4936", deco: "willows", near: "reeds" },
    lagoon: { sky: ["#84dff0", "#d8f7f3"], sun: "#fff7cf", far: "#86cfc6", mid: "#4fb0a6", top: "#ecdca6", dirt: "#d9c486", dirt2: "#c9b374", deco: "palms", near: "shells" },
    autumn: { sky: ["#f7c690", "#fde9cf"], sun: "#fff2c8", far: "#e0a76f", mid: "#c9793f", top: "#bd8240", dirt: "#6e4a32", dirt2: "#5f3f2a", deco: "autumn", near: "leaves" },
    fort:   { sky: ["#93acd0", "#dbe4f1"], sun: "#f7f3dc", far: "#919fb8", mid: "#6f7d9a", top: "#7f8a9c", dirt: "#5b6372", dirt2: "#4e5563", deco: "walls", near: "torches" },
    dunes:  { sky: ["#fad983", "#fef0c6"], sun: "#fff8d6", far: "#ecc67f", mid: "#dcad60", top: "#e5bc6c", dirt: "#c79349", dirt2: "#b6833d", deco: "dunes", near: "stones" },
    summit: { sky: ["#bcd8f2", "#f0f7fd"], sun: "#ffffff", far: "#cddcec", mid: "#acc3dc", top: "#f6fafe", dirt: "#93a7be", dirt2: "#8497ae", deco: "peaks", near: "pines" },
    ruins:  { sky: ["#8c76ba", "#d7bcde"], sun: "#f6e9ff", far: "#7d6da9", mid: "#62539a", top: "#8070ae", dirt: "#4d4270", dirt2: "#41375f", deco: "ruins", near: "rubble" },
    castle: { sky: ["#1c2250", "#4b3c7c"], sun: "#f7f2d3", far: "#313170", mid: "#26275a", top: "#41417a", dirt: "#1c1c3d", dirt2: "#16162f", deco: "turrets", near: "torches", night: true }
  };

  /* ----------------------------------------------------------- obstacles
     hop: flat on top, so Pixel lands on it and hops off the far side. */
  var OB = {
    pipe:   { w: 56, h: 78, hop: true },
    crate:  { w: 58, h: 58, hop: true },
    barrel: { w: 50, h: 62, hop: true },
    log:    { w: 84, h: 36, hop: true },
    gap:    { w: 150, h: 0, hop: false },
    lava:   { w: 150, h: 0, hop: false },
    spikes: { w: 92, h: 30, hop: false },
    stack:  { w: 56, h: 112, hop: true },
    rock:   { w: 66, h: 46, hop: true },
    cactus: { w: 40, h: 82, hop: false },
    ice:    { w: 58, h: 66, hop: true },
    column: { w: 46, h: 88, hop: true },
    gate:   { w: 40, h: 106, hop: false },
    wall:   { w: 62, h: 90, hop: true },
    cannon: { w: 74, h: 48, hop: true },
    buoy:   { w: 40, h: 52, hop: true }
  };

  function seeded(n) {
    var s = (n * 2654435761) >>> 0;
    return function () {
      s += 0x6D2B79F5;
      var t = s;
      t = Math.imul(t ^ (t >>> 15), t | 1);
      t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  function make(canvas, spriteImg) {
    var ctx = canvas.getContext("2d");
    var scale = 1;
    var skies = {};

    function fit() {
      var dpr = Math.min(window.devicePixelRatio || 1, 2);
      var cw = canvas.clientWidth || W;
      var pw = Math.max(1, Math.round(cw * dpr));
      var ph = Math.max(1, Math.round(cw * dpr * H / W));
      if (canvas.width !== pw || canvas.height !== ph) { canvas.width = pw; canvas.height = ph; }
      scale = canvas.width / W;
    }

    function rr(x, y, w, h, r) {
      r = Math.min(r, w / 2, h / 2);
      ctx.beginPath();
      ctx.moveTo(x + r, y);
      ctx.arcTo(x + w, y, x + w, y + h, r);
      ctx.arcTo(x + w, y + h, x, y + h, r);
      ctx.arcTo(x, y + h, x, y, r);
      ctx.arcTo(x, y, x + w, y, r);
      ctx.closePath();
    }

    function circle(x, y, r, fill) {
      ctx.beginPath(); ctx.arc(x, y, r, 0, 6.2832); ctx.fillStyle = fill; ctx.fill();
    }

    /* ------------------------------------------------------- background */
    function sky(pal, key) {
      var g = skies[key];
      if (!g || g.scale !== scale) {
        var gr = ctx.createLinearGradient(0, 0, 0, GROUND);
        gr.addColorStop(0, pal.sky[0]); gr.addColorStop(1, pal.sky[1]);
        g = skies[key] = { grad: gr, scale: scale };
      }
      ctx.fillStyle = g.grad;
      ctx.fillRect(0, 0, W, H);
    }

    function ridge(base, amp, f1, f2, par, cam, color, phase) {
      ctx.beginPath();
      ctx.moveTo(0, H);
      for (var x = 0; x <= W + 8; x += 8) {
        var wx = x + cam * par;
        ctx.lineTo(x, base - amp * (0.55 * Math.sin(wx * f1 + phase) + 0.45 * Math.sin(wx * f2 + phase * 1.7 + 1.7)));
      }
      ctx.lineTo(W + 8, H);
      ctx.closePath();
      ctx.fillStyle = color;
      ctx.fill();
    }

    function tiles(spacing, par, cam, fn, pad) {
      pad = pad || 80;
      var first = Math.floor((cam * par - pad) / spacing);
      var last = Math.ceil((cam * par + W + pad) / spacing);
      for (var i = first; i <= last; i++) fn(i * spacing - cam * par, i, seeded(i + 7));
    }

    function clouds(cam, t, pal) {
      var col = pal.night ? "rgba(120,110,190,.35)" : "rgba(255,255,255,.78)";
      tiles(210, 0.08, cam, function (x, i, r) {
        var cx = ((x + t * 6) % (W + 260)) - 80;
        if (cx < -80) cx += W + 260;
        var cy = 42 + r() * 70, s = 0.7 + r() * 0.7;
        ctx.fillStyle = col;
        ctx.beginPath();
        ctx.ellipse(cx, cy, 34 * s, 13 * s, 0, 0, 6.2832);
        ctx.ellipse(cx - 20 * s, cy + 4 * s, 22 * s, 10 * s, 0, 0, 6.2832);
        ctx.ellipse(cx + 22 * s, cy + 5 * s, 24 * s, 9 * s, 0, 0, 6.2832);
        ctx.fill();
      }, 140);
    }

    /* Mid layer: one silhouette per palette, drawn dark and slow. */
    var MID = {
      trees: function (x, y, r, c) {
        var s = 0.8 + r() * 0.6;
        ctx.fillStyle = c.trunk; ctx.fillRect(x - 3 * s, y - 34 * s, 6 * s, 34 * s);
        circle(x, y - 46 * s, 22 * s, c.leaf); circle(x - 14 * s, y - 36 * s, 14 * s, c.leaf); circle(x + 14 * s, y - 38 * s, 15 * s, c.leaf);
      },
      hills: function (x, y, r, c) {
        var s = 0.8 + r() * 0.6;
        ctx.fillStyle = c.trunk; ctx.fillRect(x - 2 * s, y - 52 * s, 4 * s, 52 * s);
        ctx.fillStyle = c.leaf;
        ctx.beginPath(); ctx.moveTo(x - 26 * s, y - 10 * s); ctx.lineTo(x, y - 74 * s); ctx.lineTo(x + 26 * s, y - 10 * s); ctx.closePath(); ctx.fill();
      },
      willows: function (x, y, r, c) {
        var s = 0.8 + r() * 0.5;
        ctx.fillStyle = c.trunk; ctx.fillRect(x - 3 * s, y - 40 * s, 6 * s, 40 * s);
        ctx.strokeStyle = c.leaf; ctx.lineWidth = 3;
        for (var k = -3; k <= 3; k++) { ctx.beginPath(); ctx.moveTo(x, y - 44 * s); ctx.quadraticCurveTo(x + k * 12 * s, y - 62 * s, x + k * 15 * s, y - 14 * s); ctx.stroke(); }
      },
      palms: function (x, y, r, c) {
        var s = 0.8 + r() * 0.5, lean = (r() - 0.5) * 18;
        ctx.strokeStyle = c.trunk; ctx.lineWidth = 5 * s;
        ctx.beginPath(); ctx.moveTo(x, y); ctx.quadraticCurveTo(x + lean * 0.4, y - 40 * s, x + lean, y - 74 * s); ctx.stroke();
        ctx.strokeStyle = c.leaf; ctx.lineWidth = 4;
        for (var k = 0; k < 6; k++) {
          var a = -2.9 + k * 0.52;
          ctx.beginPath(); ctx.moveTo(x + lean, y - 74 * s);
          ctx.quadraticCurveTo(x + lean + Math.cos(a) * 26 * s, y - 74 * s + Math.sin(a) * 26 * s - 8, x + lean + Math.cos(a) * 40 * s, y - 74 * s + Math.sin(a) * 40 * s + 14); ctx.stroke();
        }
      },
      autumn: function (x, y, r, c) {
        var s = 0.8 + r() * 0.6, hue = r() < 0.5 ? c.leaf : c.leaf2;
        ctx.fillStyle = c.trunk; ctx.fillRect(x - 3 * s, y - 32 * s, 6 * s, 32 * s);
        circle(x, y - 46 * s, 24 * s, hue); circle(x - 16 * s, y - 34 * s, 15 * s, hue); circle(x + 16 * s, y - 36 * s, 16 * s, hue);
      },
      walls: function (x, y, r, c) {
        var h = 46 + r() * 40, w = 62 + r() * 24;
        ctx.fillStyle = c.leaf; ctx.fillRect(x, y - h, w, h);
        for (var k = 0; k < w; k += 14) ctx.fillRect(x + k, y - h - 8, 8, 8);
        ctx.fillStyle = c.trunk; ctx.fillRect(x + w / 2 - 5, y - 26, 10, 26);
      },
      dunes: function (x, y, r, c) {
        var s = 0.9 + r() * 0.8;
        if (r() < 0.35) {
          ctx.fillStyle = c.leaf; ctx.beginPath(); ctx.moveTo(x - 46 * s, y); ctx.lineTo(x, y - 58 * s); ctx.lineTo(x + 46 * s, y); ctx.closePath(); ctx.fill();
          ctx.fillStyle = c.trunk; ctx.beginPath(); ctx.moveTo(x, y - 58 * s); ctx.lineTo(x + 46 * s, y); ctx.lineTo(x + 10 * s, y); ctx.closePath(); ctx.fill();
        } else {
          ctx.fillStyle = c.leaf; ctx.beginPath(); ctx.ellipse(x, y, 70 * s, 26 * s, 0, Math.PI, 0); ctx.fill();
        }
      },
      peaks: function (x, y, r, c) {
        var s = 0.9 + r() * 0.9;
        ctx.fillStyle = c.leaf; ctx.beginPath(); ctx.moveTo(x - 60 * s, y); ctx.lineTo(x, y - 96 * s); ctx.lineTo(x + 60 * s, y); ctx.closePath(); ctx.fill();
        ctx.fillStyle = "#ffffff"; ctx.beginPath(); ctx.moveTo(x - 17 * s, y - 70 * s); ctx.lineTo(x, y - 96 * s); ctx.lineTo(x + 17 * s, y - 70 * s); ctx.lineTo(x + 6 * s, y - 64 * s); ctx.lineTo(x - 4 * s, y - 72 * s); ctx.closePath(); ctx.fill();
      },
      ruins: function (x, y, r, c) {
        var n = 2 + Math.floor(r() * 3);
        for (var k = 0; k < n; k++) {
          var h = 34 + r() * 56;
          ctx.fillStyle = c.leaf; ctx.fillRect(x + k * 24, y - h, 12, h);
          ctx.fillStyle = c.trunk; ctx.fillRect(x + k * 24 - 3, y - h - 5, 18, 5);
        }
      },
      turrets: function (x, y, r, c) {
        var h = 54 + r() * 50, w = 34 + r() * 14;
        ctx.fillStyle = c.leaf; ctx.fillRect(x, y - h, w, h);
        ctx.beginPath(); ctx.moveTo(x - 6, y - h); ctx.lineTo(x + w / 2, y - h - 30); ctx.lineTo(x + w + 6, y - h); ctx.closePath(); ctx.fill();
        ctx.fillStyle = c.trunk; ctx.fillRect(x + w / 2 - 3, y - h + 14, 6, 12);
        ctx.fillStyle = "#ffd36b"; ctx.fillRect(x + w / 2 - 2, y - h + 16, 4, 8);
      }
    };

    var MIDCOL = {
      trees:   { trunk: "#6a8d5c", leaf: "#5fae70" },
      hills:   { trunk: "#8a5578", leaf: "#a15f86" },
      willows: { trunk: "#4f8c7a", leaf: "#58a58c" },
      palms:   { trunk: "#2f8f88", leaf: "#2b9a8e" },
      autumn:  { trunk: "#8a5a35", leaf: "#d98a3d", leaf2: "#c9602f" },
      walls:   { trunk: "#59647b", leaf: "#6a7791" },
      dunes:   { trunk: "#c99a52", leaf: "#d9aa5d" },
      peaks:   { trunk: "#9db6d0", leaf: "#b4c9df" },
      ruins:   { trunk: "#554788", leaf: "#6a5a9d" },
      turrets: { trunk: "#1b1b45", leaf: "#212255" }
    };

    /* Foreground details that sit on the path itself. */
    var NEAR = {
      flowers: function (x, y, r) {
        ctx.strokeStyle = "#3f9a52"; ctx.lineWidth = 2;
        var cols = ["#ff8fa3", "#ffd25e", "#ffffff", "#c79bff"], k = Math.floor(r() * 4);
        ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x, y - 12); ctx.stroke();
        circle(x, y - 14, 4, cols[k]); circle(x, y - 14, 1.6, "#fff6a8");
      },
      grass: function (x, y) {
        ctx.strokeStyle = "#a8803f"; ctx.lineWidth = 2;
        for (var k = -1; k <= 1; k++) { ctx.beginPath(); ctx.moveTo(x + k * 3, y); ctx.lineTo(x + k * 6, y - 12); ctx.stroke(); }
      },
      reeds: function (x, y) {
        ctx.strokeStyle = "#4a8f5e"; ctx.lineWidth = 2;
        ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + 1, y - 22); ctx.stroke();
        ctx.fillStyle = "#7b5636"; rr(x - 2.5, y - 28, 5, 11, 2.5); ctx.fill();
      },
      shells: function (x, y, r) {
        ctx.fillStyle = r() < 0.5 ? "#f4a8b4" : "#fff1d8";
        ctx.beginPath(); ctx.arc(x, y, 5, Math.PI, 0); ctx.fill();
        ctx.strokeStyle = "#d9879a"; ctx.lineWidth = 1; ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x, y - 5); ctx.stroke();
      },
      leaves: function (x, y, r) {
        ctx.fillStyle = r() < 0.5 ? "#e0702a" : "#d6a02e";
        ctx.beginPath(); ctx.ellipse(x, y - 2, 6, 3, 0.4, 0, 6.2832); ctx.fill();
      },
      torches: function (x, y, r, t, night) {
        ctx.fillStyle = night ? "#6a5a8a" : "#4d4f5a"; ctx.fillRect(x - 2, y - 26, 4, 26);
        var f = 1 + 0.18 * Math.sin(t * 9 + x);
        ctx.fillStyle = "#ffb13b"; ctx.beginPath(); ctx.ellipse(x, y - 32, 5 * f, 8 * f, 0, 0, 6.2832); ctx.fill();
        ctx.fillStyle = "#ffe486"; ctx.beginPath(); ctx.ellipse(x, y - 31, 2.4 * f, 4.5 * f, 0, 0, 6.2832); ctx.fill();
      },
      stones: function (x, y) {
        ctx.fillStyle = "#b5823c"; ctx.beginPath(); ctx.ellipse(x, y - 2, 7, 4, 0, 0, 6.2832); ctx.fill();
      },
      pines: function (x, y, r) {
        var s = 0.7 + r() * 0.5;
        ctx.fillStyle = "#4c7a64";
        for (var k = 0; k < 3; k++) { ctx.beginPath(); ctx.moveTo(x - (14 - k * 3) * s, y - 8 * s - k * 12 * s); ctx.lineTo(x, y - 24 * s - k * 12 * s); ctx.lineTo(x + (14 - k * 3) * s, y - 8 * s - k * 12 * s); ctx.closePath(); ctx.fill(); }
        ctx.fillStyle = "#fff"; ctx.fillRect(x - 3 * s, y - 62 * s, 6 * s, 2.5);
      },
      rubble: function (x, y, r) {
        ctx.fillStyle = "#6c5d9a"; ctx.beginPath(); ctx.moveTo(x - 7, y); ctx.lineTo(x - 3, y - 8 - r() * 4); ctx.lineTo(x + 6, y - 5); ctx.lineTo(x + 8, y); ctx.closePath(); ctx.fill();
      }
    };

    function ground(pal, cam, pits) {
      ctx.fillStyle = pal.dirt; ctx.fillRect(0, GROUND, W, H - GROUND);
      // a band of darker stones, scrolling with the path
      ctx.fillStyle = pal.dirt2;
      tiles(46, 1, cam, function (x, i, r) {
        ctx.beginPath(); ctx.ellipse(x + r() * 20, GROUND + 22 + r() * 36, 6 + r() * 7, 3 + r() * 3, 0, 0, 6.2832); ctx.fill();
      }, 30);
      ctx.fillStyle = pal.top; ctx.fillRect(0, GROUND, W, 11);
      ctx.fillStyle = "rgba(255,255,255,.22)"; ctx.fillRect(0, GROUND, W, 3);
      for (var k = 0; k < pits.length; k++) {
        var p = pits[k], sx = p.x - cam;
        if (sx > W + 10 || sx + p.w < -10) continue;
        // the hole, with sky-coloured air removed from the ground
        ctx.fillStyle = p.lava ? "#3a1020" : "#0e3d52";
        ctx.fillRect(sx, GROUND, p.w, H - GROUND);
        ctx.fillStyle = p.lava ? "#ff7a2a" : "#2aa7c9";
        ctx.fillRect(sx, GROUND + 30, p.w, H - GROUND - 30);
        ctx.fillStyle = p.lava ? "#ffd04a" : "#bff0fb";
        for (var w = 0; w < p.w; w += 22) {
          ctx.fillRect(sx + w + ((p.t * 14) % 22), GROUND + 32, 12, 3);
        }
        // the lip of the ground either side
        ctx.fillStyle = pal.top; ctx.fillRect(sx - 4, GROUND, 4, 11); ctx.fillRect(sx + p.w, GROUND, 4, 11);
      }
    }

    /* -------------------------------------------------------- obstacles */
    var DRAW_OB = {
      pipe: function (x, w, h) {
        var g = ctx.createLinearGradient(x, 0, x + w, 0);
        g.addColorStop(0, "#1f8f4a"); g.addColorStop(0.35, "#4fd17f"); g.addColorStop(1, "#157a3c");
        ctx.fillStyle = g; ctx.fillRect(x + 5, GROUND - h + 20, w - 10, h - 20);
        ctx.fillStyle = g; rr(x, GROUND - h, w, 22, 4); ctx.fill();
        ctx.strokeStyle = "#0f5f2e"; ctx.lineWidth = 2; rr(x, GROUND - h, w, 22, 4); ctx.stroke();
        ctx.fillStyle = "rgba(255,255,255,.28)"; ctx.fillRect(x + 8, GROUND - h + 4, 5, 14);
      },
      crate: function (x, w, h) {
        ctx.fillStyle = "#c98e4e"; ctx.fillRect(x, GROUND - h, w, h);
        ctx.strokeStyle = "#7a4d22"; ctx.lineWidth = 3; ctx.strokeRect(x + 1.5, GROUND - h + 1.5, w - 3, h - 3);
        ctx.lineWidth = 2.5; ctx.beginPath(); ctx.moveTo(x + 4, GROUND - h + 4); ctx.lineTo(x + w - 4, GROUND - 4); ctx.moveTo(x + w - 4, GROUND - h + 4); ctx.lineTo(x + 4, GROUND - 4); ctx.stroke();
      },
      barrel: function (x, w, h) {
        ctx.fillStyle = "#a8683a"; rr(x, GROUND - h, w, h, 12); ctx.fill();
        ctx.fillStyle = "#6b3f22"; ctx.fillRect(x, GROUND - h + 12, w, 5); ctx.fillRect(x, GROUND - 17, w, 5);
        ctx.fillStyle = "rgba(255,255,255,.2)"; ctx.fillRect(x + 8, GROUND - h + 4, 5, h - 8);
      },
      log: function (x, w, h) {
        ctx.fillStyle = "#8f5a2e"; rr(x, GROUND - h, w, h, 10); ctx.fill();
        ctx.fillStyle = "#b8793f"; ctx.beginPath(); ctx.ellipse(x + 8, GROUND - h / 2, 8, h / 2 - 1, 0, 0, 6.2832); ctx.fill();
        ctx.strokeStyle = "#7a4a22"; ctx.lineWidth = 1.5; ctx.beginPath(); ctx.ellipse(x + 8, GROUND - h / 2, 4, h / 2 - 7, 0, 0, 6.2832); ctx.stroke();
        ctx.strokeStyle = "rgba(0,0,0,.18)"; ctx.beginPath(); ctx.moveTo(x + 20, GROUND - h + 9); ctx.lineTo(x + w - 10, GROUND - h + 9); ctx.stroke();
      },
      spikes: function (x, w, h) {
        ctx.fillStyle = "#5c6672";
        var n = Math.round(w / 18);
        for (var k = 0; k < n; k++) {
          var sx = x + k * (w / n);
          ctx.beginPath(); ctx.moveTo(sx, GROUND); ctx.lineTo(sx + w / n / 2, GROUND - h); ctx.lineTo(sx + w / n, GROUND); ctx.closePath(); ctx.fill();
        }
        ctx.fillStyle = "rgba(255,255,255,.3)";
        for (var j = 0; j < n; j++) { var tx = x + j * (w / n); ctx.beginPath(); ctx.moveTo(tx + 3, GROUND - 2); ctx.lineTo(tx + w / n / 2, GROUND - h + 2); ctx.lineTo(tx + w / n / 2 - 1, GROUND - 2); ctx.closePath(); ctx.fill(); }
      },
      stack: function (x, w, h) {
        var each = h / 2;
        for (var k = 0; k < 2; k++) {
          var y = GROUND - each * (k + 1);
          ctx.fillStyle = k ? "#d29a58" : "#c58a4a"; ctx.fillRect(x, y, w, each);
          ctx.strokeStyle = "#7a4d22"; ctx.lineWidth = 3; ctx.strokeRect(x + 1.5, y + 1.5, w - 3, each - 3);
          ctx.lineWidth = 2; ctx.beginPath(); ctx.moveTo(x + 4, y + 4); ctx.lineTo(x + w - 4, y + each - 4); ctx.stroke();
        }
      },
      rock: function (x, w, h) {
        ctx.fillStyle = "#8b929c"; ctx.beginPath(); ctx.moveTo(x, GROUND); ctx.lineTo(x + 6, GROUND - h * 0.62); ctx.lineTo(x + w * 0.3, GROUND - h); ctx.lineTo(x + w * 0.72, GROUND - h * 0.9); ctx.lineTo(x + w, GROUND - h * 0.3); ctx.lineTo(x + w, GROUND); ctx.closePath(); ctx.fill();
        ctx.fillStyle = "rgba(255,255,255,.25)"; ctx.beginPath(); ctx.moveTo(x + 8, GROUND - h * 0.6); ctx.lineTo(x + w * 0.3, GROUND - h + 3); ctx.lineTo(x + w * 0.45, GROUND - h * 0.7); ctx.closePath(); ctx.fill();
      },
      cactus: function (x, w, h) {
        ctx.fillStyle = "#3e9c58"; rr(x + w / 2 - 8, GROUND - h, 16, h, 8); ctx.fill();
        rr(x, GROUND - h * 0.62, 12, 24, 6); ctx.fill(); ctx.fillRect(x + 4, GROUND - h * 0.45, w / 2 - 8, 9);
        rr(x + w - 12, GROUND - h * 0.78, 12, 26, 6); ctx.fill(); ctx.fillRect(x + w / 2 + 2, GROUND - h * 0.58, w / 2 - 8, 9);
        ctx.strokeStyle = "#2b7a42"; ctx.lineWidth = 1.5; ctx.beginPath(); ctx.moveTo(x + w / 2, GROUND - h + 6); ctx.lineTo(x + w / 2, GROUND - 4); ctx.stroke();
      },
      ice: function (x, w, h) {
        var g = ctx.createLinearGradient(x, GROUND - h, x + w, GROUND);
        g.addColorStop(0, "#e6f6ff"); g.addColorStop(1, "#8fcdf0");
        ctx.fillStyle = g; rr(x, GROUND - h, w, h, 6); ctx.fill();
        ctx.strokeStyle = "#5fa8d3"; ctx.lineWidth = 2; rr(x, GROUND - h, w, h, 6); ctx.stroke();
        ctx.strokeStyle = "rgba(255,255,255,.9)"; ctx.lineWidth = 3; ctx.beginPath(); ctx.moveTo(x + 9, GROUND - h + 14); ctx.lineTo(x + 20, GROUND - h + 6); ctx.moveTo(x + 9, GROUND - h + 28); ctx.lineTo(x + 14, GROUND - h + 22); ctx.stroke();
      },
      column: function (x, w, h) {
        ctx.fillStyle = "#c9c1dc"; ctx.fillRect(x + 6, GROUND - h + 10, w - 12, h - 18);
        ctx.fillStyle = "#e4def0"; ctx.fillRect(x, GROUND - h, w, 10); ctx.fillRect(x - 2, GROUND - 8, w + 4, 8);
        ctx.strokeStyle = "rgba(60,50,100,.25)"; ctx.lineWidth = 2;
        for (var k = 14; k < w - 8; k += 9) { ctx.beginPath(); ctx.moveTo(x + k, GROUND - h + 12); ctx.lineTo(x + k, GROUND - 10); ctx.stroke(); }
      },
      gate: function (x, w, h) {
        ctx.fillStyle = "#59606c"; ctx.fillRect(x - 4, GROUND - h - 6, 10, h + 6); ctx.fillRect(x + w - 6, GROUND - h - 6, 10, h + 6); ctx.fillRect(x - 4, GROUND - h - 6, w + 8, 10);
        ctx.fillStyle = "#2f343c";
        for (var k = 10; k < w - 6; k += 8) ctx.fillRect(x + k, GROUND - h + 4, 3, h - 4);
        ctx.fillRect(x + 6, GROUND - h * 0.5, w - 12, 4);
      },
      wall: function (x, w, h) {
        ctx.fillStyle = "#b8604a"; ctx.fillRect(x, GROUND - h, w, h);
        ctx.strokeStyle = "#7d3a2c"; ctx.lineWidth = 2;
        for (var r = 0; r * 18 < h; r++) {
          var y = GROUND - h + r * 18;
          ctx.beginPath(); ctx.moveTo(x, y); ctx.lineTo(x + w, y); ctx.stroke();
          for (var c = (r % 2) * 15 + 15; c < w; c += 30) { ctx.beginPath(); ctx.moveTo(x + c, y); ctx.lineTo(x + c, y + 18); ctx.stroke(); }
        }
        ctx.strokeRect(x + 1, GROUND - h + 1, w - 2, h - 2);
      },
      cannon: function (x, w, h) {
        ctx.fillStyle = "#2f343c"; ctx.save(); ctx.translate(x + w * 0.45, GROUND - 28); ctx.rotate(-0.2);
        rr(-w * 0.4, -12, w * 0.9, 24, 10); ctx.fill(); ctx.restore();
        ctx.fillStyle = "#6b4a2b"; rr(x + 4, GROUND - 30, w * 0.7, 14, 3); ctx.fill();
        circle(x + w * 0.3, GROUND - 14, 14, "#4a3320"); circle(x + w * 0.3, GROUND - 14, 5, "#9a7a52");
      },
      buoy: function (x, w, h) {
        ctx.fillStyle = "#e84f4f"; rr(x + 4, GROUND - h, w - 8, h, 14); ctx.fill();
        ctx.fillStyle = "#ffffff"; ctx.fillRect(x + 4, GROUND - h * 0.65, w - 8, 9); ctx.fillRect(x + 4, GROUND - h * 0.3, w - 8, 9);
        ctx.fillStyle = "#2b3a4a"; ctx.fillRect(x + w / 2 - 1.5, GROUND - h - 10, 3, 10);
      }
    };

    function questionBlock(cx, y, state, t) {
      // a floating block above each obstacle: ? until cleared, a tick once cleared, a cross if it won
      var s = 30;
      var col = state === "ok" ? "#46b873" : state === "bad" ? "#d85a6e" : "#ffc83d";
      var edge = state === "ok" ? "#1f7a46" : state === "bad" ? "#8f2a3d" : "#b9801a";
      ctx.fillStyle = col; rr(cx - s / 2, y - s / 2, s, s, 5); ctx.fill();
      ctx.strokeStyle = edge; ctx.lineWidth = 2.5; rr(cx - s / 2, y - s / 2, s, s, 5); ctx.stroke();
      ctx.strokeStyle = "#ffffff"; ctx.lineWidth = 3.4; ctx.lineCap = "round"; ctx.lineJoin = "round";
      ctx.beginPath();
      if (state === "ok") { ctx.moveTo(cx - 7, y + 1); ctx.lineTo(cx - 2, y + 7); ctx.lineTo(cx + 8, y - 6); }
      else if (state === "bad") { ctx.moveTo(cx - 6, y - 6); ctx.lineTo(cx + 6, y + 6); ctx.moveTo(cx + 6, y - 6); ctx.lineTo(cx - 6, y + 6); }
      else {
        ctx.moveTo(cx - 5, y - 4); ctx.bezierCurveTo(cx - 5, y - 11, cx + 6, y - 11, cx + 5, y - 4);
        ctx.bezierCurveTo(cx + 4.5, y, cx, y, cx, y + 3.5);
        ctx.moveTo(cx, y + 8); ctx.lineTo(cx, y + 8.2);
      }
      ctx.stroke();
      ctx.lineCap = "butt";
    }

    function flag(sx, t, pal) {
      ctx.fillStyle = "#e8e6ee"; ctx.fillRect(sx - 2, GROUND - 128, 5, 128);
      circle(sx + 0.5, GROUND - 130, 5, "#ffd23d");
      ctx.beginPath(); ctx.moveTo(sx + 3, GROUND - 124);
      for (var k = 0; k <= 8; k++) ctx.lineTo(sx + 3 + k * 6, GROUND - 124 + Math.sin(t * 5 + k * 0.7) * 3);
      for (var j = 8; j >= 0; j--) ctx.lineTo(sx + 3 + j * 6, GROUND - 98 + Math.sin(t * 5 + j * 0.7) * 3);
      ctx.closePath(); ctx.fillStyle = "#e8465f"; ctx.fill();
      ctx.fillStyle = "rgba(255,255,255,.9)";
      ctx.fillRect(sx + 15, GROUND - 118, 8, 8); ctx.fillRect(sx + 31, GROUND - 118, 8, 8); ctx.fillRect(sx + 23, GROUND - 108, 8, 8);
      ctx.fillStyle = pal.dirt2; rr(sx - 12, GROUND - 6, 28, 8, 3); ctx.fill();
    }

    function coin(sx, y, t, i) {
      var k = Math.abs(Math.cos(t * 4 + i));
      ctx.fillStyle = "#ffcb3a"; ctx.beginPath(); ctx.ellipse(sx, y, 8 * Math.max(0.25, k), 8, 0, 0, 6.2832); ctx.fill();
      ctx.strokeStyle = "#c98e12"; ctx.lineWidth = 1.6; ctx.beginPath(); ctx.ellipse(sx, y, 8 * Math.max(0.25, k), 8, 0, 0, 6.2832); ctx.stroke();
      ctx.fillStyle = "rgba(255,255,255,.55)"; ctx.fillRect(sx - 1, y - 4, 2, 8);
    }

    /* ------------------------------------------------------------ Pixel */
    function pixel(p, t) {
      var x = p.x, base = GROUND - p.h;
      if (p.h > -1 && p.h < 2) {
        ctx.fillStyle = "rgba(0,0,0,.2)";
        ctx.beginPath(); ctx.ellipse(x, GROUND + 3, 24, 5, 0, 0, 6.2832); ctx.fill();
      }
      ctx.save();
      if (p.alpha !== undefined && p.alpha < 1) ctx.globalAlpha = Math.max(0, p.alpha);
      ctx.translate(x, base);
      // paws under the body, alternating while running
      if (p.run) {
        var a = Math.sin(t * 16), b = -a;
        ctx.fillStyle = "#235a63";
        ctx.beginPath(); ctx.ellipse(-9 + a * 6, -3 - Math.max(0, a) * 4, 6, 3.6, 0, 0, 6.2832); ctx.fill();
        ctx.beginPath(); ctx.ellipse(9 + b * 6, -3 - Math.max(0, b) * 4, 6, 3.6, 0, 0, 6.2832); ctx.fill();
      } else if (p.h < 1) {
        ctx.fillStyle = "#235a63";
        ctx.beginPath(); ctx.ellipse(-9, -3, 6, 3.6, 0, 0, 6.2832); ctx.fill();
        ctx.beginPath(); ctx.ellipse(9, -3, 6, 3.6, 0, 0, 6.2832); ctx.fill();
      }
      var bob = p.run ? -Math.abs(Math.sin(t * 8)) * 3 : (p.idle ? Math.sin(t * 2.2) * 1.2 : 0);
      ctx.translate(0, bob - 2);
      ctx.rotate(p.rot || 0);
      ctx.scale(p.sx || 1, p.sy || 1);
      if (spriteImg && spriteImg.complete) {
        ctx.drawImage(spriteImg, -SPRITE / 2, -SPRITE * 0.86, SPRITE, SPRITE);
      } else {
        circle(0, -26, 24, "#02848B");
      }
      if (p.dizzy) {
        for (var k = 0; k < 3; k++) {
          var ang = t * 6 + k * 2.1;
          drawStar(Math.cos(ang) * 26, -SPRITE * 0.78 + Math.sin(ang) * 6, 5, "#ffd23d");
        }
      }
      ctx.restore();
    }

    function drawStar(x, y, r, fill) {
      ctx.beginPath();
      for (var k = 0; k < 10; k++) {
        var rad = k % 2 ? r * 0.45 : r, a = -1.5708 + k * 0.62832;
        ctx.lineTo(x + Math.cos(a) * rad, y + Math.sin(a) * rad);
      }
      ctx.closePath(); ctx.fillStyle = fill; ctx.fill();
    }

    function bubble(sx, y) {
      ctx.fillStyle = "#ffffff"; rr(sx - 26, y - 34, 52, 28, 9); ctx.fill();
      ctx.strokeStyle = "#2e2545"; ctx.lineWidth = 2; rr(sx - 26, y - 34, 52, 28, 9); ctx.stroke();
      ctx.fillStyle = "#ffffff"; ctx.beginPath(); ctx.moveTo(sx - 5, y - 7); ctx.lineTo(sx, y + 1); ctx.lineTo(sx + 5, y - 7); ctx.closePath(); ctx.fill();
      ctx.strokeStyle = "#2e2545"; ctx.beginPath(); ctx.moveTo(sx - 5, y - 6); ctx.lineTo(sx, y + 1); ctx.lineTo(sx + 5, y - 6); ctx.stroke();
      ctx.fillStyle = "#2e2545"; ctx.font = "700 15px ui-monospace, Menlo, Consolas, monospace"; ctx.textAlign = "center"; ctx.textBaseline = "middle";
      ctx.fillText("f( )", sx, y - 20);
    }

    /* -------------------------------------------------------- the frame */
    function draw(s) {
      fit();
      ctx.setTransform(scale, 0, 0, scale, 0, 0);
      var pal = PAL[s.palette] || PAL.meadow, t = s.t, cam = s.cam;
      sky(pal, s.palette);

      // sun or moon, and stars at night
      if (pal.night) {
        ctx.fillStyle = "rgba(255,255,255,.85)";
        var rs = seeded(11);
        for (var q = 0; q < 46; q++) { var qx = rs() * W, qy = rs() * 170, tw = 0.6 + 0.4 * Math.sin(t * 2 + q); ctx.globalAlpha = 0.35 + 0.5 * tw; ctx.fillRect(qx, qy, 1.8, 1.8); }
        ctx.globalAlpha = 1;
        circle(520, 70, 26, pal.sun); circle(530, 64, 22, "#3c3470");
      } else {
        circle(500, 66, 34, "rgba(255,255,255,.28)"); circle(500, 66, 24, pal.sun);
      }

      clouds(cam, t, pal);
      ridge(214, 40, 0.0042, 0.0091, 0.12, cam, pal.far, 0.6);
      ridge(246, 30, 0.0061, 0.0127, 0.28, cam, pal.mid, 2.2);

      var kind = pal.deco, mc = MIDCOL[kind];
      tiles(kind === "walls" || kind === "turrets" ? 190 : kind === "dunes" || kind === "peaks" ? 230 : 120, 0.42, cam, function (x, i, r) {
        if (r() < 0.25) return;
        MID[kind](x, GROUND - 2, r, mc);
      }, 120);

      ground(pal, cam, s.pits);

      // near details sit on the path itself, in world coordinates
      var near = pal.near;
      tiles(64, 1, cam, function (x, i, r) {
        if (r() < 0.45) return;
        NEAR[near](x + r() * 30, GROUND + 1, r, t, pal.night);
      }, 30);

      // obstacles
      for (var i = 0; i < s.obstacles.length; i++) {
        var o = s.obstacles[i], sx = o.x - cam, def = OB[o.kind];
        if (sx > W + 60 || sx + def.w < -60) continue;
        if (o.kind !== "gap" && o.kind !== "lava") DRAW_OB[o.kind](sx, def.w, def.h);
        var by = GROUND - def.h - 84 + (s.calm ? 0 : Math.sin(t * 3 + i) * 3);
        questionBlock(sx + def.w / 2, def.h ? by : GROUND - 112 + (s.calm ? 0 : Math.sin(t * 3 + i) * 3), o.state, t);
      }

      flag(s.flagX - cam, t, pal);

      for (var c = 0; c < s.coins.length; c++) {
        var cn = s.coins[c];
        if (cn.got) continue;
        var cx = cn.x - cam;
        if (cx > -20 && cx < W + 20) coin(cx, GROUND - cn.y, t, c);
      }

      // particles, behind Pixel for dust and in front for sparkle
      for (var k = 0; k < s.particles.length; k++) {
        var pt = s.particles[k], a = 1 - pt.age / pt.life, px = pt.x - cam;
        ctx.globalAlpha = Math.max(0, a);
        if (pt.kind === "dust") circle(px, pt.y, pt.size * (1 + (1 - a)), "rgba(255,255,255,.7)");
        else if (pt.kind === "star") drawStar(px, pt.y, pt.size, pt.color);
        else { ctx.fillStyle = pt.color; ctx.fillRect(px, pt.y, pt.size, pt.size * 0.6); }
        ctx.globalAlpha = 1;
      }

      var p = s.pixel;
      pixel({ x: p.x - cam, h: p.h, rot: p.rot, sx: p.sx, sy: p.sy, run: p.run, idle: p.idle, dizzy: p.dizzy, alpha: p.alpha }, t);
      if (s.bubble) bubble(p.x - cam + 8, GROUND - p.h - SPRITE * 0.86 - 4);

      if (s.fade > 0) {
        ctx.fillStyle = "rgba(255,255,255," + Math.min(1, s.fade) + ")";
        ctx.fillRect(0, 0, W, H);
      }
    }

    fit();
    return { draw: draw, fit: fit, W: W, H: H, GROUND: GROUND, OB: OB, PAL: PAL };
  }

  window.PixelArt = { make: make, OB: OB, PAL: PAL, W: W, H: H, GROUND: GROUND };
})();
