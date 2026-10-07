/* Stepped diagrams.
 *
 * Progressive enhancement: the markup ships with every stage visible, so a
 * reader without JavaScript still sees a complete static diagram. Only once
 * this runs are the stages hidden and the controls revealed.
 *
 * Autoplay is never started on load. It respects prefers-reduced-motion, and
 * any interaction stops it, so nothing moves unless the reader asked for it.
 */
(function () {
  "use strict";

  var reduced = window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)");

  function setup(fig) {
    var steps = [].slice.call(fig.querySelectorAll(".dg-step"));
    if (steps.length < 2) return;

    var controls = fig.querySelector("[data-dg-controls]");
    var countEl = fig.querySelector("[data-dg-count]");
    var textEl = fig.querySelector("[data-dg-text]");
    var prev = fig.querySelector("[data-dg-prev]");
    var next = fig.querySelector("[data-dg-next]");
    var play = fig.querySelector("[data-dg-play]");
    var at = 0, timer = null;

    function show(i) {
      at = (i + steps.length) % steps.length;
      steps.forEach(function (g, n) {
        // aria-hidden as well as the class: a hidden stage must not be read out.
        var on = n === at;
        g.classList.toggle("is-on", on);
        g.setAttribute("aria-hidden", on ? "false" : "true");
      });
      if (countEl) countEl.textContent = "Step " + (at + 1) + " of " + steps.length;
      if (textEl) textEl.textContent = steps[at].getAttribute("data-dg-label") || "";
      if (prev) prev.disabled = false;
      if (next) next.disabled = false;
    }

    function stop() {
      if (timer) { clearInterval(timer); timer = null; }
      if (play) { play.textContent = "Play"; play.setAttribute("aria-label", "Play the animation"); }
    }

    function start() {
      stop();
      // A full cycle is the point of these diagrams, so it loops, but slowly
      // enough to read the label before it changes.
      timer = setInterval(function () { show(at + 1); }, 2600);
      if (play) { play.textContent = "Pause"; play.setAttribute("aria-label", "Pause the animation"); }
    }

    if (prev) prev.addEventListener("click", function () { stop(); show(at - 1); });
    if (next) next.addEventListener("click", function () { stop(); show(at + 1); });
    if (play) play.addEventListener("click", function () { timer ? stop() : start(); });

    // Leaving the page or scrolling the figure away should not leave a timer
    // running, and a reader who has moved on should not have it jump about.
    document.addEventListener("visibilitychange", function () {
      if (document.hidden) stop();
    });
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (entries) {
        entries.forEach(function (e) { if (!e.isIntersecting) stop(); });
      }, { threshold: 0 }).observe(fig);
    }

    fig.classList.add("is-stepped");
    if (controls) controls.hidden = false;
    show(0);

    if (reduced && reduced.addEventListener) {
      reduced.addEventListener("change", function () { if (reduced.matches) stop(); });
    }
  }

  function init() {
    [].slice.call(document.querySelectorAll(".diagram-steps")).forEach(setup);
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
