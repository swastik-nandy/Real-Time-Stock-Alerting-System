// Show a notification
function showNotification(stockSymbol, message) {
    if (Notification.permission === 'granted') {
        const notification = new Notification(stockSymbol, {
            body: message,
            icon: '/static/accounts/img/stock_alert_icon.png' // Optional icon
        });

        notification.onclick = function(event) {
            event.preventDefault();
            window.focus(); // Focus the browser tab when clicked
        };
    }
}

// Ask permission on page load
function askNotificationPermission() {
    if ('Notification' in window) {
        Notification.requestPermission().then(function(permission) {
            console.log('Notification permission:', permission);
        });
    }
}
askNotificationPermission();

// Poll backend for triggered alerts every 5 seconds
function pollForNotifications() {
    setInterval(() => {
        fetch('/accounts/check-alerts/')
            .then(response => response.json())
            .then(data => {
                data.alerts.forEach(alert => {
                    showNotification(alert.stock, alert.message);
                });
            })
            .catch(error => {
                console.error("Error polling for alerts:", error);
            });
    }, 5000);
}
pollForNotifications();

// Register push subscription and send to backend
if ('serviceWorker' in navigator && 'PushManager' in window) {
    navigator.serviceWorker.ready.then(function(registration) {
        registration.pushManager.subscribe({
            userVisibleOnly: true,
            applicationServerKey: VAPID_PUBLIC_KEY // <-- passed from template
        }).then(function(subscription) {
            fetch('/accounts/save-subscription/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify(subscription)
            });
        }).catch(function(err) {
            console.error('Push subscription error:', err);
        });
    });
}
