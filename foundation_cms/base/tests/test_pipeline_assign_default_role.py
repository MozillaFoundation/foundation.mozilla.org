from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.test import TestCase

from foundation_cms.pipeline import DEFAULT_GROUP_NAME, assign_default_role

User = get_user_model()


class AssignDefaultRoleTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="editor", email="admin@example.com", password="x")
        self.group, _ = Group.objects.get_or_create(name=DEFAULT_GROUP_NAME)

    def test_assigns_when_group_exists_and_is_new(self):
        assign_default_role(backend=None, user=self.user, is_new=True)
        # Confirm user added to the group
        self.assertTrue(self.user.groups.filter(id=self.group.id).exists())

    def test_bails_when_group_missing(self):
        unknown_group = "A GROUP NAME THAT DOES NOT EXIST"
        self.assertFalse(Group.objects.filter(name=unknown_group).exists())
        assign_default_role(backend=None, user=self.user, is_new=True)
        # Confirm user not added to the group, and group still doesn't exist (no implicit create)
        self.assertFalse(self.user.groups.filter(name=unknown_group).exists())
        self.assertFalse(Group.objects.filter(name=unknown_group).exists())
