from functools import cached_property

from django.contrib.auth import get_user_model
from django.db.models import Q
from wagtail.permission_policies.base import ModelPermissionPolicy
from wagtail.snippets.views.snippets import SnippetViewSet

LEGACY_GROUP_NAME = "access/legacy content editor"


def is_legacy_authorized(user):
    """Return True if the user can access legacy content (superuser or legacy group member)."""
    if user.is_superuser:
        return True
    return user.groups.filter(name=LEGACY_GROUP_NAME).exists()


class LegacyContentPermissionPolicy(ModelPermissionPolicy):
    """
    Permission policy that restricts access to superusers and members of the
    'access/legacy content editor' group, regardless of Django model permissions.
    """

    def user_has_permission(self, user, action):
        return is_legacy_authorized(user)

    def user_has_any_permission(self, user, actions):
        return is_legacy_authorized(user)

    def users_with_any_permission(self, actions):
        User = get_user_model()
        return User.objects.filter(Q(is_superuser=True) | Q(groups__name=LEGACY_GROUP_NAME)).distinct()


class LegacySnippetViewSet(SnippetViewSet):
    """
    Base SnippetViewSet for legacy snippets. Restricts access to superusers and
    members of the 'access/legacy content editor' group. Wagtail automatically
    hides the menu item when the user has no permission.
    """

    @cached_property
    def permission_policy(self):
        return LegacyContentPermissionPolicy(self.model)
