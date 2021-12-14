const { test, expect } = require("@playwright/test");
const waitForImagesToLoad = require("./wait-for-images.js");

test(`Foundation homepage`, async ({ page }, testInfo) => {
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
    `#nav-newsletter-form-wrapper .country-picker.form-control`
  );
  const languagePicker = await page.locator(`#userLanguage-header`);
  expect(await countryPicker.isVisible()).toBe(false);
  expect(await languagePicker.isVisible()).toBe(false);
  const input = await page.locator(
    `#nav-newsletter-form-wrapper input[name="userEmail"]`
  );
  await input.focus();
  expect(await countryPicker.isVisible()).toBe(true);
  expect(await languagePicker.isVisible()).toBe(true);
});

test(`PNI search`, async ({ page }, testInfo) => {
  page.on(`console`, console.log);
  await page.goto(`http://localhost:8000/en/privacynotincluded`);
  await page.locator(`body.react-loaded`);
  await waitForImagesToLoad(page);

  let products, activeCategory;

  products = page.locator(`.product-box:visible`);
  await expect(products).toHaveCount(45);

  const searchBar = page.locator(`#product-filter-search-input`);
  await searchBar.type("percy");

  products = page.locator(`.product-box:visible`);
  await expect(products).toHaveCount(2);

  await page.click(`label[for="product-filter-search-input"]`);
  products = page.locator(`.product-box:visible`);
  await expect(products).toHaveCount(45);

  await page.click(`#multipage-nav a.multipage-link[data-name="Health & Exercise"]`);
  activeCategory = page.locator(`#multipage-nav a.multipage-link.active`);
  await expect(activeCategory).toHaveAttribute(`data-name`, `Health & Exercise`);

  products = page.locator(`.product-box:visible`);
  await expect(products).toHaveCount(15);

  subcats = page.locator(`a.subcategories`);
  await expect(subcats).toHaveCount(3);
  subcat = page.locator(`a.subcategories:nth-child(2)`);
  await expect(subcat).toHaveText(`Smart Scales`);
  await page.click(`a.subcategories:nth-child(2)`);
  products = page.locator(`.product-box:visible`);
  await expect(products).toHaveCount(5);

  await searchBar.type("percy");
  products = page.locator(`.product-box:visible`);
  await expect(products).toHaveCount(2);
  activeCategory = page.locator(`#multipage-nav a.multipage-link.active`);
  await expect(activeCategory).toHaveAttribute(`data-name`, `None`);

  await page.click(`label[for="product-filter-search-input"]`);
  activeCategory = page.locator(`#multipage-nav a.multipage-link.active`);
  await expect(activeCategory).toHaveAttribute(`data-name`, `Health & Exercise`);
});
