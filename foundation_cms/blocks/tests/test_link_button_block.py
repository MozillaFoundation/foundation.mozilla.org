from bs4 import BeautifulSoup
from django.core.exceptions import ValidationError
from django.template.loader import render_to_string
from django.test import SimpleTestCase
from wagtail import blocks

from foundation_cms.blocks.featured_card_block import FeaturedCardBlock
from foundation_cms.blocks.link_button_block import (
    FixedAlignmentLinkButtonBlock,
    LinkButtonBlock,
)
from foundation_cms.blocks.section_start_block import SectionStartBlock
from foundation_cms.blocks.three_column_container_block import ThreeColumnContainerBlock
from foundation_cms.blocks.two_column_container_block import TwoColumnContainerBlock


class LinkButtonRenderingTests(SimpleTestCase):
    def button_value(self, **overrides):
        return {
            "label": "Read <more>",
            "style": "btn-primary",
            "alignment": "link-button-block--left",
            "link_to": "relative_url",
            "relative_url": "/stories/",
            **overrides,
        }

    def test_saved_styles_render_direct_cosmos_links(self):
        for style, css_class in (
            ("btn-primary", "mzf-c-button--primary-icon"),
            ("btn-secondary", "mzf-c-button--cta-stroke-icon"),
        ):
            for block_class in (LinkButtonBlock, FixedAlignmentLinkButtonBlock):
                with self.subTest(style=style, block=block_class.__name__):
                    block = block_class()
                    value = block.to_python(self.button_value(style=style))
                    soup = BeautifulSoup(block.render(value), "html.parser")
                    self.assertEqual(len(soup.find_all(recursive=False)), 1)
                    anchor = soup.a
                    self.assertIsNotNone(anchor)
                    self.assertEqual(anchor["class"], ["mzf-c-button", css_class])
                    self.assertEqual(anchor["href"], "/stories/")
                    self.assertNotIn("target", anchor.attrs)
                    self.assertEqual(anchor.get_text(strip=True), "Read <more>")
                    self.assertIsNone(anchor.find("more"))
                    self.assertEqual(len(anchor.select(".mzf-c-button__label")), 1)
                    icon = anchor.select_one(".mzf-c-button__icon")
                    self.assertEqual(icon["aria-hidden"], "true")
                    self.assertIsNotNone(icon.svg)

    def test_links_preserve_destinations_and_new_window_behavior(self):
        for link_to, destination, href in (
            ("external_url", "https://example.com/", "https://example.com/"),
            ("relative_url", "/stories/", "/stories/"),
            ("email", "hello@example.com", "mailto:hello@example.com"),
            ("anchor", "details", "#details"),
            ("phone", "+15555555555", "tel:+15555555555"),
        ):
            with self.subTest(link_to=link_to):
                block = LinkButtonBlock()
                value = block.to_python(self.button_value(link_to=link_to, new_window=True, **{link_to: destination}))
                anchor = BeautifulSoup(block.render(value), "html.parser").a
                self.assertEqual(anchor["href"], href)
                self.assertEqual(anchor["target"], "_blank")

    def test_contextual_glyphs_are_opt_in_and_replace_the_arrow(self):
        for link_to, glyph in (("external_url", "external"), ("email", "email"), ("relative_url", None)):
            for contextual in (False, True):
                with self.subTest(link_to=link_to, contextual=contextual):
                    block = LinkButtonBlock()
                    value = block.to_python(self.button_value(link_to=link_to))
                    html = block.render(value, context={"render_link_type_icon": contextual})
                    icon = BeautifulSoup(html, "html.parser").select_one(".mzf-c-button__icon")
                    self.assertEqual(icon["aria-hidden"], "true")
                    self.assertEqual(icon.get("data-link-type"), glyph if contextual else None)
                    self.assertEqual(icon.svg is None, contextual and glyph is not None)

    def test_editor_preserves_existing_choices_default_and_saved_values(self):
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
                    value = block.to_python(self.button_value(style=style))
                    self.assertEqual(block.get_prep_value(value)["style"], style)
            # LP CSS variants are not additional editor choices.
            for unsupported in ("primary", "primary-white", "primary-grey", "cta-stroke", "nav"):
                with self.subTest(block=block_class.__name__, unsupported=unsupported):
                    with self.assertRaises(ValidationError):
                        style_field.clean(unsupported)

    def test_saved_alignment_controls_layout_without_becoming_a_css_class(self):
        block = LinkButtonBlock()
        for saved, rendered in (("link-button-block--left", "left"), ("link-button-block--center", "center")):
            with self.subTest(alignment=saved):
                value = block.to_python(self.button_value(alignment=saved))
                html = block.render(value)
                self.assertEqual(BeautifulSoup(html, "html.parser").a["data-alignment"], rendered)
                self.assertNotIn(saved, html)
                self.assertEqual(block.get_prep_value(value)["alignment"], saved)
        fixed = FixedAlignmentLinkButtonBlock()
        html = fixed.render(fixed.to_python(self.button_value(alignment="link-button-block--center")))
        self.assertNotIn("data-alignment", html)

    def test_cosmos_block_skips_grid_wrapper_without_changing_serialization(self):
        for block_class in (LinkButtonBlock, FixedAlignmentLinkButtonBlock):
            with self.subTest(block=block_class.__name__):
                block = block_class()
                self.assertTrue(block.is_cosmos_block)
                self.assertTrue(block.skip_default_wrapper)
                self.assertNotIn("is_cosmos_block", block.deconstruct()[2])
                self.assertNotIn("skip_default_wrapper", block.deconstruct()[2])

    def test_section_and_implicit_stream_render_buttons_without_nested_layout(self):
        stream_block = blocks.StreamBlock([("section_start", SectionStartBlock()), ("link_button", LinkButtonBlock())])
        for marked in (False, True):
            with self.subTest(marked=marked):
                data = [{"type": "section_start", "value": {"name": "Buttons"}}] if marked else []
                data.append({"type": "link_button", "value": self.button_value()})
                html = render_to_string(
                    "patterns/components/_sectioned_streamfield.html", {"streamfield": stream_block.to_python(data)}
                )
                soup = BeautifulSoup(html, "html.parser")
                self.assertIsNotNone(soup.select_one(".streamfield-block-wrapper > a.mzf-c-button"))
                self.assertEqual(bool(soup.select_one(".mzf-c-section")), marked)
                self.assertIsNone(soup.select_one(".grid-container, .grid-x, .link-button-block"))

    def test_featured_card_direct_include_renders_the_same_button(self):
        block = FeaturedCardBlock()
        value = block.to_python({"heading": "Featured", "description": "", "button": self.button_value()})
        soup = BeautifulSoup(block.render(value), "html.parser")
        anchor = soup.select_one(".featured-card__button > a.mzf-c-button")
        self.assertIsNotNone(anchor)
        self.assertEqual(anchor["href"], "/stories/")

    def test_two_and_three_column_containers_render_direct_button_children(self):
        for block_class, columns in (
            (TwoColumnContainerBlock, ("left", "right")),
            (ThreeColumnContainerBlock, ("left", "center", "right")),
        ):
            with self.subTest(block=block_class.__name__):
                block = block_class()
                value = block.to_python(
                    {f"{column}_column": [{"type": "link_button", "value": self.button_value()}] for column in columns}
                )
                soup = BeautifulSoup(block.render(value), "html.parser")
                for column in columns:
                    holder = soup.select_one(f"[class$='__column--{column}']")
                    self.assertIsNotNone(holder.find("a", class_="mzf-c-button", recursive=False))
                self.assertEqual(len(soup.select(".mzf-c-button")), len(columns))

    def test_existing_shared_consumers_keep_rolling_labels(self):
        for style in ("btn-primary", "btn-secondary"):
            with self.subTest(style=style):
                html = render_to_string(
                    "patterns/components/_button.html",
                    {"button_style": style, "label": "Read more", "url": "/stories/"},
                )
                self.assertNotIn("mzf-c-button", html)
                self.assertIn(f"{style}__roller", html)
                self.assertEqual(html.count("Read more"), 2)

    def test_existing_native_button_preserves_disabled_form_and_no_arrow_attributes(self):
        html = render_to_string(
            "patterns/components/_button.html",
            {
                "tag": "button",
                "button_type": "submit",
                "button_style": "btn-primary",
                "label": "Send",
                "disabled": True,
                "name": "action",
                "button_value": "send",
                "aria_label": "Send message",
                "classnames": "btn-primary--no-arrow",
            },
        )
        for attribute in (
            'type="submit"',
            "disabled",
            'name="action"',
            'value="send"',
            'aria-label="Send message"',
            "btn-primary--no-arrow",
        ):
            self.assertIn(attribute, html)
        self.assertNotIn("mzf-c-button", html)
        self.assertIn("btn-primary__roller", html)
