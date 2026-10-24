/* The level player: Remember, Learn, Watch, Play, Check, Improve, Celebrate.
 *
 * The shell is the same for all forty levels. It shows the short explanation,
 * runs the engine's worked example, hands the board to the student, checks the
 * answer, gives graduated hints and, if they are needed, shows a full answer.
 * Stars come from how many hints and slips it took, never from speed.
 *
 * An engine is { mount(host, level, api) } returning a controller:
 *   check()     -> result, or run(done) for a simulation that animates first
 *   answer()    -> the answer, when the shell should use CT.check[engine]
 *   mark(r)     -> show which parts were wrong
 *   reset(), showMe(), scaffold(), demo(done), destroy()   (all optional but reset)
 * A result is { ok, msg, more } where more means "round done, next round".
 */
(function (root) {
  "use strict";
  var CT = root.CT = root.CT || {};

  function stepsBar(active) {
    var names = [["learn", "Learn"], ["watch", "Watch"], ["play", "Play"], ["win", "Celebrate"]];
    var ol = CT.el("ol", { class: "ctl-steps", "aria-label": "Steps in this level" });
    var hit = false;
    names.forEach(function (n) {
      var cur = n[0] === active;
      var cls = "ctl-step" + (cur ? " is-on" : (!hit ? " is-past" : ""));
      if (cur) hit = true;
      ol.appendChild(CT.el("li", { class: cls, "aria-current": cur ? "step" : null }, n[1]));
    });
    return ol;
  }

  // The world's idea, drawn once per world, shown in the Learn step.
  CT.conceptArt = function (world) {
    var d = CT.el("div", { class: "ctl-art ctl-art-" + world, "aria-hidden": "true" });
    var A = {
      decomposition: '<svg viewBox="0 0 320 130"><rect class="a1" x="110" y="8" width="100" height="34" rx="9"/><text x="160" y="30">Big problem</text>' +
        '<path class="ln" d="M160 42 V60 M60 60 H260 M60 60 V76 M160 60 V76 M260 60 V76"/>' +
        '<rect class="a2" x="18" y="76" width="84" height="30" rx="8"/><rect class="a2 d1" x="118" y="76" width="84" height="30" rx="8"/><rect class="a2 d2" x="218" y="76" width="84" height="30" rx="8"/>' +
        '<text x="60" y="96">small</text><text x="160" y="96">small</text><text x="260" y="96">small</text></svg>',
      abstraction: '<svg viewBox="0 0 320 130"><g class="busy"><rect x="14" y="14" width="120" height="100" rx="10"/><circle cx="40" cy="40" r="8"/><circle cx="96" cy="34" r="5"/><path d="M24 98 q20 -30 40 0 t40 0"/><rect x="70" y="58" width="22" height="14"/><circle cx="112" cy="84" r="9"/><path d="M30 64 l14 -8 l12 10"/></g>' +
        '<path class="ln" d="M144 64 h36 m-10 -9 l10 9 l-10 9"/><g class="simple"><rect x="190" y="14" width="120" height="100" rx="10"/><circle cx="222" cy="64" r="9"/><circle cx="280" cy="64" r="9"/><path d="M231 64 h40"/></g></svg>',
      patterns: '<svg viewBox="0 0 320 130"><g class="unit"><rect x="12" y="40" width="96" height="50" rx="10"/></g>' +
        '<circle class="s1" cx="36" cy="65" r="13"/><rect class="s2" x="70" y="52" width="26" height="26" rx="4"/><circle class="s1" cx="134" cy="65" r="13"/><rect class="s2" x="168" y="52" width="26" height="26" rx="4"/>' +
        '<circle class="s1" cx="232" cy="65" r="13"/><rect class="s2 q" x="266" y="52" width="26" height="26" rx="4"/><text x="279" y="70">?</text></svg>',
      algorithms: '<svg viewBox="0 0 320 130"><rect class="t" x="16" y="48" width="58" height="30" rx="15"/><text x="45" y="67">Start</text><path class="ln" d="M74 63 h18"/>' +
        '<rect class="p" x="92" y="48" width="58" height="30"/><text x="121" y="67">step</text><path class="ln" d="M150 63 h14"/>' +
        '<path class="d" d="M196 36 l32 27 l-32 27 l-32 -27 z"/><text x="196" y="67">?</text><path class="ln" d="M228 63 h18"/>' +
        '<rect class="t" x="246" y="48" width="58" height="30" rx="15"/><text x="275" y="67">End</text></svg>'
    };
    d.innerHTML = A[world] || "";
    return d;
  };

  CT.play = function (host, level, opts) {
    opts = opts || {};
    var world = CT.byId(CT.data.worlds, level.world);
    var eng = CT.engines[level.engine];
    var st = { hints: 0, wrong: 0, shown: false, phase: "learn", done: false, busy: false };
    var dead = false;   // set when the student leaves: late timers must not act
    var ctl = null;
    level = Object.assign({}, level, { preview: !!opts.preview });

    CT.clear(host);
    host.setAttribute("data-world", level.world);
    var comp = CT.companion({ mood: "wave", cls: "ctl-pal" });
    var stage = CT.el("div", { class: "ctl-stage" });
    var feedback = CT.el("div", { class: "ctl-feedback", role: "status", "aria-live": "polite" });
    var hintList = CT.el("ol", { class: "ctl-hints" });
    var bCheck = CT.el("button", { type: "button", class: "ct-btn ct-btn-go" }, "✓ Check");
    var bHint = CT.el("button", { type: "button", class: "ct-btn ct-btn-soft" }, "💡 Hint (3 left)");
    var bReset = CT.el("button", { type: "button", class: "ct-btn ct-btn-soft" }, "↺ Reset");
    var bShow = CT.el("button", { type: "button", class: "ct-btn ct-btn-soft", hidden: true }, "👀 Show me");
    var bRead = CT.el("button", { type: "button", class: "ct-btn ct-btn-mini", "aria-label": "Read the task aloud" }, "🔊 Read aloud");
    var controls = CT.el("div", { class: "ctl-controls" }, [bCheck, bHint, bReset, bShow]);
    var stepsWrap = CT.el("div", { class: "ctl-steps-wrap" }, stepsBar("learn"));
    var best = CT.progress.stars(level.id);

    var header = CT.el("header", { class: "ctl-top" }, [
      CT.el("a", { class: "ctl-back", href: "#/world/" + level.world }, ["← ", world.place]),
      CT.el("div", { class: "ctl-titles" }, [
        CT.el("p", { class: "ctl-kicker" }, [CT.el("span", { class: "ctl-num" }, "Level " + level.n), " · ",
          CT.el("span", { class: "ctl-band ctl-band-" + level.band.toLowerCase() }, level.band),
          level.preview ? CT.el("span", { class: "ctl-preview" }, "Teacher preview") : null]),
        CT.el("h1", { class: "ctl-h", tabindex: "-1" }, level.title)
      ]),
      CT.el("div", { class: "ctl-best", "aria-label": best ? "Best: " + best + " stars" : "Not completed yet" },
        [1, 2, 3].map(function (i) { return CT.el("span", { class: i <= best ? "is-on" : "" }, "★"); }))
    ]);
    var side = CT.el("aside", { class: "ctl-side" }, [
      comp.el,
      CT.el("div", { class: "ctl-card" }, [CT.el("h2", null, "🎯 Goal"), CT.el("p", null, level.objective)]),
      CT.el("div", { class: "ctl-card ctl-task" }, [CT.el("h2", null, "🕹 Your task"), CT.el("p", null, level.task), bRead]),
      CT.el("div", { class: "ctl-card ctl-hintbox" }, [CT.el("h2", null, "💡 Pixel's hints"), hintList,
        CT.el("p", { class: "ctl-muted" }, "Hints are free to use. Three stars needs no hints and at most one slip.")])
    ]);
    var body = CT.el("div", { class: "ctl-body" }, [side, CT.el("div", { class: "ctl-main" }, [stage, controls, feedback])]);
    CT.append(host, [header, stepsWrap, body]);

    function setPhase(p) {
      st.phase = p;
      CT.clear(stepsWrap).appendChild(stepsBar(p === "remember" ? "learn" : p));
      host.setAttribute("data-phase", p);
      controls.hidden = p !== "play";
    }
    function say(msg, mood, hold) { comp.say(msg, mood, hold); }
    function tell(msg, kind) {
      feedback.className = "ctl-feedback" + (kind ? " is-" + kind : "");
      feedback.textContent = msg;
    }

    var api = {
      level: level,
      world: world,
      rng: CT.rng(level.id),
      say: say,
      tell: tell,
      // Engines that run a simulation call this when the student starts it.
      busy: function (b) { st.busy = b; bCheck.disabled = b; bReset.disabled = b; },
      // Engines with their own Run button report the outcome through this.
      result: function (res) { handle(res); },
      // Engines with timers check this before every tick.
      alive: function () { return !dead; }
    };

    function mount(demoMode) {
      if (ctl && ctl.destroy) ctl.destroy();
      if (ctl) ctl.dead = true;
      CT.clear(stage);
      var board = CT.el("div", { class: "ctl-board ctl-board-" + level.engine });
      stage.appendChild(board);
      ctl = eng.mount(board, level, api);
      bCheck.textContent = ctl.checkLabel || "✓ Check";
      // For the automated play-through in tools/check_ct_play.py.
      CT.debug = { ctl: function () { return ctl; }, phase: function () { return st.phase; } };
      return ctl;
    }

    // ------------------------------------------------------- Remember
    function remember() {
      var past = level.n >= 3 && !level.preview ? CT.byId(CT.data.levels, level.world + "-" + (level.n - 2)) : null;
      if (!past || !CT.progress.done(past.id) || !past.remember) { learn(); return; }
      setPhase("remember");
      say("Quick memory check before we start. No pressure!", "think");
      var q = past.remember;
      var box = CT.el("div", { class: "ctl-panel ctl-remember" }, [
        CT.el("p", { class: "ctl-kicker" }, "🧠 Remember Level " + past.n + ": " + past.title),
        CT.el("h2", null, q.q)
      ]);
      var opts = CT.el("div", { class: "ct-mcq" });
      var order = CT.shuffle(q.options.map(function (t, i) { return i; }), CT.rng("rem:" + level.id));
      order.forEach(function (i) {
        opts.appendChild(CT.el("button", { type: "button", class: "ct-mcq-opt", onclick: function () {
          var right = i === q.answer;
          Array.prototype.forEach.call(opts.children, function (b) { b.disabled = true; });
          this.classList.add(right ? "is-right" : "is-wrong");
          if (!right) opts.children[order.indexOf(q.answer)].classList.add("is-right");
          box.appendChild(CT.el("p", { class: "ctl-why" }, [right ? "✓ Yes! " : "Not quite. ", q.why]));
          box.appendChild(CT.el("button", { type: "button", class: "ct-btn ct-btn-go", onclick: learn }, "Continue →"));
          if (right && !CT.progress.done(level.id)) { CT.progress.addXP(10); CT.emit("hud"); }
          say(right ? "Remembered it! +10 XP" : "Good to see it again. That is how memories get stronger.", right ? "happy" : "wave", 2400);
          CT.sound.play(right ? "good" : "tap");
        } }, q.options[i]));
      });
      box.appendChild(opts);
      box.appendChild(CT.el("button", { type: "button", class: "ctl-skip", onclick: learn }, "Skip"));
      CT.clear(stage).appendChild(box);
    }

    // ---------------------------------------------------------- Learn
    function learn() {
      setPhase("learn");
      say("Hi! I'm Pixel. Here's the idea for this level.", "wave");
      var hasDemo = !!(level.watch || (eng && eng.demo));
      var panel = CT.el("div", { class: "ctl-panel ctl-learn" }, [
        CT.conceptArt(level.world),
        CT.el("p", { class: "ctl-kicker" }, "📘 Learn"),
        CT.el("p", { class: "ctl-learn-text" }, level.learn),
        CT.el("div", { class: "ctl-learn-btns" }, [
          hasDemo ? CT.el("button", { type: "button", class: "ct-btn ct-btn-go", onclick: watch }, "▶ Watch an example") : null,
          CT.el("button", { type: "button", class: hasDemo ? "ct-btn ct-btn-soft" : "ct-btn ct-btn-go", onclick: play }, hasDemo ? "Skip to the game" : "Let's play →")
        ])
      ]);
      CT.clear(stage).appendChild(panel);
      CT.voice.say(level.learn);
      var h = host.querySelector(".ctl-h");
      if (h && opts.focus !== false) h.focus({ preventScroll: true });
    }

    // ---------------------------------------------------------- Watch
    function watch() {
      setPhase("watch");
      mount(true);
      var cap = CT.el("p", { class: "ctl-caption" }, (level.watch && level.watch.say) || "Watch Pixel do the first step.");
      stage.insertBefore(CT.el("div", { class: "ctl-watchbar" }, [CT.el("span", { class: "ctl-kicker" }, "👀 Watch"), cap]), stage.firstChild);
      say((level.watch && level.watch.say) || "Watch me do the first one.", "think");
      CT.voice.say(cap.textContent);
      var after = function () {
        say("Your turn! You've got this.", "happy", 2200);
        var go = CT.el("button", { type: "button", class: "ct-btn ct-btn-go ctl-watch-go", onclick: function () { play(); } }, "My turn →");
        var again = CT.el("button", { type: "button", class: "ct-btn ct-btn-soft", onclick: watch }, "↺ Watch again");
        stage.appendChild(CT.el("div", { class: "ctl-learn-btns" }, [go, again]));
        go.focus({ preventScroll: true });
      };
      setTimeout(function () { if (ctl && ctl.demo) ctl.demo(after); else after(); }, CT.calm() ? 50 : 650);
    }

    // ----------------------------------------------------------- Play
    function play() {
      setPhase("play");
      mount(false);
      tell("");
      say(level.task, "idle");
      var first = stage.querySelector("button, [tabindex='0'], input, select, textarea");
      if (first) first.focus({ preventScroll: true });
    }

    function handle(res) {
      if (!res || dead || st.done) return;
      if (res.ok && res.more) {
        CT.sound.play("good");
        tell(res.msg || "Round complete!", "good");
        say(res.msg || "Round complete! On to the next one.", "happy", 2200);
        CT.celebrate.toast(res.toast || "⭐ Round complete!");
        return;
      }
      if (res.ok) { win(); return; }
      if (res.incomplete) {
        // an unfinished board is not a mistake, so it costs no stars
        tell(res.msg, "info");
        say(res.msg, "think", 2200);
        return;
      }
      st.wrong += 1;
      CT.sound.play("bad");
      if (ctl.mark) ctl.mark(res);
      var nudge = st.wrong >= 2 && st.hints < 3 ? " Try a hint if you're stuck." : "";
      tell((res.msg || "Not quite yet.") + nudge, "bad");
      say(res.pixel || pick(["Nearly! Look again.", "Mistakes help us learn. Try again!", "So close! Check the highlighted part.",
                            "Good thinking. One more look?"], st.wrong), st.wrong % 2 ? "wave" : "think", 2600);
      if (st.hints >= 3 && st.wrong >= 2 && ctl.showMe) bShow.hidden = false;
    }
    function pick(list, i) { return list[i % list.length]; }

    bCheck.addEventListener("click", function () {
      if (st.busy || st.done) return;
      if (ctl.run) { ctl.run(handle); return; }
      var res = ctl.check ? ctl.check() : CT.check[level.engine](level.data, ctl.answer());
      handle(res);
    });
    bHint.addEventListener("click", function () {
      if (st.hints >= 3) return;
      var h = level.hints[st.hints];
      st.hints += 1;
      hintList.appendChild(CT.el("li", { class: "is-new" }, h));
      bHint.textContent = st.hints >= 3 ? "💡 No hints left" : "💡 Hint (" + (3 - st.hints) + " left)";
      bHint.disabled = st.hints >= 3;
      say(h, "think");
      CT.voice.say(h);
      CT.sound.play("tap");
      if (st.hints === 3 && ctl.scaffold) ctl.scaffold();
      if (st.hints >= 3 && st.wrong >= 2 && ctl.showMe) bShow.hidden = false;
      var side = host.querySelector(".ctl-hintbox");
      if (side && root.innerWidth < 900) side.scrollIntoView({ block: "nearest", behavior: CT.calm() ? "auto" : "smooth" });
    });
    bReset.addEventListener("click", function () { if (!st.busy && ctl.reset) { ctl.reset(); tell(""); CT.announce("Board reset."); } });
    bShow.addEventListener("click", function () {
      st.shown = true;
      bShow.hidden = true;
      ctl.showMe();
      tell("Here is a correct answer. Read it through, then press " + bCheck.textContent.replace(/^\W+\s*/, "") + ".", "info");
      say("Here's one way to do it. Notice why each part goes where it does.", "think");
    });
    bRead.addEventListener("click", function () { CT.voice.say(level.task + " " + (st.phase === "learn" ? level.learn : ""), true); });

    // ------------------------------------------------------- Celebrate
    function win() {
      st.done = true;
      setPhase("win");
      controls.hidden = true;
      var stars = CT.progress.starsFor(st.hints, st.wrong, st.shown);
      var res = level.preview ? { xp: P_XP(stars), stars: stars, newBadges: [], chests: [] } : CT.progress.record(level.id, stars);
      res.stars = stars;
      CT.emit("hud");
      say(level.cheer, "cheer");
      tell("Level complete! " + stars + (stars === 1 ? " star." : " stars."), "good");
      var nextLevel = CT.byId(CT.data.levels, level.world + "-" + (level.n + 1));
      var worldCount = world.count;
      var chain = function () {
        if (res.allDone) CT.celebrate.champion({ map: function () { opts.onMap(); } });
        else if (res.worldDone) CT.celebrate.world(world, { map: function () { opts.onMap(); } });
        else opts.onMap();
      };
      CT.celebrate.level(level, Object.assign({}, res, {
        nextLabel: res.worldDone || res.allDone ? "CLAIM YOUR TROPHY" : (nextLevel ? "NEXT LEVEL" : null)
      }), {
        next: (res.worldDone || res.allDone) ? chain : (nextLevel && level.n < worldCount ? function () { opts.onNext(nextLevel); } : null),
        again: function () { CT.play(host, CT.byId(CT.data.levels, level.id), opts); },
        map: function () { if (res.worldDone || res.allDone) chain(); else opts.onMap(); }
      });
    }
    function P_XP(stars) { return CT.progress.XP_BASE + CT.progress.XP_STAR * stars; }

    if (!eng) { tell("This level could not be loaded.", "bad"); return; }
    if (!level.preview) { CT.store.state.last = level.id; CT.store.save(); }
    remember();
    return { destroy: function () { dead = true; if (ctl && ctl.destroy) ctl.destroy(); CT.voice.stop(); } };
  };
})(typeof window !== "undefined" ? window : globalThis);
