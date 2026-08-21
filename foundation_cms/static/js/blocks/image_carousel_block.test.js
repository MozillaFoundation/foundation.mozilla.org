import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { initImageCarousels } from "./image_carousel_block.js";

function createImageCarousel({ slides = 3 } = {}) {
  document.body.insertAdjacentHTML(
    "beforeend",
    `
      <section class="image-carousel is-carousel">
        <div class="image-carousel__card-container">
          <div
            class="image-carousel__track"
            style="column-gap: 16px; --carousel-transition: transform 300ms ease-out"
          >
            ${Array.from(
              { length: slides },
              (_, index) =>
                `<article class="image-carousel__slide">Image ${index + 1}</article>`,
            ).join("")}
          </div>
        </div>
        <button class="pagination-controls__prev">Previous</button>
        <span data-active-index></span>
        <button class="pagination-controls__next">Next</button>
        ${Array.from(
          { length: slides },
          () => '<button class="carousel-indicators__item"></button>',
        ).join("")}
      </section>
    `,
  );
  return document
    .querySelectorAll(".image-carousel")
    .item(document.querySelectorAll(".image-carousel").length - 1);
}

function touchEvent(type, clientX) {
  const event = new Event(type, { bubbles: true });
  Object.defineProperty(event, "touches", { value: [{ clientX }] });
  Object.defineProperty(event, "changedTouches", { value: [{ clientX }] });
  return event;
}

describe("image carousel block", () => {
  beforeEach(() => {
    vi.stubGlobal(
      "requestAnimationFrame",
      vi.fn((callback) => callback()),
    );
    vi.spyOn(HTMLElement.prototype, "getBoundingClientRect").mockReturnValue({
      width: 200,
    });
  });

  afterEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
    document.body.innerHTML = "";
  });

  it("initializes every image carousel with an infinite track", () => {
    const first = createImageCarousel();
    const second = createImageCarousel({ slides: 2 });

    initImageCarousels();

    expect(first.querySelectorAll(".image-carousel__slide")).toHaveLength(9);
    expect(second.querySelectorAll(".image-carousel__slide")).toHaveLength(6);
    expect(first.querySelector(".image-carousel__track").style.transform).toBe(
      "translateX(-648px)",
    );
    expect(first.querySelector(".image-carousel__track").style.transition).toBe(
      "none",
    );
    expect(first.querySelector("[data-active-index]").textContent).toBe("1");
    expect(
      first
        .querySelector(".carousel-indicators__item")
        .getAttribute("aria-current"),
    ).toBe("true");
    expect(first.getAttribute("tabindex")).toBe("0");
  });

  it("navigates with controls, keyboard, and swipe gestures", () => {
    const root = createImageCarousel();
    initImageCarousels();
    const track = root.querySelector(".image-carousel__track");
    const viewport = root.querySelector(".image-carousel__card-container");

    root.querySelector(".pagination-controls__next").click();
    expect(root.querySelector("[data-active-index]").textContent).toBe("2");
    expect(track.style.transform).toBe("translateX(-864px)");
    expect(track.style.transition).toBe("transform 300ms ease-out");

    root.dispatchEvent(new KeyboardEvent("keydown", { key: "ArrowLeft" }));
    expect(root.querySelector("[data-active-index]").textContent).toBe("1");

    viewport.dispatchEvent(touchEvent("touchstart", 100));
    viewport.dispatchEvent(touchEvent("touchend", 20));
    expect(root.querySelector("[data-active-index]").textContent).toBe("2");

    viewport.dispatchEvent(touchEvent("touchstart", 100));
    viewport.dispatchEvent(touchEvent("touchend", 80));
    expect(root.querySelector("[data-active-index]").textContent).toBe("2");
  });

  it("does nothing when no image carousels are present", () => {
    expect(() => initImageCarousels()).not.toThrow();
  });
});
