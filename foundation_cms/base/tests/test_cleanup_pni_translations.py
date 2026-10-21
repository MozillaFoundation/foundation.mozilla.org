"""
Tests for the cleanup_pni_translations management command.

The PNI models were dropped by wagtailpages migration 0178, so their orphaned rows cannot be
built from real content. Instead each test builds a genuine translation source from a live page
and then repoints its specific_content_type at a stale PNI content type, which is the exact
shape migration 0178 left behind.
"""

from unittest import mock

from django.contrib.contenttypes.models import ContentType
from django.core.management import call_command
from django.core.management.base import CommandError
from wagtail.models import Locale, Page, Site
from wagtail.test.utils import WagtailPageTestCase
from wagtail_localize.models import (
    StringSegment,
    StringTranslation,
    TranslatableObject,
    Translation,
    TranslationContext,
    TranslationSource,
)
from wagtail_localize_git.models import Resource, SyncLog

from foundation_cms.core.models import GeneralPage, HomePage

COMMAND = "cleanup_pni_translations"


class CleanupPNITranslationsTestCase(WagtailPageTestCase):
    @classmethod
    def setUpTestData(cls):
        cls.default_locale = Locale.get_default()
        cls.fr_locale, _ = Locale.objects.get_or_create(language_code="fr")

        cls.homepage = Page.get_first_root_node().add_child(
            instance=HomePage(
                title="Home",
                slug="pni-cleanup-home",
                seo_title="Home",
                search_description="Homepage for PNI cleanup tests.",
            )
        )
        site = Site.objects.get(is_default_site=True)
        site.root_page = cls.homepage
        site.save()

        cls.pni_content_type = ContentType.objects.get_or_create(app_label="wagtailpages", model="buyersguidepage")[0]

    def setUp(self):
        super().setUp()
        self.pni_source = self.make_source("Creepy Doorbell", "pages/homepage/privacynotincluded/doorbell")
        TranslationSource.objects.filter(pk=self.pni_source.pk).update(specific_content_type=self.pni_content_type)
        self.survivor_source = self.make_source("Keep Me", "pages/homepage/keep-me")

    def make_source(self, title, resource_path):
        page = self.homepage.add_child(
            instance=GeneralPage(
                title=title,
                slug=title.lower().replace(" ", "-"),
                seo_title=title,
                search_description=title,
            )
        )
        source, _ = TranslationSource.get_or_create_from_instance(page)
        translation = Translation.objects.create(source=source, target_locale=self.fr_locale)
        segment = source.stringsegment_set.first()
        StringTranslation.objects.create(
            translation_of=segment.string,
            locale=self.fr_locale,
            context=segment.context,
            data="traduit",
        )
        Resource.objects.create(object=source.object, path=resource_path)
        self.assertTrue(translation.enabled)
        return source

    def assertSurvivorIntact(self):
        self.assertTrue(TranslationSource.objects.filter(pk=self.survivor_source.pk).exists())
        self.assertEqual(Translation.objects.filter(source=self.survivor_source, enabled=True).count(), 1)
        self.assertTrue(StringSegment.objects.filter(source=self.survivor_source).exists())
        self.assertTrue(Resource.objects.filter(object=self.survivor_source.object).exists())

    def test_deletes_orphaned_pni_data(self):
        pni_key = self.pni_source.object_id

        call_command(COMMAND, "--execute")

        self.assertFalse(TranslationSource.objects.filter(pk=self.pni_source.pk).exists())
        self.assertFalse(TranslatableObject.objects.filter(translation_key=pni_key).exists())
        self.assertFalse(Translation.objects.filter(source__object_id=pni_key).exists())
        self.assertFalse(StringSegment.objects.filter(context__object_id=pni_key).exists())
        self.assertFalse(TranslationContext.objects.filter(object_id=pni_key).exists())
        self.assertFalse(StringTranslation.objects.filter(context__object__translation_key=pni_key).exists())
        self.assertFalse(Resource.objects.filter(object_id=pni_key).exists())
        self.assertSurvivorIntact()

    def test_dry_run_leaves_everything_in_place(self):
        call_command(COMMAND)

        self.assertTrue(TranslationSource.objects.filter(pk=self.pni_source.pk).exists())
        self.assertEqual(Translation.objects.filter(source=self.pni_source, enabled=True).count(), 1)
        self.assertTrue(StringSegment.objects.filter(source=self.pni_source).exists())
        self.assertSurvivorIntact()

    def test_disable_only_stops_the_sync_without_deleting(self):
        call_command(COMMAND, "--disable-only", "--execute")

        self.assertTrue(TranslationSource.objects.filter(pk=self.pni_source.pk).exists())
        self.assertEqual(Translation.objects.filter(source=self.pni_source, enabled=True).count(), 0)
        self.assertSurvivorIntact()

    def test_disabled_translations_are_dropped_from_the_pontoon_push(self):
        """The git sync only exports enabled translations, so disabling is what clears fomo-content."""
        pushed = Translation.objects.filter(
            source__locale=self.default_locale,
            target_locale=self.fr_locale,
            enabled=True,
        )
        self.assertIn(self.pni_source.object_id, set(pushed.values_list("source__object_id", flat=True)))

        call_command(COMMAND, "--disable-only", "--execute")

        self.assertNotIn(self.pni_source.object_id, set(pushed.values_list("source__object_id", flat=True)))
        self.assertIn(self.survivor_source.object_id, set(pushed.values_list("source__object_id", flat=True)))

    def test_refuses_to_run_against_an_installed_model(self):
        with mock.patch(
            "foundation_cms.base.management.commands.cleanup_pni_translations.PNI_MODELS",
            ["blogpage"],
        ):
            with self.assertRaisesMessage(CommandError, "still resolve to installed models"):
                call_command(COMMAND, "--execute")

        self.assertSurvivorIntact()

    def test_is_a_noop_when_there_is_nothing_to_clean(self):
        call_command(COMMAND, "--execute")
        call_command(COMMAND, "--execute")

        self.assertSurvivorIntact()

    def test_cascades_remove_the_git_sync_bookkeeping(self):
        log = SyncLog.objects.create(action=SyncLog.ACTION_PUSH, commit_id="abc123")
        log.add_translation(Translation.objects.get(source=self.pni_source))
        log.add_translation(Translation.objects.get(source=self.survivor_source))

        call_command(COMMAND, "--execute")

        self.assertFalse(log.resources.filter(resource__object_id=self.pni_source.object_id).exists())
        self.assertTrue(log.resources.filter(resource__object_id=self.survivor_source.object_id).exists())
