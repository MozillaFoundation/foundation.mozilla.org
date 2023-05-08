const { test, expect } = require("@playwright/test");
const FoundationURLs = require("./foundation-urls.js");
const MozfestURLs = require("./mozfest-urls.js");

/**
 * Test to see if the given URL can be loaded
 * and visiting it returns a successful response (status 200)
 * @param {String} domain
 * @param {String} path
 */
function testURL(domain, path) {
  return async ({ page }) => {
    const url = `${domain}${path}/`;
    const response = await page.goto(url);
    expect(response.status()).toBe(200);
  };
}

function testFoundationURL(path, locale = `en`) {
  return testURL(`http://localhost:8000/${locale}`, path);
}

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
