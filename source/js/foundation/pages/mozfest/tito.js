export function setupTito() {
    globalThis.tito = globalThis.tito || function() {
        (tito.q = tito.q || []).push(arguments);
    };

    tito('on:registration:finished', function(data) {
        const redirectURL = document.querySelector(`input[name="tito-post-registration-url"]`)?.value;
        if (redirectURL) {
            globalThis.location = redirectURL;
        }
    });
};
