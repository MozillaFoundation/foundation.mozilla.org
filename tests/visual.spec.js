const { test } = require("@playwright/test");
const percySnapshot = require("@percy/playwright");
const waitForImagesToLoad = require("./wait-for-images.js");
const FoundationURLs = require("./foundation-urls.js");
const MozfestURLs = require("./mozfest-urls.js");

const runTime = Date.now();
/**
 * Screenshot task runner
 *
 * @param {String} domain http://localhost:8000 or http://mozfest.localhost:8000
 * @param {String} path the URL path to screenshot
 * @returns
 */
function testURL(domain, path) {
  return async ({ page }, testInfo) => {
    const url = `${domain}${path}/`;
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
  return testURL(`http://localhost:8000/${locale}`, path);
}

// fall-through call for mozfest URLs
function testMozfestURL(path, locale = `en`) {
  return testURL(`http://mozfest.localhost:8000/${locale}`, path);
}

test.describe.parallel(`Foundation page tests`, () => {
  Object.entries(FoundationURLs).forEach(async ([testName, path]) => {
    test(`Foundation ${testName}`, testFoundationURL(path));
  });
});

test.describe.parallel(`Mozfest page tests`, () => {
  Object.entries(MozfestURLs).forEach(([testName, path]) => {
    test(`Mozfest ${testName}`, testMozfestURL(path));
  });
});
