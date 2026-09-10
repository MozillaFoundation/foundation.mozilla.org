import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import {
  onFocusIn,
  onFocusOut,
  onKeyDown,
  onMouseOut,
  onMouseOver,
  onPauseToggle,
  onVisibilityChange,
  updateButtonUI,
  updatePaused,
} from "./handlers.js";

function createContext() {
  document.body.innerHTML = `
    <section class="root">
      <div class="container">
        <article class="product-review-card"><button>Card</button></article>
        <article class="product-review-card"><a href="#two">Two</a></article>
      </div>
      <button class="pause"></button>
    </section>
  `;
  return {
    root: document.querySelector(".root"),
    container: document.querySelector(".container"),
    pauseBtn: document.querySelector(".pause"),
    track: document.createElement("div"),
    tick: vi.fn(),
    updatePaused: vi.fn(),
    updateButtonUI: vi.fn(),
    refreshVisibleCardFocus: vi.fn(),
    resetCardFocusability: vi.fn(),
    enabled: true,
    paused: false,
    userPaused: false,
    hovered: false,
    focusWithin: false,
    _offscreen: false,
    rafId: null,
    lastTs: 1,
  };
}

describe("product review carousel handlers", () => {
  beforeEach(() => {
    vi.stubGlobal(
      "gettext",
      vi.fn((message) => message),
    );
    vi.stubGlobal(
      "requestAnimationFrame",
      vi.fn(() => 7),
    );
    vi.stubGlobal("cancelAnimationFrame", vi.fn());
  });

  afterEach(() => {
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
    document.body.innerHTML = "";
  });

  it("toggles the user pause state and button UI", () => {
    const context = createContext();
    onPauseToggle.call(context);
    expect(context.userPaused).toBe(true);
    expect(context.updatePaused).toHaveBeenCalledOnce();
    expect(context.updateButtonUI).toHaveBeenCalledOnce();

    updateButtonUI.call(context);
    expect(context.pauseBtn.getAttribute("aria-pressed")).toBe("true");
    expect(context.pauseBtn.getAttribute("aria-label")).toBe("Play carousel");
    expect(context.pauseBtn.classList).toContain("is-paused");

    context.userPaused = false;
    updateButtonUI.call(context);
    expect(context.pauseBtn.getAttribute("aria-label")).toBe("Pause carousel");
    expect(updateButtonUI.call({ pauseBtn: null })).toBeUndefined();
  });

  it("stops and restarts animation as effective pause state changes", () => {
    const context = createContext();
    context.rafId = 5;
    context.hovered = true;

    updatePaused.call(context);
    expect(context.paused).toBe(true);
    expect(cancelAnimationFrame).toHaveBeenCalledWith(5);
    expect(context.rafId).toBeNull();
    expect(context.track.style.willChange).toBe("auto");

    context.hovered = false;
    updatePaused.call(context);
    expect(context.paused).toBe(false);
    expect(context.rafId).toBe(7);
    expect(context.track.style.willChange).toBe("transform");

    updatePaused.call(context);
    expect(requestAnimationFrame).toHaveBeenCalledOnce();
  });

  it("pauses over cards and resumes only after leaving all cards", () => {
    const context = createContext();
    const cards = context.container.querySelectorAll(".product-review-card");

    onMouseOver.call(context, { target: cards[0].querySelector("button") });
    expect(context.hovered).toBe(true);

    onMouseOut.call(context, {
      target: cards[0],
      relatedTarget: cards[1].querySelector("a"),
    });
    expect(context.hovered).toBe(true);

    onMouseOut.call(context, { target: cards[1], relatedTarget: null });
    expect(context.hovered).toBe(false);
    expect(context.updatePaused).toHaveBeenCalledTimes(2);
  });

  it("tracks focus, visibility, and Tab navigation", () => {
    const context = createContext();
    const inside = context.root.querySelector("button");

    onFocusIn.call(context);
    onFocusIn.call(context);
    onKeyDown.call(context, { key: "Tab" });
    onKeyDown.call(context, { key: "Enter" });
    onFocusOut.call(context, { relatedTarget: inside });
    expect(context.focusWithin).toBe(true);

    onFocusOut.call(context, { relatedTarget: null });
    onVisibilityChange.call(context);

    expect(context.focusWithin).toBe(false);
    expect(context.refreshVisibleCardFocus).toHaveBeenCalledTimes(2);
    expect(context.resetCardFocusability).toHaveBeenCalledOnce();
    expect(context.updatePaused).toHaveBeenCalledTimes(3);
  });
});
