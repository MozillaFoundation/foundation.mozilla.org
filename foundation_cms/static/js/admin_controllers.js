import HeroMediaController from "./controllers/hero_media_controller.js";

if (window.StimulusModule) {
  window.stimulusApp =
    window.stimulusApp || window.StimulusModule.Application.start();

  const adminControllers = [
    { name: "hero-media", controller: HeroMediaController },
    // Add other admin controllers here
  ];

  adminControllers.forEach(({ name, controller }) => {
    window.stimulusApp.register(name, controller);
  });
}
