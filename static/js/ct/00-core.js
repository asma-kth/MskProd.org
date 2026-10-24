/* Computational Thinking Adventure: shared helpers.
 *
 * Every file in static/js/ct/ adds to one CT namespace and is bundled, in file
 * name order, into /assets/js/ct.js. Files that hold pure logic (checkers, the
 * pseudocode interpreter, the simulations) touch no DOM when they load, so
 * tools/check_ct.mjs can run them under Node.
 */
(function (root) {
  "use strict";
  var CT = root.CT = root.CT || {};
  CT.engines = CT.engines || {};   // name -> { mount(host, level, api) }
  CT.check = CT.check || {};       // name -> function (data, answer) -> result
  CT.solve = CT.solve || {};       // name -> function (data) -> the model answer

  CT.el = function (tag, attrs, kids) {
    var n = document.createElement(tag);
    if (attrs) {
      for (var k in attrs) {
        if (!Object.prototype.hasOwnProperty.call(attrs, k) || attrs[k] === null || attrs[k] === undefined || attrs[k] === false) continue;
        var v = attrs[k];
        if (k === "class") n.className = v;
        else if (k === "text") n.textContent = v;
        else if (k === "html") n.innerHTML = v;
        else if (k.slice(0, 2) === "on" && typeof v === "function") n.addEventListener(k.slice(2), v);
        else if (k === "style" && typeof v === "object") { for (var s in v) n.style.setProperty(s, v[s]); }
        else n.setAttribute(k, v === true ? "" : v);
      }
    }
    CT.append(n, kids);
    return n;
  };

  CT.svg = function (tag, attrs, kids) {
    var n = document.createElementNS("http://www.w3.org/2000/svg", tag);
    if (attrs) {
      for (var k in attrs) {
        if (!Object.prototype.hasOwnProperty.call(attrs, k) || attrs[k] === null || attrs[k] === undefined || attrs[k] === false) continue;
        if (k === "text") n.textContent = attrs[k];
        else if (k.slice(0, 2) === "on" && typeof attrs[k] === "function") n.addEventListener(k.slice(2), attrs[k]);
        else n.setAttribute(k, attrs[k]);
      }
    }
    CT.append(n, kids);
    return n;
  };

  CT.append = function (n, kids) {
    if (kids === null || kids === undefined || kids === false) return n;
    if (!Array.isArray(kids)) kids = [kids];
    kids.forEach(function (c) {
      if (c === null || c === undefined || c === false) return;
      if (Array.isArray(c)) { CT.append(n, c); return; }
      n.appendChild(typeof c === "string" || typeof c === "number" ? document.createTextNode(String(c)) : c);
    });
    return n;
  };

  CT.clear = function (n) { while (n && n.firstChild) n.removeChild(n.firstChild); return n; };

  // A small seeded generator, so a shuffled board is the same every time a
  // level opens and a teacher sees what a student sees.
  CT.rng = function (seed) {
    var s = (typeof seed === "string") ? CT.hash(seed) : (seed >>> 0);
    return function () {
      s |= 0; s = s + 0x6D2B79F5 | 0;
      var t = Math.imul(s ^ s >>> 15, 1 | s);
      t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t;
      return ((t ^ t >>> 14) >>> 0) / 4294967296;
    };
  };
  CT.hash = function (str) {
    var h = 2166136261;
    for (var i = 0; i < str.length; i++) { h ^= str.charCodeAt(i); h = Math.imul(h, 16777619); }
    return h >>> 0;
  };
  CT.shuffle = function (arr, rand) {
    var a = arr.slice();
    rand = rand || Math.random;
    for (var i = a.length - 1; i > 0; i--) {
      var j = Math.floor(rand() * (i + 1)), t = a[i]; a[i] = a[j]; a[j] = t;
    }
    return a;
  };
  // Shuffle, but never hand back the solved order.
  CT.scramble = function (arr, rand, same) {
    var a = arr.slice();
    for (var tries = 0; tries < 20; tries++) {
      a = CT.shuffle(arr, rand);
      if (!(same || CT.sameOrder)(a, arr)) return a;
    }
    return a.slice(1).concat(a.slice(0, 1));
  };
  CT.sameOrder = function (a, b) {
    if (a.length !== b.length) return false;
    for (var i = 0; i < a.length; i++) if (a[i] !== b[i]) return false;
    return true;
  };

  CT.byId = function (list, id) {
    for (var i = 0; i < list.length; i++) if (list[i].id === id) return list[i];
    return null;
  };
  CT.clamp = function (v, lo, hi) { return Math.max(lo, Math.min(hi, v)); };

  // One polite live region for the whole adventure: feedback, moves, results.
  CT.announce = function (msg) {
    if (typeof document === "undefined") return;
    var r = document.getElementById("ct-live");
    if (!r) return;
    r.textContent = "";
    setTimeout(function () { r.textContent = msg; }, 30);
  };

  // Motion: the reader's own setting, which the student can also switch off.
  CT.calm = function () {
    if (typeof document === "undefined") return true;
    var app = document.getElementById("ct-app");
    return !app || app.getAttribute("data-motion") !== "full";
  };
  CT.wait = function (ms, fn) { return setTimeout(fn, CT.calm() ? Math.min(ms, 60) : ms); };

  // Simple event hub between the shell, the views and the engines.
  var subs = {};
  CT.on = function (name, fn) { (subs[name] = subs[name] || []).push(fn); };
  CT.emit = function (name, payload) { (subs[name] || []).forEach(function (fn) { fn(payload); }); };
})(typeof window !== "undefined" ? window : globalThis);
