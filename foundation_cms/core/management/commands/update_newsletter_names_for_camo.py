from django.core.management.base import BaseCommand

from foundation_cms.legacy_apps.wagtailpages.pagemodels.campaigns import CTA
from foundation_cms.snippets.models.newsletter_signup import NewsletterSignup


class Command(BaseCommand):
    help = (
        "Update all CTA and NewsletterSignup objects with outdated newsletter slugs. "
        "Use --reverse to go from the new slugs back to the old ones."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            "--reverse",
            action="store_true",
            help="Reverse the mapping (new → old).",
        )

    def handle(self, *args, **options):
        # Base mappings (old → new)
        mappings = [
            ("mozilla-foundation,mozilla-festival", "mozillafestivalorg"),
            ("mozilla-foundation", "mozillafoundationorg"),
            ("common-voice", "commonvoicemozillaorg"),
        ]

        if options["reverse"]:
            mappings = [(new, old) for (old, new) in mappings]
            self.stdout.write(self.style.WARNING("Running in REVERSE mode."))

        total_cta = 0
        total_ns = 0

        for old_slug, new_slug in mappings:
            cta_count = CTA.objects.filter(newsletter__iexact=old_slug).update(newsletter=new_slug)
            ns_count = NewsletterSignup.objects.filter(newsletter__iexact=old_slug).update(newsletter=new_slug)

            total_cta += cta_count
            total_ns += ns_count

            self.stdout.write(self.style.SUCCESS(f"CTA: '{old_slug}' → '{new_slug}': {cta_count} updated."))
            self.stdout.write(
                self.style.SUCCESS(f"NewsletterSignup: '{old_slug}' → '{new_slug}': {ns_count} updated.")
            )

        direction = "reverted" if options["reverse"] else "updated"
        self.stdout.write(
            self.style.SUCCESS(
                f"Done. {direction.capitalize()} {total_cta} CTA(s) and {total_ns} NewsletterSignup(s)."
            )
        )
