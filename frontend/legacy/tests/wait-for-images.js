/**
 * Playwright has no built-in way to wait for all on-page images
 * to be flagged as completed, so we have our own function for that.
 * @param {Playwrite Page} page
 * @returns resolve() once all images are done, or reject() if after 20 tries images still haven't finished.
 */
module.exports = async function waitForImagesToLoad(page) {
  page.on(`console`, console.log);

  const images = page.locator("img");

  return new Promise(async (resolve, reject) => {
    let cutoff = 20;
    (async function testLoaded() {
      // force-load all lazy content
      await images.evaluateAll((imgs) => {
        const visible = Array.from(imgs).filter((i) => i.offsetParent !== null);
        visible.forEach((img) => {
          if (img.loading === `lazy` && !img.complete) img.scrollIntoView();
        });
      });

      // then check how many images aren't complete yet
      const result = await images.evaluateAll((imgs) => {
        const visible = Array.from(imgs).filter((i) => i.offsetParent !== null);
        return visible.filter((img) => !img.complete).length;
      });

      if (result === 0) {
        return resolve();
      }

      if (--cutoff === 0) {
        console.log(`Some images did not finished loading:`);
        return reject();
      }

      setTimeout(testLoaded, 500);
    })();
  });
};
