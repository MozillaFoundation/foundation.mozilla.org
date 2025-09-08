const SELECTORS = {
  copyButton: ".copy-link-share-btn",
  emailButton: ".email-share-btn",
};

export default function initShareContainer() {
  const copyButtons = document.querySelectorAll(SELECTORS.copyButton);
  const emailButtons = document.querySelectorAll(SELECTORS.emailButton);

  if (!copyButtons.length && !emailButtons.length) return;

  /**
   * Shows success state by adding CSS class
   * @param {Element} button - Button element to modify
   * @param {string} successClass - CSS class to add
   * @param {number} duration - Duration in ms (0 = permanent until page reload by default)
   * @param {boolean} showCopiedText - Whether to show "Copied" alt text
   */
  function showSuccess(button, successClass, duration = 0, showCopiedText = false) {
    button.classList.add(successClass);

    // Update img title text and aria-label for copy button
    if (showCopiedText) {
      const img = button.querySelector("img");
      if (img) {
        img.title = "Copied";
      }
      button.setAttribute("aria-label", "Copied");
    }

    // Remove success state after duration (if specified)
    if (duration > 0) {
      setTimeout(() => {
        button.classList.remove(successClass);

        // Reset img title text and aria-label only if it was changed
        if (showCopiedText) {
          const img = button.querySelector("img");
          if (img) {
            img.title = "Copy Link";
          }
          button.setAttribute("aria-label", "Copy Link");
        }
      }, duration);
    }
  }

  copyButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const url = btn.getAttribute("data-copy-url");
      if (!url) return;

      navigator.clipboard
        .writeText(url)
        .then(() => {
          showSuccess(btn, "copy-success", 0, true);
        })
        .catch((error) => {
          console.log("Copy failed:", error);
        });
    });
  });

  emailButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      showSuccess(btn, "email-success");
    });
  });
}
