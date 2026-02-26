import {
  SELECTORS,
  CLASSNAMES,
  DISABLE_CAROUSEL_MIN_WIDTH,
  GROUP_SIZE,
  PREFILL_MULTIPLIER,
  PREFILL_MAX_LOOPS,
  IO_ROOT_MARGIN,
  IO_THRESHOLDS,
  MIN_INTERSECTION_RATIO,
  DEFAULT_PX_PER_SECOND,
} from "./config.js";
import {
  onPauseToggle,
  updatePaused,
  updateButtonUI,
  onMouseOver,
  onMouseOut,
  onVisibilityChange,
  onFocusIn,
  onFocusOut,
  onKeyDown,
} from "./keyboard.js";
import { tick, cancelTick } from "./tick.js";
import {
  refreshVisibleCardFocus,
  resetCardFocusability,
  updateWrapperFocusability,
  isElementHorizontallyVisible,
  makeTemporarilyUntabbable,
  restoreOriginalTabIndex,
} from "./a11y.js";

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
    this.focusWithin = false;
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
    this._lastFocusRefreshTs = null;

    // Bind imported helpers once
    this.onPauseToggle = onPauseToggle.bind(this);
    this.updatePaused = updatePaused.bind(this);
    this.updateButtonUI = updateButtonUI.bind(this);
    this.onMouseOver = onMouseOver.bind(this);
    this.onMouseOut = onMouseOut.bind(this);
    this.onVisibilityChange = onVisibilityChange.bind(this);
    this.onFocusIn = onFocusIn.bind(this);
    this.onFocusOut = onFocusOut.bind(this);
    this.onKeyDown = onKeyDown.bind(this);
    this.tick = tick.bind(this);
    this.cancelTick = cancelTick.bind(this);
    this.refreshVisibleCardFocus = refreshVisibleCardFocus.bind(this);
    this.resetCardFocusability = resetCardFocusability.bind(this);
    this.updateWrapperFocusability = updateWrapperFocusability.bind(this);
    this.isElementHorizontallyVisible = isElementHorizontallyVisible.bind(this);
    this.makeTemporarilyUntabbable = makeTemporarilyUntabbable.bind(this);
    this.restoreOriginalTabIndex = restoreOriginalTabIndex.bind(this);

    // Bind class methods once
    this.onResize = this.onResize.bind(this);
    this.boundTick = this.tick;

    this.init();
  }

  /**
   * One-time setup:
   * - Abort if `prefers-reduced-motion`
   * - Snapshot the pre-rendered track and index children
   * - Wire listeners/observers and kick the first resize pass
   */
  init() {
    if (!this.container) return;

    if (window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      this.destroyed = true;
      if (this.pauseBtn) this.pauseBtn.style.display = "none";
      return;
    }

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

    this.container.addEventListener("mouseover", this.onMouseOver, {
      passive: true,
    });

    this.container.addEventListener("mouseout", this.onMouseOut, {
      passive: true,
    });

    this.root.addEventListener("focusin", this.onFocusIn);
    this.root.addEventListener("focusout", this.onFocusOut);
    this.root.addEventListener("keydown", this.onKeyDown);
    document.addEventListener("visibilitychange", this.onVisibilityChange);

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

    if ("ResizeObserver" in window) {
      this.ro = new ResizeObserver(() => this.onResizeObserved());
      this.ro.observe(this.root);
    } else {
      window.addEventListener("resize", this.onResize, { passive: true });
      this._usingWindowResize = true;
    }

    this.pauseBtn?.addEventListener("click", this.onPauseToggle);

    this.onResizeObserved();
  }

  /**
   * Enable the carousel: restore pristine children, compute metrics, prefill,
   * and start the RAF loop.
   */
  enable() {
    if (this.enabled || this.destroyed) return;
    if (!this.container || this.originalCount === 0) return;

    if (this.originalHTML != null) this.track.innerHTML = this.originalHTML;

    this.groupAdvance = this.computeGroupAdvanceStatic(GROUP_SIZE);
    this.ensureOverflow();

    const remainder = this.track.children.length % GROUP_SIZE;
    if (remainder) this.appendCards(GROUP_SIZE - remainder);

    this.container.scrollLeft = 0;
    this.lastTs = null;
    this._fractionalRemainder = 0;
    this.track.style.transform = "translate3d(0px,0,0)";
    this.track.style.willChange = "transform";

    this.enabled = true;
    if (this.focusWithin) this.refreshVisibleCardFocus(true);
    else this.resetCardFocusability();
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

    this.resetCardFocusability();
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
        const styles = window.getComputedStyle(this.track);
        this.gapPx = parseFloat(styles.columnGap || styles.gap || "0") || 0;

        const first = this.track.children[0];
        this.cardWidthPx = first ? first.offsetWidth || 0 : 0;

        this.groupAdvance = this.computeGroupAdvanceStatic(GROUP_SIZE);

        const viewport = this.container.clientWidth || window.innerWidth;
        const target = viewport * PREFILL_MULTIPLIER;

        if (this.container.scrollWidth < target) this.ensureOverflow();
      }

      if (this.focusWithin) this.refreshVisibleCardFocus(true);
      else this.resetCardFocusability();
      this.updatePaused();
      this.updateButtonUI();
    });
  }

  /**
   * Compute the pixel distance equal to one recycled group (cards + gaps).
   * Uses cached widths/gaps when available to avoid layout reads.
   * @param {number} groupSize
   * @returns {number}
   */
  computeGroupAdvanceStatic(groupSize) {
    if (this.cardWidthPx != null && this.gapPx != null) {
      return groupSize * this.cardWidthPx + groupSize * this.gapPx;
    }

    const first = this.track.children[0];
    let gap = this.gapPx;

    if (gap == null) {
      const styles = window.getComputedStyle(this.track);
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

  /**
   * Compute next logical start index using last child's `data-index`.
   * @returns {number}
   */
  computeNextStartIndex() {
    const len = this.originalCount || 0;
    if (!len) return 0;

    const last = this.track.children[this.track.children.length - 1];
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
   * Always call with GROUP_SIZE to preserve the :nth-child cadence.
   * @param {number} groupSize
   */
  removeFirstGroup(groupSize) {
    for (let i = 0; i < groupSize; i++) {
      const first = this.track.firstElementChild;
      if (!first) break;
      first.remove();
    }
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
    this.root?.removeEventListener("focusin", this.onFocusIn);
    this.root?.removeEventListener("focusout", this.onFocusOut);
    this.root?.removeEventListener("keydown", this.onKeyDown);

    if (this._usingWindowResize) {
      window.removeEventListener("resize", this.onResize);
    }

    this.pauseBtn?.removeEventListener("click", this.onPauseToggle);

    if (this.enabled) this.disable();

    this.destroyed = true;
  }
}
