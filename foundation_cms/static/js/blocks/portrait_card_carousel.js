/**
 * Initializes carousel behavior for the PortraitCardSetBlock.
 * Adds left/right scroll buttons and keyboard navigation.
 */

const SELECTORS = {
  track: "#carousel-track",
  next: "#carousel-next",
  prev: "#carousel-prev",
  card: ".carousel-card",
};

export function initPortraitCardSetCarousel() {
  const track = document.querySelector(SELECTORS.track);
  const prevBtn = document.querySelector(SELECTORS.prev);
  const nextBtn = document.querySelector(SELECTORS.next);

  if (!track || !prevBtn || !nextBtn) return;

  const card = track.querySelector(SELECTORS.card);
  if (!card) return;

  const cardWidth = card.getBoundingClientRect().width;

  const scrollNext = () => {
    track.scrollBy({ left: cardWidth, behavior: "smooth" });
  };

  const scrollPrev = () => {
    track.scrollBy({ left: -cardWidth, behavior: "smooth" });
  };

  nextBtn.addEventListener("click", scrollNext);
  prevBtn.addEventListener("click", scrollPrev);

  track.addEventListener("keydown", (e) => {
    if (e.key === "ArrowRight") {
      scrollNext();
    } else if (e.key === "ArrowLeft") {
      scrollPrev();
    }
  });
}
