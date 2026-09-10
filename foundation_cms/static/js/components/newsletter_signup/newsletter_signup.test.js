import {
  afterEach,
  beforeAll,
  beforeEach,
  describe,
  expect,
  it,
  vi,
} from "vitest";

vi.mock("../../utils/csrf.js", () => ({
  ensureCsrfToken: vi.fn().mockResolvedValue("test-csrf-token"),
}));

let injectNewsletterSignups;

beforeAll(async () => {
  window.gettext = (message) => message;
  ({ default: injectNewsletterSignups } =
    await import("./newsletter_signup.js"));
});

function buildSignupMarkup({
  layout = "default",
  currentLanguage = "en",
  signupId = "footer",
} = {}) {
  document.body.innerHTML = `
    <div
      class="newsletter-signup__container"
      data-signup-id="${signupId}"
      data-layout="${layout}"
      data-current-language="${currentLanguage}"
    >
      <form class="newsletter-signup__form">
        <input name="email" type="email" value="" />
        <select name="country"></select>
        <select name="language"></select>
        <input name="privacy" type="checkbox" />
        <p class="email-error-message newsletter-signup__field-error--hidden"></p>
        <p class="privacy-error-message newsletter-signup__field-error--hidden"></p>
        <button class="newsletter-signup__button" type="submit">
          <span class="loading-message" style="display: none">Loading</span>
          <span class="btn-primary__rolltext">Sign up</span>
        </button>
        <div class="newsletter-signup__field newsletter-signup__field--hidden">
          Extra field
        </div>
      </form>
      <p class="newsletter-signup__success-message newsletter-signup__success-message--hidden">
        Thanks for signing up
      </p>
      <p class="newsletter-signup__error-message newsletter-signup__error-message--hidden">
        Something went wrong
      </p>
    </div>
  `;
}

describe("injectNewsletterSignups", () => {
  beforeEach(() => {
    document.body.innerHTML = "";
    delete window.wagtailAbTesting;
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        status: 201,
        ok: true,
        json: vi.fn().mockResolvedValue({}),
      }),
    );
  });

  afterEach(() => {
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
  });

  it("does nothing when no signup containers are present", () => {
    document.body.innerHTML = "";

    expect(() =>
      injectNewsletterSignups("https://foundation.test"),
    ).not.toThrow();
    expect(fetch).not.toHaveBeenCalled();
  });

  it("populates country and language selects and defaults unsupported languages to en", () => {
    buildSignupMarkup({ currentLanguage: "unsupported" });
    const countryInput = document.querySelector("select[name='country']");
    const languageInput = document.querySelector("select[name='language']");

    injectNewsletterSignups("https://foundation.test");

    expect(countryInput.options.length).toBeGreaterThan(0);
    expect(languageInput.options.length).toBeGreaterThan(0);
    expect(languageInput.value).toBe("en");
  });

  it("reveals hidden fields immediately for expanded layouts", () => {
    buildSignupMarkup({ layout: "expanded" });
    const hiddenField = document.querySelector(".newsletter-signup__field");

    injectNewsletterSignups("https://foundation.test");

    expect(
      hiddenField.classList.contains("newsletter-signup__field--hidden"),
    ).toBe(false);
  });

  it("reveals hidden fields when the email input receives focus in default layouts", () => {
    buildSignupMarkup({ layout: "default" });
    const emailInput = document.querySelector("input[name='email']");
    const hiddenField = document.querySelector(".newsletter-signup__field");

    injectNewsletterSignups("https://foundation.test");
    expect(
      hiddenField.classList.contains("newsletter-signup__field--hidden"),
    ).toBe(true);

    emailInput.dispatchEvent(new Event("focus"));

    expect(
      hiddenField.classList.contains("newsletter-signup__field--hidden"),
    ).toBe(false);
  });

  it("shows validation errors and skips the API call for invalid submissions", () => {
    buildSignupMarkup();
    const form = document.querySelector(".newsletter-signup__form");
    const emailError = document.querySelector(".email-error-message");
    const privacyError = document.querySelector(".privacy-error-message");

    injectNewsletterSignups("https://foundation.test");
    form.dispatchEvent(
      new Event("submit", { bubbles: true, cancelable: true }),
    );

    expect(
      emailError.classList.contains("newsletter-signup__field-error--hidden"),
    ).toBe(false);
    expect(
      privacyError.classList.contains("newsletter-signup__field-error--hidden"),
    ).toBe(false);
    expect(fetch).not.toHaveBeenCalled();
  });

  it("submits valid signup data and shows the success message", async () => {
    buildSignupMarkup({ signupId: "footer" });
    const form = document.querySelector(".newsletter-signup__form");
    const emailInput = document.querySelector("input[name='email']");
    const countryInput = document.querySelector("select[name='country']");
    const languageInput = document.querySelector("select[name='language']");
    const privacyCheckbox = document.querySelector("input[name='privacy']");
    const successMessage = document.querySelector(
      ".newsletter-signup__success-message",
    );

    injectNewsletterSignups("https://foundation.test");

    emailInput.value = "person@example.com";
    countryInput.value = countryInput.options[0].value;
    languageInput.value = "en";
    privacyCheckbox.checked = true;

    form.dispatchEvent(
      new Event("submit", { bubbles: true, cancelable: true }),
    );

    await vi.waitFor(() => {
      expect(fetch).toHaveBeenCalledWith(
        "https://foundation.test/newsletter-signup/footer/",
        expect.objectContaining({
          method: "POST",
          body: JSON.stringify({
            email: "person@example.com",
            country: countryInput.options[0].value,
            lang: "en",
            source: window.location.href,
          }),
        }),
      );
    });

    await vi.waitFor(() => {
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
    buildSignupMarkup();
    fetch.mockResolvedValueOnce({ status: 500, ok: false });
    const form = document.querySelector(".newsletter-signup__form");
    const emailInput = document.querySelector("input[name='email']");
    const privacyCheckbox = document.querySelector("input[name='privacy']");
    const errorMessage = document.querySelector(
      ".newsletter-signup__error-message",
    );

    injectNewsletterSignups("https://foundation.test");

    emailInput.value = "person@example.com";
    privacyCheckbox.checked = true;
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

  it("tracks footer newsletter submissions when wagtail A/B testing is enabled", async () => {
    buildSignupMarkup();
    window.wagtailAbTesting = { triggerEvent: vi.fn() };
    const form = document.querySelector(".newsletter-signup__form");
    const emailInput = document.querySelector("input[name='email']");
    const privacyCheckbox = document.querySelector("input[name='privacy']");

    injectNewsletterSignups("https://foundation.test");

    emailInput.value = "person@example.com";
    privacyCheckbox.checked = true;
    form.dispatchEvent(
      new Event("submit", { bubbles: true, cancelable: true }),
    );

    await vi.waitFor(() => {
      expect(window.wagtailAbTesting.triggerEvent).toHaveBeenCalledWith(
        "footer-newsletter-signup-submission",
      );
    });
  });
});
