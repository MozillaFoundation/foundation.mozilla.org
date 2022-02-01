/**
 * Using the tito library to set up a ticket purchasing widget.
 * This file is to hook into a callback which runs when someone completes registration.
 */

export function setupTito() {
  globalThis.tito =
    globalThis.tito ||
    function () {
      (tito.q = tito.q || []).push(arguments);
    };

  tito("on:registration:finished", function (data) {
    // TODO: this callback will be needed for #7435
    console.log("Finished");
  });
}
