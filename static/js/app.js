/* MskProd Computing - core site behaviours. No dependencies, no tracking. */
(function () {
  "use strict";

  /* ---------------------------------------------------------- storage
     Everything is stored on the student's own device only. Nothing is sent
     anywhere. If storage is unavailable the site still works, it just forgets. */
  var store = {
    get: function (k, fallback) {
      try { var v = localStorage.getItem("mskprod:" + k); return v === null ? fallback : JSON.parse(v); }
      catch (e) { return fallback; }
    },
    set: function (k, v) {
      try { localStorage.setItem("mskprod:" + k, JSON.stringify(v)); } catch (e) { /* private mode */ }
    },
    del: function (k) { try { localStorage.removeItem("mskprod:" + k); } catch (e) {} }
  };
  window.MskStore = store;

  /* ------------------------------------------------------------ theme */
  var root = document.documentElement;
  function applyTheme(t) {
    root.setAttribute("data-theme", t);
    var btn = document.getElementById("themeBtn");
    if (btn) {
      btn.setAttribute("aria-label", t === "dark" ? "Switch to light theme" : "Switch to dark theme");
      var u = btn.querySelector("use");
      if (u) u.setAttribute("href", t === "dark" ? "#i-sun" : "#i-moon");
    }
  }
  var saved = store.get("theme", null);
  applyTheme(saved || (window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches ? "dark" : "light"));
  document.addEventListener("click", function (e) {
    var b = e.target.closest && e.target.closest("#themeBtn");
    if (!b) return;
    var next = root.getAttribute("data-theme") === "dark" ? "light" : "dark";
    applyTheme(next); store.set("theme", next);
  });

  /* -------------------------------------------------------------- nav */
  var navBtn = document.getElementById("navToggle");
  var nav = document.getElementById("primaryNav");
  function closeNav() { if (nav && window.innerWidth <= 940) { nav.hidden = true; navBtn.setAttribute("aria-expanded", "false"); } }
  function syncNav() { if (!nav) return; if (window.innerWidth > 940) { nav.hidden = false; } else if (navBtn.getAttribute("aria-expanded") !== "true") { nav.hidden = true; } }
  if (navBtn && nav) {
    navBtn.addEventListener("click", function () {
      var open = navBtn.getAttribute("aria-expanded") === "true";
      navBtn.setAttribute("aria-expanded", String(!open));
      nav.hidden = open;
    });
    window.addEventListener("resize", syncNav);
    syncNav();
    nav.addEventListener("click", function (e) { if (e.target.closest("a")) closeNav(); });
  }

  /* -------------------------------------------------------- scroll bar */
  var bar = document.getElementById("readProgress");
  if (bar) {
    var tick = false;
    window.addEventListener("scroll", function () {
      if (tick) return; tick = true;
      requestAnimationFrame(function () {
        var h = document.documentElement.scrollHeight - window.innerHeight;
        bar.style.width = (h > 0 ? Math.min(100, (window.scrollY / h) * 100) : 0) + "%";
        tick = false;
      });
    }, { passive: true });
  }

  /* ------------------------------------------------------- active TOC */
  var tocLinks = Array.prototype.slice.call(document.querySelectorAll(".toc a[href^='#']"));
  if (tocLinks.length && "IntersectionObserver" in window) {
    var map = {};
    tocLinks.forEach(function (a) { var el = document.getElementById(a.getAttribute("href").slice(1)); if (el) map[el.id] = a; });
    var io = new IntersectionObserver(function (entries) {
      entries.forEach(function (en) {
        if (en.isIntersecting) {
          tocLinks.forEach(function (a) { a.classList.remove("is-current"); });
          if (map[en.target.id]) map[en.target.id].classList.add("is-current");
        }
      });
    }, { rootMargin: "-80px 0px -70% 0px", threshold: 0 });
    Object.keys(map).forEach(function (id) { io.observe(document.getElementById(id)); });
  }

  /* --------------------------------------------------------- copy code */
  document.addEventListener("click", function (e) {
    var b = e.target.closest && e.target.closest(".code-copy");
    if (!b) return;
    var pre = b.parentElement.querySelector("pre");
    if (!pre) return;
    var txt = pre.innerText;
    var done = function () { var o = b.textContent; b.textContent = "Copied"; setTimeout(function () { b.textContent = o; }, 1400); };
    if (navigator.clipboard) { navigator.clipboard.writeText(txt).then(done, function(){}); }
    else {
      var ta = document.createElement("textarea"); ta.value = txt; document.body.appendChild(ta);
      ta.select(); try { document.execCommand("copy"); done(); } catch (err) {} document.body.removeChild(ta);
    }
  });

  /* --------------------------------------------------------------- tabs */
  document.querySelectorAll("[data-tabs]").forEach(function (group) {
    var btns = group.querySelectorAll(".tabs button");
    btns.forEach(function (b) {
      b.addEventListener("click", function () {
        btns.forEach(function (o) { o.setAttribute("aria-selected", "false"); });
        b.setAttribute("aria-selected", "true");
        group.querySelectorAll(".tabpanel").forEach(function (p) { p.hidden = p.id !== b.getAttribute("aria-controls"); });
      });
    });
  });

  /* --------------------------------------------------------- flashcards */
  document.addEventListener("click", function (e) {
    var c = e.target.closest && e.target.closest(".flashcard");
    if (c) c.classList.toggle("flipped");
  });
  document.addEventListener("keydown", function (e) {
    if (e.key !== "Enter" && e.key !== " ") return;
    var c = document.activeElement && document.activeElement.closest && document.activeElement.closest(".flashcard");
    if (c) { e.preventDefault(); c.classList.toggle("flipped"); }
  });

  /* ------------------------------------------------------------ search */
  var shell = document.getElementById("searchShell");
  var input = document.getElementById("searchInput");
  var out = document.getElementById("searchResults");
  var index = null, loading = false, sel = 0, rows = [];

  function loadIndex() {
    if (index || loading) return;
    loading = true;
    fetch(window.MSK_BASE + "search-index.json")
      .then(function (r) { return r.json(); })
      .then(function (d) { index = d; loading = false; if (input && input.value) render(input.value); })
      .catch(function () { loading = false; });
  }
  function openSearch() {
    if (!shell) return;
    shell.hidden = false; loadIndex();
    setTimeout(function () { input.focus(); input.select(); }, 20);
    document.body.style.overflow = "hidden";
  }
  function closeSearch() { if (!shell) return; shell.hidden = true; document.body.style.overflow = ""; }
  function score(item, terms) {
    var t = (item.t || "").toLowerCase(), k = (item.k || "").toLowerCase(), s = 0;
    for (var i = 0; i < terms.length; i++) {
      var q = terms[i];
      if (!q) continue;
      if (t === q) s += 60;
      else if (t.indexOf(q) === 0) s += 30;
      else if (t.indexOf(q) > -1) s += 18;
      if (k.indexOf(q) > -1) s += 6;
      else if (t.indexOf(q) === -1) return -1;
    }
    return s;
  }
  function render(q) {
    if (!out) return;
    q = q.trim().toLowerCase();
    if (!q) { out.innerHTML = '<p class="search-empty">Start typing to find any topic, quiz or paper.</p>'; rows = []; return; }
    if (!index) { out.innerHTML = '<p class="search-empty">Loading the index...</p>'; return; }
    var terms = q.split(/\s+/);
    var hits = [];
    for (var i = 0; i < index.length; i++) {
      var sc = score(index[i], terms);
      if (sc > 0) hits.push([sc, index[i]]);
    }
    hits.sort(function (a, b) { return b[0] - a[0]; });
    hits = hits.slice(0, 12);
    if (!hits.length) { out.innerHTML = '<p class="search-empty">Nothing matched. Try a shorter word, for example "binary" or "CPU".</p>'; rows = []; return; }
    out.innerHTML = hits.map(function (h, i) {
      return '<a href="' + window.MSK_BASE + h[1].u + '" class="' + (i === 0 ? "is-sel" : "") + '"><b>' + h[1].t + "</b><small>" + h[1].s + "</small></a>";
    }).join("");
    rows = Array.prototype.slice.call(out.querySelectorAll("a")); sel = 0;
  }
  if (input) {
    input.addEventListener("input", function () { render(input.value); });
    input.addEventListener("keydown", function (e) {
      if (e.key === "ArrowDown" || e.key === "ArrowUp") {
        e.preventDefault();
        if (!rows.length) return;
        rows[sel].classList.remove("is-sel");
        sel = (sel + (e.key === "ArrowDown" ? 1 : rows.length - 1)) % rows.length;
        rows[sel].classList.add("is-sel");
        rows[sel].scrollIntoView({ block: "nearest" });
      } else if (e.key === "Enter") {
        if (rows.length) { e.preventDefault(); rows[sel].click(); }
      }
    });
  }
  document.addEventListener("click", function (e) {
    if (e.target.closest && e.target.closest("[data-search-open]")) { e.preventDefault(); openSearch(); }
    if (shell && !shell.hidden && e.target === shell) closeSearch();
  });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape" && shell && !shell.hidden) closeSearch();
    if ((e.key === "/" || (e.key === "k" && (e.metaKey || e.ctrlKey))) && !/^(INPUT|TEXTAREA|SELECT)$/.test(document.activeElement.tagName)) {
      e.preventDefault(); openSearch();
    }
  });

  /* ----------------------------------------------------- topic progress
     Marks a topic as visited so key stage pages can show a done dot. */
  var page = document.body.getAttribute("data-topic");
  if (page) {
    var seen = store.get("seen", {});
    seen[page] = Date.now();
    store.set("seen", seen);
  }
  var seenNow = store.get("seen", {});
  document.querySelectorAll("[data-topic-ref]").forEach(function (el) {
    if (seenNow[el.getAttribute("data-topic-ref")]) {
      var slot = el.querySelector("[data-done-slot]");
      if (slot) slot.innerHTML = '<span class="done-dot" title="You have opened this topic"></span>';
    }
  });

  /* --------------------------------------------------- reset all data */
  document.addEventListener("click", function (e) {
    var b = e.target.closest && e.target.closest("[data-reset-progress]");
    if (!b) return;
    if (!window.confirm("This clears every saved score and note stored in this browser. Continue?")) return;
    ["seen", "quiz", "exam", "theme", "mascot"].forEach(store.del);
    window.location.reload();
  });
})();
