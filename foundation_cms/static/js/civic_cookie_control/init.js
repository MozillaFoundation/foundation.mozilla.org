// Official doc from Cookie Control: https://cookiecontrol.com/docs/v9/
// GDPR/CCPA mode is based on geo location
// Locale is based on user’s browser language setting

import LOCALE_TEXT, { CCPA_TITLE } from "./text.js";

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

/**
 * Returns the text config with CCPA-specific overrides applied when in CCPA mode:
 * - `title` and `settings` are set to the CCPA opt-out label from CCPA_TITLE
 * - and `intro` is cleared
 * - All fields are returned as-is in GDPR mode.
 *
 * @param {object} text - CookieControl `text` config object for a locale.
 * @param {object|undefined} ccpaConfig - CCPA config for the same locale.
 * @param {boolean} withinCCPA - Whether the user is in a CCPA jurisdiction.
 * @param {string} locale - Locale key used to look up the CCPA_TITLE string.
 * @returns {object} The text config, with `title` overridden when applicable.
 */
function withCCPATitle(text, ccpaConfig, withinCCPA, locale = "en") {
  return withinCCPA && ccpaConfig
    ? {
        ...text,
        title: CCPA_TITLE[locale] ?? CCPA_TITLE.en,
        settings: CCPA_TITLE[locale] ?? CCPA_TITLE.en,
        intro: "",
      }
    : text;
}

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
    const mode = response.withinCCPA ? "ccpa" : "gdpr";
    console.log(`CookieControl mode will be set to:`, mode);

    const config = {
      apiKey: API_KEY,
      logConsent: true,
      initialState: "notify",
      product: PRODUCT_TYPE,
      theme: "dark",
      mode,
      // See CCPA config doc: https://cookiecontrol.com/docs/v9/optional-categories#ccpa-and-geolocation
      ...(response.withinCCPA && { ccpaConfig: LOCALE_TEXT.en.ccpaConfig }),
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
      text: withCCPATitle(
        LOCALE_TEXT.en.text,
        LOCALE_TEXT.en.ccpaConfig,
        response.withinCCPA,
        "en",
      ),
      necessaryCookies: [
        "OptanonConsent",
        "OptanonAlertBoxClosed",
        "OptanonControl",
        "__cfduid",
        "__cfruid",
        "__cf_bm",
        "cf_chl_2",
        "__cflb",
        "_cfuvid",
        "cf_clearance",
        "__stripe_mid",
        "__stripe_sid",
        "m",
        "CAKEPHP",
        "AWSALB",
        "AWSALBCORS",
        "AWSELBCORS",
        "AWSELB",
        "AWSALBTGCORS",
        "AWSALBTG",
        "aws-csds-token",
        "aws_lang",
        "aws-target-visitor-id",
        "aws-priv",
        "fundraiseup_cid",
        "fundraiseup_func",
        "hmt_id",
        "_sp",
        "_sp_var_233562",
        "_sp_var_233560",
        "_sp_var_233561",
        "_sp_var_233557",
        "_sp_var_233559",
        "_sp_var_233558",
        "_sp_var_233499",
        "_sp_var_233501",
        "_sp_var_233500",
        "_sp_var_227930",
        "_sp_var_228231",
        "_sp_var_227732",
        "_sp_var_227728",
        "_sp_var_227733",
        "_sp_var_225527",
        "_sp_var_225526",
        "_sp_var_227725",
        "_sp_var_227727",
        "_sp_var_227726",
        "_sp_var_225525",
        "sailthru_hid",
        "sailthru_bid",
        "brw",
        "brwConsent",
        "__Host-airtable-session",
        "__Host-airtable-session.sig",
      ],
      optionalCookies: [
        {
          name: "analytics",
          label: "Analytics Cookies for mozillafoundation.org",
          description:
            "These cookies allow us to count visits and traffic sources so we can " +
            "measure and improve the performance of our site. They help us to know " +
            "which pages are the most and least popular and see how visitors move around " +
            "the site. All information these cookies collect is aggregated and therefore anonymous. " +
            "If you do not allow these cookies we will not know when you have visited our site, " +
            "and will not be able to monitor its performance.",
          cookies: [
            "_ga",
            "_ga_*",
            "_gid",
            "_gat",
            "_dc_gtm_",
            "AMP_TOKEN",
            "_gat_*",
            "_gac_",
            "__utma",
            "__utmt",
            "__utmb",
            "__utmc",
            "__utmz",
            "__utmv",
            "__utmx",
            "__utmxx",
            "FPAU",
            "FPID",
            "FPLC",
            "vuid",
            "Player",
            "continuous_play_v3",
            "fundraiseup_stat",
          ],
          onAccept: function () {
            gtag("consent", "update", { analytics_storage: "granted" });
          },
          onRevoke: function () {
            gtag("consent", "update", { analytics_storage: "denied" });
          },
        },
        {
          name: "marketing",
          label: "Marketing Cookies for mozillafoundation.org",
          description:
            "These cookies may be set through our site by our advertising partners. " +
            "They may be used by those companies to build a profile of your interests " +
            "and show you relevant adverts on other sites. They do not store directly " +
            "personal information, but are based on uniquely identifying your browser and " +
            "internet device. If you do not allow these cookies, you will experience less targeted advertising.",
          cookies: [
            "GPS",
            "VISITOR_INFO1_LIVE",
            "PREF",
            "YSC",
            "DEVICE_INFO",
            "LOGIN_INFO",
            "VISITOR_PRIVACY_METADATA",
            "lu",
            "xs",
            "c_user",
            "m_user",
            "pl",
            "dbln",
            "aks",
            "aksb",
            "sfau",
            "ick",
            "csm",
            "s",
            "datr",
            "sb",
            "fr",
            "oo",
            "ddid",
            "locale",
            "_fbp",
            "_fbc",
            "js_ver",
            "rc",
            "campaign_click_url",
            "wd",
            "usida",
            "presence",
            "__Secure-YNID",
            "__Secure-ROLLOUT_TOKEN",
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
      ],
      locales: Object.entries(LOCALE_TEXT)
        .filter(([locale]) => locale !== "en")
        .map(([locale, { text, ccpaConfig }]) => ({
          locale,
          text: withCCPATitle(text, ccpaConfig, response.withinCCPA, locale),
          ...(response.withinCCPA && ccpaConfig && { ccpaConfig }),
        })),
    };

    CookieControl.load(config);

    // TODO:FIXME: DEV ONLY: remove before merge into `main`
    console.log("CookieControl mode:", config.mode);
    console.log("CookieControl geoTest response:", response);
  });
}
