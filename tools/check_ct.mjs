// Checks every level of the Computational Thinking Adventure without a browser.
//
// The game logic in static/js/ct/ touches no page while it loads, so it runs
// here in a sandbox. For every level this checks that:
//   1. the model answer passes the level's own checker;
//   2. every targeted mistake (one card moved, two steps swapped...) fails;
//   3. random boards (almost) never pass, so random clicking cannot win a level:
//      fewer than 1 in 200 random full boards may pass;
//   4. simulations (maze walks, programs, flowcharts) reach their goal.
// Run from the repository root: node tools/check_ct.mjs
import fs from "fs";
import path from "path";
import vm from "vm";
import { spawnSync } from "child_process";

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");
const JS = path.join(ROOT, "static/js/ct");

function loadCT() {
  const ctx = vm.createContext({ console, setTimeout, clearTimeout, Math, JSON, Date });
  ctx.globalThis = ctx;
  for (const f of fs.readdirSync(JS).filter((f) => f.endsWith(".js")).sort()) {
    vm.runInContext(fs.readFileSync(path.join(JS, f), "utf8"), ctx, { filename: f });
  }
  return ctx.CT;
}

function loadLevels() {
  const py = spawnSync("python3", ["-c",
    "import json, sys; sys.path.insert(0, '.'); from content.ct_adventure import payload; print(json.dumps(payload()))"],
    { cwd: ROOT, encoding: "utf8" });
  if (py.status !== 0) { console.error(py.stderr); process.exit(1); }
  return JSON.parse(py.stdout);
}

const CT = loadCT();
const DATA = loadLevels();
CT.data = DATA;
const clone = (x) => JSON.parse(JSON.stringify(x));
const ids = (list) => list.map((x) => x.id);

// ------------------------------------------------------------ mistakes
// Each returns [label, answer] pairs that must NOT pass.
function swaps(arr) {
  const out = [];
  for (let i = 0; i < arr.length; i++) for (let j = i + 1; j < arr.length; j++) {
    if (arr[i] === arr[j]) continue;
    const a = arr.slice(); [a[i], a[j]] = [a[j], a[i]]; out.push([i, j, a]);
  }
  return out;
}

const MISTAKES = {
  group(d, sol) {
    const out = [];
    for (const it of d.items) for (const z of d.zones) {
      if (z.id === it.zone) continue;
      const a = clone(sol); a[it.id] = z.id; out.push(["move " + it.id + " to " + z.id, a]);
    }
    if (d.followup) d.followup.options.forEach((_, i) => {
      if (i !== d.followup.answer) { const a = clone(sol); a.follow = i; out.push(["follow-up option " + i, a]); }
    });
    return out;
  },
  order(d, sol) {
    const out = [];
    const one = (dd, s, wrap) => {
      if (dd.rules && dd.rules.length) {
        // breaking any single rule must fail
        for (const r of dd.rules) {
          const a = s.slice(), i = a.indexOf(r[0]), j = a.indexOf(r[1]);
          [a[i], a[j]] = [a[j], a[i]];
          out.push(["break rule " + r[0] + " < " + r[1], wrap(a)]);
        }
      } else for (const [i, j, a] of swaps(s)) out.push(["swap " + i + "," + j, wrap(a)]);
    };
    if (d.rounds) d.rounds.forEach((r, k) => one(r, sol[k], (a) => { const b = clone(sol); b[k] = a; return b; }));
    else one(d, sol, (a) => a);
    return out;
  },
  tree(d, sol) {
    const out = [];
    for (const [i, j, a] of swaps(sol.slots)) if (d.ordered) out.push(["swap heads " + i + "," + j, Object.assign(clone(sol), { slots: a })]);
    const decoyHeads = d.pool.filter((p) => p.kind === "head" && !CT.byId(d.heads, p.id));
    for (const h of decoyHeads) sol.slots.forEach((s, i) => {
      if (d.heads[i].given) return;
      const a = clone(sol); a.slots[i] = h.id;
      for (const k of Object.keys(a.place)) if (a.place[k] === s) a.place[k] = h.id;
      out.push(["decoy head " + h.id + " in box " + i, a]);
    });
    for (const p of d.pool.filter((p) => p.kind === "leaf")) for (const h of d.heads) {
      if (p.parent === h.id) continue;
      const a = clone(sol); a.place[p.id] = h.id; out.push(["leaf " + p.id + " under " + h.id, a]);
    }
    if (d.roles) for (const h of d.heads) for (const r of d.roles.cards) {
      if (d.roles.answer[h.id] === r.id) continue;
      const a = clone(sol); a.roles[h.id] = r.id; out.push(["role " + r.id + " on " + h.id, a]);
    }
    return out;
  },
  assembly(d, sol) {
    const out = [];
    for (const [i, j, a] of swaps(sol.line)) out.push(["swap stations " + i + "," + j, Object.assign(clone(sol), { line: a })]);
    for (const t of d.tasks) for (const s of d.order) {
      if (t.station === s) continue;
      const a = clone(sol); a.tasks[t.id] = s; out.push(["job " + t.id + " at " + s, a]);
    }
    return out;
  },
  maze(d, sol) {
    const out = [];
    for (const [i, j, a] of swaps(sol)) out.push(["swap plan " + i + "," + j, a]);
    for (const c of d.cards.filter((c) => !c.goal)) sol.forEach((_, i) => { const a = sol.slice(); a[i] = c.id; out.push(["decoy " + c.id + " at " + i, a]); });
    return out;
  },
  select(d, sol) {
    const out = [];
    sol.rounds.forEach((r, k) => Object.keys(r).forEach((id) => {
      const a = clone(sol); a.rounds[k][id] = r[id] === "keep" ? "bin" : "keep"; out.push(["round " + k + " flip " + id, a]);
    }));
    if (d.followup) d.followup.options.forEach((_, i) => {
      if (i !== d.followup.answer) { const a = clone(sol); a.follow = i; out.push(["follow-up option " + i, a]); }
    });
    return out;
  },
  identify(d, sol) {
    const out = [];
    if (d.mode === "sensors") {
      sol.sensors.forEach((s, i) => d.sensors.forEach((x) => {
        if (sol.sensors.includes(x.id)) return;
        const a = clone(sol); a.sensors[i] = x.id; out.push(["sensor " + x.id + " for " + s, a]);
      }));
      for (const m of d.mystery) for (const c of d.classes) {
        if (c.id === m.cls) continue;
        const a = clone(sol); a.sort[m.id] = c.id; out.push(["mystery " + m.id + " as " + c.id, a]);
      }
      return out;
    }
    d.rounds.forEach((rd, k) => {
      const useless = rd.cards.filter((c) => !c.test);
      sol[k].forEach((p, i) => {
        for (const u of useless) { const a = clone(sol); a[k][i] = u.id; out.push(["round " + k + " " + u.id + " for " + p, a]); }
        const a = clone(sol); a[k].splice(i, 1); out.push(["round " + k + " without " + p, a]);
      });
    });
    return out;
  },
  graph(d, sol) {
    // every other way through the graph that is slower, plus driving through a closed road
    const out = [];
    d.rounds.forEach((rd, k) => {
      const paths = [];
      (function walk(path) {
        const here = path[path.length - 1];
        if (here === rd.end) { paths.push(path.slice()); return; }
        if (path.length > d.nodes.length) return;
        for (const e of d.edges) {
          const v = e[0] === here ? e[1] : e[1] === here ? e[0] : null;
          if (v && !path.includes(v)) { path.push(v); walk(path); path.pop(); }
        }
      })([rd.start]);
      const bestTime = (p) => p.slice(1).reduce((t, v, i) => t + CT.graphMinutes(d, p[i], v), 0);
      const want = bestTime(sol[k]);
      for (const p of paths) {
        if (JSON.stringify(p) === JSON.stringify(sol[k])) continue;
        const usesClosed = (rd.closed || []).some((c) => p.some((v, i) => i && ((p[i - 1] === c[0] && v === c[1]) || (p[i - 1] === c[1] && v === c[0]))));
        const missesVia = rd.via && !p.includes(rd.via);
        if (bestTime(p) > want || usesClosed || missesVia) { const a = clone(sol); a[k] = p; out.push(["round " + k + " route " + p.join("-"), a]); }
      }
    });
    return out;
  },
  fields(d, sol) {
    const out = [];
    d.rounds.forEach((rd, k) => {
      for (const c of d.columns) {
        if (c.id === d.key) continue;
        const a = clone(sol), cols = a[k].cols;
        if (cols.includes(c.id)) cols.splice(cols.indexOf(c.id), 1); else cols.push(c.id);
        out.push(["round " + k + " toggle " + c.id, a]);
      }
      for (const key of Object.keys(rd.answers)) rd.labels.forEach((_, li) => {
        if (li === rd.answers[key]) return;
        const a = clone(sol); a[k].labels[key] = li; out.push(["round " + k + " " + key + " as " + li, a]);
      });
    });
    return out;
  },
  model(d, sol) {
    const out = [];
    d.rounds.forEach((rd, k) => sol[k].forEach((f, i) => d.features.forEach((x) => {
      if (sol[k].includes(x.id)) return;
      const a = clone(sol); a[k][i] = x.id; out.push(["round " + k + " " + x.id + " for " + f, a]);
    })));
    return out;
  },
  datamaze(d, sol) {
    const out = [];
    d.doors.forEach((door, k) => {
      const codes = Object.keys(door.near || {}).concat(d.rows.map((r) => String(r.pages)));
      for (const c of codes) if (c !== door.code) { const a = sol.slice(); a[k] = c; out.push(["door " + k + " code " + c, a]); }
    });
    return out;
  },
  sequence(d, sol) {
    const out = [];
    const alts = (rd, v) => {
      const look = rd.look || d.look;
      if (look === "number") return [Number(v) + 1, Number(v) - 1, Number(v) * 2];
      return (rd.palette || d.palette).map((p) => (p && p.id !== undefined ? p.id : p)).filter((x) => x !== v);
    };
    d.rounds.forEach((rd, k) => {
      const put = (a) => { const b = clone(sol); b[k] = a; out.push(["round " + k + " " + JSON.stringify(a), b]); };
      if (rd.type === "fill") rd.answers.forEach((v, i) => alts(rd, v).forEach((w) => { const a = sol[k].slice(); a[i] = w; put(a); }));
      if (rd.type === "ask") {
        if (rd.input) [rd.answer + 1, rd.answer - 1, rd.answer * 2].forEach(put);
        else rd.options.forEach((_, i) => { if (i !== rd.answer) put(i); });
      }
      if (rd.type === "odd") {
        rd.seq.forEach((_, i) => { if (i !== rd.wrong) put({ pick: i, fix: rd.fix }); });
        alts(rd, rd.fix).forEach((w) => put({ pick: rd.wrong, fix: w }));
      }
      if (rd.type === "code") {
        rd.code.split("\n").forEach((_, i) => { if (i + 1 !== rd.bug) put({ line: i + 1, fix: rd.answer }); });
        rd.fixes.forEach((_, i) => { if (i !== rd.answer) put({ line: rd.bug, fix: i }); });
      }
    });
    return out;
  },
  dance(d, sol) {
    const out = [];
    const moves = ids(d.moves);
    d.rounds.forEach((rd, k) => {
      const put = (a) => { const b = clone(sol); b[k] = a; out.push(["round " + k + " " + JSON.stringify(a), b]); };
      if (rd.type === "loop") {
        [rd.answer.times - 1, rd.answer.times + 1].filter((t) => t > 0).forEach((t) => put({ times: t, unit: rd.answer.unit }));
        rd.answer.unit.forEach((m, i) => moves.forEach((x) => { if (x !== m) { const u = rd.answer.unit.slice(); u[i] = x; put({ times: rd.answer.times, unit: u }); } }));
      } else rd.answer.forEach((m, i) => moves.forEach((x) => { if (x !== m) { const a = rd.answer.slice(); a[i] = x; put(a); } }));
    });
    return out;
  },
  snakepat(d, sol) {
    const out = [];
    d.rounds.forEach((rd, k) => rd.answer.forEach((f, i) => d.fruits.forEach((x) => {
      if (x.id === f) return;
      const a = clone(sol); a[k][i] = x.id; out.push(["round " + k + " eat " + x.id + " at " + i, a]);
    })));
    return out;
  },
  codepat(d, sol) {
    const out = [];
    d.rounds.forEach((rd, k) => Object.keys(rd.blanks).forEach((b) => {
      const v = rd.blanks[b], tries = ["0", "1", "99", "i"];
      if (/^-?\d+$/.test(v)) tries.push(String(Number(v) + 1), String(Number(v) - 1));
      for (const t of tries) { if (t === v) continue; const a = clone(sol); a[k][b] = t; out.push(["round " + k + " " + b + "=" + t, a]); }
    }));
    return out;
  },
  quest(d, sol) {
    const out = [];
    d.stages.forEach((s, k) => {
      for (const [label, wrong] of MISTAKES[s.engine](s.data, sol[k])) {
        const a = clone(sol); a[k] = wrong; out.push(["stage " + k + " " + label, a]);
      }
    });
    return out;
  },
};

// --------------------------------------------------------- random boards
function pickFrom(rng, list) { return list[Math.floor(rng() * list.length)]; }
const RANDOM = {
  group(d, rng) {
    const a = {};
    for (const it of d.items) a[it.id] = pickFrom(rng, d.zones).id;
    if (d.followup) a.follow = Math.floor(rng() * d.followup.options.length);
    return a;
  },
  order(d, rng) {
    if (d.rounds) return d.rounds.map((r) => CT.shuffle(ids(r.items), rng));
    return CT.shuffle(ids(d.items), rng);
  },
  tree(d, rng) {
    const heads = CT.shuffle(ids(d.heads).filter((h) => !CT.byId(d.heads, h).given)
      .concat(d.pool.filter((p) => p.kind === "head").map((p) => p.id)), rng);
    const slots = d.heads.map((h) => (h.given ? h.id : heads.pop()));
    const place = {};
    for (const p of d.pool.filter((p) => p.kind === "leaf")) if (rng() < 0.85) place[p.id] = pickFrom(rng, slots);
    const roles = {};
    if (d.roles) { const rs = CT.shuffle(ids(d.roles.cards), rng); slots.forEach((s, i) => { roles[s] = rs[i]; }); }
    return { slots, place, roles };
  },
  assembly(d, rng) {
    const line = CT.shuffle(d.order.slice(), rng), tasks = {};
    for (const t of d.tasks) tasks[t.id] = pickFrom(rng, line);
    return { line, tasks };
  },
  maze(d, rng) { return CT.shuffle(ids(d.cards), rng).slice(0, d.plan.length); },
  select(d, rng) {
    const a = { rounds: d.rounds.map((rd) => {
      const r = {};
      for (const x of rd.layers || d.details) r[x.id] = rng() < 0.5 ? "keep" : "bin";
      return r;
    }) };
    if (d.followup) a.follow = Math.floor(rng() * d.followup.options.length);
    return a;
  },
  identify(d, rng) {
    if (d.mode === "sensors") {
      const sort = {};
      for (const m of d.mystery) sort[m.id] = pickFrom(rng, d.classes).id;
      return { sensors: CT.shuffle(ids(d.sensors), rng).slice(0, d.budget), sort };
    }
    return d.rounds.map((rd) => CT.shuffle(ids(rd.cards), rng).slice(0, rd.slots));
  },
  graph(d, rng) {
    return d.rounds.map((rd) => {
      const p = [rd.start];
      while (p[p.length - 1] !== rd.end && p.length < 12) {
        const here = p[p.length - 1];
        const next = d.edges.filter((e) => e[0] === here || e[1] === here).map((e) => (e[0] === here ? e[1] : e[0]));
        p.push(pickFrom(rng, next));
      }
      return p;
    });
  },
  fields(d, rng) {
    return d.rounds.map((rd) => {
      const cols = d.columns.filter((c) => c.id !== d.key && rng() < 0.5).map((c) => c.id), labels = {};
      for (const r of d.rows) labels[String(r[d.key])] = Math.floor(rng() * rd.labels.length);
      return { cols, labels };
    });
  },
  model(d, rng) { return d.rounds.map((rd) => CT.shuffle(ids(d.features), rng).slice(0, rd.needs.length)); },
  datamaze(d, rng) { return d.doors.map(() => String(100 + Math.floor(rng() * 900))); },
  sequence(d, rng) {
    return d.rounds.map((rd) => {
      const look = rd.look || d.look, pal = (rd.palette || d.palette || []).map((p) => (p && p.id !== undefined ? p.id : p));
      const any = () => (look === "number" ? Math.floor(rng() * 41) : pickFrom(rng, pal));
      if (rd.type === "fill") return rd.answers.map(any);
      if (rd.type === "ask") return rd.input ? Math.floor(rng() * 201) : Math.floor(rng() * rd.options.length);
      if (rd.type === "odd") return { pick: Math.floor(rng() * rd.seq.length), fix: any() };
      return { line: 1 + Math.floor(rng() * rd.code.split("\n").length), fix: Math.floor(rng() * rd.fixes.length) };
    });
  },
  dance(d, rng) {
    const moves = ids(d.moves);
    return d.rounds.map((rd) => rd.type === "loop"
      ? { times: 1 + Math.floor(rng() * 9), unit: Array.from({ length: 1 + Math.floor(rng() * rd.units) }, () => pickFrom(rng, moves)) }
      : rd.answer.map(() => pickFrom(rng, moves)));
  },
  snakepat(d, rng) { return d.rounds.map((rd) => rd.answer.map(() => pickFrom(rng, d.fruits).id)); },
  codepat(d, rng) {
    const bits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11", "12", "-1", "i", "2 * i", "3 * i", "7 * i", "i + 1"];
    return d.rounds.map((rd) => { const a = {}; Object.keys(rd.blanks).forEach((b) => { a[b] = pickFrom(rng, bits); }); return a; });
  },
  quest(d, rng) { return d.stages.map((s) => RANDOM[s.engine](s.data, rng)); },
};

// ------------------------------------------------------------ simulations
// The smallest repeating period of a list, or 0 if it never repeats twice.
function period(list) {
  for (let p = 1; p <= list.length / 2; p++) if (list.every((x, i) => i < p || x === list[i - p])) return p;
  return 0;
}
// Numbers that go up or down by a fixed step, or multiply by a fixed ratio.
function numberRule(list) {
  const n = list.map(Number), diffs = n.slice(1).map((x, i) => x - n[i]), ratios = n.slice(1).map((x, i) => x / n[i]);
  return diffs.every((x) => x === diffs[0]) || ratios.every((x) => x === ratios[0]);
}
function follows(rd, d, list) {
  return (rd.look || d.look) === "number" ? numberRule(list) : period(list) > 0;
}
const SIMULATE = {
  sequence(d) {
    for (const [k, rd] of d.rounds.entries()) {
      if (rd.type === "fill") {
        let g = 0;
        const full = rd.seq.map((v) => (v === null ? rd.answers[g++] : v));
        if (!follows(rd, d, full)) return "round " + k + ": the filled pattern does not follow a rule";
      }
      if (rd.type === "odd") {
        const fixed = rd.seq.slice(); fixed[rd.wrong] = rd.fix;
        if (!follows(rd, d, fixed)) return "round " + k + ": the fixed pattern does not follow a rule";
        if (follows(rd, d, rd.seq)) return "round " + k + ": the faulty pattern already follows a rule";
      }
      if (rd.type === "code") {
        const want = rd.expect.join("\n");
        const before = CT.pseudo.run(rd.code);
        if (before.ok && before.output.join("\n") === want) return "round " + k + ": the buggy code already prints the right output";
        for (const [i, f] of rd.fixes.entries()) {
          const r = CT.pseudo.run(CT.patchCode(rd.code, rd.bug, f));
          const good = r.ok && r.output.join("\n") === want;
          if (i === rd.answer && !good) return "round " + k + ": the right fix does not print " + rd.expect.join(", ") + " (" + (r.ok ? r.output.join(", ") : r.error.msg) + ")";
          if (i !== rd.answer && good) return "round " + k + ": fix " + i + " also prints the right output";
        }
      }
    }
    return null;
  },
  dance(d) {
    for (const [k, rd] of d.rounds.entries()) {
      if (rd.type === "next" && JSON.stringify(CT.patternNext(rd.shown, rd.answer.length)) !== JSON.stringify(rd.answer)) return "round " + k + ": the answer does not continue the pattern";
      if (rd.type === "gap") {
        let g = 0;
        const full = rd.shown.map((m) => (m === null ? rd.answer[g++] : m));
        if (!period(full)) return "round " + k + ": the filled dance does not repeat";
      }
    }
    return null;
  },
  snakepat(d) {
    for (const [k, rd] of d.rounds.entries()) {
      if (JSON.stringify(CT.patternNext(rd.eaten, rd.answer.length)) !== JSON.stringify(rd.answer)) return "round " + k + ": the answer does not continue the eaten pattern";
      if (!period(rd.eaten.concat(rd.answer))) return "round " + k + ": the fruit never repeats";
    }
    return null;
  },
  codepat(d) {
    for (const [k, rd] of d.rounds.entries()) {
      const r = CT.pseudo.run(rd.long);
      if (!r.ok) return "round " + k + ": the long program has an error: " + r.error.msg;
      if (rd.template.split("\n").length >= rd.long.split("\n").length) return "round " + k + ": the loop is not shorter than the long program";
    }
    return null;
  },
  quest(d) {
    for (const [k, s] of d.stages.entries()) {
      const f = SIMULATE[s.engine];
      const r = f ? f(s.data) : null;
      if (r) return "stage " + k + ": " + r;
    }
    return null;
  },
  maze(d) {
    const path = CT.mazeWalk(d);
    if (!path) return "the planned walk is blocked";
    const map = CT.grid.parse(d.grid), end = path[path.length - 1], exit = map.one("E");
    if (end.x !== exit.x || end.y !== exit.y) return "the walk does not finish at the exit";
    return null;
  },
};

// ------------------------------------------------------------------ run
let failures = 0, levels = 0;
const fail = (id, msg) => { failures++; console.log("  FAIL " + id + ": " + msg); };
const rng = CT.rng("check-ct");

for (const lv of DATA.levels) {
  levels++;
  const check = CT.check[lv.engine], solve = CT.solve[lv.engine];
  if (!check || !solve) { fail(lv.id, "no checker or model answer for engine " + lv.engine); continue; }
  const sol = solve(lv.data);
  const r = check(lv.data, clone(sol));
  if (!r.ok) { fail(lv.id, "the model answer fails: " + r.msg); continue; }

  const mistakes = MISTAKES[lv.engine] ? MISTAKES[lv.engine](lv.data, sol) : [];
  if (!MISTAKES[lv.engine]) fail(lv.id, "no mistake list for engine " + lv.engine);
  for (const [label, a] of mistakes) {
    const m = check(lv.data, a);
    if (m.ok) fail(lv.id, "a wrong answer passes (" + label + ")");
    else if (!m.incomplete && !m.msg) fail(lv.id, "a wrong answer gets no feedback (" + label + ")");
  }

  let wins = 0;
  const tries = 2000;
  if (RANDOM[lv.engine]) {
    for (let k = 0; k < tries; k++) if (check(lv.data, RANDOM[lv.engine](lv.data, rng)).ok) wins++;
  } else fail(lv.id, "no random-board generator for engine " + lv.engine);
  if (wins / tries > 1 / 200) fail(lv.id, wins + " of " + tries + " random boards pass");

  if (SIMULATE[lv.engine]) { const s = SIMULATE[lv.engine](lv.data); if (s) fail(lv.id, s); }
  if (lv.hints.length !== 3) fail(lv.id, "needs exactly three hints");
  console.log("ok   " + lv.id.padEnd(18) + " " + lv.engine.padEnd(10) + " " + String(mistakes.length).padStart(3) + " mistakes rejected" +
    (wins ? ", random boards pass " + (100 * wins / tries).toFixed(2) + "% of the time" : ""));
}

console.log("\n" + levels + " levels checked, " + failures + " problem" + (failures === 1 ? "" : "s") + ".");
process.exit(failures ? 1 : 0);
