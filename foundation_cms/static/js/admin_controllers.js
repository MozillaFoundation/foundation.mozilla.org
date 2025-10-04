import MediaController from "./controllers/media_controller.js";

if (window.StimulusModule) {
  window.stimulusApp =
    window.stimulusApp || window.StimulusModule.Application.start();

  const adminControllers = [
    { name: "media", controller: MediaController },
    // Add other admin controllers here
  ];

  adminControllers.forEach(({ name, controller }) => {
    window.stimulusApp.register(name, controller);
  });
}
