// Register the Service Worker for CareerFlow PWA

if ('serviceWorker' in navigator) {
    window.addEventListener('load', function () {
        navigator.serviceWorker
            .register('/service-worker.js')
            .then(function (registration) {
                console.log(
                    'CareerFlow Service Worker registered:',
                    registration.scope
                );
            })
            .catch(function (error) {
                console.error(
                    'Service Worker registration failed:',
                    error
                );
            });
    });
}