// Official doc from Cookie Control: https://cookiecontrol.com/docs/v9/
// GDPR/CCPA mode is based on geo location
// Locale is based on user’s browser language setting

import LOCALE_TEXT from "./text.js";

const API_KEY = COOKIE_CONTROL_API_KEY;
const PRODUCT_TYPE = "CUSTOM";

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
 * - `title` and `settings` are set to the opt-out button label
 * - and `intro` is cleared
 * - All fields are returned as-is in GDPR mode.
 *
 * @param {object} text - CookieControl `text` config object for a locale.
 * @param {object|undefined} ccpaConfig - CCPA config for the same locale.
 * @param {boolean} withinCCPA - Whether the user is in a CCPA jurisdiction.
 * @returns {object} The text config, with `title` overridden when applicable.
 */
function withCCPATitle(text, ccpaConfig, withinCCPA) {
  return withinCCPA && ccpaConfig
    ? {
        ...text,
        title: ccpaConfig.rejectButton,
        settings: ccpaConfig.rejectButton,
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
      // TODO:FIXME: with real CCPA content (TP1-4027)
      // See: https://cookiecontrol.com/docs/v9/optional-categories#ccpa-and-geolocation
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
      ),
      // TODO: (TP1-4033)
      //   1. Replace with real necessary/optional categories once defined.
      //   2. Revise the notify bar "Accept"/"Reject" button labels.
      //      They currently reference "Analytics Cookies" specifically, which may not be accurate once all optional categories are defined.
      necessaryCookies: ["placeholder-necessary-cookie"],
      optionalCookies: [
        {
          name: "placeholder-optional",
          label: "[For Testing Purpose] A Cookies Category",
          description: "Placeholder for testing — to be replaced in TP1-4033.",
          onAccept: function () {},
          onRevoke: function () {},
        },
      ],
      locales: Object.entries(LOCALE_TEXT)
        .filter(([locale]) => locale !== "en")
        .map(([locale, { text, ccpaConfig }]) => ({
          locale,
          text: withCCPATitle(text, ccpaConfig, response.withinCCPA),
          ...(response.withinCCPA && ccpaConfig && { ccpaConfig }),
        })),
    };

    // TODO:FIXME: DEV ONLY: reset consent state on every reload
    document.cookie =
      "CookieControl=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/";

    CookieControl.load(config);

    // TODO:FIXME: DEV ONLY: remove before merge into `main`
    console.log("CookieControl mode:", config.mode);
    console.log("CookieControl geoTest response:", response);
  });
}
