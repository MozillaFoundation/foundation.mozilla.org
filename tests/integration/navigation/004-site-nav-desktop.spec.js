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
    const dropdowns = [
      ".tw-nav-desktop-dropdown:nth-of-type(1)",
      ".tw-nav-desktop-dropdown:nth-of-type(2)",
      ".tw-nav-desktop-dropdown:nth-of-type(3)",
      ".tw-nav-desktop-dropdown:nth-of-type(4)",
      ".tw-nav-desktop-dropdown:nth-of-type(5)",
    ];

    for (const dropdown of dropdowns) {
      await page.hover(dropdown);
      await expect(
        page.locator(`${dropdown} .tw-nav-accordion-content-inner`)
      ).toBeVisible();
    }
  });
});
