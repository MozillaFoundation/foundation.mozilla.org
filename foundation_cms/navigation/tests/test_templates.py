from urllib.parse import urlsplit

from django.contrib.auth.models import AnonymousUser
from django.template import Context, Template
from django.template.loader import render_to_string
from django.test import RequestFactory, TestCase, override_settings
from django.urls import reverse
from django.utils import translation
from wagtail import models as wagtail_models
from wagtail.models import Locale

from foundation_cms.legacy_apps.wagtailpages.tests import base as test_base
from foundation_cms.navigation import factories as nav_factories
from foundation_cms.navigation import models as nav_models


class SearchDrawerTemplateTests(TestCase):
    def render_search_drawer(self, **context):
        return render_to_string(
            "patterns/components/navigation/_search_drawer.html",
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
        self.assertIn('placeholder="Search"', html)
        self.assertIn("Grantmaking", html)
        self.assertIn('href="/what-we-do/awards/"', html)

    def test_search_drawer_limits_quick_links_to_three(self):
        menu = nav_factories.NavigationMenuFactory()
        quick_links = [*menu.search_quick_links, menu.search_quick_links[0]]

        html = self.render_search_drawer(search_topic_links=[], search_quick_links=quick_links)

        self.assertEqual(html.count("Grantmaking"), 1)


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


@override_settings(
    ALLOWED_HOSTS=["localhost", "testserver", "primary.test", "secondary.test"],
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    },
)
class PrimaryNavigationTemplateTests(test_base.WagtailpagesTestCase):
    def setUp(self):
        super().setUp()
        nav_models.NavigationMenu.objects.all().delete()
        settings = nav_models.SiteNavigationMenu.for_site(self.site)
        settings.active_navigation_menu = None
        settings.save(update_fields=["active_navigation_menu"])

    def request(self, path="/", host=None):
        request = RequestFactory().get(path, HTTP_HOST=host or self.site.hostname)
        request.site = self.site
        request.user = AnonymousUser()
        return request

    def render_primary_navigation(self, path="/", menu=None, page=None, host=None):
        menu = menu or nav_factories.generate(self.site)
        return render_to_string(
            "patterns/components/navigation/primary_nav.html",
            {"menu": menu, "page": page or self.homepage},
            request=self.request(path, host=host),
        )

    @staticmethod
    def page_link(label, page, include_link_to=True):
        return {
            "label": label,
            **({"link_to": "page"} if include_link_to else {}),
            "page": page.pk,
            "external_url": "",
            "relative_url": "",
        }

    @staticmethod
    def create_page(parent, title, slug):
        return parent.add_child(instance=wagtail_models.Page(title=title, slug=slug))

    def create_multisite_pages(self):
        self.site.hostname = "primary.test"
        self.site.port = 80
        self.site.save(update_fields=["hostname", "port"])

        primary_section = self.create_page(self.homepage, "Primary section", "shared")
        primary_child = self.create_page(primary_section, "Primary child", "child")
        primary_grandchild = self.create_page(primary_child, "Primary grandchild", "grandchild")

        root = wagtail_models.Page.get_first_root_node()
        secondary_home = self.create_page(root, "Secondary home", "secondary-home")
        secondary_site = wagtail_models.Site.objects.create(
            hostname="secondary.test",
            port=80,
            root_page=secondary_home,
        )
        secondary_section = self.create_page(secondary_home, "Secondary section", "shared")

        self.assertTrue(urlsplit(primary_section.url).netloc)
        self.assertTrue(urlsplit(secondary_section.url).netloc)
        self.assertNotEqual(
            urlsplit(primary_section.url).netloc,
            urlsplit(secondary_section.url).netloc,
        )

        return primary_section, primary_child, primary_grandchild, secondary_section, secondary_site

    def create_navigation_menu(self, header_page, item_pages=None, include_link_to=True, title="Page menu"):
        raw_dropdowns = [
            {
                "type": "dropdown",
                "value": {
                    "header": self.page_link("Section", header_page, include_link_to),
                    "items": [
                        self.page_link(f"Item {index}", page, include_link_to)
                        for index, page in enumerate(item_pages or [], start=1)
                    ],
                },
            }
        ]
        dropdowns = nav_models.NavigationMenu.dropdowns.field.stream_block.to_python(raw_dropdowns)
        menu = nav_models.NavigationMenu.objects.create(
            title=title,
            locale=header_page.locale,
            dropdowns=dropdowns,
        )
        return nav_models.NavigationMenu.objects.get(pk=menu.pk)

    def create_horizontal_links(self, pages):
        raw_links = [
            {
                "type": "link",
                "value": self.page_link(f"Link {index}", page),
            }
            for index, page in enumerate(pages, start=1)
        ]
        links = nav_models.HorizontalLinkBlock.links.field.stream_block.to_python(raw_links)
        block = nav_models.HorizontalLinkBlock.objects.create(
            title="Page links",
            locale=pages[0].locale,
            links=links,
        )
        return nav_models.HorizontalLinkBlock.objects.get(pk=block.pk)

    def test_cms_navigation_renders_default_links_and_search_drawer(self):
        html = self.render_primary_navigation()

        self.assertIn('href="/meet-mozilla/"', html)
        self.assertIn('href="/what-we-do/imagine/"', html)
        self.assertIn('href="/join-us/"', html)
        self.assertIn('href="/nothing-personal/"', html)
        self.assertIn('id="primary-nav-panel"', html)
        self.assertIn('id="primary-nav-drawer"', html)
        self.assertEqual(html.count("data-primary-nav-search-toggle"), 2)
        self.assertIn('class="search-input-container"', html)
        self.assertIn('href="?form=donate-header"', html)

    def test_legacy_dropdowns_fall_back_to_links_and_flat_panels(self):
        html = self.render_primary_navigation()

        # A dropdown without items stays a plain link, in the bar and the drawer.
        self.assertInHTML('<a class="mzf-c-button mzf-c-button--nav" href="/join-us/">Join Us</a>', html)
        self.assertInHTML(
            '<a class="mzf-c-mega-menu__summary primary-nav-ns__drawer-link" href="/join-us/">Join Us</a>',
            html,
        )
        # A dropdown with items opens a panel holding its items as one unheaded
        # group, with the header link as the intro link.
        self.assertInHTML(
            """
            <button type="button" class="mzf-c-button mzf-c-button--nav" data-nav-panel="section-2"
                    aria-expanded="false" aria-controls="primary-nav-panel">What We Do</button>
            """,
            html,
        )
        self.assertInHTML(
            '<a class="mzf-c-mega-menu__link" href="/what-we-do/imagine/">Imagine</a>',
            html,
            count=2,
        )
        self.assertIn('<a class="mzf-c-link" href="/what-we-do/">What We Do<span class="mzf-c-link__icon"', html)
        self.assertNotIn('<h2 class="mzf-c-mega-menu__eyebrow"', html)
        self.assertNotIn('<section class="mzf-c-mega-menu__group"', html)
        self.assertEqual(html.count('<div class="mzf-c-mega-menu__group">'), 2)
        self.assertNotIn("mzf-c-mega-menu__groups--loose", html)
        self.assertEqual(html.count('data-nav-panel="'), 1)
        self.assertEqual(html.count("<details"), 1)

    def test_link_groups_render_intro_and_headed_groups(self):
        groups_page = self.create_page(self.homepage, "Our work", "our-work")
        program_page = self.create_page(groups_page, "Program", "program")
        raw_dropdowns = [
            {
                "type": "dropdown",
                "value": {
                    "header": self.page_link("Our Work", groups_page),
                    "items": [self.page_link("Legacy item", program_page)],
                    "intro_eyebrow": "What we do",
                    "intro_headline": "We fund people building better technology.",
                    "intro_cta": [self.page_link("Get the overview", groups_page)],
                    "group_spacing": "wide",
                    "groups": [
                        {
                            "heading": "Featured programs",
                            "links": [self.page_link("Program", program_page)],
                            "browse_all": [self.page_link("Browse all our work", groups_page)],
                        }
                    ],
                },
            }
        ]
        menu = nav_models.NavigationMenu.objects.create(
            title="Grouped menu",
            locale=self.homepage.locale,
            dropdowns=nav_models.NavigationMenu.dropdowns.field.stream_block.to_python(raw_dropdowns),
        )

        html = self.render_primary_navigation(
            urlsplit(program_page.url).path,
            menu=nav_models.NavigationMenu.objects.get(pk=menu.pk),
            page=program_page,
        )

        self.assertInHTML('<p class="mzf-c-mega-menu__eyebrow">What we do</p>', html, count=2)
        self.assertInHTML(
            '<p class="mzf-c-mega-menu__headline">We fund people building better technology.</p>',
            html,
            count=2,
        )
        self.assertInHTML('<h2 class="mzf-c-mega-menu__eyebrow">Featured programs</h2>', html, count=2)
        self.assertEqual(html.count('class="mzf-c-mega-menu__groups mzf-c-mega-menu__groups--loose"'), 2)
        self.assertIn(">Get the overview<", html)
        self.assertIn(">Browse all our work<", html)
        # Groups replace the legacy items rather than adding to them.
        self.assertNotIn("Legacy item", html)
        # The current program is marked in the desktop panel and the drawer, and
        # its section is marked active in both.
        self.assertInHTML(
            f'<a class="mzf-c-mega-menu__link" href="{program_page.localized.url}" aria-current="page">Program</a>',
            html,
            count=2,
        )
        self.assertEqual(html.count("data-nav-section-active"), 2)

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
        self.assertIn("data-primary-nav", html)

    def test_navigation_preview_uses_preview_menu_without_an_active_site_menu(self):
        preview_menu = nav_factories.generate(self.site)
        settings = nav_models.SiteNavigationMenu.for_site(self.site)
        settings.active_navigation_menu = None
        settings.save(update_fields=["active_navigation_menu"])
        request = self.request("/cms/preview/")
        context = preview_menu.get_preview_context(request, mode_name="")

        html = render_to_string("previews/navigation.html", context, request=request)

        self.assertIn('href="/meet-mozilla/"', html)
        self.assertIn("data-primary-nav", html)

    # Every link renders twice: once for the desktop bar or panel, once for the
    # phone drawer. Only one of the two is shown at a time.

    def test_localized_exact_top_level_link_is_current(self):
        html = self.render_primary_navigation("/de/join-us/")

        self.assertInHTML(
            '<a class="mzf-c-button mzf-c-button--nav" href="/join-us/" aria-current="page">Join Us</a>',
            html,
        )
        self.assertEqual(html.count('aria-current="page"'), 2)

    def test_exact_dropdown_child_is_current_and_activates_parent(self):
        html = self.render_primary_navigation("/de/what-we-do/imagine/")

        self.assertEqual(html.count("data-nav-section-active"), 2)
        self.assertInHTML(
            '<a class="mzf-c-mega-menu__link" href="/what-we-do/imagine/" aria-current="page">Imagine</a>',
            html,
            count=2,
        )
        self.assertEqual(html.count('aria-current="page"'), 2)

    def test_descendant_activates_section_without_claiming_current_page(self):
        html = self.render_primary_navigation("/de/what-we-do/imagine/article/")

        self.assertEqual(html.count("data-nav-section-active"), 2)
        self.assertInHTML(
            '<a class="mzf-c-mega-menu__link" href="/what-we-do/imagine/" aria-current="true">Imagine</a>',
            html,
            count=2,
        )
        self.assertNotIn('aria-current="page"', html)

    def test_same_site_pagechooser_is_active_in_multisite(self):
        primary_section, _child, _grandchild, _secondary_section, _secondary_site = self.create_multisite_pages()
        menu = self.create_navigation_menu(primary_section)

        html = self.render_primary_navigation(
            urlsplit(primary_section.url).path,
            menu=menu,
            page=primary_section,
            host="primary.test",
        )

        self.assertInHTML(
            f"""
            <a class="mzf-c-button mzf-c-button--nav" href="{primary_section.localized.url}"
               aria-current="page">Section</a>
            """,
            html,
        )
        self.assertEqual(html.count("aria-current="), 2)
        self.assertEqual(html.count('aria-current="page"'), 2)

    def test_pagechooser_selects_most_specific_child(self):
        primary_section, primary_child, primary_grandchild, _secondary_section, _site = self.create_multisite_pages()
        menu = self.create_navigation_menu(primary_section, [primary_child])

        descendant_html = self.render_primary_navigation(
            urlsplit(primary_grandchild.url).path,
            menu=menu,
            page=primary_grandchild,
            host="primary.test",
        )

        self.assertInHTML(
            f"""
            <a class="mzf-c-mega-menu__link" href="{primary_child.localized.url}"
               aria-current="true">Item 1</a>
            """,
            descendant_html,
            count=2,
        )
        self.assertEqual(descendant_html.count("data-nav-section-active"), 2)
        self.assertEqual(descendant_html.count("aria-current="), 2)
        self.assertNotIn('aria-current="page"', descendant_html)

        exact_html = self.render_primary_navigation(
            urlsplit(primary_child.url).path,
            menu=menu,
            page=primary_child,
            host="primary.test",
        )
        self.assertEqual(exact_html.count('aria-current="page"'), 2)

    def test_cross_site_pagechooser_with_same_path_is_not_active(self):
        primary_section, _child, _grandchild, secondary_section, _secondary_site = self.create_multisite_pages()
        menu = self.create_navigation_menu(secondary_section)

        html = self.render_primary_navigation(
            urlsplit(primary_section.url).path,
            menu=menu,
            page=primary_section,
            host="primary.test",
        )

        self.assertIn(f'href="{secondary_section.localized.url}"', html)
        self.assertNotIn("data-nav-section-active", html)
        self.assertNotIn("aria-current", html)

    def test_horizontal_pagechooser_is_active_and_prefers_child(self):
        primary_section, primary_child, primary_grandchild, _secondary_section, _site = self.create_multisite_pages()
        block = self.create_horizontal_links([primary_section, primary_child])

        exact_html = render_to_string(
            "patterns/components/navigation/_horizontal_link_block.html",
            {"block": block, "page": primary_child},
            request=self.request(urlsplit(primary_child.url).path, host="primary.test"),
        )

        self.assertInHTML(
            f"""
            <a class="horizontal-link-block__link horizontal-link-block__link--active"
               href="{primary_child.localized.url}"
               aria-current="true"><span class="horizontal-link-block__label">Link 2</span></a>
            """,
            exact_html,
        )
        self.assertEqual(exact_html.count("horizontal-link-block__link--active"), 1)

        descendant_html = render_to_string(
            "patterns/components/navigation/_horizontal_link_block.html",
            {"block": block, "page": primary_grandchild},
            request=self.request(urlsplit(primary_grandchild.url).path, host="primary.test"),
        )
        self.assertIn(primary_child.localized.url, descendant_html)
        self.assertEqual(descendant_html.count("horizontal-link-block__link--active"), 1)

    def test_horizontal_cross_site_pagechooser_is_not_active(self):
        primary_section, _child, _grandchild, secondary_section, _secondary_site = self.create_multisite_pages()
        block = self.create_horizontal_links([secondary_section])

        html = render_to_string(
            "patterns/components/navigation/_horizontal_link_block.html",
            {"block": block, "page": primary_section},
            request=self.request(urlsplit(primary_section.url).path, host="primary.test"),
        )

        self.assertIn(secondary_section.localized.url, html)
        self.assertNotIn("horizontal-link-block__link--active", html)
        self.assertNotIn("aria-current", html)

    def test_translated_pagechooser_without_link_to_is_active(self):
        primary_section, _child, _grandchild, _secondary_section, _secondary_site = self.create_multisite_pages()
        menu = self.create_navigation_menu(primary_section, title="English menu")
        french_section = primary_section.copy_for_translation(self.fr_locale, copy_parents=True)

        translated_menu = menu.copy_for_translation(self.fr_locale)
        translated_menu.title = "French menu"
        translated_dropdowns = [
            {
                "type": "dropdown",
                "value": {
                    "header": {
                        "label": "Section française",
                        "page": french_section.pk,
                        "external_url": "",
                        "relative_url": "",
                    },
                    "items": [],
                },
            }
        ]
        translated_menu.dropdowns = nav_models.NavigationMenu.dropdowns.field.stream_block.to_python(
            translated_dropdowns
        )
        translated_menu.save()

        with translation.override("fr"):
            html = self.render_primary_navigation(
                urlsplit(french_section.url).path,
                menu=menu,
                page=french_section,
                host="primary.test",
            )

        self.assertIn("Section française", html)
        self.assertNotIn(">Section<", html)
        self.assertEqual(html.count('aria-current="page"'), 2)
