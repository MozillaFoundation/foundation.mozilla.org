from foundation_cms.core.factories.careers import CAREERS_SLUG, generate
from foundation_cms.core.models import GeneralPage
from foundation_cms.legacy_apps.wagtailpages.tests import base as test_base


class CareersFactoryTests(test_base.WagtailpagesTestCase):
    def unrelated_careers_page(self):
        """A page with the same slug, living somewhere else in the tree."""
        section = self.homepage.add_child(
            instance=GeneralPage(
                title="Section",
                slug="section",
                seo_title="Section",
                search_description="Section",
                show_hero=False,
            )
        )
        return section.add_child(
            instance=GeneralPage(
                title="Someone else's careers",
                slug=CAREERS_SLUG,
                seo_title="Someone else's careers",
                search_description="Not ours",
                show_hero=False,
            )
        )

    def test_generates_a_published_careers_page_under_the_given_parent(self):
        page = generate(parent=self.homepage)

        self.assertTrue(page.live)
        self.assertEqual(page.slug, CAREERS_SLUG)
        self.assertEqual(page.get_parent().pk, self.homepage.pk)

    def test_the_page_carries_the_greenhouse_board_block(self):
        page = generate(parent=self.homepage)

        self.assertIn("greenhouse_board", [block.block_type for block in page.body])

    def test_generating_twice_reuses_the_same_page(self):
        first = generate(parent=self.homepage)
        second = generate(parent=self.homepage)

        self.assertEqual(first.pk, second.pk)
        self.assertEqual(GeneralPage.objects.child_of(self.homepage).filter(slug=CAREERS_SLUG).count(), 1)

    def test_a_same_slug_page_under_another_parent_is_left_alone(self):
        unrelated = self.unrelated_careers_page()

        page = generate(parent=self.homepage)

        self.assertNotEqual(page.pk, unrelated.pk)
        unrelated.refresh_from_db()
        self.assertEqual(unrelated.title, "Someone else's careers")
        self.assertEqual(len(unrelated.body), 0)

    def test_repeated_generation_leaves_a_same_slug_page_under_another_parent_alone(self):
        unrelated = self.unrelated_careers_page()

        generate(parent=self.homepage)
        generate(parent=self.homepage)

        self.assertTrue(GeneralPage.objects.filter(pk=unrelated.pk).exists())
        self.assertEqual(GeneralPage.objects.filter(slug=CAREERS_SLUG).count(), 2)
