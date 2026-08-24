import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { SlidingCarousel } from "./sliding_carousel.js";

const SELECTORS = {
  viewport: ".viewport",
  track: ".track",
  item: ".item",
};

function createCarousel({ isCarousel = false, withCounter = true } = {}) {
  document.body.innerHTML = `
    <section class="carousel ${isCarousel ? "is-carousel" : ""}">
      <div class="viewport">
        <div class="track" style="column-gap: 8px; --carousel-transition: transform 200ms ease;">
          <article class="item">One</article>
          <article class="item">Two</article>
          <article class="item">Three</article>
        </div>
      </div>
      <button class="pagination-controls__prev">Previous</button>
      <button class="pagination-controls__next">Next</button>
      ${withCounter ? "<span data-active-index></span>" : ""}
      <button class="carousel-indicators__item"></button>
      <button class="carousel-indicators__item"></button>
      <button class="carousel-indicators__item"></button>
    </section>
  `;

  return new SlidingCarousel(document.querySelector(".carousel"), SELECTORS);
}

describe("SlidingCarousel", () => {
  beforeEach(() => {
    vi.stubGlobal("requestAnimationFrame", (callback) => callback());
    vi.spyOn(HTMLElement.prototype, "getBoundingClientRect").mockReturnValue({
      width: 100,
    });
    Object.defineProperty(window, "innerWidth", {
      configurable: true,
      value: 768,
    });
  });

  afterEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
    document.body.innerHTML = "";
  });

  it("initializes a tripled track at the first logical item", () => {
    const carousel = createCarousel();

    carousel.init();

    expect(carousel.items).toHaveLength(9);
    expect(carousel.index).toBe(3);
    expect(carousel.slideOffset).toBe(108);
    expect(carousel.track.style.transform).toBe("translateX(-324px)");
    expect(carousel.track.style.transition).toBe("none");
    expect(carousel.counterEl.textContent).toBe("1");
    expect(carousel.root.getAttribute("tabindex")).toBe("0");
    expect(
      carousel.root.querySelector(".carousel-indicators__item--active"),
    ).toBe(carousel.root.querySelector(".carousel-indicators__item"));
  });

  it("does not slide a non-carousel at the desktop breakpoint", () => {
    const carousel = createCarousel();
    Object.defineProperty(window, "innerWidth", {
      configurable: true,
      value: 1024,
    });
    const transformSpy = vi.spyOn(carousel, "updateTransform");

    carousel.slideTo(4);

    expect(carousel.index).toBe(3);
    expect(transformSpy).not.toHaveBeenCalled();
  });

  it("slides an explicit carousel on wide viewports and updates its status", () => {
    const carousel = createCarousel({ isCarousel: true });
    Object.defineProperty(window, "innerWidth", {
      configurable: true,
      value: 1280,
    });
    carousel.slideOffset = 100;
    carousel.carouselTransition = "transform 200ms ease";

    carousel.slideTo(4);

    expect(carousel.index).toBe(4);
    expect(carousel.track.style.transform).toBe("translateX(-400px)");
    expect(carousel.track.style.transition).toBe("transform 200ms ease");
    expect(carousel.counterEl.textContent).toBe("2");
    expect(
      carousel.root
        .querySelectorAll(".carousel-indicators__item")[1]
        .getAttribute("aria-current"),
    ).toBe("true");
  });

  it("loops forward from the next clone set", () => {
    const carousel = createCarousel();
    const transformSpy = vi.spyOn(carousel, "updateTransform");
    const counterSpy = vi.spyOn(carousel, "updateCounter");

    expect(carousel.handleLoop(carousel.nextCloneTrackStart)).toBe(true);

    expect(carousel.index).toBe(4);
    expect(transformSpy).toHaveBeenNthCalledWith(1, 3, false);
    expect(transformSpy).toHaveBeenNthCalledWith(2, 4, true);
    expect(counterSpy).toHaveBeenCalledOnce();
  });

  it("loops backward from the previous clone set", () => {
    const carousel = createCarousel();
    const transformSpy = vi.spyOn(carousel, "updateTransform");

    expect(carousel.handleLoop(carousel.prevCloneTrackEnd)).toBe(true);

    expect(carousel.index).toBe(5);
    expect(transformSpy).toHaveBeenNthCalledWith(1, 6, false);
    expect(transformSpy).toHaveBeenNthCalledWith(2, 5, true);
  });

  it("leaves ordinary indices for slideTo to handle", () => {
    const carousel = createCarousel();

    expect(carousel.handleLoop(4)).toBe(false);
    expect(carousel.index).toBe(3);
  });

  it("only navigates for swipes beyond the threshold", () => {
    const carousel = createCarousel();
    const slideSpy = vi.spyOn(carousel, "slideTo").mockImplementation(() => {});

    carousel.handleSwipe(50);
    carousel.handleSwipe(-51);
    carousel.handleSwipe(51);

    expect(slideSpy).toHaveBeenCalledTimes(2);
    expect(slideSpy).toHaveBeenNthCalledWith(1, 4);
    expect(slideSpy).toHaveBeenNthCalledWith(2, 2);
  });

  it("binds pagination, keyboard, and drag interactions", () => {
    const carousel = createCarousel();
    const slideSpy = vi.spyOn(carousel, "slideTo").mockImplementation(() => {});
    const swipeSpy = vi
      .spyOn(carousel, "handleSwipe")
      .mockImplementation(() => {});

    carousel.bindEvents();
    carousel.nextBtn.click();
    carousel.prevBtn.click();
    carousel.root.dispatchEvent(
      new KeyboardEvent("keydown", { key: "ArrowRight" }),
    );
    carousel.root.dispatchEvent(
      new KeyboardEvent("keydown", { key: "ArrowLeft" }),
    );
    carousel.viewport.dispatchEvent(
      new MouseEvent("mousedown", { clientX: 100 }),
    );
    carousel.viewport.dispatchEvent(new MouseEvent("mouseup", { clientX: 20 }));

    expect(slideSpy.mock.calls).toEqual([[4], [2], [4], [2]]);
    expect(swipeSpy).toHaveBeenCalledWith(-80);
  });

  it("updates indicators even when the optional counter is absent", () => {
    const carousel = createCarousel({ withCounter: false });
    carousel.index = 5;

    carousel.updateCounter();

    expect(carousel.counterEl).toBeNull();
    expect(
      carousel.root
        .querySelectorAll(".carousel-indicators__item")[2]
        .getAttribute("aria-current"),
    ).toBe("true");
  });
});
