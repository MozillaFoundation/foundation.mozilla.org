# Test info

- Name: Donate Help Form >> (fr) Testing Form
- Location: /Users/rdivincenzo/Sites/foundation.mozilla.org/frontend/legacy/tests/integration/donate/help/001-help-form.spec.js:38:5

# Error details

```
Error: page.goto: Test ended.
Call log:
  - navigating to "http://legacy.localhost:8000/fr/donate/help/?existing=query", waiting until "load"

    at /Users/rdivincenzo/Sites/foundation.mozilla.org/frontend/legacy/tests/integration/donate/help/001-help-form.spec.js:42:35
```

# Test source

```ts
   1 | const { test, expect } = require("@playwright/test");
   2 | const waitForImagesToLoad = require("../../../wait-for-images.js");
   3 | const utility = require("./utility.js");
   4 |
   5 | test.describe("Donate Help Form", () => {
   6 |   let thankYouUrlInputValue = "";
   7 |
   8 |   // locales we support on www.mozillafoundation.org
   9 |   let foundationSupportedLocales = [
   10 |     "en",
   11 |     "de",
   12 |     "es",
   13 |     "fr",
   14 |     "fy-NL",
   15 |     "nl",
   16 |     "pl",
   17 |     "pt-BR",
   18 |     "sw",
   19 |   ];
   20 |
   21 |   // Locales supported by FormAssembly and their corresponding IDs.
   22 |   // (Locales unsupported by FA, such as SW, default to `tfa_227`)
   23 |   const formAssemblySupportedLocaleMap = {
   24 |     nl: "tfa_221",
   25 |     "fy-NL": "tfa_221",
   26 |     en: "tfa_222",
   27 |     fr: "tfa_223",
   28 |     de: "tfa_224",
   29 |     pl: "tfa_228",
   30 |     "pt-BR": "tfa_229",
   31 |     es: "tfa_231",
   32 |     other: "tfa_227",
   33 |   };
   34 |
   35 |   let localeToTest = foundationSupportedLocales[0];
   36 |
   37 |   for (const locale of foundationSupportedLocales) {
   38 |     test(`(${locale}) Testing Form`, async ({ page }) => {
   39 |       localeToTest = locale;
   40 |
   41 |       // Navigate to the URL for the current locale.
>  42 |       const response = await page.goto(utility.generateUrl(localeToTest));
      |                                   ^ Error: page.goto: Test ended.
   43 |       const status = await response.status();
   44 |       expect(status).not.toBe(404);
   45 |
   46 |       // Wait for the body to load and images to finish loading.
   47 |       await page.locator("body.react-loaded");
   48 |       await waitForImagesToLoad(page);
   49 |
   50 |       // Get the form container and wait for it to be visible.
   51 |       const wFormContainer = page.locator(".wFormContainer");
   52 |       await wFormContainer.waitFor({ state: "visible" });
   53 |       expect(await wFormContainer.count()).toBe(1);
   54 |
   55 |       // Test the "I Need..." dropdown menu exists, and is visible to the user.
   56 |       const iNeedDropDownMenu = wFormContainer.locator(
   57 |         utility.FA_FIELDS.iNeedDropDown
   58 |       );
   59 |       expect(await iNeedDropDownMenu.count()).toBe(1);
   60 |       expect(await iNeedDropDownMenu.isVisible()).toBe(true);
   61 |
   62 |       // Test that the "Name" input exists, is empty, and is not visible until the user
   63 |       // selects an option from the dropdown menu.
   64 |       const nameInput = wFormContainer.locator(utility.FA_FIELDS.name);
   65 |       expect(await nameInput.count()).toBe(1);
   66 |       expect(await nameInput.inputValue()).toBe("");
   67 |       expect(await nameInput.isVisible()).toBe(false);
   68 |
   69 |       // Test that the "Email" input exists, is empty, and is not visible until the user
   70 |       // selects an option from the dropdown menu.
   71 |       const emailInput = wFormContainer.locator(utility.FA_FIELDS.email);
   72 |       expect(await emailInput.count()).toBe(1);
   73 |       expect(await emailInput.inputValue()).toBe("");
   74 |       expect(await emailInput.isVisible()).toBe(false);
   75 |
   76 |       // Test that the "Other Details" text field exists, and is not visible until the user
   77 |       // selects an option from the dropdown menu.
   78 |       const otherDetailsTextArea = wFormContainer.locator(
   79 |         utility.FA_FIELDS.otherDetails
   80 |       );
   81 |       expect(await otherDetailsTextArea.count()).toBe(1);
   82 |       expect(await otherDetailsTextArea.inputValue()).toBe("");
   83 |       expect(await otherDetailsTextArea.isVisible()).toBe(false);
   84 |
   85 |       // Test that the optional "Screenshot" input field exists, and is not visible until the user
   86 |       // selects a supported option from the dropdown menu.
   87 |       const screenshotInput = wFormContainer.locator(
   88 |         utility.FA_FIELDS.screenshot
   89 |       );
   90 |       expect(await screenshotInput.count()).toBe(1);
   91 |       expect(await screenshotInput.getAttribute("type")).toBe("file");
   92 |       expect(await screenshotInput.isVisible()).toBe(false);
   93 |
   94 |       // Test that the "Lang" input exists, and is hidden.
   95 |       const langInput = wFormContainer.locator(utility.FA_HIDDEN_FIELDS.lang);
   96 |       expect(await langInput.count()).toBe(1);
   97 |       expect(await langInput.isHidden()).toBe(true);
   98 |
   99 |       // Test that the "Lang" input value is being prepopulated with the correct FA language code.
  100 |       if (localeToTest in formAssemblySupportedLocaleMap) {
  101 |         expect(await langInput.inputValue()).toBe(
  102 |           formAssemblySupportedLocaleMap[localeToTest]
  103 |         );
  104 |       } else {
  105 |         // If current page locale is not supported by FA, the input should default to the value of "Other".
  106 |         expect(await langInput.inputValue()).toBe(
  107 |           formAssemblySupportedLocaleMap["other"]
  108 |         );
  109 |       }
  110 |
  111 |       // Test that the "Thank You Url" input exists, is hidden, and is prepopulated with the appropriate "thank you" URL.
  112 |       const thankYouUrlInput = wFormContainer.locator(
  113 |         utility.FA_HIDDEN_FIELDS.thankYouUrl
  114 |       );
  115 |       expect(await thankYouUrlInput.count()).toBe(1);
  116 |       expect(await thankYouUrlInput.isHidden()).toBe(true);
  117 |       thankYouUrlInputValue = await thankYouUrlInput.inputValue();
  118 |       // test if the thank you url in the input field is correct
  119 |       expect(
  120 |         utility.isExpectedThankYouUrl(thankYouUrlInputValue, page.url(), false)
  121 |       ).toBe(true);
  122 |
  123 |       // Test that the "Submit" button exists, initially renders as "disabled", and is hidden until the user selects an option from the drowpdown menu.
  124 |       const submitButton = wFormContainer.locator(`input[type="submit"]`);
  125 |       expect(await submitButton.count()).toBe(1);
  126 |       expect(await submitButton.isVisible()).toBe(false);
  127 |       expect(await submitButton.isEnabled()).toBe(false);
  128 |
  129 |       // Remove the disabled attribute from the "Submit" button for testing purposes.
  130 |       await submitButton.evaluate((el) => el.removeAttribute("disabled"));
  131 |
  132 |       // Loop through each option of the "I Need..." dropdown element, and make sure that the appropriate input fields render.
  133 |       for (const option of utility.DROP_DOWN_MENU_OPTIONS) {
  134 |         await iNeedDropDownMenu.selectOption({ value: option.value });
  135 |
  136 |         expect(await nameInput.isVisible()).toBe(true);
  137 |         expect(await emailInput.isVisible()).toBe(true);
  138 |         expect(await otherDetailsTextArea.isVisible()).toBe(true);
  139 |         expect(await submitButton.isVisible()).toBe(true);
  140 |
  141 |         // If this option is set to include the optional screenshot field, make sure that it renders too.
  142 |         if (option.has_screenshot_field) {
```