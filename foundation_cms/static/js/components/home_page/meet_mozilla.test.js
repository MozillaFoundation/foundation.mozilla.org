import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import {
  getCurrentState,
  getFillProgress,
  getHeadingProgress,
  getPinnedState,
  getPinTop,
  initAllMeetMozilla,
  initMeetMozilla,
  setFill,
  setLength,
  setState,
  shouldPin,
  splitIntoWords,
} from "./meet_mozilla.js";

const VIEWPORT_HEIGHT = 1000;
// The intro heading's offset inside the sticky intro, so where it sits on screen.
const INTRO_HEADING_TOP = 371;
// Space above a statement inside its step: the big label plus the gap.
const STATEMENT_OFFSET = 41;
const PIN_TOP = INTRO_HEADING_TOP - STATEMENT_OFFSET;
// 35% of the viewport, then a 10% hold with the statement fully lit.
const FILL_DISTANCE = 350;
const HOLD_DISTANCE = 100;
// 20% of the viewport on mobile, so statements finish well before the site nav.
const STACKED_FILL_DISTANCE = 200;
// Color lines: LP's 80% when pinned, the middle when stacked.
const PINNED_COLOR_LINE = 800;
const STACKED_COLOR_LINE = 500;

let intersectionCallback;
let observer;
let animationFrames;
let prefersReducedMotion;

function rect(element, top) {
  element.getBoundingClientRect = () => ({ top });
}

function createSection({
  states = ["01", "02", "03", null],
  sticky = true,
  statement = null,
  heading = null,
} = {}) {
  const items = states
    .map(
      (state) => `
        <li class="mzf-c-meet-mozilla__item"${state ? ` data-mzf-meet-mozilla-state="${state}"` : ""}>
          <div class="mzf-c-biglabel-h2">
            <p class="mzf-c-big-label"></p>
            ${statement ? `<h3 class="mzf-c-meet-mozilla__statement">${statement}</h3>` : ""}
          </div>
        </li>
      `,
    )
    .join("");
  document.body.innerHTML = `
    <div class="mzf-c-meet-mozilla mzf-c-meet-mozilla--state-00" data-mzf-meet-mozilla>
      ${heading ? `<div class="mzf-c-text-group mzf-c-text-group--h1"><h2 class="mzf-c-text-group__heading">${heading}</h2></div>` : ""}
      <div class="mzf-c-meet-mozilla__aside" style="position: ${sticky ? "sticky" : "static"}">
        <div class="mzf-c-text-group">
          <h3 class="mzf-c-text-group__heading"></h3>
        </div>
      </div>
      <ol class="mzf-c-meet-mozilla__list">${items}</ol>
    </div>
  `;
  const root = document.querySelector("[data-mzf-meet-mozilla]");
  rect(root.querySelector(".mzf-c-meet-mozilla__aside"), 0);
  rect(root.querySelector(".mzf-c-text-group__heading"), INTRO_HEADING_TOP);
  const steps = [...root.querySelectorAll(".mzf-c-meet-mozilla__item")];
  return {
    root,
    steps,
    items: [...root.querySelectorAll("[data-mzf-meet-mozilla-state]")],
    statements: steps.map((step) =>
      step.querySelector(".mzf-c-meet-mozilla__statement"),
    ),
    heading: root.querySelector("h2"),
  };
}

// Places each step: its label (which drives the first color) and where its content
// would sit if it weren't pinned (which drives the pinned fill).
function placeSteps(steps, labelTops, contentTops = labelTops) {
  steps.forEach((step, index) => {
    rect(step.querySelector(".mzf-c-big-label"), labelTops[index]);
    rect(step, contentTops[index]);
    rect(step.querySelector(".mzf-c-biglabel-h2"), contentTops[index]);
    const statement = step.querySelector(".mzf-c-meet-mozilla__statement");
    if (statement) {
      rect(statement, contentTops[index] + STATEMENT_OFFSET);
    }
  });
}

function stateClasses(root) {
  return [...root.classList].filter((name) =>
    name.startsWith("mzf-c-meet-mozilla--state-"),
  );
}

function unreadWords(statement) {
  return [...statement.querySelectorAll("span")].map((word) =>
    word.classList.contains("mzf-c-meet-mozilla__unread"),
  );
}

function runAnimationFrames() {
  const frames = animationFrames;
  animationFrames = [];
  frames.forEach((callback) => callback());
}

function scroll() {
  window.dispatchEvent(new Event("scroll"));
  runAnimationFrames();
}

function startOnScreen(root) {
  initMeetMozilla(root);
  intersectionCallback([{ isIntersecting: true }]);
  runAnimationFrames();
}

describe("Meet Mozilla scroll behavior", () => {
  beforeEach(() => {
    animationFrames = [];
    prefersReducedMotion = false;
    vi.stubGlobal("innerHeight", VIEWPORT_HEIGHT);
    vi.stubGlobal(
      "matchMedia",
      vi.fn(() => ({ matches: prefersReducedMotion })),
    );
    vi.stubGlobal(
      "requestAnimationFrame",
      vi.fn((callback) => animationFrames.push(callback)),
    );
    observer = { observe: vi.fn() };
    vi.stubGlobal(
      "IntersectionObserver",
      vi.fn(function (callback) {
        intersectionCallback = callback;
        return observer;
      }),
    );
  });

  afterEach(() => {
    // Take the section off screen so its scroll listener doesn't leak into the next test.
    intersectionCallback?.([{ isIntersecting: false }]);
    intersectionCallback = undefined;
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
    document.body.innerHTML = "";
  });

  describe("shouldPin", () => {
    it("pins while the intro is sticky", () => {
      expect(shouldPin(createSection().root)).toBe(true);
    });

    it("doesn't pin when the layout stacks", () => {
      expect(shouldPin(createSection({ sticky: false }).root)).toBe(false);
    });
  });

  describe("getPinTop", () => {
    it("puts the statement level with the intro heading", () => {
      const { root, steps } = createSection({ statement: "one two" });
      placeSteps(steps, [900, 1600, 2300, 3000]);

      expect(
        getPinTop(root, steps[0].querySelector(".mzf-c-biglabel-h2")),
      ).toBe(PIN_TOP);
    });
  });

  describe("getCurrentState", () => {
    it("stays on the first state until a label reaches the line", () => {
      const { items } = createSection();
      placeSteps(items, [STACKED_COLOR_LINE + 1, 1500, 2200]);

      expect(getCurrentState(items, STACKED_COLOR_LINE)).toBe("00");
    });

    it("takes the state of the last label past the line", () => {
      const { items } = createSection();

      placeSteps(items, [STACKED_COLOR_LINE, 1500, 2200]);
      expect(getCurrentState(items, STACKED_COLOR_LINE)).toBe("01");

      placeSteps(items, [-900, -200, 300]);
      expect(getCurrentState(items, STACKED_COLOR_LINE)).toBe("03");
    });
  });

  describe("getPinnedState", () => {
    function pinnedSteps(firstLabelTop, done) {
      const label = document.createElement("p");
      rect(label, firstLabelTop);
      return done.map((isDone, index) => ({
        label,
        state: ["01", "02", "03", null][index],
        done: isDone,
      }));
    }

    it("brings the first color in at the line", () => {
      expect(
        getPinnedState(
          pinnedSteps(PINNED_COLOR_LINE + 1, [false, false, false, false]),
          PINNED_COLOR_LINE,
        ),
      ).toBe("00");
      expect(
        getPinnedState(
          pinnedSteps(PINNED_COLOR_LINE, [false, false, false, false]),
          PINNED_COLOR_LINE,
        ),
      ).toBe("01");
    });

    it("waits for the step before to be done", () => {
      expect(
        getPinnedState(
          pinnedSteps(0, [false, false, false, false]),
          PINNED_COLOR_LINE,
        ),
      ).toBe("01");
      expect(
        getPinnedState(
          pinnedSteps(0, [true, false, false, false]),
          PINNED_COLOR_LINE,
        ),
      ).toBe("02");
      expect(
        getPinnedState(
          pinnedSteps(0, [true, true, true, false]),
          PINNED_COLOR_LINE,
        ),
      ).toBe("03");
    });
  });

  describe("setState", () => {
    it("leaves exactly one state class on the section", () => {
      const { root } = createSection();
      root.classList.add("mzf-c-meet-mozilla--state-02");

      setState(root, "01");

      expect(stateClasses(root)).toEqual(["mzf-c-meet-mozilla--state-01"]);
    });
  });

  describe("splitIntoWords", () => {
    it("wraps each word in a span and keeps the text the same", () => {
      const statement = document.createElement("h3");
      statement.textContent = "We connect builders, dreamers.";

      const words = splitIntoWords(statement);

      expect(words.map((word) => word.textContent)).toEqual([
        "We",
        "connect",
        "builders,",
        "dreamers.",
      ]);
      expect(statement.textContent).toBe("We connect builders, dreamers.");
    });

    it("keeps editor text as text, not markup", () => {
      const statement = document.createElement("h3");
      statement.textContent = "Say <b>hi</b>";

      splitIntoWords(statement);

      expect(statement.querySelector("b")).toBeNull();
      expect(statement.textContent).toBe("Say <b>hi</b>");
    });
  });

  describe("getFillProgress", () => {
    it("is empty before the fill begins and full after the distance", () => {
      expect(getFillProgress(-10, FILL_DISTANCE)).toBe(0);
      expect(getFillProgress(0, FILL_DISTANCE)).toBe(0);
      expect(getFillProgress(FILL_DISTANCE / 2, FILL_DISTANCE)).toBeCloseTo(
        0.5,
      );
      expect(getFillProgress(FILL_DISTANCE, FILL_DISTANCE)).toBe(1);
      expect(getFillProgress(5000, FILL_DISTANCE)).toBe(1);
    });

    it("jumps from empty to full without a distance", () => {
      expect(getFillProgress(-1, 0)).toBe(0);
      expect(getFillProgress(0, 0)).toBe(1);
    });
  });

  describe("getHeadingProgress", () => {
    it("is empty until the heading is fully on screen", () => {
      expect(
        getHeadingProgress(
          VIEWPORT_HEIGHT + 1,
          2000,
          PINNED_COLOR_LINE,
          VIEWPORT_HEIGHT,
        ),
      ).toBe(0);
    });

    it("is full once the heading's bottom reaches the middle of the viewport", () => {
      // Halfway from the bottom of the viewport to the middle.
      expect(
        getHeadingProgress(750, 2000, PINNED_COLOR_LINE, VIEWPORT_HEIGHT),
      ).toBeCloseTo(0.5);
      expect(
        getHeadingProgress(500, 2000, PINNED_COLOR_LINE, VIEWPORT_HEIGHT),
      ).toBe(1);
    });

    it("is always full once the first color has arrived", () => {
      expect(
        getHeadingProgress(
          VIEWPORT_HEIGHT + 500,
          PINNED_COLOR_LINE,
          PINNED_COLOR_LINE,
          VIEWPORT_HEIGHT,
        ),
      ).toBe(1);
    });
  });

  describe("setFill", () => {
    it("lights the first share of words and dims the rest", () => {
      const statement = document.createElement("h3");
      statement.textContent = "one two three four";
      const words = splitIntoWords(statement);

      setFill(words, 0.5);
      expect(unreadWords(statement)).toEqual([false, false, true, true]);

      setFill(words, 1);
      expect(unreadWords(statement)).toEqual([false, false, false, false]);
    });
  });

  describe("setLength", () => {
    it("writes a changed length, skips an unchanged one, and clears with null", () => {
      const { root } = createSection();
      const setProperty = vi.spyOn(root.style, "setProperty");

      setLength(root, "--x", 10);
      setLength(root, "--x", 10);
      expect(setProperty).toHaveBeenCalledOnce();
      expect(root.style.getPropertyValue("--x")).toBe("10px");

      setLength(root, "--x", null);
      expect(root.style.getPropertyValue("--x")).toBe("");
    });
  });

  describe("initMeetMozilla on desktop", () => {
    it("pins the steps level with the intro heading for the fill and the hold", () => {
      const { root, steps } = createSection({ statement: "one two" });
      placeSteps(steps, [900, 1600, 2300, 3000]);

      startOnScreen(root);

      expect(root.classList).toContain("mzf-c-meet-mozilla--pinned");
      expect(root.style.getPropertyValue("--mzf-meet-mozilla-pin-top")).toBe(
        `${PIN_TOP}px`,
      );
      expect(
        root.style.getPropertyValue("--mzf-meet-mozilla-pin-distance"),
      ).toBe(`${FILL_DISTANCE + HOLD_DISTANCE}px`);
    });

    it("brings the first color in early, then fills each statement while pinned", () => {
      const { root, steps, statements } = createSection({
        statement: "one two three four",
      });
      placeSteps(steps, [900, 1600, 2300, 3000]);
      startOnScreen(root);

      // Step 1's label has passed LP's 80% line; its content hasn't reached the pin.
      placeSteps(steps, [700, 1400, 2100, 2800]);
      scroll();
      expect(stateClasses(root)).toEqual(["mzf-c-meet-mozilla--state-01"]);
      expect(unreadWords(statements[0])).toEqual([true, true, true, true]);

      // Step 1 is held at the pin, halfway through its room. Step 2 has come up past
      // the 80% line, but keeps waiting for step 1 to finish.
      placeSteps(
        steps,
        [PIN_TOP, 700, 1400, 2100],
        [PIN_TOP - FILL_DISTANCE / 2, 700, 1400, 2100],
      );
      scroll();
      expect(stateClasses(root)).toEqual(["mzf-c-meet-mozilla--state-01"]);
      expect(unreadWords(statements[0])).toEqual([false, false, true, true]);
      expect(unreadWords(statements[1])).toEqual([true, true, true, true]);

      // Step 1 is fully lit but still in its hold, so the color waits.
      placeSteps(
        steps,
        [PIN_TOP, 600, 1300, 2000],
        [PIN_TOP - FILL_DISTANCE - HOLD_DISTANCE / 2, 600, 1300, 2000],
      );
      scroll();
      expect(stateClasses(root)).toEqual(["mzf-c-meet-mozilla--state-01"]);
      expect(unreadWords(statements[0])).toEqual([false, false, false, false]);

      // The hold is over and step 1 moves on, so step 2's color takes over.
      placeSteps(
        steps,
        [PIN_TOP - 50, 550, 1250, 1950],
        [PIN_TOP - FILL_DISTANCE - HOLD_DISTANCE - 50, 550, 1250, 1950],
      );
      scroll();
      expect(stateClasses(root)).toEqual(["mzf-c-meet-mozilla--state-02"]);
      expect(unreadWords(statements[1])).toEqual([true, true, true, true]);
    });

    it("doesn't rewrite the pin lengths on frames where they don't change", () => {
      const { root, steps } = createSection({ statement: "one two" });
      placeSteps(steps, [900, 1600, 2300, 3000]);
      startOnScreen(root);
      const setProperty = vi.spyOn(root.style, "setProperty");

      placeSteps(steps, [800, 1500, 2200, 2900]);
      scroll();
      scroll();

      expect(setProperty).not.toHaveBeenCalled();
    });

    it("lights the section heading as it scrolls in", () => {
      const { root, steps, heading } = createSection({
        statement: "one",
        heading: "We back what others overlook.",
      });
      placeSteps(steps, [1900, 2600, 3300, 4000]);
      heading.getBoundingClientRect = () => ({ bottom: VIEWPORT_HEIGHT + 50 });
      startOnScreen(root);
      expect(unreadWords(heading)).toEqual([true, true, true, true, true]);

      // Fully on screen and halfway to the middle of the viewport.
      heading.getBoundingClientRect = () => ({ bottom: 750 });
      placeSteps(steps, [1650, 2350, 3050, 3750]);
      scroll();
      expect(unreadWords(heading)).toEqual([false, false, false, true, true]);

      heading.getBoundingClientRect = () => ({ bottom: 500 });
      placeSteps(steps, [1400, 2100, 2800, 3500]);
      scroll();
      expect(unreadWords(heading)).toEqual([false, false, false, false, false]);
    });

    it("sets the layout up before the reader scrolls", () => {
      const { root, steps } = createSection({ statement: "one two" });
      placeSteps(steps, [900, 1600, 2300, 3000]);

      initMeetMozilla(root);

      expect(root.classList).toContain("mzf-c-meet-mozilla--pinned");
    });
  });

  describe("initMeetMozilla when the layout stacks", () => {
    it("doesn't pin, and colors and fills from the middle of the viewport", () => {
      const { root, steps, statements } = createSection({
        sticky: false,
        statement: "one two three four",
      });
      placeSteps(steps, [900, 1600, 2300, 3000]);
      startOnScreen(root);

      placeSteps(steps, [
        STACKED_COLOR_LINE - STACKED_FILL_DISTANCE / 2,
        1000,
        1700,
        2400,
      ]);
      scroll();

      expect(root.classList).not.toContain("mzf-c-meet-mozilla--pinned");
      expect(root.style.getPropertyValue("--mzf-meet-mozilla-pin-top")).toBe(
        "",
      );
      expect(stateClasses(root)).toEqual(["mzf-c-meet-mozilla--state-01"]);
      expect(unreadWords(statements[0])).toEqual([false, false, true, true]);
    });

    it("finishes each statement 30% down the viewport, clear of the site nav", () => {
      const { root, steps, statements } = createSection({
        sticky: false,
        statement: "one two three four",
      });
      placeSteps(steps, [900, 1600, 2300, 3000]);
      startOnScreen(root);

      placeSteps(steps, [
        STACKED_COLOR_LINE - STACKED_FILL_DISTANCE,
        900,
        1600,
        2300,
      ]);
      scroll();

      expect(unreadWords(statements[0])).toEqual([false, false, false, false]);
    });
  });

  describe("initMeetMozilla in general", () => {
    it("listens to scroll only while the section is on screen", () => {
      const { root, items } = createSection({ sticky: false });
      const addListener = vi.spyOn(window, "addEventListener");
      const removeListener = vi.spyOn(window, "removeEventListener");
      initMeetMozilla(root);

      expect(observer.observe).toHaveBeenCalledWith(root);

      intersectionCallback([{ isIntersecting: true }]);
      expect(addListener).toHaveBeenCalledWith("scroll", expect.any(Function), {
        passive: true,
      });

      placeSteps(items, [-200, 300, 1500]);
      intersectionCallback([{ isIntersecting: false }]);
      expect(removeListener).toHaveBeenCalledWith(
        "scroll",
        addListener.mock.calls[0][1],
      );
      runAnimationFrames();
      expect(stateClasses(root)).toEqual(["mzf-c-meet-mozilla--state-02"]);
    });

    it("batches scroll events into one update per frame", () => {
      const { root, items } = createSection();
      placeSteps(items, [0, 1100, 1800]);
      startOnScreen(root);

      window.dispatchEvent(new Event("scroll"));
      window.dispatchEvent(new Event("scroll"));
      window.dispatchEvent(new Event("scroll"));

      expect(animationFrames).toHaveLength(1);
    });

    it("stands down with reduced motion, leaving the styles' static bands", () => {
      prefersReducedMotion = true;
      const { root, steps, statements, heading } = createSection({
        statement: "one two three",
        heading: "We back what others overlook.",
      });
      placeSteps(steps, [0, 0, 0, 0]);

      expect(initMeetMozilla(root)).toBeNull();
      expect(IntersectionObserver).not.toHaveBeenCalled();
      expect(root.classList).not.toContain("mzf-c-meet-mozilla--pinned");
      expect(stateClasses(root)).toEqual(["mzf-c-meet-mozilla--state-00"]);
      expect(statements[0].querySelector("span")).toBeNull();
      expect(statements[0].textContent).toBe("one two three");
      expect(heading.querySelector("span")).toBeNull();
    });

    it("does nothing without steps to watch", () => {
      const { root } = createSection({ states: [null, null] });

      expect(initMeetMozilla(root)).toBeNull();
      expect(IntersectionObserver).not.toHaveBeenCalled();
      expect(stateClasses(root)).toEqual(["mzf-c-meet-mozilla--state-00"]);
    });

    it("leaves everything as marked up where IntersectionObserver is missing", () => {
      vi.stubGlobal("IntersectionObserver", undefined);
      const { root, statements } = createSection({ statement: "one two" });

      expect(initMeetMozilla(root)).toBeNull();
      expect(stateClasses(root)).toEqual(["mzf-c-meet-mozilla--state-00"]);
      expect(statements[0].querySelector("span")).toBeNull();
    });
  });

  describe("initAllMeetMozilla", () => {
    it("starts every section on the page", () => {
      createSection();

      initAllMeetMozilla();

      expect(IntersectionObserver).toHaveBeenCalledOnce();
    });
  });
});
