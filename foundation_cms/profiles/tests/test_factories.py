from datetime import datetime, timezone
from types import SimpleNamespace
from unittest.mock import patch

from wagtail.models import Page
from wagtail.test.utils import WagtailPageTestCase

from foundation_cms.base.factories import ImageFactory as BaseImageFactory
from foundation_cms.base.utils.helpers import get_faker, to_streamfield_value
from foundation_cms.core.factories import HomePageFactory
from foundation_cms.gallery_hub.models import GalleryPage, ProjectPage
from foundation_cms.nothing_personal.models import (
    NothingPersonalArticlePage,
    NothingPersonalHomePage,
)
from foundation_cms.nothing_personal.models.home_page import NothingPersonalFeaturedItem
from foundation_cms.profiles import expert_profile_data as profile_data
from foundation_cms.profiles.factories import (
    CURATED_ARTICLE_EXPERT_SLUG,
    EXTERNAL_LINKS,
    ExpertHubPageFactory,
    ExpertProfilePageFactory,
    build_expert_profile_body,
    ensure_expert_curated_articles,
    ensure_expert_external_links,
    ensure_expert_intro_quote,
    ensure_expert_profile_composition,
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
        article_sections = [block for block in self.expert.body if block.block_type == "articles_section"]
        self.assertEqual(len(article_sections), 1)
        self.assertEqual(
            [item.value.pk for item in article_sections[0].value["items"]],
            [article.pk for article in articles],
        )
        self.assertEqual(
            [article.first_published_at for article in articles],
            [datetime(2025, 1, 1, tzinfo=timezone.utc)] * len(articles),
        )

        article_state = [(article.pk, article.first_published_at, article.revisions.count()) for article in articles]
        selected_item_state = [
            (selection.pk, selection.article_id, selection.sort_order) for selection in selected_articles
        ]
        featured_item_state = [(item.pk, item.page_id, item.sort_order) for item in featured_items]
        hero_item_id = home.hero_item_id
        home_revision_count = home.revisions.count()
        expert_revision_count = self.expert.revisions.count()

        self._ensure_curated_articles()

        home.refresh_from_db()
        self.expert.refresh_from_db()
        self.assertEqual(
            [
                (article.pk, article.first_published_at, article.revisions.count())
                for article in NothingPersonalArticlePage.objects.order_by("slug")
            ],
            article_state,
        )
        self.assertEqual(
            list(
                self.expert.selected_articles.order_by("sort_order", "pk").values_list(
                    "pk", "article_id", "sort_order"
                )
            ),
            selected_item_state,
        )
        self.assertEqual(
            list(home.featured_items.order_by("sort_order", "pk").values_list("pk", "page_id", "sort_order")),
            featured_item_state,
        )
        self.assertEqual(home.hero_item_id, hero_item_id)
        self.assertEqual(home.revisions.count(), home_revision_count)
        self.assertEqual(self.expert.revisions.count(), expert_revision_count)

    def test_seeds_intro_quote_once(self):
        ensure_expert_intro_quote(self.expert)
        ensure_expert_intro_quote(self.expert)

        quote_blocks = [block for block in self.expert.body if block.block_type == "quote"]
        self.assertEqual(len(quote_blocks), 1)

    def test_seeds_external_links_in_legacy_storage_and_body_once(self):
        self.expert.body = to_streamfield_value(
            [
                {
                    "type": "link_section",
                    "value": {
                        "heading": "Awards",
                        "rows": [
                            {
                                "type": "link",
                                "value": {
                                    "title": "Existing award",
                                    "description": "",
                                    "url": "",
                                },
                            }
                        ],
                    },
                    "id": "existing-awards",
                }
            ],
            stream_block=self.expert.body.stream_block,
        )
        self.expert.save_revision().publish()

        ensure_expert_external_links(self.root.locale)
        ensure_expert_external_links(self.root.locale)

        self.expert.refresh_from_db()
        link_sections = [block for block in self.expert.body if block.block_type == "link_section"]
        self.assertEqual(self.expert.external_links.count(), len(EXTERNAL_LINKS))
        self.assertEqual(
            [block.value["heading"] for block in link_sections],
            ["Awards", "Awards & Recognition", "Featured Talks"],
        )
        self.assertEqual(
            [len(block.value["rows"]) for block in link_sections[1:]],
            [5, 3],
        )

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
        self.assertEqual(repaired_featured_items[1].page_id, articles[0].pk)
        self.assertEqual(repaired_featured_items[2].pk, unused_empty_item.pk)
        self.assertIsNone(repaired_featured_items[2].page_id)
        self.assertEqual(home.revisions.count(), revision_count + 1)
        self.assertEqual(
            set(self.expert.selected_articles.values_list("article_id", flat=True)),
            {article.pk for article in articles},
        )

    def test_repairs_missing_hero_without_reusing_a_featured_article(self):
        self._ensure_curated_articles()

        home = NothingPersonalHomePage.objects.get(slug="nothing-personal")
        articles = list(NothingPersonalArticlePage.objects.order_by("slug"))
        featured_items = list(home.featured_items.order_by("sort_order", "pk"))
        preserved_featured_item = featured_items[0]
        reusable_featured_item = featured_items[1]
        unused_empty_item = NothingPersonalFeaturedItem.objects.create(
            home_page=home,
            page=None,
            sort_order=2,
        )

        home.hero_item = None
        preserved_featured_item.page = articles[0]
        preserved_featured_item.save(update_fields=["page"])
        reusable_featured_item.page = None
        reusable_featured_item.save(update_fields=["page"])
        home.save_revision().publish()
        revision_count = home.revisions.count()

        self._ensure_curated_articles()

        home.refresh_from_db()
        repaired_featured_items = list(home.featured_items.order_by("sort_order", "pk"))
        self.assertEqual(home.hero_item_id, articles[1].pk)
        self.assertEqual(len(repaired_featured_items), 3)
        self.assertEqual(repaired_featured_items[0].pk, preserved_featured_item.pk)
        self.assertEqual(repaired_featured_items[0].page_id, articles[0].pk)
        self.assertEqual(repaired_featured_items[1].pk, reusable_featured_item.pk)
        self.assertEqual(repaired_featured_items[1].page_id, articles[2].pk)
        self.assertEqual(repaired_featured_items[2].pk, unused_empty_item.pk)
        self.assertIsNone(repaired_featured_items[2].page_id)
        self.assertNotIn(
            home.hero_item_id,
            [item.page_id for item in repaired_featured_items if item.page_id],
        )
        self.assertEqual(home.revisions.count(), revision_count + 1)

        featured_state = [(item.pk, item.page_id, item.sort_order) for item in repaired_featured_items]
        revision_count = home.revisions.count()

        self._ensure_curated_articles()

        home.refresh_from_db()
        self.assertEqual(home.hero_item_id, articles[1].pk)
        self.assertEqual(
            list(home.featured_items.order_by("sort_order", "pk").values_list("pk", "page_id", "sort_order")),
            featured_state,
        )
        self.assertEqual(home.revisions.count(), revision_count)

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


class ExpertProfileDataTests(WagtailPageTestCase):
    def setUp(self):
        self.root = HomePageFactory()
        self.hub = ExpertHubPageFactory(parent=self.root)
        self.expert = ExpertProfilePageFactory(
            parent=self.hub,
            slug=profile_data.EXPERT_SLUG,
        )
        self.expert.save_revision().publish()

        gallery = GalleryPage(
            title="Gallery",
            slug="gallery",
            seo_title="Gallery",
            search_description="Explore community projects.",
        )
        Page.get_first_root_node().add_child(instance=gallery)
        gallery.save_revision().publish()
        self.projects = []
        for index in range(2):
            project = ProjectPage(
                title=f"Project {index + 1}",
                slug=f"gallery-project-{index + 1}",
                seo_title=f"Project {index + 1}",
                search_description="A community technology project.",
            )
            gallery.add_child(instance=project)
            project.save_revision().publish()
            self.projects.append(project)

        article_home = NothingPersonalHomePage(
            title="Nothing Personal",
            slug="nothing-personal",
            seo_title="Nothing Personal",
            search_description="Articles and publications.",
        )
        Page.get_first_root_node().add_child(instance=article_home)
        article_home.save_revision().publish()
        for index in (1, 5):
            article = NothingPersonalArticlePage(
                title=f"Article {index}",
                slug=f"expert-profile-article-{index}",
                seo_title=f"Article {index}",
                search_description="A public-interest technology article.",
                lede_text="A public-interest technology article.",
            )
            article_home.add_child(instance=article)
            article.save_revision().publish()

        BaseImageFactory(title=profile_data.PROFILE_IMAGE_TITLE)

    def test_representative_profile_composition_is_deterministic_and_idempotent(self):
        profile = ensure_expert_profile_composition(self.root.locale, self.projects)
        revision_count = profile.revisions.count()
        body_state = profile.body.stream_block.get_prep_value(profile.body)

        self.assertEqual(profile.title, "Priya Goswami")
        self.assertEqual(
            [block.block_type for block in profile.body],
            ["quote", "projects_section", "articles_section", "link_section", "link_section"],
        )
        project_items = profile.body[1].value["items"]
        self.assertEqual(len(project_items), 6)
        self.assertEqual(
            [item.block_type for item in project_items],
            ["cms_project", "manual_project", "cms_project", "manual_project", "manual_project", "manual_project"],
        )
        self.assertTrue(
            all("image" not in item.value for item in project_items if item.block_type == "manual_project")
        )
        self.assertEqual(len(profile.body[2].value["items"]), 7)
        self.assertEqual(
            [block.value["heading"] for block in profile.body[3:]],
            ["Awards & Recognition", "Featured Talks"],
        )

        same_profile = ensure_expert_profile_composition(self.root.locale, self.projects)
        same_profile.refresh_from_db()
        self.assertEqual(same_profile.revisions.count(), revision_count)
        self.assertEqual(same_profile.body.stream_block.get_prep_value(same_profile.body), body_state)

    def test_body_builder_uses_stable_ids_for_the_same_content(self):
        def id_factory(block_type, item_id=None):
            return f"{block_type}:{item_id or 'section'}"

        articles = [SimpleNamespace(pk=3), SimpleNamespace(pk=4)]

        first = build_expert_profile_body(
            self.projects,
            articles,
            id_factory,
        )
        second = build_expert_profile_body(
            self.projects,
            articles,
            id_factory,
        )

        self.assertEqual(first, second)
