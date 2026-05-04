const ACTIVE_CLASS = "is-active";

/**
 * Progressive enhancement for the project page hero gallery.
 *
 * Desktop users can hover or click the thumbnail rail to swap the featured
 * image. Mobile users get native horizontal scrolling; the active state follows
 * the slide nearest the viewport edge.
 */
class ProjectHeroCarousel {
  /**
   * @param {HTMLElement} root - The project hero carousel root element.
   */
  constructor(root) {
    this.root = root;
    this.viewport = root.querySelector("[data-project-hero-viewport]");
    this.slides = Array.from(root.querySelectorAll("[data-project-hero-slide]"));
    this.thumbnails = Array.from(
      root.querySelectorAll("[data-project-hero-thumbnail]"),
    );

    if (!this.viewport || this.slides.length < 2 || this.thumbnails.length < 2) {
      return;
    }

    this.activeIndex = 0;
    this.scrollTimeout = null;
    this.bindEvents();
  }

  /**
   * Attaches thumbnail and scroll listeners for the enhanced gallery states.
   */
  bindEvents() {
    this.thumbnails.forEach((thumbnail) => {
      thumbnail.addEventListener("click", () => {
        this.setActiveSlide(thumbnail.dataset.index, true);
      });

      thumbnail.addEventListener("mouseenter", () => {
        this.setActiveSlide(thumbnail.dataset.index, false);
      });
    });

    this.viewport.addEventListener(
      "scroll",
      () => {
        clearTimeout(this.scrollTimeout);
        this.scrollTimeout = setTimeout(() => this.syncActiveSlideToScroll(), 80);
      },
      { passive: true },
    );
  }

  /**
   * Updates the active slide and thumbnail state.
   *
   * @param {string|number} index - The slide index to activate.
   * @param {boolean} shouldScroll - Whether to scroll the slide into view.
   */
  setActiveSlide(index, shouldScroll) {
    const nextIndex = Number(index);

    if (Number.isNaN(nextIndex)) return;

    this.activeIndex = nextIndex;

    this.slides.forEach((slide) => {
      const isActive = Number(slide.dataset.index) === nextIndex;
      slide.classList.toggle(ACTIVE_CLASS, isActive);
      slide.setAttribute("aria-hidden", isActive ? "false" : "true");

      if (
        isActive &&
        shouldScroll &&
        this.viewport.scrollWidth > this.viewport.clientWidth
      ) {
        slide.scrollIntoView({
          behavior: "smooth",
          block: "nearest",
          inline: "start",
        });
      }
    });

    this.thumbnails.forEach((thumbnail) => {
      const isActive = Number(thumbnail.dataset.index) === nextIndex;
      thumbnail.classList.toggle(ACTIVE_CLASS, isActive);
      thumbnail.setAttribute("aria-current", isActive ? "true" : "false");
    });
  }

  /**
   * Syncs the active state to the slide nearest the horizontal viewport edge.
   */
  syncActiveSlideToScroll() {
    const viewportLeft = this.viewport.getBoundingClientRect().left;
    let closestSlide = this.slides[0];
    let closestDistance = Number.POSITIVE_INFINITY;

    this.slides.forEach((slide) => {
      const distance = Math.abs(
        slide.getBoundingClientRect().left - viewportLeft,
      );

      if (distance < closestDistance) {
        closestDistance = distance;
        closestSlide = slide;
      }
    });

    if (closestSlide && Number(closestSlide.dataset.index) !== this.activeIndex) {
      this.setActiveSlide(closestSlide.dataset.index, false);
    }
  }
}

/**
 * Initializes all project page hero carousels on the current page.
 */
function initProjectHeroCarousels() {
  document
    .querySelectorAll("[data-project-hero-carousel]")
    .forEach((carousel) => new ProjectHeroCarousel(carousel));
}

initProjectHeroCarousels();
