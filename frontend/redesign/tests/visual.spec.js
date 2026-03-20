import { test } from "@playwright/test";
import percySnapshot from "@percy/playwright";
import { mkdirSync } from "fs";
import waitForImagesToLoad from "./wait-for-images.js";
import { foundationBaseUrl } from "./base-urls.js";

const runTime = Date.now();
const screenshotDir = `tests/screenshots/${runTime}`;

test("Homepage", async ({ page }, testInfo) => {
  await page.goto(`${foundationBaseUrl()}/`);
  await page.waitForLoadState("networkidle");
  await waitForImagesToLoad(page);
  await percySnapshot(page, testInfo.title);
  mkdirSync(screenshotDir, { recursive: true });
  await page.screenshot({ path: `${screenshotDir}/${testInfo.title}.png`, fullPage: true });
});
