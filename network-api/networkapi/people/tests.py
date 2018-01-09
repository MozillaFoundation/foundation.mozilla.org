from datetime import datetime
from django.test import TestCase

from networkapi.utility.utc import UTC
from networkapi.people.factory import (
    InternetHealthIssueFactory,
    PersonFactory,
    AffiliationFactory,
)

utc = UTC()


class TestPersonFactory(TestCase):
    """
    Test PersonFactory
    """

    def test_person_creation(self):
        """
        Creating a person with the PersonFactory contructor should not raise
        an exception
        """

        person = PersonFactory()

        self.assertIsNotNone(person)

    def test_person_creation_defaults(self):
        """
        Verify the default values applied to a Person generated through the
        PersonFactory constructor
        """

        person = PersonFactory()

        self.assertIsNotNone(person.name)
        self.assertIsNotNone(person.role)
        self.assertIsNotNone(person.location)
        self.assertIsNotNone(person.quote)
        self.assertIsNotNone(person.bio)
        self.assertIsNotNone(person.image)
        self.assertIsNotNone(person.partnership_logo)
        self.assertIsNotNone(person.twitter_url)
        self.assertIsNotNone(person.linkedin_url)
        self.assertIsNotNone(person.interview_url)
        self.assertIsNotNone(person.publish_after)
        self.assertLess(person.publish_after, datetime.now(tz=utc))
        self.assertEqual(person.featured, False)
        self.assertEqual(person.internet_health_issues.count(), 0)

    def test_person_featured_param(self):
        """
        The is_featured kwarg should set featured to True
        """

        person = PersonFactory(is_featured=True)

        self.assertEqual(person.featured, True)

    def test_person_unpublished_param(self):
        """
        The unpublished kwarg should set the publish_after date to sometime
        in the future
        """

        person = PersonFactory(unpublished=True)

        self.assertGreater(person.publish_after, datetime.now(tz=utc))

    def test_person_has_expiry_param(self):
        """
        The has_expiry kwarg should set the expires date to sometime in the
        future
        """

        person = PersonFactory(has_expiry=True)

        self.assertGreater(person.expires, datetime.now(tz=utc))

    def test_person_expired_param(self):
        """
        The expired kwarg should set the expires date to sometime in the
        past
        """

        person = PersonFactory(expired=True)

        self.assertLess(person.expires, datetime.now(tz=utc))


class TestInternetHealthIssueFactory(TestCase):
    """
    Test InternetHealthIssueFactory
    """

    def test_internet_health_issue_creation(self):
        """
        Creating an Internet Health Issue using the Factory constructor should
        not raise an exception
        """

        issue = InternetHealthIssueFactory()

        self.assertIsNotNone(issue)


class TestAffiliationFactory(TestCase):
    """
    Test AffiliationFactory
    """

    def test_affiliation_creation(self):
        """
        Creating an Affiliation using the Factory should not raise an
        exception
        """

        affiliation = AffiliationFactory()

        self.assertIsNotNone(affiliation)

    def test_affiliation_person_arg(self):
        """
        The AffiliationFactory constructor should be able to set attributes
        on the SubFactory
        """

        affiliation = AffiliationFactory(
            person__is_featured=True
        )

        self.assertEqual(affiliation.person.featured, True)