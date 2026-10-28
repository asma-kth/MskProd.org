/* The grid worlds: mazes, robots, snakes and cars all live on squares.
 *
 * CT.grid.parse turns rows of characters into a map, CT.grid.bfs finds the
 * shortest walk between two squares, and CT.grid.view draws a map as SVG with
 * pieces that glide from square to square. The parsing and path finding touch
 * no DOM, so the level checks can use them under Node.
 */
(function (root) {
  "use strict";
  var CT = root.CT = root.CT || {};
  var DIRS = { up: [0, -1], right: [1, 0], down: [0, 1], left: [-1, 0] };
  var TURN_L = { up: "left", left: "down", down: "right", right: "up" };
  var TURN_R = { up: "right", right: "down", down: "left", left: "up" };

  var G = CT.grid = {
    DIRS: DIRS, TURN_L: TURN_L, TURN_R: TURN_R,
    parse: function (rows) {
      var h = rows.length, w = rows[0].length, map = { w: w, h: h, rows: rows.map(function (r) { return r.split(""); }) };
      map.at = function (x, y) { return (x < 0 || y < 0 || x >= w || y >= h) ? "#" : map.rows[y][x]; };
      map.find = function (ch) {
        var out = [];
        for (var y = 0; y < h; y++) for (var x = 0; x < w; x++) if (map.rows[y][x] === ch) out.push([x, y]);
        return out;
      };
      map.one = function (ch) { return map.find(ch)[0] || null; };
      return map;
    },
    // Breadth first search: the shortest list of squares from a to b.
    bfs: function (map, a, b, passable) {
      passable = passable || function (x, y) { return map.at(x, y) !== "#"; };
      var key = function (p) { return p[0] + "," + p[1]; };
      var prev = {}, q = [a], seen = {};
      seen[key(a)] = true;
      while (q.length) {
        var p = q.shift();
        if (p[0] === b[0] && p[1] === b[1]) {
          var path = [p];
          while (prev[key(path[0])]) path.unshift(prev[key(path[0])]);
          return path;
        }
        ["up", "right", "down", "left"].forEach(function (d) {
          var n = [p[0] + DIRS[d][0], p[1] + DIRS[d][1]];
          if (!seen[key(n)] && passable(n[0], n[1])) { seen[key(n)] = true; prev[key(n)] = p; q.push(n); }
        });
      }
      return null;
    },
    dirBetween: function (a, b) {
      var dx = b[0] - a[0], dy = b[1] - a[1];
      return dx === 1 ? "right" : dx === -1 ? "left" : dy === 1 ? "down" : "up";
    },

    // Draw a map. legend maps a character to a tile style or a sticker.
    view: function (host, map, opts) {
      opts = opts || {};
      var S = 40, svg = CT.svg("svg", { class: "cg-map", viewBox: "0 0 " + map.w * S + " " + map.h * S, role: "img",
        "aria-label": opts.label || "A grid map" });
      var tiles = CT.svg("g", { class: "cg-tiles" }), stickers = CT.svg("g", { class: "cg-stickers" }), pieces = CT.svg("g", { class: "cg-pieces" });
      var legend = opts.legend || {};
      for (var y = 0; y < map.h; y++) {
        for (var x = 0; x < map.w; x++) {
          var ch = map.at(x, y), L = legend[ch] || {};
          if (ch === "#") tiles.appendChild(CT.svg("rect", { x: x * S + 1, y: y * S + 1, width: S - 2, height: S - 2, rx: 7, class: "cg-wall" }));
          else {
            tiles.appendChild(CT.svg("rect", { x: x * S + 1, y: y * S + 1, width: S - 2, height: S - 2, rx: 6, class: "cg-floor" + ((x + y) % 2 ? " is-alt" : "") + (L.tile ? " " + L.tile : "") }));
            if (L.sticker) {
              var st = CT.icoSvg(L.sticker, x * S + 6, y * S + 6, S - 12, "cg-sticker");
              st.setAttribute("data-at", x + "," + y); st.setAttribute("data-ch", ch);
              stickers.appendChild(st);
            }
          }
        }
      }
      CT.append(svg, [tiles, stickers, pieces]);
      host.appendChild(svg);
      var api = {
        svg: svg, S: S,
        sticker: function (x, y) { return stickers.querySelector('[data-at="' + x + "," + y + '"]'); },
        removeSticker: function (x, y) { var n = api.sticker(x, y); if (n) n.remove(); },
        setTile: function (x, y, cls) {
          var t = tiles.children[y * map.w + x];
          if (t) t.setAttribute("class", "cg-floor " + cls);
        },
        // A piece is a picture name or an element, moved by translating its group.
        piece: function (id, x, y, content, cls) {
          var g = CT.svg("g", { class: "cg-piece " + (cls || ""), "data-piece": id });
          if (typeof content === "string") g.appendChild(CT.icoSvg(content, 4, 4, S - 8));
          else { content.setAttribute("x", 2); content.setAttribute("y", 1); content.setAttribute("width", S - 4); content.setAttribute("height", S - 2); g.appendChild(content); }
          pieces.appendChild(g);
          api.move(id, x, y, null, true);
          return g;
        },
        move: function (id, x, y, dir, instant) {
          var g = pieces.querySelector('[data-piece="' + id + '"]');
          if (!g) return;
          if (instant || CT.calm()) g.style.transition = "none"; else g.style.transition = "";
          var rot = dir && g.classList.contains("is-turn") ? " rotate(" + { up: 0, right: 90, down: 180, left: 270 }[dir] + " " + S / 2 + " " + S / 2 + ")" : "";
          g.setAttribute("transform", "translate(" + x * S + " " + y * S + ")" + rot);
          g.style.transform = "translate(" + x * S + "px, " + y * S + "px)";
          var inner = g.firstChild;
          if (rot && inner) inner.setAttribute("transform", "rotate(" + { up: 0, right: 90, down: 180, left: 270 }[dir] + " " + S / 2 + " " + S / 2 + ")");
        },
        bump: function (id) {
          var g = pieces.querySelector('[data-piece="' + id + '"]');
          if (!g || CT.calm()) return;
          g.classList.remove("is-bump"); void g.getBoundingClientRect(); g.classList.add("is-bump");
        },
        remove: function (id) { var g = pieces.querySelector('[data-piece="' + id + '"]'); if (g) g.remove(); },
        trail: function (x, y, cls) {
          tiles.appendChild(CT.svg("circle", { cx: x * S + S / 2, cy: y * S + S / 2, r: 5, class: "cg-trail " + (cls || "") }));
        }
      };
      return api;
    },

    // An on-screen arrow pad, for touch screens and for anyone without arrow keys.
    pad: function (onDir, labels) {
      labels = labels || { up: "Up", left: "Left", right: "Right", down: "Down" };
      var b = function (d, t) { return CT.el("button", { type: "button", class: "cg-pad-" + d, "aria-label": labels[d], onclick: function () { onDir(d); } }, t); };
      return CT.el("div", { class: "cg-pad", role: "group", "aria-label": "Move" }, [b("up", CT.ico("arrow-up")), b("left", CT.ico("arrow-left")), b("down", CT.ico("arrow-down")), b("right", CT.ico("arrow-right"))]);
    },
    // Swipes on a touch screen, and the arrow keys when the map has focus.
    controls: function (el, onDir) {
      var sx = 0, sy = 0;
      el.addEventListener("keydown", function (e) {
        var m = { ArrowUp: "up", ArrowDown: "down", ArrowLeft: "left", ArrowRight: "right" }[e.key];
        if (m) { e.preventDefault(); onDir(m); }
      });
      el.addEventListener("touchstart", function (e) { sx = e.touches[0].clientX; sy = e.touches[0].clientY; }, { passive: true });
      el.addEventListener("touchend", function (e) {
        var dx = e.changedTouches[0].clientX - sx, dy = e.changedTouches[0].clientY - sy;
        if (Math.max(Math.abs(dx), Math.abs(dy)) < 24) return;
        onDir(Math.abs(dx) > Math.abs(dy) ? (dx > 0 ? "right" : "left") : (dy > 0 ? "down" : "up"));
      });
    }
  };
})(typeof window !== "undefined" ? window : globalThis);
