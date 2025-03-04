from django.test import TestCase

from foundation_cms.legacy_apps.wagtailpages.factory.libraries.rcc import (
    detail_page as detail_page_factory,
)
from foundation_cms.legacy_apps.wagtailpages.factory.libraries.rcc import (
    relations as relations_factory,
)
from foundation_cms.legacy_apps.wagtailpages.factory.profiles import ProfileFactory
from foundation_cms.legacy_apps.wagtailpages.pagemodels.libraries.rcc import (
    utils as rcc_utils,
)
from foundation_cms.legacy_apps.wagtailpages.pagemodels.profiles import Profile


class TestGetRCCAuthors(TestCase):
    def test_get_rcc_authors(self):
        rcc_author_profile = ProfileFactory()
        relations_factory.RCCAuthorRelationFactory(
            detail_page=detail_page_factory.RCCDetailPageFactory(),
            author_profile=rcc_author_profile,
        )
        not_rcc_author_profile = ProfileFactory()

        rcc_author_profiles = rcc_utils.get_rcc_authors()

        self.assertIn(rcc_author_profile, rcc_author_profiles)
        self.assertNotIn(not_rcc_author_profile, rcc_author_profiles)

    def test_get_rcc_authors_distinct(self):
        """Return rcc author profile only once"""

        rcc_author_profile = ProfileFactory()
        relations_factory.RCCAuthorRelationFactory(
            detail_page=detail_page_factory.RCCDetailPageFactory(),
            author_profile=rcc_author_profile,
        )
        relations_factory.RCCAuthorRelationFactory(
            detail_page=detail_page_factory.RCCDetailPageFactory(),
            author_profile=rcc_author_profile,
        )

        profiles = Profile.objects.all()
        profiles = rcc_utils.get_rcc_authors()
        profiles = profiles.filter(id=rcc_author_profile.id)
        count = profiles.count()

        self.assertEqual(count, 1)
