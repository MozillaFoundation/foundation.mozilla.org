const SELECTORS = {
  root: "[data-project-block]",
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
    this.slides = Array.from(root.querySelectorAll(SELECTORS.slide));
    this.prevButton = root.querySelector(SELECTORS.prev);
    this.nextButton = root.querySelector(SELECTORS.next);
    this.pauseButton = root.querySelector(SELECTORS.pause);
    this.pauseLabel = root.querySelector(SELECTORS.pauseLabel);
    this.pagination = root.querySelector(SELECTORS.pagination);
    this.pauseText = this.pauseButton?.dataset.pauseLabel || "Pause video";
    this.playText = this.pauseButton?.dataset.playLabel || "Play video";
    this.index = 0;
  }

  /**
   * Initializes controls, pagination, and the active slide video state.
   */
  init() {
    if (!this.slides.length) return;

    this.buildPagination();
    this.bindEvents();
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
  }

  /**
   * Moves to a slide by index, clamped to the available media range.
   *
   * @param {number} index - Requested slide index.
   */
  goTo(index) {
    const nextIndex = Math.min(Math.max(index, 0), this.slides.length - 1);

    if (nextIndex === this.index) return;

    this.pauseCurrentVideo();
    this.index = nextIndex;
    this.update();
  }

  /**
   * Updates active slide, finite navigation visibility, dots, and video controls.
   */
  update() {
    this.slides.forEach((slide, index) => {
      slide.classList.toggle(CLASSES.active, index === this.index);
    });

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

    video.play().catch(() => {});
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
