// Run each Python block in a real Pyodide, the way the site's Run button does:
// a fresh namespace per block, output captured, a 10 second guard on loops.
// usage: node pyodide_blocks.mjs <path/to/pyodide.mjs> <blocks.json>
import { readFileSync } from "node:fs";
import { pathToFileURL } from "node:url";

const [, , pyodidePath, blocksPath] = process.argv;
const { loadPyodide } = await import(pathToFileURL(pyodidePath).href);
const py = await loadPyodide();
const blocks = JSON.parse(readFileSync(blocksPath, "utf8"));

py.runPython(`
import sys, time, json
def __msk_run(src, feed):
    g = {'__name__': '__main__'}
    it = iter(json.loads(feed))
    def _input(prompt=''):
        try:
            return next(it)
        except StopIteration:
            raise EOFError('EOF when reading a line')
    g['input'] = _input
    deadline = time.time() + 10
    def guard(frame, event, arg):
        if time.time() > deadline:
            raise TimeoutError('ran for more than 10 seconds')
        return guard
    sys.settrace(guard)
    try:
        exec(compile(src, 'your program', 'exec'), g)
    finally:
        sys.settrace(None)
`);

const results = [];
for (const b of blocks) {
  let out = "";
  py.setStdout({ batched: (s) => { out += s + "\n"; } });
  py.setStderr({ batched: () => {} });
  py.globals.set("__msk_src", b.code);
  py.globals.set("__msk_feed", JSON.stringify(b.feed || []));
  let ok = true, err = "";
  const started = performance.now();
  try { py.runPython("__msk_run(__msk_src, __msk_feed)"); }
  catch (e) {
    ok = false;
    const lines = String(e.message || e).trim().split("\n").filter((l) => l.trim());
    err = lines[lines.length - 1];
  }
  results.push({ id: b.id, ok, out, err, ms: Math.round(performance.now() - started) });
}
process.stdout.write(JSON.stringify(results));
