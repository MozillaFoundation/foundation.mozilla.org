// Cookie category definitions for Civic Cookie Control v9
// cookies: list of cookie names Civic should protect when a user opts in
// onAccept/onRevoke: update Google Consent Mode v2 signals via gtag()
// https://cookiecontrol.com/docs/v9/optional-categories

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
    cookies: [], // TODO: populate from OneTrust export
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
    cookies: [], // TODO: populate from OneTrust export
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
  {
    name: "social_media",
    cookies: [], // TODO: populate from OneTrust export
    onAccept: function () {},
    onRevoke: function () {},
  },
];

export default COOKIE_CATEGORIES;
