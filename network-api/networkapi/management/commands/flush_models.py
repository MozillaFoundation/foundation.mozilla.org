from django.core.management.base import BaseCommand
from wagtail.images import get_image_model

# Models
from wagtail.models import Page as WagtailPage
from wagtail.models import Site as WagtailSite

from networkapi.highlights.models import Highlight
from networkapi.news.models import News
from networkapi.wagtailpages.models import CTA

Image = get_image_model()
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
