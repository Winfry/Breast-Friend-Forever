// Service Worker for Breast Friend Forever Mobile App
const CACHE_NAME = 'bff-mobile-v2.1.0';
const STATIC_CACHE = 'bff-static-v2.1.0';
const DYNAMIC_CACHE = 'bff-dynamic-v2.1.0';

// Essential files to cache for offline functionality
const urlsToCache = [
    '/',
    '/index.html',
    '/mobile-styles.css',
    '/mobile-app.js',
    '/manifest.json',
    '/static/icons/icon-72x72.png',
    '/static/icons/icon-96x96.png',
    '/static/icons/icon-144x144.png',
    '/static/icons/icon-192x192.png',
    '/static/icons/icon-512x512.png',
    '/static/screenshots/mobile-chat.png',
    '/static/screenshots/hospital-search.png',
    '/static/screenshots/health-tips.png'
];

// INSTALL: Cache essential resources
self.addEventListener('install', function(event) {
    console.log('🔄 Service Worker installing...');
    event.waitUntil(
        caches.open(STATIC_CACHE)
            .then(function(cache) {
                console.log('📦 Caching app shell for offline use');
                return cache.addAll(urlsToCache);
            })
            .then(() => {
                console.log('✅ App shell cached successfully');
                return self.skipWaiting();
            })
            .catch(error => {
                console.error('❌ Cache installation failed:', error);
            })
    );
});

// ACTIVATE: Clean up old caches
self.addEventListener('activate', function(event) {
    console.log('🎯 Service Worker activating...');
    event.waitUntil(
        caches.keys().then(function(cacheNames) {
            return Promise.all(
                cacheNames.map(function(cacheName) {
                    if (![STATIC_CACHE, DYNAMIC_CACHE].includes(cacheName)) {
                        console.log('🗑️ Deleting old cache:', cacheName);
                        return caches.delete(cacheName);
                    }
                })
            );
        }).then(() => {
            console.log('✅ Service Worker activated and ready');
            return self.clients.claim();
        })
    );
});

// FETCH: Smart caching strategy
self.addEventListener('fetch', function(event) {
    // Skip non-GET requests
    if (event.request.method !== 'GET') return;

    const requestUrl = new URL(event.request.url);

    // Handle API requests differently
    if (requestUrl.pathname.startsWith('/api/')) {
        event.respondWith(handleApiRequest(event.request));
    } else {
        event.respondWith(handleStaticRequest(event.request));
    }
});

// Handle API requests with network-first strategy
async function handleApiRequest(request) {
    const cache = await caches.open(DYNAMIC_CACHE);
    
    try {
        // Try network first for API calls
        const networkResponse = await fetch(request);
        
        if (networkResponse.ok) {
            // Cache successful API responses for offline fallback
            cache.put(request, networkResponse.clone());
            return networkResponse;
        }
        throw new Error('Network response not ok');
    } catch (error) {
        // Network failed, try cache
        console.log('🌐 Network failed, trying cache for:', request.url);
        const cachedResponse = await cache.match(request);
        
        if (cachedResponse) {
            return cachedResponse;
        }
        
        // Return meaningful offline response for API calls
        if (request.url.includes('/api/mobile/chat')) {
            return new Response(JSON.stringify({
                response: "I'm currently offline, but I'm still here for you! Your message will be sent when connection is restored.",
                suggestions: ["Check connection", "Try again later", "Emergency contacts"],
                is_offline: true
            }), {
                headers: { 'Content-Type': 'application/json' }
            });
        }
        
        if (request.url.includes('/api/mobile/hospitals')) {
            return new Response(JSON.stringify({
                facilities: [],
                message: "Offline mode: Hospital data unavailable. Please check your connection.",
                is_offline: true
            }), {
                headers: { 'Content-Type': 'application/json' }
            });
        }
        
        // Generic offline response
        return new Response(JSON.stringify({
            error: "You're offline",
            message: "Please check your internet connection and try again"
        }), {
            status: 503,
            headers: { 'Content-Type': 'application/json' }
        });
    }
}

// Handle static requests with cache-first strategy
async function handleStaticRequest(request) {
    const cachedResponse = await caches.match(request);
    if (cachedResponse) {
        return cachedResponse;
    }
    
    try {
        const networkResponse = await fetch(request);
        if (networkResponse.ok) {
            const cache = await caches.open(STATIC_CACHE);
            cache.put(request, networkResponse.clone());
        }
        return networkResponse;
    } catch (error) {
        // If both cache and network fail, return offline page for navigation requests
        if (request.mode === 'navigate') {
            return caches.match('/offline.html');
        }
        throw error;
    }
}

// Background Sync for offline messages
self.addEventListener('sync', function(event) {
    if (event.tag === 'background-sync-messages') {
        console.log('🔄 Background sync triggered for messages');
        event.waitUntil(syncOfflineMessages());
    }
});

async function syncOfflineMessages() {
    // Implement background sync for offline chat messages
    console.log('Syncing offline messages...');
}

// Push Notifications
self.addEventListener('push', function(event) {
    if (!event.data) return;
    
    const data = event.data.json();
    const options = {
        body: data.body || 'Your breast health companion has updates!',
        icon: '/static/icons/icon-192x192.png',
        badge: '/static/icons/icon-72x72.png',
        vibrate: [200, 100, 200],
        data: data.url || '/',
        actions: [
            {
                action: 'open',
                title: 'Open App'
            },
            {
                action: 'dismiss', 
                title: 'Dismiss'
            }
        ]
    };
    
    event.waitUntil(
        self.registration.showNotification('Breast Friend Forever', options)
    );
});

self.addEventListener('notificationclick', function(event) {
    event.notification.close();
    
    if (event.action === 'open') {
        event.waitUntil(
            clients.openWindow(event.notification.data || '/')
        );
    }
});