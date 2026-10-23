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

import { ensureCsrfToken } from "../../utils/csrf.js";

let injectNewsletterSignups;
beforeAll(async () => {
  window.gettext = (message) => message;
  ({ default: injectNewsletterSignups } =
    await import("./newsletter_signup.js"));
});

function addSignup({
  layout = "expand_on_focus",
  currentLanguage = "en",
  signupId = "1234",
} = {}) {
  const container = document.createElement("div");
  container.dataset.newsletterSignup = "";
  container.dataset.signupId = signupId;
  container.dataset.layout = layout;
  container.dataset.currentLanguage = currentLanguage;
  container.dataset.loadingLabel = "Chargement…";
  container.innerHTML = `
    <form class="mzf-c-newsletter" novalidate>
      <p class="mzf-c-newsletter__heading">Stay informed</p>
      <p data-newsletter-error role="alert" hidden>Try again</p>
      <div class="mzf-c-newsletter__row">
        <div class="mzf-c-field"><label data-newsletter-email-label>Email</label>
          <input name="email" type="email" required>
        </div>
        <button type="submit"><span class="mzf-c-button__label">Subscribe</span></button>
      </div>
      <p data-email-error hidden>Enter a valid email</p>
      <div data-newsletter-expanded hidden>
        ${["country", "language"]
          .map(
            (name) => `
          <div class="mzf-c-dropdown" data-newsletter-dropdown="${name}">
            <input type="hidden" name="${name}">
            <button class="mzf-c-dropdown__trigger" type="button" aria-haspopup="listbox" aria-expanded="false">
              <span class="mzf-c-dropdown__value mzf-c-dropdown__value--placeholder">${name}</span>
            </button>
            <ul class="mzf-c-dropdown__menu" role="listbox" tabindex="-1" hidden></ul>
          </div>`,
          )
          .join("")}
      </div>
      <div data-newsletter-expanded hidden>
        <label><input name="privacy" type="checkbox" required>Privacy notice</label>
        <p data-privacy-error hidden>Consent required</p>
      </div>
    </form>
    <div data-newsletter-success role="status" tabindex="-1" hidden>Check your inbox</div>`;
  document.body.append(container);
  return container;
}

function submit(form) {
  form.dispatchEvent(new Event("submit", { bubbles: true, cancelable: true }));
}

function fill(form) {
  form.elements.email.focus();
  form.elements.email.value = "person@example.com";
  form.elements.privacy.checked = true;
}

describe("injectNewsletterSignups", () => {
  beforeEach(() => {
    ensureCsrfToken.mockResolvedValue("test-csrf-token");
    document.body.replaceChildren();
    delete window.wagtailAbTesting;
    vi.stubGlobal(
      "matchMedia",
      vi.fn(() => ({ matches: true })),
    );
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ status: 201 }));
  });
  afterEach(() => {
    vi.unstubAllGlobals();
    vi.restoreAllMocks();
  });

  it("does nothing without signup forms", () => {
    expect(() => injectNewsletterSignups("")).not.toThrow();
    expect(fetch).not.toHaveBeenCalled();
  });

  it.each([
    ["fr", "fr", "Français"],
    ["unsupported", "en", "English"],
  ])(
    "selects the supported language for %s",
    (currentLanguage, expected, label) => {
      const root = addSignup({ currentLanguage });
      injectNewsletterSignups("");
      const form = root.querySelector("form");
      const dropdown = form.querySelector(
        '[data-newsletter-dropdown="language"]',
      );
      const value = dropdown.querySelector(".mzf-c-dropdown__value");
      expect(form.elements.language.value).toBe(expected);
      expect(value.textContent).toBe(label);
      expect(
        value.classList.contains("mzf-c-dropdown__value--placeholder"),
      ).toBe(false);
      expect(
        [...dropdown.querySelectorAll('[aria-selected="true"]')].map(
          (option) => option.dataset.value,
        ),
      ).toEqual([expected]);
      expect(document.activeElement).toBe(document.body);
      expect(
        form.querySelectorAll(
          '[data-newsletter-dropdown="country"] [role="option"]',
        ).length,
      ).toBeGreaterThan(200);
      expect(form.elements.country.value).toBe("");
    },
  );

  it("keeps expanded forms open, reveals collapsed fields on keyboard focus and keeps Sign Up usable", () => {
    const expanded = addSignup({ layout: "expanded" });
    const collapsed = addSignup();
    injectNewsletterSignups("");
    expect(expanded.querySelector("[data-newsletter-expanded]").hidden).toBe(
      false,
    );
    expect(collapsed.querySelector("[data-newsletter-expanded]").hidden).toBe(
      true,
    );
    expect(collapsed.querySelector("button").disabled).toBe(false);
    collapsed.querySelector("input").focus();
    expect(
      [...collapsed.querySelectorAll("[data-newsletter-expanded]")].every(
        (el) => !el.hidden,
      ),
    ).toBe(true);
    expanded.querySelector("input").focus();
    expect(collapsed.querySelector("button").disabled).toBe(false);
    expect(collapsed.querySelector("[data-newsletter-expanded]").hidden).toBe(
      true,
    );
  });

  it("stays open when non-focusable form content is activated and collapses on exit", () => {
    const expanded = addSignup({ layout: "expanded" });
    const collapsed = addSignup();
    const outside = document.createElement("button");
    document.body.append(outside);
    injectNewsletterSignups("");
    const form = collapsed.querySelector("form");
    const consent = form.elements.privacy.closest("label");
    const isOpen = () =>
      [...form.querySelectorAll("[data-newsletter-expanded]")].every(
        (el) => !el.hidden,
      );
    const press = (target) =>
      target.dispatchEvent(new Event("pointerdown", { bubbles: true }));
    const exits = [
      ["outside press", () => press(document.body)],
      ["outside click without a press", () => outside.click()],
      [
        "keyboard focus leaving",
        () => {
          form.elements.privacy.focus();
          outside.focus();
        },
      ],
      ["leaving the page", () => window.dispatchEvent(new Event("blur"))],
    ];
    for (const [exit, leave] of exits) {
      // Pointer activation, then accessibility activation without a press.
      for (const pointer of [true, false]) {
        form.elements.email.focus();
        if (pointer) press(consent);
        form.elements.email.blur();
        consent.click();
        expect(isOpen(), exit).toBe(true);
        // A drag from the consent text released outside the form clicks a
        // shared ancestor instead of the consent text.
        if (pointer) {
          press(consent);
          document.body.click();
        }
        expect(isOpen(), exit).toBe(true);
        leave();
        expect(isOpen(), exit).toBe(false);
        expect(
          expanded.querySelector("[data-newsletter-expanded]").hidden,
        ).toBe(false);
      }
    }
    expect(form.elements.privacy.checked).toBe(false);
  });

  it("stays open during an outside touch scroll while the email keeps focus", () => {
    const root = addSignup();
    const page = document.createElement("div");
    const outside = document.createElement("button");
    document.body.append(page, outside);
    injectNewsletterSignups("");
    const form = root.querySelector("form");
    const button = form.querySelector('[type="submit"]');
    const isOpen = () =>
      [...form.querySelectorAll("[data-newsletter-expanded]")].every(
        (el) => !el.hidden,
      );
    form.elements.email.focus();
    // A finger scroll presses outside and is cancelled without moving focus.
    for (const type of ["pointerdown", "pointercancel"]) {
      page.dispatchEvent(new Event(type, { bubbles: true }));
    }
    expect(document.activeElement).toBe(form.elements.email);
    expect(isOpen()).toBe(true);
    expect(button.disabled).toBe(false);
    submit(form);
    expect(root.querySelector("[data-email-error]").hidden).toBe(false);
    expect(document.activeElement).toBe(form.elements.email);
    expect(fetch).not.toHaveBeenCalled();
    outside.focus();
    expect(isOpen()).toBe(false);
    expect(button.disabled).toBe(false);
  });

  it("collapses when blank page content around the form is clicked", () => {
    const root = addSignup();
    injectNewsletterSignups("");
    const form = root.querySelector("form");
    const isOpen = () =>
      [...form.querySelectorAll("[data-newsletter-expanded]")].every(
        (el) => !el.hidden,
      );
    form.elements.email.focus();
    // The press lands before the browser blurs the email with no related
    // target; the click then targets an ancestor of the form.
    document.body.dispatchEvent(new Event("pointerdown", { bubbles: true }));
    form.elements.email.blur();
    document.body.click();
    expect(isOpen()).toBe(false);
    expect(form.querySelector('[type="submit"]').disabled).toBe(false);
  });

  it("expands and validates when the idle Sign Up is activated before focus", () => {
    const root = addSignup();
    injectNewsletterSignups("");
    const form = root.querySelector("form");
    const button = form.querySelector('[type="submit"]');
    expect(form.querySelector("[data-newsletter-expanded]").hidden).toBe(true);
    expect(button.disabled).toBe(false);
    button.click();
    expect(
      [...form.querySelectorAll("[data-newsletter-expanded]")].every(
        (el) => !el.hidden,
      ),
    ).toBe(true);
    expect(root.querySelector("[data-email-error]").hidden).toBe(false);
    expect(root.querySelector("[data-privacy-error]").hidden).toBe(false);
    expect(document.activeElement).toBe(form.elements.email);
    expect(fetch).not.toHaveBeenCalled();
  });

  it("associates validation errors with controls and focuses the first invalid field", () => {
    const root = addSignup();
    injectNewsletterSignups("");
    const form = root.querySelector("form");
    form.elements.email.focus();
    submit(form);
    for (const [name, selector] of [
      ["email", "[data-email-error]"],
      ["privacy", "[data-privacy-error]"],
    ]) {
      expect(form.elements[name].getAttribute("aria-invalid")).toBe("true");
      expect(
        document.getElementById(
          form.elements[name].getAttribute("aria-describedby"),
        ),
      ).toBe(root.querySelector(selector));
      expect(root.querySelector(selector).hidden).toBe(false);
    }
    expect(document.activeElement).toBe(form.elements.email);
    expect(fetch).not.toHaveBeenCalled();
    form.elements.email.value = "person@example.com";
    form.elements.email.dispatchEvent(new Event("input"));
    expect(root.querySelector("[data-email-error]").hidden).toBe(true);
    expect(
      root
        .querySelector(".mzf-c-field")
        .classList.contains("mzf-c-field--filled"),
    ).toBe(true);
    submit(form);
    expect(document.activeElement).toBe(form.elements.privacy);
    expect(fetch).not.toHaveBeenCalled();
    form.elements.privacy.checked = true;
    form.elements.privacy.dispatchEvent(new Event("change"));
    expect(form.elements.privacy.hasAttribute("aria-invalid")).toBe(false);
  });

  it("sends the unchanged endpoint, payload, CSRF and tracking event, then focuses confirmation", async () => {
    const root = addSignup();
    window.wagtailAbTesting = { triggerEvent: vi.fn() };
    injectNewsletterSignups("https://foundation.test");
    const form = root.querySelector("form");
    fill(form);
    form.elements.country.value = "FR";
    form.elements.language.value = "fr";
    submit(form);
    await vi.waitFor(() => expect(form.hidden).toBe(true));
    expect(fetch).toHaveBeenCalledWith(
      "https://foundation.test/newsletter-signup/1234/",
      {
        method: "POST",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
          "X-Requested-With": "XMLHttpRequest",
          "X-CSRFToken": "test-csrf-token",
        },
        body: JSON.stringify({
          email: "person@example.com",
          country: "FR",
          lang: "fr",
          source: window.location.href,
        }),
      },
    );
    expect(
      window.wagtailAbTesting.triggerEvent,
    ).toHaveBeenCalledExactlyOnceWith("footer-newsletter-signup-submission");
    expect(root.querySelector("[data-newsletter-success]").hidden).toBe(false);
    expect(document.activeElement).toBe(
      root.querySelector("[data-newsletter-success]"),
    );
    submit(form);
    expect(fetch).toHaveBeenCalledTimes(1);
  });

  it("blocks duplicate submissions while pending and uses the translated loading label", async () => {
    let resolve;
    fetch.mockImplementation(
      () =>
        new Promise((done) => {
          resolve = done;
        }),
    );
    const root = addSignup();
    injectNewsletterSignups("");
    const form = root.querySelector("form");
    fill(form);
    submit(form);
    submit(form);
    const button = root.querySelector("button");
    expect(button.disabled).toBe(true);
    expect(button.getAttribute("aria-busy")).toBe("true");
    expect(button.textContent).toBe("Chargement…");
    await vi.waitFor(() => expect(fetch).toHaveBeenCalledTimes(1));
    resolve({ status: 201 });
    await vi.waitFor(() => expect(form.hidden).toBe(true));
  });

  it.each(["server", "network"])(
    "allows a retry after a %s failure without losing values",
    async (failure) => {
      if (failure === "server") fetch.mockResolvedValueOnce({ status: 500 });
      else fetch.mockRejectedValueOnce(new Error("offline"));
      const root = addSignup();
      injectNewsletterSignups("");
      const form = root.querySelector("form");
      fill(form);
      submit(form);
      await vi.waitFor(() =>
        expect(root.querySelector("[data-newsletter-error]").hidden).toBe(
          false,
        ),
      );
      expect(form.hidden).toBe(false);
      expect(form.elements.email.value).toBe("person@example.com");
      expect(form.elements.privacy.checked).toBe(true);
      expect(root.querySelector("button").disabled).toBe(false);
      expect(root.querySelector("button").textContent).toBe("Subscribe");
      expect(root.querySelector("button").hasAttribute("aria-busy")).toBe(
        false,
      );
      submit(form);
      expect(root.querySelector("[data-newsletter-error]").hidden).toBe(true);
      await vi.waitFor(() => expect(form.hidden).toBe(true));
      expect(fetch).toHaveBeenCalledTimes(2);
    },
  );

  it("initializes once and isolates repeated snippets, including newly inserted instances", async () => {
    const first = addSignup();
    injectNewsletterSignups("");
    const second = addSignup();
    document.body.prepend(second);
    injectNewsletterSignups("");
    injectNewsletterSignups("");
    const headings = [
      ...document.querySelectorAll(".mzf-c-newsletter__heading"),
    ];
    expect(new Set(headings.map((el) => el.id)).size).toBe(2);
    const form = first.querySelector("form");
    fill(form);
    submit(form);
    await vi.waitFor(() => expect(form.hidden).toBe(true));
    expect(fetch).toHaveBeenCalledTimes(1);
    expect(second.querySelector("form").hidden).toBe(false);
    expect(second.querySelector("[data-newsletter-success]").hidden).toBe(true);
  });
});

function key(element, value) {
  element.dispatchEvent(
    new KeyboardEvent("keydown", {
      key: value,
      bubbles: true,
      cancelable: true,
    }),
  );
}

describe("newsletter LP dropdown integration", () => {
  beforeEach(() => {
    document.body.replaceChildren();
    vi.stubGlobal(
      "matchMedia",
      vi.fn(() => ({ matches: true })),
    );
    vi.stubGlobal("fetch", vi.fn().mockResolvedValue({ status: 201 }));
  });
  afterEach(() => {
    vi.useRealTimers();
    vi.unstubAllGlobals();
  });

  it("supports arrows, Home/End, typeahead, selection and Escape without changing the selection", () => {
    const root = addSignup();
    injectNewsletterSignups("");
    root.querySelector('input[name="email"]').focus();
    const dropdown = root.querySelector('[data-newsletter-dropdown="country"]');
    const trigger = dropdown.querySelector("button");
    const menu = dropdown.querySelector("ul");
    const options = [...menu.children];
    expect(document.getElementById(trigger.getAttribute("aria-controls"))).toBe(
      menu,
    );
    key(trigger, "ArrowDown");
    expect(document.activeElement).toBe(options[0]);
    expect(trigger.getAttribute("aria-expanded")).toBe("true");
    key(menu, "End");
    expect(document.activeElement).toBe(options.at(-1));
    key(menu, "Home");
    expect(document.activeElement).toBe(options[0]);
    key(menu, "ArrowDown");
    expect(document.activeElement).toBe(options[1]);
    key(menu, "ArrowUp");
    expect(document.activeElement).toBe(options[0]);
    key(menu, "m");
    key(menu, "e");
    key(menu, "x");
    expect(document.activeElement.textContent).toBe("Mexico");
    key(menu, "Enter");
    expect(root.querySelector('[name="country"]').value).toBe("MX");
    expect(menu.hidden).toBe(true);
    expect(document.activeElement).toBe(trigger);
    expect(
      dropdown.querySelector(".mzf-c-dropdown__value--placeholder"),
    ).toBeNull();
    expect(menu.querySelectorAll('[aria-selected="true"]').length).toBe(1);
    key(trigger, "ArrowDown");
    key(menu, "ArrowUp");
    key(menu, "Escape");
    expect(root.querySelector('[name="country"]').value).toBe("MX");
    expect(document.activeElement).toBe(trigger);
  });

  it("closes on focus leaving and isolates country/language choices in repeated forms", () => {
    const first = addSignup();
    const second = addSignup();
    injectNewsletterSignups("");
    first.querySelector('input[name="email"]').focus();
    const trigger = first.querySelector(
      '[data-newsletter-dropdown="language"] button',
    );
    trigger.click();
    const menu = first.querySelector(
      '[data-newsletter-dropdown="language"] ul',
    );
    menu.querySelector('[data-value="fr"]').click();
    expect(first.querySelector('[name="language"]').value).toBe("fr");
    expect(second.querySelector('[name="language"]').value).toBe("en");
    trigger.click();
    second.querySelector('input[name="email"]').focus();
    expect(menu.hidden).toBe(true);
    expect(trigger.getAttribute("aria-expanded")).toBe("false");
    const ids = [...document.querySelectorAll('[role="listbox"]')].map(
      (menu) => menu.id,
    );
    expect(new Set(ids).size).toBe(4);
  });

  it("cancels pending animation when focus leaves and reopens during a close transition", () => {
    vi.useFakeTimers();
    matchMedia.mockReturnValue({ matches: false });
    const root = addSignup();
    injectNewsletterSignups("");
    const email = root.querySelector('[name="email"]');
    email.focus();
    const dropdown = root.querySelector(
      '[data-newsletter-dropdown="language"]',
    );
    const trigger = dropdown.querySelector("button");
    const menu = dropdown.querySelector("ul");
    trigger.click();
    email.focus();
    vi.runAllTimers();
    expect(menu.hidden).toBe(true);
    expect(trigger.getAttribute("aria-expanded")).toBe("false");
    trigger.click();
    vi.advanceTimersByTime(20);
    key(menu, "Escape");
    trigger.click();
    vi.runAllTimers();
    expect(menu.hidden).toBe(false);
    expect(trigger.getAttribute("aria-expanded")).toBe("true");
    document.body.click();
    vi.runAllTimers();
    expect(menu.hidden).toBe(true);
    expect(document.activeElement).not.toBe(trigger);
  });

  it("disables Sign Up only while pending, even if focus leaves, then restores it", async () => {
    let finish;
    fetch.mockImplementation(
      () =>
        new Promise((resolve) => {
          finish = resolve;
        }),
    );
    const root = addSignup();
    injectNewsletterSignups("");
    const form = root.querySelector("form");
    fill(form);
    submit(form);
    const outside = document.createElement("button");
    document.body.append(outside);
    outside.focus();
    const button = form.querySelector('[type="submit"]');
    expect(form.querySelector("[data-newsletter-expanded]").hidden).toBe(true);
    expect(button.disabled).toBe(true);
    submit(form);
    await vi.waitFor(() => expect(fetch).toHaveBeenCalledTimes(1));
    finish({ status: 500 });
    await vi.waitFor(() =>
      expect(root.querySelector("[data-newsletter-error]").hidden).toBe(false),
    );
    expect(fetch).toHaveBeenCalledTimes(1);
    expect(form.querySelector("[data-newsletter-expanded]").hidden).toBe(true);
    expect(button.disabled).toBe(false);
    expect(button.hasAttribute("aria-busy")).toBe(false);
    expect(form.elements.email.value).toBe("person@example.com");
  });
});
