'use strict';

self.addEventListener('push' , function(event){
	console.log('[Service Worker] Push Received');
	console.log('[Service Worker] Push had this data: "${event.data.text()}"');

	const title = 'E-malli';
	const options = {
		icon    : 'avatar.png',
		badge   : 'avatar.png',
		body    : 'Water Level Critically Low',
		vibrate : [100 , 50 , 100],
		action  : '/home'
	}

	event.waitUntil(self.registration.showNotification(title , options));
});