/* Engine: program. Move a character round a grid with a program of commands.
 *
 * data: { mode: "absolute"|"relative",
 *         rounds: [{kind: "drive"|"plan", grid: [rows], dir, max, say, answer: program}] }
 * Grid: # hedge or wall, ~ pond, S start, H home, B battery, F fish and * star to collect.
 * Absolute programs use up, down, left and right; relative ones use F (forward),
 * L and R (turn on the spot) and {repeat: n, do: [...]}. In a drive round the
 * student steers with the arrows and the moves become the program; in a plan
 * round they build the whole program first and then run it.
 * answer: [program per round]
 */
(function (root) {
  "use strict";
  var CT = root.CT = root.CT || {};
  var DIR = { up: [0, -1], right: [1, 0], down: [0, 1], left: [-1, 0] };
  var LABEL = { up: "Up", down: "Down", left: "Left", right: "Right", F: "Forward", L: "Turn left", R: "Turn right" };
  var ICON = { up: "⬆️", down: "⬇️", left: "⬅️", right: "➡️", F: "⬆️", L: "↩️", R: "↪️" };

  function flat(prog) {
    var out = [];
    (prog || []).forEach(function (c) {
      if (typeof c === "string") out.push(c);
      else for (var k = 0; k < c.repeat; k++) out = out.concat(flat(c.do));
    });
    return out;
  }
  function blocks(prog) {
    return (prog || []).reduce(function (n, c) { return n + (typeof c === "string" ? 1 : 1 + blocks(c.do)); }, 0);
  }
  CT.progFlat = flat;
  CT.progBlocks = blocks;

  // Carry out a program; every step is kept so it can be animated.
  function simulate(mode, rd, prog) {
    var map = CT.grid.parse(rd.grid), s = map.one("S"), pos = [s[0], s[1]], dir = rd.dir || "right";
    var need = {}, got = {}, steps = [], cmds = flat(prog);
    map.find("*").concat(map.find("F")).forEach(function (p) { need[p[0] + "," + p[1]] = map.at(p[0], p[1]); });
    var home = map.one("H") || map.one("B");
    for (var i = 0; i < cmds.length && i < 400; i++) {
      var c = cmds[i];
      if (c === "L") dir = CT.grid.TURN_L[dir];
      else if (c === "R") dir = CT.grid.TURN_R[dir];
      else {
        var d = mode === "absolute" ? c : dir;
        if (mode === "absolute") dir = c;
        var n = [pos[0] + DIR[d][0], pos[1] + DIR[d][1]], ch = map.at(n[0], n[1]);
        if (ch === "#" || ch === "~") {
          steps.push({ pos: pos.slice(), dir: dir, i: i, bump: true });
          return { ok: false, crash: i, steps: steps, msg: (ch === "~" ? "Splash! Move " + (i + 1) + " walks into the pond." : "Bump! Move " + (i + 1) + " walks into a wall.") +
            " The program stops there." };
        }
        pos = n;
        var key = pos[0] + "," + pos[1];
        if (need[key]) got[key] = true;
      }
      steps.push({ pos: pos.slice(), dir: dir, i: i, got: Object.assign({}, got) });
    }
    var missing = Object.keys(need).filter(function (k) { return !got[k]; });
    if (missing.length) {
      var fish = missing.some(function (k) { return need[k] === "F"; });
      return { ok: false, steps: steps, msg: fish ? "The program never reaches the fish." : missing.length + " star" + (missing.length > 1 ? "s are" : " is") + " still to collect." };
    }
    if (home && (pos[0] !== home[0] || pos[1] !== home[1])) return { ok: false, steps: steps, msg: "The program ends before reaching " + (map.at(home[0], home[1]) === "H" ? "home" : "the battery") + ". Add the missing moves." };
    if (rd.end && (pos[0] !== rd.end[0] || pos[1] !== rd.end[1])) return { ok: false, steps: steps, msg: "The robot must finish back where it started." };
    return { ok: true, steps: steps };
  }

  function checkRound(d, rd, prog) {
    prog = prog || [];
    if (!blocks(prog)) return { ok: false, incomplete: true, msg: rd.kind === "drive" ? "Steer with the arrows to drive home." : "Build a program first: pick commands from the list." };
    if (rd.max && blocks(prog) > rd.max) return { ok: false, msg: "Your program uses " + blocks(prog) + " blocks, but the limit is " + rd.max + ". Can a repeat block or a shorter route help?" };
    var r = simulate(d.mode, rd, prog);
    return r.ok ? { ok: true } : { ok: false, crash: r.crash, msg: r.msg };
  }
  CT.check.program = function (d, a) {
    a = a || [];
    for (var i = 0; i < d.rounds.length; i++) {
      var r = checkRound(d, d.rounds[i], a[i]);
      if (!r.ok) return Object.assign(r, { round: i });
    }
    return { ok: true };
  };
  CT.solve.program = function (d) { return d.rounds.map(function (rd) { return JSON.parse(JSON.stringify(rd.answer)); }); };
  CT.progSimulate = simulate;

  // A little robot that points the way it faces (drawn facing up).
  function botShape() {
    var g = CT.svg("g", { class: "cpg-bot" });
    g.innerHTML = '<rect x="7" y="9" width="26" height="24" rx="7" class="cpg-bot-body"/><circle cx="15" cy="20" r="3.5" fill="#fff"/><circle cx="25" cy="20" r="3.5" fill="#fff"/>' +
      '<circle cx="15" cy="20" r="1.6" fill="#0F172A"/><circle cx="25" cy="20" r="1.6" fill="#0F172A"/><path d="M20 1 L27 9 H13 Z" class="cpg-bot-nose"/>';
    return g;
  }

  CT.engines.program = {
    mount: function (host, level, api) {
      var d = level.data, rel = d.mode === "relative", ri = 0, rd, prog = [], into = null, view, map, pos, dir, running = false, wrongAt = -1, run = null;
      var board = CT.el("div", { class: "cpg" });
      host.appendChild(board);
      var mapBox = CT.el("div", { class: "cpg-map" }), side = CT.el("div", { class: "cpg-side" });

      function start(i) {
        ri = i; rd = d.rounds[ri]; prog = []; into = null; wrongAt = -1; running = false;
        map = CT.grid.parse(rd.grid);
        var s = map.one("S"); pos = [s[0], s[1]]; dir = rd.dir || "right";
        CT.clear(board);
        CT.append(board, [CT.roundChip(ri, d.rounds.length), CT.el("div", { class: "cpg-wrap" }, [mapBox, side])]);
        drawMap();
        render();
        api.say(rd.say, "think", 3200);
      }
      function drawMap() {
        CT.clear(mapBox);
        view = CT.grid.view(mapBox, map, { label: "The map", legend: {
          H: { sticker: "🏠", tile: "cg-exit" }, B: { sticker: "🔋", tile: "cg-exit" }, F: { sticker: "🐟" }, "*": { sticker: "⭐" }, "~": { sticker: "💧", tile: "cg-pond" } } });
        view.svg.setAttribute("tabindex", "0");
        if (rel) view.piece("me", pos[0], pos[1], botShape(), "is-turn");
        else view.piece("me", pos[0], pos[1], "🐱");
        view.move("me", pos[0], pos[1], dir, true);
        if (rd.kind === "drive") CT.grid.controls(view.svg, drive);
      }
      function place(p, dname, instant) { pos = p.slice(); dir = dname; view.move("me", pos[0], pos[1], dir, instant); }
      function resetPiece() {
        var s = map.one("S");
        // put back anything collected
        drawMap();
        place([s[0], s[1]], rd.dir || "right", true);
      }

      function chip(c, k, inner, parentIdx) {
        var label = typeof c === "string" ? LABEL[c] : "repeat";
        var bad = wrongAt === k && !inner;
        return CT.el("li", { class: "cpg-blk" + (bad ? " is-bad" : "") + (typeof c !== "string" && into === k ? " is-into" : "") }, typeof c === "string" ? [
          CT.el("span", { class: "cpg-ico", "aria-hidden": "true" }, ICON[c]), CT.el("span", null, label),
          rd.kind === "drive" ? null : CT.el("button", { type: "button", class: "cpg-x", "aria-label": "Remove " + label, onclick: function () { remove(k, parentIdx); } }, "✕")
        ] : [
          CT.el("div", { class: "cpg-rep" }, [
            CT.el("button", { type: "button", class: "cpg-rep-h", "aria-pressed": into === k ? "true" : "false", onclick: function () { into = into === k ? null : k; render(); } },
              ["🔁 repeat ", CT.el("b", null, String(c.repeat)), " times", into === k ? " (adding inside)" : ""]),
            CT.el("button", { type: "button", class: "cdz-step", "aria-label": "Fewer repeats", onclick: function () { c.repeat = Math.max(2, c.repeat - 1); render(); } }, "−"),
            CT.el("button", { type: "button", class: "cdz-step", "aria-label": "More repeats", onclick: function () { c.repeat = Math.min(9, c.repeat + 1); render(); } }, "+"),
            CT.el("button", { type: "button", class: "cpg-x", "aria-label": "Remove the repeat block", onclick: function () { remove(k, null); } }, "✕")
          ]),
          CT.el("ol", { class: "cpg-inner" }, c.do.length ? c.do.map(function (x, j) { return chip(x, j, true, k); }) :
            [CT.el("li", { class: "cpg-empty" }, "Empty: choose this loop, then add commands")])
        ]);
      }
      function remove(k, parentIdx) {
        if (running) return;
        if (parentIdx !== null && parentIdx !== undefined) prog[parentIdx].do.splice(k, 1);
        else { prog.splice(k, 1); if (into === k) into = null; else if (into !== null && into > k) into--; }
        wrongAt = -1; render();
      }
      function add(c) {
        if (running) return;
        if (into !== null && prog[into] && typeof c === "string") prog[into].do.push(c);
        else if (c === "repeat") { prog.push({ repeat: 2, do: [] }); into = prog.length - 1; }
        else prog.push(c);
        wrongAt = -1; CT.sound.play("drop"); render();
      }

      function render() {
        CT.clear(side);
        var n = blocks(prog);
        var head = CT.el("div", { class: "cpg-head" }, [
          CT.el("button", { type: "button", class: "cpg-main" + (into === null ? " is-into" : ""), onclick: function () { into = null; render(); } }, "📜 Your program"),
          CT.el("span", { class: "cpg-count" + (rd.max && n > rd.max ? " is-over" : "") }, n + (rd.max ? " / " + rd.max : "") + " blocks")]);
        var list = CT.el("ol", { class: "cpg-list", "aria-label": "Your program" }, prog.length ? prog.map(function (c, k) { return chip(c, k, false, null); }) :
          [CT.el("li", { class: "cpg-empty" }, rd.kind === "drive" ? "Your moves will appear here." : "Empty. Add commands below.")]);
        var palette;
        if (rd.kind === "drive") palette = CT.el("div", { class: "cpg-pad" }, [CT.el("p", { class: "ct-tray-h" }, "Steer Pixel"), CT.grid.pad(drive)]);
        else {
          palette = CT.el("div", { class: "cpg-pal", role: "group", "aria-label": "Commands" }, [CT.el("p", { class: "ct-tray-h" }, into !== null ? "Add to the repeat loop" : "Add a command")]);
          (rel ? ["F", "L", "R"] : ["up", "down", "left", "right"]).forEach(function (c) {
            palette.appendChild(CT.el("button", { type: "button", class: "cdz-move", onclick: function () { add(c); } }, [CT.el("span", { "aria-hidden": "true" }, ICON[c]), LABEL[c]]));
          });
          if (rel) palette.appendChild(CT.el("button", { type: "button", class: "cdz-move", disabled: into !== null ? true : null, onclick: function () { add("repeat"); } }, [CT.el("span", { "aria-hidden": "true" }, "🔁"), "Repeat"]));
        }
        CT.append(side, [head, list, palette]);
      }

      // Drive round: each arrow moves Pixel at once and is added to the program.
      function drive(dname) {
        if (running || rd.kind !== "drive") return;
        var n = [pos[0] + DIR[dname][0], pos[1] + DIR[dname][1]], ch = map.at(n[0], n[1]);
        if (ch === "#" || ch === "~") { view.bump("me"); CT.sound.play("bad"); api.say(ch === "~" ? "Pixel won't walk into the pond!" : "Bump! That way is blocked.", "think", 1400); return; }
        prog.push(dname);
        place(n, dname);
        if (map.at(n[0], n[1]) === "F" || map.at(n[0], n[1]) === "*") view.removeSticker(n[0], n[1]);
        CT.sound.play("step");
        render();
        if (map.at(n[0], n[1]) === "H") CT.wait(350, function () { if (api.alive()) api.result(finish({ ok: true })); });
      }
      function finish(r) {
        if (r.ok && ri < d.rounds.length - 1) return CT.nextRound(api, ri, d.rounds.length, start);
        return r;
      }

      function animate(done) {
        var r = checkRound(d, rd, prog);
        if (r.incomplete || (!r.ok && r.crash === undefined && rd.max && blocks(prog) > rd.max)) { done(r); return; }
        var sim = simulate(d.mode, rd, prog);
        running = true; api.busy(true); wrongAt = -1;
        resetPiece();
        var k = 0, flatList = flat(prog);
        (function step() {
          if (!api.alive()) return;
          if (k >= sim.steps.length) {
            running = false; api.busy(false);
            if (sim.crash !== undefined) wrongAt = topIndex(sim.crash);
            render();
            done(r.ok ? finish(r) : r);
            return;
          }
          var s = sim.steps[k++];
          if (s.bump) { view.bump("me"); CT.sound.play("bad"); }
          else {
            place(s.pos, s.dir);
            var ch = map.at(s.pos[0], s.pos[1]);
            if (ch === "F" || ch === "*") view.removeSticker(s.pos[0], s.pos[1]);
            CT.sound.play(flatList[s.i] === "L" || flatList[s.i] === "R" ? "tap" : "step");
          }
          CT.wait(320, step);
        })();
      }
      // Which top-level block contains the n-th command carried out.
      function topIndex(n) {
        var count = 0;
        for (var k = 0; k < prog.length; k++) {
          var c = prog[k], size = typeof c === "string" ? 1 : c.repeat * flat(c.do).length;
          if (n < count + size) return k;
          count += size;
        }
        return -1;
      }

      start(0);
      return {
        checkLabel: "▶ Run",
        run: function (done) { animate(done); },
        mark: function () { render(); },
        reset: function () { if (!running) start(ri); },
        showMe: function () { prog = JSON.parse(JSON.stringify(rd.answer)); into = null; wrongAt = -1; render(); },
        scaffold: function () {
          var ans = rd.answer, k = 0;
          while (k < prog.length && k < ans.length && JSON.stringify(prog[k]) === JSON.stringify(ans[k])) k++;
          prog = prog.slice(0, k);
          if (k < ans.length) prog.push(typeof ans[k] === "string" ? ans[k] : { repeat: ans[k].repeat, do: ans[k].do.slice(0, 1) });
          into = typeof prog[prog.length - 1] === "object" ? prog.length - 1 : null;
          if (rd.kind === "drive") resetPiece();
          wrongAt = -1; render();
          CT.announce("Pixel added the next command.");
        },
        demo: function (done) {
          prog = flat(rd.answer).slice(0, 3);
          render();
          var sim = simulate(d.mode, rd, prog), k = 0;
          (function step() {
            if (!api.alive()) return;
            if (k >= sim.steps.length) { CT.wait(400, done); return; }
            var s = sim.steps[k++]; place(s.pos, s.dir); CT.sound.play("step");
            CT.wait(450, step);
          })();
        },
        destroy: function () { }
      };
    }
  };
})(typeof window !== "undefined" ? window : globalThis);
