from django.contrib.auth.models import Group, User
from django.core.management import call_command
from django.test import TestCase


class DeleteNonStaffTest(TestCase):
    def setUp(self):
        User.objects.create(username="Alex"),

    def test_non_staff_is_deleted(self):
        """
        Simple users are deleted
        """

        call_command("delete_non_staff", "--now")

        self.assertEqual(User.objects.count(), 0)


class IsStaffNotDeletedTest(TestCase):
    def setUp(self):
        User.objects.create(username="Alex", is_staff=True)

    def test_is_staff_not_deleted(self):
        """
        Users with 'is_staff' flag at True are not deleted
        """

        call_command("delete_non_staff", "--now")

        self.assertEqual(User.objects.count(), 1)


class InGroupNotDeletedTest(TestCase):
    def setUp(self):
        group = Group.objects.create(name="TestGroup")
        group.user_set.create(username="Alex")

    def test_in_group_not_deleted(self):
        """
        Users in a group are not deleted
        """

        call_command("delete_non_staff", "--now")

        self.assertEqual(User.objects.count(), 1)


class MozillaFoundationUsersNotDeletedTest(TestCase):
    def setUp(self):
        User.objects.create(username="Alex", email="alex@mozillafoundation.org")

    def test_mozilla_foundation_users_not_deleted(self):
        """
        Mozilla Foundation Users are not deleted
        """

        call_command("delete_non_staff", "--now")

        self.assertEqual(User.objects.count(), 1)
