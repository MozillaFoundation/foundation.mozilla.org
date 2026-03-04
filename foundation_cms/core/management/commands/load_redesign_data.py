from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from wagtail.models import Page, Site

from foundation_cms.core.factories.homepage import HomePageFactory
from foundation_cms.navigation.factories import NavigationMenuFactory
from foundation_cms.navigation.models import SiteNavigationMenu

BASE_DIR = Path(__file__).resolve().parents[3] / "core" / "factories" / "data"
HOMEPAGE_DIR = BASE_DIR / "homepage"


class Command(BaseCommand):
    help = "Load homepage from manifest and register it as the Wagtail default Site root."

    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true", help="Delete and replace existing homepage if it exists.")

    def handle(self, *args, **options):
        homepage_slug = "redesign-home"
        REVIEW_APP_NAME = getattr(settings, "HEROKU_APP_NAME", None)
        hostname = f"{REVIEW_APP_NAME}.mofostaging.net" if REVIEW_APP_NAME else "localhost"
        port = 80 if REVIEW_APP_NAME else 8000

        root = Page.get_first_root_node()
        if not root.pk:
            root.save()

        # Build and publish the homepage
        self.stdout.write("Creating HomePage from manifest...")
        homepage = HomePageFactory.create_from_manifest(parent=root, slug=homepage_slug)
        self.stdout.write(self.style.SUCCESS("HomePage created and published."))

        # Assign Site root
        self.stdout.write(self.style.SUCCESS("Assigning redesign HomePage as default."))
        site = self.assign_homepage_as_site_root(homepage, hostname, port)

        self.stdout.write("Generating Navigation Menu via factory...")
        nav_menu = self.create_nav_menu(site)
        self.stdout.write(self.style.SUCCESS(f'Navigation Menu active: "{nav_menu.title}"'))

        self.stdout.write(self.style.SUCCESS("Homepage setup complete."))

    def assign_homepage_as_site_root(self, homepage, hostname, port):
        site = Site.objects.get(is_default_site=True)
        site.root_page = homepage
        site.hostname = hostname
        site.port = port
        site.site_name = "Mozilla Foundation"
        site.save()
        self.stdout.write(self.style.SUCCESS("Created new default Site"))
        return site

    def create_nav_menu(self, site):
        """
        Create a Navigation Menu and set it as the active menu in SiteNavigationMenu.
        """
        settings_obj = SiteNavigationMenu.for_site(site)

        # Create a menu with dropdowns via factory
        nav_menu = NavigationMenuFactory.create(
            title="Main Navigation",
            locale=site.root_page.locale,
        )
        settings_obj.active_navigation_menu = nav_menu
        settings_obj.save()

        return nav_menu
