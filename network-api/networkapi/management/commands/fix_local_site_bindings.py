from django.core.management.base import BaseCommand
from wagtail.core.models import Site

class Command(BaseCommand):
    help = 'Ensure site bindings are for localhost (e.g. for after a db copy)'

    def handle(self, *args, **options):
        for site in Site.objects.all():
            if site.is_default_site:
                site.hostname = 'localhost'
            else:
                site.hostname = 'mozfest.localhost'
            site.port = 8000
            site.save()
