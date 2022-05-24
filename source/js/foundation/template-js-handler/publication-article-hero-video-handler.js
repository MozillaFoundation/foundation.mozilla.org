/**
 * Adding play/pause functionality to the optional Publication/Article Page hero video section.
 */

export default function publicationArticleHeroVideoHandler() {
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
