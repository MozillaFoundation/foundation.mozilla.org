export default class extends window.StimulusModule.Controller {
  static targets = ["field"];
  static values = { triggerField: String };

  connect() {
    this.setupTriggerField();
    this.updateFieldVisibility();
  }

  setupTriggerField() {
    const exactSelector = `select[name="${this.triggerFieldValue}"], input[name="${this.triggerFieldValue}"], textarea[name="${this.triggerFieldValue}"]`;
    const suffixSelector = `select[name$="-${this.triggerFieldValue}"], input[name$="-${this.triggerFieldValue}"], textarea[name$="-${this.triggerFieldValue}"]`;

    // try to find trigger inside this controller first (handles model panels)
    this.triggerElement =
      this.element.querySelector(exactSelector) ||
      this.element.querySelector(suffixSelector);

    // fallback to document (useful in some editor DOM arrangements)
    if (!this.triggerElement && typeof document !== "undefined") {
      this.triggerElement =
        document.querySelector(exactSelector) ||
        document.querySelector(suffixSelector);
    }

    if (this.triggerElement) {
      this.triggerElement.addEventListener("change", () =>
        this.updateFieldVisibility(),
      );
    } else {
      // graceful dynamic fallback: attach a delegated listener to catch when trigger appears/changes
      this.element.addEventListener("change", (e) => {
        const t = e.target;
        if (!t || !t.name) return;
        if (
          t.name === this.triggerFieldValue ||
          t.name.endsWith(`-${this.triggerFieldValue}`)
        ) {
          this.triggerElement = t;
          this.updateFieldVisibility();
          this.triggerElement.addEventListener("change", () =>
            this.updateFieldVisibility(),
          );
        }
      });
    }
  }

  updateFieldVisibility() {
    if (!this.triggerElement) return;

    const selectedValue = this.triggerElement.value;

    this.fieldTargets.forEach((field) => {
      const shouldShow = field.dataset.condition === selectedValue;
      field.style.display = shouldShow ? "block" : "none";
      field.classList.toggle("hidden", !shouldShow);
      // disable form inputs when hidden; if an alt field doesn't exist nothing happens
      field
        .querySelectorAll("input, select, textarea, button")
        .forEach((input) => (input.disabled = !shouldShow));
    });
  }
}
