from django.core.management.base import BaseCommand
from wagtail.images.models import Image

# Models
from wagtail.models import Page as WagtailPage
from wagtail.models import Site as WagtailSite

from foundation_cms.legacy_apps.highlights.models import Highlight
from foundation_cms.legacy_apps.news.models import News
from foundation_cms.legacy_apps.wagtailpages.models import CTA


class Command(BaseCommand):
    help = "Flush the models from the database"

    def handle(self, *args, **options):
        self.stdout.write("Flushing models from the database...")

        self.stdout.write("Dropping Image objects...")
        Image.objects.all().delete()

        self.stdout.write("Dropping Highlight objects...")
        Highlight.objects.all().delete()

        self.stdout.write("Dropping News objects...")
        News.objects.all().delete()

        self.stdout.write("Dropping Wagtail CTAs...")
        CTA.objects.all().delete()

        self.stdout.write("Dropping all Pages")
        WagtailPage.objects.exclude(id=1).delete()

        try:
            print("Dropping Mozfest Site...")
            WagtailSite.objects.get(site_name="Mozilla Festival").delete()
        except WagtailSite.DoesNotExist:
            pass

        try:
            print("Dropping Donate Site...")
            WagtailSite.objects.get(site_name="Donate Now").delete()
        except WagtailSite.DoesNotExist:
            pass

        self.stdout.write(self.style.SUCCESS("Done!"))
