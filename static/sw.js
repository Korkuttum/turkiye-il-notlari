/* Basit önbellek: kabuk + harita verisi çevrimdışı çalışsın, API her zaman ağdan gelsin. */
const CACHE = "il-notlari-v1";
const KABUK = [
  "/",
  "/static/tr-cities.json",
  "/static/manifest.webmanifest",
  "/static/icons/icon-192.png",
  "/static/icons/icon-512.png",
  "/static/icons/apple-touch-icon.png"
];

self.addEventListener("install", (e) => {
  e.waitUntil(caches.open(CACHE).then((c) => c.addAll(KABUK)).then(() => self.skipWaiting()));
});

self.addEventListener("activate", (e) => {
  e.waitUntil(
    caches.keys()
      .then((ks) => Promise.all(ks.filter((k) => k !== CACHE).map((k) => caches.delete(k))))
      .then(() => self.clients.claim())
  );
});

self.addEventListener("fetch", (e) => {
  const url = new URL(e.request.url);
  if (e.request.method !== "GET" || url.origin !== location.origin) return;

  // Notlar her zaman güncel olmalı -> ağ öncelikli
  if (url.pathname.startsWith("/api/")) {
    e.respondWith(fetch(e.request).catch(() => caches.match(e.request)));
    return;
  }

  // Kabuk ve statik dosyalar -> önbellek öncelikli
  e.respondWith(
    caches.match(e.request).then((hit) => {
      const agdan = fetch(e.request).then((res) => {
        if (res.ok) {
          const kopya = res.clone();
          caches.open(CACHE).then((c) => c.put(e.request, kopya));
        }
        return res;
      }).catch(() => hit);
      return hit || agdan;
    })
  );
});
