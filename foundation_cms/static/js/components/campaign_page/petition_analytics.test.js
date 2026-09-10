import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { initPetitionAnalytics } from "./petition_analytics.js";

describe("initPetitionAnalytics", () => {
  beforeEach(() => {
    document.body.innerHTML = `
      <main data-petition-page-id="123" data-petition-state="signed">
        <button type="button" name="action" value="share" data-label="I will share instead">
          Share
        </button>
        <button type="button" data-label="Learn more">Learn more</button>
      </main>
    `;
    window.gtag = vi.fn();
    vi.spyOn(console, "log").mockImplementation(() => {});
  });

  afterEach(() => {
    delete window.gtag;
    vi.restoreAllMocks();
  });

  it("reports petition action buttons with the campaign context", () => {
    initPetitionAnalytics();

    document.querySelector('[value="share"]').click();

    expect(window.gtag).toHaveBeenCalledWith("event", "petition_flow_button", {
      action: "share",
      label: "I will share instead",
      page_id: "123",
      state: "signed",
    });
    expect(console.log).toHaveBeenCalledWith(
      "Button clicked: I will share instead (share)",
    );
  });

  it("uses the generic click action for other labeled buttons", () => {
    initPetitionAnalytics();

    document.querySelector('[data-label="Learn more"]').click();

    expect(window.gtag).toHaveBeenCalledWith(
      "event",
      "petition_flow_button",
      expect.objectContaining({ action: "click", label: "Learn more" }),
    );
  });

  it("does nothing outside a campaign page", () => {
    document.body.innerHTML =
      '<button data-label="Learn more">Learn more</button>';

    initPetitionAnalytics();
    document.querySelector("button").click();

    expect(window.gtag).not.toHaveBeenCalled();
  });
});
