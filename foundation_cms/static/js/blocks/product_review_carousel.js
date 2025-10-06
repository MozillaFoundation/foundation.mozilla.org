/**
 * ProductReviewCarousel
 * - Autoscrolls a horizontally overflowing track of cards.
 * - Recycles cards in GROUP_SIZE batches to create an infinite loop.
 * - Observes reduced motion, pauses on hover/focus/user toggle, offscreen, and tab hidden.
 * - Uses ResizeObserver + IntersectionObserver and avoids per-frame layout reads.
 */

const SELECTORS = {
  root: ".product-review-carousel",
  cardsContainer: ".product-review-carousel__cards-container",
  cardWrapper: ".product-review-carousel__card-wrapper",
  productCard: ".product-review-card",
  pauseButton: ".product-review-carousel__pause-button",
};

const CLASSNAMES = {
  paused: "is-paused",
  track: "product-review-carousel__track",
};

const DISABLE_CAROUSEL_MIN_WIDTH = 1024;
const GROUP_SIZE = 3; // keep 3-card cadence to match nth-child styling

// Behavior constants
const PREFILL_MULTIPLIER = 2.5; // % of viewport width to prefill
const PREFILL_MAX_LOOPS = 10; // cap on prefill batches
const RECYCLE_SAFETY_MAX = 6; // max groups recycled in a single frame
const FRACTION_EPSILON = 0.0005; // min delta to update fractional transform

export function initProductReviewCarousels() {
  document
    .querySelectorAll(SELECTORS.root)
    .forEach((el) => new ProductReviewCarousel(el));
}

class ProductReviewCarousel {
  constructor(rootEl) {
    this.root = rootEl;
    this.container = this.root.querySelector(SELECTORS.cardsContainer);
    this.pauseBtn = this.root.querySelector(SELECTORS.pauseButton);

    // Runtime state
    this.enabled = false;
    this.destroyed = false;
    this.paused = false;
    this.userPaused = false;
    this.hovered = false;
    this._offscreen = false;

    // Animation state
    this.rafId = null;
    this.lastTs = null;
    this.pxPerSecond = 20;
    this._fractionalRemainder = 0;

    // DOM/structure state
    this.track = null;
    this.originalHTML = null;
    this.originalCount = 0;
    this.originalNodes = [];
    this.itemsModulo = 0;

    // Recycling/metrics
    this.groupAdvance = 0;
    this.gapPx = null; // null = unknown; 0 is valid
    this.cardWidthPx = null; // null = unknown; 0 is valid

    // Layout guards
    this._origPaddingTop = null;
    this._origPaddingBottom = null;

    // Observer helpers
    this.ro = null;
    this.io = null;
    this._resizeScheduled = false;
    this._usingWindowResize = false;

    // Bind handlers once
    this.onMouseOver = this.onMouseOver.bind(this);
    this.onMouseOut = this.onMouseOut.bind(this);
    this.onVisibilityChange = this.onVisibilityChange.bind(this);
    this.onResize = this.onResize.bind(this);
    this.onPauseToggle = this.onPauseToggle.bind(this);
    this.updatePaused = this.updatePaused.bind(this);
    this.updateButtonUI = this.updateButtonUI.bind(this);
    this.boundTick = this.tick.bind(this);

    this.init();
  }

  init() {
    if (!this.container) return;

    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      this.destroyed = true;
      if (this.pauseBtn) this.pauseBtn.style.display = "none";
      return;
    }

    // Snapshot pristine content and index children for stable modulo math
    this.originalCount = this.container.children.length;
    // Assign stable data-index once (0..n-1) so modulo math is deterministic
    Array.from(this.container.children).forEach((el, i) => {
      el.setAttribute("data-index", String(i));
    });
    // Persist modulo and a detached snapshot for cloning later
    this.itemsModulo = this.originalCount;
    this.originalNodes = Array.from(this.container.children).map((el) =>
      el.cloneNode(true),
    );
    // Capture pristine HTML after adding data-index so re-enables keep attributes
    this.originalHTML = this.container.innerHTML;

    // Pointer hover pause (delegated to cards)
    this.container.addEventListener("mouseover", this.onMouseOver, {
      passive: true,
    });
    this.container.addEventListener("mouseout", this.onMouseOut, {
      passive: true,
    });

    // Tab visibility pause
    document.addEventListener("visibilitychange", this.onVisibilityChange);

    // Offscreen pause
    if ("IntersectionObserver" in window) {
      this.io = new IntersectionObserver(
        ([entry]) => {
          this._offscreen = !(
            entry &&
            entry.isIntersecting &&
            entry.intersectionRatio > 0.01
          );
          this.updatePaused();
        },
        { root: null, rootMargin: "50px 0px", threshold: [0, 0.01, 0.1] },
      );
      this.io.observe(this.root);
    }

    // Resize (container-driven) enable/disable + metric recompute
    if ("ResizeObserver" in window) {
      this.ro = new ResizeObserver(() => this.onResizeObserved());
      this.ro.observe(this.root);
    } else {
      window.addEventListener("resize", this.onResize, { passive: true });
      this._usingWindowResize = true;
    }

    // Pause/play button
    this.pauseBtn?.addEventListener("click", this.onPauseToggle);

    // First pass
    this.onResizeObserved();
  }

  enable() {
    if (this.enabled || this.destroyed) return;
    if (!this.container || this.originalCount === 0) return;

    // Restore container from pristine HTML (already includes data-index)
    if (this.originalHTML != null) {
      this.container.innerHTML = this.originalHTML;
    }
    // Ensure snapshot exists (fallback for legacy state)
    if (!this.originalNodes || this.originalNodes.length === 0) {
      const children = Array.from(this.container.children);
      this.itemsModulo = children.length;
      this.originalNodes = children.map((el) => el.cloneNode(true));
    } else {
      this.itemsModulo = this.originalNodes.length;
    }

    // Build inner track (the transform target)
    const cs = window.getComputedStyle(this.container);
    const track = document.createElement("div");
    track.className = CLASSNAMES.track;
    track.style.display = "flex";
    if (cs.columnGap || cs.gap) track.style.columnGap = cs.columnGap || cs.gap;

    // Move vertical padding to track to prevent clipping when transformed
    if (this._origPaddingTop == null)
      this._origPaddingTop = cs.paddingTop || "";
    if (this._origPaddingBottom == null)
      this._origPaddingBottom = cs.paddingBottom || "";
    track.style.paddingTop = cs.paddingTop || "";
    track.style.paddingBottom = cs.paddingBottom || "";
    this.container.style.paddingTop = "0";
    this.container.style.paddingBottom = "0";

    try {
      track.style.contain = "content";
    } catch {}

    while (this.container.firstChild)
      track.appendChild(this.container.firstChild);
    this.container.appendChild(track);
    this.track = track;

    // Compute group advance once and prefill to target width
    this.groupAdvance = this.computeGroupAdvanceStatic(GROUP_SIZE);
    this.ensureOverflow();

    // Ensure children count is a multiple of GROUP_SIZE
    const remainder = this.track.children.length % GROUP_SIZE;
    if (remainder) this.appendCards(GROUP_SIZE - remainder);

    // Reset animation state and start
    this.container.scrollLeft = 0;
    this.lastTs = null;
    this._fractionalRemainder = 0;
    this.track.style.transform = "translate3d(0px,0,0)";
    this.track.style.willChange = "transform";
    this.enabled = true;
    this.updatePaused();
    this.updateButtonUI();
    this.rafId = requestAnimationFrame(this.boundTick);
  }

  disable() {
    if (!this.enabled) return;
    this.enabled = false;
    this.cancelTick();

    if (this.originalHTML != null) this.container.innerHTML = this.originalHTML;
    this.container.scrollLeft = 0;
    this._fractionalRemainder = 0;

    // Restore container paddings
    if (this._origPaddingTop != null)
      this.container.style.paddingTop = this._origPaddingTop;
    if (this._origPaddingBottom != null)
      this.container.style.paddingBottom = this._origPaddingBottom;

    if (this.track) this.track.style.willChange = "auto";
    this.track = null;
  }

  onPauseToggle() {
    this.userPaused = !this.userPaused;
    this.updatePaused();
    this.updateButtonUI();
  }

  updatePaused() {
    const newPaused =
      this.userPaused || this.hovered || document.hidden || this._offscreen;
    if (newPaused === this.paused) return;

    this.paused = newPaused;
    this.lastTs = null;
    if (this.track)
      this.track.style.willChange = this.paused ? "auto" : "transform";

    if (this.paused && this.rafId != null) {
      cancelAnimationFrame(this.rafId);
      this.rafId = null;
    } else if (!this.paused && this.enabled && this.rafId == null) {
      this.rafId = requestAnimationFrame(this.boundTick);
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
    this.pauseBtn.classList.toggle(CLASSNAMES.paused, isPaused);
  }

  // Hover pause only when pointer is on a card (not whitespace)
  onMouseOver(e) {
    if (e.target && e.target.closest(SELECTORS.productCard) && !this.hovered) {
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
    // Fallback path when ResizeObserver isn't available
    this.onResizeObserved();
  }

  /**
   * ResizeObserver callback (debounced to an rAF).
   * - Enables/disables based on container width threshold.
   * - Recomputes cached metrics & overflow when enabled.
   */
  onResizeObserved() {
    if (this._resizeScheduled) return;
    this._resizeScheduled = true;
    requestAnimationFrame(() => {
      this._resizeScheduled = false;

      const shouldEnable = this.root.clientWidth >= DISABLE_CAROUSEL_MIN_WIDTH;
      if (shouldEnable && !this.enabled) this.enable();
      else if (!shouldEnable && this.enabled) this.disable();

      if (this.enabled) {
        // Refresh cached metrics
        const styles = window.getComputedStyle(this.track);
        this.gapPx = parseFloat(styles.columnGap || styles.gap || "0") || 0;
        const first = this.track.children[0];
        this.cardWidthPx = first ? first.offsetWidth || 0 : 0;
        this.groupAdvance = this.computeGroupAdvanceStatic(GROUP_SIZE);

        // Top up if container grew
        const viewport = this.container.clientWidth || window.innerWidth;
        const target = viewport * PREFILL_MULTIPLIER;
        if (this.container.scrollWidth < target) this.ensureOverflow();
      }

      this.updatePaused();
      this.updateButtonUI();
    });
  }

  /**
   * Compute the pixel distance after which we recycle one group.
   * Uses cached width/gap when available to avoid layout reads.
   */
  computeGroupAdvanceStatic(groupSize) {
    if (this.cardWidthPx != null && this.gapPx != null) {
      return groupSize * this.cardWidthPx + groupSize * this.gapPx;
    }
    const track = this.track;
    const first = track.children[0];

    let gap = this.gapPx;
    if (gap == null) {
      const styles = window.getComputedStyle(track);
      gap = parseFloat(styles.columnGap || styles.gap || "0") || 0;
      this.gapPx = gap;
    }

    const cardWidth = this.cardWidthPx ?? (first ? first.offsetWidth || 0 : 0);
    if (this.cardWidthPx == null) this.cardWidthPx = cardWidth;

    const total = groupSize * cardWidth + groupSize * gap; // includes trailing gap
    return total > 0 ? total : 0;
  }

  /**
   * Ensure track width >= PREFILL_MULTIPLIER * viewport by appending
   * whole groups in a single fragment (O(1) math; no loops over layout reads).
   */
  ensureOverflow() {
    const viewport = this.container.clientWidth || window.innerWidth;
    const target = viewport * PREFILL_MULTIPLIER;
    const current = this.container.scrollWidth;
    const adv = Math.max(
      1,
      this.groupAdvance || this.computeGroupAdvanceStatic(GROUP_SIZE),
    );
    const deficit = Math.max(0, target - current);
    const groupsNeeded = Math.min(PREFILL_MAX_LOOPS, Math.ceil(deficit / adv));
    if (groupsNeeded > 0) {
      const totalCards = groupsNeeded * GROUP_SIZE;
      const start = this.computeNextStartIndex();
      this.appendCardsFromStart(start, totalCards);
    }
  }

  // ----- DOM helpers -----

  // Next start index is (data-index of last child + 1) % itemsModulo
  computeNextStartIndex() {
    const len = this.itemsModulo || 0;
    if (!len) return 0;
    const children = this.track.children;
    const last = children[children.length - 1];
    const lastIdx = last ? parseInt(last.getAttribute("data-index"), 10) : -1;
    return Number.isFinite(lastIdx) && lastIdx >= 0 ? (lastIdx + 1) % len : 0;
  }

  appendCardsFromStart(start, count) {
    const len = this.itemsModulo || 0;
    if (!len || count <= 0 || !Array.isArray(this.originalNodes)) return [];
    const frag = document.createDocumentFragment();
    const appended = [];
    for (let i = 0; i < count; i++) {
      const idx = (start + i) % len;
      const node = this.originalNodes[idx].cloneNode(true);
      node.setAttribute("data-index", String(idx));
      frag.appendChild(node);
      appended.push(idx);
    }
    this.track.appendChild(frag);
    return appended;
  }

  appendCards(count) {
    if (!this.itemsModulo || count <= 0) return;
    const start = this.computeNextStartIndex();
    this.appendCardsFromStart(start, count);
  }

  removeFirstGroup(groupSize) {
    for (let i = 0; i < groupSize; i++) {
      const first = this.track.firstElementChild;
      if (!first) break;
      first.remove();
    }
  }

  // ----- Animation loop -----

  tick(ts) {
    if (!this.enabled) return;
    if (this.paused) {
      this.rafId = null;
      return;
    }

    const nowMs = ts ?? performance.now();
    if (this.lastTs == null) this.lastTs = nowMs;

    // Clamp to avoid big jumps after tab throttling
    const elapsedMs = Math.max(0, Math.min(nowMs - this.lastTs, 48));
    this.lastTs = nowMs;

    const deltaPx = (this.pxPerSecond * elapsedMs) / 1000;
    const base = this.container.scrollLeft;
    let next = base + (this._fractionalRemainder || 0) + deltaPx;

    // Recycle forward in GROUP_SIZE batches when crossing the threshold
    let safety = 0;
    const threshold = this.groupAdvance;
    while (safety < RECYCLE_SAFETY_MAX) {
      const children = this.track.children;
      if (children.length < GROUP_SIZE + 1) break;
      if (!(threshold > 0) || next < threshold) break;

      const start = this.computeNextStartIndex();
      this.appendCardsFromStart(start, GROUP_SIZE);
      next -= threshold;
      this.removeFirstGroup(GROUP_SIZE);
      safety++;
    }

    // Split integer/frac so we keep native scrolling for the int part
    const intPart = Math.floor(next);
    const fracPart = next - intPart;

    if (
      Math.abs(fracPart - (this._fractionalRemainder || 0)) > FRACTION_EPSILON
    ) {
      this.track.style.transform = `translate3d(${-fracPart}px, 0, 0)`;
    }
    if (this.container.scrollLeft !== intPart)
      this.container.scrollLeft = intPart;

    this._fractionalRemainder = fracPart;

    // Continue animating while active
    if (!this.paused && this.enabled) {
      this.rafId = requestAnimationFrame(this.boundTick);
    } else {
      this.rafId = null;
    }
  }

  cancelTick() {
    if (this.rafId != null) cancelAnimationFrame(this.rafId);
    this.rafId = null;
    this.lastTs = null;
  }

  /**
   * Cleanup to prevent observer/listener leaks when the carousel node is removed.
   * Currently unused, available for future use.
   */
  destroy() {
    if (this.destroyed) return;
    this.cancelTick();
    try {
      this.io?.disconnect?.();
    } catch {}
    try {
      this.ro?.disconnect?.();
    } catch {}
    document.removeEventListener("visibilitychange", this.onVisibilityChange);
    try {
      this.container?.removeEventListener("mouseover", this.onMouseOver);
      this.container?.removeEventListener("mouseout", this.onMouseOut);
      if (this._usingWindowResize)
        window.removeEventListener("resize", this.onResize);
      this.pauseBtn?.removeEventListener("click", this.onPauseToggle);
    } catch {}
    if (this.enabled) this.disable();
    this.destroyed = true;
  }
}
