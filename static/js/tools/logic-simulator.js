/* Logic gate simulator: place gates, wire them up, read the truth table. */
(function () {
  "use strict";

  var NS = "http://www.w3.org/2000/svg";
  var W = 680, H = 380;
  var GW = 60, GH = 40;
  var KINDS = ["AND", "OR", "NOT", "XOR", "NAND", "NOR"];
  var ARITY = { AND: 2, OR: 2, XOR: 2, NAND: 2, NOR: 2, NOT: 1 };

  function svgEl(name, attrs) {
    var n = document.createElementNS(NS, name);
    for (var k in attrs) if (attrs.hasOwnProperty(k)) n.setAttribute(k, attrs[k]);
    return n;
  }

  function el(tag, cls, txt) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (txt !== undefined && txt !== null) n.textContent = txt;
    return n;
  }

  function evalGate(kind, a, b) {
    switch (kind) {
      case "AND": return a && b ? 1 : 0;
      case "OR": return a || b ? 1 : 0;
      case "XOR": return a !== b ? 1 : 0;
      case "NAND": return a && b ? 0 : 1;
      case "NOR": return a || b ? 0 : 1;
      case "NOT": return a ? 0 : 1;
    }
    return 0;
  }

  function gatePath(kind, x, y) {
    var bubble = kind === "NAND" || kind === "NOR" || kind === "NOT";
    var bw = GW - (bubble ? 11 : 0);
    var my = y + GH / 2;
    if (kind === "AND" || kind === "NAND") {
      var r = GH / 2;
      return "M" + x + " " + y + " L" + (x + bw - r) + " " + y
        + " A" + r + " " + r + " 0 0 1 " + (x + bw - r) + " " + (y + GH)
        + " L" + x + " " + (y + GH) + " Z";
    }
    if (kind === "NOT") {
      return "M" + x + " " + y + " L" + x + " " + (y + GH) + " L" + (x + bw) + " " + my + " Z";
    }
    return "M" + x + " " + y
      + " Q" + (x + bw * 0.55) + " " + y + " " + (x + bw) + " " + my
      + " Q" + (x + bw * 0.55) + " " + (y + GH) + " " + x + " " + (y + GH)
      + " Q" + (x + bw * 0.22) + " " + my + " " + x + " " + y + " Z";
  }

  function build(body) {
    body.textContent = "";

    var nextId = 1;
    var nodes = [];
    var wires = [];

    function add(node) { node.id = "n" + (nextId++); nodes.push(node); return node; }
    function byId(id) {
      for (var i = 0; i < nodes.length; i++) if (nodes[i].id === id) return nodes[i];
      return null;
    }

    function reset(inputCount) {
      nodes.length = 0;
      wires.length = 0;
      nextId = 1;
      var labels = ["A", "B", "C"];
      for (var i = 0; i < inputCount; i++) {
        add({ kind: "in", label: labels[i], x: 24, y: 70 + i * 90, value: 0 });
      }
      add({ kind: "out", label: "Q", x: W - 60, y: 160 });
    }

    function inputs() { return nodes.filter(function (n) { return n.kind === "in"; }); }
    function outNode() {
      for (var i = 0; i < nodes.length; i++) if (nodes[i].kind === "out") return nodes[i];
      return null;
    }

    function feeder(nodeId, port) {
      for (var i = 0; i < wires.length; i++) {
        if (wires[i].to === nodeId && wires[i].port === port) return wires[i].from;
      }
      return null;
    }

    /* -------------------------------------------------------- evaluation */

    function value(nodeId, env, seen) {
      if (!nodeId) return null;
      seen = seen || {};
      if (seen[nodeId]) return null;           /* a loop has no defined value */
      seen[nodeId] = true;
      var n = byId(nodeId);
      if (!n) return null;
      if (n.kind === "in") return env[n.label];
      if (n.kind === "out") return value(feeder(n.id, 0), env, seen);
      var a = value(feeder(n.id, 0), env, seen);
      if (ARITY[n.type] === 1) return a === null ? null : evalGate(n.type, a, 0);
      var b = value(feeder(n.id, 1), env, seen);
      if (a === null || b === null) return null;
      return evalGate(n.type, a, b);
    }

    function expr(nodeId, seen) {
      if (!nodeId) return "?";
      seen = seen || {};
      if (seen[nodeId]) return "?";
      seen[nodeId] = true;
      var n = byId(nodeId);
      if (!n) return "?";
      if (n.kind === "in") return n.label;
      if (n.kind === "out") return expr(feeder(n.id, 0), seen);
      var a = expr(feeder(n.id, 0), seen);
      if (n.type === "NOT") return "NOT " + (a.length > 1 ? "(" + a + ")" : a);
      var b = expr(feeder(n.id, 1), seen);
      var join = { AND: " AND ", OR: " OR ", XOR: " XOR ", NAND: " NAND ", NOR: " NOR " };
      return "(" + a + join[n.type] + b + ")";
    }

    /* ------------------------------------------------------------ layout */

    function ports(n) {
      if (n.kind === "in") return { out: { x: n.x + 34, y: n.y + 16 }, ins: [] };
      if (n.kind === "out") return { out: null, ins: [{ x: n.x, y: n.y + 16 }] };
      var bubble = n.type === "NAND" || n.type === "NOR" || n.type === "NOT";
      var tip = n.x + (bubble ? GW : GW - 11) + (bubble ? 0 : 0);
      var ox = bubble ? n.x + GW - 11 + 11 : n.x + GW;
      if (n.type === "AND" || n.type === "NAND") ox = n.x + (n.type === "NAND" ? GW : GW);
      if (n.type === "NOT") ox = n.x + GW;
      var list = ARITY[n.type] === 1
        ? [{ x: n.x - 2, y: n.y + GH / 2 }]
        : [{ x: n.x - 2, y: n.y + 10 }, { x: n.x - 2, y: n.y + GH - 10 }];
      return { out: { x: ox + 2, y: n.y + GH / 2 }, ins: list, tip: tip };
    }

    /* ------------------------------------------------------------ canvas */

    var wrap = el("div", "ls-wrap");

    var palette = el("div", "tool-btns");
    palette.style.marginBottom = ".7rem";
    KINDS.forEach(function (k) {
      var b = el("button", "tool-btn", "Add " + k);
      b.type = "button";
      b.addEventListener("click", function () {
        var col = nodes.filter(function (n) { return n.kind === "gate"; }).length;
        add({
          kind: "gate", type: k,
          x: 150 + (col % 3) * 130,
          y: 50 + Math.floor(col / 3) * 80 % 240
        });
        draw();
      });
      palette.appendChild(b);
    });
    var bClear = el("button", "tool-btn", "Clear");
    bClear.type = "button";
    bClear.addEventListener("click", function () { reset(inputs().length); draw(); });
    var bInputs = el("button", "tool-btn", "Use 3 inputs");
    bInputs.type = "button";
    bInputs.addEventListener("click", function () {
      var n = inputs().length === 2 ? 3 : 2;
      bInputs.textContent = n === 3 ? "Use 2 inputs" : "Use 3 inputs";
      reset(n);
      draw();
    });
    palette.appendChild(bClear);
    palette.appendChild(bInputs);
    wrap.appendChild(palette);

    var help = el("p", "tool-note",
      "Add gates, then drag a gate to move it. Click an output dot and then an input dot "
      + "to join them with a wire. Click a wire to remove it. Click A, B or C to flip that "
      + "input, and the truth table below always shows every combination.");
    help.style.margin = "0 0 .7rem";
    wrap.appendChild(help);

    var svg = svgEl("svg", {
      viewBox: "0 0 " + W + " " + H,
      class: "ls-canvas",
      role: "application",
      "aria-label": "Logic circuit canvas"
    });
    wrap.appendChild(svg);
    body.appendChild(wrap);

    var exprLine = el("p", "tool-status is-good");
    body.appendChild(exprLine);
    var tableWrap = el("div", "tool-scroll");
    body.appendChild(tableWrap);

    /* ------------------------------------------------------ interaction */

    var drag = null;      /* {node, dx, dy} */
    var wiring = null;    /* {from, x, y} */

    function point(evt) {
      var pt = svg.createSVGPoint();
      pt.x = evt.clientX;
      pt.y = evt.clientY;
      var m = svg.getScreenCTM();
      if (!m) return { x: 0, y: 0 };
      var p = pt.matrixTransform(m.inverse());
      return { x: p.x, y: p.y };
    }

    svg.addEventListener("pointermove", function (e) {
      if (drag) {
        var p = point(e);
        drag.node.x = Math.max(4, Math.min(W - GW - 4, p.x - drag.dx));
        drag.node.y = Math.max(4, Math.min(H - GH - 4, p.y - drag.dy));
        draw();
      } else if (wiring) {
        var q = point(e);
        wiring.x = q.x;
        wiring.y = q.y;
        draw();
      }
    });

    function endAll() {
      if (drag) { drag = null; }
      if (wiring) { wiring = null; draw(); }
    }
    svg.addEventListener("pointerup", endAll);
    svg.addEventListener("pointerleave", endAll);

    function connect(fromId, toId, port) {
      if (fromId === toId) return;
      var from = byId(fromId), to = byId(toId);
      if (!from || !to) return;
      if (from.kind === "out") return;
      if (to.kind === "in") return;
      wires = wires.filter(function (w) {
        return !(w.to === toId && w.port === port);
      });
      wires.push({ from: fromId, to: toId, port: port });
      draw();
    }

    /* ----------------------------------------------------------- drawing */

    function draw() {
      while (svg.firstChild) svg.removeChild(svg.firstChild);

      var defs = svgEl("defs");
      svg.appendChild(defs);

      var env = {};
      inputs().forEach(function (n) { env[n.label] = n.value; });

      /* wires first so gates sit on top */
      wires.forEach(function (w, idx) {
        var from = byId(w.from), to = byId(w.to);
        if (!from || !to) return;
        var a = ports(from).out, b = ports(to).ins[w.port];
        if (!a || !b) return;
        var live = value(w.from, env, {});
        var mid = (a.x + b.x) / 2;
        var d = "M" + a.x + " " + a.y + " C" + mid + " " + a.y + " " + mid + " " + b.y
          + " " + b.x + " " + b.y;
        var hit = svgEl("path", { d: d, class: "ls-wire-hit" });
        hit.addEventListener("click", function (ev) {
          ev.stopPropagation();
          wires.splice(idx, 1);
          draw();
        });
        svg.appendChild(svgEl("path", {
          d: d, class: "ls-wire" + (live === 1 ? " is-on" : "")
        }));
        svg.appendChild(hit);
      });

      if (wiring) {
        var src = ports(byId(wiring.from)).out;
        svg.appendChild(svgEl("path", {
          d: "M" + src.x + " " + src.y + " L" + wiring.x + " " + wiring.y,
          class: "ls-wire is-temp"
        }));
      }

      nodes.forEach(function (n) {
        var p = ports(n);
        var g = svgEl("g");

        if (n.kind === "in") {
          var on = n.value === 1;
          var r = svgEl("rect", {
            x: n.x, y: n.y, width: 34, height: 32, rx: 8,
            class: "ls-input" + (on ? " is-on" : "")
          });
          r.addEventListener("click", function () { n.value = on ? 0 : 1; draw(); });
          g.appendChild(r);
          var t = svgEl("text", { x: n.x + 17, y: n.y + 21, class: "ls-label" });
          t.textContent = n.label;
          t.style.pointerEvents = "none";
          g.appendChild(t);
          var v = svgEl("text", { x: n.x + 17, y: n.y + 48, class: "ls-value" });
          v.textContent = String(n.value);
          g.appendChild(v);
        } else if (n.kind === "out") {
          var q = value(n.id, env, {});
          g.appendChild(svgEl("rect", {
            x: n.x, y: n.y, width: 36, height: 32, rx: 8,
            class: "ls-output" + (q === 1 ? " is-on" : "")
          }));
          var ot = svgEl("text", { x: n.x + 18, y: n.y + 21, class: "ls-label" });
          ot.textContent = "Q";
          g.appendChild(ot);
          var ov = svgEl("text", { x: n.x + 18, y: n.y + 48, class: "ls-value" });
          ov.textContent = q === null ? "?" : String(q);
          g.appendChild(ov);
        } else {
          var shape = svgEl("path", { d: gatePath(n.type, n.x, n.y), class: "ls-gate" });
          shape.addEventListener("pointerdown", function (e) {
            e.preventDefault();
            var pt = point(e);
            drag = { node: n, dx: pt.x - n.x, dy: pt.y - n.y };
          });
          g.appendChild(shape);
          if (n.type === "NAND" || n.type === "NOR" || n.type === "NOT") {
            g.appendChild(svgEl("circle", {
              cx: n.x + GW - 11 + 5, cy: n.y + GH / 2, r: 5, class: "ls-gate"
            }));
          }
          var gt = svgEl("text", { x: n.x + 26, y: n.y - 6, class: "ls-gate-label" });
          gt.textContent = n.type;
          g.appendChild(gt);
          var del = svgEl("text", { x: n.x + GW + 6, y: n.y - 4, class: "ls-del" });
          del.textContent = "x";
          del.addEventListener("click", function (ev) {
            ev.stopPropagation();
            wires = wires.filter(function (w) {
              return w.from !== n.id && w.to !== n.id;
            });
            nodes.splice(nodes.indexOf(n), 1);
            draw();
          });
          g.appendChild(del);
        }

        p.ins.forEach(function (pin, i) {
          var c = svgEl("circle", { cx: pin.x, cy: pin.y, r: 6, class: "ls-port ls-in" });
          c.addEventListener("pointerup", function (ev) {
            ev.stopPropagation();
            if (wiring) { connect(wiring.from, n.id, i); wiring = null; }
          });
          c.addEventListener("click", function (ev) {
            ev.stopPropagation();
            if (wiring) { connect(wiring.from, n.id, i); wiring = null; }
          });
          g.appendChild(c);
        });
        if (p.out) {
          var oc = svgEl("circle", { cx: p.out.x, cy: p.out.y, r: 6, class: "ls-port ls-out" });
          oc.addEventListener("pointerdown", function (ev) {
            ev.stopPropagation();
            ev.preventDefault();
            wiring = { from: n.id, x: p.out.x, y: p.out.y };
          });
          g.appendChild(oc);
        }
        svg.appendChild(g);
      });

      renderTable();
    }

    function renderTable() {
      var ins = inputs();
      var o = outNode();
      var rows = Math.pow(2, ins.length);
      var table = document.createElement("table");
      var thead = document.createElement("thead");
      var hr = document.createElement("tr");
      ins.forEach(function (n) {
        var th = document.createElement("th");
        th.textContent = n.label;
        hr.appendChild(th);
      });
      var thq = document.createElement("th");
      thq.textContent = "Q";
      hr.appendChild(thq);
      thead.appendChild(hr);
      table.appendChild(thead);

      var tbody = document.createElement("tbody");
      var complete = true;
      for (var r = 0; r < rows; r++) {
        var env = {};
        var tr = document.createElement("tr");
        for (var i = 0; i < ins.length; i++) {
          var bit = (r >> (ins.length - 1 - i)) & 1;
          env[ins[i].label] = bit;
          var td = document.createElement("td");
          td.textContent = String(bit);
          tr.appendChild(td);
        }
        var q = o ? value(o.id, env, {}) : null;
        if (q === null) complete = false;
        var tdq = document.createElement("td");
        tdq.className = "ls-q" + (q === 1 ? " is-on" : "");
        tdq.textContent = q === null ? "?" : String(q);
        tr.appendChild(tdq);
        tbody.appendChild(tr);
      }
      table.appendChild(tbody);
      tableWrap.textContent = "";
      tableWrap.appendChild(table);

      var e = o ? expr(o.id, {}) : "?";
      if (!complete || e.indexOf("?") >= 0) {
        exprLine.className = "tool-status";
        exprLine.textContent = "Wire every gate input and the output Q to see the "
          + "expression and a full truth table.";
      } else {
        exprLine.className = "tool-status is-good";
        exprLine.textContent = "Q = " + e.replace(/^\(|\)$/g, "");
      }
    }

    reset(2);
    /* A worked starting circuit: Q = A AND B, so the tool is useful on load. */
    var g0 = add({ kind: "gate", type: "AND", x: 260, y: 150 });
    wires.push({ from: nodes[0].id, to: g0.id, port: 0 });
    wires.push({ from: nodes[1].id, to: g0.id, port: 1 });
    wires.push({ from: g0.id, to: outNode().id, port: 0 });
    draw();
  }

  var mounts = document.querySelectorAll('.tool[data-tool="logic-simulator"] .tool-body');
  for (var i = 0; i < mounts.length; i++) build(mounts[i]);
})();
