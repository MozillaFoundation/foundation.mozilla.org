import json
from unittest.mock import patch

from django.http import JsonResponse
from django.test import SimpleTestCase, TestCase, override_settings
from django.urls import reverse

from foundation_cms.blocks.festival_newsletter_signup_block import (
    FestivalNewsletterSignupBlock,
)
from foundation_cms.blocks.three_column_container_block import ThreeColumnStreamBlock
from foundation_cms.blocks.two_column_container_block import ColumnStreamBlock


class FestivalNewsletterSignupBlockTests(SimpleTestCase):
    def test_editor_fields_are_self_contained(self):
        block = FestivalNewsletterSignupBlock()

        self.assertEqual(set(block.child_blocks), {"heading", "illustration"})
        self.assertTrue(block.child_blocks["heading"].required)
        self.assertEqual(block.child_blocks["heading"].field.max_length, 60)
        self.assertFalse(block.child_blocks["illustration"].required)

    def test_rendered_form_is_collapsed_and_uses_dedicated_endpoint(self):
        block = FestivalNewsletterSignupBlock()
        value = block.to_python(
            {
                "heading": "Keep up with Mozilla Festival",
                "illustration": None,
            }
        )

        html = block.render(value, context={"theme": "default"})

        self.assertIn('data-state="default"', html)
        self.assertIn('data-signup-url="/newsletter-signup/festival/"', html)
        self.assertIn("festival-newsletter-signup__expanded", html)
        self.assertNotIn("newsletter_signup", block.child_blocks)

    def test_block_is_available_in_two_and_three_column_containers(self):
        self.assertIsInstance(
            ColumnStreamBlock().child_blocks["festival_newsletter_signup"],
            FestivalNewsletterSignupBlock,
        )
        self.assertIsInstance(
            ThreeColumnStreamBlock().child_blocks["festival_newsletter_signup"],
            FestivalNewsletterSignupBlock,
        )


@override_settings(NEWSLETTER_SIGNUP_METHOD="BASKET")
class FestivalNewsletterSignupSubmissionTests(TestCase):
    def setUp(self):
        self.url = reverse("festival-newsletter-signup-submission")
        self.payload = {
            "email": "festival@example.com",
            "country": "CA",
            "lang": "en",
            "source": "https://www.mozillafestival.org/",
            "newsletter": "untrusted-client-value",
        }

    @patch("foundation_cms.views.subscribe_to_basket_newsletter")
    def test_uses_fixed_festival_newsletter_without_a_snippet(self, subscribe):
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
    def test_rejects_invalid_json(self, subscribe):
        response = self.client.post(
            self.url,
            data="not-json",
            content_type="application/json",
        )

        self.assertEqual(response.status_code, 500)
        subscribe.assert_not_called()
