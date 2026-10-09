import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { CONFIG, createShower, sampleShower } from "./meteor_shower.js";
import { initMeteorHeroes } from "./meteor_hero.js";

const FRAME_MS = 1000 / 60;
const HEAT_TOKENS = [
  "--color-accent-orange",
  "--color-spectrum-yellow-600",
  "--color-spectrum-blue-400",
];
const HEAT = ["#f06c13", "#eec700", "#50c9f0"];

function buildHeroMarkup() {
  document.body.innerHTML = `
    <div class="meteor-hero" data-meteor-hero>
      <canvas class="meteor-hero__canvas" aria-hidden="true"></canvas>
    </div>
  `;
  const root = document.querySelector("[data-meteor-hero]");
  HEAT.forEach((colour, i) => root.style.setProperty(HEAT_TOKENS[i], colour));
  const canvas = document.querySelector("canvas");
  Object.defineProperty(canvas, "clientWidth", { value: 1440 });
  Object.defineProperty(canvas, "clientHeight", { value: 812 });
  return { root, canvas };
}

describe("initMeteorHeroes", () => {
  let context;
  let frames;
  let now;
  let reducedMotion;
  let intersectionCallback;

  // Runs the queued animation frames for a stretch of time, 60 per second.
  const runFrames = (durationMs) => {
    const end = now + durationMs;
    while (now < end) {
      now += FRAME_MS;
      const queued = frames;
      frames = [];
      queued.forEach((callback) => callback(now));
    }
  };
  const setOnScreen = (isIntersecting) =>
    intersectionCallback([{ isIntersecting }]);

  beforeEach(() => {
    context = {
      setTransform: vi.fn(),
      clearRect: vi.fn(),
      fillRect: vi.fn(),
    };
    vi.spyOn(HTMLCanvasElement.prototype, "getContext").mockReturnValue(
      context,
    );

    frames = [];
    now = 0;
    vi.stubGlobal("requestAnimationFrame", (callback) => {
      frames.push(callback);
      return frames.length;
    });
    vi.stubGlobal("cancelAnimationFrame", () => {
      frames = [];
    });

    reducedMotion = new EventTarget();
    reducedMotion.matches = false;
    vi.stubGlobal("matchMedia", () => reducedMotion);

    intersectionCallback = null;
    vi.stubGlobal(
      "IntersectionObserver",
      class {
        constructor(callback) {
          intersectionCallback = callback;
        }
        observe() {}
      },
    );
    vi.stubGlobal(
      "ResizeObserver",
      class {
        observe() {}
      },
    );
    vi.stubGlobal("devicePixelRatio", 1);
  });

  afterEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
    document.body.innerHTML = "";
  });

  it("does nothing when there's no hero on the page", () => {
    expect(() => initMeteorHeroes()).not.toThrow();
    expect(intersectionCallback).toBeNull();
  });

  it("starts each hero only once", () => {
    const { root } = buildHeroMarkup();

    initMeteorHeroes();
    initMeteorHeroes();

    expect(root.dataset.meteorHeroInitialized).toBe("true");
    expect(context.setTransform).toHaveBeenCalledTimes(1);
  });

  it("sizes the canvas for the screen, capped at 2x pixel density", () => {
    vi.stubGlobal("devicePixelRatio", 3);
    const { canvas } = buildHeroMarkup();

    initMeteorHeroes();

    expect([canvas.width, canvas.height]).toEqual([2880, 1624]);
    expect(context.setTransform).toHaveBeenCalledWith(2, 0, 0, 2, 0, 0);
  });

  it("paints cell edges on whole screen pixels at 150% display scaling", () => {
    vi.stubGlobal("devicePixelRatio", 1.5);
    buildHeroMarkup();
    reducedMotion.matches = true;

    initMeteorHeroes();

    const edges = context.fillRect.mock.calls.flatMap(([x, y, w, h]) => [
      x,
      y,
      x + w,
      y + h,
    ]);
    const onScreenPixel = (cssPx) =>
      Math.abs(cssPx * 1.5 - Math.round(cssPx * 1.5)) < 1e-6;
    expect(edges.length).toBeGreaterThan(0);
    expect(edges.every(onScreenPixel)).toBe(true);
  });

  it("paints with the colour tokens", () => {
    buildHeroMarkup();
    reducedMotion.matches = true;

    initMeteorHeroes();

    const colours = new Set(
      context.fillRect.mock.contexts.map((ctx) => ctx.fillStyle),
    );
    expect(colours.size).toBeGreaterThan(0);
    expect([...colours].every((colour) => HEAT.includes(colour))).toBe(true);
  });

  it("draws nothing and warns when a colour token is missing", () => {
    const { root } = buildHeroMarkup();
    root.style.removeProperty("--color-spectrum-yellow-600");
    const warn = vi.spyOn(console, "warn").mockImplementation(() => {});

    initMeteorHeroes();

    expect(warn).toHaveBeenCalledWith(
      expect.stringContaining("--color-spectrum-yellow-600"),
    );
    expect(context.fillRect).not.toHaveBeenCalled();
    // It never starts watching the screen, so it can never start animating.
    expect(intersectionCallback).toBeNull();
  });

  it("waits until the hero is on screen to animate", () => {
    buildHeroMarkup();

    initMeteorHeroes();

    expect(frames).toHaveLength(0);
    setOnScreen(true);
    expect(frames).toHaveLength(1);
  });

  it("repaints once per animation step, not on every frame", () => {
    buildHeroMarkup();
    initMeteorHeroes();
    setOnScreen(true);
    context.clearRect.mockClear();

    runFrames(10 * CONFIG.step);

    // 10 steps' worth of frames is about 66 frames, but only 10 or 11 paints.
    expect(context.clearRect.mock.calls.length).toBeGreaterThanOrEqual(10);
    expect(context.clearRect.mock.calls.length).toBeLessThanOrEqual(11);
  });

  it("stops when the hero leaves the screen and resumes without skipping ahead", () => {
    buildHeroMarkup();
    initMeteorHeroes();
    setOnScreen(true);
    runFrames(1000);

    setOnScreen(false);
    expect(frames).toHaveLength(0);

    const paintsWhileAway = context.clearRect.mock.calls.length;
    context.fillRect.mockClear();
    now += 60000;
    setOnScreen(true);
    runFrames(FRAME_MS);

    // Paints straight away on return, and shows the sky from about 1 second
    // in, where it paused, not from 61 seconds in.
    expect(context.clearRect.mock.calls.length).toBe(paintsWhileAway + 1);
    const painted = context.fillRect.mock.calls;
    const skyAt = (timeMs) =>
      sampleShower(createShower(11), 1440, 812, timeMs, ["", "", ""]).rects.map(
        (rect) => [rect.x, rect.y, rect.w, rect.h],
      );
    expect(painted.length).toBeGreaterThan(0);
    expect([skyAt(900), skyAt(1000)]).toContainEqual(painted);
  });

  it("stops while the tab is hidden", () => {
    buildHeroMarkup();
    initMeteorHeroes();
    setOnScreen(true);

    vi.spyOn(document, "hidden", "get").mockReturnValue(true);
    document.dispatchEvent(new Event("visibilitychange"));

    expect(frames).toHaveLength(0);
  });

  it("shows one still frame and never animates under reduced motion", () => {
    buildHeroMarkup();
    reducedMotion.matches = true;

    initMeteorHeroes();
    setOnScreen(true);

    expect(frames).toHaveLength(0);
    expect(context.fillRect).toHaveBeenCalled();
  });

  it("switches to the still frame when reduced motion is turned on", () => {
    buildHeroMarkup();
    initMeteorHeroes();
    setOnScreen(true);
    runFrames(5000);
    context.fillRect.mockClear();

    reducedMotion.matches = true;
    reducedMotion.dispatchEvent(new Event("change"));

    expect(frames).toHaveLength(0);
    expect(context.fillRect).toHaveBeenCalled();
  });
});
