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

    is_review_app = getattr(settings, "REVIEW_APP_DOMAIN", None)
    group_name = "Administrators" if is_review_app else DEFAULT_GROUP_NAME

    with transaction.atomic():
        try:
            group = Group.objects.get(name=group_name)
            user.groups.add(group)
        except ObjectDoesNotExist:
            logging.warning(
                "Default group '%s' not found; user %s not assigned.",
                group_name,
                user,
            )
            return
