const SELECTORS = {
  shareButtons:
    ".petition__share-button-wrapper button, .petition__share-button-wrapper a",
};

/**
 * Handles the share button click event.
 * If the button has a data-sp-target attribute, it triggers the corresponding share progress anchor.
 * Otherwise, it copies the current URL (without parameters or hash) to clipboard.
 *
 * @function handleShareButtonClick
 * @param {MouseEvent} event - The click event object
 */
function handleShareButtonClick(event) {
  const el = event.currentTarget;
  const shareProgressTarget = el.getAttribute("data-sp-target");

  if (shareProgressTarget) {
    const shareProgressButtonAnchor = document.querySelector(
      `#${shareProgressTarget} a`,
    );
    if (shareProgressButtonAnchor) {
      shareProgressButtonAnchor.click();
    }
  } else {
    const url = window.location.href.split("?")[0].split("#")[0];
    navigator.clipboard.writeText(url);
    el.innerText = "Copied";
  }
}

/**
 * Initializes share button functionality for all share buttons on the page.
 * Sets up click event listeners that prevent default behavior and handle sharing.
 */
export function initShareButtons() {
  const shareButtons = document.querySelectorAll(SELECTORS.shareButtons);
  shareButtons.forEach((shareButton) => {
    shareButton.addEventListener("click", (e) => {
      e.preventDefault();
      handleShareButtonClick(e);
    });
  });
}
