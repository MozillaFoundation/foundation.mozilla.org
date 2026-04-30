const SELECTORS = {
  close: "[data-lightbox-close]",
  inner: ".expert-hub-card__inner",
  image: ".expert-hub-card__image",
  quote: ".expert-hub-card__quote",
  name: ".expert-hub-card__name",
  link: ".expert-hub-card__link",
  bubbleImage: ".expert-hub-bubble__image",
};

const FOCUSABLE_SELECTOR = [
  "button:not([disabled])",
  "a[href]:not([disabled])",
  'input:not([disabled]):not([type="hidden"])',
  "select:not([disabled])",
  "textarea:not([disabled])",
  '[tabindex]:not([tabindex="-1"])',
].join(", ");

/**
 * Wires the expert profile overlay: fills content from a bubble, manages scroll lock,
 * focus return, Tab trapping, backdrop click, and Escape.
 *
 * @param {HTMLElement | null} cardEl - `#expert-hub-card` dialog root
 * @returns {null | {
 *   open: function(HTMLElement): void,
 *   close: function(): void,
 *   bindListeners: function(AbortSignal): void,
 * }}
 *   `null` if `cardEl` is missing or required panel nodes are not found in the DOM.
 */
export function setupLightbox(cardEl) {
  if (!cardEl) return null;

  const closeBtn = cardEl.querySelector(SELECTORS.close);
  const inner = cardEl.querySelector(SELECTORS.inner);
  const imageEl = cardEl.querySelector(SELECTORS.image);
  const quoteEl = cardEl.querySelector(SELECTORS.quote);
  const nameEl = cardEl.querySelector(SELECTORS.name);
  const linkEl = cardEl.querySelector(SELECTORS.link);

  if (!inner || !imageEl || !quoteEl || !nameEl || !linkEl) {
    return null;
  }

  let previouslyFocused = null;

  /**
   * @returns {HTMLElement[]} Focusable controls inside the dialog (for Tab trapping).
   */
  function listFocusables() {
    return [...cardEl.querySelectorAll(FOCUSABLE_SELECTOR)];
  }

  /**
   * Keeps keyboard focus inside the dialog while it is open.
   *
   * @param {KeyboardEvent} e
   */
  function trapTabKey(e) {
    if (e.key !== "Tab" || cardEl.hasAttribute("hidden")) return;
    const items = listFocusables();
    if (items.length === 0) return;

    const first = items[0];
    const last = items[items.length - 1];
    const active = document.activeElement;
    const activeInside = cardEl.contains(active);

    if (e.shiftKey) {
      if (!activeInside || active === first) {
        e.preventDefault();
        last.focus();
      }
    } else if (!activeInside || active === last) {
      e.preventDefault();
      first.focus();
    }
  }

  /**
   * Populates the overlay from `dataset` / image on a bubble and shows it.
   * Locks body scroll and moves focus to the close control.
   *
   * @param {HTMLElement} el - `.expert-hub-bubble` list item
   */
  function open(el) {
    const bubbleImg = el.querySelector(SELECTORS.bubbleImage);
    imageEl.src = bubbleImg?.src ?? "";
    imageEl.alt = el.dataset.name ?? "";
    quoteEl.textContent = el.dataset.quote ?? "";
    nameEl.textContent = el.dataset.name ?? "";
    const profileUrl = el.dataset.url?.trim();
    if (profileUrl) linkEl.href = profileUrl;
    else linkEl.removeAttribute("href");

    const color = getComputedStyle(el)
      .getPropertyValue("--bubble-color")
      .trim();
    inner.style.setProperty("--bubble-color", color || "");

    previouslyFocused =
      document.activeElement instanceof HTMLElement
        ? document.activeElement
        : null;

    cardEl.removeAttribute("hidden");
    document.body.style.overflow = "hidden";
    closeBtn?.focus();
  }

  /**
   * Hides the overlay, restores body scroll and prior focus if still in the document.
   */
  function close() {
    cardEl.setAttribute("hidden", "");
    inner.style.removeProperty("--bubble-color");
    document.body.style.overflow = "";

    const restore = previouslyFocused;
    previouslyFocused = null;
    if (restore?.isConnected) {
      restore.focus({ preventScroll: true });
    }
  }

  /**
   * Registers close, backdrop, Tab trap, and Escape handlers; aborted when `signal` aborts.
   *
   * @param {AbortSignal} signal - Typically from `AbortController` owned by the viz teardown.
   */
  function bindListeners(signal) {
    closeBtn?.addEventListener("click", close, { signal });
    cardEl.addEventListener(
      "click",
      (e) => {
        if (e.target === cardEl) close();
      },
      { signal },
    );
    cardEl.addEventListener("keydown", trapTabKey, { signal });
    document.addEventListener(
      "keydown",
      (e) => {
        if (e.key === "Escape" && !cardEl.hasAttribute("hidden")) close();
      },
      { signal },
    );
  }

  return { open, close, bindListeners };
}
