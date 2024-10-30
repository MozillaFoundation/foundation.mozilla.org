/**
 * Event listeners disable the background color field whenever a background image is set.
 */

document.addEventListener("DOMContentLoaded", () => {
  const backgroundColorField = document.querySelector("#id_background_color");
  const backgroundImageField = document.querySelector("#id_background_image");

  if (!backgroundColorField || !backgroundImageField) {
    return;
  }

  function validateBackgroundImageFieldChosen() {
    if (backgroundImageField.value) {
      backgroundColorField.disabled = true;
    } else {
      backgroundColorField.disabled = false;
    }
  }

  backgroundImageField.addEventListener("change", validateBackgroundImageFieldChosen);
  validateBackgroundImageFieldChosen();
});
