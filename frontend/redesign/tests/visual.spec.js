import { test } from "@playwright/test";
import percySnapshot from "@percy/playwright";
import waitForImagesToLoad from "./wait-for-images.js";
import { foundationBaseUrl } from "./base-urls.js";
import RedesignURLs from "./redesign-urls.js";

const runTime = Date.now();

function testFoundationURL(path) {
  return async ({ page }, testInfo) => {
    await page.goto(`${foundationBaseUrl()}${path}`);
    await page.waitForLoadState("networkidle");
    await waitForImagesToLoad(page);
    await percySnapshot(page, testInfo.title);
    await page.screenshot({
      path: `tests/screenshots/${runTime}/${testInfo.title}.png`,
      fullPage: true,
    });
  };
}

test.describe.parallel("Foundation redesign page tests", () => {
  Object.entries(RedesignURLs).forEach(([testName, path]) => {
    test(testName, testFoundationURL(path));
  });
});
