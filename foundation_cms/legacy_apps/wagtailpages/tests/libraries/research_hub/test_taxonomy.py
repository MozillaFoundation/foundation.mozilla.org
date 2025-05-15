from django.db.utils import IntegrityError

from foundation_cms.legacy_apps.wagtailpages.factory.libraries.research_hub import (
    taxonomies as taxonomies_factory,
)
from foundation_cms.legacy_apps.wagtailpages.tests.libraries.research_hub import base


class ResearchTaxonomyTestCase(base.ResearchHubTestCase):
    """
    Test case for the ResearchTaxonomy model.
    Since the BaseTaxonomy model is abstract, this test case focuses on
    testing the concrete ResearchTaxonomy model.

    This test case inherits from `base.ResearchHubTestCase` and focuses on testing the ResearchTaxonomy model.

    Methods:
    - test_str_representation: Test the string representation of a ResearchTopic instance.
    - test_validate_unique: Test the uniqueness validation of a ResearchTopic instance.

    Note: This test case assumes the availability of the `taxonomies_factory.ResearchTopicFactory`
    for creating test instances.
    """

    def test_str_representation(self):
        """
        Test the string representation of a ResearchTopic instance.

        The test creates a ResearchTopic instance using the factory with a specific name and slug.
        It then asserts that the string representation of the instance matches the provided name.
        """
        taxonomy = taxonomies_factory.ResearchTopicFactory(name="Category", slug="category")

        self.assertEqual(str(taxonomy), "Category")

    def test_validate_unique(self):
        """
        Test the uniqueness validation of a ResearchTopic instance.

        The test creates a taxonomy instance with a unique combination of name and slug.
        It then creates another taxonomy instance with the same name and slug but in a different locale,
        and asserts that the validation passes, indicating uniqueness.

        Next, it attempts to create another taxonomy instance with the same name and slug in the same locale,
        expecting an IntegrityError to be raised. The test validates that the exception is raised correctly.
        """

        # Creating a taxonomy with a unique combination of name and slug
        taxonomies_factory.ResearchTopicFactory(name="Category", slug="category", locale=self.default_locale)

        # Creating a taxonomy with the same name and slug in a different locale
        taxonomy_fr = taxonomies_factory.ResearchTopicFactory(name="Category", slug="category", locale=self.fr_locale)
        self.assertIsNone(taxonomy_fr.validate_unique())

        # Creating a taxonomy with the same name and slug in the same locale
        with self.assertRaises(IntegrityError):
            taxonomy_duplicate = taxonomies_factory.ResearchTopicFactory(
                name="Category", slug="category", locale=self.default_locale
            )
            taxonomy_duplicate.validate_unique()
