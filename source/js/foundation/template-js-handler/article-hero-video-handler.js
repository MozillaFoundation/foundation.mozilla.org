/**
 * Adding play/pause functionality to the optional Article Page hero video section.
 */

export default function articleHeroVideoHandler() {
  const articlePageHero = document.querySelector(".article-hero");

  if (!articlePageHero) {
    return;
  }

  const video = articlePageHero.querySelector("video.hero-video");

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
