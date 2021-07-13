"""
Management command called during the Heroku Review App post-deployment phase.
Creates an admin user and prints the password to the build logs.
"""
from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import os
import boto3
import heroku3

from wagtail.core.models import Site

REVIEW_APP_ROUTE_53_ZONE = settings.REVIEW_APP_ROUTE_53_ZONE
REVIEW_APP_HEROKU_API_KEY = settings.REVIEW_APP_HEROKU_API_KEY


class Command(BaseCommand):
    help = "Create a superuser for use on Heroku review apps"

    def get_domain_site_mapping(self):
        """ Return a mapping of Site object names to the hostname that should be created for them """
        app_name = os.environ.get("HEROKU_APP_NAME")
        return {
            "Mozilla Festival": f"{app_name}.{REVIEW_APP_ROUTE_53_ZONE}",
            "Foundation Home Page": f"mozfest-{app_name}.{REVIEW_APP_ROUTE_53_ZONE}",
        }

    def get_hosted_zone_id(self):
        """ Get the Route 53 hosted zone from AWS based on the name given in REVIEW_APP_ROUTE_53_ZONE """
        client = boto3.client("route53")
        zones = client.list_hosted_zones_by_name(DNSName=REVIEW_APP_ROUTE_53_ZONE)

        if not zones or not zones["HostedZones"]:
            raise CommandError(
                "Failed to retrieve Route 53 zone. Make sure REVIEW_APP_ROUTE_53_ZONE is set correctly."
            )

        if zones["HostedZones"][0]["Name"] != REVIEW_APP_ROUTE_53_ZONE + ".":
            raise CommandError("AWS API returned mismatched domain for review app")

        return zones["HostedZones"][0]["Id"]

    def do_dns_changes(self, mapping, action="CREATE"):
        """ Given a mapping of hostnames to their target CNAME,
        follow the given action to make these changes in Route 53
        """
        zone_id = self.get_hosted_zone_id()
        client = boto3.client("route53")
        changes = [
            {
                "Action": action,
                "ResourceRecordSet": {
                    "Name": hostname,
                    "ResourceRecords": [{"Value": target}],
                    "TTL": 60,
                    "Type": "CNAME",
                },
            }
            for hostname, target in mapping.items()
        ]
        client.change_resource_record_sets(
            HostedZoneId=zone_id, ChangeBatch={"Changes": changes},
        )

    def add_dns_records(self):
        """ Prepare records to be added for each review app Site required """
        heroku = heroku3.from_key(REVIEW_APP_HEROKU_API_KEY)
        app_name = os.environ.get("HEROKU_APP_NAME")
        app = heroku.apps()[app_name]

        mapping = {}

        for domain in self.get_domain_site_mapping.values():
            heroku_domains = app.domains()

            # If the domain already exists in Heroku, delete it first
            if domain in [domain.hostname for domain in heroku_domains]:
                app.remove_domain(domain)

            heroku_domain = app.add_domain(domain)
            mapping[domain] = heroku_domain.cname

        self.do_dns_changes(mapping)

    def remove_dns_records(self):
        """ Prepare records to be removed for each review app Site """
        app_name = os.environ.get("HEROKU_APP_NAME")
        heroku = heroku3.from_key(REVIEW_APP_HEROKU_API_KEY)
        app = heroku.apps()[app_name]
        heroku_domains = app.domains()

        mapping = {
            domain.hostname: domain.cname for domain in heroku_domains if domain.cname
        }

        self.do_dns_changes(mapping, action="DELETE")

    def update_site_hostnames(self):
        """ Find the relevant sites in Wagtail and update their hostnames to the new domains """
        domain_site_mapping = self.get_domain_site_mapping()
        for site_name, domain in domain_site_mapping.items():
            site = Site.objects.get(site_name)
            site.hostname = domain
            site.save()

    def add_arguments(self, parser):
        parser.add_argument("action", type=str)

    def handle(self, *args, **options):
        action = options["action"]

        if not REVIEW_APP_HEROKU_API_KEY or not REVIEW_APP_ROUTE_53_ZONE:
            raise CommandError(
                "Please set REVIEW_APP_HEROKU_API_KEY and REVIEW_APP_ROUTE_53_ZONE"
            )

        if action == "create":
            print("Setting up DNS records and Sites for review app")
            self.add_dns_records()
            self.update_site_hostnames()
        elif action == "teardown":
            print("Removing DNS records for review app")
            self.remove_dns_records()
