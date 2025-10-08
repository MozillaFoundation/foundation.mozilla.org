/**
 * Stimulus controller that shows/hides field targets based on the value of a
 * separate trigger input.
 *
 * Usage notes
 * - values.triggerField: the name of the input/select/textarea to watch.
 * - targets.field: elements that will be toggled. Each must include a
 *   data-condition attribute whose value is compared to the trigger value.
 *
 * Event strategy
 * - A single delegated 'change' listener is attached to `this.element`.
 *   When a matching field changes, we record it as `this.triggerElement` and
 *   update visibility. This avoids per-element listeners and prevents leaks
 *   when StreamField re-renders blocks.
 */
export default class extends window.StimulusModule.Controller {
  static targets = ["field"];
  static values = { triggerField: String };

  /**
   * Stimulus lifecycle: runs when the controller is added to the DOM.
   * - Creates stable handler references used for add/removeEventListener.
   * - Locates an initial trigger element if present.
   * - Adds a single delegated change listener to the controller root.
   * - Performs an initial visibility update.
   */
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

  /**
   * Finds and stores a reference to the trigger element by name.
   * Tries both an exact name match and a suffix match (to support dynamic
   * StreamField names like `body-1-...-<name>`). No event listeners are
   * attached here; we only cache the element for later reads.
   */
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

  /**
   * Stimulus lifecycle: runs when the controller is removed from the DOM.
   * Cleans up the single delegated event listener and clears cached references
   * to avoid memory leaks.
   */
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

  /**
   * Shows/hides and enables/disables each field target based on the current
   * trigger value. When the `data-condition` attribute of a field target
   * equals the trigger's value, that target is made visible and enabled; all
   * others are hidden and disabled.
   */
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
