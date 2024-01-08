const { test, expect } = require("@playwright/test");
const waitForImagesToLoad = require("../../../wait-for-images.js");
const utility = require("./utility.js");

test.describe("Donate Help Form", () => {
  let thankYouUrlInputValue = "";

  // locales we support on foundation.mozilla.org
  let supportedLocales = [
    "en",
    "de",
    "es",
    "fr",
    "fy-NL",
    "nl",
    "pl",
    "pt-BR",
    "sw",
  ];

  // Locales supported by FRU and their corresponding IDs,
  // unsupported languages default to `tfa_227`.
  const localeMap = {
    "nl": "tfa_221",
    "fy-NL": "tfa_221",
    "en": "tfa_222",
    "fr": "tfa_223",
    "de": "tfa_224",
    "pl": "tfa_228",
    "pt-BR": "tfa_229",
    "es": "tfa_231",
    "other": "tfa_227",
  };

  let localeToTest = supportedLocales[0];

  for (const locale of supportedLocales) {
    test(`(${locale})`, async ({ page }) => {
      localeToTest = locale;
      // Navigate to the URL for the current locale
      const response = await page.goto(utility.generateUrl(localeToTest));
      const status = await response.status();
      expect(status).not.toBe(404);

      // Wait for the body to load and images to finish loading
      await page.locator("body.react-loaded");
      await waitForImagesToLoad(page);

      // Get the form container and wait for it to be visible
      const wFormContainer = page.locator(".wFormContainer");
      await wFormContainer.waitFor({ state: "visible" });
      expect(await wFormContainer.count()).toBe(1);

      // Test the "I Need..." dropdown menu exists, and is visible to the user.
      const iNeedDropDown = wFormContainer.locator(
        utility.FA_FIELDS.iNeedDropDown
      );
      expect(await iNeedDropDown.count()).toBe(1);
      expect(await iNeedDropDown.isVisible()).toBe(true);

      // Test that the "Name" input exists, is empty, and is not visible until the user
      // selects an option from the dropdown menu.
      const nameInput = wFormContainer.locator(utility.FA_FIELDS.name);
      expect(await nameInput.count()).toBe(1);
      expect(await nameInput.inputValue()).toBe("");
      expect(await nameInput.isVisible()).toBe(false);

      // Test that the "Email" input exists, is empty, and is not visible until the user
      // selects an option from the dropdown menu.
      const emailInput = wFormContainer.locator(utility.FA_FIELDS.email);
      expect(await emailInput.count()).toBe(1);
      expect(await emailInput.inputValue()).toBe("");
      expect(await emailInput.isVisible()).toBe(false);

      // Test that the "Other Details" text box field exists, and is not visible until the user
      // selects an option from the dropdown menu.
      const otherDetailsTextBox = wFormContainer.locator(
        utility.FA_FIELDS.otherDetailsTextBox
      );
      expect(await otherDetailsTextBox.count()).toBe(1);
      expect(await otherDetailsTextBox.inputValue()).toBe("");
      expect(await otherDetailsTextBox.isVisible()).toBe(false);

      // Test that the optional "Screenshot" input field exists, and is not visible until the user
      // selects a supported option from the dropdown menu.
      const screenshotInput = wFormContainer.locator(
        utility.FA_FIELDS.screenshotField
      );
      expect(await screenshotInput.count()).toBe(1);
      expect(await screenshotInput.getAttribute("type")).toBe("file");
      expect(await screenshotInput.isVisible()).toBe(false);

      // Test that the "Lang" input exists, is hidden, and is being appropriately mapped the correct FRU language code.
      const langInput = wFormContainer.locator(utility.FA_HIDDEN_FIELDS.lang);
      expect(await langInput.count()).toBe(1);
      expect(await langInput.isHidden()).toBe(true);
      expect(await langInput.inputValue()).toBe(
        localeMap[localeToTest] || localeMap["other"]
      );

      // Test that the "Thank You Url" input exists, is hidden, and is prepopulated with the appropriate "thank you" URL.
      const thankYouUrlInput = wFormContainer.locator(
        utility.FA_HIDDEN_FIELDS.thankYouUrl
      );
      expect(await thankYouUrlInput.count()).toBe(1);
      expect(await thankYouUrlInput.isHidden()).toBe(true);
      thankYouUrlInputValue = await thankYouUrlInput.inputValue();
      // test if the thank you url in the input field is correct
      expect(
        utility.isExpectedThankYouUrl(thankYouUrlInputValue, page.url(), false)
      ).toBe(true);

      // Test that the "Submit" button exists, initially renders as "disabled", and is hidden until the user selects an option from the drowpdown menu.
      const submitButton = wFormContainer.locator(`input[type="submit"]`);
      expect(await submitButton.count()).toBe(1);
      expect(await submitButton.isVisible()).toBe(false);
      expect(await submitButton.isEnabled()).toBe(false);

      // Remove the disabled attribute from the "Submit" button for testing purposes.
      await submitButton.evaluate((el) => el.removeAttribute("disabled"));

      // Loop through each option of the "I Need..." dropdown element, and make sure that the appropriate input fields render.
      for (const option of utility.DROP_DOWN_OPTIONS) {
        await iNeedDropDown.selectOption({ value: option.value });

        expect(await nameInput.isVisible()).toBe(true);
        expect(await emailInput.isVisible()).toBe(true);
        expect(await otherDetailsTextBox.isVisible()).toBe(true);
        expect(await submitButton.isVisible()).toBe(true);

        // If this option is set to include the optional screenshot field, make sure that it renders.
        if (option.has_image_field) {
          expect(await screenshotInput.isVisible()).toBe(true);
        } else {
          expect(await screenshotInput.isVisible()).toBe(false);
        }
      }

      // Test if submitting the form without filling out the required fields creates validation errors.
      await submitButton.click();
      expect(await page.locator(".errFld").count()).toBe(2);
      expect(await page.locator(".errMsg").count()).toBe(2);

      // Navigate to the form's "thank you" URL without submitting,
      // to avoid flooding FormAssembly with test submissions.
      // The FRU form is set to redirect to this URL upon successful submission.
      await page.goto(thankYouUrlInputValue);

      // Double check that new page URL is formatted correctly, and includes any existing params.
      expect(
        utility.isExpectedThankYouUrl(page.url(), thankYouUrlInputValue, true)
      ).toBe(true);

      // Verify that the FRU form's container div is no longer being rendered,
      // and that the "thank you" message is rendering in its place.
      const thankYouDiv = page.locator("#thank-you");
      expect(await thankYouDiv.isVisible()).toBe(true);
      expect(await wFormContainer.isVisible()).toBe(false);
    });
  }
});
