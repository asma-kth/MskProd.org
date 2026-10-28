/* Engine: snakepat. A snake game where the fruit must be eaten in a pattern.
 *
 * data: { w, h, rocks: [[x, y]], fruits: [{id, icon, text}],
 *         rounds: [{eaten: [fruitIds], answer: [fruitIds]}] }
 * The snake's body carries the fruit it has eaten, tail first, so the body
 * shows the pattern. It moves one square per key press, swipe or button, so
 * there is no rush. Eating the right fruit grows the snake; the wrong fruit is
 * spat out and counts as a slip, and three slips restart the round.
 * answer: per round, the fruit eaten in order.
 */
(function (root) {
  "use strict";
  var CT = root.CT = root.CT || {};

  // The smallest repeating part of a list, and the next n items it predicts.
  CT.patternNext = function (list, n) {
    for (var p = 1; p <= list.length; p++) {
      var fits = true;
      for (var i = p; i < list.length; i++) if (list[i] !== list[i - p]) { fits = false; break; }
      if (fits) { var out = []; for (var k = 0; k < n; k++) out.push(list[(list.length + k) % p]); return out; }
    }
    return [];
  };

  CT.check.snakepat = function (d, a) {
    a = a || [];
    for (var i = 0; i < d.rounds.length; i++) {
      var rd = d.rounds[i], got = a[i] || [];
      if (got.length < rd.answer.length) return { ok: false, incomplete: true, round: i, msg: "Eat " + (rd.answer.length - got.length) + " more fruit." };
      for (var k = 0; k < rd.answer.length; k++) if (got[k] !== rd.answer[k]) return { ok: false, round: i, msg: "That fruit breaks the pattern." };
    }
    return { ok: true };
  };
  CT.solve.snakepat = function (d) { return d.rounds.map(function (rd) { return rd.answer.slice(); }); };

  var D = { up: [0, -1], right: [1, 0], down: [0, 1], left: [-1, 0] };
  var BACK = { up: "down", down: "up", left: "right", right: "left" };

  CT.engines.snakepat = {
    mount: function (host, level, api) {
      var d = level.data, S = 40, ri = 0, rd, snake, dir, food, got, slips, rand, walking = false, glow = false;
      var board = CT.el("div", { class: "csn" });
      host.appendChild(board);
      var rock = {};
      d.rocks.forEach(function (r) { rock[r[0] + "," + r[1]] = true; });
      function fruit(id) { return CT.byId(d.fruits, id); }

      function start(i) {
        ri = i; rd = d.rounds[ri]; got = []; slips = 0; glow = false; walking = false;
        rand = CT.rng(level.id + ":" + ri);
        // tail first, head last; every segment but the head carries a fruit
        var y = Math.floor(d.h / 2), n = rd.eaten.length;
        snake = rd.eaten.map(function (f, k) { return { x: k, y: y, f: f }; });
        snake.push({ x: n, y: y, f: null });
        dir = "right";
        food = {};
        d.fruits.forEach(function (f) { food[f.id] = freeCell(); });
        layout();
        render();
        if (i > 0) api.say("New pattern! Read the snake's body from tail to head.", "think", 2600);
      }
      function head() { return snake[snake.length - 1]; }
      function taken(x, y) {
        if (rock[x + "," + y]) return true;
        if (snake.some(function (s) { return s.x === x && s.y === y; })) return true;
        return Object.keys(food).some(function (k) { return food[k] && food[k][0] === x && food[k][1] === y; });
      }
      function freeCell() {
        for (var t = 0; t < 400; t++) {
          var x = Math.floor(rand() * d.w), y = Math.floor(rand() * d.h);
          var h = snake ? head() : null;
          if (!taken(x, y) && (!h || Math.abs(h.x - x) + Math.abs(h.y - y) > 1)) return [x, y];
        }
        return null;
      }
      function want() { return rd.answer[got.length]; }

      // The layout is built once a round, so keyboard focus survives every move.
      var svg, strip, progress, chipEl;
      function layout() {
        CT.clear(board);
        strip = CT.el("ol", { class: "csn-strip", "aria-label": "Fruit eaten so far" });
        svg = CT.svg("svg", { class: "csn-map", viewBox: "0 0 " + d.w * S + " " + d.h * S, role: "img", tabindex: "0" });
        CT.grid.controls(svg, steer);
        progress = CT.el("p", { class: "csn-progress", "aria-live": "polite" });
        CT.append(board, [CT.roundChip(ri, d.rounds.length),
          CT.el("div", { class: "csn-top" }, [CT.el("p", { class: "ct-tray-h" }, "The snake's body, tail to head"), strip]),
          CT.el("div", { class: "csn-wrap" }, [svg, CT.el("div", { class: "csn-side" }, [progress, CT.grid.pad(steer),
            CT.el("p", { class: "csn-tip" }, "Click the board, then use the arrow keys, or swipe.")])])]);
      }
      function render() {
        CT.clear(strip);
        snake.slice(0, -1).forEach(function (s) { strip.appendChild(CT.el("li", null, CT.el("span", { role: "img", "aria-label": fruit(s.f).text }, CT.ico(fruit(s.f).icon)))); });
        strip.appendChild(CT.el("li", { class: "csn-next" }, CT.ico("question")));
        svg.setAttribute("aria-label", "Snake board. The head is at column " + (head().x + 1) + ", row " + (head().y + 1) +
          ". The next fruit in the pattern is somewhere on the board. Use the arrow keys to move.");
        CT.clear(svg);
        for (var y = 0; y < d.h; y++) for (var x = 0; x < d.w; x++) {
          svg.appendChild(CT.svg("rect", { x: x * S + 1, y: y * S + 1, width: S - 2, height: S - 2, rx: 6, class: "csn-cell" + ((x + y) % 2 ? " is-alt" : "") }));
        }
        d.rocks.forEach(function (r) { svg.appendChild(CT.icoSvg("rock", r[0] * S + 5, r[1] * S + 5, S - 10, "csn-ico")); });
        Object.keys(food).forEach(function (k) {
          var p = food[k];
          if (!p) return;
          if (glow && k === want()) svg.appendChild(CT.svg("circle", { cx: p[0] * S + S / 2, cy: p[1] * S + S / 2, r: S / 2 - 1, class: "csn-glow" }));
          svg.appendChild(CT.icoSvg(fruit(k).icon, p[0] * S + 5, p[1] * S + 5, S - 10, "csn-ico"));
        });
        snake.forEach(function (s, i) {
          var isHead = i === snake.length - 1;
          var g = CT.svg("g", { class: "csn-seg" + (isHead ? " is-head" : "") });
          g.appendChild(CT.svg("rect", { x: s.x * S + 3, y: s.y * S + 3, width: S - 6, height: S - 6, rx: isHead ? 14 : 10 }));
          if (isHead) {
            var dx = D[dir][0], dy = D[dir][1], cx = s.x * S + S / 2, cy = s.y * S + S / 2;
            [-1, 1].forEach(function (side) {
              var ex = cx + dx * 6 + (dy ? side * 7 : 0), ey = cy + dy * 6 + (dx ? side * 7 : 0);
              g.appendChild(CT.svg("circle", { cx: ex, cy: ey, r: 4, class: "csn-eye" }));
              g.appendChild(CT.svg("circle", { cx: ex + dx * 1.5, cy: ey + dy * 1.5, r: 2, class: "csn-pupil" }));
            });
          } else g.appendChild(CT.icoSvg(fruit(s.f).icon, s.x * S + S / 4, s.y * S + S / 4, S / 2, "csn-ico csn-small"));
          svg.appendChild(g);
        });
        CT.clear(progress);
        CT.append(progress, [CT.el("b", null, got.length + " of " + rd.answer.length), " eaten in the pattern", slips ? " · slips: " + slips + " of 3" : ""]);
      }

      function steer(dname) {
        if (walking) return;
        stepTo(dname);
      }
      function stepTo(dname) {
        if (dname === BACK[dir] && snake.length > 1) { api.say("The snake can't turn back on itself.", "think", 1600); return false; }
        var h = head(), nx = h.x + D[dname][0], ny = h.y + D[dname][1];
        dir = dname;
        if (nx < 0 || ny < 0 || nx >= d.w || ny >= d.h || rock[nx + "," + ny] ||
            snake.slice(1).some(function (s) { return s.x === nx && s.y === ny; })) {
          CT.sound.play("bad");
          api.say(rock[nx + "," + ny] ? "Bonk! A rock." : "Bonk! Try another way.", "think", 1400);
          render();
          return false;
        }
        var eat = Object.keys(food).filter(function (k) { return food[k] && food[k][0] === nx && food[k][1] === ny; })[0];
        if (eat && eat !== want()) {
          // spat out: the fruit hops away and the snake stays put
          slips++;
          food[eat] = null; food[eat] = freeCell();
          render();
          if (slips >= 3) {
            api.result({ ok: false, msg: "The pattern broke three times, so this round starts again. Read the body from tail to head first." });
            CT.wait(900, function () { if (api.alive()) start(ri); });
          } else api.result({ ok: false, msg: "Yuck! A " + fruit(eat).text + " breaks the pattern. Which fruit comes next?" });
          return false;
        }
        if (eat) {
          var old = head();
          snake.splice(snake.length - 1, 0, { x: old.x, y: old.y, f: eat });
          old.x = nx; old.y = ny;
          got.push(eat);
          glow = false;
          food[eat] = null; food[eat] = freeCell();
          CT.sound.play("good");
          render();
          if (got.length >= rd.answer.length) {
            var r = { ok: true };
            CT.wait(300, function () { if (api.alive()) api.result(ri < d.rounds.length - 1 ? CT.nextRound(api, ri, d.rounds.length, start) : r); });
          }
          return true;
        }
        for (var i = 0; i < snake.length - 1; i++) { snake[i].x = snake[i + 1].x; snake[i].y = snake[i + 1].y; }
        head().x = nx; head().y = ny;
        CT.sound.play("step");
        render();
        return true;
      }

      // Show me: steer to each fruit the pattern needs, square by square.
      function autoplay() {
        if (walking) return;
        walking = true; api.busy(true);
        var mine = rd;
        (function next() {
          if (!api.alive() || mine !== rd) { walking = false; return; }
          if (got.length >= rd.answer.length) { walking = false; api.busy(false); return; }
          var goal = food[want()], h = head();
          var path = CT.grid.bfs({ at: function () { return "."; } }, [h.x, h.y], goal, function (x, y) {
            if (x < 0 || y < 0 || x >= d.w || y >= d.h || rock[x + "," + y]) return false;
            if (snake.slice(1).some(function (s) { return s.x === x && s.y === y; })) return false;
            var f = Object.keys(food).filter(function (k) { return food[k] && food[k][0] === x && food[k][1] === y; })[0];
            return !f || f === want();
          });
          if (!path || path.length < 2) { walking = false; api.busy(false); return; }
          var dn = CT.grid.dirBetween(path[0], path[1]);
          if (dn === BACK[dir]) { dn = ["up", "down", "left", "right"].filter(function (x) { return x !== BACK[dir]; })[0]; }
          stepTo(dn);
          CT.wait(160, next);
        })();
      }

      start(0);
      return {
        checkLabel: "Check the pattern",
        check: function () {
          if (got.length < rd.answer.length) return { ok: false, incomplete: true, msg: "Steer the snake to eat " + (rd.answer.length - got.length) + " more fruit, in the pattern." };
          return { ok: true };
        },
        mark: function () { },
        reset: function () { start(ri); },
        showMe: function () { autoplay(); },
        scaffold: function () { glow = true; render(); CT.announce("The next fruit in the pattern is glowing."); },
        destroy: function () { }
      };
    }
  };
})(typeof window !== "undefined" ? window : globalThis);
