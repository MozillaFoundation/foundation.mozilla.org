from unittest.mock import patch

from wagtail.test.utils import WagtailPageTestCase

from foundation_cms.base.utils.helpers import get_faker
from foundation_cms.core.factories import HomePageFactory
from foundation_cms.nothing_personal.models import (
    NothingPersonalArticlePage,
    NothingPersonalHomePage,
)
from foundation_cms.nothing_personal.models.home_page import NothingPersonalFeaturedItem
from foundation_cms.profiles.factories import (
    CURATED_ARTICLE_EXPERT_SLUG,
    ExpertHubPageFactory,
    ExpertProfilePageFactory,
    ensure_expert_curated_articles,
)


class EnsureExpertCuratedArticlesTests(WagtailPageTestCase):
    def setUp(self):
        self.root = HomePageFactory()
        self.hub = ExpertHubPageFactory(parent=self.root)
        self.expert = ExpertProfilePageFactory(
            parent=self.hub,
            slug=CURATED_ARTICLE_EXPERT_SLUG,
        )
        self.fake = get_faker()

    def test_seeds_homepage_content_and_is_idempotent(self):
        self._ensure_curated_articles()

        home = NothingPersonalHomePage.objects.get(slug="nothing-personal")
        articles = list(NothingPersonalArticlePage.objects.order_by("slug"))
        selected_articles = list(self.expert.selected_articles.order_by("sort_order", "pk"))
        featured_items = list(home.featured_items.order_by("sort_order", "pk"))

        self.assertEqual(len(articles), 5)
        self.assertEqual(home.hero_item_id, articles[0].pk)
        self.assertEqual(
            [item.page_id for item in featured_items],
            [articles[1].pk, articles[2].pk],
        )
        self.assertEqual(
            [selection.article_id for selection in selected_articles],
            [article.pk for article in articles],
        )

        article_ids = [article.pk for article in articles]
        selected_item_ids = [selection.pk for selection in selected_articles]
        featured_item_ids = [item.pk for item in featured_items]
        home_revision_count = home.revisions.count()
        expert_revision_count = self.expert.revisions.count()

        self._ensure_curated_articles()

        home.refresh_from_db()
        self.expert.refresh_from_db()
        self.assertEqual(
            list(NothingPersonalArticlePage.objects.order_by("slug").values_list("pk", flat=True)),
            article_ids,
        )
        self.assertEqual(
            list(self.expert.selected_articles.order_by("sort_order", "pk").values_list("pk", flat=True)),
            selected_item_ids,
        )
        self.assertEqual(
            list(home.featured_items.order_by("sort_order", "pk").values_list("pk", flat=True)),
            featured_item_ids,
        )
        self.assertEqual(home.revisions.count(), home_revision_count)
        self.assertEqual(self.expert.revisions.count(), expert_revision_count)

    def test_repairs_partial_homepage_content_without_overwriting_existing_items(self):
        self._ensure_curated_articles()

        home = NothingPersonalHomePage.objects.get(slug="nothing-personal")
        articles = list(NothingPersonalArticlePage.objects.order_by("slug"))
        featured_items = list(home.featured_items.order_by("sort_order", "pk"))
        preserved_featured_item = featured_items[0]
        reusable_featured_item = featured_items[1]

        home.hero_item = articles[4]
        home.save_revision().publish()
        reusable_featured_item.page = None
        reusable_featured_item.save(update_fields=["page"])
        unused_empty_item = NothingPersonalFeaturedItem.objects.create(
            home_page=home,
            page=None,
            sort_order=2,
        )
        self.expert.selected_articles.get(article_id=articles[3].pk).delete()
        home.save_revision().publish()
        revision_count = home.revisions.count()

        self._ensure_curated_articles()

        home.refresh_from_db()
        repaired_featured_items = list(home.featured_items.order_by("sort_order", "pk"))
        self.assertEqual(home.hero_item_id, articles[4].pk)
        self.assertEqual(len(repaired_featured_items), 3)
        self.assertEqual(repaired_featured_items[0].pk, preserved_featured_item.pk)
        self.assertEqual(repaired_featured_items[0].page_id, articles[1].pk)
        self.assertEqual(repaired_featured_items[1].pk, reusable_featured_item.pk)
        self.assertEqual(repaired_featured_items[1].page_id, articles[2].pk)
        self.assertEqual(repaired_featured_items[2].pk, unused_empty_item.pk)
        self.assertIsNone(repaired_featured_items[2].page_id)
        self.assertEqual(home.revisions.count(), revision_count + 1)
        self.assertEqual(
            set(self.expert.selected_articles.values_list("article_id", flat=True)),
            {article.pk for article in articles},
        )

    def test_preserves_full_featured_item_capacity_when_no_slot_is_available(self):
        self._ensure_curated_articles()

        home = NothingPersonalHomePage.objects.get(slug="nothing-personal")
        articles = list(NothingPersonalArticlePage.objects.order_by("slug"))
        home.hero_item = articles[1]
        duplicate_featured_item = NothingPersonalFeaturedItem.objects.create(
            home_page=home,
            page=articles[2],
            sort_order=2,
        )
        home.save_revision().publish()
        revision_count = home.revisions.count()
        featured_state = list(
            home.featured_items.order_by("sort_order", "pk").values_list("pk", "page_id", "sort_order")
        )

        self._ensure_curated_articles()

        home.refresh_from_db()
        self.assertEqual(home.hero_item_id, articles[1].pk)
        self.assertEqual(
            list(home.featured_items.order_by("sort_order", "pk").values_list("pk", "page_id", "sort_order")),
            featured_state,
        )
        self.assertEqual(home.featured_items.count(), 3)
        self.assertEqual(duplicate_featured_item.page_id, articles[2].pk)
        self.assertEqual(home.revisions.count(), revision_count)

    def _ensure_curated_articles(self):
        with patch(
            "foundation_cms.profiles.factories.ImageFactory",
            return_value=self.expert.image,
        ):
            ensure_expert_curated_articles(
                root=self.root,
                default_locale=self.root.locale,
                topics=[],
                expert_pages=[self.expert],
                fake=self.fake,
            )
