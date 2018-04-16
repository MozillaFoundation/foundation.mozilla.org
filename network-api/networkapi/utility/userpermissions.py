from django.contrib.sites.models import Site
from django.contrib.auth.models import Group
from mezzanine.core.models import SitePermission


def is_mozilla_address(email):
    """
    This function determines whether a particular email address is a
    mozilla address or not. We strictly control mozilla.com and
    mozillafoundation.org addresses, and so filtering on the email
    domain section using exact string matching is acceptable.
    """
    if email is None:
        return False

    parts = email.split('@')
    domain = parts[1]

    if domain == 'mozilla.org':
        return True

    if domain == 'mozilla.com':
        return True

    if domain == 'mozillafoundation.org':
        return True

    return False


def add_user_to_main_site(user):
    """
    make sure a user has permissions to look at the main site.
    """

    sites = Site.objects.all()
    main_site = sites[0]

    permissions = False

    try:
        siteperms = SitePermission.objects.filter(user=user)
        permissions = siteperms[0]
    except Exception:
        permissions = SitePermission.objects.create(user=user)

    permissions.sites.add(main_site)


def assign_group_policy(user, name):
    """
    add a specific group policy to a user's list of group policies.
    """
    try:
        group = Group.objects.get(name=name)
        user.groups.add(group)
        user.save()
    except NameError:
        print("group", name, "not found")
        pass


def set_user_permissions(backend, user, response, *args, **kwargs):
    """
    This is a social-auth pipeline function for automatically
    setting permissions when a user logs in. Any code here triggers
    at the end of the authentication pipeline.
    """

    # One thing that always needs to happen is to add the
    # user to this site, so that their permissions (if we
    # assign them any) will kick in.

    add_user_to_main_site(user)
