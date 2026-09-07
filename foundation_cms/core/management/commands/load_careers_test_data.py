"""
Seed a /careers/ page for QA:

    inv manage "load_careers_test_data"

Content creates the real page by hand in staging and production. Which of the
block's states you see depends on GREENHOUSE_BOARD_TOKEN, not on this command.
"""

from django.core.management.base import BaseCommand, CommandError
from django.db import transaction
from wagtail.models import Locale, Site

from foundation_cms.base.utils.helpers import to_streamfield_value
from foundation_cms.core.models import GeneralPage, HomePage

CAREERS_SLUG = "careers"


class Command(BaseCommand):
    help = "Create a /careers/ General Page holding the Greenhouse job board block, for manual QA."

    def add_arguments(self, parser):
        parser.add_argument(
            "--reset",
            action="store_true",
            help=f"Delete the existing test page (slug {CAREERS_SLUG}) before creating it.",
        )

    def _get_home_page(self):
        site = Site.objects.filter(is_default_site=True).first()
        if not site:
            raise CommandError("No Wagtail Site found. Run `inv manage load_redesign_data` first.")

        parent = site.root_page.specific
        if not isinstance(parent, HomePage):
            raise CommandError("Site root must be a redesign HomePage. Run `inv manage load_redesign_data` first.")

        return parent

    def _build_body(self, page):
        return to_streamfield_value(
            [
                {
                    "type": "title_block",
                    "value": {"title": "Work with us", "style": "shape"},
                },
                {
                    "type": "greenhouse_board",
                    "value": {
                        "empty_heading": "No open roles right now",
                        "empty_description": "<p>We don't have any openings at the moment. "
                        "Please check back soon.</p>",
                        "unavailable_heading": "Our job board is temporarily unavailable",
                        "unavailable_description": "<p>We're having trouble loading our open roles. "
                        "Please try again shortly.</p>",
                        "degraded_notice": "Not seeing our open roles?",
                        "degraded_link_label": "View them on Greenhouse",
                    },
                },
            ],
            stream_block=page.body.stream_block,
        )

    @transaction.atomic
    def handle(self, *args, **options):
        default_locale = Locale.get_default()
        home_page = self._get_home_page()

        if options["reset"]:
            deleted, _ = GeneralPage.objects.filter(slug=CAREERS_SLUG).delete()
            if deleted:
                self.stdout.write(f"Deleted {deleted} existing careers page(s).")

        existing = GeneralPage.objects.filter(slug=CAREERS_SLUG, locale=default_locale).first()
        if existing:
            if not existing.live:
                existing.save_revision().publish()
            self.stdout.write(f"Using existing careers page: /en/{CAREERS_SLUG}/")
            return

        page = GeneralPage(
            title="Careers",
            slug=CAREERS_SLUG,
            seo_title="Careers at Mozilla Foundation",
            search_description="Open roles at Mozilla Foundation.",
            locale=default_locale,
            # Kept off so this fixture does not need hero media to validate.
            show_hero=False,
        )
        page.body = self._build_body(page)

        home_page.add_child(instance=page)
        page.save_revision().publish()

        self.stdout.write(self.style.SUCCESS(f"Created careers page: /en/{CAREERS_SLUG}/"))
