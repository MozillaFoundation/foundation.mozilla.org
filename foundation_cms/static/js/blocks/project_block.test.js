import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { initProjectBlocks } from "./project_block.js";

function createProjectBlock({ slides = 3 } = {}) {
  document.body.innerHTML = `
    <section data-project-block>
      <div data-project-block-viewport>
        <div data-project-block-track>
          ${Array.from(
            { length: slides },
            (_, index) => `
              <article data-project-block-slide>
                ${index === 0 ? "<video data-project-block-video></video>" : ""}
                <span>Slide ${index + 1}</span>
              </article>
            `,
          ).join("")}
        </div>
      </div>
      <div class="pagination-controls">
        <button data-direction="prev">Previous</button>
        <span data-active-index></span>
        <button data-direction="next">Next</button>
        ${Array.from(
          { length: slides },
          () => '<button class="carousel-indicators__item"></button>',
        ).join("")}
      </div>
      <button
        data-project-block-pause
        data-pause-label="Pause animation"
        data-play-label="Play animation"
      >
        <span data-project-block-pause-label></span>
      </button>
    </section>
  `;

  const root = document.querySelector("[data-project-block]");
  Object.defineProperty(
    root.querySelector("[data-project-block-viewport]"),
    "clientWidth",
    {
      value: 500,
    },
  );
  return root;
}

function touchEvent(type, clientX) {
  const event = new Event(type, { bubbles: true, cancelable: true });
  const points = [{ clientX }];
  Object.defineProperty(event, "touches", { value: points });
  Object.defineProperty(event, "changedTouches", { value: points });
  return event;
}

describe("project block", () => {
  let play;
  let pause;

  beforeEach(() => {
    vi.useFakeTimers();
    vi.stubGlobal(
      "requestAnimationFrame",
      vi.fn((callback) => callback()),
    );
    vi.stubGlobal(
      "DOMMatrix",
      class DOMMatrix {
        constructor() {
          this.m41 = -500;
        }
      },
    );
    play = vi
      .spyOn(HTMLMediaElement.prototype, "play")
      .mockResolvedValue(undefined);
    pause = vi
      .spyOn(HTMLMediaElement.prototype, "pause")
      .mockImplementation(() => {});
  });

  afterEach(() => {
    vi.useRealTimers();
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
    document.body.innerHTML = "";
  });

  it("initializes clones, controls, indicators, and active video state", () => {
    const root = createProjectBlock();

    initProjectBlocks();

    const trackSlides = root.querySelectorAll("[data-project-block-slide]");
    expect(trackSlides).toHaveLength(5);
    expect(trackSlides[0].dataset.projectBlockClone).toBe("true");
    expect(trackSlides[4].dataset.projectBlockClone).toBe("true");
    expect(trackSlides[1].classList.contains("is-active")).toBe(true);
    expect(trackSlides[1].getAttribute("aria-hidden")).toBe("false");
    expect(trackSlides[4].getAttribute("aria-hidden")).toBe("true");
    expect(
      root.querySelector("[data-project-block-track]").style.transform,
    ).toBe("translateX(-100%)");
    expect(root.querySelector("[data-active-index]").textContent).toBe("1");
    const firstIndicator = root.querySelector(".carousel-indicators__item");
    expect(firstIndicator.classList).toContain(
      "carousel-indicators__item--active",
    );
    expect(firstIndicator.getAttribute("aria-current")).toBe("true");
    expect(
      root.querySelector("[data-project-block-pause-label]").textContent,
    ).toBe("Pause animation");
    expect(play).toHaveBeenCalledOnce();
    expect(pause).toHaveBeenCalled();
  });

  it("navigates in both directions and normalizes cloned loop positions", () => {
    const root = createProjectBlock();
    initProjectBlocks();
    const track = root.querySelector("[data-project-block-track]");
    const counter = root.querySelector("[data-active-index]");

    root.querySelector("[data-direction='next']").click();
    expect(counter.textContent).toBe("2");
    expect(track.style.transform).toBe("translateX(-200%)");
    expect(pause).toHaveBeenCalled();

    root.querySelector("[data-direction='prev']").click();
    expect(counter.textContent).toBe("1");

    root.querySelector("[data-direction='prev']").click();
    expect(counter.textContent).toBe("3");
    expect(track.style.transform).toBe("translateX(-0%)");
    vi.advanceTimersByTime(300);
    expect(track.style.transform).toBe("translateX(-300%)");
    expect(track.style.transition).toBe("");

    root.querySelector("[data-direction='next']").click();
    expect(counter.textContent).toBe("1");
    expect(track.style.transform).toBe("translateX(-400%)");
    vi.advanceTimersByTime(300);
    expect(track.style.transform).toBe("translateX(-100%)");
  });

  it("supports touch swipes and snaps short gestures back", () => {
    const root = createProjectBlock();
    initProjectBlocks();
    const viewport = root.querySelector("[data-project-block-viewport]");
    const track = root.querySelector("[data-project-block-track]");

    viewport.dispatchEvent(touchEvent("touchstart", 100));
    const move = touchEvent("touchmove", 20);
    viewport.dispatchEvent(move);
    expect(move.defaultPrevented).toBe(true);
    expect(track.style.transform).toBe("translateX(-580px)");
    viewport.dispatchEvent(touchEvent("touchend", 20));
    expect(root.querySelector("[data-active-index]").textContent).toBe("2");

    viewport.dispatchEvent(touchEvent("touchstart", 100));
    const shortMove = touchEvent("touchmove", 80);
    viewport.dispatchEvent(shortMove);
    viewport.dispatchEvent(touchEvent("touchend", 80));
    expect(track.style.transform).toBe("translateX(-200%)");
    vi.advanceTimersByTime(300);
    expect(track.style.transition).toBe("");
  });

  it("supports mouse dragging and cancels when the pointer leaves", () => {
    const root = createProjectBlock();
    initProjectBlocks();
    const viewport = root.querySelector("[data-project-block-viewport]");
    const track = root.querySelector("[data-project-block-track]");

    viewport.dispatchEvent(
      new MouseEvent("mousemove", { bubbles: true, clientX: 40 }),
    );
    viewport.dispatchEvent(
      new MouseEvent("mouseup", { bubbles: true, clientX: 40 }),
    );
    expect(root.querySelector("[data-active-index]").textContent).toBe("1");

    viewport.dispatchEvent(
      new MouseEvent("mousedown", { bubbles: true, clientX: 100 }),
    );
    const move = new MouseEvent("mousemove", {
      bubbles: true,
      cancelable: true,
      clientX: 60,
    });
    viewport.dispatchEvent(move);
    expect(move.defaultPrevented).toBe(true);
    expect(track.style.transform).toBe("translateX(-540px)");

    viewport.dispatchEvent(new MouseEvent("mouseleave", { bubbles: true }));
    expect(track.style.transform).toBe("translateX(-100%)");
    vi.advanceTimersByTime(300);
    expect(track.style.transition).toBe("");
  });

  it("toggles playback and recovers when automatic playback is rejected", async () => {
    play.mockRejectedValueOnce(new Error("Playback blocked"));
    const root = createProjectBlock();
    initProjectBlocks();
    await Promise.resolve();
    const button = root.querySelector("[data-project-block-pause]");
    const label = root.querySelector("[data-project-block-pause-label]");
    const video = root.querySelector("video");

    expect(button.classList.contains("is-paused")).toBe(true);
    expect(label.textContent).toBe("Play animation");

    Object.defineProperty(video, "paused", {
      configurable: true,
      value: false,
    });
    button.click();
    expect(pause).toHaveBeenCalled();
    expect(button.classList.contains("is-paused")).toBe(true);
    expect(label.textContent).toBe("Play animation");

    Object.defineProperty(video, "paused", { configurable: true, value: true });
    button.click();
    expect(play).toHaveBeenCalledTimes(2);
    expect(button.classList.contains("is-paused")).toBe(false);
    expect(label.textContent).toBe("Pause animation");
  });

  it("disables carousel navigation for one slide and hides video controls", () => {
    const root = createProjectBlock({ slides: 1 });
    root.querySelector("video").remove();

    initProjectBlocks();
    const nextButton = root.querySelector("[data-direction='next']");
    const counter = root.querySelector("[data-active-index]");
    const track = root.querySelector("[data-project-block-track]");

    expect(root.querySelectorAll("[data-project-block-slide]")).toHaveLength(1);
    expect(root.querySelector("[data-direction='prev']").disabled).toBe(true);
    expect(nextButton.disabled).toBe(true);
    expect(
      root
        .querySelector("[data-project-block-pause]")
        .classList.contains("is-hidden"),
    ).toBe(true);
    const initialCounter = counter.textContent;
    const initialTransform = track.style.transform;

    nextButton.disabled = false;
    nextButton.click();
    root.querySelector("[data-project-block-pause]").click();

    expect(counter.textContent).toBe(initialCounter);
    expect(track.style.transform).toBe(initialTransform);
  });

  it("ignores incomplete and empty project block roots", () => {
    document.body.innerHTML = `
      <section data-project-block></section>
      <section data-project-block>
        <div data-project-block-viewport></div>
        <div data-project-block-track></div>
      </section>
    `;

    expect(() => initProjectBlocks()).not.toThrow();
  });
});
