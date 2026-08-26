import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { initSpotlightCardCarousels } from "./spotlight_card_carousel.js";

let resizeHandler;

function createCarousel({ cards = 3 } = {}) {
  document.body.innerHTML = `
    <section
      class="spotlight-card-carousel"
      style="--mobile-card-width: 100vw; --mobile-slide-gap: 16px; --mobile-infinite-slides-width: 900vw"
    >
      <div class="spotlight-card-carousel__slides">
        ${Array.from(
          { length: cards },
          (_, index) => `
            <article class="spotlight-card">
              <button class="spotlight-card__image">Image ${index + 1}</button>
              <div class="spotlight-card__content">Content ${index + 1}</div>
            </article>
          `,
        ).join("")}
      </div>
      <div class="spotlight-card-carousel__teaser"></div>
      <nav class="pagination-controls">
        <button data-direction="prev">Previous</button>
        <span data-active-index></span>
        <button data-direction="next">Next</button>
        ${Array.from(
          { length: cards },
          () => '<button class="carousel-indicators__item"></button>',
        ).join("")}
      </nav>
    </section>
  `;

  const root = document.querySelector(".spotlight-card-carousel");
  root.querySelectorAll(".spotlight-card").forEach((card, index) => {
    Object.defineProperty(card, "offsetHeight", { value: 100 + index * 20 });
  });
  Object.defineProperty(
    root.querySelector(".spotlight-card-carousel__teaser"),
    "offsetHeight",
    { value: 20 },
  );
  Object.defineProperty(
    root.querySelector(".pagination-controls"),
    "offsetHeight",
    {
      value: 10,
    },
  );
  return root;
}

function touchEvent(type, clientX) {
  const event = new Event(type, { bubbles: true, cancelable: true });
  Object.defineProperty(event, "touches", { value: [{ clientX }] });
  return event;
}

function transitionEnd(element, propertyName) {
  const event = new Event("transitionend");
  Object.defineProperty(event, "propertyName", { value: propertyName });
  element.dispatchEvent(event);
}

describe("spotlight card carousel", () => {
  beforeEach(() => {
    resizeHandler = null;
    vi.useFakeTimers();
    vi.stubGlobal(
      "requestAnimationFrame",
      vi.fn((callback) => callback()),
    );
    vi.stubGlobal(
      "gettext",
      vi.fn((message) => message),
    );
    vi.stubGlobal(
      "interpolate",
      vi.fn((message, values) =>
        message
          .replace("%(index)s", values.index)
          .replace("%(total)s", values.total),
      ),
    );
    vi.stubGlobal(
      "DOMMatrix",
      class DOMMatrix {
        constructor() {
          this.m41 = -300;
        }
      },
    );
    vi.spyOn(window, "addEventListener").mockImplementation(
      (type, listener) => {
        if (type === "resize") resizeHandler = listener;
      },
    );
    Object.defineProperty(window, "innerWidth", {
      configurable: true,
      value: 1280,
    });
  });

  afterEach(() => {
    vi.useRealTimers();
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
    document.body.innerHTML = "";
  });

  it("initializes desktop positions, accessibility, and measured layout", () => {
    const root = createCarousel();

    initSpotlightCardCarousels();

    const cards = root.querySelectorAll(".spotlight-card");
    expect(Array.from(cards, (card) => card.dataset.displayPosition)).toEqual([
      "1",
      "2",
      "3",
    ]);
    expect(cards[0].getAttribute("aria-hidden")).toBe("false");
    expect(cards[0].hasAttribute("tabindex")).toBe(false);
    expect(cards[1].getAttribute("role")).toBe("button");
    expect(cards[1].getAttribute("tabindex")).toBe("0");
    expect(cards[0].getAttribute("aria-label")).toBe("Card 1 of 3");
    expect(
      root.querySelector(".spotlight-card-carousel__teaser").textContent,
    ).toBe("Content 1");
    expect(root.style.getPropertyValue("--featured-image-height")).toBe(
      "100px",
    );
    expect(
      root.querySelector(".spotlight-card-carousel__slides").style.minHeight,
    ).toBe("130px");
  });

  it("navigates with buttons, card images, and keyboard activation", () => {
    const root = createCarousel();
    initSpotlightCardCarousels();
    const counter = root.querySelector("[data-active-index]");
    const next = root.querySelector("[data-direction='next']");
    const prev = root.querySelector("[data-direction='prev']");

    next.click();
    expect(counter.textContent).toBe("2");
    expect(
      root.querySelector("[data-display-position='1']").textContent,
    ).toContain("Content 2");
    expect(
      root
        .querySelectorAll(".carousel-indicators__item")[1]
        .getAttribute("aria-current"),
    ).toBe("true");

    prev.click();
    expect(counter.textContent).toBe("1");

    const middleImage = root.querySelector(
      "[data-display-position='2'] .spotlight-card__image",
    );
    middleImage.click();
    expect(counter.textContent).toBe("2");

    const lastCard = root.querySelector("[data-display-position='3']");
    const keyEvent = new KeyboardEvent("keydown", {
      bubbles: true,
      cancelable: true,
      key: "Enter",
    });
    lastCard.dispatchEvent(keyEvent);
    expect(keyEvent.defaultPrevented).toBe(true);
    expect(counter.textContent).toBe("1");

    next.setAttribute("disabled", "");
    next.click();
    expect(counter.textContent).toBe("1");
  });

  it("creates a tripled mobile track and handles swipe movement", () => {
    Object.defineProperty(window, "innerWidth", {
      configurable: true,
      value: 500,
    });
    const root = createCarousel();
    initSpotlightCardCarousels();
    const slides = root.querySelector(".spotlight-card-carousel__slides");

    expect(slides.querySelectorAll(".spotlight-card")).toHaveLength(9);
    expect(slides.style.width).toBe("900vw");
    expect(slides.style.transform).toContain("3 * (-100vw - 16px)");

    slides.dispatchEvent(touchEvent("touchstart", 100));
    const moveEvent = touchEvent("touchmove", 20);
    slides.dispatchEvent(moveEvent);
    expect(moveEvent.defaultPrevented).toBe(true);
    expect(slides.style.transform).toBe("translateX(-380px)");

    slides.dispatchEvent(touchEvent("touchend", 20));
    expect(root.querySelector("[data-active-index]").textContent).toBe("2");
    vi.advanceTimersByTime(300);
    expect(slides.style.transition).toBe("");
  });

  it("snaps back after a short swipe and ignores touch on desktop", () => {
    Object.defineProperty(window, "innerWidth", {
      configurable: true,
      value: 500,
    });
    const root = createCarousel();
    initSpotlightCardCarousels();
    const slides = root.querySelector(".spotlight-card-carousel__slides");

    slides.dispatchEvent(touchEvent("touchstart", 100));
    slides.dispatchEvent(touchEvent("touchmove", 80));
    slides.dispatchEvent(touchEvent("touchend", 80));
    expect(root.querySelector("[data-active-index]").textContent).toBe("");
    expect(slides.style.transform).toContain("3 * (-100vw - 16px)");

    Object.defineProperty(window, "innerWidth", {
      configurable: true,
      value: 1280,
    });
    resizeHandler();
    vi.advanceTimersByTime(200);
    const desktopTransform = slides.style.transform;
    slides.dispatchEvent(touchEvent("touchstart", 100));
    expect(slides.style.transform).toBe(desktopTransform);
  });

  it("rebases mobile clone positions after transform transitions", () => {
    Object.defineProperty(window, "innerWidth", {
      configurable: true,
      value: 500,
    });
    const root = createCarousel();
    initSpotlightCardCarousels();
    const slides = root.querySelector(".spotlight-card-carousel__slides");
    const next = root.querySelector("[data-direction='next']");

    next.click();
    next.click();
    next.click();
    const beforeReset = slides.style.transform;
    transitionEnd(slides, "opacity");
    expect(slides.style.transform).toBe(beforeReset);

    transitionEnd(slides, "transform");
    expect(slides.style.transform).toContain("3 * (-100vw - 16px)");
    expect(slides.style.transition).toBe("transform 300ms ease-out");
  });

  it("rebases the leading mobile clone after navigating before the first card", () => {
    Object.defineProperty(window, "innerWidth", {
      configurable: true,
      value: 500,
    });
    const root = createCarousel();
    initSpotlightCardCarousels();
    const slides = root.querySelector(".spotlight-card-carousel__slides");
    const prev = root.querySelector("[data-direction='prev']");

    prev.click();

    expect(root.querySelector("[data-active-index]").textContent).toBe("3");
    expect(slides.style.transform).toContain("2 * (-100vw - 16px)");

    transitionEnd(slides, "transform");

    expect(slides.style.transform).toContain("5 * (-100vw - 16px)");
    expect(slides.style.transition).toBe("transform 300ms ease-out");
  });

  it("reinitializes only when the responsive breakpoint changes", () => {
    const root = createCarousel();
    initSpotlightCardCarousels();
    const slides = root.querySelector(".spotlight-card-carousel__slides");

    resizeHandler();
    vi.advanceTimersByTime(200);
    expect(slides.querySelectorAll(".spotlight-card")).toHaveLength(3);

    Object.defineProperty(window, "innerWidth", {
      configurable: true,
      value: 500,
    });
    resizeHandler();
    vi.advanceTimersByTime(200);
    expect(slides.querySelectorAll(".spotlight-card")).toHaveLength(9);

    Object.defineProperty(window, "innerWidth", {
      configurable: true,
      value: 1280,
    });
    resizeHandler();
    vi.advanceTimersByTime(200);
    expect(slides.querySelectorAll(".spotlight-card")).toHaveLength(3);
  });

  it("ignores empty carousel roots", () => {
    document.body.innerHTML =
      '<section class="spotlight-card-carousel"></section>';
    expect(() => initSpotlightCardCarousels()).not.toThrow();
  });
});
