/* Flowcharts: a structured model, drawn with the standard symbols and run by
 * turning it into pseudocode.
 *
 * A flowchart is a list of nodes, top to bottom:
 *   {id, t: "start"|"end", text}
 *   {id, t: "io", text, code}          parallelogram: input or output
 *   {id, t: "process", text, code}     rectangle: a calculation or an action
 *   {id, t: "decision", text, code, yes: [nodes], no: [nodes]}   diamond, two labelled branches
 *   {id, t: "while", text, code, body: [nodes]}  diamond tested first: Yes runs the body and loops back
 *   {id, t: "until", text, code, body: [nodes]}  body first, then the diamond: No loops back
 *   {id, t: "slot", slot}              an empty box the student fills
 * CT.flow.code turns it into pseudocode and remembers which node each line came
 * from, so a run can light up the symbol being carried out. Everything here is
 * plain strings, so the checks can run it under Node.
 */
(function (root) {
  "use strict";
  var CT = root.CT = root.CT || {};

  var BW = 200, BH = 48, DW = 210, DH = 84, GAP = 30, BR = 36, LANE = 26;

  function esc(s) { return String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;").replace(/"/g, "&quot;"); }
  function wrap(text, max) {
    var words = String(text).split(" "), lines = [], cur = "";
    words.forEach(function (w) {
      if ((cur + " " + w).trim().length > max && cur) { lines.push(cur); cur = w; } else cur = (cur + " " + w).trim();
    });
    if (cur) lines.push(cur);
    return lines;
  }

  // ------------------------------------------------------------ to code
  function code(flow) {
    var lines = [], map = [];
    function emit(text, id, depth) { lines.push(new Array(depth + 1).join("    ") + text); map.push(id); }
    function seq(list, depth) {
      (list || []).forEach(function (n) {
        if (n.t === "start" || n.t === "end") return;
        if (n.t === "slot") { emit("// empty box", n.id, depth); return; }
        if (n.t === "io" || n.t === "process") { String(n.code).split("\n").forEach(function (c) { emit(c, n.id, depth); }); return; }
        if (n.t === "decision") {
          emit("if " + n.code + " then", n.id, depth);
          seq(n.yes, depth + 1);
          if (n.no && n.no.length) { emit("else", n.id, depth); seq(n.no, depth + 1); }
          emit("endif", n.id, depth);
          return;
        }
        if (n.t === "while") { emit("while " + n.code, n.id, depth); seq(n.body, depth + 1); emit("endwhile", n.id, depth); return; }
        if (n.t === "until") { emit("do", n.id, depth); seq(n.body, depth + 1); emit("until " + n.code, n.id, depth); }
      });
    }
    seq(flow, 0);
    return { text: lines.join("\n"), map: map };
  }

  // Run a flowchart with test inputs (and engine commands, if any).
  function run(flow, opts) {
    var c = code(flow);
    var r = CT.pseudo.run(c.text, opts || {});
    if (r.error) r.error.node = c.map[r.error.line - 1];
    return r;
  }

  // -------------------------------------------------------------- layout
  function size(n) {
    if (n.t === "decision") {
      var y = sizeSeq(n.yes), no = sizeSeq(n.no), col = Math.max(BW, y.w, no.w);
      return { w: col * 2 + BR, h: DH + GAP + Math.max(y.h, no.h) + GAP, col: col };
    }
    if (n.t === "while") { var b = sizeSeq(n.body); return { w: Math.max(DW, b.w) + LANE * 4, h: DH + GAP + b.h + GAP * 1.5 }; }
    if (n.t === "until") { var u = sizeSeq(n.body); return { w: Math.max(DW, u.w) + LANE * 4, h: GAP / 2 + u.h + GAP + DH }; }
    return { w: BW, h: BH };
  }
  function sizeSeq(list) {
    var w = 0, h = 0;
    (list || []).forEach(function (n, i) { var s = size(n); w = Math.max(w, s.w); h += s.h + (i ? GAP : 0); });
    return { w: w, h: h };
  }

  function arrow(x1, y1, x2, y2) { return '<path class="fc-line" d="M' + x1 + " " + y1 + " L" + x2 + " " + y2 + '" marker-end="url(#fc-head)"/>'; }
  function path(d, head) { return '<path class="fc-line" d="' + d + '"' + (head ? ' marker-end="url(#fc-head)"' : "") + "/>"; }
  function label(x, y, t, anchor) { return '<text class="fc-yn" x="' + x + '" y="' + y + '" text-anchor="' + (anchor || "middle") + '">' + t + "</text>"; }
  function textLines(cx, cy, text, max, cls) {
    var ls = wrap(text, max), out = "", lh = 15, top = cy - (ls.length - 1) * lh / 2 + 5;
    ls.forEach(function (l, i) { out += '<text class="fc-t' + (cls ? " " + cls : "") + '" x="' + cx + '" y="' + (top + i * lh) + '">' + esc(l) + "</text>"; });
    return out;
  }

  // Draw a node with its top centre at (cx, y); returns { svg, bottom }.
  function drawNode(n, cx, y, o) {
    var attrs = ' data-node="' + n.id + '" class="fc-node fc-' + n.t + (o.on === n.id ? " is-on" : "") + (o.picked === n.id ? " is-picked" : "") +
      (o.path && o.path[n.id] ? " is-path" : "") + (n.empty ? " is-empty" : "") +
      (o.bad && o.bad[n.id] ? " is-bad" : "") + '"' + (o.clickable ? ' tabindex="0" role="button" aria-label="' + esc((n.t === "slot" ? "Empty box" : n.text)) + '"' : "");
    var s = "";
    if (n.t === "start" || n.t === "end") {
      s = "<g" + attrs + '><rect class="fc-shape" x="' + (cx - 70) + '" y="' + y + '" width="140" height="' + BH + '" rx="' + BH / 2 + '"/>' + textLines(cx, y + BH / 2, n.text, 18) + "</g>";
      return { svg: s, bottom: y + BH };
    }
    if (n.t === "io") {
      var k = 16;
      s = "<g" + attrs + '><path class="fc-shape" d="M' + (cx - BW / 2 + k) + " " + y + " H" + (cx + BW / 2) + " L" + (cx + BW / 2 - k) + " " + (y + BH) +
        " H" + (cx - BW / 2) + ' Z"/>' + textLines(cx, y + BH / 2, n.text, 22) + "</g>";
      return { svg: s, bottom: y + BH };
    }
    if (n.t === "process" || n.t === "slot") {
      var empty = n.t === "slot" || n.empty;
      s = "<g" + attrs + ' data-slot="' + (n.slot || "") + '"><rect class="fc-shape' + (empty ? " fc-empty" : "") + '" x="' + (cx - BW / 2) + '" y="' + y + '" width="' + BW + '" height="' + BH + '" rx="' + (n.t === "slot" ? 10 : 2) + '"/>' +
        textLines(cx, y + BH / 2, n.t === "slot" ? (n.label || "?") : n.text, 24, n.t === "slot" ? "fc-q" : "") + "</g>";
      return { svg: s, bottom: y + BH };
    }
    if (n.t === "decision") {
      var sz = size(n), col = sz.col, lx = cx - col / 2 - BR / 2, rx = cx + col / 2 + BR / 2, my = y + DH / 2;
      s += "<g" + attrs + '><path class="fc-shape" d="M' + cx + " " + y + " L" + (cx + DW / 2) + " " + my + " L" + cx + " " + (y + DH) + " L" + (cx - DW / 2) + " " + my + ' Z"/>' +
        textLines(cx, my, n.text || n.label || "?", 16, n.empty ? "fc-q" : "") + "</g>";
      var top = y + DH + GAP;
      s += path("M" + (cx - DW / 2) + " " + my + " H" + lx + " V" + top, (n.yes || []).length > 0) + label(cx - DW / 2 - 6, my - 8, "Yes", "end");
      s += path("M" + (cx + DW / 2) + " " + my + " H" + rx + " V" + top, (n.no || []).length > 0) + label(cx + DW / 2 + 6, my - 8, "No", "start");
      var a = drawSeq(n.yes, lx, top, o), b = drawSeq(n.no, rx, top, o);
      var join = Math.max(a.bottom, b.bottom) + GAP / 2;
      s += a.svg + b.svg + path("M" + lx + " " + a.bottom + " V" + join + " H" + rx + " V" + b.bottom) + path("M" + cx + " " + join + " V" + (join + 1));
      s += '<circle class="fc-dot" cx="' + cx + '" cy="' + join + '" r="4"/>';
      return { svg: s, bottom: join };
    }
    if (n.t === "while") {
      var wsz = size(n), my2 = y + DH / 2, left = cx - wsz.w / 2 + LANE, right = cx + wsz.w / 2 - LANE;
      s += "<g" + attrs + '><path class="fc-shape" d="M' + cx + " " + y + " L" + (cx + DW / 2) + " " + my2 + " L" + cx + " " + (y + DH) + " L" + (cx - DW / 2) + " " + my2 + ' Z"/>' +
        textLines(cx, my2, n.text || n.label || "?", 16, n.empty ? "fc-q" : "") + "</g>";
      var bodyTop = y + DH + GAP, body = drawSeq(n.body, cx, bodyTop, o);
      s += arrow(cx, y + DH, cx, bodyTop) + label(cx + 8, y + DH + 18, "Yes", "start") + body.svg;
      var back = body.bottom + GAP / 2, exit = back + GAP;
      s += path("M" + cx + " " + body.bottom + " V" + back + " H" + left + " V" + my2 + " H" + (cx - DW / 2), true);
      s += path("M" + (cx + DW / 2) + " " + my2 + " H" + right + " V" + exit + " H" + cx) + label(cx + DW / 2 + 6, my2 - 8, "No", "start");
      return { svg: s, bottom: exit };
    }
    if (n.t === "until") {
      var usz = size(n), lft = cx - usz.w / 2 + LANE, startY = y + GAP / 2;
      var ub = drawSeq(n.body, cx, startY, o), dy = ub.bottom + GAP, my3 = dy + DH / 2;
      s += path("M" + cx + " " + y + " V" + startY, true) + '<circle class="fc-dot" cx="' + cx + '" cy="' + (y + GAP / 4) + '" r="4"/>' + ub.svg + arrow(cx, ub.bottom, cx, dy);
      s += "<g" + attrs + '><path class="fc-shape" d="M' + cx + " " + dy + " L" + (cx + DW / 2) + " " + my3 + " L" + cx + " " + (dy + DH) + " L" + (cx - DW / 2) + " " + my3 + ' Z"/>' +
        textLines(cx, my3, n.text || n.label || "?", 16, n.empty ? "fc-q" : "") + "</g>";
      s += path("M" + (cx - DW / 2) + " " + my3 + " H" + lft + " V" + (y + GAP / 4) + " H" + (cx - 5), true) + label(cx - DW / 2 - 6, my3 - 8, "No", "end");
      s += label(cx + 8, dy + DH + 16, "Yes", "start");
      return { svg: s, bottom: dy + DH };
    }
    return { svg: "", bottom: y };
  }
  function drawSeq(list, cx, y, o) {
    var s = "", cur = y;
    (list || []).forEach(function (n, i) {
      // a repeat-until block draws its own way in, where the loop joins it
      if (i) { s += n.t === "until" ? path("M" + cx + " " + cur + " V" + (cur + GAP)) : arrow(cx, cur, cx, cur + GAP); cur += GAP; }
      var r = drawNode(o.fill && n.t === "slot" && o.fill[n.slot] ? Object.assign({}, o.fill[n.slot], { id: n.id, slot: n.slot, filled: true }) : n, cx, cur, o);
      s += r.svg; cur = r.bottom;
    });
    return { svg: s, bottom: cur };
  }

  // The whole chart as an SVG string. o: { on, picked, bad, path, clickable, label }
  function svg(flow, o) {
    o = o || {};
    var sz = sizeSeq(flow), w = Math.max(sz.w + 40, 260), h = sz.h + 40;
    var body = drawSeq(flow, w / 2, 20, o);
    return '<svg class="fc" viewBox="0 0 ' + w + " " + h + '" role="img" aria-label="' + esc(o.label || "Flowchart") + '" style="max-width:' + Math.round(w * 1.1) + 'px">' +
      '<defs><marker id="fc-head" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" class="fc-headfill"/></marker></defs>' +
      body.svg + "</svg>";
  }

  // Every node in a chart, depth first.
  function nodes(flow) {
    var out = [];
    (function walk(list) {
      (list || []).forEach(function (n) { out.push(n); walk(n.yes); walk(n.no); walk(n.body); });
    })(flow);
    return out;
  }
  // A copy with one node swapped for another.
  function replace(flow, id, withNode) {
    return (flow || []).map(function (n) {
      if (n.id === id) return Object.assign({}, n, withNode, { id: n.id, yes: n.yes, no: n.no, body: n.body });
      var c = Object.assign({}, n);
      if (n.yes) c.yes = replace(n.yes, id, withNode);
      if (n.no) c.no = replace(n.no, id, withNode);
      if (n.body) c.body = replace(n.body, id, withNode);
      return c;
    });
  }
  // A copy with each slot filled by its card.
  function filled(flow, fill) {
    return (flow || []).map(function (n) {
      if (n.t === "slot") return fill && fill[n.slot] ? Object.assign({}, fill[n.slot], { id: n.id, slot: n.slot }) : n;
      var c = Object.assign({}, n);
      if (n.yes) c.yes = filled(n.yes, fill);
      if (n.no) c.no = filled(n.no, fill);
      if (n.body) c.body = filled(n.body, fill);
      return c;
    });
  }

  // Run the test cases; each test is {inputs, expect: [lines]}.
  function test(flow, tests, opts) {
    return tests.map(function (t) {
      var r = run(flow, Object.assign({ inputs: t.inputs || [], maxSteps: 3000, quiet: true }, opts || {}));
      var got = r.output;
      return { inputs: t.inputs || [], expect: t.expect, got: r.ok ? got : null, error: r.error, pass: r.ok && got.join("\n") === t.expect.join("\n") };
    });
  }

  CT.flow = { code: code, run: run, svg: svg, nodes: nodes, replace: replace, filled: filled, test: test, wrap: wrap };
})(typeof window !== "undefined" ? window : globalThis);
