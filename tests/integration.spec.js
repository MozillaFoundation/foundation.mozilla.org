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

  // Baseline product count test
  products = page.locator(`.product-box:visible`);
  await expect(products).toHaveCount(45);

  // Test search filtering for "percy": there should be two products
  const searchBar = page.locator(`#product-filter-search-input`);
  await searchBar.type("percy");
  products = page.locator(`.product-box:visible`);
  await expect(products).toHaveCount(2);

  // And we should be back to the original number when clearing search.
  await page.click(`label[for="product-filter-search-input"]`);
  products = page.locator(`.product-box:visible`);
  await expect(products).toHaveCount(45);

  // Click through to the Health & Exercise category and
  // verify the correct number of products show up.
  await page.click(
    `#multipage-nav a.multipage-link[data-name="Health & Exercise"]`
  );
  activeCategory = page.locator(`#multipage-nav a.multipage-link.active`);
  await expect(activeCategory).toHaveAttribute(
    `data-name`,
    `Health & Exercise`
  );
  products = page.locator(`.product-box:visible`);
  await expect(products).toHaveCount(15);

  // Select a known subcategory and verify the correct
  // number of products show up.
  subcats = page.locator(`a.subcategories`);
  await expect(subcats).toHaveCount(3);
  subcat = page.locator(`a.subcategories:nth-child(2)`);
  await expect(subcat).toHaveText(`Smart Scales`);
  await page.click(`a.subcategories:nth-child(2)`);
  products = page.locator(`.product-box:visible`);
  await expect(products).toHaveCount(5);

  // Filter for "percy" products: there should be two, and the active
  // category should be "all" while search filtering
  await searchBar.type("percy");
  products = page.locator(`.product-box:visible`);
  await expect(products).toHaveCount(2);
  activeCategory = page.locator(`#multipage-nav a.multipage-link.active`);
  await expect(activeCategory).toHaveAttribute(`data-name`, `None`);

  // Clear the search bar: original subcategory should be "active"
  await page.click(`label[for="product-filter-search-input"]`);
  activeCategory = page.locator(`#multipage-nav a.multipage-link.active`);
  await expect(activeCategory).toHaveAttribute(
    `data-name`,
    `Health & Exercise`
  );
  activeSubCab = page.locator(`a.subcategories.active`);
  await expect(activeSubCab).toHaveText(`Smart Scales`);
  products = page.locator(`.product-box:visible`);
  await expect(products).toHaveCount(5);

  // Clicking the subcategory should restore the parent category
  await page.click(`a.subcategories.active`);
  products = page.locator(`.product-box:visible`);
  await expect(products).toHaveCount(15);

  // Filtering for "ding" should refocus on text field if there was a search term
  await searchBar.type("a");
  await page.click(`main`);
  await page.click(`label[for="product-filter-pni-toggle"]`);
  await expect(searchBar).toBeFocused();
});
