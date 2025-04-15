from django.contrib.auth import get_user_model
from social_core.exceptions import AuthForbidden

User = get_user_model()


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
