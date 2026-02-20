from typing import Any

import wagtail_factories

from foundation_cms.legacy_apps.nav import factories as nav_factories
from foundation_cms.legacy_apps.nav.templatetags import nav_tags
from foundation_cms.legacy_apps.wagtailpages.factory import blog as blog_factories
from foundation_cms.legacy_apps.wagtailpages.tests import base as test_base


class TestCheckIfBlogDropdownCanBeActive(test_base.WagtailpagesTestCase):
    def test_active_dropdown_check(self) -> None:
        # Create some pages:

        # homepage
        page_homepage = self.homepage

        # blog pages
        page_blog_index = blog_factories.BlogIndexPageFactory(parent=page_homepage, title="Blog Index Page")
        page_blog_topic = blog_factories.BlogIndexPageFactory(parent=page_homepage, title="Blog Topic Page")
        page_blog_post = blog_factories.BlogPageFactory(parent=page_blog_index, title="Blog Post Page")

        # more pages
        page_a1 = wagtail_factories.PageFactory(parent=self.homepage, title="Page A1")
        page_a2 = wagtail_factories.PageFactory(parent=page_a1, title="Page A2")

        with self.subTest(msg="Test {page_blog_index}"):
            self.assertTrue(nav_tags.check_if_blog_dropdown_can_be_active({"page": page_blog_index}))

        with self.subTest(msg="Test {page_blog_topic}"):
            blog_factories.BlogPageTopicFactory(name="Test Topic")
            self.assertTrue(
                nav_tags.check_if_blog_dropdown_can_be_active({"page": page_blog_topic, "index_title": "Test Topic"})
            )

        with self.subTest(msg="Test {page_blog_post}"):
            self.assertTrue(nav_tags.check_if_blog_dropdown_can_be_active({"page": page_blog_post}))

        # For non-blog pages:
        for page in [page_homepage, page_a1, page_a2]:
            with self.subTest(msg="Test {page}"):
                self.assertFalse(nav_tags.check_if_blog_dropdown_can_be_active({"page": page}))

    def test_returns_false_if_no_page(self) -> None:
        """If no page is passed, the function should return False."""
        # No page is passed
        # Should return False
        self.assertFalse(nav_tags.check_if_blog_dropdown_can_be_active({}))


class TestCheckIfLinkIsActive(test_base.WagtailpagesTestCase):
    def test_active_link_check(self) -> None:
        # Create some pages:
        page_a = wagtail_factories.PageFactory(parent=self.homepage, title="Page A")
        page_b = wagtail_factories.PageFactory(parent=self.homepage, title="Page B")
        page_c = wagtail_factories.PageFactory(parent=page_b, title="Page C")

        # Create a menu with links to the pages:
        menu = nav_factories.NavMenuFactory(
            dropdowns__0__dropdown__columns__0__nav_items__0__link_to="page",
            dropdowns__0__dropdown__columns__0__nav_items__0__page=page_a,
            dropdowns__0__dropdown__columns__0__nav_items__1__external_url_link=True,
            dropdowns__0__dropdown__button__link_to="page",
            dropdowns__0__dropdown__button__page=page_b,
            dropdowns__1__dropdown__featured_column__0__nav_items__0__link_to="page",
            dropdowns__1__dropdown__featured_column__0__nav_items__0__page=page_c,
            dropdowns__1__dropdown__featured_column__0__nav_items__1__external_url_link=True,
        )

        # Get NavItem (link) objects:
        page_a_link = menu.dropdowns[0].value["columns"][0]["nav_items"][0]
        page_b_link = menu.dropdowns[0].value["button"]
        page_c_link = menu.dropdowns[1].value.featured_column_value["nav_items"][0]

        # User is on page_a
        context = {"page": page_a, "menu": menu}
        # page_a should be active since it's itself:
        self.assertTrue(nav_tags.check_if_link_is_active(context, page_a_link))
        # page_b and page_c and page_d should not be active (not related to page_a):
        self.assertFalse(nav_tags.check_if_link_is_active(context, page_b_link))
        self.assertFalse(nav_tags.check_if_link_is_active(context, page_c_link))

        # Creating a page_a1 which is a child of page_a
        page_a1 = wagtail_factories.PageFactory(parent=page_a, title="Page A1")
        # User is now on page_a1
        context = {"page": page_a1, "menu": menu}
        # page_a_link should not be active since page_a1 is not an exact match of page_a (it's a child):
        self.assertFalse(nav_tags.check_if_link_is_active(context, page_a_link))
        # page_b and page_c and page_d should not be active (not related to page_a):
        self.assertFalse(nav_tags.check_if_link_is_active(context, page_b_link))
        self.assertFalse(nav_tags.check_if_link_is_active(context, page_c_link))

        # Creating a page_b1 which is a child of page_b
        page_b1 = wagtail_factories.PageFactory(parent=page_b, title="Page B1")
        # User is now on page_b1
        context = {"page": page_b1, "menu": menu}
        # page_a should not be active:
        self.assertFalse(nav_tags.check_if_link_is_active(context, page_a_link))
        # page_b_link should not be active since page_b1 is not an exact match of page_b (it's a child):
        self.assertFalse(nav_tags.check_if_link_is_active(context, page_b_link))
        # page_c should not be active:
        self.assertFalse(nav_tags.check_if_link_is_active(context, page_c_link))

    def test_homepage_should_never_be_marked_as_active(self):
        """The homepage shouldn't receive 'active' markings."""
        # Create a menu with the first dropdown linking to the homepage:
        menu = nav_factories.NavMenuFactory(
            dropdowns__0__dropdown__button__link_to="page",
            dropdowns__0__dropdown__button__page=self.homepage,
        )

        homepage_link = menu.dropdowns[0].value["button"]

        # User is now on homepage
        context = {"page": self.homepage, "menu": menu}
        # Even so, the homepage should not be marked as active:
        self.assertFalse(nav_tags.check_if_link_is_active(context, homepage_link))

    def test_no_page_returns_false(self) -> None:
        """If no page is passed, the function should return False."""
        # Create a menu with the first dropdown linking to a page:
        page = wagtail_factories.PageFactory(parent=self.homepage, title="Test Page")
        menu = nav_factories.NavMenuFactory(
            dropdowns__0__dropdown__button__link_to="page",
            dropdowns__0__dropdown__button__page=page,
        )

        homepage_link = menu.dropdowns[0].value["button"]

        # No page is passed
        context: dict[Any, Any] = {}
        # Should return False
        self.assertFalse(nav_tags.check_if_link_is_active(context, homepage_link))
