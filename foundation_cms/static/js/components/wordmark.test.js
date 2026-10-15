import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { initWordmarkHover } from "./wordmark.js";

const M_FILLS = ["#23A5E9", "#F06C13", "#EEC700"];

function wordmarkMarkup() {
  const mShapes = M_FILLS.map(
    (fill) =>
      `<path class="mzf-c-wordmark__shape mzf-c-wordmark__shape--m" data-wordmark-letter="0" fill="${fill}" d="M0 0h1v1z"/>`,
  ).join("");
  const letterShapes = [1, 2, 6, 8, 9, 10]
    .map(
      (letter) =>
        `<path class="mzf-c-wordmark__shape" data-wordmark-letter="${letter}" fill="#00A43D" d="M0 0h1v1z"/>`,
    )
    .join("");
  return `
    <a class="mzf-c-wordmark" href="/" aria-label="Mozilla Foundation, home">
      <svg class="mzf-c-wordmark__svg" viewBox="0 0 1380 115.06" aria-hidden="true">
        ${mShapes}${letterShapes}
        <g class="mzf-c-wordmark__ink"><path d="M0 0h1v1z"/></g>
      </svg>
    </a>
  `;
}

function mockReducedMotion(matches) {
  vi.stubGlobal(
    "matchMedia",
    vi.fn().mockReturnValue({ matches, addEventListener: vi.fn() }),
  );
}

describe("initWordmarkHover", () => {
  beforeEach(() => {
    document.body.innerHTML = wordmarkMarkup();
    // jsdom ships neither the Web Animations API nor matchMedia.
    Element.prototype.getAnimations = vi.fn().mockReturnValue([]);
    Element.prototype.animate = vi.fn().mockReturnValue({
      cancel: vi.fn(),
      finished: Promise.resolve(),
    });
  });

  afterEach(() => {
    delete Element.prototype.getAnimations;
    delete Element.prototype.animate;
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
  });

  it("shows every shape at once under reduced motion and keeps the M colours", () => {
    mockReducedMotion(true);
    initWordmarkHover();

    const wordmark = document.querySelector(".mzf-c-wordmark");
    wordmark.dispatchEvent(new Event("mouseenter"));

    const shapes = [...document.querySelectorAll(".mzf-c-wordmark__shape")];
    expect(shapes.every((shape) => shape.style.opacity === "1")).toBe(true);
    expect(Element.prototype.animate).not.toHaveBeenCalled();

    const mFills = [
      ...document.querySelectorAll(".mzf-c-wordmark__shape--m"),
    ].map((shape) => shape.getAttribute("fill"));
    expect(mFills).toEqual(M_FILLS);
  });

  it("gives neighbouring letters different colours", () => {
    mockReducedMotion(true);
    initWordmarkHover();

    document
      .querySelector(".mzf-c-wordmark")
      .dispatchEvent(new Event("mouseenter"));

    const byLetter = new Map(
      [
        ...document.querySelectorAll(
          ".mzf-c-wordmark__shape:not(.mzf-c-wordmark__shape--m)",
        ),
      ].map((shape) => [
        Number(shape.dataset.wordmarkLetter),
        shape.getAttribute("fill"),
      ]),
    );
    expect(byLetter.get(1)).not.toBe(byLetter.get(2));
    expect(byLetter.get(8)).not.toBe(byLetter.get(9));
    expect(byLetter.get(9)).not.toBe(byLetter.get(10));
    expect(M_FILLS).not.toContain(byLetter.get(1));
  });

  it("hides the shapes again when the pointer leaves under reduced motion", () => {
    mockReducedMotion(true);
    initWordmarkHover();

    const wordmark = document.querySelector(".mzf-c-wordmark");
    wordmark.dispatchEvent(new Event("mouseenter"));
    wordmark.dispatchEvent(new Event("mouseleave"));

    const shapes = [...document.querySelectorAll(".mzf-c-wordmark__shape")];
    expect(shapes.every((shape) => shape.style.opacity === "0")).toBe(true);
  });

  it("animates each shape in with the Web Animations API when motion is allowed", () => {
    mockReducedMotion(false);
    initWordmarkHover();

    document
      .querySelector(".mzf-c-wordmark")
      .dispatchEvent(new Event("mouseenter"));

    const shapeCount = document.querySelectorAll(
      ".mzf-c-wordmark__shape",
    ).length;
    expect(Element.prototype.animate).toHaveBeenCalledTimes(shapeCount);
    const [keyframes, options] = Element.prototype.animate.mock.calls[0];
    expect(keyframes[1]).toEqual({ opacity: 1, transform: "scale(1)" });
    expect(options.fill).toBe("forwards");
  });

  it("wires a wordmark only once", () => {
    mockReducedMotion(true);
    initWordmarkHover();
    initWordmarkHover();

    const wordmark = document.querySelector(".mzf-c-wordmark");
    const spy = vi.spyOn(wordmark, "addEventListener");
    initWordmarkHover();

    expect(spy).not.toHaveBeenCalled();
  });

  it("does nothing when there is no wordmark", () => {
    document.body.innerHTML = "";

    expect(() => initWordmarkHover()).not.toThrow();
  });
});
