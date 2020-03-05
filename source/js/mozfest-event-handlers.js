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
      let classToToggle = `d-none`;
      console.log(`showVideoControls`);
      if (!video.paused) {
        playButton.classList.add(classToToggle);
        pauseButton.classList.remove(classToToggle);
      } else {
        pauseButton.classList.add(classToToggle);
        playButton.classList.remove(classToToggle);
      }
    };

    console.log(`video.paused`, video.paused);

    pauseButton.addEventListener(`click`, () => {
      console.log(`pauseButton clicked`);
      video.pause();
      showVideoControls();
    });

    playButton.addEventListener(`click`, () => {
      console.log(`playButton clicked`);
      video.play();
      showVideoControls();
    });

    // We do not to show video controls until video is ready to play.
    // Having the if-else check because <video> could be loaded already before
    // we could attach the "canplay" event handler.
    // See https://stackoverflow.com/a/26034492
    if (video.readyState >= video.HAVE_FUTURE_DATA) {
      showVideoControls();
    } else {
      video.addEventListener(
        `canplay`,
        () => {
          showVideoControls();
        },
        false
      );
    }
  }
};

export default () => {
  bindHomeBannerHandlers();
};
