const SELECTORS = {
  shareButtons:
    ".petition__share-button-wrapper button, .petition__share-button-wrapper a",
};

/**
 * Copies text to clipboard using the legacy execCommand approach as a fallback
 * when the modern Clipboard API is unavailable or fails.
 *
 * @function copyWithFallback
 * @param {HTMLElement} el - The element whose text content will be updated with copy status
 * @param {string} url - The URL to copy to the clipboard
 * @returns {void}
 */
function copyWithFallback(el, url) {
  const textArea = document.createElement("textarea");
  textArea.value = url;
  textArea.style.position = "fixed";
  textArea.style.opacity = "0";
  document.body.appendChild(textArea);
  textArea.select();

  try {
    document.execCommand("copy");
    el.innerText = "Copied";
  } catch (err) {
    el.innerText = "Copy failed";
  } finally {
    document.body.removeChild(textArea);
  }
}

/**
 * Handles the share button click event.
 * If the button has a data-sp-target attribute, it triggers the corresponding Share Progress anchor.
 * Otherwise, it copies the current URL (without parameters or hash) to clipboard.
 *
 * @function handleShareButtonClick
 * @param {MouseEvent} event - The click event object
 * @returns {void}
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
    if (navigator.clipboard && navigator.clipboard.writeText) {
      navigator.clipboard
        .writeText(url)
        .then(() => {
          el.innerText = "Copied";
        })
        .catch(() => {
          copyWithFallback(el, url);
        });
    } else {
      copyWithFallback(el, url);
    }
  }
}

/**
 * Initializes share button functionality for all share buttons on the page.
 * Sets up click event listeners that prevent default behavior and handle sharing.
 */
export function initShareButtons() {
  const shareButtons = document.querySelectorAll(SELECTORS.shareButtons);
  shareButtons.forEach((shareButton) => {
    shareButton.addEventListener("click", handleShareButtonClick);
  });
}
