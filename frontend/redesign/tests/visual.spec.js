import { test, expect } from "@playwright/test";
import percySnapshot from "@percy/playwright";
import waitForImagesToLoad from "./wait-for-images.js";
import { foundationBaseUrl } from "./base-urls.js";
import RedesignURLs from "./redesign-urls.js";

function testFoundationURL(path) {
  return async ({ page }, testInfo) => {
    // page.goto() already waits for the "load" event by default. We deliberately
    // don't also wait for "networkidle" here: pages with a live embed (e.g. a
    // Vimeo iframe in a video_block) can keep making background network calls
    // indefinitely, which means networkidle may never resolve even though the
    // page is fully rendered. waitForImagesToLoad below is our actual
    // readiness check before snapshotting.
    const response = await page.goto(`${foundationBaseUrl()}${path}`);
    expect(response?.status(), "Expected a successful redesign page").toBe(200);
    await expect(page.locator("body")).toHaveAttribute(
      "data-site-type",
      "redesign",
    );
    await waitForImagesToLoad(page);
    await percySnapshot(page, testInfo.title);
    await page.screenshot({
      path: testInfo.outputPath(`${testInfo.title}.png`),
      fullPage: true,
    });
  };
}

test.describe.parallel("Foundation redesign page tests", () => {
  Object.entries(RedesignURLs).forEach(([testName, path]) => {
    test(testName, testFoundationURL(path));
  });
});
