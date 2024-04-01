const { donateBaseUrl } = require("../../../base-urls.js");
const THANK_YOU_PAGE_QUERY_PARAM = {
  key: `thank_you`,
  value: `true`,
};

module.exports = {
  FA_FIELDS: {
    iNeedDropDown: `select[name="tfa_95"]`,
    otherDetails: `textarea[name="tfa_163"]`,
    name: `input[name="tfa_1"]`,
    email: `input[name="tfa_10"]`,
    screenshot: `input[name="tfa_214"]`,
  },
  DROP_DOWN_MENU_OPTIONS: [
    { value: "tfa_194", has_screenshot_field: true },
    { value: "tfa_195", has_screenshot_field: false },
    { value: "tfa_193", has_screenshot_field: false },
    { value: "tfa_192", has_screenshot_field: false },
    { value: "tfa_196", has_screenshot_field: false },
    { value: "tfa_197", has_screenshot_field: true },
    { value: "tfa_190", has_screenshot_field: false },
    { value: "tfa_191", has_screenshot_field: false },
    { value: "tfa_198", has_screenshot_field: false },
    { value: "tfa_199", has_screenshot_field: false },
    { value: "tfa_200", has_screenshot_field: true },
  ],
  FA_HIDDEN_FIELDS: {
    thankYouUrl: `input[name="tfa_236"]`,
    lang: `select[name="tfa_72"]`,
  },
  /**
   * Generate an URL
   *
   * @param {string} locale locale to be used in the URL
   * @param {boolean} addThankYouQueryParam whether to add the thank you query parameter to the URL
   */
  generateUrl: function (locale = "en", addThankYouQueryParam = false) {
    let baseUrl = `${donateBaseUrl(locale)}/help/?existing=query`;

    return addThankYouQueryParam
      ? `${baseUrl}&${THANK_YOU_PAGE_QUERY_PARAM.key}=${THANK_YOU_PAGE_QUERY_PARAM.value}`
      : baseUrl;
  },
  /**
   * Check if the testUrl's query parameters are identical to the expectedUrl's query parameters
   * This ensures that testUrl (e.g., a thank you page url) carries over the query parameters from the original url
   *
   * @param {string} testUrl url to be tested
   * @param {string} expectedUrl url to be compared with
   * @param {boolean} onThankYouPage whether we are currently on the thank you page
   */
  isExpectedThankYouUrl: function (
    testUrl,
    expectedUrl,
    onThankYouPage = false
  ) {
    // extract query parameters from testUrl
    const testUrlQp = new URLSearchParams(new URL(testUrl).search);
    if (!onThankYouPage) {
      testUrlQp.delete(THANK_YOU_PAGE_QUERY_PARAM.key);
    }

    // extract query parameters from expectedUrl
    const expectedQp = new URLSearchParams(new URL(expectedUrl).search);

    // convert query parameters to key-value pairs and sort them based on key
    const testUrlQpArray = Array.from(testUrlQp.entries()).sort();
    const expectedQpArray = Array.from(expectedQp.entries()).sort();

    // turn them into strings and compare if they are identical
    const matchesExpected =
      JSON.stringify(testUrlQpArray) === JSON.stringify(expectedQpArray);

    return matchesExpected;
  },
};
