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
      data-show-more-label="Read more"
      data-show-less-label="Show less"
      aria-expanded="false"
      aria-controls="expert-profile-bio"
      hidden
    >Read more</button>
  `;
}

function mockLayout(rangeBottom = 180, bioTop = 20) {
  const range = {
    setStart: vi.fn(),
    setEnd: vi.fn(),
    getBoundingClientRect: vi.fn(() => ({ bottom: rangeBottom })),
  };
  vi.spyOn(document, "createRange").mockReturnValue(range);
  vi.spyOn(HTMLElement.prototype, "getBoundingClientRect").mockReturnValue({
    top: bioTop,
  });
  return range;
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
    expect(range.setEnd).toHaveBeenCalledOnce();
    expect(bio.classList).toContain("expert-profile-intro__bio--collapsed");
    expect(
      bio.style.getPropertyValue("--expert-profile-bio-collapsed-height"),
    ).toBe("160px");
    expect(toggle.hidden).toBe(false);
    expect(toggle.getAttribute("aria-expanded")).toBe("false");

    toggle.focus();
    toggle.click();
    expect(document.activeElement).toBe(toggle);
    expect(bio.classList).not.toContain("expert-profile-intro__bio--collapsed");
    expect(bio.textContent).toBe(originalText);
    expect(
      bio.querySelector("[data-expert-profile-bio-overflow][aria-hidden]"),
    ).toBeNull();
    expect(toggle.getAttribute("aria-expanded")).toBe("true");
    expect(toggle.textContent).toBe("Show less");

    toggle.click();
    expect(bio.classList).toContain("expert-profile-intro__bio--collapsed");
    expect(bio.textContent).toBe(originalText);
    expect(toggle.getAttribute("aria-expanded")).toBe("false");
    expect(toggle.textContent).toBe("Read more");
  });

  it("recomputes the clipping height without replacing visible content", () => {
    renderBio("<p>One two three four five six seven eight nine</p>");
    const bio = document.querySelector("[data-expert-profile-bio]");
    const paragraph = bio.querySelector("p");
    const range = mockLayout();
    initExpertProfileBioToggle();

    range.getBoundingClientRect.mockReturnValue({ bottom: 220 });
    window.dispatchEvent(new Event("resize"));

    expect(
      bio.style.getPropertyValue("--expert-profile-bio-collapsed-height"),
    ).toBe("200px");
    expect(bio.querySelector("p")).toBe(paragraph);
    expect(bio.classList).toContain("expert-profile-intro__bio--collapsed");
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
