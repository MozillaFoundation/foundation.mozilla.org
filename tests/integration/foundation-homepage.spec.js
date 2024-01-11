const { test, expect } = require("@playwright/test");
const waitForImagesToLoad = require("../wait-for-images.js");

test(`Foundation homepage`, async ({ page }) => {
  page.on(`console`, console.log);
  await page.goto(`http://localhost:8000/en/`);
  await page.locator(`body.react-loaded`);
  await waitForImagesToLoad(page);

  // verify newsletter button in the header folds out the newsletter panel
  const newsLetterWrapper = page.locator(`#nav-newsletter-form-wrapper`);
  expect(await newsLetterWrapper.isVisible()).toBe(false);

  const newsLetterButton = page.locator(
    `.wide-screen-menu-container button.btn-newsletter`
  );
  await newsLetterButton.click();
  await page.waitForTimeout(500);
  expect(await newsLetterWrapper.isVisible()).toBe(true);

  // Does the country list show only after we focus on the signup email field?
  const countryPicker = await page.locator(
    `#nav-newsletter-form-wrapper .newsletter-signup-module select[name='country']`
  );
  const languagePicker = await page.locator(
    `#nav-newsletter-form-wrapper .newsletter-signup-module select[name='language']`
  );
  expect(await countryPicker.isVisible()).toBe(false);
  expect(await languagePicker.isVisible()).toBe(false);
  const input = await page.locator(
    `#nav-newsletter-form-wrapper input[name="email"]`
  );
  await input.focus();
  expect(await countryPicker.isVisible()).toBe(true);
  expect(await languagePicker.isVisible()).toBe(true);
});
