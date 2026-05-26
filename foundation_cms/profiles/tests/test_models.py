from wagtail.models import Page
from wagtail.test.utils import WagtailPageTestCase

from foundation_cms.gallery_hub.models import GalleryPage, ProjectPage
from foundation_cms.profiles.factories import (
    ExpertDirectoryPageFactory,
    ExpertHubPageFactory,
    ExpertProfilePageFactory,
)
from foundation_cms.profiles.models import (
    ExpertProfileSelectedArticle,
    ExpertProfileSelectedProject,
)


class ExpertProfilePageTestCase(WagtailPageTestCase):
    def setUp(self):
        self.hub = ExpertHubPageFactory()
        self.page = ExpertProfilePageFactory(parent=self.hub)

    def test_str_representation(self):
        self.assertEqual(str(self.page), self.page.title)

    def test_required_fields_populated(self):
        self.assertTrue(self.page.role)
        self.assertTrue(self.page.bio)
        self.assertTrue(self.page.location)
        self.assertIsNotNone(self.page.image)

    def test_is_leaf_page(self):
        self.assertEqual(self.page.subpage_types, [])

    def test_get_profile_projects_returns_selected_projects_in_editor_order(self):
        gallery = self._create_gallery_page()
        fallback_project = self._create_project(gallery, "Fallback Project", "fallback-project", expert=self.page)
        first_project = self._create_project(gallery, "First Selected Project", "first-selected-project")
        second_project = self._create_project(gallery, "Second Selected Project", "second-selected-project")

        ExpertProfileSelectedProject.objects.create(page=self.page, project=second_project, sort_order=0)
        ExpertProfileSelectedProject.objects.create(page=self.page, project=first_project, sort_order=1)

        projects = list(self.page.get_profile_projects())

        self.assertEqual(projects, [second_project, first_project])
        self.assertNotIn(fallback_project, projects)

    def test_get_profile_projects_falls_back_to_related_projects(self):
        gallery = self._create_gallery_page()
        older_project = self._create_project(gallery, "Older Project", "older-project", expert=self.page)
        newer_project = self._create_project(gallery, "Newer Project", "newer-project", expert=self.page)

        projects = list(self.page.get_profile_projects())

        self.assertEqual(projects, [newer_project, older_project])

    def test_get_project_block_rows_returns_three_project_blocks_per_row(self):
        gallery = self._create_gallery_page()
        projects = [
            self._create_project(gallery, f"Project {index}", f"project-{index}", expert=self.page)
            for index in range(4)
        ]

        rows = self.page.get_project_block_rows()

        self.assertEqual(len(rows), 1)
        self.assertEqual(len(rows[0]), 3)
        self.assertEqual(
            [block["project"] for row in rows for block in row],
            list(reversed(projects))[:3],
        )
        self.assertTrue(all(block["show_description"] for row in rows for block in row))

    def test_get_project_block_rows_omits_incomplete_project_rows(self):
        gallery = self._create_gallery_page()
        self._create_project(gallery, "First Project", "first-project", expert=self.page)
        self._create_project(gallery, "Second Project", "second-project", expert=self.page)

        rows = self.page.get_project_block_rows()

        self.assertEqual(rows, [])

    def test_get_selected_articles_returns_pages_in_editor_order(self):
        first_article = ExpertDirectoryPageFactory(parent=self.hub, title="First Article")
        second_article = ExpertDirectoryPageFactory(parent=self.hub, title="Second Article")

        ExpertProfileSelectedArticle.objects.create(page=self.page, article=second_article, sort_order=0)
        ExpertProfileSelectedArticle.objects.create(page=self.page, article=first_article, sort_order=1)

        articles = list(self.page.get_selected_articles())

        self.assertEqual(articles, [second_article, first_article])

    def _create_gallery_page(self):
        gallery = GalleryPage(
            title="Gallery",
            slug="gallery",
            seo_title="Gallery",
            search_description="Gallery projects.",
        )
        Page.get_first_root_node().add_child(instance=gallery)
        gallery.save_revision().publish()
        return gallery

    def _create_project(self, parent, title, slug, expert=None):
        project = ProjectPage(
            title=title,
            slug=slug,
            seo_title=title,
            search_description=f"{title} description.",
            expert=expert,
            hero_image=self.page.image,
        )
        parent.add_child(instance=project)
        project.save_revision().publish()
        return project


class ExpertDirectoryPageTestCase(WagtailPageTestCase):
    def setUp(self):
        self.hub = ExpertHubPageFactory()
        self.directory = ExpertDirectoryPageFactory(parent=self.hub)

    def test_parent_is_hub(self):
        self.assertEqual(self.directory.get_parent().specific, self.hub)

    def test_is_leaf_page(self):
        self.assertEqual(self.directory.subpage_types, [])

    def test_get_experts_returns_hub_children(self):
        expert = ExpertProfilePageFactory(parent=self.hub)
        experts = self.directory.get_experts()
        self.assertIn(expert, experts)
