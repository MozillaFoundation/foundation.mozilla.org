from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.test import SimpleTestCase

from foundation_cms.blocks.link_button_block import (
    FixedAlignmentLinkButtonBlock,
    LinkButtonBlock,
)


class LinkButtonRenderingTests(SimpleTestCase):
    component_styles = {
        "btn-primary-no-icon": "primary",
        "btn-primary": "primary-icon",
        "btn-secondary-no-icon": "cta-stroke",
        "btn-secondary": "cta-stroke-icon",
        "btn-nav": "nav",
        "btn-primary-white": "primary-white",
        "btn-primary-grey": "primary-grey",
    }

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
                    self.assertIn(f"mzf-c-button--{self.component_styles[style]}", html)
                    self.assertEqual(
                        'class="mzf-c-button__icon" aria-hidden="true"' in html,
                        style in ("btn-primary", "btn-secondary"),
                    )
                    self.assertIn("link-button-block--center", html)
                    self.assertIn(f'href="{href}"', html)
                    self.assertIn('target="_blank"', html)
                    self.assertEqual(html.count("Read &lt;more&gt;"), 1)
                    self.assertNotIn("__roller", html)
                    icon = {"external_url": "external", "email": "email"}.get(link_to, "link")
                    self.assertIn(f"link-type-icon {icon}", html)

    def test_editor_preserves_existing_choices_and_default(self):
        cms_choices = [("btn-primary", "Primary"), ("btn-secondary", "Secondary")]
        for block_class in (LinkButtonBlock, FixedAlignmentLinkButtonBlock):
            block = block_class()
            style_field = block.child_blocks["style"]
            self.assertEqual(style_field.get_default(), "btn-primary")
            self.assertEqual([(value, label) for value, label in style_field.field.choices if value], cms_choices)
            self.assertNotIn("disabled", block.child_blocks)
            for style, _ in cms_choices:
                with self.subTest(block=block_class.__name__, style=style):
                    self.assertEqual(style_field.clean(style), style)
                    value = block.to_python(
                        {"label": "Read more", "style": style, "link_to": "relative_url", "relative_url": "/"}
                    )
                    html = block.render(value)
                    self.assertIn(f"mzf-c-button--{self.component_styles[style]}", html)
                    self.assertEqual(
                        'class="mzf-c-button__icon" aria-hidden="true"' in html,
                        style in ("btn-primary", "btn-secondary"),
                    )
                    self.assertIn('href="/"', html)
                    self.assertNotIn("disabled", html)
                    if block_class is FixedAlignmentLinkButtonBlock:
                        self.assertNotIn("link-button-block--", html)
            for style in set(self.component_styles) - {value for value, _ in cms_choices}:
                with self.subTest(block=block_class.__name__, component_only_style=style):
                    with self.assertRaises(ValidationError):
                        style_field.clean(style)

    def test_shared_component_family_preserves_anchor_behavior(self):
        for style in self.component_styles:
            with self.subTest(style=style):
                html = render_to_string(
                    "patterns/components/_button.html",
                    {
                        "reskin": True,
                        "button_style": style,
                        "label": "Read <more>",
                        "url": "/stories/",
                        "value": {"new_window": True},
                    },
                )
                self.assertIn(f"mzf-c-button--{self.component_styles[style]}", html)
                self.assertEqual(
                    'class="mzf-c-button__icon" aria-hidden="true"' in html, style in ("btn-primary", "btn-secondary")
                )
                self.assertIn('href="/stories/"', html)
                self.assertIn('target="_blank"', html)
                self.assertEqual(html.count("Read &lt;more&gt;"), 1)
                self.assertNotIn("disabled", html)

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
        for style in self.component_styles:
            with self.subTest(style=style):
                html = render_to_string(
                    "patterns/components/_button.html",
                    {
                        "reskin": True,
                        "tag": "button",
                        "button_type": "submit",
                        "button_style": style,
                        "label": "Send",
                        "disabled": True,
                        "name": "action",
                        "button_value": "send",
                        "aria_label": "Send message",
                    },
                )
                self.assertIn('type="submit"', html)
                self.assertIn("disabled", html)
                self.assertIn('name="action"', html)
                self.assertIn('value="send"', html)
                self.assertIn('aria-label="Send message"', html)
                self.assertIn(f"mzf-c-button--{self.component_styles[style]}", html)
                self.assertEqual(
                    'class="mzf-c-button__icon" aria-hidden="true"' in html, style in ("btn-primary", "btn-secondary")
                )
                self.assertEqual(html.count(">Send<"), 1)

    def test_existing_no_arrow_opt_in_is_preserved(self):
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

    def test_new_styles_require_explicit_reskin_adoption(self):
        for style in self.component_styles:
            if style in ("btn-primary", "btn-secondary"):
                continue
            with self.subTest(style=style):
                html = render_to_string(
                    "patterns/components/_button.html",
                    {"button_style": style, "label": "Read more", "url": "/stories/"},
                )
                self.assertNotIn("<a", html)
