from django.utils import translation

from legacy_cms.wagtailpages.factory import profiles as profiles_factory
from legacy_cms.wagtailpages.factory.libraries.rcc import (
    detail_page as detail_page_factory,
)
from legacy_cms.wagtailpages.factory.libraries.rcc import relations as relations_factory
from legacy_cms.wagtailpages.factory.libraries.rcc import (
    taxonomies as taxonomies_factory,
)
from legacy_cms.wagtailpages.pagemodels.libraries.rcc import forms
from legacy_cms.wagtailpages.pagemodels.libraries.rcc.forms import (
    RCCLibraryPageFilterForm,
)
from legacy_cms.wagtailpages.tests.libraries.rcc import base as rcc_test_base
from legacy_cms.wagtailpages.tests.libraries.rcc import utils as rcc_test_utils


class TestFormUtilitiesFunctions(rcc_test_base.RCCTestCase):
    def test_rcc_author_profile_obtained_by_get_author_options(self):
        detail_page = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
        )

        author_options = forms._get_author_options()
        author_option_values = [i for i, _ in author_options]

        self.assertIn(
            detail_page.authors.first().author_profile.id,
            author_option_values,
        )

    def test_non_rcc_author_profile_not_obtained_by_get_author_options(self):
        profile = profiles_factory.ProfileFactory()

        author_options = forms._get_author_options()
        author_option_values = [i for i, _ in author_options]

        self.assertNotIn(
            profile.id,
            author_option_values,
        )

    def test_rcc_author_in_context_aliased_detail_page_fr(self):
        """
        After the treesync, there are alias pages in the non-default locales. But,
        before the pages are translated (a manual action) the related models like author
        are still the ones from the default locale.
        """
        detail_page_en = detail_page_factory.RCCDetailPageFactory(
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

    def test_rcc_author_in_context_translated_detail_page_fr(self):
        """
        When a profile for the active locale exists, pass that one to the context.

        Profiles are not necessarily people, so they might have translated names.
        """
        detail_page_en = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
        )
        profile_en = detail_page_en.authors.first().author_profile
        self.synchronize_tree()
        detail_page_fr = rcc_test_utils.translate_detail_page(detail_page_en, self.fr_locale)
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

    def test_rcc_topics_in_options(self):
        topic_1 = taxonomies_factory.RCCTopicFactory()
        topic_2 = taxonomies_factory.RCCTopicFactory()

        topic_options = forms._get_topic_options()
        topic_option_values = [i for i, _ in topic_options]

        self.assertEqual(len(topic_option_values), 2)
        self.assertIn(topic_1.id, topic_option_values)
        self.assertIn(topic_2.id, topic_option_values)

    def test_rcc_content_types_in_options(self):
        content_type_1 = taxonomies_factory.RCCContentTypeFactory()
        content_type_2 = taxonomies_factory.RCCContentTypeFactory()

        content_type_options = forms._get_content_type_options()
        content_type_option_values = [i for i, _ in content_type_options]

        self.assertEqual(len(content_type_option_values), 2)
        self.assertIn(content_type_1.id, content_type_option_values)
        self.assertIn(content_type_2.id, content_type_option_values)

    def test_rcc_curricular_areas_in_options(self):
        curricular_area_1 = taxonomies_factory.RCCCurricularAreaFactory()
        curricular_area_2 = taxonomies_factory.RCCCurricularAreaFactory()

        curricular_area_options = forms._get_curricular_area_options()
        curricular_area_option_values = [i for i, _ in curricular_area_options]

        self.assertEqual(len(curricular_area_option_values), 2)
        self.assertIn(curricular_area_1.id, curricular_area_option_values)
        self.assertIn(curricular_area_2.id, curricular_area_option_values)

    def test_topic_in_options_matches_active_locale(self):
        topic_en = taxonomies_factory.RCCTopicFactory()
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

    def test_content_type_in_options_matches_active_locale(self):
        content_type_en = taxonomies_factory.RCCContentTypeFactory()
        content_type_fr = content_type_en.copy_for_translation(self.fr_locale)
        content_type_fr.save()

        # Activate the default locale
        translation.activate(self.default_locale.language_code)

        content_type_options_en = forms._get_content_type_options()
        content_type_option_values_en = [i for i, _ in content_type_options_en]
        self.assertEqual(len(content_type_option_values_en), 1)
        self.assertIn(content_type_en.id, content_type_option_values_en)
        self.assertNotIn(content_type_fr.id, content_type_option_values_en)

        # Activate the French locale
        translation.activate(self.fr_locale.language_code)

        content_type_options_fr = forms._get_content_type_options()
        content_type_option_values_fr = [i for i, _ in content_type_options_fr]
        self.assertEqual(len(content_type_option_values_fr), 1)
        self.assertNotIn(content_type_en.id, content_type_option_values_fr)
        self.assertIn(content_type_fr.id, content_type_option_values_fr)

    def test_curricular_area_in_options_matches_active_locale(self):
        curricular_area_en = taxonomies_factory.RCCCurricularAreaFactory()
        curricular_area_fr = curricular_area_en.copy_for_translation(self.fr_locale)
        curricular_area_fr.save()

        # Activate the default locale
        translation.activate(self.default_locale.language_code)

        curricular_area_options_en = forms._get_curricular_area_options()
        curricular_area_option_values_en = [i for i, _ in curricular_area_options_en]
        self.assertEqual(len(curricular_area_option_values_en), 1)
        self.assertIn(curricular_area_en.id, curricular_area_option_values_en)
        self.assertNotIn(curricular_area_fr.id, curricular_area_option_values_en)

        # Activate the French locale
        translation.activate(self.fr_locale.language_code)

        curricular_area_options_fr = forms._get_curricular_area_options()
        curricular_area_option_values_fr = [i for i, _ in curricular_area_options_fr]
        self.assertEqual(len(curricular_area_option_values_fr), 1)
        self.assertNotIn(curricular_area_en.id, curricular_area_option_values_fr)
        self.assertIn(curricular_area_fr.id, curricular_area_option_values_fr)

    def test_localized_topic_options(self):
        """
        Use active locales version of topic if available.

        If no translation is available for a given topic, display the default locale
        topic.

        """
        topic_1_en = taxonomies_factory.RCCTopicFactory()
        topic_1_fr = topic_1_en.copy_for_translation(self.fr_locale)
        topic_1_fr.save()
        topic_2_en = taxonomies_factory.RCCTopicFactory()
        translation.activate(self.fr_locale.language_code)

        topic_options = forms._get_topic_options()
        topic_option_values = [i for i, _ in topic_options]

        self.assertEqual(len(topic_option_values), 2)
        self.assertNotIn(topic_1_en.id, topic_option_values)
        self.assertIn(topic_1_fr.id, topic_option_values)
        self.assertIn(topic_2_en.id, topic_option_values)

    def test_localized_content_type_options(self):
        """
        Use active locales version of content type if available.

        If no translation is available for a given content type, display the default locale
        content type.

        """
        content_type_1_en = taxonomies_factory.RCCContentTypeFactory()
        content_type_1_fr = content_type_1_en.copy_for_translation(self.fr_locale)
        content_type_1_fr.save()
        content_type_2_en = taxonomies_factory.RCCContentTypeFactory()
        translation.activate(self.fr_locale.language_code)

        content_type_options = forms._get_content_type_options()
        content_type_option_values = [i for i, _ in content_type_options]

        self.assertEqual(len(content_type_option_values), 2)
        self.assertNotIn(content_type_1_en.id, content_type_option_values)
        self.assertIn(content_type_1_fr.id, content_type_option_values)
        self.assertIn(content_type_2_en.id, content_type_option_values)

    def test_localized_curricular_area_options(self):
        """
        Use active locales version of curricular area if available.

        If no translation is available for a given curricular area, display the default locale
        curricular area.

        """
        curricular_area_1_en = taxonomies_factory.RCCCurricularAreaFactory()
        curricular_area_1_fr = curricular_area_1_en.copy_for_translation(self.fr_locale)
        curricular_area_1_fr.save()
        curricular_area_2_en = taxonomies_factory.RCCCurricularAreaFactory()
        translation.activate(self.fr_locale.language_code)

        curricular_area_options = forms._get_curricular_area_options()
        curricular_area_option_values = [i for i, _ in curricular_area_options]

        self.assertEqual(len(curricular_area_option_values), 2)
        self.assertNotIn(curricular_area_1_en.id, curricular_area_option_values)
        self.assertIn(curricular_area_1_fr.id, curricular_area_option_values)
        self.assertIn(curricular_area_2_en.id, curricular_area_option_values)


class RCCLibraryPageFilterFormTestCase(rcc_test_base.RCCTestCase):
    def test_form_content_types(self):
        """Test that the form content types field is populated with the correct choices."""
        content_types = taxonomies_factory.RCCContentTypeFactory.create_batch(size=3)
        form = RCCLibraryPageFilterForm()
        self.assertCountEqual(form.fields["content_types"].choices, [(ct.id, ct.name) for ct in content_types])

    def test_form_curricular_areas(self):
        """Test that the form curricular areas field is populated with the correct choices."""
        curricular_areas = taxonomies_factory.RCCCurricularAreaFactory.create_batch(size=3)
        form = RCCLibraryPageFilterForm()
        self.assertCountEqual(form.fields["curricular_areas"].choices, [(ca.id, ca.name) for ca in curricular_areas])

    def test_form_topics(self):
        """Test that the form topics field is populated with the correct choices."""
        topics = taxonomies_factory.RCCTopicFactory.create_batch(size=3)
        form = RCCLibraryPageFilterForm()
        self.assertCountEqual(form.fields["topics"].choices, [(t.id, t.name) for t in topics])

    def test_form_authors(self):
        """Test that the form authors field is populated with the correct choices."""
        contributors = profiles_factory.ProfileFactory.create_batch(size=3)
        detail_page = detail_page_factory.RCCDetailPageFactory(
            parent=self.library_page,
            authors=[],
        )

        for contributor in contributors:
            relations_factory.RCCAuthorRelationFactory(
                detail_page=detail_page,
                author_profile=contributor,
            )

        form = RCCLibraryPageFilterForm()
        self.assertCountEqual(form.fields["authors"].choices, [(c.id, c.name) for c in contributors])
