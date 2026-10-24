/* MskProd Computing - the adventure's teacher page and certificate page.
 *
 * The teacher page can reset the adventure saved on this device. The
 * certificate page reads the levels finished on this device, unlocks a world's
 * certificate when every level in it is done, and fills in the student's name.
 * The name is kept on this device only, under mskprod:ctcert.
 */
(function () {
  "use strict";
  function get(k, f) { try { var v = localStorage.getItem("mskprod:" + k); return v === null ? f : JSON.parse(v); } catch (e) { return f; } }
  function set(k, v) { try { localStorage.setItem("mskprod:" + k, JSON.stringify(v)); } catch (e) { /* private mode */ } }
  function $(id) { return document.getElementById(id); }

  // ------------------------------------------------------------ teacher
  var reset = $("ct-reset");
  if (reset) reset.addEventListener("click", function () {
    if (!window.confirm("Reset all adventure progress, stars, badges and chests on this device? This cannot be undone.")) return;
    try { localStorage.removeItem("mskprod:ct"); localStorage.removeItem("mskprod:ctcert"); } catch (e) { /* nothing saved */ }
    $("ct-reset-msg").textContent = "Done. The adventure on this device is back to the start.";
  });

  // -------------------------------------------------------- certificate
  var dataEl = $("ctc-data");
  if (!dataEl) return;
  var data = JSON.parse(dataEl.textContent);
  var lv = (get("ct", {}) || {}).lv || {};
  var me = get("ctcert", {}) || {};

  function status(w) {
    var done = 0, stars = 0, last = 0;
    w.levels.forEach(function (id) { var r = lv[id]; if (r) { done++; stars += r.s || 0; last = Math.max(last, r.t || 0); } });
    return { done: done, total: w.levels.length, stars: stars, last: last, complete: done === w.levels.length };
  }
  var all = { id: "all", n: 0, name: "Computational Thinking Champion", tag: "All four worlds", colour: "#B45309", deep: "#78350F", light: "#FEF3C7",
    levels: data.worlds.reduce(function (a, w) { return a.concat(w.levels); }, []) };
  var choices = data.worlds.concat([all]);
  var wanted = (/[?&]world=([a-z]+)/.exec(location.search) || [])[1];
  var pick = choices.filter(function (c) { return c.id === wanted; })[0] ||
    choices.filter(function (c) { return status(c).complete; }).pop() || choices[0];

  function longDate(ts) {
    var d = ts ? new Date(ts) : new Date();
    return d.toLocaleDateString("en-GB", { day: "numeric", month: "long", year: "numeric" });
  }
  function render() {
    var tabs = $("ctc-tabs");
    tabs.textContent = "";
    choices.forEach(function (c) {
      var s = status(c), b = document.createElement("button");
      b.type = "button";
      b.className = "ctc-tab" + (c === pick ? " is-on" : "") + (s.complete ? " is-ready" : "");
      b.setAttribute("aria-pressed", c === pick ? "true" : "false");
      b.textContent = (s.complete ? "🎓 " : "🔒 ") + (c.id === "all" ? "Champion" : c.name);
      b.addEventListener("click", function () { pick = c; history.replaceState(null, "", "?world=" + c.id); render(); });
      tabs.appendChild(b);
    });
    var s = status(pick), cert = $("ctc-cert"), paper = $("ctc-paper");
    cert.style.setProperty("--c1", pick.colour);
    cert.style.setProperty("--c2", pick.deep);
    cert.style.setProperty("--c3", pick.light);
    $("ctc-name").textContent = me.name || "Your name";
    $("ctc-has").textContent = pick.id === "all" ? "has completed all forty levels and is a" : "has completed every level of";
    $("ctc-world").textContent = pick.id === "all" ? "Computational Thinking Champion" : "World " + pick.n + ": " + pick.name;
    $("ctc-tag").textContent = pick.id === "all" ? "Decomposition · Abstraction · Pattern Recognition · Algorithms" : pick.tag + " at " + pick.place;
    $("ctc-stars").textContent = "★ " + s.stars + " of " + s.total * 3 + " stars";
    $("ctc-medal-t").textContent = pick.id === "all" ? "👑" : String(pick.n);
    $("ctc-date").textContent = longDate(s.complete ? s.last : null);
    paper.classList.toggle("is-locked", !s.complete);
    $("ctc-form").hidden = !s.complete;
    $("ctc-status").textContent = s.complete
      ? "Unlocked! Add your name, then print it or save it as a PDF."
      : "Locked: " + s.done + " of " + s.total + " levels done. Finish the rest" + (pick.id === "all" ? " of the adventure" : " of " + pick.name) + " to unlock this certificate.";
  }
  var input = $("ctc-name-in");
  input.value = me.name || "";
  input.addEventListener("input", function () { me.name = input.value.slice(0, 40); set("ctcert", me); $("ctc-name").textContent = me.name || "Your name"; });
  $("ctc-print").addEventListener("click", function () { window.print(); });
  render();
})();
