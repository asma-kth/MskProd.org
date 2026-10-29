// Checks every Key Stage 3 stretch task's marking without a browser.
//
// Written answers are marked in the browser by the keyword marker in
// static/js/quiz.js, and checked at build time by its Python twin in
// mskbuild/stretchcheck.py. This proves the two agree, and that the browser
// marker does what the build promised:
//   1. both markers give the same mark points for thousands of answers: every
//      model answer, every question, every accepted phrasing alone and with
//      common endings, and mixtures of phrasings from other questions;
//   2. in the browser, every model answer earns full marks, copying the
//      question earns nothing on a short answer and at most one mark on a
//      long one, and "I don't know" earns nothing;
//   3. every typed game answer is accepted as written, in capitals and with
//      stray spaces, and a wrong answer is not.
// Run from the repository root: node tools/check_stretch.mjs
import fs from "fs";
import path from "path";
import vm from "vm";
import { spawnSync } from "child_process";

const ROOT = path.resolve(path.dirname(new URL(import.meta.url).pathname), "..");

function load(file) {
  const doc = { addEventListener() {}, querySelectorAll() { return []; }, querySelector() { return null; }, getElementById() { return null; } };
  const ctx = vm.createContext({ console, setTimeout, clearTimeout, Math, JSON, Date, document: doc });
  ctx.window = ctx;
  vm.runInContext(fs.readFileSync(path.join(ROOT, file), "utf8"), ctx, { filename: file });
  return ctx;
}

function python(code, input) {
  const py = spawnSync("python3", ["-c", code], { cwd: ROOT, encoding: "utf8", input: input || "", maxBuffer: 1 << 28 });
  if (py.status !== 0) { console.error(py.stderr); process.exit(1); }
  return JSON.parse(py.stdout);
}

const LESSONS = python(`
import json, sys
sys.path.insert(0, ".")
from content import stretch_page
out = []
for r in stretch_page.records():
    st = r["stretch"]
    out.append({"key": r["key"],
                "written": [{"kind": kind, "n": i + 1, "q": w.q, "model": w.model, "marks": w.marks,
                             "points": [p.any for p in w.points]}
                            for kind, items in (("short", st.short), ("long", st.long)) for i, w in enumerate(items)],
                "typed": [{"q": b.q, "accept": b.accept} for b in st.blitz if b.kind == "type"]})
print(json.dumps(out))
`);

const marker = load("static/js/quiz.js").MskMarker;
const typedRight = load("static/js/stretch.js").MskStretch.typedRight;
if (!marker || !typedRight) { console.error("quiz.js or stretch.js did not expose its checker"); process.exit(1); }

const problems = [];
const cases = [];
const allPhrases = LESSONS.flatMap((l) => l.written.flatMap((w) => w.points.flat()));
let seed = 7;
const rand = (n) => { seed = (seed * 1103515245 + 12345) % 2147483648; return seed % n; };

for (const l of LESSONS) {
  for (const w of l.written) {
    const where = `${l.key} ${w.kind} answer ${w.n}`;
    const texts = [w.model, w.q, "I don't know", "", "yes"];
    for (const p of w.points) for (const ph of p) texts.push(ph, ph + "s", ph + "ed", ph + "ing", "It is " + ph.toUpperCase() + ".");
    for (let k = 0; k < 12; k++) {
      texts.push([0, 1, 2].map(() => allPhrases[rand(allPhrases.length)]).join(" and "));
    }
    for (const text of texts) cases.push({ where, text, points: w.points, js: marker.hits(text, w.points) });

    const score = (t) => Math.min(w.marks, marker.hits(t, w.points).filter(Boolean).length);
    if (score(w.model) < w.marks) problems.push(`${where}: in the browser the model answer earns ${score(w.model)} of ${w.marks}`);
    const echo = score(w.q);
    if (echo > (w.kind === "long" ? 1 : 0)) problems.push(`${where}: in the browser copying the question earns ${echo}`);
    if (score("I don't know")) problems.push(`${where}: in the browser "I don't know" earns a mark`);
  }
  for (const t of l.typed) {
    for (const a of t.accept) {
      for (const v of [a, a.toUpperCase(), "  " + a + " ", a + "."]) {
        if (!typedRight(v, t.accept)) problems.push(`${l.key}: typed answer ${JSON.stringify(v)} is refused for: ${t.q}`);
      }
    }
    if (typedRight("zzz", t.accept) || typedRight("", t.accept)) problems.push(`${l.key}: a wrong typed answer is accepted for: ${t.q}`);
  }
}

const py = python(`
import json, sys
sys.path.insert(0, ".")
from mskbuild.models import MP
from mskbuild.stretchcheck import hits
cases = json.load(sys.stdin)
print(json.dumps([hits(c["text"], [MP("", p) for p in c["points"]]) for c in cases]))
`, JSON.stringify(cases.map((c) => ({ text: c.text, points: c.points }))));

let disagree = 0;
cases.forEach((c, i) => {
  if (JSON.stringify(c.js) !== JSON.stringify(py[i])) {
    disagree += 1;
    if (disagree <= 20) problems.push(`${c.where}: markers disagree on ${JSON.stringify(c.text)}: browser ${JSON.stringify(c.js)}, build ${JSON.stringify(py[i])}`);
  }
});

const nWritten = LESSONS.reduce((n, l) => n + l.written.length, 0);
const nTyped = LESSONS.reduce((n, l) => n + l.typed.length, 0);
if (problems.length) {
  console.error("Stretch task marking FAILED:\n  " + problems.join("\n  ") + (disagree > 20 ? `\n  ...and ${disagree - 20} more disagreements` : ""));
  process.exit(1);
}
console.log(`Stretch tasks: ${LESSONS.length} lessons, ${nWritten} written answers and ${nTyped} typed answers checked; ` +
            `both markers agree on all ${cases.length} test answers.`);
