from django.core.management.base import BaseCommand, CommandError
from django.conf import settings
import os
import heroku3
import requests

from wagtail.core.models import Site

REVIEW_APP_DOMAIN = settings.REVIEW_APP_DOMAIN
CLOUDFLARE_ZONE_ID = settings.REVIEW_APP_CLOUDFLARE_ZONE_ID
CLOUDFLARE_TOKEN = settings.REVIEW_APP_CLOUDFLARE_TOKEN
HEROKU_API_KEY = settings.REVIEW_APP_HEROKU_API_KEY


class CloudflareAPI:
    CLOUDFLARE_API_BASE = "https://api.cloudflare.com/client/v4/"

    def _build_headers(self):
        return {
            "Authorization": f"Bearer {CLOUDFLARE_TOKEN}",
        }

    def create_record(self, *, zone, hostname, type, content):
        payload = {
            "type": type,
            "name": hostname,
            "content": content,
        }
        r = requests.post(
            f"{self.CLOUDFLARE_API_BASE}zones/{zone}/dns_records",
            json=payload,
            headers=self._build_headers(),
        )
        r.raise_for_status()
        return r.json()

    def delete_record(self, *, zone, record_id):
        r = requests.delete(
            f"{self.CLOUDFLARE_API_BASE}zones/{zone}/dns_records/{record_id}",
            headers=self._build_headers(),
        )
        r.raise_for_status()
        return r.json()

    def get_records(self, *, zone):
        r = requests.get(
            f"{self.CLOUDFLARE_API_BASE}/zones/{CLOUDFLARE_ZONE_ID}/dns_records",
            headers=self._build_headers(),
        )
        r.raise_for_status()
        return r.json()


class Command(BaseCommand):
    help = "Create DNS records for review apps in Cloudflare"

    def get_domain_site_mapping(self):
        """Return a mapping of Site object names to the hostname that should be created for them"""
        app_name = os.environ.get("HEROKU_APP_NAME")
        return {
            "Foundation Home Page": f"{app_name}.{REVIEW_APP_DOMAIN}",
            "Mozilla Festival": f"mozfest-{app_name}.{REVIEW_APP_DOMAIN}",
        }

    def add_dns_records(self):
        """Prepare records to be added for each review app Site required"""
        heroku = heroku3.from_key(HEROKU_API_KEY)
        app_name = os.environ.get("HEROKU_APP_NAME")
        app = heroku.apps()[app_name]

        mapping = {}

        for domain in self.get_domain_site_mapping().values():
            heroku_domains = app.domains()

            # If the domain already exists in Heroku, delete it first
            if domain in [domain.hostname for domain in heroku_domains]:
                app.remove_domain(domain)

            sni_endpoint_id = None
            for sni_endpoint in app.sni_endpoints():
                for cert_domain in sni_endpoint.ssl_cert.cert_domains:
                    # check root or wildcard
                    if cert_domain in domain or cert_domain[1:] in domain:
                        sni_endpoint_id = sni_endpoint.id

            heroku_domain = app.add_domain(domain, sni_endpoint_id)
            mapping[domain] = heroku_domain.cname

        has_acm = any(domain.acm_status for domain in app.domains())
        if not has_acm:
            app._h._http_resource(
                method="POST", resource=("apps", app.id, "acm")
            ).raise_for_status()

        cloudflare = CloudflareAPI()
        for hostname, target in mapping.items():
            cloudflare.create_record(
                zone=CLOUDFLARE_ZONE_ID, hostname=hostname, type="CNAME", content=target
            )

    def remove_dns_records(self):
        """Prepare records to be removed for each review app Site"""
        app_name = os.environ.get("HEROKU_APP_NAME")
        heroku = heroku3.from_key(HEROKU_API_KEY)
        app = heroku.apps()[app_name]
        heroku_domains = app.domains()

        cloudflare = CloudflareAPI()
        existing_records = cloudflare.get_records(zone=CLOUDFLARE_ZONE_ID)
        existing_records_by_name = {
            record["name"]: record["id"] for record in existing_records
        }

        for domain in heroku_domains:
            record_id = existing_records_by_name.get(domain.hostname)
            cloudflare.delete_record(zone=CLOUDFLARE_ZONE_ID, record_id=record_id)

    def update_site_hostnames(self):
        """Find the relevant sites in Wagtail and update their hostnames to the new domains"""
        domain_site_mapping = self.get_domain_site_mapping()
        for site_name, domain in domain_site_mapping.items():
            site = Site.objects.get(site_name=site_name)
            site.hostname = domain
            site.port = 80
            site.save()

    def add_arguments(self, parser):
        parser.add_argument("action", type=str)

    def handle(self, *args, **options):
        action = options["action"]

        if not HEROKU_API_KEY or not REVIEW_APP_DOMAIN:
            raise CommandError(
                "Please set REVIEW_APP_HEROKU_API_KEY and REVIEW_APP_DOMAIN"
            )

        if action == "create":
            print("Setting up DNS records and Sites for review app")
            self.add_dns_records()
            self.update_site_hostnames()
        elif action == "teardown":
            print("Removing DNS records for review app")
            self.remove_dns_records()
