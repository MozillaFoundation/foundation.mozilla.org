export default async function waitForImagesToLoad(page) {
  // Trigger lazy images to load by scrolling them into view
  await page.evaluate(() => {
    document.querySelectorAll("img").forEach((img) => {
      if (img.loading === "lazy" && !img.complete && img.offsetParent !== null) {
        img.scrollIntoView();
      }
    });
  });

  // Wait until all visible images report complete
  await page.waitForFunction(
    () => {
      const imgs = Array.from(document.querySelectorAll("img"));
      const visible = imgs.filter((img) => img.offsetParent !== null);
      return visible.every((img) => img.complete);
    },
    { timeout: 10000, polling: 500 }
  );
}
