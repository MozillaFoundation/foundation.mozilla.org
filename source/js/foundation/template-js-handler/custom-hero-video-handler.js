/**
 * Adding play/pause functionality to the optional custom hero video.
 */

export default function customHeroVideoHandler() {
  const customPageHero = document.querySelector("#custom-hero");

  if (!customPageHero) {
    return;
  }

  const video = customPageHero.querySelector("video.hero-video");

  function toggleVideo() {
    video.paused ? video.play() : video.pause();
  }

  if (video) {
    video.addEventListener(`click`, () => {
      toggleVideo();
    });

    video.play();
  }
}
