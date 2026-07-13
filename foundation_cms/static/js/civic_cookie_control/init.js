// Official doc from Cookie Control: https://cookiecontrol.com/docs/v9/
// GDPR/CCPA mode is based on geo location
// Locale is based on user’s browser language setting

import LOCALE_TEXT from "./text.js";

const API_KEY = COOKIE_CONTROL_API_KEY;
const PRODUCT_TYPE = "PRO_MULTISITE";

// Design system colour tokens (mirrors _colors.scss)
const COLORS = {
  blue90: "#0040d4",
  neutral200: "#eeeeee",
  neutral600: "#161616",
  orange200: "#f88539",
  white: "#ffffff",
  black: "#000000",
};

if (!COOKIE_CONTROL_API_KEY) {
  console.error(
    "COOKIE_CONTROL_API_KEY is not configured — skipping cookie consent init.",
  );
} else if (typeof CookieControl === "undefined") {
  console.warn(
    "CookieControl library not loaded — skipping cookie consent init.",
  );
} else {
  CookieControl.geoTest(PRODUCT_TYPE, API_KEY, function (response) {
    const config = {
      apiKey: API_KEY,
      logConsent: true,
      initialState: "notify",
      product: PRODUCT_TYPE,
      theme: "dark",
      branding: {
        // type
        fontFamily: '"Mozilla Text", "Helvetica Neue", Arial, sans-serif',
        // colours
        alertText: COLORS.white,
        alertBackground: COLORS.neutral200,
        backgroundColor: COLORS.blue90,
        // buttons
        acceptText: COLORS.white,
        acceptBackground: COLORS.black,
        rejectText: COLORS.white,
        rejectBackground: COLORS.black,
        // toggles
        toggleText: COLORS.neutral600,
        toggleBackground: COLORS.orange200,
        toggleColor: COLORS.white,
        removeAbout: false,
      },
      accessibility: {
        overlay: false,
        highlightFocus: true,
        outline: true,
      },
      text: LOCALE_TEXT.en.text,
      // TODO: (TP1-4033)
      //   1. Replace with real necessary/optional categories once defined.
      //   2. Revise the notify bar "Accept"/"Reject" button labels.
      //      They currently reference "Analytics Cookies" specifically, which may not be accurate once all optional categories are defined.
      necessaryCookies: ["OptanonConsent", "OptanonAlertBoxClosed", "OptanonControl",
                         "__cfduid", "__cfruid", "__cf_bm", "cf_chl_2", "__cflb",
                         "_cfuvid", "cf_clearance", "__stripe_mid", "__stripe_sid",
                         "m", "CAKEPHP", "AWSALB", "AWSALBCORS", "AWSELBCORS",
                         "AWSELB", "AWSALBTGCORS", "AWSALBTG", "aws-csds-token",
                         "aws_lang", "aws-target-visitor-id", "aws-priv",
                         "fundraiseup_cid", "fundraiseup_func", "_sp_var_227725",
                         "_sp_var_227727", "_sp_var_227726", "brw", "brwConsent",
                         "__Host-airtable-session", "__Host-airtable-session.sig"
                        ],
      optionalCookies: [
        {
          name: "analytics",
          label: "Analytics Cookies for mozillafoundation.org",
          description: "These cookies allow us to count visits and traffic sources so we can " +
                       "measure and improve the performance of our site. They help us to know " +
                       "which pages are the most and least popular and see how visitors move around " +
                       "the site. All information these cookies collect is aggregated and therefore anonymous. " +
                       "If you do not allow these cookies we will not know when you have visited our site, " +
                       "and will not be able to monitor its performance.",
          cookies: ["_ga", "_ga_*", "_gid", "_gat", "_dc_gtm_", "AMP_TOKEN",
                    "_gat_*", "_gac_", "__utma", "__utmt", "__utmb",
                    "__utmc", "__utmz", "__utmv", "__utmx", "__utmxx",
                    "FPAU", "FPID", "FPLC", "vuid", "Player",
                    "continuous_play_v3", "fundraiseup_stat"
                  ],
          onAccept: function(){
              gtag("consent", "update", {"analytics_storage": "granted"});
          },
          onRevoke: function(){
              gtag("consent", "update", {"analytics_storage": "denied"});
          }
        },
        {
          name: "marketing",
          label: "Marketing Cookies for mozillafoundation.org",
          description: "These cookies may be set through our site by our advertising partners. " +
                       "They may be used by those companies to build a profile of your interests " +
                       "and show you relevant adverts on other sites. They do not store directly " +
                       "personal information, but are based on uniquely identifying your browser and " +
                       "internet device. If you do not allow these cookies, you will experience less targeted advertising.",
          "cookies": ["GPS", "VISITOR_INFO1_LIVE", "PREF", "YSC",
                      "DEVICE_INFO", "LOGIN_INFO", "VISITOR_PRIVACY_METADATA",
                      "lu", "xs", "c_user", "m_user", "pl", "dbln", "aks",
                      "aksb", "sfau", "ick", "csm", "s", "datr", "sb",
                      "fr", "oo", "ddid", "locale", "_fbp", "_fbc",
                      "js_ver", "rc", "campaign_click_url", "wd", "usida", "presence"
                    ],
          onAccept: function(){
              gtag("consent", "update", {"ad_storage": "granted", "ad_personalization": "granted", "ad_user_data": "granted"});
          },
          onRevoke: function(){
              gtag("consent", "update", {"ad_storage": "denied", "ad_personalization": "denied", "ad_user_data": "denied"});
          }
        }
      ],
      locales: Object.entries(LOCALE_TEXT)
        .filter(([locale]) => locale !== "en")
        .map(([locale, { text }]) => ({
          locale,
          text,
        })),
    };

    // TODO:FIXME: DEV ONLY: reset consent state on every reload
    document.cookie =
      "CookieControl=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/";

    CookieControl.load(config);

    // TODO:FIXME: DEV ONLY: remove before merge into `main`
    console.log("CookieControl geoTest response:", response);
  });
}
