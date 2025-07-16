const { test, expect } = require("@playwright/test");
const waitForImagesToLoad = require("../../wait-for-images.js");
const { foundationBaseUrl } = require("../../base-urls.js");

test.describe("Main site primary nav (Desktop)", () => {
  test.beforeEach(async ({ page }) => {
    await page.goto(foundationBaseUrl("en"));
    await page.locator(`body.react-loaded`);
    await waitForImagesToLoad(page);
  });

  test("Dropdown menus expand on hover", async ({ page }) => {
    const dropdownSelector = ".tw-nav-desktop-dropdown";
    const dropdowns = await page.$$(dropdownSelector);

    for (let i = 0; i < dropdowns.length; i++) {
      await dropdowns[i].hover();
      await expect(
        page.locator(
          `${dropdownSelector}:nth-of-type(${i + 1}) .tw-nav-accordion-content-inner`
        )
      ).toBeVisible();
      // Check that other dropdowns are not visible
      for (let j = 0; j < dropdowns.length; j++) {
        if (i !== j) {
          await expect(
            page.locator(
              `${dropdownSelector}:nth-of-type(${j + 1}) .tw-nav-accordion-content-inner`
            )
          ).not.toBeVisible();
        }
      }
    }
  });
});
