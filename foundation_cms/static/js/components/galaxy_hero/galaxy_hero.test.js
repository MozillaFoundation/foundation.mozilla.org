import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { GalaxyHero } from "./galaxy_hero.js";

vi.mock("./galaxy_renderer.js", () => ({
  createGalaxyRenderer: () => ({
    draw: vi.fn(() => "#161616"),
    resize: vi.fn(),
  }),
}));

describe("Galaxy lifecycle", () => {
  let hero, motion, intersection, frames, hidden;
  beforeEach(() => {
    frames = new Map();
    let id = 0;
    vi.stubGlobal("requestAnimationFrame", (cb) => {
      frames.set(++id, cb);
      return id;
    });
    vi.stubGlobal("cancelAnimationFrame", (id) => frames.delete(id));
    motion = new EventTarget();
    motion.matches = false;
    vi.stubGlobal("matchMedia", () => motion);
    hidden = false;
    vi.spyOn(document, "hidden", "get").mockImplementation(() => hidden);
    vi.stubGlobal("getComputedStyle", () => ({
      getPropertyValue: () => "#161616",
      top: "88px",
    }));
    vi.stubGlobal(
      "ResizeObserver",
      class {
        observe() {}
        disconnect() {}
      },
    );
    vi.stubGlobal(
      "IntersectionObserver",
      class {
        constructor(cb) {
          intersection = cb;
        }
        observe() {}
        disconnect() {}
      },
    );
    vi.spyOn(HTMLCanvasElement.prototype, "getContext").mockReturnValue({});
    document.body.innerHTML =
      '<div data-galaxy-hero><div class="galaxy-hero__stage"><canvas class="galaxy-hero__canvas"></canvas><h1>First</h1><p class="galaxy-hero__second-headline">Second</p></div></div>';
    hero = new GalaxyHero(document.querySelector("[data-galaxy-hero]"));
    hero.init();
  });
  afterEach(() => {
    hero.destroy();
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
  });

  it("runs only on screen in a visible tab", () => {
    expect(frames.size).toBe(0);
    intersection([{ isIntersecting: true }]);
    expect(frames.size).toBe(1);
    hidden = true;
    document.dispatchEvent(new Event("visibilitychange"));
    expect(frames.size).toBe(0);
    hidden = false;
    document.dispatchEvent(new Event("visibilitychange"));
    expect(frames.size).toBe(1);
    intersection([{ isIntersecting: false }]);
    expect(frames.size).toBe(0);
  });

  it("pauses elapsed time and resumes without jumping", () => {
    hero.tick(100);
    hero.tick(116);
    expect(hero.elapsedMs).toBe(16);
    hero.stop();
    hero.tick(10000);
    expect(hero.elapsedMs).toBe(16);
  });

  it("uses still drawings for reduced motion and resumes when changed", () => {
    intersection([{ isIntersecting: true }]);
    motion.matches = true;
    motion.dispatchEvent(new Event("change"));
    expect(frames.size).toBe(0);
    hero.onScroll();
    expect(hero.renderer.draw).toHaveBeenLastCalledWith(
      expect.any(Number),
      0,
      true,
    );
    motion.matches = false;
    motion.dispatchEvent(new Event("change"));
    expect(frames.size).toBe(1);
  });

  it("maps native page movement to reversible progress", () => {
    Object.defineProperty(hero.root, "offsetHeight", { value: 3000 });
    Object.defineProperty(hero.stage, "offsetHeight", { value: 800 });
    vi.spyOn(hero.root, "getBoundingClientRect").mockReturnValue({
      top: -1012,
    });
    expect(hero.progress()).toBe(0.5);
    hero.root.getBoundingClientRect.mockReturnValue({ top: -3000 });
    expect(hero.progress()).toBe(1);
    hero.root.getBoundingClientRect.mockReturnValue({ top: 88 });
    expect(hero.progress()).toBe(0);
  });

  it("does not create duplicate animation loops on repeated visibility updates", () => {
    intersection([{ isIntersecting: true }]);
    intersection([{ isIntersecting: true }]);
    document.dispatchEvent(new Event("visibilitychange"));
    expect(frames.size).toBe(1);
  });

  it("cleans up listeners, restores HTML copy and allows remounting", () => {
    intersection([{ isIntersecting: true }]);
    expect(hero.stage.style.getPropertyValue("--galaxy-ink")).toBe("#161616");
    hero.destroy();
    expect(frames.size).toBe(0);
    expect(hero.stage.style.getPropertyValue("--galaxy-ink")).toBe("");
    expect(hero.root.classList.contains("galaxy-hero--enhanced")).toBe(false);
    expect(hero.root.dataset.galaxyInitialized).toBeUndefined();
    document.dispatchEvent(new Event("visibilitychange"));
    motion.dispatchEvent(new Event("change"));
    expect(frames.size).toBe(0);
    hero.init();
    intersection([{ isIntersecting: true }]);
    expect(frames.size).toBe(1);
  });

  it("animates without optional browser APIs and still pauses in a hidden tab", () => {
    hero.destroy();
    delete window.matchMedia;
    delete window.ResizeObserver;
    delete window.IntersectionObserver;
    hero = new GalaxyHero(document.querySelector("[data-galaxy-hero]"));
    hero.init();
    expect(hero.renderer.resize).toHaveBeenCalled();
    expect(hero.renderer.draw).toHaveBeenLastCalledWith(
      expect.any(Number),
      0,
      false,
    );
    expect(frames.size).toBe(1);
    hidden = true;
    document.dispatchEvent(new Event("visibilitychange"));
    expect(frames.size).toBe(0);
    hidden = false;
    document.dispatchEvent(new Event("visibilitychange"));
    expect(frames.size).toBe(1);
    expect(() => hero.destroy()).not.toThrow();
    expect(frames.size).toBe(0);
  });

  it("keeps reduced-motion stills when intersection observation is unavailable", () => {
    hero.destroy();
    delete window.IntersectionObserver;
    motion.matches = true;
    hero = new GalaxyHero(document.querySelector("[data-galaxy-hero]"));
    hero.init();
    expect(frames.size).toBe(0);
    hero.renderer.draw.mockClear();
    window.dispatchEvent(new Event("scroll"));
    expect(hero.renderer.draw).toHaveBeenCalledExactlyOnceWith(
      expect.any(Number),
      0,
      true,
    );
    hero.destroy();
    hero.renderer.draw.mockClear();
    window.dispatchEvent(new Event("scroll"));
    expect(hero.renderer.draw).not.toHaveBeenCalled();
  });

  it("leaves the HTML fallback visible when canvas has no context API", () => {
    hero.destroy();
    hero.canvas.getContext = undefined;
    expect(() => hero.init()).not.toThrow();
    expect(hero.root.classList.contains("galaxy-hero--enhanced")).toBe(false);
    expect(frames.size).toBe(0);
  });

  it("initializes and cleans up when the media query has no event listener methods", () => {
    hero.destroy();
    vi.stubGlobal("matchMedia", () => ({ matches: true }));
    hero = new GalaxyHero(document.querySelector("[data-galaxy-hero]"));
    expect(() => hero.init()).not.toThrow();
    expect(hero.renderer.resize).toHaveBeenCalled();
    expect(hero.renderer.draw).toHaveBeenLastCalledWith(
      expect.any(Number),
      0,
      true,
    );
    expect(frames.size).toBe(0);
    expect(() => hero.destroy()).not.toThrow();
    expect(hero.root.classList.contains("galaxy-hero--enhanced")).toBe(false);
  });
});
