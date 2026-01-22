import {
  SELECTORS,
  CLASSNAMES,
  submitDataToApi,
  populateSelectOptions,
  applyLayoutBehavior,
  validateForm,
} from "./newsletter_signup/newsletter_signup.js";

import { LANGUAGE_OPTIONS } from "./newsletter_signup/data/language-options.js";
import { COUNTRY_OPTIONS } from "./newsletter_signup/data/country-options.js";

const PDF_SELECTORS = {
  ...SELECTORS,
  container: `${SELECTORS.container}[data-form-type="pdf_download"]`,
};

/**
 * Submits PDF download request data to the API endpoint.
 *
 * @param {string} pdfUrl - The API URL to send the PDF download request data to.
 * @param {Object} formData - An object containing email, country, and language values.
 * @returns {Promise<boolean>} Resolves to `true` if submission is successful, otherwise `false`.
 */
async function submitPdfDownloadToApi(pdfUrl, formData) {
  const payload = {
    email: formData.email,
    country: formData.country,
    lang: formData.language,
    source: window.location.href,
  };

  try {
    const res = await fetch(pdfUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest",
      },
      body: JSON.stringify(payload),
    });

    return res.status === 200 || res.status === 201;
  } catch (err) {
    console.error("PDF download error:", err);
    return false;
  }
}

/**
 * Handles both newsletter signup and PDF download
 * 
 * @param {string} newsletterUrl - The API URL for newsletter signup.
 * @param {string} pdfUrl - The API URL for PDF download request.
 * @param {Object} formData - An object containing email, country, and language values.
 * @returns {Promise<boolean>} Resolves to `true` if PDF download submission is successful, otherwise `false`.
 */
async function handlePdfDownloadSubmission(newsletterUrl, pdfUrl, formData) {
  try {
    const newsletterSuccess = await submitDataToApi(newsletterUrl, formData);    
    const pdfSuccess = await submitPdfDownloadToApi(pdfUrl, formData);

    return pdfSuccess;

  } catch (err) {
    console.error("PDF download submission error:", err);
    return false;
  }
}

/**
 * Injects PDF download signup form behavior
 */
export default function injectPdfDownloadSignups(foundationSiteURL) {
  const formContainers = document.querySelectorAll(PDF_SELECTORS.container);

  formContainers.forEach((container) => {
    const form = container.querySelector(SELECTORS.form);
    const emailInput = form.querySelector(SELECTORS.emailInput);
    const countryInput = form.querySelector(SELECTORS.countryInput);
    const languageInput = form.querySelector(SELECTORS.languageInput);
    const privacyCheckbox = form.querySelector(SELECTORS.privacyCheckbox);

    const emailErrorMessage = form.querySelector(SELECTORS.emailErrorMessage);
    const privacyErrorMessage = form.querySelector(SELECTORS.privacyErrorMessage);
    const successMessage = container.querySelector(SELECTORS.successMessage);
    const errorMessage = container.querySelector(SELECTORS.errorMessage);

    const signupId = container.dataset.signupId;
    const layout = container.dataset.layout;

    const newsletterUrl = `${foundationSiteURL}/newsletter-signup/${signupId}/`;
    const pdfUrl = `${foundationSiteURL}/pdf-download-request/${signupId}/`;

    populateSelectOptions(languageInput, LANGUAGE_OPTIONS);
    populateSelectOptions(countryInput, COUNTRY_OPTIONS);

    const currentLanguage = container.dataset.currentLanguage;
    const supportedLanguages = LANGUAGE_OPTIONS.map((opt) => opt.value);

    languageInput.value = supportedLanguages.includes(currentLanguage)
      ? currentLanguage
      : "en";

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
      const submitBtn = container.querySelector(SELECTORS.submitButton);
      const loadingEl = submitBtn?.querySelector(SELECTORS.loadingMessage);
      const rolltextEl = submitBtn?.querySelector(SELECTORS.rolltext);

      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.setAttribute("aria-busy", "true");
      }
      if (loadingEl) loadingEl.style.display = "inline";
      if (rolltextEl) rolltextEl.style.display = "none";

      handlePdfDownloadSubmission(newsletterUrl, pdfUrl, formData).then((success) => {
        if (submitBtn) {
          submitBtn.disabled = false;
          submitBtn.removeAttribute("aria-busy");
        }
        if (loadingEl) loadingEl.style.display = "none";
        if (rolltextEl) rolltextEl.style.display = "inline";

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
