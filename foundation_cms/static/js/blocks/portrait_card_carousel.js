/**
 * Initializes all portrait card carousels on the page.
 *  * Adds left/right scroll buttons and keyboard navigation.
 */
const SELECTORS = {
  container: ".js-portrait-card-carousel",
  track: ".js-carousel-track",
  next: ".js-carousel-next",
  prev: ".js-carousel-prev",
  card: ".carousel-card",
};

export function initPortraitCardSetCarousels() {
  const carousels = document.querySelectorAll(SELECTORS.container);
  if (!carousels.length) return;

  carousels.forEach((carousel) => {
    const track = carousel.querySelector(SELECTORS.track);
    const nextBtn = carousel.querySelector(SELECTORS.next);
    const prevBtn = carousel.querySelector(SELECTORS.prev);
    const card = track?.querySelector(SELECTORS.card);

    if (!track || !card || !nextBtn || !prevBtn) return;

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
      if (e.key === "ArrowRight") scrollNext();
      else if (e.key === "ArrowLeft") scrollPrev();
    });
  });
}
