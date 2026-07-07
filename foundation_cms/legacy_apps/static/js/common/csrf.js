/**
 * Shared CSRF helpers for the legacy bundle.
 *
 * Mirrors `foundation_cms/static/js/utils/csrf.js` in the redesign tree. The site is
 * served through a CDN that full-page-caches anonymous HTML, so a `{% csrf_token %}`
 * baked into a cached page does not match the visitor's own `csrftoken` cookie (→ 403).
 * Instead, JS reads the per-user cookie at submit time and sends it as `X-CSRFToken`.
 *
 * Requires `CSRF_COOKIE_HTTPONLY = False` (Django default) so JS can read the cookie.
 */

const CSRF_COOKIE_NAME = "csrftoken";
const CSRF_MINT_URL = "/api/csrf/";

/**
 * Read a cookie value by name from `document.cookie`.
 *
 * @param {string} name - The cookie name.
 * @returns {string} The cookie value, or "" if not present.
 */
export function getCookie(name) {
  const match = document.cookie.match(
    "(?:^|;)\\s*" + name + "\\s*=\\s*([^;]*)"
  );
  return match ? decodeURIComponent(match[1]) : "";
}

/**
 * Return the current CSRF token, minting the cookie on demand via the uncached
 * `/api/csrf/` endpoint for first-time visitors who landed on a cached page.
 *
 * @returns {Promise<string>} The `csrftoken` cookie value (may be "" if minting failed).
 */
export async function ensureCsrfToken() {
  let token = getCookie(CSRF_COOKIE_NAME);
  if (token) return token;

  try {
    // fetch() only rejects on network errors, so a non-2xx response (e.g. 500,
    // 404) would otherwise fall through and re-read a still-unset cookie.
    const res = await fetch(CSRF_MINT_URL, { credentials: "same-origin" });
    if (!res.ok) return "";
  } catch (err) {
    return "";
  }
  return getCookie(CSRF_COOKIE_NAME);
}
