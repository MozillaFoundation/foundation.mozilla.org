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
  GALLERY_HUB_CLASSES,
  GALLERY_HUB_SLIDESHOW_CLASSES,
  GALLERY_HUB_SLIDESHOW_SELECTORS,
  GALLERY_HUB_SELECTORS,
} from "./config";
import { updateIndicators } from "../../blocks/util/carousel";
import { subscribeGalleryHubState } from "./state";

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
    this.activeIndex = 0;
    this.project = root.closest(GALLERY_HUB_SELECTORS.project);
  }

  /**
   * Initialize controls, indicators, and the active slide state.
   */
  init() {
    if (this.slides.length <= 1) {
      this.disableControls();
      return;
    }

    this.bindEvents();
    this.syncSlides();
    this.bindProjectState();
  }

  /**
   * Check whether this slideshow belongs to the active project.
   *
   * @returns {boolean} Whether the parent project is visible.
   */
  isProjectActive() {
    return this.project?.classList.contains(GALLERY_HUB_CLASSES.projectActive);
  }

  /**
   * Keep video playback in sync when vertical project navigation changes.
   */
  bindProjectState() {
    subscribeGalleryHubState(() => {
      this.syncSlides();
    });
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

    this.root.querySelector(".carousel-indicators")?.remove();
  }

  /**
   * Wire arrow controls to slideshow navigation.
   */
  bindEvents() {
    if (this.previous) {
      this.previous.addEventListener("click", (event) => {
        event.preventDefault();
        event.stopPropagation();
        this.goToSlide(this.activeIndex - 1);
      });
    }

    if (this.next) {
      this.next.addEventListener("click", (event) => {
        event.preventDefault();
        event.stopPropagation();
        this.goToSlide(this.activeIndex + 1);
      });
    }
  }

  /**
   * Sync disabled button state and shared carousel indicators.
   */
  syncControls() {
    if (this.previous) {
      this.previous.disabled = this.activeIndex === 0;
    }

    if (this.next) {
      this.next.disabled = this.activeIndex === this.slides.length - 1;
    }

    updateIndicators(this.root, this.activeIndex);
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
      setVideoPlayback(slide, isActive && this.isProjectActive());
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
