from django.conf import settings
from django.core.management.base import BaseCommand
from wagtail.models import Site

"""
Reassigns MoFo staging site hostnames after copying over the prod DB.

Reads two comma-separated settings:
  - settings.PROD_HOSTNAMES
  - settings.STAGING_HOSTNAMES

Loops through the prod_hostnames list, and updates the site's hostname with its
matching staging hostname.
"""


class Command(BaseCommand):
    print("Reassigning staging hostnames...")

    def handle(self, **options):

        prod_hostnames = settings.PROD_HOSTNAMES.split(",")
        staging_hostnames = settings.STAGING_HOSTNAMES.split(",")

        for prod_hostname in prod_hostnames:
            hostname = prod_hostname.strip()
            print(f"Finding site with hostname: `{hostname}`")
            site = Site.objects.filter(hostname=hostname.strip()).first()
            if site:
                staging_hostname = staging_hostnames[prod_hostnames.index(prod_hostname)].strip()
                print(f"Updating site to hostname: `{staging_hostname}`")
                site.hostname = staging_hostname
                site.save()
            else:
                print(f"No Wagtail Site found with hostname '{hostname}'.")
