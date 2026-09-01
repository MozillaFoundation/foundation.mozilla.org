from io import StringIO
from types import SimpleNamespace

from django.core.management import call_command
from django.core.management.base import CommandError
from django.test import SimpleTestCase
from django.utils.text import slugify
from wagtail.models import Page
from wagtail.test.utils import WagtailPageTestCase

from foundation_cms.base.factories import ImageFactory
from foundation_cms.base.models.abstract_base_page import Topic
from foundation_cms.core.factories import HomePageFactory
from foundation_cms.gallery_hub.models import GalleryPage, ProjectPage
from foundation_cms.nothing_personal.models import (
    NothingPersonalArticlePage,
    NothingPersonalHomePage,
)
from foundation_cms.profiles.factories import (
    ExpertHubPageFactory,
    ExpertProfilePageFactory,
)
from foundation_cms.profiles.management.commands.seed_expert_profile_qa import (
    QA_BIO,
    QA_IMAGELESS_ARTICLE_SLUG,
    QA_MANUAL_PROJECT_IMAGE_TITLE,
    QA_PROJECTS,
    QA_SLUG,
    _body,
    _validate_stream_payload,
)
from foundation_cms.profiles.models import ExpertProfilePage


class ExpertProfileQAFixtureTests(SimpleTestCase):
    def test_body_has_six_projects_with_media_then_text_only_entries(self):
        projects = [SimpleNamespace(pk=1), SimpleNamespace(pk=2)]
        articles = [SimpleNamespace(pk=3), SimpleNamespace(pk=4)]
        image = SimpleNamespace(pk=5)

        body = _body(projects, articles, image)
        project_section = next(block for block in body if block["type"] == "projects_section")
        project_items = project_section["value"]["items"]
        manual_projects = [
            item["value"] for item in project_section["value"]["items"] if item["type"] == "manual_project"
        ]

        self.assertEqual(
            [item["type"] for item in project_items],
            [
                "cms_project",
                "manual_project",
                "cms_project",
                "manual_project",
                "manual_project",
                "manual_project",
            ],
        )
        self.assertEqual(len(project_items), 6)
        self.assertEqual(len(manual_projects), 4)
        self.assertEqual(
            manual_projects[0]["image"],
            {
                "image": image.pk,
                "alt_text": "People gathered at a Mozilla Festival community event",
                "decorative": False,
            },
        )
        self.assertEqual(
            [project["image"] for project in manual_projects[1:]],
            [None] * 3,
        )
        self.assertEqual(body, _body(projects, articles, image))

    def test_body_has_reference_article_and_link_section_counts(self):
        body = _body(
            [SimpleNamespace(pk=1), SimpleNamespace(pk=2)],
            [SimpleNamespace(pk=3), SimpleNamespace(pk=4)],
            SimpleNamespace(pk=5),
        )
        article_section = next(block for block in body if block["type"] == "articles_section")
        link_sections = [block for block in body if block["type"] == "link_section"]

        self.assertEqual(
            [item["type"] for item in article_section["value"]["items"]],
            ["cms_article", "cms_article", *("manual_article" for _ in range(5))],
        )
        self.assertEqual(
            [(section["value"]["heading"], len(section["value"]["rows"])) for section in link_sections],
            [("Awards & Recognition", 5), ("Featured Talks", 3)],
        )
        self.assertTrue(any(not row["value"]["url"] for section in link_sections for row in section["value"]["rows"]))

    def test_bio_has_multiple_rich_text_paragraphs_for_headshot_wrap_qa(self):
        self.assertEqual(QA_BIO.count("<p>"), 4)
        self.assertIn("continue beneath the floated headshot", QA_BIO)
        self.assertIn('<a href="https://example.com/open-source">open source</a>', QA_BIO)

    def test_unknown_body_block_type_is_rejected(self):
        with self.assertRaisesMessage(CommandError, 'Unknown block type "unknown_section"'):
            _validate_stream_payload(
                ExpertProfilePage.body.field.stream_block,
                [{"type": "unknown_section", "value": {}}],
            )


class ExpertProfileQACommandTests(WagtailPageTestCase):
    def setUp(self):
        self.home = HomePageFactory()
        self.hub = ExpertHubPageFactory(parent=self.home, slug="expert-hub")
        self.source_profile = ExpertProfilePageFactory(parent=self.hub, slug="source-profile")
        self.source_profile.save_revision().publish()

        self.gallery = GalleryPage(
            title="QA gallery",
            slug="qa-gallery",
            seo_title="QA gallery",
            search_description="QA gallery.",
        )
        Page.get_first_root_node().add_child(instance=self.gallery)
        self.gallery.save_revision().publish()
        source_project = ProjectPage(
            title="Source project",
            slug="source-project",
            seo_title="Source project",
            search_description="Source project.",
            hero_image=self.source_profile.image,
        )
        self.gallery.add_child(instance=source_project)
        source_project.save_revision().publish()

        article_home = NothingPersonalHomePage(
            title="QA articles",
            slug="qa-articles",
            seo_title="QA articles",
            search_description="QA articles.",
        )
        Page.get_first_root_node().add_child(instance=article_home)
        article_home.save_revision().publish()
        for index in range(2):
            article = NothingPersonalArticlePage(
                title=f"Source article {index}",
                slug=f"source-article-{index}",
                seo_title=f"Source article {index}",
                search_description=f"Source article {index}.",
                lede_text=f"Source article {index} lede.",
            )
            article_home.add_child(instance=article)
            article.save_revision().publish()

        for title in [
            *(definition["image_title"] for definition in QA_PROJECTS),
            QA_MANUAL_PROJECT_IMAGE_TITLE,
        ]:
            ImageFactory(title=title)
        for name in ["Security", "Education"]:
            Topic.objects.get_or_create(
                name=name,
                defaults={"slug": slugify(name)},
            )

    def test_second_seed_is_unchanged_without_revision_churn(self):
        first_output = StringIO()
        call_command("seed_expert_profile_qa", stdout=first_output)

        profile = ExpertProfilePage.objects.get(slug=QA_SLUG)
        seeded_pages = [
            profile,
            *ProjectPage.objects.filter(slug__in=[definition["slug"] for definition in QA_PROJECTS]),
            NothingPersonalArticlePage.objects.get(slug=QA_IMAGELESS_ARTICLE_SLUG),
        ]
        revision_counts = {page.pk: page.revisions.count() for page in seeded_pages}
        body_state = profile.body.stream_block.get_prep_value(profile.body)

        second_output = StringIO()
        call_command("seed_expert_profile_qa", stdout=second_output)

        profile.refresh_from_db()
        self.assertIn("Created", first_output.getvalue())
        self.assertIn("Unchanged", second_output.getvalue())
        self.assertEqual(
            {page.pk: page.revisions.count() for page in seeded_pages},
            revision_counts,
        )
        self.assertEqual(
            profile.body.stream_block.get_prep_value(profile.body),
            body_state,
        )
