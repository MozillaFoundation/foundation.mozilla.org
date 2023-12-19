/**
 * Mozfest video component. Currently used in mixed_content_block.html
 */

const watchVideoHandler = () => {
  const videoContainers = document.querySelectorAll(`[data-mozfest-video]`);

  if (!videoContainers) {
    return;
  }

  videoContainers.forEach((videoContainer) => {
    const watchVideoButton = videoContainer.querySelector(
      '[data-mozfest-video-button]'
    );

    const externalVideo = videoContainer.querySelector(`iframe`);

    // If no video exists then do nothing
    if (!externalVideo) {
      return;
    }

    if (watchVideoButton) {
      watchVideoButton.addEventListener(`click`, () => {

      // Get video url from button
      const videoUrl = watchVideoButton.dataset.videoUrl;

      // Add Src to video to play it
      externalVideo.setAttribute("src", videoUrl);
      fadeOutOverlay(watchVideoButton);
      });
    }
  });
};

const fadeOutOverlay = (overlay) => {
  // Fade out overlay
  overlay.classList.add("tw-opacity-0");

  // After fading out remove from DOM Flow
  setTimeout(() => {
    overlay.classList.add("tw-hidden");
  }, 500);
};

/**
 * Bind handlers to MozFest video component
 */
export default () => {
  watchVideoHandler();
};
