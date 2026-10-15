from django.test import SimpleTestCase

from foundation_cms.blocks.call_to_action_block import CallToActionBlock


class CallToActionBlockTests(SimpleTestCase):
    def render(self, **overrides):
        block = CallToActionBlock()
        value = block.to_python(
            {
                "heading": "Want to collab?",
                "body": "Reach out to us and we can work together!",
                "button": {"label": "Contact Us", "link_to": "relative_url", "relative_url": "/contact/"},
                **overrides,
            }
        )
        return block.render(value, context={"theme": "default"})

    def test_renders_editor_content_with_a_primary_button(self):
        html = self.render()

        self.assertIn("Want to collab?", html)
        self.assertIn("Reach out to us and we can work together!", html)
        self.assertIn('href="/contact/"', html)
        self.assertIn("btn-primary", html)
        self.assertIn("Contact Us", html)
        self.assertNotIn('target="_blank"', html)

    def test_omits_body_when_empty(self):
        html = self.render(body="")

        self.assertNotIn("call-to-action-block__body", html)

    def test_button_can_open_in_a_new_window(self):
        html = self.render(
            button={
                "label": "Contact Us",
                "link_to": "external_url",
                "external_url": "https://example.com",
                "new_window": True,
            }
        )

        self.assertIn('href="https://example.com"', html)
        self.assertIn('target="_blank"', html)
