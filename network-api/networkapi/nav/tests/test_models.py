from django.test import TestCase
from wagtail.blocks import StreamBlockValidationError

from networkapi.nav import factories as nav_factories
from networkapi.nav import models as nav_models


class NavMenuTests(TestCase):
    def test_default_factory(self):
        """Test that the default factory creates a NavMenu with 4 dropdowns."""
        menu = nav_factories.NavMenuFactory()
        self.assertIsInstance(menu, nav_models.NavMenu)
        self.assertEqual(len(menu.dropdowns), 4)

    def test_cannot_create_nav_menu_without_dropdowns(self):
        with self.assertRaises(StreamBlockValidationError):
            menu = nav_factories.NavMenuFactory(dropdowns={})
            menu.dropdowns.stream_block.clean([])

    def test_cannot_create_nav_menu_with_more_than_five_dropdowns(self):
        with self.assertRaises(StreamBlockValidationError):
            menu = nav_factories.NavMenuFactory(
                dropdowns__0="dropdown",
                dropdowns__1="dropdown",
                dropdowns__2="dropdown",
                dropdowns__3="dropdown",
                dropdowns__4="dropdown",
            )
            menu.dropdowns.stream_block.clean([])
