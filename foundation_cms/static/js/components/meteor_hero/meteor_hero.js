// Based on the drawing code in LP studio/heroes/meteor.html (LP commit 52c6b4100d).
import { CONFIG, createShower, sampleShower } from "./meteor_shower.js";

/**
 * LP's seed, and the one frame of it shown under reduced motion. LP holds
 * 3600ms as "a rich mid-flight frame", but since LP doubled the flight speed
 * that moment falls in a lull and the sky is empty at every screen size.
 * 1320ms is the first big meteor mid-flight, its head clear above the
 * headline on desktop.
 * TODO: Confirm the still frame with design.
 */
const SEED = 11;
const STILL_FRAME_MS = 1320;

/**
 * Caps the canvas resolution, as LP does, so 3x screens don't triple the
 * pixels drawn every frame.
 */
const MAX_PIXEL_RATIO = 2;

/**
 * LP's Logo heat ladder, hottest to coolest, read from our colour tokens.
 */
const HEAT_TOKENS = [
  "--color-accent-orange",
  "--color-spectrum-yellow-600",
  "--color-spectrum-blue-400",
];

const SELECTORS = {
  root: "[data-meteor-hero]",
  canvas: ".meteor-hero__canvas",
};

/**
 * Draws the pixel meteor shower on the Meteor hero's canvas. The animation
 * runs only while the hero is on screen, the tab is visible and the visitor
 * hasn't asked for reduced motion, which gets one still frame instead.
 */
export class MeteorHero {
  /**
   * @param {HTMLElement} root - The hero element, marked `data-meteor-hero`.
   */
  constructor(root) {
    this.root = root;
    this.canvas = root.querySelector(SELECTORS.canvas);
    this.context = this.canvas?.getContext?.("2d") ?? null;
    this.reducedMotion = window.matchMedia?.(
      "(prefers-reduced-motion: reduce)",
    );
    this.shower = createShower(SEED);
    this.heat = [];
    this.width = 0;
    this.height = 0;
    this.pixelRatio = 1;
    this.elapsedMs = 0;
    this.lastFrameAt = null;
    this.paintedStep = null;
    this.frameId = null;
    this.isOnScreen = false;
    this.tick = this.tick.bind(this);
    this.update = this.update.bind(this);
  }

  init() {
    if (!this.context || this.root.dataset.meteorHeroInitialized === "true") {
      return;
    }
    this.root.dataset.meteorHeroInitialized = "true";

    // A missing token would make the canvas fall back to black squares, so
    // leave the hero without its shower and say which token is missing.
    const styles = getComputedStyle(this.root);
    this.heat = HEAT_TOKENS.map((token) =>
      styles.getPropertyValue(token).trim(),
    );
    const missing = HEAT_TOKENS.filter((_token, i) => !this.heat[i]);
    if (missing.length) {
      console.warn(
        `Meteor hero: missing colour tokens ${missing.join(", ")}, so the meteor shower won't be drawn.`,
      );
      return;
    }

    this.resize();

    if ("ResizeObserver" in window) {
      new ResizeObserver(() => this.resize()).observe(this.canvas);
    }
    if ("IntersectionObserver" in window) {
      new IntersectionObserver(([entry]) => {
        this.isOnScreen = entry.isIntersecting;
        this.update();
      }).observe(this.root);
    } else {
      this.isOnScreen = true;
    }
    document.addEventListener("visibilitychange", this.update);
    this.reducedMotion?.addEventListener?.("change", this.update);

    this.update();
  }

  /**
   * @returns {boolean} Whether the visitor has asked for reduced motion.
   */
  prefersReducedMotion() {
    return Boolean(this.reducedMotion?.matches);
  }

  /**
   * Starts or stops the animation to match the current conditions, and draws
   * the still frame under reduced motion.
   */
  update() {
    if (this.prefersReducedMotion()) {
      this.stop();
      this.redraw();
      return;
    }
    if (this.isOnScreen && !document.hidden) {
      this.start();
    } else {
      this.stop();
    }
  }

  start() {
    if (this.frameId !== null) return;
    // The canvas may be showing the still frame, so always paint first.
    this.paintedStep = null;
    this.frameId = requestAnimationFrame(this.tick);
  }

  stop() {
    if (this.frameId !== null) cancelAnimationFrame(this.frameId);
    this.frameId = null;
    this.lastFrameAt = null;
  }

  /**
   * Advances the shower's clock by the time since the last frame, so it picks
   * up where it paused rather than jumping ahead. The shower only moves in
   * 110ms steps, so it repaints when the step changes rather than on every
   * frame, which skips about 85% of repaints with no visible difference.
   *
   * @param {DOMHighResTimeStamp} now
   */
  tick(now) {
    if (this.lastFrameAt !== null) this.elapsedMs += now - this.lastFrameAt;
    this.lastFrameAt = now;
    const step = Math.floor(this.elapsedMs / CONFIG.step);
    if (step !== this.paintedStep) {
      this.paintedStep = step;
      this.draw(this.shower, this.elapsedMs);
    }
    this.frameId = requestAnimationFrame(this.tick);
  }

  /**
   * Draws the still frame from a fresh sky, so it's the same frame whenever
   * it's shown, even after the animation has run.
   */
  drawStill() {
    this.draw(createShower(SEED), STILL_FRAME_MS);
  }

  /**
   * Repaints what should be showing now: the still frame under reduced motion,
   * otherwise the shower at its current time.
   */
  redraw() {
    if (this.prefersReducedMotion()) {
      this.drawStill();
    } else {
      this.draw(this.shower, this.elapsedMs);
    }
  }

  /**
   * Matches the canvas to its displayed size, then redraws, since resizing a
   * canvas clears it.
   */
  resize() {
    this.pixelRatio = Math.min(MAX_PIXEL_RATIO, window.devicePixelRatio || 1);
    this.width = this.canvas.clientWidth;
    this.height = this.canvas.clientHeight;
    this.canvas.width = Math.round(this.width * this.pixelRatio);
    this.canvas.height = Math.round(this.height * this.pixelRatio);
    this.context.setTransform(this.pixelRatio, 0, 0, this.pixelRatio, 0, 0);
    this.redraw();
  }

  /**
   * Rounds a position to the nearest whole screen pixel. At display scaling
   * like 125% or 150%, cell edges otherwise land between screen pixels, which
   * blurs them and leaves faint seams where two cells touch.
   *
   * @param {number} value - A position in CSS px.
   * @returns {number}
   */
  snapToScreenPixel(value) {
    return Math.round(value * this.pixelRatio) / this.pixelRatio;
  }

  /**
   * @param {{seed: number, sky: object}} shower
   * @param {number} timeMs
   */
  draw(shower, timeMs) {
    const { context } = this;
    context.clearRect(0, 0, this.width, this.height);
    if (!this.width || !this.height) return;

    const { rects } = sampleShower(
      shower,
      this.width,
      this.height,
      timeMs,
      this.heat,
    );
    for (const rect of rects) {
      const left = this.snapToScreenPixel(rect.x);
      const top = this.snapToScreenPixel(rect.y);
      const right = this.snapToScreenPixel(rect.x + rect.w);
      const bottom = this.snapToScreenPixel(rect.y + rect.h);
      context.globalAlpha = rect.a;
      context.fillStyle = rect.color;
      context.fillRect(left, top, right - left, bottom - top);
    }
    context.globalAlpha = 1;
  }
}

/**
 * Starts every Meteor hero on the page.
 */
export function initMeteorHeroes() {
  document
    .querySelectorAll(SELECTORS.root)
    .forEach((root) => new MeteorHero(root).init());
}
