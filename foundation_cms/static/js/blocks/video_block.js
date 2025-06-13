export function initVideoBlocks() {
  const containers = document.querySelectorAll(".video-block__container");

  containers.forEach(container => {
    const video = container.querySelector(".video-block__video");
    const playButton = container.querySelector(".video-block__play-button");
    const overlay = container.querySelector(".video-block__overlay");

    if (!video || !playButton || !overlay) return;

    function toggleVideo() {
      if (video.paused) {
        video.play();
        playButton.classList.add("is-hidden");
      } else {
        video.pause();
        playButton.classList.remove("is-hidden");
      }
    }

    container.addEventListener("click", () => {
      toggleVideo();
    });

    video.addEventListener("ended", () => {
      playButton.classList.remove("is-hidden");
    });

    video.addEventListener("pause", () => {
      playButton.classList.remove("is-hidden");
    });

    video.addEventListener("play", () => {
      playButton.classList.add("is-hidden");
    });
  });
}
