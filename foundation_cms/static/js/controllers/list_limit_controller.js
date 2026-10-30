/**
 * Keeps a StreamField list between its min and max while editing and shows how
 * many items it holds, so editors don't first meet the limit when saving.
 * LimitedListBlock attaches it to the wrapper Wagtail renders around the list.
 */
export default class extends window.StimulusModule.Controller {
  static values = { min: Number, max: Number };

  connect() {
    this.list = this.element.querySelector(
      ":scope > [data-streamfield-list-container]",
    );

    this.counter = document.createElement("p");
    this.counter.className = "help";
    this.counter.setAttribute("aria-live", "polite");
    this.element.before(this.counter);

    // Wagtail inserts a new item as a child of the list, and marks a deleted
    // one aria-hidden as it deletes it. Clicks are not enough: the delete
    // handler runs after a listener on the list.
    this.observer = new MutationObserver(() => this.update());
    this.observer.observe(this.list, {
      childList: true,
      subtree: true,
      attributes: true,
      attributeFilter: ["aria-hidden"],
    });
    this.update();
  }

  disconnect() {
    this.observer.disconnect();
    this.counter.remove();
  }

  update() {
    // Wagtail keeps a deleted item and the add button before it in the DOM,
    // marked aria-hidden, so both are left alone here.
    const items = this.list.querySelectorAll(
      ":scope > [data-streamfield-child]:not([aria-hidden='true'])",
    );
    const isFull = items.length >= this.maxValue;
    const isAtMinimum = items.length <= this.minValue;

    this.counter.textContent = `${items.length} of ${this.maxValue}`;

    this.list
      .querySelectorAll(
        ":scope > [data-streamfield-list-add]:not([aria-hidden='true'])",
      )
      .forEach((button) => {
        button.hidden = isFull;
      });

    items.forEach((item) => {
      item.querySelector("[data-streamfield-action='DUPLICATE']").disabled =
        isFull;
      item.querySelector("[data-streamfield-action='DELETE']").disabled =
        isAtMinimum;
    });
  }
}
