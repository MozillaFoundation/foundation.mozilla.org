import datetime

from django.utils import timezone, translation

from legacy_cms.wagtailpages.factory import profiles as profiles_factory
from legacy_cms.wagtailpages.factory.libraries.research_hub import (
    detail_page as detail_page_factory,
)
from legacy_cms.wagtailpages.factory.libraries.research_hub import (
    relations as relations_factory,
)
from legacy_cms.wagtailpages.factory.libraries.research_hub import (
    taxonomies as taxonomies_factory,
)
from legacy_cms.wagtailpages.pagemodels.libraries.research_hub import forms
from legacy_cms.wagtailpages.pagemodels.libraries.research_hub.forms import (
    ResearchLibraryPageFilterForm,
)
from legacy_cms.wagtailpages.tests.libraries.research_hub import (
    base as research_test_base,
)
from legacy_cms.wagtailpages.tests.libraries.research_hub import (
    utils as research_test_utils,
)


class TestFormUtilitiesFunctions(research_test_base.ResearchHubTestCase):
    def test_research_author_profile_obtained_by_get_author_options(self):
        detail_page = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
        )

        author_options = forms._get_author_options()
        author_option_values = [i for i, _ in author_options]

        self.assertIn(
            detail_page.authors.first().author_profile.id,
            author_option_values,
        )

    def test_non_research_author_profile_not_obtained_by_get_author_options(self):
        profile = profiles_factory.ProfileFactory()

        author_options = forms._get_author_options()
        author_option_values = [i for i, _ in author_options]

        self.assertNotIn(
            profile.id,
            author_option_values,
        )

    def test_research_author_in_context_aliased_detail_page_fr(self):
        """
        After the treesync, there are alias pages in the non-default locales. But,
        before the pages are translated (a manual action) the related models like author
        are still the ones from the default locale.
        """
        detail_page_en = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
        )
        profile_en = detail_page_en.authors.first().author_profile
        self.synchronize_tree()
        translation.activate(self.fr_locale.language_code)

        author_options = forms._get_author_options()
        author_option_values = [i for i, _ in author_options]

        self.assertIn(
            profile_en.id,
            author_option_values,
        )

    def test_research_author_in_context_translated_detail_page_fr(self):
        """
        When a profile for the active locale exists, pass that one to the context.

        Profiles are not necessarily people, so they might have translated names.
        """
        detail_page_en = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
        )
        profile_en = detail_page_en.authors.first().author_profile
        self.synchronize_tree()
        detail_page_fr = research_test_utils.translate_detail_page(detail_page_en, self.fr_locale)
        profile_fr = detail_page_fr.authors.first().author_profile
        translation.activate(self.fr_locale.language_code)

        author_options = forms._get_author_options()
        author_option_values = [i for i, _ in author_options]

        self.assertNotIn(
            profile_en.id,
            author_option_values,
        )
        self.assertIn(
            profile_fr.id,
            author_option_values,
        )

    def test_research_topics_in_options(self):
        topic_1 = taxonomies_factory.ResearchTopicFactory()
        topic_2 = taxonomies_factory.ResearchTopicFactory()

        topic_options = forms._get_topic_options()
        topic_option_values = [i for i, _ in topic_options]

        self.assertEqual(len(topic_option_values), 2)
        self.assertIn(topic_1.id, topic_option_values)
        self.assertIn(topic_2.id, topic_option_values)

    def test_topic_in_options_matches_active_locale(self):
        topic_en = taxonomies_factory.ResearchTopicFactory()
        topic_fr = topic_en.copy_for_translation(self.fr_locale)
        topic_fr.save()

        # Activate the default locale
        translation.activate(self.default_locale.language_code)

        topic_options_en = forms._get_topic_options()
        topic_option_values_en = [i for i, _ in topic_options_en]
        self.assertEqual(len(topic_option_values_en), 1)
        self.assertIn(topic_en.id, topic_option_values_en)
        self.assertNotIn(topic_fr.id, topic_option_values_en)

        # Activate the French locale
        translation.activate(self.fr_locale.language_code)

        topic_options_fr = forms._get_topic_options()
        topic_option_values_fr = [i for i, _ in topic_options_fr]
        self.assertEqual(len(topic_option_values_fr), 1)
        self.assertNotIn(topic_en.id, topic_option_values_fr)
        self.assertIn(topic_fr.id, topic_option_values_fr)

    def test_localized_topic_options(self):
        """
        Use active locales version of topic if available.

        If no translation is available for a given topic, display the default locale
        topic.

        """
        topic_1_en = taxonomies_factory.ResearchTopicFactory()
        topic_1_fr = topic_1_en.copy_for_translation(self.fr_locale)
        topic_1_fr.save()
        topic_2_en = taxonomies_factory.ResearchTopicFactory()
        translation.activate(self.fr_locale.language_code)

        topic_options = forms._get_topic_options()
        topic_option_values = [i for i, _ in topic_options]

        self.assertEqual(len(topic_option_values), 2)
        self.assertNotIn(topic_1_en.id, topic_option_values)
        self.assertIn(topic_1_fr.id, topic_option_values)
        self.assertIn(topic_2_en.id, topic_option_values)

    def test_research_regions_in_options(self):
        region_1 = taxonomies_factory.ResearchRegionFactory()
        region_2 = taxonomies_factory.ResearchRegionFactory()

        region_options = forms._get_region_options()
        region_option_values = [i for i, _ in region_options]

        self.assertEqual(len(region_option_values), 2)
        self.assertIn(region_1.id, region_option_values)
        self.assertIn(region_2.id, region_option_values)

    def test_region_in_options_matches_active_locale(self):
        region_en = taxonomies_factory.ResearchRegionFactory()
        region_fr = region_en.copy_for_translation(self.fr_locale)
        region_fr.save()

        # Activate the default locale
        translation.activate(self.default_locale.language_code)

        region_options_en = forms._get_region_options()
        region_option_values_en = [i for i, _ in region_options_en]
        self.assertEqual(len(region_option_values_en), 1)
        self.assertIn(region_en.id, region_option_values_en)
        self.assertNotIn(region_fr.id, region_option_values_en)

        # Activate the French locale
        translation.activate(self.fr_locale.language_code)

        region_options_fr = forms._get_region_options()
        region_option_values_fr = [i for i, _ in region_options_fr]
        self.assertEqual(len(region_option_values_fr), 1)
        self.assertNotIn(region_en.id, region_option_values_fr)
        self.assertIn(region_fr.id, region_option_values_fr)

    def test_years_in_options(self):
        year_1 = timezone.now().year
        year_2 = year_1 - 1
        detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            original_publication_date=datetime.date(year=year_1, month=1, day=1),
        )
        detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            original_publication_date=datetime.date(year=year_2, month=1, day=1),
        )

        year_options = forms._get_year_options()
        year_option_values = [i for i, _ in year_options]

        # It's 3 options because of the two years and the "any" option.
        self.assertEqual(len(year_option_values), 3)
        self.assertIn(year_1, year_option_values)
        self.assertIn(year_2, year_option_values)


class ResearchLibraryPageFilterFormTestCase(research_test_base.ResearchHubTestCase):
    def test_form_topics(self):
        """Test that the form topics field is populated with the correct choices."""
        topics = taxonomies_factory.ResearchTopicFactory.create_batch(size=3)
        form = ResearchLibraryPageFilterForm()
        self.assertCountEqual(form.fields["topics"].choices, [(t.id, t.name) for t in topics])

    def test_form_years(self):
        """Test that the form year field is populated with the correct choices."""
        years = [timezone.now().year, timezone.now().year - 1]
        detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            original_publication_date=datetime.date(year=years[0], month=1, day=1),
        )
        detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            original_publication_date=datetime.date(year=years[1], month=1, day=1),
        )

        form = ResearchLibraryPageFilterForm()
        self.assertCountEqual(form.fields["year"].choices, [("", "Any")] + [(y, y) for y in years])

    def test_form_regions(self):
        """Test that the form regions field is populated with the correct choices."""
        regions = taxonomies_factory.ResearchRegionFactory.create_batch(size=3)
        form = ResearchLibraryPageFilterForm()
        self.assertCountEqual(form.fields["regions"].choices, [(r.id, r.name) for r in regions])

    def test_form_authors(self):
        """Test that the form authors field is populated with the correct choices."""
        authors = profiles_factory.ProfileFactory.create_batch(size=3)
        detail_page = detail_page_factory.ResearchDetailPageFactory(
            parent=self.library_page,
            authors=[],
        )

        for author in authors:
            relations_factory.ResearchAuthorRelationFactory(
                detail_page=detail_page,
                author_profile=author,
            )

        form = ResearchLibraryPageFilterForm()
        self.assertCountEqual(form.fields["authors"].choices, [(a.id, a.name) for a in authors])
