export default async function waitForImagesToLoad(page) {
  // Trigger lazy images to load by scrolling them into view one at a time, so
  // the browser renders each position and starts loading that image
  for (const img of await page.locator('img[loading="lazy"]').all()) {
    if (await img.evaluate((el) => !el.complete && el.offsetParent !== null)) {
      await img.scrollIntoViewIfNeeded();
    }
  }

  // Wait until all visible images report complete
  await page.waitForFunction(
    () => {
      const imgs = Array.from(document.querySelectorAll("img"));
      const visible = imgs.filter((img) => img.offsetParent !== null);
      return visible.every((img) => img.complete);
    },
    null,
    { timeout: 10000, polling: 500 },
  );
}
