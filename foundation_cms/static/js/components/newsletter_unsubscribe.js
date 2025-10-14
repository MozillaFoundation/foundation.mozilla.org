/**
 * CSS selectors used to locate key DOM elements in the newsletter unsubscribe component.
 */
const SELECTORS = {
  container: ".newsletter-unsubscribe-form",
  form: ".newsletter-signup__form",
  emailInput: "input[name='email']",
  emailErrorMessage: ".email-error-message",
  errorMessage: ".newsletter-signup__error-message",
  submitButton: ".newsletter-signup__button",
  loadingMessage: ".loading-message",
  rolltext: ".btn-primary__rolltext",
};

/**
 * CSS class names used to toggle visibility or styling of DOM elements.
 */
const CLASSNAMES = {
  errorHidden: "newsletter-signup__error-message--hidden",
};

/**
 * Submits newsletter unsubscribe data to the API endpoint.
 *
 * @param {string} unsubscribeUrl - The API URL to send the signup data to.
 * @param {Object} formData - An object containing email value
 * @returns {Promise<{ok: boolean, redirect?: string}>}
 */
async function submitDataToApi(unsubscribeUrl, formData) {
  const payload = {
    email: formData.email,
    source: window.location.href,
  };

  try {
    const res = await fetch(unsubscribeUrl, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest",
      },
      body: JSON.stringify(payload),
    });

    let body = {};
    try { body = await res.json(); } catch { /* non-JSON */ }

    return {
      ok: res.status === 201 || res.ok || body.status === "ok",
      redirect: body.redirect,
    };
  } catch (_err) {
    // always return an object so callers can safely read .ok / .redirect
    return { ok: false };
  }
}

/**
 * Validates the newsletter signup form inputs.
 */
function validateForm({
  email,
  emailErrorMessage,
}) {
  let isValid = true;
  const emailRegex = /^[^@]+@[^.@]+(\.[^.@]+)+$/;

  if (!email || !emailRegex.test(email)) {
    emailErrorMessage.classList.remove(CLASSNAMES.fieldErrorHidden);
    isValid = false;
  }

  return isValid;
}

/**
 * Injects newsletter signup form behavior into all instances on the page.
 */
export default function injectNewsletterSignups(foundationSiteURL) {
  console.log("injectNewsletterSignups");
  const formContainers = document.querySelectorAll(SELECTORS.container);
  console.log(`Found ${formContainers.length} newsletter signup forms on the page.`);

  formContainers.forEach((container) => {
    const form = container.querySelector(SELECTORS.form);
    console.log("Found form:", form);
    const emailInput = form.querySelector(SELECTORS.emailInput);
    console.log("Found email input:", emailInput);

    const emailErrorMessage = form.querySelector(SELECTORS.emailErrorMessage);
    console.log("Found email error message:", emailErrorMessage);
    const errorMessage = container.querySelector(SELECTORS.errorMessage);
    console.log("Found general error message:", errorMessage);

    const unsubscribeUrl = `${foundationSiteURL}/newsletter-unsubscribe/`;
    console.log("Using unsubscribeUrl URL:", unsubscribeUrl);    

    form.addEventListener("submit", function (e) {
    console.log("Form submit event triggered");
      e.preventDefault();

      const email = emailInput.value.trim();
      console.log("Form submitted with email:", email);

      const isValid = validateForm({
        email,
        emailErrorMessage,
      });

      console.log("Form validation result:", isValid);

      if (!isValid) return;

      const formData = { email };
      console.log("Prepared form data for submission:", formData);
      const submitBtn  = container.querySelector(SELECTORS.submitButton);
      console.log("Found submit button:", submitBtn);
      const loadingEl  = submitBtn?.querySelector(SELECTORS.loadingMessage);
      console.log("Found loading element:", loadingEl);
      const rolltextEl = submitBtn?.querySelector(SELECTORS.rolltext);
      console.log("Found rolltext element:", rolltextEl);   

      // show loading state
      if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.setAttribute("aria-busy", "true");
      }
      if (loadingEl) loadingEl.style.display = "inline";
      if (rolltextEl) rolltextEl.style.display = "none";

      submitDataToApi(unsubscribeUrl, formData)
        .then((result) => {
          // follow server-directed redirect if present
          if (result && result.redirect) {
            window.location.assign(result.redirect);
            return;
          }

          if (result && result.ok) {
            form.classList.add(CLASSNAMES.formHidden);
            successMessage?.classList.remove(CLASSNAMES.successHidden);
          } else {
            errorMessage?.classList.remove(CLASSNAMES.errorHidden);
          }
        })
        .finally(() => {
          // restore button state
          if (submitBtn) {
            submitBtn.disabled = false;
            submitBtn.removeAttribute("aria-busy");
          }
          if (loadingEl) loadingEl.style.display = "none";
          if (rolltextEl) rolltextEl.style.display = "";
        });
    });
  });
}
