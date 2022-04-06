import datetime
import http

from django import test
from django.core import exceptions
from django.utils import text as text_utils
from django.utils import translation
from wagtail.core import models as wagtail_models
from wagtail_localize import synctree

from networkapi.wagtailpages.factory import homepage as home_factory
from networkapi.wagtailpages.factory import profiles as profiles_factory
from networkapi.wagtailpages.factory import research_hub as research_factory


class ResearchHubTestCase(test.TestCase):
    @classmethod
    def setUpTestData(cls):
        cls._setup_homepage()
        cls._setup_research_hub_structure(homepage=cls.homepage)
        cls._setup_locales()

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

    @classmethod
    def _setup_research_hub_structure(cls, homepage):
        cls.landing_page = research_factory.ResearchLandingPageFactory(
            parent=homepage,
        )
        cls.library_page = research_factory.ResearchLibraryPageFactory(
            parent=cls.landing_page,
        )
        cls.author_index = research_factory.ResearchAuthorsIndexPageFactory(
            parent=cls.landing_page,
            title='Authors',
        )

    @classmethod
    def _setup_locales(cls):
        cls.default_locale = wagtail_models.Locale.get_default()
        cls.fr_locale, _ = wagtail_models.Locale.objects.get_or_create(
            language_code='fr'
        )
        assert cls.fr_locale != cls.default_locale

    def setUp(self):
        self.synchronize_tree()

    def synchronize_tree(self):
        synctree.synchronize_tree(
            source_locale=self.default_locale,
            target_locale=self.fr_locale
        )


class TestResearchAuthorIndexPage(ResearchHubTestCase):
    @classmethod
    def setUpTestData(cls):
        super().setUpTestData()
        cls.detail_page = research_factory.ResearchDetailPageFactory(
            parent=cls.library_page,
            original_publication_date=(
                datetime.date.today() - datetime.timedelta(days=14)
            ),

        )
        cls.research_profile = profiles_factory.ProfileFactory()
        research_factory.ResearchAuthorRelationFactory(
            research_detail_page=cls.detail_page,
            author_profile=cls.research_profile,
        )

        cls.non_research_profile = profiles_factory.ProfileFactory()

    def setUp(self):
        super().setUp()
        translation.activate(self.default_locale.language_code)
        self.fr_detail_page = self.detail_page.get_translation(self.fr_locale)

    def translate_research_profile(self):
        self.fr_profile = self.research_profile.copy_for_translation(self.fr_locale)
        self.fr_profile.save()

    def translate_detail_page(self):
        """
        Simulate click on the "translate this page" button in the Wagtail admin.

        The tree synchronzion creates page aliases with the new locale. But, at the
        alias stage, the pages are not really translated yet. E.g. inline panels
        like the research author are not translated until the "translate this page"
        button is clicked in the admin. That means, until the "manual" action of
        clicking the button is taken, the alias page is still associated with the
        profile for the default locale.

        This method simulates the manual click on the "translate this page" button.
        That action removes the alias and sets associates the profile with the
        translated profile.

        """
        if not hasattr(self, "fr_profile"):
            self.translate_research_profile()

        fr_research_author = self.fr_detail_page.research_authors.first()
        fr_research_author.author_profile = self.fr_profile
        fr_research_author.save()
        self.fr_detail_page.alias_of = None
        self.fr_detail_page.save()

    def test_get_context(self):
        context = self.author_index.get_context(request=None)
        self.translate_research_profile()

        self.assertIn(self.research_profile, context['author_profiles'])
        # Non-research profile should not show up
        self.assertNotIn(self.non_research_profile, context['author_profiles'])
        # Translated profile should not show up
        self.assertNotIn(self.fr_profile, context['author_profiles'])

    def test_get_context_fr_locale_detail_alias(self):
        translation.activate(self.fr_locale.language_code)

        fr_context = self.author_index.localized.get_context(request=None)

        # When the profile is not translated, the default locales profile should show
        self.assertIn(self.research_profile, fr_context['author_profiles'])

    def test_get_context_fr_locale_detail_translated(self):
        self.translate_detail_page()
        translation.activate(self.fr_locale.language_code)

        # Get context when fr is active
        fr_context = self.author_index.localized.get_context(request=None)

        self.assertNotIn(self.research_profile, fr_context['author_profiles'])
        self.assertIn(self.fr_profile, fr_context['author_profiles'])

    def test_profile_route(self):
        profile_slug = text_utils.slugify(self.research_profile.name)
        url = (
            f'{ self.author_index.url }'
            f'{ self.research_profile.id }/{ profile_slug }/'
        )

        response = self.client.get(url)

        self.assertContains(
            response,
            text=self.research_profile.name,
            status_code=http.HTTPStatus.OK,
        )

    def test_profile_route_wrong_id(self):
        profile_slug = text_utils.slugify(self.research_profile.name)
        url = (
            f'{ self.author_index.url }'
            f'{ self.research_profile.id + 1 }/{ profile_slug }/'
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, http.HTTPStatus.NOT_FOUND)

    def test_profile_route_wrong_name(self):
        profile_slug = text_utils.slugify(self.research_profile.name + 'a')
        url = (
            f'{ self.author_index.url }'
            f'{ self.research_profile.id }/{ profile_slug }/'
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, http.HTTPStatus.NOT_FOUND)

    def test_profile_route_with_non_research_profile(self):
        profile_slug = text_utils.slugify(self.non_research_profile.name)
        url = (
            f'{ self.author_index.url }'
            f'{ self.non_research_profile.id }/{ profile_slug }/'
        )

        response = self.client.get(url)

        self.assertEqual(response.status_code, http.HTTPStatus.NOT_FOUND)

    def test_get_author_detail_context_multiple_detail_pages(self):
        detail_page_1 = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            original_publication_date=(
                datetime.date.today() - datetime.timedelta(days=3)
            ),
        )
        detail_page_2 = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            original_publication_date=(
                datetime.date.today() - datetime.timedelta(days=2)
            ),
        )
        detail_page_3 = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            original_publication_date=(
                datetime.date.today() - datetime.timedelta(days=1)
            ),
        )
        research_factory.ResearchAuthorRelationFactory(
            research_detail_page=detail_page_1,
            author_profile=self.research_profile,
        )
        research_factory.ResearchAuthorRelationFactory(
            research_detail_page=detail_page_2,
            author_profile=self.research_profile,
        )
        research_factory.ResearchAuthorRelationFactory(
            research_detail_page=detail_page_3,
            author_profile=self.research_profile,
        )

        # author, locale, detail pages.
        with self.assertNumQueries(3):
            context = self.author_index.get_author_detail_context(
                profile_id=self.research_profile.id,
            )

            self.assertEqual(context['author_profile'], self.research_profile)
            self.assertEqual(len(context['latest_research']), 3)
            self.assertIn(detail_page_1, context['latest_research'])
            self.assertIn(detail_page_2, context['latest_research'])
            self.assertIn(detail_page_3, context['latest_research'])
            self.assertNotIn(self.detail_page, context['latest_research'])

    def test_get_author_detail_context(self):
        context = self.author_index.localized.get_author_detail_context(
            profile_id=self.research_profile.id,
        )

        self.assertIn(self.detail_page, context['latest_research'])
        self.assertNotIn(self.fr_detail_page, context['latest_research'])

    def test_get_author_detail_context_fr_locale(self):
        translation.activate(self.fr_locale.language_code)
        # When page trees are automatically synced, but have not really been translated,
        # the profile is not translated. So even when the fr locale is active it will
        # use the original profile
        localized_research_profile = self.research_profile.localized
        self.assertEqual(localized_research_profile, self.research_profile)

        context = self.author_index.localized.get_author_detail_context(
            profile_id=localized_research_profile.id,
        )

        # The displayed detail pages should be the aliased pages not the original ones.
        self.assertNotIn(self.detail_page, context['latest_research'])
        self.assertIn(self.fr_detail_page, context['latest_research'])

    def test_get_author_detail_context_alias_and_translation(self):
        # There can be mixed situations, where only some research associated with
        # a profile is properly translated, but others are still only aliased.
        self.translate_detail_page()
        extra_detail_page = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
        )
        research_factory.ResearchAuthorRelationFactory(
            research_detail_page=extra_detail_page,
            author_profile=self.research_profile,
        )
        self.synchronize_tree()
        # Grab the alias page. Note: This page is not really translated, so it is still
        # associated with the original profile.
        fr_extra_detail_page = extra_detail_page.get_translation(self.fr_locale)
        # Check localized profile
        localized_research_profile = self.research_profile.localized
        self.assertEqual(localized_research_profile, self.research_profile)

        context = self.author_index.localized.get_author_detail_context(
            profile_id=localized_research_profile.id,
        )

        # We need to make sure that the displayed works are picked based on the active
        # locale, rather than the locale of the profile we are looking at
        self.assertIn(self.detail_page, context['latest_research'])
        self.assertIn(extra_detail_page, context['latest_research'])
        self.assertNotIn(self.fr_detail_page, context['latest_research'])
        self.assertNotIn(fr_extra_detail_page, context['latest_research'])

    def test_get_author_detail_context_fr_locale_alias_and_translation(self):
        # There can be mixed situations, where only some research associated with
        # a profile is properly translated, but others are still only aliased.
        self.translate_detail_page()
        extra_detail_page = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
        )
        research_factory.ResearchAuthorRelationFactory(
            research_detail_page=extra_detail_page,
            author_profile=self.research_profile,
        )
        synctree.synchronize_tree(
            source_locale=self.default_locale,
            target_locale=self.fr_locale
        )
        # Grab the alias page. Note: This page is not really translated, so it is still
        # associated with the original profile.
        fr_extra_detail_page = extra_detail_page.get_translation(self.fr_locale)
        # Activate locale
        translation.activate(self.fr_locale.language_code)
        localized_research_profile = self.research_profile.localized
        self.assertNotEqual(localized_research_profile, self.research_profile)

        context = self.author_index.localized.get_author_detail_context(
            profile_id=localized_research_profile.id,
        )

        # We need to make sure that the displayed works are picked based on the active
        # locale, rather than the locale of the profile we are looking at
        self.assertNotIn(self.detail_page, context['latest_research'])
        self.assertNotIn(extra_detail_page, context['latest_research'])
        self.assertIn(self.fr_detail_page, context['latest_research'])
        self.assertIn(fr_extra_detail_page, context['latest_research'])


class TestResearchLibraryPage(ResearchHubTestCase):
    def test_get_research_detail_pages(self):
        detail_page_1 = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
        )
        detail_page_2 = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
        )

        research_detail_pages = self.library_page.get_research_detail_pages()

        self.assertEqual(len(research_detail_pages), 2)
        self.assertIn(detail_page_1, research_detail_pages)
        self.assertIn(detail_page_2, research_detail_pages)

    def test_get_research_detail_pages_with_translation_aliases(self):
        detail_page_1 = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
        )
        detail_page_2 = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
        )
        self.synchronize_tree()
        fr_detail_page_1 = detail_page_1.get_translation(self.fr_locale)
        fr_detail_page_2 = detail_page_2.get_translation(self.fr_locale)

        research_detail_pages = self.library_page.get_research_detail_pages()

        self.assertEqual(len(research_detail_pages), 2)
        self.assertIn(detail_page_1, research_detail_pages)
        self.assertIn(detail_page_2, research_detail_pages)
        self.assertNotIn(fr_detail_page_1, research_detail_pages)
        self.assertNotIn(fr_detail_page_2, research_detail_pages)

    def test_get_research_detail_pages_search_by_title(self):
        # Fields other than title are empty to avoid accidental test failures due to
        # fake data generation.
        apple_page = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            title='Apple',
            introduction='',
            overview='',
            collaborators='',
        )
        banana_page = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            title='Banana',
            introduction='',
            overview='',
            collaborators='',
        )

        research_detail_pages = self.library_page.get_research_detail_pages(
            search='Apple',
        )

        self.assertEqual(len(research_detail_pages), 1)
        self.assertIn(apple_page, research_detail_pages)
        self.assertNotIn(banana_page, research_detail_pages)

    def test_get_research_detail_pages_search_by_introduction(self):
        apple_page = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            title='Cherry',
            introduction='Apple',
            overview='',
            collaborators='',
        )
        banana_page = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            title='Also cherry',
            introduction='Banana',
            overview='',
            collaborators='',
        )

        research_detail_pages = self.library_page.get_research_detail_pages(
            search='Apple',
        )

        self.assertEqual(len(research_detail_pages), 1)
        self.assertIn(apple_page, research_detail_pages)
        self.assertNotIn(banana_page, research_detail_pages)

    def test_get_research_detail_pages_search_by_overview(self):
        apple_page = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            title='Cherry',
            introduction='',
            overview='Apple',
            collaborators='',
        )
        banana_page = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            title='Also cherry',
            introduction='',
            overview='Banana',
            collaborators='',
        )

        research_detail_pages = self.library_page.get_research_detail_pages(
            search='Apple',
        )

        self.assertEqual(len(research_detail_pages), 1)
        self.assertIn(apple_page, research_detail_pages)
        self.assertNotIn(banana_page, research_detail_pages)

    def test_get_research_detail_pages_search_by_collaborators(self):
        apple_page = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            title='Cherry',
            introduction='',
            overview='',
            collaborators='Apple',
        )
        banana_page = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            title='Also cherry',
            introduction='',
            overview='',
            collaborators='Banana',
        )

        research_detail_pages = self.library_page.get_research_detail_pages(
            search='Apple',
        )

        self.assertEqual(len(research_detail_pages), 1)
        self.assertIn(apple_page, research_detail_pages)
        self.assertNotIn(banana_page, research_detail_pages)

    def test_get_research_detail_pages_search_by_author_name(self):
        '''
        Test detail page can be searched by author profile name.

        While it will also be possible to filter by author name, it would seem odd
        that the main author names can not be searched, while the collaborators can.
        '''
        apple_page = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            title='Cherry',
            introduction='',
            overview='',
            collaborators='',
        )
        apple_profile = profiles_factory.ProfileFactory(
            name='Apple',
            tagline='',
            introduction='',
        )
        research_factory.ResearchAuthorRelationFactory(
            research_detail_page=apple_page,
            author_profile=apple_profile
        )
        banana_page = research_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            title='Also cherry',
            introduction='',
            overview='',
            collaborators='',
        )
        banana_profile = profiles_factory.ProfileFactory(
            name='Banana',
            tagline='',
            introduction='',
        )
        research_factory.ResearchAuthorRelationFactory(
            research_detail_page=banana_page,
            author_profile=banana_profile
        )

        research_detail_pages = self.library_page.get_research_detail_pages(
            search='Apple',
        )

        self.assertEqual(len(research_detail_pages), 1)
        self.assertIn(apple_page, research_detail_pages)
        self.assertNotIn(banana_page, research_detail_pages)


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
