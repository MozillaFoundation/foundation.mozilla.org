# The Wagtail group that grants access to legacy content alongside superusers
LEGACY_GROUP_NAME = "access/legacy content editor"


def is_legacy_authorized(user):
    """Return True if the user can access legacy content (superuser or legacy group member)."""
    # Superusers always have access
    if user.is_superuser:
        return True

    # Check if the user belongs to the legacy content editor group
    return user.groups.filter(name=LEGACY_GROUP_NAME).exists()
