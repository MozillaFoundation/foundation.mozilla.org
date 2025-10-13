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
   * @param {HTMLElement} rootEl Root carousel element.
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
    this.gapPx = null; // null = unknown; 0 is valid
    this.cardWidthPx = null; // null = unknown; 0 is valid

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
   * - Abort if `prefers-reduced-motion`
   * - Snapshot the pre-rendered track and index children (stable modulo order)
   * - Wire listeners/observers and kick the first resize pass
   */
  init() {
    if (!this.container) return;

    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      this.destroyed = true;
      if (this.pauseBtn) this.pauseBtn.style.display = "none";
      return;
    }

    // Use pre-rendered track; take a pristine snapshot and index children
    this.track = this.container.querySelector(`.${CLASSNAMES.track}`);
    if (!this.track) return;

    this.originalCount = this.track.children.length;

    Array.from(this.track.children).forEach((el, i) => {
      el.setAttribute("data-index", String(i));
    });

    this.originalNodes = Array.from(this.track.children).map((el) =>
      el.cloneNode(true),
    );

    this.originalHTML = this.track.innerHTML;

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
   * Enable the carousel: restore pristine children, compute metrics,
   * prefill to reduce future DOM churn, and start the RAF loop.
   */
  enable() {
    if (this.enabled || this.destroyed) return;
    if (!this.container || this.originalCount === 0) return;

    // Restore pristine track children (with data-index)
    if (this.originalHTML != null) {
      this.track.innerHTML = this.originalHTML;
    }

    // Pixels advanced before we recycle one GROUP_SIZE batch
    this.groupAdvance = this.computeGroupAdvanceStatic(GROUP_SIZE);

    // Prefill to target width (reduces later DOM churn)
    this.ensureOverflow();

    // Keep child count a multiple of GROUP_SIZE to avoid nth-child re-index jumps
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

  /**
   * Disable the carousel and restore the pristine DOM state.
   */
  disable() {
    if (!this.enabled) return;

    this.enabled = false;

    this.cancelTick();

    if (this.originalHTML != null) this.track.innerHTML = this.originalHTML;

    this.container.scrollLeft = 0;
    this._fractionalRemainder = 0;

    this.track.style.willChange = "auto";
  }

  /**
   * Button handler: toggle the user-controlled pause state.
   */
  onPauseToggle() {
    this.userPaused = !this.userPaused;

    this.updatePaused();
    this.updateButtonUI();
  }

  /**
   * Recompute the effective paused state (user, hover, hidden tab, offscreen)
   * and start/stop the RAF loop accordingly.
   */
  updatePaused() {
    const newPaused =
      this.userPaused || this.hovered || document.hidden || this._offscreen;

    if (newPaused === this.paused) return;

    this.paused = newPaused;
    this.lastTs = null;

    this.track.style.willChange = this.paused ? "auto" : "transform";

    if (this.paused && this.rafId != null) {
      cancelAnimationFrame(this.rafId);
      this.rafId = null;
    } else if (!this.paused && this.enabled && this.rafId == null) {
      this.rafId = requestAnimationFrame(this.boundTick);
    }
  }

  /**
   * Reflect the pause state in the UI control (pressed state + accessible name).
   */
  updateButtonUI() {
    if (!this.pauseBtn) return;

    const isPaused = this.userPaused;

    this.pauseBtn.setAttribute("aria-pressed", String(isPaused));
    this.pauseBtn.setAttribute(
      "aria-label",
      isPaused ? gettext("Play carousel") : gettext("Pause carousel"),
    );

    this.pauseBtn.classList.toggle(CLASSNAMES.paused, isPaused);
  }

  /**
   * Pause when the pointer is over any card (ignores container whitespace).
   * @param {MouseEvent} e
   */
  onMouseOver(e) {
    if (e.target && e.target.closest(SELECTORS.productCard) && !this.hovered) {
      this.hovered = true;
      this.updatePaused();
    }
  }

  /**
   * Resume when the pointer leaves the cards entirely (not card-to-card moves).
   * @param {MouseEvent} e
   */
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

  /**
   * Document visibility handler (hidden/visible): update pause state.
   */
  onVisibilityChange() {
    this.updatePaused();
  }

  /**
   * Window resize fallback (when `ResizeObserver` is unavailable).
   */
  onResize() {
    this.onResizeObserved();
  }

  /**
   * Debounced `ResizeObserver` callback:
   * - Toggles enabled/disabled based on width threshold
   * - Refreshes cached metrics and tops up overflow when needed
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

  /**
   * Compute the pixel distance equal to one recycled group (cards + gaps).
   * Uses cached widths/gaps when available to avoid layout reads.
   * @param {number} groupSize
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
   * Ensure the total track width is ≥ PREFILL_MULTIPLIER × viewport
   * by appending whole groups in a single fragment.
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

  // ---------- DOM helpers ----------

  /**
   * Compute the next logical start index based on the last child's
   * `data-index`, wrapping modulo the original card count.
   */
  computeNextStartIndex() {
    const len = this.originalCount || 0;
    if (!len) return 0;

    const children = this.track.children;
    const last = children[children.length - 1];

    const lastIdx = last ? parseInt(last.getAttribute("data-index"), 10) : -1;

    return Number.isFinite(lastIdx) && lastIdx >= 0 ? (lastIdx + 1) % len : 0;
  }

  /**
   * Append `count` cards starting from logical index `start`, wrapping modulo
   * the original card set. Preserves `data-index` for stable sequencing.
   * @param {number} start
   * @param {number} count
   */
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

  /**
   * Append `count` cards using `computeNextStartIndex()` for the start.
   * @param {number} count
   */
  appendCards(count) {
    if (!this.originalCount || count <= 0) return;

    const start = this.computeNextStartIndex();

    this.appendCardsFromStart(start, count);
  }

  /**
   * Remove the first `groupSize` cards from the track (recycling step).
   * Always call with GROUP_SIZE (3) to preserve the :nth-child(3n+*) cadence.
   * @param {number} groupSize
   */
  removeFirstGroup(groupSize) {
    for (let i = 0; i < groupSize; i++) {
      const first = this.track.firstElementChild;
      if (!first) break;

      first.remove();
    }
  }

  // ---------- Animation loop ----------

  /**
   * Main RAF loop:
   * - Convert elapsed time to pixel delta (clamped to MAX_FRAME_MS to avoid
   *   a huge “catch-up” jump after background-tab throttling)
   * - When `next` ≥ `groupAdvance`, append the next GROUP_SIZE, subtract the
   *   threshold, and remove the first GROUP_SIZE (preserves nth-child cadence)
   * - Apply integer pixels via `scrollLeft`; apply the remaining fractional
   *   pixel via `translate3d()` to keep motion smooth
   * @param {DOMHighResTimeStamp} [ts]
   */
  tick(ts) {
    if (!this.enabled) return;

    if (this.paused) {
      this.rafId = null;
      return;
    }

    const nowMs = ts ?? performance.now();

    if (this.lastTs == null) this.lastTs = nowMs;

    // Clamp elapsed so background-tab throttling doesn’t cause one giant jump
    // (catch-up is spread over a few frames; caps per-frame DOM work/recycles).
    const elapsedMs = Math.max(0, Math.min(nowMs - this.lastTs, MAX_FRAME_MS));
    this.lastTs = nowMs;

    const deltaPx = (this.pxPerSecond * elapsedMs) / 1000;

    const base = this.container.scrollLeft;
    let next = base + (this._fractionalRemainder || 0) + deltaPx;

    // Recycle strictly in GROUP_SIZE batches to preserve nth-child cadence
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

    if (this.container.scrollLeft !== intPart) {
      this.container.scrollLeft = intPart;
    }

    this._fractionalRemainder = fracPart;

    if (!this.paused && this.enabled) {
      this.rafId = requestAnimationFrame(this.boundTick);
    } else {
      this.rafId = null;
    }
  }

  /**
   * Stop the RAF loop and reset timestamps.
   */
  cancelTick() {
    if (this.rafId != null) cancelAnimationFrame(this.rafId);

    this.rafId = null;
    this.lastTs = null;
  }

  /**
   * Cleanup observers/listeners and restore DOM if still enabled.
   */
  destroy() {
    if (this.destroyed) return;

    this.cancelTick();

    this.io?.disconnect?.();
    this.ro?.disconnect?.();

    document.removeEventListener("visibilitychange", this.onVisibilityChange);

    this.container?.removeEventListener("mouseover", this.onMouseOver);
    this.container?.removeEventListener("mouseout", this.onMouseOut);

    if (this._usingWindowResize) {
      window.removeEventListener("resize", this.onResize);
    }

    this.pauseBtn?.removeEventListener("click", this.onPauseToggle);

    if (this.enabled) this.disable();

    this.destroyed = true;
  }
}
