from django.contrib.auth.models import AnonymousUser
from django.template.loader import render_to_string
from django.test import RequestFactory, TestCase, override_settings
from django.urls import reverse

from foundation_cms.legacy_apps.wagtailpages.tests import base as test_base
from foundation_cms.navigation import factories as nav_factories
from foundation_cms.navigation import models as nav_models


class SearchDrawerTemplateTests(TestCase):
    def render_search_drawer(self, **context):
        return render_to_string(
            "patterns/components/navigation/search_drawer.html",
            context,
        )

    def test_search_drawer_does_not_render_fallback_suggestions(self):
        html = self.render_search_drawer(search_topic_links=[], search_quick_links=[])

        self.assertIn("search-input-container--form-only", html)
        self.assertNotIn("Explore our ideas", html)
        self.assertNotIn("Quick Links", html)
        self.assertNotIn("Grantmaking", html)
        self.assertNotIn("privacy", html)

    def test_search_drawer_renders_configured_suggestions(self):
        menu = nav_factories.NavigationMenuFactory()
        html = self.render_search_drawer(
            search_topic_links=menu.search_topic_links,
            search_quick_links=menu.search_quick_links,
        )

        self.assertIn("Explore our ideas", html)
        self.assertIn("Quick Links", html)
        self.assertNotIn("search-input-container--form-only", html)
        self.assertIn("privacy", html)
        self.assertIn(f'href="{reverse("search")}?query=privacy"', html)
        self.assertIn('placeholder="Search"', html)
        self.assertIn("Grantmaking", html)
        self.assertIn('href="/what-we-do/awards/"', html)

    def test_search_drawer_limits_quick_links_to_three(self):
        menu = nav_factories.NavigationMenuFactory()
        quick_links = [*menu.search_quick_links, menu.search_quick_links[0]]

        html = self.render_search_drawer(search_topic_links=[], search_quick_links=quick_links)

        self.assertEqual(html.count("Grantmaking"), 1)


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

    def test_cms_navigation_renders_default_links_and_search_drawer(self):
        menu = nav_factories.generate(self.site)

        html = render_to_string(
            "patterns/components/navigation/primary_nav.html",
            {"menu": menu, "page": self.homepage},
            request=self.request(),
        )

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
