const { test, expect } = require("@playwright/test");
const FoundationURLs = require("./foundation-urls.js");
const MozfestURLs = require("./mozfest-urls.js");
const { foundationBaseUrl, mozfestBaseUrl } = require("./base-urls.js");

/**
 * Test to see if the given URL can be loaded
 * and visiting it returns a successful response (status 200)
 * @param {String} baseUrl domain with locale
 * @param {String} path path may or may not contain query string
 */
function testURL(baseUrl, path) {
  return async ({ page }) => {
    // append trailing slash to URL only if it doesn't contain query string
    const url = `${baseUrl}${path}${path.includes("?") ? "" : "/"}`;
    const response = await page.goto(url);
    expect(response.status()).toBe(200);
  };
}

function testFoundationURL(path, locale = `en`) {
  return testURL(foundationBaseUrl(locale), path);
}

function testMozfestURL(path, locale = `en`) {
  return testURL(mozfestBaseUrl(locale), path);
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
