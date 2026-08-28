import { afterEach, describe, expect, it } from "vitest";

import { getCollapsedBioText, initExpertProfileBioToggle } from "./bio_toggle";

afterEach(() => {
  document.body.innerHTML = "";
});

function renderBio(text, limit = 20) {
  document.body.innerHTML = `
    <div id="expert-profile-bio" data-expert-profile-bio data-collapsed-char-limit="${limit}">
      <p>${text}</p>
    </div>
    <button
      data-expert-profile-bio-toggle
      data-show-more-label="Show more"
      data-show-less-label="Show less"
      aria-expanded="false"
      hidden
    >Show more</button>
  `;
}

describe("getCollapsedBioText", () => {
  it("returns null when visible text is within the limit", () => {
    expect(getCollapsedBioText("Short biography", 20)).toBeNull();
  });

  it("collapses normalized text at a word boundary", () => {
    expect(getCollapsedBioText("One   two three four five", 18)).toBe(
      "One two three four…",
    );
  });
});

describe("initExpertProfileBioToggle", () => {
  it("leaves the full biography visible without a toggle below the limit", () => {
    renderBio("Short biography");
    initExpertProfileBioToggle();

    expect(document.querySelector("[data-expert-profile-bio]").hidden).toBe(
      false,
    );
    expect(
      document.querySelector("[data-expert-profile-bio-toggle]").hidden,
    ).toBe(true);
  });

  it("toggles accessible collapsed and full biography states", () => {
    renderBio("One two three four five six seven eight nine");
    initExpertProfileBioToggle();

    const bio = document.querySelector("[data-expert-profile-bio]");
    const collapsed = document.querySelector(
      "[data-expert-profile-bio-collapsed]",
    );
    const toggle = document.querySelector("[data-expert-profile-bio-toggle]");

    expect(bio.hidden).toBe(true);
    expect(collapsed.hidden).toBe(false);
    expect(toggle.hidden).toBe(false);
    expect(toggle.getAttribute("aria-expanded")).toBe("false");

    toggle.click();
    expect(bio.hidden).toBe(false);
    expect(collapsed.hidden).toBe(true);
    expect(toggle.getAttribute("aria-expanded")).toBe("true");
    expect(toggle.textContent).toBe("Show less");

    toggle.click();
    expect(bio.hidden).toBe(true);
    expect(collapsed.hidden).toBe(false);
    expect(toggle.getAttribute("aria-expanded")).toBe("false");
    expect(toggle.textContent).toBe("Show more");
  });

  it("preserves spacing between rich-text paragraphs", () => {
    document.body.innerHTML = `
      <div id="expert-profile-bio" data-expert-profile-bio data-collapsed-char-limit="35">
        <p>First paragraph ends here.</p><p>Second paragraph starts here and continues.</p>
      </div>
      <button
        data-expert-profile-bio-toggle
        data-show-more-label="Show more"
        data-show-less-label="Show less"
        aria-expanded="false"
        hidden
      >Show more</button>
    `;

    initExpertProfileBioToggle();

    expect(
      document.querySelector("[data-expert-profile-bio-collapsed]").textContent,
    ).toContain("here. Second");
  });
});
