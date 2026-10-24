/* Celebrations: confetti, the level card, the world trophy and the finale.
 *
 * Every overlay is a real dialog: focus moves into it, Tab stays inside it and
 * Escape skips the animation. With reduced motion there is no confetti and the
 * stars and XP simply appear.
 */
(function (root) {
  "use strict";
  var CT = root.CT = root.CT || {};

  var HEADLINES = ["AMAZING WORK, COMPUTER SCIENTIST!", "BRILLIANT THINKING!", "YOU NAILED IT!",
                   "SUPERB PROBLEM SOLVING!", "PAWSOME WORK!", "OUTSTANDING!", "THAT WAS GENIUS!",
                   "TOP-CLASS THINKING!", "YOU'RE ON FIRE!", "SPECTACULAR!"];

  // ------------------------------------------------------------ confetti
  function confetti(canvas, colours, ms) {
    if (CT.calm()) return function () {};
    var ctx = canvas.getContext("2d"), W, H, parts = [], stop = false, t0 = performance.now();
    function size() {
      var dpr = Math.min(2, root.devicePixelRatio || 1);
      W = canvas.clientWidth; H = canvas.clientHeight;
      canvas.width = W * dpr; canvas.height = H * dpr;
      ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    }
    size();
    for (var i = 0; i < 170; i++) {
      parts.push({ x: W / 2 + (Math.random() - .5) * 120, y: H * .38, vx: (Math.random() - .5) * 13, vy: -Math.random() * 14 - 4,
                   r: Math.random() * 6 + 4, a: Math.random() * 6, va: (Math.random() - .5) * .3,
                   c: colours[i % colours.length], s: i % 3 });
    }
    function frame(t) {
      if (stop) { ctx.clearRect(0, 0, W, H); return; }
      var age = t - t0;
      ctx.clearRect(0, 0, W, H);
      parts.forEach(function (p) {
        p.vy += 0.32; p.vx *= 0.99; p.x += p.vx; p.y += p.vy; p.a += p.va;
        ctx.save(); ctx.translate(p.x, p.y); ctx.rotate(p.a);
        ctx.globalAlpha = Math.max(0, 1 - age / ms);
        ctx.fillStyle = p.c;
        if (p.s === 0) ctx.fillRect(-p.r / 2, -p.r / 4, p.r, p.r / 2);
        else if (p.s === 1) { ctx.beginPath(); ctx.arc(0, 0, p.r / 2.6, 0, 6.3); ctx.fill(); }
        else { ctx.beginPath(); ctx.moveTo(0, -p.r / 2); ctx.lineTo(p.r / 2, p.r / 2); ctx.lineTo(-p.r / 2, p.r / 2); ctx.fill(); }
        ctx.restore();
      });
      if (age < ms) requestAnimationFrame(frame); else ctx.clearRect(0, 0, W, H);
    }
    requestAnimationFrame(frame);
    return function () { stop = true; };
  }

  // ------------------------------------------------------- dialog shell
  function overlay(cls, colours) {
    var prev = document.activeElement;
    var canvas = CT.el("canvas", { class: "ct-confetti", "aria-hidden": "true" });
    var card = CT.el("div", { class: "ct-cel-card" });
    var box = CT.el("div", { class: "ct-cel " + (cls || ""), role: "dialog", "aria-modal": "true" }, [canvas, card]);
    document.body.appendChild(box);
    document.documentElement.classList.add("ct-locked");
    var stopConfetti = function () {};
    requestAnimationFrame(function () {
      box.classList.add("is-open");
      stopConfetti = confetti(canvas, colours || ["#F59E0B", "#10B981", "#3B82F6", "#EC4899", "#8B5CF6"], 3600);
    });
    function trap(e) {
      if (e.key === "Escape") { api.skip(); return; }
      if (e.key !== "Tab") return;
      var f = Array.prototype.filter.call(card.querySelectorAll("button, a[href]"), function (n) { return n.offsetParent !== null; });
      if (!f.length) return;
      if (e.shiftKey && document.activeElement === f[0]) { e.preventDefault(); f[f.length - 1].focus(); }
      else if (!e.shiftKey && document.activeElement === f[f.length - 1]) { e.preventDefault(); f[0].focus(); }
    }
    box.addEventListener("keydown", trap);
    var api = {
      box: box, card: card,
      skip: function () { stopConfetti(); box.classList.add("is-skipped"); },
      close: function (restore) {
        stopConfetti();
        CT.voice.stop();
        box.remove();
        if (!document.querySelector(".ct-cel")) document.documentElement.classList.remove("ct-locked");
        if (restore !== false && prev && prev.focus && document.contains(prev)) prev.focus({ preventScroll: true });
      }
    };
    return api;
  }

  function paint(box, w) {
    box.style.setProperty("--w", w.colour); box.style.setProperty("--wd", w.deep); box.style.setProperty("--wl", w.light);
  }

  function starRow(n, of) {
    var row = CT.el("div", { class: "ct-cel-stars", role: "img", "aria-label": n + " out of " + (of || 3) + " stars" });
    for (var i = 0; i < (of || 3); i++) {
      row.appendChild(CT.el("span", { class: "ct-star" + (i < n ? " is-on" : ""), style: { "--i": i }, "aria-hidden": "true" }, "★"));
    }
    return row;
  }

  function countUp(node, to, prefix) {
    if (CT.calm() || to <= 0) { node.textContent = prefix + to + " XP"; return; }
    var t0 = null;
    function f(t) {
      if (t0 === null) t0 = t;
      var p = Math.min(1, (t - t0) / 900);
      node.textContent = prefix + Math.round(to * p) + " XP";
      if (p < 1) requestAnimationFrame(f);
    }
    requestAnimationFrame(f);
  }

  function button(text, cls, fn, attrs) {
    var b = CT.el("button", Object.assign({ type: "button", class: "ct-btn " + (cls || "") }, attrs || {}), text);
    b.addEventListener("click", fn);
    return b;
  }

  function badgeArt(world, icon) {
    var w = world || { colour: "#F59E0B", deep: "#B45309" };
    var wrap = CT.el("div", { class: "ct-medal", "aria-hidden": "true" });
    wrap.innerHTML =
      '<svg viewBox="0 0 120 150"><path d="M38 84 L22 146 L44 134 L56 150 L64 92 Z" fill="' + w.deep + '"/>' +
      '<path d="M82 84 L98 146 L76 134 L64 150 L56 92 Z" fill="' + w.colour + '"/>' +
      '<circle cx="60" cy="58" r="50" fill="#F5B700" stroke="#C98A00" stroke-width="4"/>' +
      '<circle cx="60" cy="58" r="38" fill="' + w.colour + '" stroke="#FFF6C9" stroke-width="3"/>' +
      '<g transform="translate(60 58)">' + CT.icons(icon || "star", "#fff") + '</g></svg>';
    return wrap;
  }

  // Small white glyphs for medals and badges, drawn around (0, 0).
  CT.icons = function (name, c) {
    var I = {
      puzzle: '<path d="M-16 -16 h10 a6 6 0 1 1 12 0 h10 v10 a6 6 0 1 1 0 12 v10 h-32 z" fill="' + c + '"/>',
      map: '<path d="M-20 -14 l12 -5 l16 5 l12 -5 v33 l-12 5 l-16 -5 l-12 5 z" fill="none" stroke="' + c + '" stroke-width="4" stroke-linejoin="round"/><path d="M-8 -19 v33 M8 -14 v33" stroke="' + c + '" stroke-width="3"/>',
      gem: '<path d="M-18 -8 l8 -10 h20 l8 10 l-18 24 z" fill="' + c + '"/><path d="M-18 -8 h36 M-10 -18 l10 34 l10 -34" stroke="rgba(0,0,0,.25)" stroke-width="2" fill="none"/>',
      gear: '<circle r="9" fill="none" stroke="' + c + '" stroke-width="5"/><path d="M0 -21 v8 M0 13 v8 M-21 0 h8 M13 0 h8 M-15 -15 l6 6 M9 9 l6 6 M-15 15 l6 -6 M9 -9 l6 -6" stroke="' + c + '" stroke-width="6" stroke-linecap="round"/>',
      flow: '<rect x="-12" y="-22" width="24" height="10" rx="5" fill="' + c + '"/><path d="M0 -12 v6" stroke="' + c + '" stroke-width="3"/><path d="M0 -6 l12 9 l-12 9 l-12 -9 z" fill="' + c + '"/><path d="M0 12 v6" stroke="' + c + '" stroke-width="3"/><rect x="-12" y="18" width="24" height="8" fill="' + c + '"/>',
      code: '<path d="M-8 -14 l-12 14 l12 14 M8 -14 l12 14 l-12 14" fill="none" stroke="' + c + '" stroke-width="5" stroke-linecap="round" stroke-linejoin="round"/>',
      bug: '<ellipse rx="10" ry="14" fill="' + c + '"/><path d="M-10 -6 h-9 M10 -6 h9 M-10 4 h-9 M10 4 h9 M-6 -14 l-5 -6 M6 -14 l5 -6" stroke="' + c + '" stroke-width="3" stroke-linecap="round"/>',
      trophy: '<path d="M-14 -20 h28 v6 q0 18 -14 20 q-14 -2 -14 -20 z" fill="' + c + '"/><path d="M-4 6 h8 v8 h8 v6 h-24 v-6 h8 z" fill="' + c + '"/>',
      star: '<path d="M0 -22 l6.5 13 14.5 2 -10.5 10.2 2.5 14.4 -13 -6.8 -13 6.8 2.5 -14.4 -10.5 -10.2 14.5 -2 z" fill="' + c + '"/>',
      chest: '<rect x="-20" y="-6" width="40" height="22" rx="3" fill="' + c + '"/><path d="M-20 -6 q20 -20 40 0 z" fill="' + c + '"/><rect x="-4" y="-2" width="8" height="9" rx="2" fill="rgba(0,0,0,.3)"/>'
    };
    return I[name] || I.star;
  };

  CT.celebrate = {
    headline: function (level) { return HEADLINES[(CT.hash(level.id) + level.n) % HEADLINES.length]; },

    // The big one, after every level.
    level: function (level, result, on) {
      var world = CT.byId(CT.data.worlds, level.world);
      var o = overlay("is-level", [world.colour, "#F5B700", "#10B981", "#3B82F6", "#EC4899"]);
      paint(o.box, world);
      var px = new CT.Pixel({ mood: "cheer" });
      var headline = CT.celebrate.headline(level);
      var xpLine = CT.el("p", { class: "ct-cel-xp" }, "+0 XP");
      var next = result.nextLabel || "NEXT LEVEL";
      CT.append(o.card, [
        CT.el("div", { class: "ct-cel-pixel" }, [px.svg]),
        CT.el("p", { class: "ct-cel-kicker" }, ["🎉 ", level.preview ? "LEVEL COMPLETE (PREVIEW)" : "LEVEL COMPLETE!", " 🎉"]),
        CT.el("h2", { class: "ct-cel-h", id: "ct-cel-h", tabindex: "-1" }, headline),
        starRow(result.stars),
        xpLine,
        CT.el("blockquote", { class: "ct-cel-say" }, [CT.el("b", null, "Pixel says: "), "“" + level.cheer + "”"]),
        CT.el("p", { class: "ct-cel-skill" }, [CT.el("span", { class: "ct-chip" }, "Skill unlocked"), " ", level.skill]),
        result.newBadges && result.newBadges.length ? CT.el("p", { class: "ct-cel-badge" },
          ["🏅 New badge: ", result.newBadges.map(function (id) { return CT.byId(CT.data.badges, id).name; }).join(", ")]) : null,
        result.chests && result.chests.length ? CT.el("p", { class: "ct-cel-badge" }, "🎁 A mystery chest has appeared on your map!") : null,
        level.preview ? CT.el("p", { class: "ct-cel-note" }, "Teacher preview: progress is not saved.") : null,
        CT.el("div", { class: "ct-cel-btns" }, [
          on.next ? button(next + " →", "ct-btn-big", function () { o.close(false); on.next(); }) : null,
          button("↺ Try again", "ct-btn-ghost", function () { o.close(false); on.again(); }),
          button("🗺 Map", "ct-btn-ghost", function () { o.close(false); on.map(); })
        ]),
        button("Skip animation", "ct-cel-skip", function () { o.skip(); })
      ]);
      o.box.setAttribute("aria-labelledby", "ct-cel-h");
      CT.sound.play("level");
      countUp(xpLine, result.xp, "+");
      if (!CT.calm()) {
        Array.prototype.forEach.call(o.card.querySelectorAll(".ct-star.is-on"), function (s, i) {
          setTimeout(function () { CT.sound.play("star"); }, 700 + i * 260);
        });
      }
      var spoken = headline + " " + result.stars + " stars. Pixel says: " + level.cheer;
      CT.announce("Level complete. " + spoken);
      CT.voice.say(spoken);
      setTimeout(function () { var b = o.card.querySelector(".ct-btn-big") || o.card.querySelector(".ct-btn"); if (b) b.focus(); }, 60);
      return o;
    },

    // After the tenth level of a world.
    world: function (world, on) {
      var badge = CT.byId(CT.data.badges, world.badge);
      var o = overlay("is-world", [world.colour, "#F5B700", "#FFFFFF", world.deep]);
      paint(o.box, world);
      var px = new CT.Pixel({ mood: "proud" });
      var st = CT.progress.world(world.id);
      CT.append(o.card, [
        CT.el("div", { class: "ct-cel-duo" }, [CT.el("div", { class: "ct-cel-pixel" }, [px.svg]), badgeArt(world, badge.icon)]),
        CT.el("p", { class: "ct-cel-kicker" }, "🏆 WORLD COMPLETE! 🏆"),
        CT.el("h2", { class: "ct-cel-h", id: "ct-cel-h", tabindex: "-1" }, "You are a " + badge.name + "!"),
        starRow(Math.round(3 * st.stars / Math.max(1, st.maxStars))),
        CT.el("p", { class: "ct-cel-xp" }, st.stars + " of " + st.maxStars + " stars in " + world.name),
        CT.el("blockquote", { class: "ct-cel-say" }, [CT.el("b", null, "Pixel says: "),
          "“You conquered " + world.place + "! " + world.about + " You can do that now. Purr-fect!”"]),
        CT.el("div", { class: "ct-cel-btns" }, [
          CT.el("a", { class: "ct-btn ct-btn-big", href: "/computational-thinking/certificate/?world=" + world.id }, "🎓 Get your certificate"),
          button("🗺 Back to the map", "ct-btn-ghost", function () { o.close(false); on.map(); })
        ]),
        button("Skip animation", "ct-cel-skip", function () { o.skip(); })
      ]);
      o.box.setAttribute("aria-labelledby", "ct-cel-h");
      CT.sound.play("world");
      CT.announce("World complete. You are a " + badge.name + ".");
      CT.voice.say("World complete! You are a " + badge.name + "!");
      setTimeout(function () { o.card.querySelector(".ct-btn-big").focus(); }, 60);
      return o;
    },

    // All forty levels.
    champion: function (on) {
      var o = overlay("is-champion", ["#F5B700", "#EA580C", "#0284C7", "#9333EA", "#059669", "#EC4899"]);
      var px = new CT.Pixel({ mood: "cheer", wear: ["crown"] });
      var t = CT.progress.totals();
      CT.append(o.card, [
        CT.el("div", { class: "ct-cel-pixel ct-cel-pixel-xl" }, [px.svg]),
        CT.el("p", { class: "ct-cel-kicker" }, "👑 ALL 40 LEVELS 👑"),
        CT.el("h2", { class: "ct-cel-h ct-cel-h-xl", id: "ct-cel-h", tabindex: "-1" }, "YOU ARE A COMPUTATIONAL THINKING CHAMPION!"),
        starRow(3),
        CT.el("p", { class: "ct-cel-xp" }, t.stars + " stars and " + t.xp + " XP"),
        CT.el("blockquote", { class: "ct-cel-say" }, [CT.el("b", null, "Pixel says: "),
          "“Decomposition, abstraction, patterns and algorithms: you think like a computer scientist now. I am SO proud of you!”"]),
        CT.el("div", { class: "ct-cel-btns" }, [
          CT.el("a", { class: "ct-btn ct-btn-big", href: "/computational-thinking/certificate/?world=all" }, "🎓 Your champion certificate"),
          button("🗺 Back to the map", "ct-btn-ghost", function () { o.close(false); on.map(); })
        ]),
        button("Skip animation", "ct-cel-skip", function () { o.skip(); })
      ]);
      o.box.setAttribute("aria-labelledby", "ct-cel-h");
      CT.sound.play("world");
      CT.announce("You are a Computational Thinking Champion.");
      CT.voice.say("You are a Computational Thinking Champion!");
      setTimeout(function () { o.card.querySelector(".ct-btn-big").focus(); }, 60);
      return o;
    },

    // A chest opening: what was inside, and the bonus puzzle it holds.
    chest: function (chest, on) {
      var o = overlay("is-chest", ["#F5B700", "#EC4899", "#8B5CF6"]);
      var px = new CT.Pixel({ mood: "happy", wear: [chest.wear] });
      CT.append(o.card, [
        CT.el("div", { class: "ct-cel-pixel" }, [px.svg]),
        CT.el("p", { class: "ct-cel-kicker" }, "🎁 MYSTERY CHEST OPENED!"),
        CT.el("h2", { class: "ct-cel-h", id: "ct-cel-h", tabindex: "-1" }, "You found: " + chest.wear_name + "!"),
        CT.el("p", { class: "ct-cel-skill" }, "Pixel can wear it now. Choose what he wears on your Me page."),
        CT.el("div", { class: "ct-cel-btns" }, [
          button("🧩 Play the bonus puzzle", "ct-btn-big", function () { o.close(false); on.bonus(); }),
          button("👕 Put it on Pixel", "ct-btn-ghost", function () { o.close(false); on.wear(); }),
          button("Later", "ct-btn-ghost", function () { o.close(); })
        ]),
        button("Skip animation", "ct-cel-skip", function () { o.skip(); })
      ]);
      o.box.setAttribute("aria-labelledby", "ct-cel-h");
      CT.sound.play("chest");
      setTimeout(function () { o.card.querySelector(".ct-btn-big").focus(); }, 60);
      return o;
    },

    // A quick pop between the rounds of one level.
    toast: function (msg) {
      var t = CT.el("div", { class: "ct-toast", role: "status" }, msg);
      document.body.appendChild(t);
      requestAnimationFrame(function () { t.classList.add("is-on"); });
      setTimeout(function () { t.classList.remove("is-on"); setTimeout(function () { t.remove(); }, 400); }, 2200);
      CT.announce(msg);
    },
    badgeArt: badgeArt
  };
})(typeof window !== "undefined" ? window : globalThis);
