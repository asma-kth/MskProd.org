/* MskProd Computing — service worker.
 *
 * Strategy, by request type:
 *   navigations   network first, falling back to the cached copy, then to the
 *                 offline page. A topic a student has already opened stays
 *                 readable with no signal.
 *   same-origin   stale while revalidate, so the shell paints instantly and
 *   assets        picks up a new build on the next visit.
 *   web fonts     cache first; they never change under a given URL.
 *
 * BUILD_ID is substituted at build time from a hash of the built assets, so a
 * deploy that changes the CSS or JS lands in fresh caches and the old ones are
 * deleted on activate.
 */
var BUILD = "__BUILD_ID__";
var SHELL = "shell-" + BUILD;
var PAGES = "pages-" + BUILD;
var FONTS = "fonts-v1";

/* Kept small on purpose: this is what must be present for the app to open
   offline at all. Everything else is cached as it is used. */
var SHELL_URLS = [
  "/",
  "/offline/",
  "/assets/css/site.css",
  "/assets/js/app.js",
  "/assets/js/mascot.js",
  "/assets/img/logo.svg",
  "/assets/img/mascot.svg",
  "/assets/img/icon-192.png",
  "/assets/img/favicon.svg",
  "/site.webmanifest"
];

/* Pyodide is tens of megabytes and is fetched only when a student presses Run,
   so it is deliberately never cached. Ad and consent requests must always be
   live: a cached ad script would serve stale creatives and would keep working
   after a visitor withdrew consent. */
var NEVER_CACHE = /^https:\/\/(cdn\.jsdelivr\.net|pagead2\.googlesyndication\.com|googleads\.g\.doubleclick\.net|fundingchoicesmessages\.google\.com|ep[12]\.adtrafficquality\.google)\//;
var FONT_HOSTS = /^https:\/\/fonts\.(googleapis|gstatic)\.com\//;

self.addEventListener("install", function (e) {
  e.waitUntil(
    caches.open(SHELL).then(function (c) {
      // addAll is atomic: one 404 would throw away the whole install, and a
      // renamed asset should not stop the worker taking over.
      return Promise.all(SHELL_URLS.map(function (u) {
        return c.add(new Request(u, { cache: "reload" })).catch(function () {});
      }));
    }).then(function () { return self.skipWaiting(); })
  );
});

self.addEventListener("activate", function (e) {
  e.waitUntil(
    caches.keys().then(function (keys) {
      return Promise.all(keys.map(function (k) {
        if (k === SHELL || k === PAGES || k === FONTS) return null;
        return caches.delete(k);
      }));
    }).then(function () { return self.clients.claim(); })
  );
});

function putSafe(cacheName, req, res) {
  // Only full, basic/cors 200s are worth keeping. Caching an opaque or partial
  // response would let a failed request masquerade as a good one later.
  if (!res || res.status !== 200 || (res.type !== "basic" && res.type !== "cors")) return;
  var copy = res.clone();
  caches.open(cacheName).then(function (c) { c.put(req, copy); }).catch(function () {});
}

self.addEventListener("fetch", function (e) {
  var req = e.request;
  if (req.method !== "GET") return;

  var url;
  try { url = new URL(req.url); } catch (err) { return; }
  if (NEVER_CACHE.test(req.url)) return;

  if (FONT_HOSTS.test(req.url)) {
    e.respondWith(
      caches.match(req).then(function (hit) {
        return hit || fetch(req).then(function (res) {
          putSafe(FONTS, req, res); return res;
        });
      }).catch(function () { return fetch(req); })
    );
    return;
  }

  if (url.origin !== self.location.origin) return;

  if (req.mode === "navigate") {
    e.respondWith(
      fetch(req).then(function (res) {
        putSafe(PAGES, req, res);
        return res;
      }).catch(function () {
        return caches.match(req).then(function (hit) {
          return hit || caches.match("/offline/").then(function (off) {
            return off || new Response(
              "<h1>Offline</h1><p>This page has not been opened before, so there is no saved copy.</p>",
              { headers: { "Content-Type": "text/html; charset=utf-8" }, status: 503 });
          });
        });
      })
    );
    return;
  }

  // Static assets: serve the cached copy at once, refresh it in the background.
  e.respondWith(
    caches.match(req).then(function (hit) {
      var net = fetch(req).then(function (res) {
        putSafe(SHELL, req, res);
        return res;
      }).catch(function () { return hit; });
      return hit || net;
    })
  );
});
