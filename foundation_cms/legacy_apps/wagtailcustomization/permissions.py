LEGACY_GROUP_NAME = "access/legacy content editor"


def is_legacy_authorized(user):
    """Return True if the user can access legacy content (superuser or legacy group member)."""
    if user.is_superuser:
        return True
    return user.groups.filter(name=LEGACY_GROUP_NAME).exists()
