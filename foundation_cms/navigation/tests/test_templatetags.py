from types import SimpleNamespace

from django.test import SimpleTestCase

from foundation_cms.navigation.templatetags.navigation_tags import (
    horizontal_link_active_url,
    horizontal_link_is_active,
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
