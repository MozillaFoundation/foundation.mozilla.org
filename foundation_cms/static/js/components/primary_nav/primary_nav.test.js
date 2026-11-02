import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import {
  initPrimaryNav,
  initWordmarkVisibilityOnScroll,
} from "./primary_nav.js";
import { CLASSNAMES, EVENTS } from "./config.js";

let eventListenerCleanups;
let reducedMotion;

/**
 * Tracks listeners added to shared event targets so tests can remove them.
 *
 * @param {EventTarget[]} targets
 */
function trackEventListeners(targets) {
  targets.forEach((target) => {
    const addEventListener = target.addEventListener.bind(target);
    vi.spyOn(target, "addEventListener").mockImplementation(
      (type, listener, options) => {
        addEventListener(type, listener, options);
        eventListenerCleanups.push(() =>
          target.removeEventListener(type, listener, options),
        );
      },
    );
  });
}

function buildPrimaryNavMarkup() {
  document.body.innerHTML = `
    <header class="mzf-c-nav primary-nav-ns" data-primary-nav>
      <div class="mzf-c-nav__bar">
        <nav class="mzf-c-nav__links">
          <button type="button" data-nav-panel="section-1" aria-expanded="false">About us</button>
          <button type="button" data-nav-panel="section-2" aria-expanded="false">Our Work</button>
          <a href="/festival/">Festival</a>
        </nav>
        <button type="button" class="mzf-c-nav__menu" aria-expanded="false"
                aria-label="Open menu" data-label-open="Open menu" data-label-close="Close menu"></button>
      </div>
      <div class="mzf-c-nav__panel" hidden>
        <div class="mzf-c-nav__panel-reveal">
          <div class="mzf-c-nav__panel-inner">
            <div class="mzf-c-nav__panel-stage">
              <div data-nav-panel-content="section-1" hidden><a href="/a/">A</a></div>
              <div data-nav-panel-content="section-2" hidden><a href="/b/">B</a></div>
            </div>
          </div>
        </div>
      </div>
      <div class="mzf-c-nav__drawer" hidden>
        <div class="mzf-c-nav__drawer-reveal">
          <div class="mzf-c-nav__drawer-inner">
            <details class="mzf-c-mega-menu__disclosure" name="sections">
              <summary class="mzf-c-mega-menu__summary">About us</summary>
              <div class="mzf-c-mega-menu__reveal"></div>
            </details>
            <details class="mzf-c-mega-menu__disclosure" name="sections">
              <summary class="mzf-c-mega-menu__summary">Our Work</summary>
              <div class="mzf-c-mega-menu__reveal"></div>
            </details>
          </div>
        </div>
      </div>
    </header>
    <main><button type="button" class="outside">Outside</button></main>
  `;

  return {
    nav: document.querySelector("[data-primary-nav]"),
    panel: document.querySelector(".mzf-c-nav__panel"),
    triggers: [...document.querySelectorAll("[data-nav-panel]")],
    contents: [...document.querySelectorAll("[data-nav-panel-content]")],
    menuButton: document.querySelector(".mzf-c-nav__menu"),
    drawer: document.querySelector(".mzf-c-nav__drawer"),
    disclosures: [...document.querySelectorAll("details")],
  };
}

function pressEscape() {
  document.dispatchEvent(
    new KeyboardEvent("keydown", { key: "Escape", bubbles: true }),
  );
}

describe("initPrimaryNav", () => {
  beforeEach(() => {
    document.body.replaceWith(document.createElement("body"));
    eventListenerCleanups = [];
    trackEventListeners([document, window]);
    reducedMotion = true;
    vi.stubGlobal(
      "matchMedia",
      vi.fn((query) => ({
        matches: query.includes("reduced-motion") ? reducedMotion : false,
        addEventListener: vi.fn(),
      })),
    );
    vi.spyOn(window, "requestAnimationFrame").mockImplementation((callback) => {
      callback(0);
      return 1;
    });
    vi.useFakeTimers();
  });

  afterEach(() => {
    eventListenerCleanups.reverse().forEach((cleanup) => cleanup());
    vi.useRealTimers();
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
  });

  it("does nothing when the nav is missing", () => {
    document.body.innerHTML = `<main></main>`;

    expect(() => initPrimaryNav()).not.toThrow();
  });

  it("opens a section's panel and announces it", () => {
    const { panel, triggers, contents } = buildPrimaryNavMarkup();
    const willOpen = vi.fn();
    document.addEventListener(EVENTS.primaryNavWillOpen, willOpen);

    initPrimaryNav();
    triggers[0].click();

    expect(willOpen).toHaveBeenCalledTimes(1);
    expect(panel.hidden).toBe(false);
    expect(panel.classList.contains(CLASSNAMES.panelOpen)).toBe(true);
    expect(contents[0].hidden).toBe(false);
    expect(contents[1].hidden).toBe(true);
    expect(triggers[0].getAttribute("aria-expanded")).toBe("true");
    expect(triggers[1].getAttribute("aria-expanded")).toBe("false");
  });

  it("switches sections in the open shell and closes on a second click", () => {
    const { panel, triggers, contents } = buildPrimaryNavMarkup();

    initPrimaryNav();
    triggers[0].click();
    triggers[1].click();

    expect(panel.hidden).toBe(false);
    expect(contents[0].hidden).toBe(true);
    expect(contents[1].hidden).toBe(false);
    expect(triggers[0].getAttribute("aria-expanded")).toBe("false");
    expect(triggers[1].getAttribute("aria-expanded")).toBe("true");

    triggers[1].click();

    expect(panel.hidden).toBe(true);
    expect(contents[1].hidden).toBe(true);
    expect(triggers[1].getAttribute("aria-expanded")).toBe("false");
  });

  it("crossfades sections with motion, then settles on the new one", () => {
    reducedMotion = false;
    const { nav, triggers, contents } = buildPrimaryNavMarkup();

    initPrimaryNav();
    triggers[0].click();
    triggers[1].click();

    expect(nav.classList.contains(CLASSNAMES.switching)).toBe(true);
    expect(contents[0].classList.contains(CLASSNAMES.contentSwapOut)).toBe(
      true,
    );
    expect(contents[1].classList.contains(CLASSNAMES.contentSwapIn)).toBe(true);

    vi.runAllTimers();

    expect(nav.classList.contains(CLASSNAMES.switching)).toBe(false);
    expect(contents[0].hidden).toBe(true);
    expect(contents[1].classList.contains(CLASSNAMES.contentActive)).toBe(true);
  });

  it("folds the panel away after its content fades on close", () => {
    reducedMotion = false;
    const { panel, triggers } = buildPrimaryNavMarkup();
    Object.defineProperty(
      document.querySelector(".mzf-c-nav__panel-inner"),
      "scrollHeight",
      { value: 300 },
    );

    initPrimaryNav();
    triggers[0].click();
    triggers[0].click();

    expect(panel.classList.contains(CLASSNAMES.panelClosing)).toBe(true);
    expect(panel.hidden).toBe(false);

    vi.runAllTimers();

    expect(panel.classList.contains(CLASSNAMES.panelClosing)).toBe(false);
    expect(panel.hidden).toBe(true);
  });

  it("closes the panel on Escape and returns focus to its trigger", () => {
    const { panel, triggers } = buildPrimaryNavMarkup();
    const focusSpy = vi.spyOn(triggers[0], "focus");

    initPrimaryNav();
    triggers[0].click();
    pressEscape();

    expect(panel.hidden).toBe(true);
    expect(focusSpy).toHaveBeenCalled();
  });

  it("closes the panel on a click outside the nav only", () => {
    const { panel, triggers, contents } = buildPrimaryNavMarkup();

    initPrimaryNav();
    triggers[0].click();
    contents[0]
      .querySelector("a")
      .dispatchEvent(new MouseEvent("click", { bubbles: true }));
    expect(panel.hidden).toBe(false);

    document.querySelector(".outside").click();
    expect(panel.hidden).toBe(true);
  });

  it("closes the menus when another overlay asks", () => {
    const { panel, triggers } = buildPrimaryNavMarkup();

    initPrimaryNav();
    triggers[0].click();
    document.dispatchEvent(new CustomEvent(EVENTS.closeMenus));

    expect(panel.hidden).toBe(true);
  });

  it("toggles the drawer from the menu button and keeps its label in step", () => {
    const { nav, menuButton, drawer } = buildPrimaryNavMarkup();

    initPrimaryNav();
    menuButton.click();

    expect(drawer.hidden).toBe(false);
    expect(nav.classList.contains(CLASSNAMES.drawerOpen)).toBe(true);
    expect(menuButton.getAttribute("aria-expanded")).toBe("true");
    expect(menuButton.getAttribute("aria-label")).toBe("Close menu");

    menuButton.click();

    expect(drawer.hidden).toBe(true);
    expect(nav.classList.contains(CLASSNAMES.drawerOpen)).toBe(false);
    expect(menuButton.getAttribute("aria-expanded")).toBe("false");
    expect(menuButton.getAttribute("aria-label")).toBe("Open menu");
  });

  it("closes the drawer at once when search is about to open", () => {
    reducedMotion = false;
    const { nav, menuButton, drawer } = buildPrimaryNavMarkup();
    Object.defineProperty(
      document.querySelector(".mzf-c-nav__drawer-inner"),
      "scrollHeight",
      { value: 352 },
    );

    initPrimaryNav();
    menuButton.click();
    document.dispatchEvent(new CustomEvent(EVENTS.searchWillOpen));

    expect(drawer.hidden).toBe(true);
    expect(nav.classList.contains(CLASSNAMES.drawerOpen)).toBe(false);
  });

  it("closes the drawer on Escape and returns focus to the menu button", () => {
    const { menuButton, drawer } = buildPrimaryNavMarkup();
    const focusSpy = vi.spyOn(menuButton, "focus");

    initPrimaryNav();
    menuButton.click();
    pressEscape();

    expect(drawer.hidden).toBe(true);
    expect(focusSpy).toHaveBeenCalled();
  });

  it("closes an open drawer row before opening the next one", () => {
    reducedMotion = false;
    const { disclosures } = buildPrimaryNavMarkup();
    const [about, work] = disclosures;

    initPrimaryNav();
    about.querySelector("summary").click();
    expect(about.open).toBe(true);

    work.querySelector("summary").click();
    expect(about.classList.contains(CLASSNAMES.disclosureClosing)).toBe(true);
    expect(work.open).toBe(false);

    vi.runAllTimers();

    expect(about.open).toBe(false);
    expect(work.open).toBe(true);
  });
});

describe("initWordmarkVisibilityOnScroll", () => {
  let observerCallback;

  beforeEach(() => {
    document.body.replaceWith(document.createElement("body"));
    observerCallback = null;
    vi.stubGlobal(
      "IntersectionObserver",
      vi.fn((callback) => {
        observerCallback = callback;
        return {
          observe: vi.fn(),
          disconnect: vi.fn(),
        };
      }),
    );
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("leaves the logo shown when the kinetic type wordmark is absent", () => {
    document.body.innerHTML = `<header data-primary-nav></header>`;

    initWordmarkVisibilityOnScroll();

    expect(
      document
        .querySelector("[data-primary-nav]")
        .classList.contains(CLASSNAMES.logoHidden),
    ).toBe(false);
    expect(IntersectionObserver).not.toHaveBeenCalled();
  });

  it("hides the nav logo while the kinetic type wordmark intersects", () => {
    document.body.innerHTML = `
      <header data-primary-nav></header>
      <div class="kinetic-type-wordmark"></div>
    `;
    const nav = document.querySelector("[data-primary-nav]");

    initWordmarkVisibilityOnScroll();

    expect(IntersectionObserver).toHaveBeenCalledTimes(1);
    observerCallback([{ isIntersecting: true }]);
    expect(nav.classList.contains(CLASSNAMES.logoHidden)).toBe(true);

    observerCallback([{ isIntersecting: false }]);
    expect(nav.classList.contains(CLASSNAMES.logoHidden)).toBe(false);
  });
});
