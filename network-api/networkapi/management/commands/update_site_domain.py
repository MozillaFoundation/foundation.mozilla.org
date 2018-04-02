from django.core.management.base import BaseCommand
from django.contrib.sites.models import Site


class Command(BaseCommand):
    help = 'update the default django site domain to localhost:8000'

    def handle(self, *args, **options):
        site = Site.objects.get(id=1)
        site.domain = 'localhost:8000'
        site.save()
