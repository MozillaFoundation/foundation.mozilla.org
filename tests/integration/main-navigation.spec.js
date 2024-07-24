const { test, expect } = require("@playwright/test");
const waitForImagesToLoad = require("../wait-for-images.js");
const { foundationBaseUrl } = require("../base-urls.js");

test.describe("Main Navigation", () => {
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

  test("Mobile menu toggle", async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 });
    const menuToggle = page.locator(".burger");
    await menuToggle.click();
    await expect(page.locator(".narrow-screen-menu")).toBeVisible();
  });

  test("Navigation links lead to correct pages", async ({ page }) => {
    test.setTimeout(240000); // Set timeout to 2 minutes
    const dropdownSelector = ".tw-nav-desktop-dropdown";
    const dropdowns = await page.$$(dropdownSelector);
    for (let i = 0; i < dropdowns.length; i++) {
      const dropdownContentSelector = `.tw-nav-desktop-dropdown:nth-of-type(${i + 1}) .tw-nav-accordion-content-inner`;
      await page.hover(`${dropdownSelector}:nth-of-type(${i + 1})`);
      await page.waitForSelector(dropdownContentSelector, { state: "visible" });
      const linkData = await page.$$eval(
        `${dropdownContentSelector} a`,
        (links) =>
          links.map((link) => ({ href: link.href, text: link.textContent }))
      );

      for (const { href, text } of linkData) {
        await page.click(`${dropdownContentSelector} a[href="${href}"]`);
        if (href.includes("internethealthreport.org")) {
          await expect(page).toHaveURL(
            /https:\/\/\d{4}\.internethealthreport\.org\//
          );
        } else {
          await expect(page).toHaveURL(new RegExp(href));
        }
        await page.goBack();
        // Re-hover the dropdown after navigation
        await page.hover(`${dropdownSelector}:nth-of-type(${i + 1})`);
        await page.waitForSelector(dropdownContentSelector, {
          state: "visible",
        });
      }
    }
  });
});
