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
    var pathsegments = window.location.pathname.split(`/`).filter(v => v);

    currentLocale = pathsegments.length > 0 ? pathsegments[0] : DEFAULT_LOCALE;
  }

  return currentLocale || DEFAULT_LOCALE;
}

export { getCurrentLanguage };
