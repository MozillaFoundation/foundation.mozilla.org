from django.core.management.base import BaseCommand
from foundation_cms.legacy_apps.wagtailpages.pagemodels.campaigns import CTA
from foundation_cms.snippets.models .newsletter_signup import NewsletterSignup


class Command(BaseCommand):
    help = "Update all CTA and NewsletterSignup objects with outdated newsletter slugs."

    def handle(self, *args, **options):
        # Update CTABase combined slug
        cta_combined = CTA.objects.filter(
            newsletter__iexact="mozilla-foundation,mozilla-festival"
        ).update(newsletter="mozilla-festival")

        # Update CTABase single slug
        cta_single = CTA.objects.filter(
            newsletter__iexact="mozilla-foundation"
        ).update(newsletter="mozilla-foundation")

        # Update NewsletterSignup combined slug
        ns_combined = NewsletterSignup.objects.filter(
            newsletter__iexact="mozilla-foundation,mozilla-festival"
        ).update(newsletter="mozilla-festival")

        # Update NewsletterSignup single slug
        ns_single = NewsletterSignup.objects.filter(
            newsletter__iexact="mozilla-foundation"
        ).update(newsletter="mozilla-foundation")

        self.stdout.write(self.style.SUCCESS(
            f"Updated {cta_combined} CTAs to 'mozillafestivalorg' and {cta_single} CTAs to 'mozillafoundationorg'."
        ))
        self.stdout.write(self.style.SUCCESS(
            f"Updated {ns_combined} NewsletterSignups to 'mozillafestivalorg' and {ns_single} NewsletterSignups to 'mozillafoundationorg'."
        ))
        self.stdout.write(self.style.SUCCESS("Done."))