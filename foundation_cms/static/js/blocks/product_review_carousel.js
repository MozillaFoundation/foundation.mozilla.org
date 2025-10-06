const SELECTORS = {
  root: ".product-review-carousel",
  cardsContainer: ".product-review-carousel__cards-container",
  cardWrapper: ".product-review-carousel__card-wrapper",
  productCard: ".product-review-card",
  pauseButton: ".product-review-carousel__pause-button",
};

const DISABLE_CAROUSEL_MIN_WIDTH = 1024;
const GROUP_SIZE = 3; // Maintain 3-card cadence to match nth-child styling
// Behavioral constants
const PREFILL_MULTIPLIER = 2.5; // how much wider than viewport to prefill
const PREFILL_MAX_LOOPS = 10; // cap prefill iterations
const RECYCLE_SAFETY_MAX = 6; // max groups recycled per frame
const FRACTION_EPSILON = 0.0005; // min delta to update transform

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
    this.pxPerSecond = 20; // scroll speed (px/s)
    this._fractionalRemainder = 0; // subpixel remainder applied via transform
    this.track = null; // inner track translated for fractional movement
    this.originalHTML = null;
    this.originalCount = 0;
    this.groupAdvance = 0; // distance to advance before recycling (gap-aware)
    this.itemsModulo = 0; // number of unique items (for index math/logging)
    this.originalNodes = []; // templates for cloning

    // Bind handlers once
    this.onMouseOver = this.onMouseOver.bind(this);
    this.onMouseOut = this.onMouseOut.bind(this);
    this.onVisibilityChange = this.onVisibilityChange.bind(this);
    this.onResize = this.onResize.bind(this);
    this.onPauseToggle = this.onPauseToggle.bind(this);
    this.updatePaused = this.updatePaused.bind(this);
    this.updateButtonUI = this.updateButtonUI.bind(this);

    this.init();
  }

  init() {
    if (!this.container) return;

    const reduce = window.matchMedia(
      "(prefers-reduced-motion: reduce)",
    ).matches;

    if (reduce) {
      this.destroyed = true;
      if (this.pauseBtn) {
        this.pauseBtn.style.display = "none";
      }
      return;
    }

    // Save pristine markup to restore when disabling
    this.originalHTML = this.container.innerHTML;
    this.originalCount = this.container.children.length;

    // Listeners
    // Pause only when hovering actual cards, not gaps (use delegation)
    this.container.addEventListener("mouseover", this.onMouseOver);
    this.container.addEventListener("mouseout", this.onMouseOut);
    document.addEventListener("visibilitychange", this.onVisibilityChange);
    window.addEventListener("resize", this.onResize, { passive: true });
    if (this.pauseBtn) {
      this.pauseBtn.addEventListener("click", this.onPauseToggle);
    }

    // Initial enable/disable per viewport
    this.toggleForViewport();
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

    // Build an inner track to translate (preserves native scrolling on container)
    const buildTrack = () => {
      const track = document.createElement("div");
      track.className = "product-review-carousel__track";
      track.style.display = "flex";
      track.style.willChange = "transform";
      const cs = window.getComputedStyle(this.container);
      const gapVal = cs.columnGap || cs.gap || "";
      if (gapVal) {
        track.style.columnGap = gapVal;
      }
      while (this.container.firstChild) {
        track.appendChild(this.container.firstChild);
      }
      this.container.appendChild(track);
      this.track = track;
    };
    buildTrack();

    // Ensure we have enough content to overflow for smooth motion
    const ensureOverflow = () => {
      const viewport = this.container.clientWidth || window.innerWidth;
      let safety = 0;
      while (
        this.container.scrollWidth < viewport * PREFILL_MULTIPLIER &&
        safety < PREFILL_MAX_LOOPS
      ) {
        // Append just one group at a time to maintain 3-card cadence
        this.appendCards(GROUP_SIZE);
        safety++;
      }
    };
    ensureOverflow();

    // Ensure children count is a multiple of GROUP_SIZE
    const ensureMultipleOfGroupSize = () => {
      // Invariant: track exists while enabled
      const totalChildren = this.track.children.length;
      const remainder = totalChildren % GROUP_SIZE;
      if (remainder !== 0) {
        const needed = GROUP_SIZE - remainder;
        this.appendCards(needed);
      }
    };
    ensureMultipleOfGroupSize();

    // Compute the distance to recycle using width+gap math first (no layout),
    // fallback to offsetLeft if needed
    this.groupAdvance = this.computeGroupAdvanceStatic(GROUP_SIZE);

    // Start from the beginning
    this.container.scrollLeft = 0;
    this.lastTs = null;
    this._fractionalRemainder = 0;
    this.track.style.transform = "translate3d(0px,0,0)";
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
    this._fractionalRemainder = 0;
    this.track = null;
  }

  // Public API
  toggleForViewport() {
    const shouldEnable = window.innerWidth >= DISABLE_CAROUSEL_MIN_WIDTH;
    if (shouldEnable && !this.enabled) {
      this.enable();
    } else if (!shouldEnable && this.enabled) {
      this.disable();
    }
  }

  onPauseToggle() {
    this.userPaused = !this.userPaused;
    this.updatePaused();
    this.updateButtonUI();
  }

  // State/UI helpers
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

  // Event handlers
  // Delegated hover handling: pause only when pointer is over an actual product card (not whitespace)
  onMouseOver(e) {
    const el = e.target && e.target.closest(SELECTORS.productCard);
    if (!el) return;
    if (!this.hovered) {
      this.hovered = true;
      this.updatePaused();
    }
  }

  onMouseOut(e) {
    const fromCard = e.target && e.target.closest(SELECTORS.productCard);
    if (!fromCard) return;
    const to = e.relatedTarget;
    const stillInCard =
      to && this.container.contains(to) && to.closest(SELECTORS.productCard);
    if (!stillInCard && this.hovered) {
      this.hovered = false;
      this.updatePaused();
    }
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

  // Static measurement (card width and gap assumed fixed)
  computeGroupAdvanceStatic(groupSize) {
    const track = this.track;
    if (!track) return 0;
    const first = track.children && track.children[0];
    if (!first) return 0;
    const styles = window.getComputedStyle(track);
    const gap = parseFloat(styles.columnGap || styles.gap || "0") || 0;
    const cardWidth = first.offsetWidth || 0;
    // Equal-width cards assumed; include internal gaps (groupSize - 1)
    // plus trailing gap to next group (1) => groupSize total gaps
    const total = groupSize * cardWidth + groupSize * gap;
    return total > 0 ? total : 0;
  }

  // DOM helpers
  // Compute next start index using data-index of current last element
  computeNextStartIndex() {
    const len = this.itemsModulo || 0;
    if (len === 0) return 0;
    const children = this.track.children; // Invariant: exists while enabled
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
    const parent = this.track; // Invariant: exists while enabled
    for (let i = 0; i < count; i++) {
      const idx = (start + i) % len;
      const node = this.originalNodes[idx].cloneNode(true);
      node.setAttribute("data-index", String(idx));
      parent.appendChild(node);
      appended.push(idx);
    }
    return appended;
  }

  // Helper used during initial overflow/population
  appendCards(count) {
    const len = this.itemsModulo || 0;
    if (len === 0 || count <= 0) return;
    const start = this.computeNextStartIndex();

    const appended = this.appendCardsFromStart(start, count);
  }

  removeFirstGroup(groupSize) {
    for (let i = 0; i < groupSize; i++) {
      const parent = this.track; // Invariant: exists while enabled
      const first = parent.firstElementChild;
      if (!first) break;
      parent.removeChild(first);
    }
  }

  // Animation loop
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
    // Merge user scroll (integer) with our fractional remainder
    const base = this.container.scrollLeft;
    let next = base + (this._fractionalRemainder || 0) + deltaPx;

    // Recycle groups of 3 gap-aware; use precomputed threshold for fewer layout reads
    let safetyCounter = 0;
    let threshold = this.groupAdvance;
    while (safetyCounter < RECYCLE_SAFETY_MAX) {
      const children = this.track.children; // Invariant: exists while enabled
      if (children.length < GROUP_SIZE + 1) break;
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
    // Split into integer scroll and fractional transform so native scrolling remains intact
    const intPart = Math.floor(next);
    const fracPart = next - intPart;

    // Only update DOM when values actually change
    const prevFrac = this._fractionalRemainder || 0;
    if (Math.abs(fracPart - prevFrac) > FRACTION_EPSILON) {
      this.track.style.transform = `translate3d(${-fracPart}px, 0, 0)`;
    }

    if (this.container.scrollLeft !== intPart) {
      this.container.scrollLeft = intPart;
    }

    this._fractionalRemainder = fracPart;
  }

  cancelTick() {
    if (this.rafId != null) {
      cancelAnimationFrame(this.rafId);
      this.rafId = null;
    }
    this.lastTs = null;
  }
}
