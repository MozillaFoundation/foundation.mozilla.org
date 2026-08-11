const COOKIE_CONTROL_COOKIE_NAME = "CookieControl";
const ANALYTICS_CATEGORY = "analytics";
const ACCEPTED_STATE = "accepted";

function getCookie(name) {
  const match = document.cookie.match(
    "(?:^|;)\\s*" + name + "\\s*=\\s*([^;]*)",
  );
  return match ? decodeURIComponent(match[1]) : "";
}

/**
 * Reads the Cookie Control consent cookie directly (there's no live event to
 * hook into) to check whether the user has already opted in to analytics.
 * @return {Boolean}
 */
function hasAnalyticsConsent() {
  try {
    const raw = getCookie(COOKIE_CONTROL_COOKIE_NAME);

    if (!raw) return false;

    const consent = JSON.parse(raw);

    return consent?.optionalCookies?.[ANALYTICS_CATEGORY] === ACCEPTED_STATE;
  } catch {
    return false;
  }
}

/**
 * Whether Sentry should be initialized, based on the user's privacy
 * preferences (Do Not Track and Cookie Control's analytics consent).
 * @param {Boolean} doNotTrack - GoogleAnalytics.doNotTrack, passed in by the
 * caller rather than imported here to avoid perturbing the existing
 * circular import between google-analytics.js and react-ga-proxy.js.
 * @return {Boolean}
 */
function shouldInitializeSentry(doNotTrack) {
  return !doNotTrack && hasAnalyticsConsent();
}

export default shouldInitializeSentry;
