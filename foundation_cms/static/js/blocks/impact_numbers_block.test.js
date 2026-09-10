import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { initImpactNumberStatAnimationsOnScroll } from "./impact_numbers_block.js";

let intersectionCallback;
let observer;
let animationFrames;
let prefersReducedMotion;

function createStats(values) {
  document.body.innerHTML = values
    .map(
      ({ finalValue, text = finalValue, withValue = true }) => `
        <div class="impact-stat__number">
          ${
            withValue
              ? `<span data-impact-stat-count-up data-final-value="${finalValue}">${text}</span>`
              : ""
          }
        </div>
      `,
    )
    .join("");

  return document.querySelectorAll(".impact-stat__number");
}

function enterViewport(target, isIntersecting = true) {
  intersectionCallback([{ isIntersecting, target }], observer);
}

describe("impact number stat animations", () => {
  beforeEach(() => {
    animationFrames = [];
    prefersReducedMotion = false;
    observer = {
      observe: vi.fn(),
      unobserve: vi.fn(),
    };
    vi.stubGlobal(
      "IntersectionObserver",
      vi.fn((callback, options) => {
        intersectionCallback = callback;
        observer.options = options;
        return observer;
      }),
    );
    vi.stubGlobal(
      "matchMedia",
      vi.fn(() => ({ matches: prefersReducedMotion })),
    );
    vi.stubGlobal(
      "requestAnimationFrame",
      vi.fn((callback) => {
        animationFrames.push(callback);
        return animationFrames.length;
      }),
    );
    vi.spyOn(window.performance, "now").mockReturnValue(1000);
  });

  afterEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
    document.body.innerHTML = "";
  });

  it("observes valid stats at the configured threshold and formats their zero state", () => {
    const containers = createStats([
      { finalValue: "$10M" },
      { finalValue: "+ de 2 000" },
      { finalValue: "1,234.50 people" },
    ]);

    initImpactNumberStatAnimationsOnScroll();

    expect(IntersectionObserver).toHaveBeenCalledOnce();
    expect(observer.options).toEqual({ threshold: 0.4 });
    expect(observer.observe.mock.calls.map(([container]) => container)).toEqual(
      Array.from(containers),
    );
    expect(containers[0].textContent.trim()).toBe("$0M");
    expect(containers[1].textContent.trim()).toBe("+ de 0");
    expect(containers[2].textContent.trim()).toBe("0.00 people");
  });

  it("skips missing and non-numeric stat values", () => {
    createStats([
      { finalValue: "not a number" },
      { finalValue: "", withValue: false },
    ]);

    initImpactNumberStatAnimationsOnScroll();

    expect(observer.observe).not.toHaveBeenCalled();
  });

  it("shows the final value immediately when reduced motion is preferred", () => {
    prefersReducedMotion = true;
    const [container] = createStats([{ finalValue: "+ de 2 000" }]);
    const valueElement = container.querySelector("[data-impact-stat-count-up]");
    initImpactNumberStatAnimationsOnScroll();

    enterViewport(container);

    expect(matchMedia).toHaveBeenCalledWith("(prefers-reduced-motion: reduce)");
    expect(valueElement.textContent).toBe("+ de 2 000");
    expect(valueElement.dataset.animationComplete).toBe("true");
    expect(requestAnimationFrame).not.toHaveBeenCalled();
    expect(observer.unobserve).toHaveBeenCalledWith(container);
  });

  it("animates a stat to its exact final value over requestAnimationFrame", () => {
    const [container] = createStats([{ finalValue: "1,000" }]);
    const valueElement = container.querySelector("[data-impact-stat-count-up]");
    initImpactNumberStatAnimationsOnScroll();

    enterViewport(container);
    expect(animationFrames).toHaveLength(1);

    animationFrames.shift()(1000);
    expect(valueElement.textContent).toBe("0");

    animationFrames.shift()(2000);
    expect(valueElement.textContent).toBe("875");

    animationFrames.shift()(3000);
    expect(valueElement.textContent).toBe("1,000");
    expect(animationFrames).toHaveLength(0);
    expect(valueElement.dataset.animationComplete).toBe("true");
    expect(observer.unobserve).toHaveBeenCalledWith(container);
  });

  it("preserves decimal precision during animation", () => {
    const [container] = createStats([{ finalValue: "2.50%" }]);
    const valueElement = container.querySelector("[data-impact-stat-count-up]");
    initImpactNumberStatAnimationsOnScroll();

    enterViewport(container);
    animationFrames.shift()(2000);

    expect(valueElement.textContent).toBe("2.19%");
  });

  it("ignores entries outside the viewport", () => {
    const [container] = createStats([{ finalValue: "10" }]);
    initImpactNumberStatAnimationsOnScroll();

    enterViewport(container, false);

    expect(requestAnimationFrame).not.toHaveBeenCalled();
    expect(observer.unobserve).not.toHaveBeenCalled();
  });

  it("unobserves values that are already complete or become invalid", () => {
    const containers = createStats([
      { finalValue: "10" },
      { finalValue: "20" },
      { finalValue: "30" },
    ]);
    const completedValue = containers[0].querySelector(
      "[data-impact-stat-count-up]",
    );
    completedValue.dataset.animationComplete = "true";
    const invalidValue = containers[1].querySelector(
      "[data-impact-stat-count-up]",
    );
    invalidValue.dataset.finalValue = "invalid";
    containers[2].querySelector("[data-impact-stat-count-up]").remove();
    initImpactNumberStatAnimationsOnScroll();

    containers.forEach((container) => enterViewport(container));

    expect(
      observer.unobserve.mock.calls.map(([container]) => container),
    ).toEqual(Array.from(containers));
    expect(requestAnimationFrame).not.toHaveBeenCalled();
  });
});
