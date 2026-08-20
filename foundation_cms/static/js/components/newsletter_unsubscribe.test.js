import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

vi.mock("../../utils/csrf.js", () => ({
  ensureCsrfToken: vi.fn().mockResolvedValue("test-csrf-token"),
}));

import injectNewsletterSignups from "./newsletter_unsubscribe.js";

let fetchMock;

function buildUnsubscribeMarkup() {
  document.body.innerHTML = `
    <div class="newsletter-unsubscribe__container">
      <form class="newsletter-signup__form">
        <input name="email" type="email" value="" />
        <p class="email-error-message newsletter-signup__field-error--hidden"></p>
        <button class="newsletter-signup__button" type="submit">
          <span class="loading-message" style="display: none">Loading</span>
          <span class="btn-primary__rolltext">Unsubscribe</span>
        </button>
      </form>
      <p class="newsletter-signup__error-message newsletter-signup__error-message--hidden">
        Something went wrong
      </p>
    </div>
  `;
}

function mockFetchResponse({ status, ok, body }) {
  fetchMock.mockImplementation(async () => ({
    status,
    ok,
    json: async () => body,
  }));
}

describe("injectNewsletterSignups (unsubscribe)", () => {
  beforeEach(() => {
    document.body.innerHTML = "";
    fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("does nothing when no unsubscribe containers are present", () => {
    document.body.innerHTML = "";

    expect(() =>
      injectNewsletterSignups("https://foundation.test"),
    ).not.toThrow();
    expect(fetchMock).not.toHaveBeenCalled();
  });

  it("shows a validation error and skips the API call for invalid email addresses", () => {
    buildUnsubscribeMarkup();
    const form = document.querySelector(".newsletter-signup__form");

    injectNewsletterSignups("https://foundation.test");
    form.dispatchEvent(
      new Event("submit", { bubbles: true, cancelable: true }),
    );

    expect(fetchMock).not.toHaveBeenCalled();
  });

  it("submits valid unsubscribe data to the API endpoint", async () => {
    buildUnsubscribeMarkup();
    mockFetchResponse({
      status: 200,
      ok: true,
      body: { redirect: "https://foundation.test/unsubscribed/" },
    });
    const form = document.querySelector(".newsletter-signup__form");
    const emailInput = document.querySelector("input[name='email']");
    const submitButton = document.querySelector(".newsletter-signup__button");
    const errorMessage = document.querySelector(
      ".newsletter-signup__error-message",
    );

    injectNewsletterSignups("https://foundation.test");

    emailInput.value = "person@example.com";
    form.dispatchEvent(
      new Event("submit", { bubbles: true, cancelable: true }),
    );

    await vi.waitFor(() => {
      expect(fetchMock).toHaveBeenCalledWith(
        "https://foundation.test/newsletter-unsubscribe/",
        expect.objectContaining({
          method: "POST",
          body: JSON.stringify({
            email: "person@example.com",
            source: window.location.href,
          }),
        }),
      );
    });

    await vi.waitFor(() => {
      expect(submitButton.disabled).toBe(false);
      expect(submitButton.getAttribute("aria-busy")).toBeNull();
      expect(
        errorMessage.classList.contains(
          "newsletter-signup__error-message--hidden",
        ),
      ).toBe(true);
    });
  });

  it("shows the error message when the API request fails", async () => {
    buildUnsubscribeMarkup();
    mockFetchResponse({
      status: 500,
      ok: false,
      body: { status: "error" },
    });
    const form = document.querySelector(".newsletter-signup__form");
    const emailInput = document.querySelector("input[name='email']");
    const errorMessage = document.querySelector(
      ".newsletter-signup__error-message",
    );

    injectNewsletterSignups("https://foundation.test");

    emailInput.value = "person@example.com";
    form.dispatchEvent(
      new Event("submit", { bubbles: true, cancelable: true }),
    );

    await vi.waitFor(() => {
      expect(
        errorMessage.classList.contains(
          "newsletter-signup__error-message--hidden",
        ),
      ).toBe(false);
    });
  });
});
