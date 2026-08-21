import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import {
  initTabbedContent,
  initTabbedContentCardSets,
} from "./tabbed_content_container.js";

function createTouchEvent(type, clientX) {
  const event = new Event(type);
  const touchList = [{ clientX }];
  Object.defineProperty(
    event,
    type === "touchstart" ? "touches" : "changedTouches",
    {
      value: touchList,
    },
  );
  return event;
}

function createCardSet({ cards = 5, cardsPerPage = 2 } = {}) {
  document.body.innerHTML = `
    <div
      class="tabbed-content-container__tab-panel"
      data-cards-per-page="${cardsPerPage}"
      style="gap: 10px"
    >
      ${Array.from(
        { length: cards },
        (_, index) => `<article class="tab-card">Card ${index + 1}</article>`,
      ).join("")}
      ${Array.from(
        { length: Math.ceil(cards / cardsPerPage) },
        () => '<button class="carousel-indicators__item"></button>',
      ).join("")}
    </div>
  `;

  return document.querySelector(".tabbed-content-container__tab-panel");
}

describe("tabbed content", () => {
  beforeEach(() => {
    HTMLElement.prototype.scrollIntoView = vi.fn();
    HTMLElement.prototype.scrollTo = vi.fn();
    vi.spyOn(HTMLElement.prototype, "clientWidth", "get").mockImplementation(
      function getClientWidth() {
        return this.classList.contains("tab-card__page") ? 100 : 0;
      },
    );
  });

  afterEach(() => {
    vi.restoreAllMocks();
    delete HTMLElement.prototype.scrollIntoView;
    delete HTMLElement.prototype.scrollTo;
    document.body.innerHTML = "";
  });

  it("switches the active tab and matching panel within its container", () => {
    document.body.innerHTML = `
      <section class="tabbed-content-container">
        <button class="tabbed-content-container__tab-button is-active">One</button>
        <button class="tabbed-content-container__tab-button">Two</button>
        <div class="tabbed-content-container__tab-panel is-active">First panel</div>
        <div class="tabbed-content-container__tab-panel">Second panel</div>
      </section>
    `;
    const buttons = document.querySelectorAll(
      ".tabbed-content-container__tab-button",
    );
    const panels = document.querySelectorAll(
      ".tabbed-content-container__tab-panel",
    );

    initTabbedContent();
    buttons[1].click();

    expect(buttons[0].classList).not.toContain("is-active");
    expect(buttons[1].classList).toContain("is-active");
    expect(panels[0].classList).not.toContain("is-active");
    expect(panels[1].classList).toContain("is-active");
    expect(buttons[1].scrollIntoView).toHaveBeenCalledWith({
      behavior: "smooth",
      block: "nearest",
      inline: "start",
    });
  });

  it("wraps cards into pages and updates indicators while scrolling", () => {
    const panel = createCardSet();
    Object.defineProperty(panel, "scrollLeft", {
      configurable: true,
      writable: true,
      value: 110,
    });

    initTabbedContentCardSets();

    const pages = panel.querySelectorAll(".tab-card__page");
    const indicators = panel.querySelectorAll(".carousel-indicators__item");
    expect(pages).toHaveLength(3);
    expect(Array.from(pages, (page) => page.children.length)).toEqual([
      2, 2, 1,
    ]);
    expect(indicators[1].getAttribute("aria-current")).toBe("true");

    panel.scrollLeft = 220;
    panel.dispatchEvent(new Event("scroll"));

    expect(indicators[2].getAttribute("aria-current")).toBe("true");
    expect(indicators[1].getAttribute("aria-current")).toBe("false");
  });

  it("does not add carousel interactions when all cards fit on one page", () => {
    const panel = createCardSet({ cards: 2, cardsPerPage: 3 });

    initTabbedContentCardSets();
    panel.dispatchEvent(createTouchEvent("touchstart", 100));
    panel.dispatchEvent(createTouchEvent("touchend", 0));

    expect(panel.querySelectorAll(".tab-card__page")).toHaveLength(1);
    expect(panel.scrollTo).not.toHaveBeenCalled();
  });

  it("moves between card pages only for swipes beyond the threshold", () => {
    const panel = createCardSet();
    Object.defineProperty(panel, "scrollLeft", {
      configurable: true,
      writable: true,
      value: 110,
    });
    initTabbedContentCardSets();

    panel.dispatchEvent(createTouchEvent("touchstart", 100));
    panel.dispatchEvent(createTouchEvent("touchend", 51));
    expect(panel.scrollTo).not.toHaveBeenCalled();

    panel.dispatchEvent(createTouchEvent("touchstart", 100));
    panel.dispatchEvent(createTouchEvent("touchend", 40));
    expect(panel.scrollTo).toHaveBeenLastCalledWith({
      behavior: "smooth",
      left: 220,
    });

    panel.scrollLeft = 110;
    panel.dispatchEvent(createTouchEvent("touchstart", 40));
    panel.dispatchEvent(createTouchEvent("touchend", 100));
    expect(panel.scrollTo).toHaveBeenLastCalledWith({
      behavior: "smooth",
      left: 0,
    });
  });

  it("keeps swipes within the first and last page boundaries", () => {
    const panel = createCardSet();
    Object.defineProperty(panel, "scrollLeft", {
      configurable: true,
      writable: true,
      value: 0,
    });
    initTabbedContentCardSets();

    panel.dispatchEvent(createTouchEvent("touchstart", 40));
    panel.dispatchEvent(createTouchEvent("touchend", 100));

    panel.scrollLeft = 220;
    panel.dispatchEvent(createTouchEvent("touchstart", 100));
    panel.dispatchEvent(createTouchEvent("touchend", 40));

    expect(panel.scrollTo).not.toHaveBeenCalled();
  });
});
