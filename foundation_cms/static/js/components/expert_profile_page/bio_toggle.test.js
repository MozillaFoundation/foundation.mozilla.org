import { afterEach, describe, expect, it, vi } from "vitest";

import {
  getBioCollapseBoundary,
  initExpertProfileBioToggle,
} from "./bio_toggle";

afterEach(() => {
  document.body.innerHTML = "";
  vi.restoreAllMocks();
});

function renderBio(content, limit = 20) {
  document.body.innerHTML = `
    <div id="expert-profile-bio" data-expert-profile-bio data-collapsed-char-limit="${limit}">
      ${content}
    </div>
    <button
      data-expert-profile-bio-toggle
      data-show-more-label="Show more"
      data-show-less-label="Show less"
      aria-expanded="false"
      aria-controls="expert-profile-bio"
      hidden
    ><span aria-hidden="true">... </span><span data-expert-profile-bio-toggle-label>Show more</span></button>
  `;
}

function mockLayout(
  { top = 140, right = 300, bottom = 180 } = {},
  bioTop = 20,
) {
  const range = {
    setStart: vi.fn(),
    setEnd: vi.fn(),
    getClientRects: vi.fn(() => [
      { top, right, bottom, width: right, height: bottom - top },
    ]),
    getBoundingClientRect: vi.fn(() => ({ top, right, bottom })),
  };
  vi.spyOn(document, "createRange").mockReturnValue(range);
  vi.spyOn(HTMLElement.prototype, "getBoundingClientRect").mockImplementation(
    function getElementRect() {
      if (this.matches?.("[data-expert-profile-bio-toggle]")) {
        return {
          top: 0,
          right: 90,
          bottom: 20,
          left: 0,
          width: 90,
          height: 20,
        };
      }
      if (this === document.body) {
        return {
          top: 0,
          right: 1000,
          bottom: 500,
          left: 0,
          width: 1000,
          height: 500,
        };
      }
      return { top: bioTop, right: 0, bottom: 0, left: 0, width: 0, height: 0 };
    },
  );
  return range;
}

function getToggleLabel() {
  return document.querySelector("[data-expert-profile-bio-toggle-label]");
}

function expectCollapsedTogglePosition(toggle) {
  expect(toggle.classList).toContain(
    "expert-profile-intro__bio-toggle--collapsed",
  );
  expect(
    toggle.style.getPropertyValue("--expert-profile-bio-toggle-left"),
  ).toBe("300px");
  expect(toggle.style.getPropertyValue("--expert-profile-bio-toggle-top")).toBe(
    "160px",
  );
}

describe("getBioCollapseBoundary", () => {
  it("returns null when normalized visible text is within the limit", () => {
    renderBio("<p>Short biography</p>", 20);

    expect(
      getBioCollapseBoundary(
        document.querySelector("[data-expert-profile-bio]"),
        20,
      ),
    ).toBeNull();
  });

  it("finds a word boundary across paragraphs and inline markup", () => {
    renderBio(
      '<p>One <strong>two</strong>   three</p><p>Four <a href="#source">five six seven</a></p>',
      20,
    );

    const boundary = getBioCollapseBoundary(
      document.querySelector("[data-expert-profile-bio]"),
      20,
    );

    expect(boundary.node.parentElement.tagName).toBe("P");
    expect(boundary.node.data).toBe("Four ");
    expect(boundary.offset).toBe(4);
  });
});

describe("initExpertProfileBioToggle", () => {
  it("leaves the full biography visible without a toggle below the limit", () => {
    renderBio("<p>Short biography</p>");
    initExpertProfileBioToggle();

    const bio = document.querySelector("[data-expert-profile-bio]");
    expect(bio.hidden).toBe(false);
    expect(bio.classList).not.toContain("expert-profile-intro__bio--collapsed");
    expect(
      document.querySelector("[data-expert-profile-bio-toggle]").hidden,
    ).toBe(true);
  });

  it("clips and reveals the original rich-text subtree", () => {
    renderBio(
      '<p>First <strong>formatted</strong> paragraph ends here.</p><p>Second paragraph has a <a href="#source">source link</a> and continues.</p>',
      35,
    );
    const bio = document.querySelector("[data-expert-profile-bio]");
    const paragraphs = Array.from(bio.children);
    const strong = bio.querySelector("strong");
    const link = bio.querySelector("a");
    const originalText = bio.textContent;
    const range = mockLayout();

    initExpertProfileBioToggle();

    const toggle = document.querySelector("[data-expert-profile-bio-toggle]");
    expect(bio.hidden).toBe(false);
    expect(Array.from(bio.children)).toEqual(paragraphs);
    expect(bio.querySelector("strong")).toBe(strong);
    expect(bio.querySelector("a")).toBe(link);
    expect(bio.textContent).toBe(originalText);
    expect(
      Array.from(
        bio.querySelectorAll("[data-expert-profile-bio-overflow]"),
      ).every((element) => element.getAttribute("aria-hidden") === "true"),
    ).toBe(true);
    expect(range.setEnd).toHaveBeenCalled();
    expect(bio.classList).toContain("expert-profile-intro__bio--collapsed");
    expect(
      bio.style.getPropertyValue("--expert-profile-bio-collapsed-height"),
    ).toBe("160px");
    expect(toggle.hidden).toBe(false);
    expect(toggle.getAttribute("aria-expanded")).toBe("false");
    expectCollapsedTogglePosition(toggle);

    toggle.focus();
    toggle.click();
    expect(document.activeElement).toBe(toggle);
    expect(bio.classList).not.toContain("expert-profile-intro__bio--collapsed");
    expect(bio.textContent).toBe(originalText);
    expect(
      bio.querySelector("[data-expert-profile-bio-overflow][aria-hidden]"),
    ).toBeNull();
    expect(toggle.getAttribute("aria-expanded")).toBe("true");
    expect(toggle.classList).not.toContain(
      "expert-profile-intro__bio-toggle--collapsed",
    );
    expect(getToggleLabel().textContent).toBe("Show less");

    toggle.click();
    expect(bio.classList).toContain("expert-profile-intro__bio--collapsed");
    expect(bio.textContent).toBe(originalText);
    expect(toggle.getAttribute("aria-expanded")).toBe("false");
    expect(getToggleLabel().textContent).toBe("Show more");
    expectCollapsedTogglePosition(toggle);
  });

  it("recomputes the clipping height without replacing visible content", () => {
    renderBio("<p>One two three four five six seven eight nine</p>");
    const bio = document.querySelector("[data-expert-profile-bio]");
    const paragraph = bio.querySelector("p");
    const range = mockLayout();
    initExpertProfileBioToggle();

    range.getClientRects.mockReturnValue([
      { top: 180, right: 340, bottom: 220, width: 340, height: 40 },
    ]);
    window.dispatchEvent(new Event("resize"));

    expect(
      bio.style.getPropertyValue("--expert-profile-bio-collapsed-height"),
    ).toBe("200px");
    expect(
      document
        .querySelector("[data-expert-profile-bio-toggle]")
        .style.getPropertyValue("--expert-profile-bio-toggle-left"),
    ).toBe("340px");
    expect(bio.querySelector("p")).toBe(paragraph);
    expect(bio.classList).toContain("expert-profile-intro__bio--collapsed");
  });

  it("backs up to a word boundary so the control stays before a floated image", () => {
    renderBio("<p>One two three four five six seven eight nine ten.</p>", 40);
    const image = document.createElement("img");
    image.className = "expert-profile-intro__image";
    document.body.prepend(image);
    const range = mockLayout();
    range.getClientRects
      .mockReturnValueOnce([
        { top: 140, right: 600, bottom: 180, width: 600, height: 40 },
      ])
      .mockReturnValue([
        { top: 140, right: 400, bottom: 180, width: 400, height: 40 },
      ]);
    const originalGetComputedStyle = window.getComputedStyle.bind(window);
    vi.spyOn(image, "getBoundingClientRect").mockReturnValue({
      top: 100,
      right: 800,
      bottom: 500,
      left: 540,
      width: 260,
      height: 400,
    });
    vi.spyOn(window, "getComputedStyle").mockImplementation((element) => {
      if (element === image) return { float: "right", marginLeft: "40px" };
      if (element.matches?.("[data-expert-profile-bio-toggle]")) {
        return { marginLeft: "4px" };
      }
      return originalGetComputedStyle(element);
    });

    initExpertProfileBioToggle();

    const toggle = document.querySelector("[data-expert-profile-bio-toggle]");
    expect(
      toggle.style.getPropertyValue("--expert-profile-bio-toggle-left"),
    ).toBe("400px");
    expect(range.setEnd.mock.calls.length).toBeGreaterThan(2);
  });

  it("makes the post-cutoff subtree inert while preserving descendant attributes", () => {
    renderBio(
      '<p>One two three four five six seven.</p><p>More text with a <a href="#source" aria-hidden="false" tabindex="3">source link</a>.</p>',
    );
    mockLayout();

    initExpertProfileBioToggle();

    const paragraphs = document.querySelectorAll("[data-expert-profile-bio] p");
    const link = document.querySelector("[data-expert-profile-bio] a");
    const toggle = document.querySelector("[data-expert-profile-bio-toggle]");
    expect(paragraphs[1].getAttribute("aria-hidden")).toBe("true");
    expect(paragraphs[1].hasAttribute("inert")).toBe(true);
    expect(link.getAttribute("aria-hidden")).toBe("false");
    expect(link.getAttribute("tabindex")).toBe("3");
    expect(link.closest("[inert]")).toBe(paragraphs[1]);

    toggle.click();
    expect(paragraphs[1].hasAttribute("aria-hidden")).toBe(false);
    expect(paragraphs[1].hasAttribute("inert")).toBe(false);
    expect(link.getAttribute("aria-hidden")).toBe("false");
    expect(link.getAttribute("tabindex")).toBe("3");
    expect(link.hasAttribute("inert")).toBe(false);

    toggle.click();
    expect(paragraphs[1].getAttribute("aria-hidden")).toBe("true");
    expect(paragraphs[1].hasAttribute("inert")).toBe(true);
    expect(link.getAttribute("aria-hidden")).toBe("false");
    expect(link.getAttribute("tabindex")).toBe("3");
  });

  it("makes a post-cutoff iframe embed inert and restores its original state", () => {
    renderBio(
      '<p>One two three four five six seven.</p><div class="embed" aria-hidden="false" tabindex="2"><iframe src="https://example.com/embed" title="Embedded media" tabindex="5"></iframe></div>',
    );
    mockLayout();

    initExpertProfileBioToggle();

    const embed = document.querySelector(".embed");
    const iframe = document.querySelector("iframe");
    const toggle = document.querySelector("[data-expert-profile-bio-toggle]");
    expect(embed.getAttribute("aria-hidden")).toBe("true");
    expect(embed.hasAttribute("inert")).toBe(true);
    expect(embed.getAttribute("tabindex")).toBe("2");
    expect(iframe.getAttribute("tabindex")).toBe("5");
    expect(iframe.closest("[inert]")).toBe(embed);

    toggle.click();
    expect(embed.getAttribute("aria-hidden")).toBe("false");
    expect(embed.hasAttribute("inert")).toBe(false);
    expect(embed.getAttribute("tabindex")).toBe("2");
    expect(iframe.getAttribute("tabindex")).toBe("5");

    toggle.click();
    expect(embed.getAttribute("aria-hidden")).toBe("true");
    expect(embed.hasAttribute("inert")).toBe(true);
    expect(embed.getAttribute("tabindex")).toBe("2");
  });

  it("keeps a boundary-straddling link semantic while hiding its suffix", () => {
    renderBio(
      '<p>Start <a href="#source">linked words continue far beyond the cutoff</a> tail text.</p>',
      15,
    );
    mockLayout();

    initExpertProfileBioToggle();

    const link = document.querySelector("[data-expert-profile-bio] a");
    const hiddenSuffix = link.querySelector(
      "[data-expert-profile-bio-overflow]",
    );
    const toggle = document.querySelector("[data-expert-profile-bio-toggle]");
    expect(link.hasAttribute("aria-hidden")).toBe(false);
    expect(link.hasAttribute("tabindex")).toBe(false);
    expect(hiddenSuffix.getAttribute("aria-hidden")).toBe("true");
    expect(hiddenSuffix.hasAttribute("inert")).toBe(true);
    expect(hiddenSuffix.textContent).toContain("words continue");

    toggle.click();
    expect(hiddenSuffix.hasAttribute("aria-hidden")).toBe(false);
    expect(hiddenSuffix.hasAttribute("inert")).toBe(false);
    expect(link.textContent).toBe(
      "linked words continue far beyond the cutoff",
    );
  });

  it("starts as full semantic content when JavaScript has not initialized", () => {
    renderBio(
      '<p>First paragraph.</p><p>Second paragraph with a <a href="#source">source</a>.</p>',
      10,
    );

    const bio = document.querySelector("[data-expert-profile-bio]");
    const toggle = document.querySelector("[data-expert-profile-bio-toggle]");
    expect(toggle.hidden).toBe(true);
    expect(bio.querySelector("[aria-hidden='true']")).toBeNull();
    expect(bio.querySelector("a").getAttribute("tabindex")).toBeNull();
  });
});
