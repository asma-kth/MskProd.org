/* Engine: graph. Drive a car across a road graph and find the quickest route.
 *
 * data: { nodes: [{id, label, icon, x, y}], edges: [[a, b, minutes]],
 *         rounds: [{start, end, via, closed: [[a, b]], say}], decor: [[emoji, x, y]], real: button text }
 * The town is drawn twice: as the real streets and as the satnav's graph,
 * which keeps only junctions, roads and minutes. The student drives junction
 * by junction; reaching the end checks the route against the quickest one.
 * answer: [[nodeId...] per round]
 */
(function (root) {
  "use strict";
  var CT = root.CT = root.CT || {};

  function key(a, b) { return a < b ? a + "|" + b : b + "|" + a; }
  function closedSet(rd) { var s = {}; (rd.closed || []).forEach(function (e) { s[key(e[0], e[1])] = true; }); return s; }
  function minutes(d, a, b, rd) {
    if (rd && closedSet(rd)[key(a, b)]) return null;
    var e = d.edges.filter(function (x) { return key(x[0], x[1]) === key(a, b); })[0];
    return e ? e[2] : null;
  }
  CT.graphMinutes = minutes;

  // Dijkstra's shortest path, ignoring closed roads.
  CT.shortest = function (d, from, to, rd) {
    var dist = {}, prev = {}, todo = d.nodes.map(function (n) { return n.id; }), closed = closedSet(rd || {});
    todo.forEach(function (n) { dist[n] = Infinity; });
    dist[from] = 0;
    while (todo.length) {
      todo.sort(function (a, b) { return dist[a] - dist[b]; });
      var u = todo.shift();
      if (dist[u] === Infinity || u === to) break;
      d.edges.forEach(function (e) {
        if (closed[key(e[0], e[1])]) return;
        var v = e[0] === u ? e[1] : e[1] === u ? e[0] : null;
        if (v && todo.indexOf(v) >= 0 && dist[u] + e[2] < dist[v]) { dist[v] = dist[u] + e[2]; prev[v] = u; }
      });
    }
    if (dist[to] === Infinity) return null;
    var path = [to];
    while (path[0] !== from) path.unshift(prev[path[0]]);
    return { time: dist[to], path: path };
  };
  function best(d, rd) {
    if (!rd.via) return CT.shortest(d, rd.start, rd.end, rd);
    var a = CT.shortest(d, rd.start, rd.via, rd), b = CT.shortest(d, rd.via, rd.end, rd);
    return { time: a.time + b.time, path: a.path.concat(b.path.slice(1)) };
  }
  function label(d, id) { return CT.byId(d.nodes, id).label; }

  function checkRound(d, rd, route) {
    route = route || [];
    if (route[0] !== rd.start) return { ok: false, incomplete: true, msg: "Start the drive at " + label(d, rd.start) + "." };
    var total = 0;
    for (var i = 1; i < route.length; i++) {
      var m = minutes(d, route[i - 1], route[i], rd);
      if (m === null) {
        var exists = minutes(d, route[i - 1], route[i]) !== null;
        return { ok: false, msg: exists ? "The road from " + label(d, route[i - 1]) + " to " + label(d, route[i]) + " is closed."
                                        : "There is no road from " + label(d, route[i - 1]) + " to " + label(d, route[i]) + "." };
      }
      total += m;
    }
    if (route[route.length - 1] !== rd.end) return { ok: false, incomplete: true, msg: "Keep driving until you reach " + label(d, rd.end) + "." };
    if (rd.via && route.indexOf(rd.via) < 0) return { ok: false, msg: "You forgot to pick up your friend at " + label(d, rd.via) + "." };
    var b = best(d, rd);
    if (total > b.time) return { ok: false, total: total, msg: "Your route takes " + total + " minutes, but the quickest takes " + b.time + ". Look for a faster way." };
    return { ok: true, total: total };
  }
  CT.check.graph = function (d, a) {
    a = a || [];
    for (var i = 0; i < d.rounds.length; i++) {
      var r = checkRound(d, d.rounds[i], a[i]);
      if (!r.ok) return Object.assign(r, { round: i });
    }
    return { ok: true };
  };
  CT.solve.graph = function (d) { return d.rounds.map(function (rd) { return best(d, rd).path; }); };

  // Houses, trees and cars for the street view, placed clear of the roads.
  var DECOR = [["house", 140, 290], ["house", 150, 360], ["tree", 130, 140], ["office", 290, 290], ["tree", 300, 140], ["house", 430, 270],
               ["tree", 560, 260], ["shop", 440, 120], ["tree", 170, 30], ["house", 470, 30], ["tree", 610, 180], ["car", 140, 345], ["car-blue", 420, 70]];

  CT.engines.graph = {
    mount: function (host, level, api) {
      var d = level.data, ri = 0, rd, route, driving = false, street = false, lastPos = null, k = 1;
      var board = CT.el("div", { class: "cgr" });
      host.appendChild(board);
      var W = 680, H = 400;

      function start(i) {
        ri = i; rd = d.rounds[ri]; route = [rd.start]; driving = false; lastPos = null;
        render();
        api.say(rd.say, ri ? "think" : "happy", 3200);
      }
      function at(id) { return CT.byId(d.nodes, id); }
      function used(a, b) {
        for (var i = 1; i < route.length; i++) if (key(route[i - 1], route[i]) === key(a, b)) return true;
        return false;
      }
      function total() {
        var t = 0;
        for (var i = 1; i < route.length; i++) t += minutes(d, route[i - 1], route[i], rd);
        return t;
      }
      function here() { return route[route.length - 1]; }
      function neighbours(id) {
        var out = [];
        d.edges.forEach(function (e) {
          var v = e[0] === id ? e[1] : e[1] === id ? e[0] : null;
          if (v) out.push({ id: v, mins: e[2], closed: !!closedSet(rd)[key(id, v)] });
        });
        return out;
      }

      function render() {
        CT.clear(board);
        var closed = closedSet(rd);
        var head = CT.el("div", { class: "cgr-head" }, [
          CT.roundChip(ri, d.rounds.length),
          CT.el("p", { class: "cgr-goal" }, ["Route: ", label(d, rd.start), " → ", rd.via ? label(d, rd.via) + " → " : "", label(d, rd.end)]),
          CT.el("p", { class: "cgr-clock", "aria-live": "polite" }, [CT.ico("stopwatch"), " ", CT.el("b", null, String(total())), " min so far"]),
          CT.el("button", { type: "button", class: "ct-btn ct-btn-mini", "aria-pressed": street ? "true" : "false",
            onclick: function () { street = !street; render(); } }, street ? "Show the graph" : (d.real || "Show the real streets"))
        ]);
        // On a narrow screen the map shrinks, so labels and junctions grow to stay readable and tappable.
        k = Math.max(1, Math.min(1.6, 0.92 * W / (board.clientWidth || W)));
        var svg = CT.svg("svg", { class: "cgr-map" + (street ? " is-street" : ""), viewBox: "0 0 " + W + " " + H, role: "img",
          style: "--k: " + k.toFixed(2),
          "aria-label": "Road map. You are at " + label(d, here()) + "." });
        var deco = CT.svg("g", { class: "cgr-decor", "aria-hidden": "true" });
        (d.decor || DECOR).forEach(function (x) { deco.appendChild(CT.icoSvg(x[0], x[1] - 14, x[2] - 22, 28)); });
        svg.appendChild(deco);
        d.edges.forEach(function (e) {
          var a = at(e[0]), b = at(e[1]), isClosed = closed[key(e[0], e[1])];
          var cls = "cgr-road" + (isClosed ? " is-closed" : "") + (used(e[0], e[1]) ? " is-used" : "");
          svg.appendChild(CT.svg("line", { x1: a.x, y1: a.y, x2: b.x, y2: b.y, class: cls + " cgr-road-bed" }));
          svg.appendChild(CT.svg("line", { x1: a.x, y1: a.y, x2: b.x, y2: b.y, class: cls + " cgr-road-top" }));
          var mx = (a.x + b.x) / 2, my = (a.y + b.y) / 2;
          var tag = CT.svg("g", { class: "cgr-tag" + (isClosed ? " is-closed" : "") });
          tag.appendChild(CT.svg("rect", { x: mx - 17 * k, y: my - 11 * k, width: 34 * k, height: 22 * k, rx: 11 * k }));
          if (isClosed) tag.appendChild(CT.icoSvg("roadworks", mx - 10 * k, my - 10 * k, 20 * k));
          else tag.appendChild(CT.svg("text", { x: mx, y: my + 5 * k, text: e[2] + "m" }));
          svg.appendChild(tag);
        });
        d.nodes.forEach(function (n) {
          var near = neighbours(here()).filter(function (x) { return x.id === n.id && !x.closed; }).length > 0;
          var g = CT.svg("g", { class: "cgr-node" + (n.icon ? " is-place" : "") + (near && !driving ? " is-next" : "") + (n.id === here() ? " is-here" : "") +
            (route.indexOf(n.id) >= 0 ? " is-been" : ""), transform: "translate(" + n.x + " " + n.y + ")" });
          g.appendChild(CT.svg("circle", { r: (n.icon ? 22 : 15) * k }));
          if (n.icon) g.appendChild(CT.icoSvg(n.icon, -15 * k, -15 * k, 30 * k, "cgr-ico"));
          else g.appendChild(CT.svg("text", { y: 5 * k, class: "cgr-lab", text: n.label }));
          if (n.icon) g.appendChild(CT.svg("text", { y: 32 * k + 4, class: "cgr-name", text: n.label }));
          if (rd.via === n.id && route.indexOf(n.id) < 0) g.appendChild(CT.icoSvg("wave-hand", 10 * k, -36 * k, 22 * k, "cgr-friend"));
          g.addEventListener("click", function () { go(n.id); });
          svg.appendChild(g);
        });
        // The car starts where it was last drawn and glides to where it is now.
        var car = at(here()), from = lastPos || car;
        var carG = CT.svg("g", { class: "cgr-carg", style: "transform: translate(" + from.x + "px, " + from.y + "px)" });
        carG.appendChild(CT.icoSvg("car", -16 * k, -50 * k, 32 * k, "cgr-car"));
        svg.appendChild(carG);
        if (from !== car) requestAnimationFrame(function () { requestAnimationFrame(function () { carG.style.transform = "translate(" + car.x + "px, " + car.y + "px)"; }); });
        lastPos = car;
        // The same choices as buttons, for keyboards, switches and small screens.
        var opts = CT.el("div", { class: "cgr-opts" }, [CT.el("p", { class: "ct-tray-h" }, "From " + label(d, here()) + ", drive to:")]);
        neighbours(here()).forEach(function (x) {
          opts.appendChild(CT.el("button", { type: "button", class: "ct-btn ct-btn-soft cgr-opt", disabled: x.closed || driving ? true : null,
            onclick: function () { go(x.id); } }, [at(x.id).icon ? CT.ico(at(x.id).icon) : null, " ", at(x.id).label, x.closed ? " (closed)" : " · " + x.mins + " min"]));
        });
        opts.appendChild(CT.el("button", { type: "button", class: "ct-btn ct-btn-mini", disabled: route.length < 2 || driving ? true : null,
          onclick: function () { route.pop(); render(); CT.sound.play("tap"); } }, "Back one road"));
        CT.append(board, [head, CT.el("div", { class: "cgr-mapwrap" }, [svg]), opts]);
      }

      function go(id) {
        if (driving || street) { if (street) api.say("Switch back to the satnav graph to drive.", "think", 2000); return; }
        var m = minutes(d, here(), id, rd);
        if (m === null) {
          var exists = minutes(d, here(), id) !== null;
          api.say(exists ? "That road is closed for roadworks!" : "No road goes straight there from " + label(d, here()) + ".", "think", 2200);
          CT.sound.play("bad");
          return;
        }
        route.push(id);
        CT.sound.play("step");
        render();
        CT.announce("Drove to " + label(d, id) + ". " + total() + " minutes so far.");
        if (id === rd.end && (!rd.via || route.indexOf(rd.via) >= 0)) CT.wait(500, function () { if (api.alive()) api.result(evaluate()); });
      }

      function evaluate() {
        var r = checkRound(d, rd, route);
        if (r.ok && ri < d.rounds.length - 1) return CT.nextRound(api, ri, d.rounds.length, start);
        return r;
      }

      function onResize() {
        var next = Math.max(1, Math.min(1.6, 0.92 * W / (board.clientWidth || W)));
        if (Math.abs(next - k) > 0.1) render();
      }
      root.addEventListener("resize", onResize);
      start(0);
      return {
        checkLabel: "Check my route",
        check: evaluate,
        mark: function () { render(); },
        reset: function () { route = [rd.start]; render(); },
        showMe: function () { route = best(d, rd).path.slice(); street = false; render(); },
        scaffold: function () {
          route = best(d, rd).path.slice(0, 2);
          render();
          CT.announce("Pixel drove part of the quickest route for you.");
        },
        destroy: function () { root.removeEventListener("resize", onResize); }
      };
    }
  };
})(typeof window !== "undefined" ? window : globalThis);
