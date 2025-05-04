self.addEventListener('push', function(event) {
    const data = event.data ? event.data.text() : 'New stock alert!';
    
    const options = {
        body: data,
        icon: '/static/accounts/img/stock_alert_icon.png', // Optional
        badge: '/static/accounts/img/stock_alert_icon.png'  // Optional
    };

    event.waitUntil(
        self.registration.showNotification("Stock Alert", options)
    );
});

self.addEventListener('notificationclick', function(event) {
    event.notification.close();
    event.waitUntil(
        clients.matchAll({ type: "window" }).then(function(clientList) {
            if (clientList.length > 0) {
                return clientList[0].focus();
            }
            return clients.openWindow('/');
        })
    );
});
