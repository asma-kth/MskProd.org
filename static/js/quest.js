/* The Media Realms: an adventure through Creative iMedia R093, topic by topic.

   One page. The places, monsters and questions are built from the R093 lessons
   at build time (content/imedia_quest) and arrive as JSON in #mq-data. Each
   place is one R093 lesson: talk to its guide, win two battles and beat its
   guardian, and the next place opens. A spell only lands when its question is
   answered correctly, and every answer shows the reason.

   Progress lives only in this browser (localStorage, key mskprod:realms). */
(function () {
  "use strict";

  var app = document.getElementById("mq-app");
  var dataNode = document.getElementById("mq-data");
  if (!app || !dataNode) return;
  var D = JSON.parse(dataNode.textContent);
  var KEY = "mskprod:realms";
  var P = D.places;
  var EL = D.elements;
  var ELS = ["ink", "light", "sound", "spark"];

  /* ------------------------------------------------------------ helpers */
  function el(tag, attrs, kids) {
    var n = document.createElement(tag);
    Object.keys(attrs || {}).forEach(function (k) {
      var v = attrs[k];
      if (v === null || v === undefined || v === false) return;
      if (k === "text") n.textContent = v;
      else if (k === "html") n.innerHTML = v;
      else if (k === "on") Object.keys(v).forEach(function (e) { n.addEventListener(e, v[e]); });
      else n.setAttribute(k, v === true ? "" : v);
    });
    (kids || []).forEach(function (c) {
      if (c === null || c === undefined || c === false) return;
      n.appendChild(typeof c === "string" ? document.createTextNode(c) : c);
    });
    return n;
  }
  function btn(cls, label, fn, attrs) {
    var b = el("button", Object.assign({ type: "button", "class": cls }, attrs || {}));
    if (typeof label === "string") b.innerHTML = label; else if (label) b.appendChild(label);
    if (fn) b.addEventListener("click", fn);
    return b;
  }
  function esc(s) { return String(s).replace(/[&<>"]/g, function (c) { return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]; }); }
  function plain(h) { var d = document.createElement("div"); d.innerHTML = h; return d.textContent; }
  function shuffle(a) {
    a = a.slice();
    for (var i = a.length - 1; i > 0; i--) { var j = Math.floor(Math.random() * (i + 1)); var t = a[i]; a[i] = a[j]; a[j] = t; }
    return a;
  }
  function pick(a) { return a[Math.floor(Math.random() * a.length)]; }
  function fmt(n) { return Math.round(n).toLocaleString("en-GB"); }
  var motionQ = window.matchMedia ? window.matchMedia("(prefers-reduced-motion: reduce)") : { matches: false };
  function calm() { return !!motionQ.matches; }
  function wait(ms) { return calm() ? Math.min(ms, 120) : ms; }
  var timers = [];
  function later(ms, fn) { var t = setTimeout(fn, wait(ms)); timers.push(t); return t; }
  function clearTimers() { timers.forEach(clearTimeout); timers = []; }

  /* --------------------------------------------------------------- icons */
  var ICONS = {
    map: '<path d="M3 6l6-2 6 2 6-2v14l-6 2-6-2-6 2z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M9 4v14M15 6v14" stroke="currentColor" stroke-width="2"/>',
    paw: '<circle cx="7" cy="9" r="2.2" fill="currentColor"/><circle cx="12" cy="6.5" r="2.2" fill="currentColor"/><circle cx="17" cy="9" r="2.2" fill="currentColor"/><path d="M12 11c-3.5 0-6 3.5-6 6 0 2 1.6 3 3.2 3 1.2 0 1.8-.7 2.8-.7s1.6.7 2.8.7c1.6 0 3.2-1 3.2-3 0-2.5-2.5-6-6-6z" fill="currentColor"/>',
    bag: '<path d="M5 8h14l-1 12H6z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M9 8V6a3 3 0 016 0v2" fill="none" stroke="currentColor" stroke-width="2"/>',
    book: '<path d="M4 5c3-1 6-1 8 1 2-2 5-2 8-1v14c-3-1-6-1-8 1-2-2-5-2-8-1z" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round"/><path d="M12 6v14" stroke="currentColor" stroke-width="2"/>',
    gear: '<circle cx="12" cy="12" r="3.2" fill="none" stroke="currentColor" stroke-width="2"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M4.9 19.1L7 17M17 7l2.1-2.1" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
    sound: '<path d="M4 9h4l5-4v14l-5-4H4z" fill="currentColor"/><path d="M16 8a5 5 0 010 8M18.5 5.5a8.5 8.5 0 010 13" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
    mute: '<path d="M4 9h4l5-4v14l-5-4H4z" fill="currentColor"/><path d="M16 9l5 6M21 9l-5 6" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
    coin: '<circle cx="12" cy="12" r="9" fill="#FBBF24" stroke="#B45309" stroke-width="2"/><path d="M12 7v10M9.5 9.5h4a1.6 1.6 0 010 3.2h-3a1.6 1.6 0 000 3.2h4" fill="none" stroke="#B45309" stroke-width="1.8" stroke-linecap="round"/>',
    potion: '<path d="M10 3h4v4l4 6a5 5 0 01-4.3 8h-3.4A5 5 0 016 13l4-6z" fill="#F472B6" stroke="#831843" stroke-width="1.8" stroke-linejoin="round"/><path d="M9 3h6" stroke="#831843" stroke-width="2" stroke-linecap="round"/><circle cx="11" cy="15" r="1.4" fill="#fff" opacity=".8"/>',
    star: '<path d="M12 2.5l2.9 6 6.6.9-4.8 4.6 1.2 6.5L12 17.4l-5.9 3.1 1.2-6.5L2.5 9.4l6.6-.9z" fill="currentColor"/>',
    lock: '<rect x="5" y="10" width="14" height="10" rx="2" fill="currentColor"/><path d="M8 10V7a4 4 0 018 0v3" fill="none" stroke="currentColor" stroke-width="2"/>',
    check: '<path d="M5 12.5l4.5 4.5L19 7.5" fill="none" stroke="currentColor" stroke-width="2.8" stroke-linecap="round" stroke-linejoin="round"/>',
    heart: '<path d="M12 20s-7.5-4.6-7.5-10A4.5 4.5 0 0112 7a4.5 4.5 0 017.5 3c0 5.4-7.5 10-7.5 10z" fill="currentColor"/>',
    back: '<path d="M15 5l-7 7 7 7" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>',
    next: '<path d="M9 5l7 7-7 7" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round"/>',
    run: '<path d="M13 4a2 2 0 11-.1 0zM9 21l2-6 3 2v5M8 12l3-4 4 2 3 3M11 8l-1 5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>',
    flag: '<path d="M6 21V4M6 4h11l-2 4 2 4H6" fill="none" stroke="currentColor" stroke-width="2" stroke-linejoin="round" stroke-linecap="round"/>',
    mend: '<path d="M12 21s-7.5-4.6-7.5-10A4.5 4.5 0 0112 8a4.5 4.5 0 017.5 3c0 5.4-7.5 10-7.5 10z" fill="currentColor"/><path d="M12 11v6M9 14h6" stroke="#fff" stroke-width="2" stroke-linecap="round"/>',
    ink: '<path d="M12 3c3 5 6 8 6 11a6 6 0 01-12 0c0-3 3-6 6-11z" fill="currentColor"/>',
    light: '<circle cx="12" cy="12" r="4.5" fill="currentColor"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M5 5l2 2M17 17l2 2M5 19l2-2M17 7l2-2" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>',
    sound2: '<path d="M3 12h2M7 8v8M11 5v14M15 8v8M19 10v4" stroke="currentColor" stroke-width="2.4" stroke-linecap="round"/>',
    spark: '<path d="M13 2L5 13h6l-1 9 8-11h-6z" fill="currentColor"/>'
  };
  function ico(name, cls) {
    var body = ICONS[name === "sound" && cls === "el" ? "sound2" : name] || "";
    return '<svg class="mq-i' + (cls ? " mq-i-" + cls : "") + '" viewBox="0 0 24 24" aria-hidden="true" focusable="false">' + body + "</svg>";
  }
  function elIco(e) { return ico(e === "sound" ? "sound2" : e, "el"); }

  /* --------------------------------------------------------------- store */
  var store = {
    get: function () { try { return JSON.parse(localStorage.getItem(KEY) || "null"); } catch (e) { return null; } },
    set: function (v) { try { localStorage.setItem(KEY, JSON.stringify(v)); } catch (e) { /* the game still runs without storage */ } },
    clear: function () { try { localStorage.removeItem(KEY); } catch (e) { /* nothing stored */ } }
  };
  function fresh() {
    return { v: 1, name: "", look: { robe: "purple", hat: "pointed", wand: "oak", skin: 2, hair: "brown" },
             xp: 0, coins: 0, items: { draught: 1, elixir: 0, biscuit: 0 },
             owned: { hat: [], robe: [], wand: [] }, pets: {}, pet: "", places: {}, seen: {},
             final: 0, free: false, sound: false, told: false };
  }
  var S = store.get();
  if (!S || S.v !== 1) S = null;
  if (S) S = Object.assign(fresh(), S);
  function save() { if (S) store.set(S); }

  /* ------------------------------------------------------------- numbers */
  function levelOf(xp) { var L = 1; while (50 * L * (L + 1) <= xp && L < 60) L++; return L; }
  function levelStart(L) { return 50 * (L - 1) * L; }
  function maxHp(L) { return 90 + 10 * L; }
  function spellDmg(L) { return 22 + 4 * L; }
  function mendAmount(L) { return 30 + 4 * L; }
  function petLevel(xp) { return Math.min(20, 1 + Math.floor((xp || 0) / 40)); }
  function petStage(L) { return L >= 8 ? 2 : L >= 4 ? 1 : 0; }
  function placeIndex(p) { return P.indexOf(p); }
  /* Monsters grow with the wizard, so a battle always asks about the same number of
     questions: four right answers on the weak spot for a wild monster, six for a
     guardian and about ten for the Great Static. Levelling up still means more
     energy, bigger numbers and a stronger pet. */
  var HITS = { wild: 4, guardian: 6, final: 11 };
  function foeHp(kind, i, L) { return Math.ceil(HITS[kind] * spellDmg(L) * 1.5 * (1 + i / 100) / 5) * 5; }
  function foeHit(kind, i, L) { return (kind === "final" ? 26 + 3 * L : kind === "guardian" ? 20 + i + 2 * L : 16 + i + 2 * L); }
  var WIN_XP = { wild: 30, guardian: 70, final: 200 };
  var WIN_COINS = { wild: 15, guardian: 40, final: 150 };
  var PET_XP = { wild: 20, guardian: 40, final: 80 };
  function freeOwned(kind) { return (D.shop[kind] || []).filter(function (x) { return !x.price; }).map(function (x) { return x.id; }); }
  function owns(kind, id) { return freeOwned(kind).indexOf(id) > -1 || (S.owned[kind] || []).indexOf(id) > -1; }
  function shopItem(kind, id) { return (D.shop[kind] || []).filter(function (x) { return x.id === id; })[0]; }

  /* ---------------------------------------------------------------- pets */
  function starter(id) { return D.starters.filter(function (s) { return s.id === id; })[0]; }
  function guardianOf(id) {
    for (var i = 0; i < P.length; i++) if (P[i].monsters[2].id === id) return { m: P[i].monsters[2], place: P[i] };
    return null;
  }
  function petInfo(id) {
    var rec = (S && S.pets[id]) || { xp: 0 }, L = petLevel(rec.xp);
    var st = starter(id);
    if (st) return { id: id, el: st.el, name: st.stages[petStage(L)], stage: petStage(L), level: L, xp: rec.xp, art: st.art, about: st.about, starter: true };
    var g = guardianOf(id);
    if (g) return { id: id, el: g.m.el, name: g.m.tamed, stage: 1, level: L, xp: rec.xp, art: g.m.art, about: "Once " + g.m.name + ". Cleared at " + g.place.name + ".", starter: false };
    return null;
  }
  function petDmg(info) { return 20 + 3 * info.level; }

  /* ------------------------------------------------------------ progress */
  function stars(p) { return (S.places[p.id] || [0, 0, 0]); }
  function cleared(p) { return stars(p)[2] > 0; }
  function unlocked(p) {
    if (S.free) return true;
    var i = placeIndex(p);
    return i === 0 || cleared(P[i - 1]);
  }
  function battleOpen(p, n) { return unlocked(p) && (S.free || n === 0 || stars(p)[n - 1] > 0); }
  function clearedCount() { return P.filter(cleared).length; }
  function finalOpen() { return S.free || clearedCount() === P.length; }
  function realm(id) { return D.realms.filter(function (r) { return r.id === id; })[0]; }
  function place(id) { return P.filter(function (p) { return p.id === id; })[0]; }

  /* --------------------------------------------------------------- sound */
  var actx = null;
  function audio() {
    if (!actx) { var A = window.AudioContext || window.webkitAudioContext; if (!A) return null; try { actx = new A(); } catch (e) { return null; } }
    if (actx.state === "suspended") actx.resume();
    return actx;
  }
  function tone(f, start, dur, type, vol, slide) {
    var a = audio(); if (!a) return;
    var o = a.createOscillator(), g = a.createGain(), t = a.currentTime + start;
    o.type = type || "triangle"; o.frequency.setValueAtTime(f, t);
    if (slide) o.frequency.exponentialRampToValueAtTime(slide, t + dur);
    g.gain.setValueAtTime(0.0001, t); g.gain.exponentialRampToValueAtTime(vol || 0.08, t + 0.02);
    g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    o.connect(g); g.connect(a.destination); o.start(t); o.stop(t + dur + 0.05);
  }
  var SOUNDS = {
    tap: function () { tone(880, 0, 0.05, "triangle", 0.04); },
    cast: function () { tone(440, 0, 0.35, "sawtooth", 0.05, 1320); },
    hit: function () { tone(180, 0, 0.18, "square", 0.07, 90); tone(660, 0.05, 0.12, "triangle", 0.05); },
    hurt: function () { tone(220, 0, 0.25, "sine", 0.09, 110); },
    heal: function () { [523, 659, 784].forEach(function (f, i) { tone(f, i * 0.07, 0.2, "sine", 0.06); }); },
    good: function () { tone(659, 0, 0.1); tone(988, 0.08, 0.18); },
    bad: function () { tone(233, 0, 0.18, "sine", 0.08); tone(185, 0.12, 0.24, "sine", 0.07); },
    pet: function () { [784, 988, 1175, 1568].forEach(function (f, i) { tone(f, i * 0.06, 0.16, "square", 0.04); }); },
    win: function () { [523, 659, 784, 1046, 784, 1046, 1318].forEach(function (f, i) { tone(f, i * 0.11, 0.26, "triangle", 0.08); }); },
    level: function () { [392, 523, 659, 784, 1046].forEach(function (f, i) { tone(f, i * 0.09, 0.3, "triangle", 0.07); }); },
    lose: function () { [392, 330, 262].forEach(function (f, i) { tone(f, i * 0.18, 0.3, "sine", 0.07); }); },
    coin: function () { tone(1318, 0, 0.08, "square", 0.04); tone(1760, 0.07, 0.12, "square", 0.04); }
  };
  function sfx(name) { if (S && S.sound && SOUNDS[name]) { try { SOUNDS[name](); } catch (e) { /* sound is a nicety */ } } }

  /* ----------------------------------------------------------------- art */
  var uid = 0;
  var ROBE = {};
  D.shop.robe.forEach(function (r) { ROBE[r.id] = r; });

  function wizardSvg(look, o) {
    o = o || {};
    uid += 1;
    var r = ROBE[look.robe] || ROBE.purple;
    var skin = D.skins[look.skin] || D.skins[2];
    var hair = D.hairs[look.hair] || D.hairs.brown;
    var g = "mqr" + uid;
    var fill = look.robe === "rainbow" ? "url(#" + g + ")" : r.c;
    var cast = o.pose === "cast";
    var s = ['<svg class="mq-wiz' + (o.cls ? " " + o.cls : "") + '" viewBox="0 0 100 132" aria-hidden="true" focusable="false">'];
    if (look.robe === "rainbow") {
      s.push('<defs><linearGradient id="' + g + '" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#EC4899"/><stop offset=".35" stop-color="#F59E0B"/><stop offset=".65" stop-color="#22C55E"/><stop offset="1" stop-color="#6366F1"/></linearGradient></defs>');
    }
    s.push('<ellipse cx="50" cy="126" rx="28" ry="5" fill="#000" opacity=".22"/>');
    if (look.hat === "hood") s.push('<path d="M28 70 Q26 30 50 24 Q74 30 72 70 Z" fill="' + r.c2 + '"/>');
    // robe, trim and belt
    s.push('<path d="M35 64 Q50 58 65 64 L80 120 Q50 129 20 120 Z" fill="' + fill + '"/>');
    s.push('<path d="M22 112 Q50 120 78 112 L80 120 Q50 129 20 120 Z" fill="' + r.c2 + '"/>');
    s.push('<path d="M30 86 Q50 91 70 86" stroke="' + r.c2 + '" stroke-width="5" fill="none" stroke-linecap="round"/>');
    s.push('<circle cx="50" cy="89" r="3.2" fill="#FBBF24" stroke="#92400E" stroke-width="1"/>');
    s.push('<path d="M44 66 L50 76 L56 66" fill="none" stroke="#fff" stroke-opacity=".5" stroke-width="2"/>');
    // the arm that rests, and the wand arm
    s.push('<path d="M37 70 Q27 84 30 98" stroke="' + fill + '" stroke-width="10" fill="none" stroke-linecap="round"/>');
    s.push('<circle cx="30" cy="99" r="4.6" fill="' + skin + '"/>');
    var hx = cast ? 84 : 77, hy = cast ? 54 : 90;
    s.push('<path d="M63 70 Q' + (cast ? "78 66 " : "75 78 ") + hx + " " + hy + '" stroke="' + fill + '" stroke-width="10" fill="none" stroke-linecap="round"/>');
    s.push(wandSvg(look.wand, hx, hy, cast ? -62 : -50));
    s.push('<circle cx="' + hx + '" cy="' + hy + '" r="4.6" fill="' + skin + '"/>');
    // head
    s.push('<circle cx="35" cy="48" r="3.4" fill="' + skin + '"/><circle cx="65" cy="48" r="3.4" fill="' + skin + '"/>');
    s.push('<circle cx="50" cy="46" r="16.5" fill="' + skin + '"/>');
    s.push('<path d="M34 46 Q34 28 50 28 Q66 28 66 46 Q61 37 52 38 Q46 34 40 39 Q36 41 34 46 Z" fill="' + hair + '"/>');
    s.push('<path d="M34 44 Q32 54 35 58 L37 46 Z M66 44 Q68 54 65 58 L63 46 Z" fill="' + hair + '"/>');
    s.push('<ellipse cx="44" cy="48" rx="2.1" ry="2.7" fill="#1E1B18"/><ellipse cx="56" cy="48" rx="2.1" ry="2.7" fill="#1E1B18"/>');
    s.push('<circle cx="44.8" cy="47" r=".8" fill="#fff"/><circle cx="56.8" cy="47" r=".8" fill="#fff"/>');
    s.push('<circle cx="40.5" cy="53.5" r="2.6" fill="#F472B6" opacity=".45"/><circle cx="59.5" cy="53.5" r="2.6" fill="#F472B6" opacity=".45"/>');
    s.push('<path d="M45 54.5 Q50 58.5 55 54.5" stroke="#7C2D12" stroke-width="1.7" fill="none" stroke-linecap="round"/>');
    s.push(hatSvg(look.hat, r));
    s.push("</svg>");
    return s.join("");
  }
  function hatSvg(h, r) {
    if (h === "wide") return '<path d="M38 34 Q38 15 50 14 Q62 15 62 34 Z" fill="#92400E"/><rect x="38" y="27" width="24" height="4" fill="#F59E0B"/><ellipse cx="50" cy="34" rx="29" ry="6" fill="#78350F"/>';
    if (h === "hood") return '<path d="M30 60 Q26 26 50 21 Q74 26 70 60 Q67 38 50 36 Q33 38 30 60 Z" fill="' + r.c + '"/><path d="M33 52 Q34 39 50 37 Q66 39 67 52" fill="none" stroke="' + r.c2 + '" stroke-width="2"/>';
    if (h === "beret") return '<ellipse cx="47" cy="31" rx="20" ry="7.5" fill="#1F2937" transform="rotate(-10 47 31)"/><circle cx="44" cy="23.5" r="2.4" fill="#1F2937"/>';
    if (h === "phones") return '<path d="M33 47 Q33 24 50 24 Q67 24 67 47" stroke="#111827" stroke-width="4.5" fill="none"/><rect x="28" y="41" width="8" height="13" rx="3.5" fill="#EF4444" stroke="#111827" stroke-width="1.5"/><rect x="64" y="41" width="8" height="13" rx="3.5" fill="#EF4444" stroke="#111827" stroke-width="1.5"/>';
    if (h === "crown") return '<path d="M36 35 L35 21 L42.5 28 L50 17 L57.5 28 L65 21 L64 35 Z" fill="#FBBF24" stroke="#B45309" stroke-width="1.5" stroke-linejoin="round"/><circle cx="50" cy="29" r="2.4" fill="#EF4444"/><circle cx="41" cy="31" r="1.6" fill="#3B82F6"/><circle cx="59" cy="31" r="1.6" fill="#22C55E"/>';
    var dark = h === "starry", c = dark ? "#1E1B4B" : r.c, c2 = dark ? "#312E81" : r.c2;
    var star = '<path d="M50 14 l1.6 3.3 3.6.5-2.6 2.5.6 3.6-3.2-1.7-3.2 1.7.6-3.6-2.6-2.5 3.6-.5z" fill="#FDE047"/>';
    return '<path d="M33 35 L50 4 Q54 -1 57 4 L67 35 Z" fill="' + c + '"/><path d="M57 4 Q66 2 70 9" stroke="' + c + '" stroke-width="4" fill="none" stroke-linecap="round"/>' +
      '<ellipse cx="50" cy="35" rx="23" ry="5.5" fill="' + c2 + '"/>' + star +
      (dark ? '<circle cx="44" cy="26" r="1.3" fill="#FDE047"/><circle cx="58" cy="25" r="1.1" fill="#FDE047"/>' : "");
  }
  function wandSvg(w, x, y, deg) {
    var s = '<g transform="translate(' + x + " " + y + ") rotate(" + deg + ')">';
    var stick = { oak: "#78350F", crystal: "#475569", quill: "#1F2937", mic: "#111827", star: "#B45309" }[w] || "#78350F";
    s += '<rect x="-1.8" y="-1.6" width="30" height="3.6" rx="1.8" fill="' + stick + '"/>';
    if (w === "crystal") s += '<path d="M29 0 L34 -5 L41 0 L34 5 Z" fill="#67E8F9" stroke="#0E7490" stroke-width="1"/>';
    else if (w === "quill") s += '<path d="M27 0 Q36 -9 46 -3 Q37 -1 27 0 Z M27 0 Q36 7 45 2" fill="#F8FAFC" stroke="#94A3B8" stroke-width="1"/>';
    else if (w === "mic") s += '<circle cx="33" cy="0" r="6" fill="#9CA3AF" stroke="#374151" stroke-width="1.5"/><path d="M29 -2h8M29 2h8" stroke="#374151" stroke-width="1"/>';
    else if (w === "star") s += '<path d="M34 -7 l2 4.2 4.6.6-3.3 3.2.8 4.6-4.1-2.2-4.1 2.2.8-4.6-3.3-3.2 4.6-.6z" fill="#FDE047" stroke="#B45309" stroke-width="1"/>';
    else s += '<circle cx="30" cy="0" r="3.6" fill="#FDE68A"/><circle cx="30" cy="0" r="6.5" fill="#FDE68A" opacity=".35"/>';
    return s + "</g>";
  }

  // Body outlines on a 100 by 100 grid, with the top of each body.
  var BODY = {
    round: { d: "M50 32 C68 32 80 44 80 61 C80 79 67 90 50 90 C33 90 20 79 20 61 C20 44 32 32 50 32 Z", top: 32, eye: 56, belly: [50, 72, 18, 13] },
    drop: { d: "M50 20 C64 36 79 50 79 66 C79 82 66 91 50 91 C34 91 21 82 21 66 C21 50 36 36 50 20 Z", top: 22, eye: 58, belly: [50, 74, 17, 12] },
    tall: { d: "M33 28 Q50 20 67 28 Q73 31 73 44 L73 78 Q73 91 50 91 Q27 91 27 78 L27 44 Q27 31 33 28 Z", top: 26, eye: 48, belly: [50, 70, 15, 16] },
    wide: { d: "M50 40 C76 40 89 52 89 66 C89 81 72 90 50 90 C28 90 11 81 11 66 C11 52 24 40 50 40 Z", top: 40, eye: 60, belly: [50, 76, 22, 10] },
    blob: { d: "M30 40 C34 25 62 23 70 35 C84 37 87 56 81 66 C88 80 73 94 56 90 C44 96 26 92 22 80 C12 70 16 51 30 40 Z", top: 28, eye: 55, belly: [50, 74, 19, 12] }
  };
  function lighten(hex, k) {
    var n = parseInt(hex.slice(1), 16), r = n >> 16, g = (n >> 8) & 255, b = n & 255;
    function f(c) { return Math.round(c + (255 - c) * k); }
    return "#" + ((1 << 24) + (f(r) << 16) + (f(g) << 8) + f(b)).toString(16).slice(1);
  }
  function topSvg(kind, t, c, c2, big) {
    var k = big ? 1.25 : 1;
    if (kind === "ears") return '<path d="M' + (32) + " " + (t + 10) + " L" + (26) + " " + (t - 12 * k) + " L" + (44) + " " + (t + 2) + ' Z" fill="' + c + '"/><path d="M68 ' + (t + 10) + " L74 " + (t - 12 * k) + " L56 " + (t + 2) + ' Z" fill="' + c + '"/><path d="M31 ' + (t + 4) + " L29 " + (t - 6 * k) + " L38 " + (t + 1) + ' Z M69 ' + (t + 4) + " L71 " + (t - 6 * k) + " L62 " + (t + 1) + ' Z" fill="' + c2 + '"/>';
    if (kind === "horns") return '<path d="M38 ' + (t + 6) + " Q30 " + (t - 10 * k) + " 22 " + (t - 14 * k) + " Q32 " + (t - 2) + ' 42 ' + (t + 4) + ' Z" fill="#F8FAFC" stroke="#94A3B8"/><path d="M62 ' + (t + 6) + " Q70 " + (t - 10 * k) + " 78 " + (t - 14 * k) + " Q68 " + (t - 2) + ' 58 ' + (t + 4) + ' Z" fill="#F8FAFC" stroke="#94A3B8"/>';
    if (kind === "antenna") return '<path d="M42 ' + (t + 4) + " Q38 " + (t - 8) + " 34 " + (t - 14 * k) + ' M58 ' + (t + 4) + " Q62 " + (t - 8) + " 66 " + (t - 14 * k) + '" stroke="' + c + '" stroke-width="2.6" fill="none" stroke-linecap="round"/><circle cx="34" cy="' + (t - 15 * k) + '" r="4" fill="' + c2 + '"/><circle cx="66" cy="' + (t - 15 * k) + '" r="4" fill="' + c2 + '"/>';
    if (kind === "spikes") {
      var p = "M28 " + (t + 10);
      for (var i = 0; i < 5; i++) { var x = 30 + i * 10; p += " L" + (x + 5) + " " + (t - 9 * k) + " L" + (x + 10) + " " + (t + 6); }
      return '<path d="' + p + ' Z" fill="' + c2 + '"/>';
    }
    if (kind === "leaf") return '<path d="M50 ' + (t + 2) + " Q36 " + (t - 16 * k) + " 24 " + (t - 8) + " Q38 " + (t - 2) + ' 50 ' + (t + 2) + ' Z" fill="#4ADE80" stroke="#166534"/><path d="M50 ' + (t + 2) + " Q64 " + (t - 18 * k) + " 78 " + (t - 10) + " Q62 " + (t - 2) + ' 50 ' + (t + 2) + ' Z" fill="#22C55E" stroke="#166534"/>';
    return "";
  }
  var GLYPH = {
    nib: '<path d="M0 -8 L6 2 L0 8 L-6 2 Z" fill="#fff" opacity=".9"/><circle cx="0" cy="1" r="1.6" fill="#A21CAF"/>',
    star: '<path d="M0 -8 l2.4 5 5.5.7-4 3.8 1 5.4L0 9.3l-4.9 2.6 1-5.4-4-3.8 5.5-.7z" fill="#fff" opacity=".9"/>',
    note: '<path d="M2 -8 V4 a3.5 3 0 1 1 -2 -2.6 V-8 Z M2 -8 L8 -6 V-2 L2 -4" fill="#fff" opacity=".9"/>',
    bolt: '<path d="M2 -9 L-5 1 H0 L-2 9 L5 -1 H0 Z" fill="#fff" opacity=".95"/>'
  };
  // mood: "muddle" for a monster, "friendly" for a pet, "cleared" for a beaten monster
  function creatureSvg(a, o) {
    o = o || {};
    var b = BODY[a.shape] || BODY.round, mood = o.mood || "friendly", stage = o.stage || 0;
    var c = a.c, c2 = a.c2;
    if (mood !== "muddle") { c = mood === "cleared" ? lighten(c, 0.25) : c; }
    uid += 1;
    var s = ['<svg class="mq-mon' + (o.cls ? " " + o.cls : "") + (mood === "muddle" ? " is-muddle" : "") + '" viewBox="0 0 100 100" aria-hidden="true" focusable="false">'];
    s.push('<ellipse cx="50" cy="94" rx="30" ry="4.5" fill="#000" opacity=".22"/>');
    if (o.aura) s.push('<circle cx="50" cy="60" r="40" fill="' + o.aura + '" opacity=".22"/>');
    if (stage >= 2 || a.extra === "wings") {
      s.push('<path d="M26 58 Q4 40 6 22 Q20 34 30 48 Z" fill="' + lighten(c, 0.45) + '" stroke="' + c + '" stroke-width="1.5"/><path d="M74 58 Q96 40 94 22 Q80 34 70 48 Z" fill="' + lighten(c, 0.45) + '" stroke="' + c + '" stroke-width="1.5"/>');
    }
    if (stage >= 1) s.push('<path d="M72 82 Q89 86 91 71" stroke="' + c + '" stroke-width="5.5" fill="none" stroke-linecap="round"/><path d="M91 59 L97 68 L91 75 L85 68 Z" fill="' + c2 + '" stroke="' + c + '" stroke-width="1.6" stroke-linejoin="round"/>');
    s.push(topSvg(a.top, b.top, c, c2, stage >= 1));
    s.push('<path d="' + b.d + '" fill="' + c + '"/>');
    s.push('<ellipse cx="' + b.belly[0] + '" cy="' + b.belly[1] + '" rx="' + b.belly[2] + '" ry="' + b.belly[3] + '" fill="' + c2 + '" opacity=".9"/>');
    if (GLYPH[a.mark]) s.push('<g transform="translate(' + b.belly[0] + " " + b.belly[1] + ')">' + GLYPH[a.mark] + "</g>");
    // eyes
    var n = a.eyes || 2, y = b.eye, xs = n === 1 ? [50] : n === 3 ? [36, 50, 64] : [40, 60];
    xs.forEach(function (x, i) {
      var yy = n === 3 && i === 1 ? y - 5 : y, r = n === 1 ? 8.5 : 6.2;
      s.push('<circle cx="' + x + '" cy="' + yy + '" r="' + r + '" fill="#fff"/>');
      if (mood === "muddle") {
        s.push('<circle cx="' + (x + (i % 2 ? -1.6 : 1.6)) + '" cy="' + (yy + 1) + '" r="' + (r * 0.46) + '" fill="#111827"/>');
        s.push('<path d="M' + (x - r) + " " + (yy - r - 2 + (i % 2 ? 3 : 0)) + " L" + (x + r) + " " + (yy - r - 2 + (i % 2 ? 0 : 3)) + '" stroke="#111827" stroke-width="2.4" stroke-linecap="round"/>');
      } else {
        s.push('<circle cx="' + x + '" cy="' + (yy + 0.5) + '" r="' + (r * 0.55) + '" fill="#111827"/><circle cx="' + (x + r * 0.2) + '" cy="' + (yy - r * 0.2) + '" r="' + (r * 0.2) + '" fill="#fff"/>');
      }
    });
    var my = y + (a.shape === "tall" ? 13 : 12);
    if (mood === "muddle") {
      if (a.mouth === "o") s.push('<ellipse cx="50" cy="' + (my + 1) + '" rx="4" ry="5" fill="#111827"/>');
      else if (a.mouth === "zig") s.push('<path d="M40 ' + my + " l4 3 4 -3 4 3 4 -3 4 3" + '" stroke="#111827" stroke-width="2.2" fill="none" stroke-linejoin="round"/>');
      else if (a.mouth === "fang") s.push('<path d="M40 ' + my + " Q50 " + (my + 7) + " 60 " + my + '" stroke="#111827" stroke-width="2.4" fill="#7F1D1D"/><path d="M43 ' + (my + 1) + " l2 4 2 -3.4 Z M57 " + (my + 1) + ' l-2 4 -2 -3.4 Z" fill="#fff"/>');
      else s.push('<path d="M41 ' + (my + 2) + " Q50 " + (my - 3) + " 59 " + (my + 2) + '" stroke="#111827" stroke-width="2.4" fill="none" stroke-linecap="round"/>');
      for (var k = 0; k < 4; k++) s.push('<rect class="mq-static" x="16" y="' + (36 + k * 14) + '" width="68" height="3" fill="#fff" opacity=".22"/>');
    } else {
      s.push('<path d="M41 ' + my + " Q50 " + (my + 8) + " 59 " + my + '" stroke="#111827" stroke-width="2.4" fill="#fff" stroke-linecap="round"/>');
      s.push('<circle cx="' + (xs[0] - 7) + '" cy="' + (y + 8) + '" r="3.4" fill="#F472B6" opacity=".45"/><circle cx="' + (xs[xs.length - 1] + 7) + '" cy="' + (y + 8) + '" r="3.4" fill="#F472B6" opacity=".45"/>');
    }
    if (stage >= 2) s.push('<path d="M40 ' + (b.top - 4) + " L42 " + (b.top - 14) + " L47 " + (b.top - 8) + " L50 " + (b.top - 17) + " L53 " + (b.top - 8) + " L58 " + (b.top - 14) + " L60 " + (b.top - 4) + ' Z" fill="#FBBF24" stroke="#B45309" stroke-width="1"/>');
    if (mood === "cleared") s.push('<path class="mq-sparkle" d="M14 26 l2 5 5 2 -5 2 -2 5 -2 -5 -5 -2 5 -2 Z M86 30 l1.6 4 4 1.6 -4 1.6 -1.6 4 -1.6 -4 -4 -1.6 4 -1.6 Z" fill="#FDE047"/>');
    s.push("</svg>");
    return s.join("");
  }
  function petSvg(info, cls) {
    return creatureSvg(info.art, { mood: "friendly", stage: info.starter ? info.stage : 1, aura: EL[info.el].colour, cls: cls });
  }

  var SCENE = {
    isles: '<rect width="400" height="220" fill="url(#sky)"/><circle cx="330" cy="50" r="26" fill="#FEF3C7" opacity=".9"/><path d="M0 150 Q100 135 200 150 T400 150 V220 H0Z" fill="#38BDF8"/><path d="M0 165 Q100 152 200 165 T400 165 V220 H0Z" fill="#0EA5E9"/><path d="M40 170 Q120 150 200 172 Q280 190 360 168 L400 220 H0Z" fill="#FDE68A"/><path d="M300 158 V100" stroke="#78350F" stroke-width="5"/><path d="M300 100 Q285 92 270 104 M300 100 Q316 90 330 102 M300 100 Q296 84 286 80 M300 100 Q308 84 320 82" stroke="#16A34A" stroke-width="6" fill="none" stroke-linecap="round"/>',
    vale: '<rect width="400" height="220" fill="url(#sky)"/><circle cx="70" cy="48" r="22" fill="#FEF9C3" opacity=".9"/><path d="M0 150 Q80 110 170 140 Q260 100 400 140 V220 H0Z" fill="#4ADE80"/><path d="M0 175 Q120 150 230 172 Q320 160 400 175 V220 H0Z" fill="#22C55E"/><path d="M320 140 V90 L332 76 L344 90 V140Z" fill="#E0E7FF" stroke="#6366F1" stroke-width="2"/><circle cx="60" cy="150" r="14" fill="#15803D"/><circle cx="80" cy="146" r="18" fill="#16A34A"/>',
    peaks: '<rect width="400" height="220" fill="url(#sky)"/><path d="M0 170 L70 70 L120 130 L190 40 L260 140 L320 80 L400 160 V220 H0Z" fill="#A78BFA"/><path d="M190 40 L170 72 L185 66 L200 76 L212 60Z M70 70 L58 88 L72 84 L82 90Z" fill="#F5F3FF"/><path d="M0 185 Q110 165 220 185 Q320 200 400 182 V220 H0Z" fill="#7C3AED"/>',
    coast: '<rect width="400" height="220" fill="url(#sky)"/><path d="M0 160 Q100 148 200 160 T400 160 V220 H0Z" fill="#FB923C" opacity=".55"/><path d="M0 172 Q100 160 200 172 T400 172 V220 H0Z" fill="#0EA5E9"/><path d="M60 168 L72 80 H92 L104 168Z" fill="#F8FAFC" stroke="#EA580C" stroke-width="3"/><path d="M70 110 H96 M66 140 H100" stroke="#EA580C" stroke-width="6"/><rect x="74" y="66" width="16" height="14" fill="#FDE047"/><path d="M90 72 L170 52 L170 92Z" fill="#FDE047" opacity=".35"/>',
    spire: '<rect width="400" height="220" fill="url(#sky)"/><path d="M170 190 L190 40 L200 20 L210 40 L230 190Z" fill="#312E81" stroke="#A78BFA" stroke-width="2"/><path d="M40 60 L60 90 L50 92 L72 128 M320 50 L300 86 L312 88 L292 124" stroke="#C4B5FD" stroke-width="3" fill="none"/><path d="M0 190 Q200 170 400 190 V220 H0Z" fill="#1E1B4B"/>'
  };
  var SKY = { isles: ["#7DD3FC", "#E0F2FE"], vale: ["#86EFAC", "#F0FDF4"], peaks: ["#C4B5FD", "#F5F3FF"], coast: ["#FDBA74", "#FFF7ED"], spire: ["#1E1B4B", "#4C1D95"] };
  function sceneSvg(id) {
    var k = SKY[id] || SKY.isles;
    return '<svg class="mq-scene" viewBox="0 0 400 220" preserveAspectRatio="xMidYMid slice" aria-hidden="true" focusable="false"><defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="' + k[0] + '"/><stop offset="1" stop-color="' + k[1] + '"/></linearGradient></defs>' + (SCENE[id] || SCENE.isles) + "</svg>";
  }

  /* ----------------------------------------------------------- Pixel */
  var pxSeq = 0;
  function pixel(mood, wear) {
    var tpl = document.getElementById("mq-pixel");
    if (!tpl) return null;
    var svg = (tpl.content ? tpl.content.firstElementChild : tpl.firstElementChild).cloneNode(true);
    pxSeq += 1;
    var map = {};
    Array.prototype.forEach.call(svg.querySelectorAll("[id]"), function (n) { map[n.id] = n.id + "-q" + pxSeq; n.id = map[n.id]; });
    Array.prototype.forEach.call(svg.querySelectorAll("[fill^='url(#']"), function (n) {
      var m = /^url\(#([^)]+)\)$/.exec(n.getAttribute("fill"));
      if (m && map[m[1]]) n.setAttribute("fill", "url(#" + map[m[1]] + ")");
    });
    svg.setAttribute("aria-hidden", "true");
    svg.setAttribute("class", "px is-" + (mood || "idle") + " wear-" + (wear || "wizard"));
    return svg;
  }

  /* -------------------------------------------------------------- shell */
  app.innerHTML = "";
  app.setAttribute("data-motion", calm() ? "calm" : "full");
  var live = el("p", { "class": "mq-live", role: "status", "aria-live": "polite" });
  var hud = el("header", { "class": "mq-hud" });
  var stage = el("div", { "class": "mq-stage" });
  var toastBox = el("div", { "class": "mq-toast", role: "status", "aria-live": "polite" });
  app.appendChild(hud); app.appendChild(stage); app.appendChild(toastBox); app.appendChild(live);
  function say(t) { live.textContent = ""; setTimeout(function () { live.textContent = t; }, 40); }
  var toastT = 0;
  function toast(t) {
    toastBox.textContent = t; toastBox.classList.add("is-on");
    clearTimeout(toastT); toastT = setTimeout(function () { toastBox.classList.remove("is-on"); }, 4200);
  }
  function focusMain() {
    var h = stage.querySelector("[data-focus]") || stage.querySelector("h1, h2");
    if (h) { if (!h.hasAttribute("tabindex")) h.setAttribute("tabindex", "-1"); setTimeout(function () { try { h.focus({ preventScroll: true }); } catch (e) { h.focus(); } }, 30); }
  }
  function screen(cls, realmId) {
    clearTimers();
    stage.className = "mq-stage " + (cls || "");
    if (realmId) stage.setAttribute("data-realm", realmId); else stage.removeAttribute("data-realm");
    stage.innerHTML = "";
    Array.prototype.forEach.call(app.querySelectorAll(".mq-modal-back"), function (m) { m.remove(); });
    var top = app.getBoundingClientRect().top;
    if (top < 0) app.scrollIntoView({ block: "start" });
    return stage;
  }

  function paintHud() {
    hud.innerHTML = "";
    if (!S || !S.name) { hud.hidden = true; return; }
    hud.hidden = false;
    var L = levelOf(S.xp), a = levelStart(L), b = levelStart(L + 1);
    var me = el("a", { "class": "mq-me", href: "#/map", "aria-label": S.name + ", level " + L + ". Open the map" });
    me.innerHTML = '<span class="mq-me-art">' + wizardSvg(S.look) + '</span><span class="mq-me-txt"><b>' + esc(S.name) + '</b><span class="mq-lv">Level ' + L + "</span></span>";
    var xp = el("div", { "class": "mq-xp", role: "img", "aria-label": fmt(S.xp - a) + " of " + fmt(b - a) + " XP to level " + (L + 1) }, [
      el("span", { "class": "mq-xp-fill", style: "width:" + Math.round(100 * (S.xp - a) / (b - a)) + "%" })]);
    var coins = el("span", { "class": "mq-chip", title: "Coins", html: ico("coin") + '<span class="mq-sr">Coins: </span>' + fmt(S.coins) });
    var pots = el("span", { "class": "mq-chip", title: "Healing draughts", html: ico("potion") + '<span class="mq-sr">Healing draughts: </span>' + (S.items.draught + S.items.elixir) });
    var nav = el("nav", { "class": "mq-nav", "aria-label": "Adventure" }, [
      navLink("#/map", "map", "Map"), navLink("#/pets", "paw", "Pets"), navLink("#/shop", "bag", "Shop"),
      navLink("#/book", "book", "Spellbook"),
      btn("mq-nb", ico(S.sound ? "sound" : "mute") + '<span class="mq-nb-t">Sound</span>', function () {
        S.sound = !S.sound; save(); paintHud(); if (S.sound) sfx("good"); say(S.sound ? "Sound on" : "Sound off");
      }, { "aria-pressed": String(!!S.sound), "aria-label": "Sound" }),
      navLink("#/settings", "gear", "Settings")]);
    hud.appendChild(el("div", { "class": "mq-hud-l" }, [me, xp]));
    hud.appendChild(el("div", { "class": "mq-hud-r" }, [coins, pots, nav]));
  }
  function navLink(href, icon, label) {
    var cur = location.hash.indexOf(href) === 0;
    return el("a", { "class": "mq-nb" + (cur ? " is-on" : ""), href: href, "aria-current": cur ? "page" : null,
                     html: ico(icon) + '<span class="mq-nb-t">' + label + "</span>" });
  }

  /* -------------------------------------------------------------- router */
  var pending = "";
  var B = null;   // the battle in progress
  function go(h) { if (location.hash === h) route(); else location.hash = h; }
  function route() {
    var h = location.hash.replace(/^#\/?/, ""), parts = h.split("/");
    if (B && parts[0] !== "battle") endBattle();
    if (!S || !S.name) {
      if (parts[0] === "place" && parts[1]) pending = parts[1];
      if (parts[0] === "new") return createScreen(false);
      return titleScreen();
    }
    paintHud();
    switch (parts[0]) {
      case "map": return mapScreen();
      case "place": var p = place(parts[1]); return p ? (unlocked(p) ? placeScreen(p) : lockedPlace(p)) : mapScreen();
      case "spire": return finalOpen() ? spireScreen() : (toast("Clear all eleven places to reach the Studio Spire."), mapScreen());
      case "battle": return B ? null : go("#/map");
      case "pets": return petsScreen();
      case "shop": return shopScreen(parts[1] || "potion");
      case "book": return parts[1] && place(parts[1]) ? bookPage(place(parts[1])) : bookScreen();
      case "settings": return settingsScreen();
      case "look": return createScreen(true);
      case "story": return storyScreen();
      default: return titleScreen();
    }
  }
  function lockedPlace(p) {
    var i = placeIndex(p);
    toast(p.name + " opens when you clear " + P[i - 1].name + ". Or switch on Explore freely in Settings.");
    mapScreen();
  }

  /* ------------------------------------------------------------- title */
  function titleScreen() {
    paintHud();
    var s = screen("mq-title", "isles");
    var art = el("div", { "class": "mq-title-art" });
    art.innerHTML = sceneSvg("isles");
    var cast = el("div", { "class": "mq-title-cast" });
    cast.innerHTML = '<span class="mq-tc-wiz">' + wizardSvg(S ? S.look : { robe: "purple", hat: "starry", wand: "star", skin: 2, hair: "brown" }, { pose: "cast" }) + "</span>" +
      '<span class="mq-tc-pet">' + creatureSvg(D.starters[1].art, { mood: "friendly", stage: 1, aura: EL.light.colour }) + "</span>" +
      '<span class="mq-tc-foe">' + creatureSvg(D.final.monster.art, { mood: "muddle", cls: "is-big" }) + "</span>";
    var px = pixel("wave", "wizard");
    if (px) { var pw = el("span", { "class": "mq-tc-px" }); pw.appendChild(px); cast.appendChild(pw); }
    art.appendChild(cast);
    s.appendChild(art);
    var box = el("div", { "class": "mq-title-box" }, [
      el("p", { "class": "mq-kicker", text: "Creative iMedia R093" }),
      el("h1", { "class": "mq-logo", "data-focus": "1", tabindex: "-1" }, [el("span", { text: "The Media" }), el("span", { text: "Realms" })]),
      el("p", { "class": "mq-tagline", text: "Answer to cast spells, clear the muddles with your pet, and master R093 topic by topic." })]);
    var row = el("div", { "class": "mq-row" });
    if (S && S.name) {
      row.appendChild(btn("mq-go", ico("next") + " Continue as " + esc(S.name), function () { go("#/map"); }));
      row.appendChild(btn("mq-ghost", "Start again", function () {
        confirmBox("Start a new adventure? This wizard, their pets and their progress will be wiped from this browser.", "Wipe and start again", function () {
          store.clear(); S = null; go("#/new");
        });
      }));
    } else {
      row.appendChild(btn("mq-go", ico("next") + " Start the adventure", function () { go("#/new"); }));
    }
    box.appendChild(row);
    box.appendChild(el("h2", { "class": "mq-sr", text: "How the adventure works" }));
    box.appendChild(el("ul", { "class": "mq-points" }, [
      el("li", { html: ico("map") + " Eleven places, one for every R093 lesson, in four realms" }),
      el("li", { html: ico("spark") + " Every spell needs a right answer, and every answer explains why" }),
      el("li", { html: ico("paw") + " Hatch, train and evolve pets, and befriend the guardians you clear" })]));
    s.appendChild(box);
    focusMain();
  }

  function confirmBox(text, yes, fn) {
    var back = el("div", { "class": "mq-modal-back" });
    var dlg = el("div", { "class": "mq-modal", role: "dialog", "aria-modal": "true", "aria-labelledby": "mq-cf-h" });
    var close = function () { back.remove(); document.removeEventListener("keydown", onKey, true); };
    function onKey(e) { if (e.key === "Escape") { e.preventDefault(); close(); } }
    dlg.appendChild(el("h2", { id: "mq-cf-h", text: "Are you sure?" }));
    dlg.appendChild(el("p", { text: text }));
    var no = btn("mq-ghost", "Keep it", close);
    dlg.appendChild(el("div", { "class": "mq-row" }, [btn("mq-go is-danger", yes, function () { close(); fn(); }), no]));
    back.appendChild(dlg);
    app.appendChild(back);
    document.addEventListener("keydown", onKey, true);
    setTimeout(function () { no.focus(); }, 30);
  }

  /* ---------------------------------------------------------- create */
  function createScreen(editing) {
    var look = editing ? Object.assign({}, S.look) : { robe: "purple", hat: "pointed", wand: "oak", skin: Math.floor(Math.random() * 6), hair: pick(Object.keys(D.hairs)) };
    var chosenPet = editing ? S.pet : "";
    var s = screen("mq-create", "vale");
    if (!editing) paintHud();
    s.appendChild(el("h1", { "class": "mq-h", "data-focus": "1", tabindex: "-1", text: editing ? "Change your look" : "Create your wizard" }));
    var preview = el("div", { "class": "mq-preview" });
    function paint() { preview.innerHTML = sceneSvg("vale") + '<span class="mq-preview-wiz">' + wizardSvg(look, { pose: "cast" }) + "</span>"; }
    paint();
    var form = el("div", { "class": "mq-form" });
    var nameIn = el("input", { id: "mq-name", type: "text", maxlength: "14", autocomplete: "off", spellcheck: "false",
                               value: editing ? S.name : "", placeholder: "Your wizard name" });
    var nameHelp = el("p", { "class": "mq-help", id: "mq-name-help", text: "Up to 14 letters, numbers and spaces. It stays in this browser only, so a first name or a made up name is fine." });
    nameIn.setAttribute("aria-describedby", "mq-name-help");
    nameIn.addEventListener("input", function () {
      var v = nameIn.value.replace(/[^A-Za-z0-9 ']/g, "");
      if (v !== nameIn.value) nameIn.value = v;
    });
    form.appendChild(el("div", { "class": "mq-field" }, [el("label", { "for": "mq-name", text: "Name" }), nameIn, nameHelp]));
    function swatches(label, list, cur, set, paintFn) {
      var g = el("div", { "class": "mq-swatches", role: "radiogroup", "aria-label": label });
      list.forEach(function (it) {
        var b = btn("mq-sw" + (it.v === cur() ? " is-on" : ""), paintFn(it), function () {
          set(it.v); Array.prototype.forEach.call(g.children, function (x) { x.classList.remove("is-on"); x.setAttribute("aria-checked", "false"); });
          b.classList.add("is-on"); b.setAttribute("aria-checked", "true"); paint(); sfx("tap");
        }, { role: "radio", "aria-checked": String(it.v === cur()), "aria-label": it.name });
        g.appendChild(b);
      });
      return el("div", { "class": "mq-field" }, [el("p", { "class": "mq-label", text: label }), g]);
    }
    var tones = ["Skin tone 1", "Skin tone 2", "Skin tone 3", "Skin tone 4", "Skin tone 5", "Skin tone 6"];
    form.appendChild(swatches("Skin", D.skins.map(function (c, i) { return { v: i, name: tones[i], c: c }; }),
      function () { return look.skin; }, function (v) { look.skin = v; }, function (it) { return '<span class="mq-dot" style="background:' + it.c + '"></span>'; }));
    form.appendChild(swatches("Hair", Object.keys(D.hairs).map(function (k) { return { v: k, name: k.charAt(0).toUpperCase() + k.slice(1) + " hair", c: D.hairs[k] }; }),
      function () { return look.hair; }, function (v) { look.hair = v; }, function (it) { return '<span class="mq-dot" style="background:' + it.c + '"></span>'; }));
    var robes = D.shop.robe.filter(function (r) { return !r.price || (editing && owns("robe", r.id)); });
    form.appendChild(swatches("Robe", robes.map(function (r) { return { v: r.id, name: r.name, c: r.c }; }),
      function () { return look.robe; }, function (v) { look.robe = v; }, function (it) { return '<span class="mq-dot" style="background:' + it.c + '"></span>'; }));
    var hats = D.shop.hat.filter(function (h) { return !h.price || (editing && owns("hat", h.id)); });
    form.appendChild(swatches("Hat", hats.map(function (h) { return { v: h.id, name: h.name }; }),
      function () { return look.hat; }, function (v) { look.hat = v; }, function (it) { return '<span class="mq-sw-t">' + esc(it.name) + "</span>"; }));
    if (editing) {
      var wands = D.shop.wand.filter(function (w) { return owns("wand", w.id); });
      form.appendChild(swatches("Wand", wands.map(function (w) { return { v: w.id, name: w.name }; }),
        function () { return look.wand; }, function (v) { look.wand = v; }, function (it) { return '<span class="mq-sw-t">' + esc(it.name) + "</span>"; }));
    }
    var grid = el("div", { "class": "mq-create-grid" }, [preview, form]);
    s.appendChild(grid);
    if (!editing) {
      s.appendChild(el("h2", { "class": "mq-h2", text: "Choose your first pet" }));
      var pets = el("div", { "class": "mq-starters", role: "radiogroup", "aria-label": "First pet" });
      D.starters.forEach(function (st) {
        var card = btn("mq-starter", "", function () {
          chosenPet = st.id;
          Array.prototype.forEach.call(pets.children, function (x) { x.classList.remove("is-on"); x.setAttribute("aria-checked", "false"); });
          card.classList.add("is-on"); card.setAttribute("aria-checked", "true"); sfx("pet");
        }, { role: "radio", "aria-checked": "false", "aria-label": st.stages[0] + ", " + EL[st.el].name + " pet. " + st.about });
        card.style.setProperty("--el", EL[st.el].colour);
        card.innerHTML = '<span class="mq-starter-art">' + creatureSvg(st.art, { mood: "friendly", aura: EL[st.el].colour }) + "</span>" +
          '<b>' + esc(st.stages[0]) + '</b><span class="mq-el" style="--el:' + EL[st.el].colour + '">' + elIco(st.el) + " " + EL[st.el].name + "</span>" +
          '<span class="mq-small">' + esc(st.about) + "</span>";
        pets.appendChild(card);
      });
      s.appendChild(pets);
    }
    var err = el("p", { "class": "mq-err", role: "alert" });
    s.appendChild(err);
    var row = el("div", { "class": "mq-row" });
    row.appendChild(btn("mq-go", editing ? ico("check") + " Save my look" : ico("next") + " Begin the adventure", function () {
      var name = nameIn.value.replace(/\s+/g, " ").trim();
      if (!name) name = "Apprentice";
      if (!editing && !chosenPet) { err.textContent = "Choose your first pet to continue."; return; }
      if (!editing) {
        S = fresh(); S.name = name; S.look = look; S.pet = chosenPet; S.pets[chosenPet] = { xp: 0 };
        save(); sfx("level");
        go("#/story");
      } else {
        S.name = name; S.look = look; save(); paintHud(); toast("Your new look is saved."); go("#/settings");
      }
    }));
    if (editing) row.appendChild(el("a", { "class": "mq-ghost", href: "#/settings", text: "Cancel" }));
    s.appendChild(row);
    focusMain();
  }

  /* ----------------------------------------------------------- story */
  function storyScreen() {
    var s = screen("mq-story", "spire");
    var px = pixel("wave", "wizard");
    var box = el("div", { "class": "mq-story-box" });
    if (px) { var w = el("div", { "class": "mq-story-px" }); w.appendChild(px); box.appendChild(w); }
    var lines = el("div", { "class": "mq-story-lines" }, [el("h1", { "class": "mq-h", "data-focus": "1", tabindex: "-1", text: "Welcome, " + S.name })]);
    D.story.forEach(function (t) { lines.appendChild(el("p", { text: t })); });
    lines.appendChild(el("p", { "class": "mq-story-tip", text: "In battle, pick a spell and answer its question. A right answer casts it. Three right answers in a row and your pet joins in with a special move." }));
    box.appendChild(lines);
    s.appendChild(box);
    var row = el("div", { "class": "mq-row" });
    row.appendChild(btn("mq-go", ico("map") + " Open the map", function () {
      S.told = true; save();
      if (pending && place(pending) && unlocked(place(pending))) { var p = pending; pending = ""; go("#/place/" + p); }
      else go("#/map");
    }));
    s.appendChild(row);
    focusMain();
  }

  /* ------------------------------------------------------------- map */
  function nodeState(p) { return !unlocked(p) ? "locked" : cleared(p) ? "done" : "open"; }
  function starRow(n, of, cls) {
    var h = '<span class="mq-stars ' + (cls || "") + '" aria-hidden="true">';
    for (var i = 0; i < of; i++) h += '<span class="' + (i < n ? "is-on" : "") + '">' + ico("star") + "</span>";
    return h + "</span>";
  }
  function placeStars(p) { return stars(p).reduce(function (a, b) { return a + b; }, 0); }
  // where a realm's name sits on the map, clear of the places' labels
  var TAG_AT = { peaks: [85, 73], coast: [21, 86] };
  function mapScreen() {
    var s = screen("mq-map");
    var done = clearedCount();
    s.appendChild(el("div", { "class": "mq-map-head" }, [
      el("h1", { "class": "mq-h", "data-focus": "1", tabindex: "-1", text: "The Media Realms" }),
      el("p", { "class": "mq-sub", text: done === P.length ? (S.final ? "Every place cleared and the Great Static beaten. Replay any place to earn more stars." : "Every place cleared. The Studio Spire awaits.") : done + " of " + P.length + " places cleared. " + (S.free ? "Explore freely is on." : "Clear a place's guardian to open the next.") })]));
    // the picture map, for wider screens
    var map = el("div", { "class": "mq-world" });
    var svg = ['<svg class="mq-world-art" viewBox="0 0 100 70" preserveAspectRatio="none" aria-hidden="true" focusable="false">',
      '<defs><radialGradient id="sea" cx=".5" cy=".5" r=".75"><stop offset="0" stop-color="#38BDF8"/><stop offset="1" stop-color="#0C4A6E"/></radialGradient></defs>',
      '<rect width="100" height="70" fill="url(#sea)"/>'];
    var isl = { isles: [22, 12.6, 17, 9], vale: [76, 20, 19, 15.5], peaks: [60, 48, 22, 10], coast: [16, 43, 14, 11.5] };
    D.realms.forEach(function (r) {
      var e = isl[r.id];
      svg.push('<ellipse cx="' + e[0] + '" cy="' + e[1] + '" rx="' + (e[2] + 1.6) + '" ry="' + (e[3] + 1.2) + '" fill="' + r.ground + '" opacity=".55"/>');
      svg.push('<ellipse cx="' + e[0] + '" cy="' + e[1] + '" rx="' + e[2] + '" ry="' + e[3] + '" fill="' + r.colour + '"/>');
    });
    svg.push('<circle cx="50" cy="31.5" r="7" fill="#312E81"/><path d="M47 34 L50 22 L53 34 Z" fill="#A78BFA"/>');
    var pts = P.map(function (p) { return p.x + "," + (p.y * 0.7); }).concat(["50,31.5"]);
    svg.push('<polyline points="' + pts.join(" ") + '" fill="none" stroke="#FFF7ED" stroke-width=".7" stroke-dasharray="1.6 1.4" stroke-linecap="round" opacity=".85"/>');
    svg.push("</svg>");
    map.innerHTML = svg.join("");
    D.realms.forEach(function (r) {
      var e = isl[r.id];
      var at = TAG_AT[r.id] || [e[0], (e[1] + e[3] - 2) / 70 * 100];
      map.appendChild(el("span", { "class": "mq-realm-tag", style: "left:" + at[0] + "%;top:" + at[1] + "%", text: r.ta + " " + r.name }));
    });
    P.forEach(function (p, i) {
      var st = nodeState(p);
      var n = el("a", { "class": "mq-node is-" + st, href: st === "locked" ? "#/map" : "#/place/" + p.id,
                        style: "left:" + p.x + "%;top:" + p.y + "%;--rc:" + realm(p.realm).colour,
                        "aria-label": (i + 1) + ". " + p.name + ": " + p.topic + ". " + (st === "locked" ? "Locked" : st === "done" ? "Cleared, " + placeStars(p) + " of 9 stars" : "Open") });
      if (st === "locked") n.addEventListener("click", function (e) { e.preventDefault(); lockedPlace(p); });
      n.innerHTML = '<span class="mq-node-dot">' + (st === "locked" ? ico("lock") : st === "done" ? ico("check") : String(i + 1)) + "</span>" +
        '<span class="mq-node-name">' + esc(p.name) + "</span>" + (st === "done" ? starRow(Math.round(placeStars(p) / 3), 3, "is-mini") : "");
      map.appendChild(n);
    });
    var fo = finalOpen();
    var fn = el("a", { "class": "mq-node mq-node-final is-" + (fo ? (S.final ? "done" : "open") : "locked"), href: fo ? "#/spire" : "#/map",
                       style: "left:50%;top:45%", "aria-label": "The Studio Spire, the final battle. " + (fo ? (S.final ? "Cleared" : "Open") : "Locked until every place is cleared") });
    if (!fo) fn.addEventListener("click", function (e) { e.preventDefault(); toast("Clear all eleven places to reach the Studio Spire."); });
    fn.innerHTML = '<span class="mq-node-dot">' + (fo ? ico("flag") : ico("lock")) + '</span><span class="mq-node-name">The Studio Spire</span>';
    map.appendChild(fn);
    s.appendChild(map);
    // the trail, a list of every place in order, for phones
    var trail = el("ol", { "class": "mq-trail" });
    D.realms.forEach(function (r) {
      trail.appendChild(el("li", { "class": "mq-trail-realm", style: "--rc:" + r.colour, html: "<b>" + esc(r.ta + " " + r.name) + "</b> " + esc(r.about) }));
      P.forEach(function (p, i) {
        if (p.realm !== r.id) return;
        var st = nodeState(p);
        var a = el("a", { "class": "mq-trail-row is-" + st, href: st === "locked" ? "#/map" : "#/place/" + p.id, style: "--rc:" + r.colour });
        if (st === "locked") a.addEventListener("click", function (e) { e.preventDefault(); lockedPlace(p); });
        a.innerHTML = '<span class="mq-node-dot">' + (st === "locked" ? ico("lock") : st === "done" ? ico("check") : String(i + 1)) + "</span>" +
          '<span class="mq-trail-t"><b>' + esc(p.name) + "</b><span>" + esc(p.topic) + "</span></span>" +
          (st === "done" ? starRow(Math.round(placeStars(p) / 3), 3, "is-mini") : st === "locked" ? '<span class="mq-sr">Locked</span>' : "");
        trail.appendChild(el("li", {}, [a]));
      });
    });
    var ft = el("a", { "class": "mq-trail-row is-" + (fo ? (S.final ? "done" : "open") : "locked") + " is-final", href: fo ? "#/spire" : "#/map" });
    if (!fo) ft.addEventListener("click", function (e) { e.preventDefault(); toast("Clear all eleven places to reach the Studio Spire."); });
    ft.innerHTML = '<span class="mq-node-dot">' + (fo ? ico("flag") : ico("lock")) + '</span><span class="mq-trail-t"><b>The Studio Spire</b><span>Final battle: every R093 topic</span></span>';
    trail.appendChild(el("li", {}, [ft]));
    s.appendChild(trail);
    var next = P.filter(function (p) { return unlocked(p) && !cleared(p); })[0];
    var row = el("div", { "class": "mq-row" });
    if (next) row.appendChild(el("a", { "class": "mq-go", href: "#/place/" + next.id, html: ico("next") + " Go to " + esc(next.name) }));
    else if (fo && !S.final) row.appendChild(el("a", { "class": "mq-go", href: "#/spire", html: ico("flag") + " Face the Great Static" }));
    s.appendChild(row);
    focusMain();
  }

  /* ------------------------------------------------------------ place */
  function guideBubble(lines, who) {
    var b = el("div", { "class": "mq-bubble" });
    b.appendChild(el("p", { "class": "mq-bubble-who", text: who }));
    lines.forEach(function (t) { b.appendChild(el("p", { text: t })); });
    return b;
  }
  function placeScreen(p) {
    var r = realm(p.realm), i = placeIndex(p);
    var s = screen("mq-place", p.realm);
    var head = el("div", { "class": "mq-place-head" });
    head.innerHTML = sceneSvg(p.realm);
    head.appendChild(el("div", { "class": "mq-place-title" }, [
      el("p", { "class": "mq-kicker", text: r.ta + " " + r.name + ", place " + (i + 1) + " of " + P.length }),
      el("h1", { "class": "mq-h", "data-focus": "1", tabindex: "-1", text: p.name }),
      el("p", { "class": "mq-sub", text: p.spec + ": " + p.topic })]));
    s.appendChild(head);
    var guide = el("div", { "class": "mq-guide" });
    guide.innerHTML = '<span class="mq-guide-art">' + wizardSvg(p.guide.look) + "</span>";
    guide.appendChild(guideBubble(p.intro, p.guide.name + ", " + p.guide.role));
    s.appendChild(guide);
    s.appendChild(el("h2", { "class": "mq-h2", text: "Clear the muddles" }));
    var list = el("div", { "class": "mq-foes" });
    p.monsters.forEach(function (m, n) {
      var open = battleOpen(p, n), won = stars(p)[n];
      var card = el("article", { "class": "mq-foe-card" + (n === 2 ? " is-guardian" : "") + (open ? "" : " is-locked") + (won ? " is-won" : "") });
      var art = el("div", { "class": "mq-foe-art", html: creatureSvg(m.art, { mood: won ? "cleared" : "muddle" }) });
      card.appendChild(art);
      var txt = el("div", { "class": "mq-foe-txt" }, [
        el("p", { "class": "mq-kicker", text: n === 2 ? "Guardian" : "Wild muddle " + (n + 1) }),
        el("h3", { text: m.name }),
        el("p", { "class": "mq-small", html: '<span class="mq-muddle">Muddle:</span> ' + esc(m.muddle) }),
        el("p", { "class": "mq-el", style: "--el:" + EL[m.el].colour, html: "Weak to " + elIco(m.el) + " " + EL[m.el].name })]);
      if (won) txt.appendChild(el("p", { "class": "mq-cleared-line", html: ico("check") + " " + esc(m.cleared) }));
      card.appendChild(txt);
      var foot = el("div", { "class": "mq-foe-go" });
      if (won) foot.innerHTML = starRow(won, 3);
      if (open) foot.appendChild(btn(won ? "mq-ghost" : "mq-go", won ? "Battle again" : "Battle", function () { startBattle(p, n); }, { "aria-label": (won ? "Battle again: " : "Battle: ") + m.name }));
      else foot.appendChild(el("p", { "class": "mq-small", html: ico("lock") + " " + (n === 2 ? "Clear both wild muddles first" : "Clear " + p.monsters[n - 1].name + " first") }));
      card.appendChild(foot);
      list.appendChild(card);
    });
    s.appendChild(list);
    var extra = el("div", { "class": "mq-place-extra" });
    if (p.fact) {
      var fx = el("div", { "class": "mq-fact" });
      var px = pixel("think", "wizard");
      if (px) { var w = el("span", { "class": "mq-fact-px" }); w.appendChild(px); fx.appendChild(w); }
      fx.appendChild(el("div", {}, [el("p", { "class": "mq-bubble-who", text: "Pixel's fun fact" }), el("p", { text: p.fact })]));
      extra.appendChild(fx);
    }
    extra.appendChild(el("div", { "class": "mq-row" }, [
      el("a", { "class": "mq-ghost", href: "#/book/" + p.id, html: ico("book") + " Spellbook page" }),
      el("a", { "class": "mq-ghost", href: p.url, html: ico("next") + " Read the lesson" }),
      el("a", { "class": "mq-ghost", href: "#/map", html: ico("map") + " Map" })]));
    s.appendChild(extra);
    focusMain();
  }
  function spireScreen() {
    var f = D.final, m = f.monster;
    var s = screen("mq-place", "spire");
    var head = el("div", { "class": "mq-place-head" });
    head.innerHTML = sceneSvg("spire");
    head.appendChild(el("div", { "class": "mq-place-title" }, [
      el("p", { "class": "mq-kicker", text: "Final battle" }),
      el("h1", { "class": "mq-h", "data-focus": "1", tabindex: "-1", text: f.name }),
      el("p", { "class": "mq-sub", text: "Questions from every R093 topic" })]));
    s.appendChild(head);
    var guide = el("div", { "class": "mq-guide" });
    var px = pixel("think", "wizard");
    if (px) { var w = el("span", { "class": "mq-guide-art mq-guide-px" }); w.appendChild(px); guide.appendChild(w); }
    guide.appendChild(guideBubble(f.intro, "Pixel"));
    s.appendChild(guide);
    var card = el("article", { "class": "mq-foe-card is-guardian is-final" + (S.final ? " is-won" : "") });
    card.appendChild(el("div", { "class": "mq-foe-art", html: creatureSvg(m.art, { mood: S.final ? "cleared" : "muddle", cls: "is-big" }) }));
    card.appendChild(el("div", { "class": "mq-foe-txt" }, [el("h3", { text: m.name }), el("p", { "class": "mq-small", text: m.muddle }),
      el("p", { "class": "mq-el", style: "--el:" + EL[m.el].colour, html: "Weak to " + elIco(m.el) + " " + EL[m.el].name })]));
    var foot = el("div", { "class": "mq-foe-go" });
    if (S.final) foot.innerHTML = starRow(S.final, 3);
    foot.appendChild(btn("mq-go", S.final ? "Battle again" : "Face the Great Static", function () { startBattle(null, 0); }));
    card.appendChild(foot);
    s.appendChild(card);
    s.appendChild(el("div", { "class": "mq-row" }, [el("a", { "class": "mq-ghost", href: "#/map", html: ico("map") + " Map" })]));
    focusMain();
  }

  /* ------------------------------------------------------------ battle */
  function poolFor(p) {
    var qs;
    if (p) qs = p.qs.map(function (q) { return { q: q, p: p }; });
    else {
      qs = [];
      P.forEach(function (pl) { shuffle(pl.qs).slice(0, 5).forEach(function (q) { qs.push({ q: q, p: pl }); }); });
    }
    var fresh1 = [], old = [];
    qs.forEach(function (x) { ((S.seen[x.p.id] || []).indexOf(x.q.id) > -1 ? old : fresh1).push(x); });
    return shuffle(fresh1).concat(shuffle(old));
  }
  function startBattle(p, n) {
    var kind = p ? (n === 2 ? "guardian" : "wild") : "final";
    var i = p ? placeIndex(p) : P.length;
    var m = p ? p.monsters[n] : D.final.monster;
    var L = levelOf(S.xp);
    B = { p: p, n: n, kind: kind, i: i, m: m, monMax: foeHp(kind, i, L), hp: maxHp(L), maxHp: maxHp(L),
          charge: 0, wrong: 0, right: 0, pool: poolFor(p), qi: 0, busy: false, over: false, L: L };
    B.monHp = B.monMax;
    location.hash = "#/battle";
    battleScreen();
  }
  function endBattle() { clearTimers(); document.removeEventListener("keydown", battleKeys); B = null; }
  var ui = {};
  function battleScreen() {
    var realmId = B.p ? B.p.realm : "spire";
    var s = screen("mq-battle", realmId);
    paintHud();
    var pet = petInfo(S.pet);
    var arena = el("div", { "class": "mq-arena" });
    arena.innerHTML = sceneSvg(realmId);
    ui.foe = el("div", { "class": "mq-foe" });
    ui.foeArt = el("div", { "class": "mq-foe-sprite", html: creatureSvg(B.m.art, { mood: "muddle", cls: B.kind === "final" ? "is-big" : "" }) });
    ui.foeBar = bar("mq-bar-foe");
    ui.foe.appendChild(el("div", { "class": "mq-plate" }, [
      el("p", { "class": "mq-plate-name" }, [el("b", { text: B.m.name }), el("span", { "class": "mq-el", style: "--el:" + EL[B.m.el].colour, html: "Weak to " + elIco(B.m.el) + " " + EL[B.m.el].name })]),
      ui.foeBar.wrap]));
    ui.foe.appendChild(ui.foeArt);
    ui.hero = el("div", { "class": "mq-hero" });
    ui.wiz = el("div", { "class": "mq-wiz-sprite", html: wizardSvg(S.look) });
    ui.pet = el("div", { "class": "mq-pet-sprite", html: pet ? petSvg(pet) : "" });
    ui.heroBar = bar("mq-bar-hero");
    ui.pips = el("span", { "class": "mq-pips", role: "img" });
    ui.hero.appendChild(el("div", { "class": "mq-hero-sprites" }, [ui.pet, ui.wiz]));
    ui.hero.appendChild(el("div", { "class": "mq-plate" }, [
      el("p", { "class": "mq-plate-name" }, [el("b", { text: S.name }), el("span", { "class": "mq-lvchip", text: "Level " + B.L })]),
      ui.heroBar.wrap,
      el("p", { "class": "mq-pet-line" }, [el("span", { text: pet ? pet.name + " " : "" }), ui.pips])]));
    ui.fx = el("div", { "class": "mq-fx", "aria-hidden": "true" });
    ui.speech = el("p", { "class": "mq-speech", hidden: true });
    arena.appendChild(ui.foe); arena.appendChild(ui.hero); arena.appendChild(ui.fx);
    s.appendChild(el("h1", { "class": "mq-sr", text: "Battle: " + B.m.name }));
    s.appendChild(arena);
    s.appendChild(ui.speech);
    ui.panel = el("div", { "class": "mq-panel" });
    s.appendChild(ui.panel);
    paintBars();
    document.addEventListener("keydown", battleKeys);
    speak(B.kind === "final" ? "The Great Static rises from the Spire!" : (B.kind === "guardian" ? "The guardian " : "A wild ") + B.m.name + " appears! " + B.m.muddle);
    say((B.kind === "guardian" ? "Guardian battle. " : B.kind === "final" ? "Final battle. " : "Battle. ") + B.m.name + ": " + B.m.muddle + " Choose a spell.");
    menu();
  }
  function bar(cls) {
    var fill = el("span", { "class": "mq-bar-fill" }), txt = el("span", { "class": "mq-bar-t" });
    var wrap = el("div", { "class": "mq-bar " + cls }, [el("span", { "class": "mq-bar-track" }, [fill]), txt]);
    return { wrap: wrap, fill: fill, txt: txt };
  }
  function paintBars() {
    function set(b, v, max, label) {
      var k = Math.max(0, v) / max;
      b.fill.style.width = (100 * k) + "%";
      b.wrap.classList.toggle("is-low", k <= 0.3);
      b.txt.textContent = Math.max(0, Math.round(v)) + " / " + max;
      b.wrap.setAttribute("aria-label", label + ": " + Math.max(0, Math.round(v)) + " of " + max);
      b.wrap.setAttribute("role", "img");
    }
    set(ui.foeBar, B.monHp, B.monMax, B.m.name + "'s energy");
    set(ui.heroBar, B.hp, B.maxHp, "Your energy");
    ui.pips.innerHTML = [0, 1, 2].map(function (i) { return '<span class="' + (i < B.charge ? "is-on" : "") + '"></span>'; }).join("");
    ui.pips.setAttribute("aria-label", "Pet charge " + B.charge + " of 3");
  }
  function speak(t, who) {
    ui.speech.hidden = false;
    ui.speech.className = "mq-speech" + (who === "hero" ? " is-hero" : "");
    ui.speech.textContent = t;
  }
  function menu() {
    if (!B) return;
    B.busy = false; B.phase = "menu";
    ui.panel.innerHTML = "";
    ui.panel.className = "mq-panel is-menu";
    var dmg = spellDmg(B.L);
    ui.panel.appendChild(el("h2", { "class": "mq-panel-h", text: "Choose a spell" }));
    var grid = el("div", { "class": "mq-spells" });
    ELS.forEach(function (e, k) {
      var weak = e === B.m.el, d = weak ? Math.round(dmg * 1.5) : dmg;
      var b = btn("mq-spell" + (weak ? " is-weak" : ""), "", function () { ask(e); },
        { "aria-label": EL[e].spell + ", " + EL[e].name + ", " + d + " damage" + (weak ? ", hits the weak spot" : "") + ". Key " + (k + 1) });
      b.setAttribute("data-el", e);
      b.innerHTML = '<span class="mq-key" aria-hidden="true">' + (k + 1) + "</span>" + elIco(e) + '<span class="mq-spell-t"><b>' + esc(EL[e].spell) + "</b><span>" + d + " damage" + (weak ? " · weak spot" : "") + "</span></span>";
      grid.appendChild(b);
    });
    var mend = btn("mq-spell is-mend", "", function () { ask("mend"); }, { "aria-label": "Mend, heals " + mendAmount(B.L) + ". Key 5" });
    mend.innerHTML = '<span class="mq-key" aria-hidden="true">5</span>' + ico("mend", "el") + '<span class="mq-spell-t"><b>Mend</b><span>Heals ' + mendAmount(B.L) + "</span></span>";
    grid.appendChild(mend);
    ui.panel.appendChild(grid);
    var row = el("div", { "class": "mq-row mq-row-small" });
    var nPot = S.items.draught + S.items.elixir;
    row.appendChild(btn("mq-ghost", ico("potion") + " Drink a draught (" + nPot + ")", drink, { disabled: nPot ? null : true, "aria-label": "Drink a healing draught. You have " + nPot + ". Key 6" }));
    row.appendChild(btn("mq-ghost", ico("run") + " Run", function () {
      var back = B.p ? "#/place/" + B.p.id : "#/spire";
      endBattle(); say("You ran back to safety."); go(back);
    }));
    ui.panel.appendChild(row);
    var first = grid.querySelector("button");
    setTimeout(function () { if (B && B.phase === "menu" && first && first.isConnected) first.focus({ preventScroll: true }); }, 40);
  }
  function battleKeys(e) {
    if (!B || e.altKey || e.ctrlKey || e.metaKey) return;
    if (e.target && /input|textarea|select/i.test(e.target.tagName)) return;
    var k = e.key;
    if (B.phase === "menu") {
      if (/^[1-6]$/.test(k)) {
        e.preventDefault();
        var n = +k;
        if (n <= 4) ask(ELS[n - 1]); else if (n === 5) ask("mend"); else drink();
      }
    } else if (B.phase === "ask") {
      var map = { "1": 0, "2": 1, "3": 2, "4": 3, a: 0, b: 1, c: 2, d: 3 };
      var i = map[k.toLowerCase()];
      if (i !== undefined && ui.opts && ui.opts[i]) { e.preventDefault(); ui.opts[i].click(); }
    }
  }
  function drink() {
    if (!B || B.busy) return;
    var id = S.items.draught ? "draught" : S.items.elixir ? "elixir" : "";
    if (!id) { toast("You have no healing draughts. Buy them in the shop."); return; }
    if (B.hp >= B.maxHp) { toast("Your energy is already full."); return; }
    S.items[id] -= 1; save(); paintHud();
    var before = B.hp;
    B.hp = Math.min(B.maxHp, B.hp + shopItem("potion", id).heal);
    floatNum(ui.wiz, "+" + (B.hp - before), "is-heal"); sfx("heal");
    paintBars();
    say("You drink a " + shopItem("potion", id).name.toLowerCase() + " and recover " + (B.hp - before) + " energy.");
    menu();
  }
  function nextQ() {
    if (!B.pool.length) B.pool = poolFor(B.p);
    var x = B.pool[B.qi % B.pool.length];
    B.qi += 1;
    return x;
  }
  function ask(spell) {
    if (!B || B.busy || B.phase !== "menu") return;
    sfx("tap");
    B.phase = "ask";
    var x = nextQ(), q = x.q;
    B.cur = { x: x, spell: spell };
    var order = q.f ? q.o.map(function (_, i) { return i; }) : shuffle(q.o.map(function (_, i) { return i; }));
    ui.panel.innerHTML = "";
    ui.panel.className = "mq-panel is-ask";
    var chip = spell === "mend" ? '<span class="mq-cast-chip is-mend">' + ico("mend", "el") + " Mend</span>"
      : '<span class="mq-cast-chip" style="--el:' + EL[spell].colour + '">' + elIco(spell) + " " + esc(EL[spell].spell) + "</span>";
    var head = el("div", { "class": "mq-q-head", html: chip + (B.kind === "final" ? '<span class="mq-q-topic">' + esc(x.p.name) + "</span>" : "") });
    ui.panel.appendChild(head);
    var qh = el("h2", { "class": "mq-q", id: "mq-q", html: q.q, tabindex: "-1" });
    ui.panel.appendChild(qh);
    if (q.i) ui.panel.appendChild(el("p", { "class": "mq-q-item", html: q.i }));
    var opts = el("div", { "class": "mq-opts" + (q.o.length === 2 ? " is-two" : ""), role: "group", "aria-labelledby": "mq-q" });
    ui.opts = [];
    order.forEach(function (oi, k) {
      var b = btn("mq-opt", '<span class="mq-key" aria-hidden="true">' + "ABCD".charAt(k) + '</span><span class="mq-opt-t">' + q.o[oi] + "</span>",
        function () { answer(oi, b); }, { "aria-label": "ABCD".charAt(k) + ": " + plain(q.o[oi]) });
      b._oi = oi;
      ui.opts.push(b);
      opts.appendChild(b);
    });
    ui.panel.appendChild(opts);
    ui.fb = el("div", { "class": "mq-fb", role: "status" });
    ui.panel.appendChild(ui.fb);
    say((q.i ? plain(q.q) + " " + plain(q.i) : plain(q.q)) + " " + ui.opts.length + " answers.");
    setTimeout(function () { if (ui.opts[0]) ui.opts[0].focus({ preventScroll: true }); }, 40);
    if (ui.panel.getBoundingClientRect().bottom > innerHeight) ui.panel.scrollIntoView({ block: "nearest", behavior: calm() ? "auto" : "smooth" });
  }
  function answer(oi, b) {
    if (!B || B.phase !== "ask") return;
    B.phase = "fb";
    var x = B.cur.x, q = x.q, ok = oi === q.a;
    ui.opts.forEach(function (o) {
      o.disabled = true;
      if (o._oi === q.a) o.classList.add("is-right");
      if (o === b && !ok) o.classList.add("is-wrong");
    });
    if (ok) {
      B.right += 1; B.charge = Math.min(3, B.charge + 1);
      var seen = S.seen[x.p.id] || (S.seen[x.p.id] = []);
      if (seen.indexOf(q.id) < 0) { seen.push(q.id); if (seen.length > 400) seen.shift(); }
      sfx("good");
    } else {
      B.wrong += 1; B.charge = 0; sfx("bad");
    }
    paintBars();
    var right = plain(q.o[q.a]);
    ui.fb.className = "mq-fb " + (ok ? "is-ok" : "is-bad");
    ui.fb.innerHTML = '<p class="mq-fb-h">' + (ok ? ico("check") + (B.cur.spell === "mend" ? " Right! Your Mend is ready." : " Right! Your " + esc(EL[B.cur.spell].spell) + " is ready.")
      : "Not quite. The answer is: " + q.o[q.a]) + "</p>" + (q.w ? '<p class="mq-fb-w">' + q.w + "</p>" : ok ? "" : "");
    var cont = btn("mq-go", (ok ? "Cast it" : "Brace yourself") + " " + ico("next"), function () { resolve(ok); });
    ui.fb.appendChild(cont);
    say((ok ? "Right. " : "Not quite. The answer is " + right + ". ") + (q.w ? plain(q.w) : ""));
    setTimeout(function () { cont.focus({ preventScroll: true }); }, 40);
    if (ui.fb.getBoundingClientRect().bottom > innerHeight) ui.fb.scrollIntoView({ block: "nearest", behavior: calm() ? "auto" : "smooth" });
  }
  function resolve(ok) {
    if (!B || B.busy) return;
    B.busy = true; B.phase = "act";
    ui.panel.innerHTML = '<p class="mq-panel-wait">' + (ok ? "Casting..." : B.m.name + " strikes...") + "</p>";
    var spell = B.cur.spell;
    if (ok && spell === "mend") {
      var before = B.hp;
      B.hp = Math.min(B.maxHp, B.hp + mendAmount(B.L));
      ui.wiz.innerHTML = wizardSvg(S.look, { pose: "cast" });
      floatNum(ui.wiz, "+" + (B.hp - before), "is-heal"); sfx("heal");
      speak("You cast Mend and recover " + (B.hp - before) + " energy.", "hero");
      say("You recover " + (B.hp - before) + " energy.");
      paintBars();
      return later(900, function () { ui.wiz.innerHTML = wizardSvg(S.look); petTurn(menu); });
    }
    if (ok) {
      ui.wiz.innerHTML = wizardSvg(S.look, { pose: "cast" });
      sfx("cast");
      bolt(spell, function () {
        var weak = spell === B.m.el, d = weak ? Math.round(spellDmg(B.L) * 1.5) : spellDmg(B.L);
        B.monHp -= d;
        hit(ui.foeArt); floatNum(ui.foeArt, String(d), weak ? "is-crit" : ""); sfx("hit");
        speak(EL[spell].spell + (weak ? " hits the weak spot" : " hits") + " for " + d + "!", "hero");
        say("Your " + EL[spell].spell + " hits " + B.m.name + " for " + d + (weak ? ", a weak spot" : "") + ". " + Math.max(0, B.monHp) + " energy left.");
        paintBars();
        later(650, function () {
          ui.wiz.innerHTML = wizardSvg(S.look);
          if (B.monHp <= 0) return victory();
          petTurn(menu);
        });
      });
      return;
    }
    // a wrong answer: the muddle strikes back
    var dmg = foeHit(B.kind, B.i, B.L);
    lunge(ui.foeArt);
    later(380, function () {
      B.hp -= dmg;
      hurt(ui.wiz); floatNum(ui.wiz, String(dmg), "is-hurt"); sfx("hurt");
      speak(pick(B.m.taunts));
      say(B.m.name + " strikes for " + dmg + ". " + Math.max(0, B.hp) + " energy left.");
      paintBars();
      later(900, function () { if (B.hp <= 0) return defeat(); menu(); });
    });
  }
  function petTurn(done) {
    var pet = petInfo(S.pet);
    if (!pet || B.charge < 3 || B.monHp <= 0) return done();
    B.charge = 0;
    var d = petDmg(pet);
    ui.pet.classList.add("is-special");
    sfx("pet");
    later(420, function () {
      B.monHp -= d;
      hit(ui.foeArt); floatNum(ui.foeArt, String(d), "is-pet"); sfx("hit");
      speak(pet.name + " joins in with a special move for " + d + "!", "hero");
      say(pet.name + "'s special move hits for " + d + ". " + Math.max(0, B.monHp) + " energy left.");
      paintBars();
      later(800, function () {
        ui.pet.classList.remove("is-special");
        if (B.monHp <= 0) return victory();
        done();
      });
    });
  }
  function fxAt(node) {
    var a = ui.fx.getBoundingClientRect(), r = node.getBoundingClientRect();
    return { x: r.left - a.left + r.width / 2, y: r.top - a.top + r.height / 2 };
  }
  function bolt(spell, done) {
    if (calm() || !ui.fx.animate) { done(); return; }
    var from = fxAt(ui.wiz), to = fxAt(ui.foeArt);
    var orb = el("span", { "class": "mq-orb", style: "--el:" + EL[spell].colour, html: elIco(spell) });
    ui.fx.appendChild(orb);
    var anim = orb.animate([
      { transform: "translate(" + from.x + "px," + (from.y - 20) + "px) scale(.6)", opacity: 0.2 },
      { transform: "translate(" + ((from.x + to.x) / 2) + "px," + (Math.min(from.y, to.y) - 60) + "px) scale(1.2)", opacity: 1 },
      { transform: "translate(" + to.x + "px," + to.y + "px) scale(1)", opacity: 1 }], { duration: 520, easing: "ease-in" });
    anim.onfinish = function () {
      orb.remove();
      var boom = el("span", { "class": "mq-boom", style: "--el:" + EL[spell].colour + ";left:" + to.x + "px;top:" + to.y + "px" });
      ui.fx.appendChild(boom);
      setTimeout(function () { boom.remove(); }, 600);
      done();
    };
  }
  function hit(node) { node.classList.remove("is-hit"); void node.offsetWidth; node.classList.add("is-hit"); }
  function hurt(node) { node.classList.remove("is-hurt"); void node.offsetWidth; node.classList.add("is-hurt"); }
  function lunge(node) { node.classList.remove("is-lunge"); void node.offsetWidth; node.classList.add("is-lunge"); }
  function floatNum(node, t, cls) {
    var p = fxAt(node);
    var n = el("span", { "class": "mq-num " + (cls || ""), style: "left:" + p.x + "px;top:" + (p.y - 30) + "px", text: t });
    ui.fx.appendChild(n);
    setTimeout(function () { n.remove(); }, 1300);
  }

  /* ----------------------------------------------------------- results */
  function victory() {
    if (!B || B.over) return;
    B.over = true; B.phase = "done";
    ui.foeArt.innerHTML = creatureSvg(B.m.art, { mood: "cleared", cls: B.kind === "final" ? "is-big" : "" });
    ui.foeArt.classList.add("is-cleared");
    speak(B.m.cleared);
    sfx("win");
    say(B.m.name + " is cleared. " + B.m.cleared);
    ui.panel.innerHTML = "";
    ui.panel.className = "mq-panel is-cleared";
    ui.panel.appendChild(el("h2", { "class": "mq-panel-h", html: ico("check") + " " + esc(B.m.name) + " is cleared" }));
    ui.panel.appendChild(el("p", { "class": "mq-fix", html: '<b>The fix:</b> ' + esc(B.m.cleared) }));
    var c = btn("mq-go", "See your rewards " + ico("next"), rewards);
    ui.panel.appendChild(c);
    setTimeout(function () { c.focus({ preventScroll: true }); }, 60);
  }
  function rewards() {
    var b = B;
    var starsWon = b.wrong === 0 ? 3 : b.wrong <= 2 ? 2 : 1;
    var L0 = levelOf(S.xp), xp = b.right * 10 + WIN_XP[b.kind], coins = b.right * 3 + WIN_COINS[b.kind] + starsWon * 5;
    S.xp += xp; S.coins += coins;
    var L1 = levelOf(S.xp);
    var notes = [];
    var pet = petInfo(S.pet), petBefore = pet;
    if (pet) {
      S.pets[S.pet].xp += PET_XP[b.kind];
      var after = petInfo(S.pet);
      if (after.level > petBefore.level) notes.push({ t: after.name + " reached pet level " + after.level + ".", i: "paw" });
      if (after.starter && after.stage > petBefore.stage) notes.push({ t: petBefore.name + " evolved into " + after.name + "!", i: "star", big: true, pet: after });
    }
    if (L1 > L0) notes.push({ t: "Level up! You are now level " + L1 + ": more energy and stronger spells.", i: "star", big: true });
    var firstClear = false, opened = null, spire = false;
    if (b.p) {
      var row = (S.places[b.p.id] || [0, 0, 0]).slice();
      var wasCleared = row[2] > 0;
      row[b.n] = Math.max(row[b.n], starsWon);
      S.places[b.p.id] = row;
      if (b.n === 2 && !wasCleared) {
        firstClear = true;
        S.pets[b.m.id] = S.pets[b.m.id] || { xp: 0 };
        notes.push({ t: b.m.name + " is cleared for good and joins you as a pet called " + b.m.tamed + "!", i: "paw", big: true, pet: petInfo(b.m.id) });
        notes.push({ t: "Spellbook page unlocked: " + b.p.topic + ".", i: "book" });
        var nx = P[b.i + 1];
        if (clearedCount() === P.length) { spire = true; notes.push({ t: "Every place is clear. The Studio Spire is open!", i: "flag", big: true }); }
        else if (nx && !S.free && !cleared(nx)) { opened = nx; notes.push({ t: "New place open: " + nx.name + ".", i: "map" }); }
      }
    } else {
      if (!S.final) notes.push({ t: "You cleared the Great Static. The Media Realms are saved!", i: "flag", big: true });
      S.final = Math.max(S.final, starsWon);
    }
    save(); paintHud();
    if (L1 > L0 || notes.some(function (n) { return n.big; })) sfx("level");
    var back = el("div", { "class": "mq-modal-back" });
    var dlg = el("div", { "class": "mq-modal mq-results", role: "dialog", "aria-modal": "true", "aria-labelledby": "mq-res-h" });
    dlg.appendChild(el("h2", { id: "mq-res-h", tabindex: "-1", text: b.kind === "final" ? "Victory over the Static!" : "Victory!" }));
    dlg.appendChild(el("div", { "class": "mq-res-stars", role: "img", "aria-label": starsWon + " of 3 stars", html: starRow(starsWon, 3, "is-big") }));
    dlg.appendChild(el("p", { "class": "mq-small", text: b.right + " right, " + b.wrong + " wrong. " + (starsWon === 3 ? "Flawless!" : starsWon === 2 ? "Two or fewer slips earns two stars." : "Fewer slips earns more stars.") }));
    dlg.appendChild(el("div", { "class": "mq-res-row" }, [
      el("span", { "class": "mq-chip is-xp", html: ico("star") + " +" + xp + " XP" }),
      el("span", { "class": "mq-chip", html: ico("coin") + " +" + coins + " coins" }),
      pet ? el("span", { "class": "mq-chip", html: ico("paw") + " +" + PET_XP[b.kind] + " pet XP" }) : null]));
    notes.forEach(function (n) {
      var row = el("p", { "class": "mq-note" + (n.big ? " is-big" : ""), html: ico(n.i) + " " + esc(n.t) });
      if (n.pet) { var art = el("span", { "class": "mq-note-art", html: petSvg(n.pet) }); row.insertBefore(art, row.firstChild); }
      dlg.appendChild(row);
    });
    var go1 = el("div", { "class": "mq-row" });
    var nextN = b.p && b.n < 2 ? b.n + 1 : -1;
    if (b.p && nextN > -1) go1.appendChild(btn("mq-go", "Next battle: " + esc(b.p.monsters[nextN].name), function () { close(); startBattle(b.p, nextN); }));
    else if (opened) go1.appendChild(btn("mq-go", "Go to " + esc(opened.name), function () { close(); go("#/place/" + opened.id); }));
    else if (spire && !S.final) go1.appendChild(btn("mq-go", "To the Studio Spire", function () { close(); go("#/spire"); }));
    go1.appendChild(btn(go1.children.length ? "mq-ghost" : "mq-go", b.p ? "Back to " + esc(b.p.name) : "Back to the map", function () { close(); go(b.p ? "#/place/" + b.p.id : "#/map"); }));
    dlg.appendChild(go1);
    back.appendChild(dlg);
    app.appendChild(back);
    if (b.kind === "final" || firstClear) confetti(back);
    function close() { back.remove(); endBattle(); }
    say("Victory. " + starsWon + " of 3 stars. " + xp + " XP and " + coins + " coins. " + notes.map(function (n) { return n.t; }).join(" "));
    setTimeout(function () { var f = dlg.querySelector(".mq-go"); if (f) f.focus({ preventScroll: true }); }, 60);
  }
  function defeat() {
    if (!B || B.over) return;
    B.over = true; B.phase = "done";
    var b = B, xp = b.right * 5;
    S.xp += xp; save(); paintHud();
    sfx("lose");
    var back = el("div", { "class": "mq-modal-back" });
    var dlg = el("div", { "class": "mq-modal mq-results is-lost", role: "dialog", "aria-modal": "true", "aria-labelledby": "mq-res-h" });
    var px = pixel("think", "wizard");
    if (px) { var w = el("span", { "class": "mq-res-px" }); w.appendChild(px); dlg.appendChild(w); }
    dlg.appendChild(el("h2", { id: "mq-res-h", tabindex: "-1", text: "Out of energy" }));
    dlg.appendChild(el("p", { text: "Pixel pulls you back to safety. " + b.m.name + " is still muddled, but every answer you read is a step closer." }));
    if (xp) dlg.appendChild(el("p", { "class": "mq-small", text: "You still earned " + xp + " XP for your right answers." }));
    dlg.appendChild(el("p", { "class": "mq-small", text: "Tip: Mend and healing draughts restore energy. Read each explanation, then try again." }));
    var row = el("div", { "class": "mq-row" });
    row.appendChild(btn("mq-go", "Try again", function () { back.remove(); endBattle(); startBattle(b.p, b.n); }));
    row.appendChild(btn("mq-ghost", b.p ? "Back to " + esc(b.p.name) : "Back to the map", function () { back.remove(); endBattle(); go(b.p ? "#/place/" + b.p.id : "#/spire"); }));
    dlg.appendChild(row);
    back.appendChild(dlg);
    app.appendChild(back);
    say("Out of energy. Try again, or go back.");
    setTimeout(function () { var f = dlg.querySelector(".mq-go"); if (f) f.focus({ preventScroll: true }); }, 60);
  }
  function confetti(host) {
    if (calm()) return;
    var c = el("canvas", { "class": "mq-confetti", "aria-hidden": "true" });
    host.appendChild(c);
    var ctx = c.getContext && c.getContext("2d");
    if (!ctx) return;
    var W = c.clientWidth, H = c.clientHeight, dpr = Math.min(2, window.devicePixelRatio || 1), t0 = performance.now(), parts = [];
    c.width = W * dpr; c.height = H * dpr; ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    var cols = ["#C026D3", "#F59E0B", "#0D9488", "#2563EB", "#FDE047", "#F472B6", "#fff"];
    for (var i = 0; i < 140; i++) parts.push({ x: W / 2, y: H / 3, vx: (Math.random() - 0.5) * 16, vy: -Math.random() * 12 - 2, r: Math.random() * 6 + 4, a: Math.random() * 6, c: cols[i % cols.length] });
    (function frame(t) {
      var age = t - t0;
      ctx.clearRect(0, 0, W, H);
      parts.forEach(function (p) {
        p.vy += 0.3; p.x += p.vx; p.y += p.vy; p.a += 0.1;
        ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.a); ctx.globalAlpha = Math.max(0, 1 - age / 2400); ctx.fillStyle = p.c;
        ctx.fillRect(-p.r / 2, -p.r / 4, p.r, p.r / 2); ctx.restore();
      });
      if (age < 2400 && c.isConnected) requestAnimationFrame(frame); else c.remove();
    })(t0);
  }

  /* --------------------------------------------------------------- pets */
  function petsScreen() {
    var s = screen("mq-pets", "vale");
    s.appendChild(el("h1", { "class": "mq-h", "data-focus": "1", tabindex: "-1", text: "Your pets" }));
    s.appendChild(el("p", { "class": "mq-sub", text: "Your active pet fights beside you and earns pet XP from every win. Starter pets evolve at pet level 4 and pet level 8. Clear a guardian and it joins you too." }));
    var grid = el("div", { "class": "mq-pet-grid" });
    var ids = Object.keys(S.pets);
    ids.forEach(function (id) {
      var info = petInfo(id);
      if (!info) return;
      var active = S.pet === id;
      var card = el("article", { "class": "mq-pet-card" + (active ? " is-active" : ""), style: "--el:" + EL[info.el].colour });
      card.innerHTML = '<span class="mq-pet-art">' + petSvg(info) + "</span>";
      var have = info.xp - 40 * (info.level - 1);
      card.appendChild(el("h2", { "class": "mq-pet-name", text: info.name }));
      card.appendChild(el("p", { "class": "mq-el", style: "--el:" + EL[info.el].colour, html: elIco(info.el) + " " + EL[info.el].name + " · Pet level " + info.level }));
      if (info.level < 20) card.appendChild(el("div", { "class": "mq-xp is-pet", role: "img", "aria-label": have + " of 40 pet XP to the next level" }, [el("span", { "class": "mq-xp-fill", style: "width:" + Math.round(100 * have / 40) + "%" })]));
      card.appendChild(el("p", { "class": "mq-small", text: info.about }));
      if (info.starter) {
        var st = starter(id);
        card.appendChild(el("p", { "class": "mq-small", text: info.stage < 2 ? "Evolves into " + st.stages[info.stage + 1] + " at pet level " + (info.stage === 0 ? 4 : 8) + "." : "Fully evolved." }));
      }
      card.appendChild(el("p", { "class": "mq-small", text: "Special move: " + petDmg(info) + " damage after three right answers in a row." }));
      card.appendChild(active ? el("p", { "class": "mq-active", html: ico("check") + " In your party" })
        : btn("mq-go is-small", "Take into battle", function () { S.pet = id; save(); toast(info.name + " joins your party."); sfx("pet"); petsScreen(); }));
      if (S.items.biscuit && active) card.appendChild(btn("mq-ghost is-small", "Feed a Pixel biscuit (" + S.items.biscuit + ")", function () {
        S.items.biscuit -= 1; S.pets[id].xp += 40; save(); sfx("pet"); toast(info.name + " loved it: +40 pet XP."); petsScreen();
      }));
      grid.appendChild(card);
    });
    P.forEach(function (p) {
      var g = p.monsters[2];
      if (S.pets[g.id]) return;
      grid.appendChild(el("article", { "class": "mq-pet-card is-locked" }, [
        el("span", { "class": "mq-pet-art is-shadow", html: creatureSvg(g.art, { mood: "friendly" }) }),
        el("h2", { "class": "mq-pet-name", text: "Not yet befriended" }),
        el("p", { "class": "mq-small", text: "Clear " + g.name + " at " + p.name + " to befriend it." })]));
    });
    s.appendChild(grid);
    focusMain();
  }

  /* --------------------------------------------------------------- shop */
  var SHOP_TABS = [["potion", "Potions and treats"], ["hat", "Hats"], ["robe", "Robes"], ["wand", "Wands"]];
  function shopScreen(tab) {
    if (!D.shop[tab]) tab = "potion";
    var s = screen("mq-shop", "coast");
    s.appendChild(el("h1", { "class": "mq-h", "data-focus": "1", tabindex: "-1", text: "The Market" }));
    s.appendChild(el("p", { "class": "mq-sub", html: "Spend the coins you win in battle. You have " + ico("coin") + " <b>" + fmt(S.coins) + "</b> coins." }));
    var tabs = el("div", { "class": "mq-tabs", role: "tablist", "aria-label": "Market stalls" });
    SHOP_TABS.forEach(function (t) {
      tabs.appendChild(el("a", { "class": "mq-tab" + (t[0] === tab ? " is-on" : ""), href: "#/shop/" + t[0], role: "tab", "aria-selected": String(t[0] === tab), text: t[1] }));
    });
    s.appendChild(tabs);
    var grid = el("div", { "class": "mq-shop-grid", role: "tabpanel" });
    D.shop[tab].forEach(function (it) {
      var card = el("article", { "class": "mq-item" });
      var art = el("span", { "class": "mq-item-art" });
      if (tab === "potion") art.innerHTML = it.id === "biscuit" ? '<svg viewBox="0 0 24 24" class="mq-i" aria-hidden="true"><circle cx="12" cy="12" r="9" fill="#D97706"/><circle cx="9" cy="9" r="1.4" fill="#78350F"/><circle cx="15" cy="11" r="1.4" fill="#78350F"/><circle cx="11" cy="15" r="1.4" fill="#78350F"/></svg>' : ico("potion");
      else art.innerHTML = wizardSvg(Object.assign({}, S.look, tab === "hat" ? { hat: it.id } : tab === "robe" ? { robe: it.id } : { wand: it.id }), { pose: tab === "wand" ? "cast" : "" });
      card.appendChild(art);
      card.appendChild(el("h2", { "class": "mq-item-name", text: it.name }));
      if (it.about) card.appendChild(el("p", { "class": "mq-small", text: it.about }));
      if (tab === "potion") {
        card.appendChild(el("p", { "class": "mq-small", text: "You have " + (S.items[it.id] || 0) + "." }));
        card.appendChild(buyBtn(it, function () { S.items[it.id] = (S.items[it.id] || 0) + 1; }));
      } else {
        var have = owns(tab, it.id), on = S.look[tab] === it.id;
        if (on) card.appendChild(el("p", { "class": "mq-active", html: ico("check") + " Wearing" }));
        else if (have) card.appendChild(btn("mq-go is-small", "Wear it", function () { S.look[tab] = it.id; save(); paintHud(); sfx("tap"); shopScreen(tab); }));
        else card.appendChild(buyBtn(it, function () { S.owned[tab].push(it.id); S.look[tab] = it.id; }));
      }
      grid.appendChild(card);
    });
    s.appendChild(grid);
    focusMain();
    function buyBtn(it, give) {
      var can = S.coins >= it.price;
      return btn("mq-go is-small" + (can ? "" : " is-off"), ico("coin") + " Buy for " + it.price, function () {
        if (S.coins < it.price) { toast("You need " + (it.price - S.coins) + " more coins. Win battles to earn them."); return; }
        S.coins -= it.price; give(); save(); paintHud(); sfx("coin"); toast("Bought: " + it.name + "."); shopScreen(tab);
      }, { "aria-label": "Buy " + it.name + " for " + it.price + " coins" + (can ? "" : ". Not enough coins yet") });
    }
  }

  /* ---------------------------------------------------------- spellbook */
  function bookScreen() {
    var s = screen("mq-book", "peaks");
    s.appendChild(el("h1", { "class": "mq-h", "data-focus": "1", tabindex: "-1", text: "Your spellbook" }));
    s.appendChild(el("p", { "class": "mq-sub", text: "One page for every place you reach: its key terms, and the fix for every muddle you clear. Revise from it before a battle, or before the exam." }));
    var list = el("ol", { "class": "mq-book-list" });
    P.forEach(function (p, i) {
      var open = unlocked(p);
      var li = el("li", {});
      if (open) li.appendChild(el("a", { "class": "mq-book-row", href: "#/book/" + p.id, style: "--rc:" + realm(p.realm).colour,
                                          html: '<span class="mq-node-dot">' + (i + 1) + '</span><span class="mq-trail-t"><b>' + esc(p.name) + "</b><span>" + esc(p.spec + ": " + p.topic) + "</span></span>" + (cleared(p) ? ico("check") : "") }));
      else li.appendChild(el("p", { "class": "mq-book-row is-locked", html: '<span class="mq-node-dot">' + ico("lock") + '</span><span class="mq-trail-t"><b>A sealed page</b><span>Reach ' + esc(p.name) + " to open it</span></span>" }));
      list.appendChild(li);
    });
    s.appendChild(list);
    focusMain();
  }
  function bookPage(p) {
    if (!unlocked(p)) { toast("Reach " + p.name + " to open this page."); return bookScreen(); }
    var s = screen("mq-book", p.realm);
    s.appendChild(el("p", { "class": "mq-kicker", text: p.spec }));
    s.appendChild(el("h1", { "class": "mq-h", "data-focus": "1", tabindex: "-1", text: p.topic }));
    var dl = el("dl", { "class": "mq-terms" });
    p.terms.forEach(function (t) { dl.appendChild(el("dt", { text: t[0] })); dl.appendChild(el("dd", { text: t[1] })); });
    s.appendChild(el("h2", { "class": "mq-h2", text: "Key terms" }));
    s.appendChild(dl);
    s.appendChild(el("h2", { "class": "mq-h2", text: "Muddles and their fixes" }));
    var ul = el("ul", { "class": "mq-muddles" });
    p.monsters.forEach(function (m, n) {
      var won = stars(p)[n] > 0;
      ul.appendChild(el("li", { "class": won ? "is-won" : "" }, [
        el("span", { "class": "mq-muddle-art", html: creatureSvg(m.art, { mood: won ? "cleared" : "muddle" }) }),
        el("div", {}, [el("b", { text: m.name }), el("p", { html: '<span class="mq-muddle">Muddle:</span> ' + esc(m.muddle) }),
          el("p", { html: won ? '<span class="mq-fixl">Fix:</span> ' + esc(m.cleared) : '<span class="mq-fixl">Fix:</span> clear ' + esc(m.name) + " to reveal it." })])]));
    });
    s.appendChild(ul);
    s.appendChild(el("div", { "class": "mq-row" }, [
      el("a", { "class": "mq-go", href: "#/place/" + p.id, html: ico("next") + " Go to " + esc(p.name) }),
      el("a", { "class": "mq-ghost", href: p.url, html: ico("book") + " Read the full lesson" }),
      el("a", { "class": "mq-ghost", href: "#/book", html: ico("back") + " All pages" })]));
    focusMain();
  }

  /* ----------------------------------------------------------- settings */
  function settingsScreen() {
    var s = screen("mq-settings", "isles");
    s.appendChild(el("h1", { "class": "mq-h", "data-focus": "1", tabindex: "-1", text: "Settings" }));
    var box = el("div", { "class": "mq-settings-box" });
    function toggle(label, help, on, fn) {
      var b = btn("mq-toggle" + (on ? " is-on" : ""), '<span class="mq-toggle-k" aria-hidden="true"></span><span><b>' + esc(label) + "</b><span>" + esc(help) + "</span></span>", fn, { role: "switch", "aria-checked": String(!!on) });
      return b;
    }
    box.appendChild(toggle("Sound effects", "Short sounds for spells, hits and wins.", S.sound, function () { S.sound = !S.sound; save(); paintHud(); settingsScreen(); }));
    box.appendChild(toggle("Explore freely", "Open every place and battle now, for revising one topic in any order.", S.free, function () { S.free = !S.free; save(); toast(S.free ? "Every place is open." : "Places open in order again."); settingsScreen(); }));
    s.appendChild(box);
    s.appendChild(el("p", { "class": "mq-small", text: calm() ? "Your device asks for reduced motion, so the battle animations are kept short and still." : "Animations follow your device's motion setting." }));
    s.appendChild(el("div", { "class": "mq-row" }, [
      el("a", { "class": "mq-go", href: "#/look", html: ico("star") + " Change your look" }),
      el("a", { "class": "mq-ghost", href: "#/story", html: ico("book") + " Read the story again" })]));
    s.appendChild(el("h2", { "class": "mq-h2", text: "Your progress" }));
    s.appendChild(el("p", { "class": "mq-small", text: S.name + " is level " + levelOf(S.xp) + " with " + fmt(S.xp) + " XP, " + clearedCount() + " of " + P.length + " places cleared and " + Object.keys(S.pets).length + " pets. Progress is saved in this browser only, so it stays on this device." }));
    s.appendChild(el("div", { "class": "mq-row" }, [btn("mq-ghost is-danger", "Wipe progress and start again", function () {
      confirmBox("Wipe " + S.name + "'s progress from this browser? This cannot be undone.", "Wipe progress", function () { store.clear(); S = null; paintHud(); go("#/new"); });
    })]));
    focusMain();
  }

  window.addEventListener("hashchange", route);
  route();
})();
