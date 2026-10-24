/* Engine: quest. A boss level made of stages, each played with another engine.
 *
 * data: { stages: [{title, engine, data}] }
 * Each stage mounts its own engine on the same board. When a stage is right,
 * the quest reports "stage done" and the next stage starts; the level is won
 * when the last stage is right.
 * answer: [answer for each stage's engine]
 */
(function (root) {
  "use strict";
  var CT = root.CT = root.CT || {};

  CT.check.quest = function (d, a) {
    a = a || [];
    for (var i = 0; i < d.stages.length; i++) {
      var s = d.stages[i], r = CT.check[s.engine](s.data, a[i]);
      if (!r.ok) return Object.assign({}, r, { stage: i, msg: "Stage " + (i + 1) + ": " + (r.msg || "not right yet.") });
    }
    return { ok: true };
  };
  CT.solve.quest = function (d) { return d.stages.map(function (s) { return CT.solve[s.engine](s.data); }); };

  CT.engines.quest = {
    mount: function (host, level, api) {
      var d = level.data, si = 0, sub = null;
      var strip = CT.el("ol", { class: "cq-strip", "aria-label": "Stages" }), box = CT.el("div", { class: "cq-stage" });
      host.appendChild(CT.el("div", { class: "cq" }, [strip, box]));

      function drawStrip() {
        CT.clear(strip);
        d.stages.forEach(function (s, i) {
          var mark = d.look === "vault" ? (i < si ? "🔓" : "🔒") : (i < si ? "✓" : String(i + 1));
          strip.appendChild(CT.el("li", { class: "cq-step" + (d.look === "vault" ? " is-lock" : "") + (i < si ? " is-done" : i === si ? " is-now" : ""), "aria-current": i === si ? "step" : null },
            [CT.el("b", { "aria-hidden": d.look === "vault" ? "true" : null }, mark), " ", s.title, i < si && d.look === "vault" ? CT.el("span", { class: "sr-only" }, " (open)") : null]));
        });
      }
      // A stage's final "right" becomes "stage done" until the last stage.
      function wrap(res) {
        if (res && res.ok && !res.more && si < d.stages.length - 1) {
          var from = si;
          CT.wait(1200, function () { if (api.alive() && si === from) mountStage(from + 1); });
          return { ok: true, more: true, msg: "Stage " + (from + 1) + " complete! On to stage " + (from + 2) + ".",
                   toast: "🏆 Stage " + (from + 1) + " of " + d.stages.length + " complete!" };
        }
        return res;
      }
      function mountStage(i) {
        if (sub && sub.destroy) sub.destroy();
        si = i; drawStrip(); CT.clear(box);
        var s = d.stages[i];
        var lv = Object.assign({}, level, { id: level.id + ":" + i, engine: s.engine, data: s.data, watch: null });
        var inner = CT.el("div", { class: "cq-inner ctl-board-" + s.engine });
        box.appendChild(CT.el("h2", { class: "cq-title" }, "Stage " + (i + 1) + ": " + s.title));
        box.appendChild(inner);
        sub = CT.engines[s.engine].mount(inner, lv, Object.assign({}, api, {
          level: lv, rng: CT.rng(lv.id),
          result: function (res) { api.result(wrap(res)); }
        }));
        api.label(sub.checkLabel || "✓ Check");
        if (i > 0) api.say("Stage " + (i + 1) + ": " + s.title + ".", "think", 2600);
      }
      mountStage(0);

      return {
        run: function (done) {
          if (sub.run) { sub.run(function (res) { done(wrap(res)); }); return; }
          var s = d.stages[si];
          done(wrap(sub.check ? sub.check() : CT.check[s.engine](s.data, sub.answer())));
        },
        mark: function (r) { if (sub.mark) sub.mark(r); },
        reset: function () { if (sub.reset) sub.reset(); },
        showMe: function () { if (sub.showMe) sub.showMe(); },
        scaffold: function () { if (sub.scaffold) sub.scaffold(); },
        destroy: function () { if (sub && sub.destroy) sub.destroy(); }
      };
    }
  };
})(typeof window !== "undefined" ? window : globalThis);
