import logging

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from social_core.exceptions import AuthForbidden

User = get_user_model()
DEFAULT_GROUP_NAME = "access/content editor: no publishing access"


def associate_by_email(backend, details, uid, user=None, *args, **kwargs):
    """
    Associates users by email address to prevent duplicate user creation
    across different social providers like Google and Auth0.
    """
    if user:
        return {"user": user}

    email = details.get("email")
    if not email:
        raise AuthForbidden(backend)

    try:
        existing_user = User.objects.get(email=email)
        return {"user": existing_user}
    except User.DoesNotExist:
        return None


def assign_default_role(backend, user, is_new=False, **kwargs):
    if not is_new:
        return

    is_review_app = bool(getattr(settings, "REVIEW_APP_DOMAIN", None))

    with transaction.atomic():
        if is_review_app and settings.APP_ENVIRONMENT == "Review":
            # assign new SSO'ed users full access for review app environments only
            user.is_superuser = True
            user.is_staff = True
            user.save(update_fields=["is_superuser", "is_staff"])
            logging.info("Granted superuser/staff to %s (review app)", user)
            return

        # otherwise, assign new SSO'ed users a default group assignment
        try:
            group = Group.objects.get(name=DEFAULT_GROUP_NAME)
            user.groups.add(group)
        except ObjectDoesNotExist:
            logging.warning(
                "Default group '%s' not found; user %s not assigned.",
                DEFAULT_GROUP_NAME,
                user,
            )
            return
