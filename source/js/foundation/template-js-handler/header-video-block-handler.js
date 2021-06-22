import { ReactGA } from "../../common";

const watchVideoButtonHandler = () => {
  let homeWatchVideoButton = document.querySelector(
    `#mozfest-home-watch-video-button`
  );

  if (homeWatchVideoButton) {
    homeWatchVideoButton.addEventListener(`click`, () => {
      ReactGA.event({
        category: `CTA`,
        action: `watch video tap`,
        label: `watch video button tap`,
      });
    });
  }
};

const backgroundVideoHandler = () => {
  let homepageBanner = document.querySelector("#video-hero .banner");

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

/**
 * Bind handlers to MozFest homepage banner
 */
export default () => {
  watchVideoButtonHandler();
  backgroundVideoHandler();
};
