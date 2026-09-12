import { test } from "@playwright/test";
import percySnapshot from "@percy/playwright";
import waitForImagesToLoad from "./wait-for-images.js";
import { foundationBaseUrl } from "./base-urls.js";
import RedesignURLs from "./redesign-urls.js";

const runTime = Date.now();

function testFoundationURL(path) {
  return async ({ page }, testInfo) => {
    // page.goto() already waits for the "load" event by default. We deliberately
    // don't also wait for "networkidle" here: pages with a live embed (e.g. a
    // Vimeo iframe in a video_block) can keep making background network calls
    // indefinitely, which means networkidle may never resolve even though the
    // page is fully rendered. waitForImagesToLoad below is our actual
    // readiness check before snapshotting.
    await page.goto(`${foundationBaseUrl()}${path}`);
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
