/* 3D scenes.
 *
 * Progressive enhancement, the same way the stepped diagrams work: the markup
 * ships with every stage visible, so a reader with no JavaScript still sees a
 * complete picture. Only once this runs are the stages hidden, the controls
 * revealed and the scene made draggable.
 *
 * Nothing moves unless the reader asks. Autoplay never starts on load, any
 * interaction stops it, and prefers-reduced-motion is respected throughout.
 */
(function () {
  "use strict";

  var reduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)");

  function setup(fig) {
    var stage = fig.querySelector("[data-sc-stage]");
    var world = fig.querySelector("[data-sc-world]");
    if (!stage || !world) return;

    // ------------------------------------------------------------ turning
    // Pitch is clamped: past vertical the sheets turn edge on and the labels
    // read upside down, which helps nobody.
    var rx = 62, rz = -34, dragging = false, px = 0, py = 0, moved = false;

    function apply() {
      world.style.setProperty("--rx", rx + "deg");
      world.style.setProperty("--rz", rz + "deg");
      // The counter rotation on every label has to follow the world, or the
      // text stops facing the reader as soon as the scene is turned.
      fig.style.setProperty("--sc-rx", (-rx) + "deg");
      fig.style.setProperty("--sc-rz", (-rz) + "deg");
    }

    function clamp(v, lo, hi) { return v < lo ? lo : v > hi ? hi : v; }

    function start(x, y) {
      dragging = true; moved = false; px = x; py = y;
      world.classList.add("is-dragging");
    }
    function move(x, y) {
      if (!dragging) return;
      var dx = x - px, dy = y - py;
      px = x; py = y;
      if (Math.abs(dx) + Math.abs(dy) > 2) moved = true;
      rx = clamp(rx + dy * 0.4, 12, 86);
      rz = rz - dx * 0.4;
      apply();
    }
    function end() { dragging = false; world.classList.remove("is-dragging"); }

    stage.addEventListener("pointerdown", function (e) {
      start(e.clientX, e.clientY);
      if (stage.setPointerCapture) { try { stage.setPointerCapture(e.pointerId); } catch (err) {} }
    });
    stage.addEventListener("pointermove", function (e) {
      if (dragging) { e.preventDefault(); move(e.clientX, e.clientY); }
    });
    stage.addEventListener("pointerup", end);
    stage.addEventListener("pointercancel", end);
    stage.addEventListener("lostpointercapture", end);

    // Keyboard, so turning the scene is not a mouse only feature.
    stage.tabIndex = 0;
    stage.setAttribute("role", "application");
    stage.setAttribute("aria-label",
      "Three dimensional diagram. Use the arrow keys to turn it.");
    stage.addEventListener("keydown", function (e) {
      var step = e.shiftKey ? 12 : 5, used = true;
      if (e.key === "ArrowLeft") rz -= step;
      else if (e.key === "ArrowRight") rz += step;
      else if (e.key === "ArrowUp") rx = clamp(rx - step, 12, 86);
      else if (e.key === "ArrowDown") rx = clamp(rx + step, 12, 86);
      else if (e.key === "Home") { rx = 62; rz = -34; }
      else used = false;
      if (used) { e.preventDefault(); apply(); }
    });

    apply();
    var hint = fig.querySelector("[data-sc-hint]");
    if (hint) hint.hidden = false;

    // ------------------------------------------------------------ stepping
    var steps = [].slice.call(fig.querySelectorAll(".sc-step"));
    if (steps.length < 2) return;

    var controls = fig.querySelector("[data-sc-controls]");
    var countEl = fig.querySelector("[data-sc-count]");
    var textEl = fig.querySelector("[data-sc-text]");
    var prev = fig.querySelector("[data-sc-prev]");
    var next = fig.querySelector("[data-sc-next]");
    var play = fig.querySelector("[data-sc-play]");
    var at = 0, timer = null;

    function show(i) {
      at = (i + steps.length) % steps.length;
      steps.forEach(function (g, n) {
        var on = n === at;
        g.classList.toggle("is-on", on);
        g.setAttribute("aria-hidden", on ? "false" : "true");
      });
      if (countEl) countEl.textContent = "Step " + (at + 1) + " of " + steps.length;
      if (textEl) textEl.textContent = steps[at].getAttribute("data-sc-label") || "";
    }

    function stop() {
      if (timer) { clearInterval(timer); timer = null; }
      if (play) { play.textContent = "Play"; play.setAttribute("aria-label", "Play the animation"); }
    }
    function startPlay() {
      stop();
      timer = setInterval(function () { show(at + 1); }, 2800);
      if (play) { play.textContent = "Pause"; play.setAttribute("aria-label", "Pause the animation"); }
    }

    if (prev) prev.addEventListener("click", function () { stop(); show(at - 1); });
    if (next) next.addEventListener("click", function () { stop(); show(at + 1); });
    if (play) play.addEventListener("click", function () { timer ? stop() : startPlay(); });
    stage.addEventListener("pointerdown", function () { if (moved) stop(); });

    document.addEventListener("visibilitychange", function () { if (document.hidden) stop(); });
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (entries) {
        entries.forEach(function (e) { if (!e.isIntersecting) stop(); });
      }, { threshold: 0 }).observe(fig);
    }
    if (reduced && reduced.addEventListener) {
      reduced.addEventListener("change", function () { if (reduced.matches) stop(); });
    }

    fig.classList.add("is-stepped");
    if (controls) controls.hidden = false;
    show(0);
  }

  function init() {
    [].slice.call(document.querySelectorAll(".scene")).forEach(setup);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
