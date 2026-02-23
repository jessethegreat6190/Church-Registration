const CACHE_NAME = 'grace-church-v1';
const ASSETS = [
  '/',
  '/index.html',
  '/dashboard.html',
  '/church logo/New Logo 2026.png'
];

self.addEventListener('install', (e) => {
  e.waitUntil(
    caches.open(CACHE_NAME).then((cache) => {
      return cache.addAll(ASSETS);
    })
  );
});

self.addEventListener('fetch', (e) => {
  e.respondWith(
    caches.match(e.request).then((response) => {
      return response || fetch(e.request);
    })
  );
});
