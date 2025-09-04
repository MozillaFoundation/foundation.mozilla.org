const SELECTORS = {
  copyButton: ".copy-link-btn",
  toast: "#toast",
};

const MESSAGES = {
  success: "Link copied to clipboard!",
  error: "Could not copy link.",
};

export default function initShareContainer() {
  const copyButtons = document.querySelectorAll(SELECTORS.copyButton);
  const toast = document.querySelector(SELECTORS.toast);

  if (!copyButtons.length || !toast) return;

  function showToast(message) {
    toast.textContent = message;
    toast.classList.add("visible");

    setTimeout(() => {
      toast.classList.remove("visible");
    }, 2500);
  }

  copyButtons.forEach((btn) => {
    btn.addEventListener("click", () => {
      const url = btn.getAttribute("data-copy-url");
      if (!url) {
        showToast("No URL to copy");
        return;
      }

      navigator.clipboard
        .writeText(url)
        .then(() => {
          showToast(MESSAGES.success);
        })
        .catch((error) => {
          showToast(MESSAGES.error);
        });
    });
  });
}
