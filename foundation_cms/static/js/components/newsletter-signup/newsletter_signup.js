import { LANGUAGE_OPTIONS } from "./data/language-options.js";
import { COUNTRY_OPTIONS } from "./data/country-options.js";

/**
 * CSS selectors used to locate key DOM elements in the newsletter signup component.
 */
const SELECTORS = {
  container: ".newsletter-signup",
  form: ".newsletter-signup__form",
  emailInput: "input[name='email']",
  countryInput: "select[name='country']",
  languageInput: "select[name='language']",
  privacyCheckbox: "input[name='privacy']",
  emailErrorMessage: ".email-error-message",
  privacyErrorMessage: ".privacy-error-message",
  successMessage: ".newsletter-signup__success-message",
  errorMessage: ".newsletter-signup__error-message",
  expandableField: ".newsletter-signup__field--hidden",
};

/**
 * CSS class names used to toggle visibility or styling of DOM elements.
 */
const CLASSNAMES = {
  formHidden: "newsletter-signup__form--hidden",
  successHidden: "newsletter-signup__success-message--hidden",
  errorHidden: "newsletter-signup__error-message--hidden",
  fieldErrorHidden: "newsletter-signup__field-error--hidden",
};

/**
 * Submits newsletter signup data to the API endpoint.
 *
 * @param {string} signupUrl - The API URL to send the signup data to.
 * @param {Object} formData - An object containing email, country, and language values.
 * @returns {Promise<boolean>} Resolves to `true` if submission is successful, otherwise `false`.
 */
async function submitDataToApi(signupUrl, formData) {
  const payload = {
    email: formData.email,
    country: formData.country,
    lang: formData.language,
    source: window.location.href,
  };

  try {
    const res = await fetch(signupUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest",
      },
      body: JSON.stringify(payload),
    });

    return res.status === 201;
  } catch (err) {
    return false;
  }
}

/**
 * Populates a <select> element with provided options.
 *
 * @param {HTMLSelectElement} selectEl - The select element to populate.
 * @param {Array<{value: string, label: string}>} options - An array of option objects.
 */
function populateSelectOptions(selectEl, options) {
  selectEl.innerHTML = "";

  options.forEach(({ value, label }) => {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = label;
    selectEl.appendChild(option);
  });
}

/**
 * Applies layout behavior to reveal additional fields either on focus or immediately.
 *
 * @param {HTMLFormElement} form - The form element containing the fields.
 * @param {string} layout - The layout type ('default' or 'expanded').
 * @param {HTMLInputElement} emailInput - The email input field that triggers expansion.
 */
function applyLayoutBehavior(form, layout, emailInput) {
  const expandableFields = form.querySelectorAll(SELECTORS.expandableField);

  const revealHiddenFields = () => {
    expandableFields.forEach((el) =>
      el.classList.remove(CLASSNAMES.fieldErrorHidden),
    );
  };

  if (layout === "expanded") {
    revealHiddenFields();
  } else {
    emailInput.addEventListener("focus", revealHiddenFields, { once: true });
  }
}

/**
 * Validates the newsletter signup form inputs.
 *
 * @param {string} email - The email address to validate.
 * @param {boolean} privacyChecked - Whether the privacy checkbox is checked.
 * @param {HTMLElement} emailErrorMessage - Element to show if email is invalid.
 * @param {HTMLElement} privacyErrorMessage - Element to show if privacy is unchecked.
 * @returns {boolean} `true` if form is valid, otherwise `false`.
 */
function validateForm({
  email,
  privacyChecked,
  emailErrorMessage,
  privacyErrorMessage,
}) {
  let isValid = true;
  const emailRegex = /^[^@]+@[^.@]+(\.[^.@]+)+$/;

  if (!email || !emailRegex.test(email)) {
    emailErrorMessage.classList.remove(CLASSNAMES.fieldErrorHidden);
    isValid = false;
  }

  if (!privacyChecked) {
    privacyErrorMessage.classList.remove(CLASSNAMES.fieldErrorHidden);
    isValid = false;
  }

  return isValid;
}

/**
 * Injects newsletter signup form behavior into all instances on the page.
 *
 * @param {string} foundationSiteURL - The base URL of the site, used to construct the API endpoint.
 */
export default function injectNewsletterSignups(foundationSiteURL) {
  const formContainers = document.querySelectorAll(SELECTORS.container);

  formContainers.forEach((container) => {
    const form = container.querySelector(SELECTORS.form);
    const emailInput = form.querySelector(SELECTORS.emailInput);
    const countryInput = form.querySelector(SELECTORS.countryInput);
    const languageInput = form.querySelector(SELECTORS.languageInput);
    const privacyCheckbox = form.querySelector(SELECTORS.privacyCheckbox);

    const emailErrorMessage = form.querySelector(SELECTORS.emailErrorMessage);
    const privacyErrorMessage = form.querySelector(
      SELECTORS.privacyErrorMessage,
    );
    const successMessage = container.querySelector(SELECTORS.successMessage);
    const errorMessage = container.querySelector(SELECTORS.errorMessage);

    const signupId = container.dataset.signupId;
    const layout = container.dataset.layout;
    const signupUrl = `${foundationSiteURL}/newsletter-signup/${signupId}/`;

    populateSelectOptions(languageInput, LANGUAGE_OPTIONS);
    populateSelectOptions(countryInput, COUNTRY_OPTIONS);

    applyLayoutBehavior(form, layout, emailInput);

    form.addEventListener("submit", function (e) {
      e.preventDefault();

      const email = emailInput.value.trim();
      const country = countryInput?.value || "";
      const language = languageInput?.value || "";
      const privacyChecked = privacyCheckbox?.checked || false;

      const isValid = validateForm({
        email,
        privacyChecked,
        emailErrorMessage,
        privacyErrorMessage,
      });

      if (!isValid) return;

      const formData = { email, country, language };

      submitDataToApi(signupUrl, formData).then((success) => {
        if (success) {
          form.classList.add(CLASSNAMES.formHidden);
          successMessage?.classList.remove(CLASSNAMES.successHidden);
        } else {
          errorMessage?.classList.remove(CLASSNAMES.errorHidden);
        }
      });
    });
  });
}
