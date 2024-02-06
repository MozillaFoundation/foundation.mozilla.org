const { test, expect } = require("@playwright/test");
const waitForImagesToLoad = require("../../wait-for-images.js");

/**
 * Perform several PNI tests related to searching/filtering
 *
 * NOTE: this requires a `new-db` run with the seed value set
 *       through RANDOM_SEED=530910203 in your .env file
 *
 */
test.describe("PNI search", () => {
  const searchTerm = "ab";

  const counts = {
    // provided RANDOM_SEED=530910203 was used!
    total: 38,
    health: 11,
    smart: 4,
    percy: 1,
    searchTerm: 5,
    searchTermWithDing: 4,
  };

  const qs = {
    ding: `#product-filter-pni-toggle`, // this is the "privacy not included" filter toggle
    dingLabel: `label[for="product-filter-pni-toggle"]`,
    products: `.product-box.d-flex`,
    searchBar: `#product-filter-search-input`,
    clearSearch: `label[for="product-filter-search-input"]`,
    activeCategory: `#multipage-nav a.multipage-link.active`,
    activeSubCategory: `a.subcategories.active`,
    healthCategory: `#multipage-nav a.multipage-link[data-name="Health & Exercise"]`,
  };

  /**
   * Helper function tot confirm whether or not all products are sorted by creepiness
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

  test.beforeEach(async ({ page }) => {
    page.on(`console`, console.log);
    await page.goto(`http://localhost:8000/en/privacynotincluded`);
    await page.locator(`body.react-loaded`);
    await waitForImagesToLoad(page);
  });

  test(`Homepage default`, async ({ page }) => {
    // verify that the PNI "ding" is not selected on initial load
    let products;
    const ding = page.locator(qs.ding);
    await expect(ding).not.toBeChecked();

    // Baseline product count test
    products = page.locator(qs.products);
    await expect(products).toHaveCount(counts.total);

    // Verify that all products are sorted on creepiness
    expect(await confirmSorted(page)).toBe(true);
  });

  test(`Search by keyword "percy'"`, async ({ page }) => {
    // Test search filtering for "percy": there should be two products
    let products;
    const searchBar = page.locator(qs.searchBar);
    await searchBar.type("percy");
    products = page.locator(qs.products);
    await expect(products).toHaveCount(counts.percy);

    // And we should be back to the original number when clearing search.
    await page.click(qs.clearSearch);
    products = page.locator(qs.products);
    await expect(products).toHaveCount(counts.total);
  });

  test(`Search when a category is active`, async ({ page }) => {
    // Click through to the Health & Exercise category and
    // verify the correct number of products show up.
    let products, activeCategory, subcats, subcat, activeSubCat;
    const searchBar = page.locator(qs.searchBar);

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
    subcat = page.locator(`a.subcategories:nth-child(3)`);
    await expect(subcat).toHaveText(`Smart Scales`);
    await page.click(`a.subcategories:nth-child(3)`);
    products = page.locator(qs.products);
    await expect(products).toHaveCount(counts.smart);

    // Filter for "percy" products: there should be two, and the active
    // category should be "all" while search filtering
    await searchBar.type("percy");
    products = page.locator(qs.products);
    await expect(products).toHaveCount(counts.percy);
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
  });

  test(`Apply "ding" toggle to search results`, async ({ page }) => {
    let products;
    const searchBar = page.locator(qs.searchBar);

    // Filtering for "ding" should refocus on text field if there
    // was a search term, while filtering for ding-only
    await searchBar.type(searchTerm);
    await page.click(`main`);
    await page.click(qs.dingLabel);
    await expect(searchBar).toBeFocused();

    // Check for the ding-only products here,
    // since the ding - only class is added to a parent element
    products = page.locator(".product-box:visible");
    await expect(products).toHaveCount(counts.searchTermWithDing);
    await page.click(qs.dingLabel);
    products = page.locator(qs.products);
    await expect(products).toHaveCount(counts.searchTerm);

    // Finally, verify that all products are still sorted
    await page.click(qs.clearSearch);
    expect(await confirmSorted(page)).toBe(true);
  });
});
