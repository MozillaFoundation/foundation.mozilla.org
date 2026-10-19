import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import {
  getCurrentState,
  getReadingLine,
  initAllMeetMozilla,
  initMeetMozilla,
  setState,
} from "./meet_mozilla.js";

const VIEWPORT_HEIGHT = 1000;
const INTRO_TOP = 371;

let intersectionCallback;
let observer;
let animationFrames;

function createSection({
  states = ["01", "02", "03", null],
  sticky = true,
} = {}) {
  const items = states
    .map(
      (state) => `
        <li class="mzf-c-meet-mozilla__item"${state ? ` data-mzf-meet-mozilla-state="${state}"` : ""}>
          <p class="mzf-c-big-label"></p>
        </li>
      `,
    )
    .join("");
  document.body.innerHTML = `
    <div class="mzf-c-meet-mozilla mzf-c-meet-mozilla--state-00" data-mzf-meet-mozilla>
      <div class="mzf-c-meet-mozilla__aside" style="position: ${sticky ? "sticky" : "static"}">
        <div class="mzf-c-text-group"></div>
      </div>
      <ol class="mzf-c-meet-mozilla__list">${items}</ol>
    </div>
  `;
  const root = document.querySelector("[data-mzf-meet-mozilla]");
  root.querySelector(".mzf-c-text-group").getBoundingClientRect = () => ({
    top: INTRO_TOP,
  });
  return {
    root,
    items: [...root.querySelectorAll("[data-mzf-meet-mozilla-state]")],
  };
}

function placeLabels(items, tops) {
  items.forEach((item, index) => {
    item.querySelector(".mzf-c-big-label").getBoundingClientRect = () => ({
      top: tops[index],
    });
  });
}

function stateClasses(root) {
  return [...root.classList].filter((name) =>
    name.startsWith("mzf-c-meet-mozilla--state-"),
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

describe("Meet Mozilla scroll states", () => {
  beforeEach(() => {
    animationFrames = [];
    vi.stubGlobal("innerHeight", VIEWPORT_HEIGHT);
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

  describe("getReadingLine", () => {
    it("is the top of the intro text while the intro is sticky", () => {
      const { root } = createSection();

      expect(getReadingLine(root, VIEWPORT_HEIGHT)).toBe(INTRO_TOP);
    });

    it("is the middle of the viewport when the layout stacks", () => {
      const { root } = createSection({ sticky: false });

      expect(getReadingLine(root, VIEWPORT_HEIGHT)).toBe(500);
    });
  });

  describe("getCurrentState", () => {
    it("stays on the first state until a step's label reaches the line", () => {
      const { items } = createSection();
      placeLabels(items, [INTRO_TOP + 1, 1200, 1900]);

      expect(getCurrentState(items, INTRO_TOP)).toBe("00");
    });

    it("takes the state of the last step whose label has reached the line", () => {
      const { items } = createSection();

      placeLabels(items, [INTRO_TOP, 1100, 1800]);
      expect(getCurrentState(items, INTRO_TOP)).toBe("01");

      placeLabels(items, [-1000, -300, 200]);
      expect(getCurrentState(items, INTRO_TOP)).toBe("03");
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

  describe("initMeetMozilla", () => {
    it("watches the section and listens to scroll only while it is on screen", () => {
      const { root, items } = createSection();
      const addListener = vi.spyOn(window, "addEventListener");
      const removeListener = vi.spyOn(window, "removeEventListener");
      initMeetMozilla(root);

      expect(observer.observe).toHaveBeenCalledWith(root);

      intersectionCallback([{ isIntersecting: true }]);
      expect(addListener).toHaveBeenCalledWith("scroll", expect.any(Function), {
        passive: true,
      });

      placeLabels(items, [-200, 300, 1500]);
      intersectionCallback([{ isIntersecting: false }]);
      expect(removeListener).toHaveBeenCalledWith(
        "scroll",
        addListener.mock.calls[0][1],
      );
      runAnimationFrames();
      expect(stateClasses(root)).toEqual(["mzf-c-meet-mozilla--state-02"]);
    });

    it("updates the section as steps reach the intro, both ways", () => {
      const { root, items } = createSection();
      initMeetMozilla(root);
      intersectionCallback([{ isIntersecting: true }]);

      placeLabels(items, [INTRO_TOP - 10, 1100, 1800]);
      scroll();
      expect(stateClasses(root)).toEqual(["mzf-c-meet-mozilla--state-01"]);

      placeLabels(items, [-800, -100, INTRO_TOP - 10]);
      scroll();
      expect(stateClasses(root)).toEqual(["mzf-c-meet-mozilla--state-03"]);

      placeLabels(items, [INTRO_TOP + 400, 1500, 2200]);
      scroll();
      expect(stateClasses(root)).toEqual(["mzf-c-meet-mozilla--state-00"]);
    });

    it("batches scroll events into one update per frame", () => {
      const { root, items } = createSection();
      placeLabels(items, [0, 1100, 1800]);
      initMeetMozilla(root);
      intersectionCallback([{ isIntersecting: true }]);
      runAnimationFrames();

      window.dispatchEvent(new Event("scroll"));
      window.dispatchEvent(new Event("scroll"));
      window.dispatchEvent(new Event("scroll"));

      expect(animationFrames).toHaveLength(1);
    });

    it("does nothing without steps to watch", () => {
      const { root } = createSection({ states: [null, null] });

      expect(initMeetMozilla(root)).toBeNull();
      expect(IntersectionObserver).not.toHaveBeenCalled();
      expect(stateClasses(root)).toEqual(["mzf-c-meet-mozilla--state-00"]);
    });

    it("keeps the markup's state where IntersectionObserver is missing", () => {
      vi.stubGlobal("IntersectionObserver", undefined);
      const { root } = createSection();

      expect(initMeetMozilla(root)).toBeNull();
      expect(stateClasses(root)).toEqual(["mzf-c-meet-mozilla--state-00"]);
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
