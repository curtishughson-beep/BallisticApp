/* Moose Rifle Dope Card — offline service worker.
   Cache-first: once installed the app never needs the network again.
   Bump CACHE when the app changes so phones pick up the new version. */
const CACHE = "dope-card-v4";
const SHELL = [
  "./",
  "./index.html",
  "./manifest.webmanifest",
  "./icon-180.png",
  "./icon-192.png",
  "./icon-512.png"
];

self.addEventListener("install", e => {
  e.waitUntil(
    caches.open(CACHE)
      .then(c => c.addAll(SHELL))
      .then(() => self.skipWaiting())
  );
});

self.addEventListener("activate", e => {
  e.waitUntil(
    caches.keys()
      .then(keys => Promise.all(keys.filter(k => k !== CACHE).map(k => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", e => {
  if (e.request.method !== "GET") return;
  e.respondWith(
    caches.match(e.request, { ignoreSearch: true }).then(hit => {
      if (hit) {
        // Refresh in the background when there happens to be coverage.
        e.waitUntil(
          fetch(e.request)
            .then(res => res && res.ok && caches.open(CACHE).then(c => c.put(e.request, res.clone())))
            .catch(() => {})
        );
        return hit;
      }
      return fetch(e.request)
        .then(res => {
          if (res && res.ok && new URL(e.request.url).origin === location.origin) {
            const copy = res.clone();
            caches.open(CACHE).then(c => c.put(e.request, copy));
          }
          return res;
        })
        .catch(() => caches.match("./index.html"));
    })
  );
});
