/**
 * Adding play/pause functionality to the optional Blog Page hero video section.
 */

const blogHeroVideoHandler = () => {
  let blogPageHero = document.querySelector("#page-hero .banner");

  if (!blogPageHero) {
    return;
  }

  let video = blogPageHero.querySelector("video.banner-video");
  let pauseButton = blogPageHero.querySelector(".btn-video-control.btn-pause");
  let playButton = blogPageHero.querySelector(".btn-video-control.btn-play");

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
 * Bind handlers to blog video banner
 */
export default () => {
  blogHeroVideoHandler();
};
