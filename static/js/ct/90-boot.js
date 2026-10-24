/* Boot and routing. The whole adventure is one page; the part after # says
 * which screen is showing, so the back button, bookmarks and a teacher's
 * shared link all work:
 *
 *   #/                      the island map
 *   #/world/<id>            a world's path of ten levels
 *   #/play/<level>          a level            (?preview: teacher, nothing saved)
 *   #/me  #/daily           the Me page and the daily challenge
 *   #/bonus/<n>             a chest's bonus puzzle
 *   #/lab/flowchart  #/lab/pseudocode
 */
(function (root) {
  "use strict";
  var CT = root.CT = root.CT || {};
  if (typeof document === "undefined") return;

  var app, view, current = null;

  CT.applyMotion = function () {
    if (!app) return;
    var m = CT.store.state.settings.motion;
    var reduce = root.matchMedia && root.matchMedia("(prefers-reduced-motion: reduce)").matches;
    app.setAttribute("data-motion", m === "full" || (m === "auto" && !reduce) ? "full" : "calm");
    document.documentElement.setAttribute("data-ct-motion", app.getAttribute("data-motion"));
  };

  function parse() {
    var h = (location.hash || "#/").replace(/^#/, "");
    var q = h.indexOf("?"), query = q >= 0 ? h.slice(q + 1) : "";
    var parts = (q >= 0 ? h.slice(0, q) : h).split("/").filter(Boolean);
    return { parts: parts, preview: /(^|&)preview\b/.test(query) };
  }

  function render() {
    if (current && current.destroy) current.destroy();
    current = null;
    CT.voice.stop();
    Array.prototype.forEach.call(document.querySelectorAll(".ct-cel"), function (n) { n.remove(); });
    document.documentElement.classList.remove("ct-locked");
    var r = parse(), p = r.parts;
    CT.store.preview = r.preview;
    app.classList.toggle("is-preview", r.preview);
    CT.clear(view);
    view.className = "ct-view";
    view.removeAttribute("style");
    var top = app.getBoundingClientRect().top + root.scrollY - 70;
    if (root.scrollY > top) root.scrollTo(0, Math.max(0, top));

    if (p[0] === "world" && p[1]) { view.classList.add("is-world"); current = CT.views.world(view, p[1]); }
    else if (p[0] === "play" && p[1]) {
      var lv = CT.byId(CT.data.levels, p[1]);
      if (!lv) { location.hash = "#/"; return; }
      if (!CT.progress.unlocked(lv.id)) {
        location.hash = "#/world/" + lv.world;
        setTimeout(function () { CT.celebrate.toast("🔒 Finish level " + (lv.n - 1) + " first"); }, 50);
        return;
      }
      view.classList.add("is-level");
      var w = CT.byId(CT.data.worlds, lv.world);
      view.style.setProperty("--w", w.colour); view.style.setProperty("--wl", w.light); view.style.setProperty("--wd", w.deep);
      current = CT.play(view, lv, {
        preview: r.preview,
        onMap: function () { location.hash = "#/world/" + lv.world + (r.preview ? "?preview" : ""); },
        onNext: function (nx) { location.hash = "#/play/" + nx.id + (r.preview ? "?preview" : ""); }
      });
    }
    else if (p[0] === "me") { view.classList.add("is-me"); current = CT.views.me(view); }
    else if (p[0] === "daily") { view.classList.add("is-daily"); current = CT.views.daily(view); }
    else if (p[0] === "bonus" && CT.views.bonus) { view.classList.add("is-level"); current = CT.views.bonus(view, Number(p[1])); }
    else if (p[0] === "lab" && CT.views.lab) { view.classList.add("is-lab"); current = CT.views.lab(view, p[1]); }
    else { view.classList.add("is-home"); current = CT.views.home(view); }
    CT.emit("hud");
  }
  CT.views = CT.views || {};
  CT.views.render = render;

  function boot() {
    app = document.getElementById("ct-app");
    var raw = document.getElementById("ct-data");
    if (!app || !raw) return;
    try { CT.data = JSON.parse(raw.textContent); } catch (e) { app.textContent = "The adventure could not load. Refresh the page to try again."; return; }
    CT.data.worlds.forEach(function (w) { w.count = CT.data.levels.filter(function (l) { return l.world === w.id; }).length; });
    CT.store.load();
    document.body.classList.add("ct-page");
    CT.clear(app);
    var hud = CT.el("div", { class: "ct-hud" });
    view = CT.el("div", { class: "ct-view" });
    CT.append(app, [hud, view, CT.el("p", { id: "ct-live", class: "sr-only", role: "status", "aria-live": "polite" })]);
    CT.applyMotion();
    if (root.matchMedia) {
      var mq = root.matchMedia("(prefers-reduced-motion: reduce)");
      if (mq.addEventListener) mq.addEventListener("change", CT.applyMotion);
    }
    CT.views.hud(hud);
    root.addEventListener("hashchange", render);
    render();
  }

  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})(typeof window !== "undefined" ? window : globalThis);
