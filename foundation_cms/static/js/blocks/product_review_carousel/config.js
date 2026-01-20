// Configuration and design invariants for ProductReviewCarousel (ES module)

export const SELECTORS = {
  root: ".product-review-carousel",
  cardsContainer: ".product-review-carousel__cards-container",
  productCard: ".product-review-card",
  pauseButton: ".product-review-carousel__pause-button",
};

export const CLASSNAMES = {
  paused: "is-paused",
  track: "product-review-carousel__track",
};

export const DISABLE_CAROUSEL_MIN_WIDTH = 1024;

// DESIGN INVARIANT — DO NOT CHANGE WITHOUT UPDATING SCSS
// Cards use three vertical offset tracks via :nth-child(3n+1..3). To preserve
// those offsets, we recycle in GROUP_SIZE batches and keep child count a multiple of 3.
export const GROUP_SIZE = 3;

// Prefill/recycling guards
export const PREFILL_MULTIPLIER = 2.5;
export const PREFILL_MAX_LOOPS = 10;
export const RECYCLE_SAFETY_MAX = 6;

// Fractional movement: threshold to skip no-op transform updates
export const FRACTION_EPSILON = 0.125;

// Intersection/Visibility + timing constants
export const IO_ROOT_MARGIN = "50px 0px";
export const IO_THRESHOLDS = [0, 0.01, 0.1];
export const MIN_INTERSECTION_RATIO = 0.01; // consider element visible when >= 1%
export const MAX_FRAME_MS = 48; // clamp large rAF gaps (tab throttling, etc.)

// Default animation speed (pixels per second)
export const DEFAULT_PX_PER_SECOND = 20;
