const loopingVideoHandler = () => {
  let loopingVideoBlocks = document.querySelectorAll("#looping-video .banner");

  if (!loopingVideoBlocks) {
    return;
  }

  // Looping through all video blocks and adding handlers/starting video.
  for (const loopingVideo of loopingVideoBlocks) {
    let video = loopingVideo.querySelector("video.banner-video");
    let pauseButton = loopingVideo.querySelector(
      ".btn-video-control.btn-pause"
    );
    let playButton = loopingVideo.querySelector(".btn-video-control.btn-play");

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
  }
};

/**
 * Bind handlers to blog video banner
 */
export default () => {
  loopingVideoHandler();
};
