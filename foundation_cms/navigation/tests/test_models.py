import wagtail_factories
from wagtail.blocks import StreamBlockValidationError

from foundation_cms.navigation import factories as nav_factories
from foundation_cms.navigation import models as nav_models
from foundation_cms.legacy_apps.wagtailpages.tests import base as test_base


class NavigationMenuTests(TestCase):
    def test_default_factory(self):
        """Test that the default factory creates a NavigationMenu with 4 dropdowns."""
        menu = nav_factories.NavigationMenuFactory()
        self.assertIsInstance(menu, nav_models.NavigationMenu)
        self.assertEqual(len(menu.dropdowns), 4)

    def test_cannot_create_nav_menu_without_dropdowns(self):
        with self.assertRaises(StreamBlockValidationError):
            menu = nav_factories.NavigationMenuFactory(dropdowns={})
            menu.dropdowns.stream_block.clean([])

    def test_cannot_create_nav_menu_with_more_than_five_dropdowns(self):
        with self.assertRaises(StreamBlockValidationError):
            menu = nav_factories.NavigationMenuFactory(
                dropdowns__0="dropdown",
                dropdowns__1="dropdown",
                dropdowns__2="dropdown",
                dropdowns__3="dropdown",
                dropdowns__4="dropdown",
            )
            menu.dropdowns.stream_block.clean([])

class TestNavigationMenuPageReferencesPerDropdown(test_base.WagtailpagesTestCase):
    def test_page_references_per_dropdown_property(self) -> None:
        # Create some pages:
        # pages ax linking to the first dropdown
        page_a1 = wagtail_factories.PageFactory(parent=self.homepage, title="Page A1")
        page_a2 = wagtail_factories.PageFactory(parent=self.homepage, title="Page A2")

        # pages bx linking to the second dropdown
        page_b1 = wagtail_factories.PageFactory(parent=self.homepage, title="Page B1")
        page_b2 = wagtail_factories.PageFactory(parent=self.homepage, title="Page B2")
        page_b3 = wagtail_factories.PageFactory(parent=self.homepage, title="Page B3")

        # Page c linked to third dropdown
        page_c = wagtail_factories.PageFactory(parent=self.homepage, title="Page C")

        # Page d not linked to any dropdowns
        page_d = wagtail_factories.PageFactory(parent=self.homepage, title="Page D")

        # Create a menu with links to the pages:
        menu = nav_factories.NavigationMenuFactory(
            # First dropdown | First Column | First link (page A1)
            dropdowns__0__dropdown__columns__0__nav_items__0__link_to="page",
            dropdowns__0__dropdown__columns__0__nav_items__0__page=page_a1,
            # First dropdown | First Column | Second link (external)
            dropdowns__0__dropdown__columns__0__nav_items__1__external_url_link=True,
            # First dropdown | CTA Button link (page A2)
            dropdowns__0__dropdown__button__link_to="page",
            dropdowns__0__dropdown__button__page=page_a2,
            # Second dropdown | First Column | First link (page B1)
            dropdowns__1__dropdown__columns__0__nav_items__0__link_to="page",
            dropdowns__1__dropdown__columns__0__nav_items__0__page=page_b1,
            # Second dropdown | First Column | Second link (external)
            dropdowns__1__dropdown__columns__0__nav_items__1__external_url_link=True,
            # Second dropdown | Second Column | First link (page B2)
            dropdowns__1__dropdown__columns__1_nav_items__0__link_to="page",
            dropdowns__1__dropdown__columns__1__nav_items__0__page=page_b2,
            # Second dropdown | Second Column | Second link (external)
            dropdowns__1__dropdown__columns__1__nav_items__1__external_url_link=True,
            # Second dropdown | CTA Button link (page B3)
            dropdowns__1__dropdown__button__link_to="page",
            dropdowns__1__dropdown__button__page=page_b3,
            # Third dropdown | First Column | First link (page C)
            dropdowns__2__dropdown__featured_column__0__nav_items__0__link_to="page",
            dropdowns__2__dropdown__featured_column__0__nav_items__0__page=page_c,
            # Third dropdown | First Column | Second link (external)
            dropdowns__2__dropdown__featured_column__0__nav_items__1__external_url_link=True,
        )

        # Get dropdown ids:
        dropdown_1_id = menu.dropdowns.raw_data[0]["id"]
        dropdown_2_id = menu.dropdowns.raw_data[1]["id"]
        dropdown_3_id = menu.dropdowns.raw_data[2]["id"]
        # The factory will create a fourth dropdown without any page links by default
        dropdown_4_id = menu.dropdowns.raw_data[3]["id"]

        expected = {
            dropdown_1_id: {
                "page_ids": [page_a1.id, page_a2.id],
                "self_page_id": page_a2.id,
                page_a1.id: page_a1.path,
                page_a2.id: page_a2.path,
            },
            dropdown_2_id: {
                "page_ids": [page_b1.id, page_b2.id, page_b3.id],
                "self_page_id": page_b3.id,
                page_b1.id: page_b1.path,
                page_b2.id: page_b2.path,
                page_b3.id: page_b3.path,
            },
            dropdown_3_id: {
                "page_ids": [page_c.id],
                "self_page_id": None,
                page_c.id: page_c.path,
            },
            dropdown_4_id: {"page_ids": [], "self_page_id": None},
        }

        # Get the page links:
        with self.assertNumQueries(1):
            page_references = menu.page_references_per_dropdown
            self.assertDictEqual(page_references, expected)

        # Get a flat list of page ids:
        page_ids = []
        for dropdown in page_references.values():
            page_ids.extend(dropdown["page_ids"])

        self.assertIn(page_a1.id, page_ids)
        self.assertIn(page_a2.id, page_ids)
        self.assertIn(page_b1.id, page_ids)
        self.assertIn(page_b2.id, page_ids)
        self.assertIn(page_b3.id, page_ids)
        self.assertIn(page_c.id, page_ids)
        self.assertNotIn(page_d.id, page_ids)


class TestNavigationMenuPageReferences(test_base.WagtailpagesTestCase):
    def test_page_references_property(self) -> None:
        # Create some pages:
        page_a = wagtail_factories.PageFactory(parent=self.homepage, title="Page A")
        page_b = wagtail_factories.PageFactory(parent=page_a, title="Page B")
        page_c = wagtail_factories.PageFactory(parent=page_b, title="Page C")
        page_d = wagtail_factories.PageFactory(parent=self.homepage, title="Page D")

        # Create a menu with links to the pages:
        menu = nav_factories.NavigationMenuFactory(
            dropdowns__0__dropdown__columns__0__nav_items__0__link_to="page",
            dropdowns__0__dropdown__columns__0__nav_items__0__page=page_a,
            dropdowns__0__dropdown__columns__0__nav_items__1__external_url_link=True,
            dropdowns__0__dropdown__button__link_to="page",
            dropdowns__0__dropdown__button__page=page_b,
            dropdowns__1__dropdown__featured_column__0__nav_items__0__link_to="page",
            dropdowns__1__dropdown__featured_column__0__nav_items__0__page=page_c,
            dropdowns__1__dropdown__featured_column__0__nav_items__1__external_url_link=True,
        )

        expected = {
            page_a.id: page_a.path,
            page_b.id: page_b.path,
            page_c.id: page_c.path,
        }

        # Get the page links:
        with self.assertNumQueries(1):
            page_references = menu.page_references
            self.assertDictEqual(page_references, expected)

        self.assertIn(page_a.id, page_references.keys())
        self.assertIn(page_b.id, page_references.keys())
        self.assertIn(page_c.id, page_references.keys())
        self.assertNotIn(page_d.id, page_references.keys())
