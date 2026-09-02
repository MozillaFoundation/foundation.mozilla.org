import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import {
  isElementHorizontallyVisible,
  makeTemporarilyUntabbable,
  refreshVisibleCardFocus,
  resetCardFocusability,
  restoreOriginalTabIndex,
  updateWrapperFocusability,
} from "./a11y.js";

function createTrack() {
  document.body.innerHTML = `
    <div class="viewport">
      <div class="track">
        <article class="product-review-carousel__card-wrapper">
          <a href="#one">One</a>
          <button tabindex="2">Action</button>
        </article>
        <article class="product-review-carousel__card-wrapper">
          <a href="#two">Two</a>
        </article>
      </div>
    </div>
  `;
  return {
    container: document.querySelector(".viewport"),
    track: document.querySelector(".track"),
    wrappers: document.querySelectorAll(
      ".product-review-carousel__card-wrapper",
    ),
  };
}

describe("product review carousel accessibility", () => {
  beforeEach(() => {
    vi.spyOn(performance, "now").mockReturnValue(1000);
  });

  afterEach(() => {
    vi.restoreAllMocks();
    document.body.innerHTML = "";
  });

  it("detects meaningful horizontal overlap", () => {
    const element = document.createElement("div");
    const rectSpy = vi.spyOn(element, "getBoundingClientRect");
    const containerRect = { left: 10, right: 110 };
    rectSpy.mockReturnValue({ left: 109, right: 150 });
    expect(isElementHorizontallyVisible(element, containerRect)).toBe(false);
    rectSpy.mockReturnValue({ left: 108, right: 150 });
    expect(isElementHorizontallyVisible(element, containerRect)).toBe(true);
  });

  it("temporarily removes and restores original tab index state", () => {
    const link = document.createElement("a");
    const button = document.createElement("button");
    button.setAttribute("tabindex", "3");

    makeTemporarilyUntabbable(link);
    makeTemporarilyUntabbable(link);
    makeTemporarilyUntabbable(button);

    expect(link.getAttribute("tabindex")).toBe("-1");
    expect(link.dataset.carouselOriginalTabindex).toBe("__none__");
    expect(button.dataset.carouselOriginalTabindex).toBe("3");

    restoreOriginalTabIndex(link);
    restoreOriginalTabIndex(button);

    expect(link.hasAttribute("tabindex")).toBe(false);
    expect(button.getAttribute("tabindex")).toBe("3");
    expect(link.hasAttribute("data-carousel-managed-tabindex")).toBe(false);
  });

  it("toggles wrapper accessibility and descendant focusability", () => {
    const { wrappers } = createTrack();
    const context = {
      makeTemporarilyUntabbable,
      restoreOriginalTabIndex,
    };

    updateWrapperFocusability.call(context, wrappers[0], false);
    expect(wrappers[0].getAttribute("aria-hidden")).toBe("true");
    expect(wrappers[0].querySelector("a").tabIndex).toBe(-1);

    updateWrapperFocusability.call(context, wrappers[0], true);
    expect(wrappers[0].getAttribute("aria-hidden")).toBe("false");
    expect(wrappers[0].querySelector("a").hasAttribute("tabindex")).toBe(false);
    expect(wrappers[0].querySelector("button").tabIndex).toBe(2);
  });

  it("refreshes visible cards and throttles repeated layout work", () => {
    const { container, track, wrappers } = createTrack();
    vi.spyOn(container, "getBoundingClientRect").mockReturnValue({
      left: 0,
      right: 100,
    });
    const context = {
      container,
      track,
      enabled: true,
      _lastFocusRefreshTs: null,
      isElementHorizontallyVisible: vi
        .fn()
        .mockReturnValueOnce(true)
        .mockReturnValueOnce(false),
      updateWrapperFocusability: vi.fn(),
      resetCardFocusability: vi.fn(),
    };

    refreshVisibleCardFocus.call(context);
    refreshVisibleCardFocus.call(context);

    expect(context.updateWrapperFocusability.mock.calls).toEqual([
      [wrappers[0], true],
      [wrappers[1], false],
    ]);
    expect(context.isElementHorizontallyVisible).toHaveBeenCalledTimes(2);
  });

  it("resets focusability when disabled and tolerates missing DOM", () => {
    const { track } = createTrack();
    const updateWrapperFocusabilitySpy = vi.fn();
    const context = {
      container: document.querySelector(".viewport"),
      track,
      enabled: false,
      _lastFocusRefreshTs: null,
      resetCardFocusability: vi.fn(),
    };

    refreshVisibleCardFocus.call(context, true);
    resetCardFocusability.call({
      track,
      updateWrapperFocusability: updateWrapperFocusabilitySpy,
    });
    refreshVisibleCardFocus.call({}, true);
    resetCardFocusability.call({});

    expect(context.resetCardFocusability).toHaveBeenCalledOnce();
    expect(updateWrapperFocusabilitySpy).toHaveBeenCalledTimes(2);
  });
});
