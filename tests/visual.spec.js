const { test } = require("@playwright/test");
const percySnapshot = require("@percy/playwright");
const waitForImagesToLoad = require("./wait-for-images.js");
const FoundationURLs = require("./foundation-urls.js");
const MozfestURLs = require("./mozfest-urls.js");
const { foundationBaseUrl, mozfestBaseUrl } = require("./base-urls.js");

const runTime = Date.now();
/**
 * Screenshot task runner
 *
 * @param {String} baseUrl domain with locale. e.g., http://localhost:8000/en or http://mozfest.localhost:8000/en
 * @param {String} path path may or may not contain query string
 * @returns
 */
function testURL(baseUrl, path) {
  return async ({ page }, testInfo) => {
    // append trailing slash to URL only if it doesn't contain query string
    const url = `${baseUrl}${path}${path.includes("?") ? "" : "/"}`;
    console.log(url);
    await page.goto(url);

    // Gets set once React has finished loading
    await page.locator(`body.react-loaded`);

    // For PNI catalog pages we need to scroll to the bottom of the page to trigger our scroll animations as well waiting for the animation to complete for the screenshot
    if (
      [
        "/privacynotincluded",
        "/privacynotincluded/categories/toys-games",
      ].includes(path)
    ) {
      await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
      await page.waitForTimeout(2000);
    }

    // For the Donate Help page, we need to scroll the reCAPTCHA box into view so it can be rendered in Percy screenshots.
    // Note: The recaptcha box only appears in Chrome screenshots. For more info, see: https://github.com/MozillaFoundation/foundation.mozilla.org/pull/11598
    if (path == "/donate/help") {
      // Wait for the reCAPTCHA iframe to be visible
      const iframeHandle = await page.waitForSelector(
        'iframe[title="reCAPTCHA"]',
        { visible: true }
      );
      await iframeHandle.scrollIntoViewIfNeeded();
      await page.waitForTimeout(3000);
    }

    // we don't want to screenshot before images are done.
    await waitForImagesToLoad(page);

    await percySnapshot(page, testInfo.title);
    await page.screenshot({
      path: `tests/screenshots/${runTime}/${testInfo.title}.png`,
      fullPage: true,
    });
  };
}

// fall-through call for foundation URLs
function testFoundationURL(path, locale = `en`) {
  return testURL(foundationBaseUrl(locale), path);
}

// fall-through call for mozfest URLs
function testMozfestURL(path, locale = `en`) {
  return testURL(mozfestBaseUrl(locale), path);
}

async function expandDropdown(page, dropdownSelector) {
  await page.hover(dropdownSelector);
  // Wait for any animations to complete
  await page.waitForTimeout(500);
}

test.describe.parallel(`Foundation page tests`, () => {
  Object.entries(FoundationURLs).forEach(async ([testName, path]) => {
    test(`Foundation ${testName}`, testFoundationURL(path));
  });

  test(`Foundation main navigation with expanded dropdown`, async ({
    page,
  }) => {
    await page.goto(foundationBaseUrl("en"));
    await page.locator(`body.react-loaded`);
    await waitForImagesToLoad(page);
    // Expand the desired dropdown
    await expandDropdown(page, "#nav-menu-item-initiatives");
    await percySnapshot(page, "Main navigation with expanded dropdown");
  });
});

test.describe.parallel(`Mozfest page tests`, () => {
  Object.entries(MozfestURLs).forEach(([testName, path]) => {
    test(`Mozfest ${testName}`, testMozfestURL(path));
  });
});
