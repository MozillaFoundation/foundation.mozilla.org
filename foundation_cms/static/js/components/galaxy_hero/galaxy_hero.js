import { createGalaxyRenderer } from "./galaxy_renderer.js";

// Match Meteor's canvas resolution cap and lifecycle vocabulary.
const MAX_PIXEL_RATIO = 2;
// Finish the transition before the sticky stage leaves the viewport.
const TRANSITION_SCROLL_FRACTION = 0.75;
const SELECTORS = {
  root: "[data-galaxy-hero]",
  stage: ".galaxy-hero__stage",
  canvas: ".galaxy-hero__canvas",
  headline: "h1",
  secondHeadline: ".galaxy-hero__second-headline",
};

const COLOR_TOKENS = [
  "--color-gray-100",
  "--color-text-default",
  "--color-text-inverse",
  "--color-accent-blue",
  "--color-accent-orange",
  "--color-spectrum-yellow-600",
  "--color-spectrum-cyan",
  "--color-spectrum-apricot",
  "--color-spectrum-crimson",
  "--color-card-pink",
  "--color-card-lime",
];

/**
 * Connects LP's two-beat renderer to native page scrolling. Like Meteor, its
 * clock runs only on screen in a visible tab; reduced motion draws stills.
 * Geometry and drawing stay in galaxy_renderer.js, with no DOM listeners.
 */
export class GalaxyHero {
  constructor(root) {
    this.root = root;
    this.stage = root.querySelector(SELECTORS.stage);
    this.canvas = root.querySelector(SELECTORS.canvas);
    this.reducedMotion = window.matchMedia?.(
      "(prefers-reduced-motion: reduce)",
    );
    this.frameId = null;
    this.initialized = false;
    this.lastFrameAt = null;
    this.elapsedMs = 0;
    this.isOnScreen = false;
    this.tick = this.tick.bind(this);
    this.update = this.update.bind(this);
    this.onScroll = this.onScroll.bind(this);
  }

  init() {
    if (
      this.root.dataset.galaxyInitialized ||
      !this.canvas?.getContext?.("2d")
    ) {
      return;
    }
    const styles = getComputedStyle(this.root);
    const colors = Object.fromEntries(
      COLOR_TOKENS.map((name) => [
        name,
        styles.getPropertyValue(name).trim().toUpperCase(),
      ]),
    );
    const missing = COLOR_TOKENS.filter((token) => !colors[token]);
    if (missing.length) {
      // Keep the HTML copy visible if the canvas cannot use the site palette.
      console.warn(`Galaxy hero: missing colour tokens ${missing.join(", ")}.`);
      return;
    }
    this.renderer = createGalaxyRenderer(this.canvas, {
      headline: this.root.querySelector(SELECTORS.headline).textContent.trim(),
      secondHeadline: this.root
        .querySelector(SELECTORS.secondHeadline)
        .textContent.trim(),
      background: this.root.dataset.background,
      colors,
    });
    this.initialized = true;
    this.root.dataset.galaxyInitialized = "true";
    this.root.classList.add("galaxy-hero--enhanced");
    if ("ResizeObserver" in window) {
      this.resizeObserver = new ResizeObserver(() => this.resize());
      this.resizeObserver.observe(this.stage);
    }
    if ("IntersectionObserver" in window) {
      this.intersectionObserver = new IntersectionObserver(([entry]) => {
        this.isOnScreen = entry.isIntersecting;
        this.update();
      });
      this.intersectionObserver.observe(this.stage);
    } else {
      this.isOnScreen = true;
    }
    window.addEventListener("scroll", this.onScroll, { passive: true });
    document.addEventListener("visibilitychange", this.update);
    this.reducedMotion?.addEventListener("change", this.update);
    this.resize();
    this.update();
    document.fonts?.ready.then(() => {
      // Font loading can finish after a dynamically mounted hero is removed.
      if (this.initialized) this.resize();
    });
  }

  prefersReducedMotion() {
    return Boolean(this.reducedMotion?.matches);
  }

  /** Map the sticky stage's travel to LP's reversible 0–1 progress input. */
  progress() {
    const stickyTop = parseFloat(getComputedStyle(this.stage).top) || 0;
    const scrollTravel = this.root.offsetHeight - this.stage.offsetHeight;
    const distanceScrolled = stickyTop - this.root.getBoundingClientRect().top;
    return Math.max(
      0,
      Math.min(
        1,
        distanceScrolled /
          Math.max(1, scrollTravel * TRANSITION_SCROLL_FRACTION),
      ),
    );
  }

  redraw() {
    const ink = this.renderer.draw(
      this.progress(),
      this.elapsedMs,
      this.prefersReducedMotion(),
    );
    if (ink) this.stage.style.setProperty("--galaxy-ink", ink);
  }

  resize() {
    if (!this.initialized) return;
    this.renderer.resize(
      this.stage.clientWidth,
      this.stage.clientHeight,
      Math.min(MAX_PIXEL_RATIO, window.devicePixelRatio || 1),
    );
    this.redraw();
  }

  onScroll() {
    if (this.prefersReducedMotion() && this.isOnScreen && !document.hidden)
      this.redraw();
  }

  update() {
    if (!this.initialized) return;
    if (this.prefersReducedMotion()) {
      this.stop();
      this.redraw();
    } else if (this.isOnScreen && !document.hidden) {
      this.start();
    } else {
      this.stop();
    }
  }

  start() {
    if (this.frameId === null) {
      this.frameId = requestAnimationFrame(this.tick);
    }
  }

  // Keep the scene's clock paused off screen, including its delayed copy reveal.
  tick(now) {
    if (this.lastFrameAt !== null) this.elapsedMs += now - this.lastFrameAt;
    this.lastFrameAt = now;
    this.redraw();
    this.frameId = requestAnimationFrame(this.tick);
  }

  stop() {
    if (this.frameId !== null) cancelAnimationFrame(this.frameId);
    this.frameId = null;
    this.lastFrameAt = null;
  }

  destroy() {
    if (!this.initialized) return;
    this.initialized = false;
    this.stop();
    this.intersectionObserver?.disconnect();
    this.resizeObserver?.disconnect();
    window.removeEventListener("scroll", this.onScroll);
    document.removeEventListener("visibilitychange", this.update);
    this.reducedMotion?.removeEventListener("change", this.update);
    this.root.classList.remove("galaxy-hero--enhanced");
    delete this.root.dataset.galaxyInitialized;
  }
}

export function initGalaxyHeroes() {
  document
    .querySelectorAll(SELECTORS.root)
    .forEach((root) => new GalaxyHero(root).init());
}
