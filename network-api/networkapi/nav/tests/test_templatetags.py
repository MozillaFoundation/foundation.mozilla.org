import wagtail_factories

from networkapi.nav import factories as nav_factories
from networkapi.nav.templatetags import nav_tags
from networkapi.wagtailpages.tests import base as test_base


class TestGetDropdownId(test_base.WagtailpagesTestCase):
    def test_get_dropdown_id(self) -> None:
        # Create a menu with 3 dropdowns:
        menu = nav_factories.NavMenuFactory()

        # Get the dropdown IDs:
        dropdown_1_id = nav_tags.get_dropdown_id(menu=menu, idx=0)
        dropdown_2_id = nav_tags.get_dropdown_id(menu=menu, idx=1)
        dropdown_3_id = nav_tags.get_dropdown_id(menu=menu, idx=2)
        dropdown_4_id = nav_tags.get_dropdown_id(menu=menu, idx=3)

        # Check if the IDs are correct:
        self.assertEqual(dropdown_1_id, menu.dropdowns.raw_data[0]["id"])
        self.assertEqual(dropdown_2_id, menu.dropdowns.raw_data[1]["id"])
        self.assertEqual(dropdown_3_id, menu.dropdowns.raw_data[2]["id"])
        self.assertEqual(dropdown_4_id, menu.dropdowns.raw_data[3]["id"])

    def test_get_dropdown_id_invalid_index(self) -> None:
        # Create a menu with 3 dropdowns:
        menu = nav_factories.NavMenuFactory()

        # Get the dropdown IDs with an invalid index:
        dropdown_id = nav_tags.get_dropdown_id(menu=menu, idx="invalid")

        # Check if the ID is None:
        self.assertIsNone(dropdown_id)


class TestCheckIfDropdownIsActive(test_base.WagtailpagesTestCase):
    def test_active_dropdown_check(self) -> None:
        # Create some pages:
        # pages ax linking to the first dropdown
        page_a1 = wagtail_factories.PageFactory(parent=self.homepage, title="Page A1")
        page_a2 = wagtail_factories.PageFactory(parent=self.homepage, title="Page A2")

        # page a3 not linked to the dropdown but a child of a2
        # (linked by being a child of the dropdown's CTA button link)
        page_a3 = wagtail_factories.PageFactory(parent=page_a2, title="Page A3")

        # page a4 not linked to the dropdown but a child of a1
        # (linked by being a child of a link inside the dropdown)
        page_a4 = wagtail_factories.PageFactory(parent=page_a1, title="Page A4")

        # pages bx linking to the second dropdown
        page_b1 = wagtail_factories.PageFactory(parent=self.homepage, title="Page B1")
        page_b2 = wagtail_factories.PageFactory(parent=self.homepage, title="Page B2")
        page_b3 = wagtail_factories.PageFactory(parent=self.homepage, title="Page B3")

        # Page c linked to third dropdown
        page_c = wagtail_factories.PageFactory(parent=self.homepage, title="Page C")

        # Page d not linked to any dropdowns
        page_d = wagtail_factories.PageFactory(parent=self.homepage, title="Page D")

        # Create a menu with links to the pages:
        menu = nav_factories.NavMenuFactory(
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

        dropdown_1_id = nav_tags.get_dropdown_id(menu=menu, idx=0)
        dropdown_2_id = nav_tags.get_dropdown_id(menu=menu, idx=1)
        dropdown_3_id = nav_tags.get_dropdown_id(menu=menu, idx=2)
        dropdown_4_id = nav_tags.get_dropdown_id(menu=menu, idx=3)

        # For pages a1 and a2:
        for page in [page_a1, page_a2, page_a3, page_a4]:
            with self.subTest(msg="Test {page}"):
                context = {"page": page, "menu": menu}
                # First dropdown should be active
                self.assertTrue(nav_tags.check_if_dropdown_is_active(context, dropdown_1_id))
                # While other shouldn't be
                self.assertFalse(nav_tags.check_if_dropdown_is_active(context, dropdown_2_id))
                self.assertFalse(nav_tags.check_if_dropdown_is_active(context, dropdown_3_id))
                self.assertFalse(nav_tags.check_if_dropdown_is_active(context, dropdown_4_id))

        # For pages b1, b2 and b3:
        for page in [page_b1, page_b2, page_b3]:
            with self.subTest(msg="Test {page}"):
                context = {"page": page, "menu": menu}
                # Second dropdown should be active
                self.assertTrue(nav_tags.check_if_dropdown_is_active(context, dropdown_2_id))
                # While other shouldn't be
                self.assertFalse(nav_tags.check_if_dropdown_is_active(context, dropdown_1_id))
                self.assertFalse(nav_tags.check_if_dropdown_is_active(context, dropdown_3_id))
                self.assertFalse(nav_tags.check_if_dropdown_is_active(context, dropdown_4_id))

        # For page c:
        context = {"page": page_c, "menu": menu}
        # Third dropdown does not define a CMS button link (the button link is external)
        # Hence, all dropdowns are inactive
        self.assertFalse(nav_tags.check_if_dropdown_is_active(context, dropdown_1_id))
        self.assertFalse(nav_tags.check_if_dropdown_is_active(context, dropdown_2_id))
        self.assertFalse(nav_tags.check_if_dropdown_is_active(context, dropdown_3_id))
        self.assertFalse(nav_tags.check_if_dropdown_is_active(context, dropdown_4_id))

        # For page d:
        context = {"page": page_d, "menu": menu}
        # All should be inactive
        self.assertFalse(nav_tags.check_if_dropdown_is_active(context, dropdown_1_id))
        self.assertFalse(nav_tags.check_if_dropdown_is_active(context, dropdown_2_id))
        self.assertFalse(nav_tags.check_if_dropdown_is_active(context, dropdown_3_id))
        self.assertFalse(nav_tags.check_if_dropdown_is_active(context, dropdown_4_id))

    def test_homepage_should_never_be_marked_as_active(self):
        """The homepage shouldn't receive 'active' markings."""
        # Create a menu with the first dropdown linking to the homepage:
        menu = nav_factories.NavMenuFactory(
            dropdowns__0__dropdown__button__link_to="page",
            dropdowns__0__dropdown__button__page=self.homepage,
        )

        dropdown_1_id = nav_tags.get_dropdown_id(menu=menu, idx=0)

        # User is now on homepage
        context = {"page": self.homepage, "menu": menu}
        # Even though the homepage is part of the dropdown, it should not be marked as active:
        self.assertFalse(nav_tags.check_if_dropdown_is_active(context, dropdown_1_id))


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
        # page_a should be active since it's the parent of page_a1:
        self.assertTrue(nav_tags.check_if_link_is_active(context, page_a_link))
        # page_b and page_c and page_d should not be active (not related to page_a):
        self.assertFalse(nav_tags.check_if_link_is_active(context, page_b_link))
        self.assertFalse(nav_tags.check_if_link_is_active(context, page_c_link))

        # Creating a page_b1 which is a child of page_b
        page_b1 = wagtail_factories.PageFactory(parent=page_b, title="Page B1")
        # User is now on page_b1
        context = {"page": page_b1, "menu": menu}
        # page_a should not be active:
        self.assertFalse(nav_tags.check_if_link_is_active(context, page_a_link))
        # page_b should be active since it's the parent of page_b1:
        self.assertTrue(nav_tags.check_if_link_is_active(context, page_b_link))
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
