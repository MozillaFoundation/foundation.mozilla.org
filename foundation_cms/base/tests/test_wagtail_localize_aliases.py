"""
Tests for locale fallback ("alias") creation for copied pages.

See wagtail_localize_aliases.py
"""

from unittest import mock

from django.core.management import call_command
from django.urls import reverse
from wagtail import hooks
from wagtail.models import Locale, Page, Site
from wagtail.test.utils import WagtailPageTestCase
from wagtail_localize import synctree
from wagtail_localize.models import LocaleSynchronization

from foundation_cms.base.wagtail_hooks import (
    wagtail_localize_create_aliases_for_copied_page,
    wagtail_localize_handles_copy,
)
from foundation_cms.base.wagtail_localize_aliases import create_aliases_for_page
from foundation_cms.core.models import GeneralPage, HomePage


def fake_upstream_hook(request, page, new_page):
    """Stands in for wagtail-localize closing this gap in a future release."""


fake_upstream_hook.__module__ = "wagtail_localize.synctree"


class LocaleFallbackTestCase(WagtailPageTestCase):
    """Redesign homepage as site root. fr syncs from the default locale; de does not."""

    @classmethod
    def setUpTestData(cls):
        cls.default_locale = Locale.get_default()
        cls.fr_locale, _ = Locale.objects.get_or_create(language_code="fr")
        cls.de_locale, _ = Locale.objects.get_or_create(language_code="de")

        cls.homepage = Page.get_first_root_node().add_child(
            instance=HomePage(
                title="Home",
                slug="locale-fallback-home",
                seo_title="Home",
                search_description="Homepage for locale fallback tests.",
            )
        )
        cls.site = Site.objects.get(is_default_site=True)
        cls.site.root_page = cls.homepage
        cls.site.save()

        LocaleSynchronization.objects.create(locale=cls.fr_locale, sync_from=cls.default_locale)

    def add_page(self, parent, title, slug=None):
        return parent.add_child(
            instance=GeneralPage(
                title=title,
                slug=slug or title.lower().replace(" ", "-"),
                seo_title=title,
                search_description=f"Description for {title}",
                show_hero=False,
            )
        )

    def fallback_for(self, page, locale):
        return page.get_translations().filter(locale=locale, alias_of__isnull=False).first()


class CreateAliasesForPageTests(LocaleFallbackTestCase):
    def test_creates_a_fallback_only_in_locales_that_sync(self):
        page = self.add_page(self.homepage, "Synced page")

        create_aliases_for_page(page)

        self.assertEqual(
            set(page.get_translations().values_list("locale__language_code", flat=True)),
            {"fr"},
        )

    def test_skips_locales_that_already_have_a_page(self):
        """Safe to re-run, and an editor's real translation is never clobbered."""
        aliased = self.add_page(self.homepage, "Run twice")
        create_aliases_for_page(aliased)

        translated = self.add_page(self.homepage, "Already translated")
        translated.copy_for_translation(self.fr_locale, copy_parents=True).save_revision().publish()

        self.assertEqual(create_aliases_for_page(aliased), [])
        self.assertEqual(create_aliases_for_page(translated), [])
        self.assertIsNone(translated.get_translations().get(locale=self.fr_locale).alias_of_id)

    def test_an_alias_is_not_itself_given_fallbacks(self):
        """A same-locale alias gets a fresh translation_key, so only the guard stops a fanout."""
        page = self.add_page(self.homepage, "Source page")
        same_locale_alias = page.create_alias(parent=self.homepage, update_slug="source-page-alias")

        self.assertEqual(create_aliases_for_page(same_locale_alias), [])
        self.assertFalse(same_locale_alias.get_translations().exists())

    def test_creates_the_parent_chain_in_the_target_locale(self):
        """Without copy_parents an untranslated parent is the common case, not an edge case."""
        section = self.add_page(self.homepage, "Untranslated section")
        child = self.add_page(section, "Child of untranslated section")

        create_aliases_for_page(child)

        child_fallback = self.fallback_for(child, self.fr_locale)
        self.assertIsNotNone(child_fallback)
        self.assertEqual(child_fallback.get_parent().translation_key, section.translation_key)

    def test_one_failing_locale_is_logged_and_does_not_stop_the_others(self):
        page = self.add_page(self.homepage, "Partially doomed page")
        LocaleSynchronization.objects.create(locale=self.de_locale, sync_from=self.default_locale)
        real_copy_for_translation = GeneralPage.copy_for_translation
        fr_locale = self.fr_locale

        def fail_for_french(page, locale, *args, **kwargs):
            if locale == fr_locale:
                raise ValueError("boom")
            return real_copy_for_translation(page, locale, *args, **kwargs)

        with mock.patch.object(GeneralPage, "copy_for_translation", fail_for_french):
            with self.assertLogs("foundation_cms.base.wagtail_localize_aliases", level="ERROR") as logs:
                create_aliases_for_page(page)

        self.assertIn("Could not create a fr locale fallback", "\n".join(logs.output))
        self.assertIsNone(self.fallback_for(page, self.fr_locale))
        self.assertIsNotNone(self.fallback_for(page, self.de_locale))


class CopiedPageLocaleFallbackTests(LocaleFallbackTestCase):
    """Regression tests for TP1-3320, driven through the real admin copy view."""

    def setUp(self):
        super().setUp()
        self.login()

    def copy_page(self, page, new_title, new_slug, copy_subpages=False):
        response = self.client.post(
            reverse("wagtailadmin_pages:copy", args=[page.id]),
            {
                "new_title": new_title,
                "new_slug": new_slug,
                "new_parent_page": str(page.get_parent().id),
                "publish_copies": "on",
                **({"copy_subpages": "on"} if copy_subpages else {}),
            },
        )
        self.assertEqual(response.status_code, 302, "the copy itself failed")
        return Page.objects.get(slug=new_slug, locale=self.default_locale)

    def test_copying_a_page_creates_fallbacks_of_its_own(self):
        source = self.add_page(self.homepage, "Original")
        create_aliases_for_page(source)

        clone = self.copy_page(source, "Clone", "clone")

        fallback = self.fallback_for(clone, self.fr_locale)
        self.assertIsNotNone(fallback)
        self.assertEqual(fallback.alias_of_id, clone.id)
        self.assertNotEqual(fallback.translation_key, source.translation_key)

    def test_subtree_descendants_are_left_to_the_cron(self):
        """A deliberate boundary, and the cron is the other half of it. See wagtail_localize_aliases."""
        source = self.add_page(self.homepage, "Section to clone")
        self.add_page(source, "Child to clone")

        clone = self.copy_page(source, "Cloned section", "cloned-section", copy_subpages=True)
        cloned_child = clone.get_children().first()

        self.assertIsNotNone(self.fallback_for(clone, self.fr_locale))
        self.assertIsNone(self.fallback_for(cloned_child, self.fr_locale))

        call_command("sync_locale_trees")

        self.assertIsNotNone(self.fallback_for(cloned_child, self.fr_locale))


class UpstreamOverlapTests(LocaleFallbackTestCase):
    """Guards for the day wagtail-localize closes this gap and both modules can go."""

    def test_wagtail_localize_still_does_not_handle_copy(self):
        self.assertNotIn(
            "wagtail_localize.synctree",
            {hook.__module__ for hook in hooks.get_hooks("after_copy_page")},
            "wagtail-localize now registers after_copy_page itself -- delete "
            "foundation_cms/base/wagtail_localize_aliases.py and wagtail_hooks.py.",
        )

    def test_our_hook_stands_down_when_upstream_takes_over(self):
        page = self.add_page(self.homepage, "Upstream job now")
        self.assertFalse(wagtail_localize_handles_copy())

        with hooks.register_temporarily("after_copy_page", fake_upstream_hook):
            self.assertTrue(wagtail_localize_handles_copy())
            wagtail_localize_create_aliases_for_copied_page(None, page, page)

        self.assertIsNone(self.fallback_for(page, self.fr_locale))

    def test_running_after_upstream_is_a_no_op(self):
        """If upstream fixes this without a hook the guard is blind, so idempotency carries it."""
        page = self.add_page(self.homepage, "Already handled upstream")
        synctree.create_aliases_for_new_page(page)

        self.assertEqual(create_aliases_for_page(page), [])
        self.assertEqual(page.get_translations().filter(locale=self.fr_locale).count(), 1)
