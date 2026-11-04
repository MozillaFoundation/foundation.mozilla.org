// Fields that apply only to some label types; any field not listed always shows.
const FIELD_RULES = {
  tag_color: ({ type }) => type === "tag",
  notification_color: ({ type }) => type === "notification",
  big_label_style: ({ type }) => type === "big_label",
  number: ({ type, style }) => type === "big_label" && style === "number",
  highlight_color: ({ type, style }) =>
    type === "big_label" && style === "highlight",
  heading_level: ({ type }) => type !== "big_label",
  subheading: ({ type }) => type !== "big_label",
  action_type: ({ type }) => type !== "big_label",
  action: ({ type }) => type !== "big_label",
};

/**
 * Shows only the Heading Text Group fields that apply to the selected label type.
 */
export default class extends window.StimulusModule.Controller {
  connect() {
    this.update = this.update.bind(this);
    this.element.addEventListener("change", this.update);
    this.update();
  }

  disconnect() {
    this.element.removeEventListener("change", this.update);
  }

  /**
   * @param {string} fieldName
   * @returns {HTMLSelectElement|null}
   */
  findSelect(fieldName) {
    return this.element.querySelector(`select[name$="-${fieldName}"]`);
  }

  update() {
    const type = this.findSelect("label_type")?.value;
    if (!type) return;

    const state = { type, style: this.findSelect("big_label_style")?.value };

    Object.entries(FIELD_RULES).forEach(([name, isVisible]) => {
      const field = this.element.querySelector(`[data-contentpath="${name}"]`);
      if (field) field.style.display = isVisible(state) ? "" : "none";
    });
  }
}
