/**
 * Standalone global build of the shared CSRF helpers, for inline template scripts.
 *
 * Inline `<script>` blocks in templates can't import from the esbuild bundle, so
 * this thin entry point re-exposes the helpers from `./csrf.js` on
 * `window.FoundationCSRF`. Templates load it via `<script src>` before the inline
 * script that needs the token. Keeping the logic in `./csrf.js` means the bundle
 * and the inline scripts share a single source of truth.
 */
import { getCookie, ensureCsrfToken } from "./csrf.js";

window.FoundationCSRF = { getCookie, ensureCsrfToken };
