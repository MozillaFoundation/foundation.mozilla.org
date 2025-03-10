from django.test import TestCase

from foundation_cms.legacy_apps.wagtailpages.factory.libraries.research_hub import (
    detail_page as detail_page_factory,
)
from foundation_cms.legacy_apps.wagtailpages.factory.libraries.research_hub import (
    relations as relations_factory,
)
from foundation_cms.legacy_apps.wagtailpages.factory.profiles import ProfileFactory
from foundation_cms.legacy_apps.wagtailpages.pagemodels.libraries.research_hub import (
    utils as research_utils,
)
from foundation_cms.legacy_apps.wagtailpages.pagemodels.profiles import Profile


class TestGetResearchAuthors(TestCase):
    def test_get_research_authors(self):
        research_author_profile = ProfileFactory()
        relations_factory.ResearchAuthorRelationFactory(
            detail_page=detail_page_factory.ResearchDetailPageFactory(),
            author_profile=research_author_profile,
        )
        not_research_author_profile = ProfileFactory()

        research_author_profiles = research_utils.get_research_authors()

        self.assertIn(research_author_profile, research_author_profiles)
        self.assertNotIn(not_research_author_profile, research_author_profiles)

    def test_get_research_authors_distinct(self):
        """Return research author profile only once"""

        research_author_profile = ProfileFactory()
        relations_factory.ResearchAuthorRelationFactory(
            detail_page=detail_page_factory.ResearchDetailPageFactory(),
            author_profile=research_author_profile,
        )
        relations_factory.ResearchAuthorRelationFactory(
            detail_page=detail_page_factory.ResearchDetailPageFactory(),
            author_profile=research_author_profile,
        )

        profiles = Profile.objects.all()
        profiles = research_utils.get_research_authors()
        profiles = profiles.filter(id=research_author_profile.id)
        count = profiles.count()

        self.assertEqual(count, 1)
