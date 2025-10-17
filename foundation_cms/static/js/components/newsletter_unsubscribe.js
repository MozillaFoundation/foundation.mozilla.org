/**
 * CSS selectors used to locate key DOM elements in the newsletter unsubscribe component.
 */
const SELECTORS = {
  container: ".newsletter-unsubscribe__container",
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
    try {
      body = await res.json();
    } catch {
      /* non-JSON */
    }

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
 * Validates the newsletter unsubscribe form inputs.
 */
function validateForm({ email, emailErrorMessage }) {
  let isValid = true;
  const emailRegex = /^[^@]+@[^.@]+(\.[^.@]+)+$/;

  if (!email || !emailRegex.test(email)) {
    emailErrorMessage.classList.remove(CLASSNAMES.fieldErrorHidden);
    isValid = false;
  }

  return isValid;
}

/**
 * Injects newsletter unsubscribe form behavior into all instances on the page.
 */
export default function injectNewsletterSignups(foundationSiteURL) {
  const formContainers = document.querySelectorAll(SELECTORS.container);

  formContainers.forEach((container) => {
    const form = container.querySelector(SELECTORS.form);
    const emailInput = form.querySelector(SELECTORS.emailInput);

    const emailErrorMessage = form.querySelector(SELECTORS.emailErrorMessage);
    const errorMessage = container.querySelector(SELECTORS.errorMessage);

    const unsubscribeUrl = `${foundationSiteURL}/newsletter-unsubscribe/`;

    form.addEventListener("submit", function (e) {
      e.preventDefault();

      const email = emailInput.value.trim();

      const isValid = validateForm({
        email,
        emailErrorMessage,
      });

      if (!isValid) return;

      const formData = { email };
      const submitBtn = container.querySelector(SELECTORS.submitButton);
      const loadingEl = submitBtn?.querySelector(SELECTORS.loadingMessage);
      const rolltextEl = submitBtn?.querySelector(SELECTORS.rolltext);

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
