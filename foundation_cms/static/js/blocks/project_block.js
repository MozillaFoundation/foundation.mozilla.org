import { SWIPE_THRESHOLD, updateIndicators } from "./util/carousel.js";

const SWIPE_TRANSITION_DURATION = 300;
const SWIPE_PREVENTION_THRESHOLD = 10;

const SELECTORS = {
  root: "[data-project-block]",
  viewport: "[data-project-block-viewport]",
  track: "[data-project-block-track]",
  slide: "[data-project-block-slide]",
  video: "[data-project-block-video]",
  prev: ".pagination-controls [data-direction='prev']",
  next: ".pagination-controls [data-direction='next']",
  pause: "[data-project-block-pause]",
  pauseLabel: "[data-project-block-pause-label]",
  activeIndex: "[data-active-index]",
};

const CLASSES = {
  active: "is-active",
  hidden: "is-hidden",
  paused: "is-paused",
};

const DATA_ATTRIBUTES = {
  clone: "data-project-block-clone",
  slideIndex: "data-project-block-slide-index",
};

export function initProjectBlocks() {
  document
    .querySelectorAll(SELECTORS.root)
    .forEach((block) => new ProjectBlock(block).init());
}

class ProjectBlock {
  /**
   * @param {Element} root - The project block root element.
   */
  constructor(root) {
    this.root = root;
    this.viewport = root.querySelector(SELECTORS.viewport);
    this.track = root.querySelector(SELECTORS.track);
    this.slides = Array.from(root.querySelectorAll(SELECTORS.slide));
    this.prevButton = root.querySelector(SELECTORS.prev);
    this.nextButton = root.querySelector(SELECTORS.next);
    this.pauseButton = root.querySelector(SELECTORS.pause);
    this.pauseLabel = root.querySelector(SELECTORS.pauseLabel);
    this.activeIndexLabel = root.querySelector(SELECTORS.activeIndex);
    this.pauseText = this.pauseButton?.dataset.pauseLabel || "Pause video";
    this.playText = this.pauseButton?.dataset.playLabel || "Play video";
    this.index = 0;
    this.startX = 0;
    this.currentX = 0;
    this.swipeStartTransform = 0;
    this.isDragging = false;
    this.isCarousel = this.slides.length > 1;
    this.trackIndex = this.slides.length > 1 ? 1 : 0;
  }

  /**
   * Initializes controls, pagination, and the active slide video state.
   */
  init() {
    if (!this.slides.length || !this.viewport || !this.track) return;

    this.setupSlides();
    this.bindEvents();
    this.setTrackTransition(false);
    this.update();
    this.clearTrackTransitionAfterSettle();
  }

  /**
   * Sets slide indexes and adds clone slides only when multiple media items exist.
   */
  setupSlides() {
    this.slides.forEach((slide, index) => {
      slide.dataset.projectBlockSlideIndex = String(index);
    });

    if (!this.isCarousel) {
      this.trackSlides = [...this.slides];
      return;
    }

    const firstClone = this.slides[0].cloneNode(true);
    const lastClone = this.slides[this.slides.length - 1].cloneNode(true);

    firstClone.setAttribute(DATA_ATTRIBUTES.clone, "true");
    firstClone.dataset.projectBlockSlideIndex = "0";
    firstClone.setAttribute("aria-hidden", "true");

    lastClone.setAttribute(DATA_ATTRIBUTES.clone, "true");
    lastClone.dataset.projectBlockSlideIndex = String(this.slides.length - 1);
    lastClone.setAttribute("aria-hidden", "true");

    this.track.prepend(lastClone);
    this.track.append(firstClone);
    this.trackSlides = Array.from(this.track.querySelectorAll(SELECTORS.slide));
  }

  /**
   * Attaches carousel and video control handlers.
   */
  bindEvents() {
    this.prevButton?.addEventListener("click", () => this.goTo(this.index - 1));
    this.nextButton?.addEventListener("click", () => this.goTo(this.index + 1));
    this.pauseButton?.addEventListener("click", () => this.toggleVideo());

    if (!this.isCarousel) {
      return;
    }

    this.viewport.addEventListener(
      "touchstart",
      (event) => this.handleSwipeStart(event.touches[0].clientX),
      { passive: true },
    );
    this.viewport.addEventListener(
      "touchmove",
      (event) => this.handleSwipeMove(event),
      { passive: false },
    );
    this.viewport.addEventListener(
      "touchend",
      (event) => this.handleSwipeEnd(event.changedTouches[0].clientX),
      { passive: true },
    );

    this.viewport.addEventListener("mousedown", (event) =>
      this.handleSwipeStart(event.clientX),
    );
    this.viewport.addEventListener("mousemove", (event) =>
      this.handleMouseSwipeMove(event),
    );
    this.viewport.addEventListener("mouseup", (event) =>
      this.handleSwipeEnd(event.clientX),
    );
    this.viewport.addEventListener("mouseleave", () => this.cancelSwipe());
  }

  /**
   * Stores the horizontal gesture start position.
   *
   * @param {number} xPosition - The pointer or touch X coordinate.
   */
  handleSwipeStart(xPosition) {
    this.startX = xPosition;
    this.currentX = xPosition;
    this.swipeStartTransform = this.getCurrentTransform();
    this.isDragging = true;
    this.setTrackTransition(false);
  }

  /**
   * Moves the slide track with the active touch gesture.
   *
   * @param {TouchEvent} event - Touch move event.
   */
  handleSwipeMove(event) {
    if (!this.isDragging) return;

    this.currentX = event.touches[0].clientX;
    this.dragTrack(event);
  }

  /**
   * Moves the slide track with a mouse drag gesture.
   *
   * @param {MouseEvent} event - Mouse move event.
   */
  handleMouseSwipeMove(event) {
    if (!this.isDragging) return;

    event.preventDefault();
    this.currentX = event.clientX;
    this.dragTrack(event);
  }

  /**
   * Moves one slide if the horizontal gesture crosses the shared threshold.
   *
   * @param {number} xPosition - The pointer or touch X coordinate.
   */
  handleSwipeEnd(xPosition) {
    if (!this.isDragging) return;

    this.isDragging = false;
    this.currentX = xPosition;
    this.setTrackTransition(true);

    const delta = xPosition - this.startX;
    if (Math.abs(delta) <= SWIPE_THRESHOLD) {
      this.updateTrackPosition();
      this.clearTrackTransitionAfterSettle();
      return;
    }

    const didMove = this.goTo(delta < 0 ? this.index + 1 : this.index - 1);
    if (!didMove) this.updateTrackPosition();

    if (!didMove) this.clearTrackTransitionAfterSettle();
  }

  /**
   * Snaps the track back if a pointer leaves before release.
   */
  cancelSwipe() {
    if (!this.isDragging) return;

    this.isDragging = false;
    this.setTrackTransition(true);
    this.updateTrackPosition();
    this.clearTrackTransitionAfterSettle();
  }

  /**
   * Moves to a slide by index, looping through the available media range.
   *
   * @param {number} index - Requested slide index.
   */
  goTo(index) {
    if (this.slides.length <= 1) return false;

    const nextIndex =
      ((index % this.slides.length) + this.slides.length) % this.slides.length;

    if (nextIndex === this.index && index === this.index) return false;

    this.pauseCurrentVideo();
    this.index = nextIndex;
    this.trackIndex = this.getTrackIndexForRequestedIndex(index, nextIndex);
    this.update();
    this.clearTrackTransitionAfterSettle(true);
    return true;
  }

  /**
   * Maps a requested logical index to its visual track index, including clones.
   *
   * @param {number} requestedIndex - Raw requested slide index.
   * @param {number} logicalIndex - Wrapped slide index.
   * @returns {number} Visual track index.
   */
  getTrackIndexForRequestedIndex(requestedIndex, logicalIndex) {
    if (this.slides.length <= 1) return logicalIndex;
    if (requestedIndex < 0) return 0;
    if (requestedIndex >= this.slides.length) return this.slides.length + 1;
    return logicalIndex + 1;
  }

  /**
   * Updates active slide, carousel navigation visibility, dots, and video controls.
   */
  update() {
    this.trackSlides?.forEach((slide, trackIndex) => {
      const logicalIndex = Number(slide.dataset.projectBlockSlideIndex);
      const isClone = slide.hasAttribute(DATA_ATTRIBUTES.clone);
      const isActive = logicalIndex === this.index;
      const isCurrentTrackSlide = trackIndex === this.trackIndex;

      slide.classList.toggle(CLASSES.active, isActive);
      slide.setAttribute(
        "aria-hidden",
        String(isClone || !isCurrentTrackSlide),
      );

      if (!isCurrentTrackSlide) {
        slide.querySelectorAll(SELECTORS.video).forEach((video) => {
          video.pause();
        });
      }
    });

    this.updateTrackPosition();

    updateIndicators(this.root, this.index);

    const hasMultipleSlides = this.slides.length > 1;
    this.prevButton?.toggleAttribute("disabled", !hasMultipleSlides);
    this.nextButton?.toggleAttribute("disabled", !hasMultipleSlides);

    if (this.activeIndexLabel) {
      this.activeIndexLabel.textContent = String(this.index + 1);
    }

    this.updateVideoControls();
  }

  /**
   * Updates the track transform during an active drag.
   */
  dragTrack(event) {
    const delta = this.currentX - this.startX;
    this.track.style.transform = `translateX(${this.swipeStartTransform + delta}px)`;

    if (Math.abs(delta) > SWIPE_PREVENTION_THRESHOLD) {
      event.preventDefault();
    }
  }

  /**
   * Reads the current translateX value from the track.
   *
   * @returns {number} Current translateX value in pixels.
   */
  getCurrentTransform() {
    const currentTransform = window.getComputedStyle(this.track).transform;

    if (currentTransform === "none") {
      return -this.trackIndex * this.viewport.clientWidth;
    }

    return new DOMMatrix(currentTransform).m41;
  }

  /**
   * Sets the track position for the current visual slide index.
   */
  updateTrackPosition() {
    this.track.style.transform = `translateX(-${this.trackIndex * 100}%)`;
  }

  /**
   * Enables or disables the track transition.
   *
   * @param {boolean} enabled - Whether the transform should animate.
   */
  setTrackTransition(enabled) {
    this.track.style.transition = enabled
      ? `transform ${SWIPE_TRANSITION_DURATION}ms ease-out`
      : "none";
  }

  /**
   * Clears inline transition once the snap animation has finished.
   *
   * @param {boolean} shouldNormalizeLoop - Whether to silently leave clone slides.
   */
  clearTrackTransitionAfterSettle(shouldNormalizeLoop = false) {
    window.setTimeout(() => {
      if (shouldNormalizeLoop) {
        this.normalizeLoopPosition();
        return;
      }

      this.track.style.transition = "";
    }, SWIPE_TRANSITION_DURATION);
  }

  /**
   * Silently moves from a clone slide to the matching real slide.
   */
  normalizeLoopPosition() {
    if (this.slides.length <= 1) return;

    if (this.trackIndex === 0) {
      this.trackIndex = this.slides.length;
    } else if (this.trackIndex === this.slides.length + 1) {
      this.trackIndex = 1;
    } else {
      return;
    }

    this.setTrackTransition(false);
    this.updateTrackPosition();
    this.track.offsetHeight;
    this.trackSlides?.forEach((slide, trackIndex) => {
      if (trackIndex !== this.trackIndex) {
        slide.querySelectorAll(SELECTORS.video).forEach((video) => {
          video.pause();
        });
      }
    });

    requestAnimationFrame(() => {
      this.track.style.transition = "";
    });
  }

  /**
   * Returns the video in the active slide, if that slide has one.
   *
   * @returns {HTMLVideoElement | null}
   */
  getCurrentVideo() {
    return this.slides[this.index]?.querySelector(SELECTORS.video);
  }

  /**
   * Shows pause controls only for video slides and starts muted playback.
   */
  updateVideoControls() {
    const video = this.getCurrentVideo();
    this.pauseButton?.classList.toggle(CLASSES.hidden, !video);

    if (!video) return;

    video.play().catch(() => {
      this.pauseButton?.classList.add(CLASSES.paused);
      if (this.pauseLabel) this.pauseLabel.textContent = this.playText;
    });
    this.pauseButton?.classList.remove(CLASSES.paused);
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
      this.pauseButton?.classList.remove(CLASSES.paused);
      if (this.pauseLabel) this.pauseLabel.textContent = this.pauseText;
    } else {
      video.pause();
      this.pauseButton?.classList.add(CLASSES.paused);
      if (this.pauseLabel) this.pauseLabel.textContent = this.playText;
    }
  }

  /**
   * Pauses the outgoing slide video before changing slides.
   */
  pauseCurrentVideo() {
    this.getCurrentVideo()?.pause();
  }
}
