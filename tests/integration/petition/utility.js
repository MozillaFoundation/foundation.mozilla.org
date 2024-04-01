const { foundationBaseUrl } = require("../../base-urls.js");

const THANK_YOU_PAGE_QUERY_PARAM = {
  key: `thank_you`,
  value: `true`,
};

module.exports = {
  TEST_CAMPAIGN_ID: "7014x0000001RPRAA2", // test campaign id used for Salesforce Production
  FA_FIELDS: {
    firstName: `input[name="tfa_28"]`,
    lastName: `input[name="tfa_30"]`,
    email: `input[name="tfa_31"]`,
    privacy: `input[name="tfa_493"]`,
    comment: `textarea[name="tfa_497"]`,
  },
  FA_HIDDEN_FIELDS: {
    campaignId: `input[name="tfa_1"]`,
    thankYouUrl: `input[name="tfa_500"]`,
    sourceUrl: `input[name="tfa_498"]`,
    lang: `input[name="tfa_499"]`,
    newsletter: `input[name="tfa_501"]`,
  },
  /**
   * Generate an URL
   *
   * @param {string} locale locale to be used in the URL
   * @param {boolean} addThankYouQueryParam whether to add the thank you query parameter to the URL
   */
  generateUrl: function (locale = "en", addThankYouQueryParam = false) {
    let baseUrl = `${foundationBaseUrl(locale)}/campaigns/single-page/?existing=query`;

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
    onThankYouPage = false,
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
