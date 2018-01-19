from datetime import datetime, timezone
from django.test import TestCase

from networkapi.people.factory import (
    InternetHealthIssueFactory,
    PersonFactory,
    AffiliationFactory,
)

from networkapi.people.models import (
    InternetHealthIssue,
    Person,
    Affiliation
)


class TestPersonFactory(TestCase):
    """
    Test PersonFactory
    """

    def test_person_creation(self):
        """
        PersonFactory should not raise and exception when generating a model instance
        """

        PersonFactory.create()

    def test_person_return_value(self):
        """
        PersonFactory should return an instance of Person
        """

        person = PersonFactory.create()

        self.assertIsInstance(person, Person)

    def test_person_featured_param(self):
        """
        The is_featured kwarg should set featured to True
        """

        person = PersonFactory.create(is_featured=True)

        self.assertEqual(person.featured, True)

    def test_person_unpublished_param(self):
        """
        The unpublished kwarg should set the publish_after date to sometime
        in the future
        """

        person = PersonFactory.create(unpublished=True)

        self.assertGreater(person.publish_after, datetime.now(tz=timezone.utc))

    def test_person_has_expiry_param(self):
        """
        The has_expiry kwarg should set the expires date to sometime in the
        future
        """

        person = PersonFactory.create(has_expiry=True)

        self.assertGreater(person.expires, datetime.now(tz=timezone.utc))

    def test_person_expired_param(self):
        """
        The expired kwarg should set the expires date to sometime in the
        past
        """

        person = PersonFactory.create(expired=True)

        self.assertLess(person.expires, datetime.now(tz=timezone.utc))


class TestInternetHealthIssueFactory(TestCase):
    """
    Test InternetHealthIssueFactory
    """

    def test_internet_health_issue_creation(self):
        """
        InternetHealthIssueFactory should not raise an exception
        """

        InternetHealthIssueFactory.create()

    def test_internet_health_issue_return_value(self):
        """
        InternetHealthIssueFactory should return an instance of InternetHealthIssue
        """

        issue = InternetHealthIssueFactory.create()

        self.assertIsInstance(issue, InternetHealthIssue)


class TestAffiliationFactory(TestCase):
    """
    Test AffiliationFactory
    """

    def test_affiliation_creation(self):
        """
        AffiliationFactory should not raise an exception
        """

        AffiliationFactory.create()

    def test_affiliation_return_value(self):
        """
        AffiliationFactory should return an instance of Affiliation
        """

        affiliation = AffiliationFactory.create()

        self.assertIsInstance(affiliation, Affiliation)
