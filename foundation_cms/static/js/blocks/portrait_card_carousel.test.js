import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { initPortraitCardSetCarousels } from "./portrait_card_carousel.js";

function createPortraitCarousel({ cards = 5 } = {}) {
  document.body.insertAdjacentHTML(
    "beforeend",
    `
      <section class="portrait-card-set is-carousel">
        <div class="portrait-card-set__card-container">
          <div class="carousel-track" style="--carousel-transition: transform 250ms ease-out">
            ${Array.from(
              { length: cards },
              (_, index) => `
                <article class="portrait-card" style="margin-right: 24px">
                  Portrait ${index + 1}
                </article>
              `,
            ).join("")}
          </div>
        </div>
        <button class="pagination-controls__prev">Previous</button>
        <span data-active-index></span>
        <button class="pagination-controls__next">Next</button>
        ${Array.from(
          { length: cards },
          () => '<button class="carousel-indicators__item"></button>',
        ).join("")}
      </section>
    `,
  );
  return document
    .querySelectorAll(".portrait-card-set")
    .item(document.querySelectorAll(".portrait-card-set").length - 1);
}

describe("portrait card carousel", () => {
  beforeEach(() => {
    vi.stubGlobal(
      "requestAnimationFrame",
      vi.fn((callback) => callback()),
    );
    vi.spyOn(HTMLElement.prototype, "getBoundingClientRect").mockReturnValue({
      width: 176,
    });
  });

  afterEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
    document.body.innerHTML = "";
  });

  it("cycles four card designs before tripling the carousel track", () => {
    const root = createPortraitCarousel();

    initPortraitCardSetCarousels();

    const cards = root.querySelectorAll(".portrait-card");
    expect(cards).toHaveLength(15);
    expect(
      Array.from(cards)
        .slice(5, 10)
        .map((card) => card.dataset.cardDesign),
    ).toEqual(["0", "1", "2", "3", "0"]);
    expect(root.querySelector(".carousel-track").style.transform).toBe(
      "translateX(-1000px)",
    );
    expect(root.querySelector("[data-active-index]").textContent).toBe("1");
  });

  it("uses card margins for spacing and updates navigation state", () => {
    const root = createPortraitCarousel({ cards: 2 });
    initPortraitCardSetCarousels();
    const track = root.querySelector(".carousel-track");

    expect(track.style.transform).toBe("translateX(-400px)");
    root.querySelector(".pagination-controls__next").click();
    expect(track.style.transform).toBe("translateX(-600px)");
    expect(track.style.transition).toBe("transform 250ms ease-out");
    expect(root.querySelector("[data-active-index]").textContent).toBe("2");
    expect(
      root
        .querySelectorAll(".carousel-indicators__item")[1]
        .getAttribute("aria-current"),
    ).toBe("true");

    root.querySelector(".pagination-controls__prev").click();
    expect(root.querySelector("[data-active-index]").textContent).toBe("1");
  });

  it("initializes multiple roots and ignores an empty page", () => {
    const first = createPortraitCarousel({ cards: 1 });
    const second = createPortraitCarousel({ cards: 2 });
    initPortraitCardSetCarousels();
    expect(first.querySelectorAll(".portrait-card")).toHaveLength(3);
    expect(second.querySelectorAll(".portrait-card")).toHaveLength(6);

    document.body.innerHTML = "";
    expect(() => initPortraitCardSetCarousels()).not.toThrow();
  });
});
