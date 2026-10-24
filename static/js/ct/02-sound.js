/* Sound and voice. Both are off until the student turns them on.
 *
 * The sounds are synthesised with the Web Audio API, so there are no audio
 * files to download or license. The voice reads instructions aloud with the
 * browser's own speech engine, in a British English voice where one exists.
 */
(function (root) {
  "use strict";
  var CT = root.CT = root.CT || {};
  var ctx = null;

  function audio() {
    if (!ctx) {
      var A = root.AudioContext || root.webkitAudioContext;
      if (!A) return null;
      try { ctx = new A(); } catch (e) { return null; }
    }
    if (ctx.state === "suspended") ctx.resume();
    return ctx;
  }
  function tone(freq, start, dur, type, vol) {
    var a = audio();
    if (!a) return;
    var o = a.createOscillator(), g = a.createGain(), t = a.currentTime + start;
    o.type = type || "sine";
    o.frequency.setValueAtTime(freq, t);
    g.gain.setValueAtTime(0.0001, t);
    g.gain.exponentialRampToValueAtTime(vol || 0.12, t + 0.015);
    g.gain.exponentialRampToValueAtTime(0.0001, t + dur);
    o.connect(g); g.connect(a.destination);
    o.start(t); o.stop(t + dur + 0.05);
  }
  var SOUNDS = {
    tap: function () { tone(660, 0, 0.06, "triangle", 0.06); },
    pick: function () { tone(520, 0, 0.08, "triangle", 0.08); },
    drop: function () { tone(392, 0, 0.1, "triangle", 0.09); },
    step: function () { tone(880, 0, 0.05, "square", 0.03); },
    good: function () { tone(523, 0, 0.12, "triangle"); tone(659, 0.09, 0.12, "triangle"); tone(784, 0.18, 0.2, "triangle"); },
    bad: function () { tone(220, 0, 0.18, "sine", 0.1); tone(196, 0.12, 0.22, "sine", 0.08); },
    star: function () { tone(1046, 0, 0.18, "sine", 0.1); tone(1568, 0.06, 0.2, "sine", 0.06); },
    level: function () { [523, 659, 784, 1046, 784, 1046].forEach(function (f, i) { tone(f, i * 0.11, 0.22, "triangle", 0.11); }); },
    world: function () { [392, 523, 659, 784, 1046, 1318].forEach(function (f, i) { tone(f, i * 0.12, 0.35, "triangle", 0.11); }); },
    chest: function () { [440, 554, 659, 880].forEach(function (f, i) { tone(f, i * 0.08, 0.25, "sine", 0.1); }); }
  };

  CT.sound = {
    on: function () { return !!(CT.store && CT.store.state.settings.sound); },
    play: function (name) {
      if (!CT.sound.on() || !SOUNDS[name]) return;
      try { SOUNDS[name](); } catch (e) { /* audio is a nicety */ }
    }
  };

  CT.voice = {
    available: function () { return typeof root.speechSynthesis !== "undefined" && typeof root.SpeechSynthesisUtterance !== "undefined"; },
    on: function () { return !!(CT.store && CT.store.state.settings.voice) && CT.voice.available(); },
    say: function (text, force) {
      if (!(force || CT.voice.on()) || !CT.voice.available() || !text) return;
      try {
        root.speechSynthesis.cancel();
        var u = new root.SpeechSynthesisUtterance(String(text).replace(/[★☆]/g, ""));
        var voices = root.speechSynthesis.getVoices() || [];
        var gb = voices.filter(function (v) { return /en-GB/i.test(v.lang); })[0] || voices.filter(function (v) { return /^en/i.test(v.lang); })[0];
        if (gb) u.voice = gb;
        u.lang = gb ? gb.lang : "en-GB";
        u.rate = 0.95;
        root.speechSynthesis.speak(u);
      } catch (e) { /* speech is a nicety */ }
    },
    stop: function () { try { if (CT.voice.available()) root.speechSynthesis.cancel(); } catch (e) { /* ignore */ } }
  };
})(typeof window !== "undefined" ? window : globalThis);
