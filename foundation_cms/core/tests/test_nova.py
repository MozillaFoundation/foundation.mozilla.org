from django.template.loader import render_to_string, select_template
from django.test import RequestFactory, override_settings
from django.urls import reverse
from wagtail.models import Locale

from foundation_cms.blocks.quote_block import QuoteBlock
from foundation_cms.core.factories.nova_demo import demo_body, generate
from foundation_cms.core.models import GeneralPage
from foundation_cms.footer.models import FooterInternalLink, SiteFooter
from foundation_cms.legacy_apps.wagtailpages.tests.base import WagtailpagesTestCase
from foundation_cms.navigation.models import NavigationMenu


@override_settings(
    STORAGES={
        "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
        "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"},
    }
)
class NovaThemeTests(WagtailpagesTestCase):
    def setUp(self):
        super().setUp()
        self.root, self.default, self.nova, self.inherited, self.overridden = generate()

    def render(self, page):
        request = RequestFactory().get(page.url)
        return render_to_string(page.get_template(request), page.get_context(request), request=request)

    def test_same_stored_content_has_different_structure_and_isolated_assets(self):
        def content(value):
            if isinstance(value, dict):
                return {key: content(item) for key, item in value.items() if key != "id"}
            if isinstance(value, list):
                return [content(item) for item in value]
            return value

        self.assertEqual(content(self.default.body.get_prep_value()), content(self.nova.body.get_prep_value()))
        default = self.render(self.default)
        nova = self.render(self.nova)
        self.assertIn('<div class="general-page">', default)
        self.assertIn('<article class="nova-page">', nova)
        self.assertNotIn("nova.compiled", default)
        self.assertIn("nova.compiled.css", nova)
        self.assertIn("nova.compiled.js", nova)
        self.assertEqual(nova.count('class="nova-quote"'), 2)
        self.assertIn('class="two-column-container ', nova)
        self.assertIn("Two-column container: default fallback", nova)
        for component in ("nova-nav", "nova-breadcrumbs", "nova-footer"):
            self.assertIn(component, nova)
            self.assertNotIn(component, default)
        self.assertNotIn('class="primary-nav-ns"', nova)
        self.assertNotIn('class="site-footer-ns"', nova)

    def test_inheritance_and_explicit_default_override(self):
        self.assertEqual(self.inherited.get_theme(), "nova")
        self.assertEqual(self.overridden.get_theme(), "default")
        self.assertIn("nova.compiled.js", self.render(self.inherited))
        self.assertNotIn("nova.compiled", self.render(self.overridden))
        for component in ("nova-nav", "nova-breadcrumbs", "nova-footer"):
            self.assertIn(component, self.render(self.inherited))
            self.assertNotIn(component, self.render(self.overridden))

    def test_nova_replaces_default_assets_for_explicit_and_inherited_themes(self):
        nova_assets = ("nova.compiled.css", "nova.compiled.js")
        default_assets = ("redesign_fallback.compiled.css", "redesign_main.compiled.js")
        for page in (self.nova, self.inherited):
            with self.subTest(page=page.slug):
                html = self.render(page)
                for asset in nova_assets:
                    self.assertEqual(html.count(asset), 1)
                for asset in default_assets:
                    self.assertNotIn(asset, html)
                self.assertIn("civic_cookie_control/init.compiled.js", html)
                self.assertNotIn("newsletter-signup__form", html)
                self.assertNotIn('id="language-switcher-form"', html)
        for page in (self.default, self.overridden):
            with self.subTest(page=page.slug):
                html = self.render(page)
                for asset in default_assets:
                    self.assertEqual(html.count(asset), 1)
                for asset in nova_assets:
                    self.assertNotIn(asset, html)

    def test_unknown_theme_falls_back_for_page_base_and_blocks(self):
        page = GeneralPage.objects.get(pk=self.default.pk)
        page.theme = "missing-theme"
        self.assertEqual(select_template(page.get_template(None)).template.name, page.template)
        html = self.render(page)
        self.assertIn('<div class="quote-block">', html)
        self.assertNotIn("nova.compiled", html)

    def test_preview_uses_the_same_template_resolution(self):
        self.assertEqual(self.nova.get_preview_template(None, ""), self.nova.get_template(None))

    def test_page_theme_takes_precedence_over_block_context(self):
        block = QuoteBlock()
        value = block.to_python(demo_body()[1]["value"])
        html = block.render(value, context={"page": self.nova, "theme": "default"})
        self.assertIn('class="nova-quote"', html)

    def test_demo_is_repeatable_without_updating_existing_pages(self):
        revisions = [page.latest_revision_id for page in generate()]
        self.assertEqual(
            [page.pk for page in generate()],
            [self.root.pk, self.default.pk, self.nova.pk, self.inherited.pk, self.overridden.pk],
        )
        self.assertEqual([page.latest_revision_id for page in generate()], revisions)

    def render_component(self, name, page=None, **context):
        page = page or self.nova
        request = RequestFactory().get(page.url)
        request.site = self.site
        return render_to_string(
            f"patterns/components/nova/{name}.html",
            {"page": page, **context},
            request=request,
        )

    def test_navigation_uses_shared_menu_and_exact_current_link(self):
        def link(page):
            return {"label": page.slug, "link_to": "page", "page": page.pk}

        menu = NavigationMenu.objects.create(
            title="Shared menu",
            locale=self.nova.locale,
            dropdowns=NavigationMenu.dropdowns.field.stream_block.to_python(
                [{"type": "dropdown", "value": {"header": link(self.nova), "items": [link(self.inherited)]}}]
            ),
        )
        html = self.render_component("navigation", menu=menu)
        self.assertEqual(html.count('aria-current="page"'), 1)
        self.assertIn(f'href="{self.nova.url}"', html)
        self.assertNotIn("primary-nav-ns", html)
        self.assertNotIn(f'href="{self.inherited.url}"', html)
        self.assertIn(f'href="{reverse("search")}"', html)
        inherited = self.render_component("navigation", page=self.inherited, menu=menu)
        self.assertNotIn('aria-current="page"', inherited)

    def test_breadcrumbs_reuse_the_full_localized_hierarchy(self):
        html = self.render_component("breadcrumbs", page=self.inherited)
        self.assertIn(f'href="{self.root.url}"', html)
        self.assertIn(f'href="{self.nova.url}"', html)
        self.assertEqual(html.count('aria-current="page"'), 1)
        self.assertNotIn(f'href="{self.inherited.url}"', html)
        self.assertNotIn("nova-breadcrumbs", self.render_component("breadcrumbs", page=self.homepage))

    def test_footer_shared_settings_localization_and_static_fallback(self):
        footer = SiteFooter.objects.create(title="Shared footer", legal_text="Shared legal", locale=self.nova.locale)
        FooterInternalLink.objects.create(footer=footer, label="Shared link", url="/shared/")
        html = self.render_component("footer", footer=footer, EDITABLE_FOOTER=True)
        self.assertIn("Shared legal", html)
        self.assertIn('href="/shared/"', html)
        self.assertLess(html.index("Shared legal"), html.index('class="nova-footer__wordmark"'))
        french, _ = Locale.objects.get_or_create(language_code="fr")
        translated = footer.copy_for_translation(french)
        translated.legal_text = "Mentions légales"
        translated.save()
        self.nova.locale = french
        html = self.render_component("footer", footer=footer, EDITABLE_FOOTER=True)
        self.assertIn("Mentions légales", html)
        for context in ({"footer": footer, "EDITABLE_FOOTER": False}, {"EDITABLE_FOOTER": True}):
            html = self.render_component("footer", **context)
            self.assertIn('<footer class="nova-footer">', html)
            self.assertNotIn('<footer class="site-footer-ns">', html)
            self.assertIn("/meet-mozilla/website-licensing/", html)
            self.assertNotIn("Shared legal", html)
