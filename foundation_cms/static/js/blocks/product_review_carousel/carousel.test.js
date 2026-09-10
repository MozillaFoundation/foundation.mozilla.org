import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import ProductReviewCarousel from "./carousel.js";

let frameCallbacks;
let intersectionCallback;
let resizeCallback;
let intersectionObserver;
let resizeObserver;
let reducedMotion;

function createRoot({
  cards = 4,
  withContainer = true,
  withTrack = true,
} = {}) {
  document.body.innerHTML = `
    <section class="product-review-carousel">
      ${
        withContainer
          ? `<div class="product-review-carousel__cards-container">
              ${
                withTrack
                  ? `<div class="product-review-carousel__track">
                      ${Array.from(
                        { length: cards },
                        (_, index) =>
                          `<article class="product-review-carousel__card-wrapper"><a href="#${index}">Card ${index}</a></article>`,
                      ).join("")}
                    </div>`
                  : ""
              }
            </div>`
          : ""
      }
      <button class="product-review-carousel__pause-button"></button>
    </section>
  `;
  const root = document.querySelector(".product-review-carousel");
  Object.defineProperty(root, "clientWidth", {
    configurable: true,
    value: 1024,
  });
  const container = root.querySelector(
    ".product-review-carousel__cards-container",
  );
  if (container) {
    Object.defineProperty(container, "clientWidth", { value: 200 });
    Object.defineProperty(container, "scrollWidth", {
      configurable: true,
      value: 1000,
    });
  }
  root
    .querySelectorAll(".product-review-carousel__card-wrapper")
    .forEach((card) =>
      Object.defineProperty(card, "offsetWidth", { value: 80 }),
    );
  return root;
}

describe("ProductReviewCarousel", () => {
  beforeEach(() => {
    frameCallbacks = [];
    reducedMotion = false;
    intersectionObserver = { observe: vi.fn(), disconnect: vi.fn() };
    resizeObserver = { observe: vi.fn(), disconnect: vi.fn() };
    vi.stubGlobal(
      "matchMedia",
      vi.fn(() => ({ matches: reducedMotion })),
    );
    vi.stubGlobal(
      "requestAnimationFrame",
      vi.fn((callback) => {
        frameCallbacks.push(callback);
        return frameCallbacks.length;
      }),
    );
    vi.stubGlobal("cancelAnimationFrame", vi.fn());
    vi.stubGlobal(
      "IntersectionObserver",
      vi.fn((callback) => {
        intersectionCallback = callback;
        return intersectionObserver;
      }),
    );
    vi.stubGlobal(
      "ResizeObserver",
      vi.fn((callback) => {
        resizeCallback = callback;
        return resizeObserver;
      }),
    );
    vi.stubGlobal(
      "gettext",
      vi.fn((message) => message),
    );
  });

  afterEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
    document.body.innerHTML = "";
  });

  it("initializes cards, observers, and responsive setup", () => {
    const root = createRoot();
    const carousel = new ProductReviewCarousel(root);

    expect(carousel.originalCount).toBe(4);
    expect(
      Array.from(carousel.track.children, (card) => card.dataset.index),
    ).toEqual(["0", "1", "2", "3"]);
    expect(intersectionObserver.observe).toHaveBeenCalledWith(root);
    expect(resizeObserver.observe).toHaveBeenCalledWith(root);
    expect(frameCallbacks).toHaveLength(1);

    frameCallbacks.shift()();
    expect(carousel.enabled).toBe(true);
    expect(carousel.track.children.length % 3).toBe(0);
    expect(carousel.track.style.willChange).toBe("transform");

    intersectionCallback([{ intersectionRatio: 0, isIntersecting: false }]);
    expect(carousel._offscreen).toBe(true);
    expect(carousel.paused).toBe(true);
  });

  it("honors reduced motion and tolerates incomplete markup", () => {
    reducedMotion = true;
    const root = createRoot();
    const carousel = new ProductReviewCarousel(root);
    expect(carousel.destroyed).toBe(true);
    expect(carousel.pauseBtn.style.display).toBe("none");

    reducedMotion = false;
    expect(
      new ProductReviewCarousel(createRoot({ withContainer: false })).track,
    ).toBeNull();
    expect(
      new ProductReviewCarousel(createRoot({ withTrack: false })).track,
    ).toBeNull();
  });

  it("computes sequencing and appends wrapped cards", () => {
    const carousel = new ProductReviewCarousel(createRoot({ cards: 4 }));
    carousel.cardWidthPx = 80;
    carousel.gapPx = 10;
    expect(carousel.computeGroupAdvance(3)).toBe(270);
    expect(carousel.computeNextStartIndex()).toBe(0);

    carousel.appendCardsFromStart(3, 3);
    expect(
      Array.from(carousel.track.children)
        .slice(-3)
        .map((card) => card.dataset.index),
    ).toEqual(["3", "0", "1"]);

    carousel.removeFirstGroup(3);
    expect(carousel.track.children).toHaveLength(4);
  });

  it("enables, disables, and destroys while restoring pristine markup", () => {
    const root = createRoot({ cards: 3 });
    const carousel = new ProductReviewCarousel(root);
    carousel.enable();
    expect(carousel.enabled).toBe(true);

    carousel.track.appendChild(document.createElement("article"));
    carousel.disable();
    expect(carousel.enabled).toBe(false);
    expect(carousel.track.children).toHaveLength(3);
    expect(carousel.track.style.willChange).toBe("auto");

    carousel.destroy();
    carousel.destroy();
    expect(carousel.destroyed).toBe(true);
    expect(intersectionObserver.disconnect).toHaveBeenCalledOnce();
    expect(resizeObserver.disconnect).toHaveBeenCalledOnce();
  });

  it("uses the window resize fallback when ResizeObserver is unavailable", () => {
    vi.unstubAllGlobals();
    vi.stubGlobal(
      "matchMedia",
      vi.fn(() => ({ matches: false })),
    );
    vi.stubGlobal(
      "requestAnimationFrame",
      vi.fn(() => 1),
    );
    vi.stubGlobal("cancelAnimationFrame", vi.fn());
    vi.stubGlobal(
      "gettext",
      vi.fn((message) => message),
    );
    const addSpy = vi.spyOn(window, "addEventListener");
    const removeSpy = vi.spyOn(window, "removeEventListener");
    const carousel = new ProductReviewCarousel(createRoot());

    expect(carousel._usingWindowResize).toBe(true);
    expect(addSpy).toHaveBeenCalledWith("resize", carousel.onResize, {
      passive: true,
    });

    carousel.destroy();
    expect(removeSpy).toHaveBeenCalledWith("resize", carousel.onResize);
  });
});
