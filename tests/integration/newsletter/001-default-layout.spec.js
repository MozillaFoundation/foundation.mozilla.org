const { test, expect } = require("@playwright/test");
const waitForImagesToLoad = require("../../wait-for-images.js");
const {
  LANGUAGE_OPTIONS,
} = require("../../../source/js/components/newsletter-signup/data/language-options.js");
const { foundationBaseUrl } = require("../../base-urls.js");

const locales = LANGUAGE_OPTIONS.map((language) => language.value);
function generateUrl(locale = "en") {
  return `${foundationBaseUrl(locale)}/blog/initial-test-blog-post-with-fixed-title/?random=query`;
}

test.describe("Blog body newsletter signup form", () => {
  let localeToTest = locales[0];
  let pageUrl,
    formEmail,
    moduleContainer,
    innerWrapper,
    countryDropdown,
    languageDropdown,
    submitButton,
    errorMessages;

  test.beforeEach(async ({ page }) => {
    pageUrl = generateUrl(localeToTest);
    formEmail = `test-${localeToTest}-${Date.now()}@example.com`; // adding a timestamp to make the email unique

    const response = await page.goto(pageUrl);
    const status = await response.status();
    expect(status).not.toBe(404);

    await page.locator("body.react-loaded");
    await waitForImagesToLoad(page);

    // test if the newsletter module is visible
    moduleContainer = page.locator(
      "main .newsletter-signup-module[data-module-type='default']"
    );
    await moduleContainer.waitFor({ state: "visible" });
    expect(await moduleContainer.count()).toBe(1);

    // test if the inner wrapper is visible and data-submission-status attribute is set to "none"
    innerWrapper = moduleContainer.locator("[data-submission-status]");
    await innerWrapper.waitFor({ state: "visible" });
    expect(await innerWrapper.count()).toBe(1);
    expect(await innerWrapper.getAttribute("data-submission-status")).toBe(
      "none"
    );

    // test if the form inside the newsletter module is visible
    const form = moduleContainer.locator("form");
    await form.waitFor({ state: "visible" });
    expect(await form.count()).toBe(1);

    // test if there's a submit button
    submitButton = form.locator(`button[type="submit"]`);
    expect(await submitButton.count()).toBe(1);

    // test if the required fields (email and privacy checkbox) are rendered on the page
    const emailInput = form.locator(`input[type="email"]`);
    expect(await emailInput.count()).toBe(1);
    expect(await emailInput.inputValue()).toBe("");
    expect(await emailInput.getAttribute("required")).toBe("");

    const privacyInput = form.locator(`input[type="checkbox"][name="privacy"]`);
    expect(await privacyInput.count()).toBe(1);
    expect(await privacyInput.isChecked()).toBe(false);
    expect(await privacyInput.getAttribute("required")).toBe("");

    // test if toggleable fields are hidden (not rendered on the page) by default
    countryDropdown = form.locator(`select[name="country"]`);
    expect(await countryDropdown.count()).toBe(0);

    languageDropdown = form.locator(`select[name="language"]`);
    expect(await languageDropdown.count()).toBe(0);

    // test if submitting the form without filling out the required fields creates validation errors
    // wait for submitButton's click event to be attached
    const requiredFields = await form.locator(`[required]`);
    errorMessages = form.locator(".error-message");
    await submitButton.waitFor({ state: "attached" });
    await submitButton.dispatchEvent("click");
    expect(await errorMessages.count()).toBe(await requiredFields.count());

    // test if putting focus on the email field triggers the toggleable fields
    await emailInput.focus();
    expect(await countryDropdown.count()).toBe(1);
    expect(await languageDropdown.count()).toBe(1);

    // filling out all required fields on the form and submitting it eliminates the validation errors
    await emailInput.fill(formEmail);
    await privacyInput.check();
  });

  // test all locales we support on the site
  for (const locale of locales) {
    localeToTest = locale;

    async function testThankYouScreen() {
      // Form has been submitted successfully.
      //   - Thank you messages should be displayed.
      //   - Form should not be displayed

      await innerWrapper.waitFor({ state: "visible" });
      expect(await innerWrapper.getAttribute("data-submission-status")).toBe(
        "success"
      );

      // test if the thank you message is displayed
      const textNodes = innerWrapper.locator("p, h1, h2, h3, h4, h5, h6");
      expect(await textNodes.count()).toBeGreaterThan(0);
      for (const node of await textNodes.all()) {
        expect(await node.textContent()).not.toBe("");
      }

      // test if the form inside the newsletter module is hidden
      const form = moduleContainer.locator("form");
      expect(await form.count()).toBe(0);
    }

    test(`(${locale}) Signing up by filling out only the required fields`, async ({
      page,
    }) => {
      // wait for the request before submitting the form
      const apiUrl = await moduleContainer.getAttribute("data-api-url");
      const fetchRequest = page.waitForRequest(apiUrl);

      await submitButton.dispatchEvent("click");
      expect(await errorMessages.count()).toBe(0);
      expect(await innerWrapper.getAttribute("data-submission-status")).toBe(
        "pending"
      );

      // check if the data going to be sent to the API is correct
      const postData = (await fetchRequest).postData();
      let postDataObj = JSON.parse(postData);

      expect(postDataObj.email).toBe(formEmail);
      expect(postDataObj.country).toBe("");
      // language by default is set to the page's locale
      expect(postDataObj.lang).toBe(localeToTest);
      expect(postDataObj.source).toBe(pageUrl);

      // wait for the fetch response to be received and check if form has been submitted successfully
      const fetchResponse = await page.waitForResponse(apiUrl);
      expect(fetchResponse.status()).toBe(201);

      // check if the thank you screen is correctly displayed
      await testThankYouScreen();
    });

    test(`(${locale}) Signing up by filling out all fields`, async ({
      page,
    }) => {
      const formCountry = "CA";
      const formLang = "pt-BR";

      await countryDropdown.selectOption(formCountry);
      await languageDropdown.selectOption(formLang);

      // wait for the request before submitting the form
      const apiUrl = await moduleContainer.getAttribute("data-api-url");
      const fetchRequest = page.waitForRequest(apiUrl);

      await submitButton.dispatchEvent("click");
      expect(await errorMessages.count()).toBe(0);
      expect(await innerWrapper.getAttribute("data-submission-status")).toBe(
        "pending"
      );

      // check if the data going to be sent to the API is correct
      const postData = (await fetchRequest).postData();
      let postDataObj = JSON.parse(postData);

      expect(postDataObj.email).toBe(formEmail);
      expect(postDataObj.country).toBe(formCountry);
      expect(postDataObj.lang).toBe(formLang);
      expect(postDataObj.source).toBe(pageUrl);

      // wait for the fetch response to be received and check if form has been submitted successfully
      const fetchResponse = await page.waitForResponse(apiUrl);
      expect(fetchResponse.status()).toBe(201);

      // check if the thank you screen is correctly displayed
      await testThankYouScreen();
    });
  }
});
