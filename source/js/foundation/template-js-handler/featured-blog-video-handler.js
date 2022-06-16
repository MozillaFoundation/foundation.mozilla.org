/**
 * Adding play/pause functionality to the blog index page's optional featured video post.
 */

export default function blogIndexFeaturedVideoHandler() {
  const featuredVideoPostContainer = document.querySelector("#featured-video-container");

  if (!featuredVideoPostContainer) {
    return;
  }

  const video = featuredVideoPostContainer.querySelector("video.featured-video");
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

    video.addEventListener(`ended`, () => {
      playButton.classList.remove("tw-hidden");
    });
  }
}
