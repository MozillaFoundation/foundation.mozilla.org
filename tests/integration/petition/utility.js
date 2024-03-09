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
  THANK_YOU_PAGE_QUERY_PARAM: {
    thank_you: "true",
  },
  /**
   * Generate a base URL
   *
   * @param {string} locale locale to be used in the URL
   * @returns {string} base URL
   */
  generateBaseUrl: function (locale = "en") {
    return `http://localhost:8000/${locale}/campaigns/single-page/?existing=query`;
  },
  /**
   * Generate an URL with query parameters
   *
   * @param {string} url URL to be used as the base
   * @param {object} queryParams query parameters to be appended to the URL
   * @returns {string} URL with query parameters
   * @example
   *
   * @example
   * generateUrlWithQueryParams('http://localhost:8000/en/campaigns/single-page/?existing=query', { thank_you: 'true', test: 'true' })
   * // returns 'http://localhost:8000/en/campaigns/single-page/?existing=query&thank_you=true&test=true'
   */
  generateUrlWithQueryParams: function (url, queryParams = {}) {
    let newUrl = new URL(url);

    for (let key in queryParams) {
      newUrl.searchParams.append(key, queryParams[key]);
    }

    return newUrl.toString();
  },
  /**
   * Check if the testUrl is identical to the expectedUrl
   * This ensures that the testUrl carries over the query parameters from the original url
   * @param {string} testUrl url to be tested
   * @param {string} expectedUrl url to be compared with
   * @returns {boolean} whether the testUrl is identical to the expectedUrl
   * @example
   * isExpectedUrl(
   *  "http://localhost:8000/en/campaigns/single-page/?existing=query&thank_you=true",
   *  "http://localhost:8000/en/campaigns/single-page/?existing=query&thank_you=true"
   * )
   * // returns true
   * @example
   * isExpectedUrl(
   *  "http://localhost:8000/en/campaigns/single-page/?existing=query&thank_you=true",
   *  "http://localhost:8000/en/campaigns/single-page/?existing=query&thank_you=false"
   * )
   * // returns false
   * @example
   * isExpectedUrl(
   *   "http://localhost:8000/en/campaigns/single-page/?existing=query&thank_you=true",
   *   "http://localhost:8000/en/campaigns/single-page/?existing=query"
   *  )
   * // returns false
   * @example
   * isExpectedUrl(
   *  "http://localhost:8000/en/campaigns/single-page/?existing=query",
   *  "http://localhost:8000/en/campaigns/not-single-page/?existing=query"
   * )
   * // returns false
   */
  isExpectedUrl: function (testUrl = "", expectedUrl = "") {
    testUrl = new URL(testUrl);
    expectedUrl = new URL(expectedUrl);

    if (
      testUrl.protocol === expectedUrl.protocol &&
      testUrl.hostname === expectedUrl.hostname &&
      testUrl.pathname === expectedUrl.pathname
    ) {
      // compare if the query params in the two URLs are identical
      const testUrlQp = new URLSearchParams(testUrl.search);
      const expectedQp = new URLSearchParams(expectedUrl.search);

      // convert query parameters to key-value pairs and sort them based on key
      const testUrlQpArray = Array.from(testUrlQp.entries()).sort();
      const expectedQpArray = Array.from(expectedQp.entries()).sort();

      // turn them into strings and compare if they are identical
      return JSON.stringify(testUrlQpArray) === JSON.stringify(expectedQpArray);
    } else {
      return false;
    }
  },
};
