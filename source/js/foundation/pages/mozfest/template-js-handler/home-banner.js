import { ReactGA } from "../../../../common";

// For the featured banner type on mozefest homepage
const watchFeaturedVideoHandler = () => {
  const watchVideoButton = document.querySelector(
    `#mozfest-home-watch-featured-video-button`
  );
  const externalVideo = document.querySelector(`#mozfest-hero-video iframe`);
  const internalVideo = document.querySelector(`#mozfest-hero-video video`);

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

        // Add Src to video to play it
        externalVideo.setAttribute("src", videoUrl);
        fadeOutOverlay(watchVideoButton);
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

const backgroundHardcodedVideoHandler = () => {
  let homepageBanner = document.querySelector(
    "#view-mozfest-home #hero .banner"
  );

  if (!homepageBanner) {
    return;
  }

  let video = homepageBanner.querySelector("video.banner-video");
  let pauseButton = homepageBanner.querySelector(
    ".btn-video-control.btn-pause"
  );
  let playButton = homepageBanner.querySelector(".btn-video-control.btn-play");

  if (video && pauseButton && playButton) {
    const HIDE = `d-none`;

    const showPauseButton = () => {
      playButton.classList.add(HIDE);
      pauseButton.classList.remove(HIDE);
    };

    const showPlayButton = () => {
      pauseButton.classList.add(HIDE);
      playButton.classList.remove(HIDE);
    };

    pauseButton.addEventListener(`click`, () => {
      video.pause();
    });

    playButton.addEventListener(`click`, () => {
      trackWatchVideoClicks();
      video.play();
    });

    video.addEventListener(`pause`, () => {
      showPlayButton();
    });

    video.addEventListener(`playing`, () => {
      showPauseButton();
    });

    video.play();
  }
};

// Track video watches in google analytics
const trackWatchVideoClicks = () => {
  ReactGA.event({
    category: `CTA`,
    action: `watch video tap`,
    label: `watch video button tap`,
  });
};

const scrollToVideoHandler = () => {
  let element = document.getElementById("mozfest-hero-video");
  let button = document.getElementById("mozfest-hero-video-cta");

  if (element && button) {
    let headerOffset = 90;
    let elementPosition = element.getBoundingClientRect().top;
    let offsetPosition = elementPosition - headerOffset;

    button.addEventListener("click", () => {
      window.scrollTo({
        top: offsetPosition,
        behavior: "smooth",
      });
    });
  }
};

/**
 * Bind handlers to MozFest homepage banner
 */
export default () => {
  watchFeaturedVideoHandler();
  backgroundHardcodedVideoHandler();
  scrollToVideoHandler();
};
