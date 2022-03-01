from django.core.management.base import BaseCommand

# Models
from wagtail.core.models import (
    Page as WagtailPage,
    Site as WagtailSite
)
from wagtail.images.models import Image

from networkapi.highlights.models import Highlight
from networkapi.news.models import News
from networkapi.people.models import (
    Person,
    Affiliation,
    InternetHealthIssue,
)
from networkapi.wagtailpages.models import CTA


class Command(BaseCommand):
    help = 'Flush the models from the database'

    def handle(self, *args, **options):

        self.stdout.write('Flushing models from the database...')

        self.stdout.write('Dropping Image objects...')
        Image.objects.all().delete()

        self.stdout.write('Dropping Highlight objects...')
        Highlight.objects.all().delete()

        self.stdout.write('Dropping News objects...')
        News.objects.all().delete()

        self.stdout.write('Dropping Person objects...')
        Person.objects.all().delete()

        self.stdout.write('Dropping InternetHealthIssue objects...')
        InternetHealthIssue.objects.all().delete()

        self.stdout.write('Dropping Affiliation objects...')
        Affiliation.objects.all().delete()

        self.stdout.write('Dropping Wagtail CTAs...')
        CTA.objects.all().delete()

        self.stdout.write('Dropping all Pages')
        WagtailPage.objects.exclude(id=1).delete()

        try:
            print('Dropping Mozfest Site...')
            WagtailSite.objects.get(site_name='Mozilla Festival').delete()
        except WagtailSite.DoesNotExist:
            pass

        self.stdout.write(self.style.SUCCESS('Done!'))
