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

/**
 * Perform several PNI tests related to searching/filtering
 *
 * NOTE: this requires a `new-db` run with the seed value set
 *       through RANDOM_SEED=530910203 in your .env file
 */
test(`PNI search`, async ({ page }, testInfo) => {
  page.on(`console`, console.log);
  await page.goto(`http://localhost:8000/en/privacynotincluded`);
  await page.locator(`body.react-loaded`);
  await waitForImagesToLoad(page);

  const counts = {
    // provided RANDOM_SEED=530910203 was used!
    total: 41,
    health: 14,
    smart: 4,
    percy: 2,
    the: 14,
    theWithDing: 4,
  };

  const qs = {
    ding: `#product-filter-pni-toggle`,
    dingLabel: `label[for="product-filter-pni-toggle"]`,
    products: `.product-box:visible`,
    searchBar: `#product-filter-search-input`,
    clearSearch: `label[for="product-filter-search-input"]`,
    activeCategory: `#multipage-nav a.multipage-link.active`,
    activeSubCategory: `a.subcategories.active`,
    healthCategory: `#multipage-nav a.multipage-link[data-name="Health & Exercise"]`,
  };

  let products, activeCategory;

  // verify that the PNI "ding" is not selected on initial load
  const ding = page.locator(qs.ding);
  await expect(ding).not.toBeChecked();

  // Baseline product count test
  products = page.locator(qs.products);
  await expect(products).toHaveCount(counts.total);

  // Verify that all products are sorted on creepiness
  expect(await confirmSorted(page)).toBe(true);

  // Test search filtering for "percy": there should be two products
  const searchBar = page.locator(qs.searchBar);
  await searchBar.type("percy");
  products = page.locator(qs.products);
  await expect(products).toHaveCount(counts.percy);

  // And we should be back to the original number when clearing search.
  await page.click(qs.clearSearch);
  products = page.locator(qs.products);
  await expect(products).toHaveCount(counts.total);

  // Click through to the Health & Exercise category and
  // verify the correct number of products show up.
  await page.click(qs.healthCategory);
  activeCategory = page.locator(qs.activeCategory);
  await expect(activeCategory).toHaveAttribute(
    `data-name`,
    `Health & Exercise`
  );
  products = page.locator(qs.products);
  await expect(products).toHaveCount(counts.health);

  // Select a known subcategory and verify the correct
  // number of products show up.
  subcats = page.locator(`a.subcategories`);
  await expect(subcats).toHaveCount(3);
  subcat = page.locator(`a.subcategories:nth-child(2)`);
  await expect(subcat).toHaveText(`Smart Scales`);
  await page.click(`a.subcategories:nth-child(2)`);
  products = page.locator(qs.products);
  await expect(products).toHaveCount(counts.smart);

  // Filter for "percy" products: there should be two, and the active
  // category should be "all" while search filtering
  await searchBar.type("percy");
  products = page.locator(qs.products);
  await expect(products).toHaveCount(2);
  activeCategory = page.locator(qs.activeCategory);
  await expect(activeCategory).toHaveAttribute(`data-name`, `None`);

  // Clear the search bar: original subcategory should be "active"
  await page.click(qs.clearSearch);
  activeCategory = page.locator(qs.activeCategory);
  await expect(activeCategory).toHaveAttribute(
    `data-name`,
    `Health & Exercise`
  );
  activeSubCat = page.locator(qs.activeSubCategory);
  await expect(activeSubCat).toHaveText(`Smart Scales`);
  products = page.locator(qs.products);
  await expect(products).toHaveCount(counts.smart);

  // Clicking the subcategory should restore the parent category
  await page.click(qs.activeSubCategory);
  products = page.locator(qs.products);
  await expect(products).toHaveCount(counts.health);

  // Filtering for "ding" should refocus on text field if there
  // was a search term, while filtering for ding-only
  await searchBar.type("the");
  await page.click(`main`);
  await page.click(qs.dingLabel);
  await expect(searchBar).toBeFocused();
  products = page.locator(qs.products);
  await expect(products).toHaveCount(counts.theWithDing);
  await page.click(qs.dingLabel);
  products = page.locator(qs.products);
  await expect(products).toHaveCount(counts.the);

  // Finally, verify that all products are still sorted
  await page.click(qs.clearSearch);
  expect(await confirmSorted(page)).toBe(true);
});

/**
 * Helper function for PNI search/filter tests.
 * Confirms whether or not all products are sorted by creepiness
 * @param {Page} page The Playwright page handle
 */
async function confirmSorted(page) {
  return page.evaluate(() => {
    const products = [...document.querySelectorAll(`.product-box`)];
    return products.every((e, i, list, a, b) => {
      if (i === 0) return true;
      a = parseFloat(list[i - 1].dataset.creepiness);
      b = parseFloat(e.dataset.creepiness);
      return b >= a;
    });
  });
}
