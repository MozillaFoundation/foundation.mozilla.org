export default class extends window.StimulusModule.Controller {
  static targets = ["field"];
  static values = { triggerField: String };

  connect() {
    this.setupTriggerField();
    this.updateFieldVisibility();
  }

  setupTriggerField() {
    this.triggerElement = this.element.querySelector(
      `select[name="${this.triggerFieldValue}"], input[name="${this.triggerFieldValue}"]`,
    );
    if (this.triggerElement) {
      this.triggerElement.addEventListener("change", () =>
        this.updateFieldVisibility(),
      );
    }
  }

  updateFieldVisibility() {
    if (!this.triggerElement) return;

    const selectedValue = this.triggerElement.value;

    this.fieldTargets.forEach((field) => {
      const shouldShow = field.dataset.condition === selectedValue;
      field.style.display = shouldShow ? "block" : "none";
      field.classList.toggle("hidden", !shouldShow);
      field
        .querySelectorAll("input, select, textarea")
        .forEach((input) => (input.disabled = !shouldShow));
    });
  }
}
