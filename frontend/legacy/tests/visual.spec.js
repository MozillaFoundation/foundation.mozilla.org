const { test } = require("@playwright/test");
const percySnapshot = require("@percy/playwright");
const waitForImagesToLoad = require("./wait-for-images.js");
const FoundationURLs = require("./foundation-urls.js");
const MozfestURLs = require("./mozfest-urls.js");
const { foundationBaseUrl, mozfestBaseUrl } = require("./base-urls.js");

const runTime = Date.now();

async function waitForReactAndImagesToLoad(page) {
  // Wait until React has fully loaded and applied the "react-loaded" class to <body>
  await page.waitForFunction(() =>
    document.body.classList.contains("react-loaded")
  );
  await waitForImagesToLoad(page);
}

async function waitForCookieBanner(page) {
  const BUTTON_IDS = {
    accept: "onetrust-accept-btn-handler",
    decline: "onetrust-reject-all-handler",
    settings: "onetrust-pc-btn-handler",
  };
  const CONTAINER_ID = "onetrust-button-group";

  try {
    // Wait for OneTrust banner to be visible
    await page.waitForSelector("#onetrust-banner-sdk", {
      state: "visible",
      timeout: 10000,
    });

    // Wait for buttons to have actual text content
    await page.waitForFunction(
      ({ buttonIds }) => {
        const buttons = Object.values(buttonIds).map((id) =>
          document.getElementById(id)
        );

        return buttons.every((btn) => btn && btn.textContent.trim().length > 0);
      },
      { timeout: 10000 },
      { buttonIds: BUTTON_IDS }
    );

    // Wait for OptanonWrapper to rearrange buttons
    await page.waitForFunction(
      ({ buttonIds, containerId }) => {
        const container = document.getElementById(containerId);
        if (!container) return false;

        return Object.values(buttonIds).every((id) => {
          const btn = document.getElementById(id);
          return btn && container.contains(btn);
        });
      },
      { timeout: 5000 },
      { buttonIds: BUTTON_IDS, containerId: CONTAINER_ID }
    );

    // Wait for text to stabilize
    await page.waitForFunction(
      ({ buttonIds }) => {
        const getText = (id) =>
          document.getElementById(id)?.textContent.trim() || "";

        const getButtonTexts = () => ({
          accept: getText(buttonIds.accept),
          decline: getText(buttonIds.decline),
          settings: getText(buttonIds.settings),
        });

        return new Promise((resolve) => {
          const previousTexts = getButtonTexts();

          setTimeout(() => {
            const currentTexts = getButtonTexts();

            // Check all texts are unchanged and non-empty
            const isStable = Object.keys(previousTexts).every(
              (key) =>
                currentTexts[key] === previousTexts[key] &&
                currentTexts[key].length > 0
            );

            resolve(isStable);
          }, 500);
        });
      },
      { timeout: 10000 },
      { buttonIds: BUTTON_IDS }
    );

    // Add extra safety delay for any CSS transitions
    await page.waitForTimeout(1000);

    // Ensure all network requests are complete
    await page.waitForLoadState("networkidle");
  } catch (error) {
    console.error(`Cookie banner wait failed: ${error.message}`);
  }
}

/**
 * Screenshot task runner
 *
 * @param {String} baseUrl domain with locale. e.g., http://localhost:8000/en or http://mozfest.localhost:8000/en
 * @param {String} path path may or may not contain query string
 * @returns
 */
function testURL(baseUrl, path, hasCookieBanner = true) {
  return async ({ page }, testInfo) => {
    // append trailing slash to URL only if it doesn't contain query string
    const url = `${baseUrl}${path}${path.includes("?") ? "" : "/"}`;
    console.log(url);
    await page.goto(url);
    await waitForReactAndImagesToLoad(page);
    if (hasCookieBanner) {
      await waitForCookieBanner(page);
    }

    // For PNI catalog pages we need to scroll to the bottom of the page to trigger our scroll animations as well waiting for the animation to complete for the screenshot
    if (
      [
        "/privacynotincluded",
        "/privacynotincluded/categories/toys-games",
      ].includes(path)
    ) {
      await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
      await page.waitForTimeout(2000);
    }

    // For the Donate Help page, we need to scroll the reCAPTCHA box into view so it can be rendered in Percy screenshots.
    // Note: The recaptcha box only appears in Chrome screenshots. For more info, see: https://github.com/MozillaFoundation/foundation.mozilla.org/pull/11598
    if (path == "/donate/help") {
      // Wait for the reCAPTCHA iframe to be visible
      const iframeHandle = await page.waitForSelector(
        'iframe[title="reCAPTCHA"]',
        { visible: true }
      );

      await iframeHandle.scrollIntoViewIfNeeded();

      // Wait for the reCAPTCHA iframe's internal document to fully load
      const frame = await iframeHandle.contentFrame();
      await frame.waitForLoadState("load"); // Ensures iframe content is fully loaded

      // Ensure all network requests are complete before snapshot
      await page.waitForLoadState("networkidle");
    }

    await percySnapshot(page, testInfo.title);
    await page.screenshot({
      path: `tests/screenshots/${runTime}/${testInfo.title}.png`,
      fullPage: true,
    });
  };
}

// fall-through call for foundation URLs
function testFoundationURL(path, locale = `en`) {
  return testURL(foundationBaseUrl(locale), path, true);
}

// fall-through call for mozfest URLs
function testMozfestURL(path, locale = `en`) {
  return testURL(mozfestBaseUrl(locale), path, false);
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
