import {ReactGA} from "../../../../common";

const watchVideoHandler = () => {
  const watchVideoButton = document.querySelector(
      `#mozfest-home-watch-video-button`
  );
  const externalVideo = document.querySelector("#mozfest-hero-video iframe");
  const internalVideo = document.querySelector("#mozfest-hero-video video");

  // If no video exists then do nothing
  if (!externalVideo && !internalVideo) {
    return;
  }

  if (watchVideoButton) {
    watchVideoButton.addEventListener(`click`, () => {
      trackWatchVideoClicks();

      if (externalVideo) {
        // Get video url from button
        const videoUrl = watchVideoButton.dataset.videoUrl;

        if (videoUrl) {
          // Add Src to video to play it
          externalVideo.setAttribute("src", videoUrl);
          fadeOutOverlay(watchVideoButton);
        }
      }

      if (internalVideo) {
        fadeOutOverlay(watchVideoButton);
        internalVideo.play();
      }

    });
  }
};

const fadeOutOverlay = (overlay) => {
  // Fade out overlay
  overlay.classList.add("tw-opacity-0");

  // After fading out remove from DOM Flow
  setTimeout(() => {
    overlay.classList.add("tw-hidden");
  }, 500);
};

// Track video watches in google analytics
const trackWatchVideoClicks = () => {
  ReactGA.event({
    category: `CTA`,
    action: `watch video tap`,
    label: `watch video button tap`,
  });
}


/**
 * Bind handlers to MozFest homepage banner
 */
export default () => {
  watchVideoHandler();
};
