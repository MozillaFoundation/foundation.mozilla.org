import { LANGUAGE_OPTIONS } from "./data/language-options.js";
import { COUNTRY_OPTIONS } from "./data/country-options.js";

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

function populateSelectOptions(selectEl, options) {
  selectEl.innerHTML = "";

  options.forEach(({ value, label }) => {
    const option = document.createElement("option");
    option.value = value;
    option.textContent = label;
    selectEl.appendChild(option);
  });
}

function applyLayoutBehavior(form, layout, emailInput) {
  const expandableFields = form.querySelectorAll(
    ".newsletter-signup__field--hidden",
  );

  const revealHiddenFields = () => {
    expandableFields.forEach((el) =>
      el.classList.remove("newsletter-signup__field--hidden"),
    );
  };

  if (layout === "expanded") {
    revealHiddenFields();
  } else {
    emailInput.addEventListener("focus", revealHiddenFields, { once: true });
  }
}

function validateForm({ email, privacyChecked, emailErrorEl, privacyErrorEl }) {
  let isValid = true;
  const emailRegex = /^[^@]+@[^.@]+(\.[^.@]+)+$/;

  if (!email || !emailRegex.test(email)) {
    emailErrorEl.classList.remove("newsletter-signup__field-error--hidden");
    isValid = false;
  }

  if (!privacyChecked) {
    privacyErrorEl.classList.remove("newsletter-signup__field-error--hidden");
    isValid = false;
  }

  return isValid;
}

export default function injectNewsletterSignups(networkSiteURL) {
  const formContainers = document.querySelectorAll(".newsletter-signup");

  formContainers.forEach((container) => {
    // Form Elements
    const form = container.querySelector(".newsletter-signup__form");
    const emailInput = form.querySelector("input[name='email']");
    const countrySelect = form.querySelector("select[name='country']");
    const languageSelect = form.querySelector("select[name='language']");
    const privacyInput = form.querySelector("input[name='privacy']");

    // Form Success and Validation Error Messages
    const emailErrorEl = form.querySelector(".email-error-message");
    const privacyErrorEl = form.querySelector(".privacy-error-message");
    const successMessage = container.querySelector(
      ".newsletter-signup__success-message",
    );
    const errorMessage = container.querySelector(
      ".newsletter-signup__error-message",
    );

    // Data attributes and API endpoint
    const signupId = container.dataset.signupId;
    const layout = container.dataset.layout;
    const signupUrl = `${networkSiteURL}/newsletter-signup/${signupId}/`;

    // Populate language options
    populateSelectOptions(languageSelect, LANGUAGE_OPTIONS);
    // Populate country options
    populateSelectOptions(countrySelect, COUNTRY_OPTIONS);

    // Hide/Render elements based on layout
    applyLayoutBehavior(form, layout, emailInput);

    // Add submission event listener
    form.addEventListener("submit", function (e) {
      e.preventDefault();

      const email = emailInput.value.trim();
      const country = countrySelect?.value || "";
      const language = languageSelect?.value || "";
      const privacyChecked = privacyInput?.checked || false;

      const isValid = validateForm({
        email,
        privacyChecked,
        emailErrorEl,
        privacyErrorEl,
      });
      if (!isValid) return;

      const formData = { email, country, language };

      submitDataToApi(signupUrl, formData).then((success) => {
        if (success) {
          form.classList.add("newsletter-signup__form--hidden");
          successMessage?.classList.remove(
            "newsletter-signup__success-message--hidden",
          );
        } else {
          errorMessage?.classList.remove(
            "newsletter-signup__error-message--hidden",
          );
        }
      });
    });
  });
}
