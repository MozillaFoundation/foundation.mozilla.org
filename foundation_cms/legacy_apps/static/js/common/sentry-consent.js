import * as Sentry from "@sentry/browser";

import initializeSentry from "./sentry-config.js";

const COOKIE_CONTROL_COOKIE_NAME = "CookieControl";
const ANALYTICS_CATEGORY = "analytics";
const ACCEPTED_STATE = "accepted";

function getCookie(name) {
  const match = document.cookie.match(
    "(?:^|;)\\s*" + name + "\\s*=\\s*([^;]*)"
  );
  return match ? decodeURIComponent(match[1]) : "";
}

/**
 * Reads the Cookie Control consent cookie directly to check whether the
 * user has opted in to analytics.
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

// Tracked separately from Sentry.isEnabled() because Sentry.close() flips
// that flag only after its internal flush() promise resolves, not
// immediately — querying it right after close() can read stale "still
// enabled" state for a beat, which is the wrong signal to gate the next
// syncSentry() call on (e.g. a revoke followed shortly by an accept).
let sentryActive = false;

/**
 * Starts or closes the Sentry client to match the user's current privacy
 * preferences. Safe to call repeatedly (e.g. on every "consent-change"
 * event) since it only acts when the desired state differs from the
 * last-known state.
 * @param {{SENTRY_DSN: string, RELEASE_VERSION: string, SENTRY_ENVIRONMENT: string}} env
 * @param {Boolean} doNotTrack - GoogleAnalytics.doNotTrack
 * @param {Boolean} [analyticsAccepted] - Known-fresh consent state from a
 * "consent-change" event's detail. Defaults to re-reading the cookie, for
 * the initial /env-load call which has no event to hand it a value —
 * Civic's onAccept/onRevoke fire before it persists the updated cookie, so
 * re-reading the cookie from inside the event handler itself would race.
 */
export function syncSentry(
  env,
  doNotTrack,
  analyticsAccepted = hasAnalyticsConsent()
) {
  if (!env?.SENTRY_DSN) return;

  const shouldRun = !doNotTrack && analyticsAccepted;

  if (shouldRun && !sentryActive) {
    initializeSentry(
      env.SENTRY_DSN,
      env.RELEASE_VERSION,
      env.SENTRY_ENVIRONMENT
    );
    sentryActive = true;
  } else if (!shouldRun && sentryActive) {
    Sentry.close();
    sentryActive = false;
  }
}
