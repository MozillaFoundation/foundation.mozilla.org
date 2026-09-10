from types import SimpleNamespace
from unittest.mock import MagicMock, patch

from bs4 import BeautifulSoup
from django.template.loader import render_to_string
from django.test import RequestFactory, SimpleTestCase, override_settings
from django.utils.text import Truncator
from wagtail import models as wagtail_models
from wagtail_ab_testing.models import AbTest

from foundation_cms.templatetags.app_environment_tags import (
    environment_prefix,
    get_app_environment,
)
from foundation_cms.templatetags.breadcrumb_nav import breadcrumb_nav
from foundation_cms.templatetags.language_switcher_tags import localized_url
from foundation_cms.templatetags.nothing_personal_tags import (
    nothing_personal_homepage_url,
)
from foundation_cms.templatetags.responsive_image_tags import (
    colon_to_slash,
    is_webp,
    orientation_to_ratio,
    responsive_image,
)
from foundation_cms.templatetags.url_query import url_with_query
from foundation_cms.templatetags.utility_tags import to_range
from foundation_cms.templatetags.wagtailcustom_tags import wagtail_ab_testing_script

# Utility Tags Tests


class ToRangeFilterTests(SimpleTestCase):
    def test_returns_range_for_positive_int(self):
        self.assertEqual(list(to_range(3)), [0, 1, 2])

    def test_returns_empty_range_for_zero(self):
        self.assertEqual(list(to_range(0)), [])


# App Environment Tests


class GetAppEnvironmentTests(SimpleTestCase):
    @override_settings(APP_ENVIRONMENT="Staging")
    def test_returns_current_app_environment(self):
        self.assertEqual(get_app_environment(), "Staging")


class EnvironmentPrefixTests(SimpleTestCase):
    @override_settings(APP_ENVIRONMENT="Staging")
    def test_staging_returns_s_prefix(self):
        self.assertEqual(environment_prefix({}), "[S]")

    @override_settings(APP_ENVIRONMENT="Review")
    def test_review_returns_ra_prefix(self):
        self.assertEqual(environment_prefix({}), "[RA]")

    @override_settings(APP_ENVIRONMENT="Production")
    def test_other_env_returns_empty_string(self):
        self.assertEqual(environment_prefix({}), "")


# Responsive Image Tags Tests


def _make_image(filename="photo.jpg"):
    """Minimal image-like object; get_rendition returns a fresh mock per call."""
    img = SimpleNamespace(file=SimpleNamespace(name=filename))
    img.get_rendition = MagicMock(side_effect=lambda spec: SimpleNamespace(spec=spec))
    return img


class IsWebpFilterTests(SimpleTestCase):
    def test_returns_true_for_webp_extension(self):
        self.assertTrue(is_webp(_make_image("photo.webp")))

    def test_case_insensitive_webp_match(self):
        self.assertTrue(is_webp(_make_image("photo.WEBP")))

    def test_returns_false_for_non_webp(self):
        self.assertFalse(is_webp(_make_image("photo.jpg")))

    def test_returns_false_for_none(self):
        self.assertFalse(is_webp(None))

    def test_returns_false_when_image_has_no_file_attribute(self):
        self.assertFalse(is_webp(SimpleNamespace()))


class ColonToSlashTests(SimpleTestCase):
    def test_converts_colon_separator_to_slash(self):
        self.assertEqual(colon_to_slash("2:3"), "2/3")

    def test_preserves_string_without_colon(self):
        self.assertEqual(colon_to_slash("16-9"), "16-9")


class OrientationToRatioTests(SimpleTestCase):
    def test_known_orientations_map_to_expected_ratios(self):
        cases = {
            "landscape": "3:2",
            "portrait": "2:3",
            "square": "1:1",
            "widescreen": "16:9",
        }
        for orientation, expected in cases.items():
            with self.subTest(orientation=orientation):
                self.assertEqual(orientation_to_ratio(orientation), expected)

    def test_unknown_orientation_defaults_to_landscape_ratio(self):
        self.assertEqual(orientation_to_ratio("unknown"), "3:2")


class ResponsiveImageTagTests(SimpleTestCase):
    def test_returns_empty_dict_for_none_image(self):
        self.assertEqual(responsive_image(None, "3:2"), {})

    def test_raises_for_ratio_missing_colon(self):
        with self.assertRaises(ValueError):
            responsive_image(_make_image(), "16x9")

    def test_raises_for_ratio_with_non_positive_values(self):
        with self.assertRaises(ValueError):
            responsive_image(_make_image(), "0:3")

    def test_webp_image_skips_rendition_generation(self):
        result = responsive_image(_make_image("photo.webp"), "3:2")
        self.assertTrue(result["is_webp"])
        self.assertEqual(result["renditions"], [])
        self.assertIsNone(result["primary_rendition"])

    def test_non_webp_generates_four_renditions(self):
        result = responsive_image(_make_image(), "3:2", base_width=100)
        self.assertEqual(len(result["renditions"]), 4)

    def test_primary_rendition_is_1_5x_rendition(self):
        # Second rendition (index 1, 1.5×) is the default src for good quality/size balance.
        img = _make_image()
        renditions_made = []
        img.get_rendition = lambda spec: renditions_made.append(spec) or SimpleNamespace(spec=spec)
        result = responsive_image(img, "3:2", base_width=100)
        self.assertEqual(result["primary_rendition"].spec, renditions_made[1])

    def test_sizes_attribute_is_passed_through(self):
        result = responsive_image(_make_image(), "3:2", sizes="100vw")
        self.assertEqual(result["sizes"], "100vw")


# Url Query Tests


class UrlWithQueryTests(SimpleTestCase):
    @staticmethod
    def ctx(params=None):
        return {"request": RequestFactory().get("/", params or {})}

    def test_base_url_with_single_override(self):
        self.assertEqual(url_with_query(self.ctx(), base_url="/search/", page=2), "/search/?page=2")

    def test_merges_existing_request_params_with_overrides(self):
        url = url_with_query(self.ctx({"q": "privacy"}), base_url="/search/", page=2)
        self.assertIn("q=privacy", url)
        self.assertIn("page=2", url)

    def test_override_replaces_existing_param(self):
        url = url_with_query(self.ctx({"page": "1"}), base_url="/search/", page=3)
        self.assertNotIn("page=1", url)
        self.assertIn("page=3", url)

    def test_none_value_removes_param(self):
        url = url_with_query(self.ctx({"page": "2"}), base_url="/search/", page=None)
        self.assertNotIn("page", url)

    def test_empty_string_removes_param(self):
        url = url_with_query(self.ctx({"q": "privacy"}), base_url="/search/", q="")
        self.assertNotIn("q=", url)

    def test_list_value_generates_multiple_query_values(self):
        url = url_with_query(self.ctx(), base_url="/search/", tag=["privacy", "security"])
        self.assertIn("tag=privacy", url)
        self.assertIn("tag=security", url)

    def test_tuple_value_generates_multiple_query_values(self):
        url = url_with_query(self.ctx(), base_url="/search/", tag=("a", "b"))
        self.assertIn("tag=a", url)
        self.assertIn("tag=b", url)

    def test_returns_base_url_when_no_params_present(self):
        self.assertEqual(url_with_query({"request": None}, base_url="/search/"), "/search/")

    def test_raises_without_viewname_or_base_url(self):
        with self.assertRaises(ValueError):
            url_with_query(self.ctx())

    @patch("foundation_cms.templatetags.url_query.reverse", return_value="/search/")
    def test_resolves_viewname_via_reverse(self, mock_reverse):
        url = url_with_query(self.ctx(), "search_view", page=1)
        mock_reverse.assert_called_once_with("search_view")
        self.assertIn("page=1", url)


# Language Switcher Tests
# DEFAULT_LOCALE_CODE is captured from settings.


class LocalizedUrlTests(SimpleTestCase):
    @staticmethod
    def ctx():
        return {"request": RequestFactory().get("/en/about/")}

    def test_replaces_default_locale_prefix_with_given_locale(self):
        self.assertEqual(localized_url(self.ctx(), "/en/about/", language_code="fr"), "/fr/about/")

    def test_default_locale_returns_url_unchanged(self):
        # "en" == DEFAULT_LOCALE_CODE
        self.assertEqual(localized_url(self.ctx(), "/en/about/", language_code="en"), "/en/about/")

    def test_no_request_returns_url_unchanged(self):
        self.assertEqual(localized_url({"request": None}, "/en/about/", language_code="fr"), "/en/about/")

    def test_url_without_matching_prefix_is_returned_unchanged(self):
        self.assertEqual(localized_url(self.ctx(), "/privacy/", language_code="de"), "/privacy/")


# Wagtail Custom Tests


class WagtailAbTestingScriptTests(SimpleTestCase):
    @staticmethod
    def ctx(serving_variant=False, ab_test=None, page=None):
        request = SimpleNamespace(
            wagtail_ab_testing_serving_variant=serving_variant,
            wagtail_ab_testing_test=ab_test,
        )
        return {"request": request, "page": page}

    @patch("foundation_cms.templatetags.wagtailcustom_tags.request_is_trackable", return_value=False)
    def test_returns_control_version_by_default(self, _):
        self.assertEqual(wagtail_ab_testing_script(self.ctx())["version"], AbTest.VERSION_CONTROL)

    @patch("foundation_cms.templatetags.wagtailcustom_tags.request_is_trackable", return_value=False)
    def test_returns_variant_version_when_flag_is_set(self, _):
        self.assertEqual(
            wagtail_ab_testing_script(self.ctx(serving_variant=True))["version"],
            AbTest.VERSION_VARIANT,
        )

    @patch("foundation_cms.templatetags.wagtailcustom_tags.request_is_trackable", return_value=True)
    def test_track_reflects_request_trackability(self, _):
        self.assertTrue(wagtail_ab_testing_script(self.ctx())["track"])

    @patch("foundation_cms.templatetags.wagtailcustom_tags.request_is_trackable", return_value=False)
    def test_passes_page_and_test_from_context(self, _):
        fake_page = object()
        fake_test = object()
        result = wagtail_ab_testing_script(self.ctx(ab_test=fake_test, page=fake_page))
        self.assertIs(result["page"], fake_page)
        self.assertIs(result["test"], fake_test)


# Breadcrumb Nav Tests


class BreadcrumbNavTests(SimpleTestCase):
    @staticmethod
    def ctx(page=None):
        return {"request": RequestFactory().get("/en/about/"), "page": page}

    @staticmethod
    def _page_with_ancestors(ancestors):
        page = MagicMock()
        page.get_ancestors.return_value.filter.return_value = ancestors
        return page

    def test_returns_empty_when_no_page_in_context(self):
        result = breadcrumb_nav(self.ctx(page=None))
        self.assertEqual(result["breadcrumbs"], [])
        self.assertEqual(result["mobile_breadcrumbs"], [])
        self.assertFalse(result["mobile_show_leading_slash"])

    def test_returns_empty_when_no_request(self):
        result = breadcrumb_nav({"request": None, "page": MagicMock()})
        self.assertEqual(result["breadcrumbs"], [])

    @patch("foundation_cms.templatetags.breadcrumb_nav.wagtail_models.Site.find_for_request", return_value=None)
    def test_top_level_page_produces_no_breadcrumbs(self, _):
        ancestor = SimpleNamespace(localized=SimpleNamespace())
        result = breadcrumb_nav(self.ctx(self._page_with_ancestors([ancestor])))
        self.assertFalse(result["breadcrumbs"])
        self.assertEqual(result["mobile_breadcrumbs"], [ancestor.localized])
        self.assertFalse(result["mobile_show_leading_slash"])

    @patch("foundation_cms.templatetags.breadcrumb_nav.wagtail_models.Site.find_for_request", return_value=None)
    def test_child_page_uses_full_trail_on_desktop_and_mobile(self, _):
        ancestors = [SimpleNamespace(localized=SimpleNamespace(title=title)) for title in ("Parent", "Current")]
        result = breadcrumb_nav(self.ctx(self._page_with_ancestors(ancestors)))
        self.assertEqual([page.title for page in result["breadcrumbs"]], ["Parent", "Current"])
        self.assertEqual([page.title for page in result["mobile_breadcrumbs"]], ["Parent", "Current"])
        self.assertFalse(result["mobile_show_leading_slash"])

    @patch("foundation_cms.templatetags.breadcrumb_nav.wagtail_models.Site.find_for_request", return_value=None)
    def test_deep_page_uses_full_desktop_trail_and_last_two_mobile_items(self, _):
        ancestors = [
            SimpleNamespace(localized=SimpleNamespace(title=title)) for title in ("Section", "Parent", "Current")
        ]
        result = breadcrumb_nav(self.ctx(self._page_with_ancestors(ancestors)))
        self.assertEqual([page.title for page in result["breadcrumbs"]], ["Section", "Parent", "Current"])
        self.assertEqual([page.title for page in result["mobile_breadcrumbs"]], ["Parent", "Current"])
        self.assertTrue(result["mobile_show_leading_slash"])


class BreadcrumbNavTemplateTests(SimpleTestCase):
    request = RequestFactory().get("/en/parent/current/")

    @staticmethod
    def _page(title, url):
        page = MagicMock(spec=wagtail_models.Page)
        page.do_not_call_in_templates = True
        page.title = title
        page.get_url.return_value = url
        return page

    def _render(self, breadcrumbs, mobile_breadcrumbs=None, mobile_show_leading_slash=False):
        return render_to_string(
            "patterns/components/_breadcrumb_nav.html",
            {
                "breadcrumbs": breadcrumbs,
                "mobile_breadcrumbs": mobile_breadcrumbs if mobile_breadcrumbs is not None else breadcrumbs,
                "mobile_show_leading_slash": mobile_show_leading_slash,
            },
            request=self.request,
        )

    def test_empty_desktop_trail_does_not_render_breadcrumb_navigation(self):
        self.assertNotIn("<nav", self._render([], []))

    def test_child_trails_render_ancestor_link_and_one_unlinked_current_item_each(self):
        parent = self._page("Parent", "/en/parent/")
        current = self._page("Current", "/en/parent/current/")
        soup = BeautifulSoup(self._render([parent, current]), "html.parser")

        for selector in (".breadcrumb__list--desktop", ".breadcrumb__list--mobile"):
            with self.subTest(selector=selector):
                trail = soup.select_one(selector)
                ancestor = trail.select_one(".breadcrumb__link")
                current_item = trail.select_one(".breadcrumb__current")

                self.assertEqual(ancestor.get_text(strip=True), "Parent")
                self.assertEqual(ancestor["href"], "/en/parent/")
                self.assertEqual(current_item.get_text(strip=True), "Current")
                self.assertIsNone(current_item.find_parent("a"))
                self.assertEqual(len(trail.select('[aria-current="page"]')), 1)

    def test_titles_are_truncated_to_thirty_characters(self):
        long_title = "A breadcrumb title that is deliberately longer than thirty characters"
        parent = self._page("Parent", "/en/parent/")
        current = self._page(long_title, "/en/parent/current/")
        soup = BeautifulSoup(self._render([parent, current]), "html.parser")
        expected_title = Truncator(long_title).chars(30)

        self.assertEqual(
            [item.get_text(strip=True) for item in soup.select(".breadcrumb__current")],
            [expected_title, expected_title],
        )
        self.assertNotIn(long_title, soup.get_text())


# Nothin Personal Tests


class NothingPersonalHomepageUrlTests(SimpleTestCase):
    @staticmethod
    def ctx():
        return {"request": RequestFactory().get("/en/")}

    @patch("foundation_cms.templatetags.nothing_personal_tags.NothingPersonalHomePage")
    @patch("foundation_cms.templatetags.nothing_personal_tags.Locale")
    def test_returns_url_for_current_locale_homepage(self, mock_locale, mock_model):
        mock_locale.objects.get.return_value = mock_locale
        mock_locale.get_default.return_value = object()
        fake_page = SimpleNamespace(get_url=lambda request: "/en/nothing-personal/")
        mock_model.objects.live.return_value.filter.return_value.first.return_value = fake_page
        self.assertEqual(nothing_personal_homepage_url(self.ctx()), "/en/nothing-personal/")

    @patch("foundation_cms.templatetags.nothing_personal_tags.NothingPersonalHomePage")
    @patch("foundation_cms.templatetags.nothing_personal_tags.Locale")
    def test_returns_empty_string_when_no_homepage_exists_in_any_locale(self, mock_locale, mock_model):
        mock_locale.objects.get.return_value = mock_locale
        mock_locale.get_default.return_value = mock_locale
        mock_model.objects.live.return_value.filter.return_value.first.return_value = None
        self.assertEqual(nothing_personal_homepage_url(self.ctx()), "")
