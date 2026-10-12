from foundation_cms.core.factories.visual_regression import generate
from foundation_cms.core.models import GeneralPage
from foundation_cms.legacy_apps.wagtailpages.tests import base as test_base


class VisualRegressionFactoryTests(test_base.WagtailpagesTestCase):
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
