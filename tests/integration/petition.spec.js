const { test, expect } = require("@playwright/test");
const waitForImagesToLoad = require("../wait-for-images.js");

const TEST_CAMPAIGN_ID = "7017i000000bIgTAAU";
const PAGE_URL = "http://localhost:8000/en/campaigns/single-page";
const FA_PAGE_URL =
  "http://localhost:8000/en/campaigns/single-page/?show_formassembly=true";
const THANK_YOU_PAGE_URL =
  "http://localhost:8000/en/campaigns/single-page/?thank_you=true";
const FA_FIELDS = {
  campaignId: `input[name="tfa_1"]`,
  firstName: `input[name="tfa_28"]`,
  lastName: `input[name="tfa_30"]`,
  email: `input[name="tfa_31"]`,
  privacy: `input[name="tfa_493"]`,
  comment: `textarea[name="tfa_497"]`,
};

const TIMESTAMP = Date.now();
const TEST_EMAIL = `test-${TIMESTAMP}@example.com`;

test.describe("React form", () => {
  test("Visibility", async ({ page }) => {
    page.on("console", console.log);
    await page.goto(PAGE_URL);
    await page.locator("body.react-loaded");
    await waitForImagesToLoad(page);

    // Test if the React form is visible
    const reactForm = page.locator("#petition-form");
    // wait for the form to be attached to the DOM
    await reactForm.waitFor({ state: "visible" });
    expect(await reactForm.count()).toBe(1);
  });
});

test.describe("Signing FormAssembly petition form", () => {
  test.beforeEach(async ({ page }, testInfo) => {
    await page.goto(FA_PAGE_URL);
    await page.locator("body.react-loaded");
    await waitForImagesToLoad(page);

    // test if the FormAssembly form is visible
    const wFormContainer = page.locator(".wFormContainer");
    await wFormContainer.waitFor({ state: "visible" });
    expect(await wFormContainer.count()).toBe(1);

    // test if there's a submit button
    const submitButton = wFormContainer.locator(`input[type="submit"]`);
    expect(await submitButton.count()).toBe(1);

    // test if required fields exist and are empty (not pre-filled)
    const firstNameInput = wFormContainer.locator(FA_FIELDS.firstName);
    expect(await firstNameInput.count()).toBe(1);
    expect(await firstNameInput.inputValue()).toBe("");

    const lastNameInput = wFormContainer.locator(FA_FIELDS.lastName);
    expect(await lastNameInput.count()).toBe(1);
    expect(await lastNameInput.inputValue()).toBe("");

    const emailInput = wFormContainer.locator(FA_FIELDS.email);
    expect(await emailInput.count()).toBe(1);
    expect(await emailInput.inputValue()).toBe("");

    const privacyInput = wFormContainer.locator(FA_FIELDS.privacy);
    expect(await privacyInput.count()).toBe(1);
    expect(await privacyInput.isChecked()).toBe(false);

    // test if submitting the form without filling out the required fields creates validation errors
    // wait for submitButton's click event to be attached
    await submitButton.waitFor({ state: "attached" });
    await submitButton.click();
    expect(await page.locator(".errFld").count()).toBe(4);
    expect(await page.locator(".errMsg").count()).toBe(4);

    // test if filling out the form and submitting it eliminates the validation errors
    await firstNameInput.fill("Integration");
    await lastNameInput.fill("Test");
    await emailInput.fill(TEST_EMAIL);
    await privacyInput.check();

    // Update campaign id to TEST_CAMPAIGN_ID so this test can be submitted to FormAssembly
    // We can't use locator because the campaign id field is hidden
    await page.evaluate(
      ({ campaignFieldId, testCampaignId, note }) => {
        if (document.querySelector(campaignFieldId)) {
          document.querySelector(campaignFieldId).value = testCampaignId;
        }

        if (document.querySelector(`textarea[name="tfa_497"]`)) {
          document.querySelector(`textarea[name="tfa_497"]`).value = note;
        }
      },
      {
        campaignFieldId: FA_FIELDS.campaignId,
        testCampaignId: TEST_CAMPAIGN_ID,
        note: testInfo.title,
      }
    );

    // prepare to wait for the form to submit
    const navigationPromise = page.waitForNavigation();
    await submitButton.click();
    await navigationPromise;
  });

  test("Integration test - Signing petition", async ({ page }) => {
    // Form has been submitted successfully. Page should be redirected to thank you page
    expect(page.url()).toContain(THANK_YOU_PAGE_URL);
  });

  test("Integration test - Signing petition using the same email", async ({
    page,
  }) => {
    // We turned off a config so that Salesforce errors won't be visible to the user.
    // This means signing the petition using the same email address should still send users to the thank you page
    expect(page.url()).toContain(THANK_YOU_PAGE_URL);
  });
});

test.describe("Thank you page flow", () => {
  test.beforeEach(async ({ page }, testInfo) => {
    await page.goto(THANK_YOU_PAGE_URL);
    await page.locator("body.react-loaded");
    await waitForImagesToLoad(page);

    // test if donation modal is visible
    let modalContent = page.locator(`.modal-content`);
    await modalContent.waitFor({ state: "visible" });

    // test if donation modal can be closed using the "x" button
    const closeButton = page.locator(
      `.modal-content button[data-dismiss="modal"].close`
    );
    expect(await closeButton.count()).toBe(1);
    await closeButton.click();
    expect(await modalContent.isVisible()).toBe(false);

    // refresh page
    await page.reload();
    modalContent = page.locator(`.modal-content`);
    await modalContent.waitFor({ state: "visible" });

    // test if donation modal can be closed using the "No thanks" button
    const noThanksButton = page.locator(
      `.modal-content button.text.dismiss[data-dismiss="modal"]`
    );
    expect(await noThanksButton.count()).toBe(1);
    await noThanksButton.click();
    expect(await page.locator(`.modal-content`).isVisible()).toBe(false);
  });

  test("Donation modal can trigger FRU widget", async ({ page }) => {
    // refresh page
    await page.reload();
    let modalContent = page.locator(`.modal-content`);
    await modalContent.waitFor({ state: "visible" });

    // test if FRU iframe pops up after clicking the Yes button
    const yesDonateButton = page.locator(
      `.modal-content .tw-btn-primary[href="?form=donate"]`
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

  test("Share buttons", async ({ page }) => {
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
