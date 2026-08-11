/**
 * Shared CSRF helpers.
 *
 * The site is served through a CDN that full-page-caches anonymous HTML, so a
 * `{% csrf_token %}` baked into a cached page belongs to whoever warmed the cache
 * and will not match the visitor's own `csrftoken` cookie (thus giving them a 403). Instead, JS reads
 * the per-user `csrftoken` cookie at submit time and supplies it either as the
 * `X-CSRFToken` header (fetch forms) or as a JS-populated hidden `csrfmiddlewaretoken`
 * input (native form POSTs that redirect).
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
    "(?:^|;)\\s*" + name + "\\s*=\\s*([^;]*)",
  );
  return match ? decodeURIComponent(match[1]) : "";
}

/**
 * Return the current CSRF token, minting the cookie on demand.
 *
 * First-time visitors landing on a fully-cached page have no `csrftoken` cookie, so
 * we hit the uncached `/api/csrf/` endpoint (which sets the cookie) and re-read it.
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

/**
 * Wire up native form POSTs that submit-and-navigate (no fetch) to populate their
 * `csrfmiddlewaretoken` at submit time from the cookie.
 *
 * Markup contract:
 *   <form data-csrf-form method="post">
 *     <input type="hidden" name="csrfmiddlewaretoken" value="" data-csrf-field>
 *     <button type="submit" name="action" value="share">…</button>
 *   </form>
 *
 * On submit we preventDefault, ensure the token, populate the hidden field, mirror the
 * clicked submit button's name/value (a programmatic `form.submit()` drops the submitter),
 * then submit. `form.submit()` does not re-fire the `submit` event, so there is no loop.
 *
 * @param {ParentNode} [root=document] - Scope to search for `[data-csrf-form]` forms.
 */
export function initCsrfForms(root = document) {
  const forms = root.querySelectorAll("[data-csrf-form]");

  forms.forEach((form) => {
    form.addEventListener("submit", async (event) => {
      const field = form.querySelector("[data-csrf-field]");
      // Already populated (e.g. a re-submit) → let the native submit proceed.
      if (field && field.value) return;

      event.preventDefault();

      // A programmatic form.submit() omits the clicked button, so mirror it into a
      // hidden input to preserve the action=share|skip (etc.) the backend reads.
      const submitter = event.submitter;
      if (submitter && submitter.name) {
        let mirror = form.querySelector("input[data-csrf-submitter]");
        if (!mirror) {
          mirror = document.createElement("input");
          mirror.type = "hidden";
          mirror.setAttribute("data-csrf-submitter", "");
          form.appendChild(mirror);
        }
        mirror.name = submitter.name;
        mirror.value = submitter.value;
      }

      const token = await ensureCsrfToken();
      if (field) field.value = token;
      form.submit();
    });
  });
}
