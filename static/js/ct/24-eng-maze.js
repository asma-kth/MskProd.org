/* Engine: maze. Rescue Pixel by solving one sub-problem at a time.
 *
 * First the student plans: which sub-goals, in which order (decoys included).
 * Then the student carries the plan out, steering through the maze with the
 * arrow keys, the on-screen pad or a swipe, while the plan ticks itself off.
 *
 * data: { grid: [rows], cards: [{id, text, icon, goal, why}], plan: [ids], orderWhy }
 *   grid: # wall, . floor, S start, K key, G locked gate, C Pixel, E exit, o coin
 * answer (for the check): [card ids in the plan]
 */
(function (root) {
  "use strict";
  var CT = root.CT = root.CT || {};

  CT.check.maze = function (d, plan) {
    plan = plan || [];
    var decoy = plan.map(function (id) { return CT.byId(d.cards, id); }).filter(function (c) { return c && !c.goal; })[0];
    if (decoy) return { ok: false, wrong: [decoy.id], msg: decoy.why };
    if (plan.filter(Boolean).length < d.plan.length) return { ok: false, incomplete: true, msg: "Your plan needs " + d.plan.length + " steps." };
    for (var i = 0; i < d.plan.length; i++) if (plan[i] !== d.plan[i]) return { ok: false, wrong: [plan[i]], msg: d.orderWhy };
    return { ok: true };
  };
  CT.solve.maze = function (d) { return d.plan.slice(); };

  // The walk that carries out the plan, square by square: used by Show me and the tests.
  CT.mazeWalk = function (d) {
    var map = CT.grid.parse(d.grid), pos = map.one("S"), path = [pos], hasKey = false;
    var targets = { K: map.one("K"), G: map.one("G"), C: map.one("C"), E: map.one("E") };
    for (var i = 0; i < d.plan.length; i++) {
      var c = CT.byId(d.cards, d.plan[i]), tgt = targets[c.goal];
      var p = CT.grid.bfs(map, pos, tgt, function (x, y) {
        var ch = map.at(x, y);
        return ch !== "#" && (ch !== "G" || hasKey);
      });
      if (!p) return null;
      path = path.concat(p.slice(1));
      pos = tgt;
      if (c.goal === "K") hasKey = true;
    }
    return path;
  };

  CT.engines.maze = {
    mount: function (host, level, api) {
      var d = level.data, map = CT.grid.parse(d.grid);
      var phase = "plan", plan = d.plan.map(function () { return null; }), wrong = {};
      var cardOrder = CT.shuffle(d.cards.map(function (c) { return c.id; }), api.rng);
      var board = CT.el("div", { class: "cmz" });
      host.appendChild(board);
      var game = null;

      function legend() {
        return { K: { sticker: "key" }, G: { tile: "cg-gate", sticker: "lock" }, E: { tile: "cg-exit", sticker: "door" }, o: { sticker: "coin" } };
      }

      function renderPlan() {
        CT.clear(board);
        var left = CT.el("div", { class: "cmz-map" });
        CT.grid.view(left, map, { legend: legend(), label: "The maze: Pixel is trapped. The key, the locked gate and the exit are marked." });
        var pv = left.querySelector("svg");
        addPixel(pv, map.one("C"));
        addRescuer(pv, map.one("S"));
        var right = CT.el("div", { class: "cmz-plan" });
        right.appendChild(CT.el("p", { class: "ct-tray-h" }, "Your rescue plan: one sub-problem per step"));
        var ol = CT.el("ol", { class: "cmz-slots" });
        plan.forEach(function (id, i) {
          var li = CT.el("li", { class: "cmz-slot", "data-zone": "slot-" + i, "data-zone-label": "plan step " + (i + 1) }, [CT.el("span", { class: "cas-num" }, String(i + 1))]);
          if (id) { var c = CT.card(CT.byId(d.cards, id)); if (wrong[id]) c.classList.add("is-wrong"); li.appendChild(c); }
          else li.appendChild(CT.el("span", { class: "ctr-empty" }, "Step " + (i + 1)));
          li.appendChild(CT.el("button", { type: "button", class: "ct-drop", "aria-label": "Put the picked card at step " + (i + 1) }, "Put here"));
          ol.appendChild(li);
        });
        right.appendChild(ol);
        var tray = CT.el("div", { class: "ct-tray", "data-zone": "tray", "data-zone-label": "the idea pile" }, [CT.el("p", { class: "ct-tray-h" }, "Ideas (not all are needed)")]);
        cardOrder.filter(function (id) { return plan.indexOf(id) < 0; }).forEach(function (id) {
          var c = CT.card(CT.byId(d.cards, id)); if (wrong[id]) c.classList.add("is-wrong"); tray.appendChild(c);
        });
        right.appendChild(tray);
        CT.append(board, [CT.el("div", { class: "cmz-wrap" }, [left, right])]);
      }
      function addPixel(svgEl, at) {
        if (!at) return;
        var px = new CT.Pixel({ mood: "think" });
        var g = CT.svg("g", { class: "cg-piece cmz-cat", "data-piece": "cat" });
        px.svg.setAttribute("x", 1); px.svg.setAttribute("y", -2); px.svg.setAttribute("width", 38); px.svg.setAttribute("height", 40);
        g.appendChild(px.svg);
        svgEl.querySelector(".cg-pieces").appendChild(g);
        g.style.transform = "translate(" + at[0] * 40 + "px," + at[1] * 40 + "px)";
        return px;
      }
      function addRescuer(svgEl, at) {
        var g = CT.svg("g", { class: "cg-piece", "data-piece": "hero" }, [CT.icoSvg("robot", 4, 4, 32)]);
        svgEl.querySelector(".cg-pieces").appendChild(g);
        g.style.transform = "translate(" + at[0] * 40 + "px," + at[1] * 40 + "px)";
      }

      // ------------------------------------------------------------ play
      function startPlay() {
        phase = "play";
        CT.clear(board);
        game = { pos: map.one("S").slice(), hasKey: false, gate: false, cat: false, done: false, step: 0, moves: 0, catPos: map.one("C").slice() };
        var left = CT.el("div", { class: "cmz-map", tabindex: "0", "aria-label": "The maze. Use the arrow keys to move the rescue robot." });
        var view = CT.grid.view(left, map, { legend: legend(), label: "The maze" });
        game.view = view;
        var px = addPixel(view.svg, map.one("C"));
        game.px = px;
        addRescuer(view.svg, game.pos);
        var list = CT.el("ol", { class: "cmz-check" });
        d.plan.forEach(function (id, i) {
          var c = CT.byId(d.cards, id);
          list.appendChild(CT.el("li", { class: i === 0 ? "is-now" : "" }, [CT.el("span", { class: "cmz-tick", "aria-hidden": "true" }), " ", CT.ico(c.icon), " ", c.text]));
        });
        game.list = list;
        var right = CT.el("div", { class: "cmz-plan" }, [CT.el("p", { class: "ct-tray-h" }, "Carry out your plan"), list,
          CT.grid.pad(move)]);
        CT.append(board, [CT.el("div", { class: "cmz-wrap" }, [left, right])]);
        CT.grid.controls(left, move);
        left.focus({ preventScroll: true });
        api.say("Plan approved! Now steer me through it, one sub-goal at a time.", "happy", 2400);
      }
      function tick(i) {
        var li = game.list.children[i];
        if (!li) return;
        li.className = "is-done"; li.querySelector(".cmz-tick").appendChild(CT.ui("check"));
        if (game.list.children[i + 1]) game.list.children[i + 1].className = "is-now";
        game.step = i + 1;
        CT.sound.play("good");
        CT.announce("Sub-goal " + (i + 1) + " done: " + CT.byId(d.cards, d.plan[i]).text + ".");
      }
      function goalIndex(g) { for (var i = 0; i < d.plan.length; i++) if (CT.byId(d.cards, d.plan[i]).goal === g) return i; return -1; }
      function move(dir) {
        if (!game || game.done) return;
        var nx = game.pos[0] + CT.grid.DIRS[dir][0], ny = game.pos[1] + CT.grid.DIRS[dir][1], ch = map.at(nx, ny);
        if (ch === "#") { game.view.bump("hero"); CT.sound.play("bad"); return; }
        if (ch === "G" && !game.hasKey) { game.view.bump("hero"); api.say("Locked! The key comes first: that's sub-goal 1.", "think", 2200); CT.sound.play("bad"); return; }
        var prev = game.pos.slice();
        game.pos = [nx, ny]; game.moves++;
        game.view.move("hero", nx, ny);
        CT.sound.play("step");
        if (game.cat) { game.catPos = prev; game.view.svg.querySelector('[data-piece="cat"]').style.transform = "translate(" + prev[0] * 40 + "px," + prev[1] * 40 + "px)"; }
        if (ch === "K" && !game.hasKey) { game.hasKey = true; game.view.removeSticker(nx, ny); tick(goalIndex("K")); }
        if (ch === "G" && !game.gate) { game.gate = true; game.view.removeSticker(nx, ny); game.view.setTile(nx, ny, "cg-open"); tick(goalIndex("G")); }
        if (ch === "C" && !game.cat) { game.cat = true; game.px.mood("happy"); tick(goalIndex("C")); api.say("You found me! I'll follow you out.", "happy", 2400); }
        if (ch === "o") game.view.removeSticker(nx, ny);
        if (ch === "E") {
          if (!game.cat) { api.say("Not without Pixel! Rescue the cat first.", "think", 2200); return; }
          game.done = true; tick(goalIndex("E"));
          setTimeout(function () { if (api.alive()) api.result({ ok: true }); }, CT.calm() ? 50 : 600);
        }
      }
      function autoWalk() {
        if (game.walking) return;
        var path = CT.mazeWalk(d), i = 1;
        if (!path) return;
        // Show me walks the whole plan from the start, wherever the robot has got to.
        startPlay();
        game.walking = true;
        api.busy(true);
        var mine = game;
        (function step() {
          if (!api.alive() || mine !== game) return;
          if (i >= path.length || game.done) { api.busy(false); game.walking = false; return; }
          move(CT.grid.dirBetween(game.pos, path[i])); i++;
          CT.wait(220, step);
        })();
      }

      var dd = CT.dnd(board, {
        canDrop: function () { return phase === "plan"; },
        onMove: function (id, zone) {
          wrong = {};
          var from = plan.indexOf(id);
          if (zone === "tray") { if (from >= 0) plan[from] = null; }
          else { var to = Number(zone.slice(5)), there = plan[to]; if (from >= 0) plan[from] = there; plan[to] = id; }
          renderPlan();
        }
      });
      renderPlan();
      return {
        checkLabel: "Check my plan",
        check: function () {
          if (phase === "play") return { ok: false, incomplete: true, msg: "Steer the robot to complete step " + (game.step + 1) + " of your plan." };
          var r = CT.check.maze(d, plan);
          if (r.ok) {
            setTimeout(startPlay, CT.calm() ? 50 : 900);
            return { ok: true, more: true, msg: "Plan approved! Now carry it out.", toast: "Plan approved!" };
          }
          return r;
        },
        mark: function (r) { wrong = {}; (r.wrong || []).forEach(function (id) { wrong[id] = true; }); if (phase === "plan") renderPlan(); },
        reset: function () { if (phase === "plan") { plan = d.plan.map(function () { return null; }); wrong = {}; renderPlan(); } else startPlay(); },
        showMe: function () { if (phase === "plan") { plan = d.plan.slice(); wrong = {}; renderPlan(); } else autoWalk(); },
        scaffold: function () {
          if (phase !== "plan") { api.say("Next: " + CT.byId(d.cards, d.plan[game.step]).text + ".", "think"); return; }
          for (var i = 0; i < d.plan.length; i++) if (plan[i] !== d.plan[i]) {
            var prev = plan.indexOf(d.plan[i]); if (prev >= 0) plan[prev] = null;
            plan[i] = d.plan[i]; renderPlan(); return;
          }
        },
        demo: function (done) {
          var id = d.plan[0], from = board.querySelector('.ct-tray [data-item="' + id + '"]'), to = board.querySelector('[data-zone="slot-0"]');
          CT.ghost(from, to, function () { plan[0] = id; renderPlan(); done(); });
        },
        destroy: function () { dd.destroy(); }
      };
    }
  };
})(typeof window !== "undefined" ? window : globalThis);
