const { test, expect } = require("@playwright/test");
const waitForImagesToLoad = require("../../wait-for-images.js");
const utility = require("./utility.js");

test.describe("Donation modal", () => {
  test.beforeEach(async ({ page }) => {
    const response = await page.goto(utility.generateUrl("en", true));
    const status = await response.status();
    expect(status).not.toBe(404);
    await page.locator("body.react-loaded");
    await waitForImagesToLoad(page);

    // test if donation modal is visible
    let modalContent = page.locator(`.modal-content`);
    await modalContent.waitFor({ state: "visible" });
  });

  test("ShareProgress script is included in the DOM", async ({ page }) => {
    const spScriptUrl = "https://c.shpg.org/352/sp.js";

    // Check if the ShareProgress script is present in the DOM
    const scriptElement = await page.$(`script[src="${spScriptUrl}"]`);
    expect(scriptElement).not.toBeNull();
  });

  test("Donation modal can be closed using the 'x' button", async ({
    page,
  }) => {
    // test if donation modal can be closed using the "x" button
    const closeButton = page
      .locator(".modal-content")
      .getByRole("button", { name: "Close" });
    expect(await closeButton.count()).toBe(1);
    await closeButton.click();
    expect(await page.locator(`.modal-content`).isVisible()).toBe(false);
  });

  test("Donation modal can be closed using the 'No thanks' button", async ({
    page,
  }) => {
    // test if donation modal can be closed using the "No thanks" button
    const noThanksButton = page
      .locator(".modal-content")
      .getByRole("button", { name: "No thanks" });
    expect(await noThanksButton.count()).toBe(1);
    await noThanksButton.click();
    expect(await page.locator(`.modal-content`).isVisible()).toBe(false);
  });

  test("Donation modal can trigger FRU widget", async ({ page }) => {
    // test if FRU iframe pops up after clicking the Yes button
    const yesDonateButton = page.locator(
      `.modal-content .tw-btn-primary[href*="?form=donate&c_id="]`
    );
    expect(await yesDonateButton.count()).toBe(1);

    const navigationPromise = page.waitForNavigation();
    await yesDonateButton.click();
    await navigationPromise;

    // check if URL contains query parameter "form=donate"
    expect(page.url()).toContain(`form=donate`);

    // test if FRU iframe is visible
    const widgetIframe = page.locator(`iframe[title="Donation Widget"]`);
    await widgetIframe.waitFor({ state: "visible" });
    expect(await widgetIframe.count()).toBe(1);
  });
});

test.describe("Share buttons", () => {
  test.beforeEach(async ({ page }) => {
    const response = await page.goto(utility.generateUrl("en", true));
    const status = await response.status();
    expect(status).not.toBe(404);
    await page.locator("body.react-loaded");
    await waitForImagesToLoad(page);

    // test if donation modal is visible
    let modalContent = page.locator(`.modal-content`);
    await modalContent.waitFor({ state: "visible" });

    // test if donation modal can be closed using the "x" button
    const closeButton = page
      .locator(".modal-content")
      .getByRole("button", { name: "Close" });
    expect(await closeButton.count()).toBe(1);
    await closeButton.click();
    expect(await page.locator(`.modal-content`).isVisible()).toBe(false);

    // test if Share section is visible
    let shareSection = page.locator(`.formassembly-petition-thank-you`);
    await shareSection.waitFor({ state: "visible" });
  });

  test("Facebook share button (linked with ShareProgress)", async ({ page }) => {
    // Because it's mostly ShareProgress's script doing the magic,
    // we can only test if an anchor element is injected by ShareProgress
    const facebookButton = page.locator("#share-progress-fb a");
    expect(await facebookButton.count()).toBe(1);
  });

  test("Twitter share button (linked with ShareProgress)", async ({ page }) => {
    // Because it's mostly ShareProgress's script doing the magic,
    // we can only test if an anchor element is injected by ShareProgress
    const twitterButton = page.locator("#share-progress-tw a");
    expect(await twitterButton.count()).toBe(1);
  });

  test("Email share button (linked with ShareProgress)", async ({ page }) => {
    // Because it's mostly ShareProgress's script doing the magic,
    // we can only test if an anchor element is injected by ShareProgress
    const twitterButton = page.locator("#share-progress-em a");
    expect(await twitterButton.count()).toBe(1);
  });

  test("Copy button", async ({ page }) => {
    // test if Share section is visible
    let shareSection = page.locator(`.formassembly-petition-thank-you`);
    await shareSection.waitFor({ state: "visible" });

    // test if Copy button is visible
    const copyButton = page.locator(
      ".formassembly-petition-thank-you button.link-share"
    );
    expect(await copyButton.count()).toBe(1);
    // check if clicking the Copy button copies the current URL (without query params) to the clipboard
    await copyButton.click();
    let clipboardText = await page.evaluate("navigator.clipboard.readText()");
    let url = page.url().split("?")[0];
    expect(clipboardText).toBe(url);
  });
});
