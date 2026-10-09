const MISSION_HEADINGS = {
  imagine: "Imagine",
  "co-create": "Co-create",
  mobilize: "Mobilize",
};

/**
 * Keeps a new Flywheel Banner heading aligned with its selected mission until
 * an editor customizes the heading.
 */
export default class extends window.StimulusModule.Controller {
  connect() {
    this.missionField = this.findField("mission");
    this.headingField = this.findField("heading");

    if (!this.missionField || !this.headingField) {
      return;
    }

    this.previousMissionHeading = this.getMissionHeading();
    this.handleMissionChange = this.handleMissionChange.bind(this);
    this.missionField.addEventListener("change", this.handleMissionChange);
  }

  disconnect() {
    this.missionField?.removeEventListener("change", this.handleMissionChange);
  }

  /**
   * Finds a StreamField child input by its field-name suffix.
   *
   * @param {string} fieldName
   * @returns {HTMLInputElement|HTMLSelectElement|null}
   */
  findField(fieldName) {
    return this.element.querySelector(
      `input[name$="-${fieldName}"], select[name$="-${fieldName}"]`,
    );
  }

  /**
   * @returns {string}
   */
  getMissionHeading() {
    return MISSION_HEADINGS[this.missionField?.value] || "";
  }

  handleMissionChange() {
    const nextMissionHeading = this.getMissionHeading();
    const canUpdateHeading =
      !this.headingField.value ||
      this.headingField.value === this.previousMissionHeading;

    if (canUpdateHeading) {
      this.headingField.value = nextMissionHeading;
      this.headingField.dispatchEvent(new Event("input", { bubbles: true }));
    }

    this.previousMissionHeading = nextMissionHeading;
  }
}
