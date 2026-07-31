import json
from unittest.mock import patch

from django.http import JsonResponse
from django.test import RequestFactory, TestCase, override_settings
from django.urls import reverse

from foundation_cms.blocks.illustrated_newsletter_signup_block import (
    IllustratedNewsletterSignupBlock,
)
from foundation_cms.snippets.factories import IllustratedNewsletterSignupFactory
from foundation_cms.snippets.models import IllustratedNewsletterSignup
from foundation_cms.views import illustrated_newsletter_signup_submission_view


class IllustratedNewsletterSignupBlockTests(TestCase):
    def test_snippet_defaults_the_newsletter_and_limits_the_heading(self):
        heading_field = IllustratedNewsletterSignup._meta.get_field("heading")
        button_text_field = IllustratedNewsletterSignup._meta.get_field("button_text")
        newsletter_field = IllustratedNewsletterSignup._meta.get_field("newsletter")

        self.assertEqual(heading_field.max_length, 70)
        self.assertEqual(button_text_field.max_length, 50)
        self.assertEqual(button_text_field.default, "Sign Up")
        self.assertEqual(newsletter_field.default, "mozillafoundationorg")

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
            button_text="Join the Festival",
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
        self.assertIn("Join the Festival", html)
        self.assertIn("illustrated-newsletter-signup__signup-view", html)
        self.assertIn("illustrated-newsletter-signup__success", html)
        self.assertNotIn("illustrated-newsletter-signup__illustration", html)
        self.assertIn("Thank you!", html)

    def test_empty_snippet_selection_renders_no_block_markup(self):
        block = IllustratedNewsletterSignupBlock()
        value = block.to_python({"newsletter_signup": None})

        html = block.render(value, context={"theme": "default"})

        self.assertNotIn("illustrated-newsletter-signup-block", html)
        self.assertNotIn("data-signup-url", html)

    def test_rendered_illustration_provides_a_retina_rendition(self):
        signup = IllustratedNewsletterSignupFactory(
            illustration__file__width=400,
            illustration__file__height=400,
        )
        block = IllustratedNewsletterSignupBlock()
        value = block.to_python({"newsletter_signup": signup.pk})

        html = block.render(value, context={"theme": "default"})

        self.assertIn('srcset="', html)
        self.assertIn(" 1x,", html)
        self.assertIn(" 2x", html)
        self.assertIn(".max-200x133.", html)
        self.assertIn(".max-400x267.", html)
        self.assertEqual(html.count('width="133"'), 2)
        self.assertEqual(html.count('height="133"'), 2)
        self.assertEqual(
            html.count('class="illustrated-newsletter-signup__illustration"'),
            2,
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
