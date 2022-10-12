/**
 * Datawrapper block iframes handle their responsiveness through an injected inline script.
 * Since these are injected by datawrapper themselves with no way to pass our CSP nonce value,
 * the scripts will not run. This file looks for data-wrapper blocks, and if any exist,
 * implements responsiveness through an event listener.
 *
 * For more context see: https://github.com/mozilla/foundation.mozilla.org/issues/9466
 */

export default () => {
  // Searching for any datawrapper blocks
  const dataWrapperBlocks = document.querySelectorAll(".datawrapper-block");

  // If any exist, add event listener to handle responsiveness
  if (dataWrapperBlocks) {
    window.addEventListener("message", function (e) {
      if (void 0 !== e.data["datawrapper-height"]) {
        var t = document.querySelectorAll("iframe");
        for (var a in e.data["datawrapper-height"])
          for (var r = 0; r < t.length; r++) {
            if (t[r].contentWindow === e.source)
              t[r].style.height = e.data["datawrapper-height"][a] + "px";
          }
      }
    });
  }
};
