from io import StringIO
from tempfile import TemporaryDirectory

from django.core.management import call_command
from django.core.management.base import CommandError
from wagtail.models import Page, Site

from foundation_cms.core.factories.homepage import HomePageFactory
from foundation_cms.core.factories.visual_regression import generate
from foundation_cms.core.models import GeneralPage
from foundation_cms.legacy_apps.wagtailpages.factory.homepage import (
    WagtailHomepageFactory,
)
from foundation_cms.legacy_apps.wagtailpages.tests import base as test_base


class VisualRegressionFactoryTests(test_base.WagtailpagesTestCase):
    @classmethod
    def _setup_homepage(cls):
        root = Page.get_first_root_node()
        cls.homepage = HomePageFactory(parent=root)
        cls.site = Site.objects.get(is_default_site=True)
        cls.site.root_page = cls.homepage
        cls.site.save()

    def test_fixtures_have_real_page_shell_and_deterministic_body(self):
        empty, populated = generate(parent=self.homepage)

        for page in (empty, populated):
            self.assertTrue(page.live)
            self.assertFalse(page.show_hero)
            self.assertEqual(page.get_parent().pk, self.homepage.pk)
            self.assertEqual(page.locale, self.homepage.locale)
            page.body.stream_block.clean(page.body)
        self.assertEqual(len(empty.body), 0)
        self.assertEqual(
            [block.block_type for block in populated.body],
            ["section_start", "rich_text", "link_button_block", "link_button_block", "accordion_block"],
        )

    def test_repeat_run_preserves_existing_content_and_revisions(self):
        empty, populated = generate(parent=self.homepage)
        empty.title = "Edited locally"
        empty.save_revision().publish()
        revision_count = empty.revisions.count()
        populated.refresh_from_db()
        populated_body = list(populated.body.raw_data)

        repeated_empty, repeated_populated = generate(parent=self.homepage)

        self.assertEqual(repeated_empty.pk, empty.pk)
        self.assertEqual(repeated_empty.title, "Edited locally")
        self.assertEqual(repeated_empty.revisions.count(), revision_count)
        self.assertEqual(repeated_populated.pk, populated.pk)
        self.assertEqual(list(repeated_populated.body.raw_data), populated_body)

    def test_does_not_reuse_same_slug_under_another_parent(self):
        section = self.homepage.add_child(
            instance=GeneralPage(
                title="Section", slug="fixture-section", seo_title="Section", search_description="Fixture section"
            )
        )
        other_pages = generate(parent=section)
        pages = generate(parent=self.homepage)

        self.assertTrue({page.pk for page in other_pages}.isdisjoint({page.pk for page in pages}))

    def make_unpublished_fixture(self):
        page = self.homepage.add_child(
            instance=GeneralPage(
                title="Edited unpublished fixture",
                slug="visual-regression-components",
                seo_title="Edited draft",
                search_description="Content to preserve",
                show_hero=False,
                live=False,
            )
        )
        page.body = [("rich_text", "<p>Keep this edited draft.</p>")]
        page.save_revision()
        page.refresh_from_db()
        return page

    def test_unpublished_fixture_preserves_draft_and_rolls_back_new_page(self):
        page = self.make_unpublished_fixture()
        body = list(page.body.raw_data)
        revision_content = page.get_latest_revision().content
        revision_ids = list(page.revisions.values_list("pk", flat=True))
        page_count = Page.objects.count()

        with self.assertRaisesRegex(ValueError, "visual-regression-components is unpublished"):
            generate(parent=self.homepage)

        page.refresh_from_db()
        self.assertFalse(page.live)
        self.assertEqual(page.title, "Edited unpublished fixture")
        self.assertEqual(list(page.body.raw_data), body)
        self.assertEqual(page.get_latest_revision().content, revision_content)
        self.assertEqual(list(page.revisions.values_list("pk", flat=True)), revision_ids)
        self.assertEqual(Page.objects.count(), page_count)
        self.assertFalse(self.homepage.get_children().filter(slug="visual-regression-empty").exists())

    def test_conflicting_page_type_is_preserved_and_rolls_back_new_page(self):
        conflict = self.homepage.add_child(instance=Page(title="Other page", slug="visual-regression-components"))
        page_count = Page.objects.count()

        with self.assertRaisesRegex(ValueError, "Refusing to reuse a non-GeneralPage at visual-regression-components"):
            generate(parent=self.homepage)

        conflict.refresh_from_db()
        self.assertEqual(conflict.title, "Other page")
        self.assertEqual(Page.objects.count(), page_count)
        self.assertFalse(self.homepage.get_children().filter(slug="visual-regression-empty").exists())

    def test_command_requires_default_site(self):
        self.site.is_default_site = False
        self.site.save()
        page_count = Page.objects.count()

        with self.assertRaisesRegex(CommandError, "default site must already have a redesign HomePage"):
            call_command("load_visual_regression_data", stdout=StringIO())

        self.assertEqual(Page.objects.count(), page_count)

    def test_command_rejects_legacy_homepage(self):
        with TemporaryDirectory() as media_root, self.settings(MEDIA_ROOT=media_root):
            legacy_homepage = WagtailHomepageFactory(parent=Page.get_first_root_node())
        self.site.root_page = legacy_homepage
        self.site.save()
        page_count = Page.objects.count()

        with self.assertRaisesRegex(CommandError, "default site must already have a redesign HomePage"):
            call_command("load_visual_regression_data", stdout=StringIO())

        self.assertEqual(Page.objects.count(), page_count)

    def test_command_creates_live_fixtures_under_redesign_homepage(self):
        output = StringIO()
        call_command("load_visual_regression_data", stdout=output)

        pages = GeneralPage.objects.child_of(self.homepage).filter(slug__startswith="visual-regression-")
        self.assertEqual(pages.count(), 2)
        self.assertTrue(all(page.live for page in pages))
        self.assertIn("Visual fixture ready: visual-regression-empty", output.getvalue())
        self.assertIn("Visual fixture ready: visual-regression-components", output.getvalue())

    def test_command_reports_unpublished_fixture_without_success_output(self):
        page = self.make_unpublished_fixture()
        revision_ids = list(page.revisions.values_list("pk", flat=True))
        output = StringIO()

        with self.assertRaisesRegex(CommandError, "visual-regression-components is unpublished. Review and publish"):
            call_command("load_visual_regression_data", stdout=output)

        page.refresh_from_db()
        self.assertFalse(page.live)
        self.assertEqual(list(page.revisions.values_list("pk", flat=True)), revision_ids)
        self.assertFalse(self.homepage.get_children().filter(slug="visual-regression-empty").exists())
        self.assertEqual(output.getvalue(), "")
