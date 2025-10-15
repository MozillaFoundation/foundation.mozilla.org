import logging

from django.conf import settings
from django.contrib.auth.models import Permission
from wagtail.models import GroupPagePermission

logger = logging.getLogger(__name__)


def filter_notification_recipients(revision, notification, recipients):
    """
    Filters workflow notification recipients based on environment settings.
    Superusers are already filtered by WAGTAILADMIN_NOTIFICATION_INCLUDE_SUPERUSERS.

    Args:
        revision: Page revision object
        notification: Notification type ('submitted', 'approved', 'rejected', 'updated_comments')
        recipients: Initial list of recipients from Wagtail's default system

    Returns:
        Filtered list of users who should receive the notification
    """

    include_page_perms = getattr(settings, "WAGTAILADMIN_NOTIFICATION_INCLUDE_USERS_WITH_PAGE_PERMISSIONS", True)
    filtered_recipients = set(_filter_basic_eligibility(recipients))

    if include_page_perms:
        page_permission_users = _get_page_permission_users(revision)
        filtered_recipients.update(page_permission_users)

    final_recipients = list(filtered_recipients)

    return final_recipients


def _filter_basic_eligibility(users):
    """Applies basic eligibility checks: active status and email presence."""
    return [user for user in users if user.is_active and user.email]


def _get_page_permission_users(revision):
    """
    Gets users with relevant page permissions.
    Finds users with edit/publish permissions on the page hierarchy.
    """
    page = revision.as_page_object()
    page_hierarchy = page.get_ancestors(inclusive=True)

    relevant_permissions = Permission.objects.filter(codename__in=["add_page", "change_page", "publish_page"])

    page_permissions = GroupPagePermission.objects.filter(
        page__in=page_hierarchy, permission__in=relevant_permissions
    ).select_related("group", "permission")

    page_users = set()
    for permission in page_permissions:
        group_users = permission.group.user_set.filter(is_active=True, email__isnull=False).exclude(email="")

        page_users.update(group_users)

    return list(page_users)
