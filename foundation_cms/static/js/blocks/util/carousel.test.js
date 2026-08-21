import { afterEach, describe, expect, it, vi } from "vitest";
import {
  RESIZE_DEBOUNCE_MS,
  SWIPE_THRESHOLD,
  debounce,
  getLogicalIndex,
  tripleCards,
  updateIndicators,
} from "./carousel.js";

describe("carousel utilities", () => {
  afterEach(() => {
    vi.useRealTimers();
  });

  it("exports the shared interaction timings", () => {
    expect(SWIPE_THRESHOLD).toBe(50);
    expect(RESIZE_DEBOUNCE_MS).toBe(200);
  });

  it.each([
    [0, 3, 0],
    [4, 3, 1],
    [-1, 3, 2],
    [-4, 3, 2],
  ])(
    "maps track index %s into a %s-item carousel",
    (index, total, expected) => {
      expect(getLogicalIndex(index, total)).toBe(expected);
    },
  );

  it("triples cards while retaining the originals in the middle set", () => {
    const cards = ["One", "Two"].map((label) => {
      const card = document.createElement("article");
      card.textContent = label;
      return card;
    });

    const nodes = Array.from(tripleCards(cards).childNodes);

    expect(nodes).toHaveLength(6);
    expect(nodes.map((node) => node.textContent)).toEqual([
      "One",
      "Two",
      "One",
      "Two",
      "One",
      "Two",
    ]);
    expect(nodes[2]).toBe(cards[0]);
    expect(nodes[3]).toBe(cards[1]);
    expect(nodes[0]).not.toBe(cards[0]);
    expect(nodes[4]).not.toBe(cards[0]);
  });

  it("updates indicator classes and aria state", () => {
    const root = document.createElement("div");
    root.innerHTML = `
      <button class="carousel-indicators__item carousel-indicators__item--active"></button>
      <button class="carousel-indicators__item"></button>
      <button class="carousel-indicators__item"></button>
    `;

    updateIndicators(root, 1);

    const indicators = root.querySelectorAll(".carousel-indicators__item");
    expect(indicators[0].classList).not.toContain(
      "carousel-indicators__item--active",
    );
    expect(indicators[0].getAttribute("aria-current")).toBe("false");
    expect(indicators[1].classList).toContain(
      "carousel-indicators__item--active",
    );
    expect(indicators[1].getAttribute("aria-current")).toBe("true");
    expect(indicators[2].getAttribute("aria-current")).toBe("false");
  });

  it("debounces calls and forwards the latest arguments", () => {
    vi.useFakeTimers();
    const callback = vi.fn();
    const debounced = debounce(callback, 100);

    debounced("first");
    vi.advanceTimersByTime(50);
    debounced("latest", 2);
    vi.advanceTimersByTime(99);

    expect(callback).not.toHaveBeenCalled();

    vi.advanceTimersByTime(1);

    expect(callback).toHaveBeenCalledOnce();
    expect(callback).toHaveBeenCalledWith("latest", 2);
  });
});
