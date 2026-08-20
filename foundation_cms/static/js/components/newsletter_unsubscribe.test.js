import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";

vi.mock("../utils/csrf.js", () => ({
  ensureCsrfToken: vi.fn().mockResolvedValue("test-csrf-token"),
}));

import { ensureCsrfToken } from "../utils/csrf.js";
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
      <p class="newsletter-signup__success-message newsletter-signup__success-message--hidden">
        You have been unsubscribed
      </p>
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

function mockLocationAssign() {
  const assign = vi.fn();
  const originalLocation = window.location;

  delete window.location;
  window.location = {
    href: "https://foundation.test/current-page/",
    assign,
  };

  return {
    assign,
    restore: () => {
      window.location = originalLocation;
    },
  };
}

describe("injectNewsletterSignups (unsubscribe)", () => {
  beforeEach(() => {
    document.body.innerHTML = "";
    fetchMock = vi.fn();
    vi.stubGlobal("fetch", fetchMock);
    ensureCsrfToken.mockClear();
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
    expect(ensureCsrfToken).not.toHaveBeenCalled();
  });

  it("shows a validation error and skips the API call for invalid email addresses", () => {
    buildUnsubscribeMarkup();
    const form = document.querySelector(".newsletter-signup__form");
    const emailError = document.querySelector(".email-error-message");

    injectNewsletterSignups("https://foundation.test");
    form.dispatchEvent(
      new Event("submit", { bubbles: true, cancelable: true }),
    );

    expect(
      emailError.classList.contains("newsletter-signup__field-error--hidden"),
    ).toBe(false);
    expect(fetchMock).not.toHaveBeenCalled();
    expect(ensureCsrfToken).not.toHaveBeenCalled();
  });

  it("follows a server-directed redirect after a successful unsubscribe", async () => {
    buildUnsubscribeMarkup();
    mockFetchResponse({
      status: 200,
      ok: true,
      body: { redirect: "https://foundation.test/unsubscribed/" },
    });
    const { assign, restore } = mockLocationAssign();
    const form = document.querySelector(".newsletter-signup__form");
    const emailInput = document.querySelector("input[name='email']");

    injectNewsletterSignups("https://foundation.test");

    emailInput.value = "person@example.com";
    form.dispatchEvent(
      new Event("submit", { bubbles: true, cancelable: true }),
    );

    await vi.waitFor(() => {
      expect(ensureCsrfToken).toHaveBeenCalledTimes(1);
      expect(fetchMock).toHaveBeenCalledTimes(1);
      expect(fetchMock).toHaveBeenCalledWith(
        "https://foundation.test/newsletter-unsubscribe/",
        expect.objectContaining({
          method: "POST",
          headers: expect.objectContaining({
            "X-CSRFToken": "test-csrf-token",
          }),
          body: JSON.stringify({
            email: "person@example.com",
            source: window.location.href,
          }),
        }),
      );
      expect(assign).toHaveBeenCalledWith(
        "https://foundation.test/unsubscribed/",
      );
    });

    restore();
  });

  it("shows the success message for a non-redirect unsubscribe response", async () => {
    buildUnsubscribeMarkup();
    mockFetchResponse({
      status: 201,
      ok: true,
      body: { status: "ok" },
    });
    const form = document.querySelector(".newsletter-signup__form");
    const emailInput = document.querySelector("input[name='email']");
    const successMessage = document.querySelector(
      ".newsletter-signup__success-message",
    );

    injectNewsletterSignups("https://foundation.test");

    emailInput.value = "person@example.com";
    form.dispatchEvent(
      new Event("submit", { bubbles: true, cancelable: true }),
    );

    await vi.waitFor(() => {
      expect(ensureCsrfToken).toHaveBeenCalledTimes(1);
      expect(form.classList.contains("newsletter-signup__form--hidden")).toBe(
        true,
      );
      expect(
        successMessage.classList.contains(
          "newsletter-signup__success-message--hidden",
        ),
      ).toBe(false);
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
