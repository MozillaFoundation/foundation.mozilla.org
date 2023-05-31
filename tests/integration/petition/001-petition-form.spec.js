const { test, expect } = require("@playwright/test");
const waitForImagesToLoad = require("../../wait-for-images.js");
const utility = require("./utility.js");

test.describe("React form", () => {
  test("Visibility", async ({ page }) => {
    page.on("console", console.log);
    await page.goto(utility.generateUrl("en"));
    await page.locator("body.react-loaded");
    await waitForImagesToLoad(page);

    // Test if the React form is visible
    const reactForm = page.locator("#petition-form");
    // wait for the form to be attached to the DOM
    await reactForm.waitFor({ state: "visible" });
    expect(await reactForm.count()).toBe(1);
  });
});

test.describe("Localization/Lang for FormAssembly form", () => {
  // we are using pt-BR for this test
  // however, this locale variable can be any non "en" locale we support on the site
  let locale = "pt-BR";

  test.beforeEach(async ({ page }) => {
    await page.goto(utility.generateUrl(locale, utility.FA_PAGE_QUERY));
    await page.locator("body.react-loaded");
    await waitForImagesToLoad(page);
  });

  test("FormAssembly form is localized", async ({ page }) => {
    // test if the FormAssembly form is visible
    const wFormContainer = page.locator(".wFormContainer");
    await wFormContainer.waitFor({ state: "visible" });
    expect(await wFormContainer.count()).toBe(1);

    const langInput = wFormContainer.locator(utility.FA_HIDDEN_FIELDS.lang);
    expect(await langInput.count()).toBe(1);
    expect(await langInput).toBeHidden();
    expect(await langInput.inputValue()).toBe(locale);
  });
});

test.describe("Signing FormAssembly petition form", () => {
  test.beforeEach(async ({ page }, testInfo) => {
    await page.goto(utility.generateUrl("en", utility.FA_PAGE_QUERY));
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
    const firstNameInput = wFormContainer.locator(utility.FA_FIELDS.firstName);
    expect(await firstNameInput.count()).toBe(1);
    expect(await firstNameInput.inputValue()).toBe("");

    const lastNameInput = wFormContainer.locator(utility.FA_FIELDS.lastName);
    expect(await lastNameInput.count()).toBe(1);
    expect(await lastNameInput.inputValue()).toBe("");

    const emailInput = wFormContainer.locator(utility.FA_FIELDS.email);
    expect(await emailInput.count()).toBe(1);
    expect(await emailInput.inputValue()).toBe("");

    const privacyInput = wFormContainer.locator(utility.FA_FIELDS.privacy);
    expect(await privacyInput.count()).toBe(1);
    expect(await privacyInput.isChecked()).toBe(false);

    // test if hidden fields exist and are indeed hidden
    const campaignIdInput = wFormContainer.locator(
      utility.FA_HIDDEN_FIELDS.campaignId
    );
    expect(await campaignIdInput.count()).toBe(1);
    expect(await campaignIdInput).toBeHidden();

    const thankYouUrlInput = wFormContainer.locator(
      utility.FA_HIDDEN_FIELDS.thankYouUrl
    );
    expect(await thankYouUrlInput.count()).toBe(1);
    expect(await thankYouUrlInput).toBeHidden();
    expect(await thankYouUrlInput.inputValue()).toContain(
      utility.THANK_YOU_PAGE_QUERY
    );

    const sourceUrlInput = wFormContainer.locator(
      utility.FA_HIDDEN_FIELDS.sourceUrl
    );
    expect(await sourceUrlInput.count()).toBe(1);
    expect(await sourceUrlInput).toBeHidden();
    expect((await sourceUrlInput.inputValue()).split("?")[0]).toContain(
      utility.generateUrl("en")
    );

    const langInput = wFormContainer.locator(utility.FA_HIDDEN_FIELDS.lang);
    expect(await langInput.count()).toBe(1);
    expect(await langInput).toBeHidden();
    expect(await langInput.inputValue()).toBe("en");

    const newsletterInput = wFormContainer.locator(
      utility.FA_HIDDEN_FIELDS.newsletter
    );
    expect(await newsletterInput.count()).toBe(1);
    expect(await newsletterInput).toBeHidden();

    // test if submitting the form without filling out the required fields creates validation errors
    // wait for submitButton's click event to be attached
    await submitButton.waitFor({ state: "attached" });
    await submitButton.click();
    expect(await page.locator(".errFld").count()).toBe(4);
    expect(await page.locator(".errMsg").count()).toBe(4);

    // test if filling out the form and submitting it eliminates the validation errors
    await firstNameInput.fill("Integration");
    await lastNameInput.fill("Test");
    await emailInput.fill(utility.TEST_EMAIL);
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
        campaignFieldId: utility.FA_HIDDEN_FIELDS.campaignId,
        testCampaignId: utility.TEST_CAMPAIGN_ID,
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
    expect(page.url()).toContain(utility.THANK_YOU_PAGE_QUERY);
  });

  test("Integration test - Signing petition using the same email", async ({
    page,
  }) => {
    // We turned off a config so that Salesforce errors won't be visible to the user.
    // This means signing the petition using the same email address should still send users to the thank you page
    expect(page.url()).toContain(utility.THANK_YOU_PAGE_QUERY);
  });
});
