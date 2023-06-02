module.exports = {
  TEST_CAMPAIGN_ID: "7017i000000bIgTAAU",
  FA_PAGE_QUERY: "show_formassembly=true",
  THANK_YOU_PAGE_QUERY: "thank_you=true",
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
  generateUrl: function (locale = "en", queryString = "") {
    let pageUrl = `http://localhost:8000/${locale}/campaigns/single-page/`;

    return queryString ? `${pageUrl}?${queryString}` : pageUrl;
  },
};
