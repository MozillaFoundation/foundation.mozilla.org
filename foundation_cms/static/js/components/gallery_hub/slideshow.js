/**
 * Project media slideshow controller for Gallery Hub project cards.
 *
 * Slides are stacked so the active media sits on top. Moving forward sends the
 * current slide out to the right; moving backward restores the previous slide
 * over the stack with mirrored motion.
 *
 * @module galleryHubSlideshow
 */

import {
  GALLERY_HUB_SLIDESHOW_CLASSES,
  GALLERY_HUB_SLIDESHOW_SELECTORS,
  GALLERY_HUB_SLIDESHOW_SETTINGS,
} from "./config";

/**
 * Play or pause any videos within a slide based on active state.
 *
 * @param {HTMLElement} slide - Slide element that may contain videos.
 * @param {boolean} shouldPlay - Whether videos in this slide should play.
 */
function setVideoPlayback(slide, shouldPlay) {
  slide.querySelectorAll("video").forEach((video) => {
    if (shouldPlay) {
      video.play().catch(() => {});
      return;
    }

    video.pause();
  });
}

/**
 * Create a slideshow pagination dot.
 *
 * @param {number} index - Slide index represented by the dot.
 * @returns {HTMLButtonElement} Pagination button.
 */
function createDot(index) {
  const dot = document.createElement("button");

  dot.className = GALLERY_HUB_SLIDESHOW_CLASSES.dot;
  dot.type = "button";
  dot.dataset.galleryHubSlideDot = `${index}`;
  dot.setAttribute("aria-label", `View media ${index + 1}`);

  return dot;
}

/**
 * Clamp a slide's visual stack slot around the active media.
 *
 * @param {number} distance - Signed distance from the active slide.
 * @returns {number} Stack position used by CSS.
 */
function getStackPosition(distance) {
  return Math.max(-2, Math.min(distance, 2));
}

/**
 * Manages one project's media slideshow.
 */
class GalleryHubSlideshow {
  /**
   * @param {HTMLElement} root - Slideshow root element.
   */
  constructor(root) {
    this.root = root;
    this.slides = Array.from(
      root.querySelectorAll(GALLERY_HUB_SLIDESHOW_SELECTORS.slide),
    );
    this.previous = root.querySelector(
      GALLERY_HUB_SLIDESHOW_SELECTORS.previous,
    );
    this.next = root.querySelector(GALLERY_HUB_SLIDESHOW_SELECTORS.next);
    this.dotsContainer = root.querySelector(
      GALLERY_HUB_SLIDESHOW_SELECTORS.dots,
    );
    this.dots = [];
    this.activeIndex = 0;
  }

  /**
   * Initialize controls, dots, and the active slide state.
   */
  init() {
    if (this.slides.length <= 1) {
      this.disableControls();
      return;
    }

    this.createDots();
    this.bindEvents();
    this.syncSlides();
  }

  /**
   * Remove navigation affordances when a project has only one media slide.
   */
  disableControls() {
    if (this.previous) {
      this.previous.hidden = true;
      this.previous.disabled = true;
    }

    if (this.next) {
      this.next.hidden = true;
      this.next.disabled = true;
    }

    this.dotsContainer?.remove();
  }

  /**
   * Render the visible dot controls, capped by the configured maximum.
   */
  createDots() {
    Array.from({
      length: Math.min(
        this.slides.length,
        GALLERY_HUB_SLIDESHOW_SETTINGS.maxDots,
      ),
    }).forEach((_, index) => {
      const dot = createDot(index);

      this.dots.push(dot);
      this.dotsContainer.append(dot);
    });
  }

  /**
   * Wire dot and arrow controls to slideshow navigation.
   */
  bindEvents() {
    this.dots.forEach((dot) => {
      dot.addEventListener("click", (event) => {
        event.preventDefault();
        event.stopPropagation();
        this.goToSlide(Number(dot.dataset.galleryHubSlideDot));
      });
    });

    this.previous.addEventListener("click", (event) => {
      event.preventDefault();
      event.stopPropagation();
      this.goToSlide(this.activeIndex - 1);
    });

    this.next.addEventListener("click", (event) => {
      event.preventDefault();
      event.stopPropagation();
      this.goToSlide(this.activeIndex + 1);
    });
  }

  /**
   * Sync disabled button state and dot labels/current state.
   */
  syncControls() {
    this.previous.disabled = this.activeIndex === 0;
    this.next.disabled = this.activeIndex === this.slides.length - 1;

    const dotStart = Math.min(
      Math.max(this.activeIndex - 1, 0),
      Math.max(this.slides.length - this.dots.length, 0),
    );

    this.dots.forEach((dot, index) => {
      const slideIndex = dotStart + index;
      const isActive = slideIndex === this.activeIndex;

      dot.dataset.galleryHubSlideDot = `${slideIndex}`;
      dot.setAttribute("aria-label", `View media ${slideIndex + 1}`);
      dot.setAttribute("aria-current", isActive ? "true" : "false");
    });
  }

  /**
   * Apply active/before/after classes and video playback to all slides.
   */
  syncSlides() {
    this.slides.forEach((slide, index) => {
      const isActive = index === this.activeIndex;
      const stackPosition = getStackPosition(index - this.activeIndex);

      slide.classList.toggle(GALLERY_HUB_SLIDESHOW_CLASSES.active, isActive);
      slide.classList.toggle(
        GALLERY_HUB_SLIDESHOW_CLASSES.beforeActive,
        index < this.activeIndex,
      );
      slide.classList.toggle(
        GALLERY_HUB_SLIDESHOW_CLASSES.afterActive,
        index > this.activeIndex,
      );
      slide.setAttribute("aria-hidden", `${!isActive}`);
      slide.dataset.galleryHubSlideStack = `${stackPosition}`;
      slide.style.zIndex = `${
        this.slides.length - Math.abs(index - this.activeIndex)
      }`;
      setVideoPlayback(slide, isActive);
    });

    this.syncControls();
  }

  /**
   * Move to a specific slide index if it exists.
   *
   * @param {number} index - Target slide index.
   */
  goToSlide(index) {
    if (index === this.activeIndex || index < 0 || index >= this.slides.length)
      return;

    this.activeIndex = index;
    this.syncSlides();
  }
}

/**
 * Initialize all Gallery Hub media slideshows on the page.
 */
export function initGalleryHubSlideshows() {
  document
    .querySelectorAll(GALLERY_HUB_SLIDESHOW_SELECTORS.root)
    .forEach((root) => {
      new GalleryHubSlideshow(root).init();
    });
}
