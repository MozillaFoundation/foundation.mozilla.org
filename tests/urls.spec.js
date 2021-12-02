const { test } = require("@playwright/test");

function testURL(domain, path) {
  return async ({ page }) => {
    const url = `${domain}${path}/`;
    await page.goto(url);
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
