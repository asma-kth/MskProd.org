/* Shared pieces for the engines: rounds, follow-up questions and readings.
 *
 * A level with rounds plays the same game several times with new data. The
 * engine checks only the round on screen; when it is right, CT.nextRound
 * reports "round done" to the shell and starts the next round shortly after.
 */
(function (root) {
  "use strict";
  var CT = root.CT = root.CT || {};

  CT.nextRound = function (api, ri, total, start, word) {
    word = word || "Round";
    CT.wait(1100, function () { if (api.alive()) start(ri + 1); });
    return { ok: true, more: true, msg: word + " " + (ri + 1) + " done! Here comes the next one.",
             toast: "⭐ " + word + " " + (ri + 1) + " of " + total + " complete!" };
  };

  CT.roundChip = function (ri, total, word) {
    return total > 1 ? CT.el("p", { class: "ct-round" }, (word || "Round") + " " + (ri + 1) + " of " + total) : null;
  };

  // The question that appears once a board is right, so the student says why.
  // onAnswer(i) records the choice; the box redraws itself.
  CT.followBox = function (f, chosen, seed, onAnswer) {
    var box = CT.el("div", { class: "cg-follow" }, [CT.el("p", { class: "ct-kicker" }, "🧠 Pixel's question"), CT.el("h3", null, f.q)]);
    var opts = CT.el("div", { class: "ct-mcq" });
    CT.shuffle(f.options.map(function (o, i) { return i; }), CT.rng(seed)).forEach(function (i) {
      opts.appendChild(CT.el("button", { type: "button", class: "ct-mcq-opt" + (chosen === i ? (i === f.answer ? " is-right" : " is-wrong") : ""),
        onclick: function () { onAnswer(i); } }, f.options[i]));
    });
    box.appendChild(opts);
    setTimeout(function () { if (box.isConnected) box.scrollIntoView({ block: "nearest", behavior: CT.calm() ? "auto" : "smooth" }); }, 50);
    return box;
  };

  // A row of reading chips, such as "Metal detector: beeps".
  CT.readings = function (pairs) {
    return CT.el("ul", { class: "ct-readings" }, pairs.map(function (p) {
      return CT.el("li", null, [CT.el("span", { "aria-hidden": "true" }, p[0] + " "), CT.el("b", null, p[1] + ": "), p[2]]);
    }));
  };
})(typeof window !== "undefined" ? window : globalThis);
