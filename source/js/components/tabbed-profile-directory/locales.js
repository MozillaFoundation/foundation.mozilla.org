import data from "./locale-strings";

const DEFAULT_LOCALE = `en`;
let currentLocale = false;

/**
 * This does a one-time fetch of the current locale based on the
 * current URL. It simply checks what the very first part of the
 * path-after-the-domain is, and tries to resolve that as a locale.
 * @return {string} The current locale string
 */
function getCurrentLanguage() {
  if (typeof window === `undefined` || !window.location) {
    return DEFAULT_LOCALE;
  }

  if (!currentLocale) {
    var pathsegments = window.location.pathname.split(`/`).filter((v) => v);

    currentLocale = pathsegments.length > 0 ? pathsegments[0] : DEFAULT_LOCALE;
  }

  return currentLocale || DEFAULT_LOCALE;
}

/**
 * Get a localized string either for an explicitly known locale,
 * or whatever is the current locale based on the page URL.
 * @param {string} key the string key to localize
 * @param {string} locale the locale for which to fetch the localized key (optional, defaults to current URL locale)
 * @return {string} the localised key (with fall-back to the default localized string, and the key itself)
 */
function getText(key, locale) {
  if (!locale) {
    locale = getCurrentLanguage();
  }

  if (!data[locale]) {
    locale = DEFAULT_LOCALE;
  }

  return data[locale][key] || key;
}

export { getText, getCurrentLanguage };
