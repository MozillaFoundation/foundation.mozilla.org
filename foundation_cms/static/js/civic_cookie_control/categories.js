// Cookie category definitions for Civic Cookie Control v9
// cookies: list of cookie names Civic should protect when a user opts in
// onAccept/onRevoke: update Google Consent Mode v2 signals via gtag()
// https://cookiecontrol.com/docs/v9/optional-categories
//
// Cookie lists are sourced from OneTrust's cookie audit export and deduplicated by name.
// OneTrust counts cookies per domain (the same cookie on 5 domains = 5 rows), so its
// totals will be higher than the unique name counts here — this is expected and correct.
//
// Google Consent Mode v2 parameter mapping:
//   functional             → no gtag signal (no Consent Mode v2 parameter covers UX/functional cookies)
//   performance            → analytics_storage (controls GA4 and analytics tracking)
//   personalized_advertising → ad_storage, ad_personalization, ad_user_data (controls ad targeting)
// Reference: https://cookiecontrol.com/docs/v9/optional-categories#integration-with-ga4-and-google-consent-mode-v2

const COOKIE_CATEGORIES = [
  {
    name: "functional",
    cookies: [
      "AWSALBTG",
      "AWSALBTGCORS",
      "__Host-airtable-session",
      "__Host-airtable-session.sig",
      "__Host-airtable-target-cell",
      "__Host-airtable-target-cell.sig",
      "__cf_bm",
      "__stripe_mid",
      "__stripe_sid",
      "_cfuvid",
      "_dd_s",
      "_sp_var_227725",
      "_sp_var_227726",
      "_sp_var_227727",
      "_sp_xxxxxxxxxx",
      "acq",
      "acq.sig",
      "brw",
      "brwConsent",
      "fundraiseup_func",
      "login-status-p",
      "vuid",
    ],
    onAccept: function () {},
    onRevoke: function () {},
  },
  {
    name: "performance",
    cookies: [
      "AWSALBTG",
      "AWSALBTGCORS",
      "__Host-airtable-session",
      "__Host-airtable-session.sig",
      "__Host-airtable-target-cell",
      "__Host-airtable-target-cell.sig",
      "__cf_bm",
      "__stripe_mid",
      "__stripe_sid",
      "_cfuvid",
      "_dd_s",
      "_ga",
      "_ga_xxxxxxxxxx",
      "_gat",
      "_gid",
      "_sp_var_227725",
      "_sp_var_227726",
      "_sp_var_227727",
      "_sp_xxxxxxxxxx",
      "acq",
      "acq.sig",
      "brw",
      "brwConsent",
      "fundraiseup_func",
      "fundraiseup_stat",
      "login-status-p",
      "vuid",
    ],
    onAccept: function () {
      gtag("consent", "update", {
        analytics_storage: "granted",
      });
    },
    onRevoke: function () {
      gtag("consent", "update", {
        analytics_storage: "denied",
      });
    },
  },
  {
    name: "personalized_advertising",
    cookies: [
      "AWSALBTG",
      "AWSALBTGCORS",
      "NID",
      "TESTCOOKIESENABLED",
      "VISITOR_INFO1_LIVE",
      "VISITOR_PRIVACY_METADATA",
      "YSC",
      "__Host-airtable-session",
      "__Host-airtable-session.sig",
      "__Host-airtable-target-cell",
      "__Host-airtable-target-cell.sig",
      "__Secure-ROLLOUT_TOKEN",
      "__Secure-YEC",
      "__Secure-YNID",
      "__Secure-xxxxxxx",
      "__cf_bm",
      "__stripe_mid",
      "__stripe_sid",
      "_cfuvid",
      "_dd_s",
      "_ga",
      "_ga_xxxxxxxxxx",
      "_gat",
      "_gat_UA-",
      "_gid",
      "_sp_var_227725",
      "_sp_var_227726",
      "_sp_var_227727",
      "_sp_xxxxxxxxxx",
      "acq",
      "acq.sig",
      "brw",
      "brwConsent",
      "fundraiseup_func",
      "fundraiseup_stat",
      "login-status-p",
      "vuid",
    ],
    onAccept: function () {
      gtag("consent", "update", {
        ad_storage: "granted",
        ad_personalization: "granted",
        ad_user_data: "granted",
      });
    },
    onRevoke: function () {
      gtag("consent", "update", {
        ad_storage: "denied",
        ad_personalization: "denied",
        ad_user_data: "denied",
      });
    },
  },
];

export default COOKIE_CATEGORIES;
