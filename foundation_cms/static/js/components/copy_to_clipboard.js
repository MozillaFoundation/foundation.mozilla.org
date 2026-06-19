const DEFAULT_SELECTOR = ".copy-to-clipboard-button";

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
    el.innerText = gettext("Copied");
  } catch (err) {
    el.innerText = gettext("Copy failed");
  } finally {
    document.body.removeChild(textArea);
  }
}

/**
 * Handles a copy-to-clipboard button click.
 * Copies the current URL (without parameters or hash) to clipboard
 * and updates the button text to "Copied".
 *
 * @function handleCopyClick
 * @param {MouseEvent} event - The click event object
 * @returns {void}
 */
function handleCopyClick(event) {
  const el = event.currentTarget;
  const url = window.location.href.split("?")[0].split("#")[0];
  if (navigator.clipboard && navigator.clipboard.writeText) {
    navigator.clipboard
      .writeText(url)
      .then(() => {
        el.innerText = gettext("Copied");
      })
      .catch(() => {
        copyWithFallback(el, url);
      });
  } else {
    copyWithFallback(el, url);
  }
}

/**
 * Initializes copy-to-clipboard functionality for all matching buttons on the page.
 *
 * @param {string} [selector] - CSS selector for buttons. Defaults to `.copy-to-clipboard-button`.
 */
export function initCopyToClipboardButtons(selector = DEFAULT_SELECTOR) {
  const buttons = document.querySelectorAll(selector);
  buttons.forEach((button) => {
    button.addEventListener("click", handleCopyClick);
  });
}
