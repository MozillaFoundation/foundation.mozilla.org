import json
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand
from wagtail.models import Page, Site

from foundation_cms.base.utils.helpers import (
    inject_images_into_data,
    load_manifest_with_partials,
    to_streamfield_value,
)
from foundation_cms.core.factories.home_factory import HomePageFactory
from foundation_cms.core.models.home_page import HomePage

BASE_DIR = Path(__file__).resolve().parents[3] / "core" / "factories" / "data"
HOMEPAGE_DIR = BASE_DIR / "homepage"
IMAGE_DIR = HOMEPAGE_DIR / "images"  # ✅ New location under homepage


class Command(BaseCommand):
    help = "Load homepage from JSON and register it as the Wagtail default Site root."

    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true", help="Delete and replace existing homepage if it exists.")

    def handle(self, *args, **options):
        slug = "redesign-home"
        manifest_path = HOMEPAGE_DIR / "manifest.json"
        image_manifest_path = HOMEPAGE_DIR / "image_manifest.json"

        REVIEW_APP_NAME = getattr(settings, "HEROKU_APP_NAME", None)
        REVIEW_APP_HOSTNAME = f"{REVIEW_APP_NAME}.herokuapp.com" if REVIEW_APP_NAME else None

        # Ensure the root page exists
        root = Page.get_first_root_node()
        if not root.pk:
            root.save()

        # Remove existing homepage if requested via --force option
        existing = HomePage.objects.child_of(root).filter(slug=slug).first()
        if existing:
            if options["force"]:
                self.stdout.write(f"Deleting existing homepage at slug '{slug}'...")
                existing.delete()
            else:
                self.stdout.write(self.style.WARNING("Homepage already exists — use --force to replace."))
                return

        # Load raw json
        with open(manifest_path, "r", encoding="utf-8") as f:
            raw = load_manifest_with_partials(manifest_path)

        # Grab image_manifest file and inject image data into homepage JSON
        with open(image_manifest_path, "r", encoding="utf-8") as f:
            image_manifest = json.load(f)

        # Upload images from manifest, and inject data into the raw json file for page generation
        raw = load_manifest_with_partials(manifest_path)
        raw = inject_images_into_data(raw, image_manifest, IMAGE_DIR)

        self.stdout.write("Creating HomePage from JSON...")

        # StreamBlock conversion
        model_instance = HomePageFactory._meta.model()  # get a model instance of homepage

        # Build the homepage
        homepage = HomePageFactory.build(
            title=raw.get("title", "Redesign Homepage"),
            slug=slug,
            hero_accordion=to_streamfield_value(  # assign values based on json data
                raw["hero_accordion"],
                stream_block=model_instance.hero_accordion.stream_block,
            ),
            body=to_streamfield_value(  # assign values based on json data
                raw.get("body", []),
                stream_block=model_instance.body.stream_block,
            ),
        )

        root.add_child(instance=homepage)
        homepage.save_revision().publish()
        self.stdout.write(self.style.SUCCESS("HomePage created and published."))

        # Set as default site root
        try:
            site = Site.objects.get(is_default_site=True)
            site.root_page = homepage
            site.hostname = REVIEW_APP_HOSTNAME or "localhost"
            site.port = 80 if REVIEW_APP_NAME else 8000
            site.site_name = "Redesign Homepage"
            site.save()
            self.stdout.write(self.style.SUCCESS("Updated existing default Site"))
        except Site.DoesNotExist:
            Site.objects.create(
                hostname=REVIEW_APP_HOSTNAME or "localhost",
                port=80 if REVIEW_APP_NAME else 8000,
                root_page=homepage,
                site_name="Redesign Homepage",
                is_default_site=True,
            )
            self.stdout.write(self.style.SUCCESS("Created new default Site"))

        self.stdout.write(self.style.SUCCESS("Homepage + Site setup complete."))
