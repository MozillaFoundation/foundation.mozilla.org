export function setupTito() {
    globalThis.tito = globalThis.tito || function() {
        (tito.q = tito.q || []).push(arguments);
    };

    tito('on:registration:finished', function(data) {
        console.log(data);
    });
};
