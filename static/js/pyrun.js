/* Runnable Python. Every Python code block on the page gets a Run button, and
   Pyodide is downloaded only when somebody actually presses one. */
(function () {
  "use strict";

  /* Pyodide moved to CPython based version numbers, so try the current scheme
     first and fall back to the older one rather than failing silently. */
  var SOURCES = [
    "https://cdn.jsdelivr.net/pyodide/v314.0.6/full/pyodide.js",
    "https://cdn.jsdelivr.net/pyodide/v0.28.3/full/pyodide.js",
    "https://cdn.jsdelivr.net/npm/pyodide/pyodide.js"
  ];

  var RUNNER = [
    "import sys, time",
    "def __msk_run(src, feed):",
    "    g = {'__name__': '__main__'}",
    "    queue = list(feed)",
    "    def _input(prompt=''):",
    "        if prompt:",
    "            print(prompt, end='')",
    "        if not queue:",
    "            raise EOFError('Your program asked for input but the input box is "
      + "empty. Type one value per line in the box above and run it again.')",
    "        v = queue.pop(0)",
    "        print(v)",
    "        return v",
    "    g['input'] = _input",
    "    deadline = time.time() + 10",
    "    def guard(frame, event, arg):",
    "        frame.f_trace_opcodes = True",
    "        if time.time() > deadline:",
    "            raise TimeoutError('Stopped after 10 seconds. That almost always means "
      + "a loop with no way out: check the condition and anything that should be "
      + "changing inside it.')",
    "        return guard",
    "    sys.settrace(guard)",
    "    try:",
    "        exec(compile(src, 'your program', 'exec'), g)",
    "    finally:",
    "        sys.settrace(None)"
  ].join("\n");

  var pyodide = null, loading = null;

  /* A traceback from Pyodide includes frames from Pyodide's own code, which are
     noise to a student. Keep the frames in their program and the error itself. */
  function cleanTrace(text) {
    var out = [], keep = false;
    String(text).split("\n").forEach(function (l) {
      if (/^Traceback/.test(l)) { out.push(l); keep = false; return; }
      var file = /^\s+File "([^"]*)"/.exec(l);
      if (file) { keep = file[1] === "your program"; if (keep) out.push(l); return; }
      if (/^\s/.test(l)) { if (keep) out.push(l); return; }
      if (l.indexOf("PythonError") === 0) return;
      out.push(l);
      keep = false;
    });
    return out.join("\n").trim();
  }

  function el(tag, cls, txt) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (txt !== undefined && txt !== null) n.textContent = txt;
    return n;
  }

  function loadScript(src) {
    return new Promise(function (resolve, reject) {
      var s = document.createElement("script");
      s.src = src;
      s.onload = resolve;
      s.onerror = function () { reject(new Error("could not load " + src)); };
      document.head.appendChild(s);
    });
  }

  function boot(onProgress) {
    if (pyodide) return Promise.resolve(pyodide);
    if (loading) return loading;
    onProgress("Downloading Python. This happens once and takes a few seconds.");
    loading = SOURCES.reduce(function (chain, url) {
      return chain.catch(function () { return loadScript(url); });
    }, Promise.reject())
      .then(function () {
        onProgress("Starting Python.");
        return window.loadPyodide();
      })
      .then(function (py) {
        pyodide = py;
        py.runPython(RUNNER);
        return py;
      })
      .catch(function (err) {
        loading = null;
        throw err;
      });
    return loading;
  }

  function attach(block) {
    var pre = block.querySelector("pre");
    var codeEl = block.querySelector("code");
    if (!pre || !codeEl) return;
    var original = codeEl.textContent;

    var bar = el("div", "pyrun-bar");
    var bRun = el("button", "tool-btn is-primary", "Run");
    var bEdit = el("button", "tool-btn", "Edit");
    var bReset = el("button", "tool-btn", "Reset");
    [bRun, bEdit, bReset].forEach(function (b) { b.type = "button"; bar.appendChild(b); });
    var note = el("span", "pyrun-note", "");
    bar.appendChild(note);

    var area = document.createElement("textarea");
    area.className = "pyrun-editor";
    area.spellcheck = false;
    area.hidden = true;
    area.value = original;
    area.rows = Math.min(24, original.split("\n").length + 1);
    area.setAttribute("aria-label", "Editable Python code");

    var inputWrap = el("div", "pyrun-input");
    inputWrap.hidden = original.indexOf("input(") < 0;
    var inLab = el("label", "tool-label", "Input, one value per line");
    var inArea = document.createElement("textarea");
    inArea.rows = 2;
    inArea.spellcheck = false;
    inArea.id = "pyin-" + Math.random().toString(36).slice(2, 8);
    inLab.setAttribute("for", inArea.id);
    inputWrap.appendChild(inLab);
    inputWrap.appendChild(inArea);

    var out = el("pre", "pyrun-out");
    out.hidden = true;
    var outCode = el("code");
    out.appendChild(outCode);

    block.appendChild(area);
    block.appendChild(inputWrap);
    block.appendChild(bar);
    block.appendChild(out);

    function source() { return area.hidden ? codeEl.textContent : area.value; }

    function say(msg, kind) {
      note.textContent = msg || "";
      note.className = "pyrun-note" + (kind ? " " + kind : "");
    }

    function write(text) {
      out.hidden = false;
      outCode.textContent += text + "\n";
    }

    bEdit.addEventListener("click", function () {
      var editing = area.hidden;
      area.hidden = !editing;
      pre.hidden = editing;
      bEdit.textContent = editing ? "Done editing" : "Edit";
      if (editing) area.focus();
      inputWrap.hidden = source().indexOf("input(") < 0;
    });

    bReset.addEventListener("click", function () {
      area.value = original;
      outCode.textContent = "";
      out.hidden = true;
      say("");
    });

    bRun.addEventListener("click", function () {
      bRun.disabled = true;
      outCode.textContent = "";
      out.hidden = true;
      var src = source();
      inputWrap.hidden = src.indexOf("input(") < 0;
      boot(function (m) { say(m); }).then(function (py) {
        say("");
        var lines = [];
        py.setStdout({ batched: function (s) { lines.push(s); } });
        py.setStderr({ batched: function (s) { lines.push(s); } });
        var feed = inArea.value.split("\n").filter(function (s, i, all) {
          return !(s === "" && i === all.length - 1);
        });
        py.globals.set("__msk_src", src);
        py.globals.set("__msk_feed", feed);
        var failed = null;
        try {
          py.runPython("__msk_run(__msk_src, __msk_feed)");
        } catch (e) {
          failed = String(e.message || e);
        }
        py.setStdout({});
        py.setStderr({});
        out.hidden = false;
        outCode.textContent = lines.join("\n");
        if (failed) {
          if (outCode.textContent) outCode.textContent += "\n";
          outCode.textContent += cleanTrace(failed);
          out.classList.add("is-error");
        } else {
          out.classList.remove("is-error");
          if (!outCode.textContent) {
            outCode.textContent = "The program ran without errors and printed nothing. "
              + "Add a print() to see a value.";
          }
        }
        bRun.disabled = false;
      }).catch(function (err) {
        say("Python could not be loaded, so this block cannot run here. The code "
          + "itself is correct and will run in any Python editor.", "is-bad");
        bRun.disabled = false;
      });
    });
  }

  /* Shared with the exam marker, which runs and marks programs typed into
     programming questions. run() resolves with what the program printed. */
  var runs = 0;
  function runSource(src, feed, files) {
    return boot(function () {}).then(function (py) {
      var lines = [];
      files = files || {};
      /* Each run gets an empty folder holding only the question's data files,
         so a file written by an earlier run cannot be mistaken for this one's. */
      var dir = "/tmp/msk-run-" + (++runs);
      try {
        py.FS.mkdirTree(dir);
        py.FS.chdir(dir);
        Object.keys(files).forEach(function (n) { py.FS.writeFile(n, files[n]); });
      } catch (e) { /* run in the default folder */ }
      py.setStdout({ batched: function (s) { lines.push(s); } });
      py.setStderr({ batched: function (s) { lines.push(s); } });
      py.globals.set("__msk_src", src);
      py.globals.set("__msk_feed", feed || []);
      var failed = null;
      try {
        py.runPython("__msk_run(__msk_src, __msk_feed)");
      } catch (e) {
        failed = cleanTrace(e.message || e);
      }
      py.setStdout({});
      py.setStderr({});
      try {
        py.FS.readdir(".").forEach(function (n) {
          if (n === "." || n === ".." || files.hasOwnProperty(n)) return;
          lines.push("\n--- " + n + " (written by your program) ---\n" + py.FS.readFile(n, { encoding: "utf8" }));
        });
      } catch (e) { /* nothing to show */ }
      return { output: lines.join("\n"), error: failed };
    });
  }
  window.MskPython = { boot: boot, run: runSource };

  function isPython(block) {
    var label = block.querySelector(".code-label");
    return label && label.textContent.trim() === "Python";
  }

  document.querySelectorAll("[data-pyrun] .code-block").forEach(function (b) {
    if (isPython(b)) attach(b);
  });
})();
