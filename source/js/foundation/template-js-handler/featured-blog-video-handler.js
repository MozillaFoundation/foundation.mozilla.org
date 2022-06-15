/**
 * Adding play/pause functionality to the blog index pages optional featured video post.
 */

export default function blogIndexFeaturedVideoHandler() {
  const featuredVideoPostContainer = document.querySelector("#featured-video");
  console.log(featuredVideoPostContainer);

  if (!featuredVideoPostContainer) {
    return;
  }

  const video = featuredVideoPostContainer.querySelector("video.hero-video");
  const playButton = featuredVideoPostContainer.querySelector(".play-button");

  function toggleVideo() {
    video.paused
      ? video.play() & playButton.classList.add("tw-hidden")
      : video.pause() & playButton.classList.remove("tw-hidden");
  }

  if (video && playButton) {
    featuredVideoPostContainer.addEventListener(`click`, () => {
      toggleVideo();
    });
  }
}
