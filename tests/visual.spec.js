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
  // Wait for OneTrust banner to be visible
  await page.waitForSelector("#onetrust-banner-sdk", {
    state: "visible",
    timeout: 5000,
  });

  // Wait for button texts to stop getting updated
  // See the "onetrust_script" block in foundation_cms/legacy_cms/templates/pages/base.html for more selector info
  await page.waitForFunction(() => {
    const getText = (id) => document.getElementById(id)?.textContent.trim();

    const acceptBtnText = getText("onetrust-accept-btn-handler");
    const declineBtnText = getText("onetrust-reject-all-handler");
    const settingsBtnText = getText("onetrust-pc-btn-handler");

    // Store texts for comparison
    return new Promise((resolve) => {
      const previousText = {
        accept: acceptBtnText,
        decline: declineBtnText,
        settings: settingsBtnText,
      };
      setTimeout(() => {
        const newAcceptText = getText("onetrust-accept-btn-handler");
        const newDeclineText = getText("onetrust-reject-all-handler");
        const newSettingsText = getText("onetrust-pc-btn-handler");

        resolve(
          newAcceptText === previousText.accept &&
            newDeclineText === previousText.decline &&
            newSettingsText === previousText.settings
        );
      }, 500); // Adjust delay as needed
    });
  });

  // Ensure all network requests are complete before snapshot
  await page.waitForLoadState("networkidle");
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

async function expandDropdown(page, dropdownSelector) {
  await page.hover(dropdownSelector);
  await page.waitForSelector(dropdownSelector, { state: "visible" });
}

test.describe.parallel(`Foundation page tests`, () => {
  Object.entries(FoundationURLs).forEach(async ([testName, path]) => {
    test(`Foundation ${testName}`, testFoundationURL(path));
  });

  test(`Foundation main navigation with expanded dropdown`, async ({
    page,
  }) => {
    await page.goto(foundationBaseUrl("en"));
    await waitForReactAndImagesToLoad(page);

    const dropdowns = await page.$$(".tw-nav-desktop-dropdown");

    for (let i = 0; i < dropdowns.length; i++) {
      await expandDropdown(
        page,
        `.tw-nav-desktop-dropdown:nth-of-type(${i + 1})`
      );
      await percySnapshot(
        page,
        `Main navigation with expanded dropdown ${i + 1}`
      );
      // Reset the page state for the next dropdown
      if (i < dropdowns.length - 1) {
        await page.goto(foundationBaseUrl("en"));
        await waitForReactAndImagesToLoad(page);
      }
    }
  });
});

test.describe.parallel(`Mozfest page tests`, () => {
  Object.entries(MozfestURLs).forEach(([testName, path]) => {
    test(`Mozfest ${testName}`, testMozfestURL(path));
  });
});
