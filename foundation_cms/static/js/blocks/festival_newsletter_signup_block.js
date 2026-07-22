import { COUNTRY_OPTIONS } from "../components/newsletter_signup/data/country-options.js";
import { LANGUAGE_OPTIONS } from "../components/newsletter_signup/data/language-options.js";

/**
 * CSS selectors used to locate elements within each Festival newsletter block.
 *
 * @type {Record<string, string>}
 */
const SELECTORS = {
  container: "[data-festival-newsletter-signup]",
  form: ".festival-newsletter-signup__form",
  emailInput: "input[name='email']",
  countryInput: "select[name='country']",
  languageInput: "select[name='language']",
  privacyCheckbox: "input[name='privacy']",
  expandedContent: ".festival-newsletter-signup__expanded",
  emailErrorMessage: ".email-error-message",
  privacyErrorMessage: ".privacy-error-message",
  errorMessage: ".festival-newsletter-signup__server-error",
  successMessage: ".festival-newsletter-signup__success",
  submitButton: ".festival-newsletter-signup__button",
};

/**
 * Populates a native select with a disabled placeholder and the supplied options.
 *
 * @param {HTMLSelectElement} selectElement - Select element to populate.
 * @param {Array<{value: string, label: string}>} options - Available options.
 * @param {string} placeholderLabel - Initial label shown before a selection.
 */
function populateSelectOptions(selectElement, options, placeholderLabel) {
  selectElement.replaceChildren(
    ...[
      { value: "", label: placeholderLabel, disabled: true },
      ...options.filter(({ value }) => value !== ""),
    ].map(({ value, label, disabled = false }) => {
      const option = document.createElement("option");
      option.value = value;
      option.textContent = label;
      option.disabled = disabled;
      return option;
    }),
  );

  selectElement.value = "";
  selectElement.dataset.hasValue = "false";
  selectElement.addEventListener("change", () => {
    selectElement.dataset.hasValue = String(Boolean(selectElement.value));
  });
}

/**
 * Keeps the input's value state available to the floating-label styles.
 *
 * @param {HTMLInputElement} inputElement - Input whose value state should be tracked.
 */
function initializeInputValueState(inputElement) {
  const updateValueState = () => {
    inputElement.dataset.hasValue = String(Boolean(inputElement.value.trim()));
  };

  updateValueState();
  inputElement.addEventListener("input", updateValueState);
  inputElement.addEventListener("change", updateValueState);
}

/**
 * Updates a field's visible error message and accessible error attributes.
 *
 * @param {HTMLInputElement} input - Field associated with the error.
 * @param {HTMLElement} errorMessage - Error message for the field.
 * @param {boolean} hasError - Whether the field is invalid.
 */
function setFieldError(input, errorMessage, hasError) {
  errorMessage.hidden = !hasError;
  input.setAttribute("aria-invalid", String(hasError));

  if (hasError) {
    input.setAttribute("aria-describedby", errorMessage.id);
  } else {
    input.removeAttribute("aria-describedby");
  }
}

/**
 * Validates the required email and privacy fields.
 *
 * @param {Object} fields - Fields and error messages used for validation.
 * @param {HTMLInputElement} fields.emailInput - Email input.
 * @param {HTMLInputElement} fields.privacyCheckbox - Privacy checkbox.
 * @param {HTMLElement} fields.emailErrorMessage - Email error message.
 * @param {HTMLElement} fields.privacyErrorMessage - Privacy error message.
 * @returns {boolean} Whether the form is valid.
 */
function validateForm({
  emailInput,
  privacyCheckbox,
  emailErrorMessage,
  privacyErrorMessage,
}) {
  const email = emailInput.value.trim();
  const validEmail = /^[^@]+@[^.@]+(\.[^.@]+)+$/.test(email);
  const privacyAccepted = privacyCheckbox.checked;

  setFieldError(emailInput, emailErrorMessage, !validEmail);
  setFieldError(privacyCheckbox, privacyErrorMessage, !privacyAccepted);

  if (!validEmail) {
    emailInput.focus();
  } else if (!privacyAccepted) {
    privacyCheckbox.focus();
  }

  return validEmail && privacyAccepted;
}

/**
 * Submits Festival newsletter signup data to the API endpoint.
 *
 * @param {string} signupUrl - Festival newsletter signup endpoint.
 * @param {{email: string, country: string, language: string}} formData - Signup values.
 * @returns {Promise<boolean>} Whether the API accepted the signup.
 */
async function submitDataToApi(signupUrl, formData) {
  const payload = {
    email: formData.email,
    country: formData.country,
    lang: formData.language,
    source: window.location.href,
  };

  try {
    const response = await fetch(signupUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest",
      },
      body: JSON.stringify(payload),
    });

    return response.status === 201;
  } catch {
    return false;
  }
}

/**
 * Initializes one Festival newsletter block instance.
 *
 * @param {HTMLElement} container - Festival newsletter block root.
 * @param {number} index - Instance index used to create unique error IDs.
 */
function initializeFestivalNewsletterSignup(container, index) {
  const form = container.querySelector(SELECTORS.form);
  const emailInput = form.querySelector(SELECTORS.emailInput);
  const countryInput = form.querySelector(SELECTORS.countryInput);
  const languageInput = form.querySelector(SELECTORS.languageInput);
  const privacyCheckbox = form.querySelector(SELECTORS.privacyCheckbox);
  const expandedContent = form.querySelectorAll(SELECTORS.expandedContent);
  const emailErrorMessage = form.querySelector(SELECTORS.emailErrorMessage);
  const privacyErrorMessage = form.querySelector(
    SELECTORS.privacyErrorMessage,
  );
  const errorMessage = container.querySelector(SELECTORS.errorMessage);
  const successMessage = container.querySelector(SELECTORS.successMessage);
  const submitButton = form.querySelector(SELECTORS.submitButton);

  emailErrorMessage.id = `festival-newsletter-email-error-${index}`;
  privacyErrorMessage.id = `festival-newsletter-privacy-error-${index}`;

  initializeInputValueState(emailInput);

  const currentLanguage = container.dataset.currentLanguage;
  const supportedLanguages = LANGUAGE_OPTIONS.map(({ value }) => value);
  const defaultLanguage = supportedLanguages.includes(currentLanguage)
    ? currentLanguage
    : "en";

  populateSelectOptions(
    countryInput,
    COUNTRY_OPTIONS,
    countryInput.nextElementSibling.textContent.trim(),
  );
  populateSelectOptions(
    languageInput,
    LANGUAGE_OPTIONS,
    languageInput.nextElementSibling.textContent.trim(),
  );

  const expand = () => {
    expandedContent.forEach((element) => {
      element.hidden = false;
    });
    container.dataset.state = "expanded";
  };

  emailInput.addEventListener("focus", expand, { once: true });

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    expand();
    errorMessage.hidden = true;

    const isValid = validateForm({
      emailInput,
      privacyCheckbox,
      emailErrorMessage,
      privacyErrorMessage,
    });
    if (!isValid) return;

    submitButton.disabled = true;
    submitButton.setAttribute("aria-busy", "true");
    container.dataset.state = "submitting";

    const submitted = await submitDataToApi(container.dataset.signupUrl, {
      email: emailInput.value.trim(),
      country: countryInput.value,
      language: languageInput.value || defaultLanguage,
    });

    if (submitted) {
      form.hidden = true;
      successMessage.hidden = false;
      container.dataset.state = "success";
      successMessage.focus();
      return;
    }

    submitButton.disabled = false;
    submitButton.removeAttribute("aria-busy");
    errorMessage.hidden = false;
    container.dataset.state = "error";
  });
}

/**
 * Initializes every Festival newsletter block on the page.
 */
export function initFestivalNewsletterSignups() {
  document
    .querySelectorAll(SELECTORS.container)
    .forEach((container, index) =>
      initializeFestivalNewsletterSignup(container, index),
    );
}
