import CharacterCountdownController from "./controllers/character_countdown_controller.js";
import ConditionalFieldsController from "./controllers/conditional_fields_controller.js";
import MaxBlocksController from "./controllers/max_blocks_controller.js";

if (window.StimulusModule) {
  window.stimulusApp =
    window.stimulusApp || window.StimulusModule.Application.start();

  const adminControllers = [
    {
      name: "character-countdown",
      controller: CharacterCountdownController,
    },
    { name: "media", controller: ConditionalFieldsController },
    { name: "conditional-fields", controller: ConditionalFieldsController },
    { name: "max-blocks", controller: MaxBlocksController },
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
