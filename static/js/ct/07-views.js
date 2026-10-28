/* The adventure's screens: the island map, each world's path, the Me page and
 * the daily challenge. A small heads-up bar above them all shows stars, XP and
 * badges, and holds the sound switch.
 */
(function (root) {
  "use strict";
  var CT = root.CT = root.CT || {};
  var V = CT.views = {};

  // ------------------------------------------------------------------ HUD
  V.hud = function (bar) {
    function render() {
      var t = CT.progress.totals(), b = CT.progress.badges().length;
      var snd = CT.store.state.settings.sound;
      CT.clear(bar);
      CT.append(bar, [
        CT.el("a", { class: "ct-hud-home", href: "#/" }, [CT.ui("map"), " Adventure map"]),
        CT.el("div", { class: "ct-hud-stats" }, [
          CT.el("span", { class: "ct-hud-chip", title: "Stars" }, [CT.ico("star"), " ", CT.el("b", null, String(t.stars)), CT.el("span", { class: "sr-only" }, " stars")]),
          CT.el("span", { class: "ct-hud-chip", title: "XP" }, [CT.ico("bolt"), " ", CT.el("b", null, String(t.xp)), " XP"]),
          CT.el("span", { class: "ct-hud-chip", title: "Badges" }, [CT.ico("medal"), " ", CT.el("b", null, String(b)), CT.el("span", { class: "sr-only" }, " badges")]),
          CT.el("span", { class: "ct-hud-chip ct-hud-pct", title: "Levels complete" }, [CT.el("b", null, t.pct + "%"), " done"])
        ]),
        CT.el("div", { class: "ct-hud-btns" }, [
          CT.el("button", { type: "button", class: "ct-hud-btn", "aria-pressed": snd ? "true" : "false",
            "aria-label": snd ? "Sound on. Turn sound off" : "Sound off. Turn sound on",
            onclick: function () {
              CT.store.state.settings.sound = !CT.store.state.settings.sound;
              CT.store.saveSettings(); render();
              CT.sound.play("good");
            } }, CT.ui(snd ? "sound" : "mute")),
          CT.el("a", { class: "ct-hud-btn", href: "#/daily", "aria-label": "Daily challenge" }, CT.ico(CT.daily.doneToday() ? "tick" : "bolt")),
          CT.el("a", { class: "ct-hud-btn ct-hud-me", href: "#/me", "aria-label": "Me" }, [CT.ui("user"), CT.el("span", null, " Me")])
        ])
      ]);
    }
    CT.on("hud", render);
    render();
  };

  function heading(h) { setTimeout(function () { if (h && h.focus) h.focus({ preventScroll: true }); }, 30); }

  // --------------------------------------------------------- island map
  var ISLES = {
    decomposition: { x: 205, y: 395, draw: function (c) {
      return '<path d="M-130 30 q10 -60 90 -66 q70 -28 130 6 q60 10 50 62 q-10 40 -120 42 q-130 6 -150 -44z" fill="#FCD9A8"/>' +
        '<path d="M-118 26 q14 -46 82 -52 q66 -24 120 6 q50 10 44 46" fill="none" stroke="#fff" stroke-opacity=".55" stroke-width="5"/>' +
        '<rect x="-70" y="-40" width="34" height="40" rx="3" fill="' + c.colour + '"/><rect x="-30" y="-58" width="40" height="58" rx="3" fill="#FB923C"/>' +
        '<rect x="16" y="-30" width="30" height="30" rx="3" fill="#FDBA74"/><path d="M60 -96 v96 M60 -96 h-70 M50 -96 l10 -10 l10 10" stroke="#9A3412" stroke-width="5" fill="none"/>' +
        '<path d="M-6 -96 v28" stroke="#9A3412" stroke-width="2"/><rect x="-16" y="-68" width="20" height="14" fill="#F59E0B"/>';
    } },
    abstraction: { x: 430, y: 185, draw: function (c) {
      return '<path d="M-140 40 q0 -50 80 -60 q60 -30 140 -6 q70 16 60 64 q-20 34 -140 34 q-130 4 -140 -32z" fill="#BBF7D0"/>' +
        '<path d="M-110 30 L-50 -70 L0 10 L40 -40 L100 30 Z" fill="' + c.colour + '"/><path d="M-50 -70 l-18 30 l18 -6 l16 8z M40 -40 l-12 18 l12 -4 l12 6z" fill="#fff"/>' +
        '<path d="M-110 30 L-50 -70 L0 10" fill="none" stroke="#075985" stroke-width="3" stroke-opacity=".4"/>' +
        '<g transform="translate(70 -2)"><rect x="-4" y="-34" width="8" height="34" fill="#475569"/><rect x="-18" y="-46" width="36" height="14" rx="7" fill="#0EA5E9" transform="rotate(-20)"/></g>';
    } },
    patterns: { x: 665, y: 390, draw: function (c) {
      return '<path d="M-130 34 q-6 -54 80 -64 q70 -30 140 0 q66 18 50 60 q-14 36 -130 38 q-130 4 -140 -34z" fill="#E9D5FF"/>' +
        '<path d="M-70 20 l18 -70 l18 70z" fill="' + c.colour + '"/><path d="M-30 20 l14 -50 l14 50z" fill="#C084FC"/><path d="M6 20 l20 -86 l20 86z" fill="#A855F7"/>' +
        '<path d="M50 20 l14 -48 l14 48z" fill="#D8B4FE"/><path d="M-52 -50 l-6 30 M26 -66 l-8 40" stroke="#fff" stroke-width="3" stroke-opacity=".7"/>' +
        '<path d="M-110 26 q40 -20 80 0 t80 0 t80 0" fill="none" stroke="#6B21A8" stroke-width="3" stroke-dasharray="2 8" stroke-linecap="round"/>';
    } },
    algorithms: { x: 845, y: 165, draw: function (c) {
      return '<path d="M-120 40 q0 -50 70 -62 q70 -26 140 4 q50 16 40 58 q-20 30 -120 32 q-120 4 -130 -32z" fill="#A7F3D0"/>' +
        '<rect x="-80" y="-70" width="34" height="80" rx="3" fill="' + c.colour + '"/><rect x="-40" y="-100" width="40" height="110" rx="3" fill="#10B981"/>' +
        '<rect x="6" y="-56" width="34" height="66" rx="3" fill="#34D399"/><g fill="#D1FAE5">' +
        '<rect x="-74" y="-60" width="8" height="8"/><rect x="-60" y="-60" width="8" height="8"/><rect x="-74" y="-44" width="8" height="8"/><rect x="-32" y="-90" width="8" height="8"/><rect x="-16" y="-90" width="8" height="8"/><rect x="-32" y="-72" width="8" height="8"/><rect x="14" y="-46" width="8" height="8"/><rect x="26" y="-46" width="8" height="8"/></g>' +
        '<g transform="translate(70 -24)"><circle r="16" fill="none" stroke="#065F46" stroke-width="7" stroke-dasharray="6 4"/><circle r="6" fill="#065F46"/></g>';
    } }
  };

  V.mapSvg = function () {
    var worlds = CT.data.worlds;
    var cur = currentWorld();
    var s = ['<svg class="ct-map-svg" viewBox="0 0 1000 560" role="group" aria-labelledby="ct-map-t">',
      '<title id="ct-map-t">The adventure map: four island worlds joined by a dotted sea route</title>',
      '<defs><linearGradient id="ct-sea" x1="0" y1="0" x2="0" y2="1"><stop offset="0" class="sea-a"/><stop offset="1" class="sea-b"/></linearGradient></defs>',
      '<rect width="1000" height="560" rx="28" fill="url(#ct-sea)"/>',
      '<g class="ct-waves">'];
    for (var i = 0; i < 14; i++) {
      var wx = 40 + (i * 137) % 920, wy = 40 + (i * 89) % 480;
      s.push('<path d="M' + wx + ' ' + wy + ' q10 -8 20 0 t20 0" />');
    }
    s.push('</g><path class="ct-route" d="M205 395 C300 340 330 230 430 185 C540 140 560 330 665 390 C760 440 780 230 845 165"/>');
    worlds.forEach(function (w) {
      var I = ISLES[w.id], p = CT.progress.world(w.id);
      s.push('<a href="#/world/' + w.id + '" class="ct-isle" aria-label="World ' + w.n + ': ' + w.name + ', ' + w.place + '. ' + p.done + ' of ' + p.total + ' levels done.">' +
        '<g transform="translate(' + I.x + ' ' + I.y + ')">' + I.draw(w) +
        '<g transform="translate(0 72)"><rect x="-92" y="-20" width="184" height="46" rx="14" fill="#fff" stroke="' + w.colour + '" stroke-width="3"/>' +
        '<text x="0" y="-1" class="ct-isle-name" fill="' + w.deep + '">' + w.n + '. ' + w.place + '</text>' +
        '<text x="0" y="17" class="ct-isle-sub">' + w.name + ' · ' + p.done + '/' + p.total + '</text></g>' +
        (p.complete ? '<g transform="translate(78 -64)"><circle r="18" fill="#F5B700" stroke="#C98A00" stroke-width="3"/><path d="M-8 0 l5 6 l11 -12" stroke="#fff" stroke-width="4" fill="none" stroke-linecap="round"/></g>' : '') +
        '</g></a>');
    });
    s.push('</svg>');
    var wrap = CT.el("div", { class: "ct-map" });
    wrap.innerHTML = s.join("");
    // Pixel stands by the island the student is working on.
    if (cur) {
      var I = ISLES[cur.id], px = new CT.Pixel({ mood: "wave", label: "Pixel is waiting at " + cur.place });
      var pin = CT.el("div", { class: "ct-map-pixel", style: { left: ((I.x - 95) / 10) + "%", top: ((I.y - 128) / 5.6) + "%" } }, [px.svg]);
      wrap.appendChild(pin);
    }
    return wrap;
  };

  function currentWorld() {
    var last = CT.store.state.last && CT.byId(CT.data.levels, CT.store.state.last);
    if (last && !CT.progress.world(last.world).complete) return CT.byId(CT.data.worlds, last.world);
    for (var i = 0; i < CT.data.worlds.length; i++) if (!CT.progress.world(CT.data.worlds[i].id).complete) return CT.data.worlds[i];
    return CT.data.worlds[CT.data.worlds.length - 1];
  }
  function continueLevel() {
    var last = CT.store.state.last && CT.byId(CT.data.levels, CT.store.state.last);
    if (last && !CT.progress.done(last.id)) return last;
    var w = currentWorld();
    return w ? CT.progress.nextIn(w.id) : null;
  }

  V.home = function (host) {
    var t = CT.progress.totals();
    var next = continueLevel();
    var greet = t.done === 0 ? "Welcome, explorer! I'm Pixel. Pick an island and let's start thinking like computer scientists."
      : (t.done === t.total ? "Champion! Replay any level to collect more stars." : "Welcome back! " + t.done + " levels done. Ready for the next one?");
    var comp = CT.companion({ mood: "wave", say: greet, cls: "ct-home-pal" });
    var ready = CT.progress.chestsReady();
    var h1 = CT.el("h1", { class: "ct-home-h", tabindex: "-1" }, ["Think Like a Computer Scientist.", CT.el("span", null, " Play. Solve. Level Up!")]);
    CT.append(host, [
      CT.el("section", { class: "ct-hero" }, [
        CT.el("div", { class: "ct-hero-text" }, [
          CT.el("p", { class: "ct-kicker" }, "Computational Thinking Adventure"),
          h1,
          CT.el("div", { class: "ct-hero-btns" }, [
            next ? CT.el("a", { class: "ct-btn ct-btn-big", href: "#/play/" + next.id }, (t.done ? "Continue: " : "Start: ") + CT.byId(CT.data.worlds, next.world).name + " " + next.n) : null,
            CT.el("a", { class: "ct-btn ct-btn-soft", href: "#/daily" }, CT.daily.doneToday() ? "Daily challenge done" : "Daily challenge")
          ])
        ]),
        comp.el
      ]),
      V.mapSvg(),
      CT.el("div", { class: "ct-worlds" }, CT.data.worlds.map(function (w) {
        var p = CT.progress.world(w.id), nx = CT.progress.nextIn(w.id);
        return CT.el("a", { class: "ct-world-card", href: "#/world/" + w.id, style: { "--w": w.colour, "--wl": w.light, "--wd": w.deep } }, [
          CT.el("span", { class: "ct-world-n" }, "World " + w.n),
          CT.el("h2", null, w.name),
          CT.el("p", { class: "ct-world-tag" }, w.tag),
          CT.el("div", { class: "ct-bar", role: "progressbar", "aria-valuemin": "0", "aria-valuemax": String(p.total), "aria-valuenow": String(p.done), "aria-label": w.name + " progress" },
            CT.el("i", { style: { width: (p.total ? 100 * p.done / p.total : 0) + "%" } })),
          CT.el("p", { class: "ct-world-meta" }, p.done + " of " + p.total + " levels · " + p.stars + " of " + p.maxStars + " stars"),
          CT.el("p", { class: "ct-world-next" }, p.complete ? "Complete" : (nx ? "Next: " + nx.title : ""))
        ]);
      })),
      CT.el("section", { class: "ct-extras", "aria-label": "More to explore" }, [
        extra("#/daily", "bolt", "Daily challenge", CT.daily.doneToday() ? "Done today. Streak: " + CT.store.state.daily.streak : ""),
        extra("#/me", "gift", "Treasure chests", ready.length ? ready.length + " ready to open" : ""),
        extra("#/lab/flowchart", "flowchart", "Flowchart Lab", ""),
        extra("#/lab/pseudocode", "keyboard", "Pseudocode Playground", ""),
        extra("#/me", "medal", "Badges and certificates", CT.progress.badges().length + " of " + CT.data.badges.length + " badges"),
        extra("/computational-thinking/teacher/", "apple", "Teacher mode", "")
      ])
    ]);
    if (ready.length) comp.say("A treasure chest is ready! Open it on your Me page.", "happy");
    heading(h1);
  };
  function extra(href, icon, title, text) {
    return CT.el("a", { class: "ct-extra", href: href }, [CT.el("span", { class: "ct-extra-i", "aria-hidden": "true" }, CT.ico(icon)),
      CT.el("span", null, [CT.el("b", null, title), text ? CT.el("small", null, text) : null])]);
  }

  // --------------------------------------------------------- world path
  V.world = function (host, wid) {
    var w = CT.byId(CT.data.worlds, wid);
    if (!w) { location.hash = "#/"; return; }
    var levels = CT.data.levels.filter(function (l) { return l.world === wid; });
    var p = CT.progress.world(wid), nx = CT.progress.nextIn(wid);
    var badge = CT.byId(CT.data.badges, w.badge), earned = CT.progress.badgeEarned(badge);
    host.style.setProperty("--w", w.colour); host.style.setProperty("--wl", w.light); host.style.setProperty("--wd", w.deep);
    var h1 = CT.el("h1", { tabindex: "-1" }, [w.name + ": ", CT.el("span", null, w.tag)]);
    var comp = CT.companion({ mood: p.complete ? "proud" : "wave", cls: "ct-world-pal",
      say: p.complete ? "You conquered " + w.place + "! Replay any level to earn more stars." :
        (p.done ? "Next up: " + nx.title + "." : "Welcome to " + w.place + "!") });
    var path = CT.el("div", { class: "ct-path", role: "list", "aria-label": w.name + " levels" });
    CT.append(host, [
      CT.el("header", { class: "ct-world-head" }, [
        CT.el("a", { class: "ct-back", href: "#/" }, "← Adventure map"),
        CT.el("div", { class: "ct-world-title" }, [CT.el("p", { class: "ct-kicker" }, "World " + w.n + " · " + w.place), h1, CT.el("p", { class: "ct-lead" }, w.about)]),
        CT.el("div", { class: "ct-world-stats" }, [
          ring(p.done, p.total), CT.el("div", null, [CT.el("b", null, [CT.ico("star"), " " + p.stars + " / " + p.maxStars]), CT.el("small", null, "stars")]),
          CT.el("div", { class: "ct-world-badge" + (earned ? " is-earned" : "") }, [CT.celebrate.badgeArt(earned ? w : { colour: "#94A3B8", deep: "#64748B" }, badge.icon),
            CT.el("small", null, earned ? badge.name : "Badge: " + badge.name)])
        ])
      ]),
      CT.el("div", { class: "ct-world-grid" }, [path, CT.el("aside", { class: "ct-world-side" }, [comp.el,
        nx ? CT.el("div", { class: "ct-next-card" }, [
          CT.el("p", { class: "ct-kicker" }, "Up next · Level " + nx.n + " · " + nx.band),
          CT.el("h2", null, nx.title),
          CT.el("a", { class: "ct-btn ct-btn-big", href: "#/play/" + nx.id }, "Play level " + nx.n)
        ]) : CT.el("div", { class: "ct-next-card" }, [CT.el("p", { class: "ct-kicker" }, "World complete"),
          CT.el("h2", null, "You are a " + badge.name + "!"),
          CT.el("a", { class: "ct-btn ct-btn-big", href: "/computational-thinking/certificate/?world=" + wid }, "Your certificate")])
      ])])
    ]);
    drawPath(path, levels, w);
    var onResize = function () { drawPath(path, levels, w); };
    root.addEventListener("resize", onResize);
    heading(h1);
    return { destroy: function () { root.removeEventListener("resize", onResize); } };
  };

  function ring(done, total) {
    var r = 22, c = 2 * Math.PI * r, f = total ? done / total : 0;
    var d = CT.el("div", { class: "ct-ring", role: "img", "aria-label": done + " of " + total + " levels done" });
    d.innerHTML = '<svg viewBox="0 0 56 56"><circle cx="28" cy="28" r="' + r + '" class="bg"/><circle cx="28" cy="28" r="' + r +
      '" class="fg" stroke-dasharray="' + (c * f) + ' ' + c + '" transform="rotate(-90 28 28)"/><text x="28" y="33">' + done + '/' + total + '</text></svg>';
    return d;
  }

  // Ten stops along a winding road: two rows on a wide screen, a zig-zag on a phone.
  function drawPath(path, levels, w) {
    var wide = path.clientWidth >= 640;
    var n = levels.length, pts = [];
    var W = 1000, H = wide ? 620 : 150 * n + 40;
    for (var i = 0; i < n; i++) {
      if (wide) {
        var row = i < Math.ceil(n / 2) ? 0 : 1, k = row ? n - 1 - i : i, per = Math.ceil(n / 2);
        pts.push([90 + k * (820 / Math.max(1, per - 1)), row ? 470 : 150 + (k % 2 ? 40 : -10)]);
        if (row) pts[i][1] = 470 + (k % 2 ? -40 : 10);
      } else {
        pts.push([i % 2 ? 690 : 310, 90 + i * 150]);
      }
    }
    var d = "M" + pts[0][0] + " " + pts[0][1];
    for (var j = 1; j < n; j++) {
      var a = pts[j - 1], b = pts[j];
      if (wide && j === Math.ceil(n / 2)) d += " C" + (a[0] + 150) + " " + a[1] + " " + (b[0] + 150) + " " + b[1] + " " + b[0] + " " + b[1];
      else d += " C" + ((a[0] + b[0]) / 2) + " " + a[1] + " " + ((a[0] + b[0]) / 2) + " " + b[1] + " " + b[0] + " " + b[1];
    }
    var doneCount = 0;
    levels.forEach(function (l) { if (CT.progress.done(l.id)) doneCount++; });
    CT.clear(path);
    path.style.aspectRatio = W + " / " + H;
    var svg = '<svg class="ct-path-svg" viewBox="0 0 ' + W + ' ' + H + '" aria-hidden="true" preserveAspectRatio="none">' +
      decor(w.id, W, H) +
      '<path d="' + d + '" class="road"/><path d="' + d + '" class="road-dash"/>' +
      '<path d="' + d + '" class="road-done" pathLength="' + (n - 1) + '" stroke-dasharray="' + Math.max(0, Math.min(n - 1, doneCount)) + ' ' + n + '"/></svg>';
    path.insertAdjacentHTML("afterbegin", svg);
    var cur = CT.progress.nextIn(w.id);
    levels.forEach(function (l, i) {
      var done = CT.progress.done(l.id), open = CT.progress.unlocked(l.id), stars = CT.progress.stars(l.id);
      var isCur = cur && cur.id === l.id;
      var node = CT.el(open ? "a" : "button", {
        class: "ct-node" + (done ? " is-done" : "") + (isCur ? " is-current" : "") + (!open ? " is-locked" : ""),
        href: open ? "#/play/" + l.id : null, type: open ? null : "button",
        "aria-label": "Level " + l.n + ": " + l.title + ". " + l.band + ". " + (done ? stars + " stars." : open ? "Ready to play." : "Locked. Finish level " + (l.n - 1) + " first."),
        onclick: open ? null : function () { CT.celebrate.toast("Finish level " + (l.n - 1) + " first"); }
      }, [
        CT.el("span", { class: "ct-node-dot" }, done ? CT.ui("check") : (open ? String(l.n) : CT.ui("lock"))),
        CT.el("span", { class: "ct-node-label" }, [CT.el("b", null, l.n + ". " + l.title),
          CT.el("span", { class: "ct-node-stars", "aria-hidden": "true" }, [1, 2, 3].map(function (s) { return CT.ico(s <= stars ? "star" : "star-off"); }))])
      ]);
      // The list item is the wrapper, so the link or button inside keeps its own role.
      path.appendChild(CT.el("div", { class: "ct-node-li", role: "listitem",
        style: { left: (pts[i][0] / W * 100) + "%", top: (pts[i][1] / H * 100) + "%" } }, [node]));
      if (isCur) {
        var px = new CT.Pixel({ mood: "wave" });
        path.appendChild(CT.el("div", { class: "ct-path-pixel", "aria-hidden": "true", style: { left: (pts[i][0] / W * 100) + "%", top: (pts[i][1] / H * 100) + "%" } }, [px.svg]));
      }
    });
  }

  function decor(wid, W, H) {
    var r = CT.rng("decor:" + wid), out = [];
    var shapes = {
      decomposition: function (x, y) { return '<g transform="translate(' + x + ' ' + y + ')" class="dc"><rect x="-14" y="-14" width="28" height="28" rx="4"/><rect x="-6" y="-26" width="12" height="12" rx="2"/></g>'; },
      abstraction: function (x, y) { return '<g transform="translate(' + x + ' ' + y + ')" class="dc"><path d="M-24 10 l20 -30 l14 18 l8 -10 l16 22z"/></g>'; },
      patterns: function (x, y) { return '<g transform="translate(' + x + ' ' + y + ')" class="dc"><path d="M0 -20 l12 14 l-12 26 l-12 -26z"/></g>'; },
      algorithms: function (x, y) { return '<g transform="translate(' + x + ' ' + y + ')" class="dc"><circle r="12"/><path d="M0 -20 v8 M0 12 v8 M-20 0 h8 M12 0 h8"/></g>'; }
    };
    for (var i = 0; i < 16; i++) out.push(shapes[wid](40 + r() * (W - 80), 40 + r() * (H - 80)));
    return out.join("");
  }

  // ------------------------------------------------------------- Me page
  V.me = function (host) {
    var t = CT.progress.totals(), earned = CT.progress.badges();
    var h1 = CT.el("h1", { tabindex: "-1" }, "Your adventure");
    var wardrobe = CT.el("div", { class: "ct-wardrobe" });
    var preview = new CT.Pixel({ mood: "happy", label: "Pixel wearing your chosen accessories" });
    function drawWardrobe() {
      CT.clear(wardrobe);
      var have = CT.progress.wearables();
      wardrobe.appendChild(CT.el("div", { class: "ct-wardrobe-cat" }, [preview.svg]));
      var list = CT.el("div", { class: "ct-wardrobe-list" });
      if (!have.length) list.appendChild(CT.el("p", { class: "ctl-muted" }, "Nothing to wear yet."));
      have.forEach(function (c) {
        var on = CT.store.state.wear.indexOf(c.wear) >= 0;
        list.appendChild(CT.el("button", { type: "button", class: "ct-chipbtn" + (on ? " is-on" : ""), "aria-pressed": on ? "true" : "false", onclick: function () {
          var wr = CT.store.state.wear, k = wr.indexOf(c.wear);
          if (k >= 0) wr.splice(k, 1); else wr.push(c.wear);
          CT.store.save(); preview.wear(wr); drawWardrobe(); CT.sound.play("tap");
        } }, [on ? CT.ui("check") : null, c.wear_name]));
      });
      wardrobe.appendChild(list);
      preview.wear(CT.store.state.wear);
    }
    var chests = CT.el("div", { class: "ct-chests" });
    function drawChests() {
      CT.clear(chests);
      CT.data.chests.forEach(function (c, i) {
        var opened = CT.store.state.chests.indexOf(c.at) >= 0, ready = !opened && t.done >= c.at;
        chests.appendChild(CT.el("div", { class: "ct-chest" + (opened ? " is-open" : ready ? " is-ready" : "") }, [
          CT.el("span", { class: "ct-chest-i", "aria-hidden": "true" }, CT.ico(opened ? "box" : ready ? "gift" : "lock")),
          CT.el("b", null, "Chest " + (i + 1)),
          CT.el("small", null, opened ? c.wear_name + " + bonus puzzle" : ready ? "Ready to open!" : "Finish " + c.at + " levels"),
          ready ? CT.el("button", { type: "button", class: "ct-btn ct-btn-go", onclick: function () {
            CT.progress.openChest(c.at);
            CT.celebrate.chest(c, {
              bonus: function () { location.hash = "#/bonus/" + (i + 1); },
              wear: function () { if (CT.store.state.wear.indexOf(c.wear) < 0) CT.store.state.wear.push(c.wear); CT.store.save(); V.render(); }
            });
            drawChests(); drawWardrobe(); CT.emit("hud");
          } }, "Open") : null,
          opened ? CT.el("a", { class: "ct-btn ct-btn-soft", href: "#/bonus/" + (i + 1) }, CT.store.state.bonus["bonus-" + (i + 1)] ? "Replay bonus" : "Bonus puzzle") : null
        ]));
      });
    }
    var s = CT.store.state.settings;
    function toggle(key, label) {
      return CT.el("label", { class: "ct-switch" }, [
        CT.el("input", { type: "checkbox", checked: s[key] ? true : null, onchange: function (e) { s[key] = e.target.checked; CT.store.saveSettings(); CT.emit("hud"); } }),
        CT.el("span", null, label)]);
    }
    var motion = CT.el("select", { onchange: function (e) { s.motion = e.target.value; CT.store.saveSettings(); CT.applyMotion(); } },
      [["auto", "Follow my device"], ["full", "Full animation"], ["calm", "Calm (no animation)"]].map(function (o) {
        return CT.el("option", { value: o[0], selected: s.motion === o[0] ? true : null }, o[1]); }));
    CT.append(host, [
      CT.el("header", { class: "ct-me-head" }, [CT.el("a", { class: "ct-back", href: "#/" }, "← Adventure map"), h1]),
      CT.el("div", { class: "ct-me-stats" }, [
        stat("star", t.stars + " / " + t.maxStars, "stars"), stat("bolt", String(t.xp), "XP"),
        stat("map", t.done + " / " + t.total, "levels"), stat("chart", t.pct + "%", "complete"),
        stat("flame", String(CT.store.state.daily.streak), "day streak")
      ]),
      CT.el("section", { class: "ct-me-sec" }, [CT.el("h2", null, "Worlds"), CT.el("div", { class: "ct-me-worlds" }, CT.data.worlds.map(function (w) {
        var p = CT.progress.world(w.id);
        return CT.el("a", { class: "ct-me-world", href: "#/world/" + w.id, style: { "--w": w.colour } }, [CT.el("b", null, w.name),
          CT.el("div", { class: "ct-bar" }, CT.el("i", { style: { width: (p.total ? 100 * p.done / p.total : 0) + "%" } })),
          CT.el("small", null, p.done + "/" + p.total + " levels · " + p.stars + " stars")]);
      }))]),
      CT.el("section", { class: "ct-me-sec" }, [CT.el("h2", null, "Badges"), CT.el("div", { class: "ct-badges" }, CT.data.badges.map(function (b) {
        var on = earned.indexOf(b.id) >= 0, w = CT.byId(CT.data.worlds, (CT.data.worlds.filter(function (x) { return x.badge === b.id; })[0] || {}).id);
        return CT.el("div", { class: "ct-badge" + (on ? " is-earned" : "") }, [
          CT.celebrate.badgeArt(on ? (w || { colour: "#D97706", deep: "#92400E" }) : { colour: "#94A3B8", deep: "#64748B" }, b.icon),
          CT.el("b", null, b.name), CT.el("small", null, on ? "Earned!" : b.desc)]);
      }))]),
      CT.el("section", { class: "ct-me-sec" }, [CT.el("h2", null, "Treasure chests"), chests]),
      CT.el("section", { class: "ct-me-sec" }, [CT.el("h2", null, "Pixel's wardrobe"), wardrobe]),
      CT.el("section", { class: "ct-me-sec" }, [CT.el("h2", null, "Certificates"), CT.el("div", { class: "ct-certs" },
        CT.data.worlds.map(function (w) {
          var ok = CT.progress.world(w.id).complete;
          return CT.el("a", { class: "ct-cert-link" + (ok ? " is-ready" : ""), href: "/computational-thinking/certificate/?world=" + w.id }, [CT.ico(ok ? "medal" : "lock"), " ", w.name]);
        }).concat([CT.el("a", { class: "ct-cert-link" + (t.done === t.total ? " is-ready" : ""), href: "/computational-thinking/certificate/?world=all" }, [CT.ico(t.done === t.total ? "medal-gold" : "lock"), " Champion"])]))]),
      CT.el("section", { class: "ct-me-sec" }, [CT.el("h2", null, "Settings"), CT.el("div", { class: "ct-settings" }, [
        toggle("sound", "Sound effects"),
        CT.voice.available() ? toggle("voice", "Read instructions aloud") : null,
        CT.el("label", { class: "ct-select" }, [CT.el("span", null, "Animation"), motion]),
        CT.el("button", { type: "button", class: "ct-btn ct-btn-danger", onclick: function () {
          if (root.confirm("Delete all your adventure progress on this device? This cannot be undone.")) { CT.store.reset(); CT.emit("hud"); V.render(); }
        } }, "Reset all progress")
      ])])
    ]);
    drawChests(); drawWardrobe();
    heading(h1);
  };
  function stat(i, v, l) { return CT.el("div", { class: "ct-stat" }, [CT.ico(i), CT.el("b", null, v), CT.el("small", null, l)]); }

  // ------------------------------------------------------------ bonus
  // A chest's bonus puzzle, played in the normal level player once the chest is open.
  V.bonus = function (host, n) {
    var lv = CT.byId(CT.data.bonus || [], "bonus-" + n), chest = (CT.data.chests || [])[n - 1];
    var open = lv && chest && (CT.store.preview || CT.store.state.chests.indexOf(chest.at) >= 0);
    if (!open) {
      var h = CT.el("h1", { tabindex: "-1" }, [CT.ico("lock"), " Bonus puzzle " + n]);
      CT.append(host, [CT.el("header", { class: "ct-me-head" }, [CT.el("a", { class: "ct-back", href: "#/me" }, "← Chests and badges"), h,
        CT.el("p", { class: "ct-lead" }, chest ? "Unlocks with treasure chest " + n + ", after " + chest.at + " levels." : "There is no bonus puzzle here.")])]);
      heading(h);
      return null;
    }
    return CT.play(host, lv, { preview: CT.store.preview, onMap: function () { location.hash = "#/me"; }, onNext: function () { location.hash = "#/me"; } });
  };

  // ------------------------------------------------------------ daily
  V.daily = function (host) {
    var lv = CT.daily.pick();
    var h1 = CT.el("h1", { tabindex: "-1" }, "Daily challenge");
    var comp = CT.companion({ mood: "think", cls: "ct-daily-pal" });
    var card = CT.el("div", { class: "ct-daily-card" });
    CT.append(host, [CT.el("header", { class: "ct-me-head" }, [CT.el("a", { class: "ct-back", href: "#/" }, "← Adventure map"), h1]),
      CT.el("div", { class: "ct-daily" }, [comp.el, card])]);
    if (CT.daily.doneToday()) {
      comp.say("You've done today's challenge! Streak: " + CT.store.state.daily.streak + " days. See you tomorrow!", "proud");
      card.appendChild(CT.el("p", { class: "ct-lead" }, [CT.ico("flame"), " " + CT.store.state.daily.streak + " day streak. Best: " + CT.store.state.daily.best + "."]));
      heading(h1); return;
    }
    if (!lv) { card.textContent = "No challenge today."; return; }
    var q = lv.remember, w = CT.byId(CT.data.worlds, lv.world);
    comp.say("From " + w.name + ", level " + lv.n + ": " + lv.title + ". Have a go!", "think");
    card.appendChild(CT.el("p", { class: "ct-kicker" }, w.name + " · Level " + lv.n));
    card.appendChild(CT.el("h2", null, q.q));
    var box = CT.el("div", { class: "ct-mcq" });
    var order = CT.shuffle(q.options.map(function (x, i) { return i; }), CT.rng("daily:" + CT.daily.today()));
    order.forEach(function (i) {
      box.appendChild(CT.el("button", { type: "button", class: "ct-mcq-opt", onclick: function () {
        var right = i === q.answer, xp = CT.daily.complete(right);
        Array.prototype.forEach.call(box.children, function (b) { b.disabled = true; });
        this.classList.add(right ? "is-right" : "is-wrong");
        if (!right) box.children[order.indexOf(q.answer)].classList.add("is-right");
        card.appendChild(CT.el("p", { class: "ctl-why" }, [right ? "Correct. " : "Not this time. ", q.why]));
        card.appendChild(CT.el("p", { class: "ct-cel-xp" }, "+" + xp + " XP · " + CT.store.state.daily.streak + " day streak"));
        comp.say(right ? "Brilliant memory!" : "Now you'll remember it. Come back tomorrow!", right ? "cheer" : "wave", 3000);
        CT.sound.play(right ? "good" : "tap");
        CT.emit("hud");
      } }, q.options[i]));
    });
    card.appendChild(box);
    heading(h1);
  };
})(typeof window !== "undefined" ? window : globalThis);
