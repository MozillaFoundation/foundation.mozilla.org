/**
 * Initializes spotlight card carousels with rotating slides.
 * Dynamically renders teaser cards based on the active primary slide.
 * Navigation via buttons and keyboard only.
 */

const SELECTORS = {
  container: "[data-carousel]",
  slide: "[data-carousel-slide]",
  teaserRegion: "[data-teasers]",
  next: ".spotlight-set__next",
  prev: ".spotlight-set__prev",
};

export function initSpotlightCardCarousels() {
  const carousels = document.querySelectorAll(SELECTORS.container);
  if (!carousels.length) return;

  carousels.forEach((carousel) => {
    const slides = Array.from(carousel.querySelectorAll(SELECTORS.slide));
    const nextBtn = carousel.querySelector(SELECTORS.next);
    const prevBtn = carousel.querySelector(SELECTORS.prev);

    if (!slides.length || !nextBtn || !prevBtn) return;

    const total = slides.length;
    let currentIndex = slides.findIndex((el) => el.classList.contains("is-active"));
    if (currentIndex === -1) currentIndex = 0;

    // Extract card HTML upfront
    const primaryCards = slides.map(slide =>
      slide.querySelector(".spotlight-card__primary")?.innerHTML || ""
    );

    const getTeaserCard = (cardHTML, positionClass) => {
      const div = document.createElement("div");
      div.className = `cell auto spotlight-card spotlight-card__${positionClass}`;
      div.innerHTML = cardHTML;
      return div;
    };

    const updateSlide = (index) => {
    slides.forEach((slide, i) => {
        slide.classList.toggle("is-active", i === index);
        if (i === index) {
        const teaserRegion = slide.querySelector(SELECTORS.teaserRegion);
        if (teaserRegion) {
            teaserRegion.innerHTML = "";
            const teaserIndex1 = (index + 1) % total;
            const teaserIndex2 = (index + 2) % total;
            teaserRegion.appendChild(getTeaserCard(primaryCards[teaserIndex1], "teaser-top"));
            teaserRegion.appendChild(getTeaserCard(primaryCards[teaserIndex2], "teaser-bottom"));
        }
        }
    });

    // 🆕 Update the counter text
    const counterDisplay = carousel.querySelector(".spotlight-set__counter-display");
    if (counterDisplay) {
        counterDisplay.textContent = `${index + 1} / ${total}`;
    }
    };

    const nextSlide = () => {
        console.log("NEXT");
      currentIndex = (currentIndex + 1) % total;
      updateSlide(currentIndex);
    };

    const prevSlide = () => {
      currentIndex = (currentIndex - 1 + total) % total;
      updateSlide(currentIndex);
    };

    nextBtn.addEventListener("click", nextSlide);
    prevBtn.addEventListener("click", prevSlide);

    carousel.addEventListener("keydown", (e) => {
      if (e.key === "ArrowRight") nextSlide();
      if (e.key === "ArrowLeft") prevSlide();
    });

    // Initial render
    updateSlide(currentIndex);
  });
}
