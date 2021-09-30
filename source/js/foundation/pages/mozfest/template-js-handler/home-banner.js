import {ReactGA} from "../../../../common";

const watchYoutubeVideoHandler = () => {
  const watchVideoButton = document.querySelector(
      `#mozfest-home-watch-video-button`
  );
  const video = document.querySelector('#mozfest-hero-video-iframe');

  if (watchVideoButton) {
    watchVideoButton.addEventListener(`click`, () => {
      // trackWatchVideoClicks()

      const videoUrl = watchVideoButton.dataset.videoUrl;

      if (videoUrl) {
        // Add Src to video to play it
        video.setAttribute('src', videoUrl)

        watchVideoButton.classList.add('tw-opacity-0');

        // After fading out remove from DOM Flow
        setTimeout(() => {
          watchVideoButton.classList.add('tw-hidden')
        }, 500)
      }

    });
  }
};

// Track video watches in google analytics
// const trackWatchVideoClicks = () => {
//   ReactGA.event({
//     category: `CTA`,
//     action: `watch video tap`,
//     label: `watch video button tap`,
//   });
// }


/**
 * Bind handlers to MozFest homepage banner
 */
export default () => {
  watchYoutubeVideoHandler();
};
