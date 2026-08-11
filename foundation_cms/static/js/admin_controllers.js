import CharacterCountdownController from "./controllers/character_countdown_controller.js";
import MediaController from "./controllers/media_controller.js";

if (window.StimulusModule) {
  window.stimulusApp =
    window.stimulusApp || window.StimulusModule.Application.start();

  const adminControllers = [
    {
      name: "character-countdown",
      controller: CharacterCountdownController,
    },
    { name: "media", controller: MediaController },
  ];

  adminControllers.forEach(({ name, controller }) => {
    window.stimulusApp.register(name, controller);
  });

  const mountCharacterCountdown = () => {
    const editForm = document.querySelector("[data-edit-form]");

    if (editForm) {
      const controllers = new Set(
        (editForm.dataset.controller || "").split(/\s+/).filter(Boolean),
      );
      controllers.add("character-countdown");
      editForm.dataset.controller = [...controllers].join(" ");
    }
  };

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", mountCharacterCountdown, {
      once: true,
    });
  } else {
    mountCharacterCountdown();
  }
}
