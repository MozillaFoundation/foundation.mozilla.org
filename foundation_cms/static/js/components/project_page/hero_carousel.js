const ACTIVE_CLASS = "is-active";
const HIDDEN_CLASS = "is-hidden";
const PAUSED_CLASS = "is-paused";

const SELECTORS = {
  frame: ".hero-carousel__frame",
  video: "[data-project-hero-video]",
  pause: "[data-project-hero-pause]",
  pauseLabel: "[data-project-hero-pause-label]",
};

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
    this.slides = Array.from(
      root.querySelectorAll("[data-project-hero-slide]"),
    );
    this.thumbnails = Array.from(
      root.querySelectorAll("[data-project-hero-thumbnail]"),
    );
    this.pauseButton = root.querySelector(SELECTORS.pause);
    this.pauseLabel = root.querySelector(SELECTORS.pauseLabel);
    this.pauseText = this.pauseButton?.dataset.pauseLabel || "Pause video";
    this.playText = this.pauseButton?.dataset.playLabel || "Play video";

    if (!this.viewport || !this.slides.length) {
      return;
    }

    this.activeIndex = 0;
    this.scrollFrame = null;
    this.bindEvents();
    this.setActiveSlide(this.activeIndex, false);
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

    this.pauseButton?.addEventListener("click", () => this.toggleVideo());

    if (this.slides.length > 1) {
      this.viewport.addEventListener(
        "scroll",
        () => {
          if (this.scrollFrame) return;

          this.scrollFrame = requestAnimationFrame(() => {
            this.scrollFrame = null;
            this.syncActiveSlideToScroll();
          });
        },
        { passive: true },
      );
    }
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

      if (!isActive) {
        slide
          .querySelectorAll(SELECTORS.video)
          .forEach((video) => video.pause());
      }

      if (isActive) {
        slide.querySelectorAll(SELECTORS.video).forEach((video) => {
          const playPromise = video.play();

          if (playPromise) {
            playPromise.catch(() => {});
          }
        });
      }

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

    this.updateVideoControls();
  }

  /**
   * Returns the video in the active slide, if that slide has one.
   *
   * @returns {HTMLVideoElement | null}
   */
  getCurrentVideo() {
    return this.slides[this.activeIndex]?.querySelector(SELECTORS.video);
  }

  /**
   * Shows pause controls only for video slides and starts muted playback.
   */
  updateVideoControls() {
    const video = this.getCurrentVideo();
    this.pauseButton?.classList.toggle(HIDDEN_CLASS, !video);

    if (!video) return;

    const frame = video.closest(SELECTORS.frame);

    if (frame && this.pauseButton.parentElement !== frame) {
      frame.appendChild(this.pauseButton);
    }

    video.play().catch(() => {
      this.pauseButton?.classList.add(PAUSED_CLASS);
      if (this.pauseLabel) this.pauseLabel.textContent = this.playText;
    });
    this.pauseButton?.classList.remove(PAUSED_CLASS);
    if (this.pauseLabel) this.pauseLabel.textContent = this.pauseText;
  }

  /**
   * Toggles active video playback from the pause button.
   */
  toggleVideo() {
    const video = this.getCurrentVideo();
    if (!video) return;

    if (video.paused) {
      video.play().catch(() => {});
      this.pauseButton?.classList.remove(PAUSED_CLASS);
      if (this.pauseLabel) this.pauseLabel.textContent = this.pauseText;
    } else {
      video.pause();
      this.pauseButton?.classList.add(PAUSED_CLASS);
      if (this.pauseLabel) this.pauseLabel.textContent = this.playText;
    }
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

    if (
      closestSlide &&
      Number(closestSlide.dataset.index) !== this.activeIndex
    ) {
      this.setActiveSlide(closestSlide.dataset.index, false);
    }
  }
}

/**
 * Initializes all project page hero carousels on the current page.
 */
export function initProjectHeroCarousels() {
  document
    .querySelectorAll("[data-project-hero-carousel]")
    .forEach((carousel) => new ProjectHeroCarousel(carousel));
}
