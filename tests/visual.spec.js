const { test, expect } = require("@playwright/test");
const percySnapshot = require("@percy/playwright");
const waitForImagesToLoad = require("./wait-for-images.js");
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
    await page.goto(url);

    // Gets set once React has finished loading
    await page.locator(`body.react-loaded`);

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

// Our list of foundation site URLS to check
const FoundationURLs = {
  homepage: "",
  "What you can do": "/what-you-can-do",
  "Who we are": "/who-we-are",
  "Blog index": "/blog",
  "Blog index (filtered on tag)": "/blog/tags/iot",
  "Blog index (non-existent tag)":
    "/blog/tags/randomnonsensetagthatdoesntexist",
  "Blog index (filtered on category)": "/blog/category/mozilla-festival",
  "Fixed blog post": "/blog/initial-test-blog-post-with-fixed-title",
  "Campaign index": "/campaigns",
  "Single-page campaign": "/campaigns/single-page",
  "Multi-page campaign": "/campaigns/multi-page",
  "Bannered campaign":
    "/campaigns/initial-test-bannered-campaign-with-fixed-title",
  "Publication page with child article":
    "/publication-page-with-child-article-pages",
  "Publication page with child chapter": "/publication-page-with-chapter-pages",
  "Publication page as chapter":
    "/publication-page-with-chapter-pages/fixed-title-chapter-page",
  "Article page":
    "/publication-page-with-chapter-pages/fixed-title-chapter-page/fixed-title-article-page",
  PNI: "/privacynotincluded",
  "PNI (filtered for category)": "/privacynotincluded/categories/toys-games",
  "PNI general product page": "/privacynotincluded/general-percy-product",
  "YouTube regrets": "/campaigns/youtube-regrets",
  "YouTube regrets  reporter": "/campaigns/regrets-reporter",
  "Dear Internet": "/campaigns/dearinternet",
  Styleguide: "/style-guide",
};

// Our list of Mozfest URLs to check
const MozfestURLs = {
  homepage: "",
  "Primary page": "/spaces",
};

// =================== Tests run here ===================

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
