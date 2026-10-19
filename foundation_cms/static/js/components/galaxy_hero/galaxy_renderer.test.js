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
});
