from types import SimpleNamespace

from django.template.loader import render_to_string
from django.test import RequestFactory

from foundation_cms.legacy_apps.wagtailpages.tests import base as test_base


class PrimaryNavTemplateTests(test_base.WagtailpagesTestCase):
    @staticmethod
    def link(label, url, is_external=False):
        return SimpleNamespace(
            label=label,
            url=url,
            is_external=is_external,
            new_window=False,
        )

    @classmethod
    def dropdown(cls, header, items=None):
        value = SimpleNamespace(
            header=header,
            header_value=header,
            dropdown_items=items or [],
        )
        return SimpleNamespace(value=value)

    def render_primary_nav(self, path, dropdowns):
        request = RequestFactory().get(path)
        return render_to_string(
            "patterns/components/navigation/primary_nav.html",
            {
                "menu": SimpleNamespace(dropdowns=dropdowns),
                "page": SimpleNamespace(locale=None),
            },
            request=request,
        )

    def test_primary_nav_renders_active_top_level_link(self):
        dropdowns = [
            self.dropdown(self.link("Join Us", "/de/join-us/")),
            self.dropdown(self.link("About", "/de/about/")),
        ]

        html = self.render_primary_nav("/de/join-us/", dropdowns)

        self.assertIn("primary-nav-ns__menu-item primary-nav-ns__menu-item--active", html)
        self.assertIn('class="nav-link primary-nav-ns__link primary-nav-ns__link--active"', html)
        self.assertIn('aria-current="page"', html)
        self.assertEqual(html.count('aria-current="page"'), 1)

    def test_primary_nav_marks_active_dropdown_item_and_parent_menu_item(self):
        dropdowns = [
            self.dropdown(
                self.link("Join Us", "/en/join-us/"),
                [self.link("Events", "/en/join-us/events/")],
            )
        ]

        html = self.render_primary_nav("/de/join-us/events/day-one/", dropdowns)

        self.assertIn("primary-nav-ns__menu-item primary-nav-ns__menu-item--active", html)
        self.assertIn('href="/en/join-us/events/"', html)
        self.assertIn('class="nav-link primary-nav-ns__link primary-nav-ns__link--active"', html)
        self.assertEqual(html.count('aria-current="page"'), 1)

    def test_primary_nav_does_not_mark_external_links_active(self):
        dropdowns = [self.dropdown(self.link("External Join", "https://example.com/de/join-us/", is_external=True))]

        html = self.render_primary_nav("/de/join-us/", dropdowns)

        self.assertNotIn("primary-nav-ns__link--active", html)
        self.assertNotIn('aria-current="page"', html)

    def test_static_primary_nav_renders_active_link_across_locale_prefixes(self):
        request = RequestFactory().get("/de/join-us/")

        html = render_to_string("patterns/components/primary_nav.html", request=request)

        self.assertIn('href="/join-us/"', html)
        self.assertIn('class="nav-link primary-nav-ns__link primary-nav-ns__link--active"', html)
        self.assertIn('aria-current="page"', html)
        self.assertEqual(html.count('aria-current="page"'), 1)
