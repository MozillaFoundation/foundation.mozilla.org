/**
 * Adds character countdowns to Wagtail's non-rich-text fields.
 *
 * Native maxlength attributes are hard limits. The data-max-length attribute
 * used by CharCountWidget is a legacy soft limit and takes precedence when
 * both attributes are present.
 */

const FIELD_SELECTOR = [
  ".max-length-warning[data-max-length]",
  '.w-field__input input[maxlength]:not([type="hidden"])',
  ".w-field__input textarea[maxlength]",
].join(", ");

const RICH_TEXT_SELECTOR = [
  ".Draftail-root",
  "[data-draftail-input]",
  '[data-controller~="w-draftail"]',
  ".w-field--draftail_rich_text_area",
].join(", ");

/**
 * Gets the configured character limit for a field.
 *
 * @param {HTMLInputElement|HTMLTextAreaElement} field
 * @returns {number|null}
 */
function getCharacterLimit(field) {
  const configuredLimit =
    field.dataset.maxLength || field.getAttribute("maxlength");
  const limit = Number.parseInt(configuredLimit, 10);

  return Number.isInteger(limit) && limit > 0 ? limit : null;
}

/**
 * Formats the remaining count for editors and assistive technology.
 *
 * @param {number} remaining
 * @returns {string}
 */
function formatCount(remaining) {
  const characterCount = Math.abs(remaining);
  const characterLabel = characterCount === 1 ? "character" : "characters";

  if (remaining < 0) {
    return `${characterCount} ${characterLabel} over limit`;
  }

  return `${characterCount} ${characterLabel} remaining`;
}

/**
 * Updates one field's countdown.
 *
 * @param {HTMLInputElement|HTMLTextAreaElement} field
 * @param {HTMLElement} countdown
 * @param {number} limit
 * @returns {void}
 */
function updateCountdown(field, countdown, limit) {
  const remaining = limit - field.value.length;

  countdown.textContent = formatCount(remaining);
  countdown.classList.toggle("warning", remaining <= 0);
}

/**
 * Finds or creates the countdown associated with a field.
 *
 * @param {HTMLInputElement|HTMLTextAreaElement} field
 * @returns {HTMLElement}
 */
function getCountdown(field) {
  const existingCountdown = field.nextElementSibling;

  if (
    existingCountdown &&
    existingCountdown.classList.contains("max-length-countdown")
  ) {
    existingCountdown.setAttribute("aria-live", "polite");
    return existingCountdown;
  }

  const countdown = document.createElement("output");
  countdown.className = "max-length-countdown";
  countdown.setAttribute("aria-live", "polite");

  if (field.id) {
    countdown.setAttribute("for", field.id);
  }

  field.insertAdjacentElement("afterend", countdown);
  return countdown;
}

/**
 * Initializes a countdown for an eligible field once.
 *
 * @param {HTMLInputElement|HTMLTextAreaElement} field
 * @returns {void}
 */
function initializeField(field) {
  if (
    field.dataset.maxLengthCountdownInitialized === "true" ||
    field.closest(RICH_TEXT_SELECTOR)
  ) {
    return;
  }

  const limit = getCharacterLimit(field);

  if (limit === null) {
    return;
  }

  const countdown = getCountdown(field);
  field.dataset.maxLengthCountdownInitialized = "true";
  updateCountdown(field, countdown, limit);
  field.addEventListener("input", () => {
    updateCountdown(field, countdown, limit);
  });
}

/**
 * Initializes fields in a document or newly inserted StreamField subtree.
 *
 * @param {Document|Element} root
 * @returns {void}
 */
function initializeFields(root) {
  if (root.matches?.(FIELD_SELECTOR)) {
    initializeField(root);
  }

  root.querySelectorAll?.(FIELD_SELECTOR).forEach(initializeField);
}

document.addEventListener("DOMContentLoaded", () => {
  initializeFields(document);

  const observer = new MutationObserver((mutations) => {
    mutations.forEach((mutation) => {
      mutation.addedNodes.forEach((node) => {
        if (node.nodeType === Node.ELEMENT_NODE) {
          initializeFields(node);
        }
      });
    });
  });

  observer.observe(document.body, { childList: true, subtree: true });
});
