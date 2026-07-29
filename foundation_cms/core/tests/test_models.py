# @TODO address test cases after factory method is more concrete

# from django.test import TestCase

# from foundation_cms.core import factories


# class HomePageTestCase(TestCase):
#     def setUp(self):
#         self.home_page = factories.create_homepage()

#     def test_get_absolute_url(self):
#         self.assertEqual(self.home_page.url, "/en/")

from foundation_cms.core.models import GeneralPage
from foundation_cms.legacy_apps.wagtailpages.tests import base as test_base
from foundation_cms.navigation import factories as nav_factories


class GeneralPageHorizontalLinkBlockTests(test_base.WagtailpagesTestCase):
    def create_page(self, parent, title, horizontal_link_block=None):
        return parent.add_child(
            instance=GeneralPage(
                title=title,
                slug=title.lower().replace(" ", "-"),
                seo_title=title,
                search_description=f"Description for {title}",
                show_hero=False,
                horizontal_link_block=horizontal_link_block,
            )
        )

    def test_page_uses_its_own_horizontal_link_block(self):
        block = nav_factories.HorizontalLinkBlockFactory()
        page = self.create_page(self.homepage, "Own block", block)

        self.assertEqual(page.get_horizontal_link_block(), block)

    def test_page_inherits_nearest_ancestor_horizontal_link_block(self):
        outer_block = nav_factories.HorizontalLinkBlockFactory(title="Outer")
        nearest_block = nav_factories.HorizontalLinkBlockFactory(title="Nearest")
        outer = self.create_page(self.homepage, "Outer page", outer_block)
        nearest = self.create_page(outer, "Nearest page", nearest_block)
        child = self.create_page(nearest, "Child page")

        self.assertEqual(child.get_horizontal_link_block(), nearest_block)

    def test_page_own_block_overrides_inherited_block(self):
        parent_block = nav_factories.HorizontalLinkBlockFactory(title="Parent")
        child_block = nav_factories.HorizontalLinkBlockFactory(title="Child")
        parent = self.create_page(self.homepage, "Parent page", parent_block)
        child = self.create_page(parent, "Override page", child_block)

        self.assertEqual(child.get_horizontal_link_block(), child_block)

    def test_page_without_assignment_or_matching_ancestor_returns_none(self):
        page = self.create_page(self.homepage, "No block")

        self.assertIsNone(page.get_horizontal_link_block())

    def test_resolved_block_is_cached_on_the_page_instance(self):
        block = nav_factories.HorizontalLinkBlockFactory()
        parent = self.create_page(self.homepage, "Cached parent", block)
        child = self.create_page(parent, "Cached child")

        child.get_horizontal_link_block()
        with self.assertNumQueries(0):
            self.assertEqual(child.get_horizontal_link_block(), block)
