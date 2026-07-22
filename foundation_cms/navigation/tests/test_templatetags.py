from types import SimpleNamespace

from django.test import SimpleTestCase

from foundation_cms.navigation.templatetags.navigation_tags import (
    horizontal_link_active_url,
    horizontal_link_is_active,
    primary_nav_active_url,
    primary_nav_dropdown_is_active,
    primary_nav_link_is_active,
    primary_nav_url_is_active,
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


class PrimaryNavActiveUrlTests(SimpleTestCase):
    @staticmethod
    def link(url, is_external=False):
        return SimpleNamespace(url=url, is_external=is_external)

    @classmethod
    def dropdown(cls, header_url, item_urls=None):
        return SimpleNamespace(
            value=SimpleNamespace(
                header_value=cls.link(header_url),
                dropdown_items=[cls.link(url) for url in item_urls or []],
            )
        )

    def test_matches_active_url_across_locale_prefixes(self):
        dropdowns = [self.dropdown("/en/join-us/")]

        self.assertEqual(primary_nav_active_url("/de/join-us/", dropdowns), "/en/join-us/")

    def test_matches_unprefixed_fallback_url_on_localized_path(self):
        dropdowns = [self.dropdown("/join-us/")]

        self.assertEqual(primary_nav_active_url("/de/join-us/", dropdowns), "/join-us/")

    def test_descendant_path_activates_ancestor_link(self):
        dropdowns = [self.dropdown("/en/join-us/")]

        self.assertEqual(primary_nav_active_url("/de/join-us/team/", dropdowns), "/en/join-us/")

    def test_similar_path_segment_is_not_active(self):
        dropdowns = [self.dropdown("/en/join-us/")]

        self.assertIsNone(primary_nav_active_url("/de/join-us-too/", dropdowns))

    def test_query_strings_and_fragments_do_not_affect_matching(self):
        dropdowns = [self.dropdown("/de/join-us/#overview")]

        self.assertEqual(primary_nav_active_url("/en/join-us/?source=nav", dropdowns), "/de/join-us/#overview")

    def test_external_and_query_only_links_are_never_active(self):
        dropdowns = [
            SimpleNamespace(
                value=SimpleNamespace(
                    header_value=self.link("https://example.com/de/join-us/", is_external=True),
                    dropdown_items=[self.link("?form=donate-header")],
                )
            )
        ]

        self.assertIsNone(primary_nav_active_url("/de/join-us/", dropdowns))

    def test_root_link_only_matches_root(self):
        dropdowns = [self.dropdown("/en/")]

        self.assertEqual(primary_nav_active_url("/de/", dropdowns), "/en/")
        self.assertIsNone(primary_nav_active_url("/de/join-us/", dropdowns))

    def test_returns_most_specific_matching_dropdown_item(self):
        dropdowns = [self.dropdown("/en/join-us/", ["/en/join-us/events/"])]

        self.assertEqual(
            primary_nav_active_url("/de/join-us/events/day-one/", dropdowns),
            "/en/join-us/events/",
        )

    def test_link_and_dropdown_active_helpers_use_selected_active_url(self):
        child = self.link("/en/join-us/events/")
        dropdown = SimpleNamespace(
            header_value=self.link("/en/join-us/"),
            dropdown_items=[child],
        )

        self.assertTrue(primary_nav_link_is_active("/en/join-us/events/", child))
        self.assertTrue(primary_nav_dropdown_is_active("/en/join-us/events/", dropdown))
        self.assertFalse(primary_nav_link_is_active("/en/join-us/", child))


class PrimaryNavUrlIsActiveTests(SimpleTestCase):
    def test_matches_across_locale_prefixes(self):
        self.assertTrue(primary_nav_url_is_active("/de/join-us/", "/join-us/"))
        self.assertTrue(primary_nav_url_is_active("/de/join-us/", "/en/join-us/"))

    def test_does_not_match_similar_segments(self):
        self.assertFalse(primary_nav_url_is_active("/de/join-us-too/", "/join-us/"))

    def test_external_urls_are_not_active(self):
        self.assertFalse(primary_nav_url_is_active("/de/join-us/", "https://example.com/de/join-us/", True))
