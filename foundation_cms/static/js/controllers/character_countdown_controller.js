const FIELD_SELECTOR = [
  ".max-length-warning[data-max-length]",
  'input[maxlength]:not([type="hidden"])',
  "textarea[maxlength]",
].join(", ");

const RICH_TEXT_SELECTOR = [
  ".Draftail-root",
  "[data-draftail-input]",
  '[data-controller~="w-draftail"]',
  ".w-field--draftail_rich_text_area",
].join(", ");

/**
 * Adds localized character countdowns to limited, non-rich-text fields in a
 * Wagtail edit form.
 *
 * A single delegated input listener supports StreamField blocks inserted
 * after connect without requiring per-block Telepath adapters.
 */
export default class extends window.StimulusModule.Controller {
  connect() {
    this.handleInput = this.handleInput.bind(this);
    this.element.addEventListener("input", this.handleInput);
    this.initializeFields();
  }

  disconnect() {
    this.element.removeEventListener("input", this.handleInput);
  }

  /**
   * Initializes fields rendered with the edit form.
   */
  initializeFields() {
    this.element.querySelectorAll(FIELD_SELECTOR).forEach((field) => {
      this.updateField(field);
    });
  }

  /**
   * Updates eligible fields, including fields in dynamically inserted blocks.
   *
   * @param {InputEvent} event
   */
  handleInput(event) {
    if (event.target.matches?.(FIELD_SELECTOR)) {
      this.updateField(event.target);
    }
  }

  /**
   * Updates one field's countdown if it has a valid limit and is not rich text.
   *
   * @param {HTMLInputElement|HTMLTextAreaElement} field
   */
  updateField(field) {
    if (field.closest(RICH_TEXT_SELECTOR)) {
      return;
    }

    const limit = this.getCharacterLimit(field);

    if (limit === null) {
      return;
    }

    const remaining = limit - field.value.length;
    const countdown = this.getCountdown(field);

    countdown.textContent = this.formatCount(remaining);
    countdown.classList.toggle("warning", remaining <= 0);
  }

  /**
   * Legacy data-max-length soft limits take precedence over native hard limits.
   *
   * @param {HTMLInputElement|HTMLTextAreaElement} field
   * @returns {number|null}
   */
  getCharacterLimit(field) {
    const configuredLimit =
      field.dataset.maxLength || field.getAttribute("maxlength");
    const limit = Number.parseInt(configuredLimit, 10);

    return Number.isInteger(limit) && limit > 0 ? limit : null;
  }

  /**
   * Finds or creates the accessible countdown associated with a field.
   *
   * @param {HTMLInputElement|HTMLTextAreaElement} field
   * @returns {HTMLElement}
   */
  getCountdown(field) {
    const existingCountdown = field.nextElementSibling;

    if (existingCountdown?.classList.contains("max-length-countdown")) {
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
   * Formats a localized singular or plural countdown message.
   *
   * @param {number} remaining
   * @returns {string}
   */
  formatCount(remaining) {
    const count = Math.abs(remaining);
    const message =
      remaining < 0
        ? window.ngettext(
            "%(count)s character over limit",
            "%(count)s characters over limit",
            count,
          )
        : window.ngettext(
            "%(count)s character remaining",
            "%(count)s characters remaining",
            count,
          );

    return window.interpolate(message, { count }, true);
  }
}
