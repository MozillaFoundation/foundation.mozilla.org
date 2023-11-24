const { test, expect } = require("@playwright/test");
const waitForImagesToLoad = require("../../wait-for-images.js");
const {
  LANGUAGE_OPTIONS,
} = require("../../../source/js/components/newsletter-signup/data/language-options.js");

const locales = LANGUAGE_OPTIONS.map((language) => language.value);

function generateUrl(locale = "en") {
  return `http://localhost:8000/${locale}/blog/initial-test-blog-post-with-fixed-title/?random=query`;
}

test.describe("Blog body newsletter signup form", () => {
  let localeToTest = locales[0];

  test.beforeEach(async ({ page }) => {
    const pageUrl = generateUrl(localeToTest);
    const testEmail = `test-${localeToTest}@example.com`;

    const response = await page.goto(pageUrl);
    const status = await response.status();
    expect(status).not.toBe(404);

    await page.locator("body.react-loaded");
    await waitForImagesToLoad(page);

    // test if the newsletter module is visible
    const moduleContainer = page.locator(
      ".newsletter-signup-module[data-module-type='blog-body']"
    );
    await moduleContainer.waitFor({ state: "visible" });
    expect(await moduleContainer.count()).toBe(1);

    // test if the inner wrapper is visible and data-submission-status attribute is set to "none"
    const innerWrapper = moduleContainer.locator(".inner-wrapper");
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
    const submitButton = form.locator(`button[type="submit"]`);
    expect(await submitButton.count()).toBe(1);

    const emailInput = form.locator(`input[type="email"]`);
    expect(await emailInput.count()).toBe(1);
    expect(await emailInput.inputValue()).toBe("");

    const privacyInput = form.locator(`input[type="checkbox"][name="privacy"]`);
    expect(await privacyInput.count()).toBe(1);
    expect(await privacyInput.isChecked()).toBe(false);

    // test if toggleable fields are hidden (not rendered on the page) by default
    const countryDropdown = form.locator(`select[name="country"]`);
    expect(await countryDropdown.count()).toBe(0);

    const languageDropdown = form.locator(`select[name="language"]`);
    expect(await languageDropdown.count()).toBe(0);

    // test if submitting the form without filling out the required fields creates validation errors
    // wait for submitButton's click event to be attached
    const requiredFields = await form.locator(`[required]`);
    let errorMessages = form.locator(".error-message");
    await submitButton.waitFor({ state: "attached" });
    await submitButton.click();
    expect(await errorMessages.count()).toBe(await requiredFields.count());

    // test if putting focus on the email field triggers the toggleable fields
    await emailInput.focus();
    expect(await countryDropdown.count()).toBe(1);
    expect(await languageDropdown.count()).toBe(1);

    // test if filling out the form and submitting it eliminates the validation errors
    await emailInput.fill(testEmail);
    await privacyInput.check();

    // wait for the request before submitting the form
    const apiUrl = await moduleContainer.getAttribute("data-api-url");
    const fetchRequest = page.waitForRequest(apiUrl);

    await submitButton.click();
    expect(await errorMessages.count()).toBe(0);
    expect(await innerWrapper.getAttribute("data-submission-status")).toBe(
      "pending"
    );

    const postData = (await fetchRequest).postData();
    let postDataObj = JSON.parse(postData);

    expect(postDataObj.email).toBe(testEmail);
    expect(postDataObj.country).toBe("");
    expect(postDataObj.lang).toBe(localeToTest);
    expect(postDataObj.source).toBe(pageUrl);

    // wait for the fetch response to be received
    const fetchResponse = await page.waitForResponse(apiUrl);
    expect(fetchResponse.status()).toBe(201);
  });

  for (const locale of locales) {
    test(`(${locale}) Signing up newsletter`, async ({ page }) => {
      localeToTest = locale;

      // Form has been submitted successfully.
      //   - Thank you messages should be displayed.
      //   - Form should not be displayed.
      const moduleContainer = page.locator(
        ".newsletter-signup-module[data-module-type='blog-body']"
      );
      await moduleContainer.waitFor({ state: "visible" });
      expect(await moduleContainer.count()).toBe(1);

      const innerWrapper = moduleContainer.locator(".inner-wrapper");
      await innerWrapper.waitFor({ state: "visible" });
      expect(await innerWrapper.count()).toBe(1);
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

      // wait for a few seconds before moving on to avoid triggering the Basket's rate limit
      await page.waitForTimeout(1000);
    });
  }
});
