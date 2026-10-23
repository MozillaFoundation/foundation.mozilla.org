import { describe, expect, it, vi } from "vitest";
import { createGalaxyRenderer } from "./galaxy_renderer.js";

const colors = {
  "--color-gray-100": "#F7F7F7",
  "--color-text-default": "#161616",
  "--color-text-inverse": "#FFFFFF",
  "--color-accent-blue": "#23A5E9",
  "--color-accent-orange": "#F06C13",
  "--color-spectrum-yellow-600": "#EEC700",
  "--color-spectrum-cyan": "#55D9E0",
  "--color-spectrum-apricot": "#FFA77F",
  "--color-spectrum-crimson": "#E6323B",
  "--color-card-pink": "#EBA0CD",
  "--color-card-lime": "#ACEE48",
};
function fixture(background = "Gray") {
  const context = {
    rect: vi.fn(),
    clip: vi.fn(),
    save: vi.fn(),
    restore: vi.fn(),
    setTransform: vi.fn(),
    translate: vi.fn(),
    scale: vi.fn(),
    fill: vi.fn(),
    beginPath: vi.fn(),
    moveTo: vi.fn(),
    lineTo: vi.fn(),
    closePath: vi.fn(),
    fillRect: vi.fn(),
    fillText: vi.fn(),
    measureText: (text) => ({ width: text.length * 20 }),
  };
  const canvas = { getContext: () => context };
  return {
    context,
    renderer: createGalaxyRenderer(canvas, {
      headline: "First headline",
      secondHeadline: "Second headline",
      background,
      colors,
    }),
  };
}

describe("Galaxy renderer", () => {
  it.each(["Gray", "Orange", "Yellow", "Blue"])(
    "resolves both reduced-motion beats and reverses on %s",
    (background) => {
      const { context, renderer } = fixture(background);
      renderer.resize(1440, 812, 2);
      renderer.draw(0, 0, true);
      expect(
        context.fillText.mock.calls.some(([word]) => word === "First"),
      ).toBe(true);
      context.fillText.mockClear();
      renderer.draw(1, 0, true);
      expect(
        context.fillText.mock.calls.some(([word]) => word === "Second"),
      ).toBe(true);
      expect(context.fillRect.mock.calls.length).toBeGreaterThan(10);
      context.fillText.mockClear();
      renderer.draw(0, 0, true);
      expect(
        context.fillText.mock.calls.some(([word]) => word === "First"),
      ).toBe(true);
    },
  );

  it("remains finite through mobile resize and motion preference changes", () => {
    const { context, renderer } = fixture();
    renderer.resize(390, 660, 2);
    renderer.draw(1, 0, true);
    for (let ms = 0; ms < 5000; ms += 16) renderer.draw(1, ms, false);
    renderer.resize(1440, 812, 1);
    renderer.draw(1, 5016, false);
    for (const call of context.fillRect.mock.calls)
      expect(call.every(Number.isFinite)).toBe(true);
    expect(
      context.fillText.mock.calls.some(([word]) => word === "Second"),
    ).toBe(true);
  });

  it.each(["Gray", "Orange", "Yellow", "Blue"])(
    "finishes the %s reveal within its scroll range under fast scrolling, then reverses",
    (background) => {
      const { context, renderer } = fixture(background);
      renderer.resize(1440, 852, 1);
      let ms = 0;
      const scroll = (from, to, frames) => {
        for (let frame = 1; frame <= frames; frame++, ms += 16)
          renderer.draw(from + ((to - from) * frame) / frames, ms, false);
      };
      scroll(0, 0, 120); // entrance
      // About 1700px of a 2156px sticky travel in half a second.
      scroll(0, 0.8, 30);
      context.fillText.mockClear();
      context.fillRect.mockClear();
      renderer.draw(0.8, ms, false);
      const words = context.fillText.mock.calls.map(([word]) => word);
      expect(words).toContain("Second");
      expect(words).toContain("headline");
      expect(context.fillRect.mock.calls.length).toBeGreaterThan(10);

      scroll(0.8, 0, 30);
      scroll(0, 0, 60);
      context.fillText.mockClear();
      renderer.draw(0, ms, false);
      const reversed = context.fillText.mock.calls.map(([word]) => word);
      expect(reversed).toContain("First");
      expect(reversed).not.toContain("Second");
    },
  );

  it("keeps LP's wall-clock reveal when scrolling stops after convergence", () => {
    const { context, renderer } = fixture();
    renderer.resize(1440, 852, 1);
    let ms = 0;
    for (let frame = 0; frame < 120; frame++, ms += 16)
      renderer.draw(0, ms, false);
    for (let frame = 1; frame <= 60; frame++, ms += 16)
      renderer.draw((0.41 * frame) / 60, ms, false);
    context.fillText.mockClear();
    for (let frame = 0; frame < 30; frame++, ms += 16)
      renderer.draw(0.41, ms, false);
    expect(
      context.fillText.mock.calls.some(([word]) => word === "Second"),
    ).toBe(false);
    for (let frame = 0; frame < 240; frame++, ms += 16)
      renderer.draw(0.41, ms, false);
    expect(
      context.fillText.mock.calls.some(([word]) => word === "Second"),
    ).toBe(true);
  });

  it("keeps a visible headline on screen through a long frame", () => {
    const { context, renderer } = fixture();
    const drawn = [];
    context.fillText.mockImplementation((word) =>
      drawn.push([word, context.globalAlpha]),
    );
    renderer.resize(1440, 852, 1);
    let ms = 0;
    for (let frame = 0; frame < 120; frame++, ms += 16)
      renderer.draw(0, ms, false);
    drawn.length = 0;
    renderer.draw(0, ms + 400, false);
    expect(drawn.find(([word]) => word === "First")?.[1]).toBeGreaterThan(0.99);
  });
});
