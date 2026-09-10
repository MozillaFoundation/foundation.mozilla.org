import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { cancelTick, tick } from "./tick.js";

function createContext() {
  const track = document.createElement("div");
  Array.from({ length: 6 }, (_, index) => {
    const card = document.createElement("article");
    card.dataset.index = String(index);
    track.appendChild(card);
  });
  return {
    enabled: true,
    paused: false,
    rafId: null,
    lastTs: 100,
    pxPerSecond: 1000,
    _fractionalRemainder: 0,
    groupAdvance: 10,
    container: { scrollLeft: 0 },
    track,
    tick: vi.fn(),
    computeNextStartIndex: vi.fn(() => 0),
    appendCardsFromStart: vi.fn(),
    removeFirstGroup: vi.fn(),
  };
}

describe("product review carousel tick", () => {
  beforeEach(() => {
    vi.stubGlobal(
      "requestAnimationFrame",
      vi.fn(() => 11),
    );
    vi.stubGlobal("cancelAnimationFrame", vi.fn());
    vi.spyOn(performance, "now").mockReturnValue(120);
  });

  afterEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
  });

  it("does nothing when disabled and clears a paused frame", () => {
    const context = createContext();
    context.enabled = false;
    tick.call(context, 120);
    expect(requestAnimationFrame).not.toHaveBeenCalled();

    context.enabled = true;
    context.paused = true;
    context.rafId = 3;
    tick.call(context, 120);
    expect(context.rafId).toBeNull();
  });

  it("moves, recycles complete groups, and schedules the next frame", () => {
    const context = createContext();
    tick.call(context, 148);

    expect(context.appendCardsFromStart).toHaveBeenCalledTimes(4);
    expect(context.removeFirstGroup).toHaveBeenCalledTimes(4);
    expect(context.container.scrollLeft).toBe(8);
    expect(context.rafId).toBe(11);
    expect(requestAnimationFrame).toHaveBeenCalledWith(context.tick);
  });

  it("keeps subpixel movement in the track transform", () => {
    const context = createContext();
    context.pxPerSecond = 25;
    context.groupAdvance = 100;
    tick.call(context, 110);

    expect(context.container.scrollLeft).toBe(0);
    expect(context._fractionalRemainder).toBe(0.25);
    expect(context.track.style.transform).toBe("translate3d(-0.25px, 0, 0)");
  });

  it("cancels an active frame and resets timestamps", () => {
    const context = createContext();
    context.rafId = 9;
    cancelTick.call(context);
    expect(cancelAnimationFrame).toHaveBeenCalledWith(9);
    expect(context.rafId).toBeNull();
    expect(context.lastTs).toBeNull();

    cancelTick.call(context);
    expect(cancelAnimationFrame).toHaveBeenCalledOnce();
  });
});
