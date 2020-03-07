const bindHomeBannerHandlers = () => {
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

export default () => {
  bindHomeBannerHandlers();
};
