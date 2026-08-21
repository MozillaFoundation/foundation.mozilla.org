import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import { ensureCsrfToken } from "../utils/csrf.js";
import { initIllustratedNewsletterSignups } from "./illustrated_newsletter_signup_block.js";

vi.mock("../utils/csrf.js", () => ({
  ensureCsrfToken: vi.fn(),
}));

vi.mock("../components/newsletter_signup/data/country_options.js", () => ({
  COUNTRY_OPTIONS: [
    { value: "", label: "Your Country" },
    { value: "CA", label: "Canada" },
    { value: "MX", label: "Mexico" },
  ],
}));

vi.mock("../components/newsletter_signup/data/language_options.js", () => ({
  LANGUAGE_OPTIONS: [
    { value: "en", label: "English" },
    { value: "fr", label: "Français" },
    { value: "de", label: "Deutsch" },
  ],
}));

function createSignup({ currentLanguage = "fr" } = {}) {
  document.body.insertAdjacentHTML(
    "beforeend",
    `
      <section
        data-illustrated-newsletter-signup
        data-state="default"
        data-current-language="${currentLanguage}"
        data-signup-url="/newsletter/signup/"
        data-loading-label="Signing up"
      >
        <div class="illustrated-newsletter-signup__signup-view">
          <form class="illustrated-newsletter-signup__form">
            <input name="email" type="email">
            <select name="country"></select>
            <label>Choose a country</label>
            <select name="language"></select>
            <label>Choose a language</label>
            <input name="privacy" type="checkbox">
            <div class="illustrated-newsletter-signup__expanded" hidden>More fields</div>
            <p class="email-error-message" hidden>Enter a valid email</p>
            <p class="privacy-error-message" hidden>Accept privacy</p>
            <button class="illustrated-newsletter-signup__button" type="submit">
              <span class="btn-primary__text">Sign up</span>
              <span class="btn-primary__text">Join</span>
            </button>
          </form>
        </div>
        <p class="illustrated-newsletter-signup__server-error" hidden>Try again</p>
        <div class="illustrated-newsletter-signup__success" tabindex="-1" hidden>
          Thank you
        </div>
      </section>
    `,
  );

  const container = document
    .querySelectorAll("[data-illustrated-newsletter-signup]")
    .item(
      document.querySelectorAll("[data-illustrated-newsletter-signup]").length -
        1,
    );
  const form = container.querySelector("form");
  const expanded = container.querySelector(
    ".illustrated-newsletter-signup__expanded",
  );
  const success = container.querySelector(
    ".illustrated-newsletter-signup__success",
  );
  Object.defineProperty(form, "offsetHeight", {
    configurable: true,
    get: () => (expanded.hidden ? 120 : 280),
  });
  Object.defineProperty(container, "offsetHeight", { value: 300 });
  Object.defineProperty(success, "offsetHeight", { value: 140 });
  return container;
}

function submit(form) {
  form.dispatchEvent(new Event("submit", { bubbles: true, cancelable: true }));
}

function transitionEnd(element, propertyName) {
  const event = new Event("transitionend");
  Object.defineProperty(event, "propertyName", { value: propertyName });
  element.dispatchEvent(event);
}

describe("illustrated newsletter signup block", () => {
  let reducedMotion;
  let fetchMock;

  beforeEach(() => {
    reducedMotion = false;
    vi.useFakeTimers();
    vi.stubGlobal(
      "requestAnimationFrame",
      vi.fn((callback) => callback()),
    );
    vi.stubGlobal("fetch", vi.fn());
    fetchMock = fetch;
    vi.stubGlobal(
      "matchMedia",
      vi.fn(() => ({ matches: reducedMotion })),
    );
    vi.mocked(ensureCsrfToken).mockReset();
    vi.mocked(ensureCsrfToken).mockResolvedValue("csrf-token");
  });

  afterEach(() => {
    vi.useRealTimers();
    vi.restoreAllMocks();
    vi.unstubAllGlobals();
    document.body.innerHTML = "";
  });

  it("initializes field state, localized options, and unique error IDs", () => {
    const first = createSignup();
    const second = createSignup({ currentLanguage: "unsupported" });
    first.querySelector("input[name='email']").value = "person@example.com";

    initIllustratedNewsletterSignups();

    const email = first.querySelector("input[name='email']");
    const country = first.querySelector("select[name='country']");
    const language = first.querySelector("select[name='language']");
    expect(email.dataset.hasValue).toBe("true");
    expect(country.options[0].textContent).toBe("Choose a country");
    expect(country.options[0].disabled).toBe(true);
    expect(country.options.length).toBeGreaterThan(2);
    expect(language.options[0].textContent).toBe("Choose a language");
    expect(language.querySelector("option[value='fr']")).not.toBeNull();
    expect(first.querySelector(".email-error-message").id).toBe(
      "illustrated-newsletter-email-error-0",
    );
    expect(second.querySelector(".email-error-message").id).toBe(
      "illustrated-newsletter-email-error-1",
    );

    email.value = "";
    email.dispatchEvent(new Event("input"));
    expect(email.dataset.hasValue).toBe("false");
    country.value = country.options[1].value;
    country.dispatchEvent(new Event("change"));
    expect(country.dataset.hasValue).toBe("true");
  });

  it("expands the form on focus and cleans up after the height transition", () => {
    const container = createSignup();
    initIllustratedNewsletterSignups();
    const form = container.querySelector("form");
    const expanded = container.querySelector(
      ".illustrated-newsletter-signup__expanded",
    );

    container
      .querySelector("input[name='email']")
      .dispatchEvent(new Event("focus"));
    expect(container.dataset.state).toBe("expanded");
    expect(expanded.hidden).toBe(false);
    expect(form.style.height).toBe("280px");
    expect(form.style.overflow).toBe("hidden");

    transitionEnd(form, "opacity");
    expect(form.style.height).toBe("280px");
    transitionEnd(form, "height");
    expect(form.style.height).toBe("");
    expect(form.style.overflow).toBe("");

    container
      .querySelector("input[name='email']")
      .dispatchEvent(new Event("focus"));
    expect(container.dataset.state).toBe("expanded");
  });

  it("expands immediately for reduced motion", () => {
    reducedMotion = true;
    const container = createSignup();
    initIllustratedNewsletterSignups();
    const form = container.querySelector("form");

    container.querySelector("input[name='email']").focus();

    expect(container.dataset.state).toBe("expanded");
    expect(
      container.querySelector(".illustrated-newsletter-signup__expanded")
        .hidden,
    ).toBe(false);
    expect(form.style.height).toBe("");
  });

  it("reports invalid email and privacy fields before making a request", () => {
    const container = createSignup();
    initIllustratedNewsletterSignups();
    const form = container.querySelector("form");
    const email = container.querySelector("input[name='email']");
    const privacy = container.querySelector("input[name='privacy']");
    const emailError = container.querySelector(".email-error-message");
    const privacyError = container.querySelector(".privacy-error-message");
    const emailFocus = vi.spyOn(email, "focus");
    const privacyFocus = vi.spyOn(privacy, "focus");

    submit(form);
    expect(emailFocus).toHaveBeenCalledOnce();
    expect(emailError.hidden).toBe(false);
    expect(email.getAttribute("aria-invalid")).toBe("true");
    expect(email.getAttribute("aria-describedby")).toBe(emailError.id);
    expect(privacyError.hidden).toBe(false);
    expect(fetchMock).not.toHaveBeenCalled();

    email.value = "person@example.com";
    submit(form);
    expect(privacyFocus).toHaveBeenCalledOnce();
    expect(emailError.hidden).toBe(true);
    expect(email.getAttribute("aria-invalid")).toBe("false");
    expect(email.hasAttribute("aria-describedby")).toBe(false);
    expect(privacy.getAttribute("aria-describedby")).toBe(privacyError.id);
  });

  it("submits values and transitions to the success view", async () => {
    fetchMock.mockResolvedValue({ status: 201 });
    const container = createSignup({ currentLanguage: "unsupported" });
    initIllustratedNewsletterSignups();
    const form = container.querySelector("form");
    const email = container.querySelector("input[name='email']");
    const country = container.querySelector("select[name='country']");
    const privacy = container.querySelector("input[name='privacy']");
    const button = container.querySelector("button[type='submit']");
    const success = container.querySelector(
      ".illustrated-newsletter-signup__success",
    );
    email.value = "  person@example.com  ";
    country.value = country.options[1].value;
    privacy.checked = true;

    submit(form);
    expect(container.dataset.state).toBe("submitting");
    expect(button.disabled).toBe(true);
    expect(button.getAttribute("aria-busy")).toBe("true");
    expect(
      Array.from(button.querySelectorAll("span"), (label) => label.textContent),
    ).toEqual(["Signing up", "Signing up"]);

    await vi.waitFor(() => expect(fetchMock).toHaveBeenCalledOnce());
    expect(fetchMock).toHaveBeenCalledWith(
      "/newsletter/signup/",
      expect.objectContaining({
        method: "POST",
        credentials: "same-origin",
        headers: expect.objectContaining({ "X-CSRFToken": "csrf-token" }),
        body: JSON.stringify({
          email: "person@example.com",
          country: country.value,
          lang: "en",
          source: window.location.href,
        }),
      }),
    );
    await vi.waitFor(() => expect(container.dataset.state).toBe("success"));
    expect(success.hidden).toBe(false);
    expect(container.style.height).toBe("140px");

    transitionEnd(container, "opacity");
    expect(
      container.querySelector(".illustrated-newsletter-signup__signup-view")
        .hidden,
    ).toBe(false);
    transitionEnd(container, "height");
    expect(
      container.querySelector(".illustrated-newsletter-signup__signup-view")
        .hidden,
    ).toBe(true);
    expect(document.activeElement).toBe(success);
    expect(container.style.height).toBe("");
  });

  it("shows the server error and restores the submit button after failure", async () => {
    fetchMock.mockRejectedValue(new Error("Network unavailable"));
    const container = createSignup();
    initIllustratedNewsletterSignups();
    const form = container.querySelector("form");
    const email = container.querySelector("input[name='email']");
    const privacy = container.querySelector("input[name='privacy']");
    const button = container.querySelector("button[type='submit']");
    email.value = "person@example.com";
    privacy.checked = true;

    submit(form);

    await vi.waitFor(() => expect(container.dataset.state).toBe("error"));
    expect(
      container.querySelector(".illustrated-newsletter-signup__server-error")
        .hidden,
    ).toBe(false);
    expect(button.disabled).toBe(false);
    expect(button.hasAttribute("aria-busy")).toBe(false);
    expect(
      Array.from(button.querySelectorAll("span"), (label) => label.textContent),
    ).toEqual(["Sign up", "Join"]);
  });

  it("uses the selected language and shows success immediately for reduced motion", async () => {
    reducedMotion = true;
    fetchMock.mockResolvedValue({ status: 201 });
    const container = createSignup();
    initIllustratedNewsletterSignups();
    const form = container.querySelector("form");
    const language = container.querySelector("select[name='language']");
    const success = container.querySelector(
      ".illustrated-newsletter-signup__success",
    );
    container.querySelector("input[name='email']").value = "person@example.com";
    container.querySelector("input[name='privacy']").checked = true;
    language.value = "de";

    submit(form);

    await vi.waitFor(() => expect(container.dataset.state).toBe("success"));
    expect(JSON.parse(fetchMock.mock.calls[0][1].body).lang).toBe("de");
    expect(
      container.querySelector(".illustrated-newsletter-signup__signup-view")
        .hidden,
    ).toBe(true);
    expect(success.hidden).toBe(false);
    expect(document.activeElement).toBe(success);
  });

  it("does nothing when no signup blocks are present", () => {
    expect(() => initIllustratedNewsletterSignups()).not.toThrow();
    expect(fetchMock).not.toHaveBeenCalled();
  });
});
