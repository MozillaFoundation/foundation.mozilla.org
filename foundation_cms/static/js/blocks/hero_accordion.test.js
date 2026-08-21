import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import {
  HorizontalAccordion,
  initAllHorizontalAccordions,
} from "./hero_accordion.js";

function createHorizontalAccordion() {
  document.body.innerHTML = `
    <section
      class="hero-accordion"
      style="--total-panels: 3; --open-multiplier: 2"
    >
      <article class="hero-accordion__panel hero-accordion__panel--video_panel active">
        <div class="hero-accordion__video-box">
          <button
            class="hero-accordion__video-overlay hidden"
            data-video-url="https://vimeo.com/12345678"
          ></button>
          <iframe></iframe>
        </div>
        <div class="hero-accordion__details hidden"></div>
      </article>
      <article class="hero-accordion__panel">Second</article>
      <article class="hero-accordion__panel">Third</article>
    </section>
  `;

  const root = document.querySelector(".hero-accordion");
  return {
    root,
    panels: root.querySelectorAll(".hero-accordion__panel"),
  };
}

describe("HorizontalAccordion", () => {
  beforeEach(() => {
    Object.defineProperty(document.documentElement, "clientWidth", {
      configurable: true,
      value: 1000,
    });
    Object.defineProperty(window, "innerWidth", {
      configurable: true,
      value: 1020,
    });
  });

  afterEach(() => {
    vi.restoreAllMocks();
    document.body.innerHTML = "";
  });

  it("initializes panel accessibility state and responsive widths once", () => {
    const { root, panels } = createHorizontalAccordion();
    const accordion = new HorizontalAccordion(root);
    const widthSpy = vi.spyOn(accordion, "_setWidth");

    accordion.init();
    accordion.init();

    expect(root.dataset.initialized).toBe("true");
    expect(root.style.getPropertyValue("--total-units")).toBe("4");
    expect(root.style.getPropertyValue("--open-panel-width")).toBe(
      "calc((100vw - 20px) / 4 * 2)",
    );
    expect(root.style.getPropertyValue("--closed-panel-width")).toBe(
      "calc((100vw - 20px) / 4)",
    );
    expect(widthSpy).toHaveBeenCalledOnce();
    panels.forEach((panel) => {
      expect(panel.getAttribute("role")).toBe("button");
      expect(panel.getAttribute("tabindex")).toBe("0");
    });
    expect(panels[0].getAttribute("aria-expanded")).toBe("true");
    expect(panels[1].getAttribute("aria-expanded")).toBe("false");
  });

  it("activates a clicked panel and restores the previous video panel", () => {
    const { root, panels } = createHorizontalAccordion();
    const accordion = new HorizontalAccordion(root);
    accordion.init();

    panels[1].click();

    expect(panels[0].classList).not.toContain("active");
    expect(panels[0].classList).toContain("transitioning-to-inactive");
    expect(panels[0].getAttribute("aria-expanded")).toBe("false");
    expect(panels[0].querySelector("iframe")).toBeNull();
    expect(
      panels[0].querySelector(".hero-accordion__video-overlay").classList,
    ).not.toContain("hidden");
    expect(
      panels[0].querySelector(".hero-accordion__details").classList,
    ).not.toContain("hidden");
    expect(panels[1].classList).toContain("active");
    expect(panels[1].getAttribute("aria-expanded")).toBe("true");

    panels[0].dispatchEvent(new Event("transitionend"));

    expect(panels[0].classList).not.toContain("transitioning-to-inactive");
  });

  it("supports Enter and Space activation without reacting to other keys", () => {
    const { root, panels } = createHorizontalAccordion();
    const accordion = new HorizontalAccordion(root);
    accordion.init();
    const clickSpy = vi.spyOn(panels[1], "click");
    const enterEvent = new KeyboardEvent("keydown", {
      cancelable: true,
      key: "Enter",
    });
    const spaceEvent = new KeyboardEvent("keydown", {
      cancelable: true,
      key: " ",
    });

    panels[1].dispatchEvent(new KeyboardEvent("keydown", { key: "Escape" }));
    panels[1].dispatchEvent(enterEvent);
    panels[1].dispatchEvent(spaceEvent);

    expect(clickSpy).toHaveBeenCalledTimes(2);
    expect(enterEvent.defaultPrevented).toBe(true);
    expect(spaceEvent.defaultPrevented).toBe(true);
  });

  it("calculates the base panel width from the document width", () => {
    const { root } = createHorizontalAccordion();
    const accordion = new HorizontalAccordion(root);

    expect(accordion._calculateBaseWidth()).toBe(250);
  });

  it("injects a Vimeo player for an active video overlay", () => {
    const { root, panels } = createHorizontalAccordion();
    panels[0].querySelector("iframe").remove();
    const overlay = panels[0].querySelector(".hero-accordion__video-overlay");
    overlay.classList.remove("hidden");

    initAllHorizontalAccordions();
    overlay.click();

    const iframe = panels[0].querySelector("iframe");
    expect(iframe.getAttribute("src")).toBe(
      "https://player.vimeo.com/video/12345678?autoplay=1&muted=1",
    );
    expect(iframe.getAttribute("allow")).toBe(
      "autoplay; fullscreen; picture-in-picture",
    );
    expect(iframe.hasAttribute("allowfullscreen")).toBe(true);
    expect(iframe.getAttribute("title")).toBe("Embedded Vimeo Video");
    expect(overlay.classList).toContain("hidden");
    expect(
      panels[0].querySelector(".hero-accordion__details").classList,
    ).toContain("hidden");
    expect(root.dataset.initialized).toBe("true");
  });

  it("warns and skips invalid video URLs", () => {
    const { panels } = createHorizontalAccordion();
    const overlay = panels[0].querySelector(".hero-accordion__video-overlay");
    overlay.setAttribute("data-video-url", "   ");
    panels[0].querySelector("iframe").remove();
    const warnSpy = vi.spyOn(console, "warn").mockImplementation(() => {});

    initAllHorizontalAccordions();
    overlay.click();

    expect(warnSpy).toHaveBeenCalledWith("Invalid Vimeo URL:", "   ");
    expect(panels[0].querySelector("iframe")).toBeNull();
  });

  it("does not play video from an inactive panel", () => {
    const { panels } = createHorizontalAccordion();
    panels[0].classList.remove("active");
    const overlay = panels[0].querySelector(".hero-accordion__video-overlay");
    panels[0].querySelector("iframe").remove();

    initAllHorizontalAccordions();
    overlay.click();

    expect(panels[0].querySelector("iframe")).toBeNull();
    expect(overlay.classList).toContain("hidden");
  });
});
