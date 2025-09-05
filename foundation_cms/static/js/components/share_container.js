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
   */
  function showSuccess(button, successClass, duration = 0) {
    button.classList.add(successClass);

    // Remove success state after duration (if specified)
    if (duration > 0) {
      setTimeout(() => {
        button.classList.remove(successClass);
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
          showSuccess(btn, "copy-success");
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
