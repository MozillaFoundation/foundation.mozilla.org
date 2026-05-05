import { SWIPE_THRESHOLD } from "./util/carousel.js";

const SWIPE_TRANSITION_DURATION = 300;
const SWIPE_PREVENTION_THRESHOLD = 10;

const SELECTORS = {
  root: "[data-project-block]",
  viewport: "[data-project-block-viewport]",
  track: "[data-project-block-track]",
  slide: "[data-project-block-slide]",
  video: "[data-project-block-video]",
  prev: "[data-project-block-prev]",
  next: "[data-project-block-next]",
  pause: "[data-project-block-pause]",
  pauseLabel: "[data-project-block-pause-label]",
  pagination: "[data-project-block-pagination]",
};

const CLASSES = {
  active: "is-active",
  hidden: "is-hidden",
  paused: "is-paused",
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
    this.pagination = root.querySelector(SELECTORS.pagination);
    this.pauseText = this.pauseButton?.dataset.pauseLabel || "Pause video";
    this.playText = this.pauseButton?.dataset.playLabel || "Play video";
    this.index = 0;
    this.startX = 0;
    this.currentX = 0;
    this.swipeStartTransform = 0;
    this.isDragging = false;
  }

  /**
   * Initializes controls, pagination, and the active slide video state.
   */
  init() {
    if (!this.slides.length || !this.viewport || !this.track) return;

    this.buildPagination();
    this.bindEvents();
    this.root.setAttribute("tabindex", "0");
    this.update();
  }

  /**
   * Creates one pagination marker per media item.
   */
  buildPagination() {
    if (!this.pagination || this.slides.length <= 1) return;

    this.pagination.innerHTML = "";

    this.slides.forEach(() => {
      const dot = document.createElement("span");
      dot.className = "project-block__pagination-dot";
      this.pagination.appendChild(dot);
    });

    this.dots = Array.from(this.pagination.children);
  }

  /**
   * Attaches finite carousel and video control handlers.
   */
  bindEvents() {
    this.prevButton?.addEventListener("click", () => this.goTo(this.index - 1));
    this.nextButton?.addEventListener("click", () => this.goTo(this.index + 1));
    this.pauseButton?.addEventListener("click", () => this.toggleVideo());

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

    this.root.addEventListener("keydown", (event) => {
      if (event.key === "ArrowLeft") this.goTo(this.index - 1);
      if (event.key === "ArrowRight") this.goTo(this.index + 1);
    });
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

    this.clearTrackTransitionAfterSettle();
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
   * Moves to a slide by index, clamped to the available media range.
   *
   * @param {number} index - Requested slide index.
   */
  goTo(index) {
    const nextIndex = Math.min(Math.max(index, 0), this.slides.length - 1);

    if (nextIndex === this.index) return false;

    this.pauseCurrentVideo();
    this.index = nextIndex;
    this.update();
    return true;
  }

  /**
   * Updates active slide, finite navigation visibility, dots, and video controls.
   */
  update() {
    this.slides.forEach((slide, index) => {
      const isActive = index === this.index;

      slide.classList.toggle(CLASSES.active, isActive);
      slide.setAttribute("aria-hidden", String(!isActive));
    });

    this.updateTrackPosition();

    this.dots?.forEach((dot, index) => {
      dot.classList.toggle(CLASSES.active, index === this.index);
    });

    this.prevButton?.classList.toggle(CLASSES.hidden, this.index === 0);
    this.nextButton?.classList.toggle(
      CLASSES.hidden,
      this.index === this.slides.length - 1,
    );

    this.pagination?.classList.toggle(CLASSES.hidden, this.slides.length <= 1);

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
      return -this.index * this.viewport.clientWidth;
    }

    return new DOMMatrix(currentTransform).m41;
  }

  /**
   * Sets the track position for the current finite slide index.
   */
  updateTrackPosition() {
    this.track.style.transform = `translateX(-${this.index * 100}%)`;
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
   */
  clearTrackTransitionAfterSettle() {
    window.setTimeout(() => {
      this.track.style.transition = "";
    }, SWIPE_TRANSITION_DURATION);
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
