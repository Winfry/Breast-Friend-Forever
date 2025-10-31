// Enhanced Service Worker for Breast Friend Forever
const CACHE_NAME = 'bff-app-v2.1.0';
const STATIC_CACHE = 'bff-static-v2.1.0';
const DYNAMIC_CACHE = 'bff-dynamic-v2.1.0';

// Essential files to cache for offline functionality
const urlsToCache = [
  '/',
  '/static/manifest.json',
  '/static/css/app.css',
  '/static/js/app.js',
  '/static/icons/icon-72x72.png',
  '/static/icons/icon-96x96.png',
  '/static/icons/icon-144x144.png',
  '/static/icons/icon-192x192.png',
  '/static/icons/icon-512x512.png',
  '/static/screenshots/mobile-chat.png'
];

// INSTALL: Cache essential resources
self.addEventListener('install', function(event) {
  console.log('Service Worker installing...');
  event.waitUntil(
    caches.open(STATIC_CACHE)
      .then(function(cache) {
        console.log('Caching app shell');
        return cache.addAll(urlsToCache);
      })
      .then(() => self.skipWaiting()) // Activate immediately
  );
});

// ACTIVATE: Clean up old caches
self.addEventListener('activate', function(event) {
  console.log('Service Worker activating...');
  event.waitUntil(
    caches.keys().then(function(cacheNames) {
      return Promise.all(
        cacheNames.map(function(cacheName) {
          if (![STATIC_CACHE, DYNAMIC_CACHE].includes(cacheName)) {
            console.log('Deleting old cache:', cacheName);
            return caches.delete(cacheName);
          }
        })
      );
    }).then(() => self.clients.claim()) // Take control immediately
  );
});

// FETCH: Smart caching strategy
self.addEventListener('fetch', function(event) {
  // Skip non-GET requests and browser extensions
  if (event.request.method !== 'GET' || 
      event.request.url.startsWith('chrome-extension://')) {
    return;
  }

  event.respondWith(
    caches.match(event.request)
      .then(function(response) {
        // Return cached version if available
        if (response) {
          return response;
        }

        // Clone the request for network fallback
        const fetchRequest = event.request.clone();

        return fetch(fetchRequest).then(function(response) {
          // Check if valid response
          if (!response || response.status !== 200 || response.type !== 'basic') {
            return response;
          }

          // Clone the response for caching
          const responseToCache = response.clone();

          // Cache dynamic requests (API calls, images, etc.)
          caches.open(DYNAMIC_CACHE)
            .then(function(cache) {
              // Don't cache API endpoints that should be fresh
              if (!event.request.url.includes('/api/chat') && 
                  !event.request.url.includes('/api/hospitals')) {
                cache.put(event.request, responseToCache);
              }
            });

          return response;
        }).catch(function(error) {
          // Network failure - you could return a custom offline page
          console.log('Fetch failed; returning offline page:', error);
          
          // For navigation requests, return offline page
          if (event.request.mode === 'navigate') {
            return caches.match('/offline.html');
          }
          
          // For API calls, return meaningful offline response
          if (event.request.url.includes('/api/')) {
            return new Response(
              JSON.stringify({ 
                error: 'You are offline', 
                suggestions: ['Check connection', 'Try again later'] 
              }),
              { headers: { 'Content-Type': 'application/json' } }
            );
          }
        });
      })
  );
});

// BACKGROUND SYNC (Future Enhancement)
self.addEventListener('sync', function(event) {
  if (event.tag === 'background-sync') {
    console.log('Background sync triggered');
    // Handle background data synchronization
  }
});

// PUSH NOTIFICATIONS (Future Enhancement)  
self.addEventListener('push', function(event) {
  const options = {
    body: 'Your breast health companion has updates!',
    icon: '/static/icons/icon-192x192.png',
    badge: '/static/icons/icon-72x72.png',
    vibrate: [200, 100, 200]
  };
  
  event.waitUntil(
    self.registration.showNotification('Breast Friend Forever', options)
  );
});