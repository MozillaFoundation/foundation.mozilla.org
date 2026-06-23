"""
Regression tests for the CSRF ⨯ CDN fix.

The site is served through a CDN that full-page-caches anonymous HTML. A `{% csrf_token %}`
rendered into a cacheable page bakes one visitor's token into the shared HTML, so every other
visitor submits a token that does not match their own `csrftoken` cookie → HTTP 403.

The durable fix is to never render `{% csrf_token %}` into cacheable templates and instead have
JS read the per-user `csrftoken` cookie (minting it via the uncached `/api/csrf/` endpoint when
absent). These tests guard both halves of that contract.
"""

from pathlib import Path

from django.test import Client, TestCase

# foundation_cms package root (…/foundation_cms/base/tests/test_csrf.py → parents[2]).
PACKAGE_ROOT = Path(__file__).resolve().parents[2]

# The only template allowed to render {% csrf_token %}: the dedicated, uncached mint endpoint.
ALLOWED_CSRF_TOKEN_TEMPLATES = {PACKAGE_ROOT / "legacy_apps" / "templates" / "api" / "csrf.html"}


class NoBakedCsrfTokenInTemplatesTest(TestCase):
    """`{% csrf_token %}` must not appear in any template except the uncached mint endpoint."""

    def test_no_csrf_token_in_cacheable_templates(self):
        offenders = []
        for template in PACKAGE_ROOT.rglob("*.html"):
            if "node_modules" in template.parts:
                continue
            if template in ALLOWED_CSRF_TOKEN_TEMPLATES:
                continue
            text = template.read_text(encoding="utf-8", errors="ignore")
            if "{% csrf_token %}" in text or "{%csrf_token%}" in text:
                offenders.append(str(template.relative_to(PACKAGE_ROOT)))

        self.assertEqual(
            offenders,
            [],
            "These templates render {% csrf_token %} into potentially cacheable HTML, which "
            "collides with the CDN cache (see test docstring). Populate the token from the "
            "csrftoken cookie via JS instead:\n  " + "\n  ".join(offenders),
        )


class CsrfMintEndpointTest(TestCase):
    """`/api/csrf/` must mint the csrftoken cookie so JS can read it."""

    def test_mint_endpoint_sets_csrftoken_cookie(self):
        response = Client().get("/api/csrf/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("csrftoken", response.cookies)
        self.assertEqual(response["Cache-Control"], "no-cache")

    def test_mint_endpoint_is_anchored(self):
        # The route is anchored (r"^api/csrf/$") so it no longer matches /api/csrf/<anything>.
        # The exact non-match status (404 from Wagtail, or a 302 locale redirect) is not what
        # we assert — only that the mint view no longer serves that path (it would be 200).
        self.assertNotEqual(Client().get("/api/csrf/extra/").status_code, 200)
