/**
 * Base class for sliding carousel components.
 *
 * Implements infinite-loop sliding via a tripled DOM track (prev clones →
 * originals → next clones), with touch/mouse swipe, keyboard navigation, and
 * pagination controls. Disabled above 1024 px unless the root has
 * `is-carousel`. Subclasses can override `getItemSpacing` to customise
 * inter-item spacing measurement.
 */
import {
  SWIPE_THRESHOLD,
  RESIZE_DEBOUNCE_MS,
  getLogicalIndex,
  tripleCards,
  debounce,
} from "./carousel.js";

const DISABLE_CAROUSEL_MIN_WIDTH = 1024;

export class SlidingCarousel {
  /**
   * @param {Element} rootEl - The carousel root element.
   * @param {object} selectors - CSS selectors for internal elements.
   * @param {string} selectors.viewport - Scrollable viewport within the root.
   * @param {string} selectors.track - Sliding track within the viewport.
   * @param {string} selectors.item - Individual slide items within the track.
   */
  constructor(rootEl, { viewport, track, item }) {
    this.root = rootEl;
    this.viewport = this.root.querySelector(viewport);
    this.track = this.viewport.querySelector(track);
    this._itemSelector = item;
    this.originalItems = Array.from(this.track.querySelectorAll(item));
    this.prevBtn = this.root.querySelector(".pagination-controls__prev");
    this.nextBtn = this.root.querySelector(".pagination-controls__next");
    this.counterEl = this.root.querySelector("[data-active-index]");
    this.total = this.originalItems.length;
    this.isCarousel = this.root.classList.contains("is-carousel");

    this.index = this.total;
    this.middleStart = this.total;
    this.middleEnd = this.total * 2;
    this.nextCloneTrackStart = this.middleEnd + 1;
    this.prevCloneTrackEnd = this.middleStart - 1;

    this.slideOffset = 0;
    this.carouselTransition = "";
  }

  init() {
    this.setupTrack();
    this.cacheComputedValues();
    this.setInitialPosition();
    this.bindEvents();
    this.updateCounter();
  }

  /**
   * Replaces track contents with a tripled set of slides to enable infinite looping.
   */
  setupTrack() {
    this.track.innerHTML = "";
    this.track.appendChild(tripleCards(this.originalItems));
    this.items = Array.from(this.track.querySelectorAll(this._itemSelector));
  }

  /**
   * Override in subclass to change how inter-item spacing is measured.
   * Default: reads `columnGap` from the track element.
   */
  getItemSpacing() {
    return parseFloat(window.getComputedStyle(this.track).columnGap) || 0;
  }

  /**
   * Reads and caches the slide width (including gap) and CSS transition value
   * from computed styles. Must be called after the track is in the DOM and laid out.
   */
  cacheComputedValues() {
    const item = this.items[this.index];
    if (item) {
      this.slideOffset =
        item.getBoundingClientRect().width + this.getItemSpacing(item);
    }
    this.carouselTransition = getComputedStyle(this.track)
      .getPropertyValue("--carousel-transition")
      .trim();
  }

  updateTransform(index, animate = true) {
    const offset = this.slideOffset * index;
    this.track.style.transition = animate ? this.carouselTransition : "none";
    this.track.style.transform = `translateX(-${offset}px)`;
  }

  setInitialPosition() {
    requestAnimationFrame(() => {
      this.cacheComputedValues();
      this.updateTransform(this.index, false);
    });
  }

  /**
   * Slides to the given track index. No-ops on wide viewports unless
   * `is-carousel` is set. Delegates loop boundary handling to `handleLoop`.
   *
   * @param {number} newIndex - Absolute track index to slide to.
   */
  slideTo(newIndex) {
    if (!this.isCarousel && window.innerWidth >= DISABLE_CAROUSEL_MIN_WIDTH)
      return;
    if (this.handleLoop(newIndex)) return;

    this.index = newIndex;
    this.updateTransform(this.index, true);
    this.updateCounter();
  }

  /**
   * Detects when the track has reached a clone boundary and performs an
   * invisible jump to the corresponding real slide, then animates one step
   * further to preserve the illusion of infinite scrolling.
   *
   * Uses a double `requestAnimationFrame` to ensure the silent repositioning
   * is painted before the animated step begins.
   *
   * @param {number} newIndex - The index that was requested by `slideTo`.
   * @returns {boolean} `true` if a loop jump was triggered, `false` otherwise.
   */
  handleLoop(newIndex) {
    const loopTransition = (resetIndex, adjustFn) => {
      this.track.style.transition = "none";
      this.index = resetIndex;
      this.updateTransform(this.index, false);

      requestAnimationFrame(() => {
        requestAnimationFrame(() => {
          this.index = adjustFn(this.index);
          this.updateTransform(this.index, true);
          this.updateCounter();
        });
      });
    };

    if (newIndex === this.nextCloneTrackStart) {
      loopTransition(this.middleStart, (i) => i + 1);
      return true;
    }

    if (newIndex === this.prevCloneTrackEnd) {
      loopTransition(this.middleEnd, (i) => i - 1);
      return true;
    }

    return false;
  }

  updateCounter() {
    if (this.counterEl) {
      this.counterEl.textContent = `${this.getLogicalIndex() + 1}`;
    }
  }

  getLogicalIndex() {
    return getLogicalIndex(this.index, this.total);
  }

  handleResize() {
    this.setInitialPosition();
  }

  handleSwipe(delta) {
    if (Math.abs(delta) > SWIPE_THRESHOLD) {
      this.slideTo(delta < 0 ? this.index + 1 : this.index - 1);
    }
  }

  /**
   * Attaches all interaction handlers: pagination button clicks, touch and
   * mouse swipe, arrow-key navigation, and a debounced resize listener.
   */
  bindEvents() {
    this.nextBtn?.addEventListener("click", () => this.slideTo(this.index + 1));
    this.prevBtn?.addEventListener("click", () => this.slideTo(this.index - 1));

    let startX = 0;
    let isDragging = false;

    const onStart = (x) => {
      startX = x;
      isDragging = true;
    };

    const onEnd = (x) => {
      if (!isDragging) return;
      isDragging = false;
      const delta = x - startX;
      this.handleSwipe(delta);
    };

    this.viewport.addEventListener(
      "touchstart",
      (e) => onStart(e.touches[0].clientX),
      { passive: true },
    );
    this.viewport.addEventListener(
      "touchend",
      (e) => onEnd(e.changedTouches[0].clientX),
      { passive: true },
    );

    this.viewport.addEventListener("mousedown", (e) => onStart(e.clientX));
    this.viewport.addEventListener("mouseup", (e) => onEnd(e.clientX));
    this.viewport.addEventListener("mouseleave", () => {
      if (isDragging) isDragging = false;
    });

    this.root.setAttribute("tabindex", "0");
    this.root.addEventListener("keydown", (e) => {
      if (e.key === "ArrowRight") this.slideTo(this.index + 1);
      if (e.key === "ArrowLeft") this.slideTo(this.index - 1);
    });

    window.addEventListener(
      "resize",
      debounce(() => this.handleResize(), RESIZE_DEBOUNCE_MS),
    );
  }
}
