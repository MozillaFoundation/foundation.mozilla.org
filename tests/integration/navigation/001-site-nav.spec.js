const { test, expect } = require("@playwright/test");
const waitForImagesToLoad = require("../../wait-for-images.js");
const { foundationBaseUrl } = require("../../base-urls.js");

const MOBILE_VIEWPORT = { width: 360, height: 800 };

test.describe("Main site primary nav", () => {
  test(`Primary nav (mobile)`, async ({ page }) => {
    const PAGE_URL = `${foundationBaseUrl("en")}/`;

    await page.setViewportSize(MOBILE_VIEWPORT);
    await page.goto(PAGE_URL);
    await page.locator(`body.react-loaded`);
    await waitForImagesToLoad(page);

    const primaryNavContainer = page.locator(".primary-nav-container");
    expect(await primaryNavContainer.count()).toBe(1);

    // check if mobile nav is not visible by default
    const nav = primaryNavContainer.locator(".narrow-screen-menu-container");
    expect(await nav.count()).toBe(1);
    await expect(nav).not.toBeInViewport();

    // check if clicking the nav button shows the nav
    const navToggleButton = primaryNavContainer.locator(".burger");
    await navToggleButton.click();
    await expect(nav).toBeInViewport();

    // check if the active link is the current page
    const activeLink = nav.locator(".nav-links a.active");
    expect(await activeLink.count()).toBe(1);
    expect(await activeLink.getAttribute("href")).toBe(PAGE_URL);

    // check if clicking the nav button again hides the nav
    await navToggleButton.click();
    await expect(nav).not.toBeInViewport();
  });
});
