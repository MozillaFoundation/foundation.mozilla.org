/**
 * Set up event listeners for Tito widget
 * Tito API Doc: https://ti.to/docs/api/widget#tito-widget-v2-callbacks
 */

export function setupTitoEventListener() {
  window.tito =
    window.tito ||
    function () {
      (tito.q = tito.q || []).push(arguments);
    };

  tito("on:widget:loaded", function () {
    // To address a bug when the sticky button is blocking users to access full content on Tito popup
    // See https://github.com/MozillaFoundation/foundation.mozilla.org/issues/10307
    try {
      document
        .querySelector(`.narrow-sticky-button-container`)
        .classList.add("hidden");
    } catch (e) {
      // Do nothing
    }
  });
}

export function loadTitoLibrary() {
  var script = document.createElement("script");

  script.src = "https://js.tito.io/v2";

  script.onload = function () {
    console.log("Tito loaded");
  };

  document.body.appendChild(script);
}
