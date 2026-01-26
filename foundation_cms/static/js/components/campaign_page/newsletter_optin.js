const SELECTORS = {
  formThankYouUrlField: ".petition__form-wrapper #tfa_500",
  formNewsletterCheckbox: ".petition__form-wrapper #tfa_495",
};

/**
 * Configures the newsletter checkbox to update the form's thank you URL.
 * When the checkbox state changes, updates the thank you URL to include or remove the newsletter_optin parameter.
 */
export function initNewsletterOptin() {
  const newsletterCheckbox = document.querySelector(
    SELECTORS.formNewsletterCheckbox,
  );
  const formThankYouUrlField = document.querySelector(
    SELECTORS.formThankYouUrlField,
  );

  if (newsletterCheckbox && formThankYouUrlField) {
    newsletterCheckbox.addEventListener("change", (e) => {
      const baseUrl = new URL(formThankYouUrlField.value);

      if (e.target.checked) {
        baseUrl.searchParams.set("newsletter_optin", "true");
      } else {
        baseUrl.searchParams.delete("newsletter_optin");
      }

      formThankYouUrlField.value = baseUrl.toString();
    });
  }
}
