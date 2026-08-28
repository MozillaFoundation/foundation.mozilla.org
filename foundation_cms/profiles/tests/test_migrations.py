import json
from importlib import import_module

from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.test import TestCase, TransactionTestCase
from wagtail.models import Locale, Page

from foundation_cms.base.utils.helpers import to_streamfield_value
from foundation_cms.gallery_hub.models import GalleryPage, ProjectPage
from foundation_cms.nothing_personal.models import (
    NothingPersonalArticlePage,
    NothingPersonalHomePage,
)
from foundation_cms.profiles.factories import (
    ExpertHubPageFactory,
    ExpertProfilePageFactory,
)
from foundation_cms.profiles.models import (
    ExpertExternalLink,
    ExpertProfileSelectedArticle,
    ExpertProfileSelectedProject,
)


class ExpertProfileMigrationGraphTests(TestCase):
    migrate_to = ("profiles", "0013_expertprofilepage_bluesky_url_and_more")

    def test_dependency_graph_provides_project_expert_field(self):
        executor = MigrationExecutor(connection)
        plan = executor.loader.graph.forwards_plan(self.migrate_to)

        self.assertLess(
            plan.index(("gallery_hub", "0004_projectpage_expert")),
            plan.index(self.migrate_to),
        )
        state = executor.loader.project_state([self.migrate_to])
        ProjectPage = state.apps.get_model("gallery_hub", "ProjectPage")
        self.assertEqual(ProjectPage._meta.get_field("expert").attname, "expert_id")


class ExpertProfileContentMigrationTests(TransactionTestCase):
    serialized_rollback = True
    migrate_from = ("profiles", "0012_expertprofilepage_selected_article_and_project")
    migrate_to = ("profiles", "0013_expertprofilepage_bluesky_url_and_more")

    def test_forward_reverse_reapply_preserves_localized_legacy_content(self):
        fixture = self._create_current_fixture()
        self._migrate([self.migrate_from])

        old_apps = self.executor.loader.project_state([self.migrate_from]).apps
        OldProfile = old_apps.get_model("profiles", "ExpertProfilePage")
        self.assertEqual(OldProfile.objects.get(pk=fixture["profile_id"]).quote, "English legacy quote")

        self._migrate([self.migrate_to])
        new_apps = self.executor.loader.project_state([self.migrate_to]).apps
        Profile = new_apps.get_model("profiles", "ExpertProfilePage")

        profile = Profile.objects.get(pk=fixture["profile_id"])
        french_profile = Profile.objects.get(pk=fixture["french_profile_id"])
        body = list(profile.body.raw_data)
        french_body = list(french_profile.body.raw_data)
        quote_less_body = list(Profile.objects.get(pk=fixture["quote_less_profile_id"]).body.raw_data)
        equivalent_quote_body = list(Profile.objects.get(pk=fixture["equivalent_quote_profile_id"]).body.raw_data)
        conflicting_quote_body = list(Profile.objects.get(pk=fixture["conflicting_quote_profile_id"]).body.raw_data)

        self.assertEqual(
            [block["type"] for block in body],
            ["quote", "rich_text", "projects_section", "articles_section", "link_section"],
        )
        self.assertEqual(body[0]["value"]["quote"], "English legacy quote")
        self.assertEqual(body[1]["id"], "existing-narrative")
        self.assertEqual(body[2]["value"]["items"][0]["value"], fixture["project_id"])
        self.assertEqual(body[3]["value"]["items"][0]["value"], fixture["article_id"])
        self.assertEqual(body[4]["value"]["rows"][0]["value"]["title"], "Legacy external link")
        self.assertEqual(french_body[0]["value"]["quote"], "Citation française")
        self.assertEqual(quote_less_body, [])
        self.assertEqual(len(equivalent_quote_body), 1)
        self.assertEqual(equivalent_quote_body[0]["id"], "existing-equivalent-quote")
        self.assertEqual(len(conflicting_quote_body), 1)
        self.assertEqual(conflicting_quote_body[0]["id"], "existing-conflicting-quote")
        self.assertEqual(conflicting_quote_body[0]["value"]["quote"], "Editor-authored quote")
        for migrated_body in [
            body,
            french_body,
            quote_less_body,
            equivalent_quote_body,
            conflicting_quote_body,
        ]:
            self.assertLessEqual(
                sum(block["type"] == "quote" for block in migrated_body),
                1,
            )

        bodies_before_repeat = {
            page_id: list(Profile.objects.get(pk=page_id).body.raw_data)
            for page_id in [
                fixture["profile_id"],
                fixture["french_profile_id"],
                fixture["quote_less_profile_id"],
                fixture["equivalent_quote_profile_id"],
                fixture["conflicting_quote_profile_id"],
            ]
        }
        migration = import_module("foundation_cms.profiles.migrations.0013_expertprofilepage_bluesky_url_and_more")
        migration.migrate_legacy_profile_content(new_apps, None)
        self.assertEqual(
            {page_id: list(Profile.objects.get(pk=page_id).body.raw_data) for page_id in bodies_before_repeat},
            bodies_before_repeat,
        )

        revision_bodies = self._revision_bodies(new_apps, fixture["profile_id"])
        self.assertTrue(revision_bodies)
        self.assertTrue(any(block["type"] == "projects_section" for block in revision_bodies[-1]))

        self._migrate([self.migrate_from])
        reversed_apps = self.executor.loader.project_state([self.migrate_from]).apps
        ReversedProfile = reversed_apps.get_model("profiles", "ExpertProfilePage")
        reversed_profile = ReversedProfile.objects.get(pk=fixture["profile_id"])
        self.assertEqual([block["type"] for block in reversed_profile.body.raw_data], ["rich_text"])
        self.assertEqual(reversed_profile.quote, "English legacy quote")
        self.assertEqual(
            list(ReversedProfile.objects.get(pk=fixture["quote_less_profile_id"]).body.raw_data),
            [],
        )
        self.assertEqual(
            list(ReversedProfile.objects.get(pk=fixture["equivalent_quote_profile_id"]).body.raw_data)[0]["id"],
            "existing-equivalent-quote",
        )
        self.assertEqual(
            list(ReversedProfile.objects.get(pk=fixture["conflicting_quote_profile_id"]).body.raw_data)[0]["id"],
            "existing-conflicting-quote",
        )
        self.assertEqual(
            reversed_apps.get_model("profiles", "ExpertExternalLink")
            .objects.filter(page_id=fixture["profile_id"])
            .count(),
            1,
        )

        self._migrate([self.migrate_to])
        reapplied_apps = self.executor.loader.project_state([self.migrate_to]).apps
        reapplied_profile = reapplied_apps.get_model("profiles", "ExpertProfilePage").objects.get(
            pk=fixture["profile_id"]
        )
        reapplied_types = [block["type"] for block in reapplied_profile.body.raw_data]
        self.assertEqual(reapplied_types.count("quote"), 1)
        self.assertEqual(reapplied_types.count("projects_section"), 1)
        self.assertEqual(reapplied_types.count("articles_section"), 1)
        self.assertEqual(reapplied_types.count("link_section"), 1)
        self.assertEqual(
            len(
                list(
                    reapplied_apps.get_model("profiles", "ExpertProfilePage")
                    .objects.get(pk=fixture["equivalent_quote_profile_id"])
                    .body.raw_data
                )
            ),
            1,
        )
        self.assertEqual(
            len(
                list(
                    reapplied_apps.get_model("profiles", "ExpertProfilePage")
                    .objects.get(pk=fixture["conflicting_quote_profile_id"])
                    .body.raw_data
                )
            ),
            1,
        )

    def _migrate(self, targets):
        self.executor = MigrationExecutor(connection)
        self.executor.migrate(targets)

    def _create_current_fixture(self):
        hub = ExpertHubPageFactory()
        profile = ExpertProfilePageFactory(
            parent=hub,
            quote="English legacy quote",
            quote_attribution="English attribution",
        )
        profile.body = to_streamfield_value(
            [
                {
                    "type": "rich_text",
                    "value": "<p>Existing narrative</p>",
                    "id": "existing-narrative",
                }
            ],
            stream_block=profile.body.stream_block,
        )
        profile.save_revision().publish()

        gallery = GalleryPage(
            title="Gallery",
            slug="migration-gallery",
            seo_title="Migration gallery",
            search_description="Migration gallery description.",
        )
        Page.get_first_root_node().add_child(instance=gallery)
        gallery.save_revision().publish()
        project = ProjectPage(
            title="Migration project",
            slug="migration-project",
            hero_image=profile.image,
            seo_title="Migration project",
            search_description="Migration project description.",
        )
        gallery.add_child(instance=project)
        project.save_revision().publish()

        np_home = NothingPersonalHomePage(
            title="Nothing Personal",
            slug="migration-np",
            seo_title="Nothing Personal migration",
            search_description="Nothing Personal migration description.",
        )
        Page.get_first_root_node().add_child(instance=np_home)
        np_home.save_revision().publish()
        article = NothingPersonalArticlePage(
            title="Migration article",
            slug="migration-article",
            lede_text="Migration article lede",
            seo_title="Migration article",
            search_description="Migration article description.",
        )
        np_home.add_child(instance=article)
        article.save_revision().publish()

        ExpertProfileSelectedProject.objects.create(page=profile, project=project, sort_order=0)
        ExpertProfileSelectedArticle.objects.create(page=profile, article=article, sort_order=0)
        ExpertExternalLink.objects.create(
            page=profile,
            title="Legacy external link",
            description="Legacy description",
            url="https://example.com/legacy",
            sort_order=0,
        )
        profile.save_revision().publish()

        french_locale, _ = Locale.objects.get_or_create(language_code="fr")
        french_profile = profile.copy_for_translation(french_locale, copy_parents=True)
        french_profile.quote = "Citation française"
        french_profile.quote_attribution = "Attribution française"
        french_profile.save_revision().publish()

        quote_less_profile = ExpertProfilePageFactory(
            parent=hub,
            quote="",
            quote_attribution="",
            body=[],
        )
        equivalent_quote_profile = ExpertProfilePageFactory(
            parent=hub,
            quote="Already represented",
            quote_attribution="Existing attribution",
        )
        equivalent_quote_profile.body = to_streamfield_value(
            [
                {
                    "type": "quote",
                    "value": {
                        "quote": "Already represented",
                        "attribution": "Existing attribution",
                    },
                    "id": "existing-equivalent-quote",
                }
            ],
            stream_block=equivalent_quote_profile.body.stream_block,
        )
        equivalent_quote_profile.save_revision().publish()

        conflicting_quote_profile = ExpertProfilePageFactory(
            parent=hub,
            quote="Legacy quote should not override body",
            quote_attribution="Legacy attribution",
        )
        conflicting_quote_profile.body = to_streamfield_value(
            [
                {
                    "type": "quote",
                    "value": {
                        "quote": "Editor-authored quote",
                        "attribution": "Editor attribution",
                    },
                    "id": "existing-conflicting-quote",
                }
            ],
            stream_block=conflicting_quote_profile.body.stream_block,
        )
        conflicting_quote_profile.save_revision().publish()

        return {
            "profile_id": profile.pk,
            "french_profile_id": french_profile.pk,
            "quote_less_profile_id": quote_less_profile.pk,
            "equivalent_quote_profile_id": equivalent_quote_profile.pk,
            "conflicting_quote_profile_id": conflicting_quote_profile.pk,
            "project_id": project.pk,
            "article_id": article.pk,
        }

    def _revision_bodies(self, apps, page_id):
        Revision = apps.get_model("wagtailcore", "Revision")
        ContentType = apps.get_model("contenttypes", "ContentType")
        content_type = ContentType.objects.get(app_label="profiles", model="expertprofilepage")
        bodies = []
        for revision in Revision.objects.filter(
            content_type_id=content_type.pk,
            object_id=str(page_id),
        ).order_by("pk"):
            body = revision.content["body"]
            bodies.append(json.loads(body) if isinstance(body, str) else body)
        return bodies
