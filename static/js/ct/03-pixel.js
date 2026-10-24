/* Pixel, the companion: one rigged drawing cloned wherever he appears.
 *
 * The drawing ships once in a <template>. Each copy renames its gradient ids,
 * because two cats on one page must not share them, and takes its pose from a
 * class: idle, wave, think, happy, cheer or proud.
 */
(function (root) {
  "use strict";
  var CT = root.CT = root.CT || {};
  var seq = 0;
  var MOODS = { idle: "is-idle", wave: "is-wave", think: "is-think", happy: "is-happy", cheer: "is-cheer", proud: "is-proud" };

  function cloneRig() {
    var tpl = document.getElementById("ct-pixel");
    if (!tpl) return CT.el("div", { class: "px-missing" });
    var svg = (tpl.content ? tpl.content.firstElementChild : tpl.firstElementChild).cloneNode(true);
    seq += 1;
    var map = {};
    Array.prototype.forEach.call(svg.querySelectorAll("[id]"), function (n) {
      var nid = n.id + "-p" + seq;
      map[n.id] = nid;
      n.id = nid;
    });
    Array.prototype.forEach.call(svg.querySelectorAll("[fill^='url(#'], [stroke^='url(#']"), function (n) {
      ["fill", "stroke"].forEach(function (a) {
        var v = n.getAttribute(a);
        var m = v && /^url\(#([^)]+)\)$/.exec(v);
        if (m && map[m[1]]) n.setAttribute(a, "url(#" + map[m[1]] + ")");
      });
    });
    return svg;
  }

  function Pixel(opts) {
    opts = opts || {};
    this.svg = cloneRig();
    this.svg.setAttribute("aria-hidden", opts.label ? "false" : "true");
    if (opts.label) this.svg.setAttribute("aria-label", opts.label);
    this._mood = "idle";
    this._wear = [];
    this._timer = null;
    this.mood(opts.mood || "idle");
    this.wear(opts.wear || (CT.store ? CT.store.state.wear : []));
  }
  Pixel.prototype.mood = function (m, holdMs) {
    var self = this;
    if (this._timer) { clearTimeout(this._timer); this._timer = null; }
    this._mood = MOODS[m] ? m : "idle";
    this._paint();
    if (holdMs) this._timer = setTimeout(function () { self.mood("idle"); }, holdMs);
    return this;
  };
  Pixel.prototype.wear = function (list) {
    this._wear = (list || []).slice();
    this._paint();
    return this;
  };
  Pixel.prototype._paint = function () {
    var cls = ["px", MOODS[this._mood]].concat(this._wear.map(function (w) { return "wear-" + w; }));
    this.svg.setAttribute("class", cls.join(" "));
  };

  CT.Pixel = Pixel;

  // Pixel with a speech bubble beside him, for the map, the world and the level.
  CT.companion = function (opts) {
    opts = opts || {};
    var px = new Pixel({ mood: opts.mood || "wave" });
    var text = CT.el("p", { class: "ct-say-text" });
    var bubble = CT.el("div", { class: "ct-say" }, [text]);
    var wrap = CT.el("div", { class: "ct-companion" + (opts.cls ? " " + opts.cls : "") }, [
      CT.el("div", { class: "ct-companion-cat" }, [px.svg]), bubble
    ]);
    var api = {
      el: wrap,
      pixel: px,
      say: function (msg, mood, holdMs) {
        text.textContent = msg;
        bubble.classList.remove("is-pop");
        void bubble.offsetWidth;
        bubble.classList.add("is-pop");
        if (mood) px.mood(mood, holdMs);
        return api;
      },
      mood: function (m, holdMs) { px.mood(m, holdMs); return api; }
    };
    if (opts.say) api.say(opts.say);
    return api;
  };
})(typeof window !== "undefined" ? window : globalThis);
