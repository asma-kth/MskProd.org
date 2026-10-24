/* Engine: botcode. One pseudocode algorithm drives a car, or steers a snake,
 * on several boards; it passes only if it works on all of them.
 *
 * data: { look: "car"|"snake", boards: [{name, grid, dir}], template, choices: {blank: [options]},
 *         answer: {blank: option}, typing, maxSteps }
 * Car grids: # grass, . road, S start, F finish. Commands: forward(), turnLeft(),
 * turnRight(); sensors: roadAhead(), roadOnLeft(), roadOnRight(), atFinish().
 * Snake grids: # wall, . empty, * food, S start. Sensors: foodAhead(),
 * foodOnLeft(), foodOnRight(), allEaten(). The snake grows as it eats, and more
 * than two turns in a row make it dizzy, so it cannot spin on the spot.
 * The student fills the template's gaps, or (with typing) writes the code.
 * answer: {blank: option} or {code: text}
 */
(function (root) {
  "use strict";
  var CT = root.CT = root.CT || {};
  var DIR = { up: [0, -1], right: [1, 0], down: [0, 1], left: [-1, 0] };

  function key(p) { return p[0] + "," + p[1]; }
  function world(look, board) {
    var map = CT.grid.parse(board.grid), s = map.one("S"), food = {};
    if (look === "snake") map.find("*").forEach(function (p) { food[key(p)] = true; });
    return { map: map, look: look, x: s[0], y: s[1], dir: board.dir || "right", body: [], food: food };
  }
  function snap(w) { return { x: w.x, y: w.y, dir: w.dir, body: w.body.map(function (b) { return b.slice(); }), food: Object.assign({}, w.food) }; }
  function cellIn(w, d) { var v = DIR[d]; return [w.x + v[0], w.y + v[1]]; }
  function commands(w, log) {
    var L = CT.grid.TURN_L, R = CT.grid.TURN_R;
    // A snake that turns more than twice in a row is spinning on the spot, which is not allowed.
    var spun = function () {
      w.spin = (w.spin || 0) + 1;
      if (w.look === "snake" && w.spin > 2) { log.push(Object.assign(snap(w), { crash: true })); return { ctError: "The snake got dizzy turning round and round! Turn towards the food instead." }; }
      log.push(snap(w));
    };
    var turn = { turnLeft: function () { w.dir = L[w.dir]; return spun(); }, turnRight: function () { w.dir = R[w.dir]; return spun(); } };
    if (w.look === "car") {
      var road = function (p) { return w.map.at(p[0], p[1]) !== "#"; };
      return Object.assign(turn, {
        roadAhead: function () { return road(cellIn(w, w.dir)); },
        roadOnLeft: function () { return road(cellIn(w, L[w.dir])); },
        roadOnRight: function () { return road(cellIn(w, R[w.dir])); },
        atFinish: function () { return w.map.at(w.x, w.y) === "F"; },
        forward: function () {
          var n = cellIn(w, w.dir);
          if (!road(n)) { log.push(Object.assign(snap(w), { crash: true })); return { ctError: "Crash! The car drove off the road." }; }
          w.x = n[0]; w.y = n[1]; w.spin = 0; log.push(snap(w));
        }
      });
    }
    var hasFood = function (p) { return !!w.food[key(p)]; };
    return Object.assign(turn, {
      foodAhead: function () { return hasFood(cellIn(w, w.dir)); },
      foodOnLeft: function () { return hasFood(cellIn(w, L[w.dir])); },
      foodOnRight: function () { return hasFood(cellIn(w, R[w.dir])); },
      allEaten: function () { return Object.keys(w.food).length === 0; },
      forward: function () {
        var n = cellIn(w, w.dir);
        if (w.map.at(n[0], n[1]) === "#") { log.push(Object.assign(snap(w), { crash: true })); return { ctError: "Crash! The snake hit a wall." }; }
        if (w.body.some(function (b) { return b[0] === n[0] && b[1] === n[1]; })) { log.push(Object.assign(snap(w), { crash: true })); return { ctError: "Ouch! The snake bit its own tail." }; }
        w.spin = 0;
        w.body.push([w.x, w.y]);
        if (hasFood(n)) delete w.food[key(n)];
        else w.body.shift();
        w.x = n[0]; w.y = n[1]; log.push(snap(w));
      }
    });
  }
  function runBoard(d, board, code) {
    var w = world(d.look, board), log = [snap(w)];
    var r = CT.pseudo.run(code, { maxSteps: d.maxSteps || 400, builtins: commands(w, log) });
    var goal = d.look === "car" ? w.map.at(w.x, w.y) === "F" : Object.keys(w.food).length === 0;
    var msg = null;
    if (r.error) msg = /too long/.test(r.error.msg) ? "The program kept going without reaching the goal. Check the loop and the turns." : "Line " + r.error.line + ": " + r.error.msg;
    else if (!goal) msg = d.look === "car" ? "The program finished, but the car never reached the finish." : "The program finished, but some food is left.";
    return { ok: !msg, msg: msg, log: log };
  }
  CT.botRun = runBoard;

  function codeOf(d, a) {
    a = a || {};
    if (a.code !== undefined) return String(a.code);
    var blanks = Object.keys(d.choices || {});
    if (blanks.some(function (b) { return !a[b]; })) return null;
    return CT.fillTemplate(d.template, a);
  }
  CT.check.botcode = function (d, a) {
    var code = codeOf(d, a);
    if (code === null) return { ok: false, incomplete: true, msg: "Choose something for every gap first." };
    if (!code.trim()) return { ok: false, incomplete: true, msg: "Write your algorithm first." };
    var p = CT.pseudo.parse(code);
    if (!p.ok) return { ok: false, msg: "Line " + p.error.line + ": " + p.error.msg };
    for (var i = 0; i < d.boards.length; i++) {
      var r = runBoard(d, d.boards[i], code);
      if (!r.ok) return { ok: false, board: i, msg: d.boards[i].name + ": " + r.msg };
    }
    return { ok: true };
  };
  CT.solve.botcode = function (d) { return Object.assign({}, d.answer); };

  // ------------------------------------------------------------- drawing
  var S = 40;
  function carShape() {
    return '<g class="cbc-car"><rect x="11" y="5" width="18" height="30" rx="6" class="cbc-car-body"/><rect x="13" y="10" width="14" height="7" rx="2" fill="#E0F2FE"/>' +
      '<rect x="8" y="9" width="4" height="7" rx="1.5" fill="#111827"/><rect x="28" y="9" width="4" height="7" rx="1.5" fill="#111827"/>' +
      '<rect x="8" y="24" width="4" height="7" rx="1.5" fill="#111827"/><rect x="28" y="24" width="4" height="7" rx="1.5" fill="#111827"/>' +
      '<circle cx="15" cy="7" r="1.6" fill="#FEF08A"/><circle cx="25" cy="7" r="1.6" fill="#FEF08A"/></g>';
  }
  var ROT = { up: 0, right: 90, down: 180, left: 270 };
  function drawBoard(svg, d, board, st) {
    var map = CT.grid.parse(board.grid), out = "";
    for (var y = 0; y < map.h; y++) for (var x = 0; x < map.w; x++) {
      var ch = map.at(x, y), cls = ch === "#" ? (d.look === "car" ? "cbc-grass" : "cbc-wall") : (d.look === "car" ? "cbc-road" : "cbc-floor");
      out += '<rect x="' + (x * S + 1) + '" y="' + (y * S + 1) + '" width="' + (S - 2) + '" height="' + (S - 2) + '" rx="5" class="' + cls + '"/>';
      if (ch === "F") out += '<text x="' + (x * S + S / 2) + '" y="' + (y * S + S / 2 + 1) + '" class="csn-ico">🏁</text>';
    }
    if (d.look === "snake") {
      Object.keys(st.food).forEach(function (k) { var p = k.split(","); out += '<text x="' + (p[0] * S + S / 2) + '" y="' + (p[1] * S + S / 2 + 1) + '" class="csn-ico">🍎</text>'; });
      st.body.forEach(function (b) { out += '<rect x="' + (b[0] * S + 4) + '" y="' + (b[1] * S + 4) + '" width="' + (S - 8) + '" height="' + (S - 8) + '" rx="9" class="cbc-seg"/>'; });
      out += '<g transform="rotate(' + ROT[st.dir] + " " + (st.x * S + S / 2) + " " + (st.y * S + S / 2) + ')"><rect x="' + (st.x * S + 3) + '" y="' + (st.y * S + 3) + '" width="' + (S - 6) + '" height="' + (S - 6) + '" rx="13" class="cbc-head"/>' +
        '<circle cx="' + (st.x * S + 14) + '" cy="' + (st.y * S + 13) + '" r="4" fill="#fff"/><circle cx="' + (st.x * S + 26) + '" cy="' + (st.y * S + 13) + '" r="4" fill="#fff"/>' +
        '<circle cx="' + (st.x * S + 14) + '" cy="' + (st.y * S + 12) + '" r="2" fill="#111827"/><circle cx="' + (st.x * S + 26) + '" cy="' + (st.y * S + 12) + '" r="2" fill="#111827"/></g>';
    } else {
      out += '<g transform="translate(' + st.x * S + " " + st.y * S + ") rotate(" + ROT[st.dir] + " 20 20)" + '"' + (st.crash ? ' class="is-crash"' : "") + ">" + carShape() + "</g>";
    }
    if (st.crash) out += '<text x="' + (st.x * S + S / 2) + '" y="' + (st.y * S + 4) + '" class="csn-ico">💥</text>';
    svg.setAttribute("viewBox", "0 0 " + map.w * S + " " + map.h * S);
    svg.innerHTML = out;
  }

  CT.engines.botcode = {
    mount: function (host, level, api) {
      var d = level.data, bi = 0, picks = {}, typing = false, code = "", status = d.boards.map(function () { return null; }), running = false, practice = null;
      var board = CT.el("div", { class: "cbc" });
      host.appendChild(board);
      var svg = CT.svg("svg", { class: "cbc-map", role: "img" });

      function render() {
        CT.clear(board);
        var tabs = CT.el("div", { class: "cbc-tabs", role: "group", "aria-label": "Boards" }, d.boards.map(function (b, i) {
          var s = status[i];
          return CT.el("button", { type: "button", class: "cbc-tab" + (i === bi ? " is-on" : "") + (s === true ? " is-pass" : s === false ? " is-fail" : ""),
            "aria-pressed": i === bi ? "true" : "false", disabled: running ? true : null,
            onclick: function () { bi = i; practice = null; render(); } }, [s === true ? "✅ " : s === false ? "❌ " : "", b.name]);
        }));
        var st = practice || snap(world(d.look, d.boards[bi]));
        drawBoard(svg, d, d.boards[bi], st);
        svg.setAttribute("aria-label", d.boards[bi].name + ". " + (d.look === "car" ? "The car must reach the finish flag." : "The snake must eat every apple."));
        var left = CT.el("div", { class: "cbc-left" }, [tabs, svg]);
        if (d.look === "car") left.appendChild(practicePad());
        CT.append(board, [CT.el("div", { class: "cbc-wrap" }, [left, codePanel()])]);
      }
      function practicePad() {
        var act = function (name) {
          if (running) return;
          var w = world(d.look, d.boards[bi]);
          if (practice) { w.x = practice.x; w.y = practice.y; w.dir = practice.dir; }
          var log = [], cmd = commands(w, log)[name]();
          practice = log[log.length - 1] || snap(w);
          if (cmd && cmd.ctError) { api.say(cmd.ctError + " Try again.", "think", 1800); CT.sound.play("bad"); CT.wait(700, function () { if (api.alive()) { practice = null; render(); } }); }
          else CT.sound.play(name === "forward" ? "step" : "tap");
          if (w.map.at(w.x, w.y) === "F") api.say("You reached the finish! Now write an algorithm that can do it by itself.", "happy", 3000);
          render();
        };
        return CT.el("div", { class: "cbc-practice" }, [CT.el("p", { class: "ct-tray-h" }, "🕹 Practise driving"),
          CT.el("button", { type: "button", class: "cdz-move", onclick: function () { act("turnLeft"); } }, "↩️ Left"),
          CT.el("button", { type: "button", class: "cdz-move", onclick: function () { act("forward"); } }, "⬆️ Forward"),
          CT.el("button", { type: "button", class: "cdz-move", onclick: function () { act("turnRight"); } }, "↪️ Right"),
          CT.el("button", { type: "button", class: "ct-btn ct-btn-mini", onclick: function () { practice = null; render(); } }, "↺ Start again")]);
      }
      function codePanel() {
        var panel = CT.el("div", { class: "cbc-code" }, [CT.el("p", { class: "ct-tray-h" }, typing ? "Your algorithm (OCR-style pseudocode)" : "Your algorithm: choose for each gap")]);
        if (typing) {
          panel.appendChild(CT.el("textarea", { class: "cbc-ta", rows: "12", spellcheck: "false", "aria-label": "Your algorithm", oninput: function () { code = this.value; status = d.boards.map(function () { return null; }); } }, code));
        } else {
          var ol = CT.el("ol", { class: "ct-code cbc-tpl" });
          d.template.split("\n").forEach(function (line, li) {
            var c = CT.el("code");
            line.split(/(\{\w+\})/).forEach(function (p) {
              var m = /^\{(\w+)\}$/.exec(p);
              if (!m) { if (p) c.appendChild(CT.el("span", { html: CT.hilite(p) })); return; }
              var b = m[1];
              var sel = CT.el("select", { class: "cbc-sel", "data-blank": b, "aria-label": "Gap on line " + (li + 1), onchange: function () { picks[b] = this.value || null; status = d.boards.map(function () { return null; }); } },
                [CT.el("option", { value: "" }, "— choose —")].concat(d.choices[b].map(function (o) { return CT.el("option", { value: o, selected: picks[b] === o ? true : null }, o); })));
              c.appendChild(sel);
            });
            ol.appendChild(CT.el("li", null, [CT.el("span", { class: "ct-ln", "aria-hidden": "true" }, String(li + 1)), c]));
          });
          panel.appendChild(ol);
        }
        if (d.typing) panel.appendChild(CT.el("button", { type: "button", class: "ct-btn ct-btn-mini", onclick: function () {
          if (!typing) code = codeOf(d, picks) || CT.fillTemplate(d.template, picks);
          typing = !typing; render();
        } }, typing ? "🧩 Back to the gaps" : "✍️ Type it myself"));
        panel.appendChild(CT.el("details", { class: "cbc-ref" }, [CT.el("summary", null, "Commands you can use"),
          CT.el("p", null, d.look === "car" ? "forward(), turnLeft(), turnRight(); sensors: roadAhead(), roadOnLeft(), roadOnRight(), atFinish()."
            : "forward(), turnLeft(), turnRight(); sensors: foodAhead(), foodOnLeft(), foodOnRight(), allEaten()."),
          CT.el("p", null, "Sensors give True or False, so they can go after if, elseif and while. Use NOT to turn True into False.")]));
        return panel;
      }

      function answer() { return typing ? { code: code } : picks; }
      function animate(done) {
        var c = codeOf(d, answer());
        var r = CT.check.botcode(d, answer());
        if (r.incomplete || c === null || !CT.pseudo.parse(c).ok) { done(r); return; }
        running = true; api.busy(true); practice = null;
        status = d.boards.map(function () { return null; });
        var i = 0;
        (function nextBoard() {
          if (!api.alive()) return;
          if (i >= d.boards.length) { running = false; api.busy(false); render(); done({ ok: true }); return; }
          bi = i; render();
          var res = runBoard(d, d.boards[i], c), f = 0;
          (function frame() {
            if (!api.alive()) return;
            if (f >= res.log.length) {
              status[i] = res.ok;
              if (!res.ok) { running = false; api.busy(false); render(); done({ ok: false, board: i, msg: d.boards[i].name + ": " + res.msg }); return; }
              CT.sound.play("good"); i++; CT.wait(350, nextBoard); return;
            }
            practice = res.log[f++]; drawBoard(svg, d, d.boards[bi], practice);
            CT.wait(110, frame);
          })();
        })();
      }

      render();
      return {
        checkLabel: d.look === "car" ? "▶ Test on all tracks" : "▶ Test on all boards",
        run: function (done) { animate(done); },
        mark: function () { render(); },
        reset: function () { if (running) return; picks = {}; code = ""; typing = false; status = d.boards.map(function () { return null; }); practice = null; render(); },
        showMe: function () { picks = Object.assign({}, d.answer); typing = false; render(); },
        scaffold: function () {
          var b = Object.keys(d.answer).filter(function (k) { return picks[k] !== d.answer[k]; })[0];
          if (b) { picks[b] = d.answer[b]; typing = false; render(); CT.announce("Pixel filled one gap for you."); }
        },
        destroy: function () { }
      };
    }
  };
})(typeof window !== "undefined" ? window : globalThis);
