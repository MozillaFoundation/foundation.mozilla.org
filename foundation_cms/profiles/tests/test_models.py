from django.db.models import URLField
from wagtail.test.utils import WagtailPageTestCase

from foundation_cms.profiles.factories import (
    ExpertDirectoryPageFactory,
    ExpertHubPageFactory,
    ExpertProfilePageFactory,
)


class ExpertProfilePageTestCase(WagtailPageTestCase):
    def setUp(self):
        self.hub = ExpertHubPageFactory()
        self.page = ExpertProfilePageFactory(parent=self.hub)

    def test_str_representation(self):
        self.assertEqual(str(self.page), self.page.title)

    def test_required_fields_populated(self):
        self.assertTrue(self.page.role)
        self.assertTrue(self.page.bio)
        self.assertTrue(self.page.location)
        self.assertIsNotNone(self.page.image)

    def test_is_leaf_page(self):
        self.assertEqual(self.page.subpage_types, [])

    def test_social_fields_use_url_validation_and_are_optional(self):
        for field_name in [
            "linkedin_url",
            "bluesky_url",
            "facebook_url",
            "instagram_url",
            "tiktok_url",
        ]:
            field = self.page._meta.get_field(field_name)
            self.assertTrue(field.blank)
            self.assertIsInstance(field, URLField)

    def test_social_fields_editor_heading(self):
        social_panel = next(
            panel for panel in self.page.content_panels if getattr(panel, "heading", None) == "Where to find me"
        )

        self.assertEqual(
            [panel.field_name for panel in social_panel.children],
            [
                "linkedin_url",
                "bluesky_url",
                "facebook_url",
                "instagram_url",
                "tiktok_url",
            ],
        )

    def test_editor_exposes_body_and_socials_but_not_legacy_content(self):
        field_names = []

        def collect_fields(panels):
            for panel in panels:
                if hasattr(panel, "field_name"):
                    field_names.append(panel.field_name)
                collect_fields(getattr(panel, "children", []))

        collect_fields(self.page.content_panels)

        self.assertIn("body", field_names)
        self.assertIn("linkedin_url", field_names)
        self.assertNotIn("quote", field_names)
        self.assertNotIn("quote_attribution", field_names)
        self.assertNotIn("selected_projects", field_names)
        self.assertNotIn("selected_articles", field_names)
        self.assertNotIn("external_links", field_names)


class ExpertDirectoryPageTestCase(WagtailPageTestCase):
    def setUp(self):
        self.hub = ExpertHubPageFactory()
        self.directory = ExpertDirectoryPageFactory(parent=self.hub)

    def test_parent_is_hub(self):
        self.assertEqual(self.directory.get_parent().specific, self.hub)

    def test_is_leaf_page(self):
        self.assertEqual(self.directory.subpage_types, [])

    def test_get_experts_returns_hub_children(self):
        expert = ExpertProfilePageFactory(parent=self.hub)
        experts = self.directory.get_experts()
        self.assertIn(expert, experts)
