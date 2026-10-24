/* Progress: stars, XP, badges, chests and the daily streak.
 *
 * Saved in this browser only, under mskprod:ct, like every other score on the
 * site. A damaged or old save is repaired field by field rather than thrown
 * away, and a teacher preview never writes at all.
 */
(function (root) {
  "use strict";
  var CT = root.CT = root.CT || {};
  var KEY = "mskprod:ct";

  function blank() {
    return { v: 1, lv: {}, xp: 0, bonus: {}, chests: [], wear: [], daily: { d: "", streak: 0, best: 0 },
             stat: { playground: 0, flowlab: 0 }, last: "", settings: { sound: false, motion: "auto", voice: false } };
  }
  function num(v, lo, hi, dflt) { v = Number(v); return isFinite(v) ? Math.max(lo, Math.min(hi, v)) : dflt; }

  // Keep what is well formed, drop what is not.
  function repair(raw) {
    var s = blank();
    if (!raw || typeof raw !== "object") return s;
    if (raw.lv && typeof raw.lv === "object") {
      Object.keys(raw.lv).forEach(function (id) {
        var r = raw.lv[id];
        if (!/^[a-z]+-\d+$/.test(id) || !r || typeof r !== "object") return;
        s.lv[id] = { s: num(r.s, 1, 3, 1), xp: num(r.xp, 0, 1000, 0), t: num(r.t, 0, 9e15, 0), n: num(r.n, 1, 1e6, 1) };
      });
    }
    s.xp = num(raw.xp, 0, 1e7, 0);
    if (raw.bonus && typeof raw.bonus === "object") Object.keys(raw.bonus).forEach(function (k) { if (raw.bonus[k]) s.bonus[k] = true; });
    if (Array.isArray(raw.chests)) s.chests = raw.chests.filter(function (x) { return typeof x === "number"; });
    if (Array.isArray(raw.wear)) s.wear = raw.wear.filter(function (x) { return typeof x === "string"; }).slice(0, 3);
    if (raw.daily && typeof raw.daily === "object") {
      s.daily = { d: typeof raw.daily.d === "string" ? raw.daily.d : "", streak: num(raw.daily.streak, 0, 9999, 0),
                  best: num(raw.daily.best, 0, 9999, 0) };
    }
    if (raw.stat && typeof raw.stat === "object") {
      s.stat.playground = num(raw.stat.playground, 0, 1e6, 0);
      s.stat.flowlab = num(raw.stat.flowlab, 0, 1e6, 0);
    }
    if (typeof raw.last === "string") s.last = raw.last;
    if (raw.settings && typeof raw.settings === "object") {
      s.settings.sound = !!raw.settings.sound;
      s.settings.voice = !!raw.settings.voice;
      s.settings.motion = ["auto", "full", "calm"].indexOf(raw.settings.motion) >= 0 ? raw.settings.motion : "auto";
    }
    return s;
  }

  var store = CT.store = {
    preview: false,
    state: blank(),
    load: function () {
      var raw = null;
      try { raw = JSON.parse(root.localStorage.getItem(KEY) || "null"); } catch (e) { raw = null; }
      store.state = repair(raw);
      return store.state;
    },
    save: function () {
      if (store.preview) return;
      try { root.localStorage.setItem(KEY, JSON.stringify(store.state)); } catch (e) { /* private mode: play on */ }
    },
    // Settings are the student's own, so they save even during a preview.
    saveSettings: function () {
      var keep = store.preview;
      store.preview = false;
      if (keep) {
        var raw = null;
        try { raw = JSON.parse(root.localStorage.getItem(KEY) || "null"); } catch (e) { raw = null; }
        var real = repair(raw);
        real.settings = store.state.settings;
        try { root.localStorage.setItem(KEY, JSON.stringify(real)); } catch (e) { /* ignore */ }
      } else store.save();
      store.preview = keep;
    },
    reset: function (levelId) {
      if (levelId) delete store.state.lv[levelId];
      else {
        var settings = store.state.settings;
        store.state = blank();
        store.state.settings = settings;
      }
      store.save();
    },
    repair: repair,
    blank: blank
  };

  // ------------------------------------------------------------ progress
  function levels() { return (CT.data && CT.data.levels) || []; }
  function level(id) { return CT.byId(levels(), id); }
  function worldLevels(w) { return levels().filter(function (l) { return l.world === w; }); }

  var P = CT.progress = {
    XP_BASE: 50, XP_STAR: 25,
    done: function (id) { return !!store.state.lv[id]; },
    stars: function (id) { return store.state.lv[id] ? store.state.lv[id].s : 0; },
    unlocked: function (id) {
      if (store.preview) return true;
      var l = level(id);
      if (!l) return false;
      if (l.n === 1) return true;
      return P.done(l.world + "-" + (l.n - 1));
    },
    // The level a student should play next in a world: the first not yet done.
    nextIn: function (w) {
      var ls = worldLevels(w);
      for (var i = 0; i < ls.length; i++) if (!P.done(ls[i].id)) return ls[i];
      return null;
    },
    world: function (w) {
      var ls = worldLevels(w), d = 0, st = 0;
      ls.forEach(function (l) { if (P.done(l.id)) d++; st += P.stars(l.id); });
      return { done: d, total: ls.length, stars: st, maxStars: ls.length * 3, complete: ls.length > 0 && d === ls.length };
    },
    totals: function () {
      var ls = levels(), d = 0, st = 0;
      ls.forEach(function (l) { if (P.done(l.id)) d++; st += P.stars(l.id); });
      return { done: d, total: ls.length, stars: st, maxStars: ls.length * 3, xp: store.state.xp,
               pct: ls.length ? Math.round(100 * d / ls.length) : 0 };
    },
    badgeEarned: function (b) {
      var r = b.rule || {};
      if (r.world) return P.world(r.world).complete;
      if (r.all) return levels().length > 0 && levels().every(function (l) { return P.done(l.id); });
      if (r.levels) {
        var ok = r.levels.every(function (id) { return P.done(id) && (!r.stars || P.stars(id) >= r.stars); });
        if (ok && r.stat) ok = (store.state.stat[r.stat] || 0) > 0;
        return ok;
      }
      return false;
    },
    badges: function () {
      return ((CT.data && CT.data.badges) || []).filter(P.badgeEarned).map(function (b) { return b.id; });
    },
    // Chests the student has earned but not yet opened.
    chestsReady: function () {
      var d = P.totals().done;
      return ((CT.data && CT.data.chests) || []).filter(function (c) {
        return d >= c.at && store.state.chests.indexOf(c.at) < 0;
      });
    },
    // Record a finished level and work out everything it changed.
    record: function (id, stars) {
      var before = P.badges(), worldBefore = level(id) ? P.world(level(id).world).complete : false;
      var allBefore = P.totals().done === levels().length;
      var prev = store.state.lv[id], xp = 0;
      if (!prev) {
        xp = P.XP_BASE + P.XP_STAR * stars;
        store.state.lv[id] = { s: stars, xp: xp, t: Date.now(), n: 1 };
      } else {
        prev.n += 1;
        if (stars > prev.s) { xp = P.XP_STAR * (stars - prev.s); prev.s = stars; prev.xp += xp; }
      }
      store.state.xp += xp;
      store.state.last = id;
      store.save();
      var after = P.badges();
      var l = level(id);
      return {
        xp: xp, stars: stars, first: !prev, improved: !!prev && xp > 0,
        newBadges: after.filter(function (b) { return before.indexOf(b) < 0; }),
        worldDone: !!l && !worldBefore && P.world(l.world).complete,
        allDone: !allBefore && P.totals().done === levels().length,
        chests: P.chestsReady()
      };
    },
    addXP: function (n) { store.state.xp += n; store.save(); },
    // A bonus puzzle: its own best score and XP, outside the worlds.
    bonusWin: function (id, stars) {
      var prev = store.state.bonus[id] || 0, xp = prev ? 0 : 50;
      store.state.bonus[id] = Math.max(prev, stars);
      store.state.xp += xp;
      store.save();
      return { xp: xp, stars: stars, first: !prev, newBadges: [], chests: [] };
    },
    openChest: function (at) {
      if (store.state.chests.indexOf(at) < 0) store.state.chests.push(at);
      store.save();
    },
    wearables: function () {
      return ((CT.data && CT.data.chests) || []).filter(function (c) { return store.state.chests.indexOf(c.at) >= 0; });
    }
  };

  // Stars from how the level went: no hints and at most one slip earns three.
  P.starsFor = function (hints, wrong, shown) {
    if (shown) return 1;
    if (hints === 0 && wrong <= 1) return 3;
    if (hints <= 1 && wrong <= 3) return 2;
    return 1;
  };

  // -------------------------------------------------------------- daily
  CT.daily = {
    today: function (d) {
      d = d || new Date();
      var m = d.getMonth() + 1, day = d.getDate();
      return d.getFullYear() + "-" + (m < 10 ? "0" : "") + m + "-" + (day < 10 ? "0" : "") + day;
    },
    doneToday: function () { return store.state.daily.d === CT.daily.today(); },
    // Today's question comes from a level already finished, so it is retrieval.
    pick: function () {
      var pool = levels().filter(function (l) { return P.done(l.id); });
      if (!pool.length) pool = levels().filter(function (l) { return l.n <= 2; });
      if (!pool.length) return null;
      var r = CT.rng("daily:" + CT.daily.today());
      return pool[Math.floor(r() * pool.length)];
    },
    complete: function (correct) {
      var s = store.state.daily, today = CT.daily.today();
      if (s.d === today) return 0;
      var y = new Date(); y.setDate(y.getDate() - 1);
      s.streak = (s.d === CT.daily.today(y)) ? s.streak + 1 : 1;
      s.best = Math.max(s.best, s.streak);
      s.d = today;
      var xp = correct ? 25 : 10;
      store.state.xp += xp;
      store.save();
      return xp;
    }
  };
})(typeof window !== "undefined" ? window : globalThis);
