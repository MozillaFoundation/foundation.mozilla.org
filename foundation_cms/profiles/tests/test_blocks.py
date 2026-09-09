import pytest
from bs4 import BeautifulSoup
from django.utils.translation import override
from wagtail import blocks
from wagtail.blocks import StreamBlockValidationError, StructBlockValidationError
from wagtail.models import Locale, Page, PageViewRestriction
from wagtail.test.utils import WagtailPageTestCase

from foundation_cms.core.models import GeneralPage
from foundation_cms.gallery_hub.models import GalleryPage, ProjectPage
from foundation_cms.nothing_personal.models import (
    NothingPersonalArticlePage,
    NothingPersonalHomePage,
)
from foundation_cms.profiles.blocks import (
    ArticlesSectionBlock,
    ProjectsSectionBlock,
)
from foundation_cms.profiles.factories import (
    ExpertHubPageFactory,
    ExpertProfilePageFactory,
)
from foundation_cms.profiles.models import ExpertProfilePage


def test_manual_project_has_no_image_field():
    manual_project = ProjectsSectionBlock().child_blocks["items"].child_blocks["manual_project"]
    assert "image" not in manual_project.child_blocks


def test_projects_section_schema_has_no_arbitrary_item_cap():
    items = ProjectsSectionBlock().child_blocks["items"]

    assert items.meta.max_num is None


def test_curated_projects_require_items():
    block = ProjectsSectionBlock()
    value = block.to_python({"source": "curated", "items": []})

    with pytest.raises(StructBlockValidationError) as exc_info:
        block.clean(value)

    assert "items" in exc_info.value.block_errors


def test_related_projects_reject_curated_items():
    block = ProjectsSectionBlock()
    value = block.to_python(
        {
            "source": "related",
            "items": [
                {
                    "type": "manual_project",
                    "value": {
                        "title": "Manual project",
                        "description": "",
                        "url": "https://example.com/project",
                        "link_label": "",
                    },
                }
            ],
        }
    )

    with pytest.raises(StructBlockValidationError) as exc_info:
        block.clean(value)

    assert "items" in exc_info.value.block_errors


def test_profile_body_limits_major_section_blocks():
    stream_block = ExpertProfilePage._meta.get_field("body").stream_block
    value = stream_block.to_python(
        [
            {"type": "quote", "value": {"quote": "First", "attribution": ""}},
            {"type": "quote", "value": {"quote": "Second", "attribution": ""}},
        ]
    )

    with pytest.raises(StreamBlockValidationError) as exc_info:
        stream_block.clean(value)

    assert exc_info.value.non_block_errors


def test_profile_only_blocks_are_not_available_on_general_pages():
    profile_blocks = ExpertProfilePage._meta.get_field("body").stream_block.child_blocks
    general_blocks = GeneralPage._meta.get_field("body").stream_block.child_blocks

    assert set(profile_blocks) == {"quote", "projects_section", "articles_section", "link_section"}
    assert not {"projects_section", "articles_section", "link_section"} & general_blocks.keys()
    assert isinstance(profile_blocks["quote"], blocks.StructBlock)


class ProfileSectionVisibilityTests(WagtailPageTestCase):
    def setUp(self):
        self.hub = ExpertHubPageFactory()
        self.profile = ExpertProfilePageFactory(parent=self.hub)
        self.gallery = GalleryPage(
            title="Visibility gallery",
            slug="visibility-gallery",
            seo_title="Visibility gallery",
            search_description="Visibility gallery.",
        )
        Page.get_first_root_node().add_child(instance=self.gallery)
        self.gallery.save_revision().publish()
        self.article_home = NothingPersonalHomePage(
            title="Visibility articles",
            slug="visibility-articles",
            seo_title="Visibility articles",
            search_description="Visibility articles.",
        )
        Page.get_first_root_node().add_child(instance=self.article_home)
        self.article_home.save_revision().publish()

    def test_curated_sections_render_only_live_public_pages(self):
        public_project = self._create_project("Public project", "public-project")
        draft_project = self._create_project("Draft project", "draft-project", live=False)
        restricted_project = self._create_project("Restricted project", "restricted-project")
        self._restrict(restricted_project)

        public_article = self._create_article("Public article", "public-article")
        draft_article = self._create_article("Draft article", "draft-article", live=False)
        restricted_article = self._create_article("Restricted article", "restricted-article")
        self._restrict(restricted_article)

        projects_value = self._projects_value(public_project, draft_project, restricted_project)
        articles_value = self._articles_value(public_article, draft_article, restricted_article)
        projects_html = ProjectsSectionBlock().render(projects_value, context={"page": self.profile})
        articles_html = ArticlesSectionBlock().render(articles_value, context={"page": self.profile})

        self.assertEqual(len(projects_value["items"]), 3)
        self.assertEqual(len(articles_value["items"]), 3)
        self.assertIn("Public project", projects_html)
        self.assertIn("Public article", articles_html)
        for hidden_title in ["Draft project", "Restricted project"]:
            self.assertNotIn(hidden_title, projects_html)
        for hidden_title in ["Draft article", "Restricted article"]:
            self.assertNotIn(hidden_title, articles_html)
        self.assertNotIn("draft-project", projects_html)
        self.assertNotIn("restricted-project", projects_html)
        self.assertNotIn("draft-article", articles_html)
        self.assertNotIn("restricted-article", articles_html)

    def test_curated_sections_filter_after_localization(self):
        locale, _ = Locale.objects.get_or_create(language_code="fr")
        public_project = self._create_project("English public project", "localized-public-project")
        restricted_project = self._create_project("English restricted project", "localized-restricted-project")
        draft_project = self._create_project("English draft project", "localized-draft-project", live=False)
        public_article = self._create_article("English public article", "localized-public-article")
        restricted_article = self._create_article("English restricted article", "localized-restricted-article")
        draft_article = self._create_article("English draft article", "localized-draft-article", live=False)

        public_project_fr = self._translate(public_project, locale, "Projet public français")
        restricted_project_fr = self._translate(restricted_project, locale, "Projet restreint français")
        self._restrict(restricted_project_fr)
        self._translate(draft_project, locale, "Projet brouillon français", live=False)
        public_article_fr = self._translate(public_article, locale, "Article public français")
        restricted_article_fr = self._translate(restricted_article, locale, "Article restreint français")
        self._restrict(restricted_article_fr)
        self._translate(draft_article, locale, "Article brouillon français", live=False)

        with override("fr"):
            projects_html = ProjectsSectionBlock().render(
                self._projects_value(public_project, restricted_project, draft_project),
                context={"page": self.profile},
            )
            articles_html = ArticlesSectionBlock().render(
                self._articles_value(public_article, restricted_article, draft_article),
                context={"page": self.profile},
            )

        self.assertIn(public_project_fr.title, projects_html)
        self.assertIn(public_article_fr.title, articles_html)
        for hidden_title in [
            restricted_project_fr.title,
            "Projet brouillon français",
            restricted_project.title,
            draft_project.title,
        ]:
            self.assertNotIn(hidden_title, projects_html)
        for hidden_title in [
            restricted_article_fr.title,
            "Article brouillon français",
            restricted_article.title,
            draft_article.title,
        ]:
            self.assertNotIn(hidden_title, articles_html)

    def test_articles_section_owns_its_visible_count(self):
        articles = [self._create_article(f"Visible article {index}", f"visible-article-{index}") for index in range(4)]
        block = ArticlesSectionBlock()
        rendered = block.render(self._articles_value(*articles), context={"page": self.profile})
        soup = BeautifulSoup(rendered, "html.parser")
        rendered_articles = soup.select("[data-expert-profile-article-list] > li")
        show_more = soup.select_one("[data-expert-profile-show-articles]")

        self.assertIn(f'data-visible-count="{block.visible_count}"', rendered)
        self.assertEqual(len(rendered_articles), 4)
        self.assertTrue(all(not article.has_attr("hidden") for article in rendered_articles))
        self.assertIsNotNone(show_more)
        self.assertTrue(show_more.has_attr("hidden"))

    def test_projects_section_accepts_more_than_three_mixed_items(self):
        projects = [self._create_project(f"Project {index}", f"project-{index}") for index in range(3)]
        block = ProjectsSectionBlock()
        value = block.to_python(
            {
                "source": "curated",
                "items": [
                    *[{"type": "cms_project", "value": project.pk} for project in projects],
                    {
                        "type": "manual_project",
                        "value": {
                            "title": "Fourth project",
                            "description": "",
                            "url": "https://example.com/fourth-project",
                            "link_label": "",
                        },
                    },
                ],
            }
        )

        cleaned = block.clean(value)

        self.assertEqual(len(cleaned["items"]), 4)

    def test_related_projects_are_not_truncated(self):
        for index in range(4):
            self._create_project(
                f"Related project {index}",
                f"related-project-{index}",
                expert=self.profile,
            )

        self.assertEqual(len(self.profile.get_related_projects()), 4)

    def _create_project(self, title, slug, live=True, expert=None):
        project = ProjectPage(
            title=title,
            slug=slug,
            live=live,
            has_unpublished_changes=not live,
            seo_title=title,
            search_description=f"{title} description.",
            hero_image=self.profile.image,
            expert=expert,
        )
        self.gallery.add_child(instance=project)
        revision = project.save_revision()
        if live:
            revision.publish()
        return project

    def _create_article(self, title, slug, live=True):
        article = NothingPersonalArticlePage(
            title=title,
            slug=slug,
            live=live,
            has_unpublished_changes=not live,
            seo_title=title,
            search_description=f"{title} description.",
            lede_text=f"{title} lede.",
        )
        self.article_home.add_child(instance=article)
        revision = article.save_revision()
        if live:
            revision.publish()
        return article

    def _translate(self, page, locale, title, live=True):
        translation = page.copy_for_translation(locale, copy_parents=True)
        translation.title = title
        translation.seo_title = title
        translation.search_description = f"{title} description."
        revision = translation.save_revision()
        if live:
            revision.publish()
        return translation

    def _restrict(self, page):
        PageViewRestriction.objects.create(
            page=page,
            restriction_type=PageViewRestriction.PASSWORD,
            password="test-password",
        )

    def _projects_value(self, *projects):
        return ProjectsSectionBlock().to_python(
            {
                "source": "curated",
                "items": [{"type": "cms_project", "value": project.pk} for project in projects],
            }
        )

    def _articles_value(self, *articles):
        return ArticlesSectionBlock().to_python(
            {
                "items": [{"type": "cms_article", "value": article.pk} for article in articles],
            }
        )
