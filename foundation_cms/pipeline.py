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
    with transaction.atomic():
        try:
            group = Group.objects.get(name=DEFAULT_GROUP_NAME)
        except ObjectDoesNotExist:
            import logging

            logging.warning(f"Default group '{DEFAULT_GROUP_NAME}' not found; user {user} not assigned.")
            return

        user.groups.add(group)
