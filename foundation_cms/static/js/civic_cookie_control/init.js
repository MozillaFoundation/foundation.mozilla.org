// Official doc from Cookie Control: https://cookiecontrol.com/docs/v9/
// GDPR/CCPA mode is based on geo location
// Locale is based on user’s browser language setting

import LOCALE_TEXT from "./text.js";
import COOKIE_CATEGORIES from "./categories.js";

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
      optionalCookies: LOCALE_TEXT.en.optionalCookies.map((cookie) => ({
        ...cookie,
        ...COOKIE_CATEGORIES.find((c) => c.name === cookie.name),
      })),
      locales: Object.entries(LOCALE_TEXT)
        .filter(([locale]) => locale !== "en")
        .map(([locale, { text, optionalCookies }]) => ({
          locale,
          text,
          ...(optionalCookies && {
            optionalCookies: optionalCookies.map((cookie) => ({
              ...cookie,
              ...COOKIE_CATEGORIES.find((c) => c.name === cookie.name),
            })),
          }),
        })),
    };

    // TODO:FIXME: DEV ONLY: reset consent state on every reload
    document.cookie =
      "CookieControl=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/";

    CookieControl.load(config);
  });
}
