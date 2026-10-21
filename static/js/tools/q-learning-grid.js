/* Q-learning grid lab: an agent learning a grid world from rewards alone.
 *
 * Each cell is split into four triangles, one per action, coloured by that
 * action's Q-value, with an arrow for the best action. Training runs real
 * episodes of tabular Q-learning with an epsilon-greedy policy, using the
 * update from the lesson. The world can be redrawn by painting cells.
 */
(function () {
  "use strict";

  var NS = "http://www.w3.org/2000/svg";
  var R = 6, C = 9, S = 50;
  var PRESETS = {
    room: ["........G",
           "..#####..",
           "........X",
           ".##..##..",
           "....X....",
           "S........"],
    cliff: [".........",
            ".........",
            ".........",
            ".........",
            ".........",
            "SXXXXXXXG"],
    maze: ["..#...#.G",
           "..#.#.#..",
           "....#...#",
           "##.##.#..",
           "......#X.",
           "S.##....."]
  };
  var MOVES = [[-1, 0], [0, 1], [1, 0], [0, -1]];       // up, right, down, left
  var NAMES = ["up", "right", "down", "left"];

  function el(tag, cls, txt) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (txt !== undefined && txt !== null) n.textContent = txt;
    return n;
  }
  function sv(tag, attrs) {
    var n = document.createElementNS(NS, tag);
    for (var k in attrs) if (Object.prototype.hasOwnProperty.call(attrs, k)) n.setAttribute(k, attrs[k]);
    return n;
  }
  function mix(a, b, t) {
    return "rgb(" + [0, 1, 2].map(function (k) { return Math.round(a[k] + (b[k] - a[k]) * t); }).join(",") + ")";
  }
  function qColour(v) {
    // untried actions show the page; blue for bad, magenta then amber for good
    if (v === 0) return "transparent";
    var t = Math.max(-1, Math.min(1, v / 8)), pale = [226, 232, 240];
    if (t < 0) return mix(pale, [29, 78, 216], Math.min(1, 0.25 - t));
    if (t <= 0.6) return mix(pale, [190, 24, 93], Math.min(1, 0.25 + t / 0.6 * 0.75));
    return mix([190, 24, 93], [245, 158, 11], (t - 0.6) / 0.4);
  }

  function build(body) {
    body.textContent = "";
    var st = { grid: PRESETS.room.map(function (r) { return r.split(""); }), Q: new Float64Array(R * C * 4),
               episodes: 0, recent: [], cursor: [0, 0], timer: 0 };

    var row = el("div", "tool-row");
    function field(label, ctrl, out) {
      var f = el("div", "tool-field"), id = "ql-" + Math.random().toString(36).slice(2, 8);
      var l = el("label", null, label); l.setAttribute("for", id); ctrl.id = id;
      f.appendChild(l); f.appendChild(ctrl); if (out) f.appendChild(out); row.appendChild(f); return f;
    }
    function slider(min, max, stepv, val) { var s = el("input"); s.type = "range"; s.min = min; s.max = max; s.step = stepv; s.value = val; return s; }
    var sWorld = el("select");
    [["room", "A room with traps"], ["cliff", "The cliff walk"], ["maze", "A maze"]].forEach(function (o) { var n = el("option", null, o[1]); n.value = o[0]; sWorld.appendChild(n); });
    field("World", sWorld);
    var sA = slider("0.05", "1", "0.05", "0.5"), oA = el("span", "ql-num", "α = 0.50"); field("Learning rate", sA, oA);
    var sG = slider("0.5", "0.99", "0.01", "0.9"), oG = el("span", "ql-num", "γ = 0.90"); field("Discount", sG, oG);
    var sE = slider("0", "0.5", "0.01", "0.1"), oE = el("span", "ql-num", "ε = 0.10"); field("Exploration", sE, oE);
    var sPaint = el("select");
    [["#", "Wall"], ["X", "Trap (−10)"], ["G", "Goal (+10)"], ["S", "Start"], [".", "Empty"]].forEach(function (o) { var n = el("option", null, o[1]); n.value = o[0]; sPaint.appendChild(n); });
    field("Click a cell to paint", sPaint);

    var btns = el("div", "tool-btns");
    var b1 = el("button", "tool-btn", "Train 1 episode"); b1.type = "button";
    var b100 = el("button", "tool-btn is-primary", "Train 100 episodes"); b100.type = "button";
    var bRun = el("button", "tool-btn", "Watch the agent"); bRun.type = "button";
    var bReset = el("button", "tool-btn", "Forget everything"); bReset.type = "button";
    [b1, b100, bRun, bReset].forEach(function (b) { btns.appendChild(b); });

    var svg = sv("svg", { viewBox: "0 0 " + C * S + " " + R * S, "class": "ql-grid", tabindex: "0", role: "application",
                          "aria-label": "Grid world. Arrow keys move the cursor; Enter paints the chosen cell type." });
    var stats = el("p", "ql-stats");
    var status = el("p", "tool-status"); status.setAttribute("role", "status"); status.setAttribute("aria-live", "polite");
    var note = el("p", "tool-note", "Each cell's four triangles show the Q-value of moving up, right, down and left: blue is bad, amber is good. Every step costs 0.1; the goal pays +10 and a trap costs −10, and both end the episode.");

    var cells = [];
    function drawGrid() {
      while (svg.firstChild) svg.removeChild(svg.firstChild);
      cells = [];
      for (var r = 0; r < R; r++) for (var c = 0; c < C; c++) {
        var x = c * S, y = r * S, g = sv("g", {}), cell = { tris: [], arrow: null, g: g };
        var cx = x + S / 2, cy = y + S / 2;
        var pts = [[x, y, x + S, y], [x + S, y, x + S, y + S], [x + S, y + S, x, y + S], [x, y + S, x, y]];
        for (var a = 0; a < 4; a++) {
          var p = pts[a];
          var tri = sv("polygon", { points: p[0] + "," + p[1] + " " + p[2] + "," + p[3] + " " + cx + "," + cy, "class": "ql-tri" });
          g.appendChild(tri); cell.tris.push(tri);
        }
        var block = sv("rect", { x: x + 1, y: y + 1, width: S - 2, height: S - 2, rx: 4, "class": "ql-block" });
        var lab = sv("text", { x: cx, y: cy + 6, "text-anchor": "middle", "class": "ql-lab" });
        var arr = sv("path", { "class": "ql-arrow" });
        g.appendChild(block); g.appendChild(arr); g.appendChild(lab);
        cell.block = block; cell.lab = lab; cell.arrow = arr;
        g.setAttribute("data-r", r); g.setAttribute("data-c", c);
        svg.appendChild(g); cells.push(cell);
      }
      st.cursorEl = sv("rect", { width: S - 4, height: S - 4, rx: 5, "class": "ql-cursor" });
      st.agentEl = sv("circle", { r: 11, "class": "ql-agent", cx: -50, cy: -50 });
      svg.appendChild(st.cursorEl); svg.appendChild(st.agentEl);
      paint();
    }
    function bestA(s) {
      var b = 0;
      for (var a = 1; a < 4; a++) if (st.Q[s * 4 + a] > st.Q[s * 4 + b]) b = a;
      return b;
    }
    function paint() {
      for (var r = 0; r < R; r++) for (var c = 0; c < C; c++) {
        var s = r * C + c, cell = cells[s], ch = st.grid[r][c];
        var special = ch === "#" || ch === "X" || ch === "G";
        cell.block.setAttribute("class", "ql-block" + (ch === "#" ? " is-wall" : ch === "X" ? " is-trap" : ch === "G" ? " is-goal" : ch === "S" ? " is-start" : ""));
        cell.lab.textContent = ch === "X" ? "−10" : ch === "G" ? "+10" : ch === "S" ? "S" : "";
        var any = false;
        for (var a = 0; a < 4; a++) {
          var q = st.Q[s * 4 + a];
          if (q !== 0) any = true;
          cell.tris[a].setAttribute("fill", special ? "none" : qColour(q));
        }
        if (!special && any) {
          var b = bestA(s), x = c * S + S / 2, y = r * S + S / 2, d = MOVES[b];
          var tx = x + d[1] * 14, ty = y + d[0] * 14, bx = x - d[1] * 10, by = y - d[0] * 10;
          var px = -d[0] * 6, py = d[1] * 6;
          cell.arrow.setAttribute("d", "M" + bx + " " + by + " L" + tx + " " + ty + " M" + (tx - d[1] * 7 + px) + " " + (ty - d[0] * 7 + py) +
            " L" + tx + " " + ty + " L" + (tx - d[1] * 7 - px) + " " + (ty - d[0] * 7 - py));
        } else {
          cell.arrow.setAttribute("d", "");
        }
      }
      st.cursorEl.setAttribute("x", st.cursor[1] * S + 2); st.cursorEl.setAttribute("y", st.cursor[0] * S + 2);
      var last = st.recent.slice(-20), wins = last.filter(function (e) { return e.goal; }).length;
      var avg = last.length ? last.reduce(function (t, e) { return t + e.steps; }, 0) / last.length : 0;
      stats.textContent = "Episodes: " + st.episodes + (last.length ? "  ·  last " + last.length + ": reached the goal " + wins + " times, " + avg.toFixed(1) + " steps on average" : "");
    }
    function start() {
      for (var r = 0; r < R; r++) for (var c = 0; c < C; c++) if (st.grid[r][c] === "S") return [r, c];
      return [R - 1, 0];
    }
    function move(p, a) {
      var nr = p[0] + MOVES[a][0], nc = p[1] + MOVES[a][1];
      if (nr < 0 || nc < 0 || nr >= R || nc >= C || st.grid[nr][nc] === "#") return p;
      return [nr, nc];
    }
    function episode() {
      var alpha = parseFloat(sA.value), gamma = parseFloat(sG.value), eps = parseFloat(sE.value);
      var p = start(), steps = 0, goal = false;
      while (steps < 200) {
        var s = p[0] * C + p[1], a;
        if (Math.random() < eps) a = Math.floor(Math.random() * 4);
        else {
          var best = -Infinity, ties = [];
          for (var k = 0; k < 4; k++) { var q = st.Q[s * 4 + k]; if (q > best + 1e-12) { best = q; ties = [k]; } else if (Math.abs(q - best) <= 1e-12) ties.push(k); }
          a = ties[Math.floor(Math.random() * ties.length)];
        }
        var np = move(p, a), ch = st.grid[np[0]][np[1]], ns = np[0] * C + np[1];
        var r = ch === "G" ? 10 : ch === "X" ? -10 : -0.1, done = ch === "G" || ch === "X";
        var target = r + (done ? 0 : gamma * Math.max(st.Q[ns * 4], st.Q[ns * 4 + 1], st.Q[ns * 4 + 2], st.Q[ns * 4 + 3]));
        st.Q[s * 4 + a] += alpha * (target - st.Q[s * 4 + a]);
        p = np; steps += 1;
        if (done) { goal = ch === "G"; break; }
      }
      st.episodes += 1;
      st.recent.push({ steps: steps, goal: goal });
      if (st.recent.length > 100) st.recent.shift();
      return { steps: steps, goal: goal };
    }
    function stopWatch() { if (st.timer) { clearTimeout(st.timer); st.timer = 0; } st.agentEl.setAttribute("cx", -50); }
    function train(n) {
      stopWatch();
      var res;
      for (var i = 0; i < n; i++) res = episode();
      paint();
      status.textContent = n === 1 ? "Episode " + st.episodes + ": " + (res.goal ? "reached the goal" : "did not reach the goal") + " after " + res.steps + " steps."
        : "Trained " + n + " more episodes. Look at how the good values have spread out from the goal.";
    }
    function watch() {
      stopWatch();
      var p = start(), steps = 0, seen = {};
      var reduce = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      function show() { st.agentEl.setAttribute("cx", p[1] * S + S / 2); st.agentEl.setAttribute("cy", p[0] * S + S / 2); }
      function next() {
        var ch = st.grid[p[0]][p[1]];
        if (ch === "G") { status.textContent = "The agent reached the goal in " + steps + " steps, following its best arrows."; return; }
        if (ch === "X") { status.textContent = "The agent walked into a trap after " + steps + " steps. Train it more."; return; }
        var key = p[0] + "," + p[1];
        if (seen[key] || steps > 60) { status.textContent = "The agent is going round in circles: it has not learned this part of the world yet. Train it more."; return; }
        seen[key] = true;
        var np = move(p, bestA(p[0] * C + p[1]));
        if (np[0] === p[0] && np[1] === p[1]) { status.textContent = "The agent keeps walking into a wall: train it more."; return; }
        p = np; steps += 1; show();
        st.timer = setTimeout(next, reduce ? 0 : 220);
      }
      show();
      status.textContent = "Watching the agent follow its best arrows, with no exploration.";
      st.timer = setTimeout(next, reduce ? 0 : 300);
    }
    function reset() {
      stopWatch();
      st.Q = new Float64Array(R * C * 4); st.episodes = 0; st.recent = [];
      paint();
      status.textContent = "Every Q-value is back to 0: the agent knows nothing. Train it.";
    }
    function paintCell(r, c) {
      var v = sPaint.value;
      if (v === "S" || v === "G") {
        for (var i = 0; i < R; i++) for (var j = 0; j < C; j++) if (st.grid[i][j] === v) st.grid[i][j] = ".";
      }
      if (st.grid[r][c] === "S" && v !== "S") return;           // keep exactly one start
      st.grid[r][c] = v;
      reset();
      status.textContent = "Changed the world, so the agent starts learning again.";
    }

    svg.addEventListener("click", function (ev) {
      var g = ev.target.closest ? ev.target.closest("g[data-r]") : null;
      if (!g) return;
      st.cursor = [+g.getAttribute("data-r"), +g.getAttribute("data-c")];
      paintCell(st.cursor[0], st.cursor[1]);
    });
    svg.addEventListener("keydown", function (ev) {
      var used = true;
      if (ev.key === "ArrowUp") st.cursor[0] = Math.max(0, st.cursor[0] - 1);
      else if (ev.key === "ArrowDown") st.cursor[0] = Math.min(R - 1, st.cursor[0] + 1);
      else if (ev.key === "ArrowLeft") st.cursor[1] = Math.max(0, st.cursor[1] - 1);
      else if (ev.key === "ArrowRight") st.cursor[1] = Math.min(C - 1, st.cursor[1] + 1);
      else if (ev.key === "Enter" || ev.key === " ") paintCell(st.cursor[0], st.cursor[1]);
      else used = false;
      if (used) { ev.preventDefault(); paint(); }
    });
    sWorld.addEventListener("change", function () { st.grid = PRESETS[sWorld.value].map(function (r) { return r.split(""); }); reset(); });
    [[sA, oA, "α"], [sG, oG, "γ"], [sE, oE, "ε"]].forEach(function (p) {
      p[0].addEventListener("input", function () { p[1].textContent = p[2] + " = " + parseFloat(p[0].value).toFixed(2); });
    });
    b1.addEventListener("click", function () { train(1); });
    b100.addEventListener("click", function () { train(100); });
    bRun.addEventListener("click", watch);
    bReset.addEventListener("click", reset);

    body.appendChild(row); body.appendChild(btns); body.appendChild(svg); body.appendChild(stats);
    body.appendChild(status); body.appendChild(note);
    drawGrid();
    status.textContent = "The agent starts at S knowing nothing. Train it, then watch it.";
  }

  function init() {
    var mounts = document.querySelectorAll('.tool[data-tool="q-learning-grid"]');
    Array.prototype.forEach.call(mounts, function (m) {
      var b = m.querySelector(".tool-body");
      if (b) build(b);
    });
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", init);
  else init();
})();
