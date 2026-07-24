import json
from unittest.mock import patch

from django.http import JsonResponse
from django.test import RequestFactory, TestCase, override_settings
from django.urls import reverse

from foundation_cms.blocks.block_registry import BlockRegistry
from foundation_cms.blocks.illustrated_newsletter_signup_block import (
    IllustratedNewsletterSignupBlock,
)
from foundation_cms.blocks.three_column_container_block import ThreeColumnStreamBlock
from foundation_cms.blocks.two_column_container_block import ColumnStreamBlock
from foundation_cms.snippets.factories import IllustratedNewsletterSignupFactory
from foundation_cms.snippets.models import IllustratedNewsletterSignup
from foundation_cms.views import illustrated_newsletter_signup_submission_view


class IllustratedNewsletterSignupBlockTests(TestCase):
    def test_snippet_requires_an_explicit_newsletter_and_limits_the_heading(self):
        heading_field = IllustratedNewsletterSignup._meta.get_field("heading")
        newsletter_field = IllustratedNewsletterSignup._meta.get_field("newsletter")

        self.assertEqual(heading_field.max_length, 60)
        self.assertFalse(newsletter_field.has_default())

    def test_editor_chooses_an_illustrated_newsletter_signup_snippet(self):
        block = IllustratedNewsletterSignupBlock()

        self.assertEqual(set(block.child_blocks), {"newsletter_signup"})
        self.assertEqual(
            block.child_blocks["newsletter_signup"].target_model,
            IllustratedNewsletterSignup,
        )

    def test_rendered_form_uses_the_selected_snippet_and_dedicated_endpoint(self):
        signup = IllustratedNewsletterSignupFactory(
            heading="Keep up with Mozilla Festival",
            illustration=None,
            newsletter="mozillafestivalorg",
        )
        block = IllustratedNewsletterSignupBlock()
        value = block.to_python({"newsletter_signup": signup.pk})

        html = block.render(value, context={"theme": "default"})

        self.assertIn('data-state="default"', html)
        self.assertIn(
            f'data-signup-url="/newsletter-signup/illustrated/{signup.pk}/"',
            html,
        )
        self.assertIn("Keep up with Mozilla Festival", html)
        self.assertIn("illustrated-newsletter-signup__expanded", html)
        self.assertIn("Sign Up", html)

    def test_block_is_available_in_two_and_three_column_containers(self):
        self.assertIs(
            BlockRegistry.BLOCKS["illustrated_newsletter_signup"]["class"],
            IllustratedNewsletterSignupBlock,
        )
        self.assertIsInstance(
            ColumnStreamBlock().child_blocks["illustrated_newsletter_signup"],
            IllustratedNewsletterSignupBlock,
        )
        self.assertIsInstance(
            ThreeColumnStreamBlock().child_blocks["illustrated_newsletter_signup"],
            IllustratedNewsletterSignupBlock,
        )


@override_settings(NEWSLETTER_SIGNUP_METHOD="BASKET")
class IllustratedNewsletterSignupSubmissionTests(TestCase):
    def setUp(self):
        self.request_factory = RequestFactory()
        self.signup = IllustratedNewsletterSignupFactory(
            illustration=None,
            newsletter="MozillaFestivalOrg",
        )
        self.url = reverse(
            "illustrated-newsletter-signup-submission",
            args=[self.signup.pk],
        )
        self.payload = {
            "email": "festival@example.com",
            "country": "CA",
            "lang": "en",
            "source": "https://www.mozillafestival.org/",
            "newsletter": "untrusted-client-value",
        }

    @patch("foundation_cms.views.subscribe_to_basket_newsletter")
    def test_uses_the_selected_snippets_newsletter(self, subscribe):
        subscribe.return_value = JsonResponse({}, status=201)

        response = self.client.post(
            self.url,
            data=json.dumps(self.payload),
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 201)
        subscribe.assert_called_once()
        submitted_data = subscribe.call_args.args[0]
        self.assertEqual(submitted_data["newsletters"], "mozillafestivalorg")

    @patch("foundation_cms.views.subscribe_to_basket_newsletter")
    def test_rejects_an_unknown_snippet(self, subscribe):
        request = self.request_factory.post(
            "/newsletter-signup/illustrated/999999/",
            data=json.dumps(self.payload),
            content_type="application/json",
        )
        response = illustrated_newsletter_signup_submission_view(request, 999999)

        self.assertEqual(response.status_code, 404)
        subscribe.assert_not_called()

    @patch("foundation_cms.views.subscribe_to_basket_newsletter")
    def test_rejects_invalid_json(self, subscribe):
        response = self.client.post(
            self.url,
            data="not-json",
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 500)
        subscribe.assert_not_called()
