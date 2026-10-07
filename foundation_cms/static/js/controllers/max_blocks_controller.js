// Insert and duplicate both add a block.
const ADD_BUTTON_SELECTOR =
  '.c-sf-add-button, [data-streamfield-action="DUPLICATE"]';

/**
 * Hides a StreamField's insert and duplicate buttons once it holds `max` blocks, since Wagtail only enforces max_num on save.
 */
export default class extends window.StimulusModule.Controller {
  static values = { max: Number };

  connect() {
    this.update = this.update.bind(this);
    // Deleting a block only changes its class/style, so watch those too.
    this.observer = new MutationObserver(this.update);
    this.observer.observe(this.element, {
      childList: true,
      subtree: true,
      attributes: true,
      attributeFilter: ["class", "style"],
    });
    this.update();
  }

  disconnect() {
    this.observer?.disconnect();
  }

  update() {
    const countInput = this.element.querySelector('input[name$="-count"]');
    if (!countInput) return;

    // Deleted blocks stay in the DOM until save, flagged by their `-deleted` input.
    const prefix = countInput.name.slice(0, -"-count".length);
    const deletedPattern = new RegExp(`^${prefix}-\\d+-deleted$`);
    const blockCount = [
      ...this.element.querySelectorAll('input[name$="-deleted"]'),
    ].filter((input) => deletedPattern.test(input.name) && !input.value).length;

    const display = blockCount >= this.maxValue ? "none" : "";
    this.element.querySelectorAll(ADD_BUTTON_SELECTOR).forEach((button) => {
      // Only write on change: a style write would retrigger the observer.
      if (button.style.display !== display) button.style.display = display;
    });
  }
}
