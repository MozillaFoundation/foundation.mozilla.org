import {
  GROUP_SIZE,
  RECYCLE_SAFETY_MAX,
  FRACTION_EPSILON,
  MAX_FRAME_MS,
} from "./config.js";

/**
 * Main RAF loop:
 * - Converts elapsed time to pixel delta
 * - Recycles cards in GROUP_SIZE batches to preserve nth-child cadence
 * - Applies integer motion via scrollLeft and fractional motion via transform
 * @param {DOMHighResTimeStamp} [ts]
 */
export function tick(ts) {
  if (!this.enabled) return;

  if (this.paused) {
    this.rafId = null;
    return;
  }

  const nowMs = ts ?? performance.now();
  if (this.lastTs == null) this.lastTs = nowMs;

  // Clamp elapsed so tab throttling does not create one giant jump.
  const elapsedMs = Math.max(0, Math.min(nowMs - this.lastTs, MAX_FRAME_MS));
  this.lastTs = nowMs;

  const deltaPx = (this.pxPerSecond * elapsedMs) / 1000;
  const base = this.container.scrollLeft;
  // Whole pixels are applied via scrollLeft; the fractional remainder stays in
  // transform so motion remains smooth without forcing subpixel scroll state.
  let next = base + (this._fractionalRemainder || 0) + deltaPx;

  let safety = 0;
  const threshold = this.groupAdvance;

  // Recycle cards in full groups so the staggered nth-child layout pattern
  // stays intact while rebasing the logical scroll position.
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

  // Commit the integer portion to scrollLeft and keep only the subpixel
  // remainder in transform for the next frame.
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
    this.rafId = requestAnimationFrame(this.tick);
  } else {
    this.rafId = null;
  }
}

/**
 * Stop the RAF loop and reset timestamps.
 */
export function cancelTick() {
  if (this.rafId != null) cancelAnimationFrame(this.rafId);
  this.rafId = null;
  this.lastTs = null;
}
