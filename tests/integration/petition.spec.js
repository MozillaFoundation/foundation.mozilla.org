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
    expect(await reactForm.count()).toBe(1);
    expect(await reactForm.isVisible()).toBe(true);
  });
});

test.describe("FormAssembly form", () => {
  test("Signing petition", async ({ page }) => {
    await page.goto(FA_PAGE_URL);
    await page.locator("body.react-loaded");
    await waitForImagesToLoad(page);

    page = await fillFormAndSubmit(page);
    // Form has been submitted successfully. Page should be redirected to thank you page
    expect(page.url()).toContain(THANK_YOU_PAGE_URL);
  });

  test("Signing petition using the same email", async ({ page }) => {
    await page.goto(FA_PAGE_URL);
    await page.locator(`body.react-loaded`);
    await waitForImagesToLoad(page);

    // We turned off a config so that Salesforce errors won't be visible to the user.
    // This is signing the petition using the same email address should still send users to the thank you page
    page = await fillFormAndSubmit(page, "Dupe email. Should still go though.");
    // Submission errors encountered, page is redirected to FormAssembly hosted form page
    expect(page.url()).toContain(THANK_YOU_PAGE_URL);
  });
});

test.describe("Thank you page flow", () => {
  test("Donation modal", async ({ page }) => {
    await page.goto(THANK_YOU_PAGE_URL);
    await page.locator("body.react-loaded");
    await waitForImagesToLoad(page);

    // test if donation modal is visible
    await page.waitForSelector(`.modal-content`, { state: "attached" });
    expect(await page.locator(`.modal-content`).isVisible()).toBe(true);

    // test if donation modal can be closed using the "x" button
    const closeButton = page.locator(
      `.modal-content button[data-dismiss="modal"].close`
    );
    expect(await closeButton.count()).toBe(1);
    await closeButton.click();
    expect(await page.locator(`.modal-content`).isVisible()).toBe(false);

    // refresh page
    await page.reload();
    await page.waitForSelector(`.modal-content`, { state: "attached" });

    // test if donation modal can be closed using the "No thanks" button
    const noThanksButton = page.locator(
      `.modal-content button.text.dismiss[data-dismiss="modal"]`
    );
    expect(await noThanksButton.count()).toBe(1);
    await noThanksButton.click();
    expect(await page.locator(`.modal-content`).isVisible()).toBe(false);

    // refresh page
    await page.reload();
    await page.waitForSelector(`.modal-content`, { state: "attached" });

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

    // wait for FRU iframe to load
    await page.waitForSelector(`iframe[title="Donation Widget"]`, {
      state: "attached",
    });

    // test if FRU iframe is visible
    const widgetIframe = page.locator(`iframe[title="Donation Widget"]`);
    expect(await widgetIframe.count()).toBe(1);
    expect(await widgetIframe.isVisible()).toBe(true);
  });

  test("Share buttons", async ({ page }) => {
    await page.goto(THANK_YOU_PAGE_URL);
    await page.locator("body.react-loaded");
    await waitForImagesToLoad(page);

    // test if donation modal is visible
    await page.waitForSelector(`.modal-content`, { state: "attached" });
    expect(await page.locator(`.modal-content`).isVisible()).toBe(true);

    // test if donation modal can be closed using the "x" button
    const closeButton = page.locator(
      `.modal-content button[data-dismiss="modal"].close`
    );
    expect(await closeButton.count()).toBe(1);
    await closeButton.click();
    expect(await page.locator(`.modal-content`).isVisible()).toBe(false);

    // test if Share section is visible
    await page.waitForSelector(`.formassembly-petition-thank-you`, {
      state: "attached",
    });
    expect(
      await page.locator(`.formassembly-petition-thank-you`).isVisible()
    ).toBe(true);

    // test if Copy button is visible
    const copyButton = page.locator(
      ".formassembly-petition-thank-you button.link-share"
    );
    expect(await copyButton.count()).toBe(1);
    // check if clicking the Copy button copies the current URL (without query params) to the clipboard
    await copyButton.click();
    let clipboardText = await await page.evaluate(
      "navigator.clipboard.readText()"
    );
    let url = page.url().split("?")[0];
    expect(clipboardText).toBe(url);
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
  // wait for submitButton's click event to be attached
  await page.waitForSelector(`input[type="submit"]`, { state: "attached" });
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
