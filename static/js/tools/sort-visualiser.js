/* Four sorting algorithms racing on the same list, with live counters. */
(function () {
  "use strict";

  var N = 22;

  function el(tag, cls, txt) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (txt !== undefined && txt !== null) n.textContent = txt;
    return n;
  }

  function frame(arr, a, b, comps, moves, sorted) {
    return { arr: arr.slice(), a: a, b: b, comps: comps, moves: moves,
             sorted: sorted ? sorted.slice() : [] };
  }

  /* Each algorithm returns the list of frames it passes through, so all four
     can be stepped in time with one another. */

  function bubble(src) {
    var a = src.slice(), f = [], c = 0, m = 0, n = a.length, sorted = [];
    f.push(frame(a, -1, -1, c, m, sorted));
    for (var pass = 0; pass < n - 1; pass++) {
      var swapped = false;
      for (var i = 0; i < n - 1 - pass; i++) {
        c++;
        f.push(frame(a, i, i + 1, c, m, sorted));
        if (a[i] > a[i + 1]) {
          var t = a[i]; a[i] = a[i + 1]; a[i + 1] = t;
          m++;
          f.push(frame(a, i, i + 1, c, m, sorted));
          swapped = true;
        }
      }
      sorted.push(n - 1 - pass);
      if (!swapped) break;
    }
    for (var k = 0; k < n; k++) if (sorted.indexOf(k) < 0) sorted.push(k);
    f.push(frame(a, -1, -1, c, m, sorted));
    return f;
  }

  function insertion(src) {
    var a = src.slice(), f = [], c = 0, m = 0, n = a.length, sorted = [0];
    f.push(frame(a, -1, -1, c, m, sorted));
    for (var i = 1; i < n; i++) {
      var key = a[i], j = i - 1;
      f.push(frame(a, i, j, c, m, sorted));
      while (j >= 0) {
        c++;
        if (a[j] <= key) break;
        a[j + 1] = a[j];
        m++;
        f.push(frame(a, j, j + 1, c, m, sorted));
        j--;
      }
      a[j + 1] = key;
      sorted.push(i);
      f.push(frame(a, j + 1, -1, c, m, sorted));
    }
    f.push(frame(a, -1, -1, c, m, sorted));
    return f;
  }

  function mergeSort(src) {
    var a = src.slice(), f = [], stat = { c: 0, m: 0 };
    f.push(frame(a, -1, -1, 0, 0, []));
    function run(lo, hi) {
      if (hi - lo < 2) return;
      var mid = Math.floor((lo + hi) / 2);
      run(lo, mid);
      run(mid, hi);
      var left = a.slice(lo, mid), rightArr = a.slice(mid, hi);
      var i = 0, j = 0, k = lo;
      while (i < left.length && j < rightArr.length) {
        stat.c++;
        if (left[i] <= rightArr[j]) { a[k] = left[i]; i++; }
        else { a[k] = rightArr[j]; j++; }
        stat.m++;
        f.push(frame(a, k, mid, stat.c, stat.m, []));
        k++;
      }
      while (i < left.length) {
        a[k] = left[i]; i++; stat.m++;
        f.push(frame(a, k, mid, stat.c, stat.m, []));
        k++;
      }
      while (j < rightArr.length) {
        a[k] = rightArr[j]; j++; stat.m++;
        f.push(frame(a, k, mid, stat.c, stat.m, []));
        k++;
      }
    }
    run(0, a.length);
    var all = [];
    for (var q = 0; q < a.length; q++) all.push(q);
    f.push(frame(a, -1, -1, stat.c, stat.m, all));
    return f;
  }

  function quickSort(src) {
    var a = src.slice(), f = [], stat = { c: 0, m: 0 }, fixed = [];
    f.push(frame(a, -1, -1, 0, 0, fixed));
    function part(lo, hi) {
      var pivot = a[hi], i = lo - 1;
      for (var j = lo; j < hi; j++) {
        stat.c++;
        f.push(frame(a, j, hi, stat.c, stat.m, fixed));
        if (a[j] <= pivot) {
          i++;
          var t = a[i]; a[i] = a[j]; a[j] = t;
          stat.m++;
          f.push(frame(a, i, j, stat.c, stat.m, fixed));
        }
      }
      var t2 = a[i + 1]; a[i + 1] = a[hi]; a[hi] = t2;
      stat.m++;
      fixed.push(i + 1);
      f.push(frame(a, i + 1, hi, stat.c, stat.m, fixed));
      return i + 1;
    }
    function run(lo, hi) {
      if (lo >= hi) {
        if (lo === hi && fixed.indexOf(lo) < 0) fixed.push(lo);
        return;
      }
      var p = part(lo, hi);
      run(lo, p - 1);
      run(p + 1, hi);
    }
    run(0, a.length - 1);
    var all = [];
    for (var q = 0; q < a.length; q++) all.push(q);
    f.push(frame(a, -1, -1, stat.c, stat.m, all));
    return f;
  }

  var ALGOS = [
    { key: "bubble", name: "Bubble sort", note: "compares neighbours, swaps if out of order", fn: bubble },
    { key: "insertion", name: "Insertion sort", note: "builds a sorted section on the left", fn: insertion },
    { key: "merge", name: "Merge sort", note: "splits, then merges in order", fn: mergeSort },
    { key: "quick", name: "Quick sort", note: "partitions around a pivot", fn: quickSort }
  ];

  function build(body) {
    body.textContent = "";

    var controls = el("div", "tool-btns");
    var bPlay = el("button", "tool-btn is-primary", "Play");
    var bStep = el("button", "tool-btn", "Step");
    var bReset = el("button", "tool-btn", "Restart");
    var bShuffle = el("button", "tool-btn", "New list");
    [bPlay, bStep, bReset, bShuffle].forEach(function (b) { b.type = "button"; });
    controls.appendChild(bPlay);
    controls.appendChild(bStep);
    controls.appendChild(bReset);
    controls.appendChild(bShuffle);

    var speedField = el("div", "tool-field");
    speedField.style.flex = "0 1 11rem";
    var speedLab = el("label", null, "Speed");
    var speed = document.createElement("input");
    speed.type = "range";
    speed.min = "1";
    speed.max = "60";
    speed.value = "22";
    speed.id = "sv-speed-" + Math.random().toString(36).slice(2, 7);
    speedLab.setAttribute("for", speed.id);
    speedField.appendChild(speedLab);
    speedField.appendChild(speed);

    var row = el("div", "tool-row");
    row.appendChild(controls);
    row.appendChild(speedField);
    body.appendChild(row);

    var grid = el("div", "sv-grid");
    body.appendChild(grid);

    var summary = el("p", "tool-note");
    body.appendChild(summary);

    var panels = ALGOS.map(function (algo) {
      var card = el("div", "sv-card");
      var head = el("div", "sv-head");
      head.appendChild(el("h5", null, algo.name));
      var counts = el("span", "sv-counts", "0 comparisons");
      head.appendChild(counts);
      card.appendChild(head);
      card.appendChild(el("p", "sv-note", algo.note));
      var bars = el("div", "sv-bars");
      bars.setAttribute("role", "img");
      card.appendChild(bars);
      var foot = el("p", "sv-foot", "");
      card.appendChild(foot);
      grid.appendChild(card);
      return { algo: algo, bars: bars, counts: counts, foot: foot, cells: [] };
    });

    var data = [], frames = [], pos = 0, timer = null, playing = false;

    function newList() {
      data = [];
      for (var i = 0; i < N; i++) data.push(4 + Math.floor(Math.random() * 96));
      restart();
    }

    function restart() {
      stop();
      frames = ALGOS.map(function (a) { return a.fn(data); });
      pos = 0;
      panels.forEach(function (p, i) {
        p.bars.textContent = "";
        p.cells = [];
        for (var k = 0; k < N; k++) {
          var b = el("span", "sv-bar");
          b.style.height = data[k] + "%";
          p.bars.appendChild(b);
          p.cells.push(b);
        }
        p.bars.setAttribute("aria-label", p.algo.name + " on a list of " + N + " values");
      });
      render();
    }

    function longest() {
      return frames.reduce(function (m, f) { return Math.max(m, f.length); }, 0);
    }

    function render() {
      panels.forEach(function (p, i) {
        var f = frames[i];
        var idx = Math.min(pos, f.length - 1);
        var fr = f[idx];
        for (var k = 0; k < N; k++) {
          var cell = p.cells[k];
          cell.style.height = fr.arr[k] + "%";
          var cls = "sv-bar";
          if (k === fr.a || k === fr.b) cls += " is-active";
          else if (fr.sorted.indexOf(k) >= 0) cls += " is-done";
          if (cell.className !== cls) cell.className = cls;
        }
        p.counts.textContent = fr.comps + " comparisons, " + fr.moves + " moves";
        p.foot.textContent = idx >= f.length - 1
          ? "Finished in " + (f.length - 1) + " steps"
          : "Step " + idx + " of " + (f.length - 1);
        p.foot.className = "sv-foot" + (idx >= f.length - 1 ? " is-done" : "");
      });
      var best = null;
      panels.forEach(function (p, i) {
        var last = frames[i][frames[i].length - 1];
        if (!best || last.comps < best.comps) best = { comps: last.comps, name: p.algo.name };
      });
      if (best) {
        summary.textContent = "On this list " + best.name + " needs the fewest "
          + "comparisons, " + best.comps + " of them. Shuffle the list and the winner "
          + "can change, which is exactly why exam answers talk about best case, "
          + "average case and worst case.";
      }
    }

    function step() {
      if (pos >= longest() - 1) { stop(); return; }
      pos++;
      render();
    }

    function stop() {
      playing = false;
      if (timer) { clearInterval(timer); timer = null; }
      bPlay.textContent = "Play";
      bPlay.classList.add("is-primary");
    }

    function play() {
      if (playing) { stop(); return; }
      if (pos >= longest() - 1) pos = 0;
      playing = true;
      bPlay.textContent = "Pause";
      var delay = Math.max(8, 620 / parseInt(speed.value, 10));
      timer = setInterval(step, delay);
    }

    bPlay.addEventListener("click", play);
    bStep.addEventListener("click", function () { stop(); step(); });
    bReset.addEventListener("click", function () { stop(); pos = 0; render(); });
    bShuffle.addEventListener("click", newList);
    speed.addEventListener("input", function () {
      if (playing) { stop(); play(); }
    });

    newList();
  }

  var mounts = document.querySelectorAll('.tool[data-tool="sort-visualiser"] .tool-body');
  for (var i = 0; i < mounts.length; i++) build(mounts[i]);
})();
