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
    let showVideoControls = () => {
      const classToToggle = `d-none`;
      let autoplayStarted =
        video.played.length == 0 && video.readyState >= video.HAVE_FUTURE_DATA;

      if (!video.paused || autoplayStarted) {
        playButton.classList.add(classToToggle);
        pauseButton.classList.remove(classToToggle);
      } else {
        pauseButton.classList.add(classToToggle);
        playButton.classList.remove(classToToggle);
      }
    };

    pauseButton.addEventListener(`click`, () => {
      video.pause();
      showVideoControls();
    });

    playButton.addEventListener(`click`, () => {
      video.play();
      showVideoControls();
    });

    showVideoControls();

    video.addEventListener(
      `canplay`,
      () => {
        showVideoControls();
      },
      false
    );
  }
};

export default () => {
  bindHomeBannerHandlers();
};
