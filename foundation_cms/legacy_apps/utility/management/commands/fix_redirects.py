from django.core.management.base import BaseCommand
from django.db.utils import IntegrityError
from wagtail.contrib.redirects.models import Redirect
from wagtail.models import Locale

# Define the list of valid values to check against
LOCALES = Locale.objects.all().values_list("language_code", flat=True)


def is_starting_with_language_code(url_path):
    """
    This function takes a URL path as input and checks if the first part of the path is a valid language code.

    Args:
        url_path (str): A string representing the URL path to be checked.

    Returns:
        bool: True if the first part of the URL path is a valid language code, otherwise False.

    Example:
        >>> is_starting_with_language_code("/en/example")
        True
        >>> is_starting_with_language_code("/fr/example")
        True
        >>> is_starting_with_language_code("/example")
        False
    """

    # Extract the first part of the URL path
    path_parts = url_path.split("/")
    first_part = path_parts[1] if len(path_parts) > 1 else ""

    # Check if the first part of the URL path is in the valid list of values
    if first_part in LOCALES:
        # do nothing
        return True
    else:
        # Create a redirect for this path
        return False


class Command(BaseCommand):
    help = "Creates redirects for each locale for each redirect if it doesn't exist."

    def handle(self, *args, **options):
        redirects = Redirect.objects.all()

        for redirect in redirects:
            has_locale_redirect = is_starting_with_language_code(url_path=redirect.old_path)
            if not has_locale_redirect:
                # create a new redirect for each locale, it will be a copy
                # of the original redirect but with the locale prefix
                for locale in LOCALES:
                    # first check if the redirect already exists, this will happen
                    # if we run this code more than once
                    if not redirects.filter(old_path=f"/{locale}{redirect.old_path}").exists():
                        try:
                            new_redirect = Redirect.objects.create(
                                old_path=f"/{locale}{redirect.old_path}",
                                site_id=redirect.site_id,
                                is_permanent=redirect.is_permanent,
                                redirect_page_id=redirect.redirect_page_id,
                                redirect_page_route_path=redirect.redirect_page_route_path,
                                redirect_link=redirect.redirect_link,
                            )
                            print(f"creating new redirect for {redirect.old_path}")
                            print(f"new redirect old_path: /{locale}{redirect.old_path}")
                            print(f" new redirect page_id: {redirect.redirect_page_id}")
                            print(f" new redirect redirect_page_route_path: {redirect.redirect_page_route_path}")
                            print(f" new redirect redirect_link: {redirect.redirect_link}")
                            new_redirect.save()
                        except IntegrityError:
                            print(f"Redirect already exists: {redirect.old_path}")
                            pass

        redirects = Redirect.objects.all()
