const SELECTORS = {
  root: ".product-review-carousel",
  cardsContainer: ".product-review-carousel__cards-container",
  cardWrapper: ".product-review-carousel__card-wrapper",
  pauseButton: ".product-review-carousel__pause-button",
};

const DISABLE_CAROUSEL_MIN_WIDTH = 1024;
const GROUP_SIZE = 3; // Maintain 3-card cadence to match nth-child styling

export function initProductReviewCarousels() {
  const carousels = document.querySelectorAll(SELECTORS.root);
  carousels.forEach((carousel) => new ProductReviewCarousel(carousel));
}

class ProductReviewCarousel {
  constructor(rootEl) {
    this.root = rootEl;
    this.container = this.root.querySelector(SELECTORS.cardsContainer);
    this.pauseBtn = this.root.querySelector(SELECTORS.pauseButton);

    // Runtime state
    this.enabled = false;
    this.destroyed = false;
    this.paused = false; // effective pause state (derived)
    this.userPaused = false; // explicit pause from button
    this.hovered = false; // hover pause state
    this.rafId = null;
    this.lastTs = null;
    this.pxPerSecond = this.readSpeedFromAttr() ?? 60; // scroll speed (px/s)
    this.originalHTML = null;
    this.originalCount = 0;
    this.groupAdvance = 0; // distance to advance before recycling (gap-aware)
    this.itemsModulo = 0; // number of unique items (for index math/logging)
    this.originalNodes = []; // templates for cloning

    // Bind handlers once
    this.onMouseEnter = this.onMouseEnter.bind(this);
    this.onMouseLeave = this.onMouseLeave.bind(this);
    this.onVisibilityChange = this.onVisibilityChange.bind(this);
    this.onResize = this.onResize.bind(this);
    this.onPauseToggle = this.onPauseToggle.bind(this);
    this.updatePaused = this.updatePaused.bind(this);
    this.updateButtonUI = this.updateButtonUI.bind(this);

    this.init();
  }

  init() {
    if (!this.container) return;

    // Save pristine markup to restore when disabling
    this.originalHTML = this.container.innerHTML;
    this.originalCount = this.container.children.length;

    // Listeners
    this.container.addEventListener("mouseenter", this.onMouseEnter);
    this.container.addEventListener("mouseleave", this.onMouseLeave);
    document.addEventListener("visibilitychange", this.onVisibilityChange);
    window.addEventListener("resize", this.onResize, { passive: true });
    if (this.pauseBtn) {
      this.pauseBtn.addEventListener("click", this.onPauseToggle);
    }

    // Initial enable/disable per viewport
    this.toggleForViewport();
  }

  onPauseToggle() {
    this.userPaused = !this.userPaused;
    this.updatePaused();
    this.updateButtonUI();
  }

  updatePaused() {
    const newPaused = this.userPaused || this.hovered || document.hidden;
    if (newPaused !== this.paused) {
      this.paused = newPaused;
      // Reset timer to avoid jumps after pause/unpause
      this.lastTs = null;
      if (!this.paused && this.enabled && this.rafId == null) this.tick();
    }
  }

  updateButtonUI() {
    if (!this.pauseBtn) return;
    const isPaused = this.userPaused;
    this.pauseBtn.setAttribute("aria-pressed", String(isPaused));
    this.pauseBtn.setAttribute(
      "aria-label",
      isPaused ? "Play carousel" : "Pause carousel",
    );
    this.pauseBtn.classList.toggle("is-paused", isPaused);
  }

  readSpeedFromAttr() {
    const v = this.root.getAttribute("data-speed");
    if (!v) return null;
    const n = Number(v);
    return Number.isFinite(n) && n > 0 ? n : null;
  }

  toggleForViewport() {
    const shouldEnable = window.innerWidth >= DISABLE_CAROUSEL_MIN_WIDTH;
    if (shouldEnable && !this.enabled) {
      this.enable();
    } else if (!shouldEnable && this.enabled) {
      this.disable();
    }
  }

  enable() {
    if (this.enabled || this.destroyed) return;
    if (!this.container || this.originalCount === 0) return;

    // Rebuild base from pristine markup (start with the author-provided order)
    const originalNodes = Array.from(
      new DOMParser().parseFromString(
        `<div>${this.originalHTML}</div>`,
        "text/html",
      ).body.firstElementChild.children,
    );
    this.itemsModulo = originalNodes.length;
    this.originalNodes = originalNodes;
    this.container.innerHTML = this.originalHTML;

    // Tag initial children with a stable data-index based on the original order
    Array.from(this.container.children).forEach((el, i) => {
      el.setAttribute("data-index", String(i % originalNodes.length));
    });

    // Persist pristine HTML after indices are added so re-enables keep data-index
    this.originalHTML = this.container.innerHTML;

    // Ensure we have enough content to overflow for smooth motion
    const ensureOverflow = () => {
      const viewport = this.container.clientWidth || window.innerWidth;
      let safety = 0;
      while (this.container.scrollWidth < viewport * 2.5 && safety < 10) {
        // Append just one group at a time to maintain 3-card cadence
        this.appendCards(GROUP_SIZE);
        safety++;
      }
    };
    ensureOverflow();

    // Ensure children count is a multiple of GROUP_SIZE
    const ensureMultipleOfGroupSize = () => {
      const totalChildren = this.container.children.length;
      const remainder = totalChildren % GROUP_SIZE;
      if (remainder !== 0) {
        const needed = GROUP_SIZE - remainder;
        this.appendCards(needed);
      }
    };
    ensureMultipleOfGroupSize();

    // Compute the distance to recycle (gap-aware)
    this.groupAdvance = this.measureGroupAdvance(GROUP_SIZE);
    // Fallback: compute by widths + gaps, including trailing gap to the next group
    if (!this.groupAdvance || !Number.isFinite(this.groupAdvance)) {
      this.groupAdvance = this.measureGroupAdvanceByWidths(GROUP_SIZE);
    }

    // Start from the beginning
    this.container.scrollLeft = 0;
    this.lastTs = null;
    this.enabled = true;
    this.updatePaused();
    this.updateButtonUI();
    this.tick();
  }

  disable() {
    if (!this.enabled) return;
    this.enabled = false;
    this.cancelTick();
    // Restore original markup
    if (this.originalHTML != null) {
      this.container.innerHTML = this.originalHTML;
    }
    this.container.scrollLeft = 0;
  }

  onMouseEnter() {
    this.hovered = true;
    this.updatePaused();
  }

  onMouseLeave() {
    this.hovered = false;
    this.updatePaused();
  }

  onVisibilityChange() {
    this.updatePaused();
  }

  onResize() {
    const shouldEnable = window.innerWidth >= DISABLE_CAROUSEL_MIN_WIDTH;
    if (shouldEnable) {
      if (this.enabled) this.disable();
      this.enable();
    } else if (this.enabled) {
      this.disable();
    }
    this.updatePaused();
    this.updateButtonUI();
  }

  measureGroupAdvance(groupSize) {
    const children = this.container.children;
    if (children.length < groupSize + 1) return 0;
    const first = children[0];
    const nextGroupFirst = children[groupSize];
    return Math.max(0, nextGroupFirst.offsetLeft - first.offsetLeft);
  }

  measureGroupAdvanceByWidths(groupSize) {
    const children = this.container.children;
    if (children.length < groupSize) return 0;
    const styles = window.getComputedStyle(this.container);
    // column-gap holds the horizontal spacing in our flex row
    const gap = parseFloat(styles.columnGap || styles.gap || "0") || 0;
    let widthSum = 0;
    for (let i = 0; i < groupSize; i++) {
      widthSum += children[i].offsetWidth;
    }
    // Include internal gaps (groupSize - 1) and the trailing gap to the next group (1) => groupSize total gaps
    const gaps = gap * groupSize;
    return widthSum + gaps;
  }

  // Compute next start index using data-index of current last element
  computeNextStartIndex() {
    const len = this.itemsModulo || 0;
    if (len === 0) return 0;
    const children = this.container.children;
    const lastChild = children[children.length - 1];
    const lastStr = lastChild ? lastChild.getAttribute("data-index") : null;
    const lastIdx = lastStr != null ? parseInt(lastStr, 10) : -1;
    return Number.isFinite(lastIdx) && lastIdx >= 0 ? (lastIdx + 1) % len : 0;
  }

  // Append a specific count starting from a given index (wrapping modulo unique items)
  appendCardsFromStart(start, count) {
    const len = this.itemsModulo || 0;
    if (len === 0 || count <= 0 || !Array.isArray(this.originalNodes))
      return [];
    const appended = [];
    for (let i = 0; i < count; i++) {
      const idx = (start + i) % len;
      const node = this.originalNodes[idx].cloneNode(true);
      node.setAttribute("data-index", String(idx));
      this.container.appendChild(node);
      appended.push(idx);
    }
    return appended;
  }

  // Public helper used during initial overflow/population
  appendCards(count) {
    const len = this.itemsModulo || 0;
    if (len === 0 || count <= 0) return;
    const start = this.computeNextStartIndex();

    const appended = this.appendCardsFromStart(start, count);
  }

  removeFirstGroup(groupSize) {
    for (let i = 0; i < groupSize; i++) {
      const first = this.container.firstElementChild;
      if (!first) break;
      this.container.removeChild(first);
    }
  }

  tick(ts) {
    if (!this.enabled) return;
    this.rafId = requestAnimationFrame(this.tick.bind(this));
    if (this.paused) return;

    if (this.lastTs == null) {
      this.lastTs = ts ?? performance.now();
      return;
    }

    const nowMs = ts ?? performance.now();
    const elapsedMs = Math.max(0, nowMs - this.lastTs);
    this.lastTs = nowMs;

    const deltaPx = (this.pxPerSecond * elapsedMs) / 1000;
    let next = this.container.scrollLeft + deltaPx;

    // Recycle groups of 3 gap-aware; compute exact threshold from current offsets
    let safetyCounter = 0;
    while (safetyCounter < 6) {
      const children = this.container.children;
      if (children.length < GROUP_SIZE + 1) break;
      const first = children[0];
      const nextGroupFirst = children[GROUP_SIZE];
      const threshold = Math.max(
        0,
        nextGroupFirst.offsetLeft - first.offsetLeft,
      );
      if (!(threshold > 0) || next < threshold) break;

      // Append new group based on index method, then remove first group
      try {
        const start = this.computeNextStartIndex();
        const appended = this.appendCardsFromStart(start, GROUP_SIZE);
      } catch {}

      next -= threshold;
      this.removeFirstGroup(GROUP_SIZE);
      safetyCounter++;
    }

    this.container.scrollLeft = next;
  }

  cancelTick() {
    if (this.rafId != null) {
      cancelAnimationFrame(this.rafId);
      this.rafId = null;
    }
    this.lastTs = null;
  }
}
