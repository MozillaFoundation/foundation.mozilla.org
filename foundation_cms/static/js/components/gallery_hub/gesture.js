/**
 * Touch gesture helpers for Gallery Hub interactions.
 *
 * The project carousel and media slideshow both listen for touch gestures, so
 * naming the axis checks keeps their gesture ownership rules consistent.
 *
 * @module galleryHubGesture
 */

/**
 * Check whether a touch gesture moved far enough to claim an intent.
 *
 * @param {number} deltaX - Horizontal gesture movement.
 * @param {number} deltaY - Vertical gesture movement.
 * @param {number} threshold - Minimum movement in either axis.
 * @returns {boolean} Whether the gesture is past the threshold.
 */
export function isPastGestureThreshold(deltaX, deltaY, threshold) {
  return Math.max(Math.abs(deltaX), Math.abs(deltaY)) >= threshold;
}

/**
 * Check whether a gesture is clearly more horizontal than vertical.
 *
 * @param {number} deltaX - Horizontal gesture movement.
 * @param {number} deltaY - Vertical gesture movement.
 * @param {number} axisLock - Multiplier required to claim horizontal intent.
 * @returns {boolean} Whether the gesture should be treated as horizontal.
 */
export function isMostlyHorizontalGesture(deltaX, deltaY, axisLock = 1) {
  return Math.abs(deltaX) > Math.abs(deltaY) * axisLock;
}

/**
 * Check whether a gesture is clearly more vertical than horizontal.
 *
 * @param {number} deltaX - Horizontal gesture movement.
 * @param {number} deltaY - Vertical gesture movement.
 * @param {number} axisLock - Multiplier required to claim vertical intent.
 * @returns {boolean} Whether the gesture should be treated as vertical.
 */
export function isMostlyVerticalGesture(deltaX, deltaY, axisLock = 1) {
  return Math.abs(deltaY) > Math.abs(deltaX) * axisLock;
}
