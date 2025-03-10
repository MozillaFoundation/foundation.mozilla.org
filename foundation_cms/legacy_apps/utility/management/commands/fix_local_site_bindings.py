from django.core.management.base import BaseCommand
from wagtail.models import Site

from foundation_cms.legacy_apps.donate.models import DonateLandingPage
from foundation_cms.legacy_apps.mozfest.models import MozfestHomepage
from foundation_cms.legacy_apps.wagtailpages.models import Homepage


class Command(BaseCommand):
    help = "Ensure site bindings are for localhost (e.g. for after a db copy)"

    def handle(self, *args, **options):
        for site in Site.objects.all():
            root_page = site.root_page.specific

            if isinstance(root_page, Homepage):
                site.hostname = "localhost"
            elif isinstance(root_page, MozfestHomepage):
                site.hostname = "mozfest.localhost"
            elif isinstance(root_page, DonateLandingPage):
                site.hostname = "donate.localhost"

            site.port = 8000
            site.save()
