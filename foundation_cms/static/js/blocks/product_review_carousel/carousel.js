import {
  SELECTORS,
  CLASSNAMES,
  DISABLE_CAROUSEL_MIN_WIDTH,
  GROUP_SIZE,
  PREFILL_MULTIPLIER,
  PREFILL_MAX_LOOPS,
  RECYCLE_SAFETY_MAX,
  FRACTION_EPSILON,
  IO_ROOT_MARGIN,
  IO_THRESHOLDS,
  MIN_INTERSECTION_RATIO,
  MAX_FRAME_MS,
  DEFAULT_PX_PER_SECOND,
} from "./config.js";

export default class ProductReviewCarousel {
  /**
   * @param {HTMLElement} rootEl
   */
  constructor(rootEl) {
    this.root = rootEl;
    this.container = this.root.querySelector(SELECTORS.cardsContainer);
    this.pauseBtn = this.root.querySelector(SELECTORS.pauseButton);

    // Runtime flags
    this.enabled = false;
    this.destroyed = false;
    this.paused = false;
    this.userPaused = false;
    this.hovered = false;
    this._offscreen = false;

    // Animation state
    this.rafId = null;
    this.lastTs = null;
    this.pxPerSecond = DEFAULT_PX_PER_SECOND;
    this._fractionalRemainder = 0;

    // DOM/structure
    this.track = null;
    this.originalHTML = null;
    this.originalCount = 0;
    this.originalNodes = [];

    // Recycling/metrics cache
    this.groupAdvance = 0;
    this.gapPx = null; // null = unknown; 0 valid
    this.cardWidthPx = null; // null = unknown; 0 valid

    // Layout guards
    this._origPaddingTop = null;
    this._origPaddingBottom = null;

    // Observers / scheduling
    this.ro = null;
    this.io = null;
    this._resizeScheduled = false;
    this._usingWindowResize = false;

    // Bind once
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

  /**
   * One-time setup:
   * - Abort if prefers-reduced-motion
   * - Snapshot pristine DOM (with stable data-index) for enable/disable cycles
   * - Wire listeners and observers
   */
  init() {
    if (!this.container) return;

    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      this.destroyed = true;
      if (this.pauseBtn) this.pauseBtn.style.display = "none";
      return;
    }

    // Snapshot pristine content and index children for deterministic modulo math
    this.originalCount = this.container.children.length;
    Array.from(this.container.children).forEach((el, i) => {
      el.setAttribute("data-index", String(i));
    });
    this.originalNodes = Array.from(this.container.children).map((el) =>
      el.cloneNode(true),
    );
    this.originalHTML = this.container.innerHTML;

    // Hover pause (delegated to cards)
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
            entry.intersectionRatio > MIN_INTERSECTION_RATIO
          );
          this.updatePaused();
        },
        { root: null, rootMargin: IO_ROOT_MARGIN, threshold: IO_THRESHOLDS },
      );
      this.io.observe(this.root);
    }

    // Responsive enable/disable and metric recompute
    if ("ResizeObserver" in window) {
      this.ro = new ResizeObserver(() => this.onResizeObserved());
      this.ro.observe(this.root);
    } else {
      window.addEventListener("resize", this.onResize, { passive: true });
      this._usingWindowResize = true;
    }

    // Pause/play toggle
    this.pauseBtn?.addEventListener("click", this.onPauseToggle);

    this.onResizeObserved();
  }

  /**
   * Enable: rebuild track, compute metrics, prefill, and start RAF.
   */
  enable() {
    if (this.enabled || this.destroyed) return;
    if (!this.container || this.originalCount === 0) return;

    // Restore pristine children (with data-index)
    if (this.originalHTML != null) {
      this.container.innerHTML = this.originalHTML;
    }

    // Build transform target track
    const cs = window.getComputedStyle(this.container);
    const track = document.createElement("div");
    track.className = CLASSNAMES.track;
    track.style.display = "flex";
    if (cs.columnGap || cs.gap) track.style.columnGap = cs.columnGap || cs.gap;

    // Move vertical padding to the track so transforms won't clip content
    if (this._origPaddingTop == null)
      this._origPaddingTop = cs.paddingTop || "";
    if (this._origPaddingBottom == null)
      this._origPaddingBottom = cs.paddingBottom || "";
    track.style.paddingTop = cs.paddingTop || "";
    track.style.paddingBottom = cs.paddingBottom || "";
    this.container.style.paddingTop = "0";
    this.container.style.paddingBottom = "0";

    track.style.contain = "content";

    while (this.container.firstChild)
      track.appendChild(this.container.firstChild);
    this.container.appendChild(track);
    this.track = track;

    // Distance one group travels before recycling
    this.groupAdvance = this.computeGroupAdvanceStatic(GROUP_SIZE);

    // Prefill to target width (reduces later DOM churn)
    this.ensureOverflow();

    // Keep child count a multiple of GROUP_SIZE to avoid nth-child re-index jumps.
    const remainder = this.track.children.length % GROUP_SIZE;
    if (remainder) this.appendCards(GROUP_SIZE - remainder);

    // Reset animation state
    this.container.scrollLeft = 0;
    this.lastTs = null;
    this._fractionalRemainder = 0;
    this.track.style.transform = "translate3d(0px,0,0)";
    this.track.style.willChange = "transform";

    // Go
    this.enabled = true;
    this.updatePaused();
    this.updateButtonUI();
    this.rafId = requestAnimationFrame(this.boundTick);
  }

  /** Disable and restore pristine DOM. */
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

  /** Toggle user pause via the button. */
  onPauseToggle() {
    this.userPaused = !this.userPaused;
    this.updatePaused();
    this.updateButtonUI();
  }

  /** Derive effective paused state and start/stop RAF accordingly. */
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

  /** Sync button UI (aria-pressed + aria-label) with userPaused. */
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

  /** Pause on mouseover of a card. */
  onMouseOver(e) {
    if (e.target && e.target.closest(SELECTORS.productCard) && !this.hovered) {
      this.hovered = true;
      this.updatePaused();
    }
  }

  /** Resume when pointer leaves cards entirely. */
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
    this.onResizeObserved();
  }

  /** Debounced ResizeObserver handler. */
  onResizeObserved() {
    if (this._resizeScheduled) return;
    this._resizeScheduled = true;
    requestAnimationFrame(() => {
      this._resizeScheduled = false;

      const shouldEnable = this.root.clientWidth >= DISABLE_CAROUSEL_MIN_WIDTH;
      if (shouldEnable && !this.enabled) this.enable();
      else if (!shouldEnable && this.enabled) this.disable();

      if (this.enabled) {
        // Refresh metrics without repeated layout reads
        const styles = window.getComputedStyle(this.track);
        this.gapPx = parseFloat(styles.columnGap || styles.gap || "0") || 0;
        const first = this.track.children[0];
        this.cardWidthPx = first ? first.offsetWidth || 0 : 0;

        // Pixels equal to one recycled group
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

  /** Compute pixel distance equal to one GROUP_SIZE batch (cards + gaps). */
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

  /** Prefill to target width by appending whole groups. */
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

  // ---------- DOM helpers ----------

  computeNextStartIndex() {
    const len = this.originalCount || 0;
    if (!len) return 0;
    const children = this.track.children;
    const last = children[children.length - 1];
    const lastIdx = last ? parseInt(last.getAttribute("data-index"), 10) : -1;
    return Number.isFinite(lastIdx) && lastIdx >= 0 ? (lastIdx + 1) % len : 0;
  }

  appendCardsFromStart(start, count) {
    if (!this.originalCount || count <= 0) return;
    if (!Array.isArray(this.originalNodes)) return;
    const len = this.originalCount;
    const frag = document.createDocumentFragment();
    for (let i = 0; i < count; i++) {
      const idx = (start + i) % len;
      const node = this.originalNodes[idx].cloneNode(true);
      node.setAttribute("data-index", String(idx));
      frag.appendChild(node);
    }
    this.track.appendChild(frag);
  }

  appendCards(count) {
    if (!this.originalCount || count <= 0) return;
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

  // ---------- Animation loop ----------

  tick(ts) {
    if (!this.enabled || !this.track) return;
    if (this.paused) {
      this.rafId = null;
      return;
    }

    const nowMs = ts ?? performance.now();
    if (this.lastTs == null) this.lastTs = nowMs;

    // Clamp to avoid big jumps after tab throttling
    const elapsedMs = Math.max(0, Math.min(nowMs - this.lastTs, MAX_FRAME_MS));
    this.lastTs = nowMs;

    const deltaPx = (this.pxPerSecond * elapsedMs) / 1000;
    const base = this.container.scrollLeft;
    let next = base + (this._fractionalRemainder || 0) + deltaPx;

    // Recycle strictly in GROUP_SIZE batches to preserve nth-child cadence.
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

    // Split integer/frac so native scroll handles the int part
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

  destroy() {
    if (this.destroyed) return;
    this.cancelTick();
    try {
      this.io?.disconnect?.();
      this.ro?.disconnect?.();
      document.removeEventListener("visibilitychange", this.onVisibilityChange);
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
