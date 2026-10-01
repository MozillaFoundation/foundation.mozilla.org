from django.template.loader import render_to_string
from django.test import SimpleTestCase

from foundation_cms.blocks.link_button_block import FixedAlignmentLinkButtonBlock, LinkButtonBlock


class LinkButtonRenderingTests(SimpleTestCase):
    def test_block_adopts_reskin_without_changing_link_behavior(self):
        for style in ("btn-primary", "btn-secondary"):
            for link_to, field, destination, href in (
                ("external_url", "external_url", "https://example.com/", "https://example.com/"),
                ("relative_url", "relative_url", "/stories/", "/stories/"),
                ("email", "email", "hello@example.com", "mailto:hello@example.com"),
                ("anchor", "anchor", "details", "#details"),
                ("phone", "phone", "+15555555555", "tel:+15555555555"),
            ):
                with self.subTest(style=style, link_to=link_to):
                    block = LinkButtonBlock()
                    value = block.to_python(
                        {
                            "label": "Read <more>",
                            "style": style,
                            "alignment": "link-button-block--center",
                            "link_to": link_to,
                            field: destination,
                            "new_window": True,
                        }
                    )
                    html = block.render(value, context={"render_link_type_icon": True})
                    self.assertIn(f"button-reskin--{style}", html)
                    self.assertIn("link-button-block--center", html)
                    self.assertIn(f'href="{href}"', html)
                    self.assertIn('target="_blank"', html)
                    self.assertEqual(html.count("Read &lt;more&gt;"), 1)
                    self.assertNotIn("__roller", html)
                    icon = {"external_url": "external", "email": "email"}.get(link_to, "link")
                    self.assertIn(f"link-type-icon {icon}", html)

    def test_fixed_alignment_block_uses_same_skin_without_alignment_class(self):
        block = FixedAlignmentLinkButtonBlock()
        html = block.render(
            block.to_python(
                {"label": "Read more", "style": "btn-primary", "link_to": "relative_url", "relative_url": "/"}
            )
        )
        self.assertIn("button-reskin--btn-primary", html)
        self.assertNotIn("link-button-block--", html)

    def test_existing_shared_consumers_keep_rolling_labels(self):
        for style in ("btn-primary", "btn-secondary"):
            with self.subTest(style=style):
                html = render_to_string(
                    "patterns/components/_button.html",
                    {"button_style": style, "label": "Read more", "url": "/stories/"},
                )
                self.assertNotIn("button-reskin", html)
                self.assertIn(f"{style}__roller", html)
                self.assertEqual(html.count("Read more"), 2)

    def test_reskinned_native_button_preserves_disabled_and_form_attributes(self):
        html = render_to_string(
            "patterns/components/_button.html",
            {
                "reskin": True,
                "tag": "button",
                "button_type": "submit",
                "button_style": "btn-primary",
                "label": "Send",
                "disabled": True,
                "name": "action",
                "button_value": "send",
                "classnames": "btn-primary--no-arrow",
            },
        )
        self.assertIn('type="submit"', html)
        self.assertIn("disabled", html)
        self.assertIn('name="action"', html)
        self.assertIn('value="send"', html)
        self.assertIn("btn-primary--no-arrow", html)
        self.assertEqual(html.count(">Send<"), 1)
