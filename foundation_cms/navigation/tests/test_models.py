from wagtail import models as wagtail_models
from wagtail.blocks import StreamBlockValidationError

from foundation_cms.legacy_apps.wagtailpages.tests import base as test_base
from foundation_cms.navigation import factories as nav_factories
from foundation_cms.navigation import models as nav_models


class NavigationMenuTests(test_base.WagtailpagesTestCase):
    def test_default_factory_creates_menu_with_four_dropdowns(self):
        """Test that the default factory creates a NavigationMenu with 4 dropdowns."""
        menu = nav_factories.NavigationMenuFactory()
        self.assertIsInstance(menu, nav_models.NavigationMenu)
        # By convention the factory builds four dropdowns by default
        self.assertEqual(len(menu.dropdowns), 4)

    def test_cannot_create_nav_menu_without_dropdowns(self):
        """Creating a menu with no dropdowns should fail StreamField validation."""
        # Validate the stream block directly (this mirrors model-level StreamField validation)
        with self.assertRaises(StreamBlockValidationError):
            # calling the stream_block.clean with an empty list should raise
            nav_models.NavigationMenu.dropdowns.field.stream_block.clean([])

    def test_cannot_create_nav_menu_with_more_than_five_dropdowns(self):
        """Enforcing the StreamField's max_num (5) for dropdowns."""
        # Make 6 minimal payloads for "dropdown" block
        payload = [{"type": "dropdown", "value": {}} for _ in range(6)]

        stream_block = nav_models.NavigationMenu.dropdowns.field.stream_block

        # Convert to python representation used by Wagtail internals before validating
        python_payload = stream_block.to_python(payload)

        with self.assertRaises(StreamBlockValidationError):
            stream_block.clean(python_payload)


class HorizontalLinkBlockTests(test_base.WagtailpagesTestCase):
    def test_default_factory_creates_three_ordered_links(self):
        block = nav_factories.HorizontalLinkBlockFactory()

        self.assertIsInstance(block, nav_models.HorizontalLinkBlock)
        self.assertEqual(len(block.links), 3)
        self.assertTrue(all(item.block_type == "link" for item in block.links))

    def test_requires_at_least_one_link(self):
        stream_block = nav_models.HorizontalLinkBlock.links.field.stream_block

        with self.assertRaises(StreamBlockValidationError):
            stream_block.clean([])

    def test_cannot_contain_more_than_seven_links(self):
        payload = [
            {
                "type": "link",
                "value": {
                    "label": f"Link {index}",
                    "link_to": "relative_url",
                    "page": None,
                    "external_url": "",
                    "relative_url": f"/link-{index}/",
                },
            }
            for index in range(8)
        ]
        stream_block = nav_models.HorizontalLinkBlock.links.field.stream_block

        with self.assertRaises(StreamBlockValidationError):
            stream_block.clean(stream_block.to_python(payload))


class SiteNavigationMenuSettingTests(test_base.WagtailpagesTestCase):
    def test_site_navigation_menu_setting_can_point_to_navigation_menu(self):
        """
        Ensure the SiteNavigationMenu setting can be created/updated and
        links to a NavigationMenu instance as the active menu.
        """
        # Create a navigation menu via factory
        menu = nav_factories.NavigationMenuFactory()

        # Find the current site (test base provides a site/homepage setup)
        site = wagtail_models.Site.objects.first()
        self.assertIsNotNone(site)

        # Retrieve (or create) the settings object for that site and set the active menu
        settings_obj = nav_models.SiteNavigationMenu.for_site(site)
        settings_obj.active_navigation_menu = menu
        settings_obj.save()

        # Reload and confirm the relationship persisted
        settings_obj.refresh_from_db()
        self.assertIsNotNone(settings_obj.active_navigation_menu)
        self.assertEqual(settings_obj.active_navigation_menu.pk, menu.pk)
