export default class extends window.StimulusModule.Controller {
  static targets = ["field"];
  static values = { triggerField: String };

  connect() {
    // Create a single bound updater method and reuse it.
    // This prevents creating multiple function instances which would
    // make removing listeners unreliable.
    this._onTriggerChange =
      this._onTriggerChange || this.updateFieldVisibility.bind(this);

    // Delegated change handler attached once to this.element.
    // - We do NOT attach per-trigger listeners. That avoids leaks when
    //   the trigger DOM node is removed/re-rendered (common inside StreamField).
    // - The handler only records the current trigger element and calls the updater.
    // - Because it's created once and stored on `this`, we can cleanly remove it in disconnect().
    this._onDelegatedChange =
      this._onDelegatedChange ||
      ((e) => {
        const t = e.target;
        if (!t || !t.name) return;
        if (
          t.name === this.triggerFieldValue ||
          t.name.endsWith(`-${this.triggerFieldValue}`)
        ) {
          // Keep a reference to the trigger element (no per-element listener added).
          this.triggerElement = t;
          this.updateFieldVisibility();
        }
      });

    // Find and remember an initial trigger element if present (no listener attached to it)
    this.setupTriggerField();

    // Attach one delegated listener to the controller root.
    // This single listener handles all change events for matching trigger inputs
    // within the controller's subtree. Removing it in disconnect() prevents leaks.
    this.element.addEventListener("change", this._onDelegatedChange);

    // Initial visibility pass (may be a no-op if trigger not found yet)
    this.updateFieldVisibility();
  }

  setupTriggerField() {
    // Try to locate trigger by exact name or by suffix (e.g. "body-1-value-media-content").
    // Note: we only store a reference to the found element here — we do NOT attach a listener.
    // Rationale: attaching per-element listeners is fragile with dynamic re-rendering.
    const exactSelector = `select[name="${this.triggerFieldValue}"], input[name="${this.triggerFieldValue}"], textarea[name="${this.triggerFieldValue}"]`;
    const suffixSelector = `select[name$="-${this.triggerFieldValue}"], input[name$="-${this.triggerFieldValue}"], textarea[name$="-${this.triggerFieldValue}"]`;

    let found =
      this.element.querySelector(exactSelector) ||
      this.element.querySelector(suffixSelector);

    if (!found && typeof document !== "undefined") {
      found =
        document.querySelector(exactSelector) ||
        document.querySelector(suffixSelector);
    }

    if (found) {
      // Store reference for updateFieldVisibility; do not add per-element listeners.
      this.triggerElement = found;
    }
  }

  disconnect() {
    // Remove the single delegated listener. This is the only listener we add
    // on connect, so removing it here prevents event-handler leaks when the
    // controller is disconnected (for example, when the block is removed).
    if (this._onDelegatedChange) {
      this.element.removeEventListener("change", this._onDelegatedChange);
    }

    // Clear any stored references so the controller is fully detached.
    this.triggerElement = null;
  }

  updateFieldVisibility() {
    if (!this.triggerElement) return;

    const selectedValue = this.triggerElement.value;

    // Toggle visibility and disabled state for target field containers.
    this.fieldTargets.forEach((field) => {
      const shouldShow = field.dataset.condition === selectedValue;
      field.style.display = shouldShow ? "block" : "none";
      field.classList.toggle("hidden", !shouldShow);
      field
        .querySelectorAll("input, select, textarea, button")
        .forEach((input) => (input.disabled = !shouldShow));
    });
  }
}
