from django import test
from django.core import exceptions
from wagtail.core import models as wagtail_models

from networkapi.wagtailpages.factory import research_hub as research_factory
from networkapi.wagtailpages.factory import homepage as home_factory
from networkapi.wagtailpages.factory import profiles as profile_factory


class TestResearchAuthorIndexPage(test.TestCase):
    @classmethod
    def setUpTestData(cls):
        cls._setup_homepage()
        cls.author_index = research_factory.ResearchAuthorsIndexPageFactory(
            parent=cls.homepage,
            title="Authors",
        )
        cls.profile = profile_factory.ProfileFactory()

    @classmethod
    def _setup_homepage(cls):
        root = wagtail_models.Page.get_first_root_node()
        if not root:
            raise ValueError('A root page should exist. Something is off.')
        cls.homepage = home_factory.WagtailHomepageFactory(parent=root)

        sites = wagtail_models.Site.objects.all()
        if sites.count() != 1:
            raise ValueError('There should be exactly one site. Something is off.')
        cls.site = sites.first()

        cls.site.root_page = cls.homepage
        cls.site.clean()
        cls.site.save()

    def test_index(self):
        response = self.client.get(self.author_index.url)

        self.assertEqual(self.author_index.title, "Authors")
        self.assertContains(
            response,
            text=self.profile.name,
            status_code=200,
        )


    # def test_profile_route(self)
    #     profile = profile_factory.ProfileFactory()


class TestResearchDetailLink(test.TestCase):
    def test_clean_with_url(self):
        link = research_factory.ResearchDetailLinkFactory.build(with_url=True)

        link.clean()

        self.assertTrue(link.url)
        self.assertFalse(link.document)

    def test_clean_with_doc(self):
        link = research_factory.ResearchDetailLinkFactory.build(with_document=True)

        link.clean()

        self.assertTrue(link.document)
        self.assertFalse(link.url)

    def test_clean_with_url_and_doc(self):
        link = research_factory.ResearchDetailLinkFactory.build(
            with_url=True,
            with_document=True,
        )

        with self.assertRaises(exceptions.ValidationError):
            link.clean()

    def test_clean_with_neither_url_nor_doc(self):
        link = research_factory.ResearchDetailLinkFactory.build()

        with self.assertRaises(exceptions.ValidationError):
            link.clean()
