import initDropdown from "./dropdown.js";
import { LANGUAGE_OPTIONS } from "./data/language_options.js";
import { COUNTRY_OPTIONS } from "./data/country_options.js";
import { ensureCsrfToken } from "../../utils/csrf.js";

async function submitDataToApi(signupUrl, formData) {
  try {
    const response = await fetch(signupUrl, {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": await ensureCsrfToken(),
      },
      body: JSON.stringify({
        email: formData.email,
        country: formData.country,
        lang: formData.language,
        source: window.location.href,
      }),
    });
    return response.status === 201;
  } catch {
    return false;
  }
}

function setFieldError(input, message, invalid) {
  message.hidden = !invalid;
  input
    .closest(".mzf-c-field")
    ?.classList.toggle("mzf-c-field--error", invalid);
  if (invalid) {
    input.setAttribute("aria-invalid", "true");
    input.setAttribute("aria-describedby", message.id);
  } else {
    input.removeAttribute("aria-invalid");
    input.removeAttribute("aria-describedby");
  }
}

function isValidEmail(email) {
  return email.validity.valid && /^[^@]+@[^.@]+(\.[^.@]+)+$/.test(email.value);
}

let nextSignupId = 0;

/** Initialize each signup independently, including repeated uses of one snippet. */
export default function injectNewsletterSignups(foundationSiteURL) {
  document.querySelectorAll("[data-newsletter-signup]").forEach((container) => {
    if (container.dataset.initialized) return;
    container.dataset.initialized = "true";
    const index = nextSignupId++;

    const form = container.querySelector("form");
    const email = form.elements.email;
    const country = form.elements.country;
    const language = form.elements.language;
    const privacy = form.elements.privacy;
    const emailError = form.querySelector("[data-email-error]");
    const privacyError = form.querySelector("[data-privacy-error]");
    const serverError = form.querySelector("[data-newsletter-error]");
    const success = container.querySelector("[data-newsletter-success]");
    const submit = form.querySelector('button[type="submit"]');
    const label = submit.querySelector(".mzf-c-button__label");
    const defaultLabel = label.textContent;
    const heading = form.querySelector(".mzf-c-newsletter__heading");
    heading.id = `newsletter-heading-${index}`;
    form.setAttribute("aria-labelledby", heading.id);
    form.removeAttribute("aria-label");
    email.id = `newsletter-email-${index}`;
    form.querySelector("[data-newsletter-email-label]").htmlFor = email.id;
    emailError.id = `newsletter-email-error-${index}`;
    privacyError.id = `newsletter-privacy-error-${index}`;

    const languageDropdown = initDropdown(
      form.querySelector('[data-newsletter-dropdown="language"]'),
      LANGUAGE_OPTIONS,
      `newsletter-language-${index}`,
    );
    const dropdowns = [
      initDropdown(
        form.querySelector('[data-newsletter-dropdown="country"]'),
        COUNTRY_OPTIONS.filter(({ value }) => value),
        `newsletter-country-${index}`,
      ),
      languageDropdown,
    ];
    languageDropdown.setValue(
      LANGUAGE_OPTIONS.some(
        ({ value }) => value === container.dataset.currentLanguage,
      )
        ? container.dataset.currentLanguage
        : "en",
    );

    let pending = false;
    const setExpanded = (expanded) => {
      form.classList.toggle("mzf-c-newsletter--expanded", expanded);
      form.querySelectorAll("[data-newsletter-expanded]").forEach((element) => {
        element.hidden = !expanded;
      });
      submit.disabled = !expanded || pending;
      if (!expanded) dropdowns.forEach(({ close }) => close(false, true));
    };
    const expand = () => setExpanded(true);
    setExpanded(container.dataset.layout === "expanded");
    form.addEventListener("focusin", expand);
    // Activating non-focusable form content, such as the consent text, blurs
    // the active field with no related target, so only focus moving to another
    // element, an outside press or click, or leaving the page collapses.
    // Outside presses and clicks are ignored while a field keeps focus: a
    // touch scroll presses outside without moving focus.
    const collapse = () => {
      if (container.dataset.layout !== "expanded") setExpanded(false);
    };
    const isOutside = (target) =>
      !form.contains(target) && !form.contains(document.activeElement);
    form.addEventListener("focusout", (event) => {
      if (event.relatedTarget && !form.contains(event.relatedTarget)) {
        collapse();
      }
    });
    // A drag from inside the form released outside clicks a shared ancestor,
    // so remember where the press started until its click or cancellation.
    let pressedInForm = false;
    document.addEventListener("pointerdown", (event) => {
      pressedInForm = form.contains(event.target);
      if (isOutside(event.target)) collapse();
    });
    document.addEventListener("pointercancel", () => {
      pressedInForm = false;
    });
    document.addEventListener("click", (event) => {
      if (isOutside(event.target) && !pressedInForm) collapse();
      pressedInForm = false;
    });
    window.addEventListener("blur", collapse);

    const updateEmail = () => {
      email
        .closest(".mzf-c-field")
        .classList.toggle("mzf-c-field--filled", !!email.value);
      if (isValidEmail(email)) setFieldError(email, emailError, false);
    };
    updateEmail();
    email.addEventListener("input", updateEmail);
    privacy.addEventListener("change", () => {
      if (privacy.checked) setFieldError(privacy, privacyError, false);
    });

    form.addEventListener("submit", async (event) => {
      event.preventDefault();
      if (submit.disabled || form.hidden) return;
      expand();
      serverError.hidden = true;
      email.value = email.value.trim();
      const validEmail = isValidEmail(email);
      setFieldError(email, emailError, !validEmail);
      setFieldError(privacy, privacyError, !privacy.checked);
      if (!validEmail || !privacy.checked) {
        (!validEmail ? email : privacy).focus();
        return;
      }

      window.wagtailAbTesting?.triggerEvent(
        "footer-newsletter-signup-submission",
      );
      pending = true;
      submit.disabled = true;
      submit.setAttribute("aria-busy", "true");
      label.textContent = container.dataset.loadingLabel;

      const submitted = await submitDataToApi(
        `${foundationSiteURL}/newsletter-signup/${container.dataset.signupId}/`,
        {
          email: email.value,
          country: country.value,
          language: language.value,
        },
      );
      pending = false;
      submit.disabled = !form.classList.contains("mzf-c-newsletter--expanded");
      submit.removeAttribute("aria-busy");
      label.textContent = defaultLabel;
      if (submitted) {
        form.hidden = true;
        success.hidden = false;
        success.focus();
      } else {
        serverError.hidden = false;
      }
    });
  });
}
