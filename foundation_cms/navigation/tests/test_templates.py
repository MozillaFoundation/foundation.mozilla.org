from django.contrib.auth.models import AnonymousUser
from django.template.loader import render_to_string
from django.test import RequestFactory, override_settings

from foundation_cms.legacy_apps.wagtailpages.tests import base as test_base
from foundation_cms.navigation import factories as nav_factories
from foundation_cms.navigation import models as nav_models


@override_settings(
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    }
)
class PrimaryNavigationTemplateTests(test_base.WagtailpagesTestCase):
    def setUp(self):
        super().setUp()
        nav_models.NavigationMenu.objects.all().delete()
        settings = nav_models.SiteNavigationMenu.for_site(self.site)
        settings.active_navigation_menu = None
        settings.save(update_fields=["active_navigation_menu"])

    def request(self, path="/"):
        request = RequestFactory().get(path, HTTP_HOST=self.site.hostname)
        request.site = self.site
        request.user = AnonymousUser()
        return request

    def render_primary_navigation(self, path="/"):
        menu = nav_factories.generate(self.site)
        return render_to_string(
            "patterns/components/navigation/primary_nav.html",
            {"menu": menu, "page": self.homepage},
            request=self.request(path),
        )

    def test_cms_navigation_renders_default_links_and_search_drawer(self):
        html = self.render_primary_navigation()

        self.assertIn('href="/meet-mozilla/"', html)
        self.assertIn('href="/what-we-do/imagine/"', html)
        self.assertIn('href="/join-us/"', html)
        self.assertIn('href="/nothing-personal/"', html)
        self.assertIn('id="primary-nav-ns-menu"', html)
        self.assertIn('class="search-toggle"', html)
        self.assertIn('class="search-input-container"', html)

    def test_redesign_parent_legacy_template_uses_cms_navigation(self):
        nav_factories.generate(self.site)

        html = render_to_string(
            "pages/base.html",
            {
                "model": self.homepage,
                "object": self.homepage,
                "page": self.homepage,
                "parent_homepage": "redesign",
                "self": self.homepage,
            },
            request=self.request(),
        )

        self.assertIn('href="/meet-mozilla/"', html)
        self.assertIn('id="primary-nav-ns-menu"', html)

    def test_navigation_preview_uses_preview_menu_without_an_active_site_menu(self):
        preview_menu = nav_factories.generate(self.site)
        settings = nav_models.SiteNavigationMenu.for_site(self.site)
        settings.active_navigation_menu = None
        settings.save(update_fields=["active_navigation_menu"])
        request = self.request("/cms/preview/")
        context = preview_menu.get_preview_context(request, mode_name="")

        html = render_to_string("previews/navigation.html", context, request=request)

        self.assertIn('href="/meet-mozilla/"', html)
        self.assertIn('id="primary-nav-ns-menu"', html)

    def test_localized_exact_top_level_link_is_current(self):
        html = self.render_primary_navigation("/de/join-us/")

        self.assertIn("primary-nav-ns__menu-item primary-nav-ns__menu-item--active", html)
        self.assertInHTML(
            """
            <a href="/join-us/"
               class="nav-link primary-nav-ns__link primary-nav-ns__link--active"
               aria-current="page">Join Us</a>
            """,
            html,
        )
        self.assertEqual(html.count('aria-current="page"'), 1)

    def test_exact_dropdown_child_is_current_and_activates_parent(self):
        html = self.render_primary_navigation("/de/what-we-do/imagine/")

        self.assertIn("primary-nav-ns__menu-item primary-nav-ns__menu-item--active", html)
        self.assertInHTML(
            """
            <a href="/what-we-do/imagine/"
               class="nav-link primary-nav-ns__link primary-nav-ns__link--active"
               aria-current="page">Imagine</a>
            """,
            html,
        )
        self.assertEqual(html.count('aria-current="page"'), 1)

    def test_descendant_activates_section_without_claiming_current_page(self):
        html = self.render_primary_navigation("/de/what-we-do/imagine/article/")

        self.assertIn("primary-nav-ns__menu-item primary-nav-ns__menu-item--active", html)
        self.assertInHTML(
            """
            <a href="/what-we-do/imagine/"
               class="nav-link primary-nav-ns__link primary-nav-ns__link--active">Imagine</a>
            """,
            html,
        )
        self.assertNotIn('aria-current="page"', html)
