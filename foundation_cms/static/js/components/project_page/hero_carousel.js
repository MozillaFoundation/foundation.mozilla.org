import { updateIndicators } from "../../blocks/util/carousel";

const ACTIVE_CLASS = "is-active";
const HIDDEN_CLASS = "is-hidden";
const PAUSED_CLASS = "is-paused";
const MOBILE_VIEWPORT_CLASS = "is-swipe-carousel";
const MOBILE_TRACK_CLASS = "hero-carousel__track";
const MOBILE_TRACK_ANIMATING_CLASS = "is-animating";
const LARGE_VIEWPORT_QUERY = "(min-width: 64em)";
const SWIPE_TRANSITION_MS = 280;

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
 * image. Mobile users get a transform-based swipe carousel with an infinite
 * loop, avoiding native scroll-snap edge cases.
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
    this.largeViewportQuery = window.matchMedia(LARGE_VIEWPORT_QUERY);
    this.mobileTrack = null;
    this.mobileSlides = [];
    this.mobilePosition = 1;
    this.isDragging = false;
    this.dragStartX = 0;
    this.dragStartY = 0;
    this.dragDeltaX = 0;
    this.dragStartTranslate = 0;
    this.transitionFallback = null;

    this.bindEvents();
    this.updateResponsiveMode();
    this.setActiveSlide(this.activeIndex, false);
  }

  /**
   * Attaches thumbnail, breakpoint, and swipe listeners.
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
    this.bindViewportChange();

    this.viewport.addEventListener("pointerdown", (event) =>
      this.handlePointerDown(event),
    );
    this.viewport.addEventListener("pointermove", (event) =>
      this.handlePointerMove(event),
    );
    this.viewport.addEventListener("pointerup", (event) =>
      this.handlePointerUp(event),
    );
    this.viewport.addEventListener("pointercancel", (event) =>
      this.handlePointerUp(event),
    );
    window.addEventListener("resize", () => this.handleResize());
  }

  /**
   * Toggles mobile carousel mode when crossing the desktop breakpoint.
   */
  bindViewportChange() {
    const onViewportChange = () => this.updateResponsiveMode();

    if (this.largeViewportQuery.addEventListener) {
      this.largeViewportQuery.addEventListener("change", onViewportChange);
    } else {
      this.largeViewportQuery.addListener(onViewportChange);
    }
  }

  /**
   * Enables or disables the mobile swipe carousel.
   */
  updateResponsiveMode() {
    if (this.largeViewportQuery.matches || this.slides.length < 2) {
      this.disableMobileCarousel();
      return;
    }

    this.enableMobileCarousel();
  }

  /**
   * Wraps slides in a transform track and adds one clone at each edge.
   */
  enableMobileCarousel() {
    if (this.mobileTrack) {
      this.jumpToMobilePosition(this.activeIndex + 1);
      return;
    }

    const firstClone = this.slides[0].cloneNode(true);
    const lastClone = this.slides[this.slides.length - 1].cloneNode(true);

    this.prepareMobileClone(firstClone);
    this.prepareMobileClone(lastClone);

    this.mobileTrack = document.createElement("div");
    this.mobileTrack.className = MOBILE_TRACK_CLASS;
    this.mobileTrack.append(lastClone, ...this.slides, firstClone);
    this.viewport.appendChild(this.mobileTrack);
    this.viewport.classList.add(MOBILE_VIEWPORT_CLASS);

    this.mobileSlides = Array.from(this.mobileTrack.children);
    this.mobilePosition = this.activeIndex + 1;
    this.mobileTrack.addEventListener("transitionend", (event) =>
      this.handleMobileTransitionEnd(event),
    );
    this.jumpToMobilePosition(this.mobilePosition);
  }

  /**
   * Restores the original desktop DOM structure.
   */
  disableMobileCarousel() {
    if (!this.mobileTrack) return;

    this.slides.forEach((slide) => this.viewport.appendChild(slide));
    this.mobileTrack.remove();
    this.mobileTrack = null;
    this.mobileSlides = [];
    this.mobilePosition = this.activeIndex + 1;
    this.viewport.classList.remove(MOBILE_VIEWPORT_CLASS);
    this.viewport.style.removeProperty("cursor");
    clearTimeout(this.transitionFallback);
  }

  /**
   * Marks a cloned slide as decorative.
   *
   * @param {HTMLElement} clone - Slide clone.
   */
  prepareMobileClone(clone) {
    clone.classList.remove(ACTIVE_CLASS);
    clone.setAttribute("aria-hidden", "true");
    clone.querySelector(SELECTORS.pause)?.remove();
  }

  /**
   * Updates the active slide and thumbnail state.
   *
   * @param {string|number} index - The slide index to activate.
   * @param {boolean} shouldMove - Whether to move the visible carousel.
   */
  setActiveSlide(index, shouldMove) {
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
    });

    this.thumbnails.forEach((thumbnail) => {
      const isActive = Number(thumbnail.dataset.index) === nextIndex;
      thumbnail.classList.toggle(ACTIVE_CLASS, isActive);
      thumbnail.setAttribute("aria-current", isActive ? "true" : "false");
    });
    updateIndicators(this.root, nextIndex);

    if (shouldMove) {
      if (this.mobileTrack) {
        this.goToMobilePosition(nextIndex + 1);
      } else if (this.viewport.scrollWidth > this.viewport.clientWidth) {
        this.slides[nextIndex]?.scrollIntoView({
          behavior: "smooth",
          block: "nearest",
          inline: "start",
        });
      }
    }

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
   * Starts a mobile swipe interaction.
   *
   * @param {PointerEvent} event - Pointer event.
   */
  handlePointerDown(event) {
    if (!this.mobileTrack || !event.isPrimary) return;

    this.isDragging = true;
    this.dragStartX = event.clientX;
    this.dragStartY = event.clientY;
    this.dragDeltaX = 0;
    this.dragStartTranslate = -this.getMobileSlideOffset(this.mobilePosition);
    this.setMobileTrackTransition(false);
    this.viewport.setPointerCapture(event.pointerId);
  }

  /**
   * Moves the mobile track with the pointer.
   *
   * @param {PointerEvent} event - Pointer event.
   */
  handlePointerMove(event) {
    if (!this.isDragging || !this.mobileTrack) return;

    const deltaX = event.clientX - this.dragStartX;
    const deltaY = event.clientY - this.dragStartY;

    if (Math.abs(deltaX) < Math.abs(deltaY)) return;

    event.preventDefault();
    this.dragDeltaX = deltaX;
    this.setMobileTrackTranslate(this.dragStartTranslate + deltaX);
  }

  /**
   * Finishes a mobile swipe interaction.
   *
   * @param {PointerEvent} event - Pointer event.
   */
  handlePointerUp(event) {
    if (!this.isDragging || !this.mobileTrack) return;

    this.isDragging = false;

    if (this.viewport.hasPointerCapture(event.pointerId)) {
      this.viewport.releasePointerCapture(event.pointerId);
    }

    const threshold = Math.min(this.getMobileSlideWidth() * 0.2, 80);
    let nextPosition = this.mobilePosition;

    if (this.dragDeltaX < -threshold) {
      nextPosition += 1;
    } else if (this.dragDeltaX > threshold) {
      nextPosition -= 1;
    }

    this.goToMobilePosition(nextPosition);
  }

  /**
   * Moves to a mobile track position with animation.
   *
   * @param {number} position - Track position, including edge clones.
   */
  goToMobilePosition(position) {
    this.mobilePosition = position;
    this.setMobileTrackTransition(true);
    this.setMobileTrackTranslate(-this.getMobileSlideOffset(position));
    clearTimeout(this.transitionFallback);
    this.transitionFallback = setTimeout(() => {
      this.handleMobileTransitionEnd();
    }, SWIPE_TRANSITION_MS + 80);
  }

  /**
   * Jumps to a mobile track position without animation.
   *
   * @param {number} position - Track position, including edge clones.
   */
  jumpToMobilePosition(position) {
    this.mobilePosition = position;
    this.setMobileTrackTransition(false);
    this.setMobileTrackTranslate(-this.getMobileSlideOffset(position));
  }

  /**
   * Handles edge clones after a swipe animation finishes.
   *
   * @param {TransitionEvent} [event] - Transition event.
   */
  handleMobileTransitionEnd(event) {
    if (event && event.target !== this.mobileTrack) return;

    clearTimeout(this.transitionFallback);

    if (this.mobilePosition === 0) {
      this.jumpToMobilePosition(this.slides.length);
    } else if (this.mobilePosition === this.slides.length + 1) {
      this.jumpToMobilePosition(1);
    }

    this.setActiveSlide(this.getMobileRealIndex(), false);
  }

  /**
   * Keeps the transform aligned after viewport size changes.
   */
  handleResize() {
    this.updateResponsiveMode();

    if (this.mobileTrack) {
      this.jumpToMobilePosition(this.mobilePosition);
    }
  }

  /**
   * Returns the real slide index for the current mobile track position.
   *
   * @returns {number}
   */
  getMobileRealIndex() {
    const slideCount = this.slides.length;

    return (this.mobilePosition - 1 + slideCount) % slideCount;
  }

  /**
   * Returns a mobile slide's offset from the track origin.
   *
   * @param {number} position - Track position.
   * @returns {number}
   */
  getMobileSlideOffset(position) {
    return this.mobileSlides[position]?.offsetLeft || 0;
  }

  /**
   * Returns the visible mobile slide width.
   *
   * @returns {number}
   */
  getMobileSlideWidth() {
    return this.mobileSlides[this.mobilePosition]?.offsetWidth || 1;
  }

  /**
   * Applies or removes the mobile transform transition.
   *
   * @param {boolean} shouldAnimate - Whether to animate transform changes.
   */
  setMobileTrackTransition(shouldAnimate) {
    this.mobileTrack?.classList.toggle(
      MOBILE_TRACK_ANIMATING_CLASS,
      shouldAnimate,
    );
  }

  /**
   * Applies the mobile track transform.
   *
   * @param {number} translateX - Horizontal transform in pixels.
   */
  setMobileTrackTranslate(translateX) {
    if (this.mobileTrack) {
      this.mobileTrack.style.transform = `translate3d(${translateX}px, 0, 0)`;
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
