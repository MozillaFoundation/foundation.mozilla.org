from types import SimpleNamespace

from django.test import SimpleTestCase

from foundation_cms.navigation import models as nav_models
from foundation_cms.navigation.templatetags.navigation_tags import (
    horizontal_link_active_url,
    horizontal_link_is_active,
    primary_nav_active_link,
    primary_nav_dropdown_is_active,
    primary_nav_link_is_active,
    primary_nav_link_is_current,
)


class HorizontalLinkIsActiveTests(SimpleTestCase):
    def test_exact_path_is_active_with_or_without_trailing_slash(self):
        self.assertTrue(horizontal_link_is_active("/events/mozfest/", "/events/mozfest"))

    def test_descendant_path_activates_ancestor_link(self):
        self.assertTrue(horizontal_link_is_active("/events/mozfest/schedule/", "/events/mozfest/"))

    def test_similar_path_segment_is_not_active(self):
        self.assertFalse(horizontal_link_is_active("/events/mozfestival/", "/events/mozfest/"))

    def test_query_string_and_fragment_do_not_affect_matching(self):
        self.assertTrue(horizontal_link_is_active("/events/mozfest/?day=1", "/events/mozfest/#schedule"))

    def test_external_link_is_never_active(self):
        self.assertFalse(horizontal_link_is_active("/events/mozfest/", "https://example.com/events/mozfest/", True))

    def test_root_link_only_matches_root(self):
        self.assertTrue(horizontal_link_is_active("/", "/"))
        self.assertFalse(horizontal_link_is_active("/events/", "/"))


class HorizontalLinkActiveUrlTests(SimpleTestCase):
    @staticmethod
    def link(url, is_external=False):
        return SimpleNamespace(value=SimpleNamespace(url=url, is_external=is_external))

    def test_returns_most_specific_matching_link(self):
        links = [
            self.link("/events/"),
            self.link("/events/mozfest/"),
            self.link("/events/mozfest/schedule/"),
        ]

        self.assertEqual(
            horizontal_link_active_url("/events/mozfest/schedule/day-one/", links),
            "/events/mozfest/schedule/",
        )

    def test_ignores_external_links(self):
        links = [self.link("https://example.com/events/", is_external=True)]

        self.assertIsNone(horizontal_link_active_url("/events/", links))

    def test_returns_none_without_a_matching_link(self):
        links = [self.link("/events/")]

        self.assertIsNone(horizontal_link_active_url("/about/", links))


class PrimaryNavActiveLinkTests(SimpleTestCase):
    @staticmethod
    def link(url, link_to="relative_url"):
        return {
            "label": url,
            "link_to": link_to,
            "page": None,
            "external_url": url if link_to == "external_url" else "",
            "relative_url": url if link_to != "external_url" else "",
        }

    @classmethod
    def dropdowns(cls, header_url, item_urls=None, header_link_to="relative_url"):
        value = [
            {
                "type": "dropdown",
                "value": {
                    "header": cls.link(header_url, header_link_to),
                    "items": [cls.link(url) for url in item_urls or []],
                },
            }
        ]
        return nav_models.NavigationMenu.dropdowns.field.stream_block.to_python(value)

    def test_matches_configured_locale_prefixes_and_unprefixed_links(self):
        localized = self.dropdowns("/en/join-us/")
        unprefixed = self.dropdowns("/join-us/")

        self.assertEqual(primary_nav_active_link("/de/join-us/", localized).url, "/en/join-us/")
        self.assertEqual(primary_nav_active_link("/de/join-us/", unprefixed).url, "/join-us/")

    def test_matches_regional_locale_prefix(self):
        dropdowns = self.dropdowns("/en/join-us/")

        self.assertEqual(primary_nav_active_link("/pt-BR/join-us/", dropdowns).url, "/en/join-us/")

    def test_does_not_strip_unsupported_first_segment(self):
        dropdowns = self.dropdowns("/join-us/")

        self.assertIsNone(primary_nav_active_link("/unsupported/join-us/", dropdowns))

    def test_descendant_path_activates_ancestor_link(self):
        dropdowns = self.dropdowns("/en/join-us/")

        self.assertEqual(primary_nav_active_link("/de/join-us/team/", dropdowns).url, "/en/join-us/")

    def test_similar_path_segment_is_not_active(self):
        dropdowns = self.dropdowns("/en/join-us/")

        self.assertIsNone(primary_nav_active_link("/de/join-us-too/", dropdowns))

    def test_query_strings_and_fragments_do_not_affect_matching(self):
        dropdowns = self.dropdowns("/de/join-us/#overview")

        self.assertEqual(
            primary_nav_active_link("/en/join-us/?source=nav", dropdowns).url,
            "/de/join-us/#overview",
        )

    def test_external_url_is_rejected_even_without_link_type_metadata(self):
        dropdowns = self.dropdowns("https://example.com/de/join-us/", header_link_to="")

        self.assertFalse(dropdowns[0].value.header_value.is_external)
        self.assertIsNone(primary_nav_active_link("/de/join-us/", dropdowns))

    def test_query_only_link_is_never_active(self):
        dropdowns = self.dropdowns("?form=donate-header")

        self.assertIsNone(primary_nav_active_link("/de/join-us/", dropdowns))

    def test_locale_root_link_only_matches_locale_root(self):
        dropdowns = self.dropdowns("/en/")

        self.assertEqual(primary_nav_active_link("/de/", dropdowns).url, "/en/")
        self.assertIsNone(primary_nav_active_link("/de/join-us/", dropdowns))

    def test_returns_most_specific_matching_dropdown_item(self):
        dropdowns = self.dropdowns("/en/join-us/", ["/en/join-us/events/"])

        active_link = primary_nav_active_link("/de/join-us/events/day-one/", dropdowns)

        self.assertIs(active_link, dropdowns[0].value.dropdown_items[0])

    def test_duplicate_urls_select_only_first_link(self):
        dropdowns = self.dropdowns("/join-us/", ["/join-us/"])
        header = dropdowns[0].value.header_value
        duplicate = dropdowns[0].value.dropdown_items[0]

        active_link = primary_nav_active_link("/join-us/", dropdowns)

        self.assertIs(active_link, header)
        self.assertTrue(primary_nav_link_is_active(active_link, header))
        self.assertFalse(primary_nav_link_is_active(active_link, duplicate))

    def test_dropdown_helper_finds_selected_child_by_identity(self):
        dropdowns = self.dropdowns("/join-us/", ["/join-us/events/"])
        dropdown = dropdowns[0].value
        child = dropdown.dropdown_items[0]

        self.assertTrue(primary_nav_dropdown_is_active(child, dropdown))
        self.assertFalse(primary_nav_dropdown_is_active(None, dropdown))

    def test_current_helper_requires_an_exact_localized_path(self):
        link = self.dropdowns("/en/join-us/")[0].value.header_value

        self.assertTrue(primary_nav_link_is_current("/de/join-us/", link))
        self.assertFalse(primary_nav_link_is_current("/de/join-us/team/", link))
