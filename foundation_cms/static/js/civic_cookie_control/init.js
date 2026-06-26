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
      mode: response.withinEU ? "GDPR" : "CCPA", // TODO:FIXME: to be confirmed if we need to explicitly set this
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
        .map(([locale, { text }]) => ({
          locale,
          text,
        })),
    };

    // TODO:FIXME: DEV ONLY: reset consent state on every reload
    document.cookie =
      "CookieControl=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/";

    CookieControl.load(config);
  });
}
