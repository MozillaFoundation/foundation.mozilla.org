from django.template import Context, Template
from django.template.loader import render_to_string
from django.test import TestCase
from django.urls import reverse
from django.utils import translation
from wagtail.models import Locale

from foundation_cms.navigation import factories as nav_factories


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
        self.assertIn("search-suggestions", html)
        self.assertIn('aria-label="Search"', html)
        self.assertNotIn("search-input-container--form-only", html)
        self.assertIn("privacy", html)
        self.assertIn(f'href="{reverse("search")}?query=privacy"', html)
        self.assertIn("Grantmaking", html)
        self.assertIn('href="/what-we-do/awards/"', html)


class TranslatedMenuTemplateTagTests(TestCase):
    def test_uses_active_locale_when_page_is_not_in_context(self):
        french_locale, _ = Locale.objects.get_or_create(language_code="fr")
        menu = nav_factories.NavigationMenuFactory()
        translated_menu = menu.copy_for_translation(french_locale)
        translated_menu.title = "Navigation française"
        translated_menu.save()

        template = Template(
            "{% load navigation_tags %}" "{% translated_menu menu as localized_menu %}" "{{ localized_menu.title }}"
        )

        with translation.override("fr"):
            html = template.render(Context({"menu": menu}))

        self.assertEqual(html, "Navigation française")
