/**
 * Checking if the user is on a mobile device.
 * If on desktop, render download buttons. If on mobile, render email reminder button.
 */

class BrowserExtension {
  constructor() {
    this.checkForMobile();
  }

  checkForMobile() {
    if (
      /Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(
        navigator.userAgent
      )
    ) {
      document
        .querySelector(".download-link-button--firefox")
        .classList.add("tw-hidden");
      document
        .querySelector(".download-link-button--chrome")
        .classList.add("tw-hidden");
      document
        .querySelector(".download-link-button--email")
        .classList.remove("tw-hidden");
    } else {
      // false for not mobile device
      document
        .querySelector(".download-link-button--email")
        .classList.add("tw-hidden");
      document
        .querySelector(".download-link-button--firefox")
        .classList.remove("tw-hidden");
      document
        .querySelector(".download-link-button--chrome")
        .classList.remove("tw-hidden");
    }
  }
}

export default BrowserExtension;
