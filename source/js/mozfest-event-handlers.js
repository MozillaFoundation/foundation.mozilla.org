const bindHomeBannerHandlers = () => {
  let homepage = document.querySelector("#view-mozfest-home");

  if (!homepage) {
    return;
  }

  let homeVideoControl = homepage.querySelector(".btn-video-control");
  let homeVideo = homepage.querySelector("video.banner-video");

  if (homeVideoControl && homeVideo) {
    let showVideoControl = () => {
      homeVideoControl.classList.remove(`invisible`);
    };

    homeVideoControl.addEventListener(`click`, () => {
      if (!homeVideo.paused) {
        homeVideo.pause();
        homeVideoControl.innerText = `Resume`;
      } else {
        homeVideo.play();
        homeVideoControl.innerText = `Pause`;
      }
    });

    // <video> could be loaded already before we could attach the "canplay" event handler
    // See https://stackoverflow.com/a/26034492
    if (homeVideo.readyState >= homeVideo.HAVE_FUTURE_DATA) {
      showVideoControl();
    } else {
      homeVideo.addEventListener(
        `canplay`,
        () => {
          showVideoControl();
        },
        false
      );
    }
  }
};

export default () => {
  bindHomeBannerHandlers();
};
