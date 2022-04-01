import datetime
import http

from django import test
from django.core import exceptions
from django.utils import text as text_utils
from django.utils import translation
from wagtail.core import models as wagtail_models
from wagtail_localize import synctree

from networkapi.wagtailpages.factory import research_hub as research_factory
from networkapi.wagtailpages.factory import homepage as home_factory
from networkapi.wagtailpages.factory import profiles as profile_factory


class TestResearchAuthorIndexPage(test.TestCase):
    @classmethod
    def setUpTestData(cls):
        cls._setup_homepage()
        cls.landing_page = research_factory.ResearchLandingPageFactory(
            parent=cls.homepage,
        )
        cls.library_page = research_factory.ResearchLibraryPageFactory(
            parent=cls.landing_page,
        )
        cls.author_index = research_factory.ResearchAuthorsIndexPageFactory(
            parent=cls.landing_page,
            title="Authors",
        )

        # Profile associated with a research detail page
        cls.detail_page = research_factory.ResearchDetailPageFactory(
            parent=cls.library_page,
            original_publication_date=(
                datetime.date.today() - datetime.timedelta(days=14)
            ),

        )
        cls.research_profile = profile_factory.ProfileFactory()
        research_factory.ResearchAuthorRelationFactory(
            research_detail_page=cls.detail_page,
            author_profile=cls.research_profile,
        )

        cls.non_research_profile = profile_factory.ProfileFactory()

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

    def _setup_synchronized_tree(self):
        # Set up additional locale
        self.default_locale = wagtail_models.Locale.get_default()
        self.assertEqual(self.research_profile.locale, self.default_locale)
        self.active_locale = wagtail_models.Locale.get_active()
        self.assertEqual(self.active_locale, self.default_locale)
        self.fr_locale, _ = wagtail_models.Locale.objects.get_or_create(
            language_code='fr'
        )
        self.assertNotEqual(self.fr_locale, self.default_locale)

        # Translate the pages
        synctree.synchronize_tree(
            source_locale=self.default_locale,
            target_locale=self.fr_locale
        )

    def _translate_research_profile(self):
        # Translate profile and set it as author on the translated detail. This is what
        # happens when you work in the localize UI.
        self.fr_profile = self.research_profile.copy_for_translation(self.fr_locale)
        self.fr_profile.save()
        self.fr_detail = self.detail_page.get_translation(self.fr_locale)
        self.fr_detail_author = self.fr_detail.research_authors.first()
        self.fr_detail_author.author_profile = self.fr_profile
        self.fr_detail_author.save()

    def test_get_context(self):
        context = self.author_index.get_context(request=None)

        self.assertIn(self.research_profile, context['author_profiles'])
        # Non-research profile should not show up
        self.assertNotIn(self.non_research_profile, context['author_profiles'])

    def test_get_context_default_locale(self):
        self._setup_synchronized_tree()
        self._translate_research_profile()

        # Get context when default is active
        context = self.author_index.localized.get_context(request=None)

        self.assertIn(self.research_profile, context['author_profiles'])
        self.assertNotIn(self.fr_profile, context['author_profiles'])

    def test_get_context_fr_locale(self):
        self._setup_synchronized_tree()
        self._translate_research_profile()
        translation.activate('fr')

        # Get context when fr is active
        fr_context = self.author_index.localized.get_context(request=None)

        self.assertNotIn(self.research_profile, fr_context['author_profiles'])
        self.assertIn(self.fr_profile, fr_context['author_profiles'])

    def test_get_context_fr_locale_profile_not_translated(self):
        self._setup_synchronized_tree()
        translation.activate('fr')

        fr_context = self.author_index.localized.get_context(request=None)

        # When the profile is not translated, the default locales profile should show
        self.assertIn(self.research_profile, fr_context['author_profiles'])

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

    def test_get_author_detail_context(self):
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

        with self.assertNumQueries(2):
            context = self.author_index.get_author_detail_context(
                profile_id=self.research_profile.id,
            )

            self.assertEqual(context['author_profile'], self.research_profile)
            self.assertEqual(len(context['latest_research']), 3)
            self.assertIn(detail_page_1, context['latest_research'])
            self.assertIn(detail_page_2, context['latest_research'])
            self.assertIn(detail_page_3, context['latest_research'])
            self.assertNotIn(self.detail_page, context['latest_research'])


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
