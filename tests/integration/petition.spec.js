const { test, expect } = require("@playwright/test");
const waitForImagesToLoad = require("../wait-for-images.js");

const TEST_CAMPAIGN_ID = "7017i000000bIgTAAU";
const PAGE_URL = "http://localhost:8000/en/campaigns/single-page";
const FA_PAGE_URL =
  "http://localhost:8000/en/campaigns/single-page/?show_formassembly=true";
const THANK_YOU_PAGE_URL =
  "http://localhost:8000/en/campaigns/single-page/?thank_you=true";
const FA_HOSTED_PAGE_URL =
  "https://mozillafoundation.tfaforms.net/forms/legacyView/9";
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

    // test if the React form is visible
    const reactForm = page.locator("#petition-form");
    expect(await reactForm.count()).toBe(1);
    expect(await reactForm.isVisible()).toBe(true);
  });
});

test.describe("FormAssembly form", () => {
  test("Visibility and validation", async ({ page }) => {
    await page.goto(FA_PAGE_URL);
    await page.locator("body.react-loaded");
    await waitForImagesToLoad(page);

    page = await fillFormAndSubmit(page);
    // form has been submitted successfully. Page should be redirected to thank you page
    expect(page.url()).toContain(THANK_YOU_PAGE_URL);
  });

  test("Signing petition using the same email", async ({ page }) => {
    // test.fixme();
    await page.goto(FA_PAGE_URL);
    await page.locator(`body.react-loaded`);
    await waitForImagesToLoad(page);

    page = await fillFormAndSubmit(page, "Dupe. Should fail.");
    // Submission errors encountered, page is redirected to FormAssembly hosted form page
    expect(page.url()).toContain(FA_HOSTED_PAGE_URL);
  });
});

async function fillFormAndSubmit(page, testNote = "Should go through.") {
  // test if the FormAssembly form is visible
  const wFormContainer = page.locator(".wFormContainer");
  expect(await wFormContainer.count()).toBe(1);
  expect(await wFormContainer.isVisible()).toBe(true);

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
    ({ campaignId, testCampaignId, note }) => {
      if (document.querySelector(campaignId)) {
        document.querySelector(campaignId).value = testCampaignId;
      }

      if (document.querySelector(`textarea[name="tfa_497"]`)) {
        document.querySelector(`textarea[name="tfa_497"]`).value = note;
      }
    },
    {
      campaignId: FA_FIELDS.campaignId,
      testCampaignId: TEST_CAMPAIGN_ID,
      note: testNote,
    }
  );

  // prepare to wait for the form to submit
  const navigationPromise = page.waitForNavigation();
  await submitButton.click();
  await navigationPromise;

  return page;
}
